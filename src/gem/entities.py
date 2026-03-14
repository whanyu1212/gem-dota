"""Entity lifecycle management for Dota 2 Source 2 replays.

Handles ``CSVCMsg_PacketEntities``, ``CDemoClassInfo``, and
``CSVCMsg_ServerInfo`` to maintain a live table of game entities.
Each entity is an instance of a serializer class; its field values are
stored in a flat dict keyed by field name and can be retrieved by name
or with typed accessors.

Reference: manta/entity.go, manta/field_reader.go, manta/field_state.go,
           manta/class.go
"""

from __future__ import annotations

import enum
import math
import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from gem.field_path import FieldPath
from gem.field_reader import read_fields
from gem.field_state import FieldState
from gem.reader import BitReader
from gem.sendtable import (
    FIELD_MODEL_FIXED_ARRAY,
    FIELD_MODEL_FIXED_TABLE,
    FIELD_MODEL_VARIABLE_ARRAY,
    FIELD_MODEL_VARIABLE_TABLE,
    Field,
    Serializer,
)
from gem.string_table import StringTables

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_INDEX_BITS: int = 14
_HANDLE_MASK: int = (1 << _INDEX_BITS) - 1
_GAME_BUILD_RE = re.compile(r"/dota_v(\d+)/")


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
        """Return True if this op includes *other*.

        Args:
            other: The flag to test for.

        Returns:
            True if the flag is set.
        """
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

    The entity state is stored in ``_state`` (a FieldState tree for decoded
    replay fields) and optionally in a plain dict overlay for direct key-value
    access. The ``get()`` method queries the flat ``_state`` dict first (which
    tests may set directly), then falls back to FieldState path resolution.

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
        "_state",
        "_fp_cache",
        "_fp_noop",
    )

    def __init__(self, index: int, serial: int, cls: Any) -> None:
        self.index = index
        self.serial = serial
        self.cls = cls
        self.active = True
        self._field_state = FieldState()
        # Flat dict for direct key-value access (tests may write here directly)
        self._state: dict[str, Any] = {}
        self._fp_cache: dict[str, FieldPath] = {}
        self._fp_noop: set[str] = set()

    # ------------------------------------------------------------------
    # Field access
    # ------------------------------------------------------------------

    def get(self, name: str) -> Any:
        """Return the current value of *name*, or None if absent.

        Checks the flat ``_state`` dict first, then resolves through the
        FieldState tree using the serializer's field schema.

        Args:
            name: Dotted field name, e.g. ``"m_iHealth"``.

        Returns:
            The decoded value, or None.
        """
        # Fast path: direct dict (set by tests or flat lookups)
        if name in self._state:
            return self._state[name]

        # Slow path: resolve through serializer field paths
        serializer = getattr(self.cls, "serializer", None)
        if serializer is None:
            return None
        if name in self._fp_noop:
            return None
        if name in self._fp_cache:
            return self._field_state.get(self._fp_cache[name])

        fp = _find_field_path(serializer, name)
        if fp is None:
            self._fp_noop.add(name)
            return None

        self._fp_cache[name] = fp
        return self._field_state.get(fp)

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
        """Return a snapshot of the flat _state dict.

        Returns:
            Dict of field name → value.
        """
        return dict(self._state)

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


# ---------------------------------------------------------------------------
# Field-path name resolver — mirrors manta/serializer.go + field.go
# ---------------------------------------------------------------------------


def _find_field_path(serializer: Serializer, name: str) -> FieldPath | None:
    fp = FieldPath()
    if _resolve_in_serializer(serializer, fp, name, 0):
        return fp
    return None


def _resolve_in_serializer(serializer: Serializer, fp: FieldPath, name: str, depth: int) -> bool:
    for i, f in enumerate(serializer.fields):
        if name == f.var_name:
            fp.path[depth] = i
            fp.last = depth
            return True
        if name.startswith(f.var_name + "."):
            fp.path[depth] = i
            remainder = name[len(f.var_name) + 1 :]
            return _resolve_in_field(f, fp, remainder, depth + 1)
    return False


def _resolve_in_field(f: Field, fp: FieldPath, name: str, depth: int) -> bool:
    model = f.model

    if model in (FIELD_MODEL_FIXED_ARRAY, FIELD_MODEL_VARIABLE_ARRAY):
        if len(name) == 4:
            try:
                fp.path[depth] = int(name)
                fp.last = depth
                return True
            except ValueError:
                return False
        return False

    if model == FIELD_MODEL_FIXED_TABLE:
        if f.serializer is not None:
            return _resolve_in_serializer(f.serializer, fp, name, depth)
        return False

    if model == FIELD_MODEL_VARIABLE_TABLE:
        if f.serializer is not None and len(name) >= 6:
            try:
                fp.path[depth] = int(name[:4])
            except ValueError:
                return False
            return _resolve_in_serializer(f.serializer, fp, name[5:], depth + 1)
        return False

    return False


# ---------------------------------------------------------------------------
# EntityTracker — handler registration and dispatch
# ---------------------------------------------------------------------------

EntityHandler = Callable[[Entity, EntityOp], None]


class EntityTracker:
    """Manages entity event handler registration and dispatch.

    Attributes:
        _handlers: List of registered EntityHandler callables.
    """

    def __init__(self) -> None:
        self._handlers: list[EntityHandler] = []

    def on_entity(self, handler: EntityHandler) -> None:
        """Register a handler to be called on entity events.

        Args:
            handler: Callable ``(Entity, EntityOp) -> None``.
        """
        self._handlers.append(handler)

    def _dispatch(self, entity: Entity, op: EntityOp) -> None:
        """Invoke all registered handlers for the given entity event.

        Args:
            entity: The entity that changed.
            op: The EntityOp bitmask.
        """
        for h in self._handlers:
            h(entity, op)


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

        game_dir: str = msg.game_dir  # type: ignore[attr-defined]
        m = _GAME_BUILD_RE.search(game_dir)
        if m:
            self.game_build = int(m.group(1))

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
        is_delta: bool = msg.legacy_is_delta  # type: ignore[attr-defined]
        updates: int = msg.updated_entries  # type: ignore[attr-defined]
        entity_data: bytes = msg.entity_data  # type: ignore[attr-defined]

        if not is_delta:
            if self._full_packets > 0:
                return []
            self._full_packets += 1

        r = BitReader(entity_data)
        index = -1
        results: list[tuple[Entity, EntityOp]] = []

        for _ in range(updates):
            index += r.read_ubit_var() + 1
            cmd = r.read_bits(2)

            if cmd & 0x01 == 0:
                if cmd & 0x02:
                    # Create entity
                    class_id = r.read_bits(self.class_id_size)
                    serial = r.read_bits(17)
                    r.read_varuint32()  # unknown / padding

                    ci = self.classes_by_id.get(class_id)
                    if ci is None:
                        raise RuntimeError(f"unknown class id {class_id}")

                    entity = Entity(index=index, serial=serial, cls=ci)
                    self.entities[index] = entity

                    # Apply baseline first, then delta
                    baseline = self.class_baselines.get(class_id)
                    if baseline and ci.serializer is not None:
                        read_fields(BitReader(baseline), ci.serializer, entity._field_state)
                    if ci.serializer is not None:
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
                op = EntityOp.LEFT
                if cmd & 0x02:
                    op |= EntityOp.DELETED
                    self.entities[index] = None
                else:
                    entity.active = False

            self.tracker._dispatch(entity, op)
            results.append((entity, op))

        return results

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

    def all_active(self) -> list[Entity]:
        """Return all currently active entities."""
        return [e for e in self.entities if e is not None and e.active]
