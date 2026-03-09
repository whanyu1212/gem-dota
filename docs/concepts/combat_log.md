# Combat Log

The combat log records every meaningful game event: damage dealt, spells
cast, heroes killed, gold earned, items purchased. It's the primary data
source for per-player statistics.

!!! note "Phase 4"
    Combat log extraction is implemented in Phase 4. This page explains
    how it works so you understand what the data means when you use it.

---

## Two ingestion paths

Dota 2 replays come in two formats depending on the game version:

### Source 1 path (older replays)

Combat log events arrive as **game events** — specifically, events named
`dota_combatlog` carried inside `CMsgSource1LegacyGameEvent` messages.
Each event has typed key-value fields, and the unit/ability names are
stored as **integer indices** rather than strings. The actual name strings
live in a string table called `CombatLogNames`.

```
CMsgSource1LegacyGameEvent (type=dota_combatlog)
  type:         6            ← DOTA_COMBATLOG_DEATH
  sourcename:   42           ← index into CombatLogNames → "npc_dota_hero_axe"
  targetname:   17           ← index → "npc_dota_hero_juggernaut"
  inflictor:    0            ← index → "" (no ability, direct attack)
  value:        0
  attackerhero: true
  targethero:   true
```

gem resolves the indices against the string table to give you real names.

### Source 2 path (modern replays)

Combat log events arrive as **user messages** —
`CMsgDOTACombatLogEntry` — with the names already resolved as strings.
No string table lookup needed.

```
CMsgDOTACombatLogEntry
  type:         DOTA_COMBATLOG_DEATH
  attacker_name: "npc_dota_hero_axe"
  target_name:  "npc_dota_hero_juggernaut"
  inflictor_name: ""
  value:        0
  attacker_hero: true
  target_hero:   true
```

gem handles both paths and normalises them into the same
`CombatLogEntry` output, so you don't need to care which version the
replay uses.

---

## Event types

The `DOTA_COMBATLOG_TYPES` enum defines what kind of event each entry
records:

| Type | What it records |
|---|---|
| `DAMAGE` | Damage dealt — source, target, amount, ability |
| `HEAL` | HP restored — source, target, amount |
| `MODIFIER_ADD` | A buff/debuff was applied |
| `MODIFIER_REMOVE` | A buff/debuff expired or was removed |
| `DEATH` | A unit died — killer, victim |
| `ABILITY` | An ability was cast |
| `ITEM` | An item was used |
| `GOLD` | Gold was gained or spent, with a reason code |
| `XP` | Experience was gained, with a reason code |
| `PURCHASE` | An item was purchased |
| `BUYBACK` | A player bought back |
| `KILLSTREAK` | A player reached a kill streak |
| `MULTIKILL` | A player got a multi-kill |
| `GAME_STATE` | Game state changed (e.g. game started, ended) |
| `CONNECT` | A player connected |
| `DISCONNECT` | A player disconnected |

---

## The CombatLogNames string table

In Source 1 replays, the `CombatLogNames` string table is built up
incrementally as new unit/ability names appear. It's a simple index → name
mapping:

```
0  → "npc_dota_hero_axe"
1  → "axe_berserkers_call"
2  → "npc_dota_hero_juggernaut"
3  → "juggernaut_blade_fury"
...
```

The table grows during the replay — names are added as new units/abilities
appear for the first time. gem updates its copy whenever
`CSVCMsg_UpdateStringTable` arrives for `CombatLogNames`.

---

## What a CombatLogEntry looks like

After gem resolves names and normalises both paths, every event becomes
a `CombatLogEntry`:

```python
@dataclass
class CombatLogEntry:
    tick: int
    log_type: str              # "DAMAGE", "DEATH", "ABILITY", ...
    attacker_name: str         # "npc_dota_hero_axe"
    target_name: str           # "npc_dota_hero_juggernaut"
    inflictor_name: str        # ability/item name, or "" for attacks
    value: int                 # damage amount, gold amount, etc.
    attacker_is_hero: bool
    target_is_hero: bool
    attacker_is_illusion: bool
    target_is_illusion: bool
```

---

## Using the combat log

```python
from gem.parser import ReplayParser

parser = ReplayParser("game.dem")
parser.on_combat_log_entry(lambda entry: print(entry))
parser.parse()
```

Example — sum total damage dealt by each hero:

```python
from collections import defaultdict
from gem.parser import ReplayParser

damage_by_hero = defaultdict(int)

def on_entry(entry):
    if entry.log_type == "DAMAGE" and entry.attacker_is_hero:
        damage_by_hero[entry.attacker_name] += entry.value

parser = ReplayParser("game.dem")
parser.on_combat_log_entry(on_entry)
parser.parse()

for hero, total in sorted(damage_by_hero.items(), key=lambda x: -x[1]):
    print(f"{hero}: {total:,} damage")
```

---

## Known limitations and edge cases

### Ward coordinates

The combat log records *who* placed a ward and *when* via `ITEM` events
(`item_ward_observer`, `item_ward_dispenser`, `item_ward_sentry`), but
does not include coordinates.

Exact coordinates come from the entity stream via `CBodyComponent.m_cellX/Y`
and `m_vecX/Y` fields. Two things are required for 100% coverage:

1. **Accept all non-DELETED entity events** — recycled entity slots emit `UPDATED`
   (not `CREATED`) but still carry the full position. Filtering to `CREATED` only
   gives ~35% coverage.
2. **Allow entity records to match multiple placements** — the same slot is reused
   across the game. A greedy matcher that globally consumes records will block later
   placements from matching the same slot.

Matching strategy: for each combat log `ITEM` placement event, find the entity event
with the smallest tick delta within ±60 ticks, without marking records as consumed.
This gives 100% exact coordinates.

Reference: `refs/parser/src/main/java/opendota/processors/warding/Wards.java` uses
`m_lifeState==0` transitions rather than op type — either approach works as long as
both points above are satisfied.

### Smoke of Deceit — empty group edge case

When a hero uses Smoke of Deceit, the combat log fires in sequence:

1. An `ITEM` event (`inflictor_name = "item_smoke_of_deceit"`) — the item is consumed
2. One `MODIFIER_ADD` event per hero that receives the smoke buff
   (`inflictor_name = "modifier_smoke_of_deceit"`, `target_is_hero = True`)

**Empty group**: if the activating hero is standing inside a sentry ward's
truesight radius at the moment they activate, the game engine instantly removes
the smoke. Step 1 fires (item consumed), but step 2 never fires for anyone —
not even the activator. The result is a recorded smoke usage with an empty group.

This is correct game behaviour, not a parsing bug. The item was genuinely wasted.
When you see a smoke event with no heroes in the group, it means the smoke broke
the instant it was activated.

Filter `MODIFIER_ADD` events by `target_is_hero = True` to exclude summoned units
(e.g. Beastmaster boars) from smoke group membership — these receive the modifier
but are not meaningful members of a smoke group.

**Alternative approach**: the `ActiveModifiers` string table carries
`CDOTAModifierBuffTableEntry` protobufs with a `player_ids` field (comma-separated
player slot numbers) for each active modifier. Reading this table directly (as
`refs/clarity` does) would give equivalent results — including an empty `player_ids`
for the instant-break case. This is not currently implemented; it would require
parsing an additional string table of protobuf messages.

### Roshan drop items not in combat log

Aegis of the Immortal, Cheese, Refresher Shard, and Aghanim's Blessing
dropped by Roshan are **not** recorded as `ITEM` log entries when picked
up. Roshan kills themselves are recorded as `DEATH` events
(`target_name = "npc_dota_roshan"`). To track which hero picks up each
drop, use entity state tracking or `CDOTAUserMsg_ItemPurchased`.
