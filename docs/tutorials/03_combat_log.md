# Tutorial 03 · Combat Log

The combat log records every meaningful game event: damage dealt, abilities cast,
heroes killed, gold earned, items used, buffs applied. This tutorial shows how to
subscribe to entries and derive common statistics.

See [concepts/combat_log.md](../concepts/combat_log.md) for a full explanation of
the two ingestion paths (S1 vs S2) and known data limitations.

---

## Basic subscription

```python
from gem.parser import ReplayParser

parser = ReplayParser("game.dem")
parser.on_combat_log_entry(lambda entry: print(entry.log_type, entry.attacker_name))
parser.parse()
```

`on_combat_log_entry` accepts any callable that takes a single `CombatLogEntry`.
Multiple handlers can be registered; all are called for every entry.

---

## Hero damage totals

```python
from collections import defaultdict
from gem.parser import ReplayParser

damage: dict[str, int] = defaultdict(int)

def on_entry(entry):
    if entry.log_type == "DAMAGE" and entry.attacker_is_hero:
        damage[entry.attacker_name] += entry.value

parser = ReplayParser("game.dem")
parser.on_combat_log_entry(on_entry)
parser.parse()

for hero, total in sorted(damage.items(), key=lambda x: -x[1]):
    print(f"{hero}: {total:,} dmg")
```

---

## Hero kill log (hero vs hero only)

```python
kills = []

def on_entry(entry):
    if entry.log_type == "DEATH" and entry.attacker_is_hero and entry.target_is_hero:
        kills.append(entry)

parser.on_combat_log_entry(on_entry)
parser.parse()

for k in kills:
    via = k.inflictor_name or "auto-attack"
    print(f"tick {k.tick:,}  {k.attacker_name}  →  {k.target_name}  [{via}]")
```

!!! note "Filter for hero-vs-hero"
    `attacker_is_hero or target_is_hero` includes creep kills and tower kills.
    Use `attacker_is_hero and target_is_hero` to get hero kill events only.

---

## Ward placements

Ward placements appear as `ITEM` events with specific item names:

| `inflictor_name` | Ward type |
|---|---|
| `item_ward_observer` | Observer |
| `item_ward_dispenser` | Observer (dispenser item plants an observer) |
| `item_ward_sentry` | Sentry |

```python
_WARD_ITEMS = frozenset({
    "item_ward_observer",
    "item_ward_dispenser",
    "item_ward_sentry",
})

ward_placements = []

def on_entry(entry):
    if entry.log_type == "ITEM" and entry.inflictor_name in _WARD_ITEMS:
        ward_placements.append(entry)
```

!!! note "Ward coordinates"
    The combat log records *who* placed a ward and *when*, but not *where*.
    Exact coordinates come from the entity stream: every entity event on a live
    ward carries its position (including `UPDATED` events on recycled slots).
    Match each `ITEM` event to the nearest entity event within ±60 ticks —
    don't filter to `CREATED` only, and allow the same entity slot to match
    multiple placements at different ticks. With this approach, 100% of ward
    placements get exact coordinates.

    See [concepts/combat_log.md](../concepts/combat_log.md#ward-coordinates)
    for full details.

---

## Smoke of Deceit tracking

```python
from gem.combatlog import CombatLogEntry

_SMOKE_ITEM = "item_smoke_of_deceit"
_SMOKE_MODIFIER = "modifier_smoke_of_deceit"

smoke_groups: dict[str, list[str]] = {}  # activator -> group members

def on_entry(entry: CombatLogEntry):
    if entry.log_type == "ITEM" and entry.inflictor_name == _SMOKE_ITEM:
        smoke_groups[entry.attacker_name] = []

    elif (entry.log_type == "MODIFIER_ADD"
          and entry.inflictor_name == _SMOKE_MODIFIER
          and entry.target_is_hero):  # exclude summons
        group = smoke_groups.get(entry.attacker_name)
        if group is not None:
            group.append(entry.target_name)
```

!!! note "Empty smoke groups"
    If a hero activates smoke while already inside a sentry ward's truesight
    radius, the smoke breaks instantly before any `MODIFIER_ADD` fires. The
    `ITEM` event is still recorded (the item was consumed), but the group list
    will be empty. This is correct behaviour — the smoke was wasted on activation.

    Always filter `MODIFIER_ADD` by `target_is_hero = True` to exclude
    non-hero units (e.g. Beastmaster boars) from the group.

---

## Roshan kills

```python
roshan_kills = []

def on_entry(entry):
    if entry.log_type == "DEATH" and entry.target_name == "npc_dota_roshan":
        roshan_kills.append(entry)
        print(f"Roshan killed at tick {entry.tick} by {entry.attacker_name}")
```

!!! note "Aegis and Cheese"
    Roshan drop items (Aegis, Cheese, Refresher Shard, Aghanim's Blessing) are
    **not** recorded as `ITEM` events when picked up. To track them, monitor
    entity state or `CDOTAUserMsg_ItemPurchased`.

---

## Display names with gem.constants

`gem.constants` provides display-name helpers backed by bundled dotaconstants data:

```python
from gem.constants import hero_display, item_display, ability_display

hero_display("npc_dota_hero_axe")          # → "Axe"
item_display("item_blink")                 # → "Blink Dagger"
ability_display("nevermore_shadowraze1")   # → "Shadowraze"
```

These fall back gracefully when a name is not found.

---

## Full working example

See [`examples/extraction_demo.py`](../../examples/extraction_demo.py) for a
complete script covering damage, heals, kills, wards, smokes, gold, and XP.

See [`examples/ward_smoke_rosh.py`](../../examples/ward_smoke_rosh.py) for a
focused script covering ward placements (with coordinates), smoke groups, and
Roshan kill events with respawn windows.
