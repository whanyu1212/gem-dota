"""Shared helpers used by more than one report section module.

Split out of the former monolithic ``_sections.py`` (see that module's
shim for backward-compatible re-exports).
"""

from __future__ import annotations

from gem.reports._formatting import TICKS_PER_SEC, game_clock
from gem.results.models import ParsedMatch

_RADIANT_COLORS = ["#4caf50", "#81c784", "#a5d6a7", "#2e7d32", "#66bb6a"]


_DIRE_COLORS = ["#f44336", "#ff7043", "#ef9a9a", "#b71c1c", "#ff8a65"]


def fight_numbers(match: ParsedMatch) -> dict[int, int]:
    """Map each fight object's ``id()`` to its 1-based number in the Fights tab."""
    return {id(fight): number for number, fight in enumerate(match.fights or [], start=1)}


def game_seconds_between(start_tick: int, end_tick: int) -> str:
    """Format the in-game time from one tick to another as ``+Ns``.

    The game clock stops during pauses, so this is pause-aware. When the clock is
    unavailable the raw tick gap is used and marked with ``*``.
    """
    clock = game_clock()
    start_s = clock.game_time_at(start_tick)
    end_s = clock.game_time_at(end_tick)
    if start_s is not None and end_s is not None:
        return f"{end_s - start_s:+.0f}s"
    return f"{(end_tick - start_tick) / TICKS_PER_SEC:+.0f}s*"


def fight_outcome(winner: str) -> str:
    """Label a fight's ``winner`` field: "Radiant won", "Dire won", "Even", or "No winner"."""
    if winner in ("radiant", "dire"):
        return f"{winner.title()} won"
    # "draw" is equal kills; "unknown" means the teams could not be resolved.
    return "Even" if winner == "draw" else "No winner"
