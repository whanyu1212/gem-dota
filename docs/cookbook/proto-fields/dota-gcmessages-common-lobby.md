# dota_gcmessages_common_lobby.proto

- Module: `dota_gcmessages_common_lobby_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **3**
- Messages: **32** (top-level: 26)
- Enums: **5** (top-level: 3)

## Imports

- `steammessages.proto`
- `dota_shared_enums.proto`
- `gcsdk_gcmessages.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgLobbyCoachFriendRequest</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `coach_account_id` | `uint32` | `optional` | `` |  |
| 2 | `player_account_id` | `uint32` | `optional` | `` |  |
| 3 | `request_state` | `.ELobbyMemberCoachRequestState` | `optional` | `` | default = k_eLobbyMemberCoachRequestState_None |

</details>

<details>
<summary><code>CMsgLobbyPlayerPlusSubscriptionData</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_badges` | `.CMsgLobbyPlayerPlusSubscriptionData.HeroBadge` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgLobbyPlayerPlusSubscriptionData.HeroBadge</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgLobbyPlayerPlusSubscriptionData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `hero_badge_xp` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgEventActionData</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `action_id` | `uint32` | `optional` | `` |  |
| 2 | `action_score` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPeriodicResourceData</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `periodic_resource_id` | `uint32` | `optional` | `` |  |
| 2 | `remaining` | `uint32` | `optional` | `` |  |
| 3 | `max` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgLobbyEventPoints</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |
| 2 | `account_points` | `.CMsgLobbyEventPoints.AccountPoints` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgLobbyEventPoints.AccountPoints</code> — fields: 14; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgLobbyEventPoints`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `normal_points` | `uint32` | `optional` | `` |  |
| 3 | `premium_points` | `uint32` | `optional` | `` |  |
| 4 | `owned` | `bool` | `optional` | `` |  |
| 7 | `event_level` | `uint32` | `optional` | `` |  |
| 12 | `active_effects_mask` | `uint64` | `optional` | `` |  |
| 23 | `wager_streak` | `uint32` | `optional` | `` |  |
| 25 | `event_game_custom_actions` | `.CMsgEventActionData` | `repeated` | `` |  |
| 26 | `tip_amount_index` | `uint32` | `optional` | `` |  |
| 27 | `active_event_season_id` | `uint32` | `optional` | `` |  |
| 28 | `teleport_fx_level` | `uint32` | `optional` | `` |  |
| 30 | `networked_event_actions` | `.CMsgEventActionData` | `repeated` | `` |  |
| 31 | `periodic_resources` | `.CMsgPeriodicResourceData` | `repeated` | `` |  |
| 32 | `extra_event_messages` | `.CExtraMsgBlock` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgLobbyEventGameData</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `game_seed` | `uint32` | `optional` | `` |  |
| 2 | `event_window_start_time` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CSODOTALobbyInvite</code> — fields: 8; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `group_id` | `uint64` | `optional` | `` | (key_field) = true |
| 2 | `sender_id` | `fixed64` | `optional` | `` |  |
| 3 | `sender_name` | `string` | `optional` | `` |  |
| 4 | `members` | `.CSODOTALobbyInvite.LobbyMember` | `repeated` | `` |  |
| 5 | `custom_game_id` | `uint64` | `optional` | `` |  |
| 6 | `invite_gid` | `fixed64` | `optional` | `` |  |
| 7 | `custom_game_crc` | `fixed64` | `optional` | `` |  |
| 8 | `custom_game_timestamp` | `fixed32` | `optional` | `` |  |

</details>

<details>
<summary><code>CSODOTALobbyInvite.LobbyMember</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CSODOTALobbyInvite`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `steam_id` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CSODOTALobbyMember</code> — fields: 14; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `id` | `fixed64` | `optional` | `` | (key_field) = true |
| 2 | `hero_id` | `int32` | `optional` | `` |  |
| 3 | `team` | `.DOTA_GC_TEAM` | `optional` | `` | default = DOTA_GC_TEAM_GOOD_GUYS |
| 7 | `slot` | `uint32` | `optional` | `` |  |
| 16 | `leaver_status` | `.DOTALeaverStatus_t` | `optional` | `` | default = DOTA_LEAVER_NONE |
| 23 | `coach_team` | `.DOTA_GC_TEAM` | `optional` | `` | default = DOTA_GC_TEAM_NOTEAM |
| 28 | `leaver_actions` | `uint32` | `optional` | `` |  |
| 31 | `custom_game_product_ids` | `uint32` | `repeated` | `` |  |
| 40 | `live_spectator_team` | `.DOTA_GC_TEAM` | `optional` | `` | default = DOTA_GC_TEAM_NOTEAM |
| 44 | `pending_awards` | `.CMsgPendingEventAward` | `repeated` | `` |  |
| 45 | `pending_awards_on_victory` | `.CMsgPendingEventAward` | `repeated` | `` |  |
| 52 | `reports_available` | `uint32` | `optional` | `` |  |
| 55 | `live_spectator_account_id` | `uint32` | `optional` | `` |  |
| 56 | `comms_reports_available` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CSODOTAServerLobbyMember</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CSODOTAStaticLobbyMember</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `party_id` | `uint64` | `optional` | `` |  |
| 3 | `channel` | `uint32` | `optional` | `` | default = 6 |
| 4 | `cameraman` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CSODOTAServerStaticLobbyMember</code> — fields: 18; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steam_id` | `fixed64` | `optional` | `` |  |
| 3 | `rank_tier` | `int32` | `optional` | `` |  |
| 4 | `leaderboard_rank` | `int32` | `optional` | `` | default = -1 |
| 5 | `lane_selection_flags` | `int32` | `optional` | `` |  |
| 6 | `rank_mmr_boost_type` | `.EDOTAMMRBoostType` | `optional` | `` | default = k_EDOTAMMRBoostType_None |
| 7 | `coach_rating` | `int32` | `optional` | `` |  |
| 8 | `coached_account_ids` | `uint32` | `repeated` | `` |  |
| 9 | `was_mvp_last_game` | `bool` | `optional` | `` |  |
| 10 | `can_earn_rewards` | `bool` | `optional` | `` |  |
| 11 | `is_plus_subscriber` | `bool` | `optional` | `` |  |
| 12 | `favorite_team_packed` | `uint64` | `optional` | `` |  |
| 13 | `is_steam_china` | `bool` | `optional` | `` |  |
| 14 | `title` | `uint32` | `optional` | `` |  |
| 15 | `guild_id` | `uint32` | `optional` | `` |  |
| 16 | `disabled_random_hero_bits` | `fixed32` | `repeated` | `` |  |
| 17 | `disabled_hero_id` | `int32` | `repeated` | `` |  |
| 18 | `enabled_hero_id` | `int32` | `repeated` | `` |  |
| 19 | `banned_hero_ids` | `int32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CLobbyTeamDetails</code> — fields: 14; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team_name` | `string` | `optional` | `` |  |
| 3 | `team_tag` | `string` | `optional` | `` |  |
| 4 | `team_id` | `uint32` | `optional` | `` |  |
| 5 | `team_logo` | `uint64` | `optional` | `` |  |
| 6 | `team_base_logo` | `uint64` | `optional` | `` |  |
| 7 | `team_banner_logo` | `uint64` | `optional` | `` |  |
| 8 | `team_complete` | `bool` | `optional` | `` |  |
| 15 | `rank` | `uint32` | `optional` | `` |  |
| 16 | `rank_change` | `sint32` | `optional` | `` |  |
| 17 | `is_home_team` | `bool` | `optional` | `` |  |
| 18 | `is_challenge_match` | `bool` | `optional` | `` |  |
| 19 | `challenge_match_token_account` | `uint64` | `optional` | `` |  |
| 20 | `team_logo_url` | `string` | `optional` | `` |  |
| 21 | `team_abbreviation` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CLobbyGuildDetails</code> — fields: 11; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `guild_primary_color` | `uint32` | `optional` | `` |  |
| 3 | `guild_secondary_color` | `uint32` | `optional` | `` |  |
| 4 | `guild_pattern` | `uint32` | `optional` | `` |  |
| 5 | `guild_logo` | `uint64` | `optional` | `` |  |
| 6 | `guild_points` | `uint32` | `optional` | `` |  |
| 7 | `guild_event` | `uint32` | `optional` | `` |  |
| 8 | `guild_flags` | `uint32` | `optional` | `` |  |
| 9 | `team_for_guild` | `.DOTA_GC_TEAM` | `optional` | `` | default = DOTA_GC_TEAM_GOOD_GUYS |
| 10 | `guild_tag` | `string` | `optional` | `` |  |
| 11 | `guild_weekly_percentile` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CLobbyTimedRewardDetails</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `item_def_index` | `uint32` | `optional` | `` |  |
| 3 | `is_supply_crate` | `bool` | `optional` | `` |  |
| 4 | `is_timed_drop` | `bool` | `optional` | `` |  |
| 5 | `account_id` | `uint32` | `optional` | `` |  |
| 6 | `origin` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CLobbyBroadcastChannelInfo</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

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
<summary><code>CLobbyGuildChallenge</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 3 | `challenge_instance_id` | `uint32` | `optional` | `` |  |
| 4 | `challenge_parameter` | `uint32` | `optional` | `` |  |
| 5 | `challenge_timestamp` | `uint32` | `optional` | `` |  |
| 6 | `challenge_period_serial` | `uint32` | `optional` | `` |  |
| 7 | `challenge_progress_at_start` | `uint32` | `optional` | `` |  |
| 8 | `eligible_account_ids` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTALobbyMatchQualityData</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `overall_quality` | `uint32` | `optional` | `` |  |
| 2 | `team_balance` | `uint32` | `optional` | `` |  |
| 3 | `match_skill_range` | `uint32` | `optional` | `` |  |
| 4 | `match_behavior` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CSODOTALobby</code> — fields: 91; oneofs: 0; nested messages: 1; nested enums: 2</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `lobby_id` | `uint64` | `optional` | `` | (key_field) = true |
| 3 | `game_mode` | `uint32` | `optional` | `` |  |
| 4 | `state` | `.CSODOTALobby.State` | `optional` | `` | default = UI |
| 5 | `connect` | `string` | `optional` | `` |  |
| 6 | `server_id` | `fixed64` | `optional` | `` | default = 0 |
| 10 | `pending_invites` | `fixed64` | `repeated` | `` |  |
| 11 | `leader_id` | `fixed64` | `optional` | `` |  |
| 12 | `lobby_type` | `.CSODOTALobby.LobbyType` | `optional` | `` | default = INVALID |
| 13 | `allow_cheats` | `bool` | `optional` | `` |  |
| 14 | `fill_with_bots` | `bool` | `optional` | `` |  |
| 16 | `game_name` | `string` | `optional` | `` |  |
| 17 | `team_details` | `.CLobbyTeamDetails` | `repeated` | `` |  |
| 19 | `tournament_id` | `uint32` | `optional` | `` |  |
| 20 | `tournament_game_id` | `uint32` | `optional` | `` |  |
| 21 | `server_region` | `uint32` | `optional` | `` | default = 0 |
| 22 | `game_state` | `.DOTA_GameState` | `optional` | `` | default = DOTA_GAMERULES_STATE_INIT |
| 23 | `num_spectators` | `uint32` | `optional` | `` |  |
| 25 | `matchgroup` | `uint32` | `optional` | `` |  |
| 28 | `cm_pick` | `.DOTA_CM_PICK` | `optional` | `` | default = DOTA_CM_RANDOM |
| 30 | `match_id` | `uint64` | `optional` | `` |  |
| 31 | `allow_spectating` | `bool` | `optional` | `` | default = true |
| 36 | `bot_difficulty_radiant` | `.DOTABotDifficulty` | `optional` | `` | default = BOT_DIFFICULTY_HARD |
| 39 | `pass_key` | `string` | `optional` | `` |  |
| 42 | `leagueid` | `uint32` | `optional` | `` |  |
| 43 | `penalty_level_radiant` | `uint32` | `optional` | `` | default = 0 |
| 44 | `penalty_level_dire` | `uint32` | `optional` | `` | default = 0 |
| 46 | `series_type` | `uint32` | `optional` | `` |  |
| 47 | `radiant_series_wins` | `uint32` | `optional` | `` |  |
| 48 | `dire_series_wins` | `uint32` | `optional` | `` |  |
| 51 | `allchat` | `bool` | `optional` | `` | default = false |
| 53 | `dota_tv_delay` | `.LobbyDotaTVDelay` | `optional` | `` | default = LobbyDotaTV_10 |
| 54 | `custom_game_mode` | `string` | `optional` | `` |  |
| 55 | `custom_map_name` | `string` | `optional` | `` |  |
| 56 | `custom_difficulty` | `uint32` | `optional` | `` |  |
| 57 | `lan` | `bool` | `optional` | `` |  |
| 58 | `broadcast_channel_info` | `.CLobbyBroadcastChannelInfo` | `repeated` | `` |  |
| 59 | `first_leaver_accountid` | `uint32` | `optional` | `` |  |
| 60 | `series_id` | `uint32` | `optional` | `` |  |
| 61 | `low_priority` | `bool` | `optional` | `` |  |
| 62 | `extra_messages` | `.CSODOTALobby.CExtraMsg` | `repeated` | `` |  |
| 65 | `first_blood_happened` | `bool` | `optional` | `` |  |
| 67 | `mass_disconnect` | `bool` | `optional` | `` |  |
| 68 | `custom_game_id` | `uint64` | `optional` | `` |  |
| 70 | `match_outcome` | `.EMatchOutcome` | `optional` | `` | default = k_EMatchOutcome_Unknown |
| 71 | `custom_min_players` | `uint32` | `optional` | `` |  |
| 72 | `custom_max_players` | `uint32` | `optional` | `` |  |
| 75 | `visibility` | `.DOTALobbyVisibility` | `optional` | `` | default = DOTALobbyVisibility_Public |
| 76 | `custom_game_crc` | `fixed64` | `optional` | `` |  |
| 77 | `custom_game_auto_created_lobby` | `bool` | `optional` | `` |  |
| 80 | `custom_game_timestamp` | `fixed32` | `optional` | `` |  |
| 81 | `previous_series_matches` | `uint64` | `repeated` | `` |  |
| 82 | `previous_match_override` | `uint64` | `optional` | `` |  |
| 87 | `game_start_time` | `uint32` | `optional` | `` |  |
| 88 | `pause_setting` | `.LobbyDotaPauseSetting` | `optional` | `` | default = LobbyDotaPauseSetting_Unlimited |
| 90 | `weekend_tourney_division_id` | `uint32` | `optional` | `` |  |
| 91 | `weekend_tourney_skill_level` | `uint32` | `optional` | `` |  |
| 92 | `weekend_tourney_bracket_round` | `uint32` | `optional` | `` |  |
| 93 | `bot_difficulty_dire` | `.DOTABotDifficulty` | `optional` | `` | default = BOT_DIFFICULTY_HARD |
| 94 | `bot_radiant` | `uint64` | `optional` | `` |  |
| 95 | `bot_dire` | `uint64` | `optional` | `` |  |
| 96 | `event_progression_enabled` | `.EEvent` | `repeated` | `` |  |
| 97 | `selection_priority_rules` | `.DOTASelectionPriorityRules` | `optional` | `` | default = k_DOTASelectionPriorityRules_Manual |
| 98 | `series_previous_selection_priority_team_id` | `uint32` | `optional` | `` |  |
| 99 | `series_current_selection_priority_team_id` | `uint32` | `optional` | `` |  |
| 100 | `series_current_priority_team_choice` | `.DOTASelectionPriorityChoice` | `optional` | `` | default = k_DOTASelectionPriorityChoice_Invalid |
| 101 | `series_current_non_priority_team_choice` | `.DOTASelectionPriorityChoice` | `optional` | `` | default = k_DOTASelectionPriorityChoice_Invalid |
| 102 | `series_current_selection_priority_used_coin_toss` | `bool` | `optional` | `` |  |
| 103 | `current_primary_event` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 104 | `current_primary_event_for_display` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 105 | `emergency_disabled_hero_ids` | `int32` | `repeated` | `` |  |
| 106 | `custom_game_private_key` | `fixed64` | `optional` | `` |  |
| 107 | `custom_game_penalties` | `bool` | `optional` | `` |  |
| 109 | `lan_host_ping_location` | `string` | `optional` | `` |  |
| 110 | `league_node_id` | `uint32` | `optional` | `` |  |
| 111 | `match_duration` | `uint32` | `optional` | `` |  |
| 113 | `league_phase` | `uint32` | `optional` | `` |  |
| 116 | `experimental_gameplay_enabled` | `bool` | `optional` | `` |  |
| 117 | `guild_challenges` | `.CLobbyGuildChallenge` | `repeated` | `` |  |
| 118 | `guild_details` | `.CLobbyGuildDetails` | `repeated` | `` |  |
| 120 | `all_members` | `.CSODOTALobbyMember` | `repeated` | `` |  |
| 121 | `member_indices` | `uint32` | `repeated` | `` |  |
| 122 | `left_member_indices` | `uint32` | `repeated` | `` |  |
| 123 | `free_member_indices` | `uint32` | `repeated` | `` |  |
| 124 | `requested_hero_ids` | `int32` | `repeated` | `` |  |
| 125 | `coach_friend_requests` | `.CMsgLobbyCoachFriendRequest` | `repeated` | `` |  |
| 126 | `is_in_steam_china` | `bool` | `optional` | `` |  |
| 127 | `with_scenario_save` | `bool` | `optional` | `` |  |
| 128 | `lobby_creation_time` | `uint32` | `optional` | `` |  |
| 129 | `event_game_definition` | `string` | `optional` | `` |  |
| 131 | `match_quality_data` | `.CDOTALobbyMatchQualityData` | `optional` | `` |  |
| 132 | `requested_hero_teams` | `int32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CSODOTALobby.CExtraMsg</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CSODOTALobby`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `id` | `uint32` | `optional` | `` |  |
| 2 | `contents` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CSODOTAServerLobby</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `all_members` | `.CSODOTAServerLobbyMember` | `repeated` | `` |  |
| 2 | `extra_startup_messages` | `.CSODOTALobby.CExtraMsg` | `repeated` | `` |  |
| 3 | `broadcast_active` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CSODOTAStaticLobby</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `all_members` | `.CSODOTAStaticLobbyMember` | `repeated` | `` |  |
| 2 | `is_player_draft` | `bool` | `optional` | `` |  |
| 3 | `is_last_match_in_series` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CSODOTAServerStaticLobby</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `all_members` | `.CSODOTAServerStaticLobbyMember` | `repeated` | `` |  |
| 2 | `post_patch_strategy_time_buffer` | `float` | `optional` | `` |  |
| 3 | `lobby_event_points` | `.CMsgLobbyEventPoints` | `repeated` | `` |  |
| 4 | `broadcast_url` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgAdditionalLobbyStartupAccountData</code> — fields: 4; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `plus_data` | `.CMsgLobbyPlayerPlusSubscriptionData` | `optional` | `` |  |
| 3 | `unlocked_chat_wheel_message_ranges` | `.CMsgAdditionalLobbyStartupAccountData.ChatWheelMessageRange` | `repeated` | `` |  |
| 4 | `unlocked_ping_wheel_message_ranges` | `.CMsgAdditionalLobbyStartupAccountData.PingWheelMessageRange` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgAdditionalLobbyStartupAccountData.ChatWheelMessageRange</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgAdditionalLobbyStartupAccountData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `message_id_start` | `uint32` | `optional` | `` | default = 4294967295 |
| 2 | `message_id_end` | `uint32` | `optional` | `` | default = 4294967295 |

</details>

<details>
<summary><code>CMsgAdditionalLobbyStartupAccountData.PingWheelMessageRange</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgAdditionalLobbyStartupAccountData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `message_id_start` | `uint32` | `optional` | `` | default = 4294967295 |
| 2 | `message_id_end` | `uint32` | `optional` | `` | default = 4294967295 |

</details>

<details>
<summary><code>CMsgLobbyInitializationComplete</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgLobbyPlaytestDetails</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `json` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgLocalServerGuildData</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 3 | `guild_points` | `uint32` | `optional` | `` |  |
| 4 | `guild_logo` | `uint64` | `optional` | `` |  |
| 5 | `guild_primary_color` | `uint32` | `optional` | `` |  |
| 6 | `guild_secondary_color` | `uint32` | `optional` | `` |  |
| 7 | `guild_pattern` | `uint32` | `optional` | `` |  |
| 8 | `guild_flags` | `uint32` | `optional` | `` |  |
| 9 | `guild_weekly_percentile` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgLocalServerFakeLobbyData</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `event_points` | `.CMsgLobbyEventPoints` | `repeated` | `` |  |
| 3 | `is_plus_subscriber` | `bool` | `optional` | `` |  |
| 4 | `primary_event_id` | `uint32` | `optional` | `` |  |
| 5 | `favorite_team` | `uint32` | `optional` | `` |  |
| 6 | `favorite_team_quality` | `uint32` | `optional` | `` |  |
| 7 | `guild_info` | `.CMsgLocalServerGuildData` | `optional` | `` |  |
| 8 | `teleport_fx_level` | `uint32` | `optional` | `` |  |
| 9 | `additional_data` | `.CMsgAdditionalLobbyStartupAccountData` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>ELobbyMemberCoachRequestState</code> — values: 3</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eLobbyMemberCoachRequestState_None` | 0 |
| `k_eLobbyMemberCoachRequestState_Accepted` | 1 |
| `k_eLobbyMemberCoachRequestState_Rejected` | 2 |

</details>

<details>
<summary><code>LobbyDotaTVDelay</code> — values: 4</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `LobbyDotaTV_10` | 0 |
| `LobbyDotaTV_120` | 1 |
| `LobbyDotaTV_300` | 2 |
| `LobbyDotaTV_900` | 3 |

</details>

<details>
<summary><code>LobbyDotaPauseSetting</code> — values: 3</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `LobbyDotaPauseSetting_Unlimited` | 0 |
| `LobbyDotaPauseSetting_Limited` | 1 |
| `LobbyDotaPauseSetting_Disabled` | 2 |

</details>

<details>
<summary><code>CSODOTALobby.State</code> — values: 7</summary>

- Parent: `CSODOTALobby`

| Name | Number |
|---|---:|
| `UI` | 0 |
| `READYUP` | 4 |
| `SERVERSETUP` | 1 |
| `RUN` | 2 |
| `POSTGAME` | 3 |
| `NOTREADY` | 5 |
| `SERVERASSIGN` | 6 |

</details>

<details>
<summary><code>CSODOTALobby.LobbyType</code> — values: 12</summary>

- Parent: `CSODOTALobby`

| Name | Number |
|---|---:|
| `INVALID` | -1 |
| `CASUAL_MATCH` | 0 |
| `PRACTICE` | 1 |
| `COOP_BOT_MATCH` | 4 |
| `COMPETITIVE_MATCH` | 7 |
| `WEEKEND_TOURNEY` | 9 |
| `LOCAL_BOT_MATCH` | 10 |
| `SPECTATOR` | 11 |
| `EVENT_MATCH` | 12 |
| `NEW_PLAYER_POOL` | 14 |
| `FEATURED_GAMEMODE` | 15 |
| `AUTOMATED_BOT_ONLY_MATCH` | 16 |

</details>
