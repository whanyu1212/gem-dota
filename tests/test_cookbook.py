"""The cookbook recipes in examples/cookbook answer their questions from gem's facts (HY-102)."""

from __future__ import annotations

import importlib.util
import warnings
from pathlib import Path
from types import ModuleType

import pandas as pd
import pytest

from gem.combat.log import CombatLogEntry, CombatLogType
from gem.extractors.fights import Fight, FightPlayer
from gem.extractors.objectives import AegisEvent, BarracksKill, RoshanKill, TowerKill
from gem.extractors.wards import WardEvent
from gem.results.models import (
    HeroVisibilityEvent,
    ParsedMatch,
    ParsedPlayer,
    SmokeEvent,
    SmokeParticipant,
    VisibilityState,
)
from gem.state.game_clock import GameClock, GamePause

COOKBOOK = Path(__file__).resolve().parent.parent / "examples" / "cookbook"


def _recipe(name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, COOKBOOK / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


roshan_next_fight = _recipe("roshan_next_fight")
core_farm_10_to_20 = _recipe("core_farm_10_to_20")
smoke_to_kill = _recipe("smoke_to_kill")
wards = _recipe("wards")
fights = _recipe("fights")


def _fight(first_death_tick: int, winner: str) -> Fight:
    return Fight(
        start_tick=first_death_tick - 300,
        end_tick=first_death_tick + 300,
        last_death_tick=first_death_tick,
        deaths=1,
        first_death_tick=first_death_tick,
        winner=winner,
        players=[FightPlayer(player_id=i) for i in range(10)],
    )


def _hero_death(
    game_time_s: int, killer_team: int, victim_team: int, **flags: bool
) -> CombatLogEntry:
    return CombatLogEntry(
        tick=game_time_s * 30,
        log_type=CombatLogType.DEATH,
        attacker_name="npc_dota_hero_axe",
        target_name="npc_dota_hero_lina",
        target_is_hero=True,
        attacker_team=killer_team,
        target_team=victim_team,
        game_time_s=game_time_s,
        **flags,
    )


def test_roshan_next_fight_pairs_each_kill_with_its_aegis_and_next_fight() -> None:
    match = ParsedMatch(
        match_id=1,
        game_start_tick=0,
        game_clock=GameClock(
            game_start_tick=0, pauses=[GamePause(start_tick=3_100, end_tick=6_100)]
        ),
        players=[ParsedPlayer(player_id=6, team=3, hero_name="npc_dota_hero_huskar")],
        roshans=[
            RoshanKill(tick=3_000, killer="npc_dota_hero_huskar", kill_number=1, killer_team=3),
            RoshanKill(tick=30_000, killer="npc_dota_hero_huskar", kill_number=2, killer_team=3),
        ],
        aegis_events=[
            AegisEvent(tick=3_010, player_id=6, event_type="denied"),
            AegisEvent(tick=30_020, player_id=6, event_type="pickup"),
        ],
        # 100 s of a 3,000-tick pause sit between the first kill and this fight.
        fights=[_fight(7_000, "dire"), _fight(50_000, "radiant")],
    )

    table = roshan_next_fight.roshan_next_fight(match)

    first, second = table.to_dict("records")
    assert (first["aegis"], first["aegis_by"]) == ("denied", "huskar")
    assert first["next_fight"] == 1
    # 4,000 ticks apart, of which 3,000 are paused: 33 s of game time.
    assert first["seconds_to_fight"] == 33
    assert first["killer_team_won"] is True
    # The second kill's only later fight is 667 s away, past the Aegis's 5 minutes.
    assert pd.isna(second["next_fight"])
    assert second["killer_team_won"] is None


def test_smoke_to_kill_counts_real_hero_kills_in_the_window() -> None:
    participant = SmokeParticipant(
        hero_name="npc_dota_hero_axe", player_id=0, applied_tick=600, removed_tick=900
    )
    match = ParsedMatch(
        match_id=1,
        game_start_tick=0,
        game_clock=GameClock(game_start_tick=0),
        smoke_events=[
            SmokeEvent(tick=600, activator="npc_dota_hero_axe", team=2, participants=[participant])
        ],
        combat_log=[
            _hero_death(
                25, killer_team=2, victim_team=3, will_reincarnate=True
            ),  # Aegis: not a kill
            _hero_death(28, killer_team=2, victim_team=3, target_is_illusion=True),  # illusion
            _hero_death(40, killer_team=2, victim_team=3),
            _hero_death(45, killer_team=3, victim_team=2),
            _hero_death(200, killer_team=2, victim_team=3),  # outside the window
        ],
    )

    row = smoke_to_kill.smoke_to_kill(match).iloc[0]

    assert row["team"] == "radiant"
    assert row["first_kill_after_s"] == 20
    assert row["first_loss_after_s"] == 25


def test_core_farm_reports_the_window_for_each_core() -> None:
    minutes = list(range(25))

    def laner(player_id: int, team: int, lane_role: int, lh_at_10: int) -> ParsedPlayer:
        return ParsedPlayer(
            player_id=player_id,
            team=team,
            hero_name=f"npc_dota_hero_{player_id}",
            lane_role=lane_role,
            lane_last_hits=lh_at_10,
            total_earned_gold_t_min=[600 * m for m in minutes],
            lh_t_min=[10 * m for m in minutes],
            # Inside the Radiant half for the whole window.
            position_log=[(tick, 10_000.0, 10_000.0) for tick in range(18_000, 36_000, 30)],
        )

    carry, support = laner(0, 2, 1, 60), laner(1, 2, 1, 5)
    neutral = CombatLogEntry(
        tick=20_000,
        log_type=CombatLogType.DEATH,
        attacker_name=carry.hero_name,
        target_name="npc_dota_neutral_kobold",
        game_time_s=700,
    )
    match = ParsedMatch(
        match_id=1,
        game_start_tick=0,
        game_clock=GameClock(game_start_tick=0),
        players=[carry, support],
        combat_log=[neutral],
    )

    row = core_farm_10_to_20.core_farm(match).iloc[0]

    assert (row["hero"], row["role"]) == ("0", "carry")  # the support laner is not a core
    assert row["gold_per_min"] == 600
    assert row["last_hits"] == 100
    assert row["neutral_kills"] == 1
    assert row["own_half"] == 1.0


@pytest.mark.integration
@pytest.mark.slow
def test_recipes_run_on_a_replay_without_deprecation_warnings(canonical_parsed_match) -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        rosh = roshan_next_fight.roshan_next_fight(canonical_parsed_match)
        farm = core_farm_10_to_20.core_farm(canonical_parsed_match)
        smokes = smoke_to_kill.smoke_to_kill(canonical_parsed_match)
        ward_rows = wards.ward_table(canonical_parsed_match)
        samples = wards.circle_samples(canonical_parsed_match, ward_rows)
        fight_rows = fights.fight_table(canonical_parsed_match)

    assert len(rosh) == len(canonical_parsed_match.roshans)
    assert list(rosh.columns) == roshan_next_fight.COLUMNS
    # The canonical replay's minute curves end before 20:00, so no core has the window.
    assert list(farm.columns) == core_farm_10_to_20.COLUMNS
    assert set(farm["role"]) <= {"carry", "mid", "offlane"}
    assert list(smokes.columns) == smoke_to_kill.COLUMNS
    assert len(smokes) > 0
    placed = [w for w in canonical_parsed_match.wards if w.x is not None and w.team in (2, 3)]
    assert list(ward_rows.columns) == wards.WARD_COLUMNS and len(ward_rows) == len(placed)
    heroes = {p.hero_name for p in canonical_parsed_match.players}
    assert set(ward_rows["placer"]) <= heroes
    assert set(samples["state"]) <= set(wards.STATES) and (samples["distance"] <= 1600).all()
    assert list(fight_rows.columns) == fights.COLUMNS
    assert len(fight_rows) == len(canonical_parsed_match.fights)
    assert set(fight_rows["more_kills"]) <= {"radiant", "dire", "even"}


def test_recipes_fall_back_to_hero_teams_without_combat_log_teams() -> None:
    # Source 1 replays record no attacker/target team on the combat log or Roshan kill.
    axe = ParsedPlayer(player_id=0, team=2, hero_name="npc_dota_hero_axe")
    lina = ParsedPlayer(player_id=5, team=3, hero_name="npc_dota_hero_lina")
    match = ParsedMatch(
        match_id=1,
        game_start_tick=0,
        game_clock=GameClock(game_start_tick=0),
        players=[axe, lina],
        roshans=[
            RoshanKill(
                tick=3_000,
                killer="npc_dota_roshan_minion",
                kill_number=1,
                killer_source="npc_dota_hero_axe",
            )
        ],
        fights=[_fight(4_000, "radiant")],
        smoke_events=[SmokeEvent(tick=600, activator="npc_dota_hero_axe", team=2)],
        combat_log=[
            CombatLogEntry(
                tick=1_200,
                log_type=CombatLogType.DEATH,
                attacker_name="npc_dota_axe_summon",
                damage_source_name="npc_dota_hero_axe",
                target_name="npc_dota_hero_lina",
                target_is_hero=True,
                game_time_s=40,
            )
        ],
    )

    rosh = roshan_next_fight.roshan_next_fight(match).iloc[0]
    smoke = smoke_to_kill.smoke_to_kill(match).iloc[0]

    assert (rosh["killed_by"], rosh["killer_team_won"]) == ("radiant", True)
    assert smoke["first_kill_after_s"] == 20


def _ward_match() -> ParsedMatch:
    """Lion (Radiant) wards; Axe (Dire) walks through Lion's observer circle."""
    lion = ParsedPlayer(player_id=0, team=2, hero_name="npc_dota_hero_lion")
    axe = ParsedPlayer(player_id=5, team=3, hero_name="npc_dota_hero_axe")
    axe.position_log = [
        (30, 16100.0, 16000.0),  # 100 from the observer: inside, seen
        (60, 17000.0, 16000.0),  # 1,000: inside, hidden
        (90, 20000.0, 16000.0),  # 4,000: outside
        (120, 16000.0, 16000.0),  # inside, but dead
        (150, 16000.0, 16000.0),  # inside, but smoked
    ]
    axe.times = [tick for tick, _, _ in axe.position_log]
    axe.hp_t = [700, 700, 700, 0, 700]
    visible, hidden = VisibilityState.VISIBLE, VisibilityState.HIDDEN

    def seen(tick: int, radiant: VisibilityState) -> HeroVisibilityEvent:
        return HeroVisibilityEvent(tick, 5, "npc_dota_hero_axe", 9, 1, radiant, visible)

    def ward(tick: int, kind: str, team: int, **end: object) -> WardEvent:
        return WardEvent(
            tick=tick,
            player_id=0 if team == 2 else 5,
            placer="npc_dota_hero_lionx",  # the slot decides, not this name
            ward_type=kind,  # type: ignore[arg-type]
            team=team,
            x=16000.0,
            y=16000.0,
            expires_tick=end.get("expires"),  # type: ignore[arg-type]
            killed_tick=end.get("killed"),  # type: ignore[arg-type]
            killer=str(end.get("killer", "")),
        )

    return ParsedMatch(
        match_id=7,
        game_start_tick=0,
        post_game_tick=20_000,
        game_clock=GameClock(game_start_tick=0),
        players=[lion, axe],
        wards=[
            ward(0, "observer", 2, expires=10_800),
            ward(10, "sentry", 3, killed=310, killer="npc_dota_hero_lion"),
            ward(5_000, "observer", 2),  # still up when the recording ends
        ],
        # Two events on tick 60: the later one wins.
        hero_visibility_events=[seen(0, visible), seen(60, visible), seen(60, hidden)],
        smoke_events=[
            SmokeEvent(
                tick=140,
                activator="npc_dota_hero_axe",
                team=3,
                participants=[
                    SmokeParticipant(
                        hero_name="npc_dota_hero_axe",
                        player_id=5,
                        applied_tick=140,
                        removed_tick=200,
                    )
                ],
            )
        ],
    )


def test_wards_lists_each_ward_with_how_it_ended() -> None:
    table = wards.ward_table(_ward_match())

    assert list(table["how"]) == ["expired", "killed", "up at the end"]
    assert list(table["placer"]) == [
        "npc_dota_hero_lion",
        "npc_dota_hero_axe",
        "npc_dota_hero_lion",
    ]
    assert list(table["lasted_s"].round(1)) == [360.0, 10.0, 500.0]
    assert table["killer"].tolist() == ["", "npc_dota_hero_lion", ""]
    # The side is the warding team's: the same spot is one team's half, the other's enemy half.
    radiant_side, dire_side = table["side"].iloc[0], table["side"].iloc[1]
    if table["region"].iloc[0].endswith("_half"):
        assert {radiant_side, dire_side} == {"own half", "enemy half"}
    lifetimes = wards.observer_lifetimes(table)
    assert lifetimes["placed"].sum() == 2 and lifetimes["killed"].sum() == 0


def test_wards_reads_visibility_as_hero_visibility_at_does() -> None:
    import gem

    match = _ward_match()
    lookup = wards._states(match)
    for tick in (-1, 0, 59, 60, 61):
        expected = gem.hero_visibility_at(match, player_id=5, observing_team=2, tick=tick)
        assert wards.visibility_at(lookup, 5, 2, tick) == expected.value


def test_wards_checks_the_circle_against_the_replays_visibility() -> None:
    samples = wards.circle_samples(_ward_match())

    # Inside: seen at 100, hidden at 1,000, smoked at 150; outside and dead are left out.
    assert samples[["tick", "state"]].values.tolist() == [
        [30, "visible"],
        [60, "hidden"],
        [150, "smoked"],
    ]
    assert samples["team"].unique().tolist() == ["radiant"]  # Dire placed no observer
    assert samples["distance"].round().tolist() == [100, 1000, 0]
    summary = wards.circle_summary(samples).iloc[0]
    assert (summary["seconds"], summary["visible"], summary["hidden"], summary["smoked"]) == (
        2,
        1,
        1,
        1,
    )
    bands = wards.by_distance(samples).set_index("distance")
    assert (
        bands.loc["0-400", "visible_pct"] == 100.0 and bands.loc["800-1200", "visible_pct"] == 0.0
    )


def test_fights_lists_each_fight_and_what_fell_next() -> None:
    def fight(start: int, end: int, radiant: int, dire: int) -> Fight:
        return Fight(
            start_tick=start,
            end_tick=end,
            last_death_tick=end - 30,
            deaths=radiant + dire,
            radiant_kills=radiant,
            dire_kills=dire,
            centroid_x=16000.0,
            centroid_y=16000.0,
            players=[
                FightPlayer(player_id=0, gold_delta=300),
                FightPlayer(player_id=5, gold_delta=-50),
            ],
        )

    match = ParsedMatch(
        match_id=3,
        game_start_tick=0,
        game_clock=GameClock(game_start_tick=0),
        players=[
            ParsedPlayer(player_id=0, team=2, hero_name="npc_dota_hero_axe"),
            ParsedPlayer(player_id=5, team=3, hero_name="npc_dota_hero_lina"),
        ],
        fights=[
            fight(9_000, 9_900, 0, 2),  # Dire more kills; nothing falls within 120 s
            fight(3_000, 3_900, 2, 1),  # Radiant more kills; Dire's tower falls 60 s later
            fight(6_000, 6_900, 1, 1),  # even
        ],
        towers=[
            TowerKill(
                tick=5_700,
                team=3,
                killer="npc_dota_hero_axe",
                tower_name="npc_dota_badguys_tower1_mid",
            )
        ],
        barracks=[
            # Radiant denies its own barracks: it still counts for Dire.
            BarracksKill(
                tick=7_000,
                team=2,
                killer="npc_dota_hero_axe",
                barracks_name="npc_dota_goodguys_melee_rax_mid",
                killer_team=2,
            )
        ],
        roshans=[
            RoshanKill(tick=20_000, killer="npc_dota_hero_lina", kill_number=1, killer_team=3)
        ],
    )

    table = fights.fight_table(match)

    assert list(table["fight"]) == [1, 2, 3] and list(table["start"]) == ["01:40", "03:20", "05:00"]
    assert list(table["more_kills"]) == ["radiant", "even", "dire"]
    first = table.iloc[0]
    assert (first["next"], first["next_for"], first["next_after_s"]) == (
        "badguys_tower1_mid",
        "radiant",
        60,
    )
    assert table.iloc[1]["next_for"] == "dire"  # the deny, 3 s after the even fight
    assert pd.isna(table.iloc[2]["next"])  # Roshan is too late
    assert (first["radiant_gold"], first["dire_gold"]) == (300, -50)
    assert fights.next_objective_summary(table) == {
        "fights": 3,
        "more_kills": 2,
        "followed": 1,
        "same_side": 1,
    }
