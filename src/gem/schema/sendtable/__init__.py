"""Public send-table schema API.

The implementation is split into parser, model, and patch modules, but callers
should continue to import from ``gem.schema.sendtable``. This module re-exports
the stable symbols used by parser, entity state, tests, and documentation.
"""

from gem.schema.sendtable.models import (
    FIELD_MODEL_FIXED_ARRAY,
    FIELD_MODEL_FIXED_TABLE,
    FIELD_MODEL_SIMPLE,
    FIELD_MODEL_VARIABLE_ARRAY,
    FIELD_MODEL_VARIABLE_TABLE,
    Field,
    FieldType,
    Serializer,
    _parse_field_type,
)
from gem.schema.sendtable.parser import parse_send_tables
from gem.schema.sendtable.patches import _FIELD_PATCHES, _FieldPatch

__all__ = [
    "FIELD_MODEL_FIXED_ARRAY",
    "FIELD_MODEL_FIXED_TABLE",
    "FIELD_MODEL_SIMPLE",
    "FIELD_MODEL_VARIABLE_ARRAY",
    "FIELD_MODEL_VARIABLE_TABLE",
    "Field",
    "FieldType",
    "Serializer",
    "_FIELD_PATCHES",
    "_FieldPatch",
    "_parse_field_type",
    "parse_send_tables",
]
