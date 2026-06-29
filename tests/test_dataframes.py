"""Tests for gem.results.dataframes conversion helpers."""

from __future__ import annotations

import gem.results.models as model_module
from gem.combat.log import CombatLogEntry, CombatLogType
from gem.extractors.objectives import AegisEvent, ShrineKill, TormentorKill, TowerKill
from gem.results.dataframes import build_dataframes
from gem.results.models import ParsedMatch, ParsedPlayer, VisionModifierEvent


class TestBuildDataframes:
    def test_players_dataframe_includes_damage_type_columns(self):
        pp = ParsedPlayer(
            player_id=0,
            hero_name="npc_dota_hero_axe",
            team=2,
            times=[30],
            gold_t=[500],
            total_earned_gold_t=[900],
            lh_t=[10],
            dn_t=[2],
            xp_t=[600],
        )
        pp.damage_by_type = {"physical": 1200, "magical": 300, "pure": 50}
        pp.damage_taken_by_type = {"physical": 800, "magical": 450, "pure": 20}

        match = ParsedMatch(players=[pp] + [ParsedPlayer(player_id=i) for i in range(1, 10)])

        dfs = build_dataframes(match)
        players_df = dfs["players"]

        assert "damage_physical" in players_df.columns
        assert "damage_magical" in players_df.columns
        assert "damage_pure" in players_df.columns
        assert "damage_taken_physical" in players_df.columns
        assert "damage_taken_magical" in players_df.columns
        assert "damage_taken_pure" in players_df.columns

        row = players_df.iloc[0]
        assert row["gold"] == 500
        assert row["total_earned_gold"] == 900
        assert row["damage_physical"] == 1200
        assert row["damage_magical"] == 300
        assert row["damage_pure"] == 50
        assert row["damage_taken_physical"] == 800
        assert row["damage_taken_magical"] == 450
        assert row["damage_taken_pure"] == 20

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

    def test_build_dataframes_returns_extended_parity_keys(self):
        match = ParsedMatch()
        dfs = build_dataframes(match)

        assert "players" in dfs
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
        assert "opendota_teamfights" in dfs
        assert "smoke_events" in dfs
        assert "vision_modifiers" in dfs
        assert "courier_snapshots" in dfs
        assert "neutral_item_finds" in dfs
        assert "player_kills_log" in dfs
        assert "player_purchase_log" in dfs
        assert "player_runes_log" in dfs
        assert "player_buyback_log" in dfs

        assert dfs["neutral_item_finds"].empty
        assert dfs["opendota_teamfights"].empty
        assert dfs["vision_modifiers"].empty

    def test_empty_dataframes_keep_stable_columns(self):
        dfs = build_dataframes(ParsedMatch())
        combat_log_columns = [
            "tick",
            "log_type",
            "attacker_name",
            "damage_source_name",
            "target_name",
            "inflictor_name",
            "value",
            "attacker_is_hero",
            "target_is_hero",
            "attacker_is_illusion",
            "target_is_illusion",
            "ability_level",
            "gold_reason",
            "xp_reason",
            "value_name",
            "damage_type",
            "stun_duration",
            "neutral_camp_type",
            "neutral_camp_team",
            "location_x",
            "location_y",
            "timestamp_s",
            "game_time_s",
            "will_reincarnate",
        ]
        player_log_columns = [*combat_log_columns, "player_id"]

        expected_columns = {
            "players": [
                "player_id",
                "player_name",
                "hero_name",
                "team",
                "tick",
                "gold",
                "total_earned_gold",
                "net_worth",
                "lh",
                "dn",
                "xp",
                "kills",
                "deaths",
                "assists",
                "stuns_dealt",
                "lane_role",
                "lane_last_hits",
                "lane_denies",
                "lane_total_gold",
                "lane_total_xp",
                "lane_efficiency_pct",
                "lane_gold_adv",
                "lane_xp_adv",
                "final_net_worth",
                "final_last_hits",
                "final_denies",
                "camps_stacked",
                "creeps_stacked",
                "obs_placed",
                "sen_placed",
                "rune_pickups",
                "tower_kills",
                "kda",
                "buyback_count",
                "is_radiant",
                "win",
                "kills_per_min",
                "gold_per_min",
                "xp_per_min",
                "total_gold",
                "total_xp",
                "hero_damage",
                "tower_damage",
                "hero_healing",
                "damage_physical",
                "damage_magical",
                "damage_pure",
                "damage_taken_physical",
                "damage_taken_magical",
                "damage_taken_pure",
                "damage",
                "damage_taken",
                "damage_inflictor",
                "damage_inflictor_received",
                "damage_targets",
                "ability_targets",
                "hero_hits",
                "max_hero_hit",
                "healing",
                "ability_uses",
                "item_uses",
                "purchase",
                "purchase_time",
                "first_purchase_time",
                "purchase_tpscroll",
                "purchase_ward_observer",
                "purchase_ward_sentry",
                "observer_uses",
                "sentry_uses",
                "observers_placed",
                "gold_reasons",
                "xp_reasons",
                "lane_pos",
            ],
            "players_minute": [
                "player_id",
                "player_name",
                "hero_name",
                "team",
                "tick",
                "gold",
                "total_earned_gold",
                "total_earned_xp",
                "net_worth",
                "lh",
                "dn",
                "xp",
            ],
            "positions": ["player_id", "hero_name", "team", "tick", "x", "y"],
            "objectives": [
                "type",
                "tick",
                "team",
                "name",
                "killer",
                "kill_number",
                "drops",
                "killer_player_id",
                "player_id",
                "event_type",
                "x",
                "y",
            ],
            "opendota_objectives": [
                "time",
                "type",
                "key",
                "unit",
                "slot",
                "player_slot",
                "team",
                "killer",
            ],
            "wards": [
                "tick",
                "player_id",
                "placer",
                "ward_type",
                "team",
                "x",
                "y",
                "expires_tick",
                "killed_tick",
                "killer",
            ],
            "combat_log": combat_log_columns,
            "player_kills_log": player_log_columns,
            "player_purchase_log": player_log_columns,
            "player_runes_log": player_log_columns,
            "player_buyback_log": [*player_log_columns, "cost", "net_worth"],
            "chat": ["tick", "player_slot", "channel", "text"],
            "match": [
                "match_id",
                "game_mode",
                "leagueid",
                "radiant_win",
                "game_start_tick",
                "game_end_tick",
                "tower_status_radiant",
                "tower_status_dire",
                "barracks_status_radiant",
                "barracks_status_dire",
                "parse_error",
                "truncated_at_tick",
            ],
            "radiant_advantage": ["minute", "radiant_gold_adv", "radiant_xp_adv"],
            "draft": ["tick", "slot_index", "hero_id", "hero_name", "is_pick", "team"],
            "teamfights": [
                "start_tick",
                "end_tick",
                "last_death_tick",
                "deaths",
                "first_death_tick",
                "radiant_kills",
                "dire_kills",
                "winner",
                "centroid_x",
                "centroid_y",
                "centroid_n",
                "players",
            ],
            "opendota_teamfights": ["start", "end", "last_death", "deaths", "players"],
            "smoke_events": ["tick", "activator", "team", "smoked", "x", "y"],
            "vision_modifiers": [
                "tick",
                "end_tick",
                "modifier_name",
                "target_name",
                "caster_name",
                "caster_team",
            ],
            "courier_snapshots": ["tick", "team", "state", "flying", "x", "y"],
            "neutral_item_finds": [
                "tick",
                "player_id",
                "item_ability_id",
                "item_key",
                "item_tier",
                "tier_item_count",
                "enhancement_ability_id",
                "enhancement_key",
                "enhancement_level",
                "trinket_level",
            ],
        }

        assert set(dfs) == set(expected_columns)
        for name, columns in expected_columns.items():
            assert list(dfs[name].columns) == columns, name

    def test_heterogeneous_tables_keep_declared_columns_when_non_empty(self):
        match = ParsedMatch(
            towers=[
                TowerKill(
                    tick=100,
                    team=3,
                    killer="npc_dota_hero_axe",
                    tower_name="npc_dota_badguys_tower1_mid",
                )
            ],
            objectives=[
                {
                    "time": 10,
                    "type": "building_kill",
                    "key": "npc_dota_badguys_tower1_mid",
                    "unit": "npc_dota_hero_axe",
                    "custom_field": "preserved",
                }
            ],
        )

        dfs = build_dataframes(match)

        assert list(dfs["objectives"].columns) == [
            "type",
            "tick",
            "team",
            "name",
            "killer",
            "kill_number",
            "drops",
            "killer_player_id",
            "player_id",
            "event_type",
            "x",
            "y",
        ]
        assert list(dfs["opendota_objectives"].columns) == [
            "time",
            "type",
            "key",
            "unit",
            "slot",
            "player_slot",
            "team",
            "killer",
            "custom_field",
        ]
        assert dfs["opendota_objectives"].iloc[0]["custom_field"] == "preserved"

    def test_vision_modifiers_dataframe_includes_event_fields(self):
        match = ParsedMatch(
            vision_modifiers=[
                VisionModifierEvent(
                    tick=100,
                    end_tick=200,
                    modifier_name="modifier_bounty_hunter_track",
                    target_name="npc_dota_hero_axe",
                    caster_name="npc_dota_hero_bounty_hunter",
                    caster_team=3,
                )
            ]
        )

        df = build_dataframes(match)["vision_modifiers"]

        assert len(df) == 1
        row = df.iloc[0]
        assert row["tick"] == 100
        assert row["end_tick"] == 200
        assert row["modifier_name"] == "modifier_bounty_hunter_track"
        assert row["target_name"] == "npc_dota_hero_axe"
        assert row["caster_name"] == "npc_dota_hero_bounty_hunter"
        assert row["caster_team"] == 3

    def test_match_dataframe_includes_partial_parse_metadata(self):
        match = ParsedMatch(parse_error="bad tail", truncated_at_tick=1234)

        row = build_dataframes(match)["match"].iloc[0]

        assert row["parse_error"] == "bad tail"
        assert row["truncated_at_tick"] == 1234

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
