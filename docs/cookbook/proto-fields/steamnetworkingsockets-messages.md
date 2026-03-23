# steamnetworkingsockets_messages.proto

- Module: `steamnetworkingsockets_messages_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **1**
- Messages: **16** (top-level: 10)
- Enums: **2** (top-level: 1)

## Imports

- `steamnetworkingsockets_messages_certs.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgSteamDatagramSessionCryptInfo</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `key_type` | `.CMsgSteamDatagramSessionCryptInfo.EKeyType` | `optional` | `` | default = INVALID |
| 2 | `key_data` | `bytes` | `optional` | `` |  |
| 3 | `nonce` | `fixed64` | `optional` | `` |  |
| 4 | `protocol_version` | `uint32` | `optional` | `` |  |
| 5 | `ciphers` | `.ESteamNetworkingSocketsCipher` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramSessionCryptInfoSigned</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `info` | `bytes` | `optional` | `` |  |
| 2 | `signature` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramDiagnostic</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `severity` | `uint32` | `optional` | `` |  |
| 2 | `text` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramLinkInstantaneousStats</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `out_packets_per_sec_x10` | `uint32` | `optional` | `` |  |
| 2 | `out_bytes_per_sec` | `uint32` | `optional` | `` |  |
| 3 | `in_packets_per_sec_x10` | `uint32` | `optional` | `` |  |
| 4 | `in_bytes_per_sec` | `uint32` | `optional` | `` |  |
| 5 | `ping_ms` | `uint32` | `optional` | `` |  |
| 6 | `packets_dropped_pct` | `uint32` | `optional` | `` |  |
| 7 | `packets_weird_sequence_pct` | `uint32` | `optional` | `` |  |
| 8 | `peak_jitter_usec` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramLinkLifetimeStats</code> — fields: 47; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `connected_seconds` | `uint32` | `optional` | `` |  |
| 3 | `packets_sent` | `uint64` | `optional` | `` |  |
| 4 | `kb_sent` | `uint64` | `optional` | `` |  |
| 5 | `packets_recv` | `uint64` | `optional` | `` |  |
| 6 | `kb_recv` | `uint64` | `optional` | `` |  |
| 7 | `packets_recv_sequenced` | `uint64` | `optional` | `` |  |
| 8 | `packets_recv_dropped` | `uint64` | `optional` | `` |  |
| 9 | `packets_recv_out_of_order` | `uint64` | `optional` | `` |  |
| 10 | `packets_recv_duplicate` | `uint64` | `optional` | `` |  |
| 11 | `packets_recv_lurch` | `uint64` | `optional` | `` |  |
| 12 | `multipath_packets_recv_sequenced` | `uint64` | `repeated` | `` |  |
| 13 | `multipath_packets_recv_later` | `uint64` | `repeated` | `` |  |
| 14 | `multipath_send_enabled` | `uint32` | `optional` | `` |  |
| 15 | `packets_recv_out_of_order_corrected` | `uint64` | `optional` | `` |  |
| 21 | `quality_histogram_100` | `uint32` | `optional` | `` |  |
| 22 | `quality_histogram_99` | `uint32` | `optional` | `` |  |
| 23 | `quality_histogram_97` | `uint32` | `optional` | `` |  |
| 24 | `quality_histogram_95` | `uint32` | `optional` | `` |  |
| 25 | `quality_histogram_90` | `uint32` | `optional` | `` |  |
| 26 | `quality_histogram_75` | `uint32` | `optional` | `` |  |
| 27 | `quality_histogram_50` | `uint32` | `optional` | `` |  |
| 28 | `quality_histogram_1` | `uint32` | `optional` | `` |  |
| 29 | `quality_histogram_dead` | `uint32` | `optional` | `` |  |
| 30 | `quality_ntile_2nd` | `uint32` | `optional` | `` |  |
| 31 | `quality_ntile_5th` | `uint32` | `optional` | `` |  |
| 32 | `quality_ntile_25th` | `uint32` | `optional` | `` |  |
| 33 | `quality_ntile_50th` | `uint32` | `optional` | `` |  |
| 41 | `ping_histogram_25` | `uint32` | `optional` | `` |  |
| 42 | `ping_histogram_50` | `uint32` | `optional` | `` |  |
| 43 | `ping_histogram_75` | `uint32` | `optional` | `` |  |
| 44 | `ping_histogram_100` | `uint32` | `optional` | `` |  |
| 45 | `ping_histogram_125` | `uint32` | `optional` | `` |  |
| 46 | `ping_histogram_150` | `uint32` | `optional` | `` |  |
| 47 | `ping_histogram_200` | `uint32` | `optional` | `` |  |
| 48 | `ping_histogram_300` | `uint32` | `optional` | `` |  |
| 49 | `ping_histogram_max` | `uint32` | `optional` | `` |  |
| 50 | `ping_ntile_5th` | `uint32` | `optional` | `` |  |
| 51 | `ping_ntile_50th` | `uint32` | `optional` | `` |  |
| 52 | `ping_ntile_75th` | `uint32` | `optional` | `` |  |
| 53 | `ping_ntile_95th` | `uint32` | `optional` | `` |  |
| 54 | `ping_ntile_98th` | `uint32` | `optional` | `` |  |
| 61 | `jitter_histogram_negligible` | `uint32` | `optional` | `` |  |
| 62 | `jitter_histogram_1` | `uint32` | `optional` | `` |  |
| 63 | `jitter_histogram_2` | `uint32` | `optional` | `` |  |
| 64 | `jitter_histogram_5` | `uint32` | `optional` | `` |  |
| 65 | `jitter_histogram_10` | `uint32` | `optional` | `` |  |
| 66 | `jitter_histogram_20` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramConnectionQuality</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `instantaneous` | `.CMsgSteamDatagramLinkInstantaneousStats` | `optional` | `` |  |
| 2 | `lifetime` | `.CMsgSteamDatagramLinkLifetimeStats` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgICECandidate</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 3 | `candidate` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgICERendezvous</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `add_candidate` | `.CMsgICECandidate` | `optional` | `` |  |
| 2 | `auth` | `.CMsgICERendezvous.Auth` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgICERendezvous.Auth</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgICERendezvous`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `pwd_frag` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamNetworkingP2PRendezvous</code> — fields: 15; oneofs: 0; nested messages: 5; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `to_connection_id` | `fixed32` | `optional` | `` |  |
| 2 | `sdr_routes` | `bytes` | `optional` | `` |  |
| 3 | `ack_peer_routes_revision` | `uint32` | `optional` | `` |  |
| 4 | `connect_request` | `.CMsgSteamNetworkingP2PRendezvous.ConnectRequest` | `optional` | `` |  |
| 5 | `connect_ok` | `.CMsgSteamNetworkingP2PRendezvous.ConnectOK` | `optional` | `` |  |
| 6 | `connection_closed` | `.CMsgSteamNetworkingP2PRendezvous.ConnectionClosed` | `optional` | `` |  |
| 7 | `ice_enabled` | `bool` | `optional` | `` |  |
| 8 | `from_identity` | `string` | `optional` | `` |  |
| 9 | `from_connection_id` | `fixed32` | `optional` | `` |  |
| 10 | `to_identity` | `string` | `optional` | `` |  |
| 11 | `ack_reliable_msg` | `uint32` | `optional` | `` |  |
| 12 | `first_reliable_msg` | `uint32` | `optional` | `` |  |
| 13 | `reliable_messages` | `.CMsgSteamNetworkingP2PRendezvous.ReliableMessage` | `repeated` | `` |  |
| 14 | `hosted_server_ticket` | `bytes` | `optional` | `` |  |
| 15 | `application_messages` | `.CMsgSteamNetworkingP2PRendezvous.ApplicationMessage` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSteamNetworkingP2PRendezvous.ConnectRequest</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamNetworkingP2PRendezvous`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 6 | `crypt` | `.CMsgSteamDatagramSessionCryptInfoSigned` | `optional` | `` |  |
| 7 | `cert` | `.CMsgSteamDatagramCertificateSigned` | `optional` | `` |  |
| 9 | `to_virtual_port` | `uint32` | `optional` | `` |  |
| 10 | `from_virtual_port` | `uint32` | `optional` | `` |  |
| 11 | `from_fakeip` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamNetworkingP2PRendezvous.ConnectOK</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamNetworkingP2PRendezvous`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 5 | `crypt` | `.CMsgSteamDatagramSessionCryptInfoSigned` | `optional` | `` |  |
| 6 | `cert` | `.CMsgSteamDatagramCertificateSigned` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamNetworkingP2PRendezvous.ConnectionClosed</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamNetworkingP2PRendezvous`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 5 | `debug` | `string` | `optional` | `` |  |
| 6 | `reason_code` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamNetworkingP2PRendezvous.ReliableMessage</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamNetworkingP2PRendezvous`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ice` | `.CMsgICERendezvous` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamNetworkingP2PRendezvous.ApplicationMessage</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamNetworkingP2PRendezvous`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `data` | `bytes` | `optional` | `` |  |
| 2 | `msg_num` | `uint64` | `optional` | `` |  |
| 3 | `flags` | `uint32` | `optional` | `` |  |
| 4 | `lane_idx` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamNetworkingICESessionSummary</code> — fields: 15; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `local_candidate_types` | `uint32` | `optional` | `` |  |
| 2 | `remote_candidate_types` | `uint32` | `optional` | `` |  |
| 3 | `initial_route_kind` | `uint32` | `optional` | `` |  |
| 4 | `initial_ping` | `uint32` | `optional` | `` |  |
| 5 | `negotiation_ms` | `uint32` | `optional` | `` |  |
| 6 | `initial_score` | `uint32` | `optional` | `` |  |
| 7 | `failure_reason_code` | `uint32` | `optional` | `` |  |
| 12 | `selected_seconds` | `uint32` | `optional` | `` |  |
| 13 | `user_settings` | `uint32` | `optional` | `` |  |
| 14 | `ice_enable_var` | `uint32` | `optional` | `` |  |
| 15 | `local_candidate_types_allowed` | `uint32` | `optional` | `` |  |
| 16 | `best_route_kind` | `uint32` | `optional` | `` |  |
| 17 | `best_ping` | `uint32` | `optional` | `` |  |
| 18 | `best_score` | `uint32` | `optional` | `` |  |
| 19 | `best_time` | `uint32` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>ESteamNetworkingSocketsCipher</code> — values: 3</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_ESteamNetworkingSocketsCipher_INVALID` | 0 |
| `k_ESteamNetworkingSocketsCipher_NULL` | 1 |
| `k_ESteamNetworkingSocketsCipher_AES_256_GCM` | 2 |

</details>

<details>
<summary><code>CMsgSteamDatagramSessionCryptInfo.EKeyType</code> — values: 2</summary>

- Parent: `CMsgSteamDatagramSessionCryptInfo`

| Name | Number |
|---|---:|
| `INVALID` | 0 |
| `CURVE25519` | 1 |

</details>
