# Field Paths

Decodes Huffman-coded field path operations used to address properties inside entity deltas.

See also: [How Proto Parsing Works](../cookbook/proto-parsing-pipeline.md)


---


---

## Generated API

## `gem.schema.field_path.read_field_paths`

### `read_field_paths`

```python
def read_field_paths(r: BitReader) -> list[FieldPath]
```

Decode field paths into independent mutable compatibility objects.

Source: [src/gem/schema/field_path/path_sequence.py:99](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/field_path/path_sequence.py#L99)

## `gem.schema.field_path.FieldPath`

### `FieldPath`

```python
class FieldPath
```

A mutable path of up to 7 integer field indices.

Source: [src/gem/schema/field_path/models.py:11](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/field_path/models.py#L11)

#### Methods

##### `reset`

Signature: `def FieldPath.reset(self) -> None`

Reset to the initial empty state.

Source: [src/gem/schema/field_path/models.py:30](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/field_path/models.py#L30)

##### `pop`

Signature: `def FieldPath.pop(self, n: int) -> None`

Pop n levels off the path, zeroing the vacated slots.

Source: [src/gem/schema/field_path/models.py:36](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/field_path/models.py#L36)

##### `copy`

Signature: `def FieldPath.copy(self) -> FieldPath`

Return an independent copy of this path.

Source: [src/gem/schema/field_path/models.py:46](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/field_path/models.py#L46)

##### `to_tuple`

Signature: `def FieldPath.to_tuple(self) -> CompactFieldPath`

Return the active indices as an immutable tuple.

Source: [src/gem/schema/field_path/models.py:58](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/field_path/models.py#L58)

##### `to_str`

Signature: `def FieldPath.to_str(self) -> str`

Return a slash-separated string of active indices.

Source: [src/gem/schema/field_path/models.py:91](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/field_path/models.py#L91)

##### `plus_one`

Signature: `def FieldPath.plus_one(self) -> None`

Increment the deepest index by 1.

Source: [src/gem/schema/field_path/models.py:99](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/field_path/models.py#L99)

## `gem.schema.field_path.FieldPathOp`

### `FieldPathOp`

```python
class FieldPathOp
```

A single field-path operation with its Huffman weight.

Source: [src/gem/schema/field_path/operations.py:20](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/field_path/operations.py#L20)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `name` | `str` | `-` |
| `weight` | `int` | `-` |
| `fn` | `Callable[[BitReader, FieldPath], None]` | `-` |
