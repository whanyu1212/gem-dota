# Protocol Buffers

Almost every payload in a `.dem` replay file is a **Protocol Buffers** (protobuf) message —
Google's binary serialisation format. You need to understand protobuf at a basic level to
follow the rest of this section.

---

## What protobuf is

Protobuf encodes structured data as a compact binary byte sequence. It is the binary
alternative to JSON: both describe the same data, but protobuf is significantly smaller
and faster to encode/decode.

The same player record, JSON versus protobuf:

```
{"name":"Cr1t","hero_id":74,"kills":12}   →   38 bytes  (JSON)
0a 04 43 72 31 74 10 4a 18 0c             →   10 bytes  (protobuf)
```

---

## Fields and tags

Every protobuf message is a sequence of **fields**. Each field is encoded as:

```
[tag varint] [value bytes]
```

The **tag** packs two things into one varint:

```
tag = (field_number << 3) | wire_type
```

The **field number** identifies which field this is (defined in the `.proto` schema).
The **wire type** controls how to read the bytes that follow.

### Wire types

| Wire type | Integer | Used for |
|---|---|---|
| Varint | 0 | `int32`, `int64`, `uint32`, `bool`, `enum` |
| 64-bit | 1 | `fixed64`, `double` |
| Length-delimited | 2 | `string`, `bytes`, nested messages, repeated fields |
| 32-bit | 5 | `fixed32`, `float` |

Wire types 3 and 4 (start/end group) are deprecated and not used by Valve.

---

## Varint encoding

Varints are variable-length integers: small values use 1 byte, larger values use more.
Each byte contributes 7 bits of value. The **most significant bit** (bit 7) is a
continuation flag: `1` means more bytes follow, `0` means this is the last byte.

Encoding the value 300:

```
300 in binary = 0b100101100

Split into 7-bit groups, LSB first:
  Group 0: 0101100 = 44  → more bytes follow → 44 | 0x80 = 0xAC
  Group 1: 0000010 =  2  → last byte         →  2          = 0x02

Encoded: AC 02
```

Decoding:

```python
def read_varuint32(data: bytes, pos: int) -> tuple[int, int]:
    x, shift = 0, 0
    while True:
        b = data[pos]; pos += 1
        x |= (b & 0x7F) << shift
        shift += 7
        if not (b & 0x80):
            break
    return x, pos
```

---

## Zigzag encoding for signed integers

`int32` and `int64` use zigzag encoding to keep small negative numbers small. Without
zigzag, `-1` would encode as 10 bytes (a 64-bit two's complement value). With zigzag:

```
0  → 0
-1 → 1
1  → 2
-2 → 3
2  → 4
...

zigzag_encode(n) = (n << 1) ^ (n >> 31)
zigzag_decode(z) = (z >> 1) ^ -(z & 1)
```

---

## Encoding example: a string field

```protobuf
message Player {
  string name = 1;    // field number 1
}
```

Encoding `name = "Cr1t"`:

```
tag:   (1 << 3) | 2 = 0x0A   (field 1, wire type 2 = length-delimited)
size:  4            = 0x04
data:  "Cr1t"       = 43 72 31 74

Full bytes: 0A 04 43 72 31 74
```

## Encoding example: integer fields

```protobuf
message Player {
  int32 hero_id = 2;
  int32 kills   = 3;
}
```

Encoding `hero_id = 74, kills = 12`:

```
hero_id: tag = (2 << 3) | 0 = 0x10,  value = varint(74) = 0x4A
kills:   tag = (3 << 3) | 0 = 0x18,  value = varint(12) = 0x0C

Full bytes: 10 4A 18 0C
```

---

## Nested messages

Protobuf fields can themselves be protobuf messages — the inner message is encoded as a
`length-delimited` field (wire type 2). This nesting is how the `.dem` format stacks
multiple layers:

```
CDemoPacket (outer message payload)
└── data: bytes (wire type 2)
    └── packed stream of inner messages:
        ├── CSVCMsg_PacketEntities
        │   └── entity_data: bytes  ← raw bit-packed entity deltas (not protobuf)
        ├── CMsgSource1LegacyGameEvent
        │   ├── eventid: int32
        │   └── keys: repeated KeyT
        └── CNETMsg_Tick
            └── tick: uint32
```

Each nested layer is decoded by calling `ParseFromString()` on the inner bytes.

---

## The schema: .proto files

To decode a protobuf message you need the **schema** — a `.proto` file that defines
which field number maps to which name and type. Without it, you can read raw tags and
values but cannot interpret them.

Valve publishes the `.proto` files used by Dota 2. gem bundles pre-compiled Python
classes generated from those files in `src/gem/proto/dota2/`. Usage:

```python
from gem.proto.dota2 import demo_pb2

msg = demo_pb2.CDemoFileInfo()
msg.ParseFromString(raw_bytes)
print(msg.playback_time)            # float: replay duration in seconds
print(msg.game_info.dota.match_id)  # int: the match ID
```

Key message classes used throughout gem:

| Module | Key messages |
|---|---|
| `demo_pb2` | `CDemoSendTables`, `CDemoClassInfo`, `CDemoFullPacket` |
| `netmessages_pb2` | `CSVCMsg_PacketEntities`, `CSVCMsg_CreateStringTable`, `CSVCMsg_FlattenedSerializer` |
| `dota_commonmessages_pb2` | `CMsgDOTACombatLogEntry` |
| `dota_usermessages_pb2` | `CDOTAUserMsg_*` |

---

## Why entity data is not protobuf

The `entity_data` field inside `CSVCMsg_PacketEntities` is **not** a protobuf message.
It is a raw bit-packed binary blob using Valve's custom encoding: varints, Huffman codes,
quantized floats, and bitfield arrays. Protobuf cannot express a format this compact.

That is why gem has a `BitReader` (`src/gem/reader.py`) — to decode these inner blobs
after protobuf has peeled away the outer layers.

```
Replay file
  └── DEM_Packet (outer framing)
        └── CDemoPacket (protobuf)
              └── CSVCMsg_PacketEntities (protobuf)
                    └── entity_data (raw bits — BitReader handles this)
```

---

## The send tables bootstrap problem

To decode entity data, gem needs the schema for each entity class — which fields it has,
what types they are, how they are encoded. But that schema is itself encoded in a protobuf
message (`CDemoSendTables` → `CSVCMsg_FlattenedSerializer`).

The replay solves this chicken-and-egg problem by sending `DEM_SendTables` exactly once,
near the start of the file, before any entity data arrives. gem reads it first, builds an
internal field-decoder map, then uses that map for every entity update in the rest of the
replay. See [Send Tables & Schema](04_send_tables.md) for the full breakdown.

---

## Further reading

- [Protocol Buffers documentation](https://protobuf.dev/)
- [Proto encoding guide](https://protobuf.dev/programming-guides/encoding/) — wire format detail
- Dota 2 proto files ship with the game client at `game/dota/pak01_dir.vpk`
