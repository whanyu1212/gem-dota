# Tutorial 01 · Reading a Replay

**Phase 1 · Available now**

In this tutorial you'll open a Dota 2 replay file, iterate its outer
messages, and understand what each message type means. No prior knowledge
of binary formats or protobuf is required.

---

## Prerequisites

```bash
pip install gem
```

You'll need a `.dem` replay file. You can download one from
[opendota.com](https://www.opendota.com) — find any match and click
"Download Replay".

---

## Step 1: Open the file

```python
from gem.stream import DemoStream

with DemoStream("my_replay.dem") as stream:
    for tick, msg_type, data in stream:
        print(tick, msg_type, len(data))
```

`DemoStream` accepts a file path and **memory-maps** the file — it doesn't
load 266 MB into RAM before starting. You'll see output immediately.

Each iteration yields a tuple of three values:

| Variable | Type | Meaning |
|---|---|---|
| `tick` | `int` | Game tick (30 ticks = 1 second). Pre-game is normalised to 0. |
| `msg_type` | `int` | `EDemoCommands` integer identifying the message type |
| `data` | `bytes` | Raw (decompressed) protobuf payload |

---

## Step 2: Count message types

Let's build a breakdown of what's in the replay:

```python
from collections import Counter
from gem.stream import DemoStream

# Human-readable names for EDemoCommands
MSG_NAMES = {
    0: "DEM_Stop",         1: "DEM_FileHeader",
    2: "DEM_FileInfo",     3: "DEM_SyncTick",
    4: "DEM_SendTables",   5: "DEM_ClassInfo",
    6: "DEM_StringTables", 7: "DEM_Packet",
    8: "DEM_SignonPacket", 13: "DEM_FullPacket",
}

counts = Counter()

with DemoStream("my_replay.dem") as stream:
    for tick, msg_type, data in stream:
        counts[msg_type] += 1

for msg_type, count in sorted(counts.items()):
    name = MSG_NAMES.get(msg_type, str(msg_type))
    print(f"{name:<20} {count:>8,}")
```

On the TI14 Grand Finals Game 1 replay (55 minutes), this gives:

```
DEM_Stop                    1
DEM_FileHeader              1
DEM_FileInfo                1
DEM_SyncTick                1
DEM_SendTables              1
DEM_ClassInfo               1
DEM_StringTables            1
DEM_Packet             49,591
DEM_SignonPacket           10
DEM_FullPacket             56
```

`DEM_Packet` dominates — there's one per game tick, and it contains all
the game state changes for that tick.

---

## Step 3: Find the tick range

```python
from gem.stream import DemoStream

min_tick, max_tick = 10**9, 0

with DemoStream("my_replay.dem") as stream:
    for tick, msg_type, data in stream:
        if tick < min_tick:
            min_tick = tick
        if tick > max_tick:
            max_tick = tick

game_seconds = max_tick / 30
print(f"Tick range: {min_tick} → {max_tick}")
print(f"Game duration: {game_seconds:.0f}s  ({game_seconds/60:.1f} min)")
```

```
Tick range: 0 → 99262
Game duration: 3309s  (55.1 min)
```

!!! tip "Pre-game ticks"
    Ticks before the game starts (during the draft and loading screen) are
    encoded as `0xFFFFFFFF` in the file. gem normalises these to `0`
    automatically.

---

## Step 4: Measure throughput

```python
import time
from gem.stream import DemoStream
from pathlib import Path

path = Path("my_replay.dem")
file_mb = path.stat().st_size / 1024 / 1024

t0 = time.perf_counter()

with DemoStream(path) as stream:
    total = sum(1 for _ in stream)

elapsed = time.perf_counter() - t0
print(f"{total:,} messages in {elapsed:.2f}s  ({file_mb/elapsed:.0f} MB/s)")
```

```
49,667 messages in 0.45s  (597 MB/s)
```

gem processes a 266 MB replay in under half a second at this stage —
purely scanning the binary framing, no protobuf decoding yet.

---

## What's next?

At this point, gem can tell you **how many** messages are in a replay and
**what types** they are, but it can't decode their contents yet.

The `data` bytes in each message are protobuf-encoded — to decode them
you need the send table schema, which gem parses in Phase 2. Once that's
done, you'll be able to read entity state, game events, and eventually
extract per-player statistics.

Continue to [Tutorial 02 · Entity State](02_entity_state.md) (available
after Phase 2 and 3 are complete).

---

## Full example

```python
"""
phase1_stream.py — what gem can do after Phase 1.

Usage: python phase1_stream.py my_replay.dem
"""
import sys
import time
from collections import Counter
from pathlib import Path
from gem.stream import DemoStream

MSG_NAMES = {
    0: "DEM_Stop",         1: "DEM_FileHeader",
    2: "DEM_FileInfo",     3: "DEM_SyncTick",
    4: "DEM_SendTables",   5: "DEM_ClassInfo",
    6: "DEM_StringTables", 7: "DEM_Packet",
    8: "DEM_SignonPacket", 13: "DEM_FullPacket",
}

path = Path(sys.argv[1] if len(sys.argv) > 1 else "my_replay.dem")
file_mb = path.stat().st_size / 1024 / 1024
print(f"Replay : {path.name}  ({file_mb:.1f} MB)")
print("Scanning...", flush=True)

counts: Counter[int] = Counter()
min_tick, max_tick = 10**9, 0
t0 = time.perf_counter()

with DemoStream(path) as stream:
    for tick, msg_type, data in stream:
        counts[msg_type] += 1
        if tick < min_tick: min_tick = tick
        if tick > max_tick: max_tick = tick

elapsed = time.perf_counter() - t0
print(f"Messages : {sum(counts.values()):,}")
print(f"Ticks    : {min_tick} → {max_tick}  ({max_tick/30:.0f}s)")
print(f"Time     : {elapsed:.2f}s  ({file_mb/elapsed:.0f} MB/s)")
print()

for t, c in sorted(counts.items()):
    print(f"  {MSG_NAMES.get(t, str(t)):<20} {c:>8,}")
```
