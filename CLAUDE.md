# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

This project is managed with **`uv`**. Prefer `uv run` — it uses the project's
`.venv` without a manual `source .venv/bin/activate`. (`CONTRIBUTING.md` has the
fuller contributor workflow; the list below is the day-to-day short version.)

```bash
# Install project + dev dependencies
uv sync --group dev

# Run default test suite (skips slow/integration markers via pyproject.toml)
uv run pytest

# Run all tests, including slow/integration markers
uv run pytest -m ""

# Run a single test file
uv run pytest tests/binary/test_reader.py

# Run a single test by name
uv run pytest tests/binary/test_reader.py::TestReadBits::test_read_8_bits

# Run with coverage
uv run pytest --cov=gem --cov-report=term-missing

# Explicit fast loop — equivalent to the default marker filter
uv run pytest -m "not slow and not integration"

# Integration suite (requires replay fixtures)
uv run pytest -m integration

# Broader remote draft integration sample (downloads/parses 5 pro replays)
GEM_DRAFT_INTEGRATION_FULL=1 uv run pytest tests/test_draft_integration.py -m integration

# Lint, format, type-check (run before committing)
uv run ruff check src/ tests/
uv run ruff format src/ tests/
uv run mypy src/gem/

# Regenerate protobuf modules after updating proto_definitions/
uv run python scripts/compile_protos.py

# Docs — VitePress lives in docs/ (Node-based, see "Docs" below)
cd docs && npm install && npm run docs:dev
```

## Architecture

> **Note:** `STRATEGY.md` (the original implementation plan referenced in older
> versions of this file) has been removed. The living architecture references are
> now `docs/architecture.md`, `docs/replay-parser.md`, and the `docs/deep-dives/`
> pages. `CHANGELOG.md` is the authoritative record of what shipped in each release.

**gem** parses Dota 2 Source 2 `.dem` replay files for DS/ML use. It is published
to PyPI as **`gem-dota`** (import name `gem`). The binary format is a stream of
outer messages (varuint command + tick + size + payload), where payloads are
protobuf messages. Entity state is reconstructed from an incremental delta system
driven by a schema (send tables) decoded at replay start.

### Module dependency order (read in this order)

Low-level binary parsing → entity reconstruction → extraction → output.

```
binary/reader.py          ← BitReader, all bit/byte/varint primitives
binary/stream.py          ← outer message loop, Snappy decompress, magic check
schema/sendtable/         ← serializer + field tree package (requires reader)
schema/field_decoder/     ← type-dispatch decoders + QuantizedFloatDecoder
schema/field_path/        ← Huffman-coded field path package (requires reader)
schema/field_state.py     ← nested mutable field-value tree (mirrors manta/field_state.go)
schema/field_reader.py    ← field decoder dispatch + entity field reading (mirrors manta/field_reader.go)
state/string_table.py           ← incremental key-history string tables
state/entities.py               ← entity create/update/delete lifecycle + state
state/game_events.py            ← game event schema + typed dispatch
combat/log.py              ← S1 (game event) + S2 (user message) combat log
combat/aggregator.py      ← per-player combat log accumulation → damage/heal/kill/purchase tallies
parser.py                 ← top-level orchestrator wiring everything together
extractors/               ← per-tick polling of entity state for output (see below)
catalog/                  ← hero/item/ability/league/XP/map lookups over bundled src/gem/data/ JSON
constants.py              ← backwards-compatible facade over catalog lookups
api.py                    ← high-level parse/export helpers exposed by the public package API
results/models.py         ← ParsedMatch, ParsedPlayer, ChatEntry, NeutralItemFoundEvent dataclasses
results/assembly.py       ← wires extractor outputs into ParsedMatch
results/dataframes.py     ← converts ParsedMatch to pandas DataFrames
reports/                  ← self-contained HTML report generation from ParsedMatch
analysis/spatial.py       ← position, nearby-hero, and net-worth lookup helpers
analysis/combat.py        ← ability-hit grouping and teamfight lookup helpers
analysis/abilities.py     ← ability-level lookup helpers
analysis/vision.py        ← geometry-based vision approximation helpers
analysis/map_context.py   ← objective-aware map-context buckets (experimental farming analysis)
analysis/roshan.py        ← post-parse Roshan conversion records (did a Rosh convert to a win?)
replays/batch.py          ← bulk replay parsing (parse_many, parallel workers)
replays/fetch.py          ← download + decompress replays from OpenDota/Valve CDN
cli.py                    ← CLI implementation
__init__.py               ← public API re-export surface
__main__.py               ← python -m gem adapter
```

The **`extractors/`** package polls entity/combat-log state during parse:

```
extractors/players.py       ← per-player snapshots/time-series (gold, XP, net worth, pos)
extractors/objectives.py    ← tower/barracks/Roshan kills, aegis events
extractors/wards.py         ← ward placements + entity-stream coordinate matching
extractors/lane.py          ← lane-position heatmaps
extractors/courier.py       ← courier state
extractors/draft.py         ← pick/ban resolution (three-tier hero-ID resolution)
extractors/teamfights.py    ← teamfight window detection + per-fight stat attribution
extractors/_snapshots.py    ← shared snapshot dataclasses/sampling helpers
```

### Reference implementations (cloned at `refs/`)

| Directory | Language | Role |
|---|---|---|
| `refs/manta/` | Go | Primary translation reference for all binary parsing logic |
| `refs/clarity/` | Java | Correctness authority for edge cases; combat log two-path handling |
| `refs/parser/` | Java | Output schema authority (`Entry.java`, `CreateParsedDataBlob.java`) |

When translating from Manta, the Go file maps closely to the Python module:
`manta/reader.go` → `binary/reader.py`, `manta/field_reader.go` →
`schema/field_reader.py`, `manta/entity.go` → `state/entities.py`, etc.

### MANDATORY: Check refs before implementing

**Do not write any implementation code before reading the relevant reference files.** This is a hard rule, not a suggestion.

Before implementing any feature or fixing any bug:
1. Read the relevant file(s) in `refs/manta/` (Go — primary)
2. Cross-check with `refs/clarity/` (Java — edge cases) and `refs/parser/` (Java — output schema)
3. Verify field names, enum values, message types, and data flow against the refs
4. Only then write code

Rushing to implement without checking refs leads to wrong enum mappings, wrong message types, wrong field attributions, and hours of debugging. When in doubt, grep all three ref dirs before touching any source file.

### Public API — how the library is used

`src/gem/api.py` implements the high-level helpers and `src/gem/__init__.py`
defines the supported surface (`__all__`) by re-exporting them. Most users never
touch the parser directly; they call `gem.parse()` and work with `ParsedMatch`:

```python
import gem

match = gem.parse("replay.dem")          # -> ParsedMatch
df = gem.parse_to_dataframe("replay.dem") # -> pandas DataFrame
gem.parse_to_json("replay.dem", "out.json")
gem.parse_to_parquet("replay.dem", "out.parquet")
matches = gem.parse_many([...])           # bulk, parallel workers
```

Headline exports (see `__all__` for the full list):
- **Parse:** `parse`, `parse_to_dataframe`, `parse_to_json`, `parse_to_parquet`,
  `parse_many*`, `to_dict`/`to_json`/`to_parquet`, `ParseResult`
- **Models:** `ParsedMatch`, `ParsedPlayer`, `ChatEntry`, `NeutralItemFoundEvent`
- **Analysis helpers (post-parse):** `find_player`, `position_at_tick`,
  `net_worth_at`, `teamfight_at_tick`, `heroes_near`, `ability_level_at_tick`,
  `is_active_teamfight_participant`, `estimate_vision`, `ward_vision_impact`
- **Experimental:** `build_map_context_timeline`, `score_camp_visit_context`,
  `build_rosh_conversions`, `RoshConversion`
- **Replay fetch:** `fetch_replay`, `fetch_replay_url`, `download_and_decompress`
- **Catalog/constants:** `catalog` (grouped lookup modules) and `constants`
  (compatibility namespace of hero/item/ability lookups)

The CLI is `python -m gem`; `__main__.py` is a small adapter over `gem.cli`.

### ReplayParser — the internal orchestrator

`parser.py` wires all subsystems together. Key implementation details:

- **Outer vs inner messages**: `DemoStream` yields outer `EDemoCommands` frames. `DEM_Packet`/`DEM_SignonPacket`/`DEM_FullPacket` contain a `CDemoPacket` whose `.data` is a packed stream of `{ubit_var type_id, varuint32 size, bytes}` inner net messages — these must be unpacked separately with `BitReader`.
- **`svc_ServerInfo` arrives before `DEM_SendTables`**: the `_pending_server_info` pattern caches it and applies it immediately after the entity manager is created in `_on_send_tables`.
- **Inner message priority**: string table messages (priority -10) are sorted before `svc_PacketEntities` (+5) within the same packet to ensure baselines are ready before entity deltas are applied.
- **Outer IDs**: `DEM_SendTables=4`, `DEM_ClassInfo=5`, `DEM_Packet=7`, `DEM_SignonPacket=8`, `DEM_FullPacket=13`
- **Inner IDs**: `net_Tick=4`, `svc_ServerInfo=40`, `svc_CreateStringTable=44`, `svc_UpdateStringTable=45`, `svc_PacketEntities=55`
- **Combat log S2** is inner message type **554** (`DOTA_UM_CombatLogDataHLTV`) — a *direct* `CMsgDOTACombatLogEntry`, NOT wrapped in `svc_UserMessage` and NOT `CDOTAUserMsg_CombatLogBulkData`. The class lives in `dota_shared_enums_pb2`, not `dota_commonmessages_pb2`.

### The entity system (most complex part)

Entities are game objects (heroes, towers, items, game rules). Their schema is defined in `CDemoSendTables` → `CSVCMsg_FlattenedSerializer`, parsed into a tree of `Serializer` → `Field` objects. Each field has a decoder function resolved once at schema-parse time.

Entity state arrives as `CSVCMsg_PacketEntities`. Each packet carries a list of (index, 2-bit command, field deltas). Field deltas use Huffman-coded field paths (40 ops, `schema/field_path/`) to address into the serializer tree, then the field's decoder reads the value from the bit stream.

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

### Gold / XP field sources — critical distinction

Three different gold/XP fields exist; using the wrong one silently produces wrong curves.

| Field | Entity | Behaviour | Use for |
|---|---|---|---|
| `m_iGold` | `CDOTAPlayerController` | Spendable cash — goes up *and down* | `gold_t` (current cash) |
| `m_iTotalEarnedGold` | `CDOTA_DataRadiant/Dire` | Monotonically increasing | `radiant_gold_adv`, `total_earned_gold_t` |
| `m_iCurrentXP` | hero entity (`CDOTA_Unit_Hero_*`) | Resets to 0 on each level-up | per-level XP display |
| `m_iTotalEarnedXP` | `CDOTA_DataRadiant/Dire` | Monotonically increasing | `radiant_xp_adv` |

Using `m_iGold` for advantage curves is wrong because spendable gold drops on every
purchase. Client replays name the data class `CDOTA_DataRadiant`/`CDOTA_DataDire`
(with underscore); HLTV uses `CDOTADataRadiant`/`CDOTADataDire` — both are handled.
Reference: `refs/parser/Parse.java` (`m_vecDataTeam.%i.m_iTotalEarnedGold/XP`).

### Neutral item found events

`DOTA_UM_FoundNeutralItem` user messages are parsed into `NeutralItemFoundEvent`
(see `results/models.py`): `player_id`, `item_ability_id` → `item_key`, `item_tier`,
plus enhancement/trinket fields. Item ability IDs are resolved against the bundled
constants; new tiers/IDs are covered by `test_audit_opendota_fixture_constants.py`.

### Camp zones & nearby-gold attribution

Neutral-camp analysis lives in `analysis/map_context.py` plus the bundled data assets
`src/gem/data/camp_zones.json`, `neutral_camps.json`, and `map_constants.json`.
`camp_zones.json` carries world bounds and per-type ellipse geometry; neutral
deaths are grouped into camp zones by world position.

**Nearby-gold attribution fix (0.2.8):** when attributing `GOLD` combat-log events
to a camp, ignore unscoped `GOLD` events whose attacker *and* target names are both
absent — these are not camp-specific and otherwise inflate camp summaries.
Audit tooling: `scripts/audit_camp_annotations.py`.

### Roshan conversion analysis

`analysis/roshan.py` (`build_rosh_conversions(match)`) is a **post-parse** helper
that turns existing facts (Roshan kills, aegis events, teamfights, wards,
objectives, buybacks, movement) into per-Roshan `RoshConversion` records answering
"did this Roshan convert into fights / objectives / map control / a closing
sequence?" Key time windows (all in ticks at 30/sec): aegis duration 5 min,
immediate-outcome window 180 s, event-association window 30 s. It reads only
`ParsedMatch`, so it needs no parser changes to extend.

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

**Files to change:** `extractors/_snapshots.py`, `extractors/players.py`,
`results/models.py`, `results/assembly.py`, `reports/_sections.py`.

## Code Style

- **Not a direct translation** — code must be idiomatic Python, not Go/Java transliterated
- Python 3.10+, 4-space indentation, type hints on public APIs
- `snake_case` for functions/variables/modules; `PascalCase` for classes/dataclasses
- Keep parser changes surgical — avoid unrelated refactors in the same change
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

## Commit & PR guidelines

- Short, imperative commit messages (e.g. `fix draft hero id normalization`).
- Keep each commit scoped to one concern.
- Add focused regression tests with parser changes — especially for string-table /
  entity ordering, combat-log normalization, and extractor output shape. Run the
  touched modules' tests before opening a PR.
- **Update `CHANGELOG.md` (`[Unreleased]`) in the same PR as the change.** Any
  user-visible addition, fix, or behavior change (new `ParsedMatch`/`ParsedPlayer`
  field, new output, corrected attribution, etc.) gets an entry under
  `[Unreleased] > Added`/`Fixed`/`Changed` as part of the feature PR — not as a
  later sweep. `CHANGELOG.md` is the authoritative per-release record, so a stale
  or missing entry is a real defect (e.g. a "not reproduced" note left in after
  the feature shipped is worse than no note). When a change supersedes an existing
  `[Unreleased]` note, correct that note rather than appending a contradicting one.
- PRs should include: summary, rationale, test commands run, and results. Link
  issues when relevant; include screenshots for docs/UI changes. The repo ships a
  PR template with release-hygiene and parser-safety checks.

## Security & configuration

- Keep secrets out of the repo — `STEAM_API_KEY` via environment variables only.
- Do not commit large replay artifacts unless explicitly required for a test fixture.
- For parser-logic changes, verify against `refs/manta/` first, then cross-check
  `refs/clarity/` and `refs/parser/` (see "Check refs before implementing" above).

## Protobuf

Generated protobuf classes live in `src/gem/proto/`. Do not hand-edit them.
`.proto` sources live in `proto_definitions/`. To regenerate:

```bash
uv run python scripts/compile_protos.py
```

Key message classes used throughout the parser:
- `demo_pb2` — `CDemoSendTables`, `CDemoClassInfo`, `CDemoFullPacket`
- `netmessages_pb2` — `CSVCMsg_PacketEntities`, `CSVCMsg_CreateStringTable`, `CSVCMsg_FlattenedSerializer`
- `dota_shared_enums_pb2` — `CMsgDOTACombatLogEntry` (S2 combat log; *not* in `dota_commonmessages_pb2`)
- `dota_usermessages_pb2` — `CDOTAUserMsg_*` (chat, rune, found-neutral-item, etc.)

## Status

Current version: **0.3.0** (see `pyproject.toml` and `CHANGELOG.md`).

The full parsing pipeline and all extractors are complete and stable: binary
reader, entity system, combat log (S1+S2), string tables, every extractor, the
`ParsedMatch` output model, DataFrame/JSON/Parquet export, bulk parsing, and
replay fetch. Recent work is feature/data refreshes (neutral items, camp-zone
annotations, Roshan conversion, OpenDota validation fixtures) rather than new
core subsystems.

In flight / deferred:
- **Distribution** — PyPI packaging + CI/CD (`gem-dota` on PyPI). 🚧
- **Rust extension** (PyO3 + maturin) for a 3–5× speedup. Deferred.

`CHANGELOG.md` is the per-release record; consult it before assuming a feature's
state rather than trusting a static table here.

## Tests

~50 test files in `tests/`, conventionally one `test_<module>.py` per source
module or subsystem. Low-level binary tests are grouped under `tests/binary/`
(e.g. `tests/binary/test_reader.py` → `binary/reader.py`), while broader
subsystems stay flat when that is the established pattern (e.g.
`test_wards_extractor.py` → `extractors/wards.py`). Newer additions cover `analysis/map_context.py`,
`analysis/roshan.py`, neutral-item parsing, camp zones, and the audit/fetch
scripts (`test_audit_camp_annotations.py`, `test_audit_opendota_fixture_constants.py`,
`test_fetch_opendota_fixture.py`, `test_fetch_icons.py`, `test_render_camp_zones_overlay.py`).

- Fixtures live in `tests/fixtures/`; shared config in `tests/conftest.py`.
  Keep committed replay fixtures truncated. Full replay fixtures should be
  local/ignored OpenDota downloads under `tests/fixtures/opendota/`.
  Map/reference images for examples, reports, and camp-zone tooling live under
  `assets/maps/`, not `tests/fixtures/`.
- `uv run pytest` skips `slow` and `integration` markers by default so local
  checks do not fetch or parse large replay files accidentally. Use `-m ""` to
  include every marker category in a full local run.
- Real `.dem` files are needed only for tests marked `@pytest.mark.integration`
  and/or `@pytest.mark.slow` — skip them in the fast loop with
  `-m "not slow and not integration"`.
- `tests/test_draft_integration.py` is intentionally a one-replay remote smoke
  test by default; set `GEM_DRAFT_INTEGRATION_FULL=1` when you need the broader
  five-replay OpenDota sample.
- Markers are declared in `pyproject.toml` under `[tool.pytest.ini_options]`.

## Examples

| Script | Description |
|---|---|
| `examples/quickstart.py` | Minimal: parse a replay, print per-minute gold/XP |
| `examples/match_report.py` | Full HTML match dashboard (Draft, Combat, Vision, Teamfights, Economy, Roshan Conversion) |
| `examples/extraction_demo.py` | Developer guide for combat-log extraction and entity polling |
| `examples/steam_match_info.py` | Fetch match info from the Steam API, display with Rich tables |

Report generation lives in `src/gem/reports/`; `examples/match_report.py` is a
thin wrapper around `gem.reports.write_html_report()`.

Hero and item icons for reports are downloaded separately — not committed or
shipped in the package (the fetch scripts skip unchanged assets):

```bash
uv run python scripts/fetch_hero_icons.py   # -> src/gem/data/hero_icons/
uv run python scripts/fetch_item_icons.py   # -> src/gem/data/item_icons/
```

A sample HTML report lives in `docs/reports/` (`ti14_finals_g3_xg_vs_falcons_report.html`).

## Docs

Documentation is a **VitePress** site under `docs/` (CI builds it via
`.github/workflows/docs.yml`). The API reference is generated from docstrings.

```bash
cd docs
npm install
npm run docs:dev      # local dev server (regenerates API reference first)
npm run docs:build    # production build -> docs/.vitepress/dist
```

Key pages: `docs/index.md`, `docs/architecture.md`, `docs/guides/`,
`docs/deep-dives/`, `docs/cookbook/`, `docs/experimental/`.

## Related docs in repo root

This file (`CLAUDE.md`) is the single source of truth for working in this repo;
`AGENTS.md` is a thin pointer back to it for tools that look for that filename.

- `CONTRIBUTING.md` — dev setup, lint/format/type-check/test workflow, PR checklist.
- `CHANGELOG.md` — authoritative per-release feature/fix record.
- `README.md` — user-facing overview and install instructions.
