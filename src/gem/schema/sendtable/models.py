"""Data models and type parsing for Source 2 send tables.

The send-table parser turns Valve's flattened serializer protobuf into a tree
of ``Serializer`` and ``Field`` objects. Each field is assigned one of the
``FIELD_MODEL_*`` shapes so field-reader code can choose the right decoder path
when packet-entity deltas arrive.

Reference: manta/field.go, manta/field_type.go, manta/serializer.go
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from gem.schema.field_decoder import FieldDecoder, find_decoder, find_decoder_by_base_type

# Types whose serializer is embedded by pointer (fixed-table model).
_POINTER_TYPES: frozenset[str] = frozenset(
    [
        "PhysicsRagdollPose_t",
        "CBodyComponent",
        "CEntityIdentity",
        "CPhysicsComponent",
        "CRenderComponent",
        "CDOTAGamerules",
        "CDOTAGameManager",
        "CDOTASpectatorGraphManager",
        "CPlayerLocalData",
        "CPlayer_CameraServices",
        "CDOTAGameRules",
    ]
)

# Named array size constants from the engine.
_ITEM_COUNTS: dict[str, int] = {
    "MAX_ITEM_STOCKS": 8,
    "MAX_ABILITY_DRAFT_ABILITIES": 48,
}

# Field model constants. These numeric values intentionally match the reference
# parser's shape categories and are used by field_reader dispatch.
FIELD_MODEL_SIMPLE = 0
FIELD_MODEL_FIXED_ARRAY = 1
FIELD_MODEL_FIXED_TABLE = 2
FIELD_MODEL_VARIABLE_ARRAY = 3
FIELD_MODEL_VARIABLE_TABLE = 4

_FIELD_TYPE_RE = re.compile(r"([^<\[*]+)(<\s(.*)\s>)?(\*)?(\[([^\]]*)\])?")


@dataclass
class FieldType:
    """Parsed representation of a C++ field type string.

    Examples include scalar types such as ``uint32``, fixed arrays such as
    ``CHandle[24]``, pointer-like nested tables such as ``CBodyComponent*``,
    and generic vectors such as ``CUtlVector< int32 >``.
    """

    base_type: str
    generic_type: FieldType | None = None
    pointer: bool = False
    count: int = 0

    def __str__(self) -> str:
        """Render the normalized type string for diagnostics and tests."""
        s = self.base_type
        if self.generic_type:
            s += f"<{self.generic_type}>"
        if self.pointer:
            s += "*"
        if self.count:
            s += f"[{self.count}]"
        return s


def _parse_field_type(name: str) -> FieldType:
    """Parse a Source 2 field type string into structured type metadata."""
    m = _FIELD_TYPE_RE.match(name)
    if not m:
        raise ValueError(f"Cannot parse field type: {name!r}")

    base = m.group(1).strip()
    generic_str = m.group(3)
    pointer = m.group(4) == "*"
    count_str = m.group(6) or ""

    generic = _parse_field_type(generic_str) if generic_str else None

    if count_str in _ITEM_COUNTS:
        count = _ITEM_COUNTS[count_str]
    else:
        try:
            count = int(count_str) if count_str else 0
        except ValueError:
            # Unknown engine constants still need a stable bound so downstream
            # fixed-array traversal can proceed without special-casing.
            count = 1024

    return FieldType(base_type=base, generic_type=generic, pointer=pointer, count=count)


@dataclass
class Field:
    """One property of a serializer, including its type model and decoders.

    ``decoder`` is used for scalar and fixed-array values. ``base_decoder`` and
    ``child_decoder`` are used by nested-table and variable-array shapes where
    field paths encode either presence/length metadata or child values.
    """

    var_name: str
    var_type: str
    send_node: str
    serializer_name: str
    serializer_version: int
    encoder: str
    encode_flags: int | None
    bit_count: int | None
    low_value: float | None
    high_value: float | None
    parent_name: str = ""
    field_type: FieldType = field(default_factory=lambda: FieldType(""))
    serializer: Serializer | None = None
    model: int = FIELD_MODEL_SIMPLE
    decoder: FieldDecoder | None = None
    base_decoder: FieldDecoder | None = None
    child_decoder: FieldDecoder | None = None

    def set_model(self, model: int) -> None:
        """Assign the field model and wire up the appropriate decoders.

        Args:
            model: One of the FIELD_MODEL_* constants.

        Raises:
            ValueError: If the field shape is inconsistent with the requested
                model.
        """
        # Imported lazily to avoid an import cycle: field_decoder imports Field
        # only for type checking and decoder selection.
        from gem.schema.field_decoder import boolean_decoder, unsigned_decoder

        self.model = model
        if model in (FIELD_MODEL_SIMPLE, FIELD_MODEL_FIXED_ARRAY):
            self.decoder = find_decoder(self)
        elif model == FIELD_MODEL_FIXED_TABLE:
            self.base_decoder = boolean_decoder
        elif model == FIELD_MODEL_VARIABLE_ARRAY:
            if self.field_type.generic_type is None:
                raise ValueError(
                    f"variable-array field {self.var_name!r} has no generic type "
                    f"(var_type={self.var_type!r})"
                )
            self.base_decoder = unsigned_decoder
            generic_base = self.field_type.generic_type.base_type
            self.child_decoder = find_decoder_by_base_type(generic_base)
        elif model == FIELD_MODEL_VARIABLE_TABLE:
            self.base_decoder = unsigned_decoder
        else:
            raise ValueError(f"unknown field model {model} for {self.var_name!r}")

    def model_name(self) -> str:
        """Return a human-readable model name for debugging."""
        return {
            FIELD_MODEL_SIMPLE: "simple",
            FIELD_MODEL_FIXED_ARRAY: "fixed-array",
            FIELD_MODEL_FIXED_TABLE: "fixed-table",
            FIELD_MODEL_VARIABLE_ARRAY: "variable-array",
            FIELD_MODEL_VARIABLE_TABLE: "variable-table",
        }.get(self.model, "unknown")


@dataclass
class Serializer:
    """A named, versioned entity class schema with ordered fields."""

    name: str
    version: int
    fields: list[Field] = field(default_factory=list)

    def __repr__(self) -> str:
        """Return a compact representation for parser/debug output."""
        return f"Serializer({self.name!r}, v{self.version}, {len(self.fields)} fields)"
