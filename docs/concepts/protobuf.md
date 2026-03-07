# Protocol Buffers

Every payload inside a `.dem` file is encoded with **Protocol Buffers**
(protobuf) — Google's binary serialisation format. This page explains
what protobuf is, why Valve uses it, and how gem decodes it.

---

## What is serialisation?

When you have a Python object like this:

```python
player = {"name": "Cr1t", "hero_id": 74, "kills": 12}
```

You need to convert it to bytes before you can write it to disk or send
it over a network. This conversion is called **serialisation**.

JSON is one serialisation format — human-readable, but verbose:

```
{"name":"Cr1t","hero_id":74,"kills":12}   →   38 bytes
```

Protobuf is another — binary, compact, and fast:

```
0a 04 43 72 31 74 10 4a 18 0c               →   10 bytes
```

The same data, 3.8× smaller, and much faster to encode/decode.

---

## How protobuf encodes data

Every protobuf message is a sequence of **fields**. Each field has:

- A **field number** (integer, defined in a `.proto` schema file)
- A **wire type** (how the bytes are encoded)
- A **value**

The field number and wire type are packed into a single varint tag:

```
tag = (field_number << 3) | wire_type
```

### Wire types

| Wire type | Value | Used for |
|---|---|---|
| Varint | 0 | int32, int64, bool, enum |
| 64-bit | 1 | fixed64, double |
| Length-delimited | 2 | string, bytes, nested messages |
| 32-bit | 5 | fixed32, float |

### Example: encoding a string field

Schema:

```protobuf
message Player {
  string name = 1;    // field 1
}
```

Encoding `name = "Cr1t"`:

```
tag:   field 1, wire type 2 (length-delimited)
       = (1 << 3) | 2 = 0x0A
size:  4 bytes  → 0x04
data:  "Cr1t"  → 43 72 31 74

Full encoding: 0A 04 43 72 31 74
```

### Example: encoding an integer field

```protobuf
message Player {
  int32 hero_id = 2;   // field 2
  int32 kills   = 3;   // field 3
}
```

Encoding `hero_id = 74, kills = 12`:

```
hero_id: tag = (2 << 3) | 0 = 0x10,  value = varint(74) = 0x4A
kills:   tag = (3 << 3) | 0 = 0x18,  value = varint(12) = 0x0C

Full encoding: 10 4A 18 0C
```

---

## The schema (.proto files)

To decode a protobuf message, you need the **schema** — a `.proto` file
that tells you what field number maps to what name and type. Without it,
you can still parse the bytes (you can read tags, sizes, and raw values)
but you won't know what `field 47` means.

Valve ships `.proto` files with the Dota 2 game client. gem bundles
pre-compiled Python classes generated from those files in
`src/gem/proto/dota2/`. For example:

```python
from gem.proto.dota2 import demo_pb2

msg = demo_pb2.CDemoFileInfo()
msg.ParseFromString(raw_bytes)

print(msg.playback_time)   # float: replay duration in seconds
print(msg.game_info.dota.match_id)   # int: the match ID
```

You never write the parsing logic yourself — the generated classes handle
it. You just call `.ParseFromString(bytes)`.

---

## Nested messages and the replay pipeline

Protobuf messages can be nested — a field of type `message` contains
another encoded message. This is how the replay's inner packet structure
works:

```
CDemoPacket (outer message payload)
└── data: bytes
    └── [repeated inner messages, each with type+size header]
        ├── CSVCMsg_PacketEntities
        │   └── entity_data: bytes  (bit-packed entity deltas)
        ├── CMsgSource1LegacyGameEvent
        │   └── eventid: int32
        │   └── keys: repeated KeyT
        └── CNETMsg_Tick
            └── tick: uint32
```

Each layer is decoded with `ParseFromString`, drilling deeper until you
reach primitive values.

---

## Why the entity data isn't protobuf

Here's the interesting part: the `entity_data` field inside
`CSVCMsg_PacketEntities` is **not** a protobuf message. It's a raw
bit-packed binary blob that uses Valve's own custom encoding — varints,
Huffman codes, quantized floats, and bitfield arrays. Protobuf can't
express a format this compact.

That's why gem has its own `BitReader` — to decode these inner blobs
after protobuf has peeled away the outer layers.

```
Replay file
  └── DEM_Packet (outer message, Snappy-compressed)
        └── CDemoPacket (protobuf)
              └── CSVCMsg_PacketEntities (protobuf)
                    └── entity_data (raw bits ← BitReader handles this)
```

---

## The send tables problem

There's a chicken-and-egg problem: to decode entity data, you need to
know the schema for each entity class (which fields it has, what types
they are, how they're encoded). But that schema is itself encoded in a
protobuf message (`CDemoSendTables` → `CSVCMsg_FlattenedSerializer`).

The replay solves this by sending `DEM_SendTables` exactly once, near the
start of the file, before any entity data arrives. gem reads and parses it
first, builds an internal field-decoder map, then uses that map for every
entity update that follows.

This is Phase 2 of gem's implementation.

---

## Protobuf in practice

You'll rarely interact with raw protobuf in gem — the library handles
decoding internally. But when you do, the pattern is always:

```python
from gem.proto.dota2 import netmessages_pb2

msg = netmessages_pb2.CSVCMsg_CreateStringTable()
msg.ParseFromString(data)

print(msg.name)              # e.g. "instancebaseline"
print(msg.num_entries)       # number of entries in the table
print(len(msg.string_data))  # raw data bytes
```

---

## Further reading

- [Protocol Buffers documentation](https://protobuf.dev/) — the official Google docs
- [proto encoding guide](https://protobuf.dev/programming-guides/encoding/) — detailed wire format explanation
- Dota 2 proto files ship with the game client at `game/dota/pak01_dir.vpk`
