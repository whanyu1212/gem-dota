# event_gcmessages_client.proto

**Not used by gem**: nothing in this file is needed to parse a replay. See [the map of all 84 files](../proto-files.md#the-map-all-84-files) for what it belongs to.

- Module: `event_gcmessages_client_pb2`
- Imports: **4**
- Messages: **20** (top-level: 20)
- Enums: **9** (top-level: 1)

## Imports

- `gcsdk_gcmessages.proto`
- `events.proto`
- `event_gcmessages_common.proto`
- `google/protobuf/descriptor.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgClientToGCGetEventPoints</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` |  | default = EVENT_ID_NONE |
| 2 | `account_id` | `uint32` | `optional` |  |  |

</details>

<details>
<summary><code>CMsgClientToGCGetEventPointsResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCGetEventPointsResponse.EResponse` | `optional` |  | default = k_eInternalError |
| 2 | `event_points` | `.CMsgUserEventPoints` | `optional` |  |  |

</details>

<details>
<summary><code>CMsgGCToClientEventPointsUpdated</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` |  | default = EVENT_ID_NONE |
| 2 | `event_points` | `.CMsgUserEventPoints` | `optional` |  |  |
| 3 | `audit_action` | `uint32` | `optional` |  |  |

</details>

<details>
<summary><code>CMsgClientToGCGetPeriodicResource</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` |  |  |
| 2 | `periodic_resource_id` | `uint32` | `optional` |  | boxed_type = "PeriodicResourceID_t" |
| 3 | `timestamp` | `uint32` | `optional` |  |  |

</details>

<details>
<summary><code>CMsgClientToGCGetPeriodicResourceResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCGetPeriodicResourceResponse.EResponse` | `optional` |  | default = k_eInternalError |
| 2 | `periodic_resource_value` | `.CMsgPeriodicResourceValue` | `optional` |  |  |

</details>

<details>
<summary><code>CMsgGCToClientPeriodicResourceUpdated</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `periodic_resource_key` | `.CMsgPeriodicResourceKey` | `optional` |  |  |
| 2 | `periodic_resource_value` | `.CMsgPeriodicResourceValue` | `optional` |  |  |

</details>

<details>
<summary><code>CMsgClientToGCDevGrantEventPoints</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` |  | default = EVENT_ID_NONE |
| 2 | `event_points` | `uint32` | `optional` |  |  |
| 3 | `premium_points` | `uint32` | `optional` |  |  |

</details>

<details>
<summary><code>CMsgClientToGCDevGrantEventPointsResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCDevGrantEventPointsResponse.EResponse` | `optional` |  | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCDevReloadEventSchema</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCDevReloadEventSchemaResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCDevReloadEventSchemaResponse.EResponse` | `optional` |  | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCDevResetEventState</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` |  | default = EVENT_ID_NONE |
| 2 | `remove_audit` | `bool` | `optional` |  |  |

</details>

<details>
<summary><code>CMsgClientToGCDevResetEventStateResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCDevResetEventStateResponse.EResponse` | `optional` |  | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCDevGrantEventAction</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` |  | default = EVENT_ID_NONE |
| 2 | `action_id` | `uint32` | `optional` |  |  |
| 3 | `action_score` | `uint32` | `optional` |  |  |

</details>

<details>
<summary><code>CMsgClientToGCDevGrantEventActionResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCDevGrantEventActionResponse.EResponse` | `optional` |  | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCDevResetEventActions</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` |  | default = EVENT_ID_NONE |
| 2 | `start_action_id` | `uint32` | `optional` |  |  |
| 3 | `end_action_id` | `uint32` | `optional` |  |  |
| 4 | `remove_audit` | `bool` | `optional` |  |  |

</details>

<details>
<summary><code>CMsgClientToGCDevResetEventActionsResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCDevResetEventActionsResponse.EResponse` | `optional` |  | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCClaimEventAction</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` |  | default = EVENT_ID_NONE |
| 2 | `action_id` | `uint32` | `optional` |  |  |
| 3 | `quantity` | `uint32` | `optional` |  |  |
| 4 | `score_mode` | `.EEventActionScoreMode` | `optional` |  | default = k_eEventActionScoreMode_Add |
| 5 | `suppress_rewards` | `bool` | `optional` |  |  |
| 6 | `claim_data` | `bytes` | `optional` |  |  |
| 7 | `consume_item_id` | `uint64` | `optional` |  | boxed_type = "itemid_t" |

</details>

<details>
<summary><code>CMsgEventActionGrantLootListRewardData</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_def` | `uint32` | `repeated` |  | boxed_type = "item_definition_index_t" |

</details>

<details>
<summary><code>CMsgEventActionGrantResult</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `action_id` | `uint32` | `optional` |  |  |
| 2 | `grant_index` | `uint32` | `optional` |  |  |
| 3 | `score_index` | `uint32` | `optional` |  |  |
| 4 | `reward_index` | `uint32` | `optional` |  |  |
| 5 | `grant_data` | `bytes` | `optional` |  |  |

</details>

<details>
<summary><code>CMsgClientToGCClaimEventActionResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCClaimEventActionResponse.EResponse` | `optional` |  | default = k_eInternalError |
| 2 | `grant_results` | `.CMsgEventActionGrantResult` | `repeated` |  |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>EGCEventClientMessages</code> — values: 18</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EMsgClientToGCGetEventPoints` | 15000 |
| `k_EMsgClientToGCGetEventPointsResponse` | 15001 |
| `k_EMsgGCToClientEventPointsUpdated` | 15002 |
| `k_EMsgClientToGCDevGrantEventPoints` | 15003 |
| `k_EMsgClientToGCDevGrantEventPointsResponse` | 15004 |
| `k_EMsgClientToGCDevReloadEventSchema` | 15005 |
| `k_EMsgClientToGCDevReloadEventSchemaResponse` | 15006 |
| `k_EMsgClientToGCDevResetEventState` | 15007 |
| `k_EMsgClientToGCDevResetEventStateResponse` | 15008 |
| `k_EMsgClientToGCDevGrantEventAction` | 15009 |
| `k_EMsgClientToGCDevGrantEventActionResponse` | 15010 |
| `k_EMsgClientToGCDevResetEventActions` | 15011 |
| `k_EMsgClientToGCDevResetEventActionsResponse` | 15012 |
| `k_EMsgClientToGCClaimEventAction` | 15020 |
| `k_EMsgClientToGCClaimEventActionResponse` | 15021 |
| `k_EMsgClientToGCGetPeriodicResource` | 15100 |
| `k_EMsgClientToGCGetPeriodicResourceResponse` | 15101 |
| `k_EMsgGCToClientPeriodicResourceUpdated` | 15102 |

</details>

<details>
<summary><code>CMsgClientToGCGetEventPointsResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCGetEventPointsResponse`

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
<summary><code>CMsgClientToGCGetPeriodicResourceResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCGetPeriodicResourceResponse`

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
<summary><code>CMsgClientToGCDevGrantEventPointsResponse.EResponse</code> — values: 8</summary>

- Parent: `CMsgClientToGCDevGrantEventPointsResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNotAllowed` | 5 |
| `k_eInvalidEvent` | 6 |
| `k_eInvalidPoints` | 7 |

</details>

<details>
<summary><code>CMsgClientToGCDevReloadEventSchemaResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCDevReloadEventSchemaResponse`

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
<summary><code>CMsgClientToGCDevResetEventStateResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCDevResetEventStateResponse`

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
<summary><code>CMsgClientToGCDevGrantEventActionResponse.EResponse</code> — values: 10</summary>

- Parent: `CMsgClientToGCDevGrantEventActionResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNotAllowed` | 5 |
| `k_eInvalidEvent` | 6 |
| `k_eInvalidAccount` | 7 |
| `k_eGrantFailed` | 8 |
| `k_eNotGranted` | 9 |

</details>

<details>
<summary><code>CMsgClientToGCDevResetEventActionsResponse.EResponse</code> — values: 8</summary>

- Parent: `CMsgClientToGCDevResetEventActionsResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNotAllowed` | 5 |
| `k_eInvalidEvent` | 6 |
| `k_eInvalidAccount` | 7 |

</details>

<details>
<summary><code>CMsgClientToGCClaimEventActionResponse.EResponse</code> — values: 16</summary>

- Parent: `CMsgClientToGCClaimEventActionResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNotAllowed` | 5 |
| `k_eInvalidAction` | 6 |
| `k_eInvalidEvent` | 7 |
| `k_eEventNotActive` | 8 |
| `k_eEventNotOwned` | 9 |
| `k_eInsufficientLevel` | 10 |
| `k_eInsufficientPoints` | 11 |
| `k_eAlreadyClaimed` | 12 |
| `k_eInvalidScoreMode` | 13 |
| `k_eRequiresSubscription` | 14 |
| `k_eInvalidItem` | 15 |

</details>
