# Tutorial 02 · Inspecting the Entity Schema

Phase 2 gives you the **schema layer** — the complete description of every entity class in the replay and every field each class can transmit.  You can answer questions like:

- What fields does `CDOTA_Unit_Hero_Axe` have?
- How is `m_flMana` encoded on the wire?
- Which fields are fixed arrays, which are variable-length tables?

You cannot yet read actual field *values* — that requires Phase 3.

---

## What Phase 2 implements

Three modules:

| Module | What it does |
|---|---|
| `sendtable.py` | Parses `CDemoSendTables` → builds the serializer tree |
| `field_decoder.py` | Maps type strings to bit-reader callables |
| `field_path.py` | Huffman-coded field path decoder (used in Phase 3) |

---

## Step 1 — Find and parse the send tables

Every replay begins with a `CDemoSendTables` outer message (type 4) that defines the full schema.  It always appears before any entity data.

```python
from gem.stream import DemoStream
from gem.sendtable import parse_send_tables

DEM_SEND_TABLES = 4

def load_schema(path: str) -> dict:
    with DemoStream(path) as stream:
        for tick, msg_type, data in stream:
            if (msg_type & ~0x40) == DEM_SEND_TABLES:
                return parse_send_tables(data)
    raise RuntimeError("CDemoSendTables not found")

serializers = load_schema("my_replay.dem")
print(f"Found {len(serializers)} entity class serializers")
# Found 3223 entity class serializers
```

---

## Step 2 — List entity classes

```python
# All serializer names, sorted
for name in sorted(serializers):
    s = serializers[name]
    print(f"{name}  ({len(s.fields)} fields)")

# CDOTA_BaseNPC  (312 fields)
# CDOTA_BaseNPC_Additive  (312 fields)
# CDOTA_Unit_Hero_Axe  (178 fields)
# CDOTAGamerulesProxy  (1 field)
# ...
```

---

## Step 3 — Inspect a specific class

```python
s = serializers["CDOTA_Unit_Hero_Axe"]

for f in s.fields:
    print(f.var_name, f.var_type, f.model_name(), f.encoder or "—")
```

Output (excerpt):

```
m_iHealth          int32      simple        —
m_iMaxHealth       int32      simple        —
m_flMana           float32    simple        coord
m_flMaxMana        float32    simple        coord
m_vecAbilities     CNetworkUtlVectorBase< CHandle< CBaseEntity > >  variable-array  —
CBodyComponent     CBodyComponent   fixed-table   —
```

---

## Field models

Each field has one of five models that controls how it appears in entity delta packets:

| Model | Meaning |
|---|---|
| `simple` | A single scalar value |
| `fixed-array` | A fixed-length array (size known at schema time) |
| `variable-array` | A dynamic-length array (length sent before elements) |
| `fixed-table` | An embedded sub-serializer, accessed via pointer |
| `variable-table` | A dynamic collection of embedded sub-serializers |

---

## Field decoders

For any simple field you can call `find_decoder(field)` to get the callable that will later read values from a `BitReader`:

```python
from gem.field_decoder import find_decoder

f = serializers["CDOTA_Unit_Hero_Axe"].fields[10]  # m_iHealth
decoder = find_decoder(f)
print(decoder)  # <function signed_decoder at 0x...>
```

The decoder is just a function `(BitReader) -> value`.  In Phase 3, the entity parser calls it automatically — you never need to invoke it directly.

---

## What's next

Phase 3 wires the schema to the live entity delta stream.  Once complete you'll be able to:

- Read `m_iHealth`, `m_flMana`, position for any hero at any tick
- Subscribe to entity create/update/delete events
- Track full game state frame by frame

See [Tutorial 03 · Entity State](02_entity_state.md) (coming in Phase 3).
