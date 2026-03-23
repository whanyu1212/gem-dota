# usercmd.proto

- Module: `usercmd_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **1**
- Messages: **5** (top-level: 5)
- Enums: **0** (top-level: 0)

## Imports

- `networkbasetypes.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CInButtonStatePB</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `buttonstate1` | `uint64` | `optional` | `` |  |
| 2 | `buttonstate2` | `uint64` | `optional` | `` |  |
| 3 | `buttonstate3` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CSubtickMoveStep</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `button` | `uint64` | `optional` | `` |  |
| 2 | `pressed` | `bool` | `optional` | `` |  |
| 3 | `when` | `float` | `optional` | `` |  |
| 4 | `analog_forward_delta` | `float` | `optional` | `` |  |
| 5 | `analog_left_delta` | `float` | `optional` | `` |  |
| 8 | `pitch_delta` | `float` | `optional` | `` |  |
| 9 | `yaw_delta` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CBaseUserCmdExecutionNotes</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ignored_reason` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CBaseUserCmdPB</code> — fields: 19; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `legacy_command_number` | `int32` | `optional` | `` |  |
| 2 | `client_tick` | `int32` | `optional` | `` |  |
| 3 | `buttons_pb` | `.CInButtonStatePB` | `optional` | `` |  |
| 4 | `viewangles` | `.CMsgQAngle` | `optional` | `` |  |
| 5 | `forwardmove` | `float` | `optional` | `` |  |
| 6 | `leftmove` | `float` | `optional` | `` |  |
| 7 | `upmove` | `float` | `optional` | `` |  |
| 8 | `impulse` | `int32` | `optional` | `` |  |
| 9 | `weaponselect` | `int32` | `optional` | `` |  |
| 10 | `random_seed` | `int32` | `optional` | `` |  |
| 11 | `mousedx` | `int32` | `optional` | `` |  |
| 12 | `mousedy` | `int32` | `optional` | `` |  |
| 14 | `pawn_entity_handle` | `uint32` | `optional` | `` | default = 16777215 |
| 17 | `prediction_offset_ticks_x256` | `uint32` | `optional` | `` |  |
| 18 | `subtick_moves` | `.CSubtickMoveStep` | `repeated` | `` |  |
| 19 | `move_crc` | `bytes` | `optional` | `` |  |
| 20 | `consumed_server_angle_changes` | `uint32` | `optional` | `` |  |
| 21 | `cmd_flags` | `int32` | `optional` | `` |  |
| 22 | `execution_notes` | `.CBaseUserCmdExecutionNotes` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserCmdBasePB</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `base` | `.CBaseUserCmdPB` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

*(No enums in this proto file.)*
