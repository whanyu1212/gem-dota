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

The analysis hardens route reconstruction and attaches comparative context
without collapsing the evidence into a single safety or quality score. It uses
facts already present on `ParsedMatch`:

- sampled positions from `ParsedPlayer.position_log`;
- calibrated camp geometry from `camp_zones.json`;
- neutral damage and deaths from the combat log;
- sampled total XP and total-earned-gold endpoints;
- bounded allied and enemy presence near each camp;
- modeled point-vision sources and gaps;
- lane-affiliated tower state;
- Roshan, Aegis, and Tormentor provenance;
- sustained comparative territory coverage and depth.

It does not change replay parsing or add extractor state.
Samples before `ParsedMatch.game_start_tick` are excluded, so pre-horn movement
does not become a farming segment.

The older objective-aware context scorer remains callable for compatibility,
but its exclusive labels (`Safe Home Farm`, `Forced Home Farm`, and so on) are
not the primary public interpretation. Context gaps remain explicit instead of
becoming neutral values.

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
            [tag.value for tag in segment.context.tags],
            segment.context.status_reasons,
        )
```

The public records are:

- `FarmingRoute`: one result per parsed player;
- `FarmingRoutePoint`: one sampled position with deterministic camp membership;
- `FarmingRouteSegment`: one camp-local window and its support evidence;
- `FarmingRouteConfig`: the inspectable reconstruction thresholds;
- `FarmingContextConfig`: comparative context windows and tag thresholds;
- `FarmingSegmentContext`: raw comparative facts, provenance, tags, and gaps;
- `FarmingContextTag`: independent stable string tags;
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
window context, but a brief touch is not promoted solely because passive or
off-zone resources changed.

## Comparative context

Each segment exposes its camp owner, lane affinity, area, catalog/geometry/
topology versions, contiguous distance travelled, and a nested
`FarmingSegmentContext`. Context is evaluated at the segment midpoint with
bounded lookback windows. The defaults are:

| Setting | Default | Meaning |
|---|---:|---|
| `lookback_ticks` | `2700` | 90-second local-presence window |
| `territory_lookback_ticks` | `3600` | Two-minute sustained territory window |
| `max_position_gap_ticks` | `300` | Do not bridge position gaps over 10 seconds |
| `max_resource_age_ticks` | `60` | Team economy/XP samples must be within two seconds |
| `max_vision_position_age_ticks` | `150` | Hero sources for point vision must be within five seconds |
| `presence_radius` | `1600` | Camp-local comparison radius in world units |
| `min_presence_coverage` | `0.70` | Minimum player-time coverage for a presence comparison |
| `high_enemy_presence_seconds` | `30.0` | Absolute enemy hero-seconds floor |
| `presence_advantage_seconds` | `15.0` | Enemy-minus-allied hero-seconds floor |
| `territorial_depth_delta` | `0.10` | Sustained normalized depth-advantage floor |
| `territorial_coverage_delta_pct` | `0.50` | Sustained enemy-side coverage advantage in percentage points |

The tags are independent and composable:

- `own_side`, `enemy_side`, or `border` comes from explicit camp topology;
- `high_enemy_presence` requires complete coverage plus both an absolute and a
  comparative enemy hero-seconds threshold;
- `vision_disadvantage` means the opponent has modeled observer coverage at
  the camp while the player's team does not. It is not proof of fog state;
- `tower_disadvantage` compares the remaining tier-one/tier-two towers in the
  camp's affiliated lane;
- `enemy_aegis_active` uses the bounded hardened Aegis lifecycle;
- `territorial_advance` requires an enemy-side segment and sustained paired
  coverage/depth advantage;
- `incomplete_context` carries exact gap codes whenever any required dimension
  is missing or stale.

Observer wards are only one modeled source. Authoritative hero visibility is
not generalized into arbitrary-point fog claims.

## Availability

Each `FarmingRoute` has one of three statuses:

- `complete`: route reconstruction succeeded and every segment has fresh
  resource endpoints;
- `partial`: route reconstruction succeeded, but one or more segment resource
  windows are unavailable;
- `unavailable`: camp geometry or player position samples are unavailable.

The corresponding `status_reasons` and per-segment `evidence_gaps` are public.
The bundled catalog reports version `2`, a 7.40 map-geometry baseline, and 7.41
camp-family/topology annotations. Geometry and topology provenance remain
separate so the metadata does not imply that the legacy geometry was redrawn.

## DataFrames

`gem.to_dataframe(match)` adds four stable flat tables:

- `farming_routes`: player-level availability, catalog metadata, and counts;
- `farming_route_segments`: boundaries, support facts, strength, comparative
  context, provenance, and gaps;
- `farming_route_points`: sampled path, selected camp, base-zone membership,
  discontinuity reason, and segment membership where applicable.
- `farming_context_tags`: one row per segment/tag with its reasons and context
  status.

String enums are exported as their raw values. Lists of reasons/gaps use
semicolon-delimited strings, matching the other flat analysis exports.

## Report behavior

The Farming tab leads with the route and timeline. Each segment row separates:

- evidence strength;
- exact support facts and missing evidence;
- composable context tags;
- an expandable explanation of comparative inputs, provenance, and gaps.

The playback trail uses the route builder's point-to-camp assignments rather
than recalculating geometry in the report. This keeps Python, DataFrame, and
HTML behavior aligned.

## Compatibility and next work

The existing `build_map_context_timeline(...)`,
`score_camp_visit_context(...)`, and `CampVisitContext` API remain available
with their existing meanings. The report retains only a collapsed formula
reference for that legacy heuristic; new code should use segment context and
tags.

There is deliberately no one-to-one label migration:

| Legacy label family | New evidence-first interpretation |
|---|---|
| `Safe Home Farm` | `own_side` plus separate route strength and raw context; no replacement tag claims safety |
| `Cautious Home Farm` / `Forced Home Farm` | `own_side` may compose with `high_enemy_presence`, `vision_disadvantage`, `tower_disadvantage`, `enemy_aegis_active`, or `incomplete_context`; gem no longer infers that the player was forced |
| `Safe Invade` | `enemy_side` may compose with `territorial_advance`; neither tag claims the route was safe or correct |
| `Contested Invade` / `High-Risk Invade` | `enemy_side` plus whichever comparative disadvantage tags are actually supported; no aggregate risk grade is substituted |

Consumers that still require the six exclusive labels must call the legacy
scorer explicitly during its compatibility period. Existing legacy fields keep
their old semantics; they are not silently populated with new tag values.

Calibration records factual evidence distributions and threshold sensitivity,
not subjective judgments about whether a route was strategically correct. See
[Farming Context Calibration](./farming-patterns-calibration.md).

## Source map

- `src/gem/analysis/farming.py`
- `src/gem/analysis/farming_context.py`
- `src/gem/analysis/map_context.py`
- `src/gem/data/camp_zones.json`
- `src/gem/results/dataframes.py`
- `src/gem/reports/sections/vision.py`
