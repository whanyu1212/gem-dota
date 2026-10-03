# Analysis Helpers

Post-parse utilities in `gem.analysis` that transform raw `ParsedMatch` / `ParsedPlayer`
data into higher-level structures for agentic and analytical use.

> **Note:** `assess_point_vision` and
> `match.vision_modifiers` are **experimental**. Point calculations use
> straight-line geometry only — high-ground penalties, terrain line-of-sight
> (trees/cliffs), and per-hero vision range modifiers are not modelled. Treat
> geometry as an approximation and prefer `hero_visibility_at(...)` for a
> canonical player hero.
>
> For the full derivation, data flow, and limitations, see
> [Experimental Features → Point-Vision Evidence](../experimental/estimate-vision.md).

Canonical implementation modules are split by responsibility:

- `gem.analysis.spatial` — position, nearby-hero, and net-worth lookup helpers
- `gem.analysis.combat` — ability-hit grouping and fight helpers
- `gem.analysis.abilities` — ability-level lookup helpers
- `gem.analysis.vision` — geometry-based vision approximation helpers
- `gem.analysis.farming` — camp-by-camp farming routes
- `gem.analysis.roshan` — Roshan kills, Aegis lifecycles and the window that followed
- `gem.analysis.smoke` — evidence-first Smoke of Deceit lifecycle analysis
- `gem.analysis.fight_positioning` — bounded fight-moment spatial evidence

`gem.analysis` re-exports the public helpers below. Use the implementation
modules directly only when module-level imports are useful.

All functions are exported directly from `gem.*`:

```python
import gem

pos     = gem.position_at_tick(player, tick)
casts   = gem.group_ability_hits(match.combat_log)
fight   = gem.fight_at_tick(match, tick)
near    = gem.heroes_near(match, tick, x, y, radius=2000)
lvl     = gem.ability_level_at_tick(player, "axe_berserkers_call", tick)
vision  = gem.assess_point_vision(match, team=2, tick=tick, x=x, y=y)
smokes  = gem.build_smoke_analysis(match)
fights  = gem.build_fight_positioning(match)
rosh    = gem.build_rosh_conversions(match)
```

Roshan records expose `roshan_team_source`, `conversion_team_source`,
`aegis_fate_source`, engagement-aware `fight_evidence` and the signed
`differential_profile`. gem 0.13 removed the tags, verdicts and territory
fields. See
[Roshan Conversion](../experimental/rosh-conversion.md) and its
[calibration record](../experimental/rosh-conversion-calibration.md).

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

## `fight_at_tick`

```python
gem.fight_at_tick(match: ParsedMatch, tick: int) -> Fight | None
```

Return the `Fight` whose `[start_tick, end_tick]` window contains `tick`, or `None`.

Uses binary search — O(log N). Fights are assumed non-overlapping and sorted by
`start_tick` (as produced by `detect_fights`).

**Example:**

```python
for entry in match.combat_log:
    fight = gem.fight_at_tick(match, entry.tick)
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

## `hero_visibility_at`

```python
state = gem.hero_visibility_at(
    match,
    player_id=7,
    observing_team=2,
    tick=120_000,
)

if state is gem.VisibilityState.VISIBLE:
    print("Radiant could see player 7's canonical hero")
```

This query reads the replay's team visibility bitsets. It returns one of
`VISIBLE`, `HIDDEN`, or `UNKNOWN`; times before the first observation and after
an entity is deleted or replaced are `UNKNOWN`. The result applies to that hero
entity only. It does not reconstruct the visible map area or identify which
hero, ward, or spell supplied the vision.

Source 2 combat-log entries also expose event-local `visible_radiant` and
`visible_dire` values. Those values are `None` when the optional protobuf field
was absent, including for legacy Source 1 events.

## `entity_visibility_at`

```python
state = gem.entity_visibility_at(
    match,
    entity_index=427,
    entity_serial=12,
    observing_team=3,
    tick=120_000,
)
```

The index-plus-serial identity prevents slot reuse from leaking state. The
latest eligible event wins; inactive terminal events return `UNKNOWN`. Coverage
is limited to active networked Dota NPC entities and packet-boundary evidence,
not arbitrary-point fog of war, source attribution, temporary viewers, or
terrain/navigation simulation.

---

## `assess_point_vision` *(experimental)*

Detailed explanation:

1. [Experimental Features → Point-Vision Evidence](../experimental/estimate-vision.md)

```python
assessment = gem.assess_point_vision(
    match: ParsedMatch,
    team: int,
    tick: int,
    x: float,
    y: float,
    *,
    target_player_id: int | None = None,
    max_position_age_ticks: int = 150,
) -> PointVisionAssessment
```

Assess the evidence that currently modelled sources covered `(x, y)` for the
given team. The result distinguishes `supported`, `unsupported`, and
`incomplete`; negative geometry is never presented as authoritative fog.

Hero sources retain their sampled coordinate, sample tick, age, player identity,
and freshness provenance. Samples older than `max_position_age_ticks` are
excluded and recorded as evidence gaps. Observer wards use their entity-derived
placement coordinates and a half-open placement-to-removal lifetime.

**Point-coverage sources:**

| Source | Radius | Night penalty |
|---|---|---|
| Allied hero | 1800 (day) / 800 (night) | Yes |
| Observer ward | 1600 | No |

Sentries are not standard vision sources. Missing or stale hero positions,
unknown ward ownership, missing observer coordinates, and queries beyond the
observed replay horizon are represented as gaps.

When `target_player_id` is supplied, the assessment also exposes the canonical
target's authoritative `visible`/`hidden`/`unknown` state and any defensible
direct-target reveal intervals. Those facts remain separate from map-point
geometry.

```python
if assessment.status is gem.PointVisionStatus.SUPPORTED:
    print(assessment.sources[0])
elif assessment.status is gem.PointVisionStatus.INCOMPLETE:
    print([gap.code for gap in assessment.gaps])
```

---

## Point-source limits *(experimental)*

`assess_point_vision(...).sources` is the distance-sorted modelled geometry
(gem 0.13 removed the old `estimate_vision` list view). Direct-target modifiers
are not arbitrary-point sources; query them for a specific canonical target
through `assess_point_vision(..., target_player_id=...)`.

The point geometry is an approximation:

- No high-ground vision penalties
- No summon/creep vision (only heroes and observer wards)
- No sentry ward true-sight (sentries do not grant standard vision)
- Aura/carrier geometry is not modelled; those events are not direct reveal sources

---

## Vision modifiers (`match.vision_modifiers`) *(experimental)*

Detailed explanation:

1. [Experimental Features → Vision Modifiers](../experimental/vision-modifiers.md)

`ParsedMatch.vision_modifiers` is a `list[VisionModifierEvent]` populated by
`gem.parse()`. It retains direct reveals, aura/carrier evidence, non-hero
targets, lifecycle evidence, and team provenance. Ambiguous/orphan removals are
available separately as `match.vision_modifier_pairing_issues`.

**`VisionModifierEvent` fields:**

```python
ev.tick           # int: tick when modifier was applied
ev.end_tick       # int | None: observed removal tick only
ev.modifier_name  # str: e.g. "modifier_slardar_amplify_damage"
ev.target_name    # str: NPC name of the revealed hero
ev.caster_name    # str: NPC name of the caster
ev.caster_team    # int: team of the caster (2=Radiant, 3=Dire)
ev.semantic       # direct_target_reveal, reveal_aura, aura_carrier, ...
ev.lifecycle_status  # removed, expired, open, or incomplete
ev.close_evidence    # observed, duration_inferred, unobserved, or ambiguous
```

**Tracked modifier names:**

| Modifier | Source |
|---|---|
| `modifier_slardar_amplify_damage` | Slardar — Corrosive Haze (ultimate) |
| `modifier_bounty_hunter_track` | Bounty Hunter — Track |
| `modifier_item_dustofappearance` | Dust of Appearance (item) |
| `modifier_item_gem_of_true_sight` | Gem carrier evidence (not a direct reveal) |
| `modifier_gem_active_truesight` | Gem reveal-aura evidence |

**Example — how long was each hero tracked by BH?**

```python
for ev in match.vision_modifiers:
    if ev.modifier_name == "modifier_bounty_hunter_track":
        print(ev.target_name, ev.lifecycle_status, ev.end_tick)
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
for fight in match.fights:
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

## `is_active_fight_participant`

```python
gem.is_active_fight_participant(player_stats) -> bool
```

Return `True` if a player was an active participant in a fight — i.e. they had
direct hero-vs-hero combat: a death, damage dealt, damage taken, or healing.

Passive presence (farming nearby, casting only on creeps) does not count.

**Example:**

```python
fight = match.fights[0]
active = [p for p in fight.players if gem.is_active_fight_participant(p)]
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

### `position_sample_at_tick`

```python
def position_sample_at_tick(player: ParsedPlayer, tick: int) -> SampledPosition | None
```

Return the nearest recorded position with its sampling metadata.

Source: [src/gem/analysis/spatial.py:35](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/spatial.py#L35)

### `position_at_tick`

```python
def position_at_tick(player: ParsedPlayer, tick: int) -> tuple[float, float] | None
```

Return the closest recorded (x, y) position for a player at a given tick.

Source: [src/gem/analysis/spatial.py:73](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/spatial.py#L73)

### `heroes_near`

```python
def heroes_near(match: ParsedMatch, tick: int, x: float, y: float, radius: float) -> list[ParsedPlayer]
```

Return all heroes within ``radius`` world units of ``(x, y)`` at ``tick``.

Source: [src/gem/analysis/spatial.py:102](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/spatial.py#L102)

### `net_worth_at`

```python
def net_worth_at(player: ParsedPlayer, tick: int) -> int
```

Return the closest sampled net worth for a player at the given tick.

Source: [src/gem/analysis/spatial.py:143](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/spatial.py#L143)

### Top-level classes

### `SampledPosition`

```python
class SampledPosition
```

Nearest recorded player position and its sampling provenance.

Source: [src/gem/analysis/spatial.py:19](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/spatial.py#L19)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `x` | `float` | `-` |
| `y` | `float` | `-` |
| `sample_tick` | `int` | `-` |
| `age_ticks` | `int` | `-` |

## Module `gem.analysis.regions`

Map regions: which named area of the 7.41 map a world position is in.

Source: [src/gem/analysis/regions.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/regions.py#L1)

### Top-level functions

### `region_of`

```python
def region_of(x: float, y: float) -> str
```

Classify a world position into a map region.

Source: [src/gem/analysis/regions.py:84](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/regions.py#L84)

## Module `gem.analysis.combat`

Combat-log and fight analysis helpers.

Source: [src/gem/analysis/combat.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/combat.py#L1)

### Top-level functions

### `group_ability_hits`

```python
def group_ability_hits(combat_log: list[CombatLogEntry], window_ticks: int = 5) -> list[AbilityCast]
```

Group DAMAGE combat log entries into per-cast ``AbilityCast`` records.

Source: [src/gem/analysis/combat.py:50](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/combat.py#L50)

### `find_fights`

```python
def find_fights(match: ParsedMatch, *, window_s: float = FIGHT_WINDOW_S, radius: float | None = FIGHT_RADIUS) -> list[Fight]
```

Group a parsed match's hero deaths into fights with your own settings.

Source: [src/gem/analysis/combat.py:124](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/combat.py#L124)

### `fight_at_tick`

```python
def fight_at_tick(match: ParsedMatch, tick: int) -> Fight | None
```

Return the fight window that contains the given tick, or ``None``.

Source: [src/gem/analysis/combat.py:196](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/combat.py#L196)

### `is_active_fight_participant`

```python
def is_active_fight_participant(player_stats: object) -> bool
```

Return True if a player was an active participant in a fight.

Source: [src/gem/analysis/combat.py:229](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/combat.py#L229)

### Top-level classes

### `AbilityCast`

```python
class AbilityCast
```

A single ability (or item) cast with all targets it hit.

Source: [src/gem/analysis/combat.py:25](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/combat.py#L25)

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

Evidence-aware visibility helpers for parsed matches.

Source: [src/gem/analysis/vision.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/vision.py#L1)

### Top-level functions

### `is_daytime`

```python
def is_daytime(game_start_tick: int | None, tick: int) -> bool
```

Return True if it is daytime at the given absolute tick.

Source: [src/gem/analysis/vision.py:213](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/vision.py#L213)

### `hero_visibility_at`

```python
def hero_visibility_at(match: ParsedMatch, *, player_id: int, observing_team: int, tick: int) -> VisibilityState
```

Return authoritative hero-entity visibility at or before ``tick``.

Source: [src/gem/analysis/vision.py:240](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/vision.py#L240)

### `entity_visibility_at`

```python
def entity_visibility_at(match: ParsedMatch, *, entity_index: int, entity_serial: int, observing_team: int, tick: int) -> VisibilityState
```

Return authoritative NPC-entity visibility at or before ``tick``.

Source: [src/gem/analysis/vision.py:282](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/vision.py#L282)

### `assess_point_vision`

```python
def assess_point_vision(match: ParsedMatch, team: int, tick: int, x: float, y: float, *, target_player_id: int | None = None, max_position_age_ticks: int = 150) -> PointVisionAssessment
```

Assess bounded modeled evidence for team vision of one map point.

Source: [src/gem/analysis/vision.py:328](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/vision.py#L328)

### `ward_vision_impact`

```python
def ward_vision_impact(ward: object, match: ParsedMatch) -> int
```

Count distinct enemy heroes spotted by an observer ward during its lifetime.

Source: [src/gem/analysis/vision.py:608](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/vision.py#L608)

### Top-level classes

### `VisionSource`

```python
class VisionSource
```

One modeled geometry source covering a map point at a given tick.

Source: [src/gem/analysis/vision.py:46](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/vision.py#L46)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `kind` | `Literal['hero', 'ward', 'modifier']` | `-` |
| `name` | `str` | `-` |
| `distance` | `float` | `-` |
| `vision_radius` | `int` | `-` |
| `x` | `float \| None` | `None` |
| `y` | `float \| None` | `None` |
| `position_tick` | `int \| None` | `None` |
| `position_age_ticks` | `int \| None` | `None` |
| `player_id` | `int \| None` | `None` |
| `position_provenance` | `Literal['sampled_player_position', 'ward_placement'] \| None` | `None` |

### `PointVisionStatus`

```python
class PointVisionStatus(str, Enum)
```

Modeled support state for an arbitrary map point.

Source: [src/gem/analysis/vision.py:83](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/vision.py#L83)

### `PointVisionSource`

```python
class PointVisionSource
```

One bounded geometry source supporting point coverage.

Source: [src/gem/analysis/vision.py:94](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/vision.py#L94)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `kind` | `Literal['hero', 'observer_ward']` | `-` |
| `name` | `str` | `-` |
| `distance` | `float` | `-` |
| `vision_radius` | `int` | `-` |
| `x` | `float` | `-` |
| `y` | `float` | `-` |
| `position_provenance` | `Literal['sampled_player_position', 'ward_placement']` | `-` |
| `position_tick` | `int \| None` | `None` |
| `position_age_ticks` | `int \| None` | `None` |
| `player_id` | `int \| None` | `None` |

#### Properties

##### `identity`

Signature: `def PointVisionSource.identity(self) -> str`

Return the source name as its stable identity.

Source: [src/gem/analysis/vision.py:122](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/vision.py#L122)

##### `radius`

Signature: `def PointVisionSource.radius(self) -> int`

Return the modeled circular vision radius.

Source: [src/gem/analysis/vision.py:127](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/vision.py#L127)

### `PointVisionGap`

```python
class PointVisionGap
```

One material omission or ambiguity in a point-vision assessment.

Source: [src/gem/analysis/vision.py:133](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/vision.py#L133)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `code` | `str` | `-` |
| `subject` | `str` | `-` |

### `DirectTargetRevealEvidence`

```python
class DirectTargetRevealEvidence
```

Bounded direct-reveal evidence for the requested canonical hero.

Source: [src/gem/analysis/vision.py:146](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/vision.py#L146)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `modifier_name` | `str` | `-` |
| `target_name` | `str` | `-` |
| `caster_name` | `str` | `-` |
| `caster_team` | `int` | `-` |
| `start_tick` | `int` | `-` |
| `end_tick` | `int` | `-` |
| `target_player_id` | `int` | `-` |

#### Properties

##### `tick`

Signature: `def DirectTargetRevealEvidence.tick(self) -> int`

Return the interval start using modifier-event terminology.

Source: [src/gem/analysis/vision.py:171](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/vision.py#L171)

### `PointVisionAssessment`

```python
class PointVisionAssessment
```

Evidence-aware modeled coverage assessment for one arbitrary point.

Source: [src/gem/analysis/vision.py:177](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/vision.py#L177)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `team` | `int` | `-` |
| `tick` | `int` | `-` |
| `x` | `float` | `-` |
| `y` | `float` | `-` |
| `status` | `PointVisionStatus` | `-` |
| `sources` | `list[PointVisionSource]` | `-` |
| `gaps` | `list[PointVisionGap]` | `-` |
| `direct_target_reveals` | `list[DirectTargetRevealEvidence]` | `-` |
| `target_player_id` | `int \| None` | `-` |
| `authoritative_applicable` | `bool` | `-` |
| `authoritative_visibility` | `VisibilityState` | `-` |
| `max_position_age_ticks` | `int` | `-` |

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

## Module `gem.analysis.farming`

Evidence-first neutral-camp route reconstruction.

Source: [src/gem/analysis/farming.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/farming.py#L1)

### Top-level functions

### `build_farming_routes`

```python
def build_farming_routes(match: ParsedMatch, *, config: FarmingRouteConfig = DEFAULT_FARMING_ROUTE_CONFIG) -> list[FarmingRoute]
```

Build deterministic camp-local route evidence for every parsed player.

Source: [src/gem/analysis/farming.py:633](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/farming.py#L633)

### Top-level classes

### `FarmingEvidenceStrength`

```python
class FarmingEvidenceStrength(str, Enum)
```

Conservative support level for a camp-local route segment.

Source: [src/gem/analysis/farming.py:25](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/farming.py#L25)

### `FarmingBoundaryReason`

```python
class FarmingBoundaryReason(str, Enum)
```

Observed reason a route segment started or ended.

Source: [src/gem/analysis/farming.py:33](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/farming.py#L33)

### `FarmingRouteConfig`

```python
class FarmingRouteConfig
```

Inspectable thresholds for farming-route reconstruction.

Source: [src/gem/analysis/farming.py:45](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/farming.py#L45)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `max_sample_gap_ticks` | `int` | `10 * _TICKS_PER_SECOND` |
| `max_contiguous_speed` | `float` | `900.0` |
| `merge_gap_ticks` | `int` | `5 * _TICKS_PER_SECOND` |
| `min_weak_dwell_ticks` | `int` | `5 * _TICKS_PER_SECOND` |
| `resource_max_age_ticks` | `int` | `2 * _TICKS_PER_SECOND` |

### `FarmingCampZone`

```python
class FarmingCampZone
```

One calibrated neutral-camp zone from the bundled catalog.

Source: [src/gem/analysis/farming.py:71](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/farming.py#L71)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `camp_id` | `int` | `-` |
| `camp_type` | `str` | `-` |
| `center_x` | `float` | `-` |
| `center_y` | `float` | `-` |
| `shape` | `str` | `-` |
| `radius_x` | `float` | `-` |
| `radius_y` | `float` | `-` |
| `rotation_degrees` | `float` | `-` |
| `polygon_points` | `tuple[tuple[float, float], ...]` | `()` |
| `enter_margin` | `float` | `0.0` |
| `exit_margin` | `float` | `0.0` |
| `owner_team` | `int \| None` | `None` |
| `lane` | `Literal['top', 'mid', 'bot', 'none', 'unknown']` | `'unknown'` |
| `area` | `str` | `'unknown'` |

### `FarmingRoutePoint`

```python
class FarmingRoutePoint
```

One sampled route point and its selected camp membership.

Source: [src/gem/analysis/farming.py:91](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/farming.py#L91)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `x` | `float` | `-` |
| `y` | `float` | `-` |
| `camp_id` | `int \| None` | `-` |
| `camp_type` | `str \| None` | `-` |
| `inside_base_zone` | `bool` | `-` |
| `boundary_before` | `FarmingBoundaryReason \| None` | `None` |

### `FarmingRouteSegment`

```python
class FarmingRouteSegment
```

One camp-local sampled route segment with factual support evidence.

Source: [src/gem/analysis/farming.py:104](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/farming.py#L104)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `segment_index` | `int` | `-` |
| `player_id` | `int` | `-` |
| `hero_name` | `str` | `-` |
| `team` | `int` | `-` |
| `camp_id` | `int` | `-` |
| `camp_type` | `str` | `-` |
| `start_tick` | `int` | `-` |
| `end_tick` | `int` | `-` |
| `duration_seconds` | `float` | `-` |
| `start_reason` | `FarmingBoundaryReason` | `-` |
| `end_reason` | `FarmingBoundaryReason` | `-` |
| `sample_count` | `int` | `-` |
| `in_zone_sample_count` | `int` | `-` |
| `position_coverage` | `float \| None` | `-` |
| `max_sample_gap_ticks` | `int \| None` | `-` |
| `micro_exit_merged` | `bool` | `-` |
| `neutral_kills` | `int` | `-` |
| `neutral_damage` | `int` | `-` |
| `window_xp_delta` | `int \| None` | `-` |
| `window_total_earned_gold_delta` | `int \| None` | `-` |
| `resource_start_sample_tick` | `int \| None` | `-` |
| `resource_end_sample_tick` | `int \| None` | `-` |
| `evidence_strength` | `FarmingEvidenceStrength` | `-` |
| `evidence_reasons` | `list[str]` | `field(...)` |
| `evidence_gaps` | `list[str]` | `field(...)` |
| `points` | `list[FarmingRoutePoint]` | `field(...)` |
| `distance_travelled` | `float \| None` | `None` |
| `camp_owner_team` | `int \| None` | `None` |
| `camp_lane` | `str` | `'unknown'` |
| `camp_area` | `str` | `'unknown'` |
| `camp_catalog_version` | `int \| None` | `None` |
| `camp_map_patch` | `str \| None` | `None` |
| `camp_topology_patch` | `str \| None` | `None` |

### `FarmingRoute`

```python
class FarmingRoute
```

Evidence-first farming route for one parsed player.

Source: [src/gem/analysis/farming.py:143](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/farming.py#L143)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `player_id` | `int` | `-` |
| `hero_name` | `str` | `-` |
| `team` | `int` | `-` |
| `camp_catalog_version` | `int \| None` | `-` |
| `camp_map_patch` | `str \| None` | `-` |
| `status` | `Literal['complete', 'partial', 'unavailable']` | `-` |
| `status_reasons` | `list[str]` | `field(...)` |
| `points` | `list[FarmingRoutePoint]` | `field(...)` |
| `segments` | `list[FarmingRouteSegment]` | `field(...)` |
| `camp_topology_patch` | `str \| None` | `None` |

## Module `gem.analysis.roshan`

Post-parse Roshan records: each kill, its Aegis lifecycle and the window that followed.

Source: [src/gem/analysis/roshan.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/roshan.py#L1)

### Top-level functions

### `build_rosh_conversions`

```python
def build_rosh_conversions(match: ParsedMatch) -> list[RoshConversion]
```

Summarise each Roshan kill, its Aegis lifecycle and the window that followed.

Source: [src/gem/analysis/roshan.py:916](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/roshan.py#L916)

### Top-level classes

### `AegisFateSource`

```python
class AegisFateSource(str, Enum)
```

Evidence or boundary used to classify an Aegis lifecycle.

Source: [src/gem/analysis/roshan.py:42](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/roshan.py#L42)

### `RoshTeamAttributionSource`

```python
class RoshTeamAttributionSource(str, Enum)
```

Provenance of a team attribution used by Roshan analysis.

Source: [src/gem/analysis/roshan.py:55](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/roshan.py#L55)

### `RoshFightRelation`

```python
class RoshFightRelation(str, Enum)
```

Temporal relationship between a fight and the conversion window.

Source: [src/gem/analysis/roshan.py:67](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/roshan.py#L67)

### `RoshFightEvidence`

```python
class RoshFightEvidence
```

Engagement-aware evidence for one fight associated with a Roshan window.

Source: [src/gem/analysis/roshan.py:77](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/roshan.py#L77)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `fight_index` | `int` | `-` |
| `relation` | `RoshFightRelation` | `-` |
| `engagement_start_tick` | `int` | `-` |
| `engagement_start_source` | `EngagementStartSource` | `-` |
| `first_death_tick` | `int` | `-` |
| `end_tick` | `int` | `-` |
| `winner` | `str` | `-` |
| `deaths` | `int` | `-` |
| `conversion_participant_ids` | `tuple[int, ...]` | `-` |
| `opponent_participant_ids` | `tuple[int, ...]` | `-` |
| `unknown_participant_ids` | `tuple[int, ...]` | `-` |

### `RoshTimelineEvent`

```python
class RoshTimelineEvent
```

One notable event inside a Roshan conversion sequence.

Source: [src/gem/analysis/roshan.py:128](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/roshan.py#L128)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `kind` | `Literal['roshan', 'aegis_pickup', 'aegis_denied', 'fight_win', 'fight_loss', 'fight_draw', 'tower', 'tower_lost', 'tower_unknown', 'barracks', 'barracks_lost', 'barracks_unknown', 'buyback', 'own_buyback', 'tormentor', 'opponent_tormentor', 'tormentor_unknown', 'banner', 'opponent_banner', 'aegis_end', 'game_end']` | `-` |
| `label` | `str` | `-` |
| `fight_index` | `int \| None` | `None` |

### `RoshDifferentialProfile`

```python
class RoshDifferentialProfile
```

Evidence-first conversion-team profile over one hardened Rosh window.

Source: [src/gem/analysis/roshan.py:160](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/roshan.py#L160)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `conversion_team` | `int \| None` | `None` |
| `opponent_team` | `int \| None` | `None` |
| `window_start_tick` | `int \| None` | `None` |
| `window_end_tick` | `int \| None` | `None` |
| `conversion_fights_won` | `int \| None` | `None` |
| `opponent_fights_won` | `int \| None` | `None` |
| `fights_drawn` | `int \| None` | `None` |
| `fight_differential` | `int \| None` | `None` |
| `conversion_towers` | `int \| None` | `None` |
| `opponent_towers` | `int \| None` | `None` |
| `conversion_barracks` | `int \| None` | `None` |
| `opponent_barracks` | `int \| None` | `None` |
| `unattributed_towers` | `int` | `0` |
| `unattributed_barracks` | `int` | `0` |
| `conversion_structure_value` | `int \| None` | `None` |
| `opponent_structure_value` | `int \| None` | `None` |
| `structure_delta` | `int \| None` | `None` |
| `net_worth_advantage_start` | `int \| None` | `None` |
| `net_worth_advantage_end` | `int \| None` | `None` |
| `net_worth_swing` | `int \| None` | `None` |
| `net_worth_swing_per_minute` | `float \| None` | `None` |
| `xp_advantage_start` | `int \| None` | `None` |
| `xp_advantage_end` | `int \| None` | `None` |
| `xp_swing` | `int \| None` | `None` |
| `xp_swing_per_minute` | `float \| None` | `None` |
| `conversion_forward_wards` | `int \| None` | `None` |
| `opponent_forward_wards` | `int \| None` | `None` |
| `forward_ward_delta` | `int \| None` | `None` |
| `conversion_tormentors` | `int \| None` | `None` |
| `opponent_tormentors` | `int \| None` | `None` |
| `unattributed_tormentors` | `int` | `0` |
| `tormentor_delta` | `int \| None` | `None` |
| `status` | `Literal['complete', 'partial', 'unavailable']` | `'unavailable'` |
| `status_reasons` | `list[str]` | `field(...)` |

### `RoshConversion`

```python
class RoshConversion
```

Derived summary for one Roshan kill and the advantage window that followed.

Source: [src/gem/analysis/roshan.py:242](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/roshan.py#L242)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `rosh_number` | `int` | `-` |
| `rosh_tick` | `int` | `-` |
| `killer_name` | `str` | `-` |
| `holder_team` | `int \| None` | `-` |
| `holder_player_id` | `int \| None` | `-` |
| `holder_name` | `str` | `-` |
| `aegis_pickup_tick` | `int \| None` | `-` |
| `immediate_end_tick` | `int` | `-` |
| `aegis_end_tick` | `int` | `-` |
| `aegis_eval_end_tick` | `int` | `-` |
| `extended_end_tick` | `int` | `-` |
| `aegis_fate` | `Literal['consumed', 'expired', 'denied', 'game_end', 'unknown']` | `-` |
| `first_fight_tick` | `int \| None` | `-` |
| `first_objective_tick` | `int \| None` | `-` |
| `fight_count` | `int` | `-` |
| `fights_won` | `int` | `-` |
| `fights_lost` | `int` | `-` |
| `fights_drawn` | `int` | `-` |
| `towers_taken` | `int` | `-` |
| `barracks_taken` | `int` | `-` |
| `enemy_buybacks_forced` | `int` | `-` |
| `enemy_half_observer_delta` | `int` | `-` |
| `timeline_events` | `list[RoshTimelineEvent]` | `field(...)` |
| `drops` | `list[str]` | `field(...)` |
| `had_high_value_drop` | `bool` | `False` |
| `banner_planted` | `bool` | `False` |
| `banner_rax_conversion` | `bool` | `False` |
| `banner_rax_lane` | `str \| None` | `None` |
| `roshan_team` | `int \| None` | `None` |
| `conversion_team` | `int \| None` | `None` |
| `roshan_team_source` | `RoshTeamAttributionSource` | `RoshTeamAttributionSource.UNKNOWN` |
| `conversion_team_source` | `RoshTeamAttributionSource` | `RoshTeamAttributionSource.UNKNOWN` |
| `aegis_fate_source` | `AegisFateSource` | `AegisFateSource.MISSING_EVENT` |
| `aegis_fate_inferred` | `bool` | `False` |
| `first_engagement_tick` | `int \| None` | `None` |
| `fight_evidence` | `list[RoshFightEvidence]` | `field(...)` |
| `analysis_status` | `Literal['complete', 'partial', 'unavailable']` | `'unavailable'` |
| `analysis_status_reasons` | `list[str]` | `field(...)` |
| `differential_profile` | `RoshDifferentialProfile` | `field(...)` |

## Module `gem.analysis.smoke`

Evidence-first post-parse Smoke of Deceit lifecycle analysis.

Source: [src/gem/analysis/smoke.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/smoke.py#L1)

### Top-level functions

### `build_smoke_analysis`

```python
def build_smoke_analysis(match: ParsedMatch) -> list[SmokeAnalysis]
```

Build factual lifecycle summaries for every smoke item use.

Source: [src/gem/analysis/smoke.py:149](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/smoke.py#L149)

### Top-level classes

### `SmokeLifecycleStatus`

```python
class SmokeLifecycleStatus(str, Enum)
```

Observed lifecycle classification for one smoke participant.

Source: [src/gem/analysis/smoke.py:35](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/smoke.py#L35)

### `SmokeGroupStatus`

```python
class SmokeGroupStatus(str, Enum)
```

Evidence-based aggregate state for one smoke activation.

Source: [src/gem/analysis/smoke.py:52](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/smoke.py#L52)

### `SmokeMemberAnalysis`

```python
class SmokeMemberAnalysis
```

Evidence summary for one hero in a smoke activation.

Source: [src/gem/analysis/smoke.py:72](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/smoke.py#L72)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `hero_name` | `str` | `-` |
| `player_id` | `int \| None` | `-` |
| `applied_tick` | `int` | `-` |
| `removed_tick` | `int \| None` | `-` |
| `lifecycle_status` | `SmokeLifecycleStatus` | `-` |
| `visibility_at_apply` | `VisibilityState` | `-` |
| `visibility_at_remove` | `VisibilityState` | `-` |
| `first_visible_tick` | `int \| None` | `None` |
| `nearest_enemy_hero` | `str \| None` | `None` |
| `nearest_enemy_player_id` | `int \| None` | `None` |
| `nearest_enemy_distance` | `float \| None` | `None` |
| `same_tick_actions` | `list[CombatLogEntry]` | `field(...)` |
| `same_tick_deaths` | `list[CombatLogEntry]` | `field(...)` |
| `evidence_gaps` | `list[str]` | `field(...)` |

### `SmokeAnalysis`

```python
class SmokeAnalysis
```

Evidence summary for one Smoke of Deceit item use.

Source: [src/gem/analysis/smoke.py:115](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/smoke.py#L115)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `activation_tick` | `int` | `-` |
| `activator` | `str` | `-` |
| `team` | `int` | `-` |
| `status` | `SmokeGroupStatus` | `-` |
| `activation_x` | `float \| None` | `-` |
| `activation_y` | `float \| None` | `-` |
| `member_centroid_x` | `float \| None` | `-` |
| `member_centroid_y` | `float \| None` | `-` |
| `members` | `list[SmokeMemberAnalysis]` | `field(...)` |
| `first_fight` | `Fight \| None` | `None` |
| `evidence_gaps` | `list[str]` | `field(...)` |

## Module `gem.analysis.fight_positioning`

Evidence-aware positioning snapshots for detected fights.

Source: [src/gem/analysis/fight_positioning.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/fight_positioning.py#L1)

### Top-level functions

### `build_fight_positioning`

```python
def build_fight_positioning(match: ParsedMatch, *, pre_engagement_ticks: int = 300, max_position_age_ticks: int = 60, nearby_radius: float = 3000.0) -> list[FightPositioning]
```

Build evidence-aware positioning records for detected fights.

Source: [src/gem/analysis/fight_positioning.py:218](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/fight_positioning.py#L218)

### Top-level classes

### `SnapshotKind`

```python
class SnapshotKind(str, Enum)
```

Logical moment represented by a positioning snapshot.

Source: [src/gem/analysis/fight_positioning.py:23](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/fight_positioning.py#L23)

### `EngagementStartSource`

```python
class EngagementStartSource(str, Enum)
```

Provenance for the engagement-start tick.

Source: [src/gem/analysis/fight_positioning.py:43](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/fight_positioning.py#L43)

### `EvidenceCompleteness`

```python
class EvidenceCompleteness(str, Enum)
```

Position-evidence completeness for one team at one snapshot.

Source: [src/gem/analysis/fight_positioning.py:62](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/fight_positioning.py#L62)

### `HeroPositionEvidence`

```python
class HeroPositionEvidence
```

Position and contextual evidence for one canonical player hero.

Source: [src/gem/analysis/fight_positioning.py:79](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/fight_positioning.py#L79)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `player_id` | `int` | `-` |
| `hero_name` | `str` | `-` |
| `player_name` | `str` | `-` |
| `team` | `int` | `-` |
| `active_participant` | `bool` | `-` |
| `near_fight` | `bool \| None` | `-` |
| `x` | `float \| None` | `-` |
| `y` | `float \| None` | `-` |
| `sample_tick` | `int \| None` | `-` |
| `sample_age_ticks` | `int \| None` | `-` |
| `visibility` | `VisibilityState` | `-` |
| `distance_to_team_centroid` | `float \| None` | `-` |
| `nearest_ally_distance` | `float \| None` | `-` |
| `nearest_enemy_distance` | `float \| None` | `-` |
| `active_smoke_activation_tick` | `int \| None` | `-` |
| `active_reveal_modifiers` | `tuple[str, ...]` | `-` |
| `evidence_gaps` | `tuple[str, ...]` | `-` |

### `TeamPositionSummary`

```python
class TeamPositionSummary
```

Fresh-position geometry and completeness for one team.

Source: [src/gem/analysis/fight_positioning.py:127](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/fight_positioning.py#L127)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `team` | `int` | `-` |
| `expected_count` | `int` | `-` |
| `positioned_count` | `int` | `-` |
| `unpositioned_count` | `int` | `-` |
| `completeness` | `EvidenceCompleteness` | `-` |
| `centroid_x` | `float \| None` | `-` |
| `centroid_y` | `float \| None` | `-` |
| `rms_spread` | `float \| None` | `-` |

### `FightPositionSnapshot`

```python
class FightPositionSnapshot
```

All canonical hero evidence at one logical fight moment.

Source: [src/gem/analysis/fight_positioning.py:153](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/fight_positioning.py#L153)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `kind` | `SnapshotKind` | `-` |
| `tick` | `int` | `-` |
| `heroes` | `tuple[HeroPositionEvidence, ...]` | `-` |
| `radiant` | `TeamPositionSummary` | `-` |
| `dire` | `TeamPositionSummary` | `-` |
| `centroid_distance` | `float \| None` | `-` |
| `active_participant_centroid_x` | `float \| None` | `-` |
| `active_participant_centroid_y` | `float \| None` | `-` |

### `FightPositioning`

```python
class FightPositioning
```

Four evidence-aware positioning snapshots for one detected fight.

Source: [src/gem/analysis/fight_positioning.py:180](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/fight_positioning.py#L180)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `fight_index` | `int` | `-` |
| `start_tick` | `int` | `-` |
| `engagement_start_tick` | `int` | `-` |
| `first_death_tick` | `int` | `-` |
| `end_tick` | `int` | `-` |
| `engagement_start_source` | `EngagementStartSource` | `-` |
| `snapshots` | `tuple[FightPositionSnapshot, ...]` | `-` |

## Module `gem.analysis.bundle`

One-call bundle of gem's evidence-first post-parse analyses.

Source: [src/gem/analysis/bundle.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/bundle.py#L1)

### Top-level functions

### `analyze`

```python
def analyze(match: ParsedMatch) -> MatchAnalysis
```

Run every default post-parse analysis on a parsed match.

Source: [src/gem/analysis/bundle.py:51](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/bundle.py#L51)

### Top-level classes

### `MatchAnalysis`

```python
class MatchAnalysis
```

Results of every default post-parse analysis for one match.

Source: [src/gem/analysis/bundle.py:31](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/analysis/bundle.py#L31)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `smoke` | `list[SmokeAnalysis]` | `field(...)` |
| `roshan_conversions` | `list[RoshConversion]` | `field(...)` |
| `farming_routes` | `list[FarmingRoute]` | `field(...)` |
| `fight_positioning` | `list[FightPositioning]` | `field(...)` |
