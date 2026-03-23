# dota_gcmessages_client_bingo.proto

- Module: `dota_gcmessages_client_bingo_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **9**
- Messages: **25** (top-level: 23)
- Enums: **10** (top-level: 1)

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
<summary><code>CMsgBingoSquare</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `stat_id` | `uint32` | `optional` | `` |  |
| 2 | `stat_threshold` | `int32` | `optional` | `` |  |
| 3 | `upgrade_level` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgBingoTokens</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `token_count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgBingoCard</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `squares` | `.CMsgBingoSquare` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgBingoUserData</code> — fields: 2; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `bingo_cards` | `.CMsgBingoUserData.BingoCardsEntry` | `repeated` | `` |  |
| 2 | `bingo_tokens` | `.CMsgBingoUserData.BingoTokensEntry` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgBingoUserData.BingoCardsEntry</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgBingoUserData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `key` | `uint32` | `optional` | `` |  |
| 2 | `value` | `.CMsgBingoCard` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgBingoUserData.BingoTokensEntry</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgBingoUserData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `key` | `uint32` | `optional` | `` |  |
| 2 | `value` | `.CMsgBingoTokens` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCBingoGetUserData</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCBingoGetUserDataResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCBingoGetUserDataResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `user_data` | `.CMsgBingoUserData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgBingoIndividualStatData</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `stat_id` | `uint32` | `optional` | `` |  |
| 2 | `stat_value` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgBingoStatsData</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `stats_data` | `.CMsgBingoIndividualStatData` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCBingoGetStatsData</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_id` | `uint32` | `optional` | `` |  |
| 2 | `league_phase` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCBingoGetStatsDataResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCBingoGetStatsDataResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `stats_data` | `.CMsgBingoStatsData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBingoUserDataUpdated</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_id` | `uint32` | `optional` | `` |  |
| 2 | `user_data` | `.CMsgBingoUserData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCBingoClaimRow</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_id` | `uint32` | `optional` | `` |  |
| 2 | `league_phase` | `uint32` | `optional` | `` |  |
| 3 | `row_index` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCBingoClaimRowResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCBingoClaimRowResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCBingoShuffleCard</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_id` | `uint32` | `optional` | `` |  |
| 2 | `league_phase` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCBingoShuffleCardResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCBingoShuffleCardResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCBingoModifySquare</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_id` | `uint32` | `optional` | `` |  |
| 2 | `league_phase` | `uint32` | `optional` | `` |  |
| 3 | `square_index` | `uint32` | `optional` | `` |  |
| 4 | `action` | `.CMsgClientToGCBingoModifySquare.EModifyAction` | `optional` | `` | default = k_eRerollStat |

</details>

<details>
<summary><code>CMsgClientToGCBingoModifySquareResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCBingoModifySquareResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCBingoDevRerollCard</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_id` | `uint32` | `optional` | `` |  |
| 2 | `league_phase` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCBingoDevRerollCardResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCBingoDevRerollCardResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCBingoDevAddTokens</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_id` | `uint32` | `optional` | `` |  |
| 2 | `league_phase` | `uint32` | `optional` | `` |  |
| 3 | `token_count` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCBingoDevAddTokensResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCBingoDevAddTokensResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCBingoDevClearInventory</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCBingoDevClearInventoryResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCBingoDevClearInventoryResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>EBingoAuditAction</code> — values: 11</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eBingoAuditAction_Invalid` | 0 |
| `k_eBingoAuditAction_DevModifyTokens` | 1 |
| `k_eBingoAuditAction_DevClearInventory` | 2 |
| `k_eBingoAuditAction_DevRerollCard` | 3 |
| `k_eBingoAuditAction_ShuffleCard` | 4 |
| `k_eBingoAuditAction_RerollSquare` | 5 |
| `k_eBingoAuditAction_UpgradeSquare` | 6 |
| `k_eBingoAuditAction_ClaimRow` | 7 |
| `k_eBingoAuditAction_EventActionTokenGrant` | 8 |
| `k_eBingoAuditAction_SupportGrantTokens` | 9 |
| `k_eBingoAuditAction_SupportStatThresholdFixup` | 10 |

</details>

<details>
<summary><code>CMsgClientToGCBingoGetUserDataResponse.EResponse</code> — values: 5</summary>

- Parent: `CMsgClientToGCBingoGetUserDataResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |

</details>

<details>
<summary><code>CMsgClientToGCBingoGetStatsDataResponse.EResponse</code> — values: 5</summary>

- Parent: `CMsgClientToGCBingoGetStatsDataResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |

</details>

<details>
<summary><code>CMsgClientToGCBingoClaimRowResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCBingoClaimRowResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidRow` | 5 |
| `k_eExpiredCard` | 6 |

</details>

<details>
<summary><code>CMsgClientToGCBingoShuffleCardResponse.EResponse</code> — values: 8</summary>

- Parent: `CMsgClientToGCBingoShuffleCardResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eExpiredCard` | 6 |
| `k_eNotAllowed` | 7 |
| `k_eInsufficientTokens` | 8 |

</details>

<details>
<summary><code>CMsgClientToGCBingoModifySquare.EModifyAction</code> — values: 2</summary>

- Parent: `CMsgClientToGCBingoModifySquare`

| Name | Number |
|---|---:|
| `k_eRerollStat` | 0 |
| `k_eUpgrade` | 1 |

</details>

<details>
<summary><code>CMsgClientToGCBingoModifySquareResponse.EResponse</code> — values: 11</summary>

- Parent: `CMsgClientToGCBingoModifySquareResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eExpiredCard` | 6 |
| `k_eNotAllowed` | 7 |
| `k_eInsufficientTokens` | 8 |
| `k_eCantUpgrade` | 9 |
| `k_eCantReroll` | 10 |
| `k_eInvalidSquare` | 11 |

</details>

<details>
<summary><code>CMsgClientToGCBingoDevRerollCardResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCBingoDevRerollCardResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eExpiredCard` | 6 |
| `k_eNotAllowed` | 7 |

</details>

<details>
<summary><code>CMsgClientToGCBingoDevAddTokensResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCBingoDevAddTokensResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eExpiredCard` | 6 |
| `k_eNotAllowed` | 7 |

</details>

<details>
<summary><code>CMsgClientToGCBingoDevClearInventoryResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCBingoDevClearInventoryResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eExpiredCard` | 6 |
| `k_eNotAllowed` | 7 |

</details>
