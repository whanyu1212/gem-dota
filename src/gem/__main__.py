"""CLI entry point: ``python -m gem <replay.dem>``

Parses a replay file and prints a summary of key statistics to stdout.
"""

from __future__ import annotations

import sys


def main() -> None:
    """Parse a replay and print a summary.

    Usage:
        python -m gem <path/to/replay.dem>
    """
    if len(sys.argv) < 2:
        print("Usage: python -m gem <replay.dem>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    print(f"Parsing {path} ...")

    from gem import parse

    match = parse(path)

    print(f"\nMatch ID: {match.match_id}")
    print(f"Towers killed: {len(match.towers)}")
    print(f"Barracks killed: {len(match.barracks)}")
    print(f"Roshan kills: {len(match.roshans)}")
    print(f"Ward placements: {len(match.wards)}")
    print(f"Combat log entries: {len(match.combat_log)}")
    print()

    for pp in match.players:
        if not pp.hero_name:
            continue
        team_str = "Radiant" if pp.team == 2 else "Dire"
        samples = len(pp.times)
        final_gold = pp.gold_t[-1] if pp.gold_t else 0
        final_lh = pp.lh_t[-1] if pp.lh_t else 0
        print(
            f"  [{team_str}] {pp.hero_name:40s}  "
            f"LH={final_lh:4d}  gold={final_gold:5d}  samples={samples}"
        )


if __name__ == "__main__":
    main()
