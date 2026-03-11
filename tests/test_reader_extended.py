"""Extended tests for gem.reader — covering uncovered paths.

Targets: read_bytes (unaligned path), read_bits_as_bytes (remainder bits),
read_varuint64 (overflow), read_varint64, read_ubit_var_fp (all 5 branches),
read_coord (all flag combos), read_angle, read_normal, read_3bit_normal,
position() (both forms), BufferError on exhaustion.
"""

from __future__ import annotations

import pytest

from gem.reader import BitReader, BufferError

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


# ---------------------------------------------------------------------------
# BufferError
# ---------------------------------------------------------------------------


class TestBufferError:
    def test_read_bits_exhausted(self):
        r = BitReader(b"\xff")
        r.read_bits(8)  # consume all
        with pytest.raises(BufferError):
            r.read_bits(1)

    def test_read_bytes_too_many(self):
        r = BitReader(b"\x01\x02")
        with pytest.raises(BufferError):
            r.read_bytes(3)

    def test_read_bytes_unaligned_exhausted(self):
        r = BitReader(b"\xff")
        r.read_bits(1)  # partial byte → unaligned
        with pytest.raises(BufferError):
            r.read_bytes(2)


# ---------------------------------------------------------------------------
# read_bytes — unaligned path
# ---------------------------------------------------------------------------


class TestReadBytesUnaligned:
    def test_unaligned_read_bytes(self):
        # After reading 4 bits, read_bytes must use the unaligned (bit-by-bit) path
        r = BitReader(bytes([0b10110100, 0b00001010]))
        r.read_bits(4)  # consume low nibble, now unaligned
        result = r.read_bytes(1)
        assert len(result) == 1
        # Low nibble of second byte's contribution follows the high nibble of first
        assert isinstance(result, bytes)

    def test_aligned_fast_path(self):
        r = BitReader(b"\xab\xcd")
        result = r.read_bytes(2)
        assert result == b"\xab\xcd"


# ---------------------------------------------------------------------------
# read_bits_as_bytes — remainder bits
# ---------------------------------------------------------------------------


class TestReadBitsAsBytes:
    def test_exact_multiple_of_8(self):
        r = BitReader(b"\xab\xcd")
        result = r.read_bits_as_bytes(16)
        assert result == b"\xab\xcd"

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
# read_coord — all flag combinations
# ---------------------------------------------------------------------------


class TestReadCoord:
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
        pos = r.position()
        assert "." in pos  # format: "byte.bit_offset"

    def test_initial_position(self):
        r = BitReader(b"\x00")
        assert r.position() == "0"
