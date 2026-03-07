# gem-dota

![Python](https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green?logo=opensourceinitiative&logoColor=white)
![Phase](https://img.shields.io/badge/phase-1%20of%206-orange)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)

**Gem of True Sight** — a Python Dota 2 replay parser.

Reads Source 2 `.dem` binary replay files and exposes structured output: per-tick entity state, combat events, gold/XP timelines, teamfights, objectives, and more.

---

## Why gem?

Existing parsers (Clarity, Manta, OpenDota) are built for backend services in Java or Go. `gem` brings that to Python without touching JVM toolchains or writing binary parsers from scratch.

```python
import gem

# Stream outer messages (Phase 1 — available now)
with gem.DemoStream("my_replay.dem") as stream:
    for tick, msg_type, data in stream:
        ...

# Full match output (Phase 6 — coming soon)
match = gem.parse("my_replay.dem")
df = match.combat_log.to_dataframe()
```

---

## Implementation Status

| Phase | Scope | Status |
|---|---|---|
| 1 | `BitReader`, `DemoStream` — binary frame iteration | ✅ Complete |
| 2 | Send tables, field paths, field decoders | 🔲 Planned |
| 3 | String tables, entity lifecycle | 🔲 Planned |
| 4 | Game events, combat log | 🔲 Planned |
| 5 | Gold/XP timelines, teamfights, objectives | 🔲 Planned |
| 6 | `gem.parse()` — full match output, DataFrame export | 🔲 Planned |

---

## Installation

Requires Python 3.10+. Uses [`uv`](https://github.com/astral-sh/uv) for dependency management.

```bash
git clone https://github.com/whanyu1212/gem-dota
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

---

## License

MIT
