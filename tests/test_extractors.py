"""Integration tests for gem.extractors — players, objectives, and wards together.

Unit tests for each extractor live in their dedicated files:
  - test_players_extractor.py
  - test_objectives_extractor.py
  - test_wards_extractor.py

Integration tests here require a real .dem fixture and are marked ``slow`` +
``integration``.
"""

from __future__ import annotations

import pytest


@pytest.mark.slow
@pytest.mark.integration
class TestExtractorsIntegration:
    @pytest.fixture(scope="class")
    def extractors(self, full_replay_path):
        """Parse the replay once per class and share the attached extractors.

        Class-scoped so the full replay fixture is parsed a single time for the whole
        class instead of once per test method.

        Returns:
            A ``(players, objectives, wards)`` tuple of populated extractors.
        """
        from gem.extractors import ObjectivesExtractor, PlayerExtractor, WardsExtractor
        from gem.parser import ReplayParser

        parser = ReplayParser(str(full_replay_path))
        players = PlayerExtractor(sample_interval=300)
        objectives = ObjectivesExtractor()
        wards = WardsExtractor()
        players.attach(parser)
        objectives.attach(parser)
        wards.attach(parser)
        parser.parse()
        return players, objectives, wards

    def test_objectives_tower_kills_positive(self, extractors):
        _, objectives, _ = extractors
        assert len(objectives.tower_kills) > 0

    def test_objectives_roshan_kills_nonnegative(self, extractors):
        _, objectives, _ = extractors
        assert len(objectives.roshan_kills) >= 0

    def test_wards_placements_positive(self, extractors):
        _, _, wards = extractors
        assert len(wards.ward_events) > 0

    def test_wards_have_some_coordinates(self, extractors):
        _, _, wards = extractors
        with_coords = [w for w in wards.ward_events if w.x is not None]
        assert len(with_coords) > 0

    def test_player_snapshots_positive(self, extractors):
        players, _, _ = extractors
        assert len(players.snapshots) > 0

    def test_player_snapshot_fields_valid(self, extractors):
        players, _, _ = extractors
        for snap in players.snapshots[:20]:
            assert 0 <= snap.player_id <= 9
            assert snap.team in (2, 3)
            assert snap.level >= 0
            assert snap.hp >= 0
            assert snap.tick >= 0

    def test_player_time_series_nonempty(self, extractors):
        players, _, _ = extractors
        found = False
        for pid in range(10):
            ts = players.time_series(pid)
            if ts.ticks:
                found = True
                assert len(ts.ticks) == len(ts.xp_t) == len(ts.lh_t)
                break
        assert found
