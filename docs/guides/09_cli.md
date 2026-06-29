# CLI Reference

gem ships a command-line interface you can invoke with `python -m gem`.

It covers three workflows:

- `parse` - parse one replay and print a summary, JSON, or Parquet output.
- `batch` - parse many replays in parallel.
- `reports assets` - inspect and populate the local asset cache used by HTML reports.

## Quick examples

```bash
# Print a match summary
python -m gem my_replay.dem

# Export one replay to JSON
python -m gem my_replay.dem --format json > match.json

# Export one replay to Parquet files
python -m gem parse my_replay.dem --format parquet --output ./out

# Parse a folder in parallel
python -m gem batch replays/ --format parquet --output ./out --workers 4

# Fail CI if any replay fails or times out
python -m gem batch replays/ --format parquet --output ./out --timeout 120 --strict

# Concatenate all replays into one set of DataFrames
python -m gem batch replays/ --format dataframe --output ./out

# Inspect report asset-cache paths and completeness
python -m gem reports assets path
python -m gem reports assets status
```

## `parse` - single replay

```bash
python -m gem [parse] <path> [options]
```

::: info
The `parse` keyword is optional. `python -m gem match.dem` is identical to
`python -m gem parse match.dem`.
:::

| Option | Values | Default | Description |
|---|---|---|---|
| `<path>` | path to `.dem` | - | Replay file to parse |
| `--format` | `summary`, `json`, `parquet` | `summary` | Output format |
| `--output` | file or directory | stdout / cwd | Output destination. Required for `parquet`; optional for `json` |
| `--progress` | flag | off | Show a live phase-by-phase progress bar |
| `--timings` | flag | off | Print a timing breakdown after parsing |
| `--quiet`, `-q` | flag | off | Suppress banner and non-essential output |
| `--no-banner` | flag | off | Hide the ASCII art banner but keep other output |

### Summary output

The default format prints a Rich table with per-player KDA, gold, net worth, last hits,
denies, and hero kills.

```bash
python -m gem my_replay.dem
python -m gem my_replay.dem --no-banner
python -m gem my_replay.dem --quiet
```

### JSON output

With `--format json`, the full `ParsedMatch` structure is serialized to JSON. Omit
`--output` to print JSON to stdout:

```bash
python -m gem my_replay.dem --format json
python -m gem parse my_replay.dem --format json --output match.json
```

Timings go to stderr when JSON is written to stdout, so piping works cleanly:

```bash
python -m gem my_replay.dem --format json --timings > match.json
```

### Parquet output

`--format parquet` writes one `.parquet` file per DataFrame table into `--output`:

```bash
python -m gem parse my_replay.dem --format parquet --output ./out

# Example files:
# out/players.parquet
# out/combat_log.parquet
# out/teamfights.parquet
# out/opendota_teamfights.parquet
```

::: info Parquet dependency
Requires `pyarrow` or `fastparquet`.
:::

## `batch` - parallel multi-replay processing

```bash
python -m gem batch <source> [options]
```

`<source>` is either a directory path or one or more explicit `.dem` file paths.

| Option | Values | Default | Description |
|---|---|---|---|
| `<source>` | directory or file list | - | Replay(s) to parse |
| `--format` | `parquet`, `dataframe` | `parquet` | Output format |
| `--output` | directory | - | Required root output directory |
| `--workers` | integer | `os.cpu_count()` | Number of parallel worker processes |
| `--recursive` | flag | off | Scan source directories recursively |
| `--timeout` | seconds | off | Per-replay parse timeout; timed-out replays are reported as failures |
| `--strict` | flag | off | Exit with code `1` if any replay fails |
| `--progress` | flag | off | Show a Rich progress bar |
| `--timings` | flag | off | Print timing breakdown after all replays |
| `--quiet`, `-q` | flag | off | Suppress all non-essential output |

### One Parquet directory per replay

```bash
python -m gem batch replays/ --format parquet --output ./out

# Output layout:
# out/
#   match_6789/
#     players.parquet
#     combat_log.parquet
#     ...
#   match_6790/
#     ...
```

### Concatenated DataFrames

`--format dataframe` concatenates each table across all parsed replays and writes one
flat set of `.parquet` files under `--output`. Each row includes a `match_path` column
for provenance.

```bash
python -m gem batch replays/ --format dataframe --output ./out

# Output layout:
# out/
#   players.parquet
#   combat_log.parquet
#   match.parquet
#   ...
```

::: warning Exit codes
By default, the `batch` command exits with code `0` even when some replays fail, for
backward compatibility. It prints a batch summary plus a typed table of failed replays;
pass `--strict` to exit with code `1` whenever any replay fails or times out.
:::

## `reports assets` - report asset cache

HTML reports can inline hero icons, item icons, and map images when those assets are
available locally. gem does not bundle these assets in the wheel; the CLI manages a user
cache for them.

```bash
# Show cache directories
python -m gem reports assets path

# Check which assets are present or missing
python -m gem reports assets status

# Exit 1 if any checked asset kind is incomplete
python -m gem reports assets status --strict

# Download hero and item icons
python -m gem reports assets download --icons

# Download only one icon category
python -m gem reports assets download --hero-icons
python -m gem reports assets download --item-icons

# Re-download existing icons
python -m gem reports assets download --icons --force

# Include recipe_* item icons in item checks/downloads
python -m gem reports assets status --include-recipes
python -m gem reports assets download --item-icons --include-recipes

# Add a locally downloaded map image to the cache
python -m gem reports assets add-map ./Game_map_7.40.jpg
python -m gem reports assets add-map ./map.jpg --name Game_map_7.40.jpg
```

All `reports assets` subcommands accept `--asset-dir` to use a custom cache root. You can
also set `GEM_REPORT_ASSET_DIR`.

## Python API equivalents

```python
import gem

match = gem.parse("my_replay.dem")

json_str = gem.parse_to_json("my_replay.dem", indent=2)

gem.parse_to_parquet("my_replay.dem", output_dir="./out")

results = gem.parse_many("replays/", workers=4)

dfs = gem.parse_many_to_dataframe("replays/", workers=4)

gem.parse_many_to_parquet("replays/", output_dir="./out", workers=4)
```

See the [API Reference](../reference/index.md) for full parameter documentation.
