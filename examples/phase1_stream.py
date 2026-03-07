"""Phase 1 example — outer message stream.

Demonstrates what gem can do after Phase 1 (reader.py + stream.py):
  - Validate the replay header
  - Iterate every outer demo message
  - Report message type breakdown, tick range, and throughput

Phase 1 operates purely at the binary framing level. It has no knowledge
of protobuf schemas, entity state, or game events — those come in later
phases. What it *can* do is tell you exactly what kinds of messages are
in a replay and how fast it can scan through them.

Usage:
    python examples/phase1_stream.py <path/to/replay.dem>
"""

import sys
import time
from collections import Counter
from pathlib import Path

# EDemoCommands names (from src/gem/proto/dota2/demo_pb2.py)
_DEMO_COMMAND_NAMES: dict[int, str] = {
    0: "DEM_Stop",
    1: "DEM_FileHeader",
    2: "DEM_FileInfo",
    3: "DEM_SyncTick",
    4: "DEM_SendTables",
    5: "DEM_ClassInfo",
    6: "DEM_StringTables",
    7: "DEM_Packet",
    8: "DEM_SignonPacket",
    13: "DEM_FullPacket",
    15: "DEM_SpawnGroups",
    17: "DEM_AnimationHeader",
    18: "DEM_Recovery",
}


def run(replay_path: Path) -> None:
    from gem.stream import DemoStream

    file_bytes = replay_path.stat().st_size
    file_mb = file_bytes / 1024 / 1024

    print(f"Replay : {replay_path.name}")
    print(f"Size   : {file_mb:.1f} MB ({file_bytes:,} bytes)")
    print("Scanning...", flush=True)

    t0 = time.perf_counter()
    counts: Counter[int] = Counter()
    payload_bytes: Counter[int] = Counter()
    min_tick = 10**9
    max_tick = 0
    total_messages = 0

    # Pass the path directly — DemoStream memory-maps the file,
    # so iteration starts immediately without loading 266 MB into RAM.
    with DemoStream(replay_path) as stream:
        for tick, msg_type, data in stream:
            counts[msg_type] += 1
            payload_bytes[msg_type] += len(data)
            if tick < min_tick:
                min_tick = tick
            if tick > max_tick:
                max_tick = tick
            total_messages += 1

    elapsed = time.perf_counter() - t0
    throughput = file_mb / elapsed

    print(f"Messages : {total_messages:,}")
    print(f"Ticks    : {min_tick} → {max_tick}  ({max_tick / 30:.0f}s game time at 30 ticks/s)")
    print(f"Time     : {elapsed:.2f}s  ({throughput:.0f} MB/s)")
    print()

    # --- message type table ---
    col_name = max(len(n) for n in _DEMO_COMMAND_NAMES.values())
    print(f"{'Message type':<{col_name}}   {'count':>8}   {'payload':>12}")
    print("-" * (col_name + 26))
    for msg_type, count in sorted(counts.items()):
        name = _DEMO_COMMAND_NAMES.get(msg_type, f"type_{msg_type}")
        kb = payload_bytes[msg_type] / 1024
        print(f"{name:<{col_name}}   {count:>8,}   {kb:>10.1f} KB")

    print()

    # --- what Phase 1 can / cannot do ---
    print("What Phase 1 gives us:")
    print(
        f"  ✓  DEM_Packet arrives {counts.get(7, 0):,} times — these contain all game state updates"
    )
    print(f"  ✓  DEM_FullPacket arrives {counts.get(13, 0):,} times — periodic full snapshots")
    print(f"  ✓  DEM_SignonPacket arrives {counts.get(8, 0):,} times — replay initialisation")
    print("  ✗  Cannot decode packet contents yet (needs Phase 2: sendtable + field decoders)")
    print("  ✗  Cannot read entity state, game events, or combat log")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        default = Path("tests/fixtures/ti14_finals_g1_xg_vs_falcons.dem")
        if default.exists():
            path = default
        else:
            print("Usage: python examples/phase1_stream.py <replay.dem>")
            sys.exit(1)
    else:
        path = Path(sys.argv[1])

    if not path.exists():
        print(f"Error: file not found: {path}")
        sys.exit(1)

    run(path)
