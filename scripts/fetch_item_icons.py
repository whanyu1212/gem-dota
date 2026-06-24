"""Download item icons from the Dota 2 CDN.

Icons are saved as PNG files to ``src/gem/data/item_icons/`` using the short
item name (e.g. ``blink.png``, ``ward_observer.png``).

CDN URL pattern::

    https://cdn.dota2.com/apps/dota2/images/dota_react/items/{short}.png

where ``{short}`` is derived from the item key by stripping ``item_``.

Usage::

    python scripts/fetch_item_icons.py           # skip already-downloaded
    python scripts/fetch_item_icons.py --check   # report missing icons
    python scripts/fetch_item_icons.py --force   # re-download non-recipe icons
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gem.reports.asset_cache import (  # noqa: E402
    ITEMS_JSON as _ITEMS_JSON,
    SOURCE_ITEM_ICON_DIR as _OUT_DIR,
    download_item_icons,
    item_icon_shorts,
    missing_item_icons,
)


def _short(item_key: str) -> str:
    return item_key.removeprefix("item_")


def _item_shorts(items_path: Path, *, include_recipes: bool = False) -> tuple[str, ...]:
    return item_icon_shorts(items_path, include_recipes=include_recipes)


def missing_icon_shorts(
    items_path: Path = _ITEMS_JSON,
    out_dir: Path = _OUT_DIR,
    *,
    include_recipes: bool = False,
) -> tuple[str, ...]:
    return missing_item_icons(items_path, out_dir, include_recipes=include_recipes)


def check(
    items_path: Path = _ITEMS_JSON,
    out_dir: Path = _OUT_DIR,
    *,
    include_recipes: bool = False,
) -> int:
    missing = missing_icon_shorts(items_path, out_dir, include_recipes=include_recipes)
    if not missing:
        print(f"All item icons present in {out_dir}")
        return 0

    print(f"Missing {len(missing)} item icon{'s' if len(missing) != 1 else ''} in {out_dir}:")
    for short in missing:
        print(f"  - {short}")
    return 1


def fetch(
    force: bool = False,
    items_path: Path = _ITEMS_JSON,
    out_dir: Path = _OUT_DIR,
    *,
    include_recipes: bool = False,
) -> None:
    result = download_item_icons(
        force=force,
        items_path=items_path,
        out_dir=out_dir,
        include_recipes=include_recipes,
        reporter=print,
        error_reporter=lambda message: print(message, file=sys.stderr),
    )
    print(
        f"\nDone — {result.downloaded} downloaded, {result.skipped} skipped, "
        f"{result.failed} failed -> {result.out_dir}"
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Download Dota 2 item icons.")
    parser.add_argument(
        "--check", action="store_true", help="Report missing icons without downloading"
    )
    parser.add_argument("--force", action="store_true", help="Re-download existing files")
    parser.add_argument(
        "--include-recipes",
        action="store_true",
        help="Include recipe_* constants when checking or downloading icons",
    )
    parser.add_argument("--items", type=Path, default=_ITEMS_JSON, help="Path to items.json")
    parser.add_argument("--out-dir", type=Path, default=_OUT_DIR, help="Icon output directory")
    args = parser.parse_args(argv)

    if args.check:
        return check(args.items, args.out_dir, include_recipes=args.include_recipes)

    fetch(
        force=args.force,
        items_path=args.items,
        out_dir=args.out_dir,
        include_recipes=args.include_recipes,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
