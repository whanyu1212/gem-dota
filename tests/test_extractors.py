"""Integration tests for gem.extractors — players, objectives, and wards together.

Unit tests for each extractor live in their dedicated files:
  - test_players_extractor.py
  - test_objectives_extractor.py
  - test_wards_extractor.py

Integration tests here require a real .dem fixture and are marked ``slow`` +
``integration``.
"""

from __future__ import annotations

from pathlib import Path

import pytest

FIXTURE = Path(__file__).parent / "fixtures" / "ti14_finals_g1_xg_vs_falcons.dem"


@pytest.mark.slow
@pytest.mark.integration
class TestExtractorsIntegration:
    @pytest.fixture(autouse=True)
    def _require_fixture(self):
        if not FIXTURE.exists():
            pytest.skip("Integration fixture not available")

    def _parse(self):
        from gem.extractors import ObjectivesExtractor, PlayerExtractor, WardsExtractor
        from gem.parser import ReplayParser

        parser = ReplayParser(str(FIXTURE))
        players = PlayerExtractor(sample_interval=300)
        objectives = ObjectivesExtractor()
        wards = WardsExtractor()
        players.attach(parser)
        objectives.attach(parser)
        wards.attach(parser)
        parser.parse()
        return players, objectives, wards

    def test_objectives_tower_kills_positive(self):
        _, objectives, _ = self._parse()
        assert len(objectives.tower_kills) > 0

    def test_objectives_roshan_kills_nonnegative(self):
        _, objectives, _ = self._parse()
        assert len(objectives.roshan_kills) >= 0

    def test_wards_placements_positive(self):
        _, _, wards = self._parse()
        assert len(wards.ward_events) > 0

    def test_wards_have_some_coordinates(self):
        _, _, wards = self._parse()
        with_coords = [w for w in wards.ward_events if w.x is not None]
        assert len(with_coords) > 0

    def test_player_snapshots_positive(self):
        players, _, _ = self._parse()
        assert len(players.snapshots) > 0

    def test_player_snapshot_fields_valid(self):
        players, _, _ = self._parse()
        for snap in players.snapshots[:20]:
            assert 0 <= snap.player_id <= 9
            assert snap.team in (2, 3)
            assert snap.level >= 0
            assert snap.hp >= 0
            assert snap.tick >= 0

    def test_player_time_series_nonempty(self):
        players, _, _ = self._parse()
        found = False
        for pid in range(10):
            ts = players.time_series(pid)
            if ts.ticks:
                found = True
                assert len(ts.ticks) == len(ts.xp_t) == len(ts.lh_t)
                break
        assert found
