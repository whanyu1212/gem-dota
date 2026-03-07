# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Activate the virtual environment first (required)
source .venv/bin/activate

# Run all tests
python -m pytest tests/

# Run a single test file
python -m pytest tests/test_reader.py

# Run a single test by name
python -m pytest tests/test_reader.py::TestReadBits::test_read_8_bits

# Run with coverage
python -m pytest tests/ --cov=gem --cov-report=term-missing

# Skip slow/integration tests (requires real .dem files)
python -m pytest tests/ -m "not slow and not integration"

# Install dev dependencies
uv sync --group dev
```

## Architecture

Read `STRATEGY.md` for the full implementation plan. The short version:

**gem** parses Dota 2 Source 2 `.dem` replay files for DS/ML use. The binary format is a stream of outer messages (varuint command + tick + size + payload), where payloads are protobuf messages. Entity state is reconstructed from an incremental delta system driven by a schema (send tables) decoded at replay start.

### Module dependency order (implement and read in this order)

```
reader.py          ← BitReader, all bit/byte/varint primitives
stream.py          ← outer message loop, Snappy decompress, magic check
sendtable.py       ← serializer + field tree (requires reader)
field_decoder.py   ← type-dispatch decoders + QuantizedFloatDecoder
field_path.py      ← Huffman-coded field path ops (requires reader)
string_table.py    ← incremental key-history string tables
entities.py        ← entity create/update/delete lifecycle + state
game_events.py     ← game event schema + typed dispatch
combatlog.py       ← S1 (game event) + S2 (user message) combat log
models.py          ← ParsedMatch, ParsedPlayer output dataclasses
parser.py          ← top-level orchestrator wiring everything together
extractors/        ← per-tick polling of entity state for output
```

### Reference implementations (cloned at `refs/`)

| Directory | Language | Role |
|---|---|---|
| `refs/manta/` | Go | Primary translation reference for all binary parsing logic |
| `refs/clarity/` | Java | Correctness authority for edge cases; combat log two-path handling |
| `refs/parser/` | Java | Output schema authority (`Entry.java`, `CreateParsedDataBlob.java`) |

When translating from Manta, the Go file maps 1:1 to the Python module:
`manta/reader.go` → `reader.py`, `manta/entity.go` → `entities.py`, etc.

### ReplayParser — the main entry point (Phase 3+)

`parser.py` wires all subsystems together. Key implementation details:

- **Outer vs inner messages**: `DemoStream` yields outer `EDemoCommands` frames. `DEM_Packet`/`DEM_SignonPacket`/`DEM_FullPacket` contain a `CDemoPacket` whose `.data` is a packed stream of `{ubit_var type_id, varuint32 size, bytes}` inner net messages — these must be unpacked separately with `BitReader`.
- **`svc_ServerInfo` arrives before `DEM_SendTables`**: the `_pending_server_info` pattern caches it and applies it immediately after the entity manager is created in `_on_send_tables`.
- **Inner message priority**: string table messages (priority -10) are sorted before `svc_PacketEntities` (+5) within the same packet to ensure baselines are ready before entity deltas are applied.
- **Outer IDs**: `DEM_SendTables=4`, `DEM_ClassInfo=5`, `DEM_Packet=7`, `DEM_SignonPacket=8`, `DEM_FullPacket=13`
- **Inner IDs**: `net_Tick=4`, `svc_ServerInfo=40`, `svc_CreateStringTable=44`, `svc_UpdateStringTable=45`, `svc_PacketEntities=55`

### The entity system (most complex part)

Entities are game objects (heroes, towers, items, game rules). Their schema is defined in `CDemoSendTables` → `CSVCMsg_FlattenedSerializer`, parsed into a tree of `Serializer` → `Field` objects. Each field has a decoder function resolved once at schema-parse time.

Entity state arrives as `CSVCMsg_PacketEntities`. Each packet carries a list of (index, 2-bit command, field deltas). Field deltas use Huffman-coded field paths (40 ops, `field_path.py`) to address into the serializer tree, then the field's decoder reads the value from the bit stream.

The `instancebaseline` string table holds default field values per class — applied first when an entity is created, before the packet's own deltas.

### Combat log — two ingestion paths

- **S1 (older replays)**: arrives as `dota_combatlog` game event via `CMsgSource1LegacyGameEvent`. Names are integer indices resolved via the `CombatLogNames` string table.
- **S2 (newer replays)**: arrives as `CMsgDOTACombatLogEntry` user message with names already resolved.

Both paths must produce the same `CombatLogEntry` output. See `refs/clarity/src/main/java/skadistats/clarity/processor/gameevents/CombatLog.java`.

## Code Style

- **Not a direct translation** — code must be idiomatic Python, not Go/Java transliterated
- `@dataclass` for value types; `enum.IntFlag` for bitmasks like `EntityOp`
- `__slots__` on hot-path objects (`BitReader`, `FieldPath`)
- `struct.unpack` fast paths for byte-aligned reads in `BitReader`
- `match` statements (Python 3.10+) for multi-branch dispatch
- All public functions and classes must have **Google-style docstrings** (autoDocstring format):
  ```python
  def example(x: int) -> str:
      """One-line summary.

      Args:
          x: Description of x.

      Returns:
          Description of return value.

      Raises:
          ValueError: When x is negative.
      """
  ```
- Module-level docstrings must cite the reference file, e.g. `Reference: manta/reader.go`
- Private methods (`_foo`) and test helpers do not require docstrings

## Protobuf

Generated protobuf classes live in `src/gem/proto/dota2/`. Do not hand-edit them. To regenerate:

```bash
python scripts/compile_protos.py
```

Key message classes used throughout the parser:
- `demo_pb2` — `CDemoSendTables`, `CDemoClassInfo`, `CDemoFullPacket`
- `netmessages_pb2` — `CSVCMsg_PacketEntities`, `CSVCMsg_CreateStringTable`, `CSVCMsg_FlattenedSerializer`
- `dota_commonmessages_pb2` — `CMsgDOTACombatLogEntry`
- `dota_usermessages_pb2` — `CDOTAUserMsg_*`

## Tests

Tests are written against the public API of each module and fail with `ModuleNotFoundError` until the corresponding module is implemented. This is by design — the test suite drives implementation phase by phase.

Fixtures (small binary blobs for unit tests) go in `tests/fixtures/`. Real `.dem` files for integration tests should be fetched with `scripts/fetch_replays.py` and are marked `@pytest.mark.integration`.
