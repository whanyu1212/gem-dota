# How Entities Are Decoded, Part 5: Entity Lifecycle

Parts 1 to 4 followed one entity update from its schema to stored values. This
part steps back to the whole entity table: how entities are created, updated,
and removed, and how the rest of gem hears about it. The code is `EntityManager`
and `EntityTracker` in `src/gem/state/entities.py`.

Examples come from the committed fixture
`tests/fixtures/ti14_finals_g3_xg_vs_falcons_truncated.dem`, which ends during the
draft. Larger numbers come from a full 99-minute replay, `8855242704`.

## The entity packet

All entity changes arrive in `svc_PacketEntities` messages (`CSVCMsg_PacketEntities`
in `netmessages.proto`). gem reads three of its fields:

| Field | Meaning |
|---|---|
| `updated_entries` | how many entity changes the packet holds |
| `legacy_is_delta` | whether the packet only has changes (`True`), or a full snapshot (`False`) |
| `entity_data` | the changes themselves, bit-packed |

`entity_data` is a list of changes, one after another. Each starts with two
things:

1. **Which slot.** Entities live in numbered slots. The packet stores the gap
   from the previous change's slot, minus one, as a `ubit_var`, so a run of
   neighbouring slots costs a few bits each.
2. **What happened.** A 2-bit command:

| Command | Bits (bit 1, bit 0) | What follows |
|---|---|---|
| **update** | `0 0` | the changed fields (parts 2 to 4) |
| **create** | `1 0` | class, serial, spawn group, then the fields |
| **leave** | `0 1` | nothing |
| **delete** | `1 1` | nothing |

In the fixture, 1,188 entity packets carry 113 creates and 28,333 updates. The
full replay has 89,692 packets with 25,258 creates, 23,248 deletes, and 12.6
million updates.

## Creating an entity

A create names the new entity's class and serial, then gives its starting values:

- **Class ID**, a fixed-width number. The width comes from `svc_ServerInfo`,
  which arrives before any entity: the fixture declares 3,171 classes, so class
  IDs take 12 bits (2¹² = 4,096).
- **Serial**, 17 bits. Explained under [handles](#slots-serials-and-handles).
- **Spawn-group handle**, a varint. gem reads and ignores it.
- **The fields**, as an ordinary update.

Most of a new entity's values are its class's defaults, so the packet doesn't
repeat them. They come from the `instancebaseline` string table, which maps each
class ID to an encoded update of default values. The fixture's table has 21
entries, one per class that actually appears; the first is 918 bytes.

To create an entity, gem makes a new `Entity`, applies its class's baseline, then
applies the packet's own fields on top. A class without a baseline is an error
that ends the parse early, with the reason in `parser.parse_error`; Manta stops
too. Building the entity without its defaults would silently leave fields empty.

## Updates, leaves, and deletes

- An **update** applies its fields to the existing entity.
- A **leave** marks the entity inactive (`active = False`) but keeps it and its
  values. In a live game this is an entity going out of the viewer's range.
- A **delete** removes the entity and frees its slot.

gem reports each change as an `EntityOp`, a set of flags:

| Change | Flags |
|---|---|
| create | `CREATED \| ENTERED` |
| update | `UPDATED` (plus `ENTERED` if the entity was inactive) |
| leave | `LEFT` |
| delete | `LEFT \| DELETED` |

Replays of professional matches are recorded with a view of the whole map, so
entities never go out of range: in three full replays (261,000 packets), no
entity left without being deleted, and none was updated while inactive. The
leave and re-enter paths exist for completeness.

## Full packets

Every so often the replay stores a **full packet**: a snapshot of every entity
rather than a list of changes. It lets a replay viewer jump to the middle of a
match. gem reads a replay from start to finish, so it applies the first full
packet, which sets up the world, and skips every later one, because its state is
already current. The fixture has 3 full packets, of which 2 are skipped; the full
replay has 101, of which 100 are skipped. Manta does the same.

## Slots, serials, and handles

There are 16,384 slots, so a slot number fits in 14 bits. When an entity is
deleted its slot is reused for a later entity, which is why each entity also has a
**serial** number, set when it's created.

Entities point at each other with **handles**: one number that packs both,
`serial × 2¹⁴ + slot`. A handle whose serial doesn't match the entity now in that
slot is stale: it pointed at an earlier entity. `EntityManager.find_by_handle()`
checks both parts.

In the fixture, the player controller in slot 1 has `m_hPawn = 2,539,707`, which
is slot 187, serial 155: that player's `CDOTAPlayerPawn`. Its `m_hAssignedHero`
is 16,777,215, the invalid handle, because no hero has been picked yet during
the draft.

## Telling the rest of gem

Code that wants to follow entities registers a handler, a function called with
the entity and its `EntityOp`:

```py
parser.on_entity(lambda entity, op: ...)
```

gem's own extractors register handlers the same way, with internal filters so
they only hear about the classes and fields they need.

**The order matters.** gem applies one change, calls its handlers, then moves
on to the next change in the packet. So a handler that reads *another* entity
sees it with the changes that came earlier in the packet, but not the later
ones. The reference parsers differ here:

| | When handlers run |
|---|---|
| gem | after each entity's change, in packet order |
| Clarity | the same: each change is applied, then reported, in packet order |
| Manta | after the whole packet is applied; each handler then sees every change |

## Cases gem doesn't need

Clarity also handles several situations that gem doesn't. gem checked how often
they happen in three full replays (89,692 + 59,936 + 111,676 packets):

| Situation | Clarity | gem | Times seen |
|---|---|---|---:|
| A create for a slot that's still in use | reports the old entity's leave and delete, or re-creates it | replaces the old entity without reporting it | 0 |
| A leave or delete for an inactive entity | ignores the leave | ends the parse with an error | 0 |
| A list of extra deletions after the last change | reads it | ignores it | 0 |
| Switching to another set of baselines | supports it | ignores it | 0 |
| A delta packet that builds on a tick not reached yet | holds it back until it can apply it | applies it at once | 0 |

None of them occurred in the replays checked, so gem keeps the simpler model.

## Where the time goes

In the core parse of the 99-minute replay, which takes about 106 seconds, the
entity loop runs 12.6 million times:

| | Time |
|---|---:|
| Decoding fields (`read_fields`, parts 2 to 4) | ~74 s |
| The loop itself: reading slots and commands, creating entities | ~15 s |
| Calling handlers, when none are registered | ~4 s |

With gem's extractors attached, calling handlers takes about 23 seconds instead;
84% of changes reach at least one handler. A later page covers how a native
version of this loop could speed it up.

## Try it

```python
from collections import Counter

from gem.parser import ReplayParser
from gem.state import EntityOp

parser = ReplayParser("tests/fixtures/ti14_finals_g3_xg_vs_falcons_truncated.dem")
ops = Counter()
parser.on_entity(lambda entity, op: ops.update([op]))
parser.parse()   # logs "Replay stream ended early": the fixture is truncated

print(ops[EntityOp.CREATED | EntityOp.ENTERED], ops[EntityOp.UPDATED])   # 113 28333

entities = parser.entity_manager
controller = entities.find(1)
pawn = controller.get_uint32("m_hPawn")
print(pawn & 0x3FFF, pawn >> 14)                                      # 187 155
print(entities.find_by_handle(pawn))                                   # Entity(187, 'CDOTAPlayerPawn')
print(entities.find_by_handle(controller.get_uint32("m_hAssignedHero")))   # None
```

## Where to go next

- [Part 4: Field State](entity-field-state.md): where each entity's values are
  stored.
- [Part 1: The Schema](entity-schema.md): the classes that class IDs refer to.
- [Entities reference](../reference/entities.md): `Entity`, `EntityOp`,
  `EntityManager`, `EntityTracker`.
- Source: `src/gem/state/entities.py`.
