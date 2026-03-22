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

Source: [src/gem/extractors/objectives.py:78](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/objectives.py#L78)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `team` | `int` | `-` |
| `killer` | `str` | `-` |
| `tower_name` | `str` | `-` |

### `RoshanKill`

```python
class RoshanKill
```

One confirmed Roshan death.

Source: [src/gem/extractors/objectives.py:95](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/objectives.py#L95)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `killer` | `str` | `-` |
| `kill_number` | `int` | `-` |
| `drops` | `list[str]` | `field(...)` |

### `BarracksKill`

```python
class BarracksKill
```

One barracks destruction event.

Source: [src/gem/extractors/objectives.py:114](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/objectives.py#L114)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `team` | `int` | `-` |
| `killer` | `str` | `-` |
| `barracks_name` | `str` | `-` |

### `TormentorKill`

```python
class TormentorKill
```

One Tormentor (miniboss) kill event.

Source: [src/gem/extractors/objectives.py:131](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/objectives.py#L131)

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

Source: [src/gem/extractors/objectives.py:150](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/objectives.py#L150)

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

Source: [src/gem/extractors/objectives.py:163](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/objectives.py#L163)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `player_id` | `int` | `-` |
| `event_type` | `str` | `-` |

### `ObjectivesExtractor`

```python
class ObjectivesExtractor
```

Extracts tower kills, Roshan kills, barracks kills, tormentor kills, and shrine kills from a replay.

Source: [src/gem/extractors/objectives.py:183](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/objectives.py#L183)

#### Methods

##### `attach`

Signature: `def ObjectivesExtractor.attach(self, parser: ReplayParser) -> None`

Register this extractor's callbacks with a parser.

Source: [src/gem/extractors/objectives.py:220](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/objectives.py#L220)
