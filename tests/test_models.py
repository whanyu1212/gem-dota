"""Tests for gem.models — ParsedPlayer and ParsedMatch dataclasses."""

from __future__ import annotations

from collections import defaultdict

from gem.models import ParsedMatch, ParsedPlayer


class TestParsedPlayerLanePos:
    def test_lane_pos_is_defaultdict(self):
        assert isinstance(ParsedPlayer(player_id=0).lane_pos, defaultdict)

    def test_missing_key_returns_zero(self):
        assert ParsedPlayer(player_id=0).lane_pos["100_200"] == 0

    def test_accumulates(self):
        pp = ParsedPlayer(player_id=0)
        pp.lane_pos["50_60"] += 1
        pp.lane_pos["50_60"] += 1
        assert pp.lane_pos["50_60"] == 2

    def test_independent_players(self):
        p1, p2 = ParsedPlayer(player_id=0), ParsedPlayer(player_id=1)
        p1.lane_pos["10_20"] += 5
        assert p2.lane_pos["10_20"] == 0


class TestParsedPlayerRepr:
    def test_slot_hero_team_kda(self):
        pp = ParsedPlayer(
            player_id=3,
            hero_name="npc_dota_hero_axe",
            team=2,
            kills=5,
            deaths=2,
            assists=8,
        )
        r = repr(pp)
        assert "slot=3" in r
        assert "axe" in r
        assert "Radiant" in r
        assert "5/2/8" in r

    def test_dire_team(self):
        assert "Dire" in repr(ParsedPlayer(player_id=7, team=3))

    def test_unknown_team(self):
        assert "team=0" in repr(ParsedPlayer(player_id=0, team=0))

    def test_no_hero_shows_unknown(self):
        assert "unknown" in repr(ParsedPlayer(player_id=0))


class TestParsedMatchRepr:
    def test_radiant_win(self):
        r = repr(ParsedMatch(match_id=12345, radiant_win=True))
        assert "12345" in r
        assert "Radiant" in r

    def test_dire_win(self):
        assert "Dire" in repr(ParsedMatch(match_id=99, radiant_win=False))

    def test_unknown_winner(self):
        assert "?" in repr(ParsedMatch(match_id=0, radiant_win=None))

    def test_player_count(self):
        assert "players=10" in repr(ParsedMatch())
