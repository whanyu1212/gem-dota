# c_peer2peer_netmessages.proto

- Module: `c_peer2peer_netmessages_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **2**
- Messages: **7** (top-level: 6)
- Enums: **2** (top-level: 1)

## Imports

- `netmessages.proto`
- `networkbasetypes.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CP2P_TextMessage</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `text` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CSteam_Voice_Encoding</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `voice_data` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CP2P_Voice</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `audio` | `.CMsgVoiceAudio` | `optional` | `` |  |
| 2 | `broadcast_group` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CP2P_Ping</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `send_time` | `uint64` | `required` | `` |  |
| 2 | `is_reply` | `bool` | `required` | `` |  |

</details>

<details>
<summary><code>CP2P_VRAvatarPosition</code> — fields: 4; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `body_parts` | `.CP2P_VRAvatarPosition.COrientation` | `repeated` | `` |  |
| 2 | `hat_id` | `int32` | `optional` | `` |  |
| 3 | `scene_id` | `int32` | `optional` | `` |  |
| 4 | `world_scale` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CP2P_VRAvatarPosition.COrientation</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CP2P_VRAvatarPosition`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `pos` | `.CMsgVector` | `optional` | `` |  |
| 2 | `ang` | `.CMsgQAngle` | `optional` | `` |  |

</details>

<details>
<summary><code>CP2P_WatchSynchronization</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `demo_tick` | `int32` | `optional` | `` |  |
| 2 | `paused` | `bool` | `optional` | `` |  |
| 3 | `tv_listen_voice_indices` | `uint64` | `optional` | `` |  |
| 4 | `dota_spectator_mode` | `int32` | `optional` | `` |  |
| 5 | `dota_spectator_watching_broadcaster` | `bool` | `optional` | `` |  |
| 6 | `dota_spectator_hero_index` | `int32` | `optional` | `` |  |
| 7 | `dota_spectator_autospeed` | `int32` | `optional` | `` |  |
| 8 | `dota_replay_speed` | `int32` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>P2P_Messages</code> — values: 7</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `p2p_TextMessage` | 256 |
| `p2p_Voice` | 257 |
| `p2p_Ping` | 258 |
| `p2p_VRAvatarPosition` | 259 |
| `p2p_WatchSynchronization` | 260 |
| `p2p_FightingGame_GameData` | 261 |
| `p2p_FightingGame_Connection` | 262 |

</details>

<details>
<summary><code>CP2P_Voice.Handler_Flags</code> — values: 1</summary>

- Parent: `CP2P_Voice`

| Name | Number |
|---|---:|
| `Played_Audio` | 1 |

</details>
