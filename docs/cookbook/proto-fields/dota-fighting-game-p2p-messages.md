# dota_fighting_game_p2p_messages.proto

- Module: `dota_fighting_game_p2p_messages_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **2**
- Messages: **6** (top-level: 4)
- Enums: **1** (top-level: 0)

## Imports

- `netmessages.proto`
- `networkbasetypes.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgFightingGame_GameData_Fighting</code> — fields: 8; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `last_acked_frame` | `int32` | `optional` | `` |  |
| 2 | `player_id` | `uint32` | `optional` | `` |  |
| 3 | `last_crc_frame` | `int32` | `optional` | `` |  |
| 4 | `last_crc_value` | `uint32` | `optional` | `` |  |
| 5 | `now` | `float` | `optional` | `` |  |
| 6 | `peer_ack_time` | `float` | `optional` | `` |  |
| 7 | `input_start_frame` | `int32` | `optional` | `` |  |
| 8 | `input_sample` | `.CMsgFightingGame_GameData_Fighting.InputSample` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgFightingGame_GameData_Fighting.InputSample</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgFightingGame_GameData_Fighting`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `button_mask` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgFightingGame_GameData_CharacterSelect</code> — fields: 6; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `cursor_index` | `uint32` | `optional` | `` |  |
| 2 | `selected_hero_id` | `int32` | `optional` | `` |  |
| 3 | `selected_style` | `uint32` | `optional` | `` |  |
| 4 | `econ_item_refs` | `.CMsgFightingGame_GameData_CharacterSelect.Item` | `repeated` | `` |  |
| 5 | `message_ack` | `int64` | `optional` | `` |  |
| 6 | `confirmed_style` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgFightingGame_GameData_CharacterSelect.Item</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgFightingGame_GameData_CharacterSelect`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_def` | `uint32` | `optional` | `` |  |
| 2 | `style_index` | `uint32` | `optional` | `` | default = 255 |

</details>

<details>
<summary><code>CMsgFightingGame_GameData_Loaded</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `now` | `float` | `optional` | `` |  |
| 2 | `peer_ack_time` | `float` | `optional` | `` |  |
| 3 | `proposed_start_time` | `float` | `optional` | `` |  |
| 4 | `accepted_start_time` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CP2P_FightingGame_GameData</code> — fields: 4; oneofs: 1; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: `state_data`

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `state` | `.CP2P_FightingGame_GameData.EState` | `optional` | `` | default = k_ChoosingCharacter |
| 2 | `fight` | `.CMsgFightingGame_GameData_Fighting` | `oneof` | `state_data` |  |
| 3 | `character_select` | `.CMsgFightingGame_GameData_CharacterSelect` | `oneof` | `state_data` |  |
| 4 | `loaded` | `.CMsgFightingGame_GameData_Loaded` | `oneof` | `state_data` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>CP2P_FightingGame_GameData.EState</code> — values: 3</summary>

- Parent: `CP2P_FightingGame_GameData`

| Name | Number |
|---|---:|
| `k_ChoosingCharacter` | 1 |
| `k_Loaded` | 2 |
| `k_Fighting` | 3 |

</details>
