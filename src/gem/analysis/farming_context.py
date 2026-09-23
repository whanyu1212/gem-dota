"""Comparative, evidence-aware context for farming route segments.

The route builder owns factual camp membership and interaction evidence. This
module adds bounded comparative context without converting missing inputs to
zero or inferring player intent.
"""

from __future__ import annotations

import math
from collections.abc import Iterable
from typing import TYPE_CHECKING

from gem.analysis._territory import build_territory_window
from gem.analysis.farming import (
    FarmingCampZone,
    FarmingContextConfig,
    FarmingContextTag,
    FarmingRoute,
    FarmingSegmentContext,
)
from gem.analysis.roshan import build_rosh_conversions
from gem.analysis.vision import assess_point_vision

if TYPE_CHECKING:
    from gem.results.models import ParsedMatch, ParsedPlayer

_TEAM_RADIANT = 2
_TEAM_DIRE = 3
_TICKS_PER_SECOND = 30


def _enemy_team(team: int) -> int:
    return _TEAM_DIRE if team == _TEAM_RADIANT else _TEAM_RADIANT


def _position_presence(
    players: Iterable[ParsedPlayer],
    *,
    start_tick: int,
    end_tick: int,
    x: float,
    y: float,
    config: FarmingContextConfig,
) -> tuple[float | None, float | None]:
    roster = list(players)
    duration = max(end_tick - start_tick, 0)
    if not roster or duration <= 0:
        return None, None

    expected_ticks = duration * len(roster)
    observed_ticks = 0
    nearby_ticks = 0
    for player in roster:
        samples = sorted(player.position_log)
        for current, following in zip(samples, samples[1:], strict=False):
            tick, sample_x, sample_y = current
            next_tick = following[0]
            gap = next_tick - tick
            if gap <= 0 or gap > config.max_position_gap_ticks:
                continue
            interval_start = max(tick, start_tick)
            interval_end = min(next_tick, end_tick)
            if interval_end <= interval_start:
                continue
            overlap = interval_end - interval_start
            observed_ticks += overlap
            if math.dist((sample_x, sample_y), (x, y)) <= config.presence_radius:
                nearby_ticks += overlap

    coverage = observed_ticks / expected_ticks if expected_ticks else None
    return nearby_ticks / _TICKS_PER_SECOND, coverage


def _nearest_fresh_value(
    player: ParsedPlayer,
    values: list[int],
    tick: int,
    max_age_ticks: int,
) -> int | None:
    length = min(len(player.times), len(values))
    if length == 0:
        return None
    index = min(range(length), key=lambda item: (abs(player.times[item] - tick), item))
    if abs(player.times[index] - tick) > max_age_ticks:
        return None
    return values[index]


def _team_advantage(
    match: ParsedMatch,
    team: int,
    tick: int,
    config: FarmingContextConfig,
) -> tuple[int | None, int | None, list[str]]:
    enemy = _enemy_team(team)
    teams = {
        team: [player for player in match.players if player.team == team],
        enemy: [player for player in match.players if player.team == enemy],
    }
    gaps: list[str] = []
    net_worth_values: dict[int, int] = {}
    total_xp_values: dict[int, int] = {}
    for current_team, players in teams.items():
        if not players:
            gaps.append(f"team_{current_team}_roster_unavailable")
            continue
        net_worth: list[int] = []
        total_xp: list[int] = []
        for player in players:
            net = _nearest_fresh_value(
                player,
                player.net_worth_t,
                tick,
                config.max_resource_age_ticks,
            )
            xp = _nearest_fresh_value(
                player,
                player.total_earned_xp_t,
                tick,
                config.max_resource_age_ticks,
            )
            if net is None:
                gaps.append(f"player_{player.player_id}_net_worth_sample_unavailable")
            else:
                net_worth.append(net)
            if xp is None:
                gaps.append(f"player_{player.player_id}_total_xp_sample_unavailable")
            else:
                total_xp.append(xp)
        if len(net_worth) == len(players):
            net_worth_values[current_team] = sum(net_worth)
        if len(total_xp) == len(players):
            total_xp_values[current_team] = sum(total_xp)

    net_worth_advantage = (
        net_worth_values[team] - net_worth_values[enemy]
        if team in net_worth_values and enemy in net_worth_values
        else None
    )
    total_xp_advantage = (
        total_xp_values[team] - total_xp_values[enemy]
        if team in total_xp_values and enemy in total_xp_values
        else None
    )
    return net_worth_advantage, total_xp_advantage, gaps


def _relevant_towers_alive(
    match: ParsedMatch,
    team: int,
    lane: str,
    tick: int,
) -> int | None:
    if lane not in {"top", "mid", "bot"}:
        return None
    owner = "goodguys" if team == _TEAM_RADIANT else "badguys"
    destroyed = {
        event.tower_name
        for event in match.towers
        if event.team == team
        and event.tick <= tick
        and event.tower_name.startswith(f"npc_dota_{owner}_tower")
        and event.tower_name.endswith(f"_{lane}")
        and ("_tower1_" in event.tower_name or "_tower2_" in event.tower_name)
    }
    return max(0, 2 - len(destroyed))


def _tormentor_at_tick(match: ParsedMatch, tick: int) -> tuple[int | None, int | None, str | None]:
    eligible = [event for event in match.tormentors if event.tick <= tick]
    if not eligible:
        return None, None, None
    event = max(eligible, key=lambda item: item.tick)
    if event.killer_team in (_TEAM_RADIANT, _TEAM_DIRE):
        return event.tick, event.killer_team, "protocol"
    player = next(
        (item for item in match.players if item.player_id == event.killer_player_id),
        None,
    )
    if player is not None and player.team in (_TEAM_RADIANT, _TEAM_DIRE):
        return event.tick, player.team, "player_id"
    matching = [item for item in match.players if item.hero_name and item.hero_name == event.killer]
    if len(matching) == 1 and matching[0].team in (_TEAM_RADIANT, _TEAM_DIRE):
        return event.tick, matching[0].team, "killer_name"
    return event.tick, None, "unknown"


def _tag(
    context: FarmingSegmentContext,
    tag: FarmingContextTag,
    *reasons: str,
) -> None:
    if tag not in context.tags:
        context.tags.append(tag)
    context.tag_reasons[tag.value] = list(reasons)


def _camp_side(owner_team: int | None, perspective_team: int) -> str:
    if owner_team is None:
        return "border"
    if owner_team == perspective_team:
        return "own_side"
    if owner_team == _enemy_team(perspective_team):
        return "enemy_side"
    return "unknown"


def attach_farming_contexts(
    match: ParsedMatch,
    routes: list[FarmingRoute],
    zones: tuple[FarmingCampZone, ...],
    config: FarmingContextConfig,
) -> None:
    """Populate segment context in place for already reconstructed routes."""
    zones_by_id = {zone.camp_id: zone for zone in zones}
    conversions = build_rosh_conversions(match) if match.roshans else []

    for route in routes:
        if route.team not in (_TEAM_RADIANT, _TEAM_DIRE):
            continue
        enemy_team = _enemy_team(route.team)
        own_players = [player for player in match.players if player.team == route.team]
        enemy_players = [player for player in match.players if player.team == enemy_team]
        for segment in route.segments:
            zone = zones_by_id.get(segment.camp_id)
            if zone is None:
                continue
            midpoint = (segment.start_tick + segment.end_tick) // 2
            lookback_start = max(match.game_start_tick or 0, midpoint - config.lookback_ticks)
            side = _camp_side(zone.owner_team, route.team)
            context = FarmingSegmentContext(
                midpoint_tick=midpoint,
                lookback_start_tick=lookback_start,
                camp_side=side,  # type: ignore[arg-type]
                camp_lane=zone.lane,
                camp_area=zone.area,
            )
            reasons: list[str] = []

            if side == "own_side":
                _tag(context, FarmingContextTag.OWN_SIDE, "camp topology owner matches player team")
            elif side == "enemy_side":
                _tag(context, FarmingContextTag.ENEMY_SIDE, "camp topology owner is opposing team")
            elif side == "border":
                _tag(context, FarmingContextTag.BORDER, "camp topology has no owning team")
            else:
                reasons.append("camp_topology_unavailable")

            (
                context.own_presence_hero_seconds,
                context.own_presence_position_coverage,
            ) = _position_presence(
                own_players,
                start_tick=lookback_start,
                end_tick=midpoint,
                x=zone.center_x,
                y=zone.center_y,
                config=config,
            )
            (
                context.enemy_presence_hero_seconds,
                context.enemy_presence_position_coverage,
            ) = _position_presence(
                enemy_players,
                start_tick=lookback_start,
                end_tick=midpoint,
                x=zone.center_x,
                y=zone.center_y,
                config=config,
            )
            presence_complete = True
            if (
                context.own_presence_position_coverage is None
                or context.own_presence_position_coverage < config.min_presence_coverage
            ):
                reasons.append("own_presence_position_coverage_below_threshold")
                presence_complete = False
            if (
                context.enemy_presence_position_coverage is None
                or context.enemy_presence_position_coverage < config.min_presence_coverage
            ):
                reasons.append("enemy_presence_position_coverage_below_threshold")
                presence_complete = False
            if (
                presence_complete
                and context.own_presence_hero_seconds is not None
                and context.enemy_presence_hero_seconds is not None
                and context.enemy_presence_hero_seconds >= config.high_enemy_presence_seconds
                and context.enemy_presence_hero_seconds - context.own_presence_hero_seconds
                >= config.presence_advantage_seconds
            ):
                _tag(
                    context,
                    FarmingContextTag.HIGH_ENEMY_PRESENCE,
                    "enemy local hero-seconds meet the configured floor",
                    "enemy local hero-seconds exceed allied local hero-seconds",
                )

            own_vision = assess_point_vision(
                match,
                route.team,
                midpoint,
                zone.center_x,
                zone.center_y,
                max_position_age_ticks=config.max_vision_position_age_ticks,
            )
            enemy_vision = assess_point_vision(
                match,
                enemy_team,
                midpoint,
                zone.center_x,
                zone.center_y,
                max_position_age_ticks=config.max_vision_position_age_ticks,
            )
            context.own_point_vision_status = own_vision.status.value
            context.enemy_point_vision_status = enemy_vision.status.value
            context.own_point_vision_source_count = len(own_vision.sources)
            context.enemy_point_vision_source_count = len(enemy_vision.sources)
            context.own_observer_vision_source_count = sum(
                source.kind == "observer_ward" for source in own_vision.sources
            )
            context.enemy_observer_vision_source_count = sum(
                source.kind == "observer_ward" for source in enemy_vision.sources
            )
            context.own_point_vision_gaps = [gap.code for gap in own_vision.gaps]
            context.enemy_point_vision_gaps = [gap.code for gap in enemy_vision.gaps]
            reasons.extend(f"own_point_vision:{gap.code}" for gap in own_vision.gaps)
            reasons.extend(f"enemy_point_vision:{gap.code}" for gap in enemy_vision.gaps)
            if (
                not own_vision.gaps
                and not enemy_vision.gaps
                and context.enemy_observer_vision_source_count > 0
                and context.own_observer_vision_source_count == 0
            ):
                _tag(
                    context,
                    FarmingContextTag.VISION_DISADVANTAGE,
                    "opponent has modeled observer coverage at the camp",
                    "player team has no modeled observer coverage at the camp",
                )

            context.own_relevant_towers_alive = _relevant_towers_alive(
                match, route.team, zone.lane, midpoint
            )
            context.enemy_relevant_towers_alive = _relevant_towers_alive(
                match, enemy_team, zone.lane, midpoint
            )
            if zone.lane == "unknown":
                reasons.append("camp_lane_topology_unavailable")
            elif (
                context.own_relevant_towers_alive is not None
                and context.enemy_relevant_towers_alive is not None
                and context.own_relevant_towers_alive < context.enemy_relevant_towers_alive
            ):
                _tag(
                    context,
                    FarmingContextTag.TOWER_DISADVANTAGE,
                    "fewer allied tier-one/tier-two towers remain in the affiliated lane",
                )

            (
                context.net_worth_advantage,
                context.total_earned_xp_advantage,
                resource_gaps,
            ) = _team_advantage(match, route.team, midpoint, config)
            reasons.extend(resource_gaps)

            active_conversion = next(
                (
                    conversion
                    for conversion in reversed(conversions)
                    if conversion.aegis_pickup_tick is not None
                    and conversion.aegis_pickup_tick <= midpoint < conversion.aegis_end_tick
                    and conversion.conversion_team in (_TEAM_RADIANT, _TEAM_DIRE)
                ),
                None,
            )
            context.aegis_active = active_conversion is not None
            if active_conversion is not None:
                context.aegis_holder_team = active_conversion.conversion_team
                context.aegis_source = (
                    f"{active_conversion.conversion_team_source.value}:"
                    f"{active_conversion.aegis_fate_source.value}"
                )
                if active_conversion.conversion_team == enemy_team:
                    _tag(
                        context,
                        FarmingContextTag.ENEMY_AEGIS_ACTIVE,
                        "opponent holds Aegis inside its bounded lifecycle",
                    )
            else:
                context.aegis_source = "no_active_aegis"

            prior_conversions = [item for item in conversions if item.rosh_tick <= midpoint]
            if prior_conversions:
                last_roshan = max(prior_conversions, key=lambda item: item.rosh_tick)
                context.last_roshan_tick = last_roshan.rosh_tick
                context.last_roshan_team = last_roshan.roshan_team
                context.roshan_team_source = last_roshan.roshan_team_source.value
            (
                context.last_tormentor_tick,
                context.last_tormentor_team,
                context.tormentor_team_source,
            ) = _tormentor_at_tick(match, midpoint)

            territory_start = max(
                match.game_start_tick or 0,
                midpoint - config.territory_lookback_ticks,
            )
            territory = build_territory_window(match, route.team, territory_start, midpoint)
            context.territory_coverage_differential_pct = territory.coverage_differential_pct
            context.territory_depth_differential = territory.depth_differential
            reasons.extend(f"territory:{reason}" for reason in territory.status_reasons)
            if (
                side == "enemy_side"
                and territory.status == "complete"
                and context.territory_coverage_differential_pct is not None
                and context.territory_depth_differential is not None
                and (
                    context.territory_coverage_differential_pct
                    >= config.territorial_coverage_delta_pct
                    or context.territory_depth_differential >= config.territorial_depth_delta
                )
            ):
                _tag(
                    context,
                    FarmingContextTag.TERRITORIAL_ADVANCE,
                    "enemy-side segment overlaps a sustained comparative territory advantage",
                )

            context.status_reasons = sorted(set(reasons))
            if context.status_reasons:
                context.status = "partial"
                _tag(
                    context,
                    FarmingContextTag.INCOMPLETE_CONTEXT,
                    *context.status_reasons,
                )
            else:
                context.status = "complete"
            segment.context = context


__all__ = ["attach_farming_contexts"]
