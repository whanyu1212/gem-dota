"""Who took each rune, and what happened while a power rune lasted?

Every power, bounty and water rune that spawned (``match.runes``): its spot,
who took it and when, or how else it ended (put in a Bottle, denied, not taken,
or still there when the game ended). A rune's spot is the top or bottom river,
or a side's jungle (``gem.region_of``); a bounty taken from the other side's
jungle says so. Several bounties taken together are several runes: untaken
bounties stay on the map and stack.

The match is split into stages: 0:00 to ``LANING_S`` (the lanes recipe's
laning stage, with the water runes), to ``MID_S`` and to the end.

- **The 0:00 bounties** (spawned at the horn): who took each and how many
  seconds after the horn, whose rune it was, the enemy heroes within ``NEAR``
  world units at the pickup, and every hero death up to ``OPENING_S``, from
  before the horn.
- **While a power rune lasted:** each power rune's buff, taken or used from a
  Bottle, runs from its ``modifier_rune_*`` add to its remove in the combat log
  (it ends early when the hero dies). An illusion rune has no buff: its two
  illusions run from their ``modifier_illusion`` adds to their removes, at most
  ``ILLUSION_S``. For each: the taker's kills, the taker's damage to Roshan and
  to buildings (its summons' and illusions' count, as the combat log's damage
  source), and the objectives its team took during it or within ``AFTER_S``
  after. That is what followed, not why.

Times are in-game seconds (pauses excluded). A pickup, or a Bottle's use, keeps
its own ``PICKUP_RUNE`` entry's time (OpenDota's clock for its chat event, at
most half a second from the game clock); a rune bottled, denied or not taken has
no such entry and is timed by the game clock when it left the map.

    python examples/cookbook/runes.py replay.dem [more.dem ...]
"""

from __future__ import annotations

import math
import re
import sys
from collections import defaultdict

import pandas as pd

import gem
from gem.combat.log import CombatLogEntry

LANING_S = 360  # the first stage ends here: the lanes recipe's laning stage
MID_S = 1200  # and the second here
NEAR = 1200  # world units: an enemy hero this close to a 0:00 bounty's pickup is listed
OPENING_S = 90  # the 0:00 bounties' deaths: from before the horn up to 1:30
OPENING_SPAWN_S = 60  # a bounty that spawned before this is a 0:00 bounty
AFTER_S = 30  # objectives this long after a power rune ended still count for it
ILLUSION_S = 75  # an illusion rune's illusions last this long at most
ILLUSION_TICKS = 6  # the illusions appear within this many ticks of the pickup
BUFF_TICKS = 2  # a buff starts within this many ticks of the pickup
PICKUP_TICKS = 2  # a PICKUP_RUNE entry is within this many ticks of its rune's removal
TEAMS = {2: "radiant", 3: "dire"}
OTHER = {2: 3, 3: 2}
STAGES = (("0:00-6:00", 0, LANING_S), ("6:00-20:00", LANING_S, MID_S), ("20:00-end", MID_S, None))
RUNES = {
    0: "double_damage", 1: "haste", 2: "illusion", 3: "invisibility", 4: "regeneration",
    5: "bounty", 6: "arcane", 7: "water", 9: "shield",
}  # fmt: skip
BUFFS = {
    0: "modifier_rune_doubledamage", 1: "modifier_rune_haste", 3: "modifier_rune_invis",
    4: "modifier_rune_regen", 6: "modifier_rune_arcane", 9: "modifier_rune_shield",
}  # fmt: skip
ILLUSION, BOUNTY, WATER = 2, 5, 7
BUILDING = re.compile(r"npc_dota_(goodguys|badguys)_(tower\d|melee_rax|range_rax|fort)")
RUNE_COLUMNS = [
    "match_id", "rune", "kind", "spawn_s", "spot", "outcome", "hero", "side", "whose",
    "time_s", "used_s", "stage", "x", "y",
]  # fmt: skip
OPENING_COLUMNS = [
    "match_id", "spot", "hero", "side", "whose", "after_horn_s", "enemies_near",
]  # fmt: skip
DEATH_COLUMNS = ["match_id", "time_s", "hero", "side", "by"]
WINDOW_COLUMNS = [
    "match_id", "rune", "hero", "side", "from_bottle", "start_s", "end_s", "died", "kills",
    "killed", "roshan_damage", "building_damage", "took", "took_s",
]  # fmt: skip
SUMMARY_COLUMNS = [
    "match_id", "stage", "side", "power", "water", "bounty_own_jungle", "bounty_other_jungle",
    "bounty_river", "denied",
]  # fmt: skip


def spot_of(x: float, y: float) -> str:
    """The rune spot a world position is at: ``top_river``, ``bot_river``, ``radiant_jungle`` or ``dire_jungle``."""
    region = gem.region_of(x, y)
    if region in ("radiant_half", "dire_half"):
        return region.replace("half", "jungle")
    if region == "top_lotus":
        return "top_river"
    if region == "bottom_lotus":
        return "bot_river"
    # The river runs from the top left to the bottom right: above its middle line is the top.
    return "top_river" if y > x else "bot_river"


def stage_of(time_s: float) -> str:
    """The stage a game second falls in (``STAGES``)."""
    return next(name for name, start, end in STAGES if end is None or time_s < end)


def _pickup_times(match: gem.ParsedMatch) -> dict[tuple[int, int, int], float]:
    """Each pickup's own time, keyed by (player slot, rune type, the rune's removal or Bottle-use tick).

    A rune taken or a Bottle used has a ``PICKUP_RUNE`` entry within
    ``PICKUP_TICKS``. Several bounties taken together have several entries, so
    each player's pickups of a type and its entries are paired in tick order.
    """
    entries: dict[tuple[int, int], list[CombatLogEntry]] = defaultdict(list)
    for entry in match.combat_log:
        if entry.log_type == "PICKUP_RUNE" and entry.rune_type in RUNES:
            entries[(entry.value, entry.rune_type)].append(entry)
    pickups: dict[tuple[int, int], list[int]] = defaultdict(list)
    for rune in match.runes:
        if rune.player_id is None:
            continue
        if rune.outcome == "picked_up" and rune.end_tick is not None:
            pickups[(rune.player_id, rune.rune_type)].append(rune.end_tick)
        if rune.used_tick is not None:
            pickups[(rune.player_id, rune.rune_type)].append(rune.used_tick)
    times = {}
    for key, ticks in pickups.items():
        remaining = sorted(entries.get(key, []), key=lambda e: e.tick)
        for tick in sorted(ticks):
            found = next((e for e in remaining if abs(e.tick - tick) <= PICKUP_TICKS), None)
            if found is not None and found.game_time_s is not None:
                remaining.remove(found)
                times[(*key, tick)] = float(found.game_time_s)
    return times


def rune_table(match: gem.ParsedMatch) -> pd.DataFrame:
    """Return every rune that spawned: where, who took it and when, or how else it ended.

    ``kind`` is ``power``, ``bounty`` or ``water``; ``outcome`` is the rune's
    own (``picked_up``, ``bottled``, ``denied``, ``not_taken``, ``still_there``).
    ``whose`` is a bounty's: ``river``, ``own`` (the taker's side's jungle) or
    ``other``. ``time_s`` is when it left the map, ``used_s`` when a bottled
    rune was used, and ``stage`` the stage of ``time_s`` (of the spawn for a
    rune still there).

    Args:
        match: A parsed match.

    Returns:
        One row per rune, in spawn order, with ``RUNE_COLUMNS``.
    """
    clock = match.game_clock
    if clock is None:
        return pd.DataFrame(columns=RUNE_COLUMNS)
    heroes = {p.player_id: p for p in match.players}
    pickup = _pickup_times(match)
    rows = []
    for rune in match.runes:
        if rune.rune_type not in RUNES or rune.x is None or rune.y is None:
            continue
        spawn_s = clock.game_time_at(rune.spawn_tick)
        player = heroes.get(rune.player_id) if rune.player_id is not None else None
        side = TEAMS.get(player.team) if player is not None else None
        time_s = used_s = None
        if rune.end_tick is not None:
            key = (rune.player_id or 0, rune.rune_type, rune.end_tick)
            time_s = pickup.get(key) if rune.outcome == "picked_up" else None
            time_s = time_s if time_s is not None else clock.game_time_at(rune.end_tick)
        if rune.used_tick is not None:
            key = (rune.player_id or 0, rune.rune_type, rune.used_tick)
            used_s = pickup.get(key, clock.game_time_at(rune.used_tick))
        spot = spot_of(rune.x, rune.y)
        whose = None
        if rune.rune_type == BOUNTY and side is not None:
            whose = (
                "river" if spot.endswith("river") else "own" if spot.startswith(side) else "other"
            )
        when = time_s if time_s is not None else spawn_s
        rows.append(
            {
                "match_id": match.match_id,
                "rune": RUNES[rune.rune_type],
                "kind": "bounty"
                if rune.rune_type == BOUNTY
                else "water"
                if rune.rune_type == WATER
                else "power",
                "spawn_s": spawn_s,
                "spot": spot,
                "outcome": rune.outcome,
                "hero": player.hero_name if player is not None else None,
                "side": side,
                "whose": whose,
                "time_s": time_s,
                "used_s": used_s,
                "stage": stage_of(max(when, 0.0)) if when is not None else None,
                "x": rune.x,
                "y": rune.y,
            }
        )
    return pd.DataFrame(rows, columns=RUNE_COLUMNS)


def opening_bounties(match: gem.ParsedMatch, runes: pd.DataFrame | None = None) -> pd.DataFrame:
    """Return the bounties that spawned at the horn: who took each, how soon, and who was near.

    ``after_horn_s`` is the pickup's game second (the horn is 0); ``whose`` is
    ``river``, ``own`` or ``other``; ``enemies_near`` the enemy heroes within
    ``NEAR`` world units of the taker at the pickup (sampled positions, about
    one a second).

    Args:
        match: A parsed match.
        runes: ``rune_table(match)``, if already built.

    Returns:
        One row per 0:00 bounty, in pickup order, with ``OPENING_COLUMNS``.
    """
    runes = rune_table(match) if runes is None else runes
    clock = match.game_clock
    first = runes[
        (runes["rune"] == "bounty")
        & (runes["spawn_s"] < OPENING_SPAWN_S)
        & runes["outcome"].isin(["picked_up", "bottled"])
    ]
    by_hero = {p.hero_name: p for p in match.players}
    rows = []
    for row in first.sort_values("time_s").itertuples(index=False):
        taker = by_hero[row.hero]
        tick = clock.tick_at(row.time_s) if clock is not None else None
        here = gem.position_at_tick(taker, tick) if tick is not None else None
        near = []
        for other in match.players:
            if other.team == taker.team or here is None or tick is None:
                continue
            there = gem.position_at_tick(other, tick)
            if there is not None and math.dist(here, there) <= NEAR:
                near.append(other.hero_name)
        rows.append(
            {
                "match_id": match.match_id,
                "spot": row.spot,
                "hero": row.hero,
                "side": row.side,
                "whose": row.whose,
                "after_horn_s": row.time_s,
                "enemies_near": ", ".join(near),
            }
        )
    return pd.DataFrame(rows, columns=OPENING_COLUMNS)


def opening_deaths(match: gem.ParsedMatch) -> pd.DataFrame:
    """Return every hero death up to ``OPENING_S``, from before the horn.

    ``by`` is the killer (a summon's kill counts for its owner, the combat log's
    damage source).

    Args:
        match: A parsed match.

    Returns:
        One row per death, in time order, with ``DEATH_COLUMNS``.
    """
    clock = match.game_clock
    heroes = {p.hero_name: p for p in match.players}
    rows = []
    for entry in match.combat_log:
        if entry.log_type != "DEATH" or entry.target_name not in heroes or entry.target_is_illusion:
            continue
        time_s = clock.game_time_at(entry.tick) if clock is not None else None
        if time_s is None or time_s > OPENING_S:
            continue
        rows.append(
            {
                "match_id": match.match_id,
                "time_s": time_s,
                "hero": entry.target_name,
                "side": TEAMS.get(heroes[entry.target_name].team),
                "by": entry.damage_source_name or entry.attacker_name,
            }
        )
    return pd.DataFrame(rows, columns=DEATH_COLUMNS)


def _window(
    match: gem.ParsedMatch, modifiers: list, rune_type: int, hero: str, tick: int
) -> tuple[int, int] | None:
    """A power rune's window in replay ticks, from its buff (or its illusions), or ``None``.

    ``modifiers`` are the match's rune-buff and illusion modifier entries.
    """
    clock = match.game_clock
    if rune_type in BUFFS:
        name = BUFFS[rune_type]
        start = next(
            (
                e.tick
                for e in modifiers
                if e.log_type == "MODIFIER_ADD"
                and e.inflictor_name == name
                and e.target_name == hero
                and not e.target_is_illusion
                and abs(e.tick - tick) <= BUFF_TICKS
            ),
            None,
        )
        if start is None:
            return None
        end = next(
            (
                e.tick
                for e in modifiers
                if e.log_type == "MODIFIER_REMOVE"
                and e.inflictor_name == name
                and e.target_name == hero
                and not e.target_is_illusion
                and e.tick >= start
            ),
            match.post_game_tick or match.game_end_tick or start,
        )
        return start, end
    adds = [
        e.tick
        for e in modifiers
        if e.log_type == "MODIFIER_ADD"
        and e.inflictor_name == "modifier_illusion"
        and e.target_name == hero
        and 0 <= e.tick - tick <= ILLUSION_TICKS
    ]
    if not adds or clock is None:
        return None
    start_s = clock.game_time_at(adds[0])
    last = clock.tick_at(start_s + ILLUSION_S) if start_s is not None else None
    removes = sorted(
        e.tick
        for e in modifiers
        if e.log_type == "MODIFIER_REMOVE"
        and e.inflictor_name == "modifier_illusion"
        and e.target_name == hero
        and e.tick >= adds[0]
    )[: len(adds)]
    end = max(removes) if len(removes) == len(adds) else None
    if last is not None and (end is None or end > last):
        end = last
    return (adds[0], end) if end is not None else None


def rune_windows(match: gem.ParsedMatch) -> pd.DataFrame:
    """Return each power rune's window and what happened in it.

    One row per power rune taken or used from a Bottle (``from_bottle``):
    ``start_s`` and ``end_s`` (in-game seconds), whether the taker ``died`` in
    it, the taker's ``kills`` (and who: ``killed``), its damage to Roshan and to
    buildings, and the objectives its team took (``took``, ``took_s`` the
    seconds after ``start_s``) from ``start_s`` to ``end_s + AFTER_S``. A
    summon's or illusion's kill and damage count for its hero (the combat log's
    damage source).

    Args:
        match: A parsed match.

    Returns:
        One row per window, in time order, with ``WINDOW_COLUMNS``.
    """
    clock = match.game_clock
    if clock is None:
        return pd.DataFrame(columns=WINDOW_COLUMNS)
    heroes = {p.player_id: p for p in match.players}
    team_of = {p.hero_name: p.team for p in match.players}

    def seconds(tick: int) -> float:
        now = clock.game_time_at(tick)
        return now if now is not None else tick / 30

    objectives = [(seconds(t.tick), OTHER.get(t.team), t.tower_name) for t in match.towers]
    objectives += [(seconds(b.tick), OTHER.get(b.team), b.barracks_name) for b in match.barracks]
    slot_team = {p.player_id: p.team for p in match.players}
    # The protocol's team; the killer's own when it's missing (Source 1 replays).
    objectives += [
        (seconds(r.tick), r.killer_team or team_of.get(r.killer), "roshan") for r in match.roshans
    ]
    objectives += [
        (seconds(t.tick), t.killer_team or slot_team.get(t.killer_player_id), "tormentor")
        for t in match.tormentors
    ]
    deaths = [
        e
        for e in match.combat_log
        if e.log_type == "DEATH" and e.target_name in team_of and not e.target_is_illusion
    ]
    damage = [
        e
        for e in match.combat_log
        if e.log_type == "DAMAGE"
        and e.value
        and (e.target_name == "npc_dota_roshan" or BUILDING.match(e.target_name))
    ]
    watched = {*BUFFS.values(), "modifier_illusion"}
    modifiers = [
        e
        for e in match.combat_log
        if e.log_type in ("MODIFIER_ADD", "MODIFIER_REMOVE") and e.inflictor_name in watched
    ]
    uses = [(r, r.end_tick, False) for r in match.runes if r.outcome == "picked_up"]
    uses += [(r, r.used_tick, True) for r in match.runes if r.used_tick is not None]
    rows = []
    for rune, tick, from_bottle in uses:
        if tick is None or rune.player_id not in heroes:
            continue
        if rune.rune_type not in BUFFS and rune.rune_type != ILLUSION:
            continue
        player = heroes[rune.player_id]
        hero, team = player.hero_name, player.team
        window = _window(match, modifiers, rune.rune_type, hero, tick)
        if window is None:
            continue
        start, end = window
        start_s, end_s = seconds(start), seconds(end)

        def mine(
            entry: CombatLogEntry, hero: str = hero, start: int = start, end: int = end
        ) -> bool:
            return (
                start <= entry.tick <= end
                and (entry.damage_source_name or entry.attacker_name) == hero
            )

        killed = [e.target_name for e in deaths if mine(e) and team_of[e.target_name] != team]
        took = [
            (round(when - start_s), name.removeprefix("npc_dota_"))
            for when, side, name in sorted(objectives)
            if side == team and start_s <= when <= end_s + AFTER_S
        ]
        rows.append(
            {
                "match_id": match.match_id,
                "rune": RUNES[rune.rune_type],
                "hero": hero,
                "side": TEAMS.get(team),
                "from_bottle": from_bottle,
                "start_s": start_s,
                "end_s": end_s,
                "died": any(start <= e.tick <= end and e.target_name == hero for e in deaths),
                "kills": len(killed),
                "killed": ", ".join(killed),
                "roshan_damage": sum(
                    e.value for e in damage if mine(e) and e.target_name == "npc_dota_roshan"
                ),
                "building_damage": sum(
                    e.value for e in damage if mine(e) and e.target_name != "npc_dota_roshan"
                ),
                "took": ", ".join(name for _, name in took),
                "took_s": ", ".join(str(after) for after, _ in took),
            }
        )
    frame = pd.DataFrame(rows, columns=WINDOW_COLUMNS)
    return frame.sort_values("start_s", ignore_index=True)


def rune_summary(runes: pd.DataFrame) -> pd.DataFrame:
    """Return each side's runes by stage and kind: taken (or bottled), and denied.

    Args:
        runes: ``rune_table(...)`` for one match or many.

    Returns:
        One row per match, stage and side, with ``SUMMARY_COLUMNS``.
    """
    taken = runes[runes["outcome"].isin(["picked_up", "bottled"])]
    rows = []
    for match_id in runes["match_id"].unique():
        for stage, _, _ in STAGES:
            for side in TEAMS.values():
                mine = taken[
                    (taken["match_id"] == match_id)
                    & (taken["stage"] == stage)
                    & (taken["side"] == side)
                ]
                bounty = mine[mine["kind"] == "bounty"]
                denied = runes[
                    (runes["match_id"] == match_id)
                    & (runes["stage"] == stage)
                    & (runes["side"] == side)
                    & (runes["outcome"] == "denied")
                ]
                rows.append(
                    {
                        "match_id": match_id,
                        "stage": stage,
                        "side": side,
                        "power": int((mine["kind"] == "power").sum()),
                        "water": int((mine["kind"] == "water").sum()),
                        "bounty_own_jungle": int((bounty["whose"] == "own").sum()),
                        "bounty_other_jungle": int((bounty["whose"] == "other").sum()),
                        "bounty_river": int((bounty["whose"] == "river").sum()),
                        "denied": len(denied),
                    }
                )
    return pd.DataFrame(rows, columns=SUMMARY_COLUMNS)


def _clock(time_s: float) -> str:
    sign = "-" if time_s < 0 else ""
    whole = abs(int(time_s))
    return f"{sign}{whole // 60:d}:{whole % 60:02d}"


def main(paths: list[str]) -> None:
    """Print each replay's runes by side and stage, its 0:00 bounties, and its power runes' windows."""
    if len(paths) == 1:
        matches = [gem.parse(paths[0])]
    else:
        matches = [result.match for result in gem.parse_many(paths) if result.match is not None]
    tables, windows = [], []
    for match in matches:
        runes = rune_table(match)
        tables.append(runes)
        print(f"\n{match.match_id}: runes taken by each side, by stage")
        summary = rune_summary(runes).drop(columns=["match_id"])
        print(summary.to_string(index=False))
        print("\nThe 0:00 bounties:")
        print(opening_bounties(match, runes).drop(columns=["match_id"]).to_string(index=False))
        deaths = opening_deaths(match)
        print(f"Hero deaths up to {_clock(OPENING_S)}: {len(deaths)}")
        found = rune_windows(match)
        windows.append(found)
        shown = found.assign(
            start=found["start_s"].map(_clock),
            lasted_s=(found["end_s"] - found["start_s"]).round(),
            objectives=found["took"].map(lambda took: len(took.split(", ")) if took else 0),
        )
        print("\nPower runes, and what happened while each lasted:")
        columns = ["start", "rune", "hero", "from_bottle", "lasted_s", "kills", "objectives"]
        print(shown[columns].to_string(index=False))
        print(f"\nObjectives the taker's team took during one or within {AFTER_S} s after:")
        for row in shown[shown["took"] != ""].itertuples(index=False):
            print(f"  {row.start} {row.rune}, {row.hero}: {row.took}")
    every = pd.concat(windows, ignore_index=True)
    with_objective = every[every["took"] != ""]
    print(
        f"\n{len(with_objective)} of {len(every)} power runes were followed by an objective for the"
        f" taker's team during them or within {AFTER_S} s after."
    )


if __name__ == "__main__":  # parse_many's worker processes re-import this file
    main(sys.argv[1:])
