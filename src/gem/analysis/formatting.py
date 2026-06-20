"""Formatting helpers for parsed Dota names."""

from __future__ import annotations


def format_npc_name(name: str) -> str:
    """Convert an NPC name to a human-readable label.

    Strips Dota 2 NPC name prefixes (``npc_dota_``, ``goodguys_``,
    ``badguys_``) and replaces underscores with spaces.  Intended for
    structures, neutrals, and other non-hero units.  For heroes, prefer
    ``gem.constants.hero_display()`` which returns the official display name.

    Args:
        name: An NPC name string (e.g. ``"npc_dota_goodguys_tower_top_1"``).

    Returns:
        A human-readable label (e.g. ``"tower top 1"``).

    Example:
        >>> format_npc_name("npc_dota_goodguys_tower_top_1")
        'tower top 1'
        >>> format_npc_name("npc_dota_neutral_ogre_mauler")
        'neutral ogre mauler'
    """
    return (
        name.replace("npc_dota_", "")
        .replace("goodguys_", "")
        .replace("badguys_", "")
        .replace("_", " ")
    )
