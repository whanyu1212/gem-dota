# dota_gcmessages_client_guild_events.proto

- Module: `dota_gcmessages_client_guild_events_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **1**
- Messages: **22** (top-level: 22)
- Enums: **7** (top-level: 1)

## Imports

- `dota_shared_enums.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgGuildContract</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `contract_id` | `uint64` | `optional` | `` |  |
| 2 | `challenge_instance_id` | `uint32` | `optional` | `` |  |
| 3 | `challenge_parameter` | `uint32` | `optional` | `` |  |
| 4 | `challenge_timestamp` | `uint32` | `optional` | `` |  |
| 5 | `assigned_account_id` | `uint32` | `optional` | `` |  |
| 6 | `contract_flags` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGuildContractSlot</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `contract` | `.CMsgGuildContract` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgAccountGuildEventData</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_points` | `uint32` | `optional` | `` |  |
| 2 | `contracts_refreshed_timestamp` | `uint32` | `optional` | `` |  |
| 3 | `contract_slots` | `.CMsgGuildContractSlot` | `repeated` | `` |  |
| 4 | `completed_challenge_count` | `uint32` | `optional` | `` |  |
| 5 | `challenges_refresh_timestamp` | `uint32` | `optional` | `` |  |
| 6 | `guild_weekly_percentile` | `uint32` | `optional` | `` |  |
| 7 | `guild_weekly_last_timestamp` | `uint32` | `optional` | `` |  |
| 8 | `last_weekly_claim_time` | `uint32` | `optional` | `` |  |
| 9 | `guild_current_percentile` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGuildActiveContracts</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `contracts_refreshed_timestamp` | `uint32` | `optional` | `` |  |
| 2 | `contracts` | `.CMsgGuildContract` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGuildChallenge</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `challenge_instance_id` | `uint32` | `optional` | `` |  |
| 2 | `challenge_parameter` | `uint32` | `optional` | `` |  |
| 3 | `challenge_timestamp` | `uint32` | `optional` | `` |  |
| 4 | `challenge_progress` | `uint32` | `optional` | `` |  |
| 5 | `challenge_flags` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGuildEventMember</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `guild_points_earned` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestAccountGuildEventData</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |

</details>

<details>
<summary><code>CMsgClientToGCRequestAccountGuildEventDataResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCRequestAccountGuildEventDataResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 3 | `event_data` | `.CMsgAccountGuildEventData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientAccountGuildEventDataUpdated</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 3 | `update_flags` | `uint32` | `optional` | `` |  |
| 4 | `guild_event_data` | `.CMsgAccountGuildEventData` | `optional` | `` |  |
| 5 | `contracts_updated` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestActiveGuildContracts</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |

</details>

<details>
<summary><code>CMsgClientToGCRequestActiveGuildContractsResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCRequestActiveGuildContractsResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `active_contracts` | `.CMsgGuildActiveContracts` | `optional` | `` |  |
| 3 | `active_challenges` | `.CMsgGuildChallenge` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientActiveGuildContractsUpdated</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |

</details>

<details>
<summary><code>CMsgClientToGCSelectGuildContract</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 3 | `contract_id` | `uint64` | `optional` | `` |  |
| 4 | `contract_slot` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCSelectGuildContractResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCSelectGuildContractResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCRequestActiveGuildChallenge</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |

</details>

<details>
<summary><code>CMsgClientToGCRequestActiveGuildChallengeResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCRequestActiveGuildChallengeResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `active_challenge` | `.CMsgGuildChallenge` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientActiveGuildChallengeUpdated</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 3 | `active_challenge` | `.CMsgGuildChallenge` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestGuildEventMembers</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |

</details>

<details>
<summary><code>CMsgClientToGCRequestGuildEventMembersResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCRequestGuildEventMembersResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `members` | `.CMsgGuildEventMember` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGuildLeaderboardCombinedResponse</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 2 | `region` | `uint32` | `optional` | `` |  |
| 3 | `last_updated` | `uint32` | `optional` | `` |  |
| 4 | `guild_id` | `uint32` | `repeated` | `` | packed = true |
| 5 | `rank` | `uint32` | `repeated` | `` | packed = true |
| 6 | `current_percentile` | `uint32` | `repeated` | `` | packed = true |
| 7 | `weekly_percentile` | `uint32` | `repeated` | `` | packed = true |
| 8 | `points` | `uint32` | `repeated` | `` | packed = true |

</details>

<details>
<summary><code>CMsgClientToGCClaimLeaderboardRewards</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |

</details>

<details>
<summary><code>CMsgClientToGCClaimLeaderboardRewardsResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCClaimLeaderboardRewardsResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `event_points` | `uint32` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>EGuildEventAuditAction</code> — values: 9</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EGuildEventAuditAction_Invalid` | 0 |
| `k_EGuildEventAuditAction_DevGrant` | 1 |
| `k_EGuildEventAuditAction_CompleteContract` | 2 |
| `k_EGuildEventAuditAction_CompleteChallenge` | 3 |
| `k_EGuildEventAuditAction_CompleteMatch_Winner` | 4 |
| `k_EGuildEventAuditAction_ChallengeProgress` | 5 |
| `k_EGuildEventAuditAction_CompleteMatch_Loser` | 6 |
| `k_EGuildEventAuditAction_WeeklyLeaderboard` | 7 |
| `k_EGuildEventAuditAction_ManualGrant` | 8 |

</details>

<details>
<summary><code>CMsgClientToGCRequestAccountGuildEventDataResponse.EResponse</code> — values: 9</summary>

- Parent: `CMsgClientToGCRequestAccountGuildEventDataResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidEvent` | 5 |
| `k_eInvalidGuild` | 6 |
| `k_eNotMember` | 7 |
| `k_eInvalidGuildEvent` | 8 |

</details>

<details>
<summary><code>CMsgClientToGCRequestActiveGuildContractsResponse.EResponse</code> — values: 9</summary>

- Parent: `CMsgClientToGCRequestActiveGuildContractsResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidEvent` | 5 |
| `k_eInvalidGuild` | 6 |
| `k_eNotMember` | 7 |
| `k_eInvalidGuildEvent` | 8 |

</details>

<details>
<summary><code>CMsgClientToGCSelectGuildContractResponse.EResponse</code> — values: 17</summary>

- Parent: `CMsgClientToGCSelectGuildContractResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidEvent` | 5 |
| `k_eInvalidGuild` | 6 |
| `k_eNotMember` | 7 |
| `k_eInvalidGuildEvent` | 8 |
| `k_eInvalidContractID` | 9 |
| `k_eAlreadyAssigned` | 10 |
| `k_eInvalidContractSlot` | 11 |
| `k_eContractSlotLockedGuild` | 12 |
| `k_eContractSlotCooldown` | 13 |
| `k_eContractDuplicate` | 14 |
| `k_eContractSlotTimeError` | 15 |
| `k_eContractSlotLockedDotaPlus` | 16 |

</details>

<details>
<summary><code>CMsgClientToGCRequestActiveGuildChallengeResponse.EResponse</code> — values: 9</summary>

- Parent: `CMsgClientToGCRequestActiveGuildChallengeResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidEvent` | 5 |
| `k_eInvalidGuild` | 6 |
| `k_eNotMember` | 7 |
| `k_eInvalidGuildEvent` | 8 |

</details>

<details>
<summary><code>CMsgClientToGCRequestGuildEventMembersResponse.EResponse</code> — values: 9</summary>

- Parent: `CMsgClientToGCRequestGuildEventMembersResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidEvent` | 5 |
| `k_eInvalidGuild` | 6 |
| `k_eNotMember` | 7 |
| `k_eInvalidGuildEvent` | 8 |

</details>

<details>
<summary><code>CMsgClientToGCClaimLeaderboardRewardsResponse.EResponse</code> — values: 11</summary>

- Parent: `CMsgClientToGCClaimLeaderboardRewardsResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidEvent` | 5 |
| `k_eInvalidGuild` | 6 |
| `k_eNotMember` | 7 |
| `k_eInvalidGuildEvent` | 8 |
| `k_eDoesNotQualify` | 9 |
| `k_eAlreadyClaimed` | 10 |

</details>
