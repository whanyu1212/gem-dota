# Batch Processing

Parallel multi-replay parsing via `ProcessPoolExecutor`.
Each worker process parses one replay independently, so performance scales with CPU cores.

::: info Memory
`parse_many_to_parquet` streams completed parses directly to parquet and discards
each match immediately, keeping memory usage flat regardless of batch size.
`parse_many_to_dataframe` holds all results in memory until concatenation — prefer
`parse_many_to_parquet` for large batches.
:::

::: info Timeouts
`timeout=` is enforced per replay inside the worker after that replay starts
parsing. A timed-out replay is returned as `ParseResult(error=TimeoutError(...))`;
it does not raise a batch-level timeout or hide other completed results. On
platforms without `signal.SIGALRM`/`setitimer` support, passing `timeout=` raises
once before workers start.
:::

::: tip Parquet dependency
Parquet output requires an optional engine. Install `pyarrow` (recommended):
```bash
pip install pyarrow
```
:::

---

    options:
      members:
        - ParseResult
        - parse_many
        - parse_many_to_dataframe
        - parse_many_to_parquet
      show_source: true

---

## Generated API

## Module `gem.replays.batch`

Bulk replay parsing — process many ``.dem`` files in parallel.

Source: [src/gem/replays/batch.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/replays/batch.py#L1)

### Top-level functions

### `parse_many`

```python
def parse_many(source: str | Path | Sequence[str | Path], *, workers: int | None = None, recursive: bool = False, progress: bool = True, timeout: float | None = None) -> list[ParseResult]
```

Parse multiple replays in parallel and return a result per replay.

Source: [src/gem/replays/batch.py:235](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/replays/batch.py#L235)

### `parse_many_to_dataframe`

```python
def parse_many_to_dataframe(source: str | Path | Sequence[str | Path], *, workers: int | None = None, recursive: bool = False, progress: bool = True, timeout: float | None = None) -> dict[str, pd.DataFrame]
```

Parse multiple replays and concatenate results into per-table DataFrames.

Source: [src/gem/replays/batch.py:271](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/replays/batch.py#L271)

### `parse_many_to_parquet`

```python
def parse_many_to_parquet(source: str | Path | Sequence[str | Path], output_dir: str | Path, *, workers: int | None = None, recursive: bool = False, progress: bool = True, timeout: float | None = None, index: bool = False) -> list[Path]
```

Parse multiple replays and write each to its own parquet subdirectory.

Source: [src/gem/replays/batch.py:317](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/replays/batch.py#L317)

### Top-level classes

### `ParseResult`

```python
class ParseResult
```

Outcome of parsing a single replay.

Source: [src/gem/replays/batch.py:43](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/replays/batch.py#L43)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `path` | `Path` | `-` |
| `match` | `ParsedMatch \| None` | `-` |
| `error` | `Exception \| None` | `-` |

#### Properties

##### `ok`

Signature: `def ParseResult.ok(self) -> bool`

Return ``True`` when parsing succeeded.

Source: [src/gem/replays/batch.py:57](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/replays/batch.py#L57)
