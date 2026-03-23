# Stream Layer

This page explains `src/gem/stream.py` line by line.

`stream.py` is the outer container reader. It does **not** parse protobuf fields. It only turns replay bytes into normalized outer messages:

```python
(tick, msg_type, data)
```

Prerequisite: [Bits & Bytes Primer](../cookbook/bits-and-bytes-primer.md)

## What this layer owns

1. Validate Source 2 replay magic (`PBDEMS2\x00`).
2. Skip file metadata bytes after magic.
3. Decode outer message framing (`command`, `tick`, `size`, `payload`).
4. Strip compression flag from `command` to get `msg_type`.
5. Snappy-decompress payload if needed.
6. Yield one normalized outer message at a time.

## Constants explained

| Constant | Value | What it means in replay bytes | Intuition |
|---|---|---|---|
| `_MAGIC_S2` | `b"PBDEMS2\x00"` | First 8 bytes in every Source 2 replay. | File signature; mismatch means the file is not this format. |
| `_METADATA_SKIP` | `8` | Next 8 bytes after magic are metadata, not outer messages. | Advance cursor before parsing commands. |
| `_DEM_IS_COMPRESSED` | `64` (`0x40`) | Bit inside `command`; if set, payload is Snappy-compressed. | Same message type can appear compressed or uncompressed. |
| `_PREGAME_TICK` | `0xFFFFFFFF` | Special pregame sentinel tick. | Normalized to `0` so callers do not handle sentinel logic. |

Compression flag example:

```python
command = 0x47  # 0x40 (compressed bit) + 0x07 (DEM_Packet)
compressed = bool(command & 0x40)  # True
msg_type = command & ~0x40         # 0x07
```

### The first 16 bytes, precisely

`DemoStream` starts with this fixed header layout:

```text
offset 0..7   : magic bytes "PBDEMS2\x00"
offset 8..11  : metadata uint32 #1 (little-endian)
offset 12..15 : metadata uint32 #2 (little-endian)
offset 16..   : first outer message framing begins
```

Why we skip metadata bytes (`_METADATA_SKIP = 8`):

1. They are size-related engine metadata hints, not message payload.
2. Outer messages are already self-delimiting via `size` varuint.
3. In truncated copies these hints can remain from original file, so they are not a safe source of truth for parser flow.

## Data model

```python
@dataclass(frozen=True, slots=True)
class OuterMessage:
    tick: int
    msg_type: int
    data: bytes
```

Why this exists:

1. Gives a typed internal representation for one outer message.
2. Keeps parsing output explicit and stable.
3. `frozen=True` avoids accidental mutation.

## `DemoStream` lifecycle

### `__init__(source)`

What it does:

1. Accepts either `bytes` or `str | Path`.
2. If path: opens file read-only and memory-maps it.
3. Initializes cursor (`self._pos = 0`).
4. Validates magic header.
5. Skips 8 metadata bytes.

Why mmap is used:

- Large `.dem` files can be read lazily without copying entire content into heap memory first.

### `close()`, `__enter__()`, `__exit__()`

- `close()` releases mmap and file descriptor.
- Context manager methods allow safe usage:

```python
with DemoStream("match.dem") as stream:
    for tick, msg_type, data in stream:
        ...
```

## Header validation

Implementation intent:

```python
magic = self._buf[self._pos : self._pos + 8]
self._pos += 8
if magic != _MAGIC_S2:
    raise ValueError(...)
```

If magic mismatches, parsing stops immediately. This protects every downstream layer from invalid input.

## Varuint decoder (`_read_varuint32`)

`stream.py` decodes varuint directly in-place for speed:

```python
x = 0
s = 0
while True:
    b = self._buf[self._pos]
    self._pos += 1
    x |= (b & 0x7F) << s
    s += 7
    if (b & 0x80) == 0 or s == 35:
        break
```

Meaning:

1. Lower 7 bits carry value bits.
2. High bit (`0x80`) means “continue”.
3. Shift grows by 7 each byte.

This method is used for `command`, `tick`, and `size` fields in every outer message.

## Core parse step (`_read_message`)

Real flow in `stream.py`:

```python
command = self._read_varuint32()
msg_type = command & ~_DEM_IS_COMPRESSED
compressed = bool(command & _DEM_IS_COMPRESSED)

tick = self._read_varuint32()
if tick == _PREGAME_TICK:
    tick = 0

size = self._read_varuint32()
payload = self._buf[self._pos : self._pos + size]
self._pos += size

if compressed:
    payload = _snappy_decompress(payload)

return OuterMessage(tick=tick, msg_type=msg_type, data=payload)
```

Field by field:

1. `command`: packed bits containing both type and compression flag.
2. `msg_type`: pure outer command ID after removing flag bit.
3. `tick`: normalized from pregame sentinel if needed.
4. `size`: byte length of payload.
5. `payload`: sliced bytes, optionally decompressed.

## Iterator contract (`__iter__`)

- Calls `_read_message()` until it returns `None` (end of buffer).
- Yields tuple form `(tick, msg_type, data)` for parser consumption.

This is the exact boundary consumed by `ReplayParser.parse()` in `parser.py`.

## Snappy helper (`_snappy_decompress`)

Responsibilities:

1. Lazy-import `python-snappy`.
2. Raise actionable `ImportError` with install command if missing.
3. Return decompressed bytes.

This isolates compression handling from main parser logic.

## End-to-end example

```python
from gem.stream import DemoStream

with DemoStream("tests/fixtures/8520014563.dem") as stream:
    for i, (tick, msg_type, data) in enumerate(stream):
        print(i, tick, msg_type, len(data))
        if i >= 11:
            break
```

Output snapshot (truncated):

```text
(0, 0, 1, 189)
(1, 0, 8, 7)
(2, 0, 8, 12)
(3, 0, 8, 79453)
(4, 0, 8, 97031)
(5, 0, 8, 124)
(6, 0, 18, 112)
(7, 0, 18, 6)
(8, 0, 8, 10)
(9, 0, 4, 801384)
(10, 0, 5, 132881)
(11, 0, 6, 215430)
```

How to read each tuple:

1. message index in stream order,
2. tick,
3. outer message type ID (`EDemoCommands` numeric value),
4. payload byte length after decompression.

## What can break at this layer

1. Wrong magic -> immediate `ValueError`.
2. Missing `python-snappy` when compressed records exist -> `ImportError`.
3. Truncated/corrupt tail -> exception during varuint/payload/decompress read.

If these happen, fix stream/container correctness before debugging higher layers.

## Next page

- [Parser Layer (`parser.py`)](parser-layer.md)
