"""Backward-compatible facade for Dota catalog lookups.

New code should prefer :mod:`gem.catalog`, which groups bundled hero, item,
ability, league, XP, and static map metadata by concern. This module preserves
the older ``gem.constants`` API.

Reference: https://github.com/odota/dotaconstants
"""

from __future__ import annotations

from typing import Any

from gem.catalog.abilities import ABILITIES
from gem.catalog.abilities import ability_display as _ability_display
from gem.catalog.heroes import (
    HEROES,
)
from gem.catalog.heroes import (
    hero_display as _hero_display,
)
from gem.catalog.heroes import (
    hero_meta as _hero_meta,
)
from gem.catalog.heroes import (
    hero_npc_name as _hero_npc_name,
)
from gem.catalog.heroes import (
    hero_short as _hero_short,
)
from gem.catalog.items import (
    ITEMS,
    PERMANENT_BUFFS,
)
from gem.catalog.items import (
    item_display as _item_display,
)
from gem.catalog.items import (
    item_key_by_id as _item_key_by_id,
)
from gem.catalog.items import (
    permanent_buff_name as _permanent_buff_name,
)
from gem.catalog.leagues import LEAGUES
from gem.catalog.leagues import league_name as _league_name
from gem.catalog.xp import XP_LEVEL
from gem.catalog.xp import xp_to_next_level as _xp_to_next_level

__all__ = [
    "ABILITIES",
    "HEROES",
    "ITEMS",
    "LEAGUES",
    "PERMANENT_BUFFS",
    "XP_LEVEL",
    "ability_display",
    "hero_display",
    "hero_meta",
    "hero_npc_name",
    "hero_short",
    "item_display",
    "item_key_by_id",
    "league_name",
    "permanent_buff_name",
    "xp_to_next_level",
]


def hero_display(npc_name: str) -> str:
    """Return the localized display name for an ``npc_dota_hero_*`` string.

    Args:
        npc_name: Internal hero name, e.g. ``"npc_dota_hero_axe"``.

    Returns:
        Localized name (e.g. ``"Axe"``), or a cleaned-up fallback.
    """
    return _hero_display(npc_name)


def hero_short(npc_name: str) -> str:
    """Return display name from either a full ``npc_dota_hero_*`` or a bare suffix.

    Args:
        npc_name: Full internal name or bare suffix (e.g. ``"axe"``).

    Returns:
        Localized display name.
    """
    return _hero_short(npc_name)


def hero_npc_name(name: str) -> str | None:
    """Resolve a display name to its ``npc_dota_hero_*`` NPC name.

    Args:
        name: Hero display name or NPC suffix.

    Returns:
        The ``npc_dota_hero_*`` key (lowercase), or ``None`` if not found.
    """
    return _hero_npc_name(name)


def hero_meta(npc_name: str) -> dict[str, Any]:
    """Return the full hero metadata dict, or an empty dict if not found.

    Args:
        npc_name: Internal hero name (case-insensitive).

    Returns:
        Dict with keys ``id``, ``localized_name``, ``primary_attr``, ``roles``.
    """
    return _hero_meta(npc_name)


def item_display(internal: str) -> str:
    """Return display name for an ``item_*`` prefixed internal name.

    Args:
        internal: Internal item name, e.g. ``"item_blink"`` or ``"blink"``.

    Returns:
        Display name (e.g. ``"Blink Dagger"``), or the raw string as fallback.
    """
    return _item_display(internal)


def item_key_by_id(item_id: int) -> str | None:
    """Return the internal item key for an item ability ID.

    Args:
        item_id: Numeric item ability ID from replay messages.

    Returns:
        Internal item key without the ``item_`` prefix, or ``None`` when unknown.
    """
    return _item_key_by_id(item_id)


def ability_display(internal: str) -> str:
    """Return display name for an ability or item internal name.

    Args:
        internal: Internal ability or item name.

    Returns:
        Display name string.
    """
    return _ability_display(internal)


def xp_to_next_level(level: int, current_xp: int) -> int | None:
    """Return XP needed to reach the next level, or None at max level.

    Args:
        level: Current hero level (1-based).
        current_xp: Current cumulative XP total.

    Returns:
        XP remaining to next level, or ``None`` if already at max.
    """
    return _xp_to_next_level(level, current_xp)


def permanent_buff_name(buff_id: int) -> str:
    """Return the item name for a permanent buff integer ID.

    Args:
        buff_id: Integer buff identifier from entity state.

    Returns:
        Internal item name (e.g. ``"moon_shard"``), or ``str(buff_id)`` as fallback.
    """
    return _permanent_buff_name(buff_id)


def league_name(leagueid: int) -> str | None:
    """Return the league name for a given league ID, or None if unknown/not found.

    Args:
        leagueid: Numeric Dota 2 league ID.

    Returns:
        League name string, or ``None`` if the league is not in the bundled data.
    """
    return _league_name(leagueid)
