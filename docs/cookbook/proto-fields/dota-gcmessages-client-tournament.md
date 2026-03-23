# dota_gcmessages_client_tournament.proto

- Module: `dota_gcmessages_client_tournament_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **1**
- Messages: **20** (top-level: 11)
- Enums: **1** (top-level: 1)

## Imports

- `dota_client_enums.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgRequestWeekendTourneySchedule</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgWeekendTourneySchedule</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `divisions` | `.CMsgWeekendTourneySchedule.Division` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgWeekendTourneySchedule.Division</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgWeekendTourneySchedule`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `division_code` | `uint32` | `optional` | `` |  |
| 2 | `time_window_open` | `uint32` | `optional` | `` |  |
| 3 | `time_window_close` | `uint32` | `optional` | `` |  |
| 4 | `time_window_open_next` | `uint32` | `optional` | `` |  |
| 5 | `trophy_id` | `uint32` | `optional` | `` |  |
| 6 | `free_weekend` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgWeekendTourneyOpts</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `participating` | `bool` | `optional` | `` |  |
| 2 | `division_id` | `uint32` | `optional` | `` |  |
| 3 | `buyin` | `uint32` | `optional` | `` |  |
| 4 | `skill_level` | `uint32` | `optional` | `` |  |
| 5 | `match_groups` | `uint32` | `optional` | `` |  |
| 6 | `team_id` | `uint32` | `optional` | `` |  |
| 7 | `pickup_team_name` | `string` | `optional` | `` |  |
| 8 | `pickup_team_logo` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgWeekendTourneyLeave</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgDOTATournament</code> — fields: 11; oneofs: 0; nested messages: 3; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `tournament_id` | `uint32` | `optional` | `` |  |
| 2 | `division_id` | `uint32` | `optional` | `` |  |
| 3 | `schedule_time` | `uint32` | `optional` | `` |  |
| 4 | `skill_level` | `uint32` | `optional` | `` |  |
| 5 | `tournament_template` | `.ETournamentTemplate` | `optional` | `` | default = k_ETournamentTemplate_None |
| 6 | `state` | `.ETournamentState` | `optional` | `` | default = k_ETournamentState_Unknown |
| 7 | `teams` | `.CMsgDOTATournament.Team` | `repeated` | `` |  |
| 8 | `games` | `.CMsgDOTATournament.Game` | `repeated` | `` |  |
| 9 | `nodes` | `.CMsgDOTATournament.Node` | `repeated` | `` |  |
| 10 | `state_seq_num` | `uint32` | `optional` | `` |  |
| 11 | `season_trophy_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTATournament.Team</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTATournament`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team_gid` | `fixed64` | `optional` | `` |  |
| 2 | `node_or_state` | `uint32` | `optional` | `` |  |
| 3 | `players` | `uint32` | `repeated` | `` | packed = true |
| 4 | `team_id` | `uint32` | `optional` | `` |  |
| 5 | `team_name` | `string` | `optional` | `` |  |
| 7 | `team_base_logo` | `uint64` | `optional` | `` |  |
| 8 | `team_ui_logo` | `uint64` | `optional` | `` |  |
| 9 | `player_buyin` | `uint32` | `repeated` | `` | packed = true |
| 10 | `player_skill_level` | `uint32` | `repeated` | `` | packed = true |
| 12 | `match_group_mask` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTATournament.Game</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTATournament`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `node_idx` | `uint32` | `optional` | `` |  |
| 2 | `lobby_id` | `fixed64` | `optional` | `` |  |
| 3 | `match_id` | `uint64` | `optional` | `` |  |
| 4 | `team_a_good` | `bool` | `optional` | `` |  |
| 5 | `state` | `.ETournamentGameState` | `optional` | `` | default = k_ETournamentGameState_Unknown |
| 6 | `start_time` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTATournament.Node</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTATournament`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `node_id` | `uint32` | `optional` | `` |  |
| 2 | `team_idx_a` | `uint32` | `optional` | `` |  |
| 3 | `team_idx_b` | `uint32` | `optional` | `` |  |
| 4 | `node_state` | `.ETournamentNodeState` | `optional` | `` | default = k_ETournamentNodeState_Unknown |

</details>

<details>
<summary><code>CMsgDOTATournamentStateChange</code> — fields: 7; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `new_tournament_id` | `uint32` | `optional` | `` |  |
| 2 | `event` | `.ETournamentEvent` | `optional` | `` | default = k_ETournamentEvent_None |
| 3 | `new_tournament_state` | `.ETournamentState` | `optional` | `` | default = k_ETournamentState_Unknown |
| 4 | `game_changes` | `.CMsgDOTATournamentStateChange.GameChange` | `repeated` | `` |  |
| 5 | `team_changes` | `.CMsgDOTATournamentStateChange.TeamChange` | `repeated` | `` |  |
| 6 | `merged_tournament_ids` | `uint32` | `repeated` | `` | packed = true |
| 7 | `state_seq_num` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTATournamentStateChange.GameChange</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTATournamentStateChange`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `new_state` | `.ETournamentGameState` | `optional` | `` | default = k_ETournamentGameState_Unknown |

</details>

<details>
<summary><code>CMsgDOTATournamentStateChange.TeamChange</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTATournamentStateChange`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team_gid` | `uint64` | `optional` | `` |  |
| 2 | `new_node_or_state` | `uint32` | `optional` | `` |  |
| 3 | `old_node_or_state` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAWeekendTourneyPlayerSkillLevelStats</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `skill_level` | `uint32` | `optional` | `` |  |
| 2 | `times_won_0` | `uint32` | `optional` | `` |  |
| 3 | `times_won_1` | `uint32` | `optional` | `` |  |
| 4 | `times_won_2` | `uint32` | `optional` | `` |  |
| 5 | `times_won_3` | `uint32` | `optional` | `` |  |
| 6 | `times_bye_and_lost` | `uint32` | `optional` | `` |  |
| 7 | `times_bye_and_won` | `uint32` | `optional` | `` |  |
| 8 | `total_games_won` | `uint32` | `optional` | `` |  |
| 9 | `score` | `uint32` | `optional` | `` |  |
| 10 | `times_unusual_champ` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAWeekendTourneyPlayerStats</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `season_trophy_id` | `uint32` | `optional` | `` |  |
| 3 | `skill_levels` | `.CMsgDOTAWeekendTourneyPlayerSkillLevelStats` | `repeated` | `` |  |
| 4 | `current_tier` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAWeekendTourneyPlayerStatsRequest</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `season_trophy_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAWeekendTourneyPlayerHistory</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 3 | `tournaments` | `.CMsgDOTAWeekendTourneyPlayerHistory.Tournament` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAWeekendTourneyPlayerHistory.Tournament</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAWeekendTourneyPlayerHistory`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `tournament_id` | `uint32` | `optional` | `` |  |
| 2 | `start_time` | `uint32` | `optional` | `` |  |
| 3 | `tournament_tier` | `uint32` | `optional` | `` |  |
| 4 | `team_id` | `uint32` | `optional` | `` |  |
| 5 | `team_date` | `uint32` | `optional` | `` |  |
| 6 | `team_result` | `uint32` | `optional` | `` |  |
| 7 | `account_id` | `uint32` | `repeated` | `` |  |
| 8 | `team_name` | `string` | `optional` | `` |  |
| 9 | `season_trophy_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAWeekendTourneyParticipationDetails</code> — fields: 1; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `divisions` | `.CMsgDOTAWeekendTourneyParticipationDetails.Division` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAWeekendTourneyParticipationDetails.Tier</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAWeekendTourneyParticipationDetails`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `tier` | `uint32` | `optional` | `` |  |
| 2 | `players` | `uint32` | `optional` | `` |  |
| 3 | `teams` | `uint32` | `optional` | `` |  |
| 4 | `winning_teams` | `uint32` | `optional` | `` |  |
| 5 | `players_streak_2` | `uint32` | `optional` | `` |  |
| 6 | `players_streak_3` | `uint32` | `optional` | `` |  |
| 7 | `players_streak_4` | `uint32` | `optional` | `` |  |
| 8 | `players_streak_5` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAWeekendTourneyParticipationDetails.Division</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAWeekendTourneyParticipationDetails`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `division_id` | `uint32` | `optional` | `` |  |
| 2 | `schedule_time` | `uint32` | `optional` | `` |  |
| 3 | `tiers` | `.CMsgDOTAWeekendTourneyParticipationDetails.Tier` | `repeated` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>ETournamentEvent</code> — values: 12</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_ETournamentEvent_None` | 0 |
| `k_ETournamentEvent_TournamentCreated` | 1 |
| `k_ETournamentEvent_TournamentsMerged` | 2 |
| `k_ETournamentEvent_GameOutcome` | 3 |
| `k_ETournamentEvent_TeamGivenBye` | 4 |
| `k_ETournamentEvent_TournamentCanceledByAdmin` | 5 |
| `k_ETournamentEvent_TeamAbandoned` | 6 |
| `k_ETournamentEvent_ScheduledGameStarted` | 7 |
| `k_ETournamentEvent_Canceled` | 8 |
| `k_ETournamentEvent_TeamParticipationTimedOut_EntryFeeRefund` | 9 |
| `k_ETournamentEvent_TeamParticipationTimedOut_EntryFeeForfeit` | 10 |
| `k_ETournamentEvent_TeamParticipationTimedOut_GrantedVictory` | 11 |

</details>
