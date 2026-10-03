"""Shared constants and helpers for the analysis package.

Holds the team constants, the fountain positions ``region_of`` falls back on,
and the small lookup helpers several analysis modules share.
"""

from __future__ import annotations

import bisect
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gem.results.models import ParsedMatch

# Team numbers (Dota convention).
_TEAM_RADIANT = 2
_TEAM_DIRE = 3

# The fountains come from the bundled ``map_constants.json`` (the same file
# ``catalog.load_map_constants`` exposes); the literals are a fallback used only
# if the JSON is missing or malformed, and must mirror it. They are the
# CDOTA_Unit_Fountain entity positions, identical on every local fixture.
_FALLBACK_RADIANT_FOUNTAIN = (8928.0, 9446.0)
_FALLBACK_DIRE_FOUNTAIN = (23792.0, 23232.0)


def _load_fountains() -> tuple[tuple[float, float], tuple[float, float]]:
    """Load the fountain positions from ``map_constants.json``.

    Falls back to the literals above if the JSON is unavailable or missing
    keys, so importing the analysis package never fails on a data problem.

    Returns:
        ``(radiant_fountain, dire_fountain)``.
    """
    try:
        from gem.catalog.map import load_map_constants

        fountains = load_map_constants()["fountains"]
        radiant, dire = fountains["radiant"], fountains["dire"]
        return (float(radiant["x"]), float(radiant["y"])), (float(dire["x"]), float(dire["y"]))
    except (OSError, ValueError, KeyError, TypeError):
        return _FALLBACK_RADIANT_FOUNTAIN, _FALLBACK_DIRE_FOUNTAIN


_RADIANT_FOUNTAIN, _DIRE_FOUNTAIN = _load_fountains()


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
