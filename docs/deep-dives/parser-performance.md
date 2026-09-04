# Parser Performance

This page records the Python parser optimization work completed after the
September 2026 baseline profile. It is a maintainer reference, not a performance
guarantee: replay duration, patch, entity volume, enabled extractors, Python
version, and hardware all affect parse time.

## Benchmark fixture and method

The common benchmark is
`tests/fixtures/opendota/8822520406.dem`, a 98,983,300-byte DreamLeague Season 29
replay lasting 1,397 seconds. The original profile was collected on macOS arm64
with Python 3.10.4.

Measurements separate three kinds of work:

1. `gem.parse`, including standard extractors and result assembly
2. `ReplayParser.parse` without standard extractors, isolating core decoding
3. instrumented profiles and counters, used for rankings and call volume

Elapsed time and peak resident memory come from fresh, uninstrumented processes.
Instrumented profiles are not used as elapsed-time benchmarks because profiler
overhead is substantial. Each optimization PR recorded the median of three full
parses and checked a normalized `ParsedMatch` against its preceding baseline.

## Baseline

The original profile at commit `ed6d7a5` measured:

| Scenario | Elapsed | Peak RSS |
|---|---:|---:|
| Public `gem.parse` | 92.976 s | 193.7 MiB |
| Core `ReplayParser.parse` | 58.280 s | 154.4 MiB |

The dominant repeated work included 36.9 million built-in callback invocations,
26.6 million `Entity.get` calls, 15.2 million `FieldPath` constructions, 9.96
million `FieldPath.copy` calls, and approximately 13.9 million recursive decoder
resolution calls. `FieldState` reads and writes also spent significant time in
small helper methods invoked once per path component.

See [issue #143](https://github.com/whanyu1212/gem-dota/issues/143) for the full
historical function table and memory breakdown.

## Optimization sequence

Five deliberately separate changes addressed the measured Python hot paths:

| Change | Main measured effect |
|---|---|
| [Class-aware callback routing](https://github.com/whanyu1212/gem-dota/pull/152) | Built-in callback invocations fell from 36,890,700 to 5,381,400 (85.4%). |
| [Per-entity loop cleanup](https://github.com/whanyu1212/gem-dota/pull/153) | Sampling eligibility checks fell from 2,169,002 to 51,312; interval hero-name resolutions fell from 1,330,198 to 42; unused result tuples were removed from the parser path. |
| [`FieldState` traversal cleanup](https://github.com/whanyu1212/gem-dota/pull/154) | Production traversal eliminated 15,868,940 `_has_slot`, 15,198,552 `_ensure`, and 15,533,746 `_is_child` dispatches. |
| [Shared compiled entity fields](https://github.com/whanyu1212/gem-dota/pull/155) | Profiled public `Entity.get` calls fell from 26.6 million to 41; serializer field caches retained about 604 KiB. |
| [Compact paths and decoder caching](https://github.com/whanyu1212/gem-dota/pull/156) | Production `FieldPath.copy` calls fell from about 9.96 million to zero; recursive decoder resolution fell from about 13.9 million calls to about 80,000. |

The final pass recorded a 64.15-second public median and a 41.40-second core
median. Those are respectively 11.2% and 15.6% faster than its immediately
preceding quiet baseline. Compared with the original #143 measurements, they are
about 31% and 29% lower, but that longer-range comparison spans separate
measurement sessions and should be treated as directional rather than a
controlled benchmark.

## Correctness gates

Each pass retained public callback and entity APIs and compared normalized output
with the preceding implementation. After the final pass, the normalized
`8822520406` output remained 33,045,771 bytes with SHA-256
`88712b6b104fa937cee13c5589708327a389e02bf70a95a3716fde9b5c2775b2`.

Focused tests cover callback ordering and lifecycle operations; sparse and nested
`FieldState` traversal; simple, fixed-array, fixed-table, variable-array, and
variable-table decoder models; serializer cache isolation; invalid paths; entity
creation, updates, deletion, and recycled slots. Full replay tests add output and
OpenDota parity coverage.

## Memory and remaining work

The final pass recorded median peak RSS of 228.2 MB, about 1.9% above its
immediately preceding public baseline. Its parse-scoped decoder caches were
estimated at 5.6 MB. The optimization sequence therefore produced a clear CPU
improvement, but did not establish a memory reduction.

The final profile still identified two measurable Python costs:

- `EntityManager.find_by_npc_name` scans the entity-slot collection.
- Some extractor paths still repeat indexed field lookup work.

These remain candidates, not committed follow-up work. A new optimization should
start with a fresh profile and demonstrate enough end-to-end impact to justify
the added indexes or extractor complexity.

The final PR recorded helper-call elimination for `FieldState`, but not a
standalone post-change `FieldState` self-time or a complete allocation ranking.
Do not infer either number from the elapsed-time improvement. Reprofile before
making claims about the current top memory allocation sites.
