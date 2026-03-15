# CLI Reference

gem ships a command-line interface you can invoke with `python -m gem`.
It covers two workflows:

- **`parse`** — parse a single replay and get a summary, JSON, or Parquet output.
- **`batch`** — parse a folder (or list) of replays in parallel and write the results.

---

## Quick examples

```bash
# Print a match summary (default)
python -m gem my_replay.dem

# Export to JSON
python -m gem my_replay.dem --format json > match.json

# Export to Parquet files
python -m gem parse my_replay.dem --format parquet --output ./out

# Parse a whole folder in parallel
python -m gem batch replays/ --format parquet --output ./out

# Concatenate all replays into one set of DataFrames
python -m gem batch replays/ --format dataframe --output ./out

# Show a live progress bar and timing breakdown
python -m gem my_replay.dem --progress --timings
```

---

## `parse` — single replay

```
python -m gem [parse] <path> [options]
```

!!! note
    The `parse` keyword is optional. `python -m gem match.dem` is identical to
    `python -m gem parse match.dem`.

| Option | Values | Default | Description |
|---|---|---|---|
| `<path>` | path to `.dem` | — | Replay file to parse |
| `--format` | `summary`, `json`, `parquet` | `summary` | Output format |
| `--output` | file or directory | stdout / cwd | Output destination. Required for `parquet`; optional for `json` (omit to print to stdout) |
| `--progress` | flag | off | Show a live phase-by-phase progress bar |
| `--timings` | flag | off | Print a timing breakdown after parsing |
| `--quiet`, `-q` | flag | off | Suppress banner and non-essential output |
| `--no-banner` | flag | off | Hide the ASCII art banner but keep other output |

### Summary output

The default format prints a Rich table with per-player KDA, gold, net worth,
last hits, denies, and hero kills, grouped by team.

```bash
python -m gem my_replay.dem
python -m gem my_replay.dem --no-banner        # skip ASCII art
python -m gem my_replay.dem --quiet            # minimal output
```

### JSON output

With `--format json`, the full `ParsedMatch` structure is serialised to JSON.
Omit `--output` to print to stdout (useful for piping):

```bash
# Print to stdout
python -m gem my_replay.dem --format json

# Write to a file
python -m gem parse my_replay.dem --format json --output match.json
```

Timings go to stderr when JSON is on stdout, so piping works cleanly:

```bash
python -m gem my_replay.dem --format json --timings > match.json
```

### Parquet output

`--format parquet` writes one `.parquet` file per DataFrame table into `--output`:

```bash
python -m gem parse my_replay.dem --format parquet --output ./out/
# Writes: out/players.parquet, out/combat_log.parquet, out/wards.parquet, ...
```

!!! note "Parquet dependency"
    Requires `pyarrow` (recommended) or `fastparquet`:
    ```bash
    pip install pyarrow
    ```

---

## `batch` — parallel multi-replay processing

```
python -m gem batch <source> [options]
```

`<source>` is either a directory path or one or more explicit `.dem` file paths.

| Option | Values | Default | Description |
|---|---|---|---|
| `<source>` | directory or file list | — | Replay(s) to parse |
| `--format` | `parquet`, `dataframe` | `parquet` | Output format |
| `--output` | directory | — | **Required.** Root output directory |
| `--workers` | integer | `os.cpu_count()` | Number of parallel worker processes |
| `--recursive` | flag | off | Scan `<source>` directory recursively |
| `--progress` | flag | off | Show a Rich progress bar |
| `--timings` | flag | off | Print timing breakdown after all replays |
| `--quiet`, `-q` | flag | off | Suppress all non-essential output |

### `--format parquet`

Each replay gets its own subdirectory under `--output`:

```bash
python -m gem batch replays/ --format parquet --output ./out

# Output layout:
# out/
#   match_6789/
#     players.parquet
#     combat_log.parquet
#     wards.parquet
#     ...
#   match_6790/
#     ...
```

### `--format dataframe`

All replays are concatenated into one set of DataFrames, then written as a flat
set of `.parquet` files under `--output`. Each row includes a `match_path` column
for provenance.

```bash
python -m gem batch replays/ --format dataframe --output ./out

# Output layout:
# out/
#   players.parquet       ← rows from all replays
#   combat_log.parquet
#   match.parquet
#   ...
```

This is equivalent to calling `gem.parse_many_to_dataframe()` and writing the
result to disk.

### Parallelism

By default gem uses all CPU cores. Cap workers for lighter load:

```bash
python -m gem batch replays/ --format parquet --output ./out --workers 4
```

!!! warning "Exit codes"
    The `batch` command exits with code `0` even when some replays fail.
    A summary table of failed replays is printed to stderr — always check it.

!!! tip
    Start with `--workers 4` on shared machines to leave cores free for other
    processes. On a dedicated parsing box, omit `--workers` to use all cores.

---

## Python API equivalents

All CLI operations have direct Python equivalents:

```python
import gem

# parse → summary  (inspect ParsedMatch directly)
match = gem.parse("my_replay.dem")

# parse → json
json_str = gem.parse_to_json("my_replay.dem", indent=2)

# parse → parquet
gem.parse_to_parquet("my_replay.dem", output_dir="./out")

# batch → list of ParseResult
results = gem.parse_many("replays/", workers=4)

# batch → concatenated DataFrames
dfs = gem.parse_many_to_dataframe("replays/", workers=4)
dfs["players"]  # has a match_path column

# batch → parquet (one subdir per replay)
gem.parse_many_to_parquet("replays/", output_dir="./out", workers=4)
```

See the [API Reference](../reference/index.md) for full parameter documentation.
