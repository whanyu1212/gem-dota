"""Entity lifecycle management for Dota 2 Source 2 replays.

Handles ``CSVCMsg_PacketEntities``, ``CDemoClassInfo``, and
``CSVCMsg_ServerInfo`` to maintain a live table of game entities.
Each entity is an instance of a serializer class; its field values live in a
``FieldState`` tree and are read by dotted field name, directly or with typed
accessors.

References:
    dotabuff/manta entity.go, class.go (pinned revision in CLAUDE.md)
    skadistats/clarity processor/entities/Entities.java (pinned revision in
    CLAUDE.md): per-entity apply-then-notify order within a packet
"""

from __future__ import annotations

import enum
import math
import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Any

from gem.binary.reader import BitReader
from gem.schema.field_path.models import CompactFieldPath
from gem.schema.field_reader import read_fields
from gem.schema.field_state import FieldState
from gem.schema.sendtable import (
    FIELD_MODEL_FIXED_ARRAY,
    FIELD_MODEL_FIXED_TABLE,
    FIELD_MODEL_SIMPLE,
    FIELD_MODEL_VARIABLE_ARRAY,
    FIELD_MODEL_VARIABLE_TABLE,
    Serializer,
)
from gem.schema.sendtable.models import FieldAccessPlan, ResolvedField
from gem.state.string_table import StringTables

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_INDEX_BITS: int = 14
_HANDLE_MASK: int = (1 << _INDEX_BITS) - 1
_GAME_BUILD_RE = re.compile(r"/dota_v(\d+)/")


def game_build_from_game_dir(game_dir: str) -> int:
    """Return the game build number from a ``CSVCMsg_ServerInfo.game_dir`` path.

    The build is the number in the ``/dota_v<build>/`` path component, as in
    Manta's ``onCSVCMsg_ServerInfo`` (dotabuff/manta ``class.go``).

    Args:
        game_dir: The server's game directory, e.g.
            ``"/opt/srcds/dota/dota_v6808/dota"``.

    Returns:
        The build number, or 0 if ``game_dir`` doesn't contain one.
    """
    m = _GAME_BUILD_RE.search(game_dir)
    return int(m.group(1)) if m else 0


# Current replays (build 6792 on) name the field ``m_nameStringTableIndex``; older
# ones spell it ``m_nameStringableIndex``.
_ENTITY_NAME_FIELDS = FieldAccessPlan(
    ("m_pEntity.m_nameStringTableIndex", "m_pEntity.m_nameStringableIndex")
)


# ---------------------------------------------------------------------------
# EntityOp
# ---------------------------------------------------------------------------


class EntityOp(enum.IntFlag):
    """Bitmask indicating what happened to an entity in a packet."""

    NONE = 0x00
    CREATED = 0x01
    UPDATED = 0x02
    DELETED = 0x04
    ENTERED = 0x08
    LEFT = 0x10

    # Convenience combinations
    CREATED_ENTERED = 0x01 | 0x08
    UPDATED_ENTERED = 0x02 | 0x08
    DELETED_LEFT = 0x04 | 0x10

    def has(self, other: EntityOp) -> bool:
        """Return True if this op overlaps any bit in *other*.

        Args:
            other: The flag to test for.

        Returns:
            True if any queried bit is set. Querying ``NONE`` returns False.
        """
        if isinstance(other, EntityOp):
            return bool(self._value_ & other._value_)
        return bool(self & other)


# ---------------------------------------------------------------------------
# ClassInfo
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class ClassInfo:
    """Mapping of a class ID to its name and Serializer.

    Attributes:
        class_id: Numeric class identifier from CDemoClassInfo.
        name: Network class name (e.g. ``"CDOTA_Unit_Hero_Axe"``).
        serializer: The associated Serializer schema, or None.
    """

    class_id: int
    name: str
    serializer: Serializer | None


# ---------------------------------------------------------------------------
# Entity
# ---------------------------------------------------------------------------


class Entity:
    """A live game entity with decoded field state.

    Field values live in a ``FieldState`` tree. ``get()`` and the typed getters
    turn a dotted field name into a path through the class's serializer, then
    read the tree.

    Attributes:
        index: Entity slot index.
        serial: Serial number for handle validation.
        cls: Class metadata (has .name, .class_id, .serializer).
        active: False while the entity is in the leave state.
    """

    __slots__ = (
        "index",
        "serial",
        "cls",
        "active",
        "_field_state",
        "_player_id_cache",
    )

    def __init__(self, index: int, serial: int, cls: Any) -> None:
        self.index = index
        self.serial = serial
        self.cls = cls
        self.active = True
        self._field_state = FieldState()
        self._player_id_cache: Any = None

    # ------------------------------------------------------------------
    # Field access
    # ------------------------------------------------------------------

    def get(self, name: str) -> Any:
        """Return the current value of *name*, or None if absent.

        Args:
            name: Dotted field name, e.g. ``"m_iHealth"``.

        Returns:
            The decoded value, or None. The name of a variable-length array or
            table (e.g. ``"m_vecPlayerTeamData"``) returns its current length.
        """
        # Resolve once per shared serializer, rather than once per entity.
        serializer = getattr(self.cls, "serializer", None)
        if serializer is None:
            return None
        resolved = serializer._resolve_field(name)
        if resolved.path is None:
            return None
        return self._field_state._get_compact(resolved.path)

    def _resolve_fields(self, plan: FieldAccessPlan) -> tuple[ResolvedField, ...]:
        """Resolve one reusable field plan for this entity's serializer."""
        serializer = self.cls.serializer
        if serializer is None:
            return plan.unresolved
        return serializer._resolve_plan(plan)

    def _get_resolved(self, field: ResolvedField) -> Any:
        """Read a pre-resolved field."""
        if field.path is None:
            return None
        return self._field_state._get_compact(field.path)

    def _get_int32_resolved(self, field: ResolvedField) -> int | None:
        if field.path is None:
            return None
        value = self._field_state._get_compact(field.path)
        return value if isinstance(value, int) else None

    def _get_uint32_resolved(self, field: ResolvedField) -> int | None:
        if field.path is None:
            return None
        value = self._field_state._get_compact(field.path)
        return (value & 0xFFFFFFFF) if isinstance(value, int) else None

    def _get_uint64_resolved(self, field: ResolvedField) -> int | None:
        if field.path is None:
            return None
        value = self._field_state._get_compact(field.path)
        return value if isinstance(value, int) else None

    def _get_float32_resolved(self, field: ResolvedField) -> float | None:
        if field.path is None:
            return None
        value = self._field_state._get_compact(field.path)
        return float(value) if isinstance(value, (int, float)) else None

    def _get_string_resolved(self, field: ResolvedField) -> str | None:
        if field.path is None:
            return None
        value = self._field_state._get_compact(field.path)
        return value if isinstance(value, str) else None

    def _get_bool_resolved(self, field: ResolvedField) -> bool | None:
        if field.path is None:
            return None
        value = self._field_state._get_compact(field.path)
        return bool(value) if isinstance(value, (bool, int)) else None

    def exists(self, name: str) -> bool:
        """Return True if *name* has a value in the entity state.

        Args:
            name: Field name to check.
        """
        return self.get(name) is not None

    def get_int32(self, name: str) -> int | None:
        """Return the value as int32, or None if absent/wrong type.

        Args:
            name: Field name.

        Returns:
            Integer value, or None if the field is absent or not an int.
        """
        v = self.get(name)
        return v if isinstance(v, int) else None

    def get_uint32(self, name: str) -> int | None:
        """Return the value as uint32 (low 32 bits), or None if absent.

        Accepts both int and uint64 values (truncating to 32 bits if needed).

        Args:
            name: Field name.

        Returns:
            Integer value masked to 32 bits, or None if absent.
        """
        v = self.get(name)
        return (v & 0xFFFFFFFF) if isinstance(v, int) else None

    def get_uint64(self, name: str) -> int | None:
        """Return the value as uint64, or None if absent.

        Args:
            name: Field name.

        Returns:
            Integer value, or None if absent.
        """
        v = self.get(name)
        return v if isinstance(v, int) else None

    def get_float32(self, name: str) -> float | None:
        """Return the value as float32, or None if absent.

        Args:
            name: Field name.

        Returns:
            Float value, or None if absent or not numeric.
        """
        v = self.get(name)
        return float(v) if isinstance(v, (int, float)) else None

    def get_string(self, name: str) -> str | None:
        """Return the value as str, or None if absent.

        Args:
            name: Field name.

        Returns:
            String value, or None if absent or not a string.
        """
        v = self.get(name)
        return v if isinstance(v, str) else None

    def get_bool(self, name: str) -> bool | None:
        """Return the value as bool, or None if absent.

        Args:
            name: Field name.

        Returns:
            Boolean value, or None if absent or not a bool/int.
        """
        v = self.get(name)
        return bool(v) if isinstance(v, (bool, int)) else None

    def to_map(self) -> dict[str, Any]:
        """Return every stored field value by name.

        Names are the ones ``get()`` accepts (dots between levels, four-digit
        array and table indexes). Like Manta's ``Entity.Map()``, only values are
        listed: a table's presence flag and an array's length are left out. Unlike
        Manta, fields that were never sent are left out rather than listed as None,
        and when a class declares a name twice only the first field (the one
        ``get()`` reads) is listed.

        Returns:
            Dict of field name → value.
        """
        values: dict[str, Any] = {}
        serializer = getattr(self.cls, "serializer", None)
        if serializer is not None:
            _collect_values(serializer, self._field_state, "", values)
        return values

    def get_class_name(self) -> str:
        """Return the entity class name."""
        return self.cls.name

    def get_class_id(self) -> int:
        """Return the entity class ID."""
        return self.cls.class_id

    def get_index(self) -> int:
        """Return the entity slot index."""
        return self.index

    def get_serial(self) -> int:
        """Return the entity serial number."""
        return self.serial

    def __repr__(self) -> str:
        return f"Entity({self.index}, {self.cls.name!r})"


def _slot(node: FieldState, index: int) -> Any:
    """Read one slot the way ``FieldState`` reads do (one spare slot required)."""
    state = node._state
    return state[index] if len(state) >= index + 2 else None


def _collect_values(
    serializer: Serializer, node: FieldState, prefix: str, out: dict[str, Any]
) -> None:
    """Add every stored value under *node* to *out*, named like ``Entity.get``.

    Mirrors Manta's ``serializer.getFieldPaths`` / ``field.getFieldPaths``. A few
    classes declare two fields with the same name (``DataTeamPlayer_t`` has two
    ``m_nPlayerID``); a name only reaches the first, so later ones are skipped.
    """
    seen: set[str] = set()
    for i, field in enumerate(serializer.fields):
        if field.var_name in seen:
            continue
        seen.add(field.var_name)
        name = prefix + field.var_name
        value = _slot(node, i)
        model = field.model
        if model == FIELD_MODEL_SIMPLE:
            if value is not None:
                out[name] = value
        elif not isinstance(value, FieldState):
            continue  # a presence flag or length with nothing stored below it
        elif model in (FIELD_MODEL_FIXED_ARRAY, FIELD_MODEL_VARIABLE_ARRAY):
            for k, element in enumerate(value._state):
                if element is not None and not isinstance(element, FieldState):
                    out[f"{name}.{k:04d}"] = element
        elif field.serializer is not None:
            if model == FIELD_MODEL_FIXED_TABLE:
                _collect_values(field.serializer, value, f"{name}.", out)
            elif model == FIELD_MODEL_VARIABLE_TABLE:
                for k, row in enumerate(value._state):
                    if isinstance(row, FieldState):
                        _collect_values(field.serializer, row, f"{name}.{k:04d}.", out)


# ---------------------------------------------------------------------------
# EntityTracker — handler registration and dispatch
# ---------------------------------------------------------------------------

EntityHandler = Callable[[Entity, EntityOp], None]


@dataclass(frozen=True, slots=True)
class _EntityHandlerRegistration:
    """One ordered catch-all or class-filtered entity handler registration."""

    handler: EntityHandler
    class_names: frozenset[str] = frozenset()
    class_prefixes: tuple[str, ...] = ()
    required_fields: tuple[str, ...] = ()
    changed_fields: tuple[str, ...] = ()

    def matches(self, cls: ClassInfo) -> bool:
        """Return whether this registration consumes *cls*."""
        if (
            (self.class_names or self.class_prefixes)
            and cls.name not in self.class_names
            and not cls.name.startswith(self.class_prefixes)
        ):
            return False
        serializer = cls.serializer
        return not self.required_fields or (
            serializer is not None
            and all(
                serializer._resolve_field(name).path is not None for name in self.required_fields
            )
        )

    def compile_field_handler(self, cls: ClassInfo) -> _FieldEntityHandler:
        serializer = cls.serializer
        changed_paths = None
        if self.changed_fields:
            changed_paths = (
                frozenset(
                    field.path
                    for field in (serializer._resolve_field(name) for name in self.changed_fields)
                    if field.path is not None
                )
                if serializer is not None
                else frozenset()
            )
        return _FieldEntityHandler(self.handler, changed_paths)


@dataclass(frozen=True, slots=True)
class _FieldEntityHandler:
    """Class-resolved handler with an optional update-path gate."""

    handler: EntityHandler
    changed_paths: frozenset[CompactFieldPath] | None = None

    def accepts(self, entity: Entity, op: EntityOp) -> bool:
        if self.changed_paths is None or op != EntityOp.UPDATED:
            return True
        updated_paths = entity._field_state._updated_paths
        # Direct synthetic dispatch has no decoder change signal, so preserve
        # observable callback behavior for tests and custom in-memory entities.
        return updated_paths is None or not self.changed_paths.isdisjoint(updated_paths)


class EntityTracker:
    """Manages ordered entity handler registration and class-aware dispatch.

    Attributes:
        _registrations: Ordered catch-all and filtered handler registrations.
        _handlers_by_class_id: Precompiled handlers for each known entity class.
    """

    def __init__(self) -> None:
        self._registrations: list[_EntityHandlerRegistration] = []
        self._classes_by_id: dict[int, ClassInfo] | None = None
        self._handlers_by_class_id: dict[int, tuple[EntityHandler, ...]] = {}
        self._ordered_handlers_by_class_id: dict[
            int, tuple[EntityHandler | _FieldEntityHandler, ...]
        ] = {}

    def on_entity(self, handler: EntityHandler) -> None:
        """Register a handler to be called on entity events.

        Args:
            handler: Callable ``(Entity, EntityOp) -> None``.
        """
        self._register(_EntityHandlerRegistration(handler=handler))

    def _on_entity_filtered(
        self,
        handler: EntityHandler,
        *,
        class_names: Iterable[str] = (),
        class_prefixes: Iterable[str] = (),
    ) -> None:
        """Register an internal handler for selected entity classes."""
        names = frozenset(class_names)
        prefixes = tuple(dict.fromkeys(class_prefixes))
        if not names and not prefixes:
            raise ValueError("filtered entity handlers require a class name or prefix")
        if any(not value for value in names) or any(not value for value in prefixes):
            raise ValueError("entity class names and prefixes must be non-empty")
        self._register(
            _EntityHandlerRegistration(
                handler=handler,
                class_names=names,
                class_prefixes=prefixes,
            )
        )

    def _on_entity_fields(
        self,
        handler: EntityHandler,
        *,
        required_fields: Iterable[str],
        changed_fields: Iterable[str] = (),
    ) -> None:
        """Register for matching schemas and relevant decoded field changes."""
        required = tuple(dict.fromkeys(required_fields))
        changed = tuple(dict.fromkeys(changed_fields))
        if not required:
            raise ValueError("schema-filtered entity handlers require a field")
        if any(not value for value in (*required, *changed)):
            raise ValueError("schema field names must be non-empty")
        self._register(
            _EntityHandlerRegistration(
                handler=handler,
                required_fields=required,
                changed_fields=changed,
            )
        )

    def _register(self, registration: _EntityHandlerRegistration) -> None:
        self._registrations.append(registration)
        if self._classes_by_id is None:
            return
        for class_id, cls in self._classes_by_id.items():
            if registration.matches(cls):
                if registration.required_fields or class_id in self._ordered_handlers_by_class_id:
                    self._compile_class_handlers(cls)
                else:
                    handlers = self._handlers_by_class_id[class_id]
                    self._handlers_by_class_id[class_id] = (*handlers, registration.handler)

    def _build_handlers(
        self, cls: ClassInfo
    ) -> tuple[tuple[EntityHandler, ...], tuple[EntityHandler | _FieldEntityHandler, ...] | None]:
        """Return *cls*'s plain handlers, and its gated handlers in registration order.

        The second tuple is None unless a matching registration gates on fields;
        dispatch then runs it instead of the plain tuple.
        """
        matching = [
            registration for registration in self._registrations if registration.matches(cls)
        ]
        ordinary = tuple(
            registration.handler for registration in matching if not registration.required_fields
        )
        if not any(registration.required_fields for registration in matching):
            return ordinary, None
        ordered = tuple(
            registration.compile_field_handler(cls)
            if registration.required_fields
            else registration.handler
            for registration in matching
        )
        return ordinary, ordered

    def _compile_class_handlers(self, cls: ClassInfo) -> None:
        """Compile one class, preserving registration order when gating is needed."""
        ordinary, ordered = self._build_handlers(cls)
        self._handlers_by_class_id[cls.class_id] = ordinary
        if ordered is None:
            self._ordered_handlers_by_class_id.pop(cls.class_id, None)
        else:
            self._ordered_handlers_by_class_id[cls.class_id] = ordered

    def _on_class_info(self, classes: Iterable[ClassInfo]) -> None:
        """Compile ordered handler tuples for the supplied entity classes."""
        class_list = list(classes)
        self._classes_by_id = {cls.class_id: cls for cls in class_list}
        self._handlers_by_class_id = {}
        self._ordered_handlers_by_class_id = {}
        for cls in class_list:
            self._compile_class_handlers(cls)

    def _dispatch(self, entity: Entity, op: EntityOp) -> None:
        """Invoke all registered handlers for the given entity event.

        Args:
            entity: The entity that changed.
            op: The EntityOp bitmask.
        """
        class_id = entity.cls.class_id
        ordered_handlers = self._ordered_handlers_by_class_id.get(class_id)
        if ordered_handlers is None:
            handlers = self._handlers_by_class_id.get(class_id)
            if handlers is None:
                # Only direct dispatch of a class the tracker hasn't compiled
                # (tests, custom in-memory entities) gets here; a real replay
                # compiles every class from CDemoClassInfo first.
                handlers, ordered_handlers = self._build_handlers(entity.cls)
            if ordered_handlers is None:
                for handler in handlers:
                    handler(entity, op)
                return
        for entry in ordered_handlers:
            if isinstance(entry, _FieldEntityHandler):
                if entry.accepts(entity, op):
                    entry.handler(entity, op)
            else:
                entry(entity, op)


# ---------------------------------------------------------------------------
# EntityManager — owns the entity table and baseline state
# ---------------------------------------------------------------------------


class EntityManager:
    """Manages entity lifecycle across a replay stream.

    Processes ``CSVCMsg_ServerInfo``, ``CDemoClassInfo``,
    ``CSVCMsg_CreateStringTable`` / ``CSVCMsg_UpdateStringTable`` side effects,
    and ``CSVCMsg_PacketEntities``.

    Attributes:
        entities: Sparse list indexed by entity slot (None = empty slot).
        classes_by_id: class_id → ClassInfo.
        classes_by_name: class_name → ClassInfo.
        class_baselines: class_id → baseline bytes.
        serializers: Output of ``parse_send_tables``.
        string_tables: StringTables container (shared with caller).
        game_build: Server build number extracted from ServerInfo.
        class_id_size: Number of bits used to encode class IDs.
    """

    def __init__(self, serializers: dict[str, Serializer], string_tables: StringTables) -> None:
        self.serializers = serializers
        self.string_tables = string_tables
        self.entities: list[Entity | None] = []
        self.classes_by_id: dict[int, ClassInfo] = {}
        self.classes_by_name: dict[str, ClassInfo] = {}
        self.class_baselines: dict[int, bytes] = {}
        self.game_build: int = 0
        self.class_id_size: int = 0
        self._class_info_ready: bool = False
        self._full_packets: int = 0
        self.tracker = EntityTracker()

    def on_entity(self, handler: EntityHandler) -> None:
        """Register an entity event handler.

        Args:
            handler: Callable ``(Entity, EntityOp) -> None``.
        """
        self.tracker.on_entity(handler)

    def _on_entity_filtered(
        self,
        handler: EntityHandler,
        *,
        class_names: Iterable[str] = (),
        class_prefixes: Iterable[str] = (),
    ) -> None:
        """Register an internal handler for selected entity classes."""
        self.tracker._on_entity_filtered(
            handler,
            class_names=class_names,
            class_prefixes=class_prefixes,
        )

    def _on_entity_fields(
        self,
        handler: EntityHandler,
        *,
        required_fields: Iterable[str],
        changed_fields: Iterable[str] = (),
    ) -> None:
        """Register an internal schema/change-path filtered handler."""
        self.tracker._on_entity_fields(
            handler,
            required_fields=required_fields,
            changed_fields=changed_fields,
        )

    # ------------------------------------------------------------------
    # Handlers
    # ------------------------------------------------------------------

    def on_server_info(self, msg: object) -> None:
        """Extract classIdSize and game build from CSVCMsg_ServerInfo.

        Args:
            msg: A ``CSVCMsg_ServerInfo`` protobuf message.
        """
        max_classes: int = msg.max_classes  # type: ignore[attr-defined]
        self.class_id_size = int(math.log2(max_classes)) + 1
        # Entity slot indices are drawn from the full Source 2 entity pool
        # (up to 2^14 = 16384 slots), not bounded by the number of class types.
        # Using max_classes here causes IndexError when a slot index > max_classes
        # is assigned in on_packet_entities.
        self.entities = [None] * (1 << 14)

        build = game_build_from_game_dir(msg.game_dir)  # type: ignore[attr-defined]
        if build:
            self.game_build = build

    def on_class_info(self, msg: object) -> None:
        """Build class maps from CDemoClassInfo.

        Args:
            msg: A ``CDemoClassInfo`` protobuf message.
        """
        for c in msg.classes:  # type: ignore[attr-defined]
            class_id: int = c.class_id
            net_name: str = c.network_name
            ser = self.serializers.get(net_name)
            ci = ClassInfo(class_id=class_id, name=net_name, serializer=ser)
            self.classes_by_id[class_id] = ci
            self.classes_by_name[net_name] = ci

        self.tracker._on_class_info(self.classes_by_id.values())
        self._class_info_ready = True
        self._update_baselines()

    def on_baseline_updated(self) -> None:
        """Call after instancebaseline string table is created or updated."""
        self._update_baselines()

    def on_packet_entities(self, msg: object) -> list[tuple[Entity, EntityOp]]:
        """Decode a CSVCMsg_PacketEntities message.

        Args:
            msg: A ``CSVCMsg_PacketEntities`` protobuf message.

        Returns:
            List of (Entity, EntityOp) tuples in the order they were processed.
        """
        results: list[tuple[Entity, EntityOp]] = []
        self._decode_packet_entities(msg, results)
        return results

    def _on_packet_entities(self, msg: object) -> None:
        """Decode packet entities without collecting unused operation tuples."""
        self._decode_packet_entities(msg, None)

    def _decode_packet_entities(
        self,
        msg: object,
        results: list[tuple[Entity, EntityOp]] | None,
    ) -> None:
        """Decode and dispatch packet entities into an optional result sink."""
        is_delta: bool = msg.legacy_is_delta  # type: ignore[attr-defined]
        updates: int = msg.updated_entries  # type: ignore[attr-defined]
        entity_data: bytes = msg.entity_data  # type: ignore[attr-defined]

        if not is_delta:
            if self._full_packets > 0:
                return
            self._full_packets += 1

        r = BitReader(entity_data)
        index = -1

        for _ in range(updates):
            index += r.read_ubit_var() + 1
            cmd = r.read_bits(2)

            if cmd & 0x01 == 0:
                if cmd & 0x02:
                    # Create entity
                    class_id = r.read_bits(self.class_id_size)
                    serial = r.read_bits(17)
                    r.read_varuint32()  # spawn-group handle (Clarity); unused here

                    ci = self.classes_by_id.get(class_id)
                    if ci is None:
                        raise RuntimeError(f"unknown class id {class_id}")

                    entity = Entity(index=index, serial=serial, cls=ci)
                    self.entities[index] = entity

                    # Apply baseline first, then delta. A missing baseline is an
                    # invariant violation: the instancebaseline string table must
                    # carry defaults for every class before any entity of that
                    # class is created. Manta panics here (entity.go: "unable to
                    # find new baseline"); surfacing it loudly prevents silently
                    # constructing an entity with default (None) field values.
                    baseline = self.class_baselines.get(class_id)
                    if baseline is None:
                        raise RuntimeError(
                            f"unable to find baseline for class id {class_id} "
                            f"({ci.name}) creating entity {index}"
                        )
                    if ci.serializer is not None:
                        read_fields(BitReader(baseline), ci.serializer, entity._field_state)
                        read_fields(r, ci.serializer, entity._field_state)

                    op = EntityOp.CREATED | EntityOp.ENTERED
                else:
                    # Update entity
                    _e = self.entities[index]
                    if _e is None:
                        raise RuntimeError(f"update on missing entity {index}")
                    entity = _e
                    op = EntityOp.UPDATED
                    if not entity.active:
                        entity.active = True
                        op |= EntityOp.ENTERED
                    if entity.cls.serializer is not None:
                        read_fields(r, entity.cls.serializer, entity._field_state)
            else:
                # Leave / delete
                _e = self.entities[index]
                if _e is None:
                    raise RuntimeError(f"leave on missing entity {index}")
                entity = _e
                # A LEAVE for an already-inactive entity is a stream-corruption
                # invariant violation (manta panics: "ordered to leave, already
                # inactive"). Surface it rather than silently re-dispatching LEFT.
                if not entity.active:
                    raise RuntimeError(
                        f"entity {index} ({entity.cls.name}) ordered to leave, already inactive"
                    )
                op = EntityOp.LEFT
                if cmd & 0x02:
                    op |= EntityOp.DELETED
                    self.entities[index] = None
                else:
                    entity.active = False

            self.tracker._dispatch(entity, op)
            if results is not None:
                results.append((entity, op))

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _update_baselines(self) -> None:
        if not self._class_info_ready:
            return
        table = self.string_tables.get_by_name("instancebaseline")
        if table is None:
            return
        for _idx, (key, value) in table.items.items():
            try:
                class_id = int(key)
            except (ValueError, AttributeError):
                continue
            self.class_baselines[class_id] = value

    # ------------------------------------------------------------------
    # Query helpers
    # ------------------------------------------------------------------

    def find(self, index: int) -> Entity | None:
        """Return the entity at the given slot index, or None.

        Args:
            index: Entity slot index.
        """
        if 0 <= index < len(self.entities):
            return self.entities[index]
        return None

    def find_by_handle(self, handle: int) -> Entity | None:
        """Return the entity for a Source 2 entity handle, or None.

        Args:
            handle: 32-bit entity handle (index in low 14 bits, serial in high bits).
        """
        idx = handle & _HANDLE_MASK
        serial = handle >> _INDEX_BITS
        entity = self.find(idx)
        if entity is not None and entity.serial == serial:
            return entity
        return None

    def filter(self, predicate: Any) -> list[Entity]:
        """Return all entities matching a predicate.

        Args:
            predicate: Callable ``(Entity) -> bool``.

        Returns:
            List of matching Entity objects.
        """
        return [e for e in self.entities if e is not None and predicate(e)]

    def find_by_class_name(self, class_name: str) -> Entity | None:
        """Return the first active entity whose class name matches, or None.

        Args:
            class_name: Entity class name, e.g. ``"CDOTAGamerulesProxy"``.
        """
        for e in self.entities:
            if e is not None and e.active and e.get_class_name() == class_name:
                return e
        return None

    def find_by_npc_name(self, npc_name: str) -> Entity | None:
        """Return the first active entity whose NPC name matches, or None.

        NPC names (e.g. ``"npc_dota_unit_warlock_golem"``) are stored in the
        ``EntityNames`` string table and referenced via
        ``m_pEntity.m_nameStringTableIndex`` (``m_nameStringableIndex`` in older
        replays) on each entity.

        Several units can share a name (every courier is ``npc_dota_courier``),
        so this returns whichever comes first. It is an O(N) scan over all
        entity slots, meant for occasional lookups.

        Args:
            npc_name: NPC name as it appears in the combat log (lowercase),
                e.g. ``"npc_dota_unit_warlock_golem"``.

        Returns:
            The first matching active entity, or ``None`` if not found.
        """
        names_table = self.string_tables.get_by_name("EntityNames")
        if names_table is None:
            return None
        for e in self.entities:
            if e is None or not e.active:
                continue
            idx = None
            for name_field in e._resolve_fields(_ENTITY_NAME_FIELDS):
                idx = e._get_int32_resolved(name_field)
                if idx is not None:
                    break
            if idx is None:
                continue
            item = names_table.items.get(idx)
            if item is None:
                continue
            key, _ = item
            if key.lower() == npc_name.lower():
                return e
        return None

    def all_active(self) -> list[Entity]:
        """Return all currently active entities."""
        return [e for e in self.entities if e is not None and e.active]
