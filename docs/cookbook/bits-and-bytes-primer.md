# Bits & Bytes: A Crash Course for Python Programmers

Most Python code never looks below the level of `int`, `str`, and `bytes`. Replay
parsing does. A Dota 2 replay packs data as tightly as it can: a 2-bit command sits
right next to a 17-bit number, then a 1-bit flag, with no padding between them.
To read gem's low-level code (`binary/reader.py`, then `schema/`), you need a
handful of ideas that Python normally hides from you.

This page teaches them from scratch, one at a time. Each section has a small
snippet you can paste into a Python prompt, and a **Where gem uses this** note. The
examples use real bytes from match `8855242704`.

If you want to know how a replay is laid out (headers, envelopes, inner
messages), read [How Proto Parsing Works](proto-parsing-pipeline.md). This page
explains the tools used to read that layout.

## 1. Bits, bytes, binary, and hex

A **bit** is a single 0 or 1. A **byte** is 8 bits, so it holds a number from 0 to
255. Python's `bytes` is a sequence of those numbers:

```python
data = b"PBDEMS2\x00"   # the first 8 bytes of every Source 2 replay
print(list(data))       # [80, 66, 68, 69, 77, 83, 50, 0]
print(data.hex(" "))    # 50 42 44 45 4d 53 32 00
```

The same number can be written three ways:

| Notation | Python | 42 written that way |
|---|---|---|
| Decimal | `42` | `42` |
| Binary (base 2) | `0b101010` | `bin(42)` → `'0b101010'` |
| Hexadecimal (base 16) | `0x2a` | `hex(42)` → `'0x2a'` |

Hex is popular because **one hex digit is exactly 4 bits**, so a byte is always two
hex digits (`00` to `ff`). Reading bits off hex takes practice but no arithmetic:
`0xf0` is `1111 0000`, and `0x0f` is `0000 1111`.

```python
print(int("2a", 16))            # 42
print(int("101010", 2))         # 42
print(format(0xB7, "08b"))      # 10110111  (8 digits, zero-padded)
```

**Where gem uses this:** everywhere. Error messages, tests, and this documentation
show bytes in hex.

## 2. Bit operations: the six operators

Python has six operators that work on the individual bits of an integer:

| Operator | Name | What it does | Example |
|---|---|---|---|
| `a & b` | AND | 1 where **both** have a 1 | `0b1100 & 0b1010` → `0b1000` |
| `a \| b` | OR | 1 where **either** has a 1 | `0b1100 \| 0b1010` → `0b1110` |
| `a ^ b` | XOR | 1 where they **differ** | `0b1100 ^ 0b1010` → `0b0110` |
| `~a` | NOT | flips every bit | `~0b1100` → `-13` (see section 5) |
| `a << n` | left shift | moves bits up by `n`, adding zeros (× 2ⁿ) | `0b11 << 2` → `0b1100` |
| `a >> n` | right shift | moves bits down by `n`, dropping the lowest (÷ 2ⁿ) | `0b1100 >> 2` → `0b11` |

Combined, they do three jobs that come up constantly:

```python
x = 0b1011_0111          # 183; underscores are allowed in numbers

# Keep only the lowest n bits with a mask of n ones: (1 << n) - 1
print(bin(x & ((1 << 4) - 1)))    # 0b111     the low 4 bits (0111)

# Pull bits out of the middle: shift them down, then mask
print(bin((x >> 4) & 0b11))       # 0b11      bits 4 and 5

# Test, set, and clear a single flag bit
FLAG = 0x40
cmd = 0x47
print(bool(cmd & FLAG))   # True   is the flag set?
print(hex(cmd & ~FLAG))   # 0x7    clear it
print(hex(0x07 | FLAG))   # 0x47   set it
```

Bit positions are counted from the right, starting at 0. In `0b1011_0111`, bit 0 is
the rightmost `1` and bit 7 is the leftmost `1`.

**Where gem uses this:** the last three lines are exactly how
`binary/stream.py` reads each envelope's label. Bit 6 (`0x40`) of the command
means "compressed", and the rest is the envelope kind:
`compressed = command & 0x40` and `msg_type = command & ~0x40`.

## 3. Byte order: little-endian

A number bigger than 255 needs several bytes, so something has to decide which
byte comes first. Replays use **little-endian** order: the lowest byte first.

Bytes 8 to 11 of match `8855242704` are `e0 85 e7 11`. Read little-endian, that is
`0x11e785e0`:

```python
import struct

raw = bytes.fromhex("e0 85 e7 11")
print(int.from_bytes(raw, "little"))    # 300385760
print(struct.unpack("<I", raw)[0])      # 300385760   "<" little-endian, "I" uint32
print(int.from_bytes(raw, "big"))       # 3766871825  the same bytes read the wrong way
```

300,385,760 is the byte position of the match summary at the end of that 300 MB
file (see [Stage 1](proto-parsing-pipeline.md#stage-1-outer-framing-container-layer)).
Reading it in the wrong order gives a number that means nothing.

**Where gem uses this:** `struct.unpack("<I", ...)` in `binary/reader.py` loads
4 bytes at a time, and `read_float` decodes floats little-endian.

## 4. Bitstreams: reading bits that don't line up with bytes

Here is the part most Python programmers have never needed. Inside Valve's packed
formats, a value can start and end **in the middle of a byte**. A 6-bit number is
followed immediately by a 17-bit number, and so on. Reading these streams is the
job of `BitReader`.

Replays read the bits of each byte **least-significant bit first** (LSB-first): bit 0
of the first byte is the first bit in the stream, then bit 1, and so on, then bit 0
of the next byte. Picture each byte's bits laid out right to left, and the reader
taking them from the right:

```text
bytes:       0x0f        0xf0
bits:     0000 1111   1111 0000
          <-- read    <-- read    (right to left within each byte, first byte first)
```

```python
from gem.binary.reader import BitReader

r = BitReader(bytes([0b0000_1111, 0b1111_0000]))
print(bin(r.read_bits(4)))   # 0b1111      the low 4 bits of byte 0
print(bin(r.read_bits(8)))   # 0b0         the high 4 of byte 0, then the low 4 of byte 1
print(bin(r.read_bits(4)))   # 0b1111      the high 4 bits of byte 1
```

The middle read takes 4 bits from each byte. Nothing lines up with a byte
boundary, and that is normal in these streams.

Under the hood, `BitReader` keeps unread bits in an integer (its *bit cache*) and
uses the operators from section 2:

```python
cache = 0b1111_0000_0000_1111   # both bytes loaded, byte 0 lowest
n = 4
value = cache & ((1 << n) - 1)   # take the lowest n bits
cache >>= n                      # drop them
print(bin(value), bin(cache))    # 0b1111 0b111100000000
```

**Where gem uses this:** `BitReader.read_bits` in `binary/reader.py` is those two
lines plus refilling the cache 4 bytes at a time. Entity updates, string tables,
and the inner-message bundles are all read this way.

## 5. Signed numbers, and why Python needs masks

A fixed number of bits can only hold so many values, so computers store negative
numbers with a trick called **two's complement**: in 32 bits, the patterns from
`0x80000000` upward mean negative numbers, and `0xFFFFFFFF` means −1.

```python
def to_int32(u: int) -> int:
    """Interpret the low 32 bits of u as a signed number."""
    u &= 0xFFFFFFFF
    return u - (1 << 32) if u >= 1 << 31 else u

print(to_int32(0xFFFFFFFF))   # -1
print(to_int32(0x80000000))   # -2147483648   the smallest int32
print(hex(-1 & 0xFFFFFFFF))   # 0xffffffff    and back again
```

In C, Go, or Java, a 32-bit integer can't hold more than 32 bits. Extra high bits
simply fall off, which programmers call *wrapping*. **Python integers never
overflow**: they grow as large as needed. That is convenient, but it means Python
code that decodes 32-bit data has to throw away the extra bits itself with
`& 0xFFFFFFFF`. The same unbounded integers explain why `~0b1100` printed `-13` in
section 2: Python flips "all" the bits of a number with infinitely many leading
zeros, giving −(x + 1).

gem once missed one of these masks. A malformed 5-byte number could come out as
`0x7ffffffff`, a 35-bit value from a function that promised 32 bits. Valve's and
Manta's readers wrap it to `0xffffffff`, and now gem's does too.

**Zigzag encoding.** In two's complement, −1 is `0xFFFFFFFF`: a big number, and
therefore expensive to store with the variable-length integers in the next section.
Zigzag interleaves negatives with positives, so numbers close to zero stay small
whether they are positive or negative:

| Signed value | 0 | −1 | 1 | −2 | 2 | −3 |
|---|---|---|---|---|---|---|
| Zigzag-encoded | 0 | 1 | 2 | 3 | 4 | 5 |

```python
def zigzag_decode(n: int) -> int:
    return (n >> 1) ^ -(n & 1)

print([zigzag_decode(n) for n in range(6)])   # [0, -1, 1, -2, 2, -3]
```

**Where gem uses this:** `read_varint32` and `read_varint64` in `binary/reader.py`
decode zigzag, and `read_varuint32` masks to 32 bits.

## 6. Variable-length integers

Most numbers in a replay are small, so spending 4 bytes on every one would waste
space. Replays use two ways to make small numbers short.

### Varints: 7 bits per byte

A **varint** stores 7 bits of the number in each byte. The top bit of each byte
(`0x80`) means "another byte follows". The lowest 7 bits come first.

| Value | Bytes |
|---|---|
| 7 | `07` |
| 127 | `7f` |
| 128 | `80 01` |
| 300 | `ac 02` |

Here is a complete decoder:

```python
def read_varint(data: bytes) -> tuple[int, int]:
    """Return (value, bytes used)."""
    value = shift = 0
    for i, b in enumerate(data):
        value |= (b & 0x7F) << shift   # add this byte's 7 bits
        shift += 7
        if not b & 0x80:               # no continuation bit: done
            return value, i + 1
    raise ValueError("ran out of bytes")

print(read_varint(bytes.fromhex("ac 02")))   # (300, 2)
```

Real bytes: the first envelope in match `8855242704` starts right after the 16-byte
file header with `01 ff ff ff ff 0f cb 01`. Those are three varints in a row, the
envelope label from [Stage 1](proto-parsing-pipeline.md#stage-1-outer-framing-container-layer):

```python
label = bytes.fromhex("01 ff ff ff ff 0f cb 01")
command, used = read_varint(label)
tick, used2 = read_varint(label[used:])
size, _ = read_varint(label[used + used2:])
print(command, hex(tick), size)   # 1 0xffffffff 203
```

Command 1 is `DEM_FileHeader`. The tick `0xffffffff` is the special "before the
game" value, which gem stores as 0. And 203 bytes is the size of the file header.

**Protobuf uses the same varints.** The 203-byte payload starts
`0a 08 50 42 44 45 4d 53 32 00 10 30`. In protobuf, each field starts with a varint
*tag* equal to `field_number << 3 | wire_type`:

- `0a` = field 1, wire type 2 ("length-delimited"). Its length is `08`, then 8
  bytes follow: `PBDEMS2\0`, the `demo_file_stamp` field.
- `10` = field 2, wire type 0 ("varint"). The value is `30` = 48, the
  `patch_version` field.

```python
print(0x0A >> 3, 0x0A & 0b111)   # 1 2
print(0x10 >> 3, 0x10 & 0b111)   # 2 0
```

That is all a protobuf message is on the wire: tags and values. See
[What protobuf is](proto-parsing-pipeline.md#what-protobuf-is).

### ubit_var: Valve's own variable-width integer

Inside bitstreams, Valve uses a second format that works in **bits** rather than
bytes. `BitReader.read_ubit_var()` reads it. Read 6 bits first. The low 4 bits are
the start of the value, and the top 2 bits say how many more bits follow:

| Top 2 bits | Extra bits | Value |
|---|---|---|
| `00` | 0 | low 4 bits |
| `01` | 4 | low 4 bits + (4 extra bits << 4) |
| `10` | 8 | low 4 bits + (8 extra bits << 4) |
| `11` | 28 | low 4 bits + (28 extra bits << 4) |

Small numbers cost 6 bits, and large ones grow as needed. The first
`svc_PacketEntities` message in match `8855242704` has this type ID:

```text
first 6 bits:  01 0111   top "01" -> read 4 more bits; low 4 bits = 0111 = 7
next 4 bits:   0011      = 3
type_id = (3 << 4) | 7 = 55   -> svc_PacketEntities
```

**Where gem uses this:** varints are payload sizes, ticks, and many entity fields.
`ubit_var` is inner-message type IDs, entity index gaps, and string-table sizes.

## 7. Floats, and how to store them in fewer bits

A normal `float` in Python takes 64 bits. Replays use two cheaper ways to store
decimal numbers.

**32-bit floats.** Four bytes in the standard IEEE 754 format, about 7 significant
digits. Python can read them with `struct`, but prints them as its own 64-bit
floats, which shows the rounding:

```python
import struct

raw = struct.pack("<f", 0.1)            # store 0.1 as a 32-bit float
print(raw.hex(" "))                      # cd cc cc 3d
print(struct.unpack("<f", raw)[0])       # 0.10000000149011612
```

**Quantized floats.** When the schema knows a value's range, it can store the value
as a whole number of equal steps across that range, in exactly as many bits as it
needs:

```text
value = low + (high - low) × stored_number / (2^bits − 1)
```

A real example from the schema of match `8855242704`: `m_flMana` is stored in
**20 bits** over the range **0 to 65,536**. Each step is about 1/16 of a mana
point:

```python
bits, low, high = 20, 0.0, 65536.0
step = (high - low) / ((1 << bits) - 1)
print(round(step, 6))                   # 0.0625
print(low + (high - low) * 8000 / ((1 << bits) - 1))   # ≈ 500.0
```

So mana costs 20 bits instead of 32. Angles work the same way:
`BitReader.read_angle(n)` spreads `n` bits evenly over 0 to 360 degrees.

**Where gem uses this:** `read_float` and `read_angle` in `binary/reader.py`, and
`schema/field_decoder/quantized_float.py`, which also handles rounding flags and
special cases. That module has its own walkthrough.

## 8. Prefix codes: short codes for common things

Suppose you have to send a long list of instructions, and one instruction is far
more common than the rest. You can give it a very short code, and give rare ones
long codes. As long as **no code is the start of another code** (a *prefix code*),
the reader always knows where each code ends, with no separators needed.

A toy code:

| Instruction | Code |
|---|---|
| A (common) | `0` |
| B | `10` |
| C | `11` |

`0 10 11 0` can only mean A, B, C, A. Read bits until they match a code, output it,
and start again. **Huffman coding** is a standard method for choosing such codes
from how often each instruction appears.

**Where gem uses this:** `schema/field_path/` decodes the list of fields that changed
in each entity update. The instructions are 40 *field-path operations*. The most
common, "move to the next field" (`PlusOne`), is the single bit `0`. "Finished"
(`FieldPathEncodeFinish`) is `10`, and the rarest operations take 17 bits. That
module has its own walkthrough.

## 9. Decode it yourself

Now put the pieces together on real bytes. The first `DEM_Packet` in match
`8855242704` holds a bundle of inner messages. Each inner message starts with a
`ubit_var` type ID, then a varint size ([Stage 3](proto-parsing-pipeline.md#stage-3-inner-message-unpack-packet-multiplexing-layer)).
The bundle's first bytes are:

```text
88 b7 b4 81 02
```

Find the first inner message's type ID and size by hand before reading the answer.

<details>
<summary>Answer</summary>

**Type ID.** Read 6 bits, LSB-first, so the low 6 bits of `0x88`:

```text
0x88 = 1000 1000  ->  low 6 bits: 00 1000
top 2 bits "00": no extra bits.  type_id = 1000 = 8
```

Type 8 is `net_SpawnGroup_Load`, a map-chunk loading message.

**Size.** The varint starts at **bit 6** of the first byte, so every "byte" of it
straddles two real bytes: the top 2 bits of one byte, then the low 6 bits of the
next.

```python
data = bytes.fromhex("88 b7 b4 81 02")

def byte_at_bit_6(i):
    """The 8 bits starting at bit 6 of data[i]."""
    return (data[i] >> 6) | ((data[i + 1] & 0b11_1111) << 2)

groups = [byte_at_bit_6(i) for i in range(3)]
print([hex(g) for g in groups])   # ['0xde', '0xd2', '0x6']

size = (0xDE & 0x7F) | ((0xD2 & 0x7F) << 7) | ((0x06 & 0x7F) << 14)
print(size)                        # 108894
```

`0xde` and `0xd2` have the continuation bit set and `0x06` doesn't, so the varint
is three groups long: 94 + 82 × 128 + 6 × 16,384 = **108,894 bytes**.

`BitReader` agrees:

```python
from gem.binary.reader import BitReader

r = BitReader(bytes.fromhex("88 b7 b4 81 02"))
print(r.read_ubit_var(), r.read_varuint32(), r.position())   # 8 108894 3.6
```

`position()` says the payload starts at byte 3, bit 6. It isn't byte-aligned, which
is why `BitReader.read_bytes` needs a path for unaligned reads.

</details>

## Common pitfalls

1. **Forgetting to mask.** Python integers don't wrap. When you decode a
   fixed-width value, `& 0xFFFFFFFF` (or the width you need) is on you.
2. **`~x` is negative.** In Python, `~x == -(x + 1)`. To flip bits within a fixed
   width, use `x ^ 0xFF` (8 bits) or `~x & 0xFF`.
3. **Byte order.** Replays are little-endian. `int.from_bytes(b, "big")` gives
   plausible-looking nonsense.
4. **Bit order.** Bitstreams are read LSB-first. The first bit of `0x88` is its
   rightmost bit, not its leftmost.
5. **Assuming byte alignment.** After any bit-width read, the next byte may start
   in the middle of a real byte. Use `BitReader.read_bytes` rather than slicing the
   buffer yourself.
6. **Mixing hex and decimal.** `10` and `0x10` are different numbers. Hex dumps
   never show the `0x`.

## Next pages

1. [How Proto Parsing Works](proto-parsing-pipeline.md): how a replay is layered,
   using these tools.
2. [The Proto Files gem Uses](proto-files.md): the protobuf messages inside it.
3. `src/gem/binary/reader.py`: `BitReader`, which you can now read line by line.
