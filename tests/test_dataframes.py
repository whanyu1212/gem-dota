"""Tests for gem.results.dataframes conversion helpers."""

from __future__ import annotations

import gem.results.models as model_module
from gem.combat.log import CombatLogEntry, CombatLogType
from gem.extractors.objectives import AegisEvent, ShrineKill, TormentorKill
from gem.results.dataframes import build_dataframes
from gem.results.models import ParsedMatch, ParsedPlayer


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
            aghanims_scepter=1,
            aghanims_shard=0,
            moonshard=1,
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
        assert "courier_snapshots" in dfs
        assert "neutral_item_finds" in dfs
        assert "player_kills_log" in dfs
        assert "player_purchase_log" in dfs
        assert "player_runes_log" in dfs
        assert "player_buyback_log" in dfs

        assert dfs["neutral_item_finds"].empty
        assert dfs["opendota_teamfights"].empty

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
