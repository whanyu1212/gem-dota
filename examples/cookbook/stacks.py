"""Who stacked each camp, who cleared it, and what did the stacks give?

A stack is a camp that spawned a wave while creeps from an earlier wave were
still alive, and that the game counted (``match.camp_stacks``: the player it
credited, and whether that credit left no choice or the camp was matched by
position). Its stacked creeps are the camp's creeps alive at the stack: the
earlier waves and the new one (``match.neutral_creeps``). A creep in two stacks
of the same camp belongs to the first.

For each stacked creep: who killed it, and the gold the killer got for it, the
killer's creep-kill gold (``GOLD`` reason ``NEUTRAL_GOLD``) on the tick it died,
split evenly over the neutrals the killer's units killed on that tick. A summon's
or an illusion's kill counts for its hero. A stacked creep killed by a lane creep
was pulled; it counts for no player.

A player is a support or a core by last hits: the ``SUPPORTS_PER_TEAM`` players
of each side with the fewest at ``ROLE_READING_S`` are supports. That is this
recipe's choice; change it to use another.

    python examples/cookbook/stacks.py replay.dem [more.dem ...]
"""

from __future__ import annotations

import sys
from collections import Counter, defaultdict

import pandas as pd

import gem

SUPPORTS_PER_TEAM = 2  # this many players per side with the fewest last hits are supports
ROLE_READING_S = 600  # the last hits that decide supports and cores: at 10:00
NEUTRAL_GOLD = 14  # the GOLD reason for killing a neutral creep
NEUTRAL_PREFIX = "npc_dota_neutral_"
LANE_CREEP_PREFIX = "npc_dota_creep_"
TEAMS = {2: "radiant", 3: "dire"}
STACK_COLUMNS = [
    "match_id", "time_s", "camp", "camp_type", "hero", "side", "role", "exact", "waves", "creeps",
]  # fmt: skip
CREEP_COLUMNS = [
    "match_id", "stack_s", "camp", "stacker", "stacker_side", "died_s", "killer", "killer_side",
    "pulled", "gold",
]  # fmt: skip
FLOW_COLUMNS = [
    "match_id", "stacker", "stacker_side", "killer", "killer_side", "enemy", "creeps", "gold",
]  # fmt: skip
PLAYER_COLUMNS = [
    "match_id", "hero", "side", "role", "stacks", "exact", "killed", "gold", "neutral_gold",
]  # fmt: skip


def roles(match: gem.ParsedMatch) -> dict[str, str]:
    """Return each hero's role: ``support`` or ``core``, by last hits at ``ROLE_READING_S``.

    Args:
        match: A parsed match.

    Returns:
        Hero name -> ``support`` or ``core``.
    """
    out = {}
    for team in TEAMS:
        side = [p for p in match.players if p.team == team]
        side.sort(key=lambda p: _last_hits_at(p, ROLE_READING_S))
        for i, player in enumerate(side):
            out[player.hero_name] = "support" if i < SUPPORTS_PER_TEAM else "core"
    return out


def _last_hits_at(player: gem.ParsedPlayer, time_s: int) -> int:
    if time_s in player.game_times_min:
        return player.lh_t_min[player.game_times_min.index(time_s)]
    return player.lh_t_min[-1] if player.lh_t_min else 0


def _seconds(match: gem.ParsedMatch, tick: int) -> int | None:
    return match.game_clock.game_seconds_at(tick) if match.game_clock is not None else None


def stack_table(match: gem.ParsedMatch, role: dict[str, str] | None = None) -> pd.DataFrame:
    """Return every stack: when, which camp, who stacked it and how many creeps it held.

    Args:
        match: A parsed match.
        role: ``roles(match)``, if already built.

    Returns:
        One row per stack, in time order, with ``STACK_COLUMNS``. ``exact`` is
        ``True`` when the game's credit left no choice of camp; ``creeps`` counts
        the stacked creeps (the earlier waves alive and the new one).
    """
    role = roles(match) if role is None else role
    heroes = {p.player_id: p for p in match.players}
    held = Counter(id(stack) for stack, _ in _stacked(match))
    rows = []
    for stack in match.camp_stacks:
        player = heroes.get(stack.player_id) if stack.player_id is not None else None
        hero = player.hero_name if player else None
        rows.append(
            {
                "match_id": match.match_id,
                "time_s": _seconds(match, stack.tick),
                "camp": stack.camp_id,
                "camp_type": stack.camp_type,
                "hero": hero,
                "side": TEAMS.get(player.team) if player else None,
                "role": role.get(hero) if hero else None,
                "exact": stack.player_exact,
                "waves": stack.waves_alive,
                "creeps": held[id(stack)],
            }
        )
    return pd.DataFrame(rows, columns=STACK_COLUMNS)


def _stacked(match: gem.ParsedMatch) -> list[tuple[gem.CampStack, gem.NeutralCreep]]:
    """Each stacked creep with the first stack of its camp it was alive at."""
    by_camp: dict[int | None, list[gem.NeutralCreep]] = defaultdict(list)
    for creep in match.neutral_creeps:
        by_camp[creep.camp_id].append(creep)
    first: dict[int, tuple[gem.CampStack, gem.NeutralCreep]] = {}
    for stack in sorted(match.camp_stacks, key=lambda s: s.tick):
        for creep in by_camp[stack.camp_id]:
            alive = creep.spawned_tick <= stack.tick and (
                creep.died_tick is None or creep.died_tick > stack.tick
            )
            if alive:
                first.setdefault(id(creep), (stack, creep))
    return list(first.values())


def _kill_gold(match: gem.ParsedMatch) -> dict[tuple[int, str], float]:
    """Each hero's creep-kill gold on a tick, per neutral its units killed on that tick."""
    gold: Counter[tuple[int, str]] = Counter()
    kills: Counter[tuple[int, str]] = Counter()
    for entry in match.combat_log:
        if entry.log_type == "GOLD" and entry.gold_reason == NEUTRAL_GOLD:
            gold[(entry.tick, entry.target_name)] += entry.value
        elif entry.log_type == "DEATH" and entry.target_name.startswith(NEUTRAL_PREFIX):
            kills[(entry.tick, entry.damage_source_name or entry.attacker_name)] += 1
    return {key: value / max(kills[key], 1) for key, value in gold.items()}


def stacked_creeps(match: gem.ParsedMatch) -> pd.DataFrame:
    """Return every stacked creep: its stack, who killed it and the gold it gave.

    Args:
        match: A parsed match.

    Returns:
        One row per stacked creep, with ``CREEP_COLUMNS``. ``killer`` is the
        killing player's hero, or the unit that killed it when no player did
        (a lane creep for a pulled creep), or ``None`` if unknown or alive.
        ``gold`` is the creep's share of its killer's gold, unrounded.
    """
    heroes = {p.player_id: p for p in match.players}
    gold = _kill_gold(match)
    rows = []
    for stack, creep in _stacked(match):
        stacker = heroes.get(stack.player_id) if stack.player_id is not None else None
        killer = heroes.get(creep.killer_player_id) if creep.killer_player_id is not None else None
        pulled = (creep.killer_name or "").startswith(LANE_CREEP_PREFIX)
        died = creep.died_tick
        rows.append(
            {
                "match_id": match.match_id,
                "stack_s": _seconds(match, stack.tick),
                "camp": stack.camp_id,
                "stacker": stacker.hero_name if stacker else None,
                "stacker_side": TEAMS.get(stacker.team) if stacker else None,
                "died_s": _seconds(match, died) if died is not None else None,
                "killer": killer.hero_name if killer else creep.killer_name,
                "killer_side": TEAMS.get(killer.team) if killer else None,
                "pulled": pulled,
                "gold": gold.get((died, killer.hero_name), 0.0) if killer and died else 0.0,
            }
        )
    frame = pd.DataFrame(rows, columns=CREEP_COLUMNS)
    frame["died_s"] = frame["died_s"].astype("Int64")
    return frame


def flows(creeps: pd.DataFrame) -> pd.DataFrame:
    """Return who cleared each player's stacks: stacked creeps and gold, stacker -> killer.

    Only creeps a player stacked and a player killed count. ``enemy`` marks a
    side's stacked creeps the other side killed.

    Args:
        creeps: ``stacked_creeps(...)`` for one match or many.

    Returns:
        One row per match, stacker and killer, most creeps first, with ``FLOW_COLUMNS``.
    """
    played = creeps.dropna(subset=["stacker", "killer_side"])
    grouped = played.groupby(
        ["match_id", "stacker", "stacker_side", "killer", "killer_side"], as_index=False
    ).agg(creeps=("gold", "size"), gold=("gold", "sum"))
    grouped["enemy"] = grouped["stacker_side"] != grouped["killer_side"]
    grouped["gold"] = grouped["gold"].astype(float).round().astype(int)
    return grouped[FLOW_COLUMNS].sort_values(
        ["match_id", "creeps"], ascending=[True, False], kind="stable", ignore_index=True
    )


def player_table(
    match: gem.ParsedMatch,
    stacks: pd.DataFrame | None = None,
    creeps: pd.DataFrame | None = None,
    role: dict[str, str] | None = None,
) -> pd.DataFrame:
    """Return each player's stacks, and the stacked creeps they killed and their gold.

    ``neutral_gold`` is all the player's creep-kill gold from neutrals, stacked
    or not, to set the stacks' gold against.

    Args:
        match: A parsed match.
        stacks: ``stack_table(match)``, if already built.
        creeps: ``stacked_creeps(match)``, if already built.
        role: ``roles(match)``, if already built.

    Returns:
        One row per player, Radiant first, with ``PLAYER_COLUMNS``.
    """
    role = roles(match) if role is None else role
    stacks = stack_table(match, role) if stacks is None else stacks
    creeps = stacked_creeps(match) if creeps is None else creeps
    neutral: Counter[str] = Counter()
    for entry in match.combat_log:
        if entry.log_type == "GOLD" and entry.gold_reason == NEUTRAL_GOLD:
            neutral[entry.target_name] += entry.value
    killed = creeps.dropna(subset=["killer_side"])
    rows = []
    for player in sorted(match.players, key=lambda p: (p.team, p.player_id)):
        hero = player.hero_name
        mine = stacks[stacks["hero"] == hero]
        kills = killed[killed["killer"] == hero]
        rows.append(
            {
                "match_id": match.match_id,
                "hero": hero,
                "side": TEAMS.get(player.team),
                "role": role.get(hero),
                "stacks": len(mine),
                "exact": int(mine["exact"].sum()),
                "killed": len(kills),
                "gold": round(kills["gold"].sum()),
                "neutral_gold": neutral[hero],
            }
        )
    return pd.DataFrame(rows, columns=PLAYER_COLUMNS)


def main(paths: list[str]) -> None:
    """Print each replay's stacks, who cleared them and each player's numbers, then the totals."""
    if len(paths) == 1:
        matches = [gem.parse(paths[0])]
    else:
        matches = [result.match for result in gem.parse_many(paths) if result.match is not None]
    players = []
    for match in matches:
        role = roles(match)
        stacks = stack_table(match, role)
        creeps = stacked_creeps(match)
        table = player_table(match, stacks, creeps, role)
        players.append(table)
        by_side = stacks["side"].value_counts()
        print(
            f"\n{match.match_id}: {len(stacks)} stacks (radiant {by_side.get('radiant', 0)}, "
            f"dire {by_side.get('dire', 0)}), {(stacks['role'] == 'support').sum()} by supports; "
            f"stacked creeps pulled: {int(creeps['pulled'].sum())}"
        )
        print(stacks.drop(columns=["match_id"]).to_string(index=False))
        print("Stacked by -> cleared by:")
        print(flows(creeps).drop(columns=["match_id"]).to_string(index=False))
        print(table.drop(columns=["match_id"]).to_string(index=False))
    every = pd.concat(players, ignore_index=True)
    cores = every[every["role"] == "core"]
    print(
        f"\nSupports made {every.loc[every['role'] == 'support', 'stacks'].sum()} of "
        f"{every['stacks'].sum()} stacks. Cores killed {cores['killed'].sum()} of "
        f"{every['killed'].sum()} stacked creeps a player killed, and took "
        f"{cores['gold'].sum():,} of their {cores['neutral_gold'].sum():,} neutral gold from them."
    )


if __name__ == "__main__":  # parse_many's worker processes re-import this file
    main(sys.argv[1:])
