# Batch Processing

Parallel multi-replay parsing via `ProcessPoolExecutor`.
Each worker process parses one replay independently, so performance scales with CPU cores.

::: info Memory
`parse_many_to_parquet` writes and discards each replay immediately, keeping memory
usage flat regardless of batch size. `parse_many_to_dataframe` holds all results in
memory until concatenation — prefer `parse_many_to_parquet` for large batches.
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

## Module `gem.batch`

Bulk replay parsing — process many ``.dem`` files in parallel.

Source: [src/gem/batch.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/batch.py#L1)

### Top-level functions

### `parse_many`

```python
def parse_many(source: str | Path | Sequence[str | Path], *, workers: int | None = None, recursive: bool = False, progress: bool = True, timeout: float | None = None) -> list[ParseResult]
```

Parse multiple replays in parallel and return a result per replay.

Source: [src/gem/batch.py:116](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/batch.py#L116)

### `parse_many_to_dataframe`

```python
def parse_many_to_dataframe(source: str | Path | Sequence[str | Path], *, workers: int | None = None, recursive: bool = False, progress: bool = True, timeout: float | None = None) -> dict[str, pd.DataFrame]
```

Parse multiple replays and concatenate results into per-table DataFrames.

Source: [src/gem/batch.py:189](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/batch.py#L189)

### `parse_many_to_parquet`

```python
def parse_many_to_parquet(source: str | Path | Sequence[str | Path], output_dir: str | Path, *, workers: int | None = None, recursive: bool = False, progress: bool = True, timeout: float | None = None, index: bool = False) -> list[Path]
```

Parse multiple replays and write each to its own parquet subdirectory.

Source: [src/gem/batch.py:235](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/batch.py#L235)

### Top-level classes

### `ParseResult`

```python
class ParseResult
```

Outcome of parsing a single replay.

Source: [src/gem/batch.py:39](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/batch.py#L39)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `path` | `Path` | `-` |
| `match` | `ParsedMatch | None` | `-` |
| `error` | `Exception | None` | `-` |

#### Properties

##### `ok`

Signature: `def ParseResult.ok(self) -> bool`

Return ``True`` when parsing succeeded.

Source: [src/gem/batch.py:53](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/batch.py#L53)
