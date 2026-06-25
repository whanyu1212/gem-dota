# Quickstart

Get from installation to useful replay data with the high-level Python API.

## Install

```bash
pip install gem-dota
```

Or with `uv`:

```bash
uv add gem-dota
```

::: info Requirements
Python 3.10 or later is required. The import name is `gem`.
:::

## Get a replay

`gem.parse()` expects a decompressed Source 2 `.dem` replay file.

You can download replays from [OpenDota](https://www.opendota.com) by opening a match
and clicking "Download Replay". The Dota 2 client also stores downloaded replays under
**Watch -> Recent Games**.

## Parse a match

```python
import gem
from gem.constants import hero_display

match = gem.parse("my_replay.dem")

winner = "Radiant" if match.radiant_win else "Dire" if match.radiant_win is False else "?"
print(f"Match {match.match_id} | {match.duration_minutes:.1f} min | winner: {winner}")

for player in match.players:
    print(
        f"{hero_display(player.hero_name):<18}"
        f" KDA {player.kills}/{player.deaths}/{player.assists}"
        f" NW {player.net_worth:>6,}"
        f" LH/DN {player.last_hits}/{player.denies}"
    )
```

`gem.parse()` returns a `ParsedMatch`. Most consumers can stay at this level and work
with fields such as `match.players`, `match.combat_log`, `match.wards`,
`match.teamfights`, `match.opendota_teamfights`, `match.draft`, and
`match.radiant_gold_adv`.

## Find one player

```python
axe = gem.find_player(match, "Axe")

if axe:
    print(axe.hero_name)
    print(axe.kills, axe.deaths, axe.assists)
    print(axe.damage_by_type)
```

`find_player()` accepts display names (`"Anti-Mage"`), loose names (`"anti mage"`), and
full NPC names (`"npc_dota_hero_antimage"`).

## Export data

### JSON

```python
json_str = gem.parse_to_json("my_replay.dem", indent=2)

match = gem.parse("my_replay.dem")
data = gem.to_dict(match)
```

Use JSON when you want the full nested `ParsedMatch` shape.

### DataFrames

```python
frames = gem.parse_to_dataframe("my_replay.dem")

print(sorted(frames))
print(frames["players"].head())
print(frames["combat_log"].head())
```

Use DataFrames for pandas, notebooks, and ML pipelines. Common tables include
`players`, `players_minute`, `positions`, `combat_log`, `wards`, `objectives`,
`opendota_objectives`, `teamfights`, `opendota_teamfights`, `neutral_item_finds`, and
per-player event logs.

### Parquet

::: info Parquet dependency
Parquet output requires an optional engine: install `pyarrow` or `fastparquet`.
:::

```python
paths = gem.parse_to_parquet("my_replay.dem", output_dir="./out")
print(paths[:3])
```

## Command line

```bash
# Match summary
python -m gem my_replay.dem

# JSON to stdout
python -m gem my_replay.dem --format json > match.json

# Parquet files
python -m gem parse my_replay.dem --format parquet --output ./out

# Batch parse a folder
python -m gem batch replays/ --format parquet --output ./out --workers 4
```

See the [CLI Reference](09_cli.md) for all options, including the report asset-cache
commands used by HTML report generation.

## Next steps

| Task | Read |
|---|---|
| Inspect every `ParsedMatch` field | [Full Match Data](04_match_data.md) |
| Work with pandas tables and time series | [Time-Series & DataFrames](05_timeseries.md) |
| Analyze combat log events | [Combat Log](03_combat_log.md) |
| Work with teamfight windows | [Teamfight Detection](06_teamfights.md) |
| Build custom parser callbacks | [Custom Extractors](07_custom_extractors.md) |
| Understand parser internals | [Parser Internals](../deep-dives/index.md) |
