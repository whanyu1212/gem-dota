"""Tests for comparative farming-segment context and composable tags."""

from __future__ import annotations

import pytest

import gem
from gem.analysis import farming, farming_context
from gem.analysis._territory import RoshTerritoryWindow
from gem.analysis.farming import (
    FarmingContextConfig,
    FarmingContextTag,
    build_farming_routes,
)
from gem.extractors.objectives import AegisEvent, RoshanKill, TowerKill
from gem.extractors.wards import WardEvent
from gem.results.models import ParsedMatch, ParsedPlayer


def _catalog() -> dict:
    return {
        "version": 2,
        "dota_patch": "test",
        "topology_patch": "test",
        "camps": [
            {
                "id": 1,
                "type": "large",
                "center": {"x": 10_000.0, "y": 15_000.0},
                "zone": {
                    "shape": "ellipse",
                    "rx": 500.0,
                    "ry": 500.0,
                    "rotation_deg": 0,
                },
                "hysteresis": {"enter_margin": 0, "exit_margin": 100},
                "topology": {"owner_team": 3, "lane": "top", "area": "jungle"},
            }
        ],
    }


def _samples(x: float, y: float) -> list[tuple[int, float, float]]:
    return [(tick, x, y) for tick in range(0, 2701, 300)]


def _player(player_id: int, team: int, x: float, y: float) -> ParsedPlayer:
    return ParsedPlayer(
        player_id=player_id,
        hero_name=f"npc_dota_hero_{player_id}",
        team=team,
        position_log=_samples(x, y),
        times=[1350],
        net_worth_t=[10_000 + player_id],
        total_earned_xp_t=[5_000 + player_id],
    )


def _complete_match() -> ParsedMatch:
    players = [_player(0, 2, 10_000.0, 15_000.0)]
    players.extend(_player(player_id, 2, 8_000.0, 8_000.0) for player_id in range(1, 5))
    players.extend(_player(player_id, 3, 10_000.0, 15_000.0) for player_id in range(5, 10))
    return ParsedMatch(game_start_tick=0, game_end_tick=2700, players=players)


def test_context_is_public() -> None:
    assert gem.FarmingContextConfig is FarmingContextConfig
    assert gem.FarmingContextTag is FarmingContextTag


def test_context_tags_are_composable_and_comparative(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(farming, "load_camp_zones", _catalog)
    match = _complete_match()
    match.towers = [
        TowerKill(
            tick=900,
            team=2,
            killer="npc_dota_hero_5",
            tower_name="npc_dota_goodguys_tower1_top",
        )
    ]
    match.wards = [
        WardEvent(
            tick=300,
            player_id=5,
            placer="npc_dota_hero_5",
            ward_type="observer",
            team=3,
            x=10_000.0,
            y=15_000.0,
            expires_tick=5000,
            killed_tick=None,
            killer="",
        )
    ]
    match.roshans = [
        RoshanKill(
            tick=1000,
            killer="npc_dota_hero_5",
            kill_number=1,
            killer_team=3,
        )
    ]
    match.aegis_events = [AegisEvent(tick=1010, player_id=5, event_type="pickup")]

    segment = build_farming_routes(match)[0].segments[0]
    context = segment.context

    assert context is not None
    assert context.status == "complete"
    assert segment.distance_travelled == 0.0
    assert segment.camp_lane == "top"
    assert segment.camp_area == "jungle"
    assert context.enemy_presence_hero_seconds > context.own_presence_hero_seconds
    assert context.own_relevant_towers_alive == 1
    assert context.enemy_relevant_towers_alive == 2
    assert {
        FarmingContextTag.ENEMY_SIDE,
        FarmingContextTag.HIGH_ENEMY_PRESENCE,
        FarmingContextTag.VISION_DISADVANTAGE,
        FarmingContextTag.TOWER_DISADVANTAGE,
        FarmingContextTag.ENEMY_AEGIS_ACTIVE,
    } <= set(context.tags)
    assert context.aegis_holder_team == 3
    assert context.aegis_source is not None
    assert context.aegis_source.startswith("player_id:")
    assert FarmingContextTag.INCOMPLETE_CONTEXT not in context.tags


def test_missing_comparative_inputs_remain_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(farming, "load_camp_zones", _catalog)
    match = ParsedMatch(
        game_start_tick=0,
        game_end_tick=2700,
        players=[_player(0, 2, 10_000.0, 15_000.0)],
    )

    context = build_farming_routes(match)[0].segments[0].context

    assert context is not None
    assert context.status == "partial"
    assert context.net_worth_advantage is None
    assert context.total_earned_xp_advantage is None
    assert context.enemy_presence_hero_seconds is None
    assert FarmingContextTag.INCOMPLETE_CONTEXT in context.tags
    assert "team_3_roster_unavailable" in context.status_reasons
    assert "enemy_presence_position_coverage_below_threshold" in context.status_reasons


def test_economy_and_xp_availability_are_independent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(farming, "load_camp_zones", _catalog)
    match = _complete_match()
    match.players[1].total_earned_xp_t = []

    context = build_farming_routes(match)[0].segments[0].context

    assert context is not None
    assert context.net_worth_advantage is not None
    assert context.total_earned_xp_advantage is None
    assert context.status == "partial"
    assert "player_1_total_xp_sample_unavailable" in context.status_reasons
    assert FarmingContextTag.INCOMPLETE_CONTEXT in context.tags


def test_incomplete_point_vision_does_not_infer_disadvantage(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(farming, "load_camp_zones", _catalog)
    match = _complete_match()
    match.players[1].position_log = []
    match.wards = [
        WardEvent(
            tick=300,
            player_id=5,
            placer="npc_dota_hero_5",
            ward_type="observer",
            team=3,
            x=10_000.0,
            y=15_000.0,
            expires_tick=5000,
            killed_tick=None,
            killer="",
        )
    ]

    context = build_farming_routes(match)[0].segments[0].context

    assert context is not None
    assert context.own_point_vision_status == "supported"
    assert context.own_point_vision_gaps
    assert context.enemy_observer_vision_source_count == 1
    assert FarmingContextTag.VISION_DISADVANTAGE not in context.tags
    assert FarmingContextTag.INCOMPLETE_CONTEXT in context.tags
    assert any(reason.startswith("own_point_vision:") for reason in context.status_reasons)


def test_enemy_side_territory_threshold_adds_independent_tag(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(farming, "load_camp_zones", _catalog)
    monkeypatch.setattr(
        farming_context,
        "build_territory_window",
        lambda *_args, **_kwargs: RoshTerritoryWindow(
            coverage_differential_pct=0.5,
            depth_differential=0.1,
            status="complete",
        ),
    )

    context = build_farming_routes(_complete_match())[0].segments[0].context

    assert context is not None
    assert FarmingContextTag.ENEMY_SIDE in context.tags
    assert FarmingContextTag.TERRITORIAL_ADVANCE in context.tags
    assert context.territory_coverage_differential_pct == 0.5
    assert context.territory_depth_differential == 0.1


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"lookback_ticks": 0}, "lookback_ticks"),
        ({"territory_lookback_ticks": 0}, "territory_lookback_ticks"),
        ({"max_position_gap_ticks": 0}, "max_position_gap_ticks"),
        ({"presence_radius": 0}, "presence_radius"),
        ({"min_presence_coverage": 1.1}, "min_presence_coverage"),
        ({"high_enemy_presence_seconds": -1}, "high_enemy_presence_seconds"),
    ],
)
def test_context_config_rejects_invalid_values(kwargs: dict, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        FarmingContextConfig(**kwargs)
