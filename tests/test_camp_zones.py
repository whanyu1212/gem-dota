from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from gem.catalog import load_neutral_camps
from gem.catalog.map import load_camp_zones


def _zones() -> dict:
    return json.loads(Path("src/gem/data/camp_zones.json").read_text(encoding="utf-8"))


def test_camp_zones_reflect_confirmed_741_type_updates() -> None:
    zones = _zones()
    camp_types = {int(camp["id"]): camp["type"] for camp in zones["camps"]}

    assert zones["version"] == 4
    assert zones["dota_patch"] == "7.41"  # centres are the 7.41 replays' camp spawners
    assert zones["topology_patch"] == "7.41"
    assert len(zones["camps"]) == 28
    assert all(
        camp.get("topology", {}).get("lane") in {"top", "mid", "bot"} for camp in zones["camps"]
    )
    assert all(camp.get("topology", {}).get("area") for camp in zones["camps"])
    # Types follow the replays: each spawner's m_Type at creation and the creeps that
    # spawn there. Liquipedia's Neutral Creeps table still shows the older layout; its
    # changelog has the 7.40/7.41 demotions behind these: ancients by the stream ends
    # (5, 26) and large camps (6, 10, 20, 22) to medium, and the medium camps by the
    # offlane gates (2, 28) to small.
    assert camp_types[2] == "small"
    assert camp_types[5] == "medium"
    assert camp_types[6] == "medium"
    assert camp_types[10] == "medium"
    assert camp_types[20] == "medium"
    assert camp_types[22] == "medium"
    assert camp_types[26] == "medium"
    assert camp_types[28] == "small"


def test_each_side_owns_the_same_fourteen_camps() -> None:
    sides: dict[int, Counter[str]] = {2: Counter(), 3: Counter()}
    for camp in _zones()["camps"]:
        sides[camp["topology"]["owner_team"]][camp["type"]] += 1

    expected = Counter(small=2, medium=5, large=3, ancient=1, flooded_small=1, flooded_medium=2)
    assert sides == {2: expected, 3: expected}


def test_every_zone_uses_its_types_default_geometry() -> None:
    zones = _zones()
    defaults = zones["defaults_by_type"]
    assert {c["id"]: c["zone"] for c in zones["camps"]} == {
        c["id"]: defaults[c["type"]] for c in zones["camps"]
    }


def test_load_neutral_camps_is_a_view_of_camp_zones() -> None:
    assert load_neutral_camps() == [
        {"id": c["id"], "x": c["center"]["x"], "y": c["center"]["y"], "type": c["type"]}
        for c in load_camp_zones()["camps"]
    ]
