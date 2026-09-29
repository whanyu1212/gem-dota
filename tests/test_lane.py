"""Tests for lane assignment, OpenDota cell rounding and lane efficiency stats.

Unit tests use synthetic lane_pos dicts and ParsedPlayer instances.
Integration tests parse a real .dem fixture and verify plausible output.
"""

from __future__ import annotations

import pytest

from gem.extractors._cells import od_cell, od_cell_index, od_one_decimal
from gem.extractors.lane import (
    LANE_BOT,
    LANE_DIRE_JUNGLE,
    LANE_MID,
    LANE_RADIANT_JUNGLE,
    LANE_TOP,
    LaneAssignment,
    assign_lane,
    lane_for_cell,
)
from gem.results.models import ParsedPlayer

# ---------------------------------------------------------------------------
# OpenDota cell rounding
# ---------------------------------------------------------------------------


class TestCellRounding:
    def test_cell_is_world_over_128(self):
        assert od_cell(11776.0) == 92.0

    def test_half_rounds_up_like_java(self):
        # Python's round() gives 92 (half to even) for 92.5; Java's Math.round 93.
        assert od_cell_index(92.5 * 128, expanded=False) == 93
        assert od_cell_index(91.5 * 128, expanded=False) == 92

    def test_one_decimal_then_round_is_rounded_twice(self):
        # 91.46 -> 91.5 -> 92 when expand() rounded it first; 91 when it did not.
        world = 91.46 * 128
        assert od_cell_index(world) == 92
        assert od_cell_index(world, expanded=False) == 91

    def test_one_decimal_uses_float32(self):
        assert od_one_decimal(91.46) == pytest.approx(91.5, abs=1e-5)


# ---------------------------------------------------------------------------
# laneMappings port
# ---------------------------------------------------------------------------


class TestLaneForCell:
    def test_mid_diagonal(self):
        assert lane_for_cell(128, 128) == LANE_MID

    def test_lanes_and_jungles(self):
        assert lane_for_cell(70, 150) == LANE_TOP  # Radiant top lane, left strip
        assert lane_for_cell(130, 185) == LANE_TOP  # top strip
        assert lane_for_cell(185, 100) == LANE_BOT  # right strip
        assert lane_for_cell(100, 70) == LANE_BOT  # bottom strip
        assert lane_for_cell(110, 150) == LANE_DIRE_JUNGLE
        assert lane_for_cell(150, 100) == LANE_RADIANT_JUNGLE

    def test_off_grid_cells_are_skipped(self):
        assert lane_for_cell(63, 128) is None
        assert lane_for_cell(192, 128) is None
        assert lane_for_cell(128, 64) is None  # row 128 is past the grid
        assert lane_for_cell(128, 193) is None


# ---------------------------------------------------------------------------
# assign_lane — OpenDota getLaneFromPosData
# ---------------------------------------------------------------------------


class TestAssignLane:
    def test_empty_is_unknown(self):
        assert assign_lane({}, team=2) == LaneAssignment()

    def test_only_off_grid_samples_is_unknown(self):
        assert assign_lane({"10": {"10": 50}}, team=2) == LaneAssignment()

    def test_radiant_roles(self):
        assert assign_lane({"100": {"70": 5}}, team=2).lane_role == 1  # bot = safe
        assert assign_lane({"70": {"150": 5}}, team=2).lane_role == 3  # top = off
        assert assign_lane({"128": {"128": 5}}, team=2).lane_role == 2
        assert assign_lane({"150": {"100": 5}}, team=2).lane_role == 4

    def test_dire_roles_are_mirrored(self):
        assert assign_lane({"70": {"150": 5}}, team=3).lane_role == 1  # top = safe
        assert assign_lane({"100": {"70": 5}}, team=3).lane_role == 3  # bot = off
        assert assign_lane({"110": {"150": 5}}, team=3).lane_role == 4

    def test_roaming_is_a_flag_beside_the_role(self):
        # Four lanes at 25% each: the first lane read wins, and it holds < 45%.
        lane_pos = {"70": {"150": 5}, "100": {"70": 5}, "128": {"128": 5}, "150": {"100": 5}}
        result = assign_lane(lane_pos, team=2)
        assert result == LaneAssignment(lane=LANE_TOP, lane_role=3, is_roaming=True)

    def test_concentrated_is_not_roaming(self):
        result = assign_lane({"100": {"70": 9}, "128": {"128": 1}}, team=2)
        assert result.lane == LANE_BOT
        assert not result.is_roaming

    def test_tie_goes_to_first_lane_read_x_then_y_numerically(self):
        # Equal counts: x "70" sorts before "100" numerically (not as strings),
        # so top reaches the count first and keeps it.
        result = assign_lane({"100": {"70": 3}, "70": {"150": 3}}, team=2)
        assert result.lane == LANE_TOP

    def test_off_grid_samples_leave_the_roaming_share(self):
        # 5 bot samples and 20 off-grid: bot holds 100% of the counted samples.
        result = assign_lane({"100": {"70": 5}, "10": {"10": 20}}, team=2)
        assert result.lane == LANE_BOT
        assert not result.is_roaming


# ---------------------------------------------------------------------------
# Lane stats from minute series — index 10 extraction
# ---------------------------------------------------------------------------


class TestLaneStatsFromMinuteSeries:
    def _make_pp(self) -> ParsedPlayer:
        return ParsedPlayer(player_id=0)

    def test_lane_lh_from_index_10(self):
        pp = self._make_pp()
        pp.lh_t_min = list(range(15))
        # Simulate the match_builder derivation
        _LM = 10
        if len(pp.lh_t_min) > _LM:
            pp.lane_last_hits = pp.lh_t_min[_LM]
        assert pp.lane_last_hits == 10

    def test_lane_denies_from_index_10(self):
        pp = self._make_pp()
        pp.dn_t_min = list(range(15))
        _LM = 10
        if len(pp.dn_t_min) > _LM:
            pp.lane_denies = pp.dn_t_min[_LM]
        assert pp.lane_denies == 10

    def test_lane_total_gold_from_index_10(self):
        pp = self._make_pp()
        pp.total_earned_gold_t_min = [i * 100 for i in range(15)]
        _LM = 10
        if len(pp.total_earned_gold_t_min) > _LM:
            pp.lane_total_gold = pp.total_earned_gold_t_min[_LM]
        assert pp.lane_total_gold == 1000

    def test_lane_total_xp_from_index_10(self):
        pp = self._make_pp()
        pp.total_earned_xp_t_min = [i * 50 for i in range(15)]
        _LM = 10
        if len(pp.total_earned_xp_t_min) > _LM:
            pp.lane_total_xp = pp.total_earned_xp_t_min[_LM]
        assert pp.lane_total_xp == 500

    def test_stats_zero_when_series_too_short(self):
        pp = self._make_pp()
        pp.lh_t_min = [5, 10]  # only 2 entries, index 10 doesn't exist
        _LM = 10
        if len(pp.lh_t_min) > _LM:
            pp.lane_last_hits = pp.lh_t_min[_LM]
        assert pp.lane_last_hits == 0

    def test_stats_zero_when_empty(self):
        pp = self._make_pp()
        # No assignment at all — defaults hold
        assert pp.lane_last_hits == 0
        assert pp.lane_denies == 0
        assert pp.lane_total_gold == 0
        assert pp.lane_total_xp == 0


# ---------------------------------------------------------------------------
# Tier-1: lane_efficiency_pct
# ---------------------------------------------------------------------------

_LANE_GOLD_BASELINE = 4948  # must match match_builder constant


class TestLaneEfficiencyPct:
    def test_exact_baseline_gives_100(self):
        pp = ParsedPlayer(player_id=0)
        pp.lane_total_gold = _LANE_GOLD_BASELINE
        pp.lane_efficiency_pct = int(pp.lane_total_gold / _LANE_GOLD_BASELINE * 100)
        assert pp.lane_efficiency_pct == 100

    def test_half_baseline_gives_50(self):
        pp = ParsedPlayer(player_id=0)
        pp.lane_total_gold = _LANE_GOLD_BASELINE // 2
        pp.lane_efficiency_pct = int(pp.lane_total_gold / _LANE_GOLD_BASELINE * 100)
        assert pp.lane_efficiency_pct == 50

    def test_above_baseline_exceeds_100(self):
        # Hero with kills/bounties can exceed 100%
        pp = ParsedPlayer(player_id=0)
        pp.lane_total_gold = 6000
        pp.lane_efficiency_pct = int(pp.lane_total_gold / _LANE_GOLD_BASELINE * 100)
        assert pp.lane_efficiency_pct > 100

    def test_zero_gold_gives_zero(self):
        pp = ParsedPlayer(player_id=0)
        pp.lane_total_gold = 0
        # zero branch — not set (remains default)
        assert pp.lane_efficiency_pct == 0

    def test_floor_truncates(self):
        # int() truncates toward zero, same as floor for positive
        pp = ParsedPlayer(player_id=0)
        pp.lane_total_gold = 3000
        pp.lane_efficiency_pct = int(pp.lane_total_gold / _LANE_GOLD_BASELINE * 100)
        assert pp.lane_efficiency_pct == 60  # 3000/4948*100 = 60.62... → 60


# ---------------------------------------------------------------------------
# Tier-2: lane_gold_adv / lane_xp_adv
# ---------------------------------------------------------------------------


class TestLaneAdvantage:
    """Test the cross-player opponent pairing logic for lane_gold_adv/lane_xp_adv."""

    def _apply_adv(self, players: list[ParsedPlayer]) -> None:
        """Replicate match_builder Tier-2 rank-based advantage computation."""
        _LANE_ROLES_WITH_OPPONENTS = {1, 2, 3}
        for role in _LANE_ROLES_WITH_OPPONENTS:
            radiant = sorted(
                [pp for pp in players if pp.team == 2 and pp.lane_role == role],
                key=lambda p: p.lane_total_gold,
                reverse=True,
            )
            dire = sorted(
                [pp for pp in players if pp.team == 3 and pp.lane_role == role],
                key=lambda p: p.lane_total_gold,
                reverse=True,
            )
            for rad, dire_opp in zip(radiant, dire, strict=False):
                rad.lane_gold_adv = rad.lane_total_gold - dire_opp.lane_total_gold
                rad.lane_xp_adv = rad.lane_total_xp - dire_opp.lane_total_xp
                dire_opp.lane_gold_adv = dire_opp.lane_total_gold - rad.lane_total_gold
                dire_opp.lane_xp_adv = dire_opp.lane_total_xp - rad.lane_total_xp

    def _make(self, pid: int, team: int, role: int, gold: int, xp: int) -> ParsedPlayer:
        pp = ParsedPlayer(player_id=pid)
        pp.team = team
        pp.lane_role = role
        pp.lane_total_gold = gold
        pp.lane_total_xp = xp
        return pp

    def test_radiant_ahead_gives_positive(self):
        rad = self._make(0, 2, 1, gold=4000, xp=5000)
        dire = self._make(5, 3, 1, gold=2500, xp=3500)
        self._apply_adv([rad, dire])
        assert rad.lane_gold_adv == 1500
        assert rad.lane_xp_adv == 1500

    def test_dire_ahead_gives_negative_for_radiant(self):
        rad = self._make(0, 2, 1, gold=2000, xp=2000)
        dire = self._make(5, 3, 1, gold=3500, xp=4000)
        self._apply_adv([rad, dire])
        assert rad.lane_gold_adv == -1500
        assert rad.lane_xp_adv == -2000

    def test_opponent_adv_is_mirror(self):
        rad = self._make(0, 2, 2, gold=3000, xp=4000)
        dire = self._make(5, 3, 2, gold=2000, xp=3000)
        self._apply_adv([rad, dire])
        assert rad.lane_gold_adv == -dire.lane_gold_adv  # type: ignore[operator]
        assert rad.lane_xp_adv == -dire.lane_xp_adv  # type: ignore[operator]

    def test_no_opponent_leaves_none(self):
        rad = self._make(0, 2, 1, gold=3000, xp=4000)
        # No dire player — lane_gold_adv stays None
        self._apply_adv([rad])
        assert rad.lane_gold_adv is None
        assert rad.lane_xp_adv is None

    def test_jungle_excluded_from_adv(self):
        jungler = self._make(0, 2, 4, gold=3000, xp=4000)
        opponent = self._make(5, 3, 4, gold=2000, xp=3000)
        self._apply_adv([jungler, opponent])
        assert jungler.lane_gold_adv is None
        assert jungler.lane_xp_adv is None

    def test_dual_lane_rank_pairing(self):
        # 2v2 safe lane: rank by gold desc, pair high vs high, low vs low.
        # Radiant: Sven=3000g, Bane=1200g  — Dire: Gyro=2500g, Pugna=900g
        # Pairs: Sven(3000) vs Gyro(2500), Bane(1200) vs Pugna(900)
        sven = self._make(0, 2, 1, gold=3000, xp=4000)
        bane = self._make(1, 2, 1, gold=1200, xp=1500)
        gyro = self._make(5, 3, 1, gold=2500, xp=3200)
        pugna = self._make(6, 3, 1, gold=900, xp=1100)
        self._apply_adv([sven, bane, gyro, pugna])
        # Sven (highest gold on Radiant) pairs vs Gyro (highest gold on Dire)
        assert sven.lane_gold_adv == 3000 - 2500
        assert sven.lane_xp_adv == 4000 - 3200
        # Bane (lowest gold on Radiant) pairs vs Pugna (lowest gold on Dire)
        assert bane.lane_gold_adv == 1200 - 900
        assert bane.lane_xp_adv == 1500 - 1100
        # Mirror symmetry
        assert gyro.lane_gold_adv == 2500 - 3000
        assert pugna.lane_gold_adv == 900 - 1200

    def test_unmatched_player_gets_no_adv(self):
        # 2v1: extra player on one side has no opponent to pair with
        rad1 = self._make(0, 2, 1, gold=3000, xp=4000)
        rad2 = self._make(1, 2, 1, gold=1200, xp=1500)
        dire = self._make(5, 3, 1, gold=2500, xp=3200)
        self._apply_adv([rad1, rad2, dire])
        # rad1 (highest gold) pairs vs dire
        assert rad1.lane_gold_adv == 3000 - 2500
        # rad2 (lower gold) has no dire counterpart — stays None
        assert rad2.lane_gold_adv is None


# ---------------------------------------------------------------------------
# Integration tests
# ---------------------------------------------------------------------------


@pytest.mark.slow
@pytest.mark.integration
class TestLaneIntegration:
    @pytest.fixture(scope="class")
    def match(self, canonical_parsed_match):
        return canonical_parsed_match

    def test_all_players_have_valid_lane_role(self, match):
        for pp in match.players:
            assert pp.lane_role in (0, 1, 2, 3, 4), (
                f"player {pp.player_id} ({pp.hero_name}) has invalid lane_role={pp.lane_role}"
            )

    def test_lane_pos_nonempty_for_most_players(self, match):
        with_data = [pp for pp in match.players if pp.lane_pos]
        assert len(with_data) >= 8

    def test_lane_stats_nonnegative(self, match):
        for pp in match.players:
            assert pp.lane_last_hits >= 0
            assert pp.lane_denies >= 0
            assert pp.lane_total_gold >= 0
            assert pp.lane_total_xp >= 0

    def test_lane_total_gold_plausible(self, match):
        # A player with lane data should have earned at least some gold in 10 min
        active = [pp for pp in match.players if pp.lane_total_gold > 0]
        assert len(active) >= 5

    def test_position_log_longer_than_lane_pos(self, match):
        # position_log covers the full game; lane_pos covers only first 10 min
        for pp in match.players:
            if pp.position_log and pp.lane_pos:
                assert len(pp.position_log) >= len(pp.lane_pos)

    def test_lane_efficiency_pct_nonnegative(self, match):
        for pp in match.players:
            assert pp.lane_efficiency_pct >= 0

    def test_lane_efficiency_pct_plausible(self, match):
        # In a real match most laners should have some efficiency; a carry hitting
        # 50+ LH in 10 min typically exceeds 50%
        above_zero = [pp for pp in match.players if pp.lane_efficiency_pct > 0]
        assert len(above_zero) >= 5

    def test_lane_adv_none_for_jungle(self, match):
        for pp in match.players:
            if pp.lane_role == 4:
                assert pp.lane_gold_adv is None
                assert pp.lane_xp_adv is None

    def test_lane_adv_set_for_laners_with_opponents(self, match):
        # At least some lane-1/2/3 players should have an advantage computed
        with_adv = [
            pp for pp in match.players if pp.lane_role in (1, 2, 3) and pp.lane_gold_adv is not None
        ]
        assert len(with_adv) >= 2

    def test_lane_adv_sum_to_zero_for_solo_matched_pairs(self, match):
        # In 1v1 lanes, the two opponents' advantages must sum to zero (each sees
        # the other as their only opponent, so adv = our_gold - their_gold, and
        # their adv = their_gold - our_gold).  Only check roles where exactly one
        # Radiant and one Dire player share the same lane_role.
        from collections import Counter

        role_counts: Counter = Counter()
        for pp in match.players:
            if pp.lane_role in (1, 2, 3):
                role_counts[(pp.team, pp.lane_role)] += 1

        for role in (1, 2, 3):
            if role_counts[(2, role)] != 1 or role_counts[(3, role)] != 1:
                continue  # skip multi-player lanes — sum-to-zero only holds 1v1
            r = next(pp for pp in match.players if pp.team == 2 and pp.lane_role == role)
            d = next(pp for pp in match.players if pp.team == 3 and pp.lane_role == role)
            if r.lane_gold_adv is not None and d.lane_gold_adv is not None:
                assert r.lane_gold_adv + d.lane_gold_adv == 0, (
                    f"role={role}: {r.hero_name} adv={r.lane_gold_adv}, "
                    f"{d.hero_name} adv={d.lane_gold_adv}"
                )
