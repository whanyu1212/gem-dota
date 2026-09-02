# event_gcmessages_common.proto

- Module: `event_gcmessages_common_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **0**
- Messages: **2** (top-level: 2)
- Enums: **0** (top-level: 0)

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgEventAction</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `action_id` | `uint32` | `optional` |  |  |
| 2 | `times_completed` | `uint32` | `optional` |  | default = 1 |

</details>

<details>
<summary><code>CMsgUserEventPoints</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` |  |  |
| 2 | `event_id` | `uint32` | `optional` |  |  |
| 3 | `total_points` | `uint32` | `optional` |  |  |
| 4 | `total_premium_points` | `uint32` | `optional` |  |  |
| 5 | `points` | `uint32` | `optional` |  |  |
| 6 | `premium_points` | `uint32` | `optional` |  |  |
| 7 | `completed_actions` | `.CMsgEventAction` | `repeated` |  |  |
| 8 | `owned` | `bool` | `optional` |  |  |
| 9 | `active_season_id` | `uint32` | `optional` |  |  |

</details>

## Enums

Expand any enum to inspect all values.

*(No enums in this proto file.)*
