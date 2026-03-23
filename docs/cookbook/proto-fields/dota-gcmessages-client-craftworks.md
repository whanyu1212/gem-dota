# dota_gcmessages_client_craftworks.proto

- Module: `dota_gcmessages_client_craftworks_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **10**
- Messages: **8** (top-level: 8)
- Enums: **4** (top-level: 0)

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
- `dota_gcmessages_common_craftworks.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgCraftworksUserData</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `component_inventory` | `.CMsgCraftworksComponents` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCraftworksGetUserData</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `craftworks_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCraftworksGetUserDataResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCCraftworksGetUserDataResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `user_data` | `.CMsgCraftworksUserData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientCraftworksUserDataUpdated</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `craftworks_id` | `uint32` | `optional` | `` |  |
| 2 | `user_data` | `.CMsgCraftworksUserData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCraftworksCraftRecipe</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `craftworks_id` | `uint32` | `optional` | `` |  |
| 2 | `recipe_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCraftworksCraftRecipeResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCCraftworksCraftRecipeResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `claim_response` | `.CMsgDOTAClaimEventActionResponse` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCraftworksDevModifyComponents</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `craftworks_id` | `uint32` | `optional` | `` |  |
| 2 | `components` | `.CMsgCraftworksComponents` | `optional` | `` |  |
| 3 | `operation` | `.CMsgClientToGCCraftworksDevModifyComponents.EOperation` | `optional` | `` | default = k_eAddComponents |

</details>

<details>
<summary><code>CMsgClientToGCCraftworksDevModifyComponentsResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCCraftworksDevModifyComponentsResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>CMsgClientToGCCraftworksGetUserDataResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCCraftworksGetUserDataResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidCraftworks` | 5 |
| `k_eExpiredCraftworks` | 6 |

</details>

<details>
<summary><code>CMsgClientToGCCraftworksCraftRecipeResponse.EResponse</code> — values: 11</summary>

- Parent: `CMsgClientToGCCraftworksCraftRecipeResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidCraftworks` | 5 |
| `k_eExpiredCraftworks` | 6 |
| `k_eNotEnoughComponents` | 7 |
| `k_eInvalidRecipe` | 8 |
| `k_eRecipeTierLocked` | 9 |
| `k_eAlreadyCraftedMaxAmount` | 10 |

</details>

<details>
<summary><code>CMsgClientToGCCraftworksDevModifyComponents.EOperation</code> — values: 2</summary>

- Parent: `CMsgClientToGCCraftworksDevModifyComponents`

| Name | Number |
|---|---:|
| `k_eAddComponents` | 1 |
| `k_eSubtractComponents` | 2 |

</details>

<details>
<summary><code>CMsgClientToGCCraftworksDevModifyComponentsResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCCraftworksDevModifyComponentsResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidCraftworks` | 5 |
| `k_eNotAllowed` | 6 |

</details>
