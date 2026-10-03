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
  tests/fixtures/opendota/8822520406.dem \
  tests/fixtures/opendota/8855188139.dem \
  tests/fixtures/opendota/8855242704.dem \
  tests/fixtures/opendota/8856501050.dem \
  tests/fixtures/opendota/8860187335.dem \
  tests/fixtures/opendota/8868259993.dem \
  tests/fixtures/opendota/8974053011.dem \
  --check tests/fixtures/opendota/farming_routes_corpus.json
```

The command parses gem's replay stream and rebuilds farming routes with the
public defaults. OpenDota JSON snapshots are not substituted for positional or
resource evidence.

## Real-match coverage

The September 2026 audit parsed seven active fixtures: one short performance
baseline, three feature-regression matches, and short, medium, and long TI2026
matches. With the version 4 camp catalog (zones centred on the camp spawners, and
every camp's type and owner checked against the replays) it covers 70 player
routes, 5,814 camp-local segments, and 206,950 sampled
route points.

| Match | Segments | Phases | Calibration role |
| --- | ---: | --- | --- |
| `8822520406` | 352 | early, mid | Short performance baseline |
| `8855188139` | 658 | early, mid, late | Roshan, purchases, and inventory regression |
| `8855242704` | 1,266 | early, mid, late | Long final-interval and XP regression |
| `8856501050` | 1,654 | early, mid, late | 93-minute stress fixture |
| `8860187335` | 910 | early, mid, late | Medium extended fixture with multiple Aegis windows |
| `8868259993` | 312 | early, mid | Canonical short integration fixture |
| `8974053011` | 662 | early, mid, late | Aegis-denial lifecycle regression |

Every player route is included rather than selecting only high-farm heroes.
That captures the different movement patterns of professional carries, mids,
offlaners, and supports without pretending the replay's coarse `lane_role`
number is an authoritative strategic-role label.

All four topology areas were exercised: 3,013 jungle, 1,207 triangle, 767
river, and 827 flooded-area segments. The phase split was 912 early, 2,413
mid, and 2,489 late segments. Lane-to-jungle movement and brief crossings are
therefore present in the factual segment totals rather than hand-picked as
subjective examples.

## Evidence-strength observations

| Evidence strength | Observed segments |
| --- | ---: |
| `strong_farm_evidence` | 2,007 |
| `weak_farm_evidence` | 1,319 |
| `transit_like` | 2,488 |

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
