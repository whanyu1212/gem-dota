# Field Paths & Huffman Coding

When an entity is updated, the payload does not send a full copy of every field. It
sends a list of **(field path, value)** pairs — only the fields that changed. A
**field path** is a compact address into the entity's field tree, and these addresses
are Huffman-coded for maximum compression.

---

## What a field path is

An entity's fields are organised in a hierarchy. Top-level fields are at depth 0; nested
sub-serialiser fields are at depth 1, 2, etc. A field path is an array of up to 7
integers, each indexing one level of the hierarchy:

```
Entity: CDOTA_Unit_Hero_Axe
  field [0]:  m_iTeamNum        (simple int)
  field [1]:  m_iHealth         (simple int)
  field [2]:  m_flMana          (quantized float)
  field [3]:  CBodyComponent    (sub-serialiser)
    field [0]: m_cellX          (uint32)
    field [1]: m_cellY          (uint32)
    field [2]: m_vecX           (float)
    ...

Path [1]       → m_iHealth
Path [3, 0]    → CBodyComponent.m_cellX
Path [3, 2]    → CBodyComponent.m_vecX
```

The path always starts at the root of the serialiser.

---

## Initial state and mutation

Field paths are decoded **incrementally** within a single entity packet. The path
starts at `[-1, 0, 0, 0, 0, 0, 0]` with `last = 0` (the index of the last active
element). A sequence of **operations** mutates the current path state. When the
sequence ends, you have read all the (path, value) pairs for this entity.

Each operation is read from the bit stream as a **Huffman code** and executed
immediately. Operations may:

- Increment one or more path elements by a fixed amount
- Push a new level (go one level deeper into a sub-serialiser)
- Pop one or more levels
- Advance a specific element by a delta read from subsequent bits

---

## The 40 operations

There are exactly 40 operations, each identified by an index 0–39. They are named
descriptively, e.g.:

| Op | Name | What it does |
|---|---|---|
| 0 | `PlusOne` | Increment the last element by 1 |
| 1 | `PlusTwo` | Increment the last element by 2 |
| 2 | `PlusThree` | Increment the last element by 3 |
| 3 | `PlusFour` | Increment the last element by 4 |
| 4 | `PlusN` | Read 3 bits → increment last element by (n+5) |
| 5 | `PushOneLeftDeltaZeroRightZero` | Push new level; last element unchanged |
| 6 | `PushOneLeftDeltaZeroRightNonZero` | Push; read 3 bits for new element delta |
| 7 | `PushOneLeftDeltaOneRightZero` | Push; increment by 1 at new level |
| ... | ... | ... |
| 39 | `FieldPathEncodeFinish` | End of field path list for this entity |

`PlusOne` is by far the most common operation (weight 36271) because successive
fields are usually updated together. It gets the shortest Huffman code.

The full list is in `src/gem/field_path.py`, translated from
`refs/manta/field_path.go`.

---

## Huffman coding

Huffman coding assigns shorter bit sequences to more frequent symbols. The 40 operations
have pre-defined **weights** (frequencies observed across many replays). gem builds a
Huffman tree from these weights once at startup and uses it for every entity decode.

Weight table excerpt (highest to lowest frequency):

```
PlusOne                   36271
FieldPathEncodeFinish     25474
PushOneLeftDeltaOneRightZero   10334
PlusN                      4128
...
NonTopologicalConsecutive   1
```

In a Huffman tree, the most frequent symbol (`PlusOne`, weight 36271) gets the shortest
code — typically 1 or 2 bits. The rarest symbols get codes up to 17 bits long.

---

## O(1) decode table

Walking a Huffman tree bit-by-bit is slow (one branch per bit). gem uses a **flat
17-bit decode table** instead: peek the next 17 bits from the stream, use them as an
index into a 131072-entry table, and get back `(op_index, bits_consumed)` in O(1).

```python
# Pseudo-code for the decode loop
while True:
    bits = reader.peek_bits(17)
    op_index, consumed = DECODE_TABLE[bits]
    reader.skip_bits(consumed)
    execute_op(op_index, path)
    if op_index == FINISH_OP:
        break
```

The table is built once in `src/gem/field_path.py` at module load time.

---

## Reading a full entity delta

The complete sequence for one entity update:

```
1. Read paths until FieldPathEncodeFinish fires:
   a. Peek 17 bits → look up (op, bits_consumed) → skip those bits → mutate path
   b. Repeat

2. For each path collected:
   a. Navigate the serialiser tree using the path indices
   b. Call the field's decoder(bit_reader) → value
   c. Store the value in the entity's FieldState

3. Fire EntityTracker callbacks
```

The serialiser navigation uses the path indices to walk the `Serializer.fields` list.
For arrays (`FIXED_ARRAY`, `VARIABLE_ARRAY`), path[depth+1] is the element index.
For sub-serialisers (`FIXED_TABLE`, `VARIABLE_TABLE`), path[depth+1] is the field index
within the sub-serialiser.

---

## gem implementation

Source: `src/gem/field_path.py`

The `FieldPath` class uses `__slots__` for performance (it is allocated for every entity
update). The `read_field_paths(reader, serializer)` function returns a list of
`(FieldPath, Field)` pairs, ready for decoding.

The Huffman decode table (`_HUFFMAN_TABLE`) is a pre-built `list[tuple[int, int]]` of
131072 entries, one per 17-bit bit-pattern.

Reference: `refs/manta/field_path.go`
