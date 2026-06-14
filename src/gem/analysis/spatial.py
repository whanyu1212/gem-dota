"""Spatial and time-series helpers for parsed match analysis."""

from __future__ import annotations

import bisect
import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gem.results.models import ParsedMatch, ParsedPlayer


def position_at_tick(
    player: ParsedPlayer,
    tick: int,
) -> tuple[float, float] | None:
    """Return the closest recorded (x, y) position for a player at a given tick.

    Searches ``player.position_log`` (a list of ``(tick, x, y)`` tuples
    sampled at ~1-second intervals) for the entry with the smallest tick
    distance to the requested tick.

    Args:
        player: A ``ParsedPlayer`` with a populated ``position_log``.
        tick: The game tick to query.

    Returns:
        ``(x, y)`` world coordinates of the nearest sample, or ``None`` if
        ``position_log`` is empty.

    Example:
        >>> pos = position_at_tick(axe_player, fight.start_tick)
        >>> if pos:
        ...     print(f"Axe was at ({pos[0]:.0f}, {pos[1]:.0f}) when the fight started")
    """
    log = player.position_log
    if not log:
        return None

    ticks = [entry[0] for entry in log]
    idx = bisect.bisect_left(ticks, tick)

    if idx == 0:
        return (log[0][1], log[0][2])
    if idx >= len(log):
        return (log[-1][1], log[-1][2])

    before = log[idx - 1]
    after = log[idx]
    # Pick whichever sample is closer in tick distance
    if tick - before[0] <= after[0] - tick:
        return (before[1], before[2])
    return (after[1], after[2])


def heroes_near(
    match: ParsedMatch,
    tick: int,
    x: float,
    y: float,
    radius: float,
) -> list[ParsedPlayer]:
    """Return all heroes within ``radius`` world units of ``(x, y)`` at ``tick``.

    Uses ``position_at_tick`` to estimate each hero's position at the requested
    tick from their ``position_log`` samples.  Heroes with no position data are
    excluded.

    Args:
        match: A parsed replay with ``players`` populated.
        tick: Game tick to query.
        x: World x coordinate of the centre point.
        y: World y coordinate of the centre point.
        radius: Search radius in world units.

    Returns:
        List of ``ParsedPlayer`` objects whose estimated position at ``tick``
        is within ``radius`` of ``(x, y)``, in ascending distance order.

    Example:
        >>> nearby = heroes_near(match, fight.start_tick,
        ...                      fight.centroid_x, fight.centroid_y, 2000)
        >>> print(f"{len(nearby)} heroes near fight start")
    """
    results: list[tuple[float, ParsedPlayer]] = []
    for player in match.players:
        pos = position_at_tick(player, tick)
        if pos is None:
            continue
        dist = math.dist(pos, (x, y))
        if dist <= radius:
            results.append((dist, player))
    results.sort(key=lambda t: t[0])
    return [p for _, p in results]


def net_worth_at(player: ParsedPlayer, tick: int) -> int:
    """Return the closest sampled net worth for a player at the given tick.

    Net worth is sampled at ~1-second intervals by the ``PlayerExtractor``
    and stored in parallel arrays ``player.times`` / ``player.net_worth_t``.
    This function finds the sample with the smallest tick distance to the
    requested tick via a linear scan.

    Args:
        player: A ``ParsedPlayer`` with ``times`` and ``net_worth_t`` populated.
        tick: The game tick to query.

    Returns:
        Net worth in gold at the nearest sample, or 0 if no data is available.

    Example:
        >>> nw = net_worth_at(player, fight.start_tick)
        >>> print(f"{player.hero_name} had {nw} net worth at fight start")
    """
    if not player.times or not player.net_worth_t:
        return 0
    best_idx = min(range(len(player.times)), key=lambda i: abs(player.times[i] - tick))
    return player.net_worth_t[best_idx]
