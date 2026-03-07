# The Entity System

The entity system is the most complex part of a Dota 2 replay. It is
how the game server tells the client — and therefore the replay — what
every game object is doing at every tick.

Understanding this is not required to use gem, but it explains *why*
the library is structured the way it is.

---

## What is an entity?

An **entity** is any game object with trackable state:

- Heroes (position, HP, mana, level, items, abilities)
- Towers and buildings (HP, team)
- Creeps (position, HP)
- The game rules object (game time, score, game state)
- Runes, wards, couriers, neutrals

At any given tick, there can be hundreds of active entities. Each one
has dozens to hundreds of **fields** — named properties with typed values.

A hero entity might have fields like:

```
m_iHealth            → 1250   (int32)
m_flMana             → 480.0  (float32)
CBodyComponent.m_cellX → 128  (uint32)   ← map position
m_hOwnerEntity       → 0x4002 (handle)   ← reference to player
m_vecAbilities.0001  → 0x0012 (handle)   ← first ability slot
```

---

## The naive approach (and why it doesn't work)

If the game sent the complete state of every entity every tick, the
replay would be enormous. 500 entities × 100 fields × 4 bytes × 30
ticks/second × 3600 seconds = **216 GB per hour**. That's not viable.

Instead, the game uses a **delta system**: only send what changed.

---

## The delta system

At the start of a replay, entities have a **baseline** — a default set
of field values for their class. When an entity is created, the server
sends:

1. The entity's class ID (which class is it?)
2. Only the fields that differ from the baseline

On subsequent ticks, the server sends only the fields that changed since
the last update. This is called a **delta**.

```
Tick 0:  Create hero entity #42 (class: CDOTA_Unit_Hero_Axe)
         Apply baseline for Axe
         Apply delta: { m_iHealth: 1250, m_flMana: 480 }

Tick 1:  Update entity #42
         Delta: { m_flMana: 460 }   ← only mana changed

Tick 2:  Update entity #42
         Delta: { m_iHealth: 1100, CBodyComponent.m_cellX: 130 }
```

gem maintains a dictionary of entity state and applies each delta as it
arrives. When you call `entity.get("m_iHealth")`, you're reading from
this dictionary.

---

## Field paths

Entity data is packed tightly into a bit stream. To identify *which*
field is being updated, the encoding uses a **field path** — a compact
address into the entity's field tree.

An entity's fields are organised hierarchically. Some fields contain
nested sub-objects (like `CBodyComponent`, which holds position data).
The field path is an array of indices tracing through this tree:

```
[3]        → top-level field 3
[3, 1]     → sub-field 1 of top-level field 3
[3, 1, 0]  → sub-sub-field 0
```

To keep field paths compact, they're encoded using **Huffman coding** —
the most common path operations (like "increment the last index by 1")
get shorter bit sequences. gem's `field_path.py` implements the full
table of 40 path operations.

---

## Send tables: the schema

To decode an entity update, gem needs to know: for field path `[3, 1]`
in class `CDOTA_Unit_Hero_Axe`, what type is the value, and how is it
encoded?

This schema is called the **send tables**. It's sent once at the start
of the replay as a `DEM_SendTables` message, containing a
`CSVCMsg_FlattenedSerializer` protobuf. This defines:

- Every entity class (serializer)
- Every field in every class
- The type, bit count, and encoding of every field

```
Serializer: CDOTA_Unit_Hero_Axe
  Field 0:  m_iTeamNum         type=uint8
  Field 1:  m_iHealth          type=int32
  Field 2:  m_flMana           type=CNetworkedQuantizedFloat  bits=11
  Field 3:  CBodyComponent     type=serializer (nested)
    Field 0: m_cellX           type=uint32
    Field 1: m_cellY           type=uint32
    ...
  ...
```

gem builds this schema once from `DEM_SendTables` and uses it for the
entire replay. This is Phase 2.

---

## Field decoders

Each field type has a corresponding **decoder** — a function that reads
the right number of bits from the bit stream and returns a Python value.

| Field type | Decoder | What it reads |
|---|---|---|
| `bool` | `boolean_decoder` | 1 bit |
| `int32` | `signed_decoder` | zigzag varint |
| `uint32` | `unsigned_decoder` | varint |
| `float32` | depends on encoder | 32 bits (raw) or coord-encoded |
| `CNetworkedQuantizedFloat` | `QuantizedFloatDecoder` | N bits, mapped to range |
| `Vector` | `vector_factory(3)` | 3× float decoder |
| `CUtlString` | `string_decoder` | null-terminated bytes |

Decoders are resolved **once** when the send table is parsed, not on
every entity update. This makes the hot path (applying thousands of
entity deltas per second) as fast as possible.

---

## Entity lifecycle

Entities are created, updated, and deleted throughout the replay.
gem tracks this with an `EntityOp` flag:

| Op | Meaning |
|---|---|
| `Created` | First time this entity appears |
| `Entered` | Entity became active (created or re-activated) |
| `Updated` | One or more fields changed |
| `Left` | Entity became inactive |
| `Deleted` | Entity was removed entirely |

You can subscribe to entity changes:

```python
# (Phase 3+)
parser.on_entity(lambda entity, op: ...)
```

---

## The instancebaseline string table

There's one more piece: the **instancebaseline** string table. It stores
the baseline field values for each class as a pre-encoded binary blob.
When a new entity is created, gem:

1. Looks up the baseline blob for that class
2. Decodes it through the send table schema (same as a delta update)
3. Applies the packet's own delta on top

This is how newly created entities start with sensible default values
without the server sending every field from scratch.

---

## Summary: the full decode pipeline

```
DEM_SendTables (once)
  → parse CSVCMsg_FlattenedSerializer
  → build Serializer tree + assign decoders

DEM_ClassInfo (once)
  → map class IDs → class names → serializers

CSVCMsg_CreateStringTable "instancebaseline" (once)
  → store baseline bytes per class ID

CSVCMsg_PacketEntities (every tick)
  → for each entity update:
      read delta index (which entity?)
      read 2-bit command (create / update / delete)
      if create:
        decode baseline → apply to entity state
      decode field paths (Huffman)
      for each field path:
        look up decoder from serializer
        call decoder(bit_reader) → value
        store value in entity state
      fire OnEntity callbacks
```

This pipeline runs ~49,000 times in a single replay.
