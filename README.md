# gem

![Python](https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green?logo=opensourceinitiative&logoColor=white)
![Phase](https://img.shields.io/badge/phase-4%20of%206-orange)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)

**Gem of True Sight** — a Python Dota 2 replay parser.

Reads Source 2 `.dem` binary replay files and exposes structured output: per-tick entity state, combat events, ward placements, smoke usage, Roshan kills, gold/XP timelines, and more.

---

## Why gem?

Existing parsers (Clarity, Manta, OpenDota/parser) are built for backend services in Java or Go. `gem` brings that to Python without touching JVM toolchains or writing binary parsers from scratch.

```python
from gem.parser import ReplayParser
from gem.constants import hero_display

# Combat log — who dealt the most damage?
damage: dict[str, int] = {}

def on_entry(entry):
    if entry.log_type == "DAMAGE" and entry.attacker_is_hero:
        damage[entry.attacker_name] = damage.get(entry.attacker_name, 0) + entry.value

parser = ReplayParser("my_replay.dem")
parser.on_combat_log_entry(on_entry)
parser.parse()

for npc, total in sorted(damage.items(), key=lambda x: -x[1])[:5]:
    print(f"{hero_display(npc)}: {total:,} dmg")
```

```python
# Entity state — read hero HP/position/level every tick
from gem.parser import ReplayParser
from gem.entities import EntityOp

parser = ReplayParser("my_replay.dem")

def on_entity(entity, op):
    if op & EntityOp.CREATED and "Hero" in entity.get_class_name():
        hp, _ = entity.get_int32("m_iHealth")
        print(f"{entity.get_class_name()}: {hp} HP")

parser.on_entity(on_entity)
parser.parse()
```

---

## Implementation Status

| Phase | Scope | Status |
|---|---|---|
| 1 | `BitReader`, `DemoStream` — binary frame iteration | ✅ Complete |
| 2 | `sendtable`, `field_decoder`, `field_path` — schema layer | ✅ Complete |
| 3 | String tables, entity lifecycle | ✅ Complete |
| 4 | Game events, combat log, `gem.constants` | ✅ Complete |
| 5 | Gold/XP timelines, teamfights, objectives | 🔲 Planned |
| 6 | `gem.parse()` — full match output, DataFrame export | 🔲 Planned |

---

## What you can extract today (Phase 4)

| Data | Source |
|---|---|
| Damage, heals, kills per hero | Combat log `DAMAGE` / `HEAL` / `DEATH` |
| Abilities cast, items used | Combat log `ABILITY` / `ITEM` |
| Gold and XP gained with reason codes | Combat log `GOLD` / `XP` |
| Ward placements (who, when, ~where) | Combat log `ITEM` + entity coords |
| Smoke of Deceit activations + groups | Combat log `ITEM` + `MODIFIER_ADD` |
| Roshan kills + respawn windows | Combat log `DEATH` |
| Hero HP, mana, position, level per tick | Entity state polling |
| Tower health over time | Entity state polling |
| Hero display names, item names, ability names | `gem.constants` (bundled) |

---

## Installation

Requires Python 3.10+. Uses [`uv`](https://github.com/astral-sh/uv) for dependency management.

```bash
git clone https://github.com/whanyu1212/gem
cd gem
uv sync
```

---

## Quick start

```bash
# Full replay summary — combat log + entity snapshots
python examples/extraction_demo.py path/to/your.dem

# Focused vision/objective report — wards, smokes, Roshan
python examples/ward_smoke_rosh.py path/to/your.dem
```

Both scripts work without arguments and use the bundled test fixture.

---

## Documentation

Full concepts, tutorials, and API reference at the project docs site (built with MkDocs Material):

```bash
uv run mkdocs serve
```

Topics covered: DEM binary format, varint encoding, Protocol Buffers, the entity delta system, combat log ingestion, and known data limitations (ward coordinate coverage, smoke edge cases).

---

## Known limitations

- **Ward coordinates** — 100% of placements have exact entity coordinates. Match combat log `ITEM` events to entity events within ±60 ticks without globally consuming entity records (slots are reused).
- **Smoke empty groups** — if a smoke breaks instantly on activation (sentry ward truesight), the group list is empty. This is correct game behaviour.
- **Roshan drops** — Aegis, Cheese, and other Roshan drops are not in the combat log. Planned for Phase 5.
