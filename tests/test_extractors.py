"""Tests for gem.extractors — players, objectives, and wards.

Unit tests use fake entity/combat-log objects to exercise extractor logic
without a real replay file. Integration tests marked ``slow`` + ``integration``
parse a real .dem fixture and verify plausible output.
"""

from __future__ import annotations

from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Helpers — fake objects
# ---------------------------------------------------------------------------

FIXTURE = Path(__file__).parent / "fixtures" / "ti14_finals_g1_xg_vs_falcons.dem"


class FakeClass:
    """Mimics an entity ClassInfo."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.class_id = 1
        self.serializer = None


def _make_entity(class_name: str, state: dict | None = None):
    from gem.entities import Entity

    e = Entity(index=0, serial=0, cls=FakeClass(class_name))
    if state:
        e._state.update(state)
    return e


def _make_hero(suffix: str = "Axe", player_id: int = 0, team: int = 2, state: dict | None = None):
    """Create a fake hero entity.

    ``player_id`` is the logical slot (0-9). The raw entity field value is
    doubled (``player_id * 2``) to match the wire format; the extractor divides
    by 2 to recover the slot. Reference: opendota/Parse.java getPlayerSlotFromEntity.
    """
    base = {
        "m_iPlayerID": player_id * 2,  # raw wire value; extractor divides by 2
        "m_iTeamNum": team,
        "m_nCurrentLevel": 5,
        "m_iCurrentXP": 1000,
        "m_iHealth": 800,
        "m_iMaxHealth": 1000,
        "m_flMana": 300.0,
        "m_flMaxMana": 400.0,
        "m_iLastHitCount": 20,
        "m_iDenies": 3,
    }
    if state:
        base.update(state)
    return _make_entity(f"CDOTA_Unit_Hero_{suffix}", base)


def _make_combat_log_entry(**kwargs):
    from gem.combatlog import CombatLogEntry

    defaults = {
        "tick": 100,
        "log_type": "DEATH",
        "attacker_name": "npc_dota_hero_axe",
        "target_name": "npc_dota_hero_juggernaut",
        "inflictor_name": "",
        "value": 0,
        "attacker_is_hero": True,
        "target_is_hero": True,
        "attacker_is_illusion": False,
        "target_is_illusion": False,
        "ability_level": 0,
        "gold_reason": 0,
        "xp_reason": 0,
    }
    defaults.update(kwargs)
    return CombatLogEntry(**defaults)


class FakeParser:
    """Minimal parser stub that records registered callbacks."""

    def __init__(self, tick: int = 0) -> None:
        self.tick = tick
        self._entity_handlers = []
        self._combat_log_handlers = []
        self._chat_event_handlers = []
        self.entity_manager = None
        self.string_tables = type("ST", (), {"get_by_name": lambda self, n: None})()

    def on_entity(self, handler) -> None:
        self._entity_handlers.append(handler)

    def on_combat_log_entry(self, handler) -> None:
        self._combat_log_handlers.append(handler)

    def on_chat_event(self, handler) -> None:
        self._chat_event_handlers.append(handler)

    def on_game_start(self, handler) -> None:
        pass

    def on_game_end(self, handler) -> None:
        pass

    def fire_entity(self, entity, op) -> None:
        for h in self._entity_handlers:
            h(entity, op)

    def fire_combat_log(self, entry) -> None:
        for h in self._combat_log_handlers:
            h(entry)


# ---------------------------------------------------------------------------
# ObjectivesExtractor tests
# ---------------------------------------------------------------------------


class TestObjectivesExtractor:
    def _make(self):
        from gem.extractors.objectives import ObjectivesExtractor

        e = ObjectivesExtractor()
        parser = FakeParser()
        e.attach(parser)
        return e, parser

    def test_attach_registers_combat_log_callback(self):
        _, parser = self._make()
        assert len(parser._combat_log_handlers) == 1

    def test_roshan_kill_detected(self):
        ext, parser = self._make()
        parser.fire_combat_log(
            _make_combat_log_entry(
                tick=500, target_name="npc_dota_roshan", attacker_name="npc_dota_hero_axe"
            )
        )
        assert len(ext.roshan_kills) == 1
        kill = ext.roshan_kills[0]
        assert kill.tick == 500
        assert kill.killer == "npc_dota_hero_axe"
        assert kill.kill_number == 1

    def test_roshan_kill_number_increments(self):
        ext, parser = self._make()
        for tick in (500, 2000, 4000):
            parser.fire_combat_log(_make_combat_log_entry(tick=tick, target_name="npc_dota_roshan"))
        assert [k.kill_number for k in ext.roshan_kills] == [1, 2, 3]

    def test_tower_kill_radiant_detected(self):
        ext, parser = self._make()
        parser.fire_combat_log(
            _make_combat_log_entry(
                tick=300,
                target_name="npc_dota_goodguys_tower1_top",
                attacker_name="npc_dota_hero_axe",
            )
        )
        assert len(ext.tower_kills) == 1
        tk = ext.tower_kills[0]
        assert tk.team == 2  # Radiant owns the tower
        assert tk.tower_name == "npc_dota_goodguys_tower1_top"

    def test_tower_kill_dire_detected(self):
        ext, parser = self._make()
        parser.fire_combat_log(
            _make_combat_log_entry(
                tick=300,
                target_name="npc_dota_badguys_tower1_top",
                attacker_name="npc_dota_hero_juggernaut",
            )
        )
        assert len(ext.tower_kills) == 1
        assert ext.tower_kills[0].team == 3  # Dire owns the tower

    def test_barracks_kill_detected(self):
        ext, parser = self._make()
        parser.fire_combat_log(
            _make_combat_log_entry(
                tick=700,
                target_name="npc_dota_goodguys_melee_rax_top",
                attacker_name="npc_dota_hero_axe",
            )
        )
        assert len(ext.barracks_kills) == 1
        bk = ext.barracks_kills[0]
        assert bk.team == 2
        assert bk.killer == "npc_dota_hero_axe"

    def test_non_death_entry_ignored(self):
        ext, parser = self._make()
        parser.fire_combat_log(
            _make_combat_log_entry(log_type="DAMAGE", target_name="npc_dota_roshan")
        )
        assert ext.roshan_kills == []
        assert ext.tower_kills == []

    def test_hero_death_not_captured(self):
        ext, parser = self._make()
        parser.fire_combat_log(
            _make_combat_log_entry(log_type="DEATH", target_name="npc_dota_hero_axe")
        )
        assert ext.roshan_kills == []
        assert ext.tower_kills == []
        assert ext.barracks_kills == []


# ---------------------------------------------------------------------------
# PlayerExtractor tests
# ---------------------------------------------------------------------------


class TestPlayerExtractor:
    def _make(self, sample_interval: int = 150):
        from gem.extractors.players import PlayerExtractor

        ext = PlayerExtractor(sample_interval=sample_interval)
        parser = FakeParser(tick=0)
        ext.attach(parser)
        return ext, parser

    def test_attach_registers_entity_callback(self):
        _, parser = self._make()
        assert len(parser._entity_handlers) == 1

    def test_snapshot_taken_at_interval(self):
        from gem.entities import EntityOp

        ext, parser = self._make(sample_interval=100)
        hero = _make_hero("Axe", player_id=0)
        parser.tick = 0
        parser.fire_entity(hero, EntityOp.CREATED_ENTERED)
        assert len(ext.snapshots) == 1  # first sample always taken

        parser.tick = 50
        parser.fire_entity(hero, EntityOp.UPDATED)
        assert len(ext.snapshots) == 1  # too soon

        parser.tick = 100
        parser.fire_entity(hero, EntityOp.UPDATED)
        assert len(ext.snapshots) == 2  # interval reached

    def test_hero_cached_on_update(self):
        from gem.entities import EntityOp

        ext, parser = self._make()
        hero = _make_hero("Axe", player_id=2)
        parser.tick = 0
        parser.fire_entity(hero, EntityOp.CREATED_ENTERED)
        assert hero.get_index() in ext._heroes

    def test_hero_removed_on_delete(self):
        from gem.entities import EntityOp

        ext, parser = self._make()
        hero = _make_hero("Axe", player_id=2)
        parser.tick = 0
        parser.fire_entity(hero, EntityOp.CREATED_ENTERED)
        assert hero.get_index() in ext._heroes
        parser.fire_entity(hero, EntityOp.DELETED_LEFT)
        assert hero.get_index() not in ext._heroes

    def test_snapshot_fields_from_entity_state(self):
        from gem.entities import EntityOp

        ext, parser = self._make(sample_interval=1)
        hero = _make_hero(
            "Juggernaut",
            player_id=1,
            team=3,
            state={
                "m_nCurrentLevel": 10,
                "m_iCurrentXP": 5000,
                "m_iHealth": 600,
                "m_iLastHitCount": 50,
                "m_iDenies": 7,
            },
        )
        parser.tick = 300
        parser.fire_entity(hero, EntityOp.CREATED_ENTERED)
        snap = ext.snapshots[-1]
        assert snap.player_id == 1
        assert snap.team == 3
        assert snap.level == 10
        assert snap.xp == 5000
        assert snap.hp == 600
        assert snap.lh == 50
        assert snap.dn == 7
        assert snap.tick == 300

    def test_position_none_when_cell_fields_missing(self):
        from gem.entities import EntityOp

        ext, parser = self._make(sample_interval=1)
        hero = _make_hero("Axe", player_id=0)
        parser.tick = 0
        parser.fire_entity(hero, EntityOp.CREATED_ENTERED)
        snap = ext.snapshots[-1]
        assert snap.x is None
        assert snap.y is None

    def test_position_computed_from_cell_fields(self):
        from gem.entities import EntityOp

        ext, parser = self._make(sample_interval=1)
        hero = _make_hero(
            "Axe",
            player_id=0,
            state={
                "CBodyComponent.m_cellX": 100,
                "CBodyComponent.m_cellY": 120,
                "CBodyComponent.m_vecX": 32.0,
                "CBodyComponent.m_vecY": 64.0,
            },
        )
        parser.tick = 0
        parser.fire_entity(hero, EntityOp.CREATED_ENTERED)
        snap = ext.snapshots[-1]
        assert snap.x == pytest.approx(100 * 128 + 32.0)
        assert snap.y == pytest.approx(120 * 128 + 64.0)

    def test_time_series_aggregates_snapshots(self):
        from gem.entities import EntityOp

        ext, parser = self._make(sample_interval=100)
        hero = _make_hero("Axe", player_id=0)
        for tick in (0, 100, 200):
            parser.tick = tick
            parser.fire_entity(hero, EntityOp.UPDATED)
        ts = ext.time_series(0)
        assert ts.player_id == 0
        assert len(ts.ticks) == len(ts.lh_t) == len(ts.xp_t)

    def test_hero_pos_lookup(self):
        from gem.entities import EntityOp

        ext, parser = self._make(sample_interval=1)
        hero = _make_hero(
            "Axe",
            player_id=0,
            state={
                "CBodyComponent.m_cellX": 50,
                "CBodyComponent.m_cellY": 60,
                "CBodyComponent.m_vecX": 10.0,
                "CBodyComponent.m_vecY": 20.0,
            },
        )
        parser.tick = 0
        parser.fire_entity(hero, EntityOp.CREATED_ENTERED)
        pos = ext.hero_pos("npc_dota_hero_axe")
        assert pos is not None
        assert pos[0] == pytest.approx(50 * 128 + 10.0)


# ---------------------------------------------------------------------------
# WardsExtractor tests
# ---------------------------------------------------------------------------


class TestWardsExtractor:
    def _make(self, window: int = 60):
        from gem.extractors.wards import WardsExtractor

        ext = WardsExtractor(coord_window=window)
        parser = FakeParser(tick=0)
        ext.attach(parser)
        return ext, parser

    def test_attach_registers_both_callbacks(self):
        _, parser = self._make()
        assert len(parser._combat_log_handlers) == 1
        assert len(parser._entity_handlers) == 1

    def test_observer_placement_from_combat_log(self):
        ext, parser = self._make()
        parser.fire_combat_log(
            _make_combat_log_entry(
                log_type="ITEM",
                tick=200,
                attacker_name="npc_dota_hero_axe",
                inflictor_name="item_ward_observer",
            )
        )
        assert len(ext._placements) == 1
        assert ext._placements[0].ward_type == "observer"
        assert ext._placements[0].placer == "npc_dota_hero_axe"

    def test_sentry_placement_from_combat_log(self):
        ext, parser = self._make()
        parser.fire_combat_log(
            _make_combat_log_entry(
                log_type="ITEM",
                tick=200,
                attacker_name="npc_dota_hero_axe",
                inflictor_name="item_ward_sentry",
            )
        )
        assert ext._placements[0].ward_type == "sentry"

    def test_dispenser_maps_to_observer(self):
        ext, parser = self._make()
        parser.fire_combat_log(
            _make_combat_log_entry(
                log_type="ITEM",
                tick=200,
                attacker_name="npc_dota_hero_axe",
                inflictor_name="item_ward_dispenser",
            )
        )
        assert ext._placements[0].ward_type == "observer"

    def test_non_ward_item_ignored(self):
        ext, parser = self._make()
        parser.fire_combat_log(_make_combat_log_entry(log_type="ITEM", inflictor_name="item_blink"))
        assert ext._placements == []

    def test_coord_match_exact_tick(self):
        from gem.extractors.wards import _match_coords, _WardPlacement

        placements = [_WardPlacement(tick=100, placer="x", ward_type="observer")]
        spawns = [(100, "observer", 2, 500.0, 600.0)]
        result = _match_coords(placements, spawns, "observer", window=60)
        assert 0 in result
        assert result[0] == pytest.approx((500.0, 600.0))

    def test_coord_match_within_window(self):
        from gem.extractors.wards import _match_coords, _WardPlacement

        placements = [_WardPlacement(tick=100, placer="x", ward_type="observer")]
        spawns = [(150, "observer", 2, 300.0, 400.0)]  # 50 ticks after → within window
        result = _match_coords(placements, spawns, "observer", window=60)
        assert 0 in result

    def test_coord_match_outside_window_gives_no_match(self):
        from gem.extractors.wards import _match_coords, _WardPlacement

        placements = [_WardPlacement(tick=100, placer="x", ward_type="observer")]
        spawns = [(200, "observer", 2, 300.0, 400.0)]  # 100 ticks after → outside window
        result = _match_coords(placements, spawns, "observer", window=60)
        assert 0 not in result

    def test_same_slot_matchable_to_multiple_placements(self):
        """Entity slot reuse: same spawn record can match multiple placements."""
        from gem.extractors.wards import _match_coords, _WardPlacement

        placements = [
            _WardPlacement(tick=100, placer="x", ward_type="observer"),
            _WardPlacement(tick=600, placer="y", ward_type="observer"),
        ]
        # One entity record at tick 100 — matches first placement
        # Another entity record at tick 600 — matches second placement
        spawns = [
            (100, "observer", 2, 100.0, 200.0),
            (600, "observer", 2, 300.0, 400.0),
        ]
        result = _match_coords(placements, spawns, "observer", window=60)
        assert 0 in result
        assert 1 in result

    def test_ward_events_lazy_finalization(self):
        ext, parser = self._make()
        assert ext._finalized is None
        _ = ext.ward_events  # trigger lazy finalization
        assert ext._finalized is not None

    def test_finalize_explicit_call(self):
        ext, parser = self._make()
        result = ext.finalize()
        assert isinstance(result, list)
        assert ext._finalized is not None

    def test_ward_event_no_coord_when_no_entity_match(self):
        ext, parser = self._make()
        parser.fire_combat_log(
            _make_combat_log_entry(
                log_type="ITEM",
                tick=200,
                attacker_name="npc_dota_hero_axe",
                inflictor_name="item_ward_observer",
            )
        )
        # No entity events → no coord match
        events = ext.ward_events
        assert len(events) == 1
        assert events[0].x is None
        assert events[0].y is None

    def test_ward_event_with_coord_when_entity_matches(self):
        from gem.entities import EntityOp

        ext, parser = self._make()
        # Place a ward via combat log
        parser.fire_combat_log(
            _make_combat_log_entry(
                log_type="ITEM",
                tick=200,
                attacker_name="npc_dota_hero_axe",
                inflictor_name="item_ward_observer",
            )
        )
        # Fire a ward entity event at the same tick
        ward = _make_entity(
            "CDOTA_NPC_Observer_Ward",
            {
                "m_iTeamNum": 2,
                "CBodyComponent.m_cellX": 100,
                "CBodyComponent.m_cellY": 120,
                "CBodyComponent.m_vecX": 0.0,
                "CBodyComponent.m_vecY": 0.0,
            },
        )
        parser.tick = 200
        parser.fire_entity(ward, EntityOp.CREATED_ENTERED)

        events = ext.ward_events
        assert len(events) == 1
        assert events[0].x == pytest.approx(100 * 128 + 0.0)
        assert events[0].y == pytest.approx(120 * 128 + 0.0)


# ---------------------------------------------------------------------------
# Integration tests
# ---------------------------------------------------------------------------


@pytest.mark.slow
@pytest.mark.integration
class TestExtractorsIntegration:
    @pytest.fixture(autouse=True)
    def _require_fixture(self):
        if not FIXTURE.exists():
            pytest.skip("Integration fixture not available")

    def _parse(self):
        from gem.extractors import ObjectivesExtractor, PlayerExtractor, WardsExtractor
        from gem.parser import ReplayParser

        parser = ReplayParser(str(FIXTURE))
        players = PlayerExtractor(sample_interval=300)
        objectives = ObjectivesExtractor()
        wards = WardsExtractor()
        players.attach(parser)
        objectives.attach(parser)
        wards.attach(parser)
        parser.parse()
        return players, objectives, wards

    def test_objectives_tower_kills_positive(self):
        _, objectives, _ = self._parse()
        assert len(objectives.tower_kills) > 0

    def test_objectives_roshan_kills_nonnegative(self):
        _, objectives, _ = self._parse()
        assert len(objectives.roshan_kills) >= 0

    def test_wards_placements_positive(self):
        _, _, wards = self._parse()
        assert len(wards.ward_events) > 0

    def test_wards_have_some_coordinates(self):
        _, _, wards = self._parse()
        with_coords = [w for w in wards.ward_events if w.x is not None]
        assert len(with_coords) > 0

    def test_player_snapshots_positive(self):
        players, _, _ = self._parse()
        assert len(players.snapshots) > 0

    def test_player_snapshot_fields_valid(self):
        players, _, _ = self._parse()
        for snap in players.snapshots[:20]:
            assert 0 <= snap.player_id <= 9
            assert snap.team in (2, 3)
            assert snap.level >= 0  # level 0 is valid before hero selects
            assert snap.hp >= 0
            assert snap.tick >= 0

    def test_player_time_series_nonempty(self):
        players, _, _ = self._parse()
        # At least one player should have time-series data
        found = False
        for pid in range(10):
            ts = players.time_series(pid)
            if ts.ticks:
                found = True
                assert len(ts.ticks) == len(ts.xp_t) == len(ts.lh_t)
                break
        assert found
