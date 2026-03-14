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

You need Python 3.10 or later.

---

## Get a replay

Download a `.dem` file from [opendota.com](https://www.opendota.com) — find any match
and click "Download Replay".

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

## DataFrame export

`gem.parse_to_dataframe()` returns a dict of pandas DataFrames:

```python
import gem

frames = gem.parse_to_dataframe("my_replay.dem")

# Available DataFrames
print(list(frames.keys()))
# ['players', 'wards', 'objectives', 'teamfights', 'combat_log']

# Per-player snapshot time series
df = frames["players"]
print(df.columns.tolist())
# ['tick', 'hero', 'gold', 'xp', 'hp', 'mana', 'x', 'y', 'lh', 'dn', ...]
print(df.head())
```

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
- [Entity State](02_entity_state.md) — subscribe to per-tick entity events
- [Combat Log](03_combat_log.md) — raw damage, heal, kill, ability events
- [Time-Series & DataFrames](05_timeseries.md) — per-minute gold/XP advantage curves
- [Understanding the Format](../understanding/index.md) — how the binary format works
