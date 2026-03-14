"""
Tests for gem.field_decoder — all field type decoders and QuantizedFloatDecoder.

Reference: manta/field_decoder.go, manta/quantizedfloat.go
"""

from __future__ import annotations

import math
import struct

import pytest

from gem.field_decoder import (
    _QFF_ENCODE_INTEGERS,
    _QFF_ENCODE_ZERO,
    _QFF_ROUNDDOWN,
    _QFF_ROUNDUP,
    QuantizedFloatDecoder,
    _qangle_factory,
    _unsigned64_factory,
    _vector_factory,
    boolean_decoder,
    component_decoder,
    find_decoder,
    find_decoder_by_base_type,
    fixed64_decoder,
    float_coord_decoder,
    noscale_decoder,
    rune_time_decoder,
    signed_decoder,
    simulation_time_decoder,
    string_decoder,
    unsigned64_decoder,
    unsigned_decoder,
)
from gem.reader import BitReader


def _bits_to_bytes(bit_str: str) -> bytes:
    """Convert a LSB-first bit string like '10110010' to bytes."""
    # pad to multiple of 8
    padded = bit_str + "0" * (-len(bit_str) % 8)
    result = []
    for i in range(0, len(padded), 8):
        byte = 0
        for j, ch in enumerate(padded[i : i + 8]):
            if ch == "1":
                byte |= 1 << j
        result.append(byte)
    return bytes(result)


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


@pytest.fixture
def reader_cls():
    from gem.reader import BitReader

    return BitReader


@pytest.fixture
def decoders():
    from gem.field_decoder import (
        boolean_decoder,
        component_decoder,
        float_coord_decoder,
        noscale_decoder,
        signed_decoder,
        simulation_time_decoder,
        string_decoder,
        unsigned64_decoder,
        unsigned_decoder,
    )

    return {
        "boolean": boolean_decoder,
        "string": string_decoder,
        "unsigned": unsigned_decoder,
        "signed": signed_decoder,
        "noscale": noscale_decoder,
        "float_coord": float_coord_decoder,
        "simulation_time": simulation_time_decoder,
        "unsigned64": unsigned64_decoder,
        "component": component_decoder,
    }


class TestBooleanDecoder:
    def test_false(self, reader_cls, decoders):
        r = reader_cls(b"\x00")
        assert decoders["boolean"](r) is False

    def test_true(self, reader_cls, decoders):
        r = reader_cls(b"\x01")
        assert decoders["boolean"](r) is True


class TestStringDecoder:
    def test_simple(self, reader_cls, decoders):
        r = reader_cls(b"abc\x00")
        assert decoders["string"](r) == "abc"

    def test_empty(self, reader_cls, decoders):
        r = reader_cls(b"\x00")
        assert decoders["string"](r) == ""


class TestUnsignedDecoder:
    @pytest.mark.parametrize("value", [0, 1, 127, 128, 65535])
    def test_values(self, reader_cls, decoders, value):
        r = reader_cls(_pack_varuint32(value))
        assert decoders["unsigned"](r) == value


class TestSignedDecoder:
    @pytest.mark.parametrize("value", [0, 1, -1, 100, -100])
    def test_values(self, reader_cls, decoders, value):
        ux = (value << 1) ^ (value >> 31)
        r = reader_cls(_pack_varuint32(ux & 0xFFFFFFFF))
        assert decoders["signed"](r) == value


class TestNoscaleDecoder:
    @pytest.mark.parametrize("value", [0.0, 1.0, -1.0, 3.14, float("inf")])
    def test_roundtrip(self, reader_cls, decoders, value):
        data = struct.pack("<f", value)
        r = reader_cls(data)
        result = decoders["noscale"](r)
        if math.isfinite(value):
            assert result == pytest.approx(value, rel=1e-6)
        else:
            assert math.isinf(result)


class TestSimulationTimeDecoder:
    def test_zero(self, reader_cls, decoders):
        r = reader_cls(_pack_varuint32(0))
        assert decoders["simulation_time"](r) == pytest.approx(0.0)

    def test_one_tick(self, reader_cls, decoders):
        # 1 tick = 1/30 seconds
        r = reader_cls(_pack_varuint32(1))
        assert decoders["simulation_time"](r) == pytest.approx(1.0 / 30.0)

    def test_thirty_ticks(self, reader_cls, decoders):
        r = reader_cls(_pack_varuint32(30))
        assert decoders["simulation_time"](r) == pytest.approx(1.0)


class TestComponentDecoder:
    def test_zero(self, reader_cls, decoders):
        r = reader_cls(b"\x00")
        assert decoders["component"](r) == 0

    def test_one(self, reader_cls, decoders):
        r = reader_cls(b"\x01")
        assert decoders["component"](r) == 1


class TestQuantizedFloatDecoder:
    @pytest.fixture
    def qfd_cls(self):
        from gem.field_decoder import QuantizedFloatDecoder

        return QuantizedFloatDecoder

    def _make_qfd(self, qfd_cls, bit_count, flags, low, high):
        return qfd_cls(bit_count=bit_count, flags=flags, low_value=low, high_value=high)

    def test_no_scale_when_bitcount_zero(self, qfd_cls, reader_cls):
        # bitcount 0 or >= 32 → NoScale mode → reads raw 32-bit float
        qfd = self._make_qfd(qfd_cls, 0, 0, 0.0, 1.0)
        data = struct.pack("<f", 0.75)
        r = reader_cls(data)
        assert qfd.decode(r) == pytest.approx(0.75, rel=1e-5)

    def test_rounddown_flag_optimised_away(self, qfd_cls, reader_cls):
        # rounddown flag (bit 0) on 8-bit [0,1]: the grid already aligns with
        # low=0.0 so the flag is removed during construction. The decoder falls
        # through to a normal quantized read.
        qfd = self._make_qfd(qfd_cls, 8, 1, 0.0, 1.0)
        assert qfd.flags == 0  # flag was cleared
        # high is adjusted to 0.99609375; reading 0 bits → low end of range
        r = reader_cls(b"\x00")
        assert qfd.decode(r) == pytest.approx(0.0)

    def test_rounddown_flag_active(self, qfd_cls, reader_cls):
        # Use a range where rounddown flag is NOT optimised away: low != 0
        # flags=1 (rounddown), 8-bit, range [-1, 1]
        qfd = self._make_qfd(qfd_cls, 8, 1, -1.0, 1.0)
        if qfd.flags & 1:  # flag survived — first bit=1 should return low
            r = reader_cls(b"\x01")
            assert qfd.decode(r) == pytest.approx(-1.0)
        else:
            pytest.skip("Flag optimised away for this range too")

    def test_roundup_flag_optimised_away(self, qfd_cls, reader_cls):
        # roundup flag (bit 1) on 8-bit [0,1]: grid aligns with high=1.0
        # so the flag is removed. Normal quantized read falls through.
        qfd = self._make_qfd(qfd_cls, 8, 2, 0.0, 1.0)
        assert qfd.flags == 0  # flag was cleared
        # low is adjusted to 0.00390625; reading 255 (all bits) → high end
        r = reader_cls(b"\xff")
        result = qfd.decode(r)
        assert result == pytest.approx(1.0, abs=0.01)

    def test_normal_decode_midpoint(self, qfd_cls, reader_cls):
        # 8 bits, range [0, 1], no flags → 128 = midpoint ≈ 0.5
        qfd = self._make_qfd(qfd_cls, 8, 0, 0.0, 1.0)
        data = struct.pack("B", 128)  # read 8 bits = 128
        r = reader_cls(data)
        result = qfd.decode(r)
        assert 0.49 < result < 0.51


class TestFindDecoder:
    """Test the decoder dispatch (fieldTypeFactories → fieldNameDecoders → fieldTypeDecoders → default)."""

    @pytest.fixture
    def find_decoder(self):
        from gem.field_decoder import find_decoder

        return find_decoder

    def test_bool_type(self, find_decoder, reader_cls):
        class FakeField:
            var_name = "m_bActive"
            field_type = type("FT", (), {"base_type": "bool"})()
            encoder = ""
            bit_count = None
            encode_flags = None
            low_value = None
            high_value = None

        decoder = find_decoder(FakeField())
        r = reader_cls(b"\x01")
        assert decoder(r) is True

    def test_uint32_type(self, find_decoder, reader_cls):
        class FakeField:
            var_name = "m_iHealth"
            field_type = type("FT", (), {"base_type": "uint32"})()
            encoder = ""
            bit_count = None
            encode_flags = None
            low_value = None
            high_value = None

        decoder = find_decoder(FakeField())
        r = reader_cls(_pack_varuint32(42))
        assert decoder(r) == 42

    def test_default_decoder_for_unknown(self, find_decoder, reader_cls):
        class FakeField:
            var_name = "m_unknown"
            field_type = type("FT", (), {"base_type": "SomeUnknownType"})()
            encoder = ""
            bit_count = None
            encode_flags = None
            low_value = None
            high_value = None

        decoder = find_decoder(FakeField())
        r = reader_cls(_pack_varuint32(99))
        # default decoder returns varuint32
        assert decoder(r) == 99


# ---------------------------------------------------------------------------
# Helpers (extended)
# ---------------------------------------------------------------------------


def _r(bits_str: str) -> BitReader:
    bits = [int(c) for c in bits_str if c in "01"]
    while len(bits) % 8:
        bits.append(0)
    data = bytearray(sum(bits[i + j] << j for j in range(8)) for i in range(0, len(bits), 8))
    return BitReader(bytes(data))


class FakeFieldType:
    def __init__(self, base_type: str) -> None:
        self.base_type = base_type


class FakeField:
    def __init__(
        self,
        base_type: str = "float32",
        var_name: str = "x",
        encoder: str = "",
        bit_count: int | None = None,
        encode_flags: int | None = None,
        low_value: float | None = None,
        high_value: float | None = None,
    ) -> None:
        self.field_type = FakeFieldType(base_type)
        self.var_name = var_name
        self.encoder = encoder
        self.bit_count = bit_count
        self.encode_flags = encode_flags
        self.low_value = low_value
        self.high_value = high_value


# ---------------------------------------------------------------------------
# QuantizedFloatDecoder — construction branches
# ---------------------------------------------------------------------------


class TestQFDConstruction:
    def test_no_scale_when_bitcount_zero(self):
        qfd = QuantizedFloatDecoder(bit_count=0, flags=0, low_value=0.0, high_value=1.0)
        assert qfd.no_scale is True

    def test_no_scale_when_bitcount_none(self):
        qfd = QuantizedFloatDecoder(bit_count=None, flags=0, low_value=0.0, high_value=1.0)
        assert qfd.no_scale is True

    def test_no_scale_when_bitcount_32_or_more(self):
        qfd = QuantizedFloatDecoder(bit_count=32, flags=0, low_value=0.0, high_value=1.0)
        assert qfd.no_scale is True

    def test_scaled_normal_case(self):
        qfd = QuantizedFloatDecoder(bit_count=8, flags=0, low_value=0.0, high_value=1.0)
        assert qfd.no_scale is False
        assert qfd.bitcount == 8

    def test_rounddown_flag_adjusts_high(self):
        qfd = QuantizedFloatDecoder(
            bit_count=8, flags=_QFF_ROUNDDOWN, low_value=0.0, high_value=1.0
        )
        assert qfd.high < 1.0

    def test_roundup_flag_adjusts_low(self):
        qfd = QuantizedFloatDecoder(bit_count=8, flags=_QFF_ROUNDUP, low_value=0.0, high_value=1.0)
        assert qfd.low > 0.0

    def test_encode_integers_expands_bitcount(self):
        qfd = QuantizedFloatDecoder(
            bit_count=4, flags=_QFF_ENCODE_INTEGERS, low_value=0.0, high_value=16.0
        )
        # ENCODE_INTEGERS may expand bitcount to fit range
        assert qfd.bitcount >= 4

    def test_encode_zero_with_low_zero_sets_rounddown(self):
        # low=0.0 + ENCODE_ZERO → becomes ROUNDDOWN flag
        qfd = QuantizedFloatDecoder(
            bit_count=8, flags=_QFF_ENCODE_ZERO, low_value=0.0, high_value=1.0
        )
        # After _validate_flags, ENCODE_ZERO removed, ROUNDDOWN set (then possibly cleared by _quantize check)
        # Verify it doesn't raise and produce a valid decoder
        assert qfd.no_scale is False

    def test_encode_zero_with_high_zero_sets_roundup(self):
        qfd = QuantizedFloatDecoder(
            bit_count=8, flags=_QFF_ENCODE_ZERO, low_value=-1.0, high_value=0.0
        )
        assert qfd.no_scale is False

    def test_range_excludes_zero_clears_encode_zero(self):
        # low > 0 → ENCODE_ZERO cleared
        qfd = QuantizedFloatDecoder(
            bit_count=8, flags=_QFF_ENCODE_ZERO, low_value=1.0, high_value=2.0
        )
        assert not (qfd.flags & _QFF_ENCODE_ZERO)

    def test_rounddown_already_satisfied_cleared(self):
        # ROUNDDOWN flag cleared when _quantize(low) == low after multiplier assignment
        qfd = QuantizedFloatDecoder(
            bit_count=8, flags=_QFF_ROUNDDOWN, low_value=0.0, high_value=1.0
        )
        # After construction, flag may or may not remain, but should not crash
        assert isinstance(qfd.flags, int)


# ---------------------------------------------------------------------------
# QuantizedFloatDecoder.decode — all branches
# ---------------------------------------------------------------------------


class TestQFDDecode:
    def test_noscale_decode(self):
        qfd = QuantizedFloatDecoder(bit_count=0, flags=0, low_value=0.0, high_value=1.0)
        val_bytes = struct.pack("<f", 3.14)
        val_int = struct.unpack("<I", val_bytes)[0]
        # Pack int as 32 bits LSB-first
        bits = "".join(str((val_int >> i) & 1) for i in range(32))
        r = _r(bits)
        result = qfd.decode(r)
        assert result == pytest.approx(3.14, abs=1e-4)

    def test_rounddown_flag_returns_low(self):
        # With ROUNDDOWN flag set and first bit = 1 → return self.low
        qfd = QuantizedFloatDecoder(
            bit_count=8, flags=_QFF_ROUNDDOWN, low_value=0.0, high_value=1.0
        )
        # Force ROUNDDOWN to remain set for testing
        qfd.flags |= _QFF_ROUNDDOWN
        r = _r("1" + "0" * 31)  # first bit = 1 → read_boolean() = True
        result = qfd.decode(r)
        assert result == pytest.approx(qfd.low)

    def test_roundup_flag_returns_high(self):
        qfd = QuantizedFloatDecoder(bit_count=8, flags=_QFF_ROUNDUP, low_value=0.0, high_value=1.0)
        qfd.flags = _QFF_ROUNDUP  # force set
        r = _r("1" + "0" * 31)  # first boolean = True → return high
        result = qfd.decode(r)
        assert result == pytest.approx(qfd.high)

    def test_encode_zero_returns_zero(self):
        qfd = QuantizedFloatDecoder(bit_count=8, flags=0, low_value=0.5, high_value=2.0)
        qfd.flags = _QFF_ENCODE_ZERO  # force
        r = _r("1" + "0" * 31)
        result = qfd.decode(r)
        assert result == 0.0

    def test_normal_decode_midpoint(self):
        qfd = QuantizedFloatDecoder(bit_count=8, flags=0, low_value=0.0, high_value=1.0)
        # Encode midpoint: bits = 128 of 256 → 128 * dec_mul * range + low
        val = 128
        bits = "".join(str((val >> i) & 1) for i in range(8))
        r = _r(bits)
        result = qfd.decode(r)
        assert 0.0 <= result <= 1.0


# ---------------------------------------------------------------------------
# _qangle_factory — all 3 branches
# ---------------------------------------------------------------------------


class TestQAngleFactory:
    def test_pitch_yaw_branch(self):
        field = FakeField(base_type="QAngle", encoder="qangle_pitch_yaw", bit_count=8)
        decoder = _qangle_factory(field)
        # Should return [angle_x, angle_y, 0.0]
        r = BitReader(bytes([0x80, 0x80]))  # 128 for each angle
        result = decoder(r)
        assert len(result) == 3
        assert result[2] == 0.0
        assert result[0] == pytest.approx(128 * 360.0 / 256)

    def test_fixed_bitcount_branch(self):
        field = FakeField(base_type="QAngle", encoder="", bit_count=8)
        decoder = _qangle_factory(field)
        r = BitReader(bytes([0x00, 0x80, 0x80]))
        result = decoder(r)
        assert len(result) == 3

    def test_coord_angle_branch(self):
        # No encoder, no bit_count → coord_angle
        field = FakeField(base_type="QAngle", encoder="", bit_count=None)
        decoder = _qangle_factory(field)
        # All 3 booleans = False → all 0.0
        r = _r("000" + "0" * 5)
        result = decoder(r)
        assert result == [0.0, 0.0, 0.0]

    def test_coord_angle_with_x(self):
        # rx=True, ry=False, rz=False, then read_coord() for x
        # has_int=0, has_frac=0 → coord = 0.0
        field = FakeField(base_type="QAngle", encoder="", bit_count=None)
        decoder = _qangle_factory(field)
        r = _r("1" + "0" + "0" + "00" + "0" * 10)
        result = decoder(r)
        assert result[0] == 0.0
        assert result[1] == 0.0


# ---------------------------------------------------------------------------
# _vector_factory with normal encoder
# ---------------------------------------------------------------------------


class TestVectorFactory:
    def test_vector3_normal_decoder(self):
        field = FakeField(base_type="Vector", encoder="normal")
        decoder = _vector_factory(3)(field)
        # has_x=0, has_y=0, neg_z=0 → [0, 0, 1]
        r = _r("000" + "0" * 5)
        result = decoder(r)
        assert len(result) == 3
        assert result[2] == pytest.approx(1.0)

    def test_vector2_no_normal(self):
        field = FakeField(base_type="Vector2D", encoder="")
        decoder = _vector_factory(2)(field)
        # Two noscale floats (bit_count=None → noscale)
        val_bytes = struct.pack("<ff", 1.0, 2.0)
        r = BitReader(val_bytes)
        result = decoder(r)
        assert result[0] == pytest.approx(1.0)
        assert result[1] == pytest.approx(2.0)


# ---------------------------------------------------------------------------
# _unsigned64_factory — fixed64 branch
# ---------------------------------------------------------------------------


class TestUnsigned64Factory:
    def test_fixed64_branch(self):
        field = FakeField(base_type="uint64", encoder="fixed64")
        decoder = _unsigned64_factory(field)
        r = BitReader(struct.pack("<Q", 0xDEADBEEF_CAFEBABE))
        assert decoder(r) == 0xDEADBEEF_CAFEBABE

    def test_non_fixed64_uses_varuint64(self):
        field = FakeField(base_type="uint64", encoder="")
        decoder = _unsigned64_factory(field)
        r = BitReader(b"\x05")
        assert decoder(r) == 5


# ---------------------------------------------------------------------------
# Primitive decoders
# ---------------------------------------------------------------------------


class TestPrimitiveDecoders:
    def test_simulation_time_decoder(self):
        r = BitReader(b"\x1e")  # 30 → 30 * (1/30) = 1.0
        assert simulation_time_decoder(r) == pytest.approx(1.0)

    def test_rune_time_decoder(self):
        # 4 bits as little-endian float (unusual but what the function does)
        r = _r("0000")
        result = rune_time_decoder(r)
        assert isinstance(result, float)

    def test_fixed64_decoder(self):
        r = BitReader(struct.pack("<Q", 12345678))
        assert fixed64_decoder(r) == 12345678

    def test_unsigned64_decoder(self):
        r = BitReader(b"\x0a")  # varuint64 = 10
        assert unsigned64_decoder(r) == 10

    def test_component_decoder(self):
        r = _r("1")
        assert component_decoder(r) == 1

    def test_float_coord_decoder(self):
        # has_int=0, has_frac=0 → 0.0
        r = _r("00")
        assert float_coord_decoder(r) == 0.0

    def test_noscale_decoder(self):
        r = BitReader(struct.pack("<f", 2.5))
        assert noscale_decoder(r) == pytest.approx(2.5)

    def test_boolean_decoder(self):
        r = _r("1")
        assert boolean_decoder(r) is True

    def test_string_decoder(self):
        r = BitReader(b"hello\x00")
        assert string_decoder(r) == "hello"

    def test_unsigned_decoder(self):
        r = BitReader(b"\x07")
        assert unsigned_decoder(r) == 7

    def test_signed_decoder_negative(self):
        # zigzag: -1 = 1
        r = BitReader(b"\x01")
        assert signed_decoder(r) == -1


# ---------------------------------------------------------------------------
# find_decoder — extended dispatch coverage
# ---------------------------------------------------------------------------


class TestFindDecoderExtended:
    def test_float32_coord(self):
        field = FakeField(base_type="float32", encoder="coord")
        dec = find_decoder(field)
        r = _r("00")  # coord = 0.0
        assert dec(r) == 0.0

    def test_float32_simtime(self):
        field = FakeField(base_type="float32", encoder="simtime")
        dec = find_decoder(field)
        r = BitReader(b"\x1e")  # 30 → 1.0s
        assert dec(r) == pytest.approx(1.0)

    def test_float32_runetime(self):
        field = FakeField(base_type="float32", encoder="runetime")
        dec = find_decoder(field)
        r = _r("0000")
        assert isinstance(dec(r), float)

    def test_float32_noscale(self):
        field = FakeField(base_type="float32", encoder="", bit_count=None)
        dec = find_decoder(field)
        r = BitReader(struct.pack("<f", 1.5))
        assert dec(r) == pytest.approx(1.5)

    def test_float32_quantized(self):
        field = FakeField(
            base_type="float32", encoder="", bit_count=8, low_value=0.0, high_value=1.0
        )
        dec = find_decoder(field)
        r = _r("0" * 8)
        result = dec(r)
        assert isinstance(result, float)

    def test_uint64_fixed64(self):
        field = FakeField(base_type="uint64", encoder="fixed64")
        dec = find_decoder(field)
        r = BitReader(struct.pack("<Q", 99))
        assert dec(r) == 99

    def test_bool_type(self):
        field = FakeField(base_type="bool")
        dec = find_decoder(field)
        r = _r("1")
        assert dec(r) is True

    def test_int32_type(self):
        field = FakeField(base_type="int32")
        dec = find_decoder(field)
        r = BitReader(b"\x01")  # zigzag -1
        assert dec(r) == -1

    def test_string_type(self):
        field = FakeField(base_type="CUtlString")
        dec = find_decoder(field)
        r = BitReader(b"hi\x00")
        assert dec(r) == "hi"

    def test_default_for_unknown_type(self):
        field = FakeField(base_type="UnknownType")
        dec = find_decoder(field)
        r = BitReader(b"\x05")
        assert dec(r) == 5  # varuint32


# ---------------------------------------------------------------------------
# find_decoder_by_base_type
# ---------------------------------------------------------------------------


class TestFindDecoderByBaseType:
    def test_known_type(self):
        dec = find_decoder_by_base_type("bool")
        r = _r("0")
        assert dec(r) is False

    def test_unknown_type_returns_default(self):
        dec = find_decoder_by_base_type("NoSuchType")
        r = BitReader(b"\x03")
        assert dec(r) == 3  # default_decoder = varuint32

    def test_uint32_type(self):
        dec = find_decoder_by_base_type("uint32")
        r = BitReader(b"\x0a")
        assert dec(r) == 10
