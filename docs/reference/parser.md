# ReplayParser

Top-level orchestrator that wires stream decoding, schema/entity updates, event ingestion, and extractor outputs.

See also: [Quickstart](../guides/01_quickstart.md), [Architecture](../architecture.md)

---

## Generated API

## `gem.parser.ReplayParser`

### `ReplayParser`

```python
class ReplayParser
```

Drives a full Source 2 replay parse, wiring all subsystems together.

Source: [src/gem/parser.py:242](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L242)

#### Methods

##### `on_entity`

Signature: `def ReplayParser.on_entity(self, callback: EntityCallback) -> None`

Register a handler called for every entity create/update/delete.

Source: [src/gem/parser.py:334](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L334)

##### `on_tick_start`

Signature: `def ReplayParser.on_tick_start(self, callback: TickStartCallback) -> None`

Register a handler called before the current tick's entity deltas.

Source: [src/gem/parser.py:406](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L406)

##### `on_game_event`

Signature: `def ReplayParser.on_game_event(self, name: str, handler: GameEventHandler) -> None`

Register a handler for the named game event.

Source: [src/gem/parser.py:514](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L514)

##### `on_combat_log_entry`

Signature: `def ReplayParser.on_combat_log_entry(self, handler: CombatLogHandler) -> None`

Register a handler for all combat log entries (S1 + S2).

Source: [src/gem/parser.py:523](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L523)

##### `on_chat_message`

Signature: `def ReplayParser.on_chat_message(self, handler: ChatCallback) -> None`

Register a handler for all-chat and team-chat messages.

Source: [src/gem/parser.py:531](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L531)

##### `on_chat_event`

Signature: `def ReplayParser.on_chat_event(self, handler: ChatEventCallback) -> None`

Register a handler for all CDOTAUserMsg_ChatEvent messages.

Source: [src/gem/parser.py:539](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L539)

##### `on_neutral_item_found`

Signature: `def ReplayParser.on_neutral_item_found(self, handler: NeutralItemFoundCallback) -> None`

Register a handler for neutral item found messages.

Source: [src/gem/parser.py:547](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L547)

##### `on_game_start`

Signature: `def ReplayParser.on_game_start(self, callback: Callable[[int], None]) -> None`

Register a handler called once when game time reaches zero.

Source: [src/gem/parser.py:555](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L555)

##### `on_game_end`

Signature: `def ReplayParser.on_game_end(self, callback: Callable[[int], None]) -> None`

Register a handler called once when the ancient is destroyed.

Source: [src/gem/parser.py:567](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L567)

##### `stop_after_tick`

Signature: `def ReplayParser.stop_after_tick(self, tick: int) -> None`

Stop parsing after this tick (inclusive).

Source: [src/gem/parser.py:609](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L609)

##### `parse`

Signature: `def ReplayParser.parse(self) -> None`

Parse the replay from start to finish (or until stop_after_tick).

Source: [src/gem/parser.py:621](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L621)

## Module `gem.errors`

Exceptions for problems in the replay data itself.

Source: [src/gem/errors.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/errors.py#L1)

### Top-level classes

### `ReplayDataError`

```python
class ReplayDataError(ValueError)
```

The replay's bytes can't be decoded: truncated, corrupt, or unsupported.

Source: [src/gem/errors.py:18](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/errors.py#L18)

### `TruncatedReplayError`

```python
class TruncatedReplayError(ReplayDataError, EOFError)
```

The replay file ends in the middle of a message.

Source: [src/gem/errors.py:22](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/errors.py#L22)

### `UnsupportedReplayError`

```python
class UnsupportedReplayError(ReplayDataError, NotImplementedError)
```

The replay uses a format gem doesn't support (e.g. LZSS string tables).

Source: [src/gem/errors.py:26](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/errors.py#L26)

### `UnknownStringTableError`

```python
class UnknownStringTableError(ReplayDataError, KeyError)
```

A string-table update refers to a table that was never created.

Source: [src/gem/errors.py:30](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/errors.py#L30)

### `EntityStateError`

```python
class EntityStateError(ReplayDataError, RuntimeError)
```

An entity update contradicts the entity table (unknown class, missing entity).

Source: [src/gem/errors.py:34](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/errors.py#L34)
