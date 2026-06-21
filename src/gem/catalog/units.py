"""Unit (NPC) classification lookups for kill categorization.

Classifies combat-log ``target_name`` values into the categories OpenDota
reports per player (ancient/neutral/lane/courier/ward/roshan/necronomicon),
used to derive the specialty kill scalars from a player's ``kills_log``.

Reference: https://github.com/odota/dotaconstants (ancients.json) and
odota/core's per-player kill categorization.
"""

from __future__ import annotations

from gem.catalog.resources import load_data_json

# ancient-neutral npc name -> 1 (truthy). e.g. "npc_dota_neutral_black_drake".
ANCIENTS: dict[str, int] = load_data_json("ancients.json")

_NEUTRAL_PREFIX = "npc_dota_neutral_"
_LANE_CREEP_PREFIX = "npc_dota_creep_"
_COURIER_NAMES = frozenset({"npc_dota_courier"})
_OBSERVER_NAMES = frozenset({"npc_dota_observer_wards", "npc_dota_ward_base_truesight"})
_SENTRY_NAMES = frozenset({"npc_dota_sentry_wards", "npc_dota_ward_base"})
_ROSHAN_NAME = "npc_dota_roshan"


def is_ancient(npc_name: str) -> bool:
    """Return True if the NPC is an ancient neutral creep.

    Args:
        npc_name: Combat-log ``target_name``, e.g. ``"npc_dota_neutral_black_drake"``.

    Returns:
        True if the name is a known ancient neutral.
    """
    return npc_name in ANCIENTS


def is_neutral(npc_name: str) -> bool:
    """Return True if the NPC is a neutral creep (ancient or regular).

    Args:
        npc_name: Combat-log ``target_name``.

    Returns:
        True if the name starts with the neutral prefix.
    """
    return npc_name.startswith(_NEUTRAL_PREFIX)


def is_lane_creep(npc_name: str) -> bool:
    """Return True if the NPC is a lane creep (melee/ranged/siege/flagbearer).

    Args:
        npc_name: Combat-log ``target_name``.

    Returns:
        True if the name starts with the lane-creep prefix.
    """
    return npc_name.startswith(_LANE_CREEP_PREFIX)


def is_courier(npc_name: str) -> bool:
    """Return True if the NPC is a courier.

    Args:
        npc_name: Combat-log ``target_name``.

    Returns:
        True if the name is a courier unit.
    """
    return npc_name in _COURIER_NAMES


def is_observer_ward(npc_name: str) -> bool:
    """Return True if the NPC is an observer ward.

    Args:
        npc_name: Combat-log ``target_name``.

    Returns:
        True if the name is an observer ward.
    """
    return npc_name in _OBSERVER_NAMES


def is_sentry_ward(npc_name: str) -> bool:
    """Return True if the NPC is a sentry ward.

    Args:
        npc_name: Combat-log ``target_name``.

    Returns:
        True if the name is a sentry ward.
    """
    return npc_name in _SENTRY_NAMES


def is_roshan(npc_name: str) -> bool:
    """Return True if the NPC is Roshan.

    Args:
        npc_name: Combat-log ``target_name``.

    Returns:
        True if the name is Roshan.
    """
    return npc_name == _ROSHAN_NAME
