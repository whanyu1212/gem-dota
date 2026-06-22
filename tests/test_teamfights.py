"""Tests for teamfight detection.

Unit tests use synthetic combat log entries.
Integration tests parse a real .dem fixture and verify plausible output.
"""

from __future__ import annotations

import pytest

from gem.combat.log import CombatLogEntry
from gem.extractors.teamfights import (
    Teamfight,
    _near_fight,
    _nearest_pos,
    _nearest_xp,
    _update_centroid,
    detect_opendota_teamfights,
    detect_teamfights,
)

_COOLDOWN = 15 * 30  # 450 ticks


def _death(
    tick: int,
    target: str = "npc_dota_hero_axe",
    illusion: bool = False,
    will_reincarnate: bool = False,
    game_time_s: int | None = None,
) -> CombatLogEntry:
    return CombatLogEntry(
        tick=tick,
        game_time_s=game_time_s,
        log_type="DEATH",
        target_name=target,
        target_is_hero=True,
        target_is_illusion=illusion,
        will_reincarnate=will_reincarnate,
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

    def test_reincarnation_trigger_not_counted_as_death(self):
        # A reincarnation/aegis trigger (will_reincarnate=True) must not count
        # toward Teamfight.deaths or attribute a per-player death — the hero
        # returns. Only the subsequent true death counts. Regression for Codex P2:
        # keeps teamfight/Roshan summaries consistent with the death curve.
        h2s = {"npc_dota_hero_axe": 0}
        entries = [
            _death(1000, "npc_dota_hero_axe", will_reincarnate=True),  # trigger
            _death(1060, "npc_dota_hero_axe"),  # true death
        ]
        fights = detect_teamfights(entries, hero_to_slot=h2s)
        assert len(fights) == 1
        assert fights[0].deaths == 1
        assert fights[0].players[0].deaths == 1

    def test_lone_reincarnation_trigger_opens_no_fight(self):
        # A solitary trigger death with no real death must not open a fight at all.
        fights = detect_teamfights([_death(1000, will_reincarnate=True)])
        assert fights == []

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

    def test_gold_delta_attributed_to_recipient(self):
        # GOLD is credited to the recipient, stored in target_name (not the
        # attacker / killed unit). Matches OpenDota and combat/aggregator.py.
        h2s = {"npc_dota_hero_axe": 0}
        gold_entry = CombatLogEntry(
            tick=1050,
            log_type="GOLD",
            target_name="npc_dota_hero_axe",
            value=200,
            gold_reason=1,
        )
        entries = [_death(1000), gold_entry]
        fights = detect_teamfights(entries, hero_to_slot=h2s)
        assert fights[0].players[0].gold_delta == 200

    def test_gold_not_attributed_to_attacker(self):
        # The killed unit (attacker_name) must NOT receive the bounty.
        h2s = {"npc_dota_hero_axe": 0, "npc_dota_hero_lina": 1}
        gold_entry = CombatLogEntry(
            tick=1050,
            log_type="GOLD",
            attacker_name="npc_dota_hero_lina",  # killed unit
            target_name="npc_dota_hero_axe",  # bounty recipient
            value=200,
            gold_reason=1,
        )
        entries = [_death(1000), gold_entry]
        fights = detect_teamfights(entries, hero_to_slot=h2s)
        assert fights[0].players[0].gold_delta == 200  # axe (recipient)
        assert fights[0].players[1].gold_delta == 0  # lina (killed unit)

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


class TestDetectOpenDotaTeamfights:
    def test_uses_combat_log_game_time_and_filters_short_windows(self):
        fights = detect_opendota_teamfights(
            [
                _death(10_000, game_time_s=1033),
                _death(10_030, target="npc_dota_hero_pudge", game_time_s=1038),
                _death(10_060, target="npc_dota_hero_lina", game_time_s=1040),
                _death(20_000, target="npc_dota_hero_crystal_maiden", game_time_s=1200),
            ]
        )

        assert [(f.start, f.end, f.last_death, f.deaths) for f in fights] == [(1018, 1055, 1040, 3)]

    def test_filters_illusions_and_reincarnation_triggers(self):
        fights = detect_opendota_teamfights(
            [
                _death(100, game_time_s=100),
                _death(110, target="npc_dota_hero_pudge", illusion=True, game_time_s=105),
                _death(
                    120,
                    target="npc_dota_hero_lina",
                    will_reincarnate=True,
                    game_time_s=106,
                ),
                _death(200, target="npc_dota_hero_drow_ranger", game_time_s=200),
                _death(210, target="npc_dota_hero_juggernaut", game_time_s=204),
                _death(220, target="npc_dota_hero_sven", game_time_s=208),
            ]
        )

        assert [(f.start, f.end, f.last_death, f.deaths) for f in fights] == [(185, 223, 208, 3)]

    def test_temporal_output_does_not_spatially_split(self):
        h2s = {"npc_dota_hero_axe": 0, "npc_dota_hero_pudge": 1, "npc_dota_hero_lina": 2}
        snaps = {
            **_make_snaps("npc_dota_hero_axe", 0, 3000, 0.0, 0.0),
            **_make_snaps("npc_dota_hero_pudge", 1, 3030, 10_000.0, 10_000.0),
            **_make_snaps("npc_dota_hero_lina", 2, 3060, -10_000.0, -10_000.0),
        }

        fights = detect_opendota_teamfights(
            [
                _death(3000, "npc_dota_hero_axe", game_time_s=100),
                _death(3030, "npc_dota_hero_pudge", game_time_s=101),
                _death(3060, "npc_dota_hero_lina", game_time_s=102),
            ],
            hero_to_slot=h2s,
            player_snapshots=snaps,
        )

        assert len(fights) == 1
        assert fights[0].deaths == 3

    def test_populates_opendota_player_fields(self):
        h2s = {"npc_dota_hero_axe": 0, "npc_dota_hero_pudge": 1}
        snaps = _make_snaps("npc_dota_hero_pudge", 1, 3000, 123.4, 567.6)
        entries = [
            CombatLogEntry(
                tick=3000,
                game_time_s=100,
                log_type="DEATH",
                attacker_name="npc_dota_hero_axe",
                target_name="npc_dota_hero_pudge",
                target_is_hero=True,
            ),
            _death(3030, "npc_dota_hero_axe", game_time_s=101),
            _death(3060, "npc_dota_hero_axe", game_time_s=102),
            CombatLogEntry(
                tick=3010,
                game_time_s=101,
                log_type="DAMAGE",
                attacker_name="npc_dota_hero_axe",
                target_name="npc_dota_hero_pudge",
                attacker_is_hero=True,
                target_is_hero=True,
                value=250,
            ),
            CombatLogEntry(
                tick=3011,
                game_time_s=101,
                log_type="HEAL",
                attacker_name="npc_dota_hero_axe",
                target_name="npc_dota_hero_pudge",
                attacker_is_hero=True,
                target_is_hero=True,
                value=75,
            ),
            CombatLogEntry(
                tick=3012,
                game_time_s=101,
                log_type="GOLD",
                target_name="npc_dota_hero_axe",
                value=200,
            ),
            CombatLogEntry(
                tick=3013,
                game_time_s=101,
                log_type="XP",
                target_name="npc_dota_hero_axe",
                value=300,
            ),
            CombatLogEntry(
                tick=3014,
                game_time_s=101,
                log_type="ABILITY",
                attacker_name="npc_dota_hero_axe",
                attacker_is_hero=True,
                inflictor_name="axe_berserkers_call",
            ),
            CombatLogEntry(
                tick=3015,
                game_time_s=101,
                log_type="ITEM",
                attacker_name="npc_dota_hero_axe",
                attacker_is_hero=True,
                inflictor_name="item_blink",
            ),
            CombatLogEntry(tick=3016, game_time_s=101, log_type="BUYBACK", value=1),
        ]

        fight = detect_opendota_teamfights(entries, hero_to_slot=h2s, player_snapshots=snaps)[0]

        assert fight.players[0].killed == {"npc_dota_hero_pudge": 1}
        assert fight.players[0].damage == 250
        assert fight.players[0].healing == 75
        assert fight.players[0].gold_delta == 200
        assert fight.players[0].xp_delta == 300
        assert fight.players[0].ability_uses == {"axe_berserkers_call": 1}
        assert fight.players[0].item_uses == {"blink": 1}
        assert fight.players[1].deaths == 1
        assert fight.players[1].deaths_pos == {"123": {"568": 1}}
        assert fight.players[1].buybacks == 1


# ---------------------------------------------------------------------------
# XP delta unit tests
# ---------------------------------------------------------------------------


class TestXpDelta:
    @staticmethod
    def _snap(tick, *, current_xp=0, total_earned_xp=0):
        # xp = m_iCurrentXP (resets on level-up); total_earned_xp =
        # m_iTotalEarnedXP (monotonic). xp_delta is diffed from the latter.
        from gem.extractors._snapshots import PlayerStateSnapshot

        return PlayerStateSnapshot(
            tick=tick,
            player_id=0,
            npc_name="npc_dota_hero_axe",
            team=2,
            level=1,
            xp=current_xp,
            gold=0,
            net_worth=0,
            total_earned_gold=0,
            total_earned_xp=total_earned_xp,
            lh=0,
            dn=0,
            hp=500,
            max_hp=500,
            mana=0.0,
            max_mana=0.0,
            x=None,
            y=None,
        )

    def test_xp_delta_computed_from_total_earned_xp(self):
        h2s = {"npc_dota_hero_axe": 0}
        # Fight: start_tick = 1000-450=550, end_tick = 1000+450=1450
        snaps = {
            0: [
                self._snap(tick=500, total_earned_xp=1000),
                self._snap(tick=1500, total_earned_xp=1500),
            ]
        }
        entries = [_death(1000, "npc_dota_hero_axe")]
        fights = detect_teamfights(entries, hero_to_slot=h2s, player_snapshots=snaps)
        assert fights[0].players[0].xp_delta == 500

    def test_xp_delta_survives_levelup(self):
        # Regression for the m_iCurrentXP bug: a hero who levels up mid-fight has
        # m_iCurrentXP go *backwards* (400 -> 100), which the old max(0, ...)
        # clamp erased to 0. m_iTotalEarnedXP keeps rising, so the real gain shows.
        h2s = {"npc_dota_hero_axe": 0}
        snaps = {
            0: [
                self._snap(tick=500, current_xp=400, total_earned_xp=1000),
                self._snap(tick=1500, current_xp=100, total_earned_xp=1700),
            ]
        }
        entries = [_death(1000, "npc_dota_hero_axe")]
        fights = detect_teamfights(entries, hero_to_slot=h2s, player_snapshots=snaps)
        assert fights[0].players[0].xp_delta == 700  # not 0


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


class TestCentroidPositionedDivisor:
    """A position-less death must not bias the centroid (uses centroid_n)."""

    @staticmethod
    def _snap(pid, tick, x, y):
        from gem.extractors._snapshots import PlayerStateSnapshot

        return PlayerStateSnapshot(
            tick=tick,
            player_id=pid,
            npc_name=f"npc_dota_hero_h{pid}",
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
            mana=0.0,
            max_mana=0.0,
            x=x,
            y=y,
        )

    def test_positionless_death_excluded_from_centroid(self):
        # Three deaths in one fight: two positioned at (0,0) and (100,100), one
        # with no position. Centroid must be the mean of the two positioned
        # deaths = (50, 50), not biased toward (0,0) by counting the third in
        # the divisor.
        h2s = {"npc_dota_hero_h0": 0, "npc_dota_hero_h1": 1, "npc_dota_hero_h2": 2}
        snaps = {
            0: [self._snap(0, 1000, 0.0, 0.0)],
            1: [self._snap(1, 1010, None, None)],  # position-less
            2: [self._snap(2, 1020, 100.0, 100.0)],
        }
        entries = [
            _death(1000, "npc_dota_hero_h0"),
            _death(1010, "npc_dota_hero_h1"),
            _death(1020, "npc_dota_hero_h2"),
        ]
        fights = detect_teamfights(entries, hero_to_slot=h2s, player_snapshots=snaps)
        assert len(fights) == 1
        assert fights[0].deaths == 3
        assert fights[0].centroid_n == 2  # only the two positioned deaths
        assert abs(fights[0].centroid_x - 50.0) < 1e-6
        assert abs(fights[0].centroid_y - 50.0) < 1e-6


class TestRoamingFightAttribution:
    """Deaths/buybacks must be attributed by fight membership, not by re-checking
    the player's position against the fight's (later-drifted) final centroid."""

    @staticmethod
    def _snap(pid, tick, x, y, team=2):
        from gem.extractors._snapshots import PlayerStateSnapshot

        return PlayerStateSnapshot(
            tick=tick,
            player_id=pid,
            npc_name=f"npc_dota_hero_h{pid}",
            team=team,
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
            mana=0.0,
            max_mana=0.0,
            x=x,
            y=y,
        )

    def test_drifting_centroid_does_not_drop_deaths(self):
        # Deaths march across the map. Whether they land in one fight or split
        # into several (the centroid can drift past _FIGHT_RADIUS from earlier
        # deaths), the invariant must hold across ALL fights: every death is
        # attributed to exactly one fight, so per-player deaths sum to the total
        # death count and kills account for every death. The old pass-2 re-filter
        # against the final centroid violated this by silently dropping deaths.
        n = 8
        step = 1200.0  # < _FIGHT_RADIUS so consecutive deaths chain
        h2s = {f"npc_dota_hero_h{i}": i for i in range(n)}
        slot_to_team = {i: (2 if i % 2 == 0 else 3) for i in range(n)}
        snaps = {
            i: [self._snap(i, 1000 + i * 30, i * step, 0.0, team=slot_to_team[i])] for i in range(n)
        }
        entries = [_death(1000 + i * 30, f"npc_dota_hero_h{i}") for i in range(n)]
        fights = detect_teamfights(
            entries, hero_to_slot=h2s, slot_to_team=slot_to_team, player_snapshots=snaps
        )
        # The fight may or may not split; the invariant holds regardless.
        total_player_deaths = sum(p.deaths for f in fights for p in f.players)
        total_headline_deaths = sum(f.deaths for f in fights)
        total_kills = sum(f.radiant_kills + f.dire_kills for f in fights)
        assert total_player_deaths == n  # no death dropped
        assert total_headline_deaths == n
        assert total_kills == n

    def test_buyback_far_from_centroid_still_counted(self):
        # A hero dies in a fight located away from base, then buys back — at the
        # fountain, far from the fight centroid. The buyback must still be
        # credited to the fight (its window contains the buyback tick).
        from gem.combat.log import CombatLogEntry

        h2s = {"npc_dota_hero_h0": 0, "npc_dota_hero_h1": 1}
        snaps = {
            0: [self._snap(0, 1000, 20000.0, 20000.0)],  # fight far from base
            1: [self._snap(1, 1000, 20100.0, 20000.0)],
        }
        entries = [
            _death(1000, "npc_dota_hero_h0"),
            _death(1000, "npc_dota_hero_h1"),
            CombatLogEntry(tick=1100, log_type="BUYBACK", value=0),  # slot 0 buys back
        ]
        fights = detect_teamfights(entries, hero_to_slot=h2s, player_snapshots=snaps)
        assert len(fights) == 1
        assert fights[0].players[0].buybacks == 1


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

        def _snap(tick, total_earned_xp):
            # _nearest_xp returns total_earned_xp (monotonic), not xp.
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
                total_earned_xp=total_earned_xp,
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
    def match(self, full_replay_path):
        import gem

        return gem.parse(str(full_replay_path))

    def test_teamfights_detected(self, match):
        assert len(match.teamfights) > 0, "Expected at least one teamfight in replay fixture"

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
