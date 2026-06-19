"""Stateless scalar field-value decoders."""

from __future__ import annotations

import struct
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gem.binary.reader import BitReader


def boolean_decoder(r: BitReader) -> bool:
    """Read a single boolean bit."""
    return r.read_boolean()


def string_decoder(r: BitReader) -> str:
    """Read a null-terminated UTF-8 string."""
    return r.read_string()


def unsigned_decoder(r: BitReader) -> int:
    """Read a varuint32 as an unsigned integer."""
    return r.read_varuint32()


def signed_decoder(r: BitReader) -> int:
    """Read a zigzag-encoded varint32."""
    return r.read_varint32()


def noscale_decoder(r: BitReader) -> float:
    """Read a raw 32-bit IEEE 754 float."""
    return struct.unpack("<f", struct.pack("<I", r.read_bits(32)))[0]


def float_coord_decoder(r: BitReader) -> float:
    """Read a Source 2 coord-encoded float."""
    return r.read_coord()


def simulation_time_decoder(r: BitReader) -> float:
    """Read a simulation time (varuint32 * 1/30 seconds)."""
    return r.read_varuint32() * (1.0 / 30.0)


def rune_time_decoder(r: BitReader) -> float:
    """Read a rune time (4-bit raw float)."""
    return struct.unpack("<f", struct.pack("<I", r.read_bits(4)))[0]


def unsigned64_decoder(r: BitReader) -> int:
    """Read a varuint64."""
    return r.read_varuint64()


def fixed64_decoder(r: BitReader) -> int:
    """Read a little-endian 64-bit unsigned integer."""
    return r.read_le_uint64()


def component_decoder(r: BitReader) -> int:
    """Read a 1-bit component presence flag."""
    return r.read_bits(1)


def default_decoder(r: BitReader) -> int:
    """Fallback: read a varuint32."""
    return r.read_varuint32()
