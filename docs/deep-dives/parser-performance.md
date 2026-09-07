# Parser Performance

Runtime builds, dependencies, replay duration, patch, entity volume, and enabled
extractors all affect parse time. This page records measured results and their
limits; historical optimization measurements are preserved below.

## CPython runtime study — 7 September 2026 {#cpython-runtime-study}

This study measures source commit
`3d1b734b60ba418b8c1324bc9cf1fb5c7688fbc8`, after the optimizations through
[#178](https://github.com/whanyu1212/gem-dota/pull/178). It does not change Gem's
Python 3.10+ requirement. The earlier measurements below remain historical;
they are not the baseline for this comparison.

### Environment and dependency control

The host was an Apple M2 Mac14,15 with 16 GiB RAM, running macOS 26.6.2 arm64
on AC power with Low Power Mode disabled. All interpreters were standard,
GIL-enabled arm64 `install_only` builds from Astral's
[20260901 release](https://github.com/astral-sh/python-build-standalone/releases/tag/20260901),
built with Clang 22.1.3. No Rosetta, free-threaded, prerelease, or enabled JIT
builds were included. `PYTHONHASHSEED=0` and `PYTHON_JIT=0` were set; build
configuration and GIL/JIT introspection were checked where available.

| Label | CPython | Production dependencies |
|---|---|---|
| A | 3.10.21 | Common Python 3.10 lock selection |
| B | 3.11.16 | Same common versions as A |
| C | 3.12.14 | Same common versions as A |
| D | 3.13.15 | Same common versions as A |
| E | 3.14.7 | Native Python 3.14 lock selection |

A–D use 43 identical production dependency versions, including NumPy 2.2.6,
pandas 2.3.3, and IPython 8.38.0. These are marker-independent constraints
materialized from the existing lock's Python 3.10 selection, including its
compatibility backports. Matching versions still use interpreter-specific
binary wheels. E uses 40 native dependencies, including NumPy 2.4.2, pandas
3.0.1, and IPython 9.11.0. E therefore compares a **runtime and dependency
environment**; its differences cannot be attributed entirely to CPython.

All environments installed the same `gem_dota-0.7.1-py3-none-any.whl`, SHA-256
`9070de91fb18289ce1461de0f919be9f912f040511ddfff7a795eebf38754bbd`.
The wheel also includes 553 pre-existing ignored report PNGs (14,120,517
uncompressed bytes). A clean archived-source rebuild has identical shared
entries except `RECORD`, but omits those icons and therefore has a different
wheel hash. Restoring the recorded assets and pinning `uv_build==0.9.8`
reproduced the measured wheel hash exactly. The asset manifest and restore
script are preserved with the reproduction notes. Exact reconstruction requires
those existing PNG bytes; the manifest alone cannot recreate them on a fresh
checkout. A clean-source experiment can use a different wheel hash consistently
across runtimes; the assets are report
resources, not parser inputs. All five runtimes used the same measured wheel.
Installation used uv 0.9.8, hash-checked binary production requirements,
explicit interpreter paths, and isolated environments. Installed versions,
wheel provenance, dependency consistency, and the installed Gem import path
were verified. Test tools lived in separate environments and did not change
production pins. The project environment, lockfile, and global tools were
preserved.

### Measurement protocol

Each scenario/replay used three fresh processes per runtime, with one parse
per process: 60 timed parses in total. Sequential blocks were A/B/C/D/E,
E/D/C/B/A, and C/A/E/B/D. No tests, profiling, or other benchmark workloads ran
concurrently. Lazy imports were preloaded; normal garbage collection remained
enabled, with a collection immediately before timing. Core parser construction
was outside the timer. Public timing included extractor setup and result
assembly. Startup, imports, serialization, and hashing were excluded.

Elapsed time, user CPU, and process peak RSS were captured before serialization.
Peak RSS includes earlier process allocations and is **not retained-result
memory**. Three observations expose variation but cannot establish a universal
ranking across hardware, builds, replay patches, or dependency versions.

The short fixture `8822520406.dem` is 98,983,300 bytes, SHA-256
`5f976ab73b2efb0e4eca9f7f14d5980f3aae5f63e7952e16a8497eeded57d39d`.
The long TI2026 fixture `8856501050.dem` is 385,487,555 bytes, SHA-256
`0f7577525b995347ed9df0c793cc8661c2a9db4ee176bf35cb5dd940e5af17e2`.


### Every production dependency difference

| Package | A–D | E |
|---|---|---|
| exceptiongroup | 1.3.1 | Absent |
| ipython | 8.38.0 | 9.11.0 |
| ipython-pygments-lexers | Absent | 1.1.1 |
| numpy | 2.2.6 | 2.4.2 |
| pandas | 2.3.3 | 3.0.1 |
| pytz | 2026.1.post1 | Absent |
| typing-extensions | 4.15.0 | Absent |
| tzdata | 2025.3 | Absent |

### Primary measurements

Medians of three runs; times in seconds, peak RSS in MiB. The parenthesized elapsed range shows all three observations. Full-precision individual measurements and start/end load averages are preserved in the reproduction notes.

| Scenario | Replay | CPython | Elapsed (range) | User CPU | Peak RSS |
|---|---|---|---:|---:|---:|
| public | 8822520406 | 3.10.21 | 45.714 (44.801–46.597) | 45.140 | 196.33 |
| public | 8822520406 | 3.11.16 | 29.804 (29.764–30.514) | 29.680 | 196.03 |
| public | 8822520406 | 3.12.14 | 30.554 (30.322–31.934) | 29.901 | 193.00 |
| public | 8822520406 | 3.13.15 | 34.361 (34.105–34.524) | 33.953 | 182.30 |
| public | 8822520406 | 3.14.7 | 28.016 (28.016–28.594) | 27.866 | 180.62 |
| public | 8856501050 | 3.10.21 | 147.273 (143.437–148.238) | 145.423 | 624.12 |
| public | 8856501050 | 3.11.16 | 96.829 (96.604–98.373) | 95.875 | 587.34 |
| public | 8856501050 | 3.12.14 | 96.414 (95.539–99.154) | 95.780 | 576.64 |
| public | 8856501050 | 3.13.15 | 111.055 (109.191–113.694) | 110.586 | 582.25 |
| public | 8856501050 | 3.14.7 | 90.189 (89.728–91.367) | 89.187 | 607.31 |
| core | 8822520406 | 3.10.21 | 35.889 (35.820–36.198) | 35.650 | 166.06 |
| core | 8822520406 | 3.11.16 | 23.181 (22.997–23.468) | 23.063 | 167.89 |
| core | 8822520406 | 3.12.14 | 23.924 (23.696–23.954) | 23.694 | 167.84 |
| core | 8822520406 | 3.13.15 | 27.214 (26.566–27.960) | 27.126 | 169.66 |
| core | 8822520406 | 3.14.7 | 21.775 (21.598–21.803) | 21.654 | 172.02 |
| core | 8856501050 | 3.10.21 | 124.749 (122.408–125.827) | 124.216 | 425.72 |
| core | 8856501050 | 3.11.16 | 79.589 (79.279–82.361) | 78.939 | 428.41 |
| core | 8856501050 | 3.12.14 | 80.972 (80.668–84.278) | 80.412 | 429.81 |
| core | 8856501050 | 3.13.15 | 93.835 (92.417–95.300) | 92.933 | 418.53 |
| core | 8856501050 | 3.14.7 | 75.997 (75.623–77.230) | 75.689 | 416.81 |

Observed 1-minute host load ranged from 2.48 to 5.34. User CPU range divided by its median stayed below 4.5% in every primary scenario/runtime. Host load is an observation, not proof of an idle machine; sequential reordered blocks reduce but cannot remove session effects.

### Interpretation and runtime guidance

The provisional validation candidate was E (3.14.7), selected by the lowest
geometric mean of the two public elapsed medians. Relative to A=1.000, scores
were E=0.613, B=0.655, C=0.661, D=0.753. Public CPU, then newer minor version,
were the declared tie-breakers; neither was needed. E is the only environment
within 5% of the overall best score, but its changed dependencies and failed
compatibility assertion prevent a recommendation.

Within the controlled A–D comparison, B and C form a close group: their public
scores differ by about 1%, and their relative per-block directions vary. Both
reduce median public elapsed and CPU time by approximately 33–35% versus A
on each replay, with improvements in all three blocks. This meets the timing
threshold of at least 5% improvement in both metrics on both replays and at
least two improving blocks. It does not resolve a uniquely fastest runtime.

The original core runs showed consistently higher peak RSS for E on the short
replay and for B/C on both replays. The predeclared anomaly checks covered
mixed block directions, CPU range/median above 10%, median RSS increases above
10%, and smaller consistent increases. The same checks were extended from E
to B/C because they were the strongest passing configurations under common
pins. Five comparisons received one fixed three-pair follow-up each (30
additional parses), ordered candidate/A, A/candidate, candidate/A. No further
timing rounds were taken.

| Core follow-up | Replay | Median candidate peak RSS MiB | Median paired A peak RSS MiB | Difference of medians |
|---|---|---:|---:|---:|
| E/A | 8822520406 | 172.109 | 165.984 | +3.69% |
| B/A | 8822520406 | 168.062 | 166.109 | +1.18% |
| B/A | 8856501050 | 442.172 | 428.781 | +3.12% |
| C/A | 8822520406 | 167.734 | 166.016 | +1.04% |
| C/A | 8856501050 | 429.172 | 425.750 | +0.80% |

These follow-ups retain the small core memory increases. Higher pre-parse
high-water marks are consistent with a runtime/dependency startup-footprint
contribution, but do not prove it. Both readings use `ru_maxrss`; subtracting
them does not measure retained memory or isolate parser allocations. The
precise cause of the differences remains unresolved.

The final C/A long-core follow-up was unstable. C user CPU observations were
78.922, 166.522, and 165.390 seconds; A observations were 122.944, 158.052, and
250.125 seconds. Near the end, the host reported AC power but a 4% battery
that was discharging; Low Power Mode remained off and thermal status was
unavailable. This is evidence of session instability, not proof of a specific
power or thermal cause. Those observations are preserved separately and do
not replace the primary results or support a clean follow-up ranking.

The primary public timing benefits are clear, but the unresolved core memory
tradeoffs and unstable final follow-up prevent an unconditional performance
recommendation under this study's acceptance rules.


For practical installation decisions, the fast common-pin configurations are
worth evaluating for a parser-heavy workload, but this study does not select
an unconditional preferred runtime. Preserve Python 3.10+ compatibility and
validate the actual dependency environment you intend to install. In
particular, the passing common-pin results do not validate the repository's
native pandas 3 environment on newer Python minors.

### Compatibility validation

| CPython | Fast suite | All offline tests | Full OpenDota parity |
|---|---|---|---|
| 3.10.21 | 3854 passed, 3 skipped, 62 deselected in 11.30s | 3915 passed, 3 skipped, 1 deselected in 258.39s (0:04:18) | 982 PASS; 0 WARN; 0 FAIL; 3 informational SKIP |
| 3.11.16 | 3818 passed, 3 skipped, 62 deselected in 10.43s | 3879 passed, 3 skipped, 1 deselected in 563.45s (0:09:23) | In progress |
| 3.12.14 | 3818 passed, 3 skipped, 62 deselected in 9.39s | 3879 passed, 3 skipped, 1 deselected in 558.58s (0:09:18) | In progress |
| 3.13.15 | 3818 passed, 3 skipped, 62 deselected in 10.37s | Not selected | Not selected |
| 3.14.7 | 1 failed, 3817 passed, 3 skipped, 62 deselected in 29.21s | 1 failed, 3878 passed, 3 skipped, 1 deselected in 539.59s (0:08:59) | In progress |

Python 3.14.7 with pandas 3.0.1 fails the existing
`tests/test_bulk.py::TestParseManyToDataframe::test_match_path_column_is_string`
assertion (`dtype == object`); pandas instead returns its default string dtype.
No assertion or production dependency was changed to hide this failure. This
blocks a compatibility recommendation for E, even though its parser JSON
matches. Pandas documents this behavior in its
[3.0 release notes](https://pandas.pydata.org/docs/whatsnew/v3.0.0.html#dedicated-string-data-type-by-default).
The current lock also selects pandas 3.0.1 on Python 3.11–3.13. Passing B/C/D
checks with common pandas 2.3.3 pins do not validate those native-lock
environments, and this failure is not established as a CPython 3.14 defect.

The 36 fewer generated tests on Python 3.11+ result from `IntFlag` iteration:
`list(EntityOp)` yields five atomic members there, versus nine named members
on 3.10. The named-member overlap parametrization therefore changes from
9×9 to 9×5 cases. The exhaustive 32×32 mask check still runs on every runtime;
no tests were deleted.

Every pytest run has the same three skips: optional pyarrow coverage
(`tests/test_bulk.py:250`), an optional Parquet engine
(`tests/test_parquet_export.py:56`), and the existing optimized-away flag case
(`tests/test_field_decoder.py:208`). Fast selection deselects 62 marked tests;
offline selection deselects only the live network test. Full parity uses the
existing references for 8868259993, 8860187335, and 8856501050 with unchanged
thresholds (325, 326, and 331 passing fields per runtime). Each replay reports
one informational `teamfights/total_count` skip for the expanded OpenDota
pipeline's deaths≥3 convention. No required local fixtures were missing.

Validation timings are not parser performance measurements. Initial untimed
metadata/fast checks overlapped, as did baseline offline/parity checks; all
were stopped before the timing matrix began. Subsequent compatibility checks
ran concurrently across separate runtime environments, only after all timed measurements finished. Their elapsed durations include contention and should not be compared as runtime benchmarks.

### Public output equality

All 15 public results per replay were byte-identical across runtimes and
repetitions, using `json.dumps(gem.to_dict(result), sort_keys=True,
separators=(",", ":")).encode()` with `PYTHONHASHSEED=0`. Arrays were not reordered
and numeric values were not rounded to manufacture agreement.

| Replay | JSON bytes | Players | Combat events | Wards | Teamfights / OpenDota teamfights | Draft events |
|---|---:|---:|---:|---:|---:|---:|
| 8822520406 | 30,401,205 | 10 | 44,686 | 60 | 24 / 3 | 24 |
| 8856501050 | 187,363,261 | 10 | 272,400 | 221 | 36 / 10 | 24 |

SHA-256:

- `8822520406`: `3b0844312187a2856743092e991ab425878d64e101d91cf8f9c83bb2b3580427`
- `8856501050`: `1e8d1f6f172d7bc39abd6b2a338539b231395780e599b9b8fbf44068128a9e5e`

### Reproduction and provenance

The [study record](https://github.com/whanyu1212/gem-dota/issues/159) preserves complete bootstrap and benchmark
scripts, commands, common/native constraints, all installed package manifests,
binary-wheel URLs and hashes, executable paths, build configuration, individual
measurements, load observations, and compatibility/skip results in linked
reproduction notes. Temporary runtimes, environments, wheels, scripts, and
outputs were removed only after publication was verified.

To reproduce the controlled configuration, use the exact source commit and
Astral artifacts, build one wheel, then install it into an isolated environment
with the published common constraints. Use the published bootstrap instead of
assuming a plain `uv sync` on Python 3.11/3.12 produces the tested environment.
Keep test dependencies in separate constrained environments. No dependency
pins or Python-version requirements in Gem were changed by this study.

<details><summary>Runtime archive SHA-256 hashes</summary>

| CPython | SHA-256 |
|---|---|
| 3.10.21 | `cee232aabfb6790eec78f3cca935caeb7bd4eedca4dcb0a10dbcdb4302320b38` |
| 3.11.16 | `50424fa409e8ae84b82a3052522f64695b47dff2158b70bb7358e0ebd6c085c9` |
| 3.12.14 | `3ee3ee547cedfeb7c2b16b2b7156039f7b470bb8f857e226fd3d2eb11db83c76` |
| 3.13.15 | `b9054a9d3d54f4cb5573d44907fddb29874b08909bde73f29f2868cf872223ee` |
| 3.14.7 | `30daa970c7d223530120f1693cd3c6fa4c0c0d31ef158710b0dd77f286a5b23e` |

</details>

Final hotspot profiling and the Rust boundary decision remain under [#158](https://github.com/whanyu1212/gem-dota/issues/158). This study makes no claims about Linux, x86, other CPython builds, or JIT/free-threaded configurations.

## Historical optimization work (#143–#156)

### Benchmark fixture and method

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

### Baseline

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

### Optimization sequence

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

### Correctness gates

Each pass retained public callback and entity APIs and compared normalized output
with the preceding implementation. After the final pass, the normalized
`8822520406` output remained 33,045,771 bytes with SHA-256
`88712b6b104fa937cee13c5589708327a389e02bf70a95a3716fde9b5c2775b2`.

Focused tests cover callback ordering and lifecycle operations; sparse and nested
`FieldState` traversal; simple, fixed-array, fixed-table, variable-array, and
variable-table decoder models; serializer cache isolation; invalid paths; entity
creation, updates, deletion, and recycled slots. Full replay tests add output and
OpenDota parity coverage.

### Memory and remaining work

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
