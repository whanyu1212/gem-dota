# Writing Custom Extractors

Built-in extractors cover common analysis needs, but `gem` is designed to be extensible.
This guide shows how to attach your own extractor logic to parser callbacks and return
custom analysis outputs.

---

## Extension model (high level)

A custom extractor is usually a small stateful class with an `attach(parser)` method.
Inside `attach`, register handlers on `ReplayParser` callback hooks.

Common hooks:

- `parser.on_entity(handler)` — `(entity, op)` for entity lifecycle + field updates
- `parser.on_game_event(name, handler)` — typed Source 1 game events
- `parser.on_combat_log_entry(handler)` — normalized combat log entries
- `parser.on_neutral_item_found(handler)` — neutral item find user messages
- `parser.on_game_start(handler)` — first game tick callback
- `parser.on_game_end(handler)` — final tick callback

There is no required abstract base class — just follow the convention used by built-in extractors.

---

## Minimal extractor example

```python
from __future__ import annotations

from dataclasses import dataclass, field

from gem.state.entities import EntityOp
from gem.parser import ReplayParser


@dataclass
class HeroSpawnExtractor:
    """Collect first-seen hero spawn ticks."""
    spawns: list[tuple[int, str]] = field(default_factory=list)

    def attach(self, parser: ReplayParser) -> None:
        parser.on_entity(self._on_entity)

    def _on_entity(self, entity, op: EntityOp) -> None:
        if not (op & EntityOp.CREATED):
            return
        cls = entity.get_class_name()
        if "CDOTA_Unit_Hero_" not in cls:
            return
        self.spawns.append((entity.get_index(), cls))
```

---

## Attaching to the parser

```python
from gem.parser import ReplayParser

parser = ReplayParser("my_replay.dem")

hero_spawns = HeroSpawnExtractor()
hero_spawns.attach(parser)

parser.parse()   # ReplayParser.parse() returns None — read results off the extractor

print(f"Recorded {len(hero_spawns.spawns)} hero creations")
```

::: tip
`ReplayParser` is the low-level driver: you attach extractors and read their
collected state after `parse()`. If you want a fully-assembled `ParsedMatch` back,
use the high-level `gem.parse("my_replay.dem")` instead.
:::

---

## Pattern used by built-in extractors

Built-in extractors follow the same `attach()` style: register parser hooks, collect state,
then expose the result to the match assembly layer.

Practical tips:
- keep callback logic lightweight (hot path),
- guard early (class-name checks, op checks),
- store normalized values (ticks, ids, names) for easier post-processing.

---

## Debugging custom extractors

If a field lookup returns missing values:

1. confirm class name and operation (`CREATED`, `UPDATED`, etc.),
2. inspect available fields on live entities,
3. verify the replay patch/version (Valve schema fields can change names).

For lower-level mechanics, see:
- [Entity State](02_entity_state.md)
- [How Proto Parsing Works](../cookbook/proto-parsing-pipeline.md)
- [Entities API Reference](../reference/entities.md)
