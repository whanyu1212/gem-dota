# Reading Entity State

Entities are the game objects inside a replay: heroes, towers, creeps, the game rules
object, runes, wards. Their state changes every tick. This guide shows how to subscribe
to entity events and read field values.

For a conceptual explanation of how the entity system works at the binary level, see
[Understanding: The Entity System](../understanding/08_entity_system.md).

---

## Subscribing to entity events

Register a callback with `parser.on_entity(handler)` before calling `parse()`.
The callback receives `(entity, op)` for every entity event in the replay.

```python
from gem.parser import ReplayParser
from gem.entities import EntityOp

parser = ReplayParser("my_replay.dem")

def on_entity(entity, op):
    print(entity.get_class_name(), op)

parser.on_entity(on_entity)
parser.parse()
```

---

## EntityOp flags

`op` is an `EntityOp` bitmask. Common patterns:

```python
if op & EntityOp.CREATED:
    ...  # entity was just created
if op & EntityOp.UPDATED:
    ...  # one or more fields changed
if op & EntityOp.DELETED:
    ...  # entity was removed
if op & EntityOp.ENTERED:
    ...  # entity became active (accompanies CREATED or a re-activation)
```

`EntityOp.has(other)` is equivalent to `bool(op & other)`.

---

## Reading field values

Every entity exposes typed getter methods. Field names come from the entity class schema
(e.g. `m_iHealth`, `m_flMana`, `m_iGold`).

```python
hp,    ok = entity.get_int32("m_iHealth")
mana,  ok = entity.get_float32("m_flMana")
gold,  ok = entity.get_uint32("m_iGold")
alive, ok = entity.get_bool("m_bIsAlive")
name,  ok = entity.get_string("m_iszUnitName")
```

All typed getters return `(value, ok)`. `ok` is `True` on success, `False` if the field
does not exist or the value is the wrong type.

For quick untyped access:

```python
val = entity.get("m_iHealth")  # returns the raw value, or None
if entity.exists("m_iHealth"):
    ...
```

---

## Filtering by class name

Most callbacks should filter by class name immediately — there are hundreds of entity
classes and you usually only care about a few:

```python
def on_entity(entity, op):
    name = entity.get_class_name()
    if "Hero" not in name:
        return
    # now work with hero entities only
```

Common class name patterns:

| Pattern | Matches |
|---|---|
| `"Hero" in name` | All hero entities |
| `name.startswith("CDOTA_Unit_Hero_")` | Exact hero entity check |
| `name == "CDOTAGamerulesProxy"` | Game rules (time, score, state) |
| `name.startswith("CDOTAPlayerController")` | Per-player state (gold, XP, LH) |
| `"tower" in name.lower()` | Tower entities |
| `name == "CDOTA_Item_Observer_Ward"` | Observer ward entities |
| `name == "CDOTA_Item_Sentry_Ward"` | Sentry ward entities |

---

## Hero position example

Hero map position combines two fields: the **cell** (coarse grid in 512-unit cells)
and the **vector** (fine offset in 0–512 unit range within that cell):

```python
def world_coord(cell: int, vec: float) -> float:
    """Convert cell + vec to world coordinate."""
    return cell * 128.0 + vec - 16384.0

def on_entity(entity, op):
    if not entity.get_class_name().startswith("CDOTA_Unit_Hero_"):
        return

    cell_x, ok1 = entity.get_uint32("CBodyComponent.m_cellX")
    cell_y, ok2 = entity.get_uint32("CBodyComponent.m_cellY")
    vec_x,  ok3 = entity.get_float32("CBodyComponent.m_vecX")
    vec_y,  ok4 = entity.get_float32("CBodyComponent.m_vecY")

    if ok1 and ok2 and ok3 and ok4:
        x = world_coord(cell_x, vec_x)
        y = world_coord(cell_y, vec_y)
        print(f"{entity.get_class_name()} at ({x:.0f}, {y:.0f})")
```

---

## Snapshot at a specific tick

To inspect all entities at a fixed point in time, stop parsing at that tick and query
the entity manager afterwards:

```python
from gem.parser import ReplayParser

parser = ReplayParser("my_replay.dem")
parser.stop_after_tick(6000)   # ~3 minutes into the game
parser.parse()

for entity in parser.entity_manager.all_active():
    if entity.get_class_name().startswith("CDOTA_Unit_Hero_"):
        hp, _ = entity.get_int32("m_iHealth")
        print(f"{entity.get_class_name()}: {hp} HP")
```

---

## Useful entity classes and fields

### Hero entity (`CDOTA_Unit_Hero_*`)

| Field | Type | Meaning |
|---|---|---|
| `m_iHealth` | int32 | Current HP |
| `m_iMaxHealth` | int32 | Maximum HP |
| `m_flMana` | float32 | Current mana |
| `m_flMaxMana` | float32 | Maximum mana |
| `m_iCurrentLevel` | int32 | Hero level |
| `CBodyComponent.m_cellX` | uint32 | Map cell X (coarse) |
| `CBodyComponent.m_cellY` | uint32 | Map cell Y (coarse) |
| `CBodyComponent.m_vecX` | float32 | Map position X (fine) |
| `CBodyComponent.m_vecY` | float32 | Map position Y (fine) |
| `m_hOwnerEntity` | uint32 | Handle to the owning PlayerController |

### PlayerController entity (`CDOTAPlayerController`)

| Field | Type | Meaning |
|---|---|---|
| `m_iGold` | uint32 | Current spendable gold |
| `m_iLastHitCount` | uint32 | Last hit count |
| `m_iDenyCount` | uint32 | Deny count |
| `m_iCurrentLevel` | int32 | Player level |

### Game rules (`CDOTAGamerulesProxy`)

| Field | Type | Meaning |
|---|---|---|
| `CDOTAGamerules.m_fGameTime` | float32 | Current game time in seconds |
| `CDOTAGamerules.m_nGameState` | uint32 | Game state enum |
| `CDOTAGamerules.m_iRadiantScore` | uint32 | Radiant kills |
| `CDOTAGamerules.m_iDireScore` | uint32 | Dire kills |

---

## gem implementation

Source: `src/gem/entities.py`, `src/gem/field_state.py`

`EntityManager.all_active()` returns all currently active entities.
`EntityManager.get_by_handle(handle)` resolves an entity handle.
