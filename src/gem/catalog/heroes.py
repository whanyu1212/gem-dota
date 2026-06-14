"""Hero catalog lookups backed by bundled dotaconstants data.

Reference: https://github.com/odota/dotaconstants
"""

from __future__ import annotations

from typing import Any

from gem.catalog.resources import load_data_json

# npc_dota_hero_* (lowercase) -> {id, localized_name, primary_attr, roles}
HEROES: dict[str, dict[str, Any]] = load_data_json("heroes.json")


def hero_display(npc_name: str) -> str:
    """Return the localized display name for an ``npc_dota_hero_*`` string.

    Args:
        npc_name: Internal hero name, e.g. ``"npc_dota_hero_axe"``.

    Returns:
        Localized name (e.g. ``"Axe"``), or a cleaned-up fallback.
    """
    hero = HEROES.get(npc_name.lower())
    if hero:
        return str(hero.get("localized_name") or npc_name)
    return npc_name.removeprefix("npc_dota_hero_").replace("_", " ").title()


def hero_short(npc_name: str) -> str:
    """Return display name from either a full ``npc_dota_hero_*`` or a bare suffix.

    Args:
        npc_name: Full internal name or bare suffix (e.g. ``"axe"``).

    Returns:
        Localized display name.
    """
    if npc_name.startswith("npc_dota_hero_"):
        return hero_display(npc_name)
    return hero_display("npc_dota_hero_" + npc_name)


def hero_npc_name(name: str) -> str | None:
    """Resolve a display name to its ``npc_dota_hero_*`` NPC name.

    Accepts common spelling variants: ``"Anti-Mage"``, ``"anti mage"``,
    ``"anti_mage"``, ``"antimage"`` all resolve to ``"npc_dota_hero_antimage"``.

    Args:
        name: Hero display name or NPC suffix.

    Returns:
        The ``npc_dota_hero_*`` key (lowercase), or ``None`` if not found.
    """
    if name.startswith("npc_dota_hero_"):
        return name.lower() if name.lower() in HEROES else None

    def _norm(s: str) -> str:
        return s.lower().replace("-", " ").replace("_", " ")

    normalised = _norm(name)
    for npc, data in HEROES.items():
        loc = _norm(str(data.get("localized_name") or ""))
        if loc == normalised:
            return npc
    return None


def hero_meta(npc_name: str) -> dict[str, Any]:
    """Return the full hero metadata dict, or an empty dict if not found.

    Args:
        npc_name: Internal hero name (case-insensitive).

    Returns:
        Dict with keys ``id``, ``localized_name``, ``primary_attr``, ``roles``.
    """
    return HEROES.get(npc_name.lower(), {})
