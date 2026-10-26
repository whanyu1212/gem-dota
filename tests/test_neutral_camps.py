"""Camp creeps and camp stacks (HY-150)."""

from __future__ import annotations

from collections import Counter
from types import SimpleNamespace

import pytest

import gem.extractors.neutral_camps as camps_module
from gem.catalog.map import load_neutral_camps
from gem.extractors.neutral_camps import (
    CampStack,
    NeutralCampExtractor,
    NeutralCreep,
    credit_stacks,
    resolve_killers,
)
from gem.state.entities import Entity, EntityOp
from tests._entities import set_fields

CREATED, UPDATED = EntityOp.CREATED, EntityOp.UPDATED
CAMP_A, CAMP_B = load_neutral_camps()[:2]
SPAWN = 1800 * 7


def _entity(class_name: str, index: int, fields: dict) -> Entity:
    entity = Entity(
        index=index, serial=1, cls=SimpleNamespace(name=class_name, class_id=1, serializer=None)
    )
    set_fields(entity, fields)
    return entity


class _Replay:
    """Feed entity updates to a NeutralCampExtractor at given ticks."""

    def __init__(self, monkeypatch: pytest.MonkeyPatch) -> None:
        self.parser = SimpleNamespace(tick=0)
        self.extractor = NeutralCampExtractor()
        self.extractor._parser = self.parser  # type: ignore[assignment]
        self.positions: dict[int, tuple[float, float]] = {}
        monkeypatch.setattr(camps_module, "_pos", lambda entity: self.positions[entity.index])

    def spawner(self, index: int, pos: tuple[float, float], camp_type: int) -> None:
        self.positions[index] = pos
        self.extractor._on_spawner(
            _entity("CDOTA_NeutralSpawner", index, {"m_Type": camp_type}), CREATED
        )

    def creep(self, index: int, spawner: int, spawned: int, died: int | None = None) -> None:
        entity = _entity(
            "CDOTA_BaseNPC_Creep_Neutral",
            index,
            {
                "m_hNeutralSpawner": (1 << 14) | spawner,
                "m_bIsWaitingToSpawn": True,
                "m_lifeState": 0,
            },
        )
        self.at(spawned - 30, entity, CREATED)
        set_fields(entity, {"m_bIsWaitingToSpawn": False})
        self.at(spawned, entity, UPDATED)
        if died is not None:
            set_fields(entity, {"m_lifeState": 1})
            self.at(died, entity, UPDATED)

    def at(self, tick: int, entity: Entity, op: EntityOp) -> None:
        self.parser.tick = tick
        self.extractor._on_creep(entity, op)


def test_stack_needs_an_earlier_wave_alive(monkeypatch: pytest.MonkeyPatch) -> None:
    replay = _Replay(monkeypatch)
    replay.spawner(500, (CAMP_A["x"], CAMP_A["y"]), camp_type=1)
    replay.spawner(501, (0.0, 0.0), camp_type=0)  # matches no catalogued camp
    replay.creep(1, 500, spawned=SPAWN - 1800, died=SPAWN)  # dies on the spawn tick: not alive
    replay.creep(2, 500, spawned=SPAWN - 1800)  # still alive: the camp stacks
    replay.creep(3, 500, spawned=SPAWN)
    replay.creep(4, 500, spawned=SPAWN + 1800)  # earlier waves still alive: stacks again
    replay.creep(5, 501, spawned=SPAWN)  # no earlier wave: no stack
    replay.parser.tick = SPAWN
    replay.extractor._on_creep(
        _entity("CDOTA_BaseNPC_Creep_Neutral", 6, {"m_hNeutralSpawner": 0xFFFFFF}), CREATED
    )  # not from a camp

    creeps, stacks = replay.extractor.finalize()

    assert Counter(creep.camp_id for creep in creeps) == {CAMP_A["id"]: 4, None: 1}
    assert stacks == [
        CampStack(
            tick=SPAWN, camp_id=CAMP_A["id"], camp_type="medium", creeps_before=1, waves_alive=2
        ),
        CampStack(
            tick=SPAWN + 1800,
            camp_id=CAMP_A["id"],
            camp_type="medium",
            creeps_before=2,
            waves_alive=3,
        ),
    ]


def test_counter_rises_become_credits() -> None:
    extractor = NeutralCampExtractor()
    extractor._parser = SimpleNamespace(tick=0)  # type: ignore[assignment]
    data = _entity("CDOTA_DataDire", 7, {"m_vecDataTeam.0002.m_iCampsStacked": 3})
    extractor._on_counters(data, CREATED)  # the first value is a baseline
    extractor._parser.tick = SPAWN
    set_fields(data, {"m_vecDataTeam.0002.m_iCampsStacked": 5})
    extractor._on_counters(data, UPDATED)

    assert [(c.tick, c.team, c.team_slot, c.camps) for c in extractor.credits] == [(SPAWN, 3, 2, 2)]


def _stack(camp: dict) -> CampStack:
    return CampStack(
        tick=SPAWN, camp_id=camp["id"], camp_type="medium", creeps_before=3, waves_alive=2
    )


def _near(camp: dict, seconds_before: int = 5) -> list[tuple[int, float, float]]:
    return [(SPAWN - seconds_before * 30, camp["x"] + 300.0, camp["y"])]


A, B = CAMP_A["id"], CAMP_B["id"]


@pytest.mark.parametrize(
    ("credits", "positions", "expected"),
    [
        # One player credited with every candidate: no position needed.
        ([(SPAWN, 4, 2)], {}, [(A, 4, True), (B, 4, True)]),
        # Two players, a camp each: matched by position.
        (
            [(SPAWN, 1, 1), (SPAWN, 6, 1)],
            {1: _near(CAMP_B), 6: _near(CAMP_A)},
            [(A, 6, False), (B, 1, False)],
        ),
        # The only sample is outside the 3-10 s window: credited, but unplaced.
        (
            [(SPAWN, 1, 1), (SPAWN, 6, 1)],
            {1: _near(CAMP_A, 1), 6: _near(CAMP_B)},
            [(A, None, False), (B, 6, False)],
        ),
        # One credit for two candidates: the other is an uncounted straggler.
        ([(SPAWN, 6, 1)], {6: _near(CAMP_B)}, [(B, 6, False)]),
        # No credit on the tick: no stack.
        ([], {}, []),
    ],
    ids=["one-player", "by-position", "stale-sample", "uncredited-straggler", "no-credit"],
)
def test_credited_stacks(credits, positions, expected) -> None:
    stacks = credit_stacks([_stack(CAMP_A), _stack(CAMP_B)], credits, positions)
    assert [(s.camp_id, s.player_id, s.player_exact) for s in stacks] == expected


def _death(tick: int, attacker: str) -> SimpleNamespace:
    return SimpleNamespace(
        log_type="DEATH",
        tick=tick,
        target_name="npc_dota_neutral_kobold",
        attacker_name=attacker,
        damage_source_name="",
    )


@pytest.mark.parametrize(
    ("deaths", "dying", "killer"),
    [
        ([_death(SPAWN, "npc_dota_hero_axe")] * 2, 2, ("npc_dota_hero_axe", 0)),
        (
            [_death(SPAWN, "npc_dota_creep_goodguys_melee")],
            1,
            ("npc_dota_creep_goodguys_melee", None),
        ),
        (
            [_death(SPAWN, "npc_dota_hero_axe"), _death(SPAWN, "npc_dota_hero_lina")],
            2,
            (None, None),
        ),
        ([_death(SPAWN, "npc_dota_hero_axe")], 2, (None, None)),
    ],
    ids=["one-hero", "pull", "two-attackers", "fewer-entries-than-deaths"],
)
def test_killers(deaths, dying, killer) -> None:
    creeps = [NeutralCreep(camp_id=1, spawned_tick=0, died_tick=SPAWN) for _ in range(dying)]
    heroes = {"npc_dota_hero_axe": 0, "npc_dota_hero_lina": 5}
    resolve_killers(creeps, deaths, lambda source, attacker: heroes.get(source or attacker))
    assert {(c.killer_name, c.killer_player_id) for c in creeps} == {killer}


@pytest.mark.slow
@pytest.mark.integration
@pytest.mark.parametrize(
    "match_fixture", ["canonical_parsed_match", "fixed8_encoder_match", "feature_parity_match"]
)
def test_stacks_equal_the_games_credits(match_fixture, request) -> None:
    match = request.getfixturevalue(match_fixture)
    credited = Counter(stack.player_id for stack in match.camp_stacks)
    assert credited == {p.player_id: p.camps_stacked for p in match.players if p.camps_stacked}
    # Flooded camps' creeps grow into their next form, recorded as deaths to their camp.
    flooded = {camp["id"] for camp in load_neutral_camps() if camp["type"].startswith("flooded")}
    died = [c for c in match.neutral_creeps if c.died_tick is not None and c.camp_id not in flooded]
    assert sum(creep.killer_name is not None for creep in died) > 0.9 * len(died)
    assert all(creep.camp_id is not None for creep in match.neutral_creeps)
