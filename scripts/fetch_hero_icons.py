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
import json
import ssl
import sys
import time
import urllib.request
from collections.abc import Sequence
from pathlib import Path

_HEROES_JSON = Path(__file__).parent.parent / "src" / "gem" / "data" / "heroes.json"
_OUT_DIR = Path(__file__).parent.parent / "src" / "gem" / "data" / "hero_icons"
_CDN_PRIMARY = "https://steamcdn-a.akamaihd.net/apps/dota2/images/heroes/{short}_icon.png"
_CDN_FALLBACK = "https://cdn.dota2.com/apps/dota2/images/heroes/{short}_icon.png"
_CDN_STRATZ = "https://cdn.stratz.com/images/dota2/heroes/{short}_icon.png"
# Some heroes use a different short name on the CDN
_CDN_OVERRIDES: dict[str, str] = {
    "dawnbreaker": "dawnbreaker",
    "kez": "kez",
    "marci": "marci",
    "muerta": "muerta",
    "primal_beast": "primal_beast",
    "ringmaster": "ringmaster",
    "void_spirit": "void_spirit",
}


def _short(npc_name: str) -> str:
    return npc_name.removeprefix("npc_dota_hero_")


def _hero_shorts(heroes_path: Path) -> tuple[str, ...]:
    heroes: dict = json.loads(heroes_path.read_text(encoding="utf-8"))
    return tuple(_short(npc_name) for npc_name in sorted(heroes))


def missing_icon_shorts(
    heroes_path: Path = _HEROES_JSON,
    out_dir: Path = _OUT_DIR,
) -> tuple[str, ...]:
    return tuple(
        short for short in _hero_shorts(heroes_path) if not (out_dir / f"{short}.png").exists()
    )


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
    out_dir.mkdir(parents=True, exist_ok=True)

    # macOS doesn't use system certs by default; disable verification for CDN
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    ok = failed = skipped = 0
    for short in _hero_shorts(heroes_path):
        out_path = out_dir / f"{short}.png"
        if out_path.exists() and not force:
            skipped += 1
            continue

        cdn_short = _CDN_OVERRIDES.get(short, short)
        urls = [
            _CDN_PRIMARY.format(short=cdn_short),
            _CDN_FALLBACK.format(short=cdn_short),
            _CDN_STRATZ.format(short=cdn_short),
        ]
        fetched = False
        for url in urls:
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
                    out_path.write_bytes(resp.read())
                print(f"  OK  {short}")
                ok += 1
                fetched = True
                time.sleep(0.05)
                break
            except Exception:
                continue
        if not fetched:
            print(f"  FAIL {short}", file=sys.stderr)
            failed += 1

    print(f"\nDone — {ok} downloaded, {skipped} skipped, {failed} failed -> {out_dir}")


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
