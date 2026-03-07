# gem

![Python](https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green?logo=opensourceinitiative&logoColor=white)
![Phase](https://img.shields.io/badge/phase-3%20of%206-orange)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)

**Gem of True Sight** — a Python Dota 2 replay parser.

Reads Source 2 `.dem` binary replay files and exposes structured output: per-tick entity state, combat events, gold/XP timelines, teamfights, objectives, and more.

---

## Why gem?

Existing parsers (Clarity, Manta, OpenDota/parser) are built for backend services in Java or Go. `gem` brings that to Python without touching JVM toolchains or writing binary parsers from scratch.

```python
from gem.parser import ReplayParser
from gem.entities import EntityOp

# Phase 3 — entity lifecycle
parser = ReplayParser("my_replay.dem")

def on_entity(entity, op):
    if op.has(EntityOp.CREATED):
        name = entity.get_class_name()
        if "Hero" in name:
            hp, ok = entity.get_int32("m_iHealth")
            print(f"{name}: {hp} HP")

parser.on_entity(on_entity)
parser.parse()

# Phase 6 — full match output (coming soon)
# match = gem.parse("my_replay.dem")
# df = match.combat_log.to_dataframe()
```

---

## Implementation Status

| Phase | Scope | Status |
|---|---|---|
| 1 | `BitReader`, `DemoStream` — binary frame iteration | ✅ Complete |
| 2 | `sendtable`, `field_decoder`, `field_path` — schema layer | ✅ Complete |
| 3 | String tables, entity lifecycle | ✅ Complete |
| 4 | Game events, combat log | 🔲 Planned |
| 5 | Gold/XP timelines, teamfights, objectives | 🔲 Planned |
| 6 | `gem.parse()` — full match output, DataFrame export | 🔲 Planned |

---

## Installation

Requires Python 3.10+. Uses [`uv`](https://github.com/astral-sh/uv) for dependency management.

```bash
git clone https://github.com/whanyu1212/gem
cd gem
uv sync
```

---

## Documentation

Full concepts, tutorials, and API reference at the project docs site (built with MkDocs Material):

```bash
uv run mkdocs serve
```

Topics covered: DEM binary format, varint encoding, Protocol Buffers, the entity delta system, and the combat log ingestion pipeline.
