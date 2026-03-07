# AGENTS.md

This file provides guidance to agents (i.e., ADAL) when working with code in this repository.

## Project Snapshot

- **Project**: `gem` — Source 2 Dota 2 replay parser (Python)
- **Current plan status**: Early-phase implementation (see `STRATEGY.md`)
- **Package manager / env**: `uv` with local `.venv`
- **Primary reference implementations**:
  - `refs/manta/` (Go; primary behavioral reference)
  - `refs/clarity/` (Java; secondary reference)

---

## Essential Commands (Copy/Paste)

### Environment Setup

```bash
uv sync
source .venv/bin/activate
```

**Gotcha**: Run `uv sync` first so tools like `pytest`, `ruff`, `mypy`, and proto tooling exist in the environment.

### Development / Protobuf Generation

```bash
uv run python scripts/compile_protos.py
uv run python scripts/compile_protos.py --force
uv run python scripts/compile_protos.py --verbose
```

- `compile_protos.py` orchestrates protobuf generation and is the canonical workflow.
- Prefer this script over ad-hoc `protoc` commands.

### Test Commands

```bash
# full test suite
python -m pytest tests/

# single file
python -m pytest tests/test_reader.py

# single test
python -m pytest tests/test_reader.py::TestReadBits::test_read_8_bits

# integration-only tests (requires replay files)
python -m pytest tests/ -m "integration"
```

Integration tests require real `.dem` replays — fetch first:

```bash
python scripts/fetch_replays.py
```

### Lint / Format / Type Check

```bash
uv run ruff check .
uv run ruff format .
uv run mypy src
```

### Docs

```bash
uv run mkdocs serve
```

---

## Critical Gotchas (Read Before Editing)

1. **Use `uv` workflows**
   This repo assumes `uv`-managed dependencies and local virtualenv semantics.

2. **Proto toolchain version skew risk**
   `scripts/compile_protos.py` uses packaged tooling (`protoc-wheel-0` path).
   If generation fails, re-run `uv sync` first. Avoid relying on system `protoc`.

3. **Match reference behavior, not Go syntax**
   Preserve logic parity with `refs/manta`, but write idiomatic Python (no mechanical transliteration).

4. **Module dependency order matters**
   Implementation/reading order: `reader.py` → `stream.py` → `sendtable.py` → `field_decoder.py` → `field_path.py` → `string_table.py` → `entities.py`

5. **Entity system is the hot/complex path**
   Huffman-coded field paths + serializer metadata + packet entity deltas must stay consistent across modules.

6. **Coding conventions** (from `CLAUDE.md` / `STRATEGY.md`):
   - `@dataclass` for structured value containers
   - `__slots__` on hot-path classes (`BitReader`, `FieldPath`)
   - Google-style docstrings on public functions
   - Don't jump ahead of foundational parsing layers (phased plan)

---

## Non-Obvious Architecture & Data Flow

### End-to-end parsing pipeline

```
stream.py → reader.py → sendtable.py → field_path.py → entities.py
(container)  (bits)      (schema)       (Huffman paths)  (state mutations)
```

1. **Container stream** — `src/gem/stream.py`
   Validates `PBDEMS2` magic, reads outer demo commands, handles Snappy decompression.

2. **Bit-level primitives** — `src/gem/reader.py`
   LSB-first bit extraction. Core forms: `varuint32`, zigzag varint, `ubit_var`. All higher layers depend on this.

3. **Schema / serializer tree** — `src/gem/sendtable.py`
   Decodes `CSVCMsg_FlattenedSerializer` into field metadata trees. Establishes decoder metadata for live entity updates.

4. **Field-path decode** — `src/gem/field_path.py`
   Huffman-coded paths → addressable positions within serializer/entity trees. Decoder logic in `src/gem/field_decoder.py`.

5. **Entity lifecycle** — `src/gem/entities.py`
   Applies packet-entity create/update/delete deltas. Uses schema + field decoders + path decode together. Main state mutation layer.

### Combat log normalization (two-source merge)

- **S1 path**: `dota_combatlog` game event → lookup via `CombatLogNames` string table (`src/gem/string_table.py`).
- **S2 path**: `CMsgDOTACombatLogEntry` user message → direct protobuf parse.
- Both converge into a unified `CombatLogEntry` dataclass.

---

## Fast Task Routing

| Problem | Start here |
|---|---|
| Bit parsing bug | `src/gem/reader.py` + `tests/test_reader.py` |
| Outer message / decompression | `src/gem/stream.py` |
| Wrong field decode in entities | `sendtable.py` + `field_decoder.py` + `field_path.py` + `entities.py` |
| Combat log mismatch | `string_table.py` + combat-log normalization path |
| Proto mismatch / build failure | `scripts/compile_protos.py` + generated proto outputs |

### Scripts & support

- `scripts/compile_protos.py` — Canonical protobuf generation
- `scripts/fetch_replays.py` — Fetch replay data for integration tests
- `tests/fixtures/` — Small binary fixtures for deterministic unit tests
