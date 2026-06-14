# Analysis Helpers

Post-parse utilities in `gem.analysis` that transform raw `ParsedMatch` / `ParsedPlayer`
data into higher-level structures for agentic and analytical use.

> **Note:** `estimate_vision` and `match.vision_modifiers` are **experimental**. Vision
> calculations use straight-line geometry only — high-ground penalties, terrain line-of-sight
> (trees/cliffs), and per-hero vision range modifiers are not modelled. Treat results as
> approximations.
>
> For the full derivation, data flow, and limitations, see
> [Experimental Features → Estimate Vision](../experimental/estimate-vision.md).

Canonical implementation modules are split by responsibility:

- `gem.analysis.spatial` — position, nearby-hero, and net-worth lookup helpers
- `gem.analysis.combat` — ability-hit grouping and teamfight helpers
- `gem.analysis.abilities` — ability-level lookup helpers
- `gem.analysis.vision` — geometry-based vision approximation helpers
- `gem.analysis.map_context` — objective-aware farming context helpers
- `gem.analysis.roshan` — Roshan conversion summaries

`gem.analysis` re-exports the public helpers below. `gem.map_context` and
`gem.rosh_conversion` remain compatibility shims for existing imports.

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

Detailed explanation:

1. [Experimental Features → Estimate Vision](../experimental/estimate-vision.md)

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

Detailed explanation:

1. [Experimental Features → Vision Modifiers](../experimental/vision-modifiers.md)

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

## `net_worth_at`

```python
gem.net_worth_at(player: ParsedPlayer, tick: int) -> int
```

Return the closest sampled net worth for a player at a given tick.

Uses a linear scan over `player.times` / `player.net_worth_t` to find the sample with
the smallest tick distance. Returns `0` if no data is available.

**Example:**

```python
for fight in match.teamfights:
    for p in fight.players:
        player = match.players[p.player_id]
        nw = gem.net_worth_at(player, fight.start_tick)
        print(f"{player.hero_name}: {nw:,} NW at fight start")
```

---

## `ward_vision_impact`

```python
gem.ward_vision_impact(ward, match: ParsedMatch) -> int
```

Count distinct enemy heroes spotted by an observer ward during its lifetime.

Checks whether any hero position sample falls within the 1600-unit observer ward vision
radius while the ward was alive. Only the first sighting per hero is counted. Sentry
wards return `0`.

::: warning Approximation
This is a heuristic — terrain, cliffs, trees, and night vision are not modelled.
Position samples are taken every ~5 seconds, so fast-moving heroes may be missed.
:::

**Example:**

```python
for ward in match.wards:
    if ward.ward_type == "observer":
        impact = gem.ward_vision_impact(ward, match)
        print(f"Ward at ({ward.x:.0f}, {ward.y:.0f}) spotted {impact} enemy heroes")
```

---

## `is_active_teamfight_participant`

```python
gem.is_active_teamfight_participant(player_stats) -> bool
```

Return `True` if a player was an active participant in a teamfight — i.e. they had
direct hero-vs-hero combat: a death, damage dealt, damage taken, or healing.

Passive presence (farming nearby, casting only on creeps) does not count.

**Example:**

```python
fight = match.teamfights[0]
active = [p for p in fight.players if gem.is_active_teamfight_participant(p)]
print(f"{len(active)} active participants in fight")
```

---

## `format_npc_name`

```python
gem.format_npc_name(name: str) -> str
```

Convert an NPC name to a human-readable label by stripping Dota 2 prefixes (`npc_dota_`,
`goodguys_`, `badguys_`) and replacing underscores with spaces. For heroes, prefer
`gem.constants.hero_display()` which returns the official display name.

**Example:**

```python
gem.format_npc_name("npc_dota_goodguys_tower_top_1")
# → "tower top 1"
```

---

## `resolve_pick_team`

```python
gem.resolve_pick_team(event: DraftEvent, players: list[ParsedPlayer]) -> int
```

Resolve the correct team (2=Radiant, 3=Dire) for a draft event. `DraftEvent.team`
comes from `m_pGameRules.m_iActiveTeam`, which is reliable for bans but can be wrong
for picks in HLTV replays and coach-slot edge cases.

For picks, cross-references the hero name against the post-game player roster. For bans,
falls back to `event.team`.

**Example:**

```python
for event in match.draft:
    team = gem.resolve_pick_team(event, match.players)
    side = "Radiant" if team == 2 else "Dire"
    action = "picks" if event.is_pick else "bans"
    print(f"{side} {action} {event.hero_name}")
```

---

## Replay download helpers

### `fetch_replay`

```python
gem.fetch_replay(match_id: int, out_dir: str | Path = ".") -> Path
```

Download and decompress a replay from OpenDota in one call. Returns the path to the
decompressed `.dem` file.

```python
dem_path = gem.fetch_replay(8734577999, out_dir="replays/")
match = gem.parse(str(dem_path))
```

### `fetch_replay_url`

```python
gem.fetch_replay_url(match_id: int) -> str
```

Fetch just the replay download URL from the OpenDota API. Raises `ValueError` if
no replay URL is available.

### `download_and_decompress`

```python
gem.download_and_decompress(match_id: int, replay_url: str, out_dir: str | Path = ".") -> Path
```

Lower-level helper: download from a known URL and decompress `.bz2` → `.dem`.

---

## Generated API

## Module `gem.analysis.spatial`

Spatial and time-series helpers for parsed match analysis.

Source: [src/gem/analysis/spatial.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/spatial.py#L1)

### Top-level functions

### `position_at_tick`

```python
def position_at_tick(player: ParsedPlayer, tick: int) -> tuple[float, float] | None
```

Return the closest recorded (x, y) position for a player at a given tick.

Source: [src/gem/analysis/spatial.py:13](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/spatial.py#L13)

### `heroes_near`

```python
def heroes_near(match: ParsedMatch, tick: int, x: float, y: float, radius: float) -> list[ParsedPlayer]
```

Return all heroes within ``radius`` world units of ``(x, y)`` at ``tick``.

Source: [src/gem/analysis/spatial.py:56](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/spatial.py#L56)

### `net_worth_at`

```python
def net_worth_at(player: ParsedPlayer, tick: int) -> int
```

Return the closest sampled net worth for a player at the given tick.

Source: [src/gem/analysis/spatial.py:97](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/spatial.py#L97)

## Module `gem.analysis.combat`

Combat-log and teamfight analysis helpers.

Source: [src/gem/analysis/combat.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/combat.py#L1)

### Top-level functions

### `group_ability_hits`

```python
def group_ability_hits(combat_log: list[CombatLogEntry], window_ticks: int = 5) -> list[AbilityCast]
```

Group DAMAGE combat log entries into per-cast ``AbilityCast`` records.

Source: [src/gem/analysis/combat.py:41](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/combat.py#L41)

### `teamfight_at_tick`

```python
def teamfight_at_tick(match: ParsedMatch, tick: int) -> Teamfight | None
```

Return the teamfight window that contains the given tick, or ``None``.

Source: [src/gem/analysis/combat.py:113](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/combat.py#L113)

### `is_active_teamfight_participant`

```python
def is_active_teamfight_participant(player_stats: object) -> bool
```

Return True if a player was an active participant in a teamfight.

Source: [src/gem/analysis/combat.py:146](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/combat.py#L146)

### Top-level classes

### `AbilityCast`

```python
class AbilityCast
```

A single ability (or item) cast with all targets it hit.

Source: [src/gem/analysis/combat.py:16](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/combat.py#L16)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `caster` | `str` | `-` |
| `ability` | `str` | `-` |
| `targets` | `list[str]` | `field(...)` |
| `total_damage` | `int` | `0` |
| `damage_type` | `str` | `''` |
| `stun_duration` | `float` | `0.0` |
| `entries` | `list[CombatLogEntry]` | `field(...)` |

## Module `gem.analysis.abilities`

Ability-level lookup helpers.

Source: [src/gem/analysis/abilities.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/abilities.py#L1)

### Top-level functions

### `ability_level_at_tick`

```python
def ability_level_at_tick(player: ParsedPlayer, ability: str, tick: int) -> int
```

Return the level of an ability for a player at a given tick.

Source: [src/gem/analysis/abilities.py:12](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/abilities.py#L12)

## Module `gem.analysis.vision`

Vision approximation helpers for parsed matches.

Source: [src/gem/analysis/vision.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/vision.py#L1)

### Top-level functions

### `estimate_vision`

```python
def estimate_vision(match: ParsedMatch, team: int, tick: int, x: float, y: float) -> list[VisionSource]
```

Estimate which allied units were providing vision of ``(x, y)`` at ``tick``.

Source: [src/gem/analysis/vision.py:74](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/vision.py#L74)

### `ward_vision_impact`

```python
def ward_vision_impact(ward: object, match: ParsedMatch) -> int
```

Count distinct enemy heroes spotted by an observer ward during its lifetime.

Source: [src/gem/analysis/vision.py:220](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/vision.py#L220)

### Top-level classes

### `VisionSource`

```python
class VisionSource
```

One unit that was providing vision of a map point at a given tick.

Source: [src/gem/analysis/vision.py:30](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/vision.py#L30)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `kind` | `Literal['hero', 'ward', 'modifier']` | `-` |
| `name` | `str` | `-` |
| `distance` | `float` | `-` |
| `vision_radius` | `int` | `-` |

## Module `gem.analysis.formatting`

Formatting helpers for parsed Dota names.

Source: [src/gem/analysis/formatting.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/formatting.py#L1)

### Top-level functions

### `format_npc_name`

```python
def format_npc_name(name: str) -> str
```

Convert an NPC name to a human-readable label.

Source: [src/gem/analysis/formatting.py:6](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/formatting.py#L6)

## Module `gem.analysis.map_context`

Objective-aware map-context helpers for farming-pattern analysis.

Source: [src/gem/analysis/map_context.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/map_context.py#L1)

### Top-level functions

### `build_map_context_timeline`

```python
def build_map_context_timeline(match: ParsedMatch, team: int, bucket_ticks: int = _DEFAULT_BUCKET_TICKS, presence_window_ticks: int = _DEFAULT_PRESENCE_WINDOW_TICKS) -> list[MapContextBucket]
```

Build objective-aware context buckets for one team's perspective.

Source: [src/gem/analysis/map_context.py:187](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/map_context.py#L187)

### `score_camp_visit_context`

```python
def score_camp_visit_context(*, team: int, camp_id: int, camp_type: str, neutral_kills: int, neutral_damage: int, xp_gain: int, bucket: MapContextBucket) -> CampVisitContext
```

Score one camp visit against a context bucket.

Source: [src/gem/analysis/map_context.py:325](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/map_context.py#L325)

### `world_in_bounds`

```python
def world_in_bounds(x: float, y: float) -> bool
```

Return True when world coordinates are within calibrated map bounds.

Source: [src/gem/analysis/map_context.py:479](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/map_context.py#L479)

### Top-level classes

### `MapContextBucket`

```python
class MapContextBucket
```

Objective- and vision-aware map-state summary for one time bucket.

Source: [src/gem/analysis/map_context.py:40](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/map_context.py#L40)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `start_tick` | `int` | `-` |
| `end_tick` | `int` | `-` |
| `tower_alive_radiant` | `int` | `-` |
| `tower_alive_dire` | `int` | `-` |
| `t1_mid_alive_radiant` | `bool` | `-` |
| `t1_mid_alive_dire` | `bool` | `-` |
| `roshan_last_kill_tick` | `int | None` | `-` |
| `aegis_holder_team` | `int | None` | `-` |
| `aegis_active` | `bool` | `-` |
| `tormentor_last_kill_tick` | `int | None` | `-` |
| `ward_count_radiant` | `int` | `-` |
| `ward_count_dire` | `int` | `-` |
| `net_worth_advantage` | `int` | `-` |
| `xp_advantage` | `int` | `-` |
| `enemy_presence_by_region` | `dict[str, float]` | `field(...)` |

### `CampVisitContext`

```python
class CampVisitContext
```

Context scores and explainability labels for one camp visit.

Source: [src/gem/analysis/map_context.py:61](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/map_context.py#L61)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `farm_safety_score` | `float` | `-` |
| `pressure_score` | `float` | `-` |
| `expected_value_score` | `float` | `-` |
| `context_label` | `Literal['safe_home_farm', 'pressured_home_farm', 'defensive_home_farm', 'safe_invade', 'pressure_invade', 'high_risk_invade']` | `-` |
| `context_drivers` | `list[str]` | `field(...)` |

## Module `gem.analysis.roshan`

Post-parse Roshan conversion analysis.

Source: [src/gem/analysis/roshan.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/roshan.py#L1)

### Top-level functions

### `build_rosh_conversions`

```python
def build_rosh_conversions(match: ParsedMatch) -> list[RoshConversion]
```

Summarise how well each Roshan was converted into advantage.

Source: [src/gem/analysis/roshan.py:387](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/roshan.py#L387)

### Top-level classes

### `RoshTimelineEvent`

```python
class RoshTimelineEvent
```

One notable event inside a Roshan conversion sequence.

Source: [src/gem/analysis/roshan.py:36](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/roshan.py#L36)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `kind` | `Literal['roshan', 'aegis_pickup', 'aegis_denied', 'fight_win', 'fight_loss', 'fight_draw', 'tower', 'barracks', 'buyback', 'aegis_end', 'game_end']` | `-` |
| `label` | `str` | `-` |

### `RoshConversion`

```python
class RoshConversion
```

Derived summary for one Roshan kill and the advantage window that followed.

Source: [src/gem/analysis/roshan.py:57](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/roshan.py#L57)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `rosh_number` | `int` | `-` |
| `rosh_tick` | `int` | `-` |
| `killer_name` | `str` | `-` |
| `holder_team` | `int | None` | `-` |
| `holder_player_id` | `int | None` | `-` |
| `holder_name` | `str` | `-` |
| `aegis_pickup_tick` | `int | None` | `-` |
| `immediate_end_tick` | `int` | `-` |
| `aegis_end_tick` | `int` | `-` |
| `aegis_eval_end_tick` | `int` | `-` |
| `extended_end_tick` | `int` | `-` |
| `aegis_fate` | `Literal['consumed', 'expired', 'denied', 'game_end', 'unknown']` | `-` |
| `first_fight_tick` | `int | None` | `-` |
| `first_objective_tick` | `int | None` | `-` |
| `fight_count` | `int` | `-` |
| `fights_won` | `int` | `-` |
| `fights_lost` | `int` | `-` |
| `fights_drawn` | `int` | `-` |
| `towers_taken` | `int` | `-` |
| `barracks_taken` | `int` | `-` |
| `enemy_buybacks_forced` | `int` | `-` |
| `enemy_half_observer_delta` | `int` | `-` |
| `enemy_half_farm_share_before` | `float` | `-` |
| `enemy_half_farm_share_during` | `float` | `-` |
| `enemy_half_farm_share_delta` | `float` | `-` |
| `conversion_score` | `int` | `-` |
| `conversion_label` | `Literal['low_conversion', 'fight_conversion', 'objective_conversion', 'map_squeeze', 'game_closing_rosh']` | `-` |
| `aegis_outcome` | `Literal['consumed_in_fight', 'expired_after_use', 'expired_unused', 'denied', 'window_lost', 'game_ended', 'unknown']` | `-` |
| `drivers` | `list[str]` | `field(...)` |
| `timeline_events` | `list[RoshTimelineEvent]` | `field(...)` |
