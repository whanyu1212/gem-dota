"""Camp zones sit on the replay's own neutral camp spawners.

Every 7.41 replay carries one ``CDOTA_NeutralSpawner`` entity per camp, at the
same position in every fixture, and neutral creeps spawn within about 100 units
of it. Positions are ``CBodyComponent`` cell * 128 + vec.

Reference: odota/parser Parse.java ``getPreciseLocation`` (pinned revision in
CLAUDE.md)
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import pytest

from gem.parser import ReplayParser
from gem.state.entities import Entity, EntityOp

_ZONES_PATH = Path("src/gem/data/camp_zones.json")
_CELL_SIZE = 128

# Spawner ``m_Type`` → the base camp type (flooded camps keep their size).
_SPAWNER_TYPES = {0: "small", 1: "medium", 2: "large", 3: "ancient"}
# Annotated types the spawner disagrees with, pending review (HY-83).
_KNOWN_TYPE_DIFFERENCES = {10: ("large", "medium")}


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
    assert differences == _KNOWN_TYPE_DIFFERENCES
