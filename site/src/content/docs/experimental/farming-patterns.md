# Farming Patterns

`Farming Patterns` is an experimental, evidence-first view of sampled hero
routes through calibrated neutral-camp zones. It answers one question:

> Which camp-local route segments were observed, and how much replay evidence
> supports treating each segment as farming rather than transit?

The route builder is available as `gem.build_farming_routes(match)`. The same
records feed the HTML report and the flat DataFrame exports.

> [!IMPORTANT]
> A route segment is not proof of player intent or a complete camp clear.
> `strong_farm_evidence`, `weak_farm_evidence`, and `transit_like` describe the
> available evidence only.

## Current scope

The analysis reconstructs camp-local routes without scoring them. It uses facts
already present on `ParsedMatch`:

- sampled positions from `ParsedPlayer.position_log`;
- calibrated camp geometry from `camp_zones.json`;
- neutral damage and deaths from the combat log;
- sampled total XP and total-earned-gold endpoints.

It does not change replay parsing or add extractor state.
Samples before `ParsedMatch.game_start_tick` are excluded, so pre-horn movement
does not become a farming segment.

gem 0.13 removed the comparative "context" and tags that 0.12 attached to each
segment. Join the facts you need yourself: `gem.region_of`, the wards, towers and
Aegis events on `ParsedMatch`, and the players' positions.

## Public API

```python
import gem

match = gem.parse("match.dem")
routes = gem.build_farming_routes(match)

for route in routes:
    print(route.player_id, route.status, route.status_reasons)
    for segment in route.segments:
        print(
            segment.camp_id,
            segment.start_tick,
            segment.end_tick,
            segment.evidence_strength.value,
            segment.evidence_reasons,
            segment.evidence_gaps,
        )
```

The public records are:

- `FarmingRoute`: one result per parsed player;
- `FarmingRoutePoint`: one sampled position with deterministic camp membership;
- `FarmingRouteSegment`: one camp-local window and its support evidence;
- `FarmingRouteConfig`: the inspectable reconstruction thresholds;
- `FarmingCampZone`: normalized camp geometry;
- `FarmingEvidenceStrength` and `FarmingBoundaryReason`: stable string enums.

## Deterministic route reconstruction

The default configuration is:

| Setting | Default | Meaning |
|---|---:|---|
| `max_sample_gap_ticks` | `300` | Split after more than 10 seconds without a position sample |
| `max_contiguous_speed` | `900.0` | Split when implied movement exceeds 900 world units/second |
| `merge_gap_ticks` | `150` | Merge a same-camp micro-exit lasting at most 5 seconds |
| `min_weak_dwell_ticks` | `150` | Five seconds of supported dwell can count as weak evidence |
| `resource_max_age_ticks` | `60` | XP/gold endpoints must be within two seconds of a boundary |

All time conversions use 30 replay ticks per second.

### Zone selection

For each position sample:

1. If the hero was already assigned to a camp and remains inside that camp's
   exit-hysteresis geometry, retain the current camp.
2. Otherwise, collect every camp whose entry geometry contains the sample.
3. Resolve overlap by normalized distance to the camp geometry.
4. Resolve an exact tie by ascending camp ID.

This avoids catalog-order dependence and prevents boundary jitter from rapidly
switching between adjacent camps.

### Boundaries

Every segment exposes a `start_reason` and `end_reason`:

- `zone_entry` / `zone_exit`;
- `camp_change`;
- `sample_gap`;
- `large_jump`;
- `log_end`.

Sample gaps and large jumps are hard discontinuities. They never merge back
together. A short exit followed by re-entry into the same camp may merge, but
the merged record keeps `micro_exit_merged=True` and retains the intervening
out-of-zone point. `in_zone_sample_count` therefore remains distinct from
`sample_count`.

## Evidence attribution

Each segment retains:

- exact start/end ticks and duration;
- camp ID and `camp_type`;
- every sampled route point;
- total and in-zone sample counts;
- sampled-window coverage and largest supported gap;
- whether a micro-exit was merged;
- neutral deaths and neutral damage;
- cumulative total-earned-XP and total-earned-gold deltas when both endpoint
  samples are fresh;
- evidence reasons and evidence gaps.

Neutral events must fall inside the segment window, target an
`npc_dota_neutral*` unit, and be attributable through either
`attacker_name` or `damage_source_name`. When an event has coordinates, those
coordinates must also lie inside the segment's camp zone. An event without
coordinates remains attributable by the bounded time window and source.

XP comes from `ParsedPlayer.total_earned_xp_t`, not the level-local `xp_t`
counter that resets on level-up. XP and gold stay `None` when fresh endpoints
are unavailable. They are never converted to zero. The route status becomes
`partial` when a segment has these resource gaps.

## Evidence strength

Evidence strength is deliberately small and composable:

| Value | Rule |
|---|---|
| `strong_farm_evidence` | At least one attributed neutral death |
| `weak_farm_evidence` | No neutral death, but neutral damage or supported dwell |
| `transit_like` | Camp-local route samples without any of the support above |

The labels do not assert that the hero cleared the camp, earned every resource
from that camp, or intended to farm. Fresh XP/gold deltas remain visible as
window facts, but a brief touch is not promoted solely because passive or
off-zone resources changed.

## Camp facts on each segment

Each segment carries its camp's owner team, lane affinity and area, the
catalog, geometry and topology versions, and the contiguous distance travelled.

## Availability

Each `FarmingRoute` has one of three statuses:

- `complete`: route reconstruction succeeded and every segment has fresh
  resource endpoints;
- `partial`: route reconstruction succeeded, but one or more segment resource
  windows are unavailable;
- `unavailable`: camp geometry or player position samples are unavailable.

The corresponding `status_reasons` and per-segment `evidence_gaps` are public.
The bundled catalog reports version `4`, 7.41 map geometry, and 7.41
camp-family/topology annotations. Each zone is centred on its camp's
`CDOTA_NeutralSpawner` entity, which sits at the same position in every 7.41
fixture replay; neutral creeps spawn within about 100 units of it. Geometry and
topology provenance remain separate fields.

## DataFrames

`gem.results.dataframes.build_dataframes(match, include=["analysis"])` (or
`gem.parse_to_dataframe(path, include=["analysis"])`) adds three stable flat tables:

- `farming_routes`: player-level availability, catalog metadata, and counts;
- `farming_route_segments`: boundaries, support facts, strength, camp facts,
  provenance, and gaps;
- `farming_route_points`: sampled path, selected camp, base-zone membership,
  `boundary_before`, and segment membership where applicable.

String enums are exported as their raw values. Lists of reasons/gaps use
semicolon-delimited strings, matching the other flat analysis exports.

## Report behavior

The report's Farming tab shows the route and timeline for each team's cores
(see [Match Reports](../reports/index.md)). Each segment row lists the camp,
its type, the visit's duration, the hero's neutral kills inside the camp zone,
and the gold and XP the hero earned during the visit. Evidence strength stays
available in Python and the DataFrame exports but is not rendered.

The playback trail uses the route builder's point-to-camp assignments rather
than recalculating geometry in the report. This keeps Python, DataFrame, and
HTML behavior aligned.

## Calibration

The farming-route corpus records factual counts per fixture replay (segments,
points, evidence strength, phase, camp area) so that a change to route
reconstruction shows up as a difference. It makes no judgment about whether a
route was strategically correct. See
[Farming Route Calibration](./farming-patterns-calibration.md).

## Source map

- `src/gem/analysis/farming.py`
- `src/gem/data/camp_zones.json`
- `src/gem/results/dataframes.py`
- `src/gem/reports/sections/vision.py`
