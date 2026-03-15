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
    banner = (
        "  ██████╗ ███████╗███╗   ███╗\n"
        " ██╔════╝ ██╔════╝████╗ ████║\n"
        " ██║  ███╗█████╗  ██╔████╔██║\n"
        " ██║   ██║██╔══╝  ██║╚██╔╝██║\n"
        " ╚██████╔╝███████╗██║ ╚═╝ ██║\n"
        "  ╚═════╝ ╚══════╝╚═╝     ╚═╝\n"
        "  Source 2 .dem replay parser · Python · DS/ML ready\n"
    )
    print(banner)

    if len(sys.argv) < 2:
        print("Usage: python -m gem <replay.dem>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    print(f"Parsing {path} ...")

    from gem import parse

    match = parse(path)

    # Derived match-level counts
    hero_kills = sum(1 for e in match.combat_log if e.log_type == "DEATH" and e.target_is_hero)
    total_buybacks = sum(len(pp.buyback_log) for pp in match.players)
    total_runes = sum(len(pp.runes_log) for pp in match.players)

    # Duration from last sample tick (ticks / 30 ≈ seconds)
    all_ticks = [t for pp in match.players for t in pp.times]
    if all_ticks:
        last_tick = max(all_ticks)
        total_secs = int(last_tick / 30)
        duration_str = f"{total_secs // 60}:{total_secs % 60:02d}"
    else:
        duration_str = "?"

    print(
        f"\nSummary: {hero_kills} hero kills  |  "
        f"{len(match.towers)} towers  |  "
        f"{len(match.barracks)} barracks  |  "
        f"{len(match.roshans)} Roshan kill(s)  |  "
        f"{len(match.aegis_events)} aegis event(s)  |  "
        f"{len(match.wards)} wards  |  "
        f"{total_buybacks} buybacks  |  "
        f"{total_runes} runes  |  "
        f"{len(match.chat)} chat msgs  |  "
        f"duration {duration_str}"
    )
    print()

    for pp in match.players:
        if not pp.hero_name:
            continue
        team_str = "Radiant" if pp.team == 2 else "Dire"
        final_gold = pp.gold_t[-1] if pp.gold_t else 0
        final_lh = pp.lh_t[-1] if pp.lh_t else 0
        print(
            f"  [{team_str}] {pp.hero_name:42s}  "
            f"LH={final_lh:4d}  gold={final_gold:5d}  "
            f"purchases={len(pp.purchase_log):3d}  "
            f"runes={len(pp.runes_log)}  "
            f"buys={len(pp.buyback_log)}"
        )


if __name__ == "__main__":
    main()
