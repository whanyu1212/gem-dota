# dota_gcmessages_client_candy_shop.proto

- Module: `dota_gcmessages_client_candy_shop_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **9**
- Messages: **34** (top-level: 34)
- Enums: **9** (top-level: 2)

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
<summary><code>CMsgCandyShopCandyCount</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `candy_type` | `uint32` | `optional` | `` |  |
| 2 | `candy_count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgCandyShopCandyQuantity</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `candy_counts` | `.CMsgCandyShopCandyCount` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgCandyShopExchangeRecipe</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `recipe_id` | `uint32` | `optional` | `` |  |
| 2 | `input` | `.CMsgCandyShopCandyQuantity` | `optional` | `` |  |
| 3 | `output` | `.CMsgCandyShopCandyQuantity` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgCandyShopRewardData_Item</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_def` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgCandyShopRewardData_EventAction</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 2 | `action_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgCandyShopRewardData_EventPoints</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 2 | `points` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgCandyShopReward</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `reward_id` | `uint32` | `optional` | `` |  |
| 2 | `reward_option_id` | `uint32` | `optional` | `` |  |
| 3 | `price` | `.CMsgCandyShopCandyQuantity` | `optional` | `` |  |
| 4 | `reward_type` | `.ECandyShopRewardType` | `optional` | `` | default = k_eCandyShopRewardType_None |
| 5 | `item_data` | `.CMsgCandyShopRewardData_Item` | `optional` | `` |  |
| 6 | `event_action_data` | `.CMsgCandyShopRewardData_EventAction` | `optional` | `` |  |
| 7 | `event_points_data` | `.CMsgCandyShopRewardData_EventPoints` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgCandyShopUserData</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `inventory_max` | `uint32` | `optional` | `` |  |
| 2 | `inventory` | `.CMsgCandyShopCandyQuantity` | `optional` | `` |  |
| 3 | `exchange_recipe_max` | `uint32` | `optional` | `` |  |
| 4 | `exchange_reset_timestamp` | `fixed32` | `optional` | `` |  |
| 5 | `exchange_recipes` | `.CMsgCandyShopExchangeRecipe` | `repeated` | `` |  |
| 6 | `active_reward_max` | `uint32` | `optional` | `` |  |
| 7 | `active_rewards` | `.CMsgCandyShopReward` | `repeated` | `` |  |
| 8 | `reroll_charges_max` | `uint32` | `optional` | `` |  |
| 9 | `reroll_charges` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCandyShopGetUserData</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `candy_shop_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCandyShopGetUserDataResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCCandyShopGetUserDataResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `user_data` | `.CMsgCandyShopUserData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientCandyShopUserDataUpdated</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `candy_shop_id` | `uint32` | `optional` | `` |  |
| 2 | `user_data` | `.CMsgCandyShopUserData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCandyShopPurchaseReward</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `candy_shop_id` | `uint32` | `optional` | `` |  |
| 2 | `reward_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCandyShopPurchaseRewardResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCCandyShopPurchaseRewardResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCCandyShopOpenBags</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `candy_shop_id` | `uint32` | `optional` | `` |  |
| 2 | `bag_count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCandyShopOpenBagsResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCCandyShopOpenBagsResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCCandyShopDoExchange</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `candy_shop_id` | `uint32` | `optional` | `` |  |
| 2 | `recipe_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCandyShopDoExchangeResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCCandyShopDoExchangeResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCCandyShopDoVariableExchange</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `candy_shop_id` | `uint32` | `optional` | `` |  |
| 2 | `input` | `.CMsgCandyShopCandyQuantity` | `optional` | `` |  |
| 3 | `output` | `.CMsgCandyShopCandyQuantity` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCandyShopDoVariableExchangeResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCCandyShopDoVariableExchangeResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCCandyShopRerollRewards</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `candy_shop_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCandyShopRerollRewardsResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCCandyShopRerollRewardsResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CCandyShopDev</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCCandyShopDevGrantCandy</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `candy_shop_id` | `uint32` | `optional` | `` |  |
| 2 | `candy_quantity` | `.CMsgCandyShopCandyQuantity` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCandyShopDevGrantCandyResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CCandyShopDev.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCCandyShopDevClearInventory</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `candy_shop_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCandyShopDevClearInventoryResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CCandyShopDev.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCCandyShopDevGrantCandyBags</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `candy_shop_id` | `uint32` | `optional` | `` |  |
| 2 | `quantity` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCandyShopDevGrantCandyBagsResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CCandyShopDev.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCCandyShopDevShuffleExchange</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `candy_shop_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCandyShopDevShuffleExchangeResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CCandyShopDev.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCCandyShopDevGrantRerollCharges</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `candy_shop_id` | `uint32` | `optional` | `` |  |
| 2 | `reroll_charges` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCandyShopDevGrantRerollChargesResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CCandyShopDev.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCCandyShopDevResetShop</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `candy_shop_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCandyShopDevResetShopResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CCandyShopDev.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>ECandyShopAuditAction</code> — values: 12</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_ECandyShopAuditAction_Invalid` | 0 |
| `k_ECandyShopAuditAction_SupportModify` | 1 |
| `k_ECandyShopAuditAction_PurchaseReward` | 2 |
| `k_ECandyShopAuditAction_OpenBags` | 3 |
| `k_ECandyShopAuditAction_RerollRewards` | 4 |
| `k_ECandyShopAuditAction_DoVariableExchange` | 5 |
| `k_ECandyShopAuditAction_DoExchange` | 6 |
| `k_ECandyShopAuditAction_DEPRECATED_EventActionGrantInventorySizeIncrease` | 7 |
| `k_ECandyShopAuditAction_EventActionGrantRerollChargesIncrease` | 8 |
| `k_ECandyShopAuditAction_EventActionGrantUpgrade_InventorySize` | 100 |
| `k_ECandyShopAuditAction_EventActionGrantUpgrade_RewardShelf` | 101 |
| `k_ECandyShopAuditAction_EventActionGrantUpgrade_ExtraExchangeRecipe` | 102 |

</details>

<details>
<summary><code>ECandyShopRewardType</code> — values: 4</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eCandyShopRewardType_None` | 0 |
| `k_eCandyShopRewardType_Item` | 1 |
| `k_eCandyShopRewardType_EventAction` | 2 |
| `k_eCandyShopRewardType_EventPoints` | 3 |

</details>

<details>
<summary><code>CMsgClientToGCCandyShopGetUserDataResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCCandyShopGetUserDataResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidShop` | 5 |
| `k_eExpiredShop` | 6 |

</details>

<details>
<summary><code>CMsgClientToGCCandyShopPurchaseRewardResponse.EResponse</code> — values: 9</summary>

- Parent: `CMsgClientToGCCandyShopPurchaseRewardResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidShop` | 5 |
| `k_eInvalidReward` | 6 |
| `k_eNotEnoughCandy` | 7 |
| `k_eExpiredShop` | 8 |

</details>

<details>
<summary><code>CMsgClientToGCCandyShopOpenBagsResponse.EResponse</code> — values: 10</summary>

- Parent: `CMsgClientToGCCandyShopOpenBagsResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidShop` | 5 |
| `k_eInvalidItem` | 6 |
| `k_eNotEnoughBags` | 7 |
| `k_eNotEnoughSpace` | 8 |
| `k_eExpiredShop` | 9 |

</details>

<details>
<summary><code>CMsgClientToGCCandyShopDoExchangeResponse.EResponse</code> — values: 10</summary>

- Parent: `CMsgClientToGCCandyShopDoExchangeResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidShop` | 5 |
| `k_eNotEnoughCandy` | 6 |
| `k_eInvalidRecipe` | 7 |
| `k_eNotEnoughSpace` | 8 |
| `k_eExpiredShop` | 9 |

</details>

<details>
<summary><code>CMsgClientToGCCandyShopDoVariableExchangeResponse.EResponse</code> — values: 10</summary>

- Parent: `CMsgClientToGCCandyShopDoVariableExchangeResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidShop` | 5 |
| `k_eNotEnoughCandy` | 6 |
| `k_eInvalidRecipe` | 7 |
| `k_eNotEnoughSpace` | 8 |
| `k_eExpiredShop` | 9 |

</details>

<details>
<summary><code>CMsgClientToGCCandyShopRerollRewardsResponse.EResponse</code> — values: 9</summary>

- Parent: `CMsgClientToGCCandyShopRerollRewardsResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidShop` | 5 |
| `k_eNoRerollCharges` | 6 |
| `k_eExpiredShop` | 7 |
| `k_eShopNotOpen` | 8 |

</details>

<details>
<summary><code>CCandyShopDev.EResponse</code> — values: 8</summary>

- Parent: `CCandyShopDev`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNotAllowed` | 5 |
| `k_eInvalidShop` | 6 |
| `k_eNotEnoughSpace` | 7 |

</details>
