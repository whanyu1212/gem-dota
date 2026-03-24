# Changelog

This page summarizes the latest parser, validation, and report changes that materially affect how `gem` behaves today.

It is intentionally short-range for now. It is **not** backfilled with older release history.

## March 2026

### Roshan conversion report was added as an experimental feature

There is now a dedicated `Roshan Conversion` report tab and a matching Experimental Features page.

The new report separates:

- the **conversion label** (`Low Conversion`, `Fight Conversion`, `Objective Conversion`, `Map Squeeze`, `Game-Closing Rosh`)
- the **Aegis outcome** (`Consumed In Fight`, `Expired After Use`, `Expired Unused`, `Denied`, `Window Lost`, `Game Ended`, `Unknown`)

Recent refinements:

- labels and Aegis outcomes are documented directly in the report
- the old single score was removed from the UI
- the report now explains how `Presence Delta` is calculated
- Roshan-fight timing now uses `first_death_tick` instead of the padded teamfight window start

This remains experimental because it is a replay-derived interpretation layer, not a native replay fact.

### Player sampling now stops at game end

`PlayerExtractor` now forces one final snapshot at the exact game-end tick and stops sampling after that point.

Why this mattered:

- some player time series were drifting into the postgame scoreboard window
- this could inflate late sampled values such as `net_worth_t`
- it created false mismatches when validating against OpenDota

Concrete impact:

- the sampled end state now reflects the actual replay game-end boundary
- the Tusk mismatch discovered during OpenDota validation was resolved by this fix

### Gold series were split into two distinct meanings

`gold_t` and `gold_t_min` now mean **current unspent gold only**.

`total_earned_gold_t` and `total_earned_gold_t_min` now mean **cumulative earned gold**.

Why this mattered:

- the older fallback path could mix current gold and cumulative gold into the same field
- that made economy analysis harder to reason about
- buyback, purchase timing, and “cash on hand” questions need current unspent gold
- advantage curves and lane-economy summaries need cumulative earned gold

Current state:

- current unspent gold is exposed
- cumulative earned gold is exposed
- reliable and unreliable gold are **not** exposed separately yet

### OpenDota validation harness was expanded

The OpenDota validator now supports more than a few pinned fixtures.

It can now:

- randomly sample candidate matches from OpenDota feeds
- download missing replays automatically
- validate in `scalar`, `parsed`, or `full` mode
- request OpenDota replay parsing when richer fields are missing
- write manifests and JSON result files for repeatable checks

Important validator clarification:

- final scalar checks use end-of-game values
- `[min]` fields are now treated as informational only
- the last whole-minute sample can legitimately precede game end by up to 59 seconds

### Farming-pattern context became more explainable

The experimental Farming Patterns work now has an explicit map-context layer.

That layer uses:

- tower state
- Roshan and Aegis timing
- ward counts
- net-worth and XP advantage
- recent enemy presence by region

Recent refinements:

- labels were made easier to read
- the old border/river special case was removed as a standalone category
- formulas, thresholds, drivers, and caveats are documented explicitly
- the report now treats route segments as useful farming-pattern evidence even when the support signals are noisy

This feature is still experimental by design.

### Replay edge cases are now documented directly

There is now a dedicated deep-dive page for replay-specific pitfalls, including:

- duplicate hero entities vs the canonical hero handle
- within-tick sampling caveats
- truncated or incomplete replays
- schema drift across builds
- inference limits for higher-level analytics

If you are debugging parser behavior, read this together with the Deep Dives and Experimental Features sections.

## Recommended follow-up pages

1. [Replay Edge Cases](./deep-dives/replay-edge-cases.md)
2. [Farming Patterns](./experimental/farming-patterns.md)
3. [Roshan Conversion](./experimental/rosh-conversion.md)
4. [Estimate Vision](./experimental/estimate-vision.md)
5. [Vision Modifiers](./experimental/vision-modifiers.md)
