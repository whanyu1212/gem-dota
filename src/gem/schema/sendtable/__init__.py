"""Public send-table schema API.

The implementation is split into ``parser``, ``models``, and ``patches``
modules; callers import from ``gem.schema.sendtable``. ``__all__`` lists the
stable public surface. Internal helpers stay in their defining modules.
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
)
from gem.schema.sendtable.parser import parse_send_tables

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
