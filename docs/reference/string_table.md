# String Tables

Manages incremental key/value side tables such as `instancebaseline` and `CombatLogNames`, including create/update flows.

See also: [String Tables](../deep-dives/string-tables.md) for the entry format and
name compression, and [How Proto Parsing Works](../cookbook/proto-parsing-pipeline.md).

---

## Generated API

## `gem.state.string_table.StringTables`

### `StringTables`

```python
class StringTables
```

Container for all string tables registered during a replay.

Source: [src/gem/state/string_table.py:75](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/string_table.py#L75)

#### Methods

##### `clear`

Signature: `def StringTables.clear(self) -> None`

Remove every table, as ``svc_ClearAllStringTables`` requests.

Source: [src/gem/state/string_table.py:88](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/string_table.py#L88)

##### `add`

Signature: `def StringTables.add(self, table: StringTable) -> None`

Register a StringTable in the container.

Source: [src/gem/state/string_table.py:97](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/string_table.py#L97)

##### `get_by_name`

Signature: `def StringTables.get_by_name(self, name: str) -> StringTable | None`

Return the table with the given name, or None if not found.

Source: [src/gem/state/string_table.py:106](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/string_table.py#L106)

##### `get_by_id`

Signature: `def StringTables.get_by_id(self, table_id: int) -> StringTable | None`

Return the table with the given index, or None if not found.

Source: [src/gem/state/string_table.py:120](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/string_table.py#L120)

## `gem.state.string_table.StringTable`

### `StringTable`

```python
class StringTable
```

A named string table with its metadata and current items.

Source: [src/gem/state/string_table.py:53](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/string_table.py#L53)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `index` | `int` | `-` |
| `name` | `str` | `-` |
| `items` | `dict[int, tuple[str, bytes]]` | `field(...)` |
| `user_data_fixed_size` | `bool` | `False` |
| `user_data_size_bits` | `int` | `0` |
| `flags` | `int` | `0` |
| `varint_bit_counts` | `bool` | `False` |

## `gem.state.string_table.StringTableItem`

### `StringTableItem`

```python
class StringTableItem(NamedTuple)
```

No docstring available.

Source: [src/gem/state/string_table.py:46](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/string_table.py#L46)

## `gem.state.string_table.parse_string_table`

### `parse_string_table`

```python
def parse_string_table(buf: bytes, num_updates: int, name: str, user_data_fixed_size: bool, user_data_size_bits: int, flags: int, varint_bit_counts: bool, existing: Mapping[int, tuple[str, bytes]] | None = None) -> list[StringTableItem]
```

Parse a string table data blob into a list of item updates.

Source: [src/gem/state/string_table.py:137](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/string_table.py#L137)

## `gem.state.string_table.handle_create`

### `handle_create`

```python
def handle_create(msg: object, string_tables: StringTables) -> StringTable
```

Process a CSVCMsg_CreateStringTable message.

Source: [src/gem/state/string_table.py:259](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/string_table.py#L259)

## `gem.state.string_table.handle_update`

### `handle_update`

```python
def handle_update(msg: object, string_tables: StringTables) -> StringTable
```

Process a CSVCMsg_UpdateStringTable message.

Source: [src/gem/state/string_table.py:312](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/string_table.py#L312)
