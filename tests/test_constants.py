"""Unit tests for gem.constants — hero/item/ability display helpers and data loading.

All tests are pure unit tests and exercise the public API of constants.py against
the bundled data files in src/gem/data/.  No replay fixtures are required.
"""

from __future__ import annotations

import pytest

import gem.constants as C

# ---------------------------------------------------------------------------
# Data loading sanity checks
# ---------------------------------------------------------------------------


class TestDataLoading:
    """Verify that the bundled data files loaded correctly and are non-empty."""

    def test_heroes_is_nonempty_dict(self) -> None:
        assert isinstance(C.HEROES, dict)
        assert len(C.HEROES) > 0

    def test_items_is_nonempty_dict(self) -> None:
        assert isinstance(C.ITEMS, dict)
        assert len(C.ITEMS) > 0

    def test_abilities_is_nonempty_dict(self) -> None:
        assert isinstance(C.ABILITIES, dict)
        assert len(C.ABILITIES) > 0

    def test_xp_level_is_nonempty_list(self) -> None:
        assert isinstance(C.XP_LEVEL, list)
        assert len(C.XP_LEVEL) > 0

    def test_permanent_buffs_is_nonempty_dict(self) -> None:
        assert isinstance(C.PERMANENT_BUFFS, dict)
        assert len(C.PERMANENT_BUFFS) > 0

    def test_leagues_is_nonempty_dict(self) -> None:
        assert isinstance(C.LEAGUES, dict)
        assert len(C.LEAGUES) > 0

    def test_heroes_entries_have_expected_keys(self) -> None:
        # Every entry should have these four fields from build_constants.py
        sample_hero = C.HEROES["npc_dota_hero_axe"]
        assert "id" in sample_hero
        assert "localized_name" in sample_hero
        assert "primary_attr" in sample_hero
        assert "roles" in sample_hero

    def test_items_entries_have_expected_keys(self) -> None:
        sample_item = C.ITEMS["blink"]
        assert "id" in sample_item
        assert "dname" in sample_item

    def test_xp_level_first_element_is_zero(self) -> None:
        # Level 1 requires 0 XP (already at threshold)
        assert C.XP_LEVEL[0] == 0

    def test_xp_level_values_are_increasing(self) -> None:
        for i in range(1, len(C.XP_LEVEL)):
            assert C.XP_LEVEL[i] > C.XP_LEVEL[i - 1], (
                f"XP threshold at index {i} is not greater than index {i - 1}"
            )


# ---------------------------------------------------------------------------
# hero_display()
# ---------------------------------------------------------------------------


class TestHeroDisplay:
    """Tests for gem.constants.hero_display()."""

    def test_known_hero_returns_localized_name(self) -> None:
        assert C.hero_display("npc_dota_hero_axe") == "Axe"

    def test_known_hero_pudge_returns_localized_name(self) -> None:
        assert C.hero_display("npc_dota_hero_pudge") == "Pudge"

    def test_known_hero_anti_mage_returns_localized_name(self) -> None:
        # localized name includes a hyphen
        assert C.hero_display("npc_dota_hero_antimage") == "Anti-Mage"

    def test_known_hero_case_insensitive(self) -> None:
        # hero_display calls .lower() on the key
        assert C.hero_display("NPC_DOTA_HERO_AXE") == "Axe"

    def test_unknown_hero_falls_back_to_titlecase_slug(self) -> None:
        # Strip npc_dota_hero_ prefix, replace _ with space, titlecase
        result = C.hero_display("npc_dota_hero_totally_fake_hero")
        assert result == "Totally Fake Hero"

    def test_unknown_hero_no_prefix_falls_back_to_raw_titlecase(self) -> None:
        # No npc_dota_hero_ prefix to strip; result is just titlecased input
        result = C.hero_display("totally_fake_hero")
        assert result == "Totally Fake Hero"

    def test_empty_string_fallback(self) -> None:
        result = C.hero_display("")
        # removeprefix("npc_dota_hero_") leaves "", replace("_"," ") → "", title() → ""
        assert result == ""

    def test_crystal_maiden_localized_name(self) -> None:
        assert C.hero_display("npc_dota_hero_crystal_maiden") == "Crystal Maiden"


# ---------------------------------------------------------------------------
# hero_short()
# ---------------------------------------------------------------------------


class TestHeroShort:
    """Tests for gem.constants.hero_short()."""

    def test_full_npc_name_works(self) -> None:
        assert C.hero_short("npc_dota_hero_axe") == "Axe"

    def test_bare_suffix_works(self) -> None:
        # hero_short prepends "npc_dota_hero_" before delegating to hero_display
        assert C.hero_short("axe") == "Axe"

    def test_bare_suffix_pudge(self) -> None:
        assert C.hero_short("pudge") == "Pudge"

    def test_bare_suffix_antimage(self) -> None:
        assert C.hero_short("antimage") == "Anti-Mage"

    def test_bare_suffix_crystal_maiden(self) -> None:
        assert C.hero_short("crystal_maiden") == "Crystal Maiden"

    def test_unknown_bare_suffix_falls_back(self) -> None:
        result = C.hero_short("made_up_hero")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_full_name_and_bare_suffix_give_same_result(self) -> None:
        assert C.hero_short("npc_dota_hero_sven") == C.hero_short("sven")


# ---------------------------------------------------------------------------
# hero_meta()
# ---------------------------------------------------------------------------


class TestHeroMeta:
    """Tests for gem.constants.hero_meta()."""

    def test_known_hero_returns_nonempty_dict(self) -> None:
        meta = C.hero_meta("npc_dota_hero_axe")
        assert isinstance(meta, dict)
        assert len(meta) > 0

    def test_known_hero_has_expected_fields(self) -> None:
        meta = C.hero_meta("npc_dota_hero_pudge")
        assert meta["localized_name"] == "Pudge"
        assert meta["id"] == 14
        assert isinstance(meta["primary_attr"], str)
        assert isinstance(meta["roles"], list)
        assert len(meta["roles"]) > 0

    def test_known_hero_axe_id(self) -> None:
        meta = C.hero_meta("npc_dota_hero_axe")
        assert meta["id"] == 2

    def test_known_hero_antimage_primary_attr(self) -> None:
        meta = C.hero_meta("npc_dota_hero_antimage")
        assert meta["primary_attr"] == "agi"

    def test_unknown_hero_returns_empty_dict(self) -> None:
        meta = C.hero_meta("npc_dota_hero_completely_fake")
        assert meta == {}

    def test_empty_string_returns_empty_dict(self) -> None:
        assert C.hero_meta("") == {}


# ---------------------------------------------------------------------------
# item_display()
# ---------------------------------------------------------------------------


class TestItemDisplay:
    """Tests for gem.constants.item_display()."""

    def test_known_item_with_prefix(self) -> None:
        assert C.item_display("item_blink") == "Blink Dagger"

    def test_known_item_boots(self) -> None:
        assert C.item_display("item_boots") == "Boots of Speed"

    def test_known_item_black_king_bar(self) -> None:
        assert C.item_display("item_black_king_bar") == "Black King Bar"

    def test_known_item_smoke_of_deceit(self) -> None:
        assert C.item_display("item_smoke_of_deceit") == "Smoke of Deceit"

    def test_known_item_aegis(self) -> None:
        assert C.item_display("item_aegis") == "Aegis of the Immortal"

    def test_unknown_item_returns_raw_string(self) -> None:
        raw = "item_totally_nonexistent_item_xyz"
        assert C.item_display(raw) == raw

    def test_unknown_item_no_prefix_returns_raw_string(self) -> None:
        # Without "item_" prefix, key lookup will also miss
        raw = "totally_nonexistent_item_xyz"
        assert C.item_display(raw) == raw

    def test_known_item_without_item_prefix_falls_back(self) -> None:
        # "blink" without the "item_" prefix — removeprefix leaves it unchanged,
        # key "blink" IS in items.json so it should succeed
        assert C.item_display("blink") == "Blink Dagger"


# ---------------------------------------------------------------------------
# ability_display()
# ---------------------------------------------------------------------------


class TestAbilityDisplay:
    """Tests for gem.constants.ability_display()."""

    def test_known_ability_returns_display_name(self) -> None:
        # axe_berserkers_call is a well-known ability
        result = C.ability_display("axe_berserkers_call")
        assert isinstance(result, str)
        assert result != "axe_berserkers_call"
        assert len(result) > 0

    def test_known_ability_axe_culling_blade(self) -> None:
        result = C.ability_display("axe_culling_blade")
        assert isinstance(result, str)
        assert result != "axe_culling_blade"

    def test_item_prefix_falls_through_to_item_display(self) -> None:
        # When an ability name starts with "item_", fall through to item_display
        result = C.ability_display("item_blink")
        assert result == "Blink Dagger"

    def test_item_prefix_unknown_item_returns_raw(self) -> None:
        raw = "item_completely_fake_item_xyz"
        assert C.ability_display(raw) == raw

    def test_unknown_ability_no_item_prefix_returns_raw(self) -> None:
        raw = "completely_unknown_ability_xyz"
        assert C.ability_display(raw) == raw

    def test_known_ability_pudge_meat_hook(self) -> None:
        result = C.ability_display("pudge_meat_hook")
        assert isinstance(result, str)
        assert result != "pudge_meat_hook"

    def test_ability_display_delegates_item_smoke(self) -> None:
        # item_smoke_of_deceit should resolve via item_display
        result = C.ability_display("item_smoke_of_deceit")
        assert result == "Smoke of Deceit"


# ---------------------------------------------------------------------------
# xp_to_next_level()
# ---------------------------------------------------------------------------


class TestXpToNextLevel:
    """Tests for gem.constants.xp_to_next_level()."""

    def test_level_1_returns_positive_int(self) -> None:
        # XP_LEVEL[1] = 240, so at level=1 with 0 XP we need 240
        result = C.xp_to_next_level(1, 0)
        assert isinstance(result, int)
        assert result > 0

    def test_level_1_exact_threshold(self) -> None:
        # At level=1, threshold is XP_LEVEL[1] = 240
        assert C.xp_to_next_level(1, 240) == 0

    def test_level_1_above_threshold_clamps_to_zero(self) -> None:
        # current_xp exceeds next threshold — max(0, ...) should give 0
        assert C.xp_to_next_level(1, 500) == 0

    def test_level_2_partial_xp(self) -> None:
        # XP_LEVEL[2] = 640; at level=2 with 400 XP → need 240 more
        result = C.xp_to_next_level(2, 400)
        assert result == C.XP_LEVEL[2] - 400

    def test_level_0_returns_zero_since_already_past_threshold(self) -> None:
        # XP_LEVEL[0] = 0; max(0, 0 - 0) = 0
        assert C.xp_to_next_level(0, 0) == 0

    def test_returns_none_at_max_level(self) -> None:
        # level >= len(XP_LEVEL) → None
        max_level = len(C.XP_LEVEL)
        assert C.xp_to_next_level(max_level, 0) is None

    def test_returns_none_well_above_max_level(self) -> None:
        assert C.xp_to_next_level(999, 0) is None

    def test_returns_int_at_second_to_last_level(self) -> None:
        # Last valid index is len(XP_LEVEL) - 1
        last_valid = len(C.XP_LEVEL) - 1
        result = C.xp_to_next_level(last_valid, 0)
        assert isinstance(result, int)

    def test_return_type_is_int_not_none_for_low_level(self) -> None:
        result = C.xp_to_next_level(5, 2440)
        assert result is not None
        assert isinstance(result, int)


# ---------------------------------------------------------------------------
# permanent_buff_name()
# ---------------------------------------------------------------------------


class TestPermanentBuffName:
    """Tests for gem.constants.permanent_buff_name()."""

    def test_buff_id_1_is_moon_shard(self) -> None:
        # PERMANENT_BUFFS["1"] = "moon_shard"
        assert C.permanent_buff_name(1) == "moon_shard"

    def test_buff_id_2_is_ultimate_scepter(self) -> None:
        # PERMANENT_BUFFS["2"] = "ultimate_scepter"
        assert C.permanent_buff_name(2) == "ultimate_scepter"

    def test_buff_id_6_is_tome_of_knowledge(self) -> None:
        # PERMANENT_BUFFS["6"] = "tome_of_knowledge"
        assert C.permanent_buff_name(6) == "tome_of_knowledge"

    def test_buff_id_12_is_aghanims_shard(self) -> None:
        # PERMANENT_BUFFS["12"] = "aghanims_shard"
        assert C.permanent_buff_name(12) == "aghanims_shard"

    def test_buff_id_13_is_axe_culling_blade(self) -> None:
        # PERMANENT_BUFFS["13"] = "axe_culling_blade"
        assert C.permanent_buff_name(13) == "axe_culling_blade"

    def test_invalid_buff_id_returns_string_of_id(self) -> None:
        result = C.permanent_buff_name(99999)
        assert result == "99999"

    def test_invalid_buff_id_zero_returns_string(self) -> None:
        result = C.permanent_buff_name(0)
        assert result == "0"

    def test_return_type_is_always_str(self) -> None:
        assert isinstance(C.permanent_buff_name(1), str)
        assert isinstance(C.permanent_buff_name(99999), str)


# ---------------------------------------------------------------------------
# league_name()
# ---------------------------------------------------------------------------


class TestLeagueName:
    """Tests for gem.constants.league_name()."""

    def test_zero_returns_none(self) -> None:
        assert C.league_name(0) is None

    def test_unknown_league_id_returns_none(self) -> None:
        # Use a very high ID that is extremely unlikely to exist
        assert C.league_name(999999999) is None

    def test_negative_id_returns_none(self) -> None:
        # Negative IDs should not match any league
        assert C.league_name(-1) is None

    def test_known_league_returns_string(self) -> None:
        # Pick the first key from LEAGUES (whatever it is) and verify we get a string back
        if not C.LEAGUES:
            pytest.skip("LEAGUES dict is empty")
        first_id = int(next(iter(C.LEAGUES)))
        result = C.league_name(first_id)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_all_league_values_are_strings(self) -> None:
        for str_id, name in C.LEAGUES.items():
            assert isinstance(name, str), f"League {str_id} value is not a str: {name!r}"

    def test_return_type_none_for_zero(self) -> None:
        result = C.league_name(0)
        assert result is None
