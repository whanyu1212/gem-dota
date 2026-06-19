# gem.binary

`gem.binary` is the lowest-level reading layer in the replay parser. It turns
raw Source 2 `.dem` bytes into well-bounded byte slices that the rest of `gem`
can parse as protobuf messages, and it provides the bit-level primitives needed
for Valve's custom packed streams inside those protobuf messages.

This package is intentionally small:

- `stream.py` reads the outer `.dem` message stream.
- `reader.py` reads bits, bytes, varints, packed values, and Source 2-specific
  integer encodings.
- `__init__.py` re-exports the small public surface: `DemoStream`,
  `OuterMessage`, `BitReader`, and `BufferReadError`.

It is not the generated protobuf layer. The generated protobuf classes live in
`gem.proto`. This package exists because replay files are not stored as one
plain protobuf document; they are a binary container with nested protobuf
payloads and several protobuf fields that contain additional bit-packed data.

## Mental Model

Think of replay parsing as a set of nested containers:

```text
.dem file
  -> outer demo messages
       -> protobuf payloads such as CDemoPacket, CDemoFileInfo, CDemoSendTables
            -> sometimes nested packed byte streams
                 -> inner net messages or entity/string-table bitstreams
                      -> more protobuf payloads or schema-driven field values
```

`gem.binary` owns the parts where the parser must know how to move through raw
bytes and bits. Once a complete protobuf payload has been isolated, the parser
usually hands it to a generated protobuf class with `ParseFromString`.

## Outer Replay Stream

`DemoStream` in `stream.py` reads the top-level Source 2 replay container.

At the start of a supported replay, the stream expects:

```text
8 bytes  magic: PBDEMS2\0
8 bytes  file-size metadata, currently skipped
```

After that, the file is a sequence of outer demo messages:

```text
varuint32 command
varuint32 tick
varuint32 payload_size
bytes     payload
```

`command` contains both the message type and a compression flag:

```text
msg_type   = command & ~0x40
compressed = command & 0x40
```

If the compression flag is set, `DemoStream` Snappy-decompresses the payload
before yielding it. It also normalizes the Source 2 pre-game tick value
`0xffffffff` to `0`.

The iterator yields:

```python
for tick, msg_type, data in DemoStream(path):
    ...
```

At this point, `data` is the raw, decompressed payload for one outer demo
message. For most outer message types, `parser.py` immediately parses it with a
generated protobuf class:

```python
pkt_msg = CDemoPacket()
pkt_msg.ParseFromString(data)
```

That handoff is the main boundary between `gem.binary.stream` and the protobuf
layer.

## Inner Packet Streams

Some outer protobuf messages contain another packed stream. The most important
example is `CDemoPacket.data`, used by `DEM_Packet`,
`DEM_SignonPacket`, and `DEM_FullPacket`.

The inner stream is not itself a protobuf message. It is a sequence of:

```text
ubit_var  type_id
varuint32 payload_size
bytes     payload
```

`parser.py` uses `BitReader` to unpack that sequence:

```python
r = BitReader(data)
while r.rem_bits() >= 8:
    type_id = r.read_ubit_var()
    size = r.read_varuint32()
    payload = r.read_bytes(size)
```

Only after this step can the parser choose the correct generated protobuf class
for each inner message type:

```python
if type_id == SVC_SERVER_INFO:
    msg = CSVCMsg_ServerInfo()
    msg.ParseFromString(payload)
```

This is why `BitReader` is necessary even though the project already has
generated protobuf modules.

## BitReader

`BitReader` in `reader.py` is a small stateful reader over a `bytes` buffer. It
tracks:

- the current byte position
- a local bit buffer
- how many unread bits remain in that bit buffer

Source 2 network data is read least-significant-bit first. That means reading
one bit from `b"\x01"` returns `1`, and reading several bits consumes the low
bits before the high bits. `BitReader` preserves that behavior across byte
boundaries.

The reader supports several groups of operations.

### Plain Bits And Bytes

Use these when the replay format specifies an exact bit or byte width:

```python
r.read_bits(2)       # command flags, field path fragments, compact counters
r.read_boolean()     # single-bit flags
r.read_bytes(size)   # byte payloads, usually protobuf payloads
r.read_bits_as_bytes(bit_count)
```

`read_bytes` is performance-sensitive because it extracts protobuf payloads
from inner message streams. Those payloads often start at a bit offset rather
than on a clean byte boundary, because the preceding `type_id` and `size`
fields are variable-width encodings.

The implementation keeps three paths:

- byte-aligned reads use a direct slice from the backing buffer;
- large unaligned reads bulk-compose logical bytes from the bit cache and the
  backing buffer;
- very small unaligned reads use the original byte-by-byte bit path.

That original path remains available internally as `_read_bytes_slow`. It is
not a compatibility API; it exists so tests and profiling can compare the fast
path against the simple reference implementation.

The parity contract is:

```text
fast read_bytes(data, offset, n)
  == slow byte-by-byte read_bits(8) loop
```

The tests check this across offsets, sizes, data patterns, reader position,
remaining-bit counts, and the entire remaining bitstream after the read. Parser
tests also decode the same synthetic inner-message blob once through the fast
path and once with `read_bytes` monkeypatched to `_read_bytes_slow`.

### Protobuf-Style Varints

Use these when the replay format stores integers with continuation bytes:

```python
r.read_varuint32()
r.read_varint32()
r.read_varuint64()
r.read_varint64()
```

The unsigned form uses the usual 7-bit continuation-byte scheme. The signed
form uses zigzag decoding.

These methods are useful both around protobuf payloads and inside Valve's
custom packed sections. For example, outer message sizes and inner payload
sizes are varuint32 values.

### Source 2 Packed Integers

Source 2 also uses custom variable-width integer encodings:

```python
r.read_ubit_var()
r.read_ubit_var_fp()
```

`read_ubit_var` reads an integer whose first 6 bits include a 2-bit size hint.
It is used for inner message type IDs and entity index deltas.

`read_ubit_var_fp` is used by field-path decoding. Field paths identify which
entity fields changed in an incremental entity update.

### Source Network Value Types

The reader also includes helpers for values used by schema-driven entity field
decoders:

```python
r.read_float()
r.read_coord()
r.read_angle(bits)
r.read_normal()
r.read_3bit_normal()
r.read_string()
r.read_string_n(size)
```

These are not generic Python serialization helpers. They match Source network
encodings used in replay payloads.

## How This Package Fits With Protobuf Parsing

The relationship between `gem.binary` and protobuf parsing is cooperative:

1. `DemoStream` extracts one outer replay payload.
2. `parser.py` selects the generated protobuf class for that outer message.
3. If a parsed protobuf contains a packed byte field, `BitReader` decodes that
   nested stream.
4. The resulting payload bytes are handed back to generated protobuf classes or
   to schema-driven entity decoders.

Important examples:

- `DEM_FileInfo` payloads are parsed directly as `CDemoFileInfo`.
- `DEM_Packet` payloads are parsed as `CDemoPacket`, then `CDemoPacket.data` is
  unpacked with `BitReader` into inner net messages.
- `svc_ServerInfo`, `svc_CreateStringTable`, and `svc_PacketEntities` inner
  payloads are parsed with generated protobuf classes.
- `CSVCMsg_PacketEntities.entity_data` is then decoded with `BitReader` because
  the entity deltas inside it are bit-packed and schema-driven.
- `CSVCMsg_CreateStringTable.string_data` and update string-table data are also
  decoded with `BitReader` because they use compact key/value encodings.

So the boundary is:

```text
complete protobuf payload bytes -> generated *_pb2 class
bit-packed replay substream     -> BitReader
```

## What This Package Does Not Do

`gem.binary` deliberately does not:

- know Dota hero, item, ability, or event semantics
- build entity serializers from send tables
- apply field decoders to entity state
- maintain string tables or entity lifecycles
- choose high-level parse outputs
- inspect generated protobuf descriptors

Those responsibilities live in `schema`, `state`, `combat`, `extractors`, and
the top-level parser orchestration.

Keeping this package narrow makes it easier to reason about replay corruption
and parser bugs. If the failure is "cannot isolate the next payload", look here.
If the failure is "the payload parses but the entity state is wrong", the bug is
usually in `schema` or `state`.

## Common Pitfalls

### Confusing Protobuf Payloads With Packed Streams

Do not call `ParseFromString` on `CDemoPacket.data` directly. That field is an
inner stream of message records, not one protobuf message.

Do call `ParseFromString` on each payload after the inner stream has provided a
complete `(type_id, payload)` pair.

### Losing Bit Alignment

Byte reads are only simple slices when the reader is byte-aligned. After any
bit-width read, the next byte may begin in the middle of the current underlying
byte. Use `BitReader.read_bytes` rather than slicing the original buffer by
hand.

### Treating Entity Data As Protobuf

`CSVCMsg_PacketEntities` is a protobuf message, but its `entity_data` field is a
bit-packed entity delta stream. Parse the outer protobuf first, then use
`BitReader` on `entity_data`.

### Ignoring Compression Flags

Outer demo messages can set the `DEM_IsCompressed` flag. `DemoStream` removes
the flag from the message type and decompresses the payload before yielding it.
Code downstream should not have to re-check outer compression.

String-table values may also be compressed, but that compression is local to
string-table parsing and is handled in `state.string_table`, not in
`DemoStream`.

## When To Add Code Here

Add code to `gem.binary` when the change is about moving through raw replay
bytes or interpreting a low-level Source 2 wire encoding.

Good fits:

- a missing bit/byte primitive used by several decoders
- a corrected Source 2 integer or float reader
- replay container framing behavior
- low-level error reporting for truncated buffers

Poor fits:

- mapping message IDs to Dota concepts
- changing entity field semantics
- decoding a specific hero/item/game event
- adding public analysis helpers

When in doubt, keep `gem.binary` format-focused and let higher layers attach
meaning to the values it reads.
