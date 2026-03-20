"""Extract all distinct npc_dota_hero_* names from an OpenDota match and map to display names.

Fetches ``/api/matches/{match_id}``, recursively scans every key and string value
in the response for ``npc_dota_hero_`` prefixed names, then resolves each to a
human-readable display name via gem's bundled constants.

Usage::

    uv run python scripts/fetch_hero_npc_names.py <match_id>
    uv run python scripts/fetch_hero_npc_names.py <match_id> --json
"""

from __future__ import annotations

import argparse
import json
import ssl
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

OPENDOTA_API = "https://api.opendota.com/api/matches"

SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.check_hostname = False
SSL_CONTEXT.verify_mode = ssl.CERT_NONE


def fetch_match(match_id: int) -> dict:
    url = f"{OPENDOTA_API}/{match_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "gem/1.0"})
    with urllib.request.urlopen(req, context=SSL_CONTEXT, timeout=20) as resp:
        return json.loads(resp.read())


def scan_npc_heroes(obj: object, found: set[str]) -> None:
    """Recursively scan a JSON object for npc_dota_hero_* names."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(k, str) and k.startswith("npc_dota_hero_"):
                found.add(k)
            scan_npc_heroes(v, found)
    elif isinstance(obj, list):
        for item in obj:
            scan_npc_heroes(item, found)
    elif isinstance(obj, str) and obj.startswith("npc_dota_hero_"):
        found.add(obj)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract distinct npc_dota_hero_* names from an OpenDota match."
    )
    parser.add_argument("match_id", type=int, help="Steam match ID.")
    parser.add_argument("--json", action="store_true", help="Output as JSON.")
    args = parser.parse_args()

    from rich.console import Console
    from rich.table import Table

    console = Console()
    console.print(f"Fetching match [bold cyan]{args.match_id}[/] from OpenDota ...")

    try:
        data = fetch_match(args.match_id)
    except Exception as exc:
        console.print(f"[bold red]ERROR:[/] {exc}")
        sys.exit(1)

    found: set[str] = set()
    scan_npc_heroes(data, found)

    if not found:
        console.print("[yellow]No npc_dota_hero_* names found in response.[/]")
        sys.exit(0)

    from gem.constants import hero_display

    mapping = {npc: hero_display(npc) for npc in sorted(found)}

    if args.json:
        print(json.dumps(mapping, indent=2))
        return

    table = Table(
        title=f"npc_dota_hero_* — Match {args.match_id}",
        show_header=True,
        header_style="bold",
    )
    table.add_column("NPC name", style="dim")
    table.add_column("Display name", style="bold")

    for npc, display in mapping.items():
        table.add_row(npc, display)

    console.print(table)
    console.print(f"  [dim]Total: {len(mapping)}[/]")


if __name__ == "__main__":
    main()
