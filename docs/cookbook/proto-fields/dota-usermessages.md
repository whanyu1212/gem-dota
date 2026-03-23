# dota_usermessages.proto

- Module: `dota_usermessages_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **3**
- Messages: **190** (top-level: 172)
- Enums: **19** (top-level: 14)

## Imports

- `networkbasetypes.proto`
- `dota_shared_enums.proto`
- `dota_commonmessages.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CDOTAUserMsg_AIDebugLine</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `message` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_Ping</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `ping` | `uint32` | `optional` | `` |  |
| 3 | `loss` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_SwapVerify</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAUserMsg_ChatEvent</code> — fields: 11; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `type` | `.DOTA_CHAT_MESSAGE` | `required` | `` | default = CHAT_MESSAGE_INVALID |
| 2 | `value` | `uint32` | `optional` | `` |  |
| 3 | `playerid_1` | `sint32` | `optional` | `` | default = -1 |
| 4 | `playerid_2` | `sint32` | `optional` | `` | default = -1 |
| 5 | `playerid_3` | `sint32` | `optional` | `` | default = -1 |
| 6 | `playerid_4` | `sint32` | `optional` | `` | default = -1 |
| 7 | `playerid_5` | `sint32` | `optional` | `` | default = -1 |
| 8 | `playerid_6` | `sint32` | `optional` | `` | default = -1 |
| 9 | `value2` | `uint32` | `optional` | `` |  |
| 10 | `value3` | `uint32` | `optional` | `` |  |
| 11 | `time` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_BotChat</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 3 | `message` | `string` | `optional` | `` |  |
| 4 | `target` | `string` | `optional` | `` |  |
| 5 | `team_only` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_CombatHeroPositions</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `index` | `uint32` | `optional` | `` |  |
| 2 | `time` | `int32` | `optional` | `` |  |
| 3 | `world_pos` | `.CMsgVector2D` | `optional` | `` |  |
| 4 | `health` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_CombatLogBulkData</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `combat_entries` | `.CMsgDOTACombatLogEntry` | `repeated` | `` |  |
| 2 | `timestamp` | `float` | `optional` | `` |  |
| 3 | `duration` | `float` | `optional` | `` |  |
| 4 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 5 | `request_time` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_ProjectileParticleCPData</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `control_point` | `int32` | `optional` | `` |  |
| 2 | `vector` | `.CMsgVector` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_UpdateLinearProjectileCPData</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `handle` | `int32` | `optional` | `` |  |
| 2 | `control_point` | `int32` | `optional` | `` |  |
| 3 | `vector` | `.CMsgVector` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_MiniKillCamInfo</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `attackers` | `.CDOTAUserMsg_MiniKillCamInfo.Attacker` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_MiniKillCamInfo.Attacker</code> — fields: 4; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: `CDOTAUserMsg_MiniKillCamInfo`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `attacker` | `uint32` | `optional` | `` | default = 16777215 |
| 2 | `total_damage` | `int32` | `optional` | `` |  |
| 3 | `abilities` | `.CDOTAUserMsg_MiniKillCamInfo.Attacker.Ability` | `repeated` | `` |  |
| 4 | `attacker_name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_MiniKillCamInfo.Attacker.Ability</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAUserMsg_MiniKillCamInfo.Attacker`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ability_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `damage` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_GlobalLightColor</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `color` | `uint32` | `optional` | `` |  |
| 2 | `duration` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_GlobalLightDirection</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `direction` | `.CMsgVector` | `optional` | `` |  |
| 2 | `duration` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_LocationPing</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `location_ping` | `.CDOTAMsg_LocationPing` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_PingConfirmation</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id_of_original_pinger` | `int32` | `optional` | `` | default = -1 |
| 2 | `entity_index` | `uint32` | `optional` | `` |  |
| 3 | `icon_type` | `uint32` | `optional` | `` |  |
| 4 | `location` | `.CMsgVector` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_ItemAlert</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `item_alert` | `.CDOTAMsg_ItemAlert` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_EnemyItemAlert</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `target_player_id` | `int32` | `optional` | `` | default = -1 |
| 3 | `item_ability_id` | `int32` | `optional` | `` | default = -1 |
| 4 | `rune_type` | `int32` | `optional` | `` | default = -1 |
| 5 | `entity_id` | `int32` | `optional` | `` |  |
| 6 | `item_level` | `int32` | `optional` | `` | default = -1 |
| 7 | `primary_charges` | `int32` | `optional` | `` | default = -1 |
| 8 | `secondary_charges` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAUserMsg_ModifierAlert</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `class_name` | `string` | `optional` | `` |  |
| 3 | `stack_count` | `uint32` | `optional` | `` |  |
| 4 | `is_debuff` | `bool` | `optional` | `` |  |
| 5 | `target_entindex` | `int32` | `optional` | `` | default = -1 |
| 6 | `seconds_remaining` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_HPManaAlert</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `target_entindex` | `int32` | `optional` | `` | default = -1 |
| 3 | `show_raw_values` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_NeutralCampAlert</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `spawner_entindex` | `int32` | `optional` | `` | default = -1 |
| 3 | `unit_entindex` | `int32` | `optional` | `` | default = -1 |
| 4 | `stack_count` | `int32` | `optional` | `` |  |
| 5 | `camp_type` | `int32` | `optional` | `` |  |
| 6 | `stack_request` | `bool` | `optional` | `` |  |
| 7 | `stack_intention` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_GlyphAlert</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `negative` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_RadarAlert</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `negative` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_RoshanTimer</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `negative` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_TormentorTimer</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `negative` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_WillPurchaseAlert</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_ability_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 3 | `gold_remaining` | `uint32` | `optional` | `` |  |
| 4 | `suggestion_player_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAUserMsg_EmptyTeleportAlert</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `source_player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `target_player_id` | `int32` | `optional` | `` | default = -1 |
| 3 | `cooldown_seconds` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_MarsArenaOfBloodAttack</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `source_ehandle` | `uint32` | `optional` | `` | default = 16777215 |
| 2 | `target_ehandle` | `uint32` | `optional` | `` | default = 16777215 |
| 3 | `warrior_index` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_BuyBackStateAlert</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAUserMsg_QuickBuyAlert</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `item_ability_id` | `int32` | `optional` | `` | default = -1 |
| 3 | `gold_cost` | `int32` | `optional` | `` |  |
| 4 | `item_cooldown_seconds` | `int32` | `optional` | `` |  |
| 5 | `show_buyback` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_CourierKilledAlert</code> — fields: 7; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team` | `uint32` | `optional` | `` |  |
| 2 | `gold_value` | `uint32` | `optional` | `` |  |
| 3 | `entity_handle` | `uint32` | `optional` | `` | default = 16777215 |
| 4 | `timestamp` | `int32` | `optional` | `` |  |
| 5 | `lost_items` | `.CDOTAUserMsg_CourierKilledAlert.LostItem` | `repeated` | `` |  |
| 6 | `killer_player_id` | `int32` | `optional` | `` | default = -1 |
| 7 | `owning_player_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAUserMsg_CourierKilledAlert.LostItem</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAUserMsg_CourierKilledAlert`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_ability_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `quantity` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_MinimapEvent</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_type` | `int32` | `optional` | `` |  |
| 2 | `entity_handle` | `uint32` | `optional` | `` | default = 16777215 |
| 3 | `x` | `int32` | `optional` | `` |  |
| 4 | `y` | `int32` | `optional` | `` |  |
| 5 | `duration` | `int32` | `optional` | `` |  |
| 6 | `target_entity_handle` | `uint32` | `optional` | `` | default = 16777215 |

</details>

<details>
<summary><code>CDOTAUserMsg_MapLine</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `mapline` | `.CDOTAMsg_MapLine` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_MinimapDebugPoint</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `location` | `.CMsgVector` | `optional` | `` |  |
| 2 | `color` | `uint32` | `optional` | `` |  |
| 3 | `size` | `int32` | `optional` | `` |  |
| 4 | `duration` | `float` | `optional` | `` |  |
| 5 | `index` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_CreateLinearProjectile</code> — fields: 12; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `origin` | `.CMsgVector` | `optional` | `` |  |
| 2 | `velocity` | `.CMsgVector2D` | `optional` | `` |  |
| 4 | `entindex` | `int32` | `optional` | `` | default = -1 |
| 5 | `particle_index` | `uint64` | `optional` | `` |  |
| 6 | `handle` | `int32` | `optional` | `` |  |
| 7 | `acceleration` | `.CMsgVector2D` | `optional` | `` |  |
| 8 | `max_speed` | `float` | `optional` | `` |  |
| 9 | `fow_radius` | `float` | `optional` | `` |  |
| 10 | `sticky_fow_reveal` | `bool` | `optional` | `` |  |
| 11 | `distance` | `float` | `optional` | `` |  |
| 12 | `colorgemcolor` | `fixed32` | `optional` | `` |  |
| 13 | `particle_cp_data` | `.CDOTAUserMsg_ProjectileParticleCPData` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_DestroyLinearProjectile</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `handle` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_DodgeTrackingProjectiles</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `entindex` | `int32` | `required` | `` | default = -1 |
| 2 | `attacks_only` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_SpectatorPlayerClick</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `entindex` | `int32` | `required` | `` | default = -1 |
| 2 | `order_type` | `int32` | `optional` | `` |  |
| 3 | `target_index` | `int32` | `optional` | `` | default = 0 |

</details>

<details>
<summary><code>CDOTAUserMsg_SpectatorPlayerUnitOrders</code> — fields: 11; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `entindex` | `int32` | `optional` | `` | default = -1 |
| 2 | `order_type` | `int32` | `optional` | `` |  |
| 3 | `units` | `int32` | `repeated` | `` |  |
| 4 | `target_index` | `int32` | `optional` | `` | default = 0 |
| 5 | `ability_id` | `int32` | `optional` | `` | default = -1 |
| 6 | `position` | `.CMsgVector` | `optional` | `` |  |
| 7 | `queue` | `bool` | `optional` | `` |  |
| 8 | `sequence_number` | `int32` | `optional` | `` |  |
| 9 | `flags` | `uint32` | `optional` | `` |  |
| 10 | `last_order_latency` | `uint32` | `optional` | `` |  |
| 11 | `ping` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_NevermoreRequiem</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `entity_handle` | `uint32` | `optional` | `` | default = 16777215 |
| 2 | `lines` | `int32` | `optional` | `` |  |
| 3 | `origin` | `.CMsgVector` | `optional` | `` |  |
| 4 | `reverse` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_InvalidCommand</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `message` | `string` | `optional` | `` |  |
| 2 | `sequence_number` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_HudError</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `order_id` | `int32` | `optional` | `` |  |
| 2 | `sequence_number` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_SharedCooldown</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `entindex` | `int32` | `optional` | `` | default = -1 |
| 2 | `name` | `string` | `optional` | `` |  |
| 3 | `cooldown` | `float` | `optional` | `` |  |
| 4 | `name_index` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_SetNextAutobuyItem</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_HalloweenDrops</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_defs` | `uint32` | `repeated` | `` |  |
| 2 | `player_ids` | `int32` | `repeated` | `` |  |
| 3 | `prize_list` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_CourierLeftFountainAlert</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `owning_player_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAResponseQuerySerialized</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `facts` | `.CDOTAResponseQuerySerialized.Fact` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAResponseQuerySerialized.Fact</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: `CDOTAResponseQuerySerialized`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `key` | `int32` | `required` | `` |  |
| 2 | `valtype` | `.CDOTAResponseQuerySerialized.Fact.ValueType` | `required` | `` | default = NUMERIC |
| 3 | `val_numeric` | `float` | `optional` | `` |  |
| 4 | `val_string` | `string` | `optional` | `` |  |
| 5 | `val_stringtable_index` | `int32` | `optional` | `` |  |
| 6 | `val_int_numeric` | `sint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTASpeechMatchOnClient</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `speech_concept` | `int32` | `optional` | `` |  |
| 2 | `recipient_type` | `int32` | `optional` | `` |  |
| 3 | `responsequery` | `.CDOTAResponseQuerySerialized` | `optional` | `` |  |
| 4 | `randomseed` | `sfixed32` | `optional` | `` | default = 0 |

</details>

<details>
<summary><code>CDOTAUserMsg_UnitEvent</code> — fields: 9; oneofs: 0; nested messages: 7; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `msg_type` | `.EDotaEntityMessages` | `required` | `` | default = DOTA_UNIT_SPEECH |
| 2 | `entity_index` | `int32` | `required` | `` |  |
| 3 | `speech` | `.CDOTAUserMsg_UnitEvent.Speech` | `optional` | `` |  |
| 4 | `speech_mute` | `.CDOTAUserMsg_UnitEvent.SpeechMute` | `optional` | `` |  |
| 5 | `add_gesture` | `.CDOTAUserMsg_UnitEvent.AddGesture` | `optional` | `` |  |
| 6 | `remove_gesture` | `.CDOTAUserMsg_UnitEvent.RemoveGesture` | `optional` | `` |  |
| 7 | `blood_impact` | `.CDOTAUserMsg_UnitEvent.BloodImpact` | `optional` | `` |  |
| 8 | `fade_gesture` | `.CDOTAUserMsg_UnitEvent.FadeGesture` | `optional` | `` |  |
| 9 | `speech_match_on_client` | `.CDOTASpeechMatchOnClient` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_UnitEvent.Interval</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAUserMsg_UnitEvent`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `start` | `float` | `optional` | `` |  |
| 2 | `range` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_UnitEvent.Speech</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAUserMsg_UnitEvent`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `speech_concept` | `int32` | `optional` | `` |  |
| 2 | `response` | `string` | `optional` | `` |  |
| 3 | `recipient_type` | `int32` | `optional` | `` |  |
| 5 | `muteable` | `bool` | `optional` | `` | default = false |
| 6 | `predelay` | `.CDOTAUserMsg_UnitEvent.Interval` | `optional` | `` |  |
| 7 | `flags` | `uint32` | `optional` | `` |  |
| 8 | `response_type` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_UnitEvent.SpeechMute</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAUserMsg_UnitEvent`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `delay` | `float` | `optional` | `` | default = 0.5 |

</details>

<details>
<summary><code>CDOTAUserMsg_UnitEvent.AddGesture</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAUserMsg_UnitEvent`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `activity` | `int32` | `optional` | `` |  |
| 2 | `slot` | `int32` | `optional` | `` |  |
| 3 | `fade_in` | `float` | `optional` | `` | default = 0 |
| 4 | `fade_out` | `float` | `optional` | `` | default = 0.1 |
| 5 | `playback_rate` | `float` | `optional` | `` | default = 1 |
| 6 | `sequence_variant` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_UnitEvent.RemoveGesture</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAUserMsg_UnitEvent`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `activity` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_UnitEvent.BloodImpact</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAUserMsg_UnitEvent`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `scale` | `int32` | `optional` | `` |  |
| 2 | `x_normal` | `int32` | `optional` | `` |  |
| 3 | `y_normal` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_UnitEvent.FadeGesture</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAUserMsg_UnitEvent`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `activity` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_ItemPurchased</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_ability_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `from_combine` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_ItemSold</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_ability_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAUserMsg_ItemFound</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player` | `int32` | `optional` | `` | default = -1 |
| 2 | `quality` | `int32` | `optional` | `` |  |
| 3 | `rarity` | `int32` | `optional` | `` |  |
| 4 | `method` | `int32` | `optional` | `` |  |
| 5 | `itemdef` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_OverheadEvent</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `message_type` | `.DOTA_OVERHEAD_ALERT` | `required` | `` | default = OVERHEAD_ALERT_GOLD |
| 2 | `value` | `int32` | `optional` | `` |  |
| 3 | `target_player_entindex` | `int32` | `optional` | `` | default = -1 |
| 4 | `target_entindex` | `int32` | `optional` | `` | default = -1 |
| 5 | `source_player_entindex` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAUserMsg_TutorialTipInfo</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `progress` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_TutorialFinish</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `heading` | `string` | `optional` | `` |  |
| 2 | `emblem` | `string` | `optional` | `` |  |
| 3 | `body` | `string` | `optional` | `` |  |
| 4 | `success` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_TutorialMinimapPosition</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CDOTAUserMsg_SendGenericToolTip</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `title` | `string` | `optional` | `` |  |
| 2 | `text` | `string` | `optional` | `` |  |
| 3 | `entindex` | `int32` | `optional` | `` |  |
| 4 | `close` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_WorldLine</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `worldline` | `.CDOTAMsg_WorldLine` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_ChatWheel</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `chat_message_id` | `uint32` | `optional` | `` | default = 4294967295 |
| 2 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 3 | `account_id` | `uint32` | `optional` | `` |  |
| 4 | `param_hero_id` | `int32` | `optional` | `` |  |
| 5 | `emoticon_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_ReceivedXmasGift</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `item_name` | `string` | `optional` | `` |  |
| 3 | `inventory_slot` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_ShowSurvey</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `survey_id` | `int32` | `optional` | `` |  |
| 2 | `match_id` | `uint64` | `optional` | `` |  |
| 3 | `response_style` | `string` | `optional` | `` |  |
| 4 | `teammate_hero_id` | `int32` | `optional` | `` |  |
| 5 | `teammate_name` | `string` | `optional` | `` |  |
| 6 | `teammate_account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_UpdateSharedContent</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `slot_type` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_TutorialRequestExp</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CDOTAUserMsg_TutorialFade</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `tgt_alpha` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_TutorialPingMinimap</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `pos_x` | `float` | `optional` | `` |  |
| 3 | `pos_y` | `float` | `optional` | `` |  |
| 4 | `pos_z` | `float` | `optional` | `` |  |
| 5 | `entity_index` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_GamerulesStateChanged</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `state` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_AddQuestLogEntry</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `npc_name` | `string` | `optional` | `` |  |
| 2 | `npc_dialog` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_SendStatPopup</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `statpopup` | `.CDOTAMsg_SendStatPopup` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_DismissAllStatPopups</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `dismissallmsg` | `.CDOTAMsg_DismissAllStatPopups` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_SendRoshanSpectatorPhase</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `phase` | `.DOTA_ROSHAN_PHASE` | `optional` | `` | default = k_SRSP_ROSHAN_ALIVE |
| 2 | `phase_start_time` | `int32` | `optional` | `` |  |
| 3 | `phase_length` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_SendRoshanPopup</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `reclaimed` | `bool` | `optional` | `` |  |
| 2 | `gametime` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_SendFinalGold</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `reliable_gold` | `uint32` | `repeated` | `` |  |
| 2 | `unreliable_gold` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_CustomMsg</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `message` | `string` | `optional` | `` |  |
| 2 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 3 | `value` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_CoachHUDPing</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `hud_ping` | `.CDOTAMsg_CoachHUDPing` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_ClientLoadGridNav</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CDOTAUserMsg_TE_Projectile</code> — fields: 18; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `source` | `uint32` | `optional` | `` | default = 16777215 |
| 2 | `target` | `uint32` | `optional` | `` | default = 16777215 |
| 3 | `move_speed` | `int32` | `optional` | `` |  |
| 4 | `source_attachment` | `int32` | `optional` | `` |  |
| 5 | `particle_system_handle` | `int64` | `optional` | `` |  |
| 6 | `dodgeable` | `bool` | `optional` | `` |  |
| 7 | `is_attack` | `bool` | `optional` | `` |  |
| 9 | `expire_time` | `float` | `optional` | `` |  |
| 10 | `maximpacttime` | `float` | `optional` | `` |  |
| 11 | `colorgemcolor` | `fixed32` | `optional` | `` |  |
| 12 | `launch_tick` | `int32` | `optional` | `` |  |
| 13 | `handle` | `int32` | `optional` | `` |  |
| 14 | `target_loc` | `.CMsgVector` | `optional` | `` |  |
| 15 | `particle_cp_data` | `.CDOTAUserMsg_ProjectileParticleCPData` | `repeated` | `` |  |
| 16 | `additional_particle_system_handle` | `int64` | `optional` | `` |  |
| 17 | `original_move_speed` | `int32` | `optional` | `` |  |
| 18 | `ability` | `uint32` | `optional` | `` | default = 16777215 |
| 19 | `target_projectile_handle` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_TE_ProjectileLoc</code> — fields: 16; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `source_loc` | `.CMsgVector` | `optional` | `` |  |
| 2 | `target` | `uint32` | `optional` | `` | default = 16777215 |
| 3 | `move_speed` | `int32` | `optional` | `` |  |
| 4 | `particle_system_handle` | `int64` | `optional` | `` |  |
| 5 | `dodgeable` | `bool` | `optional` | `` |  |
| 6 | `is_attack` | `bool` | `optional` | `` |  |
| 9 | `expire_time` | `float` | `optional` | `` |  |
| 10 | `target_loc` | `.CMsgVector` | `optional` | `` |  |
| 11 | `colorgemcolor` | `fixed32` | `optional` | `` |  |
| 12 | `launch_tick` | `int32` | `optional` | `` |  |
| 13 | `handle` | `int32` | `optional` | `` |  |
| 14 | `source` | `uint32` | `optional` | `` | default = 16777215 |
| 15 | `source_attachment` | `int32` | `optional` | `` |  |
| 16 | `particle_cp_data` | `.CDOTAUserMsg_ProjectileParticleCPData` | `repeated` | `` |  |
| 17 | `additional_particle_system_handle` | `int64` | `optional` | `` |  |
| 18 | `original_move_speed` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_TE_DestroyProjectile</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `handle` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_TE_DotaBloodImpact</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `entity` | `uint32` | `optional` | `` | default = 16777215 |
| 2 | `scale` | `float` | `optional` | `` |  |
| 3 | `xnormal` | `float` | `optional` | `` |  |
| 4 | `ynormal` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_AbilityPing</code> — fields: 13; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `ability_id` | `int32` | `optional` | `` | default = -1 |
| 3 | `type` | `.DOTA_ABILITY_PING_TYPE` | `optional` | `` | default = ABILITY_PING_READY |
| 4 | `cooldown_seconds` | `uint32` | `optional` | `` |  |
| 5 | `level` | `uint32` | `optional` | `` |  |
| 6 | `passive` | `bool` | `optional` | `` |  |
| 7 | `mana_needed` | `uint32` | `optional` | `` |  |
| 8 | `entity_id` | `uint32` | `optional` | `` |  |
| 9 | `primary_charges` | `int32` | `optional` | `` |  |
| 10 | `secondary_charges` | `int32` | `optional` | `` |  |
| 12 | `ctrl_held` | `bool` | `optional` | `` |  |
| 13 | `reclaim_time` | `float` | `optional` | `` |  |
| 14 | `owner_entity` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAUserMsg_TE_UnitAnimation</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `entity` | `uint32` | `optional` | `` | default = 16777215 |
| 2 | `sequence_variant` | `int32` | `optional` | `` |  |
| 3 | `playbackrate` | `float` | `optional` | `` |  |
| 4 | `castpoint` | `float` | `optional` | `` |  |
| 5 | `type` | `int32` | `optional` | `` |  |
| 6 | `activity` | `int32` | `optional` | `` |  |
| 7 | `lag_compensation_time` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_TE_UnitAnimationEnd</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `entity` | `uint32` | `optional` | `` | default = 16777215 |
| 2 | `snap` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_ShowGenericPopup</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `header` | `string` | `required` | `` |  |
| 2 | `body` | `string` | `required` | `` |  |
| 3 | `param1` | `string` | `optional` | `` |  |
| 4 | `param2` | `string` | `optional` | `` |  |
| 5 | `tint_screen` | `bool` | `optional` | `` |  |
| 6 | `show_no_other_dialogs` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_VoteStart</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `title` | `string` | `optional` | `` |  |
| 2 | `duration` | `float` | `optional` | `` |  |
| 3 | `choice_count` | `int32` | `optional` | `` |  |
| 4 | `choices` | `string` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_VoteUpdate</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `choice_counts` | `int32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_VoteEnd</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `selected_choice` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_BoosterStatePlayer</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `bonus` | `float` | `optional` | `` |  |
| 3 | `event_bonus` | `float` | `optional` | `` |  |
| 4 | `bonus_item_id` | `uint32` | `optional` | `` |  |
| 5 | `event_bonus_item_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_BoosterState</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `boosted_players` | `.CDOTAUserMsg_BoosterStatePlayer` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_AbilitySteal</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `ability_id` | `int32` | `optional` | `` | default = -1 |
| 3 | `ability_level` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_StatsHeroLookup</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `hero_id` | `int32` | `optional` | `` |  |
| 3 | `hero_name` | `string` | `optional` | `` |  |
| 4 | `persona` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_StatsHeroPositionInfo</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `average_position` | `float` | `optional` | `` |  |
| 2 | `position_details` | `.CDOTAUserMsg_StatsHeroPositionInfo.PositionPair` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_StatsHeroPositionInfo.PositionPair</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAUserMsg_StatsHeroPositionInfo`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `position_category` | `.DOTA_POSITION_CATEGORY` | `optional` | `` | default = DOTA_POSITION_NONE |
| 2 | `position_count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_StatsHeroMinuteDetails</code> — fields: 15; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `last_hits` | `uint32` | `optional` | `` |  |
| 2 | `hero_kills` | `uint32` | `optional` | `` |  |
| 3 | `hero_damage` | `uint32` | `optional` | `` |  |
| 4 | `tower_damage` | `uint32` | `optional` | `` |  |
| 5 | `position_info` | `.CDOTAUserMsg_StatsHeroPositionInfo` | `optional` | `` |  |
| 6 | `total_xp` | `uint32` | `optional` | `` |  |
| 7 | `net_worth` | `uint32` | `optional` | `` |  |
| 8 | `harvested_creep_gold` | `uint32` | `optional` | `` |  |
| 9 | `claimed_farm` | `uint32` | `optional` | `` |  |
| 10 | `wards_placed` | `uint32` | `optional` | `` |  |
| 11 | `runes_collected` | `uint32` | `optional` | `` |  |
| 12 | `tps_used` | `uint32` | `optional` | `` |  |
| 13 | `mana_spent` | `uint32` | `repeated` | `` |  |
| 14 | `damage_absorbed` | `uint32` | `repeated` | `` |  |
| 15 | `damage_done` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_StatsTeamMinuteDetails</code> — fields: 10; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_stats` | `.CDOTAUserMsg_StatsHeroMinuteDetails` | `repeated` | `` |  |
| 2 | `tower_kills` | `uint32` | `optional` | `` |  |
| 3 | `barrack_kills` | `uint32` | `optional` | `` |  |
| 4 | `available_lane_creep_gold` | `uint32` | `optional` | `` |  |
| 5 | `balance_kill_value` | `uint32` | `optional` | `` |  |
| 6 | `balance_tower_value` | `uint32` | `optional` | `` |  |
| 7 | `balance_barracks_value` | `uint32` | `optional` | `` |  |
| 8 | `balance_gold_value` | `uint32` | `optional` | `` |  |
| 9 | `balance_xp_value` | `uint32` | `optional` | `` |  |
| 10 | `lane_performance` | `.CDOTAUserMsg_StatsTeamMinuteDetails.LocationPerformance` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_StatsTeamMinuteDetails.LocationPerformance</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAUserMsg_StatsTeamMinuteDetails`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `location_category` | `uint32` | `optional` | `` |  |
| 2 | `stat_type` | `uint32` | `optional` | `` |  |
| 3 | `value` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_StatsPlayerKillShare</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `kill_share_percent` | `float` | `optional` | `` |  |
| 3 | `player_loc_x` | `float` | `optional` | `` |  |
| 4 | `player_loc_y` | `float` | `optional` | `` |  |
| 5 | `health_percent` | `float` | `optional` | `` |  |
| 6 | `mana_percent` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_StatsKillDetails</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `victim_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `kill_shares` | `.CDOTAUserMsg_StatsPlayerKillShare` | `repeated` | `` |  |
| 3 | `damage_to_kill` | `uint32` | `optional` | `` |  |
| 4 | `effective_health` | `uint32` | `optional` | `` |  |
| 5 | `death_time` | `float` | `optional` | `` |  |
| 6 | `killer_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAUserMsg_StatsMatchDetails</code> — fields: 6; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_lookup` | `.CDOTAUserMsg_StatsHeroLookup` | `repeated` | `` |  |
| 2 | `radiant_stats` | `.CDOTAUserMsg_StatsTeamMinuteDetails` | `repeated` | `` |  |
| 3 | `dire_stats` | `.CDOTAUserMsg_StatsTeamMinuteDetails` | `repeated` | `` |  |
| 4 | `radiant_kills` | `.CDOTAUserMsg_StatsKillDetails` | `repeated` | `` |  |
| 5 | `dire_kills` | `.CDOTAUserMsg_StatsKillDetails` | `repeated` | `` |  |
| 6 | `fight_details` | `.CDOTAUserMsg_StatsMatchDetails.CDOTAUserMsg_StatsFightDetails` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_StatsMatchDetails.CDOTAUserMsg_StatsFightTeamDetails</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAUserMsg_StatsMatchDetails`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `participants` | `int32` | `repeated` | `` |  |
| 2 | `deaths` | `int32` | `repeated` | `` |  |
| 3 | `gold_delta` | `uint32` | `optional` | `` |  |
| 4 | `xp_delta` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_StatsMatchDetails.CDOTAUserMsg_StatsFightDetails</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAUserMsg_StatsMatchDetails`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `start_time` | `float` | `optional` | `` |  |
| 2 | `end_time` | `float` | `optional` | `` |  |
| 3 | `radiant_fight_details` | `.CDOTAUserMsg_StatsMatchDetails.CDOTAUserMsg_StatsFightTeamDetails` | `optional` | `` |  |
| 4 | `dire_fight_details` | `.CDOTAUserMsg_StatsMatchDetails.CDOTAUserMsg_StatsFightTeamDetails` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_MiniTaunt</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `taunting_player_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAUserMsg_SpeechBubble</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `destroy_all` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_CustomHeaderMessage</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `duration` | `float` | `optional` | `` |  |
| 3 | `message` | `string` | `optional` | `` |  |
| 4 | `value` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgHeroAbilityStat</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `stat_type` | `.EHeroStatType` | `optional` | `` | default = k_EHeroStatType_None |
| 2 | `int_value` | `int32` | `optional` | `` |  |
| 3 | `float_value` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgCombatAnalyzerPlayerStat</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `hero_ability_stats` | `.CMsgHeroAbilityStat` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgCombatAnalyzerStats</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `player_stats` | `.CMsgCombatAnalyzerPlayerStat` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_BeastChat</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team` | `uint32` | `optional` | `` |  |
| 2 | `format` | `string` | `optional` | `` |  |
| 3 | `message` | `string` | `optional` | `` |  |
| 4 | `target` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_CustomHudElement_Create</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `element_id` | `string` | `optional` | `` |  |
| 2 | `layout_filename` | `string` | `optional` | `` |  |
| 3 | `data` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_CustomHudElement_Modify</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `element_id` | `string` | `optional` | `` |  |
| 2 | `modify_visible` | `bool` | `optional` | `` |  |
| 3 | `data` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_CustomHudElement_Destroy</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `element_id` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_CompendiumStatePlayer</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `level` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_CompendiumState</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `compendium_players` | `.CDOTAUserMsg_CompendiumStatePlayer` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_ProjectionAbility</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ability_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `caster_ent_index` | `int32` | `optional` | `` | default = -1 |
| 3 | `caster_team` | `int32` | `optional` | `` |  |
| 4 | `channel_end` | `bool` | `optional` | `` |  |
| 5 | `origin` | `.CMsgVector` | `optional` | `` |  |
| 6 | `track_caster_only` | `bool` | `optional` | `` |  |
| 7 | `end_time` | `float` | `optional` | `` |  |
| 8 | `victim_ent_index` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAUserMsg_ProjectionEvent</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EProjectionEvent` | `optional` | `` | default = ePE_FirstBlood |
| 2 | `team` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_XPAlert</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `target_entindex` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAUserMsg_TalentTreeAlert</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `target_entindex` | `int32` | `optional` | `` | default = -1 |
| 3 | `ability_id` | `int32` | `optional` | `` | default = -1 |
| 4 | `slot` | `int32` | `optional` | `` |  |
| 5 | `learned` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_UpdateQuestProgress</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CDOTAUserMsg_QuestStatus</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `required` | `` | default = -1 |
| 2 | `quest_id` | `uint32` | `optional` | `` |  |
| 3 | `challenge_id` | `uint32` | `optional` | `` |  |
| 4 | `progress` | `uint32` | `optional` | `` |  |
| 5 | `goal` | `uint32` | `optional` | `` |  |
| 6 | `query` | `uint32` | `optional` | `` |  |
| 7 | `fail_gametime` | `float` | `optional` | `` |  |
| 8 | `item_ability_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAUserMsg_SuggestHeroPick</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `required` | `` | default = -1 |
| 2 | `hero_id` | `int32` | `optional` | `` |  |
| 3 | `ban` | `bool` | `optional` | `` |  |
| 4 | `facet_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_SuggestHeroRole</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `required` | `` | default = -1 |
| 2 | `hero_role` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_KillcamDamageTaken</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `required` | `` | default = -1 |
| 2 | `damage_taken` | `uint32` | `optional` | `` |  |
| 3 | `item_type` | `uint32` | `optional` | `` |  |
| 4 | `item_ability_id` | `int32` | `optional` | `` | default = -1 |
| 5 | `hero_name` | `string` | `optional` | `` |  |
| 6 | `damage_color` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_SelectPenaltyGold</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `required` | `` | default = -1 |
| 2 | `cost` | `sint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_RollDiceResult</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `channel_type` | `uint32` | `optional` | `` |  |
| 3 | `roll_min` | `uint32` | `optional` | `` |  |
| 4 | `roll_max` | `uint32` | `optional` | `` |  |
| 5 | `result` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_FlipCoinResult</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `channel_type` | `uint32` | `optional` | `` |  |
| 3 | `result` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMessage_RequestItemSuggestions</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAUserMessage_TeamCaptainChanged</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team` | `uint32` | `optional` | `` |  |
| 2 | `captain_player_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAUserMsg_ChatWheelCooldown</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `message_id` | `uint32` | `optional` | `` | default = 4294967295 |
| 2 | `cooldown_remaining` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_HeroRelicProgress</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_relic_type` | `uint32` | `optional` | `` |  |
| 2 | `value` | `uint32` | `optional` | `` |  |
| 3 | `ehandle` | `uint32` | `optional` | `` | default = 16777215 |
| 4 | `event_id` | `uint32` | `optional` | `` |  |
| 5 | `value_display` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_AbilityDraftRequestAbility</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `requested_ability_id` | `int32` | `optional` | `` | default = -1 |
| 3 | `ctrl_is_down` | `bool` | `optional` | `` |  |
| 4 | `requested_hero_id` | `int32` | `optional` | `` |  |
| 5 | `requested_facet_key` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_DamageReport</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `target_hero_id` | `int32` | `optional` | `` |  |
| 3 | `source_hero_id` | `int32` | `optional` | `` |  |
| 4 | `damage_amount` | `int32` | `optional` | `` |  |
| 5 | `broadcast` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_SalutePlayer</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `source_player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `target_player_id` | `int32` | `optional` | `` | default = -1 |
| 3 | `tip_amount` | `uint32` | `optional` | `` |  |
| 4 | `event_id` | `uint32` | `optional` | `` |  |
| 5 | `custom_tip_style` | `string` | `optional` | `` |  |
| 6 | `num_recent_tips` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_GiftPlayer</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `source_player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `target_player_id` | `int32` | `optional` | `` | default = -1 |
| 3 | `gift_item_def_index` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_TipAlert</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `tip_text` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_ReplaceQueryUnit</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `required` | `` | default = -1 |
| 2 | `source_entindex` | `int32` | `optional` | `` | default = -1 |
| 3 | `target_entindex` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAUserMsg_ESArcanaCombo</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ehandle` | `uint32` | `optional` | `` | default = 16777215 |
| 2 | `combo_count` | `uint32` | `optional` | `` |  |
| 3 | `arcana_level` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_ESArcanaComboSummary</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ehandle` | `uint32` | `optional` | `` | default = 16777215 |
| 2 | `combo_count` | `uint32` | `optional` | `` |  |
| 3 | `damage_amount` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_OMArcanaCombo</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ehandle` | `uint32` | `optional` | `` | default = 16777215 |
| 2 | `multicast_amount` | `uint32` | `optional` | `` |  |
| 3 | `arcana_level` | `uint32` | `optional` | `` |  |
| 4 | `multicast_chance` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_HighFiveCompleted</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id_1` | `int32` | `optional` | `` | default = -1 |
| 2 | `player_id_2` | `int32` | `optional` | `` | default = -1 |
| 3 | `special_high_five` | `bool` | `optional` | `` |  |
| 4 | `special_entindex` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAUserMsg_HighFiveLeftHanging</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAUserMsg_ShovelUnearth</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `all_chat` | `bool` | `optional` | `` |  |
| 3 | `locstring` | `string` | `optional` | `` |  |
| 4 | `quantity` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_AllStarEvent</code> — fields: 5; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `source_player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `target_player_id` | `int32` | `optional` | `` | default = -1 |
| 3 | `point_amount` | `uint32` | `optional` | `` |  |
| 4 | `event_id` | `uint32` | `optional` | `` |  |
| 5 | `player_scores` | `.CDOTAUserMsg_AllStarEvent.PlayerScore` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_AllStarEvent.PlayerScore</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAUserMsg_AllStarEvent`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `score_sans_kda` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_QueuedOrderRemoved</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `unit_order_sequence` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_DebugChallenge</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `challenge_type` | `uint32` | `required` | `` |  |
| 2 | `challenge_query_id` | `uint32` | `required` | `` |  |
| 3 | `event_id` | `uint32` | `required` | `` |  |
| 4 | `instance_id` | `uint32` | `optional` | `` |  |
| 5 | `challenge_var_0` | `uint32` | `optional` | `` |  |
| 6 | `challenge_var_1` | `uint32` | `optional` | `` |  |
| 7 | `challenge_max_rank` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_FoundNeutralItem</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `item_ability_id` | `int32` | `optional` | `` | default = -1 |
| 3 | `item_tier` | `uint32` | `optional` | `` |  |
| 4 | `tier_item_count` | `uint32` | `optional` | `` |  |
| 5 | `enhancement_ability_id` | `int32` | `optional` | `` | default = -1 |
| 6 | `enhancement_level` | `int32` | `optional` | `` |  |
| 7 | `trinket_level` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_OutpostCaptured</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `outpost_entindex` | `int32` | `optional` | `` | default = -1 |
| 2 | `team_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_OutpostGrantedXP</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team_id` | `uint32` | `optional` | `` |  |
| 2 | `xp_amount` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_MoveCameraToUnit</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `unit_ehandle` | `uint32` | `optional` | `` | default = 16777215 |

</details>

<details>
<summary><code>CDOTAUserMsg_PauseMinigameData</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `data_bits` | `.CDOTAUserMsg_PauseMinigameData.DataBit` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_PauseMinigameData.DataBit</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAUserMsg_PauseMinigameData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `index` | `uint32` | `optional` | `` |  |
| 2 | `data` | `int32` | `optional` | `` |  |
| 3 | `data_extra` | `int64` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_VersusScene_PlayerBehavior</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `behavior` | `.EDOTAVersusScenePlayerBehavior` | `optional` | `` | default = VS_PLAYER_BEHAVIOR_PLAY_ACTIVITY |
| 3 | `play_activity` | `.VersusScene_PlayActivity` | `optional` | `` |  |
| 4 | `chat_wheel` | `.VersusScene_ChatWheel` | `optional` | `` |  |
| 5 | `playback_rate` | `.VersusScene_PlaybackRate` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_QoP_ArcanaSummary</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ehandle` | `uint32` | `optional` | `` | default = 16777215 |
| 2 | `arcana_level` | `uint32` | `optional` | `` |  |
| 3 | `players_hit` | `uint32` | `optional` | `` |  |
| 4 | `players_killed` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_HotPotato_Created</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id_1` | `int32` | `optional` | `` | default = -1 |
| 2 | `player_id_2` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAUserMsg_HotPotato_Exploded</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAUserMsg_WK_Arcana_Progress</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ehandle` | `uint32` | `optional` | `` | default = 16777215 |
| 2 | `arcana_level` | `uint32` | `optional` | `` |  |
| 3 | `hero_id` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_GuildChallenge_Progress</code> — fields: 7; oneofs: 0; nested messages: 1; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_progress` | `.CDOTAUserMsg_GuildChallenge_Progress.PlayerProgress` | `repeated` | `` |  |
| 2 | `guild_id` | `uint32` | `optional` | `` |  |
| 3 | `challenge_instance_id` | `uint32` | `optional` | `` |  |
| 4 | `challenge_parameter` | `uint32` | `optional` | `` |  |
| 5 | `challenge_type` | `.CDOTAUserMsg_GuildChallenge_Progress.EChallengeType` | `optional` | `` | default = k_EChallengeType_Invalid |
| 7 | `challenge_progress_at_start` | `uint32` | `optional` | `` |  |
| 8 | `complete` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_GuildChallenge_Progress.PlayerProgress</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAUserMsg_GuildChallenge_Progress`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 6 | `progress` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_WRArcanaProgress</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ehandle` | `uint32` | `optional` | `` | default = 16777215 |
| 2 | `target_ehandle` | `uint32` | `optional` | `` | default = 16777215 |
| 3 | `arrows_landed` | `uint32` | `optional` | `` |  |
| 4 | `damage_dealt` | `uint32` | `optional` | `` |  |
| 5 | `target_hp` | `uint32` | `optional` | `` |  |
| 6 | `target_max_hp` | `uint32` | `optional` | `` |  |
| 7 | `arcana_level` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_WRArcanaSummary</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ehandle` | `uint32` | `optional` | `` | default = 16777215 |
| 2 | `target_ehandle` | `uint32` | `optional` | `` | default = 16777215 |
| 3 | `arrows_landed` | `uint32` | `optional` | `` |  |
| 4 | `damage_dealt` | `uint32` | `optional` | `` |  |
| 5 | `target_hp` | `uint32` | `optional` | `` |  |
| 6 | `target_max_hp` | `uint32` | `optional` | `` |  |
| 7 | `arcana_level` | `uint32` | `optional` | `` |  |
| 8 | `success` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_EmptyItemSlotAlert</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `source_player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `target_player_id` | `int32` | `optional` | `` | default = -1 |
| 3 | `slot_index` | `int32` | `optional` | `` |  |
| 4 | `cooldown_seconds` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_AghsStatusAlert</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `source_player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `target_player_id` | `int32` | `optional` | `` | default = -1 |
| 3 | `target_entindex` | `int32` | `optional` | `` | default = -1 |
| 4 | `alert_type` | `uint32` | `optional` | `` |  |
| 5 | `has_scepter` | `bool` | `optional` | `` |  |
| 6 | `has_shard` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_MutedPlayers</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `text_muted_player_ids` | `int32` | `repeated` | `` |  |
| 2 | `voice_muted_player_ids` | `int32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_ContextualTip</code> — fields: 15; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `tip_id` | `int32` | `optional` | `` |  |
| 2 | `referenced_abilities` | `string` | `repeated` | `` |  |
| 3 | `referenced_units` | `string` | `repeated` | `` |  |
| 4 | `panorama_classes` | `string` | `repeated` | `` |  |
| 5 | `force_annotation` | `bool` | `optional` | `` |  |
| 6 | `variant` | `int32` | `optional` | `` |  |
| 7 | `int_param` | `int32` | `optional` | `` |  |
| 8 | `int_param2` | `int32` | `optional` | `` |  |
| 9 | `float_param` | `float` | `optional` | `` |  |
| 10 | `float_param2` | `float` | `optional` | `` |  |
| 11 | `string_param` | `string` | `optional` | `` |  |
| 12 | `string_param2` | `string` | `optional` | `` |  |
| 13 | `tip_text_override` | `string` | `optional` | `` |  |
| 14 | `tip_annotation_override` | `string` | `optional` | `` |  |
| 15 | `panorama_snippet` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_ChatMessage</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `source_player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `channel_type` | `uint32` | `optional` | `` |  |
| 3 | `message_text` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_RockPaperScissorsStarted</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id_source` | `int32` | `optional` | `` | default = -1 |
| 2 | `player_id_target` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAUserMsg_RockPaperScissorsFinished</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id_1` | `int32` | `optional` | `` | default = -1 |
| 2 | `player_id_2` | `int32` | `optional` | `` | default = -1 |
| 3 | `player_1_choice` | `int32` | `optional` | `` |  |
| 4 | `player_2_choice` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_DuelOpponentKilled</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id_winner` | `int32` | `optional` | `` |  |
| 2 | `player_id_loser` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_DuelAccepted</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id_1` | `int32` | `optional` | `` |  |
| 2 | `player_id_2` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_DuelRequested</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id_requestor` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAUserMsg_MuertaReleaseEvent_AssignedTargetKilled</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id_killer` | `int32` | `required` | `` | default = -1 |
| 2 | `player_id_target` | `int32` | `required` | `` | default = -1 |
| 3 | `points` | `int32` | `required` | `` |  |
| 4 | `points_total` | `int32` | `required` | `` |  |
| 5 | `last_hit` | `bool` | `required` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_PlayerDraftSuggestPick</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `suggestion_player_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAUserMsg_PlayerDraftPick</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id_captain` | `int32` | `optional` | `` | default = -1 |
| 2 | `player_id_target` | `int32` | `optional` | `` | default = -1 |
| 3 | `team` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_FacetPing</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `facet_strhash` | `uint32` | `optional` | `` |  |
| 3 | `entity_id` | `uint32` | `optional` | `` |  |
| 4 | `all_chat` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_InnatePing</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `entity_id` | `uint32` | `optional` | `` |  |
| 3 | `all_chat` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_NeutralCraftAvailable</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CDOTAUserMsg_TimerAlert</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `timer_alert_type` | `.ETimerAlertType` | `optional` | `` | default = k_TimerAlertType_PowerRune |

</details>

<details>
<summary><code>CDOTAUserMsg_MadstoneAlert</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `target_entindex` | `int32` | `optional` | `` | default = -1 |
| 3 | `tier` | `int32` | `optional` | `` |  |
| 4 | `madstone_alert_type` | `.CDOTAUserMsg_MadstoneAlert.EMadstoneAlertType` | `optional` | `` | default = CraftAvailable |
| 5 | `value` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_MonsterHunter_InvestigationsAvailable</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `investigations` | `.CMsgMonsterHunterInvestigation` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_MonsterHunter_InvestigationGameState</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `investigation_game_state` | `.CMsgMonsterHunterInvestigationGameState` | `optional` | `` |  |
| 2 | `investigations_locked` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_MonsterHunter_HuntAlert</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 2</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `hero_id` | `int32` | `optional` | `` |  |
| 3 | `hunt_alert_type` | `.CDOTAUserMsg_MonsterHunter_HuntAlert.EHuntAlertType` | `optional` | `` | default = MainObjective |
| 4 | `hunt_status_type` | `.CDOTAUserMsg_MonsterHunter_HuntAlert.EHuntStatusType` | `optional` | `` | default = Pending |
| 5 | `index` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAUserMsg_KillEffect</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `victim_ent_index` | `int32` | `optional` | `` | default = -1 |
| 2 | `killer_player_id` | `int32` | `optional` | `` | default = -1 |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>EDotaUserMessages</code> — values: 168</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `DOTA_UM_AddUnitToSelection` | 464 |
| `DOTA_UM_AIDebugLine` | 465 |
| `DOTA_UM_ChatEvent` | 466 |
| `DOTA_UM_CombatHeroPositions` | 467 |
| `DOTA_UM_CombatLogData` | 468 |
| `DOTA_UM_CombatLogBulkData` | 470 |
| `DOTA_UM_CreateLinearProjectile` | 471 |
| `DOTA_UM_DestroyLinearProjectile` | 472 |
| `DOTA_UM_DodgeTrackingProjectiles` | 473 |
| `DOTA_UM_GlobalLightColor` | 474 |
| `DOTA_UM_GlobalLightDirection` | 475 |
| `DOTA_UM_InvalidCommand` | 476 |
| `DOTA_UM_LocationPing` | 477 |
| `DOTA_UM_MapLine` | 478 |
| `DOTA_UM_MiniKillCamInfo` | 479 |
| `DOTA_UM_MinimapDebugPoint` | 480 |
| `DOTA_UM_MinimapEvent` | 481 |
| `DOTA_UM_NevermoreRequiem` | 482 |
| `DOTA_UM_OverheadEvent` | 483 |
| `DOTA_UM_SetNextAutobuyItem` | 484 |
| `DOTA_UM_SharedCooldown` | 485 |
| `DOTA_UM_SpectatorPlayerClick` | 486 |
| `DOTA_UM_TutorialTipInfo` | 487 |
| `DOTA_UM_UnitEvent` | 488 |
| `DOTA_UM_ParticleManager` | 489 |
| `DOTA_UM_BotChat` | 490 |
| `DOTA_UM_HudError` | 491 |
| `DOTA_UM_ItemPurchased` | 492 |
| `DOTA_UM_Ping` | 493 |
| `DOTA_UM_ItemFound` | 494 |
| `DOTA_UM_CharacterSpeakConcept` | 495 |
| `DOTA_UM_SwapVerify` | 496 |
| `DOTA_UM_WorldLine` | 497 |
| `DOTA_UM_TournamentDrop` | 498 |
| `DOTA_UM_ItemAlert` | 499 |
| `DOTA_UM_HalloweenDrops` | 500 |
| `DOTA_UM_ChatWheel` | 501 |
| `DOTA_UM_ReceivedXmasGift` | 502 |
| `DOTA_UM_UpdateSharedContent` | 503 |
| `DOTA_UM_TutorialRequestExp` | 504 |
| `DOTA_UM_TutorialPingMinimap` | 505 |
| `DOTA_UM_GamerulesStateChanged` | 506 |
| `DOTA_UM_ShowSurvey` | 507 |
| `DOTA_UM_TutorialFade` | 508 |
| `DOTA_UM_AddQuestLogEntry` | 509 |
| `DOTA_UM_SendStatPopup` | 510 |
| `DOTA_UM_TutorialFinish` | 511 |
| `DOTA_UM_SendRoshanPopup` | 512 |
| `DOTA_UM_SendGenericToolTip` | 513 |
| `DOTA_UM_SendFinalGold` | 514 |
| `DOTA_UM_CustomMsg` | 515 |
| `DOTA_UM_CoachHUDPing` | 516 |
| `DOTA_UM_ClientLoadGridNav` | 517 |
| `DOTA_UM_TE_Projectile` | 518 |
| `DOTA_UM_TE_ProjectileLoc` | 519 |
| `DOTA_UM_TE_DotaBloodImpact` | 520 |
| `DOTA_UM_TE_UnitAnimation` | 521 |
| `DOTA_UM_TE_UnitAnimationEnd` | 522 |
| `DOTA_UM_AbilityPing` | 523 |
| `DOTA_UM_ShowGenericPopup` | 524 |
| `DOTA_UM_VoteStart` | 525 |
| `DOTA_UM_VoteUpdate` | 526 |
| `DOTA_UM_VoteEnd` | 527 |
| `DOTA_UM_BoosterState` | 528 |
| `DOTA_UM_WillPurchaseAlert` | 529 |
| `DOTA_UM_TutorialMinimapPosition` | 530 |
| `DOTA_UM_AbilitySteal` | 532 |
| `DOTA_UM_CourierKilledAlert` | 533 |
| `DOTA_UM_EnemyItemAlert` | 534 |
| `DOTA_UM_StatsMatchDetails` | 535 |
| `DOTA_UM_MiniTaunt` | 536 |
| `DOTA_UM_BuyBackStateAlert` | 537 |
| `DOTA_UM_SpeechBubble` | 538 |
| `DOTA_UM_CustomHeaderMessage` | 539 |
| `DOTA_UM_QuickBuyAlert` | 540 |
| `DOTA_UM_StatsHeroDetails` | 541 |
| `DOTA_UM_PredictionResult` | 542 |
| `DOTA_UM_ModifierAlert` | 543 |
| `DOTA_UM_HPManaAlert` | 544 |
| `DOTA_UM_GlyphAlert` | 545 |
| `DOTA_UM_BeastChat` | 546 |
| `DOTA_UM_SpectatorPlayerUnitOrders` | 547 |
| `DOTA_UM_CustomHudElement_Create` | 548 |
| `DOTA_UM_CustomHudElement_Modify` | 549 |
| `DOTA_UM_CustomHudElement_Destroy` | 550 |
| `DOTA_UM_CompendiumState` | 551 |
| `DOTA_UM_ProjectionAbility` | 552 |
| `DOTA_UM_ProjectionEvent` | 553 |
| `DOTA_UM_CombatLogDataHLTV` | 554 |
| `DOTA_UM_XPAlert` | 555 |
| `DOTA_UM_UpdateQuestProgress` | 556 |
| `DOTA_UM_MatchMetadata` | 557 |
| `DOTA_UM_MatchDetails` | 558 |
| `DOTA_UM_QuestStatus` | 559 |
| `DOTA_UM_SuggestHeroPick` | 560 |
| `DOTA_UM_SuggestHeroRole` | 561 |
| `DOTA_UM_KillcamDamageTaken` | 562 |
| `DOTA_UM_SelectPenaltyGold` | 563 |
| `DOTA_UM_RollDiceResult` | 564 |
| `DOTA_UM_FlipCoinResult` | 565 |
| `DOTA_UM_RequestItemSuggestions` | 566 |
| `DOTA_UM_TeamCaptainChanged` | 567 |
| `DOTA_UM_SendRoshanSpectatorPhase` | 568 |
| `DOTA_UM_ChatWheelCooldown` | 569 |
| `DOTA_UM_DismissAllStatPopups` | 570 |
| `DOTA_UM_TE_DestroyProjectile` | 571 |
| `DOTA_UM_HeroRelicProgress` | 572 |
| `DOTA_UM_AbilityDraftRequestAbility` | 573 |
| `DOTA_UM_ItemSold` | 574 |
| `DOTA_UM_DamageReport` | 575 |
| `DOTA_UM_SalutePlayer` | 576 |
| `DOTA_UM_TipAlert` | 577 |
| `DOTA_UM_ReplaceQueryUnit` | 578 |
| `DOTA_UM_EmptyTeleportAlert` | 579 |
| `DOTA_UM_MarsArenaOfBloodAttack` | 580 |
| `DOTA_UM_ESArcanaCombo` | 581 |
| `DOTA_UM_ESArcanaComboSummary` | 582 |
| `DOTA_UM_HighFiveLeftHanging` | 583 |
| `DOTA_UM_HighFiveCompleted` | 584 |
| `DOTA_UM_ShovelUnearth` | 585 |
| `DOTA_UM_RadarAlert` | 587 |
| `DOTA_UM_AllStarEvent` | 588 |
| `DOTA_UM_TalentTreeAlert` | 589 |
| `DOTA_UM_QueuedOrderRemoved` | 590 |
| `DOTA_UM_DebugChallenge` | 591 |
| `DOTA_UM_OMArcanaCombo` | 592 |
| `DOTA_UM_FoundNeutralItem` | 593 |
| `DOTA_UM_OutpostCaptured` | 594 |
| `DOTA_UM_OutpostGrantedXP` | 595 |
| `DOTA_UM_MoveCameraToUnit` | 596 |
| `DOTA_UM_PauseMinigameData` | 597 |
| `DOTA_UM_VersusScene_PlayerBehavior` | 598 |
| `DOTA_UM_QoP_ArcanaSummary` | 600 |
| `DOTA_UM_HotPotato_Created` | 601 |
| `DOTA_UM_HotPotato_Exploded` | 602 |
| `DOTA_UM_WK_Arcana_Progress` | 603 |
| `DOTA_UM_GuildChallenge_Progress` | 604 |
| `DOTA_UM_WRArcanaProgress` | 605 |
| `DOTA_UM_WRArcanaSummary` | 606 |
| `DOTA_UM_EmptyItemSlotAlert` | 607 |
| `DOTA_UM_AghsStatusAlert` | 608 |
| `DOTA_UM_PingConfirmation` | 609 |
| `DOTA_UM_MutedPlayers` | 610 |
| `DOTA_UM_ContextualTip` | 611 |
| `DOTA_UM_ChatMessage` | 612 |
| `DOTA_UM_NeutralCampAlert` | 613 |
| `DOTA_UM_RockPaperScissorsStarted` | 614 |
| `DOTA_UM_RockPaperScissorsFinished` | 615 |
| `DOTA_UM_DuelOpponentKilled` | 616 |
| `DOTA_UM_DuelAccepted` | 617 |
| `DOTA_UM_DuelRequested` | 618 |
| `DOTA_UM_MuertaReleaseEvent_AssignedTargetKilled` | 619 |
| `DOTA_UM_PlayerDraftSuggestPick` | 620 |
| `DOTA_UM_PlayerDraftPick` | 621 |
| `DOTA_UM_UpdateLinearProjectileCPData` | 622 |
| `DOTA_UM_GiftPlayer` | 623 |
| `DOTA_UM_FacetPing` | 624 |
| `DOTA_UM_InnatePing` | 625 |
| `DOTA_UM_RoshanTimer` | 626 |
| `DOTA_UM_NeutralCraftAvailable` | 627 |
| `DOTA_UM_TimerAlert` | 628 |
| `DOTA_UM_MadstoneAlert` | 629 |
| `DOTA_UM_CourierLeftFountainAlert` | 630 |
| `DOTA_UM_MonsterHunter_InvestigationsAvailable` | 631 |
| `DOTA_UM_MonsterHunter_InvestigationGameState` | 632 |
| `DOTA_UM_MonsterHunter_HuntAlert` | 633 |
| `DOTA_UM_TormentorTimer` | 634 |
| `DOTA_UM_KillEffect` | 635 |

</details>

<details>
<summary><code>DOTA_CHAT_MESSAGE</code> — values: 115</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `CHAT_MESSAGE_INVALID` | -1 |
| `CHAT_MESSAGE_HERO_KILL` | 0 |
| `CHAT_MESSAGE_HERO_DENY` | 1 |
| `CHAT_MESSAGE_BARRACKS_KILL` | 2 |
| `CHAT_MESSAGE_TOWER_KILL` | 3 |
| `CHAT_MESSAGE_TOWER_DENY` | 4 |
| `CHAT_MESSAGE_FIRSTBLOOD` | 5 |
| `CHAT_MESSAGE_STREAK_KILL` | 6 |
| `CHAT_MESSAGE_BUYBACK` | 7 |
| `CHAT_MESSAGE_AEGIS` | 8 |
| `CHAT_MESSAGE_ROSHAN_KILL` | 9 |
| `CHAT_MESSAGE_COURIER_LOST` | 10 |
| `CHAT_MESSAGE_COURIER_RESPAWNED` | 11 |
| `CHAT_MESSAGE_GLYPH_USED` | 12 |
| `CHAT_MESSAGE_ITEM_PURCHASE` | 13 |
| `CHAT_MESSAGE_CONNECT` | 14 |
| `CHAT_MESSAGE_DISCONNECT` | 15 |
| `CHAT_MESSAGE_DISCONNECT_WAIT_FOR_RECONNECT` | 16 |
| `CHAT_MESSAGE_DISCONNECT_TIME_REMAINING` | 17 |
| `CHAT_MESSAGE_DISCONNECT_TIME_REMAINING_PLURAL` | 18 |
| `CHAT_MESSAGE_RECONNECT` | 19 |
| `CHAT_MESSAGE_PLAYER_LEFT` | 20 |
| `CHAT_MESSAGE_SAFE_TO_LEAVE` | 21 |
| `CHAT_MESSAGE_RUNE_PICKUP` | 22 |
| `CHAT_MESSAGE_RUNE_BOTTLE` | 23 |
| `CHAT_MESSAGE_RUNE_DENY` | 114 |
| `CHAT_MESSAGE_INTHEBAG` | 24 |
| `CHAT_MESSAGE_SECRETSHOP` | 25 |
| `CHAT_MESSAGE_ITEM_AUTOPURCHASED` | 26 |
| `CHAT_MESSAGE_ITEMS_COMBINED` | 27 |
| `CHAT_MESSAGE_SUPER_CREEPS` | 28 |
| `CHAT_MESSAGE_CANT_USE_ACTION_ITEM` | 29 |
| `CHAT_MESSAGE_CANTPAUSE` | 31 |
| `CHAT_MESSAGE_NOPAUSESLEFT` | 32 |
| `CHAT_MESSAGE_CANTPAUSEYET` | 33 |
| `CHAT_MESSAGE_PAUSED` | 34 |
| `CHAT_MESSAGE_UNPAUSE_COUNTDOWN` | 35 |
| `CHAT_MESSAGE_UNPAUSED` | 36 |
| `CHAT_MESSAGE_AUTO_UNPAUSED` | 37 |
| `CHAT_MESSAGE_YOUPAUSED` | 38 |
| `CHAT_MESSAGE_CANTUNPAUSETEAM` | 39 |
| `CHAT_MESSAGE_VOICE_TEXT_BANNED` | 41 |
| `CHAT_MESSAGE_SPECTATORS_WATCHING_THIS_GAME` | 42 |
| `CHAT_MESSAGE_REPORT_REMINDER` | 43 |
| `CHAT_MESSAGE_ECON_ITEM` | 44 |
| `CHAT_MESSAGE_TAUNT` | 45 |
| `CHAT_MESSAGE_RANDOM` | 46 |
| `CHAT_MESSAGE_RD_TURN` | 47 |
| `CHAT_MESSAGE_DROP_RATE_BONUS` | 49 |
| `CHAT_MESSAGE_NO_BATTLE_POINTS` | 50 |
| `CHAT_MESSAGE_DENIED_AEGIS` | 51 |
| `CHAT_MESSAGE_INFORMATIONAL` | 52 |
| `CHAT_MESSAGE_AEGIS_STOLEN` | 53 |
| `CHAT_MESSAGE_ROSHAN_CANDY` | 54 |
| `CHAT_MESSAGE_ITEM_GIFTED` | 55 |
| `CHAT_MESSAGE_HERO_KILL_WITH_GREEVIL` | 56 |
| `CHAT_MESSAGE_HOLDOUT_TOWER_DESTROYED` | 57 |
| `CHAT_MESSAGE_HOLDOUT_WALL_DESTROYED` | 58 |
| `CHAT_MESSAGE_HOLDOUT_WALL_FINISHED` | 59 |
| `CHAT_MESSAGE_PLAYER_LEFT_LIMITED_HERO` | 62 |
| `CHAT_MESSAGE_ABANDON_LIMITED_HERO_EXPLANATION` | 63 |
| `CHAT_MESSAGE_DISCONNECT_LIMITED_HERO` | 64 |
| `CHAT_MESSAGE_LOW_PRIORITY_COMPLETED_EXPLANATION` | 65 |
| `CHAT_MESSAGE_RECRUITMENT_DROP_RATE_BONUS` | 66 |
| `CHAT_MESSAGE_FROSTIVUS_SHINING_BOOSTER_ACTIVE` | 67 |
| `CHAT_MESSAGE_PLAYER_LEFT_AFK` | 73 |
| `CHAT_MESSAGE_PLAYER_LEFT_DISCONNECTED_TOO_LONG` | 74 |
| `CHAT_MESSAGE_PLAYER_ABANDONED` | 75 |
| `CHAT_MESSAGE_PLAYER_ABANDONED_AFK` | 76 |
| `CHAT_MESSAGE_PLAYER_ABANDONED_DISCONNECTED_TOO_LONG` | 77 |
| `CHAT_MESSAGE_WILL_NOT_BE_SCORED` | 78 |
| `CHAT_MESSAGE_WILL_NOT_BE_SCORED_RANKED` | 79 |
| `CHAT_MESSAGE_WILL_NOT_BE_SCORED_NETWORK` | 80 |
| `CHAT_MESSAGE_WILL_NOT_BE_SCORED_NETWORK_RANKED` | 81 |
| `CHAT_MESSAGE_CAN_QUIT_WITHOUT_ABANDON` | 82 |
| `CHAT_MESSAGE_RANKED_GAME_STILL_SCORED_LEAVERS_GET_LOSS` | 83 |
| `CHAT_MESSAGE_ABANDON_RANKED_BEFORE_FIRST_BLOOD_PARTY` | 84 |
| `CHAT_MESSAGE_COMPENDIUM_LEVEL` | 85 |
| `CHAT_MESSAGE_VICTORY_PREDICTION_STREAK` | 86 |
| `CHAT_MESSAGE_ASSASSIN_ANNOUNCE` | 87 |
| `CHAT_MESSAGE_ASSASSIN_SUCCESS` | 88 |
| `CHAT_MESSAGE_ASSASSIN_DENIED` | 89 |
| `CHAT_MESSAGE_VICTORY_PREDICTION_SINGLE_USER_CONFIRM` | 90 |
| `CHAT_MESSAGE_EFFIGY_KILL` | 91 |
| `CHAT_MESSAGE_VOICE_TEXT_BANNED_OVERFLOW` | 92 |
| `CHAT_MESSAGE_YEAR_BEAST_KILLED` | 93 |
| `CHAT_MESSAGE_PAUSE_COUNTDOWN` | 94 |
| `CHAT_MESSAGE_COINS_WAGERED` | 95 |
| `CHAT_MESSAGE_HERO_NOMINATED_BAN` | 96 |
| `CHAT_MESSAGE_HERO_BANNED` | 97 |
| `CHAT_MESSAGE_HERO_BAN_COUNT` | 98 |
| `CHAT_MESSAGE_RIVER_PAINTED` | 99 |
| `CHAT_MESSAGE_SCAN_USED` | 100 |
| `CHAT_MESSAGE_SHRINE_KILLED` | 101 |
| `CHAT_MESSAGE_WAGER_TOKEN_SPENT` | 102 |
| `CHAT_MESSAGE_RANK_WAGER` | 103 |
| `CHAT_MESSAGE_NEW_PLAYER_REMINDER` | 104 |
| `CHAT_MESSAGE_OBSERVER_WARD_KILLED` | 105 |
| `CHAT_MESSAGE_SENTRY_WARD_KILLED` | 106 |
| `CHAT_MESSAGE_ITEM_PLACED_IN_NEUTRAL_STASH` | 107 |
| `CHAT_MESSAGE_HERO_CHOICE_INVALID` | 108 |
| `CHAT_MESSAGE_BOUNTY` | 109 |
| `CHAT_MESSAGE_ABILITY_DRAFT_START` | 110 |
| `CHAT_MESSAGE_HERO_FOUND_CANDY` | 111 |
| `CHAT_MESSAGE_ABILITY_DRAFT_RANDOMED` | 112 |
| `CHAT_MESSAGE_PRIVATE_COACH_CONNECTED` | 113 |
| `CHAT_MESSAGE_CANT_PAUSE_TOO_EARLY` | 115 |
| `CHAT_MESSAGE_HERO_KILL_WITH_PENGUIN` | 116 |
| `CHAT_MESSAGE_MINIBOSS_KILL` | 117 |
| `CHAT_MESSAGE_PLAYER_IN_GAME_BAN_TEXT` | 118 |
| `CHAT_MESSAGE_BANNER_PLANTED` | 119 |
| `CHAT_MESSAGE_ALCHEMIST_GRANTED_SCEPTER` | 120 |
| `CHAT_MESSAGE_PROTECTOR_SPAWNED` | 121 |
| `CHAT_MESSAGE_CRAFTING_XP` | 122 |
| `CHAT_MESSAGE_ROSHAN_ROAR` | 123 |

</details>

<details>
<summary><code>DOTA_NO_BATTLE_POINTS_REASONS</code> — values: 4</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `NO_BATTLE_POINTS_WRONG_LOBBY_TYPE` | 1 |
| `NO_BATTLE_POINTS_PRACTICE_BOTS` | 2 |
| `NO_BATTLE_POINTS_CHEATS_ENABLED` | 3 |
| `NO_BATTLE_POINTS_LOW_PRIORITY` | 4 |

</details>

<details>
<summary><code>DOTA_CHAT_INFORMATIONAL</code> — values: 5</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `INFO_COOP_BATTLE_POINTS_RULES` | 1 |
| `INFO_FROSTIVUS_ABANDON_REMINDER` | 2 |
| `INFO_RANKED_REMINDER` | 3 |
| `INFO_COOP_LOW_PRIORITY_PASSIVE_REMINDER` | 4 |
| `INFO_CUSTOM_GAME_PENALTY_REMINDER` | 5 |

</details>

<details>
<summary><code>DOTA_ABILITY_PING_TYPE</code> — values: 16</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `ABILITY_PING_READY` | 1 |
| `ABILITY_PING_MANA` | 2 |
| `ABILITY_PING_COOLDOWN` | 3 |
| `ABILITY_PING_ENEMY` | 4 |
| `ABILITY_PING_UNLEARNED` | 5 |
| `ABILITY_PING_INBACKPACK` | 6 |
| `ABILITY_PING_INSTASH` | 7 |
| `ABILITY_PING_ONCOURIER` | 8 |
| `ABILITY_PING_ALLY` | 9 |
| `ABILITY_PING_LEARN_READY` | 10 |
| `ABILITY_PING_WILL_LEARN` | 11 |
| `ABILITY_PING_FUTURE_LEARN` | 12 |
| `ABILITY_PING_NEUTRAL_OFFER` | 13 |
| `ABILITY_PING_NEUTRAL_REQUEST` | 14 |
| `ABILITY_PING_NEUTRAL_EQUIP` | 15 |
| `ABILITY_PING_INCOURIERBACKPACK` | 16 |

</details>

<details>
<summary><code>DOTA_REPLAY_STATE_EVENT</code> — values: 6</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `DOTA_REPLAY_STATE_EVENT_GAME_START` | 1 |
| `DOTA_REPLAY_STATE_EVENT_STARTING_HORN` | 2 |
| `DOTA_REPLAY_STATE_EVENT_FIRST_BLOOD` | 3 |
| `DOTA_REPLAY_STATE_EVENT_SHOWCASE` | 4 |
| `DOTA_REPLAY_STATE_EVENT_POST_GAME` | 5 |
| `DOTA_REPLAY_STATE_EVENT_WAIT_FOR_MAP` | 6 |

</details>

<details>
<summary><code>EDotaEntityMessages</code> — values: 7</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `DOTA_UNIT_SPEECH` | 0 |
| `DOTA_UNIT_SPEECH_MUTE` | 1 |
| `DOTA_UNIT_ADD_GESTURE` | 2 |
| `DOTA_UNIT_REMOVE_GESTURE` | 3 |
| `DOTA_UNIT_REMOVE_ALL_GESTURES` | 4 |
| `DOTA_UNIT_FADE_GESTURE` | 6 |
| `DOTA_UNIT_SPEECH_CLIENTSIDE_RULES` | 7 |

</details>

<details>
<summary><code>DOTA_OVERHEAD_ALERT</code> — values: 25</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `OVERHEAD_ALERT_GOLD` | 0 |
| `OVERHEAD_ALERT_DENY` | 1 |
| `OVERHEAD_ALERT_CRITICAL` | 2 |
| `OVERHEAD_ALERT_XP` | 3 |
| `OVERHEAD_ALERT_BONUS_SPELL_DAMAGE` | 4 |
| `OVERHEAD_ALERT_MISS` | 5 |
| `OVERHEAD_ALERT_DAMAGE` | 6 |
| `OVERHEAD_ALERT_EVADE` | 7 |
| `OVERHEAD_ALERT_BLOCK` | 8 |
| `OVERHEAD_ALERT_BONUS_POISON_DAMAGE` | 9 |
| `OVERHEAD_ALERT_HEAL` | 10 |
| `OVERHEAD_ALERT_MANA_ADD` | 11 |
| `OVERHEAD_ALERT_MANA_LOSS` | 12 |
| `OVERHEAD_ALERT_MAGICAL_BLOCK` | 16 |
| `OVERHEAD_ALERT_INCOMING_DAMAGE` | 17 |
| `OVERHEAD_ALERT_OUTGOING_DAMAGE` | 18 |
| `OVERHEAD_ALERT_DISABLE_RESIST` | 19 |
| `OVERHEAD_ALERT_DEATH` | 20 |
| `OVERHEAD_ALERT_BLOCKED` | 21 |
| `OVERHEAD_ALERT_ITEM_RECEIVED` | 22 |
| `OVERHEAD_ALERT_SHARD` | 23 |
| `OVERHEAD_ALERT_DEADLY_BLOW` | 24 |
| `OVERHEAD_ALERT_FORCE_MISS` | 25 |
| `OVERHEAD_ALERT_AEGIS` | 26 |
| `OVERHEAD_ALERT_DISPEL` | 27 |

</details>

<details>
<summary><code>DOTA_ROSHAN_PHASE</code> — values: 3</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_SRSP_ROSHAN_ALIVE` | 0 |
| `k_SRSP_ROSHAN_BASE_TIMER` | 1 |
| `k_SRSP_ROSHAN_VISIBLE_TIMER` | 2 |

</details>

<details>
<summary><code>DOTA_POSITION_CATEGORY</code> — values: 16</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `DOTA_POSITION_NONE` | 0 |
| `DOTA_POSITION_BOTTOM_LANE` | 1 |
| `DOTA_POSITION_MID_LANE` | 2 |
| `DOTA_POSITION_TOP_LANE` | 3 |
| `DOTA_POSITION_RADIANT_JUNGLE` | 4 |
| `DOTA_POSITION_DIRE_JUNGLE` | 5 |
| `DOTA_POSITION_RADIANT_ANCIENTS` | 6 |
| `DOTA_POSITION_DIRE_ANCIENTS` | 7 |
| `DOTA_POSITION_RADIANT_SECRET_SHOP` | 8 |
| `DOTA_POSITION_DIRE_SECRET_SHOP` | 9 |
| `DOTA_POSITION_RIVER` | 10 |
| `DOTA_POSITION_ROSHAN_PIT` | 11 |
| `DOTA_POSITION_RADIANT_BASE` | 12 |
| `DOTA_POSITION_DIRE_BASE` | 13 |
| `DOTA_POSITION_FOUNTAIN` | 14 |
| `DOTA_POSITION_OTHER` | 15 |

</details>

<details>
<summary><code>DOTA_ABILITY_TARGET_TYPE</code> — values: 6</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `DOTA_ABILITY_TARGET_NONE` | 0 |
| `DOTA_ABILITY_TARGET_SELF` | 1 |
| `DOTA_ABILITY_TARGET_ALLY_HERO` | 2 |
| `DOTA_ABILITY_TARGET_ALLY_CREEP` | 3 |
| `DOTA_ABILITY_TARGET_ENEMY_HERO` | 4 |
| `DOTA_ABILITY_TARGET_ENEMY_CREEP` | 5 |

</details>

<details>
<summary><code>EHeroStatType</code> — values: 22</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EHeroStatType_None` | 0 |
| `k_EHeroStatType_AxeTotalDamage` | 2000 |
| `k_EHeroStatType_BattleHungerDamage` | 2001 |
| `k_EHeroStatType_CounterHelixDamage` | 2002 |
| `k_EHeroStatType_CullingBladeDamage` | 2003 |
| `k_EHeroStatType_BerserkersCallCastCount` | 2004 |
| `k_EHeroStatType_BerserkersCallHeroesHitAverage` | 2005 |
| `k_EHeroStatType_BerserkersCallOtherUnitsHit` | 2006 |
| `k_EHeroStatType_BerserkersCallHeroAttacksTaken` | 2007 |
| `k_EHeroStatType_BerserkersCallOtherAttacksTaken` | 2008 |
| `k_EHeroStatType_BattleHungerCastCount` | 2009 |
| `k_EHeroStatType_BattleHungerPotentialDuration` | 2010 |
| `k_EHeroStatType_BattleHungerAverageDuration` | 2011 |
| `k_EHeroStatType_CounterHelixProcCount` | 2012 |
| `k_EHeroStatType_CounterHelixHeroProcCount` | 2013 |
| `k_EHeroStatType_CounterHelixHeroesHitAverage` | 2014 |
| `k_EHeroStatType_CounterHelixOtherUnitsHitCount` | 2015 |
| `k_EHeroStatType_CullingBladeCastCount` | 2016 |
| `k_EHeroStatType_CullingBladeKillCount` | 2017 |
| `k_EHeroStatType_CullingBladeAverageHealthCulled` | 2018 |
| `k_EHeroStatType_CullingBladeAverageDamageAvailable` | 2019 |
| `k_EHeroStatType_CullingBladeHeroBuffAverage` | 2020 |

</details>

<details>
<summary><code>EPlayerVoiceListenState</code> — values: 20</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `kPVLS_None` | 0 |
| `kPVLS_DeniedChatBanned` | 1 |
| `kPVLS_DeniedPartner` | 2 |
| `kPVLS_DeniedHLTVTalkerNotSpectator` | 3 |
| `kPVLS_DeniedHLTVNoTalkerPlayerID` | 4 |
| `kPVLS_DeniedHLTVTalkerNotBroadcaster` | 5 |
| `kPVLS_DeniedTeamSpectator` | 6 |
| `kPVLS_DeniedStudent` | 8 |
| `kPVLS_DeniedPrivateCoach` | 9 |
| `kPVLS_Denied` | 64 |
| `kPVLS_AllowHLTVTalkerIsBroadcaster` | 65 |
| `kPVLS_AllowCoBroadcaster` | 66 |
| `kPVLS_AllowAllChat` | 67 |
| `kPVLS_AllowStudentToCoach` | 68 |
| `kPVLS_AllowFellowStudent` | 69 |
| `kPVLS_AllowTalkerIsCoach` | 70 |
| `kPVLS_AllowCoachHearTeam` | 71 |
| `kPVLS_AllowSameTeam` | 72 |
| `kPVLS_AllowShowcase` | 73 |
| `kPVLS_AllowPrivateCoach` | 74 |

</details>

<details>
<summary><code>EProjectionEvent</code> — values: 2</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `ePE_FirstBlood` | 0 |
| `ePE_Killstreak_godlike` | 1 |

</details>

<details>
<summary><code>CDOTAResponseQuerySerialized.Fact.ValueType</code> — values: 4</summary>

- Parent: `CDOTAResponseQuerySerialized.Fact`

| Name | Number |
|---|---:|
| `NUMERIC` | 1 |
| `STRING` | 2 |
| `STRINGTABLE_INDEX` | 3 |
| `INT_NUMERIC` | 4 |

</details>

<details>
<summary><code>CDOTAUserMsg_GuildChallenge_Progress.EChallengeType</code> — values: 3</summary>

- Parent: `CDOTAUserMsg_GuildChallenge_Progress`

| Name | Number |
|---|---:|
| `k_EChallengeType_Invalid` | 0 |
| `k_EChallengeType_Cooperative` | 1 |
| `k_EChallengeType_Contract` | 2 |

</details>

<details>
<summary><code>CDOTAUserMsg_MadstoneAlert.EMadstoneAlertType</code> — values: 3</summary>

- Parent: `CDOTAUserMsg_MadstoneAlert`

| Name | Number |
|---|---:|
| `CraftAvailable` | 0 |
| `NeedMadstone` | 1 |
| `WaitingForNextTier` | 2 |

</details>

<details>
<summary><code>CDOTAUserMsg_MonsterHunter_HuntAlert.EHuntAlertType</code> — values: 7</summary>

- Parent: `CDOTAUserMsg_MonsterHunter_HuntAlert`

| Name | Number |
|---|---:|
| `MainObjective` | 0 |
| `MainObjectiveAll` | 1 |
| `HuntedBy` | 2 |
| `HuntedByAll` | 3 |
| `HunterDuel` | 4 |
| `HunterDuelAll` | 5 |
| `HuntSelection` | 6 |

</details>

<details>
<summary><code>CDOTAUserMsg_MonsterHunter_HuntAlert.EHuntStatusType</code> — values: 3</summary>

- Parent: `CDOTAUserMsg_MonsterHunter_HuntAlert`

| Name | Number |
|---|---:|
| `Pending` | 0 |
| `Success` | 1 |
| `Failed` | 2 |

</details>
