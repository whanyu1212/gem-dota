"""Tests for conservative smoke-to-fight post-parse insights."""

from __future__ import annotations

import math

import pytest

from gem.analysis.smoke_fight import (
    EvidenceCompleteness,
    FightCentroidSource,
    FollowUpBoundary,
    FollowUpKind,
    SmokeFightStatus,
    TeamRelation,
    build_smoke_fight_insights,
)
from gem.analysis.vision import PointVisionStatus
from gem.combat.log import CombatLogEntry, CombatLogType
from gem.extractors.objectives import BarracksKill, RoshanKill, TormentorKill, TowerKill
from gem.extractors.teamfights import Teamfight, TeamfightPlayer
from gem.extractors.wards import WardEvent
from gem.results.models import (
    HeroVisibilityEvent,
    ParsedMatch,
    ParsedPlayer,
    SmokeEvent,
    SmokeParticipant,
    VisibilityState,
    VisionModifierCloseEvidence,
    VisionModifierEvent,
    VisionModifierLifecycleStatus,
    VisionModifierPairingStatus,
    VisionModifierSemantic,
)


def _player(
    player_id: int,
    *,
    team: int | None = None,
    hero: str | None = None,
    positions: list[tuple[int, float, float]] | None = None,
) -> ParsedPlayer:
    return ParsedPlayer(
        player_id=player_id,
        team=team if team is not None else (2 if player_id < 5 else 3),
        hero_name=hero or f"npc_dota_hero_{player_id}",
        player_name=f"player {player_id}",
        position_log=positions or [],
    )


def _participant(
    player_id: int | None,
    *,
    hero: str | None = None,
    applied_tick: int = 1_000,
    removed_tick: int | None = 1_100,
    applied_game_time_s: int | None = 10,
    removed_game_time_s: int | None = 13,
) -> SmokeParticipant:
    return SmokeParticipant(
        hero_name=hero or f"npc_dota_hero_{player_id}",
        player_id=player_id,
        applied_tick=applied_tick,
        removed_tick=removed_tick,
        modifier_duration_s=20.0,
        modifier_elapsed_duration_s=3.0,
        applied_game_time_s=applied_game_time_s,
        removed_game_time_s=removed_game_time_s,
    )


def _smoke(
    tick: int = 1_000,
    *,
    team: int = 2,
    participants: list[SmokeParticipant] | None = None,
    activation_game_time_s: int | None = 10,
) -> SmokeEvent:
    members = participants if participants is not None else [_participant(0, applied_tick=tick)]
    return SmokeEvent(
        tick=tick,
        activator="npc_dota_hero_0",
        team=team,
        smoked=[member.hero_name for member in members],
        participants=members,
        activation_game_time_s=activation_game_time_s,
    )


def _fight(
    engagement_tick: int,
    *,
    start_tick: int | None = None,
    end_tick: int | None = None,
    active_ids: tuple[int, ...] = (0,),
    first_death_tick: int | None = None,
    centroid: tuple[float, float] | None = None,
) -> Teamfight:
    stats = [TeamfightPlayer(player_id=player_id) for player_id in range(10)]
    for player_id in active_ids:
        stats[player_id].damage_dealt = 1
    return Teamfight(
        start_tick=start_tick if start_tick is not None else engagement_tick - 100,
        end_tick=end_tick if end_tick is not None else engagement_tick + 100,
        first_death_tick=(engagement_tick if first_death_tick is None else first_death_tick),
        last_death_tick=engagement_tick,
        deaths=1,
        radiant_kills=1,
        dire_kills=0,
        winner="radiant",
        centroid_x=centroid[0] if centroid else None,
        centroid_y=centroid[1] if centroid else None,
        centroid_n=1 if centroid else 0,
        players=stats,
    )


def _visibility(
    player_id: int,
    tick: int,
    *,
    dire: VisibilityState,
) -> HeroVisibilityEvent:
    return HeroVisibilityEvent(
        tick=tick,
        player_id=player_id,
        hero_name=f"npc_dota_hero_{player_id}",
        entity_index=player_id,
        entity_serial=1,
        radiant_state=VisibilityState.HIDDEN,
        dire_state=dire,
    )


def _combat(
    tick: int,
    log_type: CombatLogType,
    *,
    attacker: str = "",
    source: str = "",
    target: str = "",
    inflictor: str = "",
    target_is_hero: bool = False,
    game_time_s: int | None = None,
) -> CombatLogEntry:
    return CombatLogEntry(
        tick=tick,
        log_type=log_type,
        attacker_name=attacker,
        damage_source_name=source,
        target_name=target,
        inflictor_name=inflictor,
        target_is_hero=target_is_hero,
        game_time_s=game_time_s,
    )


def test_association_boundaries_preexisting_and_multiple_links_are_stable() -> None:
    smoke = _smoke()
    fights = [
        _fight(900, start_tick=800, end_tick=1_000),
        _fight(1_001),
        _fight(2_800),
        _fight(2_801),
    ]
    match = ParsedMatch(
        players=[_player(0, positions=[(1_001, 0.0, 0.0), (2_800, 0.0, 0.0)])],
        smoke_events=[smoke],
        teamfights=fights,
    )

    insights = build_smoke_fight_insights(match)

    assert [(row.smoke_index, row.fight_index, row.status) for row in insights] == [
        (0, 0, SmokeFightStatus.PREEXISTING),
        (0, 1, SmokeFightStatus.LINKED),
        (0, 2, SmokeFightStatus.LINKED),
    ]
    assert insights[0].active_smoked_player_ids == (0,)
    assert all(row.outcome is None for row in insights if row.status is not SmokeFightStatus.LINKED)


def test_parallel_same_tick_fights_keep_first_death_metadata_separate() -> None:
    smoke = _smoke()
    first = _fight(1_100, active_ids=(0,))
    second = _fight(1_100, active_ids=(0,))
    first.players[0].deaths = 1
    second.players[5].deaths = 1
    match = ParsedMatch(
        players=[
            _player(0, hero="npc_dota_hero_axe", positions=[(1_100, 0.0, 0.0)]),
            _player(5, hero="npc_dota_hero_lina", positions=[(1_100, 5_000.0, 0.0)]),
        ],
        smoke_events=[smoke],
        teamfights=[first, second],
        combat_log=[
            _combat(1_100, CombatLogType.DEATH, target="npc_dota_hero_axe"),
            _combat(1_100, CombatLogType.DEATH, target="npc_dota_hero_lina"),
        ],
    )

    insights = build_smoke_fight_insights(match)

    assert [insight.first_death.target_name for insight in insights if insight.first_death] == [
        "npc_dota_hero_axe",
        "npc_dota_hero_lina",
    ]


def test_temporal_candidate_requires_active_member_not_proximity() -> None:
    match = ParsedMatch(
        players=[
            _player(0, positions=[(1_100, 0.0, 0.0)]),
            _player(5, positions=[(1_100, 0.0, 0.0)]),
        ],
        smoke_events=[_smoke()],
        teamfights=[_fight(1_100, active_ids=(5,), centroid=(0.0, 0.0))],
    )

    insight = build_smoke_fight_insights(match)[0]

    assert insight.status is SmokeFightStatus.TEMPORAL_ONLY
    assert insight.active_smoked_player_ids == ()
    assert insight.members[0].sampled_near_fight is not None
    assert insight.outcome is None


def test_supported_smokes_contending_for_one_fight_are_ambiguous() -> None:
    match = ParsedMatch(
        players=[
            _player(0, positions=[(1_100, 0.0, 0.0)]),
            _player(1, positions=[(1_100, 10.0, 0.0)]),
        ],
        smoke_events=[
            _smoke(participants=[_participant(0)]),
            _smoke(tick=1_010, participants=[_participant(1, applied_tick=1_010)]),
        ],
        teamfights=[_fight(1_100, active_ids=(0, 1))],
    )

    insights = build_smoke_fight_insights(match)

    assert [row.status for row in insights] == [
        SmokeFightStatus.AMBIGUOUS,
        SmokeFightStatus.AMBIGUOUS,
    ]
    assert all(row.outcome is None for row in insights)
    assert all(row.follow_up_window is None and row.follow_ups == () for row in insights)


def test_no_candidate_keeps_lifecycle_events_and_unavailable_evidence() -> None:
    match = ParsedMatch(
        players=[_player(0)],
        smoke_events=[_smoke(participants=[_participant(0, removed_tick=1_030)])],
    )

    insight = build_smoke_fight_insights(match)[0]

    assert insight.status is SmokeFightStatus.NO_CANDIDATE
    assert insight.fight_index is None
    assert insight.evidence_completeness is EvidenceCompleteness.UNAVAILABLE
    assert insight.first_member_removal is not None
    assert insight.first_member_removal.tick == 1_030
    assert insight.first_member_removal.tick_delta == 30
    assert insight.first_member_removal.game_time_delta_s == 3


def test_exact_sequence_spatial_evidence_and_point_vision_stay_separate() -> None:
    hero0 = "npc_dota_hero_0"
    hero1 = "npc_dota_hero_1"
    smoke = _smoke(
        participants=[
            _participant(0, removed_tick=1_030, removed_game_time_s=11),
            _participant(1, removed_tick=1_080, removed_game_time_s=14),
        ]
    )
    reveal = VisionModifierEvent(
        tick=1_025,
        end_tick=1_090,
        modifier_name="modifier_bounty_hunter_track",
        target_name=hero0,
        caster_name="npc_dota_hero_5",
        caster_team=3,
        semantic=VisionModifierSemantic.DIRECT_TARGET_REVEAL,
        lifecycle_status=VisionModifierLifecycleStatus.REMOVED,
        close_evidence=VisionModifierCloseEvidence.OBSERVED,
        pairing_status=VisionModifierPairingStatus.EXACT,
        target_is_hero=True,
        target_team=2,
        add_game_time_s=12,
    )
    combat_log = [
        _combat(
            1_040,
            CombatLogType.ITEM,
            source=hero0,
            inflictor="item_smoke_of_deceit",
        ),
        _combat(
            1_041,
            CombatLogType.DAMAGE,
            attacker=hero0,
            source="npc_dota_hero_5",
            target=hero1,
            target_is_hero=True,
        ),
        _combat(
            1_042,
            CombatLogType.DAMAGE,
            source=hero0,
            target="npc_dota_creep",
            target_is_hero=False,
        ),
        _combat(
            1_043,
            CombatLogType.ABILITY,
            source=hero0,
            target="npc_dota_hero_5",
            inflictor="axe_berserkers_call",
            game_time_s=12,
        ),
        _combat(
            1_050,
            CombatLogType.DEATH,
            attacker=hero0,
            target="npc_dota_hero_5",
            game_time_s=13,
        ),
    ]
    match = ParsedMatch(
        game_end_tick=2_000,
        players=[
            _player(
                0,
                positions=[(1_005, 0.0, 0.0), (1_050, 0.0, 0.0)],
            ),
            _player(
                1,
                positions=[(1_015, 3.0, 4.0), (1_050, 3.0, 4.0)],
            ),
            _player(5, positions=[(1_050, 100.0, 0.0)]),
        ],
        smoke_events=[smoke],
        teamfights=[_fight(1_050, active_ids=(0, 5))],
        hero_visibility_events=[
            _visibility(0, 1_000, dire=VisibilityState.HIDDEN),
            _visibility(0, 1_020, dire=VisibilityState.VISIBLE),
        ],
        vision_modifiers=[reveal],
        combat_log=combat_log,
    )

    insight = build_smoke_fight_insights(match)[0]

    assert insight.status is SmokeFightStatus.LINKED
    assert insight.first_member_removal is not None
    assert insight.first_member_removal.tick == 1_030
    assert insight.first_member_removal.tick_delta == 30
    assert insight.first_member_removal.game_time_delta_s == 1
    assert insight.first_authoritative_visible is not None
    assert insight.first_authoritative_visible.tick == 1_020
    assert insight.first_direct_reveal is not None
    assert insight.first_direct_reveal.tick == 1_025
    assert insight.first_member_action is not None
    assert insight.first_member_action.tick == 1_043
    assert insight.first_member_action.source_index == 3
    assert insight.first_death is not None
    assert insight.first_death.tick == 1_050
    assert insight.first_death.game_time_delta_s == 3
    assert insight.fight_end is not None and insight.fight_end.tick == 1_150
    assert [event.kind.value for event in insight.exact_events] == [
        "activation",
        "authoritative_visible",
        "direct_reveal",
        "member_removal",
        "member_action",
        "first_death",
        "fight_end",
    ]

    formation = insight.engagement_formation
    assert formation is not None
    assert formation.completeness is EvidenceCompleteness.COMPLETE
    assert formation.centroid_x == pytest.approx(1.5)
    assert formation.centroid_y == pytest.approx(2.0)
    assert formation.rms_spread == pytest.approx(2.5)
    assert formation.max_pairwise_distance == pytest.approx(5.0)
    assert [member.sample_tick for member in formation.members] == [1_050, 1_050]
    assert insight.near_fight_centroid_source is FightCentroidSource.ENGAGEMENT_ACTIVE_PARTICIPANTS
    assert insight.sampled_near_fight_spread_ticks == 10

    member = insight.members[0]
    assert member.authoritative_visibility is VisibilityState.VISIBLE
    assert member.point_vision is not None
    assert member.point_vision.status is PointVisionStatus.SUPPORTED
    assert member.sampled_near_fight is not None
    assert member.sampled_near_fight.tick == 1_005
    assert member.engagement_position is not None
    assert member.engagement_position.sample_tick == 1_050


def test_invalid_source_first_death_is_not_replaced_by_positioning_fallback() -> None:
    fight = _fight(
        1_100,
        first_death_tick=0,
        active_ids=(0,),
        centroid=(0.0, 0.0),
    )
    match = ParsedMatch(
        players=[_player(0, positions=[(1_100, 0.0, 0.0)])],
        smoke_events=[_smoke()],
        teamfights=[fight],
    )

    insight = build_smoke_fight_insights(match)[0]

    assert insight.status is SmokeFightStatus.LINKED
    assert insight.first_death is None
    assert "exact_first_death_unavailable" in insight.evidence_gaps
    assert insight.members[0].sampled_near_fight is not None
    assert insight.members[0].sampled_near_fight.tick == 1_100


def test_near_fight_falls_back_to_death_centroid_with_explicit_provenance() -> None:
    match = ParsedMatch(
        players=[_player(0, positions=[(1_010, 10.0, 0.0)])],
        smoke_events=[_smoke()],
        teamfights=[_fight(1_100, active_ids=(0,), centroid=(0.0, 0.0))],
    )

    insight = build_smoke_fight_insights(match, max_position_age_ticks=10)[0]

    assert insight.near_fight_centroid_source is FightCentroidSource.FIGHT_DEATHS
    assert insight.members[0].sampled_near_fight is not None
    assert insight.members[0].sampled_near_fight.centroid_source is FightCentroidSource.FIGHT_DEATHS
    assert insight.members[0].point_vision is None


def test_followups_are_half_open_truncated_at_next_smoke_and_allocated_once() -> None:
    hero0 = "npc_dota_hero_0"
    hero5 = "npc_dota_hero_5"
    smoke = _smoke()
    next_smoke = _smoke(tick=1_550, participants=[])
    match = ParsedMatch(
        game_end_tick=1_600,
        players=[
            _player(0, hero=hero0, positions=[(1_100, 0.0, 0.0), (1_400, 0.0, 0.0)]),
            _player(5, hero=hero5, positions=[(1_100, 10.0, 0.0), (1_400, 10.0, 0.0)]),
        ],
        smoke_events=[smoke, next_smoke],
        teamfights=[
            _fight(1_100, end_tick=1_200, active_ids=(0, 5)),
            _fight(1_400, end_tick=1_500, active_ids=(0, 5)),
        ],
        towers=[
            TowerKill(
                tick=1_500,
                team=2,
                killer=hero5,
                tower_name="npc_dota_badguys_tower1_top",
            )
        ],
        barracks=[
            BarracksKill(
                tick=1_549,
                team=3,
                killer="npc_dota_summon",
                killer_source=hero0,
                barracks_name="npc_dota_badguys_melee_rax_top",
            )
        ],
        roshans=[
            RoshanKill(tick=1_550, killer=hero0, kill_number=1),
        ],
        tormentors=[
            TormentorKill(tick=1_200, killer=hero0, killer_player_id=0, kill_number=1),
        ],
        wards=[
            WardEvent(
                tick=1_499,
                player_id=0,
                placer=hero0,
                ward_type="observer",
                team=3,
                x=0.0,
                y=0.0,
                expires_tick=None,
                killed_tick=None,
                killer="",
            ),
            WardEvent(
                tick=1_300,
                player_id=0,
                placer=hero0,
                ward_type="sentry",
                team=2,
                x=0.0,
                y=0.0,
                expires_tick=None,
                killed_tick=None,
                killer="",
            ),
        ],
    )

    insights = build_smoke_fight_insights(match)
    linked = [row for row in insights if row.status is SmokeFightStatus.LINKED]

    assert [row.fight_index for row in linked] == [0, 1]
    assert linked[0].follow_up_window is not None
    assert linked[0].follow_up_window.start_tick == 1_200
    assert linked[0].follow_up_window.end_tick == 1_550
    assert linked[0].follow_up_window.end_reasons == (FollowUpBoundary.NEXT_SAME_TEAM_SMOKE,)
    assert [(event.kind, event.tick) for event in linked[0].follow_ups] == [
        (FollowUpKind.TORMENTOR, 1_200),
        (FollowUpKind.OBSERVER_WARD, 1_499),
    ]
    assert [(event.kind, event.tick) for event in linked[1].follow_ups] == [
        (FollowUpKind.TOWER, 1_500),
        (FollowUpKind.BARRACKS, 1_549),
    ]
    tower = linked[1].follow_ups[0]
    assert tower.actor_team == 3
    assert tower.relation is TeamRelation.OPPONENT
    barracks = linked[1].follow_ups[1]
    assert barracks.actor_team == 2
    assert barracks.relation is TeamRelation.SMOKE_TEAM
    all_allocated = [event for row in linked for event in row.follow_ups]
    assert len(all_allocated) == 4
    assert all(event.tick != 1_550 for event in all_allocated)


def test_unresolved_observer_owner_preserves_entity_team_attribution() -> None:
    match = ParsedMatch(
        players=[_player(0)],
        smoke_events=[_smoke()],
        teamfights=[_fight(1_100, end_tick=1_200, active_ids=(0,))],
        wards=[
            WardEvent(
                tick=1_250,
                player_id=-1,
                placer="npc_dota_hero_unresolved",
                ward_type="observer",
                team=2,
                x=0.0,
                y=0.0,
                expires_tick=None,
                killed_tick=None,
                killer="",
            )
        ],
    )

    insight = build_smoke_fight_insights(match)[0]

    assert insight.status is SmokeFightStatus.LINKED
    assert len(insight.follow_ups) == 1
    observer = insight.follow_ups[0]
    assert observer.actor_name == "npc_dota_hero_unresolved"
    assert observer.actor_player_id is None
    assert observer.actor_team == 2
    assert observer.relation is TeamRelation.SMOKE_TEAM


def test_follow_up_window_clamps_earlier_external_bounds_to_fight_end() -> None:
    match = ParsedMatch(
        game_end_tick=1_150,
        players=[_player(0), _player(1)],
        smoke_events=[
            _smoke(tick=1_000, participants=[_participant(0)]),
            _smoke(tick=1_150, participants=[_participant(1, applied_tick=1_150)]),
        ],
        teamfights=[
            _fight(
                1_200,
                start_tick=1_150,
                end_tick=1_550,
                active_ids=(0,),
            )
        ],
    )

    linked = build_smoke_fight_insights(match)[0]

    assert linked.status is SmokeFightStatus.LINKED
    assert linked.follow_up_window is not None
    assert linked.follow_up_window.start_tick == 1_550
    assert linked.follow_up_window.end_tick == 1_550
    assert FollowUpBoundary.GAME_END in linked.follow_up_window.end_reasons
    assert FollowUpBoundary.NEXT_SAME_TEAM_SMOKE in linked.follow_up_window.end_reasons


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"fight_window_ticks": -1}, "fight_window_ticks"),
        ({"follow_up_ticks": -1}, "follow_up_ticks"),
        ({"nearby_radius": -1.0}, "nearby_radius"),
        ({"nearby_radius": math.nan}, "nearby_radius"),
        ({"max_position_age_ticks": -1}, "max_position_age_ticks"),
    ],
)
def test_invalid_bounds(kwargs: dict[str, object], message: str) -> None:
    with pytest.raises(ValueError, match=message):
        build_smoke_fight_insights(ParsedMatch(), **kwargs)
