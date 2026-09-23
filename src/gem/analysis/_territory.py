"""Territory evidence for Roshan conversion analysis.

Positions are the replay's observed hero samples.  Intervals longer than ten
seconds are deliberately not filled, so disconnects, missing snapshots, and
teleports cannot create synthetic map control.

Reference: pinned OpenDota parser revision documented in ``CLAUDE.md``
(``src/main/java/opendota/Parse.java``; hero coordinates).
"""

from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal

from gem.analysis._shared import (
    _DIRE_FOUNTAIN,
    _MAP_XMAX,
    _MAP_XMIN,
    _MAP_YMAX,
    _MAP_YMIN,
    _RADIANT_FOUNTAIN,
    _TEAM_DIRE,
    _TEAM_RADIANT,
    region_of,
)

if TYPE_CHECKING:
    from gem.results.models import ParsedMatch, ParsedPlayer

_TICKS_PER_SECOND = 30
_CELL_SIZE = 600.0
_BUCKET_TICKS = 30 * _TICKS_PER_SECOND
_MAX_SAMPLE_GAP_TICKS = 10 * _TICKS_PER_SECOND
_MIN_HERO_SECONDS = 10.0
_MIN_DISTINCT_HEROES = 2
_MIN_PLAYER_TIME_COVERAGE = 0.70


@dataclass(frozen=True, slots=True)
class RoshTerritoryConfig:
    """Inspectable calibration inputs for sampled territory evidence."""

    cell_size: float = _CELL_SIZE
    bucket_ticks: int = _BUCKET_TICKS
    max_sample_gap_ticks: int = _MAX_SAMPLE_GAP_TICKS
    min_hero_seconds: float = _MIN_HERO_SECONDS
    min_distinct_heroes: int = _MIN_DISTINCT_HEROES
    min_player_time_coverage: float = _MIN_PLAYER_TIME_COVERAGE
    depth_percentile: float = 0.90

    def __post_init__(self) -> None:
        if self.cell_size <= 0:
            raise ValueError("cell_size must be positive")
        if self.bucket_ticks <= 0:
            raise ValueError("bucket_ticks must be positive")
        if self.max_sample_gap_ticks <= 0:
            raise ValueError("max_sample_gap_ticks must be positive")
        if self.min_hero_seconds < 0:
            raise ValueError("min_hero_seconds must be nonnegative")
        if self.min_distinct_heroes < 1:
            raise ValueError("min_distinct_heroes must be positive")
        if not 0.0 <= self.min_player_time_coverage <= 1.0:
            raise ValueError("min_player_time_coverage must be between 0 and 1")
        if not 0.0 < self.depth_percentile <= 1.0:
            raise ValueError("depth_percentile must be greater than 0 and at most 1")


DEFAULT_ROSH_TERRITORY_CONFIG = RoshTerritoryConfig()


@dataclass
class RoshCoverageCell:
    """One bounded world-grid cell represented in a territory window.

    Attributes:
        grid_x: Zero-based column in the calibrated world bounds.
        grid_y: Zero-based row in the calibrated world bounds.
        x_min: Inclusive lower world-x bound.
        x_max: Inclusive upper world-x bound, clipped to the map.
        y_min: Inclusive lower world-y bound.
        y_max: Inclusive upper world-y bound, clipped to the map.
        hero_seconds: Observed hero-seconds in the cell across the window.
        distinct_heroes: Number of distinct heroes observed in the cell.
        occupied_buckets: Number of 30-second buckets where the cell met the
            occupancy threshold.
        bucket_count: Number of buckets in the window.
        occupancy_share: Fraction of window buckets in which the cell was
            occupied.
    """

    grid_x: int = 0
    grid_y: int = 0
    x_min: float = 0.0
    x_max: float = 0.0
    y_min: float = 0.0
    y_max: float = 0.0
    hero_seconds: float = 0.0
    distinct_heroes: int = 0
    occupied_buckets: int = 0
    bucket_count: int = 0
    occupancy_share: float = 0.0


@dataclass
class RoshTerritoryWindow:
    """Paired territory evidence for the conversion team and its opponent.

    Coverage is the time-weighted average percentage of enemy-side map area
    occupied per 30-second bucket.  Depth is the time-weighted 90th percentile
    of observed enemy-side positions, normalized from the side boundary (0) to
    the enemy fountain (1).  A side is unavailable unless at least 70 percent
    of its expected player-time is represented by sample intervals no longer
    than ten seconds.

    Attributes:
        start_tick: Inclusive beginning of the evidence window.
        end_tick: Inclusive end of the evidence window.
        conversion_coverage_pct: Conversion team's enemy-side coverage percent.
        opponent_coverage_pct: Opponent's enemy-side coverage percent.
        coverage_differential_pct: Conversion minus opponent coverage.
        conversion_depth_p90: Conversion team's time-weighted depth p90.
        opponent_depth_p90: Opponent's time-weighted depth p90.
        depth_differential: Conversion minus opponent depth.
        conversion_player_time_coverage: Fraction of expected conversion-team
            player-time supported by valid sample intervals.
        opponent_player_time_coverage: Equivalent opponent evidence fraction.
        conversion_cells: Bounded aggregate cells for the conversion team.
        opponent_cells: Bounded aggregate cells for the opponent.
        status: Evidence availability for the paired window.
        status_reasons: Machine-readable explanations for partial/unavailable
            evidence.
    """

    start_tick: int = 0
    end_tick: int = 0
    conversion_coverage_pct: float | None = None
    opponent_coverage_pct: float | None = None
    coverage_differential_pct: float | None = None
    conversion_depth_p90: float | None = None
    opponent_depth_p90: float | None = None
    depth_differential: float | None = None
    conversion_player_time_coverage: float | None = None
    opponent_player_time_coverage: float | None = None
    conversion_cells: list[RoshCoverageCell] = field(default_factory=list)
    opponent_cells: list[RoshCoverageCell] = field(default_factory=list)
    status: Literal["complete", "partial", "unavailable"] = "unavailable"
    status_reasons: list[str] = field(default_factory=list)


@dataclass
class _SideTerritory:
    coverage_pct: float | None
    depth_p90: float | None
    player_time_coverage: float | None
    cells: list[RoshCoverageCell]


def _enemy_region(team: int) -> str:
    return "dire_half" if team == _TEAM_RADIANT else "radiant_half"


def _grid_shape(config: RoshTerritoryConfig) -> tuple[int, int]:
    return (
        math.ceil((_MAP_XMAX - _MAP_XMIN) / config.cell_size),
        math.ceil((_MAP_YMAX - _MAP_YMIN) / config.cell_size),
    )


def _cell_index(x: float, y: float, config: RoshTerritoryConfig) -> tuple[int, int] | None:
    if not (_MAP_XMIN <= x <= _MAP_XMAX and _MAP_YMIN <= y <= _MAP_YMAX):
        return None
    nx, ny = _grid_shape(config)
    gx = min(int((x - _MAP_XMIN) // config.cell_size), nx - 1)
    gy = min(int((y - _MAP_YMIN) // config.cell_size), ny - 1)
    return gx, gy


def _cell_bounds(
    cell: tuple[int, int], config: RoshTerritoryConfig
) -> tuple[float, float, float, float]:
    gx, gy = cell
    x_min = _MAP_XMIN + gx * config.cell_size
    y_min = _MAP_YMIN + gy * config.cell_size
    return (
        x_min,
        min(x_min + config.cell_size, _MAP_XMAX),
        y_min,
        min(y_min + config.cell_size, _MAP_YMAX),
    )


def _cell_area(cell: tuple[int, int], config: RoshTerritoryConfig) -> float:
    x_min, x_max, y_min, y_max = _cell_bounds(cell, config)
    return (x_max - x_min) * (y_max - y_min)


def _enemy_cells(team: int, config: RoshTerritoryConfig) -> dict[tuple[int, int], float]:
    wanted_region = _enemy_region(team)
    nx, ny = _grid_shape(config)
    cells: dict[tuple[int, int], float] = {}
    for gx in range(nx):
        for gy in range(ny):
            bounds = _cell_bounds((gx, gy), config)
            center_x = (bounds[0] + bounds[1]) / 2
            center_y = (bounds[2] + bounds[3]) / 2
            if region_of(center_x, center_y) == wanted_region:
                cells[(gx, gy)] = _cell_area((gx, gy), config)
    return cells


def _depth(team: int, x: float, y: float) -> float:
    own = _RADIANT_FOUNTAIN if team == _TEAM_RADIANT else _DIRE_FOUNTAIN
    enemy = _DIRE_FOUNTAIN if team == _TEAM_RADIANT else _RADIANT_FOUNTAIN
    axis_x = enemy[0] - own[0]
    axis_y = enemy[1] - own[1]
    axis_len_sq = axis_x * axis_x + axis_y * axis_y
    if axis_len_sq <= 0:
        return 0.0
    projection = ((x - own[0]) * axis_x + (y - own[1]) * axis_y) / axis_len_sq
    # Projection 0.5 is the symmetric side boundary; the enemy fountain is 1.
    return max(0.0, min(1.0, (projection - 0.5) * 2.0))


def _weighted_percentile(values: list[tuple[float, float]], quantile: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values, key=lambda item: item[0])
    total_weight = sum(weight for _, weight in ordered)
    if total_weight <= 0:
        return None
    target = total_weight * quantile
    cumulative = 0.0
    for value, weight in ordered:
        cumulative += weight
        if cumulative >= target:
            return value
    return ordered[-1][0]


def _sample_intervals(
    player: ParsedPlayer,
    start_tick: int,
    end_tick: int,
    config: RoshTerritoryConfig,
) -> list[tuple[int, int, float, float]]:
    samples = sorted(player.position_log)
    intervals: list[tuple[int, int, float, float]] = []
    for current, following in zip(samples, samples[1:], strict=False):
        tick, x, y = current
        next_tick = following[0]
        if next_tick <= tick or next_tick - tick > config.max_sample_gap_ticks:
            continue
        interval_start = max(tick, start_tick)
        interval_end = min(next_tick, end_tick)
        if interval_end > interval_start:
            intervals.append((interval_start, interval_end, x, y))
    return intervals


def _split_bucket_intervals(
    interval_start: int,
    interval_end: int,
    window_start: int,
    config: RoshTerritoryConfig,
) -> list[tuple[int, int]]:
    pieces: list[tuple[int, int]] = []
    cursor = interval_start
    while cursor < interval_end:
        bucket = (cursor - window_start) // config.bucket_ticks
        boundary = window_start + (bucket + 1) * config.bucket_ticks
        piece_end = min(interval_end, boundary)
        pieces.append((int(bucket), piece_end - cursor))
        cursor = piece_end
    return pieces


def _side_territory(
    match: ParsedMatch,
    team: int,
    start_tick: int,
    end_tick: int,
    config: RoshTerritoryConfig,
) -> _SideTerritory:
    players = [player for player in match.players if player.team == team]
    duration_ticks = max(end_tick - start_tick, 0)
    if not players or duration_ticks <= 0:
        return _SideTerritory(None, None, None, [])

    expected_ticks = duration_ticks * len(players)
    observed_ticks = 0
    enemy_cells = _enemy_cells(team, config)
    enemy_area = sum(enemy_cells.values())
    bucket_cell_seconds: defaultdict[tuple[int, tuple[int, int]], float] = defaultdict(float)
    bucket_cell_heroes: defaultdict[tuple[int, tuple[int, int]], set[int]] = defaultdict(set)
    cell_seconds: defaultdict[tuple[int, int], float] = defaultdict(float)
    cell_heroes: defaultdict[tuple[int, int], set[int]] = defaultdict(set)
    depth_values: list[tuple[float, float]] = []

    for player in players:
        for interval_start, interval_end, x, y in _sample_intervals(
            player, start_tick, end_tick, config
        ):
            interval_ticks = interval_end - interval_start
            observed_ticks += interval_ticks
            cell = _cell_index(x, y, config)
            if cell is None or cell not in enemy_cells:
                continue
            seconds = interval_ticks / _TICKS_PER_SECOND
            cell_seconds[cell] += seconds
            cell_heroes[cell].add(player.player_id)
            depth_values.append((_depth(team, x, y), seconds))
            for bucket, piece_ticks in _split_bucket_intervals(
                interval_start, interval_end, start_tick, config
            ):
                key = (bucket, cell)
                bucket_cell_seconds[key] += piece_ticks / _TICKS_PER_SECOND
                bucket_cell_heroes[key].add(player.player_id)

    evidence_fraction = observed_ticks / expected_ticks if expected_ticks else None
    if evidence_fraction is None or evidence_fraction < config.min_player_time_coverage:
        return _SideTerritory(None, None, evidence_fraction, [])

    bucket_count = math.ceil(duration_ticks / config.bucket_ticks)
    occupied_by_bucket: defaultdict[int, set[tuple[int, int]]] = defaultdict(set)
    cell_occupied_buckets: defaultdict[tuple[int, int], set[int]] = defaultdict(set)
    for (bucket, cell), hero_seconds in bucket_cell_seconds.items():
        heroes = bucket_cell_heroes[(bucket, cell)]
        if hero_seconds >= config.min_hero_seconds or len(heroes) >= config.min_distinct_heroes:
            occupied_by_bucket[bucket].add(cell)
            cell_occupied_buckets[cell].add(bucket)

    coverage_weighted_sum = 0.0
    total_bucket_seconds = 0.0
    for bucket in range(bucket_count):
        bucket_start = start_tick + bucket * config.bucket_ticks
        bucket_end = min(end_tick, bucket_start + config.bucket_ticks)
        bucket_seconds = max(bucket_end - bucket_start, 0) / _TICKS_PER_SECOND
        occupied_area = sum(enemy_cells[cell] for cell in occupied_by_bucket[bucket])
        coverage = (occupied_area / enemy_area * 100.0) if enemy_area else 0.0
        coverage_weighted_sum += coverage * bucket_seconds
        total_bucket_seconds += bucket_seconds

    cells: list[RoshCoverageCell] = []
    for cell in sorted(cell_occupied_buckets):
        x_min, x_max, y_min, y_max = _cell_bounds(cell, config)
        occupied = len(cell_occupied_buckets[cell])
        cells.append(
            RoshCoverageCell(
                grid_x=cell[0],
                grid_y=cell[1],
                x_min=x_min,
                x_max=x_max,
                y_min=y_min,
                y_max=y_max,
                hero_seconds=cell_seconds[cell],
                distinct_heroes=len(cell_heroes[cell]),
                occupied_buckets=occupied,
                bucket_count=bucket_count,
                occupancy_share=occupied / bucket_count if bucket_count else 0.0,
            )
        )

    coverage_pct = coverage_weighted_sum / total_bucket_seconds if total_bucket_seconds else None
    depth_p90 = _weighted_percentile(depth_values, config.depth_percentile)
    # With sufficient player-time, no enemy-side samples is observed evidence
    # of zero forward depth, not missing telemetry.
    if depth_p90 is None:
        depth_p90 = 0.0
    return _SideTerritory(
        coverage_pct=coverage_pct,
        depth_p90=depth_p90,
        player_time_coverage=evidence_fraction,
        cells=cells,
    )


def build_territory_window(
    match: ParsedMatch,
    conversion_team: int,
    start_tick: int,
    end_tick: int,
    *,
    config: RoshTerritoryConfig = DEFAULT_ROSH_TERRITORY_CONFIG,
) -> RoshTerritoryWindow:
    """Build paired conversion/opponent territory evidence for one window.

    ``config`` is public so calibration and sensitivity checks can reproduce
    alternate cell, bucket, completeness, and percentile settings without
    mutating module globals.
    """
    opponent_team = _TEAM_DIRE if conversion_team == _TEAM_RADIANT else _TEAM_RADIANT
    conversion = _side_territory(match, conversion_team, start_tick, end_tick, config)
    opponent = _side_territory(match, opponent_team, start_tick, end_tick, config)
    reasons: list[str] = []
    if conversion.coverage_pct is None:
        reasons.append("conversion_team_position_coverage_below_70pct")
    if opponent.coverage_pct is None:
        reasons.append("opponent_position_coverage_below_70pct")
    if not reasons:
        status: Literal["complete", "partial", "unavailable"] = "complete"
    elif len(reasons) == 1:
        status = "partial"
    else:
        status = "unavailable"

    coverage_differential = None
    if conversion.coverage_pct is not None and opponent.coverage_pct is not None:
        coverage_differential = conversion.coverage_pct - opponent.coverage_pct
    depth_differential = None
    if conversion.depth_p90 is not None and opponent.depth_p90 is not None:
        depth_differential = conversion.depth_p90 - opponent.depth_p90

    return RoshTerritoryWindow(
        start_tick=start_tick,
        end_tick=end_tick,
        conversion_coverage_pct=conversion.coverage_pct,
        opponent_coverage_pct=opponent.coverage_pct,
        coverage_differential_pct=coverage_differential,
        conversion_depth_p90=conversion.depth_p90,
        opponent_depth_p90=opponent.depth_p90,
        depth_differential=depth_differential,
        conversion_player_time_coverage=conversion.player_time_coverage,
        opponent_player_time_coverage=opponent.player_time_coverage,
        conversion_cells=conversion.cells,
        opponent_cells=opponent.cells,
        status=status,
        status_reasons=reasons,
    )
