"""Tests for evidence-first farming-route reconstruction."""

from __future__ import annotations

import pytest

import gem
from gem.analysis import farming
from gem.analysis.farming import (
    FarmingBoundaryReason,
    FarmingEvidenceStrength,
    FarmingRouteConfig,
    build_farming_routes,
)
from gem.combat.log import CombatLogEntry, CombatLogType
from gem.results.models import ParsedMatch, ParsedPlayer


def _zone(
    camp_id: int,
    center_x: float,
    *,
    radius: float = 10.0,
    camp_type: str = "large",
    exit_margin: float = 0.0,
) -> dict:
    return {
        "id": camp_id,
        "type": camp_type,
        "center": {"x": center_x, "y": 0.0},
        "zone": {
            "shape": "ellipse",
            "rx": radius,
            "ry": radius,
            "rotation_deg": 0,
        },
        "hysteresis": {"enter_margin": 0, "exit_margin": exit_margin},
    }


def _catalog(*zones: dict) -> dict:
    return {"version": 7, "dota_patch": "test", "camps": list(zones)}


def _player(
    points: list[tuple[int, float, float]],
    *,
    times: list[int] | None = None,
    xp: list[int] | None = None,
    gold: list[int] | None = None,
) -> ParsedPlayer:
    return ParsedPlayer(
        player_id=0,
        hero_name="npc_dota_hero_axe",
        team=2,
        position_log=points,
        times=times or [],
        xp_t=xp or [],
        total_earned_gold_t=gold or [],
    )


def test_missing_positions_remain_unavailable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(farming, "load_camp_zones", lambda: _catalog(_zone(1, 0)))

    route = build_farming_routes(ParsedMatch(players=[_player([])]))[0]

    assert route.status == "unavailable"
    assert route.status_reasons == ["position_samples_unavailable"]
    assert route.camp_catalog_version == 7
    assert route.camp_map_patch == "test"


def test_farming_route_builder_is_public() -> None:
    assert gem.build_farming_routes is build_farming_routes
    assert gem.FarmingRouteConfig is FarmingRouteConfig


@pytest.mark.parametrize(
    "camp_type",
    ["small", "medium", "large", "ancient", "flooded_small", "flooded_medium"],
)
def test_every_bundled_camp_family_uses_the_same_geometry_contract(
    monkeypatch: pytest.MonkeyPatch,
    camp_type: str,
) -> None:
    monkeypatch.setattr(
        farming,
        "load_camp_zones",
        lambda: _catalog(_zone(1, 0, camp_type=camp_type)),
    )

    route = build_farming_routes(ParsedMatch(players=[_player([(0, 0.0, 0.0)])]))[0]

    assert route.points[0].camp_id == 1
    assert route.points[0].camp_type == camp_type
    assert route.points[0].inside_base_zone is True


def test_missing_catalog_is_explicitly_unavailable(monkeypatch: pytest.MonkeyPatch) -> None:
    def _raise_missing() -> dict:
        raise OSError("missing catalog")

    monkeypatch.setattr(farming, "load_camp_zones", _raise_missing)

    route = build_farming_routes(ParsedMatch(players=[_player([(0, 0.0, 0.0)])]))[0]

    assert route.status == "unavailable"
    assert route.status_reasons == ["camp_zone_catalog_unavailable"]
    assert route.camp_catalog_version is None
    assert route.camp_map_patch is None


def test_route_starts_at_the_match_start_tick(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(farming, "load_camp_zones", lambda: _catalog(_zone(1, 0)))
    player = _player([(-30, 0.0, 0.0), (0, 0.0, 0.0), (30, 0.0, 0.0)])

    route = build_farming_routes(ParsedMatch(game_start_tick=0, players=[player]))[0]

    assert [point.tick for point in route.points] == [0, 30]
    assert route.segments[0].start_tick == 0


def test_only_pregame_positions_are_unavailable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(farming, "load_camp_zones", lambda: _catalog(_zone(1, 0)))

    route = build_farming_routes(
        ParsedMatch(game_start_tick=100, players=[_player([(90, 0.0, 0.0)])])
    )[0]

    assert route.status == "unavailable"
    assert route.status_reasons == ["in_game_position_samples_unavailable"]


def test_overlap_prefers_current_zone_then_normalized_distance_and_id(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        farming,
        "load_camp_zones",
        lambda: _catalog(
            _zone(2, 0, radius=10, exit_margin=2),
            _zone(1, 15, radius=10),
        ),
    )
    match = ParsedMatch(players=[_player([(0, 0.0, 0.0), (30, 8.0, 0.0), (60, 15.0, 0.0)])])

    route = build_farming_routes(match)[0]

    assert [point.camp_id for point in route.points] == [2, 2, 1]
    assert [
        (segment.camp_id, segment.start_tick, segment.end_tick) for segment in route.segments
    ] == [
        (2, 0, 30),
        (1, 60, 60),
    ]
    assert route.segments[0].end_reason is FarmingBoundaryReason.CAMP_CHANGE

    # With no retained current camp, equal normalized distance resolves by ID.
    tie = ParsedMatch(players=[_player([(0, 7.5, 0.0)])])
    assert build_farming_routes(tie)[0].points[0].camp_id == 1


@pytest.mark.parametrize(
    ("points", "config", "reason"),
    [
        (
            [(0, 0.0, 0.0), (61, 0.0, 0.0)],
            FarmingRouteConfig(max_sample_gap_ticks=60),
            FarmingBoundaryReason.SAMPLE_GAP,
        ),
        (
            [(0, 0.0, 0.0), (30, 101.0, 0.0)],
            FarmingRouteConfig(max_contiguous_speed=100.0),
            FarmingBoundaryReason.LARGE_JUMP,
        ),
    ],
)
def test_discontinuities_split_same_camp_and_never_merge(
    monkeypatch: pytest.MonkeyPatch,
    points: list[tuple[int, float, float]],
    config: FarmingRouteConfig,
    reason: FarmingBoundaryReason,
) -> None:
    monkeypatch.setattr(farming, "load_camp_zones", lambda: _catalog(_zone(1, 0, radius=1000)))

    route = build_farming_routes(ParsedMatch(players=[_player(points)]), config=config)[0]

    assert len(route.segments) == 2
    assert route.segments[0].end_reason is reason
    assert route.segments[1].start_reason is reason
    assert not any(segment.micro_exit_merged for segment in route.segments)


def test_short_same_camp_exit_merges_without_claiming_continuous_membership(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(farming, "load_camp_zones", lambda: _catalog(_zone(1, 0)))
    match = ParsedMatch(players=[_player([(0, 0.0, 0.0), (30, 11.0, 0.0), (60, 0.0, 0.0)])])

    route = build_farming_routes(match, config=FarmingRouteConfig(merge_gap_ticks=60))[0]
    segment = route.segments[0]

    assert len(route.segments) == 1
    assert segment.micro_exit_merged is True
    assert segment.sample_count == 3
    assert segment.in_zone_sample_count == 2
    assert segment.position_coverage == pytest.approx(1.0)
    assert segment.evidence_strength is FarmingEvidenceStrength.TRANSIT_LIKE


def test_neutral_death_via_damage_source_is_strong_factual_evidence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(farming, "load_camp_zones", lambda: _catalog(_zone(1, 0)))
    player = _player(
        [(0, 0.0, 0.0), (150, 1.0, 0.0)],
        times=[0, 150],
        xp=[100, 250],
        gold=[200, 350],
    )
    match = ParsedMatch(
        players=[player],
        combat_log=[
            CombatLogEntry(
                tick=90,
                log_type=CombatLogType.DEATH,
                attacker_name="npc_dota_axe_soldier",
                damage_source_name=player.hero_name,
                target_name="npc_dota_neutral_centaur_khan",
                location_x=1.0,
                location_y=0.0,
            )
        ],
    )

    segment = build_farming_routes(match)[0].segments[0]

    assert segment.neutral_kills == 1
    assert segment.evidence_strength is FarmingEvidenceStrength.STRONG
    assert segment.evidence_reasons == ["neutral_death"]
    assert segment.window_xp_delta == 150
    assert segment.window_total_earned_gold_delta == 150
    assert segment.evidence_gaps == []


def test_damage_is_weak_and_stale_resources_stay_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(farming, "load_camp_zones", lambda: _catalog(_zone(1, 0)))
    player = _player(
        [(100, 0.0, 0.0), (130, 1.0, 0.0)],
        times=[0, 300],
        xp=[100, 200],
        gold=[100, 200],
    )
    match = ParsedMatch(
        players=[player],
        combat_log=[
            CombatLogEntry(
                tick=110,
                log_type=CombatLogType.DAMAGE,
                attacker_name=player.hero_name,
                target_name="npc_dota_neutral_satyr_hellcaller",
                value=75,
                location_x=0.0,
                location_y=0.0,
            ),
            CombatLogEntry(
                tick=115,
                log_type=CombatLogType.DEATH,
                attacker_name=player.hero_name,
                target_name="npc_dota_neutral_satyr_hellcaller",
                location_x=100.0,
                location_y=100.0,
            ),
        ],
    )

    route = build_farming_routes(match, config=FarmingRouteConfig(resource_max_age_ticks=10))[0]
    segment = route.segments[0]

    assert segment.neutral_kills == 0
    assert segment.neutral_damage == 75
    assert segment.evidence_strength is FarmingEvidenceStrength.WEAK
    assert segment.window_xp_delta is None
    assert segment.window_total_earned_gold_delta is None
    assert route.status == "partial"
    assert set(segment.evidence_gaps) == {
        "xp_endpoint_samples_unavailable",
        "gold_endpoint_samples_unavailable",
    }


def test_short_resource_only_touch_remains_transit_like(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(farming, "load_camp_zones", lambda: _catalog(_zone(1, 0)))
    player = _player(
        [(0, 0.0, 0.0), (30, 1.0, 0.0)],
        times=[0, 30],
        xp=[100, 112],
        gold=[200, 201],
    )

    segment = build_farming_routes(ParsedMatch(players=[player]))[0].segments[0]

    assert segment.evidence_strength is FarmingEvidenceStrength.TRANSIT_LIKE
    assert segment.evidence_reasons == ["window_xp_gain", "window_gold_gain"]


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"max_sample_gap_ticks": 0}, "max_sample_gap_ticks"),
        ({"max_contiguous_speed": 0}, "max_contiguous_speed"),
        ({"merge_gap_ticks": -1}, "merge_gap_ticks"),
        ({"min_weak_dwell_ticks": -1}, "min_weak_dwell_ticks"),
        ({"resource_max_age_ticks": -1}, "resource_max_age_ticks"),
    ],
)
def test_route_config_rejects_invalid_values(kwargs: dict, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        FarmingRouteConfig(**kwargs)
