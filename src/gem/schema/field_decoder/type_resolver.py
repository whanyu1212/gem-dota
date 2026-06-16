"""Field type and encoder dispatch for entity field-value decoders."""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from gem.schema.field_decoder.composite_codecs import _qangle_factory, _vector_normal_decoder
from gem.schema.field_decoder.contracts import FieldDecoder, _FieldLike
from gem.schema.field_decoder.quantized_float import QuantizedFloatDecoder
from gem.schema.field_decoder.scalar_codecs import (
    boolean_decoder,
    component_decoder,
    default_decoder,
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

if TYPE_CHECKING:
    from gem.binary.reader import BitReader


def _unsigned_factory(field: _FieldLike) -> FieldDecoder:
    """Return the standard unsigned decoder for field types with unused metadata."""
    return unsigned_decoder


def _unsigned64_factory(field: _FieldLike) -> FieldDecoder:
    """Return the uint64 decoder variant selected by field encoder metadata."""
    if field.encoder == "fixed64":
        return fixed64_decoder
    return unsigned64_decoder


def _float_factory(field: _FieldLike) -> FieldDecoder:
    """Return the float decoder variant selected by field encoder metadata."""
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
    """Create a quantized-float decoder from send-table field metadata."""
    qfd = QuantizedFloatDecoder(
        bit_count=field.bit_count,
        flags=field.encode_flags,
        low_value=field.low_value,
        high_value=field.high_value,
    )
    return qfd.decode


def _vector_factory(n: int) -> Callable[[_FieldLike], FieldDecoder]:
    """Create a vector decoder factory for vectors with n float components."""

    def factory(field: _FieldLike) -> FieldDecoder:
        if n == 3 and field.encoder == "normal":
            return _vector_normal_decoder
        component = _float_factory(field)

        def decoder(r: BitReader) -> list[object]:
            return [component(r) for _ in range(n)]

        return decoder

    return factory


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

_FIELD_NAME_DECODERS: dict[str, FieldDecoder] = {}


def find_decoder(field: _FieldLike) -> FieldDecoder:
    """Return the appropriate decoder for the given field.

    Dispatch order:
    1. Type factories (QAngle, float32, Vector, ...) - need field parameters
    2. Name overrides
    3. Direct type -> decoder table
    4. Default (varuint32)

    Args:
        field: An object with ``field_type.base_type``, ``encoder``,
            ``bit_count``, ``encode_flags``, ``low_value``, ``high_value``,
            and ``var_name`` attributes.

    Returns:
        A callable ``(BitReader) -> value``.
    """
    base_type = field.field_type.base_type

    if base_type in _FIELD_TYPE_FACTORIES:
        return _FIELD_TYPE_FACTORIES[base_type](field)

    var_name = getattr(field, "var_name", "")
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
