"""Item and permanent-buff catalog lookups.

Reference: https://github.com/odota/dotaconstants
"""

from __future__ import annotations

from typing import Any

from gem.catalog.resources import load_data_json

# internal_key (without item_ prefix) -> {id, dname}
ITEMS: dict[str, dict[str, Any]] = load_data_json("items.json")
_ITEM_KEYS_BY_ID: dict[int, str] = {}
for _key, _item in ITEMS.items():
    _item_id = _item.get("id")
    if isinstance(_item_id, int):
        _ITEM_KEYS_BY_ID[_item_id] = _key

# int_str -> internal_item_name, e.g. "1" -> "moon_shard"
PERMANENT_BUFFS: dict[str, str] = load_data_json("permanent_buffs.json")


def item_display(internal: str) -> str:
    """Return display name for an ``item_*`` prefixed internal name.

    Args:
        internal: Internal item name, e.g. ``"item_blink"`` or ``"blink"``.

    Returns:
        Display name (e.g. ``"Blink Dagger"``), or the raw string as fallback.
    """
    key = internal.removeprefix("item_")
    item = ITEMS.get(key)
    return str(item["dname"]) if item else internal


def item_key_by_id(item_id: int) -> str | None:
    """Return the internal item key for an item ability ID.

    Args:
        item_id: Numeric item ability ID from replay messages.

    Returns:
        Internal item key without the ``item_`` prefix, or ``None`` when unknown.
    """
    return _ITEM_KEYS_BY_ID.get(item_id)


def permanent_buff_name(buff_id: int) -> str:
    """Return the item name for a permanent buff integer ID.

    Args:
        buff_id: Integer buff identifier from entity state.

    Returns:
        Internal item name (e.g. ``"moon_shard"``), or ``str(buff_id)`` as fallback.
    """
    return PERMANENT_BUFFS.get(str(buff_id), str(buff_id))
