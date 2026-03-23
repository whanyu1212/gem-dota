# econ_gcmessages.proto

- Module: `econ_gcmessages_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **4**
- Messages: **143** (top-level: 121)
- Enums: **15** (top-level: 2)

## Imports

- `steammessages.proto`
- `econ_shared_enums.proto`
- `gcsdk_gcmessages.proto`
- `base_gcmessages.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgApplyAutograph</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `autograph_item_id` | `uint64` | `optional` | `` |  |
| 2 | `item_item_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgAdjustItemEquippedState</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_id` | `uint64` | `optional` | `` |  |
| 2 | `new_class` | `uint32` | `optional` | `` |  |
| 3 | `new_slot` | `uint32` | `optional` | `` |  |
| 4 | `style_index` | `uint32` | `optional` | `` | default = 255 |

</details>

<details>
<summary><code>CMsgEconPlayerStrangeCountAdjustment</code> — fields: 3; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `strange_count_adjustments` | `.CMsgEconPlayerStrangeCountAdjustment.CStrangeCountAdjustment` | `repeated` | `` |  |
| 3 | `turbo_mode` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgEconPlayerStrangeCountAdjustment.CStrangeCountAdjustment</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgEconPlayerStrangeCountAdjustment`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_type` | `uint32` | `optional` | `` |  |
| 2 | `item_id` | `uint64` | `optional` | `` |  |
| 3 | `adjustment` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgCraftingResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_ids` | `uint64` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCRequestStoreSalesData</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `version` | `uint32` | `optional` | `` |  |
| 2 | `currency` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCRequestStoreSalesDataResponse</code> — fields: 3; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `sale_price` | `.CMsgGCRequestStoreSalesDataResponse.Price` | `repeated` | `` |  |
| 2 | `version` | `uint32` | `optional` | `` |  |
| 3 | `expiration_time` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCRequestStoreSalesDataResponse.Price</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCRequestStoreSalesDataResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_def` | `uint32` | `optional` | `` |  |
| 2 | `price` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCRequestStoreSalesDataUpToDateResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `version` | `uint32` | `optional` | `` |  |
| 2 | `expiration_time` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCPingRequest</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgGCToGCPingResponse</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgGCToGCGetUserSessionServer</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCGetUserSessionServerResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `server_steam_id` | `fixed64` | `optional` | `` |  |
| 2 | `is_online` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCGetUserServerMembers</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `max_spectators` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCGetUserServerMembersResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `member_account_id` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgLookupMultipleAccountNames</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `accountids` | `uint32` | `repeated` | `` | packed = true |

</details>

<details>
<summary><code>CMsgLookupMultipleAccountNamesResponse</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `accounts` | `.CMsgLookupMultipleAccountNamesResponse.Account` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgLookupMultipleAccountNamesResponse.Account</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgLookupMultipleAccountNamesResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `accountid` | `uint32` | `optional` | `` |  |
| 2 | `persona` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgRequestCrateItems</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `crate_item_def` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgRequestCrateItemsResponse</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `uint32` | `optional` | `` |  |
| 2 | `item_defs` | `uint32` | `repeated` | `` |  |
| 3 | `peek_item_defs` | `uint32` | `repeated` | `` |  |
| 4 | `peek_items` | `.CSOEconItem` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgRequestCrateEscalationLevel</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `crate_item_def` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgRequestCrateEscalationLevelResponse</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `uint32` | `optional` | `` |  |
| 2 | `escalation_level0` | `uint32` | `optional` | `` |  |
| 3 | `escalation_level1` | `uint32` | `optional` | `` |  |
| 4 | `escalation_level2` | `uint32` | `optional` | `` |  |
| 5 | `escalation_level3` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCCanUseDropRateBonus</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `drop_rate_bonus` | `float` | `optional` | `` |  |
| 3 | `booster_type` | `uint32` | `optional` | `` |  |
| 4 | `exclusive_item_def` | `uint32` | `optional` | `` |  |
| 5 | `allow_equal_rate` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSQLAddDropRateBonus</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `item_id` | `uint64` | `optional` | `` |  |
| 3 | `item_def` | `uint32` | `optional` | `` |  |
| 4 | `drop_rate_bonus` | `float` | `optional` | `` |  |
| 5 | `booster_type` | `uint32` | `optional` | `` |  |
| 6 | `seconds_duration` | `uint32` | `optional` | `` |  |
| 7 | `end_time_stamp` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSQLUpgradeBattleBooster</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `item_def` | `uint32` | `optional` | `` |  |
| 3 | `bonus_to_add` | `float` | `optional` | `` |  |
| 4 | `booster_type` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCRefreshSOCache</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `reload` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCAddSubscriptionTime</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `matching_subscription_def_indexes` | `uint32` | `repeated` | `` |  |
| 3 | `additional_seconds` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCGrantAccountRolledItems</code> — fields: 4; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `items` | `.CMsgGCToGCGrantAccountRolledItems.Item` | `repeated` | `` |  |
| 3 | `audit_action` | `uint32` | `optional` | `` |  |
| 4 | `audit_data` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCGrantAccountRolledItems.Item</code> — fields: 8; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: `CMsgGCToGCGrantAccountRolledItems`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_def` | `uint32` | `optional` | `` |  |
| 2 | `loot_lists` | `string` | `repeated` | `` |  |
| 3 | `ignore_limit` | `bool` | `optional` | `` |  |
| 4 | `origin` | `uint32` | `optional` | `` |  |
| 5 | `dynamic_attributes` | `.CMsgGCToGCGrantAccountRolledItems.Item.DynamicAttribute` | `repeated` | `` |  |
| 6 | `additional_audit_entries` | `.CMsgGCToGCGrantAccountRolledItems.Item.AdditionalAuditEntry` | `repeated` | `` |  |
| 7 | `inventory_token` | `uint32` | `optional` | `` |  |
| 8 | `quality` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CMsgGCToGCGrantAccountRolledItems.Item.DynamicAttribute</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToGCGrantAccountRolledItems.Item`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `value_uint32` | `uint32` | `optional` | `` |  |
| 3 | `value_float` | `float` | `optional` | `` |  |
| 4 | `value_string` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCGrantAccountRolledItems.Item.AdditionalAuditEntry</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToGCGrantAccountRolledItems.Item`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `owner_account_id` | `uint32` | `optional` | `` |  |
| 2 | `audit_action` | `uint32` | `optional` | `` |  |
| 3 | `audit_data` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCBetaDeleteItems</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `item_ids` | `uint64` | `repeated` | `` |  |
| 3 | `item_defs` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCGrantSelfMadeItemToAccount</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_def_index` | `uint32` | `optional` | `` |  |
| 2 | `accountid` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCUnlockCrate</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `crate_item_id` | `uint64` | `optional` | `` |  |
| 3 | `key_item_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgUseItem</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_id` | `uint64` | `optional` | `` |  |
| 2 | `target_steam_id` | `fixed64` | `optional` | `` |  |
| 3 | `gift__potential_targets` | `uint32` | `repeated` | `` |  |
| 4 | `duel__class_lock` | `uint32` | `optional` | `` |  |
| 5 | `initiator_steam_id` | `uint64` | `optional` | `` |  |
| 6 | `itempack__ack_immediately` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerUseItem</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `initiator_account_id` | `uint32` | `optional` | `` |  |
| 2 | `use_item_msg` | `.CMsgUseItem` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgUseMultipleItems</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_ids` | `uint64` | `repeated` | `` |  |

</details>

<details>
<summary><code>CGCStoreRechargeRedirect_LineItem</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_def_id` | `uint32` | `optional` | `` |  |
| 2 | `quantity` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCEconSQLWorkItemEmbeddedRollbackData</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `deleted_item_id` | `uint64` | `optional` | `` |  |
| 3 | `old_audit_action` | `uint32` | `optional` | `` |  |
| 4 | `new_audit_action` | `uint32` | `optional` | `` |  |
| 5 | `expected_audit_action` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgCraftStatue</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `heroid` | `uint32` | `optional` | `` |  |
| 2 | `sequencename` | `string` | `optional` | `` |  |
| 3 | `cycle` | `float` | `optional` | `` |  |
| 4 | `description` | `string` | `optional` | `` |  |
| 5 | `pedestal_itemdef` | `uint32` | `optional` | `` |  |
| 6 | `toolid` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgRedeemCode</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `code` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgRedeemCodeResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `uint32` | `optional` | `` |  |
| 2 | `item_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDevNewItemRequest</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 3 | `item_def_name` | `string` | `optional` | `` |  |
| 4 | `loot_list_name` | `string` | `optional` | `` |  |
| 5 | `attr_def_name` | `string` | `repeated` | `` |  |
| 6 | `attr_value` | `string` | `repeated` | `` |  |
| 7 | `item_quality` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDevNewItemRequestResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `success` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDevUnlockAllItemStyles</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDevUnlockAllItemStylesResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `success` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCGetAccountSubscriptionItem</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCGetAccountSubscriptionItemResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `def_index` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCAddGiftItem</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `gifter_account_id` | `uint32` | `optional` | `` |  |
| 2 | `receiver_account_id` | `uint32` | `optional` | `` |  |
| 3 | `wrapped_item` | `.CSOEconItem` | `optional` | `` |  |
| 4 | `gift_message` | `string` | `optional` | `` |  |
| 5 | `is_wallet_cash_trusted` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCWrapAndDeliverGift</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_id` | `uint64` | `optional` | `` |  |
| 2 | `give_to_account_id` | `uint32` | `optional` | `` |  |
| 3 | `gift_message` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSQLGCToGCRevokeUntrustedGift</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 4 | `sent_item_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCWrapAndDeliverGiftResponse</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.EGCMsgResponse` | `optional` | `` | default = k_EGCMsgResponseOK |
| 2 | `gifting_charge_uses` | `uint32` | `optional` | `` |  |
| 3 | `gifting_charge_max` | `int32` | `optional` | `` |  |
| 4 | `gifting_uses` | `uint32` | `optional` | `` |  |
| 5 | `gifting_max` | `int32` | `optional` | `` |  |
| 6 | `gifting_window_hours` | `uint32` | `optional` | `` |  |
| 7 | `trade_restriction` | `.EGCMsgInitiateTradeResponse` | `optional` | `` | default = k_EGCMsgInitiateTradeResponse_Accepted |

</details>

<details>
<summary><code>CMsgClientToGCUnwrapGift</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetGiftPermissions</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCGetGiftPermissionsResponse</code> — fields: 6; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `is_unlimited` | `bool` | `optional` | `` |  |
| 3 | `has_two_factor` | `bool` | `optional` | `` |  |
| 6 | `sender_permission` | `.EGCMsgInitiateTradeResponse` | `optional` | `` | default = k_EGCMsgInitiateTradeResponse_Accepted |
| 7 | `friendship_age_requirement` | `uint32` | `optional` | `` |  |
| 8 | `friendship_age_requirement_two_factor` | `uint32` | `optional` | `` |  |
| 9 | `friend_permissions` | `.CMsgClientToGCGetGiftPermissionsResponse.FriendPermission` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetGiftPermissionsResponse.FriendPermission</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCGetGiftPermissionsResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `permission` | `.EGCMsgInitiateTradeResponse` | `optional` | `` | default = k_EGCMsgInitiateTradeResponse_Accepted |

</details>

<details>
<summary><code>CMsgClientToGCUnpackBundle</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCUnpackBundleResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `unpacked_item_ids` | `uint64` | `repeated` | `` |  |
| 2 | `response` | `.CMsgClientToGCUnpackBundleResponse.EUnpackBundle` | `optional` | `` | default = k_UnpackBundle_Succeeded |
| 3 | `unpacked_item_def_indexes` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCPackBundle</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_ids` | `uint64` | `repeated` | `` |  |
| 2 | `bundle_item_def_index` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCPackBundleResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_id` | `uint64` | `optional` | `` |  |
| 2 | `response` | `.CMsgClientToGCPackBundleResponse.EPackBundle` | `optional` | `` | default = k_PackBundle_Succeeded |

</details>

<details>
<summary><code>CMsgGCToClientStoreTransactionCompleted</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `txn_id` | `uint64` | `optional` | `` |  |
| 2 | `item_ids` | `uint64` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCEquipItems</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `equips` | `.CMsgAdjustItemEquippedState` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCEquipItemsResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `so_cache_version_id` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCSetItemStyle</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_id` | `uint64` | `optional` | `` |  |
| 2 | `style_index` | `uint32` | `optional` | `` | default = 255 |

</details>

<details>
<summary><code>CMsgClientToGCSetItemStyleResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCSetItemStyleResponse.ESetStyle` | `optional` | `` | default = k_SetStyle_Succeeded |

</details>

<details>
<summary><code>CMsgClientToGCUnlockItemStyle</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_to_unlock` | `uint64` | `optional` | `` |  |
| 2 | `style_index` | `uint32` | `optional` | `` | default = 255 |
| 3 | `consumable_item_ids` | `uint64` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCUnlockItemStyleResponse</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCUnlockItemStyleResponse.EUnlockStyle` | `optional` | `` | default = k_UnlockStyle_Succeeded |
| 2 | `item_id` | `uint64` | `optional` | `` |  |
| 3 | `style_index` | `uint32` | `optional` | `` | default = 255 |
| 4 | `style_prereq` | `uint32` | `optional` | `` | default = 255 |

</details>

<details>
<summary><code>CMsgClientToGCSetItemInventoryCategory</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_ids` | `uint64` | `repeated` | `` |  |
| 2 | `set_to_value` | `uint32` | `optional` | `` |  |
| 3 | `remove_categories` | `uint32` | `optional` | `` |  |
| 4 | `add_categories` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCUnlockCrate</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `crate_item_id` | `uint64` | `optional` | `` |  |
| 2 | `key_item_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCUnlockCrateResponse</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.EGCMsgResponse` | `optional` | `` | default = k_EGCMsgResponseOK |
| 2 | `granted_items` | `.CMsgClientToGCUnlockCrateResponse.Item` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCUnlockCrateResponse.Item</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCUnlockCrateResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_id` | `uint64` | `optional` | `` |  |
| 2 | `def_index` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRemoveItemAttribute</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRemoveItemAttributeResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCRemoveItemAttributeResponse.ERemoveItemAttribute` | `optional` | `` | default = k_RemoveItemAttribute_Succeeded |
| 2 | `item_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCNameItem</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `subject_item_id` | `uint64` | `optional` | `` |  |
| 2 | `tool_item_id` | `uint64` | `optional` | `` |  |
| 3 | `name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCNameItemResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCNameItemResponse.ENameItem` | `optional` | `` | default = k_NameItem_Succeeded |
| 2 | `item_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCSetItemPosition</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_id` | `uint64` | `optional` | `` |  |
| 2 | `new_position` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CAttribute_ItemDynamicRecipeComponent</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_def` | `uint32` | `optional` | `` |  |
| 2 | `item_quality` | `uint32` | `optional` | `` |  |
| 3 | `item_flags` | `uint32` | `optional` | `` |  |
| 4 | `attributes_string` | `string` | `optional` | `` |  |
| 5 | `item_count` | `uint32` | `optional` | `` |  |
| 6 | `items_fulfilled` | `uint32` | `optional` | `` |  |
| 7 | `item_rarity` | `uint32` | `optional` | `` |  |
| 8 | `lootlist` | `string` | `optional` | `` |  |
| 9 | `fulfilled_item_id` | `uint64` | `optional` | `` |  |
| 10 | `associated_item_def` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CProtoItemSocket</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_id` | `uint64` | `optional` | `` |  |
| 2 | `attr_def_index` | `uint32` | `optional` | `` |  |
| 3 | `required_type` | `uint32` | `optional` | `` |  |
| 4 | `required_hero` | `string` | `optional` | `` |  |
| 5 | `gem_def_index` | `uint32` | `optional` | `` |  |
| 6 | `not_tradable` | `bool` | `optional` | `` |  |
| 7 | `required_item_slot` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CProtoItemSocket_Empty</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `socket` | `.CProtoItemSocket` | `optional` | `` |  |

</details>

<details>
<summary><code>CProtoItemSocket_Effect</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `socket` | `.CProtoItemSocket` | `optional` | `` |  |
| 2 | `effect` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CProtoItemSocket_Color</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `socket` | `.CProtoItemSocket` | `optional` | `` |  |
| 2 | `red` | `uint32` | `optional` | `` |  |
| 3 | `green` | `uint32` | `optional` | `` |  |
| 4 | `blue` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CProtoItemSocket_Strange</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `socket` | `.CProtoItemSocket` | `optional` | `` |  |
| 2 | `strange_type` | `uint32` | `optional` | `` |  |
| 3 | `strange_value` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CProtoItemSocket_Strange_DESERIALIZE_FROM_STRING_ONLY</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `socket` | `.CProtoItemSocket` | `optional` | `` |  |
| 2 | `strange_type` | `uint32` | `optional` | `` |  |
| 3 | `strange_value` | `uint32` | `optional` | `` |  |
| 4 | `ability_effect` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CProtoItemSocket_Spectator</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `socket` | `.CProtoItemSocket` | `optional` | `` |  |
| 2 | `games_viewed` | `uint32` | `optional` | `` |  |
| 3 | `corporation_id` | `uint32` | `optional` | `` |  |
| 4 | `league_id` | `uint32` | `optional` | `` |  |
| 5 | `team_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CProtoItemSocket_AssetModifier</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `socket` | `.CProtoItemSocket` | `optional` | `` |  |
| 2 | `asset_modifier` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CProtoItemSocket_AssetModifier_DESERIALIZE_FROM_STRING_ONLY</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `socket` | `.CProtoItemSocket` | `optional` | `` |  |
| 2 | `asset_modifier` | `uint32` | `optional` | `` |  |
| 3 | `anim_modifier` | `uint32` | `optional` | `` |  |
| 4 | `ability_effect` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CProtoItemSocket_Autograph</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `socket` | `.CProtoItemSocket` | `optional` | `` |  |
| 2 | `autograph` | `string` | `optional` | `` |  |
| 3 | `autograph_id` | `uint32` | `optional` | `` |  |
| 4 | `autograph_score` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CProtoItemSocket_StaticVisuals</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `socket` | `.CProtoItemSocket` | `optional` | `` |  |

</details>

<details>
<summary><code>CAttribute_String</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `value` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CWorkshop_GetItemDailyRevenue_Request</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `appid` | `uint32` | `optional` | `` |  |
| 2 | `item_id` | `uint32` | `optional` | `` |  |
| 3 | `date_start` | `uint32` | `optional` | `` |  |
| 4 | `date_end` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CWorkshop_GetItemDailyRevenue_Response</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `country_revenue` | `.CWorkshop_GetItemDailyRevenue_Response.CountryDailyRevenue` | `repeated` | `` |  |

</details>

<details>
<summary><code>CWorkshop_GetItemDailyRevenue_Response.CountryDailyRevenue</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CWorkshop_GetItemDailyRevenue_Response`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `country_code` | `string` | `optional` | `` |  |
| 2 | `date` | `uint32` | `optional` | `` |  |
| 3 | `revenue_usd` | `int64` | `optional` | `` |  |
| 4 | `units` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CWorkshop_GetPackageDailyRevenue_Request</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `packageid` | `uint32` | `optional` | `` |  |
| 2 | `date_start` | `uint32` | `optional` | `` |  |
| 3 | `date_end` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CWorkshop_GetPackageDailyRevenue_Response</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `country_revenue` | `.CWorkshop_GetPackageDailyRevenue_Response.CountryDailyRevenue` | `repeated` | `` |  |

</details>

<details>
<summary><code>CWorkshop_GetPackageDailyRevenue_Response.CountryDailyRevenue</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CWorkshop_GetPackageDailyRevenue_Response`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `country_code` | `string` | `optional` | `` |  |
| 2 | `date` | `uint32` | `optional` | `` |  |
| 3 | `revenue_usd` | `int64` | `optional` | `` |  |
| 4 | `units` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSQLGCToGCGrantBackpackSlots</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `add_slots` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCLookupAccountName</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCLookupAccountNameResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `account_name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCreateStaticRecipe</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `items` | `.CMsgClientToGCCreateStaticRecipe.Item` | `repeated` | `` |  |
| 2 | `recipe_def_index` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCreateStaticRecipe.Item</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCCreateStaticRecipe`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_id` | `uint64` | `optional` | `` |  |
| 2 | `slot_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCreateStaticRecipeResponse</code> — fields: 4; oneofs: 0; nested messages: 3; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCCreateStaticRecipeResponse.EResponse` | `optional` | `` | default = eResponse_Success |
| 2 | `output_items` | `.CMsgClientToGCCreateStaticRecipeResponse.OutputItem` | `repeated` | `` |  |
| 3 | `input_errors` | `.CMsgClientToGCCreateStaticRecipeResponse.InputError` | `repeated` | `` |  |
| 4 | `additional_outputs` | `.CMsgClientToGCCreateStaticRecipeResponse.AdditionalOutput` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCreateStaticRecipeResponse.OutputItem</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCCreateStaticRecipeResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `def_index` | `uint32` | `optional` | `` |  |
| 2 | `item_id` | `uint64` | `optional` | `` |  |
| 3 | `slot_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCreateStaticRecipeResponse.InputError</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCCreateStaticRecipeResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `slot_id` | `uint32` | `optional` | `` |  |
| 2 | `error` | `.CMsgClientToGCCreateStaticRecipeResponse.EResponse` | `optional` | `` | default = eResponse_Success |

</details>

<details>
<summary><code>CMsgClientToGCCreateStaticRecipeResponse.AdditionalOutput</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCCreateStaticRecipeResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `slot_id` | `uint32` | `optional` | `` |  |
| 2 | `value` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgProcessTransactionOrder</code> — fields: 9; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `txn_id` | `uint64` | `optional` | `` |  |
| 2 | `steam_txn_id` | `uint64` | `optional` | `` |  |
| 3 | `partner_txn_id` | `uint64` | `optional` | `` |  |
| 4 | `steam_id` | `fixed64` | `optional` | `` |  |
| 5 | `time_stamp` | `uint32` | `optional` | `` |  |
| 6 | `watermark` | `uint64` | `optional` | `` |  |
| 7 | `purchase_report_status` | `int32` | `optional` | `` |  |
| 8 | `currency` | `uint32` | `optional` | `` |  |
| 9 | `items` | `.CMsgProcessTransactionOrder.Item` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgProcessTransactionOrder.Item</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgProcessTransactionOrder`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_def_index` | `uint32` | `optional` | `` |  |
| 2 | `item_price` | `uint32` | `optional` | `` |  |
| 3 | `quantity` | `uint32` | `optional` | `` |  |
| 4 | `category_desc` | `string` | `optional` | `` |  |
| 5 | `store_purchase_type` | `uint32` | `optional` | `` |  |
| 6 | `source_reference_id` | `uint64` | `optional` | `` |  |
| 7 | `parent_stack_index` | `int32` | `optional` | `` |  |
| 8 | `default_price` | `bool` | `optional` | `` |  |
| 9 | `is_user_facing` | `bool` | `optional` | `` |  |
| 11 | `price_index` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCStoreProcessCDKeyTransaction</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `order` | `.CMsgProcessTransactionOrder` | `optional` | `` |  |
| 2 | `reason_code` | `uint32` | `optional` | `` |  |
| 3 | `partner` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCStoreProcessCDKeyTransactionResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `success` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCStoreProcessSettlement</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `order` | `.CMsgProcessTransactionOrder` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCStoreProcessSettlementResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `success` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCBroadcastConsoleCommand</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `con_command` | `string` | `optional` | `` |  |
| 2 | `report_output` | `bool` | `optional` | `` |  |
| 3 | `sending_gc` | `int32` | `optional` | `` | default = -1 |
| 4 | `output_initiator` | `string` | `optional` | `` |  |
| 5 | `sender_source` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCConsoleOutput</code> — fields: 4; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `initiator` | `string` | `optional` | `` |  |
| 2 | `sending_gc` | `int32` | `optional` | `` | default = -1 |
| 3 | `msgs` | `.CMsgGCToGCConsoleOutput.OutputLine` | `repeated` | `` |  |
| 4 | `is_last_for_source_job` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCConsoleOutput.OutputLine</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToGCConsoleOutput`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `text` | `string` | `optional` | `` |  |
| 2 | `spew_level` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgItemAges</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `max_item_id_timestamps` | `.CMsgItemAges.MaxItemIDTimestamp` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgItemAges.MaxItemIDTimestamp</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgItemAges`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `timestamp` | `uint32` | `optional` | `` |  |
| 2 | `max_item_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCInternalTestMsg</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `sending_gc` | `int32` | `optional` | `` | default = -1 |
| 2 | `sender_id` | `fixed64` | `optional` | `` |  |
| 3 | `context` | `uint32` | `optional` | `` |  |
| 4 | `message_id` | `uint32` | `optional` | `` |  |
| 5 | `message_body` | `bytes` | `optional` | `` |  |
| 6 | `job_id_source` | `fixed64` | `optional` | `` |  |
| 7 | `job_id_target` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCClientServerVersionsUpdated</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `client_min_allowed_version` | `uint32` | `optional` | `` |  |
| 2 | `client_active_version` | `uint32` | `optional` | `` |  |
| 3 | `server_active_version` | `uint32` | `optional` | `` |  |
| 4 | `server_deployed_version` | `uint32` | `optional` | `` |  |
| 5 | `what_changed` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCBroadcastMessageFromSub</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `msg_id` | `uint32` | `optional` | `` |  |
| 2 | `serialized_msg` | `bytes` | `optional` | `` |  |
| 3 | `account_id_list` | `uint32` | `repeated` | `` | packed = true |
| 4 | `steam_id_list` | `fixed64` | `repeated` | `` | packed = true |

</details>

<details>
<summary><code>CMsgGCToClientCurrencyPricePoints</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `price_key` | `uint64` | `repeated` | `` | packed = true |
| 2 | `currencies` | `.CMsgGCToClientCurrencyPricePoints.Currency` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientCurrencyPricePoints.Currency</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientCurrencyPricePoints`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `currency_id` | `uint32` | `optional` | `` |  |
| 2 | `currency_price` | `uint64` | `repeated` | `` | packed = true |

</details>

<details>
<summary><code>CMsgBannedWordList</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `version` | `uint32` | `optional` | `` |  |
| 2 | `banned_words` | `string` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCFlushSteamInventoryCache</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `keys` | `.CMsgGCToGCFlushSteamInventoryCache.Key` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCFlushSteamInventoryCache.Key</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToGCFlushSteamInventoryCache`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steamid` | `uint64` | `optional` | `` |  |
| 2 | `contextid` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCUpdateSubscriptionItems</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `always_notify` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCSelfPing</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `sample_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCGetInfuxIntervalStats</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgGCToGCGetInfuxIntervalStatsResponse</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `stat_ids` | `fixed32` | `repeated` | `` | packed = true |
| 2 | `stat_total` | `uint64` | `repeated` | `` | packed = true |
| 3 | `stat_samples` | `uint32` | `repeated` | `` | packed = true |
| 4 | `stat_max` | `uint32` | `repeated` | `` | packed = true |
| 5 | `sample_duration_ms` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCPurchaseSucceeded</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCGetLimitedItemPurchaseQuantity</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_def` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetLimitedItemPurchaseQuantityResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCGetLimitedItemPurchaseQuantityResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `quantity_purchased` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetInFlightItemCharges</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_def` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetInFlightItemChargesResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCGetInFlightItemChargesResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `charges_in_flight` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCPurchaseChargeCostItems</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `items` | `.CMsgClientToGCPurchaseChargeCostItems.Item` | `repeated` | `` |  |
| 2 | `currency` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCPurchaseChargeCostItems.Item</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCPurchaseChargeCostItems`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_def_index` | `uint32` | `optional` | `` |  |
| 2 | `quantity` | `uint32` | `optional` | `` |  |
| 3 | `source_reference_id` | `uint64` | `optional` | `` |  |
| 4 | `price_index` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCPurchaseChargeCostItemsResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCPurchaseChargeCostItemsResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `item_ids` | `uint64` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientInFlightChargesUpdated</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `in_flight_charges` | `.CMsgGCToClientInFlightChargesUpdated.ItemCharges` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientInFlightChargesUpdated.ItemCharges</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientInFlightChargesUpdated`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_def` | `uint32` | `optional` | `` |  |
| 2 | `charges_in_flight` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCancelUnfinalizedTransactions</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `unused` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCancelUnfinalizedTransactionsResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCUpdateWelcomeMsg</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `server` | `bool` | `optional` | `` |  |
| 2 | `new_msg` | `.CExtraMsgBlock` | `optional` | `` |  |
| 3 | `broadcast` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRecycleMultipleItems</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `items` | `.CMsgClientToGCRecycleMultipleItems.Item` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRecycleMultipleItems.Item</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCRecycleMultipleItems`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_id` | `uint64` | `optional` | `` |  |
| 2 | `slot_id` | `uint32` | `optional` | `` |  |
| 3 | `recipe_def_index` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRecycleMultipleItemsResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `responses` | `.CMsgClientToGCCreateStaticRecipeResponse` | `repeated` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>EGCItemMsg</code> — values: 135</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EMsgGCBase` | 1000 |
| `k_EMsgGCSetItemPosition` | 1001 |
| `k_EMsgClientToGCPackBundle` | 1002 |
| `k_EMsgClientToGCPackBundleResponse` | 1003 |
| `k_EMsgGCDelete` | 1004 |
| `k_EMsgGCVerifyCacheSubscription` | 1005 |
| `k_EMsgClientToGCNameItem` | 1006 |
| `k_EMsgGCPaintItem` | 1009 |
| `k_EMsgGCPaintItemResponse` | 1010 |
| `k_EMsgGCNameBaseItem` | 1019 |
| `k_EMsgGCNameBaseItemResponse` | 1020 |
| `k_EMsgGCUseItemRequest` | 1025 |
| `k_EMsgGCUseItemResponse` | 1026 |
| `k_EMsgGCGiftedItems` | 1027 |
| `k_EMsgGCUnwrapGiftRequest` | 1037 |
| `k_EMsgGCUnwrapGiftResponse` | 1038 |
| `k_EMsgGCSortItems` | 1041 |
| `k_EMsgGCBackpackSortFinished` | 1058 |
| `k_EMsgGCAdjustItemEquippedState` | 1059 |
| `k_EMsgGCItemAcknowledged` | 1062 |
| `k_EMsgClientToGCNameItemResponse` | 1068 |
| `k_EMsgGCApplyStrangePart` | 1073 |
| `k_EMsgGCApplyPennantUpgrade` | 1076 |
| `k_EMsgGCSetItemPositions` | 1077 |
| `k_EMsgGCApplyEggEssence` | 1078 |
| `k_EMsgGCNameEggEssenceResponse` | 1079 |
| `k_EMsgGCExtractGems` | 1086 |
| `k_EMsgGCAddSocket` | 1087 |
| `k_EMsgGCAddItemToSocket` | 1088 |
| `k_EMsgGCAddItemToSocketResponse` | 1089 |
| `k_EMsgGCAddSocketResponse` | 1090 |
| `k_EMsgGCResetStrangeGemCount` | 1091 |
| `k_EMsgGCRequestCrateItems` | 1092 |
| `k_EMsgGCRequestCrateItemsResponse` | 1093 |
| `k_EMsgGCExtractGemsResponse` | 1094 |
| `k_EMsgGCResetStrangeGemCountResponse` | 1095 |
| `k_EMsgGCServerUseItemRequest` | 1103 |
| `k_EMsgGCAddGiftItem` | 1104 |
| `k_EMsgSQLGCToGCRevokeUntrustedGift` | 1105 |
| `k_EMsgClientToGCRemoveItemGifterAttributes` | 1109 |
| `k_EMsgClientToGCRemoveItemName` | 1110 |
| `k_EMsgClientToGCRemoveItemDescription` | 1111 |
| `k_EMsgClientToGCRemoveItemAttributeResponse` | 1112 |
| `k_EMsgGCDev_NewItemRequest` | 2001 |
| `k_EMsgGCDev_NewItemRequestResponse` | 2002 |
| `k_EMsgGCDev_UnlockAllItemStylesRequest` | 2003 |
| `k_EMsgGCDev_UnlockAllItemStylesResponse` | 2004 |
| `k_EMsgGCStorePurchaseFinalize` | 2504 |
| `k_EMsgGCStorePurchaseFinalizeResponse` | 2505 |
| `k_EMsgGCStorePurchaseCancel` | 2506 |
| `k_EMsgGCStorePurchaseCancelResponse` | 2507 |
| `k_EMsgGCStorePurchaseInit` | 2510 |
| `k_EMsgGCStorePurchaseInitResponse` | 2511 |
| `k_EMsgGCToGCBannedWordListUpdated` | 2515 |
| `k_EMsgGCToGCDirtySDOCache` | 2516 |
| `k_EMsgGCToGCUpdateSQLKeyValue` | 2518 |
| `k_EMsgGCToGCBroadcastConsoleCommand` | 2521 |
| `k_EMsgGCServerVersionUpdated` | 2522 |
| `k_EMsgGCApplyAutograph` | 2523 |
| `k_EMsgGCToGCWebAPIAccountChanged` | 2524 |
| `k_EMsgGCClientVersionUpdated` | 2528 |
| `k_EMsgGCToGCUpdateWelcomeMsg` | 2529 |
| `k_EMsgGCToGCPlayerStrangeCountAdjustments` | 2535 |
| `k_EMsgGCRequestStoreSalesData` | 2536 |
| `k_EMsgGCRequestStoreSalesDataResponse` | 2537 |
| `k_EMsgGCRequestStoreSalesDataUpToDateResponse` | 2538 |
| `k_EMsgGCToGCPingRequest` | 2539 |
| `k_EMsgGCToGCPingResponse` | 2540 |
| `k_EMsgGCToGCGetUserSessionServer` | 2541 |
| `k_EMsgGCToGCGetUserSessionServerResponse` | 2542 |
| `k_EMsgGCToGCGetUserServerMembers` | 2543 |
| `k_EMsgGCToGCGetUserServerMembersResponse` | 2544 |
| `k_EMsgGCToGCCanUseDropRateBonus` | 2547 |
| `k_EMsgSQLAddDropRateBonus` | 2548 |
| `k_EMsgGCToGCRefreshSOCache` | 2549 |
| `k_EMsgGCToGCGrantAccountRolledItems` | 2554 |
| `k_EMsgGCToGCGrantSelfMadeItemToAccount` | 2555 |
| `k_EMsgGCToGCUnlockCrate` | 2556 |
| `k_EMsgGCStatueCraft` | 2561 |
| `k_EMsgGCRedeemCode` | 2562 |
| `k_EMsgGCRedeemCodeResponse` | 2563 |
| `k_EMsgGCToGCItemConsumptionRollback` | 2564 |
| `k_EMsgClientToGCWrapAndDeliverGift` | 2565 |
| `k_EMsgClientToGCWrapAndDeliverGiftResponse` | 2566 |
| `k_EMsgClientToGCUnpackBundleResponse` | 2567 |
| `k_EMsgGCToClientStoreTransactionCompleted` | 2568 |
| `k_EMsgClientToGCEquipItems` | 2569 |
| `k_EMsgClientToGCEquipItemsResponse` | 2570 |
| `k_EMsgClientToGCUnlockItemStyle` | 2571 |
| `k_EMsgClientToGCUnlockItemStyleResponse` | 2572 |
| `k_EMsgClientToGCSetItemInventoryCategory` | 2573 |
| `k_EMsgClientToGCUnlockCrate` | 2574 |
| `k_EMsgClientToGCUnlockCrateResponse` | 2575 |
| `k_EMsgClientToGCUnpackBundle` | 2576 |
| `k_EMsgClientToGCSetItemStyle` | 2577 |
| `k_EMsgClientToGCSetItemStyleResponse` | 2578 |
| `k_EMsgSQLGCToGCGrantBackpackSlots` | 2580 |
| `k_EMsgClientToGCLookupAccountName` | 2581 |
| `k_EMsgClientToGCLookupAccountNameResponse` | 2582 |
| `k_EMsgClientToGCCreateStaticRecipe` | 2584 |
| `k_EMsgClientToGCCreateStaticRecipeResponse` | 2585 |
| `k_EMsgGCToGCStoreProcessCDKeyTransaction` | 2586 |
| `k_EMsgGCToGCStoreProcessCDKeyTransactionResponse` | 2587 |
| `k_EMsgGCToGCStoreProcessSettlement` | 2588 |
| `k_EMsgGCToGCStoreProcessSettlementResponse` | 2589 |
| `k_EMsgGCToGCConsoleOutput` | 2590 |
| `k_EMsgGCToClientItemAges` | 2591 |
| `k_EMsgGCToGCInternalTestMsg` | 2592 |
| `k_EMsgGCToGCClientServerVersionsUpdated` | 2593 |
| `k_EMsgGCUseMultipleItemsRequest` | 2594 |
| `k_EMsgGCGetAccountSubscriptionItem` | 2595 |
| `k_EMsgGCGetAccountSubscriptionItemResponse` | 2596 |
| `k_EMsgGCToGCBroadcastMessageFromSub` | 2598 |
| `k_EMsgGCToClientCurrencyPricePoints` | 2599 |
| `k_EMsgGCToGCAddSubscriptionTime` | 2600 |
| `k_EMsgGCToGCFlushSteamInventoryCache` | 2601 |
| `k_EMsgGCRequestCrateEscalationLevel` | 2602 |
| `k_EMsgGCRequestCrateEscalationLevelResponse` | 2603 |
| `k_EMsgGCToGCUpdateSubscriptionItems` | 2604 |
| `k_EMsgGCToGCSelfPing` | 2605 |
| `k_EMsgGCToGCGetInfuxIntervalStats` | 2606 |
| `k_EMsgGCToGCGetInfuxIntervalStatsResponse` | 2607 |
| `k_EMsgGCToGCPurchaseSucceeded` | 2608 |
| `k_EMsgClientToGCGetLimitedItemPurchaseQuantity` | 2609 |
| `k_EMsgClientToGCGetLimitedItemPurchaseQuantityResponse` | 2610 |
| `k_EMsgGCToGCBetaDeleteItems` | 2611 |
| `k_EMsgClientToGCGetInFlightItemCharges` | 2612 |
| `k_EMsgClientToGCGetInFlightItemChargesResponse` | 2613 |
| `k_EMsgGCToClientInFlightChargesUpdated` | 2614 |
| `k_EMsgClientToGCPurchaseChargeCostItems` | 2615 |
| `k_EMsgClientToGCPurchaseChargeCostItemsResponse` | 2616 |
| `k_EMsgClientToGCCancelUnfinalizedTransactions` | 2617 |
| `k_EMsgClientToGCCancelUnfinalizedTransactionsResponse` | 2618 |
| `k_EMsgClientToGCRecycleMultipleItems` | 2619 |
| `k_EMsgClientToGCRecycleMultipleItemsResponse` | 2620 |

</details>

<details>
<summary><code>EGCMsgInitiateTradeResponse</code> — values: 25</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EGCMsgInitiateTradeResponse_Accepted` | 0 |
| `k_EGCMsgInitiateTradeResponse_Declined` | 1 |
| `k_EGCMsgInitiateTradeResponse_VAC_Banned_Initiator` | 2 |
| `k_EGCMsgInitiateTradeResponse_VAC_Banned_Target` | 3 |
| `k_EGCMsgInitiateTradeResponse_Target_Already_Trading` | 4 |
| `k_EGCMsgInitiateTradeResponse_Disabled` | 5 |
| `k_EGCMsgInitiateTradeResponse_NotLoggedIn` | 6 |
| `k_EGCMsgInitiateTradeResponse_Cancel` | 7 |
| `k_EGCMsgInitiateTradeResponse_TooSoon` | 8 |
| `k_EGCMsgInitiateTradeResponse_TooSoonPenalty` | 9 |
| `k_EGCMsgInitiateTradeResponse_Trade_Banned_Initiator` | 10 |
| `k_EGCMsgInitiateTradeResponse_Trade_Banned_Target` | 11 |
| `k_EGCMsgInitiateTradeResponse_Free_Account_Initiator_DEPRECATED` | 12 |
| `k_EGCMsgInitiateTradeResponse_Shared_Account_Initiator` | 13 |
| `k_EGCMsgInitiateTradeResponse_Service_Unavailable` | 14 |
| `k_EGCMsgInitiateTradeResponse_Target_Blocked` | 15 |
| `k_EGCMsgInitiateTradeResponse_NeedVerifiedEmail` | 16 |
| `k_EGCMsgInitiateTradeResponse_NeedSteamGuard` | 17 |
| `k_EGCMsgInitiateTradeResponse_SteamGuardDuration` | 18 |
| `k_EGCMsgInitiateTradeResponse_TheyCannotTrade` | 19 |
| `k_EGCMsgInitiateTradeResponse_Recent_Password_Reset` | 20 |
| `k_EGCMsgInitiateTradeResponse_Using_New_Device` | 21 |
| `k_EGCMsgInitiateTradeResponse_Sent_Invalid_Cookie` | 22 |
| `k_EGCMsgInitiateTradeResponse_TooRecentFriend` | 23 |
| `k_EGCMsgInitiateTradeResponse_WalledFundsNotTrusted` | 24 |

</details>

<details>
<summary><code>CMsgRequestCrateItemsResponse.EResult</code> — values: 2</summary>

- Parent: `CMsgRequestCrateItemsResponse`

| Name | Number |
|---|---:|
| `k_Succeeded` | 0 |
| `k_Failed` | 1 |

</details>

<details>
<summary><code>CMsgRequestCrateEscalationLevelResponse.EResult</code> — values: 2</summary>

- Parent: `CMsgRequestCrateEscalationLevelResponse`

| Name | Number |
|---|---:|
| `k_Succeeded` | 0 |
| `k_Failed` | 1 |

</details>

<details>
<summary><code>CMsgRedeemCodeResponse.EResultCode</code> — values: 4</summary>

- Parent: `CMsgRedeemCodeResponse`

| Name | Number |
|---|---:|
| `k_Succeeded` | 0 |
| `k_Failed_CodeNotFound` | 1 |
| `k_Failed_CodeAlreadyUsed` | 2 |
| `k_Failed_OtherError` | 3 |

</details>

<details>
<summary><code>CMsgClientToGCUnpackBundleResponse.EUnpackBundle</code> — values: 7</summary>

- Parent: `CMsgClientToGCUnpackBundleResponse`

| Name | Number |
|---|---:|
| `k_UnpackBundle_Succeeded` | 0 |
| `k_UnpackBundle_Failed_ItemIsNotBundle` | 1 |
| `k_UnpackBundle_Failed_UnableToCreateContainedItem` | 2 |
| `k_UnpackBundle_Failed_SOCacheError` | 3 |
| `k_UnpackBundle_Failed_ItemIsInvalid` | 4 |
| `k_UnpackBundle_Failed_BadItemQuantity` | 5 |
| `k_UnpackBundle_Failed_UnableToDeleteItem` | 6 |

</details>

<details>
<summary><code>CMsgClientToGCPackBundleResponse.EPackBundle</code> — values: 15</summary>

- Parent: `CMsgClientToGCPackBundleResponse`

| Name | Number |
|---|---:|
| `k_PackBundle_Succeeded` | 0 |
| `k_PackBundle_Failed_InternalError` | 1 |
| `k_PackBundle_Failed_ItemIsNotBundle` | 2 |
| `k_PackBundle_Failed_SOCacheError` | 3 |
| `k_PackBundle_Failed_ItemIsInvalid` | 4 |
| `k_PackBundle_Failed_BadItemQuantity` | 5 |
| `k_PackBundle_Failed_UnableToDeleteItem` | 6 |
| `k_PackBundle_Failed_BundleCannotBePacked` | 7 |
| `k_PackBundle_Failed_ItemIsUntradeable` | 8 |
| `k_PackBundle_Failed_ItemIsEquipped` | 9 |
| `k_PackBundle_Failed_ItemHasGems` | 10 |
| `k_PackBundle_Failed_ItemMixedQuality` | 11 |
| `k_PackBundle_Failed_ItemInvalidQuality` | 12 |
| `k_PackBundle_Failed_ItemIsNonEconomy` | 13 |
| `k_PackBundle_Failed_Disabled` | 14 |

</details>

<details>
<summary><code>CMsgClientToGCSetItemStyleResponse.ESetStyle</code> — values: 3</summary>

- Parent: `CMsgClientToGCSetItemStyleResponse`

| Name | Number |
|---|---:|
| `k_SetStyle_Succeeded` | 0 |
| `k_SetStyle_Failed` | 1 |
| `k_SetStyle_Failed_StyleIsLocked` | 2 |

</details>

<details>
<summary><code>CMsgClientToGCUnlockItemStyleResponse.EUnlockStyle</code> — values: 12</summary>

- Parent: `CMsgClientToGCUnlockItemStyleResponse`

| Name | Number |
|---|---:|
| `k_UnlockStyle_Succeeded` | 0 |
| `k_UnlockStyle_Failed_PreReq` | 1 |
| `k_UnlockStyle_Failed_CantAfford` | 2 |
| `k_UnlockStyle_Failed_CantCommit` | 3 |
| `k_UnlockStyle_Failed_CantLockCache` | 4 |
| `k_UnlockStyle_Failed_CantAffordAttrib` | 5 |
| `k_UnlockStyle_Failed_CantAffordGem` | 6 |
| `k_UnlockStyle_Failed_NoCompendiumLevel` | 7 |
| `k_UnlockStyle_Failed_AlreadyUnlocked` | 8 |
| `k_UnlockStyle_Failed_OtherError` | 9 |
| `k_UnlockStyle_Failed_ItemIsInvalid` | 10 |
| `k_UnlockStyle_Failed_ToolIsInvalid` | 11 |

</details>

<details>
<summary><code>CMsgClientToGCRemoveItemAttributeResponse.ERemoveItemAttribute</code> — values: 5</summary>

- Parent: `CMsgClientToGCRemoveItemAttributeResponse`

| Name | Number |
|---|---:|
| `k_RemoveItemAttribute_Succeeded` | 0 |
| `k_RemoveItemAttribute_Failed` | 1 |
| `k_RemoveItemAttribute_Failed_ItemIsInvalid` | 2 |
| `k_RemoveItemAttribute_Failed_AttributeCannotBeRemoved` | 3 |
| `k_RemoveItemAttribute_Failed_AttributeDoesntExist` | 4 |

</details>

<details>
<summary><code>CMsgClientToGCNameItemResponse.ENameItem</code> — values: 5</summary>

- Parent: `CMsgClientToGCNameItemResponse`

| Name | Number |
|---|---:|
| `k_NameItem_Succeeded` | 0 |
| `k_NameItem_Failed` | 1 |
| `k_NameItem_Failed_ToolIsInvalid` | 2 |
| `k_NameItem_Failed_ItemIsInvalid` | 3 |
| `k_NameItem_Failed_NameIsInvalid` | 4 |

</details>

<details>
<summary><code>CMsgClientToGCCreateStaticRecipeResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCCreateStaticRecipeResponse`

| Name | Number |
|---|---:|
| `eResponse_Success` | 0 |
| `eResponse_OfferingDisabled` | 1 |
| `eResponse_InvalidItems` | 2 |
| `eResponse_InternalError` | 3 |
| `eResponse_MissingLeague` | 4 |
| `eResponse_MissingEvent` | 5 |

</details>

<details>
<summary><code>CMsgClientToGCGetLimitedItemPurchaseQuantityResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCGetLimitedItemPurchaseQuantityResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidItemDef` | 5 |
| `k_eItemDefNotLimited` | 6 |

</details>

<details>
<summary><code>CMsgClientToGCGetInFlightItemChargesResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCGetInFlightItemChargesResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidItemDef` | 5 |

</details>

<details>
<summary><code>CMsgClientToGCPurchaseChargeCostItemsResponse.EResponse</code> — values: 10</summary>

- Parent: `CMsgClientToGCPurchaseChargeCostItemsResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidParam` | 5 |
| `k_eInvalidPrice` | 6 |
| `k_eInsufficientCharges` | 7 |
| `k_eLimitedItem` | 8 |
| `k_eMissingPrereq` | 10 |

</details>
