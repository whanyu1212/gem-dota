"""Fetch league names from the OpenDota API and save to src/gem/data/leagues.json.

Only premium, professional, and amateur tier leagues are kept — excluded and
untiered entries (test/junk leagues) are dropped.

Usage::

    python scripts/fetch_leagues.py
"""

from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

_API = "https://api.opendota.com/api/leagues"
_OUT = Path(__file__).parent.parent / "src" / "gem" / "data" / "leagues.json"
_KEEP_TIERS = {"premium", "professional", "amateur"}


def fetch() -> None:
    print(f"Fetching {_API} ...")
    with urllib.request.urlopen(_API, timeout=30) as resp:
        leagues = json.load(resp)

    mapping = {
        str(league["leagueid"]): league["name"]
        for league in leagues
        if league.get("tier") in _KEEP_TIERS and league.get("name")
    }

    _OUT.parent.mkdir(parents=True, exist_ok=True)
    _OUT.write_text(
        json.dumps(mapping, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
    )
    print(f"Saved {len(mapping)} leagues → {_OUT}  ({_OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    try:
        fetch()
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
