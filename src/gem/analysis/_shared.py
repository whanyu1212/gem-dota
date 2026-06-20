"""Shared constants and helpers for the analysis package.

Centralises the map-geometry constants and the small lookup helpers that were
previously duplicated across :mod:`gem.analysis.roshan`,
:mod:`gem.analysis.map_context`, and :mod:`gem.reports._sections`.
"""

from __future__ import annotations

import bisect
import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gem.results.models import ParsedMatch

# Team numbers (Dota convention).
_TEAM_RADIANT = 2
_TEAM_DIRE = 3

# Map geometry is sourced from the bundled ``map_constants.json`` so there is a
# single source of truth — the same file the public ``catalog.load_map_constants``
# exposes. The literals below are a calibrated fallback used only if the JSON is
# missing or malformed (they must mirror the JSON). Calibrated against
# assets/maps/Game_map_7.40.jpg.
_FALLBACK_MAP_BOUNDS = (7563.0, 25900.0, 7800.0, 25600.0)  # xmin, xmax, ymin, ymax
_FALLBACK_RADIANT_FOUNTAIN = (9684.0, 9684.0)
_FALLBACK_DIRE_FOUNTAIN = (23120.0, 22350.0)
_FALLBACK_RIVER_STRIP = 1200.0


def _load_map_geometry() -> tuple[
    float, float, float, float, tuple[float, float], tuple[float, float], float
]:
    """Load map bounds/fountains/river-strip from ``map_constants.json``.

    Falls back to the calibrated literals if the JSON is unavailable or missing
    keys, so importing the analysis package never fails on a data problem.

    Returns:
        ``(xmin, xmax, ymin, ymax, radiant_fountain, dire_fountain, river_strip)``.
    """
    try:
        from gem.catalog.map import load_map_constants

        data = load_map_constants()
        wb = data["world_bounds"]
        fr = data["fountains"]["radiant"]
        fd = data["fountains"]["dire"]
        return (
            float(wb["xmin"]),
            float(wb["xmax"]),
            float(wb["ymin"]),
            float(wb["ymax"]),
            (float(fr["x"]), float(fr["y"])),
            (float(fd["x"]), float(fd["y"])),
            float(data.get("river_strip", _FALLBACK_RIVER_STRIP)),
        )
    except (OSError, ValueError, KeyError, TypeError):
        return (
            *_FALLBACK_MAP_BOUNDS,
            _FALLBACK_RADIANT_FOUNTAIN,
            _FALLBACK_DIRE_FOUNTAIN,
            _FALLBACK_RIVER_STRIP,
        )


(
    _MAP_XMIN,
    _MAP_XMAX,
    _MAP_YMIN,
    _MAP_YMAX,
    _RADIANT_FOUNTAIN,
    _DIRE_FOUNTAIN,
    _RIVER_STRIP,
) = _load_map_geometry()


def infer_match_end_tick(match: ParsedMatch) -> int:
    """Return the match end tick, falling back to the last observed sample.

    Prefers ``match.game_end_tick`` when set; otherwise uses the latest tick
    seen across player time-series and position logs.

    Args:
        match: The parsed match.

    Returns:
        The end tick (``0`` if no data is available).
    """
    if match.game_end_tick > 0:
        return match.game_end_tick

    max_tick = 0
    for player in match.players:
        if player.times:
            max_tick = max(max_tick, player.times[-1])
        if player.position_log:
            max_tick = max(max_tick, player.position_log[-1][0])
    return max_tick


def region_of(x: float, y: float) -> str:
    """Classify a world position into ``river``, ``radiant_half`` or ``dire_half``.

    Points within the diagonal river strip (``|x - y| <= _RIVER_STRIP``) are the
    river; otherwise the position is assigned to whichever fountain is nearer.
    The threshold is on the ``|x - y|`` difference (the river follows the
    ``x = y`` diagonal), which corresponds to a perpendicular half-width of
    ``_RIVER_STRIP / sqrt(2)`` world units — see the constant's note.

    Args:
        x: World x coordinate.
        y: World y coordinate.

    Returns:
        One of ``"river"``, ``"radiant_half"``, ``"dire_half"``.
    """
    if abs(x - y) <= _RIVER_STRIP:
        return "river"
    dr = math.dist((x, y), _RADIANT_FOUNTAIN)
    dd = math.dist((x, y), _DIRE_FOUNTAIN)
    return "radiant_half" if dr <= dd else "dire_half"


def nearest_series_value(times: list[int], values: list[int], tick: int) -> int:
    """Return the series value whose sample tick is nearest ``tick``.

    Assumes ``times`` is sorted ascending and parallel to ``values``.

    Args:
        times: Ascending sample ticks.
        values: Values parallel to ``times``.
        tick: Tick to look up.

    Returns:
        The nearest value, or ``0`` if either list is empty.
    """
    if not times or not values:
        return 0
    idx = bisect.bisect_left(times, tick)
    if idx <= 0:
        return values[0]
    if idx >= len(times):
        return values[-1]
    before = idx - 1
    after = idx
    if tick - times[before] <= times[after] - tick:
        return values[before]
    return values[after]
