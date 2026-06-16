"""Public field-value decoder API.

Implementation modules use domain-specific names to avoid confusion with
``binary.reader`` and ``schema.field_reader``. Callers should continue to import
from ``gem.schema.field_decoder``.
"""

from gem.schema.field_decoder.composite_codecs import _qangle_factory, _vector_normal_decoder
from gem.schema.field_decoder.contracts import FieldDecoder, _FieldLike, _FieldTypeLike
from gem.schema.field_decoder.quantized_float import (
    _QFF_ENCODE_INTEGERS,
    _QFF_ENCODE_ZERO,
    _QFF_ROUNDDOWN,
    _QFF_ROUNDUP,
    QuantizedFloatDecoder,
)
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
from gem.schema.field_decoder.type_resolver import (
    _FIELD_NAME_DECODERS,
    _FIELD_TYPE_DECODERS,
    _FIELD_TYPE_FACTORIES,
    _float_factory,
    _quantized_factory,
    _unsigned64_factory,
    _unsigned_factory,
    _vector_factory,
    find_decoder,
    find_decoder_by_base_type,
)

__all__ = [
    "FieldDecoder",
    "QuantizedFloatDecoder",
    "_FIELD_NAME_DECODERS",
    "_FIELD_TYPE_DECODERS",
    "_FIELD_TYPE_FACTORIES",
    "_FieldLike",
    "_FieldTypeLike",
    "_QFF_ENCODE_INTEGERS",
    "_QFF_ENCODE_ZERO",
    "_QFF_ROUNDDOWN",
    "_QFF_ROUNDUP",
    "_float_factory",
    "_qangle_factory",
    "_quantized_factory",
    "_unsigned64_factory",
    "_unsigned_factory",
    "_vector_factory",
    "_vector_normal_decoder",
    "boolean_decoder",
    "component_decoder",
    "default_decoder",
    "find_decoder",
    "find_decoder_by_base_type",
    "fixed64_decoder",
    "float_coord_decoder",
    "noscale_decoder",
    "rune_time_decoder",
    "signed_decoder",
    "simulation_time_decoder",
    "string_decoder",
    "unsigned64_decoder",
    "unsigned_decoder",
]
