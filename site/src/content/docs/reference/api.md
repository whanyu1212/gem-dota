# Public API

High-level helpers exposed from `import gem`. The implementation lives in
`gem.api`; `gem.__init__` re-exports this supported package surface.

---

## Generated API

## Module `gem.api`

High-level public API for Dota 2 Source 2 replay parsing.

Source: [src/gem/api.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/api.py#L1)

### Top-level functions

### `parse`

```python
def parse(path: str | Path) -> ParsedMatch
```

Parse a Dota 2 replay file and return structured match data.

Source: [src/gem/api.py:215](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/api.py#L215)

### `find_player`

```python
def find_player(match: ParsedMatch, hero: str) -> ParsedPlayer | None
```

Look up a player by hero name.

Source: [src/gem/api.py:330](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/api.py#L330)

### `parse_to_json`

```python
def parse_to_json(path: str | Path, *, analyze: bool = False, indent: int | None = None, sort_keys: bool = False) -> str
```

Parse a replay and return the result as JSON.

Source: [src/gem/api.py:350](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/api.py#L350)

### `parse_to_dataframe`

```python
def parse_to_dataframe(path: str | Path, *, include: Iterable[str] = ()) -> dict[str, pd.DataFrame]
```

Parse a replay and return flat tabular projections as pandas DataFrames.

Source: [src/gem/api.py:374](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/api.py#L374)

### `to_parquet`

```python
def to_parquet(match: ParsedMatch, output_dir: str | Path, *, include: Iterable[str] = (), index: bool = False) -> list[Path]
```

Export DataFrame projections for a parsed match to parquet files.

Source: [src/gem/api.py:409](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/api.py#L409)

### `parse_to_parquet`

```python
def parse_to_parquet(path: str | Path, output_dir: str | Path, *, include: Iterable[str] = (), index: bool = False) -> list[Path]
```

Parse a replay and export DataFrame projections to parquet files.

Source: [src/gem/api.py:451](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/api.py#L451)
