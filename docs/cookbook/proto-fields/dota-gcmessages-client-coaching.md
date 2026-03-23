# dota_gcmessages_client_coaching.proto

- Module: `dota_gcmessages_client_coaching_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **2**
- Messages: **35** (top-level: 35)
- Enums: **17** (top-level: 4)

## Imports

- `dota_shared_enums.proto`
- `dota_gcmessages_common_lobby.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgPlayerCoachMatch</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `match_outcome` | `.EMatchOutcome` | `optional` | `` | default = k_EMatchOutcome_Unknown |
| 3 | `coached_team` | `uint32` | `optional` | `` |  |
| 4 | `start_time` | `fixed32` | `optional` | `` |  |
| 5 | `duration` | `uint32` | `optional` | `` |  |
| 6 | `teammate_ratings` | `.ECoachTeammateRating` | `repeated` | `` |  |
| 7 | `coach_flags` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPrivateCoachingSessionMember</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `member_flags` | `uint32` | `optional` | `` |  |
| 3 | `member_session_rating` | `.ECoachTeammateRating` | `optional` | `` | default = k_ECoachTeammateRating_None |

</details>

<details>
<summary><code>CMsgPrivateCoachingSession</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `private_coaching_session_id` | `uint64` | `optional` | `` |  |
| 2 | `requested_timestamp` | `fixed32` | `optional` | `` |  |
| 3 | `requested_language` | `uint32` | `optional` | `` |  |
| 4 | `coaching_session_state` | `.EPrivateCoachingSessionState` | `optional` | `` | default = k_ePrivateCoachingSessionState_Invalid |
| 5 | `session_members` | `.CMsgPrivateCoachingSessionMember` | `repeated` | `` |  |
| 6 | `current_lobby_id` | `uint64` | `optional` | `` |  |
| 7 | `current_server_steam_id` | `uint64` | `optional` | `` |  |
| 8 | `accepted_timestamp` | `fixed32` | `optional` | `` |  |
| 9 | `completed_timestamp` | `fixed32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPrivateCoachingSessionStatus</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `requester_competitive_rank_tier` | `uint32` | `optional` | `` |  |
| 2 | `requester_games_played` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgAvailablePrivateCoachingSession</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `coaching_session` | `.CMsgPrivateCoachingSession` | `optional` | `` |  |
| 2 | `coaching_session_status` | `.CMsgPrivateCoachingSessionStatus` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgAvailablePrivateCoachingSessionList</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `available_coaching_sessions` | `.CMsgAvailablePrivateCoachingSession` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgAvailablePrivateCoachingSessionSummary</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `coaching_session_count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestPlayerCoachMatches</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestPlayerCoachMatchesResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCRequestPlayerCoachMatchesResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `coach_matches` | `.CMsgPlayerCoachMatch` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestPlayerCoachMatch</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestPlayerCoachMatchResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCRequestPlayerCoachMatchResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `coach_match` | `.CMsgPlayerCoachMatch` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCSubmitCoachTeammateRating</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `coach_account_id` | `uint32` | `optional` | `` |  |
| 3 | `rating` | `.ECoachTeammateRating` | `optional` | `` | default = k_ECoachTeammateRating_None |
| 4 | `reason` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCSubmitCoachTeammateRatingResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCSubmitCoachTeammateRatingResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgGCToClientCoachTeammateRatingsChanged</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `coach_match` | `.CMsgPlayerCoachMatch` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestPrivateCoachingSession</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `language` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestPrivateCoachingSessionResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `coaching_session` | `.CMsgPrivateCoachingSession` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCAcceptPrivateCoachingSession</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `coaching_session_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCAcceptPrivateCoachingSessionResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `coaching_session` | `.CMsgPrivateCoachingSession` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCLeavePrivateCoachingSession</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCLeavePrivateCoachingSessionResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCLeavePrivateCoachingSessionResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCGetCurrentPrivateCoachingSession</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCGetCurrentPrivateCoachingSessionResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCGetCurrentPrivateCoachingSessionResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `current_session` | `.CMsgPrivateCoachingSession` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientPrivateCoachingSessionUpdated</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `coaching_session` | `.CMsgPrivateCoachingSession` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCSubmitPrivateCoachingSessionRating</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `coaching_session_id` | `uint64` | `optional` | `` |  |
| 2 | `session_rating` | `.ECoachTeammateRating` | `optional` | `` | default = k_ECoachTeammateRating_None |

</details>

<details>
<summary><code>CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCGetAvailablePrivateCoachingSessions</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `language` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetAvailablePrivateCoachingSessionsResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCGetAvailablePrivateCoachingSessionsResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `available_sessions_list` | `.CMsgAvailablePrivateCoachingSessionList` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetAvailablePrivateCoachingSessionsSummary</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCGetAvailablePrivateCoachingSessionsSummaryResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCGetAvailablePrivateCoachingSessionsSummaryResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `coaching_session_summary` | `.CMsgAvailablePrivateCoachingSessionSummary` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCJoinPrivateCoachingSessionLobby</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCCoachFriend</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCoachFriendResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCCoachFriendResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCRespondToCoachFriendRequest</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `coach_account_id` | `uint32` | `optional` | `` |  |
| 2 | `response` | `.ELobbyMemberCoachRequestState` | `optional` | `` | default = k_eLobbyMemberCoachRequestState_None |

</details>

<details>
<summary><code>CMsgClientToGCRespondToCoachFriendRequestResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCRespondToCoachFriendRequestResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>ECoachTeammateRating</code> — values: 4</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_ECoachTeammateRating_None` | 0 |
| `k_ECoachTeammateRating_Positive` | 1 |
| `k_ECoachTeammateRating_Negative` | 2 |
| `k_ECoachTeammateRating_Abusive` | 3 |

</details>

<details>
<summary><code>EPrivateCoachingSessionState</code> — values: 6</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_ePrivateCoachingSessionState_Invalid` | 0 |
| `k_ePrivateCoachingSessionState_SearchingForCoach` | 1 |
| `k_ePrivateCoachingSessionState_CoachAssigned` | 2 |
| `k_ePrivateCoachingSessionState_Finished` | 3 |
| `k_ePrivateCoachingSessionState_Expired` | 4 |
| `k_ePrivateCoachingSessionState_Abandoned` | 5 |

</details>

<details>
<summary><code>EPrivateCoachingSessionMemberFlag</code> — values: 3</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EPrivateCoachingSessionMemberFlag_Requester` | 1 |
| `k_EPrivateCoachingSessionMemberFlag_Coach` | 2 |
| `k_EPrivateCoachingSessionMemberFlag_LeftSession` | 4 |

</details>

<details>
<summary><code>EPlayerCoachMatchFlag</code> — values: 2</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EPlayerCoachMatchFlag_EligibleForRewards` | 1 |
| `k_EPlayerCoachMatchFlag_PrivateCoach` | 2 |

</details>

<details>
<summary><code>CMsgClientToGCRequestPlayerCoachMatchesResponse.EResponse</code> — values: 4</summary>

- Parent: `CMsgClientToGCRequestPlayerCoachMatchesResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |

</details>

<details>
<summary><code>CMsgClientToGCRequestPlayerCoachMatchResponse.EResponse</code> — values: 4</summary>

- Parent: `CMsgClientToGCRequestPlayerCoachMatchResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |

</details>

<details>
<summary><code>CMsgClientToGCSubmitCoachTeammateRatingResponse.EResponse</code> — values: 12</summary>

- Parent: `CMsgClientToGCSubmitCoachTeammateRatingResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eInvalidInput` | 4 |
| `k_eAlreadySubmitted` | 5 |
| `k_eVotingFinished` | 6 |
| `k_ePlayerNotInMatch` | 7 |
| `k_eCoachNotInMatch` | 8 |
| `k_ePlayerNotOnCoachTeam` | 9 |
| `k_ePlayerInSamePartyAsCoach` | 10 |
| `k_eMatchNotEligible` | 11 |

</details>

<details>
<summary><code>CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse</code> — values: 14</summary>

- Parent: `CMsgClientToGCRequestPrivateCoachingSessionResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eAlreadyInSession` | 5 |
| `k_eBehaviorScoreTooLow` | 6 |
| `k_eInvalidLobbyType` | 7 |
| `k_eLowPriorityPlayer` | 8 |
| `k_eLowPriorityLobby` | 9 |
| `k_eLowPriorityParty` | 10 |
| `k_eTextChatBan` | 11 |
| `k_eVoiceChatBan` | 12 |
| `k_eMatchBan` | 13 |

</details>

<details>
<summary><code>CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse</code> — values: 22</summary>

- Parent: `CMsgClientToGCAcceptPrivateCoachingSessionResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eUnknownSession` | 5 |
| `k_eAlreadyHasCoach` | 6 |
| `k_eAlreadyHasSession` | 7 |
| `k_eInvalidUser` | 8 |
| `k_eAlreadyFinished` | 9 |
| `k_eInvalidLobbyType` | 10 |
| `k_eAlreadyInLobby` | 11 |
| `k_eLobbyIsLan` | 12 |
| `k_eLobbyIsLeague` | 13 |
| `k_eInvalidLobbyState` | 14 |
| `k_eRequesterIsNotPlayer` | 15 |
| `k_eTooManyCoaches` | 16 |
| `k_eCoachWasPlayer` | 17 |
| `k_eCoachBehaviorScoreTooLow` | 18 |
| `k_eCoachRankNotCalibrated` | 19 |
| `k_eCoachRankNotEligible` | 20 |
| `k_eCoachRankTooLow` | 21 |

</details>

<details>
<summary><code>CMsgClientToGCLeavePrivateCoachingSessionResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCLeavePrivateCoachingSessionResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNoSession` | 5 |
| `k_eAlreadyLeft` | 6 |

</details>

<details>
<summary><code>CMsgClientToGCGetCurrentPrivateCoachingSessionResponse.EResponse</code> — values: 5</summary>

- Parent: `CMsgClientToGCGetCurrentPrivateCoachingSessionResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |

</details>

<details>
<summary><code>CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse.EResponse</code> — values: 12</summary>

- Parent: `CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eUnknownSession` | 5 |
| `k_eNotMember` | 6 |
| `k_eAlreadySubmitted` | 7 |
| `k_eSessionActive` | 8 |
| `k_eSessionTooShort` | 9 |
| `k_eNoCoach` | 10 |
| `k_eInvalidRating` | 11 |

</details>

<details>
<summary><code>CMsgClientToGCGetAvailablePrivateCoachingSessionsResponse.EResponse</code> — values: 5</summary>

- Parent: `CMsgClientToGCGetAvailablePrivateCoachingSessionsResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |

</details>

<details>
<summary><code>CMsgClientToGCGetAvailablePrivateCoachingSessionsSummaryResponse.EResponse</code> — values: 5</summary>

- Parent: `CMsgClientToGCGetAvailablePrivateCoachingSessionsSummaryResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |

</details>

<details>
<summary><code>CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse</code> — values: 20</summary>

- Parent: `CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNoSession` | 5 |
| `k_eSessionFinished` | 6 |
| `k_eAlreadyLeft` | 7 |
| `k_eNotACoach` | 8 |
| `k_eNoLobby` | 9 |
| `k_eCoachInThisLobby` | 10 |
| `k_eCoachInALobby` | 11 |
| `k_eLobbyIsLan` | 12 |
| `k_eLobbyIsLeague` | 13 |
| `k_eInvalidLobbyType` | 14 |
| `k_eInvalidLobbyState` | 15 |
| `k_eRequesterIsNotPlayer` | 16 |
| `k_eTooManyCoaches` | 17 |
| `k_eCoachWasPlayer` | 18 |
| `k_eJoinFailed` | 19 |

</details>

<details>
<summary><code>CMsgClientToGCCoachFriendResponse.EResponse</code> — values: 20</summary>

- Parent: `CMsgClientToGCCoachFriendResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eCoachNotSubscriber` | 5 |
| `k_eLobbyNotFound` | 6 |
| `k_eFriendsOnBothSides` | 7 |
| `k_eNotFriends` | 8 |
| `k_eCoachInThisLobby` | 9 |
| `k_eCoachInALobby` | 10 |
| `k_eLobbyIsLan` | 11 |
| `k_eInvalidLobbyType` | 12 |
| `k_eInvalidLobbyState` | 13 |
| `k_eFriendIsNotAPlayer` | 14 |
| `k_eTooManyCoaches` | 15 |
| `k_eCoachSwitchedTeams` | 16 |
| `k_eLobbyIsLeague` | 17 |
| `k_eCoachWasPlayer` | 18 |
| `k_eRequestRejected` | 19 |

</details>

<details>
<summary><code>CMsgClientToGCRespondToCoachFriendRequestResponse.EResponse</code> — values: 13</summary>

- Parent: `CMsgClientToGCRespondToCoachFriendRequestResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eLobbyNotFound` | 5 |
| `k_eInvalidLobbyState` | 6 |
| `k_eCoachNotInLobby` | 7 |
| `k_ePlayerInvalidTeam` | 8 |
| `k_eCoachInvalidTeam` | 9 |
| `k_eNoRequest` | 10 |
| `k_eInvalidResponse` | 11 |
| `k_eAlreadyResponded` | 12 |

</details>
