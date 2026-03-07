"""
Tests for gem.reader.BitReader

Reference: manta/reader.go
"""

import struct

import pytest

# ---------------------------------------------------------------------------
# Helpers to build raw byte sequences for testing
# ---------------------------------------------------------------------------


def _pack_varuint32(value: int) -> bytes:
    """Encode a value as a protobuf-style varuint32."""
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


def _pack_varint32_zigzag(value: int) -> bytes:
    """Zigzag-encode a signed int32 then varuint-encode it."""
    ux = (value << 1) ^ (value >> 31)
    return _pack_varuint32(ux & 0xFFFFFFFF)


# ---------------------------------------------------------------------------
# Import under test — will fail until Phase 1 is implemented
# ---------------------------------------------------------------------------


@pytest.fixture
def reader_cls():
    from gem.reader import BitReader

    return BitReader


# ---------------------------------------------------------------------------
# read_bits
# ---------------------------------------------------------------------------


class TestReadBits:
    def test_read_single_bit_zero(self, reader_cls):
        r = reader_cls(b"\x00")
        assert r.read_bits(1) == 0

    def test_read_single_bit_one(self, reader_cls):
        r = reader_cls(b"\x01")
        assert r.read_bits(1) == 1

    def test_read_8_bits(self, reader_cls):
        r = reader_cls(b"\xab")
        assert r.read_bits(8) == 0xAB

    def test_read_across_bytes(self, reader_cls):
        # Low 4 bits of 0xF0 = 0, high 4 bits of 0x0F = 0
        # Byte 0: 0b11110000, Byte 1: 0b00001111
        # First 4 bits (LSB-first): 0b0000 = 0
        # Next 4 bits: 0b1111 = 15
        r = reader_cls(b"\xf0\x0f")
        assert r.read_bits(4) == 0x0  # low nibble of 0xF0
        assert r.read_bits(4) == 0xF  # high nibble of 0xF0

    def test_read_multiple_sequential(self, reader_cls):
        r = reader_cls(b"\xff")
        for _ in range(8):
            assert r.read_bits(1) == 1

    def test_read_16_bits(self, reader_cls):
        data = struct.pack("<H", 0x1234)
        r = reader_cls(data)
        assert r.read_bits(16) == 0x1234


# ---------------------------------------------------------------------------
# read_boolean
# ---------------------------------------------------------------------------


class TestReadBoolean:
    def test_false(self, reader_cls):
        r = reader_cls(b"\x00")
        assert r.read_boolean() is False

    def test_true(self, reader_cls):
        r = reader_cls(b"\x01")
        assert r.read_boolean() is True


# ---------------------------------------------------------------------------
# read_varuint32
# ---------------------------------------------------------------------------


class TestReadVarUint32:
    @pytest.mark.parametrize("value", [0, 1, 127, 128, 255, 300, 16383, 16384, 2097151, 0xFFFFFFFF])
    def test_roundtrip(self, reader_cls, value):
        data = _pack_varuint32(value)
        r = reader_cls(data)
        assert r.read_varuint32() == value

    def test_single_byte_zero(self, reader_cls):
        r = reader_cls(b"\x00")
        assert r.read_varuint32() == 0

    def test_single_byte_max(self, reader_cls):
        r = reader_cls(b"\x7f")
        assert r.read_varuint32() == 127

    def test_two_bytes(self, reader_cls):
        # 128 = 0x80 0x01
        r = reader_cls(b"\x80\x01")
        assert r.read_varuint32() == 128

    def test_five_bytes_max(self, reader_cls):
        r = reader_cls(_pack_varuint32(0xFFFFFFFF))
        assert r.read_varuint32() == 0xFFFFFFFF


# ---------------------------------------------------------------------------
# read_varint32 (zigzag)
# ---------------------------------------------------------------------------


class TestReadVarInt32:
    @pytest.mark.parametrize("value", [0, -1, 1, -2, 2, 127, -128, 2147483647, -2147483648])
    def test_roundtrip(self, reader_cls, value):
        data = _pack_varint32_zigzag(value)
        r = reader_cls(data)
        assert r.read_varint32() == value


# ---------------------------------------------------------------------------
# read_varuint64
# ---------------------------------------------------------------------------


class TestReadVarUint64:
    @pytest.mark.parametrize("value", [0, 1, 0xFFFFFFFF, 0xFFFFFFFFFFFFFFFF])
    def test_roundtrip(self, reader_cls, value):
        out = []
        v = value
        while True:
            bits = v & 0x7F
            v >>= 7
            if v:
                out.append(bits | 0x80)
            else:
                out.append(bits)
                break
        data = bytes(out)
        r = reader_cls(data)
        assert r.read_varuint64() == value


# ---------------------------------------------------------------------------
# read_ubit_var (6-bit groups, 2-bit size hint)
# ---------------------------------------------------------------------------


class TestReadUBitVar:
    def test_small_value_no_extension(self, reader_cls):
        # Value < 16 → top 2 bits of 6-bit group = 0b00 → return low 6 bits
        # Byte = 0b00001010 = 10, top 2 bits = 00
        r = reader_cls(b"\x0a")
        assert r.read_ubit_var() == 10

    def test_zero(self, reader_cls):
        r = reader_cls(b"\x00")
        assert r.read_ubit_var() == 0


# ---------------------------------------------------------------------------
# read_le_uint32 / read_le_uint64
# ---------------------------------------------------------------------------


class TestReadLE:
    def test_le_uint32(self, reader_cls):
        data = struct.pack("<I", 0xDEADBEEF)
        r = reader_cls(data)
        assert r.read_le_uint32() == 0xDEADBEEF

    def test_le_uint64(self, reader_cls):
        data = struct.pack("<Q", 0xCAFEBABEDEADBEEF)
        r = reader_cls(data)
        assert r.read_le_uint64() == 0xCAFEBABEDEADBEEF


# ---------------------------------------------------------------------------
# read_string / read_string_n
# ---------------------------------------------------------------------------


class TestReadString:
    def test_null_terminated(self, reader_cls):
        r = reader_cls(b"hello\x00")
        assert r.read_string() == "hello"

    def test_empty_string(self, reader_cls):
        r = reader_cls(b"\x00")
        assert r.read_string() == ""

    def test_read_string_n(self, reader_cls):
        r = reader_cls(b"PBDEMS2\x00")
        assert r.read_string_n(8) == "PBDEMS2\x00"


# ---------------------------------------------------------------------------
# read_coord
# ---------------------------------------------------------------------------


class TestReadCoord:
    def test_zero(self, reader_cls):
        # intval=0, fractval=0 → value=0.0
        # bits: 0 (intval flag), 0 (fractval flag) → 2 bits = 0b00
        r = reader_cls(b"\x00")
        assert r.read_coord() == pytest.approx(0.0)

    def test_positive_integer(self, reader_cls):
        # intval=1, fractval=0, sign=+
        # bit0=1 (has int), bit1=0 (no frac), bit2=0 (positive)
        # then 14 bits for int value (value - 1 stored, so 0 stored = 1)
        # Construct: bits = 1 (intval) | 0 (fractval) → read sign=0, read 14 bit int=0 → value=1.0
        # bit pattern LSB-first: 1, 0, 0, then 14 bits of 0
        # = 0b00000001 = 0x01 for first byte, rest zero
        # bit 0 = intval=1, bit 1 = fractval=0, bit 2 = sign=0, bits 3-16 = 0 (int = 0+1 = 1)
        bits = 0
        bits |= 1 << 0  # intval flag
        bits |= 0 << 1  # fractval flag
        bits |= 0 << 2  # sign = positive
        # 14-bit int value = 0 (meaning 1.0)
        data = bits.to_bytes(3, "little")
        r = reader_cls(data)
        assert r.read_coord() == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# rem_bits / boundary checks
# ---------------------------------------------------------------------------


class TestBoundary:
    def test_rem_bits_after_reads(self, reader_cls):
        r = reader_cls(b"\xff\xff")
        r.read_bits(8)
        assert r.rem_bits() == 8

    def test_empty_buffer_raises(self, reader_cls):
        r = reader_cls(b"")
        with pytest.raises(BufferError):
            r.read_bits(1)
