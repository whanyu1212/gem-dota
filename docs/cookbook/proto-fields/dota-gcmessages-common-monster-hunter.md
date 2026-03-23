# dota_gcmessages_common_monster_hunter.proto

- Module: `dota_gcmessages_common_monster_hunter_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **4**
- Messages: **36** (top-level: 33)
- Enums: **16** (top-level: 2)

## Imports

- `steammessages.proto`
- `dota_shared_enums.proto`
- `dota_gcmessages_common.proto`
- `gcsdk_gcmessages.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgMonsterHunterMaterialCount</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `material_id` | `uint32` | `optional` | `` |  |
| 2 | `material_count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgMonsterHunterHeroCodexEntry</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `stats` | `uint32` | `repeated` | `` |  |
| 2 | `unlocked` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgMonsterHunterUserData</code> — fields: 3; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `material_inventory` | `.CMsgMonsterHunterMaterialQuantity` | `optional` | `` |  |
| 2 | `hero_codex` | `.CMsgMonsterHunterUserData.HeroCodexEntry` | `repeated` | `` |  |
| 3 | `unlocked_count` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgMonsterHunterUserData.HeroCodexEntry</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgMonsterHunterUserData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `key` | `int32` | `optional` | `` |  |
| 2 | `value` | `.CMsgMonsterHunterHeroCodexEntry` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgMonsterHunterMatchRewards</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `players` | `.CMsgMonsterHunterMatchRewards.Player` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgMonsterHunterMatchRewards.Player</code> — fields: 6; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: `CMsgMonsterHunterMatchRewards`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_slot` | `uint32` | `optional` | `` |  |
| 2 | `possible_match_reward_materials` | `.CMsgMonsterHunterMaterialQuantity` | `optional` | `` |  |
| 3 | `actual_match_reward_materials` | `.CMsgMonsterHunterMaterialQuantity` | `optional` | `` |  |
| 4 | `hunt_reward` | `.CMsgMonsterHunterMatchRewards.Player.HuntReward` | `optional` | `` |  |
| 5 | `denial_rewards` | `.CMsgMonsterHunterMatchRewards.Player.HuntReward` | `repeated` | `` |  |
| 6 | `hunter_duel` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgMonsterHunterMatchRewards.Player.HuntReward</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgMonsterHunterMatchRewards.Player`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `materials` | `.CMsgMonsterHunterMaterialQuantity` | `optional` | `` |  |
| 3 | `success` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterGetUserData</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterGetUserDataResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCMonsterHunterGetUserDataResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `user_data` | `.CMsgMonsterHunterUserData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientMonsterHunterUserDataUpdated</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `user_data` | `.CMsgMonsterHunterUserData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterClaimReward</code> — fields: 2; oneofs: 1; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: `RewardType`

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_id` | `uint32` | `oneof` | `RewardType` |  |
| 2 | `hunter_rank_reward` | `uint32` | `oneof` | `RewardType` |  |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterClaimRewardResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCMonsterHunterClaimRewardResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `claim_response` | `.CMsgDOTAClaimEventActionResponse` | `optional` | `` |  |
| 3 | `materials_received` | `.CMsgMonsterHunterMaterialQuantity` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgMonsterHunterItemSet</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `econ_item_id` | `uint32` | `optional` | `` |  |
| 2 | `set_index` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterClaimSetReward</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_sets` | `.CMsgMonsterHunterItemSet` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterClaimSetRewardResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCMonsterHunterClaimSetRewardResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `claim_responses` | `.CMsgDOTAClaimEventActionResponse` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterTradeMaterials</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `material_offer` | `.CMsgMonsterHunterMaterialQuantity` | `optional` | `` |  |
| 2 | `material_request` | `.CMsgMonsterHunterMaterialQuantity` | `optional` | `` |  |
| 3 | `recipe_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterTradeMaterialsResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCMonsterHunterTradeMaterialsResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `materials_received` | `.CMsgMonsterHunterMaterialQuantity` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterGiftMaterials</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `token_gift` | `.CMsgMonsterHunterMaterialCount` | `optional` | `` |  |
| 2 | `recipient_account_id` | `uint32` | `optional` | `` |  |
| 3 | `periodic_resource_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterGiftMaterialsResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCMonsterHunterGiftMaterialsResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterRequestMaterialsNeededByFriend</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `friend_account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterRequestMaterialsNeededByFriendResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCMonsterHunterRequestMaterialsNeededByFriendResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `token_quantity` | `.CMsgMonsterHunterMaterialQuantity` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterDevResetAll</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `reset_codex_only` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterDevResetAllResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCMonsterHunterDevResetAllResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterDevGrantMaterials</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `material_quantity` | `.CMsgMonsterHunterMaterialQuantity` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterDevGrantMaterialsResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCMonsterHunterDevGrantMaterialsResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterDevClearInventory</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterDevClearInventoryResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCMonsterHunterDevClearInventoryResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterDevClaimInvestigationRewards</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `investigation_game_state` | `.CMsgMonsterHunterInvestigationGameState` | `optional` | `` |  |
| 2 | `win` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterDevClaimInvestigationRewardsResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCMonsterHunterDevClaimInvestigationRewardsResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterClaimCodexReward</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `codex_id` | `uint32` | `optional` | `` |  |
| 2 | `reward` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterClaimCodexRewardResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCMonsterHunterClaimCodexRewardResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `claim_response` | `.CMsgDOTAClaimEventActionResponse` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDevModifyCodexAction</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `codex_id` | `uint32` | `optional` | `` |  |
| 2 | `stat_type` | `.EHeroCodexEntryStatType` | `optional` | `` | default = k_eHeroCodexEntryStatType_Killed |
| 3 | `action` | `.CMsgDevModifyCodexAction.EAction` | `optional` | `` | default = k_eClear |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterDevModifyHeroCodex</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `actions` | `.CMsgDevModifyCodexAction` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterDevModifyHeroCodexResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCMonsterHunterDevModifyHeroCodexResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterFeedback</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `language` | `uint32` | `optional` | `` |  |
| 2 | `feedback` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterFeedbackResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCMonsterHunterFeedbackResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>EMonsterHunterAuditAction</code> — values: 16</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eMonsterHunterAuditAction_Invalid` | 0 |
| `k_eMonsterHunterAuditAction_DevModifyMaterials` | 1 |
| `k_eMonsterHunterAuditAction_DevGrantMaterials` | 2 |
| `k_eMonsterHunterAuditAction_DevResetAll` | 3 |
| `k_eMonsterHunterAuditAction_ClaimReward` | 4 |
| `k_eMonsterHunterAuditAction_MatchRewardsWin` | 5 |
| `k_eMonsterHunterAuditAction_MatchRewardsLose` | 6 |
| `k_eMonsterHunterAuditAction_MaterialTraderLost` | 7 |
| `k_eMonsterHunterAuditAction_MaterialTraderGained` | 8 |
| `k_eMonsterHunterAuditAction_RewardMaterialCost` | 9 |
| `k_eMonsterHunterAuditAction_SupportGrantMaterials` | 10 |
| `k_eMonsterHunterAuditAction_MaterialGiftSent` | 11 |
| `k_eMonsterHunterAuditAction_DevClaimInvestigationRewards` | 12 |
| `k_eMonsterHunterAuditAction_HeroCodexUpdate` | 13 |
| `k_eMonsterHunterAuditAction_EventActionReward` | 14 |
| `k_eMonsterHunterAuditAction_AutoCraft` | 15 |

</details>

<details>
<summary><code>EHeroCodexEntryStatType</code> — values: 10</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eHeroCodexEntryStatType_Killed` | 0 |
| `k_eHeroCodexEntryStatType_WinsPlayingAsHero` | 1 |
| `k_eHeroCodexEntryStatType_WinsWith` | 2 |
| `k_eHeroCodexEntryStatType_LossesPlayingAsHero` | 3 |
| `k_eHeroCodexEntryStatType_LossesWith` | 4 |
| `k_eHeroCodexEntryStatType_TurboWinsPlayingAsHero` | 5 |
| `k_eHeroCodexEntryStatType_TurboWinsWith` | 6 |
| `k_eHeroCodexEntryStatType_TurboLossesPlayingAsHero` | 7 |
| `k_eHeroCodexEntryStatType_TurboLossesWith` | 8 |
| `k_eHeroCodexEntryStatType_Count` | 9 |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterGetUserDataResponse.EResponse</code> — values: 5</summary>

- Parent: `CMsgClientToGCMonsterHunterGetUserDataResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterClaimRewardResponse.EResponse</code> — values: 10</summary>

- Parent: `CMsgClientToGCMonsterHunterClaimRewardResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eRewardAlreadyClaimed` | 5 |
| `k_eNotEnoughMaterialsForReward` | 6 |
| `k_eNotEnoughResourceForReward` | 7 |
| `k_eRequiredHunterLevel` | 8 |
| `k_eDontHavePremium` | 9 |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterClaimSetRewardResponse.EResponse</code> — values: 8</summary>

- Parent: `CMsgClientToGCMonsterHunterClaimSetRewardResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eRewardAlreadyClaimed` | 5 |
| `k_eNotEnoughMaterialsForReward` | 6 |
| `k_eDontHavePremium` | 7 |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterTradeMaterialsResponse.EResponse</code> — values: 10</summary>

- Parent: `CMsgClientToGCMonsterHunterTradeMaterialsResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNotAllowed` | 5 |
| `k_eInvalidOffer` | 6 |
| `k_eNotEnoughMaterials` | 7 |
| `k_eRewardDoesNotMatchRecipe` | 8 |
| `k_eAlreadyClaimedMax` | 9 |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterGiftMaterialsResponse.EResponse</code> — values: 10</summary>

- Parent: `CMsgClientToGCMonsterHunterGiftMaterialsResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNotAllowed` | 5 |
| `k_eInvalidGift` | 6 |
| `k_eNotEnoughMaterials` | 7 |
| `k_eInvalidRecipient` | 8 |
| `k_eNotEnoughPeriodicResource` | 9 |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterRequestMaterialsNeededByFriendResponse.EResponse</code> — values: 8</summary>

- Parent: `CMsgClientToGCMonsterHunterRequestMaterialsNeededByFriendResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNotAllowed` | 5 |
| `k_eInvalidFriend` | 6 |
| `k_eTooManyRequests` | 7 |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterDevResetAllResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCMonsterHunterDevResetAllResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNotAllowed` | 5 |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterDevGrantMaterialsResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCMonsterHunterDevGrantMaterialsResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNotAllowed` | 5 |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterDevClearInventoryResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCMonsterHunterDevClearInventoryResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNotAllowed` | 5 |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterDevClaimInvestigationRewardsResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCMonsterHunterDevClaimInvestigationRewardsResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNotAllowed` | 5 |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterClaimCodexRewardResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCMonsterHunterClaimCodexRewardResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNotAllowed` | 5 |
| `k_eAlreadyClaimed` | 6 |

</details>

<details>
<summary><code>CMsgDevModifyCodexAction.EAction</code> — values: 2</summary>

- Parent: `CMsgDevModifyCodexAction`

| Name | Number |
|---|---:|
| `k_eClear` | 0 |
| `k_eAdd` | 1 |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterDevModifyHeroCodexResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCMonsterHunterDevModifyHeroCodexResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNotAllowed` | 5 |

</details>

<details>
<summary><code>CMsgClientToGCMonsterHunterFeedbackResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCMonsterHunterFeedbackResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNotAllowed` | 5 |

</details>
