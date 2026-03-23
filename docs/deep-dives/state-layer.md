# State Reconstruction Layer

This page explains how gem turns packet updates into live world state.

Modules covered:

1. `src/gem/string_table.py`
2. `src/gem/entities.py`

Prerequisites:

1. [Bits & Bytes Primer](../cookbook/bits-and-bytes-primer.md)
2. [Stream Layer (`stream.py`)](stream-layer.md)
3. [Parser Layer (`parser.py`)](parser-layer.md)
4. [SendTable Layer (`sendtable.py`)](sendtable-layer.md)

## Why these two modules are one layer

`string_table.py` and `entities.py` are tightly coupled:

1. String tables carry lookup data and baselines.
2. Entities consume those baselines and decode deltas against them.

Without string table updates, entity decoding is incomplete or wrong.

## `string_table.py` constants and structures

### Constants

| Constant | Value | Meaning | Why it matters |
|---|---|---|---|
| `_KEY_HISTORY_SIZE` | `32` | Ring buffer length for key-prefix compression. | Needed to reconstruct compacted keys correctly. |

### Data structures

| Type | Role |
|---|---|
| `StringTableItem(index, key, value)` | One parsed update entry. |
| `StringTable` | A named table with metadata and current items. |
| `StringTables` | Container of all tables by id and by name. |

## `parse_string_table(...)` step-by-step

This decodes a bit-packed string table blob.

For each update entry:

1. Decode index:
   - increment previous index, or
   - read absolute index (`varuint + 1`).
2. Decode key:
   - maybe absent,
   - maybe direct string,
   - maybe prefix-compressed via history buffer (`pos`, `size`, `suffix`).
3. Decode value:
   - fixed-size or variable-size,
   - optional per-entry compression flag (`flags & 0x1`),
   - optional Snappy decompression.

Output is an ordered list of `(index, key, value)` updates.

## Message handlers in `string_table.py`

### `handle_create(msg, string_tables)`

1. Creates new `StringTable` metadata.
2. Decompresses full blob if `data_compressed` is set.
3. Parses initial items and stores them by index.
4. Registers table in global container.

### `handle_update(msg, string_tables)`

1. Looks up existing table by `table_id`.
2. Parses changed entries.
3. Merges updates per item index:
   - empty key keeps old key,
   - empty value keeps old value.

This merge behavior is critical because updates may send only key or only value.

## `entities.py` constants and structures

### Constants

| Constant | Value | Meaning | Why it matters |
|---|---|---|---|
| `_INDEX_BITS` | `14` | Number of low bits used for entity index in handles. | Defines max slot pool (`2^14 = 16384`). |
| `_HANDLE_MASK` | `(1 << 14) - 1` | Mask to extract entity index from handle. | Used in `find_by_handle`. |
| `_GAME_BUILD_RE` | regex `/dota_v(\d+)/` | Build extraction from `ServerInfo.game_dir`. | Enables build-aware logic across parser stack. |

### `EntityOp` flags

| Flag | Value | Meaning |
|---|---|---|
| `CREATED` | `0x01` | Entity slot created this packet. |
| `UPDATED` | `0x02` | Existing entity updated. |
| `DELETED` | `0x04` | Entity removed from slot. |
| `ENTERED` | `0x08` | Entity entered active set. |
| `LEFT` | `0x10` | Entity left active set. |

Convenience combinations in code:

- `CREATED_ENTERED` (`0x09`)
- `UPDATED_ENTERED` (`0x0A`)
- `DELETED_LEFT` (`0x14`)

### Key classes

| Class | Role |
|---|---|
| `ClassInfo` | Maps class id -> class name + serializer. |
| `Entity` | One live entity with decoded field state and typed accessors. |
| `EntityTracker` | Event handler registry + dispatch. |
| `EntityManager` | Main lifecycle/state owner for all entities. |

## Entity field access model

`Entity` stores state in two forms:

1. flat dict (`_state`) for direct key-value access,
2. hierarchical `FieldState` (`_field_state`) for decoded replay fields.

`Entity.get(name)` behavior:

1. fast path: check `_state` directly,
2. slow path: resolve field path from serializer (`_find_field_path`) and query `FieldState`.

Field-path resolution helpers:

- `_find_field_path`
- `_resolve_in_serializer`
- `_resolve_in_field`

These map dotted names to field indices in nested models.

## `EntityManager` lifecycle methods

### `on_server_info(msg)`

1. Computes `class_id_size` from `max_classes`.
2. Allocates full entity slot array (`16384` slots).
3. Extracts `game_build` from `game_dir` via regex.

### `on_class_info(msg)`

1. Builds `classes_by_id` and `classes_by_name`.
2. Marks class info ready.
3. Triggers baseline refresh (`_update_baselines`).

### `on_baseline_updated()` / `_update_baselines()`

Reads `instancebaseline` string table and maps:

```python
class_id -> baseline_bytes
```

These baselines are applied before per-packet deltas on entity creation.

## Packet entity decode flow (`on_packet_entities`)

For each updated entry:

1. Read entity index delta.
2. Read 2-bit command.
3. Execute one lifecycle branch.

Command branch table from code logic:

| `cmd` bits | Operation |
|---|---|
| `00` | Update existing entity |
| `10` | Create new entity |
| `01` | Leave (deactivate) entity |
| `11` | Delete entity |

Create path (`10`) specifics:

1. Read `class_id`, `serial`.
2. Instantiate `Entity`.
3. Apply class baseline first.
4. Apply delta fields second.
5. Dispatch `CREATED | ENTERED`.

Update path (`00`) specifics:

1. Entity must already exist.
2. If inactive, mark active and add `ENTERED`.
3. Read and apply field deltas.

Leave/delete path (`01`/`11`):

- leave marks inactive,
- delete removes slot entry.

## Lookup helpers and why they matter

`EntityManager` utility methods:

1. `find(index)` direct slot lookup.
2. `find_by_handle(handle)` split handle into index+serial and validate both.
3. `find_by_class_name(...)` and `all_active()` for high-level scans.
4. `find_by_npc_name(...)` uses `EntityNames` string table for combat-log name resolution.

## Real snapshot from fixture

Using `tests/fixtures/8520014563.dem`, parse up to tick 600:

```text
tick_end 601
string_tables 18
instancebaseline_entries 33
entity_manager_exists True
classes 3172
class_baselines 33
active_entities 94
sample_entity_events
(4, 0, 'CWorld', 9)
(4, 1, 'CDOTAPlayerController', 9)
(4, 2, 'CDOTAPlayerController', 9)
...
```

Interpretation:

1. `EntityOp` value `9` means `CREATED | ENTERED`.
2. Baselines are loaded early (`instancebaseline_entries = 33`).
3. Active entities grow as packet entity messages are applied.

## Common failure modes in this layer

1. Wrong message ordering (entity deltas before string-table updates).
2. Missing class info or wrong `class_id_size`.
3. Baseline table not loaded when creation deltas are applied.
4. Handle mismatch bugs (wrong index/serial split).

When symptoms are “fields missing/wrong after parser is otherwise healthy,” this is the first layer to inspect.

## Next pages

1. [Event Normalization Layer (`game_events.py` + `combatlog.py`)](event-layer.md)
2. [Entity State](../guides/02_entity_state.md)
3. [Combat Log](../guides/03_combat_log.md)
