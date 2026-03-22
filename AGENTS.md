# AGENTS.md

This file provides guidance to agents (i.e., ADAL) when working with code in this repository.

## Project Snapshot

- **Project**: `gem` — Source 2 Dota 2 replay parser (Python)
- **Current state**: Core parser + extractors are implemented through **Phase 10**, with Phase 11b modularization landed (`match_builder.py`, `combat_aggregator.py`, `dataframes.py`)
- **Current branch**: `validation`
- **Package manager / env**: `uv` with local `.venv`
- **Primary references**:
  - `refs/manta/` (Go; primary implementation/behavior reference)
  - `refs/clarity/` (Java; edge-case/correctness authority)
  - `refs/parser/` (OpenDota parser; output schema authority)

---

## Essential Commands (Copy/Paste)

### Environment Setup

```bash
uv sync
source .venv/bin/activate
```

**Gotcha**: Run `uv sync` first so `pytest`, `ruff`, `mypy`, and proto tooling are available.

### Development / Protobuf Generation

```bash
uv run python scripts/compile_protos.py
uv run python scripts/compile_protos.py --force
uv run python scripts/compile_protos.py --verbose
```

- `scripts/compile_protos.py` is the canonical proto workflow.
- Do not rely on system `protoc`.

### Test Commands

```bash
# full suite
python -m pytest tests/

# single file
python -m pytest tests/test_reader.py

# single test
python -m pytest tests/test_reader.py::TestReadBits::test_read_8_bits

# integration tests only (needs replay files)
python -m pytest tests/ -m "integration"
```

Integration tests need real `.dem` files:

```bash
python scripts/fetch_replays.py
```

### Lint / Format / Type Check

```bash
uv run ruff check .
uv run ruff format .
uv run mypy src
```

### Docs (VitePress)

```bash
cd docs
npm install
npm run docs:dev
```

Build-only check:

```bash
cd docs
npm run docs:build
```

---

## MANDATORY: Check References Before Implementing

Do **not** implement features blindly from memory.

Before any feature or bugfix:
1. Read relevant code in `refs/manta/` first
2. Cross-check with `refs/clarity/` and `refs/parser/`
3. Verify enums, field names, message paths, and data flow
4. Then implement in idiomatic Python

Skipping this leads to common failures: wrong enum values, wrong message path, incorrect player attribution, and broken combat-log handling.

---

## Current Architecture (implemented)

### End-to-end pipeline

```text
stream.py → reader.py → sendtable.py → field_decoder.py → field_path.py → string_table.py → entities.py → parser.py → match_builder.py → combat_aggregator.py → dataframes.py → extractors/*
```

### Core modules

1. **`src/gem/stream.py`**
   - Validates `PBDEMS2` magic
   - Reads outer demo commands (tick/type/size)
   - Handles Snappy decompression

2. **`src/gem/reader.py`**
   - LSB-first bit primitives (`read_bits`, varints, `read_ubit_var`, coord/angle/normal)

3. **`src/gem/sendtable.py`**
   - Parses `CSVCMsg_FlattenedSerializer`
   - Builds serializer/field metadata tree and field models

4. **`src/gem/field_decoder.py`**
   - Decoder dispatch + quantized float support

5. **`src/gem/field_path.py`**
   - Huffman-coded field path decoding (40 ops)

6. **`src/gem/string_table.py`**
   - Create/update string tables
   - Key-history logic
   - Side tables like `instancebaseline` and `CombatLogNames`

7. **`src/gem/entities.py`**
   - Packet entities create/update/delete lifecycle
   - Baseline + delta application
   - Entity state mutation hot path
   - Field-state and field-reading logic remain in this module

8. **`src/gem/game_events.py` + `src/gem/combatlog.py`**
   - Source1 game events
   - S1 + S2 combat log ingestion into unified `CombatLogEntry`

9. **`src/gem/parser.py`**
   - Top-level replay orchestrator
   - Handles outer + inner message dispatch
   - Maintains ordering constraints (string tables before packet entities)

10. **`src/gem/match_builder.py`**
   - Assembles `ParsedMatch`
   - Wires extraction outputs into final model fields (including teamfight integration)

11. **`src/gem/combat_aggregator.py`**
   - Aggregates combat-log-derived stats (damage/healing/purchases) for match/player outputs

12. **`src/gem/dataframes.py`**
   - Converts parsed match outputs into pandas DataFrames (`parse_to_dataframe` path)

13. **`src/gem/extractors/`**
   - `players.py`, `objectives.py`, `wards.py`, `courier.py`, `draft.py`, `teamfights.py`

14. **Public API**
   - `gem.parse(path) -> ParsedMatch`
   - `gem.parse_to_dataframe(path) -> dict[str, pd.DataFrame]`
   - CLI: `python -m gem <replay.dem>`

---

## Implemented Scope Status

- **Phases 1–10**: Completed (reader/stream, schema/decode, entities/string tables, events/combat log, extraction layer, output API, gap closures including teamfights, validation/fuzz baseline)
- **Phase 11a**: Performance (Python optimizations complete; Rust extension planned/in progress)
- **Phase 11b**: Refactor/cleanup for release quality (✅ completed: modularization into `match_builder.py`, `combat_aggregator.py`, `dataframes.py`)
- **Phase 12**: Packaging/distribution (planned)

---

## High-Risk / Non-Obvious Behaviors

1. **Server info ordering**
   - `svc_ServerInfo` can arrive before send tables; preserve pending handling before entity manager init.

2. **Packet ordering**
   - Within a packet, process string table updates before packet entities so baselines are available.

3. **Combat log has two paths**
   - S1: `dota_combatlog` game event + `CombatLogNames` lookup
   - S2: direct `CMsgDOTACombatLogEntry`
   - Both must normalize to same output shape.

4. **Ward coordinate matching**
   - Do not restrict to only `CREATED`; recycled slots can produce `UPDATED` with full position.
   - Do not globally consume slot records during matching; slot reuse is expected.

5. **Teamfight logic**
   - Merge death windows using 15s (450 ticks), not 45s.
   - Participation requires hero-vs-hero involvement; avoid neutrals/illusion noise.

---

## Coding Conventions

- Preserve behavior parity with references, but write idiomatic Python
- `@dataclass` for structured value containers
- `__slots__` on hot-path objects (`BitReader`, `FieldPath`)
- Type annotations on public APIs
- Google-style docstrings for public classes/functions
- Avoid transliterating Go/Java patterns directly

---

## Fast Task Routing

| Problem | Start here |
|---|---|
| Bit parsing bug | `src/gem/reader.py` + `tests/test_reader.py` |
| Outer message/decompression issue | `src/gem/stream.py` |
| Schema/decoder mismatch | `sendtable.py` + `field_decoder.py` |
| Field-path/entity decode issue | `field_path.py` + `entities.py` |
| Combat-log mismatch | `string_table.py` + `combatlog.py` + `game_events.py` |
| Teamfight discrepancy | `extractors/teamfights.py` + `tests/test_teamfights.py` |
| Match assembly/output wiring | `parser.py` + `match_builder.py` + `dataframes.py` |
| Combat aggregation mismatch | `combat_aggregator.py` + `combatlog.py` + `extractors/players.py` |
| Proto generation issue | `scripts/compile_protos.py` |

---

## Key Scripts & Artifacts

- `scripts/compile_protos.py` — canonical protobuf generation
- `scripts/fetch_replays.py` — fetch integration replay fixtures
- `scripts/validate_opendota.py` — output diff vs OpenDota
- `tests/test_fuzz.py` — malformed/truncated replay robustness

---

## Practical Working Rules for Agents

1. Use `uv` workflows (`uv sync`, `uv run ...`) consistently.
2. Check references before code changes in parser/decoder/entity paths.
3. Make surgical edits; avoid unrelated refactors.
4. Run focused tests for touched modules before finishing.
5. For parser logic changes, prioritize regression tests around:
   - entities/string tables
   - combat log normalization
   - extractor output shape
6. Never hand-edit generated protobuf modules under `src/gem/proto/`.
