# Analysis Helpers

Post-parse utilities in `gem.analysis` that transform raw `ParsedMatch` / `ParsedPlayer`
data into higher-level structures for agentic and analytical use.

> **Note:** `estimate_vision` and `match.vision_modifiers` are **experimental**. Vision
> calculations use straight-line geometry only — high-ground penalties, terrain line-of-sight
> (trees/cliffs), and per-hero vision range modifiers are not modelled. Treat results as
> approximations.

All functions are exported directly from `gem.*`:

```python
import gem

pos     = gem.position_at_tick(player, tick)
casts   = gem.group_ability_hits(match.combat_log)
fight   = gem.teamfight_at_tick(match, tick)
near    = gem.heroes_near(match, tick, x, y, radius=2000)
lvl     = gem.ability_level_at_tick(player, "axe_berserkers_call", tick)
sources = gem.estimate_vision(match, team=2, tick=tick, x=x, y=y)
```

---

## `position_at_tick`

```python
gem.position_at_tick(player: ParsedPlayer, tick: int) -> tuple[float, float] | None
```

Return the closest recorded `(x, y)` position for a player at a given tick.

Searches `player.position_log` (sampled at ~1-second intervals) for the entry with the
smallest tick distance to the requested tick. Ties go to the earlier sample.

Returns `None` if `position_log` is empty.

**Example:**

```python
pos = gem.position_at_tick(axe_player, fight.start_tick)
if pos:
    print(f"Axe was at ({pos[0]:.0f}, {pos[1]:.0f}) when the fight started")
```

---

## `group_ability_hits`

```python
gem.group_ability_hits(
    combat_log: list[CombatLogEntry],
    window_ticks: int = 5,
) -> list[AbilityCast]
```

Group `DAMAGE` combat log entries into per-cast `AbilityCast` records.

Many abilities hit multiple targets simultaneously (Ravage, Black Hole, RP). The combat
log emits one `DAMAGE` entry per target. This function collapses those into a single
`AbilityCast` record with a `targets` list and `total_damage` sum.

Only entries with a non-empty `inflictor_name` are considered (auto-attacks are excluded).
Entries from the same `(caster, ability)` pair within `window_ticks` are merged.

**`AbilityCast` fields:**

```python
cast.tick          # int: tick of the first hit
cast.caster        # str: NPC name of the casting unit
cast.ability       # str: ability/item inflictor name
cast.targets       # list[str]: NPC names of all units hit
cast.total_damage  # int: sum of all damage values
cast.damage_type   # str: damage type of the first hit
cast.stun_duration # float: stun seconds (first hit with a stun)
cast.entries       # list[CombatLogEntry]: raw entries that compose this cast
```

**Example:**

```python
casts = gem.group_ability_hits(match.combat_log)
big_hits = [c for c in casts if len(c.targets) >= 3]
for cast in big_hits:
    print(f"{cast.caster} hit {len(cast.targets)} heroes with {cast.ability} "
          f"for {cast.total_damage:,} total damage")
```

---

## `teamfight_at_tick`

```python
gem.teamfight_at_tick(match: ParsedMatch, tick: int) -> Teamfight | None
```

Return the `Teamfight` whose `[start_tick, end_tick]` window contains `tick`, or `None`.

Uses binary search — O(log N). Fights are assumed non-overlapping and sorted by
`start_tick` (as produced by `detect_teamfights`).

**Example:**

```python
for entry in match.combat_log:
    fight = gem.teamfight_at_tick(match, entry.tick)
    if fight:
        print(f"Event at tick {entry.tick} during fight won by {fight.winner}")
```

---

## `heroes_near`

```python
gem.heroes_near(
    match: ParsedMatch,
    tick: int,
    x: float,
    y: float,
    radius: float,
) -> list[ParsedPlayer]
```

Return all heroes within `radius` world units of `(x, y)` at `tick`, sorted by
ascending distance.

Uses `position_at_tick` internally. Heroes with no position data are excluded.

**Example:**

```python
# Who was close enough to join the fight at initiation?
if fight.centroid_x is not None:
    nearby = gem.heroes_near(match, fight.start_tick,
                             fight.centroid_x, fight.centroid_y, radius=2000)
    for player in nearby:
        pos = gem.position_at_tick(player, fight.start_tick)
        print(f"{player.hero_name} at {pos}")
```

---

## `ability_level_at_tick`

```python
gem.ability_level_at_tick(
    player: ParsedPlayer,
    ability: str,
    tick: int,
) -> int
```

Return the level (1–4) of an ability for a player at a given tick.

Uses per-minute ability level snapshots stored in `player._ability_snapshots`
(populated automatically by `gem.parse()`). Returns the last known level at or before
`tick`. Returns `0` if the ability was not yet learned.

Ability names match the `inflictor_name` field in the combat log (e.g.
`"axe_berserkers_call"`).

**Example:**

```python
casts = gem.group_ability_hits(match.combat_log)
for cast in casts:
    player = gem.find_player(match, cast.caster)
    if player:
        lvl = gem.ability_level_at_tick(player, cast.ability, cast.tick)
        print(f"{cast.ability} cast at level {lvl}")
```

---

## `estimate_vision` *(experimental)*

```python
gem.estimate_vision(
    match: ParsedMatch,
    team: int,
    tick: int,
    x: float,
    y: float,
) -> list[VisionSource]
```

Estimate which allied units were providing vision of `(x, y)` at `tick` for the given team
(2=Radiant, 3=Dire).

Returns a list of `VisionSource` objects sorted by ascending distance. An empty list means
the point was in fog for that team.

**Checks three sources:**

| Source | Radius | Night penalty |
|---|---|---|
| Allied hero | 1800 (day) / 800 (night) | Yes |
| Observer ward | 1600 | No |
| Vision modifier (Slardar, BH Track, Dust, Gem) | N/A — direct reveal | No |

Vision modifiers are tracked from combat log `MODIFIER_ADD`/`MODIFIER_REMOVE` events during
parse and stored in `match.vision_modifiers`.

**`VisionSource` fields:**

```python
source.kind          # "hero", "ward", or "modifier"
source.name          # hero NPC name, "observer_ward", or modifier internal name
source.distance      # float: world-unit distance from source to query point
source.vision_radius # int: radius used (0 for modifier reveals)
```

**Limitations** — geometry approximation only:

- No high-ground vision penalties
- No summon/creep vision (only heroes and observer wards)
- No sentry ward true-sight (sentries do not grant standard vision)
- Dust/Gem aura radii are not modelled — modifier reveals are unconditional

**Example:**

```python
sources = gem.estimate_vision(match, team=3, tick=fight.start_tick,
                               x=target_x, y=target_y)
if sources:
    s = sources[0]
    if s.kind == "hero":
        print(f"Dire had vision via {s.name} ({s.vision_radius} units away)")
    elif s.kind == "modifier":
        print(f"Dire had reveal via {s.name} on the target hero")
else:
    print("Blind initiation — target was in fog")
```

---

## Vision modifiers (`match.vision_modifiers`) *(experimental)*

`ParsedMatch.vision_modifiers` is a `list[VisionModifierEvent]` populated by `gem.parse()`.
It tracks every application of a vision-granting ability or item (Slardar Corrosive Haze,
Bounty Hunter Track, Dust of Appearance, Gem of True Sight).

**`VisionModifierEvent` fields:**

```python
ev.tick           # int: tick when modifier was applied
ev.end_tick       # int | None: tick when removed, or None if still active at game end
ev.modifier_name  # str: e.g. "modifier_slardar_amplify_damage"
ev.target_name    # str: NPC name of the revealed hero
ev.caster_name    # str: NPC name of the caster
ev.caster_team    # int: team of the caster (2=Radiant, 3=Dire)
```

**Tracked modifier names:**

| Modifier | Source |
|---|---|
| `modifier_slardar_amplify_damage` | Slardar — Corrosive Haze (ultimate) |
| `modifier_bounty_hunter_track` | Bounty Hunter — Track |
| `modifier_item_dustofappearance` | Dust of Appearance (item) |
| `modifier_item_gem_of_true_sight` | Gem of True Sight (item, on target) |
| `modifier_gem_active_truesight` | Gem of True Sight (thinker aura) |

**Example — how long was each hero tracked by BH?**

```python
for ev in match.vision_modifiers:
    if ev.modifier_name == "modifier_bounty_hunter_track":
        duration = ((ev.end_tick or match.game_end_tick) - ev.tick) / 30
        print(f"{ev.target_name} tracked for {duration:.1f}s")
```

---

::: gem.analysis
