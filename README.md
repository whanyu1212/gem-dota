<p align="center">
  <img src="https://raw.githubusercontent.com/whanyu1212/gem-dota/main/site/public/gem-readme-banner-wordmark-subtitle-spaced.png" alt="gem: a Dota 2 replay parser for Python" width="860">
</p>

<p align="center">
  <strong>Turn Dota 2 replays into analysis-ready Python data.</strong><br>
  Parse Source 2 <code>.dem</code> files offline into typed models, pandas DataFrames,
  JSON and Parquet.
</p>

<p align="center">
  <a href="https://pypi.org/project/gem-dota/"><img alt="PyPI version" src="https://img.shields.io/pypi/v/gem-dota.svg"></a>
  <a href="https://pypi.org/project/gem-dota/"><img alt="Python versions" src="https://img.shields.io/pypi/pyversions/gem-dota.svg"></a>
  <a href="https://github.com/whanyu1212/gem-dota/actions/workflows/ci.yml"><img alt="CI status" src="https://github.com/whanyu1212/gem-dota/actions/workflows/ci.yml/badge.svg?branch=main"></a>
  <a href="https://codecov.io/gh/whanyu1212/gem-dota"><img alt="Coverage" src="https://codecov.io/gh/whanyu1212/gem-dota/graph/badge.svg"></a>
  <a href="https://github.com/whanyu1212/gem-dota/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-2ea44f"></a>
</p>

<p align="center">
  <a href="https://whanyu1212.github.io/gem-dota/">Documentation</a> ·
  <a href="https://whanyu1212.github.io/gem-dota/guides/01_quickstart">Quickstart</a> ·
  <a href="https://whanyu1212.github.io/gem-dota/cookbook/questions">Recipes</a> ·
  <a href="https://whanyu1212.github.io/gem-dota/reference/">API reference</a> ·
  <a href="https://github.com/whanyu1212/gem-dota/blob/main/CHANGELOG.md">Changelog</a>
</p>

---

gem reads a replay the way the game recorded it: every entity update, combat-log
entry and chat event, rebuilt into one `ParsedMatch`. It runs offline, needs no API
keys, and handles both the old and new combat-log formats.

**Facts, not verdicts.** gem reports what happened: who was where, what they did,
what it cost and what followed. It doesn't score plays or decide whether a Roshan
"converted"; the [recipes](#recipes) show how to answer questions like that from the
facts, in code you can change.

## Install

gem needs Python 3.10 or newer.

```bash
# pip
pip install gem-dota

# uv (in a project)
uv add gem-dota

# uv (pip interface)
uv pip install gem-dota

# Poetry
poetry add gem-dota
```

Parquet export also needs `pyarrow` or `fastparquet`
([engine notes](https://whanyu1212.github.io/gem-dota/reference/dataframes)).

## Quickstart

```python
import gem

match = gem.parse("match.dem")

print(f"Score: {match.radiant_score}–{match.dire_score}")
for player in match.players:
    hero = gem.constants.hero_display(player.hero_name)
    print(f"{hero:20} {player.kills}/{player.deaths}/{player.assists}  {player.net_worth:,} NW")
```

No replay yet? `gem.fetch_replay(match_id, "replays/")` downloads and decompresses one
through OpenDota (Valve keeps replays for a limited time).

Prefer tables?

```python
frames = gem.parse_to_dataframe("match.dem")
frames["player_summary"]      # one row per player
frames["player_timeseries"]   # sampled gold, XP and net worth
frames["positions"]           # hero positions over time
frames["combat_log"]          # every normalized combat-log entry
```

Or the command line:

```bash
python -m gem match.dem
python -m gem match.dem --format json --output match.json
python -m gem batch replays/ --format parquet --output out/ --workers 4
```

## What you get

| Domain | Examples |
|---|---|
| Match and players | Score, winner, duration, teams, K/D/A, level, GPM/XPM, final net worth |
| Draft and objectives | Picks and bans, towers, barracks, Roshan and the Aegis, Tormentors, building status |
| Combat | The normalized combat log, damage and healing, kills, ability and item use, fights |
| Economy | Gold, XP and net-worth curves, minute-aligned advantages, purchases, a per-player gold ledger, exact buyback costs |
| Map | Hero positions, map regions, neutral camps, lane heatmaps, wards, smoke groups, couriers, runes |
| Items | Final inventories, neutral-item finds, consumed upgrades, Roshan drops, banner plants |
| Lookups | Position, net worth or ability level at a tick, nearby heroes, the fight at a tick, hero visibility |
| Exports | Dataclasses, DataFrames, JSON, Parquet, parallel multi-replay batches |

<p align="center">
  <img src="https://raw.githubusercontent.com/whanyu1212/gem-dota/main/site/public/map-annotations.jpg" alt="gem's map regions and the 28 neutral camps on the 7.41 map" width="720">
  <br>
  <sub>gem's map model: the river, both halves, the lotus pools and all 28 neutral camps, checked against the replays.
  <code>gem.region_of(x, y)</code> labels any position.</sub>
</p>

Good entry points:

- `gem.parse()` → `ParsedMatch`; `gem.parse_many()` for parallel batches
- `gem.parse_to_dataframe()`, `gem.to_json()` / `gem.load_json()`, `gem.to_parquet()`
- `gem.find_player()`, `gem.position_at_tick()`, `gem.fight_at_tick()`, `gem.region_of()`
- `gem.fetch_replay()` to download and decompress a replay by match ID

## Recipes

The [recipes](https://whanyu1212.github.io/gem-dota/cookbook/questions) answer one
question each from gem's facts and pandas. Every page has a figure for one match, the
answer across the test replays, and the code to run on yours:

- [Where were the fights, and who got the kills?](https://whanyu1212.github.io/gem-dota/cookbook/fights)
- [Where did each team ward, and what could the wards see?](https://whanyu1212.github.io/gem-dota/cookbook/wards)
- [How did each lane go?](https://whanyu1212.github.io/gem-dota/cookbook/lanes)
- [What moved the gold and XP lead?](https://whanyu1212.github.io/gem-dota/cookbook/lead)
- [When did each objective fall, and did teams convert their edges?](https://whanyu1212.github.io/gem-dota/cookbook/objectives)
- [Who took each rune, and what happened while a power rune lasted?](https://whanyu1212.github.io/gem-dota/cookbook/runes)
- [Did the Roshan team win the next fight?](https://whanyu1212.github.io/gem-dota/cookbook/roshan-next-fight) ·
  [How fast did each core farm from 10 to 20 minutes?](https://whanyu1212.github.io/gem-dota/cookbook/core-farm) ·
  [How often did a smoke lead to a kill?](https://whanyu1212.github.io/gem-dota/cookbook/smoke-to-kill)

The code lives in [`examples/cookbook/`](https://github.com/whanyu1212/gem-dota/tree/main/examples/cookbook):

```bash
python examples/cookbook/fights.py replays/*.dem
```

## Accuracy

gem is an independent Python implementation, checked against the
[Manta](https://github.com/dotabuff/manta), [Clarity](https://github.com/skadistats/clarity)
and [OpenDota](https://github.com/odota/parser) parsers at pinned revisions. On the
test replays and recent pro matches (most recently nine from October 2026), its per-player totals (K/D/A, last hits, net worth, GPM/XPM, hero and tower
damage, healing, wards, stacks, runes, buybacks) and per-minute gold, XP, last-hit and
deny curves match OpenDota exactly. Replays with an embedded postgame summary give
exact final gold, net worth and spending; older or incomplete replays fall back to
replay-derived values, and fields whose absence means something stay `None`.

Some outputs are reconstructed rather than recorded:

- Farming routes, smoke analysis, fight positioning and Roshan records are
  [experimental](https://whanyu1212.github.io/gem-dota/experimental/): they join replay
  facts with documented, inspectable rules.
- A truncated or corrupt replay returns what was read, with `parse_error` and
  `truncated_at_tick` set.
- Healing Lotus pickups aren't in the replay's event stream.

See [Replay Edge Cases](https://whanyu1212.github.io/gem-dota/deep-dives/replay-edge-cases)
for the details.

## Performance

gem is pure Python, built for research and batch analysis. A 40-minute professional
match parses in about a minute and a half on an Apple M2; `gem.parse_many()` spreads replays
across processes, and bounded Parquet export doesn't keep every finished match in
memory. The [performance study](https://whanyu1212.github.io/gem-dota/deep-dives/parser-performance)
has the method and numbers.

## Documentation

- [Quickstart](https://whanyu1212.github.io/gem-dota/guides/01_quickstart) and the
  [guides](https://whanyu1212.github.io/gem-dota/guides/) (entity state, combat log,
  DataFrames, fights, laning, the CLI, JSON output)
- [Recipes](https://whanyu1212.github.io/gem-dota/cookbook/questions)
- [API reference](https://whanyu1212.github.io/gem-dota/reference/)
- [Architecture](https://whanyu1212.github.io/gem-dota/architecture) and
  [parser internals](https://whanyu1212.github.io/gem-dota/deep-dives/); new to replay
  internals? Start with the
  [Bits & Bytes Primer](https://whanyu1212.github.io/gem-dota/cookbook/bits-and-bytes-primer)
- [Map regions and camps](https://whanyu1212.github.io/gem-dota/experimental/map-annotations)

## Development

```bash
git clone https://github.com/whanyu1212/gem-dota.git
cd gem-dota
uv sync --group dev

uv run pytest                                   # fast suite
uv run pytest -m "integration and not network"  # full replays (sync them first)
uv run ruff check . && uv run mypy src/gem/
```

Contributions are welcome: [CONTRIBUTING.md](https://github.com/whanyu1212/gem-dota/blob/main/CONTRIBUTING.md)
has the workflow and PR checklist. Parser changes are checked against the upstream
revisions pinned in [`upstream-refs.lock.json`](https://github.com/whanyu1212/gem-dota/blob/main/upstream-refs.lock.json)
(see [CLAUDE.md](https://github.com/whanyu1212/gem-dota/blob/main/CLAUDE.md)) and come
with focused regression tests.

## Acknowledgements

gem builds on years of open work by the Dota replay community:
[Manta](https://github.com/dotabuff/manta),
[Clarity](https://github.com/skadistats/clarity),
the [OpenDota parser](https://github.com/odota/parser),
[dotaconstants](https://github.com/odota/dotaconstants) and
[SteamTracking/Protobufs](https://github.com/SteamTracking/Protobufs). No source code
was copied from these projects: they are the references used to understand the protocol
and to validate gem's own implementation. See
[THIRD_PARTY_LICENSES](https://github.com/whanyu1212/gem-dota/blob/main/THIRD_PARTY_LICENSES)
for license texts.

gem is named after the **Gem of True Sight**: it reveals the match hidden in the
replay's bytes.

<p align="center">
  <a href="https://github.com/sponsors/whanyu1212"><img alt="Sponsor gem" src="https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?logo=github"></a>
</p>
