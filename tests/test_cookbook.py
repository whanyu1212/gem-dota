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
from gem.extractors.objectives import AegisEvent, RoshanKill
from gem.results.models import ParsedMatch, ParsedPlayer, SmokeEvent, SmokeParticipant
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

    assert len(rosh) == len(canonical_parsed_match.roshans)
    assert list(rosh.columns) == roshan_next_fight.COLUMNS
    # The canonical replay's minute curves end before 20:00, so no core has the window.
    assert list(farm.columns) == core_farm_10_to_20.COLUMNS
    assert set(farm["role"]) <= {"carry", "mid", "offlane"}
    assert list(smokes.columns) == smoke_to_kill.COLUMNS
    assert len(smokes) > 0
