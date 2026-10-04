# Experimental Features

The records in this section join several replay facts into one record per
route, Roshan, smoke, fight or point. They hold no tags, scores or verdicts: gem
reports what the replay shows, and answering questions from it is left to you
(see the [Recipes](../cookbook/questions.md)).

## What makes them experimental

- They join facts that the replay records separately, such as a camp catalog
  and sampled positions, or a Roshan kill and the fights that followed.
- Some of their choices are analytical rather than read from the replay: window
  lengths, segment boundaries, and evidence categories such as
  `strong_farm_evidence`.
- Those choices, and the record fields, may still change between releases.

> [!IMPORTANT]
> Experimental does **not** mean guessed.
>
> Each page states its inputs, windows and boundaries, and every field is either
> a replay fact or a documented derivation of one. Where the replay lacks
> evidence, the record says so instead of filling the gap.

## Available experimental features

| Feature | What it tries to answer |
|---|---|
| [Farming Patterns](./farming-patterns.md) | Which camp-local routes were observed, and what supports farming rather than transit |
| [Farming Route Calibration](./farming-patterns-calibration.md) | Which real-replay facts and targeted boundaries the farming-route corpus guards |
| [Roshan Conversion](./rosh-conversion.md) | What happened after each Roshan kill: the Aegis lifecycle, and the fights, structures, economy, wards and Tormentors in the window |
| [Roshan Conversion Calibration](./rosh-conversion-calibration.md) | Which real-replay attribution, lifecycle and fight-association facts the Roshan corpus guards |
| [Smoke Analysis](./smoke-analysis.md) | When each smoked hero gained and lost the modifier, what the enemy could see, and what happened next |
| [Fight Positioning](./fight-positioning.md) | How both teams were arranged at four bounded fight moments, with position freshness and opposing-team visibility kept explicit |
| [Fight Timeline](./fight-timeline.md) | What each hero cast in a fight, who it hit and for how much, what hit each hero before it died, and the gold and XP paid for each kill |
| [Point-Vision Evidence](./estimate-vision.md) | Bounded hero/observer geometry with explicit support, incompleteness, provenance, and separate target evidence |
| [Vision Modifiers](./vision-modifiers.md) | Which reveal-style modifier windows gem tracks, how they are derived from combat-log events, and how they feed later vision analysis |

## Recommended reading order

1. [Bits & Bytes Primer](../cookbook/bits-and-bytes-primer.md)
2. [Parser Internals](../deep-dives/index.md)
3. [Reports](../reports/index.md)
4. [Farming Patterns](./farming-patterns.md)
5. [Farming Route Calibration](./farming-patterns-calibration.md)
6. [Roshan Conversion](./rosh-conversion.md)
7. [Roshan Conversion Calibration](./rosh-conversion-calibration.md)
8. [Smoke Analysis](./smoke-analysis.md)
9. [Fight Positioning](./fight-positioning.md)
10. [Fight Timeline](./fight-timeline.md)
11. [Point-Vision Evidence](./estimate-vision.md)
12. [Vision Modifiers](./vision-modifiers.md)

The first three tell you where the underlying replay data comes from. The pages
in this section explain how gem joins that data into each record, and what the
record does and does not establish. The map regions and camp catalog these
records use are on [Map Regions and Camps](./map-annotations.md).
