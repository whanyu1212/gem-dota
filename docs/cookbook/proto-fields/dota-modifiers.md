# dota_modifiers.proto

- Module: `dota_modifiers_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **1**
- Messages: **2** (top-level: 2)
- Enums: **1** (top-level: 1)

## Imports

- `networkbasetypes.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CDOTAModifierBuffTableEntry</code> — fields: 40; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `entry_type` | `.DOTA_MODIFIER_ENTRY_TYPE` | `required` | `` | default = DOTA_MODIFIER_ENTRY_TYPE_ACTIVE |
| 2 | `parent` | `uint32` | `required` | `` | default = 16777215 |
| 3 | `index` | `int32` | `required` | `` |  |
| 4 | `serial_num` | `int32` | `required` | `` |  |
| 5 | `modifier_class` | `int32` | `optional` | `` |  |
| 6 | `ability_level` | `int32` | `optional` | `` |  |
| 7 | `stack_count` | `int32` | `optional` | `` |  |
| 8 | `creation_time` | `float` | `optional` | `` |  |
| 9 | `duration` | `float` | `optional` | `` | default = -1 |
| 10 | `caster` | `uint32` | `optional` | `` | default = 16777215 |
| 11 | `ability` | `uint32` | `optional` | `` | default = 16777215 |
| 12 | `armor` | `int32` | `optional` | `` |  |
| 13 | `fade_time` | `float` | `optional` | `` |  |
| 14 | `subtle` | `bool` | `optional` | `` |  |
| 15 | `channel_time` | `float` | `optional` | `` |  |
| 16 | `v_start` | `.CMsgVector` | `optional` | `` |  |
| 17 | `v_end` | `.CMsgVector` | `optional` | `` |  |
| 18 | `portal_loop_appear` | `string` | `optional` | `` |  |
| 19 | `portal_loop_disappear` | `string` | `optional` | `` |  |
| 20 | `hero_loop_appear` | `string` | `optional` | `` |  |
| 21 | `hero_loop_disappear` | `string` | `optional` | `` |  |
| 22 | `movement_speed` | `int32` | `optional` | `` |  |
| 23 | `aura` | `bool` | `optional` | `` |  |
| 24 | `activity` | `int32` | `optional` | `` |  |
| 25 | `damage` | `int32` | `optional` | `` |  |
| 26 | `range` | `int32` | `optional` | `` |  |
| 27 | `dd_modifier_index` | `int32` | `optional` | `` |  |
| 28 | `dd_ability_id` | `int32` | `optional` | `` | default = -1 |
| 29 | `illusion_label` | `string` | `optional` | `` |  |
| 30 | `active` | `bool` | `optional` | `` |  |
| 31 | `player_ids` | `string` | `optional` | `` |  |
| 32 | `lua_name` | `string` | `optional` | `` |  |
| 33 | `attack_speed` | `int32` | `optional` | `` |  |
| 34 | `aura_owner` | `uint32` | `optional` | `` | default = 16777215 |
| 35 | `bonus_all_stats` | `int32` | `optional` | `` |  |
| 36 | `bonus_health` | `int32` | `optional` | `` |  |
| 37 | `bonus_mana` | `int32` | `optional` | `` |  |
| 38 | `custom_entity` | `uint32` | `optional` | `` | default = 16777215 |
| 39 | `aura_within_range` | `bool` | `optional` | `` |  |
| 40 | `move_slow` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTALuaModifierEntry</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `modifier_type` | `int32` | `required` | `` |  |
| 2 | `modifier_filename` | `string` | `required` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>DOTA_MODIFIER_ENTRY_TYPE</code> — values: 2</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `DOTA_MODIFIER_ENTRY_TYPE_ACTIVE` | 1 |
| `DOTA_MODIFIER_ENTRY_TYPE_REMOVED` | 2 |

</details>
