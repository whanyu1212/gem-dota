# Guides

Practical how-to guides for using gem's Python API. Each guide assumes gem is installed
and you have a Dota 2 `.dem` replay file to work with.

You can download replays from [opendota.com](https://www.opendota.com) — find any match
and click "Download Replay".

---

## If you want parser internals first

Parser internals now live in a dedicated section:

1. [Bits & Bytes Primer](../cookbook/bits-and-bytes-primer.md)
2. [Deep Dives](../deep-dives/index.md)

---

| Guide | What you will learn |
|---|---|
| [Entity State](02_entity_state.md) | Subscribe to entity events and read field values |
| [Combat Log](03_combat_log.md) | Filter events, count damage, track kills and wards |
| [Full Match Data](04_match_data.md) | Walk through everything in `ParsedMatch` |
| [Time-Series & DataFrames](05_timeseries.md) | Per-minute gold/XP curves and pandas export |
| [Teamfight Detection](06_teamfights.md) | `match.teamfights` — windows, participants, stats |
| [Laning Analysis](08_laning.md) | Lane role classification, lane efficiency %, gold/XP advantage |
| [CLI Reference](09_cli.md) | `parse` and `batch` subcommands, all flags, Python API equivalents |
| [Annotated JSON Output](10_json_output.md) | Real TI14 replay output explained field by field |
| [Custom Extractors](07_custom_extractors.md) | Attach parser callbacks to build your own outputs |
