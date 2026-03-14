# Using the Combat Log

The combat log records every meaningful game event at the entry level: damage, heals,
kills, ability uses, item uses, gold changes, ward placements, buybacks. This guide shows
how to subscribe to entries and derive common statistics.

For a conceptual explanation of the two ingestion paths and edge cases, see
[Understanding: The Combat Log](../understanding/09_combat_log.md).

---

## Basic subscription

```python
from gem.parser import ReplayParser

parser = ReplayParser("my_replay.dem")

def on_entry(entry):
    print(entry.tick, entry.log_type, entry.attacker_name, "->", entry.target_name)

parser.on_combat_log_entry(on_entry)
parser.parse()
```

Multiple handlers can be registered. All are called for every entry in arrival order.

---

## Filtering by log type

The most useful filter — only process the entries you care about:

```python
def on_entry(entry):
    match entry.log_type:
        case "DAMAGE":
            ...
        case "DEATH":
            ...
        case "MODIFIER_ADD":
            ...
```

Or with a string comparison:

```python
if entry.log_type == "DAMAGE" and entry.attacker_is_hero:
    ...
```

---

## Hero damage totals

```python
from collections import defaultdict
from gem.parser import ReplayParser

damage_by_hero: dict[str, int] = defaultdict(int)

def on_entry(entry):
    if entry.log_type == "DAMAGE" and entry.attacker_is_hero:
        damage_by_hero[entry.attacker_name] += entry.value

parser = ReplayParser("my_replay.dem")
parser.on_combat_log_entry(on_entry)
parser.parse()

for hero, total in sorted(damage_by_hero.items(), key=lambda x: -x[1]):
    print(f"{hero}: {total:,} damage")
```

---

## Hero kill log

```python
kills = []

def on_entry(entry):
    # Both must be heroes for a hero kill
    if (entry.log_type == "DEATH"
            and entry.attacker_is_hero
            and entry.target_is_hero):
        kills.append(entry)

parser.on_combat_log_entry(on_entry)
parser.parse()

for k in kills:
    via = k.inflictor_name or "auto-attack"
    t = k.tick / 30  # ticks to seconds
    print(f"{t:6.0f}s  {k.attacker_name}  kills  {k.target_name}  [{via}]")
```

Note: `attacker_is_hero or target_is_hero` would include tower kills and creep deaths.
Use `attacker_is_hero and target_is_hero` for hero-vs-hero only.

---

## Kill count with summon attribution

Summoned units (Warlock Golem, Undying Zombie, Pugna Nether Ward) show up as the
`attacker_name` on `DEATH` events, not the player hero. gem's `CombatAggregator`
handles this automatically when you use `gem.parse()`. For manual tracking:

```python
# Map summoned unit name → owning hero name (built from entity stream)
summon_owner: dict[str, str] = {}

def on_entity(entity, op):
    if not (op & EntityOp.CREATED):
        return
    name = entity.get_class_name()
    if "Warlock_Golem" in name or "Zombie" in name:
        # resolve owner via entity handle...
        pass

kill_count: dict[str, int] = defaultdict(int)

def on_entry(entry):
    if entry.log_type == "DEATH" and entry.target_is_hero:
        attacker = summon_owner.get(entry.attacker_name, entry.attacker_name)
        kill_count[attacker] += 1
```

When using `gem.parse()`, kills credited to summons are attributed to the owning hero
automatically in `player.kills`.

---

## Damage type breakdown

`DAMAGE` entries include a `damage_type` field (`"physical"`, `"magical"`, `"pure"`, or
`""` for unset). This lets you break down hero damage by school:

```python
from collections import defaultdict

damage_by_type: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

def on_entry(entry):
    if entry.log_type == "DAMAGE" and entry.attacker_is_hero and entry.damage_type:
        damage_by_type[entry.attacker_name][entry.damage_type] += entry.value

parser.on_combat_log_entry(on_entry)
parser.parse()

for hero, by_type in sorted(damage_by_type.items()):
    total = sum(by_type.values())
    print(f"{hero}: {dict(by_type)}  (total {total:,})")
```

When using `gem.parse()`, the breakdown is pre-aggregated on each `ParsedPlayer` as
`damage_by_type` and `damage_taken_by_type` (keys: `"physical"`, `"magical"`, `"pure"`,
`"others"`).

!!! note
    `damage_type` is only populated for S2 combat log entries (modern replays).
    The `"others"` bucket in the pre-aggregated dicts covers damage against non-hero
    units where Valve does not set the type field.

---

## Healing totals

```python
healing: dict[str, int] = defaultdict(int)

def on_entry(entry):
    if entry.log_type == "HEAL" and entry.attacker_is_hero:
        healing[entry.attacker_name] += entry.value
```

---

## Ability usage count

```python
from collections import Counter

ability_uses: Counter[str] = Counter()

def on_entry(entry):
    if entry.log_type == "ABILITY" and entry.attacker_is_hero:
        ability_uses[entry.inflictor_name] += 1
```

---

## Ward placements

Ward placements appear as `ITEM` log entries:

```python
_WARD_ITEMS = frozenset({
    "item_ward_observer",
    "item_ward_dispenser",
    "item_ward_sentry",
})

ward_events = []

def on_entry(entry):
    if entry.log_type == "ITEM" and entry.inflictor_name in _WARD_ITEMS:
        ward_events.append(entry)
```

The combat log records who placed the ward and when, but **not where**. For coordinates,
use the entity stream (see `WardsExtractor` in
[Full Match Data](04_match_data.md) or gem's `WardsExtractor`).

---

## Buybacks

```python
buybacks = []

def on_entry(entry):
    if entry.log_type == "BUYBACK":
        buybacks.append({
            "tick":        entry.tick,
            "player_slot": entry.value,  # value field holds the player slot
        })
```

---

## Display names

`gem.constants` provides human-readable names backed by bundled dotaconstants data:

```python
from gem.constants import hero_display, item_display, ability_display

hero_display("npc_dota_hero_axe")          # → "Axe"
item_display("item_blink")                 # → "Blink Dagger"
ability_display("nevermore_shadowraze1")   # → "Shadowraze"
```

`ability_display()` handles Aghanim's Scepter and Shard abilities correctly. These
abilities use internal names like `arc_warden_scepter` or `ability_lamp_use` that do not
appear in the dotaconstants abilities table. gem falls back to stripping the hero prefix
and title-casing the remainder:

```python
ability_display("arc_warden_scepter")  # → "Scepter"
ability_display("ability_lamp_use")    # → "Lamp Use"
ability_display("zuus_shard")          # → "Shard"
```

Previously these returned the raw internal string. If you compare ability names across
replays, use the raw `entry.inflictor_name` for stable matching rather than the display
name.

---

## Full working examples

- `examples/match_report.py` — full dashboard including combat log, kills, and vision timelines
- `examples/extraction_demo.py` — developer guide for custom combat log handlers
