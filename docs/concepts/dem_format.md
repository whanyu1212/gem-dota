# The .dem Format

A `.dem` file is a Dota 2 replay. It is a raw binary file — not JSON,
not CSV, not anything a text editor can read. This page explains exactly
how it's structured, from the first byte to the last.

---

## What is a binary file?

A text file stores data as human-readable characters. A binary file stores
data in whatever encoding is most compact and fast to parse. Replay files
use binary encoding because they need to record 30 frames of game state
per second for 40–60 minutes — that's up to 108,000 snapshots per game.
If each snapshot were JSON, a single replay would be several gigabytes.
As a binary file, it's typically 200–300 MB.

---

## The outer structure

Every `.dem` file has the same top-level layout:

```
┌─────────────────────────────────────────────┐
│  Magic bytes (8 bytes): "PBDEMS2\0"         │
├─────────────────────────────────────────────┤
│  File metadata (8 bytes): skip              │
├─────────────────────────────────────────────┤
│  Message 1                                  │
│  Message 2                                  │
│  Message 3                                  │
│  ...                                        │
│  Message N  (DEM_Stop)                      │
└─────────────────────────────────────────────┘
```

### Magic bytes

The first 8 bytes are always `PBDEMS2\0` (the `\0` is a null byte).
This is called a **magic number** — a fixed sequence that identifies the
file format. If a file doesn't start with these bytes, it's not a valid
Source 2 replay.

```python
>>> open("my_replay.dem", "rb").read(8)
b'PBDEMS2\x00'
```

Source 1 replays (older Dota 2 replays, pre-2013) start with `PUFDEMSM\0`
instead. gem only supports Source 2.

### Each message

After the header, the file is a flat sequence of **outer messages**. Each
message has this layout:

```
┌──────────────────────────────────────────────────────┐
│  command    varuint32   message type + compressed flag │
│  tick       varuint32   game tick this message belongs to │
│  size       varuint32   byte length of the payload    │
│  payload    [size bytes] the actual message data      │
└──────────────────────────────────────────────────────┘
```

---

## Variable-length integers (varints)

The `command`, `tick`, and `size` fields are all **varints** — integers
encoded in a variable number of bytes. This is a common trick in binary
protocols to avoid wasting space.

A fixed 32-bit integer always takes 4 bytes, even if the value is 1.
A varint uses as few bytes as needed:

| Value | Fixed (4 bytes) | Varint |
|---|---|---|
| 0 | `00 00 00 00` | `00` (1 byte) |
| 127 | `7F 00 00 00` | `7F` (1 byte) |
| 128 | `80 00 00 00` | `80 01` (2 bytes) |
| 300 | `2C 01 00 00` | `AC 02` (2 bytes) |
| 16384 | `00 40 00 00` | `80 80 01` (3 bytes) |

### How varint encoding works

Each byte contributes 7 bits of value. The **high bit** (bit 7) is a
continuation flag — if it's `1`, more bytes follow; if it's `0`, this
is the last byte.

```
Value 300 = 0b100101100

Split into 7-bit groups (LSB first):
  Group 0: 0101100  = 44  → more bytes follow → 44 | 0x80 = 0xAC
  Group 1: 0000010  =  2  → last byte         →  2          = 0x02

Encoded: AC 02
```

To decode:

```python
def read_varuint32(buf, pos):
    x, shift = 0, 0
    while True:
        b = buf[pos]; pos += 1
        x |= (b & 0x7F) << shift
        shift += 7
        if not (b & 0x80):
            break
    return x, pos
```

gem's `BitReader.read_varuint32()` does exactly this.

---

## Message types

The `command` field encodes two things packed into one integer:

```python
msg_type   = command & ~0x40   # low bits: the message type
compressed = command &  0x40   # bit 6: is the payload Snappy-compressed?
```

The message types are defined in the `EDemoCommands` protobuf enum.
The ones that matter for parsing:

| Type | Name | Frequency | Purpose |
|---|---|---|---|
| 1 | `DEM_FileHeader` | 1× | Replay metadata (map, server name) |
| 2 | `DEM_FileInfo` | 1× | Match result, player list, duration |
| 4 | `DEM_SendTables` | 1× | Entity class schema — the "dictionary" |
| 5 | `DEM_ClassInfo` | 1× | Maps class IDs to class names |
| 6 | `DEM_StringTables` | 1× | Periodic full string table dump |
| 7 | `DEM_Packet` | ~49,000× | One game tick — contains all state updates |
| 8 | `DEM_SignonPacket` | ~10× | Initialisation packets before game starts |
| 13 | `DEM_FullPacket` | ~56× | Periodic full entity state snapshot |
| 0 | `DEM_Stop` | 1× | End of replay |

In the TI14 Grand Finals Game 1 replay (55 minutes), `DEM_Packet` appears
49,591 times and accounts for 268 MB of the 266 MB file — almost everything
is tick data.

---

## Compression

When bit 6 of `command` is set, the payload is compressed with
[Snappy](https://google.github.io/snappy/) — a fast compression algorithm
optimised for speed over compression ratio. gem decompresses automatically:

```python
import snappy
payload = snappy.decompress(raw_bytes)
```

---

## Inside a DEM_Packet

Each `DEM_Packet` payload is itself a protobuf message (`CDemoPacket`)
containing a blob of **inner messages** — multiple SVC/NET messages
concatenated together. Each inner message has its own type+size header:

```
┌──────────────────────────────────────────────┐
│  DEM_Packet payload (one game tick)          │
│  ┌────────────────────────────────────────┐  │
│  │ inner msg: CSVCMsg_PacketEntities      │  │
│  ├────────────────────────────────────────┤  │
│  │ inner msg: CMsgSource1LegacyGameEvent  │  │
│  ├────────────────────────────────────────┤  │
│  │ inner msg: CNETMsg_Tick                │  │
│  └────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
```

Decoding these inner messages requires the protobuf schema — which is
what Phase 2 of gem handles.

---

## What gem gives you

After Phase 1, gem can read the entire outer structure of a replay:

```python
from gem.stream import DemoStream

with DemoStream("my_replay.dem") as stream:
    for tick, msg_type, data in stream:
        # tick:     game tick number (0 = pre-game)
        # msg_type: EDemoCommands integer
        # data:     raw decompressed payload bytes
        pass
```

The payload bytes are not yet decoded — that requires protobuf, which is
covered in the next concept page.

---

## Further reading

- [Manta source — parser.go](https://github.com/dotabuff/manta/blob/master/parser.go) — the Go implementation gem is translated from
- [Snappy compression](https://google.github.io/snappy/) — the compression format used for large packets
