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

# World-coordinate bounds calibrated against assets/maps/Game_map_7.40.jpg.
_MAP_XMIN = 7563.0
_MAP_XMAX = 25900.0
_MAP_YMIN = 7800.0
_MAP_YMAX = 25600.0

# Fountain world positions, used to classify a point's map half.
_RADIANT_FOUNTAIN = (9684.0, 9684.0)
_DIRE_FOUNTAIN = (23120.0, 22350.0)

# Half-width of the diagonal river strip, in world units.
_RIVER_STRIP = 1200.0


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
