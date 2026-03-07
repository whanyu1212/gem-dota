"""
Tests for gem.string_table — string table creation, updates, and key-history compression.

Reference: manta/string_table.go
"""

import pytest


@pytest.fixture
def string_tables_cls():
    from gem.string_table import StringTables

    return StringTables


@pytest.fixture
def string_table_cls():
    from gem.string_table import StringTable

    return StringTable


@pytest.fixture
def parse_string_table():
    from gem.string_table import parse_string_table

    return parse_string_table


class TestStringTables:
    def test_empty_on_init(self, string_tables_cls):
        st = string_tables_cls()
        assert len(st.tables) == 0

    def test_get_by_name_missing(self, string_tables_cls):
        st = string_tables_cls()
        result = st.get_by_name("nonexistent")
        assert result is None

    def test_add_and_retrieve_by_name(self, string_tables_cls, string_table_cls):
        st = string_tables_cls()
        tbl = string_table_cls(index=0, name="instancebaseline")
        st.add(tbl)
        assert st.get_by_name("instancebaseline") is tbl

    def test_add_increments_index(self, string_tables_cls, string_table_cls):
        st = string_tables_cls()
        t1 = string_table_cls(index=0, name="a")
        t2 = string_table_cls(index=1, name="b")
        st.add(t1)
        st.add(t2)
        assert st.get_by_name("a").index == 0
        assert st.get_by_name("b").index == 1


class TestStringTable:
    def test_get_item_by_index(self, string_table_cls):
        t = string_table_cls(index=0, name="test")
        t.items[0] = ("mykey", b"myvalue")
        key, value = t.items[0]
        assert key == "mykey"
        assert value == b"myvalue"


class TestParseStringTable:
    """
    Test the binary string table parser (key-history encoding).

    Reference: manta/string_table.go parseStringTable()
    Format per entry:
      bit: incr (1=increment index, 0=read absolute index as varuint+1)
      bit: has_key
        if has_key:
          bit: use_history
            if use_history: 5-bit pos, 5-bit size, null-terminated suffix
            else: null-terminated string
      bit: has_value
        if has_value:
          if fixed: userDataSizeBits bits
          else: 17-bit size*8 bits, then that many bits
    """

    def _build_entry(
        self, incr: bool, key: str | None, value: bytes | None, prev_index: int = -1
    ) -> bytes:
        """Build a single simple string table entry (no history, fixed=False, flags=0)."""

        bits = []

        # incr flag
        bits.append(1 if incr else 0)
        if not incr:
            # absolute index = prev_index + 1, encoded as varuint - 1
            # For simplicity, just use incr=True in most tests
            raise NotImplementedError("absolute index encoding not implemented in helper")

        # has_key
        if key is not None:
            bits.append(1)
            bits.append(0)  # use_history = False
            for ch in key.encode("utf-8"):
                for i in range(8):
                    bits.append((ch >> i) & 1)
            bits.append(0)  # null terminator
        else:
            bits.append(0)

        # has_value
        if value is not None:
            bits.append(1)
            # 17-bit size in bytes → size * 8 in bits
            size_bits = len(value)  # number of bytes
            for i in range(17):
                bits.append((size_bits >> i) & 1)
            for byte in value:
                for i in range(8):
                    bits.append((byte >> i) & 1)
        else:
            bits.append(0)

        # convert bits to bytes
        padded = bits + [0] * (-len(bits) % 8)
        result = []
        for i in range(0, len(padded), 8):
            byte = 0
            for j in range(8):
                if padded[i + j]:
                    byte |= 1 << j
            result.append(byte)
        return bytes(result)

    def test_single_entry_with_key_and_value(self, parse_string_table):
        data = self._build_entry(incr=True, key="hero_0", value=b"\xde\xad")
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
        idx, key, value = items[0]
        assert idx == 0
        assert key == "hero_0"
        assert value == b"\xde\xad"

    def test_single_entry_no_key_no_value(self, parse_string_table):
        data = self._build_entry(incr=True, key=None, value=None)
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
        idx, key, value = items[0]
        assert idx == 0
        assert key == ""
        assert value == b""

    def test_empty_buffer_returns_empty(self, parse_string_table):
        items = parse_string_table(
            buf=b"",
            num_updates=0,
            name="test",
            user_data_fixed_size=False,
            user_data_size_bits=0,
            flags=0,
            varint_bit_counts=False,
        )
        assert items == []

    def test_multiple_entries_incrementing(self, parse_string_table):
        entry0 = self._build_entry(incr=True, key="a", value=b"\x01")
        entry1 = self._build_entry(incr=True, key="b", value=b"\x02")
        data = entry0 + entry1
        items = parse_string_table(
            buf=data,
            num_updates=2,
            name="test",
            user_data_fixed_size=False,
            user_data_size_bits=0,
            flags=0,
            varint_bit_counts=False,
        )
        assert len(items) == 2
        assert items[0][0] == 0
        assert items[1][0] == 1
        assert items[0][1] == "a"
        assert items[1][1] == "b"
