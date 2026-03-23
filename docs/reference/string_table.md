# String Tables

Manages incremental key/value side tables such as `instancebaseline` and `CombatLogNames`, including create/update flows.

See also: [How Proto Parsing Works](../cookbook/proto-parsing-pipeline.md)


---


---


---


---


---

## Generated API

## `gem.string_table.StringTables`

### `StringTables`

```python
class StringTables
```

Container for all string tables registered during a replay.

Source: [src/gem/string_table.py:61](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/string_table.py#L61)

#### Methods

##### `add`

Signature: `def StringTables.add(self, table: StringTable) -> None`

Register a StringTable in the container.

Source: [src/gem/string_table.py:74](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/string_table.py#L74)

##### `get_by_name`

Signature: `def StringTables.get_by_name(self, name: str) -> StringTable | None`

Return the table with the given name, or None if not found.

Source: [src/gem/string_table.py:83](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/string_table.py#L83)

##### `get_by_id`

Signature: `def StringTables.get_by_id(self, table_id: int) -> StringTable | None`

Return the table with the given index, or None if not found.

Source: [src/gem/string_table.py:97](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/string_table.py#L97)

## `gem.string_table.StringTable`

### `StringTable`

```python
class StringTable
```

A named string table with its metadata and current items.

Source: [src/gem/string_table.py:39](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/string_table.py#L39)

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

## `gem.string_table.StringTableItem`

### `StringTableItem`

```python
class StringTableItem(NamedTuple)
```

No docstring available.

Source: [src/gem/string_table.py:32](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/string_table.py#L32)

## `gem.string_table.parse_string_table`

### `parse_string_table`

```python
def parse_string_table(buf: bytes, num_updates: int, name: str, user_data_fixed_size: bool, user_data_size_bits: int, flags: int, varint_bit_counts: bool) -> list[StringTableItem]
```

Parse a string table data blob into a list of item updates.

Source: [src/gem/string_table.py:114](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/string_table.py#L114)

## `gem.string_table.handle_create`

### `handle_create`

```python
def handle_create(msg: object, string_tables: StringTables) -> StringTable
```

Process a CSVCMsg_CreateStringTable message.

Source: [src/gem/string_table.py:204](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/string_table.py#L204)

## `gem.string_table.handle_update`

### `handle_update`

```python
def handle_update(msg: object, string_tables: StringTables) -> StringTable
```

Process a CSVCMsg_UpdateStringTable message.

Source: [src/gem/string_table.py:260](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/string_table.py#L260)
