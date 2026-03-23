# dota_gcmessages_client_watch.proto

- Module: `dota_gcmessages_client_watch_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **1**
- Messages: **23** (top-level: 19)
- Enums: **2** (top-level: 0)

## Imports

- `dota_gcmessages_common.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CSourceTVGameSmall</code> — fields: 33; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `activate_time` | `uint32` | `optional` | `` |  |
| 2 | `deactivate_time` | `uint32` | `optional` | `` |  |
| 3 | `server_steam_id` | `uint64` | `optional` | `` |  |
| 4 | `lobby_id` | `uint64` | `optional` | `` |  |
| 5 | `league_id` | `uint32` | `optional` | `` |  |
| 6 | `lobby_type` | `uint32` | `optional` | `` |  |
| 7 | `game_time` | `int32` | `optional` | `` |  |
| 8 | `delay` | `uint32` | `optional` | `` |  |
| 9 | `spectators` | `uint32` | `optional` | `` |  |
| 10 | `game_mode` | `uint32` | `optional` | `` |  |
| 11 | `average_mmr` | `uint32` | `optional` | `` |  |
| 12 | `match_id` | `uint64` | `optional` | `` |  |
| 13 | `series_id` | `uint32` | `optional` | `` |  |
| 15 | `team_name_radiant` | `string` | `optional` | `` |  |
| 16 | `team_name_dire` | `string` | `optional` | `` |  |
| 17 | `sort_score` | `uint32` | `optional` | `` |  |
| 18 | `last_update_time` | `float` | `optional` | `` |  |
| 19 | `radiant_lead` | `int32` | `optional` | `` |  |
| 20 | `radiant_score` | `uint32` | `optional` | `` |  |
| 21 | `dire_score` | `uint32` | `optional` | `` |  |
| 22 | `players` | `.CSourceTVGameSmall.Player` | `repeated` | `` |  |
| 23 | `building_state` | `fixed32` | `optional` | `` |  |
| 24 | `team_logo_radiant` | `fixed64` | `optional` | `` |  |
| 25 | `team_logo_dire` | `fixed64` | `optional` | `` |  |
| 26 | `weekend_tourney_tournament_id` | `uint32` | `optional` | `` |  |
| 27 | `weekend_tourney_division` | `uint32` | `optional` | `` |  |
| 28 | `weekend_tourney_skill_level` | `uint32` | `optional` | `` |  |
| 29 | `weekend_tourney_bracket_round` | `uint32` | `optional` | `` |  |
| 30 | `team_id_radiant` | `uint32` | `optional` | `` |  |
| 31 | `team_id_dire` | `uint32` | `optional` | `` |  |
| 32 | `custom_game_difficulty` | `uint32` | `optional` | `` |  |
| 33 | `is_player_draft` | `bool` | `optional` | `` |  |
| 34 | `is_watch_eligible` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CSourceTVGameSmall.Player</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CSourceTVGameSmall`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `hero_id` | `int32` | `optional` | `` |  |
| 3 | `team_slot` | `uint32` | `optional` | `` |  |
| 4 | `team` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCFindTopSourceTVGames</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `search_key` | `string` | `optional` | `` |  |
| 2 | `league_id` | `uint32` | `optional` | `` |  |
| 3 | `hero_id` | `int32` | `optional` | `` |  |
| 4 | `start_game` | `uint32` | `optional` | `` |  |
| 5 | `game_list_index` | `uint32` | `optional` | `` |  |
| 6 | `lobby_ids` | `uint64` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientFindTopSourceTVGamesResponse</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `search_key` | `string` | `optional` | `` |  |
| 2 | `league_id` | `uint32` | `optional` | `` |  |
| 3 | `hero_id` | `int32` | `optional` | `` |  |
| 4 | `start_game` | `uint32` | `optional` | `` |  |
| 5 | `num_games` | `uint32` | `optional` | `` |  |
| 6 | `game_list_index` | `uint32` | `optional` | `` |  |
| 7 | `game_list` | `.CSourceTVGameSmall` | `repeated` | `` |  |
| 8 | `specific_games` | `bool` | `optional` | `` |  |
| 9 | `bot_game` | `.CSourceTVGameSmall` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientTopWeekendTourneyGames</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `live_games` | `.CSourceTVGameSmall` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCTopLeagueMatchesRequest</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCTopFriendMatchesRequest</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCMatchesMinimalRequest</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_ids` | `uint64` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCMatchesMinimalResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `matches` | `.CMsgDOTAMatchMinimal` | `repeated` | `` |  |
| 2 | `last_match` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientTopLeagueMatchesResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `matches` | `.CMsgDOTAMatchMinimal` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientTopFriendMatchesResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `matches` | `.CMsgDOTAMatchMinimal` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSpectateFriendGame</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steam_id` | `fixed64` | `optional` | `` |  |
| 2 | `live` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSpectateFriendGameResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 4 | `server_steamid` | `fixed64` | `optional` | `` |  |
| 5 | `watch_live_result` | `.CMsgSpectateFriendGameResponse.EWatchLiveResult` | `optional` | `` | default = SUCCESS |

</details>

<details>
<summary><code>CDOTAReplayDownloadInfo</code> — fields: 6; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match` | `.CMsgDOTAMatchMinimal` | `optional` | `` |  |
| 2 | `title` | `string` | `optional` | `` |  |
| 3 | `description` | `string` | `optional` | `` |  |
| 4 | `size` | `uint32` | `optional` | `` |  |
| 5 | `tags` | `string` | `repeated` | `` |  |
| 6 | `exists_on_disk` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAReplayDownloadInfo.Highlight</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAReplayDownloadInfo`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `timestamp` | `uint32` | `optional` | `` |  |
| 2 | `description` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgWatchGame</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `server_steamid` | `fixed64` | `optional` | `` |  |
| 2 | `client_version` | `uint32` | `optional` | `` |  |
| 3 | `watch_server_steamid` | `fixed64` | `optional` | `` |  |
| 4 | `lobby_id` | `uint64` | `optional` | `` |  |
| 5 | `regions` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgCancelWatchGame</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgWatchGameResponse</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `watch_game_result` | `.CMsgWatchGameResponse.WatchGameResult` | `optional` | `` | default = PENDING |
| 2 | `source_tv_public_addr` | `uint32` | `optional` | `` |  |
| 3 | `source_tv_private_addr` | `uint32` | `optional` | `` |  |
| 4 | `source_tv_port` | `uint32` | `optional` | `` |  |
| 5 | `game_server_steamid` | `fixed64` | `optional` | `` |  |
| 6 | `watch_server_steamid` | `fixed64` | `optional` | `` |  |
| 7 | `watch_tv_unique_secret_code` | `fixed64` | `optional` | `` |  |
| 8 | `broadcast_url` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPartyLeaderWatchGamePrompt</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 5 | `game_server_steamid` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTABroadcasterInfo</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `server_steam_id` | `fixed64` | `optional` | `` |  |
| 3 | `live` | `bool` | `optional` | `` |  |
| 4 | `team_name_radiant` | `string` | `optional` | `` |  |
| 5 | `team_name_dire` | `string` | `optional` | `` |  |
| 7 | `series_game` | `uint32` | `optional` | `` |  |
| 9 | `upcoming_broadcast_timestamp` | `uint32` | `optional` | `` |  |
| 10 | `allow_live_video` | `bool` | `optional` | `` |  |
| 11 | `node_type` | `uint32` | `optional` | `` |  |
| 12 | `node_name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTASeries</code> — fields: 6; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `series_id` | `uint32` | `optional` | `` |  |
| 2 | `series_type` | `uint32` | `optional` | `` |  |
| 3 | `team_1` | `.CMsgDOTASeries.TeamInfo` | `optional` | `` |  |
| 4 | `team_2` | `.CMsgDOTASeries.TeamInfo` | `optional` | `` |  |
| 5 | `match_minimal` | `.CMsgDOTAMatchMinimal` | `repeated` | `` |  |
| 6 | `live_game` | `.CMsgDOTASeries.LiveGame` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTASeries.TeamInfo</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTASeries`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team_id` | `uint32` | `optional` | `` |  |
| 2 | `team_name` | `string` | `optional` | `` |  |
| 3 | `team_logo_url` | `string` | `optional` | `` |  |
| 4 | `wager_count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTASeries.LiveGame</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTASeries`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `server_steam_id` | `fixed64` | `optional` | `` |  |
| 2 | `team_radiant` | `.CMsgDOTASeries.TeamInfo` | `optional` | `` |  |
| 3 | `team_dire` | `.CMsgDOTASeries.TeamInfo` | `optional` | `` |  |
| 4 | `team_radiant_score` | `uint32` | `optional` | `` |  |
| 5 | `team_dire_score` | `uint32` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>CMsgSpectateFriendGameResponse.EWatchLiveResult</code> — values: 15</summary>

- Parent: `CMsgSpectateFriendGameResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `ERROR_GENERIC` | 1 |
| `ERROR_NO_PLUS` | 2 |
| `ERROR_NOT_FRIENDS` | 3 |
| `ERROR_LOBBY_NOT_FOUND` | 4 |
| `ERROR_SPECTATOR_IN_A_LOBBY` | 5 |
| `ERROR_LOBBY_IS_LAN` | 6 |
| `ERROR_WRONG_LOBBY_TYPE` | 7 |
| `ERROR_WRONG_LOBBY_STATE` | 8 |
| `ERROR_PLAYER_NOT_PLAYER` | 9 |
| `ERROR_TOO_MANY_SPECTATORS` | 10 |
| `ERROR_SPECTATOR_SWITCHED_TEAMS` | 11 |
| `ERROR_FRIENDS_ON_BOTH_SIDES` | 12 |
| `ERROR_SPECTATOR_IN_THIS_LOBBY` | 13 |
| `ERROR_LOBBY_IS_LEAGUE` | 14 |

</details>

<details>
<summary><code>CMsgWatchGameResponse.WatchGameResult</code> — values: 8</summary>

- Parent: `CMsgWatchGameResponse`

| Name | Number |
|---|---:|
| `PENDING` | 0 |
| `READY` | 1 |
| `GAMESERVERNOTFOUND` | 2 |
| `UNAVAILABLE` | 3 |
| `CANCELLED` | 4 |
| `INCOMPATIBLEVERSION` | 5 |
| `MISSINGLEAGUESUBSCRIPTION` | 6 |
| `LOBBYNOTFOUND` | 7 |

</details>
