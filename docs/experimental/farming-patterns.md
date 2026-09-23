# Farming Patterns

`Farming Patterns` is an experimental, evidence-first view of sampled hero
routes through calibrated neutral-camp zones. It answers a narrower and more
defensible question than the original report:

> Which camp-local route segments were observed, and how much replay evidence
> supports treating each segment as farming rather than transit?

The route builder is available as `gem.build_farming_routes(match)`. The same
records feed the HTML report and the flat DataFrame exports.

> [!IMPORTANT]
> A route segment is not proof of player intent or a complete camp clear.
> `strong_farm_evidence`, `weak_farm_evidence`, and `transit_like` describe the
> available evidence only.

## Current scope

This first evidence-first layer hardens route reconstruction and exposes its
provenance. It uses facts already present on `ParsedMatch`:

- sampled positions from `ParsedPlayer.position_log`;
- calibrated camp geometry from `camp_zones.json`;
- neutral damage and deaths from the combat log;
- sampled total XP and total-earned-gold endpoints.

It does not change replay parsing or add extractor state.
Samples before `ParsedMatch.game_start_tick` are excluded, so pre-horn movement
does not become a farming segment.

The older objective-aware context scorer still appears in the report as a
secondary compatibility view. Its exclusive labels (`Safe Home Farm`, `Forced
Home Farm`, and so on) are not the primary public interpretation. If a fresh XP
window or map-context bucket is unavailable, the report says `Context
Unavailable` instead of inserting a neutral value.

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
- camp ID and family;
- every sampled route point;
- total and in-zone sample counts;
- sampled-window coverage and largest supported gap;
- whether a micro-exit was merged;
- neutral deaths and neutral damage;
- XP and total-earned-gold deltas when both endpoint samples are fresh;
- evidence reasons and evidence gaps.

Neutral events must fall inside the segment window, target an
`npc_dota_neutral*` unit, and be attributable through either
`attacker_name` or `damage_source_name`. When an event has coordinates, those
coordinates must also lie inside the segment's camp zone. An event without
coordinates remains attributable by the bounded time window and source.

XP and gold stay `None` when fresh endpoints are unavailable. They are never
converted to zero. The route status becomes `partial` when a segment has these
resource gaps.

## Evidence strength

Evidence strength is deliberately small and composable:

| Value | Rule |
|---|---|
| `strong_farm_evidence` | At least one attributed neutral death |
| `weak_farm_evidence` | No neutral death, but neutral damage or supported dwell |
| `transit_like` | Camp-local route samples without any of the support above |

The labels do not assert that the hero cleared the camp, earned every resource
from that camp, or intended to farm. Fresh XP/gold deltas remain visible as
window context, but a brief touch is not promoted solely because passive or
off-zone resources changed.

## Availability

Each `FarmingRoute` has one of three statuses:

- `complete`: route reconstruction succeeded and every segment has fresh
  resource endpoints;
- `partial`: route reconstruction succeeded, but one or more segment resource
  windows are unavailable;
- `unavailable`: camp geometry or player position samples are unavailable.

The corresponding `status_reasons` and per-segment `evidence_gaps` are public.
The bundled catalog currently reports version `1` and a 7.40 map-geometry
baseline; its camp-family annotations include the confirmed 7.41 updates.

## DataFrames

`gem.to_dataframe(match)` adds three stable flat tables:

- `farming_routes`: player-level availability, catalog metadata, and counts;
- `farming_route_segments`: boundaries, support facts, strength, and gaps;
- `farming_route_points`: sampled path, selected camp, base-zone membership,
  discontinuity reason, and segment membership where applicable.

String enums are exported as their raw values. Lists of reasons/gaps use
semicolon-delimited strings, matching the other flat analysis exports.

## Report behavior

The Farming tab leads with the route and timeline. Each segment row separates:

- evidence strength;
- exact support facts and missing evidence;
- the legacy context label;
- legacy context drivers.

The playback trail uses the route builder's point-to-camp assignments rather
than recalculating geometry in the report. This keeps Python, DataFrame, and
HTML behavior aligned.

## Compatibility and next work

The existing `build_map_context_timeline(...)`,
`score_camp_visit_context(...)`, and `CampVisitContext` API remain available.
The report keeps their six qualitative labels as a clearly marked legacy
compatibility view; no public field has silently changed meaning.

The next hardening layer for issue #195 is intentionally separate. It will add
composable territorial and context tags, comparative pressure inputs,
bounded enemy-presence and visibility provenance, tower/Aegis/Roshan/Tormentor
context completeness, camp side/topology, distance travelled, and a calibrated
multi-replay corpus. Until then, prefer the raw route evidence over the legacy
context labels.

## Source map

- `src/gem/analysis/farming.py`
- `src/gem/analysis/map_context.py`
- `src/gem/data/camp_zones.json`
- `src/gem/results/dataframes.py`
- `src/gem/reports/sections/vision.py`
