"""Phase 3 example — entity lifecycle and string tables.

Uses ReplayParser to drive the full parse loop and prints:
  - Schema size (serializers loaded)
  - Classes registered after CDemoClassInfo
  - All hero/NPC entities created in the first full packet (name + health)
  - Active entity count at end of the first full packet

Usage::

    uv run python examples/phase3_entities.py path/to/replay.dem
"""

from __future__ import annotations

import sys
from pathlib import Path

from gem.entities import Entity, EntityOp
from gem.parser import ReplayParser


def main(dem_path: str) -> None:
    path = Path(dem_path)
    if not path.exists():
        print(f"File not found: {dem_path}")
        sys.exit(1)

    print(f"Parsing: {path.name}")

    seen_first_packet = False

    parser = ReplayParser(path)

    def on_entity(entity: Entity, op: EntityOp) -> None:
        nonlocal seen_first_packet
        if not seen_first_packet and op.has(EntityOp.CREATED):
            name = entity.get_class_name()
            if "Hero" in name or "NPC" in name:
                health = entity.get_int32("m_iHealth")
                print(f"  [{name}] m_iHealth={health if health is not None else '?'}")

    parser.on_entity(on_entity)
    parser.parse()

    em = parser.entity_manager
    if em is None:
        print("No entity manager — send tables not found in replay.")
        return

    print(f"\nGame build:        {parser.game_build}")
    print(f"Serializers:       {len(em.serializers)}")
    print(f"Classes:           {len(em.classes_by_id)}")
    print(f"String tables:     {len(parser.string_tables.tables)}")
    print(f"Active entities:   {len(em.all_active())}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run python examples/phase3_entities.py <replay.dem>")
        sys.exit(1)
    main(sys.argv[1])
