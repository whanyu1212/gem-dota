# BitReader

Low-level bit-stream primitives for reading LSB-first bits, varints, and Dota-specific coordinate/angle types.

See also: [How Proto Parsing Works](../cookbook/proto-parsing-pipeline.md)

---

## Generated API

## `gem.binary.reader.BitReader`

### `BitReader`

```python
class BitReader
```

Stateful reader for Source 2's LSB-first binary encodings.

Source: [src/gem/binary/reader.py:23](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L23)

#### Methods

##### `read_bits`

Signature: `def BitReader.read_bits(self, n: int) -> int`

Read ``n`` bits in Source 2's LSB-first order.

Source: [src/gem/binary/reader.py:69](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L69)

##### `read_boolean`

Signature: `def BitReader.read_boolean(self) -> bool`

Read one bit and interpret it as a boolean.

Source: [src/gem/binary/reader.py:107](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L107)

##### `read_bytes`

Signature: `def BitReader.read_bytes(self, n: int) -> bytes`

Read exactly ``n`` logical bytes from the current position.

Source: [src/gem/binary/reader.py:152](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L152)

##### `read_bits_as_bytes`

Signature: `def BitReader.read_bits_as_bytes(self, n: int) -> bytes`

Read ``n`` bits and return them packed into bytes.

Source: [src/gem/binary/reader.py:231](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L231)

##### `read_le_uint32`

Signature: `def BitReader.read_le_uint32(self) -> int`

Read a little-endian unsigned 32-bit integer.

Source: [src/gem/binary/reader.py:255](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L255)

##### `read_le_uint64`

Signature: `def BitReader.read_le_uint64(self) -> int`

Read a little-endian unsigned 64-bit integer.

Source: [src/gem/binary/reader.py:263](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L263)

##### `read_varuint32`

Signature: `def BitReader.read_varuint32(self) -> int`

Read an unsigned 32-bit protobuf-style varint.

Source: [src/gem/binary/reader.py:275](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L275)

##### `read_varint32`

Signature: `def BitReader.read_varint32(self) -> int`

Read a signed 32-bit protobuf-style varint using zigzag decoding.

Source: [src/gem/binary/reader.py:298](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L298)

##### `read_varuint64`

Signature: `def BitReader.read_varuint64(self) -> int`

Read an unsigned 64-bit protobuf-style varint.

Source: [src/gem/binary/reader.py:313](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L313)

##### `read_varint64`

Signature: `def BitReader.read_varint64(self) -> int`

Read a signed 64-bit protobuf-style varint using zigzag decoding.

Source: [src/gem/binary/reader.py:335](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L335)

##### `read_ubit_var`

Signature: `def BitReader.read_ubit_var(self) -> int`

Read Source 2's ``UBitVar`` unsigned integer encoding.

Source: [src/gem/binary/reader.py:351](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L351)

##### `read_ubit_var_fp`

Signature: `def BitReader.read_ubit_var_fp(self) -> int`

Read Source 2's field-path variable-width integer encoding.

Source: [src/gem/binary/reader.py:375](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L375)

##### `read_float`

Signature: `def BitReader.read_float(self) -> float`

Read a little-endian IEEE 754 single-precision float.

Source: [src/gem/binary/reader.py:399](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L399)

##### `read_coord`

Signature: `def BitReader.read_coord(self) -> float`

Read a Source network coordinate.

Source: [src/gem/binary/reader.py:407](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L407)

##### `read_angle`

Signature: `def BitReader.read_angle(self, n: int) -> float`

Read an angle encoded in ``n`` bits, mapped to [0, 360) degrees.

Source: [src/gem/binary/reader.py:431](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L431)

##### `read_normal`

Signature: `def BitReader.read_normal(self) -> float`

Read a normalized float in the range [-1, 1].

Source: [src/gem/binary/reader.py:442](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L442)

##### `read_3bit_normal`

Signature: `def BitReader.read_3bit_normal(self) -> list[float]`

Read a compressed three-component unit normal vector.

Source: [src/gem/binary/reader.py:455](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L455)

##### `read_string`

Signature: `def BitReader.read_string(self) -> str`

Read a null-terminated UTF-8 string.

Source: [src/gem/binary/reader.py:483](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L483)

##### `read_string_n`

Signature: `def BitReader.read_string_n(self, n: int) -> str`

Read exactly ``n`` bytes and return them as a Latin-1 string.

Source: [src/gem/binary/reader.py:497](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L497)

##### `peek_bits`

Signature: `def BitReader.peek_bits(self, n: int) -> int`

Return the next ``n`` bits without consuming logical bits.

Source: [src/gem/binary/reader.py:512](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L512)

##### `skip_bits`

Signature: `def BitReader.skip_bits(self, n: int) -> None`

Discard ``n`` bits that are already loaded in the bit cache.

Source: [src/gem/binary/reader.py:546](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L546)

##### `rem_bits`

Signature: `def BitReader.rem_bits(self) -> int`

Return the number of logical unread bits remaining.

Source: [src/gem/binary/reader.py:559](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L559)

##### `position`

Signature: `def BitReader.position(self) -> str`

Return a reader position string for debugging.

Source: [src/gem/binary/reader.py:567](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L567)
