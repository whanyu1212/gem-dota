"""Evidence-aware positioning snapshots for detected teamfights.

Reference: ``odota/parser src/main/java/opendota/CreateParsedDataBlob.java``
for the teamfight windows consumed by this post-parse analysis. Position,
visibility, smoke, and modifier evidence comes from Gem's parsed timelines.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

from gem.analysis.combat import is_active_teamfight_participant
from gem.analysis.spatial import position_sample_at_tick

if TYPE_CHECKING:
    from gem.extractors.teamfights import Teamfight
    from gem.results.models import ParsedMatch, ParsedPlayer, VisibilityState


class SnapshotKind(str, Enum):
    """Logical moment represented by a positioning snapshot.

    Attributes:
        PRE_ENGAGEMENT: Configured lookback before engagement-start evidence.
        ENGAGEMENT_START: Best-supported engagement-start moment.
        FIRST_DEATH: Best-supported first hero-death moment. For legacy or
            manually constructed fights without a usable first-death tick, the
            engagement source records which conservative fallback was used.
        FIGHT_END: Detected teamfight window end.
    """

    __str__ = str.__str__

    PRE_ENGAGEMENT = "pre_engagement"
    ENGAGEMENT_START = "engagement_start"
    FIRST_DEATH = "first_death"
    FIGHT_END = "fight_end"


class EngagementStartSource(str, Enum):
    """Provenance for the engagement-start tick.

    Attributes:
        FIRST_DEATH_FALLBACK: No earlier observed engagement boundary exists,
            so the first hero death is used without implying combat began then.
        LAST_DEATH_FALLBACK: First-death metadata is missing or outside the
            fight window, so the observed last-death tick is used.
        FIGHT_WINDOW_START_FALLBACK: Neither death tick is usable, so the
            detected fight-window start is used without claiming a death there.
    """

    __str__ = str.__str__

    FIRST_DEATH_FALLBACK = "first_death_fallback"
    LAST_DEATH_FALLBACK = "last_death_fallback"
    FIGHT_WINDOW_START_FALLBACK = "fight_window_start_fallback"


class EvidenceCompleteness(str, Enum):
    """Position-evidence completeness for one team at one snapshot.

    Attributes:
        COMPLETE: Every expected canonical hero has a fresh position.
        PARTIAL: At least one, but not every, expected hero has a fresh position.
        UNAVAILABLE: No expected canonical hero has a fresh position.
    """

    __str__ = str.__str__

    COMPLETE = "complete"
    PARTIAL = "partial"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True, slots=True)
class HeroPositionEvidence:
    """Position and contextual evidence for one canonical player hero.

    Attributes:
        player_id: Canonical logical player slot from 0 through 9.
        hero_name: Internal NPC hero name.
        player_name: Player display name when available.
        team: Team number (2=Radiant, 3=Dire).
        active_participant: Whether the fight recorded direct combat involvement.
        near_fight: Whether the fresh hero position is within the configured
            radius of the fresh active-participant centroid, or ``None`` when
            either side of that comparison is unavailable.
        x: Fresh sampled world x coordinate, or ``None`` when missing or stale.
        y: Fresh sampled world y coordinate, or ``None`` when missing or stale.
        sample_tick: Tick of the nearest position sample, even when stale.
        sample_age_ticks: Absolute distance from the snapshot to the sample.
        visibility: Authoritative visibility to the opposing team.
        distance_to_team_centroid: Distance from this fresh position to its
            team's fresh-position centroid.
        nearest_ally_distance: Distance to the nearest other fresh allied hero.
        nearest_enemy_distance: Distance to the nearest fresh opposing hero.
        active_smoke_activation_tick: Smoke item-use tick when a bounded,
            observed participant interval is active.
        active_reveal_modifiers: Names of bounded direct-target reveal modifiers
            active for the opposing team at this snapshot.
        evidence_gaps: Stable labels for material missing or ambiguous evidence.
    """

    player_id: int
    hero_name: str
    player_name: str
    team: int
    active_participant: bool
    near_fight: bool | None
    x: float | None
    y: float | None
    sample_tick: int | None
    sample_age_ticks: int | None
    visibility: VisibilityState
    distance_to_team_centroid: float | None
    nearest_ally_distance: float | None
    nearest_enemy_distance: float | None
    active_smoke_activation_tick: int | None
    active_reveal_modifiers: tuple[str, ...]
    evidence_gaps: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class TeamPositionSummary:
    """Fresh-position geometry and completeness for one team.

    Attributes:
        team: Team number (2=Radiant, 3=Dire).
        expected_count: Number of canonical player heroes expected for the team.
        positioned_count: Number with a fresh position at this snapshot.
        unpositioned_count: Number without a fresh position.
        completeness: Complete, partial, or unavailable position evidence.
        centroid_x: Mean fresh-position x coordinate, or ``None``.
        centroid_y: Mean fresh-position y coordinate, or ``None``.
        rms_spread: Root-mean-square distance of fresh positions from the
            centroid, or ``None`` when no fresh position exists.
    """

    team: int
    expected_count: int
    positioned_count: int
    unpositioned_count: int
    completeness: EvidenceCompleteness
    centroid_x: float | None
    centroid_y: float | None
    rms_spread: float | None


@dataclass(frozen=True, slots=True)
class FightPositionSnapshot:
    """All canonical hero evidence at one logical teamfight moment.

    Attributes:
        kind: Logical snapshot kind.
        tick: Exact replay tick queried.
        heroes: Canonical heroes in ascending player-slot order.
        radiant: Radiant fresh-position summary.
        dire: Dire fresh-position summary.
        centroid_distance: Distance between team centroids when both exist.
        active_participant_centroid_x: Combined fresh active-participant
            centroid x coordinate, or ``None``.
        active_participant_centroid_y: Combined fresh active-participant
            centroid y coordinate, or ``None``.
    """

    kind: SnapshotKind
    tick: int
    heroes: tuple[HeroPositionEvidence, ...]
    radiant: TeamPositionSummary
    dire: TeamPositionSummary
    centroid_distance: float | None
    active_participant_centroid_x: float | None
    active_participant_centroid_y: float | None


@dataclass(frozen=True, slots=True)
class TeamfightPositioning:
    """Four evidence-aware positioning snapshots for one detected teamfight.

    Attributes:
        fight_index: Deterministic zero-based index in ``match.teamfights``.
        start_tick: Detector's padded teamfight-window start tick.
        engagement_start_tick: Best-supported engagement-start tick.
        first_death_tick: Best-supported first-death snapshot tick. Consult
            ``engagement_start_source`` before treating it as exact.
        end_tick: Detector's teamfight-window end tick.
        engagement_start_source: Provenance for ``engagement_start_tick``.
        snapshots: Four logical moments in enum declaration order. Logical
            records remain distinct even when two or more ticks coincide.
    """

    fight_index: int
    start_tick: int
    engagement_start_tick: int
    first_death_tick: int
    end_tick: int
    engagement_start_source: EngagementStartSource
    snapshots: tuple[FightPositionSnapshot, ...]


@dataclass(slots=True)
class _HeroDraft:
    player: ParsedPlayer
    active_participant: bool
    x: float | None
    y: float | None
    sample_tick: int | None
    sample_age_ticks: int | None
    visibility: VisibilityState
    active_smoke_activation_tick: int | None
    active_reveal_modifiers: tuple[str, ...]
    evidence_gaps: list[str]


def build_teamfight_positioning(
    match: ParsedMatch,
    *,
    pre_engagement_ticks: int = 300,
    max_position_age_ticks: int = 60,
    nearby_radius: float = 3000.0,
) -> list[TeamfightPositioning]:
    """Build evidence-aware positioning records for detected teamfights.

    Engagement start currently uses the best-supported death tick as an
    explicitly labelled fallback. A positive first-death tick is accepted only
    when it falls inside the detected fight window; otherwise the last-death
    tick, then the fight-window start, is used with distinct provenance. Every
    output retains all four logical snapshots even when two logical moments
    have the same tick.

    Args:
        match: Parsed match containing players, teamfights, and evidence
            timelines.
        pre_engagement_ticks: Lookback from engagement start for the first
            logical snapshot.
        max_position_age_ticks: Maximum absolute age of a usable position.
        nearby_radius: Radius around the fresh active-participant centroid used
            to classify nearby heroes.

    Returns:
        One positioning record per source teamfight, in source order.

    Raises:
        ValueError: If any configurable bound is negative or not nonnegative.
    """
    if pre_engagement_ticks < 0:
        raise ValueError("pre_engagement_ticks must be nonnegative")
    if max_position_age_ticks < 0:
        raise ValueError("max_position_age_ticks must be nonnegative")
    if not nearby_radius >= 0:
        raise ValueError("nearby_radius must be nonnegative")

    roster = _canonical_roster(match)
    hero_name_counts: dict[str, int] = {}
    for player in roster:
        if player.hero_name:
            hero_name_counts[player.hero_name] = hero_name_counts.get(player.hero_name, 0) + 1

    results: list[TeamfightPositioning] = []
    for fight_index, fight in enumerate(match.teamfights):
        engagement_tick, engagement_source = _resolve_engagement_tick(fight)
        lower_bound = _pre_engagement_lower_bound(match.game_start_tick, engagement_tick)
        pre_tick = max(lower_bound, engagement_tick - pre_engagement_ticks)
        moments = (
            (SnapshotKind.PRE_ENGAGEMENT, pre_tick),
            (SnapshotKind.ENGAGEMENT_START, engagement_tick),
            (SnapshotKind.FIRST_DEATH, engagement_tick),
            (SnapshotKind.FIGHT_END, fight.end_tick),
        )
        snapshots = tuple(
            _build_snapshot(
                match,
                fight,
                roster,
                hero_name_counts,
                kind,
                tick,
                max_position_age_ticks=max_position_age_ticks,
                nearby_radius=nearby_radius,
            )
            for kind, tick in moments
        )
        results.append(
            TeamfightPositioning(
                fight_index=fight_index,
                start_tick=fight.start_tick,
                engagement_start_tick=engagement_tick,
                first_death_tick=engagement_tick,
                end_tick=fight.end_tick,
                engagement_start_source=engagement_source,
                snapshots=snapshots,
            )
        )

    return results


def _resolve_engagement_tick(
    fight: Teamfight,
) -> tuple[int, EngagementStartSource]:
    """Return a usable in-window death tick and its evidence provenance."""
    if fight.start_tick <= fight.first_death_tick <= fight.end_tick and fight.first_death_tick > 0:
        return fight.first_death_tick, EngagementStartSource.FIRST_DEATH_FALLBACK
    if fight.start_tick <= fight.last_death_tick <= fight.end_tick and fight.last_death_tick > 0:
        return fight.last_death_tick, EngagementStartSource.LAST_DEATH_FALLBACK
    return max(0, fight.start_tick), EngagementStartSource.FIGHT_WINDOW_START_FALLBACK


def _canonical_roster(match: ParsedMatch) -> tuple[ParsedPlayer, ...]:
    players_by_id: dict[int, ParsedPlayer] = {}
    for player in match.players:
        if player.team in (2, 3) and 0 <= player.player_id <= 9:
            players_by_id.setdefault(player.player_id, player)
    return tuple(players_by_id[player_id] for player_id in sorted(players_by_id))


def _pre_engagement_lower_bound(game_start_tick: int | None, engagement_tick: int) -> int:
    if game_start_tick is not None and 0 <= game_start_tick <= engagement_tick:
        return game_start_tick
    return 0


def _build_snapshot(
    match: ParsedMatch,
    fight: Teamfight,
    roster: tuple[ParsedPlayer, ...],
    hero_name_counts: dict[str, int],
    kind: SnapshotKind,
    tick: int,
    *,
    max_position_age_ticks: int,
    nearby_radius: float,
) -> FightPositionSnapshot:
    from gem.analysis.vision import hero_visibility_at
    from gem.results.models import VisibilityState

    fight_players: dict[int, object] = {}
    for player_stats in fight.players:
        player_id = getattr(player_stats, "player_id", None)
        if isinstance(player_id, int):
            fight_players.setdefault(player_id, player_stats)

    drafts: list[_HeroDraft] = []
    for player in roster:
        sample = position_sample_at_tick(player, tick)
        gaps: list[str] = []
        if sample is None:
            x = y = None
            sample_tick = sample_age_ticks = None
            gaps.append("position_sample_unavailable")
        else:
            sample_tick = sample.sample_tick
            sample_age_ticks = sample.age_ticks
            if sample.age_ticks > max_position_age_ticks:
                x = y = None
                gaps.append("position_sample_stale")
            else:
                x, y = sample.x, sample.y

        opponent = 3 if player.team == 2 else 2
        visibility = hero_visibility_at(
            match,
            player_id=player.player_id,
            observing_team=opponent,
            tick=tick,
        )
        if visibility is VisibilityState.UNKNOWN:
            gaps.append("visibility_unavailable")

        smoke_tick, smoke_gaps = _smoke_context(
            match,
            player,
            hero_name_counts,
            tick,
        )
        reveal_modifiers, reveal_gaps = _reveal_context(
            match,
            player,
            hero_name_counts,
            tick,
        )
        gaps.extend(smoke_gaps)
        gaps.extend(reveal_gaps)

        stats = fight_players.get(player.player_id)
        drafts.append(
            _HeroDraft(
                player=player,
                active_participant=(stats is not None and is_active_teamfight_participant(stats)),
                x=x,
                y=y,
                sample_tick=sample_tick,
                sample_age_ticks=sample_age_ticks,
                visibility=visibility,
                active_smoke_activation_tick=smoke_tick,
                active_reveal_modifiers=reveal_modifiers,
                evidence_gaps=_deduplicate(gaps),
            )
        )

    summaries = {team: _team_summary(drafts, team) for team in (2, 3)}
    active_positions = [
        (draft.x, draft.y)
        for draft in drafts
        if draft.active_participant and draft.x is not None and draft.y is not None
    ]
    active_centroid_x: float | None
    active_centroid_y: float | None
    if active_positions:
        active_centroid_x = sum(x for x, _ in active_positions) / len(active_positions)
        active_centroid_y = sum(y for _, y in active_positions) / len(active_positions)
    else:
        active_centroid_x = None
        active_centroid_y = None

    heroes = tuple(
        _finalize_hero(
            draft,
            drafts,
            summaries[draft.player.team],
            active_centroid_x,
            active_centroid_y,
            nearby_radius,
        )
        for draft in drafts
    )

    radiant = summaries[2]
    dire = summaries[3]
    centroid_distance = None
    if (
        radiant.centroid_x is not None
        and radiant.centroid_y is not None
        and dire.centroid_x is not None
        and dire.centroid_y is not None
    ):
        centroid_distance = math.dist(
            (radiant.centroid_x, radiant.centroid_y),
            (dire.centroid_x, dire.centroid_y),
        )

    return FightPositionSnapshot(
        kind=kind,
        tick=tick,
        heroes=heroes,
        radiant=radiant,
        dire=dire,
        centroid_distance=centroid_distance,
        active_participant_centroid_x=active_centroid_x,
        active_participant_centroid_y=active_centroid_y,
    )


def _team_summary(drafts: list[_HeroDraft], team: int) -> TeamPositionSummary:
    expected = [draft for draft in drafts if draft.player.team == team]
    positioned = [draft for draft in expected if draft.x is not None and draft.y is not None]
    expected_count = len(expected)
    positioned_count = len(positioned)

    if positioned_count == 0:
        completeness = EvidenceCompleteness.UNAVAILABLE
        centroid_x = centroid_y = rms_spread = None
    else:
        completeness = (
            EvidenceCompleteness.COMPLETE
            if positioned_count == expected_count
            else EvidenceCompleteness.PARTIAL
        )
        centroid_x = sum(draft.x for draft in positioned if draft.x is not None) / positioned_count
        centroid_y = sum(draft.y for draft in positioned if draft.y is not None) / positioned_count
        rms_spread = math.sqrt(
            sum(
                (draft.x - centroid_x) ** 2 + (draft.y - centroid_y) ** 2
                for draft in positioned
                if draft.x is not None and draft.y is not None
            )
            / positioned_count
        )

    return TeamPositionSummary(
        team=team,
        expected_count=expected_count,
        positioned_count=positioned_count,
        unpositioned_count=expected_count - positioned_count,
        completeness=completeness,
        centroid_x=centroid_x,
        centroid_y=centroid_y,
        rms_spread=rms_spread,
    )


def _finalize_hero(
    draft: _HeroDraft,
    drafts: list[_HeroDraft],
    summary: TeamPositionSummary,
    active_centroid_x: float | None,
    active_centroid_y: float | None,
    nearby_radius: float,
) -> HeroPositionEvidence:
    x = draft.x
    y = draft.y
    if (
        x is not None
        and y is not None
        and active_centroid_x is not None
        and active_centroid_y is not None
    ):
        near_fight = math.dist((x, y), (active_centroid_x, active_centroid_y)) <= nearby_radius
    else:
        near_fight = None

    distance_to_team_centroid = None
    if (
        x is not None
        and y is not None
        and summary.centroid_x is not None
        and summary.centroid_y is not None
    ):
        distance_to_team_centroid = math.dist(
            (x, y),
            (summary.centroid_x, summary.centroid_y),
        )

    nearest_ally_distance = _nearest_distance(draft, drafts, same_team=True)
    nearest_enemy_distance = _nearest_distance(draft, drafts, same_team=False)

    return HeroPositionEvidence(
        player_id=draft.player.player_id,
        hero_name=draft.player.hero_name,
        player_name=draft.player.player_name,
        team=draft.player.team,
        active_participant=draft.active_participant,
        near_fight=near_fight,
        x=draft.x,
        y=draft.y,
        sample_tick=draft.sample_tick,
        sample_age_ticks=draft.sample_age_ticks,
        visibility=draft.visibility,
        distance_to_team_centroid=distance_to_team_centroid,
        nearest_ally_distance=nearest_ally_distance,
        nearest_enemy_distance=nearest_enemy_distance,
        active_smoke_activation_tick=draft.active_smoke_activation_tick,
        active_reveal_modifiers=draft.active_reveal_modifiers,
        evidence_gaps=tuple(draft.evidence_gaps),
    )


def _nearest_distance(
    subject: _HeroDraft,
    drafts: list[_HeroDraft],
    *,
    same_team: bool,
) -> float | None:
    if subject.x is None or subject.y is None:
        return None
    distances = []
    for other in drafts:
        if other is subject or other.x is None or other.y is None:
            continue
        teams_match = other.player.team == subject.player.team
        if teams_match is not same_team:
            continue
        distances.append(math.dist((subject.x, subject.y), (other.x, other.y)))
    return min(distances) if distances else None


def _smoke_context(
    match: ParsedMatch,
    player: ParsedPlayer,
    hero_name_counts: dict[str, int],
    tick: int,
) -> tuple[int | None, list[str]]:
    active_ticks: list[int] = []
    gaps: list[str] = []
    for smoke in match.smoke_events:
        for participant in smoke.participants:
            if not _smoke_participant_matches(participant, player, hero_name_counts):
                continue
            if participant.applied_tick > tick:
                continue
            if participant.removed_tick is None:
                gaps.append("smoke_removal_unobserved")
                continue
            if participant.removed_tick <= participant.applied_tick:
                gaps.append("smoke_interval_invalid")
                continue
            if tick < participant.removed_tick:
                active_ticks.append(smoke.tick)
    return (max(active_ticks) if active_ticks else None, _deduplicate(gaps))


def _smoke_participant_matches(
    participant: object,
    player: ParsedPlayer,
    hero_name_counts: dict[str, int],
) -> bool:
    participant_player_id = getattr(participant, "player_id", None)
    if participant_player_id is not None:
        return participant_player_id == player.player_id
    participant_name = getattr(participant, "hero_name", "")
    return (
        bool(player.hero_name)
        and participant_name == player.hero_name
        and hero_name_counts.get(player.hero_name) == 1
    )


def _reveal_context(
    match: ParsedMatch,
    player: ParsedPlayer,
    hero_name_counts: dict[str, int],
    tick: int,
) -> tuple[tuple[str, ...], list[str]]:
    from gem.results.models import (
        VisionModifierCloseEvidence,
        VisionModifierLifecycleStatus,
        VisionModifierPairingStatus,
        VisionModifierSemantic,
    )

    if not player.hero_name:
        return (), []

    opponent = 3 if player.team == 2 else 2
    active: list[str] = []
    gaps: list[str] = []
    for event in match.vision_modifiers:
        if event.semantic is not VisionModifierSemantic.DIRECT_TARGET_REVEAL:
            continue
        if event.target_name != player.hero_name or event.tick > tick:
            continue
        if event.end_tick is not None and tick >= event.end_tick:
            continue
        if hero_name_counts.get(player.hero_name) != 1:
            gaps.append("direct_reveal_target_identity_ambiguous")
            continue
        if not event.target_is_hero or event.target_is_illusion:
            gaps.append("direct_reveal_target_not_canonical_hero")
            continue
        if event.target_team in (2, 3) and event.target_team != player.team:
            gaps.append("direct_reveal_target_team_conflict")
            continue
        if event.caster_team == 0:
            gaps.append("direct_reveal_caster_team_unknown")
            continue
        if event.caster_team != opponent:
            continue

        usable = True
        if event.lifecycle_status not in (
            VisionModifierLifecycleStatus.REMOVED,
            VisionModifierLifecycleStatus.EXPIRED,
        ):
            gaps.append("direct_reveal_lifecycle_incomplete")
            usable = False
        if event.pairing_status not in (
            VisionModifierPairingStatus.EXACT,
            VisionModifierPairingStatus.UNIQUE_FALLBACK,
        ):
            gaps.append("direct_reveal_pairing_ambiguous")
            usable = False
        if (
            event.end_tick is None
            or event.close_evidence is not VisionModifierCloseEvidence.OBSERVED
        ):
            gaps.append("direct_reveal_close_unobserved")
            usable = False
        if usable:
            active.append(event.modifier_name)

    return (tuple(dict.fromkeys(active)), _deduplicate(gaps))


def _deduplicate(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))
