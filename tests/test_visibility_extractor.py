"""Focused tests for authoritative hero visibility extraction and querying."""

from __future__ import annotations

import json
from dataclasses import FrozenInstanceError
from types import SimpleNamespace

import pytest

import gem
from gem.analysis import entity_visibility_at, hero_visibility_at
from gem.extractors.visibility import VisibilityExtractor
from gem.results.dataframes import build_dataframes
from gem.results.models import (
    EntityVisibilityEvent,
    HeroVisibilityEvent,
    ParsedMatch,
    VisibilityState,
)
from gem.state.entities import Entity, EntityOp


class _Class:
    def __init__(self, name: str, class_id: int) -> None:
        self.name = name
        self.class_id = class_id
        self.serializer = None


_next_class_id = 1


def _entity(
    class_name: str,
    *,
    index: int = 0,
    serial: int = 0,
    class_id: int | None = None,
    npc: bool = False,
    **state: int,
) -> Entity:
    global _next_class_id
    if class_id is None:
        class_id = _next_class_id
        _next_class_id += 1
    entity = Entity(index=index, serial=serial, cls=_Class(class_name, class_id))
    if npc:
        state.setdefault("m_iDayTimeVisionRange", 1800)
    entity._state.update(state)
    return entity


class _StringTables:
    def __init__(self, table=None) -> None:
        self.table = table

    def get_by_name(self, _name: str):
        return self.table


class _Players:
    def __init__(self) -> None:
        self.heroes: dict[int, Entity] = {}

    def _canonical_hero_entity(self, player_id: int) -> Entity | None:
        return self.heroes.get(player_id)

    def _hero_aliases(self, class_name: str) -> tuple[str, str]:
        ending = class_name.removeprefix("CDOTA_Unit_Hero_").lower()
        name = f"npc_dota_hero_{ending}"
        return name, name


class _Parser:
    def __init__(self) -> None:
        self.tick = 0
        self.string_tables = _StringTables()
        self.entity_callback = None
        self.packet_callback = None

    def on_entity(self, callback) -> None:
        self.entity_callback = callback

    def _on_packet_end(self, callback) -> None:
        self.packet_callback = callback

    def entity(self, entity: Entity, op: EntityOp = EntityOp.UPDATED) -> None:
        assert self.entity_callback is not None
        self.entity_callback(entity, op)

    def packet_end(self, tick: int) -> None:
        assert self.packet_callback is not None
        self.tick = tick
        self.packet_callback(tick)


def _attached() -> tuple[VisibilityExtractor, _Players, _Parser]:
    players = _Players()
    parser = _Parser()
    extractor = VisibilityExtractor(players)  # type: ignore[arg-type]
    extractor.attach(parser)  # type: ignore[arg-type]
    return extractor, players, parser


def test_samples_bits_zero_63_and_64_at_packet_end() -> None:
    extractor, players, parser = _attached()
    players.heroes = {
        0: _entity("CDOTA_Unit_Hero_Axe", index=0),
        1: _entity("CDOTA_Unit_Hero_Lina", index=63),
        2: _entity("CDOTA_Unit_Hero_Puck", index=64),
    }
    radiant = _entity(
        "CDOTADataRadiant",
        **{
            "m_bNPCVisibleState.0000": (1 << 0) | (1 << 63),
            "m_bNPCVisibleState.0001": 0,
        },
    )
    dire = _entity(
        "CDOTADataDire",
        **{"m_bNPCVisibleState.0000": 0, "m_bNPCVisibleState.0001": 1},
    )

    parser.entity(radiant)
    parser.entity(dire)
    assert extractor.events == []
    parser.packet_end(100)

    assert [(event.radiant_state, event.dire_state) for event in extractor.events] == [
        (VisibilityState.VISIBLE, VisibilityState.HIDDEN),
        (VisibilityState.VISIBLE, VisibilityState.HIDDEN),
        (VisibilityState.HIDDEN, VisibilityState.VISIBLE),
    ]


@pytest.mark.parametrize(
    ("radiant_class", "dire_class"),
    [
        ("CDOTADataRadiant", "CDOTADataDire"),
        ("CDOTA_DataRadiant", "CDOTA_DataDire"),
    ],
)
def test_team_data_aliases_are_watched(radiant_class: str, dire_class: str) -> None:
    extractor, players, parser = _attached()
    players.heroes[0] = _entity("CDOTA_Unit_Hero_Axe", index=3)
    parser.entity(_entity(radiant_class, **{"m_bNPCVisibleState.0000": 1 << 3}))
    parser.entity(_entity(dire_class, **{"m_bNPCVisibleState.0000": 0}))
    parser.packet_end(5)

    assert extractor.events[0].radiant_state is VisibilityState.VISIBLE
    assert extractor.events[0].dire_state is VisibilityState.HIDDEN
    assert parser.entity_callback is not None


def test_missing_team_or_word_is_unknown_never_hidden() -> None:
    extractor, players, parser = _attached()
    players.heroes[0] = _entity("CDOTA_Unit_Hero_Axe", index=64)
    parser.entity(_entity("CDOTADataRadiant", **{"m_bNPCVisibleState.0000": 0}))
    parser.packet_end(10)

    event = extractor.events[0]
    assert event.radiant_state is VisibilityState.UNKNOWN
    assert event.dire_state is VisibilityState.UNKNOWN


def test_team_data_packet_before_hero_creation_emits_when_hero_appears() -> None:
    extractor, players, parser = _attached()
    radiant = _entity("CDOTADataRadiant", **{"m_bNPCVisibleState.0000": 1 << 4})
    parser.entity(radiant)
    parser.packet_end(10)
    assert extractor.events == []

    hero = _entity("CDOTA_Unit_Hero_Axe", index=4)
    players.heroes[0] = hero
    parser.entity(hero, EntityOp.CREATED)
    parser.packet_end(11)

    assert len(extractor.events) == 1
    assert extractor.events[0].tick == 11
    assert extractor.events[0].radiant_state is VisibilityState.VISIBLE


def test_canonical_name_prefers_string_table_index_and_event_is_frozen() -> None:
    extractor, players, parser = _attached()
    parser.string_tables = _StringTables(
        SimpleNamespace(
            items={
                10: ("npc_dota_hero_queenofpain", b""),
                11: ("wrong_stringable_name", b""),
            }
        )
    )
    hero = _entity(
        "CDOTA_Unit_Hero_QueenOfPain",
        index=8,
        **{
            "m_pEntity.m_nameStringTableIndex": 10,
            "m_pEntity.m_nameStringableIndex": 11,
        },
    )
    players.heroes[0] = hero
    parser.entity(hero, EntityOp.CREATED)
    parser.packet_end(12)

    event = extractor.events[0]
    assert event.hero_name == "npc_dota_hero_queenofpain"
    with pytest.raises(FrozenInstanceError):
        event.tick = 13  # type: ignore[misc]


def test_visibility_state_has_plain_string_behavior() -> None:
    assert isinstance(VisibilityState.VISIBLE, str)
    assert VisibilityState.VISIBLE == "visible"
    assert str(VisibilityState.VISIBLE) == "visible"


def test_dedupes_unchanged_states_and_coalesces_same_tick_to_final_state() -> None:
    extractor, players, parser = _attached()
    players.heroes[0] = _entity("CDOTA_Unit_Hero_Axe", index=2)
    radiant = _entity("CDOTADataRadiant", **{"m_bNPCVisibleState.0000": 1 << 2})
    parser.entity(radiant)
    parser.packet_end(10)

    parser.entity(radiant)
    parser.packet_end(11)
    assert len(extractor.events) == 1

    radiant._state["m_bNPCVisibleState.0000"] = 0
    parser.entity(radiant)
    parser.packet_end(20)
    radiant._state["m_bNPCVisibleState.0000"] = 1 << 2
    parser.entity(radiant)
    parser.packet_end(20)

    assert [(event.tick, event.radiant_state) for event in extractor.events] == [
        (10, VisibilityState.VISIBLE)
    ]


def test_creation_deletion_and_slot_reuse_emit_identity_boundaries() -> None:
    extractor, players, parser = _attached()
    team = _entity("CDOTADataRadiant", **{"m_bNPCVisibleState.0000": 1 << 7})
    old = _entity("CDOTA_Unit_Hero_Axe", index=7, serial=1)
    players.heroes[0] = old
    parser.entity(team)
    parser.entity(old, EntityOp.CREATED)
    parser.packet_end(30)

    players.heroes.clear()
    parser.entity(old, EntityOp.DELETED)
    parser.packet_end(40)
    terminal = extractor.events[-1]
    assert (terminal.entity_index, terminal.entity_serial) == (7, 1)
    assert terminal.radiant_state is terminal.dire_state is VisibilityState.UNKNOWN

    replacement = _entity("CDOTA_Unit_Hero_Lina", index=7, serial=2)
    players.heroes[0] = replacement
    parser.entity(replacement, EntityOp.CREATED)
    parser.packet_end(40)
    initial = extractor.events[-1]
    assert (initial.entity_index, initial.entity_serial) == (7, 2)
    assert initial.hero_name == "npc_dota_hero_lina"
    assert initial.radiant_state is VisibilityState.VISIBLE


def test_same_tick_identity_churn_back_to_original_has_no_stale_terminal() -> None:
    extractor, players, parser = _attached()
    team = _entity("CDOTADataRadiant", **{"m_bNPCVisibleState.0000": 1 << 7})
    original = _entity("CDOTA_Unit_Hero_Axe", index=7, serial=1)
    replacement = _entity("CDOTA_Unit_Hero_Lina", index=8, serial=2)
    players.heroes[0] = original
    parser.entity(team)
    parser.entity(original, EntityOp.CREATED)
    parser.packet_end(30)

    players.heroes[0] = replacement
    parser.entity(original, EntityOp.DELETED)
    parser.entity(replacement, EntityOp.CREATED)
    parser.packet_end(40)

    players.heroes[0] = original
    parser.entity(replacement, EntityOp.DELETED)
    parser.entity(original, EntityOp.CREATED)
    parser.packet_end(40)

    match = ParsedMatch(hero_visibility_events=extractor.events)
    assert [(event.tick, event.entity_index) for event in extractor.events] == [(30, 7)]
    assert (
        hero_visibility_at(match, player_id=0, observing_team=2, tick=40) is VisibilityState.VISIBLE
    )


def test_query_json_dataframe_and_public_exports() -> None:
    events = [
        HeroVisibilityEvent(
            tick=10,
            player_id=0,
            hero_name="npc_dota_hero_axe",
            entity_index=7,
            entity_serial=1,
            radiant_state=VisibilityState.VISIBLE,
            dire_state=VisibilityState.HIDDEN,
        ),
        HeroVisibilityEvent(
            tick=20,
            player_id=0,
            hero_name="npc_dota_hero_axe",
            entity_index=7,
            entity_serial=1,
            radiant_state=VisibilityState.UNKNOWN,
            dire_state=VisibilityState.UNKNOWN,
        ),
    ]
    match = ParsedMatch(hero_visibility_events=events)

    assert (
        hero_visibility_at(match, player_id=0, observing_team=2, tick=9) is VisibilityState.UNKNOWN
    )
    assert (
        hero_visibility_at(match, player_id=0, observing_team=2, tick=10) is VisibilityState.VISIBLE
    )
    assert (
        hero_visibility_at(match, player_id=0, observing_team=3, tick=10) is VisibilityState.HIDDEN
    )
    assert (
        hero_visibility_at(match, player_id=0, observing_team=2, tick=99) is VisibilityState.UNKNOWN
    )
    with pytest.raises(ValueError, match="observing_team"):
        hero_visibility_at(match, player_id=0, observing_team=4, tick=10)

    assert gem.to_dict(match)["hero_visibility_events"][0]["radiant_state"] == "visible"
    assert json.loads(gem.to_json(match))["hero_visibility_events"][0]["radiant_state"] == "visible"
    dataframe = build_dataframes(match)["hero_visibility_events"]
    assert dataframe.loc[0, "dire_state"] == "hidden"
    assert gem.HeroVisibilityEvent is HeroVisibilityEvent
    assert gem.VisibilityState is VisibilityState
    assert gem.hero_visibility_at is hero_visibility_at


def test_same_tick_query_uses_last_matching_event() -> None:
    match = ParsedMatch(
        hero_visibility_events=[
            HeroVisibilityEvent(10, 0, "axe", 1, 0, VisibilityState.HIDDEN, VisibilityState.HIDDEN),
            HeroVisibilityEvent(
                10, 0, "axe", 1, 0, VisibilityState.VISIBLE, VisibilityState.HIDDEN
            ),
        ]
    )
    assert (
        hero_visibility_at(match, player_id=0, observing_team=2, tick=10) is VisibilityState.VISIBLE
    )


def test_query_reflects_public_timeline_mutations() -> None:
    match = ParsedMatch(
        hero_visibility_events=[
            HeroVisibilityEvent(10, 0, "axe", 1, 0, VisibilityState.HIDDEN, VisibilityState.HIDDEN)
        ]
    )
    assert (
        hero_visibility_at(match, player_id=0, observing_team=2, tick=20) is VisibilityState.HIDDEN
    )

    match.hero_visibility_events.append(
        HeroVisibilityEvent(20, 0, "axe", 1, 0, VisibilityState.VISIBLE, VisibilityState.HIDDEN)
    )
    assert (
        hero_visibility_at(match, player_id=0, observing_team=2, tick=20) is VisibilityState.VISIBLE
    )

    match.hero_visibility_events[-1] = HeroVisibilityEvent(
        20, 0, "axe", 1, 0, VisibilityState.HIDDEN, VisibilityState.HIDDEN
    )
    assert (
        hero_visibility_at(match, player_id=0, observing_team=2, tick=20) is VisibilityState.HIDDEN
    )

    match.hero_visibility_events = [
        HeroVisibilityEvent(20, 0, "axe", 1, 0, VisibilityState.VISIBLE, VisibilityState.HIDDEN)
    ]
    assert (
        hero_visibility_at(match, player_id=0, observing_team=2, tick=20) is VisibilityState.VISIBLE
    )


def test_entity_timeline_covers_npc_schema_across_class_names_and_visibility_words() -> None:
    extractor, _players, parser = _attached()
    parser.string_tables = _StringTables(
        SimpleNamespace(
            items={
                1: ("npc_dota_hero_axe", b""),
                2: ("npc_dota_observer_wards", b""),
                3: ("npc_dota_creep_goodguys_melee", b""),
                4: ("npc_dota_goodguys_tower1_mid", b""),
                5: ("npc_dota_unprefixed_test", b""),
            }
        )
    )
    radiant = _entity(
        "CDOTADataRadiant",
        **{
            "m_bNPCVisibleState.0000": (1 << 0) | (1 << 63),
            "m_bNPCVisibleState.0001": 1,
            "m_bNPCVisibleState.0002": 1 << 2,
        },
    )
    dire = _entity(
        "CDOTADataDire",
        **{
            "m_bNPCVisibleState.0000": 0,
            "m_bNPCVisibleState.0001": 1 << 1,
            "m_bNPCVisibleState.0002": 0,
        },
    )
    entities = [
        _entity(
            "CDOTA_Unit_Hero_Axe",
            index=0,
            npc=True,
            **{"m_pEntity.m_nameStringTableIndex": 1, "m_iTeamNum": 2},
        ),
        _entity(
            "CDOTA_NPC_Observer_Ward",
            index=63,
            npc=True,
            **{"m_pEntity.m_nameStringableIndex": 2, "m_iTeamNum": 2},
        ),
        _entity(
            "CDOTA_BaseNPC_Creep_Lane",
            index=64,
            npc=True,
            **{"m_pEntity.m_nameStringTableIndex": 3, "m_iTeamNum": 2},
        ),
        _entity(
            "CDOTA_BaseNPC_Tower",
            index=65,
            npc=True,
            **{"m_pEntity.m_nameStringTableIndex": 4, "m_iTeamNum": 3},
        ),
        _entity(
            "CompletelyNonstandardNetworkClass",
            index=130,
            npc=True,
            **{"m_pEntity.m_nameStringTableIndex": 5, "m_iTeamNum": 4},
        ),
    ]
    non_npc = _entity("CDOTAPlayerController", index=9)

    parser.entity(radiant)
    parser.entity(dire)
    for entity in entities:
        parser.entity(entity, EntityOp.CREATED_ENTERED)
    parser.entity(non_npc, EntityOp.CREATED_ENTERED)
    parser.packet_end(100)

    assert [event.entity_index for event in extractor.entity_events] == [0, 63, 64, 65, 130]
    assert [event.npc_name for event in extractor.entity_events] == [
        "npc_dota_hero_axe",
        "npc_dota_observer_wards",
        "npc_dota_creep_goodguys_melee",
        "npc_dota_goodguys_tower1_mid",
        "npc_dota_unprefixed_test",
    ]
    assert [(event.radiant_state, event.dire_state) for event in extractor.entity_events] == [
        (VisibilityState.VISIBLE, VisibilityState.HIDDEN),
        (VisibilityState.VISIBLE, VisibilityState.HIDDEN),
        (VisibilityState.VISIBLE, VisibilityState.HIDDEN),
        (VisibilityState.HIDDEN, VisibilityState.VISIBLE),
        (VisibilityState.VISIBLE, VisibilityState.HIDDEN),
    ]


def test_npc_classification_is_cached_by_class_id_and_name_falls_back_to_class() -> None:
    extractor, _players, parser = _attached()
    first = _entity("OddNpc", index=1, class_id=700, npc=True, m_iTeamNum=3)
    second = _entity("OddNpc", index=2, class_id=700, m_iTeamNum=3)
    parser.entity(first, EntityOp.CREATED_ENTERED)
    parser.entity(second, EntityOp.CREATED_ENTERED)
    parser.packet_end(10)

    assert len(extractor.entity_events) == 2
    assert extractor.entity_events[1].class_name == "OddNpc"
    assert extractor.entity_events[1].npc_name == "OddNpc"
    assert extractor.entity_events[1].team == 3


def test_entity_missing_team_or_visibility_word_is_unknown() -> None:
    extractor, _players, parser = _attached()
    npc = _entity("CDOTA_BaseNPC_Creep", index=64, npc=True)
    parser.entity(_entity("CDOTADataRadiant", **{"m_bNPCVisibleState.0000": 0}))
    parser.entity(npc, EntityOp.CREATED_ENTERED)
    parser.packet_end(10)

    event = extractor.entity_events[0]
    assert event.team is None
    assert event.radiant_state is VisibilityState.UNKNOWN
    assert event.dire_state is VisibilityState.UNKNOWN


def test_entity_lifecycle_leave_enter_delete_and_same_tick_slot_reuse() -> None:
    extractor, _players, parser = _attached()
    parser.entity(_entity("CDOTADataRadiant", **{"m_bNPCVisibleState.0000": 1 << 7}))
    old = _entity("CDOTA_BaseNPC_Creep", index=7, serial=1, npc=True, m_iTeamNum=2)
    parser.entity(old, EntityOp.CREATED_ENTERED)
    parser.packet_end(10)

    old.active = False
    parser.entity(old, EntityOp.LEFT)
    parser.packet_end(20)
    assert extractor.entity_events[-1].active is False
    assert extractor.entity_events[-1].radiant_state is VisibilityState.UNKNOWN

    old.active = True
    parser.entity(old, EntityOp.UPDATED_ENTERED)
    parser.packet_end(30)
    assert extractor.entity_events[-1].active is True
    assert extractor.entity_events[-1].radiant_state is VisibilityState.VISIBLE

    parser.entity(old, EntityOp.DELETED_LEFT)
    parser.packet_end(40)
    replacement = _entity("CDOTA_NPC_Observer_Ward", index=7, serial=2, npc=True, m_iTeamNum=2)
    parser.entity(replacement, EntityOp.CREATED_ENTERED)
    parser.packet_end(40)

    at_reuse_tick = [event for event in extractor.entity_events if event.tick == 40]
    assert [(event.entity_serial, event.active) for event in at_reuse_tick] == [
        (1, False),
        (2, True),
    ]


def test_entity_visibility_changes_coalesce_to_final_same_tick_state() -> None:
    extractor, _players, parser = _attached()
    team = _entity("CDOTADataRadiant", **{"m_bNPCVisibleState.0000": 0})
    npc = _entity("CDOTA_BaseNPC_Creep", index=2, npc=True)
    parser.entity(team)
    parser.entity(npc, EntityOp.CREATED_ENTERED)
    parser.packet_end(10)

    team._state["m_bNPCVisibleState.0000"] = 1 << 2
    parser.entity(team)
    parser.packet_end(20)
    team._state["m_bNPCVisibleState.0000"] = 0
    parser.entity(team)
    parser.packet_end(20)

    assert [(event.tick, event.radiant_state) for event in extractor.entity_events] == [
        (10, VisibilityState.HIDDEN)
    ]


def test_new_entity_created_and_deleted_same_tick_has_no_net_event() -> None:
    extractor, _players, parser = _attached()
    npc = _entity("CDOTA_BaseNPC_Creep", index=2, serial=7, npc=True)

    parser.entity(npc, EntityOp.CREATED_ENTERED)
    parser.packet_end(20)
    parser.entity(npc, EntityOp.DELETED_LEFT)
    parser.packet_end(20)

    assert extractor.entity_events == []


class _CountingEntity(Entity):
    def __init__(self, class_name: str) -> None:
        global _next_class_id
        super().__init__(index=0, serial=0, cls=_Class(class_name, _next_class_id))
        _next_class_id += 1
        self.reads: list[str] = []

    def _get_uint64_resolved(self, field) -> int | None:
        self.reads.append(field.name)
        return super()._get_uint64_resolved(field)


def test_visibility_words_are_read_once_per_team_and_occupied_word() -> None:
    extractor, _players, parser = _attached()
    radiant = _CountingEntity("CDOTADataRadiant")
    dire = _CountingEntity("CDOTADataDire")
    radiant._state.update(
        {"m_bNPCVisibleState.0000": (1 << 1) | (1 << 2), "m_bNPCVisibleState.0001": 1}
    )
    dire._state.update({"m_bNPCVisibleState.0000": 0, "m_bNPCVisibleState.0001": 0})
    parser.entity(radiant)
    parser.entity(dire)
    for index in (1, 2, 64):
        parser.entity(_entity("NPC", index=index, class_id=800, npc=True), EntityOp.CREATED_ENTERED)
    parser.packet_end(10)

    assert radiant.reads == ["m_bNPCVisibleState.0000", "m_bNPCVisibleState.0001"]
    assert dire.reads == ["m_bNPCVisibleState.0000", "m_bNPCVisibleState.0001"]


def test_ordinary_npc_updates_do_not_resample_unchanged_visibility() -> None:
    extractor, _players, parser = _attached()
    radiant = _CountingEntity("CDOTADataRadiant")
    radiant._state["m_bNPCVisibleState.0000"] = 1 << 2
    npc = _entity("NPC", index=2, npc=True, m_iTeamNum=2)
    parser.entity(radiant)
    parser.entity(npc, EntityOp.CREATED_ENTERED)
    parser.packet_end(10)
    radiant.reads.clear()

    npc._state["m_iHealth"] = 500
    parser.entity(npc, EntityOp.UPDATED)
    parser.packet_end(20)

    assert radiant.reads == []
    assert len(extractor.entity_events) == 1


def test_entity_metadata_changes_emit_transition_without_visibility_change() -> None:
    extractor, _players, parser = _attached()
    npc = _entity("NPC", index=2, npc=True, m_iTeamNum=2)
    parser.entity(npc, EntityOp.CREATED_ENTERED)
    parser.packet_end(10)

    npc._state["m_iTeamNum"] = 3
    parser.entity(npc, EntityOp.UPDATED)
    parser.packet_end(20)

    assert [(event.tick, event.team) for event in extractor.entity_events] == [(10, 2), (20, 3)]


def test_entity_query_serial_terminal_metadata_serialization_and_exports() -> None:
    events = [
        EntityVisibilityEvent(
            tick=10,
            entity_index=7,
            entity_serial=1,
            class_name="CDOTA_NPC_Observer_Ward",
            npc_name="npc_dota_observer_wards",
            team=2,
            active=True,
            radiant_state=VisibilityState.VISIBLE,
            dire_state=VisibilityState.HIDDEN,
        ),
        EntityVisibilityEvent(
            tick=20,
            entity_index=7,
            entity_serial=1,
            class_name="CDOTA_NPC_Observer_Ward",
            npc_name="npc_dota_observer_wards",
            team=2,
            active=False,
            radiant_state=VisibilityState.UNKNOWN,
            dire_state=VisibilityState.UNKNOWN,
        ),
        EntityVisibilityEvent(
            tick=20,
            entity_index=7,
            entity_serial=2,
            class_name="CDOTA_BaseNPC_Creep",
            npc_name="npc_dota_creep_badguys_melee",
            team=3,
            active=True,
            radiant_state=VisibilityState.HIDDEN,
            dire_state=VisibilityState.VISIBLE,
        ),
    ]
    match = ParsedMatch(entity_visibility_events=events)

    assert (
        entity_visibility_at(match, entity_index=7, entity_serial=1, observing_team=2, tick=10)
        is VisibilityState.VISIBLE
    )
    assert (
        entity_visibility_at(match, entity_index=7, entity_serial=1, observing_team=2, tick=20)
        is VisibilityState.UNKNOWN
    )
    assert (
        entity_visibility_at(match, entity_index=7, entity_serial=2, observing_team=3, tick=20)
        is VisibilityState.VISIBLE
    )
    with pytest.raises(ValueError, match="observing_team"):
        entity_visibility_at(match, entity_index=7, entity_serial=2, observing_team=4, tick=20)
    with pytest.raises(FrozenInstanceError):
        events[0].active = False  # type: ignore[misc]

    plain = gem.to_dict(match)["entity_visibility_events"]
    assert plain[0]["radiant_state"] == "visible"
    assert json.loads(gem.to_json(match))["entity_visibility_events"][1]["active"] is False
    dataframe = build_dataframes(match)["entity_visibility"]
    assert list(dataframe["entity_serial"]) == [1, 1, 2]
    assert dataframe.loc[2, "dire_state"] == "visible"
    assert gem.EntityVisibilityEvent is EntityVisibilityEvent
    assert gem.entity_visibility_at is entity_visibility_at


def test_entity_query_latest_same_tick_event_wins() -> None:
    common = {
        "tick": 10,
        "entity_index": 3,
        "entity_serial": 4,
        "class_name": "NPC",
        "npc_name": "npc",
        "team": None,
        "active": True,
        "dire_state": VisibilityState.HIDDEN,
    }
    match = ParsedMatch(
        entity_visibility_events=[
            EntityVisibilityEvent(radiant_state=VisibilityState.HIDDEN, **common),
            EntityVisibilityEvent(radiant_state=VisibilityState.VISIBLE, **common),
        ]
    )
    assert (
        entity_visibility_at(match, entity_index=3, entity_serial=4, observing_team=2, tick=10)
        is VisibilityState.VISIBLE
    )
