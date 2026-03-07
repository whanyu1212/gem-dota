"""Field decoders for Dota 2 Source 2 entity fields.

Maps field type strings and encoder hints to callables that read a typed
value from a BitReader.  The dispatch chain mirrors manta/field_decoder.go:

  1. fieldTypeFactories  — type needs constructor-time parameters (QFD, QAngle…)
  2. fieldNameDecoders   — per-name overrides (currently empty, reserved)
  3. fieldTypeDecoders   — direct type → decoder mapping
  4. default             — varuint32

Reference: manta/field_decoder.go, manta/quantizedfloat.go
"""

from __future__ import annotations

import math
import struct
from collections.abc import Callable
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from gem.reader import BitReader


class _FieldLike(Protocol):
    """Structural type for field objects passed to decoder factories."""

    @property
    def field_type(self) -> object: ...

    @property
    def var_name(self) -> str: ...

    @property
    def encoder(self) -> str: ...

    @property
    def bit_count(self) -> int | None: ...

    @property
    def encode_flags(self) -> int | None: ...

    @property
    def low_value(self) -> float | None: ...

    @property
    def high_value(self) -> float | None: ...


# ---------------------------------------------------------------------------
# Type alias
# ---------------------------------------------------------------------------

FieldDecoder = Callable[["BitReader"], object]

# ---------------------------------------------------------------------------
# Quantized float flags (matching Source 2 enum)
# ---------------------------------------------------------------------------

_QFF_ROUNDDOWN = 1 << 0
_QFF_ROUNDUP = 1 << 1
_QFF_ENCODE_ZERO = 1 << 2
_QFF_ENCODE_INTEGERS = 1 << 3


class QuantizedFloatDecoder:
    """Decoder for Source 2 quantized floats (CNetworkedQuantizedFloat).

    Encodes a float in a fixed bit-width with optional round-up/down and
    zero-preservation flags.  Parameters are derived from the field's
    send-table entry.

    Args:
        bit_count: Number of bits used to encode the value, or None/0/>=32
            for no-scale (raw 32-bit IEEE float).
        flags: Bitmask of QFF_* flags, or None for 0.
        low_value: Minimum representable value, or None for 0.0.
        high_value: Maximum representable value, or None for 1.0.
    """

    __slots__ = (
        "low",
        "high",
        "high_low_mul",
        "dec_mul",
        "bitcount",
        "flags",
        "no_scale",
    )

    def __init__(
        self,
        bit_count: int | None,
        flags: int | None,
        low_value: float | None,
        high_value: float | None,
    ) -> None:
        bc = bit_count or 0
        if bc == 0 or bc >= 32:
            self.no_scale = True
            self.bitcount = 32
            self.low = self.high = self.high_low_mul = self.dec_mul = 0.0
            self.flags = 0
            return

        self.no_scale = False
        self.bitcount = bc
        self.low = low_value if low_value is not None else 0.0
        self.high = high_value if high_value is not None else 1.0
        self.flags = flags if flags is not None else 0

        self._validate_flags()

        steps = 1 << self.bitcount
        range_ = self.high - self.low

        if self.flags & _QFF_ROUNDDOWN:
            self.high -= range_ / steps
        elif self.flags & _QFF_ROUNDUP:
            self.low += range_ / steps

        if self.flags & _QFF_ENCODE_INTEGERS:
            delta = max(self.high - self.low, 1.0)
            delta_log2 = math.ceil(math.log2(delta))
            range2 = 1 << int(delta_log2)
            bc2 = self.bitcount
            while (1 << bc2) <= range2:
                bc2 += 1
            if bc2 > self.bitcount:
                self.bitcount = bc2
                steps = 1 << self.bitcount
            offset = range2 / steps
            self.high = self.low + range2 - offset

        self._assign_multipliers(steps)

        # Remove flags that are already satisfied by the multiplier
        if self.flags & _QFF_ROUNDDOWN and self._quantize(self.low) == self.low:
            self.flags &= ~_QFF_ROUNDDOWN
        if self.flags & _QFF_ROUNDUP and self._quantize(self.high) == self.high:
            self.flags &= ~_QFF_ROUNDUP
        if self.flags & _QFF_ENCODE_ZERO and self._quantize(0.0) == 0.0:
            self.flags &= ~_QFF_ENCODE_ZERO

    def _validate_flags(self) -> None:
        if not self.flags:
            return
        if (self.low == 0.0 and self.flags & _QFF_ROUNDDOWN) or (
            self.high == 0.0 and self.flags & _QFF_ROUNDUP
        ):
            self.flags &= ~_QFF_ENCODE_ZERO
        if self.low == 0.0 and self.flags & _QFF_ENCODE_ZERO:
            self.flags |= _QFF_ROUNDDOWN
            self.flags &= ~_QFF_ENCODE_ZERO
        if self.high == 0.0 and self.flags & _QFF_ENCODE_ZERO:
            self.flags |= _QFF_ROUNDUP
            self.flags &= ~_QFF_ENCODE_ZERO
        if self.low > 0.0 or self.high < 0.0:
            self.flags &= ~_QFF_ENCODE_ZERO
        if self.flags & _QFF_ENCODE_INTEGERS:
            self.flags &= ~(_QFF_ROUNDUP | _QFF_ROUNDDOWN | _QFF_ENCODE_ZERO)

    def _assign_multipliers(self, steps: int) -> None:
        range_ = self.high - self.low
        high_int = 0xFFFFFFFE if self.bitcount == 32 else (1 << self.bitcount) - 1
        high_mul = float(high_int) if abs(range_) <= 0.0 else high_int / range_
        # Adjust precision to avoid overflow
        if high_mul * range_ > high_int:
            for mult in (0.9999, 0.99, 0.9, 0.8, 0.7):
                high_mul = high_int / range_ * mult
                if high_mul * range_ <= high_int:
                    break
        self.high_low_mul = high_mul
        self.dec_mul = 1.0 / (steps - 1)

    def _quantize(self, val: float) -> float:
        i = int((val - self.low) * self.high_low_mul)
        return self.low + (self.high - self.low) * (i * self.dec_mul)

    def decode(self, r: BitReader) -> float:
        """Read and decode one quantized float from r.

        Args:
            r: BitReader positioned at the start of the encoded value.

        Returns:
            Decoded float value.
        """
        if self.no_scale:
            return struct.unpack("<f", struct.pack("<I", r.read_bits(32)))[0]
        if self.flags & _QFF_ROUNDDOWN and r.read_boolean():
            return self.low
        if self.flags & _QFF_ROUNDUP and r.read_boolean():
            return self.high
        if self.flags & _QFF_ENCODE_ZERO and r.read_boolean():
            return 0.0
        return self.low + (self.high - self.low) * r.read_bits(self.bitcount) * self.dec_mul


# ---------------------------------------------------------------------------
# Primitive decoders (stateless callables)
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Factory functions — return a decoder configured from field parameters
# ---------------------------------------------------------------------------


def _unsigned_factory(field: _FieldLike) -> FieldDecoder:
    return unsigned_decoder


def _unsigned64_factory(field: _FieldLike) -> FieldDecoder:
    if field.encoder == "fixed64":
        return fixed64_decoder
    return unsigned64_decoder


def _float_factory(field: _FieldLike) -> FieldDecoder:
    if field.encoder == "coord":
        return float_coord_decoder
    if field.encoder == "simtime":
        return simulation_time_decoder
    if field.encoder == "runetime":
        return rune_time_decoder
    bc = field.bit_count
    if bc is None or bc <= 0 or bc >= 32:
        return noscale_decoder
    return _quantized_factory(field)


def _quantized_factory(field: _FieldLike) -> FieldDecoder:
    qfd = QuantizedFloatDecoder(
        bit_count=field.bit_count,
        flags=field.encode_flags,
        low_value=field.low_value,
        high_value=field.high_value,
    )
    return qfd.decode


def _vector_factory(n: int) -> Callable[[_FieldLike], FieldDecoder]:
    def factory(field: _FieldLike) -> FieldDecoder:
        if n == 3 and field.encoder == "normal":
            return _vector_normal_decoder
        component = _float_factory(field)

        def decoder(r: BitReader) -> list[object]:
            return [component(r) for _ in range(n)]

        return decoder

    return factory


def _vector_normal_decoder(r: BitReader) -> list[float]:
    return list(r.read_3bit_normal())


def _qangle_factory(field: _FieldLike) -> FieldDecoder:
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


# ---------------------------------------------------------------------------
# Dispatch tables
# ---------------------------------------------------------------------------

# Types that need a factory (constructor-time parameters)
_FIELD_TYPE_FACTORIES: dict[str, Callable[[_FieldLike], FieldDecoder]] = {
    "float32": _float_factory,
    "CNetworkedQuantizedFloat": _quantized_factory,
    "Vector": _vector_factory(3),
    "Vector2D": _vector_factory(2),
    "Vector4D": _vector_factory(4),
    "VectorWS": _vector_factory(3),
    "uint64": _unsigned64_factory,
    "QAngle": _qangle_factory,
    "CHandle": _unsigned_factory,
    "CStrongHandle": _unsigned64_factory,
    "CEntityHandle": _unsigned_factory,
}

# Types with a fixed decoder (no per-field parameters needed)
_FIELD_TYPE_DECODERS: dict[str, FieldDecoder] = {
    "bool": boolean_decoder,
    "char": string_decoder,
    "color32": unsigned_decoder,
    "int8": signed_decoder,
    "int16": signed_decoder,
    "int32": signed_decoder,
    "int64": signed_decoder,
    "uint8": unsigned_decoder,
    "uint16": unsigned_decoder,
    "uint32": unsigned_decoder,
    "GameTime_t": noscale_decoder,
    "HeroFacetKey_t": unsigned64_decoder,
    "BloodType": unsigned_decoder,
    "CBodyComponent": component_decoder,
    "CGameSceneNodeHandle": unsigned_decoder,
    "Color": unsigned_decoder,
    "CPhysicsComponent": component_decoder,
    "CRenderComponent": component_decoder,
    "CUtlString": string_decoder,
    "CUtlStringToken": unsigned_decoder,
    "CUtlSymbolLarge": string_decoder,
}

# Per-name overrides (reserved, currently empty)
_FIELD_NAME_DECODERS: dict[str, FieldDecoder] = {}


def find_decoder(field: _FieldLike) -> FieldDecoder:
    """Return the appropriate decoder for the given field.

    Dispatch order:
    1. Type factories (QAngle, float32, Vector, …) — need field parameters
    2. Name overrides
    3. Direct type → decoder table
    4. Default (varuint32)

    Args:
        field: An object with ``field_type.base_type``, ``encoder``,
            ``bit_count``, ``encode_flags``, ``low_value``, ``high_value``,
            and ``var_name`` attributes.

    Returns:
        A callable ``(BitReader) -> value``.
    """
    base_type: str = field.field_type.base_type  # type: ignore[attr-defined]

    if base_type in _FIELD_TYPE_FACTORIES:
        return _FIELD_TYPE_FACTORIES[base_type](field)

    var_name: str = getattr(field, "var_name", "")
    if var_name in _FIELD_NAME_DECODERS:
        return _FIELD_NAME_DECODERS[var_name]

    if base_type in _FIELD_TYPE_DECODERS:
        return _FIELD_TYPE_DECODERS[base_type]

    return default_decoder


def find_decoder_by_base_type(base_type: str) -> FieldDecoder:
    """Return a decoder for a base type string without field context.

    Used for variable-array child elements where no field object is available.

    Args:
        base_type: The C++ type name string (e.g. ``"uint32"``).

    Returns:
        A callable ``(BitReader) -> value``.
    """
    return _FIELD_TYPE_DECODERS.get(base_type, default_decoder)
