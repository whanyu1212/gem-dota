from __future__ import annotations

import pytest

from gem.analysis._territory import RoshTerritoryConfig, build_territory_window
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


def test_player_time_completeness_threshold_is_inclusive_at_seventy_percent() -> None:
    def _truncated(end: int) -> ParsedMatch:
        players: list[ParsedPlayer] = []
        for player_id in range(10):
            point = (24000.0, 21000.0) if player_id < 5 else (8804.0, 11034.0)
            player = _sampled_player(
                player_id,
                2 if player_id < 5 else 3,
                point,
                end=end,
            )
            if player.position_log[-1][0] != end:
                player.position_log.append((end, *point))
            players.append(player)
        return ParsedMatch(players=players)

    at_threshold = build_territory_window(_truncated(2520), 2, 0, 3600)
    below_threshold = build_territory_window(_truncated(2400), 2, 0, 3600)

    assert at_threshold.status == "complete"
    assert at_threshold.conversion_player_time_coverage == pytest.approx(0.70)
    assert below_threshold.status == "unavailable"
    assert below_threshold.conversion_player_time_coverage == pytest.approx(2 / 3)


def test_cell_bucket_and_depth_settings_are_reproducible_for_sensitivity_checks() -> None:
    stationary = _paired_match((24000.0, 21000.0), (8804.0, 11034.0))
    default = build_territory_window(stationary, 2, 0, 3600)
    larger_cells = build_territory_window(
        stationary,
        2,
        0,
        3600,
        config=RoshTerritoryConfig(cell_size=1200.0),
    )
    wider_buckets = build_territory_window(
        stationary,
        2,
        0,
        3600,
        config=RoshTerritoryConfig(bucket_ticks=60 * 30),
    )

    assert larger_cells.conversion_coverage_pct != pytest.approx(default.conversion_coverage_pct)
    assert wider_buckets.conversion_coverage_pct == pytest.approx(default.conversion_coverage_pct)

    players = [_sampled_player(player_id, 2, (20500.0, 18500.0)) for player_id in range(5)]
    players[0].position_log[-2:] = [
        (3300, 25000.0, 22000.0),
        (3600, 25000.0, 22000.0),
    ]
    players.extend(_sampled_player(player_id, 3, (8804.0, 11034.0)) for player_id in range(5, 10))
    depth_match = ParsedMatch(players=players)
    p90 = build_territory_window(depth_match, 2, 0, 3600)
    maximum = build_territory_window(
        depth_match,
        2,
        0,
        3600,
        config=RoshTerritoryConfig(depth_percentile=1.0),
    )
    assert maximum.conversion_depth_p90 > p90.conversion_depth_p90


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"cell_size": 0.0}, "cell_size"),
        ({"bucket_ticks": 0}, "bucket_ticks"),
        ({"min_player_time_coverage": 1.1}, "min_player_time_coverage"),
        ({"depth_percentile": 0.0}, "depth_percentile"),
    ],
)
def test_territory_config_rejects_invalid_values(kwargs: dict, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        RoshTerritoryConfig(**kwargs)
