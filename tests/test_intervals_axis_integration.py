"""Integration lock-in for OpenDota's tick-start interval boundary.

OpenDota reads interval entities from Clarity's ``@OnTickStart`` callback. Gem
decodes ``CNETMsg_Tick``, samples minute zero immediately, and queues later
rounded-minute crossings for the following tick start to reproduce Clarity's
effective phase. This fixture locks in point-level parity against the published
arrays.

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


def _residuals(series_fn, od_by_logical: dict[int, dict]) -> dict[str, int]:
    """Sum element-wise absolute error by metric vs OpenDota."""
    totals = dict.fromkeys(_METRICS, 0)
    for pid, ref in od_by_logical.items():
        ts = series_fn(pid)
        gem = {"gold_t": ts.gold_t, "xp_t": ts.xp_t, "lh_t": ts.lh_t, "dn_t": ts.dn_t}
        for metric in _METRICS:
            g, r = gem[metric], ref[metric]
            # Compare the overlapping prefix; arrays may differ in trailing length.
            for a, b in zip(g, r, strict=False):
                totals[metric] += abs(a - b)
    return totals


@pytest.mark.slow
@pytest.mark.integration
class TestIntervalAxisLockIn:
    @pytest.fixture(scope="class")
    def residuals(self):
        """Parse once and return per-metric residuals against OpenDota."""
        dem = FIXTURES_DIR / f"{_MATCH_ID}.dem"
        od_path = FIXTURES_DIR / f"{_MATCH_ID}.opendota.json"
        if not dem.exists() or not od_path.exists():
            pytest.skip(f"OpenDota fixture {_MATCH_ID} (.dem + .opendota.json) not available")

        parser = ReplayParser(str(dem))

        interval_ext = IntervalExtractor(interval_s=60)
        interval_ext.attach(parser)
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

        return _residuals(interval_ext.series, od_by_logical)

    def test_tick_start_xp_lh_and_denies_are_exact(self, residuals):
        assert residuals["xp_t"] == 0
        assert residuals["lh_t"] == 0
        assert residuals["dn_t"] == 0

    def test_tick_start_gold_is_exact(self, residuals):
        assert residuals["gold_t"] == 0
