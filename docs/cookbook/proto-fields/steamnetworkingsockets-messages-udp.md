# steamnetworkingsockets_messages_udp.proto

- Module: `steamnetworkingsockets_messages_udp_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **2**
- Messages: **7** (top-level: 7)
- Enums: **2** (top-level: 1)

## Imports

- `steamnetworkingsockets_messages_certs.proto`
- `steamnetworkingsockets_messages.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgSteamSockets_UDP_ChallengeRequest</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `connection_id` | `fixed32` | `optional` | `` |  |
| 3 | `my_timestamp` | `fixed64` | `optional` | `` |  |
| 4 | `protocol_version` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamSockets_UDP_ChallengeReply</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `connection_id` | `fixed32` | `optional` | `` |  |
| 2 | `challenge` | `fixed64` | `optional` | `` |  |
| 3 | `your_timestamp` | `fixed64` | `optional` | `` |  |
| 4 | `protocol_version` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamSockets_UDP_ConnectRequest</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `client_connection_id` | `fixed32` | `optional` | `` |  |
| 2 | `challenge` | `fixed64` | `optional` | `` |  |
| 3 | `legacy_client_steam_id` | `fixed64` | `optional` | `` |  |
| 4 | `cert` | `.CMsgSteamDatagramCertificateSigned` | `optional` | `` |  |
| 5 | `my_timestamp` | `fixed64` | `optional` | `` |  |
| 6 | `ping_est_ms` | `uint32` | `optional` | `` |  |
| 7 | `crypt` | `.CMsgSteamDatagramSessionCryptInfoSigned` | `optional` | `` |  |
| 8 | `legacy_protocol_version` | `uint32` | `optional` | `` |  |
| 9 | `legacy_identity_binary` | `.CMsgSteamNetworkingIdentityLegacyBinary` | `optional` | `` |  |
| 10 | `identity_string` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamSockets_UDP_ConnectOK</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `client_connection_id` | `fixed32` | `optional` | `` |  |
| 2 | `legacy_server_steam_id` | `fixed64` | `optional` | `` |  |
| 3 | `your_timestamp` | `fixed64` | `optional` | `` |  |
| 4 | `delay_time_usec` | `uint32` | `optional` | `` |  |
| 5 | `server_connection_id` | `fixed32` | `optional` | `` |  |
| 7 | `crypt` | `.CMsgSteamDatagramSessionCryptInfoSigned` | `optional` | `` |  |
| 8 | `cert` | `.CMsgSteamDatagramCertificateSigned` | `optional` | `` |  |
| 10 | `legacy_identity_binary` | `.CMsgSteamNetworkingIdentityLegacyBinary` | `optional` | `` |  |
| 11 | `identity_string` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamSockets_UDP_ConnectionClosed</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `debug` | `string` | `optional` | `` |  |
| 3 | `reason_code` | `uint32` | `optional` | `` |  |
| 4 | `to_connection_id` | `fixed32` | `optional` | `` |  |
| 5 | `from_connection_id` | `fixed32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamSockets_UDP_NoConnection</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `from_connection_id` | `fixed32` | `optional` | `` |  |
| 3 | `to_connection_id` | `fixed32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamSockets_UDP_Stats</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `stats` | `.CMsgSteamDatagramConnectionQuality` | `optional` | `` |  |
| 3 | `flags` | `uint32` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>ESteamNetworkingUDPMsgID</code> — values: 6</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_ESteamNetworkingUDPMsg_ChallengeRequest` | 32 |
| `k_ESteamNetworkingUDPMsg_ChallengeReply` | 33 |
| `k_ESteamNetworkingUDPMsg_ConnectRequest` | 34 |
| `k_ESteamNetworkingUDPMsg_ConnectOK` | 35 |
| `k_ESteamNetworkingUDPMsg_ConnectionClosed` | 36 |
| `k_ESteamNetworkingUDPMsg_NoConnection` | 37 |

</details>

<details>
<summary><code>CMsgSteamSockets_UDP_Stats.Flags</code> — values: 3</summary>

- Parent: `CMsgSteamSockets_UDP_Stats`

| Name | Number |
|---|---:|
| `ACK_REQUEST_E2E` | 2 |
| `ACK_REQUEST_IMMEDIATE` | 4 |
| `NOT_PRIMARY_TRANSPORT_E2E` | 16 |

</details>
