# gem.state

`gem.state` reconstructs the **live state of a replay** as it plays back: the
table of game entities, the string tables that feed them, and the typed game
events fired along the way.

If `gem.schema` answers *"given these bits and this class, what does each field
decode to?"*, `gem.state` answers *"which entity is this, does it exist yet,
what are its current field values, and what just happened to it?"* It sits
directly above `gem.schema` (it calls `read_fields` to decode field values) and
is driven by `gem.parser`, which feeds it the relevant protobuf messages in
order. `gem.state` does not import `gem.schema`'s callers — the dependency flows
one way: `binary -> schema -> state`.

## Mental Model — Three Coordinating Subsystems

`gem.state` is three subsystems that share data:

```text
string_table.py   key/value tables updated throughout the replay.
                  The critical one is `instancebaseline`: per-class default
                  field values.
        │
        │  instancebaseline feeds entity creation
        ▼
entities.py       the live entity table. On create, an entity is seeded from
                  its class baseline, THEN the packet's own delta is applied.
                  EntityManager owns the table; EntityTracker dispatches
                  create/update/delete events to handlers.

game_events.py    independent: registers a game-event schema, then dispatches
                  typed events (e.g. dota_combatlog) to handlers by name.
```

The non-obvious coupling is between **string tables and entities**: a new
entity's fields don't start empty. They start from the `instancebaseline` entry
for the entity's class, and only then does the packet's delta overwrite the
fields that actually changed. Miss that and decoded entities look half-empty.

## Entity Lifecycle

`CSVCMsg_PacketEntities` carries a sequence of entity updates. Each update is a
2-bit command that `EntityManager.on_packet_entities` decodes into an
`EntityOp`:

```text
cmd  low bit  high bit  meaning   EntityOp
0b00    0        0       update    UPDATED (| ENTERED if it was inactive)
0b10    0        1       create    CREATED | ENTERED
0b01    1        0       leave     LEFT     → entity goes inactive
0b11    1        1       delete    LEFT | DELETED → entity removed from the table
```

The low bit selects create/update (0) vs leave/delete (1); the high bit then
distinguishes the pair.

`EntityOp` is an `IntFlag`, so ops combine (`CREATED | ENTERED`) and you test
them with `op.has(EntityOp.CREATED)`. The create path is where the baseline
coupling lives:

```python
# entities.py — on_packet_entities, create branch
baseline = self.class_baselines.get(class_id)
if baseline and ci.serializer is not None:
    read_fields(BitReader(baseline), ci.serializer, entity._field_state)  # 1. seed from baseline
if ci.serializer is not None:
    read_fields(r, ci.serializer, entity._field_state)                    # 2. apply packet delta
```

Updates apply only the delta. An entity that "leaves" goes inactive but keeps
its state (it can re-enter); a "delete" removes it from the table. Serial
numbers exist so an entity handle can be validated against slot reuse — a slot
index can be recycled, but the serial distinguishes the new occupant from the
old.

## Baseline State

`class_baselines` is a `dict[class_id, bytes]` — the raw, still-bit-packed
baseline payload per class. It is rebuilt by `_update_baselines()`, which is
triggered two ways:

- `on_class_info()` — after `CDemoClassInfo` maps class IDs to serializers.
- `on_baseline_updated()` — after the `instancebaseline` string table is created
  or updated.

So the order that matters at replay start is: class info + the
`instancebaseline` string table must both be present before the first
non-baseline entity packet, or new entities can't be seeded. `gem.parser`
enforces this ordering (string-table messages are prioritized ahead of
`svc_PacketEntities` within a packet); `gem.state` just exposes the
`on_baseline_updated()` hook the parser calls.

## String Tables

`StringTables` is a container of named `StringTable` objects; each table is an
incremental `dict[int, (key, value)]` updated across the replay.

- `parse_string_table(...)` — decodes a table's entries from the bit stream,
  including the **key-history** ring buffer (recent keys are referenced by a
  small back-index instead of being respelled — `_KEY_HISTORY_SIZE = 32`).
- `handle_create(msg, tables)` — handles `CSVCMsg_CreateStringTable` (a new
  table; string data may be Snappy-compressed).
- `handle_update(msg, tables)` — handles `CSVCMsg_UpdateStringTable` (deltas to
  an existing table).

Despite the names, `handle_create`/`handle_update` are not generic event
callbacks — they are the proto-message → `StringTable` converters for those two
specific message types.

The `instancebaseline` table is the one entity decoding depends on; others
(`CombatLogNames`, `EntityNames`, `ActiveModifiers`, …) are consumed elsewhere
in the parser.

## Field Access — Why Entities Have Two Storage Modes

`Entity` stores field values in **two places**, and `Entity.get(name)` checks
them in order:

```text
_state        a plain dict overlay. Checked FIRST. Tests (and any flat lookup)
              can write here directly to bypass schema resolution.
_field_state  the FieldState tree that replay decoding actually writes into,
              addressed by FieldPath. The real source of decoded values.
```

`get("m_iHealth")` returns `_state["m_iHealth"]` if present, otherwise it
resolves the name to a `FieldPath` through the serializer and reads
`_field_state`. Two small caches make the slow path cheap on repeat:

- `_fp_cache` — memoizes `name → FieldPath` so a resolved field isn't re-walked.
- `_fp_noop` — memoizes names that **don't** resolve, so repeatedly asking for a
  field a class doesn't have doesn't re-search the serializer tree every time.

Typed accessors (`get_int32`, `get_float32`, `get_string`, …) wrap `get()` and
coerce. This dual-storage design is why test code can construct an `Entity` and
set `_state` directly without building a full schema.

## Game Events

`game_events.py` is independent of the entity/string-table machinery:

- `GameEventManager.register_schema(...)` ingests `CSVCMsg_GameEventList` — the
  per-event field layout (name → key index + type id).
- `GameEvent` wraps a raw `CSVCMsg_GameEvent` with typed accessors that read
  fields by the registered schema.
- `on_game_event(name, handler)` registers a handler; `dispatch(raw)` routes an
  event to the handlers registered for its name.

The combat log's S1 path (`dota_combatlog`) arrives as a game event, which is
why `gem.combat` registers a handler here.

## What This Package Does Not Do

`gem.state` deliberately does not:

- decode field *values* — it calls `gem.schema.read_fields`; the bit-level value
  decoding lives in `gem.schema.field_decoder`
- read the `.dem` stream or unpack inner packets (that is `gem.binary`)
- know what a field *means* in Dota terms — `m_iHealth` is just an int here;
  attaching meaning is `extractors` / `analysis`
- interpret combat-log or game-event *semantics* — it dispatches typed events;
  `gem.combat` decides what a `dota_combatlog` entry means
- choose high-level parse outputs (`ParsedMatch` assembly is `results`)

If a decoded entity field is *wrong*, the bug is usually in `gem.schema`. If an
entity is missing, half-empty, or attributed to the wrong slot, the bug is
usually here — baseline ordering, the 2-bit command decode, or serial/handle
handling.

## Common Pitfalls

### New entities aren't empty — they're seeded from the baseline

On create, fields are read from the class's `instancebaseline` bytes *before*
the packet delta. If baselines aren't loaded yet (class info or the
`instancebaseline` string table hasn't arrived), new entities decode with
missing fields. This is an ordering bug, not a decoder bug.

### `_field_state` is sparse; `get()` returns `None` for absent fields

An entity only carries the fields that were actually sent. Reading a field a
class doesn't have returns `None` (and is cached in `_fp_noop`). Callers must
tolerate `None` rather than assume every field is present.

### Slot indices are reused — check serials

An entity index can be recycled for a new entity after the old one is deleted.
Code that holds an entity handle across time should validate the serial, not
just the index, or it may read the wrong occupant.

### `handle_create` / `handle_update` are message converters, not event hooks

Their names suggest observer callbacks. They are the
`CSVCMsg_CreateStringTable` / `CSVCMsg_UpdateStringTable` decoders. The actual
observer pattern for entities is `EntityTracker.on_entity(handler)`.

## When To Add Code Here

Add code to `gem.state` when the change is about **what a replay's live state is
at a given moment** — entity lifecycle, baselines, string tables, or game-event
dispatch.

Good fits:

- a fix to entity create/update/delete handling or the 2-bit command decode
- baseline seeding / ordering corrections
- string-table key-history or compression handling
- registering/decoding a new game event

Poor fits:

- decoding a new field *value* type → `gem.schema.field_decoder`
- interpreting a field or event as a Dota concept → `extractors` / `analysis`
- combat-log semantics → `gem.combat`
- outer/inner stream framing → `gem.binary`

When in doubt, keep `gem.state` about *which entity, when, and with what current
values* — and let `gem.schema` own *how a value decodes* and `extractors` own
*what it means*.
