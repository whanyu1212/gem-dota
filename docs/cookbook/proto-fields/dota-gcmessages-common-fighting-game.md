# dota_gcmessages_common_fighting_game.proto

- Module: `dota_gcmessages_common_fighting_game_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **4**
- Messages: **8** (top-level: 8)
- Enums: **2** (top-level: 0)

## Imports

- `steammessages.proto`
- `dota_shared_enums.proto`
- `dota_gcmessages_common.proto`
- `gcsdk_gcmessages.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgClientToGCFightingGameChallengeFriend</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `friend_account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCFightingGameChallengeFriendResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCFightingGameChallengeFriendResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCFightingGameCancelChallengeFriend</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `friend_account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCFightingGameAnswerChallenge</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `challenger_account_id` | `uint32` | `optional` | `` |  |
| 2 | `accept` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCFightingGameAnswerChallengeResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCFightingGameAnswerChallengeResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgGCToClientFightingGameChallenge</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `challenger_account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientFightingGameChallengeCanceled</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `challenger_account_id` | `uint32` | `optional` | `` |  |
| 2 | `responder_account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientFightingGameStartMatch</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `challenger_account_id` | `uint32` | `optional` | `` |  |
| 2 | `responder_account_id` | `uint32` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>CMsgClientToGCFightingGameChallengeFriendResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCFightingGameChallengeFriendResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidAccountID` | 5 |
| `k_eStillWaitingOnAnotherChallenge` | 6 |

</details>

<details>
<summary><code>CMsgClientToGCFightingGameAnswerChallengeResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCFightingGameAnswerChallengeResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidChallenge` | 5 |

</details>
