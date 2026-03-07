# gem

**gem** is a Python library for parsing Dota 2 replay files (`.dem`), designed for data science and machine learning workflows.

Named after the **Gem of True Sight** — it reveals what is hidden inside replay files.

---

## What gem does

A Dota 2 replay is a 200–300 MB binary file that records every game event at 30 frames per second. gem reads that file and turns it into data structures your code can actually use — DataFrames, event streams, typed Python objects.

```python
from gem.stream import DemoStream

with DemoStream("my_replay.dem") as stream:
    for tick, msg_type, data in stream:
        print(tick, msg_type, len(data))
```

---

## Installation

```bash
pip install gem
```

Or with `uv`:

```bash
uv add gem
```

---

## Where to start

=== "I want to use it"

    Jump to the [Tutorials](tutorials/index.md) — start with
    [Reading a Replay](tutorials/01_reading_a_replay.md).

=== "I want to understand how it works"

    Start with [Concepts](concepts/index.md). The [.dem Format](concepts/dem_format.md)
    page explains the binary layout from scratch — no prior knowledge needed.

=== "I want the API"

    Go to the [API Reference](reference/index.md).

---

## Implementation status

gem is being built incrementally. Here's what's available today:

| Phase | What it unlocks | Status |
|---|---|---|
| 1 — Binary framing | Iterate outer messages, tick range, message type counts | ✅ Done |
| 2 — Schema | Parse send tables, resolve field types and decoders | ✅ Done |
| 3 — Entity state | Read hero HP, position, gold, items per tick | 🔜 Next |
| 4 — Events | Game events, combat log (damage, kills, abilities) | 🔜 |
| 5 — Extraction | Per-player time-series DataFrames | 🔜 |
| 6 — Full output | `ParsedMatch` object, JSON export | 🔜 |
