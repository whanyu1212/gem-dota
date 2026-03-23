# dota_usercmd.proto

- Module: `dota_usercmd_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **2**
- Messages: **1** (top-level: 1)
- Enums: **0** (top-level: 0)

## Imports

- `networkbasetypes.proto`
- `usercmd.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CDota2UserCmdPB</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `base` | `.CBaseUserCmdPB` | `optional` | `` |  |
| 2 | `spectator_query_unit_entindex` | `int32` | `optional` | `` |  |
| 3 | `crosshairtrace` | `.CMsgVector` | `optional` | `` |  |
| 4 | `cameraposition_x` | `int32` | `optional` | `` |  |
| 5 | `cameraposition_y` | `int32` | `optional` | `` |  |
| 6 | `clickbehavior` | `uint32` | `optional` | `` |  |
| 7 | `statspanel` | `uint32` | `optional` | `` |  |
| 8 | `shoppanel` | `uint32` | `optional` | `` |  |
| 9 | `stats_dropdown` | `uint32` | `optional` | `` |  |
| 10 | `stats_dropdown_sort` | `uint32` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

*(No enums in this proto file.)*
