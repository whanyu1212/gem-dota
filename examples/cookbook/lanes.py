"""How did each lane go?

Each hero's lane is the one (top, mid or bottom) it spent the most of the
laning stage in, 0:00 to ``LANE_S``, read from its once-a-second positions on
OpenDota's lane grid. That is not ``ParsedPlayer.lane``: OpenDota's lane takes
the first 10 minutes, when supports have often left to rotate.

For every lane, at ``LANE_S`` and again at ``COMPARE_S``: each side's net
worth, XP, last hits and denies, and its earned gold by source from the gold
ledger. Then what happened in each lane up to ``COMPARE_S``: deaths (by where
the victim was), teleports into it, and heroes from other lanes who stayed at
least ``MIN_VISIT_S``.

    python examples/cookbook/lanes.py replay.dem [more.dem ...]
"""

from __future__ import annotations

import math
import sys
from collections import Counter

import pandas as pd

import gem
from gem.extractors._cells import od_cell_index
from gem.extractors.lane import LANE_BOT, LANE_MID, LANE_TOP, lane_for_cell

LANE_S = 360  # the laning stage: lanes, and the first reading
COMPARE_S = 600  # the second reading, the one people quote
MIN_VISIT_S = 20  # how long a hero from another lane stays to count as a visit
BASE_S = 30  # before this, heroes are walking out of base, not visiting
TP_LAND_S = 8  # a teleport lands within this long of its cast, or was cancelled
TP_MIN_JUMP = 1500  # world units a teleport moves the hero, at least
LANES = {LANE_TOP: "top", LANE_MID: "mid", LANE_BOT: "bot"}
TEAMS = {2: "radiant", 3: "dire"}
LANE_COLUMNS = [
    "match_id", "lane", "reading_s", "side", "heroes", "net_worth", "xp", "last_hits",
    "denies", "lane_creep_gold", "hero_kill_gold", "neutral_gold", "other_gold",
]  # fmt: skip
EVENT_COLUMNS = ["match_id", "time_s", "end_s", "kind", "lane", "hero", "side", "by", "from_lane"]


def lane_at(x: float, y: float) -> str:
    """The lane a world position is on: ``top``, ``mid``, ``bot``, ``jungle`` or ``""``."""
    # OpenDota's own cell rounding (float32, one decimal, then half up), as gem's lane_pos uses.
    lane = lane_for_cell(od_cell_index(x), od_cell_index(y))
    return LANES.get(lane, "jungle") if lane is not None else ""


def _lanes_by_second(match: gem.ParsedMatch, player: gem.ParsedPlayer, until_s: int) -> list[str]:
    """Where the hero was at each game second from 0 up to ``until_s``."""
    clock = match.game_clock
    out = []
    for second in range(until_s):
        tick = clock.tick_at(second) if clock is not None else None
        spot = gem.position_at_tick(player, tick) if tick is not None else None
        out.append(lane_at(*spot) if spot is not None else "")
    return out


def hero_lanes(match: gem.ParsedMatch, until_s: int = LANE_S) -> pd.DataFrame:
    """Return each hero's lane: where it spent the most of 0:00 to ``until_s``.

    Args:
        match: A parsed match.
        until_s: The end of the laning stage, in game seconds.

    Returns:
        One row per hero: ``match_id``, ``hero``, ``side``, ``lane`` and ``share``
        (the part of the stretch it spent there), then the seconds it spent in
        ``top``, ``mid``, ``bot`` and the ``jungle``.
    """
    rows = []
    for player in match.players:
        seconds = Counter(_lanes_by_second(match, player, until_s))
        lane = max(("top", "mid", "bot"), key=lambda name: seconds[name])
        rows.append(
            {
                "match_id": match.match_id,
                "hero": player.hero_name,
                "side": TEAMS.get(player.team),
                "lane": lane if seconds[lane] else "",
                "share": round(seconds[lane] / until_s, 2) if until_s else 0.0,
                **{name: seconds[name] for name in ("top", "mid", "bot", "jungle")},
            }
        )
    return pd.DataFrame(rows)


def lane_table(
    match: gem.ParsedMatch,
    lanes: pd.DataFrame | None = None,
    readings: tuple[int, ...] = (LANE_S, COMPARE_S),
) -> pd.DataFrame:
    """Return each side's numbers in each lane at each reading.

    Net worth, XP (total earned), last hits and denies are summed over the side's
    heroes in the lane. Earned gold is split by the gold ledger's sources: lane
    creeps, hero kills (and assists), neutrals, and the rest (passive income,
    bounty runes, …).

    Args:
        match: A parsed match.
        lanes: ``hero_lanes(match)``, if already built.
        readings: The game seconds to read at; each must be a whole minute.

    Returns:
        One row per lane, reading and side, with ``LANE_COLUMNS``.
    """
    lanes = hero_lanes(match) if lanes is None else lanes
    home = dict(zip(lanes["hero"], lanes["lane"], strict=True))
    rows = []
    for reading in readings:
        for lane in ("top", "mid", "bot"):
            for team, side in TEAMS.items():
                players = [
                    p for p in match.players if p.team == team and home.get(p.hero_name) == lane
                ]
                sums = dict.fromkeys(LANE_COLUMNS[5:], 0)
                for player in players:
                    if reading not in player.game_times_min:
                        continue
                    i = player.game_times_min.index(reading)
                    sums["net_worth"] += player.net_worth_t_min[i]
                    sums["xp"] += player.total_earned_xp_t_min[i]
                    sums["last_hits"] += player.lh_t_min[i]
                    sums["denies"] += player.dn_t_min[i]
                    # A ledger can have a final reading but no per-minute ones.
                    minutes = player.gold_ledger.per_minute if player.gold_ledger else []
                    ledger = minutes[i] if i < len(minutes) else None
                    if ledger is not None:
                        named = (
                            ledger.creep_kill_gold
                            + ledger.hero_kill_gold
                            + ledger.neutral_kill_gold
                        )
                        sums["lane_creep_gold"] += ledger.creep_kill_gold
                        sums["hero_kill_gold"] += ledger.hero_kill_gold
                        sums["neutral_gold"] += ledger.neutral_kill_gold
                        sums["other_gold"] += player.total_earned_gold_t_min[i] - named
                heroes = ", ".join(p.hero_name for p in players)
                row: dict[str, object] = {"match_id": match.match_id, "lane": lane}
                row |= {"reading_s": reading, "side": side, "heroes": heroes}
                rows.append(row | sums)
    return pd.DataFrame(rows, columns=LANE_COLUMNS)


def lane_events(
    match: gem.ParsedMatch, lanes: pd.DataFrame | None = None, until_s: int = COMPARE_S
) -> pd.DataFrame:
    """Return what happened in each lane up to ``until_s``.

    - ``death``: a hero died; ``lane`` is where the victim was, ``by`` the killer
      (a summon's kill counts for its owner) and ``from_lane`` the killer's lane.
    - ``teleport``: a hero's Town Portal Scroll moved it at least
      ``TP_MIN_JUMP`` within ``TP_LAND_S`` game seconds; ``lane`` is where it
      landed.
    - ``visit``: a hero stayed at least ``MIN_VISIT_S`` in a lane that isn't its
      own (``from_lane``), from ``BASE_S`` on; ``end_s`` is when it left.

    Args:
        match: A parsed match.
        lanes: ``hero_lanes(match)``, if already built.
        until_s: The last game second to look at.

    Returns:
        One row per event, in time order, with ``EVENT_COLUMNS``.
    """
    lanes = hero_lanes(match) if lanes is None else lanes
    home = dict(zip(lanes["hero"], lanes["lane"], strict=True))
    clock = match.game_clock
    heroes = {p.hero_name: p for p in match.players}
    rows = []

    def add(time_s: float, kind: str, lane: str, hero: str, **extra: object) -> None:
        side = TEAMS.get(heroes[hero].team) if hero in heroes else None
        rows.append(
            {"match_id": match.match_id, "time_s": round(time_s), "kind": kind, "lane": lane}
            | {"hero": hero, "side": side, "end_s": None, "by": None, "from_lane": None}
            | extra
        )

    if clock is None:
        return pd.DataFrame(columns=EVENT_COLUMNS)
    for entry in match.combat_log:
        time_s = clock.game_time_at(entry.tick)
        if time_s is None or not 0 <= time_s <= until_s:
            continue
        if (
            entry.log_type == "DEATH"
            and entry.target_name in heroes
            and not entry.target_is_illusion
        ):
            spot = gem.position_at_tick(heroes[entry.target_name], entry.tick)
            killer = entry.damage_source_name or entry.attacker_name
            lane = lane_at(*spot) if spot is not None else ""
            add(time_s, "death", lane, entry.target_name, by=killer, from_lane=home.get(killer))
        elif (
            entry.log_type == "ITEM"
            and entry.inflictor_name == "item_tpscroll"
            and entry.attacker_name in heroes
        ):
            player = heroes[entry.attacker_name]
            cast = gem.position_at_tick(player, entry.tick)
            for second in range(1, TP_LAND_S + 1):
                # The game clock, so a pause during the channel doesn't use up the window.
                landed = clock.tick_at(time_s + second)
                spot = gem.position_at_tick(player, landed) if landed is not None else None
                if cast is not None and spot is not None and math.dist(cast, spot) >= TP_MIN_JUMP:
                    add(
                        time_s,
                        "teleport",
                        lane_at(*spot),
                        entry.attacker_name,
                        from_lane=home.get(entry.attacker_name),
                    )
                    break
    for player in match.players:
        own = home.get(player.hero_name)
        where = _lanes_by_second(match, player, until_s) + [""]
        start = 0
        for second in range(1, len(where)):
            if where[second] == where[start]:
                continue
            lane = where[start]
            if (
                lane in ("top", "mid", "bot")
                and lane != own
                and start >= BASE_S
                and second - start >= MIN_VISIT_S
            ):
                add(start, "visit", lane, player.hero_name, end_s=second, from_lane=own)
            start = second
    frame = pd.DataFrame(rows, columns=EVENT_COLUMNS)
    frame["end_s"] = frame["end_s"].astype("Int64")
    return frame.sort_values(["time_s", "kind"], ignore_index=True)


def lane_gaps(table: pd.DataFrame) -> pd.DataFrame:
    """Return each lane's net-worth gap (Radiant minus Dire) at each reading.

    Args:
        table: ``lane_table(...)`` for one match or many.

    Returns:
        One row per match and lane: ``match_id``, ``lane``, then a column per
        reading (``gap_360``, ``gap_600``, …).
    """
    sign = table["side"].map({"radiant": 1, "dire": -1})
    gaps = table.assign(gap=table["net_worth"] * sign)
    wide = gaps.pivot_table(
        index=["match_id", "lane"], columns="reading_s", values="gap", aggfunc="sum"
    )
    wide.columns = [f"gap_{reading}" for reading in wide.columns]
    return wide.reset_index()


def main(paths: list[str]) -> None:
    """Print each replay's lanes, their numbers at both readings, and their events."""
    if len(paths) == 1:
        matches = [gem.parse(paths[0])]
    else:
        matches = [result.match for result in gem.parse_many(paths) if result.match is not None]
    tables = []
    for match in matches:
        lanes = hero_lanes(match)
        table = lane_table(match, lanes)
        tables.append(table)
        print(f"\n{match.match_id}: lanes over 0:00-{LANE_S // 60}:00")
        print(lanes[["hero", "side", "lane", "share"]].to_string(index=False))
        print(table.drop(columns=["match_id"]).to_string(index=False))
        events = lane_events(match, lanes)
        print(events.drop(columns=["match_id"]).to_string(index=False))
    gaps = lane_gaps(pd.concat(tables, ignore_index=True))
    first, second = f"gap_{LANE_S}", f"gap_{COMPARE_S}"
    ahead = gaps[gaps[first] != 0]
    same = ((ahead[first] > 0) == (ahead[second] > 0)).sum()
    print(
        f"\nThe side ahead on net worth at {LANE_S // 60}:00 was still ahead at {COMPARE_S // 60}:00 in {same} of {len(ahead)} lanes."
    )


if __name__ == "__main__":  # parse_many's worker processes re-import this file
    main(sys.argv[1:])
