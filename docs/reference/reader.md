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

Source: [src/gem/binary/reader.py:25](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L25)

#### Methods

##### `read_bits`

Signature: `def BitReader.read_bits(self, n: int) -> int`

Read ``n`` bits in Source 2's LSB-first order.

Source: [src/gem/binary/reader.py:71](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L71)

##### `read_boolean`

Signature: `def BitReader.read_boolean(self) -> bool`

Read one bit and interpret it as a boolean.

Source: [src/gem/binary/reader.py:109](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L109)

##### `read_bytes`

Signature: `def BitReader.read_bytes(self, n: int) -> bytes`

Read exactly ``n`` logical bytes from the current position.

Source: [src/gem/binary/reader.py:154](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L154)

##### `read_bits_as_bytes`

Signature: `def BitReader.read_bits_as_bytes(self, n: int) -> bytes`

Read ``n`` bits and return them packed into bytes.

Source: [src/gem/binary/reader.py:233](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L233)

##### `read_le_uint32`

Signature: `def BitReader.read_le_uint32(self) -> int`

Read a little-endian unsigned 32-bit integer.

Source: [src/gem/binary/reader.py:266](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L266)

##### `read_le_uint64`

Signature: `def BitReader.read_le_uint64(self) -> int`

Read a little-endian unsigned 64-bit integer.

Source: [src/gem/binary/reader.py:274](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L274)

##### `read_varuint32`

Signature: `def BitReader.read_varuint32(self) -> int`

Read an unsigned 32-bit protobuf-style varint.

Source: [src/gem/binary/reader.py:286](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L286)

##### `read_varint32`

Signature: `def BitReader.read_varint32(self) -> int`

Read a signed 32-bit protobuf-style varint using zigzag decoding.

Source: [src/gem/binary/reader.py:312](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L312)

##### `read_varuint64`

Signature: `def BitReader.read_varuint64(self) -> int`

Read an unsigned 64-bit protobuf-style varint.

Source: [src/gem/binary/reader.py:328](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L328)

##### `read_varint64`

Signature: `def BitReader.read_varint64(self) -> int`

Read a signed 64-bit protobuf-style varint using zigzag decoding.

Source: [src/gem/binary/reader.py:351](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L351)

##### `read_ubit_var`

Signature: `def BitReader.read_ubit_var(self) -> int`

Read Source 2's ``UBitVar`` unsigned integer encoding.

Source: [src/gem/binary/reader.py:367](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L367)

##### `read_ubit_var_fp`

Signature: `def BitReader.read_ubit_var_fp(self) -> int`

Read Source 2's field-path variable-width integer encoding.

Source: [src/gem/binary/reader.py:391](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L391)

##### `read_float`

Signature: `def BitReader.read_float(self) -> float`

Read a little-endian IEEE 754 single-precision float.

Source: [src/gem/binary/reader.py:415](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L415)

##### `read_coord`

Signature: `def BitReader.read_coord(self) -> float`

Read a Source network coordinate.

Source: [src/gem/binary/reader.py:423](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L423)

##### `read_angle`

Signature: `def BitReader.read_angle(self, n: int) -> float`

Read an angle encoded in ``n`` bits, mapped to [0, 360) degrees.

Source: [src/gem/binary/reader.py:447](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L447)

##### `read_normal`

Signature: `def BitReader.read_normal(self) -> float`

Read a normalized float in the range [-1, 1].

Source: [src/gem/binary/reader.py:458](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L458)

##### `read_3bit_normal`

Signature: `def BitReader.read_3bit_normal(self) -> list[float]`

Read a compressed three-component unit normal vector.

Source: [src/gem/binary/reader.py:471](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L471)

##### `read_string`

Signature: `def BitReader.read_string(self) -> str`

Read a null-terminated UTF-8 string.

Source: [src/gem/binary/reader.py:499](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L499)

##### `peek_bits`

Signature: `def BitReader.peek_bits(self, n: int) -> int`

Return the next ``n`` bits without consuming logical bits.

Source: [src/gem/binary/reader.py:517](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L517)

##### `skip_bits`

Signature: `def BitReader.skip_bits(self, n: int) -> None`

Discard ``n`` bits that are already loaded in the bit cache.

Source: [src/gem/binary/reader.py:555](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L555)

##### `rem_bits`

Signature: `def BitReader.rem_bits(self) -> int`

Return the number of logical unread bits remaining.

Source: [src/gem/binary/reader.py:568](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L568)

##### `position`

Signature: `def BitReader.position(self) -> str`

Return a reader position string for debugging.

Source: [src/gem/binary/reader.py:576](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L576)
