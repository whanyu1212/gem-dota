# Guides

Practical how-to guides for using gem's Python API. Each guide assumes gem is installed
and you have a Dota 2 `.dem` replay file to work with.

You can download replays from [opendota.com](https://www.opendota.com) — find any match
and click "Download Replay".

---

| Guide | What you will learn |
|---|---|
| [Quickstart](01_quickstart.md) | Install, parse a replay, print KDA and the draft |
| [Troubleshooting](troubleshooting.md) | Fix common install, parsing, and docs build issues |
| [Entity State](02_entity_state.md) | Subscribe to entity events and read field values |
| [Combat Log](03_combat_log.md) | Filter events, count damage, track kills and wards |
| [Full Match Data](04_match_data.md) | Walk through everything in `ParsedMatch` |
| [Time-Series & DataFrames](05_timeseries.md) | Per-minute gold/XP curves and pandas export |
| [Teamfight Detection](06_teamfights.md) | `match.teamfights` — windows, participants, stats |
| [Laning Analysis](08_laning.md) | Lane role classification, lane efficiency %, gold/XP advantage |
| [CLI Reference](09_cli.md) | `parse` and `batch` subcommands, all flags, Python API equivalents |
| [Annotated JSON Output](10_json_output.md) | Real TI14 replay output explained field by field |
| [Custom Extractors](07_custom_extractors.md) | Attach parser callbacks to build your own outputs |
