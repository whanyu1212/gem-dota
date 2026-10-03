from __future__ import annotations

from gem.catalog.map import load_camp_zones
from scripts.export_site_home_data import SIZE, map_overlay


def test_map_overlay_has_every_camp_and_both_lotus_pools() -> None:
    overlay = map_overlay()
    assert len(overlay["camps"]) == len(load_camp_zones()["camps"]) == 28
    assert len(overlay["lotus_pools"]) == 2
    assert {camp["type"] for camp in overlay["camps"]} <= {
        "small",
        "medium",
        "large",
        "ancient",
        "flooded_small",
        "flooded_medium",
    }


def test_map_overlay_points_fall_inside_the_square() -> None:
    overlay = map_overlay()
    points = [camp["at"] for camp in overlay["camps"]] + overlay["lotus_pools"] + overlay["river"]
    assert all(0 <= x <= SIZE and 0 <= y <= SIZE for x, y in points)


def test_map_overlay_puts_radiant_camps_below_dire_camps() -> None:
    # Radiant is the bottom-left half of the map; y grows downwards in the square.
    camps = load_camp_zones()["camps"]
    heights: dict[int, list[float]] = {2: [], 3: []}
    for camp, projected in zip(camps, map_overlay()["camps"], strict=True):
        heights[camp["topology"]["owner_team"]].append(projected["at"][1])
    mean = {team: sum(ys) / len(ys) for team, ys in heights.items()}
    assert mean[2] > mean[3]
