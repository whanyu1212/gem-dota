"""
Tests for gem.field_decoder — all field type decoders and QuantizedFloatDecoder.

Reference: manta/field_decoder.go, manta/quantizedfloat.go
"""

import math
import struct

import pytest


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

    def test_rounddown_flag(self, qfd_cls, reader_cls):
        # rounddown flag (bit 0): if first bit is 1, return low
        qfd = self._make_qfd(qfd_cls, 8, 1, 0.0, 1.0)  # flags=1 = rounddown
        # First bit = 1 → return low = 0.0
        r = reader_cls(b"\x01")
        assert qfd.decode(r) == pytest.approx(0.0)

    def test_roundup_flag(self, qfd_cls, reader_cls):
        # roundup flag (bit 1): if bit is 1, return high
        # flags=2 = roundup, no rounddown
        # First rounddown check: bit=0, Second roundup check: bit=1 → return high
        qfd = self._make_qfd(qfd_cls, 8, 2, 0.0, 1.0)
        # bit0=0 (no rounddown), bit1=1 (roundup → return high=1.0)
        r = reader_cls(_bits_to_bytes("01"))
        assert qfd.decode(r) == pytest.approx(1.0)

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
