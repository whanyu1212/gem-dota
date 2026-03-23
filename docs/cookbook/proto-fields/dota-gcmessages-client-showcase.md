# dota_gcmessages_client_showcase.proto

- Module: `dota_gcmessages_client_showcase_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **9**
- Messages: **60** (top-level: 49)
- Enums: **20** (top-level: 6)

## Imports

- `steammessages.proto`
- `dota_shared_enums.proto`
- `dota_gcmessages_common.proto`
- `dota_gcmessages_webapi.proto`
- `gcsdk_gcmessages.proto`
- `base_gcmessages.proto`
- `econ_gcmessages.proto`
- `dota_gcmessages_client.proto`
- `valveextensions.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgShowcaseEconItemReference</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `id` | `uint64` | `optional` | `` |  |
| 2 | `original_id` | `uint64` | `optional` | `` |  |
| 3 | `definition_index` | `uint32` | `optional` | `` |  |
| 4 | `equipment_slot_index` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CMsgHeroPlusInfo</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `flags` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgShowcaseItem_Trophy</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `data` | `.CMsgShowcaseItem_Trophy.Data` | `optional` | `` |  |
| 2 | `trophy_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgShowcaseItem_Trophy.Data</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgShowcaseItem_Trophy`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `trophy_score` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgShowcaseItem_EconItem</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `data` | `.CMsgShowcaseItem_EconItem.Data` | `optional` | `` |  |
| 2 | `ref` | `.CMsgShowcaseEconItemReference` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgShowcaseItem_EconItem.Data</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgShowcaseItem_EconItem`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `econ_item` | `.CSOEconItem` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgShowcaseItem_Hero</code> — fields: 12; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `data` | `.CMsgShowcaseItem_Hero.Data` | `optional` | `` |  |
| 2 | `hero_id` | `int32` | `optional` | `` |  |
| 3 | `econ_item_refs` | `.CMsgShowcaseEconItemReference` | `repeated` | `` |  |
| 4 | `rotation` | `uint32` | `optional` | `` |  |
| 5 | `flags` | `uint32` | `optional` | `` |  |
| 6 | `plus_info` | `.CMsgHeroPlusInfo` | `optional` | `` |  |
| 7 | `animation_name` | `string` | `optional` | `` |  |
| 8 | `animation_playback_speed` | `uint32` | `optional` | `` | default = 100 |
| 9 | `animation_offset` | `uint32` | `optional` | `` |  |
| 10 | `zoom` | `uint32` | `optional` | `` | default = 100 |
| 11 | `slot_index` | `uint32` | `optional` | `` |  |
| 12 | `model_index` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgShowcaseItem_Hero.Data</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgShowcaseItem_Hero`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `econ_items` | `.CSOEconItem` | `repeated` | `` |  |
| 2 | `actual_hero_id` | `int32` | `optional` | `` |  |
| 3 | `plus_hero_xp` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgShowcaseItem_HeroIcon</code> — fields: 3; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `data` | `.CMsgShowcaseItem_HeroIcon.Data` | `optional` | `` |  |
| 2 | `hero_id` | `int32` | `optional` | `` |  |
| 3 | `econ_item_ref` | `.CMsgShowcaseEconItemReference` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgShowcaseItem_HeroIcon.Data</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgShowcaseItem_HeroIcon`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `econ_item` | `.CSOEconItem` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgShowcaseItem_PlayerMatch</code> — fields: 3; oneofs: 0; nested messages: 1; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `data` | `.CMsgShowcaseItem_PlayerMatch.Data` | `optional` | `` |  |
| 2 | `match_id` | `uint64` | `optional` | `` |  |
| 3 | `player_slot` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgShowcaseItem_PlayerMatch.Data</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgShowcaseItem_PlayerMatch`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `timestamp` | `uint32` | `optional` | `` |  |
| 3 | `duration` | `uint32` | `optional` | `` |  |
| 4 | `game_mode` | `.DOTA_GameMode` | `optional` | `` | default = DOTA_GAMEMODE_NONE |
| 5 | `outcome` | `.CMsgShowcaseItem_PlayerMatch.EPlayerOutcome` | `optional` | `` | default = k_eInvalid |
| 6 | `kills` | `uint32` | `optional` | `` |  |
| 7 | `deaths` | `uint32` | `optional` | `` |  |
| 8 | `assists` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgShowcaseItem_ChatWheel</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `data` | `.CMsgShowcaseItem_ChatWheel.Data` | `optional` | `` |  |
| 2 | `chat_wheel_message_id` | `uint32` | `optional` | `` | default = 4294967295 |

</details>

<details>
<summary><code>CMsgShowcaseItem_ChatWheel.Data</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgShowcaseItem_ChatWheel`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgShowcaseItem_Emoticon</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `data` | `.CMsgShowcaseItem_Emoticon.Data` | `optional` | `` |  |
| 2 | `emoticon_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgShowcaseItem_Emoticon.Data</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgShowcaseItem_Emoticon`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgShowcaseItem_SpiderGraph</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `data` | `.CMsgShowcaseItem_SpiderGraph.Data` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgShowcaseItem_SpiderGraph.Data</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgShowcaseItem_SpiderGraph`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgShowcaseItem_UserFeed</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `data` | `.CMsgShowcaseItem_UserFeed.Data` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgShowcaseItem_UserFeed.Data</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgShowcaseItem_UserFeed`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgShowcaseItem_Stat</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `data` | `.CMsgShowcaseItem_Stat.Data` | `optional` | `` |  |
| 2 | `stat_id` | `.CMsgDOTAProfileCard.EStatID` | `optional` | `` | default = k_eStat_Wins |

</details>

<details>
<summary><code>CMsgShowcaseItem_Stat.Data</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgShowcaseItem_Stat`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `stat_score` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgShowcaseBackground</code> — fields: 5; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `data` | `.CMsgShowcaseBackground.Data` | `optional` | `` |  |
| 2 | `loading_screen_ref` | `.CMsgShowcaseEconItemReference` | `optional` | `` |  |
| 3 | `dim` | `uint32` | `optional` | `` |  |
| 4 | `blur` | `uint32` | `optional` | `` |  |
| 5 | `background_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgShowcaseBackground.Data</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgShowcaseBackground`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `loading_screen` | `.CSOEconItem` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgShowcaseItemData</code> — fields: 20; oneofs: 1; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: `item`

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `trophy` | `.CMsgShowcaseItem_Trophy` | `oneof` | `item` |  |
| 2 | `econ_item_icon` | `.CMsgShowcaseItem_EconItem` | `oneof` | `item` |  |
| 3 | `sticker` | `.CMsgShowcaseItem_EconItem` | `oneof` | `item` |  |
| 4 | `hero_model` | `.CMsgShowcaseItem_Hero` | `oneof` | `item` |  |
| 5 | `player_match` | `.CMsgShowcaseItem_PlayerMatch` | `oneof` | `item` |  |
| 6 | `chat_wheel` | `.CMsgShowcaseItem_ChatWheel` | `oneof` | `item` |  |
| 7 | `spray` | `.CMsgShowcaseItem_ChatWheel` | `oneof` | `item` |  |
| 8 | `emoticon` | `.CMsgShowcaseItem_Emoticon` | `oneof` | `item` |  |
| 10 | `courier` | `.CMsgShowcaseItem_EconItem` | `oneof` | `item` |  |
| 11 | `ward` | `.CMsgShowcaseItem_EconItem` | `oneof` | `item` |  |
| 12 | `hero_icon` | `.CMsgShowcaseItem_HeroIcon` | `oneof` | `item` |  |
| 13 | `spider_graph` | `.CMsgShowcaseItem_SpiderGraph` | `oneof` | `item` |  |
| 14 | `user_feed` | `.CMsgShowcaseItem_UserFeed` | `oneof` | `item` |  |
| 15 | `stat` | `.CMsgShowcaseItem_Stat` | `oneof` | `item` |  |
| 16 | `roshan` | `.CMsgShowcaseItem_EconItem` | `oneof` | `item` |  |
| 17 | `creep` | `.CMsgShowcaseItem_EconItem` | `oneof` | `item` |  |
| 18 | `tower` | `.CMsgShowcaseItem_EconItem` | `oneof` | `item` |  |
| 19 | `effigy` | `.CMsgShowcaseItem_EconItem` | `oneof` | `item` |  |
| 20 | `decoration` | `.CMsgShowcaseItem_EconItem` | `oneof` | `item` |  |
| 100 | `background` | `.CMsgShowcaseBackground` | `oneof` | `item` |  |

</details>

<details>
<summary><code>CMsgShowcaseItemPosition</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `position_x` | `int32` | `optional` | `` |  |
| 2 | `position_y` | `int32` | `optional` | `` |  |
| 3 | `scale` | `uint32` | `optional` | `` |  |
| 4 | `width` | `uint32` | `optional` | `` |  |
| 5 | `height` | `uint32` | `optional` | `` |  |
| 6 | `rotation` | `uint32` | `optional` | `` |  |
| 7 | `parent_id` | `uint32` | `optional` | `` |  |
| 8 | `parent_attachment_point_id` | `uint32` | `optional` | `` |  |
| 9 | `attachment_anchor_x` | `uint32` | `optional` | `` |  |
| 10 | `attachment_anchor_y` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgShowcaseItem</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `showcase_item_id` | `uint32` | `optional` | `` |  |
| 2 | `item_position` | `.CMsgShowcaseItemPosition` | `optional` | `` |  |
| 3 | `item_data` | `.CMsgShowcaseItemData` | `optional` | `` |  |
| 4 | `state` | `.EShowcaseItemState` | `optional` | `` | default = k_eShowcaseItemState_Ok |
| 5 | `flags` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgShowcase</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `showcase_items` | `.CMsgShowcaseItem` | `repeated` | `` |  |
| 3 | `background` | `.CMsgShowcaseItem` | `optional` | `` |  |
| 4 | `moderation_state` | `.CMsgShowcase.EModerationState` | `optional` | `` | default = k_eModerationState_Ok |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseGetUserData</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `showcase_type` | `.EShowcaseType` | `optional` | `` | default = k_eShowcaseType_Invalid |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseGetUserDataResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCShowcaseGetUserDataResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `showcase` | `.CMsgShowcase` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseSetUserData</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `showcase_type` | `.EShowcaseType` | `optional` | `` | default = k_eShowcaseType_Invalid |
| 2 | `showcase` | `.CMsgShowcase` | `optional` | `` |  |
| 3 | `format_version` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseSetUserDataResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCShowcaseSetUserDataResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `validated_showcase` | `.CMsgShowcase` | `optional` | `` |  |
| 3 | `locked_until_timestamp` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseSubmitReport</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_account_id` | `uint32` | `optional` | `` |  |
| 2 | `showcase_type` | `.EShowcaseType` | `optional` | `` | default = k_eShowcaseType_Invalid |
| 3 | `report_comment` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseSubmitReportResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCShowcaseSubmitReportResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgShowcaseReportsRollupInfo</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `rollup_id` | `uint32` | `optional` | `` |  |
| 2 | `start_timestamp` | `uint32` | `optional` | `` |  |
| 3 | `end_timestamp` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgShowcaseReportsRollupList</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `rollups` | `.CMsgShowcaseReportsRollupInfo` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgShowcaseReportsRollupEntry</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `showcase_type` | `.EShowcaseType` | `optional` | `` | default = k_eShowcaseType_Invalid |
| 3 | `report_count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgShowcaseReportsRollup</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `rollup_info` | `.CMsgShowcaseReportsRollupInfo` | `optional` | `` |  |
| 2 | `rollup_entries` | `.CMsgShowcaseReportsRollupEntry` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseAdminGetReportsRollupList</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseAdminGetReportsRollupListResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCShowcaseAdminGetReportsRollupListResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `rollup_list` | `.CMsgShowcaseReportsRollupList` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseAdminGetReportsRollup</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `rollup_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseAdminGetReportsRollupResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCShowcaseAdminGetReportsRollupResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `rollup` | `.CMsgShowcaseReportsRollup` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgShowcaseAuditEntry</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `showcase_type` | `.EShowcaseType` | `optional` | `` | default = k_eShowcaseType_Invalid |
| 2 | `audit_action` | `.EShowcaseAuditAction` | `optional` | `` | default = k_eShowcaseAuditAction_Invalid |
| 3 | `audit_data` | `uint64` | `optional` | `` |  |
| 4 | `timestamp` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgShowcaseReport</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `reporter_account_id` | `uint32` | `optional` | `` |  |
| 2 | `showcase_type` | `.EShowcaseType` | `optional` | `` | default = k_eShowcaseType_Invalid |
| 3 | `report_timestamp` | `uint32` | `optional` | `` |  |
| 4 | `report_comment` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgShowcaseAdminUserDetails</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `locked_until_timestamp` | `uint32` | `optional` | `` |  |
| 2 | `audit_entries` | `.CMsgShowcaseAuditEntry` | `repeated` | `` |  |
| 3 | `reports` | `.CMsgShowcaseReport` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseAdminGetUserDetails</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseAdminGetUserDetailsResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCShowcaseAdminGetUserDetailsResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `user_details` | `.CMsgShowcaseAdminUserDetails` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseAdminReset</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_account_id` | `uint32` | `optional` | `` |  |
| 2 | `showcase_type` | `.EShowcaseType` | `optional` | `` | default = k_eShowcaseType_Invalid |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseAdminResetResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCShowcaseAdminResetResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseAdminLockAccount</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_account_id` | `uint32` | `optional` | `` |  |
| 2 | `locked_until_timestamp` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseAdminLockAccountResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCShowcaseAdminLockAccountResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseAdminConvict</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_account_id` | `uint32` | `optional` | `` |  |
| 2 | `showcase_type` | `.EShowcaseType` | `optional` | `` | default = k_eShowcaseType_Invalid |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseAdminConvictResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCShowcaseAdminConvictResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseAdminExonerate</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_account_id` | `uint32` | `optional` | `` |  |
| 2 | `showcase_type` | `.EShowcaseType` | `optional` | `` | default = k_eShowcaseType_Invalid |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseAdminExonerateResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCShowcaseAdminExonerateResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgShowcaseModerationInfo</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `showcase_type` | `.EShowcaseType` | `optional` | `` | default = k_eShowcaseType_Invalid |
| 3 | `showcase_timestamp` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseModerationGetQueue</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `start_timestamp` | `uint32` | `optional` | `` |  |
| 2 | `result_count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseModerationGetQueueResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCShowcaseModerationGetQueueResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `showcases` | `.CMsgShowcaseModerationInfo` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseModerationApplyModeration</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `showcase_type` | `.EShowcaseType` | `optional` | `` | default = k_eShowcaseType_Invalid |
| 3 | `showcase_timestamp` | `uint32` | `optional` | `` |  |
| 4 | `approve` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseModerationApplyModerationResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCShowcaseModerationApplyModerationResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>EShowcaseHeroPlusFlag</code> — values: 6</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eShowcaseHeroPlusFlag_None` | 0 |
| `k_eShowcaseHeroPlusFlag_BadgePosTop` | 1 |
| `k_eShowcaseHeroPlusFlag_BadgePosBottom` | 2 |
| `k_eShowcaseHeroPlusFlag_BadgePosLeft` | 4 |
| `k_eShowcaseHeroPlusFlag_BadgePosRight` | 8 |
| `k_eShowcaseHeroPlusFlag_ShowRelics` | 16 |

</details>

<details>
<summary><code>EShowcaseType</code> — values: 5</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eShowcaseType_Invalid` | 0 |
| `k_eShowcaseType_Profile` | 1 |
| `k_eShowcaseType_MiniProfile` | 2 |
| `k_eShowcaseType_DefaultProfile` | 3 |
| `k_eShowcaseType_DefaultMiniProfile` | 4 |

</details>

<details>
<summary><code>EShowcaseItemState</code> — values: 6</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eShowcaseItemState_Ok` | 0 |
| `k_eShowcaseItemState_MinorModifications` | 1 |
| `k_eShowcaseItemState_ValidityUnknown` | 2 |
| `k_eShowcaseItemState_PartiallyInvalid` | 3 |
| `k_eShowcaseItemState_Invalid` | 4 |
| `k_eShowcaseItemState_Failure` | 5 |

</details>

<details>
<summary><code>EShowcaseAuditAction</code> — values: 8</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eShowcaseAuditAction_Invalid` | 0 |
| `k_eShowcaseAuditAction_ShowcaseChanged` | 1 |
| `k_eShowcaseAuditAction_AdminShowcaseReset` | 2 |
| `k_eShowcaseAuditAction_AdminShowcaseAccountLocked` | 3 |
| `k_eShowcaseAuditAction_AdminShowcaseExonerated` | 4 |
| `k_eShowcaseAuditAction_AdminShowcaseConvicted` | 5 |
| `k_eShowcaseAuditAction_AdminModerationApproved` | 6 |
| `k_eShowcaseAuditAction_AdminModerationRejected` | 7 |

</details>

<details>
<summary><code>EShowcaseItemFlag</code> — values: 2</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eShowcaseItemFlag_None` | 0 |
| `k_eShowcaseItemFlag_FlipHorizontally` | 1 |

</details>

<details>
<summary><code>EShowcaseItemFlag_Hero</code> — values: 6</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eShowcaseItemFlag_Hero_None` | 0 |
| `k_eShowcaseItemFlag_Hero_ShowPedestal` | 1 |
| `k_eShowcaseItemFlag_Hero_UseCurrentLoadout` | 2 |
| `k_eShowcaseItemFlag_Hero_ShowHeroCard` | 4 |
| `k_eShowcaseItemFlag_Hero_HeroCardHideName` | 8 |
| `k_eShowcaseItemFlag_Hero_HeroCardUseMovie` | 16 |

</details>

<details>
<summary><code>CMsgShowcaseItem_PlayerMatch.EPlayerOutcome</code> — values: 4</summary>

- Parent: `CMsgShowcaseItem_PlayerMatch`

| Name | Number |
|---|---:|
| `k_eInvalid` | 0 |
| `k_eWin` | 1 |
| `k_eLoss` | 2 |
| `k_eNotScored` | 3 |

</details>

<details>
<summary><code>CMsgShowcase.EModerationState</code> — values: 2</summary>

- Parent: `CMsgShowcase`

| Name | Number |
|---|---:|
| `k_eModerationState_Ok` | 0 |
| `k_eModerationState_PendingApproval` | 1 |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseGetUserDataResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCShowcaseGetUserDataResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eUnknownShowcase` | 5 |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseSetUserDataResponse.EResponse</code> — values: 9</summary>

- Parent: `CMsgClientToGCShowcaseSetUserDataResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalid` | 5 |
| `k_eLockedFromEditing` | 6 |
| `k_eBudgetExceeded` | 7 |
| `k_eCommunicationScoreTooLow` | 8 |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseSubmitReportResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCShowcaseSubmitReportResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eAlreadyReported` | 5 |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseAdminGetReportsRollupListResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCShowcaseAdminGetReportsRollupListResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNoPermission` | 5 |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseAdminGetReportsRollupResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCShowcaseAdminGetReportsRollupResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNoPermission` | 5 |
| `k_eNotFound` | 6 |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseAdminGetUserDetailsResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCShowcaseAdminGetUserDetailsResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNoPermission` | 5 |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseAdminResetResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCShowcaseAdminResetResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNoPermission` | 5 |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseAdminLockAccountResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCShowcaseAdminLockAccountResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNoPermission` | 5 |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseAdminConvictResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCShowcaseAdminConvictResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNoPermission` | 5 |
| `k_eAlreadyConvicted` | 6 |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseAdminExonerateResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCShowcaseAdminExonerateResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNoPermission` | 5 |
| `k_eAlreadyExonerated` | 6 |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseModerationGetQueueResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCShowcaseModerationGetQueueResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNoPermission` | 5 |

</details>

<details>
<summary><code>CMsgClientToGCShowcaseModerationApplyModerationResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCShowcaseModerationApplyModerationResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNoPermission` | 5 |
| `k_eGone` | 6 |

</details>
