# dota_gcmessages_common_bot_script.proto

- Module: `dota_gcmessages_common_bot_script_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **1**
- Messages: **18** (top-level: 1)
- Enums: **2** (top-level: 0)

## Imports

- `valveextensions.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgBotWorldState</code> — fields: 23; oneofs: 0; nested messages: 17; nested enums: 2</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team_id` | `uint32` | `optional` | `` |  |
| 2 | `game_time` | `float` | `optional` | `` |  |
| 3 | `dota_time` | `float` | `optional` | `` |  |
| 4 | `game_state` | `uint32` | `optional` | `` |  |
| 5 | `hero_pick_state` | `uint32` | `optional` | `` |  |
| 6 | `time_of_day` | `float` | `optional` | `` |  |
| 7 | `glyph_cooldown` | `float` | `optional` | `` |  |
| 8 | `glyph_cooldown_enemy` | `float` | `optional` | `` |  |
| 10 | `players` | `.CMsgBotWorldState.Player` | `repeated` | `` | (valve_map_field) = true |
| 11 | `units` | `.CMsgBotWorldState.Unit` | `repeated` | `` | (valve_map_field) = true |
| 12 | `dropped_items` | `.CMsgBotWorldState.DroppedItem` | `repeated` | `` | (diff_encode_field) = 112 |
| 13 | `rune_infos` | `.CMsgBotWorldState.RuneInfo` | `repeated` | `` | (diff_encode_field) = 113 |
| 14 | `incoming_teleports` | `.CMsgBotWorldState.TeleportInfo` | `repeated` | `` |  |
| 15 | `linear_projectiles` | `.CMsgBotWorldState.LinearProjectile` | `repeated` | `` | (valve_map_field) = true |
| 16 | `avoidance_zones` | `.CMsgBotWorldState.AvoidanceZone` | `repeated` | `` |  |
| 17 | `couriers` | `.CMsgBotWorldState.Courier` | `repeated` | `` | (valve_map_field) = true |
| 20 | `ability_events` | `.CMsgBotWorldState.EventAbility` | `repeated` | `` |  |
| 21 | `damage_events` | `.CMsgBotWorldState.EventDamage` | `repeated` | `` |  |
| 22 | `courier_killed_events` | `.CMsgBotWorldState.EventCourierKilled` | `repeated` | `` |  |
| 23 | `roshan_killed_events` | `.CMsgBotWorldState.EventRoshanKilled` | `repeated` | `` |  |
| 24 | `tree_events` | `.CMsgBotWorldState.EventTree` | `repeated` | `` |  |
| 112 | `dropped_items_deltas` | `int32` | `repeated` | `` |  |
| 113 | `rune_infos_deltas` | `int32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgBotWorldState.Vector</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgBotWorldState`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `x` | `float` | `optional` | `` |  |
| 2 | `y` | `float` | `optional` | `` |  |
| 3 | `z` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgBotWorldState.Player</code> — fields: 11; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgBotWorldState`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | (valve_map_key) = true |
| 2 | `hero_id` | `int32` | `optional` | `` |  |
| 3 | `is_alive` | `bool` | `optional` | `` |  |
| 4 | `respawn_time` | `float` | `optional` | `` |  |
| 5 | `kills` | `uint32` | `optional` | `` |  |
| 6 | `deaths` | `uint32` | `optional` | `` |  |
| 7 | `assists` | `uint32` | `optional` | `` |  |
| 8 | `team_id` | `uint32` | `optional` | `` |  |
| 9 | `primary_unit_handle` | `uint32` | `optional` | `` | default = 4294967295 |
| 10 | `mmr` | `int32` | `optional` | `` |  |
| 11 | `location` | `.CMsgBotWorldState.Vector` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgBotWorldState.Ability</code> — fields: 18; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgBotWorldState`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `handle` | `uint32` | `optional` | `` | (valve_map_key) = true |
| 2 | `ability_id` | `int32` | `optional` | `` | default = -1 |
| 3 | `slot` | `uint32` | `optional` | `` |  |
| 5 | `caster_handle` | `uint32` | `optional` | `` | default = 4294967295 |
| 6 | `level` | `uint32` | `optional` | `` |  |
| 10 | `cast_range` | `uint32` | `optional` | `` |  |
| 11 | `channel_time` | `float` | `optional` | `` |  |
| 12 | `cooldown_remaining` | `float` | `optional` | `` | default = 0 |
| 20 | `is_activated` | `bool` | `optional` | `` |  |
| 21 | `is_toggled` | `bool` | `optional` | `` |  |
| 22 | `is_in_ability_phase` | `bool` | `optional` | `` |  |
| 23 | `is_channeling` | `bool` | `optional` | `` |  |
| 24 | `is_stolen` | `bool` | `optional` | `` |  |
| 25 | `is_fully_castable` | `bool` | `optional` | `` |  |
| 30 | `charges` | `uint32` | `optional` | `` |  |
| 31 | `secondary_charges` | `uint32` | `optional` | `` |  |
| 40 | `is_combined_locked` | `bool` | `optional` | `` |  |
| 50 | `power_treads_stat` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CMsgBotWorldState.DroppedItem</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgBotWorldState`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `location` | `.CMsgBotWorldState.Vector` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgBotWorldState.RuneInfo</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgBotWorldState`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `type` | `int32` | `optional` | `` |  |
| 2 | `location` | `.CMsgBotWorldState.Vector` | `optional` | `` |  |
| 3 | `status` | `uint32` | `optional` | `` |  |
| 4 | `time_since_seen` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgBotWorldState.TeleportInfo</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgBotWorldState`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` |  |
| 2 | `location` | `.CMsgBotWorldState.Vector` | `optional` | `` |  |
| 3 | `time_remaining` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgBotWorldState.Modifier</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgBotWorldState`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `stack_count` | `uint32` | `optional` | `` |  |
| 3 | `ability_handle` | `uint32` | `optional` | `` | default = 4294967295 |
| 4 | `ability_id` | `int32` | `optional` | `` | default = -1 |
| 5 | `remaining_duration` | `float` | `optional` | `` |  |
| 6 | `auxiliary_units_handles` | `uint32` | `repeated` | `` |  |
| 7 | `handle` | `uint32` | `optional` | `` | (valve_map_key) = true |

</details>

<details>
<summary><code>CMsgBotWorldState.LinearProjectile</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgBotWorldState`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `handle` | `uint32` | `optional` | `` | (valve_map_key) = true |
| 2 | `caster_handle` | `uint32` | `optional` | `` | default = 4294967295 |
| 3 | `caster_player_id` | `int32` | `optional` | `` |  |
| 4 | `ability_handle` | `uint32` | `optional` | `` | default = 4294967295 |
| 5 | `ability_id` | `int32` | `optional` | `` | default = -1 |
| 6 | `location` | `.CMsgBotWorldState.Vector` | `optional` | `` |  |
| 7 | `velocity` | `.CMsgBotWorldState.Vector` | `optional` | `` |  |
| 8 | `radius` | `uint32` | `optional` | `` |  |
| 9 | `caster_unit_type` | `.CMsgBotWorldState.UnitType` | `optional` | `` | default = INVALID |

</details>

<details>
<summary><code>CMsgBotWorldState.TrackingProjectile</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgBotWorldState`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `caster_handle` | `uint32` | `optional` | `` | default = 4294967295 |
| 2 | `caster_player_id` | `int32` | `optional` | `` |  |
| 3 | `ability_handle` | `uint32` | `optional` | `` | default = 4294967295 |
| 4 | `ability_id` | `int32` | `optional` | `` | default = -1 |
| 5 | `location` | `.CMsgBotWorldState.Vector` | `optional` | `` |  |
| 6 | `velocity` | `uint32` | `optional` | `` |  |
| 7 | `is_dodgeable` | `bool` | `optional` | `` |  |
| 8 | `is_attack` | `bool` | `optional` | `` |  |
| 9 | `caster_unit_type` | `.CMsgBotWorldState.UnitType` | `optional` | `` | default = INVALID |
| 10 | `handle` | `uint32` | `optional` | `` | (valve_map_key) = true |

</details>

<details>
<summary><code>CMsgBotWorldState.AvoidanceZone</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgBotWorldState`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `location` | `.CMsgBotWorldState.Vector` | `optional` | `` |  |
| 2 | `caster_handle` | `uint32` | `optional` | `` | default = 4294967295 |
| 3 | `caster_player_id` | `int32` | `optional` | `` |  |
| 4 | `ability_handle` | `uint32` | `optional` | `` | default = 4294967295 |
| 5 | `ability_id` | `int32` | `optional` | `` | default = -1 |
| 6 | `radius` | `uint32` | `optional` | `` |  |
| 7 | `caster_unit_type` | `.CMsgBotWorldState.UnitType` | `optional` | `` | default = INVALID |

</details>

<details>
<summary><code>CMsgBotWorldState.Courier</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgBotWorldState`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `handle` | `uint32` | `optional` | `` | (valve_map_key) = true |
| 2 | `state` | `.CMsgBotWorldState.CourierState` | `optional` | `` | default = COURIER_STATE_INIT |
| 3 | `player_id` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgBotWorldState.EventAbility</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgBotWorldState`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ability_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `player_id` | `int32` | `optional` | `` |  |
| 3 | `unit_handle` | `uint32` | `optional` | `` | default = 4294967295 |
| 4 | `location` | `.CMsgBotWorldState.Vector` | `optional` | `` |  |
| 5 | `is_channel_start` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgBotWorldState.EventDamage</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgBotWorldState`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `damage` | `uint32` | `optional` | `` |  |
| 2 | `victim_player_id` | `int32` | `optional` | `` |  |
| 3 | `victim_unit_handle` | `uint32` | `optional` | `` | default = 4294967295 |
| 4 | `attacker_player_id` | `int32` | `optional` | `` |  |
| 5 | `attacker_unit_handle` | `uint32` | `optional` | `` | default = 4294967295 |
| 6 | `ability_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CMsgBotWorldState.EventCourierKilled</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgBotWorldState`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team_id` | `uint32` | `optional` | `` |  |
| 2 | `courier_unit_handle` | `uint32` | `optional` | `` | default = 4294967295 |
| 3 | `killer_player_id` | `int32` | `optional` | `` |  |
| 4 | `killer_unit_handle` | `uint32` | `optional` | `` | default = 4294967295 |

</details>

<details>
<summary><code>CMsgBotWorldState.EventRoshanKilled</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgBotWorldState`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `killer_player_id` | `int32` | `optional` | `` |  |
| 2 | `killer_unit_handle` | `uint32` | `optional` | `` | default = 4294967295 |

</details>

<details>
<summary><code>CMsgBotWorldState.EventTree</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgBotWorldState`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `tree_id` | `uint32` | `optional` | `` |  |
| 2 | `destroyed` | `bool` | `optional` | `` |  |
| 3 | `respawned` | `bool` | `optional` | `` |  |
| 4 | `location` | `.CMsgBotWorldState.Vector` | `optional` | `` |  |
| 5 | `delayed` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgBotWorldState.Unit</code> — fields: 91; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgBotWorldState`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `handle` | `uint32` | `optional` | `` | (valve_map_key) = true |
| 2 | `unit_type` | `.CMsgBotWorldState.UnitType` | `optional` | `` | default = INVALID |
| 3 | `name` | `string` | `optional` | `` |  |
| 4 | `team_id` | `uint32` | `optional` | `` |  |
| 5 | `level` | `uint32` | `optional` | `` |  |
| 6 | `location` | `.CMsgBotWorldState.Vector` | `optional` | `` |  |
| 7 | `is_alive` | `bool` | `optional` | `` |  |
| 8 | `player_id` | `int32` | `optional` | `` |  |
| 10 | `bounding_radius` | `int32` | `optional` | `` |  |
| 11 | `facing` | `int32` | `optional` | `` |  |
| 12 | `ground_height` | `uint32` | `optional` | `` |  |
| 15 | `vision_range_daytime` | `uint32` | `optional` | `` |  |
| 16 | `vision_range_nighttime` | `uint32` | `optional` | `` |  |
| 20 | `health` | `int32` | `optional` | `` |  |
| 21 | `health_max` | `int32` | `optional` | `` |  |
| 22 | `health_regen` | `float` | `optional` | `` |  |
| 25 | `mana` | `int32` | `optional` | `` |  |
| 26 | `mana_max` | `int32` | `optional` | `` |  |
| 27 | `mana_regen` | `float` | `optional` | `` |  |
| 30 | `base_movement_speed` | `int32` | `optional` | `` |  |
| 31 | `current_movement_speed` | `int32` | `optional` | `` |  |
| 35 | `anim_activity` | `int32` | `optional` | `` |  |
| 36 | `anim_cycle` | `float` | `optional` | `` |  |
| 40 | `base_damage` | `int32` | `optional` | `` |  |
| 41 | `base_damage_variance` | `int32` | `optional` | `` |  |
| 42 | `bonus_damage` | `int32` | `optional` | `` |  |
| 43 | `attack_damage` | `int32` | `optional` | `` |  |
| 44 | `attack_range` | `int32` | `optional` | `` |  |
| 45 | `attack_speed` | `float` | `optional` | `` |  |
| 46 | `attack_anim_point` | `float` | `optional` | `` |  |
| 47 | `attack_acquisition_range` | `int32` | `optional` | `` |  |
| 48 | `attack_projectile_speed` | `int32` | `optional` | `` |  |
| 49 | `attack_target_handle` | `uint32` | `optional` | `` | default = 4294967295 |
| 50 | `attacks_per_second` | `int32` | `optional` | `` | default = -1 |
| 51 | `last_attack_time` | `float` | `optional` | `` | default = -1 |
| 52 | `attack_target_name` | `string` | `optional` | `` |  |
| 60 | `bounty_xp` | `uint32` | `optional` | `` |  |
| 61 | `bounty_gold_min` | `uint32` | `optional` | `` |  |
| 62 | `bounty_gold_max` | `uint32` | `optional` | `` |  |
| 65 | `is_channeling` | `bool` | `optional` | `` |  |
| 66 | `active_ability_handle` | `uint32` | `optional` | `` | default = 4294967295 |
| 70 | `is_attack_immune` | `bool` | `optional` | `` |  |
| 71 | `is_blind` | `bool` | `optional` | `` |  |
| 72 | `is_block_disabled` | `bool` | `optional` | `` |  |
| 73 | `is_disarmed` | `bool` | `optional` | `` |  |
| 74 | `is_dominated` | `bool` | `optional` | `` |  |
| 75 | `is_evade_disabled` | `bool` | `optional` | `` |  |
| 76 | `is_hexed` | `bool` | `optional` | `` |  |
| 77 | `is_invisible` | `bool` | `optional` | `` |  |
| 78 | `is_invulnerable` | `bool` | `optional` | `` |  |
| 79 | `is_magic_immune` | `bool` | `optional` | `` |  |
| 80 | `is_muted` | `bool` | `optional` | `` |  |
| 82 | `is_nightmared` | `bool` | `optional` | `` |  |
| 83 | `is_rooted` | `bool` | `optional` | `` |  |
| 84 | `is_silenced` | `bool` | `optional` | `` |  |
| 85 | `is_specially_deniable` | `bool` | `optional` | `` |  |
| 86 | `is_stunned` | `bool` | `optional` | `` |  |
| 87 | `is_unable_to_miss` | `bool` | `optional` | `` |  |
| 88 | `has_scepter` | `bool` | `optional` | `` |  |
| 90 | `abilities` | `.CMsgBotWorldState.Ability` | `repeated` | `` | (valve_map_field) = true |
| 91 | `items` | `.CMsgBotWorldState.Ability` | `repeated` | `` | (valve_map_field) = true |
| 92 | `modifiers` | `.CMsgBotWorldState.Modifier` | `repeated` | `` | (valve_map_field) = true |
| 93 | `incoming_tracking_projectiles` | `.CMsgBotWorldState.TrackingProjectile` | `repeated` | `` | (valve_map_field) = true |
| 94 | `is_specially_undeniable` | `bool` | `optional` | `` |  |
| 100 | `action_type` | `uint32` | `optional` | `` |  |
| 101 | `ability_target_handle` | `uint32` | `optional` | `` | default = 4294967295 |
| 102 | `is_using_ability` | `bool` | `optional` | `` |  |
| 103 | `ability_target_name` | `string` | `optional` | `` |  |
| 110 | `primary_attribute` | `uint32` | `optional` | `` |  |
| 111 | `is_illusion` | `bool` | `optional` | `` |  |
| 112 | `respawn_time` | `float` | `optional` | `` |  |
| 113 | `buyback_cost` | `uint32` | `optional` | `` |  |
| 114 | `buyback_cooldown` | `float` | `optional` | `` |  |
| 115 | `spell_amplification` | `float` | `optional` | `` |  |
| 116 | `armor` | `float` | `optional` | `` |  |
| 117 | `magic_resist` | `float` | `optional` | `` |  |
| 118 | `evasion` | `float` | `optional` | `` |  |
| 120 | `xp_needed_to_level` | `uint32` | `optional` | `` |  |
| 121 | `ability_points` | `uint32` | `optional` | `` |  |
| 122 | `reliable_gold` | `int32` | `optional` | `` | default = -1 |
| 123 | `unreliable_gold` | `int32` | `optional` | `` | default = -1 |
| 124 | `last_hits` | `uint32` | `optional` | `` |  |
| 125 | `denies` | `uint32` | `optional` | `` |  |
| 126 | `net_worth` | `uint32` | `optional` | `` |  |
| 127 | `strength` | `uint32` | `optional` | `` |  |
| 128 | `agility` | `uint32` | `optional` | `` |  |
| 129 | `intelligence` | `uint32` | `optional` | `` |  |
| 130 | `remaining_lifespan` | `float` | `optional` | `` |  |
| 140 | `flying_courier` | `bool` | `optional` | `` |  |
| 150 | `shrine_cooldown` | `float` | `optional` | `` |  |
| 151 | `is_shrine_healing` | `bool` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>CMsgBotWorldState.UnitType</code> — values: 13</summary>

- Parent: `CMsgBotWorldState`

| Name | Number |
|---|---:|
| `INVALID` | 0 |
| `HERO` | 1 |
| `CREEP_HERO` | 2 |
| `LANE_CREEP` | 3 |
| `JUNGLE_CREEP` | 4 |
| `ROSHAN` | 5 |
| `TOWER` | 6 |
| `BARRACKS` | 7 |
| `SHRINE` | 8 |
| `FORT` | 9 |
| `BUILDING` | 10 |
| `COURIER` | 11 |
| `WARD` | 12 |

</details>

<details>
<summary><code>CMsgBotWorldState.CourierState</code> — values: 9</summary>

- Parent: `CMsgBotWorldState`

| Name | Number |
|---|---:|
| `COURIER_STATE_INIT` | -1 |
| `COURIER_STATE_IDLE` | 0 |
| `COURIER_STATE_AT_BASE` | 1 |
| `COURIER_STATE_MOVING` | 2 |
| `COURIER_STATE_DELIVERING_ITEMS` | 3 |
| `COURIER_STATE_RETURNING_TO_BASE` | 4 |
| `COURIER_STATE_DEAD` | 5 |
| `COURIER_STATE_GOING_TO_SECRET_SHOP` | 6 |
| `COURIER_STATE_AT_SECRET_SHOP` | 7 |

</details>
