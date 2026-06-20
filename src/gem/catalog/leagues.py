"""League catalog lookups.

Reference: https://github.com/odota/dotaconstants
"""

from __future__ import annotations

from gem.catalog.resources import load_data_json

# leagueid (str) -> league name; premium/professional/amateur only
LEAGUES: dict[str, str] = load_data_json("leagues.json")


def league_name(leagueid: int) -> str | None:
    """Return the league name for a given league ID, or None if unknown/not found.

    Args:
        leagueid: Numeric Dota 2 league ID.

    Returns:
        League name string (e.g. ``"The International 2024"``), or ``None``
        if the league is not in the bundled data.
    """
    if not leagueid:
        return None
    return LEAGUES.get(str(leagueid))
