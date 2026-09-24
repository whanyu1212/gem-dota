# Batch Processing

Parallel multi-replay parsing via `ProcessPoolExecutor`.
Each worker process parses one replay independently, so performance scales with CPU cores.

::: info Memory
`parse_many_to_parquet` writes and discards each replay immediately, keeping memory
bounded by the worker count regardless of batch size. Load one table back across
replays with `read_parquet_table`. `parse_many_to_dataframe` is deprecated: it holds
every parsed match and every table in memory until concatenation.
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
        - parse_many_to_parquet
        - read_parquet_table
        - parse_many_to_dataframe
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

Source: [src/gem/replays/batch.py:127](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/replays/batch.py#L127)

### `parse_many_to_dataframe`

```python
def parse_many_to_dataframe(source: str | Path | Sequence[str | Path], *, workers: int | None = None, recursive: bool = False, progress: bool = True, timeout: float | None = None) -> dict[str, pd.DataFrame]
```

Parse multiple replays and concatenate results into per-table DataFrames.

Source: [src/gem/replays/batch.py:200](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/replays/batch.py#L200)

### `parse_many_to_parquet`

```python
def parse_many_to_parquet(source: str | Path | Sequence[str | Path], output_dir: str | Path, *, workers: int | None = None, recursive: bool = False, progress: bool = True, timeout: float | None = None, include: Iterable[str] = (), index: bool = False) -> list[Path]
```

Parse multiple replays and write each to its own parquet subdirectory.

Source: [src/gem/replays/batch.py:257](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/replays/batch.py#L257)

### `read_parquet_table`

```python
def read_parquet_table(output_dir: str | Path, table: str) -> pd.DataFrame
```

Load one table across every replay written by :func:`parse_many_to_parquet`.

Source: [src/gem/replays/batch.py:405](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/replays/batch.py#L405)

### Top-level classes

### `ParseResult`

```python
class ParseResult
```

Outcome of parsing a single replay.

Source: [src/gem/replays/batch.py:50](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/replays/batch.py#L50)

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

Source: [src/gem/replays/batch.py:64](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/replays/batch.py#L64)
