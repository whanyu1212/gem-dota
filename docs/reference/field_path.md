# Field Paths

Decodes Huffman-coded field path operations used to address properties inside entity deltas.

See also: [Field Paths & Huffman](../understanding/05_field_paths.md)


---


---

## Generated API

## `gem.field_path.read_field_paths`

### `read_field_paths`

```python
def read_field_paths(r: BitReader) -> list[FieldPath]
```

Decode a Huffman-coded sequence of field paths from r.

Source: [src/gem/field_path.py:493](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/field_path.py#L493)

## `gem.field_path.FieldPath`

### `FieldPath`

```python
class FieldPath
```

A mutable path of up to 7 integer field indices.

Source: [src/gem/field_path.py:29](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/field_path.py#L29)

#### Methods

##### `reset`

Signature: `def FieldPath.reset(self) -> None`

Reset to the initial empty state.

Source: [src/gem/field_path.py:48](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/field_path.py#L48)

##### `pop`

Signature: `def FieldPath.pop(self, n: int) -> None`

Pop n levels off the path, zeroing the vacated slots.

Source: [src/gem/field_path.py:54](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/field_path.py#L54)

##### `copy`

Signature: `def FieldPath.copy(self) -> FieldPath`

Return an independent copy of this path.

Source: [src/gem/field_path.py:64](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/field_path.py#L64)

##### `to_tuple`

Signature: `def FieldPath.to_tuple(self) -> tuple[int, ...]`

Return the active indices as an immutable tuple.

Source: [src/gem/field_path.py:76](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/field_path.py#L76)

##### `to_str`

Signature: `def FieldPath.to_str(self) -> str`

Return a slash-separated string of active indices.

Source: [src/gem/field_path.py:84](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/field_path.py#L84)

##### `plus_one`

Signature: `def FieldPath.plus_one(self) -> None`

Increment the deepest index by 1.

Source: [src/gem/field_path.py:92](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/field_path.py#L92)

## `gem.field_path.FieldPathOp`

### `FieldPathOp`

```python
class FieldPathOp
```

A single field-path operation with its Huffman weight.

Source: [src/gem/field_path.py:150](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/field_path.py#L150)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `name` | `str` | `-` |
| `weight` | `int` | `-` |
| `fn` | `Callable[[BitReader, FieldPath], None]` | `-` |
