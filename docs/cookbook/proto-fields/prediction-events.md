# prediction_events.proto

- Module: `prediction_events_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **1**
- Messages: **3** (top-level: 3)
- Enums: **1** (top-level: 1)

## Imports

- `networkbasetypes.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CPredictionEvent_Teleport</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `origin` | `.CMsgVector` | `optional` | `` |  |
| 2 | `angles` | `.CMsgQAngle` | `optional` | `` |  |
| 3 | `drop_to_ground_range` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CPredictionEvent_StringCommand</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `command` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CPredictionEvent_Diagnostic</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `id` | `uint32` | `optional` | `` |  |
| 2 | `requested_sync` | `uint32` | `optional` | `` |  |
| 3 | `requested_player_index` | `uint32` | `optional` | `` |  |
| 4 | `execution_sync` | `uint32` | `repeated` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>EBasePredictionEvents</code> — values: 3</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `BPE_StringCommand` | 128 |
| `BPE_Teleport` | 130 |
| `BPE_Diagnostic` | 16384 |

</details>
