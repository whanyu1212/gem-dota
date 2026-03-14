"""Download item icons from the Dota 2 CDN.

Icons are saved as PNG files to ``src/gem/data/item_icons/`` using the short
item name (e.g. ``blink.png``, ``ward_observer.png``).

CDN URL pattern::

    https://cdn.dota2.com/apps/dota2/images/dota_react/items/{short}.png

where ``{short}`` is derived from the item key by stripping ``item_``.

Usage::

    python scripts/fetch_item_icons.py           # skip already-downloaded
    python scripts/fetch_item_icons.py --force   # re-download all
"""

from __future__ import annotations

import argparse
import json
import ssl
import sys
import time
import urllib.request
from pathlib import Path

_ITEMS_JSON = Path(__file__).parent.parent / "src" / "gem" / "data" / "items.json"
_OUT_DIR = Path(__file__).parent.parent / "src" / "gem" / "data" / "item_icons"
_CDN = "https://cdn.dota2.com/apps/dota2/images/dota_react/items/{short}.png"


def _short(item_key: str) -> str:
    return item_key.removeprefix("item_")


def fetch(force: bool = False) -> None:
    _OUT_DIR.mkdir(parents=True, exist_ok=True)
    items: dict = json.loads(_ITEMS_JSON.read_text(encoding="utf-8"))

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    ok = failed = skipped = 0
    for item_key in sorted(items):
        short = _short(item_key)
        out_path = _OUT_DIR / f"{short}.png"
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

    print(f"\nDone — {ok} downloaded, {skipped} skipped, {failed} failed → {_OUT_DIR}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download Dota 2 item icons.")
    parser.add_argument("--force", action="store_true", help="Re-download existing files")
    args = parser.parse_args()
    fetch(force=args.force)
