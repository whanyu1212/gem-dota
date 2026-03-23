# demo.proto

- Module: `demo_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **0**
- Messages: **27** (top-level: 19)
- Enums: **1** (top-level: 1)

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CDemoFileHeader</code> — fields: 15; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `demo_file_stamp` | `string` | `required` | `` |  |
| 2 | `patch_version` | `int32` | `optional` | `` |  |
| 3 | `server_name` | `string` | `optional` | `` |  |
| 4 | `client_name` | `string` | `optional` | `` |  |
| 5 | `map_name` | `string` | `optional` | `` |  |
| 6 | `game_directory` | `string` | `optional` | `` |  |
| 7 | `fullpackets_version` | `int32` | `optional` | `` |  |
| 8 | `allow_clientside_entities` | `bool` | `optional` | `` |  |
| 9 | `allow_clientside_particles` | `bool` | `optional` | `` |  |
| 10 | `addons` | `string` | `optional` | `` |  |
| 11 | `demo_version_name` | `string` | `optional` | `` |  |
| 12 | `demo_version_guid` | `string` | `optional` | `` |  |
| 13 | `build_num` | `int32` | `optional` | `` |  |
| 14 | `game` | `string` | `optional` | `` |  |
| 15 | `server_start_tick` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CGameInfo</code> — fields: 2; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 4 | `dota` | `.CGameInfo.CDotaGameInfo` | `optional` | `` |  |
| 5 | `cs` | `.CGameInfo.CCSGameInfo` | `optional` | `` |  |

</details>

<details>
<summary><code>CGameInfo.CDotaGameInfo</code> — fields: 11; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: `CGameInfo`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `game_mode` | `int32` | `optional` | `` |  |
| 3 | `game_winner` | `int32` | `optional` | `` |  |
| 4 | `player_info` | `.CGameInfo.CDotaGameInfo.CPlayerInfo` | `repeated` | `` |  |
| 5 | `leagueid` | `uint32` | `optional` | `` |  |
| 6 | `picks_bans` | `.CGameInfo.CDotaGameInfo.CHeroSelectEvent` | `repeated` | `` |  |
| 7 | `radiant_team_id` | `uint32` | `optional` | `` |  |
| 8 | `dire_team_id` | `uint32` | `optional` | `` |  |
| 9 | `radiant_team_tag` | `string` | `optional` | `` |  |
| 10 | `dire_team_tag` | `string` | `optional` | `` |  |
| 11 | `end_time` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CGameInfo.CDotaGameInfo.CPlayerInfo</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CGameInfo.CDotaGameInfo`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_name` | `string` | `optional` | `` |  |
| 2 | `player_name` | `string` | `optional` | `` |  |
| 3 | `is_fake_client` | `bool` | `optional` | `` |  |
| 4 | `steamid` | `uint64` | `optional` | `` |  |
| 5 | `game_team` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CGameInfo.CDotaGameInfo.CHeroSelectEvent</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CGameInfo.CDotaGameInfo`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `is_pick` | `bool` | `optional` | `` |  |
| 2 | `team` | `uint32` | `optional` | `` |  |
| 3 | `hero_id` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CGameInfo.CCSGameInfo</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CGameInfo`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `round_start_ticks` | `int32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDemoFileInfo</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `playback_time` | `float` | `optional` | `` |  |
| 2 | `playback_ticks` | `int32` | `optional` | `` |  |
| 3 | `playback_frames` | `int32` | `optional` | `` |  |
| 4 | `game_info` | `.CGameInfo` | `optional` | `` |  |

</details>

<details>
<summary><code>CDemoPacket</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 3 | `data` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CDemoFullPacket</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `string_table` | `.CDemoStringTables` | `optional` | `` |  |
| 2 | `packet` | `.CDemoPacket` | `optional` | `` |  |

</details>

<details>
<summary><code>CDemoSaveGame</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `data` | `bytes` | `optional` | `` |  |
| 2 | `steam_id` | `fixed64` | `optional` | `` |  |
| 3 | `signature` | `fixed64` | `optional` | `` |  |
| 4 | `version` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDemoSyncTick</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CDemoConsoleCmd</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `cmdstring` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CDemoSendTables</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `data` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CDemoClassInfo</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `classes` | `.CDemoClassInfo.class_t` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDemoClassInfo.class_t</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDemoClassInfo`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `class_id` | `int32` | `optional` | `` |  |
| 2 | `network_name` | `string` | `optional` | `` |  |
| 3 | `table_name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CDemoCustomData</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `callback_index` | `int32` | `optional` | `` |  |
| 2 | `data` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CDemoCustomDataCallbacks</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `save_id` | `string` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDemoAnimationHeader</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `entity_id` | `sint32` | `optional` | `` |  |
| 2 | `tick` | `int32` | `optional` | `` |  |
| 3 | `data` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CDemoAnimationData</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `entity_id` | `sint32` | `optional` | `` |  |
| 2 | `start_tick` | `int32` | `optional` | `` |  |
| 3 | `end_tick` | `int32` | `optional` | `` |  |
| 4 | `data` | `bytes` | `optional` | `` |  |
| 5 | `data_checksum` | `int64` | `optional` | `` |  |

</details>

<details>
<summary><code>CDemoStringTables</code> — fields: 1; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `tables` | `.CDemoStringTables.table_t` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDemoStringTables.items_t</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDemoStringTables`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `str` | `string` | `optional` | `` |  |
| 2 | `data` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CDemoStringTables.table_t</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDemoStringTables`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `table_name` | `string` | `optional` | `` |  |
| 2 | `items` | `.CDemoStringTables.items_t` | `repeated` | `` |  |
| 3 | `items_clientside` | `.CDemoStringTables.items_t` | `repeated` | `` |  |
| 4 | `table_flags` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDemoStop</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CDemoUserCmd</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `cmd_number` | `int32` | `optional` | `` |  |
| 2 | `data` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CDemoSpawnGroups</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 3 | `msgs` | `bytes` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDemoRecovery</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `initial_spawn_group` | `.CDemoRecovery.DemoInitialSpawnGroupEntry` | `optional` | `` |  |
| 2 | `spawn_group_message` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CDemoRecovery.DemoInitialSpawnGroupEntry</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDemoRecovery`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `spawngrouphandle` | `uint32` | `optional` | `` |  |
| 2 | `was_created` | `bool` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>EDemoCommands</code> — values: 22</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `DEM_Error` | -1 |
| `DEM_Stop` | 0 |
| `DEM_FileHeader` | 1 |
| `DEM_FileInfo` | 2 |
| `DEM_SyncTick` | 3 |
| `DEM_SendTables` | 4 |
| `DEM_ClassInfo` | 5 |
| `DEM_StringTables` | 6 |
| `DEM_Packet` | 7 |
| `DEM_SignonPacket` | 8 |
| `DEM_ConsoleCmd` | 9 |
| `DEM_CustomData` | 10 |
| `DEM_CustomDataCallbacks` | 11 |
| `DEM_UserCmd` | 12 |
| `DEM_FullPacket` | 13 |
| `DEM_SaveGame` | 14 |
| `DEM_SpawnGroups` | 15 |
| `DEM_AnimationData` | 16 |
| `DEM_AnimationHeader` | 17 |
| `DEM_Recovery` | 18 |
| `DEM_Max` | 19 |
| `DEM_IsCompressed` | 64 |

</details>
