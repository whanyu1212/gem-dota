# base_gcmessages.proto

- Module: `base_gcmessages_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **3**
- Messages: **62** (top-level: 58)
- Enums: **6** (top-level: 2)

## Imports

- `steammessages.proto`
- `gcsdk_gcmessages.proto`
- `steammessages_steamlearn.steamworkssdk.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CGCStorePurchaseInit_LineItem</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_def_id` | `uint32` | `optional` | `` |  |
| 2 | `quantity` | `uint32` | `optional` | `` |  |
| 3 | `cost_in_local_currency` | `uint32` | `optional` | `` |  |
| 4 | `purchase_type` | `uint32` | `optional` | `` |  |
| 5 | `source_reference_id` | `uint64` | `optional` | `` |  |
| 6 | `price_index` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCStorePurchaseInit</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `country` | `string` | `optional` | `` |  |
| 2 | `language` | `int32` | `optional` | `` |  |
| 3 | `currency` | `int32` | `optional` | `` |  |
| 4 | `line_items` | `.CGCStorePurchaseInit_LineItem` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCStorePurchaseInitResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `int32` | `optional` | `` |  |
| 2 | `txn_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientPingData</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 4 | `relay_codes` | `fixed32` | `repeated` | `` | packed = true |
| 5 | `relay_pings` | `uint32` | `repeated` | `` | packed = true |
| 8 | `region_codes` | `uint32` | `repeated` | `` | packed = true |
| 9 | `region_pings` | `uint32` | `repeated` | `` | packed = true |
| 10 | `region_ping_failed_bitmask` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgInviteToParty</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steam_id` | `fixed64` | `optional` | `` |  |
| 2 | `client_version` | `uint32` | `optional` | `` |  |
| 3 | `team_id` | `uint32` | `optional` | `` |  |
| 4 | `as_coach` | `bool` | `optional` | `` |  |
| 5 | `ping_data` | `.CMsgClientPingData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgInviteToLobby</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steam_id` | `fixed64` | `optional` | `` |  |
| 2 | `client_version` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgInvitationCreated</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `group_id` | `uint64` | `optional` | `` |  |
| 2 | `steam_id` | `fixed64` | `optional` | `` |  |
| 3 | `user_offline` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPartyInviteResponse</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `party_id` | `uint64` | `optional` | `` |  |
| 2 | `accept` | `bool` | `optional` | `` |  |
| 3 | `client_version` | `uint32` | `optional` | `` |  |
| 8 | `ping_data` | `.CMsgClientPingData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgLobbyInviteResponse</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `lobby_id` | `fixed64` | `optional` | `` |  |
| 2 | `accept` | `bool` | `optional` | `` |  |
| 3 | `client_version` | `uint32` | `optional` | `` |  |
| 6 | `custom_game_crc` | `fixed64` | `optional` | `` |  |
| 7 | `custom_game_timestamp` | `fixed32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgKickFromParty</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steam_id` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgLeaveParty</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgCustomGameInstallStatus</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `status` | `.ECustomGameInstallStatus` | `optional` | `` | default = k_ECustomGameInstallStatus_Unknown |
| 2 | `message` | `string` | `optional` | `` |  |
| 3 | `latest_timestamp_from_steam` | `fixed32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerAvailable</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `custom_game_install_status` | `.CMsgCustomGameInstallStatus` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgLANServerAvailable</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `lobby_id` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CSOEconGameAccountClient</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `additional_backpack_slots` | `uint32` | `optional` | `` | default = 0 |
| 2 | `trial_account` | `bool` | `optional` | `` | default = false |
| 3 | `eligible_for_online_play` | `bool` | `optional` | `` | default = true |
| 4 | `need_to_choose_most_helpful_friend` | `bool` | `optional` | `` |  |
| 5 | `in_coaches_list` | `bool` | `optional` | `` |  |
| 6 | `trade_ban_expiration` | `fixed32` | `optional` | `` |  |
| 7 | `duel_ban_expiration` | `fixed32` | `optional` | `` |  |
| 9 | `made_first_purchase` | `bool` | `optional` | `` | default = false |

</details>

<details>
<summary><code>CMsgApplyStrangePart</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `strange_part_item_id` | `uint64` | `optional` | `` |  |
| 2 | `item_item_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgApplyPennantUpgrade</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `upgrade_item_id` | `uint64` | `optional` | `` |  |
| 2 | `pennant_item_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgApplyEggEssence</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `essence_item_id` | `uint64` | `optional` | `` |  |
| 2 | `egg_item_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CSOEconItemAttribute</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `def_index` | `uint32` | `optional` | `` | default = 65535 |
| 2 | `value` | `uint32` | `optional` | `` |  |
| 3 | `value_bytes` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CSOEconItemEquipped</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `new_class` | `uint32` | `optional` | `` |  |
| 2 | `new_slot` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CSOEconItem</code> — fields: 14; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `id` | `uint64` | `optional` | `` |  |
| 2 | `account_id` | `uint32` | `optional` | `` |  |
| 3 | `inventory` | `uint32` | `optional` | `` |  |
| 4 | `def_index` | `uint32` | `optional` | `` |  |
| 5 | `quantity` | `uint32` | `optional` | `` | default = 1 |
| 6 | `level` | `uint32` | `optional` | `` | default = 1 |
| 7 | `quality` | `uint32` | `optional` | `` | default = 4 |
| 8 | `flags` | `uint32` | `optional` | `` | default = 0 |
| 9 | `origin` | `uint32` | `optional` | `` | default = 0 |
| 12 | `attribute` | `.CSOEconItemAttribute` | `repeated` | `` |  |
| 13 | `interior_item` | `.CSOEconItem` | `optional` | `` |  |
| 15 | `style` | `uint32` | `optional` | `` | default = 0 |
| 16 | `original_id` | `uint64` | `optional` | `` |  |
| 18 | `equipped_state` | `.CSOEconItemEquipped` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSortItems</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `sort_type` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgItemAcknowledged</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `inventory` | `uint32` | `optional` | `` |  |
| 3 | `def_index` | `uint32` | `optional` | `` |  |
| 4 | `quality` | `uint32` | `optional` | `` |  |
| 5 | `rarity` | `uint32` | `optional` | `` |  |
| 6 | `origin` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSetItemPositions</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_positions` | `.CMsgSetItemPositions.ItemPosition` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSetItemPositions.ItemPosition</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSetItemPositions`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_id` | `uint64` | `optional` | `` |  |
| 2 | `position` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCStorePurchaseCancel</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `txn_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCStorePurchaseCancelResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCStorePurchaseFinalize</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `txn_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCStorePurchaseFinalizeResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `uint32` | `optional` | `` |  |
| 2 | `item_ids` | `uint64` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCBannedWordListUpdated</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `group_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCDirtySDOCache</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `sdo_type` | `uint32` | `optional` | `` |  |
| 2 | `key_uint64` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSDONoMemcached</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgGCToGCUpdateSQLKeyValue</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `key_name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCServerVersionUpdated</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `server_version` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCClientVersionUpdated</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `client_version` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCWebAPIAccountChanged</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgExtractGems</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `tool_item_id` | `uint64` | `optional` | `` |  |
| 2 | `item_item_id` | `uint64` | `optional` | `` |  |
| 3 | `item_socket_id` | `uint32` | `optional` | `` | default = 65535 |

</details>

<details>
<summary><code>CMsgExtractGemsResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_id` | `uint64` | `optional` | `` |  |
| 2 | `response` | `.CMsgExtractGemsResponse.EExtractGems` | `optional` | `` | default = k_ExtractGems_Succeeded |

</details>

<details>
<summary><code>CMsgAddSocket</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `tool_item_id` | `uint64` | `optional` | `` |  |
| 2 | `item_item_id` | `uint64` | `optional` | `` |  |
| 3 | `unusual` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgAddSocketResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_id` | `uint64` | `optional` | `` |  |
| 2 | `updated_socket_index` | `uint32` | `repeated` | `` |  |
| 3 | `response` | `.CMsgAddSocketResponse.EAddSocket` | `optional` | `` | default = k_AddSocket_Succeeded |

</details>

<details>
<summary><code>CMsgAddItemToSocketData</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `gem_item_id` | `uint64` | `optional` | `` |  |
| 2 | `socket_index` | `uint32` | `optional` | `` | default = 65535 |

</details>

<details>
<summary><code>CMsgAddItemToSocket</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_item_id` | `uint64` | `optional` | `` |  |
| 2 | `gems_to_socket` | `.CMsgAddItemToSocketData` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgAddItemToSocketResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_item_id` | `uint64` | `optional` | `` |  |
| 2 | `updated_socket_index` | `uint32` | `repeated` | `` |  |
| 3 | `response` | `.CMsgAddItemToSocketResponse.EAddGem` | `optional` | `` | default = k_AddGem_Succeeded |

</details>

<details>
<summary><code>CMsgResetStrangeGemCount</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_item_id` | `uint64` | `optional` | `` |  |
| 2 | `socket_index` | `uint32` | `optional` | `` | default = 65535 |

</details>

<details>
<summary><code>CMsgResetStrangeGemCountResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgResetStrangeGemCountResponse.EResetGem` | `optional` | `` | default = k_ResetGem_Succeeded |

</details>

<details>
<summary><code>CMsgGCToClientPollFileRequest</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `file_name` | `string` | `optional` | `` |  |
| 2 | `client_version` | `uint32` | `optional` | `` |  |
| 3 | `poll_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientPollFileResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `poll_id` | `uint32` | `optional` | `` |  |
| 2 | `file_size` | `uint32` | `optional` | `` |  |
| 3 | `file_crc` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCPerformManualOp</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `op_id` | `uint64` | `optional` | `` |  |
| 2 | `group_code` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCPerformManualOpCompleted</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `success` | `bool` | `optional` | `` |  |
| 2 | `source_gc` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CMsgGCToGCReloadServerRegionSettings</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgGCAdditionalWelcomeMsgList</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `welcome_messages` | `.CExtraMsgBlock` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgApplyRemoteConVars</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `con_vars` | `.CMsgApplyRemoteConVars.ConVar` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgApplyRemoteConVars.ConVar</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgApplyRemoteConVars`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `value` | `string` | `optional` | `` |  |
| 3 | `version_min` | `uint32` | `optional` | `` |  |
| 4 | `version_max` | `uint32` | `optional` | `` |  |
| 5 | `platform` | `.EGCPlatform` | `optional` | `` | default = k_eGCPlatform_None |

</details>

<details>
<summary><code>CMsgGCToClientApplyRemoteConVars</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `msg` | `.CMsgApplyRemoteConVars` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToServerApplyRemoteConVars</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `msg` | `.CMsgApplyRemoteConVars` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCIntegrityStatus</code> — fields: 3; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `report` | `string` | `optional` | `` |  |
| 2 | `secure_allowed` | `bool` | `optional` | `` |  |
| 3 | `diagnostics` | `.CMsgClientToGCIntegrityStatus.keyvalue` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCIntegrityStatus.keyvalue</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCIntegrityStatus`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `id` | `uint32` | `optional` | `` |  |
| 2 | `extended` | `uint32` | `optional` | `` |  |
| 3 | `value` | `uint64` | `optional` | `` |  |
| 4 | `string_value` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCAggregateMetrics</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `metrics` | `.CMsgClientToGCAggregateMetrics.SingleMetric` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCAggregateMetrics.SingleMetric</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCAggregateMetrics`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `metric_name` | `string` | `optional` | `` |  |
| 2 | `metric_count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientAggregateMetricsBackoff</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `upload_rate_modifier` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToServerSteamLearnAccessTokensChanged</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `access_tokens` | `.CMsgSteamLearnAccessTokens` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToServerSteamLearnUseHTTP</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `use_http` | `bool` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>EGCBaseMsg</code> — values: 24</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EMsgGCInviteToParty` | 4501 |
| `k_EMsgGCInvitationCreated` | 4502 |
| `k_EMsgGCPartyInviteResponse` | 4503 |
| `k_EMsgGCKickFromParty` | 4504 |
| `k_EMsgGCLeaveParty` | 4505 |
| `k_EMsgGCServerAvailable` | 4506 |
| `k_EMsgGCClientConnectToServer` | 4507 |
| `k_EMsgGCGameServerInfo` | 4508 |
| `k_EMsgGCLANServerAvailable` | 4511 |
| `k_EMsgGCInviteToLobby` | 4512 |
| `k_EMsgGCLobbyInviteResponse` | 4513 |
| `k_EMsgGCToClientPollFileRequest` | 4514 |
| `k_EMsgGCToClientPollFileResponse` | 4515 |
| `k_EMsgGCToGCPerformManualOp` | 4516 |
| `k_EMsgGCToGCPerformManualOpCompleted` | 4517 |
| `k_EMsgGCToGCReloadServerRegionSettings` | 4518 |
| `k_EMsgGCAdditionalWelcomeMsgList` | 4519 |
| `k_EMsgGCToClientApplyRemoteConVars` | 4520 |
| `k_EMsgGCToServerApplyRemoteConVars` | 4521 |
| `k_EMsgClientToGCIntegrityStatus` | 4522 |
| `k_EMsgClientToGCAggregateMetrics` | 4523 |
| `k_EMsgGCToClientAggregateMetricsBackoff` | 4524 |
| `k_EMsgGCToServerSteamLearnAccessTokensChanged` | 4525 |
| `k_EMsgGCToServerSteamLearnUseHTTP` | 4526 |

</details>

<details>
<summary><code>ECustomGameInstallStatus</code> — values: 10</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_ECustomGameInstallStatus_Unknown` | 0 |
| `k_ECustomGameInstallStatus_Ready` | 1 |
| `k_ECustomGameInstallStatus_Busy` | 2 |
| `k_ECustomGameInstallStatus_FailedGeneric` | 101 |
| `k_ECustomGameInstallStatus_FailedInternalError` | 102 |
| `k_ECustomGameInstallStatus_RequestedTimestampTooOld` | 103 |
| `k_ECustomGameInstallStatus_RequestedTimestampTooNew` | 104 |
| `k_ECustomGameInstallStatus_CRCMismatch` | 105 |
| `k_ECustomGameInstallStatus_FailedSteam` | 106 |
| `k_ECustomGameInstallStatus_FailedCanceled` | 107 |

</details>

<details>
<summary><code>CMsgExtractGemsResponse.EExtractGems</code> — values: 5</summary>

- Parent: `CMsgExtractGemsResponse`

| Name | Number |
|---|---:|
| `k_ExtractGems_Succeeded` | 0 |
| `k_ExtractGems_Failed_ToolIsInvalid` | 1 |
| `k_ExtractGems_Failed_ItemIsInvalid` | 2 |
| `k_ExtractGems_Failed_ToolCannotRemoveGem` | 3 |
| `k_ExtractGems_Failed_FailedToRemoveGem` | 4 |

</details>

<details>
<summary><code>CMsgAddSocketResponse.EAddSocket</code> — values: 4</summary>

- Parent: `CMsgAddSocketResponse`

| Name | Number |
|---|---:|
| `k_AddSocket_Succeeded` | 0 |
| `k_AddSocket_Failed_ToolIsInvalid` | 1 |
| `k_AddSocket_Failed_ItemCannotBeSocketed` | 2 |
| `k_AddSocket_Failed_FailedToAddSocket` | 3 |

</details>

<details>
<summary><code>CMsgAddItemToSocketResponse.EAddGem</code> — values: 8</summary>

- Parent: `CMsgAddItemToSocketResponse`

| Name | Number |
|---|---:|
| `k_AddGem_Succeeded` | 0 |
| `k_AddGem_Failed_GemIsInvalid` | 1 |
| `k_AddGem_Failed_ItemIsInvalid` | 2 |
| `k_AddGem_Failed_FailedToAddGem` | 3 |
| `k_AddGem_Failed_InvalidGemTypeForSocket` | 4 |
| `k_AddGem_Failed_InvalidGemTypeForHero` | 5 |
| `k_AddGem_Failed_InvalidGemTypeForSlot` | 6 |
| `k_AddGem_Failed_SocketContainsUnremovableGem` | 7 |

</details>

<details>
<summary><code>CMsgResetStrangeGemCountResponse.EResetGem</code> — values: 5</summary>

- Parent: `CMsgResetStrangeGemCountResponse`

| Name | Number |
|---|---:|
| `k_ResetGem_Succeeded` | 0 |
| `k_ResetGem_Failed_FailedToResetGem` | 1 |
| `k_ResetGem_Failed_ItemIsInvalid` | 2 |
| `k_ResetGem_Failed_InvalidSocketId` | 3 |
| `k_ResetGem_Failed_SocketCannotBeReset` | 4 |

</details>
