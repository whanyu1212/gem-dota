# Field Decoders

Dispatches field types to concrete decoders, including quantized float handling and packed value decoding.

See also: [How Proto Parsing Works](../cookbook/proto-parsing-pipeline.md)


---


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

Source: [src/gem/schema/field_decoder/type_resolver.py:156](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/field_decoder/type_resolver.py#L156)

## `gem.schema.field_decoder.QuantizedFloatDecoder`

### `QuantizedFloatDecoder`

```python
class QuantizedFloatDecoder
```

Decoder for Source 2 quantized floats (CNetworkedQuantizedFloat).

Source: [src/gem/schema/field_decoder/quantized_float.py:19](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/field_decoder/quantized_float.py#L19)

#### Methods

##### `decode`

Signature: `def QuantizedFloatDecoder.decode(self, r: BitReader) -> float`

Read and decode one quantized float from r.

Source: [src/gem/schema/field_decoder/quantized_float.py:131](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/schema/field_decoder/quantized_float.py#L131)
