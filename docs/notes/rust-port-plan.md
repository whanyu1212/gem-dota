# Rust Port Plan (Future Reference)

This note captures what should be ported to Rust for meaningful replay parse speedups, and what repository layout changes are expected. It is intentionally planning-only.

## Why porting only some parts is not enough

The main bottleneck is the entity update hot path, not high-level orchestration. Porting only `BitReader`/field paths usually loses performance because Python↔Rust boundary crossings are too frequent.

Target boundary: one Rust call per packet entity update batch (or per packet), not per field.

## Must-Port Scope (High ROI)

Port these together as one engine:
- Bit primitives and varints (`reader.py` hot primitives)
- Field path decoding (`field_path.py`)
- Decoder dispatch and field decode application (`field_decoder.py`, `field_reader.py`)
- Field state storage and mutation (`field_state.py`)
- Entity delta apply loop (`entities.py` update path)

## Keep in Python (for now)

- Outer replay framing/decompression orchestration (`stream.py`)
- Top-level parser flow and protobuf dispatch (`parser.py`)
- Extractors, match assembly, DataFrame/JSON/Parquet exports
- Docs, CLI, and report generation

## Foreseeable Folder Structure Changes

```text
gem/
├── src/gem/
│   ├── _engine.py           # backend selector (python vs rust)
│   ├── _engine_py.py        # current pure-python entity engine
│   ├── _engine_rust.py      # thin wrapper over compiled module
│   ├── parser.py            # orchestration stays here
│   └── stream.py
├── rust/
│   └── gem_rust/
│       ├── Cargo.toml
│       └── src/
│           ├── lib.rs
│           ├── reader.rs
│           ├── field_path.rs
│           ├── field_decoder.rs
│           ├── field_state.rs
│           └── entity_engine.rs
```

## Suggested Migration Sequence

1. Add backend interface in Python (`_engine.py`) with pure-Python default.
2. Implement Rust engine with parity tests against current outputs.
3. Route packet entity updates through Rust backend behind a feature flag.
4. Benchmark and validate correctness on fixtures and integration replays.
5. Keep pure-Python fallback for environments without compiled wheels.

