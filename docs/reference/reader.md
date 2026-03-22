# BitReader

Low-level bit-stream primitives for reading LSB-first bits, varints, and Dota-specific coordinate/angle types.

See also: [The .dem Format](../understanding/02_dem_format.md)

---

## Generated API

## `gem.reader.BitReader`

### `BitReader`

```python
class BitReader
```

Reads bits and structured values from a byte buffer in LSB-first order.

Source: [src/gem/reader.py:19](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/reader.py#L19)

#### Methods

##### `read_bits`

Signature: `def BitReader.read_bits(self, n: int) -> int`

Read n bits from the buffer in LSB-first order.

Source: [src/gem/reader.py:64](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/reader.py#L64)

##### `read_boolean`

Signature: `def BitReader.read_boolean(self) -> bool`

Read a single bit as a boolean.

Source: [src/gem/reader.py:101](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/reader.py#L101)

##### `read_bytes`

Signature: `def BitReader.read_bytes(self, n: int) -> bytes`

Read exactly n bytes from the buffer.

Source: [src/gem/reader.py:135](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/reader.py#L135)

##### `read_bits_as_bytes`

Signature: `def BitReader.read_bits_as_bytes(self, n: int) -> bytes`

Read n bits, returning them packed into bytes.

Source: [src/gem/reader.py:164](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/reader.py#L164)

##### `read_le_uint32`

Signature: `def BitReader.read_le_uint32(self) -> int`

Read a little-endian unsigned 32-bit integer.

Source: [src/gem/reader.py:185](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/reader.py#L185)

##### `read_le_uint64`

Signature: `def BitReader.read_le_uint64(self) -> int`

Read a little-endian unsigned 64-bit integer.

Source: [src/gem/reader.py:193](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/reader.py#L193)

##### `read_varuint32`

Signature: `def BitReader.read_varuint32(self) -> int`

Read an unsigned 32-bit variable-length integer.

Source: [src/gem/reader.py:205](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/reader.py#L205)

##### `read_varint32`

Signature: `def BitReader.read_varint32(self) -> int`

Read a signed 32-bit variable-length integer using zigzag encoding.

Source: [src/gem/reader.py:228](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/reader.py#L228)

##### `read_varuint64`

Signature: `def BitReader.read_varuint64(self) -> int`

Read an unsigned 64-bit variable-length integer.

Source: [src/gem/reader.py:242](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/reader.py#L242)

##### `read_varint64`

Signature: `def BitReader.read_varint64(self) -> int`

Read a signed 64-bit variable-length integer using zigzag encoding.

Source: [src/gem/reader.py:264](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/reader.py#L264)

##### `read_ubit_var`

Signature: `def BitReader.read_ubit_var(self) -> int`

Read a variable-length uint32 using a 6-bit group with 2-bit size hint.

Source: [src/gem/reader.py:280](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/reader.py#L280)

##### `read_ubit_var_fp`

Signature: `def BitReader.read_ubit_var_fp(self) -> int`

Read a variable-length uint32 using field-path encoding.

Source: [src/gem/reader.py:303](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/reader.py#L303)

##### `read_float`

Signature: `def BitReader.read_float(self) -> float`

Read an IEEE 754 single-precision float (little-endian).

Source: [src/gem/reader.py:326](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/reader.py#L326)

##### `read_coord`

Signature: `def BitReader.read_coord(self) -> float`

Read a Source Engine network coordinate as a float.

Source: [src/gem/reader.py:334](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/reader.py#L334)

##### `read_angle`

Signature: `def BitReader.read_angle(self, n: int) -> float`

Read a bit-encoded angle of n bits, mapping to [0, 360) degrees.

Source: [src/gem/reader.py:357](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/reader.py#L357)

##### `read_normal`

Signature: `def BitReader.read_normal(self) -> float`

Read a normalised float in the range [-1, 1] using 12 bits.

Source: [src/gem/reader.py:368](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/reader.py#L368)

##### `read_3bit_normal`

Signature: `def BitReader.read_3bit_normal(self) -> list[float]`

Read a 3-component normal vector using compressed encoding.

Source: [src/gem/reader.py:381](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/reader.py#L381)

##### `read_string`

Signature: `def BitReader.read_string(self) -> str`

Read a null-terminated UTF-8 string.

Source: [src/gem/reader.py:408](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/reader.py#L408)

##### `read_string_n`

Signature: `def BitReader.read_string_n(self, n: int) -> str`

Read exactly n bytes and return them as a string.

Source: [src/gem/reader.py:422](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/reader.py#L422)

##### `peek_bits`

Signature: `def BitReader.peek_bits(self, n: int) -> int`

Read n bits without advancing the position.

Source: [src/gem/reader.py:437](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/reader.py#L437)

##### `skip_bits`

Signature: `def BitReader.skip_bits(self, n: int) -> None`

Discard n bits that have already been loaded into the bit buffer.

Source: [src/gem/reader.py:470](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/reader.py#L470)

##### `rem_bits`

Signature: `def BitReader.rem_bits(self) -> int`

Return the number of unread bits remaining in the buffer.

Source: [src/gem/reader.py:482](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/reader.py#L482)

##### `position`

Signature: `def BitReader.position(self) -> str`

Return a human-readable position string for debugging.

Source: [src/gem/reader.py:490](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/reader.py#L490)
