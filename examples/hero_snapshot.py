"""Hero snapshot — rich per-hero state at game start.

Parses the replay until all 10 heroes have been created, then prints a
detailed snapshot of each hero: position, stats, attributes, combat values,
vision, and team.

Usage::

    uv run python examples/hero_snapshot.py path/to/replay.dem
"""

from __future__ import annotations

import sys
from pathlib import Path

from gem.entities import Entity, EntityOp
from gem.parser import ReplayParser

# Source 2 cell size in world units
_CELL_SIZE = 128

TEAM_NAMES = {2: "Radiant", 3: "Dire"}
ATTR_NAMES = {0: "Strength", 1: "Agility", 2: "Intelligence", 3: "Universal"}


def world_pos(entity: Entity) -> tuple[float, float, float]:
    """Convert cell + sub-cell offset to world coordinates."""
    cx, _ = entity.get_int32("CBodyComponent.m_cellX")
    cy, _ = entity.get_int32("CBodyComponent.m_cellY")
    cz, _ = entity.get_int32("CBodyComponent.m_cellZ")
    vx, _ = entity.get_float32("CBodyComponent.m_vecX")
    vy, _ = entity.get_float32("CBodyComponent.m_vecY")
    vz, _ = entity.get_float32("CBodyComponent.m_vecZ")
    return (cx * _CELL_SIZE + vx, cy * _CELL_SIZE + vy, cz * _CELL_SIZE + vz)


def print_hero(entity: Entity) -> None:
    name = entity.get_class_name()
    team, _ = entity.get_int32("m_iTeamNum")
    player_id, _ = entity.get_int32("m_iPlayerID")
    level, _ = entity.get_int32("m_iCurrentLevel")
    xp, _ = entity.get_int32("m_iCurrentXP")

    hp, _ = entity.get_int32("m_iHealth")
    max_hp, _ = entity.get_int32("m_iMaxHealth")
    hp_regen, _ = entity.get_float32("m_flHealthRegen")
    mana, _ = entity.get_float32("m_flMana")
    max_mana, _ = entity.get_float32("m_flMaxMana")
    mana_regen, _ = entity.get_float32("m_flManaRegen")

    str_base, _ = entity.get_float32("m_flStrength")
    agi_base, _ = entity.get_float32("m_flAgility")
    int_base, _ = entity.get_float32("m_flIntellect")
    str_total, _ = entity.get_float32("m_flStrengthTotal")
    agi_total, _ = entity.get_float32("m_flAgilityTotal")
    int_total, _ = entity.get_float32("m_flIntellectTotal")
    primary, _ = entity.get_int32("m_iPrimaryAttribute")

    dmg_min, _ = entity.get_int32("m_iDamageMin")
    dmg_max, _ = entity.get_int32("m_iDamageMax")
    attack_range, _ = entity.get_int32("m_iAttackRange")
    bat, _ = entity.get_float32("m_flBaseAttackTime")
    move_speed, _ = entity.get_int32("m_iMoveSpeed")
    armor, _ = entity.get_float32("m_flPhysicalArmorValue")
    magic_resist, _ = entity.get_float32("m_flMagicalResistanceValue")

    day_vision, _ = entity.get_int32("m_iDayTimeVisionRange")
    night_vision, _ = entity.get_int32("m_iNightTimeVisionRange")

    wx, wy, wz = world_pos(entity)

    team_label = TEAM_NAMES.get(team, str(team))
    attr_label = ATTR_NAMES.get(primary, str(primary))
    hero_short = name.replace("CDOTA_Unit_Hero_", "")

    print(f"{'─' * 60}")
    print(f"  {hero_short}  (player {player_id}, {team_label}, lv{level})")
    print(f"{'─' * 60}")
    print(f"  Position       ({wx:.0f}, {wy:.0f}, {wz:.0f})")
    print(f"  HP             {hp} / {max_hp}  (+{hp_regen:.2f}/s)")
    print(f"  Mana           {mana:.0f} / {max_mana:.0f}  (+{mana_regen:.2f}/s)")
    print(f"  Primary attr   {attr_label}")
    print(f"  STR            {str_base:.0f}  (total {str_total:.0f})")
    print(f"  AGI            {agi_base:.0f}  (total {agi_total:.0f})")
    print(f"  INT            {int_base:.0f}  (total {int_total:.0f})")
    print(f"  Damage         {dmg_min}–{dmg_max}")
    print(f"  Attack range   {attack_range}  BAT {bat:.2f}s")
    print(f"  Move speed     {move_speed}")
    print(f"  Armor          {armor:.1f}  Magic resist {magic_resist:.0f}%")
    print(f"  Vision         {day_vision} day / {night_vision} night")
    print(f"  XP             {xp}")
    print()


def main(dem_path: str) -> None:
    path = Path(dem_path)
    if not path.exists():
        print(f"File not found: {dem_path}")
        sys.exit(1)

    print(f"Parsing: {path.name}\n")

    heroes: dict[int, Entity] = {}
    parser = ReplayParser(path)

    def on_entity(entity: Entity, op: EntityOp) -> None:
        if "Hero" in entity.get_class_name() and op.has(EntityOp.CREATED):
            heroes[entity.get_index()] = entity
            if len(heroes) == 10:
                parser.stop_after_tick(parser.tick)

    parser.on_entity(on_entity)
    parser.parse()

    if not heroes:
        print("No heroes found — replay may be truncated.")
        return

    radiant = [e for e in heroes.values() if e.get_int32("m_iTeamNum")[0] == 2]
    dire = [e for e in heroes.values() if e.get_int32("m_iTeamNum")[0] == 3]

    print(f"{'═' * 60}")
    print(f"  RADIANT  ({len(radiant)} heroes)")
    print(f"{'═' * 60}\n")
    for e in sorted(radiant, key=lambda e: e.get_int32("m_iPlayerID")[0]):
        print_hero(e)

    print(f"{'═' * 60}")
    print(f"  DIRE  ({len(dire)} heroes)")
    print(f"{'═' * 60}\n")
    for e in sorted(dire, key=lambda e: e.get_int32("m_iPlayerID")[0]):
        print_hero(e)

    print(f"Game build: {parser.game_build}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run python examples/hero_snapshot.py <replay.dem>")
        sys.exit(1)
    main(sys.argv[1])
