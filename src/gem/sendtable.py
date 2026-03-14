"""Send table parser for Dota 2 Source 2 replays.

Parses the ``CDemoSendTables`` outer message to build the full serializer
tree: every entity class, its fields, their types, and the decoder wired
to each field.

The serializer tree is the "schema" of the replay — it describes every
property of every entity class that the server can transmit.  It must be
parsed before any entity delta packets can be decoded.

Reference: manta/sendtable.go, manta/field.go, manta/field_type.go,
           manta/serializer.go, manta/field_patch.go
"""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Proto imports (order matters — dependency chain must be resolved first)
# ---------------------------------------------------------------------------
from google.protobuf import descriptor_pb2  # noqa: F401 — must load first

from gem.field_decoder import FieldDecoder, find_decoder, find_decoder_by_base_type
from gem.proto.dota2 import (
    network_connection_pb2,  # noqa: F401 — side-effect import
    networkbasetypes_pb2,  # noqa: F401
)
from gem.proto.dota2.demo_pb2 import CDemoSendTables
from gem.proto.dota2.netmessages_pb2 import CSVCMsg_FlattenedSerializer

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Types whose serializer is embedded by pointer (fixed-table model)
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

# Named array size constants from the engine
_ITEM_COUNTS: dict[str, int] = {
    "MAX_ITEM_STOCKS": 8,
    "MAX_ABILITY_DRAFT_ABILITIES": 48,
}

# Field model constants
FIELD_MODEL_SIMPLE = 0
FIELD_MODEL_FIXED_ARRAY = 1
FIELD_MODEL_FIXED_TABLE = 2
FIELD_MODEL_VARIABLE_ARRAY = 3
FIELD_MODEL_VARIABLE_TABLE = 4

# ---------------------------------------------------------------------------
# FieldType
# ---------------------------------------------------------------------------

_FIELD_TYPE_RE = re.compile(r"([^<\[*]+)(<\s(.*)\s>)?(\*)?(\[([^\]]*)\])?")


@dataclass
class FieldType:
    """Parsed representation of a C++ field type string.

    Examples::

        "uint32"               → base_type="uint32"
        "CUtlVector< int32 >"  → base_type="CUtlVector", generic_type=FieldType("int32")
        "CHandle[24]"          → base_type="CHandle", count=24
        "CBodyComponent*"      → base_type="CBodyComponent", pointer=True

    Attributes:
        base_type: The root type name without generics, pointer, or array.
        generic_type: The inner type for generic containers, or None.
        pointer: True if the field is a pointer type.
        count: Array element count (0 = not an array).
    """

    base_type: str
    generic_type: FieldType | None = None
    pointer: bool = False
    count: int = 0

    def __str__(self) -> str:
        s = self.base_type
        if self.generic_type:
            s += f"<{self.generic_type}>"
        if self.pointer:
            s += "*"
        if self.count:
            s += f"[{self.count}]"
        return s


def _parse_field_type(name: str) -> FieldType:
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
            count = 1024  # unknown constant → large bound

    return FieldType(base_type=base, generic_type=generic, pointer=pointer, count=count)


# ---------------------------------------------------------------------------
# Field
# ---------------------------------------------------------------------------


@dataclass
class Field:
    """One property of a serializer, with its type and decoder.

    Attributes:
        var_name: Property name (e.g. ``"m_iHealth"``).
        var_type: Raw type string from the send table.
        send_node: Network send node path (empty string for root).
        serializer_name: Name of the associated sub-serializer, if any.
        serializer_version: Version of the associated sub-serializer.
        encoder: Encoder hint (e.g. ``"coord"``, ``"simtime"``).
        encode_flags: QFD encode flags bitmask.
        bit_count: QFD / angle bit width.
        low_value: QFD lower bound.
        high_value: QFD upper bound.
        parent_name: Serializer that owns this field (set for build ≤ 990).
        field_type: Parsed FieldType.
        serializer: Resolved sub-serializer for nested types, or None.
        model: One of the FIELD_MODEL_* constants.
        decoder: Callable for simple / fixed-array fields.
        base_decoder: Callable for the length prefix of array / table fields.
        child_decoder: Callable for variable-array elements.
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
        """
        from gem.field_decoder import boolean_decoder, unsigned_decoder

        self.model = model
        if model in (FIELD_MODEL_SIMPLE, FIELD_MODEL_FIXED_ARRAY):
            self.decoder = find_decoder(self)
        elif model == FIELD_MODEL_FIXED_TABLE:
            self.base_decoder = boolean_decoder
        elif model == FIELD_MODEL_VARIABLE_ARRAY:
            self.base_decoder = unsigned_decoder
            generic_base = (
                self.field_type.generic_type.base_type if self.field_type.generic_type else ""
            )
            self.child_decoder = find_decoder_by_base_type(generic_base)
        elif model == FIELD_MODEL_VARIABLE_TABLE:
            self.base_decoder = unsigned_decoder

    def model_name(self) -> str:
        """Return a human-readable model name for debugging.

        Returns:
            One of ``"simple"``, ``"fixed-array"``, ``"fixed-table"``,
            ``"variable-array"``, ``"variable-table"``.
        """
        return {
            FIELD_MODEL_SIMPLE: "simple",
            FIELD_MODEL_FIXED_ARRAY: "fixed-array",
            FIELD_MODEL_FIXED_TABLE: "fixed-table",
            FIELD_MODEL_VARIABLE_ARRAY: "variable-array",
            FIELD_MODEL_VARIABLE_TABLE: "variable-table",
        }.get(self.model, "unknown")


# ---------------------------------------------------------------------------
# Serializer
# ---------------------------------------------------------------------------


@dataclass
class Serializer:
    """A named, versioned entity class schema with an ordered list of fields.

    Attributes:
        name: Entity class name (e.g. ``"CDOTA_Unit_Hero_Axe"``).
        version: Schema version integer.
        fields: Ordered list of Field objects.
    """

    name: str
    version: int
    fields: list[Field] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"Serializer({self.name!r}, v{self.version}, {len(self.fields)} fields)"


# ---------------------------------------------------------------------------
# Field patches (build-range overrides matching manta/field_patch.go)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _FieldPatch:
    min_build: int
    max_build: int
    patch: Callable[[Field], None]

    def should_apply(self, build: int) -> bool:
        if self.min_build == 0 and self.max_build == 0:
            return True
        return self.min_build <= build <= self.max_build


def _make_patches() -> list[_FieldPatch]:
    def patch_pre991(f: Field) -> None:
        if f.var_name in {
            "angExtraLocalAngles",
            "angLocalAngles",
            "m_angInitialAngles",
            "m_angRotation",
            "m_ragAngles",
            "m_vLightDirection",
        }:
            f.encoder = (
                "qangle_pitch_yaw"
                if f.parent_name == "CBodyComponentBaseAnimatingOverlay"
                else "QAngle"
            )
        elif f.var_name in {
            "dirPrimary",
            "localSound",
            "m_flElasticity",
            "m_location",
            "m_poolOrigin",
            "m_ragPos",
            "m_vecEndPos",
            "m_vecLadderDir",
            "m_vecPlayerMountPositionBottom",
            "m_vecPlayerMountPositionTop",
            "m_viewtarget",
            "m_WorldMaxs",
            "m_WorldMins",
            "origin",
            "vecLocalOrigin",
        }:
            f.encoder = "coord"
        elif f.var_name == "m_vecLadderNormal":
            f.encoder = "normal"

    def patch_pre955(f: Field) -> None:
        if f.var_name in ("m_flMana", "m_flMaxMana"):
            f.low_value = None
            f.high_value = 8192.0

    def patch_1016_1027(f: Field) -> None:
        if f.var_name in {
            "m_bItemWhiteList",
            "m_bWorldTreeState",
            "m_iPlayerIDsInControl",
            "m_iPlayerSteamID",
            "m_ulTeamBannerLogo",
            "m_ulTeamBaseLogo",
            "m_ulTeamLogo",
        }:
            f.encoder = "fixed64"

    def patch_simtime(f: Field) -> None:
        if f.var_name in ("m_flSimulationTime", "m_flAnimTime"):
            f.encoder = "simtime"
        elif f.var_name == "m_flRuneTime":
            f.encoder = "runetime"

    return [
        _FieldPatch(0, 990, patch_pre991),
        _FieldPatch(0, 954, patch_pre955),
        _FieldPatch(1016, 1027, patch_1016_1027),
        _FieldPatch(0, 0, patch_simtime),
    ]


_FIELD_PATCHES: list[_FieldPatch] = _make_patches()


# ---------------------------------------------------------------------------
# SendTable parser
# ---------------------------------------------------------------------------


def parse_send_tables(data: bytes, game_build: int = 0) -> dict[str, Serializer]:
    """Parse a CDemoSendTables payload into a serializer dictionary.

    The payload is a varuint32 length prefix followed by a serialized
    ``CSVCMsg_FlattenedSerializer`` protobuf message.

    Args:
        data: Raw bytes from a ``CDemoSendTables`` outer message.
        game_build: Server build number (from ``CSVCMsg_ServerInfo``).
            Used to select build-range field patches.  Pass 0 to apply
            only the always-on patches.

    Returns:
        Mapping of serializer name → Serializer, containing every entity
        class schema defined in this replay.
    """
    # The outer payload is a CDemoSendTables protobuf whose .data field
    # contains a varuint32-prefixed CSVCMsg_FlattenedSerializer.
    outer = CDemoSendTables()
    outer.ParseFromString(data)
    inner = outer.data

    # Strip the varuint32 length prefix from the inner buffer
    pos = 0
    size = 0
    shift = 0
    while True:
        b = inner[pos]
        pos += 1
        size |= (b & 0x7F) << shift
        if not (b & 0x80):
            break
        shift += 7

    msg = CSVCMsg_FlattenedSerializer()
    msg.ParseFromString(inner[pos : pos + size])

    symbols = list(msg.symbols)

    def sym(idx: int | None) -> str:
        return symbols[idx] if idx is not None else ""

    # Select applicable patches
    active_patches = [p for p in _FIELD_PATCHES if p.should_apply(game_build)]

    # Build field type cache (shared across fields with the same type string)
    field_type_cache: dict[str, FieldType] = {}

    # Build field cache (shared across serializers that reference the same field index)
    field_cache: dict[int, Field] = {}

    serializers: dict[str, Serializer] = {}

    for s_proto in msg.serializers:
        s_name = symbols[s_proto.serializer_name_sym]
        s_version = s_proto.serializer_version
        serializer = Serializer(name=s_name, version=s_version)

        for idx in s_proto.fields_index:
            if idx not in field_cache:
                fp = msg.fields[idx]

                encode_flags = fp.encode_flags if fp.HasField("encode_flags") else None
                bit_count = fp.bit_count if fp.HasField("bit_count") else None
                low_value = fp.low_value if fp.HasField("low_value") else None
                high_value = fp.high_value if fp.HasField("high_value") else None

                send_node = sym(fp.send_node_sym if fp.HasField("send_node_sym") else None)
                if send_node == "(root)":
                    send_node = ""

                f = Field(
                    var_name=sym(fp.var_name_sym if fp.HasField("var_name_sym") else None),
                    var_type=sym(fp.var_type_sym if fp.HasField("var_type_sym") else None),
                    send_node=send_node,
                    serializer_name=sym(
                        fp.field_serializer_name_sym
                        if fp.HasField("field_serializer_name_sym")
                        else None
                    ),
                    serializer_version=fp.field_serializer_version,
                    encoder=sym(fp.var_encoder_sym if fp.HasField("var_encoder_sym") else None),
                    encode_flags=encode_flags,
                    bit_count=bit_count,
                    low_value=low_value,
                    high_value=high_value,
                )

                # Patch parent name for old builds
                if game_build <= 990:
                    f.parent_name = s_name

                # Parse and cache the field type
                if f.var_type not in field_type_cache:
                    field_type_cache[f.var_type] = _parse_field_type(f.var_type)
                f.field_type = field_type_cache[f.var_type]

                # Resolve sub-serializer
                if f.serializer_name:
                    f.serializer = serializers.get(f.serializer_name)

                # Apply build-range patches before determining the model
                for patch in active_patches:
                    patch.patch(f)

                # Determine field model
                if f.serializer is not None:
                    if f.field_type.pointer or f.field_type.base_type in _POINTER_TYPES:
                        f.set_model(FIELD_MODEL_FIXED_TABLE)
                    else:
                        f.set_model(FIELD_MODEL_VARIABLE_TABLE)
                elif f.field_type.count > 0 and f.field_type.base_type != "char":
                    f.set_model(FIELD_MODEL_FIXED_ARRAY)
                elif f.field_type.base_type in ("CUtlVector", "CNetworkUtlVectorBase"):
                    f.set_model(FIELD_MODEL_VARIABLE_ARRAY)
                else:
                    f.set_model(FIELD_MODEL_SIMPLE)

                field_cache[idx] = f

            serializer.fields.append(field_cache[idx])

        serializers[s_name] = serializer

    return serializers
