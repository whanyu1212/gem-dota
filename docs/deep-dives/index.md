# Parser Internals

This page is a maintainer-oriented map of how gem turns Source 2 replay bytes into
`ParsedMatch`. It avoids private-method inventories; use the API reference and source links
when you need exact function signatures.

If you are new to the binary format, start with
[Bits & Bytes Primer](../cookbook/bits-and-bytes-primer.md) and
[How Proto Parsing Works](../cookbook/proto-parsing-pipeline.md).

## Pipeline

```text
.dem bytes
  -> binary/stream.py
  -> parser.py
  -> schema/sendtable/
  -> state/string_table.py + state/entities.py
  -> state/game_events.py + combat/log.py
  -> extractors/
  -> combat/aggregator.py + results/assembly.py
  -> ParsedMatch / DataFrames / JSON / Parquet
```

## Layer Responsibilities

| Layer | What it owns | Source |
|---|---|---|
| Stream | Validates `PBDEMS2`, reads outer records, strips compression flags, decompresses payloads | [DemoStream](../reference/stream.md) |
| Parser | Decodes `CDemo*` envelopes, unpacks inner messages, orders state updates, routes callbacks | [ReplayParser](../reference/parser.md) |
| Send tables | Builds serializer schemas and field models used for entity delta decoding | [Send Tables](../reference/sendtable.md) |
| State | Maintains string tables, instance baselines, entity lifecycle, handles, and field access | [Entities](../reference/entities.md) |
| Events | Normalizes Source 1 events, Source 2 combat entries, chat, match metadata, and neutral item messages | [Combat Log](../reference/combatlog.md) |
| Extractors | Converts entity/event streams into players, objectives, wards, couriers, draft, intervals, and derived fight/lane records | [Extractors](../reference/extractors/) |
| Assembly | Merges extractor state into `ParsedMatch`, OpenDota-shaped outputs, and DataFrame projections | [Models](../reference/models.md) |

## Parser Flow

`ReplayParser` is the low-level driver. Most users should call `gem.parse()`, but the
parser is still the extension point for custom extractors.

The parser reads outer messages in stream order, then decodes packet payloads into inner
messages. It applies string-table and server-info messages before packet-entity deltas so
entity updates can resolve baselines, names, and class metadata correctly. Combat log,
chat, match metadata, and neutral-item messages are dispatched through typed callbacks.

Important parser state includes:

- `match_id`, `game_mode`, `leagueid`, `radiant_win`, and `match_metadata`
- `game_start_tick`, `game_time_s`, `combat_log_time_s`, and `duration_s`
- `parse_error` and `truncated_at_tick` for partial parses
- callback hooks such as `on_entity`, `on_tick_start`, `on_combat_log_entry`,
  `on_chat_message`, `on_chat_event`, `on_neutral_item_found`, `on_game_start`,
  and `on_game_end`

For custom callback usage, see [Writing Custom Extractors](../guides/07_custom_extractors.md).

## Extractor Flow

The high-level `gem.parse()` helper wires the standard extractors, collects normalized
combat entries, then calls `build_parsed_match(...)`.

Built-in extraction covers:

- player snapshots, inventories, abilities, positions, and scoreboard values
- OpenDota-aligned interval data for gold and XP advantage curves
- towers, barracks, Roshan, Tormentor, Shrine of Wisdom, Aegis, and courier deaths
- ward placement, expiry, and kill attribution
- courier state snapshots
- draft picks and bans
- smoke events, vision modifier windows, neutral item finds, and chat
- native teamfight windows plus OpenDota-compatible teamfight windows

The public output shape is documented in [Full Match Data](../guides/04_match_data.md),
[Time-Series and DataFrames](../guides/05_timeseries.md), and the
[Models reference](../reference/models.md).

## Stability Notes

Replay internals are intentionally not treated as a stable public API. Private constants,
message IDs, fixture row counts, and helper methods can change when Valve changes replay
schemas or when gem improves OpenDota parity.

Stable documentation should live in:

- [Architecture](../architecture.md) for module boundaries
- [Guides](../guides/) for consumer workflows
- [API Reference](../reference/) for generated source-linked signatures
- [Replay Edge Cases](replay-edge-cases.md) for ambiguity, truncation, and inference limits
