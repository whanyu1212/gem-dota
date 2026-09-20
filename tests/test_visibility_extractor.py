"""Focused tests for authoritative hero visibility extraction and querying."""

from __future__ import annotations

import json
from dataclasses import FrozenInstanceError
from types import SimpleNamespace

import pytest

import gem
from gem.analysis import hero_visibility_at
from gem.extractors.visibility import VisibilityExtractor
from gem.results.dataframes import build_dataframes
from gem.results.models import HeroVisibilityEvent, ParsedMatch, VisibilityState
from gem.state.entities import Entity, EntityOp


class _Class:
    def __init__(self, name: str) -> None:
        self.name = name
        self.class_id = 1
        self.serializer = None


def _entity(class_name: str, *, index: int = 0, serial: int = 0, **state: int) -> Entity:
    entity = Entity(index=index, serial=serial, cls=_Class(class_name))
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
        self.filters: dict[str, object] = {}

    def _on_entity_filtered(self, callback, **filters) -> None:
        self.entity_callback = callback
        self.filters = filters

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
    assert set(parser.filters["class_names"]) >= {
        "CDOTADataRadiant",
        "CDOTA_DataRadiant",
        "CDOTADataDire",
        "CDOTA_DataDire",
    }


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
    assert match._hero_visibility_index is not None
    assert "_hero_visibility_index" not in gem.to_dict(match)
