# API Reference

Auto-generated from source docstrings. All public classes and functions follow
[Google-style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).

## Core parsing modules

| Module | Contents |
|---|---|
| [BitReader](reader.md) | Low-level bit/byte/varint reader |
| [DemoStream](stream.md) | Outer message stream iterator |
| [Send Tables](sendtable.md) | Serializer tree — `parse_send_tables`, `Serializer`, `Field` |
| [Field Decoders](field_decoder.md) | Type → decoder dispatch, `QuantizedFloatDecoder` |
| [Field Paths](field_path.md) | Huffman field path decoder, `FieldPath` |
| [String Tables](string_table.md) | Table creation, updates, key-history decoder |
| [Entities](entities.md) | Entity lifecycle, `EntityOp`, typed field accessors |
| [Game Events](game_events.md) | Game event schema registration and typed dispatch |
| [Combat Log](combatlog.md) | Combat log entry decoding and dispatch |
| [ReplayParser](parser.md) | Top-level parse driver — wires all subsystems |

## Output and extraction

| Module | Contents |
|---|---|
| [Models](models.md) | `ParsedMatch`, `ParsedPlayer`, output dataclasses |
| [Constants](constants.md) | `hero_display()`, `item_display()`, name lookups |
| [Match Builder](match_builder.md) | Assembles extractor output into `ParsedMatch` |
| [Combat Aggregator](combat_aggregator.md) | Per-player combat stat aggregation |
| [DataFrames](dataframes.md) | `parse_to_dataframe()` — pandas export |

## Extractors

| Module | Contents |
|---|---|
| [Overview](extractors/index.md) | How extractors attach to the parser |
| [Players](extractors/players.md) | Hero/player snapshots, time series, runes |
| [Objectives](extractors/objectives.md) | Towers, barracks, Roshan |
| [Wards](extractors/wards.md) | Ward placements with coordinates |
| [Courier](extractors/courier.md) | Courier state per tick |
| [Draft](extractors/draft.md) | Pick and ban events |
| [Teamfights](extractors/teamfights.md) | Teamfight window detection |
