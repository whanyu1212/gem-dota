"""Tests for teamfight detection.

Unit tests use synthetic combat log entries.
Integration tests parse a real .dem fixture and verify plausible output.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from gem.combatlog import CombatLogEntry
from gem.extractors.teamfights import (
    Teamfight,
    _near_fight,
    _nearest_pos,
    _nearest_xp,
    _update_centroid,
    detect_teamfights,
)

FIXTURE = Path(__file__).parent / "fixtures" / "ti14_finals_g3_xg_vs_falcons.dem"

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

    def test_heal_attributed_to_attacker(self):
        h2s = {"npc_dota_hero_dazzle": 0, "npc_dota_hero_axe": 1}
        heal_entry = CombatLogEntry(
            tick=1050,
            log_type="HEAL",
            attacker_name="npc_dota_hero_dazzle",
            target_name="npc_dota_hero_axe",
            attacker_is_hero=True,
            target_is_hero=True,
            target_is_illusion=False,
            value=250,
        )
        entries = [_death(1000, "npc_dota_hero_axe"), heal_entry]
        fights = detect_teamfights(entries, hero_to_slot=h2s)
        assert fights[0].players[0].healing == 250

    def test_self_heal_not_counted(self):
        h2s = {"npc_dota_hero_axe": 0}
        self_heal = CombatLogEntry(
            tick=1050,
            log_type="HEAL",
            attacker_name="npc_dota_hero_axe",
            target_name="npc_dota_hero_axe",
            attacker_is_hero=True,
            target_is_hero=True,
            target_is_illusion=False,
            value=200,
        )
        entries = [_death(1000, "npc_dota_hero_axe"), self_heal]
        fights = detect_teamfights(entries, hero_to_slot=h2s)
        assert fights[0].players[0].healing == 0

    def test_gold_delta_attributed_to_attacker(self):
        h2s = {"npc_dota_hero_axe": 0}
        gold_entry = CombatLogEntry(
            tick=1050,
            log_type="GOLD",
            attacker_name="npc_dota_hero_axe",
            attacker_is_hero=True,
            value=200,
            gold_reason=1,
        )
        entries = [_death(1000), gold_entry]
        fights = detect_teamfights(entries, hero_to_slot=h2s)
        assert fights[0].players[0].gold_delta == 200

    def test_item_use_recorded(self):
        h2s = {"npc_dota_hero_axe": 0}
        item_entry = CombatLogEntry(
            tick=1050,
            log_type="ITEM",
            attacker_name="npc_dota_hero_axe",
            inflictor_name="item_blink",
            attacker_is_hero=True,
            attacker_is_illusion=False,
        )
        entries = [_death(1000), item_entry]
        fights = detect_teamfights(entries, hero_to_slot=h2s)
        assert fights[0].players[0].item_uses.get("item_blink") == 1


# ---------------------------------------------------------------------------
# XP delta unit tests
# ---------------------------------------------------------------------------


class TestXpDelta:
    def test_xp_delta_computed_from_snapshots(self):
        from gem.extractors._snapshots import PlayerStateSnapshot

        def _snap(tick, xp):
            return PlayerStateSnapshot(
                tick=tick,
                player_id=0,
                npc_name="npc_dota_hero_axe",
                team=2,
                level=1,
                xp=xp,
                gold=0,
                net_worth=0,
                total_earned_gold=0,
                total_earned_xp=0,
                lh=0,
                dn=0,
                hp=500,
                max_hp=500,
                mana=0.0,
                max_mana=0.0,
                x=None,
                y=None,
            )

        h2s = {"npc_dota_hero_axe": 0}
        # Fight: start_tick = 1000-450=550, end_tick = 1000+450=1450
        snaps = {0: [_snap(tick=500, xp=1000), _snap(tick=1500, xp=1500)]}
        entries = [_death(1000, "npc_dota_hero_axe")]
        fights = detect_teamfights(entries, hero_to_slot=h2s, player_snapshots=snaps)
        assert fights[0].players[0].xp_delta == 500

    def test_xp_delta_clamped_to_zero(self):
        from gem.extractors._snapshots import PlayerStateSnapshot

        def _snap(tick, xp):
            return PlayerStateSnapshot(
                tick=tick,
                player_id=0,
                npc_name="npc_dota_hero_axe",
                team=2,
                level=1,
                xp=xp,
                gold=0,
                net_worth=0,
                total_earned_gold=0,
                total_earned_xp=0,
                lh=0,
                dn=0,
                hp=500,
                max_hp=500,
                mana=0.0,
                max_mana=0.0,
                x=None,
                y=None,
            )

        h2s = {"npc_dota_hero_axe": 0}
        snaps = {0: [_snap(500, xp=2000), _snap(1500, xp=1800)]}
        entries = [_death(1000, "npc_dota_hero_axe")]
        fights = detect_teamfights(entries, hero_to_slot=h2s, player_snapshots=snaps)
        assert fights[0].players[0].xp_delta == 0


# ---------------------------------------------------------------------------
# Helper function unit tests
# ---------------------------------------------------------------------------


class TestUpdateCentroid:
    def test_first_death_returns_pos(self):
        result = _update_centroid(None, None, 1, (100.0, 200.0))
        assert result == (100.0, 200.0)

    def test_two_deaths_averages(self):
        cx, cy = _update_centroid(None, None, 1, (0.0, 0.0))
        cx, cy = _update_centroid(cx, cy, 2, (100.0, 200.0))
        assert cx == 50.0
        assert cy == 100.0

    def test_three_deaths_incremental_mean(self):
        cx, cy = _update_centroid(None, None, 1, (0.0, 0.0))
        cx, cy = _update_centroid(cx, cy, 2, (300.0, 300.0))
        cx, cy = _update_centroid(cx, cy, 3, (600.0, 600.0))
        assert abs(cx - 300.0) < 1e-6
        assert abs(cy - 300.0) < 1e-6


class TestNearestPos:
    def test_empty_returns_none(self):
        assert _nearest_pos([], tick=100) is None

    def test_picks_nearest_tick(self):
        from gem.extractors._snapshots import PlayerStateSnapshot

        def _snap(tick, x, y):
            return PlayerStateSnapshot(
                tick=tick,
                player_id=0,
                npc_name="",
                team=2,
                level=1,
                xp=0,
                gold=0,
                net_worth=0,
                total_earned_gold=0,
                total_earned_xp=0,
                lh=0,
                dn=0,
                hp=100,
                max_hp=100,
                mana=0.0,
                max_mana=0.0,
                x=x,
                y=y,
            )

        snaps = [_snap(100, 1.0, 2.0), _snap(300, 5.0, 6.0)]
        pos = _nearest_pos(snaps, tick=110)
        assert pos == (1.0, 2.0)

    def test_returns_none_when_x_y_are_none(self):
        from gem.extractors._snapshots import PlayerStateSnapshot

        snap = PlayerStateSnapshot(
            tick=100,
            player_id=0,
            npc_name="",
            team=2,
            level=1,
            xp=0,
            gold=0,
            net_worth=0,
            total_earned_gold=0,
            total_earned_xp=0,
            lh=0,
            dn=0,
            hp=100,
            max_hp=100,
            mana=0.0,
            max_mana=0.0,
            x=None,
            y=None,
        )
        assert _nearest_pos([snap], tick=100) is None


class TestNearestXp:
    def test_empty_returns_none(self):
        assert _nearest_xp([], tick=100) is None

    def test_picks_nearest_tick(self):
        from gem.extractors._snapshots import PlayerStateSnapshot

        def _snap(tick, xp):
            return PlayerStateSnapshot(
                tick=tick,
                player_id=0,
                npc_name="",
                team=2,
                level=1,
                xp=xp,
                gold=0,
                net_worth=0,
                total_earned_gold=0,
                total_earned_xp=0,
                lh=0,
                dn=0,
                hp=100,
                max_hp=100,
                mana=0.0,
                max_mana=0.0,
                x=None,
                y=None,
            )

        snaps = [_snap(100, 1000), _snap(500, 2000)]
        assert _nearest_xp(snaps, tick=120) == 1000
        assert _nearest_xp(snaps, tick=400) == 2000


class TestNearFight:
    def test_no_snapshots_returns_true(self):
        fight = Teamfight(
            start_tick=0,
            end_tick=1000,
            last_death_tick=500,
            deaths=1,
            centroid_x=0.0,
            centroid_y=0.0,
        )
        assert _near_fight(0, 500, fight, player_snapshots=None) is True

    def test_no_centroid_returns_true(self):
        fight = Teamfight(
            start_tick=0,
            end_tick=1000,
            last_death_tick=500,
            deaths=1,
            centroid_x=None,
            centroid_y=None,
        )
        assert _near_fight(0, 500, fight, player_snapshots={}) is True

    def test_player_within_radius_returns_true(self):
        from gem.extractors._snapshots import PlayerStateSnapshot

        snap = PlayerStateSnapshot(
            tick=500,
            player_id=0,
            npc_name="",
            team=2,
            level=1,
            xp=0,
            gold=0,
            net_worth=0,
            total_earned_gold=0,
            total_earned_xp=0,
            lh=0,
            dn=0,
            hp=100,
            max_hp=100,
            mana=0.0,
            max_mana=0.0,
            x=100.0,
            y=100.0,
        )
        fight = Teamfight(
            start_tick=0,
            end_tick=1000,
            last_death_tick=500,
            deaths=1,
            centroid_x=200.0,
            centroid_y=200.0,
        )
        assert _near_fight(0, 500, fight, player_snapshots={0: [snap]}) is True

    def test_player_beyond_radius_returns_false(self):
        from gem.extractors._snapshots import PlayerStateSnapshot

        snap = PlayerStateSnapshot(
            tick=500,
            player_id=0,
            npc_name="",
            team=2,
            level=1,
            xp=0,
            gold=0,
            net_worth=0,
            total_earned_gold=0,
            total_earned_xp=0,
            lh=0,
            dn=0,
            hp=100,
            max_hp=100,
            mana=0.0,
            max_mana=0.0,
            x=0.0,
            y=0.0,
        )
        fight = Teamfight(
            start_tick=0,
            end_tick=1000,
            last_death_tick=500,
            deaths=1,
            centroid_x=5000.0,
            centroid_y=5000.0,
        )  # ~7071 units away
        assert _near_fight(0, 500, fight, player_snapshots={0: [snap]}) is False


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

    def test_far_deaths_split_into_separate_fights(self):
        """Two deaths within cooldown but >3000 units apart are split into separate fights."""
        h2s = {"npc_dota_hero_axe": 0, "npc_dota_hero_pudge": 1}
        snaps = {
            **_make_snaps("npc_dota_hero_axe", 0, 1000, 0.0, 0.0),
            **_make_snaps("npc_dota_hero_pudge", 1, 1200, 5000.0, 5000.0),  # ~7071 units away
        }
        entries = [
            _death(1000, "npc_dota_hero_axe"),
            _death(1200, "npc_dota_hero_pudge"),
        ]
        fights = detect_teamfights(entries, hero_to_slot=h2s, player_snapshots=snaps)
        assert len(fights) == 2
        assert fights[0].deaths == 1
        assert fights[1].deaths == 1

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
