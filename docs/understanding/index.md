# Understanding the Format

This section explains how Dota 2 replay files are structured at the binary level.
Read in order — each page builds on the previous.

A `.dem` file is a 200–300 MB binary blob. Nothing inside it is plain text or JSON.
To extract a single field value — say, a hero's HP at a specific tick — a parser must
work through six nested layers of encoding before arriving at a number. These pages
explain each layer.

---

| Page | What you will learn |
|---|---|
| [1 · Protocol Buffers](01_protobuf.md) | The binary serialisation format used for nearly every payload |
| [2 · The .dem Format](02_dem_format.md) | The outer message framing — magic bytes, command+tick+size+payload |
| [3 · Snappy Compression](03_snappy.md) | When and how payloads are compressed |
| [4 · Send Tables & Schema](04_send_tables.md) | The entity class schema: serialisers, fields, types, decoders |
| [5 · Field Paths & Huffman](05_field_paths.md) | How field addresses inside entities are Huffman-coded |
| [6 · Field Decoders](06_field_decoders.md) | How individual field values are read from the bit stream |
| [7 · String Tables](07_string_tables.md) | Key→value dictionaries built incrementally through the replay |
| [8 · The Entity System](08_entity_system.md) | Entity lifecycle: create, update, delete, and the delta loop |
| [9 · The Combat Log](09_combat_log.md) | Damage, kills, abilities, gold, and items — two ingestion paths |
| [10 · Game Events](10_game_events.md) | Rune pickups, aegis, chat messages, and typed event dispatch |
