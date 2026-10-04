"""Catalog accessors for bundled Dota metadata and static map data.

The raw JSON assets live under :mod:`gem.data`; this package is the code-level
interface for loading and interpreting them. ``gem.constants`` remains as a
backwards-compatible facade for older imports.

Reference: https://github.com/odota/dotaconstants
"""

from __future__ import annotations

from gem.catalog.abilities import ABILITIES, ability_display
from gem.catalog.heroes import (
    HEROES,
    hero_display,
    hero_id,
    hero_meta,
    hero_npc_name,
    hero_short,
)
from gem.catalog.items import (
    ITEMS,
    PERMANENT_BUFFS,
    item_display,
    item_key_by_id,
    permanent_buff_name,
)
from gem.catalog.leagues import LEAGUES, league_name
from gem.catalog.map import (
    MAP_IMAGE_HEIGHT,
    MAP_IMAGE_WIDTH,
    MAP_XMAX,
    MAP_XMIN,
    MAP_YMAX,
    MAP_YMIN,
    load_camp_zones,
    load_map_constants,
    load_neutral_camp_centers,
    load_neutral_camps,
    map_image_to_world,
    world_to_map_image,
)
from gem.catalog.resources import load_data_json, load_data_text
from gem.catalog.xp import XP_LEVEL, xp_to_next_level

__all__ = [
    "ABILITIES",
    "HEROES",
    "ITEMS",
    "LEAGUES",
    "MAP_IMAGE_HEIGHT",
    "MAP_IMAGE_WIDTH",
    "MAP_XMAX",
    "MAP_XMIN",
    "MAP_YMAX",
    "MAP_YMIN",
    "PERMANENT_BUFFS",
    "XP_LEVEL",
    "ability_display",
    "hero_display",
    "hero_id",
    "hero_meta",
    "hero_npc_name",
    "hero_short",
    "item_display",
    "item_key_by_id",
    "league_name",
    "load_camp_zones",
    "load_data_json",
    "load_data_text",
    "load_map_constants",
    "load_neutral_camp_centers",
    "load_neutral_camps",
    "map_image_to_world",
    "permanent_buff_name",
    "world_to_map_image",
    "xp_to_next_level",
]
