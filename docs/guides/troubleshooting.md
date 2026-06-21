# Troubleshooting

Common issues when installing `gem` and parsing replays, with quick fixes.

## Installation

### Verify the install

```bash
python -c "import gem; print(gem.__version__)"
```

If that prints a version, you're ready. The PyPI package is `gem-dota`; the import
name is `gem`:

::: code-group
```bash [pip]
pip install gem-dota
```
```bash [uv]
uv add gem-dota
```
:::

Requires Python 3.10+.

### `ImportError` for `snappy` / `python-snappy`

`gem` uses Snappy to decompress packet payloads, and it is installed automatically
as a dependency. If importing `gem` fails with a Snappy error, the C extension
likely couldn't build on your platform. Install your OS's Snappy development
library, then reinstall:

```bash
# macOS
brew install snappy
# Debian / Ubuntu
sudo apt-get install libsnappy-dev

pip install --force-reinstall gem-dota
```

### Parquet export raises `ImportError`

`gem.parse_to_parquet()` / `to_parquet()` need a Parquet engine, which is **not**
installed by default. Install one:

```bash
pip install pyarrow      # recommended
# or
pip install fastparquet
```

`pyarrow` and `fastparquet` are optional — you only need them for Parquet output.
DataFrame and JSON export work without them.

## Parsing

### `ValueError: unexpected magic: expected b'PBDEMS2\x00'`

`gem.parse()` expects a **decompressed Source 2** `.dem` file. This error almost
always means one of:

- **The file is still compressed.** Replays download from Valve's CDN as
  `.dem.bz2`. Decompress first — or let `gem` do it for you:

  ```python
  import gem
  path = gem.download_and_decompress(match_id, replay_url, out_dir=".")
  match = gem.parse(path)   # path is the decompressed .dem
  ```

- **The file isn't a replay** (an HTML error page saved with a `.dem` name, a
  truncated download, or a Source 1 replay). Re-download from a known-good source.

### Parsing returns partial data or stops early

Live, unfinished, or corrupted downloads can end abruptly. `gem` parses as far as
the stream allows and returns what it decoded. To isolate the cause:

- compare the file size against the source listing (a too-small file is truncated),
- re-download the replay,
- confirm a known-good replay parses cleanly in the same environment.

### Results look empty or zero

If `match.players` is populated but a specific field is empty (e.g. no wards, no
teamfights), the most common reasons are:

- **The event genuinely didn't occur** in that match (no smokes used, no Roshan
  killed).
- **Patch differences** — Valve occasionally renames internal fields between
  patches, so a value present in one replay can be absent in another. `gem`
  tolerates this and leaves the field empty rather than failing.

Cross-check against the [Full Match Data guide](04_match_data.md) to confirm you're
reading the right attribute (e.g. `match.towers`, not `match.tower_kills`).

### Handling failures across many replays

`gem.parse_many()` never raises on a bad replay — it captures the error per file so
one corrupt replay can't abort a batch. Each result carries `ok`, `match`, and
`error`:

```python
import gem

results = gem.parse_many(["a.dem", "b.dem", "broken.dem"])
ok      = [r.match for r in results if r.ok]
failed  = [(r.path, r.error) for r in results if not r.ok]

print(f"parsed {len(ok)}, failed {len(failed)}")
for path, err in failed:
    print(f"  {path}: {err}")
```

## Still stuck?

Open an issue on [GitHub](https://github.com/whanyu1212/gem-dota/issues) with:

- Python version + OS,
- the exact command or code you ran,
- the full traceback,
- the replay source (match id / salt if shareable),
- whether it reproduces on more than one replay.

---

## For contributors

Working on `gem` itself (cloned the repo) rather than consuming it from PyPI?

- **Dev environment:** `uv sync --group dev`, then run tools with `uv run …`
  (e.g. `uv run pytest`). See [CONTRIBUTING.md](https://github.com/whanyu1212/gem-dota/blob/main/CONTRIBUTING.md).
- **Docs build fails locally:** run `cd docs && npm install && npm run docs:build`.
  If it reports link issues, fix the broken links rather than disabling checks.
  Docs dependencies are pinned intentionally to avoid accidental major-version breakage.
