from __future__ import annotations

import json
from pathlib import Path

import pytest

import scripts.export_site_home_data as export
from gem.catalog.map import load_camp_zones
from gem.combat.log import CombatLogEntry
from gem.extractors.fights import Fight, FightPlayer
from gem.extractors.wards import WardEvent
from gem.results.models import BuybackEvent, ParsedMatch, ParsedPlayer
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
    monkeypatch.setattr(export, "write_icons", lambda *args: None)
    data, playback, image = tmp_path / "home.json", tmp_path / "fight.json", tmp_path / "map.jpg"
    args = ["replay.dem", "--data", str(data), "--fight-data", str(playback)]
    assert export.main([*args, "--map-image", str(image)]) == 0
    assert json.loads(playback.read_text()) is None
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


def test_write_icons_copies_the_items_it_has_and_skips_the_rest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    items, heroes = tmp_path / "items", tmp_path / "heroes"
    items.mkdir()
    heroes.mkdir()
    for name in ("ward_observer", "ward_sentry", "black_king_bar"):
        (items / f"{name}.png").write_bytes(b"png")
    monkeypatch.setattr(export, "ITEM_ICONS", items)
    monkeypatch.setattr(export, "HERO_ICONS", heroes)
    out = tmp_path / "site-icons"
    (out / "items").mkdir(parents=True)
    (out / "items" / "stale.png").write_bytes(b"old match")

    export.write_icons(out, set(), {"black_king_bar", "not_downloaded"})

    assert [p.name for p in (out / "items").iterdir()] == ["black_king_bar.png"]


def test_unit_and_disable_names() -> None:
    assert export._unit_name("npc_dota_hero_nevermore") == "Shadow Fiend"
    assert export._unit_name("npc_dota_creep_badguys_ranged") == "Creep dire ranged"
    assert export._disable_name("modifier_lion_voodoo") == "Hex"
    assert export._disable_name("modifier_tiny_avalanche_stun") == "Avalanche"
    assert export._disable_name("modifier_sheepstick_debuff") == "Scythe of Vyse"
    assert export._disable_name("modifier_bashed") == "Bash"


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


def _playback_match() -> ParsedMatch:
    """Tiny (Radiant) hits Lion (Dire) with Avalanche, Lion dies and buys back."""
    match = _fight_match()
    lion, tiny = match.players
    lion.team, tiny.team = 3, 2
    for player in (lion, tiny):
        player.times = [t for t, _, _ in player.position_log]
        player.hp_t = [500] * len(player.times)
        player.max_hp_t = [600] * len(player.times)
        player.mana_t = [100.4] * len(player.times)
        player.max_mana_t = [300.0] * len(player.times)
    lion.buybacks = [
        BuybackEvent(tick=200, player_slot=0, cost=831, net_worth=8000, cost_exact=True)
    ]
    tiny_name, lion_name = tiny.hero_name, lion.hero_name

    def entry(log_type: str, tick: int, **fields: object) -> CombatLogEntry:
        return CombatLogEntry(tick=tick, log_type=log_type, **fields)  # type: ignore[arg-type]

    match.combat_log = sorted(
        [
            *match.combat_log,
            # Blade Mail's reflect was on before the window opened: no ring.
            entry(
                "MODIFIER_REMOVE",
                30,
                attacker_name=lion_name,
                target_name=lion_name,
                inflictor_name="modifier_item_blade_mail_reflect",
            ),
            entry("ITEM", 90, attacker_name=tiny_name, inflictor_name="item_black_king_bar"),
            entry(
                "MODIFIER_ADD",
                91,
                attacker_name=tiny_name,
                damage_source_name=tiny_name,
                target_name=tiny_name,
                inflictor_name="modifier_black_king_bar_immune",
            ),
            entry("ABILITY", 150, attacker_name=tiny_name, inflictor_name="tiny_avalanche"),
            entry(
                "DAMAGE",
                160,
                attacker_name=tiny_name,
                damage_source_name=tiny_name,
                target_name=lion_name,
                inflictor_name="tiny_avalanche",
                damage_type="magical",
                value=312,
            ),
            entry(
                "MODIFIER_ADD",
                160,
                attacker_name=tiny_name,
                damage_source_name=tiny_name,
                target_name=lion_name,
                inflictor_name="modifier_tiny_avalanche_stun",
                stun_duration=1.2,
            ),
            entry("GOLD", 180, target_name=lion_name, value=-210, gold_reason=1),
            entry("GOLD", 180, target_name=tiny_name, value=326, gold_reason=12),
            entry("XP", 180, target_name=tiny_name, value=468, xp_reason=1),
        ],
        key=lambda e: e.tick,
    )
    return match


def test_fight_playback_indexes_heroes_and_carries_the_timeline() -> None:
    playback = export.fight_playback(_playback_match())
    assert playback is not None
    heroes = [hero["hero"] for hero in playback["heroes"]]
    assert heroes == ["Lion", "Tiny"]  # by player slot
    lion, tiny = 0, 1
    # The playback runs to two seconds past the last death (tick 270).
    assert playback["duration"] == 11.0
    first = playback["heroes"][lion]["runs"][0][0]
    assert first[0] == 0.0 and first[3:] == [500, 600, 100, 300]

    bkb, avalanche = playback["casts"]
    assert bkb == {
        "t": 3.0,
        "by": tiny,
        "what": "Black King Bar",
        "hits": [],
        "item": "black_king_bar",
        "self": True,
    }
    assert avalanche["what"] == "Avalanche"
    assert avalanche["hits"] == [[lion, 312, "magical", 1.2]]
    assert "item" not in avalanche and "self" not in avalanche

    assert playback["damage"] == [[5.3, tiny, lion, 312, "magical", 1, "Avalanche"]]
    assert playback["disables"] == [[5.3, lion, tiny, "Avalanche", 1.2]]
    assert playback["buffs"] == [[3.0, 11.0, tiny, "bkb"]]
    death = next(d for d in playback["deaths"] if d["victim"] == lion and not d["aegis"])
    assert (death["t"], death["killer"], death["gold_lost"]) == (6.0, tiny, 210)
    assert death["gold"] == [[tiny, 326]] and death["xp"] == [[tiny, 468]]
    assert death["recent"][0] == ["Tiny", "Avalanche", "magical", 312]
    assert death["recent_total"] == 312 and "tick_victims" not in death
    assert playback["buybacks"] == [[6.7, lion, 831]]


def test_fight_playback_is_none_without_fights() -> None:
    assert export.fight_playback(ParsedMatch(match_id=1)) is None


def test_fight_playback_puts_same_tick_rewards_on_one_death() -> None:
    match = _playback_match()
    lion, tiny = match.players
    match.combat_log = sorted(
        [
            *match.combat_log,
            CombatLogEntry(
                tick=180,
                log_type="DEATH",
                attacker_name=lion.hero_name,
                target_name=tiny.hero_name,
                target_is_hero=True,
            ),
        ],
        key=lambda e: e.tick,
    )
    playback = export.fight_playback(match)
    assert playback is not None
    on_tick = [d for d in playback["deaths"] if d["t"] == 6.0]
    assert [d["victim"] for d in on_tick] == [0, 1]
    assert all(d["tick_victims"] == [0, 1] for d in on_tick)
    # The tick's bounty and XP appear once, on its first death.
    assert on_tick[0]["gold"] == [[1, 326]] and on_tick[0]["xp"] == [[1, 468]]
    assert on_tick[1]["gold"] == [] and on_tick[1]["xp"] == []
