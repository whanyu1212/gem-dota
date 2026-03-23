# steamdatagram_messages_sdr.proto

- Module: `steamdatagram_messages_sdr_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **2**
- Messages: **42** (top-level: 33)
- Enums: **10** (top-level: 1)

## Imports

- `steamnetworkingsockets_messages_certs.proto`
- `steamnetworkingsockets_messages.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgSteamNetworkingIPAddress</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `v4` | `fixed32` | `optional` | `` |  |
| 2 | `v6` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramSignedMessageGeneric</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `cert` | `.CMsgSteamDatagramCertificateSigned` | `optional` | `` |  |
| 2 | `signed_data` | `bytes` | `optional` | `` |  |
| 3 | `signature` | `bytes` | `optional` | `` |  |
| 1023 | `dummy_pad` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramRouterPingReply</code> — fields: 21; oneofs: 0; nested messages: 2; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `client_timestamp` | `fixed32` | `optional` | `` |  |
| 2 | `latency_datacenter_ids` | `fixed32` | `repeated` | `` | packed = true |
| 3 | `latency_ping_ms` | `uint32` | `repeated` | `` | packed = true |
| 4 | `your_public_ip` | `fixed32` | `optional` | `` |  |
| 5 | `server_time` | `fixed32` | `optional` | `` |  |
| 6 | `challenge` | `fixed64` | `optional` | `` |  |
| 7 | `seconds_until_shutdown` | `uint32` | `optional` | `` |  |
| 8 | `client_cookie` | `fixed32` | `optional` | `` |  |
| 9 | `scoring_penalty_relay_cluster` | `uint32` | `optional` | `` |  |
| 10 | `route_exceptions` | `.CMsgSteamDatagramRouterPingReply.RouteException` | `repeated` | `` |  |
| 11 | `your_public_port` | `fixed32` | `optional` | `` |  |
| 12 | `flags` | `uint32` | `optional` | `` |  |
| 13 | `alt_addresses` | `.CMsgSteamDatagramRouterPingReply.AltAddress` | `repeated` | `` |  |
| 14 | `latency_datacenter_ids_p2p` | `fixed32` | `repeated` | `` | packed = true |
| 15 | `latency_ping_ms_p2p` | `uint32` | `repeated` | `` | packed = true |
| 16 | `recv_tos` | `uint32` | `optional` | `` |  |
| 17 | `echo_sent_tos` | `uint32` | `optional` | `` |  |
| 18 | `sent_tos` | `uint32` | `optional` | `` |  |
| 19 | `echo_request_reply_tos` | `uint32` | `optional` | `` |  |
| 99 | `dummy_pad` | `bytes` | `optional` | `` |  |
| 100 | `dummy_varint` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramRouterPingReply.RouteException</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamDatagramRouterPingReply`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `data_center_id` | `fixed32` | `optional` | `` |  |
| 2 | `flags` | `uint32` | `optional` | `` |  |
| 3 | `penalty` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramRouterPingReply.AltAddress</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: `CMsgSteamDatagramRouterPingReply`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ipv4` | `fixed32` | `optional` | `` |  |
| 2 | `port` | `uint32` | `optional` | `` |  |
| 3 | `penalty` | `uint32` | `optional` | `` |  |
| 4 | `protocol` | `.CMsgSteamDatagramRouterPingReply.AltAddress.Protocol` | `optional` | `` | default = DefaultProtocol |
| 5 | `id` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramGameserverPingRequestBody</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `relay_popid` | `fixed32` | `optional` | `` |  |
| 2 | `your_public_ip` | `.CMsgSteamNetworkingIPAddress` | `optional` | `` |  |
| 3 | `your_public_port` | `uint32` | `optional` | `` |  |
| 4 | `relay_unix_time` | `uint64` | `optional` | `` |  |
| 5 | `routing_secret` | `fixed64` | `optional` | `` |  |
| 6 | `my_ips` | `.CMsgSteamNetworkingIPAddress` | `repeated` | `` |  |
| 8 | `echo` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramGameserverPingRequestEnvelope</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `legacy_your_public_ip` | `fixed32` | `optional` | `` |  |
| 2 | `legacy_relay_unix_time` | `fixed32` | `optional` | `` |  |
| 3 | `legacy_challenge` | `fixed64` | `optional` | `` |  |
| 4 | `legacy_router_timestamp` | `fixed32` | `optional` | `` |  |
| 5 | `legacy_your_public_port` | `fixed32` | `optional` | `` |  |
| 6 | `cert` | `.CMsgSteamDatagramCertificateSigned` | `optional` | `` |  |
| 7 | `signed_data` | `bytes` | `optional` | `` |  |
| 8 | `signature` | `bytes` | `optional` | `` |  |
| 1023 | `dummy_pad` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramGameserverPingReplyData</code> — fields: 11; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `echo_relay_unix_time` | `fixed32` | `optional` | `` |  |
| 3 | `legacy_challenge` | `fixed64` | `optional` | `` |  |
| 4 | `legacy_router_timestamp` | `fixed32` | `optional` | `` |  |
| 5 | `data_center_id` | `fixed32` | `optional` | `` |  |
| 6 | `appid` | `uint32` | `optional` | `` |  |
| 7 | `protocol_version` | `uint32` | `optional` | `` |  |
| 8 | `echo` | `bytes` | `optional` | `` |  |
| 9 | `build` | `string` | `optional` | `` |  |
| 10 | `network_config_version` | `uint64` | `optional` | `` |  |
| 11 | `my_unix_time` | `fixed32` | `optional` | `` |  |
| 12 | `routing_blob` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramNoSessionRelayToClient</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `your_public_ip` | `fixed32` | `optional` | `` |  |
| 3 | `server_time` | `fixed32` | `optional` | `` |  |
| 4 | `challenge` | `fixed64` | `optional` | `` |  |
| 5 | `seconds_until_shutdown` | `uint32` | `optional` | `` |  |
| 6 | `your_public_port` | `fixed32` | `optional` | `` |  |
| 7 | `connection_id` | `fixed32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramNoSessionRelayToPeer</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `legacy_relay_session_id` | `uint32` | `optional` | `` |  |
| 2 | `from_relay_session_id` | `fixed32` | `optional` | `` |  |
| 7 | `from_connection_id` | `fixed32` | `optional` | `` |  |
| 99 | `kludge_pad` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTOSTreatment</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `l4s_detect` | `string` | `optional` | `` |  |
| 2 | `up_ecn1` | `string` | `optional` | `` |  |
| 3 | `down_dscp45` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramClientPingSampleRequest</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `connection_id` | `fixed32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramClientPingSampleReply</code> — fields: 5; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `connection_id` | `fixed32` | `optional` | `` |  |
| 2 | `pops` | `.CMsgSteamDatagramClientPingSampleReply.POP` | `repeated` | `` |  |
| 3 | `legacy_data_centers` | `.CMsgSteamDatagramClientPingSampleReply.LegacyDataCenter` | `repeated` | `` |  |
| 5 | `relay_override_active` | `bool` | `optional` | `` |  |
| 6 | `tos` | `.CMsgTOSTreatment` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramClientPingSampleReply.POP</code> — fields: 16; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: `CMsgSteamDatagramClientPingSampleReply`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `pop_id` | `fixed32` | `optional` | `` |  |
| 2 | `default_front_ping_ms` | `uint32` | `optional` | `` |  |
| 3 | `default_e2e_ping_ms` | `uint32` | `optional` | `` |  |
| 4 | `cluster_penalty` | `uint32` | `optional` | `` |  |
| 5 | `default_e2e_score` | `uint32` | `optional` | `` |  |
| 6 | `p2p_via_peer_relay_pop_id` | `fixed32` | `optional` | `` |  |
| 7 | `alt_addresses` | `.CMsgSteamDatagramClientPingSampleReply.POP.AltAddress` | `repeated` | `` |  |
| 9 | `best_dc_ping_ms` | `uint32` | `optional` | `` |  |
| 10 | `best_dc_score` | `uint32` | `optional` | `` |  |
| 11 | `best_dc_via_relay_pop_id` | `fixed32` | `optional` | `` |  |
| 12 | `default_dc_ping_ms` | `uint32` | `optional` | `` |  |
| 13 | `default_dc_score` | `uint32` | `optional` | `` |  |
| 14 | `default_dc_via_relay_pop_id` | `fixed32` | `optional` | `` |  |
| 15 | `test_dc_ping_ms` | `uint32` | `optional` | `` |  |
| 16 | `test_dc_score` | `uint32` | `optional` | `` |  |
| 17 | `test_dc_via_relay_pop_id` | `fixed32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramClientPingSampleReply.POP.AltAddress</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamDatagramClientPingSampleReply.POP`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `id` | `string` | `optional` | `` |  |
| 2 | `front_ping_ms` | `uint32` | `optional` | `` |  |
| 3 | `penalty` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramClientPingSampleReply.LegacyDataCenter</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamDatagramClientPingSampleReply`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `data_center_id` | `fixed32` | `optional` | `` |  |
| 2 | `best_dc_via_relay_pop_id` | `fixed32` | `optional` | `` |  |
| 3 | `best_dc_ping_ms` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramClientSwitchedPrimary</code> — fields: 12; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `connection_id` | `fixed32` | `optional` | `` |  |
| 2 | `from_ip` | `fixed32` | `optional` | `` |  |
| 3 | `from_port` | `uint32` | `optional` | `` |  |
| 4 | `from_router_cluster` | `fixed32` | `optional` | `` |  |
| 5 | `from_active_time` | `uint32` | `optional` | `` |  |
| 6 | `from_active_packets_recv` | `uint32` | `optional` | `` |  |
| 7 | `from_dropped_reason` | `string` | `optional` | `` |  |
| 8 | `gap_ms` | `uint32` | `optional` | `` |  |
| 9 | `from_quality_now` | `.CMsgSteamDatagramClientSwitchedPrimary.RouterQuality` | `optional` | `` |  |
| 10 | `to_quality_now` | `.CMsgSteamDatagramClientSwitchedPrimary.RouterQuality` | `optional` | `` |  |
| 11 | `from_quality_then` | `.CMsgSteamDatagramClientSwitchedPrimary.RouterQuality` | `optional` | `` |  |
| 12 | `to_quality_then` | `.CMsgSteamDatagramClientSwitchedPrimary.RouterQuality` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramClientSwitchedPrimary.RouterQuality</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamDatagramClientSwitchedPrimary`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `score` | `uint32` | `optional` | `` |  |
| 2 | `front_ping` | `uint32` | `optional` | `` |  |
| 3 | `back_ping` | `uint32` | `optional` | `` |  |
| 4 | `seconds_until_down` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramConnectRequest</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `connection_id` | `fixed32` | `optional` | `` |  |
| 2 | `gameserver_relay_session_id` | `uint32` | `optional` | `` |  |
| 3 | `legacy_client_steam_id` | `fixed64` | `optional` | `` |  |
| 4 | `my_timestamp` | `fixed64` | `optional` | `` |  |
| 5 | `ping_est_ms` | `uint32` | `optional` | `` |  |
| 6 | `crypt` | `.CMsgSteamDatagramSessionCryptInfoSigned` | `optional` | `` |  |
| 7 | `cert` | `.CMsgSteamDatagramCertificateSigned` | `optional` | `` |  |
| 9 | `virtual_port` | `uint32` | `optional` | `` |  |
| 10 | `routing_secret` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramConnectOK</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `client_connection_id` | `fixed32` | `optional` | `` |  |
| 2 | `gameserver_relay_session_id` | `uint32` | `optional` | `` |  |
| 3 | `your_timestamp` | `fixed64` | `optional` | `` |  |
| 4 | `delay_time_usec` | `uint32` | `optional` | `` |  |
| 5 | `crypt` | `.CMsgSteamDatagramSessionCryptInfoSigned` | `optional` | `` |  |
| 6 | `cert` | `.CMsgSteamDatagramCertificateSigned` | `optional` | `` |  |
| 7 | `server_connection_id` | `fixed32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamNetworkingP2PSDRRoutingSummary</code> — fields: 15; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `initial_ping` | `uint32` | `optional` | `` |  |
| 2 | `initial_ping_front_local` | `uint32` | `optional` | `` |  |
| 3 | `initial_ping_front_remote` | `uint32` | `optional` | `` |  |
| 4 | `initial_score` | `uint32` | `optional` | `` |  |
| 5 | `initial_pop_local` | `fixed32` | `optional` | `` |  |
| 6 | `initial_pop_remote` | `fixed32` | `optional` | `` |  |
| 7 | `negotiation_ms` | `uint32` | `optional` | `` |  |
| 8 | `selected_seconds` | `uint32` | `optional` | `` |  |
| 11 | `best_ping` | `uint32` | `optional` | `` |  |
| 12 | `best_ping_front_local` | `uint32` | `optional` | `` |  |
| 13 | `best_ping_front_remote` | `uint32` | `optional` | `` |  |
| 14 | `best_score` | `uint32` | `optional` | `` |  |
| 15 | `best_pop_local` | `fixed32` | `optional` | `` |  |
| 16 | `best_pop_remote` | `fixed32` | `optional` | `` |  |
| 17 | `best_time` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramP2PRoutingSummary</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `ice` | `.CMsgSteamNetworkingICESessionSummary` | `optional` | `` |  |
| 3 | `sdr` | `.CMsgSteamNetworkingP2PSDRRoutingSummary` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramConnectionClosed</code> — fields: 20; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `legacy_gameserver_relay_session_id` | `uint32` | `optional` | `` |  |
| 3 | `legacy_from_steam_id` | `fixed64` | `optional` | `` |  |
| 4 | `relay_mode` | `.CMsgSteamDatagramConnectionClosed.ERelayMode` | `optional` | `` | default = None |
| 5 | `debug` | `string` | `optional` | `` |  |
| 6 | `reason_code` | `uint32` | `optional` | `` |  |
| 7 | `to_connection_id` | `fixed32` | `optional` | `` |  |
| 8 | `from_connection_id` | `fixed32` | `optional` | `` |  |
| 9 | `to_relay_session_id` | `fixed32` | `optional` | `` |  |
| 10 | `from_relay_session_id` | `fixed32` | `optional` | `` |  |
| 11 | `forward_target_relay_routing_token` | `bytes` | `optional` | `` |  |
| 12 | `forward_target_revision` | `uint32` | `optional` | `` |  |
| 13 | `legacy_from_identity_binary` | `.CMsgSteamNetworkingIdentityLegacyBinary` | `optional` | `` |  |
| 14 | `routing_secret` | `fixed64` | `optional` | `` |  |
| 15 | `from_identity_string` | `string` | `optional` | `` |  |
| 16 | `not_primary_session` | `bool` | `optional` | `` |  |
| 17 | `quality_relay` | `.CMsgSteamDatagramConnectionQuality` | `optional` | `` |  |
| 18 | `quality_e2e` | `.CMsgSteamDatagramConnectionQuality` | `optional` | `` |  |
| 19 | `not_primary_transport` | `bool` | `optional` | `` |  |
| 21 | `p2p_routing_summary` | `.CMsgSteamDatagramP2PRoutingSummary` | `optional` | `` |  |
| 22 | `relay_override_active` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramNoConnection</code> — fields: 16; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `legacy_gameserver_relay_session_id` | `uint32` | `optional` | `` |  |
| 3 | `legacy_from_steam_id` | `fixed64` | `optional` | `` |  |
| 4 | `end_to_end` | `bool` | `optional` | `` |  |
| 5 | `to_connection_id` | `fixed32` | `optional` | `` |  |
| 6 | `from_connection_id` | `fixed32` | `optional` | `` |  |
| 7 | `from_identity_string` | `string` | `optional` | `` |  |
| 9 | `to_relay_session_id` | `fixed32` | `optional` | `` |  |
| 10 | `from_relay_session_id` | `fixed32` | `optional` | `` |  |
| 11 | `routing_secret` | `fixed64` | `optional` | `` |  |
| 12 | `not_primary_session` | `bool` | `optional` | `` |  |
| 13 | `quality_relay` | `.CMsgSteamDatagramConnectionQuality` | `optional` | `` |  |
| 14 | `quality_e2e` | `.CMsgSteamDatagramConnectionQuality` | `optional` | `` |  |
| 15 | `not_primary_transport` | `bool` | `optional` | `` |  |
| 16 | `p2p_routing_summary` | `.CMsgSteamDatagramP2PRoutingSummary` | `optional` | `` |  |
| 17 | `relay_override_active` | `bool` | `optional` | `` |  |
| 1023 | `dummy_pad` | `fixed32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramGameserverSessionRequest</code> — fields: 11; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ticket` | `bytes` | `optional` | `` |  |
| 3 | `challenge_time` | `fixed32` | `optional` | `` |  |
| 4 | `challenge` | `fixed64` | `optional` | `` |  |
| 5 | `client_connection_id` | `fixed32` | `optional` | `` |  |
| 6 | `network_config_version` | `uint64` | `optional` | `` |  |
| 7 | `protocol_version` | `uint32` | `optional` | `` |  |
| 8 | `server_connection_id` | `fixed32` | `optional` | `` |  |
| 9 | `platform` | `string` | `optional` | `` |  |
| 10 | `build` | `string` | `optional` | `` |  |
| 100 | `dev_gameserver_identity` | `string` | `optional` | `` |  |
| 101 | `dev_client_cert` | `.CMsgSteamDatagramCertificateSigned` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramGameserverSessionEstablished</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `connection_id` | `fixed32` | `optional` | `` |  |
| 2 | `gameserver_identity_string` | `string` | `optional` | `` |  |
| 3 | `legacy_gameserver_steamid` | `fixed64` | `optional` | `` |  |
| 4 | `seconds_until_shutdown` | `uint32` | `optional` | `` |  |
| 6 | `seq_num_r2c` | `uint32` | `optional` | `` |  |
| 7 | `dummy_legacy_identity_binary` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramConnectionStatsClientToRouter</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `quality_relay` | `.CMsgSteamDatagramConnectionQuality` | `optional` | `` |  |
| 2 | `quality_e2e` | `.CMsgSteamDatagramConnectionQuality` | `optional` | `` |  |
| 4 | `ack_relay` | `fixed32` | `repeated` | `` |  |
| 5 | `legacy_ack_e2e` | `fixed32` | `repeated` | `` |  |
| 6 | `flags` | `uint32` | `optional` | `` |  |
| 8 | `client_connection_id` | `fixed32` | `optional` | `` |  |
| 9 | `seq_num_c2r` | `uint32` | `optional` | `` |  |
| 10 | `seq_num_e2e` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramConnectionStatsRouterToClient</code> — fields: 12; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `quality_relay` | `.CMsgSteamDatagramConnectionQuality` | `optional` | `` |  |
| 2 | `quality_e2e` | `.CMsgSteamDatagramConnectionQuality` | `optional` | `` |  |
| 6 | `seconds_until_shutdown` | `uint32` | `optional` | `` |  |
| 7 | `client_connection_id` | `fixed32` | `optional` | `` |  |
| 8 | `seq_num_r2c` | `uint32` | `optional` | `` |  |
| 9 | `seq_num_e2e` | `uint32` | `optional` | `` |  |
| 10 | `migrate_request_ip` | `fixed32` | `optional` | `` |  |
| 11 | `migrate_request_port` | `uint32` | `optional` | `` |  |
| 12 | `scoring_penalty_relay_cluster` | `uint32` | `optional` | `` |  |
| 13 | `ack_relay` | `fixed32` | `repeated` | `` |  |
| 14 | `legacy_ack_e2e` | `fixed32` | `repeated` | `` |  |
| 15 | `flags` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramConnectionStatsRouterToServer</code> — fields: 13; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `quality_relay` | `.CMsgSteamDatagramConnectionQuality` | `optional` | `` |  |
| 2 | `quality_e2e` | `.CMsgSteamDatagramConnectionQuality` | `optional` | `` |  |
| 5 | `seq_num_r2s` | `uint32` | `optional` | `` |  |
| 6 | `seq_num_e2e` | `uint32` | `optional` | `` |  |
| 7 | `legacy_client_steam_id` | `fixed64` | `optional` | `` |  |
| 8 | `relay_session_id` | `uint32` | `optional` | `` |  |
| 9 | `client_connection_id` | `fixed32` | `optional` | `` |  |
| 10 | `ack_relay` | `fixed32` | `repeated` | `` |  |
| 11 | `legacy_ack_e2e` | `fixed32` | `repeated` | `` |  |
| 12 | `flags` | `uint32` | `optional` | `` |  |
| 13 | `server_connection_id` | `fixed32` | `optional` | `` |  |
| 14 | `routing_secret` | `fixed64` | `optional` | `` |  |
| 15 | `client_identity_string` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramConnectionStatsServerToRouter</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `quality_relay` | `.CMsgSteamDatagramConnectionQuality` | `optional` | `` |  |
| 2 | `quality_e2e` | `.CMsgSteamDatagramConnectionQuality` | `optional` | `` |  |
| 3 | `seq_num_s2r` | `uint32` | `optional` | `` |  |
| 4 | `seq_num_e2e` | `uint32` | `optional` | `` |  |
| 6 | `relay_session_id` | `uint32` | `optional` | `` |  |
| 7 | `client_connection_id` | `fixed32` | `optional` | `` |  |
| 8 | `ack_relay` | `fixed32` | `repeated` | `` |  |
| 9 | `legacy_ack_e2e` | `fixed32` | `repeated` | `` |  |
| 10 | `flags` | `uint32` | `optional` | `` |  |
| 11 | `server_connection_id` | `fixed32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramP2PSessionRequestBody</code> — fields: 13; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `challenge_time` | `fixed32` | `optional` | `` |  |
| 2 | `challenge` | `fixed64` | `optional` | `` |  |
| 3 | `client_connection_id` | `fixed32` | `optional` | `` |  |
| 4 | `legacy_peer_steam_id` | `fixed64` | `optional` | `` |  |
| 5 | `peer_connection_id` | `fixed32` | `optional` | `` |  |
| 8 | `protocol_version` | `uint32` | `optional` | `` |  |
| 9 | `network_config_version` | `uint64` | `optional` | `` |  |
| 11 | `peer_identity_string` | `string` | `optional` | `` |  |
| 12 | `platform` | `string` | `optional` | `` |  |
| 13 | `build` | `string` | `optional` | `` |  |
| 14 | `encrypted_data` | `bytes` | `optional` | `` |  |
| 15 | `encryption_your_public_key_lead_byte` | `uint32` | `optional` | `` |  |
| 16 | `encryption_my_ephemeral_public_key` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramP2PSessionRequestBody.EncryptedData</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamDatagramP2PSessionRequestBody`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `peer_identity_string` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramP2PSessionRequest</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `cert` | `.CMsgSteamDatagramCertificateSigned` | `optional` | `` |  |
| 2 | `body` | `bytes` | `optional` | `` |  |
| 3 | `signature` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramP2PSessionEstablished</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `connection_id` | `fixed32` | `optional` | `` |  |
| 3 | `seconds_until_shutdown` | `uint32` | `optional` | `` |  |
| 4 | `relay_routing_token` | `bytes` | `optional` | `` |  |
| 5 | `seq_num_r2c` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramConnectionStatsP2PClientToRouter</code> — fields: 13; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `quality_relay` | `.CMsgSteamDatagramConnectionQuality` | `optional` | `` |  |
| 2 | `quality_e2e` | `.CMsgSteamDatagramConnectionQuality` | `optional` | `` |  |
| 3 | `ack_relay` | `fixed32` | `repeated` | `` |  |
| 4 | `legacy_ack_e2e` | `fixed32` | `repeated` | `` |  |
| 5 | `flags` | `uint32` | `optional` | `` |  |
| 6 | `forward_target_relay_routing_token` | `bytes` | `optional` | `` |  |
| 7 | `forward_target_revision` | `uint32` | `optional` | `` |  |
| 8 | `routes` | `bytes` | `optional` | `` |  |
| 9 | `ack_peer_routes_revision` | `uint32` | `optional` | `` |  |
| 10 | `connection_id` | `fixed32` | `optional` | `` |  |
| 11 | `seq_num_c2r` | `uint32` | `optional` | `` |  |
| 12 | `seq_num_e2e` | `uint32` | `optional` | `` |  |
| 14 | `p2p_routing_summary` | `.CMsgSteamDatagramP2PRoutingSummary` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramConnectionStatsP2PRouterToClient</code> — fields: 15; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `quality_relay` | `.CMsgSteamDatagramConnectionQuality` | `optional` | `` |  |
| 2 | `quality_e2e` | `.CMsgSteamDatagramConnectionQuality` | `optional` | `` |  |
| 3 | `seconds_until_shutdown` | `uint32` | `optional` | `` |  |
| 4 | `migrate_request_ip` | `fixed32` | `optional` | `` |  |
| 5 | `migrate_request_port` | `uint32` | `optional` | `` |  |
| 6 | `scoring_penalty_relay_cluster` | `uint32` | `optional` | `` |  |
| 7 | `ack_relay` | `fixed32` | `repeated` | `` |  |
| 8 | `legacy_ack_e2e` | `fixed32` | `repeated` | `` |  |
| 9 | `flags` | `uint32` | `optional` | `` |  |
| 10 | `ack_forward_target_revision` | `uint32` | `optional` | `` |  |
| 11 | `routes` | `bytes` | `optional` | `` |  |
| 12 | `ack_peer_routes_revision` | `uint32` | `optional` | `` |  |
| 13 | `connection_id` | `fixed32` | `optional` | `` |  |
| 14 | `seq_num_r2c` | `uint32` | `optional` | `` |  |
| 15 | `seq_num_e2e` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramP2PBadRouteRouterToClient</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `connection_id` | `fixed32` | `optional` | `` |  |
| 2 | `failed_relay_routing_token` | `bytes` | `optional` | `` |  |
| 3 | `ack_forward_target_revision` | `uint32` | `optional` | `` |  |
| 99 | `kludge_pad` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramP2PRoutes</code> — fields: 3; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `relay_clusters` | `.CMsgSteamDatagramP2PRoutes.RelayCluster` | `repeated` | `` |  |
| 2 | `routes` | `.CMsgSteamDatagramP2PRoutes.Route` | `repeated` | `` |  |
| 3 | `revision` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramP2PRoutes.RelayCluster</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamDatagramP2PRoutes`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `pop_id` | `fixed32` | `optional` | `` |  |
| 2 | `ping_ms` | `uint32` | `optional` | `` |  |
| 3 | `score_penalty` | `uint32` | `optional` | `` |  |
| 4 | `session_relay_routing_token` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramP2PRoutes.Route</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamDatagramP2PRoutes`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `my_pop_id` | `fixed32` | `optional` | `` |  |
| 2 | `your_pop_id` | `fixed32` | `optional` | `` |  |
| 3 | `legacy_score` | `uint32` | `optional` | `` |  |
| 4 | `interior_score` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramSetSecondaryAddressRequest</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `client_main_ip` | `fixed32` | `optional` | `` |  |
| 2 | `client_main_port` | `fixed32` | `optional` | `` |  |
| 3 | `client_connection_id` | `fixed32` | `optional` | `` |  |
| 4 | `client_identity` | `string` | `optional` | `` |  |
| 5 | `request_send_duplication` | `bool` | `optional` | `` |  |
| 99 | `kludge_pad` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramSetSecondaryAddressResult</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `success` | `bool` | `optional` | `` |  |
| 2 | `message` | `string` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>ESteamDatagramMsgID</code> — values: 34</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_ESteamDatagramMsg_Invalid` | 0 |
| `k_ESteamDatagramMsg_RouterPingRequest` | 1 |
| `k_ESteamDatagramMsg_RouterPingReply` | 2 |
| `k_ESteamDatagramMsg_GameserverPingRequest` | 3 |
| `k_ESteamDatagramMsg_GameserverSessionRequest` | 5 |
| `k_ESteamDatagramMsg_GameserverSessionEstablished` | 6 |
| `k_ESteamDatagramMsg_NoSession` | 7 |
| `k_ESteamDatagramMsg_Diagnostic` | 8 |
| `k_ESteamDatagramMsg_DataClientToRouter` | 9 |
| `k_ESteamDatagramMsg_DataRouterToServer` | 10 |
| `k_ESteamDatagramMsg_DataServerToRouter` | 11 |
| `k_ESteamDatagramMsg_DataRouterToClient` | 12 |
| `k_ESteamDatagramMsg_Stats` | 13 |
| `k_ESteamDatagramMsg_ClientPingSampleRequest` | 14 |
| `k_ESteamDatagramMsg_ClientPingSampleReply` | 15 |
| `k_ESteamDatagramMsg_ClientToRouterSwitchedPrimary` | 16 |
| `k_ESteamDatagramMsg_RelayHealth` | 17 |
| `k_ESteamDatagramMsg_ConnectRequest` | 18 |
| `k_ESteamDatagramMsg_ConnectOK` | 19 |
| `k_ESteamDatagramMsg_ConnectionClosed` | 20 |
| `k_ESteamDatagramMsg_NoConnection` | 21 |
| `k_ESteamDatagramMsg_TicketDecryptRequest` | 22 |
| `k_ESteamDatagramMsg_TicketDecryptReply` | 23 |
| `k_ESteamDatagramMsg_P2PSessionRequest` | 24 |
| `k_ESteamDatagramMsg_P2PSessionEstablished` | 25 |
| `k_ESteamDatagramMsg_P2PStatsClient` | 26 |
| `k_ESteamDatagramMsg_P2PStatsRelay` | 27 |
| `k_ESteamDatagramMsg_P2PBadRoute` | 28 |
| `k_ESteamDatagramMsg_GameserverPingReply` | 29 |
| `k_ESteamDatagramMsg_LegacyGameserverRegistration` | 30 |
| `k_ESteamDatagramMsg_SetSecondaryAddressRequest` | 31 |
| `k_ESteamDatagramMsg_SetSecondaryAddressResult` | 32 |
| `k_ESteamDatagramMsg_RelayToRelayPingRequest` | 33 |
| `k_ESteamDatagramMsg_RelayToRelayPingReply` | 34 |

</details>

<details>
<summary><code>CMsgSteamDatagramRouterPingReply.Flags</code> — values: 2</summary>

- Parent: `CMsgSteamDatagramRouterPingReply`

| Name | Number |
|---|---:|
| `FLAG_MAYBE_MORE_DATA_CENTERS` | 1 |
| `FLAG_MAYBE_MORE_ALT_ADDRESSES` | 2 |

</details>

<details>
<summary><code>CMsgSteamDatagramRouterPingReply.AltAddress.Protocol</code> — values: 1</summary>

- Parent: `CMsgSteamDatagramRouterPingReply.AltAddress`

| Name | Number |
|---|---:|
| `DefaultProtocol` | 0 |

</details>

<details>
<summary><code>CMsgSteamDatagramConnectionClosed.ERelayMode</code> — values: 3</summary>

- Parent: `CMsgSteamDatagramConnectionClosed`

| Name | Number |
|---|---:|
| `None` | 0 |
| `EndToEnd` | 1 |
| `ClosedByPeer` | 2 |

</details>

<details>
<summary><code>CMsgSteamDatagramConnectionStatsClientToRouter.Flags</code> — values: 5</summary>

- Parent: `CMsgSteamDatagramConnectionStatsClientToRouter`

| Name | Number |
|---|---:|
| `ACK_REQUEST_RELAY` | 1 |
| `ACK_REQUEST_E2E` | 2 |
| `ACK_REQUEST_IMMEDIATE` | 4 |
| `NOT_PRIMARY_SESSION` | 8 |
| `CLIENT_RELAY_OVERRIDE` | 32 |

</details>

<details>
<summary><code>CMsgSteamDatagramConnectionStatsRouterToClient.Flags</code> — values: 3</summary>

- Parent: `CMsgSteamDatagramConnectionStatsRouterToClient`

| Name | Number |
|---|---:|
| `ACK_REQUEST_RELAY` | 1 |
| `ACK_REQUEST_E2E` | 2 |
| `ACK_REQUEST_IMMEDIATE` | 4 |

</details>

<details>
<summary><code>CMsgSteamDatagramConnectionStatsRouterToServer.Flags</code> — values: 3</summary>

- Parent: `CMsgSteamDatagramConnectionStatsRouterToServer`

| Name | Number |
|---|---:|
| `ACK_REQUEST_RELAY` | 1 |
| `ACK_REQUEST_E2E` | 2 |
| `ACK_REQUEST_IMMEDIATE` | 4 |

</details>

<details>
<summary><code>CMsgSteamDatagramConnectionStatsServerToRouter.Flags</code> — values: 3</summary>

- Parent: `CMsgSteamDatagramConnectionStatsServerToRouter`

| Name | Number |
|---|---:|
| `ACK_REQUEST_RELAY` | 1 |
| `ACK_REQUEST_E2E` | 2 |
| `ACK_REQUEST_IMMEDIATE` | 4 |

</details>

<details>
<summary><code>CMsgSteamDatagramConnectionStatsP2PClientToRouter.Flags</code> — values: 6</summary>

- Parent: `CMsgSteamDatagramConnectionStatsP2PClientToRouter`

| Name | Number |
|---|---:|
| `ACK_REQUEST_RELAY` | 1 |
| `ACK_REQUEST_E2E` | 2 |
| `ACK_REQUEST_IMMEDIATE` | 4 |
| `NOT_PRIMARY_SESSION` | 8 |
| `NOT_PRIMARY_TRANSPORT_E2E` | 16 |
| `CLIENT_RELAY_OVERRIDE` | 32 |

</details>

<details>
<summary><code>CMsgSteamDatagramConnectionStatsP2PRouterToClient.Flags</code> — values: 4</summary>

- Parent: `CMsgSteamDatagramConnectionStatsP2PRouterToClient`

| Name | Number |
|---|---:|
| `ACK_REQUEST_RELAY` | 1 |
| `ACK_REQUEST_E2E` | 2 |
| `ACK_REQUEST_IMMEDIATE` | 4 |
| `NOT_PRIMARY_TRANSPORT_E2E` | 16 |

</details>
