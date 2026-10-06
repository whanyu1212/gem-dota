"""When did each objective fall, who took it, and did each team convert its edges?

Every building that fell (``match.towers``, ``match.barracks``), every Roshan
(``match.roshans``), every Tormentor (``match.tormentors``) and every wisdom
rune taken: when, for which side, the last hit (or the hero who took the rune),
and the fight that ended in the ``WINDOW_S`` in-game seconds before it. For buildings, who damaged it in the ``DAMAGE_S`` seconds before it
fell: each hero (a summon's damage counts for its owner) and the creeps.

Then each team's edges and what they led to:

- every fight where the team scored more kills (``match.fights``): the first
  building or Roshan within ``WINDOW_S`` after it ended was the team's
  (``converted``), the other side's (``other side first``), or nothing fell;
- every Roshan the team killed: the buildings it took in the ``AEGIS_S`` seconds
  after (the Aegis's five minutes), or none.

A building counts for the side that didn't own it (a deny still loses it).

Wisdom runes spawn at each side's shrine at ``WISDOM_FIRST_S`` (7:00) and every
``WISDOM_EVERY_S`` after. A pickup is a ``PICKUP_RUNE`` entry of the wisdom type,
whose ``value`` is the player's slot; the rune's spot is the half of the map the
hero was on, and its XP the wisdom-rune XP (reason 4) the picker's team got on
that tick. For each spawn, who took each side's rune before the next one: its
own side, the other side, or nobody. The replay records no rune entity for them,
so an untaken rune's fate isn't known; on the fixtures no spot was ever taken
twice between two spawns.

    python examples/cookbook/objectives.py replay.dem [more.dem ...]
"""

from __future__ import annotations

import sys
from collections import defaultdict

import pandas as pd

import gem

WINDOW_S = 120  # how long after a fight its edge can turn into an objective
AEGIS_S = 300  # how long after a Roshan the team's buildings count for the Aegis
DAMAGE_S = 90  # how long before a building fell its damage counts
WISDOM_FIRST_S = 420  # the first wisdom runes spawn at 7:00
WISDOM_EVERY_S = 420  # and again every 7 minutes
WISDOM_RUNE = 8  # the wisdom rune's type in PICKUP_RUNE entries
XP_WISDOM = 4  # the combat log's XP reason for a wisdom rune
PICKUP_TICKS = 3  # a pickup's XP lands within this many ticks of it
TEAMS = {2: "radiant", 3: "dire"}
OTHER = {2: 3, 3: 2}
OBJECTIVE_COLUMNS = [
    "match_id", "tick", "time_s", "time", "kind", "name", "for_side", "last_hit", "after_fight", "after_fight_s",
]  # fmt: skip
WISDOM_COLUMNS = [
    "match_id", "spawn_s", "spot", "taken_by", "hero", "tick", "time_s", "after_s", "xp", "outcome",
]  # fmt: skip
EDGE_COLUMNS = [
    "match_id",
    "team",
    "edge",
    "number",
    "tick",
    "time_s",
    "outcome",
    "took",
    "after_s",
]


def objective_table(match: gem.ParsedMatch) -> pd.DataFrame:
    """Return every objective: when, what, for which side, the last hit and the fight before it.

    ``kind`` is ``tower``, ``barracks``, ``roshan`` or ``tormentor``; ``name``
    the unit (``goodguys_tower1_bot``, ``roshan``); ``for_side`` the side it counted
    for. ``after_fight`` is the number of the last fight (``match.fights`` in
    time order, from 1) that ended within ``WINDOW_S`` before it, and
    ``after_fight_s`` how long before.

    Args:
        match: A parsed match.

    Returns:
        A DataFrame with one row per objective, in time order.
    """
    clock = match.game_clock
    if clock is None:
        return pd.DataFrame(columns=OBJECTIVE_COLUMNS)
    team_of = {player.player_id: player.team for player in match.players}
    rows = [(t.tick, "tower", t.tower_name, OTHER.get(t.team), t.killer) for t in match.towers]
    rows += [
        (b.tick, "barracks", b.barracks_name, OTHER.get(b.team), b.killer) for b in match.barracks
    ]
    rows += [(r.tick, "roshan", "roshan", r.killer_team, r.killer) for r in match.roshans]
    rows += [
        # The protocol's team; the chat event's player slot only when it's missing.
        (
            t.tick,
            "tormentor",
            "tormentor",
            t.killer_team if t.killer_team is not None else team_of.get(t.killer_player_id),
            t.killer,
        )
        for t in match.tormentors
    ]
    rows += [
        (w["tick"], "wisdom_rune", f"{w['spot'] or 'unknown'}_wisdom_rune", w["team"], w["hero"])
        for w in wisdom_pickups(match)
    ]
    fight_ends = sorted(
        (clock.game_time_at(fight.end_tick), number)
        for number, fight in enumerate(sorted(match.fights, key=lambda f: f.start_tick), start=1)
    )
    table = []
    for tick, kind, name, team, killer in sorted(rows, key=lambda row: row[0]):
        time_s = clock.game_time_at(tick)
        if time_s is None:
            continue
        before = [
            (end, n) for end, n in fight_ends if end is not None and 0 <= time_s - end <= WINDOW_S
        ]
        end, number = before[-1] if before else (None, None)
        table.append(
            {
                "match_id": match.match_id,
                "tick": tick,
                "time_s": time_s,
                "time": clock.format_tick(tick),
                "kind": kind,
                "name": name.removeprefix("npc_dota_"),
                "for_side": TEAMS.get(team) if team is not None else None,
                "last_hit": killer,
                "after_fight": number,
                "after_fight_s": round(time_s - end) if end is not None else None,
            }
        )
    frame = pd.DataFrame(table, columns=OBJECTIVE_COLUMNS)
    for column in ("after_fight", "after_fight_s"):
        frame[column] = frame[column].astype("Int64")
    return frame


def wisdom_pickups(match: gem.ParsedMatch) -> list[dict]:
    """Return every wisdom rune taken: when, by whom, at which side's spot, and its XP.

    Args:
        match: A parsed match.

    Returns:
        One dict per pickup, in time order: ``tick``, ``hero``, ``team`` (2 or
        3), ``spot`` (``radiant``/``dire``: the half the hero was on, or ``""``)
        and ``xp`` (the wisdom-rune XP the picker's team got on that tick).
    """
    by_slot = {player.player_id: player for player in match.players}
    team_of = {player.hero_name: player.team for player in match.players}
    xp_at: dict[int, list] = defaultdict(list)
    for entry in match.combat_log:
        if entry.log_type == "XP" and entry.xp_reason == XP_WISDOM:
            xp_at[entry.tick].append(entry)
    pickups = []
    for entry in match.combat_log:
        if entry.log_type != "PICKUP_RUNE" or entry.rune_type != WISDOM_RUNE:
            continue
        player = by_slot.get(entry.value)
        if player is None:
            continue
        spot = gem.position_at_tick(player, entry.tick)
        half = gem.region_of(*spot) if spot is not None else None
        # Both teams can take their runes on the same tick: keep the picker's team's XP.
        xp = sum(
            gained.value
            for tick in range(entry.tick - PICKUP_TICKS, entry.tick + PICKUP_TICKS + 1)
            for gained in xp_at.get(tick, [])
            if team_of.get(gained.target_name) == player.team
        )
        pickups.append(
            {
                "tick": entry.tick,
                "hero": player.hero_name,
                "team": player.team,
                "spot": {"radiant_half": "radiant", "dire_half": "dire"}.get(half or "", ""),
                "xp": xp,
            }
        )
    return sorted(pickups, key=lambda p: p["tick"])


def wisdom_runes(match: gem.ParsedMatch) -> pd.DataFrame:
    """Return who took each side's wisdom rune at each spawn.

    For every spawn up to the end of the game and each side's spot: the side
    and hero that took it before the next spawn, how long after the spawn, and
    its XP. ``outcome`` is ``own side``, ``other side``, ``not taken`` (before
    the next spawn) or ``game ended`` (before the next spawn came).

    Args:
        match: A parsed match.

    Returns:
        One row per spawn and spot, with ``WISDOM_COLUMNS``.
    """
    clock = match.game_clock
    end_tick = match.post_game_tick or match.game_end_tick
    if clock is None or not end_tick:
        return pd.DataFrame(columns=WISDOM_COLUMNS)
    end_s = clock.game_time_at(end_tick)
    if end_s is None or end_s < WISDOM_FIRST_S:
        return pd.DataFrame(columns=WISDOM_COLUMNS)
    taken: dict[tuple[int, str], dict] = {}
    for found in wisdom_pickups(match):
        time_s = clock.game_time_at(found["tick"])
        if time_s is None or time_s < WISDOM_FIRST_S or not found["spot"]:
            continue
        spawn = WISDOM_FIRST_S + (time_s - WISDOM_FIRST_S) // WISDOM_EVERY_S * WISDOM_EVERY_S
        taken.setdefault((int(spawn), found["spot"]), found | {"time_s": time_s})
    rows = []
    for spawn in range(WISDOM_FIRST_S, int(end_s) + 1, WISDOM_EVERY_S):
        for spot in ("radiant", "dire"):
            pickup = taken.get((spawn, spot))
            side = TEAMS.get(pickup["team"]) if pickup else None
            if pickup is None:
                outcome = "game ended" if spawn + WISDOM_EVERY_S > end_s else "not taken"
            else:
                outcome = "own side" if side == spot else "other side"
            rows.append(
                {
                    "match_id": match.match_id,
                    "spawn_s": spawn,
                    "spot": spot,
                    "taken_by": side,
                    "hero": pickup["hero"] if pickup else None,
                    "tick": pickup["tick"] if pickup else None,
                    "time_s": pickup["time_s"] if pickup else None,
                    "after_s": round(pickup["time_s"] - spawn) if pickup else None,
                    "xp": pickup["xp"] if pickup else None,
                    "outcome": outcome,
                }
            )
    frame = pd.DataFrame(rows, columns=WISDOM_COLUMNS)
    for column in ("tick", "after_s", "xp"):
        frame[column] = frame[column].astype("Int64")
    return frame


def wisdom_summary(runes: pd.DataFrame) -> pd.DataFrame:
    """Count each side's wisdom runes by who took them: the figure's bars."""
    counts = runes.groupby(["spot", "outcome"]).size().unstack("outcome", fill_value=0)
    counts = counts.reindex(
        columns=["own side", "other side", "not taken", "game ended"], fill_value=0
    )
    counts.insert(0, "spawns", counts.sum(axis=1))
    return counts.reset_index()


def building_damage(match: gem.ParsedMatch) -> pd.DataFrame:
    """Return who damaged each building in the ``DAMAGE_S`` seconds before it fell.

    One row per building and attacker: a hero (a summon's damage counts for its
    owner, the combat log's damage source) or ``creeps`` for lane and siege
    creeps and anything else. The two tier-4 towers of a side share a name in
    the combat log, so their damage can't be told apart (``shared`` is True).

    Args:
        match: A parsed match.

    Returns:
        A DataFrame: ``match_id``, ``name``, ``time_s``, ``attacker``, ``damage``, ``shared``.
    """
    clock = match.game_clock
    heroes = {player.hero_name for player in match.players}
    fallen = [(t.tick, t.tower_name) for t in match.towers] + [
        (b.tick, b.barracks_name) for b in match.barracks
    ]

    # In-game seconds, so a pause inside the window doesn't shorten it; raw ticks
    # only for a replay without a game clock.
    def seconds(tick: int) -> float:
        now = clock.game_time_at(tick) if clock is not None else None
        return now if now is not None else tick / 30

    by_name: dict[str, list] = defaultdict(list)
    for entry in match.combat_log:
        if entry.log_type == "DAMAGE" and entry.value:
            by_name[entry.target_name].append(entry)
    rows = []
    for tick, name in fallen:
        totals: dict[str, int] = defaultdict(int)
        fell_s = seconds(tick)
        for entry in by_name.get(name, []):
            if entry.tick <= tick and fell_s - DAMAGE_S <= seconds(entry.tick) <= fell_s:
                source = entry.damage_source_name or entry.attacker_name
                totals[source if source in heroes else "creeps"] += entry.value
        for attacker, damage in totals.items():
            rows.append(
                {
                    "match_id": match.match_id,
                    "name": name.removeprefix("npc_dota_"),
                    "time_s": clock.game_time_at(tick) if clock else None,
                    "attacker": attacker,
                    "damage": damage,
                    "shared": name.endswith("tower4"),
                }
            )
    return pd.DataFrame(
        rows, columns=["match_id", "name", "time_s", "attacker", "damage", "shared"]
    )


def edges(match: gem.ParsedMatch, objectives: pd.DataFrame | None = None) -> pd.DataFrame:
    """Return each team's edges and what each led to.

    A fight edge is a fight where the team scored more kills; its ``outcome`` is
    ``converted`` when the first building or Roshan within ``WINDOW_S`` after the
    fight ended counted for the team, ``other side first`` when it counted for
    the enemy, ``nothing`` when none fell. An Aegis edge is a Roshan the team
    killed; ``converted`` when the team took a building within ``AEGIS_S``.

    Args:
        match: A parsed match.
        objectives: ``objective_table(match)``, if already built.

    Returns:
        One row per edge: ``team``, ``edge`` (``fight``/``aegis``), ``number``
        (the fight's, or Roshan's kill number), ``time_s``, ``outcome``, ``took``
        (what it took: the first objective, or the buildings joined by ``; ``) and
        ``after_s`` (how long after, for the first).
    """
    clock = match.game_clock
    if clock is None:
        return pd.DataFrame(columns=EDGE_COLUMNS)
    objectives = objective_table(match) if objectives is None else objectives
    taken = objectives[objectives["kind"].isin(["tower", "barracks", "roshan"])]
    buildings = objectives[objectives["kind"].isin(["tower", "barracks"])]
    rows = []
    for number, fight in enumerate(sorted(match.fights, key=lambda f: f.start_tick), start=1):
        r, d = fight.radiant_kills, fight.dire_kills
        start_s, end_s = clock.game_time_at(fight.start_tick), clock.game_time_at(fight.end_tick)
        if r == d or start_s is None or end_s is None:
            continue
        team = "radiant" if r > d else "dire"
        after = taken[(taken["time_s"] >= end_s) & (taken["time_s"] <= end_s + WINDOW_S)]
        first = after.iloc[0] if len(after) else None
        outcome = (
            "nothing"
            if first is None
            else "converted"
            if first["for_side"] == team
            else "other side first"
        )
        rows.append(
            {
                "match_id": match.match_id,
                "team": team,
                "edge": "fight",
                "number": number,
                "tick": fight.start_tick,
                "time_s": start_s,
                "outcome": outcome,
                "took": first["name"] if first is not None else None,
                "after_s": round(first["time_s"] - end_s) if first is not None else None,
            }
        )
    for roshan in match.roshans:
        time_s = clock.game_time_at(roshan.tick)
        killer_team = TEAMS.get(roshan.killer_team) if roshan.killer_team is not None else None
        if time_s is None or killer_team is None:
            continue
        mine = buildings[
            (buildings["for_side"] == killer_team)
            & (buildings["time_s"] >= time_s)
            & (buildings["time_s"] <= time_s + AEGIS_S)
        ]
        rows.append(
            {
                "match_id": match.match_id,
                "team": killer_team,
                "edge": "aegis",
                "number": roshan.kill_number,
                "tick": roshan.tick,
                "time_s": time_s,
                "outcome": "converted" if len(mine) else "nothing",
                "took": "; ".join(mine["name"]) if len(mine) else None,
                "after_s": round(mine.iloc[0]["time_s"] - time_s) if len(mine) else None,
            }
        )
    frame = pd.DataFrame(rows, columns=EDGE_COLUMNS).sort_values("time_s", ignore_index=True)
    frame["after_s"] = frame["after_s"].astype("Int64")
    return frame


def conversion_summary(edge_rows: pd.DataFrame) -> pd.DataFrame:
    """Count each team's edges by outcome: the bars in the recipe's figure."""
    counts = edge_rows.groupby(["team", "edge", "outcome"]).size().unstack("outcome", fill_value=0)
    counts = counts.reindex(columns=["converted", "other side first", "nothing"], fill_value=0)
    counts.insert(0, "edges", counts.sum(axis=1))
    return counts.reset_index()


def main(paths: list[str]) -> None:
    """Print each replay's objectives and edges, then each team's conversions."""
    if len(paths) == 1:
        matches = [gem.parse(paths[0])]
    else:
        matches = [result.match for result in gem.parse_many(paths) if result.match is not None]
    objectives = [objective_table(match) for match in matches]
    table = pd.concat(objectives, ignore_index=True)
    if table.empty:
        print("No objectives in these replays.")
        return
    print(table.drop(columns=["tick", "time_s"]).to_string(index=False))
    edge_rows = pd.concat(
        [edges(match, o) for match, o in zip(matches, objectives, strict=True)], ignore_index=True
    )
    print("\nEach team's edges, by what they led to:")
    print(conversion_summary(edge_rows).to_string(index=False))
    runes = pd.concat([wisdom_runes(match) for match in matches], ignore_index=True)
    print("\nEach side's wisdom runes, by who took them:")
    print(wisdom_summary(runes).to_string(index=False))


if __name__ == "__main__":  # parse_many's worker processes re-import this file
    main(sys.argv[1:])
