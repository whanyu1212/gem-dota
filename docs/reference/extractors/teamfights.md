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

Source: [src/gem/extractors/teamfights.py:167](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/teamfights.py#L167)

### `detect_opendota_teamfights`

```python
def detect_opendota_teamfights(combat_log: list[CombatLogEntry], hero_to_slot: dict[str, int] | None = None, player_snapshots: dict[int, list[PlayerStateSnapshot]] | None = None, *, game_start_tick: int | None = None, duration_s: int | None = None) -> list[OpenDotaTeamfight]
```

Project combat log entries into OpenDota-compatible teamfight output.

Source: [src/gem/extractors/teamfights.py:425](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/teamfights.py#L425)

### Top-level classes

### `TeamfightPlayer`

```python
class TeamfightPlayer
```

Per-player stats accumulated within one teamfight window.

Source: [src/gem/extractors/teamfights.py:51](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/teamfights.py#L51)

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

Source: [src/gem/extractors/teamfights.py:80](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/teamfights.py#L80)

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
| `centroid_n` | `int` | `0` |
| `players` | `list[TeamfightPlayer]` | `field(...)` |

### `OpenDotaTeamfightPlayer`

```python
class OpenDotaTeamfightPlayer
```

OpenDota-compatible per-player teamfight row.

Source: [src/gem/extractors/teamfights.py:120](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/teamfights.py#L120)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `deaths_pos` | `dict[str, dict[str, int]]` | `field(...)` |
| `ability_uses` | `dict[str, int]` | `field(...)` |
| `ability_targets` | `dict[str, int]` | `field(...)` |
| `item_uses` | `dict[str, int]` | `field(...)` |
| `killed` | `dict[str, int]` | `field(...)` |
| `deaths` | `int` | `0` |
| `buybacks` | `int` | `0` |
| `damage` | `int` | `0` |
| `healing` | `int` | `0` |
| `gold_delta` | `int` | `0` |
| `xp_delta` | `int` | `0` |
| `xp_start` | `int | None` | `None` |
| `xp_end` | `int | None` | `None` |

### `OpenDotaTeamfight`

```python
class OpenDotaTeamfight
```

OpenDota-compatible temporal teamfight window.

Source: [src/gem/extractors/teamfights.py:150](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/teamfights.py#L150)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `start` | `int` | `-` |
| `end` | `int` | `-` |
| `last_death` | `int` | `-` |
| `deaths` | `int` | `-` |
| `players` | `list[OpenDotaTeamfightPlayer]` | `field(...)` |
