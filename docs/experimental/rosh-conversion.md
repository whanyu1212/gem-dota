# Roshan Conversion

`Roshan Conversion` is an experimental analysis layer that asks a practical question:

> After securing Roshan, did the team actually turn that advantage into anything?

The replay tells us when Roshan died, who claimed Aegis, when towers and barracks fell, when buybacks happened, where heroes moved, and where teamfights were detected.

This feature joins those facts into a post-Roshan summary that tries to answer whether the window became:

- a fight advantage
- an objective push
- a territorial squeeze
- a game-closing sequence
- or a low-conversion window

## Why this is experimental

The replay does **not** contain a native field called `rosh_conversion`.

This page is describing an interpretation layer that combines:

- Roshan kills
- Aegis pickup / steal / deny events
- teamfight windows
- towers and barracks taken
- enemy buybacks forced
- observer wards placed in enemy territory
- movement-based territorial expansion after Roshan

That means the feature is useful, but still heuristic.

## Main windows

The analysis uses 3 nested windows.

### Immediate window

```text
rosh_tick -> rosh_tick + 180 seconds
```

This is the quick-read lens.

It answers questions like:

- did the team fight quickly after Roshan?
- did they hit a tower soon after?
- did their map presence expand immediately?

### Aegis window

```text
aegis_pickup_tick -> inferred consume / expire / deny
```

This is the main evaluation window.

If Aegis is consumed mid-fight, the overlapping fight is still counted in full. The report does **not** cut the fight in half at the consume tick.

### Extended window

```text
rosh_tick -> next Roshan or game end
```

This is only for broader context.

It is useful for questions like:

- did this Roshan lead into the final closing sequence?
- did the game state materially change before the next Roshan?

## Labels shown in the report

The report now separates 2 things:

1. the **conversion label**
2. the **Aegis outcome**

That split is intentional. A team can have a low-conversion Roshan and also have an Aegis that expired unused, or a low-conversion Roshan where the Aegis window was actively lost.

### Conversion labels

#### `Low Conversion`

Roshan was secured, but the window did not clearly translate into fights, structures, or territorial squeeze.

This is the fallback label when none of the stronger downstream signals fired.

#### `Fight Conversion`

Roshan mainly translated into won fights.

Used when post-Roshan fight results are favorable but structural conversion is not large enough to call it an objective push.

#### `Objective Conversion`

Roshan translated into clear structural damage.

Current rule of thumb:

- at least 2 towers, or
- any barracks

inside the main evaluation window.

#### `Map Squeeze`

Roshan mainly translated into territorial pressure rather than raw building damage.

This shows up when the Aegis side:

- places more forward observer wards, or
- meaningfully expands its enemy-half map presence

without a stronger fight/objective label taking priority.

#### `Game-Closing Rosh`

This Roshan fed directly into the final closing sequence before the game ended.

## Aegis outcomes

#### `Consumed In Fight`

The Aegis holder died once during the evaluated window and Aegis triggered.

#### `Expired After Use`

Aegis timed out, but the team still got useful value from the Roshan window before expiry.

#### `Expired Unused`

Aegis expired without a second life and without meaningful downstream conversion.

#### `Denied`

The Aegis was denied, so the immortality window never existed for that team.

#### `Window Lost`

The Aegis side lost the key window and did not offset that with structures.

Current rule of thumb:

- more fights lost than won
- and no towers / barracks taken

#### `Game Ended`

The game ended before Aegis could be consumed or expire normally.

#### `Unknown`

The replay does not let gem classify the Aegis lifecycle confidently.

## Important timing caveat

The Roshan report uses teamfight timing carefully.

`Teamfight.start_tick` in gem is padded backward by the detector cooldown window, so it is **not** a literal “combat began here” timestamp.

To avoid misleading timelines, the Roshan layer now uses:

- `first_death_tick` from the teamfight
- clamped against the Aegis window start when needed

So if a fight was already underway around the Roshan/Aegis transition, the report will say:

- `Fight already underway ...`

instead of pretending that combat began exactly at the padded fight-window start.

## Metrics shown in the report

### Fights

```text
wins-losses-draws
```

Counted from teamfight windows that overlap the main Aegis evaluation window.

### Objectives

```text
towers_taken / barracks_taken
```

Only enemy structures count.

### Enemy Buybacks

Count of enemy players whose `BUYBACK` events happened inside the Aegis evaluation window.

### Ward Delta

```text
Aegis-side observer wards placed in enemy half
- enemy observer wards placed in their own forward half
```

Positive means the Roshan team pushed vision deeper than the opponent did during the same window.

### Presence Delta

```text
enemy_half_farm_share_during - enemy_half_farm_share_before
```

Where:

- `enemy_half_farm_share_before` = percentage of holder-team position samples in the enemy half during the **3 minutes before Roshan**
- `enemy_half_farm_share_during` = percentage of holder-team position samples in the enemy half during the **first 3 minutes after Roshan**

The report shows this in **percentage points**.

Example:

- before: `22%`
- during: `37%`
- presence delta: `+15 pts`

This is a territorial-expansion proxy, not true map-control truth.

## Why there is no single score in the report

Earlier versions exposed a rolled-up score.

That looked tidy, but it is not a good apples-to-apples comparison because:

- late-game Roshan windows naturally have more game-ending leverage
- one tower at 18 minutes does not mean the same thing as one tower at 48 minutes
- some Roshan windows are more about squeeze and buybacks than raw structure count

So the report now favors:

- labels
- counts
- timelines
- drivers

instead of pretending the windows are directly comparable through one number.

## Current limits

- Aegis consume is inferred from the holder's first hero death before expiry, not from a dedicated “Aegis popped here” replay event.
- `Presence Delta` is movement-sample based, so it is a territorial proxy, not true control.
- Teamfight detection is still built on death-window clustering, so it is better at capturing meaningful engagements than perfectly timestamping every skirmish start.
- The labels are intentionally conservative and may still be tuned further on real match review.

## Related pages

1. [Reports](../reports/index.md)
2. [Farming Patterns](./farming-patterns.md)
3. [Estimate Vision](./estimate-vision.md)
4. [Vision Modifiers](./vision-modifiers.md)
