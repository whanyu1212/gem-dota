# dota_match_metadata.proto

- Module: `dota_match_metadata_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **10**
- Messages: **38** (top-level: 3)
- Enums: **2** (top-level: 1)

## Imports

- `base_gcmessages.proto`
- `dota_gcmessages_common_match_management.proto`
- `dota_gcmessages_common_lobby.proto`
- `dota_gcmessages_common_overworld.proto`
- `dota_gcmessages_common_craftworks.proto`
- `dota_gcmessages_common_monster_hunter.proto`
- `dota_gcmessages_common.proto`
- `dota_shared_enums.proto`
- `gcsdk_gcmessages.proto`
- `networkbasetypes.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CDOTAMatchMetadataFile</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `version` | `int32` | `required` | `` |  |
| 2 | `match_id` | `uint64` | `required` | `` |  |
| 3 | `metadata` | `.CDOTAMatchMetadata` | `optional` | `` |  |
| 5 | `private_metadata` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchMetadata</code> — fields: 12; oneofs: 0; nested messages: 4; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `teams` | `.CDOTAMatchMetadata.Team` | `repeated` | `` |  |
| 3 | `lobby_id` | `fixed64` | `optional` | `` |  |
| 4 | `report_until_time` | `fixed64` | `optional` | `` |  |
| 5 | `event_game_custom_table` | `bytes` | `optional` | `` |  |
| 6 | `primary_event_id` | `uint32` | `optional` | `` |  |
| 8 | `matchmaking_stats` | `.CMsgMatchMatchmakingStats` | `optional` | `` |  |
| 9 | `mvp_data` | `.CMvpData` | `optional` | `` |  |
| 10 | `guild_challenge_progress` | `.CDOTAMatchMetadata.GuildChallengeProgress` | `repeated` | `` |  |
| 11 | `custom_post_game_table` | `bytes` | `optional` | `` |  |
| 12 | `match_tips` | `.CDOTAMatchMetadata.Tip` | `repeated` | `` |  |
| 13 | `match_tracked_stats` | `.CMsgTrackedStat` | `repeated` | `` |  |
| 14 | `primary_event_id_for_display` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchMetadata.EconItem</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAMatchMetadata`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `def_index` | `uint32` | `optional` | `` |  |
| 2 | `quality` | `uint32` | `optional` | `` | default = 4 |
| 3 | `attribute` | `.CSOEconItemAttribute` | `repeated` | `` |  |
| 4 | `style` | `uint32` | `optional` | `` | default = 0 |
| 5 | `equipped_state` | `.CSOEconItemEquipped` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchMetadata.Team</code> — fields: 10; oneofs: 0; nested messages: 15; nested enums: 0</summary>

- Parent: `CDOTAMatchMetadata`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `dota_team` | `uint32` | `optional` | `` |  |
| 2 | `players` | `.CDOTAMatchMetadata.Team.Player` | `repeated` | `` |  |
| 3 | `graph_experience` | `float` | `repeated` | `` |  |
| 4 | `graph_gold_earned` | `float` | `repeated` | `` |  |
| 5 | `graph_net_worth` | `float` | `repeated` | `` |  |
| 6 | `cm_first_pick` | `bool` | `optional` | `` |  |
| 7 | `cm_captain_player_id` | `int32` | `optional` | `` | default = -1 |
| 10 | `cm_penalty` | `uint32` | `optional` | `` |  |
| 11 | `team_tracked_stats` | `.CMsgTrackedStat` | `repeated` | `` |  |
| 12 | `kills` | `.CDOTAMatchMetadata.Team.KillInfo` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchMetadata.Team.PlayerKill</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAMatchMetadata.Team`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `victim_slot` | `uint32` | `optional` | `` |  |
| 2 | `count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchMetadata.Team.ItemPurchase</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAMatchMetadata.Team`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `purchase_time` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchMetadata.Team.InventorySnapshot</code> — fields: 12; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAMatchMetadata.Team`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_id` | `int32` | `repeated` | `` |  |
| 2 | `game_time` | `int32` | `optional` | `` |  |
| 3 | `kills` | `uint32` | `optional` | `` |  |
| 4 | `deaths` | `uint32` | `optional` | `` |  |
| 5 | `assists` | `uint32` | `optional` | `` |  |
| 6 | `level` | `uint32` | `optional` | `` |  |
| 7 | `backpack_item_id` | `int32` | `repeated` | `` |  |
| 8 | `neutral_item_id` | `int32` | `optional` | `` | default = -1 |
| 9 | `neutral_enhancement_id` | `int32` | `optional` | `` | default = -1 |
| 10 | `last_hits` | `uint32` | `optional` | `` |  |
| 11 | `denies` | `uint32` | `optional` | `` |  |
| 12 | `flags` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchMetadata.Team.AutoStyleCriteria</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAMatchMetadata.Team`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name_token` | `uint32` | `optional` | `` |  |
| 2 | `value` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchMetadata.Team.StrangeGemProgress</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAMatchMetadata.Team`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `kill_eater_type` | `uint32` | `optional` | `` |  |
| 2 | `gem_item_def_index` | `uint32` | `optional` | `` |  |
| 3 | `required_hero_id` | `int32` | `optional` | `` |  |
| 4 | `starting_value` | `uint32` | `optional` | `` |  |
| 5 | `ending_value` | `uint32` | `optional` | `` |  |
| 6 | `owner_item_def_index` | `uint32` | `optional` | `` |  |
| 7 | `owner_item_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchMetadata.Team.VictoryPrediction</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAMatchMetadata.Team`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_id` | `uint64` | `optional` | `` |  |
| 2 | `item_def_index` | `uint32` | `optional` | `` |  |
| 3 | `starting_value` | `uint32` | `optional` | `` |  |
| 4 | `is_victory` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchMetadata.Team.SubChallenge</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAMatchMetadata.Team`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `slot_id` | `uint32` | `optional` | `` |  |
| 2 | `start_value` | `uint32` | `optional` | `` |  |
| 3 | `end_value` | `uint32` | `optional` | `` |  |
| 4 | `completed` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchMetadata.Team.CavernChallengeResult</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAMatchMetadata.Team`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `completed_path_id` | `uint32` | `optional` | `` | default = 255 |
| 2 | `claimed_room_id` | `uint32` | `optional` | `` | default = 255 |

</details>

<details>
<summary><code>CDOTAMatchMetadata.Team.ActionGrant</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAMatchMetadata.Team`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `action_id` | `uint32` | `optional` | `` |  |
| 2 | `quantity` | `uint32` | `optional` | `` |  |
| 3 | `audit` | `uint32` | `optional` | `` |  |
| 5 | `audit_data` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchMetadata.Team.CandyGrant</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAMatchMetadata.Team`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `points` | `uint32` | `optional` | `` |  |
| 2 | `reason` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchMetadata.Team.PeriodicResourceData</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAMatchMetadata.Team`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `periodic_resource_id` | `uint32` | `optional` | `` |  |
| 2 | `remaining` | `uint32` | `optional` | `` |  |
| 3 | `max` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchMetadata.Team.EventData</code> — fields: 26; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAMatchMetadata.Team`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |
| 2 | `event_points` | `uint32` | `optional` | `` |  |
| 3 | `challenge_instance_id` | `uint32` | `optional` | `` |  |
| 4 | `challenge_quest_id` | `uint32` | `optional` | `` |  |
| 5 | `challenge_quest_challenge_id` | `uint32` | `optional` | `` |  |
| 6 | `challenge_completed` | `bool` | `optional` | `` |  |
| 7 | `challenge_rank_completed` | `uint32` | `optional` | `` |  |
| 8 | `challenge_rank_previously_completed` | `uint32` | `optional` | `` |  |
| 9 | `event_owned` | `bool` | `optional` | `` |  |
| 10 | `sub_challenges_with_progress` | `.CDOTAMatchMetadata.Team.SubChallenge` | `repeated` | `` |  |
| 11 | `wager_winnings` | `uint32` | `optional` | `` |  |
| 12 | `cavern_challenge_active` | `bool` | `optional` | `` |  |
| 13 | `cavern_challenge_winnings` | `uint32` | `optional` | `` |  |
| 14 | `amount_wagered` | `uint32` | `optional` | `` |  |
| 16 | `periodic_point_adjustments` | `uint32` | `optional` | `` |  |
| 17 | `cavern_challenge_map_results` | `.CDOTAMatchMetadata.Team.CavernChallengeResult` | `repeated` | `` |  |
| 18 | `cavern_challenge_plus_shard_winnings` | `uint32` | `optional` | `` |  |
| 19 | `actions_granted` | `.CDOTAMatchMetadata.Team.ActionGrant` | `repeated` | `` |  |
| 20 | `cavern_crawl_map_variant` | `uint32` | `optional` | `` | default = 255 |
| 21 | `team_wager_bonus_pct` | `uint32` | `optional` | `` |  |
| 22 | `wager_streak_pct` | `uint32` | `optional` | `` |  |
| 23 | `candy_points_granted` | `.CDOTAMatchMetadata.Team.CandyGrant` | `repeated` | `` |  |
| 24 | `active_season_id` | `uint32` | `optional` | `` |  |
| 25 | `cavern_crawl_half_credit` | `bool` | `optional` | `` |  |
| 26 | `periodic_resources` | `.CDOTAMatchMetadata.Team.PeriodicResourceData` | `repeated` | `` |  |
| 27 | `extra_event_messages` | `.CExtraMsgBlock` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchMetadata.Team.FeaturedGamemodeProgress</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAMatchMetadata.Team`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `start_value` | `uint32` | `optional` | `` |  |
| 2 | `end_value` | `uint32` | `optional` | `` |  |
| 3 | `max_value` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchMetadata.Team.KillInfo</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: `CDOTAMatchMetadata.Team`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `kill_type` | `.CDOTAMatchMetadata.Team.KillInfo.KillType` | `optional` | `` | default = KILL_TYPE_PLAYER |
| 2 | `victim_player_slot` | `uint32` | `optional` | `` |  |
| 3 | `killer_player_slot` | `uint32` | `repeated` | `` |  |
| 4 | `time` | `int32` | `optional` | `` |  |
| 5 | `bounty` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchMetadata.Team.Player</code> — fields: 57; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: `CDOTAMatchMetadata.Team`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `ability_upgrades` | `int32` | `repeated` | `` |  |
| 3 | `player_slot` | `uint32` | `optional` | `` |  |
| 5 | `kills` | `.CDOTAMatchMetadata.Team.PlayerKill` | `repeated` | `` |  |
| 6 | `items` | `.CDOTAMatchMetadata.Team.ItemPurchase` | `repeated` | `` |  |
| 7 | `avg_kills_x16` | `uint32` | `optional` | `` |  |
| 8 | `avg_deaths_x16` | `uint32` | `optional` | `` |  |
| 9 | `avg_assists_x16` | `uint32` | `optional` | `` |  |
| 10 | `avg_gpm_x16` | `uint32` | `optional` | `` |  |
| 11 | `avg_xpm_x16` | `uint32` | `optional` | `` |  |
| 12 | `best_kills_x16` | `uint32` | `optional` | `` |  |
| 13 | `best_assists_x16` | `uint32` | `optional` | `` |  |
| 14 | `best_gpm_x16` | `uint32` | `optional` | `` |  |
| 15 | `best_xpm_x16` | `uint32` | `optional` | `` |  |
| 16 | `win_streak` | `uint32` | `optional` | `` |  |
| 17 | `best_win_streak` | `uint32` | `optional` | `` |  |
| 18 | `fight_score` | `float` | `optional` | `` |  |
| 19 | `farm_score` | `float` | `optional` | `` |  |
| 20 | `support_score` | `float` | `optional` | `` |  |
| 21 | `push_score` | `float` | `optional` | `` |  |
| 22 | `level_up_times` | `uint32` | `repeated` | `` |  |
| 23 | `graph_net_worth` | `float` | `repeated` | `` |  |
| 24 | `inventory_snapshot` | `.CDOTAMatchMetadata.Team.InventorySnapshot` | `repeated` | `` |  |
| 25 | `avg_stats_calibrated` | `bool` | `optional` | `` |  |
| 26 | `auto_style_criteria` | `.CDOTAMatchMetadata.Team.AutoStyleCriteria` | `repeated` | `` |  |
| 29 | `event_data` | `.CDOTAMatchMetadata.Team.EventData` | `repeated` | `` |  |
| 30 | `strange_gem_progress` | `.CDOTAMatchMetadata.Team.StrangeGemProgress` | `repeated` | `` |  |
| 31 | `hero_xp` | `uint32` | `optional` | `` |  |
| 32 | `camps_stacked` | `uint32` | `optional` | `` |  |
| 33 | `victory_prediction` | `.CDOTAMatchMetadata.Team.VictoryPrediction` | `repeated` | `` |  |
| 34 | `lane_selection_flags` | `uint32` | `optional` | `` |  |
| 35 | `rampages` | `uint32` | `optional` | `` |  |
| 36 | `triple_kills` | `uint32` | `optional` | `` |  |
| 37 | `aegis_snatched` | `uint32` | `optional` | `` |  |
| 38 | `rapiers_purchased` | `uint32` | `optional` | `` |  |
| 39 | `couriers_killed` | `uint32` | `optional` | `` |  |
| 40 | `net_worth_rank` | `uint32` | `optional` | `` |  |
| 41 | `support_gold_spent` | `uint32` | `optional` | `` |  |
| 42 | `observer_wards_placed` | `uint32` | `optional` | `` |  |
| 43 | `sentry_wards_placed` | `uint32` | `optional` | `` |  |
| 44 | `wards_dewarded` | `uint32` | `optional` | `` |  |
| 45 | `stun_duration` | `float` | `optional` | `` |  |
| 46 | `rank_mmr_boost_type` | `.EDOTAMMRBoostType` | `optional` | `` | default = k_EDOTAMMRBoostType_None |
| 48 | `contract_progress` | `.CDOTAMatchMetadata.Team.Player.ContractProgress` | `repeated` | `` |  |
| 49 | `guild_ids` | `uint32` | `repeated` | `` |  |
| 50 | `graph_hero_damage` | `float` | `repeated` | `` |  |
| 51 | `team_number` | `.DOTA_GC_TEAM` | `optional` | `` | default = DOTA_GC_TEAM_GOOD_GUYS |
| 52 | `team_slot` | `uint32` | `optional` | `` |  |
| 53 | `featured_gamemode_progress` | `.CDOTAMatchMetadata.Team.FeaturedGamemodeProgress` | `optional` | `` |  |
| 54 | `featured_hero_sticker_index` | `uint32` | `optional` | `` |  |
| 55 | `featured_hero_sticker_quality` | `uint32` | `optional` | `` |  |
| 56 | `equipped_econ_items` | `.CDOTAMatchMetadata.EconItem` | `repeated` | `` |  |
| 57 | `game_player_id` | `int32` | `optional` | `` | default = -1 |
| 58 | `player_tracked_stats` | `.CMsgTrackedStat` | `repeated` | `` |  |
| 59 | `overworld_rewards` | `.CDOTAMatchMetadata.Team.Player.OverworldRewards` | `optional` | `` |  |
| 60 | `craftworks_quest_rewards` | `.CMsgCraftworksQuestReward` | `repeated` | `` |  |
| 61 | `ad_facet_hero_id` | `int32` | `optional` | `` |  |
| 62 | `monster_hunter_rewards` | `.CMsgMonsterHunterMatchRewards.Player` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchMetadata.Team.Player.ContractProgress</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAMatchMetadata.Team.Player`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `event_id` | `uint32` | `optional` | `` |  |
| 3 | `challenge_instance_id` | `uint32` | `optional` | `` |  |
| 4 | `challenge_parameter` | `uint32` | `optional` | `` |  |
| 5 | `contract_stars` | `uint32` | `optional` | `` |  |
| 6 | `contract_slot` | `uint32` | `optional` | `` |  |
| 7 | `completed` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchMetadata.Team.Player.OverworldRewards</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAMatchMetadata.Team.Player`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `overworld_id` | `uint32` | `optional` | `` |  |
| 2 | `tokens` | `.CMsgOverworldTokenQuantity` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchMetadata.GuildChallengeProgress</code> — fields: 8; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: `CDOTAMatchMetadata`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 3 | `challenge_instance_id` | `uint32` | `optional` | `` |  |
| 4 | `challenge_parameter` | `uint32` | `optional` | `` |  |
| 5 | `challenge_timestamp` | `uint32` | `optional` | `` |  |
| 6 | `challenge_progress_at_start` | `uint32` | `optional` | `` |  |
| 7 | `challenge_progress_accumulated` | `uint32` | `optional` | `` |  |
| 8 | `individual_progress` | `.CDOTAMatchMetadata.GuildChallengeProgress.IndividualProgress` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchMetadata.GuildChallengeProgress.IndividualProgress</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAMatchMetadata.GuildChallengeProgress`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `progress` | `uint32` | `optional` | `` |  |
| 3 | `player_slot` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchMetadata.Tip</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAMatchMetadata`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `source_player_slot` | `uint32` | `optional` | `` |  |
| 2 | `target_player_slot` | `uint32` | `optional` | `` |  |
| 3 | `tip_amount` | `uint32` | `optional` | `` |  |
| 4 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |

</details>

<details>
<summary><code>CDOTAMatchPrivateMetadata</code> — fields: 3; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `teams` | `.CDOTAMatchPrivateMetadata.Team` | `repeated` | `` |  |
| 2 | `graph_win_probability` | `float` | `repeated` | `` |  |
| 3 | `string_names` | `.CDOTAMatchPrivateMetadata.StringName` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchPrivateMetadata.StringName</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAMatchPrivateMetadata`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `id` | `uint32` | `optional` | `` |  |
| 2 | `name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchPrivateMetadata.Team</code> — fields: 3; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: `CDOTAMatchPrivateMetadata`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `dota_team` | `uint32` | `optional` | `` |  |
| 2 | `players` | `.CDOTAMatchPrivateMetadata.Team.Player` | `repeated` | `` |  |
| 3 | `buildings` | `.CDOTAMatchPrivateMetadata.Team.Building` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchPrivateMetadata.Team.Player</code> — fields: 14; oneofs: 0; nested messages: 4; nested enums: 0</summary>

- Parent: `CDOTAMatchPrivateMetadata.Team`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `player_slot` | `uint32` | `optional` | `` |  |
| 3 | `position_stream` | `bytes` | `optional` | `` |  |
| 4 | `combat_segments` | `.CDOTAMatchPrivateMetadata.Team.Player.CombatSegment` | `repeated` | `` |  |
| 5 | `damage_unit_names` | `string` | `repeated` | `` |  |
| 6 | `buff_records` | `.CDOTAMatchPrivateMetadata.Team.Player.BuffRecord` | `repeated` | `` |  |
| 7 | `graph_kills` | `float` | `repeated` | `` |  |
| 8 | `graph_deaths` | `float` | `repeated` | `` |  |
| 9 | `graph_assists` | `float` | `repeated` | `` |  |
| 10 | `graph_lasthits` | `float` | `repeated` | `` |  |
| 11 | `graph_denies` | `float` | `repeated` | `` |  |
| 12 | `gold_received` | `.CDOTAMatchPrivateMetadata.Team.Player.GoldReceived` | `optional` | `` |  |
| 13 | `xp_received` | `.CDOTAMatchPrivateMetadata.Team.Player.XPReceived` | `optional` | `` |  |
| 14 | `team_number` | `.DOTA_GC_TEAM` | `optional` | `` | default = DOTA_GC_TEAM_GOOD_GUYS |
| 15 | `team_slot` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchPrivateMetadata.Team.Player.CombatSegment</code> — fields: 3; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: `CDOTAMatchPrivateMetadata.Team.Player`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `game_time` | `int32` | `optional` | `` |  |
| 2 | `damage_by_ability` | `.CDOTAMatchPrivateMetadata.Team.Player.CombatSegment.DamageByAbility` | `repeated` | `` |  |
| 3 | `healing_by_ability` | `.CDOTAMatchPrivateMetadata.Team.Player.CombatSegment.HealingByAbility` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchPrivateMetadata.Team.Player.CombatSegment.DamageByAbility</code> — fields: 3; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: `CDOTAMatchPrivateMetadata.Team.Player.CombatSegment`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ability_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `by_hero_targets` | `.CDOTAMatchPrivateMetadata.Team.Player.CombatSegment.DamageByAbility.ByHeroTarget` | `repeated` | `` |  |
| 3 | `source_unit_index` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchPrivateMetadata.Team.Player.CombatSegment.DamageByAbility.ByHeroTarget</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAMatchPrivateMetadata.Team.Player.CombatSegment.DamageByAbility`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `damage` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchPrivateMetadata.Team.Player.CombatSegment.HealingByAbility</code> — fields: 3; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: `CDOTAMatchPrivateMetadata.Team.Player.CombatSegment`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ability_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `by_hero_targets` | `.CDOTAMatchPrivateMetadata.Team.Player.CombatSegment.HealingByAbility.ByHeroTarget` | `repeated` | `` |  |
| 3 | `source_unit_index` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchPrivateMetadata.Team.Player.CombatSegment.HealingByAbility.ByHeroTarget</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAMatchPrivateMetadata.Team.Player.CombatSegment.HealingByAbility`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `healing` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchPrivateMetadata.Team.Player.BuffRecord</code> — fields: 3; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: `CDOTAMatchPrivateMetadata.Team.Player`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `buff_ability_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `by_hero_targets` | `.CDOTAMatchPrivateMetadata.Team.Player.BuffRecord.ByHeroTarget` | `repeated` | `` |  |
| 3 | `buff_modifier_name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchPrivateMetadata.Team.Player.BuffRecord.ByHeroTarget</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAMatchPrivateMetadata.Team.Player.BuffRecord`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `elapsed_duration` | `float` | `optional` | `` |  |
| 3 | `is_hidden` | `bool` | `optional` | `` |  |
| 4 | `instance_count` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchPrivateMetadata.Team.Player.GoldReceived</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAMatchPrivateMetadata.Team.Player`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `creep` | `uint32` | `optional` | `` |  |
| 2 | `heroes` | `uint32` | `optional` | `` |  |
| 3 | `bounty_runes` | `uint32` | `optional` | `` |  |
| 4 | `passive` | `uint32` | `optional` | `` |  |
| 5 | `buildings` | `uint32` | `optional` | `` |  |
| 6 | `abilities` | `uint32` | `optional` | `` |  |
| 7 | `wards` | `uint32` | `optional` | `` |  |
| 8 | `other` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchPrivateMetadata.Team.Player.XPReceived</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAMatchPrivateMetadata.Team.Player`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `creep` | `uint32` | `optional` | `` |  |
| 2 | `heroes` | `uint32` | `optional` | `` |  |
| 3 | `roshan` | `uint32` | `optional` | `` |  |
| 4 | `tome_of_knowledge` | `uint32` | `optional` | `` |  |
| 5 | `outpost` | `uint32` | `optional` | `` |  |
| 6 | `other` | `uint32` | `optional` | `` |  |
| 7 | `abilities` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMatchPrivateMetadata.Team.Building</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAMatchPrivateMetadata.Team`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `unit_name` | `string` | `optional` | `` |  |
| 2 | `position_quant_x` | `uint32` | `optional` | `` |  |
| 3 | `position_quant_y` | `uint32` | `optional` | `` |  |
| 4 | `death_time` | `float` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>EPlayerInventorySnapshotFlags</code> — values: 2</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `EPlayerInventorySnapshotFlags_HasScepter` | 1 |
| `EPlayerInventorySnapshotFlags_HasShard` | 2 |

</details>

<details>
<summary><code>CDOTAMatchMetadata.Team.KillInfo.KillType</code> — values: 5</summary>

- Parent: `CDOTAMatchMetadata.Team.KillInfo`

| Name | Number |
|---|---:|
| `KILL_TYPE_PLAYER` | 0 |
| `KILL_TYPE_TOWER` | 1 |
| `KILL_TYPE_BARRACKS` | 2 |
| `KILL_TYPE_ROSHAN` | 3 |
| `KILL_TYPE_MINIBOSS` | 4 |

</details>
