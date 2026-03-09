"""Dota 2 game constants — heroes, items, abilities, XP thresholds.

Data is bundled from odota/dotaconstants and pre-processed by
``scripts/build_constants.py`` into ``src/gem/data/``.

All public functions accept internal game names and return human-readable
display strings, falling back gracefully when a name is not found.

Reference: https://github.com/odota/dotaconstants
"""

from __future__ import annotations

import json
from importlib.resources import files
from typing import Any

# ---------------------------------------------------------------------------
# Data loading — once at import time
# ---------------------------------------------------------------------------


def _load(name: str) -> Any:
    data = files("gem.data").joinpath(name).read_text(encoding="utf-8")
    return json.loads(data)


# npc_dota_hero_* (lowercase) -> {id, localized_name, primary_attr, roles}
HEROES: dict[str, dict] = _load("heroes.json")

# internal_key (without item_ prefix) -> {id, dname}
ITEMS: dict[str, dict] = _load("items.json")

# internal_ability_name -> display_name str
ABILITIES: dict[str, str] = _load("abilities.json")

# list[int]: index = level, value = cumulative XP required to reach that level
XP_LEVEL: list[int] = _load("xp_level.json")

# int_str -> internal_item_name, e.g. "1" -> "moon_shard"
PERMANENT_BUFFS: dict[str, str] = _load("permanent_buffs.json")


# ---------------------------------------------------------------------------
# Hero lookups
# ---------------------------------------------------------------------------


def hero_display(npc_name: str) -> str:
    """Return the localized display name for an ``npc_dota_hero_*`` string.

    Args:
        npc_name: Internal hero name, e.g. ``"npc_dota_hero_axe"``.

    Returns:
        Localized name (e.g. ``"Axe"``), or a cleaned-up fallback.
    """
    hero = HEROES.get(npc_name.lower())
    if hero:
        return hero.get("localized_name") or npc_name
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


def hero_meta(npc_name: str) -> dict:
    """Return the full hero metadata dict, or an empty dict if not found.

    Args:
        npc_name: Internal hero name (case-insensitive).

    Returns:
        Dict with keys ``id``, ``localized_name``, ``primary_attr``, ``roles``.
    """
    return HEROES.get(npc_name.lower(), {})


# ---------------------------------------------------------------------------
# Item lookups
# ---------------------------------------------------------------------------


def item_display(internal: str) -> str:
    """Return display name for an ``item_*`` prefixed internal name.

    Args:
        internal: Internal item name, e.g. ``"item_blink"`` or ``"blink"``.

    Returns:
        Display name (e.g. ``"Blink Dagger"``), or the raw string as fallback.
    """
    key = internal.removeprefix("item_")
    item = ITEMS.get(key)
    return item["dname"] if item else internal


# ---------------------------------------------------------------------------
# Ability lookups
# ---------------------------------------------------------------------------


def ability_display(internal: str) -> str:
    """Return display name for an ability or item internal name.

    Falls back to ``item_display`` for ``item_*`` names not found in abilities.

    Args:
        internal: Internal ability or item name.

    Returns:
        Display name, or the raw string as fallback.
    """
    dname = ABILITIES.get(internal)
    if dname:
        return dname
    if internal.startswith("item_"):
        return item_display(internal)
    return internal


# ---------------------------------------------------------------------------
# XP helpers
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Permanent buff helpers
# ---------------------------------------------------------------------------


def permanent_buff_name(buff_id: int) -> str:
    """Return the item name for a permanent buff integer ID.

    Args:
        buff_id: Integer buff identifier from entity state.

    Returns:
        Internal item name (e.g. ``"moon_shard"``), or ``str(buff_id)`` as fallback.
    """
    return PERMANENT_BUFFS.get(str(buff_id), str(buff_id))
