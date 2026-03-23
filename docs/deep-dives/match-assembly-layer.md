# Match Assembly Layer

This page explains how gem turns extractor state into final outputs:

1. `ParsedMatch` (structured object)
2. per-player combat aggregates
3. tabular DataFrame projections (`parse_to_dataframe`)

Modules covered:

1. `src/gem/combat_aggregator.py`
2. `src/gem/match_builder.py`
3. `src/gem/dataframes.py`

Prerequisites:

1. [Bits & Bytes Primer](../cookbook/bits-and-bytes-primer.md)
2. [Stream Layer (`stream.py`)](stream-layer.md)
3. [Parser Layer (`parser.py`)](parser-layer.md)
4. [SendTable Layer (`sendtable.py`)](sendtable-layer.md)
5. [State Reconstruction Layer (`string_table.py` + `entities.py`)](state-layer.md)
6. [Event Normalization Layer (`game_events.py` + `combatlog.py`)](event-layer.md)
7. [Extractors Layer](extractors-layer.md)

## Why this is the next layer

After extractors collect raw timelines, this layer:

1. merges everything into one coherent match object
2. computes derived metrics (lane stats, advantages, teamfights)
3. exposes table outputs for analytics pipelines

## `combat_aggregator.py`: per-player combat counters

`_CombatAggregator` consumes normalized `CombatLogEntry` events during parse and accumulates per-player buckets.

### Core structures

| Type | Role |
|---|---|
| `_ParsedPlayerAgg` | Mutable per-player accumulator (damage/heal/uses/reasons/logs/stuns) |
| `_CombatAggregator.players` | `player_id -> _ParsedPlayerAgg` map |

### Key methods

| Method | What it does |
|---|---|
| `_hero_to_pid` | Resolve hero NPC name to player slot (0-9) |
| `_summon_to_pid` | Resolve summon unit to owner hero slot via `m_hOwnerEntity` |
| `on_entry` | Routes each combat-log type to the right per-player bucket |
| `_dedup_purchase_log` | Removes duplicate starting-window purchase entries |

### `on_entry` routing summary

| `log_type` | Aggregation effect |
|---|---|
| `DAMAGE` | update attacker damage + target damage_taken (+ type splits) |
| `HEAL` | update attacker healing |
| `ABILITY` / `ITEM` | increment usage counts |
| `GOLD` / `XP` | add reason-based totals on target |
| `DEATH` | append kills log for attacker |
| `PURCHASE` | append purchase log (attacker/target fallback) |
| `PICKUP_RUNE` | append rune event for player slot in `entry.value` |
| `BUYBACK` | populated later in `match_builder` post-pass |

## `match_builder.py`: assemble final `ParsedMatch`

`build_parsed_match(...)` is the main output assembly function.

### Key constants

| Constant | Value | Meaning |
|---|---|---|
| `_LANE_GRID` | `64` | Lane heatmap cell size (world units) |
| `_LANE_WINDOW` | `600 * 30 = 18000` | First 10 game-minutes for lane analysis |
| `_STEAM_ID_BASE` | `76561197960265728` | SteamID64 -> account_id offset |

### Build flow (high level)

1. Resolve `radiant_win` fallback from ancient death if parser metadata is missing.
2. Create base `ParsedMatch` with extractor outputs (`towers`, `roshans`, `wards`, `draft`, etc.).
3. Post-pass BUYBACK entries into combat aggregates.
4. For each player slot `0..9`:
   - wire regular + minute time series from `PlayerExtractor`
   - attach combat aggregates (damage, uses, logs, stuns)
   - attach scoreboard K/D/A
   - build lane heatmap and lane-role/lane-10m metrics
5. Populate player names/steam ids from `CDOTA_PlayerResource`.
6. Populate team metadata from `CDOTATeam` entities.
7. Attach observer/sentry ward logs per player.
8. Build `radiant_gold_adv` and `radiant_xp_adv` arrays from minute series.
9. Run `detect_teamfights(...)` with hero-slot/team/snapshot context.
10. Build `_ability_snapshots` for `ability_level_at_tick()` lookup.

### Important correctness rules in this layer

1. Advantage curves must use cumulative totals (`total_earned_*`), not spendable gold or level-local XP.
2. Lane role is derived from first 10 minutes only.
3. Purchase logs are deduplicated only in the starting snapshot window.

## `dataframes.py`: tabular projection layer

`build_dataframes(match)` converts `ParsedMatch` into analytics-friendly DataFrames.

### Exported tables

| Key | Content |
|---|---|
| `players` | per-sample player rows (tick-level) |
| `players_minute` | minute-boundary player rows |
| `positions` | `(tick, x, y)` rows per player |
| `combat_log` | normalized combat entries |
| `wards` | ward events |
| `objectives` | towers/barracks/roshan/tormentor/shrine/aegis |
| `chat` | chat messages |
| `match` | match-level metadata |
| `radiant_advantage` | minute-by-minute radiant gold/xp advantage |
| `draft` | draft events |
| `teamfights` | teamfight windows |
| `smoke_events` | smoke activations |
| `courier_snapshots` | courier state samples |
| `player_kills_log` | per-player kill entries |
| `player_purchase_log` | per-player purchases |
| `player_runes_log` | per-player runes |
| `player_buyback_log` | per-player buybacks |

`gem.parse_to_dataframe(path)` is a convenience wrapper:

1. `parse(path)` -> `ParsedMatch`
2. `build_dataframes(match)` -> `dict[str, DataFrame]`

## Real snapshot from fixture (truncated)

From `parse_to_dataframe("tests/fixtures/8520014563.dem")`:

```text
table_count 17
chat (2, 4)
combat_log (108594, 16)
courier_snapshots (6701, 6)
draft (0, 0)
match (1, 6)
objectives (27, 9)
player_buyback_log (5, 17)
player_kills_log (3393, 17)
player_purchase_log (661, 17)
player_runes_log (67, 17)
players (34941, 36)
players_minute (550, 12)
positions (34941, 6)
radiant_advantage (55, 3)
smoke_events (15, 6)
teamfights (42, 10)
wards (119, 10)
...
```

Interpretation:

1. Empty `draft` table is valid for some replay paths.
2. `players` and `positions` are large because they sample over many ticks.
3. `players_minute` and `radiant_advantage` are compact minute-bucket tables.

## Common failure modes in this layer

1. Using non-cumulative fields for advantage calculations causes drift.
2. Missing player-name/team resolution when `CDOTA_PlayerResource` path changes.
3. Over-deduplicating purchases outside the starting window removes valid repeated buys.
4. Assuming all tables are non-empty (`draft`, `chat`, etc.).

## Next pages

1. [Time-Series and DataFrames](../guides/05_timeseries.md)
2. [Full Match Data](../guides/04_match_data.md)
3. [Annotated JSON Output](../guides/10_json_output.md)
