"""Tests for gem.find_player — hero-name convenience lookup."""

from __future__ import annotations

from unittest.mock import MagicMock

import gem


def _make_match(*hero_names: str) -> gem.ParsedMatch:
    """Build a fake ParsedMatch with players using the given hero NPC names."""
    players = []
    for i, npc in enumerate(hero_names):
        p = MagicMock(spec=gem.ParsedPlayer)
        p.hero_name = npc
        p.player_id = i
        players.append(p)

    m = MagicMock(spec=gem.ParsedMatch)
    m.players = players
    return m


class TestFindPlayerByDisplayName:
    def test_finds_by_exact_display_name(self) -> None:
        match = _make_match("npc_dota_hero_axe", "npc_dota_hero_antimage")
        result = gem.find_player(match, "Axe")
        assert result is not None
        assert result.hero_name == "npc_dota_hero_axe"

    def test_case_insensitive_display_name(self) -> None:
        match = _make_match("npc_dota_hero_axe")
        assert gem.find_player(match, "axe") is not None
        assert gem.find_player(match, "AXE") is not None

    def test_hyphenated_display_name(self) -> None:
        match = _make_match("npc_dota_hero_antimage")
        result = gem.find_player(match, "Anti-Mage")
        assert result is not None
        assert result.hero_name == "npc_dota_hero_antimage"

    def test_spaced_display_name(self) -> None:
        match = _make_match("npc_dota_hero_antimage")
        assert gem.find_player(match, "anti mage") is not None


class TestFindPlayerByNpcName:
    def test_finds_by_full_npc_name(self) -> None:
        match = _make_match("npc_dota_hero_axe")
        result = gem.find_player(match, "npc_dota_hero_axe")
        assert result is not None
        assert result.hero_name == "npc_dota_hero_axe"

    def test_bare_suffix(self) -> None:
        # "axe" should fall back to npc_dota_hero_axe
        match = _make_match("npc_dota_hero_axe")
        result = gem.find_player(match, "axe")
        assert result is not None


class TestFindPlayerNotFound:
    def test_returns_none_when_hero_absent(self) -> None:
        match = _make_match("npc_dota_hero_axe")
        assert gem.find_player(match, "Anti-Mage") is None

    def test_returns_none_empty_roster(self) -> None:
        match = _make_match()
        assert gem.find_player(match, "Axe") is None

    def test_returns_none_unknown_name(self) -> None:
        match = _make_match("npc_dota_hero_axe")
        assert gem.find_player(match, "Definitely Not A Hero") is None


class TestFindPlayerCorrectPlayer:
    def test_returns_correct_player_among_many(self) -> None:
        match = _make_match(
            "npc_dota_hero_axe",
            "npc_dota_hero_antimage",
            "npc_dota_hero_shadow_demon",
        )
        result = gem.find_player(match, "Anti-Mage")
        assert result is not None
        assert result.hero_name == "npc_dota_hero_antimage"
        assert result.player_id == 1
