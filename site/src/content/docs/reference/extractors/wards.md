# Wards Extractor

Ward placement events with exact map coordinates.

---

## Generated API

## Module `gem.extractors.wards`

Ward placement extractor for Dota 2 replays.

Source: [src/gem/extractors/wards.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/wards.py#L1)

### Top-level classes

### `WardEvent`

```python
class WardEvent
```

A complete ward placement record with coordinates.

Source: [src/gem/extractors/wards.py:87](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/wards.py#L87)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `player_id` | `int` | `-` |
| `placer` | `str` | `-` |
| `ward_type` | `Literal['observer', 'sentry']` | `-` |
| `team` | `int` | `-` |
| `x` | `float \| None` | `-` |
| `y` | `float \| None` | `-` |
| `expires_tick` | `int \| None` | `-` |
| `killed_tick` | `int \| None` | `-` |
| `killer` | `str` | `-` |
| `left_attacker` | `str \| None` | `None` |
| `left_player_id` | `int \| None` | `None` |

### `WardsExtractor`

```python
class WardsExtractor
```

Extracts ward placement, expiry, and kill events from the entity stream.

Source: [src/gem/extractors/wards.py:131](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/wards.py#L131)

#### Properties

##### `_tick`

Signature: `def WardsExtractor._tick(self) -> int`

No docstring available.

Source: [src/gem/extractors/wards.py:188](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/wards.py#L188)

#### Methods

##### `attach`

Signature: `def WardsExtractor.attach(self, parser: ReplayParser) -> None`

Register callbacks with the parser.

Source: [src/gem/extractors/wards.py:173](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/wards.py#L173)

##### `finalize`

Signature: `def WardsExtractor.finalize(self) -> list[WardEvent]`

Back-fill placer names and return ward events.

Source: [src/gem/extractors/wards.py:191](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/wards.py#L191)
