"""Composite vector and angle decoder factories."""

from __future__ import annotations

from typing import TYPE_CHECKING

from gem.schema.field_decoder.contracts import FieldDecoder, _FieldLike
from gem.schema.field_decoder.scalar_codecs import noscale_decoder

if TYPE_CHECKING:
    from gem.binary.reader import BitReader


#: Bits per angle under ``qangle_precise``. Build 6956 replays declare it in the send
#: tables (``coord_size_params.angle_bits``), which are checked against it.
PRECISE_ANGLE_BITS = 20


def _vector_normal_decoder(r: BitReader) -> list[float]:
    """Read a packed normalized 3D vector."""
    return list(r.read_3bit_normal())


def _qangle_factory(field: _FieldLike) -> FieldDecoder:
    """Build a QAngle decoder for the field's encoder and bit-count metadata.

    Branch order follows Clarity's ``QAngleDecoderFactory``: a 32-bit count means
    raw floats even under ``qangle_precise`` (18e6bdf6, a CS2 declaration). Manta
    tests ``qangle_precise`` first; no Dota field declares it.
    """
    encoder = field.encoder
    bc = field.bit_count or 0

    if encoder == "qangle_pitch_yaw":
        if bc in (0, 32):

            def pitch_yaw_floats(r: BitReader) -> list[float]:
                return [noscale_decoder(r), noscale_decoder(r), 0.0]

            return pitch_yaw_floats

        def pitch_yaw(r: BitReader) -> list[float]:
            return [r.read_angle(bc), r.read_angle(bc), 0.0]

        return pitch_yaw

    if bc == 32:

        def raw_floats(r: BitReader) -> list[float]:
            return [noscale_decoder(r), noscale_decoder(r), noscale_decoder(r)]

        return raw_floats

    if encoder == "qangle_precise":

        def precise_angle(r: BitReader) -> list[float]:
            present = (r.read_boolean(), r.read_boolean(), r.read_boolean())
            return [r.read_angle(PRECISE_ANGLE_BITS) if has else 0.0 for has in present]

        return precise_angle

    if bc != 0:

        def fixed_angle(r: BitReader) -> list[float]:
            return [r.read_angle(bc), r.read_angle(bc), r.read_angle(bc)]

        return fixed_angle

    def coord_angle(r: BitReader) -> list[float]:
        ret = [0.0, 0.0, 0.0]
        rx, ry, rz = r.read_boolean(), r.read_boolean(), r.read_boolean()
        if rx:
            ret[0] = r.read_coord()
        if ry:
            ret[1] = r.read_coord()
        if rz:
            ret[2] = r.read_coord()
        return ret

    return coord_angle
