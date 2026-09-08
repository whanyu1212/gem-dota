# Final Python parser profile

This study measures v0.8.0 after the Python workstreams in
[#158](https://github.com/whanyu1212/gem-dota/issues/158). The measured parser
source is commit `e3ec865e8d4831a2f7518663cec10a0ae0136283`. No parser,
extractor, dependency, or public result behavior changes in this study.
Measurements are dated 8 September 2026 UTC. The long-core allocation and
cProfile diagnostics were collected after resuming an interrupted session
(9 September in Singapore); all completed matrix records were
retained, and no timing runs were repeated.

This completes the final profiling and native-boundary decision for the Python
optimization roadmap. A Rust implementation remains future work, with adoption
dependent on measured public-API benefit and compatibility checks.

## Method and scope

The existing environment is CPython 3.10.4, Clang 14.0.3, on an Apple M2
with 8 CPUs and 16 GiB RAM, macOS 26.6.2 arm64. Production packages include
NumPy 2.2.6, pandas 2.3.3, protobuf 7.34.0, and python-snappy 0.7.3.
Each measurement records the complete installed package list, interpreter,
source commit, harness hash, fixture integrity, load averages, and power state.
This is not the Python 3.10.21 build from the earlier runtime comparison.
`system_profiler` confirmed Mac14,15, Apple M2, and 16 GB. Every timing run
started and ended on AC power at 80%; Low Power Mode was disabled. Thermal and
CPU performance status were unavailable through `pmset`, so throttling cannot
be confirmed or excluded. Recorded 1-minute load averages spanned 2.57–3.74;
they do not establish exclusive use of the host.

| Fixture | Role | Match duration | Replay bytes |
|---|---|---:|---:|
| `8822520406` | DreamLeague performance baseline | 1,397 s | 98,983,300 |
| `8856501050` | TI2026 long stress replay | 5,576 s | 385,487,555 |

The harness verifies both replay sizes and SHA-256 digests against the committed
fixture manifest, using a 1 MiB streaming buffer. This reads the file before
timing; these are warm-filesystem-cache CPU benchmarks, not cold disk or download
benchmarks. Each invocation imports Gem from the measured checkout and parses
one whole replay in a fresh process. Imports are preloaded equally in both
scenarios, normal GC stays enabled, and a full collection precedes measurement.
`PYTHONHASHSEED=0` and `PYTHON_JIT=0` are set throughout.

Public timing includes extractor setup, parsing, finalization, and result
assembly through `gem.parse`. Core timing constructs `ReplayParser` before
the timer and calls `parse()` without standard extractors. Core still runs the
parser's built-in metadata, string-table, combat-message, and entity handling.
A single wrapper checks `parse_error` and captures terminal metadata in both
scenarios. An incomplete parse fails the measurement.

Twelve uninstrumented runs cover three observations of each scenario/fixture.
The sequential block order is:

1. Public short, core short, public long, core long.
2. Core long, public long, core short, public short.
3. Core short, public short, core long, public long.

No tests, profiler runs, or other benchmark jobs run alongside these timings.
A separate short public pilot checked the harness and is excluded from the
matrix. Reordering exposes session drift; three observations do not establish
performance on other machines, runtimes, patches, or arbitrary replay lengths.

Elapsed and user/system CPU time exclude imports, fixture hashing, output
serialization, and reporting. Process peak RSS is captured before serialization
and GC and includes pre-timer allocations. Current RSS is also captured at parse
return and after GC, with the result or core parser still alive. Core/public
differences are workload comparisons, not an exact decomposition of extractor
cost or exclusively owned memory.

## Uninstrumented results

Medians of three fresh processes. Seconds and MiB; elapsed ranges retain every
observation. [Individual JSON measurements](../benchmarks/2026-09-08-parser/index.md)
include all CPU, RSS, load, and output-integrity readings.

| Scenario | Replay | Elapsed median (range) | User CPU | Peak RSS | RSS after GC |
|---|---|---:|---:|---:|---:|
| Public | Short | 53.367 (49.548–54.582) | 53.249 | 211.12 | 122.52 |
| Core | Short | 42.060 (39.250–42.118) | 41.981 | 167.38 | 72.97 |
| Public | Long | 173.650 (160.803–175.869) | 173.164 | 675.03 | 323.94 |
| Core | Long | 146.827 (142.394–147.016) | 146.120 | 441.53 | 73.89 |

The workload is predominantly single-core CPU-bound: user CPU stays close to
elapsed time. Later blocks are generally slower than the first, despite stable
power observations. Session/frequency effects remain unresolved. These are
current baseline measurements, not a controlled speedup claim against an older
release, runtime build, or measurement session. No observations were discarded
and no follow-up timing was selected to improve the median.

Core elapsed medians are about 79% and 85% of the corresponding public medians.
This points toward core decoding as the main acceleration opportunity, subject
to the more specific call-stack profile below. The ratio is not a direct
measurement of time spent in extractors, because these are separate workloads.

Core RSS after GC is about 73–74 MiB on both replays, while its peak grows from
167 to 442 MiB. The peak-to-end differences closely track the replay mapping
sizes (94.4 and 367.6 MiB); `DemoStream` unmaps the replay at parse completion.
This supports separating file-backed RSS from retained Python data. It does
not imply every peak-RSS byte has been attributed, or that a Rust kernel would
eliminate mapped replay memory. Public post-GC RSS also grows substantially
with the larger result; allocation checkpoints examine that separately.

All six public results exactly match the previously validated normalized
SHA-256 values; no float rounding, field removal, or array reordering is used.

| Replay | JSON bytes | Combat entries | End tick | SHA-256 |
|---|---:|---:|---:|---|
| `8822520406` | 30,401,205 | 44,686 | 102642 | `3b0844312187a2856743092e991ab425878d64e101d91cf8f9c83bb2b3580427` |
| `8856501050` | 187,363,261 | 272,400 | 224720 | `1e8d1f6f172d7bc39abd6b2a338539b231395780e599b9b8fbf44068128a9e5e` |

Each public result has 10 players and the manifest's expected duration.
All core runs reach the same terminal match IDs, ticks, and game-build metadata
as the corresponding public runs, without a recorded parse error.

## CPU diagnostics

Separate Pyinstrument 5.1.3 runs sample each full public/core scenario on both
fixtures, with a 5 ms interval and async tracking disabled. These provide
call-stack rankings, not benchmark times. Exclusive time includes a function's
synthetic self-time samples; inclusive time counts recursive occurrences once
per stack. Inclusive rows overlap and must not be summed. A separate short
public `cProfile` run supplies deterministic call counts; its seconds include
substantial instrumentation overhead.

| Scenario | Replay | Instrumented elapsed | Stack samples | `read_fields` inclusive share |
|---|---|---:|---:|---:|
| Public | Short | 92.152 s | 18,402 | 54.00% |
| Core | Short | 74.313 s | 14,859 | 70.78% |
| Public | Long | 320.280 s | 63,830 | 59.15% |
| Core | Long | 261.896 s | 52,352 | 71.54% |

Sampling elapsed is about 1.7–1.8 times the uninstrumented median. That is
substantial overhead: use the profiles for directional rankings, not exact
uninstrumented attribution or native-speedup predictions. There is one
diagnostic observation per scenario/fixture, not a statistical confidence
interval. All sampled public output hashes match the timing runs.

The largest consistent individual costs are shown as **exclusive** sampled
time; these rows do not include their callees:

| Function | Public short | Public long | Core short | Core long |
|---|---:|---:|---:|---:|
| `_read_compact_field_paths` | 14.38% | 15.75% | 18.88% | 19.06% |
| `BitReader.read_bits` | 12.76% | 13.79% | 16.83% | 17.06% |
| `FieldState._set_compact` | 5.56% | 6.68% | 7.38% | 7.98% |
| `read_fields` loop itself | 4.62% | 5.39% | 6.49% | 6.40% |

The broader `read_fields` subtree includes Huffman operations, primitive
reads, decoder execution and state writes. Its 54–59% public / 71–72% core
share makes it the selected prototype boundary. Some primitive reads also
occur outside that subtree; do not sum the inclusive kernel share with its
nested functions or attribute every bit read to the kernel.

Entity callback dispatch including its handlers accounts for 22.63% / 14.89%
of sampled public time on short/long, versus 2.58% / 2.39% in core. Residual
`find_by_npc_name` scanning accounts for 1.57% / 2.78% of public time, including
callees. These remain real costs, but do not justify another broad Python
index/cache rewrite ahead of the kernel prototype on this evidence.

About 41–46% of sampled public time lies outside the selected kernel. A
zero-cost kernel would yield only roughly 2.2–2.4× in an illustrative Amdahl
calculation using those fractions. That is not a forecast—the profiling
overhead, native boundary costs, object conversion, and cache effects are
unresolved—but it explains why this study does not support the old 3–5×
end-to-end Rust estimate.

The short public cProfile run confirms the volume at this boundary:

| Function | Calls |
|---|---:|
| `BitReader.read_bits` | 34,056,940 |
| `FieldState._set_compact` | 9,962,805 |
| `FieldPath.__init__` | 5,274,740 |
| `read_fields` | 5,272,673 |
| `_read_compact_field_paths` | 5,272,673 |
| `find_by_npc_name` | 621 |

These counts include the whole public parse, so primitive-read counts are not
exclusive to the proposed kernel. Even the grouped boundary is crossed over
five million times on this short fixture; transition and Python-object costs
must therefore be measured in the prototype. The run took 165.617 seconds
with cProfile enabled, about 3.1 times the uninstrumented median. Its host load
fell from 11.21 to 5.16 after the allocation run. Use its counts, not its elapsed
time, to characterize the production workload. Its output hash also matches.

## Allocation diagnostics

One fresh process per scenario/fixture uses `tracemalloc` with one traceback frame. Public checkpoints
are immediately before result assembly, at parse return, and after full GC.
Core checkpoints are at parse return and after GC. The report keeps the top
100 live allocation locations at each checkpoint and the traced live-byte
high-water mark. Imports and core parser construction precede tracing.

These are **live traced Python allocations**, not cumulative allocation churn,
total RSS, or allocation stacks at the exact RSS peak. Checkpoint snapshots
also add instrumentation overhead. In particular, replay `mmap` pages and
untraced native buffers are not represented by Python allocation totals.
Use the uninstrumented timing runs for process peak-RSS conclusions.
Core retains its parser/entity state; public retains its returned `ParsedMatch`.
Those are different object sets. A smaller Python allocation count cannot by
itself promise a corresponding RSS reduction.

The one-frame trace groups generated code under shared locations such as
`<string>:3`; that bucket combines constructors and cannot identify an exact
record type. Named allocation locations also omit allocations attributed to
callees. In particular, the `CombatLogEntry(...)` call site's bytes are not the
total size of combat records and their referenced dictionaries and values.

MiB of traced allocations, with one diagnostic observation per row. The peak
column is the high-water mark captured at the parse-return checkpoint and
includes earlier checkpoint instrumentation; it is not process peak RSS.

| Scenario | Replay | Before assembly | At parse return | After GC | Traced peak |
|---|---|---:|---:|---:|---:|
| Public | Short | 63.702 | 67.429 | 33.179 | 69.609 |
| Core | Short | — | 20.903 | 20.885 | 21.742 |
| Public | Long | 242.162 | 254.240 | 182.647 | 269.680 |
| Core | Long | — | 21.632 | 21.589 | 22.556 |

Public live allocations fall by 34.250 MiB / 71.592 MiB after collection.
Core retains its parser, so most of its live allocations remain. The similar
post-GC core heaps on these two fixtures do not establish a bound for every
replay. Public histories and records grow substantially with the larger
result; a decode kernel that preserves those Python objects will not remove
that retained-data cost.

Representative post-GC allocation locations:

| Location | Public short | Public long | Interpretation |
|---|---:|---:|---|
| `<string>:3` | 17.801 | 105.904 | Shared generated-code bucket; not a single record type |
| `extractors/players.py:786` | 1.831 | 21.286 | Ability-level dictionaries |
| `combat/log.py:445` | 2.042 | 12.463 | Combat-entry allocation call site, excluding constructor-internal allocations |

Core post-GC decoder-cache insertions at `field_reader.py:126` account for
2.232 / 2.814 MiB. Serializer field lists at `sendtable/parser.py:257` account
for 2.005 MiB on both fixtures. Field-state list growth and compact path tuples
are other leading core sites. These are checkpoint allocation locations, not
exclusive subsystem ownership or a cumulative allocation-churn ranking.

The resumed long-core trace encountered materially different host conditions:
its 1-minute load rose from 2.27 to 11.21, and elapsed/user CPU were
1,192.804 / 988.572 seconds. A host check during the run showed about 6.3 GiB
occupied by the memory compressor ([host observations](../benchmarks/2026-09-08-parser/resumed-host-observation.txt)). Those observations are consistent with
contention and memory pressure but do not isolate the cause of the slowdown.
Its instrumented peak RSS was only 255.11 MiB, illustrating why it must not
replace the earlier uninstrumented 441.53 MiB core-long median. Tracer metadata
also costs memory: after-GC metadata was about 17.0 / 17.1 MiB for core and
28.4 / 126.1 MiB for public short/long. All public allocation-run hashes match
the timing results, and the core-long parse completed at the expected tick.

## Selected native boundary

The next prototype should use one optional **entity-field decode/apply kernel**, at
`schema/field_reader.py::read_fields`. It encompasses Huffman field paths,
bit/varint reads, cached schema/decoder selection, value decoding, and writes
to the existing field-state tree. The entity manager invokes it for baseline
and delta decoding, then runs the existing Python callbacks against fully
updated entities. Manta's `field_reader.go` groups decoding and state writes
at this boundary. Clarity's `S2FieldReader.readFields` likewise decodes all
paths before their values, but returns `FieldChanges` for later application.

Moving only individual bit-reader methods to Rust would leave a language
transition for every primitive. Moving only Huffman path decoding would leave
Python tuple materialization, decoder calls, and state-write dispatch in the
inner loop. The grouped kernel instead crosses once per entity baseline/delta;
it is still a frequent boundary and its overhead must be benchmarked.

A prototype should compile parse-scoped immutable native schema descriptors,
including quantized-float parameters and fixed/variable table and array models.
Decode the complete path sequence before reading its values, as the wire
format requires, and preserve Gem's existing floating-point results exactly.
It should reuse the input buffer, synchronize the reader's byte position and
prefetched bit cache, and preserve the Python `FieldState` tree's identity and
mutation rules. Keeping Python objects initially also keeps the GIL and much
of their storage cost; native code does not automatically make one parse
parallel or reduce retained-result memory.

Keep packet/entity lifecycle, callback ordering, extractors, aggregation, and
result assembly in Python. Preserve the public `BitReader`, mutable
`FieldPath`, `FieldState`, and decoder APIs and provide a pure-Python fallback.
Unsupported custom decoders or state/reader behavior should select fallback
before consuming input. Native execution must match malformed/truncated input
errors, cursor state, and partial mutations; blindly retrying after a partially
applied native delta would be unsafe.

The prototype's acceptance gates are native/Python differential reader and
decoder tests, all field models, shallow/deep/sparse state and protected child
nodes, baseline-before-delta ordering, recycled entities, callback ordering,
and exact public output on both profiling fixtures. Run the full offline and
TI2026 OpenDota-parity gates and fresh paired public/core CPU/RSS measurements.
Choose adoption from measured end-to-end benefit after schema compilation,
Python object conversion, and boundary costs—not from a bit-reader
microbenchmark. This study does not implement or promise a Rust speedup.

## Reproduction

The harness is `scripts/profile_parser.py`; each command runs one fresh process
and refuses to overwrite an existing result. Use the recorded dependency
environment and the local ignored replay files. It requires `psutil` for
current RSS; the sampling mode additionally requires Pyinstrument 5.1.3.
Neither profiler is added to Gem's production dependencies.
The recorded commit is Git HEAD; reproduce against the named clean parser
source. The current harness rejects staged, unstaged, and untracked changes in
`src/gem` before importing the parser and again before returning the report.
It also rejects a changed HEAD or failed Git command. Unrelated edits and
ignored cache files do not invalidate parser provenance.

The measured harness SHA-256 is
`3b130052940674c4768dc0c3c60c3fb1fb4d0214a1fbfeeb441a2145f693b85c`.
The original PR commit `f0f4e90814f517f4d19313d55e81d1983657f31a` contains that
harness plus five inline `type: ignore` comments; removing those comments and
their two preceding spaces from that revision reproduces the measured bytes.
Review subsequently added automatic parser-provenance and output-hash guards
outside the measurement window. The original study checked these conditions
separately; its 21 records retain their original hashes and were not rerun or
relabeled as measurements of the updated harness.

```bash
PYTHONHASHSEED=0 PYTHON_JIT=0 .venv/bin/python scripts/profile_parser.py \
  --replay tests/fixtures/opendota/8822520406.dem \
  --scenario public --mode timing --output tmp/profile/public-short-1.json
```

Repeat timing commands in the block order above, changing fixture, scenario,
and output filename. After timings finish, run `--mode sample` and `--mode
memory` once per scenario/fixture, then `--mode cprofile` for public short.
Sampling can import an isolated installation using
`--profiler-path /path/to/pyinstrument-installation`. This study reused the
locally cached 5.1.3 wheel, without changing the project environment.

All normalized public outputs use
`json.dumps(gem.to_dict(match), sort_keys=True, separators=(",", ":"))`,
encoded as UTF-8. Serialization happens after measurements. Core runs check
terminal parser metadata; they do not construct or claim to validate a public
`ParsedMatch`. Instrumented public output hashes must equal the uninstrumented
ones and the earlier validated hashes. The current harness enforces the two
documented expected hashes and fails before saving a measurement on mismatch.
Public runs on other fixtures require a separately validated expected hash
before profiling; a newly observed digest is not automatically a baseline.

## Validation

- Fast suite: **3,895 passed, 5 skipped, 62 deselected**, including regression
  checks for synthetic self-time attribution and recursive inclusive-time
  accounting in the profiling summaries.
- Ruff lint and format checks passed for `src/`, `tests/`, and the harness.
- Mypy passed for all 88 checked source files.
- PR preparation also type-checked the harness and reran its two regression
  tests after the typing-only comments described above.
- Review follow-up adds regression checks for detailed output changes despite
  unchanged metadata, staged/unstaged/deleted/untracked parser sources, clean
  checkouts with unrelated files, Git failures, and the recorded public hashes.
  The updated fast suite passed: **3,903 passed, 5 skipped, 62 deselected**.
- All 21 measurement records have the same harness hash, source commit,
  interpreter, and installed-package manifest. All 11 public parses, including
  instrumented runs, match the expected output hashes.
- VitePress production docs build passed, with a bundle-size warning.
- Fixture size/digest, parser completion, public match identity/player count/
  duration, and normalized-output checks run outside the timing window.

The fast-suite command was:

```bash
.venv/bin/python -m pytest -q -o addopts='' \
  -m 'not slow and not integration and not network' --tb=short
```

No parser source changes are present. Exact prior validated output hashes
serve as the full-replay compatibility oracle for this profiling-only change;
this study does not rerun the external OpenDota comparison or the entire
offline integration matrix. Those remain required gates for the proposed
native implementation.
