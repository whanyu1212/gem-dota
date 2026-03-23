# Game Events

Handles Source 1 style game events (schema + payload decoding) used for objectives, runes, chat, and related signals.

See also: [How Proto Parsing Works](../cookbook/proto-parsing-pipeline.md)


---


---

## Generated API

## `gem.game_events.GameEventManager`

### `GameEventManager`

```python
class GameEventManager
```

Manages game event schema registration and handler dispatch.

Source: [src/gem/game_events.py:146](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/game_events.py#L146)

#### Methods

##### `register_schema`

Signature: `def GameEventManager.register_schema(self, schema_dict: dict[str, Any]) -> None`

Register an event schema from a dict (e.g. from CSVCMsg_GameEventList).

Source: [src/gem/game_events.py:160](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/game_events.py#L160)

##### `has_event`

Signature: `def GameEventManager.has_event(self, name: str) -> bool`

Return True if an event schema with the given name is registered.

Source: [src/gem/game_events.py:178](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/game_events.py#L178)

##### `on_game_event`

Signature: `def GameEventManager.on_game_event(self, name: str, handler: GameEventHandler) -> None`

Register a handler for the named event.

Source: [src/gem/game_events.py:186](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/game_events.py#L186)

##### `dispatch`

Signature: `def GameEventManager.dispatch(self, raw_event: Any) -> None`

Dispatch a raw CMsgSource1LegacyGameEvent message to registered handlers.

Source: [src/gem/game_events.py:195](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/game_events.py#L195)

## `gem.game_events.GameEvent`

### `GameEvent`

```python
class GameEvent
```

A decoded game event instance.

Source: [src/gem/game_events.py:40](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/game_events.py#L40)

#### Methods

##### `get_string`

Signature: `def GameEvent.get_string(self, name: str) -> tuple[str, str | None]`

Return (value, None) as str, or ('', error) on failure.

Source: [src/gem/game_events.py:65](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/game_events.py#L65)

##### `get_float`

Signature: `def GameEvent.get_float(self, name: str) -> tuple[float, str | None]`

Return (value, None) as float, or (0.0, error) on failure.

Source: [src/gem/game_events.py:80](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/game_events.py#L80)

##### `get_int32`

Signature: `def GameEvent.get_int32(self, name: str) -> tuple[int, str | None]`

Return (value, None) as int32 (long/short/byte), or (0, error).

Source: [src/gem/game_events.py:94](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/game_events.py#L94)

##### `get_bool`

Signature: `def GameEvent.get_bool(self, name: str) -> tuple[bool, str | None]`

Return (value, None) as bool, or (False, error) on failure.

Source: [src/gem/game_events.py:114](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/game_events.py#L114)

##### `get_uint64`

Signature: `def GameEvent.get_uint64(self, name: str) -> tuple[int, str | None]`

Return (value, None) as uint64, or (0, error) on failure.

Source: [src/gem/game_events.py:128](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/game_events.py#L128)

## `gem.game_events.GameEventSchema`

### `GameEventSchema`

```python
class GameEventSchema
```

Schema for a single game event type.

Source: [src/gem/game_events.py:26](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/game_events.py#L26)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `event_id` | `int` | `-` |
| `name` | `str` | `-` |
| `fields` | `dict[str, tuple[int, int]]` | `field(...)` |
