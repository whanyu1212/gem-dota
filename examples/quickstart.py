"""Quickstart examples — mirrors docs/guides/01_quickstart.md.

Usage:
    python examples/quickstart.py path/to/replay.dem
"""

import sys

import gem
from gem.constants import hero_display

if len(sys.argv) < 2:
    print("Usage: python examples/quickstart.py <path/to/replay.dem>")
    sys.exit(1)

dem_path = sys.argv[1]
match = gem.parse(dem_path)

# ── KDA for every player ────────────────────────────────────────────────────
print(f"Match duration: {match.duration_minutes:.1f} minutes")
print()

for player in match.players:
    print(
        f"{hero_display(player.hero_name):<25}"
        f"  KDA {player.kills}/{player.deaths}/{player.assists}"
        f"  NW {player.net_worth_t_min[-1] if player.net_worth_t_min else 0:,}"
        f"  LH/DN {player.lh_t_min[-1] if player.lh_t_min else 0}"
        f"/{player.dn_t_min[-1] if player.dn_t_min else 0}"
    )

print()

# ── Draft picks and bans ────────────────────────────────────────────────────
print("Draft:")
for event in match.draft:
    team = "Radiant" if event.team == 2 else "Dire"
    action = "picks" if event.is_pick else "bans"
    print(f"  {team} {action} {hero_display(event.hero_name)}")

print()

# ── Ward count per player ───────────────────────────────────────────────────
print("Wards placed:")
for player in match.players:
    wards = [w for w in match.wards if w.placer == player.hero_name]
    print(f"  {hero_display(player.hero_name)}: {len(wards)} wards placed")
