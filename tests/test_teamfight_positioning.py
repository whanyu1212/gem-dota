"""Tests for evidence-aware teamfight positioning analysis."""

from __future__ import annotations

import math

import pytest

from gem.analysis.teamfight_positioning import (
    EngagementStartSource,
    EvidenceCompleteness,
    SnapshotKind,
    build_teamfight_positioning,
)
from gem.extractors.teamfights import Teamfight, TeamfightPlayer
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
    hero_name: str | None = None,
    positions: list[tuple[int, float, float]] | None = None,
) -> ParsedPlayer:
    return ParsedPlayer(
        player_id=player_id,
        hero_name=hero_name or f"npc_dota_hero_{player_id}",
        player_name=f"player {player_id}",
        team=team if team is not None else (2 if player_id < 5 else 3),
        position_log=positions or [],
    )


def _fight(
    *,
    first_death_tick: int = 1_000,
    start_tick: int = 550,
    end_tick: int = 1_450,
    active_ids: tuple[int, ...] = (),
) -> Teamfight:
    stats = [TeamfightPlayer(player_id=player_id) for player_id in range(10)]
    for player_id in active_ids:
        stats[player_id].damage_dealt = 1
    return Teamfight(
        start_tick=start_tick,
        end_tick=end_tick,
        last_death_tick=first_death_tick,
        deaths=1,
        first_death_tick=first_death_tick,
        players=stats,
    )


def _visibility(
    player_id: int,
    *,
    tick: int,
    radiant: VisibilityState = VisibilityState.UNKNOWN,
    dire: VisibilityState = VisibilityState.UNKNOWN,
) -> HeroVisibilityEvent:
    return HeroVisibilityEvent(
        tick=tick,
        player_id=player_id,
        hero_name=f"npc_dota_hero_{player_id}",
        entity_index=player_id,
        entity_serial=1,
        radiant_state=radiant,
        dire_state=dire,
    )


def _reveal(
    *,
    target_name: str,
    tick: int = 900,
    end_tick: int | None = 1_100,
    modifier_name: str = "modifier_bounty_hunter_track",
    caster_team: int = 3,
    lifecycle: VisionModifierLifecycleStatus = VisionModifierLifecycleStatus.REMOVED,
    close: VisionModifierCloseEvidence = VisionModifierCloseEvidence.OBSERVED,
    pairing: VisionModifierPairingStatus = VisionModifierPairingStatus.EXACT,
    target_is_hero: bool = True,
    target_is_illusion: bool = False,
    target_team: int = 2,
) -> VisionModifierEvent:
    return VisionModifierEvent(
        tick=tick,
        end_tick=end_tick,
        modifier_name=modifier_name,
        target_name=target_name,
        caster_name="npc_dota_hero_bounty_hunter",
        caster_team=caster_team,
        semantic=VisionModifierSemantic.DIRECT_TARGET_REVEAL,
        lifecycle_status=lifecycle,
        close_evidence=close,
        pairing_status=pairing,
        target_is_hero=target_is_hero,
        target_is_illusion=target_is_illusion,
        target_team=target_team,
    )


def _at_engagement(match: ParsedMatch, **kwargs: object):
    result = build_teamfight_positioning(match, **kwargs)
    return result[0].snapshots[1]


def test_four_logical_moments_preserved_with_clamping_and_provenance() -> None:
    match = ParsedMatch(
        game_start_tick=900,
        players=[_player(0, positions=[(1_000, 0.0, 0.0)])],
        teamfights=[_fight(first_death_tick=1_000, end_tick=1_000)],
    )

    result = build_teamfight_positioning(match)[0]

    assert result.fight_index == 0
    assert result.engagement_start_tick == 1_000
    assert result.engagement_start_source is EngagementStartSource.FIRST_DEATH_FALLBACK
    assert [snapshot.kind for snapshot in result.snapshots] == list(SnapshotKind)
    assert [snapshot.tick for snapshot in result.snapshots] == [900, 1_000, 1_000, 1_000]
    assert len(result.snapshots) == 4


def test_pre_engagement_clamps_to_zero_without_usable_game_start() -> None:
    match = ParsedMatch(
        game_start_tick=2_000,
        players=[_player(0, positions=[(100, 0.0, 0.0)])],
        teamfights=[_fight(first_death_tick=100, start_tick=0, end_tick=550)],
    )

    result = build_teamfight_positioning(match, pre_engagement_ticks=300)[0]

    assert result.snapshots[0].tick == 0


def test_default_first_death_tick_uses_observed_last_death_with_provenance() -> None:
    fight = Teamfight(
        start_tick=550,
        end_tick=1_450,
        last_death_tick=1_000,
        deaths=1,
        players=[TeamfightPlayer(player_id=i) for i in range(10)],
    )
    match = ParsedMatch(
        players=[_player(0, positions=[(700, 1.0, 2.0), (1_000, 3.0, 4.0)])],
        teamfights=[fight],
    )

    result = build_teamfight_positioning(match)[0]

    assert result.engagement_start_tick == 1_000
    assert result.first_death_tick == 1_000
    assert result.engagement_start_source is EngagementStartSource.LAST_DEATH_FALLBACK
    assert [snapshot.tick for snapshot in result.snapshots] == [700, 1_000, 1_000, 1_450]


def test_invalid_death_ticks_fall_back_to_nonnegative_fight_window_start() -> None:
    fight = Teamfight(
        start_tick=550,
        end_tick=1_450,
        first_death_tick=100,
        last_death_tick=2_000,
        deaths=1,
    )

    result = build_teamfight_positioning(ParsedMatch(teamfights=[fight]))[0]

    assert result.engagement_start_tick == 550
    assert result.engagement_start_source is EngagementStartSource.FIGHT_WINDOW_START_FALLBACK
    assert [snapshot.tick for snapshot in result.snapshots] == [250, 550, 550, 1_450]


def test_fresh_stale_and_missing_positions_keep_sample_provenance() -> None:
    match = ParsedMatch(
        players=[
            _player(0, positions=[(1_000, 1.0, 2.0)]),
            _player(1, positions=[(939, 3.0, 4.0)]),
            _player(5),
        ],
        teamfights=[_fight()],
    )

    heroes = {hero.player_id: hero for hero in _at_engagement(match).heroes}

    assert (heroes[0].x, heroes[0].y) == (1.0, 2.0)
    assert heroes[0].sample_tick == 1_000
    assert heroes[0].sample_age_ticks == 0
    assert heroes[1].x is None and heroes[1].y is None
    assert heroes[1].sample_tick == 939
    assert heroes[1].sample_age_ticks == 61
    assert "position_sample_stale" in heroes[1].evidence_gaps
    assert heroes[5].x is None and heroes[5].y is None
    assert heroes[5].sample_tick is None
    assert heroes[5].sample_age_ticks is None
    assert "position_sample_unavailable" in heroes[5].evidence_gaps


def test_centroids_rms_spread_and_nearest_distances_use_only_fresh_positions() -> None:
    match = ParsedMatch(
        players=[
            _player(0, positions=[(1_000, 0.0, 0.0)]),
            _player(1, positions=[(1_000, 6.0, 8.0)]),
            _player(5, positions=[(1_000, 10.0, 0.0)]),
        ],
        teamfights=[_fight()],
    )

    snapshot = _at_engagement(match)
    heroes = {hero.player_id: hero for hero in snapshot.heroes}

    assert snapshot.radiant.completeness is EvidenceCompleteness.COMPLETE
    assert snapshot.radiant.expected_count == 2
    assert snapshot.radiant.positioned_count == 2
    assert snapshot.radiant.unpositioned_count == 0
    assert snapshot.radiant.centroid_x == pytest.approx(3.0)
    assert snapshot.radiant.centroid_y == pytest.approx(4.0)
    assert snapshot.radiant.rms_spread == pytest.approx(5.0)
    assert snapshot.dire.centroid_x == pytest.approx(10.0)
    assert snapshot.dire.centroid_y == pytest.approx(0.0)
    assert snapshot.centroid_distance == pytest.approx(math.sqrt(65.0))
    assert heroes[0].distance_to_team_centroid == pytest.approx(5.0)
    assert heroes[0].nearest_ally_distance == pytest.approx(10.0)
    assert heroes[0].nearest_enemy_distance == pytest.approx(10.0)
    assert heroes[1].nearest_enemy_distance == pytest.approx(math.sqrt(80.0))
    assert heroes[5].nearest_ally_distance is None


def test_complete_partial_and_unavailable_team_evidence() -> None:
    match = ParsedMatch(
        players=[
            _player(0, positions=[(1_000, 0.0, 0.0)]),
            _player(1),
            _player(5),
            _player(6),
        ],
        teamfights=[_fight()],
    )

    snapshot = _at_engagement(match)

    assert snapshot.radiant.completeness is EvidenceCompleteness.PARTIAL
    assert snapshot.radiant.positioned_count == 1
    assert snapshot.radiant.unpositioned_count == 1
    assert snapshot.dire.completeness is EvidenceCompleteness.UNAVAILABLE
    assert snapshot.dire.positioned_count == 0
    assert snapshot.dire.unpositioned_count == 2
    assert snapshot.dire.centroid_x is None
    assert snapshot.dire.rms_spread is None
    assert snapshot.centroid_distance is None


def test_active_participants_and_nearby_nonparticipants_are_separate() -> None:
    match = ParsedMatch(
        players=[
            _player(0, positions=[(1_000, 0.0, 0.0)]),
            _player(1, positions=[(1_000, 3.0, 4.0)]),
            _player(2, positions=[(1_000, 6.0, 0.0)]),
            _player(5),
        ],
        teamfights=[_fight(active_ids=(0,))],
    )

    snapshot = _at_engagement(match, nearby_radius=5.0)
    heroes = {hero.player_id: hero for hero in snapshot.heroes}

    assert snapshot.active_participant_centroid_x == pytest.approx(0.0)
    assert snapshot.active_participant_centroid_y == pytest.approx(0.0)
    assert heroes[0].active_participant is True
    assert heroes[0].near_fight is True
    assert heroes[1].active_participant is False
    assert heroes[1].near_fight is True
    assert heroes[2].active_participant is False
    assert heroes[2].near_fight is False
    assert heroes[5].near_fight is None


def test_authoritative_opponent_visibility_preserves_tri_state() -> None:
    match = ParsedMatch(
        players=[
            _player(0, positions=[(1_000, 0.0, 0.0)]),
            _player(1, positions=[(1_000, 1.0, 0.0)]),
            _player(5, positions=[(1_000, 2.0, 0.0)]),
        ],
        teamfights=[_fight()],
        hero_visibility_events=[
            _visibility(0, tick=900, dire=VisibilityState.HIDDEN),
            _visibility(1, tick=900, dire=VisibilityState.VISIBLE),
        ],
    )

    heroes = {hero.player_id: hero for hero in _at_engagement(match).heroes}

    assert heroes[0].visibility is VisibilityState.HIDDEN
    assert heroes[1].visibility is VisibilityState.VISIBLE
    assert heroes[5].visibility is VisibilityState.UNKNOWN
    assert "visibility_unavailable" in heroes[5].evidence_gaps


def test_canonical_roster_deduplicates_slots_and_rejects_invalid_entries() -> None:
    canonical = _player(0, hero_name="npc_dota_hero_axe", positions=[(1_000, 1.0, 2.0)])
    duplicate = _player(0, hero_name="npc_dota_hero_illusion", positions=[(1_000, 9.0, 9.0)])
    match = ParsedMatch(
        players=[
            canonical,
            duplicate,
            _player(10, team=2, positions=[(1_000, 3.0, 3.0)]),
            _player(5, team=0, positions=[(1_000, 4.0, 4.0)]),
        ],
        teamfights=[_fight()],
    )

    heroes = _at_engagement(match).heroes

    assert len(heroes) == 1
    assert heroes[0].player_id == 0
    assert heroes[0].hero_name == "npc_dota_hero_axe"
    assert (heroes[0].x, heroes[0].y) == (1.0, 2.0)


def test_smoke_context_requires_observed_half_open_participant_interval() -> None:
    players = [
        _player(0, positions=[(1_000, 0.0, 0.0)]),
        _player(1, positions=[(1_000, 1.0, 0.0)]),
        _player(2, positions=[(1_000, 2.0, 0.0)]),
    ]
    match = ParsedMatch(
        players=players,
        teamfights=[_fight()],
        smoke_events=[
            SmokeEvent(
                tick=850,
                activator=players[0].hero_name,
                team=2,
                participants=[
                    SmokeParticipant(
                        hero_name=players[0].hero_name,
                        player_id=0,
                        applied_tick=900,
                        removed_tick=1_100,
                    ),
                    SmokeParticipant(
                        hero_name=players[1].hero_name,
                        player_id=1,
                        applied_tick=900,
                        removed_tick=1_000,
                    ),
                    SmokeParticipant(
                        hero_name=players[2].hero_name,
                        player_id=2,
                        applied_tick=900,
                        removed_tick=None,
                    ),
                ],
            )
        ],
    )

    heroes = {hero.player_id: hero for hero in _at_engagement(match).heroes}

    assert heroes[0].active_smoke_activation_tick == 850
    assert heroes[1].active_smoke_activation_tick is None
    assert heroes[2].active_smoke_activation_tick is None
    assert "smoke_removal_unobserved" in heroes[2].evidence_gaps


def test_direct_reveals_require_bounded_authoritative_lifecycle_evidence() -> None:
    players = [
        _player(0, positions=[(1_000, 0.0, 0.0)]),
        _player(1, positions=[(1_000, 1.0, 0.0)]),
        _player(2, positions=[(1_000, 2.0, 0.0)]),
        _player(3, positions=[(1_000, 3.0, 0.0)]),
        _player(4, positions=[(1_000, 4.0, 0.0)]),
    ]
    match = ParsedMatch(
        players=players,
        teamfights=[_fight()],
        vision_modifiers=[
            _reveal(target_name=players[0].hero_name),
            _reveal(
                target_name=players[0].hero_name,
                modifier_name="modifier_slardar_amplify_damage",
                pairing=VisionModifierPairingStatus.UNIQUE_FALLBACK,
            ),
            _reveal(target_name=players[1].hero_name, end_tick=1_000),
            _reveal(
                target_name=players[2].hero_name,
                end_tick=None,
                lifecycle=VisionModifierLifecycleStatus.OPEN,
                close=VisionModifierCloseEvidence.UNOBSERVED,
            ),
            _reveal(
                target_name=players[3].hero_name,
                pairing=VisionModifierPairingStatus.AMBIGUOUS,
            ),
            _reveal(
                target_name=players[4].hero_name,
                target_is_illusion=True,
            ),
        ],
    )

    heroes = {hero.player_id: hero for hero in _at_engagement(match).heroes}

    assert heroes[0].active_reveal_modifiers == (
        "modifier_bounty_hunter_track",
        "modifier_slardar_amplify_damage",
    )
    assert heroes[1].active_reveal_modifiers == ()
    assert heroes[2].active_reveal_modifiers == ()
    assert "direct_reveal_lifecycle_incomplete" in heroes[2].evidence_gaps
    assert "direct_reveal_close_unobserved" in heroes[2].evidence_gaps
    assert heroes[3].active_reveal_modifiers == ()
    assert "direct_reveal_pairing_ambiguous" in heroes[3].evidence_gaps
    assert heroes[4].active_reveal_modifiers == ()
    assert "direct_reveal_target_not_canonical_hero" in heroes[4].evidence_gaps


def test_duplicate_hero_names_do_not_resolve_direct_reveals() -> None:
    duplicated_name = "npc_dota_hero_meepo"
    match = ParsedMatch(
        players=[
            _player(0, hero_name=duplicated_name, positions=[(1_000, 0.0, 0.0)]),
            _player(1, hero_name=duplicated_name, positions=[(1_000, 1.0, 0.0)]),
        ],
        teamfights=[_fight()],
        vision_modifiers=[_reveal(target_name=duplicated_name)],
    )

    heroes = _at_engagement(match).heroes

    assert all(hero.active_reveal_modifiers == () for hero in heroes)
    assert all("direct_reveal_target_identity_ambiguous" in hero.evidence_gaps for hero in heroes)


def test_overlapping_fights_remain_distinct_and_source_ordered() -> None:
    first = _fight(first_death_tick=1_000, start_tick=550, end_tick=1_450)
    second = _fight(first_death_tick=1_100, start_tick=650, end_tick=1_550)
    match = ParsedMatch(
        players=[_player(0, positions=[(1_000, 0.0, 0.0), (1_100, 1.0, 0.0)])],
        teamfights=[second, first],
    )

    results = build_teamfight_positioning(match)

    assert [result.fight_index for result in results] == [0, 1]
    assert [result.first_death_tick for result in results] == [1_100, 1_000]
    assert results[0].snapshots is not results[1].snapshots


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"pre_engagement_ticks": -1}, "pre_engagement_ticks"),
        ({"max_position_age_ticks": -1}, "max_position_age_ticks"),
        ({"nearby_radius": -1.0}, "nearby_radius"),
        ({"nearby_radius": math.nan}, "nearby_radius"),
    ],
)
def test_argument_validation(kwargs: dict[str, object], message: str) -> None:
    with pytest.raises(ValueError, match=message):
        build_teamfight_positioning(ParsedMatch(), **kwargs)  # type: ignore[arg-type]


@pytest.mark.integration
@pytest.mark.slow
def test_real_replay_positioning_is_deterministic_and_provenance_bounded(
    canonical_parsed_match: ParsedMatch,
) -> None:
    first = build_teamfight_positioning(canonical_parsed_match)
    second = build_teamfight_positioning(canonical_parsed_match)

    assert first == second
    assert first
    assert any(
        hero.x is not None
        for fight in first
        for snapshot in fight.snapshots
        for hero in snapshot.heroes
    )
    for fight in first:
        assert [snapshot.kind for snapshot in fight.snapshots] == list(SnapshotKind)
        for snapshot in fight.snapshots:
            assert len({hero.player_id for hero in snapshot.heroes}) == len(snapshot.heroes)
            for hero in snapshot.heroes:
                assert (hero.x is None) is (hero.y is None)
                if hero.x is not None:
                    assert hero.sample_tick is not None
                    assert hero.sample_age_ticks is not None
                    assert hero.sample_age_ticks <= 60
                    assert (hero.x, hero.y) != (0.0, 0.0)
