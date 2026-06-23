"""Tests for gem.results.derived and gem.catalog.units kill categorization."""

from __future__ import annotations

from gem.catalog import units
from gem.combat.log import CombatLogEntry
from gem.results.derived import categorize_kills, killed_counts


def _kill(target: str, tick: int = 1, will_reincarnate: bool = False) -> CombatLogEntry:
    return CombatLogEntry(
        tick=tick,
        log_type="DEATH",
        target_name=target,
        will_reincarnate=will_reincarnate,
    )


# ---------------------------------------------------------------------------
# catalog.units classifiers
# ---------------------------------------------------------------------------


class TestUnitClassifiers:
    def test_ancient_is_also_neutral(self):
        name = "npc_dota_neutral_black_drake"
        assert units.is_ancient(name)
        assert units.is_neutral(name)

    def test_regular_neutral_is_not_ancient(self):
        name = "npc_dota_neutral_kobold"
        assert units.is_neutral(name)
        assert not units.is_ancient(name)

    def test_lane_creep(self):
        assert units.is_lane_creep("npc_dota_creep_badguys_melee")
        assert not units.is_lane_creep("npc_dota_neutral_kobold")

    def test_courier_observer_sentry_roshan(self):
        assert units.is_courier("npc_dota_courier")
        assert units.is_observer_ward("npc_dota_observer_wards")
        assert units.is_sentry_ward("npc_dota_sentry_wards")
        assert units.is_roshan("npc_dota_roshan")

    def test_roshan_banner_counts_as_roshan(self):
        # Some replays credit the Roshan kill under the banner unit; OpenDota
        # counts both toward roshan_kills, so both must classify as Roshan.
        assert units.is_roshan("npc_dota_roshan")
        assert units.is_roshan("npc_dota_unit_roshans_banner")


# ---------------------------------------------------------------------------
# killed_counts
# ---------------------------------------------------------------------------


class TestKilledCounts:
    def test_counts_per_target(self):
        log = [
            _kill("npc_dota_creep_badguys_melee"),
            _kill("npc_dota_creep_badguys_melee"),
            _kill("npc_dota_neutral_kobold"),
        ]
        assert killed_counts(log) == {
            "npc_dota_creep_badguys_melee": 2,
            "npc_dota_neutral_kobold": 1,
        }

    def test_skips_reincarnation_trigger_deaths(self):
        # The trigger death (will_reincarnate) is not a real kill.
        log = [
            _kill("npc_dota_hero_wraith_king", will_reincarnate=True),
            _kill("npc_dota_hero_wraith_king"),
        ]
        assert killed_counts(log) == {"npc_dota_hero_wraith_king": 1}

    def test_skips_empty_target(self):
        assert killed_counts([_kill("")]) == {}


# ---------------------------------------------------------------------------
# categorize_kills
# ---------------------------------------------------------------------------


class TestCategorizeKills:
    def test_ancient_counts_toward_both_neutral_and_ancient(self):
        killed = {"npc_dota_neutral_black_drake": 3}
        cats = categorize_kills(killed)
        assert cats.ancient_kills == 3
        assert cats.neutral_kills == 3

    def test_regular_neutral_only_neutral(self):
        cats = categorize_kills({"npc_dota_neutral_kobold": 5})
        assert cats.neutral_kills == 5
        assert cats.ancient_kills == 0

    def test_each_category(self):
        killed = {
            "npc_dota_creep_badguys_melee": 10,
            "npc_dota_courier": 1,
            "npc_dota_observer_wards": 2,
            "npc_dota_sentry_wards": 3,
            "npc_dota_roshan": 1,
        }
        cats = categorize_kills(killed)
        assert cats.lane_kills == 10
        assert cats.courier_kills == 1
        assert cats.observer_kills == 2
        assert cats.sentry_kills == 3
        assert cats.roshan_kills == 1
        assert cats.neutral_kills == 0

    def test_roshan_banner_counts_toward_roshan_kills(self):
        # Replays that record the kill under the banner unit must still count.
        cats = categorize_kills({"npc_dota_unit_roshans_banner": 1})
        assert cats.roshan_kills == 1

    def test_hero_kills_not_categorized(self):
        # Heroes/buildings are not any of the specialty categories.
        cats = categorize_kills({"npc_dota_hero_axe": 4, "npc_dota_badguys_tower1_mid": 1})
        assert cats.neutral_kills == 0
        assert cats.lane_kills == 0
        assert cats.roshan_kills == 0


# ---------------------------------------------------------------------------
# Building-status bitmasks
# ---------------------------------------------------------------------------

from dataclasses import dataclass  # noqa: E402

from gem.results.derived import building_status  # noqa: E402


@dataclass
class _TK:
    team: int
    tower_name: str


@dataclass
class _BK:
    team: int
    barracks_name: str


class TestBuildingStatus:
    _ALL_TOWERS = (1 << 11) - 1  # 2047
    _ALL_RAX = (1 << 6) - 1  # 63

    def test_no_kills_all_standing(self):
        r = building_status([], [])
        assert r["tower_status_radiant"] == self._ALL_TOWERS
        assert r["tower_status_dire"] == self._ALL_TOWERS
        assert r["barracks_status_radiant"] == self._ALL_RAX
        assert r["barracks_status_dire"] == self._ALL_RAX

    def test_tier1_top_clears_bit0(self):
        r = building_status([_TK(2, "npc_dota_goodguys_tower1_top")], [])
        # bit 0 cleared -> 2047 - 1 = 2046
        assert r["tower_status_radiant"] == self._ALL_TOWERS - 1

    def test_tier_lane_bit_layout(self):
        # mid tier2 = lane offset 3 + (2-1) = bit 4 -> clears 16.
        r = building_status([_TK(3, "npc_dota_badguys_tower2_mid")], [])
        assert r["tower_status_dire"] == self._ALL_TOWERS - (1 << 4)

    def test_two_tier4_clear_both_ancient_bits(self):
        # Both tier-4 towers share the name ..._tower4; two deaths clear bits 9 & 10.
        r = building_status(
            [_TK(2, "npc_dota_goodguys_tower4"), _TK(2, "npc_dota_goodguys_tower4")], []
        )
        assert r["tower_status_radiant"] == self._ALL_TOWERS - (1 << 9) - (1 << 10)

    def test_one_tier4_clears_one_bit(self):
        r = building_status([_TK(3, "npc_dota_badguys_tower4")], [])
        assert r["tower_status_dire"] == self._ALL_TOWERS - (1 << 9)

    def test_barracks_bit_layout(self):
        # mid melee = lane offset 2 + 0 = bit 2; mid ranged = bit 3.
        r = building_status(
            [],
            [
                _BK(3, "npc_dota_badguys_melee_rax_mid"),
                _BK(3, "npc_dota_badguys_range_rax_mid"),
            ],
        )
        # bits 2 and 3 cleared -> 63 - 4 - 8 = 51 (matches OpenDota fixture).
        assert r["barracks_status_dire"] == 51

    def test_team_separation(self):
        # A Radiant tower death must not affect the Dire mask.
        r = building_status([_TK(2, "npc_dota_goodguys_tower1_bot")], [])
        assert r["tower_status_dire"] == self._ALL_TOWERS
        assert r["tower_status_radiant"] != self._ALL_TOWERS
