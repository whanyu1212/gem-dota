"""Audit neutral camp annotations against replay-derived evidence.

The script is intentionally non-mutating: it parses replay files, groups
neutral creep deaths by the current ``camp_zones.json`` annotations, and emits
evidence that can be reviewed before changing fixture data.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter, defaultdict
from collections.abc import Callable
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ZONES_PATH = REPO_ROOT / "src" / "gem" / "data" / "camp_zones.json"
DEFAULT_FIXTURE_REPLAY_DIR = REPO_ROOT / "tests" / "fixtures" / "opendota"
NEUTRAL_PREFIX = "npc_dota_neutral_"
DEFAULT_MAX_POSITION_DELTA_TICKS = 90
DEFAULT_MAX_CAMP_DISTANCE = 1400.0
DEFAULT_GOLD_WINDOW_TICKS = 30

# Dev-facing hints only. We do not use these to rewrite annotations; they
# provide a quick way to spot camps that are obviously no longer the old type.
ANCIENT_NEUTRALS: frozenset[str] = frozenset(
    {
        "npc_dota_neutral_jungle_stalker",
        "npc_dota_neutral_elder_jungle_stalker",
        "npc_dota_neutral_prowler_acolyte",
        "npc_dota_neutral_prowler_shaman",
        "npc_dota_neutral_rock_golem",
        "npc_dota_neutral_granite_golem",
        "npc_dota_neutral_ice_shaman",
        "npc_dota_neutral_frostbitten_golem",
        "npc_dota_neutral_big_thunder_lizard",
        "npc_dota_neutral_small_thunder_lizard",
        "npc_dota_neutral_black_drake",
        "npc_dota_neutral_black_dragon",
        "npc_dota_neutral_ancient_frog",
        "npc_dota_neutral_ancient_frog_mage",
    }
)
FLOODED_NEUTRAL_MARKERS: tuple[str, ...] = (
    "npc_dota_neutral_froglet",
    "npc_dota_neutral_grown_frog",
)


@dataclass(frozen=True)
class CampZone:
    id: int
    type: str
    x: float
    y: float
    shape: str
    rx: float = 0.0
    ry: float = 0.0
    rotation_deg: float = 0.0
    points: tuple[tuple[float, float], ...] = ()


def load_camp_zones(path: Path) -> tuple[CampZone, ...]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    defaults_by_type = payload.get("defaults_by_type", {})
    zones: list[CampZone] = []
    for camp in payload.get("camps", []):
        camp_type = str(camp["type"])
        zone = dict(defaults_by_type.get(camp_type, {}))
        zone.update(camp.get("zone", {}))
        center = camp["center"]
        shape = str(zone.get("shape", "ellipse"))
        points: tuple[tuple[float, float], ...] = ()
        if shape == "polygon":
            points = tuple(_point_tuple(point) for point in zone.get("points", []))
        zones.append(
            CampZone(
                id=int(camp["id"]),
                type=camp_type,
                x=float(center["x"]),
                y=float(center["y"]),
                shape=shape,
                rx=float(zone.get("rx", 0.0)),
                ry=float(zone.get("ry", 0.0)),
                rotation_deg=float(zone.get("rotation_deg", 0.0)),
                points=points,
            )
        )
    return tuple(zones)


def point_in_zone(zone: CampZone, x: float, y: float) -> bool:
    return _point_in_zone(zone, x, y, margin=0.0)


def nearest_position(
    samples: list[tuple[int, float, float]],
    *,
    tick: int,
    max_delta_ticks: int,
) -> tuple[int, float, float] | None:
    if not samples:
        return None
    best = min(samples, key=lambda sample: abs(sample[0] - tick))
    if abs(best[0] - tick) > max_delta_ticks:
        return None
    return best


@dataclass(frozen=True)
class NeutralObservation:
    match_id: int
    tick: int
    attacker_name: str
    neutral_name: str
    hero_position_tick: int
    x: float
    y: float
    camp_id: int
    annotated_type: str
    in_zone: bool
    distance_to_center: float
    nearby_gold: int = 0
    nearby_gold_events: int = 0
    unit_type_hint: str = "unknown"
    neutral_camp_type: int = 0
    neutral_camp_team: int = 0
    position_source: str = "hero_position"


@dataclass(frozen=True)
class MatchAuditReport:
    match_id: int
    observations: tuple[NeutralObservation, ...]
    skipped_neutral_deaths_no_position: int
    skipped_neutral_deaths_unassigned: int


@dataclass(frozen=True)
class CampSummary:
    camp_id: int
    annotated_type: str
    observed_deaths: int
    neutral_counts: dict[str, int]
    unit_type_hint_counts: dict[str, int]
    replay_camp_type_counts: dict[str, int]
    total_nearby_gold: int
    average_nearby_gold: float
    suggested_type: str | None
    status: str
    match_ids: tuple[int, ...]


def collect_neutral_observations(
    match: Any,
    zones: tuple[CampZone, ...],
    *,
    max_position_delta_ticks: int = DEFAULT_MAX_POSITION_DELTA_TICKS,
    max_camp_distance: float = DEFAULT_MAX_CAMP_DISTANCE,
    gold_window_ticks: int = DEFAULT_GOLD_WINDOW_TICKS,
) -> tuple[NeutralObservation, ...]:
    """Collect neutral creep death observations with nearest hero position."""
    return audit_match(
        match,
        zones,
        max_position_delta_ticks=max_position_delta_ticks,
        max_camp_distance=max_camp_distance,
        gold_window_ticks=gold_window_ticks,
    ).observations


def audit_match(
    match: Any,
    zones: tuple[CampZone, ...],
    *,
    max_position_delta_ticks: int = DEFAULT_MAX_POSITION_DELTA_TICKS,
    max_camp_distance: float = DEFAULT_MAX_CAMP_DISTANCE,
    gold_window_ticks: int = DEFAULT_GOLD_WINDOW_TICKS,
) -> MatchAuditReport:
    positions_by_hero = _positions_by_hero(match)
    observations: list[NeutralObservation] = []
    skipped_no_position = 0
    skipped_unassigned = 0
    combat_log = list(getattr(match, "combat_log", []))

    for entry in combat_log:
        if not _is_neutral_death(entry):
            continue
        attacker_name = str(getattr(entry, "attacker_name", ""))
        tick = int(getattr(entry, "tick", 0))
        event_pos = _entry_location(entry)
        position_source = "combat_log"
        if event_pos is None:
            pos = nearest_position(
                positions_by_hero.get(attacker_name, []),
                tick=tick,
                max_delta_ticks=max_position_delta_ticks,
            )
            if pos is None:
                skipped_no_position += 1
                continue
            source_tick, x, y = pos
            position_source = "hero_position"
        else:
            source_tick = tick
            x, y = event_pos

        assigned = _assign_camp(zones, x, y, max_camp_distance=max_camp_distance)
        if assigned is None:
            skipped_unassigned += 1
            continue
        zone, in_zone, distance = assigned
        nearby_gold, nearby_gold_events = _nearby_gold(
            combat_log,
            entry,
            attacker_name=attacker_name,
            gold_window_ticks=gold_window_ticks,
        )
        neutral_name = str(getattr(entry, "target_name", ""))
        observations.append(
            NeutralObservation(
                match_id=int(getattr(match, "match_id", 0)),
                tick=tick,
                attacker_name=attacker_name,
                neutral_name=neutral_name,
                hero_position_tick=source_tick,
                x=x,
                y=y,
                camp_id=zone.id,
                annotated_type=zone.type,
                in_zone=in_zone,
                distance_to_center=distance,
                nearby_gold=nearby_gold,
                nearby_gold_events=nearby_gold_events,
                unit_type_hint=unit_type_hint(neutral_name),
                neutral_camp_type=int(getattr(entry, "neutral_camp_type", 0) or 0),
                neutral_camp_team=int(getattr(entry, "neutral_camp_team", 0) or 0),
                position_source=position_source,
            )
        )

    return MatchAuditReport(
        match_id=int(getattr(match, "match_id", 0)),
        observations=tuple(observations),
        skipped_neutral_deaths_no_position=skipped_no_position,
        skipped_neutral_deaths_unassigned=skipped_unassigned,
    )


def summarize_camps(
    zones: tuple[CampZone, ...],
    observations: tuple[NeutralObservation, ...],
) -> list[CampSummary]:
    by_camp: dict[int, list[NeutralObservation]] = defaultdict(list)
    for obs in observations:
        by_camp[obs.camp_id].append(obs)

    summaries: list[CampSummary] = []
    for zone in zones:
        camp_obs = by_camp.get(zone.id, [])
        if not camp_obs:
            continue
        neutral_counts = Counter(obs.neutral_name for obs in camp_obs)
        hint_counts = Counter(obs.unit_type_hint for obs in camp_obs)
        replay_type_counts = Counter(
            str(obs.neutral_camp_type) for obs in camp_obs if obs.neutral_camp_type
        )
        suggested_type = _suggest_type(zone.type, hint_counts, len(camp_obs))
        status = _summary_status(zone.type, suggested_type)
        total_gold = sum(obs.nearby_gold for obs in camp_obs)
        summaries.append(
            CampSummary(
                camp_id=zone.id,
                annotated_type=zone.type,
                observed_deaths=len(camp_obs),
                neutral_counts=dict(sorted(neutral_counts.items())),
                unit_type_hint_counts=dict(sorted(hint_counts.items())),
                replay_camp_type_counts=dict(sorted(replay_type_counts.items())),
                total_nearby_gold=total_gold,
                average_nearby_gold=round(total_gold / len(camp_obs), 2),
                suggested_type=suggested_type,
                status=status,
                match_ids=tuple(sorted({obs.match_id for obs in camp_obs})),
            )
        )
    return summaries


def unit_type_hint(neutral_name: str) -> str:
    if neutral_name in ANCIENT_NEUTRALS:
        return "ancient"
    if any(neutral_name.startswith(marker) for marker in FLOODED_NEUTRAL_MARKERS):
        return "flooded"
    if neutral_name.startswith(NEUTRAL_PREFIX):
        return "non_ancient"
    return "unknown"


def audit_replays(
    replay_paths: list[Path],
    zones: tuple[CampZone, ...],
    *,
    max_position_delta_ticks: int = DEFAULT_MAX_POSITION_DELTA_TICKS,
    max_camp_distance: float = DEFAULT_MAX_CAMP_DISTANCE,
    gold_window_ticks: int = DEFAULT_GOLD_WINDOW_TICKS,
    progress: Callable[[Path], None] | None = None,
) -> tuple[list[MatchAuditReport], list[CampSummary]]:
    from gem import parse

    reports: list[MatchAuditReport] = []
    all_observations: list[NeutralObservation] = []
    for replay_path in replay_paths:
        if progress is not None:
            progress(replay_path)
        match = parse(replay_path)
        report = audit_match(
            match,
            zones,
            max_position_delta_ticks=max_position_delta_ticks,
            max_camp_distance=max_camp_distance,
            gold_window_ticks=gold_window_ticks,
        )
        reports.append(report)
        all_observations.extend(report.observations)
    return reports, summarize_camps(zones, tuple(all_observations))


def format_text_report(reports: list[MatchAuditReport], summaries: list[CampSummary]) -> str:
    observation_count = sum(len(report.observations) for report in reports)
    skipped_no_position = sum(report.skipped_neutral_deaths_no_position for report in reports)
    skipped_unassigned = sum(report.skipped_neutral_deaths_unassigned for report in reports)
    lines = [
        f"Audited {len(reports)} replay(s).",
        f"Assigned neutral deaths: {observation_count}",
        f"Skipped neutral deaths without nearby hero position: {skipped_no_position}",
        f"Skipped neutral deaths outside camp range: {skipped_unassigned}",
    ]
    if not summaries:
        lines.append("No camp observations found.")
        return "\n".join(lines)

    lines.append("")
    lines.append("Camp evidence:")
    for summary in sorted(summaries, key=lambda item: item.camp_id):
        suggestion = summary.suggested_type or "-"
        lines.append(
            f"- camp {summary.camp_id:02d}: annotated={summary.annotated_type} "
            f"status={summary.status} suggested={suggestion} "
            f"deaths={summary.observed_deaths} avg_gold={summary.average_nearby_gold}"
        )
        if summary.unit_type_hint_counts:
            lines.append(f"  unit_hints: {_format_counts(summary.unit_type_hint_counts)}")
        if summary.replay_camp_type_counts:
            lines.append(f"  replay_camp_types: {_format_counts(summary.replay_camp_type_counts)}")
        lines.append(f"  top_units: {_format_counts(summary.neutral_counts, limit=8)}")
    return "\n".join(lines)


def report_to_jsonable(
    reports: list[MatchAuditReport],
    summaries: list[CampSummary],
) -> dict[str, Any]:
    return {
        "matches": [asdict(report) for report in reports],
        "camp_summaries": [asdict(summary) for summary in summaries],
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "replays",
        nargs="*",
        type=Path,
        help="Replay .dem files to audit. Defaults to tests/fixtures/opendota/*.dem.",
    )
    parser.add_argument(
        "--zones",
        type=Path,
        default=DEFAULT_ZONES_PATH,
        help=f"Camp zones JSON path. Default: {DEFAULT_ZONES_PATH}",
    )
    parser.add_argument(
        "--max-position-delta-ticks",
        type=int,
        default=DEFAULT_MAX_POSITION_DELTA_TICKS,
        help="Maximum tick delta when matching a neutral death to a hero position sample.",
    )
    parser.add_argument(
        "--max-camp-distance",
        type=float,
        default=DEFAULT_MAX_CAMP_DISTANCE,
        help="Maximum distance from camp center for assigning deaths outside an ellipse.",
    )
    parser.add_argument(
        "--gold-window-ticks",
        type=int,
        default=DEFAULT_GOLD_WINDOW_TICKS,
        help="Tick window around a neutral death for summing nearby GOLD combat-log entries.",
    )
    parser.add_argument(
        "--json-out",
        type=Path,
        default=None,
        help="Optional path to write the full JSON audit report.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    replay_paths = args.replays or sorted(DEFAULT_FIXTURE_REPLAY_DIR.glob("*.dem"))
    if not replay_paths:
        print("No replay files provided or found in default fixture directory.", file=sys.stderr)
        return 1

    zones = load_camp_zones(args.zones)
    reports, summaries = audit_replays(
        replay_paths,
        zones,
        max_position_delta_ticks=args.max_position_delta_ticks,
        max_camp_distance=args.max_camp_distance,
        gold_window_ticks=args.gold_window_ticks,
        progress=lambda path: print(f"Parsing {path}", file=sys.stderr),
    )
    print(format_text_report(reports, summaries))
    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(
            json.dumps(report_to_jsonable(reports, summaries), indent=2, sort_keys=True),
            encoding="utf-8",
        )
        print(f"JSON report written to: {args.json_out}")
    return 0


def _point_tuple(point: Any) -> tuple[float, float]:
    if isinstance(point, dict):
        return float(point["x"]), float(point["y"])
    return float(point[0]), float(point[1])


def _point_in_zone(zone: CampZone, x: float, y: float, *, margin: float) -> bool:
    if zone.shape == "ellipse":
        if zone.rx <= 0 or zone.ry <= 0:
            return False
        dx = x - zone.x
        dy = y - zone.y
        angle = math.radians(zone.rotation_deg)
        ca = math.cos(angle)
        sa = math.sin(angle)
        local_x = dx * ca + dy * sa
        local_y = -dx * sa + dy * ca
        rx = zone.rx + margin
        ry = zone.ry + margin
        return (local_x / rx) ** 2 + (local_y / ry) ** 2 <= 1.0

    if zone.shape == "polygon":
        return _point_in_polygon(x, y, zone.points)

    return False


def _point_in_polygon(x: float, y: float, points: tuple[tuple[float, float], ...]) -> bool:
    if len(points) < 3:
        return False
    inside = False
    j = len(points) - 1
    for i, point in enumerate(points):
        xi, yi = point
        xj, yj = points[j]
        intersects = (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi
        if intersects:
            inside = not inside
        j = i
    return inside


def _positions_by_hero(match: Any) -> dict[str, list[tuple[int, float, float]]]:
    positions: dict[str, list[tuple[int, float, float]]] = {}
    for player in getattr(match, "players", []):
        hero_name = getattr(player, "hero_name", "")
        if not hero_name:
            continue
        samples = [
            (int(tick), float(x), float(y)) for tick, x, y in getattr(player, "position_log", [])
        ]
        positions[str(hero_name)] = sorted(samples, key=lambda sample: sample[0])
    return positions


def _is_neutral_death(entry: Any) -> bool:
    return getattr(entry, "log_type", "") == "DEATH" and str(
        getattr(entry, "target_name", "")
    ).startswith(NEUTRAL_PREFIX)


def _entry_location(entry: Any) -> tuple[float, float] | None:
    x = getattr(entry, "location_x", None)
    y = getattr(entry, "location_y", None)
    if x is None or y is None:
        return None
    return float(x), float(y)


def _assign_camp(
    zones: tuple[CampZone, ...],
    x: float,
    y: float,
    *,
    max_camp_distance: float,
) -> tuple[CampZone, bool, float] | None:
    if not zones:
        return None
    containing = [zone for zone in zones if point_in_zone(zone, x, y)]
    candidates = containing or list(zones)
    zone = min(candidates, key=lambda candidate: _distance(candidate.x, candidate.y, x, y))
    distance = _distance(zone.x, zone.y, x, y)
    in_zone = bool(containing)
    if not in_zone and distance > max_camp_distance:
        return None
    return zone, in_zone, distance


def _nearby_gold(
    combat_log: list[Any],
    death_entry: Any,
    *,
    attacker_name: str,
    gold_window_ticks: int,
) -> tuple[int, int]:
    death_tick = int(getattr(death_entry, "tick", 0))
    total = 0
    count = 0
    for entry in combat_log:
        if getattr(entry, "log_type", "") != "GOLD":
            continue
        if abs(int(getattr(entry, "tick", 0)) - death_tick) > gold_window_ticks:
            continue
        if getattr(entry, "attacker_name", "") not in ("", attacker_name) and getattr(
            entry, "target_name", ""
        ) not in ("", attacker_name):
            continue
        value = int(getattr(entry, "value", 0))
        if value <= 0:
            continue
        total += value
        count += 1
    return total, count


def _suggest_type(
    annotated_type: str,
    hint_counts: Counter[str],
    total: int,
) -> str | None:
    if not total:
        return None
    ancient_count = hint_counts.get("ancient", 0)
    flooded_count = hint_counts.get("flooded", 0)
    if ancient_count / total >= 0.6:
        return "ancient"
    if flooded_count / total >= 0.6:
        if annotated_type.startswith("flooded_"):
            return annotated_type
        return "flooded"
    return None


def _summary_status(annotated_type: str, suggested_type: str | None) -> str:
    if suggested_type is None:
        return "review"
    if suggested_type == annotated_type:
        return "match"
    if suggested_type == "flooded" and annotated_type.startswith("flooded_"):
        return "match"
    return "mismatch"


def _distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.hypot(x1 - x2, y1 - y2)


def _format_counts(counts: dict[str, int], *, limit: int | None = None) -> str:
    items = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    if limit is not None:
        items = items[:limit]
    return ", ".join(f"{key}={value}" for key, value in items)


if __name__ == "__main__":
    raise SystemExit(main())
