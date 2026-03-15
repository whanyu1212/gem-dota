# Quickstart

Get from install to a KDA table in under a minute.

---

## Install

```bash
pip install gem-dota
```

Or with `uv`:

```bash
uv add gem-dota
```

!!! info "Requirements"
    Python **3.10 or later** is required. gem has no compiled extensions — it runs
    in pure Python out of the box.

---

## Get a replay

Download a `.dem` file from [opendota.com](https://www.opendota.com) — find any match
and click "Download Replay".

!!! tip
    You can also find replays in your Dota 2 client under **Watch → Recent Games**,
    then click the download icon next to any match.

---

## KDA for every player

```python
import gem

match = gem.parse("my_replay.dem")

print(f"Match duration: {match.duration_minutes:.1f} minutes")
print()

for player in match.players:
    print(
        f"{player.hero_name:<30}"
        f"  KDA {player.kills}/{player.deaths}/{player.assists}"
        f"  NW {player.net_worth:,}"
        f"  LH/DN {player.last_hits}/{player.denies}"
    )
```

Sample output:

```
Match duration: 42.3 minutes

CDOTA_Unit_Hero_Axe             KDA 8/3/12  NW 28,450  LH/DN 182/14
CDOTA_Unit_Hero_ShadowDemon     KDA 4/5/18  NW 18,220  LH/DN 64/3
...
```

---

## Draft picks and bans

```python
import gem

match = gem.parse("my_replay.dem")

for event in match.draft:
    team = "Radiant" if event.team == 2 else "Dire"
    action = "picks" if event.is_pick else "bans"
    print(f"  {team} {action} {event.hero_name}")
```

---

## Ward count per player

```python
for player in match.players:
    wards = [w for w in match.wards if w.placed_by == player.hero_name]
    print(f"  {player.hero_name}: {len(wards)} wards placed")
```

---

## Export formats

### DataFrames

`gem.parse_to_dataframe()` returns a dict of pandas DataFrames:

```python
import gem

frames = gem.parse_to_dataframe("my_replay.dem")

# Available DataFrames
print(list(frames.keys()))
# ['players', 'players_minute', 'positions', 'combat_log', 'wards',
#  'objectives', 'chat', 'match', 'radiant_advantage', 'draft',
#  'teamfights', 'smoke_events', 'courier_snapshots', ...]

df = frames["players"]
print(df.columns.tolist())
print(df.head())
```

### JSON

```python
# Parse directly to a JSON string
json_str = gem.parse_to_json("my_replay.dem", indent=2)

# Or convert an already-parsed match
match = gem.parse("my_replay.dem")
json_str = gem.to_json(match)
data     = gem.to_dict(match)   # plain Python dict
```

### Parquet

!!! note "Parquet dependency"
    Parquet output requires an optional engine. Install `pyarrow` (recommended) or
    `fastparquet`:
    ```bash
    pip install pyarrow
    ```

```python
# One .parquet file per DataFrame table
paths = gem.parse_to_parquet("my_replay.dem", output_dir="./out")

# Or export from an already-parsed match
paths = gem.to_parquet(match, output_dir="./out")
```

### Batch processing

Parse a whole folder of replays in parallel with `gem.parse_many_to_dataframe()`:

```python
import gem

# Concatenated DataFrames from every replay in the folder
dfs = gem.parse_many_to_dataframe("replays/", workers=4)
print(dfs["players"].head())   # has a match_path column for provenance
```

Or write each replay to its own Parquet subdirectory:

```python
gem.parse_many_to_parquet("replays/", output_dir="./out", workers=4)
```

---

## Command-line interface

gem can also be used from the terminal without writing Python code:

```bash
# Match summary
python -m gem my_replay.dem

# Export to JSON
python -m gem my_replay.dem --format json > match.json

# Export to Parquet
python -m gem parse my_replay.dem --format parquet --output ./out

# Batch — parse a folder in parallel
python -m gem batch replays/ --format parquet --output ./out --workers 4
```

See the [CLI Reference](09_cli.md) for all flags and options.

---

## What is `gem.parse()`?

`gem.parse()` runs the full parser pipeline and returns a `ParsedMatch` object.
Under the hood it:

1. Opens and memory-maps the `.dem` file.
2. Parses `DEM_SendTables` to build the entity class schema.
3. Processes every `DEM_Packet` tick: entity state, combat log, game events.
4. Runs all extractors: player stats, wards, objectives, draft, teamfights.
5. Assembles the results into `ParsedMatch` and its `ParsedPlayer` list.

A typical 45-minute replay parses in 2–4 seconds in pure Python.

---

## Next steps

- [Full Match Data](04_match_data.md) — all fields on `ParsedMatch` and `ParsedPlayer`
- [CLI Reference](09_cli.md) — `parse` and `batch` subcommands, all flags
- [Entity State](02_entity_state.md) — subscribe to per-tick entity events
- [Combat Log](03_combat_log.md) — raw damage, heal, kill, ability events
- [Time-Series & DataFrames](05_timeseries.md) — per-minute gold/XP advantage curves, JSON and Parquet export
- [Understanding the Format](../understanding/index.md) — how the binary format works
