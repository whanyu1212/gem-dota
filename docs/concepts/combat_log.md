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

## Using the combat log (Phase 4+)

```python
# Coming in Phase 4
parser.on_combat_log_entry(lambda entry: ...)
```

Example — sum total damage dealt by each hero:

```python
from collections import defaultdict

damage_by_hero = defaultdict(int)

def on_entry(entry):
    if entry.log_type == "DAMAGE" and entry.attacker_is_hero:
        damage_by_hero[entry.attacker_name] += entry.value

parser.on_combat_log_entry(on_entry)
parser.start()

for hero, total in sorted(damage_by_hero.items(), key=lambda x: -x[1]):
    print(f"{hero}: {total:,} damage")
```
