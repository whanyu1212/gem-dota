# Gem

<div class="hero-card">
  <h2>Python Dota 2 Replay Parser</h2>
  <p>
    <strong>gem</strong> reads Source 2 <code>.dem</code> replay files and turns them into
    structured Python objects — named after the <em>Gem of True Sight</em>, which reveals
    what is hidden. Parse a replay and work with the result directly in pandas, notebooks,
    and ML pipelines.
  </p>
  <div class="hero-actions">
    <a class="VPButton medium brand" href="guides/01_quickstart">Quickstart</a>
    <a class="VPButton medium alt" href="reference/">API Reference</a>
    <a class="VPButton medium alt" href="changelog">Changelog</a>
    <a class="VPButton medium alt" href="guides/troubleshooting">Troubleshooting</a>
    <a class="VPButton medium alt" href="cookbook/bits-and-bytes-primer">Bits &amp; Bytes Primer</a>
    <a class="VPButton medium alt" href="cookbook/">Proto Cookbook</a>
    <a class="VPButton medium alt" href="experimental/">Experimental Features</a>
    <a class="VPButton medium alt" href="reports/">Reports</a>
  </div>
</div>

## Install

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

match = gem.parse("my_replay.dem")        # -> ParsedMatch
print(match.duration_minutes, "min,", len(match.players), "players")
```

## What you can do

- **Parse one call** — `gem.parse(path)` returns a typed `ParsedMatch`: players, draft,
  combat log, wards, objectives, teamfights, couriers, smoke events, aegis, and chat.
- **Export anywhere** — convert to pandas DataFrames, JSON, or Parquet with a single
  function (`gem.parse_to_dataframe`, `gem.parse_to_json`, `gem.parse_to_parquet`).
- **Batch in parallel** — `gem.parse_many*` parses many replays across processes; failed
  replays are captured, not raised.
- **Exact ward coordinates** — ward placements carry precise map coordinates pulled from
  the entity stream, not approximations.
- **Experimental interpretation layers** — Farming Patterns, Roshan Conversion, and vision
  estimation, each documented with formulas, thresholds, drivers, and known limits.
- **CLI included** — parse, export, and batch-process from the terminal with no Python code.

```python
# Export
frames = gem.parse_to_dataframe("replay.dem")    # -> dict[str, pandas.DataFrame]
json_str = gem.parse_to_json("replay.dem", indent=2)   # -> JSON string
gem.parse_to_parquet("replay.dem", "./out")      # one Parquet file per frame in ./out

# Batch (across processes)
gem.parse_many_to_parquet(["a.dem", "b.dem"], "./out", workers=8)
```

```bash
# Same things from the terminal
python -m gem parse replay.dem --format json --output out.json
```

## Where to start

::: tip I want to use it
Start with the [Quickstart](./guides/01_quickstart.md) for install-to-KDA in a few lines,
then [Full Match Data](./guides/04_match_data.md) for a walkthrough of everything in
`ParsedMatch`.
:::

::: info I want to understand the format
Read [How Proto Parsing Works](./cookbook/proto-parsing-pipeline.md), then use the
[Proto Field Atlas](./cookbook/proto-fields/) for per-message field details. The
[Deep Dives](./deep-dives/) trace each layer of the parser.
:::

::: info I need the API
Go to the [API Reference](./reference/). Every public class and function has a
Google-style docstring, and the reference pages link straight to source.
:::

## Project status

`gem` is published to PyPI as [`gem-dota`](https://pypi.org/project/gem-dota/). The full
parsing pipeline and every extractor are complete and stable. It is a pure-Python parser:
the Go ([Manta](https://github.com/dotabuff/manta)) and Java
([Clarity](https://github.com/skadistats/clarity)) reference parsers are faster in raw
throughput — `gem` optimizes instead for Python-native ergonomics and an implementation
you can read end-to-end. See the [Changelog](./changelog.md) for the latest parser,
validation, and report changes.
