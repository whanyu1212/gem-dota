"""Tests for gem.dataframes conversion helpers."""

from __future__ import annotations

from gem.dataframes import build_dataframes
from gem.extractors.objectives import AegisEvent, ShrineKill, TormentorKill
from gem.models import ParsedMatch, ParsedPlayer


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
        assert "smoke_events" in dfs
        assert "courier_snapshots" in dfs
        assert "player_kills_log" in dfs
        assert "player_purchase_log" in dfs
        assert "player_runes_log" in dfs
        assert "player_buyback_log" in dfs

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
