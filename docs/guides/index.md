# Guides

Practical guides for using gem's public Python API, CLI, and lower-level parser hooks.
Each guide assumes gem is installed and you have a decompressed Dota 2 `.dem` replay.

You can download replays from [OpenDota](https://www.opendota.com) or from the Dota 2
client under **Watch -> Recent Games**.

## Start here

| Guide | Use it when you want to |
|---|---|
| [Quickstart](01_quickstart.md) | Install gem, parse one replay, and export data |
| [Full Match Data](04_match_data.md) | Understand the `ParsedMatch` and `ParsedPlayer` fields |
| [Time-Series & DataFrames](05_timeseries.md) | Work with pandas tables, positions, and advantage curves |

## Analyze replay events

| Guide | Use it when you want to |
|---|---|
| [Combat Log](03_combat_log.md) | Filter damage, healing, kills, item uses, and modifiers |
| [Teamfight Detection](06_teamfights.md) | Use Gem and OpenDota-compatible fight windows |
| [Laning Analysis](08_laning.md) | Read lane roles, lane efficiency, and 10-minute advantages |
| [Entity State](02_entity_state.md) | Subscribe to raw entity lifecycle and field updates |

## Export and extend

| Guide | Use it when you want to |
|---|---|
| [CLI Reference](09_cli.md) | Run `parse`, `batch`, and report asset-cache commands |
| [JSON Output Shape](10_json_output.md) | Understand the nested JSON structure returned by `to_json()` |
| [Custom Extractors](07_custom_extractors.md) | Register parser callbacks and collect custom outputs |

## Internals

Parser internals live in dedicated pages:

1. [Bits & Bytes Primer](../cookbook/bits-and-bytes-primer.md)
2. [Parser Internals](../deep-dives/index.md)
