# Field State

Reads one entity update into an entity's value tree, and stores decoded field
values by field path.

See also: [How Entities Are Decoded, Part 4: Field State](../deep-dives/entity-field-state.md)
for an explanation with real examples.

---

## Generated API

## `gem.schema.field_reader.read_fields`

### `read_fields`

```python
def read_fields(r: BitReader, serializer: Serializer, state: FieldState) -> None
```

Read all field-path/value pairs from *r* into *state*.

Source: [src/gem/schema/field_reader.py:95](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/field_reader.py#L95)

## `gem.schema.field_state.FieldState`

### `FieldState`

```python
class FieldState
```

Nested mutable tree that stores decoded field values.

Source: [src/gem/schema/field_state.py:23](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/field_state.py#L23)

#### Methods

##### `get`

Signature: `def FieldState.get(self, fp: FieldPath) -> FieldValue`

Read the value at the given field path.

Source: [src/gem/schema/field_state.py:48](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/field_state.py#L48)

##### `set`

Signature: `def FieldState.set(self, fp: FieldPath, value: FieldValue) -> None`

Write a value at the given field path, growing the tree as needed.

Source: [src/gem/schema/field_state.py:95](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/field_state.py#L95)
