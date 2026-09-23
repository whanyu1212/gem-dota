"""Audit factual Roshan conversion evidence in local replay fixtures.

The output intentionally records attribution, boundaries, lifecycle provenance,
fight association, and evidence availability.  Tags are included as calibration
observations, not as subjective fixture truth.

Examples:
    uv run python scripts/audit_roshan_conversion_corpus.py \
        tests/fixtures/opendota/8974053011.dem
    uv run python scripts/audit_roshan_conversion_corpus.py \
        --check tests/fixtures/opendota/roshan_conversion_corpus.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import gem
from gem.analysis import build_rosh_conversions

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CORPUS = REPO_ROOT / "tests" / "fixtures" / "opendota" / "roshan_conversion_corpus.json"


def _aegis_event_type(match: gem.ParsedMatch, tick: int | None) -> str | None:
    if tick is None:
        return None
    return next(
        (event.event_type for event in match.aegis_events if event.tick == tick),
        None,
    )


def snapshot_replay(path: Path) -> dict[str, Any]:
    """Parse one replay and return factual Roshan calibration evidence."""
    match = gem.parse(path)
    conversions = build_rosh_conversions(match)
    return {
        "match_id": match.match_id or int(path.stem),
        "game_end_tick": match.game_end_tick,
        "roshan_count": len(conversions),
        "conversions": [
            {
                "rosh_number": conversion.rosh_number,
                "rosh_tick": conversion.rosh_tick,
                "roshan_team": conversion.roshan_team,
                "roshan_team_source": conversion.roshan_team_source.value,
                "conversion_team": conversion.conversion_team,
                "conversion_team_source": conversion.conversion_team_source.value,
                "aegis_event_type": _aegis_event_type(match, conversion.aegis_pickup_tick),
                "aegis_pickup_tick": conversion.aegis_pickup_tick,
                "aegis_fate": conversion.aegis_fate,
                "aegis_fate_source": conversion.aegis_fate_source.value,
                "aegis_fate_inferred": conversion.aegis_fate_inferred,
                "analysis_start_tick": (conversion.differential_profile.window_start_tick),
                "analysis_end_tick": conversion.differential_profile.window_end_tick,
                "next_roshan_boundary_tick": conversion.extended_end_tick,
                "analysis_status": conversion.analysis_status,
                "analysis_status_reasons": conversion.analysis_status_reasons,
                "fight_indexes": [evidence.fight_index for evidence in conversion.fight_evidence],
                "fight_relations": [
                    evidence.relation.value for evidence in conversion.fight_evidence
                ],
                "unattributed_towers": (conversion.differential_profile.unattributed_towers),
                "unattributed_barracks": (conversion.differential_profile.unattributed_barracks),
                "unattributed_tormentors": (
                    conversion.differential_profile.unattributed_tormentors
                ),
                "conversion_tags_observed": conversion.conversion_tags,
                "tag_ruleset": conversion.differential_profile.tag_ruleset,
            }
            for conversion in conversions
        ],
    }


def _assert_subset(expected: Any, actual: Any, path: str = "root") -> None:
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            raise AssertionError(f"{path}: expected object, got {type(actual).__name__}")
        for key, value in expected.items():
            if key not in actual:
                raise AssertionError(f"{path}: missing key {key!r}")
            _assert_subset(value, actual[key], f"{path}.{key}")
        return
    if isinstance(expected, list):
        if not isinstance(actual, list) or len(expected) != len(actual):
            raise AssertionError(
                f"{path}: expected list length {len(expected)}, "
                f"got {len(actual) if isinstance(actual, list) else 'non-list'}"
            )
        for index, value in enumerate(expected):
            _assert_subset(value, actual[index], f"{path}[{index}]")
        return
    if expected != actual:
        raise AssertionError(f"{path}: expected {expected!r}, got {actual!r}")


def _load_corpus(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1 or not isinstance(payload.get("matches"), list):
        raise ValueError(f"invalid Roshan corpus schema: {path}")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("replays", nargs="*", type=Path)
    parser.add_argument(
        "--check",
        nargs="?",
        const=DEFAULT_CORPUS,
        type=Path,
        help="Validate replay output against the committed factual corpus.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.check is not None:
        corpus = _load_corpus(args.check)
        snapshots: list[dict[str, Any]] = []
        for case in corpus["matches"]:
            replay = args.check.parent / case["replay"]
            if not replay.exists():
                raise FileNotFoundError(
                    f"missing {replay}; sync match {case['match_id']} from manifest.json"
                )
            actual = snapshot_replay(replay)
            _assert_subset(case["expected"], actual, str(case["match_id"]))
            by_number = {
                conversion["rosh_number"]: conversion for conversion in actual["conversions"]
            }
            for expected_conversion in case.get("conversion_expectations", []):
                rosh_number = expected_conversion["rosh_number"]
                if rosh_number not in by_number:
                    raise AssertionError(f"{case['match_id']}: missing Roshan #{rosh_number}")
                _assert_subset(
                    expected_conversion,
                    by_number[rosh_number],
                    f"{case['match_id']}.roshan[{rosh_number}]",
                )
            snapshots.append(actual)
        print(json.dumps(snapshots, indent=2))
        return 0

    if not args.replays:
        raise SystemExit("provide replay paths or --check")
    print(json.dumps([snapshot_replay(path) for path in args.replays], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
