# Models

Output dataclasses produced by `gem.parse()`.

See also: [Full Match Data](../guides/04_match_data.md), [Quickstart](../guides/01_quickstart.md)

## Notable recent fields

- `ParsedMatch.radiant_team_id` / `dire_team_id`: `int` — tournament team ID (matches OpenDota `/teams/{id}` URL). `0` for pub games.
- `ParsedMatch.radiant_team_name` / `dire_team_name`: `str` — team name (e.g. `"Xtreme Gaming"`). Empty string for pub games.
- `ParsedMatch.radiant_team_tag` / `dire_team_tag`: `str` — team tag (e.g. `"XG"`). Empty string for pub games.
- `ParsedPlayer.steam_id`: `int` — 64-bit Steam ID. `0` if unavailable.
- `ParsedPlayer.account_id`: `int` — 32-bit account ID (the ID in OpenDota/Dotabuff player URLs). `0` if unavailable.
- `ParsedMatch.neutral_item_finds`: `list[NeutralItemFoundEvent]` — replay-observed neutral item finds from `DOTA_UM_FoundNeutralItem`, including resolved item and enhancement keys.
- `ParsedMatch.vision_modifiers`: `list[VisionModifierEvent]` *(experimental)* — every application of a vision-granting modifier (Slardar Corrosive Haze, BH Track, Dust of Appearance, Gem of True Sight). See [`estimate_vision`](analysis.md) for how these integrate with the vision API.
- `ParsedMatch.tormentors`: `list[TormentorKill]` — chronological Tormentor kill events.
- `ParsedMatch.shrines`: `list[ShrineKill]` — chronological Shrine of Wisdom destruction events.
- `ParsedPlayer.damage_by_type`: `dict[str, int]` — total damage dealt by damage type (`physical`, `magical`, `pure`).
- `ParsedPlayer.damage_taken_by_type`: `dict[str, int]` — total damage taken by damage type.
- `ParsedPlayer.buyback_log`: `list[CombatLogEntry]` — buyback events attributed to the player.
- `ParsedPlayer.lane_efficiency_pct`: `int` — lane efficiency percentage derived from lane gold.

## TormentorKill

- `tick`: game tick of the kill.
- `killer`: NPC name of the killing unit.
- `killer_player_id`: player slot (`0-9`) of the killer when resolved, else `-1`.
- `kill_number`: sequential Tormentor kill number in the match.

---

## Generated API

## Module `gem.results.models`

Output data models for gem replay parsing.

Source: [src/gem/results/models.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L1)

### Top-level classes

### `VisionModifierEvent`

```python
class VisionModifierEvent
```

A vision-granting modifier applied to a hero (Slardar ulti, BH Track, Dust, Gem, etc.).

Source: [src/gem/results/models.py:33](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L33)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `end_tick` | `int \| None` | `-` |
| `modifier_name` | `str` | `-` |
| `target_name` | `str` | `-` |
| `caster_name` | `str` | `-` |
| `caster_team` | `int` | `-` |

### `SmokeEvent`

```python
class SmokeEvent
```

One Smoke of Deceit activation.

Source: [src/gem/results/models.py:59](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L59)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `activator` | `str` | `-` |
| `team` | `int` | `-` |
| `smoked` | `list[str]` | `field(...)` |
| `x` | `float \| None` | `None` |
| `y` | `float \| None` | `None` |

### `BuybackEvent`

```python
class BuybackEvent
```

One buyback, with its estimated gold cost.

Source: [src/gem/results/models.py:82](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L82)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `player_slot` | `int` | `-` |
| `cost` | `int` | `-` |
| `net_worth` | `int` | `-` |

### `ChatEntry`

```python
class ChatEntry
```

A single chat message from the match.

Source: [src/gem/results/models.py:110](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L110)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `player_slot` | `int` | `-` |
| `channel` | `str` | `-` |
| `text` | `str` | `-` |

### `NeutralItemFoundEvent`

```python
class NeutralItemFoundEvent
```

A neutral item found event emitted by DOTA_UM_FoundNeutralItem.

Source: [src/gem/results/models.py:127](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L127)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `player_id` | `int` | `-` |
| `item_ability_id` | `int` | `-` |
| `item_key` | `str` | `''` |
| `item_tier` | `int` | `0` |
| `tier_item_count` | `int` | `0` |
| `enhancement_ability_id` | `int` | `-1` |
| `enhancement_key` | `str` | `''` |
| `enhancement_level` | `int` | `0` |
| `trinket_level` | `int` | `0` |

### `ParsedPlayer`

```python
class ParsedPlayer
```

Aggregated statistics for one player over a full match.

Source: [src/gem/results/models.py:161](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L161)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `player_id` | `int` | `-` |
| `hero_name` | `str` | `''` |
| `player_name` | `str` | `''` |
| `steam_id` | `int` | `0` |
| `account_id` | `int` | `0` |
| `team` | `int` | `0` |
| `times` | `list[int]` | `field(...)` |
| `gold_t` | `list[int]` | `field(...)` |
| `total_earned_gold_t` | `list[int]` | `field(...)` |
| `net_worth_t` | `list[int]` | `field(...)` |
| `lh_t` | `list[int]` | `field(...)` |
| `dn_t` | `list[int]` | `field(...)` |
| `xp_t` | `list[int]` | `field(...)` |
| `times_min` | `list[int]` | `field(...)` |
| `gold_t_min` | `list[int]` | `field(...)` |
| `total_earned_gold_t_min` | `list[int]` | `field(...)` |
| `total_earned_xp_t_min` | `list[int]` | `field(...)` |
| `net_worth_t_min` | `list[int]` | `field(...)` |
| `lh_t_min` | `list[int]` | `field(...)` |
| `dn_t_min` | `list[int]` | `field(...)` |
| `xp_t_min` | `list[int]` | `field(...)` |
| `total_hero_damage_t_min` | `list[int]` | `field(...)` |
| `total_hero_healing_t_min` | `list[int]` | `field(...)` |
| `total_deaths_t_min` | `list[int]` | `field(...)` |
| `total_stuns_t_min` | `list[float]` | `field(...)` |
| `obs_log` | `list[WardEvent]` | `field(...)` |
| `sen_log` | `list[WardEvent]` | `field(...)` |
| `obs_left_log` | `list[dict[str, Any]]` | `field(...)` |
| `sen_left_log` | `list[dict[str, Any]]` | `field(...)` |
| `obs` | `dict[str, dict[str, int]]` | `field(...)` |
| `sen` | `dict[str, dict[str, int]]` | `field(...)` |
| `damage` | `dict[str, int]` | `field(...)` |
| `damage_taken` | `dict[str, int]` | `field(...)` |
| `damage_by_type` | `dict[str, int]` | `field(...)` |
| `damage_taken_by_type` | `dict[str, int]` | `field(...)` |
| `damage_inflictor` | `dict[str, int]` | `field(...)` |
| `damage_inflictor_received` | `dict[str, int]` | `field(...)` |
| `damage_targets` | `dict[str, dict[str, int]]` | `field(...)` |
| `ability_targets` | `dict[str, dict[str, int]]` | `field(...)` |
| `hero_hits` | `dict[str, int]` | `field(...)` |
| `max_hero_hit` | `dict[str, Any] \| None` | `None` |
| `healing` | `dict[str, int]` | `field(...)` |
| `ability_uses` | `dict[str, int]` | `field(...)` |
| `ability_upgrades_arr` | `list[int]` | `field(...)` |
| `item_uses` | `dict[str, int]` | `field(...)` |
| `final_items` | `dict[int, str]` | `field(...)` |
| `gold_reasons` | `dict[str, int]` | `field(...)` |
| `xp_reasons` | `dict[str, int]` | `field(...)` |
| `kills_log` | `list[CombatLogEntry]` | `field(...)` |
| `purchase_log` | `list[CombatLogEntry]` | `field(...)` |
| `runes_log` | `list[CombatLogEntry]` | `field(...)` |
| `buyback_log` | `list[CombatLogEntry]` | `field(...)` |
| `buybacks` | `list[BuybackEvent]` | `field(...)` |
| `lane_pos` | `defaultdict[str, int]` | `field(...)` |
| `position_log` | `list[tuple[int, float, float]]` | `field(...)` |
| `stuns_dealt` | `float` | `0.0` |
| `kills` | `int` | `0` |
| `deaths` | `int` | `0` |
| `assists` | `int` | `0` |
| `lane_role` | `int` | `0` |
| `lane_last_hits` | `int` | `0` |
| `lane_denies` | `int` | `0` |
| `lane_total_gold` | `int` | `0` |
| `lane_total_xp` | `int` | `0` |
| `lane_efficiency_pct` | `int` | `0` |
| `lane_gold_adv` | `int \| None` | `None` |
| `lane_xp_adv` | `int \| None` | `None` |
| `net_worth` | `int` | `0` |
| `last_hits` | `int` | `0` |
| `denies` | `int` | `0` |
| `camps_stacked` | `int` | `0` |
| `creeps_stacked` | `int` | `0` |
| `obs_placed` | `int` | `0` |
| `sen_placed` | `int` | `0` |
| `rune_pickups` | `int` | `0` |
| `tower_kills` | `int` | `0` |
| `kda` | `float` | `0.0` |
| `buyback_count` | `int` | `0` |
| `is_radiant` | `bool` | `False` |
| `win` | `int` | `0` |
| `kills_per_min` | `float` | `0.0` |
| `hero_damage` | `int` | `0` |
| `tower_damage` | `int` | `0` |
| `hero_healing` | `int` | `0` |
| `gold_per_min` | `int` | `0` |
| `xp_per_min` | `int` | `0` |
| `total_gold` | `int` | `0` |
| `total_xp` | `int` | `0` |
| `killed` | `dict[str, int]` | `field(...)` |
| `ancient_kills` | `int` | `0` |
| `neutral_kills` | `int` | `0` |
| `lane_kills` | `int` | `0` |
| `courier_kills` | `int` | `0` |
| `observer_kills` | `int` | `0` |
| `sentry_kills` | `int` | `0` |
| `roshan_kills` | `int` | `0` |
| `hero_id` | `int` | `0` |
| `level` | `int` | `0` |
| `gold_spent` | `int` | `0` |
| `life_state_dead` | `int` | `0` |
| `firstblood_claimed` | `int` | `0` |
| `teamfight_participation` | `float` | `0.0` |
| `purchase` | `dict[str, int]` | `field(...)` |
| `purchase_time` | `dict[str, int]` | `field(...)` |
| `first_purchase_time` | `dict[str, int]` | `field(...)` |
| `purchase_tpscroll` | `int` | `0` |
| `purchase_ward_observer` | `int` | `0` |
| `purchase_ward_sentry` | `int` | `0` |
| `observer_uses` | `int` | `0` |
| `sentry_uses` | `int` | `0` |
| `observers_placed` | `int` | `0` |

### `ParsedMatch`

```python
class ParsedMatch
```

Top-level parsed output for a single Dota 2 replay.

Source: [src/gem/results/models.py:536](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L536)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `match_id` | `int` | `0` |
| `game_mode` | `int` | `0` |
| `leagueid` | `int` | `0` |
| `radiant_win` | `bool \| None` | `None` |
| `radiant_team_id` | `int` | `0` |
| `radiant_team_name` | `str` | `''` |
| `radiant_team_tag` | `str` | `''` |
| `dire_team_id` | `int` | `0` |
| `dire_team_name` | `str` | `''` |
| `dire_team_tag` | `str` | `''` |
| `game_start_tick` | `int \| None` | `None` |
| `game_end_tick` | `int` | `0` |
| `duration` | `int` | `0` |
| `radiant_score` | `int` | `0` |
| `dire_score` | `int` | `0` |
| `first_blood_time` | `int` | `0` |
| `pre_game_duration` | `int` | `0` |
| `players` | `list[ParsedPlayer]` | `field(...)` |
| `towers` | `list[TowerKill]` | `field(...)` |
| `barracks` | `list[BarracksKill]` | `field(...)` |
| `roshans` | `list[RoshanKill]` | `field(...)` |
| `aegis_events` | `list[AegisEvent]` | `field(...)` |
| `tormentors` | `list[TormentorKill]` | `field(...)` |
| `shrines` | `list[ShrineKill]` | `field(...)` |
| `courier_deaths` | `list[CourierDeath]` | `field(...)` |
| `objectives` | `list[dict[str, Any]]` | `field(...)` |
| `tower_status_radiant` | `int` | `0` |
| `tower_status_dire` | `int` | `0` |
| `barracks_status_radiant` | `int` | `0` |
| `barracks_status_dire` | `int` | `0` |
| `wards` | `list[WardEvent]` | `field(...)` |
| `radiant_gold_adv` | `list[int]` | `field(...)` |
| `radiant_xp_adv` | `list[int]` | `field(...)` |
| `combat_log` | `list[CombatLogEntry]` | `field(...)` |
| `chat` | `list[ChatEntry]` | `field(...)` |
| `courier_snapshots` | `list[CourierSnapshot]` | `field(...)` |
| `neutral_item_finds` | `list[NeutralItemFoundEvent]` | `field(...)` |
| `smoke_events` | `list[SmokeEvent]` | `field(...)` |
| `draft` | `list[DraftEvent]` | `field(...)` |
| `teamfights` | `list[Teamfight]` | `field(...)` |
| `opendota_teamfights` | `list[OpenDotaTeamfight]` | `field(...)` |
| `vision_modifiers` | `list[VisionModifierEvent]` | `field(...)` |
| `banner_plants` | `list[BannerPlant]` | `field(...)` |

#### Properties

##### `duration_seconds`

Signature: `def ParsedMatch.duration_seconds(self) -> float`

Game duration in seconds, derived from ``game_start_tick`` and ``game_end_tick``.

Source: [src/gem/results/models.py:668](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L668)

##### `duration_minutes`

Signature: `def ParsedMatch.duration_minutes(self) -> float`

Game duration in minutes, derived from ``game_start_tick`` and ``game_end_tick``.

Source: [src/gem/results/models.py:674](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L674)
