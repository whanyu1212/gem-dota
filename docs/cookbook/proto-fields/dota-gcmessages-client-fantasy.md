# dota_gcmessages_client_fantasy.proto

- Module: `dota_gcmessages_client_fantasy_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **1**
- Messages: **59** (top-level: 38)
- Enums: **13** (top-level: 1)

## Imports

- `dota_shared_enums.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgDOTAPlayerInfo</code> — fields: 16; oneofs: 0; nested messages: 3; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `name` | `string` | `optional` | `` |  |
| 3 | `country_code` | `string` | `optional` | `` |  |
| 4 | `fantasy_role` | `.Fantasy_Roles` | `optional` | `` | default = FANTASY_ROLE_UNDEFINED |
| 5 | `team_id` | `uint32` | `optional` | `` |  |
| 6 | `team_name` | `string` | `optional` | `` |  |
| 7 | `team_tag` | `string` | `optional` | `` |  |
| 8 | `sponsor` | `string` | `optional` | `` |  |
| 11 | `real_name` | `string` | `optional` | `` |  |
| 13 | `total_earnings` | `uint32` | `optional` | `` |  |
| 14 | `results` | `.CMsgDOTAPlayerInfo.Results` | `repeated` | `` |  |
| 15 | `team_url_logo` | `string` | `optional` | `` |  |
| 16 | `audit_entries` | `.CMsgDOTAPlayerInfo.AuditEntry` | `repeated` | `` |  |
| 17 | `team_abbreviation` | `string` | `optional` | `` |  |
| 18 | `pro_registration` | `.CMsgDOTAPlayerInfo.ProRegistration` | `repeated` | `` |  |
| 19 | `has_played_in_international` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAPlayerInfo.Results</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAPlayerInfo`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_id` | `uint32` | `optional` | `` |  |
| 2 | `placement` | `uint32` | `optional` | `` |  |
| 3 | `earnings` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAPlayerInfo.AuditEntry</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAPlayerInfo`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `start_timestamp` | `uint32` | `optional` | `` |  |
| 2 | `end_timestamp` | `uint32` | `optional` | `` |  |
| 3 | `team_id` | `uint32` | `optional` | `` |  |
| 4 | `team_name` | `string` | `optional` | `` |  |
| 5 | `team_tag` | `string` | `optional` | `` |  |
| 6 | `team_url_logo` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAPlayerInfo.ProRegistration</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAPlayerInfo`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `registration_period` | `uint32` | `optional` | `` |  |
| 2 | `timestamp` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAPlayerInfoList</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_infos` | `.CMsgDOTAPlayerInfo` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTATeamRoster</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `timestamp` | `uint32` | `optional` | `` |  |
| 2 | `team_id` | `uint32` | `optional` | `` |  |
| 3 | `member_account_ids` | `uint32` | `repeated` | `` |  |
| 4 | `coach_account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTADPCProfileInfo</code> — fields: 4; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_info` | `.CMsgDOTAPlayerInfo` | `optional` | `` |  |
| 2 | `prediction_info` | `.CMsgDOTADPCProfileInfo.PredictionInfo` | `optional` | `` |  |
| 3 | `fantasy_info` | `.CMsgDOTADPCProfileInfo.FantasyInfo` | `optional` | `` |  |
| 4 | `disabled_notifications` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTADPCProfileInfo.PredictionInfo</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTADPCProfileInfo`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `percent` | `uint32` | `optional` | `` |  |
| 2 | `shard_winnings` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTADPCProfileInfo.FantasyInfo</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTADPCProfileInfo`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `top_90_finishes` | `uint32` | `optional` | `` |  |
| 2 | `top_75_finishes` | `uint32` | `optional` | `` |  |
| 3 | `top_50_finishes` | `uint32` | `optional` | `` |  |
| 4 | `shard_winnings` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALeaderboards</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `leaderboards` | `.CMsgDOTALeaderboards.RegionLeaderboard` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALeaderboards.RegionLeaderboard</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTALeaderboards`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `division` | `uint32` | `optional` | `` |  |
| 2 | `account_ids` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAPassportVoteTeamGuess</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_id` | `uint32` | `optional` | `` |  |
| 2 | `winner_id` | `uint32` | `optional` | `` |  |
| 3 | `runnerup_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAPassportVoteGenericSelection</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `selection_index` | `.DOTA_2013PassportSelectionIndices` | `optional` | `` | default = PP13_SEL_ALLSTAR_PLAYER_0 |
| 2 | `selection` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAPassportStampedPlayer</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steam_id` | `uint64` | `optional` | `` |  |
| 2 | `stamp_level` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAPassportPlayerCardChallenge</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `challenge_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAPassportVote</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team_votes` | `.CMsgDOTAPassportVoteTeamGuess` | `repeated` | `` |  |
| 2 | `generic_selections` | `.CMsgDOTAPassportVoteGenericSelection` | `repeated` | `` |  |
| 3 | `stamped_players` | `.CMsgDOTAPassportStampedPlayer` | `repeated` | `` |  |
| 4 | `player_card_challenges` | `.CMsgDOTAPassportPlayerCardChallenge` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetPlayerCardRosterRequest</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_id` | `uint32` | `optional` | `` |  |
| 3 | `fantasy_period` | `uint32` | `optional` | `` | default = 4294967295 |

</details>

<details>
<summary><code>CMsgClientToGCGetPlayerCardRosterResponse</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCGetPlayerCardRosterResponse.Result` | `optional` | `` | default = SUCCESS |
| 2 | `player_card_item_id` | `uint64` | `repeated` | `` |  |
| 3 | `score` | `float` | `optional` | `` |  |
| 4 | `finalized` | `bool` | `optional` | `` |  |
| 5 | `percentile` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCBatchGetPlayerCardRosterRequest</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_timestamps` | `.CMsgClientToGCBatchGetPlayerCardRosterRequest.LeagueTimestamp` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCBatchGetPlayerCardRosterRequest.LeagueTimestamp</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCBatchGetPlayerCardRosterRequest`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_id` | `uint32` | `optional` | `` |  |
| 3 | `fantasy_period` | `uint32` | `optional` | `` | default = 4294967295 |

</details>

<details>
<summary><code>CMsgClientToGCBatchGetPlayerCardRosterResponse</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `responses` | `.CMsgClientToGCBatchGetPlayerCardRosterResponse.RosterResponse` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCBatchGetPlayerCardRosterResponse.RosterResponse</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCBatchGetPlayerCardRosterResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_id` | `uint32` | `optional` | `` |  |
| 2 | `deprecated_timestamp` | `uint32` | `optional` | `` |  |
| 3 | `result` | `.CMsgClientToGCBatchGetPlayerCardRosterResponse.Result` | `optional` | `` | default = SUCCESS |
| 4 | `player_card_item_id` | `uint64` | `repeated` | `` |  |
| 5 | `score` | `float` | `optional` | `` |  |
| 6 | `finalized` | `bool` | `optional` | `` |  |
| 7 | `percentile` | `float` | `optional` | `` |  |
| 8 | `fantasy_period` | `uint32` | `optional` | `` | default = 4294967295 |

</details>

<details>
<summary><code>CMsgClientToGCSetPlayerCardRosterRequest</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_id` | `uint32` | `optional` | `` |  |
| 2 | `deprecated_timestamp` | `uint32` | `optional` | `` |  |
| 3 | `slot` | `uint32` | `optional` | `` |  |
| 4 | `player_card_item_id` | `uint64` | `optional` | `` |  |
| 5 | `event_id` | `uint32` | `optional` | `` |  |
| 6 | `fantasy_period` | `uint32` | `optional` | `` | default = 4294967295 |

</details>

<details>
<summary><code>CMsgClientToGCSetPlayerCardRosterResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCSetPlayerCardRosterResponse.Result` | `optional` | `` | default = SUCCESS |

</details>

<details>
<summary><code>CMsgDOTAFantasyDPCLeagueStatus</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_infos` | `.CMsgDOTAFantasyDPCLeagueStatus.LeagueInfo` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAFantasyDPCLeagueStatus.LeagueInfo</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAFantasyDPCLeagueStatus`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_id` | `uint32` | `optional` | `` |  |
| 2 | `league_name` | `string` | `optional` | `` |  |
| 3 | `start_timestamp` | `uint32` | `optional` | `` |  |
| 4 | `end_timestamp` | `uint32` | `optional` | `` |  |
| 5 | `day_timestamps` | `uint32` | `repeated` | `` |  |
| 8 | `status` | `.CMsgDOTAFantasyDPCLeagueStatus.ERosterStatus` | `optional` | `` | default = UNSET |

</details>

<details>
<summary><code>CMsgDOTADPCSearchResults</code> — fields: 3; oneofs: 0; nested messages: 3; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `players` | `.CMsgDOTADPCSearchResults.Player` | `repeated` | `` |  |
| 2 | `teams` | `.CMsgDOTADPCSearchResults.Team` | `repeated` | `` |  |
| 3 | `leagues` | `.CMsgDOTADPCSearchResults.League` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTADPCSearchResults.Player</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTADPCSearchResults`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `id` | `uint32` | `optional` | `` |  |
| 2 | `name` | `string` | `optional` | `` |  |
| 3 | `real_name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTADPCSearchResults.Team</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTADPCSearchResults`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `id` | `uint32` | `optional` | `` |  |
| 2 | `name` | `string` | `optional` | `` |  |
| 3 | `url` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTADPCSearchResults.League</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTADPCSearchResults`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `id` | `uint32` | `optional` | `` |  |
| 2 | `name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTADPCTeamFavoriteRankings</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `teams` | `.CMsgDOTADPCTeamFavoriteRankings.Team` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTADPCTeamFavoriteRankings.Team</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTADPCTeamFavoriteRankings`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team_id` | `uint32` | `optional` | `` |  |
| 2 | `favorites` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDotaFantasyCraftingTabletPeriodData</code> — fields: 2; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `fantasy_period` | `uint32` | `optional` | `` | default = 4294967295 |
| 2 | `tablets` | `.CMsgDotaFantasyCraftingTabletPeriodData.Tablet` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDotaFantasyCraftingTabletPeriodData.Gem</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDotaFantasyCraftingTabletPeriodData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `type` | `.Fantasy_Gem_Type` | `optional` | `` | default = FANTASY_GEM_TYPE_RUBY |
| 2 | `slot` | `uint32` | `optional` | `` |  |
| 3 | `shape` | `uint32` | `optional` | `` |  |
| 4 | `quality` | `uint32` | `optional` | `` |  |
| 5 | `stat` | `.Fantasy_Scoring` | `optional` | `` | default = FANTASY_SCORING_KILLS |

</details>

<details>
<summary><code>CMsgDotaFantasyCraftingTabletPeriodData.Tablet</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDotaFantasyCraftingTabletPeriodData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `tablet_id` | `uint32` | `optional` | `` |  |
| 2 | `tablet_level` | `uint32` | `optional` | `` |  |
| 3 | `fantasy_role` | `.Fantasy_Roles` | `optional` | `` | default = FANTASY_ROLE_UNDEFINED |
| 4 | `account_id` | `uint32` | `optional` | `` |  |
| 5 | `prefix` | `uint32` | `optional` | `` |  |
| 6 | `suffix` | `uint32` | `optional` | `` |  |
| 7 | `gems` | `.CMsgDotaFantasyCraftingTabletPeriodData.Gem` | `repeated` | `` |  |
| 8 | `score` | `float` | `optional` | `` |  |
| 9 | `best_series` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDotaFantasyCraftingTabletData</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `tablet_period_data` | `.CMsgDotaFantasyCraftingTabletData.TabletPeriodDataEntry` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDotaFantasyCraftingTabletData.TabletPeriodDataEntry</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDotaFantasyCraftingTabletData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `key` | `uint32` | `optional` | `` |  |
| 2 | `value` | `.CMsgDotaFantasyCraftingTabletPeriodData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDotaFantasyCraftingUserData</code> — fields: 3; oneofs: 0; nested messages: 3; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `available_rolls` | `uint32` | `repeated` | `` |  |
| 2 | `period_roll_tokens` | `.CMsgDotaFantasyCraftingUserData.PeriodRollTokensEntry` | `repeated` | `` |  |
| 3 | `period_scores` | `.CMsgDotaFantasyCraftingUserData.PeriodScoresEntry` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDotaFantasyCraftingUserData.PeriodScore</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDotaFantasyCraftingUserData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `total_score` | `float` | `optional` | `` |  |
| 2 | `percentile` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDotaFantasyCraftingUserData.PeriodRollTokensEntry</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDotaFantasyCraftingUserData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `key` | `uint32` | `optional` | `` |  |
| 2 | `value` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDotaFantasyCraftingUserData.PeriodScoresEntry</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDotaFantasyCraftingUserData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `key` | `uint32` | `optional` | `` |  |
| 2 | `value` | `.CMsgDotaFantasyCraftingUserData.PeriodScore` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDotaFantasyCraftingDataCache</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `cache_entries` | `.CMsgDotaFantasyCraftingDataCache.CacheEntry` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDotaFantasyCraftingDataCache.CacheEntry</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDotaFantasyCraftingDataCache`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `fantasy_league` | `uint32` | `optional` | `` |  |
| 3 | `cache_data` | `.CMsgGCToClientFantasyCraftingDataUpdated` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCFantasyCraftingGetData</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `fantasy_league` | `uint32` | `optional` | `` |  |
| 2 | `account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCFantasyCraftingGetDataResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCFantasyCraftingGetDataResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `user_data` | `.CMsgDotaFantasyCraftingUserData` | `optional` | `` |  |
| 4 | `tablet_data` | `.CMsgDotaFantasyCraftingTabletData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCFantasyCraftingPerformOperation</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `fantasy_league` | `uint32` | `optional` | `` |  |
| 2 | `tablet_id` | `uint32` | `optional` | `` |  |
| 3 | `operation_id` | `uint32` | `optional` | `` |  |
| 4 | `extra_data` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCFantasyCraftingPerformOperationResponse</code> — fields: 9; oneofs: 0; nested messages: 1; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCFantasyCraftingPerformOperationResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `operation_id` | `uint32` | `optional` | `` |  |
| 3 | `player_choices` | `uint32` | `repeated` | `` |  |
| 4 | `prefix_choices` | `uint32` | `repeated` | `` |  |
| 5 | `suffix_choices` | `uint32` | `repeated` | `` |  |
| 6 | `title_choices` | `.CMsgClientToGCFantasyCraftingPerformOperationResponse.TitleChoice` | `repeated` | `` |  |
| 7 | `tablet_id` | `uint32` | `optional` | `` |  |
| 8 | `user_data` | `.CMsgDotaFantasyCraftingUserData` | `optional` | `` |  |
| 9 | `tablet_data` | `.CMsgDotaFantasyCraftingTabletData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCFantasyCraftingPerformOperationResponse.TitleChoice</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCFantasyCraftingPerformOperationResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `prefix_choice` | `uint32` | `optional` | `` |  |
| 2 | `suffix_choice` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientFantasyCraftingDataUpdated</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `fantasy_league` | `uint32` | `optional` | `` |  |
| 2 | `user_data` | `.CMsgDotaFantasyCraftingUserData` | `optional` | `` |  |
| 4 | `tablet_data` | `.CMsgDotaFantasyCraftingTabletData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCFantasyCraftingDevModifyTablet</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `fantasy_league` | `uint32` | `optional` | `` |  |
| 2 | `reset_tablet` | `bool` | `optional` | `` |  |
| 3 | `modify_tokens` | `uint32` | `optional` | `` |  |
| 5 | `fantasy_period` | `uint32` | `optional` | `` | default = 4294967295 |
| 6 | `upgrade_tablets` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCFantasyCraftingDevModifyTabletResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCFantasyCraftingDevModifyTabletResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `user_data` | `.CMsgDotaFantasyCraftingUserData` | `optional` | `` |  |
| 3 | `tablet_data` | `.CMsgDotaFantasyCraftingTabletData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCFantasyCraftingSelectPlayer</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `fantasy_league` | `uint32` | `optional` | `` |  |
| 2 | `account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCFantasyCraftingSelectPlayerResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCFantasyCraftingSelectPlayerResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `tablet_data` | `.CMsgDotaFantasyCraftingTabletData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCFantasyCraftingGenerateTablets</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `fantasy_league` | `uint32` | `optional` | `` |  |
| 2 | `account_ids` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCFantasyCraftingGenerateTabletsResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCFantasyCraftingGenerateTabletsResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `user_data` | `.CMsgDotaFantasyCraftingUserData` | `optional` | `` |  |
| 3 | `tablet_data` | `.CMsgDotaFantasyCraftingTabletData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGcFantasyCraftingUpgradeTablets</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `fantasy_league` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGcFantasyCraftingUpgradeTabletsResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGcFantasyCraftingUpgradeTabletsResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 3 | `tablet_data` | `.CMsgDotaFantasyCraftingTabletData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCFantasyCraftingRerollOptions</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `fantasy_league` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCFantasyCraftingRerollOptionsResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCFantasyCraftingRerollOptionsResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `user_data` | `.CMsgDotaFantasyCraftingUserData` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>DOTA_2013PassportSelectionIndices</code> — values: 96</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `PP13_SEL_ALLSTAR_PLAYER_0` | 0 |
| `PP13_SEL_ALLSTAR_PLAYER_1` | 1 |
| `PP13_SEL_ALLSTAR_PLAYER_2` | 2 |
| `PP13_SEL_ALLSTAR_PLAYER_3` | 3 |
| `PP13_SEL_ALLSTAR_PLAYER_4` | 4 |
| `PP13_SEL_ALLSTAR_PLAYER_5` | 5 |
| `PP13_SEL_ALLSTAR_PLAYER_6` | 6 |
| `PP13_SEL_ALLSTAR_PLAYER_7` | 7 |
| `PP13_SEL_ALLSTAR_PLAYER_8` | 8 |
| `PP13_SEL_ALLSTAR_PLAYER_9` | 9 |
| `PP13_SEL_QUALPRED_WEST_0` | 10 |
| `PP13_SEL_QUALPRED_WEST_1` | 11 |
| `PP13_SEL_QUALPRED_WEST_2` | 12 |
| `PP13_SEL_QUALPRED_WEST_3` | 13 |
| `PP13_SEL_QUALPRED_WEST_4` | 14 |
| `PP13_SEL_QUALPRED_WEST_5` | 15 |
| `PP13_SEL_QUALPRED_WEST_6` | 16 |
| `PP13_SEL_QUALPRED_WEST_7` | 17 |
| `PP13_SEL_QUALPRED_WEST_8` | 18 |
| `PP13_SEL_QUALPRED_WEST_9` | 19 |
| `PP13_SEL_QUALPRED_WEST_10` | 20 |
| `PP13_SEL_QUALPRED_WEST_11` | 21 |
| `PP13_SEL_QUALPRED_WEST_12` | 22 |
| `PP13_SEL_QUALPRED_WEST_13` | 23 |
| `PP13_SEL_QUALPRED_WEST_14` | 24 |
| `PP13_SEL_QUALPRED_EAST_0` | 25 |
| `PP13_SEL_QUALPRED_EAST_1` | 26 |
| `PP13_SEL_QUALPRED_EAST_2` | 27 |
| `PP13_SEL_QUALPRED_EAST_3` | 28 |
| `PP13_SEL_QUALPRED_EAST_4` | 29 |
| `PP13_SEL_QUALPRED_EAST_5` | 30 |
| `PP13_SEL_QUALPRED_EAST_6` | 31 |
| `PP13_SEL_QUALPRED_EAST_7` | 32 |
| `PP13_SEL_QUALPRED_EAST_8` | 33 |
| `PP13_SEL_QUALPRED_EAST_9` | 34 |
| `PP13_SEL_QUALPRED_EAST_10` | 35 |
| `PP13_SEL_QUALPRED_EAST_11` | 36 |
| `PP13_SEL_QUALPRED_EAST_12` | 37 |
| `PP13_SEL_QUALPRED_EAST_13` | 38 |
| `PP13_SEL_QUALPRED_EAST_14` | 39 |
| `PP13_SEL_TEAMCUP_TEAM` | 40 |
| `PP13_SEL_TEAMCUP_PLAYER` | 41 |
| `PP13_SEL_TEAMCUP_TEAM_LOCK` | 42 |
| `PP13_SEL_TEAMCUP_PLAYER_LOCK` | 43 |
| `PP13_SEL_EVENTPRED_0` | 44 |
| `PP13_SEL_EVENTPRED_1` | 45 |
| `PP13_SEL_EVENTPRED_2` | 46 |
| `PP13_SEL_EVENTPRED_3` | 47 |
| `PP13_SEL_EVENTPRED_4` | 48 |
| `PP13_SEL_EVENTPRED_5` | 49 |
| `PP13_SEL_EVENTPRED_6` | 50 |
| `PP13_SEL_EVENTPRED_7` | 51 |
| `PP13_SEL_EVENTPRED_8` | 52 |
| `PP13_SEL_EVENTPRED_9` | 53 |
| `PP13_SEL_EVENTPRED_10` | 54 |
| `PP13_SEL_EVENTPRED_11` | 55 |
| `PP13_SEL_EVENTPRED_12` | 56 |
| `PP13_SEL_EVENTPRED_13` | 57 |
| `PP13_SEL_EVENTPRED_14` | 58 |
| `PP13_SEL_EVENTPRED_15` | 59 |
| `PP13_SEL_EVENTPRED_16` | 60 |
| `PP13_SEL_EVENTPRED_17` | 61 |
| `PP13_SEL_EVENTPRED_18` | 62 |
| `PP13_SEL_EVENTPRED_19` | 63 |
| `PP13_SEL_EVENTPRED_20` | 64 |
| `PP13_SEL_EVENTPRED_21` | 65 |
| `PP13_SEL_EVENTPRED_22` | 66 |
| `PP13_SEL_EVENTPRED_23` | 67 |
| `PP13_SEL_EVENTPRED_24` | 68 |
| `PP13_SEL_EVENTPRED_25` | 69 |
| `PP13_SEL_EVENTPRED_26` | 70 |
| `PP13_SEL_EVENTPRED_27` | 71 |
| `PP13_SEL_EVENTPRED_28` | 72 |
| `PP13_SEL_EVENTPRED_29` | 73 |
| `PP13_SEL_EVENTPRED_30` | 74 |
| `PP13_SEL_EVENTPRED_31` | 75 |
| `PP13_SEL_EVENTPRED_32` | 76 |
| `PP13_SEL_EVENTPRED_33` | 77 |
| `PP13_SEL_EVENTPRED_34` | 78 |
| `PP13_SEL_EVENTPRED_35` | 79 |
| `PP13_SEL_EVENTPRED_36` | 80 |
| `PP13_SEL_EVENTPRED_37` | 81 |
| `PP13_SEL_EVENTPRED_38` | 82 |
| `PP13_SEL_EVENTPRED_39` | 83 |
| `PP13_SEL_EVENTPRED_40` | 84 |
| `PP13_SEL_EVENTPRED_41` | 85 |
| `PP13_SEL_EVENTPRED_42` | 86 |
| `PP13_SEL_EVENTPRED_43` | 87 |
| `PP13_SEL_SOLO_0` | 88 |
| `PP13_SEL_SOLO_1` | 89 |
| `PP13_SEL_SOLO_2` | 90 |
| `PP13_SEL_SOLO_3` | 91 |
| `PP13_SEL_SOLO_4` | 92 |
| `PP13_SEL_SOLO_5` | 93 |
| `PP13_SEL_SOLO_6` | 94 |
| `PP13_SEL_SOLO_7` | 95 |

</details>

<details>
<summary><code>CMsgClientToGCGetPlayerCardRosterResponse.Result</code> — values: 4</summary>

- Parent: `CMsgClientToGCGetPlayerCardRosterResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `ERROR_UNSPECIFIED` | 1 |
| `ERROR_INVALID_LEAGUE_ID` | 2 |
| `ERROR_INVALID_TIMESTAMP` | 3 |

</details>

<details>
<summary><code>CMsgClientToGCBatchGetPlayerCardRosterResponse.Result</code> — values: 4</summary>

- Parent: `CMsgClientToGCBatchGetPlayerCardRosterResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `ERROR_UNSPECIFIED` | 1 |
| `ERROR_INVALID_LEAGUE_ID` | 2 |
| `ERROR_INVALID_TIMESTAMP` | 3 |

</details>

<details>
<summary><code>CMsgClientToGCSetPlayerCardRosterResponse.Result</code> — values: 11</summary>

- Parent: `CMsgClientToGCSetPlayerCardRosterResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `ERROR_UNSPECIFIED` | 1 |
| `ERROR_INVALID_LEAGUE_ID` | 2 |
| `ERROR_INVALID_TIMESTAMP` | 3 |
| `ERROR_PLAYER_CARD_NOT_OWNED` | 4 |
| `ERROR_INVALID_SLOT` | 5 |
| `ERROR_FAILED_CARD_INFO` | 6 |
| `ERROR_ACCOUNT_DUPLICATE` | 7 |
| `ERROR_LOCKED_TIMESTAMP` | 8 |
| `ERROR_INVALID_LEAGUE_FOR_PERIOD` | 9 |
| `ERROR_INVALID_EVENT` | 10 |

</details>

<details>
<summary><code>CMsgDOTAFantasyDPCLeagueStatus.ERosterStatus</code> — values: 4</summary>

- Parent: `CMsgDOTAFantasyDPCLeagueStatus`

| Name | Number |
|---|---:|
| `UNSET` | 0 |
| `PARTIAL` | 1 |
| `FULL` | 2 |
| `CONCLUDED` | 3 |

</details>

<details>
<summary><code>CMsgDOTADPCSearchResults.ESearchResultsDesired</code> — values: 4</summary>

- Parent: `CMsgDOTADPCSearchResults`

| Name | Number |
|---|---:|
| `k_ESearchResultsDesired_Players` | 1 |
| `k_ESearchResultsDesired_Teams` | 2 |
| `k_ESearchResultsDesired_Leagues` | 4 |
| `k_ESearchResultsDesired_All` | 7 |

</details>

<details>
<summary><code>CMsgClientToGCFantasyCraftingGetDataResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCFantasyCraftingGetDataResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidLeague` | 5 |

</details>

<details>
<summary><code>CMsgClientToGCFantasyCraftingPerformOperationResponse.EResponse</code> — values: 8</summary>

- Parent: `CMsgClientToGCFantasyCraftingPerformOperationResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidLeague` | 5 |
| `k_eNoTokens` | 6 |
| `k_eMoreInfo` | 7 |

</details>

<details>
<summary><code>CMsgClientToGCFantasyCraftingDevModifyTabletResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCFantasyCraftingDevModifyTabletResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidLeague` | 5 |

</details>

<details>
<summary><code>CMsgClientToGCFantasyCraftingSelectPlayerResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCFantasyCraftingSelectPlayerResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidLeague` | 5 |
| `k_eInvalidPlayer` | 6 |

</details>

<details>
<summary><code>CMsgClientToGCFantasyCraftingGenerateTabletsResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCFantasyCraftingGenerateTabletsResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidLeague` | 5 |
| `k_eInvalidPlayer` | 6 |

</details>

<details>
<summary><code>CMsgClientToGcFantasyCraftingUpgradeTabletsResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGcFantasyCraftingUpgradeTabletsResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidLeague` | 5 |

</details>

<details>
<summary><code>CMsgClientToGCFantasyCraftingRerollOptionsResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCFantasyCraftingRerollOptionsResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidLeague` | 5 |
| `k_eInsufficientTokens` | 6 |

</details>
