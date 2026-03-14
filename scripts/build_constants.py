"""Build bundled constant data files from refs/dotaconstants.

Reads the raw JSON files from refs/dotaconstants/build/ and writes slim,
pre-processed versions into src/gem/data/. Run this script whenever
dotaconstants is updated.

Usage:
    python scripts/build_constants.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_SRC = Path(__file__).parent.parent / "refs" / "dotaconstants" / "build"
_DST = Path(__file__).parent.parent / "src" / "gem" / "data"


def _load(name: str) -> dict | list:
    path = _SRC / name
    if not path.exists():
        print(f"  [skip] {name} not found in refs/dotaconstants/build/")
        return {} if name.endswith(".json") else []
    with open(path) as f:
        return json.load(f)


def build_heroes() -> None:
    """Slim heroes.json: npc_dota_hero_* -> {id, localized_name, primary_attr, roles}."""
    raw: dict = _load("heroes.json")  # type: ignore[assignment]
    out: dict[str, dict] = {}
    for hero in raw.values():
        name: str = hero.get("name", "")
        if not name:
            continue
        out[name.lower()] = {
            "id": hero.get("id"),
            "localized_name": hero.get("localized_name", ""),
            "primary_attr": hero.get("primary_attr", ""),
            "roles": hero.get("roles", []),
        }
    _write("heroes.json", out)
    print(f"  heroes.json: {len(out)} entries")


def build_items() -> None:
    """Slim items.json: internal_key -> {id, dname}."""
    raw: dict = _load("items.json")  # type: ignore[assignment]
    out: dict[str, dict] = {}
    for key, item in raw.items():
        dname = item.get("dname") or ""
        if dname:
            out[key] = {"id": item.get("id"), "dname": dname}
    _write("items.json", out)
    print(f"  items.json: {len(out)} entries")


def build_abilities() -> None:
    """Slim abilities.json: internal_name -> {dname}."""
    raw: dict = _load("abilities.json")  # type: ignore[assignment]
    out: dict[str, str] = {}
    for name, ab in raw.items():
        dname = ab.get("dname") or ""
        if dname:
            out[name] = dname
    _write("abilities.json", out)
    print(f"  abilities.json: {len(out)} entries")


def build_xp_level() -> None:
    """Copy xp_level.json as-is (list of cumulative XP thresholds)."""
    raw = _load("xp_level.json")
    _write("xp_level.json", raw)
    print(f"  xp_level.json: {len(raw)} levels")


def build_permanent_buffs() -> None:
    """permanent_buffs.json: int_str -> internal_item_name (e.g. '1' -> 'moon_shard')."""
    raw: dict = _load("permanent_buffs.json")  # type: ignore[assignment]
    _write("permanent_buffs.json", raw)
    print(f"  permanent_buffs.json: {len(raw)} entries")


def _write(name: str, data: dict | list) -> None:
    _DST.mkdir(parents=True, exist_ok=True)
    out_path = _DST / name
    with open(out_path, "w") as f:
        json.dump(data, f, separators=(",", ":"))


def main() -> None:
    if not _SRC.exists():
        print(f"Error: {_SRC} not found. Clone refs/dotaconstants first.", file=sys.stderr)
        sys.exit(1)

    print(f"Source: {_SRC}")
    print(f"Output: {_DST}")
    print()

    build_heroes()
    build_items()
    build_abilities()
    build_xp_level()
    build_permanent_buffs()

    print("\nDone.")


if __name__ == "__main__":
    main()
