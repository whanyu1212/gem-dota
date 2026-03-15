# DataFrames

Converts a `ParsedMatch` into a dictionary of pandas DataFrames, one per table.
This is the primary interface for ML/data-science workflows.

!!! note "Parquet dependency"
    `to_parquet()` requires `pyarrow` (recommended) or `fastparquet`:
    ```bash
    pip install pyarrow
    ```

## Available tables

| Key | Contents |
|---|---|
| `"players"` | Per-player snapshots at each sample tick |
| `"players_minute"` | Per-player stats aggregated by game minute |
| `"positions"` | Hero position heatmap grid (64-unit cells) |
| `"combat_log"` | Every damage, kill, heal, and modifier event |
| `"wards"` | Ward placements with exact map coordinates |
| `"objectives"` | Tower kills, barracks, Roshan kills |
| `"teamfights"` | Detected fight windows with participant stats |
| `"smoke_events"` | Smoke activations with grouped heroes and centroid |
| `"aegis_events"` | Aegis pickups, steals, and denies |
| `"draft"` | Pick and ban events in order |
| `"match"` | Single-row match metadata (id, duration, winner, …) |
| `"radiant_advantage"` | Per-minute gold and XP advantage curves |
| `"chat"` | All-chat and team-chat messages |
| `"courier_snapshots"` | Courier state sampled each tick |

---

::: gem.dataframes
