from __future__ import annotations

import json
from pathlib import Path

import pytest

import scripts.export_site_home_data as export
from gem.catalog.map import load_camp_zones
from gem.extractors.wards import WardEvent
from gem.results.models import ParsedMatch
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


def test_main_writes_to_paths_outside_the_repository(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(export, "load_match", lambda replay: ParsedMatch(match_id=1))
    # Icons are downloaded, not committed, so CI has none; copying them is tested below.
    monkeypatch.setattr(export, "write_icons", lambda icons_dir, heroes: None)
    data, image = tmp_path / "home.json", tmp_path / "map.jpg"
    assert export.main(["replay.dem", "--data", str(data), "--map-image", str(image)]) == 0
    written = json.loads(data.read_text())
    assert written["match"]["match_id"] == 1
    # No fights: no fight figure, and no wards up.
    assert written["fight"] is None
    assert written["wards"]["up"] == []
    assert image.stat().st_size > 0
    assert str(data) in capsys.readouterr().out


def _ward(
    kind: str, team: int, placed: int, gone: int | None, *, killed: bool = False
) -> WardEvent:
    return WardEvent(
        tick=placed,
        player_id=0,
        placer="npc_dota_hero_lion",
        ward_type=kind,  # type: ignore[arg-type]
        team=team,
        x=0.0,
        y=0.0,
        expires_tick=None if killed else gone,
        killed_tick=gone if killed else None,
        killer="",
    )


def test_wards_up_are_those_placed_and_not_yet_gone() -> None:
    match = ParsedMatch(
        match_id=1,
        wards=[
            _ward("observer", 2, placed=100, gone=500),  # up
            _ward("sentry", 3, placed=100, gone=200, killed=True),  # killed before
            _ward("observer", 3, placed=300, gone=900),  # placed at the moment: up
            _ward("sentry", 2, placed=301, gone=900),  # placed after
            _ward("observer", 2, placed=100, gone=300),  # expired at the moment: gone
        ],
    )
    snapshot = export.wards_snapshot(match, tick=300)
    assert [(w["type"], w["team"]) for w in snapshot["up"]] == [
        ("observer", "radiant"),
        ("observer", "dire"),
    ]
    # Observers carry their vision circle; sentries give no map vision.
    assert all("vision_radius" in w for w in snapshot["up"])
    assert snapshot["totals"] == {"observer": 3, "sentry": 2}
    assert export.wards_snapshot(match, tick=None)["up"] == []


def test_write_icons_copies_wards_and_the_fight_heroes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    items, heroes = tmp_path / "items", tmp_path / "heroes"
    items.mkdir()
    heroes.mkdir()
    for name in ("ward_observer", "ward_sentry"):
        (items / f"{name}.png").write_bytes(b"png")
    (heroes / "lion.png").write_bytes(b"lion")
    monkeypatch.setattr(export, "ITEM_ICONS", items)
    monkeypatch.setattr(export, "HERO_ICONS", heroes)
    out = tmp_path / "site-icons"
    (out / "heroes").mkdir(parents=True)
    (out / "heroes" / "stale.png").write_bytes(b"old match")

    export.write_icons(out, {"lion"})
    assert sorted(p.name for p in out.glob("*.png")) == ["ward_observer.png", "ward_sentry.png"]
    assert [p.name for p in (out / "heroes").iterdir()] == ["lion.png"]

    with pytest.raises(SystemExit, match="fetch_hero_icons"):
        export.write_icons(out, {"nevermore"})
