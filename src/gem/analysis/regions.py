"""Map regions: which named area of the 7.41 map a world position is in.

``region_of`` is a fixed lookup, not a judgement. Its geometry lives in
``map_constants.json`` (``regions``): the river outline traced from the map image
(``scripts/trace_river_region.py``), the half line through the river, and the
lotus pools (``CDOTA_BaseNPC_LotusPool`` entity positions). The tests pin it to
replay entity positions: fountains, ancients, mid towers, power-rune spawners,
Roshan pits, lotus pools and the 28 camp spawners.

Reference: none of the pinned parsers (manta, clarity, odota/parser) defines map
regions; this is gem's own reference data, checked against replay 8974053011.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from gem.analysis._shared import _DIRE_FOUNTAIN, _RADIANT_FOUNTAIN

#: Every label ``region_of`` can return.
MAP_REGIONS = ("river", "radiant_half", "dire_half", "top_lotus", "bottom_lotus")

_Point = tuple[float, float]


@dataclass(frozen=True)
class _RegionGeometry:
    river_outline: tuple[_Point, ...]
    radiant_half: tuple[_Point, ...]
    lotus_pools: tuple[tuple[str, _Point], ...]
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


def _in_polygon(x: float, y: float, polygon: tuple[_Point, ...]) -> bool:
    # Even-odd ray cast towards +x.
    inside = False
    x1, y1 = polygon[-1]
    for x2, y2 in polygon:
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            inside = not inside
        x1, y1 = x2, y2
    return inside


def region_of(x: float, y: float) -> str:
    """Classify a world position into a map region.

    Public as ``gem.region_of``. A fixed lookup, not a judgement: the regions
    come from ``map_constants.json`` (``regions``), traced on the 7.41 map and
    checked against replay entities (fountains, ancients, mid towers, power-rune
    spawners, Roshan pits, lotus pools and camp spawners). They are checked in
    this order:

    - ``"top_lotus"`` / ``"bottom_lotus"``: within ``lotus_radius`` of a lotus
      pool. Both teams contest these from their lanes, so they belong to neither
      half.
    - ``"river"``: inside the river's outline, which runs from the top-lane
      crossing to the bottom-lane crossing and includes both Roshan pools. The
      lanes themselves are not river.
    - ``"radiant_half"`` / ``"dire_half"``: the side of the half line, which runs
      along the river's middle and, past its ends, straight out to the map edges.

    Without the geometry (a broken data file), every point falls in the half of
    the nearer fountain. Lanes, jungles and bases are not regions; for lanes use
    ``ParsedPlayer.lane`` (OpenDota's lane grid).

    Example:
        Share of each hero's sampled positions spent in the river::

            from collections import Counter
            for player in match.players:
                regions = Counter(gem.region_of(x, y) for _, x, y in player.position_log)
                print(player.hero_name, regions["river"] / max(regions.total(), 1))

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
