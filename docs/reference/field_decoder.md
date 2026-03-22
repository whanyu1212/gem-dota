# Field Decoders

Dispatches field types to concrete decoders, including quantized float handling and packed value decoding.

See also: [Field Decoders](../understanding/06_field_decoders.md)


---


---

## Generated API

## `gem.field_decoder.find_decoder`

### `find_decoder`

```python
def find_decoder(field: _FieldLike) -> FieldDecoder
```

Return the appropriate decoder for the given field.

Source: [src/gem/field_decoder.py:403](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/field_decoder.py#L403)

## `gem.field_decoder.find_decoder_by_base_type`

### `find_decoder_by_base_type`

```python
def find_decoder_by_base_type(base_type: str) -> FieldDecoder
```

Return a decoder for a base type string without field context.

Source: [src/gem/field_decoder.py:435](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/field_decoder.py#L435)

## `gem.field_decoder.QuantizedFloatDecoder`

### `QuantizedFloatDecoder`

```python
class QuantizedFloatDecoder
```

Decoder for Source 2 quantized floats (CNetworkedQuantizedFloat).

Source: [src/gem/field_decoder.py:66](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/field_decoder.py#L66)

#### Methods

##### `decode`

Signature: `def QuantizedFloatDecoder.decode(self, r: BitReader) -> float`

Read and decode one quantized float from r.

Source: [src/gem/field_decoder.py:180](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/field_decoder.py#L180)
