# Extractors

Extractors are stateful objects that attach to a `ReplayParser`, accumulate data during
parsing, and expose structured output when parsing is complete.

Each extractor subscribes to one or more events (entity events, combat log entries, or
user messages) via the parser's callback system. After `parser.parse()` completes, the
extractor's output properties are ready to read.

| Extractor | Module | What it collects |
|---|---|---|
| `PlayerExtractor` | `gem.extractors.players` | Hero/player state snapshots, time series, rune pickups |
| `ObjectivesExtractor` | `gem.extractors.objectives` | Tower kills, barracks, Roshan kills, Tormentor kills |
| `WardsExtractor` | `gem.extractors.wards` | Ward placements with coordinates |
| `CourierExtractor` | `gem.extractors.courier` | Courier state per tick |
| `DraftExtractor` | `gem.extractors.draft` | Pick and ban events |
| `TeamfightsExtractor` | `gem.extractors.teamfights` | Teamfight window detection |
| `classify_lane()` | `gem.extractors.lane` | Lane role from 10-min position heatmap |

When using `gem.parse()`, all extractors are attached and run automatically.
`classify_lane()` is a pure function called internally by `match_builder` — it can also
be called directly on any `lane_pos` dict.
