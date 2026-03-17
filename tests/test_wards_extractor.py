"""Unit tests for gem.extractors.wards (entity-based approach).

Covers WardsExtractor._on_combat_log (killer queues), _on_entity
(placement detection, death detection, hero tracking), finalize
(placer back-fill), and the public ward_events interface.
"""

from __future__ import annotations

from gem.combatlog import CombatLogEntry
from gem.entities import Entity, EntityOp
from gem.extractors.wards import (
    _EXPIRY_TOLERANCE_TICKS,
    _OBSERVER_LIFESPAN_TICKS,
    _SENTRY_LIFESPAN_TICKS,
    WardsExtractor,
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
    index: int = 0, x: float = 1280.0, y: float = 2560.0, life_state: int = 0, team: int = 2
) -> Entity:
    cell_x = int(x) // 128
    vec_x = x - cell_x * 128
    cell_y = int(y) // 128
    vec_y = y - cell_y * 128
    return _ent(
        "CDOTA_NPC_Observer_Ward",
        index=index,
        **{
            "m_lifeState": life_state,
            "m_iTeamNum": team,
            "CBodyComponent.m_cellX": cell_x,
            "CBodyComponent.m_cellY": cell_y,
            "CBodyComponent.m_vecX": float(vec_x),
            "CBodyComponent.m_vecY": float(vec_y),
        },
    )


def _sentry_entity(
    index: int = 1, x: float = 3840.0, y: float = 5120.0, life_state: int = 0, team: int = 3
) -> Entity:
    cell_x = int(x) // 128
    vec_x = x - cell_x * 128
    cell_y = int(y) // 128
    vec_y = y - cell_y * 128
    return _ent(
        "CDOTA_NPC_Observer_Ward_TrueSight",
        index=index,
        **{
            "m_lifeState": life_state,
            "m_iTeamNum": team,
            "CBodyComponent.m_cellX": cell_x,
            "CBodyComponent.m_cellY": cell_y,
            "CBodyComponent.m_vecX": float(vec_x),
            "CBodyComponent.m_vecY": float(vec_y),
        },
    )


class FakeParser:
    def __init__(self, tick: int = 0):
        self.tick = tick
        self._cl_handlers = []
        self._ent_handlers = []
        self.entity_manager = None

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
# _on_combat_log — killer queues
# ---------------------------------------------------------------------------


class TestOnCombatLogKillerQueue:
    def test_ward_death_adds_to_killer_queue(self):
        ext, _ = _ward_extractor()
        entry = CombatLogEntry(
            tick=500,
            log_type="DEATH",
            target_name="npc_dota_observer_wards",
            attacker_name="npc_dota_hero_lina",
        )
        ext._on_combat_log(entry)
        assert ext._killer_queue["npc_dota_observer_wards"] == ["npc_dota_hero_lina"]

    def test_sentry_death_uses_sentry_queue(self):
        ext, _ = _ward_extractor()
        entry = CombatLogEntry(
            tick=500,
            log_type="DEATH",
            target_name="npc_dota_sentry_wards",
            attacker_name="npc_dota_hero_axe",
        )
        ext._on_combat_log(entry)
        assert ext._killer_queue["npc_dota_sentry_wards"] == ["npc_dota_hero_axe"]

    def test_non_ward_death_ignored(self):
        ext, _ = _ward_extractor()
        entry = CombatLogEntry(
            tick=100,
            log_type="DEATH",
            target_name="npc_dota_hero_axe",
            attacker_name="npc_dota_hero_pudge",
        )
        ext._on_combat_log(entry)
        assert ext._killer_queue["npc_dota_observer_wards"] == []
        assert ext._killer_queue["npc_dota_sentry_wards"] == []

    def test_empty_killer_not_queued(self):
        ext, _ = _ward_extractor()
        entry = CombatLogEntry(
            tick=500,
            log_type="DEATH",
            target_name="npc_dota_observer_wards",
            attacker_name="",
        )
        ext._on_combat_log(entry)
        assert ext._killer_queue["npc_dota_observer_wards"] == []

    def test_item_events_ignored(self):
        ext, _ = _ward_extractor()
        entry = CombatLogEntry(
            tick=100,
            log_type="ITEM",
            target_name="npc_dota_observer_wards",
            attacker_name="npc_dota_hero_axe",
            inflictor_name="item_ward_observer",
        )
        ext._on_combat_log(entry)
        assert ext._killer_queue["npc_dota_observer_wards"] == []


# ---------------------------------------------------------------------------
# _on_entity — hero tracking
# ---------------------------------------------------------------------------


class TestOnEntityHeroTracking:
    def test_hero_player_id_recorded(self):
        ext, _ = _ward_extractor()
        e = _ent("CDOTA_Unit_Hero_Axe", **{"m_nPlayerID": 4, "m_iTeamNum": 2})
        ext._on_entity(e, EntityOp.CREATED)
        assert ext._hero_by_player_id[2] == "npc_dota_hero_axe"

    def test_hero_fallback_to_m_iPlayerID(self):
        ext, _ = _ward_extractor()
        e = _ent("CDOTA_Unit_Hero_Lina", **{"m_iPlayerID": 6, "m_iTeamNum": 2})
        ext._on_entity(e, EntityOp.CREATED)
        assert ext._hero_by_player_id[3] == "npc_dota_hero_lina"

    def test_non_hero_entity_not_tracked(self):
        ext, _ = _ward_extractor()
        e = _ent("CDOTAGamerulesProxy")
        ext._on_entity(e, EntityOp.CREATED)
        assert ext._hero_by_player_id == {}


# ---------------------------------------------------------------------------
# _on_entity — ward placement detection
# ---------------------------------------------------------------------------


class TestOnEntityWardPlacement:
    def test_created_with_lifestate_0_adds_event(self):
        ext, parser = _ward_extractor(tick=100)
        e = _observer_entity(index=0, x=1280.0, y=2560.0, life_state=0)
        ext._on_entity(e, EntityOp.CREATED)
        assert len(ext.ward_events) == 1
        ev = ext.ward_events[0]
        assert ev.tick == 100
        assert ev.ward_type == "observer"
        assert ev.x == 1280.0
        assert ev.y == 2560.0
        assert ev.team == 2

    def test_sentry_entity_detected(self):
        ext, parser = _ward_extractor(tick=200)
        e = _sentry_entity(index=1)
        ext._on_entity(e, EntityOp.CREATED)
        assert len(ext.ward_events) == 1
        assert ext.ward_events[0].ward_type == "sentry"

    def test_lifestate_transition_to_0_adds_event(self):
        """UPDATED event with m_lifeState changing from 2 → 0 should register as placement."""
        ext, parser = _ward_extractor(tick=50)
        e_alive = _observer_entity(index=0, life_state=0)
        # Simulate: previous state was non-zero (default prev=2)
        ext._on_entity(e_alive, EntityOp.UPDATED)
        assert len(ext.ward_events) == 1

    def test_no_event_if_already_alive(self):
        """UPDATED event with m_lifeState staying at 0 should NOT add another placement."""
        ext, parser = _ward_extractor(tick=50)
        e = _observer_entity(index=0, life_state=0)
        ext._on_entity(e, EntityOp.CREATED)  # first spawn
        ext._on_entity(e, EntityOp.UPDATED)  # another update, still life_state=0
        assert len(ext.ward_events) == 1  # still only one

    def test_deleted_cleans_lifestate(self):
        ext, parser = _ward_extractor(tick=100)
        e = _observer_entity(index=5)
        ext._prev_lifestate[5] = 0
        ext._on_entity(e, EntityOp.DELETED)
        assert 5 not in ext._prev_lifestate
        assert 5 not in ext._active

    def test_no_pos_entity_no_coords(self):
        """Ward with missing position fields still creates event but with None coords."""
        ext, _ = _ward_extractor(tick=100)
        e = _ent("CDOTA_NPC_Observer_Ward", index=0, **{"m_lifeState": 0, "m_iTeamNum": 2})
        ext._on_entity(e, EntityOp.CREATED)
        assert len(ext.ward_events) == 1
        assert ext.ward_events[0].x is None
        assert ext.ward_events[0].y is None


# ---------------------------------------------------------------------------
# _on_entity — ward death detection
# ---------------------------------------------------------------------------


class TestOnEntityWardDeath:
    def test_death_sets_killed_tick(self):
        ext, parser = _ward_extractor(tick=100)
        # Place a ward
        e = _observer_entity(index=0, x=1280.0, y=2560.0)
        ext._on_entity(e, EntityOp.CREATED)
        assert len(ext.ward_events) == 1

        # Add a killer to the queue
        death_entry = CombatLogEntry(
            tick=200,
            log_type="DEATH",
            target_name="npc_dota_observer_wards",
            attacker_name="npc_dota_hero_lina",
        )
        ext._on_combat_log(death_entry)

        # Ward transitions to dying (m_lifeState=1)
        parser.tick = 200
        e_dying = _observer_entity(index=0, life_state=1)
        ext._on_entity(e_dying, EntityOp.UPDATED)

        ev = ext.ward_events[0]
        assert ev.killed_tick == 200
        assert ev.killer == "npc_dota_hero_lina"
        assert ev.expires_tick is None

    def test_natural_expiry_sets_expires_tick(self):
        ext, parser = _ward_extractor(tick=100)
        e = _observer_entity(index=0, x=1280.0, y=2560.0)
        ext._on_entity(e, EntityOp.CREATED)

        # No killer in queue; die at natural lifespan
        natural_death_tick = 100 + _OBSERVER_LIFESPAN_TICKS
        parser.tick = natural_death_tick
        e_dying = _observer_entity(index=0, life_state=1)
        ext._on_entity(e_dying, EntityOp.UPDATED)

        ev = ext.ward_events[0]
        assert ev.expires_tick == natural_death_tick
        assert ev.killed_tick is None

    def test_early_death_without_killer_sets_killed_tick(self):
        ext, parser = _ward_extractor(tick=100)
        e = _observer_entity(index=0, x=1280.0, y=2560.0)
        ext._on_entity(e, EntityOp.CREATED)

        # Die early (50 ticks), no killer in queue
        parser.tick = 150
        e_dying = _observer_entity(index=0, life_state=1)
        ext._on_entity(e_dying, EntityOp.UPDATED)

        ev = ext.ward_events[0]
        assert ev.killed_tick == 150
        assert ev.expires_tick is None
        assert ev.killer == ""

    def test_slot_reuse_second_spawn_independent(self):
        """Same entity slot used twice — two separate WardEvents."""
        ext, parser = _ward_extractor(tick=100)
        e1 = _observer_entity(index=0, x=1280.0, y=2560.0, life_state=0)
        ext._on_entity(e1, EntityOp.CREATED)

        # Ward dies
        parser.tick = 200
        e_dying = _observer_entity(index=0, life_state=1)
        ext._on_entity(e_dying, EntityOp.UPDATED)

        # Same slot reused: new spawn
        parser.tick = 300
        e2 = _observer_entity(index=0, x=3840.0, y=5120.0, life_state=0)
        ext._on_entity(e2, EntityOp.UPDATED)  # transition 1 → 0

        assert len(ext.ward_events) == 2
        assert ext.ward_events[0].tick == 100
        assert ext.ward_events[1].tick == 300


# ---------------------------------------------------------------------------
# finalize — placer back-fill
# ---------------------------------------------------------------------------


class TestFinalize:
    def test_empty_returns_empty(self):
        ext, _ = _ward_extractor()
        events = ext.finalize()
        assert events == []

    def test_back_fills_placer_for_known_player_id(self):
        ext, parser = _ward_extractor(tick=100)
        # Ward placed pre-game: player_id resolved from controller but placer unknown
        e = _observer_entity(index=0, x=1280.0, y=2560.0)
        # No m_hOwnerEntity → player_id=-1 initially; manually set for test
        ext._on_entity(e, EntityOp.CREATED)
        ev = ext.ward_events[0]
        ev.player_id = 2  # simulate resolution from CDOTAPlayerController
        ev.placer = ""

        # Hero seen later in game
        hero_e = _ent("CDOTA_Unit_Hero_Axe", **{"m_nPlayerID": 4, "m_iTeamNum": 2})
        ext._on_entity(hero_e, EntityOp.UPDATED)

        ext.finalize()
        assert ev.placer == "npc_dota_hero_axe"

    def test_no_back_fill_when_player_id_unknown(self):
        ext, parser = _ward_extractor(tick=100)
        e = _observer_entity(index=0, x=1280.0, y=2560.0)
        ext._on_entity(e, EntityOp.CREATED)
        ev = ext.ward_events[0]
        ev.player_id = -1
        ev.placer = ""

        hero_e = _ent("CDOTA_Unit_Hero_Axe", **{"m_nPlayerID": 4, "m_iTeamNum": 2})
        ext._on_entity(hero_e, EntityOp.UPDATED)

        ext.finalize()
        assert ev.placer == ""  # player_id=-1, no fill

    def test_finalize_returns_ward_events(self):
        ext, parser = _ward_extractor(tick=100)
        e = _observer_entity(index=0)
        ext._on_entity(e, EntityOp.CREATED)
        result = ext.finalize()
        assert result is ext.ward_events
        assert len(result) == 1


# ---------------------------------------------------------------------------
# Ward lifespan named constants
# ---------------------------------------------------------------------------


class TestWardLifespanConstants:
    def test_values(self):
        assert _OBSERVER_LIFESPAN_TICKS == 720
        assert _SENTRY_LIFESPAN_TICKS == 360
        assert _EXPIRY_TOLERANCE_TICKS == 30

    def test_observer_longer_than_sentry(self):
        assert _OBSERVER_LIFESPAN_TICKS > _SENTRY_LIFESPAN_TICKS


# ---------------------------------------------------------------------------
# WardsExtractor.attach
# ---------------------------------------------------------------------------


class TestWardsExtractorAttach:
    def test_attach_registers_both_callbacks(self):
        ext = WardsExtractor()
        parser = FakeParser()
        ext.attach(parser)
        assert len(parser._cl_handlers) == 1
        assert len(parser._ent_handlers) == 1


# ---------------------------------------------------------------------------
# Same-tick ordering: entity callback fires before combat log callback
# ---------------------------------------------------------------------------


class TestSameTickOrderingFix:
    """Regression tests for the same-tick killer attribution bug.

    When a ward is killed, the entity m_lifeState→1 callback fires before
    the combat log DEATH callback at the same tick.  Without the back-fill
    logic, _on_ward_left would see an empty killer queue and mark the ward
    as killed with killer="" (displayed as "?").

    After the fix, _on_combat_log checks for ward_events with killed_tick==
    entry.tick and back-fills the killer directly.
    """

    def test_sentry_killer_backfilled_when_combat_log_arrives_after_lifestate(self):
        """Entity callback fires first (tick=500), then combat log arrives — back-fill."""
        ext, parser = _ward_extractor(tick=400)
        # Place sentry at tick 400
        e = _sentry_entity(index=1, x=3840.0, y=5120.0, life_state=0, team=3)
        ext._on_entity(e, EntityOp.CREATED)
        assert len(ext.ward_events) == 1

        # Entity dies at tick 500 (lifestate→1 callback fires first)
        parser.tick = 500
        e_dying = _sentry_entity(index=1, life_state=1)
        ext._on_entity(e_dying, EntityOp.UPDATED)

        # Ward marked as killed but no killer yet
        ev = ext.ward_events[0]
        assert ev.killed_tick == 500
        assert ev.killer == ""

        # Combat log DEATH arrives at same tick 500 (fires after entity callback)
        death_entry = CombatLogEntry(
            tick=500,
            log_type="DEATH",
            target_name="npc_dota_sentry_wards",
            attacker_name="npc_dota_hero_bane",
        )
        ext._on_combat_log(death_entry)

        # Back-fill: killer is now set
        assert ev.killed_tick == 500
        assert ev.killer == "npc_dota_hero_bane"
        # Queue should remain empty (back-fill consumed it)
        assert ext._killer_queue["npc_dota_sentry_wards"] == []

    def test_observer_killer_backfilled_same_tick(self):
        """Same-tick back-fill works for observer wards too."""
        ext, parser = _ward_extractor(tick=100)
        e = _observer_entity(index=0, x=1280.0, y=2560.0, life_state=0, team=2)
        ext._on_entity(e, EntityOp.CREATED)

        parser.tick = 300
        e_dying = _observer_entity(index=0, life_state=1)
        ext._on_entity(e_dying, EntityOp.UPDATED)

        death_entry = CombatLogEntry(
            tick=300,
            log_type="DEATH",
            target_name="npc_dota_observer_wards",
            attacker_name="npc_dota_hero_axe",
        )
        ext._on_combat_log(death_entry)

        ev = ext.ward_events[0]
        assert ev.killer == "npc_dota_hero_axe"
        assert ext._killer_queue["npc_dota_observer_wards"] == []

    def test_different_tick_still_uses_queue(self):
        """If combat log arrives at a different tick, it goes to the queue as normal."""
        ext, parser = _ward_extractor(tick=100)
        e = _observer_entity(index=0, life_state=0)
        ext._on_entity(e, EntityOp.CREATED)

        # Combat log arrives at tick 250, before the lifestate transition
        death_entry = CombatLogEntry(
            tick=250,
            log_type="DEATH",
            target_name="npc_dota_observer_wards",
            attacker_name="npc_dota_hero_lina",
        )
        ext._on_combat_log(death_entry)
        assert ext._killer_queue["npc_dota_observer_wards"] == ["npc_dota_hero_lina"]

        # Ward dies at tick 300 — consumes from queue
        parser.tick = 300
        e_dying = _observer_entity(index=0, life_state=1)
        ext._on_entity(e_dying, EntityOp.UPDATED)

        ev = ext.ward_events[0]
        assert ev.killed_tick == 300
        assert ev.killer == "npc_dota_hero_lina"

    def test_same_tick_natural_expiry_via_combat_log(self):
        """If the 'killer' in the combat log is the ward itself, it's natural expiry."""
        ext, parser = _ward_extractor(tick=100)
        e = _sentry_entity(index=1, life_state=0)
        ext._on_entity(e, EntityOp.CREATED)

        # Lifestate→1 fires first, marks as killed with no killer
        parser.tick = 300
        e_dying = _sentry_entity(index=1, life_state=1)
        ext._on_entity(e_dying, EntityOp.UPDATED)
        ev = ext.ward_events[0]
        assert ev.killed_tick == 300

        # Combat log arrives with ward killing itself (natural expiry)
        death_entry = CombatLogEntry(
            tick=300,
            log_type="DEATH",
            target_name="npc_dota_sentry_wards",
            attacker_name="npc_dota_sentry_wards",  # ward killing itself
        )
        ext._on_combat_log(death_entry)

        # Should be reclassified as natural expiry
        assert ev.killed_tick is None
        assert ev.expires_tick == 300
        assert ev.killer == ""
