# gem.analysis

`gem.analysis` is the post-parse query layer of the replay parser. Every helper
here takes a finished `ParsedMatch` (or one of its parts) and answers a question
*about* a parsed game — "where was this hero at that tick?", "did the team have
vision of the cliff?", "what did this Roshan convert into?" — without ever
touching the binary stream, schema, or `ReplayParser`. It is the only package
whose functions are designed to be called *after* parsing is complete, by a
notebook, report, or downstream ML pipeline.

The package divides into two halves:

- **Cheap lookups** (`spatial.py`, `combat.py`, `abilities.py`, `formatting.py`)
  — near-instant point queries over already-collected fact lists.
- **Heavy, experimental builders** (`map_context.py`, `roshan.py`) — multi-pass
  scans that synthesise new derived records (context buckets, Roshan-conversion
  summaries) from many fact sources at once.

A vision sub-area (`vision.py`) sits between the two and is explicitly an
**approximation**, not a replay-accurate measurement.

## Mental Model

The whole package obeys one contract: **operate on `ParsedMatch` facts; never
re-parse.**

```text
ReplayParser  ──parse──▶  ParsedMatch
                            (players, wards, towers, barracks, roshans,
                             tormentors, aegis_events, teamfights,
                             combat_log, vision_modifiers, ...)
                                   │
                                   │  read-only
                                   ▼
                            gem.analysis
                  ┌────────────────┴─────────────────┐
                  │                                   │
          cheap point lookups               heavy derived builders
   position_at_tick / heroes_near /     build_map_context_timeline /
   net_worth_at / teamfight_at_tick /   build_rosh_conversions
   group_ability_hits / ability_                  │
   level_at_tick / estimate_vision               ▼
                  │                     new dataclasses
                  ▼                     (MapContextBucket,
          tuples / lists /              CampVisitContext,
          small dataclasses             RoshConversion, ...)
```

Because the input is already a plain Python object graph, these helpers need no
parser changes to extend. Adding a new question is just adding a new function
that reads existing fields. That is the core reason this package exists
separately from `extractors/`: extractors *collect* facts *during* a parse;
analysis *interrogates* them afterwards.

The public surface is re-exported from `analysis/__init__.py`; most of it is
also surfaced at the top level of `gem` — `gem/__init__.py` does
`from gem.api import *`, and `gem.api` re-exports the analysis helpers (e.g.
`gem.position_at_tick`, `gem.build_rosh_conversions`).

## Cheap Lookups

These are O(log N) or single-pass helpers over a sorted/parallel fact list.

### Spatial (`spatial.py`)

- `position_at_tick(player, tick)` searches `player.position_log` (a list of
  `(tick, x, y)` tuples sampled ~1/sec) with `bisect`, returning the `(x, y)` of
  the nearest sample by tick distance, or `None` if the log is empty.
- `heroes_near(match, tick, x, y, radius)` calls `position_at_tick` for every
  player, keeps those within `radius` world units of `(x, y)`, and returns them
  in **ascending distance order**. Heroes with no position sample are skipped.
- `net_worth_at(player, tick)` does a *linear* `min()` scan over the parallel
  `player.times` / `player.net_worth_t` arrays (sampled ~1/sec) and returns the
  net worth at the nearest tick, or `0` if either array is empty.

### Combat (`combat.py`)

- `group_ability_hits(combat_log, window_ticks=5)` collapses the per-target
  `DAMAGE` entries of a single multi-target cast (Ravage, RP, etc.) into one
  `AbilityCast` dataclass. Only entries with a non-empty `inflictor_name` are
  considered (raw right-clicks have an empty inflictor); entries from the same
  `(attacker_name, inflictor_name)` pair within `window_ticks` of the cast's
  **start tick** (`existing.tick`, which is fixed at the first hit and not
  updated as more hits join) merge into the same cast. Default `5` (~1/6 s at
  30 ticks/s) suits AoE spells; the docstring suggests `10`–`15` for channelled
  abilities.
- `teamfight_at_tick(match, tick)` binary-searches `match.teamfights` (assumed
  non-overlapping and sorted by `start_tick`) and returns the `Teamfight` whose
  `[start_tick, end_tick]` window contains `tick`, else `None`.
- `is_active_teamfight_participant(player_stats)` returns `True` when a
  per-fight stats object has any of `deaths`, `damage_dealt`, `damage_taken`, or
  `healing` greater than 0 (read via `getattr(..., 0)`, so missing attributes
  count as 0). This encodes the "direct hero-vs-hero combat" definition shared
  with the HTML report.

### Abilities (`abilities.py`)

- `ability_level_at_tick(player, ability, tick)` reads
  `player._ability_snapshots` — a list of `(tick, {ability_name: level})` tuples
  built from per-minute snapshots — and returns the level from the latest
  snapshot whose tick is `<= tick` (so it is "last known level at or before the
  tick"). Returns `0` if snapshots are missing (the attribute is read with
  `getattr(..., [])` for older parsed data) or the ability is not yet learned.
  Ability names match the combat-log `inflictor_name` (e.g.
  `"axe_berserkers_call"`).

### Formatting (`formatting.py`)

- `format_npc_name(name)` strips the `npc_dota_`, `goodguys_`, and `badguys_`
  prefixes and turns underscores into spaces. It is for structures/neutrals; the
  docstring directs heroes to `gem.constants.hero_display()` instead.

## Vision — Explicit Approximations (`vision.py`)

`vision.py` is the package's honest fuzzy area. Its docstrings repeatedly state
that the results are heuristics with no terrain/high-ground modelling.

- `is_daytime(game_start_tick, tick)` computes the Dota day/night phase. The
  cycle is 10 minutes (`_DAY_NIGHT_CYCLE_TICKS = 18000`): day from 0:00, night
  from 5:00 (`_NIGHT_START_TICKS = 9000`), repeating. Tick 0 is daytime; the
  first night begins at tick 9000.
  (Reference: [Liquipedia — Time of Day](https://liquipedia.net/dota2/Time_of_Day).)
  `_is_daytime` is a backwards-compatible alias for the same function (kept
  because the dev branch exported the underscored name).
- `estimate_vision(match, team, tick, x, y)` returns a distance-sorted list of
  `VisionSource` dataclasses (`kind` ∈ `"hero" | "ward" | "modifier"`) for every
  allied unit that *could* see `(x, y)`. Hero radius is day/night-adjusted
  (`_DAY_VISION = 1800` / `_NIGHT_VISION = 800`); observer wards use a constant
  `_WARD_VISION = 1600`; modifier reveals (from `match.vision_modifiers`, e.g.
  Slardar Corrosive Haze, Track, Dust) report distance to the revealed hero with
  `vision_radius = 0` and **no radius gate**. The docstring quotes ~85–90%
  accuracy for the "was this initiation telegraphed or blind?" use case and lists
  what it does *not* model (high ground, ability vision, summon/creep vision,
  sentry true-sight).
- `ward_vision_impact(ward, match)` counts *distinct* enemy heroes whose
  `position_log` samples ever fell inside the ward's 1600-unit radius during its
  alive window (squared-distance check against `_WARD_VISION_RADIUS_SQ`, one
  sighting per hero). Returns `0` for non-observer wards or wards with no
  coordinates. The docstring flags it as approximate: ~5 s sampling gaps, flat 2D
  radius (no terrain), and day-vision radius always used.

## Heavy Builders — Experimental (`map_context.py`, `roshan.py`)

These are multi-pass scans that emit *new* derived dataclasses. They are the
experimental, opinionated end of the package (scoring weights and thresholds are
hand-tuned, not ground truth).

### Map context (`map_context.py`)

- `build_map_context_timeline(match, team, bucket_ticks=900, presence_window_ticks=2700)`
  sweeps the game in fixed-width buckets (default 30 s) and, for each, emits a
  `MapContextBucket` with tower-alive counts, T1-mid state, last Roshan/Tormentor
  kill ticks, aegis-holder state, per-team observer counts, net-worth/XP
  advantage, and decayed enemy presence per region. It maintains running
  counters (`towers_alive`, `t1_mid_alive`, aegis bookkeeping) across buckets and
  validates `team ∈ {2, 3}` and positive bucket/window sizes (raises
  `ValueError`).
- `score_camp_visit_context(*, team, camp_id, camp_type, neutral_kills, neutral_damage, xp_gain, bucket)`
  turns a single camp visit plus its overlapping bucket into a `CampVisitContext`
  with three `0–1` scores (`farm_safety_score`, `pressure_score`,
  `expected_value_score`), a categorical `context_label` (one of six values like
  `safe_home_farm` … `high_risk_invade`), and a list of explainability
  `context_drivers`. All scoring is a hand-weighted linear blend clamped via
  `_clamp01`.
- `world_in_bounds(x, y)` is a simple bounds check against the calibrated map
  rectangle.
- Camp geometry comes from `gem.catalog.map.load_neutral_camp_centers()`, loaded
  once into module-level `_CAMP_CENTERS`.

### Roshan conversion (`roshan.py`)

- `build_rosh_conversions(match)` returns one `RoshConversion` per entry in
  `match.roshans`, answering "did this Roshan convert into fights / objectives /
  map control / a closing sequence?" For each kill it associates the nearest
  `AegisEvent` (within `_ASSOCIATION_WINDOW_TICKS = 30 s`), resolves the holder
  team/hero, decides the aegis `fate` (`consumed` via a holder DEATH in the
  combat log / `expired` / `denied` / `game_end` / `unknown`), then tallies
  fights won/lost/drawn, towers, barracks, forced enemy buybacks, enemy-half
  observer delta, and enemy-half farm-share shift across the advantage window. It
  produces a 0–100 `conversion_score`, a `conversion_label`, an `aegis_outcome`,
  human-readable `drivers`, and a sorted `timeline_events` list of
  `RoshTimelineEvent`. Key windows: aegis duration `_AEGIS_DURATION_TICKS = 5 min`,
  immediate-outcome `_IMMEDIATE_WINDOW_TICKS = 180 s`, post-consume grace
  `_POST_CONSUME_GRACE_TICKS = 30 s` (all at 30 ticks/s).

## Shared Internals (`_shared.py`)

`_shared.py` holds map-geometry constants and the small lookups that were
previously duplicated between `roshan.py`, `map_context.py`, and
`reports/_sections.py`:

- `_TEAM_RADIANT = 2`, `_TEAM_DIRE = 3` and the calibrated map bounds
  (`_MAP_XMIN/XMAX/YMIN/YMAX`), fountain positions, and `_RIVER_STRIP`.
- `region_of(x, y)` classifies a point as `"river"` (when `|x - y| <=
  _RIVER_STRIP`) or, otherwise, the half of whichever fountain is nearer
  (`"radiant_half"` / `"dire_half"`).
- `nearest_series_value(times, values, tick)` is the `bisect`-based parallel-array
  lookup used by `map_context.py` (the `spatial.py` and `roshan.py` helpers
  inline their own near-identical scans rather than calling it).
- `infer_match_end_tick(match)` returns `match.game_end_tick` when set, else the
  latest tick observed across all players' `times` and `position_log`.

## Data Flow Notes

- Everything is read-only against `ParsedMatch`/`ParsedPlayer`. No function in
  this package mutates the match or calls back into the parser.
- The boundary with `extractors/` is **types only**: `combat.py` and `roshan.py`
  import `Teamfight` / `AegisEvent` (and `combat.py`'s `CombatLogEntry`,
  `roshan.py`/`map_context.py`'s `ParsedMatch`) under `if TYPE_CHECKING:`, so
  there is no runtime dependency on the extractor or results packages. The one
  real runtime import outside `analysis` is
  `map_context.py` → `gem.catalog.map.load_neutral_camp_centers`.
- `is_active_teamfight_participant` and `ward_vision_impact` deliberately accept
  `object` / duck-typed args (read via `getattr`) so they work with any
  stats/ward shape, not just the concrete extractor dataclass.

## What This Package Does Not Do

- **Read replay bytes / bits.** That is `binary` (`DemoStream`, `BitReader`).
- **Build serializers or decode entity fields.** That is `schema`.
- **Track string tables or entity lifecycle.** That is `state`.
- **Ingest the combat log.** Producing `CombatLogEntry` objects (S1 + S2 paths)
  is `combat`; this package only *reads* the finished `match.combat_log`.
- **Collect facts during a parse.** Sampling player snapshots, ward placements,
  teamfight windows, draft, objectives, etc. is `extractors`. Analysis only
  imports extractor result *types* (under `TYPE_CHECKING`).
- **Assemble `ParsedMatch` / export DataFrames/JSON/Parquet.** That is `results`
  (`assembly.py`, `dataframes.py`, `models.py`).
- **Render HTML reports.** That is `reports`; it *consumes* analysis output (and
  shares `_shared.py` constants), but the rendering lives there.
- **Resolve hero/item/ability/map names from IDs.** That is `catalog` (and the
  `constants` facade). `map_context.py` calls into `catalog.map` for camp
  centres; `format_npc_name` is only string munging, not a catalog lookup.

If a value looks wrong here, the bug is usually upstream: a missing
`position_log` sample, an empty `teamfights` list, or a mis-extracted ward — fix
it in the extractor that produced the field, not in the lookup that reads it.

## Common Pitfalls

### `estimate_vision` / `ward_vision_impact` are approximations, not truth
They do flat 2D radius checks with no high-ground, tree, or cliff modelling, and
sample positions only every ~1–5 seconds. An empty `estimate_vision` result
means "no *modelled* vision", not a guaranteed fog state. Do not treat their
output as replay-accurate vision.

### `modifier` vision sources have `vision_radius = 0` and no radius check
In `estimate_vision`, a modifier-revealed enemy hero is *always* added as a
source regardless of how far the query point is from that hero — the `distance`
field is informational only. This is intentional (the modifier grants direct
vision of the hero), not a missing radius gate.

### `net_worth_at` scans linearly; `position_at_tick` bisects
`net_worth_at` uses an O(N) `min()` over `player.times`, while `position_at_tick`
and `teamfight_at_tick` use `bisect`. Don't assume all "at_tick" helpers share
the same cost or that the arrays are interchangeable.

### `ability_level_at_tick` reads a private attribute
It depends on `player._ability_snapshots`. If that attribute is absent (older
parsed data, or a hand-built `ParsedPlayer`), it silently returns `0` rather than
raising. A constant `0` for a hero you know levelled the spell usually means the
snapshots were never populated.

### `group_ability_hits` ignores auto-attacks by design
Entries with an empty `inflictor_name` (raw right-clicks) are dropped, and the
merge key is `(attacker_name, inflictor_name)`. The window is measured from the
cast's start tick (the first hit), not from the most recent hit, so a long
sustained stream of hits from one `(attacker, ability)` pair will *not* keep
extending the same cast indefinitely. Two genuinely separate casts of the same
ability within `window_ticks` will merge; widen or narrow `window_ticks` per
ability type (channelled spells need a larger window).

### `teamfight_at_tick` assumes non-overlapping, sorted fights
It binary-searches on `start_tick` and checks a single candidate window. If the
`teamfights` list is unsorted or windows overlap, it can miss a containing fight.

### `region_of` is geometric, not lane-aware
The river is just the diagonal strip `|x - y| <= 1200`; halves are
nearest-fountain. It does not know lanes, ramps, or the actual river polygon.
Camp/ward "enemy half" attribution inherits this coarseness.

### The heavy builders are experimental and weight-tuned
`score_camp_visit_context`, `build_map_context_timeline`, and
`build_rosh_conversions` encode hand-picked thresholds (e.g. `>= 3500` net-worth
"winning_state", `0.10` farm-share delta, the 0–100 score weights). Treat their
labels/scores as opinionated heuristics, not derived constants, and expect them
to change between releases.

## When To Add Code Here

Add code to `gem.analysis` when the change answers a *new question about an
already-parsed match* using fields that `ParsedMatch` already carries.

Good fits:

- a new point lookup over existing parallel arrays or fact lists (mirroring
  `position_at_tick` / `net_worth_at`);
- a new derived summary/scoring builder that scans existing facts (in the spirit
  of `build_rosh_conversions`);
- a refinement to a vision/region heuristic, clearly documented as an
  approximation.

Poor fits:

- needing data that isn't on `ParsedMatch` yet — add a field in the relevant
  **extractor** + `results` model first, then read it here;
- anything that requires re-reading the replay, the schema, or live entity state
  (that belongs in `binary`/`schema`/`state`/`extractors`);
- name/ID resolution tables (belongs in `catalog`);
- HTML/visual rendering (belongs in `reports`).

Keep new helpers read-only, keep extractor result types behind `TYPE_CHECKING`,
and push genuinely shared map constants into `_shared.py` rather than
re-declaring them.