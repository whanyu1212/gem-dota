# steamdatagram_messages_auth.proto

- Module: `steamdatagram_messages_auth_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **1**
- Messages: **7** (top-level: 6)
- Enums: **0** (top-level: 0)

## Imports

- `steamnetworkingsockets_messages_certs.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgSteamDatagramRelayAuthTicket</code> — fields: 13; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `time_expiry` | `fixed32` | `optional` | `` |  |
| 2 | `legacy_authorized_steam_id` | `fixed64` | `optional` | `` |  |
| 3 | `authorized_public_ip` | `fixed32` | `optional` | `` |  |
| 4 | `legacy_gameserver_steam_id` | `fixed64` | `optional` | `` |  |
| 7 | `app_id` | `uint32` | `optional` | `` |  |
| 8 | `extra_fields` | `.CMsgSteamDatagramRelayAuthTicket.ExtraField` | `repeated` | `` |  |
| 9 | `legacy_gameserver_pop_id` | `fixed32` | `optional` | `` |  |
| 10 | `virtual_port` | `uint32` | `optional` | `` |  |
| 11 | `gameserver_address` | `bytes` | `optional` | `` |  |
| 12 | `legacy_authorized_client_identity_binary` | `bytes` | `optional` | `` |  |
| 13 | `legacy_gameserver_identity_binary` | `bytes` | `optional` | `` |  |
| 14 | `authorized_client_identity_string` | `string` | `optional` | `` |  |
| 15 | `gameserver_identity_string` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramRelayAuthTicket.ExtraField</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamDatagramRelayAuthTicket`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `string_value` | `string` | `optional` | `` |  |
| 3 | `int64_value` | `sint64` | `optional` | `` |  |
| 5 | `fixed64_value` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramSignedRelayAuthTicket</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `reserved_do_not_use` | `fixed64` | `optional` | `` |  |
| 2 | `key_id` | `fixed64` | `optional` | `` |  |
| 3 | `ticket` | `bytes` | `optional` | `` |  |
| 4 | `signature` | `bytes` | `optional` | `` |  |
| 5 | `certs` | `.CMsgSteamDatagramCertificateSigned` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramCachedCredentialsForApp</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `private_key` | `bytes` | `optional` | `` |  |
| 2 | `cert` | `bytes` | `optional` | `` |  |
| 3 | `relay_tickets` | `bytes` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramGameCoordinatorServerLogin</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `time_generated` | `uint32` | `optional` | `` |  |
| 2 | `appid` | `uint32` | `optional` | `` |  |
| 3 | `routing` | `bytes` | `optional` | `` |  |
| 4 | `appdata` | `bytes` | `optional` | `` |  |
| 5 | `legacy_identity_binary` | `bytes` | `optional` | `` |  |
| 6 | `identity_string` | `string` | `optional` | `` |  |
| 99 | `dummy_steam_id` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramSignedGameCoordinatorServerLogin</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `cert` | `.CMsgSteamDatagramCertificateSigned` | `optional` | `` |  |
| 2 | `login` | `bytes` | `optional` | `` |  |
| 3 | `signature` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamDatagramHostedServerAddressPlaintext</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ipv4` | `fixed32` | `optional` | `` |  |
| 2 | `ipv6` | `bytes` | `optional` | `` |  |
| 3 | `port` | `uint32` | `optional` | `` |  |
| 4 | `routing_secret` | `fixed64` | `optional` | `` |  |
| 5 | `protocol_version` | `uint32` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

*(No enums in this proto file.)*
