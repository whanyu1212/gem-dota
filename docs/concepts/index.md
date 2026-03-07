# Concepts

These pages explain the underlying technology that gem is built on.
You don't need to read them to use gem — but if you've ever wondered
*why* the code looks the way it does, or want to understand what's
happening inside a replay file, this is the place to start.

| Page | What you'll learn |
|---|---|
| [The .dem Format](dem_format.md) | How replay files are structured at the binary level |
| [Protobuf](protobuf.md) | What Protocol Buffers are and why Valve uses them |
| [The Entity System](entity_system.md) | How game state is tracked with deltas and baselines |
| [Combat Log](combat_log.md) | How damage, kills, and ability events are recorded |
