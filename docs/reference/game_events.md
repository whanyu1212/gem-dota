# Game Events

Handles Source 1 style game events: the event schema, and named field access for each
event. Current replays send only broadcast camera hints and version info this way; the
combat log arrives separately.

See also: [`gameevents.proto`](../cookbook/proto-files.md#gameevents-proto-named-game-events-and-the-old-combat-log)
and [How Proto Parsing Works](../cookbook/proto-parsing-pipeline.md).

---

## Generated API

## `gem.state.game_events.GameEventManager`

### `GameEventManager`

```python
class GameEventManager
```

Manages game event schema registration and handler dispatch.

Source: [src/gem/state/game_events.py:217](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_events.py#L217)

#### Methods

##### `register_schema`

Signature: `def GameEventManager.register_schema(self, schema_dict: dict[str, Any]) -> None`

Register an event schema from a dict (e.g. from CSVCMsg_GameEventList).

Source: [src/gem/state/game_events.py:231](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_events.py#L231)

##### `has_event`

Signature: `def GameEventManager.has_event(self, name: str) -> bool`

Return True if an event schema with the given name is registered.

Source: [src/gem/state/game_events.py:249](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_events.py#L249)

##### `get_schema`

Signature: `def GameEventManager.get_schema(self, event_id: int) -> GameEventSchema | None`

Return the registered schema for an event id, or ``None``.

Source: [src/gem/state/game_events.py:257](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_events.py#L257)

##### `on_game_event`

Signature: `def GameEventManager.on_game_event(self, name: str, handler: GameEventHandler) -> None`

Register a handler for the named event.

Source: [src/gem/state/game_events.py:268](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_events.py#L268)

##### `dispatch`

Signature: `def GameEventManager.dispatch(self, raw_event: Any) -> None`

Dispatch a raw CMsgSource1LegacyGameEvent message to registered handlers.

Source: [src/gem/state/game_events.py:277](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_events.py#L277)

## `gem.state.game_events.GameEvent`

### `GameEvent`

```python
class GameEvent
```

A decoded game event instance.

Source: [src/gem/state/game_events.py:65](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_events.py#L65)

#### Properties

##### `name`

Signature: `def GameEvent.name(self) -> str`

The event's name, e.g. ``"dota_combatlog"``.

Source: [src/gem/state/game_events.py:82](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_events.py#L82)

#### Methods

##### `get`

Signature: `def GameEvent.get(self, name: str, default: Any = None) -> Any`

Return the value of field *name*, or *default* if it is missing.

Source: [src/gem/state/game_events.py:86](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_events.py#L86)

##### `to_dict`

Signature: `def GameEvent.to_dict(self) -> dict[str, Any]`

Return every field present in this event, by name.

Source: [src/gem/state/game_events.py:113](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_events.py#L113)

##### `get_string`

Signature: `def GameEvent.get_string(self, name: str) -> tuple[str, str | None]`

Return (value, None) as str, or ('', error) on failure.

Source: [src/gem/state/game_events.py:131](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_events.py#L131)

##### `get_float`

Signature: `def GameEvent.get_float(self, name: str) -> tuple[float, str | None]`

Return (value, None) as float, or (0.0, error) on failure.

Source: [src/gem/state/game_events.py:146](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_events.py#L146)

##### `get_int32`

Signature: `def GameEvent.get_int32(self, name: str) -> tuple[int, str | None]`

Return (value, None) as an integer, or (0, error).

Source: [src/gem/state/game_events.py:160](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_events.py#L160)

##### `get_bool`

Signature: `def GameEvent.get_bool(self, name: str) -> tuple[bool, str | None]`

Return (value, None) as bool, or (False, error) on failure.

Source: [src/gem/state/game_events.py:177](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_events.py#L177)

##### `get_uint64`

Signature: `def GameEvent.get_uint64(self, name: str) -> tuple[int, str | None]`

Return (value, None) as uint64, or (0, error) on failure.

Source: [src/gem/state/game_events.py:191](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_events.py#L191)

## `gem.state.game_events.GameEventSchema`

### `GameEventSchema`

```python
class GameEventSchema
```

Schema for a single game event type.

Source: [src/gem/state/game_events.py:51](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_events.py#L51)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `event_id` | `int` | `-` |
| `name` | `str` | `-` |
| `fields` | `dict[str, tuple[int, int]]` | `field(...)` |
