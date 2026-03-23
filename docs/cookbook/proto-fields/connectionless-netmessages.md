# connectionless_netmessages.proto

- Module: `connectionless_netmessages_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **1**
- Messages: **3** (top-level: 3)
- Enums: **0** (top-level: 0)

## Imports

- `netmessages.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>C2S_CONNECT_SameProcessCheck</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `localhost_process_id` | `uint64` | `optional` | `` |  |
| 2 | `key` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>C2S_CONNECT_Message</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `host_version` | `uint32` | `optional` | `` |  |
| 2 | `auth_protocol` | `uint32` | `optional` | `` |  |
| 3 | `challenge_number` | `uint32` | `optional` | `` |  |
| 4 | `reservation_cookie` | `fixed64` | `optional` | `` |  |
| 5 | `low_violence` | `bool` | `optional` | `` |  |
| 6 | `encrypted_password` | `bytes` | `optional` | `` |  |
| 7 | `splitplayers` | `.CCLCMsg_SplitPlayerConnect` | `repeated` | `` |  |
| 8 | `auth_steam` | `bytes` | `optional` | `` |  |
| 9 | `challenge_context` | `string` | `optional` | `` |  |
| 10 | `localhost_same_process_check` | `.C2S_CONNECT_SameProcessCheck` | `optional` | `` |  |

</details>

<details>
<summary><code>C2S_CONNECTION_Message</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `addon_name` | `string` | `optional` | `` |  |
| 2 | `localhost_same_process_check` | `.C2S_CONNECT_SameProcessCheck` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

*(No enums in this proto file.)*
