"""A small built match for the stacks recipe's tests (tests/test_cookbook.py) and its export's."""

from __future__ import annotations

from gem.combat.log import CombatLogEntry, CombatLogType
from gem.extractors.neutral_camps import CampStack, NeutralCreep
from gem.results.models import ParsedMatch, ParsedPlayer
from gem.state.game_clock import GameClock

LION, AA, TIMBER = (
    "npc_dota_hero_lion",
    "npc_dota_hero_ancient_apparition",
    "npc_dota_hero_shredder",
)
RUBICK, TREANT, SF = "npc_dota_hero_rubick", "npc_dota_hero_treant", "npc_dota_hero_nevermore"
MELEE = "npc_dota_creep_goodguys_melee"
ANCIENT, MEDIUM = 3, 6  # camp ids in camp_zones.json


def at(second: int) -> int:
    """The tick of a game second (the game starts at tick 0)."""
    return second * 30


def stacks_match() -> ParsedMatch:
    minutes = list(range(0, 601, 60))

    def player(pid: int, team: int, hero: str, lh_at_10: int) -> ParsedPlayer:
        return ParsedPlayer(
            player_id=pid,
            team=team,
            hero_name=hero,
            game_times_min=minutes,
            lh_t_min=[lh_at_10 * m // 600 for m in minutes],
        )

    def creep(camp: int, spawned: int, died: int | None, killer: str | None, pid: int | None):
        return NeutralCreep(
            camp_id=camp,
            spawned_tick=at(spawned),
            died_tick=at(died) if died is not None else None,
            killer_name=killer,
            killer_player_id=pid,
        )

    def stack(second: int, camp: int, kind: str, pid: int, exact: bool, waves: int) -> CampStack:
        return CampStack(
            tick=at(second),
            camp_id=camp,
            camp_type=kind,
            creeps_before=waves,
            waves_alive=waves,
            player_id=pid,
            player_exact=exact,
        )

    def entry(second: int, log_type: CombatLogType, **fields: object) -> CombatLogEntry:
        return CombatLogEntry(tick=at(second), log_type=log_type, **fields)  # type: ignore[arg-type]

    def death(second: int, attacker: str) -> CombatLogEntry:
        return entry(
            second,
            CombatLogType.DEATH,
            attacker_name=attacker,
            target_name="npc_dota_neutral_kobold",
        )

    def gold(second: int, hero: str, value: int) -> CombatLogEntry:
        return entry(second, CombatLogType.GOLD, target_name=hero, value=value, gold_reason=14)

    return ParsedMatch(
        match_id=7,
        game_start_tick=0,
        game_clock=GameClock(game_start_tick=0),
        players=[
            player(0, 2, LION, 5),
            player(1, 2, AA, 8),
            player(2, 2, TIMBER, 60),
            player(5, 3, RUBICK, 3),
            player(6, 3, TREANT, 4),
            player(7, 3, SF, 70),
        ],
        camp_stacks=[
            stack(240, ANCIENT, "ancient", 0, True, 2),
            # Stacked again: the creeps still there from the first stack stay the first's.
            stack(300, ANCIENT, "ancient", 0, True, 3),
            stack(300, MEDIUM, "medium", 7, False, 2),
        ],
        neutral_creeps=[
            creep(ANCIENT, 120, 200, LION, 0),  # died before any stack
            creep(ANCIENT, 180, 250, LION, 0),
            creep(ANCIENT, 180, 320, TIMBER, 2),
            creep(ANCIENT, 180, 320, TIMBER, 2),
            creep(ANCIENT, 240, 330, SF, 7),  # Lion's stack, taken by the enemy
            creep(ANCIENT, 240, None, None, None),  # alive at the end
            creep(ANCIENT, 300, 330, MELEE, None),  # pulled
            creep(MEDIUM, 240, 310, RUBICK, 5),
            creep(MEDIUM, 300, 310, RUBICK, 5),
        ],
        combat_log=[
            death(200, LION),
            gold(200, LION, 35),
            death(250, LION),
            gold(250, LION, 40),
            death(310, RUBICK),
            death(310, RUBICK),
            gold(310, RUBICK, 60),
            death(320, TIMBER),
            death(320, TIMBER),
            gold(320, TIMBER, 100),
            death(330, SF),
            gold(330, SF, 70),
            death(330, MELEE),
            death(500, TIMBER),
            gold(500, TIMBER, 200),  # not from a stack
        ],  # fmt: skip
    )
