"""Unit tests for gem.catalog resource-backed lookup helpers."""

from __future__ import annotations

from importlib.resources import files

import gem
import gem.catalog as catalog
import gem.constants as constants


def test_catalog_exposed_from_top_level_package() -> None:
    assert hasattr(gem, "catalog")
    assert "catalog" in gem.__all__
    assert gem.catalog.hero_display("npc_dota_hero_axe") == "Axe"


def test_catalog_lookups_match_constants_facade() -> None:
    assert catalog.hero_display("npc_dota_hero_antimage") == constants.hero_display(
        "npc_dota_hero_antimage"
    )
    assert catalog.item_display("item_blink") == constants.item_display("item_blink")
    assert catalog.ability_display("axe_berserkers_call") == constants.ability_display(
        "axe_berserkers_call"
    )
    assert catalog.item_key_by_id(1861) == constants.item_key_by_id(1861)
    assert catalog.xp_to_next_level(1, 0) == constants.xp_to_next_level(1, 0)


def test_catalog_resolves_internal_hero_suffixes() -> None:
    assert catalog.hero_npc_name("antimage") == "npc_dota_hero_antimage"
    assert catalog.hero_npc_name("queenofpain") == "npc_dota_hero_queenofpain"
    assert catalog.hero_npc_name("nevermore") == "npc_dota_hero_nevermore"


def test_hero_id_resolves_numeric_id() -> None:
    assert catalog.hero_id("npc_dota_hero_antimage") == 1
    assert catalog.hero_id("npc_dota_hero_broodmother") == 61
    assert catalog.hero_id("NPC_DOTA_HERO_AXE") == 2  # case-insensitive
    assert catalog.hero_id("npc_dota_hero_not_a_hero") == 0  # unknown -> 0
    assert "hero_id" in gem.catalog.__all__


def test_item_display_unknown_falls_back_to_raw_name() -> None:
    # Unknown items return the raw string rather than raising.
    assert catalog.item_display("item_not_a_real_item") == "item_not_a_real_item"
    assert catalog.item_display("totally_unknown") == "totally_unknown"


def test_item_display_missing_dname_falls_back(monkeypatch) -> None:
    # A catalog row without a "dname" key must not raise KeyError.
    from gem.catalog import items as items_mod

    monkeypatch.setitem(items_mod.ITEMS, "_malformed", {"id": 99999})
    assert catalog.item_display("item__malformed") == "item__malformed"


def test_catalog_loads_core_json_resources() -> None:
    heroes = catalog.load_data_json("heroes.json")
    assert heroes["npc_dota_hero_axe"]["localized_name"] == "Axe"
    assert files("gem.data").joinpath("heroes.json").is_file()


def test_map_catalog_loads_neutral_camp_centers() -> None:
    centers = catalog.load_neutral_camp_centers()
    assert centers
    assert all(isinstance(camp_id, int) for camp_id in centers)
    assert all(len(center) == 2 for center in centers.values())
