from __future__ import annotations

import sys
from pathlib import Path

from gem.combatlog import CombatLogEntry
from gem.extractors.objectives import AegisEvent, BarracksKill, RoshanKill, TowerKill
from gem.extractors.teamfights import Teamfight, TeamfightPlayer
from gem.extractors.wards import WardEvent
from gem.models import ParsedMatch, ParsedPlayer
from gem.rosh_conversion import build_rosh_conversions

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from report.html_sections import build_rosh_conversion


def _make_players() -> list[ParsedPlayer]:
    players: list[ParsedPlayer] = []
    for pid in range(10):
        team = 2 if pid < 5 else 3
        players.append(
            ParsedPlayer(
                player_id=pid,
                hero_name=f"npc_dota_hero_hero_{pid}",
                team=team,
            )
        )
    return players


def _make_fight(start: int, end: int, winner: str, deaths: int = 2) -> Teamfight:
    return Teamfight(
        start_tick=start,
        end_tick=end,
        last_death_tick=end - 60,
        deaths=deaths,
        winner=winner,
        players=[TeamfightPlayer(player_id=i) for i in range(10)],
    )


def test_build_rosh_conversions_objective_conversion() -> None:
    players = _make_players()
    players[0].position_log = [(800, 9800.0, 9800.0), (1300, 24500.0, 22000.0)]
    players[1].position_log = [(820, 9900.0, 9850.0), (1320, 23850.0, 21400.0)]
    players[5].buyback_log = [CombatLogEntry(tick=1500, log_type="BUYBACK")]

    match = ParsedMatch(
        game_start_tick=0,
        game_end_tick=10000,
        radiant_win=None,
        players=players,
        roshans=[RoshanKill(tick=1000, killer="npc_dota_hero_hero_0", kill_number=1)],
        aegis_events=[AegisEvent(tick=1010, player_id=0, event_type="pickup")],
        towers=[
            TowerKill(
                tick=1600,
                team=3,
                killer="npc_dota_hero_hero_0",
                tower_name="npc_dota_badguys_tower2_mid",
            ),
            TowerKill(
                tick=1700,
                team=3,
                killer="npc_dota_hero_hero_1",
                tower_name="npc_dota_badguys_tower2_top",
            ),
        ],
        barracks=[
            BarracksKill(
                tick=2000,
                team=3,
                killer="npc_dota_hero_hero_0",
                barracks_name="npc_dota_badguys_melee_rax_mid",
            )
        ],
        wards=[
            WardEvent(
                tick=1400,
                player_id=0,
                placer="npc_dota_hero_hero_0",
                ward_type="observer",
                team=2,
                x=24500.0,
                y=22000.0,
                expires_tick=None,
                killed_tick=None,
                killer="",
            )
        ],
        teamfights=[_make_fight(1200, 1450, "radiant")],
        combat_log=[],
    )

    conversions = build_rosh_conversions(match)
    assert len(conversions) == 1
    conversion = conversions[0]
    assert conversion.conversion_label == "objective_conversion"
    assert conversion.fights_won == 1
    assert conversion.towers_taken == 2
    assert conversion.barracks_taken == 1
    assert conversion.enemy_buybacks_forced == 1
    assert conversion.enemy_half_observer_delta == 1
    assert conversion.enemy_half_farm_share_delta > 0.0
    assert any(event.kind == "barracks" for event in conversion.timeline_events)


def test_build_rosh_conversions_failed_aegis_on_lost_fight() -> None:
    players = _make_players()
    players[5].position_log = [(1800, 23000.0, 22000.0), (2250, 15000.0, 15000.0)]

    match = ParsedMatch(
        game_start_tick=0,
        game_end_tick=9000,
        radiant_win=None,
        players=players,
        roshans=[RoshanKill(tick=2000, killer="npc_dota_hero_hero_5", kill_number=1)],
        aegis_events=[AegisEvent(tick=2010, player_id=5, event_type="pickup")],
        teamfights=[_make_fight(2200, 2600, "radiant")],
        combat_log=[
            CombatLogEntry(
                tick=2300,
                log_type="DEATH",
                target_name="npc_dota_hero_hero_5",
                target_is_hero=True,
                target_is_illusion=False,
            )
        ],
    )

    conversions = build_rosh_conversions(match)
    assert len(conversions) == 1
    conversion = conversions[0]
    assert conversion.aegis_fate == "consumed"
    assert conversion.conversion_label == "low_conversion"
    assert conversion.aegis_outcome == "window_lost"
    assert conversion.fights_lost == 1
    assert conversion.towers_taken == 0
    assert conversion.barracks_taken == 0
    assert any(event.kind == "aegis_end" for event in conversion.timeline_events)


def test_build_rosh_conversions_uses_first_death_for_fight_timing() -> None:
    players = _make_players()
    fight = Teamfight(
        start_tick=500,
        end_tick=1300,
        last_death_tick=850,
        deaths=2,
        first_death_tick=950,
        winner="radiant",
        players=[TeamfightPlayer(player_id=i) for i in range(10)],
    )
    match = ParsedMatch(
        game_start_tick=0,
        game_end_tick=4000,
        radiant_win=None,
        players=players,
        roshans=[RoshanKill(tick=1000, killer="npc_dota_hero_hero_0", kill_number=1)],
        aegis_events=[AegisEvent(tick=1010, player_id=0, event_type="pickup")],
        teamfights=[fight],
    )

    conversion = build_rosh_conversions(match)[0]
    assert conversion.first_fight_tick == 1010
    fight_events = [
        event for event in conversion.timeline_events if event.kind.startswith("fight_")
    ]
    assert fight_events
    assert fight_events[0].tick == 1010
    assert "already underway" in fight_events[0].label.lower()


def test_build_rosh_conversion_html_smoke() -> None:
    players = _make_players()
    match = ParsedMatch(
        game_start_tick=0,
        game_end_tick=6000,
        radiant_win=None,
        players=players,
        roshans=[RoshanKill(tick=1000, killer="npc_dota_hero_hero_0", kill_number=1)],
        aegis_events=[AegisEvent(tick=1010, player_id=0, event_type="pickup")],
    )

    html = build_rosh_conversion(match)
    assert "Roshan Conversion" in html
    assert "Roshan #1" in html
