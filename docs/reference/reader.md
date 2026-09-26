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

Source: [src/gem/binary/reader.py:264](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L264)

##### `read_le_uint64`

Signature: `def BitReader.read_le_uint64(self) -> int`

Read a little-endian unsigned 64-bit integer.

Source: [src/gem/binary/reader.py:272](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L272)

##### `read_varuint32`

Signature: `def BitReader.read_varuint32(self) -> int`

Read an unsigned 32-bit protobuf-style varint.

Source: [src/gem/binary/reader.py:284](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L284)

##### `read_varint32`

Signature: `def BitReader.read_varint32(self) -> int`

Read a signed 32-bit protobuf-style varint using zigzag decoding.

Source: [src/gem/binary/reader.py:310](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L310)

##### `read_varuint64`

Signature: `def BitReader.read_varuint64(self) -> int`

Read an unsigned 64-bit protobuf-style varint.

Source: [src/gem/binary/reader.py:326](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L326)

##### `read_varint64`

Signature: `def BitReader.read_varint64(self) -> int`

Read a signed 64-bit protobuf-style varint using zigzag decoding.

Source: [src/gem/binary/reader.py:348](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L348)

##### `read_ubit_var`

Signature: `def BitReader.read_ubit_var(self) -> int`

Read Source 2's ``UBitVar`` unsigned integer encoding.

Source: [src/gem/binary/reader.py:364](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L364)

##### `read_ubit_var_fp`

Signature: `def BitReader.read_ubit_var_fp(self) -> int`

Read Source 2's field-path variable-width integer encoding.

Source: [src/gem/binary/reader.py:388](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L388)

##### `read_float`

Signature: `def BitReader.read_float(self) -> float`

Read a little-endian IEEE 754 single-precision float.

Source: [src/gem/binary/reader.py:412](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L412)

##### `read_coord`

Signature: `def BitReader.read_coord(self) -> float`

Read a Source network coordinate.

Source: [src/gem/binary/reader.py:420](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L420)

##### `read_angle`

Signature: `def BitReader.read_angle(self, n: int) -> float`

Read an angle encoded in ``n`` bits, mapped to [0, 360) degrees.

Source: [src/gem/binary/reader.py:444](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L444)

##### `read_normal`

Signature: `def BitReader.read_normal(self) -> float`

Read a normalized float in the range [-1, 1].

Source: [src/gem/binary/reader.py:455](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L455)

##### `read_3bit_normal`

Signature: `def BitReader.read_3bit_normal(self) -> list[float]`

Read a compressed three-component unit normal vector.

Source: [src/gem/binary/reader.py:468](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L468)

##### `read_string`

Signature: `def BitReader.read_string(self) -> str`

Read a null-terminated UTF-8 string.

Source: [src/gem/binary/reader.py:496](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L496)

##### `peek_bits`

Signature: `def BitReader.peek_bits(self, n: int) -> int`

Return the next ``n`` bits without consuming logical bits.

Source: [src/gem/binary/reader.py:514](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L514)

##### `skip_bits`

Signature: `def BitReader.skip_bits(self, n: int) -> None`

Discard ``n`` bits that are already loaded in the bit cache.

Source: [src/gem/binary/reader.py:552](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L552)

##### `rem_bits`

Signature: `def BitReader.rem_bits(self) -> int`

Return the number of logical unread bits remaining.

Source: [src/gem/binary/reader.py:565](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L565)

##### `position`

Signature: `def BitReader.position(self) -> str`

Return a reader position string for debugging.

Source: [src/gem/binary/reader.py:573](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/binary/reader.py#L573)
