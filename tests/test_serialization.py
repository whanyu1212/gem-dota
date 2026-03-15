"""Tests for gem serialization helpers."""

from __future__ import annotations

import json
from collections import defaultdict

import gem
from gem.models import ParsedMatch, ParsedPlayer


class TestSerializationHelpers:
    def test_to_dict_converts_defaultdict_and_tuples(self):
        pp = ParsedPlayer(
            player_id=0,
            hero_name="npc_dota_hero_axe",
            team=2,
            times=[30],
            position_log=[(30, 100.5, -50.25)],
        )
        pp.lane_pos = defaultdict(int, {"100_200": 3})

        match = ParsedMatch(
            match_id=42,
            players=[pp] + [ParsedPlayer(player_id=i) for i in range(1, 10)],
        )

        data = gem.to_dict(match)

        assert isinstance(data, dict)
        assert data["match_id"] == 42
        assert isinstance(data["players"][0]["lane_pos"], dict)
        assert data["players"][0]["lane_pos"]["100_200"] == 3
        assert isinstance(data["players"][0]["position_log"], list)
        assert data["players"][0]["position_log"][0] == [30, 100.5, -50.25]

    def test_to_json_returns_valid_json(self):
        match = ParsedMatch(match_id=7)
        payload = gem.to_json(match, sort_keys=True)

        decoded = json.loads(payload)
        assert decoded["match_id"] == 7
        assert "players" in decoded

    def test_parse_to_json_uses_parse_result(self, monkeypatch):
        fake_match = ParsedMatch(match_id=999)

        monkeypatch.setattr(gem, "parse", lambda path: fake_match)

        payload = gem.parse_to_json("dummy.dem")
        decoded = json.loads(payload)

        assert decoded["match_id"] == 999
