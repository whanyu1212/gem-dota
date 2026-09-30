# Fights Extractor

Fight detection (every fight, adjustable grouping), OpenDota-exact teamfights, and per-participant statistics.

---

## Generated API

## Module `gem.extractors.fights`

Fight detection from combat log entries.

Source: [src/gem/extractors/fights.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/fights.py#L1)

### Top-level functions

### `detect_fights`

```python
def detect_fights(combat_log: list[CombatLogEntry], hero_to_slot: dict[str, int] | None = None, player_snapshots: dict[int, list[PlayerStateSnapshot]] | None = None, slot_to_team: dict[int, int] | None = None, *, window_s: float = FIGHT_WINDOW_S, radius: float | None = FIGHT_RADIUS) -> list[Fight]
```

Detect fights from a match combat log.

Source: [src/gem/extractors/fights.py:184](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/fights.py#L184)

### `detect_opendota_teamfights`

```python
def detect_opendota_teamfights(combat_log: list[CombatLogEntry], hero_to_slot: dict[str, int] | None = None, player_snapshots: dict[int, list[PlayerStateSnapshot]] | None = None, *, game_start_tick: int | None = None, duration_s: int | None = None, game_clock: GameClock | None = None, interval_samples: Sequence[IntervalSample] | None = None, aegis_events: Iterable[AegisEvent] = ()) -> list[OpenDotaTeamfight]
```

Project combat log entries into OpenDota-compatible teamfight output.

Source: [src/gem/extractors/fights.py:456](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/fights.py#L456)

### Top-level classes

### `FightPlayer`

```python
class FightPlayer
```

Per-player stats accumulated within one fight window.

Source: [src/gem/extractors/fights.py:68](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/fights.py#L68)

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

### `Fight`

```python
class Fight
```

A detected fight window with per-player breakdowns.

Source: [src/gem/extractors/fights.py:97](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/fights.py#L97)

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
| `centroid_x` | `float \| None` | `None` |
| `centroid_y` | `float \| None` | `None` |
| `centroid_n` | `int` | `0` |
| `players` | `list[FightPlayer]` | `field(...)` |

### `OpenDotaTeamfightPlayer`

```python
class OpenDotaTeamfightPlayer
```

OpenDota-compatible per-player teamfight row.

Source: [src/gem/extractors/fights.py:137](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/fights.py#L137)

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
| `xp_start` | `int \| None` | `None` |
| `xp_end` | `int \| None` | `None` |

### `OpenDotaTeamfight`

```python
class OpenDotaTeamfight
```

OpenDota-compatible temporal teamfight window.

Source: [src/gem/extractors/fights.py:167](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/fights.py#L167)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `start` | `int` | `-` |
| `end` | `int` | `-` |
| `last_death` | `int` | `-` |
| `deaths` | `int` | `-` |
| `players` | `list[OpenDotaTeamfightPlayer]` | `field(...)` |
