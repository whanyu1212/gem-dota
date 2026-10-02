"""Shared constants and helpers for the analysis package.

Centralises the map-geometry constants and the small lookup helpers that were
previously duplicated across :mod:`gem.analysis.roshan`,
:mod:`gem.analysis.map_context`, and :mod:`gem.reports._sections`.
"""

from __future__ import annotations

import bisect
import math
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gem.results.models import ParsedMatch

# Team numbers (Dota convention).
_TEAM_RADIANT = 2
_TEAM_DIRE = 3

# Map geometry is sourced from the bundled ``map_constants.json`` so there is a
# single source of truth — the same file the public ``catalog.load_map_constants``
# exposes. The literals below are a calibrated fallback used only if the JSON is
# missing or malformed (they must mirror the JSON). These are analysis constants
# (territory grid, in-map checks, fountain anchors), not the report's image
# projection, which gem.reports._formatting calibrates separately. The fountains
# are the CDOTA_Unit_Fountain entity positions, identical on every local fixture.
_FALLBACK_MAP_BOUNDS = (7563.0, 25900.0, 7800.0, 25600.0)  # xmin, xmax, ymin, ymax
_FALLBACK_RADIANT_FOUNTAIN = (8928.0, 9446.0)
_FALLBACK_DIRE_FOUNTAIN = (23792.0, 23232.0)

#: Every label ``region_of`` can return.
MAP_REGIONS = ("river", "radiant_half", "dire_half", "top_lotus", "bottom_lotus")

Point = tuple[float, float]


def _load_map_geometry() -> tuple[float, float, float, float, Point, Point]:
    """Load map bounds and fountains from ``map_constants.json``.

    Falls back to the calibrated literals if the JSON is unavailable or missing
    keys, so importing the analysis package never fails on a data problem.

    Returns:
        ``(xmin, xmax, ymin, ymax, radiant_fountain, dire_fountain)``.
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
        )
    except (OSError, ValueError, KeyError, TypeError):
        return (*_FALLBACK_MAP_BOUNDS, _FALLBACK_RADIANT_FOUNTAIN, _FALLBACK_DIRE_FOUNTAIN)


(
    _MAP_XMIN,
    _MAP_XMAX,
    _MAP_YMIN,
    _MAP_YMAX,
    _RADIANT_FOUNTAIN,
    _DIRE_FOUNTAIN,
) = _load_map_geometry()


@dataclass(frozen=True)
class _RegionGeometry:
    river_outline: tuple[Point, ...]
    radiant_half: tuple[Point, ...]
    lotus_pools: tuple[tuple[str, Point], ...]
    lotus_radius: float


# Far enough past the map that closing the Radiant half there never cuts it.
_FAR = 1.0e7


def _load_region_geometry() -> _RegionGeometry | None:
    """Load the river outline, half line and lotus pools from ``map_constants.json``.

    The Radiant half is the half line closed around the Radiant corner: its ends
    run on flat to ``_FAR`` and down to ``-_FAR``.

    Returns:
        The region geometry, or ``None`` if the JSON is unavailable or malformed.
        ``region_of`` then falls back to the fountains' bisector with no river or
        lotus areas. The outline is too long to mirror as a literal.
    """
    try:
        from gem.catalog.map import load_map_constants

        regions = load_map_constants()["regions"]
        outline = tuple((float(x), float(y)) for x, y in regions["river_outline"])
        line = [(float(x), float(y)) for x, y in regions["half_line"]]
        lotus = tuple(
            (str(name), (float(pos["x"]), float(pos["y"])))
            for name, pos in regions["lotus_pools"].items()
        )
        radius = float(regions["lotus_radius"])
    except (OSError, ValueError, KeyError, TypeError):
        return None
    if len(outline) < 3 or len(line) < 2:
        return None
    first_y, last_y = line[0][1], line[-1][1]
    radiant_half = (*line, (_FAR, last_y), (_FAR, -_FAR), (-_FAR, -_FAR), (-_FAR, first_y))
    return _RegionGeometry(outline, radiant_half, lotus, radius)


_REGIONS = _load_region_geometry()


def _in_polygon(x: float, y: float, polygon: tuple[Point, ...]) -> bool:
    # Even-odd ray cast towards +x.
    inside = False
    x1, y1 = polygon[-1]
    for x2, y2 in polygon:
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            inside = not inside
        x1, y1 = x2, y2
    return inside


def infer_match_end_tick(match: ParsedMatch) -> int:
    """Return the match end tick, falling back to the last observed sample.

    Prefers ``match.post_game_tick`` (the Ancient destroyed), then
    ``match.game_end_tick`` (the end of the recording, which can run long past
    the match), and otherwise the latest tick seen across player time-series and
    position logs.

    Args:
        match: The parsed match.

    Returns:
        The end tick (``0`` if no data is available).
    """
    if match.post_game_tick is not None and match.post_game_tick > 0:
        return match.post_game_tick
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
    """Classify a world position into a map region.

    The regions come from ``map_constants.json`` (``regions``), traced on the
    7.41 map:

    - ``"top_lotus"`` / ``"bottom_lotus"``: within ``lotus_radius`` of a lotus
      pool. Both teams contest these from their lanes, so they belong to neither
      half.
    - ``"river"``: inside the river's outline, which runs from the top-lane
      crossing to the bottom-lane crossing and includes both Roshan pools. The
      lanes themselves are not river.
    - ``"radiant_half"`` / ``"dire_half"``: the side of the half line, which runs
      along the river's middle and, past its ends, straight out to the map edges.

    Args:
        x: World x coordinate.
        y: World y coordinate.

    Returns:
        One of :data:`MAP_REGIONS`.
    """
    geometry = _REGIONS
    if geometry is None:
        dr = math.dist((x, y), _RADIANT_FOUNTAIN)
        dd = math.dist((x, y), _DIRE_FOUNTAIN)
        return "radiant_half" if dr <= dd else "dire_half"
    for name, centre in geometry.lotus_pools:
        if math.dist((x, y), centre) <= geometry.lotus_radius:
            return name
    if _in_polygon(x, y, geometry.river_outline):
        return "river"
    return "radiant_half" if _in_polygon(x, y, geometry.radiant_half) else "dire_half"


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
