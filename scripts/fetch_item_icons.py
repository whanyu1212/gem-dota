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
import json
import ssl
import sys
import time
import urllib.request
from collections.abc import Sequence
from pathlib import Path

_ITEMS_JSON = Path(__file__).parent.parent / "src" / "gem" / "data" / "items.json"
_OUT_DIR = Path(__file__).parent.parent / "src" / "gem" / "data" / "item_icons"
_CDN = "https://cdn.dota2.com/apps/dota2/images/dota_react/items/{short}.png"


def _short(item_key: str) -> str:
    return item_key.removeprefix("item_")


def _item_shorts(items_path: Path, *, include_recipes: bool = False) -> tuple[str, ...]:
    items: dict = json.loads(items_path.read_text(encoding="utf-8"))
    shorts = []
    for item_key in sorted(items):
        short = _short(item_key)
        if short.startswith("recipe_") and not include_recipes:
            continue
        shorts.append(short)
    return tuple(shorts)


def missing_icon_shorts(
    items_path: Path = _ITEMS_JSON,
    out_dir: Path = _OUT_DIR,
    *,
    include_recipes: bool = False,
) -> tuple[str, ...]:
    return tuple(
        short
        for short in _item_shorts(items_path, include_recipes=include_recipes)
        if not (out_dir / f"{short}.png").exists()
    )


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
    out_dir.mkdir(parents=True, exist_ok=True)

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    ok = failed = skipped = 0
    for short in _item_shorts(items_path, include_recipes=include_recipes):
        out_path = out_dir / f"{short}.png"
        if out_path.exists() and not force:
            skipped += 1
            continue

        url = _CDN.format(short=short)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
                data = resp.read()
            out_path.write_bytes(data)
            print(f"  OK  {short}")
            ok += 1
            time.sleep(0.05)
        except Exception as exc:
            print(f"  FAIL {short}  ({exc})", file=sys.stderr)
            failed += 1

    print(f"\nDone — {ok} downloaded, {skipped} skipped, {failed} failed -> {out_dir}")


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
