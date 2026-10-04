from __future__ import annotations

import json
from pathlib import Path

import pytest

import scripts.export_site_home_data as export
from gem.catalog.map import load_camp_zones
from gem.combat.log import CombatLogEntry
from gem.extractors.fights import Fight, FightPlayer
from gem.extractors.wards import WardEvent
from gem.results.models import ParsedMatch, ParsedPlayer
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


def _fight_match(*, clock: object = None) -> ParsedMatch:
    """Two heroes; Lion dies twice (once to an Aegis), Tiny dies far from the paths."""
    lion = ParsedPlayer(player_id=0, hero_name="npc_dota_hero_lion", team=2)
    tiny = ParsedPlayer(player_id=5, hero_name="npc_dota_hero_tiny", team=3)
    # World coordinates (the map window spans about 7,500 to 26,000 on each axis).
    lion.position_log = [(t, 16000.0, 16000.0) for t in range(0, 301, 30)]
    tiny.position_log = [(t, 16100.0, 16000.0) for t in range(0, 241, 30)] + [
        (270, 21000.0, 16000.0)
    ]

    def death(tick: int, victim: str, *, reincarnates: bool = False) -> CombatLogEntry:
        return CombatLogEntry(
            tick=tick,
            log_type="DEATH",
            attacker_name="npc_dota_hero_tiny" if victim.endswith("lion") else "npc_dota_hero_lion",
            target_name=victim,
            target_is_hero=True,
            will_reincarnate=reincarnates,
        )

    match = ParsedMatch(
        match_id=1,
        players=[lion, tiny],
        fights=[
            Fight(
                start_tick=0,
                end_tick=300,
                last_death_tick=270,
                first_death_tick=120,
                deaths=2,
                centroid_x=16000.0,
                centroid_y=16000.0,
                players=[FightPlayer(player_id=0), FightPlayer(player_id=5)],
            )
        ],
        combat_log=[
            death(120, "npc_dota_hero_lion", reincarnates=True),
            death(180, "npc_dota_hero_lion"),
            death(270, "npc_dota_hero_tiny"),
        ],
    )
    match.game_clock = clock  # type: ignore[assignment]
    return match


def test_fight_leaves_out_reincarnation_triggers() -> None:
    fight = export.fight_snapshot(_fight_match())
    assert fight is not None
    kills = [event["text"] for event in fight["events"]]
    assert kills == ["Tiny killed Lion", "Lion killed Tiny"]
    assert len(fight["deaths_at"]) == 2


def test_fight_crop_contains_every_death() -> None:
    # Tiny dies 5,000 units from the centroid, beyond the paths that frame the fight.
    fight = export.fight_snapshot(_fight_match())
    assert fight is not None
    x, y, size = fight["box"]
    for death in fight["deaths_at"]:
        dx, dy = death["at"]
        assert x <= dx <= x + size and y <= dy <= y + size


class _PausedClock:
    """A game clock frozen for 60 ticks (2 s) from tick 60."""

    def game_time_at(self, tick: int) -> float:
        return (tick - max(0, min(tick, 120) - 60)) / 30

    def format_tick(self, tick: int) -> str:
        seconds = int(self.game_time_at(tick))
        return f"{seconds // 60}:{seconds % 60:02d}"


def test_fight_timing_skips_pauses() -> None:
    fight = export.fight_snapshot(_fight_match(clock=_PausedClock()))
    assert fight is not None
    # The death at tick 180 is 6 s of ticks after the start but 4 s of game time.
    assert [event["t"] for event in fight["events"]] == [4.0, 7.0]
    assert fight["duration_s"] == 7.0
