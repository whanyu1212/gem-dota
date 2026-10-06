"""A small built match for the runes recipe's tests (tests/test_cookbook.py) and its export's."""

from __future__ import annotations

from gem.combat.log import CombatLogEntry, CombatLogType
from gem.extractors.objectives import RoshanKill, TowerKill
from gem.extractors.runes import Rune
from gem.results.models import ParsedMatch, ParsedPlayer
from gem.state.game_clock import GameClock

# The four rune spots on the 7.41 map, in world units.
TOP_RIVER, BOT_RIVER = (14700.0, 17500.0), (17600.0, 15200.0)
DIRE_JUNGLE, RADIANT_JUNGLE = (15400.0, 20800.0), (17000.0, 11700.0)
HORN = 900  # the horn's tick: game second 0
AXE, LINA = "npc_dota_hero_axe", "npc_dota_hero_lina"
PUDGE, SF = "npc_dota_hero_pudge", "npc_dota_hero_nevermore"


def at(second: float) -> int:
    """The tick of a game second."""
    return HORN + round(second * 30)


def runes_match() -> ParsedMatch:
    def player(pid: int, team: int, hero: str, spot: tuple[float, float]) -> ParsedPlayer:
        return ParsedPlayer(
            player_id=pid,
            team=team,
            hero_name=hero,
            position_log=[(at(s), *spot) for s in range(-30, 120)],
        )

    def entry(second: float, log_type: CombatLogType, **fields: object) -> CombatLogEntry:
        return CombatLogEntry(tick=at(second), log_type=log_type, **fields)  # type: ignore[arg-type]

    def pickup(second: float, slot: int, rune_type: int, clock_s: int) -> CombatLogEntry:
        return entry(
            second, CombatLogType.PICKUP_RUNE, value=slot, rune_type=rune_type, game_time_s=clock_s
        )

    used = 600.0  # the illusion rune's Bottle use
    combat_log = [
        # Pudge dies before the horn, and Lina at 1:40 (after the 0:00 bounties' deaths).
        entry(-10, CombatLogType.DEATH, attacker_name=AXE, target_name=PUDGE, target_is_hero=True),
        entry(3, CombatLogType.PICKUP_RUNE, value=0, rune_type=5, game_time_s=3),
        # The chat clock reads 5 though the rune left at 5.1 s.
        entry(5.1, CombatLogType.PICKUP_RUNE, value=1, rune_type=5, game_time_s=5),
        entry(100, CombatLogType.DEATH, attacker_name=SF, target_name=LINA, target_is_hero=True),
        pickup(125, 1, 7, 125),
        # Double damage for Shadow Fiend, 6:40 to 7:25: a kill, tower damage, and the tower.
        pickup(400, 6, 0, 400),
        entry(
            400,
            CombatLogType.MODIFIER_ADD,
            inflictor_name="modifier_rune_doubledamage",
            target_name=SF,
            target_is_hero=True,
        ),
        entry(420, CombatLogType.DEATH, attacker_name=SF, target_name=LINA, target_is_hero=True),
        # Axe's Aegis triggers: not a death, so not a kill.
        entry(
            425,
            CombatLogType.DEATH,
            attacker_name=SF,
            target_name=AXE,
            target_is_hero=True,
            will_reincarnate=True,
        ),
        entry(
            430,
            CombatLogType.DAMAGE,
            attacker_name=SF,
            target_name="npc_dota_goodguys_tower1_top",
            value=300,
        ),
        entry(
            445,
            CombatLogType.MODIFIER_REMOVE,
            inflictor_name="modifier_rune_doubledamage",
            target_name=SF,
            target_is_hero=True,
        ),
        # Axe uses a bottled illusion rune at 10:00: two illusions, one gone after
        # 30 s and one after 100 s (capped at 75), one hitting Roshan; Radiant kills
        # Roshan at 10:40. An illusion Axe had from 9:50 goes first, at 10:00.
        pickup(used, 0, 2, 600),
        *[
            entry(
                used + 4 / 30,
                CombatLogType.MODIFIER_ADD,
                inflictor_name="modifier_illusion",
                target_name=AXE,
                target_is_illusion=True,
            )
            for _ in range(2)
        ],
        entry(
            620,
            CombatLogType.DAMAGE,
            attacker_name=AXE,
            damage_source_name=AXE,
            attacker_is_illusion=True,
            target_name="npc_dota_roshan",
            value=200,
        ),
        *[
            entry(
                used + 4 / 30 + lasted,
                CombatLogType.MODIFIER_REMOVE,
                inflictor_name="modifier_illusion",
                target_name=AXE,
                target_is_illusion=True,
                modifier_elapsed_duration_s=lasted,
            )
            for lasted in (30.0, 100.0)
        ],
        entry(
            used + 4 / 30 + 10,
            CombatLogType.MODIFIER_REMOVE,
            inflictor_name="modifier_illusion",
            target_name=AXE,
            target_is_illusion=True,
            modifier_elapsed_duration_s=20.0,
        ),
    ]
    runes = [
        # The 0:00 bounties: Axe in Dire's jungle, Lina at the top river; Radiant's not taken.
        Rune(at(0), 5, *DIRE_JUNGLE, end_tick=at(3), outcome="picked_up", player_id=0),
        Rune(at(0), 5, *TOP_RIVER, end_tick=at(5.1), outcome="picked_up", player_id=1),
        Rune(at(0), 5, *RADIANT_JUNGLE, end_tick=at(120), outcome="not_taken"),
        Rune(at(120), 7, *TOP_RIVER, end_tick=at(125), outcome="picked_up", player_id=1),
        Rune(at(360), 0, *TOP_RIVER, end_tick=at(400), outcome="picked_up", player_id=6),
        Rune(
            at(480),
            2,
            *BOT_RIVER,
            end_tick=at(500),
            outcome="bottled",
            player_id=0,
            used_tick=at(used),
        ),
        Rune(at(1200), 9, *BOT_RIVER, end_tick=at(1210), outcome="denied", player_id=5),
        Rune(at(1320), 1, *TOP_RIVER),
    ]
    return ParsedMatch(
        match_id=9,
        game_start_tick=HORN,
        game_clock=GameClock(game_start_tick=HORN),
        players=[
            player(0, 2, AXE, DIRE_JUNGLE),
            player(1, 2, LINA, TOP_RIVER),
            # Pudge stands 1,000 units from Axe's bounty; Shadow Fiend is far away.
            player(5, 3, PUDGE, (DIRE_JUNGLE[0] + 1000, DIRE_JUNGLE[1])),
            player(6, 3, SF, BOT_RIVER),
        ],
        combat_log=combat_log,
        towers=[
            TowerKill(tick=at(460), team=2, killer=SF, tower_name="npc_dota_goodguys_tower1_top")
        ],
        roshans=[RoshanKill(tick=at(640), killer=AXE, kill_number=1)],
        runes=runes,
    )
