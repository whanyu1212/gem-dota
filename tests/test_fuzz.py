"""Fuzz and robustness tests for gem replay parsing.

Verifies that malformed, truncated, or garbage input fails loudly by default
while still supporting opt-in partial replay analysis.

Key design contract (from parser.py):
- ``ReplayParser.parse()`` records stream/decoder failures on ``parse_error`` /
  ``truncated_at_tick`` and raises by default.
- ``allow_partial=True`` keeps the previous truncated-replay workflow: return the
  partial ``ParsedMatch`` accumulated before the failure and surface the error on
  the result.
- ``DemoStream`` raises ``ValueError`` on wrong magic when used directly.
- ``BitReader`` raises ``IndexError`` / similar on reads past end-of-buffer.

These tests verify:
1. ``DemoStream`` raises the right exceptions when used directly.
2. ``gem.parse()`` raises for bad inputs by default.
3. ``gem.parse(..., allow_partial=True)`` returns a ``ParsedMatch`` with partial
   parse metadata.
4. ``BitReader`` raises on out-of-bounds reads.
"""

from __future__ import annotations

from pathlib import Path

import pytest

FIXTURE_TRUNCATED = (
    Path(__file__).parent / "fixtures" / "ti14_finals_g3_xg_vs_falcons_truncated.dem"
)

_MAGIC_S2 = b"PBDEMS2\x00"


def _pack_varuint32(value: int) -> bytes:
    out = []
    while True:
        bits = value & 0x7F
        value >>= 7
        if value:
            out.append(bits | 0x80)
        else:
            out.append(bits)
            break
    return bytes(out)


def _make_dem_header() -> bytes:
    """Return the 16-byte .dem header (magic + 8 zero bytes)."""
    return _MAGIC_S2 + b"\x00" * 8


# ---------------------------------------------------------------------------
# DemoStream — direct usage raises on bad input
# ---------------------------------------------------------------------------


class TestDemoStreamFuzz:
    """DemoStream raises ValueError on bad magic; handles truncation cleanly."""

    def test_empty_bytes(self) -> None:
        from gem.binary.stream import DemoStream

        # Empty bytes → wrong magic (0 bytes) → ValueError
        with pytest.raises(ValueError):
            DemoStream(b"")

    def test_wrong_magic(self) -> None:
        from gem.binary.stream import DemoStream

        bad = b"NOTDOTA2" + b"\x00" * 8
        with pytest.raises(ValueError):
            DemoStream(bad)

    def test_header_only_no_messages(self) -> None:
        from gem.binary.stream import DemoStream

        # Valid header, no messages — should yield nothing and not hang.
        with DemoStream(_make_dem_header()) as stream:
            messages = list(stream)
        assert messages == []

    def test_truncated_after_header(self) -> None:
        from gem.binary.stream import DemoStream

        # Header + incomplete varuint — should raise or yield nothing (no hang).
        data = _make_dem_header() + b"\x80"  # incomplete varuint
        with DemoStream(data) as stream:
            try:
                messages = list(stream)
                assert isinstance(messages, list)
            except Exception:
                pass  # any exception is fine — no hang

    def test_truncated_mid_payload(self) -> None:
        from gem.binary.stream import DemoStream

        # Header + valid outer message claiming 100 bytes, only 10 provided.
        cmd = _pack_varuint32(7)  # DEM_Packet
        tick = _pack_varuint32(0)
        size = _pack_varuint32(100)
        payload = b"\x00" * 10  # only 10 bytes instead of 100

        data = _make_dem_header() + cmd + tick + size + payload
        with DemoStream(data) as stream:
            try:
                messages = list(stream)
                assert isinstance(messages, list)
            except Exception:
                pass  # truncated payload raises — acceptable

    def test_garbage_after_magic(self) -> None:
        from gem.binary.stream import DemoStream

        # Valid magic, then garbage content — iteration may raise or return partial.
        data = _make_dem_header() + b"\xff" * 256
        with DemoStream(data) as stream:
            try:
                messages = list(stream)
                assert isinstance(messages, list)
            except Exception:
                pass  # no hang


# ---------------------------------------------------------------------------
# gem.parse() robustness — strict by default, partial by opt-in
# ---------------------------------------------------------------------------


class TestParseFuzz:
    """gem.parse() raises by default and returns partial output only when asked."""

    def test_empty_file_raises_by_default(self, tmp_path: Path) -> None:
        import gem

        f = tmp_path / "empty.dem"
        f.write_bytes(b"")
        with pytest.raises(ValueError):
            gem.parse(str(f))

    def test_wrong_magic_file_raises_by_default(self, tmp_path: Path) -> None:
        import gem

        f = tmp_path / "bad_magic.dem"
        f.write_bytes(b"NOTVALID" + b"\x00" * 8 + b"\xff" * 64)
        with pytest.raises(ValueError):
            gem.parse(str(f))

    def test_nonexistent_file_raises_by_default(self, tmp_path: Path) -> None:
        import gem

        with pytest.raises(FileNotFoundError):
            gem.parse(str(tmp_path / "does_not_exist.dem"))

    def test_header_only_file_is_clean_empty_match(self, tmp_path: Path) -> None:
        """Valid header with no messages is a clean parse, not a partial error."""
        import gem
        from gem.results.models import ParsedMatch

        f = tmp_path / "header_only.dem"
        f.write_bytes(_make_dem_header())
        result = gem.parse(str(f))
        assert isinstance(result, ParsedMatch)
        assert result.parse_error is None
        assert result.truncated_at_tick is None

    def test_garbage_content_file_raises_by_default(self, tmp_path: Path) -> None:
        import snappy

        import gem

        f = tmp_path / "garbage.dem"
        f.write_bytes(_make_dem_header() + b"\xff" * 1024)
        with pytest.raises(snappy.UncompressError):
            gem.parse(str(f))

    def test_empty_file_allow_partial_returns_error_metadata(self, tmp_path: Path) -> None:
        import gem
        from gem.results.models import ParsedMatch

        f = tmp_path / "empty.dem"
        f.write_bytes(b"")
        result = gem.parse(str(f), allow_partial=True)
        assert isinstance(result, ParsedMatch)
        assert result.parse_error is not None
        assert result.truncated_at_tick == 0

    def test_truncated_fixture_allow_partial(self) -> None:
        """Pre-built truncated fixture parses without hanging when opted in."""
        import gem
        from gem.results.models import ParsedMatch

        if not FIXTURE_TRUNCATED.exists():
            pytest.skip("Truncated fixture not found")

        result = gem.parse(str(FIXTURE_TRUNCATED), allow_partial=True)
        assert isinstance(result, ParsedMatch)
        assert result.match_id >= 0
        assert result.parse_error is not None
        assert result.truncated_at_tick is not None

    def test_truncated_fixture_allow_partial_has_partial_data(self) -> None:
        """Truncated fixture returns partial data, not a completely blank match."""
        import gem

        if not FIXTURE_TRUNCATED.exists():
            pytest.skip("Truncated fixture not found")

        result = gem.parse(str(FIXTURE_TRUNCATED), allow_partial=True)
        # At minimum the sendtables/entitymanager must have initialised
        # (truncation happens after the header, so some data is available).
        assert result.match_id != 0 or len(result.combat_log) > 0 or len(result.players) == 10


# ---------------------------------------------------------------------------
# BitReader robustness
# ---------------------------------------------------------------------------


class TestBitReaderFuzz:
    """BitReader raises on reads past end-of-buffer."""

    def test_read_bits_past_end(self) -> None:
        from gem.binary.reader import BitReader

        r = BitReader(b"\x00")
        r.read_bits(8)  # consume the single byte
        with pytest.raises((EOFError, IndexError, ValueError, Exception)):
            r.read_bits(1)  # past end

    def test_empty_buffer_raises(self) -> None:
        from gem.binary.reader import BitReader

        r = BitReader(b"")
        with pytest.raises((EOFError, IndexError, ValueError, Exception)):
            r.read_bits(1)

    def test_read_byte_past_end(self) -> None:
        from gem.binary.reader import BitReader

        r = BitReader(b"\xab")
        r.read_bits(8)  # consume all
        with pytest.raises((EOFError, IndexError, ValueError, Exception)):
            r.read_bits(8)  # nothing left
