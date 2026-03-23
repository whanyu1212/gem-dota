# dota_gcmessages_common_match_management.proto

- Module: `dota_gcmessages_common_match_management_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **3**
- Messages: **15** (top-level: 11)
- Enums: **9** (top-level: 7)

## Imports

- `steammessages.proto`
- `gcsdk_gcmessages.proto`
- `dota_shared_enums.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CSODOTAPartyMember</code> — fields: 15; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `is_coach` | `bool` | `optional` | `` |  |
| 4 | `region_ping_codes` | `uint32` | `repeated` | `` | packed = true |
| 5 | `region_ping_times` | `uint32` | `repeated` | `` | packed = true |
| 6 | `region_ping_failed_bitmask` | `uint32` | `optional` | `` |  |
| 7 | `tourney_skill_level` | `uint32` | `optional` | `` |  |
| 8 | `tourney_buyin` | `uint32` | `optional` | `` |  |
| 9 | `tourney_prevent_until` | `uint32` | `optional` | `` |  |
| 10 | `is_plus_subscriber` | `bool` | `optional` | `` |  |
| 11 | `lane_selection_flags` | `uint32` | `optional` | `` |  |
| 12 | `joined_from_partyfinder` | `bool` | `optional` | `` |  |
| 13 | `mm_data_valid` | `bool` | `optional` | `` |  |
| 14 | `high_priority_disabled` | `bool` | `optional` | `` |  |
| 15 | `has_hp_resource` | `bool` | `optional` | `` |  |
| 16 | `is_steam_china` | `bool` | `optional` | `` |  |
| 17 | `banned_hero_ids` | `int32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CSODOTAParty</code> — fields: 56; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `party_id` | `uint64` | `optional` | `` | (key_field) = true |
| 2 | `leader_id` | `fixed64` | `optional` | `` |  |
| 3 | `member_ids` | `fixed64` | `repeated` | `` |  |
| 4 | `game_modes` | `uint32` | `optional` | `` |  |
| 6 | `state` | `.CSODOTAParty.State` | `optional` | `` | default = UI |
| 7 | `effective_started_matchmaking_time` | `uint32` | `optional` | `` |  |
| 11 | `matchgroups` | `uint32` | `optional` | `` |  |
| 19 | `low_priority_account_id` | `uint32` | `optional` | `` |  |
| 21 | `match_type` | `.MatchType` | `optional` | `` | default = MATCH_TYPE_CASUAL |
| 23 | `team_id` | `uint32` | `optional` | `` |  |
| 24 | `match_disabled_until_date` | `uint32` | `optional` | `` |  |
| 25 | `match_disabled_account_id` | `uint32` | `optional` | `` |  |
| 26 | `matchmaking_max_range_minutes` | `uint32` | `optional` | `` |  |
| 27 | `matchlanguages` | `uint32` | `optional` | `` |  |
| 29 | `members` | `.CSODOTAPartyMember` | `repeated` | `` |  |
| 32 | `raw_started_matchmaking_time` | `uint32` | `optional` | `` |  |
| 33 | `attempt_start_time` | `uint32` | `optional` | `` |  |
| 34 | `attempt_num` | `uint32` | `optional` | `` |  |
| 35 | `low_priority_games_remaining` | `uint32` | `optional` | `` |  |
| 40 | `open_for_join_requests` | `bool` | `optional` | `` |  |
| 41 | `sent_invites` | `.CSODOTAPartyInvite` | `repeated` | `` |  |
| 42 | `recv_invites` | `.CSODOTAPartyInvite` | `repeated` | `` |  |
| 43 | `account_flags` | `uint32` | `optional` | `` |  |
| 44 | `region_select_flags` | `uint32` | `optional` | `` |  |
| 45 | `exclusive_tournament_id` | `uint32` | `optional` | `` |  |
| 47 | `tourney_division_id` | `uint32` | `optional` | `` |  |
| 48 | `tourney_schedule_time` | `uint32` | `optional` | `` |  |
| 49 | `tourney_skill_level` | `uint32` | `optional` | `` |  |
| 50 | `tourney_bracket_round` | `uint32` | `optional` | `` |  |
| 51 | `team_name` | `string` | `optional` | `` |  |
| 52 | `team_ui_logo` | `uint64` | `optional` | `` |  |
| 53 | `team_base_logo` | `uint64` | `optional` | `` |  |
| 54 | `tourney_queue_deadline_time` | `uint32` | `optional` | `` |  |
| 55 | `tourney_queue_deadline_state` | `.ETourneyQueueDeadlineState` | `optional` | `` | default = k_ETourneyQueueDeadlineState_Normal |
| 56 | `party_builder_slots_to_fill` | `uint32` | `optional` | `` |  |
| 57 | `party_builder_match_groups` | `uint32` | `optional` | `` |  |
| 58 | `party_builder_start_time` | `uint32` | `optional` | `` |  |
| 59 | `solo_queue` | `bool` | `optional` | `` |  |
| 61 | `steam_clan_account_id` | `uint32` | `optional` | `` |  |
| 62 | `ready_check` | `.CMsgReadyCheckStatus` | `optional` | `` |  |
| 63 | `custom_game_disabled_until_date` | `uint32` | `optional` | `` |  |
| 64 | `custom_game_disabled_account_id` | `uint32` | `optional` | `` |  |
| 65 | `is_challenge_match` | `bool` | `optional` | `` |  |
| 66 | `party_search_beacon_active` | `bool` | `optional` | `` |  |
| 67 | `matchmaking_flags` | `uint32` | `optional` | `` |  |
| 68 | `high_priority_state` | `.EHighPriorityMMState` | `optional` | `` | default = k_EHighPriorityMM_Unknown |
| 69 | `lane_selections_enabled` | `bool` | `optional` | `` |  |
| 70 | `custom_game_difficulty_mask` | `uint32` | `optional` | `` |  |
| 71 | `is_steam_china` | `bool` | `optional` | `` |  |
| 72 | `bot_difficulty_mask` | `uint32` | `optional` | `` |  |
| 73 | `bot_script_index_mask` | `uint32` | `optional` | `` |  |
| 74 | `restricted_from_ranked` | `bool` | `optional` | `` |  |
| 75 | `restricted_from_ranked_account_id` | `uint32` | `optional` | `` |  |
| 76 | `rank_spread_likert_scale` | `uint32` | `optional` | `` |  |
| 77 | `behavior_score_likert_scale` | `uint32` | `optional` | `` |  |
| 78 | `contains_required_playtester` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CSODOTAPartyInvite</code> — fields: 8; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `group_id` | `uint64` | `optional` | `` | (key_field) = true |
| 2 | `sender_id` | `fixed64` | `optional` | `` |  |
| 3 | `sender_name` | `string` | `optional` | `` |  |
| 4 | `members` | `.CSODOTAPartyInvite.PartyMember` | `repeated` | `` |  |
| 5 | `team_id` | `uint32` | `optional` | `` |  |
| 6 | `low_priority_status` | `bool` | `optional` | `` |  |
| 7 | `as_coach` | `bool` | `optional` | `` |  |
| 8 | `invite_gid` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CSODOTAPartyInvite.PartyMember</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CSODOTAPartyInvite`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `steam_id` | `fixed64` | `optional` | `` |  |
| 4 | `is_coach` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgLeaverState</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `lobby_state` | `uint32` | `optional` | `` |  |
| 2 | `game_state` | `.DOTA_GameState` | `optional` | `` | default = DOTA_GAMERULES_STATE_INIT |
| 3 | `leaver_detected` | `bool` | `optional` | `` |  |
| 4 | `first_blood_happened` | `bool` | `optional` | `` |  |
| 5 | `discard_match_results` | `bool` | `optional` | `` |  |
| 6 | `mass_disconnect` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgReadyCheckStatus</code> — fields: 4; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `start_timestamp` | `uint32` | `optional` | `` |  |
| 2 | `finish_timestamp` | `uint32` | `optional` | `` |  |
| 3 | `initiator_account_id` | `uint32` | `optional` | `` |  |
| 4 | `ready_members` | `.CMsgReadyCheckStatus.ReadyMember` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgReadyCheckStatus.ReadyMember</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgReadyCheckStatus`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `ready_status` | `.EReadyCheckStatus` | `optional` | `` | default = k_EReadyCheckStatus_Unknown |

</details>

<details>
<summary><code>CMsgPartyReadyCheckRequest</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgPartyReadyCheckResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.EReadyCheckRequestResult` | `optional` | `` | default = k_EReadyCheckRequestResult_Success |

</details>

<details>
<summary><code>CMsgPartyReadyCheckAcknowledge</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ready_status` | `.EReadyCheckStatus` | `optional` | `` | default = k_EReadyCheckStatus_Unknown |

</details>

<details>
<summary><code>CMsgLobbyEventGameDetails</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `kv_data` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgMatchMatchmakingStats</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `average_queue_time` | `uint32` | `optional` | `` |  |
| 2 | `maximum_queue_time` | `uint32` | `optional` | `` |  |
| 3 | `behavior_score_variance` | `.EMatchBehaviorScoreVariance` | `optional` | `` | default = k_EMatchBehaviorScoreVariance_Invalid |

</details>

<details>
<summary><code>CMvpData</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `mvps` | `.CMvpData.MvpDatum` | `repeated` | `` |  |
| 2 | `event_mvps` | `.CMvpData.MvpDatum` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMvpData.MvpDatum</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: `CMvpData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_slot` | `uint32` | `optional` | `` |  |
| 2 | `accolades` | `.CMvpData.MvpDatum.MvpAccolade` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMvpData.MvpDatum.MvpAccolade</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: `CMvpData.MvpDatum`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `type` | `.CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType` | `optional` | `` | default = kills |
| 2 | `detail_value` | `float` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>ELaneSelection</code> — values: 5</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_ELaneSelection_SAFELANE` | 0 |
| `k_ELaneSelection_OFFLANE` | 1 |
| `k_ELaneSelection_MIDLANE` | 2 |
| `k_ELaneSelection_SUPPORT` | 3 |
| `k_ELaneSelection_HARDSUPPORT` | 4 |

</details>

<details>
<summary><code>ELaneSelectionFlags</code> — values: 10</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_ELaneSelectionFlags_SAFELANE` | 1 |
| `k_ELaneSelectionFlags_OFFLANE` | 2 |
| `k_ELaneSelectionFlags_MIDLANE` | 4 |
| `k_ELaneSelectionFlags_SUPPORT` | 8 |
| `k_ELaneSelectionFlags_HARDSUPPORT` | 16 |
| `k_ELaneSelectionFlagGroup_None` | 0 |
| `k_ELaneSelectionFlagGroup_CORE` | 7 |
| `k_ELaneSelectionFlagGroup_SUPPORT` | 24 |
| `k_ELaneSelectionFlagGroup_ALL` | 31 |
| `k_ELaneSelectionFlagGroup_HIGHDEMAND` | 18 |

</details>

<details>
<summary><code>EPartyMatchmakingFlags</code> — values: 2</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EPartyMatchmakingFlags_None` | 0 |
| `k_EPartyMatchmakingFlags_LargeRankSpread` | 1 |

</details>

<details>
<summary><code>EHighPriorityMMState</code> — values: 9</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EHighPriorityMM_Unknown` | 0 |
| `k_EHighPriorityMM_MissingMMData` | 1 |
| `k_EHighPriorityMM_ResourceMissing` | 2 |
| `k_EHighPriorityMM_ManuallyDisabled` | 3 |
| `k_EHighPriorityMM_Min_Enabled` | 64 |
| `k_EHighPriorityMM_AllRolesSelected` | 65 |
| `k_EHighPriorityMM_UsingResource` | 66 |
| `k_EHighPriorityMM_FiveStack` | 67 |
| `k_EHighPriorityMM_HighDemand` | 68 |

</details>

<details>
<summary><code>EReadyCheckStatus</code> — values: 3</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EReadyCheckStatus_Unknown` | 0 |
| `k_EReadyCheckStatus_NotReady` | 1 |
| `k_EReadyCheckStatus_Ready` | 2 |

</details>

<details>
<summary><code>EReadyCheckRequestResult</code> — values: 5</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EReadyCheckRequestResult_Success` | 0 |
| `k_EReadyCheckRequestResult_AlreadyInProgress` | 1 |
| `k_EReadyCheckRequestResult_NotInParty` | 2 |
| `k_EReadyCheckRequestResult_SendError` | 3 |
| `k_EReadyCheckRequestResult_UnknownError` | 4 |

</details>

<details>
<summary><code>EMatchBehaviorScoreVariance</code> — values: 4</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EMatchBehaviorScoreVariance_Invalid` | 0 |
| `k_EMatchBehaviorScoreVariance_Low` | 1 |
| `k_EMatchBehaviorScoreVariance_Medium` | 2 |
| `k_EMatchBehaviorScoreVariance_High` | 3 |

</details>

<details>
<summary><code>CSODOTAParty.State</code> — values: 3</summary>

- Parent: `CSODOTAParty`

| Name | Number |
|---|---:|
| `UI` | 0 |
| `FINDING_MATCH` | 1 |
| `IN_MATCH` | 2 |

</details>

<details>
<summary><code>CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType</code> — values: 283</summary>

- Parent: `CMvpData.MvpDatum.MvpAccolade`

| Name | Number |
|---|---:|
| `kills` | 1 |
| `deaths` | 2 |
| `assists` | 3 |
| `net_worth` | 5 |
| `item_value` | 6 |
| `support_gold_spent` | 7 |
| `wards_placed` | 8 |
| `dewards` | 9 |
| `camps_stacked` | 10 |
| `last_hits` | 11 |
| `denies` | 12 |
| `kKillEaterEvent_Killing_Sprees` | 13 |
| `kKillEaterEvent_Godlike` | 14 |
| `kKillEaterEvent_Towers_Destroyed` | 15 |
| `kKillEaterEventType_Invoker_SunstrikeKills` | 16 |
| `kKillEaterEventType_Axe_Culls` | 17 |
| `kKillEaterEventType_Axe_BattleHungerKills` | 18 |
| `kKillEaterEventType_LowHealthKills` | 19 |
| `kKillEaterEventType_Invoker_TornadoKills` | 20 |
| `kKillEaterEventType_Sven_DoubleStuns` | 21 |
| `kKillEaterEventType_Sven_WarcryAssists` | 22 |
| `kKillEaterEventType_Sven_CleaveDoubleKills` | 23 |
| `kKillEaterEventType_Sven_TeleportInterrupts` | 24 |
| `kKillEaterEventType_Faceless_MultiChrono` | 25 |
| `kKillEaterEventType_Faceless_ChronoKills` | 26 |
| `kKillEaterEventType_Ursa_MultiShocks` | 27 |
| `kKillEaterEventType_RoshanKills` | 28 |
| `kKillEaterEventType_Lion_FingerKills` | 29 |
| `kKillEaterEventType_Riki_SmokedHeroKills` | 32 |
| `kKillEaterEventType_HeroesRevealedWithDust` | 33 |
| `kKillEaterEventType_SkeletonKing_ReincarnationKills` | 34 |
| `kKillEaterEventType_Skywrath_FlareKills` | 35 |
| `kKillEaterEventType_Leshrac_SplitEarthStuns` | 36 |
| `kKillEaterEventType_Mirana_MaxStunArrows` | 37 |
| `kKillEaterEventType_PhantomAssassin_CoupdeGraceCrits` | 38 |
| `kKillEaterEventType_PhantomAssassin_DaggerCrits` | 39 |
| `kKillEaterEventType_Meepo_Earthbinds` | 40 |
| `kKillEaterEventType_Bloodseeker_RuptureKills` | 41 |
| `kKillEaterEventType_Slark_LeashedEnemies` | 42 |
| `kKillEaterEventType_Disruptor_FountainGlimpses` | 43 |
| `kKillEaterEventType_Rubick_SpellsStolen` | 44 |
| `kKillEaterEventType_Rubick_UltimatesStolen` | 45 |
| `kKillEaterEventType_Doom_EnemiesDoomed` | 46 |
| `kKillEaterEventType_Omniknight_Purifications` | 47 |
| `kKillEaterEventType_Omniknight_AlliesRepelled` | 48 |
| `kKillEaterEventType_Omniknight_EnemiesRepelled` | 49 |
| `kKillEaterEventType_Warlock_FiveHeroFatalBonds` | 50 |
| `kKillEaterEventType_CrystalMaiden_FrostbittenEnemies` | 51 |
| `kKillEaterEventType_CrystalMaiden_CrystalNovas` | 52 |
| `kKillEaterEventType_Kunkka_DoubleHeroTorrents` | 53 |
| `kKillEaterEventType_Kunkka_TripleHeroGhostShips` | 54 |
| `kKillEaterEventType_NagaSiren_EnemiesEnsnared` | 55 |
| `kKillEaterEventType_NagaSiren_TripleHeroRipTides` | 56 |
| `kKillEaterEventType_Lycan_KillsDuringShapeshift` | 57 |
| `kKillEaterEventType_Pudge_DismemberKills` | 58 |
| `kKillEaterEventType_Pudge_EnemyHeroesHooked` | 59 |
| `kKillEaterEventType_Pudge_HookKills` | 60 |
| `kKillEaterEventType_Pudge_UnseenEnemyHeroesHooked` | 61 |
| `kKillEaterEventType_DrowRanger_EnemiesSilenced` | 62 |
| `kKillEaterEventType_DrowRanger_MultiHeroSilences` | 63 |
| `kKillEaterEventType_DrowRanger_SilencedKills` | 64 |
| `kKillEaterEventType_DrowRanger_FrostArrowKills` | 65 |
| `kKillEaterEventType_DragonKnight_KillsInDragonForm` | 66 |
| `kKillEaterEventType_DragonKnight_BreatheFireKills` | 67 |
| `kKillEaterEventType_DragonKnight_SplashKills` | 68 |
| `kKillEaterEventType_WitchDoctor_CaskStuns` | 69 |
| `kKillEaterEventType_WitchDoctor_MaledictKills` | 70 |
| `kKillEaterEventType_WitchDoctor_MultiHeroMaledicts` | 71 |
| `kKillEaterEventType_WitchDoctor_DeathWardKills` | 72 |
| `kKillEaterEventType_Disruptor_ThunderStrikeKills` | 73 |
| `kKillEaterEventType_Disruptor_HeroesGlimpsed` | 74 |
| `kKillEaterEventType_CrystalMaiden_FreezingFieldKills` | 75 |
| `kKillEaterEventType_Medusa_EnemiesPetrified` | 77 |
| `kKillEaterEventType_Warlock_FatalBondsKills` | 78 |
| `kKillEaterEventType_Warlock_GolemKills` | 79 |
| `kKillEaterEventType_Tusk_WalrusPunches` | 80 |
| `kKillEaterEventType_Tusk_SnowballStuns` | 81 |
| `kKillEaterEventType_Earthshaker_FissureStuns` | 82 |
| `kKillEaterEventType_Earthshaker_3HeroEchoslams` | 83 |
| `kKillEaterEventType_SandKing_BurrowstrikeStuns` | 84 |
| `kKillEaterEventType_SandKing_EpicenterKills` | 85 |
| `kKillEaterEventType_SkywrathMage_AncientSealKills` | 86 |
| `kKillEaterEventType_SkywrathMage_ConcussiveShotKills` | 87 |
| `kKillEaterEventType_Luna_LucentBeamKills` | 88 |
| `kKillEaterEventType_Luna_EclipseKills` | 89 |
| `kKillEaterEventType_KeeperOfTheLight_IlluminateKills` | 90 |
| `kKillEaterEventType_KeeperOfTheLight_ManaLeakStuns` | 91 |
| `kKillEaterEventType_KeeperOfTheLight_TeammatesRecalled` | 92 |
| `kKillEaterEventType_LegionCommander_DuelsWon` | 93 |
| `kKillEaterEventType_Beastmaster_RoarKills` | 94 |
| `kKillEaterEventType_Beastmaster_RoarMultiKills` | 95 |
| `kKillEaterEventType_Windrunner_FocusFireBuildings` | 96 |
| `kKillEaterEventType_Windrunner_PowershotKills` | 97 |
| `kKillEaterEventType_PhantomAssassin_DaggerLastHits` | 98 |
| `kKillEaterEventType_PhantomAssassin_PhantomStrikeKills` | 99 |
| `kKillEaterEventType_DeathProphet_CryptSwarmKills` | 100 |
| `kKillEaterEventType_DeathProphet_ExorcismBuildingKills` | 101 |
| `kKillEaterEventType_DeathProphet_ExorcismSpiritsSummoned` | 102 |
| `kKillEaterEventType_DeathProphet_MultiHeroSilences` | 103 |
| `kKillEaterEventType_Abaddon_MistCoilKills` | 104 |
| `kKillEaterEventType_Abaddon_MistCoilHealed` | 105 |
| `kKillEaterEventType_Abaddon_AphoticShieldKills` | 106 |
| `kKillEaterEventType_Lich_ChainFrostTripleKills` | 107 |
| `kKillEaterEventType_Lich_ChainFrostMultiKills` | 108 |
| `kKillEaterEventType_Lich_ChainFrostBounces` | 109 |
| `kKillEaterEventType_Ursa_EnragedKills` | 110 |
| `kKillEaterEventType_Ursa_EarthshockKills` | 111 |
| `kKillEaterEventType_Lina_LagunaBladeKills` | 112 |
| `kKillEaterEventType_Lina_DragonSlaveKills` | 113 |
| `kKillEaterEventType_Lina_LightStrikeArrayStuns` | 114 |
| `kKillEaterEvent_Barracks_Destroyed` | 115 |
| `kKillEaterEvent_TemplarAssassin_MeldKills` | 116 |
| `kKillEaterEvent_TemplarAssassin_HeroesSlowed` | 117 |
| `kKillEaterEvent_Sniper_AssassinationKills` | 118 |
| `kKillEaterEvent_Sniper_HeadshotStuns` | 119 |
| `kKillEaterEvent_EarthSpirit_SmashStuns` | 120 |
| `kKillEaterEvent_EarthSpirit_GripSilences` | 121 |
| `kKillEaterEvent_ShadowShaman_ShackleKills` | 122 |
| `kKillEaterEvent_ShadowShaman_HexKills` | 123 |
| `kKillEaterEvent_Centaur_EnemiesStomped` | 124 |
| `kKillEaterEvent_Centaur_DoubleEdgeKills` | 125 |
| `kKillEaterEvent_Centaur_ReturnKills` | 126 |
| `kKillEaterEvent_EmberSpirit_EnemiesChained` | 127 |
| `kKillEaterEvent_EmberSpirit_SleightOfFistMultiKills` | 128 |
| `kKillEaterEvent_Puck_OrbKills` | 129 |
| `kKillEaterEvent_VengefulSpirit_EnemiesStunned` | 130 |
| `kKillEaterEvent_Lifestealer_RageKills` | 131 |
| `kKillEaterEvent_Lifestealer_OpenWoundsKills` | 132 |
| `kKillEaterEvent_Lifestealer_InfestKills` | 133 |
| `kKillEaterEvent_ElderTitan_SpiritKills` | 134 |
| `kKillEaterEvent_ElderTitan_GoodStomps` | 135 |
| `kKillEaterEvent_Clockwerk_RocketKills` | 136 |
| `kKillEaterEvent_Clockwerk_BlindRocketKills` | 137 |
| `kKillEaterEvent_StormSpirit_BallKills` | 138 |
| `kKillEaterEvent_StormSpirit_DoubleRemnantKills` | 139 |
| `kKillEaterEvent_StormSpirit_VortexKills` | 140 |
| `kKillEaterEvent_Tinker_DoubleMissileKills` | 141 |
| `kKillEaterEvent_Tinker_LaserKills` | 142 |
| `kKillEaterEvent_Techies_SuicideKills` | 143 |
| `kKillEaterEvent_Techies_LandMineKills` | 144 |
| `kKillEaterEvent_Techies_StatisTrapStuns` | 145 |
| `kKillEaterEvent_Techies_RemoteMineKills` | 146 |
| `kKillEaterEvent_ShadowFiend_TripleRazeKills` | 147 |
| `kKillEaterEvent_ShadowFiend_RequiemMultiKills` | 148 |
| `kKillEaterEvent_ShadowFiend_QRazeKills` | 149 |
| `kKillEaterEvent_ShadowFiend_WRazeKills` | 150 |
| `kKillEaterEvent_ShadowFiend_ERazeKills` | 151 |
| `kKillEaterEvent_Oracle_FatesEdictKills` | 152 |
| `kKillEaterEvent_Oracle_FalsePromiseSaves` | 153 |
| `kKillEaterEvent_Juggernaut_OmnislashKills` | 154 |
| `kKillEaterEventType_SkeletonKing_SkeletonHeroKills` | 157 |
| `kKillEaterEventType_DarkWillow_CursedCrownTripleStuns` | 158 |
| `kKillEaterEventType_Dazzle_ShallowGraveSaves` | 159 |
| `kKillEaterEventType_Dazzle_PoisonTouchKills` | 160 |
| `kKillEaterEventType_ThreeManMeks` | 161 |
| `kKillEaterEventType_Viper_PoisonAttackKills` | 162 |
| `kKillEaterEventType_Viper_CorrosiveSkinKills` | 163 |
| `kKillEaterEventType_ThreeHeroVeils` | 164 |
| `kKillEaterEventType_Viper_KillsDuringViperStrike` | 165 |
| `kKillEaterEventType_SolarCrestKills` | 166 |
| `kKillEaterEventType_Tiny_TreeThrowKills` | 167 |
| `kKillEaterEventType_Riki_BackstabKills` | 168 |
| `kKillEaterEventType_Phoenix_ThreeHeroSupernovaStuns` | 169 |
| `kKillEaterEventType_Terrorblade_MetamorphosisKills` | 170 |
| `kKillEaterEventType_Lion_GreatFingerKills` | 171 |
| `kKillEaterEventType_Antimage_SpellsBlockedWithAghanims` | 172 |
| `kKillEaterEventType_Antimage_ThreeManManaVoids` | 173 |
| `kKillEaterEventType_ArcWarden_TempestDoubleKills` | 174 |
| `kKillEaterEventType_ArcWarden_SparkWraithKills` | 175 |
| `kKillEaterEventType_Bane_BrainSapKills` | 176 |
| `kKillEaterEventType_Bane_FiendsGripKills` | 177 |
| `kKillEaterEventType_Batrider_TripleHeroFlamebreaks` | 178 |
| `kKillEaterEventType_Batrider_DoubleHeroLassoes` | 179 |
| `kKillEaterEventType_Brewmaster_KillsDuringPrimalSplit` | 180 |
| `kKillEaterEventType_Bristleback_KillsUnderFourQuillStacks` | 181 |
| `kKillEaterEventType_Bristleback_TripleHeroNasalGoo` | 182 |
| `kKillEaterEventType_Broodmother_SpiderlingHeroKills` | 183 |
| `kKillEaterEventType_Broodmother_KillsInsideWeb` | 184 |
| `kKillEaterEventType_Centaur_ThreeHeroStampede` | 185 |
| `kKillEaterEventType_ChaosKnight_RealityRiftKills` | 186 |
| `kKillEaterEventType_Chen_KillsWithPenitence` | 187 |
| `kKillEaterEventType_CrystalMaiden_TwoHeroCrystalNovas` | 188 |
| `kKillEaterEventType_CrystalMaiden_ThreeHeroFreezingFields` | 189 |
| `kKillEaterEventType_Dazzle_ShadowWaveKills` | 190 |
| `kKillEaterEventType_DeathProphet_SiphonKills` | 191 |
| `kKillEaterEventType_DeathProphet_ExorcismKillsDuringEuls` | 192 |
| `kKillEaterEventType_Disruptor_ThreeHeroKineticFieldStaticStorm` | 193 |
| `kKillEaterEventType_Doom_InfernalBladeBurnKills` | 194 |
| `kKillEaterEventType_DrowRanger_PrecisionAuraCreepTowerKills` | 195 |
| `kKillEaterEventType_EmberSpirit_RemnantKills` | 196 |
| `kKillEaterEventType_EmberSpirit_SleightOfFistKills` | 197 |
| `kKillEaterEventType_Enigma_MidnightPulseBlackHoleCombos` | 198 |
| `kKillEaterEventType_Enigma_ThreeManBlackHoles` | 199 |
| `kKillEaterEventType_FacelessVoid_MultiHeroTimeDilation` | 200 |
| `kKillEaterEventType_Gyrocopter_ThreeHeroFlakCannon` | 201 |
| `kKillEaterEventType_Gyrocopter_HomingMissileKills` | 202 |
| `kKillEaterEventType_Gyrocopter_RocketBarrageKills` | 203 |
| `kKillEaterEventType_Huskar_KillsDuringLifeBreak` | 204 |
| `kKillEaterEventType_Huskar_BurningSpearKills` | 205 |
| `kKillEaterEventType_Invoker_MultiHeroIceWall` | 206 |
| `kKillEaterEventType_Invoker_ThreeHeroEMP` | 207 |
| `kKillEaterEventType_Invoker_ThreeHeroDeafeningBlast` | 208 |
| `kKillEaterEventType_Invoker_MultiHeroChaosMeteor` | 209 |
| `kKillEaterEventType_Jakiro_MultiHeroDualBreath` | 210 |
| `kKillEaterEventType_Jakiro_IcePathMacropyreCombos` | 211 |
| `kKillEaterEventType_Leshrac_PulseNovaKills` | 212 |
| `kKillEaterEventType_Leshrac_ThreeHeroLightningStorm` | 213 |
| `kKillEaterEventType_Lion_ThreeHeroFingerOfDeath` | 214 |
| `kKillEaterEventType_Meepo_PoofKills` | 215 |
| `kKillEaterEventType_Meepo_MultiHeroEarthbinds` | 216 |
| `kKillEaterEventType_NightStalker_NighttimeKills` | 217 |
| `kKillEaterEventType_Morphling_KillsDuringReplicate` | 218 |
| `kKillEaterEventType_OgreMagi_FireblastKills` | 219 |
| `kKillEaterEventType_OgreMagi_IgniteKills` | 220 |
| `kKillEaterEventType_DominatingKillStreaks` | 221 |
| `kKillEaterEventType_MegaKillStreaks` | 222 |
| `kKillEaterEventType_Alchemist_AghanimsGiven` | 223 |
| `kKillEaterEventType_VeilsLeadingToKills` | 224 |
| `kKillEaterEventType_DustLeadingToKills` | 225 |
| `kKillEaterEventType_WitchDoctor_MultiHeroCaskStuns` | 226 |
| `kKillEaterEventType_Weaver_ShukuchiKills` | 227 |
| `kKillEaterEventType_Windrunner_ShackleFocusFireKills` | 228 |
| `kKillEaterEventType_VengefulSpirit_VengeanceAuraIllusionKills` | 229 |
| `kKillEaterEventType_Tusk_WalrusPunchKills` | 230 |
| `kKillEaterEventType_Tinker_MultiHeroLasers` | 231 |
| `kKillEaterEventType_TemplarAssassin_MultiHeroPsiBlades` | 232 |
| `kKillEaterEventType_Sven_KillsDuringGodsStrength` | 233 |
| `kKillEaterEventType_Sniper_ThreeHeroShrapnels` | 234 |
| `kKillEaterEventType_Slark_KillsDuringShadowDance` | 235 |
| `kKillEaterEventType_ShadowShaman_MultiHeroEtherShocks` | 236 |
| `kKillEaterEventType_ShadowShaman_SerpentWardShackleKills` | 237 |
| `kKillEaterEventType_Riki_ThreeHeroTricksOfTheTrade` | 238 |
| `kKillEaterEventType_Razor_EyeOfTheStormKills` | 239 |
| `kKillEaterEventType_Pugna_LifeDrainKills` | 240 |
| `kKillEaterEventType_ObsidianDestroyer_SanitysEclipseKills` | 241 |
| `kKillEaterEventType_Oracle_MultiHeroFortunesEnd` | 242 |
| `kKillEaterEventType_Omniknight_PurificationKills` | 243 |
| `kKillEaterEventType_NightStalker_EnemyMissesUnderCripplingFear` | 244 |
| `kKillEaterEventType_Warlock_ThreeHeroFatalBonds` | 245 |
| `kKillEaterEventType_Riki_TricksOfTheTradeKills` | 246 |
| `kKillEaterEventType_Earthshaker_AftershockHits10` | 247 |
| `kKillEaterEventType_Earthshaker_5HeroEchoslams` | 248 |
| `kKillEaterEventType_Lina_LagunaBladeHeroKills` | 249 |
| `kKillEaterEventType_Lina_LightStrikeHeroStuns` | 250 |
| `kKillEaterEventType_Earthshaker_FissureMultiStuns` | 251 |
| `kKillEaterEventType_Earthshaker_TotemKills` | 252 |
| `kKillEaterEventType_Pangolier_SwashbuckleKills` | 253 |
| `kKillEaterEventType_Furion_EnemyHeroesTrapped` | 254 |
| `kKillEaterEventType_Pangolier_HeartpiercerKills` | 255 |
| `kKillEaterEventType_Medusa_MultiHeroStoneGaze` | 256 |
| `kKillEaterEventType_Medusa_SplitShotKills` | 257 |
| `kKillEaterEventType_Mirana_MultiHeroStarstorm` | 258 |
| `kKillEaterEventType_Mirana_KillsFromMoonlightShadow` | 259 |
| `kKillEaterEventType_Magnus_MultiHeroSkewers` | 260 |
| `kKillEaterEventType_Magnus_MultiHeroReversePolarity` | 261 |
| `kKillEaterEventType_Magnus_HeroesSlowedWithShockwave` | 262 |
| `kKillEaterEventType_NagaSiren_MultiHeroSong` | 263 |
| `kKillEaterEventType_NagaSiren_AlliesHealedBySong` | 264 |
| `kKillEaterEventType_LoneDruid_MultiHeroRoar` | 265 |
| `kKillEaterEventType_LoneDruid_BattleCryKills` | 266 |
| `kKillEaterEventType_WinterWyvern_ThreeHeroCurses` | 267 |
| `kKillEaterEventType_Antimage_SpellsBlockedWithCounterspell` | 268 |
| `kKillEaterEventType_Mars_EnemiesKilledInArena` | 269 |
| `kKillEaterEventType_Mars_MultiHeroGodsRebuke` | 270 |
| `kKillEaterEventType_Mars_GodsRebukeKills` | 271 |
| `kKillEaterEventType_Snapfire_LizardBlobsKills` | 272 |
| `kKillEaterEventType_Snapfire_TwoHeroCookieStuns` | 273 |
| `Custom_KillStreak` | 274 |
| `kKillEaterEventType_Muerta_DeadShotKills` | 275 |
| `kKillEaterEventType_Muerta_PierceTheVeilKills` | 276 |
| `kKillEaterEventType_Muerta_MultiHeroDeadShot` | 277 |
| `kKillEaterEventType_Muerta_DeadShotsIntoTheCalling` | 278 |
| `kKillEaterEventType_Ringmaster_LongRangeDaggerHits` | 279 |
| `kKillEaterEventType_Ringmaster_MultiHeroWhips` | 280 |
| `kKillEaterEventType_Ringmaster_MultiHeroMesmerizes` | 281 |
| `kKillEaterEventType_Kez_ParryCounterAttacks` | 282 |
| `kKillEaterEventType_Kez_RavensVeilKills` | 283 |
| `kKillEaterEventType_Kez_RaptorDanceHealing` | 284 |
| `kKillEaterEventType_Kez_KillsDuringFalconRush` | 285 |
| `kKillEaterEventType_Seasonal_PartyHatsStolen` | 286 |
| `kKillEaterEventType_Seasonal_TallestHat` | 287 |
| `kKillEaterEventType_Largo_MultiHeroFrogstomp` | 288 |
| `kKillEaterEventType_Largo_AmphibianRhapsodyKillsAndAssists` | 289 |

</details>
