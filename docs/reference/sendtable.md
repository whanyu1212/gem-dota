# Send Tables

Parses flattened serializers into the schema tree used to decode packet entities and their fields.

See also: [Proto Parsing Pipeline](../cookbook/proto-parsing-pipeline.md)


---


---


---

## Generated API

## `gem.schema.sendtable.parse_send_tables`

### `parse_send_tables`

```python
def parse_send_tables(data: bytes, game_build: int = 0) -> dict[str, Serializer]
```

Parse a CDemoSendTables payload into a serializer dictionary.

Source: [src/gem/schema/sendtable/parser.py:168](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/sendtable/parser.py#L168)

## `gem.schema.sendtable.Serializer`

### `Serializer`

```python
class Serializer
```

A named, versioned entity class schema with an ordered list of fields.

Source: [src/gem/schema/sendtable/models.py:154](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/sendtable/models.py#L154)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `name` | `str` | `-` |
| `version` | `int` | `-` |
| `fields` | `list[Field]` | `field(...)` |

## `gem.schema.sendtable.Field`

### `Field`

```python
class Field
```

One property of a serializer, with its type and decoder.

Source: [src/gem/schema/sendtable/models.py:90](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/sendtable/models.py#L90)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `var_name` | `str` | `-` |
| `var_type` | `str` | `-` |
| `send_node` | `str` | `-` |
| `serializer_name` | `str` | `-` |
| `serializer_version` | `int` | `-` |
| `encoder` | `str` | `-` |
| `encode_flags` | `int | None` | `-` |
| `bit_count` | `int | None` | `-` |
| `low_value` | `float | None` | `-` |
| `high_value` | `float | None` | `-` |
| `parent_name` | `str` | `''` |
| `field_type` | `FieldType` | `field(...)` |
| `serializer` | `Serializer | None` | `None` |
| `model` | `int` | `FIELD_MODEL_SIMPLE` |
| `decoder` | `FieldDecoder | None` | `None` |
| `base_decoder` | `FieldDecoder | None` | `None` |
| `child_decoder` | `FieldDecoder | None` | `None` |

#### Methods

##### `set_model`

Signature: `def Field.set_model(self, model: int) -> None`

Assign the field model and wire up the appropriate decoders.

Source: [src/gem/schema/sendtable/models.py:111](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/sendtable/models.py#L111)

##### `model_name`

Signature: `def Field.model_name(self) -> str`

Return a human-readable model name for debugging.

Source: [src/gem/schema/sendtable/models.py:142](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/sendtable/models.py#L142)

## `gem.schema.sendtable.FieldType`

### `FieldType`

```python
class FieldType
```

Parsed representation of a C++ field type string.

Source: [src/gem/schema/sendtable/models.py:47](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/sendtable/models.py#L47)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `base_type` | `str` | `-` |
| `generic_type` | `FieldType | None` | `None` |
| `pointer` | `bool` | `False` |
| `count` | `int` | `0` |
