# Point-Vision Evidence

gem exposes two different kinds of visibility evidence:

- `hero_visibility_at(...)` reads authoritative replay visibility for a
  canonical player hero.
- `assess_point_vision(...)` models whether the sources gem currently knows
  about could cover an arbitrary map coordinate.

These answers are deliberately kept separate. A geometric model can explain
possible sources, but it cannot prove Valve's terrain-aware fog-of-war state.

> [!IMPORTANT]
> An `unsupported` point assessment means only that no currently modelled
> source covered the point. It does not mean the replay proved that the point
> was hidden.

## Choosing the right API

| Question | API | Result |
|---|---|---|
| Could Radiant see player 7's canonical hero? | `hero_visibility_at(...)` | `visible`, `hidden`, or `unknown` |
| What modelled sources could cover `(x, y)`? | `assess_point_vision(...)` | Evidence-rich `PointVisionAssessment` |
| Which modelled geometry sources covered `(x, y)`? | `estimate_vision(...)` | Compatibility list of `VisionSource` |

Prefer the authoritative query whenever the subject is a canonical player
hero. Use the point assessment for empty map coordinates, source explanations,
or cases where authoritative entity visibility does not apply.

## Evidence-rich point assessment

```python
assessment = gem.assess_point_vision(
    match,
    team=2,
    tick=120_000,
    x=-1_250.0,
    y=2_400.0,
)

if assessment.status is gem.PointVisionStatus.SUPPORTED:
    for source in assessment.sources:
        print(source.kind, source.name, source.distance)
elif assessment.status is gem.PointVisionStatus.INCOMPLETE:
    for gap in assessment.gaps:
        print(gap.code, gap.subject)
else:
    print("No currently modelled source covered the point")
```

The assessment preserves the query inputs, evidence status, contributing
sources, and any evidence gaps. Its status is one of:

- `supported`: at least one fresh, modelled geometry source covers the point;
- `unsupported`: the relevant model inputs were available, but none covered
  the point;
- `incomplete`: missing or stale evidence could change an otherwise negative
  answer.

Support takes precedence over incompleteness. An assessment can therefore be
`supported` and still contain gaps for other allied heroes or wards. Consumers
that require complete evidence should inspect both `status` and `gaps`.

## Position freshness and provenance

Player positions are sampled, not continuous. The default parser samples at
roughly one-second intervals, but callers can configure a wider interval.

`assess_point_vision(...)` accepts `max_position_age_ticks`, which defaults to
150 ticks (five seconds at 30 ticks per second). A hero sample older than this
bound is excluded and recorded as a gap instead of being silently carried over
an arbitrary distance in time.

Every accepted sampled hero source records:

- the sampled world coordinate;
- the source sample tick;
- the absolute age of that sample at the query tick;
- sampled-position provenance;
- the canonical player ID when available.

The lower-level `position_sample_at_tick(...)` helper exposes the nearest
sample and its tick/age without applying a freshness policy. The older
`position_at_tick(...)` coordinate-only helper remains available.

The model never interpolates between samples. In particular, it does not draw a
path across a teleport or another large movement discontinuity.

## Modelled point sources

The point model currently accepts two source families.

### Allied canonical heroes

An allied hero supports the point when:

1. a position sample exists within the configured freshness bound; and
2. its straight-line distance to the point is within the modelled hero radius.

The model uses 1800 world units during the day and 800 at night. It does not
model hero-specific vision changes, cliffs, trees, or terrain occlusion.

### Allied observer wards

An observer supports the point when:

1. its team is known and matches the queried team;
2. its placement coordinates are available;
3. the query lies in its observed lifetime; and
4. its straight-line distance to the point is at most 1600 world units.

Ward lifetimes are half-open: placement is active at `ward.tick`, while the
observed kill or expiry tick is no longer active. This matches the entity
life-state transition that produced the terminal event.

An observer with no terminal event remains active only through the replay's
observed horizon. A query beyond that horizon is incomplete. Missing coordinates
or unknown team attribution are also gaps rather than negative evidence.

Sentry wards are kept distinct. They provide true sight but do not grant
standard map vision, so they are not point-coverage sources.

## Direct-target reveals are not point sources

Track, Corrosive Haze, and similar direct reveals answer a target question:

> Was this specific hero covered by a defensible direct-reveal interval?

They do not establish coverage of every arbitrary coordinate. Pass
`target_player_id` when the point corresponds to a canonical player hero:

```python
assessment = gem.assess_point_vision(
    match,
    team=3,
    tick=tick,
    x=x,
    y=y,
    target_player_id=4,
)

print(assessment.authoritative_visibility)
for reveal in assessment.direct_target_reveals:
    print(reveal.modifier_name, reveal.start_tick, reveal.end_tick)
```

The result exposes three independent facts:

- authoritative visibility of the canonical target, when applicable;
- geometry sources covering the coordinate;
- bounded direct-target reveal evidence for that target.

Only non-illusion hero applications with a supported team, unambiguous pairing,
and bounded observed interval are returned as direct-target evidence. Ambiguous
or incomplete matching evidence is preserved as a gap, not promoted into
coverage.

Authoritative `visible`, `hidden`, and `unknown` values are never blended with
the modelled point status. `unknown` does not mean hidden.

## Compatibility helper

`estimate_vision(...)` remains available for callers that need a simple,
distance-sorted `list[VisionSource]`:

```python
sources = gem.estimate_vision(match, team=2, tick=tick, x=x, y=y)
```

It now uses the same bounded hero-position and ward-lifetime rules as the
evidence-rich assessment. Its list shape cannot represent why evidence was
missing, so an empty list remains ambiguous. New code should use
`assess_point_vision(...)` whenever a negative result matters.

Direct-target modifiers are no longer returned as arbitrary point sources. Use
`target_player_id` on `assess_point_vision(...)` to request that separate
evidence.

## Day and night

The model uses a ten-minute cycle:

```text
day:   0:00 through 4:59.99
night: 5:00 through 9:59.99
```

The cycle repeats every 18,000 ticks at 30 ticks per second. If
`game_start_tick` is unavailable, tick zero is used as the fallback origin.

## Known limits

The assessment intentionally does not claim terrain-perfect vision. It omits:

- cliffs, trees, blockers, and patch-specific map geometry;
- summon, creep, building, and temporary ability vision;
- hero-specific day/night radius changes;
- exact rasterized fog-of-war state;
- attribution of authoritative visibility to one revealing source.

An observer circle or hero radius is evidence of modelled support, not proof
that terrain allowed vision. Conversely, `unsupported` is model non-support,
not proof of fog.

## Serialization

The assessment and its nested evidence records are public dataclasses. They can
be converted with `gem.to_dict(...)` or Python's `dataclasses.asdict(...)`:

```python
payload = gem.to_dict(assessment)
```

Point assessments are query results rather than persistent match timelines, so
they are not added as a separate `ParsedMatch` DataFrame or Parquet table.

## Validation boundaries

Tests cover:

- fresh, stale, and missing player positions;
- day/night range boundaries;
- observer placement, kill, and expiry equality;
- sentry separation and missing ward evidence;
- complete versus incomplete negative results;
- authoritative visible, hidden, and unknown target states;
- direct-target reveal separation;
- serialization and real-replay provenance.

For terrain-sensitive decisions, retain the assessment as screening evidence
and confirm the situation in the game replay.
