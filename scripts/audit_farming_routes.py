"""Summarize farming routes across locally synced replays as a regression corpus.

Records factual route counts (segments, points, evidence strength, phase, camp
area, lane roles) per replay, so a change to route reconstruction shows up as a
corpus difference.

Examples:
    uv run python scripts/audit_farming_routes.py tests/fixtures/opendota/8868259993.dem
    uv run python scripts/audit_farming_routes.py tests/fixtures/opendota/*.dem --pretty
    uv run python scripts/audit_farming_routes.py tests/fixtures/opendota/*.dem \
        --check tests/fixtures/opendota/farming_routes_corpus.json
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

import gem
from gem.analysis import build_farming_routes

TICKS_PER_MINUTE = 60 * 30


def _phase(tick: int, game_start_tick: int | None) -> str:
    game_tick = max(tick - (game_start_tick or 0), 0)
    if game_tick < 10 * TICKS_PER_MINUTE:
        return "early"
    if game_tick < 30 * TICKS_PER_MINUTE:
        return "mid"
    return "late"


def summarize_match(match: Any) -> dict[str, Any]:
    """Return deterministic factual farming-route counts for one parsed match."""
    routes = build_farming_routes(match)
    segments = [segment for route in routes for segment in route.segments]
    return {
        "match_id": int(match.match_id),
        "game_start_tick": match.game_start_tick,
        "game_end_tick": match.game_end_tick,
        "route_count": len(routes),
        "segment_count": len(segments),
        "point_count": sum(len(route.points) for route in routes),
        "evidence_strength_counts": dict(
            sorted(Counter(segment.evidence_strength.value for segment in segments).items())
        ),
        "phase_counts": dict(
            sorted(
                Counter(
                    _phase(
                        (segment.start_tick + segment.end_tick) // 2,
                        match.game_start_tick,
                    )
                    for segment in segments
                ).items()
            )
        ),
        "camp_area_counts": dict(
            sorted(Counter(segment.camp_area for segment in segments).items())
        ),
        "lane_role_counts": dict(
            sorted(Counter(str(player.lane_role) for player in match.players).items())
        ),
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("replays", nargs="+", type=Path, help="Local .dem replay paths")
    parser.add_argument("--pretty", action="store_true", help="Indent the JSON output")
    parser.add_argument("--output", type=Path, help="Optional output JSON path")
    parser.add_argument(
        "--check",
        type=Path,
        help="Fail unless generated match summaries equal a committed corpus file",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    summaries = []
    for replay in args.replays:
        if not replay.exists():
            raise SystemExit(f"replay not found: {replay}")
        summaries.append(summarize_match(gem.parse(replay)))
    payload = {"schema_version": 1, "matches": summaries}
    rendered = json.dumps(payload, indent=2 if args.pretty else None, sort_keys=True)
    if args.check is not None:
        expected = json.loads(args.check.read_text(encoding="utf-8"))
        if expected.get("matches") != summaries:
            raise SystemExit(f"farming-route corpus mismatch: {args.check}")
        print(f"farming-route corpus matches {args.check}")
        if args.output is None:
            return 0
    if args.output is not None:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
