"""Objective-aware map-context helpers for farming-pattern analysis.

These utilities turn match-level objective/vision telemetry into coarse
time buckets that can be joined with camp visits to reduce context blindness.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from gem.models import ParsedMatch

_TEAM_RADIANT = 2
_TEAM_DIRE = 3

_MAP_XMIN = 7563.0
_MAP_XMAX = 25900.0
_MAP_YMIN = 7800.0
_MAP_YMAX = 25600.0

_RADIANT_FOUNTAIN = (9684.0, 9684.0)
_DIRE_FOUNTAIN = (23120.0, 22350.0)

# Dota has 11 towers per side (T1/2/3 across lanes + T4 pair + filler naming variants).
# We keep this coarse on purpose; exact per-lane tower state is not required for v1 context.
_INITIAL_TOWERS_PER_TEAM = 11

_AEGIS_ACTIVE_TICKS = 5 * 60 * 30
_DEFAULT_BUCKET_TICKS = 900  # 30 seconds
_DEFAULT_PRESENCE_WINDOW_TICKS = 2700  # 90 seconds
_PRESENCE_TAU_TICKS = 900.0  # exponential decay ~30 seconds


@dataclass
class MapContextBucket:
    """Objective- and vision-aware map-state summary for one time bucket."""

    start_tick: int
    end_tick: int
    tower_alive_radiant: int
    tower_alive_dire: int
    t1_mid_alive_radiant: bool
    t1_mid_alive_dire: bool
    roshan_last_kill_tick: int | None
    aegis_holder_team: int | None
    aegis_active: bool
    tormentor_last_kill_tick: int | None
    ward_count_radiant: int
    ward_count_dire: int
    net_worth_advantage: int
    xp_advantage: int
    enemy_presence_by_region: dict[str, float] = field(default_factory=dict)


@dataclass
class CampVisitContext:
    """Context scores and explainability labels for one camp visit."""

    farm_safety_score: float
    pressure_score: float
    expected_value_score: float
    context_label: Literal[
        "safe_home_farm",
        "pressured_home_farm",
        "defensive_home_farm",
        "safe_invade",
        "pressure_invade",
        "high_risk_invade",
    ]
    context_drivers: list[str] = field(default_factory=list)


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def _active_ward_count(match: ParsedMatch, team: int, tick: int) -> int:
    count = 0
    for ward in match.wards:
        if ward.team != team or ward.ward_type != "observer":
            continue
        if ward.tick > tick:
            continue
        end_tick = ward.killed_tick if ward.killed_tick is not None else ward.expires_tick
        if end_tick is not None and tick > end_tick:
            continue
        count += 1
    return count


def _region_of(wx: float, wy: float) -> str:
    # Diagonal strip around the river.
    if abs(wx - wy) <= 1200:
        return "river"

    dr = math.dist((wx, wy), _RADIANT_FOUNTAIN)
    dd = math.dist((wx, wy), _DIRE_FOUNTAIN)
    return "radiant_half" if dr <= dd else "dire_half"


def _enemy_presence_by_region(
    match: ParsedMatch,
    team: int,
    start_tick: int,
    end_tick: int,
) -> dict[str, float]:
    enemy_regions: dict[str, float] = {"river": 0.0, "radiant_half": 0.0, "dire_half": 0.0}
    enemy_team = _TEAM_DIRE if team == _TEAM_RADIANT else _TEAM_RADIANT

    for player in match.players:
        if player.team != enemy_team:
            continue
        for tick, wx, wy in player.position_log:
            if tick < start_tick or tick > end_tick:
                continue
            # Recent samples contribute more than old samples in the window.
            age = float(end_tick - tick)
            weight = math.exp(-age / _PRESENCE_TAU_TICKS)
            enemy_regions[_region_of(wx, wy)] += weight

    # Soft normalization for easier thresholding; still interpretable as "more is higher pressure".
    # 10 is an empirical convenience scale for ~90s windows and 5 enemy heroes.
    for region in list(enemy_regions):
        enemy_regions[region] = _clamp01(enemy_regions[region] / 10.0)

    return enemy_regions


def _infer_match_end_tick(match: ParsedMatch) -> int:
    if match.game_end_tick > 0:
        return match.game_end_tick

    max_tick = 0
    for player in match.players:
        if player.times:
            max_tick = max(max_tick, player.times[-1])
        if player.position_log:
            max_tick = max(max_tick, player.position_log[-1][0])
    return max_tick


def _nearest_series_value(times: list[int], values: list[int], tick: int) -> int:
    if not times or not values:
        return 0
    lo = 0
    hi = len(times)
    while lo < hi:
        mid = (lo + hi) // 2
        if times[mid] < tick:
            lo = mid + 1
        else:
            hi = mid
    idx = lo
    if idx <= 0:
        return values[0]
    if idx >= len(times):
        return values[-1]
    before = idx - 1
    after = idx
    if tick - times[before] <= times[after] - tick:
        return values[before]
    return values[after]


def _team_resource_advantage(match: ParsedMatch, team: int, tick: int) -> tuple[int, int]:
    own_net_worth = 0
    own_xp = 0
    enemy_net_worth = 0
    enemy_xp = 0
    for player in match.players:
        net_worth = _nearest_series_value(player.times, player.net_worth_t, tick)
        xp = _nearest_series_value(player.times, player.xp_t, tick)
        if player.team == team:
            own_net_worth += net_worth
            own_xp += xp
        else:
            enemy_net_worth += net_worth
            enemy_xp += xp
    return own_net_worth - enemy_net_worth, own_xp - enemy_xp


def build_map_context_timeline(
    match: ParsedMatch,
    team: int,
    bucket_ticks: int = _DEFAULT_BUCKET_TICKS,
    presence_window_ticks: int = _DEFAULT_PRESENCE_WINDOW_TICKS,
) -> list[MapContextBucket]:
    """Build objective-aware context buckets for one team's perspective.

    Args:
        match: Parsed replay output.
        team: Perspective team (2=Radiant, 3=Dire). Enemy presence is computed
            relative to this team.
        bucket_ticks: Bucket width in ticks (default: 30s).
        presence_window_ticks: Window length used for decayed enemy-presence
            scoring (default: 90s).

    Returns:
        Chronological list of context buckets from game start to game end.
    """
    if team not in (_TEAM_RADIANT, _TEAM_DIRE):
        raise ValueError(f"team must be 2 or 3, got {team}")
    if bucket_ticks <= 0:
        raise ValueError(f"bucket_ticks must be > 0, got {bucket_ticks}")
    if presence_window_ticks <= 0:
        raise ValueError(f"presence_window_ticks must be > 0, got {presence_window_ticks}")

    start_tick = match.game_start_tick or 0
    end_tick = _infer_match_end_tick(match)
    if end_tick < start_tick:
        end_tick = start_tick

    towers_alive = {_TEAM_RADIANT: _INITIAL_TOWERS_PER_TEAM, _TEAM_DIRE: _INITIAL_TOWERS_PER_TEAM}
    t1_mid_alive = {_TEAM_RADIANT: True, _TEAM_DIRE: True}

    tower_events = sorted(match.towers, key=lambda t: t.tick)
    roshan_events = sorted(match.roshans, key=lambda r: r.tick)
    tormentor_events = sorted(match.tormentors, key=lambda t: t.tick)
    aegis_events = sorted(match.aegis_events, key=lambda a: a.tick)

    tower_i = 0
    roshan_i = 0
    tormentor_i = 0
    aegis_i = 0

    roshan_last_kill_tick: int | None = None
    tormentor_last_kill_tick: int | None = None
    aegis_holder_team: int | None = None
    aegis_pickup_tick: int | None = None

    slot_to_team: dict[int, int] = {player.player_id: player.team for player in match.players}

    buckets: list[MapContextBucket] = []
    tick = start_tick
    while tick <= end_tick:
        bucket_end = min(tick + bucket_ticks - 1, end_tick)

        while tower_i < len(tower_events) and tower_events[tower_i].tick <= bucket_end:
            tower_ev = tower_events[tower_i]
            if tower_ev.team in towers_alive:
                towers_alive[tower_ev.team] = max(0, towers_alive[tower_ev.team] - 1)
                if "tower1_mid" in tower_ev.tower_name:
                    t1_mid_alive[tower_ev.team] = False
            tower_i += 1

        while roshan_i < len(roshan_events) and roshan_events[roshan_i].tick <= bucket_end:
            roshan_last_kill_tick = roshan_events[roshan_i].tick
            roshan_i += 1

        while (
            tormentor_i < len(tormentor_events) and tormentor_events[tormentor_i].tick <= bucket_end
        ):
            tormentor_last_kill_tick = tormentor_events[tormentor_i].tick
            tormentor_i += 1

        while aegis_i < len(aegis_events) and aegis_events[aegis_i].tick <= bucket_end:
            aegis_ev = aegis_events[aegis_i]
            if aegis_ev.event_type in {"pickup", "stolen"}:
                aegis_holder_team = slot_to_team.get(aegis_ev.player_id)
                if aegis_holder_team in (_TEAM_RADIANT, _TEAM_DIRE):
                    aegis_pickup_tick = aegis_ev.tick
                else:
                    aegis_pickup_tick = None
            elif aegis_ev.event_type == "denied":
                aegis_holder_team = None
                aegis_pickup_tick = None
            aegis_i += 1

        aegis_active = (
            aegis_holder_team in (_TEAM_RADIANT, _TEAM_DIRE)
            and aegis_pickup_tick is not None
            and bucket_end - aegis_pickup_tick <= _AEGIS_ACTIVE_TICKS
        )
        if not aegis_active:
            aegis_holder_team = None
            aegis_pickup_tick = None

        presence_start = max(start_tick, bucket_end - presence_window_ticks + 1)
        enemy_presence = _enemy_presence_by_region(match, team, presence_start, bucket_end)
        net_worth_advantage, xp_advantage = _team_resource_advantage(match, team, bucket_end)

        buckets.append(
            MapContextBucket(
                start_tick=tick,
                end_tick=bucket_end,
                tower_alive_radiant=towers_alive[_TEAM_RADIANT],
                tower_alive_dire=towers_alive[_TEAM_DIRE],
                t1_mid_alive_radiant=t1_mid_alive[_TEAM_RADIANT],
                t1_mid_alive_dire=t1_mid_alive[_TEAM_DIRE],
                roshan_last_kill_tick=roshan_last_kill_tick,
                aegis_holder_team=aegis_holder_team,
                aegis_active=aegis_active,
                tormentor_last_kill_tick=tormentor_last_kill_tick,
                ward_count_radiant=_active_ward_count(match, _TEAM_RADIANT, bucket_end),
                ward_count_dire=_active_ward_count(match, _TEAM_DIRE, bucket_end),
                net_worth_advantage=net_worth_advantage,
                xp_advantage=xp_advantage,
                enemy_presence_by_region=enemy_presence,
            )
        )
        tick += bucket_ticks

    return buckets


def _load_camp_centers() -> dict[int, tuple[float, float]]:
    path = Path(__file__).resolve().parent / "data" / "neutral_camps.json"
    camps = json.loads(path.read_text(encoding="utf-8"))
    return {int(c["id"]): (float(c["x"]), float(c["y"])) for c in camps}


_CAMP_CENTERS = _load_camp_centers()


def _camp_half(camp_id: int) -> str:
    pos = _CAMP_CENTERS.get(camp_id)
    if pos is None:
        return "river"
    return _region_of(pos[0], pos[1])


def score_camp_visit_context(
    *,
    team: int,
    camp_id: int,
    camp_type: str,
    neutral_kills: int,
    neutral_damage: int,
    xp_gain: int,
    bucket: MapContextBucket,
) -> CampVisitContext:
    """Score one camp visit against a context bucket.

    Args:
        team: Team perspective (2=Radiant, 3=Dire).
        camp_id: Neutral camp id.
        camp_type: Camp type string (small/medium/large/ancient/...).
        neutral_kills: Neutral kills attributed to the visit.
        neutral_damage: Neutral damage attributed to the visit.
        xp_gain: XP gained in the visit window.
        bucket: Context bucket overlapping the visit.

    Returns:
        A context-scored visit object with explainability drivers.
    """
    if team not in (_TEAM_RADIANT, _TEAM_DIRE):
        raise ValueError(f"team must be 2 or 3, got {team}")

    own_half = "radiant_half" if team == _TEAM_RADIANT else "dire_half"
    enemy_half = "dire_half" if team == _TEAM_RADIANT else "radiant_half"

    own_towers = bucket.tower_alive_radiant if team == _TEAM_RADIANT else bucket.tower_alive_dire
    enemy_towers = bucket.tower_alive_dire if team == _TEAM_RADIANT else bucket.tower_alive_radiant
    tower_diff = (own_towers - enemy_towers) / float(_INITIAL_TOWERS_PER_TEAM)

    own_wards = bucket.ward_count_radiant if team == _TEAM_RADIANT else bucket.ward_count_dire
    enemy_wards = bucket.ward_count_dire if team == _TEAM_RADIANT else bucket.ward_count_radiant
    ward_diff = (own_wards - enemy_wards) / 6.0

    enemy_presence_own_half = bucket.enemy_presence_by_region.get(own_half, 0.0)
    enemy_presence_enemy_half = bucket.enemy_presence_by_region.get(enemy_half, 0.0)
    enemy_presence_river = bucket.enemy_presence_by_region.get("river", 0.0)

    enemy_aegis_active = bucket.aegis_active and bucket.aegis_holder_team not in (None, team)
    camp_half = _camp_half(camp_id)
    is_border = camp_half == "river"
    is_invading = camp_half == enemy_half

    safety = 0.55 + 0.25 * tower_diff + 0.20 * ward_diff
    safety -= 0.45 * enemy_presence_own_half
    if enemy_aegis_active:
        safety -= 0.20
    if is_invading:
        safety -= 0.15
    if is_border:
        safety -= 0.08
    farm_safety_score = _clamp01(safety)

    pressure = 0.30 + 0.40 * enemy_presence_own_half + 0.20 * enemy_presence_river
    pressure += max(0.0, -tower_diff) * 0.20
    if enemy_aegis_active:
        pressure += 0.20
    if is_invading:
        pressure += 0.15 + 0.15 * enemy_presence_enemy_half
    if is_border:
        pressure += 0.08
    pressure_score = _clamp01(pressure)

    camp_value = {
        "small": 0.35,
        "medium": 0.45,
        "large": 0.55,
        "ancient": 0.70,
        "flooded_small": 0.40,
        "flooded_medium": 0.50,
    }.get(camp_type, 0.45)
    evidence = 0.0
    evidence += min(neutral_kills / 4.0, 1.0) * 0.35
    evidence += min(neutral_damage / 3000.0, 1.0) * 0.30
    evidence += min(xp_gain / 600.0, 1.0) * 0.35
    expected_value_score = _clamp01(0.5 * camp_value + 0.5 * evidence)

    lost_t1_mid = not (
        bucket.t1_mid_alive_radiant if team == _TEAM_RADIANT else bucket.t1_mid_alive_dire
    )
    structural_deficit = tower_diff < -0.25 or (lost_t1_mid and ward_diff < -0.20)
    heavy_pressure = pressure_score >= 0.70
    winning_state = bucket.net_worth_advantage >= 3500 or bucket.xp_advantage >= 4500
    losing_state = bucket.net_worth_advantage <= -3500 or bucket.xp_advantage <= -4500

    label: Literal[
        "safe_home_farm",
        "pressured_home_farm",
        "defensive_home_farm",
        "safe_invade",
        "pressure_invade",
        "high_risk_invade",
    ]
    if is_invading:
        if pressure_score >= 0.70 or (
            enemy_aegis_active and (enemy_presence_enemy_half >= 0.35 or losing_state)
        ):
            label = "high_risk_invade"
        elif (
            farm_safety_score >= 0.52
            and pressure_score <= 0.48
            and tower_diff >= -0.05
            and ward_diff >= -0.10
            and not enemy_aegis_active
            and winning_state
        ):
            label = "safe_invade"
        else:
            label = "pressure_invade"
    elif farm_safety_score >= 0.68 and pressure_score <= 0.40 and not losing_state:
        label = "safe_home_farm"
    elif (
        (losing_state and pressure_score >= 0.52)
        or (heavy_pressure and not winning_state)
        or (enemy_aegis_active and pressure_score >= 0.55 and not winning_state)
        or (structural_deficit and pressure_score >= 0.45 and not winning_state)
    ):
        label = "defensive_home_farm"
    else:
        label = "pressured_home_farm"

    drivers: list[str] = []
    if lost_t1_mid:
        drivers.append("lost_t1_mid")
    if enemy_aegis_active:
        drivers.append("enemy_aegis_active")
    if enemy_presence_own_half >= 0.45:
        drivers.append("enemy_presence_high_own_half")
    if enemy_presence_river >= 0.45:
        drivers.append("enemy_presence_high_river")
    if ward_diff < -0.15:
        drivers.append("vision_deficit")
    if tower_diff < -0.15:
        drivers.append("map_control_deficit")
    if is_border:
        drivers.append("border_zone_farm")
    if is_invading:
        drivers.append("invading_enemy_half")
    if expected_value_score >= 0.7:
        drivers.append("high_farm_value")

    return CampVisitContext(
        farm_safety_score=farm_safety_score,
        pressure_score=pressure_score,
        expected_value_score=expected_value_score,
        context_label=label,
        context_drivers=drivers,
    )


def world_in_bounds(x: float, y: float) -> bool:
    """Return True when world coordinates are within calibrated map bounds."""
    return _MAP_XMIN <= x <= _MAP_XMAX and _MAP_YMIN <= y <= _MAP_YMAX
