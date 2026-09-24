"""Tests for gem.results.dataframes conversion helpers."""

from __future__ import annotations

import pytest

import gem.results.models as model_module
from gem.combat.log import CombatLogEntry, CombatLogSource, CombatLogType
from gem.extractors.objectives import (
    AegisEvent,
    RoshanKill,
    ShrineKill,
    TormentorKill,
    TowerKill,
)
from gem.extractors.teamfights import Teamfight, TeamfightPlayer
from gem.results.dataframes import CORE_TABLES, OPTIONAL_GROUPS, build_dataframes
from gem.results.models import (
    ParsedMatch,
    ParsedPlayer,
    SmokeEvent,
    SmokeParticipant,
    VisionModifierEvent,
    VisionModifierPairingIssue,
    VisionModifierSemantic,
)


class TestBuildDataframes:
    def test_player_tables_split_summary_and_timeseries(self):
        pp = ParsedPlayer(
            player_id=0,
            hero_name="npc_dota_hero_axe",
            team=2,
            times=[30],
            gold_t=[500],
            total_earned_gold_t=[900],
            total_earned_xp_t=[1200],
            lh_t=[10],
            dn_t=[2],
            xp_t=[600],
            aghanims_scepter=1,
            aghanims_shard=0,
            moonshard=1,
        )
        pp.damage_by_type = {"physical": 1200, "magical": 300, "pure": 50}
        pp.damage_taken_by_type = {"physical": 800, "magical": 450, "pure": 20}

        match = ParsedMatch(players=[pp] + [ParsedPlayer(player_id=i) for i in range(1, 10)])

        dfs = build_dataframes(match)
        assert "players" not in dfs

        summary_df = dfs["player_summary"]
        assert len(summary_df) == 10
        assert summary_df["player_id"].is_unique

        series = dfs["player_timeseries"].iloc[0]
        assert series["tick"] == 30
        assert series["gold"] == 500
        assert series["total_earned_gold"] == 900
        assert series["total_earned_xp"] == 1200
        assert "kills" not in dfs["player_timeseries"].columns

        row = summary_df.iloc[0]
        assert row["damage_physical"] == 1200
        assert row["damage_magical"] == 300
        assert row["damage_pure"] == 50
        assert row["damage_taken_physical"] == 800
        assert row["damage_taken_magical"] == 450
        assert row["damage_taken_pure"] == 20
        assert row["aghanims_scepter"] == 1
        assert row["aghanims_shard"] == 0
        assert row["moonshard"] == 1

    def test_log_type_is_plain_str_in_every_log_bearing_table(self):
        # log_type is a CombatLogType enum internally, but every exported table
        # built from CombatLogEntry objects must hold plain str cells so the
        # public DataFrame/Parquet schema is unchanged. This covers the
        # top-level combat_log table AND the per-player log projections.
        pp = ParsedPlayer(player_id=0)
        pp.kills_log = [CombatLogEntry(tick=10, log_type=CombatLogType.DEATH)]
        pp.purchase_log = [CombatLogEntry(tick=11, log_type=CombatLogType.PURCHASE)]
        pp.runes_log = [CombatLogEntry(tick=12, log_type=CombatLogType.PICKUP_RUNE)]
        pp.buyback_log = [CombatLogEntry(tick=13, log_type=CombatLogType.BUYBACK)]

        match = ParsedMatch(players=[pp] + [ParsedPlayer(player_id=i) for i in range(1, 10)])
        match.combat_log = [
            CombatLogEntry(tick=10, log_type=CombatLogType.DAMAGE, value=100),
            CombatLogEntry(tick=20, log_type=CombatLogType.DEATH),
        ]

        dfs = build_dataframes(match)

        log_tables = [
            "combat_log",
            "player_kills_log",
            "player_purchase_log",
            "player_runes_log",
            "player_buyback_log",
        ]
        for name in log_tables:
            df = dfs[name]
            assert "log_type" in df.columns, name
            assert all(type(v) is str for v in df["log_type"]), name

        assert list(dfs["combat_log"]["log_type"]) == ["DAMAGE", "DEATH"]
        assert list(dfs["player_kills_log"]["log_type"]) == ["DEATH"]
        assert list(dfs["player_purchase_log"]["log_type"]) == ["PURCHASE"]
        assert list(dfs["player_runes_log"]["log_type"]) == ["PICKUP_RUNE"]
        assert list(dfs["player_buyback_log"]["log_type"]) == ["BUYBACK"]

    def test_default_tables_are_core_and_groups_are_opt_in(self):
        match = ParsedMatch()

        dfs = build_dataframes(match)
        assert tuple(dfs) == CORE_TABLES
        for group_tables in OPTIONAL_GROUPS.values():
            assert not set(group_tables) & set(dfs)

        analysis_only = build_dataframes(match, include="analysis")
        assert set(analysis_only) == set(CORE_TABLES) | set(OPTIONAL_GROUPS["analysis"])

    def test_unknown_include_group_raises(self):
        with pytest.raises(ValueError, match="Unknown DataFrame group"):
            build_dataframes(ParsedMatch(), include=["players_legacy"])

    def test_every_table_leads_with_match_id(self):
        match = ParsedMatch(match_id=8822520406, players=[ParsedPlayer(player_id=0, times=[1])])

        dfs = build_dataframes(match, include=list(OPTIONAL_GROUPS))

        for name, df in dfs.items():
            assert df.columns[0] == "match_id", name
            assert (df["match_id"] == 8822520406).all(), name

    def test_build_dataframes_returns_extended_parity_keys(self):
        match = ParsedMatch()
        dfs = build_dataframes(match, include=["analysis", "opendota"])

        assert "player_summary" in dfs
        assert "player_timeseries" in dfs
        assert "player_breakdowns" in dfs
        assert "positions" in dfs
        assert "combat_log" in dfs
        assert "wards" in dfs
        assert "objectives" in dfs
        assert "chat" in dfs

        assert "players_minute" in dfs
        assert "match" in dfs
        assert "radiant_advantage" in dfs
        assert "draft" in dfs
        assert "teamfights" in dfs
        assert "teamfight_positioning" in dfs
        assert "roshan_conversions" in dfs
        assert "roshan_conversion_fights" in dfs
        assert "opendota_teamfights" in dfs
        assert "smoke_events" in dfs
        assert "smoke_members" in dfs
        assert "smoke_fight_insights" in dfs
        assert "smoke_fight_members" in dfs
        assert "smoke_fight_followups" in dfs
        assert "farming_routes" in dfs
        assert "farming_route_segments" in dfs
        assert "farming_route_points" in dfs
        assert "farming_context_tags" in dfs
        assert "courier_snapshots" in dfs
        assert "neutral_item_finds" in dfs
        assert "vision_modifiers" in dfs
        assert "vision_modifier_pairing_issues" in dfs
        assert "player_kills_log" in dfs
        assert "player_purchase_log" in dfs
        assert "player_runes_log" in dfs
        assert "player_buyback_log" in dfs

        assert dfs["neutral_item_finds"].empty
        assert dfs["opendota_teamfights"].empty
        assert dfs["teamfight_positioning"].empty
        assert dfs["roshan_conversions"].empty
        assert dfs["roshan_conversion_fights"].empty
        assert dfs["farming_route_segments"].empty
        assert dfs["farming_route_points"].empty
        assert list(dfs["farming_route_segments"].columns[1:7]) == [
            "player_id",
            "hero_name",
            "team",
            "segment_index",
            "camp_id",
            "camp_type",
        ]
        assert list(dfs["roshan_conversions"].columns[1:7]) == [
            "rosh_number",
            "rosh_tick",
            "killer_name",
            "roshan_team",
            "roshan_team_source",
            "conversion_team",
        ]
        assert list(dfs["roshan_conversion_fights"].columns[1:6]) == [
            "rosh_number",
            "fight_index",
            "relation",
            "engagement_start_tick",
            "engagement_start_source",
        ]
        assert list(dfs["teamfight_positioning"].columns[1:9]) == [
            "fight_index",
            "fight_start_tick",
            "engagement_start_tick",
            "first_death_tick",
            "fight_end_tick",
            "engagement_start_source",
            "snapshot_kind",
            "snapshot_tick",
        ]
        assert dfs["smoke_members"].empty
        assert list(dfs["smoke_members"].columns) == [
            "match_id",
            "smoke_event_index",
            "activation_tick",
            "activation_game_time_s",
            "activator",
            "team",
            "hero_name",
            "player_id",
            "applied_tick",
            "removed_tick",
            "modifier_duration_s",
            "modifier_elapsed_duration_s",
            "applied_x",
            "applied_y",
            "removed_x",
            "removed_y",
            "applied_game_time_s",
            "removed_game_time_s",
        ]
        assert dfs["smoke_fight_insights"].empty
        assert list(dfs["smoke_fight_insights"].columns[1:8]) == [
            "smoke_index",
            "fight_index",
            "status",
            "evidence_completeness",
            "smoke_team",
            "activator",
            "smoke_lifecycle_status",
        ]
        assert dfs["smoke_fight_members"].empty
        assert list(dfs["smoke_fight_members"].columns[1:7]) == [
            "smoke_index",
            "fight_index",
            "status",
            "participant_index",
            "player_id",
            "hero_name",
        ]
        assert dfs["smoke_fight_followups"].empty
        assert list(dfs["smoke_fight_followups"].columns[1:6]) == [
            "smoke_index",
            "fight_index",
            "kind",
            "source_index",
            "tick",
        ]
        assert dfs["vision_modifiers"].empty
        assert dfs["vision_modifier_pairing_issues"].empty
        assert list(dfs["vision_modifiers"].columns[1:7]) == [
            "tick",
            "end_tick",
            "modifier_name",
            "target_name",
            "caster_name",
            "caster_team",
        ]
        assert list(dfs["vision_modifier_pairing_issues"].columns[1:7]) == [
            "tick",
            "reason",
            "modifier_name",
            "caster_name",
            "target_name",
            "source",
        ]

    def test_roshan_conversion_tables_flatten_provenance_and_fight_evidence(self):
        players = [
            ParsedPlayer(
                player_id=player_id,
                hero_name=f"npc_dota_hero_hero_{player_id}",
                team=2 if player_id < 5 else 3,
            )
            for player_id in range(10)
        ]
        fight_players = [TeamfightPlayer(player_id=player_id) for player_id in range(10)]
        fight_players[0].damage_dealt = 500
        fight_players[5].deaths = 1
        match = ParsedMatch(
            game_start_tick=0,
            game_end_tick=20000,
            players=players,
            roshans=[
                RoshanKill(
                    1000,
                    "npc_dota_hero_hero_0",
                    1,
                    drops=["aegis"],
                    killer_team=2,
                )
            ],
            aegis_events=[AegisEvent(1010, 0, "pickup")],
            towers=[
                TowerKill(
                    1500,
                    3,
                    "",
                    "npc_dota_badguys_tower1_mid",
                    killer_team=2,
                )
            ],
            teamfights=[
                Teamfight(
                    start_tick=1100,
                    end_tick=1400,
                    first_death_tick=1300,
                    last_death_tick=1300,
                    deaths=1,
                    winner="radiant",
                    players=fight_players,
                )
            ],
        )

        frames = build_dataframes(match, include="analysis")
        conversion = frames["roshan_conversions"].iloc[0]
        fight = frames["roshan_conversion_fights"].iloc[0]
        objective_rows = frames["objectives"].set_index("type")

        assert objective_rows.loc["roshan", "killer_team"] == 2
        assert objective_rows.loc["tower", "killer_team"] == 2
        assert conversion["roshan_team_source"] == "protocol"
        assert conversion["conversion_team_source"] == "player_id"
        assert conversion["aegis_fate_source"] == "nominal_expiry"
        assert conversion["legacy_conversion_label"] == "fight_conversion"
        assert conversion["unattributed_towers"] == 0
        assert fight["fight_index"] == 0
        assert fight["relation"] == "in_window"
        assert fight["engagement_start_source"] in {
            "first_damage",
            "first_death_fallback",
        }
        assert fight["conversion_participant_ids"] == "0"
        assert fight["opponent_participant_ids"] == "5"

    def test_teamfight_positioning_table_is_flat_and_preserves_missing_values(self):
        radiant = ParsedPlayer(
            player_id=0,
            hero_name="npc_dota_hero_axe",
            team=2,
            position_log=[(1_000, 100.0, 200.0)],
        )
        dire = ParsedPlayer(
            player_id=5,
            hero_name="npc_dota_hero_bane",
            team=3,
            position_log=[],
        )
        fight_players = [TeamfightPlayer(player_id=i) for i in range(10)]
        fight_players[0].damage_dealt = 50
        match = ParsedMatch(
            players=[radiant, dire],
            teamfights=[
                Teamfight(
                    start_tick=550,
                    end_tick=1_450,
                    first_death_tick=1_000,
                    last_death_tick=1_000,
                    deaths=1,
                    players=fight_players,
                )
            ],
        )

        frame = build_dataframes(match, include="analysis")["teamfight_positioning"]

        assert len(frame) == 8  # four logical snapshots × two canonical heroes
        assert set(frame["snapshot_kind"]) == {
            "pre_engagement",
            "engagement_start",
            "first_death",
            "fight_end",
        }
        assert set(frame["engagement_start_source"]) == {"first_death_fallback"}
        assert set(frame["visibility"]) == {"unknown"}
        assert all(type(value) is str for value in frame["snapshot_kind"])
        bane = frame[frame["player_id"] == 5]
        assert bane["x"].isna().all()
        assert bane["sample_tick"].isna().all()
        assert set(bane["dire_completeness"]) == {"unavailable"}

    def test_vision_modifier_tables_are_flat_and_enum_backed_values_are_plain(self):
        match = ParsedMatch(
            vision_modifiers=[
                VisionModifierEvent(
                    100,
                    200,
                    "modifier_slardar_amplify_damage",
                    "npc_dota_hero_riki",
                    "npc_dota_hero_slardar",
                    2,
                    semantic=VisionModifierSemantic.DIRECT_TARGET_REVEAL,
                )
            ],
            vision_modifier_pairing_issues=[
                VisionModifierPairingIssue(
                    tick=300,
                    reason="unmatched",
                    modifier_name="modifier_bounty_hunter_track",
                    caster_name="",
                    target_name="npc_dota_hero_riki",
                    source=CombatLogSource.S2_BULK,
                    candidate_add_ticks=[],
                )
            ],
        )

        dfs = build_dataframes(match)

        assert dfs["vision_modifiers"].iloc[0]["semantic"] == "direct_target_reveal"
        assert dfs["vision_modifier_pairing_issues"].iloc[0]["source"] == "s2_bulk"
        assert dfs["vision_modifier_pairing_issues"].iloc[0]["candidate_add_ticks"] == ""

    def test_smoke_members_dataframe_is_flat_and_preserves_exact_ticks(self):
        match = ParsedMatch(
            smoke_events=[
                SmokeEvent(
                    tick=1_000,
                    activator="npc_dota_hero_axe",
                    team=2,
                    activation_game_time_s=10,
                    participants=[
                        SmokeParticipant(
                            hero_name="npc_dota_hero_axe",
                            player_id=0,
                            applied_tick=1_001,
                            removed_tick=1_448,
                            modifier_duration_s=45.0,
                            modifier_elapsed_duration_s=14.9,
                            applied_x=100.0,
                            applied_y=200.0,
                            removed_x=300.0,
                            removed_y=400.0,
                            applied_game_time_s=11,
                            removed_game_time_s=26,
                        )
                    ],
                )
            ]
        )

        row = build_dataframes(match)["smoke_members"].iloc[0]

        assert row["smoke_event_index"] == 0
        assert row["activation_tick"] == 1_000
        assert row["activation_game_time_s"] == 10
        assert row["activator"] == "npc_dota_hero_axe"
        assert row["applied_tick"] == 1_001
        assert row["removed_tick"] == 1_448
        assert row["modifier_elapsed_duration_s"] == 14.9
        assert row["applied_game_time_s"] == 11
        assert row["removed_game_time_s"] == 26

    def test_smoke_fight_tables_preserve_no_candidate_and_member_rows(self):
        match = ParsedMatch(
            players=[
                ParsedPlayer(
                    player_id=0,
                    hero_name="npc_dota_hero_axe",
                    team=2,
                )
            ],
            smoke_events=[
                SmokeEvent(
                    tick=1_000,
                    activator="npc_dota_hero_axe",
                    team=2,
                    activation_game_time_s=10,
                    participants=[
                        SmokeParticipant(
                            hero_name="npc_dota_hero_axe",
                            player_id=0,
                            applied_tick=1_001,
                        )
                    ],
                )
            ],
        )

        dfs = build_dataframes(match, include="analysis")
        insight = dfs["smoke_fight_insights"].iloc[0]
        member = dfs["smoke_fight_members"].iloc[0]

        assert insight["smoke_index"] == 0
        assert insight["status"] == "no_candidate"
        assert insight["activation_tick"] == 1_000
        assert insight["activation_game_time_s"] == 10
        assert member["status"] == "no_candidate"
        assert member["player_id"] == 0
        assert member["authoritative_visibility"] == "unknown"
        assert dfs["smoke_fight_followups"].empty

    def test_farming_route_tables_preserve_segments_points_and_missing_evidence(self):
        player = ParsedPlayer(
            player_id=0,
            hero_name="npc_dota_hero_axe",
            team=2,
            position_log=[(0, 8647.0, 15564.0), (150, 8650.0, 15564.0)],
        )
        match = ParsedMatch(players=[player])

        dfs = build_dataframes(match, include="analysis")
        route = dfs["farming_routes"].iloc[0]
        segment = dfs["farming_route_segments"].iloc[0]
        points = dfs["farming_route_points"]

        assert route["camp_catalog_version"] == 2
        assert route["camp_map_patch"] == "7.40"
        assert route["camp_topology_patch"] == "7.41"
        assert route["status"] == "partial"
        assert route["segment_count"] == 1
        assert segment["camp_id"] == 1
        assert segment["evidence_strength"] == "weak_farm_evidence"
        assert segment["window_xp_delta"] is None
        assert segment["window_total_earned_gold_delta"] is None
        assert segment["camp_owner_team"] == 2
        assert segment["camp_lane"] == "top"
        assert segment["camp_catalog_version"] == 2
        assert segment["camp_map_patch"] == "7.40"
        assert segment["camp_topology_patch"] == "7.41"
        assert segment["context_camp_side"] == "own_side"
        assert segment["context_status"] == "partial"
        assert "own_side" in segment["context_tags"]
        assert "incomplete_context" in segment["context_tags"]
        assert set(dfs["farming_context_tags"]["tag"]) >= {
            "own_side",
            "incomplete_context",
        }
        assert list(points["segment_index"]) == [1, 1]
        assert list(points["inside_base_zone"]) == [True, True]

    def test_minute_tables_include_authoritative_game_time_axis(self):
        pp = ParsedPlayer(
            player_id=0,
            team=2,
            times_min=[12_345, 14_145],
            gold_t_min=[600, 700],
            game_times_min=[0, 60],
        )
        match = ParsedMatch(
            players=[pp],
            radiant_gold_adv=[100, 250],
            radiant_xp_adv=[50, 125],
            game_times_min=[0, 60],
        )

        dfs = build_dataframes(match)

        assert list(dfs["players_minute"]["game_time_s"]) == [0, 60]
        assert list(dfs["players_minute"]["minute"]) == [0, 1]
        assert list(dfs["radiant_advantage"]["game_time_s"]) == [0, 60]
        assert list(dfs["radiant_advantage"]["minute"]) == [0, 1]

        legacy = ParsedMatch(radiant_gold_adv=[100, 250], radiant_xp_adv=[50, 125])
        legacy_adv = build_dataframes(legacy)["radiant_advantage"]
        assert list(legacy_adv["game_time_s"]) == [0, 60]
        assert list(legacy_adv["minute"]) == [0, 1]

    def test_neutral_item_finds_dataframe_includes_event_fields(self):
        neutral_event_cls = getattr(model_module, "NeutralItemFoundEvent", None)
        assert neutral_event_cls is not None
        match = ParsedMatch(
            neutral_item_finds=[
                neutral_event_cls(
                    tick=29858,
                    player_id=6,
                    item_ability_id=1861,
                    item_key="stonefeather_satchel",
                    item_tier=4,
                    tier_item_count=2,
                    enhancement_ability_id=1865,
                    enhancement_key="enhancement_vital",
                    enhancement_level=1,
                    trinket_level=1,
                )
            ]
        )

        df = build_dataframes(match)["neutral_item_finds"]

        assert len(df) == 1
        row = df.iloc[0]
        assert row["tick"] == 29858
        assert row["player_id"] == 6
        assert row["item_ability_id"] == 1861
        assert row["item_key"] == "stonefeather_satchel"
        assert row["item_tier"] == 4
        assert row["tier_item_count"] == 2
        assert row["enhancement_ability_id"] == 1865
        assert row["enhancement_key"] == "enhancement_vital"
        assert row["enhancement_level"] == 1
        assert row["trinket_level"] == 1

    def test_objectives_dataframe_includes_new_objective_types(self):
        match = ParsedMatch(
            tormentors=[
                TormentorKill(
                    tick=1000,
                    killer="npc_dota_hero_axe",
                    killer_player_id=0,
                    kill_number=1,
                )
            ],
            shrines=[ShrineKill(tick=1100, team=2)],
            aegis_events=[AegisEvent(tick=1200, player_id=3, event_type="pickup")],
        )

        objectives_df = build_dataframes(match)["objectives"]
        assert not objectives_df.empty
        objective_types = set(objectives_df["type"].tolist())

        assert "tormentor" in objective_types
        assert "shrine" in objective_types
        assert "aegis" in objective_types

    def test_player_breakdowns_is_long_form_of_player_dicts(self):
        pp = ParsedPlayer(player_id=3)
        pp.damage = {"npc_dota_hero_lina": 900}
        pp.damage_targets = {
            "axe_counter_helix": {"npc_dota_hero_lina": 600, "npc_dota_hero_bane": 40}
        }
        pp.gold_reasons = {"12": 350}
        pp.max_hero_hit = {
            "inflictor": "axe_culling_blade",
            "key": "npc_dota_hero_lina",
            "value": 700,
            "time": 912,
        }

        dfs = build_dataframes(ParsedMatch(players=[pp]))
        breakdowns = dfs["player_breakdowns"]

        assert list(breakdowns.columns) == [
            "match_id",
            "player_id",
            "stat",
            "key",
            "subkey",
            "value",
        ]
        rows = {(row.stat, row.key, row.subkey): row.value for row in breakdowns.itertuples()}
        assert rows == {
            ("damage", "npc_dota_hero_lina", None): 900,
            ("damage_targets", "axe_counter_helix", "npc_dota_hero_lina"): 600,
            ("damage_targets", "axe_counter_helix", "npc_dota_hero_bane"): 40,
            ("gold_reasons", "12", None): 350,
        }
        summary = dfs["player_summary"].iloc[0]
        assert summary["max_hero_hit_value"] == 700
        assert summary["max_hero_hit_inflictor"] == "axe_culling_blade"
        assert summary["max_hero_hit_target"] == "npc_dota_hero_lina"
        assert summary["max_hero_hit_time"] == 912

    def test_teamfights_export_players_as_their_own_table(self):
        fight_players = [TeamfightPlayer(player_id=i) for i in range(10)]
        fight_players[2].damage_dealt = 450
        fight_players[2].ability_uses = {"axe_berserkers_call": 1}
        match = ParsedMatch(
            teamfights=[
                Teamfight(
                    start_tick=100,
                    end_tick=900,
                    first_death_tick=500,
                    last_death_tick=600,
                    deaths=2,
                    players=fight_players,
                )
            ]
        )

        dfs = build_dataframes(match)

        assert "players" not in dfs["teamfights"].columns
        assert dfs["teamfights"].iloc[0]["fight_index"] == 0
        fight_rows = dfs["teamfight_players"]
        assert len(fight_rows) == 10
        assert "ability_uses" not in fight_rows.columns
        assert fight_rows.set_index("player_id").loc[2, "damage_dealt"] == 450

    def test_smoke_events_join_smoked_and_drop_participants(self):
        match = ParsedMatch(
            smoke_events=[
                SmokeEvent(
                    tick=1_000,
                    activator="npc_dota_hero_axe",
                    team=2,
                    smoked=["npc_dota_hero_axe", "npc_dota_hero_lina"],
                    participants=[
                        SmokeParticipant(
                            hero_name="npc_dota_hero_axe", player_id=0, applied_tick=1_001
                        )
                    ],
                )
            ]
        )

        row = build_dataframes(match)["smoke_events"].iloc[0]

        assert "participants" not in row.index
        assert row["smoked"] == "npc_dota_hero_axe;npc_dota_hero_lina"

    def test_core_tables_hold_only_primitive_cells(self):
        pp = ParsedPlayer(
            player_id=0,
            hero_name="npc_dota_hero_axe",
            team=2,
            times=[30, 60],
            gold_t=[500, 600],
            times_min=[30],
            gold_t_min=[500],
            position_log=[(30, 1.0, 2.0)],
        )
        pp.damage = {"npc_dota_hero_lina": 900}
        pp.damage_targets = {"axe_counter_helix": {"npc_dota_hero_lina": 600}}
        pp.lane_pos = {"64_64": 3}
        pp.max_hero_hit = {"inflictor": "axe_culling_blade", "key": "x", "value": 1, "time": 2}
        pp.kills_log = [CombatLogEntry(tick=10, log_type=CombatLogType.DEATH)]
        match = ParsedMatch(
            players=[pp],
            combat_log=[CombatLogEntry(tick=10, log_type=CombatLogType.DAMAGE, value=5)],
            teamfights=[
                Teamfight(
                    start_tick=1,
                    end_tick=2,
                    first_death_tick=1,
                    last_death_tick=1,
                    deaths=1,
                    players=[TeamfightPlayer(player_id=0, item_uses={"blink": 1})],
                )
            ],
            smoke_events=[SmokeEvent(tick=1, activator="a", team=2, smoked=["a"])],
            vision_modifiers=[VisionModifierEvent(1, 2, "m", "t", "c", 2, evidence_gaps=["gap"])],
            vision_modifier_pairing_issues=[
                VisionModifierPairingIssue(
                    tick=3,
                    reason="unmatched",
                    modifier_name="m",
                    caster_name="",
                    target_name="t",
                    source=CombatLogSource.S2_BULK,
                    candidate_add_ticks=[1, 2],
                )
            ],
        )

        dfs = build_dataframes(match)

        for name, df in dfs.items():
            for column in df.columns:
                nested = [v for v in df[column] if isinstance(v, (dict, list, tuple, set))]
                assert not nested, f"{name}.{column} holds nested cells: {nested[:1]}"
