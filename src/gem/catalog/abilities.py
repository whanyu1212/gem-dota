"""Ability catalog lookups backed by bundled dotaconstants data.

Reference: https://github.com/odota/dotaconstants
"""

from __future__ import annotations

from gem.catalog.heroes import HEROES
from gem.catalog.items import item_display
from gem.catalog.resources import load_data_json

# internal_ability_name -> display_name str
ABILITIES: dict[str, str] = load_data_json("abilities.json")

# Known hero NPC name prefixes to strip when prettifying unknown ability names.
_HERO_PREFIXES: frozenset[str] = frozenset(HEROES)


def _prettify_ability(internal: str) -> str:
    """Best-effort prettify for ability names not found in ABILITIES.

    Strips the hero name prefix (e.g. ``arc_warden_``) and title-cases the
    remainder so ``arc_warden_scepter`` -> ``"Scepter"`` and
    ``ability_lamp_use`` -> ``"Lamp Use"``.

    Args:
        internal: Raw internal ability name.

    Returns:
        Prettified display string.
    """
    name = internal
    if name.startswith("ability_"):
        name = name[len("ability_") :]
    else:
        for hero_npc in _HERO_PREFIXES:
            short = hero_npc.replace("npc_dota_hero_", "") + "_"
            if name.startswith(short):
                name = name[len(short) :]
                break
    return name.replace("_", " ").title()


def ability_display(internal: str) -> str:
    """Return display name for an ability or item internal name.

    Falls back to ``item_display`` for ``item_*`` names, and to a
    prettified version of the internal name for any unrecognised ability.

    Args:
        internal: Internal ability or item name.

    Returns:
        Display name string.
    """
    dname = ABILITIES.get(internal)
    if dname:
        return dname
    if internal.startswith("item_"):
        return item_display(internal)
    return _prettify_ability(internal)
