"""Evidence-first neutral-camp route reconstruction.

This module turns sampled hero positions into deterministic camp-local route
segments.  It preserves sample, continuity, combat, and resource provenance;
it does not infer player intent or claim that a camp was completely cleared.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any, Literal

from gem.catalog.map import load_camp_zones

if TYPE_CHECKING:
    from gem.results.models import ParsedMatch, ParsedPlayer

_TICKS_PER_SECOND = 30


class FarmingEvidenceStrength(str, Enum):
    """Conservative support level for a camp-local route segment."""

    TRANSIT_LIKE = "transit_like"
    WEAK = "weak_farm_evidence"
    STRONG = "strong_farm_evidence"


class FarmingBoundaryReason(str, Enum):
    """Observed reason a route segment started or ended."""

    ZONE_ENTRY = "zone_entry"
    ZONE_EXIT = "zone_exit"
    CAMP_CHANGE = "camp_change"
    SAMPLE_GAP = "sample_gap"
    LARGE_JUMP = "large_jump"
    LOG_END = "log_end"


@dataclass(frozen=True, slots=True)
class FarmingRouteConfig:
    """Inspectable thresholds for farming-route reconstruction."""

    max_sample_gap_ticks: int = 10 * _TICKS_PER_SECOND
    max_contiguous_speed: float = 900.0
    merge_gap_ticks: int = 5 * _TICKS_PER_SECOND
    min_weak_dwell_ticks: int = 5 * _TICKS_PER_SECOND
    resource_max_age_ticks: int = 2 * _TICKS_PER_SECOND

    def __post_init__(self) -> None:
        if self.max_sample_gap_ticks <= 0:
            raise ValueError("max_sample_gap_ticks must be positive")
        if self.max_contiguous_speed <= 0:
            raise ValueError("max_contiguous_speed must be positive")
        if self.merge_gap_ticks < 0:
            raise ValueError("merge_gap_ticks must be nonnegative")
        if self.min_weak_dwell_ticks < 0:
            raise ValueError("min_weak_dwell_ticks must be nonnegative")
        if self.resource_max_age_ticks < 0:
            raise ValueError("resource_max_age_ticks must be nonnegative")


DEFAULT_FARMING_ROUTE_CONFIG = FarmingRouteConfig()


@dataclass(frozen=True, slots=True)
class FarmingCampZone:
    """One calibrated neutral-camp zone from the bundled catalog."""

    camp_id: int
    camp_type: str
    center_x: float
    center_y: float
    shape: str
    radius_x: float
    radius_y: float
    rotation_degrees: float
    polygon_points: tuple[tuple[float, float], ...] = ()
    enter_margin: float = 0.0
    exit_margin: float = 0.0


@dataclass(frozen=True, slots=True)
class FarmingRoutePoint:
    """One sampled route point and its selected camp membership."""

    tick: int
    x: float
    y: float
    camp_id: int | None
    camp_type: str | None
    inside_base_zone: bool
    boundary_before: FarmingBoundaryReason | None = None


@dataclass(slots=True)
class FarmingRouteSegment:
    """One camp-local sampled route segment with factual support evidence."""

    segment_index: int
    player_id: int
    hero_name: str
    team: int
    camp_id: int
    camp_type: str
    start_tick: int
    end_tick: int
    duration_seconds: float
    start_reason: FarmingBoundaryReason
    end_reason: FarmingBoundaryReason
    sample_count: int
    in_zone_sample_count: int
    position_coverage: float | None
    max_sample_gap_ticks: int | None
    micro_exit_merged: bool
    neutral_kills: int
    neutral_damage: int
    window_xp_delta: int | None
    window_total_earned_gold_delta: int | None
    resource_start_sample_tick: int | None
    resource_end_sample_tick: int | None
    evidence_strength: FarmingEvidenceStrength
    evidence_reasons: list[str] = field(default_factory=list)
    evidence_gaps: list[str] = field(default_factory=list)
    points: list[FarmingRoutePoint] = field(default_factory=list)


@dataclass(slots=True)
class FarmingRoute:
    """Evidence-first farming route for one parsed player."""

    player_id: int
    hero_name: str
    team: int
    camp_catalog_version: int | None
    camp_map_patch: str | None
    status: Literal["complete", "partial", "unavailable"]
    status_reasons: list[str] = field(default_factory=list)
    points: list[FarmingRoutePoint] = field(default_factory=list)
    segments: list[FarmingRouteSegment] = field(default_factory=list)


@dataclass(slots=True)
class _SegmentCandidate:
    zone: FarmingCampZone
    start_index: int
    end_index: int
    start_reason: FarmingBoundaryReason
    end_reason: FarmingBoundaryReason
    micro_exit_merged: bool = False


def _parse_zones(payload: dict[str, Any]) -> tuple[FarmingCampZone, ...]:
    zones: list[FarmingCampZone] = []
    for raw in payload.get("camps", []):
        center = raw.get("center", {})
        geometry = raw.get("zone", {})
        hysteresis = raw.get("hysteresis", {})
        points = tuple(
            (
                float(point.get("x", 0.0) if isinstance(point, dict) else point[0]),
                float(point.get("y", 0.0) if isinstance(point, dict) else point[1]),
            )
            for point in geometry.get("points", [])
        )
        zones.append(
            FarmingCampZone(
                camp_id=int(raw["id"]),
                camp_type=str(raw.get("type", "unknown")),
                center_x=float(center.get("x", 0.0)),
                center_y=float(center.get("y", 0.0)),
                shape=str(geometry.get("shape", "ellipse")),
                radius_x=float(geometry.get("rx", 0.0)),
                radius_y=float(geometry.get("ry", 0.0)),
                rotation_degrees=float(geometry.get("rotation_deg", 0.0)),
                polygon_points=points,
                enter_margin=float(hysteresis.get("enter_margin", 0.0)),
                exit_margin=float(hysteresis.get("exit_margin", 0.0)),
            )
        )
    return tuple(sorted(zones, key=lambda zone: zone.camp_id))


def _point_in_polygon(x: float, y: float, points: tuple[tuple[float, float], ...]) -> bool:
    if len(points) < 3:
        return False
    inside = False
    previous = len(points) - 1
    for index, (current_x, current_y) in enumerate(points):
        previous_x, previous_y = points[previous]
        intersects = (current_y > y) != (previous_y > y) and x < (
            (previous_x - current_x) * (y - current_y) / ((previous_y - current_y) or 1e-9)
            + current_x
        )
        if intersects:
            inside = not inside
        previous = index
    return inside


def _contains(zone: FarmingCampZone, x: float, y: float, margin: float = 0.0) -> bool:
    if zone.shape == "ellipse":
        radius_x = zone.radius_x + margin
        radius_y = zone.radius_y + margin
        if radius_x <= 0.0 or radius_y <= 0.0:
            return False
        angle = math.radians(zone.rotation_degrees)
        dx = x - zone.center_x
        dy = y - zone.center_y
        local_x = dx * math.cos(angle) + dy * math.sin(angle)
        local_y = -dx * math.sin(angle) + dy * math.cos(angle)
        return (local_x * local_x) / (radius_x * radius_x) + (local_y * local_y) / (
            radius_y * radius_y
        ) <= 1.0
    if zone.shape == "polygon":
        # The current catalog uses ellipses. Polygon membership remains exact;
        # a future polygon catalog should provide explicit expanded geometry
        # rather than relying on an ambiguous synthetic margin.
        return _point_in_polygon(x, y, zone.polygon_points)
    return False


def _normalized_distance(zone: FarmingCampZone, x: float, y: float) -> float:
    if zone.shape != "ellipse" or zone.radius_x <= 0 or zone.radius_y <= 0:
        return math.dist((x, y), (zone.center_x, zone.center_y))
    angle = math.radians(zone.rotation_degrees)
    dx = x - zone.center_x
    dy = y - zone.center_y
    local_x = dx * math.cos(angle) + dy * math.sin(angle)
    local_y = -dx * math.sin(angle) + dy * math.cos(angle)
    return math.hypot(local_x / zone.radius_x, local_y / zone.radius_y)


def _select_zone(
    zones: tuple[FarmingCampZone, ...],
    x: float,
    y: float,
    current: FarmingCampZone | None,
) -> tuple[FarmingCampZone | None, bool]:
    if current is not None and _contains(current, x, y, current.exit_margin):
        return current, _contains(current, x, y)
    candidates = [zone for zone in zones if _contains(zone, x, y, zone.enter_margin)]
    if not candidates:
        return None, False
    selected = min(candidates, key=lambda zone: (_normalized_distance(zone, x, y), zone.camp_id))
    return selected, True


def _continuity_boundary(
    previous: tuple[int, float, float],
    current: tuple[int, float, float],
    config: FarmingRouteConfig,
) -> FarmingBoundaryReason | None:
    elapsed_ticks = current[0] - previous[0]
    if elapsed_ticks <= 0:
        return (
            FarmingBoundaryReason.LARGE_JUMP if math.dist(previous[1:], current[1:]) > 0 else None
        )
    if elapsed_ticks > config.max_sample_gap_ticks:
        return FarmingBoundaryReason.SAMPLE_GAP
    elapsed_seconds = elapsed_ticks / _TICKS_PER_SECOND
    speed = math.dist(previous[1:], current[1:]) / elapsed_seconds
    if speed > config.max_contiguous_speed:
        return FarmingBoundaryReason.LARGE_JUMP
    return None


def _route_points(
    player: ParsedPlayer,
    zones: tuple[FarmingCampZone, ...],
    config: FarmingRouteConfig,
    min_tick: int,
) -> list[FarmingRoutePoint]:
    raw_points = sorted(
        (point for point in player.position_log if point[0] >= min_tick),
        key=lambda point: point[0],
    )
    points: list[FarmingRoutePoint] = []
    current_zone: FarmingCampZone | None = None
    previous: tuple[int, float, float] | None = None
    for tick, x, y in raw_points:
        raw = (int(tick), float(x), float(y))
        boundary = _continuity_boundary(previous, raw, config) if previous is not None else None
        if boundary is not None:
            current_zone = None
        selected, inside_base = _select_zone(zones, raw[1], raw[2], current_zone)
        points.append(
            FarmingRoutePoint(
                tick=raw[0],
                x=raw[1],
                y=raw[2],
                camp_id=selected.camp_id if selected else None,
                camp_type=selected.camp_type if selected else None,
                inside_base_zone=inside_base,
                boundary_before=boundary,
            )
        )
        current_zone = selected
        previous = raw
    return points


def _segment_candidates(
    points: list[FarmingRoutePoint], zones_by_id: dict[int, FarmingCampZone]
) -> list[_SegmentCandidate]:
    candidates: list[_SegmentCandidate] = []
    active: _SegmentCandidate | None = None
    for index, point in enumerate(points):
        camp_id = point.camp_id
        if active is not None and point.boundary_before is not None:
            active.end_index = index - 1
            active.end_reason = point.boundary_before
            candidates.append(active)
            active = None
        if camp_id is None:
            if active is not None:
                active.end_index = index - 1
                active.end_reason = FarmingBoundaryReason.ZONE_EXIT
                candidates.append(active)
                active = None
            continue
        zone = zones_by_id[camp_id]
        if active is None:
            active = _SegmentCandidate(
                zone=zone,
                start_index=index,
                end_index=index,
                start_reason=(point.boundary_before or FarmingBoundaryReason.ZONE_ENTRY),
                end_reason=FarmingBoundaryReason.LOG_END,
            )
            continue
        if active.zone.camp_id == camp_id:
            active.end_index = index
            continue
        active.end_index = index - 1
        active.end_reason = FarmingBoundaryReason.CAMP_CHANGE
        candidates.append(active)
        active = _SegmentCandidate(
            zone=zone,
            start_index=index,
            end_index=index,
            start_reason=FarmingBoundaryReason.CAMP_CHANGE,
            end_reason=FarmingBoundaryReason.LOG_END,
        )
    if active is not None:
        active.end_index = len(points) - 1
        active.end_reason = FarmingBoundaryReason.LOG_END
        candidates.append(active)
    return candidates


def _merge_candidates(
    candidates: list[_SegmentCandidate],
    points: list[FarmingRoutePoint],
    config: FarmingRouteConfig,
) -> list[_SegmentCandidate]:
    merged: list[_SegmentCandidate] = []
    for candidate in candidates:
        if not merged:
            merged.append(candidate)
            continue
        previous = merged[-1]
        gap_ticks = points[candidate.start_index].tick - points[previous.end_index].tick
        between = points[previous.end_index + 1 : candidate.start_index]
        can_merge = (
            previous.zone.camp_id == candidate.zone.camp_id
            and gap_ticks <= config.merge_gap_ticks
            and all(point.camp_id is None for point in between)
            and all(point.boundary_before is None for point in between)
            and points[candidate.start_index].boundary_before is None
        )
        if can_merge:
            previous.end_index = candidate.end_index
            previous.end_reason = candidate.end_reason
            previous.micro_exit_merged = True
        else:
            merged.append(candidate)
    return merged


def _nearest_fresh_sample(
    times: list[int],
    values: list[int],
    tick: int,
    max_age_ticks: int,
) -> tuple[int, int] | None:
    length = min(len(times), len(values))
    if length == 0:
        return None
    nearest_index = min(range(length), key=lambda index: (abs(times[index] - tick), times[index]))
    sample_tick = times[nearest_index]
    if abs(sample_tick - tick) > max_age_ticks:
        return None
    return values[nearest_index], sample_tick


def _resource_deltas(
    player: ParsedPlayer,
    start_tick: int,
    end_tick: int,
    config: FarmingRouteConfig,
) -> tuple[int | None, int | None, int | None, int | None, list[str]]:
    start_xp = _nearest_fresh_sample(
        player.times, player.xp_t, start_tick, config.resource_max_age_ticks
    )
    end_xp = _nearest_fresh_sample(
        player.times, player.xp_t, end_tick, config.resource_max_age_ticks
    )
    start_gold = _nearest_fresh_sample(
        player.times,
        player.total_earned_gold_t,
        start_tick,
        config.resource_max_age_ticks,
    )
    end_gold = _nearest_fresh_sample(
        player.times,
        player.total_earned_gold_t,
        end_tick,
        config.resource_max_age_ticks,
    )
    gaps: list[str] = []
    xp_delta: int | None = None
    gold_delta: int | None = None
    if start_xp is not None and end_xp is not None and end_xp[0] >= start_xp[0]:
        xp_delta = end_xp[0] - start_xp[0]
    else:
        gaps.append("xp_endpoint_samples_unavailable")
    if start_gold is not None and end_gold is not None and end_gold[0] >= start_gold[0]:
        gold_delta = end_gold[0] - start_gold[0]
    else:
        gaps.append("gold_endpoint_samples_unavailable")
    start_ticks = [sample[1] for sample in (start_xp, start_gold) if sample is not None]
    end_ticks = [sample[1] for sample in (end_xp, end_gold) if sample is not None]
    return (
        xp_delta,
        gold_delta,
        min(start_ticks) if start_ticks else None,
        max(end_ticks) if end_ticks else None,
        gaps,
    )


def _neutral_evidence(
    match: ParsedMatch,
    player: ParsedPlayer,
    zone: FarmingCampZone,
    start_tick: int,
    end_tick: int,
) -> tuple[int, int]:
    kills = 0
    damage = 0
    for entry in match.combat_log:
        if entry.tick < start_tick or entry.tick > end_tick:
            continue
        if not entry.target_name.startswith("npc_dota_neutral"):
            continue
        if player.hero_name not in {entry.attacker_name, entry.damage_source_name}:
            continue
        if (
            entry.location_x is not None
            and entry.location_y is not None
            and not _contains(zone, entry.location_x, entry.location_y)
        ):
            continue
        if entry.log_type == "DEATH":
            kills += 1
        elif entry.log_type == "DAMAGE" and entry.value > 0:
            damage += entry.value
    return kills, damage


def _position_metrics(
    points: list[FarmingRoutePoint], camp_id: int
) -> tuple[int, float | None, int | None]:
    if not points:
        return 0, None, None
    in_zone_count = sum(point.camp_id == camp_id for point in points)
    duration = points[-1].tick - points[0].tick
    if duration <= 0:
        return in_zone_count, None, None
    supported = 0
    maximum_gap = 0
    for previous, current in zip(points, points[1:], strict=False):
        gap = current.tick - previous.tick
        if gap <= 0 or current.boundary_before is not None:
            continue
        supported += gap
        maximum_gap = max(maximum_gap, gap)
    return in_zone_count, supported / duration, maximum_gap


def _build_segments(
    match: ParsedMatch,
    player: ParsedPlayer,
    points: list[FarmingRoutePoint],
    zones: tuple[FarmingCampZone, ...],
    config: FarmingRouteConfig,
) -> list[FarmingRouteSegment]:
    zones_by_id = {zone.camp_id: zone for zone in zones}
    candidates = _merge_candidates(_segment_candidates(points, zones_by_id), points, config)
    segments: list[FarmingRouteSegment] = []
    for segment_index, candidate in enumerate(candidates, start=1):
        segment_points = points[candidate.start_index : candidate.end_index + 1]
        start_tick = segment_points[0].tick
        end_tick = segment_points[-1].tick
        kills, damage = _neutral_evidence(match, player, candidate.zone, start_tick, end_tick)
        xp_delta, gold_delta, resource_start, resource_end, evidence_gaps = _resource_deltas(
            player, start_tick, end_tick, config
        )
        in_zone_count, coverage, maximum_gap = _position_metrics(
            segment_points, candidate.zone.camp_id
        )
        duration_ticks = max(end_tick - start_tick, 0)
        evidence_reasons: list[str] = []
        if kills > 0:
            strength = FarmingEvidenceStrength.STRONG
            evidence_reasons.append("neutral_death")
        else:
            if damage > 0:
                evidence_reasons.append("neutral_damage")
            if (xp_delta or 0) > 0:
                evidence_reasons.append("window_xp_gain")
            if (gold_delta or 0) > 0:
                evidence_reasons.append("window_gold_gain")
            supported_dwell = duration_ticks >= config.min_weak_dwell_ticks and in_zone_count >= 2
            if supported_dwell:
                evidence_reasons.append("supported_dwell")
            strength = (
                FarmingEvidenceStrength.WEAK
                if damage > 0 or supported_dwell
                else FarmingEvidenceStrength.TRANSIT_LIKE
            )
        segments.append(
            FarmingRouteSegment(
                segment_index=segment_index,
                player_id=player.player_id,
                hero_name=player.hero_name,
                team=player.team,
                camp_id=candidate.zone.camp_id,
                camp_type=candidate.zone.camp_type,
                start_tick=start_tick,
                end_tick=end_tick,
                duration_seconds=duration_ticks / _TICKS_PER_SECOND,
                start_reason=candidate.start_reason,
                end_reason=candidate.end_reason,
                sample_count=len(segment_points),
                in_zone_sample_count=in_zone_count,
                position_coverage=coverage,
                max_sample_gap_ticks=maximum_gap,
                micro_exit_merged=candidate.micro_exit_merged,
                neutral_kills=kills,
                neutral_damage=damage,
                window_xp_delta=xp_delta,
                window_total_earned_gold_delta=gold_delta,
                resource_start_sample_tick=resource_start,
                resource_end_sample_tick=resource_end,
                evidence_strength=strength,
                evidence_reasons=evidence_reasons,
                evidence_gaps=evidence_gaps,
                points=segment_points,
            )
        )
    return segments


def build_farming_routes(
    match: ParsedMatch,
    *,
    config: FarmingRouteConfig = DEFAULT_FARMING_ROUTE_CONFIG,
) -> list[FarmingRoute]:
    """Build deterministic camp-local route evidence for every parsed player.

    The builder keeps sampled movement and resource provenance explicit. Route
    tags describe evidence strength only; they do not infer farming intent or
    a complete camp clear.
    """
    try:
        payload = load_camp_zones()
        zones = _parse_zones(payload)
        catalog_version = int(payload["version"]) if "version" in payload else None
        map_patch = str(payload["dota_patch"]) if payload.get("dota_patch") is not None else None
    except (OSError, ValueError, KeyError, TypeError):
        zones = ()
        catalog_version = None
        map_patch = None

    routes: list[FarmingRoute] = []
    for player in sorted(match.players, key=lambda item: item.player_id):
        reasons: list[str] = []
        if not zones:
            reasons.append("camp_zone_catalog_unavailable")
        if not player.position_log:
            reasons.append("position_samples_unavailable")
        if reasons:
            routes.append(
                FarmingRoute(
                    player_id=player.player_id,
                    hero_name=player.hero_name,
                    team=player.team,
                    camp_catalog_version=catalog_version,
                    camp_map_patch=map_patch,
                    status="unavailable",
                    status_reasons=reasons,
                )
            )
            continue

        points = _route_points(player, zones, config, match.game_start_tick or 0)
        if not points:
            routes.append(
                FarmingRoute(
                    player_id=player.player_id,
                    hero_name=player.hero_name,
                    team=player.team,
                    camp_catalog_version=catalog_version,
                    camp_map_patch=map_patch,
                    status="unavailable",
                    status_reasons=["in_game_position_samples_unavailable"],
                )
            )
            continue
        segments = _build_segments(match, player, points, zones, config)
        status_reasons = sorted({gap for segment in segments for gap in segment.evidence_gaps})
        routes.append(
            FarmingRoute(
                player_id=player.player_id,
                hero_name=player.hero_name,
                team=player.team,
                camp_catalog_version=catalog_version,
                camp_map_patch=map_patch,
                status="partial" if status_reasons else "complete",
                status_reasons=status_reasons,
                points=points,
                segments=segments,
            )
        )
    return routes


__all__ = [
    "DEFAULT_FARMING_ROUTE_CONFIG",
    "FarmingBoundaryReason",
    "FarmingCampZone",
    "FarmingEvidenceStrength",
    "FarmingRoute",
    "FarmingRouteConfig",
    "FarmingRoutePoint",
    "FarmingRouteSegment",
    "build_farming_routes",
]
