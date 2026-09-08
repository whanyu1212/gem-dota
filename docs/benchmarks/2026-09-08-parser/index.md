# Final parser profile: measurement records

Source: `e3ec865e8d4831a2f7518663cec10a0ae0136283` (v0.8.0).

[Study and interpretation](../../deep-dives/parser-profile-2026-09.md).

The JSON records include all observations and environment details. Timing records are uninstrumented; sampling, tracemalloc, and cProfile records are diagnostic and must not be used as production speed/RSS benchmarks.

Timing records retain individual observations. Sampling records contain
per-function exclusive/inclusive aggregates, not raw sampled stacks or saved
Pyinstrument sessions. Allocation records retain totals and the top 100 live
allocation locations at each checkpoint; cProfile records contain function
counts/times without caller edges. The harness can reproduce these summaries.

## Timing runs

- [timing-core-8822520406-1.json](timing-core-8822520406-1.json)
- [timing-core-8822520406-2.json](timing-core-8822520406-2.json)
- [timing-core-8822520406-3.json](timing-core-8822520406-3.json)
- [timing-core-8856501050-1.json](timing-core-8856501050-1.json)
- [timing-core-8856501050-2.json](timing-core-8856501050-2.json)
- [timing-core-8856501050-3.json](timing-core-8856501050-3.json)
- [timing-public-8822520406-1.json](timing-public-8822520406-1.json)
- [timing-public-8822520406-2.json](timing-public-8822520406-2.json)
- [timing-public-8822520406-3.json](timing-public-8822520406-3.json)
- [timing-public-8856501050-1.json](timing-public-8856501050-1.json)
- [timing-public-8856501050-2.json](timing-public-8856501050-2.json)
- [timing-public-8856501050-3.json](timing-public-8856501050-3.json)

## CPU sampling

- [sample-core-8822520406.json](sample-core-8822520406.json)
- [sample-core-8856501050.json](sample-core-8856501050.json)
- [sample-public-8822520406.json](sample-public-8822520406.json)
- [sample-public-8856501050.json](sample-public-8856501050.json)

## Allocation diagnostics

- [memory-core-8822520406.json](memory-core-8822520406.json)
- [memory-core-8856501050.json](memory-core-8856501050.json)
- [memory-public-8822520406.json](memory-public-8822520406.json)
- [memory-public-8856501050.json](memory-public-8856501050.json)

## Deterministic call counts

- [cprofile-public-8822520406.json](cprofile-public-8822520406.json)

## Host observations

[Resumed allocation-run host observations](resumed-host-observation.txt) record
load, virtual-memory, and process readings taken during the long-core trace.
They are supplementary context, not benchmark measurements.
