# Quickstart

Get from install to a KDA table in under a minute.

## Install

```bash
pip install gem-dota
```

Or with `uv`:

```bash
uv add gem-dota
```

::: info Requirements
Python **3.10 or later** is required. gem has no compiled extensions — it runs
in pure Python out of the box.
:::

## Get a replay

Download a `.dem` file from [opendota.com](https://www.opendota.com) — find any match
and click "Download Replay".

::: tip
You can also find replays in your Dota 2 client under **Watch → Recent Games**,
then click the download icon next to any match.
:::

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
        f"  NW {player.net_worth_t_min[-1] if player.net_worth_t_min else 0:,}"
        f"  LH/DN {player.lh_t_min[-1] if player.lh_t_min else 0}/{player.dn_t_min[-1] if player.dn_t_min else 0}"
    )
```

Sample output:

```
Match duration: 54.4 minutes

npc_dota_hero_muerta            KDA 8/8/15  NW 37,348  LH/DN 605/32
npc_dota_hero_queenofpain       KDA 17/5/22  NW 34,377  LH/DN 395/15
npc_dota_hero_pugna             KDA 3/7/30  NW 16,795  LH/DN 85/6
...
```

## Draft picks and bans

```python
import gem

match = gem.parse("my_replay.dem")

for event in match.draft:
    team = "Radiant" if event.team == 2 else "Dire"
    action = "picks" if event.is_pick else "bans"
    print(f"  {team} {action} {event.hero_name}")
```

Sample output (truncated):

```text
  Dire bans npc_dota_hero_chen
  Dire bans npc_dota_hero_naga_siren
  Radiant bans npc_dota_hero_mars
  Dire bans npc_dota_hero_monkey_king
  Dire bans npc_dota_hero_earthshaker
  Radiant bans npc_dota_hero_centaur
  Radiant bans npc_dota_hero_enchantress
  Dire picks npc_dota_hero_shadow_demon
  Radiant picks npc_dota_hero_pangolier
  ...
```

## Ward count per player

```python
for player in match.players:
    wards = [w for w in match.wards if w.placer == player.hero_name]
    print(f"  {player.hero_name}: {len(wards)} wards placed")
```

Sample output (truncated):

```text
  npc_dota_hero_muerta: 0 wards placed
  npc_dota_hero_queenofpain: 4 wards placed
  npc_dota_hero_pugna: 26 wards placed
  npc_dota_hero_lion: 36 wards placed
  ...
```

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

Sample output (truncated):

```text
['players', 'players_minute', 'positions', 'combat_log', 'wards', 'objectives', 'chat', 'match', ...]
['player_id', 'player_name', 'hero_name', 'team', 'tick', 'gold', 'net_worth', 'lh', 'dn', 'xp', ...]
 player_id            hero_name  team  tick  gold  net_worth
         0 npc_dota_hero_muerta     2  3618     0          0
         0 npc_dota_hero_muerta     2  3648     0        600
...
```

### JSON

```python
# Parse directly to a JSON string
json_str = gem.parse_to_json("my_replay.dem", indent=2)

# Or convert an already-parsed match
match = gem.parse("my_replay.dem")
json_str = gem.to_json(match)
data     = gem.to_dict(match)   # plain Python dict

print(json_str[:300])
```

Sample output (truncated):

```json
{
  "match_id": 8520014563,
  "game_mode": 22,
  "leagueid": 0,
  "radiant_win": true,
  "radiant_team_name": "#DOTA_GoodGuys",
  "dire_team_name": "#DOTA_BadGuys",
  "players": [
    {
      "player_id": 0,
      "hero_name": "npc_dota_hero_muerta",
      "player_name": "TianJiao"
    }
  ]
}
```

### Parquet

::: info Parquet dependency
Parquet output requires an optional engine. Install `pyarrow` (recommended) or
`fastparquet`:
```bash
pip install pyarrow
```
:::

```python
# One .parquet file per DataFrame table
paths = gem.parse_to_parquet("my_replay.dem", output_dir="./out")
print(paths[:3])

# Or export from an already-parsed match
paths = gem.to_parquet(match, output_dir="./out")
print(paths[:3])
```

Sample output (truncated):

```text
ImportError: Parquet export requires an optional engine.
Install 'pyarrow' or 'fastparquet'.
```

### Batch processing

Parse a whole folder of replays in parallel with `gem.parse_many_to_dataframe()`:

```python
import gem

# Concatenated DataFrames from every replay in the folder
dfs = gem.parse_many_to_dataframe("replays/", workers=4)
print(dfs["players"].head())   # has a match_path column for provenance
```

Sample output (truncated):

```text
 player_id            hero_name  team  tick                                                                  match_path
         0 npc_dota_hero_muerta     2  3618 /tmp/.../8520014563.dem
         0 npc_dota_hero_muerta     2  3648 /tmp/.../8520014563.dem
...
```

Or write each replay to its own Parquet subdirectory:

```python
gem.parse_many_to_parquet("replays/", output_dir="./out", workers=4)
```

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

Sample output (truncated):

```text
Parsing tests/fixtures/8520014563.dem ...
94 hero kills | 16 towers | 6 barracks | 2 Roshan kill(s) | 119 wards
...
ImportError: Parquet export requires 'pyarrow' or 'fastparquet'.
```

See the [CLI Reference](09_cli.md) for all flags and options.

## What is `gem.parse()`?

`gem.parse()` runs the full parser pipeline and returns a `ParsedMatch` object.
Under the hood it:

1. Opens and memory-maps the `.dem` file.
2. Parses `DEM_SendTables` to build the entity class schema.
3. Processes every `DEM_Packet` tick: entity state, combat log, game events.
4. Runs all extractors: player stats, wards, objectives, draft, teamfights.
5. Assembles the results into `ParsedMatch` and its `ParsedPlayer` list.

A typical 45-minute replay parses in 2–4 seconds in pure Python.

## Next steps

- [Full Match Data](04_match_data.md) — all fields on `ParsedMatch` and `ParsedPlayer`
- [CLI Reference](09_cli.md) — `parse` and `batch` subcommands, all flags
- [Entity State](02_entity_state.md) — subscribe to per-tick entity events
- [Combat Log](03_combat_log.md) — raw damage, heal, kill, ability events
- [Time-Series & DataFrames](05_timeseries.md) — per-minute gold/XP advantage curves, JSON and Parquet export
- [How Proto Parsing Works](../cookbook/proto-parsing-pipeline.md) — conceptual parser pipeline
