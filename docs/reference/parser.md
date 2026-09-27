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

Source: [src/gem/parser.py:232](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L232)

#### Methods

##### `on_entity`

Signature: `def ReplayParser.on_entity(self, callback: EntityCallback) -> None`

Register a handler called for every entity create/update/delete.

Source: [src/gem/parser.py:324](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L324)

##### `on_tick_start`

Signature: `def ReplayParser.on_tick_start(self, callback: TickStartCallback) -> None`

Register a handler called before the current tick's entity deltas.

Source: [src/gem/parser.py:396](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L396)

##### `on_game_event`

Signature: `def ReplayParser.on_game_event(self, name: str, handler: GameEventHandler) -> None`

Register a handler for the named game event.

Source: [src/gem/parser.py:504](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L504)

##### `on_combat_log_entry`

Signature: `def ReplayParser.on_combat_log_entry(self, handler: CombatLogHandler) -> None`

Register a handler for all combat log entries (S1 + S2).

Source: [src/gem/parser.py:513](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L513)

##### `on_chat_message`

Signature: `def ReplayParser.on_chat_message(self, handler: ChatCallback) -> None`

Register a handler for all-chat and team-chat messages.

Source: [src/gem/parser.py:521](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L521)

##### `on_chat_event`

Signature: `def ReplayParser.on_chat_event(self, handler: ChatEventCallback) -> None`

Register a handler for all CDOTAUserMsg_ChatEvent messages.

Source: [src/gem/parser.py:529](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L529)

##### `on_neutral_item_found`

Signature: `def ReplayParser.on_neutral_item_found(self, handler: NeutralItemFoundCallback) -> None`

Register a handler for neutral item found messages.

Source: [src/gem/parser.py:537](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L537)

##### `on_game_start`

Signature: `def ReplayParser.on_game_start(self, callback: Callable[[int], None]) -> None`

Register a handler called once when game time reaches zero.

Source: [src/gem/parser.py:545](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L545)

##### `on_game_end`

Signature: `def ReplayParser.on_game_end(self, callback: Callable[[int], None]) -> None`

Register a handler called once when the ancient is destroyed.

Source: [src/gem/parser.py:557](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L557)

##### `stop_after_tick`

Signature: `def ReplayParser.stop_after_tick(self, tick: int) -> None`

Stop parsing after this tick (inclusive).

Source: [src/gem/parser.py:599](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L599)

##### `parse`

Signature: `def ReplayParser.parse(self) -> None`

Parse the replay from start to finish (or until stop_after_tick).

Source: [src/gem/parser.py:611](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L611)
