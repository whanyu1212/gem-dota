"""Integration lock-in: the combat-log axis beats the entity axis for intervals.

OpenDota times its interval boundaries on the combat-log timestamp axis, anchored
at the GAME_STATE==5 horn. gem's entity-derived ``game_time_s`` differs from that
axis by a per-replay constant, so sampling boundaries on the entity clock drifts
the per-minute gold/xp/lh curves away from OpenDota.

This test parses one fixture once and attaches two interval extractors: one on the
authoritative combat-log axis (the default) and one forced onto the entity axis. It
asserts the combat-log axis produces a strictly smaller residual against the
published OpenDota arrays. It is a guard against any future change flipping
``IntervalExtractor._clock()`` back to the entity clock.

Marked ``slow`` + ``integration`` — needs a real ``.dem`` plus its ``.opendota.json``.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from gem.extractors.intervals import IntervalExtractor
from gem.parser import ReplayParser

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "opendota"
# Smallest full fixture with a committed OpenDota ground-truth JSON.
_MATCH_ID = 8822520406
_METRICS = ("gold_t", "xp_t", "lh_t", "dn_t")


def _od_slot_to_logical(slot: int) -> int:
    """Map an OpenDota player_slot (radiant 0-4, dire 128-132) to logical 0-9."""
    return slot if slot < 128 else (slot - 128) + 5


def _residual(series_fn, od_by_logical: dict[int, dict]) -> int:
    """Sum element-wise absolute error of a player's minute arrays vs OpenDota."""
    total = 0
    for pid, ref in od_by_logical.items():
        ts = series_fn(pid)
        gem = {"gold_t": ts.gold_t, "xp_t": ts.xp_t, "lh_t": ts.lh_t, "dn_t": ts.dn_t}
        for metric in _METRICS:
            g, r = gem[metric], ref[metric]
            # Compare the overlapping prefix; arrays may differ in trailing length.
            for a, b in zip(g, r, strict=False):
                total += abs(a - b)
    return total


@pytest.mark.slow
@pytest.mark.integration
class TestIntervalAxisLockIn:
    @pytest.fixture(scope="class")
    def axes(self):
        """Parse the fixture once, sampling both clock axes in a single pass.

        Returns:
            ``(combat_log_residual, entity_residual)`` against OpenDota arrays.
        """
        dem = FIXTURES_DIR / f"{_MATCH_ID}.dem"
        od_path = FIXTURES_DIR / f"{_MATCH_ID}.opendota.json"
        if not dem.exists() or not od_path.exists():
            pytest.skip(f"OpenDota fixture {_MATCH_ID} (.dem + .opendota.json) not available")

        parser = ReplayParser(str(dem))

        combat_log_ext = IntervalExtractor(interval_s=60)
        entity_ext = IntervalExtractor(interval_s=60)

        # Force the second extractor onto the entity clock so both axes are
        # measured from the same single parse. The default extractor keeps the
        # authoritative combat-log axis.
        def _entity_clock() -> int | None:
            return getattr(parser, "game_time_s", None)

        entity_ext._clock = _entity_clock  # type: ignore[method-assign]

        combat_log_ext.attach(parser)
        entity_ext.attach(parser)
        parser.parse()

        with open(od_path) as fh:
            od = json.load(fh)
        od_by_logical: dict[int, dict] = {}
        for i, player in enumerate(od.get("players") or []):
            logical = _od_slot_to_logical(player.get("player_slot", i))
            od_by_logical[logical] = {
                "gold_t": player.get("gold_t") or [],
                "xp_t": player.get("xp_t") or [],
                "lh_t": player.get("lh_t") or [],
                "dn_t": player.get("dn_t") or [],
            }

        combat_log_residual = _residual(combat_log_ext.series, od_by_logical)
        entity_residual = _residual(entity_ext.series, od_by_logical)
        return combat_log_residual, entity_residual

    def test_combat_log_axis_residual_is_smaller_than_entity_axis(self, axes):
        combat_log_residual, entity_residual = axes
        # The combat-log axis must beat the entity axis by a wide margin; on this
        # fixture the entity axis drifts the curves by orders of magnitude more.
        assert combat_log_residual < entity_residual

    def test_combat_log_axis_residual_is_small_absolute(self, axes):
        combat_log_residual, _ = axes
        # The nudged combat-log axis lands the per-minute curves within a few
        # hundred total absolute units across all 10 players (measured ~142).
        assert combat_log_residual < 400
