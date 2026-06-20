"""CDemoSendTables parser and serializer tree builder.

This module converts the replay's nested flattened-serializer payload into the
runtime schema consumed by entity state reconstruction. It keeps protobuf
unpacking separate from field construction so validation errors can point at the
bad layer: outer payload, inner serializer payload, symbol lookup, or field
reference resolution.

Reference: manta/sendtable.go, manta/field.go
"""

from __future__ import annotations

# Proto imports: the descriptor dependency chain must be resolved first.
from google.protobuf import descriptor_pb2  # noqa: F401 - must load first
from google.protobuf.message import DecodeError

from gem.binary.reader import BitReader
from gem.proto import (
    network_connection_pb2,  # noqa: F401 - side-effect import
    networkbasetypes_pb2,  # noqa: F401
)
from gem.proto.demo_pb2 import CDemoSendTables
from gem.proto.netmessages_pb2 import (
    CSVCMsg_FlattenedSerializer,
    ProtoFlattenedSerializer_t,
    ProtoFlattenedSerializerField_t,
)
from gem.schema.sendtable.models import (
    _POINTER_TYPES,
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
from gem.schema.sendtable.patches import _FIELD_PATCHES, _FieldPatch


def _parse_flattened_serializer(data: bytes) -> CSVCMsg_FlattenedSerializer:
    """Parse the nested flattened serializer from a ``CDemoSendTables`` payload."""
    outer = CDemoSendTables()
    try:
        outer.ParseFromString(data)
    except DecodeError as exc:
        raise ValueError("invalid CDemoSendTables payload") from exc

    r = BitReader(outer.data)
    size = r.read_varuint32()
    inner_payload = r.read_bytes(size)

    msg = CSVCMsg_FlattenedSerializer()
    try:
        msg.ParseFromString(inner_payload)
    except DecodeError as exc:
        raise ValueError("invalid CSVCMsg_FlattenedSerializer payload") from exc

    return msg


def _symbol(symbols: list[str], idx: int | None, context: str) -> str:
    """Resolve a symbol-table index and include context in validation errors."""
    if idx is None:
        return ""
    if idx < 0 or idx >= len(symbols):
        raise ValueError(f"invalid symbol index {idx} for {context}; symbols={len(symbols)}")
    return symbols[idx]


def _optional_symbol(
    proto: ProtoFlattenedSerializerField_t,
    field_name: str,
    symbols: list[str],
    context: str,
) -> str:
    """Resolve an optional protobuf symbol field to a string."""
    if not proto.HasField(field_name):
        return ""
    return _symbol(symbols, getattr(proto, field_name), context)


def _build_field(
    field_proto: ProtoFlattenedSerializerField_t,
    symbols: list[str],
    owner_name: str,
    game_build: int,
) -> Field:
    """Build a ``Field`` from protobuf metadata before linking decoders."""
    send_node = _optional_symbol(field_proto, "send_node_sym", symbols, f"{owner_name}.send_node")
    if send_node == "(root)":
        send_node = ""

    f = Field(
        var_name=_optional_symbol(field_proto, "var_name_sym", symbols, f"{owner_name}.var_name"),
        var_type=_optional_symbol(field_proto, "var_type_sym", symbols, f"{owner_name}.var_type"),
        send_node=send_node,
        serializer_name=_optional_symbol(
            field_proto,
            "field_serializer_name_sym",
            symbols,
            f"{owner_name}.field_serializer_name",
        ),
        serializer_version=field_proto.field_serializer_version,
        encoder=_optional_symbol(
            field_proto,
            "var_encoder_sym",
            symbols,
            f"{owner_name}.var_encoder",
        ),
        encode_flags=field_proto.encode_flags if field_proto.HasField("encode_flags") else None,
        bit_count=field_proto.bit_count if field_proto.HasField("bit_count") else None,
        low_value=field_proto.low_value if field_proto.HasField("low_value") else None,
        high_value=field_proto.high_value if field_proto.HasField("high_value") else None,
    )

    if game_build <= 990:
        f.parent_name = owner_name

    return f


def _select_field_model(f: Field) -> int:
    """Select the field-reader model from parsed type and serializer metadata."""
    if f.serializer is not None:
        if f.field_type.pointer or f.field_type.base_type in _POINTER_TYPES:
            return FIELD_MODEL_FIXED_TABLE
        return FIELD_MODEL_VARIABLE_TABLE
    if f.field_type.count > 0 and f.field_type.base_type != "char":
        return FIELD_MODEL_FIXED_ARRAY
    if f.field_type.base_type in ("CUtlVector", "CNetworkUtlVectorBase"):
        return FIELD_MODEL_VARIABLE_ARRAY
    return FIELD_MODEL_SIMPLE


def _resolve_serializer_reference(
    serializer_name: str,
    serializer_version: int,
    *,
    owner_name: str,
    field_name: str,
    serializers_by_name: dict[str, Serializer],
    serializers_by_key: dict[tuple[str, int], Serializer],
) -> Serializer:
    """Resolve a nested serializer reference, preferring an exact version match."""
    exact_match = serializers_by_key.get((serializer_name, serializer_version))
    if exact_match is not None:
        return exact_match

    fallback = serializers_by_name.get(serializer_name)
    if fallback is not None:
        return fallback

    raise ValueError(
        f"unresolved serializer reference {serializer_name!r} "
        f"(version {serializer_version}) for {owner_name}.{field_name}"
    )


def _get_or_build_field(
    idx: int,
    *,
    owner_name: str,
    msg: CSVCMsg_FlattenedSerializer,
    symbols: list[str],
    serializers_by_name: dict[str, Serializer],
    serializers_by_key: dict[tuple[str, int], Serializer],
    field_type_cache: dict[str, FieldType],
    field_cache: dict[int, Field],
    active_patches: list[_FieldPatch],
    game_build: int,
) -> Field:
    """Return a cached field object or construct and validate it.

    Flattened serializer fields can be referenced by more than one serializer,
    so this cache preserves object identity and avoids repeating decoder setup.
    """
    if idx in field_cache:
        return field_cache[idx]
    if idx < 0 or idx >= len(msg.fields):
        raise ValueError(f"invalid field index {idx} for serializer {owner_name!r}")

    f = _build_field(msg.fields[idx], symbols, owner_name, game_build)

    if f.var_type not in field_type_cache:
        field_type_cache[f.var_type] = _parse_field_type(f.var_type)
    f.field_type = field_type_cache[f.var_type]

    if f.serializer_name:
        f.serializer = _resolve_serializer_reference(
            f.serializer_name,
            f.serializer_version,
            owner_name=owner_name,
            field_name=f.var_name,
            serializers_by_name=serializers_by_name,
            serializers_by_key=serializers_by_key,
        )

    for patch in active_patches:
        patch.patch(f)

    f.set_model(_select_field_model(f))
    field_cache[idx] = f
    return f


def parse_send_tables(data: bytes, game_build: int = 0) -> dict[str, Serializer]:
    """Parse a CDemoSendTables payload into a serializer dictionary.

    Args:
        data: Raw bytes from a ``CDemoSendTables`` outer message.
        game_build: Server build number (from ``CSVCMsg_ServerInfo``).
            Used to select build-range field patches. Pass 0 to apply only
            the always-on patches.

    Returns:
        Mapping of serializer name to Serializer, containing every entity
        class schema defined in this replay.
    """
    msg = _parse_flattened_serializer(data)
    symbols = list(msg.symbols)

    active_patches = [p for p in _FIELD_PATCHES if p.should_apply(game_build)]
    field_type_cache: dict[str, FieldType] = {}
    field_cache: dict[int, Field] = {}
    serializers_by_name: dict[str, Serializer] = {}
    serializers_by_key: dict[tuple[str, int], Serializer] = {}
    serializer_entries: list[tuple[str, ProtoFlattenedSerializer_t, Serializer]] = []

    # First allocate every serializer instance so fields can resolve references
    # to later declarations while still honoring duplicate name/version pairs.
    for s_proto in msg.serializers:
        s_name = _symbol(symbols, s_proto.serializer_name_sym, "serializer_name")
        serializer = Serializer(name=s_name, version=s_proto.serializer_version)
        serializers_by_name[s_name] = serializer
        serializers_by_key[(s_name, serializer.version)] = serializer
        serializer_entries.append((s_name, s_proto, serializer))

    # Then populate fields once all serializer names are available.
    for s_name, s_proto, serializer in serializer_entries:
        for idx in s_proto.fields_index:
            field_obj = _get_or_build_field(
                idx,
                owner_name=s_name,
                msg=msg,
                symbols=symbols,
                serializers_by_name=serializers_by_name,
                serializers_by_key=serializers_by_key,
                field_type_cache=field_type_cache,
                field_cache=field_cache,
                active_patches=active_patches,
                game_build=game_build,
            )
            serializer.fields.append(field_obj)

    return serializers_by_name
