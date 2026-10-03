"""Tests for gem.analysis — position_at_tick and group_ability_hits."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest

import gem
import gem.analysis as analysis
import gem.analysis.combat as analysis_combat
import gem.analysis.fight_positioning as analysis_teamfight_positioning
import gem.analysis.spatial as analysis_spatial
from gem.analysis import group_ability_hits, position_at_tick, position_sample_at_tick, regions
from gem.combat.log import CombatLogEntry


def test_analysis_package_reexports_public_helpers() -> None:
    assert analysis.position_at_tick is analysis_spatial.position_at_tick
    assert analysis.position_sample_at_tick is analysis_spatial.position_sample_at_tick
    assert analysis.SampledPosition is analysis_spatial.SampledPosition
    assert analysis.group_ability_hits is analysis_combat.group_ability_hits
    assert analysis.AbilityCast is analysis_combat.AbilityCast
    assert (
        analysis.build_fight_positioning is analysis_teamfight_positioning.build_fight_positioning
    )
    assert gem.build_fight_positioning is analysis.build_fight_positioning


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _player(position_log: list[tuple[int, float, float]]) -> MagicMock:
    p = MagicMock()
    p.position_log = position_log
    return p


def _entry(**kwargs: Any) -> CombatLogEntry:
    defaults: dict[str, Any] = {
        "tick": 0,
        "log_type": "DAMAGE",
        "attacker_name": "npc_dota_hero_axe",
        "target_name": "npc_dota_hero_antimage",
        "inflictor_name": "axe_berserkers_call",
        "value": 100,
        "attacker_is_hero": True,
        "target_is_hero": True,
        "damage_type": "magical",
        "stun_duration": 0.0,
    }
    defaults.update(kwargs)
    return CombatLogEntry(**defaults)


# ---------------------------------------------------------------------------
# position_at_tick
# ---------------------------------------------------------------------------


class TestPositionAtTick:
    def test_empty_log_returns_none(self) -> None:
        player = _player([])
        assert position_at_tick(player, 100) is None

    def test_single_entry_always_returned(self) -> None:
        player = _player([(500, 1.0, 2.0)])
        assert position_at_tick(player, 0) == (1.0, 2.0)
        assert position_at_tick(player, 500) == (1.0, 2.0)
        assert position_at_tick(player, 9999) == (1.0, 2.0)

    def test_exact_tick_match(self) -> None:
        player = _player([(100, 10.0, 20.0), (200, 30.0, 40.0)])
        assert position_at_tick(player, 100) == (10.0, 20.0)
        assert position_at_tick(player, 200) == (30.0, 40.0)

    def test_tick_before_first_entry_returns_first(self) -> None:
        player = _player([(100, 10.0, 20.0), (200, 30.0, 40.0)])
        assert position_at_tick(player, 50) == (10.0, 20.0)

    def test_tick_after_last_entry_returns_last(self) -> None:
        player = _player([(100, 10.0, 20.0), (200, 30.0, 40.0)])
        assert position_at_tick(player, 500) == (30.0, 40.0)

    def test_picks_closer_of_two_samples(self) -> None:
        player = _player([(100, 1.0, 1.0), (200, 2.0, 2.0)])
        # tick 130 is 30 away from 100 and 70 away from 200 → picks (100)
        assert position_at_tick(player, 130) == (1.0, 1.0)
        # tick 180 is 80 away from 100 and 20 away from 200 → picks (200)
        assert position_at_tick(player, 180) == (2.0, 2.0)

    def test_equidistant_prefers_earlier(self) -> None:
        player = _player([(100, 1.0, 1.0), (200, 2.0, 2.0)])
        # tick 150 is 50 away from both — tie goes to the earlier (before)
        assert position_at_tick(player, 150) == (1.0, 1.0)

    def test_multiple_entries(self) -> None:
        log = [(i * 30, float(i), float(i)) for i in range(100)]
        player = _player(log)
        pos = position_at_tick(player, 30 * 50)
        assert pos == (50.0, 50.0)


class TestPositionSampleAtTick:
    def test_empty_log_returns_none(self) -> None:
        assert position_sample_at_tick(_player([]), 100) is None

    def test_returns_nearest_sample_metadata(self) -> None:
        sample = position_sample_at_tick(_player([(100, 1.0, 2.0), (200, 3.0, 4.0)]), 175)

        assert sample is not None
        assert (sample.x, sample.y) == (3.0, 4.0)
        assert sample.sample_tick == 200
        assert sample.age_ticks == 25

    def test_equidistant_sample_prefers_earlier(self) -> None:
        sample = position_sample_at_tick(_player([(100, 1.0, 2.0), (200, 3.0, 4.0)]), 150)

        assert sample is not None
        assert sample.sample_tick == 100
        assert sample.age_ticks == 50


# ---------------------------------------------------------------------------
# group_ability_hits
# ---------------------------------------------------------------------------


class TestGroupAbilityHits:
    def test_empty_log_returns_empty(self) -> None:
        assert group_ability_hits([]) == []

    def test_entries_without_inflictor_excluded(self) -> None:
        e = _entry(inflictor_name="")
        result = group_ability_hits([e])
        assert result == []

    def test_non_damage_entries_excluded(self) -> None:
        e = _entry(log_type="ABILITY")
        result = group_ability_hits([e])
        assert result == []

    def test_single_hit_becomes_single_cast(self) -> None:
        e = _entry(tick=100, value=200)
        casts = group_ability_hits([e])
        assert len(casts) == 1
        c = casts[0]
        assert c.tick == 100
        assert c.caster == "npc_dota_hero_axe"
        assert c.ability == "axe_berserkers_call"
        assert c.targets == ["npc_dota_hero_antimage"]
        assert c.total_damage == 200

    def test_two_hits_within_window_merged(self) -> None:
        e1 = _entry(tick=100, target_name="npc_dota_hero_antimage", value=150)
        e2 = _entry(
            tick=103, target_name="npc_dota_hero_axe", value=150, attacker_name="npc_dota_hero_axe"
        )
        # Same caster + ability, 3 ticks apart (within default window of 5)
        casts = group_ability_hits([e1, e2])
        assert len(casts) == 1
        assert casts[0].total_damage == 300
        assert len(casts[0].targets) == 2

    def test_two_hits_outside_window_are_separate_casts(self) -> None:
        e1 = _entry(tick=100, value=150)
        e2 = _entry(tick=110, value=150)  # 10 ticks apart, window=5
        casts = group_ability_hits([e1, e2])
        assert len(casts) == 2

    def test_different_abilities_are_separate_casts(self) -> None:
        e1 = _entry(tick=100, inflictor_name="axe_berserkers_call", value=100)
        e2 = _entry(tick=101, inflictor_name="axe_culling_blade", value=200)
        casts = group_ability_hits([e1, e2])
        assert len(casts) == 2

    def test_different_casters_are_separate_casts(self) -> None:
        e1 = _entry(tick=100, attacker_name="npc_dota_hero_axe", value=100)
        e2 = _entry(tick=101, attacker_name="npc_dota_hero_antimage", value=100)
        casts = group_ability_hits([e1, e2])
        assert len(casts) == 2

    def test_custom_window(self) -> None:
        e1 = _entry(tick=100, value=100)
        e2 = _entry(tick=108, value=100)  # 8 ticks apart
        # window=5: separate; window=10: merged
        assert len(group_ability_hits([e1, e2], window_ticks=5)) == 2
        assert len(group_ability_hits([e1, e2], window_ticks=10)) == 1

    def test_stun_duration_carried(self) -> None:
        e = _entry(tick=100, stun_duration=1.5)
        casts = group_ability_hits([e])
        assert casts[0].stun_duration == 1.5

    def test_damage_type_carried(self) -> None:
        e = _entry(tick=100, damage_type="magical")
        casts = group_ability_hits([e])
        assert casts[0].damage_type == "magical"

    def test_output_sorted_by_tick(self) -> None:
        entries = [_entry(tick=t, inflictor_name=f"spell_{t}") for t in [300, 100, 200]]
        casts = group_ability_hits(entries)
        ticks = [c.tick for c in casts]
        assert ticks == sorted(ticks)

    def test_entries_reference_preserved(self) -> None:
        e1 = _entry(tick=100, value=50)
        e2 = _entry(tick=102, target_name="npc_dota_hero_sf", value=60)
        casts = group_ability_hits([e1, e2])
        assert len(casts[0].entries) == 2
        assert casts[0].entries[0] is e1
        assert casts[0].entries[1] is e2


# ---------------------------------------------------------------------------
# Map-geometry single source of truth (_shared.py loads from map_constants.json)
# ---------------------------------------------------------------------------


class TestMapGeometrySingleSource:
    """_shared.py must derive map geometry from map_constants.json, not duplicate it."""

    def test_shared_constants_match_json(self) -> None:
        from gem.analysis import _shared
        from gem.catalog.map import load_map_constants

        data = load_map_constants()
        fr = data["fountains"]["radiant"]
        fd = data["fountains"]["dire"]
        assert (float(fr["x"]), float(fr["y"])) == _shared._RADIANT_FOUNTAIN
        assert (float(fd["x"]), float(fd["y"])) == _shared._DIRE_FOUNTAIN

    def test_region_geometry_matches_json(self) -> None:
        from gem.catalog.map import load_map_constants

        data = load_map_constants()["regions"]
        geometry = regions._REGIONS
        assert geometry is not None
        assert geometry.river_outline == tuple(
            (float(x), float(y)) for x, y in data["river_outline"]
        )
        half_line = tuple((float(x), float(y)) for x, y in data["half_line"])
        assert geometry.radiant_half[: len(half_line)] == half_line
        assert dict(geometry.lotus_pools) == {
            name: (float(pos["x"]), float(pos["y"])) for name, pos in data["lotus_pools"].items()
        }
        assert geometry.lotus_radius == float(data["lotus_radius"])

    def test_fallback_literals_mirror_json(self) -> None:
        # The graceful-fallback literals must stay in sync with the JSON so a
        # JSON-load failure degrades to the same values, not stale ones.
        from gem.analysis import _shared
        from gem.catalog.map import load_map_constants

        data = load_map_constants()
        fr = data["fountains"]["radiant"]
        fd = data["fountains"]["dire"]
        assert (float(fr["x"]), float(fr["y"])) == _shared._FALLBACK_RADIANT_FOUNTAIN
        assert (float(fd["x"]), float(fd["y"])) == _shared._FALLBACK_DIRE_FOUNTAIN


# The CDOTA_Unit_Fountain positions, read from every local fixture replay
# (8821954344 through 8974053011); all nine agree exactly.
_RADIANT_FOUNTAIN_ENTITY = (8928.0, 9446.0)
_DIRE_FOUNTAIN_ENTITY = (23792.0, 23232.0)


class TestFountainAnchorsAreFountainEntities:
    """The fountain anchors are the replay's fountain entities, not report-canvas guesses."""

    def test_anchors_pin_entity_positions(self) -> None:
        from gem.analysis import _shared

        assert _shared._RADIANT_FOUNTAIN == _RADIANT_FOUNTAIN_ENTITY
        assert _shared._DIRE_FOUNTAIN == _DIRE_FOUNTAIN_ENTITY

    @pytest.mark.slow
    @pytest.mark.integration
    def test_anchors_match_replay_fountain_entities(self, full_replay_path: Path) -> None:
        from gem.analysis import _shared
        from gem.extractors._snapshots import _pos
        from gem.parser import ReplayParser

        fountains: dict[int, set[tuple[float, float] | None]] = {}

        parser = ReplayParser(str(full_replay_path))

        def on_entity(entity: Any, op: Any) -> None:
            if entity.get_class_name() == "CDOTA_Unit_Fountain":
                fountains.setdefault(entity.get("m_iTeamNum"), set()).add(_pos(entity))
                if len(fountains) == 2:
                    # Both are created in the signon packet; the rest of the replay is not needed.
                    parser.stop_after_tick(parser.tick)

        parser.on_entity(on_entity)
        parser.parse()

        assert fountains == {
            2: {_shared._RADIANT_FOUNTAIN},
            3: {_shared._DIRE_FOUNTAIN},
        }


# Entity positions from replay 8974053011: fountains and ancients (CDOTA_Unit_Fountain,
# CDOTA_BaseNPC_Fort), mid T1 towers, the power-rune spawners, the Roshan pits, the
# lotus pools (CDOTA_BaseNPC_LotusPool), the wisdom shrines and the outposts.
_REGION_LANDMARKS = {
    "radiant fountain": ((8928, 9446), "radiant_half"),
    "dire fountain": ((23792, 23232), "dire_half"),
    "radiant ancient": ((10464, 11032), "radiant_half"),
    "dire ancient": ((21912, 21384), "dire_half"),
    "radiant mid T1": ((14840, 14976), "radiant_half"),
    "dire mid T1": ((16908, 17036), "dire_half"),
    "top power rune": ((14744, 17496), "river"),
    "bottom power rune": ((17564, 15168), "river"),
    "top Roshan pit": ((13190, 18779), "river"),
    "bottom Roshan pit": ((19214, 13644), "river"),
    "dire lotus pool": ((8836, 20593), "top_lotus"),
    "radiant lotus pool": ((23888, 11979), "bottom_lotus"),
    "west wisdom shrine": ((8296, 17152), "radiant_half"),
    "east wisdom shrine": ((24551, 15242), "dire_half"),
    "radiant outpost": ((12288, 15936), "radiant_half"),
    "dire outpost": ((19776, 15936), "dire_half"),
}


class TestRegionOf:
    """region_of follows the river traced on the 7.41 map, not the x = y diagonal."""

    def test_is_public(self) -> None:

        assert gem.region_of is regions.region_of
        assert gem.analysis.region_of is regions.region_of
        assert gem.MAP_REGIONS == regions.MAP_REGIONS
        assert {"region_of", "MAP_REGIONS"} <= set(gem.__all__)
        assert {"region_of", "MAP_REGIONS"} <= set(gem.analysis.__all__)

    @pytest.mark.parametrize("name", list(_REGION_LANDMARKS))
    def test_landmarks(self, name: str) -> None:
        from gem.analysis.regions import region_of

        (x, y), expected = _REGION_LANDMARKS[name]
        assert region_of(x, y) == expected

    @pytest.mark.parametrize(
        ("point", "expected"),
        [
            # North edge of Roshan pit 1's pool and south edge of pit 2's pool.
            ((12971, 19797), "river"),
            ((19568, 12497), "river"),
            # The top-lane stone plaza and the bottom-lane ford, either side of the
            # river's ends, are lane, not river.
            ((10375, 19094), "radiant_half"),
            ((10159, 19526), "dire_half"),
            ((22596, 13578), "dire_half"),
            ((22596, 12900), "radiant_half"),
        ],
    )
    def test_river_ends_at_the_lane_crossings(
        self, point: tuple[float, float], expected: str
    ) -> None:
        from gem.analysis.regions import region_of

        assert region_of(*point) == expected

    def test_lotus_area_radius(self) -> None:

        geometry = regions._REGIONS
        assert geometry is not None
        for name, (cx, cy) in geometry.lotus_pools:
            assert regions.region_of(cx + geometry.lotus_radius - 1, cy) == name
            assert regions.region_of(cx + geometry.lotus_radius + 1, cy) != name

    def test_owned_camps_sit_in_their_owners_half(self) -> None:
        from gem.analysis.regions import region_of
        from gem.catalog.map import load_camp_zones

        halves = {2: "radiant_half", 3: "dire_half"}
        wrong = {}
        for camp in load_camp_zones()["camps"]:
            owner = camp["topology"]["owner_team"]
            assert owner in halves, camp["id"]
            region = region_of(camp["center"]["x"], camp["center"]["y"])
            if region != halves[owner]:
                wrong[camp["id"]] = region
        assert wrong == {}

    def test_every_label_is_a_map_region(self) -> None:
        from gem.catalog.map import load_map_constants

        bounds = load_map_constants()["world_bounds"]
        labels = {
            regions.region_of(x, y)
            for x in range(int(bounds["xmin"]), int(bounds["xmax"]), 250)
            for y in range(int(bounds["ymin"]), int(bounds["ymax"]), 250)
        }
        assert labels == set(regions.MAP_REGIONS)

    def test_falls_back_to_fountain_bisector_without_geometry(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:

        monkeypatch.setattr(regions, "_REGIONS", None)
        assert regions.region_of(14744, 17496) == "radiant_half"
        assert regions.region_of(17564, 15168) == "dire_half"

    @pytest.mark.slow
    @pytest.mark.integration
    def test_replay_lotus_pools_runes_and_roshan(self, full_replay_path: Path) -> None:
        from gem.analysis.regions import region_of
        from gem.extractors._snapshots import _pos
        from gem.parser import ReplayParser

        positions: dict[str, set[tuple[float, float]]] = {}
        wanted = {
            "CDOTA_BaseNPC_LotusPool": 2,
            "CDOTA_Item_RuneSpawner_Powerup": 2,
            "CDOTA_RoshanSpawner": 1,
        }
        parser = ReplayParser(str(full_replay_path))

        def on_entity(entity: Any, op: Any) -> None:
            name = entity.get_class_name()
            pos = _pos(entity)
            if name in wanted and pos is not None:
                positions.setdefault(name, set()).add(pos)
                if all(len(positions.get(n, ())) >= k for n, k in wanted.items()):
                    # All are created in the signon packet.
                    parser.stop_after_tick(parser.tick)

        parser.on_entity(on_entity)
        parser.parse()

        lotus = sorted(region_of(*p) for p in positions["CDOTA_BaseNPC_LotusPool"])
        assert lotus == ["bottom_lotus", "top_lotus"]
        for name in ("CDOTA_Item_RuneSpawner_Powerup", "CDOTA_RoshanSpawner"):
            assert {region_of(*p) for p in positions[name]} == {"river"}
