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

print()

# ── OpenDota-parity outputs (0.4.0) ─────────────────────────────────────────
# gem.parse() now reproduces much of OpenDota's match schema straight from the
# .dem: final inventories, OpenDota-style kill categories, building-status
# bitmasks, the objectives timeline, per-target combat dicts, the purchase
# timeline, and ward logs. A small taste:
print(f"Score: Radiant {match.radiant_score} – {match.dire_score} Dire")
print("Final items + kill breakdown (first 3 players):")
for player in match.players[:3]:
    items = ", ".join(
        name.replace("item_", "") for slot, name in sorted(player.final_items.items()) if slot < 6
    )
    print(
        f"  {hero_display(player.hero_name):<18} lvl {player.level:>2}"
        f"  lane/neutral/ancient kills: {player.lane_kills}/{player.neutral_kills}/{player.ancient_kills}"
        f"  items: {items}"
    )

print("\nFor the full OpenDota-parity showcase (objectives timeline, building")
print("status, combat dicts, purchase/ward logs, with an optional cross-check")
print("against the real OpenDota match API), run:")
print("    python examples/opendota_parity.py")
