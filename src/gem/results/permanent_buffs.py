"""OpenDota-compatible flags derived from Game Coordinator permanent buffs."""

from __future__ import annotations

from collections.abc import Iterable

# OpenDota derives these top-level player flags directly from permanent_buffs.
PERMANENT_BUFF_FLAG_IDS: dict[str, int] = {
    "aghanims_scepter": 2,
    "aghanims_shard": 12,
    "moonshard": 1,
}


def permanent_buff_flags(buff_ids: Iterable[int]) -> dict[str, int]:
    """Return OpenDota's three consumed-upgrade flags for permanent buff IDs.

    Args:
        buff_ids: Permanent-buff identifiers from a Game Coordinator player
            summary or API response.

    Returns:
        Mapping of OpenDota player field names to exact ``0`` or ``1`` values.
    """
    present = set(buff_ids)
    return {
        field_name: int(buff_id in present)
        for field_name, buff_id in PERMANENT_BUFF_FLAG_IDS.items()
    }
