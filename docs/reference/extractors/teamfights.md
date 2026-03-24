# Teamfights Extractor

Teamfight window detection and per-participant statistics.

---

## Generated API

## Module `gem.extractors.teamfights`

Teamfight detection from combat log entries.

Source: [src/gem/extractors/teamfights.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/teamfights.py#L1)

### Top-level functions

### `detect_teamfights`

```python
def detect_teamfights(combat_log: list[CombatLogEntry], hero_to_slot: dict[str, int] | None = None, player_snapshots: dict[int, list[PlayerStateSnapshot]] | None = None, slot_to_team: dict[int, int] | None = None) -> list[Teamfight]
```

Detect teamfights from a match combat log.

Source: [src/gem/extractors/teamfights.py:114](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/teamfights.py#L114)

### Top-level classes

### `TeamfightPlayer`

```python
class TeamfightPlayer
```

Per-player stats accumulated within one teamfight window.

Source: [src/gem/extractors/teamfights.py:50](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/teamfights.py#L50)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `player_id` | `int` | `-` |
| `deaths` | `int` | `0` |
| `buybacks` | `int` | `0` |
| `damage_dealt` | `int` | `0` |
| `damage_taken` | `int` | `0` |
| `healing` | `int` | `0` |
| `gold_delta` | `int` | `0` |
| `xp_delta` | `int` | `0` |
| `ability_uses` | `dict[str, int]` | `field(...)` |
| `item_uses` | `dict[str, int]` | `field(...)` |

### `Teamfight`

```python
class Teamfight
```

A detected teamfight window with per-player breakdowns.

Source: [src/gem/extractors/teamfights.py:79](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/teamfights.py#L79)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `start_tick` | `int` | `-` |
| `end_tick` | `int` | `-` |
| `last_death_tick` | `int` | `-` |
| `deaths` | `int` | `-` |
| `first_death_tick` | `int` | `0` |
| `radiant_kills` | `int` | `0` |
| `dire_kills` | `int` | `0` |
| `winner` | `str` | `'unknown'` |
| `centroid_x` | `float | None` | `None` |
| `centroid_y` | `float | None` | `None` |
| `players` | `list[TeamfightPlayer]` | `field(...)` |
