# Farming Context Calibration

This page records the reproducible validation behind the default comparative
farming-context thresholds. It keeps replay facts separate from strategic
judgment: the corpus asserts route, evidence, topology, completeness, and tag
counts, but never labels a route as good, bad, safe, or forced.

## Reproduce the corpus

The committed summaries live in
`tests/fixtures/opendota/farming_context_corpus.json`. Full `.dem` files remain
gitignored and are synchronized from `tests/fixtures/opendota/manifest.json`.

```bash
uv run python scripts/sync_opendota_fixtures.py --all-active
uv run python scripts/calibrate_farming_context.py \
  tests/fixtures/opendota/8822520406.dem \
  tests/fixtures/opendota/8855188139.dem \
  tests/fixtures/opendota/8855242704.dem \
  tests/fixtures/opendota/8856501050.dem \
  tests/fixtures/opendota/8860187335.dem \
  tests/fixtures/opendota/8868259993.dem \
  tests/fixtures/opendota/8974053011.dem \
  --check tests/fixtures/opendota/farming_context_corpus.json
```

The command parses gem's replay stream and rebuilds farming routes with the
public defaults. OpenDota JSON snapshots are not substituted for positional,
objective, resource, or vision evidence.

## Real-match coverage

The September 2026 audit parsed seven active fixtures: one short performance
baseline, three feature-regression matches, and short, medium, and long TI2026
matches. With the version 3 camp catalog (zones centred on the camp spawners)
it covers 70 player routes, 5,848 camp-local segments, and 206,950 sampled
route points.

| Match | Segments | Phases | Calibration role |
| --- | ---: | --- | --- |
| `8822520406` | 352 | early, mid | Short performance baseline |
| `8855188139` | 659 | early, mid, late | Roshan, purchases, and inventory regression |
| `8855242704` | 1,275 | early, mid, late | Long final-interval and XP regression |
| `8856501050` | 1,671 | early, mid, late | 93-minute stress fixture |
| `8860187335` | 912 | early, mid, late | Medium extended fixture with multiple Aegis windows |
| `8868259993` | 317 | early, mid | Canonical short integration fixture |
| `8974053011` | 662 | early, mid, late | Aegis-denial lifecycle regression |

Every player route is included rather than selecting only high-farm heroes.
That captures the different movement patterns of professional carries, mids,
offlaners, and supports without pretending the replay's coarse `lane_role`
number is an authoritative strategic-role label.

All four topology areas were exercised: 3,046 jungle, 1,207 triangle, 767
river, and 828 flooded-area segments. The phase split was 913 early, 2,425
mid, and 2,510 late segments. Lane-to-jungle movement and brief crossings are
therefore present in the factual segment totals rather than hand-picked as
subjective examples.

## Evidence-strength observations

| Evidence strength | Observed segments |
| --- | ---: |
| `strong_farm_evidence` | 2,023 |
| `weak_farm_evidence` | 1,326 |
| `transit_like` | 2,499 |

These counts demonstrate that the reconstruction does not promote every camp
touch to farming. They are sensitivity observations, not precision or recall:
the corpus has no defensible ground-truth field for player intent or complete
camp clears.

## Context-tag observations

| Context tag | Observed segments |
| --- | ---: |
| `own_side` | 3,145 |
| `enemy_side` | 1,936 |
| `border` | 767 |
| `high_enemy_presence` | 621 |
| `vision_disadvantage` | 375 |
| `tower_disadvantage` | 1,460 |
| `enemy_aegis_active` | 527 |
| `territorial_advance` | 1,307 |

Tags are independent, so their totals intentionally exceed the segment count.
For example, an enemy-side segment can also overlap active enemy Aegis,
modeled observer disadvantage, and sustained territorial advance. Observer
coverage is only a modeled source at the camp point; it is not proof that a
hero was hidden or visible.

All 5,848 real-replay contexts were complete under the recorded defaults. That
does not imply completeness is guaranteed. Targeted tests cover absent rosters,
stale economy samples, insufficient position coverage, point-vision gaps,
sample discontinuities, overlapping zones, and exact tag thresholds; those
cases must retain `None`, gap codes, and `incomplete_context` rather than
becoming synthetic zeroes.

## Threshold and topology policy

The corpus records the exact `FarmingContextConfig` defaults used to generate
its counts. A threshold change should update the configuration, boundary tests,
corpus summaries, and this page in the same pull request. Counts alone are not
a reason to tune a threshold toward a preferred story.

Camp ownership, lane affinity, and area are explicit 7.41 topology annotations.
The zone centres are the 7.41 replays' camp spawner positions (catalog version
3); the per-type radii are unchanged from the hand-drawn catalog. Geometry and
topology versions stay separate fields.

Future calibration should add real fixtures when they expose a new factual
boundary or missing-data condition. Human-reviewed strategy labels may be
studied separately, but must not replace the evidence-first regression corpus.
