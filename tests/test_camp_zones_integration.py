"""Camp zones sit on the replay's own neutral camp spawners, with the game's types and owners.

Every 7.41 replay carries one ``CDOTA_NeutralSpawner`` entity per camp, at the
same position in every fixture, and neutral creeps spawn within about 100 units
of it. Positions are ``CBodyComponent`` cell * 128 + vec. The spawner's
``m_Type`` at creation is the camp's tier, and the combat log's
``neutral_camp_team`` on a neutral death is the team the game files the camp
under (neither pinned parser reads it; its meaning here is checked on the
fixtures: every death at a camp carries the same value).

Reference: odota/parser Parse.java ``getPreciseLocation`` (pinned revision in
CLAUDE.md)
"""

from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import pytest

from gem.combat.log import CombatLogEntry
from gem.parser import ReplayParser
from gem.state.entities import Entity, EntityOp

_ZONES_PATH = Path("src/gem/data/camp_zones.json")
_CELL_SIZE = 128

# Spawner ``m_Type`` → the base camp type (flooded camps keep their size).
_SPAWNER_TYPES = {0: "small", 1: "medium", 2: "large", 3: "ancient"}
# Camps whose owner_team differs from the game's neutral_camp_team. Camp 22 sits in
# Dire jungle and the catalog follows the terrain (14 camps a side, mirrored), but
# the game files it under Radiant.
_KNOWN_TEAM_DIFFERENCES = {22: (3, 2)}


def _spawners(replay_path: Path) -> list[tuple[float, float, int]]:
    parser = ReplayParser(str(replay_path))
    spawners: list[tuple[float, float, int]] = []

    def on_entity(entity: Entity, op: EntityOp) -> None:
        if not op.has(EntityOp.CREATED) or entity.get_class_name() != "CDOTA_NeutralSpawner":
            return
        x = entity.get("CBodyComponent.m_cellX") * _CELL_SIZE + entity.get("CBodyComponent.m_vecX")
        y = entity.get("CBodyComponent.m_cellY") * _CELL_SIZE + entity.get("CBodyComponent.m_vecY")
        spawners.append((x, y, entity.get("m_Type")))

    parser.on_entity(on_entity)
    parser.parse()
    assert parser.parse_error is None
    return spawners


@pytest.mark.integration
@pytest.mark.slow
def test_every_camp_zone_is_centred_on_its_spawner(ti2026_short_replay_path: Path) -> None:
    camps = json.loads(_ZONES_PATH.read_text(encoding="utf-8"))["camps"]
    spawners = _spawners(ti2026_short_replay_path)

    assert len(spawners) == len(camps) == 28
    matched: dict[int, tuple[float, float, int]] = {}
    for camp in camps:
        cx, cy = camp["center"]["x"], camp["center"]["y"]
        nearest = min(spawners, key=lambda s: math.hypot(s[0] - cx, s[1] - cy))
        assert math.hypot(nearest[0] - cx, nearest[1] - cy) <= 1.0, camp["id"]
        matched[camp["id"]] = nearest
    assert len(set(matched.values())) == 28

    differences = {
        camp["id"]: (camp["type"], _SPAWNER_TYPES[matched[camp["id"]][2]])
        for camp in camps
        if camp["type"].removeprefix("flooded_") != _SPAWNER_TYPES[matched[camp["id"]][2]]
    }
    assert differences == {}


def _game_camp_teams(replay_path: Path, centres: dict[int, tuple[float, float]]) -> dict[int, int]:
    """Majority ``neutral_camp_team`` per camp, from deaths joined to the creep that died.

    The combat log has no death position, so each neutral DEATH is matched to the
    one neutral creep whose ``m_lifeState`` left 0 on the same tick, and that
    creep's spawn position picks the camp.
    """
    parser = ReplayParser(str(replay_path))
    spawned: dict[int, tuple[float, float, float]] = {}  # index -> (create time, x, y)
    dead: set[int] = set()
    creep_deaths: defaultdict[int, list[tuple[float, float]]] = defaultdict(list)
    log_deaths: list[tuple[int, int]] = []

    def on_entity(entity: Entity, op: EntityOp) -> None:
        if entity.get_class_name() != "CDOTA_BaseNPC_Creep_Neutral":
            return
        created = entity.get("m_flCreateTime")
        known = spawned.get(entity.index)
        if known is None or known[0] != created:
            x = entity.get("CBodyComponent.m_cellX") * _CELL_SIZE + entity.get(
                "CBodyComponent.m_vecX"
            )
            y = entity.get("CBodyComponent.m_cellY") * _CELL_SIZE + entity.get(
                "CBodyComponent.m_vecY"
            )
            spawned[entity.index] = known = (created, x, y)
            dead.discard(entity.index)
        if entity.get("m_lifeState") not in (None, 0) and entity.index not in dead:
            dead.add(entity.index)
            creep_deaths[parser.tick].append((known[1], known[2]))

    def on_combat_log(entry: CombatLogEntry) -> None:
        if entry.log_type == "DEATH" and (entry.target_name or "").startswith("npc_dota_neutral_"):
            log_deaths.append((entry.tick, entry.neutral_camp_team))

    parser.on_entity(on_entity)
    parser.on_combat_log_entry(on_combat_log)
    parser.parse()
    assert parser.parse_error is None

    teams: defaultdict[int, Counter[int]] = defaultdict(Counter)
    for tick, team in log_deaths:
        creeps = creep_deaths.get(tick, [])
        if len(creeps) != 1 or not team:
            continue
        camp_id, distance = min(
            ((cid, math.dist(creeps[0], centre)) for cid, centre in centres.items()),
            key=lambda pair: pair[1],
        )
        if distance <= 600:
            teams[camp_id][team] += 1
    return {cid: counts.most_common(1)[0][0] for cid, counts in teams.items()}


@pytest.mark.integration
@pytest.mark.slow
def test_camp_owners_match_the_games_camp_team(ti2026_short_replay_path: Path) -> None:
    camps = json.loads(_ZONES_PATH.read_text(encoding="utf-8"))["camps"]
    centres = {camp["id"]: (camp["center"]["x"], camp["center"]["y"]) for camp in camps}
    game_teams = _game_camp_teams(ti2026_short_replay_path, centres)

    # Not every camp is farmed in a short game: 19 of 28 are on this replay. All 28
    # were checked across the 9 local fixtures when the owners were fixed (HY-85).
    assert len(game_teams) >= 15
    differences = {
        camp["id"]: (camp["topology"]["owner_team"], game_teams[camp["id"]])
        for camp in camps
        if camp["id"] in game_teams and camp["topology"]["owner_team"] != game_teams[camp["id"]]
    }
    expected = {cid: pair for cid, pair in _KNOWN_TEAM_DIFFERENCES.items() if cid in game_teams}
    assert differences == expected
