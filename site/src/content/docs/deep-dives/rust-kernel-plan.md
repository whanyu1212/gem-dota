# Rust Kernel Plan

gem is pure Python, and most of a parse is spent in one small, busy loop: decoding
entity updates. This page is the plan for moving that loop into an optional native
extension, written in Rust with [PyO3](https://pyo3.rs) and
[maturin](https://www.maturin.rs). It collects what each stop of the
"How Entities Are Decoded" series measured and learned, and it builds on the
[final Python parser profile](parser-profile-2026-09.md), which chose the first
native boundary.

**Status: a plan, not an implementation.** No speedup is promised. The numbers
below are upper bounds, used to decide what is worth building.

## The short version

- Port **one loop**: decoding and applying entity updates. First `read_fields()`
  (stage 1), then the per-entity packet loop around it (stage 2).
- Port **nothing else** for now. The file reader, decompression, message
  framing, the schema build, extractors, and result assembly stay in Python.
- Keep it **optional**. Without the extension, gem runs the same Python code as
  today, and that code stays the readable reference implementation.
- **Expected gain:** at most about 2× (stage 1) to 2.5× (both stages) for
  `gem.parse()`, and about 3× to 4.5× for the core parse. Realistic gains are lower. Bulk users already scale across cores
  with `gem.parse_many()`; the kernel cuts per-replay CPU time.

## Where the time goes

One 99-minute replay (`8855242704`), timed with lightweight wrappers around each
layer. Wrapper overhead adds about 4 seconds, so read the shares as approximate.
The core parse runs the parser without gem's extractors; `gem.parse()` runs
everything.

| Layer | Core parse | `gem.parse()` |
|---|---:|---:|
| `read_fields()`: field paths, values, state writes ([parts 2–4](entity-field-paths.md)) | 74.4 s (65%) | 76.8 s (50%) |
| Per-entity loop: slots, commands, creating entities ([part 5](entity-lifecycle.md)) | 15.1 s (13%) | 15.6 s (10%) |
| Calling handlers (a few of the parser's own in the core parse; gem's extractors in `gem.parse()`) | 3.8 s (3%) | 22.7 s (15%) |
| Everything else: file, decompression, messages, combat log, string tables, results, and the wrapper overhead | ~21 s (18%) | ~37 s (24%) |
| **Total (timed)** | **114.4 s** | **152.2 s** |

Inside `read_fields()`, about 44% of the time decodes field paths, about 43%
decodes values and runs the loop, and about 12% writes into `FieldState`. The
v0.8.0 profile found the same shape with a sampling profiler on two other replays:
`read_fields()` was 71–72% of the core parse and 54–59% of the public one.

## What not to port

Each stop of the series asked whether its code was worth porting on its own:

| Code | Share | Verdict |
|---|---:|---|
| Reading the file and Snappy decompression (`binary/stream.py`) | ~1% | No. Decompression is already native code. |
| Splitting packets into messages (`binary/packet.py`) | ~6% | No. A pure-Python change may help first: skip copying payloads of message types gem ignores. On the 99-minute replay, voice data alone is 1 million messages and 38% of the bytes (the gain is unmeasured). |
| `BitReader` on its own | 13–17% | No. It's called 34 million times from Python on a 23-minute replay; moving it alone would add a language crossing to every call. It pays off only inside a larger kernel. |
| Building the schema (`schema/sendtable/`) | 0.07 s once | No. Its output becomes the kernel's compiled schema. |
| Extractors, the combat log, and result assembly | most of the last two rows of `gem.parse()` | No. This is where gem's features live and change, and it is what the docs promise readers can follow end to end. |

## The kernel, in two stages

### Stage 1: `read_fields()`

The v0.8.0 profile selected this boundary, and every later measurement agrees.
One call decodes one entity update: all its field paths, then a value for each,
written into the entity's `FieldState`. The kernel would take the same inputs as
today's function (the bitstream position, the class's serializer, and the
`FieldState`) and return with the reader advanced.

It is called 12.6 million times on the 99-minute replay, so the per-call cost of
crossing from Python into Rust matters and has to be measured in the prototype.

### Stage 2: the per-entity packet loop

The loop in `EntityManager` that reads each change's slot and command, creates
entities, and calls `read_fields()` adds another 13% of the core parse. The first
assessment rejected moving it, because handlers might then see a different state.
That concern doesn't hold. A native loop can call back into Python after each
entity, in packet order, exactly as gem does now (the same order as Clarity).
Handlers see the same state; only the loop between them becomes native.

Stage 2 also cuts the number of crossings from one per entity update to one per
packet, plus one for each entity update that has handlers to call. The core parse
has almost none; in `gem.parse()`, 84% of entity updates reach a handler, so that
many callbacks remain.

### What each stage could gain

Two illustrations. "Free" assumes the ported code takes no time at all, which
is the ceiling. "10× faster" is a plausible native speed for this kind of
bit-level work, but it hasn't been measured.

| | Core, free | Core, 10× faster | `gem.parse()`, free | `gem.parse()`, 10× faster |
|---|---:|---:|---:|---:|
| Stage 1 | 2.9× | 2.4× | 2.0× | 1.8× |
| Stages 1 and 2 | 4.6× | 3.4× | 2.5× | 2.2× |

The limit for `gem.parse()` is everything that stays in Python: extractors, the
combat log, and result assembly, about 40% of its time. So after the kernel, the
next gains would come from Python-side work in those areas, not from more Rust.

## What the kernel must keep exactly

The series turned up rules that any second implementation must follow. Most are
now pinned by tests, which the kernel's differential tests should reuse.

| Rule | Where it comes from |
|---|---|
| The 40 field-path operations and their Huffman codes are identical to Manta's. | [Part 2](entity-field-paths.md); `tests/test_field_path.py` pins all 40 codes |
| All of an update's paths are read before any of its values. | The wire format; Manta, Clarity |
| Each field's decoder is fixed when the schema is built, after build-specific patches. | [Part 1](entity-schema.md), [Part 3](entity-field-decoders.md) |
| Quantized-float flag decisions use 32-bit float arithmetic; decoded values stay 64-bit. | [Part 3](entity-field-decoders.md); `tests/test_field_decoder.py` checks 28 real setups against Manta |
| 32-bit varints wrap to 32 bits (Valve's semantics). | `tests/binary/test_reader.py` |
| `FieldState`: grows to `max(i + 2, 2 × size)`; a value never replaces a node; a length on an array node trims it; reading a node returns its length or `True`. | [Part 4](entity-field-state.md); `tests/test_field_state.py`, `tests/test_entity_arrays_integration.py` |
| The paths decoded by the last update are recorded, for changed-field filters. | [Part 4](entity-field-state.md) |
| A new entity gets its class baseline, then the packet's values. | [Part 5](entity-lifecycle.md) |
| Handlers run after each entity's change, in packet order. | [Part 5](entity-lifecycle.md) |
| Errors on truncated or malformed data, and how far the reader has advanced, match Python. | v0.8.0 profile; partial updates can't simply be retried |

Four decoders account for 92% of value decodes (quantized floats 27%, signed
varints 25%, unsigned varints 21%, raw 32-bit floats 20%), so a native decoder
table can start small and fall back to Python for rare decoder types.

## Interface sketch

1. **Compile the schema once per replay.** After send tables are parsed and the
   game build is known, walk gem's `Serializer`/`Field` tree and hand Rust a
   compact, read-only description of it: field models, child classes, and each
   field's decoder with its parameters (bit counts, ranges, flags). Fields whose
   decoder Rust doesn't know are marked, so their updates fall back to Python
   before any bits are consumed.
2. **Stage 1 call:** `read_fields(buffer, bit_position, class_handle, field_state)`
   decodes one update, writes Python values into the existing `FieldState` lists,
   and returns the new bit position. Keeping Python objects means every stored
   value is still a Python `int` or `float`: 28 million of them on the long replay.
   That is a known cost the prototype must measure. Moving the value tree itself
   into Rust would change `FieldState`, which is public API, so it is out of scope.
3. **Stage 2 call:** `decode_packet(entity_data, updates, handlers)` runs the
   entity loop natively. It creates and updates Python `Entity` objects, and calls
   the Python dispatcher after each entity.

The Python implementation stays in place. gem uses the extension only when it is
installed and supports the replay's schema, and a setting forces the Python
path, for debugging and for differential tests.

## Packaging

- Build with maturin as an **optional** package (for example `gem-dota[fast]`),
  not a required dependency, so `pip install gem-dota` stays pure Python.
- Publish wheels for the platforms gem's users run: Linux x86-64 and arm64,
  macOS arm64 and x86-64, and Windows x86-64. Use the stable ABI (`abi3`), so one
  wheel covers Python 3.10 and later.
- CI builds the wheels and runs the full test suite twice: once with the
  extension, once without.

## How to decide whether to adopt it

A prototype of stage 1 must pass these checks before it's kept:

1. **Differential tests:** for random and real bitstreams, native and Python
   decoding produce the same values, the same `FieldState` trees, and the same
   reader position. This includes every field model, the quantized-float setups
   and Huffman codes already pinned, array shrinking, and truncated input.
2. **Byte-identical output:** `gem.to_json(gem.parse(...))` matches the Python
   path on the committed fixture and on the full OpenDota fixtures, and the
   offline integration suite passes with the extension enabled.
3. **Measured benefit:** fresh timing of `gem.parse()` and the core parse on
   the v0.8.0 profile's two replays, with and without the extension, including
   schema compilation and boundary costs. It is kept only if the gain is large
   enough to justify a compiled dependency.

Stage 2 follows only if stage 1 is kept, with the same three checks plus
handler-order tests.

## Python-only wins, available now

Some costs found along the way need no Rust:

- **`find_by_npc_name` never finds anything on current replays.** It looks up
  `m_pEntity.m_nameStringableIndex`, but every replay checked from build 6792 on
  names the field `m_nameStringTableIndex`, so each call scans all 16,384 entity slots and
  returns `None`. The v0.8.0 profile measured this scan at 1.6–2.8% of
  `gem.parse()`. The fix changes how summoned units are credited, so it needs an
  OpenDota parity check first. It is scheduled with the combat-log review.
- **Payloads gem ignores** (voice data above) could skip being copied.
- **Handler-heavy classes:** 84% of entity updates reach a handler in
  `gem.parse()`, mostly creeps, through the visibility extractor's field-filtered
  handlers. That's 19 seconds of handler time on the long replay, to be reviewed
  with the extractors.

## Where to go next

- [Final Python parser profile](parser-profile-2026-09.md): the sampling profile
  and the original boundary decision.
- [Parser Performance](parser-performance.md): how gem is benchmarked.
- The "How Entities Are Decoded" series, from [Part 1: The Schema](entity-schema.md)
  to [Part 5: Entity Lifecycle](entity-lifecycle.md).
