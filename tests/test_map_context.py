"""Tests for objective-aware map-context helpers."""

from __future__ import annotations

from gem.extractors.objectives import AegisEvent, RoshanKill, TowerKill
from gem.extractors.wards import WardEvent
from gem.map_context import MapContextBucket, build_map_context_timeline, score_camp_visit_context
from gem.models import ParsedMatch


def _make_match() -> ParsedMatch:
    match = ParsedMatch(game_start_tick=0, game_end_tick=3600)

    # Team assignment and minimal movement logs.
    for idx, player in enumerate(match.players):
        player.team = 2 if idx < 5 else 3
        if idx == 5:
            # Enemy hero pathing in Radiant half to create pressure.
            player.position_log = [(2800, 11000.0, 9000.0), (3200, 11800.0, 9800.0)]

    match.towers = [
        TowerKill(
            tick=1000,
            team=2,
            killer="npc_dota_hero_axe",
            tower_name="npc_dota_goodguys_tower1_mid",
        )
    ]
    match.roshans = [RoshanKill(tick=1800, killer="npc_dota_hero_ursa", kill_number=1)]
    # Dire slot 5 picks up Aegis.
    match.aegis_events = [AegisEvent(tick=1810, player_id=5, event_type="pickup")]
    match.wards = [
        WardEvent(
            tick=800,
            player_id=0,
            placer="npc_dota_hero_crystal_maiden",
            ward_type="observer",
            team=2,
            x=12000.0,
            y=12000.0,
            expires_tick=2600,
            killed_tick=None,
            killer="",
        ),
        WardEvent(
            tick=900,
            player_id=5,
            placer="npc_dota_hero_axe",
            ward_type="observer",
            team=3,
            x=17000.0,
            y=17000.0,
            expires_tick=None,
            killed_tick=None,
            killer="",
        ),
    ]
    return match


def test_build_map_context_timeline_tracks_objective_state() -> None:
    match = _make_match()
    buckets = build_map_context_timeline(match, team=2, bucket_ticks=900, presence_window_ticks=900)

    assert buckets
    # Last bucket should reflect the persisted objective state.
    last = buckets[-1]
    assert last.t1_mid_alive_radiant is False
    assert last.roshan_last_kill_tick == 1800
    assert last.aegis_active is True
    assert last.aegis_holder_team == 3
    assert last.ward_count_dire >= 1
    assert last.enemy_presence_by_region["radiant_half"] > 0.0


def test_score_camp_visit_context_emits_expected_drivers() -> None:
    bucket = MapContextBucket(
        start_tick=2700,
        end_tick=3599,
        tower_alive_radiant=8,
        tower_alive_dire=10,
        t1_mid_alive_radiant=False,
        t1_mid_alive_dire=True,
        roshan_last_kill_tick=1800,
        aegis_holder_team=3,
        aegis_active=True,
        tormentor_last_kill_tick=None,
        ward_count_radiant=0,
        ward_count_dire=2,
        net_worth_advantage=-6000,
        xp_advantage=-5000,
        enemy_presence_by_region={"river": 0.5, "radiant_half": 0.7, "dire_half": 0.1},
    )

    ctx = score_camp_visit_context(
        team=2,
        camp_id=1,
        camp_type="large",
        neutral_kills=3,
        neutral_damage=2500,
        xp_gain=520,
        bucket=bucket,
    )

    assert 0.0 <= ctx.farm_safety_score <= 1.0
    assert 0.0 <= ctx.pressure_score <= 1.0
    assert 0.0 <= ctx.expected_value_score <= 1.0
    assert ctx.context_label == "defensive_home_farm"
    assert "lost_t1_mid" in ctx.context_drivers
    assert "enemy_aegis_active" in ctx.context_drivers
    assert "vision_deficit" in ctx.context_drivers


def test_winning_team_home_farm_downgrades_to_pressured() -> None:
    bucket = MapContextBucket(
        start_tick=2700,
        end_tick=3599,
        tower_alive_radiant=9,
        tower_alive_dire=8,
        t1_mid_alive_radiant=True,
        t1_mid_alive_dire=False,
        roshan_last_kill_tick=None,
        aegis_holder_team=None,
        aegis_active=False,
        tormentor_last_kill_tick=None,
        ward_count_radiant=1,
        ward_count_dire=1,
        net_worth_advantage=7000,
        xp_advantage=6500,
        enemy_presence_by_region={"river": 0.5, "radiant_half": 0.65, "dire_half": 0.1},
    )

    ctx = score_camp_visit_context(
        team=2,
        camp_id=1,
        camp_type="large",
        neutral_kills=3,
        neutral_damage=2000,
        xp_gain=420,
        bucket=bucket,
    )

    assert ctx.context_label == "pressured_home_farm"
