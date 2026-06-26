---
title: Gem
---

<section class="gem-hero">
  <p class="gem-hero-label">Python replay parsing for Dota 2</p>
  <h1>Turn Source 2 <code>.dem</code> files into analysis-ready Python data.</h1>
  <p class="gem-hero-lede">
    <strong>gem</strong> reads Dota 2 replay files and returns typed match objects,
    pandas DataFrames, JSON, Parquet, and self-contained HTML reports.
  </p>
  <div class="gem-hero-actions">
    <a class="gem-button gem-button--primary" href="guides/01_quickstart">Quickstart</a>
    <a class="gem-button gem-button--secondary" href="reference/">API Reference</a>
    <a class="gem-button gem-button--secondary" href="cookbook/">Proto Cookbook</a>
  </div>
</section>

<div class="gem-trust">
  <a class="gem-trust-item" href="https://pypi.org/project/gem-dota/" target="_blank" rel="noreferrer">
    <span class="gem-trust-k">Install</span>
    <span class="gem-trust-v">On PyPI as <code>gem-dota</code></span>
  </a>
  <span class="gem-trust-item">
    <span class="gem-trust-k">Runtime</span>
    <span class="gem-trust-v">Pure Python · 3.10+</span>
  </span>
  <span class="gem-trust-item">
    <span class="gem-trust-k">Readable</span>
    <span class="gem-trust-v">Implementation you can read end-to-end</span>
  </span>
</div>

::: code-group

```bash [pip]
pip install gem-dota
```

```bash [uv]
uv add gem-dota
```

:::

Requires Python 3.10+. The import name is `gem`; the PyPI package is `gem-dota`.

```python
import gem
from gem.constants import hero_display

# Parse a local replay into a typed ParsedMatch object.
match = gem.parse("replay.dem")
print(match.duration_minutes, "min ·", len(match.players), "players")

# Every field is a real Python attribute — inspect players directly.
for p in match.players:
    print(hero_display(p.hero_name), p.net_worth, p.kills, p.deaths)

# Or pull analysis-ready pandas DataFrames in one call.
frames = gem.parse_to_dataframe("replay.dem")
frames["combat_log"].head()
```

## What you can do

<div class="gem-feature-grid">
  <a class="gem-feature-card" href="guides/04_match_data">
    <span class="gem-feature-icon" aria-hidden="true">◵</span>
    <span class="gem-feature-kicker">Parse</span>
    <strong>Typed match data</strong>
    <span>Players, draft, combat log, wards, objectives, teamfights, couriers, smoke, Aegis, and chat.</span>
  </a>
  <a class="gem-feature-card" href="guides/05_timeseries">
    <span class="gem-feature-icon" aria-hidden="true">◷</span>
    <span class="gem-feature-kicker">Analyze</span>
    <strong>DataFrames and time series</strong>
    <span>Export player snapshots, positions, combat rows, advantages, and OpenDota-shaped tables.</span>
  </a>
  <a class="gem-feature-card" href="guides/09_cli">
    <span class="gem-feature-icon" aria-hidden="true">⎇</span>
    <span class="gem-feature-kicker">Operate</span>
    <strong>CLI and batch workflows</strong>
    <span>Parse one replay, process folders in parallel, export Parquet, and manage report assets.</span>
  </a>
  <a class="gem-feature-card" href="reports/">
    <span class="gem-feature-icon" aria-hidden="true">◳</span>
    <span class="gem-feature-kicker">Report</span>
    <strong>HTML match reports</strong>
    <span>Generate portable replay reports with movement, combat, teamfight, vision, and farming views.</span>
  </a>
</div>

## Common workflows

```python
# Export to analysis formats
frames = gem.parse_to_dataframe("replay.dem")
json_str = gem.parse_to_json("replay.dem", indent=2)
gem.parse_to_parquet("replay.dem", "./out")

# Batch across processes
gem.parse_many_to_parquet(["a.dem", "b.dem"], "./out", workers=8)
```

```bash
# Same workflow from the terminal
python -m gem parse replay.dem --format json --output out.json
python -m gem batch replays/ --format parquet --output ./out --workers 4
```

## Where to start

<div class="gem-start-grid">
  <a class="gem-start-card" href="guides/01_quickstart">
    <span>Use it</span>
    <strong>Quickstart</strong>
    <small>Install gem, parse one replay, inspect players, and export data.</small>
  </a>
  <a class="gem-start-card" href="cookbook/proto-parsing-pipeline">
    <span>Understand it</span>
    <strong>Proto Parsing Pipeline</strong>
    <small>Learn how outer demo frames, inner net messages, and protobuf payloads fit together.</small>
  </a>
  <a class="gem-start-card" href="reference/">
    <span>Integrate it</span>
    <strong>API Reference</strong>
    <small>Every public class and function, generated from the Python docstrings.</small>
  </a>
</div>

## Project status

`gem` is published to PyPI as [`gem-dota`](https://pypi.org/project/gem-dota/). The full
parsing pipeline and every extractor are complete and stable. It is a pure-Python parser:
the Go ([Manta](https://github.com/dotabuff/manta)) and Java
([Clarity](https://github.com/skadistats/clarity)) reference parsers are faster in raw
throughput; `gem` optimizes instead for Python-native ergonomics and an implementation
you can read end-to-end.

See the [Changelog](./changelog.md) for the latest parser, validation, and report changes.
