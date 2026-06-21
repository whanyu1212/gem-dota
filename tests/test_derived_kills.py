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

    def test_roshan_banner_is_not_roshan(self):
        # The banner unit is distinct from Roshan and must not count.
        assert not units.is_roshan("npc_dota_unit_roshans_banner")


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

    def test_hero_kills_not_categorized(self):
        # Heroes/buildings are not any of the specialty categories.
        cats = categorize_kills({"npc_dota_hero_axe": 4, "npc_dota_badguys_tower1_mid": 1})
        assert cats.neutral_kills == 0
        assert cats.lane_kills == 0
        assert cats.roshan_kills == 0
