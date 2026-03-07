# Tutorial 03 · Entity State

Phase 3 implements the full entity lifecycle: string tables, entity creation/update/delete,
and typed field access. This tutorial shows how to use `ReplayParser` to subscribe to
entity events and read per-tick game state.

---

## Prerequisites

- Phase 1: `DemoStream` — reading outer messages
- Phase 2: `sendtable` — serializer schema

---

## The ReplayParser

`ReplayParser` is the main entry point. It wires together the send-table schema,
string tables, and entity manager, then drives the parse loop.

```python
from gem.parser import ReplayParser

parser = ReplayParser("my_replay.dem")
parser.parse()

em = parser.entity_manager
print(f"Build:       {parser.game_build}")
print(f"Serializers: {len(em.serializers)}")
print(f"Classes:     {len(em.classes_by_id)}")
print(f"Entities:    {len(em.all_active())}")
```

---

## Subscribing to entity events

Register a callback with `on_entity(callback)` before calling `parse()`.
The callback receives `(entity, op)` where `op` is an `EntityOp` bitmask.

```python
from gem.parser import ReplayParser
from gem.entities import EntityOp

parser = ReplayParser("my_replay.dem")

def on_entity(entity, op):
    if op.has(EntityOp.CREATED):
        print(f"created: {entity.get_class_name()} #{entity.get_index()}")
    elif op.has(EntityOp.DELETED):
        print(f"deleted: {entity.get_class_name()} #{entity.get_index()}")

parser.on_entity(on_entity)
parser.parse()
```

### EntityOp flags

| Flag | Meaning |
|---|---|
| `CREATED` | Entity was just created this tick |
| `UPDATED` | One or more fields changed |
| `DELETED` | Entity was removed |
| `ENTERED` | Entity entered the PVS (may accompany CREATED or UPDATED) |
| `LEFT` | Entity left the PVS |

Use `op.has(EntityOp.CREATED)` to test any flag.

---

## Reading field values

Every entity carries a class name and typed field accessors.
Field names come from the send-table schema (e.g. `m_iHealth`, `m_flMana`).

```python
def on_entity(entity, op):
    if "Hero" not in entity.get_class_name():
        return

    hp, ok = entity.get_int32("m_iHealth")
    mana, ok2 = entity.get_float32("m_flMana")

    if ok:
        print(f"{entity.get_class_name()}: HP={hp}, mana={mana if ok2 else '?'}")
```

### Typed getters

All getters return `(value, ok)` — `ok` is `True` on success, `False` if the field
does not exist or has the wrong type.

| Method | Return type |
|---|---|
| `get_int32(name)` | `(int, bool)` |
| `get_uint32(name)` | `(int, bool)` |
| `get_float32(name)` | `(float, bool)` |
| `get_string(name)` | `(str, bool)` |
| `get_bool(name)` | `(bool, bool)` |
| `get(name)` | raw value or `None` |
| `exists(name)` | `bool` |

---

## Stopping early

Use `stop_after_tick()` to limit parsing to the first N ticks — useful for
inspecting game state at a specific moment without reading the full file.

```python
parser = ReplayParser("my_replay.dem")
parser.stop_after_tick(3000)   # ~100 seconds into the game
parser.on_entity(on_entity)
parser.parse()
```

---

## Snapshot at a tick

To capture a full snapshot of all active entities at a given tick:

```python
parser = ReplayParser("my_replay.dem")
parser.stop_after_tick(6000)
parser.parse()

for entity in parser.entity_manager.all_active():
    name = entity.get_class_name()
    if "Hero" in name:
        hp, _ = entity.get_int32("m_iHealth")
        print(f"{name}: {hp} HP")
```

---

## Complete example

See `examples/phase3_entities.py` for a runnable script that prints all hero
and NPC entities created during the first full packet, with their health values.

```bash
uv run python examples/phase3_entities.py path/to/replay.dem
```

Sample output:

```
Parsing: my_replay.dem
  [CDOTA_Unit_Hero_Sven] m_iHealth=670
  [CDOTA_Unit_Hero_Bane] m_iHealth=670
  [CDOTA_Unit_Hero_Pugna] m_iHealth=632
  ...

Game build:        9107
Serializers:       3223
Classes:           3171
String tables:     18
Active entities:   113
```
