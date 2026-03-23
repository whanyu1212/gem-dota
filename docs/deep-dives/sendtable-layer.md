# SendTable Layer

This page explains `src/gem/sendtable.py`, the schema-construction layer.

Prerequisites:

1. [Bits & Bytes Primer](../cookbook/bits-and-bytes-primer.md)
2. [Stream Layer (`stream.py`)](stream-layer.md)
3. [Parser Layer (`parser.py`)](parser-layer.md)

## Where this layer sits

`sendtable.py` runs when parser receives outer `DEM_SendTables`.

Its job is to convert raw send-table payloads into a runtime schema:

```python
dict[str, Serializer]
```

That schema is then used by `entities.py` to decode field deltas.

## Input and output

Input:

- bytes from `CDemoSendTables` outer payload (`data: bytes`)
- optional `game_build` for build-specific patches

Output:

- mapping of serializer name -> `Serializer`
- each serializer contains ordered `Field` definitions with decoders wired

## Constants explained

| Constant | Value | Meaning | Why it matters |
|---|---|---|---|
| `_POINTER_TYPES` | set of type names | Known embedded-by-pointer types in Source 2 schema. | Forces fixed-table modeling for these fields. |
| `_ITEM_COUNTS` | e.g. `MAX_ITEM_STOCKS: 8` | Engine array-size symbols -> numeric counts. | Converts symbolic array lengths into concrete sizes. |
| `FIELD_MODEL_SIMPLE` | `0` | Scalar field model. | Direct single-value decode path. |
| `FIELD_MODEL_FIXED_ARRAY` | `1` | Fixed-length array model. | Decoder applies repeated element decode with known length. |
| `FIELD_MODEL_FIXED_TABLE` | `2` | Pointer-like nested table model. | Nested serializer with fixed presence model. |
| `FIELD_MODEL_VARIABLE_ARRAY` | `3` | Variable-length array model. | Needs length prefix + child element decoder. |
| `FIELD_MODEL_VARIABLE_TABLE` | `4` | Variable nested table model. | Nested serializer with variable instances. |
| `_FIELD_TYPE_RE` | regex | Parses C++-style type strings (generic/pointer/array). | Turns raw type text into structured `FieldType`. |

## Core data structures

### `FieldType`

Represents parsed type metadata from strings like:

- `uint32`
- `CUtlVector< int32 >`
- `CHandle[24]`
- `CBodyComponent*`

Fields:

1. `base_type`
2. `generic_type`
3. `pointer`
4. `count`

### `Field`

Represents one property in a serializer schema.

Key things it carries:

1. name/type metadata (`var_name`, `var_type`, encoder hints)
2. linked nested serializer (if any)
3. field model (`simple`, `fixed-array`, etc)
4. concrete decoder functions selected by `set_model(...)`

`set_model` is the bridge from schema metadata to actual decode behavior.

### `Serializer`

Container for one class schema:

1. `name`
2. `version`
3. ordered `fields`

`entities.py` depends on this order for field path resolution and field-state decode.

## Build-range patch subsystem

`sendtable.py` includes patch hooks to match known build-specific quirks.

Patch components:

1. `_FieldPatch(min_build, max_build, patch_fn)`
2. `_make_patches()` defines patch rules
3. `active_patches` selected by `game_build`

Examples of patched behavior:

- force encoder hints (`coord`, `normal`, `QAngle`, `simtime`, `runetime`)
- adjust special ranges (example: mana max for old builds)
- patch 64-bit encoded fields in specific build windows

Why patches exist:

- replay schema can be inconsistent across game builds
- these patches normalize behavior to keep decode parity with reference parsers

## `parse_send_tables(...)` step-by-step

Core flow:

1. Parse outer protobuf `CDemoSendTables`.
2. Read varuint length prefix in `outer.data`.
3. Parse inner `CSVCMsg_FlattenedSerializer` payload.
4. Build symbol table (`msg.symbols`) for string lookups.
5. Select active build patches.
6. Build caches:
   - type cache (`str -> FieldType`)
   - field cache (`field_index -> Field`)
7. Iterate each serializer in protobuf and populate `Serializer.fields`.
8. For each field:
   - resolve symbol-backed names/types/encoders
   - parse `FieldType`
   - resolve nested serializer (if known)
   - apply active patches
   - choose model + wire decoder(s)
9. Return final serializer mapping.

## Field model decision logic

Decision order in code:

1. If field has nested serializer:
   - pointer / pointer-type -> `FIELD_MODEL_FIXED_TABLE`
   - otherwise -> `FIELD_MODEL_VARIABLE_TABLE`
2. Else if `count > 0` and not `char` -> `FIELD_MODEL_FIXED_ARRAY`
3. Else if base type is vector container (`CUtlVector`, `CNetworkUtlVectorBase`) -> `FIELD_MODEL_VARIABLE_ARRAY`
4. Else -> `FIELD_MODEL_SIMPLE`

This decision is critical because `entities.py` decode path depends on model shape.

## Real output snapshot

Using fixture `tests/fixtures/8520014563.dem`:

```text
serializer_count 3224
0 CEntityIdentity 0 1
1 CBodyComponentBaseAnimating 2 28
2 CRenderComponent 0 0
3 CDestructiblePartsSystemComponent 0 3
4 EntityRenderAttribute_t 0 2
sample_field CEntityIdentity m_nameStringableIndex int32 simple
```

How to read it:

1. Total serializers available for replay decode.
2. Each serializer has version + field count.
3. Sample field shows resolved name, type, and chosen model.

## What can go wrong at this layer

1. Wrong symbol/type parsing -> decoders wired to wrong model.
2. Missing/incorrect build patch -> subtle field decode drift.
3. Wrong nested serializer linkage -> broken table/array path decode.

Symptoms usually appear later as entity fields being wrong or missing.

## Next page

- [State Reconstruction Layer (`string_table.py` + `entities.py`)](state-layer.md)
