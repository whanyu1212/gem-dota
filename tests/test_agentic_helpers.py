"""Tests for the four agentic helper functions.

Covers:
    teamfight_at_tick  — tick → Teamfight lookup
    heroes_near        — spatial hero query
    ability_level_at_tick — ability level at cast time
    Teamfight.winner / radiant_kills / dire_kills — fight outcome fields
"""

from __future__ import annotations

from unittest.mock import MagicMock

from gem.analysis import ability_level_at_tick, heroes_near, teamfight_at_tick
from gem.combatlog import CombatLogEntry
from gem.extractors.teamfights import (
    Teamfight,
    TeamfightPlayer,
    detect_teamfights,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _fight(start: int, end: int, last_death: int | None = None, deaths: int = 1) -> Teamfight:
    return Teamfight(
        start_tick=start,
        end_tick=end,
        last_death_tick=last_death if last_death is not None else end,
        deaths=deaths,
        players=[TeamfightPlayer(player_id=i) for i in range(10)],
    )


def _match(fights: list[Teamfight], players=None) -> MagicMock:
    m = MagicMock()
    m.teamfights = fights
    m.players = players or []
    return m


def _player(hero: str, team: int, position_log: list[tuple[int, float, float]]) -> MagicMock:
    p = MagicMock()
    p.hero_name = hero
    p.team = team
    p.position_log = position_log
    p.player_id = 0
    return p


def _death_entry(**kwargs) -> CombatLogEntry:
    defaults = {
        "tick": 0,
        "log_type": "DEATH",
        "attacker_name": "npc_dota_hero_axe",
        "target_name": "npc_dota_hero_antimage",
        "inflictor_name": "",
        "value": 0,
        "attacker_is_hero": True,
        "target_is_hero": True,
        "attacker_is_illusion": False,
        "target_is_illusion": False,
        "damage_type": "",
        "stun_duration": 0.0,
    }
    defaults.update(kwargs)
    return CombatLogEntry(**defaults)


# ---------------------------------------------------------------------------
# teamfight_at_tick
# ---------------------------------------------------------------------------


class TestTeamfightAtTick:
    def test_empty_fights_returns_none(self) -> None:
        match = _match([])
        assert teamfight_at_tick(match, 500) is None

    def test_tick_inside_fight_returns_fight(self) -> None:
        f = _fight(100, 300)
        match = _match([f])
        assert teamfight_at_tick(match, 200) is f

    def test_tick_at_start_boundary(self) -> None:
        f = _fight(100, 300)
        match = _match([f])
        assert teamfight_at_tick(match, 100) is f

    def test_tick_at_end_boundary(self) -> None:
        f = _fight(100, 300)
        match = _match([f])
        assert teamfight_at_tick(match, 300) is f

    def test_tick_before_all_fights(self) -> None:
        f = _fight(100, 300)
        match = _match([f])
        assert teamfight_at_tick(match, 50) is None

    def test_tick_after_all_fights(self) -> None:
        f = _fight(100, 300)
        match = _match([f])
        assert teamfight_at_tick(match, 400) is None

    def test_tick_in_gap_between_fights(self) -> None:
        f1 = _fight(100, 200)
        f2 = _fight(400, 600)
        match = _match([f1, f2])
        assert teamfight_at_tick(match, 300) is None

    def test_selects_correct_fight_among_multiple(self) -> None:
        f1 = _fight(100, 300)
        f2 = _fight(500, 700)
        f3 = _fight(900, 1100)
        match = _match([f1, f2, f3])
        assert teamfight_at_tick(match, 600) is f2

    def test_returns_none_when_tick_just_after_fight_end(self) -> None:
        f = _fight(100, 300)
        match = _match([f])
        assert teamfight_at_tick(match, 301) is None


# ---------------------------------------------------------------------------
# heroes_near
# ---------------------------------------------------------------------------


class TestHeroesNear:
    def test_empty_players_returns_empty(self) -> None:
        match = _match([], players=[])
        assert heroes_near(match, 100, 0.0, 0.0, 1000) == []

    def test_hero_within_radius_included(self) -> None:
        p = _player("npc_dota_hero_axe", 2, [(100, 0.0, 0.0)])
        match = _match([], players=[p])
        result = heroes_near(match, 100, 0.0, 0.0, 500)
        assert result == [p]

    def test_hero_outside_radius_excluded(self) -> None:
        p = _player("npc_dota_hero_axe", 2, [(100, 1000.0, 0.0)])
        match = _match([], players=[p])
        result = heroes_near(match, 100, 0.0, 0.0, 500)
        assert result == []

    def test_hero_exactly_at_radius_included(self) -> None:
        p = _player("npc_dota_hero_axe", 2, [(100, 500.0, 0.0)])
        match = _match([], players=[p])
        result = heroes_near(match, 100, 0.0, 0.0, 500)
        assert result == [p]

    def test_hero_with_no_position_log_excluded(self) -> None:
        p = _player("npc_dota_hero_axe", 2, [])
        match = _match([], players=[p])
        result = heroes_near(match, 100, 0.0, 0.0, 9999)
        assert result == []

    def test_result_sorted_by_distance(self) -> None:
        p_far = _player("npc_dota_hero_axe", 2, [(100, 800.0, 0.0)])
        p_near = _player("npc_dota_hero_antimage", 3, [(100, 200.0, 0.0)])
        match = _match([], players=[p_far, p_near])
        result = heroes_near(match, 100, 0.0, 0.0, 1000)
        assert result == [p_near, p_far]

    def test_multiple_heroes_some_outside_radius(self) -> None:
        inside1 = _player("npc_dota_hero_axe", 2, [(100, 100.0, 0.0)])
        inside2 = _player("npc_dota_hero_antimage", 3, [(100, 200.0, 0.0)])
        outside = _player("npc_dota_hero_invoker", 2, [(100, 5000.0, 0.0)])
        match = _match([], players=[inside1, inside2, outside])
        result = heroes_near(match, 100, 0.0, 0.0, 500)
        assert outside not in result
        assert inside1 in result
        assert inside2 in result


# ---------------------------------------------------------------------------
# ability_level_at_tick
# ---------------------------------------------------------------------------


class TestAbilityLevelAtTick:
    def _player_with_snapshots(self, snapshots: list[tuple[int, dict]]) -> MagicMock:
        p = MagicMock()
        p._ability_snapshots = snapshots
        return p

    def test_no_snapshots_returns_zero(self) -> None:
        p = self._player_with_snapshots([])
        assert ability_level_at_tick(p, "axe_berserkers_call", 100) == 0

    def test_missing_attribute_returns_zero(self) -> None:
        p = MagicMock(spec=[])  # no _ability_snapshots attribute
        assert ability_level_at_tick(p, "axe_berserkers_call", 100) == 0

    def test_ability_not_yet_learned(self) -> None:
        p = self._player_with_snapshots([(1800, {"axe_berserkers_call": 1})])
        # Tick before first snapshot
        assert ability_level_at_tick(p, "axe_berserkers_call", 100) == 0

    def test_ability_level_at_exact_snapshot_tick(self) -> None:
        p = self._player_with_snapshots([(1800, {"axe_berserkers_call": 2})])
        assert ability_level_at_tick(p, "axe_berserkers_call", 1800) == 2

    def test_ability_level_after_snapshot_tick(self) -> None:
        p = self._player_with_snapshots([(1800, {"axe_berserkers_call": 2})])
        assert ability_level_at_tick(p, "axe_berserkers_call", 9999) == 2

    def test_returns_latest_level_before_tick(self) -> None:
        p = self._player_with_snapshots(
            [
                (1800, {"axe_berserkers_call": 1}),
                (3600, {"axe_berserkers_call": 2}),
                (5400, {"axe_berserkers_call": 3}),
            ]
        )
        assert ability_level_at_tick(p, "axe_berserkers_call", 4000) == 2

    def test_unknown_ability_returns_zero(self) -> None:
        p = self._player_with_snapshots([(1800, {"axe_berserkers_call": 3})])
        assert ability_level_at_tick(p, "axe_culling_blade", 5000) == 0

    def test_multiple_abilities_independent(self) -> None:
        p = self._player_with_snapshots(
            [
                (1800, {"axe_berserkers_call": 1, "axe_battle_hunger": 2}),
            ]
        )
        assert ability_level_at_tick(p, "axe_berserkers_call", 2000) == 1
        assert ability_level_at_tick(p, "axe_battle_hunger", 2000) == 2


# ---------------------------------------------------------------------------
# Teamfight.winner / radiant_kills / dire_kills
# ---------------------------------------------------------------------------


class TestTeamfightOutcome:
    def _make_entries(self, deaths: list[tuple[int, str, str]]) -> list[CombatLogEntry]:
        """deaths = list of (tick, attacker_npc, target_npc)."""
        return [_death_entry(tick=t, attacker_name=atk, target_name=tgt) for t, atk, tgt in deaths]

    def test_radiant_win(self) -> None:
        # Axe (Radiant) kills Anti-Mage and Invoker (both Dire)
        entries = self._make_entries(
            [
                (100, "npc_dota_hero_axe", "npc_dota_hero_antimage"),
                (200, "npc_dota_hero_axe", "npc_dota_hero_invoker"),
            ]
        )
        h2s = {
            "npc_dota_hero_axe": 0,
            "npc_dota_hero_antimage": 5,
            "npc_dota_hero_invoker": 6,
        }
        s2t = {0: 2, 5: 3, 6: 3}  # slot → team
        fights = detect_teamfights(entries, hero_to_slot=h2s, slot_to_team=s2t)
        assert len(fights) == 1
        f = fights[0]
        assert f.radiant_kills == 2
        assert f.dire_kills == 0
        assert f.winner == "radiant"

    def test_dire_win(self) -> None:
        entries = self._make_entries(
            [
                (100, "npc_dota_hero_antimage", "npc_dota_hero_axe"),
            ]
        )
        h2s = {"npc_dota_hero_axe": 0, "npc_dota_hero_antimage": 5}
        s2t = {0: 2, 5: 3}
        fights = detect_teamfights(entries, hero_to_slot=h2s, slot_to_team=s2t)
        assert fights[0].winner == "dire"
        assert fights[0].dire_kills == 1
        assert fights[0].radiant_kills == 0

    def test_draw(self) -> None:
        entries = self._make_entries(
            [
                (100, "npc_dota_hero_axe", "npc_dota_hero_antimage"),
                (110, "npc_dota_hero_antimage", "npc_dota_hero_axe"),
            ]
        )
        h2s = {"npc_dota_hero_axe": 0, "npc_dota_hero_antimage": 5}
        s2t = {0: 2, 5: 3}
        fights = detect_teamfights(entries, hero_to_slot=h2s, slot_to_team=s2t)
        assert fights[0].winner == "draw"
        assert fights[0].radiant_kills == 1
        assert fights[0].dire_kills == 1

    def test_unknown_without_slot_to_team(self) -> None:
        entries = self._make_entries(
            [
                (100, "npc_dota_hero_axe", "npc_dota_hero_antimage"),
            ]
        )
        h2s = {"npc_dota_hero_axe": 0, "npc_dota_hero_antimage": 5}
        fights = detect_teamfights(entries, hero_to_slot=h2s)
        assert fights[0].winner == "unknown"
        assert fights[0].radiant_kills == 0
        assert fights[0].dire_kills == 0

    def test_illusion_deaths_not_counted(self) -> None:
        entries = [
            _death_entry(
                tick=100,
                attacker_name="npc_dota_hero_axe",
                target_name="npc_dota_hero_antimage",
                target_is_illusion=True,
            )
        ]
        h2s = {"npc_dota_hero_axe": 0, "npc_dota_hero_antimage": 5}
        s2t = {0: 2, 5: 3}
        fights = detect_teamfights(entries, hero_to_slot=h2s, slot_to_team=s2t)
        # Illusion deaths don't open a fight window
        assert fights == []
