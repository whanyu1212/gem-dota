"""Evidence-aware visibility helpers for parsed matches.

Ward type and lifetime semantics follow
``odota/parser src/main/java/opendota/processors/warding/Wards.java``. Arbitrary
point geometry is gem-specific and deliberately separate from authoritative
canonical-hero visibility.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Literal

from gem.analysis._shared import infer_match_end_tick
from gem.analysis.spatial import position_sample_at_tick
from gem.results.models import (
    VisibilityState,
    VisionModifierCloseEvidence,
    VisionModifierLifecycleStatus,
    VisionModifierPairingStatus,
    VisionModifierSemantic,
)

if TYPE_CHECKING:
    from gem.results.models import ParsedMatch

# Standard Dota 2 hero vision radii (world units).
# Heroes with special vision (Slardar ulti, Aghs upgrades, etc.) are edge cases
# we cannot track without per-tick entity sampling — these defaults cover ~95%.
_DAY_VISION: int = 1800
_NIGHT_VISION: int = 800

# Observer ward vision radius (constant, no items change it)
_WARD_VISION: int = 1600

# Day/night cycle constants (ticks at 30 ticks/sec).
# Dota's cycle is 10 minutes: day from 0:00, night from 5:00, repeating.
# Reference: https://liquipedia.net/dota2/Time_of_Day
_DAY_NIGHT_CYCLE_TICKS: int = 10 * 60 * 30  # 18000 ticks (10:00)
_NIGHT_START_TICKS: int = 5 * 60 * 30  # 9000 ticks (night starts at 5:00)


@dataclass
class VisionSource:
    """One modeled geometry source covering a map point at a given tick.

    Attributes:
        kind: ``"hero"`` if the source is an allied hero or ``"ward"`` if an
            observer ward. The historical ``"modifier"`` literal remains in
            the type for constructor compatibility, but hardened point queries
            report direct-target reveals separately.
        name: NPC hero name (e.g. ``"npc_dota_hero_axe"``) for heroes,
            or ``"observer_ward"`` for wards.
        distance: World-unit distance from the source to the queried point.
        vision_radius: Vision radius used for this source at the queried tick
            (day/night-adjusted for heroes; constant for wards).
        x: Source world x coordinate when available.
        y: Source world y coordinate when available.
        position_tick: Hero sample tick or ward placement tick.
        position_age_ticks: Hero sample age; ``None`` for static ward positions.
        player_id: Canonical hero slot or ward placer slot when known.
        position_provenance: Sampled-hero or entity-derived ward provenance.
    """

    kind: Literal["hero", "ward", "modifier"]
    name: str
    distance: float
    vision_radius: int
    x: float | None = None
    y: float | None = None
    position_tick: int | None = None
    position_age_ticks: int | None = None
    player_id: int | None = None
    position_provenance: Literal["sampled_player_position", "ward_placement"] | None = None


class PointVisionStatus(str, Enum):
    """Modeled support state for an arbitrary map point."""

    __str__ = str.__str__

    SUPPORTED = "supported"
    UNSUPPORTED = "unsupported"
    INCOMPLETE = "incomplete"


@dataclass(frozen=True, slots=True)
class PointVisionSource:
    """One bounded geometry source supporting point coverage.

    Attributes:
        kind: ``"hero"`` or ``"observer_ward"``.
        name: Canonical hero name or ``"observer_ward"``.
        distance: World-unit distance from the source to the query point.
        vision_radius: Circular vision radius used for the assessment.
        x: Source world x coordinate.
        y: Source world y coordinate.
        position_provenance: How the coordinate was obtained.
        position_tick: Tick of the position sample or ward placement.
        position_age_ticks: Absolute query-to-position tick difference.
        player_id: Logical player slot for hero and ward attribution when known.
    """

    kind: Literal["hero", "observer_ward"]
    name: str
    distance: float
    vision_radius: int
    x: float
    y: float
    position_provenance: Literal["sampled_player_position", "ward_placement"]
    position_tick: int | None = None
    position_age_ticks: int | None = None
    player_id: int | None = None

    @property
    def identity(self) -> str:
        """Return the source name as its stable identity."""
        return self.name

    @property
    def radius(self) -> int:
        """Return the modeled circular vision radius."""
        return self.vision_radius


@dataclass(frozen=True, slots=True)
class PointVisionGap:
    """One material omission or ambiguity in a point-vision assessment.

    Attributes:
        code: Stable machine-readable gap code.
        subject: Hero, ward, modifier, or roster identity affected by the gap.
    """

    code: str
    subject: str


@dataclass(frozen=True, slots=True)
class DirectTargetRevealEvidence:
    """Bounded direct-reveal evidence for the requested canonical hero.

    Direct target reveals are returned separately because they establish
    evidence about that target, not circular coverage of an arbitrary point.

    Attributes:
        modifier_name: Internal reveal modifier name.
        target_name: Canonical NPC hero name receiving the modifier.
        caster_name: NPC name recorded as applying the modifier.
        caster_team: Team receiving the direct reveal.
        start_tick: Exact application tick.
        end_tick: Exact observed interval end tick.
        target_player_id: Canonical logical player slot of the target.
    """

    modifier_name: str
    target_name: str
    caster_name: str
    caster_team: int
    start_tick: int
    end_tick: int
    target_player_id: int

    @property
    def tick(self) -> int:
        """Return the interval start using modifier-event terminology."""
        return self.start_tick


@dataclass(frozen=True, slots=True)
class PointVisionAssessment:
    """Evidence-aware modeled coverage assessment for one arbitrary point.

    ``status`` describes only modeled hero/observer geometry. Authoritative
    visible/hidden/unknown state applies only when ``target_player_id`` resolves
    to a canonical player hero and is therefore exposed separately.

    Attributes:
        team: Team whose modeled vision is being assessed.
        tick: Replay tick queried.
        x: Queried world x coordinate.
        y: Queried world y coordinate.
        status: Supported, unsupported, or incomplete modeled state.
        sources: Bounded geometry sources covering the point.
        gaps: Material missing, stale, or ambiguous evidence.
        direct_target_reveals: Qualifying target-specific reveal evidence.
        target_player_id: Requested canonical target slot, if any.
        authoritative_applicable: Whether the target resolved to a player hero.
        authoritative_visibility: Replay-observed hero visibility state.
        max_position_age_ticks: Freshness bound applied to hero samples.
    """

    team: int
    tick: int
    x: float
    y: float
    status: PointVisionStatus
    sources: list[PointVisionSource]
    gaps: list[PointVisionGap]
    direct_target_reveals: list[DirectTargetRevealEvidence]
    target_player_id: int | None
    authoritative_applicable: bool
    authoritative_visibility: VisibilityState
    max_position_age_ticks: int


def is_daytime(game_start_tick: int | None, tick: int) -> bool:
    """Return True if it is daytime at the given absolute tick.

    Dota 2 day/night cycle: day starts at game time 0:00, night begins at 5:00,
    and the cycle repeats every 10 minutes (5 min day + 5 min night). Tick 0 is
    daytime; the first night begins at tick 9000 (5:00).
    Reference: https://liquipedia.net/dota2/Time_of_Day

    Args:
        game_start_tick: Absolute tick when the game clock started, or ``None``.
        tick: Absolute tick to query.

    Returns:
        ``True`` if daytime, ``False`` if nighttime.
    """
    start = game_start_tick or 0
    game_ticks = max(tick - start, 0)
    phase = game_ticks % _DAY_NIGHT_CYCLE_TICKS
    return phase < _NIGHT_START_TICKS


# Backwards-compatible alias for the pre-rename name. ``is_daytime`` is the
# preferred public name; ``_is_daytime`` was exported from ``gem.analysis`` on
# the development branch, so keep the alias to avoid breaking that import.
_is_daytime = is_daytime


def hero_visibility_at(
    match: ParsedMatch,
    *,
    player_id: int,
    observing_team: int,
    tick: int,
) -> VisibilityState:
    """Return authoritative hero-entity visibility at or before ``tick``.

    The last event at the latest eligible tick wins. A query before the first
    observation, or after an identity's terminal event, returns ``UNKNOWN``.

    Args:
        match: Parsed match containing hero visibility events.
        player_id: Logical player slot from 0 through 9.
        observing_team: Radiant (2) or Dire (3).
        tick: Replay tick to query.

    Returns:
        The latest known :class:`VisibilityState`, or ``UNKNOWN`` when no
        eligible observation exists or the identity has terminated.

    Raises:
        ValueError: If ``observing_team`` is not 2 or 3.
    """
    if observing_team not in (2, 3):
        raise ValueError("observing_team must be 2 (Radiant) or 3 (Dire)")

    latest = None
    for event in match.hero_visibility_events:
        if (
            event.player_id == player_id
            and event.tick <= tick
            and (latest is None or event.tick >= latest.tick)
        ):
            latest = event

    if latest is None:
        return VisibilityState.UNKNOWN
    return latest.radiant_state if observing_team == 2 else latest.dire_state


def entity_visibility_at(
    match: ParsedMatch,
    *,
    entity_index: int,
    entity_serial: int,
    observing_team: int,
    tick: int,
) -> VisibilityState:
    """Return authoritative NPC-entity visibility at or before ``tick``.

    Identity includes both the entity-table index and serial, so reuse of a
    slot cannot leak visibility across entities. The last eligible event wins;
    an inactive terminal event returns ``UNKNOWN``.

    Args:
        match: Parsed match containing entity visibility events.
        entity_index: Entity-table slot index.
        entity_serial: Entity serial for the queried identity.
        observing_team: Radiant (2) or Dire (3).
        tick: Replay tick to query.

    Returns:
        The latest known :class:`VisibilityState`, or ``UNKNOWN`` when no
        eligible active observation exists.

    Raises:
        ValueError: If ``observing_team`` is not 2 or 3.
    """
    if observing_team not in (2, 3):
        raise ValueError("observing_team must be 2 (Radiant) or 3 (Dire)")

    latest = None
    for event in match.entity_visibility_events:
        if (
            event.entity_index == entity_index
            and event.entity_serial == entity_serial
            and event.tick <= tick
            and (latest is None or event.tick >= latest.tick)
        ):
            latest = event

    if latest is None or not latest.active:
        return VisibilityState.UNKNOWN
    return latest.radiant_state if observing_team == 2 else latest.dire_state


def assess_point_vision(
    match: ParsedMatch,
    team: int,
    tick: int,
    x: float,
    y: float,
    *,
    target_player_id: int | None = None,
    max_position_age_ticks: int = 150,
) -> PointVisionAssessment:
    """Assess bounded modeled evidence for team vision of one map point.

    Hero coordinates use the nearest sampled position only when its absolute
    age is at most ``max_position_age_ticks`` (five seconds at 30 ticks/sec by
    default). Observer wards use a half-open active interval
    ``[placement_tick, min(killed_tick, expires_tick))``. Open ward lifetimes
    are usable only through a known observed match horizon.

    Direct target reveals never become point-radius sources. When a canonical
    ``target_player_id`` is supplied, qualifying bounded reveals and the
    authoritative hero visibility state are returned in separate fields.

    ``UNSUPPORTED`` means only that no currently modeled geometry source covers
    the point. It is not proof that the point was hidden in-game. Terrain,
    trees, blockers, summons, buildings, and many temporary mechanics are not
    modeled.

    Args:
        match: A parsed replay.
        team: Team number to assess (2=Radiant, 3=Dire).
        tick: Game tick to query.
        x: Queried world x coordinate.
        y: Queried world y coordinate.
        target_player_id: Optional canonical player slot at the queried subject.
        max_position_age_ticks: Maximum allowed absolute hero sample age.

    Returns:
        A structured assessment containing modeled sources, evidence gaps,
        target-specific reveals, and separately scoped authoritative evidence.

    Raises:
        ValueError: If ``team`` is not 2 or 3, or the age bound is negative.
    """
    if team not in (2, 3):
        raise ValueError("team must be 2 (Radiant) or 3 (Dire)")
    if max_position_age_ticks < 0:
        raise ValueError("max_position_age_ticks must be nonnegative")

    daytime = is_daytime(match.game_start_tick, tick)
    hero_radius = _DAY_VISION if daytime else _NIGHT_VISION

    sources: list[PointVisionSource] = []
    gaps: list[PointVisionGap] = []
    point_incomplete = False

    def add_gap(code: str, subject: str, *, point_evidence: bool = False) -> None:
        nonlocal point_incomplete
        gap = PointVisionGap(code=code, subject=subject)
        if gap not in gaps:
            gaps.append(gap)
        if point_evidence:
            point_incomplete = True

    # --- Hero vision ---
    allied_players = [player for player in match.players if player.team == team]
    if not allied_players:
        add_gap("allied_roster_empty", f"team:{team}", point_evidence=True)

    for player in allied_players:
        identity = player.hero_name or f"player:{player.player_id}"
        sample = position_sample_at_tick(player, tick)
        if sample is None:
            add_gap("allied_hero_position_missing", identity, point_evidence=True)
            continue
        if sample.age_ticks > max_position_age_ticks:
            add_gap("allied_hero_position_stale", identity, point_evidence=True)
            continue
        dist = math.dist((sample.x, sample.y), (x, y))
        if dist <= hero_radius:
            sources.append(
                PointVisionSource(
                    kind="hero",
                    name=identity,
                    distance=dist,
                    vision_radius=hero_radius,
                    x=sample.x,
                    y=sample.y,
                    position_provenance="sampled_player_position",
                    position_tick=sample.sample_tick,
                    position_age_ticks=sample.age_ticks,
                    player_id=player.player_id,
                )
            )

    # --- Observer ward vision ---
    for ward in match.wards:
        if ward.ward_type != "observer":
            continue
        if ward.tick > tick:
            continue

        bounded_ends = [end for end in (ward.killed_tick, ward.expires_tick) if end is not None]
        end_tick = min(bounded_ends) if bounded_ends else None
        subject = f"observer_ward:{ward.player_id}:{ward.tick}"
        if end_tick is not None and tick >= end_tick:
            continue

        if ward.team not in (2, 3):
            add_gap("observer_ward_team_unknown", subject, point_evidence=True)
            continue
        if ward.team != team:
            continue

        unusable_ward = False
        if end_tick is None:
            game_end_tick = getattr(match, "game_end_tick", None)
            known_horizon = (
                game_end_tick if isinstance(game_end_tick, int) and game_end_tick > 0 else None
            )
            if known_horizon is None or tick > known_horizon:
                add_gap("observer_ward_lifetime_unknown", subject, point_evidence=True)
                unusable_ward = True

        ward_x = ward.x
        ward_y = ward.y
        if ward_x is None or ward_y is None:
            add_gap("observer_ward_position_missing", subject, point_evidence=True)
            unusable_ward = True
        if unusable_ward:
            continue
        assert ward_x is not None and ward_y is not None

        dist = math.dist((ward_x, ward_y), (x, y))
        if dist <= _WARD_VISION:
            sources.append(
                PointVisionSource(
                    kind="observer_ward",
                    name="observer_ward",
                    distance=dist,
                    vision_radius=_WARD_VISION,
                    x=ward_x,
                    y=ward_y,
                    position_provenance="ward_placement",
                    position_tick=ward.tick,
                    position_age_ticks=None,
                    player_id=ward.player_id if ward.player_id >= 0 else None,
                )
            )

    authoritative_applicable = False
    authoritative_visibility = VisibilityState.UNKNOWN
    direct_target_reveals: list[DirectTargetRevealEvidence] = []

    target_player = None
    if target_player_id is not None:
        target_player = next(
            (
                player
                for player in match.players
                if player.player_id == target_player_id and player.hero_name
            ),
            None,
        )
        if target_player is not None:
            authoritative_applicable = True
            authoritative_visibility = hero_visibility_at(
                match,
                player_id=target_player_id,
                observing_team=team,
                tick=tick,
            )

            matching_players = [
                player for player in match.players if player.hero_name == target_player.hero_name
            ]
            target_reveal_usable = True
            if len(matching_players) != 1:
                add_gap("target_identity_ambiguous", target_player.hero_name)
                target_reveal_usable = False
            if target_player.team not in (2, 3):
                add_gap("target_team_unknown", target_player.hero_name)
                target_reveal_usable = False
            elif target_player.team == team:
                add_gap(
                    "direct_target_reveal_target_team_conflict",
                    target_player.hero_name,
                )
                target_reveal_usable = False

            for mod_ev in getattr(match, "vision_modifiers", []):
                if not target_reveal_usable:
                    break
                if mod_ev.semantic != VisionModifierSemantic.DIRECT_TARGET_REVEAL:
                    continue
                if mod_ev.target_name != target_player.hero_name:
                    continue
                if not mod_ev.target_is_hero or mod_ev.target_is_illusion:
                    continue
                if mod_ev.tick > tick:
                    continue
                # Observed removal ticks bound a half-open interval. Check
                # temporal relevance before recording gaps so old, ended
                # evidence cannot make a current assessment incomplete.
                if mod_ev.end_tick is not None and tick >= mod_ev.end_tick:
                    continue
                if mod_ev.target_team in (2, 3) and mod_ev.target_team != target_player.team:
                    add_gap(
                        "direct_target_reveal_target_team_conflict",
                        mod_ev.modifier_name,
                    )
                    continue
                if mod_ev.caster_team == 0:
                    add_gap("direct_target_reveal_team_unknown", mod_ev.modifier_name)
                    continue
                if mod_ev.caster_team != team:
                    continue

                unusable = False
                if mod_ev.lifecycle_status not in (
                    VisionModifierLifecycleStatus.REMOVED,
                    VisionModifierLifecycleStatus.EXPIRED,
                ):
                    add_gap("direct_target_reveal_incomplete", mod_ev.modifier_name)
                    unusable = True
                if mod_ev.pairing_status not in (
                    VisionModifierPairingStatus.EXACT,
                    VisionModifierPairingStatus.UNIQUE_FALLBACK,
                ):
                    add_gap("direct_target_reveal_ambiguous", mod_ev.modifier_name)
                    unusable = True
                if (
                    mod_ev.end_tick is None
                    or mod_ev.close_evidence is not VisionModifierCloseEvidence.OBSERVED
                ):
                    add_gap("direct_target_reveal_unbounded", mod_ev.modifier_name)
                    unusable = True
                if unusable:
                    continue

                direct_target_reveals.append(
                    DirectTargetRevealEvidence(
                        modifier_name=mod_ev.modifier_name,
                        target_name=mod_ev.target_name,
                        caster_name=mod_ev.caster_name,
                        caster_team=mod_ev.caster_team,
                        start_tick=mod_ev.tick,
                        end_tick=mod_ev.end_tick,
                        target_player_id=target_player_id,
                    )
                )
        else:
            add_gap("target_player_missing", f"player:{target_player_id}")

    sources.sort(key=lambda s: s.distance)
    if sources:
        status = PointVisionStatus.SUPPORTED
    elif point_incomplete:
        status = PointVisionStatus.INCOMPLETE
    else:
        status = PointVisionStatus.UNSUPPORTED

    return PointVisionAssessment(
        team=team,
        tick=tick,
        x=x,
        y=y,
        status=status,
        sources=sources,
        gaps=gaps,
        direct_target_reveals=direct_target_reveals,
        target_player_id=target_player_id,
        authoritative_applicable=authoritative_applicable,
        authoritative_visibility=authoritative_visibility,
        max_position_age_ticks=max_position_age_ticks,
    )


def estimate_vision(
    match: ParsedMatch,
    team: int,
    tick: int,
    x: float,
    y: float,
    *,
    max_position_age_ticks: int = 150,
) -> list[VisionSource]:
    """Return bounded modeled hero and observer sources covering a map point.

    This compatibility helper retains its list return shape. It now applies the
    same sample freshness and ward lifetime rules as :func:`assess_point_vision`
    and no longer treats target-specific modifier reveals as arbitrary-point
    geometry. Use the structured API when unsupported and incomplete evidence
    must be distinguished.

    Args:
        match: A parsed replay.
        team: Team number to assess (2=Radiant, 3=Dire).
        tick: Replay tick to query.
        x: Queried world x coordinate.
        y: Queried world y coordinate.
        max_position_age_ticks: Maximum allowed absolute hero sample age.

    Returns:
        Compatible source records sorted by ascending distance. An empty list
        is not proof that the point was hidden in-game.

    Raises:
        ValueError: If ``team`` is invalid or the age bound is negative.
    """
    assessment = assess_point_vision(
        match,
        team,
        tick,
        x,
        y,
        max_position_age_ticks=max_position_age_ticks,
    )
    return [
        VisionSource(
            kind="ward" if source.kind == "observer_ward" else "hero",
            name=source.name,
            distance=source.distance,
            vision_radius=source.vision_radius,
            x=source.x,
            y=source.y,
            position_tick=source.position_tick,
            position_age_ticks=source.position_age_ticks,
            player_id=source.player_id,
            position_provenance=source.position_provenance,
        )
        for source in assessment.sources
    ]


_WARD_VISION_RADIUS_SQ: int = _WARD_VISION * _WARD_VISION


def ward_vision_impact(ward: object, match: ParsedMatch) -> int:
    """Count distinct enemy heroes spotted by an observer ward during its lifetime.

    For each enemy hero, checks whether any position sample within the ward's
    active window falls within the standard 1600-unit observer ward vision
    radius.  Only the first sighting per hero is counted — the goal is to
    measure how many distinct enemies the ward revealed, not how many times.

    Only observer wards are evaluated; sentry wards return 0.

    Args:
        ward: A ward object (e.g. from ``match.wards``) with attributes:
            ``ward_type``, ``x``, ``y``, ``tick``, ``killed_tick``,
            ``expires_tick``, ``team``.
        match: A parsed replay with ``players`` and ``game_end_tick`` populated.

    Returns:
        Number of distinct enemy heroes that entered the ward's vision radius
        while it was alive. Returns 0 for sentry wards or wards with no
        coordinate data.

    Note:
        This is an **approximation**, not ground-truth vision data:

        - Position samples are taken every ~5 seconds (150 ticks), so heroes
          passing through the ward's radius between samples go undetected.
        - Vision is a flat 2D radius check — terrain, cliffs, and trees that
          block line-of-sight in-game are not modelled.
        - Night vision (800 units) is not distinguished from day vision (1600
          units); the full 1600-unit radius is always used.

        The result is suitable as a heuristic ward-quality signal, not a
        precise replay-accurate vision count.

    Example:
        >>> impact = ward_vision_impact(ward, match)
        >>> print(f"Ward spotted {impact} distinct enemy heroes")
    """
    if getattr(ward, "ward_type", "") != "observer":
        return 0
    wx = getattr(ward, "x", None)
    wy = getattr(ward, "y", None)
    if wx is None or wy is None:
        return 0

    ward_tick: int = getattr(ward, "tick", 0)
    end_tick: int = (
        getattr(ward, "killed_tick", None)
        or getattr(ward, "expires_tick", None)
        or infer_match_end_tick(match)
        or 0
    )
    enemy_team = 3 if getattr(ward, "team", 0) == 2 else 2

    seen: set[str] = set()
    for player in match.players:
        if player.team != enemy_team:
            continue
        for tick, px, py in player.position_log:
            if tick < ward_tick or tick > end_tick:
                continue
            if (px - wx) ** 2 + (py - wy) ** 2 <= _WARD_VISION_RADIUS_SQ:
                seen.add(player.hero_name)
                break  # one sighting is enough per hero
    return len(seen)
