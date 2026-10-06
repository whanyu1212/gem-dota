"""A small built match for the lanes recipe's tests (tests/test_cookbook.py) and its export's."""

from __future__ import annotations

from collections.abc import Callable

from gem.combat.log import CombatLogEntry, CombatLogType
from gem.results.models import GoldLedger, GoldLedgerSnapshot, ParsedMatch, ParsedPlayer
from gem.state.game_clock import GameClock

# Map cells on OpenDota's lane grid, in world units (cell * 128).
TOP, MID, BOT, JUNGLE = (
    (8960.0, 19200.0),
    (16384.0, 16384.0),
    (23040.0, 10240.0),
    (14080.0, 12800.0),
)


def lanes_match() -> ParsedMatch:
    def player(
        pid: int, team: int, hero: str, where: Callable[[int], tuple[float, float]]
    ) -> ParsedPlayer:
        minutes = list(range(0, 601, 60))
        return ParsedPlayer(
            player_id=pid,
            team=team,
            hero_name=hero,
            position_log=[(s * 30, *where(s)) for s in range(0, 601)],
            game_times_min=minutes,
            net_worth_t_min=[1000 + 10 * m * (pid + 1) for m in minutes],
            total_earned_xp_t_min=[5 * m for m in minutes],
            total_earned_gold_t_min=[600 + 4 * m for m in minutes],
            lh_t_min=[m // 10 for m in minutes],
            dn_t_min=[m // 60 for m in minutes],
            gold_ledger=GoldLedger(
                per_minute=[
                    GoldLedgerSnapshot(
                        tick=m * 30, game_time_s=m, creep_kill_gold=2 * m, neutral_kill_gold=m // 2
                    )
                    for m in minutes
                ]
            ),
        )

    axe, lina, pudge, sf = (
        "npc_dota_hero_axe",
        "npc_dota_hero_lina",
        "npc_dota_hero_pudge",
        "npc_dota_hero_nevermore",
    )
    return ParsedMatch(
        match_id=8,
        game_start_tick=0,
        game_clock=GameClock(game_start_tick=0),
        players=[
            # Walks out through mid (before 0:30, not a visit), then top, with a
            # 40 s visit to mid.
            player(0, 2, axe, lambda s: MID if s < 25 or 300 <= s < 340 else TOP),
            # Mid, then teleports top at 6:40 and stays 30 s.
            player(1, 2, lina, lambda s: TOP if 401 <= s < 431 else MID),
            player(5, 3, pudge, lambda s: TOP),
            player(6, 3, sf, lambda s: JUNGLE if 90 <= s < 111 else MID),
        ],
        combat_log=[
            CombatLogEntry(
                tick=100 * 30,
                log_type=CombatLogType.DEATH,
                attacker_name=axe,
                target_name=sf,
                target_is_hero=True,
            ),
            CombatLogEntry(
                tick=400 * 30,
                log_type=CombatLogType.ITEM,
                attacker_name=lina,
                inflictor_name="item_tpscroll",
            ),
            CombatLogEntry(
                tick=410 * 30,
                log_type=CombatLogType.DEATH,
                attacker_name="npc_dota_lina_summon",
                damage_source_name=lina,
                target_name=pudge,
                target_is_hero=True,
            ),
        ],
    )
