# dota_broadcastmessages.proto

- Module: `dota_broadcastmessages_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **0**
- Messages: **4** (top-level: 3)
- Enums: **1** (top-level: 1)

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CDOTABroadcastMsg</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `type` | `.EDotaBroadcastMessages` | `required` | `` | default = DOTA_BM_LANLobbyRequest |
| 2 | `msg` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTABroadcastMsg_LANLobbyRequest</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CDOTABroadcastMsg_LANLobbyReply</code> — fields: 9; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `id` | `uint64` | `optional` | `` |  |
| 2 | `tournament_id` | `uint32` | `optional` | `` |  |
| 3 | `tournament_game_id` | `uint32` | `optional` | `` |  |
| 4 | `members` | `.CDOTABroadcastMsg_LANLobbyReply.CLobbyMember` | `repeated` | `` |  |
| 5 | `requires_pass_key` | `bool` | `optional` | `` |  |
| 6 | `leader_account_id` | `uint32` | `optional` | `` |  |
| 7 | `game_mode` | `uint32` | `optional` | `` |  |
| 8 | `name` | `string` | `optional` | `` |  |
| 9 | `players` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTABroadcastMsg_LANLobbyReply.CLobbyMember</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTABroadcastMsg_LANLobbyReply`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `player_name` | `string` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>EDotaBroadcastMessages</code> — values: 2</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `DOTA_BM_LANLobbyRequest` | 1 |
| `DOTA_BM_LANLobbyReply` | 2 |

</details>
