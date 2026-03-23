# dota_gcmessages_common.proto

- Module: `dota_gcmessages_common_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **4**
- Messages: **187** (top-level: 101)
- Enums: **29** (top-level: 12)

## Imports

- `steammessages.proto`
- `gcsdk_gcmessages.proto`
- `dota_shared_enums.proto`
- `networkbasetypes.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CSODOTAGameAccountClient</code> — fields: 56; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` | (key_field) = true |
| 3 | `wins` | `uint32` | `optional` | `` |  |
| 4 | `losses` | `uint32` | `optional` | `` |  |
| 12 | `xp` | `uint32` | `optional` | `` |  |
| 13 | `level` | `uint32` | `optional` | `` |  |
| 14 | `initial_skill` | `uint32` | `optional` | `` |  |
| 15 | `leaver_count` | `uint32` | `optional` | `` |  |
| 18 | `low_priority_until_date` | `uint32` | `optional` | `` |  |
| 20 | `prevent_text_chat_until_date` | `uint32` | `optional` | `` |  |
| 21 | `prevent_voice_until_date` | `uint32` | `optional` | `` |  |
| 22 | `last_abandoned_game_date` | `uint32` | `optional` | `` |  |
| 23 | `leaver_penalty_count` | `uint32` | `optional` | `` |  |
| 24 | `completed_game_streak` | `uint32` | `optional` | `` |  |
| 38 | `account_disabled_until_date` | `uint32` | `optional` | `` |  |
| 39 | `account_disabled_count` | `uint32` | `optional` | `` |  |
| 41 | `match_disabled_until_date` | `uint32` | `optional` | `` |  |
| 42 | `match_disabled_count` | `uint32` | `optional` | `` |  |
| 47 | `shutdownlawterminatetimestamp` | `uint32` | `optional` | `` |  |
| 48 | `low_priority_games_remaining` | `uint32` | `optional` | `` |  |
| 55 | `recruitment_level` | `uint32` | `optional` | `` |  |
| 56 | `has_new_notifications` | `bool` | `optional` | `` |  |
| 57 | `is_league_admin` | `bool` | `optional` | `` |  |
| 58 | `secondary_leaver_count` | `uint32` | `optional` | `` |  |
| 59 | `last_secondary_abandoned_game_date` | `uint32` | `optional` | `` |  |
| 60 | `casual_games_played` | `uint32` | `optional` | `` |  |
| 61 | `solo_competitive_games_played` | `uint32` | `optional` | `` |  |
| 62 | `party_competitive_games_played` | `uint32` | `optional` | `` |  |
| 65 | `casual_1v1_games_played` | `uint32` | `optional` | `` |  |
| 67 | `curr_all_hero_challenge_id` | `int32` | `optional` | `` |  |
| 68 | `play_time_points` | `uint32` | `optional` | `` |  |
| 69 | `account_flags` | `uint32` | `optional` | `` |  |
| 70 | `play_time_level` | `uint32` | `optional` | `` |  |
| 71 | `player_behavior_seq_num_last_report` | `uint32` | `optional` | `` |  |
| 72 | `player_behavior_score_last_report` | `uint32` | `optional` | `` |  |
| 73 | `player_behavior_report_old_data` | `bool` | `optional` | `` |  |
| 74 | `tourney_skill_level` | `uint32` | `optional` | `` |  |
| 85 | `tourney_recent_participation_date` | `uint32` | `optional` | `` |  |
| 86 | `prevent_public_text_chat_until_date` | `uint32` | `optional` | `` |  |
| 88 | `anchored_phone_number_id` | `uint64` | `optional` | `` |  |
| 89 | `ranked_matchmaking_ban_until_date` | `uint32` | `optional` | `` |  |
| 90 | `recent_game_time_1` | `uint32` | `optional` | `` |  |
| 91 | `recent_game_time_2` | `uint32` | `optional` | `` |  |
| 92 | `recent_game_time_3` | `uint32` | `optional` | `` |  |
| 103 | `favorite_team_packed` | `uint64` | `optional` | `` |  |
| 104 | `recent_report_time` | `uint32` | `optional` | `` |  |
| 105 | `custom_game_disabled_until_date` | `uint32` | `optional` | `` |  |
| 106 | `recent_win_time_1` | `uint32` | `optional` | `` |  |
| 107 | `recent_win_time_2` | `uint32` | `optional` | `` |  |
| 108 | `recent_win_time_3` | `uint32` | `optional` | `` |  |
| 109 | `coach_rating` | `uint32` | `optional` | `` |  |
| 114 | `queue_points` | `uint32` | `optional` | `` |  |
| 115 | `role_handicaps` | `.CSODOTAGameAccountClient.RoleHandicap` | `repeated` | `` |  |
| 120 | `event_mode_recent_time` | `uint32` | `optional` | `` |  |
| 121 | `mmr_recalibration_time` | `uint32` | `optional` | `` |  |
| 122 | `prevent_new_player_chat_until_date` | `uint32` | `optional` | `` |  |
| 123 | `banned_hero_ids` | `int32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CSODOTAGameAccountClient.RoleHandicap</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CSODOTAGameAccountClient`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `role` | `uint32` | `optional` | `` |  |
| 2 | `handicap` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CSODOTAGameAccountPlus</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` | (key_field) = true |
| 2 | `original_start_date` | `uint32` | `optional` | `` |  |
| 3 | `plus_flags` | `uint32` | `optional` | `` |  |
| 4 | `plus_status` | `uint32` | `optional` | `` |  |
| 5 | `prepaid_time_start` | `uint32` | `optional` | `` |  |
| 6 | `prepaid_time_balance` | `uint32` | `optional` | `` |  |
| 7 | `next_payment_date` | `fixed32` | `optional` | `` |  |
| 8 | `steam_agreement_id` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CSODOTAChatWheel</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `message_id` | `uint32` | `optional` | `` | default = 4294967295, (key_field) = true |

</details>

<details>
<summary><code>CMsgLobbyFeaturedGamemodeProgress</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `accounts` | `.CMsgLobbyFeaturedGamemodeProgress.AccountProgress` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgLobbyFeaturedGamemodeProgress.AccountProgress</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgLobbyFeaturedGamemodeProgress`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `current_value` | `uint32` | `optional` | `` |  |
| 3 | `max_value` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgBattleCupVictory</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `win_date` | `uint32` | `optional` | `` |  |
| 3 | `valid_until` | `uint32` | `optional` | `` |  |
| 4 | `skill_level` | `uint32` | `optional` | `` |  |
| 5 | `tournament_id` | `uint32` | `optional` | `` |  |
| 6 | `division_id` | `uint32` | `optional` | `` |  |
| 7 | `team_id` | `uint32` | `optional` | `` |  |
| 8 | `streak` | `uint32` | `optional` | `` |  |
| 9 | `trophy_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgLobbyBattleCupVictoryList</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `winners` | `.CMsgBattleCupVictory` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTABroadcastNotification</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `message` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CProtoItemHeroStatue</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `status_effect_index` | `uint32` | `optional` | `` |  |
| 3 | `sequence_name` | `string` | `optional` | `` |  |
| 4 | `cycle` | `float` | `optional` | `` |  |
| 5 | `wearable` | `uint32` | `repeated` | `` |  |
| 6 | `inscription` | `string` | `optional` | `` |  |
| 7 | `style` | `uint32` | `repeated` | `` |  |
| 8 | `tournament_drop` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMatchPlayerAbilityUpgrade</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ability` | `int32` | `optional` | `` | default = -1 |
| 2 | `time` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMatchPlayerTimedCustomStat</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `stat` | `.EDOTAMatchPlayerTimeCustomStat` | `optional` | `` | default = k_EDOTA_MatchPlayerTimeCustomStat_HPRegenUnderT1Towers |
| 3 | `value` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMatchPlayerTimedStats</code> — fields: 37; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `time` | `uint32` | `optional` | `` |  |
| 2 | `kills` | `uint32` | `optional` | `` |  |
| 3 | `deaths` | `uint32` | `optional` | `` |  |
| 4 | `assists` | `uint32` | `optional` | `` |  |
| 5 | `net_worth` | `uint32` | `optional` | `` |  |
| 6 | `xp` | `uint32` | `optional` | `` |  |
| 7 | `last_hits` | `uint32` | `optional` | `` |  |
| 8 | `denies` | `uint32` | `optional` | `` |  |
| 9 | `bounty_rune_gold` | `uint32` | `optional` | `` |  |
| 10 | `range_creep_upgrade_gold` | `uint32` | `optional` | `` |  |
| 11 | `observer_wards_dewarded` | `uint32` | `optional` | `` |  |
| 12 | `reliable_gold_earned` | `uint32` | `optional` | `` |  |
| 13 | `gold_loss_prevented` | `uint32` | `optional` | `` |  |
| 14 | `hero_kill_gold` | `uint32` | `optional` | `` |  |
| 15 | `creep_kill_gold` | `uint32` | `optional` | `` |  |
| 16 | `building_gold` | `uint32` | `optional` | `` |  |
| 17 | `other_gold` | `uint32` | `optional` | `` |  |
| 18 | `comeback_gold` | `uint32` | `optional` | `` |  |
| 19 | `experimental_gold` | `uint32` | `optional` | `` |  |
| 20 | `experimental2_gold` | `uint32` | `optional` | `` |  |
| 21 | `creep_deny_gold` | `uint32` | `optional` | `` |  |
| 22 | `tp_scrolls_purchased_1` | `uint32` | `optional` | `` |  |
| 23 | `tp_scrolls_purchased_2` | `uint32` | `optional` | `` |  |
| 24 | `tp_scrolls_purchased_3` | `uint32` | `optional` | `` |  |
| 25 | `tp_scrolls_purchased_4` | `uint32` | `optional` | `` |  |
| 26 | `tp_scrolls_purchased_5` | `uint32` | `optional` | `` |  |
| 27 | `neutral_gold` | `uint32` | `optional` | `` |  |
| 28 | `courier_gold` | `uint32` | `optional` | `` |  |
| 29 | `roshan_gold` | `uint32` | `optional` | `` |  |
| 30 | `income_gold` | `uint32` | `optional` | `` |  |
| 36 | `item_value` | `uint32` | `optional` | `` |  |
| 37 | `support_gold_spent` | `uint32` | `optional` | `` |  |
| 38 | `camps_stacked` | `uint32` | `optional` | `` |  |
| 39 | `wards_placed` | `uint32` | `optional` | `` |  |
| 40 | `triple_kills` | `uint32` | `optional` | `` |  |
| 41 | `rampages` | `uint32` | `optional` | `` |  |
| 42 | `custom_stats` | `.CMatchPlayerTimedCustomStat` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMatchTeamTimedStats</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `time` | `uint32` | `optional` | `` |  |
| 2 | `enemy_towers_killed` | `uint32` | `optional` | `` |  |
| 3 | `enemy_barracks_killed` | `uint32` | `optional` | `` |  |
| 4 | `enemy_towers_status` | `uint32` | `optional` | `` |  |
| 5 | `enemy_barracks_status` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMatchAdditionalUnitInventory</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `unit_name` | `string` | `optional` | `` |  |
| 2 | `items` | `int32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMatchPlayerPermanentBuff</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `permanent_buff` | `uint32` | `optional` | `` |  |
| 2 | `stack_count` | `uint32` | `optional` | `` |  |
| 3 | `grant_time` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMatchHeroSelectEvent</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `is_pick` | `bool` | `optional` | `` |  |
| 2 | `team` | `uint32` | `optional` | `` |  |
| 3 | `hero_id` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMatchClip</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `player_account_id` | `uint32` | `optional` | `` |  |
| 3 | `game_time_seconds` | `uint32` | `optional` | `` |  |
| 4 | `duration_seconds` | `uint32` | `optional` | `` |  |
| 5 | `player_id` | `uint32` | `optional` | `` |  |
| 6 | `hero_id` | `int32` | `optional` | `` |  |
| 7 | `ability_id` | `int32` | `optional` | `` | default = -1 |
| 8 | `camera_mode` | `uint32` | `optional` | `` |  |
| 9 | `comment` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CPartySearchClientParty</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `party_id` | `fixed64` | `optional` | `` |  |
| 2 | `beacon_type` | `int32` | `optional` | `` |  |
| 3 | `party_members` | `fixed32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAHasItemQuery</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `item_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAHasItemResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `has_item` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCGetPlayerCardItemInfo</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `player_card_item_ids` | `uint64` | `repeated` | `` |  |
| 3 | `all_for_event` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCGetPlayerCardItemInfoResponse</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_card_infos` | `.CMsgGCGetPlayerCardItemInfoResponse.PlayerCardInfo` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCGetPlayerCardItemInfoResponse.PlayerCardInfo</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCGetPlayerCardItemInfoResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_card_item_id` | `uint64` | `optional` | `` |  |
| 2 | `account_id` | `uint32` | `optional` | `` |  |
| 3 | `packed_bonuses` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CSODOTAMapLocationState</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` | (key_field) = true |
| 2 | `location_id` | `int32` | `optional` | `` | (key_field) = true |
| 3 | `completed` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgLeagueAdminList</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_ids` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAProfileCard</code> — fields: 15; oneofs: 0; nested messages: 1; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 3 | `slots` | `.CMsgDOTAProfileCard.Slot` | `repeated` | `` |  |
| 4 | `badge_points` | `uint32` | `optional` | `` |  |
| 6 | `event_id` | `uint32` | `optional` | `` |  |
| 7 | `recent_battle_cup_victory` | `.CMsgBattleCupVictory` | `optional` | `` |  |
| 8 | `rank_tier` | `uint32` | `optional` | `` |  |
| 9 | `leaderboard_rank` | `uint32` | `optional` | `` |  |
| 10 | `is_plus_subscriber` | `bool` | `optional` | `` |  |
| 11 | `plus_original_start_date` | `uint32` | `optional` | `` |  |
| 12 | `rank_tier_score` | `uint32` | `optional` | `` |  |
| 17 | `leaderboard_rank_core` | `uint32` | `optional` | `` |  |
| 23 | `title` | `uint32` | `optional` | `` |  |
| 24 | `favorite_team_packed` | `uint64` | `optional` | `` |  |
| 25 | `lifetime_games` | `uint32` | `optional` | `` |  |
| 26 | `event_level` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAProfileCard.Slot</code> — fields: 7; oneofs: 0; nested messages: 6; nested enums: 0</summary>

- Parent: `CMsgDOTAProfileCard`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `slot_id` | `uint32` | `optional` | `` |  |
| 2 | `trophy` | `.CMsgDOTAProfileCard.Slot.Trophy` | `optional` | `` |  |
| 3 | `stat` | `.CMsgDOTAProfileCard.Slot.Stat` | `optional` | `` |  |
| 4 | `item` | `.CMsgDOTAProfileCard.Slot.Item` | `optional` | `` |  |
| 5 | `hero` | `.CMsgDOTAProfileCard.Slot.Hero` | `optional` | `` |  |
| 6 | `emoticon` | `.CMsgDOTAProfileCard.Slot.Emoticon` | `optional` | `` |  |
| 7 | `team` | `.CMsgDOTAProfileCard.Slot.Team` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAProfileCard.Slot.Trophy</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAProfileCard.Slot`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `trophy_id` | `uint32` | `optional` | `` |  |
| 2 | `trophy_score` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAProfileCard.Slot.Stat</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAProfileCard.Slot`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `stat_id` | `.CMsgDOTAProfileCard.EStatID` | `optional` | `` | default = k_eStat_Wins |
| 2 | `stat_score` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAProfileCard.Slot.Item</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAProfileCard.Slot`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `serialized_item` | `bytes` | `optional` | `` |  |
| 2 | `item_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAProfileCard.Slot.Hero</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAProfileCard.Slot`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `hero_wins` | `uint32` | `optional` | `` |  |
| 3 | `hero_losses` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAProfileCard.Slot.Emoticon</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAProfileCard.Slot`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `emoticon_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAProfileCard.Slot.Team</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAProfileCard.Slot`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CSODOTAPlayerChallenge</code> — fields: 17; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` | (key_field) = true |
| 2 | `event_id` | `uint32` | `optional` | `` | (key_field) = true |
| 3 | `slot_id` | `uint32` | `optional` | `` | (key_field) = true |
| 5 | `int_param_0` | `uint32` | `optional` | `` |  |
| 6 | `int_param_1` | `uint32` | `optional` | `` |  |
| 7 | `created_time` | `uint32` | `optional` | `` |  |
| 8 | `completed` | `uint32` | `optional` | `` |  |
| 9 | `sequence_id` | `uint32` | `optional` | `` |  |
| 10 | `challenge_tier` | `uint32` | `optional` | `` |  |
| 11 | `flags` | `uint32` | `optional` | `` |  |
| 12 | `attempts` | `uint32` | `optional` | `` |  |
| 13 | `complete_limit` | `uint32` | `optional` | `` |  |
| 14 | `quest_rank` | `uint32` | `optional` | `` |  |
| 15 | `max_quest_rank` | `uint32` | `optional` | `` |  |
| 16 | `instance_id` | `uint32` | `optional` | `` |  |
| 17 | `hero_id` | `int32` | `optional` | `` |  |
| 18 | `template_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRerollPlayerChallenge</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 3 | `sequence_id` | `uint32` | `optional` | `` |  |
| 4 | `hero_id` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCRerollPlayerChallengeResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgGCRerollPlayerChallengeResponse.EResult` | `optional` | `` | default = eResult_Success |

</details>

<details>
<summary><code>CMsgGCTopCustomGamesList</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `top_custom_games` | `uint64` | `repeated` | `` |  |
| 2 | `game_of_the_day` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTARealtimeGameStats</code> — fields: 5; oneofs: 0; nested messages: 12; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match` | `.CMsgDOTARealtimeGameStats.MatchDetails` | `optional` | `` |  |
| 2 | `teams` | `.CMsgDOTARealtimeGameStats.TeamDetails` | `repeated` | `` |  |
| 3 | `buildings` | `.CMsgDOTARealtimeGameStats.BuildingDetails` | `repeated` | `` |  |
| 4 | `graph_data` | `.CMsgDOTARealtimeGameStats.GraphData` | `optional` | `` |  |
| 5 | `delta_frame` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTARealtimeGameStats.TeamDetails</code> — fields: 11; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTARealtimeGameStats`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team_number` | `uint32` | `optional` | `` |  |
| 2 | `team_id` | `uint32` | `optional` | `` |  |
| 3 | `team_name` | `string` | `optional` | `` |  |
| 4 | `team_logo` | `fixed64` | `optional` | `` |  |
| 5 | `score` | `uint32` | `optional` | `` |  |
| 6 | `players` | `.CMsgDOTARealtimeGameStats.PlayerDetails` | `repeated` | `` |  |
| 7 | `only_team` | `bool` | `optional` | `` |  |
| 8 | `cheers` | `uint32` | `optional` | `` |  |
| 9 | `net_worth` | `uint32` | `optional` | `` |  |
| 10 | `team_tag` | `string` | `optional` | `` |  |
| 11 | `team_logo_url` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTARealtimeGameStats.ItemDetails</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTARealtimeGameStats`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_ability_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `name` | `string` | `optional` | `` |  |
| 3 | `time` | `int32` | `optional` | `` |  |
| 4 | `sold` | `bool` | `optional` | `` |  |
| 5 | `stackcount` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTARealtimeGameStats.AbilityDetails</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTARealtimeGameStats`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `id` | `int32` | `optional` | `` | default = -1 |
| 2 | `name` | `string` | `optional` | `` |  |
| 3 | `level` | `uint32` | `optional` | `` |  |
| 4 | `cooldown` | `float` | `optional` | `` |  |
| 5 | `cooldown_max` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTARealtimeGameStats.HeroToHeroStats</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTARealtimeGameStats`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `victimid` | `int32` | `optional` | `` | default = -1 |
| 2 | `kills` | `uint32` | `optional` | `` |  |
| 3 | `assists` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTARealtimeGameStats.AbilityList</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTARealtimeGameStats`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `id` | `int32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTARealtimeGameStats.PlayerDetails</code> — fields: 50; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTARealtimeGameStats`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `accountid` | `uint32` | `optional` | `` |  |
| 2 | `playerid` | `int32` | `optional` | `` | default = -1 |
| 3 | `name` | `string` | `optional` | `` |  |
| 4 | `team` | `uint32` | `optional` | `` |  |
| 5 | `heroid` | `int32` | `optional` | `` |  |
| 6 | `healthpoints` | `uint32` | `optional` | `` |  |
| 7 | `maxhealthpoints` | `uint32` | `optional` | `` |  |
| 8 | `healthregenrate` | `float` | `optional` | `` |  |
| 9 | `manapoints` | `uint32` | `optional` | `` |  |
| 10 | `maxmanapoints` | `uint32` | `optional` | `` |  |
| 11 | `manaregenrate` | `float` | `optional` | `` |  |
| 12 | `base_strength` | `uint32` | `optional` | `` |  |
| 13 | `base_agility` | `uint32` | `optional` | `` |  |
| 14 | `base_intelligence` | `uint32` | `optional` | `` |  |
| 15 | `base_armor` | `int32` | `optional` | `` |  |
| 16 | `base_movespeed` | `uint32` | `optional` | `` |  |
| 17 | `base_damage` | `uint32` | `optional` | `` |  |
| 18 | `strength` | `uint32` | `optional` | `` |  |
| 19 | `agility` | `uint32` | `optional` | `` |  |
| 20 | `intelligence` | `uint32` | `optional` | `` |  |
| 21 | `armor` | `int32` | `optional` | `` |  |
| 22 | `movespeed` | `uint32` | `optional` | `` |  |
| 23 | `damage` | `uint32` | `optional` | `` |  |
| 24 | `hero_damage` | `uint32` | `optional` | `` |  |
| 25 | `tower_damage` | `uint32` | `optional` | `` |  |
| 26 | `abilities` | `.CMsgDOTARealtimeGameStats.AbilityDetails` | `repeated` | `` |  |
| 27 | `level` | `uint32` | `optional` | `` |  |
| 28 | `kill_count` | `uint32` | `optional` | `` |  |
| 29 | `death_count` | `uint32` | `optional` | `` |  |
| 30 | `assists_count` | `uint32` | `optional` | `` |  |
| 31 | `denies_count` | `uint32` | `optional` | `` |  |
| 32 | `lh_count` | `uint32` | `optional` | `` |  |
| 33 | `hero_healing` | `uint32` | `optional` | `` |  |
| 34 | `gold_per_min` | `uint32` | `optional` | `` |  |
| 35 | `xp_per_min` | `uint32` | `optional` | `` |  |
| 36 | `net_gold` | `uint32` | `optional` | `` |  |
| 37 | `gold` | `uint32` | `optional` | `` |  |
| 38 | `x` | `float` | `optional` | `` |  |
| 39 | `y` | `float` | `optional` | `` |  |
| 40 | `respawn_time` | `int32` | `optional` | `` |  |
| 41 | `ultimate_cooldown` | `uint32` | `optional` | `` |  |
| 42 | `has_buyback` | `bool` | `optional` | `` |  |
| 43 | `items` | `.CMsgDOTARealtimeGameStats.ItemDetails` | `repeated` | `` |  |
| 44 | `stashitems` | `.CMsgDOTARealtimeGameStats.ItemDetails` | `repeated` | `` |  |
| 45 | `itemshoppinglist` | `.CMsgDOTARealtimeGameStats.ItemDetails` | `repeated` | `` |  |
| 46 | `levelpoints` | `.CMsgDOTARealtimeGameStats.AbilityList` | `repeated` | `` |  |
| 47 | `hero_to_hero_stats` | `.CMsgDOTARealtimeGameStats.HeroToHeroStats` | `repeated` | `` |  |
| 48 | `has_ultimate` | `bool` | `optional` | `` |  |
| 49 | `has_ultimate_mana` | `bool` | `optional` | `` |  |
| 50 | `team_slot` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTARealtimeGameStats.BuildingDetails</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTARealtimeGameStats`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `team` | `uint32` | `optional` | `` |  |
| 3 | `heading` | `float` | `optional` | `` |  |
| 4 | `lane` | `uint32` | `optional` | `` |  |
| 5 | `tier` | `uint32` | `optional` | `` |  |
| 6 | `type` | `uint32` | `optional` | `` |  |
| 7 | `x` | `float` | `optional` | `` |  |
| 8 | `y` | `float` | `optional` | `` |  |
| 9 | `destroyed` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTARealtimeGameStats.KillDetails</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTARealtimeGameStats`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `death_time` | `int32` | `optional` | `` |  |
| 3 | `killer_player_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CMsgDOTARealtimeGameStats.BroadcasterDetails</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTARealtimeGameStats`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CMsgDOTARealtimeGameStats.PickBanDetails</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTARealtimeGameStats`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero` | `int32` | `optional` | `` |  |
| 2 | `team` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTARealtimeGameStats.MatchDetails</code> — fields: 21; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTARealtimeGameStats`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `server_steam_id` | `fixed64` | `optional` | `` |  |
| 2 | `match_id` | `uint64` | `optional` | `` |  |
| 3 | `timestamp` | `uint32` | `optional` | `` |  |
| 4 | `time_of_day` | `float` | `optional` | `` |  |
| 5 | `is_nightstalker_night` | `bool` | `optional` | `` |  |
| 6 | `game_time` | `int32` | `optional` | `` |  |
| 8 | `teamid_radiant` | `uint32` | `optional` | `` |  |
| 9 | `teamid_dire` | `uint32` | `optional` | `` |  |
| 10 | `picks` | `.CMsgDOTARealtimeGameStats.PickBanDetails` | `repeated` | `` |  |
| 11 | `bans` | `.CMsgDOTARealtimeGameStats.PickBanDetails` | `repeated` | `` |  |
| 12 | `kills` | `.CMsgDOTARealtimeGameStats.KillDetails` | `repeated` | `` |  |
| 13 | `broadcasters` | `.CMsgDOTARealtimeGameStats.BroadcasterDetails` | `repeated` | `` |  |
| 14 | `game_mode` | `uint32` | `optional` | `` |  |
| 15 | `league_id` | `uint32` | `optional` | `` |  |
| 16 | `single_team` | `bool` | `optional` | `` |  |
| 17 | `cheers_peak` | `uint32` | `optional` | `` |  |
| 18 | `league_node_id` | `uint32` | `optional` | `` |  |
| 19 | `game_state` | `uint32` | `optional` | `` |  |
| 20 | `lobby_type` | `uint32` | `optional` | `` |  |
| 21 | `start_timestamp` | `uint32` | `optional` | `` |  |
| 22 | `is_player_draft` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTARealtimeGameStats.GraphData</code> — fields: 6; oneofs: 0; nested messages: 2; nested enums: 2</summary>

- Parent: `CMsgDOTARealtimeGameStats`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `graph_gold` | `int32` | `repeated` | `` |  |
| 2 | `graph_xp` | `int32` | `repeated` | `` |  |
| 3 | `graph_kill` | `int32` | `repeated` | `` |  |
| 4 | `graph_tower` | `int32` | `repeated` | `` |  |
| 5 | `graph_rax` | `int32` | `repeated` | `` |  |
| 6 | `team_loc_stats` | `.CMsgDOTARealtimeGameStats.GraphData.TeamLocationStats` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTARealtimeGameStats.GraphData.LocationStats</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTARealtimeGameStats.GraphData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `stats` | `int32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTARealtimeGameStats.GraphData.TeamLocationStats</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTARealtimeGameStats.GraphData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `loc_stats` | `.CMsgDOTARealtimeGameStats.GraphData.LocationStats` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTARealtimeGameStatsTerse</code> — fields: 5; oneofs: 0; nested messages: 6; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match` | `.CMsgDOTARealtimeGameStatsTerse.MatchDetails` | `optional` | `` |  |
| 2 | `teams` | `.CMsgDOTARealtimeGameStatsTerse.TeamDetails` | `repeated` | `` |  |
| 3 | `buildings` | `.CMsgDOTARealtimeGameStatsTerse.BuildingDetails` | `repeated` | `` |  |
| 4 | `graph_data` | `.CMsgDOTARealtimeGameStatsTerse.GraphData` | `optional` | `` |  |
| 5 | `delta_frame` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTARealtimeGameStatsTerse.TeamDetails</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTARealtimeGameStatsTerse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team_number` | `uint32` | `optional` | `` |  |
| 2 | `team_id` | `uint32` | `optional` | `` |  |
| 3 | `team_name` | `string` | `optional` | `` |  |
| 4 | `team_logo` | `fixed64` | `optional` | `` |  |
| 5 | `score` | `uint32` | `optional` | `` |  |
| 6 | `players` | `.CMsgDOTARealtimeGameStatsTerse.PlayerDetails` | `repeated` | `` |  |
| 7 | `net_worth` | `uint32` | `optional` | `` |  |
| 8 | `team_tag` | `string` | `optional` | `` |  |
| 9 | `team_logo_url` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTARealtimeGameStatsTerse.PlayerDetails</code> — fields: 18; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTARealtimeGameStatsTerse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `accountid` | `uint32` | `optional` | `` |  |
| 2 | `playerid` | `int32` | `optional` | `` | default = -1 |
| 3 | `name` | `string` | `optional` | `` |  |
| 4 | `team` | `uint32` | `optional` | `` |  |
| 5 | `heroid` | `int32` | `optional` | `` |  |
| 6 | `level` | `uint32` | `optional` | `` |  |
| 7 | `kill_count` | `uint32` | `optional` | `` |  |
| 8 | `death_count` | `uint32` | `optional` | `` |  |
| 9 | `assists_count` | `uint32` | `optional` | `` |  |
| 10 | `denies_count` | `uint32` | `optional` | `` |  |
| 11 | `lh_count` | `uint32` | `optional` | `` |  |
| 12 | `gold` | `uint32` | `optional` | `` |  |
| 13 | `x` | `float` | `optional` | `` |  |
| 14 | `y` | `float` | `optional` | `` |  |
| 15 | `net_worth` | `uint32` | `optional` | `` |  |
| 16 | `abilities` | `int32` | `repeated` | `` |  |
| 17 | `items` | `int32` | `repeated` | `` |  |
| 18 | `team_slot` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTARealtimeGameStatsTerse.BuildingDetails</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTARealtimeGameStatsTerse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team` | `uint32` | `optional` | `` |  |
| 2 | `heading` | `float` | `optional` | `` |  |
| 3 | `type` | `uint32` | `optional` | `` |  |
| 4 | `lane` | `uint32` | `optional` | `` |  |
| 5 | `tier` | `uint32` | `optional` | `` |  |
| 6 | `x` | `float` | `optional` | `` |  |
| 7 | `y` | `float` | `optional` | `` |  |
| 8 | `destroyed` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTARealtimeGameStatsTerse.PickBanDetails</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTARealtimeGameStatsTerse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero` | `int32` | `optional` | `` |  |
| 2 | `team` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTARealtimeGameStatsTerse.MatchDetails</code> — fields: 14; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTARealtimeGameStatsTerse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `server_steam_id` | `fixed64` | `optional` | `` |  |
| 2 | `match_id` | `uint64` | `optional` | `` |  |
| 3 | `timestamp` | `uint32` | `optional` | `` |  |
| 4 | `game_time` | `int32` | `optional` | `` |  |
| 6 | `steam_broadcaster_account_ids` | `uint32` | `repeated` | `` |  |
| 7 | `game_mode` | `uint32` | `optional` | `` |  |
| 8 | `league_id` | `uint32` | `optional` | `` |  |
| 9 | `league_node_id` | `uint32` | `optional` | `` |  |
| 10 | `game_state` | `uint32` | `optional` | `` |  |
| 11 | `picks` | `.CMsgDOTARealtimeGameStatsTerse.PickBanDetails` | `repeated` | `` |  |
| 12 | `bans` | `.CMsgDOTARealtimeGameStatsTerse.PickBanDetails` | `repeated` | `` |  |
| 13 | `lobby_type` | `uint32` | `optional` | `` |  |
| 14 | `start_timestamp` | `uint32` | `optional` | `` |  |
| 15 | `is_player_draft` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTARealtimeGameStatsTerse.GraphData</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTARealtimeGameStatsTerse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `graph_gold` | `int32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTABroadcastTimelineEvent</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event` | `.EBroadcastTimelineEvent` | `optional` | `` | default = EBroadcastTimelineEvent_MatchStarted |
| 2 | `timestamp` | `fixed32` | `optional` | `` |  |
| 3 | `data` | `uint32` | `optional` | `` |  |
| 4 | `string_data` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientMatchGroupsVersion</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `matchgroups_version` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTASDOHeroStatsHistory</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `game_mode` | `uint32` | `optional` | `` |  |
| 3 | `lobby_type` | `uint32` | `optional` | `` |  |
| 4 | `start_time` | `uint32` | `optional` | `` |  |
| 5 | `won` | `bool` | `optional` | `` |  |
| 6 | `gpm` | `uint32` | `optional` | `` |  |
| 7 | `xpm` | `uint32` | `optional` | `` |  |
| 8 | `kills` | `uint32` | `optional` | `` |  |
| 9 | `deaths` | `uint32` | `optional` | `` |  |
| 10 | `assists` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPredictionChoice</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `value` | `uint32` | `optional` | `` |  |
| 2 | `name` | `string` | `optional` | `` |  |
| 3 | `min_raw_value` | `uint32` | `optional` | `` |  |
| 4 | `max_raw_value` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgInGamePrediction</code> — fields: 14; oneofs: 0; nested messages: 1; nested enums: 4</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `id` | `uint32` | `optional` | `` |  |
| 2 | `name` | `string` | `optional` | `` |  |
| 3 | `type` | `.CMsgInGamePrediction.EPredictionType` | `optional` | `` | default = Generic |
| 4 | `group` | `.CMsgInGamePrediction.ERandomSelectionGroup_t` | `optional` | `` | default = EarlyGame |
| 5 | `question` | `string` | `optional` | `` |  |
| 6 | `choices` | `.CMsgPredictionChoice` | `repeated` | `` |  |
| 7 | `required_heroes` | `string` | `repeated` | `` |  |
| 8 | `query_name` | `string` | `optional` | `` |  |
| 9 | `query_values` | `.CMsgInGamePrediction.QueryKeyValues` | `repeated` | `` |  |
| 10 | `answer_resolution_type` | `.CMsgInGamePrediction.EResolutionType_t` | `optional` | `` | default = InvalidQuery |
| 11 | `points_to_grant` | `uint32` | `optional` | `` |  |
| 12 | `reward_action` | `uint32` | `optional` | `` |  |
| 13 | `debug_force_selection` | `uint32` | `optional` | `` |  |
| 14 | `raw_value_type` | `.CMsgInGamePrediction.ERawValueType_t` | `optional` | `` | default = Number |

</details>

<details>
<summary><code>CMsgInGamePrediction.QueryKeyValues</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgInGamePrediction`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `value` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTASeasonPredictions</code> — fields: 4; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `predictions` | `.CMsgDOTASeasonPredictions.Prediction` | `repeated` | `` |  |
| 2 | `in_game_predictions` | `.CMsgInGamePrediction` | `repeated` | `` |  |
| 3 | `in_game_prediction_count_per_game` | `uint32` | `optional` | `` |  |
| 4 | `in_game_prediction_voting_period_minutes` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTASeasonPredictions.Prediction</code> — fields: 20; oneofs: 0; nested messages: 1; nested enums: 2</summary>

- Parent: `CMsgDOTASeasonPredictions`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `type` | `.CMsgDOTASeasonPredictions.Prediction.EPredictionType` | `optional` | `` | default = Generic |
| 2 | `question` | `string` | `optional` | `` |  |
| 3 | `choices` | `.CMsgPredictionChoice` | `repeated` | `` |  |
| 4 | `selection_id` | `uint32` | `optional` | `` |  |
| 5 | `start_date` | `uint32` | `optional` | `` |  |
| 6 | `lock_date` | `uint32` | `optional` | `` |  |
| 7 | `reward` | `uint32` | `optional` | `` |  |
| 8 | `answer_type` | `.CMsgDOTASeasonPredictions.Prediction.EAnswerType` | `optional` | `` | default = SingleInt |
| 9 | `answer_id` | `uint32` | `optional` | `` |  |
| 10 | `answers` | `.CMsgDOTASeasonPredictions.Prediction.Answers` | `repeated` | `` |  |
| 11 | `query_name` | `string` | `optional` | `` |  |
| 13 | `lock_on_selection_id` | `uint32` | `optional` | `` |  |
| 14 | `lock_on_selection_value` | `uint32` | `optional` | `` |  |
| 15 | `lock_on_selection_set` | `bool` | `optional` | `` |  |
| 16 | `use_answer_value_ranges` | `bool` | `optional` | `` |  |
| 17 | `region` | `.ELeagueRegion` | `optional` | `` | default = LEAGUE_REGION_UNSET |
| 18 | `phases` | `.ELeaguePhase` | `repeated` | `` |  |
| 19 | `reward_event` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 20 | `league_node_id` | `uint32` | `optional` | `` |  |
| 21 | `reward_event_action` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTASeasonPredictions.Prediction.Answers</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTASeasonPredictions.Prediction`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `answer_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgAvailablePredictions</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_predictions` | `.CMsgAvailablePredictions.MatchPrediction` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgAvailablePredictions.MatchPrediction</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgAvailablePredictions`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `predictions` | `.CMsgInGamePrediction` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgLeagueWatchedGames</code> — fields: 1; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `leagues` | `.CMsgLeagueWatchedGames.League` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgLeagueWatchedGames.Series</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgLeagueWatchedGames`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `node_id` | `uint32` | `optional` | `` |  |
| 2 | `game` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgLeagueWatchedGames.League</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgLeagueWatchedGames`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_id` | `uint32` | `optional` | `` |  |
| 2 | `series` | `.CMsgLeagueWatchedGames.Series` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAMatch</code> — fields: 48; oneofs: 0; nested messages: 5; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 3 | `duration` | `uint32` | `optional` | `` |  |
| 4 | `starttime` | `fixed32` | `optional` | `` |  |
| 5 | `players` | `.CMsgDOTAMatch.Player` | `repeated` | `` |  |
| 6 | `match_id` | `uint64` | `optional` | `` |  |
| 8 | `tower_status` | `uint32` | `repeated` | `` |  |
| 9 | `barracks_status` | `uint32` | `repeated` | `` |  |
| 10 | `cluster` | `uint32` | `optional` | `` |  |
| 12 | `first_blood_time` | `uint32` | `optional` | `` |  |
| 13 | `replay_salt` | `fixed32` | `optional` | `` |  |
| 14 | `server_ip` | `fixed32` | `optional` | `` |  |
| 15 | `server_port` | `uint32` | `optional` | `` |  |
| 16 | `lobby_type` | `uint32` | `optional` | `` |  |
| 17 | `human_players` | `uint32` | `optional` | `` |  |
| 18 | `average_skill` | `uint32` | `optional` | `` |  |
| 19 | `game_balance` | `float` | `optional` | `` |  |
| 20 | `radiant_team_id` | `uint32` | `optional` | `` |  |
| 21 | `dire_team_id` | `uint32` | `optional` | `` |  |
| 22 | `leagueid` | `uint32` | `optional` | `` |  |
| 23 | `radiant_team_name` | `string` | `optional` | `` |  |
| 24 | `dire_team_name` | `string` | `optional` | `` |  |
| 25 | `radiant_team_logo` | `uint64` | `optional` | `` |  |
| 26 | `dire_team_logo` | `uint64` | `optional` | `` |  |
| 27 | `radiant_team_complete` | `uint32` | `optional` | `` |  |
| 28 | `dire_team_complete` | `uint32` | `optional` | `` |  |
| 31 | `game_mode` | `.DOTA_GameMode` | `optional` | `` | default = DOTA_GAMEMODE_NONE |
| 32 | `picks_bans` | `.CMatchHeroSelectEvent` | `repeated` | `` |  |
| 33 | `match_seq_num` | `uint64` | `optional` | `` |  |
| 34 | `replay_state` | `.CMsgDOTAMatch.ReplayState` | `optional` | `` | default = REPLAY_AVAILABLE |
| 35 | `radiant_guild_id` | `uint32` | `optional` | `` |  |
| 36 | `dire_guild_id` | `uint32` | `optional` | `` |  |
| 37 | `radiant_team_tag` | `string` | `optional` | `` |  |
| 38 | `dire_team_tag` | `string` | `optional` | `` |  |
| 39 | `series_id` | `uint32` | `optional` | `` |  |
| 40 | `series_type` | `uint32` | `optional` | `` |  |
| 43 | `broadcaster_channels` | `.CMsgDOTAMatch.BroadcasterChannel` | `repeated` | `` |  |
| 44 | `engine` | `uint32` | `optional` | `` |  |
| 45 | `custom_game_data` | `.CMsgDOTAMatch.CustomGameData` | `optional` | `` |  |
| 46 | `match_flags` | `uint32` | `optional` | `` |  |
| 47 | `private_metadata_key` | `fixed32` | `optional` | `` |  |
| 48 | `radiant_team_score` | `uint32` | `optional` | `` |  |
| 49 | `dire_team_score` | `uint32` | `optional` | `` |  |
| 50 | `match_outcome` | `.EMatchOutcome` | `optional` | `` | default = k_EMatchOutcome_Unknown |
| 51 | `tournament_id` | `uint32` | `optional` | `` |  |
| 52 | `tournament_round` | `uint32` | `optional` | `` |  |
| 53 | `pre_game_duration` | `uint32` | `optional` | `` |  |
| 54 | `radiant_team_logo_url` | `string` | `optional` | `` |  |
| 55 | `dire_team_logo_url` | `string` | `optional` | `` |  |
| 57 | `coaches` | `.CMsgDOTAMatch.Coach` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAMatch.Player</code> — fields: 77; oneofs: 0; nested messages: 2; nested enums: 1</summary>

- Parent: `CMsgDOTAMatch`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `player_slot` | `uint32` | `optional` | `` |  |
| 3 | `hero_id` | `int32` | `optional` | `` |  |
| 4 | `item_0` | `int32` | `optional` | `` | default = -1 |
| 5 | `item_1` | `int32` | `optional` | `` | default = -1 |
| 6 | `item_2` | `int32` | `optional` | `` | default = -1 |
| 7 | `item_3` | `int32` | `optional` | `` | default = -1 |
| 8 | `item_4` | `int32` | `optional` | `` | default = -1 |
| 9 | `item_5` | `int32` | `optional` | `` | default = -1 |
| 10 | `expected_team_contribution` | `float` | `optional` | `` |  |
| 11 | `scaled_metric` | `float` | `optional` | `` |  |
| 12 | `previous_rank` | `uint32` | `optional` | `` |  |
| 13 | `rank_change` | `sint32` | `optional` | `` |  |
| 14 | `kills` | `uint32` | `optional` | `` |  |
| 15 | `deaths` | `uint32` | `optional` | `` |  |
| 16 | `assists` | `uint32` | `optional` | `` |  |
| 17 | `leaver_status` | `uint32` | `optional` | `` |  |
| 18 | `gold` | `uint32` | `optional` | `` |  |
| 19 | `last_hits` | `uint32` | `optional` | `` |  |
| 20 | `denies` | `uint32` | `optional` | `` |  |
| 21 | `gold_per_min` | `uint32` | `optional` | `` |  |
| 22 | `xp_per_min` | `uint32` | `optional` | `` |  |
| 23 | `gold_spent` | `uint32` | `optional` | `` |  |
| 24 | `hero_damage` | `uint32` | `optional` | `` |  |
| 25 | `tower_damage` | `uint32` | `optional` | `` |  |
| 26 | `hero_healing` | `uint32` | `optional` | `` |  |
| 27 | `level` | `uint32` | `optional` | `` |  |
| 28 | `time_last_seen` | `uint32` | `optional` | `` |  |
| 29 | `player_name` | `string` | `optional` | `` |  |
| 30 | `support_ability_value` | `uint32` | `optional` | `` |  |
| 32 | `feeding_detected` | `bool` | `optional` | `` |  |
| 34 | `search_rank` | `uint32` | `optional` | `` |  |
| 35 | `search_rank_uncertainty` | `uint32` | `optional` | `` |  |
| 36 | `rank_uncertainty_change` | `int32` | `optional` | `` |  |
| 37 | `hero_play_count` | `uint32` | `optional` | `` |  |
| 38 | `party_id` | `fixed64` | `optional` | `` |  |
| 39 | `scaled_kills` | `float` | `optional` | `` |  |
| 40 | `scaled_deaths` | `float` | `optional` | `` |  |
| 41 | `scaled_assists` | `float` | `optional` | `` |  |
| 42 | `claimed_farm_gold` | `uint32` | `optional` | `` |  |
| 43 | `support_gold` | `uint32` | `optional` | `` |  |
| 44 | `claimed_denies` | `uint32` | `optional` | `` |  |
| 45 | `claimed_misses` | `uint32` | `optional` | `` |  |
| 46 | `misses` | `uint32` | `optional` | `` |  |
| 47 | `ability_upgrades` | `.CMatchPlayerAbilityUpgrade` | `repeated` | `` |  |
| 48 | `additional_units_inventory` | `.CMatchAdditionalUnitInventory` | `repeated` | `` |  |
| 50 | `custom_game_data` | `.CMsgDOTAMatch.Player.CustomGameData` | `optional` | `` |  |
| 51 | `active_plus_subscription` | `bool` | `optional` | `` |  |
| 52 | `net_worth` | `uint32` | `optional` | `` |  |
| 54 | `scaled_hero_damage` | `uint32` | `optional` | `` |  |
| 55 | `scaled_tower_damage` | `uint32` | `optional` | `` |  |
| 56 | `scaled_hero_healing` | `uint32` | `optional` | `` |  |
| 57 | `permanent_buffs` | `.CMatchPlayerPermanentBuff` | `repeated` | `` |  |
| 58 | `bot_difficulty` | `uint32` | `optional` | `` |  |
| 59 | `item_6` | `int32` | `optional` | `` | default = -1 |
| 60 | `item_7` | `int32` | `optional` | `` | default = -1 |
| 61 | `item_8` | `int32` | `optional` | `` | default = -1 |
| 63 | `hero_pick_order` | `uint32` | `optional` | `` |  |
| 64 | `hero_was_randomed` | `bool` | `optional` | `` |  |
| 67 | `hero_damage_received` | `.CMsgDOTAMatch.Player.HeroDamageReceived` | `repeated` | `` |  |
| 69 | `hero_was_dota_plus_suggestion` | `bool` | `optional` | `` |  |
| 70 | `seconds_dead` | `uint32` | `optional` | `` |  |
| 71 | `gold_lost_to_death` | `uint32` | `optional` | `` |  |
| 72 | `pro_name` | `string` | `optional` | `` |  |
| 73 | `real_name` | `string` | `optional` | `` |  |
| 74 | `mmr_type` | `uint32` | `optional` | `` |  |
| 75 | `lane_selection_flags` | `uint32` | `optional` | `` |  |
| 76 | `item_9` | `int32` | `optional` | `` | default = -1 |
| 77 | `bounty_runes` | `uint32` | `optional` | `` |  |
| 78 | `outposts_captured` | `uint32` | `optional` | `` |  |
| 79 | `hero_damage_dealt` | `.CMsgDOTAMatch.Player.HeroDamageReceived` | `repeated` | `` |  |
| 80 | `team_number` | `.DOTA_GC_TEAM` | `optional` | `` | default = DOTA_GC_TEAM_GOOD_GUYS |
| 81 | `team_slot` | `uint32` | `optional` | `` |  |
| 82 | `selected_facet` | `uint32` | `optional` | `` |  |
| 83 | `item_10` | `int32` | `optional` | `` | default = -1 |
| 84 | `item_10_lvl` | `int32` | `optional` | `` |  |
| 85 | `disable_duration` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAMatch.Player.CustomGameData</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAMatch.Player`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `dota_team` | `uint32` | `optional` | `` |  |
| 2 | `winner` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAMatch.Player.HeroDamageReceived</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAMatch.Player`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `pre_reduction` | `uint32` | `optional` | `` |  |
| 2 | `post_reduction` | `uint32` | `optional` | `` |  |
| 3 | `damage_type` | `.CMsgDOTAMatch.Player.HeroDamageType` | `optional` | `` | default = HERO_DAMAGE_PHYSICAL |

</details>

<details>
<summary><code>CMsgDOTAMatch.BroadcasterInfo</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAMatch`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAMatch.BroadcasterChannel</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAMatch`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `country_code` | `string` | `optional` | `` |  |
| 2 | `description` | `string` | `optional` | `` |  |
| 3 | `broadcaster_infos` | `.CMsgDOTAMatch.BroadcasterInfo` | `repeated` | `` |  |
| 4 | `language_code` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAMatch.Coach</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAMatch`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `coach_name` | `string` | `optional` | `` |  |
| 3 | `coach_rating` | `uint32` | `optional` | `` |  |
| 4 | `coach_team` | `uint32` | `optional` | `` |  |
| 5 | `coach_party_id` | `uint64` | `optional` | `` |  |
| 6 | `is_private_coach` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAMatch.CustomGameData</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAMatch`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `custom_game_id` | `uint64` | `optional` | `` |  |
| 2 | `map_name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPlayerCard</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `stat_modifier` | `.CMsgPlayerCard.StatModifier` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgPlayerCard.StatModifier</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgPlayerCard`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `stat` | `uint32` | `optional` | `` |  |
| 2 | `value` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAFantasyPlayerStats</code> — fields: 27; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_account_id` | `uint32` | `optional` | `` |  |
| 2 | `match_id` | `uint64` | `optional` | `` |  |
| 3 | `match_completed` | `bool` | `optional` | `` |  |
| 4 | `team_id` | `uint32` | `optional` | `` |  |
| 5 | `league_id` | `uint32` | `optional` | `` |  |
| 6 | `delay` | `uint32` | `optional` | `` |  |
| 7 | `series_id` | `uint32` | `optional` | `` |  |
| 8 | `series_type` | `uint32` | `optional` | `` |  |
| 10 | `kills` | `uint32` | `optional` | `` |  |
| 11 | `deaths` | `uint32` | `optional` | `` |  |
| 12 | `cs` | `uint32` | `optional` | `` |  |
| 13 | `gpm` | `float` | `optional` | `` |  |
| 14 | `tower_kills` | `uint32` | `optional` | `` |  |
| 15 | `roshan_kills` | `uint32` | `optional` | `` |  |
| 16 | `teamfight_participation` | `float` | `optional` | `` |  |
| 17 | `wards_placed` | `uint32` | `optional` | `` |  |
| 18 | `camps_stacked` | `uint32` | `optional` | `` |  |
| 19 | `runes_grabbed` | `uint32` | `optional` | `` |  |
| 20 | `first_blood` | `uint32` | `optional` | `` |  |
| 21 | `stuns` | `float` | `optional` | `` |  |
| 22 | `smokes` | `uint32` | `optional` | `` |  |
| 24 | `watchers` | `uint32` | `optional` | `` |  |
| 25 | `lotuses` | `uint32` | `optional` | `` |  |
| 26 | `tormentors` | `uint32` | `optional` | `` |  |
| 27 | `courier_kills` | `uint32` | `optional` | `` |  |
| 28 | `title_stats` | `fixed64` | `optional` | `` |  |
| 29 | `madstone` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAFantasyPlayerMatchStats</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `matches` | `.CMsgDOTAFantasyPlayerStats` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTABotDebugInfo</code> — fields: 13; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `bots` | `.CMsgDOTABotDebugInfo.Bot` | `repeated` | `` |  |
| 2 | `desire_push_lane_top` | `float` | `optional` | `` |  |
| 3 | `desire_push_lane_mid` | `float` | `optional` | `` |  |
| 4 | `desire_push_lane_bot` | `float` | `optional` | `` |  |
| 5 | `desire_defend_lane_top` | `float` | `optional` | `` |  |
| 6 | `desire_defend_lane_mid` | `float` | `optional` | `` |  |
| 7 | `desire_defend_lane_bot` | `float` | `optional` | `` |  |
| 8 | `desire_farm_lane_top` | `float` | `optional` | `` |  |
| 9 | `desire_farm_lane_mid` | `float` | `optional` | `` |  |
| 10 | `desire_farm_lane_bot` | `float` | `optional` | `` |  |
| 11 | `desire_farm_roshan` | `float` | `optional` | `` |  |
| 12 | `execution_time` | `float` | `optional` | `` |  |
| 13 | `rune_status` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTABotDebugInfo.Bot</code> — fields: 12; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: `CMsgDOTABotDebugInfo`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_owner_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `hero_id` | `int32` | `optional` | `` |  |
| 3 | `difficulty` | `uint32` | `optional` | `` |  |
| 4 | `power_current` | `uint32` | `optional` | `` |  |
| 5 | `power_max` | `uint32` | `optional` | `` |  |
| 6 | `move_target_x` | `uint32` | `optional` | `` |  |
| 7 | `move_target_y` | `uint32` | `optional` | `` |  |
| 8 | `move_target_z` | `uint32` | `optional` | `` |  |
| 9 | `active_mode_id` | `uint32` | `optional` | `` |  |
| 10 | `execution_time` | `float` | `optional` | `` |  |
| 11 | `modes` | `.CMsgDOTABotDebugInfo.Bot.Mode` | `repeated` | `` |  |
| 12 | `action` | `.CMsgDOTABotDebugInfo.Bot.Action` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTABotDebugInfo.Bot.Mode</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTABotDebugInfo.Bot`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `mode_id` | `uint32` | `optional` | `` |  |
| 2 | `desire` | `float` | `optional` | `` |  |
| 3 | `target_entity` | `int32` | `optional` | `` | default = -1 |
| 4 | `target_x` | `uint32` | `optional` | `` |  |
| 5 | `target_y` | `uint32` | `optional` | `` |  |
| 6 | `target_z` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTABotDebugInfo.Bot.Action</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTABotDebugInfo.Bot`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `action_id` | `uint32` | `optional` | `` |  |
| 2 | `action_target` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSuccessfulHero</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `win_percent` | `float` | `optional` | `` |  |
| 3 | `longest_streak` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgRecentMatchInfo</code> — fields: 11; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `game_mode` | `.DOTA_GameMode` | `optional` | `` | default = DOTA_GAMEMODE_NONE |
| 3 | `kills` | `uint32` | `optional` | `` |  |
| 4 | `deaths` | `uint32` | `optional` | `` |  |
| 5 | `assists` | `uint32` | `optional` | `` |  |
| 6 | `duration` | `uint32` | `optional` | `` |  |
| 7 | `player_slot` | `uint32` | `optional` | `` |  |
| 8 | `match_outcome` | `.EMatchOutcome` | `optional` | `` | default = k_EMatchOutcome_Unknown |
| 9 | `timestamp` | `uint32` | `optional` | `` |  |
| 10 | `lobby_type` | `uint32` | `optional` | `` |  |
| 11 | `team_number` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgMatchTips</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `tips` | `.CMsgMatchTips.SingleTip` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgMatchTips.SingleTip</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgMatchTips`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `source_account_id` | `uint32` | `optional` | `` |  |
| 2 | `target_account_id` | `uint32` | `optional` | `` |  |
| 3 | `tip_amount` | `uint32` | `optional` | `` |  |
| 4 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |

</details>

<details>
<summary><code>CMsgDOTAMatchMinimal</code> — fields: 11; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `start_time` | `fixed32` | `optional` | `` |  |
| 3 | `duration` | `uint32` | `optional` | `` |  |
| 4 | `game_mode` | `.DOTA_GameMode` | `optional` | `` | default = DOTA_GAMEMODE_NONE |
| 6 | `players` | `.CMsgDOTAMatchMinimal.Player` | `repeated` | `` |  |
| 7 | `tourney` | `.CMsgDOTAMatchMinimal.Tourney` | `optional` | `` |  |
| 8 | `match_outcome` | `.EMatchOutcome` | `optional` | `` | default = k_EMatchOutcome_Unknown |
| 9 | `radiant_score` | `uint32` | `optional` | `` |  |
| 10 | `dire_score` | `uint32` | `optional` | `` |  |
| 11 | `lobby_type` | `uint32` | `optional` | `` |  |
| 12 | `is_player_draft` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAMatchMinimal.Player</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAMatchMinimal`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `hero_id` | `int32` | `optional` | `` |  |
| 3 | `kills` | `uint32` | `optional` | `` |  |
| 4 | `deaths` | `uint32` | `optional` | `` |  |
| 5 | `assists` | `uint32` | `optional` | `` |  |
| 6 | `items` | `int32` | `repeated` | `` |  |
| 7 | `player_slot` | `uint32` | `optional` | `` |  |
| 8 | `pro_name` | `string` | `optional` | `` |  |
| 9 | `level` | `uint32` | `optional` | `` |  |
| 10 | `team_number` | `.DOTA_GC_TEAM` | `optional` | `` | default = DOTA_GC_TEAM_GOOD_GUYS |

</details>

<details>
<summary><code>CMsgDOTAMatchMinimal.Tourney</code> — fields: 15; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAMatchMinimal`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_id` | `uint32` | `optional` | `` |  |
| 2 | `radiant_team_id` | `uint32` | `optional` | `` |  |
| 3 | `radiant_team_name` | `string` | `optional` | `` |  |
| 4 | `radiant_team_logo` | `fixed64` | `optional` | `` |  |
| 5 | `dire_team_id` | `uint32` | `optional` | `` |  |
| 6 | `dire_team_name` | `string` | `optional` | `` |  |
| 7 | `dire_team_logo` | `fixed64` | `optional` | `` |  |
| 8 | `series_type` | `uint32` | `optional` | `` |  |
| 9 | `series_game` | `uint32` | `optional` | `` |  |
| 10 | `weekend_tourney_tournament_id` | `uint32` | `optional` | `` |  |
| 11 | `weekend_tourney_season_trophy_id` | `uint32` | `optional` | `` |  |
| 12 | `weekend_tourney_division` | `uint32` | `optional` | `` |  |
| 13 | `weekend_tourney_skill_level` | `uint32` | `optional` | `` |  |
| 14 | `radiant_team_logo_url` | `string` | `optional` | `` |  |
| 15 | `dire_team_logo_url` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgConsumableUsage</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_def` | `uint32` | `optional` | `` |  |
| 2 | `quantity_change` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgMatchConsumableUsage</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_consumables_used` | `.CMsgMatchConsumableUsage.PlayerUsage` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgMatchConsumableUsage.PlayerUsage</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgMatchConsumableUsage`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `consumables_used` | `.CMsgConsumableUsage` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgMatchEventActionGrants</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_grants` | `.CMsgMatchEventActionGrants.PlayerGrants` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgMatchEventActionGrants.PlayerGrants</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgMatchEventActionGrants`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 3 | `actions_granted` | `.CMsgPendingEventAward` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgCustomGameWhitelist</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `version` | `uint32` | `optional` | `` |  |
| 2 | `custom_games_whitelist` | `uint64` | `repeated` | `` |  |
| 3 | `disable_whitelist` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgCustomGameWhitelistForEdit</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `whitelist_entries` | `.CMsgCustomGameWhitelistForEdit.WhitelistEntry` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgCustomGameWhitelistForEdit.WhitelistEntry</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgCustomGameWhitelistForEdit`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `custom_game_id` | `uint64` | `optional` | `` |  |
| 2 | `whitelist_state` | `.ECustomGameWhitelistState` | `optional` | `` | default = CUSTOM_GAME_WHITELIST_STATE_UNKNOWN |

</details>

<details>
<summary><code>CMsgPlayerRecentMatchInfo</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `timestamp` | `uint32` | `optional` | `` |  |
| 3 | `duration` | `uint32` | `optional` | `` |  |
| 4 | `win` | `bool` | `optional` | `` |  |
| 5 | `hero_id` | `int32` | `optional` | `` |  |
| 6 | `kills` | `uint32` | `optional` | `` |  |
| 7 | `deaths` | `uint32` | `optional` | `` |  |
| 8 | `assists` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPlayerMatchRecord</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `wins` | `uint32` | `optional` | `` |  |
| 2 | `losses` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPlayerRecentMatchOutcomes</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `outcomes` | `uint32` | `optional` | `` |  |
| 2 | `match_count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPlayerRecentCommends</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `commends` | `uint32` | `optional` | `` |  |
| 2 | `match_count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPlayerRecentAccomplishments</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `recent_outcomes` | `.CMsgPlayerRecentMatchOutcomes` | `optional` | `` |  |
| 2 | `total_record` | `.CMsgPlayerMatchRecord` | `optional` | `` |  |
| 3 | `prediction_streak` | `uint32` | `optional` | `` |  |
| 4 | `plus_prediction_streak` | `uint32` | `optional` | `` |  |
| 5 | `recent_commends` | `.CMsgPlayerRecentCommends` | `optional` | `` |  |
| 6 | `first_match_timestamp` | `uint32` | `optional` | `` |  |
| 7 | `last_match` | `.CMsgPlayerRecentMatchInfo` | `optional` | `` |  |
| 8 | `recent_mvps` | `.CMsgPlayerRecentMatchOutcomes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPlayerHeroRecentAccomplishments</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `recent_outcomes` | `.CMsgPlayerRecentMatchOutcomes` | `optional` | `` |  |
| 2 | `total_record` | `.CMsgPlayerMatchRecord` | `optional` | `` |  |
| 3 | `last_match` | `.CMsgPlayerRecentMatchInfo` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgRecentAccomplishments</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_accomplishments` | `.CMsgPlayerRecentAccomplishments` | `optional` | `` |  |
| 2 | `hero_accomplishments` | `.CMsgPlayerHeroRecentAccomplishments` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCRequestPlayerRecentAccomplishments</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `hero_id` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCRequestPlayerRecentAccomplishmentsResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgServerToGCRequestPlayerRecentAccomplishmentsResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `player_accomplishments` | `.CMsgRecentAccomplishments` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgArcanaVoteMatchVotes</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint32` | `optional` | `` |  |
| 2 | `hero_id` | `int32` | `optional` | `` |  |
| 3 | `vote_count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCtoGCAssociatedExploiterAccountInfo</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `num_matches_to_search` | `uint32` | `optional` | `` |  |
| 3 | `min_shared_match_count` | `uint32` | `optional` | `` |  |
| 4 | `num_additional_players` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCtoGCAssociatedExploiterAccountInfoResponse</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `accounts` | `.CMsgGCtoGCAssociatedExploiterAccountInfoResponse.Account` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCtoGCAssociatedExploiterAccountInfoResponse.Account</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCtoGCAssociatedExploiterAccountInfoResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `num_common_matches` | `uint32` | `optional` | `` |  |
| 3 | `earliest_common_match` | `uint32` | `optional` | `` |  |
| 4 | `latest_common_match` | `uint32` | `optional` | `` |  |
| 5 | `generation` | `uint32` | `optional` | `` |  |
| 6 | `persona` | `string` | `optional` | `` |  |
| 7 | `already_banned` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPullTabsData</code> — fields: 3; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `slots` | `.CMsgPullTabsData.Slot` | `repeated` | `` |  |
| 2 | `jackpots` | `.CMsgPullTabsData.Jackpot` | `repeated` | `` |  |
| 3 | `last_board` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPullTabsData.Slot</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgPullTabsData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |
| 2 | `board_id` | `uint32` | `optional` | `` |  |
| 3 | `hero_id` | `int32` | `optional` | `` |  |
| 4 | `action_id` | `uint32` | `optional` | `` |  |
| 5 | `redeemed` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPullTabsData.Jackpot</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgPullTabsData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `board_id` | `uint32` | `optional` | `` |  |
| 2 | `action_id` | `uint32` | `optional` | `` |  |
| 3 | `hero_id` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgUnderDraftData</code> — fields: 5; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `bench_slots` | `.CMsgUnderDraftData.BenchSlot` | `repeated` | `` |  |
| 2 | `shop_slots` | `.CMsgUnderDraftData.ShopSlot` | `repeated` | `` |  |
| 3 | `gold` | `uint32` | `optional` | `` |  |
| 4 | `total_gold` | `uint32` | `optional` | `` |  |
| 5 | `not_restorable` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgUnderDraftData.BenchSlot</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgUnderDraftData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `slot_id` | `uint32` | `optional` | `` |  |
| 2 | `hero_id` | `int32` | `optional` | `` |  |
| 3 | `stars` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgUnderDraftData.ShopSlot</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgUnderDraftData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `slot_id` | `uint32` | `optional` | `` |  |
| 2 | `hero_id` | `int32` | `optional` | `` |  |
| 3 | `is_special_reward` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPlayerTitleData</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `title` | `uint32` | `repeated` | `` |  |
| 2 | `event_id` | `uint32` | `repeated` | `` |  |
| 3 | `active` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTATriviaQuestion</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `question_id` | `uint32` | `optional` | `` |  |
| 2 | `category` | `.EDOTATriviaQuestionCategory` | `optional` | `` | default = k_EDOTATriviaQuestionCategory_AbilityIcon |
| 3 | `timestamp` | `uint32` | `optional` | `` |  |
| 4 | `question_value` | `string` | `optional` | `` |  |
| 5 | `answer_values` | `string` | `repeated` | `` |  |
| 6 | `correct_answer_index` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTATriviaQuestionAnswersSummary</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `summary_available` | `bool` | `optional` | `` |  |
| 2 | `picked_count` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGameDataSpecialValueBonus</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `value` | `float` | `optional` | `` |  |
| 3 | `operation` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGameDataSpecialValues</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `values_float` | `float` | `repeated` | `` |  |
| 4 | `is_percentage` | `bool` | `optional` | `` |  |
| 5 | `heading_loc` | `string` | `optional` | `` |  |
| 6 | `bonuses` | `.CMsgGameDataSpecialValueBonus` | `repeated` | `` |  |
| 7 | `values_shard` | `float` | `repeated` | `` |  |
| 8 | `values_scepter` | `float` | `repeated` | `` |  |
| 9 | `facet_bonus` | `.CMsgGameDataFacetAbilityBonus` | `optional` | `` |  |
| 10 | `required_facet` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGameDataFacetAbilityBonus</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `values` | `float` | `repeated` | `` |  |
| 3 | `operation` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGameDataAbilityOrItem</code> — fields: 40; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `id` | `int32` | `optional` | `` | default = -1 |
| 2 | `name` | `string` | `optional` | `` |  |
| 5 | `name_loc` | `string` | `optional` | `` |  |
| 6 | `desc_loc` | `string` | `optional` | `` |  |
| 7 | `lore_loc` | `string` | `optional` | `` |  |
| 8 | `notes_loc` | `string` | `repeated` | `` |  |
| 9 | `shard_loc` | `string` | `optional` | `` |  |
| 10 | `scepter_loc` | `string` | `optional` | `` |  |
| 11 | `facets_loc` | `string` | `repeated` | `` |  |
| 20 | `type` | `uint32` | `optional` | `` |  |
| 21 | `behavior` | `uint64` | `optional` | `` |  |
| 22 | `target_team` | `uint32` | `optional` | `` |  |
| 23 | `target_type` | `uint32` | `optional` | `` |  |
| 24 | `flags` | `uint32` | `optional` | `` |  |
| 25 | `damage` | `uint32` | `optional` | `` |  |
| 26 | `immunity` | `uint32` | `optional` | `` |  |
| 27 | `dispellable` | `uint32` | `optional` | `` |  |
| 28 | `max_level` | `uint32` | `optional` | `` |  |
| 30 | `cast_ranges` | `uint32` | `repeated` | `` |  |
| 31 | `cast_points` | `float` | `repeated` | `` |  |
| 32 | `channel_times` | `float` | `repeated` | `` |  |
| 33 | `cooldowns` | `float` | `repeated` | `` |  |
| 34 | `durations` | `float` | `repeated` | `` |  |
| 35 | `damages` | `uint32` | `repeated` | `` |  |
| 36 | `mana_costs` | `uint32` | `repeated` | `` |  |
| 37 | `gold_costs` | `uint32` | `repeated` | `` |  |
| 38 | `health_costs` | `uint32` | `repeated` | `` |  |
| 40 | `special_values` | `.CMsgGameDataSpecialValues` | `repeated` | `` |  |
| 50 | `is_item` | `bool` | `optional` | `` |  |
| 60 | `ability_has_scepter` | `bool` | `optional` | `` |  |
| 61 | `ability_has_shard` | `bool` | `optional` | `` |  |
| 62 | `ability_is_granted_by_scepter` | `bool` | `optional` | `` |  |
| 63 | `ability_is_granted_by_shard` | `bool` | `optional` | `` |  |
| 64 | `ability_is_innate` | `bool` | `optional` | `` |  |
| 70 | `item_cost` | `uint32` | `optional` | `` |  |
| 71 | `item_initial_charges` | `uint32` | `optional` | `` |  |
| 72 | `item_neutral_tier` | `uint32` | `optional` | `` |  |
| 73 | `item_stock_max` | `uint32` | `optional` | `` |  |
| 74 | `item_stock_time` | `float` | `optional` | `` |  |
| 85 | `item_quality` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGameDataAbilityOrItemList</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `abilities` | `.CMsgGameDataAbilityOrItem` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGameDataHero</code> — fields: 36; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `id` | `int32` | `optional` | `` |  |
| 2 | `name` | `string` | `optional` | `` |  |
| 3 | `order_id` | `uint32` | `optional` | `` |  |
| 5 | `name_loc` | `string` | `optional` | `` |  |
| 6 | `bio_loc` | `string` | `optional` | `` |  |
| 7 | `hype_loc` | `string` | `optional` | `` |  |
| 8 | `npe_desc_loc` | `string` | `optional` | `` |  |
| 10 | `str_base` | `uint32` | `optional` | `` |  |
| 11 | `str_gain` | `float` | `optional` | `` |  |
| 12 | `agi_base` | `uint32` | `optional` | `` |  |
| 13 | `agi_gain` | `float` | `optional` | `` |  |
| 14 | `int_base` | `uint32` | `optional` | `` |  |
| 15 | `int_gain` | `float` | `optional` | `` |  |
| 20 | `primary_attr` | `uint32` | `optional` | `` |  |
| 21 | `complexity` | `uint32` | `optional` | `` |  |
| 22 | `attack_capability` | `uint32` | `optional` | `` |  |
| 23 | `role_levels` | `uint32` | `repeated` | `` |  |
| 24 | `damage_min` | `int32` | `optional` | `` |  |
| 25 | `damage_max` | `int32` | `optional` | `` |  |
| 26 | `attack_rate` | `float` | `optional` | `` |  |
| 27 | `attack_range` | `uint32` | `optional` | `` |  |
| 28 | `projectile_speed` | `uint32` | `optional` | `` |  |
| 29 | `armor` | `float` | `optional` | `` |  |
| 30 | `magic_resistance` | `uint32` | `optional` | `` |  |
| 31 | `movement_speed` | `uint32` | `optional` | `` |  |
| 32 | `turn_rate` | `float` | `optional` | `` |  |
| 33 | `sight_range_day` | `uint32` | `optional` | `` |  |
| 34 | `sight_range_night` | `uint32` | `optional` | `` |  |
| 35 | `max_health` | `uint32` | `optional` | `` |  |
| 36 | `health_regen` | `float` | `optional` | `` |  |
| 37 | `max_mana` | `uint32` | `optional` | `` |  |
| 38 | `mana_regen` | `float` | `optional` | `` |  |
| 40 | `abilities` | `.CMsgGameDataAbilityOrItem` | `repeated` | `` |  |
| 41 | `talents` | `.CMsgGameDataAbilityOrItem` | `repeated` | `` |  |
| 42 | `facet_abilities` | `.CMsgGameDataAbilityOrItemList` | `repeated` | `` |  |
| 43 | `facets` | `.CMsgGameDataHero.Facet` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGameDataHero.Facet</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGameDataHero`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `color` | `uint32` | `optional` | `` |  |
| 2 | `title_loc` | `string` | `optional` | `` |  |
| 3 | `description_loc` | `string` | `optional` | `` |  |
| 4 | `name` | `string` | `optional` | `` |  |
| 5 | `icon` | `string` | `optional` | `` |  |
| 6 | `gradient_id` | `int32` | `optional` | `` |  |
| 7 | `index` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGameDataAbilities</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `abilities` | `.CMsgGameDataAbilityOrItem` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGameDataItems</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `items` | `.CMsgGameDataAbilityOrItem` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGameDataHeroes</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `heroes` | `.CMsgGameDataHero` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGameDataHeroList</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `heroes` | `.CMsgGameDataHeroList.HeroInfo` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGameDataHeroList.HeroInfo</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGameDataHeroList`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `id` | `int32` | `optional` | `` |  |
| 2 | `name` | `string` | `optional` | `` |  |
| 3 | `name_loc` | `string` | `optional` | `` |  |
| 4 | `name_english_loc` | `string` | `optional` | `` |  |
| 5 | `primary_attr` | `uint32` | `optional` | `` |  |
| 6 | `complexity` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGameDataItemAbilityList</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `itemabilities` | `.CMsgGameDataItemAbilityList.ItemAbilityInfo` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGameDataItemAbilityList.ItemAbilityInfo</code> — fields: 9; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: `CMsgGameDataItemAbilityList`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `id` | `int32` | `optional` | `` | default = -1 |
| 2 | `name` | `string` | `optional` | `` |  |
| 3 | `name_loc` | `string` | `optional` | `` |  |
| 4 | `name_english_loc` | `string` | `optional` | `` |  |
| 5 | `neutral_item_tier` | `int32` | `optional` | `` |  |
| 6 | `is_pregame_suggested` | `bool` | `optional` | `` |  |
| 7 | `is_earlygame_suggested` | `bool` | `optional` | `` |  |
| 8 | `is_lategame_suggested` | `bool` | `optional` | `` |  |
| 9 | `recipes` | `.CMsgGameDataItemAbilityList.ItemAbilityInfo.Recipe` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGameDataItemAbilityList.ItemAbilityInfo.Recipe</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGameDataItemAbilityList.ItemAbilityInfo`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `items` | `int32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgLobbyAbilityDraftData</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `shuffle_draft_order` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CSOEconItemDropRateBonus</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` | (key_field) = true |
| 2 | `expiration_date` | `fixed32` | `optional` | `` |  |
| 3 | `bonus` | `float` | `optional` | `` | (key_field) = true |
| 4 | `bonus_count` | `uint32` | `optional` | `` |  |
| 5 | `item_id` | `uint64` | `optional` | `` |  |
| 6 | `def_index` | `uint32` | `optional` | `` |  |
| 7 | `seconds_left` | `uint32` | `optional` | `` |  |
| 8 | `booster_type` | `uint32` | `optional` | `` | (key_field) = true |

</details>

<details>
<summary><code>CSOEconItemTournamentPassport</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `league_id` | `uint32` | `optional` | `` |  |
| 3 | `item_id` | `uint64` | `optional` | `` |  |
| 4 | `original_purchaser_id` | `uint32` | `optional` | `` |  |
| 5 | `passports_bought` | `uint32` | `optional` | `` |  |
| 6 | `version` | `uint32` | `optional` | `` |  |
| 7 | `def_index` | `uint32` | `optional` | `` |  |
| 8 | `reward_flags` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgStickerbookSticker</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_def_id` | `uint32` | `optional` | `` |  |
| 2 | `sticker_num` | `uint32` | `optional` | `` |  |
| 3 | `quality` | `uint32` | `optional` | `` |  |
| 4 | `position_x` | `float` | `optional` | `` |  |
| 5 | `position_y` | `float` | `optional` | `` |  |
| 6 | `rotation` | `float` | `optional` | `` |  |
| 7 | `scale` | `float` | `optional` | `` |  |
| 8 | `position_z` | `float` | `optional` | `` |  |
| 9 | `source_item_id` | `uint64` | `optional` | `` |  |
| 10 | `depth_bias` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgStickerbookPage</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `page_num` | `uint32` | `optional` | `` |  |
| 2 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 3 | `team_id` | `uint32` | `optional` | `` |  |
| 4 | `stickers` | `.CMsgStickerbookSticker` | `repeated` | `` |  |
| 5 | `page_type` | `.EStickerbookPageType` | `optional` | `` | default = STICKER_PAGE_GENERIC |

</details>

<details>
<summary><code>CMsgStickerbookTeamPageOrderSequence</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `page_numbers` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgStickerbook</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `pages` | `.CMsgStickerbookPage` | `repeated` | `` |  |
| 2 | `team_page_order_sequence` | `.CMsgStickerbookTeamPageOrderSequence` | `optional` | `` |  |
| 3 | `favorite_page_num` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgStickerHero</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `item_def_id` | `uint32` | `optional` | `` |  |
| 3 | `quality` | `uint32` | `optional` | `` |  |
| 4 | `source_item_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgStickerHeroes</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `heroes` | `.CMsgStickerHero` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgHeroRoleStats</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `lane_selection_flags` | `uint32` | `optional` | `` |  |
| 2 | `match_count` | `uint32` | `optional` | `` |  |
| 3 | `win_count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgHeroRoleHeroStats</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `role_stats` | `.CMsgHeroRoleStats` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgHeroRoleRankStats</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `rank_tier` | `uint32` | `optional` | `` |  |
| 2 | `hero_stats` | `.CMsgHeroRoleHeroStats` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgHeroRoleAllRanksStats</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `start_timestamp` | `uint32` | `optional` | `` |  |
| 2 | `end_timestamp` | `uint32` | `optional` | `` |  |
| 3 | `rank_stats` | `.CMsgHeroRoleRankStats` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgMapStatsSnapshot</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `timestamp` | `uint32` | `optional` | `` |  |
| 2 | `lotuses_gained` | `uint64` | `optional` | `` |  |
| 3 | `wisdom_runes_gained` | `uint64` | `optional` | `` |  |
| 4 | `roshan_kills_day` | `uint64` | `optional` | `` |  |
| 5 | `roshan_kills_night` | `uint64` | `optional` | `` |  |
| 6 | `portals_used` | `uint64` | `optional` | `` |  |
| 7 | `watchers_taken` | `uint64` | `optional` | `` |  |
| 8 | `tormentor_kills` | `uint64` | `optional` | `` |  |
| 9 | `outposts_captured` | `uint64` | `optional` | `` |  |
| 10 | `shield_runes_gained` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGlobalMapStats</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `current` | `.CMsgMapStatsSnapshot` | `optional` | `` |  |
| 2 | `window_start` | `.CMsgMapStatsSnapshot` | `optional` | `` |  |
| 3 | `window_end` | `.CMsgMapStatsSnapshot` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTrackedStat</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `tracked_stat_id` | `uint32` | `optional` | `` |  |
| 2 | `tracked_stat_value` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAClaimEventActionResponse</code> — fields: 3; oneofs: 0; nested messages: 6; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgDOTAClaimEventActionResponse.ResultCode` | `optional` | `` | default = Success |
| 2 | `reward_results` | `.CMsgDOTAClaimEventActionResponse.GrantedRewardData` | `repeated` | `` |  |
| 3 | `action_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAClaimEventActionResponse.MysteryItemRewardData</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAClaimEventActionResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_def` | `uint32` | `optional` | `` |  |
| 2 | `item_category` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAClaimEventActionResponse.LootListRewardData</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAClaimEventActionResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_def` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAClaimEventActionResponse.ActionListRewardData</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAClaimEventActionResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `action_id` | `uint32` | `optional` | `` |  |
| 2 | `result_reward_data` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAClaimEventActionResponse.OverworldTokenRewardData</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: `CMsgDOTAClaimEventActionResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `tokens` | `.CMsgDOTAClaimEventActionResponse.OverworldTokenRewardData.TokenQuantity` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAClaimEventActionResponse.OverworldTokenRewardData.TokenQuantity</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAClaimEventActionResponse.OverworldTokenRewardData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `token_id` | `uint32` | `optional` | `` |  |
| 2 | `token_count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAClaimEventActionResponse.MonsterHunterMaterialRewardData</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: `CMsgDOTAClaimEventActionResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `materials` | `.CMsgDOTAClaimEventActionResponse.MonsterHunterMaterialRewardData.MaterialQuantity` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAClaimEventActionResponse.MonsterHunterMaterialRewardData.MaterialQuantity</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAClaimEventActionResponse.MonsterHunterMaterialRewardData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `material_id` | `uint32` | `optional` | `` |  |
| 2 | `material_count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAClaimEventActionResponse.GrantedRewardData</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAClaimEventActionResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `grant_index` | `uint32` | `optional` | `` |  |
| 2 | `score_index` | `uint32` | `optional` | `` |  |
| 3 | `reward_index` | `uint32` | `optional` | `` |  |
| 4 | `reward_data` | `bytes` | `optional` | `` |  |
| 5 | `action_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCDotaLabsFeedback</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `language` | `uint32` | `optional` | `` |  |
| 2 | `feedback_item` | `uint32` | `optional` | `` |  |
| 3 | `feedback` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCDotaLabsFeedbackResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCDotaLabsFeedbackResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CDotaMsg_PredictionResult</code> — fields: 4; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `match_id` | `uint64` | `optional` | `` |  |
| 3 | `correct` | `bool` | `optional` | `` |  |
| 4 | `predictions` | `.CDotaMsg_PredictionResult.Prediction` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDotaMsg_PredictionResult.Prediction</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: `CDotaMsg_PredictionResult`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_def` | `uint32` | `optional` | `` |  |
| 2 | `num_correct` | `uint32` | `optional` | `` |  |
| 3 | `num_fails` | `uint32` | `optional` | `` |  |
| 4 | `result` | `.CDotaMsg_PredictionResult.Prediction.EResult` | `optional` | `` | default = k_eResult_ItemGranted |
| 6 | `granted_item_defs` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDotaMsgStructuredTooltipProperties</code> — fields: 11; oneofs: 0; nested messages: 15; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ability_name_loc_token` | `string` | `optional` | `` |  |
| 2 | `ability_category_loc_token` | `string` | `optional` | `` |  |
| 3 | `ability_level` | `int32` | `optional` | `` |  |
| 4 | `current_mana_cost` | `int32` | `optional` | `` |  |
| 5 | `current_health_cost` | `int32` | `optional` | `` |  |
| 6 | `current_cooldown` | `float` | `optional` | `` |  |
| 7 | `summary_description_loc_token` | `string` | `optional` | `` |  |
| 8 | `summary_description_level_up_loc_token` | `string` | `optional` | `` |  |
| 9 | `summary_description_embed_values` | `.CDotaMsgStructuredTooltipProperties.SummaryDescriptionEmbedValue` | `repeated` | `` |  |
| 10 | `summary_description_facet` | `.CDotaMsgStructuredTooltipProperties.FacetDisplayProperties` | `optional` | `` |  |
| 20 | `chunks` | `.CDotaMsgStructuredTooltipProperties.TooltipContentChunk` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDotaMsgStructuredTooltipProperties.AttributeValueValue</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDotaMsgStructuredTooltipProperties`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `value` | `float` | `optional` | `` |  |
| 2 | `is_active_value` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDotaMsgStructuredTooltipProperties.AttributeValue_Single</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDotaMsgStructuredTooltipProperties`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `single_value` | `.CDotaMsgStructuredTooltipProperties.AttributeValueValue` | `optional` | `` |  |

</details>

<details>
<summary><code>CDotaMsgStructuredTooltipProperties.AttributeValue_Variable</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDotaMsgStructuredTooltipProperties`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `values` | `.CDotaMsgStructuredTooltipProperties.AttributeValueValue` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDotaMsgStructuredTooltipProperties.AttributeValue_Delta</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDotaMsgStructuredTooltipProperties`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `prev` | `.CDotaMsgStructuredTooltipProperties.AttributeValueValue` | `optional` | `` |  |
| 2 | `next` | `.CDotaMsgStructuredTooltipProperties.AttributeValueValue` | `optional` | `` |  |

</details>

<details>
<summary><code>CDotaMsgStructuredTooltipProperties.AttributeValue</code> — fields: 3; oneofs: 1; nested messages: 0; nested enums: 0</summary>

- Parent: `CDotaMsgStructuredTooltipProperties`
- Oneofs: `attr_value`

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `single` | `.CDotaMsgStructuredTooltipProperties.AttributeValue_Single` | `oneof` | `attr_value` |  |
| 2 | `variable` | `.CDotaMsgStructuredTooltipProperties.AttributeValue_Variable` | `oneof` | `attr_value` |  |
| 3 | `delta` | `.CDotaMsgStructuredTooltipProperties.AttributeValue_Delta` | `oneof` | `attr_value` |  |

</details>

<details>
<summary><code>CDotaMsgStructuredTooltipProperties.FacetDisplayProperties</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDotaMsgStructuredTooltipProperties`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `facet_name_loc_token` | `string` | `optional` | `` |  |
| 2 | `facet_desc_loc_token` | `string` | `optional` | `` |  |
| 3 | `facet_icon_style_name` | `string` | `optional` | `` |  |
| 4 | `facet_color_style_name` | `string` | `optional` | `` |  |
| 5 | `facet_gradient_style_name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CDotaMsgStructuredTooltipProperties.Attribute</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDotaMsgStructuredTooltipProperties`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name_loc_token` | `string` | `optional` | `` |  |
| 2 | `type` | `.CDotaMsgStructuredTooltipProperties.EAttributeType` | `optional` | `` | default = kUnknown |
| 3 | `value` | `.CDotaMsgStructuredTooltipProperties.AttributeValue` | `optional` | `` |  |
| 4 | `facet` | `.CDotaMsgStructuredTooltipProperties.FacetDisplayProperties` | `optional` | `` |  |

</details>

<details>
<summary><code>CDotaMsgStructuredTooltipProperties.AttributeGroupDesc_Basic</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDotaMsgStructuredTooltipProperties`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CDotaMsgStructuredTooltipProperties.AttributeGroupDesc_Specific</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDotaMsgStructuredTooltipProperties`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `title_loc_token` | `string` | `optional` | `` |  |
| 2 | `desc_loc_token` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CDotaMsgStructuredTooltipProperties.AttributeGroupDesc_Facet</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDotaMsgStructuredTooltipProperties`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `facet` | `.CDotaMsgStructuredTooltipProperties.FacetDisplayProperties` | `optional` | `` |  |

</details>

<details>
<summary><code>CDotaMsgStructuredTooltipProperties.AttributeGroupDescription</code> — fields: 3; oneofs: 1; nested messages: 0; nested enums: 0</summary>

- Parent: `CDotaMsgStructuredTooltipProperties`
- Oneofs: `attr_group_desc`

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `basic` | `.CDotaMsgStructuredTooltipProperties.AttributeGroupDesc_Basic` | `oneof` | `attr_group_desc` |  |
| 2 | `specific` | `.CDotaMsgStructuredTooltipProperties.AttributeGroupDesc_Specific` | `oneof` | `attr_group_desc` |  |
| 3 | `facet` | `.CDotaMsgStructuredTooltipProperties.AttributeGroupDesc_Facet` | `oneof` | `attr_group_desc` |  |

</details>

<details>
<summary><code>CDotaMsgStructuredTooltipProperties.AttributeGroup</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDotaMsgStructuredTooltipProperties`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `desc` | `.CDotaMsgStructuredTooltipProperties.AttributeGroupDescription` | `optional` | `` |  |
| 2 | `attributes` | `.CDotaMsgStructuredTooltipProperties.Attribute` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDotaMsgStructuredTooltipProperties.ContentChunk_AttributeGroup</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDotaMsgStructuredTooltipProperties`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `groups` | `.CDotaMsgStructuredTooltipProperties.AttributeGroup` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDotaMsgStructuredTooltipProperties.TooltipContentChunk</code> — fields: 1; oneofs: 1; nested messages: 0; nested enums: 0</summary>

- Parent: `CDotaMsgStructuredTooltipProperties`
- Oneofs: `content_chunk`

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `attribute_group` | `.CDotaMsgStructuredTooltipProperties.ContentChunk_AttributeGroup` | `oneof` | `content_chunk` |  |

</details>

<details>
<summary><code>CDotaMsgStructuredTooltipProperties.SummaryDescriptionEmbedValue</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDotaMsgStructuredTooltipProperties`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `type` | `.CDotaMsgStructuredTooltipProperties.EAttributeType` | `optional` | `` | default = kUnknown |
| 3 | `value` | `.CDotaMsgStructuredTooltipProperties.AttributeValue` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>ESpecialPingValue</code> — values: 2</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_ESpecialPingValue_NoData` | 16382 |
| `k_ESpecialPingValue_Failed` | 16383 |

</details>

<details>
<summary><code>EDOTAGCSessionNeed</code> — values: 14</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EDOTAGCSessionNeed_Unknown` | 0 |
| `k_EDOTAGCSessionNeed_UserNoSessionNeeded` | 100 |
| `k_EDOTAGCSessionNeed_UserInOnlineGame` | 101 |
| `k_EDOTAGCSessionNeed_UserInLocalGame` | 102 |
| `k_EDOTAGCSessionNeed_UserInUIWasConnected` | 103 |
| `k_EDOTAGCSessionNeed_UserInUINeverConnected` | 104 |
| `k_EDOTAGCSessionNeed_UserTutorials` | 105 |
| `k_EDOTAGCSessionNeed_UserInUIWasConnectedIdle` | 106 |
| `k_EDOTAGCSessionNeed_UserInUINeverConnectedIdle` | 107 |
| `k_EDOTAGCSessionNeed_GameServerOnline` | 200 |
| `k_EDOTAGCSessionNeed_GameServerLocal` | 201 |
| `k_EDOTAGCSessionNeed_GameServerIdle` | 202 |
| `k_EDOTAGCSessionNeed_GameServerRelay` | 203 |
| `k_EDOTAGCSessionNeed_GameServerLocalUpload` | 204 |

</details>

<details>
<summary><code>EDOTAMatchPlayerTimeCustomStat</code> — values: 3</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EDOTA_MatchPlayerTimeCustomStat_HPRegenUnderT1Towers` | 1 |
| `k_EDOTA_MatchPlayerTimeCustomStat_MagicDamageReducedWithNewFormula_Absolute` | 2 |
| `k_EDOTA_MatchPlayerTimeCustomStat_MagicDamageReducedWithNewFormula_PercentOfTotalHP` | 3 |

</details>

<details>
<summary><code>DOTA_TournamentEvents</code> — values: 12</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `TE_FIRST_BLOOD` | 0 |
| `TE_GAME_END` | 1 |
| `TE_MULTI_KILL` | 2 |
| `TE_HERO_DENY` | 3 |
| `TE_AEGIS_DENY` | 4 |
| `TE_AEGIS_STOLEN` | 5 |
| `TE_GODLIKE` | 6 |
| `TE_COURIER_KILL` | 7 |
| `TE_ECHOSLAM` | 8 |
| `TE_RAPIER` | 9 |
| `TE_EARLY_ROSHAN` | 10 |
| `TE_BLACK_HOLE` | 11 |

</details>

<details>
<summary><code>EBroadcastTimelineEvent</code> — values: 9</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `EBroadcastTimelineEvent_MatchStarted` | 1 |
| `EBroadcastTimelineEvent_GameStateChanged` | 2 |
| `EBroadcastTimelineEvent_TowerDeath` | 3 |
| `EBroadcastTimelineEvent_BarracksDeath` | 4 |
| `EBroadcastTimelineEvent_AncientDeath` | 5 |
| `EBroadcastTimelineEvent_RoshanDeath` | 6 |
| `EBroadcastTimelineEvent_HeroDeath` | 7 |
| `EBroadcastTimelineEvent_TeamFight` | 8 |
| `EBroadcastTimelineEvent_FirstBlood` | 9 |

</details>

<details>
<summary><code>ECustomGameWhitelistState</code> — values: 3</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `CUSTOM_GAME_WHITELIST_STATE_UNKNOWN` | 0 |
| `CUSTOM_GAME_WHITELIST_STATE_APPROVED` | 1 |
| `CUSTOM_GAME_WHITELIST_STATE_REJECTED` | 2 |

</details>

<details>
<summary><code>EDOTATriviaQuestionCategory</code> — values: 18</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EDOTATriviaQuestionCategory_AbilityIcon` | 0 |
| `k_EDOTATriviaQuestionCategory_AbilityCooldown` | 1 |
| `k_EDOTATriviaQuestionCategory_HeroAttributes` | 2 |
| `k_EDOTATriviaQuestionCategory_HeroMovementSpeed` | 3 |
| `k_EDOTATriviaQuestionCategory_TalentTree` | 4 |
| `k_EDOTATriviaQuestionCategory_HeroStats` | 5 |
| `k_EDOTATriviaQuestionCategory_ItemPrice` | 6 |
| `k_EDOTATriviaQuestionCategory_AbilitySound` | 7 |
| `k_EDOTATriviaQuestionCategory_InvokerSpells` | 8 |
| `k_EDOTATriviaQuestionCategory_AbilityManaCost` | 9 |
| `k_EDOTATriviaQuestionCategory_HeroAttackSound` | 10 |
| `k_EDOTATriviaQuestionCategory_AbilityName` | 11 |
| `k_EDOTATriviaQuestionCategory_ItemComponents` | 12 |
| `k_EDOTATriviaQuestionCategory_ItemLore` | 13 |
| `k_EDOTATriviaQuestionCategory_ItemPassives` | 14 |
| `k_EDOTATriviaQuestionCategory_STATIC_QUESTIONS_END` | 15 |
| `k_EDOTATriviaQuestionCategory_DYNAMIC_QUESTIONS_START` | 99 |
| `k_EDOTATriviaQuestionCategory_Dynamic_ItemBuild` | 100 |

</details>

<details>
<summary><code>EOverwatchConviction</code> — values: 4</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EOverwatchConviction_None` | 0 |
| `k_EOverwatchConviction_NotGuilty` | 1 |
| `k_EOverwatchConviction_GuiltUnclear` | 2 |
| `k_EOverwatchConviction_Guilty` | 3 |

</details>

<details>
<summary><code>EHeroRelicRarity</code> — values: 3</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `HERO_RELIC_RARITY_INVALID` | -1 |
| `HERO_RELIC_RARITY_COMMON` | 0 |
| `HERO_RELIC_RARITY_RARE` | 1 |

</details>

<details>
<summary><code>EStickerbookAuditAction</code> — values: 5</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `STICKERBOOK_AUDIT_CREATE_PAGE` | 0 |
| `STICKERBOOK_AUDIT_DELETE_PAGE` | 1 |
| `STICKERBOOK_AUDIT_STICK_STICKERS` | 2 |
| `STICKERBOOK_AUDIT_REPLACE_STICKERS` | 3 |
| `STICKERBOOK_AUDIT_HERO_STICKER` | 4 |

</details>

<details>
<summary><code>EStickerbookPageType</code> — values: 3</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `STICKER_PAGE_GENERIC` | 0 |
| `STICKER_PAGE_TEAM` | 1 |
| `STICKER_PAGE_TALENT` | 2 |

</details>

<details>
<summary><code>ENewBloomGiftingResponse</code> — values: 13</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `kENewBloomGifting_Success` | 0 |
| `kENewBloomGifting_UnknownFailure` | 1 |
| `kENewBloomGifting_MalformedRequest` | 2 |
| `kENewBloomGifting_FeatureDisabled` | 3 |
| `kENewBloomGifting_ItemNotFound` | 4 |
| `kENewBloomGifting_PlayerNotAllowedToGiveGifts` | 5 |
| `kENewBloomGifting_TargetNotAllowedToReceiveGifts` | 6 |
| `kENewBloomGifting_ServerNotAuthorized` | 100 |
| `kENewBloomGifting_PlayerNotInLobby` | 101 |
| `kENewBloomGifting_TargetNotInLobby` | 102 |
| `kENewBloomGifting_LobbyNotEligible` | 103 |
| `kENewBloomGifting_TargetNotFriend` | 200 |
| `kENewBloomGifting_TargetFriendDurationTooShort` | 201 |

</details>

<details>
<summary><code>CMsgDOTAProfileCard.EStatID</code> — values: 6</summary>

- Parent: `CMsgDOTAProfileCard`

| Name | Number |
|---|---:|
| `k_eStat_Wins` | 3 |
| `k_eStat_Commends` | 4 |
| `k_eStat_GamesPlayed` | 5 |
| `k_eStat_FirstMatchDate` | 6 |
| `k_eStat_PreviousSeasonRank` | 7 |
| `k_eStat_GamesMVP` | 8 |

</details>

<details>
<summary><code>CMsgGCRerollPlayerChallengeResponse.EResult</code> — values: 5</summary>

- Parent: `CMsgGCRerollPlayerChallengeResponse`

| Name | Number |
|---|---:|
| `eResult_Success` | 0 |
| `eResult_Dropped` | 1 |
| `eResult_NotFound` | 2 |
| `eResult_CantReroll` | 3 |
| `eResult_ServerError` | 4 |

</details>

<details>
<summary><code>CMsgDOTARealtimeGameStats.GraphData.eStat</code> — values: 4</summary>

- Parent: `CMsgDOTARealtimeGameStats.GraphData`

| Name | Number |
|---|---:|
| `CreepGoldEarned` | 0 |
| `KillGoldEarned` | 1 |
| `DeathAndBuybackGoldLost` | 2 |
| `XPEarned` | 3 |

</details>

<details>
<summary><code>CMsgDOTARealtimeGameStats.GraphData.eLocation</code> — values: 6</summary>

- Parent: `CMsgDOTARealtimeGameStats.GraphData`

| Name | Number |
|---|---:|
| `BotLane` | 0 |
| `MidLane` | 1 |
| `TopLane` | 2 |
| `Jungle` | 3 |
| `Ancients` | 4 |
| `Other` | 5 |

</details>

<details>
<summary><code>CMsgInGamePrediction.ERawValueType_t</code> — values: 2</summary>

- Parent: `CMsgInGamePrediction`

| Name | Number |
|---|---:|
| `Number` | 0 |
| `Time` | 1 |

</details>

<details>
<summary><code>CMsgInGamePrediction.EPredictionType</code> — values: 7</summary>

- Parent: `CMsgInGamePrediction`

| Name | Number |
|---|---:|
| `Generic` | 0 |
| `Hero` | 1 |
| `Team` | 2 |
| `Player` | 3 |
| `Special` | 4 |
| `YesNo` | 5 |
| `QualifiersTeam` | 6 |

</details>

<details>
<summary><code>CMsgInGamePrediction.EResolutionType_t</code> — values: 9</summary>

- Parent: `CMsgInGamePrediction`

| Name | Number |
|---|---:|
| `InvalidQuery` | 0 |
| `FirstToPassQuery` | 1 |
| `LastToPassQuery` | 2 |
| `LastRemainingQuery` | 3 |
| `MaxToPassQuery` | 4 |
| `MinToPassQuery` | 5 |
| `SumQuery` | 6 |
| `MaxTeamSumToPassQuery` | 7 |
| `MinTeamSumToPassQuery` | 8 |

</details>

<details>
<summary><code>CMsgInGamePrediction.ERandomSelectionGroup_t</code> — values: 4</summary>

- Parent: `CMsgInGamePrediction`

| Name | Number |
|---|---:|
| `EarlyGame` | 0 |
| `MidGame` | 1 |
| `LateGame` | 2 |
| `Count` | 3 |

</details>

<details>
<summary><code>CMsgDOTASeasonPredictions.Prediction.EPredictionType</code> — values: 8</summary>

- Parent: `CMsgDOTASeasonPredictions.Prediction`

| Name | Number |
|---|---:|
| `Generic` | 0 |
| `Hero` | 1 |
| `Team` | 2 |
| `Player` | 3 |
| `Special` | 4 |
| `YesNo` | 5 |
| `QualifiersTeam` | 6 |
| `LastChanceTeam` | 7 |

</details>

<details>
<summary><code>CMsgDOTASeasonPredictions.Prediction.EAnswerType</code> — values: 8</summary>

- Parent: `CMsgDOTASeasonPredictions.Prediction`

| Name | Number |
|---|---:|
| `SingleInt` | 0 |
| `SingleFloat` | 1 |
| `MultipleInt` | 2 |
| `MultipleFloat` | 3 |
| `AnswerTeam` | 4 |
| `SingleTime` | 5 |
| `MultipleTime` | 6 |
| `NoAnswer` | 7 |

</details>

<details>
<summary><code>CMsgDOTAMatch.ReplayState</code> — values: 3</summary>

- Parent: `CMsgDOTAMatch`

| Name | Number |
|---|---:|
| `REPLAY_AVAILABLE` | 0 |
| `REPLAY_NOT_RECORDED` | 1 |
| `REPLAY_EXPIRED` | 2 |

</details>

<details>
<summary><code>CMsgDOTAMatch.Player.HeroDamageType</code> — values: 3</summary>

- Parent: `CMsgDOTAMatch.Player`

| Name | Number |
|---|---:|
| `HERO_DAMAGE_PHYSICAL` | 0 |
| `HERO_DAMAGE_MAGICAL` | 1 |
| `HERO_DAMAGE_PURE` | 2 |

</details>

<details>
<summary><code>CMsgServerToGCRequestPlayerRecentAccomplishmentsResponse.EResponse</code> — values: 4</summary>

- Parent: `CMsgServerToGCRequestPlayerRecentAccomplishmentsResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |

</details>

<details>
<summary><code>CMsgDOTAClaimEventActionResponse.ResultCode</code> — values: 15</summary>

- Parent: `CMsgDOTAClaimEventActionResponse`

| Name | Number |
|---|---:|
| `Success` | 0 |
| `InvalidEvent` | 1 |
| `EventNotActive` | 2 |
| `InvalidAction` | 3 |
| `ServerError` | 4 |
| `InsufficientPoints` | 5 |
| `InsufficentLevel` | 6 |
| `AlreadyClaimed` | 7 |
| `SDOLockFailure` | 8 |
| `SDOLoadFailure` | 9 |
| `EventNotOwned` | 10 |
| `Timeout` | 11 |
| `RequiresPlusSubscription` | 12 |
| `InvalidItem` | 13 |
| `AsyncRewards` | 14 |

</details>

<details>
<summary><code>CMsgClientToGCDotaLabsFeedbackResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCDotaLabsFeedbackResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNotAllowed` | 5 |
| `k_eInvalidItem` | 6 |

</details>

<details>
<summary><code>CDotaMsg_PredictionResult.Prediction.EResult</code> — values: 2</summary>

- Parent: `CDotaMsg_PredictionResult.Prediction`

| Name | Number |
|---|---:|
| `k_eResult_ItemGranted` | 1 |
| `k_eResult_Destroyed` | 2 |

</details>

<details>
<summary><code>CDotaMsgStructuredTooltipProperties.EAttributeType</code> — values: 14</summary>

- Parent: `CDotaMsgStructuredTooltipProperties`

| Name | Number |
|---|---:|
| `kUnknown` | 0 |
| `kDuration` | 1 |
| `kManaCost` | 2 |
| `kHealthCost` | 3 |
| `kCastRange` | 4 |
| `kAreaOfEffectRadius` | 5 |
| `kPhysicalDamage` | 6 |
| `kMagicalDamage` | 7 |
| `kPureDamage` | 8 |
| `kCooldown` | 9 |
| `kDebuffPercentage` | 10 |
| `kDebuffValue` | 11 |
| `kBuffPercentage` | 12 |
| `kBuffValue` | 13 |

</details>
