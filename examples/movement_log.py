"""Movement log example — print each hero's position samples over time.

Usage::

    python examples/movement_log.py <replay.dem> [--hero <npc_name>] [--interval <minutes>]

Examples::

    # All heroes, full game
    python examples/movement_log.py replay.dem

    # One hero only
    python examples/movement_log.py replay.dem --hero npc_dota_hero_axe

    # First 10 minutes only
    python examples/movement_log.py replay.dem --interval 10
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import gem
from gem.constants import hero_display

_TICKS_PER_SEC = 30


def _fmt_tick(tick: int) -> str:
    secs = tick // _TICKS_PER_SEC
    return f"{secs // 60:02d}:{secs % 60:02d}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Print hero movement log from a replay.")
    parser.add_argument("replay", help="Path to .dem file")
    parser.add_argument("--hero", default=None, help="Filter to one hero NPC name")
    parser.add_argument("--interval", type=int, default=None, help="Only show first N minutes")
    args = parser.parse_args()

    print(f"Parsing {args.replay} ...")
    match = gem.parse(args.replay)
    print(f"Done — {len(match.players)} players\n")

    tick_cutoff = args.interval * 60 * _TICKS_PER_SEC if args.interval else None

    for pp in match.players:
        if not pp.position_log:
            continue
        if args.hero and args.hero.lower() not in pp.hero_name.lower():
            continue

        team = "Radiant" if pp.team == 2 else "Dire"
        name = hero_display(pp.hero_name)
        entries = pp.position_log
        if tick_cutoff:
            entries = [(t, x, y) for t, x, y in entries if t <= tick_cutoff]

        print(f"  [{team}] {name}  ({len(entries)} samples)")
        print(f"  {'Time':>6}  {'X':>10}  {'Y':>10}")
        print(f"  {'-' * 6}  {'-' * 10}  {'-' * 10}")
        for tick, x, y in entries:
            print(f"  {_fmt_tick(tick):>6}  {x:>10.1f}  {y:>10.1f}")
        print()


if __name__ == "__main__":
    main()
