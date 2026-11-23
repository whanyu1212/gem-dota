# Farming Route Calibration

This page records the reproducible regression corpus behind farming-route
reconstruction. It asserts route, evidence-strength, phase and topology counts
per fixture replay, and never labels a route as good, bad, safe, or forced.

gem 0.12's comparative segment context and its tags were removed in 0.13, and
with them this page's tag observations.

## Reproduce the corpus

The committed summaries live in
`tests/fixtures/opendota/farming_routes_corpus.json`. Full `.dem` files remain
gitignored and are synchronized from `tests/fixtures/opendota/manifest.json`.

```bash
uv run python scripts/sync_opendota_fixtures.py --all-active
uv run python scripts/audit_farming_routes.py \
  tests/fixtures/opendota/8974053011.dem \
  tests/fixtures/opendota/9097868416.dem \
  tests/fixtures/opendota/9097870389.dem \
  tests/fixtures/opendota/9098298585.dem \
  tests/fixtures/opendota/9101190574.dem \
  tests/fixtures/opendota/9101299342.dem \
  tests/fixtures/opendota/9101479361.dem \
  --check tests/fixtures/opendota/farming_routes_corpus.json
```

The command parses gem's replay stream and rebuilds farming routes with the
public defaults. OpenDota JSON snapshots are not substituted for positional or
resource evidence.

## Real-match coverage

The November 2026 audit parsed seven fixtures: six patch 7.42 BLAST SLAM IX matches (the shortest, the longest, three near the
median, and the Dark Seer game) and one 7.41 replay. With the version 5 camp
catalog, which uses only the camps a replay's spawners produced, it covers
70 player routes, 5,145 camp-local segments, and 179,220 sampled
route points.

| Match | Segments | Phases | Calibration role |
| --- | ---: | --- | --- |
| `8974053011` | 662 | early, mid, late | Patch 7.41 replay; Aegis-denial lifecycle regression |
| `9097868416` | 739 | early, mid, late | Feature parity: Roshan, purchases, and objectives |
| `9097870389` | 334 | early, mid | Canonical short integration fixture |
| `9098298585` | 648 | early, mid, late | Performance baseline with in-game pauses |
| `9101190574` | 775 | early, mid, late | Medium extended fixture |
| `9101299342` | 1,272 | early, mid, late | 73-minute stress fixture |
| `9101479361` | 715 | early, mid, late | Dark Seer illusions; first 7.42 fixture |

Every player route is included rather than selecting only high-farm heroes.
That captures the different movement patterns of professional carries, mids,
offlaners, and supports without pretending the replay's coarse `lane_role`
number is an authoritative strategic-role label.

All four topology areas were exercised: 2,691 jungle, 1,100 triangle, 664
river, and 690 flooded-area segments. The phase split was 806 early, 2,785
mid, and 1,554 late segments. Lane-to-jungle movement and brief crossings are
therefore present in the factual segment totals rather than hand-picked as
subjective examples.

## Evidence-strength observations

| Evidence strength | Observed segments |
| --- | ---: |
| `strong_farm_evidence` | 1,705 |
| `weak_farm_evidence` | 1,128 |
| `transit_like` | 2,312 |

These counts demonstrate that the reconstruction does not promote every camp
touch to farming. They are sensitivity observations, not precision or recall:
the corpus has no defensible ground-truth field for player intent or complete
camp clears.

## Threshold and topology policy

A change to `FarmingRouteConfig` or the camp catalog should update the boundary
tests, the corpus summaries and this page in the same pull request. Counts alone
are not a reason to tune a threshold toward a preferred story.

Camp ownership, lane affinity, and area are explicit 7.41 topology annotations.
The zone centres are the 7.41 replays' camp spawner positions (catalog version
4); the per-type radii are unchanged from the hand-drawn catalog. Geometry and
topology versions stay separate fields.

Future calibration should add real fixtures when they expose a new factual
boundary or missing-data condition. Human-reviewed strategy labels may be
studied separately, but must not replace the evidence-first regression corpus.
