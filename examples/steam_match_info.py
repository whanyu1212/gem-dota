"""Fetch and display Dota 2 match info from the Steam Web API.

Calls ``IDOTA2Match_570/GetMatchDetails/V1`` and pretty-prints the result
using Rich tables — one table for match-level fields, one for per-player stats.

Usage::

    python examples/steam_match_info.py <match_id> --key <STEAM_API_KEY>

Example::

    python examples/steam_match_info.py 8461735141 --key YOUR_KEY_HERE

You can get a Steam Web API key at https://steamcommunity.com/dev/apikey

Notes
-----
- ``net_worth`` is NOT present in the Steam API response; it is derived from
  entity state in the replay (as gem does via ``m_iNetWorth``).
- The Steam API ``GetMatchDetails`` endpoint became unreliable for matches
  played after Dota patch 7.36 (June 2024). Use OpenDota API as a fallback
  for newer matches.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request as urlreq
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

STEAM_API = "https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V1"


# Player slot → team label
def _team(slot: int) -> str:
    return "Radiant" if slot < 128 else "Dire"


def fetch_match(match_id: int, key: str) -> dict:
    url = f"{STEAM_API}?key={key}&match_id={match_id}"
    req = urlreq.Request(url, headers={"User-Agent": "gem-example/1.0"})
    with urlreq.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read())
    if "result" not in data:
        raise ValueError(f"Unexpected response: {data}")
    result = data["result"]
    if result.get("error"):
        raise ValueError(f"Steam API error: {result['error']}")
    return result


def display(match: dict) -> None:
    from rich import box
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table

    console = Console()

    # -----------------------------------------------------------------------
    # Match-level panel
    # -----------------------------------------------------------------------
    winner = "[green]Radiant[/]" if match.get("radiant_win") else "[red]Dire[/]"
    duration_s = match.get("duration", 0)
    duration = f"{duration_s // 60}m {duration_s % 60}s"

    match_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    match_table.add_column("Field", style="dim")
    match_table.add_column("Value")

    match_fields = [
        ("Match ID", str(match.get("match_id", "—"))),
        ("Winner", winner),
        ("Duration", duration),
        ("Game mode", str(match.get("game_mode", "—"))),
        ("Lobby type", str(match.get("lobby_type", "—"))),
        ("Cluster", str(match.get("cluster", "—"))),
        ("First blood", f"{match.get('first_blood_time', 0)}s"),
        ("Tower status (Radiant)", bin(match.get("tower_status_radiant", 0))),
        ("Tower status (Dire)", bin(match.get("tower_status_dire", 0))),
        ("Barracks (Radiant)", bin(match.get("barracks_status_radiant", 0))),
        ("Barracks (Dire)", bin(match.get("barracks_status_dire", 0))),
    ]
    for label, value in match_fields:
        match_table.add_row(label, value)

    console.print()
    console.print(
        Panel(match_table, title=f"[bold cyan]Match {match.get('match_id')}[/]", expand=False)
    )

    # -----------------------------------------------------------------------
    # Per-player table
    # -----------------------------------------------------------------------
    player_table = Table(box=box.SIMPLE_HEAVY, show_header=True, header_style="bold")
    player_table.add_column("Team", style="dim", justify="left")
    player_table.add_column("Slot", justify="center")
    player_table.add_column("Hero ID", justify="center")
    player_table.add_column("Level", justify="right")
    player_table.add_column("K", justify="right")
    player_table.add_column("D", justify="right")
    player_table.add_column("A", justify="right")
    player_table.add_column("LH", justify="right")
    player_table.add_column("DN", justify="right")
    player_table.add_column("Gold", justify="right")
    player_table.add_column("GPM", justify="right")
    player_table.add_column("XPM", justify="right")
    player_table.add_column("HD", justify="right", style="yellow")
    player_table.add_column("TD", justify="right", style="cyan")
    player_table.add_column("Healing", justify="right", style="green")

    players = sorted(match.get("players", []), key=lambda p: p.get("player_slot", 0))
    for p in players:
        slot = p.get("player_slot", 0)
        team = "[green]Radiant[/]" if slot < 128 else "[red]Dire[/]"
        gpm = round(p.get("gold", 0) / (duration_s / 60), 0) if duration_s else 0
        xpm = round(p.get("xp_per_min", p.get("xp", 0) / (duration_s / 60) if duration_s else 0), 0)
        player_table.add_row(
            team,
            str(slot),
            str(p.get("hero_id", "—")),
            str(p.get("level", "—")),
            str(p.get("kills", "—")),
            str(p.get("deaths", "—")),
            str(p.get("assists", "—")),
            str(p.get("last_hits", "—")),
            str(p.get("denies", "—")),
            str(p.get("gold", "—")),
            str(int(gpm)),
            str(int(xpm)),
            str(p.get("hero_damage", "—")),
            str(p.get("tower_damage", "—")),
            str(p.get("hero_healing", "—")),
        )

    console.print("[bold]Per-player stats[/]")
    console.print(player_table)

    # -----------------------------------------------------------------------
    # Raw JSON (for inspection)
    # -----------------------------------------------------------------------
    console.print("[bold]Raw JSON[/] [dim](truncated player entries)[/]")
    raw = {k: v for k, v in match.items() if k != "players"}
    from rich.pretty import Pretty

    console.print(Pretty(raw, indent_guides=True))


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch Dota 2 match info from Steam API.")
    parser.add_argument("match_id", type=int, help="Steam match ID (64-bit).")
    parser.add_argument("--key", required=True, help="Steam Web API key.")
    parser.add_argument("--json", action="store_true", help="Dump raw JSON instead of tables.")
    args = parser.parse_args()

    try:
        match = fetch_match(args.match_id, args.key)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(match, indent=2))
    else:
        display(match)


if __name__ == "__main__":
    main()
