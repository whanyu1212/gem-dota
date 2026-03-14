# Send Tables & the Schema

Before any entity data can be decoded, the parser needs a **schema** that describes every
entity class: what fields it has, what types those fields are, and how to decode their
binary encoding. That schema is called the **send tables**.

---

## Where the schema lives

A `DEM_SendTables` outer message (type ID 4) appears exactly once per replay, near the
start of the file and before any entity packets. Its payload is a protobuf
`CDemoSendTables` message whose `data` field contains a serialised
`CSVCMsg_FlattenedSerializer` — the complete class schema for this replay build.

```
DEM_SendTables (outer message, type 4)
└── CDemoSendTables (protobuf)
    └── .data: bytes
        └── CSVCMsg_FlattenedSerializer (protobuf, embedded)
            ├── serializers[0]: name="CBaseAnimatingActivity", version=0
            │   └── fields_index: [0, 1, 2, ...]
            ├── serializers[1]: name="CDOTA_Unit_Hero_Axe", version=0
            │   └── fields_index: [0, 3, 7, ...]
            └── fields[0..N]: ProtoFlattenedSerializerField_t
                ├── var_name_sym: symbol index
                ├── var_type_sym: symbol index
                ├── field_serializer_name_sym: (if nested type)
                ├── encoder_sym: (e.g. "coord", "qangle_pitch_yaw")
                ├── encode_flags: bitmask
                ├── bit_count: int
                ├── low_value: float
                └── high_value: float
```

The `symbols` array in `CSVCMsg_FlattenedSerializer` maps symbol indices to strings.
All names (var names, type names, encoder names) are stored as symbol indices to avoid
redundant string storage.

gem parses this in `src/gem/sendtable.py` and builds an in-memory `Serializer` tree.

---

## Serialisers and fields

A **serialiser** represents one entity class. It has a name (matching the network class
name) and a list of **fields** in order.

A **field** describes one property of an entity. Key attributes:

| Attribute | Meaning |
|---|---|
| `var_name` | Field name as it appears in entity state, e.g. `m_iHealth` |
| `var_type` | Type string, e.g. `int32`, `float32`, `CNetworkedQuantizedFloat` |
| `base_type` | Parsed from `var_type` — the core type name |
| `encoder` | Optional encoding hint: `coord`, `qangle_pitch_yaw`, `normal`, etc. |
| `bit_count` | For fixed-width fields: number of bits |
| `low_value` | Quantized float range minimum |
| `high_value` | Quantized float range maximum |
| `field_serializer_name` | For nested types: name of the sub-serialiser |
| `encode_flags` | Bitmask controlling rounding behaviour for quantized floats |

---

## Field models

Each field has one of five **models** that control how it appears in entity delta packets:

| Model | Meaning |
|---|---|
| `SIMPLE` | A single scalar value — one path, one decoder call |
| `FIXED_ARRAY` | A compile-time-fixed-length array, e.g. `m_vecAbilities[16]` |
| `FIXED_TABLE` | An embedded sub-serialiser accessed via a pointer field |
| `VARIABLE_ARRAY` | A runtime-variable-length array; the current length is tracked in the entity state |
| `VARIABLE_TABLE` | A runtime-variable collection of embedded sub-serialisers |

The model is inferred from the field's type string and whether `field_serializer_name` is
set. For example:

- `int32` → `SIMPLE`
- `CHandle< CBaseEntity >[16]` → `FIXED_ARRAY`
- `CNetworkUtlVectorBase< CHandle< CBaseEntity > >` → `VARIABLE_ARRAY`
- `CBodyComponent` (with `field_serializer_name` set) → `FIXED_TABLE`

---

## Pointer types

Some type names are **pointer types** — embedded sub-serialisers that are accessed via
a pointer field rather than being inlined. Examples:

```
CBodyComponent, CEntityIdentity, CPhysicsComponent, CRenderComponent,
CDOTAGamerules, CDOTAPlayerController, CDOTATeam
```

gem identifies these by a fixed list in `sendtable.py`. When a field's type is a pointer
type, a synthetic boolean field `{var_name}.m_bMinimumList` is inserted into the
serialiser before the sub-serialiser's fields. This matches how manta/clarity handle the
format.

---

## CDemoClassInfo

After `DEM_SendTables`, a `DEM_ClassInfo` message (type 5) arrives. It maps:

```
class_id (integer) → network_name (string) → serialiser
```

The `network_name` is the same string as the serialiser name (e.g.
`CDOTA_Unit_Hero_Axe`). The `class_id` is a compact integer used in entity packets to
identify the class without sending the full string name.

gem stores this mapping in `EntityManager.classes_by_id` so it can look up the
serialiser for any entity in O(1).

---

## Decoder assignment

When gem parses the send tables, it calls `find_decoder(field)` for each field and
stores the result on the field object. Decoders are resolved **once** at schema-parse
time — not on every entity update. This keeps the hot path (applying thousands of
entity deltas per second) fast.

The decoder assignment logic is in `src/gem/field_decoder.py`. See
[Field Decoders](06_field_decoders.md) for the dispatch chain.

---

## svc_ServerInfo dependency

The `CSVCMsg_ServerInfo` inner message (type 40) carries two values needed for entity
parsing:

- `max_classes` — the maximum number of entity classes. Used to compute
  `classIdSize = floor(log2(max_classes)) + 1`, the bit width for reading class IDs
  from entity packets.
- `game_dir` — path string containing the game build number, e.g. `/dota_v9107/`.

`svc_ServerInfo` arrives inside a `DEM_SignonPacket` **before** `DEM_SendTables`.
gem caches it and applies it immediately after the `EntityManager` is created.

---

## gem API

```python
from gem.stream import DemoStream
from gem.sendtable import parse_send_tables

DEM_SEND_TABLES = 4

with DemoStream("my_replay.dem") as stream:
    for tick, msg_type, data in stream:
        if msg_type == DEM_SEND_TABLES:
            serializers = parse_send_tables(data)
            break

# Inspect a serialiser
s = serializers["CDOTA_Unit_Hero_Axe"]
for f in s.fields:
    print(f.var_name, f.var_type, f.model_name())
```

Source: `src/gem/sendtable.py`, `src/gem/field_decoder.py`
