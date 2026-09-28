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

Source: [src/gem/parser.py:228](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L228)

#### Properties

##### `net_tick`

Signature: `def ReplayParser.net_tick(self) -> int`

Current net tick (from ``net_Tick`` inner messages).

Source: [src/gem/parser.py:306](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L306)

##### `game_time_s`

Signature: `def ReplayParser.game_time_s(self) -> int | None`

Rounded game-relative clock, refreshed at network-tick start.

Source: [src/gem/parser.py:315](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L315)

##### `game_clock`

Signature: `def ReplayParser.game_clock(self) -> GameClock`

Pause-aware tick/game-time anchors and observed pauses.

Source: [src/gem/parser.py:324](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L324)

##### `game_start_tick`

Signature: `def ReplayParser.game_start_tick(self) -> int | None`

Replay tick at which the game start (horn) was first seen.

Source: [src/gem/parser.py:333](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L333)

##### `combat_log_time_s`

Signature: `def ReplayParser.combat_log_time_s(self) -> int | None`

Horn-anchored time of the latest timed combat-log entry.

Source: [src/gem/parser.py:342](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L342)

##### `duration_s`

Signature: `def ReplayParser.duration_s(self) -> int | None`

OpenDota-style match duration: combat-log time at ``POST_GAME``.

Source: [src/gem/parser.py:355](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L355)

#### Methods

##### `net_tick`

Signature: `def ReplayParser.net_tick(self, value: int) -> None`

No docstring available.

Source: [src/gem/parser.py:311](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L311)

##### `game_time_s`

Signature: `def ReplayParser.game_time_s(self, value: int | None) -> None`

No docstring available.

Source: [src/gem/parser.py:320](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L320)

##### `game_clock`

Signature: `def ReplayParser.game_clock(self, value: GameClock) -> None`

No docstring available.

Source: [src/gem/parser.py:329](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L329)

##### `game_start_tick`

Signature: `def ReplayParser.game_start_tick(self, value: int | None) -> None`

No docstring available.

Source: [src/gem/parser.py:338](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L338)

##### `combat_log_time_s`

Signature: `def ReplayParser.combat_log_time_s(self, value: int | None) -> None`

No docstring available.

Source: [src/gem/parser.py:351](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L351)

##### `duration_s`

Signature: `def ReplayParser.duration_s(self, value: int | None) -> None`

No docstring available.

Source: [src/gem/parser.py:360](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L360)

##### `on_entity`

Signature: `def ReplayParser.on_entity(self, callback: EntityCallback) -> None`

Register a handler called for every entity create/update/delete.

Source: [src/gem/parser.py:367](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L367)

##### `on_tick_start`

Signature: `def ReplayParser.on_tick_start(self, callback: TickStartCallback) -> None`

Register a handler called before the current tick's entity deltas.

Source: [src/gem/parser.py:399](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L399)

##### `on_game_event`

Signature: `def ReplayParser.on_game_event(self, name: str, handler: GameEventHandler) -> None`

Register a handler for the named game event.

Source: [src/gem/parser.py:429](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L429)

##### `on_combat_log_entry`

Signature: `def ReplayParser.on_combat_log_entry(self, handler: CombatLogHandler) -> None`

Register a handler for all combat log entries (S1 + S2).

Source: [src/gem/parser.py:438](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L438)

##### `on_chat_message`

Signature: `def ReplayParser.on_chat_message(self, handler: ChatCallback) -> None`

Register a handler for all-chat and team-chat messages.

Source: [src/gem/parser.py:446](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L446)

##### `on_chat_event`

Signature: `def ReplayParser.on_chat_event(self, handler: ChatEventCallback) -> None`

Register a handler for all CDOTAUserMsg_ChatEvent messages.

Source: [src/gem/parser.py:454](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L454)

##### `on_neutral_item_found`

Signature: `def ReplayParser.on_neutral_item_found(self, handler: NeutralItemFoundCallback) -> None`

Register a handler for neutral item found messages.

Source: [src/gem/parser.py:462](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L462)

##### `on_game_start`

Signature: `def ReplayParser.on_game_start(self, callback: Callable[[int], None]) -> None`

Register a handler called once when game time reaches zero.

Source: [src/gem/parser.py:470](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L470)

##### `on_game_end`

Signature: `def ReplayParser.on_game_end(self, callback: Callable[[int], None]) -> None`

Register a handler called once when the ancient is destroyed.

Source: [src/gem/parser.py:482](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L482)

##### `stop_after_tick`

Signature: `def ReplayParser.stop_after_tick(self, tick: int) -> None`

Stop parsing after this tick (inclusive).

Source: [src/gem/parser.py:524](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L524)

##### `parse`

Signature: `def ReplayParser.parse(self) -> None`

Parse the replay from start to finish (or until stop_after_tick).

Source: [src/gem/parser.py:536](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L536)

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

### `VarintOverflowError`

```python
class VarintOverflowError(ReplayDataError, OverflowError)
```

A varint in the replay encodes a value too large for its type.

Source: [src/gem/errors.py:26](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/errors.py#L26)

### `UnsupportedReplayError`

```python
class UnsupportedReplayError(ReplayDataError, NotImplementedError)
```

The replay uses a format gem doesn't support (e.g. LZSS string tables).

Source: [src/gem/errors.py:30](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/errors.py#L30)

### `UnknownStringTableError`

```python
class UnknownStringTableError(ReplayDataError, KeyError)
```

A string-table update refers to a table that was never created.

Source: [src/gem/errors.py:34](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/errors.py#L34)

### `EntityStateError`

```python
class EntityStateError(ReplayDataError, RuntimeError)
```

An entity update contradicts the entity table (unknown class, missing entity).

Source: [src/gem/errors.py:38](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/errors.py#L38)
