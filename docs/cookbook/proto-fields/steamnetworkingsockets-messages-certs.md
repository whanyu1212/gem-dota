# steamnetworkingsockets_messages_certs.proto

- Module: `steamnetworkingsockets_messages_certs_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **0**
- Messages: **4** (top-level: 4)
- Enums: **1** (top-level: 0)

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgSteamNetworkingIdentityLegacyBinary</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `generic_bytes` | `bytes` | `optional` | `` |  |
| 3 | `generic_string` | `string` | `optional` | `` |  |
| 4 | `ipv6_and_port` | `bytes` | `optional` | `` |  |
| 16 | `steam_id` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramCertificate</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `key_type` | `.CMsgSteamDatagramCertificate.EKeyType` | `optional` | `` | default = INVALID |
| 2 | `key_data` | `bytes` | `optional` | `` |  |
| 4 | `legacy_steam_id` | `fixed64` | `optional` | `` |  |
| 5 | `gameserver_datacenter_ids` | `fixed32` | `repeated` | `` |  |
| 8 | `time_created` | `fixed32` | `optional` | `` |  |
| 9 | `time_expiry` | `fixed32` | `optional` | `` |  |
| 10 | `app_ids` | `uint32` | `repeated` | `` |  |
| 11 | `legacy_identity_binary` | `.CMsgSteamNetworkingIdentityLegacyBinary` | `optional` | `` |  |
| 12 | `identity_string` | `string` | `optional` | `` |  |
| 13 | `ip_addresses` | `string` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramCertificateSigned</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `private_key_data` | `bytes` | `optional` | `` |  |
| 4 | `cert` | `bytes` | `optional` | `` |  |
| 5 | `ca_key_id` | `fixed64` | `optional` | `` |  |
| 6 | `ca_signature` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramCertificateRequest</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `cert` | `.CMsgSteamDatagramCertificate` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>CMsgSteamDatagramCertificate.EKeyType</code> — values: 2</summary>

- Parent: `CMsgSteamDatagramCertificate`

| Name | Number |
|---|---:|
| `INVALID` | 0 |
| `ED25519` | 1 |

</details>
