"""Ability-level lookup helpers."""

from __future__ import annotations

import bisect
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gem.results.models import ParsedPlayer


def ability_level_at_tick(
    player: ParsedPlayer,
    ability: str,
    tick: int,
) -> int:
    """Return the level of an ability for a player at a given tick.

    Searches ``player.position_log``-aligned snapshots indirectly via the
    per-minute ability level data stored in ``ParsedPlayer``.  Since full
    per-tick ability level snapshots are not stored, this uses the nearest
    minute-boundary snapshot whose tick is ``≤ tick`` (last known level at or
    before the requested tick).

    Ability names match the ``inflictor_name`` field in the combat log (e.g.
    ``"axe_berserkers_call"``).  Returns 0 if the ability is not yet learned
    at the given tick.

    Args:
        player: A ``ParsedPlayer`` with ``_ability_snapshots`` populated, or
            accessed via the ``ability_levels_at`` helper that uses
            ``times_min`` parallel arrays.  In practice, call
            ``ability_level_at_tick`` with the ``ParsedPlayer`` and ability
            name — it returns the last-known level at or before ``tick``.
        ability: Ability name as it appears in the combat log
            (``inflictor_name``).
        tick: Game tick to query.

    Returns:
        Ability level (1–4 for most abilities, 0 if not yet learned).

    Example:
        >>> lvl = ability_level_at_tick(axe, "axe_berserkers_call", cast.tick)
        >>> print(f"Berserker's Call was level {lvl} when cast")
    """
    # ability_snapshots is a list of (tick, ability_levels_dict) sorted by tick,
    # built from the per-minute snapshots stored on ParsedPlayer._ability_snapshots.
    # Fall back gracefully if the attribute is missing (older parsed data).
    snapshots: list[tuple[int, dict[str, int]]] = getattr(player, "_ability_snapshots", [])
    if not snapshots:
        return 0

    snap_ticks = [s[0] for s in snapshots]
    idx = bisect.bisect_right(snap_ticks, tick) - 1
    if idx < 0:
        return 0
    return snapshots[idx][1].get(ability, 0)
