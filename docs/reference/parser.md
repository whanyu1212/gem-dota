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

Source: [src/gem/parser.py:198](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L198)

#### Methods

##### `on_entity`

Signature: `def ReplayParser.on_entity(self, callback: EntityCallback) -> None`

Register a handler called for every entity create/update/delete.

Source: [src/gem/parser.py:283](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L283)

##### `on_tick_start`

Signature: `def ReplayParser.on_tick_start(self, callback: TickStartCallback) -> None`

Register a handler called before the current tick's entity deltas.

Source: [src/gem/parser.py:326](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L326)

##### `on_game_event`

Signature: `def ReplayParser.on_game_event(self, name: str, handler: GameEventHandler) -> None`

Register a handler for the named game event.

Source: [src/gem/parser.py:383](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L383)

##### `on_combat_log_entry`

Signature: `def ReplayParser.on_combat_log_entry(self, handler: CombatLogHandler) -> None`

Register a handler for all combat log entries (S1 + S2).

Source: [src/gem/parser.py:392](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L392)

##### `on_chat_message`

Signature: `def ReplayParser.on_chat_message(self, handler: ChatCallback) -> None`

Register a handler for all-chat and team-chat messages.

Source: [src/gem/parser.py:400](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L400)

##### `on_chat_event`

Signature: `def ReplayParser.on_chat_event(self, handler: ChatEventCallback) -> None`

Register a handler for all CDOTAUserMsg_ChatEvent messages.

Source: [src/gem/parser.py:408](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L408)

##### `on_neutral_item_found`

Signature: `def ReplayParser.on_neutral_item_found(self, handler: NeutralItemFoundCallback) -> None`

Register a handler for neutral item found messages.

Source: [src/gem/parser.py:416](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L416)

##### `on_game_start`

Signature: `def ReplayParser.on_game_start(self, callback: Callable[[int], None]) -> None`

Register a handler called once when game time reaches zero.

Source: [src/gem/parser.py:424](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L424)

##### `on_game_end`

Signature: `def ReplayParser.on_game_end(self, callback: Callable[[int], None]) -> None`

Register a handler called once when the ancient is destroyed.

Source: [src/gem/parser.py:436](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L436)

##### `stop_after_tick`

Signature: `def ReplayParser.stop_after_tick(self, tick: int) -> None`

Stop parsing after this tick (inclusive).

Source: [src/gem/parser.py:476](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L476)

##### `parse`

Signature: `def ReplayParser.parse(self) -> None`

Parse the replay from start to finish (or until stop_after_tick).

Source: [src/gem/parser.py:488](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/parser.py#L488)
