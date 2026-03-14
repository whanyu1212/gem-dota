"""Tests for gem.dataframes conversion helpers."""

from __future__ import annotations

from gem.dataframes import build_dataframes
from gem.models import ParsedMatch, ParsedPlayer


class TestBuildDataframes:
    def test_players_dataframe_includes_damage_type_columns(self):
        pp = ParsedPlayer(
            player_id=0,
            hero_name="npc_dota_hero_axe",
            team=2,
            times=[30],
            gold_t=[500],
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
        assert row["damage_physical"] == 1200
        assert row["damage_magical"] == 300
        assert row["damage_pure"] == 50
        assert row["damage_taken_physical"] == 800
        assert row["damage_taken_magical"] == 450
        assert row["damage_taken_pure"] == 20
