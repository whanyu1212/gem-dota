"""Game event schema registration and typed dispatch.

Handles ``CSVCMsg_GameEventList`` (schema registration) and
``CSVCMsg_GameEvent`` (dispatch) messages.

Reference: manta/game_event.go
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

# Key type IDs matching Source 2 protobuf encoding
_TYPE_STRING = 1
_TYPE_FLOAT = 2
_TYPE_LONG = 3
_TYPE_SHORT = 4
_TYPE_BYTE = 5
_TYPE_BOOL = 6
_TYPE_UINT64 = 7


@dataclass
class GameEventSchema:
    """Schema for a single game event type.

    Attributes:
        event_id: Numeric event identifier.
        name: Human-readable event name.
        fields: Mapping of field name → (key_index, type_id).
    """

    event_id: int
    name: str
    fields: dict[str, tuple[int, int]] = field(default_factory=dict)


class GameEvent:
    """A decoded game event instance.

    Wraps a raw ``CSVCMsg_GameEvent`` message and its schema to provide
    typed field accessors.

    Attributes:
        schema: The GameEventSchema for this event type.
        msg: The raw protobuf message.
    """

    def __init__(self, schema: GameEventSchema, msg: Any) -> None:
        self.schema = schema
        self._keys = list(msg.keys)

    def _get_key(self, name: str) -> tuple[Any, str | None]:
        """Return (key_obj, error_str) for the named field."""
        entry = self.schema.fields.get(name)
        if entry is None:
            return None, f"field {name!r} not in event schema {self.schema.name!r}"
        key_idx, _ = entry
        if key_idx >= len(self._keys):
            return None, f"field {name!r} index {key_idx} out of range"
        return self._keys[key_idx], None

    def get_string(self, name: str) -> tuple[str, str | None]:
        """Return (value, None) as str, or ('', error) on failure.

        Args:
            name: Field name.
        """
        key, err = self._get_key(name)
        if err:
            return "", err
        entry = self.schema.fields[name]
        _, type_id = entry
        if type_id != _TYPE_STRING:
            return "", f"field {name!r} is type {type_id}, not string"
        return key.val_string, None

    def get_float(self, name: str) -> tuple[float, str | None]:
        """Return (value, None) as float, or (0.0, error) on failure.

        Args:
            name: Field name.
        """
        key, err = self._get_key(name)
        if err:
            return 0.0, err
        _, type_id = self.schema.fields[name]
        if type_id != _TYPE_FLOAT:
            return 0.0, f"field {name!r} is type {type_id}, not float"
        return key.val_float, None

    def get_int32(self, name: str) -> tuple[int, str | None]:
        """Return (value, None) as int32 (long/short/byte), or (0, error).

        Accepts long (3), short (4), or byte (5) type IDs.

        Args:
            name: Field name.
        """
        key, err = self._get_key(name)
        if err:
            return 0, err
        _, type_id = self.schema.fields[name]
        if type_id == _TYPE_LONG:
            return key.val_long, None
        if type_id == _TYPE_SHORT:
            return key.val_short, None
        if type_id == _TYPE_BYTE:
            return key.val_byte, None
        return 0, f"field {name!r} is type {type_id}, not an integer type"

    def get_bool(self, name: str) -> tuple[bool, str | None]:
        """Return (value, None) as bool, or (False, error) on failure.

        Args:
            name: Field name.
        """
        key, err = self._get_key(name)
        if err:
            return False, err
        _, type_id = self.schema.fields[name]
        if type_id != _TYPE_BOOL:
            return False, f"field {name!r} is type {type_id}, not bool"
        return key.val_bool, None

    def get_uint64(self, name: str) -> tuple[int, str | None]:
        """Return (value, None) as uint64, or (0, error) on failure.

        Args:
            name: Field name.
        """
        key, err = self._get_key(name)
        if err:
            return 0, err
        _, type_id = self.schema.fields[name]
        if type_id != _TYPE_UINT64:
            return 0, f"field {name!r} is type {type_id}, not uint64"
        return key.val_uint64, None


GameEventHandler = Callable[[GameEvent], None]


class GameEventManager:
    """Manages game event schema registration and handler dispatch.

    Attributes:
        _schemas_by_id: event_id → GameEventSchema.
        _schemas_by_name: event_name → GameEventSchema.
        _handlers: event_name → list of handlers.
    """

    def __init__(self) -> None:
        self._schemas_by_id: dict[int, GameEventSchema] = {}
        self._schemas_by_name: dict[str, GameEventSchema] = {}
        self._handlers: dict[str, list[GameEventHandler]] = {}

    def register_schema(self, schema_dict: dict[str, Any]) -> None:
        """Register an event schema from a dict (e.g. from CSVCMsg_GameEventList).

        Expected keys: ``eventid``, ``name``, ``keys`` (list of ``{name, type}``).

        Args:
            schema_dict: Dict with event schema data.
        """
        event_id: int = schema_dict["eventid"]
        name: str = schema_dict["name"]
        fields: dict[str, tuple[int, int]] = {}
        for i, k in enumerate(schema_dict.get("keys", [])):
            fields[k["name"]] = (i, k["type"])

        schema = GameEventSchema(event_id=event_id, name=name, fields=fields)
        self._schemas_by_id[event_id] = schema
        self._schemas_by_name[name] = schema

    def has_event(self, name: str) -> bool:
        """Return True if an event schema with the given name is registered.

        Args:
            name: Event name to check.
        """
        return name in self._schemas_by_name

    def on_game_event(self, name: str, handler: GameEventHandler) -> None:
        """Register a handler for the named event.

        Args:
            name: Event name to listen for.
            handler: Callable ``(GameEvent) -> None``.
        """
        self._handlers.setdefault(name, []).append(handler)

    def dispatch(self, raw_event: Any) -> None:
        """Dispatch a raw CMsgSource1LegacyGameEvent message to registered handlers.

        Args:
            raw_event: A ``CMsgSource1LegacyGameEvent``-like object with
                ``eventid`` and ``keys`` attributes.
        """
        event_id: int = raw_event.eventid
        schema = self._schemas_by_id.get(event_id)
        if schema is None:
            return

        handlers = self._handlers.get(schema.name, [])
        if not handlers:
            return

        event = GameEvent(schema=schema, msg=raw_event)
        for h in handlers:
            h(event)
