# dota_gcmessages_common_item_battler.proto

- Module: `dota_gcmessages_common_item_battler_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **4**
- Messages: **22** (top-level: 19)
- Enums: **6** (top-level: 2)

## Imports

- `steammessages.proto`
- `dota_shared_enums.proto`
- `dota_gcmessages_common.proto`
- `gcsdk_gcmessages.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgItemBattlerPlayerInfo</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `rank` | `uint32` | `optional` | `` |  |
| 3 | `run_count` | `uint32` | `optional` | `` |  |
| 4 | `victory_count` | `uint32` | `optional` | `` |  |
| 5 | `concede_count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgItemBattlerItemModifier</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `type` | `uint32` | `optional` | `` |  |
| 2 | `value` | `float` | `optional` | `` |  |
| 3 | `multiplicative` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgItemBattlerItem</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_definition_id` | `uint32` | `optional` | `` |  |
| 2 | `item_instance_id` | `uint32` | `optional` | `` |  |
| 3 | `item_container_id` | `uint32` | `optional` | `` |  |
| 4 | `position_x` | `uint32` | `optional` | `` |  |
| 5 | `position_y` | `uint32` | `optional` | `` |  |
| 6 | `permanent_modifiers` | `.CMsgItemBattlerItemModifier` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgItemBattlerItemContainer</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_container_id` | `uint32` | `optional` | `` |  |
| 2 | `item_slot_ids` | `uint32` | `repeated` | `` |  |
| 3 | `width` | `int32` | `optional` | `` |  |
| 4 | `height` | `int32` | `optional` | `` |  |
| 5 | `is_shop` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgItemBattlerFightEvent</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_instance_id` | `uint32` | `optional` | `` |  |
| 2 | `item_target_instance_ids` | `uint32` | `repeated` | `` |  |
| 3 | `tick` | `uint32` | `optional` | `` |  |
| 4 | `effect` | `uint32` | `optional` | `` |  |
| 5 | `value` | `int32` | `optional` | `` |  |
| 6 | `critical` | `bool` | `optional` | `` |  |
| 7 | `lifesteal_healing` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgItemBattlerFightResult</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `win` | `bool` | `optional` | `` |  |
| 2 | `events` | `.CMsgItemBattlerFightEvent` | `repeated` | `` |  |
| 3 | `error` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgItemBattlerPlayerData</code> — fields: 15; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `hero_id` | `uint32` | `optional` | `` |  |
| 3 | `monster_id` | `uint32` | `optional` | `` |  |
| 4 | `board` | `.CMsgItemBattlerItemContainer` | `optional` | `` |  |
| 5 | `wins` | `int32` | `optional` | `` |  |
| 6 | `losses` | `int32` | `optional` | `` |  |
| 7 | `prestige` | `int32` | `optional` | `` |  |
| 8 | `level` | `uint32` | `optional` | `` |  |
| 9 | `experience` | `int32` | `optional` | `` |  |
| 10 | `skills` | `uint32` | `repeated` | `` |  |
| 11 | `income` | `int32` | `optional` | `` |  |
| 12 | `gold` | `int32` | `optional` | `` |  |
| 13 | `base_max_health` | `uint32` | `optional` | `` |  |
| 14 | `bonus_max_health` | `uint32` | `optional` | `` |  |
| 15 | `abilities` | `.CMsgItemBattlerItemContainer` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgItemBattlerEncounterData</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `is_shop` | `bool` | `optional` | `` |  |
| 2 | `encounter_id` | `uint32` | `optional` | `` |  |
| 3 | `shop_items` | `.CMsgItemBattlerItemContainer` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgItemBattlerGhostData</code> — fields: 4; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_data` | `.CMsgItemBattlerPlayerData` | `optional` | `` |  |
| 2 | `items` | `.CMsgItemBattlerGhostData.ItemsEntry` | `repeated` | `` |  |
| 3 | `day` | `int32` | `optional` | `` |  |
| 4 | `abilities` | `.CMsgItemBattlerGhostData.AbilitiesEntry` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgItemBattlerGhostData.ItemsEntry</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgItemBattlerGhostData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `key` | `uint32` | `optional` | `` |  |
| 2 | `value` | `.CMsgItemBattlerItem` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgItemBattlerGhostData.AbilitiesEntry</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgItemBattlerGhostData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `key` | `uint32` | `optional` | `` |  |
| 2 | `value` | `.CMsgItemBattlerItem` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgItemBattlerWorldData</code> — fields: 14; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `run_active` | `bool` | `optional` | `` |  |
| 2 | `run_id` | `uint32` | `optional` | `` |  |
| 3 | `game_state` | `.EItemBattlerGameState` | `optional` | `` | default = k_eGameState_Invalid |
| 4 | `player_data` | `.CMsgItemBattlerPlayerData` | `optional` | `` |  |
| 5 | `opponent_data` | `.CMsgItemBattlerPlayerData` | `optional` | `` |  |
| 6 | `stash` | `.CMsgItemBattlerItemContainer` | `optional` | `` |  |
| 7 | `encounter` | `.CMsgItemBattlerEncounterData` | `optional` | `` |  |
| 8 | `fight_result` | `.CMsgItemBattlerFightResult` | `optional` | `` |  |
| 9 | `items` | `.CMsgItemBattlerWorldData.ItemsEntry` | `repeated` | `` |  |
| 10 | `day` | `int32` | `optional` | `` |  |
| 11 | `hour` | `int32` | `optional` | `` |  |
| 12 | `encounter_choices` | `uint32` | `repeated` | `` |  |
| 13 | `monster_choices` | `uint32` | `repeated` | `` |  |
| 14 | `conceded` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgItemBattlerWorldData.ItemsEntry</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgItemBattlerWorldData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `key` | `uint32` | `optional` | `` |  |
| 2 | `value` | `.CMsgItemBattlerItem` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgItemBattlerGameData</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `seed` | `uint32` | `optional` | `` |  |
| 2 | `world_data` | `.CMsgItemBattlerWorldData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCItemBattlerGetUserData</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCItemBattlerGetUserDataResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCItemBattlerGetUserDataResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `world_data` | `.CMsgItemBattlerWorldData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgItemBattlerItemAction</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCItemBattlerGameAction</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `action` | `.CMsgClientToGCItemBattlerGameAction.EAction` | `optional` | `` | default = k_eInvalid |
| 2 | `choice_index` | `uint32` | `optional` | `` |  |
| 3 | `item_instance_id` | `uint32` | `optional` | `` |  |
| 4 | `item_container_id` | `uint32` | `optional` | `` |  |
| 5 | `item_position_x` | `uint32` | `optional` | `` |  |
| 6 | `item_position_y` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCItemBattlerGameActionResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCItemBattlerGameActionResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `updated_world_data` | `.CMsgItemBattlerWorldData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCItemBattlerDevGrantItem</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_definition_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCItemBattlerDevGrantItemResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCItemBattlerDevGrantItemResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgGCToClientItemBattlerUserDataUpdated</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `world_data` | `.CMsgItemBattlerWorldData` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>EItemBattlerAuditAction</code> — values: 1</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eItemBattlerAuditAction_Invalid` | 0 |

</details>

<details>
<summary><code>EItemBattlerGameState</code> — values: 11</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eGameState_Invalid` | 0 |
| `k_eGameState_ChoosingEncounter` | 1 |
| `k_eGameState_Encounter_Choice` | 2 |
| `k_eGameState_Encounter_Shop` | 3 |
| `k_eGameState_ChoosingMonster` | 4 |
| `k_eGameState_SearchingForOpponent` | 5 |
| `k_eGameState_ShowingOpponent` | 6 |
| `k_eGameState_PreFight` | 7 |
| `k_eGameState_Fight` | 8 |
| `k_eGameState_PostFight` | 9 |
| `k_eGameState_GameOver` | 10 |

</details>

<details>
<summary><code>CMsgClientToGCItemBattlerGetUserDataResponse.EResponse</code> — values: 5</summary>

- Parent: `CMsgClientToGCItemBattlerGetUserDataResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |

</details>

<details>
<summary><code>CMsgClientToGCItemBattlerGameAction.EAction</code> — values: 8</summary>

- Parent: `CMsgClientToGCItemBattlerGameAction`

| Name | Number |
|---|---:|
| `k_eInvalid` | 0 |
| `k_eStartNewRun` | 1 |
| `k_eForfeitRun` | 2 |
| `k_eChooseOption` | 3 |
| `k_eContinue` | 4 |
| `k_eItemMove` | 5 |
| `k_eItemPurchase` | 6 |
| `k_eItemSell` | 7 |

</details>

<details>
<summary><code>CMsgClientToGCItemBattlerGameActionResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCItemBattlerGameActionResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidAction` | 5 |

</details>

<details>
<summary><code>CMsgClientToGCItemBattlerDevGrantItemResponse.EResponse</code> — values: 5</summary>

- Parent: `CMsgClientToGCItemBattlerDevGrantItemResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |

</details>
