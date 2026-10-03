"""Did the team that killed Roshan win the next fight, and how soon?

Joins three facts gem records: Roshan kills (``match.roshans``), what happened to
the Aegis (``match.aegis_events``) and the fights (``match.fights``). Times use
the pause-aware game clock, so a pause between the kill and the fight is not
counted.

    python examples/cookbook/roshan_next_fight.py replay.dem [more.dem ...]
"""

from __future__ import annotations

import sys

import pandas as pd

import gem

TEAM_NAMES = {2: "radiant", 3: "dire"}
WINDOW_S = 300  # the Aegis lasts five minutes; later fights are not about this Roshan
COLUMNS = [
    "match_id", "roshan", "time", "killed_by", "aegis", "aegis_by",
    "next_fight", "seconds_to_fight", "fight_winner", "killer_team_won",
]  # fmt: skip


def roshan_next_fight(match: gem.ParsedMatch) -> pd.DataFrame:
    """Return one row per Roshan kill with the Aegis outcome and the next fight.

    Args:
        match: A parsed match.

    Returns:
        A DataFrame with the kill's time and team, what happened to the Aegis,
        and the first fight whose first death came within ``WINDOW_S`` in-game
        seconds after the kill (``None`` when there was none).
    """
    clock = match.game_clock
    if clock is None:
        return pd.DataFrame(columns=COLUMNS)
    players = {player.player_id: player for player in match.players}
    # Older (Source 1) replays don't record the killing team; fall back to the killer's.
    hero_team = {player.hero_name: player.team for player in match.players}
    # Fight numbers match the HTML report's Fights tab: the order of match.fights.
    fights = [
        (number, fight, clock.game_time_at(fight.first_death_tick))
        for number, fight in enumerate(match.fights, start=1)
    ]
    fights.sort(key=lambda item: item[1].first_death_tick)
    kills = sorted(match.roshans, key=lambda kill: kill.tick)

    rows = []
    for index, kill in enumerate(kills):
        kill_s = clock.game_time_at(kill.tick)
        if kill_s is None:
            continue
        # The Aegis event for this kill comes after it and before the next one.
        next_kill_tick = kills[index + 1].tick if index + 1 < len(kills) else float("inf")
        aegis = next((e for e in match.aegis_events if kill.tick <= e.tick < next_kill_tick), None)
        # The player who picked up, stole or denied it.
        aegis_player = players.get(aegis.player_id) if aegis else None
        number, fight, fight_s = next(
            (
                (n, f, s)
                for n, f, s in fights
                if f.first_death_tick >= kill.tick and s is not None and s - kill_s <= WINDOW_S
            ),
            (None, None, None),
        )

        killer_team = TEAM_NAMES.get(
            kill.killer_team or hero_team.get(kill.killer_source) or hero_team.get(kill.killer) or 0
        )
        rows.append(
            {
                "match_id": match.match_id,
                "roshan": index + 1,
                "time": clock.format_tick(kill.tick),
                "killed_by": killer_team,
                "aegis": aegis.event_type if aegis else None,
                "aegis_by": (
                    aegis_player.hero_name.removeprefix("npc_dota_hero_") if aegis_player else None
                ),
                "next_fight": number,
                "seconds_to_fight": round(fight_s - kill_s) if fight_s is not None else None,
                "fight_winner": fight.winner if fight else None,
                "killer_team_won": (
                    fight.winner == killer_team
                    if fight and fight.winner in TEAM_NAMES.values()
                    else None
                ),
            }
        )
    table = pd.DataFrame(rows, columns=COLUMNS)
    for column in ("next_fight", "seconds_to_fight"):
        table[column] = table[column].astype("Int64")
    return table


def main(paths: list[str]) -> None:
    """Print the table for each replay, then the rate across all of them."""
    if len(paths) == 1:
        matches = [gem.parse(paths[0])]
    else:
        matches = [result.match for result in gem.parse_many(paths) if result.match is not None]
    tables = [table for table in map(roshan_next_fight, matches) if not table.empty]
    if not tables:
        print("Nothing to report for these replays.")
        return
    table = pd.concat(tables, ignore_index=True)
    print(table.to_string(index=False))

    decided = table["killer_team_won"].dropna()
    print(
        f"\n{table['next_fight'].notna().sum()} of {len(table)} Roshans had a fight within "
        f"{WINDOW_S // 60} minutes (median wait {table['seconds_to_fight'].median():.0f} s); "
        f"the Roshan team won {int(decided.sum())} of the {len(decided)} with a winner."
    )


if __name__ == "__main__":  # parse_many's worker processes re-import this file
    main(sys.argv[1:])
