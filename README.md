<p align="center">
  <img src="https://raw.githubusercontent.com/whanyu1212/gem-dota/main/site/public/gem-readme-banner-wordmark-subtitle-spaced.png" alt="gem: a Dota 2 replay parser for Python" width="860">
</p>

<p align="center">
  <strong>Turn Dota 2 replays into analysis-ready Python data.</strong><br>
  Parse Source 2 <code>.dem</code> files offline into typed models, pandas DataFrames,
  JSON, Parquet, and interactive HTML reports.
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
  <a href="https://whanyu1212.github.io/gem-dota/reference/">API reference</a> ·
  <a href="https://github.com/whanyu1212/gem-dota/blob/main/CHANGELOG.md">Changelog</a>
</p>

---

## Install

Gem requires Python 3.10 or newer.

```bash
pip install gem-dota
```

Using another package manager? Run `uv add gem-dota` or `poetry add gem-dota`.
Parquet export additionally requires `pyarrow` or `fastparquet`; see the
[DataFrame and export reference](https://whanyu1212.github.io/gem-dota/reference/dataframes)
for current engine notes.

## Quickstart

```python
import gem

match = gem.parse("match.dem")

print(f"Score: {match.radiant_score}–{match.dire_score}")
for player in match.players:
    hero = gem.constants.hero_display(player.hero_name)
    print(f"{hero:20} {player.kills}/{player.deaths}/{player.assists}  {player.net_worth:,} NW")

# Convert the same structured result to JSON.
json_payload = gem.to_json(match, indent=2)
```

Need tables instead?

```python
frames = gem.parse_to_dataframe("match.dem")
players = frames["player_summary"]     # one row per player
series = frames["player_timeseries"]   # sampled gold/XP/net worth
positions = frames["positions"]
combat = frames["combat_log"]
```

Or use the CLI:

```bash
python -m gem match.dem
python -m gem match.dem --format json --output match.json
python -m gem batch replays/ --format parquet --output out/ --workers 4
```

## Why Gem?

| | |
|---|---|
| **🐍 Python-native**<br>Typed match objects plug directly into notebooks, pandas, ML pipelines, and ordinary Python code. | **🔎 Replay-first**<br>Analyze local replays without depending on third-party match-history availability. |
| **⚔️ Full-match context**<br>Draft, combat, economy, vision, movement, objectives, items, chat, and fights in one model. | **📦 Flexible outputs**<br>Work with dataclasses, DataFrames, JSON, Parquet, batch exports, or a self-contained HTML report. |

Gem is named after the **Gem of True Sight**: it reveals the structured match state
hidden inside dense replay bytes. The parser is an independent Python implementation,
cross-checked against Manta, Clarity, the OpenDota parser, and replay-derived validation
fixtures.

**Facts, not verdicts.** Gem reports what the replay records: who was where, what they
did, what it cost and what happened next. It doesn't score plays or decide whether a
Roshan was "converted"; that interpretation is yours to build on top. Gem 0.12
deprecates the older helpers that did this, and 0.13 removes them.

## Match reports

Gem can turn a parsed replay into a self-contained interactive report with overview,
combat, laning, farming, fight, Roshan, vision, economy, draft, and movement views.

<p align="center">
  <img src="https://raw.githubusercontent.com/whanyu1212/gem-dota/main/assets/readme-report-overview.png" alt="Gem interactive Dota 2 match report overview" width="100%">
  <br>
  <sub>Interactive HTML report generated from a real <code>.dem</code> replay.</sub>
</p>

<table>
  <tr>
    <td width="34%" valign="top" align="center">
      <a href="https://raw.githubusercontent.com/whanyu1212/gem-dota/main/assets/readme-report-vision.png">
        <img src="https://raw.githubusercontent.com/whanyu1212/gem-dota/main/assets/readme-report-vision.png" alt="Gem interactive ward map at 16 minutes" width="100%">
      </a>
      <br>
      <sub><strong>Vision</strong> — scrub through observer and sentry ward activity.</sub>
    </td>
    <td width="66%" valign="top" align="center">
      <a href="https://raw.githubusercontent.com/whanyu1212/gem-dota/main/assets/readme-report-teamfight.png">
        <img src="https://raw.githubusercontent.com/whanyu1212/gem-dota/main/assets/readme-report-teamfight.png" alt="Gem fight breakdown with positions, combat statistics and an Aegis badge" width="100%">
      </a>
      <br>
      <sub><strong>Fights</strong> — step through positions, then inspect damage, abilities, and reveals.</sub>
    </td>
  </tr>
</table>

```python
from gem.reports import fetch_match_icons, write_html_report

assets = fetch_match_icons(match)  # downloads the hero/item icons this match needs
write_html_report(match, "match-report.html", assets=assets)
```

Hero and item icons are Valve's artwork, so Gem doesn't ship them. `fetch_match_icons`
downloads the ones a match needs into a local cache; `write_html_report` itself never
downloads, and shows a hero's name where its icon is missing.
`examples/match_report.py` fetches the icons for you (`--offline` skips this). See the
[asset-cache guide](https://whanyu1212.github.io/gem-dota/guides/09_cli#reports-assets-report-asset-cache)
and the [report API](https://whanyu1212.github.io/gem-dota/reference/reports) for details.

## What you get

| Domain | Examples |
|---|---|
| Match and players | Scores, winner, duration, teams, K/D/A, level, GPM/XPM, final net worth |
| Draft and objectives | Picks/bans, towers, barracks, Roshan, Aegis, Tormentor, building status |
| Combat | Normalized combat log, damage/healing, kills, ability and item usage, fights |
| Economy | Gold, XP, net-worth and minute-aligned advantage curves, purchases, per-player gold ledger, exact buyback costs |
| Map state | Player positions, map regions (river, halves, lotus pools), neutral camps, lane heatmaps, wards, smoke groups, courier snapshots |
| Items | Final inventories, neutral-item finds, consumed upgrades, Roshan drops and banner plants |
| Lookups | Position, net worth and ability level at a tick, nearby heroes, the fight at a tick, hero visibility, smoke lifecycles and first fights, the Aegis lifecycle |
| Exports | DataFrames, JSON, Parquet, multi-replay processing, interactive HTML reports |

Useful entry points include:

- `gem.parse()` → `ParsedMatch`
- `gem.parse_to_dataframe()` / `gem.to_json()` / `gem.to_parquet()`
- `gem.parse_many*()` for parallel replay batches
- `gem.find_player()`, `gem.position_at_tick()`, and `gem.fight_at_tick()`
- `gem.region_of()` to label a position as river, either half, or a lotus pool
- `gem.fetch_replay()` for OpenDota/Valve replay download and decompression

For current complete replays, Gem's minute curves are validated against OpenDota's
effective sampling boundaries. Embedded `MatchDetails` data enables exact postgame
duration, damage, healing, GPM, and XPM values. Older or incomplete replays use
replay-derived fallbacks. Fields whose absence is meaningful—such as consumed-upgrade
flags—remain `None`; other outputs use the documented defaults for their field type.

## Documentation

The hosted documentation covers both the public API and the replay format itself:

- [Getting started](https://whanyu1212.github.io/gem-dota/guides/01_quickstart)
- [Architecture](https://whanyu1212.github.io/gem-dota/architecture)
- [Parser internals](https://whanyu1212.github.io/gem-dota/deep-dives/)
- [CLI reference](https://whanyu1212.github.io/gem-dota/guides/09_cli)
- [Parser performance](https://whanyu1212.github.io/gem-dota/deep-dives/parser-performance)
- [Map regions and camps](https://whanyu1212.github.io/gem-dota/experimental/map-annotations): how Gem's map annotation
  was checked against the replays
- [Experimental analysis](https://whanyu1212.github.io/gem-dota/experimental/)

New to replay internals? Start with the
[Bits & Bytes Primer](https://whanyu1212.github.io/gem-dota/cookbook/bits-and-bytes-primer),
then continue into the parser and entity-system deep dives.

## Performance and scope

Gem is a pure-Python parser optimized for research, batch analysis, and direct use in
the Python data ecosystem. Multi-replay APIs distribute work across processes, while
bounded Parquet export avoids retaining every completed match at once. The
[v0.8 performance study](https://whanyu1212.github.io/gem-dota/deep-dives/parser-performance) records the benchmark
method, compatibility checks, and current optimization boundary without claiming an
apples-to-oranges win over Go or Java parsers.

Some outputs are necessarily reconstructed:

- Farming routes, smoke analysis, fight positioning and Roshan records are experimental:
  they join replay facts with documented, inspectable rules. gem 0.13 removed the
  tags, scores and territory estimates that used to sit on top of them.
- Incomplete replays can return partial output, and some exact postgame fields require embedded match details.
- Healing Lotus pickups are not available from the replay event stream.
- Hero/item icons and the report map image are not shipped in the wheel; call
  `gem.reports.fetch_match_icons(match)` to download the icons a report needs.

See [Replay Edge Cases](https://whanyu1212.github.io/gem-dota/deep-dives/replay-edge-cases)
and the experimental-feature guides for the detailed boundaries.

## Development

```bash
git clone https://github.com/whanyu1212/gem-dota.git
cd gem-dota
uv sync --group dev

uv run pytest
uv run pytest -m "integration and not network"
uv run ruff check src/ tests/
uv run mypy src/gem/
```

Contributions are welcome. Read [CONTRIBUTING.md](https://github.com/whanyu1212/gem-dota/blob/main/CONTRIBUTING.md) for the workflow and
PR checklist. Parser changes should be checked against the pinned upstream reference
revisions listed in [CLAUDE.md](https://github.com/whanyu1212/gem-dota/blob/main/CLAUDE.md)
and accompanied by focused regression tests. Additional tool guidance is available in
[AGENTS.md](https://github.com/whanyu1212/gem-dota/blob/main/AGENTS.md).

## Acknowledgements

Gem builds on years of open work by the Dota replay community:
[Manta](https://github.com/dotabuff/manta),
[Clarity](https://github.com/skadistats/clarity),
[OpenDota parser](https://github.com/odota/parser), and
[dotaconstants](https://github.com/odota/dotaconstants).

No source code was copied from these projects; they are reference implementations used
to understand protocol behavior and validate Gem's independent Python implementation.
See [THIRD_PARTY_LICENSES](https://github.com/whanyu1212/gem-dota/blob/main/THIRD_PARTY_LICENSES)
for license texts.

<p align="center">
  <a href="https://github.com/sponsors/whanyu1212"><img alt="Sponsor Gem" src="https://img.shields.io/badge/Sponsor-GitHub-ea4aaa?logo=github"></a>
</p>
