# dota_gcmessages_client_match_management.proto

- Module: `dota_gcmessages_client_match_management_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **5**
- Messages: **62** (top-level: 57)
- Enums: **1** (top-level: 1)

## Imports

- `steammessages.proto`
- `dota_shared_enums.proto`
- `dota_client_enums.proto`
- `base_gcmessages.proto`
- `dota_gcmessages_common_lobby.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgStartFindingMatch</code> — fields: 20; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `key` | `string` | `optional` | `` |  |
| 2 | `matchgroups` | `uint32` | `optional` | `` | default = 4294967295 |
| 3 | `client_version` | `uint32` | `optional` | `` |  |
| 4 | `game_modes` | `uint32` | `optional` | `` | default = 4294967295 |
| 6 | `match_type` | `.MatchType` | `optional` | `` | default = MATCH_TYPE_CASUAL |
| 7 | `matchlanguages` | `uint32` | `optional` | `` | default = 4294967295 |
| 8 | `team_id` | `uint32` | `optional` | `` |  |
| 10 | `game_language_enum` | `.MatchLanguages` | `optional` | `` | default = MATCH_LANGUAGE_INVALID |
| 11 | `game_language_name` | `string` | `optional` | `` |  |
| 12 | `ping_data` | `.CMsgClientPingData` | `optional` | `` |  |
| 13 | `region_select_flags` | `uint32` | `optional` | `` |  |
| 14 | `solo_queue` | `bool` | `optional` | `` |  |
| 16 | `steam_clan_account_id` | `uint32` | `optional` | `` |  |
| 17 | `is_challenge_match` | `bool` | `optional` | `` |  |
| 18 | `lane_selection_flags` | `uint32` | `optional` | `` |  |
| 19 | `high_priority_disabled` | `bool` | `optional` | `` |  |
| 20 | `disable_experimental_gameplay` | `bool` | `optional` | `` |  |
| 21 | `custom_game_difficulty_mask` | `uint32` | `optional` | `` |  |
| 22 | `bot_difficulty_mask` | `uint32` | `optional` | `` |  |
| 23 | `bot_script_index_mask` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgStartFindingMatchResult</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `legacy_generic_eresult` | `uint32` | `optional` | `` | default = 2 |
| 2 | `result` | `.EStartFindingMatchResult` | `optional` | `` | default = k_EStartFindingMatchResult_Invalid |
| 3 | `error_token` | `string` | `optional` | `` |  |
| 4 | `debug_message` | `string` | `optional` | `` |  |
| 5 | `responsible_party_members` | `fixed64` | `repeated` | `` |  |
| 6 | `result_metadata` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgStopFindingMatch</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `accept_cooldown` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPartyBuilderOptions</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `additional_slots` | `uint32` | `optional` | `` |  |
| 2 | `match_type` | `.MatchType` | `optional` | `` | default = MATCH_TYPE_CASUAL |
| 3 | `matchgroups` | `uint32` | `optional` | `` |  |
| 4 | `client_version` | `uint32` | `optional` | `` |  |
| 5 | `language` | `.MatchLanguages` | `optional` | `` | default = MATCH_LANGUAGE_INVALID |

</details>

<details>
<summary><code>CMsgReadyUp</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `state` | `.DOTALobbyReadyState` | `optional` | `` | default = DOTALobbyReadyState_UNDECLARED |
| 2 | `ready_up_key` | `fixed64` | `optional` | `` |  |
| 3 | `hardware_specs` | `.CDOTAClientHardwareSpecs` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgReadyUpStatus</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `lobby_id` | `fixed64` | `optional` | `` |  |
| 2 | `accepted_ids` | `uint32` | `repeated` | `` |  |
| 3 | `declined_ids` | `uint32` | `repeated` | `` |  |
| 4 | `accepted_indices` | `uint32` | `repeated` | `` |  |
| 5 | `declined_indices` | `uint32` | `repeated` | `` |  |
| 6 | `local_ready_state` | `.DOTALobbyReadyState` | `optional` | `` | default = DOTALobbyReadyState_UNDECLARED |

</details>

<details>
<summary><code>CMsgAbandonCurrentGame</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgLobbyScenarioSave</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `version` | `int32` | `optional` | `` |  |
| 2 | `data` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPracticeLobbySetDetails</code> — fields: 43; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `lobby_id` | `uint64` | `optional` | `` |  |
| 2 | `game_name` | `string` | `optional` | `` |  |
| 3 | `team_details` | `.CLobbyTeamDetails` | `repeated` | `` |  |
| 4 | `server_region` | `uint32` | `optional` | `` |  |
| 5 | `game_mode` | `uint32` | `optional` | `` |  |
| 6 | `cm_pick` | `.DOTA_CM_PICK` | `optional` | `` | default = DOTA_CM_RANDOM |
| 9 | `bot_difficulty_radiant` | `.DOTABotDifficulty` | `optional` | `` | default = BOT_DIFFICULTY_PASSIVE |
| 10 | `allow_cheats` | `bool` | `optional` | `` |  |
| 11 | `fill_with_bots` | `bool` | `optional` | `` |  |
| 13 | `allow_spectating` | `bool` | `optional` | `` |  |
| 15 | `pass_key` | `string` | `optional` | `` |  |
| 16 | `leagueid` | `uint32` | `optional` | `` |  |
| 17 | `penalty_level_radiant` | `uint32` | `optional` | `` |  |
| 18 | `penalty_level_dire` | `uint32` | `optional` | `` |  |
| 20 | `series_type` | `uint32` | `optional` | `` |  |
| 21 | `radiant_series_wins` | `uint32` | `optional` | `` |  |
| 22 | `dire_series_wins` | `uint32` | `optional` | `` |  |
| 23 | `allchat` | `bool` | `optional` | `` | default = false |
| 24 | `dota_tv_delay` | `.LobbyDotaTVDelay` | `optional` | `` | default = LobbyDotaTV_120 |
| 25 | `lan` | `bool` | `optional` | `` |  |
| 26 | `custom_game_mode` | `string` | `optional` | `` |  |
| 27 | `custom_map_name` | `string` | `optional` | `` |  |
| 28 | `custom_difficulty` | `uint32` | `optional` | `` |  |
| 29 | `custom_game_id` | `uint64` | `optional` | `` |  |
| 30 | `custom_min_players` | `uint32` | `optional` | `` |  |
| 31 | `custom_max_players` | `uint32` | `optional` | `` |  |
| 33 | `visibility` | `.DOTALobbyVisibility` | `optional` | `` | default = DOTALobbyVisibility_Public |
| 34 | `custom_game_crc` | `fixed64` | `optional` | `` |  |
| 37 | `custom_game_timestamp` | `fixed32` | `optional` | `` |  |
| 38 | `previous_match_override` | `uint64` | `optional` | `` |  |
| 42 | `pause_setting` | `.LobbyDotaPauseSetting` | `optional` | `` | default = LobbyDotaPauseSetting_Unlimited |
| 43 | `bot_difficulty_dire` | `.DOTABotDifficulty` | `optional` | `` | default = BOT_DIFFICULTY_PASSIVE |
| 44 | `bot_radiant` | `uint64` | `optional` | `` |  |
| 45 | `bot_dire` | `uint64` | `optional` | `` |  |
| 46 | `selection_priority_rules` | `.DOTASelectionPriorityRules` | `optional` | `` | default = k_DOTASelectionPriorityRules_Manual |
| 47 | `custom_game_penalties` | `bool` | `optional` | `` |  |
| 48 | `lan_host_ping_location` | `string` | `optional` | `` |  |
| 49 | `league_node_id` | `uint32` | `optional` | `` |  |
| 50 | `requested_hero_ids` | `int32` | `repeated` | `` |  |
| 51 | `scenario_save` | `.CMsgLobbyScenarioSave` | `optional` | `` |  |
| 52 | `ability_draft_specific_details` | `.CMsgPracticeLobbySetDetails.AbilityDraftSpecificDetails` | `optional` | `` |  |
| 53 | `do_player_draft` | `bool` | `optional` | `` |  |
| 54 | `requested_hero_teams` | `int32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgPracticeLobbySetDetails.AbilityDraftSpecificDetails</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgPracticeLobbySetDetails`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `shuffle_draft_order` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPracticeLobbyCreate</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `search_key` | `string` | `optional` | `` |  |
| 5 | `pass_key` | `string` | `optional` | `` |  |
| 6 | `client_version` | `uint32` | `optional` | `` |  |
| 7 | `lobby_details` | `.CMsgPracticeLobbySetDetails` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPracticeLobbySetTeamSlot</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team` | `.DOTA_GC_TEAM` | `optional` | `` | default = DOTA_GC_TEAM_GOOD_GUYS |
| 2 | `slot` | `uint32` | `optional` | `` |  |
| 3 | `bot_difficulty` | `.DOTABotDifficulty` | `optional` | `` | default = BOT_DIFFICULTY_PASSIVE |

</details>

<details>
<summary><code>CMsgPracticeLobbySetCoach</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team` | `.DOTA_GC_TEAM` | `optional` | `` | default = DOTA_GC_TEAM_GOOD_GUYS |

</details>

<details>
<summary><code>CMsgPracticeLobbyJoinBroadcastChannel</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `channel` | `uint32` | `optional` | `` |  |
| 2 | `preferred_description` | `string` | `optional` | `` |  |
| 3 | `preferred_country_code` | `string` | `optional` | `` |  |
| 4 | `preferred_language_code` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPracticeLobbyCloseBroadcastChannel</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `channel` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPracticeLobbyToggleBroadcastChannelCameramanStatus</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgPracticeLobbyKick</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 3 | `account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPracticeLobbyKickFromTeam</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPracticeLobbyLeave</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgPracticeLobbyLaunch</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 5 | `client_version` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgApplyTeamToPracticeLobby</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPracticeLobbyList</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `pass_key` | `string` | `optional` | `` |  |
| 3 | `region` | `uint32` | `optional` | `` |  |
| 4 | `game_mode` | `.DOTA_GameMode` | `optional` | `` | default = DOTA_GAMEMODE_NONE |

</details>

<details>
<summary><code>CMsgPracticeLobbyListResponseEntry</code> — fields: 16; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `id` | `uint64` | `optional` | `` | (key_field) = true |
| 5 | `members` | `.CMsgPracticeLobbyListResponseEntry.CLobbyMember` | `repeated` | `` |  |
| 6 | `requires_pass_key` | `bool` | `optional` | `` |  |
| 7 | `leader_account_id` | `uint32` | `optional` | `` |  |
| 10 | `name` | `string` | `optional` | `` |  |
| 11 | `custom_game_mode` | `string` | `optional` | `` |  |
| 12 | `game_mode` | `.DOTA_GameMode` | `optional` | `` | default = DOTA_GAMEMODE_NONE |
| 13 | `friend_present` | `bool` | `optional` | `` |  |
| 14 | `players` | `uint32` | `optional` | `` |  |
| 15 | `custom_map_name` | `string` | `optional` | `` |  |
| 16 | `max_player_count` | `uint32` | `optional` | `` |  |
| 17 | `server_region` | `uint32` | `optional` | `` |  |
| 19 | `league_id` | `uint32` | `optional` | `` |  |
| 20 | `lan_host_ping_location` | `string` | `optional` | `` |  |
| 21 | `min_player_count` | `uint32` | `optional` | `` |  |
| 22 | `penalties_enabled` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPracticeLobbyListResponseEntry.CLobbyMember</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgPracticeLobbyListResponseEntry`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `player_name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPracticeLobbyListResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `lobbies` | `.CMsgPracticeLobbyListResponseEntry` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgLobbyList</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `server_region` | `uint32` | `optional` | `` | default = 0 |
| 2 | `game_mode` | `.DOTA_GameMode` | `optional` | `` | default = DOTA_GAMEMODE_NONE |

</details>

<details>
<summary><code>CMsgLobbyListResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `lobbies` | `.CMsgPracticeLobbyListResponseEntry` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgPracticeLobbyJoin</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `lobby_id` | `uint64` | `optional` | `` |  |
| 2 | `client_version` | `uint32` | `optional` | `` |  |
| 3 | `pass_key` | `string` | `optional` | `` |  |
| 4 | `custom_game_crc` | `fixed64` | `optional` | `` |  |
| 5 | `custom_game_timestamp` | `fixed32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPracticeLobbyJoinResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.DOTAJoinLobbyResult` | `optional` | `` | default = DOTA_JOIN_RESULT_SUCCESS |

</details>

<details>
<summary><code>CMsgFriendPracticeLobbyListRequest</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `friends` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgFriendPracticeLobbyListResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `lobbies` | `.CMsgPracticeLobbyListResponseEntry` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgJoinableCustomGameModesRequest</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `server_region` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgJoinableCustomGameModesResponseEntry</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `custom_game_id` | `uint64` | `optional` | `` |  |
| 2 | `lobby_count` | `uint32` | `optional` | `` |  |
| 3 | `player_count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgJoinableCustomGameModesResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `game_modes` | `.CMsgJoinableCustomGameModesResponseEntry` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgJoinableCustomLobbiesRequest</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `server_region` | `uint32` | `optional` | `` |  |
| 2 | `custom_game_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgJoinableCustomLobbiesResponseEntry</code> — fields: 16; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `lobby_id` | `fixed64` | `optional` | `` |  |
| 2 | `custom_game_id` | `uint64` | `optional` | `` |  |
| 3 | `lobby_name` | `string` | `optional` | `` |  |
| 4 | `member_count` | `uint32` | `optional` | `` |  |
| 5 | `leader_account_id` | `uint32` | `optional` | `` |  |
| 6 | `leader_name` | `string` | `optional` | `` |  |
| 7 | `custom_map_name` | `string` | `optional` | `` |  |
| 8 | `max_player_count` | `uint32` | `optional` | `` |  |
| 9 | `server_region` | `uint32` | `optional` | `` |  |
| 11 | `has_pass_key` | `bool` | `optional` | `` |  |
| 12 | `lan_host_ping_location` | `string` | `optional` | `` |  |
| 13 | `lobby_creation_time` | `uint32` | `optional` | `` |  |
| 14 | `custom_game_timestamp` | `uint32` | `optional` | `` |  |
| 15 | `custom_game_crc` | `uint64` | `optional` | `` |  |
| 16 | `min_player_count` | `uint32` | `optional` | `` |  |
| 17 | `penalties_enabled` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgJoinableCustomLobbiesResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `lobbies` | `.CMsgJoinableCustomLobbiesResponseEntry` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgQuickJoinCustomLobby</code> — fields: 7; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `legacy_server_region` | `uint32` | `optional` | `` |  |
| 2 | `custom_game_id` | `uint64` | `optional` | `` |  |
| 3 | `client_version` | `uint32` | `optional` | `` |  |
| 4 | `create_lobby_details` | `.CMsgPracticeLobbySetDetails` | `optional` | `` |  |
| 5 | `allow_any_map` | `bool` | `optional` | `` |  |
| 6 | `legacy_region_pings` | `.CMsgQuickJoinCustomLobby.LegacyRegionPing` | `repeated` | `` |  |
| 7 | `ping_data` | `.CMsgClientPingData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgQuickJoinCustomLobby.LegacyRegionPing</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgQuickJoinCustomLobby`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `server_region` | `uint32` | `optional` | `` |  |
| 2 | `ping` | `uint32` | `optional` | `` |  |
| 3 | `region_code` | `fixed32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgQuickJoinCustomLobbyResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.DOTAJoinLobbyResult` | `optional` | `` | default = DOTA_JOIN_RESULT_SUCCESS |

</details>

<details>
<summary><code>CMsgBotGameCreate</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `search_key` | `string` | `optional` | `` |  |
| 2 | `client_version` | `uint32` | `optional` | `` |  |
| 3 | `difficulty_radiant` | `.DOTABotDifficulty` | `optional` | `` | default = BOT_DIFFICULTY_PASSIVE |
| 4 | `team` | `.DOTA_GC_TEAM` | `optional` | `` | default = DOTA_GC_TEAM_GOOD_GUYS |
| 5 | `game_mode` | `uint32` | `optional` | `` |  |
| 6 | `difficulty_dire` | `.DOTABotDifficulty` | `optional` | `` | default = BOT_DIFFICULTY_PASSIVE |

</details>

<details>
<summary><code>CMsgDOTAPartyMemberSetCoach</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `wants_coach` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTASetGroupLeader</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `new_leader_steamid` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTACancelGroupInvites</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `invited_steamids` | `fixed64` | `repeated` | `` |  |
| 2 | `invited_groupids` | `fixed64` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTASetGroupOpenStatus</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `open` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAGroupMergeInvite</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `other_group_id` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAGroupMergeResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `initiator_group_id` | `fixed64` | `optional` | `` |  |
| 2 | `accept` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAGroupMergeReply</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.EDOTAGroupMergeResult` | `optional` | `` | default = k_EDOTAGroupMergeResult_OK |

</details>

<details>
<summary><code>CMsgSpectatorLobbyGameDetails</code> — fields: 10; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `language` | `uint32` | `optional` | `` |  |
| 2 | `match_id` | `uint64` | `optional` | `` |  |
| 3 | `server_steam_id` | `fixed64` | `optional` | `` |  |
| 4 | `stream_url` | `string` | `optional` | `` |  |
| 5 | `stream_name` | `string` | `optional` | `` |  |
| 6 | `league_id` | `uint32` | `optional` | `` |  |
| 7 | `series_type` | `uint32` | `optional` | `` |  |
| 8 | `series_game` | `uint32` | `optional` | `` |  |
| 9 | `radiant_team` | `.CMsgSpectatorLobbyGameDetails.Team` | `optional` | `` |  |
| 10 | `dire_team` | `.CMsgSpectatorLobbyGameDetails.Team` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSpectatorLobbyGameDetails.Team</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSpectatorLobbyGameDetails`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team_id` | `uint32` | `optional` | `` |  |
| 2 | `team_name` | `string` | `optional` | `` |  |
| 3 | `team_logo` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSetSpectatorLobbyDetails</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `lobby_id` | `uint64` | `optional` | `` |  |
| 2 | `lobby_name` | `string` | `optional` | `` |  |
| 3 | `pass_key` | `string` | `optional` | `` |  |
| 4 | `game_details` | `.CMsgSpectatorLobbyGameDetails` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgCreateSpectatorLobby</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `client_version` | `uint32` | `optional` | `` |  |
| 2 | `details` | `.CMsgSetSpectatorLobbyDetails` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSpectatorLobbyList</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgSpectatorLobbyListResponse</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `lobbies` | `.CMsgSpectatorLobbyListResponse.SpectatorLobby` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSpectatorLobbyListResponse.SpectatorLobby</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSpectatorLobbyListResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `lobby_id` | `uint64` | `optional` | `` |  |
| 2 | `game_name` | `string` | `optional` | `` |  |
| 3 | `requires_pass_key` | `bool` | `optional` | `` |  |
| 4 | `leader_account_id` | `uint32` | `optional` | `` |  |
| 5 | `member_count` | `uint32` | `optional` | `` |  |
| 7 | `game_details` | `.CMsgSpectatorLobbyGameDetails` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestSteamDatagramTicket</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `server_steam_id` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestSteamDatagramTicketResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `serialized_ticket` | `bytes` | `optional` | `` |  |
| 2 | `message` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientSteamDatagramTicket</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `legacy_time_expiry` | `fixed32` | `optional` | `` |  |
| 2 | `legacy_authorized_steam_id` | `fixed64` | `optional` | `` |  |
| 3 | `legacy_authorized_public_ip` | `fixed32` | `optional` | `` |  |
| 4 | `legacy_gameserver_steam_id` | `fixed64` | `optional` | `` |  |
| 5 | `legacy_gameserver_net_id` | `fixed64` | `optional` | `` |  |
| 6 | `legacy_signature` | `bytes` | `optional` | `` |  |
| 7 | `legacy_app_id` | `uint32` | `optional` | `` |  |
| 8 | `legacy_extra_fields` | `bytes` | `repeated` | `` |  |
| 16 | `serialized_ticket` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientRequestLaneSelection</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgGCToClientRequestLaneSelectionResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `lane_selection_flags` | `uint32` | `optional` | `` |  |
| 2 | `high_priority_disabled` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientRequestMMInfo</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCMMInfo</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `lane_selection_flags` | `uint32` | `optional` | `` |  |
| 2 | `high_priority_disabled` | `bool` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>EStartFindingMatchResult</code> — values: 41</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EStartFindingMatchResult_Invalid` | 0 |
| `k_EStartFindingMatchResult_OK` | 1 |
| `k_EStartFindingMatchResult_AlreadySearching` | 2 |
| `k_EStartFindingMatchResult_FailGeneric` | 100 |
| `k_EStartFindingMatchResult_FailedIgnore` | 101 |
| `k_EStartFindingMatchResult_MatchmakingDisabled` | 102 |
| `k_EStartFindingMatchResult_RegionOffline` | 103 |
| `k_EStartFindingMatchResult_MatchmakingCooldown` | 104 |
| `k_EStartFindingMatchResult_ClientOutOfDate` | 105 |
| `k_EStartFindingMatchResult_CompetitiveNoLowPriority` | 106 |
| `k_EStartFindingMatchResult_CompetitiveNotUnlocked` | 107 |
| `k_EStartFindingMatchResult_GameModeNotUnlocked` | 108 |
| `k_EStartFindingMatchResult_CompetitiveNotEnoughPlayTime` | 109 |
| `k_EStartFindingMatchResult_MissingInitialSkill` | 110 |
| `k_EStartFindingMatchResult_CompetitiveRankSpreadTooLarge` | 111 |
| `k_EStartFindingMatchResult_MemberAlreadyInLobby` | 112 |
| `k_EStartFindingMatchResult_MemberNotVACVerified` | 113 |
| `k_EStartFindingMatchResult_WeekendTourneyBadPartySize` | 114 |
| `k_EStartFindingMatchResult_WeekendTourneyTeamBuyInTooSmall` | 115 |
| `k_EStartFindingMatchResult_WeekendTourneyIndividualBuyInTooLarge` | 116 |
| `k_EStartFindingMatchResult_WeekendTourneyTeamBuyInTooLarge` | 117 |
| `k_EStartFindingMatchResult_MemberMissingEventOwnership` | 118 |
| `k_EStartFindingMatchResult_WeekendTourneyNotUnlocked` | 119 |
| `k_EStartFindingMatchResult_WeekendTourneyRecentParticipation` | 120 |
| `k_EStartFindingMatchResult_MemberMissingAnchoredPhoneNumber` | 121 |
| `k_EStartFindingMatchResult_NotMemberOfClan` | 122 |
| `k_EStartFindingMatchResult_CoachesChallengeBadPartySize` | 123 |
| `k_EStartFindingMatchResult_CoachesChallengeRequirementsNotMet` | 124 |
| `k_EStartFindingMatchResult_InvalidRoleSelections` | 125 |
| `k_EStartFindingMatchResult_PhoneNumberDiscrepancy` | 126 |
| `k_EStartFindingMatchResult_NoQueuePoints` | 127 |
| `k_EStartFindingMatchResult_MemberMissingGauntletFlag` | 128 |
| `k_EStartFindingMatchResult_MemberGauntletTooRecent` | 129 |
| `k_EStartFindingMatchResult_DifficultyNotUnlocked` | 130 |
| `k_EStartFindingMatchResult_CoachesNotAllowedInParty` | 131 |
| `k_EStartFindingMatchResult_MatchmakingBusy` | 132 |
| `k_EStartFindingMatchResult_SteamChinaBanned` | 133 |
| `k_EStartFindingMatchResult_SteamChinaInvalidMixedParty` | 134 |
| `k_EStartFindingMatchResult_RestrictedFromRanked` | 135 |
| `k_EStartFindingMatchResult_RankPreventsParties` | 136 |
| `k_EStartFindingMatchResult_RegisteredNameRequired` | 137 |

</details>
