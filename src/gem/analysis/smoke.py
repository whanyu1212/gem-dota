"""Evidence-first post-parse Smoke of Deceit lifecycle analysis.

Reference: ``CMsgDOTACombatLogEntry`` in
``refs/manta/dota/dota_shared_enums.proto`` and Clarity's S1/S2 combat-log
adapters in ``refs/clarity``.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING

from gem.combat.log import CombatLogEntry

if TYPE_CHECKING:
    from gem.extractors.teamfights import Teamfight
    from gem.results.models import (
        ParsedMatch,
        ParsedPlayer,
        SmokeEvent,
        SmokeParticipant,
        VisibilityState,
    )

_TICKS_PER_SECOND = 30
_DURATION_TOLERANCE_S = 0.25
_TEAMFIGHT_WINDOW_TICKS = 60 * _TICKS_PER_SECOND
_ACTION_TYPES = frozenset({"ABILITY", "ITEM", "DAMAGE"})


class SmokeLifecycleStatus(str, Enum):
    """Observed lifecycle classification for one smoke participant.

    Attributes:
        EXPIRED: Removal was observed at the intended duration, within a
            quarter-second tolerance.
        EARLY: Removal was observed before the intended expiry tolerance.
        UNOBSERVED: Removal or intended-duration evidence was unavailable.
    """

    __str__ = str.__str__

    EXPIRED = "expired"
    EARLY = "early"
    UNOBSERVED = "unobserved"


class SmokeGroupStatus(str, Enum):
    """Evidence-based aggregate state for one smoke activation.

    Attributes:
        NO_MEMBERS_OBSERVED: The item use had no observed hero modifier adds.
        EARLY_REMOVAL: At least one participant had an observed early removal.
        EXPIRED: Every observed participant reached intended expiry.
        INCOMPLETE: Members exist, but at least one lifecycle is unobserved and
            no member has an observed early removal.
    """

    __str__ = str.__str__

    NO_MEMBERS_OBSERVED = "no_members_observed"
    EARLY_REMOVAL = "early_removal"
    EXPIRED = "expired"
    INCOMPLETE = "incomplete"


@dataclass
class SmokeMemberAnalysis:
    """Evidence summary for one hero in a smoke activation.

    Attributes:
        hero_name: NPC name of the smoked hero.
        player_id: Logical player slot, or ``None`` when unresolved.
        applied_tick: Exact modifier-add combat-log tick.
        removed_tick: Exact modifier-remove combat-log tick, or ``None``.
        lifecycle_status: Duration-based lifecycle classification.
        visibility_at_apply: Opposing team's authoritative visibility state at
            the apply tick.
        visibility_at_remove: Opposing team's authoritative visibility state at
            the remove tick, or ``UNKNOWN`` if removal was not observed.
        first_visible_tick: First authoritative transition to ``VISIBLE`` during
            the observed/expected lifecycle, or ``None`` if none was observed.
        nearest_enemy_hero: Nearest opposing hero at removal from sampled
            positions, or ``None`` when the fact cannot be derived.
        nearest_enemy_player_id: Player slot for ``nearest_enemy_hero``.
        nearest_enemy_distance: World-unit distance to that hero at removal.
        same_tick_actions: Ability, item, or damage entries initiated by this
            hero at the exact removal tick.
        same_tick_deaths: Death entries for this hero at the exact removal tick.
        evidence_gaps: Machine-readable reasons requested evidence was
            unavailable. These describe missing facts, not causes of removal.
    """

    hero_name: str
    player_id: int | None
    applied_tick: int
    removed_tick: int | None
    lifecycle_status: SmokeLifecycleStatus
    visibility_at_apply: VisibilityState
    visibility_at_remove: VisibilityState
    first_visible_tick: int | None = None
    nearest_enemy_hero: str | None = None
    nearest_enemy_player_id: int | None = None
    nearest_enemy_distance: float | None = None
    same_tick_actions: list[CombatLogEntry] = field(default_factory=list)
    same_tick_deaths: list[CombatLogEntry] = field(default_factory=list)
    evidence_gaps: list[str] = field(default_factory=list)


@dataclass
class SmokeAnalysis:
    """Evidence summary for one Smoke of Deceit item use.

    Attributes:
        activation_tick: Exact item-use combat-log tick.
        activator: NPC hero name of the item user.
        team: Activator team (2=Radiant, 3=Dire), or 0 if unresolved.
        status: Aggregate participant lifecycle status.
        activation_x: Activator position sampled at the item-use tick.
        activation_y: Activator position sampled at the item-use tick.
        member_centroid_x: Legacy centroid of member positions at their
            individual modifier-add ticks.
        member_centroid_y: Legacy member-centroid y coordinate.
        members: Per-participant lifecycle and factual evidence.
        first_teamfight: First detected teamfight whose first death occurs from
            activation through 60 seconds afterward, or ``None``.
        evidence_gaps: Machine-readable reasons group-level evidence was
            unavailable. These do not assign a cause or success score.
    """

    activation_tick: int
    activator: str
    team: int
    status: SmokeGroupStatus
    activation_x: float | None
    activation_y: float | None
    member_centroid_x: float | None
    member_centroid_y: float | None
    members: list[SmokeMemberAnalysis] = field(default_factory=list)
    first_teamfight: Teamfight | None = None
    evidence_gaps: list[str] = field(default_factory=list)


def build_smoke_analysis(match: ParsedMatch) -> list[SmokeAnalysis]:
    """Build factual lifecycle summaries for every smoke item use.

    The helper preserves combat-log ticks exactly. It uses modifier duration
    metadata only to distinguish observed expiry from observed early removal;
    visibility, sampled proximity, same-tick actions/deaths, and later
    teamfights remain separate factual signals and are never treated as causes.

    Args:
        match: Parsed match containing smoke events and supporting timelines.

    Returns:
        One :class:`SmokeAnalysis` per smoke event, in source order.
    """
    players_by_id = {player.player_id: player for player in match.players}
    analyses: list[SmokeAnalysis] = []

    for smoke in match.smoke_events:
        members = [
            _build_member_analysis(match, smoke, participant, players_by_id)
            for participant in smoke.participants
        ]
        status = _group_status(members)
        evidence_gaps: list[str] = []
        if smoke.team not in (2, 3):
            evidence_gaps.append("activation_team_unavailable")
        if smoke.activation_x is None or smoke.activation_y is None:
            evidence_gaps.append("activation_position_unavailable")

        analyses.append(
            SmokeAnalysis(
                activation_tick=smoke.tick,
                activator=smoke.activator,
                team=smoke.team,
                status=status,
                activation_x=smoke.activation_x,
                activation_y=smoke.activation_y,
                member_centroid_x=smoke.x,
                member_centroid_y=smoke.y,
                members=members,
                first_teamfight=_first_teamfight(match, smoke.tick),
                evidence_gaps=evidence_gaps,
            )
        )

    return analyses


def _build_member_analysis(
    match: ParsedMatch,
    smoke: SmokeEvent,
    participant: SmokeParticipant,
    players_by_id: dict[int, ParsedPlayer],
) -> SmokeMemberAnalysis:
    from gem.results.models import VisibilityState

    lifecycle_status = _lifecycle_status(participant)
    member_player = (
        players_by_id.get(participant.player_id) if participant.player_id is not None else None
    )
    member_team = member_player.team if member_player is not None else smoke.team
    opposing_team = 3 if member_team == 2 else 2 if member_team == 3 else None

    visibility_at_apply = _visibility_at(
        match,
        participant.player_id,
        opposing_team,
        participant.applied_tick,
    )
    visibility_at_remove = (
        _visibility_at(
            match,
            participant.player_id,
            opposing_team,
            participant.removed_tick,
        )
        if participant.removed_tick is not None
        else VisibilityState.UNKNOWN
    )
    first_visible_tick = _first_visible_tick(match, participant, opposing_team)
    nearest_hero, nearest_player_id, nearest_distance = _nearest_enemy_at_removal(
        match,
        participant,
        member_team,
    )
    same_tick_actions, same_tick_deaths = _same_tick_evidence(match, participant)

    evidence_gaps: list[str] = []
    if participant.player_id is None:
        evidence_gaps.append("player_id_unavailable")
    if opposing_team is None:
        evidence_gaps.append("opposing_team_unavailable")
    if participant.removed_tick is None:
        evidence_gaps.append("removal_not_observed")
    if participant.modifier_duration_s is None:
        evidence_gaps.append("modifier_duration_unavailable")
    if participant.removed_tick is not None and (
        participant.removed_x is None or participant.removed_y is None
    ):
        evidence_gaps.append("removal_position_unavailable")

    return SmokeMemberAnalysis(
        hero_name=participant.hero_name,
        player_id=participant.player_id,
        applied_tick=participant.applied_tick,
        removed_tick=participant.removed_tick,
        lifecycle_status=lifecycle_status,
        visibility_at_apply=visibility_at_apply,
        visibility_at_remove=visibility_at_remove,
        first_visible_tick=first_visible_tick,
        nearest_enemy_hero=nearest_hero,
        nearest_enemy_player_id=nearest_player_id,
        nearest_enemy_distance=nearest_distance,
        same_tick_actions=same_tick_actions,
        same_tick_deaths=same_tick_deaths,
        evidence_gaps=evidence_gaps,
    )


def _lifecycle_status(participant: SmokeParticipant) -> SmokeLifecycleStatus:
    if participant.removed_tick is None or participant.modifier_duration_s is None:
        return SmokeLifecycleStatus.UNOBSERVED

    elapsed_s = participant.modifier_elapsed_duration_s
    if elapsed_s is None:
        elapsed_s = (participant.removed_tick - participant.applied_tick) / _TICKS_PER_SECOND
    if elapsed_s + _DURATION_TOLERANCE_S >= participant.modifier_duration_s:
        return SmokeLifecycleStatus.EXPIRED
    return SmokeLifecycleStatus.EARLY


def _group_status(members: list[SmokeMemberAnalysis]) -> SmokeGroupStatus:
    if not members:
        return SmokeGroupStatus.NO_MEMBERS_OBSERVED
    if any(member.lifecycle_status is SmokeLifecycleStatus.EARLY for member in members):
        return SmokeGroupStatus.EARLY_REMOVAL
    if all(member.lifecycle_status is SmokeLifecycleStatus.EXPIRED for member in members):
        return SmokeGroupStatus.EXPIRED
    return SmokeGroupStatus.INCOMPLETE


def _visibility_at(
    match: ParsedMatch,
    player_id: int | None,
    opposing_team: int | None,
    tick: int,
) -> VisibilityState:
    from gem.analysis.vision import hero_visibility_at
    from gem.results.models import VisibilityState

    if player_id is None or opposing_team is None:
        return VisibilityState.UNKNOWN
    return hero_visibility_at(
        match,
        player_id=player_id,
        observing_team=opposing_team,
        tick=tick,
    )


def _first_visible_tick(
    match: ParsedMatch,
    participant: SmokeParticipant,
    opposing_team: int | None,
) -> int | None:
    from gem.analysis.vision import hero_visibility_at
    from gem.results.models import VisibilityState

    if participant.player_id is None or opposing_team is None:
        return None

    end_tick = participant.removed_tick
    if end_tick is None and participant.modifier_duration_s is not None:
        end_tick = participant.applied_tick + round(
            participant.modifier_duration_s * _TICKS_PER_SECOND
        )
    if end_tick is None:
        end_tick = match.game_end_tick
    if end_tick < participant.applied_tick:
        return None

    for event in sorted(match.hero_visibility_events, key=lambda candidate: candidate.tick):
        if event.player_id != participant.player_id:
            continue
        if not participant.applied_tick <= event.tick <= end_tick:
            continue
        state = event.radiant_state if opposing_team == 2 else event.dire_state
        if state is not VisibilityState.VISIBLE:
            continue
        previous = hero_visibility_at(
            match,
            player_id=participant.player_id,
            observing_team=opposing_team,
            tick=event.tick - 1,
        )
        if previous is not VisibilityState.VISIBLE:
            return event.tick
    return None


def _nearest_enemy_at_removal(
    match: ParsedMatch,
    participant: SmokeParticipant,
    member_team: int,
) -> tuple[str | None, int | None, float | None]:
    from gem.analysis.spatial import position_at_tick

    if participant.removed_tick is None or member_team not in (2, 3):
        return (None, None, None)

    member_position: tuple[float, float] | None = None
    if participant.removed_x is not None and participant.removed_y is not None:
        member_position = (participant.removed_x, participant.removed_y)
    elif participant.player_id is not None:
        member_player = next(
            (player for player in match.players if player.player_id == participant.player_id),
            None,
        )
        if member_player is not None:
            member_position = position_at_tick(member_player, participant.removed_tick)
    if member_position is None:
        return (None, None, None)

    nearest: tuple[float, ParsedPlayer] | None = None
    for player in match.players:
        if player.team not in (2, 3) or player.team == member_team:
            continue
        position = position_at_tick(player, participant.removed_tick)
        if position is None:
            continue
        distance = math.dist(member_position, position)
        if nearest is None or distance < nearest[0]:
            nearest = (distance, player)

    if nearest is None:
        return (None, None, None)
    distance, player = nearest
    return (player.hero_name, player.player_id, distance)


def _same_tick_evidence(
    match: ParsedMatch,
    participant: SmokeParticipant,
) -> tuple[list[CombatLogEntry], list[CombatLogEntry]]:
    if participant.removed_tick is None:
        return ([], [])

    actions: list[CombatLogEntry] = []
    deaths: list[CombatLogEntry] = []
    for entry in match.combat_log:
        if entry.tick != participant.removed_tick:
            continue
        if entry.log_type == "DEATH" and entry.target_name == participant.hero_name:
            deaths.append(entry)
        elif entry.log_type in _ACTION_TYPES and (
            entry.attacker_name == participant.hero_name
            or entry.damage_source_name == participant.hero_name
        ):
            actions.append(entry)
    return (actions, deaths)


def _first_teamfight(match: ParsedMatch, activation_tick: int) -> Teamfight | None:
    eligible = [
        fight
        for fight in match.teamfights
        if activation_tick <= fight.first_death_tick <= activation_tick + _TEAMFIGHT_WINDOW_TICKS
    ]
    return min(eligible, key=lambda fight: fight.first_death_tick, default=None)
