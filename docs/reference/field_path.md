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

Decode a Huffman-coded sequence of field paths from r.

Source: [src/gem/schema/field_path/decoder.py:20](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/field_path/decoder.py#L20)

## `gem.schema.field_path.FieldPath`

### `FieldPath`

```python
class FieldPath
```

A mutable path of up to 7 integer field indices.

Source: [src/gem/schema/field_path/model.py:8](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/field_path/model.py#L8)

#### Methods

##### `reset`

Signature: `def FieldPath.reset(self) -> None`

Reset to the initial empty state.

Source: [src/gem/schema/field_path/model.py:27](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/field_path/model.py#L27)

##### `pop`

Signature: `def FieldPath.pop(self, n: int) -> None`

Pop n levels off the path, zeroing the vacated slots.

Source: [src/gem/schema/field_path/model.py:33](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/field_path/model.py#L33)

##### `copy`

Signature: `def FieldPath.copy(self) -> FieldPath`

Return an independent copy of this path.

Source: [src/gem/schema/field_path/model.py:43](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/field_path/model.py#L43)

##### `to_tuple`

Signature: `def FieldPath.to_tuple(self) -> tuple[int, ...]`

Return the active indices as an immutable tuple.

Source: [src/gem/schema/field_path/model.py:55](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/field_path/model.py#L55)

##### `to_str`

Signature: `def FieldPath.to_str(self) -> str`

Return a slash-separated string of active indices.

Source: [src/gem/schema/field_path/model.py:63](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/field_path/model.py#L63)

##### `plus_one`

Signature: `def FieldPath.plus_one(self) -> None`

Increment the deepest index by 1.

Source: [src/gem/schema/field_path/model.py:71](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/field_path/model.py#L71)

## `gem.schema.field_path.FieldPathOp`

### `FieldPathOp`

```python
class FieldPathOp
```

A single field-path operation with its Huffman weight.

Source: [src/gem/schema/field_path/ops.py:20](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/field_path/ops.py#L20)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `name` | `str` | `-` |
| `weight` | `int` | `-` |
| `fn` | `Callable[[BitReader, FieldPath], None]` | `-` |
