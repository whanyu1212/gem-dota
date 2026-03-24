# Experimental Features

Features in this section are intentionally ambitious and still being tuned.

They are useful today, but they are not presented as exact replay ground truth. The goal is to expose higher-level interpretations that sit on top of gem's parsed replay data and make analytical workflows easier.

## What belongs here

An experimental feature usually has at least one of these properties:

- it combines multiple replay signals into a heuristic interpretation
- it answers a question the replay does not provide directly
- it makes useful tradeoffs between readability and precision
- its thresholds or labels will likely be refined over time

> [!IMPORTANT]
> Experimental does **not** mean random.
> 
> It means the feature is implemented carefully, with explicit formulas, inputs, thresholds, and caveats, but gem is honest that the output is still an interpretation layer.

## Available experimental features

| Feature | What it tries to answer |
|---|---|
| [Farming Patterns](./farming-patterns.md) | Where a hero is routing on the map, how safe or forced those routes look, and what objective state may be shaping those choices |
| [Roshan Conversion](./rosh-conversion.md) | Whether a team actually translated Roshan into fights, structures, territorial squeeze, or a game-closing sequence |
| [Estimate Vision](./estimate-vision.md) | Whether a team likely had vision of a point, which source provided it, and how that approximation is derived |
| [Vision Modifiers](./vision-modifiers.md) | Which reveal-style modifier windows gem tracks, how they are derived from combat-log events, and how they feed later vision analysis |

## Recommended reading order

1. [Bits & Bytes Primer](../cookbook/bits-and-bytes-primer.md)
2. [Deep Dives](../deep-dives/index.md)
3. [Reports](../reports/index.md)
4. [Farming Patterns](./farming-patterns.md)
5. [Roshan Conversion](./rosh-conversion.md)
6. [Estimate Vision](./estimate-vision.md)
7. [Vision Modifiers](./vision-modifiers.md)

The first three tell you where the underlying replay data comes from. The Experimental Features pages explain how gem turns that raw data into analyst-facing interpretations.
