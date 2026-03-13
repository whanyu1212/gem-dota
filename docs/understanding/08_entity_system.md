# The Entity System

The entity system is the core of a Dota 2 replay. Every game object — heroes, towers,
creeps, the game rules, runes, wards, couriers — is an **entity**. Their state is
tracked at every tick through an incremental delta system driven by the schema described
in [Send Tables](04_send_tables.md).

---

## What is an entity?

An entity is any game object with addressable state. Examples:

- `CDOTA_Unit_Hero_Axe` — Axe hero: HP, mana, level, position, items, abilities
- `CDOTAGamerulesProxy` — game rules: game time, game state, score, Roshan timer
- `CDOTA_NPC_Dota_Tower` — a tower: team, HP, kill status
- `CDOTA_Item_Observer_Ward` — a placed observer ward: position, owner, expiry
- `CDOTAPlayerController` — per-player state: gold, XP, last hits, denies

At any tick there can be hundreds of active entities. Each entity has dozens to
hundreds of fields.

---

## Entity indices and serials

Entities are stored in slots numbered 0–16383. Each slot has an associated **serial
number** — a 17-bit counter that increments when a new entity occupies the slot. This
prevents stale handles from referencing a new entity in the same slot.

A **handle** combines both:

```
handle = (serial << 14) | index
```

---

## svc_PacketEntities

All entity updates for a tick arrive in one `svc_PacketEntities` inner message
(type 55). The payload contains a bitstream with `updated_entries` entity records.

### Reading one entity record

```
1. Read index delta:
   ubit_var index_delta (relative to previous entity index, starting from -1)
   entity_index = previous_index + index_delta + 1

2. Read 2-bit command:
   bits 0b00 → UPDATE   (entity exists, delta follows)
   bits 0b10 → CREATE   (entity is being created)
   bits 0b01 → LEAVE    (entity leaves PVS / becomes inactive)
   bits 0b11 → DELETE   (entity is deleted; no field delta)

3. If CREATE:
   class_id   ← classIdSize bits   (classIdSize = floor(log2(max_classes)) + 1)
   serial     ← 17 bits
   padding    ← varuint32 (discard)
   Apply instancebaseline for this class_id
   Apply the packet's own delta on top

4. If UPDATE or CREATE (after baseline):
   read_fields(reader, serializer, entity.field_state)

5. Fire EntityTracker callbacks with the entity and its EntityOp flags
```

---

## FieldState

Entity field values are stored in a `FieldState` — a nested list tree that mirrors the
serialiser hierarchy. Accessing a field requires navigating the tree with a field path:

```python
# Conceptually:
field_state.set([3, 0], 128)   # set CBodyComponent.m_cellX to 128
field_state.get([3, 0])        # returns 128
```

The nesting reflects sub-serialisers:

```
FieldState (root)
├── [0] m_iTeamNum       → 2
├── [1] m_iHealth        → 1250
├── [2] m_flMana         → 480.0
└── [3] CBodyComponent   → [sub-list]
         ├── [0] m_cellX → 128
         ├── [1] m_cellY → 95
         └── [2] m_vecX  → -3.25
```

`FieldState` is implemented in `src/gem/field_state.py`.

---

## EntityOp flags

When a callback fires, it receives an `EntityOp` bitmask describing what happened:

| Flag | Meaning |
|---|---|
| `CREATED` | Entity was just created this tick |
| `UPDATED` | One or more fields changed |
| `DELETED` | Entity was removed |
| `ENTERED` | Entity entered the PVS (accompanies CREATED or a returning UPDATED) |
| `LEFT` | Entity left the PVS |

`EntityOp` is an `IntFlag`, so you can test combinations:

```python
if op & EntityOp.CREATED:
    ...
if op.has(EntityOp.UPDATED):
    ...
```

---

## Entity lifecycle

```
Tick N:  CREATE entity #42 (class: CDOTA_Unit_Hero_Axe)
          → op = CREATED | ENTERED
          → fields set from baseline, then delta applied

Tick N+5: UPDATE entity #42
          → op = UPDATED
          → delta applied (only changed fields)

Tick N+10: UPDATE entity #42, entity moves out of PVS
          → op = UPDATED | LEFT

...later...

Tick M:   entity #42 slot reused by a new entity (different serial)
          → op = CREATED | ENTERED
          → old state discarded, new baseline applied
```

---

## Reading field values

The `Entity` class exposes typed getter methods:

```python
hp,    ok = entity.get_int32("m_iHealth")
mana,  ok = entity.get_float32("m_flMana")
gold,  ok = entity.get_uint32("m_iGold")
name,  ok = entity.get_string("m_iszUnitName")
alive, ok = entity.get_bool("m_bIsAlive")

# Untyped (returns None if not found)
val = entity.get("m_iHealth")
```

All typed getters return a `(value, bool_ok)` tuple. `ok` is `True` on success,
`False` if the field does not exist or has a mismatched type.

Nested field access uses dot notation in the name string:

```python
cell_x, ok = entity.get_int32("CBodyComponent.m_cellX")
```

---

## Subscribing to entity events

```python
from gem.parser import ReplayParser
from gem.entities import EntityOp

parser = ReplayParser("my_replay.dem")

def on_entity(entity, op):
    if "Hero" not in entity.get_class_name():
        return
    if op & EntityOp.CREATED:
        hp, _ = entity.get_int32("m_iHealth")
        print(f"Hero created: {entity.get_class_name()} HP={hp}")

parser.on_entity(on_entity)
parser.parse()
```

Multiple handlers can be registered. All are called for every entity event.

---

## Full decode pipeline summary

```
DEM_SendTables (once)
  → parse CSVCMsg_FlattenedSerializer
  → build Serializer tree + assign decoders to every field

DEM_ClassInfo (once)
  → map class_id → network_name → Serializer

svc_CreateStringTable "instancebaseline" (once, early)
  → store baseline bytes per class_id

svc_PacketEntities (every tick, ~49,000 times per replay)
  → for each of updated_entries entities:
      read index delta → entity_index
      read 2-bit command
      if CREATE:
        read class_id, serial
        decode baseline bytes → apply to entity FieldState
      read field paths (Huffman) → list of (path, Field) pairs
      for each (path, Field):
        call field.decoder(reader) → value
        store value in entity.field_state at path
      fire EntityTracker callbacks with (entity, EntityOp)
```

## Functional reference

- [Entities API Reference](../reference/entities.md)
- [Field Paths API Reference](../reference/field_path.md)
- [Field Decoders API Reference](../reference/field_decoder.md)

Source: `src/gem/entities.py`, `src/gem/field_reader.py`, `src/gem/field_state.py`

Reference: `refs/manta/entity.go`
