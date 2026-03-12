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
    cx = entity.get_int32("CBodyComponent.m_cellX") or 0
    cy = entity.get_int32("CBodyComponent.m_cellY") or 0
    cz = entity.get_int32("CBodyComponent.m_cellZ") or 0
    vx = entity.get_float32("CBodyComponent.m_vecX") or 0.0
    vy = entity.get_float32("CBodyComponent.m_vecY") or 0.0
    vz = entity.get_float32("CBodyComponent.m_vecZ") or 0.0
    return (cx * _CELL_SIZE + vx, cy * _CELL_SIZE + vy, cz * _CELL_SIZE + vz)


def print_hero(entity: Entity) -> None:
    name = entity.get_class_name()
    team = entity.get_int32("m_iTeamNum") or 0
    player_id = entity.get_int32("m_iPlayerID") or 0
    level = entity.get_int32("m_iCurrentLevel") or 0
    xp = entity.get_int32("m_iCurrentXP") or 0

    hp = entity.get_int32("m_iHealth") or 0
    max_hp = entity.get_int32("m_iMaxHealth") or 0
    hp_regen = entity.get_float32("m_flHealthRegen") or 0.0
    mana = entity.get_float32("m_flMana") or 0.0
    max_mana = entity.get_float32("m_flMaxMana") or 0.0
    mana_regen = entity.get_float32("m_flManaRegen") or 0.0

    str_base = entity.get_float32("m_flStrength") or 0.0
    agi_base = entity.get_float32("m_flAgility") or 0.0
    int_base = entity.get_float32("m_flIntellect") or 0.0
    str_total = entity.get_float32("m_flStrengthTotal") or 0.0
    agi_total = entity.get_float32("m_flAgilityTotal") or 0.0
    int_total = entity.get_float32("m_flIntellectTotal") or 0.0
    primary = entity.get_int32("m_iPrimaryAttribute") or 0

    dmg_min = entity.get_int32("m_iDamageMin") or 0
    dmg_max = entity.get_int32("m_iDamageMax") or 0
    attack_range = entity.get_int32("m_iAttackRange") or 0
    bat = entity.get_float32("m_flBaseAttackTime") or 0.0
    move_speed = entity.get_int32("m_iMoveSpeed") or 0
    armor = entity.get_float32("m_flPhysicalArmorValue") or 0.0
    magic_resist = entity.get_float32("m_flMagicalResistanceValue") or 0.0

    day_vision = entity.get_int32("m_iDayTimeVisionRange") or 0
    night_vision = entity.get_int32("m_iNightTimeVisionRange") or 0

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

    radiant = [e for e in heroes.values() if e.get_int32("m_iTeamNum") == 2]
    dire = [e for e in heroes.values() if e.get_int32("m_iTeamNum") == 3]

    print(f"{'═' * 60}")
    print(f"  RADIANT  ({len(radiant)} heroes)")
    print(f"{'═' * 60}\n")
    for e in sorted(radiant, key=lambda e: e.get_int32("m_iPlayerID") or 0):
        print_hero(e)

    print(f"{'═' * 60}")
    print(f"  DIRE  ({len(dire)} heroes)")
    print(f"{'═' * 60}\n")
    for e in sorted(dire, key=lambda e: e.get_int32("m_iPlayerID") or 0):
        print_hero(e)

    print(f"Game build: {parser.game_build}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run python examples/hero_snapshot.py <replay.dem>")
        sys.exit(1)
    main(sys.argv[1])
