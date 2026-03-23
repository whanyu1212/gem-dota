# dota_gcmessages_common_battle_report.proto

- Module: `dota_gcmessages_common_battle_report_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **7**
- Messages: **23** (top-level: 18)
- Enums: **13** (top-level: 8)

## Imports

- `steammessages.proto`
- `dota_shared_enums.proto`
- `dota_gcmessages_common.proto`
- `gcsdk_gcmessages.proto`
- `base_gcmessages.proto`
- `econ_gcmessages.proto`
- `valveextensions.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgClientToGCGetBattleReport</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `timestamp` | `uint32` | `optional` | `` |  |
| 3 | `duration` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgBattleReport_Game</code> — fields: 50; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `kills` | `uint32` | `optional` | `` |  |
| 3 | `deaths` | `uint32` | `optional` | `` |  |
| 4 | `assists` | `uint32` | `optional` | `` |  |
| 5 | `rank_change` | `int32` | `optional` | `` |  |
| 6 | `last_hits` | `uint32` | `optional` | `` |  |
| 7 | `gpm` | `uint32` | `optional` | `` |  |
| 8 | `xpm` | `uint32` | `optional` | `` |  |
| 9 | `role` | `.CMsgBattleReport_Role` | `optional` | `` | default = k_eUnknownRole |
| 10 | `outcome` | `.CMsgBattleReport_EOutcome` | `optional` | `` | default = k_eWin |
| 11 | `lane_outcome` | `.CMsgBattleReport_ELaneOutcome` | `optional` | `` | default = k_eUnknownLaneOutcome |
| 12 | `ranked` | `bool` | `optional` | `` |  |
| 13 | `match_id` | `uint64` | `optional` | `` |  |
| 14 | `lane_selection_flags` | `uint32` | `optional` | `` |  |
| 15 | `predicted_position` | `uint32` | `optional` | `` |  |
| 16 | `seconds_dead` | `uint32` | `optional` | `` |  |
| 17 | `winning_team` | `uint32` | `optional` | `` |  |
| 19 | `party_game` | `bool` | `optional` | `` |  |
| 20 | `start_time` | `uint32` | `optional` | `` |  |
| 21 | `denies` | `uint32` | `optional` | `` |  |
| 22 | `bounty_runes` | `uint32` | `optional` | `` |  |
| 23 | `water_runes` | `uint32` | `optional` | `` |  |
| 24 | `power_runes` | `uint32` | `optional` | `` |  |
| 25 | `time_enemy_t1_tower_destroyed` | `uint32` | `optional` | `` |  |
| 26 | `time_friendly_t1_tower_destroyed` | `uint32` | `optional` | `` |  |
| 27 | `enemy_roshan_kills` | `uint32` | `optional` | `` |  |
| 28 | `player_slot` | `uint32` | `optional` | `` |  |
| 29 | `teleports_used` | `uint32` | `optional` | `` |  |
| 30 | `dewards` | `uint32` | `optional` | `` |  |
| 31 | `camps_stacked` | `uint32` | `optional` | `` |  |
| 32 | `support_gold` | `uint32` | `optional` | `` |  |
| 33 | `hero_damage` | `uint32` | `optional` | `` |  |
| 34 | `hero_healing` | `uint32` | `optional` | `` |  |
| 35 | `tower_damage` | `uint32` | `optional` | `` |  |
| 36 | `successful_smokes` | `uint32` | `optional` | `` |  |
| 37 | `stun_duration` | `uint32` | `optional` | `` |  |
| 38 | `duration` | `uint32` | `optional` | `` |  |
| 39 | `friendly_roshan_kills` | `uint32` | `optional` | `` |  |
| 40 | `previous_rank` | `int32` | `optional` | `` |  |
| 41 | `game_mode` | `uint32` | `optional` | `` |  |
| 42 | `lobby_type` | `uint32` | `optional` | `` |  |
| 43 | `time_purchased_shard` | `float` | `optional` | `` |  |
| 44 | `time_purchased_scepter` | `float` | `optional` | `` |  |
| 45 | `item0` | `int32` | `optional` | `` | default = -1 |
| 46 | `item1` | `int32` | `optional` | `` | default = -1 |
| 47 | `item2` | `int32` | `optional` | `` | default = -1 |
| 48 | `item3` | `int32` | `optional` | `` | default = -1 |
| 49 | `item4` | `int32` | `optional` | `` | default = -1 |
| 50 | `item5` | `int32` | `optional` | `` | default = -1 |
| 51 | `selected_facet` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgBattleReport_GameList</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `games` | `.CMsgBattleReport_Game` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgBattleReport</code> — fields: 2; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `games` | `.CMsgBattleReport_Game` | `repeated` | `` |  |
| 3 | `highlights` | `.CMsgBattleReportHighlights` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgBattleReport.HighlightGeneral</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgBattleReport`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `win_loss_window` | `int32` | `optional` | `` |  |
| 2 | `win_percent` | `float` | `optional` | `` |  |
| 3 | `mmr_delta` | `int32` | `optional` | `` |  |
| 4 | `highlight_score` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgBattleReport.Highlight</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgBattleReport`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `highlight_id` | `uint32` | `required` | `` |  |
| 2 | `category` | `.CMsgBattleReport_HighlightCategory` | `required` | `` | default = k_eHighlightGeneral |
| 3 | `tier` | `.CMsgBattleReport_HighlightTier` | `optional` | `` | default = k_eHighlightTierLow |
| 4 | `rarity` | `.CMsgBattleReport_HighlightRarity` | `optional` | `` | default = k_eHighlightCommon |
| 5 | `score` | `float` | `optional` | `` |  |
| 6 | `confidence` | `float` | `optional` | `` |  |
| 7 | `hero_id` | `int32` | `optional` | `` |  |
| 8 | `role` | `.CMsgBattleReport_Role` | `optional` | `` | default = k_eUnknownRole |
| 9 | `comparison_delta_value` | `float` | `optional` | `` |  |
| 10 | `context` | `.CMsgBattleReport_CompareContext` | `optional` | `` | default = k_eCompareContextInvalid |

</details>

<details>
<summary><code>CMsgBattleReportInfo</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `timestamp` | `uint32` | `optional` | `` |  |
| 2 | `duration` | `uint32` | `optional` | `` |  |
| 3 | `acknowledged` | `bool` | `optional` | `` |  |
| 4 | `featured_hero_id` | `int32` | `optional` | `` |  |
| 5 | `featured_position` | `uint32` | `optional` | `` |  |
| 6 | `games_played` | `uint32` | `optional` | `` |  |
| 7 | `medal_counts` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgBattleReportInfoList</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `battle_report_info` | `.CMsgBattleReportInfo` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgBattleReportHighlights</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `highlights` | `.CMsgBattleReport.Highlight` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgBattleReportAggregateStats</code> — fields: 1; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgBattleReportAggregateStats.CMsgBattleReportAggregate` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgBattleReportAggregateStats.CMsgBattleReportStat</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgBattleReportAggregateStats`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `mean` | `float` | `optional` | `` |  |
| 2 | `stdev` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgBattleReportAggregateStats.CMsgBattleReportAggregate</code> — fields: 31; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgBattleReportAggregateStats`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `predicted_position` | `uint32` | `optional` | `` |  |
| 3 | `game_count` | `uint32` | `optional` | `` |  |
| 4 | `win_count` | `uint32` | `optional` | `` |  |
| 5 | `lane_win_count` | `uint32` | `optional` | `` |  |
| 6 | `kills` | `.CMsgBattleReportAggregateStats.CMsgBattleReportStat` | `optional` | `` |  |
| 7 | `deaths` | `.CMsgBattleReportAggregateStats.CMsgBattleReportStat` | `optional` | `` |  |
| 8 | `assists` | `.CMsgBattleReportAggregateStats.CMsgBattleReportStat` | `optional` | `` |  |
| 9 | `rank_change` | `.CMsgBattleReportAggregateStats.CMsgBattleReportStat` | `optional` | `` |  |
| 10 | `last_hits` | `.CMsgBattleReportAggregateStats.CMsgBattleReportStat` | `optional` | `` |  |
| 11 | `denies` | `.CMsgBattleReportAggregateStats.CMsgBattleReportStat` | `optional` | `` |  |
| 12 | `gpm` | `.CMsgBattleReportAggregateStats.CMsgBattleReportStat` | `optional` | `` |  |
| 13 | `xpm` | `.CMsgBattleReportAggregateStats.CMsgBattleReportStat` | `optional` | `` |  |
| 14 | `seconds_dead` | `.CMsgBattleReportAggregateStats.CMsgBattleReportStat` | `optional` | `` |  |
| 15 | `bounty_runes` | `.CMsgBattleReportAggregateStats.CMsgBattleReportStat` | `optional` | `` |  |
| 16 | `water_runes` | `.CMsgBattleReportAggregateStats.CMsgBattleReportStat` | `optional` | `` |  |
| 17 | `power_runes` | `.CMsgBattleReportAggregateStats.CMsgBattleReportStat` | `optional` | `` |  |
| 18 | `time_enemy_t1_tower_destroyed` | `.CMsgBattleReportAggregateStats.CMsgBattleReportStat` | `optional` | `` |  |
| 19 | `time_friendly_t1_tower_destroyed` | `.CMsgBattleReportAggregateStats.CMsgBattleReportStat` | `optional` | `` |  |
| 20 | `enemy_roshan_kills` | `.CMsgBattleReportAggregateStats.CMsgBattleReportStat` | `optional` | `` |  |
| 21 | `teleports_used` | `.CMsgBattleReportAggregateStats.CMsgBattleReportStat` | `optional` | `` |  |
| 22 | `dewards` | `.CMsgBattleReportAggregateStats.CMsgBattleReportStat` | `optional` | `` |  |
| 23 | `camps_stacked` | `.CMsgBattleReportAggregateStats.CMsgBattleReportStat` | `optional` | `` |  |
| 24 | `support_gold` | `.CMsgBattleReportAggregateStats.CMsgBattleReportStat` | `optional` | `` |  |
| 25 | `hero_damage` | `.CMsgBattleReportAggregateStats.CMsgBattleReportStat` | `optional` | `` |  |
| 26 | `hero_healing` | `.CMsgBattleReportAggregateStats.CMsgBattleReportStat` | `optional` | `` |  |
| 27 | `tower_damage` | `.CMsgBattleReportAggregateStats.CMsgBattleReportStat` | `optional` | `` |  |
| 28 | `successful_smokes` | `.CMsgBattleReportAggregateStats.CMsgBattleReportStat` | `optional` | `` |  |
| 29 | `stun_duration` | `.CMsgBattleReportAggregateStats.CMsgBattleReportStat` | `optional` | `` |  |
| 30 | `duration` | `.CMsgBattleReportAggregateStats.CMsgBattleReportStat` | `optional` | `` |  |
| 31 | `friendly_roshan_kills` | `.CMsgBattleReportAggregateStats.CMsgBattleReportStat` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgBattleReportAggregatedGeneralStats</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCGetBattleReportResponse</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `report` | `.CMsgBattleReport` | `optional` | `` |  |
| 2 | `response` | `.CMsgClientToGCGetBattleReportResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 3 | `aggregate_stats` | `.CMsgBattleReportAggregateStats` | `optional` | `` |  |
| 4 | `info` | `.CMsgBattleReportInfo` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetBattleReportAggregateStats</code> — fields: 4; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `aggregate_keys` | `.CMsgClientToGCGetBattleReportAggregateStats.CMsgBattleReportAggregateKey` | `repeated` | `` |  |
| 2 | `timestamp` | `uint32` | `optional` | `` |  |
| 3 | `duration` | `uint32` | `optional` | `` |  |
| 4 | `rank` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetBattleReportAggregateStats.CMsgBattleReportAggregateKey</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientToGCGetBattleReportAggregateStats`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `predicted_position` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetBattleReportAggregateStatsResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `aggregate_stats` | `.CMsgBattleReportAggregateStats` | `optional` | `` |  |
| 2 | `response` | `.CMsgClientToGCGetBattleReportAggregateStatsResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCGetBattleReportInfo</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetBattleReportInfoResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `battle_report_info_list` | `.CMsgBattleReportInfoList` | `optional` | `` |  |
| 2 | `response` | `.CMsgClientToGCGetBattleReportInfoResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCAcknowledgeBattleReport</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `timestamp` | `uint32` | `optional` | `` |  |
| 3 | `duration` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCAcknowledgeBattleReportResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCAcknowledgeBattleReportResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `shards_awarded` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetBattleReportMatchHistory</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `timestamp` | `uint32` | `optional` | `` |  |
| 3 | `duration` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGetBattleReportMatchHistoryResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCGetBattleReportMatchHistoryResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `games` | `.CMsgBattleReport_GameList` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>CMsgBattleReport_HighlightType</code> — values: 67</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eHighlightTypeInvalid` | -1 |
| `k_eGameWinrate` | 0 |
| `k_eLaneWinrate` | 1 |
| `k_eMMRDelta` | 2 |
| `k_eNumHeroesPlayed` | 3 |
| `k_eNumGamesPlayed` | 4 |
| `k_eAveragePowerRunesTaken` | 5 |
| `k_eAverageBountyRunesTaken` | 6 |
| `k_eTotalKillEnemyT1First` | 7 |
| `k_eTotalRoshanKills` | 8 |
| `k_eTotalDewards` | 9 |
| `k_eTotalCampsStacked` | 10 |
| `k_eMaxWinstreak` | 11 |
| `k_eAverageDewards` | 12 |
| `k_eAverageKills` | 13 |
| `k_eMaxKills` | 14 |
| `k_eAverageAssists` | 15 |
| `k_eMaxAssists` | 16 |
| `k_eAverageDeaths` | 17 |
| `k_eMinDeaths` | 18 |
| `k_eAverageCampsStacked` | 19 |
| `k_eTotalLastHits` | 20 |
| `k_eAverageLastHits` | 21 |
| `k_eTotalDenies` | 22 |
| `k_eAverageDenies` | 23 |
| `k_eTotalGamesWithRoshanAdvantage` | 24 |
| `k_ePercentGamesWithRoshanAdvantage` | 25 |
| `k_eAverageStunDuration` | 26 |
| `k_eTotalStunDuration` | 27 |
| `k_eAverageTeleportsUsed` | 28 |
| `k_eTotalTeleportsUsed` | 29 |
| `k_eAverageHeroDamage` | 30 |
| `k_eTotalHeroDamage` | 31 |
| `k_eAverageHeroHealing` | 32 |
| `k_eTotalHeroHealing` | 33 |
| `k_eAverageTowerDamage` | 34 |
| `k_eTotalTowerDamage` | 35 |
| `k_eMaxLossStreak` | 36 |
| `k_eAverageGameDuration` | 37 |
| `k_eMaxGameDuration` | 38 |
| `k_eMinGameDuration` | 39 |
| `k_eAverageWinDuration` | 40 |
| `k_eMaxWinDuration` | 41 |
| `k_eMinWinDuration` | 42 |
| `k_eAverageLossDuration` | 43 |
| `k_eMaxLossDuration` | 44 |
| `k_eMinLossDuration` | 45 |
| `k_ePctGamesEnemyT1TakenFirst` | 46 |
| `k_eMaxCampsStacked` | 47 |
| `k_eMaxDewards` | 48 |
| `k_eMaxRoshanKills` | 49 |
| `k_eMaxBountyRunesTaken` | 50 |
| `k_eMaxPowerRunesTaken` | 51 |
| `k_eMaxDeaths` | 52 |
| `k_eMaxLastHits` | 53 |
| `k_eMaxDenies` | 54 |
| `k_eRadiantWinRate` | 55 |
| `k_eDireWinRate` | 56 |
| `k_eRadiantGameCount` | 57 |
| `k_eDireGameCount` | 58 |
| `k_eMaxDamage` | 59 |
| `k_eMaxHealing` | 60 |
| `k_eMaxTowerDamage` | 61 |
| `k_eAverageGPM` | 62 |
| `k_eMaxGPM` | 63 |
| `k_eAverageXPM` | 64 |
| `k_eMaxXPM` | 65 |

</details>

<details>
<summary><code>CMsgBattleReport_HighlightCategory</code> — values: 3</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eHighlightGeneral` | 0 |
| `k_eHighlightHero` | 1 |
| `k_eHighlightRole` | 2 |

</details>

<details>
<summary><code>CMsgBattleReport_Role</code> — values: 6</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eUnknownRole` | -1 |
| `k_eSafelane` | 0 |
| `k_eMidlane` | 1 |
| `k_eOfflane` | 2 |
| `k_eSupport` | 3 |
| `k_eHardSupport` | 4 |

</details>

<details>
<summary><code>CMsgBattleReport_CompareContext</code> — values: 5</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eCompareContextInvalid` | -1 |
| `k_eAbsoluteValue` | 0 |
| `k_ePlayersOfSimilarRank` | 1 |
| `k_eAllPlayers` | 2 |
| `k_ePlayersPersonalHistory` | 3 |

</details>

<details>
<summary><code>CMsgBattleReport_HighlightTier</code> — values: 6</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eHighlightTierLow` | -1 |
| `k_eHighlightTierNone` | 0 |
| `k_eHighlightTier1` | 1 |
| `k_eHighlightTier2` | 2 |
| `k_eHighlightTier3` | 3 |
| `k_eHighlightTierCustom` | 4 |

</details>

<details>
<summary><code>CMsgBattleReport_HighlightRarity</code> — values: 3</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eHighlightCommon` | 0 |
| `k_eHighlightUncommon` | 1 |
| `k_eHighlightRare` | 2 |

</details>

<details>
<summary><code>CMsgBattleReport_EOutcome</code> — values: 2</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eWin` | 0 |
| `k_eLoss` | 1 |

</details>

<details>
<summary><code>CMsgBattleReport_ELaneOutcome</code> — values: 4</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eUnknownLaneOutcome` | -1 |
| `k_eWonLane` | 0 |
| `k_eLostLane` | 1 |
| `k_eEvenLane` | 2 |

</details>

<details>
<summary><code>CMsgClientToGCGetBattleReportResponse.EResponse</code> — values: 12</summary>

- Parent: `CMsgClientToGCGetBattleReportResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_ePermissionDenied` | 4 |
| `k_eNotSubscribedToDotaPlus` | 5 |
| `k_eInvalidParameters` | 6 |
| `k_eUnableToGetPlusSubInfo` | 7 |
| `k_eUnableToLoadBattleReport` | 8 |
| `k_eUnableToSaveBattleReport` | 9 |
| `k_eUnableToGetAggregates` | 10 |
| `k_eNotEnoughGamesPlayed` | 11 |

</details>

<details>
<summary><code>CMsgClientToGCGetBattleReportAggregateStatsResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCGetBattleReportAggregateStatsResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_ePermissionDenied` | 4 |
| `k_eInvalidParams` | 5 |
| `k_eNotSubscribedToDotaPlus` | 6 |

</details>

<details>
<summary><code>CMsgClientToGCGetBattleReportInfoResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCGetBattleReportInfoResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_ePermissionDenied` | 4 |
| `k_eNotSubscribedToDotaPlus` | 5 |

</details>

<details>
<summary><code>CMsgClientToGCAcknowledgeBattleReportResponse.EResponse</code> — values: 11</summary>

- Parent: `CMsgClientToGCAcknowledgeBattleReportResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_ePermissionDenied` | 5 |
| `k_eUnableToLoadBattleReport` | 6 |
| `k_eAlreadyAcknowledged` | 7 |
| `k_eUnknownReport` | 8 |
| `k_eNotSubscribedToDotaPlus` | 9 |
| `k_eNotEnoughGamesPlayed` | 10 |

</details>

<details>
<summary><code>CMsgClientToGCGetBattleReportMatchHistoryResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCGetBattleReportMatchHistoryResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_ePermissionDenied` | 5 |
| `k_eNotSubscribedToDotaPlus` | 6 |

</details>
