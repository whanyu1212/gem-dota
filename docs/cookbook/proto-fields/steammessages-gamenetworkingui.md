# steammessages_gamenetworkingui.proto

- Module: `steammessages_gamenetworkingui_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **2**
- Messages: **5** (top-level: 5)
- Enums: **0** (top-level: 0)

## Imports

- `steamnetworkingsockets_messages.proto`
- `steamdatagram_messages_sdr.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CGameNetworkingUI_GlobalState</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CGameNetworkingUI_ConnectionState</code> — fields: 27; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `connection_key` | `string` | `optional` | `` |  |
| 2 | `appid` | `uint32` | `optional` | `` |  |
| 3 | `connection_id_local` | `fixed32` | `optional` | `` |  |
| 4 | `identity_local` | `string` | `optional` | `` |  |
| 5 | `identity_remote` | `string` | `optional` | `` |  |
| 10 | `connection_state` | `uint32` | `optional` | `` |  |
| 12 | `start_time` | `uint32` | `optional` | `` |  |
| 13 | `close_time` | `uint32` | `optional` | `` |  |
| 14 | `close_reason` | `uint32` | `optional` | `` |  |
| 15 | `close_message` | `string` | `optional` | `` |  |
| 16 | `status_loc_token` | `string` | `optional` | `` |  |
| 20 | `transport_kind` | `uint32` | `optional` | `` |  |
| 21 | `sdrpopid_local` | `string` | `optional` | `` |  |
| 22 | `sdrpopid_remote` | `string` | `optional` | `` |  |
| 23 | `address_remote` | `string` | `optional` | `` |  |
| 24 | `p2p_routing` | `.CMsgSteamDatagramP2PRoutingSummary` | `optional` | `` |  |
| 25 | `ping_interior` | `uint32` | `optional` | `` |  |
| 26 | `ping_remote_front` | `uint32` | `optional` | `` |  |
| 27 | `ping_default_internet_route` | `uint32` | `optional` | `` |  |
| 30 | `e2e_quality_local` | `.CMsgSteamDatagramConnectionQuality` | `optional` | `` |  |
| 31 | `e2e_quality_remote` | `.CMsgSteamDatagramConnectionQuality` | `optional` | `` |  |
| 32 | `e2e_quality_remote_instantaneous_time` | `uint64` | `optional` | `` |  |
| 33 | `e2e_quality_remote_lifetime_time` | `uint64` | `optional` | `` |  |
| 40 | `front_quality_local` | `.CMsgSteamDatagramConnectionQuality` | `optional` | `` |  |
| 41 | `front_quality_remote` | `.CMsgSteamDatagramConnectionQuality` | `optional` | `` |  |
| 42 | `front_quality_remote_instantaneous_time` | `uint64` | `optional` | `` |  |
| 43 | `front_quality_remote_lifetime_time` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CGameNetworkingUI_Message</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `connection_state` | `.CGameNetworkingUI_ConnectionState` | `repeated` | `` |  |

</details>

<details>
<summary><code>CGameNetworkingUI_ConnectionSummary</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `transport_kind` | `uint32` | `optional` | `` |  |
| 2 | `sdrpop_local` | `string` | `optional` | `` |  |
| 3 | `sdrpop_remote` | `string` | `optional` | `` |  |
| 4 | `ping_ms` | `uint32` | `optional` | `` |  |
| 5 | `packet_loss` | `float` | `optional` | `` |  |
| 6 | `ping_default_internet_route` | `uint32` | `optional` | `` |  |
| 7 | `ip_was_shared` | `bool` | `optional` | `` |  |
| 8 | `connection_state` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CGameNetworkingUI_AppSummary</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `appid` | `uint32` | `optional` | `` |  |
| 10 | `ip_was_shared_with_friend` | `bool` | `optional` | `` |  |
| 11 | `ip_was_shared_with_nonfriend` | `bool` | `optional` | `` |  |
| 20 | `active_connections` | `uint32` | `optional` | `` |  |
| 30 | `main_cxn` | `.CGameNetworkingUI_ConnectionSummary` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

*(No enums in this proto file.)*
