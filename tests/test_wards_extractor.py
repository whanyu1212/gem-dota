"""Unit tests for gem.extractors.wards.

Covers _match_coords, WardsExtractor._on_combat_log, _on_entity,
_find_spawn_state, _find_killer, _make_event, finalize/ward_events,
and hero player_id resolution.
"""

from __future__ import annotations

from gem.combatlog import CombatLogEntry
from gem.entities import Entity, EntityOp
from gem.extractors.wards import (
    WardsExtractor,
    _match_coords,
    _WardPlacement,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class FakeClass:
    def __init__(self, name: str) -> None:
        self.name = name
        self.class_id = 1
        self.serializer = None


def _ent(class_name: str, index: int = 0, **state) -> Entity:
    e = Entity(index=index, serial=0, cls=FakeClass(class_name))
    e._state.update(state)
    return e


def _observer_entity(
    index: int = 0, tick_spawn: int = 100, x: float = 1000.0, y: float = 2000.0
) -> Entity:
    cell_x = int(x) // 128
    vec_x = x - cell_x * 128
    cell_y = int(y) // 128
    vec_y = y - cell_y * 128
    return _ent(
        "CDOTA_NPC_Observer_Ward",
        index=index,
        **{
            "m_lifeState": 0,
            "m_iTeamNum": 2,
            "CBodyComponent.m_cellX": cell_x,
            "CBodyComponent.m_cellY": cell_y,
            "CBodyComponent.m_vecX": float(vec_x),
            "CBodyComponent.m_vecY": float(vec_y),
        },
    )


def _sentry_entity(index: int = 1, x: float = 3000.0, y: float = 4000.0) -> Entity:
    cell_x = int(x) // 128
    vec_x = x - cell_x * 128
    cell_y = int(y) // 128
    vec_y = y - cell_y * 128
    return _ent(
        "CDOTA_NPC_Observer_Ward_TrueSight",
        index=index,
        **{
            "m_lifeState": 0,
            "m_iTeamNum": 3,
            "CBodyComponent.m_cellX": cell_x,
            "CBodyComponent.m_cellY": cell_y,
            "CBodyComponent.m_vecX": float(vec_x),
            "CBodyComponent.m_vecY": float(vec_y),
        },
    )


def _placement(
    tick: int, placer: str = "npc_dota_hero_axe", ward_type: str = "observer"
) -> _WardPlacement:
    return _WardPlacement(tick=tick, placer=placer, ward_type=ward_type)


class FakeParser:
    def __init__(self, tick: int = 0):
        self.tick = tick
        self._cl_handlers = []
        self._ent_handlers = []

    def on_combat_log_entry(self, h):
        self._cl_handlers.append(h)

    def on_entity(self, h):
        self._ent_handlers.append(h)


def _ward_extractor(tick: int = 0) -> tuple[WardsExtractor, FakeParser]:
    ext = WardsExtractor()
    parser = FakeParser(tick=tick)
    ext.attach(parser)
    return ext, parser


# ---------------------------------------------------------------------------
# _match_coords
# ---------------------------------------------------------------------------


class TestMatchCoords:
    def test_exact_tick_match(self):
        placements = [_placement(100)]
        spawns = [(100, "observer", 2, 500.0, 600.0)]
        result = _match_coords(placements, spawns, "observer", 60)
        assert 0 in result
        assert result[0] == (500.0, 600.0)

    def test_within_window(self):
        placements = [_placement(100)]
        spawns = [(130, "observer", 2, 700.0, 800.0)]
        result = _match_coords(placements, spawns, "observer", 60)
        assert 0 in result

    def test_outside_window_no_match(self):
        placements = [_placement(100)]
        spawns = [(200, "observer", 2, 700.0, 800.0)]
        result = _match_coords(placements, spawns, "observer", 60)
        assert 0 not in result

    def test_wrong_type_filtered(self):
        placements = [_placement(100, ward_type="observer")]
        spawns = [(100, "sentry", 2, 500.0, 600.0)]
        result = _match_coords(placements, spawns, "observer", 60)
        assert 0 not in result

    def test_nearest_match_chosen(self):
        placements = [_placement(100)]
        spawns = [
            (90, "observer", 2, 1.0, 1.0),  # dt=10
            (105, "observer", 2, 2.0, 2.0),  # dt=5 — closer
        ]
        result = _match_coords(placements, spawns, "observer", 60)
        assert result[0] == (2.0, 2.0)

    def test_multiple_placements_same_spawn_reused(self):
        placements = [_placement(100), _placement(200)]
        spawns = [(100, "observer", 2, 5.0, 6.0), (200, "observer", 2, 7.0, 8.0)]
        result = _match_coords(placements, spawns, "observer", 60)
        assert result[0] == (5.0, 6.0)
        assert result[1] == (7.0, 8.0)

    def test_empty_placements(self):
        result = _match_coords([], [(100, "observer", 2, 1.0, 2.0)], "observer", 60)
        assert result == {}

    def test_empty_spawns(self):
        placements = [_placement(100)]
        result = _match_coords(placements, [], "observer", 60)
        assert result == {}


# ---------------------------------------------------------------------------
# WardsExtractor._on_combat_log
# ---------------------------------------------------------------------------


class TestOnCombatLog:
    def test_observer_placement_recorded(self):
        ext, _ = _ward_extractor()
        entry = CombatLogEntry(
            tick=100,
            log_type="ITEM",
            attacker_name="npc_dota_hero_axe",
            inflictor_name="item_ward_observer",
        )
        ext._on_combat_log(entry)
        assert len(ext._placements) == 1
        assert ext._placements[0].ward_type == "observer"

    def test_sentry_placement_recorded(self):
        ext, _ = _ward_extractor()
        entry = CombatLogEntry(
            tick=200,
            log_type="ITEM",
            attacker_name="npc_dota_hero_lina",
            inflictor_name="item_ward_sentry",
        )
        ext._on_combat_log(entry)
        assert len(ext._placements) == 1
        assert ext._placements[0].ward_type == "sentry"

    def test_dispenser_item_also_recorded(self):
        ext, _ = _ward_extractor()
        entry = CombatLogEntry(
            tick=50,
            log_type="ITEM",
            attacker_name="npc_dota_hero_axe",
            inflictor_name="item_ward_dispenser",
        )
        ext._on_combat_log(entry)
        assert len(ext._placements) == 1

    def test_non_ward_item_ignored(self):
        ext, _ = _ward_extractor()
        entry = CombatLogEntry(
            tick=100,
            log_type="ITEM",
            attacker_name="npc_dota_hero_axe",
            inflictor_name="item_blink",
        )
        ext._on_combat_log(entry)
        assert len(ext._placements) == 0

    def test_ward_death_recorded(self):
        ext, _ = _ward_extractor()
        entry = CombatLogEntry(
            tick=500,
            log_type="DEATH",
            target_name="npc_dota_observer_ward",
            attacker_name="npc_dota_hero_lina",
        )
        ext._on_combat_log(entry)
        assert len(ext._ward_deaths) == 1
        assert ext._ward_deaths[0] == (500, "npc_dota_hero_lina")

    def test_non_ward_death_ignored(self):
        ext, _ = _ward_extractor()
        entry = CombatLogEntry(
            tick=100,
            log_type="DEATH",
            target_name="npc_dota_hero_axe",
            attacker_name="npc_dota_hero_pudge",
        )
        ext._on_combat_log(entry)
        assert len(ext._ward_deaths) == 0


# ---------------------------------------------------------------------------
# WardsExtractor._on_entity — hero tracking
# ---------------------------------------------------------------------------


class TestOnEntityHero:
    def test_hero_registered(self):
        ext, _ = _ward_extractor()
        e = _ent("CDOTA_Unit_Hero_Axe")
        ext._on_entity(e, EntityOp.CREATED)
        assert "npc_dota_hero_axe" in ext._heroes_by_npc

    def test_hero_removed_on_deleted(self):
        ext, _ = _ward_extractor()
        e = _ent("CDOTA_Unit_Hero_Axe")
        ext._on_entity(e, EntityOp.CREATED)
        ext._on_entity(e, EntityOp.DELETED)
        assert "npc_dota_hero_axe" not in ext._heroes_by_npc


# ---------------------------------------------------------------------------
# WardsExtractor._on_entity — ward entity spawn recording
# ---------------------------------------------------------------------------


class TestOnEntityWard:
    def test_observer_spawn_recorded_in_spawns(self):
        ext, parser = _ward_extractor(tick=100)
        e = _observer_entity(index=0, x=1280.0, y=2560.0)
        ext._on_entity(e, EntityOp.CREATED)
        assert len(ext._spawns) == 1
        tick, wt, team, x, y = ext._spawns[0]
        assert wt == "observer"
        assert tick == 100

    def test_sentry_spawn_recorded(self):
        ext, parser = _ward_extractor(tick=200)
        e = _sentry_entity(index=1, x=3840.0, y=5120.0)
        ext._on_entity(e, EntityOp.CREATED)
        assert len(ext._spawns) == 1
        assert ext._spawns[0][1] == "sentry"

    def test_deleted_cleans_lifestate(self):
        ext, parser = _ward_extractor(tick=100)
        e = _observer_entity(index=5)
        ext._prev_lifestate[5] = 0
        ext._on_entity(e, EntityOp.DELETED)
        assert 5 not in ext._prev_lifestate

    def test_no_pos_entity_not_added_to_spawns(self):
        ext, _ = _ward_extractor(tick=100)
        # Observer ward but no position fields
        e = _ent("CDOTA_NPC_Observer_Ward", index=0, **{"m_lifeState": 0, "m_iTeamNum": 2})
        ext._on_entity(e, EntityOp.CREATED)
        assert len(ext._spawns) == 0

    def test_death_tick_recorded_on_lifestate_transition(self):
        from gem.extractors.wards import _SpawnState

        ext, parser = _ward_extractor(tick=100)
        # Create a spawn history entry
        state = _SpawnState(spawn_tick=100, ward_type="observer", team=2, x=0.0, y=0.0)
        ext._slot_history[0] = [state]
        ext._prev_lifestate[0] = 0  # was alive

        # Now entity updates with lifeState=1 (dying)
        e = _ent(
            "CDOTA_NPC_Observer_Ward",
            index=0,
            **{
                "m_lifeState": 1,
                "m_iTeamNum": 2,
                "CBodyComponent.m_cellX": 10,
                "CBodyComponent.m_cellY": 10,
                "CBodyComponent.m_vecX": 0.0,
                "CBodyComponent.m_vecY": 0.0,
            },
        )
        parser.tick = 500
        ext._on_entity(e, EntityOp.UPDATED)
        assert state.death_tick == 500


# ---------------------------------------------------------------------------
# WardsExtractor._find_spawn_state
# ---------------------------------------------------------------------------


class TestFindSpawnState:
    def test_returns_closest_match(self):
        from gem.extractors.wards import _SpawnState

        ext, _ = _ward_extractor()
        s1 = _SpawnState(spawn_tick=100, ward_type="observer", team=2, x=1.0, y=2.0)
        s2 = _SpawnState(spawn_tick=110, ward_type="observer", team=2, x=3.0, y=4.0)
        ext._slot_history[0] = [s1, s2]
        result = ext._find_spawn_state("observer", 112)
        assert result is s2

    def test_returns_none_when_no_match_within_window(self):
        from gem.extractors.wards import _SpawnState

        ext, _ = _ward_extractor()
        s = _SpawnState(spawn_tick=100, ward_type="observer", team=2, x=1.0, y=2.0)
        ext._slot_history[0] = [s]
        result = ext._find_spawn_state("observer", 300)  # 200 ticks away > window
        assert result is None

    def test_type_filter_applied(self):
        from gem.extractors.wards import _SpawnState

        ext, _ = _ward_extractor()
        s = _SpawnState(spawn_tick=100, ward_type="sentry", team=3, x=1.0, y=2.0)
        ext._slot_history[0] = [s]
        result = ext._find_spawn_state("observer", 100)  # looking for observer
        assert result is None


# ---------------------------------------------------------------------------
# WardsExtractor._find_killer
# ---------------------------------------------------------------------------


class TestFindKiller:
    def test_finds_closest_killer(self):
        ext, _ = _ward_extractor()
        # lina at 495 (dt=5), axe at 502 (dt=2) — axe is strictly closer
        ext._ward_deaths = [(495, "npc_dota_hero_lina"), (502, "npc_dota_hero_axe")]
        assert ext._find_killer(500) == "npc_dota_hero_axe"

    def test_returns_empty_when_no_match(self):
        ext, _ = _ward_extractor()
        ext._ward_deaths = [(600, "npc_dota_hero_lina")]
        assert ext._find_killer(100) == ""

    def test_exact_tick_match(self):
        ext, _ = _ward_extractor()
        ext._ward_deaths = [(300, "npc_dota_hero_pudge")]
        assert ext._find_killer(300) == "npc_dota_hero_pudge"


# ---------------------------------------------------------------------------
# WardsExtractor.finalize / ward_events
# ---------------------------------------------------------------------------


class TestFinalize:
    def test_empty_returns_empty(self):
        ext, _ = _ward_extractor()
        events = ext.finalize()
        assert events == []

    def test_ward_events_property_triggers_finalize(self):
        ext, _ = _ward_extractor()
        assert ext._finalized is None
        events = ext.ward_events
        assert ext._finalized is not None
        assert events == []

    def test_ward_events_cached(self):
        ext, _ = _ward_extractor()
        e1 = ext.ward_events
        e2 = ext.ward_events
        assert e1 is e2

    def test_placement_with_matching_spawn(self):
        ext, parser = _ward_extractor(tick=100)
        # Record a combat log placement
        entry = CombatLogEntry(
            tick=100,
            log_type="ITEM",
            attacker_name="npc_dota_hero_axe",
            inflictor_name="item_ward_observer",
        )
        ext._on_combat_log(entry)
        # Record matching spawn
        e = _observer_entity(index=0, x=1280.0, y=2560.0)
        ext._on_entity(e, EntityOp.CREATED)

        events = ext.finalize()
        assert len(events) == 1
        ev = events[0]
        assert ev.tick == 100
        assert ev.ward_type == "observer"
        assert ev.placer == "npc_dota_hero_axe"
        assert ev.x is not None
        assert ev.y is not None

    def test_placement_without_spawn_has_none_coords(self):
        ext, _ = _ward_extractor()
        entry = CombatLogEntry(
            tick=500,
            log_type="ITEM",
            attacker_name="npc_dota_hero_pudge",
            inflictor_name="item_ward_sentry",
        )
        ext._on_combat_log(entry)
        events = ext.finalize()
        assert len(events) == 1
        assert events[0].x is None
        assert events[0].y is None

    def test_events_sorted_by_tick(self):
        ext, parser = _ward_extractor()
        for tick in [300, 100, 200]:
            parser.tick = tick
            ext._on_combat_log(
                CombatLogEntry(
                    tick=tick,
                    log_type="ITEM",
                    attacker_name="npc_dota_hero_axe",
                    inflictor_name="item_ward_observer",
                )
            )
        events = ext.finalize()
        ticks = [e.tick for e in events]
        assert ticks == sorted(ticks)


# ---------------------------------------------------------------------------
# WardsExtractor._make_event — player_id and team resolution
# ---------------------------------------------------------------------------


class TestMakeEvent:
    def test_player_id_resolved_from_hero(self):
        ext, _ = _ward_extractor()
        hero = _ent("CDOTA_Unit_Hero_Axe", **{"m_nPlayerID": 4, "m_iTeamNum": 2})
        ext._heroes_by_npc["npc_dota_hero_axe"] = hero

        wp = _placement(100, placer="npc_dota_hero_axe")
        ev = ext._make_event(wp, coord=None, spawn=None)
        assert ev.player_id == 2  # 4 // 2
        assert ev.team == 2

    def test_player_id_minus_one_when_hero_not_found(self):
        ext, _ = _ward_extractor()
        wp = _placement(100, placer="npc_dota_hero_unknown")
        ev = ext._make_event(wp, coord=None, spawn=None)
        assert ev.player_id == -1
        assert ev.team == 0

    def test_coords_from_coord_tuple(self):
        ext, _ = _ward_extractor()
        wp = _placement(100)
        ev = ext._make_event(wp, coord=(1500.0, 2500.0), spawn=None)
        assert ev.x == 1500.0
        assert ev.y == 2500.0

    def test_coords_none_when_no_coord(self):
        ext, _ = _ward_extractor()
        wp = _placement(100)
        ev = ext._make_event(wp, coord=None, spawn=None)
        assert ev.x is None
        assert ev.y is None

    def test_natural_expiry_detected(self):
        from gem.extractors.wards import _SpawnState

        ext, _ = _ward_extractor()
        # Observer ward lasts 720 ticks; if death_tick >= spawn_tick + 690 → natural
        spawn = _SpawnState(spawn_tick=100, ward_type="observer", team=2, x=0.0, y=0.0)
        spawn.death_tick = 100 + 720  # exactly natural
        wp = _placement(100)
        ev = ext._make_event(wp, coord=None, spawn=spawn)
        assert ev.expires_tick == 820
        assert ev.killed_tick is None

    def test_killed_detected(self):
        from gem.extractors.wards import _SpawnState

        ext, _ = _ward_extractor()
        ext._ward_deaths = [(200, "npc_dota_hero_lina")]
        spawn = _SpawnState(spawn_tick=100, ward_type="observer", team=2, x=0.0, y=0.0)
        spawn.death_tick = 200  # well before natural expiry (100 + 690)
        wp = _placement(100)
        ev = ext._make_event(wp, coord=None, spawn=spawn)
        assert ev.killed_tick == 200
        assert ev.expires_tick is None
        assert ev.killer == "npc_dota_hero_lina"

    def test_no_death_tick_both_none(self):
        from gem.extractors.wards import _SpawnState

        ext, _ = _ward_extractor()
        spawn = _SpawnState(spawn_tick=100, ward_type="observer", team=2, x=0.0, y=0.0)
        # death_tick remains None (ward still alive)
        wp = _placement(100)
        ev = ext._make_event(wp, coord=None, spawn=spawn)
        assert ev.expires_tick is None
        assert ev.killed_tick is None
