"""How often did a smoke lead to a kill, and how fast?

For each Smoke of Deceit (``gem.build_smoke_analysis``), finds the first enemy
hero the smoking team killed after the smoke, the first hero it lost, and the
smoke's first fight. Kills come straight from the combat log; a death the hero
came back from (Aegis, Reincarnation) is not a kill.

    python examples/cookbook/smoke_to_kill.py replay.dem [more.dem ...]
"""

from __future__ import annotations

import sys

import pandas as pd

import gem

WINDOW_S = 60  # how long after the smoke a kill still counts
COLUMNS = [
    "match_id", "smoke", "time", "team", "heroes",
    "first_kill_after_s", "first_loss_after_s", "first_fight", "fight_winner",
]  # fmt: skip


def hero_deaths(match: gem.ParsedMatch) -> pd.DataFrame:
    """Return every real hero death: its game time and the killing and dying teams."""
    # Older (Source 1) combat logs have no team fields; fall back to the heroes' teams.
    # A summon's kill names its owner as the damage source.
    hero_team = {player.hero_name: player.team for player in match.players}
    return pd.DataFrame(
        [
            {
                "game_time_s": entry.game_time_s,
                "killer_team": entry.attacker_team
                or hero_team.get(entry.damage_source_name)
                or hero_team.get(entry.attacker_name),
                "victim_team": entry.target_team or hero_team.get(entry.target_name),
            }
            for entry in match.combat_log
            if entry.log_type == "DEATH"
            and entry.target_is_hero
            and not entry.target_is_illusion
            and not entry.will_reincarnate
            and entry.game_time_s is not None
        ],
        columns=["game_time_s", "killer_team", "victim_team"],
    )


def smoke_to_kill(match: gem.ParsedMatch) -> pd.DataFrame:
    """Return one row per smoke: its first kill, first loss and first fight within the window.

    Args:
        match: A parsed match.

    Returns:
        A DataFrame; the ``*_after_s`` columns are ``None`` when nothing happened
        within ``WINDOW_S`` in-game seconds of the smoke.
    """
    clock = match.game_clock
    if clock is None:
        return pd.DataFrame(columns=COLUMNS)
    deaths = hero_deaths(match)
    fight_numbers = {id(fight): n for n, fight in enumerate(match.fights, start=1)}

    def first_after(start_s: float, rows: pd.DataFrame) -> float | None:
        later = rows[(rows["game_time_s"] >= start_s) & (rows["game_time_s"] <= start_s + WINDOW_S)]
        return round(float(later["game_time_s"].min() - start_s)) if len(later) else None

    rows = []
    for number, smoke in enumerate(gem.build_smoke_analysis(match), start=1):
        start_s = clock.game_time_at(smoke.activation_tick)
        if start_s is None or smoke.team not in (2, 3):
            continue
        fight = smoke.first_fight
        rows.append(
            {
                "match_id": match.match_id,
                "smoke": number,
                "time": clock.format_tick(smoke.activation_tick),
                "team": "radiant" if smoke.team == 2 else "dire",
                "heroes": len(smoke.members),
                "first_kill_after_s": first_after(
                    start_s, deaths[deaths["killer_team"] == smoke.team]
                ),
                "first_loss_after_s": first_after(
                    start_s, deaths[deaths["victim_team"] == smoke.team]
                ),
                "first_fight": fight_numbers.get(id(fight)) if fight else None,
                "fight_winner": fight.winner if fight else None,
            }
        )
    table = pd.DataFrame(rows, columns=COLUMNS)
    for column in ("first_kill_after_s", "first_loss_after_s", "first_fight"):
        table[column] = table[column].astype("Int64")
    return table


def main(paths: list[str]) -> None:
    """Print the table for each replay, then how often a smoke led to a kill."""
    if len(paths) == 1:
        matches = [gem.parse(paths[0])]
    else:
        matches = [result.match for result in gem.parse_many(paths) if result.match is not None]
    tables = [table for table in map(smoke_to_kill, matches) if not table.empty]
    if not tables:
        print("Nothing to report for these replays.")
        return
    table = pd.concat(tables, ignore_index=True)
    print(table.to_string(index=False))

    kills = table["first_kill_after_s"].dropna()
    print(
        f"\n{len(kills)} of {len(table)} smokes got a kill within {WINDOW_S} s "
        f"(median {kills.median():.0f} s); "
        f"{table['first_loss_after_s'].notna().sum()} lost a hero within {WINDOW_S} s."
    )


if __name__ == "__main__":  # parse_many's worker processes re-import this file
    main(sys.argv[1:])
