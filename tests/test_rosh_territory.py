from __future__ import annotations

import pytest

from gem.analysis._territory import build_territory_window
from gem.results.models import ParsedMatch, ParsedPlayer


def _sampled_player(
    player_id: int,
    team: int,
    point: tuple[float, float],
    *,
    start: int = 0,
    end: int = 3600,
    step: int = 300,
) -> ParsedPlayer:
    return ParsedPlayer(
        player_id=player_id,
        team=team,
        position_log=[(tick, *point) for tick in range(start, end + 1, step)],
    )


def _paired_match(
    radiant_point: tuple[float, float],
    dire_point: tuple[float, float],
    *,
    step: int = 300,
) -> ParsedMatch:
    return ParsedMatch(
        players=[
            *[_sampled_player(pid, 2, radiant_point, step=step) for pid in range(5)],
            *[_sampled_player(pid, 3, dire_point, step=step) for pid in range(5, 10)],
        ]
    )


def test_grid_occupancy_is_sample_frequency_invariant() -> None:
    sparse = _paired_match((24000.0, 21000.0), (8804.0, 11034.0), step=300)
    dense = _paired_match((24000.0, 21000.0), (8804.0, 11034.0), step=150)

    sparse_window = build_territory_window(sparse, 2, 0, 3600)
    dense_window = build_territory_window(dense, 2, 0, 3600)

    assert sparse_window.status == "complete"
    assert dense_window.status == "complete"
    assert sparse_window.conversion_coverage_pct == pytest.approx(
        dense_window.conversion_coverage_pct
    )
    assert sparse_window.conversion_depth_p90 == pytest.approx(dense_window.conversion_depth_p90)
    assert len(sparse_window.conversion_cells) == 1
    cell = sparse_window.conversion_cells[0]
    assert cell.hero_seconds == pytest.approx(5 * 120)
    assert cell.distinct_heroes == 5
    assert cell.x_min <= 24000.0 <= cell.x_max
    assert cell.y_min <= 21000.0 <= cell.y_max


def test_gap_is_not_interpolated_and_fails_evidence_floor() -> None:
    players = [
        ParsedPlayer(
            player_id=pid,
            team=2 if pid < 5 else 3,
            position_log=[
                (0, 24000.0, 21000.0),
                (301, 8804.0, 11034.0),
                (3600, 8804.0, 11034.0),
            ],
        )
        for pid in range(10)
    ]
    window = build_territory_window(ParsedMatch(players=players), 2, 0, 3600)

    assert window.status == "unavailable"
    assert window.conversion_coverage_pct is None
    assert window.conversion_cells == []
    assert window.conversion_player_time_coverage == 0.0


def test_depth_is_symmetric_and_uses_weighted_p90_not_max() -> None:
    # The two points are reflections across the midpoint between fountains, so
    # the normalized forward depth is identical for opposite teams.
    symmetric = _paired_match((24000.0, 21000.0), (8804.0, 11034.0))
    window = build_territory_window(symmetric, 2, 0, 3600)
    assert window.conversion_depth_p90 == pytest.approx(window.opponent_depth_p90)

    # One final 10-second deep observation is under ten percent of observed
    # time.  A weighted p90 therefore stays at the repeated shallower position.
    players: list[ParsedPlayer] = []
    for pid in range(5):
        samples = [(tick, 20500.0, 18500.0) for tick in range(0, 3301, 300)]
        if pid == 0:
            samples.extend([(3300, 25000.0, 22000.0), (3600, 25000.0, 22000.0)])
        else:
            samples.append((3600, 20500.0, 18500.0))
        players.append(ParsedPlayer(player_id=pid, team=2, position_log=samples))
    players.extend(_sampled_player(pid, 3, (8804.0, 11034.0)) for pid in range(5, 10))
    outlier_window = build_territory_window(ParsedMatch(players=players), 2, 0, 3600)
    shallow_window = build_territory_window(
        _paired_match((20500.0, 18500.0), (8804.0, 11034.0)), 2, 0, 3600
    )
    assert outlier_window.conversion_depth_p90 == pytest.approx(shallow_window.conversion_depth_p90)


def test_missing_positions_are_none_not_zero() -> None:
    players = [ParsedPlayer(player_id=pid, team=2 if pid < 5 else 3) for pid in range(10)]
    window = build_territory_window(ParsedMatch(players=players), 2, 0, 3600)
    assert window.status == "unavailable"
    assert window.conversion_coverage_pct is None
    assert window.opponent_coverage_pct is None
    assert window.coverage_differential_pct is None
    assert window.conversion_depth_p90 is None


def test_complete_sampling_without_forward_presence_has_zero_depth() -> None:
    match = _paired_match((8804.0, 11034.0), (24000.0, 21000.0))
    window = build_territory_window(match, 2, 0, 3600)

    assert window.status == "complete"
    assert window.conversion_coverage_pct == 0.0
    assert window.opponent_coverage_pct == 0.0
    assert window.conversion_depth_p90 == 0.0
    assert window.opponent_depth_p90 == 0.0
    assert window.depth_differential == 0.0
