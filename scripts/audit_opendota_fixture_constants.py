"""Audit saved OpenDota fixture metadata against bundled item constants.

Usage:
    uv run python scripts/audit_opendota_fixture_constants.py
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).parent.parent
DEFAULT_FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "opendota"
DEFAULT_ITEMS_PATH = REPO_ROOT / "src" / "gem" / "data" / "items.json"

# Present in OpenDota fixture metadata, but not currently exposed by odota/dotaconstants.
DEFAULT_ALLOWED_MISSING_ITEM_KEYS: frozenset[str] = frozenset({"guardian_shell"})

ITEM_KEY_DICT_FIELDS: tuple[str, ...] = ("purchase", "item_uses")
ITEM_KEY_LOG_FIELDS: tuple[str, ...] = ("purchase_log",)
NEUTRAL_HISTORY_ITEM_FIELDS: tuple[str, ...] = ("item_neutral", "item_neutral_enhancement")
ITEM_ID_FIELDS: tuple[str, ...] = (
    "item_0",
    "item_1",
    "item_2",
    "item_3",
    "item_4",
    "item_5",
    "backpack_0",
    "backpack_1",
    "backpack_2",
    "item_neutral",
    "item_neutral2",
)


@dataclass(frozen=True)
class ObservedItemConstants:
    item_keys: frozenset[str]
    item_ids: frozenset[int]


@dataclass(frozen=True)
class AuditReport:
    fixture_count: int
    observed_item_key_count: int
    observed_item_id_count: int
    missing_item_keys: tuple[str, ...]
    allowed_missing_item_keys: tuple[str, ...]
    missing_item_ids: tuple[int, ...]

    @property
    def ok(self) -> bool:
        return not self.missing_item_keys and not self.missing_item_ids


def load_items(path: Path) -> dict[str, dict[str, Any]]:
    """Load bundled item constants from ``src/gem/data/items.json``."""
    return json.loads(path.read_text(encoding="utf-8"))


def find_fixture_paths(fixture_dir: Path) -> list[Path]:
    """Return saved OpenDota metadata snapshots in stable order."""
    return sorted(fixture_dir.glob("*.opendota.json"))


def collect_observed_item_constants(paths: list[Path]) -> ObservedItemConstants:
    """Collect item string keys and numeric inventory IDs from OpenDota snapshots."""
    item_keys: set[str] = set()
    item_ids: set[int] = set()

    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        for player in payload.get("players", []):
            if not isinstance(player, dict):
                continue
            _collect_player_item_keys(player, item_keys)
            _collect_player_item_ids(player, item_ids)

    return ObservedItemConstants(frozenset(item_keys), frozenset(item_ids))


def audit_fixture_constants(
    fixture_paths: list[Path],
    items: dict[str, dict[str, Any]],
    *,
    allowed_missing_item_keys: frozenset[str] = frozenset(),
) -> AuditReport:
    """Compare observed OpenDota item constants against bundled item metadata."""
    observed = collect_observed_item_constants(fixture_paths)
    item_ids = _known_item_ids(items)

    known_keys = set(items)
    missing_keys = observed.item_keys - known_keys
    allowed_keys = missing_keys & allowed_missing_item_keys
    unexpected_missing_keys = missing_keys - allowed_missing_item_keys
    missing_ids = observed.item_ids - item_ids

    return AuditReport(
        fixture_count=len(fixture_paths),
        observed_item_key_count=len(observed.item_keys),
        observed_item_id_count=len(observed.item_ids),
        missing_item_keys=tuple(sorted(unexpected_missing_keys)),
        allowed_missing_item_keys=tuple(sorted(allowed_keys)),
        missing_item_ids=tuple(sorted(missing_ids)),
    )


def _collect_player_item_keys(player: dict[str, Any], item_keys: set[str]) -> None:
    for field in ITEM_KEY_DICT_FIELDS:
        value = player.get(field)
        if isinstance(value, dict):
            item_keys.update(str(key) for key in value if key)

    for field in ITEM_KEY_LOG_FIELDS:
        value = player.get(field)
        if isinstance(value, list):
            for entry in value:
                if isinstance(entry, dict) and isinstance(entry.get("key"), str):
                    item_keys.add(entry["key"])

    value = player.get("neutral_item_history")
    if isinstance(value, list):
        for entry in value:
            if not isinstance(entry, dict):
                continue
            for field in NEUTRAL_HISTORY_ITEM_FIELDS:
                item_key = entry.get(field)
                if isinstance(item_key, str) and item_key:
                    item_keys.add(item_key)


def _collect_player_item_ids(player: dict[str, Any], item_ids: set[int]) -> None:
    for field in ITEM_ID_FIELDS:
        value = player.get(field)
        if isinstance(value, int) and value > 0:
            item_ids.add(value)


def _known_item_ids(items: dict[str, dict[str, Any]]) -> set[int]:
    ids: set[int] = set()
    for item in items.values():
        item_id = item.get("id")
        if isinstance(item_id, int):
            ids.add(item_id)
    return ids


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit saved OpenDota fixture metadata against bundled item constants."
    )
    parser.add_argument(
        "--fixtures",
        type=Path,
        default=DEFAULT_FIXTURE_DIR,
        help="Directory containing *.opendota.json fixture snapshots.",
    )
    parser.add_argument(
        "--items",
        type=Path,
        default=DEFAULT_ITEMS_PATH,
        help="Bundled items.json to audit against.",
    )
    parser.add_argument(
        "--allow-missing-item-key",
        action="append",
        default=sorted(DEFAULT_ALLOWED_MISSING_ITEM_KEYS),
        help="Known OpenDota item key that is allowed to be absent from bundled constants.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    fixture_paths = find_fixture_paths(args.fixtures)
    report = audit_fixture_constants(
        fixture_paths,
        load_items(args.items),
        allowed_missing_item_keys=frozenset(args.allow_missing_item_key),
    )

    print(f"Audited {report.fixture_count} OpenDota fixture snapshots.")
    print(f"Observed {report.observed_item_key_count} item keys.")
    print(f"Observed {report.observed_item_id_count} item IDs.")
    if report.allowed_missing_item_keys:
        print("Allowed missing item keys:")
        for key in report.allowed_missing_item_keys:
            print(f"  - {key}")
    if report.missing_item_keys:
        print("Missing item keys:", file=sys.stderr)
        for key in report.missing_item_keys:
            print(f"  - {key}", file=sys.stderr)
    if report.missing_item_ids:
        print("Missing item IDs:", file=sys.stderr)
        for item_id in report.missing_item_ids:
            print(f"  - {item_id}", file=sys.stderr)
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
