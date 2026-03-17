# Teamfight Detection

gem detects teamfights by looking for windows of concentrated hero-vs-hero combat in
the combat log. `match.teamfights` is a list of `Teamfight` objects, one per detected
window.

---

## What a teamfight is

gem detects a fight by:

1. Scanning for hero death events in the combat log.
2. Opening a window of ±15 seconds around each death.
3. Merging windows that share deaths — extending the fight while combat continues.
4. Optionally splitting simultaneous skirmishes in different parts of the map using
   spatial clustering (when position data is available).

The result is a list of non-overlapping fight windows with per-participant statistics.

---

## Accessing teamfight data

```python
import gem

match = gem.parse("my_replay.dem")

for fight in match.teamfights:
    duration = (fight.end_tick - fight.start_tick) / 30
    print(
        f"Fight at tick {fight.start_tick:,}–{fight.end_tick:,}  "
        f"({duration:.0f}s)  "
        f"{fight.deaths} deaths  "
        f"winner: {fight.winner}  "
        f"({fight.radiant_kills}–{fight.dire_kills})"
    )
```

---

## Teamfight fields

```python
fight.start_tick      # int: tick the window opens
fight.end_tick        # int: tick the window closes
fight.last_death_tick # int: tick of the final death
fight.deaths          # int: total hero deaths in the window
fight.radiant_kills   # int: hero kills scored by Radiant
fight.dire_kills      # int: hero kills scored by Dire
fight.winner          # str: "radiant", "dire", "draw", or "unknown"
fight.centroid_x      # float | None: weighted mean X of all deaths
fight.centroid_y      # float | None: weighted mean Y of all deaths
fight.players         # list[TeamfightPlayer]: one per slot (0–9)
```

---

## Per-participant stats

```python
for player in fight.players:
    print(player.player_id)     # int: player slot 0–9
    print(player.deaths)        # int: deaths in this fight window
    print(player.damage_dealt)  # int: damage dealt to enemy heroes
    print(player.damage_taken)  # int: damage taken from enemy heroes
    print(player.healing)       # int: healing dealt to allied heroes (not self)
    print(player.buybacks)      # int: buybacks used in this window
    print(player.gold_delta)    # int: net gold change during the fight
    print(player.xp_delta)      # int: net XP change during the fight
    print(player.ability_uses)  # dict[str, int]: ability name → use count
    print(player.item_uses)     # dict[str, int]: item name → use count
```

---

## What counts as a participant

A hero is only an **active participant** in a fight if they had direct hero-vs-hero
combat in the window:

- `deaths > 0` — died in the window, OR
- `damage_dealt > 0` — dealt damage to an enemy hero, OR
- `damage_taken > 0` — took damage from an enemy hero, OR
- `healing > 0` — healed a different allied hero

**Not counted as participation:**

- Dealing damage to creeps, towers, or Roshan inside the window.
- Self-healing (tango, salve, faerie fire) — these show `attacker == target` and are excluded.
- Neutrals or creeps attacking a hero — damage must come from `attacker_is_hero=True`.

---

## Applying your own threshold

gem returns all detected windows without a minimum death threshold. Apply your own
filter to match OpenDota's convention (3+ deaths = teamfight):

```python
significant_fights = [f for f in match.teamfights if f.deaths >= 3]
```

---

## Finding the fight at a specific tick

Use `gem.teamfight_at_tick()` to look up which fight contains a given tick — useful when
you have a combat log event and want its fight context:

```python
fight = gem.teamfight_at_tick(match, entry.tick)
if fight:
    print(f"Event happened during a fight: {fight.winner} won ({fight.deaths} deaths)")
```

---

## Finding heroes near a fight location

Use `gem.heroes_near()` to find all heroes within a radius of the fight centroid at
initiation time — useful for answering "who was in position to join?":

```python
if fight.centroid_x is not None:
    nearby = gem.heroes_near(match, fight.start_tick,
                             fight.centroid_x, fight.centroid_y,
                             radius=2000)
    for player in nearby:
        print(f"{player.hero_name} was near fight start")
```

---

## HTML teamfight report

The Teamfights tab in `examples/match_report.py` generates a self-contained report with:

- A minimap showing fight locations
- Hero icon timelines
- Per-fight combat log with AoE spells collapsed into grouped cast rows
- Live slider filters for minimum deaths and minimum participant count

```bash
python examples/match_report.py my_replay.dem
```

---

## gem implementation

Source: `src/gem/extractors/teamfights.py`

`detect_teamfights(combat_log, hero_to_slot, player_snapshots, slot_to_team)` is the
main function. It runs four passes:

1. **Pass 1** — detect fight windows from hero death events.
2. **Pass 2** — accumulate per-player stats (damage, healing, deaths, kills) and
   populate `radiant_kills` / `dire_kills`.
3. **Pass 3** — compute XP deltas from bracketing snapshots.
4. **Pass 4** — set `winner` from kill counts.
