# Reading Entity State

Entities are the game objects inside a replay: heroes, towers, creeps, the game rules
object, runes, wards. Their state changes every tick. This guide shows how to subscribe
to entity events and read field values.

For how entities are created, updated, and removed, and when your handler is called,
see [How Entities Are Decoded, Part 5: Entity Lifecycle](../deep-dives/entity-lifecycle.md).
For where entity parsing fits into the overall pipeline, see
[How Proto Parsing Works](../cookbook/proto-parsing-pipeline.md).

---

## Subscribing to entity events

Register a callback with `parser.on_entity(handler)` before calling `parse()`.
The callback receives `(entity, op)` for every entity event in the replay.

```python
from gem.parser import ReplayParser
from gem.state.entities import EntityOp

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

A deleted entity arrives with `LEFT | DELETED`. Entities in the replays gem was
checked against never leave without being deleted.

`EntityOp.has(other)` is equivalent to `bool(op & other)`.

---

## Reading field values

Every entity exposes typed getter methods. Field names come from the entity class schema
(e.g. `m_iHealth`, `m_flMana`, `m_iCurrentLevel`).

```python
hp    = entity.get_int32("m_iHealth")
mana  = entity.get_float32("m_flMana")
level = entity.get_int32("m_iCurrentLevel")
life  = entity.get_int32("m_lifeState")   # 0 = alive
team  = entity.get_int32("m_iTeamNum")    # 2 = Radiant, 3 = Dire
```

All typed getters return the value, or `None` if the field does not exist or the value
is the wrong type. Guard with `is not None` rather than a truthiness check, since `0`,
`0.0`, and `False` are all valid values:

```python
hp = entity.get_int32("m_iHealth")
if hp is not None:
    ...  # hp is a valid int (possibly 0)
```

For quick untyped access:

```python
val = entity.get("m_iHealth")  # returns the raw value, or None
if entity.exists("m_iHealth"):
    ...
```

To see everything an entity holds, `entity.to_map()` returns every stored value by
the same names.

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
| `name.startswith("CDOTA_Unit_Hero_")` | Hero units |
| `name == "CDOTAPlayerController"` | One per connected player (casters too): owns the player's hero |
| `name == "CDOTA_PlayerResource"` | Per-player kills, deaths, assists, level |
| `name in ("CDOTA_DataRadiant", "CDOTA_DataDire")` | Per-player gold, XP, net worth, last hits |
| `name == "CDOTAGamerulesProxy"` | Game rules: game state, draft, start time |
| `name == "CDOTA_BaseNPC_Tower"` | Towers |
| `name == "CDOTA_NPC_Observer_Ward"` | Placed observer wards |
| `name == "CDOTA_NPC_Observer_Ward_TrueSight"` | Placed sentry wards |

---

## Hero position example

A unit's map position is split into a **cell**, one of a grid of 128-unit squares,
and an **offset** inside that cell, from 0 to 256 (see
[Part 3: Field Decoders](../deep-dives/entity-field-decoders.md#positions-a-cell-plus-an-offset)).
gem's extractors combine them as `cell × 128 + offset`:

```python
def world_coord(cell: int, offset: float) -> float:
    """Combine a cell and its offset into one coordinate, as gem does."""
    return cell * 128.0 + offset

def on_entity(entity, op):
    if not entity.get_class_name().startswith("CDOTA_Unit_Hero_"):
        return

    cell_x = entity.get_uint32("CBodyComponent.m_cellX")
    cell_y = entity.get_uint32("CBodyComponent.m_cellY")
    vec_x  = entity.get_float32("CBodyComponent.m_vecX")
    vec_y  = entity.get_float32("CBodyComponent.m_vecY")

    if None not in (cell_x, cell_y, vec_x, vec_y):
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
parser.stop_after_tick(6000)   # 200 s into the recording, not the game clock
parser.parse()

for entity in parser.entity_manager.all_active():
    if entity.get_class_name().startswith("CDOTA_Unit_Hero_"):
        hp = entity.get_int32("m_iHealth")
        print(f"{entity.get_class_name()}: {hp} HP")
```

---

## Useful entity classes and fields

These names are checked against a full replay from game build 6808.

### Hero entity (`CDOTA_Unit_Hero_*`)

| Field | Meaning |
|---|---|
| `m_iHealth`, `m_iMaxHealth` | Current and maximum HP |
| `m_flMana`, `m_flMaxMana` | Current and maximum mana |
| `m_iCurrentLevel` | Hero level |
| `m_iCurrentXP` | XP towards the next level (resets at each level-up) |
| `m_lifeState` | 0 while alive |
| `m_iTeamNum` | 2 = Radiant, 3 = Dire |
| `CBodyComponent.m_cellX`, `m_cellY` | Map cell (coarse) |
| `CBodyComponent.m_vecX`, `m_vecY` | Offset inside the cell (fine) |
| `m_hOwnerEntity` | Handle to the owning `CDOTAPlayerController` |

### Player controller (`CDOTAPlayerController`)

| Field | Meaning |
|---|---|
| `m_nPlayerID` | Player ID, stored doubled (10 is player 5) |
| `m_hAssignedHero` | Handle to the player's hero; the invalid handle 16,777,215 before a hero is assigned |

### Team data (`CDOTA_DataRadiant`, `CDOTA_DataDire`)

One row per player, `m_vecDataTeam.0000` to `.0004`:

| Field | Meaning |
|---|---|
| `m_vecDataTeam.0000.m_iNetWorth` | Net worth |
| `m_vecDataTeam.0000.m_iTotalEarnedGold` | Gold earned so far (only goes up) |
| `m_vecDataTeam.0000.m_iReliableGold`, `…m_iUnreliableGold` | Spendable gold, in two parts |
| `m_vecDataTeam.0000.m_iLastHitCount`, `…m_iDenyCount` | Last hits and denies |

### Player resource (`CDOTA_PlayerResource`)

| Field | Meaning |
|---|---|
| `m_vecPlayerTeamData.0000.m_iKills`, `…m_iDeaths`, `…m_iAssists` | K/D/A |
| `m_vecPlayerTeamData.0000.m_iLevel` | Hero level |
| `m_vecPlayerTeamData.0000.m_hSelectedHero` | Handle to the selected hero |

### Game rules (`CDOTAGamerulesProxy`)

| Field | Meaning |
|---|---|
| `m_pGameRules.m_nGameState` | Game state enum |
| `m_pGameRules.m_flGameStartTime` | Engine time the game clock started (0 before) |
| `m_pGameRules.m_nTotalPausedTicks` | Ticks spent paused so far |

For the in-game clock, use `match.game_clock` (or `parser.game_time_s` during a parse)
rather than computing it from ticks: ticks keep running during pauses.

---

## gem implementation

Source: `src/gem/state/entities.py`, `src/gem/schema/field_state.py`

`EntityManager.all_active()` returns all currently active entities.
`EntityManager.find_by_handle(handle)` resolves an entity handle.
