"""Fuzz and robustness tests for gem replay parsing.

Verifies that malformed, truncated, or garbage input completes without
hanging or crashing with an unhandled exception at the public API level.

Key design contract (from parser.py):
- ``ReplayParser.parse()`` catches all stream-level exceptions internally
  and returns whatever partial state was accumulated. This means bad inputs
  silently return an empty ``ParsedMatch`` rather than raising — by design,
  to support truncated replay analysis.
- ``DemoStream`` raises ``ValueError`` on wrong magic when used directly.
- ``BitReader`` raises ``IndexError`` / similar on reads past end-of-buffer.

These tests verify:
1. ``DemoStream`` raises the right exceptions when used directly.
2. ``gem.parse()`` always returns a ``ParsedMatch`` (never hangs or crashes).
3. ``BitReader`` raises on out-of-bounds reads.
"""

from __future__ import annotations

from pathlib import Path

import pytest

FIXTURE_TRUNCATED = (
    Path(__file__).parent / "fixtures" / "ti14_finals_g1_xg_vs_falcons_truncated.dem"
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
        from gem.stream import DemoStream

        # Empty bytes → wrong magic (0 bytes) → ValueError
        with pytest.raises(ValueError):
            DemoStream(b"")

    def test_wrong_magic(self) -> None:
        from gem.stream import DemoStream

        bad = b"NOTDOTA2" + b"\x00" * 8
        with pytest.raises(ValueError):
            DemoStream(bad)

    def test_header_only_no_messages(self) -> None:
        from gem.stream import DemoStream

        # Valid header, no messages — should yield nothing and not hang.
        with DemoStream(_make_dem_header()) as stream:
            messages = list(stream)
        assert messages == []

    def test_truncated_after_header(self) -> None:
        from gem.stream import DemoStream

        # Header + incomplete varuint — should raise or yield nothing (no hang).
        data = _make_dem_header() + b"\x80"  # incomplete varuint
        with DemoStream(data) as stream:
            try:
                messages = list(stream)
                assert isinstance(messages, list)
            except Exception:
                pass  # any exception is fine — no hang

    def test_truncated_mid_payload(self) -> None:
        from gem.stream import DemoStream

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
        from gem.stream import DemoStream

        # Valid magic, then garbage content — iteration may raise or return partial.
        data = _make_dem_header() + b"\xff" * 256
        with DemoStream(data) as stream:
            try:
                messages = list(stream)
                assert isinstance(messages, list)
            except Exception:
                pass  # no hang


# ---------------------------------------------------------------------------
# gem.parse() robustness — always returns ParsedMatch (never hangs/crashes)
# ---------------------------------------------------------------------------


class TestParseFuzz:
    """gem.parse() resilience: parser.py swallows stream exceptions internally.

    Bad/empty/truncated files return an empty (or partial) ParsedMatch rather
    than raising. The public contract is "no hang, no unhandled crash".
    """

    def test_empty_file(self, tmp_path: Path) -> None:
        """Empty .dem file → parser catches ValueError and returns empty ParsedMatch."""
        import gem
        from gem.models import ParsedMatch

        f = tmp_path / "empty.dem"
        f.write_bytes(b"")
        result = gem.parse(str(f))
        assert isinstance(result, ParsedMatch)

    def test_wrong_magic_file(self, tmp_path: Path) -> None:
        """Wrong magic → parser catches ValueError and returns empty ParsedMatch."""
        import gem
        from gem.models import ParsedMatch

        f = tmp_path / "bad_magic.dem"
        f.write_bytes(b"NOTVALID" + b"\x00" * 8 + b"\xff" * 64)
        result = gem.parse(str(f))
        assert isinstance(result, ParsedMatch)

    def test_nonexistent_file(self, tmp_path: Path) -> None:
        """Nonexistent file → parser catches FileNotFoundError, returns empty ParsedMatch."""
        import gem
        from gem.models import ParsedMatch

        result = gem.parse(str(tmp_path / "does_not_exist.dem"))
        assert isinstance(result, ParsedMatch)

    def test_header_only_file(self, tmp_path: Path) -> None:
        """Valid header with no messages → empty ParsedMatch, no hang."""
        import gem
        from gem.models import ParsedMatch

        f = tmp_path / "header_only.dem"
        f.write_bytes(_make_dem_header())
        result = gem.parse(str(f))
        assert isinstance(result, ParsedMatch)

    def test_garbage_content_file(self, tmp_path: Path) -> None:
        """Valid header + garbage payload → empty ParsedMatch, no hang."""
        import gem
        from gem.models import ParsedMatch

        f = tmp_path / "garbage.dem"
        f.write_bytes(_make_dem_header() + b"\xff" * 1024)
        result = gem.parse(str(f))
        assert isinstance(result, ParsedMatch)

    def test_truncated_fixture(self) -> None:
        """Pre-built truncated fixture parses without hanging."""
        import gem
        from gem.models import ParsedMatch

        if not FIXTURE_TRUNCATED.exists():
            pytest.skip("Truncated fixture not found")

        result = gem.parse(str(FIXTURE_TRUNCATED))
        assert isinstance(result, ParsedMatch)
        # Truncated replay should still extract some partial data
        assert result.match_id >= 0

    def test_truncated_fixture_has_partial_data(self) -> None:
        """Truncated fixture returns partial (non-empty) data, not a completely blank match."""
        import gem

        if not FIXTURE_TRUNCATED.exists():
            pytest.skip("Truncated fixture not found")

        result = gem.parse(str(FIXTURE_TRUNCATED))
        # At minimum the sendtables/entitymanager must have initialised
        # (truncation happens after the header, so some data is available).
        assert result.match_id != 0 or len(result.combat_log) > 0 or len(result.players) == 10


# ---------------------------------------------------------------------------
# BitReader robustness
# ---------------------------------------------------------------------------


class TestBitReaderFuzz:
    """BitReader raises on reads past end-of-buffer."""

    def test_read_bits_past_end(self) -> None:
        from gem.reader import BitReader

        r = BitReader(b"\x00")
        r.read_bits(8)  # consume the single byte
        with pytest.raises((EOFError, IndexError, ValueError, Exception)):
            r.read_bits(1)  # past end

    def test_empty_buffer_raises(self) -> None:
        from gem.reader import BitReader

        r = BitReader(b"")
        with pytest.raises((EOFError, IndexError, ValueError, Exception)):
            r.read_bits(1)

    def test_read_byte_past_end(self) -> None:
        from gem.reader import BitReader

        r = BitReader(b"\xab")
        r.read_bits(8)  # consume all
        with pytest.raises((EOFError, IndexError, ValueError, Exception)):
            r.read_bits(8)  # nothing left
