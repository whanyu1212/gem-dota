"""Where were the fights, who got the kills, and what fell next?

Every fight in ``match.fights``: when it started and how long it lasted, its
deaths, the kills each side scored, where its deaths were (the centre of them,
as a ``gem.region_of`` region) and each side's net gold in it (gold earned near
the fight, less gold lost on death).
Then what fell next: the first building or Roshan within ``WINDOW_S`` in-game
seconds of the fight's end, and for which side. A building counts for the side
that didn't own it (a deny still loses it); Roshan for the team that killed it.

The summary asks how often the side with more kills in a fight also got the
next building or Roshan.

    python examples/cookbook/fights.py replay.dem [more.dem ...]
"""

from __future__ import annotations

import sys

import pandas as pd

import gem

WINDOW_S = 120  # how long after a fight the next building or Roshan still counts
TEAMS = {2: "radiant", 3: "dire"}
OTHER = {2: 3, 3: 2}
COLUMNS = [
    "match_id", "fight", "start", "start_s", "duration_s", "deaths", "radiant_kills",
    "dire_kills", "more_kills", "region", "radiant_gold", "dire_gold",
    "next", "next_for", "next_after_s",
]  # fmt: skip


def objectives(match: gem.ParsedMatch) -> pd.DataFrame:
    """Return every building that fell and every Roshan kill: when, what, and for which side."""
    clock = match.game_clock
    rows = []
    for tower in match.towers:
        rows.append((tower.tick, tower.tower_name, OTHER.get(tower.team)))
    for barracks in match.barracks:
        rows.append((barracks.tick, barracks.barracks_name, OTHER.get(barracks.team)))
    for roshan in match.roshans:
        rows.append((roshan.tick, "roshan", roshan.killer_team))
    table = pd.DataFrame(
        [
            {
                "time_s": clock.game_time_at(tick) if clock else None,
                "what": what.removeprefix("npc_dota_"),
                "for": TEAMS.get(team) if team is not None else None,
            }
            for tick, what, team in rows
        ],
        columns=["time_s", "what", "for"],
    )
    return table.sort_values("time_s", ignore_index=True)


def fight_table(match: gem.ParsedMatch) -> pd.DataFrame:
    """Return one row per fight: kills each side scored, where, the gold, and what fell next.

    ``more_kills`` is ``radiant``, ``dire`` or ``even``. ``radiant_gold`` and
    ``dire_gold`` are each side's net gold change near the fight
    (``FightPlayer.gold_delta``). ``region`` is ``None``
    when none of the fight's deaths had a position. ``next`` is the first
    building or Roshan within ``WINDOW_S`` in-game seconds after the fight
    ended, ``next_for`` the side it counted for, ``next_after_s`` how long after.

    Args:
        match: A parsed match.

    Returns:
        A DataFrame with one row per fight, in time order.
    """
    clock = match.game_clock
    if clock is None:
        return pd.DataFrame(columns=COLUMNS)
    team_of = {player.player_id: player.team for player in match.players}
    later = objectives(match)
    rows = []
    for number, fight in enumerate(sorted(match.fights, key=lambda f: f.start_tick), start=1):
        start_s = clock.game_time_at(fight.start_tick)
        end_s = clock.game_time_at(fight.end_tick)
        if start_s is None or end_s is None:
            continue
        gold = {2: 0, 3: 0}
        for player in fight.players:
            team = team_of.get(player.player_id)
            if team in gold:
                gold[team] += player.gold_delta
        r, d = fight.radiant_kills, fight.dire_kills
        after = later[(later["time_s"] >= end_s) & (later["time_s"] <= end_s + WINDOW_S)]
        first = after.iloc[0] if len(after) else None
        rows.append(
            {
                "match_id": match.match_id,
                "fight": number,
                "start": clock.format_tick(fight.start_tick),
                "start_s": start_s,
                "duration_s": end_s - start_s,
                "deaths": fight.deaths,
                "radiant_kills": r,
                "dire_kills": d,
                "more_kills": "radiant" if r > d else "dire" if d > r else "even",
                "region": (
                    gem.region_of(fight.centroid_x, fight.centroid_y)
                    if fight.centroid_x is not None and fight.centroid_y is not None
                    else None
                ),
                "radiant_gold": gold[2],
                "dire_gold": gold[3],
                "next": first["what"] if first is not None else None,
                "next_for": first["for"] if first is not None else None,
                "next_after_s": round(first["time_s"] - end_s) if first is not None else None,
            }
        )
    table = pd.DataFrame(rows, columns=COLUMNS)
    table["next_after_s"] = table["next_after_s"].astype("Int64")
    return table


def next_objective_summary(table: pd.DataFrame) -> dict[str, int]:
    """Count the fights one side won on kills, those followed by a building or Roshan, and those it got."""
    decided = table[table["more_kills"] != "even"]
    followed = decided[decided["next"].notna()]
    return {
        "fights": len(table),
        "more_kills": len(decided),
        "followed": len(followed),
        "same_side": int((followed["next_for"] == followed["more_kills"]).sum()),
    }


def main(paths: list[str]) -> None:
    """Print each replay's fights, then how often the side with more kills got what fell next."""
    if len(paths) == 1:
        matches = [gem.parse(paths[0])]
    else:
        matches = [result.match for result in gem.parse_many(paths) if result.match is not None]
    tables = [table for table in map(fight_table, matches) if not table.empty]
    if not tables:
        print("No fights in these replays.")
        return
    table = pd.concat(tables, ignore_index=True)
    shown = ["match_id", "fight", "start", "deaths", "radiant_kills", "dire_kills", "more_kills"]
    print(table[[*shown, "region", "next", "next_for", "next_after_s"]].to_string(index=False))
    n = next_objective_summary(table)
    print(
        f"\n{n['more_kills']} of {n['fights']} fights had a side with more kills; "
        f"{n['followed']} of those had a building fall or Roshan killed within {WINDOW_S} s, "
        f"and the side with more kills got {n['same_side']} of them."
    )


if __name__ == "__main__":  # parse_many's worker processes re-import this file
    main(sys.argv[1:])
