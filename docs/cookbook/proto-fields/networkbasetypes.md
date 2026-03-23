# networkbasetypes.proto

- Module: `networkbasetypes_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **2**
- Messages: **27** (top-level: 24)
- Enums: **3** (top-level: 3)

## Imports

- `google/protobuf/descriptor.proto`
- `network_connection.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgVector</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `x` | `float` | `optional` | `` |  |
| 2 | `y` | `float` | `optional` | `` |  |
| 3 | `z` | `float` | `optional` | `` |  |
| 4 | `w` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgVector2D</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `x` | `float` | `optional` | `` |  |
| 2 | `y` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgQAngle</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `x` | `float` | `optional` | `` |  |
| 2 | `y` | `float` | `optional` | `` |  |
| 3 | `z` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgQuaternion</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `x` | `float` | `optional` | `` |  |
| 2 | `y` | `float` | `optional` | `` |  |
| 3 | `z` | `float` | `optional` | `` |  |
| 4 | `w` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTransform</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `position` | `.CMsgVector` | `optional` | `` |  |
| 2 | `scale` | `float` | `optional` | `` |  |
| 3 | `orientation` | `.CMsgQuaternion` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgRGBA</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `r` | `int32` | `optional` | `` |  |
| 2 | `g` | `int32` | `optional` | `` |  |
| 3 | `b` | `int32` | `optional` | `` |  |
| 4 | `a` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPlayerInfo</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `xuid` | `fixed64` | `optional` | `` |  |
| 3 | `userid` | `int32` | `optional` | `` |  |
| 4 | `steamid` | `fixed64` | `optional` | `` |  |
| 5 | `fakeplayer` | `bool` | `optional` | `` |  |
| 6 | `ishltv` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CEntityMsg</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_entity` | `uint32` | `optional` | `` | default = 16777215 |

</details>

<details>
<summary><code>CMsg_CVars</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `cvars` | `.CMsg_CVars.CVar` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsg_CVars.CVar</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsg_CVars`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `value` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CNETMsg_NOP</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CNETMsg_SplitScreenUser</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `slot` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CNETMsg_Tick</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `tick` | `uint32` | `optional` | `` |  |
| 4 | `host_computationtime` | `uint32` | `optional` | `` |  |
| 5 | `host_computationtime_std_deviation` | `uint32` | `optional` | `` |  |
| 7 | `legacy_host_loss` | `uint32` | `optional` | `` |  |
| 8 | `host_unfiltered_frametime` | `uint32` | `optional` | `` |  |
| 9 | `hltv_replay_flags` | `uint32` | `optional` | `` |  |
| 10 | `expected_long_tick` | `uint32` | `optional` | `` |  |
| 11 | `expected_long_tick_reason` | `string` | `optional` | `` |  |
| 12 | `host_frame_dropped_pct_x10` | `uint32` | `optional` | `` |  |
| 13 | `host_frame_irregular_arrival_pct_x10` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CNETMsg_StringCmd</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `command` | `string` | `optional` | `` |  |
| 2 | `prediction_sync` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CNETMsg_SetConVar</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `convars` | `.CMsg_CVars` | `optional` | `` |  |

</details>

<details>
<summary><code>CNETMsg_SignonState</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `signon_state` | `.SignonState_t` | `optional` | `` | default = SIGNONSTATE_NONE |
| 2 | `spawn_count` | `uint32` | `optional` | `` |  |
| 3 | `num_server_players` | `uint32` | `optional` | `` |  |
| 4 | `players_networkids` | `string` | `repeated` | `` |  |
| 5 | `map_name` | `string` | `optional` | `` |  |
| 6 | `addons` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_GameEvent</code> — fields: 3; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_name` | `string` | `optional` | `` |  |
| 2 | `eventid` | `int32` | `optional` | `` |  |
| 3 | `keys` | `.CSVCMsg_GameEvent.key_t` | `repeated` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_GameEvent.key_t</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CSVCMsg_GameEvent`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `type` | `int32` | `optional` | `` |  |
| 2 | `val_string` | `string` | `optional` | `` |  |
| 3 | `val_float` | `float` | `optional` | `` |  |
| 4 | `val_long` | `int32` | `optional` | `` |  |
| 5 | `val_short` | `int32` | `optional` | `` |  |
| 6 | `val_byte` | `int32` | `optional` | `` |  |
| 7 | `val_bool` | `bool` | `optional` | `` |  |
| 8 | `val_uint64` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsgList_GameEvents</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `events` | `.CSVCMsgList_GameEvents.event_t` | `repeated` | `` |  |

</details>

<details>
<summary><code>CSVCMsgList_GameEvents.event_t</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CSVCMsgList_GameEvents`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `tick` | `int32` | `optional` | `` |  |
| 2 | `event` | `.CSVCMsg_GameEvent` | `optional` | `` |  |

</details>

<details>
<summary><code>CNETMsg_SpawnGroup_Load</code> — fields: 20; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `worldname` | `string` | `optional` | `` |  |
| 2 | `entitylumpname` | `string` | `optional` | `` |  |
| 3 | `entityfiltername` | `string` | `optional` | `` |  |
| 4 | `spawngrouphandle` | `uint32` | `optional` | `` |  |
| 5 | `spawngroupownerhandle` | `uint32` | `optional` | `` |  |
| 6 | `world_offset_pos` | `.CMsgVector` | `optional` | `` |  |
| 7 | `world_offset_angle` | `.CMsgQAngle` | `optional` | `` |  |
| 8 | `spawngroupmanifest` | `bytes` | `optional` | `` |  |
| 9 | `flags` | `uint32` | `optional` | `` |  |
| 10 | `tickcount` | `int32` | `optional` | `` |  |
| 11 | `manifestincomplete` | `bool` | `optional` | `` |  |
| 12 | `localnamefixup` | `string` | `optional` | `` |  |
| 13 | `parentnamefixup` | `string` | `optional` | `` |  |
| 14 | `manifestloadpriority` | `int32` | `optional` | `` |  |
| 15 | `worldgroupid` | `uint32` | `optional` | `` |  |
| 16 | `creationsequence` | `uint32` | `optional` | `` |  |
| 17 | `savegamefilename` | `string` | `optional` | `` |  |
| 18 | `spawngroupparenthandle` | `uint32` | `optional` | `` |  |
| 19 | `leveltransition` | `bool` | `optional` | `` |  |
| 20 | `worldgroupname` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CNETMsg_SpawnGroup_ManifestUpdate</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `spawngrouphandle` | `uint32` | `optional` | `` |  |
| 2 | `spawngroupmanifest` | `bytes` | `optional` | `` |  |
| 3 | `manifestincomplete` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CNETMsg_SpawnGroup_SetCreationTick</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `spawngrouphandle` | `uint32` | `optional` | `` |  |
| 2 | `tickcount` | `int32` | `optional` | `` |  |
| 3 | `creationsequence` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CNETMsg_SpawnGroup_Unload</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `spawngrouphandle` | `uint32` | `optional` | `` |  |
| 2 | `flags` | `uint32` | `optional` | `` |  |
| 3 | `tickcount` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CNETMsg_SpawnGroup_LoadCompleted</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `spawngrouphandle` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_GameSessionConfiguration</code> — fields: 19; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `is_multiplayer` | `bool` | `optional` | `` |  |
| 2 | `is_loadsavegame` | `bool` | `optional` | `` |  |
| 3 | `is_background_map` | `bool` | `optional` | `` |  |
| 4 | `is_headless` | `bool` | `optional` | `` |  |
| 5 | `min_client_limit` | `uint32` | `optional` | `` |  |
| 6 | `max_client_limit` | `uint32` | `optional` | `` |  |
| 7 | `max_clients` | `uint32` | `optional` | `` |  |
| 8 | `tick_interval` | `fixed32` | `optional` | `` |  |
| 9 | `hostname` | `string` | `optional` | `` |  |
| 10 | `savegamename` | `string` | `optional` | `` |  |
| 11 | `s1_mapname` | `string` | `optional` | `` |  |
| 12 | `gamemode` | `string` | `optional` | `` |  |
| 13 | `server_ip_address` | `string` | `optional` | `` |  |
| 14 | `data` | `bytes` | `optional` | `` |  |
| 15 | `is_localonly` | `bool` | `optional` | `` |  |
| 16 | `is_transition` | `bool` | `optional` | `` |  |
| 17 | `previouslevel` | `string` | `optional` | `` |  |
| 18 | `landmarkname` | `string` | `optional` | `` |  |
| 19 | `no_steam_server` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CNETMsg_DebugOverlay</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `etype` | `int32` | `optional` | `` |  |
| 2 | `vectors` | `.CMsgVector` | `repeated` | `` |  |
| 3 | `colors` | `.CMsgRGBA` | `repeated` | `` |  |
| 4 | `dimensions` | `float` | `repeated` | `` |  |
| 5 | `times` | `float` | `repeated` | `` |  |
| 6 | `bools` | `bool` | `repeated` | `` |  |
| 7 | `uint64s` | `uint64` | `repeated` | `` |  |
| 8 | `strings` | `string` | `repeated` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>SignonState_t</code> — values: 8</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `SIGNONSTATE_NONE` | 0 |
| `SIGNONSTATE_CHALLENGE` | 1 |
| `SIGNONSTATE_CONNECTED` | 2 |
| `SIGNONSTATE_NEW` | 3 |
| `SIGNONSTATE_PRESPAWN` | 4 |
| `SIGNONSTATE_SPAWN` | 5 |
| `SIGNONSTATE_FULL` | 6 |
| `SIGNONSTATE_CHANGELEVEL` | 7 |

</details>

<details>
<summary><code>NET_Messages</code> — values: 13</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `net_NOP` | 0 |
| `net_Disconnect_Legacy` | 1 |
| `net_SplitScreenUser` | 3 |
| `net_Tick` | 4 |
| `net_StringCmd` | 5 |
| `net_SetConVar` | 6 |
| `net_SignonState` | 7 |
| `net_SpawnGroup_Load` | 8 |
| `net_SpawnGroup_ManifestUpdate` | 9 |
| `net_SpawnGroup_SetCreationTick` | 11 |
| `net_SpawnGroup_Unload` | 12 |
| `net_SpawnGroup_LoadCompleted` | 13 |
| `net_DebugOverlay` | 15 |

</details>

<details>
<summary><code>SpawnGroupFlags_t</code> — values: 8</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `SPAWN_GROUP_LOAD_ENTITIES_FROM_SAVE` | 1 |
| `SPAWN_GROUP_DONT_SPAWN_ENTITIES` | 2 |
| `SPAWN_GROUP_SYNCHRONOUS_SPAWN` | 4 |
| `SPAWN_GROUP_IS_INITIAL_SPAWN_GROUP` | 8 |
| `SPAWN_GROUP_CREATE_CLIENT_ONLY_ENTITIES` | 16 |
| `SPAWN_GROUP_BLOCK_UNTIL_LOADED` | 64 |
| `SPAWN_GROUP_LOAD_STREAMING_DATA` | 128 |
| `SPAWN_GROUP_CREATE_NEW_SCENE_WORLD` | 256 |

</details>
