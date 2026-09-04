# Objectives Extractor

Tower kills, barracks destructions, Roshan kills, and Tormentor kills.

## Tormentor Kills

Tracks destruction of Tormentor minibosses. Killer player attribution is resolved by
combining combat log death data with the corresponding miniboss kill chat event.

---

## Generated API

## Module `gem.extractors.objectives`

Objective event extractor for Dota 2 replays.

Source: [src/gem/extractors/objectives.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/objectives.py#L1)

### Top-level classes

### `TowerKill`

```python
class TowerKill
```

One tower destruction event.

Source: [src/gem/extractors/objectives.py:89](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/objectives.py#L89)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `team` | `int` | `-` |
| `killer` | `str` | `-` |
| `tower_name` | `str` | `-` |
| `killer_source` | `str` | `''` |

### `RoshanKill`

```python
class RoshanKill
```

One confirmed Roshan death.

Source: [src/gem/extractors/objectives.py:111](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/objectives.py#L111)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `killer` | `str` | `-` |
| `kill_number` | `int` | `-` |
| `drops` | `list[str]` | `field(...)` |
| `killer_source` | `str` | `''` |

### `BarracksKill`

```python
class BarracksKill
```

One barracks destruction event.

Source: [src/gem/extractors/objectives.py:133](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/objectives.py#L133)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `team` | `int` | `-` |
| `killer` | `str` | `-` |
| `barracks_name` | `str` | `-` |
| `killer_source` | `str` | `''` |

### `TormentorKill`

```python
class TormentorKill
```

One Tormentor (miniboss) kill event.

Source: [src/gem/extractors/objectives.py:153](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/objectives.py#L153)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `killer` | `str` | `-` |
| `killer_player_id` | `int` | `-` |
| `kill_number` | `int` | `-` |

### `ShrineKill`

```python
class ShrineKill
```

One Shrine of Wisdom destruction event.

Source: [src/gem/extractors/objectives.py:172](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/objectives.py#L172)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `team` | `int` | `-` |

### `AegisEvent`

```python
class AegisEvent
```

An Aegis of the Immortal pickup, steal, or denial event.

Source: [src/gem/extractors/objectives.py:185](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/objectives.py#L185)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `player_id` | `int` | `-` |
| `event_type` | `str` | `-` |

### `BannerPlant`

```python
class BannerPlant
```

One Roshan's Banner plant event.

Source: [src/gem/extractors/objectives.py:201](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/objectives.py#L201)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `team` | `int` | `-` |
| `player_id` | `int` | `-` |
| `x` | `float \| None` | `-` |
| `y` | `float \| None` | `-` |

### `CourierDeath`

```python
class CourierDeath
```

One courier death, detected from the combat log.

Source: [src/gem/extractors/objectives.py:225](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/objectives.py#L225)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `killer` | `str` | `-` |
| `killer_source` | `str` | `''` |

### `ObjectivesExtractor`

```python
class ObjectivesExtractor
```

Extracts tower kills, Roshan kills, barracks kills, tormentor kills, and shrine kills from a replay.

Source: [src/gem/extractors/objectives.py:250](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/objectives.py#L250)

#### Methods

##### `attach`

Signature: `def ObjectivesExtractor.attach(self, parser: ReplayParser) -> None`

Register this extractor's callbacks with a parser.

Source: [src/gem/extractors/objectives.py:308](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/objectives.py#L308)
