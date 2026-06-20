"""Public field-value decoder API.

Implementation modules use domain-specific names to avoid confusion with
``binary.reader`` and ``schema.field_reader``. Callers should continue to import
from ``gem.schema.field_decoder``. ``__all__`` lists the stable public surface:
the named scalar/composite decoders, the ``find_decoder`` lookups, and the
``FieldDecoder``/``QuantizedFloatDecoder`` types. The underscore-prefixed names
re-exported below (decoder factories, quantized-float flag constants, the
dispatch tables, and the ``_FieldLike``/``_FieldTypeLike`` protocols) are
internal helpers shared with sibling modules and tests — importable by name, but
not part of the public contract.
"""

# Underscore-prefixed names use redundant ``as`` aliases to mark them as
# deliberate re-exports (shared internals, not public API) without listing them
# in ``__all__``.
from gem.schema.field_decoder.composite_codecs import (
    _qangle_factory as _qangle_factory,
    _vector_normal_decoder as _vector_normal_decoder,
)
from gem.schema.field_decoder.contracts import (
    FieldDecoder,
    _FieldLike as _FieldLike,
    _FieldTypeLike as _FieldTypeLike,
)
from gem.schema.field_decoder.quantized_float import (
    _QFF_ENCODE_INTEGERS as _QFF_ENCODE_INTEGERS,
    _QFF_ENCODE_ZERO as _QFF_ENCODE_ZERO,
    _QFF_ROUNDDOWN as _QFF_ROUNDDOWN,
    _QFF_ROUNDUP as _QFF_ROUNDUP,
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
    _FIELD_NAME_DECODERS as _FIELD_NAME_DECODERS,
    _FIELD_TYPE_DECODERS as _FIELD_TYPE_DECODERS,
    _FIELD_TYPE_FACTORIES as _FIELD_TYPE_FACTORIES,
    _float_factory as _float_factory,
    _quantized_factory as _quantized_factory,
    _unsigned64_factory as _unsigned64_factory,
    _unsigned_factory as _unsigned_factory,
    _vector_factory as _vector_factory,
    find_decoder,
    find_decoder_by_base_type,
)

__all__ = [
    "FieldDecoder",
    "QuantizedFloatDecoder",
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
