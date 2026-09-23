from __future__ import annotations

import json
from pathlib import Path


def test_camp_zones_reflect_confirmed_741_type_updates() -> None:
    zones = json.loads(Path("src/gem/data/camp_zones.json").read_text(encoding="utf-8"))
    camp_types = {int(camp["id"]): camp["type"] for camp in zones["camps"]}

    assert zones["version"] == 1
    assert zones["dota_patch"] == "7.40"  # geometry baseline; types below include 7.41 updates
    assert camp_types[2] == "small"
    assert camp_types[5] == "medium"
    assert camp_types[6] == "medium"
    assert camp_types[20] == "medium"
    assert camp_types[22] == "medium"
    assert camp_types[26] == "medium"
    assert camp_types[28] == "small"
