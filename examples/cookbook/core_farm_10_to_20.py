"""How fast did each core farm from minute 10 to 20, and where?

Uses the per-minute curves (``total_earned_gold_t_min``, ``lh_t_min``), the
combat log's neutral creep deaths, and the sampled positions labelled with
``gem.region_of``. The cores are each team's safe-lane, mid and off-lane player
with the most last hits at 10:00, the rule the HTML report's Farming tab uses.

    python examples/cookbook/core_farm_10_to_20.py replay.dem [more.dem ...]
"""

from __future__ import annotations

import sys
from collections import Counter

import pandas as pd

import gem

ROLES = {1: "carry", 2: "mid", 3: "offlane"}
OWN_HALF = {2: "radiant_half", 3: "dire_half"}
START_MIN, END_MIN = 10, 20
COLUMNS = [
    "match_id", "team", "role", "hero", "gold_per_min", "last_hits",
    "neutral_kills", "own_half", "river", "enemy_half",
]  # fmt: skip


def cores(match: gem.ParsedMatch) -> list[tuple[gem.ParsedPlayer, str]]:
    """Return each team's carry, mid and offlaner: the laner with the most last hits at 10:00."""
    picked = []
    for team in (2, 3):
        for lane_role, role in ROLES.items():
            laners = [p for p in match.players if p.team == team and p.lane_role == lane_role]
            if laners:
                picked.append((max(laners, key=lambda p: p.lane_last_hits), role))
    return picked


def core_farm(match: gem.ParsedMatch) -> pd.DataFrame:
    """Return one row per core: gold, last hits, neutral kills and map time from 10:00 to 20:00.

    Args:
        match: A parsed match.

    Returns:
        A DataFrame, empty when the match is shorter than 20 minutes.
    """
    clock = match.game_clock
    start_s, end_s = START_MIN * 60, END_MIN * 60
    # Pauses stop the game clock, not replay ticks, so convert the window once.
    start_tick = clock.tick_at(start_s) if clock else None
    end_tick = clock.tick_at(end_s) if clock else None
    if start_tick is None or end_tick is None:
        return pd.DataFrame(columns=COLUMNS)
    rows = []
    for player, role in cores(match):
        gold, last_hits = player.total_earned_gold_t_min, player.lh_t_min
        if len(gold) <= END_MIN or len(last_hits) <= END_MIN:
            continue
        hero = player.hero_name
        neutral_kills = sum(
            1
            for entry in match.combat_log
            if entry.log_type == "DEATH"
            and entry.target_name.startswith("npc_dota_neutral")
            and hero in (entry.attacker_name, entry.damage_source_name)
            and entry.game_time_s is not None
            and start_s <= entry.game_time_s < end_s
        )
        regions = Counter(
            gem.region_of(x, y)
            for tick, x, y in player.position_log
            if start_tick <= tick < end_tick
        )
        samples = sum(regions.values()) or 1
        own, enemy = OWN_HALF[player.team], OWN_HALF[5 - player.team]
        rows.append(
            {
                "match_id": match.match_id,
                "team": "radiant" if player.team == 2 else "dire",
                "role": role,
                "hero": hero.removeprefix("npc_dota_hero_"),
                "gold_per_min": (gold[END_MIN] - gold[START_MIN]) / (END_MIN - START_MIN),
                "last_hits": last_hits[END_MIN] - last_hits[START_MIN],
                "neutral_kills": neutral_kills,
                "own_half": regions[own] / samples,
                "river": regions["river"] / samples,
                "enemy_half": regions[enemy] / samples,
            }
        )
    return pd.DataFrame(rows, columns=COLUMNS)


def main(paths: list[str]) -> None:
    """Print the table for each replay, then the averages by role."""
    if len(paths) == 1:
        matches = [gem.parse(paths[0])]
    else:
        matches = [result.match for result in gem.parse_many(paths) if result.match is not None]
    tables = [table for table in map(core_farm, matches) if not table.empty]
    if not tables:
        print("Nothing to report for these replays.")
        return
    table = pd.concat(tables, ignore_index=True)
    with pd.option_context("display.float_format", "{:.2f}".format):
        print(table.to_string(index=False))
        print("\nAverage by role, 10:00 to 20:00:")
        print(
            table.groupby("role")[["gold_per_min", "last_hits", "neutral_kills", "enemy_half"]]
            .mean()
            .round(2)
            .to_string()
        )


if __name__ == "__main__":  # parse_many's worker processes re-import this file
    main(sys.argv[1:])
