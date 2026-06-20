"""Hero experience threshold catalog.

Reference: https://github.com/odota/dotaconstants
"""

from __future__ import annotations

from gem.catalog.resources import load_data_json

# list[int]: index = level, value = cumulative XP required to reach that level
XP_LEVEL: list[int] = load_data_json("xp_level.json")


def xp_to_next_level(level: int, current_xp: int) -> int | None:
    """Return XP needed to reach the next level, or None at max level.

    Args:
        level: Current hero level (1-based).
        current_xp: Current cumulative XP total.

    Returns:
        XP remaining to next level, or ``None`` if already at max.
    """
    if level < len(XP_LEVEL):
        return max(0, XP_LEVEL[level] - current_xp)
    return None
