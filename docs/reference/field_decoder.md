# Field Decoders

Dispatches field types to concrete decoders, including quantized float handling and packed value decoding.

See also: [How Entities Are Decoded, Part 3: Field Decoders](../deep-dives/entity-field-decoders.md)
for an explanation with real values, and
[How Proto Parsing Works](../cookbook/proto-parsing-pipeline.md).

---

## Generated API

## `gem.schema.field_decoder.find_decoder`

### `find_decoder`

```python
def find_decoder(field: _FieldLike) -> FieldDecoder
```

Return the appropriate decoder for the given field.

Source: [src/gem/schema/field_decoder/type_resolver.py:124](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/field_decoder/type_resolver.py#L124)

## `gem.schema.field_decoder.find_decoder_by_base_type`

### `find_decoder_by_base_type`

```python
def find_decoder_by_base_type(base_type: str) -> FieldDecoder
```

Return a decoder for a base type string without field context.

Source: [src/gem/schema/field_decoder/type_resolver.py:155](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/field_decoder/type_resolver.py#L155)

## `gem.schema.field_decoder.QuantizedFloatDecoder`

### `QuantizedFloatDecoder`

```python
class QuantizedFloatDecoder
```

Decoder for Source 2 quantized floats (CNetworkedQuantizedFloat).

Source: [src/gem/schema/field_decoder/quantized_float.py:98](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/field_decoder/quantized_float.py#L98)

#### Methods

##### `decode`

Signature: `def QuantizedFloatDecoder.decode(self, r: BitReader) -> float`

Read and decode one quantized float from r.

Source: [src/gem/schema/field_decoder/quantized_float.py:213](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/field_decoder/quantized_float.py#L213)
