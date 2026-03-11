"""Extended tests for gem.string_table — uncovered paths.

Covers:
  - parse_string_table: non-sequential (absolute) index, key-history prefix
    compression, value with compression flag (flags & 0x1), varint_bit_counts
    path, fixed-size user data.
  - handle_create: table registration, _next_index increments, data_compressed
    blob, LZSS guard, empty initial entries.
  - handle_update: update existing key/value, new entry insertion, blank key
    preserves existing key, missing table raises KeyError.

Reference: manta/string_table.go
"""

from __future__ import annotations

import pytest
import snappy

# ---------------------------------------------------------------------------
# Bit-packing helpers (LSB-first, identical convention to test_field_path.py)
# ---------------------------------------------------------------------------


def _pack_bits(bits: list[int]) -> bytes:
    """Pack a list of 0/1 values into LSB-first bytes."""
    padded = bits + [0] * (-len(bits) % 8)
    result = []
    for i in range(0, len(padded), 8):
        byte = 0
        for j in range(8):
            if padded[i + j]:
                byte |= 1 << j
        result.append(byte)
    return bytes(result)


def _append_varuint32(bits: list[int], value: int) -> None:
    """Append a varuint32-encoded value to *bits* in LSB-first bit order.

    The BitReader.read_varuint32 reads bytes via _read_byte (which respects
    the bit buffer), so we must emit the bytes in bit-stream order.
    Each varuint byte is emitted as 8 LSB-first bits.
    """
    while True:
        byte = value & 0x7F
        value >>= 7
        if value:
            byte |= 0x80
        for i in range(8):
            bits.append((byte >> i) & 1)
        if not value:
            break


def _append_string(bits: list[int], s: str) -> None:
    """Append a null-terminated UTF-8 string to *bits* (LSB-first)."""
    for ch in s.encode("utf-8"):
        for i in range(8):
            bits.append((ch >> i) & 1)
    # null terminator
    for _ in range(8):
        bits.append(0)


def _build_entry_bits(
    *,
    incr: bool,
    abs_index: int | None = None,
    key: str | None = None,
    history_pos: int | None = None,
    history_size: int | None = None,
    history_suffix: str = "",
    value: bytes | None = None,
    flags: int = 0,
    compressed: bool = False,
    varint_bit_counts: bool = False,
) -> list[int]:
    """Build the raw bit list for a single string table entry.

    Args:
        incr: True → sequential (increment index).  False → absolute index.
        abs_index: When incr=False, the absolute index to encode (stored as
            abs_index - 1 as a varuint32 — the parser adds +1 back).
        key: Plain string key (no history).  None → has_key=False.
        history_pos: When set, emit a history-prefix key using this ring-buffer
            position and *history_size* prefix length, with *history_suffix*.
        history_size: Number of bytes from history[pos] to use as prefix.
        history_suffix: Suffix appended after the history prefix.
        value: Raw bytes value.  None → has_value=False.
        flags: Table flags (bit 0 enables per-entry compression).
        compressed: When flags&0x1, emit compressed=True boolean before size.
        varint_bit_counts: If True, encode value byte size as ubit_var instead
            of 17-bit fixed.
    """
    bits: list[int] = []

    # Index
    bits.append(1 if incr else 0)
    if not incr:
        # encode (abs_index - 1) as varuint32; parser does: index = read_varuint32() + 1
        _append_varuint32(bits, abs_index - 1)  # type: ignore[arg-type]

    # Key
    if key is not None or history_pos is not None:
        bits.append(1)  # has_key
        if history_pos is not None:
            bits.append(1)  # use_history
            for i in range(5):
                bits.append((history_pos >> i) & 1)
            hs = history_size if history_size is not None else 0
            for i in range(5):
                bits.append((hs >> i) & 1)
            _append_string(bits, history_suffix)
        else:
            bits.append(0)  # no history
            _append_string(bits, key)  # type: ignore[arg-type]
    else:
        bits.append(0)  # no key

    # Value
    if value is not None:
        bits.append(1)  # has_value
        if flags & 0x1:
            bits.append(1 if compressed else 0)
        num_bytes = len(value)
        if varint_bit_counts:
            # ubit_var encoding: low 4 bits + top-2-bit size hint → 0b00 means no extension
            # For small values (< 16 bytes) the low 6 bits with top 2 = 0b00 are enough.
            # ubit_var: read 6 bits; top-2-bit hint in bits[4:6].
            # 0b00xxxx (top 2 = 00): value = low 4 bits directly.
            # We emit 6 bits: the low 4 bits of num_bytes + 0b00 in positions 4-5.
            assert num_bytes < 16, "test helper only supports small ubit_var values"
            for i in range(6):
                bits.append((num_bytes >> i) & 1)
        else:
            for i in range(17):
                bits.append((num_bytes >> i) & 1)
        for byte in value:
            for i in range(8):
                bits.append((byte >> i) & 1)
    else:
        bits.append(0)  # no value

    return bits


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def parse_string_table():
    from gem.string_table import parse_string_table

    return parse_string_table


@pytest.fixture
def string_tables_cls():
    from gem.string_table import StringTables

    return StringTables


@pytest.fixture
def string_table_cls():
    from gem.string_table import StringTable

    return StringTable


# ---------------------------------------------------------------------------
# Tests: parse_string_table — absolute index path
# ---------------------------------------------------------------------------


class TestAbsoluteIndex:
    """Non-sequential (absolute) index reads — incr=False branch."""

    def test_single_absolute_index(self, parse_string_table):
        # Emit one entry with incr=False targeting index 5.
        bits = _build_entry_bits(incr=False, abs_index=5, key="abs_key", value=b"\xab")
        data = _pack_bits(bits)
        items = parse_string_table(
            buf=data,
            num_updates=1,
            name="test",
            user_data_fixed_size=False,
            user_data_size_bits=0,
            flags=0,
            varint_bit_counts=False,
        )
        assert len(items) == 1
        assert items[0].index == 5
        assert items[0].key == "abs_key"
        assert items[0].value == b"\xab"

    def test_absolute_index_zero(self, parse_string_table):
        # abs_index=0 encodes varuint32(-1) which wraps to 0xFFFFFFFF; parser adds 1 → 0.
        # Actually: index = read_varuint32() + 1, so to get index=0 we need varuint32 = -1?
        # No — varuint32 is unsigned, minimum is 0 → index = 0+1 = 1.
        # The lowest absolute index expressible this way is 1 (varuint32=0 → index=1).
        bits = _build_entry_bits(incr=False, abs_index=1, key="zero_abs", value=None)
        data = _pack_bits(bits)
        items = parse_string_table(
            buf=data,
            num_updates=1,
            name="test",
            user_data_fixed_size=False,
            user_data_size_bits=0,
            flags=0,
            varint_bit_counts=False,
        )
        assert items[0].index == 1

    def test_mixed_sequential_and_absolute(self, parse_string_table):
        # Entry 0: incr=True → index=0
        # Entry 1: incr=False, abs_index=10 → index=10
        all_bits = _build_entry_bits(incr=True, key="seq", value=None)
        all_bits += _build_entry_bits(incr=False, abs_index=10, key="jump", value=b"\x01")
        data = _pack_bits(all_bits)
        items = parse_string_table(
            buf=data,
            num_updates=2,
            name="test",
            user_data_fixed_size=False,
            user_data_size_bits=0,
            flags=0,
            varint_bit_counts=False,
        )
        assert items[0].index == 0
        assert items[0].key == "seq"
        assert items[1].index == 10
        assert items[1].key == "jump"


# ---------------------------------------------------------------------------
# Tests: parse_string_table — key-history prefix compression
# ---------------------------------------------------------------------------


class TestKeyHistoryCompression:
    """History ring-buffer prefix compression — use_history=True branch."""

    def test_history_prefix_basic(self, parse_string_table):
        # First entry establishes "instancebaseline" in history at position 0.
        # Second entry uses history[0] with prefix size=8 + suffix "extra".
        # Result: "instance" + "extra" = "instanceextra"
        e0 = _build_entry_bits(incr=True, key="instancebaseline", value=None)
        e1 = _build_entry_bits(
            incr=True,
            history_pos=0,
            history_size=8,
            history_suffix="extra",
            value=None,
        )
        data = _pack_bits(e0 + e1)
        items = parse_string_table(
            buf=data,
            num_updates=2,
            name="test",
            user_data_fixed_size=False,
            user_data_size_bits=0,
            flags=0,
            varint_bit_counts=False,
        )
        assert items[0].key == "instancebaseline"
        assert items[1].key == "instanceextra"

    def test_history_prefix_size_exceeds_key_length(self, parse_string_table):
        # history_size > len(history_key): parser uses the full key as prefix.
        e0 = _build_entry_bits(incr=True, key="abc", value=None)
        e1 = _build_entry_bits(
            incr=True,
            history_pos=0,
            history_size=10,  # > len("abc") = 3
            history_suffix="XYZ",
            value=None,
        )
        data = _pack_bits(e0 + e1)
        items = parse_string_table(
            buf=data,
            num_updates=2,
            name="test",
            user_data_fixed_size=False,
            user_data_size_bits=0,
            flags=0,
            varint_bit_counts=False,
        )
        # size > len(s) → full key + suffix
        assert items[1].key == "abcXYZ"

    def test_history_pos_out_of_range_uses_suffix_only(self, parse_string_table):
        # history_pos >= len(keys) at parse time → key = suffix only.
        # Only one entry has been seen so far (at pos 0), so pos=1 is out of range.
        e0 = _build_entry_bits(incr=True, key="first", value=None)
        e1 = _build_entry_bits(
            incr=True,
            history_pos=5,  # out of range — only index 0 is populated
            history_size=3,
            history_suffix="fallback",
            value=None,
        )
        data = _pack_bits(e0 + e1)
        items = parse_string_table(
            buf=data,
            num_updates=2,
            name="test",
            user_data_fixed_size=False,
            user_data_size_bits=0,
            flags=0,
            varint_bit_counts=False,
        )
        assert items[1].key == "fallback"

    def test_history_ring_buffer_wraps_at_32(self, parse_string_table):
        # Fill 33 entries; key history ring is capped at 32.
        # The 33rd key (index 32) should evict the first (index 0).
        # After that, history[0] refers to what was at index 1 ("k001").
        all_bits: list[int] = []
        for i in range(33):
            all_bits += _build_entry_bits(incr=True, key=f"k{i:03d}", value=None)
        # One more entry using history[0] with prefix size=4: "k001" → "k001suffix"
        all_bits += _build_entry_bits(
            incr=True, history_pos=0, history_size=4, history_suffix="suffix", value=None
        )
        data = _pack_bits(all_bits)
        items = parse_string_table(
            buf=data,
            num_updates=34,
            name="test",
            user_data_fixed_size=False,
            user_data_size_bits=0,
            flags=0,
            varint_bit_counts=False,
        )
        # history[0] after eviction = "k001"
        assert items[33].key == "k001suffix"

    def test_empty_suffix_history_prefix(self, parse_string_table):
        # history_size=5 prefix of "hello world" + empty suffix → "hello"
        e0 = _build_entry_bits(incr=True, key="hello world", value=None)
        e1 = _build_entry_bits(
            incr=True, history_pos=0, history_size=5, history_suffix="", value=None
        )
        data = _pack_bits(e0 + e1)
        items = parse_string_table(
            buf=data,
            num_updates=2,
            name="test",
            user_data_fixed_size=False,
            user_data_size_bits=0,
            flags=0,
            varint_bit_counts=False,
        )
        assert items[1].key == "hello"


# ---------------------------------------------------------------------------
# Tests: parse_string_table — compression flag (flags & 0x1)
# ---------------------------------------------------------------------------


class TestValueCompression:
    """Per-entry Snappy compression when flags & 0x1 and compressed bit = True."""

    def test_uncompressed_with_flag_set(self, parse_string_table):
        # flags=1 → compression boolean is read, but compressed=False → raw bytes
        bits = _build_entry_bits(
            incr=True, key="k", value=b"\x01\x02\x03", flags=1, compressed=False
        )
        data = _pack_bits(bits)
        items = parse_string_table(
            buf=data,
            num_updates=1,
            name="test",
            user_data_fixed_size=False,
            user_data_size_bits=0,
            flags=1,
            varint_bit_counts=False,
        )
        assert items[0].value == b"\x01\x02\x03"

    def test_compressed_value_is_decompressed(self, parse_string_table):
        # Build a Snappy-compressed payload and embed it with compressed=True.
        original = b"compressible data for the string table test"
        compressed_payload = snappy.compress(original)

        # Build the entry bits manually with compressed=True
        bits: list[int] = []
        bits.append(1)  # incr
        bits.append(1)  # has_key
        bits.append(0)  # no history
        _append_string(bits, "ckey")
        bits.append(1)  # has_value
        bits.append(1)  # compressed = True (flags & 0x1 → this bit is read)
        num_bytes = len(compressed_payload)
        for i in range(17):
            bits.append((num_bytes >> i) & 1)
        for byte in compressed_payload:
            for i in range(8):
                bits.append((byte >> i) & 1)

        data = _pack_bits(bits)
        items = parse_string_table(
            buf=data,
            num_updates=1,
            name="test",
            user_data_fixed_size=False,
            user_data_size_bits=0,
            flags=1,
            varint_bit_counts=False,
        )
        assert items[0].key == "ckey"
        assert items[0].value == original

    def test_flags_zero_no_compression_bit_read(self, parse_string_table):
        # When flags=0 the compressed boolean is never read — value is raw.
        bits = _build_entry_bits(incr=True, key="raw", value=b"\xff", flags=0)
        data = _pack_bits(bits)
        items = parse_string_table(
            buf=data,
            num_updates=1,
            name="test",
            user_data_fixed_size=False,
            user_data_size_bits=0,
            flags=0,
            varint_bit_counts=False,
        )
        assert items[0].value == b"\xff"


# ---------------------------------------------------------------------------
# Tests: parse_string_table — varint_bit_counts path
# ---------------------------------------------------------------------------


class TestVarintBitCounts:
    """Value size encoded as ubit_var (varint_bit_counts=True) path."""

    def test_varint_bit_counts_small_value(self, parse_string_table):
        # ubit_var with top-2 bits = 0b00: value is the low 4 bits directly.
        # We're encoding num_bytes=3, which fits in 4 bits with top-2=00.
        bits = _build_entry_bits(
            incr=True,
            key="vk",
            value=b"\xaa\xbb\xcc",
            varint_bit_counts=True,
        )
        data = _pack_bits(bits)
        items = parse_string_table(
            buf=data,
            num_updates=1,
            name="test",
            user_data_fixed_size=False,
            user_data_size_bits=0,
            flags=0,
            varint_bit_counts=True,
        )
        assert items[0].value == b"\xaa\xbb\xcc"

    def test_varint_bit_counts_versus_fixed_17bit_same_value(self, parse_string_table):
        # Same raw bytes, parsed once with varint_bit_counts=True and once False —
        # two different blobs that must yield identical output.
        payload = b"\x01\x02"

        bits_varint = _build_entry_bits(incr=True, key="v", value=payload, varint_bit_counts=True)
        bits_fixed = _build_entry_bits(incr=True, key="v", value=payload, varint_bit_counts=False)

        items_varint = parse_string_table(
            buf=_pack_bits(bits_varint),
            num_updates=1,
            name="t",
            user_data_fixed_size=False,
            user_data_size_bits=0,
            flags=0,
            varint_bit_counts=True,
        )
        items_fixed = parse_string_table(
            buf=_pack_bits(bits_fixed),
            num_updates=1,
            name="t",
            user_data_fixed_size=False,
            user_data_size_bits=0,
            flags=0,
            varint_bit_counts=False,
        )
        assert items_varint[0].value == items_fixed[0].value == payload


# ---------------------------------------------------------------------------
# Tests: parse_string_table — fixed-size user data
# ---------------------------------------------------------------------------


class TestFixedSizeUserData:
    """user_data_fixed_size=True path: value is exactly user_data_size_bits bits."""

    def test_fixed_size_8bit(self, parse_string_table):
        # 8-bit fixed value: the parser reads user_data_size_bits=8 bits directly.
        bits: list[int] = []
        bits.append(1)  # incr
        bits.append(1)  # has_key
        bits.append(0)  # no history
        _append_string(bits, "fixedkey")
        bits.append(1)  # has_value
        # For fixed size, no size prefix — just the raw bits (8 bits for 0xAB)
        val = 0xAB
        for i in range(8):
            bits.append((val >> i) & 1)

        data = _pack_bits(bits)
        items = parse_string_table(
            buf=data,
            num_updates=1,
            name="test",
            user_data_fixed_size=True,
            user_data_size_bits=8,
            flags=0,
            varint_bit_counts=False,
        )
        assert items[0].key == "fixedkey"
        assert items[0].value == bytes([0xAB])

    def test_fixed_size_16bit(self, parse_string_table):
        bits: list[int] = []
        bits.append(1)  # incr
        bits.append(0)  # no key
        bits.append(1)  # has_value
        val = 0x1234
        for i in range(16):
            bits.append((val >> i) & 1)

        data = _pack_bits(bits)
        items = parse_string_table(
            buf=data,
            num_updates=1,
            name="test",
            user_data_fixed_size=True,
            user_data_size_bits=16,
            flags=0,
            varint_bit_counts=False,
        )
        assert items[0].value == bytes([0x34, 0x12])  # little-endian bit packing


# ---------------------------------------------------------------------------
# Tests: handle_create
# ---------------------------------------------------------------------------


class TestHandleCreate:
    """handle_create: table registration and _next_index bookkeeping."""

    def _make_create_msg(
        self,
        name: str,
        string_data: bytes = b"",
        num_entries: int = 0,
        user_data_fixed_size: bool = False,
        user_data_size_bits: int = 0,
        flags: int = 0,
        using_varint_bitcounts: bool = False,
        data_compressed: bool = False,
    ):
        """Return a plain-object mock of CSVCMsg_CreateStringTable."""

        class _Msg:
            pass

        m = _Msg()
        m.name = name
        m.string_data = string_data
        m.num_entries = num_entries
        m.user_data_fixed_size = user_data_fixed_size
        m.user_data_size_bits = user_data_size_bits
        m.flags = flags
        m.using_varint_bitcounts = using_varint_bitcounts
        m.data_compressed = data_compressed
        return m

    def test_registers_table_in_container(self, string_tables_cls):
        from gem.string_table import handle_create

        st = string_tables_cls()
        msg = self._make_create_msg("instancebaseline")
        tbl = handle_create(msg, st)
        assert st.get_by_name("instancebaseline") is tbl

    def test_table_index_starts_at_zero(self, string_tables_cls):
        from gem.string_table import handle_create

        st = string_tables_cls()
        msg = self._make_create_msg("first")
        tbl = handle_create(msg, st)
        assert tbl.index == 0

    def test_next_index_increments_per_create(self, string_tables_cls):
        from gem.string_table import handle_create

        st = string_tables_cls()
        t0 = handle_create(self._make_create_msg("alpha"), st)
        t1 = handle_create(self._make_create_msg("beta"), st)
        t2 = handle_create(self._make_create_msg("gamma"), st)
        assert t0.index == 0
        assert t1.index == 1
        assert t2.index == 2
        assert st._next_index == 3

    def test_creates_table_with_correct_metadata(self, string_tables_cls):
        from gem.string_table import handle_create

        st = string_tables_cls()
        msg = self._make_create_msg(
            "myTable",
            user_data_fixed_size=True,
            user_data_size_bits=16,
            flags=3,
            using_varint_bitcounts=True,
        )
        tbl = handle_create(msg, st)
        assert tbl.name == "myTable"
        assert tbl.user_data_fixed_size is True
        assert tbl.user_data_size_bits == 16
        assert tbl.flags == 3
        assert tbl.varint_bit_counts is True

    def test_parses_initial_items_into_table(self, string_tables_cls):
        from gem.string_table import handle_create

        bits = _build_entry_bits(incr=True, key="slot_0", value=b"\x01")
        bits += _build_entry_bits(incr=True, key="slot_1", value=b"\x02")
        blob = _pack_bits(bits)

        st = string_tables_cls()
        msg = self._make_create_msg("populated", string_data=blob, num_entries=2)
        tbl = handle_create(msg, st)

        assert 0 in tbl.items
        assert 1 in tbl.items
        assert tbl.items[0] == ("slot_0", b"\x01")
        assert tbl.items[1] == ("slot_1", b"\x02")

    def test_data_compressed_blob_is_decompressed(self, string_tables_cls):
        from gem.string_table import handle_create

        bits = _build_entry_bits(incr=True, key="compressed_key", value=b"\xde\xad")
        raw_blob = _pack_bits(bits)
        compressed_blob = snappy.compress(raw_blob)

        st = string_tables_cls()
        msg = self._make_create_msg(
            "snappy_table",
            string_data=compressed_blob,
            num_entries=1,
            data_compressed=True,
        )
        tbl = handle_create(msg, st)
        assert tbl.items[0] == ("compressed_key", b"\xde\xad")

    def test_data_compressed_lzss_raises(self, string_tables_cls):
        from gem.string_table import handle_create

        st = string_tables_cls()
        msg = self._make_create_msg(
            "lzss_table",
            string_data=b"LZSS" + b"\x00" * 16,
            data_compressed=True,
        )
        with pytest.raises(NotImplementedError):
            handle_create(msg, st)

    def test_empty_data_creates_table_with_no_items(self, string_tables_cls):
        from gem.string_table import handle_create

        st = string_tables_cls()
        msg = self._make_create_msg("empty_table", string_data=b"", num_entries=0)
        tbl = handle_create(msg, st)
        assert tbl.items == {}

    def test_get_by_id_returns_same_table(self, string_tables_cls):
        from gem.string_table import handle_create

        st = string_tables_cls()
        handle_create(self._make_create_msg("t0"), st)
        handle_create(self._make_create_msg("t1"), st)
        assert st.get_by_id(0) is not None
        assert st.get_by_id(0).name == "t0"
        assert st.get_by_id(1).name == "t1"


# ---------------------------------------------------------------------------
# Tests: handle_update
# ---------------------------------------------------------------------------


class TestHandleUpdate:
    """handle_update: merging updates into existing tables."""

    def _make_update_msg(
        self,
        table_id: int,
        string_data: bytes,
        num_changed_entries: int,
    ):
        class _Msg:
            pass

        m = _Msg()
        m.table_id = table_id
        m.string_data = string_data
        m.num_changed_entries = num_changed_entries
        return m

    def _create_table_with_items(self, string_tables_cls, string_table_cls, name: str, items: dict):
        from gem.string_table import StringTable

        st = string_tables_cls()
        tbl = StringTable(index=0, name=name)
        tbl.items = dict(items)
        st.tables[0] = tbl
        st.name_index[name] = 0
        st._next_index = 1
        return st, tbl

    def test_update_replaces_value_of_existing_entry(self, string_tables_cls, string_table_cls):
        from gem.string_table import handle_update

        st, tbl = self._create_table_with_items(
            string_tables_cls, string_table_cls, "test", {0: ("hero", b"\x01")}
        )
        bits = _build_entry_bits(incr=True, key="hero", value=b"\x99")
        msg = self._make_update_msg(0, _pack_bits(bits), 1)
        handle_update(msg, st)
        assert tbl.items[0] == ("hero", b"\x99")

    def test_update_blank_key_preserves_existing_key(self, string_tables_cls, string_table_cls):
        from gem.string_table import handle_update

        # Existing entry has key "oldkey"; update sends no key (key="")
        st, tbl = self._create_table_with_items(
            string_tables_cls, string_table_cls, "test", {0: ("oldkey", b"\x01")}
        )
        bits = _build_entry_bits(incr=True, key=None, value=b"\x02")
        msg = self._make_update_msg(0, _pack_bits(bits), 1)
        handle_update(msg, st)
        # Key must remain "oldkey" — blank update key does not overwrite
        key, val = tbl.items[0]
        assert key == "oldkey"
        assert val == b"\x02"

    def test_update_blank_value_preserves_existing_value(self, string_tables_cls, string_table_cls):
        from gem.string_table import handle_update

        st, tbl = self._create_table_with_items(
            string_tables_cls, string_table_cls, "test", {0: ("mykey", b"\xde\xad")}
        )
        bits = _build_entry_bits(incr=True, key="mykey", value=None)
        msg = self._make_update_msg(0, _pack_bits(bits), 1)
        handle_update(msg, st)
        key, val = tbl.items[0]
        assert key == "mykey"
        assert val == b"\xde\xad"

    def test_update_inserts_new_entry(self, string_tables_cls, string_table_cls):
        from gem.string_table import handle_update

        st, tbl = self._create_table_with_items(string_tables_cls, string_table_cls, "test", {})
        bits = _build_entry_bits(incr=True, key="newkey", value=b"\xaa")
        msg = self._make_update_msg(0, _pack_bits(bits), 1)
        handle_update(msg, st)
        assert 0 in tbl.items
        assert tbl.items[0] == ("newkey", b"\xaa")

    def test_update_multiple_entries(self, string_tables_cls, string_table_cls):
        from gem.string_table import handle_update

        st, tbl = self._create_table_with_items(
            string_tables_cls,
            string_table_cls,
            "test",
            {0: ("a", b"\x01"), 1: ("b", b"\x02")},
        )
        bits = _build_entry_bits(incr=True, key="a", value=b"\x10")
        bits += _build_entry_bits(incr=True, key="b", value=b"\x20")
        msg = self._make_update_msg(0, _pack_bits(bits), 2)
        handle_update(msg, st)
        assert tbl.items[0] == ("a", b"\x10")
        assert tbl.items[1] == ("b", b"\x20")

    def test_update_missing_table_raises_key_error(self, string_tables_cls):
        from gem.string_table import handle_update

        st = string_tables_cls()
        bits = _build_entry_bits(incr=True, key="k", value=b"\x01")
        msg = self._make_update_msg(99, _pack_bits(bits), 1)
        with pytest.raises(KeyError):
            handle_update(msg, st)

    def test_update_absolute_index_into_existing_table(self, string_tables_cls, string_table_cls):
        from gem.string_table import handle_update

        # Pre-populate entries 0..4; update jumps to absolute index 3.
        items = {i: (f"k{i}", bytes([i])) for i in range(5)}
        st, tbl = self._create_table_with_items(string_tables_cls, string_table_cls, "test", items)
        bits = _build_entry_bits(incr=False, abs_index=3, key="k3", value=b"\xff")
        msg = self._make_update_msg(0, _pack_bits(bits), 1)
        handle_update(msg, st)
        assert tbl.items[3] == ("k3", b"\xff")
