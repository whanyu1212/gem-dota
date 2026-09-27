"""Give synthetic test entities real field state.

Tests describe entity values by field name, as ``Entity.get()`` reads them:
``"m_iHealth"``, ``"m_pGameRules.m_nHeroPickState"``, ``"m_hItems.0003"``, or
``"m_vecPlayerTeamData.0003.m_iKills"``. ``set_fields`` adds any missing names to
the entity's serializer, then writes the values into its ``FieldState``, so reads
go through the same schema resolution as a real replay.

Naming rules when a field is added:

- ``a`` is a simple field.
- ``a.b`` makes ``a`` a fixed table holding ``b``.
- ``a.0003`` makes ``a`` a fixed array (element 3).
- ``a.0003.b`` makes ``a`` a variable table whose rows hold ``b``.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from gem.schema.field_path.models import CompactFieldPath
from gem.schema.sendtable import (
    FIELD_MODEL_FIXED_ARRAY,
    FIELD_MODEL_FIXED_TABLE,
    FIELD_MODEL_SIMPLE,
    FIELD_MODEL_VARIABLE_TABLE,
    Field,
    Serializer,
)
from gem.state.entities import Entity


def set_fields(entity: Entity, fields: Mapping[str, Any]) -> None:
    """Write *fields* (name → value) into *entity*, adding unknown names first.

    A value of ``None`` clears the field, as if it had never been sent.
    """
    for name, value in fields.items():
        entity._field_state._set_compact(_ensure_path(_serializer_of(entity), name), value)


def clear_fields(entity: Entity) -> None:
    """Clear every stored field value, keeping the entity's serializer."""
    set_fields(entity, dict.fromkeys(entity.to_map()))


def _serializer_of(entity: Entity) -> Serializer:
    serializer = getattr(entity.cls, "serializer", None)
    if serializer is None:
        serializer = Serializer(name=getattr(entity.cls, "name", "CTest"), version=0)
        entity.cls.serializer = serializer
    return serializer


def _ensure_path(serializer: Serializer, name: str) -> CompactFieldPath:
    path = serializer._resolve_field(name).path
    if path is None:
        _add_field(serializer, name.split("."), name)
        # The serializer caches failed lookups, so forget them.
        serializer._resolved_fields.clear()
        serializer._resolved_plans.clear()
        path = serializer._resolve_field(name).path
        assert path is not None, name
    return path


def _add_field(serializer: Serializer, parts: list[str], full_name: str) -> None:
    head, rest = parts[0], parts[1:]
    if not rest:
        model = FIELD_MODEL_SIMPLE
    elif not _is_index(rest[0]):
        model = FIELD_MODEL_FIXED_TABLE
    elif len(rest) == 1:
        model = FIELD_MODEL_FIXED_ARRAY
    else:
        model = FIELD_MODEL_VARIABLE_TABLE

    field = next((f for f in serializer.fields if f.var_name == head), None)
    if field is None:
        field = Field(
            var_name=head,
            var_type="",
            send_node="",
            serializer_name="",
            serializer_version=0,
            encoder="",
            encode_flags=None,
            bit_count=None,
            low_value=None,
            high_value=None,
        )
        field.model = model
        if model in (FIELD_MODEL_FIXED_TABLE, FIELD_MODEL_VARIABLE_TABLE):
            field.serializer = Serializer(name=f"{serializer.name}.{head}", version=0)
        serializer.fields.append(field)
    elif field.model != model:
        raise ValueError(f"{full_name!r} conflicts with the existing field {head!r}")

    if model == FIELD_MODEL_FIXED_TABLE:
        assert field.serializer is not None
        _add_field(field.serializer, rest, full_name)
    elif model == FIELD_MODEL_VARIABLE_TABLE:
        assert field.serializer is not None
        _add_field(field.serializer, rest[1:], full_name)


def _is_index(part: str) -> bool:
    return len(part) == 4 and part.isdigit()
