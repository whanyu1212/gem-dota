"""Conservative post-parse associations between smoke activations and fights.

Combat-log event semantics follow Clarity's ``CombatLog.java`` at pinned
revision ``7fb3f1d0``; teamfight window semantics follow OpenDota's
``CreateParsedDataBlob.java`` at pinned revision ``e58a668f`` (see
``CLAUDE.md``). Exact replay events and sampled spatial evidence deliberately
remain separate.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, replace
from enum import Enum
from typing import TYPE_CHECKING

from gem.analysis._shared import infer_match_end_tick
from gem.analysis.combat import is_active_teamfight_participant
from gem.analysis.smoke import SmokeAnalysis, SmokeGroupStatus, build_smoke_analysis
from gem.analysis.teamfight_positioning import (
    EvidenceCompleteness,
    FightPositionSnapshot,
    SnapshotKind,
    TeamfightPositioning,
    build_teamfight_positioning,
)

if TYPE_CHECKING:
    from gem.analysis.vision import PointVisionAssessment
    from gem.combat.log import CombatLogEntry
    from gem.extractors.teamfights import Teamfight
    from gem.results.models import (
        ParsedMatch,
        SmokeEvent,
        VisibilityState,
        VisionModifierEvent,
    )


_SMOKE_ITEM = "item_smoke_of_deceit"


class SmokeFightStatus(str, Enum):
    """Deterministic association state for one smoke/fight observation."""

    __str__ = str.__str__

    LINKED = "linked"
    TEMPORAL_ONLY = "temporal_only"
    AMBIGUOUS = "ambiguous"
    PREEXISTING = "preexisting"
    NO_CANDIDATE = "no_candidate"


class ExactEventKind(str, Enum):
    """Kinds of exact events retained in an insight sequence."""

    __str__ = str.__str__

    ACTIVATION = "activation"
    MEMBER_REMOVAL = "member_removal"
    AUTHORITATIVE_VISIBLE = "authoritative_visible"
    DIRECT_REVEAL = "direct_reveal"
    MEMBER_ACTION = "member_action"
    FIRST_DEATH = "first_death"
    FIGHT_END = "fight_end"


class FightCentroidSource(str, Enum):
    """Provenance of the center used for sampled near-fight arrival evidence."""

    __str__ = str.__str__

    ENGAGEMENT_ACTIVE_PARTICIPANTS = "engagement_active_participants"
    FIGHT_DEATHS = "fight_deaths"


class FollowUpKind(str, Enum):
    """Kinds of bounded post-fight events."""

    __str__ = str.__str__

    TOWER = "tower"
    BARRACKS = "barracks"
    ROSHAN = "roshan"
    TORMENTOR = "tormentor"
    OBSERVER_WARD = "observer_ward"


class TeamRelation(str, Enum):
    """Actor-team relation to the smoke team."""

    __str__ = str.__str__

    SMOKE_TEAM = "smoke_team"
    OPPONENT = "opponent"
    UNKNOWN = "unknown"


class FollowUpBoundary(str, Enum):
    """Evidence that bounded a post-fight follow-up window."""

    __str__ = str.__str__

    CONFIGURED_LIMIT = "configured_limit"
    GAME_END = "game_end"
    NEXT_SAME_TEAM_SMOKE = "next_same_team_smoke"


@dataclass(frozen=True, slots=True)
class ExactEventEvidence:
    """One exact source event with activation-relative timing.

    Attributes:
        kind: Semantic event kind.
        tick: Exact replay tick from the source record.
        game_time_s: Pause-aware source game time when recorded.
        tick_delta: Raw tick difference from smoke activation.
        game_time_delta_s: Pause-aware difference from activation when both
            source times exist.
        provenance: Source collection or analysis that supplied the event.
        source_index: Stable index within that source when applicable.
        player_id: Canonical player slot associated with the event.
        hero_name: Associated canonical hero name.
        source_name: Action, modifier, or actor name when applicable.
        target_name: Event target name when applicable.
    """

    kind: ExactEventKind
    tick: int
    game_time_s: int | None
    tick_delta: int
    game_time_delta_s: int | None
    provenance: str
    source_index: int | None = None
    player_id: int | None = None
    hero_name: str = ""
    source_name: str = ""
    target_name: str = ""


@dataclass(frozen=True, slots=True)
class MemberPositionEvidence:
    """One smoke member's positioning-snapshot provenance."""

    player_id: int | None
    hero_name: str
    active_participant: bool
    x: float | None
    y: float | None
    sample_tick: int | None
    sample_age_ticks: int | None
    evidence_gaps: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class FormationEvidence:
    """Filtered smoke-member geometry at one existing fight snapshot."""

    kind: SnapshotKind
    tick: int
    expected_count: int
    positioned_count: int
    completeness: EvidenceCompleteness
    centroid_x: float | None
    centroid_y: float | None
    rms_spread: float | None
    max_pairwise_distance: float | None
    members: tuple[MemberPositionEvidence, ...]


@dataclass(frozen=True, slots=True)
class SampledNearFightEvidence:
    """Earliest raw member-position sample observed near the fight center."""

    player_id: int
    hero_name: str
    tick: int
    x: float
    y: float
    distance: float
    centroid_source: FightCentroidSource


@dataclass(frozen=True, slots=True)
class SmokeFightMemberInsight:
    """Per-smoke-member fight participation, visibility, and spatial evidence."""

    participant_index: int
    player_id: int | None
    hero_name: str
    resolved: bool
    active_participant: bool
    authoritative_visibility: VisibilityState
    point_vision: PointVisionAssessment | None
    pre_engagement_position: MemberPositionEvidence | None
    engagement_position: MemberPositionEvidence | None
    sampled_near_fight: SampledNearFightEvidence | None
    evidence_gaps: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class FightOutcome:
    """Factual source fight result, credited only to a unique link."""

    deaths: int
    radiant_kills: int
    dire_kills: int
    winner: str


@dataclass(frozen=True, slots=True)
class FollowUpWindow:
    """Half-open window used to associate post-fight raw events."""

    start_tick: int
    end_tick: int
    end_reasons: tuple[FollowUpBoundary, ...]


@dataclass(frozen=True, slots=True)
class FollowUpEvent:
    """One raw objective or observer placement allocated to a unique link."""

    kind: FollowUpKind
    source_index: int
    tick: int
    game_time_s: int | None
    tick_delta: int
    game_time_delta_s: int | None
    actor_name: str
    actor_player_id: int | None
    actor_team: int | None
    relation: TeamRelation
    subject_name: str


@dataclass(frozen=True, slots=True)
class SmokeFightInsight:
    """Evidence-first observation for one smoke and zero or one source fight."""

    smoke_index: int
    fight_index: int | None
    status: SmokeFightStatus
    evidence_completeness: EvidenceCompleteness
    smoke_team: int
    activator: str
    smoke_lifecycle_status: SmokeGroupStatus
    activation: ExactEventEvidence
    first_member_removal: ExactEventEvidence | None
    first_authoritative_visible: ExactEventEvidence | None
    first_direct_reveal: ExactEventEvidence | None
    first_member_action: ExactEventEvidence | None
    first_death: ExactEventEvidence | None
    fight_end: ExactEventEvidence | None
    active_smoked_player_ids: tuple[int, ...]
    members: tuple[SmokeFightMemberInsight, ...]
    pre_engagement_formation: FormationEvidence | None
    engagement_formation: FormationEvidence | None
    sampled_near_fight_spread_ticks: int | None
    near_fight_centroid_source: FightCentroidSource | None
    outcome: FightOutcome | None
    follow_up_window: FollowUpWindow | None
    follow_ups: tuple[FollowUpEvent, ...]
    evidence_gaps: tuple[str, ...]

    @property
    def exact_events(self) -> tuple[ExactEventEvidence, ...]:
        """Return present exact events in chronological, deterministic order."""
        events = (
            self.activation,
            self.first_member_removal,
            self.first_authoritative_visible,
            self.first_direct_reveal,
            self.first_member_action,
            self.first_death,
            self.fight_end,
        )
        kind_rank = {kind: rank for rank, kind in enumerate(ExactEventKind)}
        return tuple(
            sorted(
                (event for event in events if event is not None),
                key=lambda event: (
                    event.tick,
                    kind_rank[event.kind],
                    event.source_index if event.source_index is not None else -1,
                ),
            )
        )


@dataclass(frozen=True, slots=True)
class _Association:
    smoke_index: int
    fight_index: int | None
    positioning: TeamfightPositioning | None
    active_member_ids: tuple[int, ...]
    provisional: SmokeFightStatus


@dataclass(frozen=True, slots=True)
class _RawFollowUp:
    kind: FollowUpKind
    source_index: int
    event: object


def build_smoke_fight_insights(
    match: ParsedMatch,
    *,
    fight_window_ticks: int = 1800,
    follow_up_ticks: int = 1800,
    nearby_radius: float = 3000.0,
    max_position_age_ticks: int = 60,
) -> list[SmokeFightInsight]:
    """Build deterministic smoke-to-fight observations from parsed records.

    A fight whose bounded engagement tick has already been reached at activation
    is emitted as ``preexisting`` and is never credited. Post-activation
    candidates use the inclusive engagement interval
    ``[activation, activation + fight_window_ticks]``. At least one
    resolved smoked member must be an active fight participant to support a
    link. Competing supported smokes make every contender ``ambiguous``.

    Args:
        match: Parsed match containing smoke, fight, position, vision, combat,
            objective, and ward timelines.
        fight_window_ticks: Inclusive post-activation engagement-start window.
        follow_up_ticks: Configured length of the half-open post-fight window.
        nearby_radius: Radius around the selected fight center for sampled
            member-arrival evidence.
        max_position_age_ticks: Freshness bound passed to positioning and point
            vision analysis.

    Returns:
        Insights in smoke source order, then fight source order.

    Raises:
        ValueError: If any configurable bound is negative or ``nearby_radius``
            is not a nonnegative number.
    """
    if fight_window_ticks < 0:
        raise ValueError("fight_window_ticks must be nonnegative")
    if follow_up_ticks < 0:
        raise ValueError("follow_up_ticks must be nonnegative")
    if not nearby_radius >= 0:
        raise ValueError("nearby_radius must be nonnegative")
    if max_position_age_ticks < 0:
        raise ValueError("max_position_age_ticks must be nonnegative")

    smoke_analyses = build_smoke_analysis(match)
    positionings = build_teamfight_positioning(
        match,
        nearby_radius=nearby_radius,
        max_position_age_ticks=max_position_age_ticks,
    )
    associations = _associate(match, positionings, fight_window_ticks)
    supported_by_fight: dict[int, int] = {}
    for association in associations:
        if association.provisional is SmokeFightStatus.LINKED:
            assert association.fight_index is not None
            supported_by_fight[association.fight_index] = (
                supported_by_fight.get(association.fight_index, 0) + 1
            )

    insights: list[SmokeFightInsight] = []
    for association in associations:
        status = association.provisional
        if (
            status is SmokeFightStatus.LINKED
            and association.fight_index is not None
            and supported_by_fight[association.fight_index] > 1
        ):
            status = SmokeFightStatus.AMBIGUOUS
        insights.append(
            _build_insight(
                match,
                smoke_analyses,
                association,
                status,
                follow_up_ticks=follow_up_ticks,
                nearby_radius=nearby_radius,
                max_position_age_ticks=max_position_age_ticks,
            )
        )

    return _allocate_follow_ups(match, insights)


def _associate(
    match: ParsedMatch,
    positionings: list[TeamfightPositioning],
    fight_window_ticks: int,
) -> list[_Association]:
    associations: list[_Association] = []
    for smoke_index, smoke in enumerate(match.smoke_events):
        smoke_records: list[_Association] = []
        resolved_member_ids = tuple(
            dict.fromkeys(
                participant.player_id
                for participant in smoke.participants
                if isinstance(participant.player_id, int)
            )
        )
        for positioning in positionings:
            fight = match.teamfights[positioning.fight_index]
            engagement_tick = positioning.engagement_start_tick
            active_ids = _active_smoked_members(fight, resolved_member_ids)
            if engagement_tick <= smoke.tick <= fight.end_tick:
                smoke_records.append(
                    _Association(
                        smoke_index,
                        positioning.fight_index,
                        positioning,
                        active_ids,
                        SmokeFightStatus.PREEXISTING,
                    )
                )
                continue
            if not smoke.tick <= engagement_tick <= smoke.tick + fight_window_ticks:
                continue

            smoke_records.append(
                _Association(
                    smoke_index,
                    positioning.fight_index,
                    positioning,
                    active_ids,
                    (SmokeFightStatus.LINKED if active_ids else SmokeFightStatus.TEMPORAL_ONLY),
                )
            )

        if smoke_records:
            associations.extend(smoke_records)
        else:
            associations.append(
                _Association(
                    smoke_index,
                    None,
                    None,
                    (),
                    SmokeFightStatus.NO_CANDIDATE,
                )
            )
    return associations


def _active_smoked_members(
    fight: Teamfight,
    member_ids: tuple[int, ...],
) -> tuple[int, ...]:
    active: set[int] = set()
    member_set = set(member_ids)
    for stats in fight.players:
        player_id = getattr(stats, "player_id", None)
        if player_id in member_set and is_active_teamfight_participant(stats):
            active.add(player_id)
    return tuple(player_id for player_id in member_ids if player_id in active)


def _build_insight(
    match: ParsedMatch,
    smoke_analyses: list[SmokeAnalysis],
    association: _Association,
    status: SmokeFightStatus,
    *,
    follow_up_ticks: int,
    nearby_radius: float,
    max_position_age_ticks: int,
) -> SmokeFightInsight:
    smoke = match.smoke_events[association.smoke_index]
    smoke_analysis = smoke_analyses[association.smoke_index]
    activation_time = _optional_int(smoke, "activation_game_time_s", "game_time_s")
    activation = _exact_event(
        ExactEventKind.ACTIVATION,
        smoke.tick,
        activation_time,
        smoke.tick,
        activation_time,
        provenance="smoke_events",
        source_index=association.smoke_index,
        hero_name=smoke.activator,
        source_name=_SMOKE_ITEM,
    )
    first_removal = _first_removal(smoke, activation_time)
    first_visible = _first_visible(
        match,
        smoke,
        smoke_analysis,
        activation_time,
    )

    if association.fight_index is None or association.positioning is None:
        members, member_gaps = _member_insights_without_fight(match, smoke)
        gaps = member_gaps
        if not smoke.participants:
            gaps.append("smoke_members_unavailable")
        if smoke.team not in (2, 3):
            gaps.append("smoke_team_unavailable")
        return SmokeFightInsight(
            smoke_index=association.smoke_index,
            fight_index=None,
            status=status,
            evidence_completeness=EvidenceCompleteness.UNAVAILABLE,
            smoke_team=smoke.team,
            activator=smoke.activator,
            smoke_lifecycle_status=smoke_analysis.status,
            activation=activation,
            first_member_removal=first_removal,
            first_authoritative_visible=first_visible,
            first_direct_reveal=None,
            first_member_action=None,
            first_death=None,
            fight_end=None,
            active_smoked_player_ids=(),
            members=members,
            pre_engagement_formation=None,
            engagement_formation=None,
            sampled_near_fight_spread_ticks=None,
            near_fight_centroid_source=None,
            outcome=None,
            follow_up_window=None,
            follow_ups=(),
            evidence_gaps=tuple(_deduplicate(gaps)),
        )

    fight_index = association.fight_index
    fight = match.teamfights[fight_index]
    positioning = association.positioning
    pre_snapshot = _snapshot(positioning, SnapshotKind.PRE_ENGAGEMENT)
    engagement_snapshot = _snapshot(positioning, SnapshotKind.ENGAGEMENT_START)
    pre_formation = _formation(smoke, pre_snapshot)
    engagement_formation = _formation(smoke, engagement_snapshot)

    valid_first_death_tick = _valid_first_death_tick(fight)
    center, center_source = _fight_center(engagement_snapshot, fight)
    near_samples, near_gaps = _near_fight_samples(
        match,
        smoke,
        center,
        center_source,
        valid_first_death_tick if valid_first_death_tick is not None else fight.end_tick,
        nearby_radius,
    )
    members, member_gaps = _member_insights(
        match,
        smoke,
        fight,
        pre_formation,
        engagement_formation,
        near_samples,
        engagement_snapshot,
        max_position_age_ticks,
    )
    first_reveal, reveal_gaps = _first_direct_reveal(
        match,
        smoke,
        fight,
        activation_time,
    )
    first_action = _first_member_action(match, smoke, fight, activation_time)
    first_death, death_gaps = _first_death(
        match,
        fight,
        fight_index,
        smoke.tick,
        activation_time,
    )
    fight_end = _exact_event(
        ExactEventKind.FIGHT_END,
        fight.end_tick,
        None,
        smoke.tick,
        activation_time,
        provenance="teamfights",
        source_index=fight_index,
    )

    observed_near_ticks = [sample.tick for sample in near_samples.values()]
    spread = max(observed_near_ticks) - min(observed_near_ticks) if observed_near_ticks else None
    completeness = engagement_formation.completeness
    gaps = [*member_gaps, *near_gaps, *reveal_gaps, *death_gaps]
    if pre_formation.completeness is not EvidenceCompleteness.COMPLETE:
        gaps.append("pre_engagement_formation_incomplete")
    if engagement_formation.completeness is not EvidenceCompleteness.COMPLETE:
        gaps.append("engagement_formation_incomplete")
    if first_action is None:
        gaps.append("member_action_unobserved")
    if valid_first_death_tick is None:
        gaps.append("exact_first_death_unavailable")
    if smoke.team not in (2, 3):
        gaps.append("smoke_team_unavailable")

    unique_link = status is SmokeFightStatus.LINKED
    outcome = (
        FightOutcome(
            deaths=fight.deaths,
            radiant_kills=fight.radiant_kills,
            dire_kills=fight.dire_kills,
            winner=fight.winner,
        )
        if unique_link
        else None
    )
    follow_up_window = (
        _follow_up_window(
            match,
            association.smoke_index,
            fight.end_tick,
            follow_up_ticks,
        )
        if unique_link
        else None
    )

    return SmokeFightInsight(
        smoke_index=association.smoke_index,
        fight_index=fight_index,
        status=status,
        evidence_completeness=completeness,
        smoke_team=smoke.team,
        activator=smoke.activator,
        smoke_lifecycle_status=smoke_analysis.status,
        activation=activation,
        first_member_removal=first_removal,
        first_authoritative_visible=first_visible,
        first_direct_reveal=first_reveal,
        first_member_action=first_action,
        first_death=first_death,
        fight_end=fight_end,
        active_smoked_player_ids=association.active_member_ids,
        members=members,
        pre_engagement_formation=pre_formation,
        engagement_formation=engagement_formation,
        sampled_near_fight_spread_ticks=spread,
        near_fight_centroid_source=center_source,
        outcome=outcome,
        follow_up_window=follow_up_window,
        follow_ups=(),
        evidence_gaps=tuple(_deduplicate(gaps)),
    )


def _snapshot(
    positioning: TeamfightPositioning,
    kind: SnapshotKind,
) -> FightPositionSnapshot:
    return next(snapshot for snapshot in positioning.snapshots if snapshot.kind is kind)


def _formation(smoke: SmokeEvent, snapshot: FightPositionSnapshot) -> FormationEvidence:
    heroes = {hero.player_id: hero for hero in snapshot.heroes}
    members: list[MemberPositionEvidence] = []
    positioned: list[tuple[float, float]] = []
    for participant in smoke.participants:
        hero = heroes.get(participant.player_id) if isinstance(participant.player_id, int) else None
        if hero is None:
            gaps = (
                "participant_player_id_unavailable"
                if participant.player_id is None
                else "participant_not_in_positioning_roster",
            )
            member = MemberPositionEvidence(
                player_id=participant.player_id,
                hero_name=participant.hero_name,
                active_participant=False,
                x=None,
                y=None,
                sample_tick=None,
                sample_age_ticks=None,
                evidence_gaps=gaps,
            )
        else:
            member = MemberPositionEvidence(
                player_id=participant.player_id,
                hero_name=participant.hero_name,
                active_participant=hero.active_participant,
                x=hero.x,
                y=hero.y,
                sample_tick=hero.sample_tick,
                sample_age_ticks=hero.sample_age_ticks,
                evidence_gaps=hero.evidence_gaps,
            )
            if hero.x is not None and hero.y is not None:
                positioned.append((hero.x, hero.y))
        members.append(member)

    expected_count = len(members)
    positioned_count = len(positioned)
    completeness = _completeness(expected_count, positioned_count)
    if not positioned:
        centroid_x = centroid_y = rms_spread = max_pairwise = None
    else:
        centroid_x = sum(x for x, _ in positioned) / positioned_count
        centroid_y = sum(y for _, y in positioned) / positioned_count
        rms_spread = math.sqrt(
            sum((x - centroid_x) ** 2 + (y - centroid_y) ** 2 for x, y in positioned)
            / positioned_count
        )
        max_pairwise = max(
            (
                math.dist(left, right)
                for index, left in enumerate(positioned)
                for right in positioned[index + 1 :]
            ),
            default=0.0,
        )
    return FormationEvidence(
        kind=snapshot.kind,
        tick=snapshot.tick,
        expected_count=expected_count,
        positioned_count=positioned_count,
        completeness=completeness,
        centroid_x=centroid_x,
        centroid_y=centroid_y,
        rms_spread=rms_spread,
        max_pairwise_distance=max_pairwise,
        members=tuple(members),
    )


def _completeness(expected: int, observed: int) -> EvidenceCompleteness:
    if expected > 0 and observed == expected:
        return EvidenceCompleteness.COMPLETE
    if observed > 0:
        return EvidenceCompleteness.PARTIAL
    return EvidenceCompleteness.UNAVAILABLE


def _fight_center(
    engagement: FightPositionSnapshot,
    fight: Teamfight,
) -> tuple[tuple[float, float] | None, FightCentroidSource | None]:
    if (
        engagement.active_participant_centroid_x is not None
        and engagement.active_participant_centroid_y is not None
    ):
        return (
            (
                engagement.active_participant_centroid_x,
                engagement.active_participant_centroid_y,
            ),
            FightCentroidSource.ENGAGEMENT_ACTIVE_PARTICIPANTS,
        )
    if fight.centroid_x is not None and fight.centroid_y is not None:
        return (
            (fight.centroid_x, fight.centroid_y),
            FightCentroidSource.FIGHT_DEATHS,
        )
    return (None, None)


def _near_fight_samples(
    match: ParsedMatch,
    smoke: SmokeEvent,
    center: tuple[float, float] | None,
    center_source: FightCentroidSource | None,
    end_tick: int,
    nearby_radius: float,
) -> tuple[dict[int, SampledNearFightEvidence], list[str]]:
    if center is None or center_source is None:
        return ({}, ["near_fight_centroid_unavailable"])
    if end_tick < smoke.tick:
        return ({}, ["near_fight_sample_window_empty"])

    players = {player.player_id: player for player in match.players}
    results: dict[int, SampledNearFightEvidence] = {}
    gaps: list[str] = []
    for participant in smoke.participants:
        player_id = participant.player_id
        if not isinstance(player_id, int):
            continue
        player = players.get(player_id)
        if player is None:
            continue
        eligible = [
            (source_index, sample)
            for source_index, sample in enumerate(player.position_log)
            if smoke.tick <= sample[0] <= end_tick
            and math.dist((sample[1], sample[2]), center) <= nearby_radius
        ]
        if not eligible:
            gaps.append(f"near_fight_sample_unavailable:{player_id}")
            continue
        _, (tick, x, y) = min(eligible, key=lambda item: (item[1][0], item[0]))
        results[player_id] = SampledNearFightEvidence(
            player_id=player_id,
            hero_name=participant.hero_name,
            tick=tick,
            x=x,
            y=y,
            distance=math.dist((x, y), center),
            centroid_source=center_source,
        )
    return (results, gaps)


def _member_insights(
    match: ParsedMatch,
    smoke: SmokeEvent,
    fight: Teamfight,
    pre_formation: FormationEvidence,
    engagement_formation: FormationEvidence,
    near_samples: dict[int, SampledNearFightEvidence],
    engagement_snapshot: FightPositionSnapshot,
    max_position_age_ticks: int,
) -> tuple[tuple[SmokeFightMemberInsight, ...], list[str]]:
    from gem.analysis.vision import assess_point_vision
    from gem.results.models import VisibilityState

    players = {player.player_id: player for player in match.players}
    fight_stats = {
        getattr(stats, "player_id", None): stats
        for stats in fight.players
        if isinstance(getattr(stats, "player_id", None), int)
    }
    engagement_heroes = {hero.player_id: hero for hero in engagement_snapshot.heroes}
    members: list[SmokeFightMemberInsight] = []
    all_gaps: list[str] = []
    for index, participant in enumerate(smoke.participants):
        player_id = participant.player_id
        player = players.get(player_id) if isinstance(player_id, int) else None
        hero = engagement_heroes.get(player_id) if isinstance(player_id, int) else None
        gaps: list[str] = []
        if player_id is None:
            gaps.append("participant_player_id_unavailable")
        elif player is None:
            gaps.append("participant_player_unavailable")

        point_vision = None
        visibility = hero.visibility if hero is not None else VisibilityState.UNKNOWN
        if (
            hero is not None
            and hero.x is not None
            and hero.y is not None
            and player_id is not None
            and smoke.team in (2, 3)
        ):
            opponent = 3 if smoke.team == 2 else 2
            point_vision = assess_point_vision(
                match,
                opponent,
                engagement_snapshot.tick,
                hero.x,
                hero.y,
                target_player_id=player_id,
                max_position_age_ticks=max_position_age_ticks,
            )
        else:
            gaps.append("engagement_point_vision_unavailable")

        stats = fight_stats.get(player_id)
        active = stats is not None and is_active_teamfight_participant(stats)
        member = SmokeFightMemberInsight(
            participant_index=index,
            player_id=player_id,
            hero_name=participant.hero_name,
            resolved=player is not None,
            active_participant=active,
            authoritative_visibility=visibility,
            point_vision=point_vision,
            pre_engagement_position=pre_formation.members[index],
            engagement_position=engagement_formation.members[index],
            sampled_near_fight=(
                near_samples.get(player_id) if isinstance(player_id, int) else None
            ),
            evidence_gaps=tuple(_deduplicate(gaps)),
        )
        members.append(member)
        all_gaps.extend(f"member:{index}:{gap}" for gap in member.evidence_gaps)
    return (tuple(members), all_gaps)


def _member_insights_without_fight(
    match: ParsedMatch,
    smoke: SmokeEvent,
) -> tuple[tuple[SmokeFightMemberInsight, ...], list[str]]:
    from gem.results.models import VisibilityState

    players = {player.player_id: player for player in match.players}
    members: list[SmokeFightMemberInsight] = []
    gaps: list[str] = []
    for index, participant in enumerate(smoke.participants):
        resolved = participant.player_id in players
        member_gaps = () if resolved else ("participant_player_unavailable",)
        members.append(
            SmokeFightMemberInsight(
                participant_index=index,
                player_id=participant.player_id,
                hero_name=participant.hero_name,
                resolved=resolved,
                active_participant=False,
                authoritative_visibility=VisibilityState.UNKNOWN,
                point_vision=None,
                pre_engagement_position=None,
                engagement_position=None,
                sampled_near_fight=None,
                evidence_gaps=member_gaps,
            )
        )
        gaps.extend(f"member:{index}:{gap}" for gap in member_gaps)
    return (tuple(members), gaps)


def _first_removal(
    smoke: SmokeEvent,
    activation_time: int | None,
) -> ExactEventEvidence | None:
    candidates = [
        (index, participant)
        for index, participant in enumerate(smoke.participants)
        if isinstance(participant.removed_tick, int)
    ]
    if not candidates:
        return None
    index, participant = min(candidates, key=lambda item: (item[1].removed_tick, item[0]))
    assert participant.removed_tick is not None
    game_time = _optional_int(participant, "removed_game_time_s", "game_time_s")
    return _exact_event(
        ExactEventKind.MEMBER_REMOVAL,
        participant.removed_tick,
        game_time,
        smoke.tick,
        activation_time,
        provenance="smoke_participants",
        source_index=index,
        player_id=participant.player_id,
        hero_name=participant.hero_name,
    )


def _first_visible(
    match: ParsedMatch,
    smoke: SmokeEvent,
    smoke_analysis: SmokeAnalysis,
    activation_time: int | None,
) -> ExactEventEvidence | None:
    candidates = [
        (index, member)
        for index, member in enumerate(smoke_analysis.members)
        if member.first_visible_tick is not None
    ]
    if not candidates:
        return None
    index, member = min(candidates, key=lambda item: (item[1].first_visible_tick, item[0]))
    assert member.first_visible_tick is not None
    source_event = next(
        (
            event
            for event in match.hero_visibility_events
            if event.player_id == member.player_id and event.tick == member.first_visible_tick
        ),
        None,
    )
    game_time = _optional_int(source_event, "game_time_s") if source_event is not None else None
    return _exact_event(
        ExactEventKind.AUTHORITATIVE_VISIBLE,
        member.first_visible_tick,
        game_time,
        smoke.tick,
        activation_time,
        provenance="smoke_analysis",
        source_index=index,
        player_id=member.player_id,
        hero_name=member.hero_name,
    )


def _first_direct_reveal(
    match: ParsedMatch,
    smoke: SmokeEvent,
    fight: Teamfight,
    activation_time: int | None,
) -> tuple[ExactEventEvidence | None, list[str]]:
    from gem.results.models import VisionModifierSemantic

    if smoke.team not in (2, 3):
        return (None, ["direct_reveal_opposing_team_unavailable"])
    opponent = 3 if smoke.team == 2 else 2
    players_by_id = {player.player_id: player for player in match.players}
    name_counts: dict[str, int] = {}
    for roster_player in match.players:
        if roster_player.hero_name:
            name_counts[roster_player.hero_name] = name_counts.get(roster_player.hero_name, 0) + 1
    targets: dict[str, int] = {}
    gaps: list[str] = []
    for participant in smoke.participants:
        resolved_player = (
            players_by_id.get(participant.player_id)
            if isinstance(participant.player_id, int)
            else None
        )
        if resolved_player is None or not resolved_player.hero_name:
            continue
        if name_counts.get(resolved_player.hero_name) != 1:
            gaps.append(f"direct_reveal_target_identity_ambiguous:{resolved_player.hero_name}")
            continue
        targets[resolved_player.hero_name] = resolved_player.player_id

    candidates: list[tuple[int, VisionModifierEvent, int]] = []
    for index, event in enumerate(match.vision_modifiers):
        if event.semantic is not VisionModifierSemantic.DIRECT_TARGET_REVEAL:
            continue
        if not smoke.tick <= event.tick <= fight.end_tick:
            continue
        target_player_id = targets.get(event.target_name)
        if target_player_id is None or not event.target_is_hero or event.target_is_illusion:
            continue
        if event.caster_team not in (2, 3):
            gaps.append(f"direct_reveal_caster_team_unavailable:{index}")
            continue
        if event.caster_team != opponent:
            continue
        target_player = players_by_id[target_player_id]
        if event.target_team in (2, 3) and event.target_team != target_player.team:
            gaps.append(f"direct_reveal_target_team_conflict:{index}")
            continue
        candidates.append((index, event, target_player_id))

    if not candidates:
        return (None, gaps)
    index, event, target_player_id = min(
        candidates,
        key=lambda item: (item[1].tick, item[0]),
    )
    game_time = _optional_int(event, "add_game_time_s", "game_time_s")
    return (
        _exact_event(
            ExactEventKind.DIRECT_REVEAL,
            event.tick,
            game_time,
            smoke.tick,
            activation_time,
            provenance="vision_modifiers",
            source_index=index,
            player_id=target_player_id,
            hero_name=event.target_name,
            source_name=event.modifier_name,
            target_name=event.target_name,
        ),
        gaps,
    )


def _first_member_action(
    match: ParsedMatch,
    smoke: SmokeEvent,
    fight: Teamfight,
    activation_time: int | None,
) -> ExactEventEvidence | None:
    players = {player.player_id: player for player in match.players}
    member_names: set[str] = set()
    for participant in smoke.participants:
        if not isinstance(participant.player_id, int):
            continue
        player = players.get(participant.player_id)
        if player is not None and player.hero_name:
            member_names.add(player.hero_name)
    start_tick = max(smoke.tick, fight.start_tick)
    candidates: list[tuple[int, CombatLogEntry, str]] = []
    for index, entry in enumerate(match.combat_log):
        if not start_tick <= entry.tick <= fight.end_tick:
            continue
        if entry.log_type not in ("ABILITY", "ITEM", "DAMAGE"):
            continue
        if entry.log_type == "DAMAGE" and not entry.target_is_hero:
            continue
        if entry.inflictor_name == _SMOKE_ITEM or entry.value_name == _SMOKE_ITEM:
            continue
        source_name = entry.damage_source_name or entry.attacker_name
        if source_name not in member_names:
            continue
        candidates.append((index, entry, source_name))
    if not candidates:
        return None
    index, entry, source_name = min(candidates, key=lambda item: (item[1].tick, item[0]))
    player_id = next(
        (player.player_id for player in players.values() if player.hero_name == source_name),
        None,
    )
    return _exact_event(
        ExactEventKind.MEMBER_ACTION,
        entry.tick,
        entry.game_time_s,
        smoke.tick,
        activation_time,
        provenance="combat_log",
        source_index=index,
        player_id=player_id,
        hero_name=source_name,
        source_name=entry.inflictor_name or source_name,
        target_name=entry.target_name,
    )


def _valid_first_death_tick(fight: Teamfight) -> int | None:
    tick = fight.first_death_tick
    if tick > 0 and fight.start_tick <= tick <= fight.end_tick:
        return tick
    return None


def _first_death(
    match: ParsedMatch,
    fight: Teamfight,
    fight_index: int,
    activation_tick: int,
    activation_time: int | None,
) -> tuple[ExactEventEvidence | None, list[str]]:
    tick = _valid_first_death_tick(fight)
    if tick is None:
        return (None, [])

    candidates = [
        entry
        for entry in match.combat_log
        if entry.tick == tick and entry.log_type == "DEATH" and not entry.will_reincarnate
    ]
    source = candidates[0] if len(candidates) == 1 else None
    gaps: list[str] = []
    if len(candidates) > 1:
        players_by_id = {player.player_id: player for player in match.players}
        died_names: set[str] = set()
        for stats in fight.players:
            player_id = getattr(stats, "player_id", None)
            if getattr(stats, "deaths", 0) <= 0 or not isinstance(player_id, int):
                continue
            player = players_by_id.get(player_id)
            if player is not None and player.hero_name:
                died_names.add(player.hero_name)
        matching = [entry for entry in candidates if entry.target_name in died_names]
        if len(matching) == 1:
            source = matching[0]
        else:
            gaps.append("first_death_source_ambiguous")
    elif not candidates:
        gaps.append("first_death_source_unavailable")

    return (
        _exact_event(
            ExactEventKind.FIRST_DEATH,
            tick,
            source.game_time_s if source is not None else None,
            activation_tick,
            activation_time,
            provenance="teamfights",
            source_index=fight_index,
            hero_name=source.target_name if source is not None else "",
            source_name=(source.damage_source_name or source.attacker_name) if source else "",
            target_name=source.target_name if source is not None else "",
        ),
        gaps,
    )


def _exact_event(
    kind: ExactEventKind,
    tick: int,
    game_time_s: int | None,
    activation_tick: int,
    activation_game_time_s: int | None,
    *,
    provenance: str,
    source_index: int | None = None,
    player_id: int | None = None,
    hero_name: str = "",
    source_name: str = "",
    target_name: str = "",
) -> ExactEventEvidence:
    pause_delta = (
        game_time_s - activation_game_time_s
        if game_time_s is not None and activation_game_time_s is not None
        else None
    )
    return ExactEventEvidence(
        kind=kind,
        tick=tick,
        game_time_s=game_time_s,
        tick_delta=tick - activation_tick,
        game_time_delta_s=pause_delta,
        provenance=provenance,
        source_index=source_index,
        player_id=player_id,
        hero_name=hero_name,
        source_name=source_name,
        target_name=target_name,
    )


def _follow_up_window(
    match: ParsedMatch,
    smoke_index: int,
    fight_end_tick: int,
    follow_up_ticks: int,
) -> FollowUpWindow:
    smoke = match.smoke_events[smoke_index]
    bounds = [(fight_end_tick + follow_up_ticks, FollowUpBoundary.CONFIGURED_LIMIT)]
    match_end_tick = infer_match_end_tick(match)
    if match_end_tick > 0:
        bounds.append((match_end_tick, FollowUpBoundary.GAME_END))
    next_smoke_ticks = [
        other.tick
        for index, other in enumerate(match.smoke_events)
        if index != smoke_index and other.team == smoke.team and other.tick > smoke.tick
    ]
    if next_smoke_ticks:
        bounds.append((min(next_smoke_ticks), FollowUpBoundary.NEXT_SAME_TEAM_SMOKE))
    limiting_tick = min(tick for tick, _ in bounds)
    end_tick = max(fight_end_tick, limiting_tick)
    reasons = tuple(reason for tick, reason in bounds if tick == limiting_tick)
    return FollowUpWindow(fight_end_tick, end_tick, reasons)


def _allocate_follow_ups(
    match: ParsedMatch,
    insights: list[SmokeFightInsight],
) -> list[SmokeFightInsight]:
    linked = [
        (index, insight)
        for index, insight in enumerate(insights)
        if insight.status is SmokeFightStatus.LINKED and insight.follow_up_window is not None
    ]
    if not linked:
        return insights

    allocated: dict[int, list[FollowUpEvent]] = {index: [] for index, _ in linked}
    for raw in _raw_follow_ups(match):
        tick = getattr(raw.event, "tick", None)
        if not isinstance(tick, int):
            continue
        eligible = [
            (index, insight, insight.follow_up_window.start_tick)
            for index, insight in linked
            if insight.follow_up_window is not None
            and insight.follow_up_window.start_tick <= tick < insight.follow_up_window.end_tick
        ]
        if not eligible:
            continue
        insight_index, insight, _ = min(
            eligible,
            key=lambda item: (-item[2], item[0]),
        )
        allocated[insight_index].append(_follow_up_event(match, insight, raw))

    result = list(insights)
    kind_order = {kind: index for index, kind in enumerate(FollowUpKind)}
    for index, events in allocated.items():
        events.sort(key=lambda event: (event.tick, kind_order[event.kind], event.source_index))
        result[index] = replace(result[index], follow_ups=tuple(events))
    return result


def _raw_follow_ups(match: ParsedMatch) -> list[_RawFollowUp]:
    result = [
        _RawFollowUp(FollowUpKind.TOWER, index, event) for index, event in enumerate(match.towers)
    ]
    result.extend(
        _RawFollowUp(FollowUpKind.BARRACKS, index, event)
        for index, event in enumerate(match.barracks)
    )
    result.extend(
        _RawFollowUp(FollowUpKind.ROSHAN, index, event) for index, event in enumerate(match.roshans)
    )
    result.extend(
        _RawFollowUp(FollowUpKind.TORMENTOR, index, event)
        for index, event in enumerate(match.tormentors)
    )
    result.extend(
        _RawFollowUp(FollowUpKind.OBSERVER_WARD, index, event)
        for index, event in enumerate(match.wards)
        if event.ward_type == "observer"
    )
    return result


def _follow_up_event(
    match: ParsedMatch,
    insight: SmokeFightInsight,
    raw: _RawFollowUp,
) -> FollowUpEvent:
    actor_player_id, actor_name, actor_team = _actor(match, raw)
    game_time = _optional_int(raw.event, "game_time_s")
    tick = _optional_int(raw.event, "tick")
    assert tick is not None
    relation = _relation(insight.smoke_team, actor_team)
    subject_name = _subject_name(raw)
    return FollowUpEvent(
        kind=raw.kind,
        source_index=raw.source_index,
        tick=tick,
        game_time_s=game_time,
        tick_delta=tick - insight.activation.tick,
        game_time_delta_s=(
            game_time - insight.activation.game_time_s
            if game_time is not None and insight.activation.game_time_s is not None
            else None
        ),
        actor_name=actor_name,
        actor_player_id=actor_player_id,
        actor_team=actor_team,
        relation=relation,
        subject_name=subject_name,
    )


def _actor(
    match: ParsedMatch,
    raw: _RawFollowUp,
) -> tuple[int | None, str, int | None]:
    players_by_id = {player.player_id: player for player in match.players}
    if raw.kind is FollowUpKind.TORMENTOR:
        player_id = getattr(raw.event, "killer_player_id", -1)
        if player_id in players_by_id:
            player = players_by_id[player_id]
            return (player_id, getattr(raw.event, "killer", "") or player.hero_name, player.team)
    elif raw.kind is FollowUpKind.OBSERVER_WARD:
        player_id = getattr(raw.event, "player_id", -1)
        if player_id in players_by_id:
            player = players_by_id[player_id]
            return (player_id, getattr(raw.event, "placer", "") or player.hero_name, player.team)

    names = []
    if raw.kind is FollowUpKind.OBSERVER_WARD:
        names.append(getattr(raw.event, "placer", ""))
    else:
        names.extend(
            (
                getattr(raw.event, "killer_source", ""),
                getattr(raw.event, "killer", ""),
            )
        )
    for name in names:
        if not name:
            continue
        candidates = [player for player in match.players if player.hero_name == name]
        if len(candidates) == 1:
            player = candidates[0]
            return (player.player_id, name, player.team)
    actor_team = None
    if raw.kind is FollowUpKind.OBSERVER_WARD:
        event_team = getattr(raw.event, "team", None)
        if isinstance(event_team, int) and event_team in (2, 3):
            actor_team = event_team
    return (None, next((name for name in names if name), ""), actor_team)


def _subject_name(raw: _RawFollowUp) -> str:
    if raw.kind is FollowUpKind.TOWER:
        return getattr(raw.event, "tower_name", "")
    if raw.kind is FollowUpKind.BARRACKS:
        return getattr(raw.event, "barracks_name", "")
    if raw.kind is FollowUpKind.ROSHAN:
        return "roshan"
    if raw.kind is FollowUpKind.TORMENTOR:
        return "tormentor"
    return "observer_ward"


def _relation(smoke_team: int, actor_team: int | None) -> TeamRelation:
    if smoke_team not in (2, 3) or actor_team not in (2, 3):
        return TeamRelation.UNKNOWN
    if smoke_team == actor_team:
        return TeamRelation.SMOKE_TEAM
    return TeamRelation.OPPONENT


def _optional_int(source: object, *names: str) -> int | None:
    for name in names:
        value = getattr(source, name, None)
        if isinstance(value, int):
            return value
    return None


def _deduplicate(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))
