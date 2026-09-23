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

Source: [src/gem/parser.py:202](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L202)

#### Methods

##### `on_entity`

Signature: `def ReplayParser.on_entity(self, callback: EntityCallback) -> None`

Register a handler called for every entity create/update/delete.

Source: [src/gem/parser.py:294](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L294)

##### `on_tick_start`

Signature: `def ReplayParser.on_tick_start(self, callback: TickStartCallback) -> None`

Register a handler called before the current tick's entity deltas.

Source: [src/gem/parser.py:366](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L366)

##### `on_game_event`

Signature: `def ReplayParser.on_game_event(self, name: str, handler: GameEventHandler) -> None`

Register a handler for the named game event.

Source: [src/gem/parser.py:474](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L474)

##### `on_combat_log_entry`

Signature: `def ReplayParser.on_combat_log_entry(self, handler: CombatLogHandler) -> None`

Register a handler for all combat log entries (S1 + S2).

Source: [src/gem/parser.py:483](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L483)

##### `on_chat_message`

Signature: `def ReplayParser.on_chat_message(self, handler: ChatCallback) -> None`

Register a handler for all-chat and team-chat messages.

Source: [src/gem/parser.py:491](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L491)

##### `on_chat_event`

Signature: `def ReplayParser.on_chat_event(self, handler: ChatEventCallback) -> None`

Register a handler for all CDOTAUserMsg_ChatEvent messages.

Source: [src/gem/parser.py:499](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L499)

##### `on_neutral_item_found`

Signature: `def ReplayParser.on_neutral_item_found(self, handler: NeutralItemFoundCallback) -> None`

Register a handler for neutral item found messages.

Source: [src/gem/parser.py:507](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L507)

##### `on_game_start`

Signature: `def ReplayParser.on_game_start(self, callback: Callable[[int], None]) -> None`

Register a handler called once when game time reaches zero.

Source: [src/gem/parser.py:515](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L515)

##### `on_game_end`

Signature: `def ReplayParser.on_game_end(self, callback: Callable[[int], None]) -> None`

Register a handler called once when the ancient is destroyed.

Source: [src/gem/parser.py:527](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L527)

##### `stop_after_tick`

Signature: `def ReplayParser.stop_after_tick(self, tick: int) -> None`

Stop parsing after this tick (inclusive).

Source: [src/gem/parser.py:568](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L568)

##### `parse`

Signature: `def ReplayParser.parse(self) -> None`

Parse the replay from start to finish (or until stop_after_tick).

Source: [src/gem/parser.py:580](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L580)
