"""Integration lock-in for OpenDota's tick-start interval boundary.

OpenDota reads interval entities from Clarity's ``@OnTickStart`` callback. Gem
decodes ``CNETMsg_Tick`` and queues rounded-minute crossings for the following
tick start to reproduce Clarity's effective phase. Minute zero is the batch read when the raw clock reached the
rounded game start, which can precede the tick where the start becomes visible
(8855242704: start seen only after the rounded clock passed 0; 8974053011: a last
hit between the two). These fixtures lock in exact parity, length included,
against the published arrays.

Marked ``slow`` + ``integration`` — needs a real ``.dem`` plus its ``.opendota.json``.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from gem.extractors.intervals import IntervalExtractor
from gem.parser import ReplayParser

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "opendota"
# The smallest full fixture, plus the two minute-zero edge cases above.
_MATCH_IDS = (8822520406, 8855242704, 8974053011)
_METRICS = ("gold_t", "xp_t", "lh_t", "dn_t")


def _od_slot_to_logical(slot: int) -> int:
    """Map an OpenDota player_slot (radiant 0-4, dire 128-132) to logical 0-9."""
    return slot if slot < 128 else (slot - 128) + 5


def _mismatches(series_fn, od_by_logical: dict[int, dict]) -> dict[str, list[int]]:
    """Return, per metric, the players whose full array differs from OpenDota."""
    bad: dict[str, list[int]] = {metric: [] for metric in _METRICS}
    for pid, ref in od_by_logical.items():
        ts = series_fn(pid)
        gem = {"gold_t": ts.gold_t, "xp_t": ts.xp_t, "lh_t": ts.lh_t, "dn_t": ts.dn_t}
        for metric in _METRICS:
            if gem[metric] != ref[metric]:
                bad[metric].append(pid)
    return bad


@pytest.mark.slow
@pytest.mark.integration
class TestIntervalAxisLockIn:
    @pytest.fixture(scope="class", params=_MATCH_IDS)
    def mismatches(self, request):
        """Parse once per fixture and return players differing from OpenDota."""
        match_id = request.param
        dem = FIXTURES_DIR / f"{match_id}.dem"
        od_path = FIXTURES_DIR / f"{match_id}.opendota.json"
        if not dem.exists() or not od_path.exists():
            pytest.skip(f"OpenDota fixture {match_id} (.dem + .opendota.json) not available")

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

        return _mismatches(interval_ext.series, od_by_logical)

    def test_tick_start_xp_lh_and_denies_are_exact(self, mismatches):
        assert mismatches["xp_t"] == []
        assert mismatches["lh_t"] == []
        assert mismatches["dn_t"] == []

    def test_tick_start_gold_is_exact(self, mismatches):
        assert mismatches["gold_t"] == []
