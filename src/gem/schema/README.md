# gem.schema

`gem.schema` is the part of the parser that turns a replay's **send-table
schema** into concrete **field decoders**, and then uses those decoders to read
**entity field values** out of bit-packed entity-update streams.

If `gem.binary` answers *"where does the next chunk of bytes/bits begin and
end?"*, `gem.schema` answers *"given these bits and this entity's class, what
does each field decode to, and where does it live in the entity's state tree?"*

This package sits directly above `gem.binary` (it consumes `BitReader`) and
directly below `gem.state` (which owns entity lifecycle and string tables and
*calls into* this package to apply updates). `gem.schema` does not import
`gem.state` — the dependency only flows one way.

## Mental Model

Entity decoding is a **two-stage process**:

```text
Stage 1 — build the schema (once, at replay start)
  CDemoSendTables  (a protobuf message)
    -> parse_send_tables()
         -> a tree of Serializer -> Field objects,
            each Field with a decoder function chosen ONCE here

Stage 2 — decode entity updates (many times, every packet)
  bit-packed entity delta
    -> read_field_paths()   : which fields changed (Huffman-coded paths)
    -> read_fields()        : walk each path into the Serializer tree,
                              call that field's decoder, write the value
                              into the entity's FieldState tree
```

The key idea: **a field's decoder is resolved exactly once**, when the send
tables are parsed (Stage 1). At decode time (Stage 2) the parser never re-asks
"what type is this field?" — it already has the decoder attached to the `Field`.
This is why the package is split the way it is: schema-building and value-
decoding are separate concerns that happen at different times.

## The Four Areas

| Area | Module(s) | Role |
|---|---|---|
| **Send tables** | `sendtable/` | Parse `CDemoSendTables` → a `Serializer`/`Field` tree. Assign each field its decoder and field *model* (simple / fixed-array / variable-table / …). |
| **Field paths** | `field_path/` | Decode the Huffman-coded operation stream that says *which* fields in an entity changed, mutating a `FieldPath` cursor. |
| **Field decoders** | `field_decoder/` | The catalog of value decoders (bool, string, varint, quantized float, vectors, angles…) plus the dispatch tables that map a field's declared type to the right one. |
| **Reading + state** | `field_reader.py`, `field_state.py` | `read_fields()` ties it together: walk each decoded field path into the serializer tree, run the field's decoder, and store the result in a `FieldState` tree. |

### `sendtable/`

- `models.py` — `FieldType`, `Field`, `Serializer`, and the `FIELD_MODEL_*`
  constants. A field's *model* (SIMPLE, FIXED_ARRAY, FIXED_TABLE,
  VARIABLE_ARRAY, VARIABLE_TABLE) determines how its field path is interpreted
  during decode — e.g. a variable-table field path addresses into a dynamically
  sized collection.
- `parser.py` — `parse_send_tables()`: builds the serializer tree from the
  protobuf, resolving each field's decoder via `field_decoder`.
- `patches.py` — build-specific corrections to field metadata, applied when a
  particular game build encodes a field differently than its declared type
  implies.

### `field_path/`

Field paths are how an entity update says "field 3, then sub-field 0, then
element 12 changed" without spelling out names. They are Huffman-coded for
compactness.

- `models.py` — `FieldPath`, a small mutable cursor (a list of indices plus a
  position) that operations push/pop/increment.
- `operations.py` — the table of ~40 field-path operations (the canonical
  `FIELD_PATH_OPS`); each operation mutates a `FieldPath`.
- `huffman.py` — the Huffman tree / flat decode table that maps bits → which
  operation to apply. Built once at import time.
- `path_sequence.py` — `read_field_paths()`: the loop that reads operations
  until the path stream terminates, yielding the list of changed paths.

### `field_decoder/`

- `scalar_codecs.py` — individual value decoders (boolean, string, signed/
  unsigned varints, coord/noscale/simulation-time floats, …).
- `composite_codecs.py` — factories for vector and angle decoders.
- `quantized_float.py` — `QuantizedFloatDecoder`, the bit-count/flag-driven
  decoder for Valve's quantized floats.
- `type_resolver.py` — the dispatch tables (`find_decoder`,
  `find_decoder_by_base_type`) that pick a decoder from a field's declared type
  or name.
- `contracts.py` — the typing protocols (`FieldDecoder`, and the `_FieldLike` /
  `_FieldTypeLike` structural protocols). This is a thin module on purpose: it
  exists so the dispatch tables and codecs can share types without an import
  cycle.

### `field_reader.py` and `field_state.py`

- `field_reader.py` — `read_fields()`: the bridge between a decoded list of
  field paths and the actual values. For each path it walks the serializer tree
  (recursing into nested tables), finds the field, calls its decoder against the
  `BitReader`, and writes the value into the entity's `FieldState`.
- `field_state.py` — `FieldState`, the nested **mutable** value tree that mirrors
  manta's structure. It grows lazily (a sparse tree) because most entities only
  touch a handful of their fields per update.

## Public Surface vs Internal Helpers

Each nested package exposes a **facade** `__init__.py`: callers import from
`gem.schema.sendtable`, `gem.schema.field_path`, and `gem.schema.field_decoder`
(or the top-level `gem.schema`), never from the implementation submodules.

`__all__` in each facade lists only the **stable public surface**. Several
underscore-prefixed names are *also* re-exported (e.g. `_parse_field_type`,
`_FIELD_PATCHES`, the `_*_factory` decoder factories, `_QFF_*` flag constants,
the `_FIELD_*` dispatch tables). These are **shared internals** — used by sibling
modules and by tests — and are importable by name, but they are deliberately
kept out of `__all__` so they do not appear as public API. The redundant
`import X as X` aliases on those lines mark them as intentional re-exports.

So when reading a facade: **names without a leading underscore are the contract;
underscore-prefixed re-exports are wiring.**

## What This Package Does Not Do

`gem.schema` deliberately does not:

- read the outer `.dem` stream or unpack inner packet streams (that is
  `gem.binary`)
- own entity creation/update/delete, serial numbers, or handles (that is
  `gem.state.entities`)
- maintain string tables, including the `instancebaseline` table that seeds new
  entities' default field values (that is `gem.state.string_table`)
- interpret what a field *means* in Dota terms — a decoded `m_iHealth` is just an
  integer here; attaching meaning is the job of `extractors` and `analysis`
- decode game events or the combat log (`gem.state.game_events`, `gem.combat`)

Keeping this boundary sharp localizes bugs. If field *values* come out wrong
(off by a quantization step, wrong sign, wrong vector length), the bug is almost
always in `field_decoder` or a `sendtable` patch. If the *wrong field* is being
written, look at `field_path` or `field_reader`'s tree walk.

## Common Pitfalls

### Confusing the two stages

A decoder is chosen at **schema-build** time, not decode time. If a field decodes
incorrectly for one game build, the fix usually belongs in `sendtable/patches.py`
(correct the field's metadata so the right decoder is selected), not in the
decode loop.

### Field models drive field-path interpretation

The same field-path operation means different things depending on the field's
*model*. A `VARIABLE_TABLE` field grows on demand; a `FIXED_ARRAY` does not.
Misclassifying a field's model makes its paths address the wrong slot — which
shows up as values landing in the wrong field, not as a decode error.

### `FieldState` is sparse and mutable

`FieldState` is not a fully-populated dict of every field. It is a lazily grown
tree; a field that was never sent simply is not present. Code reading entity
state must tolerate missing fields rather than assume a dense structure.

### Quantized floats need their flags

`QuantizedFloatDecoder` depends on bit count, low/high bounds, and the `_QFF_*`
encode flags from the field definition. A quantized float read without its flags
(e.g. treated as a plain float) produces plausible-but-wrong values — the kind of
bug that passes a smoke test but corrupts positions/health curves.

## When To Add Code Here

Add code to `gem.schema` when the change is about **how a replay's schema maps to
decoders, or how field values/paths are read**.

Good fits:

- a missing or corrected value decoder (a new Source 2 float/int encoding)
- a `sendtable` patch for a build that encodes a field differently
- a field-path operation or Huffman-table correction
- a fix to how `read_fields` walks nested tables

Poor fits:

- interpreting a decoded field as a Dota concept (gold, position, hero) →
  `extractors` / `analysis`
- entity lifecycle, baselines, or string tables → `gem.state`
- outer/inner stream framing or bit primitives → `gem.binary`

When in doubt, keep `gem.schema` about **schema → decoders → values**, and let
`gem.state` decide *which entity* a value belongs to and *when* it changes.
