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

Source: [src/gem/schema/sendtable/parser.py:210](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/sendtable/parser.py#L210)

## `gem.schema.sendtable.Serializer`

### `Serializer`

```python
class Serializer
```

A named, versioned entity class schema with ordered fields.

Source: [src/gem/schema/sendtable/models.py:176](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/sendtable/models.py#L176)

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

One property of a serializer, including its type model and decoders.

Source: [src/gem/schema/sendtable/models.py:105](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/sendtable/models.py#L105)

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

Source: [src/gem/schema/sendtable/models.py:131](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/sendtable/models.py#L131)

##### `model_name`

Signature: `def Field.model_name(self) -> str`

Return a human-readable model name for debugging.

Source: [src/gem/schema/sendtable/models.py:164](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/sendtable/models.py#L164)

## `gem.schema.sendtable.FieldType`

### `FieldType`

```python
class FieldType
```

Parsed representation of a C++ field type string.

Source: [src/gem/schema/sendtable/models.py:53](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/sendtable/models.py#L53)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `base_type` | `str` | `-` |
| `generic_type` | `FieldType | None` | `None` |
| `pointer` | `bool` | `False` |
| `count` | `int` | `0` |
