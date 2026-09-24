# DataFrames

Converts a `ParsedMatch` into a dictionary of pandas DataFrames, one per table.
This is the primary interface for ML/data-science workflows.

::: info Parquet dependency
`to_parquet()` requires `pyarrow` (recommended) or `fastparquet`:
```bash
pip install pyarrow
```
:::

## Available tables

Every table starts with a `match_id` column (`0` when the replay has no match ID).
Core tables hold only primitive cells, so they write to Parquet with a stable schema
and concatenate across replays.

### Core tables (always returned)

| Key | Contents |
|---|---|
| `"match"` | Single-row match metadata (id, mode, winner, ticks, final status bitmasks) |
| `"player_summary"` | One row per player: identity, K/D/A, final net worth/LH/DN, GPM/XPM, damage/healing totals, lane stats, damage-type split, largest hero hit, consumed Aghanim's/Moon Shard flags |
| `"player_timeseries"` | Per-player sampled `gold`, `total_earned_gold`, `total_earned_xp`, `net_worth`, `lh`, `dn`, `xp` by tick |
| `"players_minute"` | Per-player series resampled to game minutes |
| `"player_breakdowns"` | Long-form per-player dict stats as `(player_id, stat, key, subkey, value)` |
| `"positions"` | Per-player sampled world `(x, y)` positions |
| `"radiant_advantage"` | Per-minute gold and XP advantage curves |
| `"combat_log"` | Every damage, kill, heal, and modifier event |
| `"wards"` | Ward placements with exact map coordinates |
| `"objectives"` | Tower, barracks, Roshan, Tormentor, shrine, Aegis, courier, and banner rows |
| `"chat"` | All-chat and team-chat messages |
| `"draft"` | Pick and ban events in order |
| `"teamfights"` | Detected fight windows, one row per fight with a `fight_index` |
| `"teamfight_players"` | Per-fight, per-player deaths, buybacks, damage, healing, gold/XP delta |
| `"smoke_events"` | Smoke activations, `";"`-joined smoked heroes, and centroids |
| `"smoke_members"` | Flat per-hero smoke application/removal ticks, durations, and sampled positions |
| `"courier_snapshots"` | Courier state samples |
| `"neutral_item_finds"` | Neutral item finds with item and enhancement IDs/keys |
| `"hero_visibility_events"` | Change-only Radiant/Dire visibility state for canonical player heroes |
| `"entity_visibility"` | Change-only packet-boundary visibility and lifecycle for networked Dota NPC entities |
| `"vision_modifiers"` | Flat vision-relevant modifier application lifecycles and evidence |
| `"vision_modifier_pairing_issues"` | Flat ambiguous/orphan modifier removal evidence |
| `"player_kills_log"`, `"player_purchase_log"`, `"player_runes_log"`, `"player_buyback_log"` | Per-player combat-log projections |

### Optional groups

Pass `include=["analysis"]` and/or `include=["opendota"]` to add these tables.

| Group | Key | Contents |
|---|---|---|
| `analysis` | `"teamfight_positioning"` | Flat per-fight, per-snapshot, per-hero positioning evidence with freshness, geometry, and visibility |
| `analysis` | `"roshan_conversions"` | One flat row per Roshan with attribution/lifecycle provenance, raw differential evidence, availability, tags/ruleset, and prefixed legacy fields |
| `analysis` | `"roshan_conversion_fights"` | One row per Roshan-associated fight with engagement provenance, relation, winner, and participant IDs by side |
| `analysis` | `"smoke_fight_insights"` | One row per bounded smoke/fight candidate, including association, exact-event, visibility, and formation summaries |
| `analysis` | `"smoke_fight_members"` | Per-candidate smoked-member participation, visibility, sampled position, and evidence-gap details |
| `analysis` | `"smoke_fight_followups"` | Uniquely allocated objective and observer-placement evidence inside bounded post-fight windows |
| `analysis` | `"farming_routes"` | One row per player with route availability, camp-catalog metadata, and segment/point counts |
| `analysis` | `"farming_route_segments"` | Camp-local route windows with boundary provenance, sampled coverage, neutral/resource support, evidence strength, and gaps |
| `analysis` | `"farming_route_points"` | Sampled path points with deterministic camp membership and optional segment membership |
| `analysis` | `"farming_context_tags"` | One row per farming segment/context tag and its reasons |
| `opendota` | `"opendota_objectives"` | OpenDota-shaped unified objective timeline |
| `opendota` | `"opendota_teamfights"` | OpenDota-compatible 3+ death temporal teamfight windows |

---

## Generated API

## Module `gem.results.dataframes`

DataFrame conversion for :class:`ParsedMatch` output.

Source: [src/gem/results/dataframes.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/dataframes.py#L1)

### Top-level functions

### `build_dataframes`

```python
def build_dataframes(match: ParsedMatch, *, include: Iterable[str] = ()) -> dict[str, pd.DataFrame]
```

Convert a :class:`ParsedMatch` into a dict of flat pandas DataFrames.

Source: [src/gem/results/dataframes.py:167](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/results/dataframes.py#L167)
