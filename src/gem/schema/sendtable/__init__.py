"""Public send-table schema API.

The implementation is split into parser, model, and patch modules, but callers
should continue to import from ``gem.schema.sendtable``. ``__all__`` lists the
stable public surface. The underscore-prefixed names re-exported below
(``_parse_field_type``, ``_FIELD_PATCHES``, ``_FieldPatch``) are internal
helpers shared with sibling modules and tests — importable by name, but not part
of the public contract.
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
    _parse_field_type as _parse_field_type,
)
from gem.schema.sendtable.parser import parse_send_tables
from gem.schema.sendtable.patches import (
    _FIELD_PATCHES as _FIELD_PATCHES,
    _FieldPatch as _FieldPatch,
)

__all__ = [
    "FIELD_MODEL_FIXED_ARRAY",
    "FIELD_MODEL_FIXED_TABLE",
    "FIELD_MODEL_SIMPLE",
    "FIELD_MODEL_VARIABLE_ARRAY",
    "FIELD_MODEL_VARIABLE_TABLE",
    "Field",
    "FieldType",
    "Serializer",
    "parse_send_tables",
]
