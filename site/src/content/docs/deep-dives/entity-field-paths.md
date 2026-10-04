# How Entities Are Decoded, Part 2: Field Paths

[Part 1](entity-schema.md) described the schema: a tree of classes and fields that
says what every entity looks like. This part covers the first thing an entity
update contains: **which fields changed**.

An update never names its fields. It doesn't even number them directly. Instead it
gives **directions** through the schema tree, using a small set of short commands
such as "next field", "jump ahead 12", or "step into this sub-object". Each position
the directions land on is one changed field. gem decodes these directions in
`src/gem/schema/field_path/`.

This page assumes the crash course's sections on
[bitstreams](../cookbook/bits-and-bytes-primer.md#_4-bitstreams-reading-bits-that-don-t-line-up-with-bytes)
and [prefix codes](../cookbook/bits-and-bytes-primer.md#_8-prefix-codes-short-codes-for-common-things).
Examples come from the committed fixture
`tests/fixtures/ti14_finals_g3_xg_vs_falcons_truncated.dem`, which ends during the
draft, before the game starts.

## What a field path is

A **field path** is a position in the schema tree: a list of up to seven indexes.
Each index picks a field at one level of the tree.

```text
(0,)          field 0 of the entity's class
(0, 67)       field 67 inside field 0 (field 0 is a sub-object)
(0, 67, 1)    element 1 of that field (field 67 is an array)
```

gem keeps the path being built in a `FieldPath` object: a list of 7 integers, plus
`last`, the index of the deepest level in use. It starts as `[-1, 0, 0, 0, 0, 0, 0]`
with `last = 0`, which is "just before field 0".

Decoding an update's paths is a loop:

1. Read one **operation** (a command) from the bitstream.
2. Apply it: it moves the path, sometimes reading a few more bits for a number.
3. If the operation wasn't "finish", the new position is one changed field.
   Record it and go back to step 1.

All of an update's paths come first, followed by all of their values. The values
are covered in the next part.

## A real update, step by step

This is a game-rules update from the fixture, sent during the draft. It changes five
fields using 57 bits of directions: 26 bits of operation codes, plus 31 bits of the
numbers some operations read after their code.

| Bits read | Operation | Path afterwards | Field |
|---|---|---|---|
| `11000` + a number | `PushOneLeftDeltaOneRightNonZero` | `(0, 1)` | `m_pGameRules.m_iFoWFrameNumber` |
| `11010` + a number | `PlusN` | `(0, 16)` | `m_pGameRules.m_nHeroPickState` |
| `11010` + a number | `PlusN` | `(0, 30)` | `m_pGameRules.m_flHeroPickStateTransitionTime` |
| `0` | `PlusOne` | `(0, 31)` | `m_pGameRules.m_iPlayerIDsInControl` |
| `11011001` + two numbers | `PushOneLeftDeltaNRightNonZero` | `(0, 67, 1)` | `m_pGameRules.m_iCaptainPlayerIDs.0001` |
| `10` | `FieldPathEncodeFinish` | (done) | |

Following the first two steps:

- The path starts at `(-1)`. `PushOneLeftDeltaOneRightNonZero` adds 1 to the
  current level (→ 0), then goes down a level and sets it to the number that
  follows (→ 1). The result is `(0, 1)`: field 1 inside field 0, `m_pGameRules`.
- `PlusN` adds *N + 5* to the deepest level. Here N was 10, so `(0, 1)` becomes
  `(0, 16)`.

The fourth field cost a single bit: `PlusOne` ("next field") is by far the most
common operation, so it has the shortest code.

## The 40 operations

Manta's `field_path.go` and gem's `schema/field_path/operations.py` define the same
40 operations, in the same order. They fall into five groups:

| Group | Operations | What they do |
|---|---|---|
| **Move along** | `PlusOne`, `PlusTwo`, `PlusThree`, `PlusFour`, `PlusN` | Add to the deepest index: the next field, or a jump ahead |
| **Go down** | `PushOne…`, `PushTwo…`, `PushThree…`, `PushN` (21 in all) | Optionally move the current level, then go 1, 2, 3 or N levels deeper and set the new indexes |
| **Come back up** | `PopOne…`, `PopAllButOne…`, `PopN…` (8) | Go up one level, back to the top, or up N levels, then move along |
| **Jump anywhere** | `NonTopoComplex`, `NonTopoComplexPack4Bits`, `NonTopoPenultimatePlusOne`, `PushNAndNonTopological`, `PopNAndNonTopographical` | Change indexes at any level, not only the deepest ("non-topological") |
| **Stop** | `FieldPathEncodeFinish` | This update's list of paths is complete |

The long names describe the moves. `PushOneLeftDeltaNRightNonZero` means "push one
level; before pushing, move the current level (left) by N; the new level (right)
starts at a non-zero number".

Several operations read a number after their code. Most use a small variable-width
format, `BitReader.read_ubit_var_fp()`: 1 to 4 selector bits choose a 2-, 4-, 10-,
17-, or 31-bit value, so small numbers stay cheap. The `Pack` variants use a fixed
3-, 4-, 5- or 6-bit number instead.

## The Huffman code

Each operation has a **weight**, Valve's estimate of how often it occurs. `PlusOne`
has 36,271; 16 of the 40 have a weight of 0 (treated as 1). gem builds a Huffman tree
from these weights when it's imported, which gives frequent operations short codes:

| Operation | Code | Bits |
|---|---|---:|
| `PlusOne` | `0` | 1 |
| `FieldPathEncodeFinish` | `10` | 2 |
| `PlusTwo` | `1110` | 4 |
| `PushOneLeftDeltaNRightNonZeroPack6Bits` | `1111` | 4 |
| `PushOneLeftDeltaOneRightNonZero` | `11000` | 5 |
| `PlusN` | `11010` | 5 |
| ... | | |
| 17 rare operations, e.g. `PushThreeLeftDeltaZero` | | 16–17 |

Codes are written in the order the bits are read. The encoder and decoder must build
exactly the same tree, so the weights, their order, and the tie-breaking rule all
matter. gem's 40 codes are identical to the ones Manta's `huffman.go` produces, and
`tests/test_field_path.py` pins every one of them.

How often the operations actually occur depends on the game phase. In the fixture
(the draft), `PlusOne` is 32% of the 92,762 operations, "finish" 31%, and `PlusN`
28%. Most of the 28,559 updates change a single field.

## How gem decodes it quickly

Reading a Huffman code bit by bit means walking the tree one bit at a time, a Python
loop step per bit. gem avoids that with a **lookup table**:

- The longest code is 17 bits. gem builds a table with one entry for every possible
  17-bit value: 131,072 entries.
- Each entry holds the operation whose code those bits start with, and how many bits
  that code really uses. A 1-bit code like `PlusOne` fills half the table: every
  17-bit value whose first bit read is 0.
- To decode, gem looks at the next 17 bits without consuming them, finds the
  operation in one table lookup, and then consumes only that operation's bits.

The loop in `path_sequence.py` does this directly on `BitReader`'s internal bit
cache instead of calling its methods, which saves millions of Python function calls
per replay. Near the end of a stream, where fewer than 17 bits are left, it falls
back to walking the tree. The tests check that the table and the tree agree on real
data and on every code.

## Try it

This builds a bitstream by hand from four operations and decodes it with gem. The
helper packs a string of bits into bytes in the order `BitReader` reads them
(least-significant bit first).

```python
from gem.binary.reader import BitReader
from gem.schema.field_path import read_field_paths

def pack(bits: str) -> bytes:
    bits += "0" * (-len(bits) % 8)
    return bytes(int(bits[i:i + 8][::-1], 2) for i in range(0, len(bits), 8))

PLUS_ONE, PLUS_TWO, FINISH = "0", "1110", "10"
PUSH_ONE_LEFT_DELTA_ONE_RIGHT_ZERO = "11011010"

bits = PLUS_ONE + PLUS_TWO + PUSH_ONE_LEFT_DELTA_ONE_RIGHT_ZERO + PLUS_ONE + FINISH
paths = read_field_paths(BitReader(pack(bits)))
print([p.to_tuple() for p in paths])   # [(0,), (2,), (3, 0), (3, 1)]
```

Starting from `(-1)`: `PlusOne` gives `(0)`; `PlusTwo` gives `(2)`; the push adds 1 to
the top level and starts a new level at 0, giving `(3, 0)`; `PlusOne` gives `(3, 1)`.
Four fields in 16 bits.

## Where this fits

Field paths are the first step of `read_fields` in `schema/field_reader.py`, which
decodes one entity update: first all of its paths, then a value for each path. On a
99-minute replay, decoding field paths takes about a third of the core parse time,
and `read_fields` as a whole about two thirds. That makes this loop the main target
for speeding up the parser, which the last part of this series will cover.

## Where to go next

- [Part 3: Field Decoders](entity-field-decoders.md): how each changed field's new
  value is read.
- [Part 1: The Schema](entity-schema.md): the tree these paths point into.
- [Field Paths reference](../reference/field_path.md): `read_field_paths`,
  `FieldPath`, `FieldPathOp`.
- Source: `src/gem/schema/field_path/` (`operations.py`, `huffman.py`,
  `path_sequence.py`, `models.py`).
