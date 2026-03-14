"""Tests for teamfight detection.

Unit tests use synthetic combat log entries.
Integration tests parse a real .dem fixture and verify plausible output.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from gem.combatlog import CombatLogEntry
from gem.extractors.teamfights import detect_teamfights

FIXTURE = Path(__file__).parent / "fixtures" / "ti14_finals_g1_xg_vs_falcons.dem"

_COOLDOWN = 15 * 30  # 450 ticks


def _death(tick: int, target: str = "npc_dota_hero_axe", illusion: bool = False) -> CombatLogEntry:
    return CombatLogEntry(
        tick=tick,
        log_type="DEATH",
        target_name=target,
        target_is_hero=True,
        target_is_illusion=illusion,
    )


def _damage(tick: int, attacker: str, target: str, value: int = 100) -> CombatLogEntry:
    return CombatLogEntry(
        tick=tick,
        log_type="DAMAGE",
        attacker_name=attacker,
        target_name=target,
        attacker_is_hero=True,
        target_is_hero=True,
        target_is_illusion=False,
        value=value,
    )


def _ability(tick: int, attacker: str, ability: str) -> CombatLogEntry:
    return CombatLogEntry(
        tick=tick,
        log_type="ABILITY",
        attacker_name=attacker,
        inflictor_name=ability,
        attacker_is_hero=True,
        attacker_is_illusion=False,
    )


# ---------------------------------------------------------------------------
# Unit tests — detect_teamfights
# ---------------------------------------------------------------------------


class TestDetectTeamfights:
    def test_empty_log_returns_empty(self):
        assert detect_teamfights([]) == []

    def test_no_hero_deaths_returns_empty(self):
        entries = [CombatLogEntry(tick=100, log_type="DAMAGE", value=50)]
        assert detect_teamfights(entries) == []

    def test_illusion_death_ignored(self):
        entries = [_death(100, illusion=True)]
        assert detect_teamfights(entries) == []

    def test_single_death_creates_one_fight(self):
        fights = detect_teamfights([_death(1000)])
        assert len(fights) == 1

    def test_fight_window_start_end(self):
        fights = detect_teamfights([_death(1000)])
        tf = fights[0]
        assert tf.start_tick == 1000 - _COOLDOWN
        assert tf.end_tick == 1000 + _COOLDOWN
        assert tf.last_death_tick == 1000

    def test_deaths_within_cooldown_merged(self):
        entries = [_death(1000), _death(1200), _death(1400)]
        fights = detect_teamfights(entries)
        assert len(fights) == 1
        assert fights[0].deaths == 3

    def test_deaths_beyond_cooldown_split_into_two(self):
        entries = [_death(1000), _death(1000 + _COOLDOWN + 1)]
        fights = detect_teamfights(entries)
        assert len(fights) == 2

    def test_deaths_count_correct(self):
        entries = [_death(1000, "npc_dota_hero_axe"), _death(1100, "npc_dota_hero_pudge")]
        fights = detect_teamfights(entries)
        assert fights[0].deaths == 2

    def test_players_list_always_10(self):
        fights = detect_teamfights([_death(1000)])
        assert len(fights[0].players) == 10

    def test_start_tick_clamped_to_zero(self):
        fights = detect_teamfights([_death(10)])  # 10 < cooldown
        assert fights[0].start_tick == 0

    def test_damage_attributed_to_attacker_and_target(self):
        h2s = {"npc_dota_hero_axe": 0, "npc_dota_hero_pudge": 1}
        entries = [
            _death(1000, "npc_dota_hero_pudge"),
            _damage(1050, "npc_dota_hero_axe", "npc_dota_hero_pudge", value=300),
        ]
        fights = detect_teamfights(entries, hero_to_slot=h2s)
        assert fights[0].players[0].damage_dealt == 300
        assert fights[0].players[1].damage_taken == 300

    def test_damage_outside_window_not_counted(self):
        h2s = {"npc_dota_hero_axe": 0, "npc_dota_hero_pudge": 1}
        entries = [
            _death(1000, "npc_dota_hero_pudge"),
            _damage(1000 + _COOLDOWN + 100, "npc_dota_hero_axe", "npc_dota_hero_pudge", value=500),
        ]
        fights = detect_teamfights(entries, hero_to_slot=h2s)
        assert fights[0].players[0].damage_dealt == 0

    def test_death_increments_target_player_deaths(self):
        h2s = {"npc_dota_hero_axe": 0}
        entries = [_death(1000, "npc_dota_hero_axe")]
        fights = detect_teamfights(entries, hero_to_slot=h2s)
        assert fights[0].players[0].deaths == 1

    def test_buyback_attributed_to_slot(self):
        entries = [
            _death(1000),
            CombatLogEntry(tick=1050, log_type="BUYBACK", value=2),
        ]
        fights = detect_teamfights(entries)
        assert fights[0].players[2].buybacks == 1

    def test_ability_use_recorded(self):
        h2s = {"npc_dota_hero_axe": 0}
        entries = [
            _death(1000),
            _ability(1050, "npc_dota_hero_axe", "axe_berserkers_call"),
        ]
        fights = detect_teamfights(entries, hero_to_slot=h2s)
        assert fights[0].players[0].ability_uses.get("axe_berserkers_call") == 1

    def test_no_hero_to_slot_damage_not_attributed(self):
        """Without hero_to_slot, damage is not attributed but no crash occurs."""
        entries = [
            _death(1000),
            _damage(1050, "npc_dota_hero_axe", "npc_dota_hero_pudge"),
        ]
        fights = detect_teamfights(entries)
        assert all(p.damage_dealt == 0 for p in fights[0].players)


# ---------------------------------------------------------------------------
# Spatial split tests
# ---------------------------------------------------------------------------


def _make_snaps(hero: str, slot: int, tick: int, x: float, y: float):
    """Return a minimal player_snapshots dict with one snapshot."""
    from gem.extractors._snapshots import PlayerStateSnapshot

    snap = PlayerStateSnapshot(
        tick=tick,
        player_id=slot,
        npc_name=hero,
        team=2,
        level=1,
        xp=0,
        gold=0,
        net_worth=0,
        total_earned_gold=0,
        total_earned_xp=0,
        lh=0,
        dn=0,
        hp=500,
        max_hp=500,
        mana=0,
        max_mana=0,
        x=x,
        y=y,
    )
    return {slot: [snap]}


class TestSpatialSplit:
    def test_nearby_deaths_not_split(self):
        """Two deaths close together on map stay in one fight."""
        h2s = {"npc_dota_hero_axe": 0, "npc_dota_hero_pudge": 1}
        snaps = {
            **_make_snaps("npc_dota_hero_axe", 0, 1000, 2000.0, 2000.0),
            **_make_snaps("npc_dota_hero_pudge", 1, 1200, 2500.0, 2000.0),
        }
        entries = [
            _death(1000, "npc_dota_hero_axe"),
            _death(1200, "npc_dota_hero_pudge"),
        ]
        fights = detect_teamfights(entries, hero_to_slot=h2s, player_snapshots=snaps)
        assert len(fights) == 1
        assert fights[0].deaths == 2

    def test_far_deaths_do_not_split_with_temporal_detection(self):
        """Two deaths within cooldown stay in one fight even if far apart."""
        h2s = {"npc_dota_hero_axe": 0, "npc_dota_hero_pudge": 1}
        snaps = {
            **_make_snaps("npc_dota_hero_axe", 0, 1000, 0.0, 0.0),
            **_make_snaps("npc_dota_hero_pudge", 1, 1200, 5000.0, 5000.0),  # far away
        }
        entries = [
            _death(1000, "npc_dota_hero_axe"),
            _death(1200, "npc_dota_hero_pudge"),
        ]
        fights = detect_teamfights(entries, hero_to_slot=h2s, player_snapshots=snaps)
        assert len(fights) == 1
        assert fights[0].deaths == 2

    def test_no_snapshots_falls_back_to_temporal_only(self):
        """Without position data spatial split is skipped; temporal logic still works."""
        entries = [_death(1000), _death(1200)]
        fights = detect_teamfights(entries)
        assert len(fights) == 1
        assert fights[0].deaths == 2


# ---------------------------------------------------------------------------
# Integration tests
# ---------------------------------------------------------------------------


@pytest.mark.slow
@pytest.mark.integration
class TestTeamfightsIntegration:
    @pytest.fixture(scope="class")
    def match(self):
        import gem

        return gem.parse(str(FIXTURE))

    def test_teamfights_detected(self, match):
        assert len(match.teamfights) > 0, "Expected at least one teamfight in TI14 game"

    def test_fight_windows_valid(self, match):
        for tf in match.teamfights:
            assert tf.start_tick < tf.end_tick
            assert tf.start_tick <= tf.last_death_tick <= tf.end_tick

    def test_deaths_positive(self, match):
        for tf in match.teamfights:
            assert tf.deaths >= 1

    def test_players_count(self, match):
        for tf in match.teamfights:
            assert len(tf.players) == 10

    def test_damage_non_negative(self, match):
        for tf in match.teamfights:
            for p in tf.players:
                assert p.damage_dealt >= 0
                assert p.damage_taken >= 0

    def test_some_fights_have_multiple_deaths(self, match):
        multi = [tf for tf in match.teamfights if tf.deaths >= 2]
        assert len(multi) > 0, "Expected some fights with 2+ deaths"

    def test_xp_delta_non_negative(self, match):
        for tf in match.teamfights:
            for p in tf.players:
                assert p.xp_delta >= 0
