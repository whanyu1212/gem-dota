# dota_gcmessages_client.proto

- Module: `dota_gcmessages_client_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **10**
- Messages: **475** (top-level: 379)
- Enums: **86** (top-level: 11)

## Imports

- `steammessages.proto`
- `dota_shared_enums.proto`
- `dota_gcmessages_common.proto`
- `dota_gcmessages_webapi.proto`
- `gcsdk_gcmessages.proto`
- `dota_gcmessages_common_lobby.proto`
- `dota_gcmessages_common_match_management.proto`
- `base_gcmessages.proto`
- `econ_gcmessages.proto`
- `valveextensions.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgClientSuspended</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `time_end` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgBalancedShuffleLobby</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgInitialQuestionnaireResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `initial_skill` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTARequestMatchesResponse</code> — fields: 5; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `matches` | `.CMsgDOTAMatch` | `repeated` | `` |  |
| 2 | `series` | `.CMsgDOTARequestMatchesResponse.Series` | `repeated` | `` |  |
| 3 | `request_id` | `uint32` | `optional` | `` |  |
| 4 | `total_results` | `uint32` | `optional` | `` |  |
| 5 | `results_remaining` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTARequestMatchesResponse.Series</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTARequestMatchesResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `matches` | `.CMsgDOTAMatch` | `repeated` | `` |  |
| 2 | `series_id` | `uint32` | `optional` | `` |  |
| 3 | `series_type` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAPopup</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `id` | `.CMsgDOTAPopup.PopupID` | `optional` | `` | default = NONE |
| 2 | `custom_text` | `string` | `optional` | `` |  |
| 3 | `int_data` | `sint32` | `optional` | `` |  |
| 4 | `popup_data` | `bytes` | `optional` | `` |  |
| 5 | `loc_token_header` | `string` | `optional` | `` |  |
| 6 | `loc_token_msg` | `string` | `optional` | `` |  |
| 7 | `var_names` | `string` | `repeated` | `` |  |
| 8 | `var_values` | `string` | `repeated` | `` |  |
| 9 | `debug_text` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAReportsRemainingRequest</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgDOTAReportsRemainingResponse</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `num_positive_reports_remaining` | `uint32` | `optional` | `` |  |
| 2 | `num_negative_reports_remaining` | `uint32` | `optional` | `` |  |
| 3 | `num_positive_reports_total` | `uint32` | `optional` | `` |  |
| 4 | `num_negative_reports_total` | `uint32` | `optional` | `` |  |
| 5 | `num_comms_reports_remaining` | `uint32` | `optional` | `` |  |
| 6 | `num_comms_reports_total` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTASubmitPlayerReport</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_account_id` | `uint32` | `optional` | `` |  |
| 2 | `report_flags` | `uint32` | `optional` | `` |  |
| 4 | `lobby_id` | `uint64` | `optional` | `` |  |
| 5 | `comment` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTASubmitPlayerReportResponse</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_account_id` | `uint32` | `optional` | `` |  |
| 2 | `report_flags` | `uint32` | `optional` | `` |  |
| 4 | `debug_message` | `string` | `optional` | `` |  |
| 5 | `enum_result` | `.CMsgDOTASubmitPlayerReportResponse.EResult` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgDOTASubmitPlayerAvoidRequest</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_account_id` | `uint32` | `optional` | `` |  |
| 4 | `lobby_id` | `uint64` | `optional` | `` |  |
| 5 | `user_note` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTASubmitPlayerAvoidRequestResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_account_id` | `uint32` | `optional` | `` |  |
| 2 | `result` | `uint32` | `optional` | `` |  |
| 3 | `debug_message` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTASubmitPlayerReportV2</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_account_id` | `uint32` | `optional` | `` |  |
| 2 | `report_reason` | `uint32` | `repeated` | `` |  |
| 3 | `lobby_id` | `uint64` | `optional` | `` |  |
| 4 | `game_time` | `float` | `optional` | `` |  |
| 5 | `debug_slot` | `uint32` | `optional` | `` |  |
| 6 | `debug_match_id` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTASubmitPlayerReportResponseV2</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_account_id` | `uint32` | `optional` | `` |  |
| 2 | `report_reason` | `uint32` | `repeated` | `` |  |
| 4 | `debug_message` | `string` | `optional` | `` |  |
| 5 | `enum_result` | `.CMsgDOTASubmitPlayerReportResponseV2.EResult` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgDOTASubmitLobbyMVPVote</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTASubmitLobbyMVPVoteResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_account_id` | `uint32` | `optional` | `` |  |
| 2 | `eresult` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALobbyMVPAwarded</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `mvp_account_id` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAKickedFromMatchmakingQueue</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_type` | `.MatchType` | `optional` | `` | default = MATCH_TYPE_CASUAL |

</details>

<details>
<summary><code>CMsgGCMatchDetailsRequest</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCMatchDetailsResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `uint32` | `optional` | `` |  |
| 2 | `match` | `.CMsgDOTAMatch` | `optional` | `` |  |
| 3 | `vote` | `.DOTAMatchVote` | `optional` | `` | default = DOTAMatchVote_INVALID |

</details>

<details>
<summary><code>CMsgDOTAProfileTickets</code> — fields: 3; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `uint32` | `optional` | `` |  |
| 2 | `account_id` | `uint32` | `optional` | `` |  |
| 3 | `league_passes` | `.CMsgDOTAProfileTickets.LeaguePass` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAProfileTickets.LeaguePass</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAProfileTickets`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_id` | `uint32` | `optional` | `` |  |
| 2 | `item_def` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetProfileTickets</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientPartySearchInvites</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `invites` | `.CMsgGCToClientPartySearchInvite` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAWelcome</code> — fields: 19; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 5 | `store_item_hash` | `uint32` | `optional` | `` |  |
| 6 | `timeplayedconsecutively` | `uint32` | `optional` | `` |  |
| 7 | `allow_3rd_party_match_history` | `bool` | `optional` | `` |  |
| 13 | `last_ip_address` | `uint32` | `optional` | `` |  |
| 17 | `profile_private` | `bool` | `optional` | `` |  |
| 18 | `currency` | `uint32` | `optional` | `` |  |
| 20 | `should_request_player_origin` | `bool` | `optional` | `` |  |
| 22 | `gc_socache_file_version` | `uint32` | `optional` | `` |  |
| 24 | `is_perfect_world_test_account` | `bool` | `optional` | `` |  |
| 26 | `extra_messages` | `.CMsgDOTAWelcome.CExtraMsg` | `repeated` | `` |  |
| 27 | `minimum_recent_item_id` | `uint64` | `optional` | `` |  |
| 28 | `active_event` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 29 | `additional_user_message` | `uint32` | `optional` | `` |  |
| 30 | `custom_game_whitelist_version` | `uint32` | `optional` | `` |  |
| 31 | `party_search_friend_invites` | `.CMsgGCToClientPartySearchInvites` | `optional` | `` |  |
| 32 | `remaining_playtime` | `int32` | `optional` | `` | default = -1 |
| 33 | `disable_guild_persona_info` | `bool` | `optional` | `` |  |
| 34 | `extra_message_blocks` | `.CExtraMsgBlock` | `repeated` | `` |  |
| 35 | `active_event_for_display` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |

</details>

<details>
<summary><code>CMsgDOTAWelcome.CExtraMsg</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAWelcome`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `id` | `uint32` | `optional` | `` |  |
| 2 | `contents` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CSODOTAGameHeroFavorites</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` | (key_field) = true |
| 2 | `hero_id` | `int32` | `optional` | `` | (key_field) = true |

</details>

<details>
<summary><code>CMsgDOTAMatchVotes</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `votes` | `.CMsgDOTAMatchVotes.PlayerVote` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAMatchVotes.PlayerVote</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAMatchVotes`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `vote` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgMatchmakingMatchGroupInfo</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `players_searching` | `uint32` | `optional` | `` |  |
| 2 | `auto_region_select_ping_penalty` | `sint32` | `optional` | `` |  |
| 3 | `status` | `.EMatchGroupServerStatus` | `optional` | `` | default = k_EMatchGroupServerStatus_OK |
| 4 | `auto_region_select_ping_penalty_custom` | `sint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAMatchmakingStatsRequest</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgDOTAMatchmakingStatsResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `matchgroups_version` | `uint32` | `optional` | `` |  |
| 7 | `legacy_searching_players_by_group_source2` | `uint32` | `repeated` | `` |  |
| 8 | `match_groups` | `.CMsgMatchmakingMatchGroupInfo` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAUpdateMatchmakingStats</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `stats` | `.CMsgDOTAMatchmakingStatsResponse` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAUpdateMatchManagementStats</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `stats` | `.CMsgDOTAMatchmakingStatsResponse` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTASetMatchHistoryAccess</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `allow_3rd_party_match_history` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTASetMatchHistoryAccessResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `eresult` | `uint32` | `optional` | `` | default = 2 |

</details>

<details>
<summary><code>CMsgDOTANotifyAccountFlagsChange</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `accountid` | `uint32` | `optional` | `` |  |
| 2 | `account_flags` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTASetProfilePrivacy</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `profile_private` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTASetProfilePrivacyResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `eresult` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgUpgradeLeagueItem</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `league_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgUpgradeLeagueItemResponse</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgGCWatchDownloadedReplay</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `watch_type` | `.DOTA_WatchReplayType` | `optional` | `` | default = DOTA_WATCH_REPLAY_NORMAL |

</details>

<details>
<summary><code>CMsgClientToGCWatchingBroadcast</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientsRejoinChatChannels</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgGCGetHeroStandings</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgGCGetHeroStandingsResponse</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `standings` | `.CMsgGCGetHeroStandingsResponse.Hero` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCGetHeroStandingsResponse.Hero</code> — fields: 27; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCGetHeroStandingsResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `wins` | `uint32` | `optional` | `` |  |
| 3 | `losses` | `uint32` | `optional` | `` |  |
| 4 | `win_streak` | `uint32` | `optional` | `` |  |
| 5 | `best_win_streak` | `uint32` | `optional` | `` |  |
| 6 | `avg_kills` | `float` | `optional` | `` |  |
| 7 | `avg_deaths` | `float` | `optional` | `` |  |
| 8 | `avg_assists` | `float` | `optional` | `` |  |
| 9 | `avg_gpm` | `float` | `optional` | `` |  |
| 10 | `avg_xpm` | `float` | `optional` | `` |  |
| 11 | `best_kills` | `uint32` | `optional` | `` |  |
| 12 | `best_assists` | `uint32` | `optional` | `` |  |
| 13 | `best_gpm` | `uint32` | `optional` | `` |  |
| 14 | `best_xpm` | `uint32` | `optional` | `` |  |
| 15 | `performance` | `float` | `optional` | `` |  |
| 16 | `wins_with_ally` | `uint32` | `optional` | `` |  |
| 17 | `losses_with_ally` | `uint32` | `optional` | `` |  |
| 18 | `wins_against_enemy` | `uint32` | `optional` | `` |  |
| 19 | `losses_against_enemy` | `uint32` | `optional` | `` |  |
| 20 | `networth_peak` | `uint32` | `optional` | `` |  |
| 21 | `lasthit_peak` | `uint32` | `optional` | `` |  |
| 22 | `deny_peak` | `uint32` | `optional` | `` |  |
| 23 | `damage_peak` | `uint32` | `optional` | `` |  |
| 24 | `longest_game_peak` | `uint32` | `optional` | `` |  |
| 25 | `healing_peak` | `uint32` | `optional` | `` |  |
| 26 | `avg_lasthits` | `float` | `optional` | `` |  |
| 27 | `avg_denies` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMatchPlayerTimedStatAverages</code> — fields: 13; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `kills` | `float` | `optional` | `` |  |
| 3 | `deaths` | `float` | `optional` | `` |  |
| 4 | `assists` | `float` | `optional` | `` |  |
| 5 | `net_worth` | `float` | `optional` | `` |  |
| 6 | `last_hits` | `float` | `optional` | `` |  |
| 7 | `denies` | `float` | `optional` | `` |  |
| 8 | `item_value` | `float` | `optional` | `` |  |
| 9 | `support_gold_spent` | `float` | `optional` | `` |  |
| 10 | `camps_stacked` | `float` | `optional` | `` |  |
| 11 | `wards_placed` | `float` | `optional` | `` |  |
| 12 | `dewards` | `float` | `optional` | `` |  |
| 13 | `triple_kills` | `float` | `optional` | `` |  |
| 14 | `rampages` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMatchPlayerTimedStatStdDeviations</code> — fields: 13; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `kills` | `float` | `optional` | `` | default = 1 |
| 3 | `deaths` | `float` | `optional` | `` | default = 1 |
| 4 | `assists` | `float` | `optional` | `` | default = 1 |
| 5 | `net_worth` | `float` | `optional` | `` | default = 1 |
| 6 | `last_hits` | `float` | `optional` | `` | default = 1 |
| 7 | `denies` | `float` | `optional` | `` | default = 1 |
| 8 | `item_value` | `float` | `optional` | `` | default = 1 |
| 9 | `support_gold_spent` | `float` | `optional` | `` | default = 1 |
| 10 | `camps_stacked` | `float` | `optional` | `` | default = 1 |
| 11 | `wards_placed` | `float` | `optional` | `` | default = 1 |
| 12 | `dewards` | `float` | `optional` | `` | default = 1 |
| 13 | `triple_kills` | `float` | `optional` | `` | default = 1 |
| 14 | `rampages` | `float` | `optional` | `` | default = 1 |

</details>

<details>
<summary><code>CMsgGCGetHeroTimedStatsResponse</code> — fields: 2; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `rank_chunked_stats` | `.CMsgGCGetHeroTimedStatsResponse.RankChunkedStats` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCGetHeroTimedStatsResponse.TimedStatsContainer</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCGetHeroTimedStatsResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `time` | `uint32` | `optional` | `` |  |
| 2 | `all_stats` | `.CMatchPlayerTimedStatAverages` | `optional` | `` |  |
| 3 | `winning_stats` | `.CMatchPlayerTimedStatAverages` | `optional` | `` |  |
| 4 | `losing_stats` | `.CMatchPlayerTimedStatAverages` | `optional` | `` |  |
| 5 | `winning_stddevs` | `.CMatchPlayerTimedStatStdDeviations` | `optional` | `` |  |
| 6 | `losing_stddevs` | `.CMatchPlayerTimedStatStdDeviations` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCGetHeroTimedStatsResponse.RankChunkedStats</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCGetHeroTimedStatsResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `rank_chunk` | `uint32` | `optional` | `` |  |
| 2 | `timed_stats` | `.CMsgGCGetHeroTimedStatsResponse.TimedStatsContainer` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCItemEditorReservationsRequest</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgGCItemEditorReservation</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `def_index` | `uint32` | `optional` | `` |  |
| 2 | `name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCItemEditorReservationsResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `reservations` | `.CMsgGCItemEditorReservation` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCItemEditorReserveItemDef</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `def_index` | `uint32` | `optional` | `` |  |
| 2 | `username` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCItemEditorReserveItemDefResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `def_index` | `uint32` | `optional` | `` |  |
| 2 | `username` | `string` | `optional` | `` |  |
| 3 | `result` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCItemEditorReleaseReservation</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `def_index` | `uint32` | `optional` | `` |  |
| 2 | `username` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCItemEditorReleaseReservationResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `def_index` | `uint32` | `optional` | `` |  |
| 2 | `released` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgFlipLobbyTeams</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgGCLobbyUpdateBroadcastChannelInfo</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `channel_id` | `uint32` | `optional` | `` |  |
| 2 | `country_code` | `string` | `optional` | `` |  |
| 3 | `description` | `string` | `optional` | `` |  |
| 4 | `language_code` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAClaimEventActionData</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 4 | `grant_item_gift_data` | `.CMsgDOTAClaimEventActionData.GrantItemGiftData` | `optional` | `` |  |
| 5 | `grant_item_choice_item_def` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAClaimEventActionData.GrantItemGiftData</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAClaimEventActionData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `give_to_account_id` | `uint32` | `optional` | `` |  |
| 2 | `gift_message` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAClaimEventAction</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |
| 2 | `action_id` | `uint32` | `optional` | `` |  |
| 3 | `quantity` | `uint32` | `optional` | `` |  |
| 4 | `data` | `.CMsgDOTAClaimEventActionData` | `optional` | `` |  |
| 5 | `score_mode` | `.EEventActionScoreMode` | `optional` | `` | default = k_eEventActionScoreMode_Add |
| 6 | `suppress_rewards` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCClaimEventActionUsingItem</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |
| 2 | `action_id` | `uint32` | `optional` | `` |  |
| 3 | `item_id` | `uint64` | `optional` | `` |  |
| 4 | `quantity` | `uint32` | `optional` | `` |  |
| 5 | `suppress_rewards` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCClaimEventActionUsingItemResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `action_results` | `.CMsgDOTAClaimEventActionResponse` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientClaimEventActionUsingItemCompleted</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_id` | `uint64` | `optional` | `` |  |
| 2 | `action_results` | `.CMsgDOTAClaimEventActionResponse` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAGetEventPoints</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |
| 2 | `account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAGetEventPointsResponse</code> — fields: 10; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `total_points` | `uint32` | `optional` | `` |  |
| 2 | `total_premium_points` | `uint32` | `optional` | `` |  |
| 3 | `event_id` | `uint32` | `optional` | `` |  |
| 4 | `points` | `uint32` | `optional` | `` |  |
| 5 | `premium_points` | `uint32` | `optional` | `` |  |
| 6 | `completed_actions` | `.CMsgDOTAGetEventPointsResponse.Action` | `repeated` | `` |  |
| 7 | `account_id` | `uint32` | `optional` | `` |  |
| 8 | `owned` | `bool` | `optional` | `` |  |
| 9 | `audit_action` | `uint32` | `optional` | `` |  |
| 10 | `active_season_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAGetEventPointsResponse.Action</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAGetEventPointsResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `action_id` | `uint32` | `optional` | `` |  |
| 2 | `times_completed` | `uint32` | `optional` | `` | default = 1 |

</details>

<details>
<summary><code>CMsgDOTAGetPeriodicResource</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `periodic_resource_id` | `uint32` | `optional` | `` |  |
| 3 | `timestamp` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAGetPeriodicResourceResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `periodic_resource_max` | `uint32` | `optional` | `` |  |
| 2 | `periodic_resource_used` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAPeriodicResourceUpdated</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `periodic_resource_key` | `.CMsgDOTAGetPeriodicResource` | `optional` | `` |  |
| 2 | `periodic_resource_value` | `.CMsgDOTAGetPeriodicResourceResponse` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTACompendiumSelection</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `selection_index` | `uint32` | `optional` | `` |  |
| 2 | `selection` | `uint32` | `optional` | `` |  |
| 3 | `leagueid` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTACompendiumSelectionResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `eresult` | `uint32` | `optional` | `` | default = 2 |

</details>

<details>
<summary><code>CMsgDOTACompendiumRemoveAllSelections</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `leagueid` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTACompendiumRemoveAllSelectionsResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `eresult` | `uint32` | `optional` | `` | default = 2 |

</details>

<details>
<summary><code>CMsgDOTACompendiumData</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `selections` | `.CMsgDOTACompendiumSelection` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTACompendiumDataRequest</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `leagueid` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTACompendiumDataResponse</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `leagueid` | `uint32` | `optional` | `` |  |
| 3 | `result` | `uint32` | `optional` | `` | default = 2 |
| 4 | `compendium_data` | `.CMsgDOTACompendiumData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAGetPlayerMatchHistory</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `start_at_match_id` | `uint64` | `optional` | `` |  |
| 3 | `matches_requested` | `uint32` | `optional` | `` |  |
| 4 | `hero_id` | `int32` | `optional` | `` |  |
| 5 | `request_id` | `uint32` | `optional` | `` |  |
| 7 | `include_practice_matches` | `bool` | `optional` | `` |  |
| 8 | `include_custom_games` | `bool` | `optional` | `` |  |
| 9 | `include_event_games` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAGetPlayerMatchHistoryResponse</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `matches` | `.CMsgDOTAGetPlayerMatchHistoryResponse.Match` | `repeated` | `` |  |
| 2 | `request_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAGetPlayerMatchHistoryResponse.Match</code> — fields: 22; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAGetPlayerMatchHistoryResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `start_time` | `uint32` | `optional` | `` |  |
| 3 | `hero_id` | `int32` | `optional` | `` |  |
| 4 | `winner` | `bool` | `optional` | `` |  |
| 5 | `game_mode` | `uint32` | `optional` | `` |  |
| 6 | `rank_change` | `int32` | `optional` | `` |  |
| 7 | `previous_rank` | `uint32` | `optional` | `` |  |
| 8 | `lobby_type` | `uint32` | `optional` | `` |  |
| 9 | `solo_rank` | `bool` | `optional` | `` |  |
| 10 | `abandon` | `bool` | `optional` | `` |  |
| 11 | `duration` | `uint32` | `optional` | `` |  |
| 12 | `engine` | `uint32` | `optional` | `` |  |
| 13 | `active_plus_subscription` | `bool` | `optional` | `` |  |
| 14 | `seasonal_rank` | `bool` | `optional` | `` |  |
| 15 | `tourney_id` | `uint32` | `optional` | `` |  |
| 16 | `tourney_round` | `uint32` | `optional` | `` |  |
| 17 | `tourney_tier` | `uint32` | `optional` | `` |  |
| 18 | `tourney_division` | `uint32` | `optional` | `` |  |
| 19 | `team_id` | `uint32` | `optional` | `` |  |
| 20 | `team_name` | `string` | `optional` | `` |  |
| 21 | `ugc_team_ui_logo` | `uint64` | `optional` | `` |  |
| 22 | `selected_facet` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCNotificationsRequest</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgGCNotifications_Notification</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `id` | `uint64` | `optional` | `` |  |
| 2 | `type` | `uint32` | `optional` | `` |  |
| 3 | `timestamp` | `uint32` | `optional` | `` |  |
| 4 | `reference_a` | `uint32` | `optional` | `` |  |
| 5 | `reference_b` | `uint32` | `optional` | `` |  |
| 6 | `reference_c` | `uint32` | `optional` | `` |  |
| 7 | `message` | `string` | `optional` | `` |  |
| 8 | `unread` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCNotificationsUpdate</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgGCNotificationsUpdate.EResult` | `optional` | `` | default = SUCCESS |
| 2 | `notifications` | `.CMsgGCNotifications_Notification` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCNotificationsResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `update` | `.CMsgGCNotificationsUpdate` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCNotificationsMarkReadRequest</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgGCPlayerInfoSubmit</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_name` | `string` | `optional` | `` |  |
| 2 | `country_code` | `string` | `optional` | `` |  |
| 3 | `fantasy_role` | `uint32` | `optional` | `` |  |
| 4 | `team_id` | `uint32` | `optional` | `` |  |
| 5 | `sponsor` | `string` | `optional` | `` |  |
| 6 | `accepted_pro_agreement` | `bool` | `optional` | `` |  |
| 7 | `registration_period` | `uint32` | `optional` | `` |  |
| 8 | `real_name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCPlayerInfoSubmitResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgGCPlayerInfoSubmitResponse.EResult` | `optional` | `` | default = SUCCESS |

</details>

<details>
<summary><code>CMsgDOTAEmoticonAccessSDO</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `unlocked_emoticons` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCEmoticonDataRequest</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgGCToClientEmoticonData</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `emoticon_access` | `.CMsgDOTAEmoticonAccessSDO` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientTournamentItemDrop</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_def` | `uint32` | `optional` | `` |  |
| 2 | `event_type` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetAllHeroOrder</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCGetAllHeroOrderResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_ids` | `int32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetAllHeroProgress</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetAllHeroProgressResponse</code> — fields: 20; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `curr_hero_id` | `int32` | `optional` | `` |  |
| 3 | `laps_completed` | `uint32` | `optional` | `` |  |
| 4 | `curr_hero_games` | `uint32` | `optional` | `` |  |
| 5 | `curr_lap_time_started` | `uint32` | `optional` | `` |  |
| 6 | `curr_lap_games` | `uint32` | `optional` | `` |  |
| 7 | `best_lap_games` | `uint32` | `optional` | `` |  |
| 8 | `best_lap_time` | `uint32` | `optional` | `` |  |
| 9 | `lap_heroes_completed` | `uint32` | `optional` | `` |  |
| 10 | `lap_heroes_remaining` | `uint32` | `optional` | `` |  |
| 11 | `next_hero_id` | `int32` | `optional` | `` |  |
| 12 | `prev_hero_id` | `int32` | `optional` | `` |  |
| 13 | `prev_hero_games` | `uint32` | `optional` | `` |  |
| 14 | `prev_avg_tries` | `float` | `optional` | `` |  |
| 15 | `curr_avg_tries` | `float` | `optional` | `` |  |
| 16 | `next_avg_tries` | `float` | `optional` | `` |  |
| 17 | `full_lap_avg_tries` | `float` | `optional` | `` |  |
| 18 | `curr_lap_avg_tries` | `float` | `optional` | `` |  |
| 19 | `profile_name` | `string` | `optional` | `` |  |
| 20 | `start_hero_id` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetTrophyList</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetTrophyListResponse</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `trophies` | `.CMsgClientToGCGetTrophyListResponse.Trophy` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetTrophyListResponse.Trophy</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCGetTrophyListResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `trophy_id` | `uint32` | `optional` | `` |  |
| 2 | `trophy_score` | `uint32` | `optional` | `` |  |
| 3 | `last_updated` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientTrophyAwarded</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `trophy_id` | `uint32` | `optional` | `` |  |
| 2 | `trophy_score` | `uint32` | `optional` | `` |  |
| 3 | `trophy_old_score` | `uint32` | `optional` | `` |  |
| 4 | `last_updated` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRankRequest</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `rank_type` | `.ERankType` | `optional` | `` | default = k_ERankType_Invalid |

</details>

<details>
<summary><code>CMsgGCToClientRankResponse</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgGCToClientRankResponse.EResultCode` | `optional` | `` | default = k_Succeeded |
| 2 | `rank_value` | `uint32` | `optional` | `` |  |
| 3 | `rank_data1` | `uint32` | `optional` | `` |  |
| 4 | `rank_data2` | `uint32` | `optional` | `` |  |
| 5 | `rank_data3` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientRankUpdate</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `rank_type` | `.ERankType` | `optional` | `` | default = k_ERankType_Invalid |
| 2 | `rank_info` | `.CMsgGCToClientRankResponse` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetProfileCard</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCSetProfileCardSlots</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `slots` | `.CMsgClientToGCSetProfileCardSlots.CardSlot` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCSetProfileCardSlots.CardSlot</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCSetProfileCardSlots`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `slot_id` | `uint32` | `optional` | `` |  |
| 2 | `slot_type` | `.EProfileCardSlotType` | `optional` | `` | default = k_EProfileCardSlotType_Empty |
| 3 | `slot_value` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetProfileCardStats</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCCreateHeroStatue</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `source_item_id` | `uint64` | `optional` | `` |  |
| 3 | `hero_id` | `int32` | `optional` | `` |  |
| 4 | `sequence_name` | `string` | `optional` | `` |  |
| 5 | `cycle` | `float` | `optional` | `` |  |
| 6 | `wearables` | `uint32` | `repeated` | `` |  |
| 7 | `inscription` | `string` | `optional` | `` |  |
| 8 | `styles` | `uint32` | `repeated` | `` |  |
| 9 | `reforger_item_id` | `uint64` | `optional` | `` |  |
| 10 | `tournament_drop` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientHeroStatueCreateResult</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `resulting_item_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCPlayerStatsRequest</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientPlayerStatsResponse</code> — fields: 23; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `player_stats` | `float` | `repeated` | `` |  |
| 3 | `match_count` | `uint32` | `optional` | `` |  |
| 4 | `mean_gpm` | `float` | `optional` | `` |  |
| 5 | `mean_xppm` | `float` | `optional` | `` |  |
| 6 | `mean_lasthits` | `float` | `optional` | `` |  |
| 7 | `rampages` | `uint32` | `optional` | `` |  |
| 8 | `triple_kills` | `uint32` | `optional` | `` |  |
| 9 | `first_blood_claimed` | `uint32` | `optional` | `` |  |
| 10 | `first_blood_given` | `uint32` | `optional` | `` |  |
| 11 | `couriers_killed` | `uint32` | `optional` | `` |  |
| 12 | `aegises_snatched` | `uint32` | `optional` | `` |  |
| 13 | `cheeses_eaten` | `uint32` | `optional` | `` |  |
| 14 | `creeps_stacked` | `uint32` | `optional` | `` |  |
| 15 | `fight_score` | `float` | `optional` | `` |  |
| 16 | `farm_score` | `float` | `optional` | `` |  |
| 17 | `support_score` | `float` | `optional` | `` |  |
| 18 | `push_score` | `float` | `optional` | `` |  |
| 19 | `versatility_score` | `float` | `optional` | `` |  |
| 20 | `mean_networth` | `float` | `optional` | `` |  |
| 21 | `mean_damage` | `float` | `optional` | `` |  |
| 22 | `mean_heals` | `float` | `optional` | `` |  |
| 23 | `rapiers_purchased` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCustomGamesFriendsPlayedRequest</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgGCToClientCustomGamesFriendsPlayedResponse</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `games` | `.CMsgGCToClientCustomGamesFriendsPlayedResponse.CustomGame` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientCustomGamesFriendsPlayedResponse.CustomGame</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientCustomGamesFriendsPlayedResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `custom_game_id` | `uint64` | `optional` | `` |  |
| 2 | `account_ids` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCSocialFeedPostCommentRequest</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint64` | `optional` | `` |  |
| 2 | `comment` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientSocialFeedPostCommentResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `success` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCSocialFeedPostMessageRequest</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `message` | `string` | `optional` | `` |  |
| 2 | `match_id` | `uint64` | `optional` | `` |  |
| 3 | `match_timestamp` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientSocialFeedPostMessageResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `success` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCFriendsPlayedCustomGameRequest</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `custom_game_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientFriendsPlayedCustomGameResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `custom_game_id` | `uint64` | `optional` | `` |  |
| 2 | `account_ids` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAPartyRichPresence</code> — fields: 9; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `party_id` | `fixed64` | `optional` | `` |  |
| 2 | `party_state` | `.CSODOTAParty.State` | `optional` | `` | default = UI |
| 3 | `open` | `bool` | `optional` | `` |  |
| 4 | `members` | `.CMsgDOTAPartyRichPresence.Member` | `repeated` | `` |  |
| 5 | `low_priority` | `bool` | `optional` | `` |  |
| 6 | `weekend_tourney` | `.CMsgDOTAPartyRichPresence.WeekendTourney` | `optional` | `` |  |
| 7 | `team_id` | `uint32` | `optional` | `` |  |
| 8 | `team_name` | `string` | `optional` | `` |  |
| 9 | `ugc_team_ui_logo` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAPartyRichPresence.Member</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAPartyRichPresence`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steam_id` | `fixed64` | `optional` | `` |  |
| 2 | `coach` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAPartyRichPresence.WeekendTourney</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAPartyRichPresence`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `division` | `uint32` | `optional` | `` |  |
| 2 | `skill_level` | `uint32` | `optional` | `` |  |
| 3 | `round` | `uint32` | `optional` | `` |  |
| 4 | `tournament_id` | `uint32` | `optional` | `` |  |
| 5 | `state_seq_num` | `uint32` | `optional` | `` |  |
| 6 | `event` | `.EWeekendTourneyRichPresenceEvent` | `optional` | `` | default = k_EWeekendTourneyRichPresenceEvent_None |
| 7 | `event_round` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALobbyRichPresence</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `lobby_id` | `fixed64` | `optional` | `` |  |
| 2 | `lobby_state` | `.CSODOTALobby.State` | `optional` | `` | default = UI |
| 3 | `password` | `bool` | `optional` | `` |  |
| 4 | `game_mode` | `.DOTA_GameMode` | `optional` | `` | default = DOTA_GAMEMODE_NONE |
| 5 | `member_count` | `uint32` | `optional` | `` |  |
| 6 | `max_member_count` | `uint32` | `optional` | `` |  |
| 7 | `custom_game_id` | `fixed64` | `optional` | `` |  |
| 8 | `name` | `string` | `optional` | `` |  |
| 9 | `lobby_type` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTACustomGameListenServerStartedLoading</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `lobby_id` | `fixed64` | `optional` | `` |  |
| 2 | `custom_game_id` | `uint64` | `optional` | `` |  |
| 3 | `lobby_members` | `uint32` | `repeated` | `` |  |
| 4 | `start_time` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTACustomGameClientFinishedLoading</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `lobby_id` | `fixed64` | `optional` | `` |  |
| 2 | `loading_duration` | `uint32` | `optional` | `` |  |
| 3 | `result_code` | `sint32` | `optional` | `` |  |
| 4 | `result_string` | `string` | `optional` | `` |  |
| 5 | `signon_states` | `uint32` | `optional` | `` |  |
| 6 | `comment` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCApplyGemCombiner</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_id_1` | `uint64` | `optional` | `` |  |
| 2 | `item_id_2` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCH264Unsupported</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCGetQuestProgress</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `quest_ids` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetQuestProgressResponse</code> — fields: 2; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `success` | `bool` | `optional` | `` |  |
| 2 | `quests` | `.CMsgClientToGCGetQuestProgressResponse.Quest` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetQuestProgressResponse.Challenge</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCGetQuestProgressResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `challenge_id` | `uint32` | `optional` | `` |  |
| 2 | `time_completed` | `uint32` | `optional` | `` |  |
| 3 | `attempts` | `uint32` | `optional` | `` |  |
| 4 | `hero_id` | `int32` | `optional` | `` |  |
| 5 | `template_id` | `uint32` | `optional` | `` |  |
| 6 | `quest_rank` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetQuestProgressResponse.Quest</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCGetQuestProgressResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `quest_id` | `uint32` | `optional` | `` |  |
| 2 | `completed_challenges` | `.CMsgClientToGCGetQuestProgressResponse.Challenge` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientMatchSignedOut</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCGetHeroStatsHistory</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCGetHeroStatsHistoryResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `records` | `.CMsgDOTASDOHeroStatsHistory` | `repeated` | `` |  |
| 3 | `result` | `.CMsgGCGetHeroStatsHistoryResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgPlayerConductScorecardRequest</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgPlayerConductScorecard</code> — fields: 17; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `match_id` | `uint64` | `optional` | `` |  |
| 3 | `seq_num` | `uint32` | `optional` | `` |  |
| 4 | `reasons` | `uint32` | `optional` | `` |  |
| 5 | `matches_in_report` | `uint32` | `optional` | `` |  |
| 6 | `matches_clean` | `uint32` | `optional` | `` |  |
| 7 | `matches_reported` | `uint32` | `optional` | `` |  |
| 8 | `matches_abandoned` | `uint32` | `optional` | `` |  |
| 9 | `reports_count` | `uint32` | `optional` | `` |  |
| 10 | `reports_parties` | `uint32` | `optional` | `` |  |
| 11 | `commend_count` | `uint32` | `optional` | `` |  |
| 14 | `date` | `uint32` | `optional` | `` |  |
| 17 | `raw_behavior_score` | `uint32` | `optional` | `` |  |
| 18 | `old_raw_behavior_score` | `uint32` | `optional` | `` |  |
| 19 | `comms_reports` | `uint32` | `optional` | `` |  |
| 20 | `comms_parties` | `uint32` | `optional` | `` |  |
| 21 | `behavior_rating` | `.CMsgPlayerConductScorecard.EBehaviorRating` | `optional` | `` | default = k_eBehaviorGood |

</details>

<details>
<summary><code>CMsgClientToGCWageringRequest</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientWageringResponse</code> — fields: 13; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `coins_remaining` | `uint32` | `optional` | `` |  |
| 2 | `total_points_won` | `uint32` | `optional` | `` |  |
| 3 | `total_points_wagered` | `uint32` | `optional` | `` |  |
| 4 | `total_points_tipped` | `uint32` | `optional` | `` |  |
| 5 | `success_rate` | `uint32` | `optional` | `` |  |
| 6 | `total_games_wagered` | `uint32` | `optional` | `` |  |
| 7 | `coins_max` | `uint32` | `optional` | `` |  |
| 8 | `rank_wagers_remaining` | `uint32` | `optional` | `` |  |
| 9 | `rank_wagers_max` | `uint32` | `optional` | `` |  |
| 10 | `prediction_tokens_remaining` | `uint32` | `optional` | `` |  |
| 11 | `prediction_tokens_max` | `uint32` | `optional` | `` |  |
| 12 | `bounties_remaining` | `uint32` | `optional` | `` |  |
| 13 | `bounties_max` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientWageringUpdate</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |
| 2 | `wagering_info` | `.CMsgGCToClientWageringResponse` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientArcanaVotesUpdate</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |
| 2 | `arcana_votes` | `.CMsgClientToGCRequestArcanaVotesRemainingResponse` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetEventGoals</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_ids` | `.EEvent` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgEventGoals</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_goals` | `.CMsgEventGoals.EventGoal` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgEventGoals.EventGoal</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgEventGoals`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 2 | `goal_id` | `uint32` | `optional` | `` |  |
| 3 | `value` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCLeaguePredictions</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPredictionRankings</code> — fields: 1; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `predictions` | `.CMsgPredictionRankings.Prediction` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgPredictionRankings.PredictionLine</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgPredictionRankings`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `answer_id` | `uint32` | `optional` | `` |  |
| 2 | `answer_name` | `string` | `optional` | `` |  |
| 3 | `answer_logo` | `uint64` | `optional` | `` |  |
| 4 | `answer_value` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPredictionRankings.Prediction</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgPredictionRankings`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `selection_id` | `uint32` | `optional` | `` |  |
| 2 | `prediction_lines` | `.CMsgPredictionRankings.PredictionLine` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgPredictionResults</code> — fields: 1; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `results` | `.CMsgPredictionResults.Result` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgPredictionResults.ResultBreakdown</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgPredictionResults`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `answer_selection` | `uint32` | `optional` | `` |  |
| 3 | `answer_value` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPredictionResults.Result</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgPredictionResults`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `selection_id` | `uint32` | `optional` | `` |  |
| 2 | `result_breakdown` | `.CMsgPredictionResults.ResultBreakdown` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCHasPlayerVotedForMVP</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCHasPlayerVotedForMVPResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCVoteForMVP</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 3 | `account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCVoteForMVPResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCMVPVoteTimeout</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCMVPVoteTimeoutResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCTeammateStatsRequest</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCTeammateStatsResponse</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `success` | `bool` | `optional` | `` |  |
| 2 | `teammate_stats` | `.CMsgClientToGCTeammateStatsResponse.TeammateStat` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCTeammateStatsResponse.TeammateStat</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCTeammateStatsResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `games` | `uint32` | `optional` | `` |  |
| 3 | `wins` | `uint32` | `optional` | `` |  |
| 4 | `most_recent_game_timestamp` | `uint32` | `optional` | `` |  |
| 5 | `most_recent_game_match_id` | `uint64` | `optional` | `` |  |
| 100 | `performance` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCVoteForArcana</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `matches` | `.CMsgArcanaVoteMatchVotes` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCVoteForArcanaResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCVoteForArcanaResponse.Result` | `optional` | `` | default = SUCCEEDED |

</details>

<details>
<summary><code>CMsgClientToGCRequestArcanaVotesRemaining</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestArcanaVotesRemainingResponse</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `bool` | `optional` | `` |  |
| 2 | `votes_remaining` | `uint32` | `optional` | `` |  |
| 3 | `votes_total` | `uint32` | `optional` | `` |  |
| 4 | `matches_previously_voted_for` | `.CMsgArcanaVoteMatchVotes` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestEventPointLogV2</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestEventPointLogResponseV2</code> — fields: 3; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `bool` | `optional` | `` |  |
| 2 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 3 | `log_entries` | `.CMsgClientToGCRequestEventPointLogResponseV2.LogEntry` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestEventPointLogResponseV2.LogEntry</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCRequestEventPointLogResponseV2`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `timestamp` | `uint32` | `optional` | `` |  |
| 2 | `audit_action` | `uint32` | `optional` | `` |  |
| 3 | `event_points` | `int32` | `optional` | `` |  |
| 4 | `audit_data` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCPublishUserStat</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `user_stats_event` | `uint32` | `optional` | `` |  |
| 2 | `reference_data` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestSlarkGameResult</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 2 | `slot_chosen` | `uint32` | `optional` | `` |  |
| 3 | `week` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestSlarkGameResultResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `points_won` | `uint32` | `optional` | `` |  |
| 2 | `aura_won` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientQuestProgressUpdated</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `quest_id` | `uint32` | `optional` | `` |  |
| 2 | `completed_challenges` | `.CMsgGCToClientQuestProgressUpdated.Challenge` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientQuestProgressUpdated.Challenge</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientQuestProgressUpdated`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `challenge_id` | `uint32` | `optional` | `` |  |
| 2 | `time_completed` | `uint32` | `optional` | `` |  |
| 3 | `attempts` | `uint32` | `optional` | `` |  |
| 4 | `hero_id` | `int32` | `optional` | `` |  |
| 5 | `template_id` | `uint32` | `optional` | `` |  |
| 6 | `quest_rank` | `uint32` | `optional` | `` |  |
| 7 | `max_quest_rank` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTARedeemItem</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `currency_id` | `uint64` | `optional` | `` |  |
| 2 | `purchase_def` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTARedeemItemResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgDOTARedeemItemResponse.EResultCode` | `optional` | `` | default = k_Succeeded |

</details>

<details>
<summary><code>CMsgClientToGCSelectCompendiumInGamePrediction</code> — fields: 3; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `predictions` | `.CMsgClientToGCSelectCompendiumInGamePrediction.Prediction` | `repeated` | `` |  |
| 3 | `league_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCSelectCompendiumInGamePrediction.Prediction</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCSelectCompendiumInGamePrediction`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `prediction_id` | `uint32` | `optional` | `` |  |
| 2 | `prediction_value` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCSelectCompendiumInGamePredictionResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCSelectCompendiumInGamePredictionResponse.EResult` | `optional` | `` | default = SUCCESS |

</details>

<details>
<summary><code>CMsgClientToGCOpenPlayerCardPack</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_card_pack_item_id` | `uint64` | `optional` | `` |  |
| 2 | `team_id` | `uint32` | `optional` | `` |  |
| 3 | `deprecated_league_id` | `uint32` | `optional` | `` |  |
| 4 | `region` | `.ELeagueRegion` | `optional` | `` | default = LEAGUE_REGION_UNSET |

</details>

<details>
<summary><code>CMsgClientToGCOpenPlayerCardPackResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCOpenPlayerCardPackResponse.Result` | `optional` | `` | default = SUCCESS |
| 2 | `player_card_item_ids` | `uint64` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRecyclePlayerCard</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `event_id` | `uint32` | `optional` | `` |  |
| 3 | `player_card_item_ids` | `uint64` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRecyclePlayerCardResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCRecyclePlayerCardResponse.Result` | `optional` | `` | default = SUCCESS |
| 2 | `dust_amount` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCreatePlayerCardPack</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `card_dust_item_id` | `uint64` | `optional` | `` |  |
| 2 | `event_id` | `uint32` | `optional` | `` |  |
| 3 | `premium_pack` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCreatePlayerCardPackResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCCreatePlayerCardPackResponse.Result` | `optional` | `` | default = SUCCESS |

</details>

<details>
<summary><code>CMsgClientToGCCreateTeamPlayerCardPack</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `card_dust_item_id` | `uint64` | `optional` | `` |  |
| 2 | `event_id` | `uint32` | `optional` | `` |  |
| 3 | `premium_pack` | `bool` | `optional` | `` |  |
| 4 | `team_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCreateTeamPlayerCardPackResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCCreateTeamPlayerCardPackResponse.Result` | `optional` | `` | default = SUCCESS |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_International2016</code> — fields: 9; oneofs: 0; nested messages: 8; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `battle_pass_level` | `uint32` | `optional` | `` |  |
| 2 | `questlines` | `.CMsgGCToClientBattlePassRollup_International2016.Questlines` | `repeated` | `` |  |
| 3 | `wagering` | `.CMsgGCToClientBattlePassRollup_International2016.Wagering` | `optional` | `` |  |
| 4 | `achievements` | `.CMsgGCToClientBattlePassRollup_International2016.Achievements` | `optional` | `` |  |
| 5 | `battle_cup` | `.CMsgGCToClientBattlePassRollup_International2016.BattleCup` | `optional` | `` |  |
| 6 | `predictions` | `.CMsgGCToClientBattlePassRollup_International2016.Predictions` | `optional` | `` |  |
| 7 | `bracket` | `.CMsgGCToClientBattlePassRollup_International2016.Bracket` | `optional` | `` |  |
| 8 | `player_cards` | `.CMsgGCToClientBattlePassRollup_International2016.PlayerCard` | `repeated` | `` |  |
| 9 | `fantasy_challenge` | `.CMsgGCToClientBattlePassRollup_International2016.FantasyChallenge` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_International2016.Questlines</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_International2016`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `onestar` | `uint32` | `optional` | `` |  |
| 3 | `twostar` | `uint32` | `optional` | `` |  |
| 4 | `threestar` | `uint32` | `optional` | `` |  |
| 5 | `total` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_International2016.Wagering</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_International2016`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `total_wagered` | `uint32` | `optional` | `` |  |
| 2 | `total_won` | `uint32` | `optional` | `` |  |
| 3 | `average_won` | `uint32` | `optional` | `` |  |
| 4 | `success_rate` | `uint32` | `optional` | `` |  |
| 5 | `total_tips` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_International2016.Achievements</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_International2016`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `completed` | `uint32` | `optional` | `` |  |
| 2 | `total` | `uint32` | `optional` | `` |  |
| 3 | `points` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_International2016.BattleCup</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_International2016`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `wins` | `uint32` | `optional` | `` |  |
| 2 | `score` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_International2016.Predictions</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_International2016`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `correct` | `uint32` | `optional` | `` |  |
| 2 | `total` | `uint32` | `optional` | `` |  |
| 3 | `points` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_International2016.Bracket</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_International2016`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `correct` | `uint32` | `optional` | `` |  |
| 2 | `points` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_International2016.PlayerCard</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_International2016`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `quality` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_International2016.FantasyChallenge</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_International2016`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `total_score` | `float` | `optional` | `` |  |
| 2 | `percentile` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_Fall2016</code> — fields: 9; oneofs: 0; nested messages: 8; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `battle_pass_level` | `uint32` | `optional` | `` |  |
| 2 | `questlines` | `.CMsgGCToClientBattlePassRollup_Fall2016.Questlines` | `repeated` | `` |  |
| 3 | `wagering` | `.CMsgGCToClientBattlePassRollup_Fall2016.Wagering` | `optional` | `` |  |
| 4 | `achievements` | `.CMsgGCToClientBattlePassRollup_Fall2016.Achievements` | `optional` | `` |  |
| 5 | `battle_cup` | `.CMsgGCToClientBattlePassRollup_Fall2016.BattleCup` | `optional` | `` |  |
| 6 | `predictions` | `.CMsgGCToClientBattlePassRollup_Fall2016.Predictions` | `optional` | `` |  |
| 7 | `bracket` | `.CMsgGCToClientBattlePassRollup_Fall2016.Bracket` | `optional` | `` |  |
| 8 | `player_cards` | `.CMsgGCToClientBattlePassRollup_Fall2016.PlayerCard` | `repeated` | `` |  |
| 9 | `fantasy_challenge` | `.CMsgGCToClientBattlePassRollup_Fall2016.FantasyChallenge` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_Fall2016.Questlines</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_Fall2016`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `onestar` | `uint32` | `optional` | `` |  |
| 3 | `twostar` | `uint32` | `optional` | `` |  |
| 4 | `threestar` | `uint32` | `optional` | `` |  |
| 5 | `total` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_Fall2016.Wagering</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_Fall2016`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `total_wagered` | `uint32` | `optional` | `` |  |
| 2 | `total_won` | `uint32` | `optional` | `` |  |
| 3 | `average_won` | `uint32` | `optional` | `` |  |
| 4 | `success_rate` | `uint32` | `optional` | `` |  |
| 5 | `total_tips` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_Fall2016.Achievements</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_Fall2016`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `completed` | `uint32` | `optional` | `` |  |
| 2 | `total` | `uint32` | `optional` | `` |  |
| 3 | `points` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_Fall2016.BattleCup</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_Fall2016`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `wins` | `uint32` | `optional` | `` |  |
| 2 | `score` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_Fall2016.Predictions</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_Fall2016`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `correct` | `uint32` | `optional` | `` |  |
| 2 | `total` | `uint32` | `optional` | `` |  |
| 3 | `points` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_Fall2016.Bracket</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_Fall2016`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `correct` | `uint32` | `optional` | `` |  |
| 2 | `points` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_Fall2016.PlayerCard</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_Fall2016`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `quality` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_Fall2016.FantasyChallenge</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_Fall2016`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `total_score` | `float` | `optional` | `` |  |
| 2 | `percentile` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_Winter2017</code> — fields: 9; oneofs: 0; nested messages: 8; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `battle_pass_level` | `uint32` | `optional` | `` |  |
| 2 | `questlines` | `.CMsgGCToClientBattlePassRollup_Winter2017.Questlines` | `repeated` | `` |  |
| 3 | `wagering` | `.CMsgGCToClientBattlePassRollup_Winter2017.Wagering` | `optional` | `` |  |
| 4 | `achievements` | `.CMsgGCToClientBattlePassRollup_Winter2017.Achievements` | `optional` | `` |  |
| 5 | `battle_cup` | `.CMsgGCToClientBattlePassRollup_Winter2017.BattleCup` | `optional` | `` |  |
| 6 | `predictions` | `.CMsgGCToClientBattlePassRollup_Winter2017.Predictions` | `optional` | `` |  |
| 7 | `bracket` | `.CMsgGCToClientBattlePassRollup_Winter2017.Bracket` | `optional` | `` |  |
| 8 | `player_cards` | `.CMsgGCToClientBattlePassRollup_Winter2017.PlayerCard` | `repeated` | `` |  |
| 9 | `fantasy_challenge` | `.CMsgGCToClientBattlePassRollup_Winter2017.FantasyChallenge` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_Winter2017.Questlines</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_Winter2017`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `onestar` | `uint32` | `optional` | `` |  |
| 3 | `twostar` | `uint32` | `optional` | `` |  |
| 4 | `threestar` | `uint32` | `optional` | `` |  |
| 5 | `total` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_Winter2017.Wagering</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_Winter2017`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `total_wagered` | `uint32` | `optional` | `` |  |
| 2 | `total_won` | `uint32` | `optional` | `` |  |
| 3 | `average_won` | `uint32` | `optional` | `` |  |
| 4 | `success_rate` | `uint32` | `optional` | `` |  |
| 5 | `total_tips` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_Winter2017.Achievements</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_Winter2017`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `completed` | `uint32` | `optional` | `` |  |
| 2 | `total` | `uint32` | `optional` | `` |  |
| 3 | `points` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_Winter2017.BattleCup</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_Winter2017`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `wins` | `uint32` | `optional` | `` |  |
| 2 | `score` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_Winter2017.Predictions</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_Winter2017`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `correct` | `uint32` | `optional` | `` |  |
| 2 | `total` | `uint32` | `optional` | `` |  |
| 3 | `points` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_Winter2017.Bracket</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_Winter2017`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `correct` | `uint32` | `optional` | `` |  |
| 2 | `points` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_Winter2017.PlayerCard</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_Winter2017`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `quality` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_Winter2017.FantasyChallenge</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_Winter2017`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `total_score` | `float` | `optional` | `` |  |
| 2 | `percentile` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_TI7</code> — fields: 9; oneofs: 0; nested messages: 8; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `battle_pass_level` | `uint32` | `optional` | `` |  |
| 2 | `questlines` | `.CMsgGCToClientBattlePassRollup_TI7.Questlines` | `repeated` | `` |  |
| 3 | `wagering` | `.CMsgGCToClientBattlePassRollup_TI7.Wagering` | `optional` | `` |  |
| 4 | `achievements` | `.CMsgGCToClientBattlePassRollup_TI7.Achievements` | `optional` | `` |  |
| 5 | `battle_cup` | `.CMsgGCToClientBattlePassRollup_TI7.BattleCup` | `optional` | `` |  |
| 6 | `predictions` | `.CMsgGCToClientBattlePassRollup_TI7.Predictions` | `optional` | `` |  |
| 7 | `bracket` | `.CMsgGCToClientBattlePassRollup_TI7.Bracket` | `optional` | `` |  |
| 8 | `player_cards` | `.CMsgGCToClientBattlePassRollup_TI7.PlayerCard` | `repeated` | `` |  |
| 9 | `fantasy_challenge` | `.CMsgGCToClientBattlePassRollup_TI7.FantasyChallenge` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_TI7.Questlines</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_TI7`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `onestar` | `uint32` | `optional` | `` |  |
| 3 | `twostar` | `uint32` | `optional` | `` |  |
| 4 | `threestar` | `uint32` | `optional` | `` |  |
| 5 | `total` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_TI7.Wagering</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_TI7`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `total_wagered` | `uint32` | `optional` | `` |  |
| 2 | `total_won` | `uint32` | `optional` | `` |  |
| 3 | `average_won` | `uint32` | `optional` | `` |  |
| 4 | `success_rate` | `uint32` | `optional` | `` |  |
| 5 | `total_tips` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_TI7.Achievements</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_TI7`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `completed` | `uint32` | `optional` | `` |  |
| 2 | `total` | `uint32` | `optional` | `` |  |
| 3 | `points` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_TI7.BattleCup</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_TI7`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `wins` | `uint32` | `optional` | `` |  |
| 2 | `score` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_TI7.Predictions</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_TI7`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `correct` | `uint32` | `optional` | `` |  |
| 2 | `total` | `uint32` | `optional` | `` |  |
| 3 | `points` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_TI7.Bracket</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_TI7`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `correct` | `uint32` | `optional` | `` |  |
| 2 | `points` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_TI7.PlayerCard</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_TI7`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `quality` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_TI7.FantasyChallenge</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_TI7`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `total_score` | `float` | `optional` | `` |  |
| 2 | `percentile` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_TI8</code> — fields: 8; oneofs: 0; nested messages: 7; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `battle_pass_level` | `uint32` | `optional` | `` |  |
| 2 | `cavern_crawl` | `.CMsgGCToClientBattlePassRollup_TI8.CavernCrawl` | `optional` | `` |  |
| 3 | `wagering` | `.CMsgGCToClientBattlePassRollup_TI8.Wagering` | `optional` | `` |  |
| 4 | `achievements` | `.CMsgGCToClientBattlePassRollup_TI8.Achievements` | `optional` | `` |  |
| 6 | `predictions` | `.CMsgGCToClientBattlePassRollup_TI8.Predictions` | `optional` | `` |  |
| 7 | `bracket` | `.CMsgGCToClientBattlePassRollup_TI8.Bracket` | `optional` | `` |  |
| 8 | `player_cards` | `.CMsgGCToClientBattlePassRollup_TI8.PlayerCard` | `repeated` | `` |  |
| 9 | `fantasy_challenge` | `.CMsgGCToClientBattlePassRollup_TI8.FantasyChallenge` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_TI8.CavernCrawl</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_TI8`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `rooms_cleared` | `uint32` | `optional` | `` |  |
| 2 | `carry_completed` | `bool` | `optional` | `` |  |
| 3 | `support_completed` | `bool` | `optional` | `` |  |
| 4 | `utility_completed` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_TI8.Wagering</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_TI8`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `total_wagered` | `uint32` | `optional` | `` |  |
| 2 | `total_won` | `uint32` | `optional` | `` |  |
| 3 | `average_won` | `uint32` | `optional` | `` |  |
| 4 | `success_rate` | `uint32` | `optional` | `` |  |
| 5 | `total_tips` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_TI8.Achievements</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_TI8`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `completed` | `uint32` | `optional` | `` |  |
| 2 | `total` | `uint32` | `optional` | `` |  |
| 3 | `points` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_TI8.Predictions</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_TI8`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `correct` | `uint32` | `optional` | `` |  |
| 2 | `total` | `uint32` | `optional` | `` |  |
| 3 | `points` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_TI8.Bracket</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_TI8`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `correct` | `uint32` | `optional` | `` |  |
| 2 | `points` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_TI8.PlayerCard</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_TI8`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `quality` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_TI8.FantasyChallenge</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollup_TI8`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `total_score` | `float` | `optional` | `` |  |
| 2 | `percentile` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_TI9</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `battle_pass_level` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollup_TI10</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `battle_pass_level` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollupRequest</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |
| 2 | `account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollupResponse</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_ti6` | `.CMsgGCToClientBattlePassRollup_International2016` | `optional` | `` |  |
| 2 | `event_fall2016` | `.CMsgGCToClientBattlePassRollup_Fall2016` | `optional` | `` |  |
| 3 | `event_winter2017` | `.CMsgGCToClientBattlePassRollup_Winter2017` | `optional` | `` |  |
| 4 | `event_ti7` | `.CMsgGCToClientBattlePassRollup_TI7` | `optional` | `` |  |
| 5 | `event_ti8` | `.CMsgGCToClientBattlePassRollup_TI8` | `optional` | `` |  |
| 6 | `event_ti9` | `.CMsgGCToClientBattlePassRollup_TI9` | `optional` | `` |  |
| 7 | `event_ti10` | `.CMsgGCToClientBattlePassRollup_TI10` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollupListRequest</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollupListResponse</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_info` | `.CMsgGCToClientBattlePassRollupListResponse.EventInfo` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientBattlePassRollupListResponse.EventInfo</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientBattlePassRollupListResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |
| 2 | `level` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCTransferSeasonalMMRRequest</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `is_party` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCTransferSeasonalMMRResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `success` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientPlaytestStatus</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `active` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCJoinPlaytest</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `client_version` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCJoinPlaytestResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `error` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTASetFavoriteTeam</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team_id` | `uint32` | `optional` | `` |  |
| 2 | `event_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTATriviaCurrentQuestions</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `questions` | `.CMsgDOTATriviaQuestion` | `repeated` | `` |  |
| 2 | `trivia_enabled` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTASubmitTriviaQuestionAnswer</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `question_id` | `uint32` | `optional` | `` |  |
| 2 | `answer_index` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTASubmitTriviaQuestionAnswerResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.EDOTATriviaAnswerResult` | `optional` | `` | default = k_EDOTATriviaAnswerResult_Success |

</details>

<details>
<summary><code>CMsgDOTAStartTriviaSession</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgDOTAStartTriviaSessionResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `trivia_enabled` | `bool` | `optional` | `` |  |
| 2 | `current_timestamp` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAAnchorPhoneNumberRequest</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgDOTAAnchorPhoneNumberResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgDOTAAnchorPhoneNumberResponse.Result` | `optional` | `` | default = SUCCESS |

</details>

<details>
<summary><code>CMsgDOTAUnanchorPhoneNumberRequest</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgDOTAUnanchorPhoneNumberResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgDOTAUnanchorPhoneNumberResponse.Result` | `optional` | `` | default = SUCCESS |

</details>

<details>
<summary><code>CMsgGCToClientCommendNotification</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `commender_account_id` | `uint32` | `optional` | `` |  |
| 2 | `commender_name` | `string` | `optional` | `` |  |
| 3 | `flags` | `uint32` | `optional` | `` |  |
| 4 | `commender_hero_id` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAClientToGCQuickStatsRequest</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_account_id` | `uint32` | `optional` | `` |  |
| 2 | `hero_id` | `int32` | `optional` | `` |  |
| 3 | `item_id` | `int32` | `optional` | `` | default = -1 |
| 4 | `league_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAClientToGCQuickStatsResponse</code> — fields: 7; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `original_request` | `.CMsgDOTAClientToGCQuickStatsRequest` | `optional` | `` |  |
| 2 | `hero_stats` | `.CMsgDOTAClientToGCQuickStatsResponse.SimpleStats` | `optional` | `` |  |
| 3 | `item_stats` | `.CMsgDOTAClientToGCQuickStatsResponse.SimpleStats` | `optional` | `` |  |
| 4 | `item_hero_stats` | `.CMsgDOTAClientToGCQuickStatsResponse.SimpleStats` | `optional` | `` |  |
| 5 | `item_player_stats` | `.CMsgDOTAClientToGCQuickStatsResponse.SimpleStats` | `optional` | `` |  |
| 6 | `hero_player_stats` | `.CMsgDOTAClientToGCQuickStatsResponse.SimpleStats` | `optional` | `` |  |
| 7 | `full_set_stats` | `.CMsgDOTAClientToGCQuickStatsResponse.SimpleStats` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAClientToGCQuickStatsResponse.SimpleStats</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAClientToGCQuickStatsResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `win_percent` | `float` | `optional` | `` |  |
| 2 | `pick_percent` | `float` | `optional` | `` |  |
| 3 | `win_count` | `uint32` | `optional` | `` |  |
| 4 | `pick_count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTASelectionPriorityChoiceRequest</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `choice` | `.DOTASelectionPriorityChoice` | `optional` | `` | default = k_DOTASelectionPriorityChoice_Invalid |

</details>

<details>
<summary><code>CMsgDOTASelectionPriorityChoiceResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgDOTASelectionPriorityChoiceResponse.Result` | `optional` | `` | default = SUCCESS |

</details>

<details>
<summary><code>CMsgDOTAGameAutographReward</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `badge_id` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAGameAutographRewardResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgDOTAGameAutographRewardResponse.Result` | `optional` | `` | default = SUCCESS |

</details>

<details>
<summary><code>CMsgDOTADestroyLobbyRequest</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgDOTADestroyLobbyResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgDOTADestroyLobbyResponse.Result` | `optional` | `` | default = SUCCESS |

</details>

<details>
<summary><code>CMsgDOTAGetRecentPlayTimeFriendsRequest</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgDOTAGetRecentPlayTimeFriendsResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_ids` | `fixed32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgPurchaseItemWithEventPoints</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_def` | `uint32` | `optional` | `` |  |
| 2 | `quantity` | `uint32` | `optional` | `` |  |
| 3 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 4 | `use_premium_points` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPurchaseItemWithEventPointsResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgPurchaseItemWithEventPointsResponse.Result` | `optional` | `` | default = SUCCESS |

</details>

<details>
<summary><code>CMsgPurchaseHeroRandomRelic</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `relic_rarity` | `.EHeroRelicRarity` | `optional` | `` | default = HERO_RELIC_RARITY_INVALID |

</details>

<details>
<summary><code>CMsgPurchaseHeroRandomRelicResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.EPurchaseHeroRelicResult` | `optional` | `` | default = k_EPurchaseHeroRelicResult_Success |
| 2 | `kill_eater_type` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestPlusWeeklyChallengeResult</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 2 | `week` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestPlusWeeklyChallengeResultResponse</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgProfileRequest</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgProfileResponse</code> — fields: 7; oneofs: 0; nested messages: 2; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `background_item` | `.CSOEconItem` | `optional` | `` |  |
| 2 | `featured_heroes` | `.CMsgProfileResponse.FeaturedHero` | `repeated` | `` |  |
| 3 | `recent_matches` | `.CMsgProfileResponse.MatchInfo` | `repeated` | `` |  |
| 4 | `successful_heroes` | `.CMsgSuccessfulHero` | `repeated` | `` |  |
| 5 | `recent_match_details` | `.CMsgRecentMatchInfo` | `optional` | `` |  |
| 6 | `result` | `.CMsgProfileResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 7 | `stickerbook_page` | `.CMsgStickerbookPage` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgProfileResponse.FeaturedHero</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgProfileResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `equipped_econ_items` | `.CSOEconItem` | `repeated` | `` |  |
| 3 | `manually_set` | `bool` | `optional` | `` |  |
| 4 | `plus_hero_xp` | `uint32` | `optional` | `` |  |
| 5 | `plus_hero_relics_item` | `.CSOEconItem` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgProfileResponse.MatchInfo</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgProfileResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `match_timestamp` | `uint32` | `optional` | `` |  |
| 3 | `performance_rating` | `sint32` | `optional` | `` |  |
| 4 | `hero_id` | `int32` | `optional` | `` |  |
| 5 | `won_match` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgProfileUpdate</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `background_item_id` | `uint64` | `optional` | `` |  |
| 2 | `featured_hero_ids` | `int32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgProfileUpdateResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgProfileUpdateResponse.Result` | `optional` | `` | default = SUCCESS |

</details>

<details>
<summary><code>CMsgTalentWinRates</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `last_run` | `uint32` | `optional` | `` |  |
| 2 | `ability_id` | `int32` | `optional` | `` | default = -1 |
| 3 | `game_count` | `uint32` | `optional` | `` |  |
| 4 | `win_count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGlobalHeroAverages</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `last_run` | `uint32` | `optional` | `` |  |
| 3 | `avg_gold_per_min` | `uint32` | `optional` | `` |  |
| 4 | `avg_xp_per_min` | `uint32` | `optional` | `` |  |
| 5 | `avg_kills` | `uint32` | `optional` | `` |  |
| 6 | `avg_deaths` | `uint32` | `optional` | `` |  |
| 7 | `avg_assists` | `uint32` | `optional` | `` |  |
| 8 | `avg_last_hits` | `uint32` | `optional` | `` |  |
| 9 | `avg_denies` | `uint32` | `optional` | `` |  |
| 10 | `avg_net_worth` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgHeroGlobalDataRequest</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgHeroGlobalDataResponse</code> — fields: 2; oneofs: 0; nested messages: 3; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `hero_data_per_chunk` | `.CMsgHeroGlobalDataResponse.HeroDataPerRankChunk` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgHeroGlobalDataResponse.GraphData</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgHeroGlobalDataResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `day` | `uint32` | `optional` | `` |  |
| 2 | `win_percent` | `float` | `optional` | `` |  |
| 3 | `pick_percent` | `float` | `optional` | `` |  |
| 4 | `ban_percent` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgHeroGlobalDataResponse.WeekData</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgHeroGlobalDataResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `week` | `uint32` | `optional` | `` |  |
| 2 | `win_percent` | `float` | `optional` | `` |  |
| 3 | `pick_percent` | `float` | `optional` | `` |  |
| 4 | `ban_percent` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgHeroGlobalDataResponse.HeroDataPerRankChunk</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgHeroGlobalDataResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `rank_chunk` | `uint32` | `optional` | `` |  |
| 2 | `talent_win_rates` | `.CMsgTalentWinRates` | `repeated` | `` |  |
| 3 | `hero_averages` | `.CMsgGlobalHeroAverages` | `optional` | `` |  |
| 4 | `graph_data` | `.CMsgHeroGlobalDataResponse.GraphData` | `repeated` | `` |  |
| 5 | `week_data` | `.CMsgHeroGlobalDataResponse.WeekData` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgHeroGlobalDataAllHeroes</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `heroes` | `.CMsgHeroGlobalDataResponse` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgHeroGlobalDataHeroesAlliesAndEnemies</code> — fields: 1; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ranked_hero_data` | `.CMsgHeroGlobalDataHeroesAlliesAndEnemies.RankedHeroData` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgHeroGlobalDataHeroesAlliesAndEnemies.HeroData</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgHeroGlobalDataHeroesAlliesAndEnemies`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `win_rate` | `uint32` | `optional` | `` |  |
| 3 | `first_other_hero_id` | `int32` | `optional` | `` |  |
| 5 | `ally_win_rate` | `uint32` | `repeated` | `` |  |
| 6 | `enemy_win_rate` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgHeroGlobalDataHeroesAlliesAndEnemies.RankedHeroData</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgHeroGlobalDataHeroesAlliesAndEnemies`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `rank` | `uint32` | `optional` | `` |  |
| 2 | `hero_data` | `.CMsgHeroGlobalDataHeroesAlliesAndEnemies.HeroData` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgPrivateMetadataKeyRequest</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPrivateMetadataKeyResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `private_key` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgActivatePlusFreeTrialResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgActivatePlusFreeTrialResponse.Result` | `optional` | `` | default = SUCCESS |

</details>

<details>
<summary><code>CMsgGCToClientCavernCrawlMapPathCompleted</code> — fields: 4; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |
| 2 | `hero_id_completed` | `int32` | `optional` | `` |  |
| 3 | `completed_paths` | `.CMsgGCToClientCavernCrawlMapPathCompleted.CompletedPathInfo` | `repeated` | `` |  |
| 4 | `map_variant` | `uint32` | `optional` | `` | default = 255 |

</details>

<details>
<summary><code>CMsgGCToClientCavernCrawlMapPathCompleted.CompletedPathInfo</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientCavernCrawlMapPathCompleted`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `path_id_completed` | `uint32` | `optional` | `` | default = 255 |
| 2 | `received_ultra_rare_reward` | `bool` | `optional` | `` |  |
| 3 | `half_completed` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientCavernCrawlMapUpdated</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCavernCrawlClaimRoom</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |
| 2 | `room_id` | `uint32` | `optional` | `` | default = 255 |
| 3 | `map_variant` | `uint32` | `optional` | `` | default = 255 |

</details>

<details>
<summary><code>CMsgClientToGCCavernCrawlClaimRoomResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCCavernCrawlClaimRoomResponse.Result` | `optional` | `` | default = SUCCESS |

</details>

<details>
<summary><code>CMsgClientToGCCavernCrawlUseItemOnRoom</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |
| 2 | `room_id` | `uint32` | `optional` | `` | default = 255 |
| 3 | `item_type` | `uint32` | `optional` | `` |  |
| 4 | `map_variant` | `uint32` | `optional` | `` | default = 255 |

</details>

<details>
<summary><code>CMsgClientToGCCavernCrawlUseItemOnRoomResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCCavernCrawlUseItemOnRoomResponse.Result` | `optional` | `` | default = SUCCESS |

</details>

<details>
<summary><code>CMsgClientToGCCavernCrawlUseItemOnPath</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |
| 2 | `path_id` | `uint32` | `optional` | `` | default = 255 |
| 3 | `item_type` | `uint32` | `optional` | `` |  |
| 4 | `map_variant` | `uint32` | `optional` | `` | default = 255 |

</details>

<details>
<summary><code>CMsgClientToGCCavernCrawlUseItemOnPathResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCCavernCrawlUseItemOnPathResponse.Result` | `optional` | `` | default = SUCCESS |

</details>

<details>
<summary><code>CMsgClientToGCCavernCrawlRequestMapState</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCavernCrawlRequestMapStateResponse</code> — fields: 4; oneofs: 0; nested messages: 4; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCCavernCrawlRequestMapStateResponse.Result` | `optional` | `` | default = SUCCESS |
| 2 | `available_map_variants_mask` | `uint32` | `optional` | `` |  |
| 3 | `inventory_item` | `.CMsgClientToGCCavernCrawlRequestMapStateResponse.InventoryItem` | `repeated` | `` |  |
| 4 | `map_variants` | `.CMsgClientToGCCavernCrawlRequestMapStateResponse.MapVariant` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCavernCrawlRequestMapStateResponse.SwappedChallenge</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCCavernCrawlRequestMapStateResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `path_id_1` | `uint32` | `optional` | `` | default = 255 |
| 2 | `path_id_2` | `uint32` | `optional` | `` | default = 255 |

</details>

<details>
<summary><code>CMsgClientToGCCavernCrawlRequestMapStateResponse.InventoryItem</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCCavernCrawlRequestMapStateResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_type` | `uint32` | `optional` | `` |  |
| 2 | `count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCavernCrawlRequestMapStateResponse.TreasureMap</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCCavernCrawlRequestMapStateResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `map_room_id` | `uint32` | `optional` | `` | default = 255 |
| 2 | `revealed_room_id` | `uint32` | `optional` | `` | default = 255 |

</details>

<details>
<summary><code>CMsgClientToGCCavernCrawlRequestMapStateResponse.MapVariant</code> — fields: 16; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCCavernCrawlRequestMapStateResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `map_variant` | `uint32` | `optional` | `` | default = 255 |
| 2 | `claimed_rooms_1` | `fixed64` | `optional` | `` |  |
| 3 | `claimed_rooms_2` | `fixed64` | `optional` | `` |  |
| 4 | `revealed_rooms_1` | `fixed64` | `optional` | `` |  |
| 5 | `revealed_rooms_2` | `fixed64` | `optional` | `` |  |
| 6 | `completed_paths_1` | `fixed64` | `optional` | `` |  |
| 7 | `completed_paths_2` | `fixed64` | `optional` | `` |  |
| 8 | `completed_paths_3` | `fixed64` | `optional` | `` |  |
| 9 | `completed_paths_4` | `fixed64` | `optional` | `` |  |
| 10 | `half_completed_paths_1` | `fixed64` | `optional` | `` |  |
| 11 | `half_completed_paths_2` | `fixed64` | `optional` | `` |  |
| 12 | `half_completed_paths_3` | `fixed64` | `optional` | `` |  |
| 13 | `half_completed_paths_4` | `fixed64` | `optional` | `` |  |
| 14 | `swapped_challenge` | `.CMsgClientToGCCavernCrawlRequestMapStateResponse.SwappedChallenge` | `repeated` | `` |  |
| 15 | `ultra_rare_reward_room_number` | `uint32` | `optional` | `` | default = 255 |
| 16 | `treasure_map` | `.CMsgClientToGCCavernCrawlRequestMapStateResponse.TreasureMap` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCavernCrawlGetClaimedRoomCount</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCavernCrawlGetClaimedRoomCountResponse</code> — fields: 3; oneofs: 0; nested messages: 1; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCCavernCrawlGetClaimedRoomCountResponse.Result` | `optional` | `` | default = SUCCESS |
| 2 | `map_variants` | `.CMsgClientToGCCavernCrawlGetClaimedRoomCountResponse.MapVariant` | `repeated` | `` |  |
| 3 | `available_map_variants_mask` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCavernCrawlGetClaimedRoomCountResponse.MapVariant</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCCavernCrawlGetClaimedRoomCountResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `map_variant` | `uint32` | `optional` | `` | default = 255 |
| 2 | `count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAMutationList</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `mutations` | `.CMsgDOTAMutationList.Mutation` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAMutationList.Mutation</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAMutationList`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `id` | `uint32` | `optional` | `` |  |
| 2 | `name` | `string` | `optional` | `` |  |
| 3 | `description` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgEventTipsSummaryRequest</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 2 | `account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgEventTipsSummaryResponse</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `bool` | `optional` | `` |  |
| 2 | `tips_received` | `.CMsgEventTipsSummaryResponse.Tipper` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgEventTipsSummaryResponse.Tipper</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgEventTipsSummaryResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `tipper_account_id` | `uint32` | `optional` | `` |  |
| 2 | `tip_count` | `uint32` | `optional` | `` | default = 1 |

</details>

<details>
<summary><code>CMsgSocialFeedRequest</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `self_only` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSocialFeedResponse</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgSocialFeedResponse.Result` | `optional` | `` | default = SUCCESS |
| 2 | `feed_events` | `.CMsgSocialFeedResponse.FeedEvent` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSocialFeedResponse.FeedEvent</code> — fields: 11; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSocialFeedResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `feed_event_id` | `uint64` | `optional` | `` |  |
| 2 | `account_id` | `uint32` | `optional` | `` |  |
| 3 | `timestamp` | `uint32` | `optional` | `` |  |
| 4 | `comment_count` | `uint32` | `optional` | `` |  |
| 5 | `event_type` | `uint32` | `optional` | `` |  |
| 6 | `event_sub_type` | `uint32` | `optional` | `` |  |
| 7 | `param_big_int_1` | `uint64` | `optional` | `` |  |
| 8 | `param_int_1` | `uint32` | `optional` | `` |  |
| 9 | `param_int_2` | `uint32` | `optional` | `` |  |
| 10 | `param_int_3` | `uint32` | `optional` | `` |  |
| 11 | `param_string` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSocialFeedCommentsRequest</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `feed_event_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSocialFeedCommentsResponse</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgSocialFeedCommentsResponse.Result` | `optional` | `` | default = SUCCESS |
| 3 | `feed_comments` | `.CMsgSocialFeedCommentsResponse.FeedComment` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSocialFeedCommentsResponse.FeedComment</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSocialFeedCommentsResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `commenter_account_id` | `uint32` | `optional` | `` |  |
| 2 | `timestamp` | `uint32` | `optional` | `` |  |
| 3 | `comment_text` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCPlayerCardSpecificPurchaseRequest</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_account_id` | `uint32` | `optional` | `` |  |
| 2 | `event_id` | `uint32` | `optional` | `` |  |
| 3 | `card_dust_item_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCPlayerCardSpecificPurchaseResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCPlayerCardSpecificPurchaseResponse.Result` | `optional` | `` | default = SUCCESS |
| 2 | `item_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestContestVotes</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `contest_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestContestVotesResponse</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCRequestContestVotesResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `votes` | `.CMsgClientToGCRequestContestVotesResponse.ItemVote` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestContestVotesResponse.ItemVote</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCRequestContestVotesResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `contest_item_id` | `uint64` | `optional` | `` |  |
| 2 | `vote` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRecordContestVote</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `contest_id` | `uint32` | `optional` | `` |  |
| 2 | `contest_item_id` | `uint64` | `optional` | `` |  |
| 3 | `vote` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientRecordContestVoteResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `eresult` | `.CMsgGCToClientRecordContestVoteResponse.EResult` | `optional` | `` | default = SUCCESS |

</details>

<details>
<summary><code>CMsgDevGrantEventPoints</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 2 | `event_points` | `uint32` | `optional` | `` |  |
| 3 | `premium_points` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDevGrantEventPointsResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.EDevEventRequestResult` | `optional` | `` | default = k_EDevEventRequestResult_Success |

</details>

<details>
<summary><code>CMsgDevGrantEventAction</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 2 | `action_id` | `uint32` | `optional` | `` |  |
| 3 | `action_score` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDevGrantEventActionResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.EDevEventRequestResult` | `optional` | `` | default = k_EDevEventRequestResult_Success |

</details>

<details>
<summary><code>CMsgDevDeleteEventActions</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 2 | `start_action_id` | `uint32` | `optional` | `` |  |
| 3 | `end_action_id` | `uint32` | `optional` | `` |  |
| 4 | `remove_audit` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDevDeleteEventActionsResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.EDevEventRequestResult` | `optional` | `` | default = k_EDevEventRequestResult_Success |

</details>

<details>
<summary><code>CMsgDevResetEventState</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 2 | `remove_audit` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDevResetEventStateResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.EDevEventRequestResult` | `optional` | `` | default = k_EDevEventRequestResult_Success |

</details>

<details>
<summary><code>CMsgDevReloadAllEvents</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgDevReloadAllEventsResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.EDevEventRequestResult` | `optional` | `` | default = k_EDevEventRequestResult_Success |

</details>

<details>
<summary><code>CMsgConsumeEventSupportGrantItem</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgConsumeEventSupportGrantItemResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.ESupportEventRequestResult` | `optional` | `` | default = k_ESupportEventRequestResult_Success |

</details>

<details>
<summary><code>CMsgClientToGCGetFilteredPlayers</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgGCToClientGetFilteredPlayersResponse</code> — fields: 5; oneofs: 0; nested messages: 1; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgGCToClientGetFilteredPlayersResponse.Result` | `optional` | `` | default = SUCCESS |
| 2 | `filtered_players` | `.CMsgGCToClientGetFilteredPlayersResponse.CFilterEntry` | `repeated` | `` |  |
| 3 | `base_slots` | `int32` | `optional` | `` |  |
| 4 | `additional_slots` | `int32` | `optional` | `` |  |
| 5 | `next_slot_cost` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientGetFilteredPlayersResponse.CFilterEntry</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientGetFilteredPlayersResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `fixed32` | `optional` | `` |  |
| 2 | `time_added` | `fixed32` | `optional` | `` |  |
| 3 | `time_expires` | `fixed32` | `optional` | `` |  |
| 4 | `note` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRemoveFilteredPlayer</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id_to_remove` | `fixed32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientRemoveFilteredPlayerResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgGCToClientRemoveFilteredPlayerResponse.Result` | `optional` | `` | default = SUCCESS |

</details>

<details>
<summary><code>CMsgClientToGCPurchaseFilteredPlayerSlot</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `additional_slots_current` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientPurchaseFilteredPlayerSlotResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgGCToClientPurchaseFilteredPlayerSlotResponse.Result` | `optional` | `` | default = SUCCESS |
| 2 | `additional_slots` | `int32` | `optional` | `` |  |
| 3 | `next_slot_cost` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCUpdateFilteredPlayerNote</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_account_id` | `fixed32` | `optional` | `` |  |
| 2 | `new_note` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientUpdateFilteredPlayerNoteResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgGCToClientUpdateFilteredPlayerNoteResponse.Result` | `optional` | `` | default = SUCCESS |

</details>

<details>
<summary><code>CMsgPartySearchPlayer</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `fixed32` | `optional` | `` |  |
| 2 | `match_id` | `fixed64` | `optional` | `` |  |
| 3 | `creation_time` | `fixed32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientPlayerBeaconState</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `num_active_beacons` | `int32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientPartyBeaconUpdate</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `beacon_added` | `bool` | `optional` | `` |  |
| 2 | `beacon_type` | `int32` | `optional` | `` |  |
| 3 | `account_id` | `fixed32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCUpdatePartyBeacon</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `action` | `.CMsgClientToGCUpdatePartyBeacon.Action` | `optional` | `` | default = ON |

</details>

<details>
<summary><code>CMsgClientToGCRequestActiveBeaconParties</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgGCToClientRequestActiveBeaconPartiesResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgGCToClientRequestActiveBeaconPartiesResponse.EResponse` | `optional` | `` | default = SUCCESS |
| 2 | `active_parties` | `.CPartySearchClientParty` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCJoinPartyFromBeacon</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `party_id` | `fixed64` | `optional` | `` |  |
| 2 | `account_id` | `fixed32` | `optional` | `` |  |
| 3 | `beacon_type` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientJoinPartyFromBeaconResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgGCToClientJoinPartyFromBeaconResponse.EResponse` | `optional` | `` | default = SUCCESS |

</details>

<details>
<summary><code>CMsgClientToGCManageFavorites</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `action` | `.CMsgClientToGCManageFavorites.Action` | `optional` | `` | default = ADD |
| 2 | `account_id` | `fixed32` | `optional` | `` |  |
| 3 | `favorite_name` | `string` | `optional` | `` |  |
| 4 | `invite_response` | `bool` | `optional` | `` |  |
| 5 | `from_friendlist` | `bool` | `optional` | `` |  |
| 6 | `lobby_id` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientManageFavoritesResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgGCToClientManageFavoritesResponse.EResponse` | `optional` | `` | default = SUCCESS |
| 2 | `debug_message` | `string` | `optional` | `` |  |
| 3 | `player` | `.CMsgPartySearchPlayer` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetFavoritePlayers</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `pagination_key` | `uint64` | `optional` | `` |  |
| 2 | `pagination_count` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientGetFavoritePlayersResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgGCToClientGetFavoritePlayersResponse.EResponse` | `optional` | `` | default = SUCCESS |
| 2 | `players` | `.CMsgPartySearchPlayer` | `repeated` | `` |  |
| 3 | `next_pagination_key` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientPartySearchInvite</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `fixed32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCVerifyFavoritePlayers</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_ids` | `fixed32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientVerifyFavoritePlayersResponse</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `results` | `.CMsgGCToClientVerifyFavoritePlayersResponse.Result` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientVerifyFavoritePlayersResponse.Result</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToClientVerifyFavoritePlayersResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player` | `.CMsgPartySearchPlayer` | `optional` | `` |  |
| 2 | `is_favorite` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestPlayerRecentAccomplishments</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestPlayerRecentAccomplishmentsResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCRequestPlayerRecentAccomplishmentsResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `player_accomplishments` | `.CMsgPlayerRecentAccomplishments` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestPlayerHeroRecentAccomplishments</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `hero_id` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestPlayerHeroRecentAccomplishmentsResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCRequestPlayerHeroRecentAccomplishmentsResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `hero_accomplishments` | `.CMsgPlayerHeroRecentAccomplishments` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCSubmitPlayerMatchSurvey</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 3 | `rating` | `sint32` | `optional` | `` |  |
| 4 | `flags` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCSubmitPlayerMatchSurveyResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `eresult` | `.CMsgClientToGCSubmitPlayerMatchSurveyResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientVACReminder</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCUnderDraftRequest</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `event_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCUnderDraftResponse</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.EUnderDraftResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `account_id` | `uint32` | `optional` | `` |  |
| 3 | `event_id` | `uint32` | `optional` | `` |  |
| 4 | `draft_data` | `.CMsgUnderDraftData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCUnderDraftReroll</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCUnderDraftRerollResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.EUnderDraftResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `event_id` | `uint32` | `optional` | `` |  |
| 3 | `draft_data` | `.CMsgUnderDraftData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCUnderDraftBuy</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |
| 2 | `slot_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientGuildUnderDraftGoldUpdated</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCUnderDraftBuyResponse</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.EUnderDraftResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `event_id` | `uint32` | `optional` | `` |  |
| 3 | `slot_id` | `uint32` | `optional` | `` |  |
| 4 | `draft_data` | `.CMsgUnderDraftData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCUnderDraftRollBackBench</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCUnderDraftRollBackBenchResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.EUnderDraftResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `event_id` | `uint32` | `optional` | `` |  |
| 3 | `draft_data` | `.CMsgUnderDraftData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCUnderDraftSell</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |
| 2 | `slot_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCUnderDraftSellResponse</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.EUnderDraftResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `event_id` | `uint32` | `optional` | `` |  |
| 3 | `slot_id` | `uint32` | `optional` | `` |  |
| 4 | `draft_data` | `.CMsgUnderDraftData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCUnderDraftRedeemReward</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |
| 2 | `action_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCUnderDraftRedeemRewardResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.EUnderDraftResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCSubmitDraftTriviaMatchAnswer</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `chose_radiant_as_winner` | `bool` | `optional` | `` |  |
| 2 | `event_id` | `uint32` | `optional` | `` |  |
| 3 | `end_time` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCSubmitDraftTriviaMatchAnswerResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.EDOTADraftTriviaAnswerResult` | `optional` | `` | default = k_EDOTADraftTriviaAnswerResult_Success |

</details>

<details>
<summary><code>CMsgDraftTriviaVoteCount</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `total_votes` | `uint32` | `optional` | `` |  |
| 2 | `radiant_votes` | `uint32` | `optional` | `` |  |
| 3 | `dire_votes` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestReporterUpdates</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestReporterUpdatesResponse</code> — fields: 4; oneofs: 0; nested messages: 1; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `enum_result` | `.CMsgClientToGCRequestReporterUpdatesResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `updates` | `.CMsgClientToGCRequestReporterUpdatesResponse.ReporterUpdate` | `repeated` | `` |  |
| 3 | `num_reported` | `int32` | `optional` | `` |  |
| 4 | `num_no_action_taken` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestReporterUpdatesResponse.ReporterUpdate</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCRequestReporterUpdatesResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `hero_id` | `int32` | `optional` | `` |  |
| 3 | `report_reason` | `uint32` | `optional` | `` |  |
| 4 | `timestamp` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCAcknowledgeReporterUpdates</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_ids` | `uint64` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRecalibrateMMR</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCRecalibrateMMRResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCRecalibrateMMRResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgDOTAPostGameItemAwardNotification</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `receiver_account_id` | `uint32` | `optional` | `` |  |
| 2 | `item_def_index` | `uint32` | `repeated` | `` |  |
| 3 | `action_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetOWMatchDetails</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCGetOWMatchDetailsResponse</code> — fields: 11; oneofs: 0; nested messages: 1; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCGetOWMatchDetailsResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `overwatch_replay_id` | `uint64` | `optional` | `` |  |
| 3 | `decryption_key` | `uint64` | `optional` | `` |  |
| 4 | `cluster` | `uint32` | `optional` | `` |  |
| 5 | `overwatch_salt` | `uint32` | `optional` | `` |  |
| 6 | `target_player_slot` | `uint32` | `optional` | `` |  |
| 7 | `markers` | `.CMsgClientToGCGetOWMatchDetailsResponse.Marker` | `repeated` | `` |  |
| 8 | `report_reason` | `.EOverwatchReportReason` | `optional` | `` | default = k_EOverwatchReportReason_Unknown |
| 9 | `target_hero_id` | `int32` | `optional` | `` |  |
| 10 | `rank_tier` | `uint32` | `optional` | `` |  |
| 11 | `lane_selection_flags` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetOWMatchDetailsResponse.Marker</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCGetOWMatchDetailsResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `start_game_time_s` | `uint32` | `optional` | `` |  |
| 2 | `end_game_time_s` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCSubmitOWConviction</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `overwatch_replay_id` | `uint64` | `optional` | `` |  |
| 2 | `target_player_slot` | `uint32` | `optional` | `` |  |
| 3 | `cheating_conviction` | `.EOverwatchConviction` | `optional` | `` | default = k_EOverwatchConviction_None |
| 4 | `griefing_conviction` | `.EOverwatchConviction` | `optional` | `` | default = k_EOverwatchConviction_None |

</details>

<details>
<summary><code>CMsgClientToGCSubmitOWConvictionResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCSubmitOWConvictionResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `overwatch_replay_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCChinaSSAURLRequest</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCChinaSSAURLResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `agreement_url` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCChinaSSAAcceptedRequest</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCChinaSSAAcceptedResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `agreement_accepted` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientOverwatchCasesAvailable</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `expire_time` | `fixed32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCStartWatchingOverwatch</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `overwatch_replay_id` | `uint64` | `optional` | `` |  |
| 2 | `target_player_slot` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCStopWatchingOverwatch</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `overwatch_replay_id` | `uint64` | `optional` | `` |  |
| 2 | `target_player_slot` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCOverwatchReplayError</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `overwatch_replay_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetDPCFavorites</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCGetDPCFavoritesResponse</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCGetDPCFavoritesResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `favorites` | `.CMsgClientToGCGetDPCFavoritesResponse.Favorite` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetDPCFavoritesResponse.Favorite</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCGetDPCFavoritesResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `favorite_type` | `.EDPCFavoriteType` | `optional` | `` | default = FAVORITE_TYPE_ALL |
| 2 | `favorite_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCSetDPCFavoriteState</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `favorite_type` | `.EDPCFavoriteType` | `optional` | `` | default = FAVORITE_TYPE_ALL |
| 2 | `favorite_id` | `uint32` | `optional` | `` |  |
| 3 | `enabled` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCSetDPCFavoriteStateResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCSetDPCFavoriteStateResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCSetEventActiveSeasonID</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |
| 2 | `active_season_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCSetEventActiveSeasonIDResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCSetEventActiveSeasonIDResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCPurchaseLabyrinthBlessings</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 2 | `blessing_ids` | `int32` | `repeated` | `` |  |
| 3 | `debug` | `bool` | `optional` | `` |  |
| 4 | `debug_remove` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCPurchaseLabyrinthBlessingsResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCPurchaseLabyrinthBlessingsResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCGetStickerbookRequest</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetStickerbookResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCGetStickerbookResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `stickerbook` | `.CMsgStickerbook` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCreateStickerbookPageRequest</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team_id` | `uint32` | `optional` | `` |  |
| 2 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 3 | `page_type` | `.EStickerbookPageType` | `optional` | `` | default = STICKER_PAGE_GENERIC |

</details>

<details>
<summary><code>CMsgClientToGCCreateStickerbookPageResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCCreateStickerbookPageResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `page_number` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCDeleteStickerbookPageRequest</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `page_num` | `uint32` | `optional` | `` |  |
| 2 | `sticker_count` | `uint32` | `optional` | `` |  |
| 3 | `sticker_max` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCDeleteStickerbookPageResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCDeleteStickerbookPageResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCPlaceStickersRequest</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `sticker_items` | `.CMsgClientToGCPlaceStickersRequest.StickerItem` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCPlaceStickersRequest.StickerItem</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCPlaceStickersRequest`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `page_num` | `uint32` | `optional` | `` |  |
| 3 | `sticker` | `.CMsgStickerbookSticker` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCPlaceStickersResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCPlaceStickersResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCPlaceCollectionStickersRequest</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `slots` | `.CMsgClientToGCPlaceCollectionStickersRequest.Slot` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCPlaceCollectionStickersRequest.Slot</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCPlaceCollectionStickersRequest`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `page_num` | `uint32` | `optional` | `` |  |
| 2 | `slot` | `uint32` | `optional` | `` |  |
| 3 | `new_item_id` | `uint64` | `optional` | `` |  |
| 4 | `old_item_def_id` | `uint32` | `optional` | `` |  |
| 5 | `old_quality` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCPlaceCollectionStickersResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCPlaceCollectionStickersResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCOrderStickerbookTeamPageRequest</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `page_order_sequence` | `.CMsgStickerbookTeamPageOrderSequence` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCOrderStickerbookTeamPageResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCOrderStickerbookTeamPageResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCSetHeroSticker</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `new_item_id` | `uint64` | `optional` | `` |  |
| 3 | `old_item_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCSetHeroStickerResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCSetHeroStickerResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCGetHeroStickers</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCGetHeroStickersResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCGetHeroStickersResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `sticker_heroes` | `.CMsgStickerHeroes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCSetFavoritePage</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `page_num` | `uint32` | `optional` | `` |  |
| 2 | `clear` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCSetFavoritePageResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCSetFavoritePageResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCClaimSwag</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 2 | `action_id` | `uint32` | `optional` | `` |  |
| 3 | `data` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCClaimSwagResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCClaimSwagResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCCollectorsCacheAvailableDataRequest</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `contest_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientCollectorsCacheAvailableDataResponse</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `votes` | `.CMsgGCToClientCollectorsCacheAvailableDataResponse.Vote` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientCollectorsCacheAvailableDataResponse.Vote</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: `CMsgGCToClientCollectorsCacheAvailableDataResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_def` | `uint32` | `optional` | `` |  |
| 2 | `vote_type` | `.CMsgGCToClientCollectorsCacheAvailableDataResponse.Vote.EVoteType` | `optional` | `` | default = k_eUp |

</details>

<details>
<summary><code>CMsgClientToGCUploadMatchClip</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_clip` | `.CMatchClip` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientUploadMatchClipResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgGCToClientUploadMatchClipResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCMapStatsRequest</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgGCToClientMapStatsResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgGCToClientMapStatsResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `personal_stats` | `.CMsgMapStatsSnapshot` | `optional` | `` |  |
| 3 | `global_stats` | `.CMsgGlobalMapStats` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgRoadToTIAssignedQuest</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `quest_id` | `uint32` | `optional` | `` |  |
| 2 | `difficulty` | `uint32` | `optional` | `` |  |
| 3 | `progress_flags` | `uint32` | `optional` | `` |  |
| 4 | `half_credit_flags` | `uint32` | `optional` | `` |  |
| 5 | `completed` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgRoadToTIUserData</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `quests` | `.CMsgRoadToTIAssignedQuest` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRoadToTIGetQuests</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRoadToTIGetQuestsResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCRoadToTIGetQuestsResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `quest_data` | `.CMsgRoadToTIUserData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRoadToTIGetActiveQuest</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRoadToTIGetActiveQuestResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCRoadToTIGetActiveQuestResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `quest_data` | `.CMsgRoadToTIAssignedQuest` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientRoadToTIQuestDataUpdated</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |
| 2 | `quest_data` | `.CMsgRoadToTIUserData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRoadToTIUseItem</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |
| 2 | `item_type` | `uint32` | `optional` | `` |  |
| 3 | `hero_index` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRoadToTIUseItemResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCRoadToTIUseItemResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCRoadToTIDevForceQuest</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |
| 2 | `force_match_type` | `bool` | `optional` | `` |  |
| 3 | `force_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgLobbyRoadToTIMatchQuestData</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `quest_data` | `.CMsgRoadToTIAssignedQuest` | `optional` | `` |  |
| 2 | `quest_period` | `uint32` | `optional` | `` |  |
| 3 | `quest_number` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCNewBloomGift</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `defindex` | `uint32` | `optional` | `` |  |
| 2 | `lobby_id` | `uint64` | `optional` | `` |  |
| 3 | `target_account_ids` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCNewBloomGiftResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.ENewBloomGiftingResponse` | `optional` | `` | default = kENewBloomGifting_UnknownFailure |
| 2 | `received_account_ids` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCSetBannedHeroes</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `banned_hero_ids` | `int32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCUpdateComicBookStats</code> — fields: 3; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `comic_id` | `uint32` | `optional` | `` |  |
| 2 | `stats` | `.CMsgClientToGCUpdateComicBookStats.SingleStat` | `repeated` | `` |  |
| 3 | `language_stats` | `.CMsgClientToGCUpdateComicBookStats.LanguageStats` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCUpdateComicBookStats.SingleStat</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCUpdateComicBookStats`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `stat_type` | `.CMsgClientToGCUpdateComicBookStat_Type` | `optional` | `` | default = CMsgClientToGCUpdateComicBookStat_Type_HighestPageRead |
| 2 | `stat_value` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCUpdateComicBookStats.LanguageStats</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCUpdateComicBookStats`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `comic_id` | `uint32` | `optional` | `` |  |
| 2 | `client_language` | `uint32` | `optional` | `` |  |
| 3 | `client_comic_language` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCRankedPlayerInfoSubmit</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCRankedPlayerInfoSubmitResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgGCRankedPlayerInfoSubmitResponse.EResult` | `optional` | `` | default = SUCCESS |

</details>

<details>
<summary><code>CMsgDOTAClaimGatedEvent</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |

</details>

<details>
<summary><code>CMsgDOTAClaimGatedEventResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgDOTAClaimGatedEventResponse.ResultCode` | `optional` | `` | default = Success |

</details>

<details>
<summary><code>CMsgClientToGCGetEventRanking</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 2 | `account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetEventRankingResponse</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 2 | `account_id` | `uint32` | `optional` | `` |  |
| 3 | `score` | `float` | `optional` | `` |  |
| 4 | `percentile` | `float` | `optional` | `` |  |
| 5 | `final_rank_bucket` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetEventCoupon</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 2 | `coupon_ids` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetEventCouponResponse</code> — fields: 3; oneofs: 0; nested messages: 1; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCGetEventCouponResponse.ResultCode` | `optional` | `` | default = Success |
| 2 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 3 | `coupons` | `.CMsgClientToGCGetEventCouponResponse.Coupon` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetEventCouponResponse.Coupon</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCGetEventCouponResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `coupon_id` | `uint32` | `optional` | `` |  |
| 2 | `coupon_code` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCConvertEventPoints</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id_points_to_buy` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 2 | `event_id_points_to_spend` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 3 | `num_points_to_buy` | `uint32` | `optional` | `` |  |
| 4 | `num_points_to_spend` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCConvertEventPointsResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCConvertEventPointsResponse.ResultCode` | `optional` | `` | default = Success |

</details>

<details>
<summary><code>CMsgClientToGCInviteToDemoMode</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `server_id` | `fixed64` | `optional` | `` |  |
| 2 | `invited_player_id` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientInviteToDemoMode</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `server_id` | `fixed64` | `optional` | `` |  |
| 2 | `from_player` | `fixed64` | `optional` | `` |  |
| 3 | `party_invite` | `bool` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>CMsgDOTARequestMatches_SkillLevel</code> — values: 4</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `CMsgDOTARequestMatches_SkillLevel_Any` | 0 |
| `CMsgDOTARequestMatches_SkillLevel_Normal` | 1 |
| `CMsgDOTARequestMatches_SkillLevel_High` | 2 |
| `CMsgDOTARequestMatches_SkillLevel_VeryHigh` | 3 |

</details>

<details>
<summary><code>DOTA_WatchReplayType</code> — values: 2</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `DOTA_WATCH_REPLAY_NORMAL` | 0 |
| `DOTA_WATCH_REPLAY_HIGHLIGHTS` | 1 |

</details>

<details>
<summary><code>EItemEditorReservationResult</code> — values: 4</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EItemEditorReservationResult_OK` | 1 |
| `k_EItemEditorReservationResult_AlreadyExists` | 2 |
| `k_EItemEditorReservationResult_Reserved` | 3 |
| `k_EItemEditorReservationResult_TimedOut` | 4 |

</details>

<details>
<summary><code>EWeekendTourneyRichPresenceEvent</code> — values: 4</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EWeekendTourneyRichPresenceEvent_None` | 0 |
| `k_EWeekendTourneyRichPresenceEvent_StartedMatch` | 1 |
| `k_EWeekendTourneyRichPresenceEvent_WonMatch` | 2 |
| `k_EWeekendTourneyRichPresenceEvent_Eliminated` | 3 |

</details>

<details>
<summary><code>EDOTATriviaAnswerResult</code> — values: 6</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EDOTATriviaAnswerResult_Success` | 0 |
| `k_EDOTATriviaAnswerResult_InvalidQuestion` | 1 |
| `k_EDOTATriviaAnswerResult_InvalidAnswer` | 2 |
| `k_EDOTATriviaAnswerResult_QuestionLocked` | 3 |
| `k_EDOTATriviaAnswerResult_AlreadyAnswered` | 4 |
| `k_EDOTATriviaAnswerResult_TriviaDisabled` | 5 |

</details>

<details>
<summary><code>EPurchaseHeroRelicResult</code> — values: 8</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EPurchaseHeroRelicResult_Success` | 0 |
| `k_EPurchaseHeroRelicResult_FailedToSend` | 1 |
| `k_EPurchaseHeroRelicResult_NotEnoughPoints` | 2 |
| `k_EPurchaseHeroRelicResult_InternalServerError` | 3 |
| `k_EPurchaseHeroRelicResult_PurchaseNotAllowed` | 4 |
| `k_EPurchaseHeroRelicResult_InvalidRelic` | 5 |
| `k_EPurchaseHeroRelicResult_AlreadyOwned` | 6 |
| `k_EPurchaseHeroRelicResult_InvalidRarity` | 7 |

</details>

<details>
<summary><code>EDevEventRequestResult</code> — values: 7</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EDevEventRequestResult_Success` | 0 |
| `k_EDevEventRequestResult_NotAllowed` | 1 |
| `k_EDevEventRequestResult_InvalidEvent` | 2 |
| `k_EDevEventRequestResult_SqlFailure` | 3 |
| `k_EDevEventRequestResult_Timeout` | 4 |
| `k_EDevEventRequestResult_LockFailure` | 5 |
| `k_EDevEventRequestResult_SDOLoadFailure` | 6 |

</details>

<details>
<summary><code>ESupportEventRequestResult</code> — values: 14</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_ESupportEventRequestResult_Success` | 0 |
| `k_ESupportEventRequestResult_Timeout` | 1 |
| `k_ESupportEventRequestResult_CantLockSOCache` | 2 |
| `k_ESupportEventRequestResult_ItemNotInInventory` | 3 |
| `k_ESupportEventRequestResult_InvalidItemDef` | 4 |
| `k_ESupportEventRequestResult_InvalidEvent` | 5 |
| `k_ESupportEventRequestResult_EventExpired` | 6 |
| `k_ESupportEventRequestResult_InvalidSupportAccount` | 7 |
| `k_ESupportEventRequestResult_InvalidSupportMessage` | 8 |
| `k_ESupportEventRequestResult_InvalidEventPoints` | 9 |
| `k_ESupportEventRequestResult_InvalidPremiumPoints` | 10 |
| `k_ESupportEventRequestResult_InvalidActionID` | 11 |
| `k_ESupportEventRequestResult_InvalidActionScore` | 12 |
| `k_ESupportEventRequestResult_TransactionFailed` | 13 |

</details>

<details>
<summary><code>EUnderDraftResponse</code> — values: 12</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eNoGold` | 2 |
| `k_eInvalidSlot` | 3 |
| `k_eNoBenchSpace` | 4 |
| `k_eNoTickets` | 5 |
| `k_eEventNotOwned` | 6 |
| `k_eInvalidReward` | 7 |
| `k_eHasBigReward` | 8 |
| `k_eNoGCConnection` | 9 |
| `k_eTooBusy` | 10 |
| `k_eCantRollBack` | 11 |

</details>

<details>
<summary><code>EDOTADraftTriviaAnswerResult</code> — values: 6</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EDOTADraftTriviaAnswerResult_Success` | 0 |
| `k_EDOTADraftTriviaAnswerResult_InvalidMatchID` | 1 |
| `k_EDOTADraftTriviaAnswerResult_AlreadyAnswered` | 2 |
| `k_EDOTADraftTriviaAnswerResult_InternalError` | 3 |
| `k_EDOTADraftTriviaAnswerResult_TriviaDisabled` | 4 |
| `k_EDOTADraftTriviaAnswerResult_GCDown` | 5 |

</details>

<details>
<summary><code>CMsgClientToGCUpdateComicBookStat_Type</code> — values: 3</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `CMsgClientToGCUpdateComicBookStat_Type_HighestPageRead` | 1 |
| `CMsgClientToGCUpdateComicBookStat_Type_SecondsSpentReading` | 2 |
| `CMsgClientToGCUpdateComicBookStat_Type_HighestPercentRead` | 3 |

</details>

<details>
<summary><code>CMsgDOTAPopup.PopupID</code> — values: 63</summary>

- Parent: `CMsgDOTAPopup`

| Name | Number |
|---|---:|
| `NONE` | -1 |
| `KICKED_FROM_LOBBY` | 0 |
| `KICKED_FROM_PARTY` | 1 |
| `KICKED_FROM_TEAM` | 2 |
| `TEAM_WAS_DISBANDED` | 3 |
| `TEAM_MATCHMAKE_ALREADY_MATCH` | 4 |
| `TEAM_MATCHMAKE_ALREADY_FINDING` | 5 |
| `TEAM_MATCHMAKE_FULL` | 6 |
| `TEAM_MATCHMAKE_FAIL_ADD` | 7 |
| `TEAM_MATCHMAKE_FAIL_ADD_CURRENT` | 8 |
| `TEAM_MATCHMAKE_FAILED_TEAM_MEMBER` | 9 |
| `TEAM_MATCHMAKE_ALREADY_GAME` | 10 |
| `TEAM_MATCHMAKE_FAIL_GET_PARTY` | 11 |
| `MATCHMAKING_DISABLED` | 12 |
| `INVITE_DENIED` | 13 |
| `PARTY_FULL` | 14 |
| `MADE_ADMIN` | 15 |
| `NEED_TO_PURCHASE` | 16 |
| `SIGNON_MESSAGE` | 17 |
| `MATCHMAKING_REGION_OFFLINE` | 19 |
| `TOURNAMENT_GAME_NOT_FOUND` | 21 |
| `TOURNAMENT_GAME_HAS_LOBBY_ID` | 22 |
| `TOURNAMENT_GAME_HAS_MATCH_ID` | 23 |
| `TOURNAMENT_GAME_HAS_NO_RADIANT_TEAM` | 24 |
| `TOURNAMENT_GAME_HAS_NO_DIRE_TEAM` | 25 |
| `TOURNAMENT_GAME_SQL_UPDATE_FAILED` | 26 |
| `NOT_LEAGUE_ADMIN` | 27 |
| `IN_ANOTHER_GAME` | 29 |
| `PARTY_MEMBER_IN_ANOTHER_GAME` | 30 |
| `PARTY_MEMBER_IN_LOW_PRIORITY` | 31 |
| `CLIENT_OUT_OF_DATE` | 32 |
| `SAVE_GAME_CORRUPT` | 38 |
| `INSUFFICIENT_INGOTS` | 39 |
| `COMPETITIVE_MM_NOT_ENOUGH_PLAY_TIME_PLAY_MORE_CASUAL` | 42 |
| `PARTY_LEADER_JOINED_LOBBY` | 44 |
| `WEEKEND_TOURNEY_UNMATCHED` | 48 |
| `POST_MATCH_SURVEY` | 49 |
| `TROPHY_AWARDED` | 50 |
| `TROPHY_LEVEL_UP` | 51 |
| `ALL_HERO_CHALLENGE_PROGRESS` | 52 |
| `NEED_INITIAL_SKILL` | 53 |
| `NEED_INITIAL_SKILL_IN_PARTY` | 54 |
| `TARGET_ENGINE_MISMATCH` | 55 |
| `VAC_NOT_VERIFIED` | 56 |
| `KICKED_FROM_QUEUE_EVENT_STARTING` | 57 |
| `KICKED_FROM_QUEUE_EVENT_ENDING` | 58 |
| `LOBBY_FULL` | 62 |
| `EVENT_POINTS_EARNED` | 63 |
| `CUSTOM_GAME_INCORRECT_VERSION` | 64 |
| `LIMITED_USER_CHAT` | 66 |
| `EVENT_PREMIUM_POINTS_EARNED` | 67 |
| `LOBBY_MVP_AWARDED` | 68 |
| `LOW_BADGE_LEVEL_CHAT` | 71 |
| `LOW_WINS_CHAT` | 72 |
| `UNVERIFIED_USER_CHAT` | 73 |
| `PARTY_STARTED_FINDING_EVENT_MATCH` | 74 |
| `GENERIC_INFO` | 69 |
| `GENERIC_ERROR` | 70 |
| `RANK_TIER_UPDATED` | 75 |
| `CUSTOM_GAME_COOLDOWN_RESTRICTED` | 76 |
| `CREATE_LOBBY_FAILED_TOO_MUCH_PLAYTIME` | 77 |
| `CUSTOM_GAME_TOO_FEW_GAMES` | 78 |
| `COMM_SCORE_TOO_LOW` | 79 |

</details>

<details>
<summary><code>CMsgDOTASubmitPlayerReportResponse.EResult</code> — values: 14</summary>

- Parent: `CMsgDOTASubmitPlayerReportResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eDuplicateReport` | 2 |
| `k_eMixedReportFlags` | 3 |
| `k_eTooLate` | 4 |
| `k_eInvalidPregameReport` | 5 |
| `k_eHasntChatted` | 6 |
| `k_eInvalid` | 7 |
| `k_eOwnership` | 8 |
| `k_eMissingRequirements` | 9 |
| `k_eInvalidRoleReport` | 10 |
| `k_eInvalidCoachReport` | 11 |
| `k_eNoRemainingReports` | 12 |
| `k_eInvalidMember` | 13 |

</details>

<details>
<summary><code>CMsgDOTASubmitPlayerReportResponseV2.EResult</code> — values: 15</summary>

- Parent: `CMsgDOTASubmitPlayerReportResponseV2`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eDuplicateReport` | 2 |
| `k_eMixedReportFlags` | 3 |
| `k_eTooLate` | 4 |
| `k_eInvalidPregameReport` | 5 |
| `k_eHasntChatted` | 6 |
| `k_eInvalid` | 7 |
| `k_eOwnership` | 8 |
| `k_eMissingRequirements` | 9 |
| `k_eInvalidRoleReport` | 10 |
| `k_eInvalidCoachReport` | 11 |
| `k_eNoRemainingReports` | 12 |
| `k_eInvalidMember` | 13 |
| `k_eCannotReportPartyMember` | 14 |

</details>

<details>
<summary><code>CMsgGCNotificationsUpdate.EResult</code> — values: 2</summary>

- Parent: `CMsgGCNotificationsUpdate`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `ERROR_UNSPECIFIED` | 1 |

</details>

<details>
<summary><code>CMsgGCPlayerInfoSubmitResponse.EResult</code> — values: 4</summary>

- Parent: `CMsgGCPlayerInfoSubmitResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `ERROR_UNSPECIFIED` | 1 |
| `ERROR_INFO_LOCKED` | 2 |
| `ERROR_NOT_MEMBER_OF_TEAM` | 3 |

</details>

<details>
<summary><code>CMsgGCToClientRankResponse.EResultCode</code> — values: 3</summary>

- Parent: `CMsgGCToClientRankResponse`

| Name | Number |
|---|---:|
| `k_Succeeded` | 0 |
| `k_Failed` | 1 |
| `k_InvalidRankType` | 2 |

</details>

<details>
<summary><code>CMsgGCGetHeroStatsHistoryResponse.EResponse</code> — values: 4</summary>

- Parent: `CMsgGCGetHeroStatsHistoryResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |

</details>

<details>
<summary><code>CMsgPlayerConductScorecard.EBehaviorRating</code> — values: 3</summary>

- Parent: `CMsgPlayerConductScorecard`

| Name | Number |
|---|---:|
| `k_eBehaviorGood` | 0 |
| `k_eBehaviorWarning` | 1 |
| `k_eBehaviorBad` | 2 |

</details>

<details>
<summary><code>CMsgClientToGCVoteForArcanaResponse.Result</code> — values: 3</summary>

- Parent: `CMsgClientToGCVoteForArcanaResponse`

| Name | Number |
|---|---:|
| `SUCCEEDED` | 0 |
| `VOTING_NOT_ENABLED_FOR_ROUND` | 1 |
| `UNKNOWN_FAILURE` | 2 |

</details>

<details>
<summary><code>CMsgDOTARedeemItemResponse.EResultCode</code> — values: 2</summary>

- Parent: `CMsgDOTARedeemItemResponse`

| Name | Number |
|---|---:|
| `k_Succeeded` | 0 |
| `k_Failed` | 1 |

</details>

<details>
<summary><code>CMsgClientToGCSelectCompendiumInGamePredictionResponse.EResult</code> — values: 4</summary>

- Parent: `CMsgClientToGCSelectCompendiumInGamePredictionResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `INVALID_MATCH` | 1 |
| `PREDICTIONS_ARE_CLOSED` | 2 |
| `OTHER_ERROR` | 3 |

</details>

<details>
<summary><code>CMsgClientToGCOpenPlayerCardPackResponse.Result</code> — values: 7</summary>

- Parent: `CMsgClientToGCOpenPlayerCardPackResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 1 |
| `ERROR_INTERNAL` | 2 |
| `ERROR_FAILED_TO_FIND_PACK` | 3 |
| `ERROR_ITEM_NOT_CARD_PACK` | 4 |
| `ERROR_FAILED_CARD_CREATE` | 5 |
| `ERROR_INVALID_TEAM_ID_ATTRIBUTE` | 6 |
| `ERROR_INVALID_TEAM_ID` | 7 |

</details>

<details>
<summary><code>CMsgClientToGCRecyclePlayerCardResponse.Result</code> — values: 7</summary>

- Parent: `CMsgClientToGCRecyclePlayerCardResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 1 |
| `ERROR_INTERNAL` | 2 |
| `ERROR_FAILED_TO_FIND_PLAYER_CARD` | 3 |
| `ERROR_ITEM_NOT_PLAYER_CARD` | 4 |
| `ERROR_FAILED_DUST_CARD_CREATE` | 5 |
| `ERROR_CARD_LOCKED` | 6 |
| `ERROR_NO_CARDS_SPECIFIED` | 7 |

</details>

<details>
<summary><code>CMsgClientToGCCreatePlayerCardPackResponse.Result</code> — values: 7</summary>

- Parent: `CMsgClientToGCCreatePlayerCardPackResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 1 |
| `ERROR_INTERNAL` | 2 |
| `ERROR_INSUFFICIENT_DUST` | 3 |
| `ERROR_ITEM_NOT_DUST_ITEM` | 4 |
| `ERROR_FAILED_CARD_PACK_CREATE` | 5 |
| `ERROR_NO_CARD_PACK` | 6 |
| `ERROR_NOT_AVAILABLE` | 7 |

</details>

<details>
<summary><code>CMsgClientToGCCreateTeamPlayerCardPackResponse.Result</code> — values: 7</summary>

- Parent: `CMsgClientToGCCreateTeamPlayerCardPackResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 1 |
| `ERROR_INTERNAL` | 2 |
| `ERROR_INSUFFICIENT_DUST` | 3 |
| `ERROR_ITEM_NOT_DUST_ITEM` | 4 |
| `ERROR_FAILED_CARD_PACK_CREATE` | 5 |
| `ERROR_NO_CARD_PACK` | 6 |
| `ERROR_NOT_AVAILABLE` | 7 |

</details>

<details>
<summary><code>CMsgDOTAAnchorPhoneNumberResponse.Result</code> — values: 6</summary>

- Parent: `CMsgDOTAAnchorPhoneNumberResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `ERROR_UNKNOWN` | 1 |
| `ERROR_NO_STEAM_PHONE` | 2 |
| `ERROR_ALREADY_IN_USE` | 3 |
| `ERROR_COOLDOWN_ACTIVE` | 4 |
| `ERROR_GAC_ISSUE` | 5 |

</details>

<details>
<summary><code>CMsgDOTAUnanchorPhoneNumberResponse.Result</code> — values: 2</summary>

- Parent: `CMsgDOTAUnanchorPhoneNumberResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `ERROR_UNKNOWN` | 1 |

</details>

<details>
<summary><code>CMsgDOTASelectionPriorityChoiceResponse.Result</code> — values: 2</summary>

- Parent: `CMsgDOTASelectionPriorityChoiceResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `ERROR_UNKNOWN` | 1 |

</details>

<details>
<summary><code>CMsgDOTAGameAutographRewardResponse.Result</code> — values: 2</summary>

- Parent: `CMsgDOTAGameAutographRewardResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `ERROR_UNKNOWN` | 1 |

</details>

<details>
<summary><code>CMsgDOTADestroyLobbyResponse.Result</code> — values: 2</summary>

- Parent: `CMsgDOTADestroyLobbyResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `ERROR_UNKNOWN` | 1 |

</details>

<details>
<summary><code>CMsgPurchaseItemWithEventPointsResponse.Result</code> — values: 14</summary>

- Parent: `CMsgPurchaseItemWithEventPointsResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `UNKNOWN_EVENT` | 1 |
| `UNKNOWN_ITEM` | 2 |
| `BAD_QUANTITY` | 3 |
| `NOT_PURCHASEABLE` | 4 |
| `SDO_LOAD_FAILED` | 5 |
| `NOT_ENOUGH_POINTS` | 6 |
| `SQL_ERROR` | 7 |
| `FAILED_TO_SEND` | 8 |
| `SERVER_ERROR` | 9 |
| `NOT_ALLOWED` | 10 |
| `CANCELLED` | 11 |
| `CLIENT_ERROR` | 12 |
| `SUBSCRIPTION_REQUIRED` | 13 |

</details>

<details>
<summary><code>CMsgProfileResponse.EResponse</code> — values: 4</summary>

- Parent: `CMsgProfileResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |

</details>

<details>
<summary><code>CMsgProfileUpdateResponse.Result</code> — values: 5</summary>

- Parent: `CMsgProfileUpdateResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `FAILURE` | 1 |
| `FAILURE_BAD_HERO1` | 2 |
| `FAILURE_BAD_HERO2` | 3 |
| `FAILURE_BAD_HERO3` | 4 |

</details>

<details>
<summary><code>CMsgActivatePlusFreeTrialResponse.Result</code> — values: 5</summary>

- Parent: `CMsgActivatePlusFreeTrialResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `ERROR_GENERIC` | 1 |
| `ERROR_ALREADY_IN_FREE_TRIAL` | 2 |
| `ERROR_ALREADY_USED_FREE_TRIAL` | 3 |
| `ERROR_OFFER_NOT_VALID` | 4 |

</details>

<details>
<summary><code>CMsgClientToGCCavernCrawlClaimRoomResponse.Result</code> — values: 3</summary>

- Parent: `CMsgClientToGCCavernCrawlClaimRoomResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `ERROR_UNKNOWN` | 1 |
| `RECEIVED_ULTRA_RARE_REWARD` | 2 |

</details>

<details>
<summary><code>CMsgClientToGCCavernCrawlUseItemOnRoomResponse.Result</code> — values: 3</summary>

- Parent: `CMsgClientToGCCavernCrawlUseItemOnRoomResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `ERROR_UNKNOWN` | 1 |
| `RECEIVED_ULTRA_RARE_REWARD` | 2 |

</details>

<details>
<summary><code>CMsgClientToGCCavernCrawlUseItemOnPathResponse.Result</code> — values: 3</summary>

- Parent: `CMsgClientToGCCavernCrawlUseItemOnPathResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `ERROR_UNKNOWN` | 1 |
| `RECEIVED_ULTRA_RARE_REWARD` | 2 |

</details>

<details>
<summary><code>CMsgClientToGCCavernCrawlRequestMapStateResponse.Result</code> — values: 3</summary>

- Parent: `CMsgClientToGCCavernCrawlRequestMapStateResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `ERROR_UNKNOWN` | 1 |
| `EVENT_NOT_OWNED` | 2 |

</details>

<details>
<summary><code>CMsgClientToGCCavernCrawlGetClaimedRoomCountResponse.Result</code> — values: 3</summary>

- Parent: `CMsgClientToGCCavernCrawlGetClaimedRoomCountResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `ERROR_UNKNOWN` | 1 |
| `EVENT_NOT_OWNED` | 2 |

</details>

<details>
<summary><code>CMsgSocialFeedResponse.Result</code> — values: 6</summary>

- Parent: `CMsgSocialFeedResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `FAILED_TO_LOAD_FRIENDS` | 1 |
| `FAILED_TO_LOAD_FEED_DATA` | 2 |
| `FAILED_TO_LOAD_FEED_ENTRY` | 3 |
| `FAILED_TO_LOAD_COMMENTS` | 4 |
| `FAILED_TOO_MANY_REQUESTS` | 5 |

</details>

<details>
<summary><code>CMsgSocialFeedCommentsResponse.Result</code> — values: 3</summary>

- Parent: `CMsgSocialFeedCommentsResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `FAILED_TOO_MANY_REQUESTS` | 1 |
| `FAILED_TO_LOAD_COMMENTS` | 2 |

</details>

<details>
<summary><code>CMsgClientToGCPlayerCardSpecificPurchaseResponse.Result</code> — values: 6</summary>

- Parent: `CMsgClientToGCPlayerCardSpecificPurchaseResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 1 |
| `ERROR_INTERNAL` | 2 |
| `ERROR_INSUFFICIENT_DUST` | 3 |
| `ERROR_ITEM_NOT_DUST_ITEM` | 4 |
| `ERROR_FAILED_CARD_PACK_CREATE` | 5 |
| `ERROR_NOT_AVAILABLE` | 6 |

</details>

<details>
<summary><code>CMsgClientToGCRequestContestVotesResponse.EResponse</code> — values: 4</summary>

- Parent: `CMsgClientToGCRequestContestVotesResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |

</details>

<details>
<summary><code>CMsgGCToClientRecordContestVoteResponse.EResult</code> — values: 6</summary>

- Parent: `CMsgGCToClientRecordContestVoteResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `FAILED_EVENT_NOT_OWNED` | 1 |
| `FAILED_SQL_INSERT_FAILED` | 2 |
| `FAILED_INVALID_CONTEST` | 3 |
| `FAILED_CONTEST_NOT_ACTIVE` | 4 |
| `FAILED_TIMEOUT` | 5 |

</details>

<details>
<summary><code>CMsgGCToClientGetFilteredPlayersResponse.Result</code> — values: 2</summary>

- Parent: `CMsgGCToClientGetFilteredPlayersResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `FAILURE` | 1 |

</details>

<details>
<summary><code>CMsgGCToClientRemoveFilteredPlayerResponse.Result</code> — values: 2</summary>

- Parent: `CMsgGCToClientRemoveFilteredPlayerResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `FAILURE` | 1 |

</details>

<details>
<summary><code>CMsgGCToClientPurchaseFilteredPlayerSlotResponse.Result</code> — values: 4</summary>

- Parent: `CMsgGCToClientPurchaseFilteredPlayerSlotResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `FAILURE` | 1 |
| `CURRENT_SLOTCOUNT_DOESNT_MATCH` | 2 |
| `CANT_AFFORD` | 3 |

</details>

<details>
<summary><code>CMsgGCToClientUpdateFilteredPlayerNoteResponse.Result</code> — values: 3</summary>

- Parent: `CMsgGCToClientUpdateFilteredPlayerNoteResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `FAILURE` | 1 |
| `NOT_FOUND` | 2 |

</details>

<details>
<summary><code>CMsgClientToGCUpdatePartyBeacon.Action</code> — values: 2</summary>

- Parent: `CMsgClientToGCUpdatePartyBeacon`

| Name | Number |
|---|---:|
| `ON` | 0 |
| `OFF` | 1 |

</details>

<details>
<summary><code>CMsgGCToClientRequestActiveBeaconPartiesResponse.EResponse</code> — values: 3</summary>

- Parent: `CMsgGCToClientRequestActiveBeaconPartiesResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `FAILURE` | 1 |
| `BUSY` | 2 |

</details>

<details>
<summary><code>CMsgGCToClientJoinPartyFromBeaconResponse.EResponse</code> — values: 4</summary>

- Parent: `CMsgGCToClientJoinPartyFromBeaconResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `FAILURE` | 1 |
| `BUSY` | 2 |
| `NOT_LEADER` | 3 |

</details>

<details>
<summary><code>CMsgClientToGCManageFavorites.Action</code> — values: 2</summary>

- Parent: `CMsgClientToGCManageFavorites`

| Name | Number |
|---|---:|
| `ADD` | 0 |
| `REMOVE` | 1 |

</details>

<details>
<summary><code>CMsgGCToClientManageFavoritesResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgGCToClientManageFavoritesResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `FAILURE` | 1 |
| `NO_INVITE_PRESENT` | 2 |
| `INVITE_SENT` | 3 |
| `EXPIRED` | 4 |
| `BUSY` | 5 |

</details>

<details>
<summary><code>CMsgGCToClientGetFavoritePlayersResponse.EResponse</code> — values: 2</summary>

- Parent: `CMsgGCToClientGetFavoritePlayersResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `FAILURE` | 1 |

</details>

<details>
<summary><code>CMsgClientToGCRequestPlayerRecentAccomplishmentsResponse.EResponse</code> — values: 4</summary>

- Parent: `CMsgClientToGCRequestPlayerRecentAccomplishmentsResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |

</details>

<details>
<summary><code>CMsgClientToGCRequestPlayerHeroRecentAccomplishmentsResponse.EResponse</code> — values: 4</summary>

- Parent: `CMsgClientToGCRequestPlayerHeroRecentAccomplishmentsResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |

</details>

<details>
<summary><code>CMsgClientToGCSubmitPlayerMatchSurveyResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCSubmitPlayerMatchSurveyResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eAlreadySubmitted` | 4 |
| `k_ePlayerNotValid` | 5 |

</details>

<details>
<summary><code>CMsgClientToGCRequestReporterUpdatesResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCRequestReporterUpdatesResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTimeout` | 2 |
| `k_eTooBusy` | 3 |
| `k_eNotPermitted` | 4 |
| `k_eNotToSoon` | 5 |
| `k_eNotValid` | 6 |

</details>

<details>
<summary><code>CMsgClientToGCRecalibrateMMRResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCRecalibrateMMRResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTimeout` | 2 |
| `k_eTooBusy` | 3 |
| `k_eNotPermitted` | 4 |
| `k_eNotToSoon` | 5 |
| `k_eNotValid` | 6 |

</details>

<details>
<summary><code>CMsgClientToGCGetOWMatchDetailsResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCGetOWMatchDetailsResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTimeout` | 2 |
| `k_eTooBusy` | 3 |
| `k_eNotPermitted` | 4 |
| `k_eNoCaseAvailable` | 5 |

</details>

<details>
<summary><code>CMsgClientToGCSubmitOWConvictionResponse.EResponse</code> — values: 8</summary>

- Parent: `CMsgClientToGCSubmitOWConvictionResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTimeout` | 2 |
| `k_eTooBusy` | 3 |
| `k_eNotPermitted` | 4 |
| `k_eInvalidReplayID` | 5 |
| `k_eInvalidConviction` | 6 |
| `k_eInvalidPlayerSlot` | 7 |

</details>

<details>
<summary><code>CMsgClientToGCGetDPCFavoritesResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCGetDPCFavoritesResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidRequest` | 5 |

</details>

<details>
<summary><code>CMsgClientToGCSetDPCFavoriteStateResponse.EResponse</code> — values: 9</summary>

- Parent: `CMsgClientToGCSetDPCFavoriteStateResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eFavoriteTypeOutOfRange` | 2 |
| `k_eLockFailed` | 3 |
| `k_eAlreadyFavorited` | 4 |
| `k_eAlreadyUnfavorited` | 5 |
| `k_eInsertRecordFailed` | 6 |
| `k_eRemoveRecordFailed` | 7 |
| `k_eTimeout` | 8 |

</details>

<details>
<summary><code>CMsgClientToGCSetEventActiveSeasonIDResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCSetEventActiveSeasonIDResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eDisabled` | 2 |
| `k_eTooBusy` | 3 |
| `k_eNotAllowed` | 4 |
| `k_eTimeout` | 5 |
| `k_eInternalSuccessNoChange` | 6 |

</details>

<details>
<summary><code>CMsgClientToGCPurchaseLabyrinthBlessingsResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCPurchaseLabyrinthBlessingsResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eNoSuchBlessing` | 2 |
| `k_eNotEnoughShards` | 3 |
| `k_eNoPath` | 4 |
| `k_eTimeout` | 5 |

</details>

<details>
<summary><code>CMsgClientToGCGetStickerbookResponse.EResponse</code> — values: 5</summary>

- Parent: `CMsgClientToGCGetStickerbookResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTimeout` | 2 |
| `k_eNotAllowed` | 3 |
| `k_eTooBusy` | 4 |

</details>

<details>
<summary><code>CMsgClientToGCCreateStickerbookPageResponse.EResponse</code> — values: 5</summary>

- Parent: `CMsgClientToGCCreateStickerbookPageResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTimeout` | 2 |
| `k_eTooManyPages` | 3 |
| `k_eTooBusy` | 4 |

</details>

<details>
<summary><code>CMsgClientToGCDeleteStickerbookPageResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCDeleteStickerbookPageResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTimeout` | 2 |
| `k_eInvalidStickerCount` | 3 |
| `k_eTooBusy` | 4 |
| `k_eInvalidStickerMax` | 5 |
| `k_eInvalidPage` | 6 |

</details>

<details>
<summary><code>CMsgClientToGCPlaceStickersResponse.EResponse</code> — values: 9</summary>

- Parent: `CMsgClientToGCPlaceStickersResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTimeout` | 2 |
| `k_eMissingItem` | 3 |
| `k_eTooBusy` | 4 |
| `k_eDuplicateItem` | 5 |
| `k_eInvalidPage` | 6 |
| `k_ePageTypeMismatch` | 7 |
| `k_eTooManyStickers` | 8 |

</details>

<details>
<summary><code>CMsgClientToGCPlaceCollectionStickersResponse.EResponse</code> — values: 11</summary>

- Parent: `CMsgClientToGCPlaceCollectionStickersResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTimeout` | 2 |
| `k_eMissingItem` | 3 |
| `k_eTooBusy` | 4 |
| `k_eDuplicateItem` | 5 |
| `k_eInvalidPage` | 6 |
| `k_ePageTypeMismatch` | 7 |
| `k_eOldItemMismatch` | 8 |
| `k_eInvalidSlot` | 9 |
| `k_eSlotTypeMismatch` | 10 |

</details>

<details>
<summary><code>CMsgClientToGCOrderStickerbookTeamPageResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCOrderStickerbookTeamPageResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTimeout` | 2 |
| `k_eTooManyPages` | 3 |
| `k_eTooBusy` | 4 |
| `k_eInvalidPage` | 5 |

</details>

<details>
<summary><code>CMsgClientToGCSetHeroStickerResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCSetHeroStickerResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTimeout` | 2 |
| `k_eMissingItem` | 3 |
| `k_eTooBusy` | 4 |
| `k_eOldItemMismatch` | 5 |
| `k_eInvalidHero` | 6 |

</details>

<details>
<summary><code>CMsgClientToGCGetHeroStickersResponse.EResponse</code> — values: 4</summary>

- Parent: `CMsgClientToGCGetHeroStickersResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTimeout` | 2 |
| `k_eTooBusy` | 4 |

</details>

<details>
<summary><code>CMsgClientToGCSetFavoritePageResponse.EResponse</code> — values: 5</summary>

- Parent: `CMsgClientToGCSetFavoritePageResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTimeout` | 2 |
| `k_eTooBusy` | 4 |
| `k_eInvalidPage` | 5 |

</details>

<details>
<summary><code>CMsgClientToGCClaimSwagResponse.EResponse</code> — values: 10</summary>

- Parent: `CMsgClientToGCClaimSwagResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTimeout` | 2 |
| `k_eTooBusy` | 4 |
| `k_eAlreadyClaimed` | 5 |
| `k_eDisabled` | 6 |
| `k_eInvalidRequest` | 7 |
| `k_eUserNotEligible` | 8 |
| `k_eStorageError` | 9 |
| `k_eRewardDisabled` | 10 |

</details>

<details>
<summary><code>CMsgGCToClientCollectorsCacheAvailableDataResponse.Vote.EVoteType</code> — values: 2</summary>

- Parent: `CMsgGCToClientCollectorsCacheAvailableDataResponse.Vote`

| Name | Number |
|---|---:|
| `k_eUp` | 0 |
| `k_eDown` | 1 |

</details>

<details>
<summary><code>CMsgGCToClientUploadMatchClipResponse.EResponse</code> — values: 4</summary>

- Parent: `CMsgGCToClientUploadMatchClipResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTimeout` | 2 |
| `k_eTooBusy` | 4 |

</details>

<details>
<summary><code>CMsgGCToClientMapStatsResponse.EResponse</code> — values: 2</summary>

- Parent: `CMsgGCToClientMapStatsResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |

</details>

<details>
<summary><code>CMsgClientToGCRoadToTIGetQuestsResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCRoadToTIGetQuestsResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidID` | 5 |

</details>

<details>
<summary><code>CMsgClientToGCRoadToTIGetActiveQuestResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCRoadToTIGetActiveQuestResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eNone` | 2 |
| `k_eTooBusy` | 3 |
| `k_eDisabled` | 4 |
| `k_eTimeout` | 5 |
| `k_eInvalidID` | 6 |

</details>

<details>
<summary><code>CMsgClientToGCRoadToTIUseItemResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCRoadToTIUseItemResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eBadInput` | 2 |
| `k_eNoItem` | 3 |
| `k_eDisabled` | 4 |
| `k_eTimeout` | 5 |
| `k_eInvalidID` | 6 |

</details>

<details>
<summary><code>CMsgGCRankedPlayerInfoSubmitResponse.EResult</code> — values: 2</summary>

- Parent: `CMsgGCRankedPlayerInfoSubmitResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `ERROR_UNSPECIFIED` | 1 |

</details>

<details>
<summary><code>CMsgDOTAClaimGatedEventResponse.ResultCode</code> — values: 7</summary>

- Parent: `CMsgDOTAClaimGatedEventResponse`

| Name | Number |
|---|---:|
| `Success` | 0 |
| `InvalidEvent` | 1 |
| `EventNotActive` | 2 |
| `UserIneligible` | 3 |
| `AlreadyClaimed` | 4 |
| `ServerError` | 5 |
| `RateLimit` | 6 |

</details>

<details>
<summary><code>CMsgClientToGCGetEventCouponResponse.ResultCode</code> — values: 7</summary>

- Parent: `CMsgClientToGCGetEventCouponResponse`

| Name | Number |
|---|---:|
| `Success` | 0 |
| `InvalidEvent` | 1 |
| `EventNotActive` | 2 |
| `UserIneligible` | 3 |
| `ServerError` | 4 |
| `Timeout` | 5 |
| `MultipleCoupons` | 6 |

</details>

<details>
<summary><code>CMsgClientToGCConvertEventPointsResponse.ResultCode</code> — values: 6</summary>

- Parent: `CMsgClientToGCConvertEventPointsResponse`

| Name | Number |
|---|---:|
| `Success` | 0 |
| `InvalidEvent` | 1 |
| `EventNotActive` | 2 |
| `UserIneligible` | 3 |
| `ServerError` | 4 |
| `Timeout` | 5 |

</details>
