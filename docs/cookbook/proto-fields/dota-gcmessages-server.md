# dota_gcmessages_server.proto

- Module: `dota_gcmessages_server_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **14**
- Messages: **186** (top-level: 119)
- Enums: **6** (top-level: 1)

## Imports

- `steammessages.proto`
- `valveextensions.proto`
- `dota_shared_enums.proto`
- `dota_gcmessages_common.proto`
- `econ_gcmessages.proto`
- `base_gcmessages.proto`
- `network_connection.proto`
- `dota_gcmessages_common_lobby.proto`
- `dota_gcmessages_common_match_management.proto`
- `dota_gcmessages_common_overworld.proto`
- `dota_gcmessages_common_craftworks.proto`
- `dota_gcmessages_common_monster_hunter.proto`
- `gcsdk_gcmessages.proto`
- `steammessages_steamlearn.steamworkssdk.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgPoorNetworkConditions</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `detection_type` | `.EPoorNetworkConditionsType` | `optional` | `` | default = k_EPoorNetworkConditions_None |
| 2 | `players` | `.CMsgPoorNetworkConditions.Player` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgPoorNetworkConditions.Player</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgPoorNetworkConditions`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `disconnect_reason` | `.ENetworkDisconnectionReason` | `optional` | `` | default = NETWORK_DISCONNECT_INVALID |
| 3 | `num_bad_intervals` | `uint32` | `optional` | `` |  |
| 4 | `peak_loss_pct` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGameserverCrash</code> — fields: 12; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `lobby_id` | `fixed64` | `optional` | `` |  |
| 3 | `game_state` | `.DOTA_GameState` | `optional` | `` | default = DOTA_GAMERULES_STATE_INIT |
| 4 | `sentinel_save_time` | `fixed32` | `optional` | `` |  |
| 5 | `server_steam_id` | `fixed64` | `optional` | `` |  |
| 6 | `server_public_ip_addr` | `fixed32` | `optional` | `` |  |
| 7 | `server_port` | `uint32` | `optional` | `` |  |
| 8 | `server_cluster` | `uint32` | `optional` | `` |  |
| 9 | `pid` | `uint32` | `optional` | `` |  |
| 10 | `engine` | `uint32` | `optional` | `` |  |
| 11 | `custom_game_id` | `fixed64` | `optional` | `` |  |
| 12 | `tournament_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgConnectedPlayers</code> — fields: 11; oneofs: 0; nested messages: 2; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `connected_players` | `.CMsgConnectedPlayers.Player` | `repeated` | `` |  |
| 2 | `game_state` | `.DOTA_GameState` | `optional` | `` | default = DOTA_GAMERULES_STATE_INIT |
| 6 | `first_blood_happened` | `bool` | `optional` | `` |  |
| 7 | `disconnected_players` | `.CMsgConnectedPlayers.Player` | `repeated` | `` |  |
| 8 | `send_reason` | `.CMsgConnectedPlayers.SendReason` | `optional` | `` | default = INVALID |
| 10 | `poor_network_conditions` | `.CMsgPoorNetworkConditions` | `optional` | `` |  |
| 11 | `radiant_kills` | `uint32` | `optional` | `` |  |
| 12 | `dire_kills` | `uint32` | `optional` | `` |  |
| 14 | `radiant_lead` | `int32` | `optional` | `` |  |
| 15 | `building_state` | `uint32` | `optional` | `` |  |
| 16 | `player_draft` | `.CMsgConnectedPlayers.PlayerDraft` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgConnectedPlayers.Player</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgConnectedPlayers`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steam_id` | `fixed64` | `optional` | `` |  |
| 2 | `hero_id` | `int32` | `optional` | `` |  |
| 3 | `leaver_state` | `.CMsgLeaverState` | `optional` | `` |  |
| 4 | `disconnect_reason` | `.ENetworkDisconnectionReason` | `optional` | `` | default = NETWORK_DISCONNECT_INVALID |

</details>

<details>
<summary><code>CMsgConnectedPlayers.PlayerDraft</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgConnectedPlayers`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steam_id` | `fixed64` | `optional` | `` |  |
| 2 | `team` | `.DOTA_GC_TEAM` | `optional` | `` | default = DOTA_GC_TEAM_GOOD_GUYS |
| 3 | `team_slot` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGameServerInfo</code> — fields: 26; oneofs: 0; nested messages: 0; nested enums: 2</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `server_public_ip_addr` | `fixed32` | `optional` | `` |  |
| 2 | `server_private_ip_addr` | `fixed32` | `optional` | `` |  |
| 3 | `server_port` | `uint32` | `optional` | `` |  |
| 4 | `server_tv_port` | `uint32` | `optional` | `` |  |
| 5 | `server_key` | `string` | `optional` | `` |  |
| 6 | `server_hibernation` | `bool` | `optional` | `` |  |
| 7 | `server_type` | `.CMsgGameServerInfo.ServerType` | `optional` | `` | default = UNSPECIFIED |
| 8 | `server_region` | `uint32` | `optional` | `` |  |
| 9 | `server_loadavg` | `float` | `optional` | `` |  |
| 10 | `server_tv_broadcast_time` | `float` | `optional` | `` |  |
| 11 | `server_game_time` | `float` | `optional` | `` |  |
| 12 | `server_relay_connected_steam_id` | `fixed64` | `optional` | `` |  |
| 13 | `relay_slots_max` | `uint32` | `optional` | `` |  |
| 14 | `relays_connected` | `int32` | `optional` | `` |  |
| 15 | `relay_clients_connected` | `int32` | `optional` | `` |  |
| 16 | `relayed_game_server_steam_id` | `fixed64` | `optional` | `` |  |
| 17 | `parent_relay_count` | `uint32` | `optional` | `` |  |
| 18 | `tv_secret_code` | `fixed64` | `optional` | `` |  |
| 19 | `server_version` | `uint32` | `optional` | `` |  |
| 20 | `server_cluster` | `uint32` | `optional` | `` |  |
| 22 | `assigned_server_tv_port` | `uint32` | `optional` | `` |  |
| 23 | `allow_custom_games` | `.CMsgGameServerInfo.CustomGames` | `optional` | `` | default = BOTH |
| 24 | `build_version` | `uint32` | `optional` | `` |  |
| 26 | `srcds_instance` | `uint32` | `optional` | `` |  |
| 27 | `legacy_server_steamdatagram_address` | `bytes` | `optional` | `` |  |
| 28 | `dev_force_server_type` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgLeaverDetected</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steam_id` | `fixed64` | `optional` | `` |  |
| 2 | `leaver_status` | `.DOTALeaverStatus_t` | `optional` | `` | default = DOTA_LEAVER_NONE |
| 4 | `leaver_state` | `.CMsgLeaverState` | `optional` | `` |  |
| 5 | `server_cluster` | `uint32` | `optional` | `` |  |
| 6 | `disconnect_reason` | `.ENetworkDisconnectionReason` | `optional` | `` | default = NETWORK_DISCONNECT_INVALID |
| 7 | `poor_network_conditions` | `.CMsgPoorNetworkConditions` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgLeaverDetectedResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAFantasyFinalPlayerStats</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `stats` | `.CMsgDOTAFantasyPlayerStats` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAFantasyLivePlayerStats</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `stats` | `.CMsgDOTAFantasyPlayerStats` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCRealtimeStats</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `delayed` | `.CMsgDOTARealtimeGameStatsTerse` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToServerRealtimeStatsStartStop</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `delayed` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToServerUpdateSteamBroadcasting</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `active` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutGameplayStats</code> — fields: 1; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `teams` | `.CMsgSignOutGameplayStats.CTeam` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutGameplayStats.CPlayer</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSignOutGameplayStats`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steam_id` | `fixed64` | `optional` | `` |  |
| 2 | `player_slot` | `uint32` | `optional` | `` |  |
| 3 | `hero_id` | `int32` | `optional` | `` |  |
| 4 | `timed_player_stats` | `.CMatchPlayerTimedStats` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutGameplayStats.CTeam</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSignOutGameplayStats`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `is_winning_team` | `bool` | `optional` | `` |  |
| 2 | `is_radiant_team` | `bool` | `optional` | `` |  |
| 3 | `timed_team_stats` | `.CMatchTeamTimedStats` | `repeated` | `` |  |
| 4 | `players` | `.CMsgSignOutGameplayStats.CPlayer` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGameMatchSignOut</code> — fields: 30; oneofs: 0; nested messages: 6; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` | (key_field) = true |
| 2 | `duration` | `uint32` | `optional` | `` |  |
| 3 | `good_guys_win` | `bool` | `optional` | `` |  |
| 4 | `date` | `fixed32` | `optional` | `` |  |
| 6 | `teams` | `.CMsgGameMatchSignOut.CTeam` | `repeated` | `` |  |
| 8 | `tower_status` | `uint32` | `repeated` | `` |  |
| 9 | `barracks_status` | `uint32` | `repeated` | `` |  |
| 10 | `cluster` | `uint32` | `optional` | `` |  |
| 11 | `server_addr` | `string` | `optional` | `` |  |
| 12 | `first_blood_time` | `uint32` | `optional` | `` |  |
| 14 | `event_score` | `uint32` | `optional` | `` |  |
| 17 | `player_strange_count_adjustments` | `.CMsgEconPlayerStrangeCountAdjustment` | `repeated` | `` |  |
| 18 | `automatic_surrender` | `bool` | `optional` | `` |  |
| 19 | `server_version` | `uint32` | `optional` | `` |  |
| 20 | `additional_msgs` | `.CMsgGameMatchSignOut.CAdditionalSignoutMsg` | `repeated` | `` |  |
| 22 | `average_networth_delta` | `sint32` | `optional` | `` |  |
| 35 | `poor_network_conditions` | `.CMsgPoorNetworkConditions` | `optional` | `` |  |
| 36 | `social_feed_events` | `.CMsgGameMatchSignOut.CSocialFeedMatchEvent` | `repeated` | `` |  |
| 37 | `custom_game_data` | `.CMsgGameMatchSignOut.CCustomGameData` | `optional` | `` |  |
| 38 | `match_flags` | `uint32` | `optional` | `` |  |
| 39 | `team_scores` | `uint32` | `repeated` | `` |  |
| 40 | `pre_game_duration` | `uint32` | `optional` | `` |  |
| 41 | `fantasy_stats` | `.CMsgDOTAFantasyPlayerStats` | `repeated` | `` |  |
| 42 | `event_game_leaderboard_entries` | `.CMsgGameMatchSignOut.EventGameLeaderboardEntry` | `repeated` | `` |  |
| 43 | `ward_placements` | `.CMsgGameMatchSignOut.WardPlacement` | `repeated` | `` |  |
| 44 | `gameplay_stats` | `.CMsgSignOutGameplayStats` | `optional` | `` |  |
| 54 | `extra_messages` | `.CExtraMsgBlock` | `repeated` | `` |  |
| 56 | `winning_team` | `.DOTA_GC_TEAM` | `optional` | `` | default = DOTA_GC_TEAM_GOOD_GUYS |
| 57 | `normalized_win_probability_diff` | `float` | `optional` | `` |  |
| 58 | `match_tracked_stats` | `.CMsgTrackedStat` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGameMatchSignOut.CTeam</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: `CMsgGameMatchSignOut`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `players` | `.CMsgGameMatchSignOut.CTeam.CPlayer` | `repeated` | `` |  |
| 2 | `team_tracked_stats` | `.CMsgTrackedStat` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGameMatchSignOut.CTeam.CPlayer</code> — fields: 74; oneofs: 0; nested messages: 2; nested enums: 1</summary>

- Parent: `CMsgGameMatchSignOut.CTeam`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steam_id` | `fixed64` | `optional` | `` |  |
| 3 | `hero_id` | `int32` | `optional` | `` |  |
| 4 | `items` | `int32` | `repeated` | `` |  |
| 5 | `gold` | `uint32` | `optional` | `` |  |
| 6 | `kills` | `uint32` | `optional` | `` |  |
| 7 | `deaths` | `uint32` | `optional` | `` |  |
| 8 | `assists` | `uint32` | `optional` | `` |  |
| 9 | `leaver_status` | `uint32` | `optional` | `` |  |
| 10 | `last_hits` | `uint32` | `optional` | `` |  |
| 11 | `denies` | `uint32` | `optional` | `` |  |
| 12 | `gold_per_min` | `uint32` | `optional` | `` |  |
| 13 | `xp_per_minute` | `uint32` | `optional` | `` |  |
| 14 | `gold_spent` | `uint32` | `optional` | `` |  |
| 15 | `level` | `uint32` | `optional` | `` |  |
| 16 | `scaled_hero_damage` | `uint32` | `optional` | `` |  |
| 17 | `scaled_tower_damage` | `uint32` | `optional` | `` |  |
| 18 | `scaled_hero_healing` | `uint32` | `optional` | `` |  |
| 19 | `time_last_seen` | `uint32` | `optional` | `` |  |
| 20 | `support_ability_value` | `uint32` | `optional` | `` |  |
| 21 | `party_id` | `uint64` | `optional` | `` |  |
| 27 | `claimed_farm_gold` | `uint32` | `optional` | `` |  |
| 28 | `support_gold` | `uint32` | `optional` | `` |  |
| 29 | `claimed_denies` | `uint32` | `optional` | `` |  |
| 30 | `claimed_misses` | `uint32` | `optional` | `` |  |
| 31 | `misses` | `uint32` | `optional` | `` |  |
| 32 | `ability_upgrades` | `.CMatchPlayerAbilityUpgrade` | `repeated` | `` |  |
| 33 | `additional_units_inventory` | `.CMatchAdditionalUnitInventory` | `repeated` | `` |  |
| 34 | `net_worth` | `uint32` | `optional` | `` |  |
| 35 | `custom_game_data` | `.CMsgGameMatchSignOut.CTeam.CPlayer.CCustomGameData` | `optional` | `` |  |
| 36 | `match_player_flags` | `uint32` | `optional` | `` |  |
| 37 | `hero_damage` | `uint32` | `optional` | `` |  |
| 38 | `tower_damage` | `uint32` | `optional` | `` |  |
| 39 | `hero_healing` | `uint32` | `optional` | `` |  |
| 40 | `permanent_buffs` | `.CMatchPlayerPermanentBuff` | `repeated` | `` |  |
| 41 | `talent_ability_ids` | `int32` | `repeated` | `` |  |
| 42 | `hero_pick_order` | `uint32` | `optional` | `` |  |
| 43 | `hero_was_randomed` | `bool` | `optional` | `` |  |
| 45 | `lane` | `uint32` | `optional` | `` |  |
| 47 | `is_using_plus_guide` | `bool` | `optional` | `` |  |
| 48 | `hero_damage_received` | `.CMsgGameMatchSignOut.CTeam.CPlayer.HeroDamageReceived` | `repeated` | `` |  |
| 50 | `hero_was_dota_plus_suggestion` | `bool` | `optional` | `` |  |
| 51 | `seconds_dead` | `uint32` | `optional` | `` |  |
| 52 | `gold_lost_to_death` | `uint32` | `optional` | `` |  |
| 53 | `command_count` | `uint32` | `optional` | `` |  |
| 54 | `mouse_click_cast_command_count` | `uint32` | `optional` | `` |  |
| 55 | `teleports_used` | `uint32` | `optional` | `` |  |
| 56 | `cavern_crawl_preferred_map_variant` | `uint32` | `optional` | `` | default = 255 |
| 57 | `bounty_runes` | `uint32` | `optional` | `` |  |
| 58 | `outposts_captured` | `uint32` | `optional` | `` |  |
| 59 | `dewards` | `uint32` | `optional` | `` |  |
| 60 | `wards_placed` | `uint32` | `optional` | `` |  |
| 61 | `camps_stacked` | `uint32` | `optional` | `` |  |
| 62 | `player_slot` | `uint32` | `optional` | `` |  |
| 63 | `item_purchase_times` | `uint32` | `repeated` | `` |  |
| 64 | `hero_damage_dealt` | `.CMsgGameMatchSignOut.CTeam.CPlayer.HeroDamageReceived` | `repeated` | `` |  |
| 66 | `predicted_position` | `uint32` | `optional` | `` |  |
| 67 | `lane_outcomes` | `uint32` | `optional` | `` | default = 255 |
| 68 | `friendly_t1_destroyed_time` | `uint32` | `optional` | `` |  |
| 69 | `enemy_t1_destroyed_time` | `uint32` | `optional` | `` |  |
| 70 | `friendly_roshan_kills` | `uint32` | `optional` | `` |  |
| 71 | `enemy_roshan_kills` | `uint32` | `optional` | `` |  |
| 72 | `power_runes` | `uint32` | `optional` | `` |  |
| 73 | `water_runes` | `uint32` | `optional` | `` |  |
| 74 | `stun_duration` | `float` | `optional` | `` |  |
| 75 | `team_number` | `.DOTA_GC_TEAM` | `optional` | `` | default = DOTA_GC_TEAM_GOOD_GUYS |
| 76 | `team_slot` | `uint32` | `optional` | `` |  |
| 77 | `time_purchased_shard` | `uint32` | `optional` | `` |  |
| 78 | `time_purchased_aghs` | `uint32` | `optional` | `` |  |
| 79 | `ability_draft_abilities` | `int32` | `repeated` | `` |  |
| 80 | `player_tracked_stats` | `.CMsgTrackedStat` | `repeated` | `` |  |
| 81 | `predicted_rank` | `uint32` | `optional` | `` |  |
| 82 | `selected_facet` | `uint32` | `optional` | `` |  |
| 83 | `enhancement_level` | `uint32` | `optional` | `` |  |
| 84 | `disable_duration` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGameMatchSignOut.CTeam.CPlayer.CCustomGameData</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGameMatchSignOut.CTeam.CPlayer`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `dota_team` | `uint32` | `optional` | `` |  |
| 2 | `winner` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGameMatchSignOut.CTeam.CPlayer.HeroDamageReceived</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGameMatchSignOut.CTeam.CPlayer`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `pre_reduction` | `uint32` | `optional` | `` |  |
| 2 | `post_reduction` | `uint32` | `optional` | `` |  |
| 3 | `damage_type` | `.CMsgGameMatchSignOut.CTeam.CPlayer.HeroDamageType` | `optional` | `` | default = HERO_DAMAGE_PHYSICAL |

</details>

<details>
<summary><code>CMsgGameMatchSignOut.CAdditionalSignoutMsg</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGameMatchSignOut`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `id` | `uint32` | `optional` | `` |  |
| 2 | `contents` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGameMatchSignOut.CSocialFeedMatchEvent</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGameMatchSignOut`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `timestamp` | `uint32` | `optional` | `` |  |
| 3 | `event_type` | `uint32` | `optional` | `` |  |
| 4 | `game_time` | `int32` | `optional` | `` |  |
| 5 | `replay_time` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGameMatchSignOut.CCustomGameData</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGameMatchSignOut`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `publish_timestamp` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGameMatchSignOut.EventGameLeaderboardEntry</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGameMatchSignOut`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name_suffix` | `string` | `optional` | `` |  |
| 2 | `score` | `int32` | `optional` | `` |  |
| 3 | `extra_data_1` | `uint32` | `optional` | `` |  |
| 4 | `extra_data_2` | `uint32` | `optional` | `` |  |
| 5 | `extra_data_3` | `uint32` | `optional` | `` |  |
| 6 | `extra_data_4` | `uint32` | `optional` | `` |  |
| 7 | `extra_data_5` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGameMatchSignOut.WardPlacement</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGameMatchSignOut`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `team_id` | `uint32` | `optional` | `` |  |
| 3 | `placed_time` | `uint32` | `optional` | `` |  |
| 4 | `building_state` | `uint32` | `optional` | `` |  |
| 5 | `creep_state` | `uint32` | `optional` | `` |  |
| 6 | `roshan_alive` | `bool` | `optional` | `` |  |
| 7 | `position_x` | `uint32` | `optional` | `` |  |
| 8 | `position_y` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutDraftInfo</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `radiant_captain_account_id` | `uint32` | `optional` | `` |  |
| 2 | `dire_captain_account_id` | `uint32` | `optional` | `` |  |
| 3 | `picks_bans` | `.CMatchHeroSelectEvent` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutBotInfo</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `allow_cheats` | `bool` | `optional` | `` |  |
| 2 | `bot_difficulty_radiant` | `.DOTABotDifficulty` | `optional` | `` | default = BOT_DIFFICULTY_PASSIVE |
| 3 | `created_lobby` | `bool` | `optional` | `` |  |
| 5 | `bot_difficulty_dire` | `.DOTABotDifficulty` | `optional` | `` | default = BOT_DIFFICULTY_PASSIVE |

</details>

<details>
<summary><code>CMsgSignOutTextMuteInfo</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `text_mute_messages` | `.CMsgSignOutTextMuteInfo.TextMuteMessage` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutTextMuteInfo.TextMuteMessage</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSignOutTextMuteInfo`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `region` | `uint32` | `optional` | `` |  |
| 2 | `caused_text_mute` | `bool` | `optional` | `` |  |
| 3 | `chat_message` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutPlayerStats</code> — fields: 30; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `int32` | `optional` | `` |  |
| 2 | `match_id` | `uint64` | `optional` | `` |  |
| 3 | `rank` | `uint32` | `optional` | `` |  |
| 4 | `hero_id` | `int32` | `optional` | `` |  |
| 5 | `rampages` | `uint32` | `optional` | `` |  |
| 6 | `triple_kills` | `uint32` | `optional` | `` |  |
| 7 | `first_blood_claimed` | `uint32` | `optional` | `` |  |
| 8 | `first_blood_given` | `uint32` | `optional` | `` |  |
| 9 | `couriers_killed` | `uint32` | `optional` | `` |  |
| 10 | `aegises_snatched` | `uint32` | `optional` | `` |  |
| 11 | `cheeses_eaten` | `uint32` | `optional` | `` |  |
| 12 | `creeps_stacked` | `uint32` | `optional` | `` |  |
| 13 | `fight_score` | `float` | `optional` | `` |  |
| 14 | `farm_score` | `float` | `optional` | `` |  |
| 15 | `support_score` | `float` | `optional` | `` |  |
| 16 | `push_score` | `float` | `optional` | `` |  |
| 17 | `kills` | `uint32` | `optional` | `` |  |
| 18 | `deaths` | `uint32` | `optional` | `` |  |
| 19 | `assists` | `uint32` | `optional` | `` |  |
| 20 | `last_hits` | `uint32` | `optional` | `` |  |
| 21 | `denies` | `uint32` | `optional` | `` |  |
| 22 | `gpm` | `float` | `optional` | `` |  |
| 23 | `xppm` | `float` | `optional` | `` |  |
| 24 | `net_worth` | `float` | `optional` | `` |  |
| 25 | `damage` | `float` | `optional` | `` |  |
| 26 | `heals` | `float` | `optional` | `` |  |
| 27 | `rapiers_purchased` | `uint32` | `optional` | `` |  |
| 28 | `observer_wards_placed` | `uint32` | `optional` | `` |  |
| 29 | `wards_destroyed` | `uint32` | `optional` | `` |  |
| 30 | `lobby_type` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutCommunicationSummary</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `players` | `.CMsgSignOutCommunicationSummary.PlayerCommunication` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutCommunicationSummary.PlayerCommunication</code> — fields: 18; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: `CMsgSignOutCommunicationSummary`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `pings` | `uint32` | `optional` | `` |  |
| 3 | `max_pings_per_interval` | `uint32` | `optional` | `` |  |
| 4 | `teammate_pings` | `uint32` | `optional` | `` |  |
| 5 | `max_teammate_pings_per_interval` | `uint32` | `optional` | `` |  |
| 6 | `team_chat_messages` | `uint32` | `optional` | `` |  |
| 7 | `all_chat_messages` | `uint32` | `optional` | `` |  |
| 8 | `chat_wheel_messages` | `uint32` | `optional` | `` |  |
| 9 | `pauses` | `uint32` | `optional` | `` |  |
| 10 | `unpauses` | `uint32` | `optional` | `` |  |
| 11 | `lines_drawn` | `uint32` | `optional` | `` |  |
| 12 | `voice_chat_seconds` | `uint32` | `optional` | `` |  |
| 13 | `chat_mutes` | `uint32` | `optional` | `` |  |
| 14 | `voice_mutes` | `uint32` | `optional` | `` |  |
| 15 | `ping_details` | `.CMsgSignOutCommunicationSummary.PlayerCommunication.PingDetail` | `repeated` | `` |  |
| 16 | `comms_blocks_solo` | `uint32` | `optional` | `` |  |
| 17 | `comms_blocks_mass` | `uint32` | `optional` | `` |  |
| 18 | `chat_log` | `string` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutCommunicationSummary.PlayerCommunication.PingDetail</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSignOutCommunicationSummary.PlayerCommunication`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `type` | `uint32` | `optional` | `` | default = 4294967295 |
| 2 | `count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGameMatchSignoutResponse</code> — fields: 12; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `replay_salt` | `fixed32` | `optional` | `` |  |
| 5 | `leagueid` | `uint32` | `optional` | `` |  |
| 7 | `metadata_private_key` | `fixed32` | `optional` | `` |  |
| 8 | `match_details` | `.CMsgDOTAMatch` | `optional` | `` |  |
| 9 | `players_metadata` | `.CMsgGameMatchSignoutResponse.PlayerMetadata` | `repeated` | `` |  |
| 10 | `mvp_data` | `.CMvpData` | `optional` | `` |  |
| 11 | `ow_private_key` | `fixed64` | `optional` | `` |  |
| 12 | `ow_salt` | `fixed32` | `optional` | `` |  |
| 13 | `ow_replay_id` | `uint64` | `optional` | `` |  |
| 14 | `overworld_rewards` | `.CMsgOverworldMatchRewards` | `optional` | `` |  |
| 15 | `monster_hunter_rewards` | `.CMsgMonsterHunterMatchRewards` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGameMatchSignoutResponse.PlayerMetadata</code> — fields: 13; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGameMatchSignoutResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `avg_kills_x16` | `uint32` | `optional` | `` |  |
| 3 | `avg_deaths_x16` | `uint32` | `optional` | `` |  |
| 4 | `avg_assists_x16` | `uint32` | `optional` | `` |  |
| 5 | `avg_gpm_x16` | `uint32` | `optional` | `` |  |
| 6 | `avg_xpm_x16` | `uint32` | `optional` | `` |  |
| 7 | `best_kills_x16` | `uint32` | `optional` | `` |  |
| 8 | `best_assists_x16` | `uint32` | `optional` | `` |  |
| 9 | `best_gpm_x16` | `uint32` | `optional` | `` |  |
| 10 | `best_xpm_x16` | `uint32` | `optional` | `` |  |
| 11 | `win_streak` | `uint32` | `optional` | `` |  |
| 12 | `best_win_streak` | `uint32` | `optional` | `` |  |
| 13 | `games_played` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGameMatchSignOutPermissionRequest</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `server_version` | `uint32` | `optional` | `` |  |
| 2 | `local_attempt` | `uint32` | `optional` | `` |  |
| 3 | `total_attempt` | `uint32` | `optional` | `` |  |
| 4 | `seconds_waited` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGameMatchSignOutPermissionResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `permission_granted` | `bool` | `optional` | `` | default = false |
| 2 | `abandon_signout` | `bool` | `optional` | `` | default = false |
| 3 | `retry_delay_seconds` | `uint32` | `optional` | `` | default = 0 |

</details>

<details>
<summary><code>CMsgGameMatchSignOutEventGameData</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 2 | `game_name` | `string` | `optional` | `` |  |
| 3 | `map_name` | `string` | `optional` | `` |  |
| 4 | `event_game_data` | `bytes` | `optional` | `` |  |
| 5 | `start_time` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGameMatchSignOutPerfData</code> — fields: 28; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `average_frame_time` | `float` | `repeated` | `` |  |
| 2 | `max_frame_time` | `float` | `repeated` | `` |  |
| 3 | `server_average_frame_time` | `float` | `optional` | `` |  |
| 4 | `server_max_frame_time` | `float` | `optional` | `` |  |
| 5 | `average_compute_time` | `float` | `repeated` | `` |  |
| 6 | `max_compute_time` | `float` | `repeated` | `` |  |
| 7 | `average_client_tick_time` | `float` | `repeated` | `` |  |
| 8 | `max_client_tick_time` | `float` | `repeated` | `` |  |
| 9 | `average_client_simulate_time` | `float` | `repeated` | `` |  |
| 10 | `max_client_simulate_time` | `float` | `repeated` | `` |  |
| 11 | `average_output_time` | `float` | `repeated` | `` |  |
| 12 | `max_output_time` | `float` | `repeated` | `` |  |
| 13 | `average_wait_for_rendering_to_complete_time` | `float` | `repeated` | `` |  |
| 14 | `max_wait_for_rendering_to_complete_time` | `float` | `repeated` | `` |  |
| 15 | `average_swap_time` | `float` | `repeated` | `` |  |
| 16 | `max_swap_time` | `float` | `repeated` | `` |  |
| 17 | `average_frame_update_time` | `float` | `repeated` | `` |  |
| 18 | `max_frame_update_time` | `float` | `repeated` | `` |  |
| 19 | `average_idle_time` | `float` | `repeated` | `` |  |
| 20 | `max_idle_time` | `float` | `repeated` | `` |  |
| 21 | `average_input_processing_time` | `float` | `repeated` | `` |  |
| 22 | `max_input_processing_time` | `float` | `repeated` | `` |  |
| 23 | `num_slow_frames` | `uint32` | `optional` | `` |  |
| 24 | `server_average_oversleep_frame_time` | `float` | `optional` | `` |  |
| 25 | `server_max_oversleep_frame_time` | `float` | `optional` | `` |  |
| 26 | `server_average_sleep_frame_time` | `float` | `optional` | `` |  |
| 27 | `server_max_sleep_frame_time` | `float` | `optional` | `` |  |
| 28 | `num_multitick_frames` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGameMatchSignOutBanData</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_bans` | `int32` | `repeated` | `` |  |
| 2 | `hero_ban_votes` | `int32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALiveScoreboardUpdate</code> — fields: 9; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `tournament_id` | `uint32` | `optional` | `` |  |
| 2 | `tournament_game_id` | `uint32` | `optional` | `` |  |
| 3 | `duration` | `float` | `optional` | `` |  |
| 4 | `hltv_delay` | `int32` | `optional` | `` |  |
| 5 | `team_good` | `.CMsgDOTALiveScoreboardUpdate.Team` | `optional` | `` |  |
| 6 | `team_bad` | `.CMsgDOTALiveScoreboardUpdate.Team` | `optional` | `` |  |
| 7 | `roshan_respawn_timer` | `uint32` | `optional` | `` |  |
| 8 | `league_id` | `uint32` | `optional` | `` |  |
| 9 | `match_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALiveScoreboardUpdate.Team</code> — fields: 6; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: `CMsgDOTALiveScoreboardUpdate`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `players` | `.CMsgDOTALiveScoreboardUpdate.Team.Player` | `repeated` | `` |  |
| 2 | `score` | `uint32` | `optional` | `` |  |
| 3 | `tower_state` | `uint32` | `optional` | `` |  |
| 4 | `barracks_state` | `uint32` | `optional` | `` |  |
| 5 | `hero_picks` | `int32` | `repeated` | `` |  |
| 6 | `hero_bans` | `int32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALiveScoreboardUpdate.Team.Player</code> — fields: 27; oneofs: 0; nested messages: 1; nested enums: 1</summary>

- Parent: `CMsgDOTALiveScoreboardUpdate.Team`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_slot` | `uint32` | `optional` | `` |  |
| 2 | `player_name` | `string` | `optional` | `` |  |
| 3 | `hero_name` | `string` | `optional` | `` |  |
| 4 | `hero_id` | `int32` | `optional` | `` |  |
| 5 | `kills` | `uint32` | `optional` | `` |  |
| 6 | `deaths` | `uint32` | `optional` | `` |  |
| 7 | `assists` | `uint32` | `optional` | `` |  |
| 8 | `last_hits` | `uint32` | `optional` | `` |  |
| 9 | `denies` | `uint32` | `optional` | `` |  |
| 10 | `gold` | `uint32` | `optional` | `` |  |
| 11 | `level` | `uint32` | `optional` | `` |  |
| 12 | `gold_per_min` | `float` | `optional` | `` |  |
| 13 | `xp_per_min` | `float` | `optional` | `` |  |
| 14 | `ultimate_state` | `.CMsgDOTALiveScoreboardUpdate.Team.Player.DOTAUltimateState` | `optional` | `` | default = k_EDOTAUltimateStateNotLearned |
| 15 | `ultimate_cooldown` | `float` | `optional` | `` |  |
| 16 | `item0` | `int32` | `optional` | `` | default = -1 |
| 17 | `item1` | `int32` | `optional` | `` | default = -1 |
| 18 | `item2` | `int32` | `optional` | `` | default = -1 |
| 19 | `item3` | `int32` | `optional` | `` | default = -1 |
| 20 | `item4` | `int32` | `optional` | `` | default = -1 |
| 21 | `item5` | `int32` | `optional` | `` | default = -1 |
| 22 | `respawn_timer` | `uint32` | `optional` | `` |  |
| 23 | `account_id` | `uint32` | `optional` | `` |  |
| 24 | `position_x` | `float` | `optional` | `` |  |
| 25 | `position_y` | `float` | `optional` | `` |  |
| 26 | `net_worth` | `uint32` | `optional` | `` |  |
| 27 | `abilities` | `.CMsgDOTALiveScoreboardUpdate.Team.Player.HeroAbility` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALiveScoreboardUpdate.Team.Player.HeroAbility</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTALiveScoreboardUpdate.Team.Player`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ability_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `ability_level` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCRequestBatchPlayerResources</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_ids` | `uint32` | `repeated` | `` | packed = true |
| 4 | `rank_types` | `uint32` | `repeated` | `` | packed = true |
| 5 | `lobby_type` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCRequestBatchPlayerResourcesResponse</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 6 | `results` | `.CMsgServerToGCRequestBatchPlayerResourcesResponse.Result` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCRequestBatchPlayerResourcesResponse.Result</code> — fields: 14; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgServerToGCRequestBatchPlayerResourcesResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 4 | `rank` | `uint32` | `optional` | `` |  |
| 5 | `rank_calibrated` | `bool` | `optional` | `` |  |
| 6 | `low_priority` | `bool` | `optional` | `` |  |
| 7 | `is_new_player` | `bool` | `optional` | `` |  |
| 8 | `is_guide_player` | `bool` | `optional` | `` |  |
| 9 | `comm_level` | `int32` | `optional` | `` |  |
| 10 | `behavior_level` | `int32` | `optional` | `` |  |
| 11 | `wins` | `int32` | `optional` | `` |  |
| 12 | `losses` | `int32` | `optional` | `` |  |
| 13 | `smurf_category` | `int32` | `optional` | `` |  |
| 14 | `comm_score` | `int32` | `optional` | `` |  |
| 15 | `behavior_score` | `int32` | `optional` | `` |  |
| 16 | `rank_uncertainty` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAPlayerFailedToConnect</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `failed_loaders` | `fixed64` | `repeated` | `` |  |
| 2 | `abandoned_loaders` | `fixed64` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCToRelayConnect</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `source_tv_public_addr` | `uint32` | `optional` | `` |  |
| 2 | `source_tv_private_addr` | `uint32` | `optional` | `` |  |
| 3 | `source_tv_port` | `uint32` | `optional` | `` |  |
| 4 | `game_server_steam_id` | `uint64` | `optional` | `` |  |
| 5 | `parent_count` | `uint32` | `optional` | `` |  |
| 6 | `tv_unique_secret_code` | `fixed64` | `optional` | `` |  |
| 7 | `source_tv_steamid` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCGCToLANServerRelayConnect</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `relay_steamid` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCBanStatusRequest</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCBanStatusResponse</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `uint32` | `optional` | `` |  |
| 2 | `low_priority` | `bool` | `optional` | `` |  |
| 3 | `text_chat_banned` | `bool` | `optional` | `` |  |
| 4 | `voice_chat_banned` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTournamentItemEvent</code> — fields: 12; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `killer_account_id` | `fixed32` | `optional` | `` |  |
| 2 | `victim_account_id` | `fixed32` | `optional` | `` |  |
| 3 | `event_type` | `.DOTA_TournamentEvents` | `optional` | `` | default = TE_FIRST_BLOOD |
| 4 | `tv_delay` | `int32` | `optional` | `` |  |
| 5 | `dota_time` | `int32` | `optional` | `` |  |
| 6 | `replay_time` | `float` | `optional` | `` |  |
| 7 | `loot_list` | `string` | `optional` | `` |  |
| 8 | `event_team` | `uint32` | `optional` | `` |  |
| 9 | `multi_kill_count` | `uint32` | `optional` | `` |  |
| 10 | `winner_score` | `uint32` | `optional` | `` |  |
| 11 | `loser_score` | `uint32` | `optional` | `` |  |
| 12 | `hero_statues` | `.CProtoItemHeroStatue` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgTournamentItemEventResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_type` | `.DOTA_TournamentEvents` | `optional` | `` | default = TE_FIRST_BLOOD |
| 6 | `viewers_granted` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTeamFanfare</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgResponseTeamFanfare</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `fanfare_goodguys` | `uint32` | `optional` | `` |  |
| 2 | `fanfare_badguys` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAAwardEventPoints</code> — fields: 5; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `award_points` | `.CMsgDOTAAwardEventPoints.AwardPoints` | `repeated` | `` |  |
| 2 | `match_id` | `uint64` | `optional` | `` |  |
| 4 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 5 | `timestamp` | `uint32` | `optional` | `` |  |
| 6 | `audit_action` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAAwardEventPoints.AwardPoints</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAAwardEventPoints`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `points` | `int32` | `optional` | `` |  |
| 3 | `premium_points` | `int32` | `optional` | `` |  |
| 5 | `trade_ban_time` | `uint32` | `optional` | `` |  |
| 6 | `eligible_for_periodic_adjustment` | `bool` | `optional` | `` | default = false |
| 7 | `point_cap_periodic_resource_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToServerPingRequest</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `request_id` | `fixed64` | `optional` | `` |  |
| 2 | `request_time` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToServerPingResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `request_id` | `fixed64` | `optional` | `` |  |
| 2 | `request_time` | `uint64` | `optional` | `` |  |
| 3 | `cluster` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCMatchConnectionStats</code> — fields: 5; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `region_id` | `uint32` | `optional` | `` |  |
| 3 | `league_id` | `uint32` | `optional` | `` |  |
| 4 | `players` | `.CMsgServerToGCMatchConnectionStats.Player` | `repeated` | `` |  |
| 5 | `cluster_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCMatchConnectionStats.Player</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgServerToGCMatchConnectionStats`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `ip` | `fixed32` | `optional` | `` |  |
| 3 | `avg_ping_ms` | `uint32` | `optional` | `` |  |
| 5 | `packet_loss` | `float` | `optional` | `` |  |
| 6 | `ping_deviation` | `float` | `optional` | `` |  |
| 7 | `full_resends` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerGCUpdateSpectatorCount</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `spectator_count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CSerializedCombatLog</code> — fields: 3; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `version` | `uint32` | `optional` | `` |  |
| 2 | `dictionary` | `.CSerializedCombatLog.Dictionary` | `optional` | `` |  |
| 3 | `entries` | `.CMsgDOTACombatLogEntry` | `repeated` | `` |  |

</details>

<details>
<summary><code>CSerializedCombatLog.Dictionary</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: `CSerializedCombatLog`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `strings` | `.CSerializedCombatLog.Dictionary.DictString` | `repeated` | `` |  |

</details>

<details>
<summary><code>CSerializedCombatLog.Dictionary.DictString</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CSerializedCombatLog.Dictionary`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `id` | `uint32` | `required` | `` |  |
| 2 | `value` | `string` | `required` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCVictoryPredictions</code> — fields: 1; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `records` | `.CMsgServerToGCVictoryPredictions.Record` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCVictoryPredictions.PredictionItem</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgServerToGCVictoryPredictions`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_id` | `uint64` | `optional` | `` |  |
| 2 | `item_def` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCVictoryPredictions.Record</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgServerToGCVictoryPredictions`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 5 | `item_ids` | `uint64` | `repeated` | `` |  |
| 6 | `prediction_items` | `.CMsgServerToGCVictoryPredictions.PredictionItem` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCRequestStatus</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgServerToGCRequestStatus_Response</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToServerEvaluateToxicChat</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_account_id` | `uint32` | `optional` | `` |  |
| 2 | `reporter_account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCEvaluateToxicChat</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_account_id` | `uint32` | `optional` | `` |  |
| 2 | `reporter_account_id` | `uint32` | `optional` | `` |  |
| 3 | `match_id` | `fixed64` | `optional` | `` |  |
| 4 | `timestamp` | `uint32` | `repeated` | `` |  |
| 5 | `line` | `string` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCEvaluateToxicChatResponse</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_account_id` | `uint32` | `optional` | `` |  |
| 2 | `reporter_account_id` | `uint32` | `optional` | `` |  |
| 3 | `ban_reason` | `uint32` | `optional` | `` |  |
| 4 | `ban_duration` | `uint32` | `optional` | `` |  |
| 5 | `toxicity_score` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutAssassinMiniGameInfo</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `winning_players` | `fixed64` | `repeated` | `` |  |
| 2 | `losing_players` | `fixed64` | `repeated` | `` |  |
| 3 | `arcana_owners` | `fixed64` | `repeated` | `` |  |
| 4 | `assassin_won` | `bool` | `optional` | `` |  |
| 5 | `target_hero_id` | `int32` | `optional` | `` |  |
| 6 | `contract_completed` | `bool` | `optional` | `` |  |
| 7 | `contract_complete_time` | `float` | `optional` | `` |  |
| 8 | `pa_is_radiant` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCKillSummaries</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ingameevent_id` | `uint32` | `optional` | `` |  |
| 2 | `summaries` | `.CMsgServerToGCKillSummaries.KillSummary` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCKillSummaries.KillSummary</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgServerToGCKillSummaries`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `killer_hero_id` | `uint32` | `optional` | `` |  |
| 2 | `victim_hero_id` | `uint32` | `optional` | `` |  |
| 3 | `kill_count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCLockCharmTrading</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `item_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutUpdatePlayerChallenge</code> — fields: 5; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `completed` | `.CMsgSignOutUpdatePlayerChallenge.Challenge` | `repeated` | `` |  |
| 3 | `rerolled` | `.CMsgSignOutUpdatePlayerChallenge.Challenge` | `repeated` | `` |  |
| 4 | `match_id` | `uint64` | `optional` | `` |  |
| 5 | `hero_id` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutUpdatePlayerChallenge.Challenge</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSignOutUpdatePlayerChallenge`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 2 | `slot_id` | `uint32` | `optional` | `` |  |
| 3 | `sequence_id` | `uint32` | `optional` | `` |  |
| 4 | `progress` | `uint32` | `optional` | `` |  |
| 5 | `challenge_rank` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCRerollPlayerChallenge</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `reroll_msg` | `.CMsgClientToGCRerollPlayerChallenge` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSpendWager</code> — fields: 5; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `players` | `.CMsgSpendWager.Player` | `repeated` | `` |  |
| 2 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 3 | `timestamp` | `uint32` | `optional` | `` |  |
| 4 | `match_id` | `uint64` | `optional` | `` |  |
| 5 | `server_steam_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSpendWager.Player</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSpendWager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `wager` | `uint32` | `optional` | `` |  |
| 3 | `wager_token_item_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutXPCoins</code> — fields: 4; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `players` | `.CMsgSignOutXPCoins.Player` | `repeated` | `` |  |
| 2 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 3 | `match_id` | `uint64` | `optional` | `` |  |
| 4 | `timestamp` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutXPCoins.Player</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSignOutXPCoins`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `xp_gained` | `uint32` | `optional` | `` |  |
| 3 | `coins_spent` | `uint32` | `optional` | `` |  |
| 4 | `wager_token_item_id` | `uint64` | `optional` | `` |  |
| 5 | `rank_wager` | `uint32` | `optional` | `` |  |
| 6 | `wager_streak` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutBounties</code> — fields: 4; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `bounties` | `.CMsgSignOutBounties.Bounty` | `repeated` | `` |  |
| 2 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 3 | `match_id` | `uint64` | `optional` | `` |  |
| 4 | `timestamp` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutBounties.Bounty</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSignOutBounties`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `issuer_account_id` | `uint32` | `optional` | `` |  |
| 2 | `completer_account_id` | `uint32` | `optional` | `` |  |
| 3 | `target_account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutCommunityGoalProgress</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 2 | `event_increments` | `.CMsgSignOutCommunityGoalProgress.EventGoalIncrement` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutCommunityGoalProgress.EventGoalIncrement</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSignOutCommunityGoalProgress`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_goal_id` | `uint32` | `optional` | `` |  |
| 2 | `increment_amount` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCCloseCompendiumInGamePredictionVoting</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `hltv_delay` | `uint32` | `optional` | `` |  |
| 3 | `league_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCCloseCompendiumInGamePredictionVotingResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCCompendiumInGamePredictionResults</code> — fields: 4; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `results` | `.CMsgServerToGCCompendiumInGamePredictionResults.PredictionResult` | `repeated` | `` |  |
| 3 | `league_id` | `uint32` | `optional` | `` |  |
| 4 | `league_node_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCCompendiumInGamePredictionResults.PredictionResult</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgServerToGCCompendiumInGamePredictionResults`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `prediction_id` | `uint32` | `optional` | `` |  |
| 2 | `prediction_value` | `uint32` | `optional` | `` |  |
| 3 | `prediction_value_is_mask` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCCompendiumChosenInGamePredictions</code> — fields: 3; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `predictions_chosen` | `.CMsgServerToGCCompendiumChosenInGamePredictions.Prediction` | `repeated` | `` |  |
| 3 | `league_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCCompendiumChosenInGamePredictions.Prediction</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgServerToGCCompendiumChosenInGamePredictions`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `prediction_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCCompendiumInGamePredictionResults</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `results` | `.CMsgServerToGCCompendiumInGamePredictionResults` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCMatchPlayerItemPurchaseHistory</code> — fields: 3; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `mmr` | `uint32` | `optional` | `` |  |
| 3 | `players` | `.CMsgServerToGCMatchPlayerItemPurchaseHistory.Player` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCMatchPlayerItemPurchaseHistory.ItemPurchase</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgServerToGCMatchPlayerItemPurchaseHistory`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item` | `int32` | `optional` | `` | default = -1 |
| 2 | `gold` | `uint32` | `optional` | `` |  |
| 3 | `net_worth` | `uint32` | `optional` | `` |  |
| 4 | `game_time` | `uint32` | `optional` | `` |  |
| 5 | `inventory_items` | `int32` | `repeated` | `` |  |
| 7 | `talents_skilled` | `bool` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCMatchPlayerItemPurchaseHistory.Player</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgServerToGCMatchPlayerItemPurchaseHistory`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_slot` | `uint32` | `optional` | `` |  |
| 2 | `account_id` | `uint32` | `optional` | `` |  |
| 3 | `hero_id` | `int32` | `optional` | `` |  |
| 4 | `allied_hero_ids` | `int32` | `repeated` | `` |  |
| 5 | `enemy_hero_ids` | `int32` | `repeated` | `` |  |
| 6 | `item_purchases` | `.CMsgServerToGCMatchPlayerItemPurchaseHistory.ItemPurchase` | `repeated` | `` |  |
| 7 | `lane` | `uint32` | `optional` | `` |  |
| 8 | `is_winner` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCMatchPlayerNeutralItemEquipHistory</code> — fields: 2; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `players` | `.CMsgServerToGCMatchPlayerNeutralItemEquipHistory.Player` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCMatchPlayerNeutralItemEquipHistory.ItemEquip</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgServerToGCMatchPlayerNeutralItemEquipHistory`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item` | `int32` | `optional` | `` | default = -1 |
| 2 | `game_time` | `uint32` | `optional` | `` |  |
| 3 | `inventory_items` | `int32` | `repeated` | `` |  |
| 4 | `talents_skilled` | `bool` | `repeated` | `` |  |
| 5 | `available_neutral_items` | `int32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCMatchPlayerNeutralItemEquipHistory.Player</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgServerToGCMatchPlayerNeutralItemEquipHistory`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `allied_hero_ids` | `int32` | `repeated` | `` |  |
| 3 | `enemy_hero_ids` | `int32` | `repeated` | `` |  |
| 4 | `item_equips` | `.CMsgServerToGCMatchPlayerNeutralItemEquipHistory.ItemEquip` | `repeated` | `` |  |
| 5 | `is_winner` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCMatchStateHistory</code> — fields: 4; oneofs: 0; nested messages: 3; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `radiant_won` | `bool` | `optional` | `` |  |
| 3 | `mmr` | `uint32` | `optional` | `` |  |
| 4 | `match_states` | `.CMsgServerToGCMatchStateHistory.MatchState` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCMatchStateHistory.PlayerState</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgServerToGCMatchStateHistory`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `net_worth` | `uint32` | `optional` | `` |  |
| 3 | `level` | `uint32` | `optional` | `` |  |
| 4 | `deaths` | `uint32` | `optional` | `` |  |
| 5 | `respawn_time` | `uint32` | `optional` | `` |  |
| 6 | `has_buyback` | `bool` | `optional` | `` |  |
| 7 | `has_aegis` | `bool` | `optional` | `` |  |
| 8 | `has_rapier` | `bool` | `optional` | `` |  |
| 9 | `distance` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCMatchStateHistory.TeamState</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgServerToGCMatchStateHistory`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team` | `uint32` | `optional` | `` |  |
| 2 | `player_states` | `.CMsgServerToGCMatchStateHistory.PlayerState` | `repeated` | `` | (steamml_max_entries) = 5 |
| 3 | `tower_health_pct` | `uint32` | `repeated` | `` | (steamml_max_entries) = 11 |
| 4 | `barracks_health_pct` | `uint32` | `repeated` | `` | (steamml_max_entries) = 3 |
| 5 | `ancient_health_pct` | `uint32` | `optional` | `` |  |
| 6 | `glyph_cooldown` | `uint32` | `optional` | `` |  |
| 7 | `kills` | `uint32` | `optional` | `` |  |
| 8 | `creep_distance_safe` | `uint32` | `optional` | `` |  |
| 9 | `creep_distance_mid` | `uint32` | `optional` | `` |  |
| 10 | `creep_distance_off` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCMatchStateHistory.MatchState</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgServerToGCMatchStateHistory`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `game_time` | `uint32` | `optional` | `` |  |
| 2 | `radiant_state` | `.CMsgServerToGCMatchStateHistory.TeamState` | `optional` | `` |  |
| 3 | `dire_state` | `.CMsgServerToGCMatchStateHistory.TeamState` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgMatchStateSteamMLEntry</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_state` | `.CMsgServerToGCMatchStateHistory.MatchState` | `optional` | `` |  |
| 2 | `mmr` | `uint32` | `optional` | `` |  |
| 3 | `radiant_won` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgLaneSelectionSteamMLEntry</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_ids` | `int32` | `repeated` | `` | (steamml_max_entries) = 10 |
| 2 | `lanes` | `uint32` | `repeated` | `` | (steamml_max_entries) = 6 |

</details>

<details>
<summary><code>CMsgAbilitySelectionSteamMLEntry</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `mmr` | `uint32` | `optional` | `` |  |
| 2 | `hero_id` | `int32` | `optional` | `` |  |
| 3 | `enemy_hero_ids` | `int32` | `repeated` | `` | (steamml_max_entries) = 4 |
| 4 | `lane` | `uint32` | `optional` | `` |  |
| 5 | `abilities` | `int32` | `repeated` | `` | (steamml_max_entries) = 25 |
| 6 | `selected_ability` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CMsgItemPurchasePregameSteamMLEntry</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `mmr` | `uint32` | `optional` | `` |  |
| 2 | `lane` | `uint32` | `optional` | `` |  |
| 3 | `balance` | `float` | `optional` | `` |  |
| 4 | `hero_id` | `int32` | `optional` | `` |  |
| 5 | `allied_hero_ids` | `int32` | `repeated` | `` | (steamml_max_entries) = 4 |
| 6 | `enemy_hero_ids` | `int32` | `repeated` | `` | (steamml_max_entries) = 5 |
| 7 | `items` | `int32` | `repeated` | `` | (steamml_max_entries) = 9 |

</details>

<details>
<summary><code>CMsgItemPurchaseSteamMLEntry</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `mmr` | `uint32` | `optional` | `` |  |
| 2 | `lane` | `uint32` | `optional` | `` |  |
| 3 | `hero_id` | `int32` | `optional` | `` |  |
| 4 | `allied_hero_ids` | `int32` | `repeated` | `` | (steamml_max_entries) = 4 |
| 5 | `enemy_hero_ids` | `int32` | `repeated` | `` | (steamml_max_entries) = 5 |
| 6 | `items` | `int32` | `repeated` | `` | (steamml_max_entries) = 20 |
| 7 | `items_to_be_purchased` | `int32` | `repeated` | `` | (steamml_max_entries) = 20 |

</details>

<details>
<summary><code>CMsgItemPurchaseSequenceSteamMLEntry</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `mmr` | `uint32` | `optional` | `` |  |
| 2 | `lane` | `uint32` | `optional` | `` |  |
| 3 | `hero_id` | `int32` | `optional` | `` |  |
| 4 | `allied_hero_ids` | `int32` | `repeated` | `` | (steamml_max_entries) = 4 |
| 5 | `enemy_hero_ids` | `int32` | `repeated` | `` | (steamml_max_entries) = 5 |
| 6 | `items` | `int32` | `repeated` | `` | (steamml_max_entries) = 20 |
| 7 | `item_to_be_purchased` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CMsgServerToGCCavernCrawlIsHeroActive</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |
| 2 | `account_id` | `uint32` | `optional` | `` |  |
| 3 | `preferred_map_variant` | `uint32` | `optional` | `` | default = 255 |
| 4 | `hero_id` | `int32` | `optional` | `` |  |
| 5 | `turbo_mode` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCPlayerChallengeHistory</code> — fields: 3; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `average_rank` | `uint32` | `optional` | `` |  |
| 3 | `challenge_records` | `.CMsgServerToGCPlayerChallengeHistory.PlayerChallenge` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCPlayerChallengeHistory.PlayerChallenge</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgServerToGCPlayerChallengeHistory`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `challenge_type` | `.EPlayerChallengeHistoryType` | `optional` | `` | default = k_EPlayerChallengeHistoryType_Invalid |
| 3 | `challenge_id1` | `uint32` | `optional` | `` |  |
| 4 | `challenge_id2` | `uint32` | `optional` | `` |  |
| 5 | `progress_value_start` | `uint32` | `optional` | `` |  |
| 6 | `progress_value_end` | `uint32` | `optional` | `` |  |
| 7 | `team_won` | `bool` | `optional` | `` |  |
| 8 | `audit_data` | `uint64` | `optional` | `` |  |
| 9 | `hero_id` | `int32` | `optional` | `` |  |
| 10 | `rank_completed` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCCavernCrawlIsHeroActiveResponse</code> — fields: 5; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `bool` | `optional` | `` |  |
| 2 | `potential_winnings` | `uint32` | `optional` | `` |  |
| 3 | `map_results` | `.CMsgServerToGCCavernCrawlIsHeroActiveResponse.MapResults` | `repeated` | `` |  |
| 4 | `potential_plus_shard_winnings` | `uint32` | `optional` | `` |  |
| 5 | `map_variant` | `uint32` | `optional` | `` | default = 255 |

</details>

<details>
<summary><code>CMsgServerToGCCavernCrawlIsHeroActiveResponse.MapResults</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgServerToGCCavernCrawlIsHeroActiveResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `path_id_completed` | `uint32` | `optional` | `` | default = 255 |
| 2 | `room_id_claimed` | `uint32` | `optional` | `` | default = 255 |

</details>

<details>
<summary><code>CMsgNeutralItemStats</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `neutral_items` | `.CMsgNeutralItemStats.NeutralItem` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgNeutralItemStats.NeutralItem</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgNeutralItemStats`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `time_dropped` | `uint32` | `optional` | `` |  |
| 3 | `team` | `uint32` | `optional` | `` |  |
| 4 | `time_last_equipped` | `uint32` | `optional` | `` |  |
| 5 | `time_last_unequipped` | `uint32` | `optional` | `` |  |
| 6 | `duration_equipped` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToServerLobbyHeroBanRates</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ban_data` | `.CMsgGCToServerLobbyHeroBanRates.HeroBanEntry` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCToServerLobbyHeroBanRates.HeroBanEntry</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToServerLobbyHeroBanRates`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `ban_count` | `uint32` | `optional` | `` |  |
| 3 | `pick_count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutGuildContractProgress</code> — fields: 1; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_contracts` | `.CMsgSignOutGuildContractProgress.PlayerContract` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutGuildContractProgress.CompletedGuildEventContracts</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSignOutGuildContractProgress`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `event_id` | `uint32` | `optional` | `` |  |
| 3 | `contracts` | `uint64` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutGuildContractProgress.PlayerContract</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSignOutGuildContractProgress`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `completed_contracts` | `.CMsgSignOutGuildContractProgress.CompletedGuildEventContracts` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutGuildChallengeProgress</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_challenges_progresses` | `.CMsgSignOutGuildChallengeProgress.ChallengeProgress` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutGuildChallengeProgress.ChallengeProgress</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSignOutGuildChallengeProgress`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `event_id` | `uint32` | `optional` | `` |  |
| 3 | `challenge_instance_id` | `uint32` | `optional` | `` |  |
| 4 | `challenge_instance_timestamp` | `uint32` | `optional` | `` |  |
| 5 | `challenge_period_serial` | `uint32` | `optional` | `` |  |
| 6 | `progress` | `uint32` | `optional` | `` |  |
| 7 | `challenge_parameter` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutMVPStats</code> — fields: 5; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `game_mode` | `uint32` | `optional` | `` |  |
| 3 | `winning_team` | `uint32` | `optional` | `` |  |
| 4 | `game_time` | `float` | `optional` | `` |  |
| 5 | `players` | `.CMsgSignOutMVPStats.Player` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutMVPStats.Player</code> — fields: 25; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: `CMsgSignOutMVPStats`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team_id` | `uint32` | `optional` | `` |  |
| 2 | `team_networth_rank` | `uint32` | `optional` | `` |  |
| 3 | `account_id` | `uint32` | `optional` | `` |  |
| 4 | `hero_id` | `int32` | `optional` | `` |  |
| 5 | `role` | `uint32` | `optional` | `` |  |
| 6 | `kills` | `int32` | `optional` | `` |  |
| 7 | `deaths` | `int32` | `optional` | `` |  |
| 8 | `assists` | `int32` | `optional` | `` |  |
| 9 | `xp` | `int32` | `optional` | `` |  |
| 10 | `net_worth` | `int32` | `optional` | `` |  |
| 12 | `support_gold_spent` | `int32` | `optional` | `` |  |
| 13 | `wards_placed` | `int32` | `optional` | `` |  |
| 14 | `wards_spotted_for_dewarding` | `int32` | `optional` | `` |  |
| 15 | `camps_stacked` | `int32` | `optional` | `` |  |
| 16 | `last_hits` | `int32` | `optional` | `` |  |
| 17 | `denies` | `int32` | `optional` | `` |  |
| 19 | `building_damage` | `int32` | `optional` | `` |  |
| 20 | `other_damage` | `int32` | `optional` | `` |  |
| 26 | `triple_kills` | `int32` | `optional` | `` |  |
| 28 | `rampages` | `int32` | `optional` | `` |  |
| 31 | `first_blood` | `int32` | `optional` | `` |  |
| 32 | `player_slot` | `uint32` | `optional` | `` |  |
| 33 | `rank` | `uint32` | `optional` | `` |  |
| 34 | `kill_eater_events` | `.CMsgSignOutMVPStats.Player.KillEaterEvent` | `repeated` | `` |  |
| 35 | `highest_killstreak` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutMVPStats.Player.KillEaterEvent</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSignOutMVPStats.Player`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_type` | `uint32` | `required` | `` |  |
| 2 | `amount` | `uint32` | `required` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCGetGuildContracts</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_ids` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCGetGuildContractsResponse</code> — fields: 1; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_contracts` | `.CMsgServerToGCGetGuildContractsResponse.Player` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCGetGuildContractsResponse.ContractDetails</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgServerToGCGetGuildContractsResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `contract_id` | `uint64` | `optional` | `` |  |
| 2 | `challenge_instance_id` | `uint32` | `optional` | `` |  |
| 3 | `challenge_parameter` | `uint32` | `optional` | `` |  |
| 4 | `contract_stars` | `uint32` | `optional` | `` |  |
| 5 | `contract_slot` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCGetGuildContractsResponse.Player</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgServerToGCGetGuildContractsResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `guild_id` | `uint32` | `optional` | `` |  |
| 3 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 4 | `contracts` | `.CMsgServerToGCGetGuildContractsResponse.ContractDetails` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgMatchDiretideCandy</code> — fields: 2; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_candy_data` | `.CMsgMatchDiretideCandy.PlayerCandy` | `repeated` | `` |  |
| 2 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |

</details>

<details>
<summary><code>CMsgMatchDiretideCandy.CandyDetails</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgMatchDiretideCandy`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `amount` | `uint32` | `optional` | `` |  |
| 2 | `audit` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgMatchDiretideCandy.PlayerCandy</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgMatchDiretideCandy`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 3 | `candy_amount` | `uint32` | `optional` | `` |  |
| 4 | `consumes_periodic_resource` | `bool` | `optional` | `` |  |
| 5 | `candy_breakdown` | `.CMsgMatchDiretideCandy.CandyDetails` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCToServerCheerData</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `cheer_types` | `.CMsgGCToServerCheerData.CheerTypeCount` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCToServerCheerData.CheerTypeCount</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToServerCheerData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `cheer_type` | `uint32` | `optional` | `` |  |
| 2 | `cheer_count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgCheerConfig</code> — fields: 18; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `cheers_enabled` | `bool` | `optional` | `` |  |
| 2 | `is_valid_league_id` | `bool` | `optional` | `` |  |
| 3 | `window_duration` | `float` | `optional` | `` |  |
| 4 | `window_bucket_count` | `uint32` | `optional` | `` |  |
| 6 | `crowd_level_push_time` | `float` | `optional` | `` |  |
| 10 | `crowd_level_low` | `uint32` | `optional` | `` |  |
| 11 | `crowd_level_medium` | `uint32` | `optional` | `` |  |
| 12 | `crowd_level_high` | `uint32` | `optional` | `` |  |
| 13 | `cheer_scale_start` | `float` | `optional` | `` |  |
| 14 | `cheer_scale_speed` | `float` | `optional` | `` |  |
| 15 | `cheer_scale_push_mark` | `uint32` | `optional` | `` |  |
| 16 | `cheer_scale_pull_mark` | `uint32` | `optional` | `` |  |
| 17 | `cheer_scale_pct_of_max_cps_clamp` | `float` | `optional` | `` |  |
| 18 | `cheer_factor_bronze` | `float` | `optional` | `` |  |
| 19 | `cheer_factor_silver` | `float` | `optional` | `` |  |
| 20 | `cheer_factor_gold` | `float` | `optional` | `` |  |
| 21 | `cheer_scale_dampener_value` | `float` | `optional` | `` |  |
| 22 | `cheer_scale_dampener_lerp_time` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToServerCheerConfig</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `cheer_config` | `.CMsgCheerConfig` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCGetCheerConfig</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCGetCheerConfigResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `cheer_config` | `.CMsgCheerConfig` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToServerCheerScalesOverride</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `scales` | `float` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCToServerGetCheerState</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgCheerTypeState</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `cheer_counts` | `uint32` | `repeated` | `` |  |
| 2 | `max_per_second` | `float` | `optional` | `` |  |
| 3 | `cheer_scale` | `float` | `optional` | `` |  |
| 4 | `override_scale` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgCheerState</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `cheer_types` | `.CMsgCheerTypeState` | `repeated` | `` |  |
| 2 | `radiant_crowd_level` | `uint32` | `optional` | `` |  |
| 3 | `dire_crowd_level` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCReportCheerState</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `cheer_config` | `.CMsgCheerConfig` | `optional` | `` |  |
| 2 | `cheer_state` | `.CMsgCheerState` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCGetStickerHeroes</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_ids` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCGetStickerHeroesResponse</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `players` | `.CMsgServerToGCGetStickerHeroesResponse.Player` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCGetStickerHeroesResponse.Player</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgServerToGCGetStickerHeroesResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `stickers` | `.CMsgStickerHeroes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearnMatchInfo</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `average_mmr` | `uint32` | `optional` | `` |  |
| 2 | `radiant_won` | `bool` | `optional` | `` |  |
| 3 | `duration` | `uint32` | `optional` | `` |  |
| 4 | `game_mode` | `uint32` | `optional` | `` |  |
| 5 | `lobby_type` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearnMatchInfoPlayer</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `average_mmr` | `uint32` | `optional` | `` |  |
| 2 | `team_won` | `bool` | `optional` | `` |  |
| 3 | `duration` | `uint32` | `optional` | `` |  |
| 4 | `game_mode` | `uint32` | `optional` | `` |  |
| 5 | `lobby_type` | `uint32` | `optional` | `` |  |
| 6 | `player_mmr` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearnMatchInfoTeam</code> — fields: 3; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `radiant_players` | `.CMsgSteamLearnMatchInfoTeam.Player` | `repeated` | `` | (steamlearn_count) = 5 |
| 2 | `dire_players` | `.CMsgSteamLearnMatchInfoTeam.Player` | `repeated` | `` | (steamlearn_count) = 5 |
| 3 | `radiant_team_won` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearnMatchInfoTeam.Player</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamLearnMatchInfoTeam`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `prematch_mmr` | `uint32` | `optional` | `` |  |
| 2 | `prematch_rank_uncertainty` | `uint32` | `optional` | `` |  |
| 3 | `prematch_behavior_score` | `uint32` | `optional` | `` |  |
| 4 | `prematch_comm_score` | `uint32` | `optional` | `` |  |
| 5 | `num_players_in_party` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearnMatchHeroesV3</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `radiant_hero_ids` | `int32` | `repeated` | `` | (steamlearn_count) = 5 |
| 2 | `dire_hero_ids` | `int32` | `repeated` | `` | (steamlearn_count) = 5 |
| 3 | `radiant_lanes` | `uint32` | `repeated` | `` | (steamlearn_count) = 5 |
| 4 | `dire_lanes` | `uint32` | `repeated` | `` | (steamlearn_count) = 5 |
| 5 | `radiant_hero_facets` | `uint32` | `repeated` | `` | (steamlearn_count) = 5 |
| 6 | `dire_hero_facets` | `uint32` | `repeated` | `` | (steamlearn_count) = 5 |
| 7 | `radiant_positions` | `uint32` | `repeated` | `` | (steamlearn_count) = 5 |
| 8 | `dire_positions` | `uint32` | `repeated` | `` | (steamlearn_count) = 5 |

</details>

<details>
<summary><code>CMsgSteamLearnMatchHeroesV4</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `radiant_hero_ids` | `int32` | `repeated` | `` | (steamlearn_count) = 5 |
| 2 | `dire_hero_ids` | `int32` | `repeated` | `` | (steamlearn_count) = 5 |
| 3 | `radiant_lanes` | `uint32` | `repeated` | `` | (steamlearn_count) = 5 |
| 4 | `dire_lanes` | `uint32` | `repeated` | `` | (steamlearn_count) = 5 |
| 5 | `radiant_positions` | `uint32` | `repeated` | `` | (steamlearn_count) = 5 |
| 6 | `dire_positions` | `uint32` | `repeated` | `` | (steamlearn_count) = 5 |

</details>

<details>
<summary><code>CMsgSteamLearnMatchHeroV6</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `facet` | `uint32` | `optional` | `` |  |
| 3 | `hero_and_facet` | `uint32` | `optional` | `` |  |
| 4 | `lane` | `uint32` | `optional` | `` |  |
| 5 | `position` | `uint32` | `optional` | `` |  |
| 6 | `allied_hero_and_facet` | `uint32` | `repeated` | `` | (steamlearn_count) = 4 |
| 7 | `enemy_hero_and_facet` | `uint32` | `repeated` | `` | (steamlearn_count) = 5 |

</details>

<details>
<summary><code>CMsgSteamLearnMatchHeroV8</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `lane` | `uint32` | `optional` | `` |  |
| 3 | `position` | `uint32` | `optional` | `` |  |
| 4 | `allied_heroes` | `uint32` | `repeated` | `` | (steamlearn_count) = 4 |
| 5 | `enemy_heroes` | `uint32` | `repeated` | `` | (steamlearn_count) = 5 |

</details>

<details>
<summary><code>CMsgSteamLearnPlayerTimedStats</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `stat_buckets` | `.CMsgSteamLearnPlayerTimedStats.StatBucket` | `repeated` | `` | (steamlearn_count) = 90 |

</details>

<details>
<summary><code>CMsgSteamLearnPlayerTimedStats.StatBucket</code> — fields: 12; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamLearnPlayerTimedStats`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `game_time` | `float` | `optional` | `` |  |
| 2 | `kills` | `uint32` | `optional` | `` |  |
| 3 | `deaths` | `uint32` | `optional` | `` |  |
| 4 | `assists` | `uint32` | `optional` | `` |  |
| 5 | `experience` | `uint32` | `optional` | `` |  |
| 6 | `last_hits` | `uint32` | `optional` | `` |  |
| 7 | `denies` | `uint32` | `optional` | `` |  |
| 8 | `net_worth` | `uint32` | `optional` | `` |  |
| 9 | `idle_time` | `float` | `optional` | `` |  |
| 10 | `commands_issued` | `uint32` | `optional` | `` |  |
| 11 | `sentry_wards_placed` | `uint32` | `optional` | `` |  |
| 12 | `observer_wards_placed` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearnMatchStateV5</code> — fields: 3; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `game_time` | `float` | `optional` | `` |  |
| 2 | `radiant_state` | `.CMsgSteamLearnMatchStateV5.TeamState` | `optional` | `` |  |
| 3 | `dire_state` | `.CMsgSteamLearnMatchStateV5.TeamState` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearnMatchStateV5.PlayerState</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamLearnMatchStateV5`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `net_worth` | `uint32` | `optional` | `` |  |
| 3 | `level` | `uint32` | `optional` | `` |  |
| 4 | `deaths` | `uint32` | `optional` | `` |  |
| 5 | `respawn_time` | `uint32` | `optional` | `` |  |
| 6 | `has_buyback` | `bool` | `optional` | `` |  |
| 7 | `has_aegis` | `bool` | `optional` | `` |  |
| 8 | `has_rapier` | `bool` | `optional` | `` |  |
| 9 | `distance` | `uint32` | `optional` | `` |  |
| 10 | `hero_facet` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearnMatchStateV5.TeamState</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamLearnMatchStateV5`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team` | `uint32` | `optional` | `` |  |
| 2 | `player_states` | `.CMsgSteamLearnMatchStateV5.PlayerState` | `repeated` | `` | (steamlearn_count) = 5 |
| 3 | `tower_health_pct` | `uint32` | `repeated` | `` | (steamlearn_count) = 11 |
| 4 | `barracks_health_pct` | `uint32` | `repeated` | `` | (steamlearn_count) = 6 |
| 5 | `ancient_health_pct` | `uint32` | `optional` | `` |  |
| 6 | `glyph_cooldown` | `uint32` | `optional` | `` |  |
| 7 | `kills` | `uint32` | `optional` | `` |  |
| 8 | `creep_distance_safe` | `uint32` | `optional` | `` |  |
| 9 | `creep_distance_mid` | `uint32` | `optional` | `` |  |
| 10 | `creep_distance_off` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearnItemPurchaseV7</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `purchase_history` | `int32` | `repeated` | `` | (steamlearn_count) = 50 |

</details>

<details>
<summary><code>CMsgSteamLearnPreGameItemPurchases</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_ids` | `int32` | `repeated` | `` | (steamlearn_count) = 10 |
| 2 | `is_radiant_team` | `uint32` | `optional` | `` |  |
| 3 | `is_using_dota_plus` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearnPreGameItemPurchase</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `purchase_history` | `int32` | `repeated` | `` | (steamlearn_count) = 10 |
| 2 | `item_id` | `int32` | `optional` | `` | default = -1, (steamlearn_count) = 10 |

</details>

<details>
<summary><code>CMsgSteamLearnNeutralItemPurchaseV4</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `tier` | `uint32` | `optional` | `` |  |
| 2 | `trinket_options` | `int32` | `repeated` | `` | (steamlearn_count) = 4 |
| 3 | `enhancement_options` | `int32` | `repeated` | `` | (steamlearn_count) = 4 |
| 4 | `trinket_id` | `int32` | `optional` | `` | default = -1 |
| 5 | `enhancement_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CMsgSteamLearnAbilitySkill</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ability_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `skilled_abilities` | `int32` | `repeated` | `` | (steamlearn_count) = 30 |
| 3 | `game_time` | `float` | `optional` | `` |  |
| 4 | `is_using_dota_plus` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearnWardPlacement</code> — fields: 3; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ward_loc` | `.CMsgSteamLearnWardPlacement.Location` | `optional` | `` |  |
| 2 | `existing_ward_locs` | `.CMsgSteamLearnWardPlacement.Location` | `repeated` | `` | (steamlearn_count) = 6 |
| 3 | `team` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearnWardPlacement.Location</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamLearnWardPlacement`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `x` | `float` | `optional` | `` |  |
| 2 | `y` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearnPlayerMatchState</code> — fields: 12; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `net_worth` | `uint32` | `optional` | `` |  |
| 2 | `level` | `uint32` | `optional` | `` |  |
| 3 | `deaths` | `uint32` | `optional` | `` |  |
| 4 | `respawn_time` | `uint32` | `optional` | `` |  |
| 5 | `has_buyback` | `bool` | `optional` | `` |  |
| 6 | `has_aegis` | `bool` | `optional` | `` |  |
| 7 | `has_rapier` | `bool` | `optional` | `` |  |
| 8 | `team_net_worth` | `uint32` | `optional` | `` |  |
| 9 | `enemy_team_net_worth` | `uint32` | `optional` | `` |  |
| 10 | `team_kills` | `uint32` | `optional` | `` |  |
| 11 | `enemy_team_kills` | `uint32` | `optional` | `` |  |
| 12 | `game_time` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutMuertaMinigame</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_game_data` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutMapStats</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `players` | `.CMsgSignOutMapStats.Player` | `repeated` | `` |  |
| 2 | `global_stats` | `.CMsgMapStatsSnapshot` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutMapStats.Player</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSignOutMapStats`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `personal_stats` | `.CMsgMapStatsSnapshot` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCNewBloomGift</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `defindex` | `uint32` | `optional` | `` |  |
| 2 | `gifter_account_id` | `uint32` | `optional` | `` |  |
| 3 | `target_account_ids` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCNewBloomGiftResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.ENewBloomGiftingResponse` | `optional` | `` | default = kENewBloomGifting_UnknownFailure |
| 2 | `received_account_ids` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutOverworld</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `players` | `.CMsgSignOutOverworld.Player` | `repeated` | `` |  |
| 2 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |

</details>

<details>
<summary><code>CMsgSignOutOverworld.Player</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSignOutOverworld`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `overworld_id` | `uint32` | `optional` | `` |  |
| 3 | `desired_token_rewards` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutCraftworks</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `players` | `.CMsgSignOutCraftworks.Player` | `repeated` | `` |  |
| 2 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |

</details>

<details>
<summary><code>CMsgSignOutCraftworks.Player</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSignOutCraftworks`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `components` | `.CMsgCraftworksComponents` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSignOutMonsterHunter</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `players` | `.CMsgSignOutMonsterHunter.Player` | `repeated` | `` |  |
| 2 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |

</details>

<details>
<summary><code>CMsgSignOutMonsterHunter.Player</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSignOutMonsterHunter`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `investigation_game_state` | `.CMsgMonsterHunterInvestigationGameState` | `optional` | `` |  |
| 3 | `codex_update_data` | `.CMsgMonsterHunterCodexUpdateData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCWarningLowServerFramerate</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `match_id` | `uint64` | `optional` | `` |  |
| 2 | `ticks_per_interval_average` | `float` | `optional` | `` |  |
| 3 | `custom_game_id` | `uint64` | `optional` | `` |  |
| 4 | `bot_script_id_radiant` | `uint64` | `optional` | `` |  |
| 5 | `bot_script_id_dire` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerToGCWarningInvalidBotAbilityUsage</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `description` | `string` | `optional` | `` |  |
| 2 | `unit_name` | `string` | `optional` | `` |  |
| 3 | `ability_name` | `string` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>EPoorNetworkConditionsType</code> — values: 4</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EPoorNetworkConditions_None` | 0 |
| `k_EPoorNetworkConditions_Unknown` | 1 |
| `k_EPoorNetworkConditions_MassDisconnect` | 2 |
| `k_EPoorNetworkConditions_ExcessBadQosIntervals` | 3 |

</details>

<details>
<summary><code>CMsgConnectedPlayers.SendReason</code> — values: 12</summary>

- Parent: `CMsgConnectedPlayers`

| Name | Number |
|---|---:|
| `INVALID` | 0 |
| `HEARTBEAT` | 1 |
| `GAME_STATE` | 2 |
| `FIRST_BLOOD` | 3 |
| `PLAYER_CONNECTED` | 4 |
| `PLAYER_HERO` | 5 |
| `PLAYER_DISCONNECTED_CONSEQUENCES` | 6 |
| `PLAYER_DISCONNECTED_NOCONSEQUENCES` | 7 |
| `GAMESTATE_TIMEOUT` | 10 |
| `MASS_DISCONNECT` | 11 |
| `KILLS` | 13 |
| `BUILDING_STATE` | 14 |

</details>

<details>
<summary><code>CMsgGameServerInfo.ServerType</code> — values: 6</summary>

- Parent: `CMsgGameServerInfo`

| Name | Number |
|---|---:|
| `UNSPECIFIED` | 0 |
| `GAME` | 1 |
| `PROXY` | 2 |
| `DOTA_ONLY` | 4 |
| `CUSTOM_GAME_ONLY` | 5 |
| `EVENT_GAME_ONLY` | 6 |

</details>

<details>
<summary><code>CMsgGameServerInfo.CustomGames</code> — values: 4</summary>

- Parent: `CMsgGameServerInfo`

| Name | Number |
|---|---:|
| `BOTH` | 0 |
| `NONE` | 1 |
| `ONLY` | 2 |
| `EVENT` | 3 |

</details>

<details>
<summary><code>CMsgGameMatchSignOut.CTeam.CPlayer.HeroDamageType</code> — values: 3</summary>

- Parent: `CMsgGameMatchSignOut.CTeam.CPlayer`

| Name | Number |
|---|---:|
| `HERO_DAMAGE_PHYSICAL` | 0 |
| `HERO_DAMAGE_MAGICAL` | 1 |
| `HERO_DAMAGE_PURE` | 2 |

</details>

<details>
<summary><code>CMsgDOTALiveScoreboardUpdate.Team.Player.DOTAUltimateState</code> — values: 4</summary>

- Parent: `CMsgDOTALiveScoreboardUpdate.Team.Player`

| Name | Number |
|---|---:|
| `k_EDOTAUltimateStateNotLearned` | 0 |
| `k_EDOTAUltimateStateCooldown` | 1 |
| `k_EDOTAUltimateStateNeedsMana` | 2 |
| `k_EDOTAUltimateStateReady` | 3 |

</details>
