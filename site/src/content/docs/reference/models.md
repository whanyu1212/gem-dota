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
- `ParsedMatch.vision_modifiers`: `list[VisionModifierEvent]` *(experimental)* — evidence-preserving applications of direct reveals, reveal auras, and aura carriers.
- `ParsedMatch.vision_modifier_pairing_issues`: `list[VisionModifierPairingIssue]` *(experimental)* — ambiguous/orphan removal evidence without fabricated applications.
- `ParsedMatch.hero_visibility_events`: `list[HeroVisibilityEvent]` — authoritative,
  change-only visibility states for canonical player heroes, read from each
  team's replay bitset. `unknown` means the replay state was unavailable; it
  does not mean hidden.
- `ParsedMatch.entity_visibility_events`: `list[EntityVisibilityEvent]` —
  identity-safe packet-boundary visibility and active lifecycle for networked
  Dota NPC entities.
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

### `VisibilityState`

```python
class VisibilityState(str, Enum)
```

A team's authoritative visibility state for one hero entity.

Source: [src/gem/results/models.py:33](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L33)

### `HeroVisibilityEvent`

```python
class HeroVisibilityEvent
```

A visibility-state transition for one canonical player hero identity.

Source: [src/gem/results/models.py:50](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L50)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `player_id` | `int` | `-` |
| `hero_name` | `str` | `-` |
| `entity_index` | `int` | `-` |
| `entity_serial` | `int` | `-` |
| `radiant_state` | `VisibilityState` | `-` |
| `dire_state` | `VisibilityState` | `-` |

### `EntityVisibilityEvent`

```python
class EntityVisibilityEvent
```

Packet-boundary visibility evidence for one networked Dota NPC entity.

Source: [src/gem/results/models.py:73](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L73)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `entity_index` | `int` | `-` |
| `entity_serial` | `int` | `-` |
| `class_name` | `str` | `-` |
| `npc_name` | `str` | `-` |
| `team` | `int \| None` | `-` |
| `active` | `bool` | `-` |
| `radiant_state` | `VisibilityState` | `-` |
| `dire_state` | `VisibilityState` | `-` |

### `VisionModifierSemantic`

```python
class VisionModifierSemantic(str, Enum)
```

How a tracked modifier contributes vision evidence.

Source: [src/gem/results/models.py:104](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L104)

### `VisionModifierLifecycleStatus`

```python
class VisionModifierLifecycleStatus(str, Enum)
```

Best-supported lifecycle state for a modifier application.

Source: [src/gem/results/models.py:115](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L115)

### `VisionModifierCloseEvidence`

```python
class VisionModifierCloseEvidence(str, Enum)
```

Evidence supporting the lifecycle close classification.

Source: [src/gem/results/models.py:126](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L126)

### `VisionModifierPairingStatus`

```python
class VisionModifierPairingStatus(str, Enum)
```

Confidence with which a removal was paired to an application.

Source: [src/gem/results/models.py:137](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L137)

### `VisionModifierTeamSource`

```python
class VisionModifierTeamSource(str, Enum)
```

Evidence source used to attribute a modifier participant's team.

Source: [src/gem/results/models.py:148](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L148)

### `VisionModifierEvent`

```python
class VisionModifierEvent
```

One tracked vision-relevant modifier application and its evidence.

Source: [src/gem/results/models.py:159](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L159)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `end_tick` | `int \| None` | `-` |
| `modifier_name` | `str` | `-` |
| `target_name` | `str` | `-` |
| `caster_name` | `str` | `-` |
| `caster_team` | `int` | `-` |
| `semantic` | `VisionModifierSemantic` | `VisionModifierSemantic.DIRECT_TARGET_REVEAL` |
| `lifecycle_status` | `VisionModifierLifecycleStatus` | `VisionModifierLifecycleStatus.OPEN` |
| `close_evidence` | `VisionModifierCloseEvidence` | `VisionModifierCloseEvidence.UNOBSERVED` |
| `pairing_status` | `VisionModifierPairingStatus` | `VisionModifierPairingStatus.EXACT` |
| `target_is_hero` | `bool` | `True` |
| `caster_is_hero` | `bool` | `False` |
| `caster_is_illusion` | `bool` | `False` |
| `target_is_illusion` | `bool` | `False` |
| `caster_is_hero_present` | `bool` | `False` |
| `target_is_hero_present` | `bool` | `False` |
| `caster_is_illusion_present` | `bool` | `False` |
| `target_is_illusion_present` | `bool` | `False` |
| `target_team` | `int` | `0` |
| `caster_team_source` | `VisionModifierTeamSource` | `VisionModifierTeamSource.UNKNOWN` |
| `target_team_source` | `VisionModifierTeamSource` | `VisionModifierTeamSource.UNKNOWN` |
| `add_attacker_team` | `int \| None` | `None` |
| `add_target_team` | `int \| None` | `None` |
| `remove_attacker_team` | `int \| None` | `None` |
| `remove_target_team` | `int \| None` | `None` |
| `add_source` | `CombatLogSource` | `CombatLogSource.UNKNOWN` |
| `remove_source` | `CombatLogSource \| None` | `None` |
| `add_game_time_s` | `int \| None` | `None` |
| `remove_game_time_s` | `int \| None` | `None` |
| `add_modifier_duration_s` | `float \| None` | `None` |
| `remove_modifier_duration_s` | `float \| None` | `None` |
| `add_modifier_elapsed_duration_s` | `float \| None` | `None` |
| `remove_modifier_elapsed_duration_s` | `float \| None` | `None` |
| `add_aura_modifier` | `bool \| None` | `None` |
| `remove_aura_modifier` | `bool \| None` | `None` |
| `remove_modifier_purged` | `bool \| None` | `None` |
| `remove_modifier_purged_duration_s` | `float \| None` | `None` |
| `remove_caster_name` | `str` | `''` |
| `remove_caster_is_hero` | `bool \| None` | `None` |
| `remove_target_is_hero` | `bool \| None` | `None` |
| `remove_caster_is_illusion` | `bool \| None` | `None` |
| `remove_target_is_illusion` | `bool \| None` | `None` |
| `evidence_gaps` | `list[str]` | `field(...)` |

### `VisionModifierPairingIssue`

```python
class VisionModifierPairingIssue
```

Removal evidence that could not be paired to one application safely.

Source: [src/gem/results/models.py:259](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L259)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `reason` | `str` | `-` |
| `modifier_name` | `str` | `-` |
| `caster_name` | `str` | `-` |
| `target_name` | `str` | `-` |
| `source` | `CombatLogSource` | `CombatLogSource.UNKNOWN` |
| `candidate_add_ticks` | `list[int]` | `field(...)` |
| `game_time_s` | `int \| None` | `None` |
| `modifier_duration_s` | `float \| None` | `None` |
| `modifier_elapsed_duration_s` | `float \| None` | `None` |
| `attacker_team` | `int \| None` | `None` |
| `target_team` | `int \| None` | `None` |
| `caster_is_hero` | `bool \| None` | `None` |
| `target_is_hero` | `bool \| None` | `None` |
| `caster_is_illusion` | `bool \| None` | `None` |
| `target_is_illusion` | `bool \| None` | `None` |
| `aura_modifier` | `bool \| None` | `None` |
| `modifier_purged` | `bool \| None` | `None` |
| `modifier_purged_duration_s` | `float \| None` | `None` |

### `SmokeParticipant`

```python
class SmokeParticipant
```

One hero's observed Smoke of Deceit modifier lifecycle.

Source: [src/gem/results/models.py:303](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L303)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `hero_name` | `str` | `-` |
| `player_id` | `int \| None` | `-` |
| `applied_tick` | `int` | `-` |
| `removed_tick` | `int \| None` | `None` |
| `modifier_duration_s` | `float \| None` | `None` |
| `modifier_elapsed_duration_s` | `float \| None` | `None` |
| `applied_x` | `float \| None` | `None` |
| `applied_y` | `float \| None` | `None` |
| `removed_x` | `float \| None` | `None` |
| `removed_y` | `float \| None` | `None` |
| `applied_game_time_s` | `int \| None` | `None` |
| `removed_game_time_s` | `int \| None` | `None` |

### `SmokeEvent`

```python
class SmokeEvent
```

One Smoke of Deceit activation.

Source: [src/gem/results/models.py:342](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L342)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `activator` | `str` | `-` |
| `team` | `int` | `-` |
| `smoked` | `list[str]` | `field(...)` |
| `x` | `float \| None` | `None` |
| `y` | `float \| None` | `None` |
| `activation_x` | `float \| None` | `None` |
| `activation_y` | `float \| None` | `None` |
| `participants` | `list[SmokeParticipant]` | `field(...)` |
| `activation_game_time_s` | `int \| None` | `None` |

### `BuybackEvent`

```python
class BuybackEvent
```

One buyback and its gold cost.

Source: [src/gem/results/models.py:377](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L377)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `player_slot` | `int` | `-` |
| `cost` | `int` | `-` |
| `net_worth` | `int` | `-` |
| `cost_exact` | `bool` | `False` |
| `reliable_gold` | `int \| None` | `None` |
| `unreliable_gold` | `int \| None` | `None` |

### `GoldLedgerSnapshot`

```python
class GoldLedgerSnapshot
```

One reading of a player's gold ledger from the team data entity.

Source: [src/gem/results/models.py:422](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L422)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `game_time_s` | `int` | `-` |
| `hero_kill_gold` | `int` | `0` |
| `creep_kill_gold` | `int` | `0` |
| `neutral_kill_gold` | `int` | `0` |
| `income_gold` | `int` | `0` |
| `building_gold` | `int` | `0` |
| `roshan_gold` | `int` | `0` |
| `bounty_gold` | `int` | `0` |
| `ward_kill_gold` | `int` | `0` |
| `courier_gold` | `int` | `0` |
| `ability_gold` | `int` | `0` |
| `comeback_gold` | `int` | `0` |
| `creep_deny_gold` | `int` | `0` |
| `other_gold` | `int` | `0` |
| `shared_gold` | `int` | `0` |
| `spent_on_items` | `int` | `0` |
| `spent_on_consumables` | `int` | `0` |
| `spent_on_support` | `int` | `0` |
| `spent_on_buybacks` | `int` | `0` |
| `lost_to_death` | `int` | `0` |

### `GoldLedger`

```python
class GoldLedger
```

A player's gold ledger at game end and at every game minute.

Source: [src/gem/results/models.py:492](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L492)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `final` | `GoldLedgerSnapshot \| None` | `None` |
| `per_minute` | `list[GoldLedgerSnapshot]` | `field(...)` |

### `ChatEntry`

```python
class ChatEntry
```

A single chat message from the match.

Source: [src/gem/results/models.py:508](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L508)

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

Source: [src/gem/results/models.py:527](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L527)

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

Source: [src/gem/results/models.py:561](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L561)

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
| `lane_pos` | `dict[str, dict[str, int]]` | `field(...)` |
| `position_log` | `list[tuple[int, float, float]]` | `field(...)` |
| `stuns_dealt` | `float` | `0.0` |
| `kills` | `int` | `0` |
| `deaths` | `int` | `0` |
| `assists` | `int` | `0` |
| `lane` | `int` | `0` |
| `lane_role` | `int` | `0` |
| `is_roaming` | `bool` | `False` |
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
| `game_times_min` | `list[int]` | `field(...)` |
| `aghanims_scepter` | `int \| None` | `None` |
| `aghanims_shard` | `int \| None` | `None` |
| `moonshard` | `int \| None` | `None` |
| `total_earned_xp_t` | `list[int]` | `field(...)` |
| `gold` | `int` | `0` |
| `gold_ledger` | `GoldLedger \| None` | `None` |
| `multi_kills` | `dict[str, int]` | `field(...)` |
| `kill_streaks` | `dict[str, int]` | `field(...)` |
| `killed_by` | `dict[str, int]` | `field(...)` |

### `ParsedMatch`

```python
class ParsedMatch
```

Top-level parsed output for a single Dota 2 replay.

Source: [src/gem/results/models.py:1017](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L1017)

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
| `fights` | `list[Fight]` | `field(...)` |
| `opendota_teamfights` | `list[OpenDotaTeamfight]` | `field(...)` |
| `vision_modifiers` | `list[VisionModifierEvent]` | `field(...)` |
| `banner_plants` | `list[BannerPlant]` | `field(...)` |
| `game_times_min` | `list[int]` | `field(...)` |
| `hero_visibility_events` | `list[HeroVisibilityEvent]` | `field(...)` |
| `vision_modifier_pairing_issues` | `list[VisionModifierPairingIssue]` | `field(...)` |
| `entity_visibility_events` | `list[EntityVisibilityEvent]` | `field(...)` |
| `post_game_tick` | `int \| None` | `None` |
| `game_clock` | `GameClock \| None` | `None` |
| `parse_error` | `str \| None` | `None` |
| `truncated_at_tick` | `int \| None` | `None` |

#### Properties

##### `duration_seconds`

Signature: `def ParsedMatch.duration_seconds(self) -> float`

Game duration in seconds, derived from ``game_start_tick`` and ``game_end_tick``.

Source: [src/gem/results/models.py:1187](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L1187)

##### `duration_minutes`

Signature: `def ParsedMatch.duration_minutes(self) -> float`

Game duration in minutes, derived from ``game_start_tick`` and ``game_end_tick``.

Source: [src/gem/results/models.py:1193](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/models.py#L1193)

## Module `gem.state.game_clock`

Pause-aware conversion between replay ticks and the in-game clock.

Source: [src/gem/state/game_clock.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_clock.py#L1)

### Top-level functions

### `game_clock_for`

```python
def game_clock_for(match: object) -> GameClock
```

Return a match's game clock, or a tick-only fallback for older matches.

Source: [src/gem/state/game_clock.py:186](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_clock.py#L186)

### Top-level classes

### `GamePause`

```python
class GamePause
```

One interval during which the in-game clock was stopped.

Source: [src/gem/state/game_clock.py:40](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_clock.py#L40)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `start_tick` | `int` | `-` |
| `end_tick` | `int \| None` | `-` |

#### Properties

##### `duration_ticks`

Signature: `def GamePause.duration_ticks(self) -> int | None`

Paused length in ticks, or ``None`` for a pause that never ended.

Source: [src/gem/state/game_clock.py:53](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_clock.py#L53)

### `GameClock`

```python
class GameClock
```

Maps replay ticks to pause-aware in-game time and back.

Source: [src/gem/state/game_clock.py:61](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_clock.py#L61)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `game_start_tick` | `int \| None` | `None` |
| `pauses` | `list[GamePause]` | `field(...)` |
| `game_start_time_s` | `float \| None` | `None` |
| `net_tick_offset` | `int` | `0` |

#### Methods

##### `paused_ticks_before`

Signature: `def GameClock.paused_ticks_before(self, tick: int) -> int`

Return how many ticks of pause elapsed before ``tick``.

Source: [src/gem/state/game_clock.py:84](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_clock.py#L84)

##### `game_time_at`

Signature: `def GameClock.game_time_at(self, tick: int) -> float | None`

Return the exact in-game clock reading at a replay tick.

Source: [src/gem/state/game_clock.py:109](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_clock.py#L109)

##### `game_seconds_at`

Signature: `def GameClock.game_seconds_at(self, tick: int) -> int | None`

Return whole in-game seconds at a replay tick, as OpenDota reports them.

Source: [src/gem/state/game_clock.py:124](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_clock.py#L124)

##### `tick_at`

Signature: `def GameClock.tick_at(self, game_time_s: float) -> int | None`

Return the first replay tick at which the in-game clock reads a time.

Source: [src/gem/state/game_clock.py:146](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_clock.py#L146)

##### `format_tick`

Signature: `def GameClock.format_tick(self, tick: int) -> str`

Format a replay tick as the in-game clock (``MM:SS``, ``-MM:SS`` pre-horn).

Source: [src/gem/state/game_clock.py:169](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_clock.py#L169)

### `GameClockTracker`

```python
class GameClockTracker
```

Builds the in-game clock while a replay is parsed.

Source: [src/gem/state/game_clock.py:239](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_clock.py#L239)

#### Methods

##### `on_net_tick`

Signature: `def GameClockTracker.on_net_tick(self, net_tick: int) -> None`

Record a ``CNETMsg_Tick``.

Source: [src/gem/state/game_clock.py:288](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_clock.py#L288)

##### `net_tick_offset`

Signature: `def GameClockTracker.net_tick_offset(self, tick: int) -> int`

Return ``net_tick - tick``, or 0 before any network tick.

Source: [src/gem/state/game_clock.py:293](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_clock.py#L293)

##### `update`

Signature: `def GameClockTracker.update(self, entity: Entity, tick: int) -> None`

Refresh the clock from the ``CDOTAGamerulesProxy`` entity.

Source: [src/gem/state/game_clock.py:297](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_clock.py#L297)

##### `snapshot_tick_start`

Signature: `def GameClockTracker.snapshot_tick_start(self, entity: Entity | None) -> None`

Record OpenDota's running clock at the start of an outer replay tick.

Source: [src/gem/state/game_clock.py:328](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_clock.py#L328)

##### `observe_game_start`

Signature: `def GameClockTracker.observe_game_start(self, entity: Entity, tick: int) -> bool`

Refresh the clock, and report whether the game has just started.

Source: [src/gem/state/game_clock.py:352](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_clock.py#L352)

##### `track_pause`

Signature: `def GameClockTracker.track_pause(self, paused: bool, pause_start_net_tick: int | None, total_paused_ticks: int | None, tick: int) -> None`

Record pause intervals from ``m_bGamePaused`` transitions.

Source: [src/gem/state/game_clock.py:377](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_clock.py#L377)

##### `combat_log_time`

Signature: `def GameClockTracker.combat_log_time(self, timestamp: float | None, game_state: int | None) -> int | None`

Return OpenDota-style game-relative time for a combat-log entry.

Source: [src/gem/state/game_clock.py:413](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_clock.py#L413)

##### `finish`

Signature: `def GameClockTracker.finish(self) -> None`

Close a pause still open when the replay ends.

Source: [src/gem/state/game_clock.py:443](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/game_clock.py#L443)

## Module `gem.results.serialization`

JSON serialization and deserialization for :class:`ParsedMatch`.

Source: [src/gem/results/serialization.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/serialization.py#L1)

### Top-level functions

### `to_dict`

```python
def to_dict(value: Any) -> Any
```

Convert a supported dataclass or nested value to JSON-compatible data.

Source: [src/gem/results/serialization.py:63](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/serialization.py#L63)

### `to_json`

```python
def to_json(match: ParsedMatch, *, analysis: MatchAnalysis | None = None, indent: int | None = None, sort_keys: bool = False) -> str
```

Serialize a :class:`ParsedMatch` to a JSON string.

Source: [src/gem/results/serialization.py:82](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/serialization.py#L82)

### `from_dict`

```python
def from_dict(data: Mapping[str, Any]) -> ParsedMatch
```

Rebuild a :class:`ParsedMatch` from :func:`to_json` or :func:`to_dict` data.

Source: [src/gem/results/serialization.py:117](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/serialization.py#L117)

### `load_json`

```python
def load_json(path: str | Path) -> ParsedMatch
```

Load a :class:`ParsedMatch` from a JSON file written by :func:`to_json`.

Source: [src/gem/results/serialization.py:171](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/serialization.py#L171)
