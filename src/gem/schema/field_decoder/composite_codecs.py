"""Composite vector and angle decoder factories."""

from __future__ import annotations

from typing import TYPE_CHECKING

from gem.schema.field_decoder.contracts import FieldDecoder, _FieldLike

if TYPE_CHECKING:
    from gem.binary.reader import BitReader


def _vector_normal_decoder(r: BitReader) -> list[float]:
    """Read a packed normalized 3D vector."""
    return list(r.read_3bit_normal())


def _qangle_factory(field: _FieldLike) -> FieldDecoder:
    """Build a QAngle decoder for the field's encoder and bit-count metadata."""
    encoder = field.encoder
    bc = field.bit_count

    if encoder == "qangle_pitch_yaw":
        n = bc or 0

        def pitch_yaw(r: BitReader) -> list[float]:
            return [r.read_angle(n), r.read_angle(n), 0.0]

        return pitch_yaw

    if bc is not None and bc != 0:
        n = bc

        def fixed_angle(r: BitReader) -> list[float]:
            return [r.read_angle(n), r.read_angle(n), r.read_angle(n)]

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
