# dota_gcmessages_common_league.proto

- Module: `dota_gcmessages_common_league_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **1**
- Messages: **37** (top-level: 17)
- Enums: **2** (top-level: 2)

## Imports

- `dota_shared_enums.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgDOTALeagueNode</code> — fields: 20; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `node_id` | `uint32` | `optional` | `` |  |
| 3 | `node_group_id` | `uint32` | `optional` | `` |  |
| 4 | `winning_node_id` | `uint32` | `optional` | `` |  |
| 5 | `losing_node_id` | `uint32` | `optional` | `` |  |
| 6 | `incoming_node_id_1` | `uint32` | `optional` | `` |  |
| 7 | `incoming_node_id_2` | `uint32` | `optional` | `` |  |
| 8 | `node_type` | `.ELeagueNodeType` | `optional` | `` | default = INVALID_NODE_TYPE |
| 9 | `scheduled_time` | `uint32` | `optional` | `` |  |
| 10 | `series_id` | `uint32` | `optional` | `` |  |
| 11 | `team_id_1` | `uint32` | `optional` | `` |  |
| 12 | `team_id_2` | `uint32` | `optional` | `` |  |
| 13 | `matches` | `.CMsgDOTALeagueNode.MatchDetails` | `repeated` | `` |  |
| 14 | `team_1_wins` | `uint32` | `optional` | `` |  |
| 15 | `team_2_wins` | `uint32` | `optional` | `` |  |
| 16 | `has_started` | `bool` | `optional` | `` |  |
| 17 | `is_completed` | `bool` | `optional` | `` |  |
| 18 | `stream_ids` | `uint32` | `repeated` | `` |  |
| 19 | `actual_time` | `uint32` | `optional` | `` |  |
| 20 | `vods` | `.CMsgDOTALeagueNode.VOD` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALeagueNode.MatchDetails</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTALeagueNode`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `winning_team_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALeagueNode.VOD</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTALeagueNode`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `series_game` | `uint32` | `optional` | `` |  |
| 2 | `stream_id` | `uint32` | `optional` | `` |  |
| 3 | `url` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALeagueNodeGroup</code> — fields: 27; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `node_group_id` | `uint32` | `optional` | `` |  |
| 3 | `parent_node_group_id` | `uint32` | `optional` | `` |  |
| 4 | `incoming_node_group_ids` | `uint32` | `repeated` | `` |  |
| 5 | `advancing_node_group_id` | `uint32` | `optional` | `` |  |
| 6 | `advancing_team_count` | `uint32` | `optional` | `` |  |
| 7 | `team_count` | `uint32` | `optional` | `` |  |
| 8 | `node_group_type` | `.ELeagueNodeGroupType` | `optional` | `` | default = INVALID_GROUP_TYPE |
| 9 | `default_node_type` | `.ELeagueNodeType` | `optional` | `` | default = INVALID_NODE_TYPE |
| 10 | `round` | `uint32` | `optional` | `` |  |
| 11 | `max_rounds` | `uint32` | `optional` | `` |  |
| 12 | `is_tiebreaker` | `bool` | `optional` | `` |  |
| 13 | `is_final_group` | `bool` | `optional` | `` |  |
| 14 | `is_completed` | `bool` | `optional` | `` |  |
| 15 | `team_standings` | `.CMsgDOTALeagueNodeGroup.TeamStanding` | `repeated` | `` |  |
| 16 | `nodes` | `.CMsgDOTALeagueNode` | `repeated` | `` |  |
| 17 | `node_groups` | `.CMsgDOTALeagueNodeGroup` | `repeated` | `` |  |
| 18 | `phase` | `.ELeaguePhase` | `optional` | `` | default = LEAGUE_PHASE_UNSET |
| 19 | `region` | `.ELeagueRegion` | `optional` | `` | default = LEAGUE_REGION_UNSET |
| 20 | `start_time` | `uint32` | `optional` | `` |  |
| 21 | `end_time` | `uint32` | `optional` | `` |  |
| 22 | `secondary_advancing_node_group_id` | `uint32` | `optional` | `` |  |
| 23 | `secondary_advancing_team_count` | `uint32` | `optional` | `` |  |
| 24 | `tertiary_advancing_node_group_id` | `uint32` | `optional` | `` |  |
| 25 | `tertiary_advancing_team_count` | `uint32` | `optional` | `` |  |
| 26 | `elimination_dpc_points` | `uint32` | `optional` | `` |  |
| 27 | `win_loss_limit` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALeagueNodeGroup.TeamStanding</code> — fields: 15; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTALeagueNodeGroup`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `standing` | `uint32` | `optional` | `` |  |
| 2 | `team_id` | `uint32` | `optional` | `` |  |
| 3 | `team_name` | `string` | `optional` | `` |  |
| 4 | `team_tag` | `string` | `optional` | `` |  |
| 5 | `team_logo` | `uint64` | `optional` | `` |  |
| 6 | `team_logo_url` | `string` | `optional` | `` |  |
| 7 | `wins` | `uint32` | `optional` | `` |  |
| 8 | `losses` | `uint32` | `optional` | `` |  |
| 9 | `score` | `int64` | `optional` | `` |  |
| 10 | `team_abbreviation` | `string` | `optional` | `` |  |
| 14 | `is_pro` | `bool` | `optional` | `` |  |
| 15 | `tiebreak_game_win_pct` | `uint32` | `optional` | `` |  |
| 16 | `tiebreak_opponent_match_wins` | `uint32` | `optional` | `` |  |
| 17 | `tiebreak_opponent_game_win_pct` | `uint32` | `optional` | `` |  |
| 18 | `tiebreak_coinflip` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALeague</code> — fields: 7; oneofs: 0; nested messages: 7; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `info` | `.CMsgDOTALeague.Info` | `optional` | `` |  |
| 2 | `prize_pool` | `.CMsgDOTALeague.PrizePool` | `optional` | `` |  |
| 3 | `admins` | `.CMsgDOTALeague.Admin` | `repeated` | `` |  |
| 4 | `streams` | `.CMsgDOTALeague.Stream` | `repeated` | `` |  |
| 5 | `node_groups` | `.CMsgDOTALeagueNodeGroup` | `repeated` | `` |  |
| 6 | `series_infos` | `.CMsgDOTALeague.SeriesInfo` | `repeated` | `` |  |
| 7 | `registered_players` | `.CMsgDOTALeague.Player` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALeague.Info</code> — fields: 14; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTALeague`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_id` | `uint32` | `optional` | `` |  |
| 2 | `name` | `string` | `optional` | `` |  |
| 3 | `tier` | `.ELeagueTier` | `optional` | `` | default = LEAGUE_TIER_UNSET |
| 4 | `region` | `.ELeagueRegion` | `optional` | `` | default = LEAGUE_REGION_UNSET |
| 5 | `url` | `string` | `optional` | `` |  |
| 6 | `description` | `string` | `optional` | `` |  |
| 7 | `notes` | `string` | `optional` | `` |  |
| 8 | `start_timestamp` | `uint32` | `optional` | `` |  |
| 9 | `end_timestamp` | `uint32` | `optional` | `` |  |
| 10 | `pro_circuit_points` | `uint32` | `optional` | `` |  |
| 11 | `image_bits` | `uint32` | `optional` | `` |  |
| 12 | `status` | `.ELeagueStatus` | `optional` | `` | default = LEAGUE_STATUS_UNSET |
| 13 | `most_recent_activity` | `uint32` | `optional` | `` |  |
| 14 | `registration_period` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALeague.Admin</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTALeague`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `is_primary` | `bool` | `optional` | `` |  |
| 3 | `email_address` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALeague.PrizePoolItem</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTALeague`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_def` | `uint32` | `optional` | `` |  |
| 2 | `sales_stop_timestamp` | `uint32` | `optional` | `` |  |
| 3 | `revenue_pct` | `uint32` | `optional` | `` |  |
| 4 | `revenue_cents_per_sale` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALeague.PrizePool</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTALeague`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `base_prize_pool` | `uint32` | `optional` | `` |  |
| 2 | `total_prize_pool` | `uint32` | `optional` | `` |  |
| 3 | `prize_split_pct_x100` | `uint32` | `repeated` | `` |  |
| 4 | `prize_pool_items` | `.CMsgDOTALeague.PrizePoolItem` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALeague.Stream</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTALeague`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `stream_id` | `uint32` | `optional` | `` |  |
| 2 | `language` | `uint32` | `optional` | `` |  |
| 3 | `name` | `string` | `optional` | `` |  |
| 4 | `broadcast_provider` | `.ELeagueBroadcastProvider` | `optional` | `` | default = LEAGUE_BROADCAST_UNKNOWN |
| 5 | `stream_url` | `string` | `optional` | `` |  |
| 6 | `vod_url` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALeague.SeriesInfo</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTALeague`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `series_id` | `uint32` | `optional` | `` |  |
| 2 | `series_type` | `uint32` | `optional` | `` |  |
| 3 | `start_time` | `uint32` | `optional` | `` |  |
| 4 | `match_ids` | `uint64` | `repeated` | `` |  |
| 5 | `team_id_1` | `uint32` | `optional` | `` |  |
| 6 | `team_id_2` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALeague.Player</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTALeague`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `name` | `string` | `optional` | `` |  |
| 3 | `team_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALeagueList</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `leagues` | `.CMsgDOTALeague` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALeagueInfo</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_id` | `uint32` | `optional` | `` |  |
| 2 | `name` | `string` | `optional` | `` |  |
| 3 | `tier` | `.ELeagueTier` | `optional` | `` | default = LEAGUE_TIER_UNSET |
| 4 | `region` | `.ELeagueRegion` | `optional` | `` | default = LEAGUE_REGION_UNSET |
| 5 | `most_recent_activity` | `uint32` | `optional` | `` |  |
| 6 | `total_prize_pool` | `uint32` | `optional` | `` |  |
| 7 | `start_timestamp` | `uint32` | `optional` | `` |  |
| 8 | `end_timestamp` | `uint32` | `optional` | `` |  |
| 9 | `status` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALeagueInfoList</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `infos` | `.CMsgDOTALeagueInfo` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALeagueLiveGames</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `games` | `.CMsgDOTALeagueLiveGames.LiveGame` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALeagueLiveGames.LiveGame</code> — fields: 13; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTALeagueLiveGames`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_id` | `uint32` | `optional` | `` |  |
| 2 | `server_steam_id` | `uint64` | `optional` | `` |  |
| 3 | `radiant_name` | `string` | `optional` | `` |  |
| 4 | `radiant_logo` | `uint64` | `optional` | `` |  |
| 5 | `dire_name` | `string` | `optional` | `` |  |
| 6 | `dire_logo` | `uint64` | `optional` | `` |  |
| 7 | `time` | `uint32` | `optional` | `` |  |
| 8 | `spectators` | `uint32` | `optional` | `` |  |
| 9 | `radiant_team_id` | `uint32` | `optional` | `` |  |
| 10 | `dire_team_id` | `uint32` | `optional` | `` |  |
| 11 | `league_node_id` | `uint32` | `optional` | `` |  |
| 12 | `series_id` | `uint32` | `optional` | `` |  |
| 13 | `match_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALeagueMessages</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `messages` | `.CMsgDOTALeagueMessages.Message` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALeagueMessages.Message</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTALeagueMessages`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `author_account_id` | `uint32` | `optional` | `` |  |
| 2 | `timestamp` | `uint32` | `optional` | `` |  |
| 3 | `message` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALeaguePrizePool</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `prize_pool` | `uint32` | `optional` | `` |  |
| 2 | `increment_per_second` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALeagueInfoListAdminsRequest</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgDOTALeagueAvailableLobbyNodesRequest</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALeagueAvailableLobbyNodes</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `node_infos` | `.CMsgDOTALeagueAvailableLobbyNodes.NodeInfo` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALeagueAvailableLobbyNodes.NodeInfo</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTALeagueAvailableLobbyNodes`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `node_id` | `uint32` | `optional` | `` |  |
| 2 | `node_name` | `string` | `optional` | `` |  |
| 3 | `node_group_name` | `string` | `optional` | `` |  |
| 4 | `team_id_1` | `uint32` | `optional` | `` |  |
| 5 | `team_id_2` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALeagueNodeResults</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `node_results` | `.CMsgDOTALeagueNodeResults.Result` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALeagueNodeResults.Result</code> — fields: 17; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTALeagueNodeResults`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `node_id` | `uint32` | `optional` | `` |  |
| 2 | `winning_node_id` | `uint32` | `optional` | `` |  |
| 3 | `losing_node_id` | `uint32` | `optional` | `` |  |
| 4 | `incoming_node_id_1` | `uint32` | `optional` | `` |  |
| 5 | `incoming_node_id_2` | `uint32` | `optional` | `` |  |
| 6 | `team_id_1` | `uint32` | `optional` | `` |  |
| 7 | `team_id_2` | `uint32` | `optional` | `` |  |
| 8 | `team_1_name` | `string` | `optional` | `` |  |
| 9 | `team_2_name` | `string` | `optional` | `` |  |
| 10 | `team_1_wins` | `uint32` | `optional` | `` |  |
| 11 | `team_2_wins` | `uint32` | `optional` | `` |  |
| 12 | `winning_team_id` | `uint32` | `optional` | `` |  |
| 13 | `losing_team_id` | `uint32` | `optional` | `` |  |
| 14 | `has_started` | `bool` | `optional` | `` |  |
| 15 | `is_completed` | `bool` | `optional` | `` |  |
| 16 | `scheduled_time` | `uint32` | `optional` | `` |  |
| 17 | `match_ids` | `uint64` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTADPCLeagueResults</code> — fields: 3; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `results` | `.CMsgDOTADPCLeagueResults.Result` | `repeated` | `` |  |
| 2 | `points` | `uint32` | `repeated` | `` |  |
| 3 | `dollars` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTADPCLeagueResults.Result</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTADPCLeagueResults`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `standing` | `uint32` | `optional` | `` |  |
| 2 | `team_id` | `uint32` | `optional` | `` |  |
| 3 | `team_name` | `string` | `optional` | `` |  |
| 4 | `team_logo` | `uint64` | `optional` | `` |  |
| 5 | `team_logo_url` | `string` | `optional` | `` |  |
| 6 | `points` | `uint32` | `optional` | `` |  |
| 7 | `earnings` | `uint32` | `optional` | `` |  |
| 8 | `timestamp` | `uint32` | `optional` | `` |  |
| 9 | `phase` | `.ELeaguePhase` | `optional` | `` | default = LEAGUE_PHASE_UNSET |
| 10 | `team_abbreviation` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTADPCTeamResults</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `results` | `.CMsgDOTADPCTeamResults.Result` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTADPCTeamResults.Result</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTADPCTeamResults`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_id` | `uint32` | `optional` | `` |  |
| 2 | `standing` | `uint32` | `optional` | `` |  |
| 3 | `points` | `uint32` | `optional` | `` |  |
| 4 | `earnings` | `uint32` | `optional` | `` |  |
| 5 | `timestamp` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTADPCSeasonResults</code> — fields: 5; oneofs: 0; nested messages: 4; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `results` | `.CMsgDOTADPCSeasonResults.TeamResult` | `repeated` | `` |  |
| 2 | `standings` | `.CMsgDOTADPCSeasonResults.Standing` | `repeated` | `` |  |
| 3 | `major_wildcard_standings` | `.CMsgDOTADPCSeasonResults.StandingEntry` | `repeated` | `` |  |
| 4 | `major_group_standings` | `.CMsgDOTADPCSeasonResults.StandingEntry` | `repeated` | `` |  |
| 5 | `major_playoff_standings` | `.CMsgDOTADPCSeasonResults.StandingEntry` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTADPCSeasonResults.TeamLeagueResult</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTADPCSeasonResults`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `timestamp` | `uint32` | `optional` | `` |  |
| 2 | `league_id` | `uint32` | `optional` | `` |  |
| 3 | `standing` | `uint32` | `optional` | `` |  |
| 4 | `points` | `uint32` | `optional` | `` |  |
| 5 | `earnings` | `uint32` | `optional` | `` |  |
| 6 | `audit_action` | `uint32` | `optional` | `` |  |
| 7 | `audit_data` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTADPCSeasonResults.TeamResult</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTADPCSeasonResults`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team_id` | `uint32` | `optional` | `` |  |
| 2 | `team_name` | `string` | `optional` | `` |  |
| 3 | `team_logo` | `uint64` | `optional` | `` |  |
| 4 | `team_logo_url` | `string` | `optional` | `` |  |
| 5 | `total_points` | `uint32` | `optional` | `` |  |
| 6 | `total_earnings` | `uint32` | `optional` | `` |  |
| 7 | `league_results` | `.CMsgDOTADPCSeasonResults.TeamLeagueResult` | `repeated` | `` |  |
| 8 | `team_abbreviation` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTADPCSeasonResults.StandingEntry</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTADPCSeasonResults`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team_id` | `uint32` | `optional` | `` |  |
| 2 | `wins` | `uint32` | `optional` | `` |  |
| 3 | `losses` | `uint32` | `optional` | `` |  |
| 4 | `team_url` | `string` | `optional` | `` |  |
| 5 | `team_name` | `string` | `optional` | `` |  |
| 6 | `team_abbreviation` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTADPCSeasonResults.Standing</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTADPCSeasonResults`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `region` | `.ELeagueRegion` | `optional` | `` | default = LEAGUE_REGION_UNSET |
| 2 | `division` | `.ELeagueDivision` | `optional` | `` | default = LEAGUE_DIVISION_UNSET |
| 3 | `entries` | `.CMsgDOTADPCSeasonResults.StandingEntry` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTADPCSeasonSpoilerResults</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `time_last_updated` | `uint32` | `optional` | `` |  |
| 2 | `saved_results` | `.CMsgDOTADPCSeasonResults` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>ELeagueNodeGroupType</code> — values: 10</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `INVALID_GROUP_TYPE` | 0 |
| `ORGANIZATIONAL` | 1 |
| `ROUND_ROBIN` | 2 |
| `SWISS` | 3 |
| `BRACKET_SINGLE` | 4 |
| `BRACKET_DOUBLE_SEED_LOSER` | 5 |
| `BRACKET_DOUBLE_ALL_WINNER` | 6 |
| `SHOWMATCH` | 7 |
| `GSL` | 8 |
| `PLACEMENT` | 9 |

</details>

<details>
<summary><code>ELeagueNodeType</code> — values: 5</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `INVALID_NODE_TYPE` | 0 |
| `BEST_OF_ONE` | 1 |
| `BEST_OF_THREE` | 2 |
| `BEST_OF_FIVE` | 3 |
| `BEST_OF_TWO` | 4 |

</details>
