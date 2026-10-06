"""What moved the gold and XP lead?

The gold lead is Radiant's total earned gold minus Dire's
(``m_iTotalEarnedGold``, as OpenDota's ``radiant_gold_adv`` reads it). The game
also keeps each player's earned gold by source: the gold ledger
(``ParsedPlayer.gold_ledger``, read once a game minute and at the end of the
game). Each reading's sources add up to the player's total earned gold, so the
lead splits into its sources exactly. Gold a source the replay has no field for
(seen once, on a newer patch) is ``unlisted``, the rest of the total.

The XP lead (``m_iTotalEarnedXP``) splits the same way, from the combat log's XP
entries and their reason: hero kills, creeps, Roshan, wisdom runes. The combat
log doesn't say which creep gave the XP, so the recipe looks at what died on
that tick: lane creeps, neutral creeps, or other units (summons, wards). When
more than one kind died, or none did, the XP is ``unclear_creeps``.

Neither lead counts gold or XP lost: gold lost on death and gold spent are not
part of earned gold.

    python examples/cookbook/lead.py replay.dem [more.dem ...]
"""

from __future__ import annotations

import bisect
import sys
from collections import defaultdict

import pandas as pd

import gem

#: Each gold column and the ledger fields it adds up.
GOLD_SOURCES = {
    "hero_kills": ("hero_kill_gold",),
    "lane_creeps": ("creep_kill_gold",),
    "neutral_creeps": ("neutral_kill_gold",),
    "buildings": ("building_gold",),
    "roshan": ("roshan_gold",),
    "bounty_runes": ("bounty_gold",),
    "passive_income": ("income_gold",),
    "other": (
        "ward_kill_gold",
        "courier_gold",
        "ability_gold",
        "comeback_gold",
        "creep_deny_gold",
        "other_gold",
    ),
}
XP_SOURCES = [
    "hero_kills",
    "lane_creeps",
    "neutral_creeps",
    "other_units",
    "unclear_creeps",
    "roshan",
    "wisdom_runes",
    "other",
]
TEAMS = {2: "radiant", 3: "dire"}
LANE_PREFIXES = (
    "npc_dota_creep_goodguys",
    "npc_dota_creep_badguys",
    "npc_dota_goodguys_siege",
    "npc_dota_badguys_siege",
)
READING_COLUMNS = ["match_id", "player_id", "hero", "team", "tick", "time_s"]


def _readings(match: gem.ParsedMatch) -> list[tuple[int, float]]:
    """Each reading's tick and game seconds: every minute, then the end of the game."""
    ledgers = [(p, p.gold_ledger) for p in match.players if p.gold_ledger is not None]
    if not ledgers or len(ledgers) != len(match.players):
        return []
    count = min(min(len(ledger.per_minute), len(p.times_min)) for p, ledger in ledgers)
    first, ledger = ledgers[0]
    readings = [(first.times_min[i], float(ledger.per_minute[i].game_time_s)) for i in range(count)]
    finals = [ledger.final for _, ledger in ledgers]
    clock = match.game_clock
    if finals[0] is not None and all(finals) and clock is not None:
        tick = finals[0].tick
        time_s = clock.game_time_at(tick)
        if time_s is not None and (not readings or tick > readings[-1][0]):
            readings.append((tick, round(time_s, 1)))
    return readings


def _total_at(times: list[int], totals: list[int], tick: int) -> int:
    """A dense series' value at the last sample on or before ``tick``."""
    i = bisect.bisect_right(times[: len(totals)], tick) - 1
    return totals[i] if i >= 0 else 0


def gold_sources(match: gem.ParsedMatch) -> pd.DataFrame:
    """Return each player's earned gold by source at every reading.

    One row per player and reading: every game minute (``gold_ledger.per_minute``)
    and the end of the game (``gold_ledger.final``). The source columns
    (``GOLD_SOURCES``) are running totals from the ledger; ``total`` is the
    player's total earned gold and ``unlisted`` the part of it no source covers.

    Args:
        match: A parsed match.

    Returns:
        A DataFrame: ``READING_COLUMNS``, then each source, ``unlisted``, ``total``.
    """
    columns = READING_COLUMNS + [*GOLD_SOURCES, "unlisted", "total"]
    readings = _readings(match)
    rows = []
    for player in match.players:
        ledger = player.gold_ledger
        if ledger is None:
            continue
        for i, (tick, time_s) in enumerate(readings):
            minute = i < len(ledger.per_minute) and ledger.per_minute[i].tick == tick
            snapshot = ledger.per_minute[i] if minute else ledger.final
            total = (
                player.total_earned_gold_t_min[i]
                if minute and i < len(player.total_earned_gold_t_min)
                else _total_at(player.times, player.total_earned_gold_t, tick)
            )
            row = {
                name: sum(getattr(snapshot, f) for f in fields)
                for name, fields in GOLD_SOURCES.items()
            }
            row["unlisted"] = total - sum(row.values())
            row["total"] = total
            rows.append(_reading_row(match, player, tick, time_s) | row)
    return pd.DataFrame(rows, columns=columns)


def _unit_kind(name: str) -> str:
    if name.startswith("npc_dota_neutral_"):
        return "neutral_creeps"
    if name.startswith(LANE_PREFIXES):
        return "lane_creeps"
    return "other_units"


def _xp_source(reason: int, died: set[str]) -> str:
    """An XP entry's source, from its reason and the kinds of unit that died on its tick."""
    match reason:
        case 1:
            return "hero_kills"
        case 3:
            return "roshan"
        case 4:
            return "wisdom_runes"
        case 2:
            return next(iter(died)) if len(died) == 1 else "unclear_creeps"
    return "other"


def xp_sources(match: gem.ParsedMatch) -> pd.DataFrame:
    """Return each player's XP by source at every reading.

    The readings are ``gold_sources``'s. A source is the running total of the
    player's combat-log XP entries before the reading's tick; creep XP is split
    by the units that died on its tick (``lane_creeps``, ``neutral_creeps``,
    ``other_units``, or ``unclear_creeps`` when more than one kind or none did).
    ``total`` is the player's total earned XP and ``unlisted`` the part of it no
    entry covers.

    Args:
        match: A parsed match.

    Returns:
        A DataFrame: ``READING_COLUMNS``, then each of ``XP_SOURCES``, ``unlisted``, ``total``.
    """
    columns = READING_COLUMNS + [*XP_SOURCES, "unlisted", "total"]
    readings = _readings(match)
    died: dict[int, set[str]] = defaultdict(set)
    for e in match.combat_log:
        if (
            e.log_type == "DEATH"
            and not e.target_is_hero
            and not e.target_name.startswith("npc_dota_hero")
        ):
            died[e.tick].add(_unit_kind(e.target_name))
    entries: dict[str, list[tuple[int, str, int]]] = defaultdict(list)
    for e in match.combat_log:
        if e.log_type == "XP":
            source = _xp_source(e.xp_reason, died.get(e.tick, set()))
            entries[e.target_name].append((e.tick, source, e.value))
    rows = []
    for player in match.players:
        if player.gold_ledger is None:
            continue
        mine = sorted(entries.get(player.hero_name, []))
        ticks = [tick for tick, _, _ in mine]
        for i, (tick, time_s) in enumerate(readings):
            row = dict.fromkeys(XP_SOURCES, 0)
            for _, source, value in mine[: bisect.bisect_left(ticks, tick)]:
                row[source] += value
            minute = i < len(player.times_min) and player.times_min[i] == tick
            total = (
                player.total_earned_xp_t_min[i]
                if minute and i < len(player.total_earned_xp_t_min)
                else _total_at(player.times, player.total_earned_xp_t, tick)
            )
            row["unlisted"] = total - sum(row.values())
            row["total"] = total
            rows.append(_reading_row(match, player, tick, time_s) | row)
    return pd.DataFrame(rows, columns=columns)


def _reading_row(
    match: gem.ParsedMatch, player: gem.ParsedPlayer, tick: int, time_s: float
) -> dict:
    return {
        "match_id": match.match_id,
        "player_id": player.player_id,
        "hero": player.hero_name,
        "team": TEAMS.get(player.team),
        "tick": tick,
        "time_s": time_s,
    }


def lead_by_source(sources: pd.DataFrame) -> pd.DataFrame:
    """Return the lead at every reading, and how much of it each source makes up.

    Each column is Radiant's sum minus Dire's, so the sources add up to
    ``lead`` exactly (``total`` is renamed ``lead``).

    Args:
        sources: ``gold_sources(match)`` or ``xp_sources(match)``.

    Returns:
        One row per reading: ``match_id``, ``tick``, ``time_s``, each source, ``lead``.
    """
    values = [c for c in sources.columns if c not in READING_COLUMNS]
    sign = sources["team"].map({"radiant": 1, "dire": -1}).fillna(0).astype(int)
    signed = sources[values].mul(sign, axis=0)
    signed[["match_id", "tick", "time_s"]] = sources[["match_id", "tick", "time_s"]]
    lead = signed.groupby(["match_id", "tick", "time_s"], as_index=False)[values].sum()
    return lead.rename(columns={"total": "lead"})


def what_moved(
    lead: pd.DataFrame, start_s: float | None = None, end_s: float | None = None
) -> pd.Series:
    """Return how much each source moved the lead between two readings.

    Positive is toward Radiant. ``lead`` is the change in the lead; the sources
    add up to it.

    Args:
        lead: ``lead_by_source(...)`` for one match.
        start_s: The first reading at or after this game second (default: the first).
        end_s: The last reading at or before this game second (default: the last).

    Returns:
        A Series indexed by source, then ``lead``.
    """
    rows = lead.sort_values("time_s")
    if start_s is not None:
        rows = rows[rows["time_s"] >= start_s]
    if end_s is not None:
        rows = rows[rows["time_s"] <= end_s]
    values = [c for c in lead.columns if c not in ("match_id", "tick", "time_s")]
    if rows.empty:
        return pd.Series(0, index=values)
    return rows.iloc[-1][values] - rows.iloc[0][values]


def lead_changes(lead: pd.DataFrame) -> pd.DataFrame:
    """Return the readings where the lead changed hands.

    A level reading (a lead of 0) doesn't change hands: the lead changes hands
    when it comes out on the other side of 0 from the last reading that wasn't.

    Args:
        lead: ``lead_by_source(...)`` for one match.

    Returns:
        ``match_id``, ``tick``, ``time_s``, ``lead`` and ``ahead`` (``radiant``/``dire``).
    """
    rows, side = [], 0
    for row in lead.sort_values("time_s").itertuples(index=False):
        now = (row.lead > 0) - (row.lead < 0)
        if now and side and now != side:
            rows.append(
                {
                    "match_id": row.match_id,
                    "tick": row.tick,
                    "time_s": row.time_s,
                    "lead": row.lead,
                    "ahead": "radiant" if now > 0 else "dire",
                }
            )
        side = now or side
    return pd.DataFrame(rows, columns=["match_id", "tick", "time_s", "lead", "ahead"])


def main(paths: list[str]) -> None:
    """Print what moved each replay's gold and XP lead over the whole match."""
    if len(paths) == 1:
        matches = [gem.parse(paths[0])]
    else:
        matches = [result.match for result in gem.parse_many(paths) if result.match is not None]
    for match in matches:
        gold = lead_by_source(gold_sources(match))
        xp = lead_by_source(xp_sources(match))
        if gold.empty:
            print(f"{match.match_id}: no gold ledger in this replay.")
            continue
        clock = match.game_clock
        end = int(gold.iloc[-1]["tick"])
        when = clock.format_tick(end) if clock is not None else f"tick {end}"
        print(f"\n{match.match_id}, at the end of the game ({when}). Radiant's lead:")
        print(f"gold {int(gold['lead'].iloc[-1]):+,}, XP {int(xp['lead'].iloc[-1]):+,}")
        for name, lead in (("Gold", gold), ("XP", xp)):
            moved = what_moved(lead)
            moved = moved[(moved != 0) | (moved.index == "lead")].astype(int)
            print(f"\n{name} lead by source over the match (+ toward Radiant):")
            print(moved.to_string())
        changes = lead_changes(gold)
        if not changes.empty and clock is not None:
            times = ", ".join(
                f"{clock.format_tick(int(c.tick))} {c.ahead}"
                for c in changes.itertuples(index=False)
            )
            print(f"\nThe gold lead changed hands at: {times}")


if __name__ == "__main__":  # parse_many's worker processes re-import this file
    main(sys.argv[1:])
