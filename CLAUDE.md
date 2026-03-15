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

### MANDATORY: Check refs before implementing

**Do not write any implementation code before reading the relevant reference files.** This is a hard rule, not a suggestion.

Before implementing any feature or fixing any bug:
1. Read the relevant file(s) in `refs/manta/` (Go — primary)
2. Cross-check with `refs/clarity/` (Java — edge cases) and `refs/parser/` (Java — output schema)
3. Verify field names, enum values, message types, and data flow against the refs
4. Only then write code

Rushing to implement without checking refs leads to wrong enum mappings, wrong message types, wrong field attributions, and hours of debugging. When in doubt, grep all three ref dirs before touching any source file.

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

### Ward coordinates — how to get 100% coverage

The combat log `ITEM` event (`item_ward_observer`, `item_ward_dispenser`, `item_ward_sentry`) records who placed a ward and when, but not where. Coordinates come from the entity stream.

**Do not** filter to `EntityOp.CREATED` only — recycled entity slots emit `UPDATED` (not `CREATED`) but still carry the full position. Record every entity event on live ward entities (excluding `DELETED`).

**Do not** globally consume entity records in the matcher — the same slot is reused across the game, so it must be matchable to multiple placements at different ticks.

Correct approach: for each combat log placement event, find the entity event with the smallest tick delta within ±60 ticks, allowing reuse. This gives 100% exact coordinates.

Reference: `refs/parser/src/main/java/opendota/processors/warding/Wards.java` — uses `m_lifeState==0` transitions instead of op type. Either works; what matters is accepting all non-DELETED events and not consuming entity records globally in the matcher.

### Smoke of Deceit — empty group edge case

Tracking smoke:
1. `ITEM` event (`inflictor_name = "item_smoke_of_deceit"`) — item consumed
2. `MODIFIER_ADD` events (`inflictor_name = "modifier_smoke_of_deceit"`, `target_is_hero = True`) — one per hero that receives the buff

Filter `MODIFIER_ADD` by `target_is_hero = True` to exclude summoned units (e.g. Beastmaster boars) from the group.

**Empty group edge case**: if the activating hero is standing inside a sentry ward's truesight radius at activation time, the smoke breaks instantly before any `MODIFIER_ADD` fires. The `ITEM` event is still recorded (item consumed) but zero modifier events follow. This is correct game behaviour — the item was wasted — not a parsing gap. Output this as a smoke usage with an empty group.

Alternative approach (refs): read the `ActiveModifiers` string table directly — each entry is a `CDOTAModifierBuffTableEntry` protobuf with a `player_ids` field (comma-separated player slots). Would give the same result for empty-group cases. Not currently implemented; requires parsing an additional string table of protobufs.

## Workflow preferences

- **Never run Bash commands in the background.** Always run foreground (blocking) so output is visible immediately. Efficiency is less important than observability.
- When writing temporary investigation scripts to `/tmp/`, delete them after use (`rm /tmp/script.py`).
- Kills by summoned units (Warlock Golem, Undying zombie, Pugna Nether Ward, etc.) should be credited to the owning hero's kill count.
- Deaths count all causes (hero, tower, creep, neutral, summon) — not just hero-dealt deaths.

## Deferred: buyback cost breakdown (reliable vs unreliable gold)

The HTML report buybacks section shows only time/hero/team. Adding a reliable/unreliable gold
cost breakdown was investigated but deferred. Key findings:

- `m_vecDataTeam.{slot}.m_iReliableGold` / `m_iUnreliableGold` on `CDOTADataRadiant/Dire`
  exist and are readable, but reflect **remaining gold after** the buyback deduction — not the
  cost paid.
- `CDOTAUserMsg_SendFinalGold` (type 514) provides per-player reliable/unreliable gold at game
  end only — not per buyback event.
- The buyback cost is not stored directly in the entity stream.

**Approaches to explore when revisiting:**
1. Event-driven sampling: hook the BUYBACK combat log entry and snapshot gold immediately before
   it fires (requires sampling outside the periodic `_maybe_sample()` loop).
2. Formula approximation: `cost ≈ 200 + net_worth / 12` (capped ~2100 in Dota 7.x). Net worth
   at buyback tick is available from the nearest `PlayerStateSnapshot`.

**Files to change:** `extractors/_snapshots.py`, `extractors/players.py`, `models.py`,
`match_builder.py`, `examples/report/html_sections.py`. See `STRATEGY.md` section 7b+.

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

## Implementation status

| Phase | Scope | Status |
|---|---|---|
| 1 | `reader.py`, `stream.py` | ✅ Complete |
| 2 | `sendtable.py`, `field_decoder.py`, `field_path.py` | ✅ Complete |
| 3 | `string_table.py`, `entities.py`, `game_events.py`, `combatlog.py`, `parser.py` | ✅ Complete |
| 4 | `constants.py` + bundled `src/gem/data/` JSON assets | ✅ Complete |
| 5 | `extractors/players.py`, `objectives.py`, `wards.py` | ✅ Complete |
| 6 | `models.py`, `__init__.py` (`parse()`/`parse_to_dataframe()`), `__main__.py` (CLI) | ✅ Complete |
| 7 | Rune pickups, buybacks, aegis, lane heatmaps, chat, purchase log, movement heatmap example | ✅ Complete |
| 8 | `extractors/courier.py`, `extractors/draft.py`, ability levels on snapshots, stun duration | ✅ Complete |
| 9 | Teamfights | ✅ Complete |
| 10 | Validation (`scripts/validate_opendota.py`), fuzz tests (`test_fuzz.py`), Steam API example | ✅ Complete |
| 11 | Performance — Python quick-wins (struct.unpack fast path, flat Huffman table) | ✅ Complete |
| 11b | Refactor & Cleanup — API surface, pyproject.toml metadata, tests, entity typed getters | ✅ Complete |
| 12 | Docs & README — bottom-up technical guide (`understanding/` 10 pages), guides, API reference | 🚧 In Progress |
| 13 | Distribution — PyPI packaging, CI/CD | 🚧 Planned |
| 14 | Rust extension (PyO3 + maturin) — full entity system in Rust for 3–5× speedup | 🚧 Deferred |

## Test files

| File | Covers |
|---|---|
| `test_reader.py` | `BitReader` primitives |
| `test_stream.py` | `DemoStream` outer message loop |
| `test_sendtable.py` | Send table / serializer parsing |
| `test_field_decoder.py` | All field type decoders |
| `test_field_path.py` | Huffman field path ops |
| `test_field_path_ops.py` | All 40 field path op functions |
| `test_string_table.py` | String table create/update |
| `test_string_table_extended.py` | Key history, value compression, handle_create/update edge cases |
| `test_entities.py` | Entity lifecycle and typed getters |
| `test_game_events.py` | Game event schema and dispatch |
| `test_combatlog.py` | S1 and S2 combat log paths |
| `test_extractors.py` | `PlayerExtractor`, `ObjectivesExtractor`, `WardsExtractor` |
| `test_ability_courier_draft_stuns.py` | Ability levels, `CourierExtractor`, `DraftExtractor`, stun duration |
| `test_constants.py` | `constants.py` — all lookup functions |
| `test_draft_extractor.py` | `DraftExtractor` — resolution tiers, finalize, idempotency |
| `test_teamfights.py` | `detect_teamfights` — window detection, stat attribution |
| `test_fuzz.py` | Robustness: malformed/truncated/empty inputs don't hang or crash |

Fixtures go in `tests/fixtures/`. Real `.dem` files for integration tests are marked `@pytest.mark.integration` and `@pytest.mark.slow`.

## Examples

| Script | Description |
|---|---|
| `examples/match_report.py` | Full match dashboard (Draft, Combat, Vision, Teamfights, Economy) |
| `examples/extraction_demo.py` | Developer guide for combat log extraction and entity polling |
| `examples/steam_match_info.py` | Fetch match info from Steam API and display with Rich tables |

Hero and item icons for `match_report.py` are downloaded separately — not committed or shipped in the package:

```bash
python scripts/fetch_hero_icons.py   # downloads to src/gem/data/hero_icons/
```
