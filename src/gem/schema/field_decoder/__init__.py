"""Public field-value decoder API.

Implementation modules use domain-specific names to avoid confusion with
``binary.reader`` and ``schema.field_reader``; callers import from
``gem.schema.field_decoder``. ``__all__`` lists the stable public surface: the
named scalar/composite decoders, the ``find_decoder`` lookups, and the
``FieldDecoder``/``QuantizedFloatDecoder`` types. Internal helpers (decoder
factories, quantized-float flag constants, dispatch tables, and the
``_FieldLike`` protocols) stay in their defining modules.
"""

from gem.schema.field_decoder.contracts import FieldDecoder
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
from gem.schema.field_decoder.type_resolver import find_decoder, find_decoder_by_base_type

__all__ = [
    "FieldDecoder",
    "QuantizedFloatDecoder",
    "binary_block_decoder",
    "boolean_decoder",
    "component_decoder",
    "default_decoder",
    "find_decoder",
    "find_decoder_by_base_type",
    "fixed8_decoder",
    "fixed8_signed_decoder",
    "fixed64_decoder",
    "float_coord_decoder",
    "hsequence_decoder",
    "noscale_decoder",
    "rune_time_decoder",
    "signed64_decoder",
    "signed_decoder",
    "simulation_time_decoder",
    "string_decoder",
    "unsigned64_decoder",
    "unsigned_decoder",
]
