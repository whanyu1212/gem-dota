# Teamfight Detection

gem detects teamfights by looking for windows of concentrated hero-vs-hero combat in
the combat log. `match.teamfights` is a list of `Teamfight` objects, one per detected
window.

---

## What a teamfight is

gem detects a fight by:

1. Sliding a time window over the combat log.
2. Looking for windows that contain at least one hero death.
3. Merging adjacent windows that overlap (extending the fight while combat continues).

The result is a list of non-overlapping fight windows with per-participant statistics.

---

## Accessing teamfight data

```python
import gem

match = gem.parse("my_replay.dem")

for fight in match.teamfights:
    duration = (fight.end_tick - fight.start_tick) / 30
    deaths = sum(p.deaths for p in fight.players)
    print(
        f"Fight at tick {fight.start_tick:,}–{fight.end_tick:,}  "
        f"({duration:.0f}s)  "
        f"{deaths} deaths  "
        f"{len(fight.players)} participants"
    )
```

---

## Teamfight fields

```python
fight.start_tick    # int: tick the window opens
fight.end_tick      # int: tick the window closes
fight.players       # list[TeamfightPlayer]: one per active participant
```

---

## Per-participant stats

```python
for player in fight.players:
    print(player.hero_name)      # "CDOTA_Unit_Hero_Axe"
    print(player.deaths)         # int: deaths in this fight window
    print(player.damage_dealt)   # int: damage dealt to enemy heroes
    print(player.damage_taken)   # int: damage taken from enemy heroes
    print(player.healing)        # int: healing dealt to allied heroes (not self)
    print(player.buybacks)       # int: buybacks used in this window
    print(player.gold_delta)     # int: net gold change during the fight
    print(player.xp_delta)       # int: net XP change during the fight
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
significant_fights = [f for f in match.teamfights
                      if sum(p.deaths for p in f.players) >= 3]
```

---

## HTML teamfight report

The Teamfights tab in `examples/match_report.py` generates a self-contained report with:
- A minimap showing fight locations
- Hero icon timelines
- Live slider filters for minimum deaths and minimum participant count

```bash
python examples/match_report.py my_replay.dem
# Outputs an HTML report including the Teamfights tab
```

---

## gem implementation

Source: `src/gem/extractors/teamfights.py`

`detect_teamfights(combat_log_entries, snapshots)` is the main function. It takes the
complete list of `CombatLogEntry` objects and the player snapshot list, and returns a
`list[Teamfight]`.

The windowing algorithm:

1. Collect all hero death ticks.
2. For each death, open a window of ±N ticks.
3. Merge overlapping windows.
4. For each merged window, filter combat log entries to those within the window.
5. Determine active participants by the criteria above.
6. Compute per-participant stats.
