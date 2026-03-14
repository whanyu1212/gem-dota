"""Tests for lane role classification and lane efficiency stats.

Unit tests use synthetic lane_pos dicts and ParsedPlayer instances.
Integration tests parse a real .dem fixture and verify plausible output.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import pytest

from gem.extractors.lane import classify_lane
from gem.models import ParsedPlayer

FIXTURE = Path(__file__).parent / "fixtures" / "ti14_finals_g1_xg_vs_falcons.dem"

_GRID = 64  # must match extractors/lane._GRID and match_builder._LANE_GRID
_LANE_WINDOW = 600 * 30  # 18000 ticks


def _cell(wx: float, wy: float, count: int = 100) -> dict[str, int]:
    """Build a single-cell lane_pos dict at the given world coordinates."""
    gx = int(wx) // _GRID
    gy = int(wy) // _GRID
    return {f"{gx}_{gy}": count}


# ---------------------------------------------------------------------------
# classify_lane — empty / unknown
# ---------------------------------------------------------------------------


class TestClassifyLaneEmpty:
    def test_empty_returns_unknown(self):
        assert classify_lane({}, team=2) == 0

    def test_zero_counts_returns_unknown(self):
        assert classify_lane({"200_200": 0}, team=2) == 0

    def test_unknown_team_does_not_crash(self):
        result = classify_lane(_cell(21500, 10000), team=0)
        assert result in (0, 1, 2, 3, 4, 5)


# ---------------------------------------------------------------------------
# classify_lane — Radiant (team=2) lane zones
# ---------------------------------------------------------------------------


class TestClassifyLaneRadiant:
    def test_safe_lane_bottom_strip(self):
        # Deep bottom, clearly Radiant safe lane
        assert classify_lane(_cell(16000, 9500), team=2) == 1

    def test_safe_lane_bottom_right_corner(self):
        # Far right, low Y — Radiant safe
        assert classify_lane(_cell(21500, 10000), team=2) == 1

    def test_mid_lane_centre(self):
        # Map centre, on the diagonal
        assert classify_lane(_cell(16000, 16000), team=2) == 2

    def test_mid_lane_radiant_side(self):
        # Mid lane closer to Radiant fountain, still on diagonal
        assert classify_lane(_cell(12000, 12000), team=2) == 2

    def test_mid_lane_dire_side(self):
        # Mid lane closer to Dire fountain
        assert classify_lane(_cell(20000, 20000), team=2) == 2

    def test_off_lane_top_left(self):
        # Top-left — Radiant off lane
        assert classify_lane(_cell(10000, 21000), team=2) == 3

    def test_jungle_interior(self):
        # Interior Radiant jungle: far enough from diagonal, above safe-lane Y floor
        assert classify_lane(_cell(17000, 13500), team=2) == 4


# ---------------------------------------------------------------------------
# classify_lane — Dire (team=3) — safe/off mirrored
# ---------------------------------------------------------------------------


class TestClassifyLaneDire:
    def test_safe_lane_top_left(self):
        # Top-left is Dire safe lane
        assert classify_lane(_cell(10000, 21000), team=3) == 1

    def test_off_lane_bottom_right(self):
        # Bottom-right is Dire off lane
        assert classify_lane(_cell(21500, 10000), team=3) == 3

    def test_mid_is_same_for_both_teams(self):
        # Mid doesn't flip
        assert classify_lane(_cell(16000, 16000), team=3) == 2

    def test_jungle_interior_dire(self):
        # Dire jungle: right-side interior, off the diagonal and not safe/off
        assert classify_lane(_cell(20000, 17000), team=3) == 4


# ---------------------------------------------------------------------------
# classify_lane — roaming detection
# ---------------------------------------------------------------------------


class TestClassifyLaneRoaming:
    def test_widely_spread_across_zones_is_roaming(self):
        # Equal dwell spread evenly across all five zones — no dominant zone
        # Zone mapping (wx, wy):
        #   safe_r: (16000, 9500)  — wy < 12500
        #   mid:    (16000, 16000) — on diagonal
        #   off_r:  (10000, 21000) — wx<12500, wy>19000
        #   jungle: (17000, 13500) — interior
        #   other:  (9000, 17000)  — none of the above
        # 5 zones × 20 ticks = 100 total; each zone = 20% < 45% → roaming
        cells = {}
        for wx, wy in [
            (16000, 9500),  # safe_r
            (16000, 16000),  # mid
            (10000, 21000),  # off_r
            (17000, 13500),  # jungle
            (9000, 17000),  # other
        ]:
            gx = int(wx) // _GRID
            gy = int(wy) // _GRID
            cells[f"{gx}_{gy}"] = 20
        assert classify_lane(cells, team=2) == 5

    def test_split_between_two_zones_is_roaming(self):
        # 40% safe_r, 40% off_r, 20% other — no zone dominates at ≥ 45%
        cells = {
            # safe_r cells (40 ticks each zone)
            f"{16000 // _GRID}_{9500 // _GRID}": 20,
            f"{21500 // _GRID}_{10000 // _GRID}": 20,
            # off_r cells
            f"{10000 // _GRID}_{21000 // _GRID}": 20,
            f"{11000 // _GRID}_{20000 // _GRID}": 20,
            # other cell
            f"{9000 // _GRID}_{17000 // _GRID}": 20,
        }
        assert classify_lane(cells, team=2) == 5

    def test_concentrated_is_not_roaming(self):
        # 90% of dwell in safe-lane cells — dominant zone well above 45%
        safe_cells = {
            f"{16000 // _GRID}_{9500 // _GRID}": 450,
            f"{14000 // _GRID}_{10000 // _GRID}": 450,
        }
        spread_cells = {
            f"{16000 // _GRID}_{16000 // _GRID}": 50,  # mid
            f"{10000 // _GRID}_{21000 // _GRID}": 50,  # off_r
        }
        cells = {**safe_cells, **spread_cells}
        assert classify_lane(cells, team=2) != 5


# ---------------------------------------------------------------------------
# lane_pos time filter — logic tests (without a full parser)
# ---------------------------------------------------------------------------


class TestLanePosTimeFilter:
    """Test the time-filter logic used in match_builder to populate lane_pos."""

    def _apply_filter(
        self,
        snaps: list[tuple[int, float, float]],  # (tick, x, y)
        game_start_tick: int | None,
    ) -> dict[str, int]:
        """Replicate the match_builder lane_pos accumulation logic."""
        lane_pos: dict[str, int] = defaultdict(int)
        lane_window = _LANE_WINDOW
        for tick, x, y in snaps:
            if game_start_tick is not None and (
                tick < game_start_tick or tick > game_start_tick + lane_window
            ):
                continue
            lane_pos[f"{int(x) // _GRID}_{int(y) // _GRID}"] += 1
        return dict(lane_pos)

    def test_snaps_at_start_included(self):
        gst = 1000
        result = self._apply_filter([(gst, 10000, 10000)], gst)
        assert len(result) == 1

    def test_snaps_at_end_of_window_included(self):
        gst = 1000
        result = self._apply_filter([(gst + _LANE_WINDOW, 10000, 10000)], gst)
        assert len(result) == 1

    def test_snaps_after_window_excluded(self):
        gst = 1000
        result = self._apply_filter([(gst + _LANE_WINDOW + 1, 10000, 10000)], gst)
        assert len(result) == 0

    def test_snaps_before_game_start_excluded(self):
        gst = 1000
        result = self._apply_filter([(gst - 1, 10000, 10000)], gst)
        assert len(result) == 0

    def test_no_game_start_tick_includes_all(self):
        snaps = [(0, 10000, 10000), (99999, 20000, 20000)]
        result = self._apply_filter(snaps, game_start_tick=None)
        assert len(result) == 2

    def test_position_log_is_independent(self):
        # position_log is built without any time filter — verify the contract
        gst = 1000
        snaps = [
            (gst - 500, 9000.0, 9000.0),  # before game start
            (gst + 100, 10000.0, 10000.0),  # in window
            (gst + 99999, 20000.0, 20000.0),  # far past window
        ]
        # position_log never filters by tick — all snaps should appear
        position_log = [(tick, x, y) for tick, x, y in snaps]
        assert len(position_log) == 3


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
        """Replicate match_builder Tier-2 advantage computation."""
        _LANE_ROLES_WITH_OPPONENTS = {1, 2, 3}
        for pp in players:
            if pp.lane_role not in _LANE_ROLES_WITH_OPPONENTS:
                continue
            opp_team = 3 if pp.team == 2 else 2
            opponents = [
                op for op in players if op.team == opp_team and op.lane_role == pp.lane_role
            ]
            if not opponents:
                continue
            pp.lane_gold_adv = pp.lane_total_gold - sum(op.lane_total_gold for op in opponents)
            pp.lane_xp_adv = pp.lane_total_xp - sum(op.lane_total_xp for op in opponents)

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

    def test_roaming_excluded_from_adv(self):
        roamer = self._make(0, 2, 5, gold=2000, xp=2500)
        opponent = self._make(5, 3, 5, gold=1500, xp=2000)
        self._apply_adv([roamer, opponent])
        assert roamer.lane_gold_adv is None

    def test_dual_lane_sums_both_opponents(self):
        # 2-hero safe lane vs solo: adv = our_gold - sum(both opponents)
        rad = self._make(0, 2, 1, gold=2000, xp=3000)
        dire1 = self._make(5, 3, 1, gold=1000, xp=1500)
        dire2 = self._make(6, 3, 1, gold=800, xp=1200)
        self._apply_adv([rad, dire1, dire2])
        assert rad.lane_gold_adv == 2000 - (1000 + 800)
        assert rad.lane_xp_adv == 3000 - (1500 + 1200)


# ---------------------------------------------------------------------------
# Integration tests
# ---------------------------------------------------------------------------


@pytest.mark.slow
@pytest.mark.integration
class TestLaneIntegration:
    @pytest.fixture(scope="class")
    def match(self):
        import gem

        return gem.parse(str(FIXTURE))

    def test_all_players_have_valid_lane_role(self, match):
        for pp in match.players:
            assert pp.lane_role in (0, 1, 2, 3, 4, 5), (
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

    def test_lane_adv_none_for_jungle_and_roaming(self, match):
        for pp in match.players:
            if pp.lane_role in (4, 5):
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
