# Bits & Bytes Primer (Dota Replay Context)

This page is a practical prerequisite for parser deep dives.

If you are comfortable with Python but less familiar with binary formats, read this first.
It explains exactly how replay bytes are laid out before `stream.py` and `parser.py` decode them.

## Why this matters

A `.dem` replay is not JSON and not plain protobuf from byte 0.

It is a binary container:

1. file header bytes,
2. repeated framed records,
3. protobuf payloads inside those records,
4. and sometimes bit-packed payloads inside protobuf fields.

Understanding these layers makes `stream.py` and `parser.py` much easier to follow.

## Bits vs bytes (quick refresh)

- `1 byte = 8 bits`.
- A byte is usually shown in hex (`0x00` to `0xFF`).
- Python `bytes` is an immutable sequence of byte values.

Example:

```python
b = b"\x50\x42\x44\x45"
print(len(b))         # 4 bytes
print(list(b))        # [80, 66, 68, 69]
print(b.hex(" "))     # 50 42 44 45
```

## The first bytes in a Source 2 Dota replay

`stream.py` expects this at the start:

1. 8-byte magic: `PBDEMS2\x00`
2. 8 metadata bytes (skipped by parser)

Exact byte layout:

```text
offset 0..7   : magic (8 bytes)
offset 8..11  : metadata uint32 #1 (little-endian)
offset 12..15 : metadata uint32 #2 (little-endian)
offset 16..   : first outer message record
```

Header hex shape:

```text
50 42 44 45 4d 53 32 00   00 00 00 00 00 00 00 00
|------ magic ---------|   |------ metadata ------|
```

What these mean:

- `PBDEMS2\x00` is the file signature for Source 2 protobuf demo format.
- The next 8 bytes are engine metadata hints (two little-endian `uint32` values).
- Parser logic does not need these hints for correctness because each outer message is self-framed (`command`, `tick`, `size`, `payload`).

Why parser skips metadata:

1. They are not required to decode message boundaries.
2. They can be stale in truncated files.

Example from local fixtures:

- `ti14_finals_g3_xg_vs_falcons.dem` metadata: `278882831`, `278882714`
- `ti14_finals_g3_xg_vs_falcons_truncated.dem` has the same metadata values but much smaller actual file size.

If magic mismatches, `DemoStream` raises immediately before parsing anything else.

## Outer message framing (what `stream.py` reads)

After header+metadata, replay data is a repeated sequence:

```text
command(varuint32) + tick(varuint32) + size(varuint32) + payload[size]
```

Where:

- `command` includes outer type plus compression flag bit.
- `tick` is game tick for this outer message.
- `size` is payload byte length.
- `payload` is usually protobuf bytes (`CDemo*` envelopes).

## Varuint32 in one minute

Varuint stores an integer across 1+ bytes:

- lower 7 bits of each byte carry value bits,
- high bit (`0x80`) says “continue to next byte”.

Small values (`0..127`) are 1 byte.

Examples:

| Value | Encoded bytes (hex) |
|---|---|
| `7` | `07` |
| `64` | `40` |
| `127` | `7f` |
| `128` | `80 01` |
| `300` | `ac 02` |

## A tiny synthetic replay fragment

Suppose we write one outer message:

- `command = 7` (`DEM_Packet`, uncompressed)
- `tick = 42`
- `size = 3`
- `payload = aa bb cc`

Bytes after header would be:

```text
07 2a 03 aa bb cc
|  |  |  \-- payload (3 bytes)
|  |  \----- size=3
|  \-------- tick=42
\----------- command=7
```

Full file prefix would look like:

```text
50 42 44 45 4d 53 32 00 00 00 00 00 00 00 00 00 07 2a 03 aa bb cc
```

## Compression flag in `command`

In Source 2 demo commands, `0x40` means “payload is Snappy-compressed”.

Example:

- base command `7` (`DEM_Packet`) -> `0x07`
- compressed command -> `0x47` (`0x40 | 0x07`)

`stream.py` does:

1. `compressed = bool(command & 0x40)`
2. `msg_type = command & ~0x40`

So downstream sees `msg_type == 7` whether compressed or not.

## How this connects to Dota replay parsing

At outer layer:

1. `stream.py` yields `(tick, msg_type, payload)` from framed bytes.
2. `parser.py` maps `msg_type` to outer protobuf envelope (`CDemoPacket`, `CDemoFullPacket`, etc.).
3. If envelope is packet-like, `parser.py` unpacks inner messages from `CDemoPacket.data`.

Inner packet framing is another repeated structure:

```text
type_id(ubit_var) + size(varuint32) + payload
```

That is why replay parsing is “layers of framing”, not a single protobuf decode call.

## Common beginner pitfalls

1. Treating the whole replay as one protobuf message.
2. Forgetting `command` also carries compression flag.
3. Mixing decimal and hex while debugging bytes.
4. Assuming every payload field is protobuf (some are bit-packed blobs).
5. Ignoring ordering: some inner messages must be processed before others.

## Next pages

1. [How Proto Parsing Works](proto-parsing-pipeline.md)
2. [Stream Layer (`stream.py`)](../deep-dives/stream-layer.md)
3. [Parser Layer (`parser.py`)](../deep-dives/parser-layer.md)
