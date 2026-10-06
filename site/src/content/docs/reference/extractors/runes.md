# Runes Extractor

Every power, bounty and water rune that spawned, and how it ended.

## Rune lifecycle

Each rune is a `CDOTA_Item_Rune` entity while it sits on the map: its creation gives
the spawn tick, type and position, and its deletion the tick it left. The rune chat
events say who took it and how: picked up, put in a Bottle, or denied. A rune removed
with no chat event was not taken (power runes are replaced at the next spawn), and a
bottled rune's later use is the pickup that removes no rune of its own. Wisdom runes
are no entity, so they stay `PICKUP_RUNE` entries in the combat log.

---

## Generated API

## Module `gem.extractors.runes`

Rune extractor: every rune that spawned, where, and how it ended.

Source: [src/gem/extractors/runes.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/runes.py#L1)

### Top-level classes

### `Rune`

```python
class Rune
```

One rune that spawned, and how it ended.

Source: [src/gem/extractors/runes.py:59](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/runes.py#L59)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `spawn_tick` | `int` | `-` |
| `rune_type` | `int` | `-` |
| `x` | `float \| None` | `-` |
| `y` | `float \| None` | `-` |
| `end_tick` | `int \| None` | `None` |
| `outcome` | `RuneOutcome` | `'still_there'` |
| `player_id` | `int \| None` | `None` |
| `used_tick` | `int \| None` | `None` |

### `RuneExtractor`

```python
class RuneExtractor
```

Collects every rune entity and the rune chat events, then matches them.

Source: [src/gem/extractors/runes.py:88](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/runes.py#L88)

#### Methods

##### `attach`

Signature: `def RuneExtractor.attach(self, parser: ReplayParser) -> None`

Register this extractor's callbacks with a parser.

Source: [src/gem/extractors/runes.py:109](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/runes.py#L109)

##### `finalize`

Signature: `def RuneExtractor.finalize(self) -> list[Rune]`

Match the chat events to the runes and return every rune, by spawn tick.

Source: [src/gem/extractors/runes.py:147](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/runes.py#L147)
