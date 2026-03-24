# Farming Patterns

`Farming Patterns` is an experimental interpretation layer that sits on top of parsed replay data and tries to answer a practical analyst question:

> Where is a hero choosing to farm, and what does that route say about map safety, pressure, and objective state?

This feature currently appears in the HTML match report as the `Farming` tab.

> [!IMPORTANT]
> This is **not** a ground-truth "which neutral camp was definitely cleared" feature.
> 
> It is a route-and-context feature. It is designed to surface farming intent and map usage patterns, with explicit support signals and explicit caveats.

## Why this feature exists

A raw hero trail is not enough.

If you only plot position samples on the map, you can see where a hero moved, but you still cannot answer the questions analysts actually ask:

- Was this normal home-side farming or a forced contraction into safe camps?
- Was the carry taking enemy space or just crossing the river briefly?
- Did tower losses, ward coverage, or Aegis pressure change where the hero felt allowed to farm?
- Are we looking at a comfortable route, a cautious route, or a punishable invade?

The replay does not give a single built-in field for any of those interpretations. The feature has to derive them by combining multiple lower-level signals.

## What the replay gives us directly

The feature is built from facts gem can already parse:

- hero position samples (`player.position_log`)
- camp metadata and calibrated camp zones
- tower death state
- Aegis pickup / deny events
- Roshan and Tormentor events
- observer ward activity
- net-worth and XP advantage snapshots
- enemy hero movement density by region
- neutral kills, neutral damage, and XP gained during visit windows

Those are real replay-derived facts. The `Farming Patterns` feature begins once gem starts combining them.

## What the replay does **not** give us directly

The replay does **not** directly tell us:

- true per-player fog-of-war state at every moment
- real map control ownership as a clean scalar
- whether a hero's exact intention was "farm", "cut wave", "scout", or "move through"
- a built-in label like `safe_home_farm` or `high_risk_invade`

So the feature is intentionally framed as a heuristic layer, not replay truth.

> [!NOTE]
> The right way to evaluate this feature is not "is every label perfect?"
> 
> The right question is: "does this produce a defensible, readable first-pass explanation of the hero's farming route?"

## Design goals

The current implementation is trying to optimize for these goals:

1. Show farming **routes**, not just isolated camp dots.
2. Keep the output readable for humans, especially in the HTML report.
3. Use objective-aware context instead of treating every camp as equally safe.
4. Avoid pretending we know more than the replay actually tells us.
5. Make the heuristics inspectable: formulas, thresholds, and drivers are all visible.

## High-level pipeline

The feature works in five stages.

### 1. Build camp-local geometry

Each neutral camp has calibrated map geometry in `camp_zones.json`.

Instead of saying "nearest camp center wins", gem asks whether a hero sample falls inside the zone geometry for a specific camp. That reduces context blindness and makes nearby camps easier to distinguish.

### 2. Build route segments from hero movement

Hero movement is read from `player.position_log`.

A route segment is created when a hero spends time moving through or around a camp zone. The feature no longer tries to draw a strict binary line between "actual farm" and "transit" because, for route analysis, both often express the same strategic intent: this is space the hero is using.

Support signals are still recorded when available:

- neutral kills
- neutral damage
- XP gained during the segment window
- in-zone sample count

These support signals increase confidence, but they are not strict requirements.

### 3. Build objective-aware map context buckets

The feature constructs coarse 30-second map-context buckets for each team perspective.

Each bucket includes:

- towers alive on both teams
- whether mid T1 is still alive
- current Aegis state
- last Roshan / Tormentor timing
- active observer ward counts
- team net-worth advantage
- team XP advantage
- enemy movement density in three coarse regions:
  - own half
  - enemy half
  - river / border strip

This is the layer that tries to answer: "what did the map probably feel like around this time?"

### 4. Score each visit against the active bucket

For every route segment, gem computes three scores:

- `farm_safety_score`
- `pressure_score`
- `expected_value_score`

These are not learned model outputs. They are explicit formulas in code.

### 5. Assign an analyst-facing label and drivers

The final label is chosen from a small readable set:

- `Safe Home Farm`
- `Cautious Home Farm`
- `Forced Home Farm`
- `Safe Invade`
- `Contested Invade`
- `High-Risk Invade`

The label is accompanied by drivers such as:

- `lost_t1_mid`
- `enemy_aegis_active`
- `enemy_presence_high_own_half`
- `vision_deficit`
- `map_control_deficit`
- `border_zone_farm`
- `invading_enemy_half`
- `high_farm_value`

That combination is what makes the feature inspectable instead of opaque.

## Exact formulas

The current formulas come directly from `src/gem/map_context.py`.

### `clamp`

`clamp(x)` means: force the result into the range `[0.0, 1.0]`.

Examples:

- `clamp(1.18) = 1.0`
- `clamp(-0.12) = 0.0`
- `clamp(0.44) = 0.44`

Conceptually:

```python
clamp(x) = max(0.0, min(1.0, x))
```

### Safety

```text
Safety = clamp(
    0.55
    + 0.25 * tower_diff
    + 0.20 * ward_diff
    - 0.45 * enemy_own_half
    - 0.20 * enemy_aegis
    - 0.15 * invading
    - 0.08 * border_zone
)
```

Interpretation:

- starts from a neutral baseline of `0.55`
- goes up if your team owns more towers or has more observer coverage
- goes down if enemy presence on your side is high
- goes down when the enemy has Aegis
- goes down when you are farming enemy territory
- goes down slightly for border-zone camps near the map diagonal

### Pressure

```text
Pressure = clamp(
    0.30
    + 0.40 * enemy_own_half
    + 0.20 * enemy_river
    + 0.20 * max(0, -tower_diff)
    + 0.20 * enemy_aegis
    + invade_bonus
    + 0.08 * border_zone
)
```

Interpretation:

- starts from a lower baseline of `0.30`
- rises when recent enemy movement density is high
- rises when your team is down towers
- rises when the enemy has Aegis
- rises more if you are farming enemy territory
- rises slightly for camps near the border strip

### Invade bonus

```text
Invade Bonus = 0.15 + 0.15 * enemy_enemy_half   when invading
Invade Bonus = 0                                 otherwise
```

Interpretation:

Invading already makes the route riskier. It becomes even riskier if recent enemy presence is also high on their own side.

### Value

```text
Value = clamp(0.5 * camp_value + 0.5 * evidence)
```

Interpretation:

The route is considered more valuable when:

- the camp itself is economically valuable
- the visit window also contains stronger support signals

### Camp value by camp type

```text
small           -> 0.35
medium          -> 0.45
large           -> 0.55
ancient         -> 0.70
flooded_small   -> 0.40
flooded_medium  -> 0.50
fallback        -> 0.45
```

Interpretation:

This is a deliberately coarse economic prior. Ancients should push the score upward more than a small camp even before we look at supporting evidence.

### Evidence

`evidence` is a support score for meaningful interaction during the route segment.

It is built from three capped components:

```text
neutral_kill_component   = min(neutral_kills / 4.0, 1.0) * 0.35
neutral_damage_component = min(neutral_damage / 3000.0, 1.0) * 0.30
xp_component             = min(xp_gain / 600.0, 1.0) * 0.35

evidence = neutral_kill_component + neutral_damage_component + xp_component
```

Interpretation:

- more neutral kills support the idea that this was a meaningful farming segment
- more neutral damage supports the same
- XP gained also supports that interpretation

> [!TIP]
> `evidence` is not proof of a full neutral clear.
> 
> It is a support score used to make route segments more informative. The feature is intentionally route-first, evidence-second.

## Derived terms

### `tower_diff`

```text
tower_diff = (own_towers - enemy_towers) / 11
```

Why divide by `11`?

Because each team has 11 lane towers on a standard Dota map:

- top lane: T1, T2, T3, T4A, T4B = 5
- mid lane: T1, T2, T3 = 3
- bottom lane: T1, T2, T3 = 3

Total = `11`

This normalization keeps tower advantage on a compact scale before it is mixed into the safety and pressure formulas.

### `ward_diff`

```text
ward_diff = (own_observers - enemy_observers) / 6
```

Interpretation:

This is a coarse observer-coverage differential. Positive means your team currently has more active observer wards than the enemy.

### `winning`

```text
winning = net_worth_advantage >= 3500 or xp_advantage >= 4500
```

Interpretation:

This is a shortcut for "clearly ahead enough that own-side farming should not automatically be treated as forced".

### `losing`

```text
losing = net_worth_advantage <= -3500 or xp_advantage <= -4500
```

Interpretation:

This is a shortcut for "clearly behind enough that the same route may deserve a more defensive reading".

### `structural_deficit`

```text
structural_deficit = tower_diff < -0.25 or (lost mid T1 and ward_diff < -0.20)
```

Interpretation:

This tries to capture the moment where own-side farm stops looking like ordinary routing and starts looking structurally constrained.

### `border_zone`

```text
border_zone = camp center falls in the diagonal strip abs(x - y) <= 1200
```

Interpretation:

These camps sit near the central map boundary. They are treated as slightly less safe and slightly more pressured, but they do not receive a dedicated public label.

## Category rules

These are the current public labels.

### `Safe Home Farm`

Meaning:

Own-side farm with good cover and relatively low contest risk.

Rule:

```text
home side and safety >= 0.68 and pressure <= 0.40 and not losing
```

### `Cautious Home Farm`

Meaning:

Own-side farm with contest risk, but not enough stress to say the map is clearly forcing the hero inward.

Rule:

```text
fallback non-invade label when the visit is not safe and not forced
```

### `Forced Home Farm`

Meaning:

Own-side farm that looks reactive or constrained by map state.

Rule:

```text
(losing and pressure >= 0.52)
or (pressure >= 0.70 and not winning)
or (enemy Aegis and pressure >= 0.55 and not winning)
or (structural_deficit and pressure >= 0.45 and not winning)
```

### `Safe Invade`

Meaning:

Enemy-side farm taken while sufficiently ahead or stable to own that area.

Rule:

```text
invading
and safety >= 0.52
and pressure <= 0.48
and tower_diff >= -0.05
and ward_diff >= -0.10
and no enemy Aegis
and winning
```

### `Contested Invade`

Meaning:

Enemy-side farm with some risk, but not yet the most punishable invade state.

Rule:

```text
fallback invade label when the visit is not safe invade and not high-risk invade
```

### `High-Risk Invade`

Meaning:

Enemy-side farm that looks especially punishable.

Rule:

```text
invading and (
    pressure >= 0.70
    or (enemy Aegis and (enemy presence in enemy half >= 0.35 or losing))
)
```

## Driver definitions

Drivers explain *why* a label was assigned.

### `lost_t1_mid`

Trigger:

```text
own mid T1 is dead
```

Meaning:

Your side of the map is more open through the central entrance than in a stable early-game state.

### `enemy_aegis_active`

Trigger:

```text
Aegis is active and the holder team is the enemy team
```

Meaning:

This is short-lived but important objective pressure. It widens the window where aggressive enemy map occupation is plausible.

### `enemy_presence_high_own_half`

Trigger:

```text
enemy_own_half >= 0.45
```

Meaning:

Recent enemy movement density on your side of the map is high enough to materially affect route interpretation.

### `enemy_presence_high_river`

Trigger:

```text
enemy_river >= 0.45
```

Meaning:

Recent enemy movement density is high near the central diagonal / border region.

### `vision_deficit`

Trigger:

```text
ward_diff < -0.15
```

Meaning:

The enemy currently has better observer coverage than your team.

### `map_control_deficit`

Trigger:

```text
tower_diff < -0.15
```

Meaning:

Your team has lost enough towers that your side of the map is materially less secure.

### `border_zone_farm`

Trigger:

```text
camp center falls in the diagonal border strip
```

Meaning:

The route is using a camp in an area where ownership is naturally less stable, even if we no longer expose this as its own category.

### `invading_enemy_half`

Trigger:

```text
camp is on the enemy half of the map
```

Meaning:

The route is taking enemy-side space.

### `high_farm_value`

Trigger:

```text
value >= 0.70
```

Meaning:

The segment is either inherently valuable because of camp type, strongly supported by neutral / XP evidence, or both.

## How enemy presence is measured

Enemy presence is one of the most important parts of the model, so it is worth calling out explicitly.

gem looks at enemy hero position samples inside a recent time window and buckets them into three coarse regions:

- `river`
- `radiant_half`
- `dire_half`

Recent samples are weighted more heavily than older samples using exponential decay.

This is not a real influence map. It is a compact, practical pressure proxy.

### Current bucket settings

- context bucket width: `900` ticks = 30 seconds
- enemy-presence window: `2700` ticks = 90 seconds
- exponential decay tau: `900` ticks = about 30 seconds

Interpretation:

- the feature wants pressure to feel recent, not permanent
- but it also should not disappear instantly after one enemy pathing sample

## Why the feature is route-first, not clear-first

A common temptation is to demand a strict distinction between:

- `actual camp farm`
- `transit`

That sounds cleaner than it really is.

In practice, for analyst-facing route interpretation, the more useful question is often:

> Was this space part of the hero's farming pattern?

A carry can pass through a camp area very quickly, partially hit it, stack it, posture near it, or clip it while moving to the next camp. Those behaviors still matter for understanding map usage.

That is why the feature now treats camp-path segments as valid route segments and shows support signals instead of pretending every segment is a confirmed full neutral clear.

## Why there is no separate border-camp label

Earlier versions exposed a dedicated border / river-edge category.

That turned out to be too noisy and not very intuitive. The better approach is:

- keep border-zone geography in the scoring model
- expose it as a driver (`border_zone_farm`)
- let the public label still resolve to home-side or invade-oriented language

That gives the user the right contextual hint without bloating the label system.

## Why this feature is useful despite being heuristic

The feature is still valuable because it helps answer questions that are otherwise awkward to reconstruct manually:

- Is the carry repeatedly retreating into ancients and triangle camps?
- Are they looping own-side camps or stepping across the map boundary?
- Does a Roshan / Aegis window coincide with safer or more constrained routes?
- Is a winning core taking enemy space, or only threatening to do so?

The labels are not perfect truth. They are compact analyst summaries of route posture.

## Known limitations

> [!IMPORTANT]
> The current feature should be treated as a strong first-pass visualization, not a final tactical judge.

Current limits include:

- no true per-player fog-of-war reconstruction
- no terrain-aware line-of-sight model
- no exact camp-clear confirmation model
- threshold tuning is still match-dependent
- border-region and pressure heuristics can still overstate danger in some games
- short camp touches can introduce noise
- long routes can visually clump without careful playback use

## How to read the report correctly

The HTML report is easiest to interpret if you read it in this order:

1. scrub or play the route on the map
2. check the context label for the active segment
3. inspect the support signals
4. read the drivers
5. use the label as a summary, not as an unquestionable verdict

This is especially important for borderline cases like:

- short cross-river clips
- ancient-triangle loops during tense midgame windows
- losing teams that still briefly step into enemy space
- winning teams farming own side for efficiency rather than necessity

## Future tuning directions

Likely next improvements include:

1. better smoothing and time-window fading for long routes
2. region-aware thresholds by camp family instead of one global set
3. more stable enemy-presence modeling
4. optional higher-level grouping of micro-visits into larger farming stints
5. better tie-in with tower-state changes and Roshan windows
6. richer report interactions and explanations

## Code locations

If you want to inspect or tune the implementation directly:

- `src/gem/map_context.py`
- `examples/report/html_sections.py`
- `examples/report/style.py`
- `src/gem/data/neutral_camps.json`
- `src/gem/data/camp_zones.json`

## Related reading

1. [Reports](../reports/index.md)
2. [Replay Edge Cases](../deep-dives/replay-edge-cases.md)
3. [Extractors Layer](../deep-dives/extractors-layer.md)
4. [Analysis Helpers](../reference/analysis.md)
