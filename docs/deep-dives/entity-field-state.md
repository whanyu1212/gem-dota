# How Entities Are Decoded, Part 4: Field State

The first three parts covered the schema, the field paths that say which fields
changed, and the decoders that read each new value. This part covers where those
values go, and how you read them back. Two small modules do this:

- `read_fields()` in `src/gem/schema/field_reader.py` decodes one entity update.
- `FieldState` in `src/gem/schema/field_state.py` holds an entity's values.

Examples come from the committed fixture
`tests/fixtures/ti14_finals_g3_xg_vs_falcons_truncated.dem`, which ends during the
draft.

## One update, start to finish

`read_fields(reader, serializer, state)` decodes one entity update in three steps:

1. **Read every field path** (part 2). The bitstream lists all of an update's
   paths before any of its values.
2. **For each path, find its decoder** by walking the entity's schema (below).
3. **Decode the value** (part 3) **and store it** in the entity's `FieldState`
   at that path.

Nothing marks where one value ends and the next begins, so step 3 must read the
values in exactly the order of the paths.

When an entity is **created**, its class's default values are applied first.
Those defaults, the *baseline*, come from the `instancebaseline` string table in
the same format as an update. gem reads the baseline into the new entity's
`FieldState`, then reads the creation packet's own update on top of it.

## Finding a path's decoder

A path is a list of indexes into the schema tree (part 1). To find its decoder,
gem starts at the entity's class and reads the path one index at a time. The
field's **model** decides what the next index means:

| Model | If the path ends at the field | If the path continues |
|---|---|---|
| simple | the field's decoder | (never happens) |
| fixed-array | (never written) | next index = element; the field's decoder |
| variable-array | the array's **length** (unsigned integer) | next index = element; the element decoder |
| fixed-table | the table's **presence** flag (boolean) | next index = a field of the table's class |
| variable-table | the table's **length** (unsigned integer) | next index = element, then a field of the element's class |

Two real paths from the fixture:

- `(0, 16)` on the game-rules entity: field 0 of `CDOTAGamerulesProxy` is
  `m_pGameRules`, a fixed table of class `CDOTAGameRules`, and field 16 of that
  class is `m_nHeroPickState`. Its decoder is the default unsigned varint.
- `(0, 3, 3)` on `CDOTA_PlayerResource`: field 0 is `m_vecPlayerTeamData`, a
  variable table; `3` picks player slot 3's row; field 3 of the row is
  `m_iKills`.

This walk is the same for every update to a class, so gem does it once per path
and keeps the answer in a per-class cache. On a full 99-minute replay
(`8855242704`), 28 million paths resolved to only 67,456 distinct entries across
500 classes: 99.76% of lookups are a single dictionary hit.

## FieldState: a tree of lists

A `FieldState` is a **tree of Python lists**, the same design as Manta's
`field_state.go`. Each node is a list of slots, and each slot holds a value,
`None` (never sent), or a child node. The path `(0, 16)` means slot 0 of the root,
then slot 16 of the node found there.

```text
game-rules entity
root (8 slots)
└─ [0] m_pGameRules  → node (256 slots, 187 used)
      ├─ [1]  m_iFoWFrameNumber
      ├─ [16] m_nHeroPickState = 12
      └─ ...  36 of the 187 slots are child nodes of their own
```

Nodes start with 8 slots and grow only when a write needs it. Writing index *i*
needs *i* + 2 slots (one spare, as Manta does), and the list grows to
`max(i + 2, 2 × current size)`. So `m_pGameRules`, whose fields fill indexes 0 to
186, grew from 8 to 16, 32, 64, 128, and then 256 slots.

Lists fit because paths are small, dense integers: indexing a list is faster and
smaller than hashing into a dictionary. The trees are also sparse, since a field
that was never sent takes no work at all. At the end of the fixture:

| | Count |
|---|---:|
| Live entities | 113 |
| Nodes | 4,298 (3,647 still at 8 slots; the largest has 512) |
| Slots | 73,064 |
| Stored values | 33,029 (45% of the slots) |

The game-rules entity alone holds 785 values in 60 nodes, nested up to three
levels below the root.

## Tables and arrays in the tree

A table or an array gets its own child node, holding the table's fields or the
array's elements. The field's own slot also receives a value: a table's presence
flag, or an array's length. That value arrives first, and the slot turns into a
node when the first field or element is written. Two rules follow:

- **A value never replaces a node.** Writing to the slot of a table that already
  has fields leaves the fields alone, as in Manta.
- **An array's length resizes it.** A new length is kept on the node, and
  elements at or past it are dropped. This follows Clarity. Arrays really do
  shrink: in the 99-minute replay, `m_vecKnownClearCamps` drops to zero hundreds
  of times, and `CDOTATeam.m_aPlayers` goes from 14 players to 13.

Reading the field's own name gives that value back. An array or variable table
returns its length. A fixed table returns its presence flag as sent, which is
`True` once the table has fields, and can be `False` for a table that has none.

## Reading a value by name

`Entity.get("m_pGameRules.m_nHeroPickState")` works in two steps:

1. **Name to path.** The serializer walks its fields by name (part 1 described
   the naming: dots between levels, four-digit array indexes) and finds
   `(0, 16)`. The result is cached per class, so every entity of the class shares
   it. An unknown name gives `None`.
2. **Path to value.** `FieldState` follows the path through its nodes and returns
   the slot's value, or `None` if the path runs past what was ever written.

The typed getters (`get_int32()`, `get_float32()`, and so on) do the same, then
check the value's type.

## What changed in this update

`read_fields()` also records the paths it just decoded on the `FieldState`. That
is how gem knows *which* fields an update touched, not only their new values.
Some of gem's extractors use it to skip updates that don't touch the fields they
care about. When an entity is created, the recorded paths are the creation
packet's own, not the baseline's.

## Where the time goes

This loop is the busiest code in gem. On the 99-minute replay, `read_fields()`
runs 12.6 million times and makes up about two thirds of the core parse:

| Share of `read_fields()` time (approximate) | |
|---|---:|
| Decoding field paths (part 2) | ~44% |
| Decoding values and running the loop (part 3) | ~43% |
| Writing into `FieldState` | ~12% |

Reads are lighter: a full `gem.parse()` of another long replay (`8974053011`)
made 8.9 million reads for 13.9 million writes. The work is small, fixed-shape
steps repeated millions of times, which makes this loop the natural target for
a native (Rust) version of the parser. A later page covers that plan.

## Try it

A `FieldState` on its own, using the public `get()` and `set()`, which take a
`FieldPath` (part 2):

```python
from gem.schema import FieldPath, FieldState

def fp(*indexes):
    path = FieldPath()
    for i, index in enumerate(indexes):
        path.path[i] = index
    path.last = len(indexes) - 1
    return path

state = FieldState()
state.set(fp(0, 16), 12)                       # a field inside the table at slot 0
print(state.get(fp(0, 16)))                    # 12
print(state.get(fp(0)))                        # True
print(state.get(fp(5, 1)))                     # None

state.set(fp(3), 2)                            # an array's length...
state.set(fp(3, 0), "a")                       # ...and its elements
state.set(fp(3, 1), "b")
state.set(fp(3), 1)                            # the array shrinks
print(state.get(fp(3)), state.get(fp(3, 1)))   # 1 None
```

And the same reads on real entities from the fixture:

```python
from gem.parser import ReplayParser

parser = ReplayParser("tests/fixtures/ti14_finals_g3_xg_vs_falcons_truncated.dem")
parser.parse()   # logs "Replay stream ended early": the fixture is truncated

rules = parser.entity_manager.find_by_class_name("CDOTAGamerulesProxy")
print(rules.get("m_pGameRules.m_nHeroPickState"))            # 12

resource = parser.entity_manager.find_by_class_name("CDOTA_PlayerResource")
print(resource.get("m_vecPlayerTeamData"))                   # 10
print(resource.get("m_vecPlayerTeamData.0003.m_iKills"))     # 0
```

## Where to go next

- [Part 3: Field Decoders](entity-field-decoders.md): how each value is read.
- [Part 1: The Schema](entity-schema.md): the field models and names used here.
- [Field State reference](../reference/field_state.md): `read_fields` and
  `FieldState`.
- Source: `src/gem/schema/field_reader.py`, `src/gem/schema/field_state.py`.
