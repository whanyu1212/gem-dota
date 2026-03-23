# dota_scenariomessages.proto

- Module: `dota_scenariomessages_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **1**
- Messages: **23** (top-level: 7)
- Enums: **0** (top-level: 0)

## Imports

- `dota_shared_enums.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CScenario_Position</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `x` | `float` | `optional` | `` |  |
| 2 | `y` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CScenarioGame_RoshanSpawner</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `kill_count` | `int32` | `optional` | `` |  |
| 2 | `state` | `int32` | `optional` | `` |  |
| 3 | `cooldown` | `float` | `optional` | `` |  |
| 4 | `killer_team` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CScenarioEnt_Courier</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team_number` | `int32` | `optional` | `` |  |
| 2 | `owner_player_id` | `int32` | `optional` | `` | default = -1 |
| 3 | `cooldown` | `float` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CScenarioEnt_NPC</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `position` | `.CScenario_Position` | `optional` | `` |  |
| 2 | `unit_name` | `string` | `optional` | `` |  |
| 3 | `team_number` | `int32` | `optional` | `` |  |
| 4 | `health_frac` | `float` | `optional` | `` | default = 1 |
| 10 | `owning_camp` | `string` | `optional` | `` |  |
| 11 | `owning_camp_position` | `.CScenario_Position` | `optional` | `` |  |
| 20 | `invade_goal` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CScenarioEnt_SpiritBear</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `owner_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `team_id` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CScenarioEnt_DroppedItem</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `position` | `.CScenario_Position` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDotaScenario</code> — fields: 9; oneofs: 0; nested messages: 16; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `lobby_id` | `uint64` | `optional` | `` |  |
| 2 | `game` | `.CMsgDotaScenario.Game` | `optional` | `` |  |
| 3 | `teams` | `.CMsgDotaScenario.Team` | `repeated` | `` |  |
| 4 | `heroes` | `.CMsgDotaScenario.Hero` | `repeated` | `` |  |
| 5 | `stock` | `.CMsgDotaScenario.Stock` | `repeated` | `` |  |
| 6 | `buildings` | `.CMsgDotaScenario.Building` | `repeated` | `` |  |
| 7 | `entities` | `.CMsgDotaScenario.Entity` | `repeated` | `` |  |
| 8 | `items` | `.CMsgDotaScenario.Item` | `repeated` | `` |  |
| 9 | `modifiers` | `.CMsgDotaScenario.Modifier` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDotaScenario.EntityRef</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDotaScenario`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `neutral_stash_id` | `int32` | `optional` | `` | default = -1 |
| 3 | `entity_idx` | `int32` | `optional` | `` | default = -1 |
| 4 | `roshan` | `bool` | `optional` | `` | default = false |
| 10 | `ability_name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDotaScenario.Game</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDotaScenario`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `game_mode` | `int32` | `optional` | `` |  |
| 3 | `clock_time` | `float` | `optional` | `` |  |
| 4 | `internal_time` | `float` | `optional` | `` |  |
| 5 | `roshan` | `.CScenarioGame_RoshanSpawner` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDotaScenario.TeamNeutralItem</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDotaScenario`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `consumed` | `bool` | `optional` | `` |  |
| 3 | `tier` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDotaScenario.Team</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDotaScenario`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team_number` | `int32` | `optional` | `` |  |
| 2 | `neutral_items` | `.CMsgDotaScenario.TeamNeutralItem` | `repeated` | `` |  |
| 3 | `hero_kills` | `int32` | `optional` | `` |  |
| 4 | `tower_kills` | `int32` | `optional` | `` |  |
| 5 | `barracks_kills` | `int32` | `optional` | `` |  |
| 6 | `glyph_cooldown` | `float` | `optional` | `` |  |
| 7 | `radar_cooldown` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDotaScenario.HeroHeroInt</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDotaScenario`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `value` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDotaScenario.HeroHeroFloat</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDotaScenario`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `value` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDotaScenario.DamageStatsByType</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDotaScenario`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `damage_type` | `int32` | `optional` | `` |  |
| 2 | `received_pre_reduction` | `float` | `optional` | `` |  |
| 3 | `received_post_reduction` | `float` | `optional` | `` |  |
| 4 | `outgoing_pre_reduction` | `float` | `optional` | `` |  |
| 5 | `outgoing_post_reduction` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDotaScenario.HeroAbility</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDotaScenario`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `level` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDotaScenario.HeroNeutralChoice</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDotaScenario`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `choice_index` | `int32` | `optional` | `` |  |
| 2 | `artifact_name` | `string` | `optional` | `` |  |
| 3 | `enchantment_name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDotaScenario.HeroNeutralTier</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDotaScenario`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `tier` | `uint32` | `optional` | `` |  |
| 2 | `choices` | `.CMsgDotaScenario.HeroNeutralChoice` | `repeated` | `` |  |
| 3 | `selected_artifact` | `int32` | `optional` | `` |  |
| 4 | `selected_enchantment` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDotaScenario.Hero</code> — fields: 68; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDotaScenario`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steam_id` | `fixed64` | `optional` | `` |  |
| 2 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 3 | `team_id` | `int32` | `optional` | `` |  |
| 4 | `hero` | `string` | `optional` | `` |  |
| 5 | `total_xp` | `int32` | `optional` | `` |  |
| 6 | `bkb_charges_used` | `int32` | `optional` | `` |  |
| 7 | `aeon_charges_used` | `int32` | `optional` | `` |  |
| 8 | `reliable_gold` | `int32` | `optional` | `` |  |
| 9 | `unreliable_gold` | `int32` | `optional` | `` |  |
| 10 | `total_earned_gold` | `int32` | `optional` | `` |  |
| 11 | `shared_gold` | `int32` | `optional` | `` |  |
| 12 | `hero_kill_gold` | `int32` | `optional` | `` |  |
| 13 | `creep_kill_gold` | `int32` | `optional` | `` |  |
| 14 | `neutral_kill_gold` | `int32` | `optional` | `` |  |
| 15 | `courier_gold` | `int32` | `optional` | `` |  |
| 16 | `bounty_gold` | `int32` | `optional` | `` |  |
| 17 | `roshan_gold` | `int32` | `optional` | `` |  |
| 18 | `building_gold` | `int32` | `optional` | `` |  |
| 19 | `other_gold` | `int32` | `optional` | `` |  |
| 26 | `income_gold` | `int32` | `optional` | `` |  |
| 27 | `ward_kill_gold` | `int32` | `optional` | `` |  |
| 28 | `ability_gold` | `int32` | `optional` | `` |  |
| 29 | `denies` | `int32` | `optional` | `` |  |
| 30 | `last_hits` | `int32` | `optional` | `` |  |
| 31 | `last_hit_streak` | `int32` | `optional` | `` |  |
| 32 | `last_hit_multikill` | `int32` | `optional` | `` |  |
| 33 | `nearby_creep_death_count` | `int32` | `optional` | `` |  |
| 34 | `claimed_deny_count` | `int32` | `optional` | `` |  |
| 35 | `claimed_miss_count` | `int32` | `optional` | `` |  |
| 36 | `miss_count` | `int32` | `optional` | `` |  |
| 40 | `buyback_cooldown_time` | `float` | `optional` | `` |  |
| 41 | `buyback_gold_limit_time` | `float` | `optional` | `` |  |
| 44 | `stun_duration` | `float` | `optional` | `` |  |
| 45 | `healing` | `float` | `optional` | `` |  |
| 46 | `tower_kills` | `int32` | `optional` | `` |  |
| 47 | `roshan_kills` | `int32` | `optional` | `` |  |
| 48 | `observer_wards_placed` | `int32` | `optional` | `` |  |
| 49 | `sentry_wards_placed` | `int32` | `optional` | `` |  |
| 50 | `creeps_stacked` | `int32` | `optional` | `` |  |
| 51 | `camps_stacked` | `int32` | `optional` | `` |  |
| 52 | `rune_pickups` | `int32` | `optional` | `` |  |
| 53 | `gold_spent_on_support` | `int32` | `optional` | `` |  |
| 54 | `hero_damage` | `float` | `optional` | `` |  |
| 55 | `wards_purchased` | `int32` | `optional` | `` |  |
| 56 | `wards_destroyed` | `int32` | `optional` | `` |  |
| 58 | `gold_spent_on_consumables` | `int32` | `optional` | `` |  |
| 59 | `gold_spent_on_items` | `int32` | `optional` | `` |  |
| 60 | `gold_spent_on_buybacks` | `int32` | `optional` | `` |  |
| 61 | `gold_lost_to_death` | `int32` | `optional` | `` |  |
| 62 | `kills` | `int32` | `optional` | `` |  |
| 63 | `assists` | `int32` | `optional` | `` |  |
| 64 | `deaths` | `int32` | `optional` | `` |  |
| 65 | `kill_streak` | `int32` | `optional` | `` |  |
| 68 | `respawn_seconds` | `int32` | `optional` | `` | default = -1 |
| 69 | `last_buyback_time` | `int32` | `optional` | `` |  |
| 71 | `first_blood_claimed` | `bool` | `optional` | `` |  |
| 72 | `first_blood_given` | `bool` | `optional` | `` |  |
| 73 | `bounty_runes` | `int32` | `optional` | `` |  |
| 74 | `outposts_captured` | `int32` | `optional` | `` |  |
| 75 | `position` | `.CScenario_Position` | `optional` | `` |  |
| 150 | `enemy_kills` | `.CMsgDotaScenario.HeroHeroInt` | `repeated` | `` |  |
| 151 | `damage_stats` | `.CMsgDotaScenario.DamageStatsByType` | `repeated` | `` |  |
| 152 | `abilities` | `.CMsgDotaScenario.HeroAbility` | `repeated` | `` |  |
| 153 | `hero_facet` | `uint32` | `optional` | `` |  |
| 154 | `total_madstone` | `uint32` | `optional` | `` |  |
| 155 | `current_madstone` | `uint32` | `optional` | `` |  |
| 156 | `neutral_tiers` | `.CMsgDotaScenario.HeroNeutralTier` | `repeated` | `` |  |
| 157 | `refresher_charges_used` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDotaScenario.Stock</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDotaScenario`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `team_number` | `int32` | `optional` | `` | default = -1 |
| 3 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 4 | `current_stock` | `int32` | `optional` | `` |  |
| 5 | `cooldown` | `float` | `optional` | `` |  |
| 6 | `bonus_stock` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDotaScenario.Building</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDotaScenario`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `entity_name` | `string` | `optional` | `` |  |
| 2 | `entity_class` | `string` | `optional` | `` |  |
| 3 | `team_id` | `int32` | `optional` | `` |  |
| 4 | `is_destroyed` | `bool` | `optional` | `` |  |
| 5 | `health_frac` | `float` | `optional` | `` | default = 1 |

</details>

<details>
<summary><code>CMsgDotaScenario.Entity</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDotaScenario`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `courier` | `.CScenarioEnt_Courier` | `optional` | `` |  |
| 2 | `npc` | `.CScenarioEnt_NPC` | `optional` | `` |  |
| 3 | `spirit_bear` | `.CScenarioEnt_SpiritBear` | `optional` | `` |  |
| 4 | `dropped_item` | `.CScenarioEnt_DroppedItem` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDotaScenario.Item</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDotaScenario`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `location` | `.CMsgDotaScenario.EntityRef` | `optional` | `` |  |
| 3 | `owner_id` | `int32` | `optional` | `` | default = -1 |
| 4 | `item_slot` | `int32` | `optional` | `` |  |
| 5 | `neutral_drop_team` | `int32` | `optional` | `` |  |
| 6 | `charges` | `int32` | `optional` | `` |  |
| 7 | `secondary_charges` | `int32` | `optional` | `` |  |
| 8 | `lifetime` | `float` | `optional` | `` | default = -1 |
| 9 | `stored_rune_type` | `int32` | `optional` | `` | default = -1 |
| 10 | `level` | `int32` | `optional` | `` | default = 1 |

</details>

<details>
<summary><code>CMsgDotaScenario.Modifier</code> — fields: 16; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDotaScenario`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `parent` | `.CMsgDotaScenario.EntityRef` | `optional` | `` |  |
| 3 | `caster` | `.CMsgDotaScenario.EntityRef` | `optional` | `` |  |
| 4 | `ability` | `.CMsgDotaScenario.EntityRef` | `optional` | `` |  |
| 5 | `duration` | `float` | `optional` | `` | default = -1 |
| 6 | `lifetime_remaining` | `float` | `optional` | `` | default = 0 |
| 7 | `stack_count` | `int32` | `optional` | `` |  |
| 8 | `create_even_if_existing` | `bool` | `optional` | `` |  |
| 9 | `create_without_caster` | `bool` | `optional` | `` |  |
| 10 | `create_without_ability` | `bool` | `optional` | `` |  |
| 100 | `moonshard_consumed_bonus` | `int32` | `optional` | `` |  |
| 101 | `moonshard_consumed_bonus_night_vision` | `int32` | `optional` | `` |  |
| 110 | `wardtruesight_range` | `int32` | `optional` | `` |  |
| 120 | `ultimate_scepter_consumed_alchemist_bonus_all_stats` | `int32` | `optional` | `` |  |
| 121 | `ultimate_scepter_consumed_alchemist_bonus_health` | `int32` | `optional` | `` |  |
| 122 | `ultimate_scepter_consumed_alchemist_bonus_mana` | `int32` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

*(No enums in this proto file.)*
