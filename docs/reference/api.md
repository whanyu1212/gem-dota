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

Source: [src/gem/api.py:123](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/api.py#L123)

### `find_player`

```python
def find_player(match: ParsedMatch, hero: str) -> ParsedPlayer | None
```

Look up a player by hero name.

Source: [src/gem/api.py:308](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/api.py#L308)

### `to_dict`

```python
def to_dict(match: ParsedMatch) -> dict[str, Any]
```

Convert a :class:`ParsedMatch` to a JSON-serializable dictionary.

Source: [src/gem/api.py:339](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/api.py#L339)

### `to_json`

```python
def to_json(match: ParsedMatch, *, indent: int | None = None, sort_keys: bool = False) -> str
```

Serialize a :class:`ParsedMatch` to a JSON string.

Source: [src/gem/api.py:344](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/api.py#L344)

### `parse_to_json`

```python
def parse_to_json(path: str | Path, *, indent: int | None = None, sort_keys: bool = False) -> str
```

Parse a replay and return the result as JSON.

Source: [src/gem/api.py:349](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/api.py#L349)

### `parse_to_dataframe`

```python
def parse_to_dataframe(path: str | Path) -> dict[str, pd.DataFrame]
```

Parse a replay and return tabular projections as pandas DataFrames.

Source: [src/gem/api.py:354](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/api.py#L354)

### `to_parquet`

```python
def to_parquet(match: ParsedMatch, output_dir: str | Path, *, index: bool = False) -> list[Path]
```

Export DataFrame projections for a parsed match to parquet files.

Source: [src/gem/api.py:376](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/api.py#L376)

### `parse_to_parquet`

```python
def parse_to_parquet(path: str | Path, output_dir: str | Path, *, index: bool = False) -> list[Path]
```

Parse a replay and export DataFrame projections to parquet files.

Source: [src/gem/api.py:407](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/api.py#L407)
