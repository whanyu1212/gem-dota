"""
Tests for gem.binary.reader.BitReader

Reference: manta/reader.go
"""

from __future__ import annotations

import struct

import pytest

from gem.binary.reader import BitReader, BufferReadError

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
    from gem.binary.reader import BitReader

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
# read_float
# ---------------------------------------------------------------------------


class TestReadFloat:
    def test_float32_little_endian(self):
        r = BitReader(struct.pack("<f", 12.5))
        assert r.read_float() == pytest.approx(12.5)


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
        with pytest.raises(BufferReadError):
            r.read_bits(1)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _r(bits_str: str) -> BitReader:
    """Build a BitReader from an LSB-first bit string ('0'/'1' chars)."""
    bits = [int(c) for c in bits_str if c in "01"]
    while len(bits) % 8:
        bits.append(0)
    data = bytearray()
    for i in range(0, len(bits), 8):
        byte = sum(bits[i + j] << j for j in range(8))
        data.append(byte)
    return BitReader(bytes(data))


def _bytes_r(*byte_vals: int) -> BitReader:
    return BitReader(bytes(byte_vals))


def _drain_bits_for_comparison(r: BitReader) -> list[tuple[int, int]]:
    """Drain a reader in varied chunk sizes for logical-state comparison."""
    chunks: list[tuple[int, int]] = []
    chunk_sizes = (1, 2, 3, 5, 8, 13, 21, 32, 7)
    i = 0
    while r.rem_bits() > 0:
        n = min(chunk_sizes[i % len(chunk_sizes)], r.rem_bits())
        chunks.append((n, r.read_bits(n)))
        i += 1
    return chunks


def _assert_read_bytes_matches_slow(data: bytes, skip_bits: int, n: int) -> None:
    """Compare optimized read_bytes against the preserved slow implementation."""
    fast = BitReader(data)
    slow = BitReader(data)

    if skip_bits:
        assert fast.read_bits(skip_bits) == slow.read_bits(skip_bits)

    assert fast.read_bytes(n) == slow._read_bytes_slow(n)
    assert fast.position() == slow.position()
    assert fast.rem_bits() == slow.rem_bits()
    assert _drain_bits_for_comparison(fast) == _drain_bits_for_comparison(slow)


# ---------------------------------------------------------------------------
# BufferReadError
# ---------------------------------------------------------------------------


class TestBufferReadError:
    def test_subclasses_eof_error(self):
        assert issubclass(BufferReadError, EOFError)

    def test_old_buffer_error_name_is_not_exported(self):
        import gem.binary as binary
        import gem.binary.reader as reader

        assert not hasattr(reader, "BufferError")
        assert not hasattr(binary, "BufferError")

    def test_read_bits_exhausted(self):
        r = BitReader(b"\xff")
        r.read_bits(8)  # consume all
        with pytest.raises(BufferReadError):
            r.read_bits(1)

    def test_read_boolean_empty_buffer_exhausted(self):
        r = BitReader(b"")
        with pytest.raises(BufferReadError):
            r.read_boolean()

    def test_read_bytes_too_many(self):
        r = BitReader(b"\x01\x02")
        with pytest.raises(BufferReadError):
            r.read_bytes(3)

    def test_read_bytes_unaligned_exhausted(self):
        r = BitReader(b"\xff")
        r.read_bits(1)  # partial byte → unaligned
        with pytest.raises(BufferReadError):
            r.read_bytes(2)


# ---------------------------------------------------------------------------
# read_bytes — unaligned path
# ---------------------------------------------------------------------------


class TestReadBytesUnaligned:
    def test_unaligned_read_bytes(self):
        r = BitReader(bytes([0b10110100, 0b00001010]))
        r.read_bits(4)  # consume low nibble, now unaligned
        result = r.read_bytes(1)
        # Low nibble of second byte's contribution follows the high nibble of first
        assert result == b"\xab"

    def test_read_bytes_matches_slow_fallback_across_offsets_sizes_and_data(self):
        patterns = [
            b"\x00" * 96,
            b"\xff" * 96,
            bytes(range(96)),
            bytes(reversed(range(96))),
            bytes((i * 37 + 11) & 0xFF for i in range(96)),
            b"\xaa\x55" * 48,
        ]
        candidate_lengths = (0, 1, 2, 3, 4, 5, 7, 8, 15, 16, 17, 31, 32, 33, 63, 64, 65, 83)

        for data in patterns:
            for skip_bits in range(8):
                max_n = (len(data) * 8 - skip_bits) // 8
                for n in candidate_lengths:
                    if n <= max_n:
                        _assert_read_bytes_matches_slow(data, skip_bits, n)

    def test_unaligned_bulk_path_returns_expected_bytes(self):
        data = bytes(range(1, 80))
        skip_bits = 6
        n = 24
        r = BitReader(data)
        r.read_bits(skip_bits)

        expected_int = (int.from_bytes(data, "little") >> skip_bits) & ((1 << (n * 8)) - 1)
        assert r.read_bytes(n) == expected_int.to_bytes(n, "little")

    def test_aligned_fast_path(self):
        r = BitReader(b"\xab\xcd")
        result = r.read_bytes(2)
        assert result == b"\xab\xcd"

    def test_cached_byte_aligned_fast_path_after_peek(self):
        r = BitReader(b"\x01\x02\x03\x04\x05")
        assert r.peek_bits(16) == 0x0201
        assert r.position() == "0"

        assert r.read_bytes(5) == b"\x01\x02\x03\x04\x05"
        assert r.position() == "5"
        assert r.rem_bits() == 0


# ---------------------------------------------------------------------------
# read_bits_as_bytes — remainder bits
# ---------------------------------------------------------------------------


class TestReadBitsAsBytes:
    def test_exact_multiple_of_8(self):
        r = BitReader(b"\xab\xcd")
        result = r.read_bits_as_bytes(16)
        assert result == b"\xab\xcd"

    def test_full_byte_from_unaligned_position(self):
        r = BitReader(b"\xf0\x0f")
        assert r.read_bits(4) == 0
        assert r.read_bits_as_bytes(8) == b"\xff"

    def test_remainder_bits(self):
        # read_bits_as_bytes(10) = 1 full byte + 2 remainder bits
        r = BitReader(bytes([0b11111111, 0b00000011]))
        result = r.read_bits_as_bytes(10)
        assert len(result) == 2
        assert result[0] == 0xFF
        assert result[1] == 0x03  # low 2 bits of next byte

    def test_less_than_8_bits(self):
        r = BitReader(bytes([0b00001111]))
        result = r.read_bits_as_bytes(4)
        assert len(result) == 1
        assert result[0] == 0x0F


# ---------------------------------------------------------------------------
# read_varuint64 — overflow paths
# ---------------------------------------------------------------------------


class TestReadVarint64:
    def test_basic_value(self):
        r = BitReader(b"\x01")
        assert r.read_varuint64() == 1

    def test_multibyte(self):
        r = BitReader(bytes([0x80 | 1, 0x01]))
        assert r.read_varuint64() == 0x81

    def test_overflow_9th_byte(self):
        # 10 bytes all with continuation bit set → last byte > 1 → overflow
        data = bytes([0x80] * 9 + [0x02])
        r = BitReader(data)
        with pytest.raises(OverflowError):
            r.read_varuint64()

    def test_overflow_after_ten_continuation_bytes(self):
        data = bytes([0x80] * 10)
        r = BitReader(data)
        with pytest.raises(OverflowError):
            r.read_varuint64()

    def test_max_valid_9th_byte(self):
        # 9 bytes with continuation bit + last byte = 1 → valid (max uint64-ish)
        data = bytes([0x80] * 9 + [0x01])
        r = BitReader(data)
        val = r.read_varuint64()
        assert val > 0

    def test_read_varint64_positive(self):
        # zigzag: positive n → n*2 encoded
        # Encode value 5 → zigzag = 10 → varuint64 = 10 = 0x0A
        r = BitReader(b"\x0a")
        assert r.read_varint64() == 5

    def test_read_varint64_negative(self):
        # zigzag: -1 → 1 = 0x01
        r = BitReader(b"\x01")
        assert r.read_varint64() == -1


# ---------------------------------------------------------------------------
# read_ubit_var — all branches
# ---------------------------------------------------------------------------


class TestReadUbitVar:
    def test_selector_00(self):
        # Low 6 bits: selector (bits 4-5) = 0b00 → return low 4 bits
        # value = 0b001010 → selector=00, val=0b1010=10
        r = _r("0101000000")  # bits 0-5 LSB: 0,1,0,1,0,0 = 0b001010 = 10
        assert r.read_ubit_var() == 10

    def test_selector_01(self):
        # 6 bits: selector=01, low4=val; then 4 more bits
        # Build: low4=0b0001, selector=0b01 → 6 bits = 0b010001 = 17
        # then 4 more bits = 0b0010 = 2
        # result = (17 & 0x0F) | (2 << 4) = 1 | 32 = 33
        bits = "100010" + "0100"  # 6 bits + 4 bits LSB-first
        r = _r(bits)
        val = r.read_ubit_var()
        assert val == (0b0001 | (0b0010 << 4))

    def test_selector_10(self):
        # selector=0b10 in bits 4-5, low4=1, then 8 more bits=3
        # 6 bits: low4=0001, sel=10 → 0b100001
        # 8 more bits = 3
        bits = "100001" + "11000000"  # sel=10, low4=1, ext=3
        r = _r(bits)
        val = r.read_ubit_var()
        assert val == (1 | (3 << 4))

    def test_selector_11(self):
        # 6-bit value = 49 (sel=0x30, low4=1): bit0=1,bit1=0,bit2=0,bit3=0,bit4=1,bit5=1
        # 28-bit value = 5: bit0=1,bit1=0,bit2=1,rest=0
        # LSB-first string: "100011" + "101" + "0"*25
        bits = "100011" + "101" + "0" * 25
        r = _r(bits)
        val = r.read_ubit_var()
        assert val == (1 | (5 << 4))


# ---------------------------------------------------------------------------
# read_ubit_var_fp — all 5 branches
# ---------------------------------------------------------------------------


class TestReadUbitVarFp:
    def test_branch_1_bit(self):
        # First boolean=True → read 2 bits
        # bit0=1 (True), then 2 bits = 0b01 = 1
        r = _r("1" + "10")
        assert r.read_ubit_var_fp() == 1

    def test_branch_4_bits(self):
        # First=False, second=True → read 4 bits
        r = _r("0" + "1" + "0101")  # = 0b1010 = 10
        assert r.read_ubit_var_fp() == 10

    def test_branch_10_bits(self):
        # First=False, second=False, third=True → read 10 bits
        r = _r("0" + "0" + "1" + "1000000000")  # = 1
        assert r.read_ubit_var_fp() == 1

    def test_branch_17_bits(self):
        # 3 False, 4th=True → read 17 bits
        r = _r("0" + "0" + "0" + "1" + "10000000000000000")  # = 1
        assert r.read_ubit_var_fp() == 1

    def test_branch_31_bits(self):
        # 4 False → read 31 bits
        r = _r("0" + "0" + "0" + "0" + "1" + "0" * 30)  # = 1
        assert r.read_ubit_var_fp() == 1


# ---------------------------------------------------------------------------
# read_coord — all flag combinations (extended)
# ---------------------------------------------------------------------------


class TestReadCoordExtended:
    def test_both_zero_flags(self):
        # has_int=0, has_frac=0 → return 0.0 immediately
        r = _r("00")
        assert r.read_coord() == 0.0

    def test_int_only_positive(self):
        # has_int=1, has_frac=0, negative=0, int_val=14 bits, frac_val=0
        # int_val encoded as (n-1), so n=1 → bits=0
        bits = "1" + "0" + "0" + "0" * 14  # has_int=1, has_frac=0, neg=0, int_val=0 (→1)
        r = _r(bits)
        result = r.read_coord()
        assert result == pytest.approx(1.0)

    def test_frac_only_positive(self):
        # has_int=0, has_frac=1, negative=0, frac_val=1 → 1/32
        bits = "0" + "1" + "0" + "10000"  # has_int=0, has_frac=1, neg=0, frac=1
        r = _r(bits)
        result = r.read_coord()
        assert result == pytest.approx(1.0 / 32.0)

    def test_negative_coord(self):
        # has_int=1, has_frac=0, negative=1, int_val=0 (→1)
        bits = "1" + "0" + "1" + "0" * 14
        r = _r(bits)
        result = r.read_coord()
        assert result == pytest.approx(-1.0)

    def test_int_and_frac(self):
        # has_int=1, has_frac=1, negative=0, int_val=1 (encoded as 0), frac=16 → 0.5
        bits = "1" + "1" + "0" + "0" * 14 + "00001"  # frac=16→LSB first: 00001 = 16
        r = _r(bits)
        result = r.read_coord()
        assert result == pytest.approx(1.0 + 16.0 / 32.0)


# ---------------------------------------------------------------------------
# read_angle
# ---------------------------------------------------------------------------


class TestReadAngle:
    def test_zero_angle(self):
        r = BitReader(b"\x00\x00")
        assert r.read_angle(8) == 0.0

    def test_full_range_8bit(self):
        # All 8 bits set = 255 → 255 * 360/256 = 358.59375
        r = BitReader(b"\xff")
        assert r.read_angle(8) == pytest.approx(255 * 360.0 / 256)

    def test_half_range(self):
        # 128 of 256 → 180.0
        r = BitReader(b"\x80")
        assert r.read_angle(8) == pytest.approx(180.0)

    def test_4bit_angle(self):
        # 4 bits, value=8 → 8 * 360/16 = 180.0
        r = _r("0001")  # LSB-first: 0001 = 8
        assert r.read_angle(4) == pytest.approx(180.0)


# ---------------------------------------------------------------------------
# read_normal
# ---------------------------------------------------------------------------


class TestReadNormal:
    def test_zero_magnitude(self):
        # negative=0, magnitude=0 → 0.0
        bits = "0" + "0" * 11
        r = _r(bits)
        assert r.read_normal() == pytest.approx(0.0)

    def test_max_positive(self):
        # negative=0, magnitude=2047 (all 11 bits set) → 1.0
        bits = "0" + "1" * 11
        r = _r(bits)
        assert r.read_normal() == pytest.approx(1.0)

    def test_max_negative(self):
        # negative=1, magnitude=2047 → -1.0
        bits = "1" + "1" * 11
        r = _r(bits)
        assert r.read_normal() == pytest.approx(-1.0)


# ---------------------------------------------------------------------------
# read_3bit_normal
# ---------------------------------------------------------------------------


class TestRead3BitNormal:
    def test_no_x_no_y(self):
        # has_x=0, has_y=0, neg_z=0 → z=1.0 (positive from constraint)
        bits = "0" + "0" + "0"
        r = _r(bits)
        result = r.read_3bit_normal()
        assert result[0] == pytest.approx(0.0)
        assert result[1] == pytest.approx(0.0)
        assert result[2] == pytest.approx(1.0)

    def test_neg_z_flag(self):
        # has_x=0, has_y=0, neg_z=1 → z=-1.0
        bits = "0" + "0" + "1"
        r = _r(bits)
        result = r.read_3bit_normal()
        assert result[2] == pytest.approx(-1.0)

    def test_has_x(self):
        # has_x=1, 12-bit normal (0,2047→1.0); has_y=0, neg_z=0
        # z = sqrt(1 - 1^2) = 0.0
        bits = "1" + "0" + "0" + "1" * 11 + "0"
        r = _r(bits)
        result = r.read_3bit_normal()
        assert result[0] == pytest.approx(1.0)
        assert result[2] == pytest.approx(0.0)

    def test_has_x_and_y(self):
        # Both x and y → z derived from sqrt(1 - x^2 - y^2)
        # Use zero x and y: negative=0, magnitude=0 → 0.0 for both
        bits = "1" + "1" + "0" + "0" * 11 + "0" + "0" * 11 + "0"
        r = _r(bits)
        result = r.read_3bit_normal()
        assert result[0] == pytest.approx(0.0)
        assert result[1] == pytest.approx(0.0)
        assert result[2] == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# peek_bits / skip_bits
# ---------------------------------------------------------------------------


class TestPeekSkipBits:
    def test_peek_bits_does_not_consume_logical_position(self):
        r = BitReader(b"\xab\xcd\x00\x00")
        assert r.position() == "0"
        assert r.peek_bits(8) == 0xAB
        assert r.position() == "0"
        assert r.read_bits(8) == 0xAB
        assert r.position() == "1"

    def test_skip_bits_consumes_peeked_bits(self):
        r = BitReader(b"\xab")
        assert r.peek_bits(4) == 0xB
        r.skip_bits(4)
        assert r.read_bits(4) == 0xA
        assert r.rem_bits() == 0

    def test_peek_bits_exhausted(self):
        r = BitReader(b"\xff")
        with pytest.raises(BufferReadError):
            r.peek_bits(9)


# ---------------------------------------------------------------------------
# position()
# ---------------------------------------------------------------------------


class TestPosition:
    def test_aligned_position(self):
        r = BitReader(b"\x00\x00\x00")
        r.read_bytes(2)
        assert r.position() == "2"

    def test_unaligned_position(self):
        r = BitReader(b"\xff")
        r.read_bits(3)
        assert r.position() == "0.3"

    def test_position_after_4_byte_prefetch(self):
        r = BitReader(b"\xff\x00\x00\x00")
        assert r.read_bits(1) == 1
        assert r.position() == "0.1"
        assert r.rem_bits() == 31
        assert r.read_bits(7) == 0x7F
        assert r.position() == "1"

    def test_initial_position(self):
        r = BitReader(b"\x00")
        assert r.position() == "0"
