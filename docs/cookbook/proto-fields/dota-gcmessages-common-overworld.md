# dota_gcmessages_common_overworld.proto

- Module: `dota_gcmessages_common_overworld_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **5**
- Messages: **51** (top-level: 46)
- Enums: **19** (top-level: 4)

## Imports

- `steammessages.proto`
- `dota_shared_enums.proto`
- `dota_gcmessages_common.proto`
- `dota_gcmessages_common_survivors.proto`
- `gcsdk_gcmessages.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgOverworldTokenCount</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `token_id` | `uint32` | `optional` | `` |  |
| 2 | `token_count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgOverworldTokenQuantity</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `token_counts` | `.CMsgOverworldTokenCount` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgOverworldEncounterTokenTreasureData</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `reward_options` | `.CMsgOverworldEncounterTokenTreasureData.RewardOption` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgOverworldEncounterTokenTreasureData.RewardOption</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgOverworldEncounterTokenTreasureData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `reward_data` | `uint32` | `optional` | `` |  |
| 2 | `token_cost` | `.CMsgOverworldTokenQuantity` | `optional` | `` |  |
| 3 | `token_reward` | `.CMsgOverworldTokenQuantity` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgOverworldEncounterTokenQuestData</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `quests` | `.CMsgOverworldEncounterTokenQuestData.Quest` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgOverworldEncounterTokenQuestData.Quest</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgOverworldEncounterTokenQuestData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `reward_data` | `uint32` | `optional` | `` |  |
| 2 | `token_cost` | `.CMsgOverworldTokenQuantity` | `optional` | `` |  |
| 3 | `token_reward` | `.CMsgOverworldTokenQuantity` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgOverworldHeroList</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_ids` | `int32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgOverworldEncounterChooseHeroData</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_list` | `.CMsgOverworldHeroList` | `optional` | `` |  |
| 2 | `additive` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgOverworldEncounterProgressData</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `choice` | `int32` | `optional` | `` |  |
| 2 | `progress` | `int32` | `optional` | `` |  |
| 3 | `max_progress` | `int32` | `optional` | `` |  |
| 4 | `visited` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgOverworldEncounterData</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `extra_encounter_data` | `.CExtraMsgBlock` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgOverworldNode</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `node_id` | `uint32` | `optional` | `` |  |
| 2 | `node_state` | `.EOverworldNodeState` | `optional` | `` | default = k_eOverworldNodeState_Invalid |
| 3 | `node_encounter_data` | `.CMsgOverworldEncounterData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgOverworldPath</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `path_id` | `uint32` | `optional` | `` |  |
| 2 | `path_cost` | `.CMsgOverworldTokenQuantity` | `optional` | `` |  |
| 3 | `path_state` | `.EOverworldPathState` | `optional` | `` | default = k_eOverworldPathState_Invalid |

</details>

<details>
<summary><code>CMsgOverworldMinigameCustomData</code> — fields: 1; oneofs: 1; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: `minigame_type`

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `survivors_data` | `.CMsgSurvivorsUserData` | `oneof` | `minigame_type` |  |

</details>

<details>
<summary><code>CMsgOverworldMinigameUserData</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `node_id` | `uint32` | `optional` | `` |  |
| 2 | `currency_amount` | `uint32` | `optional` | `` |  |
| 3 | `custom_data` | `.CMsgOverworldMinigameCustomData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgOverworldUserData</code> — fields: 5; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `token_inventory` | `.CMsgOverworldTokenQuantity` | `optional` | `` |  |
| 2 | `overworld_nodes` | `.CMsgOverworldNode` | `repeated` | `` |  |
| 3 | `overworld_paths` | `.CMsgOverworldPath` | `repeated` | `` |  |
| 4 | `current_node_id` | `uint32` | `optional` | `` |  |
| 5 | `minigame_data` | `.CMsgOverworldUserData.MinigameDataEntry` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgOverworldUserData.MinigameDataEntry</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgOverworldUserData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `key` | `uint32` | `optional` | `` |  |
| 2 | `value` | `.CMsgOverworldMinigameUserData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgOverworldMatchRewards</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `players` | `.CMsgOverworldMatchRewards.Player` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgOverworldMatchRewards.Player</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgOverworldMatchRewards`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_slot` | `uint32` | `optional` | `` |  |
| 2 | `tokens` | `.CMsgOverworldTokenQuantity` | `optional` | `` |  |
| 3 | `overworld_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCOverworldGetUserData</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `overworld_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCOverworldGetUserDataResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCOverworldGetUserDataResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `user_data` | `.CMsgOverworldUserData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientOverworldUserDataUpdated</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `overworld_id` | `uint32` | `optional` | `` |  |
| 2 | `user_data` | `.CMsgOverworldUserData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCOverworldCompletePath</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `overworld_id` | `uint32` | `optional` | `` |  |
| 2 | `path_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCOverworldCompletePathResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCOverworldCompletePathResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `claim_response` | `.CMsgDOTAClaimEventActionResponse` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgOverworldEncounterPitFighterRewardData</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `token_id` | `uint32` | `optional` | `` |  |
| 2 | `choice` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCOverworldClaimEncounterReward</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `overworld_id` | `uint32` | `optional` | `` |  |
| 2 | `node_id` | `uint32` | `optional` | `` |  |
| 3 | `reward_data` | `uint32` | `optional` | `` |  |
| 4 | `periodic_resource_id` | `uint32` | `optional` | `` |  |
| 5 | `extra_reward_data` | `.CMsgOverworldEncounterData` | `optional` | `` |  |
| 6 | `leaderboard_data` | `uint32` | `optional` | `` |  |
| 7 | `leaderboard_index` | `uint32` | `optional` | `` |  |
| 8 | `should_claim_reward` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCOverworldClaimEncounterRewardResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `claim_response` | `.CMsgDOTAClaimEventActionResponse` | `optional` | `` |  |
| 3 | `tokens_received` | `.CMsgOverworldTokenQuantity` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCOverworldVisitEncounter</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `overworld_id` | `uint32` | `optional` | `` |  |
| 2 | `node_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCOverworldVisitEncounterResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCOverworldVisitEncounterResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCOverworldMoveToNode</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `overworld_id` | `uint32` | `optional` | `` |  |
| 2 | `node_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCOverworldMoveToNodeResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCOverworldMoveToNodeResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCOverworldTradeTokens</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `overworld_id` | `uint32` | `optional` | `` |  |
| 2 | `token_offer` | `.CMsgOverworldTokenQuantity` | `optional` | `` |  |
| 3 | `token_request` | `.CMsgOverworldTokenQuantity` | `optional` | `` |  |
| 4 | `recipe` | `uint32` | `optional` | `` |  |
| 5 | `encounter_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCOverworldTradeTokensResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCOverworldTradeTokensResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `tokens_received` | `.CMsgOverworldTokenQuantity` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCOverworldGiftTokens</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `overworld_id` | `uint32` | `optional` | `` |  |
| 2 | `token_gift` | `.CMsgOverworldTokenCount` | `optional` | `` |  |
| 3 | `recipient_account_id` | `uint32` | `optional` | `` |  |
| 4 | `periodic_resource_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCOverworldGiftTokensResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCOverworldGiftTokensResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCOverworldRequestTokensNeededByFriend</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `friend_account_id` | `uint32` | `optional` | `` |  |
| 2 | `overworld_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCOverworldRequestTokensNeededByFriendResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `token_quantity` | `.CMsgOverworldTokenQuantity` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCOverworldDevResetAll</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `overworld_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCOverworldDevResetAllResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCOverworldDevResetAllResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCOverworldDevResetNode</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `overworld_id` | `uint32` | `optional` | `` |  |
| 2 | `node_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCOverworldDevResetNodeResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCOverworldDevResetNodeResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCOverworldDevGrantTokens</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `overworld_id` | `uint32` | `optional` | `` |  |
| 2 | `token_quantity` | `.CMsgOverworldTokenQuantity` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCOverworldDevGrantTokensResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCOverworldDevGrantTokensResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCOverworldDevClearInventory</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `overworld_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCOverworldDevClearInventoryResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCOverworldDevClearInventoryResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCOverworldFeedback</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `language` | `uint32` | `optional` | `` |  |
| 2 | `overworld_id` | `uint32` | `optional` | `` |  |
| 3 | `feedback` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCOverworldFeedbackResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCOverworldFeedbackResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCOverworldGetDynamicImage</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `magic` | `uint32` | `optional` | `` |  |
| 2 | `image_id` | `uint32` | `optional` | `` |  |
| 3 | `language` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCOverworldGetDynamicImageResponse</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `image_id` | `uint32` | `optional` | `` |  |
| 2 | `images` | `.CMsgClientToGCOverworldGetDynamicImageResponse.Image` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCOverworldGetDynamicImageResponse.Image</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCOverworldGetDynamicImageResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `width` | `uint32` | `optional` | `` |  |
| 2 | `height` | `uint32` | `optional` | `` |  |
| 3 | `format` | `.CMsgClientToGCOverworldGetDynamicImageResponse.EDynamicImageFormat` | `optional` | `` | default = k_eUnknown |
| 4 | `image_bytes` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCOverworldMinigameAction</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `overworld_id` | `uint32` | `optional` | `` |  |
| 2 | `node_id` | `uint32` | `optional` | `` |  |
| 3 | `action` | `.EOverworldMinigameAction` | `optional` | `` | default = k_eOverworldMinigameAction_Invalid |
| 4 | `selection` | `uint32` | `optional` | `` |  |
| 5 | `option_value` | `uint32` | `optional` | `` |  |
| 6 | `currency_amount` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCOverworldMinigameActionResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCOverworldMinigameActionResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>EOverworldNodeState</code> — values: 3</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eOverworldNodeState_Invalid` | 0 |
| `k_eOverworldNodeState_Locked` | 1 |
| `k_eOverworldNodeState_Unlocked` | 2 |

</details>

<details>
<summary><code>EOverworldPathState</code> — values: 3</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eOverworldPathState_Invalid` | 0 |
| `k_eOverworldPathState_Incomplete` | 1 |
| `k_eOverworldPathState_Complete` | 2 |

</details>

<details>
<summary><code>EOverworldAuditAction</code> — values: 17</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eOverworldAuditAction_Invalid` | 0 |
| `k_eOverworldAuditAction_DevModifyTokens` | 1 |
| `k_eOverworldAuditAction_DevClearInventory` | 2 |
| `k_eOverworldAuditAction_DevGrantTokens` | 3 |
| `k_eOverworldAuditAction_CompletePath` | 4 |
| `k_eOverworldAuditAction_ClaimEncounterReward` | 5 |
| `k_eOverworldAuditAction_DevResetNode` | 6 |
| `k_eOverworldAuditAction_DevResetPath` | 7 |
| `k_eOverworldAuditAction_MatchRewardsFull` | 8 |
| `k_eOverworldAuditAction_MatchRewardsHalf` | 9 |
| `k_eOverworldAuditAction_EventActionTokenGrant` | 10 |
| `k_eOverworldAuditAction_TokenTraderLost` | 11 |
| `k_eOverworldAuditAction_TokenTraderGained` | 12 |
| `k_eOverworldAuditAction_EncounterRewardTokenCost` | 13 |
| `k_eOverworldAuditAction_EncounterRewardTokenReward` | 14 |
| `k_eOverworldAuditAction_SupportGrantTokens` | 16 |
| `k_eOverworldAuditAction_TokenGiftSent` | 17 |

</details>

<details>
<summary><code>EOverworldMinigameAction</code> — values: 7</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eOverworldMinigameAction_Invalid` | 0 |
| `k_eOverworldMinigameAction_DevReset` | 1 |
| `k_eOverworldMinigameAction_DevGiveCurrency` | 2 |
| `k_eOverworldMinigameAction_Purchase` | 3 |
| `k_eOverworldMinigameAction_SetOption` | 4 |
| `k_eOverworldMinigameAction_ReportCurrencyGained` | 5 |
| `k_eOverworldMinigameAction_UnlockDifficulty` | 6 |

</details>

<details>
<summary><code>CMsgClientToGCOverworldGetUserDataResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCOverworldGetUserDataResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidOverworld` | 5 |

</details>

<details>
<summary><code>CMsgClientToGCOverworldCompletePathResponse.EResponse</code> — values: 11</summary>

- Parent: `CMsgClientToGCOverworldCompletePathResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidOverworld` | 5 |
| `k_eInvalidPath` | 6 |
| `k_eNotEnoughTokens` | 7 |
| `k_ePathIsLocked` | 8 |
| `k_ePathAlreadyUnlocked` | 9 |
| `k_eEventExpired` | 10 |

</details>

<details>
<summary><code>CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse</code> — values: 17</summary>

- Parent: `CMsgClientToGCOverworldClaimEncounterRewardResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidOverworld` | 5 |
| `k_eInvalidNode` | 6 |
| `k_eNodeLocked` | 7 |
| `k_eRewardAlreadyClaimed` | 8 |
| `k_eNodeNotEncounter` | 9 |
| `k_eEncounterMissingRewards` | 10 |
| `k_eInvalidEncounterRewardStyle` | 11 |
| `k_eInvalidEncounterData` | 12 |
| `k_eNotEnoughTokensForReward` | 13 |
| `k_eNotEnoughResourceForReward` | 14 |
| `k_eInvalidRewardData` | 15 |
| `k_eEventExpired` | 16 |

</details>

<details>
<summary><code>CMsgClientToGCOverworldVisitEncounterResponse.EResponse</code> — values: 10</summary>

- Parent: `CMsgClientToGCOverworldVisitEncounterResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidOverworld` | 5 |
| `k_eInvalidNode` | 6 |
| `k_eNodeLocked` | 7 |
| `k_eNodeNotEncounter` | 8 |
| `k_eAlreadyVisited` | 9 |

</details>

<details>
<summary><code>CMsgClientToGCOverworldMoveToNodeResponse.EResponse</code> — values: 8</summary>

- Parent: `CMsgClientToGCOverworldMoveToNodeResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidOverworld` | 5 |
| `k_eInvalidNode` | 6 |
| `k_eNodeLocked` | 7 |

</details>

<details>
<summary><code>CMsgClientToGCOverworldTradeTokensResponse.EResponse</code> — values: 13</summary>

- Parent: `CMsgClientToGCOverworldTradeTokensResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNotAllowed` | 5 |
| `k_eNodeLocked` | 6 |
| `k_eInvalidOverworld` | 7 |
| `k_eInvalidOffer` | 8 |
| `k_eNotEnoughTokens` | 9 |
| `k_eInvalidNode` | 10 |
| `k_eInvalidEncounter` | 11 |
| `k_eRewardDoesNotMatchRecipe` | 12 |

</details>

<details>
<summary><code>CMsgClientToGCOverworldGiftTokensResponse.EResponse</code> — values: 12</summary>

- Parent: `CMsgClientToGCOverworldGiftTokensResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNotAllowed` | 5 |
| `k_eNodeLocked` | 6 |
| `k_eInvalidOverworld` | 7 |
| `k_eInvalidGift` | 8 |
| `k_eNotEnoughTokens` | 9 |
| `k_eInvalidRecipient` | 10 |
| `k_eNotEnoughPeriodicResource` | 11 |

</details>

<details>
<summary><code>CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse</code> — values: 10</summary>

- Parent: `CMsgClientToGCOverworldRequestTokensNeededByFriendResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNotAllowed` | 5 |
| `k_eNodeLocked` | 6 |
| `k_eInvalidOverworld` | 7 |
| `k_eInvalidFriend` | 8 |
| `k_eTooManyRequests` | 9 |

</details>

<details>
<summary><code>CMsgClientToGCOverworldDevResetAllResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCOverworldDevResetAllResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNotAllowed` | 5 |
| `k_eInvalidOverworld` | 6 |

</details>

<details>
<summary><code>CMsgClientToGCOverworldDevResetNodeResponse.EResponse</code> — values: 8</summary>

- Parent: `CMsgClientToGCOverworldDevResetNodeResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNotAllowed` | 5 |
| `k_eInvalidOverworld` | 6 |
| `k_eInvalidNode` | 7 |

</details>

<details>
<summary><code>CMsgClientToGCOverworldDevGrantTokensResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCOverworldDevGrantTokensResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNotAllowed` | 5 |
| `k_eInvalidOverworld` | 6 |

</details>

<details>
<summary><code>CMsgClientToGCOverworldDevClearInventoryResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCOverworldDevClearInventoryResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNotAllowed` | 5 |
| `k_eInvalidOverworld` | 6 |

</details>

<details>
<summary><code>CMsgClientToGCOverworldFeedbackResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCOverworldFeedbackResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNotAllowed` | 5 |
| `k_eInvalidOverworld` | 6 |

</details>

<details>
<summary><code>CMsgClientToGCOverworldGetDynamicImageResponse.EDynamicImageFormat</code> — values: 3</summary>

- Parent: `CMsgClientToGCOverworldGetDynamicImageResponse`

| Name | Number |
|---|---:|
| `k_eUnknown` | 0 |
| `k_ePNG` | 1 |
| `k_eData` | 2 |

</details>

<details>
<summary><code>CMsgClientToGCOverworldMinigameActionResponse.EResponse</code> — values: 12</summary>

- Parent: `CMsgClientToGCOverworldMinigameActionResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidOverworld` | 5 |
| `k_eInvalidNode` | 6 |
| `k_eNodeLocked` | 7 |
| `k_eInvalidSelection` | 8 |
| `k_eNotEnoughTokens` | 9 |
| `k_eNotEnoughMinigameCurrency` | 10 |
| `k_eNotAllowed` | 11 |

</details>
