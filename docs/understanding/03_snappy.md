# Snappy Compression

Some outer messages in a `.dem` replay are compressed. This page explains when that
happens and what gem does about it.

---

## The compressed flag

As described in [The .dem Format](02_dem_format.md), the `command` field of each outer
message packs two things together:

```python
msg_type   = command & ~0x40
compressed = bool(command & 0x40)   # DEM_IsCompressed = 0x40
```

Bit 6 (`0x40`) is the compression flag. When it is set:

1. Strip the flag to get the real `msg_type`.
2. Decompress the payload bytes with Snappy before passing them to a protobuf parser.

---

## What is Snappy?

Snappy is a fast compression/decompression library written by Google. Its design goal is
speed rather than maximum compression ratio — it typically compresses at several hundred
MB/s and decompresses faster still, with compression ratios around 1.5–1.7× for typical
game data.

Snappy is **not** zlib and **not** gzip. The byte format is incompatible with both.
Calling `zlib.decompress()` on Snappy data will raise an error.

gem uses the `python-snappy` package:

```python
import snappy

decompressed = snappy.decompress(raw_payload_bytes)
```

---

## Which messages are compressed?

In a typical Dota 2 replay:

- **`DEM_FullPacket`** — almost always compressed. These are periodic full entity
  snapshots that can be several hundred kilobytes each. Compression is significant here.
- **`DEM_Packet`** — usually not compressed (the incremental delta packets).
- **Other types** — occasionally compressed; always check the flag.

The flag must be checked on every outer message. Do not assume only certain types are
ever compressed.

---

## gem's implementation

`DemoStream` (`src/gem/stream.py`) handles this transparently. The `data` bytes it
yields are always decompressed — callers never need to call Snappy themselves:

```python
from gem.stream import DemoStream

with DemoStream("my_replay.dem") as stream:
    for tick, msg_type, data in stream:
        # data is already decompressed — pass directly to ParseFromString()
        pass
```

Inside `DemoStream`, the relevant logic is:

```python
if command & 0x40:
    msg_type = command & ~0x40
    data = snappy.decompress(data)
```

---

## Snappy inside string tables

There is a second location where Snappy appears: string table values. Some entries in
`svc_CreateStringTable` messages have their value bytes Snappy-compressed at the
per-entry level. gem's `string_table.py` handles this separately from the outer
message decompression.

See [String Tables](07_string_tables.md) for details.
