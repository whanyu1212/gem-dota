# String Tables

String tables are key→value dictionaries that are built up and patched incrementally
throughout a replay. They carry data that is too dynamic or too large to put in entity
fields — name lookups, baseline state blobs, modifier data, and more.

---

## Creation and updates

Two inner net messages manage string tables:

- **`svc_CreateStringTable`** (type 44) — creates a new table and sets its initial
  entries.
- **`svc_UpdateStringTable`** (type 45) — patches an existing table, adding or
  modifying entries.

A table is identified by name (e.g. `"instancebaseline"`, `"CombatLogNames"`) and by
an integer ID assigned at creation time.

---

## Entry format

Each entry is an `(index, key, value)` triple:

- **index** — integer position in the table (can be sparse; gaps are valid)
- **key** — a string key (the "name" of the entry)
- **value** — arbitrary bytes (often empty, or a serialised protobuf message)

String table data in `svc_CreateStringTable` uses a custom bit-packed format —
**not** standard protobuf. gem's `parse_string_table()` in `src/gem/string_table.py`
implements the decoder.

---

## Key history compression

To save space, keys can reference previous keys via a **key history buffer** of the
last 32 keys seen. An entry with key compression encodes:

```
use_history: 1 bit
if use_history:
  index:  5 bits  (which of the last 32 keys to reference)
  length: 5 bits  (how many characters to borrow from that key)
  suffix: null-terminated string (appended after the borrowed prefix)
```

For example, if a previous key was `"npc_dota_hero_axe"` and the new key is
`"npc_dota_hero_axe_sword"`, the encoding can borrow the first 17 characters and only
send `"_sword\0"`.

---

## Value compression

String table values may themselves be compressed. The `user_data_fixed_size` flag in
`svc_CreateStringTable` controls this:

- If `user_data_fixed_size` is set and `user_data_size > 0`, each value is exactly
  `user_data_size` bytes (fixed-width entries).
- Otherwise, a bit flag per entry indicates whether the value is present and, if
  `user_data_size_bits` is set, the size is read from that many bits.
- Some tables store Snappy-compressed values at the per-entry level — gem detects and
  decompresses these.

---

## Critical string tables

### `instancebaseline`

The most important string table for entity parsing. It stores **default field state**
for each entity class.

- **Key**: the `class_id` as a decimal string, e.g. `"42"`.
- **Value**: serialised field state bytes — the same format as a partial entity delta,
  decoded through the entity's serialiser.

When a new entity is created, gem:

1. Looks up the class baseline in `instancebaseline` by `class_id`.
2. Decodes the baseline bytes through the entity's serialiser (same as applying a delta).
3. Applies the packet's own delta on top.

This gives the entity its default values without the server retransmitting every field.

### `CombatLogNames`

Used in **S1 (older)** replays. Maps integer indices to unit/ability/item name strings:

```
0  → "npc_dota_hero_axe"
1  → "axe_berserkers_call"
2  → "npc_dota_hero_juggernaut"
```

New entries are added throughout the replay as new units/abilities appear. When a
combat log game event arrives, its `sourcename`, `targetname`, and `inflictor` fields
are indices into this table.

### `EntityNames`

Maps `m_pEntity.m_nameStringableIndex` (an integer stored on entity objects) to the
entity's class name string. Used for resolving item names from hero inventory handles.

### `ActiveModifiers`

Stores active modifier state as `CDOTAModifierBuffTableEntry` protobuf messages.
Each entry encodes which heroes (player slots) currently carry a given modifier.
Not used by gem's current extractors, but available for extension.

---

## gem API

```python
from gem.string_table import StringTables, handle_create, handle_update

# StringTables is managed internally by ReplayParser.
# Access via parser.string_tables after parsing.
table = parser.string_tables.get_by_name("instancebaseline")

# Each item is a (key, value) tuple at index i:
key, value = table.items[class_id_int]
```

Source: `src/gem/string_table.py`
