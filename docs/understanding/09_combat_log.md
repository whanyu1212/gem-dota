# The Combat Log

The combat log is the primary source of game event data: damage dealt, spells cast,
heroes killed, gold earned, items used, buybacks. It does not come from the entity
stream — it arrives through its own channels, with two different formats depending on
the replay version.

---

## Two ingestion paths

### S1 path — older replays

Combat log events arrive as **game events** named `dota_combatlog`, carried inside
`CMsgSource1LegacyGameEvent` messages (inner message type 45 or 46). Each event is a
typed key-value record where **unit and ability names are integer indices** rather than
strings. The actual strings live in the `CombatLogNames` string table (see
[String Tables](07_string_tables.md)).

Example: a hero kill event in S1 format:

```
CMsgSource1LegacyGameEvent (event name: dota_combatlog)
  type:         6         ← DOTA_COMBATLOG_DEATH
  sourcename:   42        ← index into CombatLogNames → "npc_dota_hero_axe"
  targetname:   17        ← index → "npc_dota_hero_juggernaut"
  inflictor:    0         ← index → "" (direct attack, no ability)
  value:        0
  attackerhero: 1         ← attacker is a hero
  targethero:   1         ← target is a hero
```

gem resolves the indices against the current `CombatLogNames` table at event time.

### S2 path — modern/HLTV replays

Combat log events arrive as inner messages of type **554** (`DOTA_UM_CombatLogDataHLTV`).
Each message is a `CMsgDOTACombatLogEntry` protobuf with names **already resolved as
strings** — no string table lookup needed.

The same kill event in S2 format:

```
CMsgDOTACombatLogEntry (inner type 554)
  type:           DOTA_COMBATLOG_DEATH
  attacker_name:  "npc_dota_hero_axe"
  target_name:    "npc_dota_hero_juggernaut"
  inflictor_name: ""
  value:          0
  attacker_hero:  true
  target_hero:    true
```

gem handles both paths and normalises them into the same `CombatLogEntry` output.

---

## CombatLogEntry

After normalisation, every event becomes a `CombatLogEntry` dataclass:

```python
@dataclass
class CombatLogEntry:
    tick: int
    log_type: str               # see table below
    attacker_name: str          # "npc_dota_hero_axe"
    target_name: str            # "npc_dota_hero_juggernaut"
    inflictor_name: str         # ability/item name, or "" for attacks
    value: int                  # damage amount, gold amount, etc.
    attacker_is_hero: bool
    target_is_hero: bool
    attacker_is_illusion: bool
    target_is_illusion: bool
    attacker_team: int          # 2 = Radiant, 3 = Dire
    target_team: int
```

---

## Log types

The `log_type` field is a string label from `DOTA_COMBATLOG_TYPES`:

| Type | What it records |
|---|---|
| `DAMAGE` | Damage dealt — attacker, target, amount, ability |
| `HEAL` | HP restored — source, target, amount |
| `MODIFIER_ADD` | A buff or debuff was applied |
| `MODIFIER_REMOVE` | A buff or debuff expired or was removed |
| `DEATH` | A unit died — killer and victim |
| `ABILITY` | An ability was cast |
| `ITEM` | An item was used (includes ward placements) |
| `GOLD` | Gold gained or spent, with a reason code in `value` |
| `XP` | Experience gained, with a reason code |
| `PURCHASE` | An item was purchased |
| `BUYBACK` | A player bought back; `value` is the player slot |
| `KILLSTREAK` | A kill streak milestone |
| `MULTIKILL` | A multi-kill |
| `GAME_STATE` | Game state transition (game started, ended) |
| `CONNECT` | Player connected |
| `DISCONNECT` | Player disconnected |

---

## Derived economy stats

Some economy metrics are reconstructed during match assembly rather than read
directly from raw combat-log payloads:

- **Buyback gold cost** is derived in `match_builder` using
  `floor(200 + net_worth / 13)`.
- **Laning efficiency** is computed against a fixed 10-minute baseline of
  `4948` gold.

---

## Ward placements

Ward placements appear as `ITEM` events with specific inflictor names:

| `inflictor_name` | Ward type |
|---|---|
| `item_ward_observer` | Observer ward placed |
| `item_ward_dispenser` | Observer ward (dispenser variant) |
| `item_ward_sentry` | Sentry ward placed |

The combat log records **who** placed the ward and **when**, but **not where**.
Coordinates must be obtained from the entity stream — see
[Guide: Reading Entity State](../guides/02_entity_state.md) for how.

**100% coverage requires:**

1. Accept all non-DELETED entity events (not just `CREATED`) — recycled entity slots
   emit `UPDATED` but still carry the full position.
2. Do not globally consume entity records in the matcher — the same slot is reused
   across the game. For each combat log `ITEM` event, find the entity event with the
   smallest tick delta within ±60 ticks, without marking records consumed.

---

## Smoke of Deceit

Smoke tracking uses two event types:

1. **`ITEM`** event with `inflictor_name = "item_smoke_of_deceit"` — the item was consumed.
2. **`MODIFIER_ADD`** events with `inflictor_name = "modifier_smoke_of_deceit"` and
   `target_is_hero = True` — one per hero that received the smoke buff.

Filter `MODIFIER_ADD` by `target_is_hero = True` to exclude summoned units (e.g.
Beastmaster boars) from the smoke group.

**Empty group edge case:** if the activating hero is inside a sentry ward's truesight
radius at activation, the smoke breaks instantly. The `ITEM` event fires (item consumed)
but zero `MODIFIER_ADD` events follow. This is correct game behaviour — the item was
wasted — not a parsing bug.

---

## Summon kill attribution

When a summoned unit (Warlock Golem, Undying Zombie, Pugna Nether Ward, etc.) kills a
hero, the combat log `DEATH` event records the summoned unit as `attacker_name`, not the
summoning hero. To credit the kill to the owning hero:

1. Track all summoned unit entities (`CDOTABaseNPC` subclasses with a player owner handle).
2. Map summoned unit NPC name → owning hero NPC name at CREATED time.
3. On `DEATH` events, substitute the owner name if the attacker is a known summon.

gem's `CombatAggregator` handles this attribution.

---

## Subscribing to the combat log

```python
from gem.parser import ReplayParser

parser = ReplayParser("my_replay.dem")

def on_entry(entry):
    if entry.log_type == "DEATH" and entry.target_is_hero:
        print(f"tick {entry.tick}: {entry.target_name} killed by {entry.attacker_name}")

parser.on_combat_log_entry(on_entry)
parser.parse()
```

## Functional reference

- [Combat Log API Reference](../reference/combatlog.md)
- [Combat Log Guide](../guides/03_combat_log.md)
- [Combat Aggregator API Reference](../reference/combat_aggregator.md)

Source: `src/gem/combatlog.py`

Reference: `refs/clarity/src/main/java/skadistats/clarity/processor/gameevents/CombatLog.java`
