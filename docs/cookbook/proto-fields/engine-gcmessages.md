# engine_gcmessages.proto

- Module: `engine_gcmessages_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **1**
- Messages: **1** (top-level: 1)
- Enums: **0** (top-level: 0)

## Imports

- `google/protobuf/descriptor.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CEngineGotvSyncPacket</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `instance_id` | `uint32` | `optional` | `` |  |
| 3 | `signupfragment` | `uint32` | `optional` | `` |  |
| 4 | `currentfragment` | `uint32` | `optional` | `` |  |
| 5 | `tickrate` | `float` | `optional` | `` |  |
| 6 | `tick` | `uint32` | `optional` | `` |  |
| 8 | `rtdelay` | `float` | `optional` | `` |  |
| 9 | `rcvage` | `float` | `optional` | `` |  |
| 10 | `keyframe_interval` | `float` | `optional` | `` |  |
| 11 | `cdndelay` | `uint32` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

*(No enums in this proto file.)*
