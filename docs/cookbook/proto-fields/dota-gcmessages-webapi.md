# dota_gcmessages_webapi.proto

- Module: `dota_gcmessages_webapi_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **5**
- Messages: **38** (top-level: 19)
- Enums: **14** (top-level: 6)

## Imports

- `steammessages.proto`
- `gcsdk_gcmessages.proto`
- `dota_shared_enums.proto`
- `dota_gcmessages_common.proto`
- `dota_match_metadata.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgArcanaVotes</code> — fields: 8; oneofs: 0; nested messages: 1; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `matches` | `.CMsgArcanaVotes.Match` | `repeated` | `` |  |
| 2 | `round_time_remaining` | `uint32` | `optional` | `` |  |
| 3 | `round_number` | `uint32` | `optional` | `` |  |
| 4 | `voting_state` | `uint32` | `optional` | `` |  |
| 5 | `is_current_round_calibrating` | `bool` | `optional` | `` |  |
| 6 | `closest_active_match_id` | `uint32` | `optional` | `` |  |
| 7 | `event_id` | `uint32` | `optional` | `` |  |
| 8 | `voting_start_time` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgArcanaVotes.Match</code> — fields: 11; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgArcanaVotes`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint32` | `optional` | `` |  |
| 2 | `hero_id_0` | `int32` | `optional` | `` |  |
| 3 | `hero_id_1` | `int32` | `optional` | `` |  |
| 4 | `hero_seeding_0` | `uint32` | `optional` | `` |  |
| 5 | `hero_seeding_1` | `uint32` | `optional` | `` |  |
| 6 | `vote_count_0` | `uint32` | `optional` | `` |  |
| 7 | `vote_count_1` | `uint32` | `optional` | `` |  |
| 8 | `voting_state` | `uint32` | `optional` | `` |  |
| 9 | `round_number` | `uint32` | `optional` | `` |  |
| 10 | `is_votes_hidden` | `bool` | `optional` | `` |  |
| 11 | `calibration_time_remaining` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTADPCFeed</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `elements` | `.CMsgDOTADPCFeed.Element` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTADPCFeed.Element</code> — fields: 13; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTADPCFeed`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `type` | `.CMsgDOTADPCFeed.EFeedElementType` | `optional` | `` | default = FEED_SERIES_RESULT |
| 2 | `timestamp` | `uint32` | `optional` | `` |  |
| 3 | `series_id` | `uint32` | `optional` | `` |  |
| 4 | `match_id` | `uint64` | `optional` | `` |  |
| 5 | `team_id` | `uint32` | `optional` | `` |  |
| 6 | `account_id` | `uint32` | `optional` | `` |  |
| 7 | `league_id` | `uint32` | `optional` | `` |  |
| 8 | `node_id` | `uint32` | `optional` | `` |  |
| 9 | `data_1` | `uint32` | `optional` | `` |  |
| 10 | `data_2` | `uint32` | `optional` | `` |  |
| 11 | `data_3` | `uint32` | `optional` | `` |  |
| 12 | `data_4` | `uint32` | `optional` | `` |  |
| 13 | `server_steam_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTADPCUserInfo</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `is_plus_subscriber` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDraftTrivia</code> — fields: 8; oneofs: 0; nested messages: 3; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `has_valid_match` | `bool` | `optional` | `` |  |
| 2 | `match_hero_info` | `.CMsgDraftTrivia.DraftTriviaMatchInfo` | `optional` | `` |  |
| 3 | `match_rank_tier` | `uint32` | `optional` | `` |  |
| 4 | `end_time` | `uint32` | `optional` | `` |  |
| 5 | `event_id` | `uint32` | `optional` | `` |  |
| 6 | `current_match_voted_radiant` | `bool` | `optional` | `` |  |
| 7 | `previous_result` | `.CMsgDraftTrivia.PreviousResult` | `optional` | `` |  |
| 8 | `current_streak` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDraftTrivia.DraftTriviaHeroInfo</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDraftTrivia`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `role` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDraftTrivia.DraftTriviaMatchInfo</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDraftTrivia`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `radiant_heroes` | `.CMsgDraftTrivia.DraftTriviaHeroInfo` | `repeated` | `` |  |
| 2 | `dire_heroes` | `.CMsgDraftTrivia.DraftTriviaHeroInfo` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDraftTrivia.PreviousResult</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDraftTrivia`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `voted_correctly` | `bool` | `optional` | `` |  |
| 2 | `voted_radiant` | `bool` | `optional` | `` |  |
| 3 | `match_hero_info` | `.CMsgDraftTrivia.DraftTriviaMatchInfo` | `optional` | `` |  |
| 4 | `match_rank_tier` | `uint32` | `optional` | `` |  |
| 5 | `end_time` | `uint32` | `optional` | `` |  |
| 6 | `match_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTeamFanContentAssetStatus</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `asset_type` | `.ETeamFanContentAssetType` | `optional` | `` | default = k_eFanContentAssetType_LogoPNG |
| 2 | `asset_index` | `uint32` | `optional` | `` |  |
| 3 | `asset_status` | `.ETeamFanContentAssetStatus` | `optional` | `` | default = k_eFanContentAssetStatus_None |
| 4 | `crc` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTeamFanContentAssetStatusResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgTeamFanContentAssetStatusResponse.EResult` | `optional` | `` | default = k_eSuccess |

</details>

<details>
<summary><code>CMsgTeamFanContentStatus</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team_status_list` | `.CMsgTeamFanContentStatus.TeamStatus` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgTeamFanContentStatus.TeamStatus</code> — fields: 18; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgTeamFanContentStatus`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `team_id` | `uint32` | `optional` | `` |  |
| 3 | `logo_url` | `string` | `optional` | `` |  |
| 4 | `status` | `.ETeamFanContentStatus` | `optional` | `` | default = TEAM_FAN_CONTENT_STATUS_INVALID |
| 5 | `timestamp` | `uint32` | `optional` | `` |  |
| 7 | `ugc_logo` | `uint64` | `optional` | `` |  |
| 8 | `workshop_account_id` | `uint32` | `optional` | `` |  |
| 9 | `abbreviation` | `string` | `optional` | `` |  |
| 10 | `voiceline_count` | `uint32` | `optional` | `` |  |
| 11 | `spray_count` | `uint32` | `optional` | `` |  |
| 12 | `emoticon_count` | `uint32` | `optional` | `` |  |
| 13 | `wallpaper_count` | `uint32` | `optional` | `` |  |
| 14 | `comment` | `string` | `optional` | `` |  |
| 15 | `comment_timestamp` | `uint32` | `optional` | `` |  |
| 16 | `asset_status` | `.CMsgTeamFanContentAssetStatus` | `repeated` | `` |  |
| 17 | `email_timestamp` | `uint32` | `optional` | `` |  |
| 18 | `email_tier` | `uint32` | `optional` | `` |  |
| 19 | `languages` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTeamFanContentAutographStatus</code> — fields: 1; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team_autographs` | `.CMsgTeamFanContentAutographStatus.TeamStatus` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgTeamFanContentAutographStatus.AutographStatus</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgTeamFanContentAutographStatus`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `pro_name` | `string` | `optional` | `` |  |
| 2 | `account_id` | `uint32` | `optional` | `` |  |
| 3 | `timestamp` | `uint32` | `optional` | `` |  |
| 4 | `file` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTeamFanContentAutographStatus.TeamStatus</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgTeamFanContentAutographStatus`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `team_id` | `uint32` | `optional` | `` |  |
| 3 | `autographs` | `.CMsgTeamFanContentAutographStatus.AutographStatus` | `repeated` | `` |  |
| 4 | `workshop_account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTalentContentAssetStatus</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `asset_type` | `.ETalentContentAssetType` | `optional` | `` | default = k_eTalentContentAssetType_Photo |
| 2 | `asset_index` | `uint32` | `optional` | `` |  |
| 3 | `asset_status` | `.ETalentContentAssetStatus` | `optional` | `` | default = k_eTalentContentAssetStatus_None |

</details>

<details>
<summary><code>CMsgTalentContentStatus</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `talent_status` | `.CMsgTalentContentStatus.TalentDetails` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgTalentContentStatus.TalentDetails</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgTalentContentStatus`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `full_name` | `string` | `optional` | `` |  |
| 3 | `nickname` | `string` | `optional` | `` |  |
| 4 | `workshop_item_id` | `uint32` | `optional` | `` |  |
| 5 | `zip_file` | `string` | `optional` | `` |  |
| 6 | `status` | `.ETalentContentStatus` | `optional` | `` | default = TALENT_CONTENT_STATUS_INVALID |
| 7 | `asset_status` | `.CMsgTalentContentAssetStatus` | `repeated` | `` |  |
| 8 | `broadcast_language` | `uint32` | `optional` | `` |  |
| 9 | `submission_timestamp` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSetTalentContentResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgSetTalentContentResponse.EResult` | `optional` | `` | default = k_eSuccess |

</details>

<details>
<summary><code>CMsgDPCEvent</code> — fields: 15; oneofs: 0; nested messages: 2; nested enums: 4</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event` | `.CMsgDPCEvent.ELeagueEvent` | `optional` | `` | default = EVENT_INVALID |
| 2 | `event_type` | `.CMsgDPCEvent.ELeagueEventType` | `optional` | `` | default = UNKNOWN |
| 3 | `leagues` | `.CMsgDPCEvent.League` | `repeated` | `` |  |
| 4 | `registration_period` | `uint32` | `optional` | `` |  |
| 5 | `is_event_upcoming` | `bool` | `optional` | `` |  |
| 6 | `is_event_completed` | `bool` | `optional` | `` |  |
| 7 | `event_name` | `string` | `optional` | `` |  |
| 8 | `multicast_league_id` | `uint32` | `optional` | `` |  |
| 9 | `multicast_streams` | `uint32` | `repeated` | `` |  |
| 10 | `tour` | `.CMsgDPCEvent.ETour` | `optional` | `` | default = TOUR_NONE |
| 12 | `timestamp_drop_lock` | `uint32` | `optional` | `` |  |
| 13 | `timestamp_add_lock` | `uint32` | `optional` | `` |  |
| 14 | `timestamp_content_deadline` | `uint32` | `optional` | `` |  |
| 15 | `is_fantasy_enabled` | `bool` | `optional` | `` |  |
| 16 | `timestamp_content_review_deadline` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDPCEvent.PhaseInfo</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDPCEvent`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `phase` | `.CMsgDPCEvent.ELeagueEventPhase` | `optional` | `` | default = PHASE_INVALID |
| 2 | `node_group_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDPCEvent.League</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDPCEvent`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `region` | `.ELeagueRegion` | `optional` | `` | default = LEAGUE_REGION_UNSET |
| 2 | `division` | `.ELeagueDivision` | `optional` | `` | default = LEAGUE_DIVISION_UNSET |
| 3 | `league_id` | `uint32` | `optional` | `` |  |
| 4 | `phases` | `.CMsgDPCEvent.PhaseInfo` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDPCEventList</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `events` | `.CMsgDPCEvent` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAFantasyCardLineup</code> — fields: 1; oneofs: 0; nested messages: 4; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `periods` | `.CMsgDOTAFantasyCardLineup.Period` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAFantasyCardLineup.CardBonus</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAFantasyCardLineup`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `bonus_stat` | `uint32` | `optional` | `` |  |
| 2 | `bonus_value` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAFantasyCardLineup.Card</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAFantasyCardLineup`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_account_id` | `uint32` | `optional` | `` |  |
| 2 | `player_name` | `string` | `optional` | `` |  |
| 3 | `team_id` | `uint32` | `optional` | `` |  |
| 4 | `team_name` | `string` | `optional` | `` |  |
| 5 | `role` | `uint32` | `optional` | `` |  |
| 6 | `bonuses` | `.CMsgDOTAFantasyCardLineup.CardBonus` | `repeated` | `` |  |
| 7 | `score` | `float` | `optional` | `` |  |
| 8 | `finalized` | `bool` | `optional` | `` |  |
| 9 | `item_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAFantasyCardLineup.League</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAFantasyCardLineup`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_id` | `uint32` | `optional` | `` |  |
| 2 | `cards` | `.CMsgDOTAFantasyCardLineup.Card` | `repeated` | `` |  |
| 3 | `score` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAFantasyCardLineup.Period</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAFantasyCardLineup`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `fantasy_period` | `uint32` | `optional` | `` | default = 4294967295 |
| 2 | `timestamp_start` | `uint32` | `optional` | `` |  |
| 3 | `timestamp_end` | `uint32` | `optional` | `` |  |
| 4 | `leagues` | `.CMsgDOTAFantasyCardLineup.League` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAFantasyCardList</code> — fields: 1; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `cards` | `.CMsgDOTAFantasyCardList.Card` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAFantasyCardList.CardBonus</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAFantasyCardList`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `bonus_stat` | `uint32` | `optional` | `` |  |
| 2 | `bonus_value` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAFantasyCardList.Card</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAFantasyCardList`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_account_id` | `uint32` | `optional` | `` |  |
| 2 | `player_name` | `string` | `optional` | `` |  |
| 3 | `team_id` | `uint32` | `optional` | `` |  |
| 4 | `team_name` | `string` | `optional` | `` |  |
| 5 | `role` | `uint32` | `optional` | `` |  |
| 6 | `bonuses` | `.CMsgDOTAFantasyCardList.CardBonus` | `repeated` | `` |  |
| 8 | `item_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgChatToxicityToxicPlayerMatchesReport</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `rows` | `.CMsgChatToxicityToxicPlayerMatchesReport.IndividualRow` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgChatToxicityToxicPlayerMatchesReport.IndividualRow</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgChatToxicityToxicPlayerMatchesReport`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_account_id` | `uint32` | `optional` | `` |  |
| 2 | `num_matches_seen` | `uint32` | `optional` | `` |  |
| 3 | `num_messages` | `uint32` | `optional` | `` |  |
| 4 | `num_messages_toxic` | `uint32` | `optional` | `` |  |
| 5 | `first_match_seen` | `uint64` | `optional` | `` |  |
| 6 | `last_match_seen` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgChatToxicityReport</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `num_matches_seen` | `uint32` | `optional` | `` |  |
| 2 | `num_messages` | `uint32` | `optional` | `` |  |
| 4 | `num_messages_ml_thinks_toxic` | `uint32` | `optional` | `` |  |
| 5 | `status` | `string` | `optional` | `` |  |
| 6 | `result` | `uint32` | `optional` | `` |  |
| 7 | `message` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGetTeamAuditInformation</code> — fields: 4; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team_id` | `uint32` | `optional` | `` |  |
| 2 | `team_name` | `string` | `optional` | `` |  |
| 3 | `actions` | `.CMsgGetTeamAuditInformation.Action` | `repeated` | `` |  |
| 4 | `last_updated` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGetTeamAuditInformation.Action</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGetTeamAuditInformation`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `registration_period` | `uint32` | `optional` | `` |  |
| 2 | `account_id` | `uint32` | `optional` | `` |  |
| 3 | `action` | `uint32` | `optional` | `` |  |
| 4 | `timestamp` | `uint32` | `optional` | `` |  |
| 5 | `player_name` | `string` | `optional` | `` |  |
| 6 | `player_real_name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTADPCMatch</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match` | `.CMsgDOTAMatch` | `optional` | `` |  |
| 2 | `metadata` | `.CDOTAMatchMetadata` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>ETeamFanContentStatus</code> — values: 3</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `TEAM_FAN_CONTENT_STATUS_INVALID` | 0 |
| `TEAM_FAN_CONTENT_STATUS_PENDING` | 1 |
| `TEAM_FAN_CONTENT_STATUS_EVALUATED` | 2 |

</details>

<details>
<summary><code>ETeamFanContentAssetType</code> — values: 11</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eFanContentAssetType_LogoPNG` | 1 |
| `k_eFanContentAssetType_LogoSVG` | 2 |
| `k_eFanContentAssetType_Logo3D` | 3 |
| `k_eFanContentAssetType_Players` | 4 |
| `k_eFanContentAssetType_Sprays` | 5 |
| `k_eFanContentAssetType_Wallpapers` | 6 |
| `k_eFanContentAssetType_Emoticons` | 7 |
| `k_eFanContentAssetType_VoiceLines` | 8 |
| `k_eFanContentAssetType_Localization` | 9 |
| `k_eFanContentAssetType_Banner` | 10 |
| `k_eFanContentAssetType_BaseLogo` | 11 |

</details>

<details>
<summary><code>ETeamFanContentAssetStatus</code> — values: 3</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eFanContentAssetStatus_None` | 0 |
| `k_eFanContentAssetStatus_Approved` | 1 |
| `k_eFanContentAssetStatus_Rejected` | 2 |

</details>

<details>
<summary><code>ETalentContentStatus</code> — values: 5</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `TALENT_CONTENT_STATUS_INVALID` | 0 |
| `TALENT_CONTENT_STATUS_PENDING` | 1 |
| `TALENT_CONTENT_STATUS_EVALUATED` | 2 |
| `TALENT_CONTENT_STATUS_REJECTED` | 3 |
| `TALENT_CONTENT_STATUS_APPROVED` | 4 |

</details>

<details>
<summary><code>ETalentContentAssetType</code> — values: 3</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eTalentContentAssetType_Photo` | 1 |
| `k_eTalentContentAssetType_Autograph` | 2 |
| `k_eTalentContentAssetType_Voicelines` | 3 |

</details>

<details>
<summary><code>ETalentContentAssetStatus</code> — values: 3</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eTalentContentAssetStatus_None` | 0 |
| `k_eTalentContentAssetStatus_Approved` | 1 |
| `k_eTalentContentAssetStatus_Rejected` | 2 |

</details>

<details>
<summary><code>CMsgArcanaVotes.VotingState</code> — values: 3</summary>

- Parent: `CMsgArcanaVotes`

| Name | Number |
|---|---:|
| `FINISHED` | 0 |
| `IN_PROGRESS` | 1 |
| `IN_FUTURE` | 2 |

</details>

<details>
<summary><code>CMsgDOTADPCFeed.EFeedElementType</code> — values: 14</summary>

- Parent: `CMsgDOTADPCFeed`

| Name | Number |
|---|---:|
| `FEED_SERIES_RESULT` | 1 |
| `FEED_MATCH_POPULAR` | 2 |
| `FEED_TEAM_UPCOMING_MATCH` | 3 |
| `FEED_TEAM_LEAGUE_RESULT` | 4 |
| `FEED_TEAM_ADD_PLAYER` | 5 |
| `FEED_TEAM_REMOVE_PLAYER` | 6 |
| `FEED_TEAM_DISBAND` | 7 |
| `FEED_LEAGUE_UPCOMING` | 8 |
| `FEED_LEAGUE_CONCLUDED` | 9 |
| `FEED_DPC_STANDINGS` | 10 |
| `FEED_ALERT_PREDICTIONS` | 11 |
| `FEED_ALERT_FANTASY` | 12 |
| `FEED_LEAGUE_LIVE_MATCH` | 13 |
| `FEED_LEAGUE_INPROGRESS_SERIES` | 14 |

</details>

<details>
<summary><code>CMsgTeamFanContentAssetStatusResponse.EResult</code> — values: 2</summary>

- Parent: `CMsgTeamFanContentAssetStatusResponse`

| Name | Number |
|---|---:|
| `k_eSuccess` | 0 |
| `k_eInternalError` | 1 |

</details>

<details>
<summary><code>CMsgSetTalentContentResponse.EResult</code> — values: 3</summary>

- Parent: `CMsgSetTalentContentResponse`

| Name | Number |
|---|---:|
| `k_eSuccess` | 0 |
| `k_eInternalError` | 1 |
| `k_eOutOfDate` | 2 |

</details>

<details>
<summary><code>CMsgDPCEvent.ELeagueEvent</code> — values: 24</summary>

- Parent: `CMsgDPCEvent`

| Name | Number |
|---|---:|
| `EVENT_INVALID` | 0 |
| `SPRING_2021_LEAGUE` | 1 |
| `SPRING_2021_MAJOR` | 2 |
| `INTERNATIONAL_2021_QUALIFIERS` | 3 |
| `INTERNATIONAL_2021` | 4 |
| `WINTER_2021_LEAGUE` | 5 |
| `WINTER_2021_LEAGUE_FINALS` | 6 |
| `SPRING_2022_LEAGUE` | 7 |
| `SPRING_2022_MAJOR` | 8 |
| `SUMMER_2022_LEAGUE` | 9 |
| `SUMMER_2022_MAJOR` | 10 |
| `INTERNATIONAL_2022` | 11 |
| `CHINA_REGIONAL_FINALS` | 12 |
| `INTERNATIONAL_2022_REGIONAL_QUALIFIERS` | 13 |
| `INTERNATIONAL_2022_LAST_CHANCE_QUALIFIERS` | 14 |
| `WINTER_2023_LEAGUE` | 15 |
| `WINTER_2023_MAJOR` | 16 |
| `SPRING_2023_LEAGUE` | 17 |
| `SPRING_2023_MAJOR` | 18 |
| `SUMMER_2023_LEAGUE` | 19 |
| `SUMMER_2023_MAJOR` | 20 |
| `INTERNATIONAL_2023` | 21 |
| `INTERNATIONAL_2024` | 23 |
| `INTERNATIONAL_2025` | 24 |

</details>

<details>
<summary><code>CMsgDPCEvent.ELeagueEventPhase</code> — values: 12</summary>

- Parent: `CMsgDPCEvent`

| Name | Number |
|---|---:|
| `PHASE_INVALID` | 0 |
| `WILD_CARD` | 1 |
| `GROUP_STAGE` | 2 |
| `GROUP_A` | 3 |
| `GROUP_B` | 4 |
| `OVERALL` | 5 |
| `PLAYOFF` | 6 |
| `RESULTS` | 7 |
| `DPC_POINT_STANDINGS` | 8 |
| `GROUP_C` | 9 |
| `GROUP_D` | 10 |
| `PLACEMENT` | 11 |

</details>

<details>
<summary><code>CMsgDPCEvent.ELeagueEventType</code> — values: 7</summary>

- Parent: `CMsgDPCEvent`

| Name | Number |
|---|---:|
| `UNKNOWN` | 0 |
| `LEAGUE` | 1 |
| `MAJOR` | 2 |
| `INTERNATIONAL_QUALIFIERS` | 3 |
| `INTERNATIONAL` | 4 |
| `LEAGUE_FINALS` | 5 |
| `EXTERNAL` | 6 |

</details>

<details>
<summary><code>CMsgDPCEvent.ETour</code> — values: 4</summary>

- Parent: `CMsgDPCEvent`

| Name | Number |
|---|---:|
| `TOUR_NONE` | 0 |
| `TOUR_1` | 1 |
| `TOUR_2` | 2 |
| `TOUR_3` | 3 |

</details>
