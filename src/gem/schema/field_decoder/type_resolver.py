"""Field type and encoder dispatch for entity field-value decoders.

Reference: dotabuff/manta field_decoder.go ``findDecoder`` and
skadistats/clarity S2DecoderFactory.java (pinned revisions in CLAUDE.md). The
``fixed8`` encoder postdates those pins: manta d29a0824 (``fixed8Decoder``) and
clarity 17b33df6 (its ``ENCODERS`` map).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from gem.schema.field_decoder.composite_codecs import _qangle_factory, _vector_normal_decoder
from gem.schema.field_decoder.contracts import FieldDecoder, _FieldLike
from gem.schema.field_decoder.quantized_float import QuantizedFloatDecoder
from gem.schema.field_decoder.scalar_codecs import (
    binary_block_decoder,
    boolean_decoder,
    component_decoder,
    default_decoder,
    fixed8_decoder,
    fixed8_signed_decoder,
    fixed64_decoder,
    float_coord_decoder,
    hsequence_decoder,
    noscale_decoder,
    rune_time_decoder,
    signed64_decoder,
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
    "Quaternion": _vector_factory(4),
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
    "int64": signed64_decoder,
    "uint8": unsigned_decoder,
    "uint16": unsigned_decoder,
    "uint32": unsigned_decoder,
    # Zigzag-signed, though neither pinned Manta nor Clarity maps them: decoded
    # unsigned, every ID reads 2x and the -1 "none" value reads 1 (HY-174,
    # HY-176). OpenDota halves player IDs instead, which turns -1 into slot 0.
    "AbilityID_t": signed_decoder,
    "PlayerID_t": signed_decoder,
    "HeroID_t": signed_decoder,
    "GameTime_t": noscale_decoder,
    "HeroFacetKey_t": unsigned64_decoder,
    "HSequence": hsequence_decoder,
    "BloodType": fixed8_decoder,
    "CBodyComponent": component_decoder,
    "CGameSceneNodeHandle": unsigned_decoder,
    "Color": unsigned_decoder,
    "CPhysicsComponent": component_decoder,
    "CRenderComponent": component_decoder,
    "CUtlString": string_decoder,
    "CUtlStringToken": unsigned_decoder,
    "CUtlSymbolLarge": string_decoder,
    "CUtlBinaryBlock": binary_block_decoder,
    "CGlobalSymbol": string_decoder,
    "ResourceId_t": unsigned64_decoder,
}

_FIELD_NAME_DECODERS: dict[str, FieldDecoder] = {}


def _encoder_decoder(encoder: str, base_type: str) -> FieldDecoder | None:
    """Return the decoder a var encoder forces whatever the type, if any.

    Since build 6951 the send tables mark 90 field definitions (~25k serializer
    slots) ``fixed8`` (``uint8``, ``int8``, enums such as ``MoveType_t``,
    ``CNetworkUtlVectorBase< uint8 >`` elements): the server writes 8 raw bits. Read as varints they agree only
    below 128, so a 255 swallows the next bytes and shifts every later field
    (HY-177). Clarity likewise checks its encoder map before the type table.
    """
    if encoder == "fixed8":
        return fixed8_signed_decoder if base_type == "int8" else fixed8_decoder
    return None


def find_decoder(field: _FieldLike) -> FieldDecoder:
    """Return the appropriate decoder for the given field.

    Dispatch order:
    1. Var encoders that apply to any type (``fixed8``)
    2. Type factories (QAngle, float32, Vector, ...) - need field parameters
    3. Name overrides
    4. Direct type -> decoder table
    5. Default (varuint32)

    Args:
        field: An object with ``field_type.base_type``, ``encoder``,
            ``bit_count``, ``encode_flags``, ``low_value``, ``high_value``,
            and ``var_name`` attributes.

    Returns:
        A callable ``(BitReader) -> value``.
    """
    base_type = field.field_type.base_type

    forced = _encoder_decoder(field.encoder, base_type)
    if forced is not None:
        return forced

    if base_type in _FIELD_TYPE_FACTORIES:
        return _FIELD_TYPE_FACTORIES[base_type](field)

    if field.var_name in _FIELD_NAME_DECODERS:
        return _FIELD_NAME_DECODERS[field.var_name]

    if base_type in _FIELD_TYPE_DECODERS:
        return _FIELD_TYPE_DECODERS[base_type]

    return default_decoder


def find_decoder_by_base_type(base_type: str, encoder: str = "") -> FieldDecoder:
    """Return a decoder for a base type string without field context.

    Used for variable-array child elements, which take the array field's var
    encoder: a ``fixed8`` ``CNetworkUtlVectorBase< uint8 >`` keeps a varint
    length but stores 8-bit elements.

    Args:
        base_type: The C++ type name string (e.g. ``"uint32"``).
        encoder: The owning field's var encoder (``""`` when none).

    Returns:
        A callable ``(BitReader) -> value``.
    """
    forced = _encoder_decoder(encoder, base_type)
    if forced is not None:
        return forced
    return _FIELD_TYPE_DECODERS.get(base_type, default_decoder)
