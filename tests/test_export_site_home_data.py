from __future__ import annotations

import json
import math
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
    ward_data = tmp_path / "wards" / "wards.json"  # a folder that doesn't exist yet
    args = ["replay.dem", "--data", str(data), "--fight-data", str(playback)]
    args += ["--wards-data", str(ward_data), "--public-figures", str(tmp_path / "figures")]
    args += [
        "--fights-data",
        str(tmp_path / "fights"),
        "--objectives-data",
        str(tmp_path / "objectives.json"),
        "--lead-data",
        str(tmp_path / "lead.json"),
        "--lanes-data",
        str(tmp_path / "lanes.json"),
    ]
    assert export.main([*args, "--map-image", str(image)]) == 0
    assert (tmp_path / "figures" / "map.webp").stat().st_size > 0
    assert (tmp_path / "figures" / "ward_sentry.png").is_file()
    assert json.loads((tmp_path / "fights" / "index.json").read_text())["fights"] == []
    assert json.loads((tmp_path / "objectives.json").read_text())["objectives"] == []
    assert json.loads((tmp_path / "lead.json").read_text())["times"] == []
    assert json.loads((tmp_path / "lanes.json").read_text())["events"] == []
    assert json.loads(playback.read_text()) is None
    assert json.loads(ward_data.read_text())["wards"] == []
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


def test_unit_and_modifier_names() -> None:
    assert export._unit_name("npc_dota_hero_nevermore") == "Shadow Fiend"
    assert export._unit_name("npc_dota_creep_badguys_ranged") == "Creep dire ranged"
    assert export._modifier_name("modifier_lion_voodoo") == "Hex"
    assert export._modifier_name("modifier_tiny_avalanche_stun") == "Avalanche"
    assert export._modifier_name("modifier_sheepstick_debuff") == "Scythe of Vyse"
    assert export._modifier_name("modifier_bashed") == "Bash"
    assert export._modifier_name("modifier_item_shivas_guard_blast") == "Shiva's Guard"
    assert export._modifier_name("modifier_nevermore_shadowraze_debuff") == "Shadowraze"


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
                modifier_duration_s=7.0,
            ),
            # Left out of the feed: an internal timer, and a short state of Tiny's own.
            entry(
                "MODIFIER_ADD",
                95,
                attacker_name=tiny_name,
                target_name=tiny_name,
                inflictor_name="modifier_tiny_avalanche_timer",
                modifier_duration_s=30.0,
            ),
            entry(
                "MODIFIER_ADD",
                96,
                attacker_name=tiny_name,
                target_name=tiny_name,
                inflictor_name="modifier_tiny_tree_grab",
                modifier_duration_s=0.5,
            ),
            # A debuff on Lion, removed a second later.
            entry(
                "MODIFIER_ADD",
                170,
                attacker_name=tiny_name,
                target_name=lion_name,
                inflictor_name="modifier_tiny_toss",
                modifier_duration_s=1.0,
            ),
            entry(
                "MODIFIER_REMOVE",
                200,
                attacker_name=tiny_name,
                target_name=lion_name,
                inflictor_name="modifier_tiny_toss",
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

    assert playback["damage"] == [[5.33, tiny, lion, 312, "magical", 1, "Avalanche"]]
    # [t, until, target, source, name, kind, ring, seconds]; still on at the end
    # runs to 11.0.
    assert playback["modifiers"] == [
        [3.03, 11.0, tiny, tiny, "Black King Bar", "buff", "bkb", 7.0],
        [5.33, 11.0, lion, tiny, "Avalanche", "disable", None, 1.2],
        [5.67, 6.67, lion, tiny, "Toss", "debuff", None, 1.0],
    ]
    death = next(d for d in playback["deaths"] if d["victim"] == lion and not d["aegis"])
    assert (death["t"], death["killer"], death["gold_lost"]) == (6.0, tiny, 210)
    assert death["gold"] == [[tiny, 326]] and death["xp"] == [[tiny, 468]]
    assert death["recent"][0] == ["Tiny", "Avalanche", "magical", 312]
    assert death["recent_total"] == 312 and "tick_victims" not in death
    assert playback["buybacks"] == [[6.67, lion, 831]]


def _state(tick: int, x: float, *, hp: int = 500, life: int = 0) -> export.HeroState:
    return (tick, x, 16000.0, hp, 600, 100.0, 300.0, life)


def _since(tick: int) -> float:
    return round(tick / 30, 2)


def test_hero_runs_break_at_a_blink_but_not_a_dash() -> None:
    walk = [_state(t, 16000.0 + t) for t in range(0, 11, 2)]
    blink = [_state(t, 17200.0 + t) for t in range(12, 17, 2)]  # one 1,200-unit jump
    dash = [_state(t, 17216.0 + (t - 16) * 750) for t in range(18, 23, 2)]  # 1,500 a packet
    runs = export._hero_runs(walk + blink + dash, 0, 100, _since)
    # The run breaks on the Blink's own packet, not a second later.
    assert [[sample[0] for sample in run][0] for run in runs] == [0.0, 0.4]
    assert runs[0][-1][0] == _since(10)
    assert runs[1][-1][0] == _since(22)  # the dash stays one path


def test_hero_runs_leave_out_the_dead_and_restart_after() -> None:
    states = [_state(0, 16000.0), _state(2, 16010.0, hp=0, life=1)]
    states += [_state(t, 16010.0, hp=0, life=2) for t in range(4, 31, 2)]
    states += [_state(32, 16020.0)]  # bought back where it died
    runs = export._hero_runs(states, 0, 100, _since)
    # Dying and dead have no samples: the hero is gone from the dying tick.
    assert [[sample[0] for sample in run] for run in runs] == [[0.0], [1.07]]


def test_hero_runs_restart_after_an_aegis() -> None:
    states = [_state(0, 16000.0), _state(2, 16000.0, hp=0, life=1)]
    states += [_state(t, 16000.0, hp=1200) for t in range(150, 155, 2)]  # reincarnated
    runs = export._hero_runs(states, 0, 200, _since)
    assert [run[0][0] for run in runs] == [0.0, 5.0]


def test_thin_handles_a_pause() -> None:
    # A pause freezes the clock: samples share a time while the state holds.
    samples = [[1.0, 100.0, 200.0, 500, 600, 50, 300]] * 3 + [
        [1.1, 101.0, 200.0, 500, 600, 50, 300]
    ]
    assert export._thin(samples)[0] == samples[0] and export._thin(samples)[-1] == samples[-1]


def test_thin_keeps_what_the_straight_lines_cannot_redraw() -> None:
    samples = [[t / 10, 100.0 + t, 200.0, 500, 600, 50, 300] for t in range(10)]
    # A straight walk is its two ends.
    assert export._thin(samples) == [samples[0], samples[-1]]
    hp = [500, 500, 500, 420, 420, 420, 431, 442, 453, 453]
    stepped = [[t / 10, 100.0, 200.0, h, 600, 50, 300] for t, h in enumerate(hp)]
    kept = export._thin(stepped)
    # The step stays one sample wide; the regen ramp is its two ends.
    assert [sample[0] for sample in kept] == [0.0, 0.2, 0.3, 0.5, 0.8, 0.9]
    # Every dropped sample is what the client's interpolation draws.
    for sample in stepped:
        a = max((k for k in kept if k[0] <= sample[0]), key=lambda k: k[0])
        b = min((k for k in kept if k[0] >= sample[0]), key=lambda k: k[0])
        f = 0.0 if a is b else (sample[0] - a[0]) / (b[0] - a[0])
        assert abs(a[3] + (b[3] - a[3]) * f - sample[3]) < 0.5


def test_fight_playback_draws_the_heroes_from_the_states_it_is_given() -> None:
    match = _playback_match()
    states = {
        0: [_state(t, 16000.0) for t in range(0, 61, 2)]
        + [_state(t, 17500.0) for t in range(62, 331, 2)],
    }
    playback = export.fight_playback(match, states)
    assert playback is not None
    lion_runs = playback["heroes"][0]["runs"]
    assert [run[0][0] for run in lion_runs] == [0.0, 2.07]
    assert playback["heroes"][1]["runs"] == []  # no states for Tiny


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


def test_fight_playback_starts_at_its_smoke_and_marks_who_the_enemy_couldnt_see(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from types import SimpleNamespace

    from gem.results.models import HeroVisibilityEvent, VisibilityState

    match = _playback_match()
    lion, tiny = match.players  # Lion Dire (slot 0), Tiny Radiant (slot 5)
    fight = match.fights[0]
    smoke = SimpleNamespace(
        activation_tick=-300,  # 10 s before the window opens at tick 0
        team=2,
        first_fight=fight,
        members=[SimpleNamespace(hero_name=tiny.hero_name, applied_tick=-300, removed_tick=60)],
    )
    monkeypatch.setattr(export.gem, "build_smoke_analysis", lambda m: [smoke])
    tiny.position_log = [(t, 16100.0, 16000.0) for t in range(-300, 241, 30)] + [
        (270, 21000.0, 16000.0)
    ]

    def seen(tick: int, dire: VisibilityState, slot: int = 5, name: str = tiny.hero_name):
        return HeroVisibilityEvent(
            tick=tick,
            player_id=slot,
            hero_name=name,
            entity_index=1,
            entity_serial=1,
            radiant_state=VisibilityState.VISIBLE,
            dire_state=dire,
        )

    match.hero_visibility_events = [
        seen(-400, VisibilityState.HIDDEN),  # hidden from Dire when the playback starts
        seen(75, VisibilityState.VISIBLE),  # seen half a second after the smoke breaks
        seen(150, VisibilityState.HIDDEN),
        seen(160, VisibilityState.VISIBLE),  # a third of a second: fog flicker, left out
    ]

    playback = export.fight_playback(match)
    assert playback is not None
    assert playback["start_s"] == -10.0 and playback["duration"] == 21.0
    tiny_i = 1  # by player slot: Lion 0, Tiny 5
    # Smoked from the start to the break at tick 60; Dire saw him 0.5 s later.
    assert playback["smokes"] == [["radiant", 0.0, [[tiny_i, 0.0, 12.0, 12.5]]]]
    assert playback["hidden"] == [[tiny_i, 0.0, 12.5]]
    # Clocks line up with the narration's window: the first death (tick 120) is 14 s in.
    assert [d["t"] for d in playback["deaths"]][:1] == [14.0]


def _smoked_tiny(
    monkeypatch: pytest.MonkeyPatch, *, activation: int = -300, removed: int | None = 60
) -> ParsedMatch:
    from types import SimpleNamespace

    match = _playback_match()
    tiny = match.players[1]
    smoke = SimpleNamespace(
        activation_tick=activation,
        team=2,
        first_fight=match.fights[0],
        members=[
            SimpleNamespace(hero_name=tiny.hero_name, applied_tick=activation, removed_tick=removed)
        ],
    )
    monkeypatch.setattr(export.gem, "build_smoke_analysis", lambda m: [smoke])
    tiny.position_log = [(t, 16100.0, 16000.0) for t in range(activation, 241, 30)]
    return match


def _visible_to_dire(tick: int, state: str, slot: int = 5) -> object:
    from gem.results.models import HeroVisibilityEvent, VisibilityState

    return HeroVisibilityEvent(
        tick=tick,
        player_id=slot,
        hero_name="npc_dota_hero_tiny",
        entity_index=1,
        entity_serial=1,
        radiant_state=VisibilityState.VISIBLE,
        dire_state=VisibilityState(state),
    )


def test_fight_playback_keeps_a_break_after_the_end_as_still_smoked(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # The window ends at tick 330 (last death 270 + 2 s); the smoke breaks at 900.
    match = _smoked_tiny(monkeypatch, removed=900)

    playback = export.fight_playback(match)

    assert playback is not None
    assert playback["smokes"] == [["radiant", 0.0, [[1, 0.0, None, None]]]]


def test_fight_playback_keeps_same_tick_visibility_in_the_extractors_order(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    match = _smoked_tiny(monkeypatch)
    # A terminal "unknown" then the replacement's "hidden", on one tick: hidden wins.
    match.hero_visibility_events = [
        _visible_to_dire(-400, "unknown"),  # type: ignore[list-item]
        _visible_to_dire(-400, "hidden"),  # type: ignore[list-item]
        _visible_to_dire(75, "visible"),  # type: ignore[list-item]
    ]

    playback = export.fight_playback(match)

    assert playback is not None
    assert playback["hidden"] == [[1, 0.0, 12.5]]


class _PauseBeforeTheFight:
    """A clock frozen for 20 s (ticks -1500 to -900), between a smoke and its fight."""

    def game_time_at(self, tick: int) -> float:
        if tick <= -1500:
            return tick / 30
        if tick <= -900:
            return -50.0
        return (tick - 600) / 30

    def game_seconds_at(self, tick: int) -> int:
        return math.floor(self.game_time_at(tick))

    def format_tick(self, tick: int) -> str:
        seconds = int(self.game_time_at(tick)) % 3600
        return f"{seconds // 60}:{seconds % 60:02d}"


def test_fight_playback_measures_the_smoke_lead_on_the_game_clock(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # 70 s of ticks before the window, but 50 s of game time: the smoke still counts.
    match = _smoked_tiny(monkeypatch, activation=-2100, removed=60)
    match.game_clock = _PauseBeforeTheFight()  # type: ignore[assignment]

    playback = export.fight_playback(match)

    assert playback is not None
    # -70 s plus half a tick, so the floor the playback takes is safe from rounding.
    assert playback["start_s"] == -69.9833
    assert playback["smokes"][0][1] == 0.0


class _OpenDotaClock:
    """Shows whole seconds the way OpenDota does: the raw seconds and the game
    start (here 0.4 s into a second) are rounded separately."""

    def game_time_at(self, tick: int) -> float:
        return tick / 30

    def game_seconds_at(self, tick: int) -> int:
        return math.floor(tick / 30 + 0.4 + 0.5) - math.floor(0.4 + 0.5)


def test_the_playback_clock_shows_gems_second_at_every_tick() -> None:
    match = ParsedMatch(match_id=1)
    clock = _OpenDotaClock()
    match.game_clock = clock  # type: ignore[assignment]
    start, end = 95, 400
    base = export._clock_base(match, start, end)
    since = export._seconds_since(match, start, places=2)
    # floor(start_s + t), as the playback's clockAt takes it.
    shown = [math.floor(base + since(tick) + 1e-6) for tick in range(start, end + 1)]
    assert shown == [clock.game_seconds_at(tick) for tick in range(start, end + 1)]
    # Here the second turns over at x.1 of the exact game time, not x.0.
    assert clock.game_time_at(122) < 4.1 <= clock.game_time_at(123)
    assert [math.floor(base + since(t) + 1e-6) for t in (122, 123)] == [4, 5]


def test_modifier_kinds() -> None:
    from gem.analysis.fight_timeline import ModifierWindow

    team = {"npc_dota_hero_lion": 2, "npc_dota_hero_tiny": 2, "npc_dota_hero_axe": 3}

    def kind(name: str, source: str | None, target: str, **fields: object) -> str | None:
        window = ModifierWindow(
            target=target,
            modifier=name,
            source=source or "",
            source_hero=source,
            start_tick=0,
            end_tick=30,
            duration_s=fields.get("duration_s", 3.0),  # type: ignore[arg-type]
            stun_s=fields.get("stun_s", 0.0),  # type: ignore[arg-type]
            aura=fields.get("aura", False),  # type: ignore[arg-type]
        )
        return export._modifier_kind(window, team)

    lion, tiny, axe = "npc_dota_hero_lion", "npc_dota_hero_tiny", "npc_dota_hero_axe"
    assert kind("modifier_tiny_avalanche_stun", tiny, axe, stun_s=1.2) == "disable"
    assert kind("modifier_lion_voodoo", lion, axe) == "disable"  # no stun time, still a hex
    assert kind("modifier_eul_cyclone", axe, lion) == "disable"  # Eul's on an enemy
    assert kind("modifier_eul_cyclone", lion, lion) == "buff"  # Eul's on yourself: a save
    assert kind("modifier_sniper_headshot_slow", lion, axe) == "debuff"
    assert kind("modifier_treant_living_armor", tiny, lion) == "buff"
    # Left out: timers, auras, no duration, a short state of one's own, no hero source.
    assert kind("modifier_ember_spirit_fire_remnant_timer", lion, lion) is None
    assert kind("modifier_item_assault_positive", lion, tiny, aura=True) is None
    assert kind("modifier_tiny_tree_grab", tiny, tiny, duration_s=None) is None
    assert kind("modifier_pangolier_swashbuckle", tiny, tiny, duration_s=0.5) is None
    assert kind("modifier_creep_slow", None, lion) is None
    # The log's -1 means "no duration": not a duration, unless it's a disable.
    assert kind("modifier_tiny_toss", tiny, axe, duration_s=-1.0) is None
    assert kind("modifier_lion_voodoo", lion, axe, duration_s=-1.0) == "disable"


def test_applied_seconds_ignores_the_no_duration_sentinel() -> None:
    from gem.analysis.fight_timeline import ModifierWindow

    def window(duration: float | None, stun: float = 0.0) -> ModifierWindow:
        return ModifierWindow("t", "m", "s", "s", 0, 30, duration_s=duration, stun_s=stun)

    assert export._applied_seconds(window(3.0)) == 3.0
    assert export._applied_seconds(window(-1.0)) == 0.0
    assert export._applied_seconds(window(None)) == 0.0
    assert export._applied_seconds(window(-1.0, stun=1.2)) == 1.2


def test_wards_recipe_lists_every_ward_with_how_it_ended() -> None:
    lion = ParsedPlayer(player_id=0, hero_name="npc_dota_hero_ancient_apparition", team=2)

    def ward(tick: int, **end: object) -> WardEvent:
        return WardEvent(
            tick=tick,
            player_id=0,
            placer="npc_dota_hero_ancientapparition",  # the slot decides, not this name
            ward_type="observer",
            team=2,
            x=16000.0,
            y=16000.0,
            expires_tick=end.get("expires"),  # type: ignore[arg-type]
            killed_tick=end.get("killed"),  # type: ignore[arg-type]
            killer=str(end.get("killer", "")),
        )

    match = ParsedMatch(
        match_id=1,
        players=[lion],
        post_game_tick=9_000,
        wards=[
            ward(300, killed=600, killer="npc_dota_creep_badguys_ranged_upgraded"),
            ward(0, expires=10_800),
            ward(30),
        ],
    )
    data = export.wards_recipe(match)

    # In placement order; no game clock, so seconds are raw ticks / 30.
    assert [w[4:7] for w in data["wards"]] == [
        [0.0, 360.0, "e"],
        [1.0, 300.0, "u"],
        [10.0, 20.0, "k"],
    ]
    assert {w[7] for w in data["wards"]} == {"Ancient Apparition"}
    assert data["wards"][2][8] == "a Dire creep"
    assert data["wards"][0][9:] == ["tick 0", "tick 10800"]  # gem's clock; ticks without one
    assert data["end_s"] == 300.0 and data["start_s"] == -90.0
    assert data["range"] is None  # no fight to open on
    assert data["radius"] == round(1600 / (export.MAP_XMAX - export.MAP_XMIN) * SIZE, 1)


def test_objective_names_read_as_a_reader_would() -> None:
    name = export._objective_name
    assert name("goodguys_tower1_bot") == "Radiant tier 1 bottom tower"
    assert name("badguys_tower4") == "Dire tier 4 tower"
    assert name("goodguys_range_rax_top") == "Radiant top ranged barracks"
    assert name("badguys_melee_rax_mid") == "Dire middle melee barracks"
    assert name("goodguys_fort") == "Radiant Ancient"
    assert name("roshan") == "Roshan"


def test_a_fights_breakdown_has_its_timeline_but_no_hero_states() -> None:
    match = _playback_match()
    fight = match.fights[0]
    breakdown = export.fight_playback(match, {}, fight)
    assert breakdown is not None
    assert all(hero["runs"] == [] for hero in breakdown["heroes"])
    assert [cast["what"] for cast in breakdown["casts"]] == ["Black King Bar", "Avalanche"]
    assert breakdown["deaths"] and breakdown["damage"]


def test_fights_recipe_indexes_every_fight_with_its_file() -> None:
    from gem.state.game_clock import GameClock

    match = _playback_match()
    match.game_clock = GameClock(game_start_tick=0)
    files = {1: "fight.json"}
    index = export.fights_recipe(match, files, {1: [0.0, 0.0, 400.0]})
    assert len(index) == len(match.fights) == 1
    entry = index[0]
    assert entry["file"] == "fight.json" and entry["box"] == [0.0, 0.0, 400.0]
    assert entry["kills"] == [match.fights[0].radiant_kills, match.fights[0].dire_kills]
    assert entry["more"] in {"r", "d", "x"} and entry["deaths"] == match.fights[0].deaths


def test_objectives_recipe_places_each_objective_and_lists_the_edges() -> None:
    from gem.extractors.objectives import RoshanKill, TormentorKill, TowerKill
    from gem.state.game_clock import GameClock

    axe = ParsedPlayer(player_id=0, hero_name="npc_dota_hero_axe", team=2)
    lina = ParsedPlayer(player_id=5, hero_name="npc_dota_hero_lina", team=3)
    axe.position_log = [
        (t, 20000.0, 20000.0) for t in range(0, 30_001, 30)
    ]  # near the "_top" tier 4
    lina.position_log = [(t, 9000.0, 9000.0) for t in range(0, 30_001, 30)]
    match = ParsedMatch(
        match_id=1,
        game_start_tick=0,
        post_game_tick=30_000,
        game_clock=GameClock(game_start_tick=0),
        players=[axe, lina],
        fights=[
            Fight(
                start_tick=3_000,
                end_tick=3_900,
                last_death_tick=3_870,
                deaths=1,
                radiant_kills=0,
                dire_kills=1,
            )
        ],
        towers=[
            TowerKill(
                tick=4_500,
                team=2,
                killer="npc_dota_hero_lina",
                tower_name="npc_dota_goodguys_tower1_mid",
                killer_team=3,
            ),
            TowerKill(
                tick=18_000,
                team=3,
                killer="npc_dota_hero_axe",
                tower_name="npc_dota_badguys_tower4",
                killer_team=2,
            ),
        ],
        roshans=[RoshanKill(tick=10_000, killer="npc_dota_hero_axe", kill_number=1, killer_team=2)],
        tormentors=[
            TormentorKill(
                tick=12_000, killer="npc_dota_hero_lina", killer_player_id=5, kill_number=1
            )
        ],
    )
    places = {
        "buildings": {
            "goodguys_tower1_mid": (14000.0, 14000.0),
            "badguys_tower4_bot": (23000.0, 19000.0),
            "badguys_tower4_top": (20100.0, 20100.0),
        },
        "roshan": [
            (0, 12000.0, 18000.0),
            (9_000, 19000.0, 13000.0),
        ],  # in the second pit by the kill
        "tormentor": [(0, 9100.0, 9100.0), (100, 9150.0, 9100.0), (0, 24000.0, 24000.0)],
    }

    data = export.objectives_recipe(match, places)

    assert [b["key"] for b in data["buildings"]] == [
        "badguys_tower4_bot",
        "badguys_tower4_top",
        "goodguys_tower1_mid",
    ]
    assert len(data["tormentor_spawns"]) == 2  # nearby readings are one spawn
    tower1, roshan, tormentor, tower4 = data["objectives"]
    assert tower1["name"] == "Radiant tier 1 middle tower" and tower1["for"] == "d"
    assert tower1["after"] == [1, 20] and tower1["last_hit"] == "Lina"
    assert roshan["at"] == export._project(19000.0, 13000.0)
    assert tormentor["at"] == export._project(9100.0, 9100.0)  # the spawn nearest its killer
    assert tower4["at"] == export._project(
        20100.0, 20100.0
    )  # the tier 4 nearest the last hit's hero
    fight_edge = next(e for e in data["edges"] if e["edge"] == "fight")
    assert fight_edge["outcome"] == "c" and fight_edge["took"] == ["Radiant tier 1 middle tower"]
    aegis = next(e for e in data["edges"] if e["edge"] == "aegis")
    assert (
        aegis["team"] == "r" and aegis["outcome"] == "c" and aegis["took"] == ["Dire tier 4 tower"]
    )


def test_lead_recipe_writes_running_totals_by_source_and_by_hero() -> None:
    from gem.results.models import GoldLedger, GoldLedgerSnapshot
    from gem.state.game_clock import GameClock

    def player(
        pid: int, team: int, hero: str, final: GoldLedgerSnapshot, total: int
    ) -> ParsedPlayer:
        return ParsedPlayer(
            player_id=pid,
            team=team,
            hero_name=hero,
            times=[0, 1_800, 1_860],
            times_min=[0, 1_800],
            total_earned_gold_t=[0, 0, total],
            total_earned_gold_t_min=[0, 0],
            total_earned_xp_t=[0, 0, 0],
            total_earned_xp_t_min=[0, 0],
            gold_ledger=GoldLedger(
                per_minute=[GoldLedgerSnapshot(0, 0), GoldLedgerSnapshot(1_800, 60)], final=final
            ),
        )

    axe = player(
        0,
        2,
        "npc_dota_hero_axe",
        GoldLedgerSnapshot(1_860, 62, hero_kill_gold=300, creep_kill_gold=100, income_gold=50),
        450,
    )
    lina = player(
        5, 3, "npc_dota_hero_lina", GoldLedgerSnapshot(1_860, 62, neutral_kill_gold=200), 200
    )
    match = ParsedMatch(
        match_id=1,
        game_start_tick=0,
        game_clock=GameClock(game_start_tick=0),
        players=[lina, axe],
        fights=[
            Fight(
                start_tick=900,
                end_tick=1_200,
                last_death_tick=1_170,
                deaths=2,
                radiant_kills=1,
                dire_kills=1,
            )
        ],
    )
    data = export.lead_recipe(match)

    assert data["times"] == [0, 60, 62]
    assert data["gold"]["lead"] == [0, 0, 250]
    sources = dict(data["gold"]["sources"])
    assert sources["hero_kills"] == [0, 0, 300] and sources["neutral_creeps"] == [0, 0, -200]
    assert sources["unlisted"] == [0, 0, 0]
    # Radiant first; gold in three groups: hero kills, creeps, the rest.
    assert [(h["name"], h["side"]) for h in data["heroes"]] == [("Axe", "r"), ("Lina", "d")]
    assert [g[-1] for g in data["heroes"][0]["gold"]] == [300, 100, 50]
    assert data["fights"] == [[1, 30.0, 40.0, 2, ""]]
    assert data["objectives"] == []


def test_lanes_recipe_writes_each_lane_with_shares_numbers_and_events() -> None:
    from tests._lanes import lanes_match

    match = lanes_match()
    match.players[0].lane = 2  # OpenDota's lane (mid), which the recipe's (top) differs from
    data = export.lanes_recipe(match)

    assert data["readings"] == [360, 600] and data["min_visit_s"] == 20
    top = data["lanes"][0]
    assert top["lane"] == "top"
    assert top["sides"]["r"]["heroes"] == [["Axe", 0.82]]
    assert top["sides"]["d"]["at"]["360"][0] == 1000 + 60 * 360
    assert [e[:4] for e in data["events"]][:2] == [
        [100, None, "death", "jungle"],
        [300, 340, "visit", "mid"],
    ]
    assert data["events"][4][6] == "Lina"  # the summon's owner
    # Only heroes with an OpenDota lane (the others here have none) that differs.
    assert data["opendota"] == [["Axe", "mid", "top"]]
