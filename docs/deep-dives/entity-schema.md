# How Entities Are Decoded, Part 1: The Schema

Almost everything gem reports comes from **entities**: the game objects the server
tracks, such as heroes, creeps, towers, items, wards, and the game rules. The server
never sends "Axe has 620 health" as text. It sends packed bitstreams that say, in
effect, "entity 312, field 17, new value 620". To make sense of that, you need to
know what field 17 of entity 312 *is*, and how its value was packed.

That knowledge is the **schema**. The replay sends it once, before any entity
update, in the `DEM_SendTables` envelope. This page explains what it contains and
how gem turns it into the tree of classes and fields that everything else relies
on.

This is part 1 of a series that follows an entity update from raw bits to Python
values. It assumes the ideas in the
[Bits & Bytes crash course](../cookbook/bits-and-bytes-primer.md) (bit counts,
quantized floats) and the layers in
[How Proto Parsing Works](../cookbook/proto-parsing-pipeline.md).

Every number on this page comes from the replay fixture committed to the repo,
`tests/fixtures/ti14_finals_g3_xg_vs_falcons_truncated.dem` (game build 6559), so
you can reproduce all of it.

## What the schema is

Think of the schema as a catalogue of object types. For every kind of entity it
lists the fields, in order, and says how each field's value is stored:

- its **name**, such as `m_iHealth`
- its **type**, such as `int32`, `float32`, or `CNetworkUtlVectorBase< CHandle< CBaseEntity > >`
- how it is **encoded**: a bit count, a value range, or a named encoder such as
  `coord` or `simtime`

Entity updates carry none of this. They only say "field number *n* changed" and
then give the packed value. Without the schema, the update is just bits; with it,
gem knows that field *n* is `m_flMana` and that its value is a 20-bit quantized
float between 0 and 65,536.

In the fixture, the schema is an 800 KB message holding:

| Part | Count | What it is |
|---|---:|---|
| Serializers | 3,234 | One per entity class (and class version), e.g. `CDOTA_Unit_Hero_Axe` |
| Field definitions | 2,008 | One per distinct field, e.g. `m_flMana` as a 20-bit float |
| Symbols | 5,423 | Every name and type string, each stored once |

`CDOTA_Unit_Hero_Axe` alone has 178 fields.

## Why it's called "flattened"

The schema arrives as a `CSVCMsg_FlattenedSerializer` protobuf message (defined in
`netmessages.proto`). "Flattened" means it works like a normalised database:

- **Symbols** are a list of strings. Everything else refers to a name by its
  position in this list.
- **Field definitions** are a list of records. Each record stores symbol numbers
  for its name and type, plus its encoding settings.
- **Serializers** are classes. Each is a name, a version, and a list of field
  definition numbers.

Many classes share the same fields. Every hero has `m_flMana`, but it is defined
once and referenced by number from each hero class. gem builds each field once and
reuses it: the fixture's 1,995 `Field` objects fill 217,881 field slots across all
the classes.

Here is the raw record for `m_flMana`, followed by what it means:

```text
var_type_sym: 3249     -> symbols[3249] = "float32"
var_name_sym: 3734     -> symbols[3734] = "m_flMana"
bit_count: 20          -> store the value in 20 bits
high_value: 65536      -> ... spread over 0 to 65,536
                          (low_value is absent, so the range starts at 0)
```

That is enough to decode mana: read 20 bits and scale them into the range, as in the
[quantized floats section](../cookbook/bits-and-bytes-primer.md#_7-floats-and-how-to-store-them-in-fewer-bits)
of the crash course.

## From protobuf to gem's objects

`parse_send_tables()` in `gem/schema/sendtable/parser.py` turns the message into
a dictionary of `Serializer` objects, keyed by class name. Each `Serializer` has a
`name`, a `version`, and an ordered list of `Field` objects. A `Field` keeps the
raw metadata (`var_name`, `var_type`, `encoder`, `bit_count`, `low_value`,
`high_value`) and adds what gem works out from it:

| Attribute | Meaning |
|---|---|
| `field_type` | The type string parsed into parts (see below) |
| `serializer` | For a field that is itself an object, the `Serializer` it contains |
| `model` | Which of five shapes the field has (see below) |
| `decoder` | The function that reads this field's value from the bitstream |

The decoder is chosen **once, while the schema is built**, not for every update.
Deciding "20-bit quantized float, 0 to 65,536" happens once per field per replay,
and the result is reused for every one of the millions of updates that follow.

Building each field takes five steps:

1. Look up its name, type, and encoder in the symbol list.
2. Parse the type string.
3. If the field is an object, link it to that object's `Serializer`.
4. Apply any build-specific patches (see below).
5. Choose its model and decoder.

gem creates every `Serializer` first and fills in their fields second, so a field
can refer to a class declared later in the message. Real replays never do this,
but the two passes cost nothing.

## Field types

Type strings are C++-style and are parsed into four parts:

| Type string | Base type | Generic type | Pointer | Count |
|---|---|---|---|---|
| `int32` | `int32` | | | |
| `uint32[1]` | `uint32` | | | 1 |
| `CEntityIdentity*` | `CEntityIdentity` | | yes | |
| `CNetworkUtlVectorBase< CHandle< CBaseEntity > >` | `CNetworkUtlVectorBase` | `CHandle<CBaseEntity>` | | |

A few array sizes are engine constants rather than numbers, such as
`MAX_ABILITY_DRAFT_ABILITIES`. gem knows two of them. Any other name gets a size of
1,024, as Manta does. The size is only an upper bound, because updates address
array elements by index.

## The five field models

Every field gets one of five **models**, its shape. The model decides how the next
stages walk into the field, so getting it wrong would make updates land in the
wrong place.

| Model | Shape | Example in the fixture | Field slots |
|---|---|---|---:|
| **simple** | One value | `m_iHealth` (`int32`), `m_flMana` (`float32`) | 207,564 |
| **fixed-table** | An embedded object, always present | `CBodyComponent` → the `CBodyComponentBaseAnimatingOverlay` class (25 fields, including position and rotation) | 6,914 |
| **variable-array** | A list of values that can grow and shrink | `m_hItems` (Axe's inventory, a list of item handles) | 1,882 |
| **fixed-array** | A list with a fixed number of values | `m_bvDisabledHitGroups` (`uint32[1]`) | 1,058 |
| **variable-table** | A list of objects that can grow and shrink | `m_vecPlayerTeamData` on `CDOTA_PlayerResource`: one 63-field object per player | 463 |

The rules, in order:

1. The field links to a serializer: a **fixed-table** if its type is a pointer or
   one of a few known component types (`CBodyComponent`, `CEntityIdentity`, …),
   otherwise a **variable-table**.
2. The type has a count, and isn't a `char` string: a **fixed-array**.
3. The base type is `CUtlVector` or `CNetworkUtlVectorBase`: a **variable-array**.
4. Anything else: **simple**.

These are exactly Manta's rules (`sendtable.go`).

## Nesting, and how nested fields are named

Tables make the schema a tree. A hero's position isn't a field of the hero class
directly: it lives inside its `CBodyComponent`, whose own class has fields such as
`m_cellX`, `m_vecX`, and `m_angRotation`. A list of objects adds an index level.

gem names nested fields with dots, and array or table indexes as four-digit numbers:

```text
CBodyComponent.m_cellX
m_vecPlayerTeamData.0003.m_iKills      (player slot 3's kills)
m_hItems.0000                          (the first inventory slot)
```

These are the names you pass to `Entity.get_int32()`, `get_float32()`, and so on.

## Versions

A class can appear more than once with different versions. The fixture has four
such classes, all body components; `CBodyComponentBaseAnimatingOverlay` has
versions 0 to 4. Each field that contains an object records both the class name and
the version it wants. Axe's `CBodyComponent` asks for version 1, so gem links it to
version 1.

gem matches the exact name and version. Manta instead uses the latest version of
that name seen so far in the message. Valve declares each version just before it
is used, so both rules pick the same class for every reference in real replays.

## Build patches

A few old game builds sent incomplete or inconsistent field metadata. gem fixes
those fields before choosing their decoders, using the same four patches as Manta
(`field_patch.go`):

| Builds | What the patch does |
|---|---|
| up to 990 | Adds missing encoder hints: angles become `QAngle` (or `qangle_pitch_yaw` inside `CBodyComponentBaseAnimatingOverlay`), certain positions `coord`, and `m_vecLadderNormal` `normal` |
| up to 954 | Sets mana's range to 0–8,192 (old builds stored it that way) |
| 1016 to 1027 | Reads some 64-bit IDs and bitfields as `fixed64` |
| all builds | Gives `m_flSimulationTime` and `m_flAnimTime` the `simtime` encoder, and `m_flRuneTime` the `runetime` encoder (313 field slots in the fixture) |

The build number comes from the `svc_ServerInfo` message, in its `game_dir` path
(for example `.../dota_v6559/dota`). It must be known **before** the schema is
parsed, or the wrong patches apply. gem once got this wrong: it passed build 0,
which counts as "up to 954", so modern replays got the old mana range and every
mana value came out at one eighth of its real value. `svc_ServerInfo` arrives a few
envelopes before `DEM_SendTables`, and gem now records the build as soon as it does,
as Manta does.

## Explore the schema yourself

Run this from the repository root. The fixture is truncated, so the parser logs a
"Replay stream ended early" warning when it reaches the end; that is expected.

```python
from collections import Counter

from gem.parser import ReplayParser

parser = ReplayParser("tests/fixtures/ti14_finals_g3_xg_vs_falcons_truncated.dem")
parser.stop_after_tick(0)       # the schema arrives before tick 1
parser.parse()

schema = parser.entity_manager.serializers
print(parser.game_build)                        # 6559
print(len(schema))                              # 3223  (unique class names)

axe = schema["CDOTA_Unit_Hero_Axe"]
print(axe)                                      # Serializer('CDOTA_Unit_Hero_Axe', v0, 178 fields)

mana = next(f for f in axe.fields if f.var_name == "m_flMana")
print(mana.var_type, mana.bit_count, mana.high_value, mana.model_name())   # float32 20 65536.0 simple

print(Counter(f.model_name() for f in axe.fields))   # Counter({'simple': 167, 'variable-array': 5, 'fixed-table': 4, 'variable-table': 1, 'fixed-array': 1})

body = next(f for f in axe.fields if f.var_name == "CBodyComponent")
print(body.serializer)                          # Serializer('CBodyComponentBaseAnimatingOverlay', v1, 25 fields)
print([f.var_name for f in body.serializer.fields[:6]])   # ['m_cellX', 'm_cellY', 'm_cellZ', 'm_vecX', 'm_vecY', 'm_vecZ']
```

Reading a nested field needs entities, which arrive a little later:

```python
parser = ReplayParser("tests/fixtures/ti14_finals_g3_xg_vs_falcons_truncated.dem")
parser.parse()                                  # the whole truncated fixture

resource = parser.entity_manager.find_by_class_name("CDOTA_PlayerResource")
print(resource.get_int32("m_vecPlayerData.0003.m_iPlayerTeam"))   # 2  (Radiant)
```

## Performance

Building the schema is cheap: about 0.07 s, once per replay. It is not a target for
optimisation. Its *output* matters more: the models and decoders chosen here drive
the per-update decoding loop that dominates parse time, and any future native
(Rust) decoder would have to consume this schema. See
[Final Python parser profile](parser-profile-2026-09.md).

## Where to go next

- [How Proto Parsing Works](../cookbook/proto-parsing-pipeline.md), Stage 6: where
  entity updates sit in a replay.
- [Send Tables reference](../reference/sendtable.md): `parse_send_tables`,
  `Serializer`, `Field`, and `FieldType` signatures.
- Source: `src/gem/schema/sendtable/` (`parser.py`, `models.py`, `patches.py`).
