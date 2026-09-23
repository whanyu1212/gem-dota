# Teamfight Positioning

`build_teamfight_positioning(match)` reconstructs how the two canonical hero
rosters were arranged at four moments around each detected fight:

- ten seconds before the best available engagement-start tick
- engagement start
- the first hero death
- the end of the detected fight window

The analysis exposes spatial evidence. It does not grade positioning or claim
why a fight was won.

## Quick start

```python
import gem

match = gem.parse("match.dem")

for fight in gem.build_teamfight_positioning(match):
    print(fight.fight_index, fight.engagement_start_source.value)
    for snapshot in fight.snapshots:
        print(snapshot.kind.value, snapshot.tick, snapshot.centroid_distance)
        for hero in snapshot.heroes:
            print(
                hero.hero_name,
                hero.x,
                hero.y,
                hero.sample_age_ticks,
                hero.visibility.value,
            )
```

The builder is post-parse and deterministic. It reads existing teamfight,
position, visibility, smoke, and reveal timelines; it does not run another
extractor or modify the parsed match.

## Moment semantics

Gem's existing fight detector opens its window 15 seconds before the first
death and closes it 15 seconds after the last death. Those padded boundaries
are useful for attribution, but the opening boundary is not an observed combat
start.

The current positioning API therefore uses the exact first-death tick as the
conservative engagement-start fallback and exposes
`engagement_start_source="first_death_fallback"`. Consequently, the
`engagement_start` and `first_death` snapshots may share a tick. Both logical
moments remain in the result so a future, stronger start signal can be added
without changing the snapshot shape.

For legacy or manually constructed fights, the dataclass default
`first_death_tick=0` is treated as missing rather than as observed evidence. An
out-of-window first-death tick is also rejected. The builder then uses an
in-window `last_death_tick` with
`engagement_start_source="last_death_fallback"`; if neither death tick is
usable, it uses the nonnegative fight-window start with
`engagement_start_source="fight_window_start_fallback"`. The report labels
these degraded cases as death fallbacks instead of presenting them as exact
first-death observations.

## Sample freshness

Snapshot ticks are requested analytical moments. Hero coordinates are sampled
entity evidence, normally recorded about once per second. Every hero record
therefore retains:

- the requested snapshot tick
- the source position-sample tick
- the absolute sample age in ticks
- nullable coordinates and derived distances

The default freshness limit is 60 ticks, or two seconds at 30 ticks per second.
When the nearest sample is older, its tick and age remain available as
provenance, but the coordinates and all geometry derived from them become
unavailable. Missing evidence is never replaced by `(0, 0)`.

## Geometry and completeness

Only fresh canonical-player positions contribute to geometry. For each team,
the centroid is the arithmetic mean of its positioned heroes. Spread is the
root-mean-square distance from that centroid:

```text
sqrt(mean(distance(hero, team_centroid) ** 2))
```

Hero records also include distance from their team centroid and distance to the
nearest positioned ally and enemy. The snapshot exposes the distance between
team centroids when both are available.

Team completeness is:

| State | Meaning |
|---|---|
| `complete` | Every canonical team hero has a fresh position |
| `partial` | At least one, but not every, canonical team hero has a fresh position |
| `unavailable` | No canonical team hero has a fresh position |

Every canonical Radiant or Dire player is retained. Active participants are
identified using the existing direct-combat definition. Fresh nonparticipants
are separately marked as near or away from the combined active-participant
centroid using the configured radius; they are not silently dropped.

## Visibility, smoke, and reveals

`visibility` is the opposing team's state from the authoritative canonical-hero
visibility timeline and remains `visible`, `hidden`, or `unknown`. Gem does not
substitute arbitrary-point geometry for missing authoritative evidence.

Smoke and direct-target reveal context is reported only for bounded observed
half-open intervals. Open, ambiguous, unresolved, or otherwise incomplete
lifecycles become evidence-gap codes instead of active claims.

## DataFrames and reports

`gem.parse_to_dataframe(...)` and `gem.results.dataframes.build_dataframes(...)`
include a `teamfight_positioning` table with one row per fight, snapshot, and
canonical hero. Nullable values preserve unavailable geometry.

The HTML report presents the same four moments on one map. Team colour,
active/nonparticipant emphasis, visibility styling, short fresh-sample trails,
and an evidence note are descriptive only.

[Smoke/Fight Insights](./smoke-fight-insights.md) composes these snapshots with
smoke lifecycles and bounded exact events. The composed layer preserves each
position sample's tick and freshness rather than replacing exact action,
removal, or death ticks with sampled spatial times.

## Limitations

- Engagement start currently falls back to first death because the existing
  detector does not retain reliable pre-death event attribution for parallel
  fight windows.
- Positions are sampled, not exact event coordinates.
- The public position timeline does not expose per-snapshot life state, so the
  analysis does not claim whether a hero was alive, dead, or disconnected.
- Visibility is authoritative only for canonical player heroes and may remain
  unknown when the replay lacks a usable observation.
