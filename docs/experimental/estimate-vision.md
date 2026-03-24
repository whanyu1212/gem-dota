# Estimate Vision

`estimate_vision` is an experimental post-parse helper that tries to answer a simple but important question:

> At tick `t`, did team `X` likely have vision of map point `(x, y)`?

This question matters for practical replay analysis:

- was an initiation blind or telegraphed?
- did a smoke break in enemy vision?
- was a gank visible before it happened?
- was a ward or hero actually giving information at that location?

The replay does not give gem a perfect, terrain-accurate fog-of-war oracle. So `estimate_vision` is intentionally implemented as a geometry-based approximation with explicit inputs and explicit limits.

> [!IMPORTANT]
> `estimate_vision` is useful, but it is not true fog-of-war reconstruction.
>
> It gives a defensible first-pass answer for many analytical workflows, not a terrain-perfect verdict.

## What the function returns

API:

```python
gem.estimate_vision(
    match: ParsedMatch,
    team: int,
    tick: int,
    x: float,
    y: float,
) -> list[VisionSource]
```

It returns a list of `VisionSource` objects sorted by ascending distance.

Each source is one thing that plausibly grants vision of the queried point:

- an allied hero
- an allied observer ward
- a vision-granting modifier reveal

If the list is empty, the point is treated as in fog for that team under the current approximation.

## Why this is experimental

True Dota vision depends on more than Euclidean distance:

- cliffs and high-ground rules
- trees and terrain occlusion
- hero-specific or item-specific vision changes
- summons and creep vision
- special reveal mechanics

gem does not reconstruct all of that. Instead, `estimate_vision` deliberately uses the subset it can model reliably from parsed replay data.

That tradeoff is why the feature belongs in `Experimental Features` instead of being presented as a final truth layer.

## Inputs used by the model

The current implementation in `src/gem/analysis.py` uses these inputs:

- `match.players`
- `player.position_log`
- `match.wards`
- `match.vision_modifiers`
- `match.game_start_tick`
- the queried `(team, tick, x, y)`

These are all replay-derived structures. The approximation begins when gem interprets them geometrically.

## High-level derivation

The function works in four steps.

### 1. Determine whether it is day or night

Dota vision changes with the day/night cycle, so the function first asks whether the queried tick is daytime.

Current constants in `src/gem/analysis.py`:

```text
day hero vision   = 1800
night hero vision = 800
ward vision       = 1600
full cycle        = 15 minutes
night starts      = 7:30 into the cycle
tick rate         = 30 ticks/sec
```

Derived tick constants:

```text
DAY_NIGHT_CYCLE_TICKS = 15 * 60 * 30 = 27000
NIGHT_START_TICKS     = 7 * 60 * 30 + 15 * 30 = 13950
```

The function converts absolute replay tick into game-relative tick:

```text
game_ticks = max(tick - game_start_tick, 0)
phase      = game_ticks % 27000
daytime    = phase < 13950
```

Interpretation:

- before `7:30`, it is day
- after `7:30`, it is night
- after `15:00`, the cycle repeats

This yields the hero vision radius for the rest of the check.

## 2. Check allied hero vision

For every player on the queried team:

1. get the hero position at the queried tick with `position_at_tick(...)`
2. compute Euclidean distance from the hero position to `(x, y)`
3. compare that distance to the current day/night hero radius

If:

```text
distance <= hero_radius
```

then that hero is included as a `VisionSource(kind="hero", ...)`.

### Why this works reasonably well

For many tactical replay questions, the first-order question is simply:

> Was an allied hero physically close enough that the target point was probably visible?

That is exactly what this check tries to answer.

### What it ignores

This hero check does **not** model:

- cliffs
- trees
- special hero vision bonuses
- temporary vision reductions or increases

So it is best understood as a straight-line radius test around the hero's estimated position.

## 3. Check observer ward vision

For every observer ward on the queried team:

1. ignore sentries
2. ignore wards with missing coordinates
3. require the ward to have already been placed by the queried tick
4. require the ward to still be alive
5. compute Euclidean distance from ward position to `(x, y)`
6. compare that distance to the fixed observer radius `1600`

If:

```text
distance <= 1600
```

then the ward is included as a `VisionSource(kind="ward", ...)`.

The alive check is:

```text
ward.tick <= query_tick
and query_tick <= (ward.killed_tick or ward.expires_tick)
```

with the usual handling for missing kill / expire ticks.

### Why wards are simpler than heroes

Observer wards do not have a day/night penalty in this model. They use a single constant vision radius.

That keeps the ward part of the approximation fairly straightforward.

## 4. Check vision-granting modifiers

This is the least obvious part of the function, and it is where the derivation matters most.

gem tracks certain reveal modifiers during parse and stores them in:

```python
match.vision_modifiers
```

Each event records:

- when the reveal started
- when it ended
- which modifier caused it
- which hero was revealed
- which team applied it

The current function then applies this rule:

1. keep modifier events where `caster_team == team`
2. require the modifier to be active at the queried tick
3. find the revealed target hero
4. get that hero's position at the queried tick
5. treat that revealed hero position as a vision source for the query

Unlike hero and ward checks, modifier reveals do **not** use a radius gate in this approximation.

Instead, the function always adds a `VisionSource(kind="modifier", vision_radius=0)` once the modifier is active and the target hero position can be resolved.

The reported `distance` is:

```text
distance(revealed_hero_position, query_point)
```

Interpretation:

- if the query point is exactly the revealed hero's position, distance is `0`
- if the query point is near that hero, distance is small
- if the query point is far from that hero, distance is large

The modifier source still appears because the revealed hero itself is considered directly seen.

### Why `vision_radius = 0` for modifiers

Because this is not a radius-based visibility check in the same sense as hero or ward vision.

The modifier is treated as a direct reveal mechanism. So `vision_radius = 0` is really a signal that says:

> this source was not accepted because of a radius threshold; it was accepted because the target was actively revealed

### Tracked modifier families

The docs already list the current modifier set in the API reference, including examples like:

- Slardar Corrosive Haze
- Bounty Hunter Track
- Dust of Appearance
- Gem of True Sight

Those are the reveal-style effects the current approximation extends beyond pure geometry.

## Data flow behind `match.vision_modifiers`

`estimate_vision` only works because the parser already extracts reveal-style modifier events during parse.

The high-level flow is:

1. combat log normalization sees relevant modifier add/remove events
2. gem records them as `VisionModifierEvent`
3. `match_builder` places them onto `ParsedMatch.vision_modifiers`
4. `estimate_vision` reads them later during post-parse analysis

This means the function is not inventing modifier state from scratch at query time. It consumes a replay-derived event stream that was already captured during parsing.

For the event-stream derivation itself, see [Vision Modifiers](./vision-modifiers.md).

## Exact decision model

The practical decision model is:

```text
vision_sources = []

if allied hero is within day/night hero radius:
    add hero source

if allied observer ward is alive and within 1600:
    add ward source

if allied reveal modifier is active on an enemy hero:
    add modifier source based on the revealed hero position

sort all accepted sources by ascending distance
return them
```

The function therefore answers:

> Which modeled sources support the claim that this team could see this point?

not:

> Can we reconstruct Valve's exact internal fog-of-war state?

## Why distance sorting matters

The function sorts accepted sources by ascending distance before returning them.

That makes the first source a useful first explanation:

- nearest hero vision
- nearest ward
- nearest revealed-hero modifier source

This is especially useful in analyst tooling and reports where you want a compact answer like:

- \"Radiant had vision via observer ward\"
- \"Dire had vision via Shadow Demon\"
- \"Dire had reveal via modifier_bounty_hunter_track\"

## What this approximation does well

It works reasonably well for questions like:

- \"Was this blink initiation likely visible?\"
- \"Did this ward plausibly cover that ramp?\"
- \"Was the target hero explicitly revealed by Track or Corrosive Haze?\"
- \"Was there any obvious allied source that should have seen this point?\"

These are practical analyst questions, and straight-line geometry captures a large fraction of them usefully.

## What this approximation does poorly

It is weaker for questions where terrain and line-of-sight dominate:

- exact uphill/downhill vision disputes
- tree occlusion edge cases
- unusual hero-specific vision ranges
- summon-based scouting
- precise Dust/Gem aura geometry

This is where the feature should be treated as suggestive, not definitive.

## Limitations by source type

### Heroes

Limitations:

- uses nearest sampled hero position, not continuous movement
- ignores terrain and cliffs
- assumes a generic day/night radius

### Wards

Limitations:

- uses simple circular coverage
- ignores terrain-specific ward vision interactions
- ignores all non-observer sight sources

### Modifiers

Limitations:

- the query uses the revealed hero position, not a full reveal field
- Dust / Gem auras are approximated as direct reveals once tracked
- modifier coverage is only as good as the extracted modifier event stream

## Relationship to `position_at_tick`

`estimate_vision` depends on `position_at_tick(...)` for hero positions and revealed-target positions.

That means its output inherits the assumptions of sampled movement:

- position logs are discrete samples, not full continuous trajectories
- the nearest sample is used for the queried tick

This is usually acceptable for high-level tactical questions, but it still matters for fine edge cases.

## Why this is still useful

Even with the limitations, the function is valuable because the alternative is often much worse:

- manually eyeballing the replay
- guessing whether a ward covered an area
- ignoring reveal modifiers entirely
- treating every initiation as either obviously seen or obviously blind

`estimate_vision` gives a structured, repeatable approximation with explicit source objects and explicit caveats.

That is a good fit for automated replay analysis, agentic workflows, and report generation.

## How to interpret the output responsibly

Use the function as:

- a first-pass visibility check
- an explanation generator for likely vision sources
- a screening tool for \"visible vs likely fogged\" situations

Do **not** use it as:

- final proof of true fog-of-war state
- exact terrain-aware scouting reconstruction
- a substitute for replay review in high-stakes edge cases

## Example reasoning workflow

If a gank starts at `(x, y)` on tick `t`, a good workflow is:

1. call `estimate_vision(match, team, t, x, y)`
2. inspect whether the list is empty
3. if not empty, inspect the nearest source
4. check whether that source is a hero, ward, or modifier reveal
5. confirm visually in replay if the situation is high stakes or terrain-sensitive

That makes the function useful without pretending it is perfect.

## Code locations

Implementation and supporting structures:

- `src/gem/analysis.py`
- `src/gem/models.py`
- `src/gem/match_builder.py`
- `docs/reference/analysis.md`

## Related reading

1. [Analysis Helpers](../reference/analysis.md)
2. [Vision Modifiers](./vision-modifiers.md)
3. [Replay Edge Cases](../deep-dives/replay-edge-cases.md)
4. [Experimental Features](./index.md)
