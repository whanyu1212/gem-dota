# Gem

**Gem** reads Dota 2 `.dem` replay files and turns them into structured Python objects.

Named after the **Gem of True Sight** — it reveals what is hidden inside replay files.

---

## Install

```bash
pip install gem-dota
```

Or with `uv`:

```bash
uv add gem-dota
```

---

## Quickstart

```python
import gem

match = gem.parse("my_replay.dem")

# KDA and net worth for each player
for player in match.players:
    print(
        f"{player.hero_name:<30}"
        f"  KDA {player.kills}/{player.deaths}/{player.assists}"
        f"  NW {player.net_worth:,}"
    )

# Draft
for pick in match.draft:
    if pick.is_pick:
        print(f"  {'Radiant' if pick.team == 0 else 'Dire'} picks {pick.hero_name}")

# Ward count per player
for player in match.players:
    print(f"  {player.hero_name}: {len(player.wards)} wards")
```

---

## Export formats

```python
import gem

# DataFrames (pandas)
frames = gem.parse_to_dataframe("my_replay.dem")
heroes_df = frames["players"]   # columns: tick, hero, gold, xp, lh, dn, ...

# JSON — to string or file
json_str = gem.parse_to_json("my_replay.dem", indent=2)
match = gem.parse("my_replay.dem")
data = gem.to_dict(match)        # plain Python dict
json_str = gem.to_json(match)

# Parquet — one file per DataFrame table
paths = gem.parse_to_parquet("my_replay.dem", output_dir="./out")
paths = gem.to_parquet(match, output_dir="./out")
```

---

## Where to start

=== "I want to use it"

    Jump to the [Guides](guides/index.md) — start with the
    [Quickstart](guides/01_quickstart.md) for install-to-KDA in 10 lines, or go
    straight to [Full Match Data](guides/04_match_data.md) for a walkthrough of
    everything in `ParsedMatch`.

=== "I want to understand the format"

    Read [Understanding the Format](understanding/index.md). It explains the Dota 2
    replay binary format from scratch — magic bytes, outer message framing, protobuf
    payloads, the entity delta system, field path Huffman coding, string tables, and
    the combat log. Each page builds on the previous.

=== "I need the API"

    Go to the [API Reference](reference/index.md). Every public class and function
    has a Google-style docstring.
