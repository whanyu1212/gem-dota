# The .dem Binary Format

A `.dem` file is a Dota 2 replay. It is a raw binary file — not JSON, not CSV, not anything
a text editor can interpret. This page explains the byte-level layout from the first byte
to the last.

---

## Why binary?

The game server records 30 frames of game state per second for a 40–60 minute match.
That is up to 108,000 snapshots per game. If each snapshot were JSON it would be several
gigabytes. As a compact binary file it is typically 200–300 MB.

---

## Top-level layout

```
┌────────────────────────────────────────────┐
│  Magic bytes  (8 bytes): "PBDEMS2\0"       │
├────────────────────────────────────────────┤
│  File metadata  (8 bytes): skip            │
├────────────────────────────────────────────┤
│  Outer message 1                           │
│  Outer message 2                           │
│  Outer message 3                           │
│  ...                                       │
│  Outer message N  (DEM_Stop)               │
└────────────────────────────────────────────┘
```

Total header: 16 bytes before the first message.

---

## Magic bytes

The first 8 bytes are always `PBDEMS2\0` (a null-terminated ASCII string).
This is the **magic number** — a fixed signature that identifies the file format.

```python
>>> open("my_replay.dem", "rb").read(8)
b'PBDEMS2\x00'
```

If a file does not start with these bytes, it is not a valid Source 2 replay.
Source 1 replays (pre-2013) start with `PUFDEMSM\0` instead. gem only supports Source 2.

---

## Each outer message

After the 16-byte header, the file is a flat sequence of **outer messages**:

```
┌──────────────────────────────────────────────────────────────┐
│  command    varuint32   message type ID, plus compressed flag │
│  tick       varuint32   game tick this message belongs to     │
│  size       varuint32   byte length of the payload            │
│  payload    [size bytes] the actual message data              │
└──────────────────────────────────────────────────────────────┘
```

All three header fields are varints (see [Protocol Buffers](01_protobuf.md) for varint
encoding). The total header overhead per message is typically 3–6 bytes.

### The command field

The command field encodes two things in one integer:

```python
msg_type   = command & ~0x40   # low bits: EDemoCommands enum value
compressed = bool(command & 0x40)  # bit 6: is payload Snappy-compressed?
```

`DEM_IsCompressed = 0x40`. If this bit is set, strip it to get the real type ID, then
decompress the payload with Snappy before parsing.

### Tick normalisation

Ticks before the game clock starts (draft, loading screen) are encoded as `0xFFFFFFFF`
in the file. gem normalises these to `0` automatically.

---

## Outer message types

These are the `EDemoCommands` values that matter for parsing:

| ID | Name | Count | Purpose |
|---|---|---|---|
| 0 | `DEM_Stop` | 1 | End of replay — stop iterating |
| 1 | `DEM_FileHeader` | 1 | Replay metadata: server, map, game mode |
| 2 | `DEM_FileInfo` | 1 | Match result, player list, duration |
| 3 | `DEM_SyncTick` | 1 | Sync point between signon and game |
| 4 | `DEM_SendTables` | 1 | Entity class schema — must parse first |
| 5 | `DEM_ClassInfo` | 1 | Maps class IDs → network names → serialisers |
| 6 | `DEM_StringTables` | 1 | Periodic full string table dump |
| 7 | `DEM_Packet` | ~49,000 | One game tick — all state updates |
| 8 | `DEM_SignonPacket` | ~10 | Initialisation packets before game starts |
| 13 | `DEM_FullPacket` | ~56 | Periodic full entity state snapshot |

In a 55-minute TI14 replay, `DEM_Packet` appears 49,591 times and accounts for nearly
the entire file.

---

## Inner messages: inside a DEM_Packet

`DEM_Packet`, `DEM_SignonPacket`, and `DEM_FullPacket` each contain a `CDemoPacket`
protobuf message. Its `.data` field is a **packed stream of inner net messages** —
multiple SVC/NET messages concatenated together.

Each inner message has its own type+size header:

```
inner message format:
  type_id    ubit_var     (variable-length bitfield integer)
  size       varuint32    byte count of the inner payload
  payload    [size bytes] protobuf payload for this inner type
```

The `ubit_var` type is Valve's own variable-bit-width integer. gem's `BitReader.read_ubit_var()`
implements it.

### Full nesting picture

```
DEM_Packet  (outer, varuint32 framing)
└── CDemoPacket  (protobuf)
    └── .data  (bytes)
        ├── inner msg: CSVCMsg_PacketEntities  (type 55)
        │   └── entity_data: bytes  ← raw bit-packed entity deltas
        ├── inner msg: CMsgSource1LegacyGameEvent  (type 45 or 46)
        │   └── eventid, keys
        ├── inner msg: CSVCMsg_CreateStringTable  (type 44)
        │   └── name, string_data
        └── inner msg: CNETMsg_Tick  (type 4)
            └── tick: uint32
```

---

## Key inner message type IDs

| ID | Name | Purpose |
|---|---|---|
| 4 | `net_Tick` | Current tick number |
| 40 | `svc_ServerInfo` | Map name, game build, max classes |
| 44 | `svc_CreateStringTable` | Create a new string table |
| 45 | `svc_UpdateStringTable` | Patch an existing string table |
| 55 | `svc_PacketEntities` | Entity deltas for this tick |

---

## Parsing order

gem processes messages in this order within each packet:

1. String table messages (`svc_CreateStringTable`, `svc_UpdateStringTable`) — priority -10
2. All other inner messages
3. `svc_PacketEntities` — priority +5 (last, so baselines are ready)

This ensures entity baselines from the `instancebaseline` string table are applied
before the entity delta stream tries to use them.

---

## Reading the outer stream

gem's `DemoStream` (`src/gem/stream.py`) abstracts the outer message loop:

```python
from gem.stream import DemoStream

with DemoStream("my_replay.dem") as stream:
    for tick, msg_type, data in stream:
        # tick:     int — game tick, normalised to 0 for pre-game
        # msg_type: int — EDemoCommands value (compressed flag already stripped)
        # data:     bytes — decompressed payload, ready for protobuf parsing
        pass
```

`DemoStream` memory-maps the file, normalises pre-game ticks, and handles
Snappy decompression transparently.

---

## Further reading

- [Snappy Compression](03_snappy.md) — when and how the compressed flag works
- [Send Tables & Schema](04_send_tables.md) — what `DEM_SendTables` contains
- [The Entity System](08_entity_system.md) — what is in `CSVCMsg_PacketEntities`
- [DemoStream API Reference](../reference/stream.md) — outer message iteration API
