"""Download hero portrait icons from the Dota 2 CDN.

Icons are saved as PNG files to ``src/gem/data/hero_icons/`` using the short
hero name (e.g. ``axe.png``, ``anti_mage.png``).

CDN URL pattern::

    https://cdn.dota2.com/apps/dota2/images/heroes/{short}_icon.png

where ``{short}`` is derived from the NPC name by stripping ``npc_dota_hero_``.

Usage::

    python scripts/fetch_hero_icons.py           # skip already-downloaded
    python scripts/fetch_hero_icons.py --check   # report missing icons
    python scripts/fetch_hero_icons.py --force   # re-download all
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gem.reports.asset_cache import (  # noqa: E402
    HEROES_JSON as _HEROES_JSON,
    SOURCE_HERO_ICON_DIR as _OUT_DIR,
    download_hero_icons,
    hero_icon_shorts,
    missing_hero_icons,
)


def _short(npc_name: str) -> str:
    return npc_name.removeprefix("npc_dota_hero_")


def _hero_shorts(heroes_path: Path) -> tuple[str, ...]:
    return hero_icon_shorts(heroes_path)


def missing_icon_shorts(
    heroes_path: Path = _HEROES_JSON,
    out_dir: Path = _OUT_DIR,
) -> tuple[str, ...]:
    return missing_hero_icons(heroes_path, out_dir)


def check(heroes_path: Path = _HEROES_JSON, out_dir: Path = _OUT_DIR) -> int:
    missing = missing_icon_shorts(heroes_path, out_dir)
    if not missing:
        print(f"All hero icons present in {out_dir}")
        return 0

    print(f"Missing {len(missing)} hero icon{'s' if len(missing) != 1 else ''} in {out_dir}:")
    for short in missing:
        print(f"  - {short}")
    return 1


def fetch(
    force: bool = False,
    heroes_path: Path = _HEROES_JSON,
    out_dir: Path = _OUT_DIR,
) -> None:
    result = download_hero_icons(
        force=force,
        heroes_path=heroes_path,
        out_dir=out_dir,
        reporter=print,
        error_reporter=lambda message: print(message, file=sys.stderr),
    )
    print(
        f"\nDone — {result.downloaded} downloaded, {result.skipped} skipped, "
        f"{result.failed} failed -> {result.out_dir}"
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Download Dota 2 hero icons.")
    parser.add_argument(
        "--check", action="store_true", help="Report missing icons without downloading"
    )
    parser.add_argument("--force", action="store_true", help="Re-download existing files")
    parser.add_argument("--heroes", type=Path, default=_HEROES_JSON, help="Path to heroes.json")
    parser.add_argument("--out-dir", type=Path, default=_OUT_DIR, help="Icon output directory")
    args = parser.parse_args(argv)

    if args.check:
        return check(args.heroes, args.out_dir)

    fetch(force=args.force, heroes_path=args.heroes, out_dir=args.out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
