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

Source: [src/gem/extractors/wards.py:81](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/wards.py#L81)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `player_id` | `int` | `-` |
| `placer` | `str` | `-` |
| `ward_type` | `Literal['observer', 'sentry']` | `-` |
| `team` | `int` | `-` |
| `x` | `float | None` | `-` |
| `y` | `float | None` | `-` |
| `expires_tick` | `int | None` | `-` |
| `killed_tick` | `int | None` | `-` |
| `killer` | `str` | `-` |

### `WardsExtractor`

```python
class WardsExtractor
```

Extracts ward placement, expiry, and kill events from the entity stream.

Source: [src/gem/extractors/wards.py:115](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/wards.py#L115)

#### Properties

##### `_tick`

Signature: `def WardsExtractor._tick(self) -> int`

No docstring available.

Source: [src/gem/extractors/wards.py:159](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/wards.py#L159)

#### Methods

##### `attach`

Signature: `def WardsExtractor.attach(self, parser: ReplayParser) -> None`

Register callbacks with the parser.

Source: [src/gem/extractors/wards.py:148](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/wards.py#L148)

##### `finalize`

Signature: `def WardsExtractor.finalize(self) -> list[WardEvent]`

Back-fill placer names and return ward events.

Source: [src/gem/extractors/wards.py:162](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/wards.py#L162)
