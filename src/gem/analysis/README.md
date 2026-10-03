# gem.analysis

`gem.analysis` is the post-parse query layer of the replay parser. Every helper
here takes a finished `ParsedMatch` (or one of its parts) and answers a question
*about* a parsed game — "where was this hero at that tick?", "did the team have
vision of the cliff?", "what happened in the window after this Roshan?" — without ever
touching the binary stream, schema, or `ReplayParser`. It is the only package
whose functions are designed to be called *after* parsing is complete, by a
notebook, report, or downstream ML pipeline.

The package divides into two halves:

- **Cheap lookups** (`spatial.py`, `combat.py`, `abilities.py`, `formatting.py`)
  — near-instant point queries over already-collected fact lists.
- **Heavy, experimental builders** (`farming.py`, `roshan.py`, `smoke.py`,
  `fight_positioning.py`) — multi-pass scans that join many fact sources into
  new records (camp routes, Roshan windows, smoke lifecycles). They report facts;
  gem 0.13 removed the tags, scores and territory estimates that used to sit on
  top of them (HY-96).

A vision sub-area (`vision.py`) sits between the two and is explicitly an
**approximation**, not a replay-accurate measurement.

## Mental Model

The whole package obeys one contract: **operate on `ParsedMatch` facts; never
re-parse.**

```text
ReplayParser  ──parse──▶  ParsedMatch
                            (players, wards, towers, barracks, roshans,
                             tormentors, aegis_events, fights,
                             combat_log, vision_modifiers, ...)
                                   │
                                   │  read-only
                                   ▼
                            gem.analysis
                  ┌────────────────┴─────────────────┐
                  │                                   │
          cheap point lookups               heavy derived builders
   position_at_tick / heroes_near /     build_farming_routes /
   net_worth_at / fight_at_tick /       build_fight_positioning /
   group_ability_hits / ability_        build_rosh_conversions /
   level_at_tick / assess_point_vision  build_smoke_analysis
                  │                                   │
                  ▼                                   ▼
          tuples / lists /              new dataclasses
          small dataclasses             (FarmingRoute, RoshConversion,
                                         SmokeAnalysis, ...)
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
- `position_sample_at_tick(player, tick)` uses the same selection rule while
  retaining the chosen sample tick and absolute age for callers that must apply
  an explicit freshness policy.
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
- `fight_at_tick(match, tick)` binary-searches `match.fights` (assumed
  non-overlapping and sorted by `start_tick`) and returns the `Fight` whose
  `[start_tick, end_tick]` window contains `tick`, else `None`.
- `is_active_fight_participant(player_stats)` returns `True` when a
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
- `assess_point_vision(match, team, tick, x, y, ...)` is the primary point query.
  It returns `supported`, `unsupported`, or `incomplete`, retains sampled-position
  provenance and missing-evidence gaps, and optionally reports authoritative
  canonical-target visibility plus bounded direct-target reveals as separate
  evidence. Hero radius is day/night-adjusted (`_DAY_VISION = 1800` /
  `_NIGHT_VISION = 800`); observer wards use `_WARD_VISION = 1600`.
- `ward_vision_impact(ward, match)` counts *distinct* enemy heroes whose
  `position_log` samples ever fell inside the ward's 1600-unit radius during its
  alive window (squared-distance check against `_WARD_VISION_RADIUS_SQ`, one
  sighting per hero). Returns `0` for non-observer wards or wards with no
  coordinates. The docstring flags it as approximate: ~5 s sampling gaps, flat 2D
  radius (no terrain), and day-vision radius always used.

## Heavy Builders — Experimental (`farming.py`, `roshan.py`)

These are multi-pass scans that emit *new* derived dataclasses. Their window
boundaries and evidence categories are documented analytical choices, not
ground truth.

### Farming routes (`farming.py`)

- `build_farming_routes(match, config=DEFAULT_FARMING_ROUTE_CONFIG)` returns one
  `FarmingRoute` per player. It assigns sampled positions to calibrated camp
  zones with current-zone hysteresis, normalized-distance overlap resolution,
  and camp-ID tie breaking.
- Sample gaps over 300 ticks and implied speeds over 900 world units/second are
  hard discontinuities. Same-camp exits of at most 150 ticks may merge, while
  retaining their out-of-zone samples and `micro_exit_merged` provenance.
- Segment evidence keeps neutral damage/deaths, fresh XP and total-earned-gold
  endpoint deltas, sampled-window coverage, boundary reasons, and gaps. Missing
  resource endpoints stay `None`.
- `strong_farm_evidence`, `weak_farm_evidence`, and `transit_like` describe
  support strength only; they do not assert player intent or a complete clear.
  Resource changes remain visible but do not promote a brief touch by
  themselves, because they may be passive or earned away from the camp.
- Every segment also carries its camp's owner, lane and area, the catalog
  versions, and the contiguous distance travelled.
- The same public records feed the opt-in (`include=["analysis"]`)
  `farming_routes`, `farming_route_segments`, and `farming_route_points`
  DataFrames and the Farming report tab.

### Roshan conversion (`roshan.py`)

- `build_rosh_conversions(match)` returns one `RoshConversion` per entry in
  `match.roshans`. It associates Aegis only inside the 30-second post-kill
  boundary, caps ownership and analysis at the next Roshan/game end, and infers
  consume only from a holder death inside the bounded five-minute ownership
  horizon. The main analysis may include up to two minutes of aftermath, plus
  the rest of a fight containing an inferred consume.
- Team and Aegis lifecycle fields expose their attribution/inference source.
  `fight_evidence` uses engagement-aware starts, labels fights already underway,
  and retains participant IDs. Unknown structures and Tormentors remain counted
  but uncredited.
- `RoshDifferentialProfile` compares the attributed conversion team with its
  opponent over one hardened window. It exposes signed fight, weighted
  structure, net-worth, XP, forward-ward and Tormentor differentials, together
  with both teams' raw values. Optional resource values remain `None` when
  evidence is incomplete.
- Buybacks remain context/timeline annotations. Tormentor is a separate signed
  secondary-objective dimension and is not folded into the structure value.

## Shared Internals (`_shared.py`)

`_shared.py` holds the team constants and the small lookups several modules share:

- `_TEAM_RADIANT = 2`, `_TEAM_DIRE = 3` and the fountain positions (the
  `CDOTA_Unit_Fountain` entities, loaded from `map_constants.json`), which
  `region_of` falls back on when the region geometry is unavailable.
- `region_of(x, y)` lives in `regions.py` (public as `gem.region_of`) and returns one of `MAP_REGIONS` (public as `gem.MAP_REGIONS`): `"top_lotus"` /
  `"bottom_lotus"` within `lotus_radius` (700) of a lotus pool, `"river"` inside
  the river outline, otherwise `"radiant_half"` / `"dire_half"` by the side of
  the half line.
- `nearest_series_value(times, values, tick)` is a `bisect`-based parallel-array
  lookup (the `spatial.py` and `roshan.py` helpers inline their own
  near-identical scans rather than calling it).
- `infer_match_end_tick(match)` returns `match.game_end_tick` when set, else the
  latest tick observed across all players' `times` and `position_log`.

## Data Flow Notes

- Everything is read-only against `ParsedMatch`/`ParsedPlayer`. No function in
  this package mutates the match or calls back into the parser.
- The boundary with `extractors/` is **types only**: `combat.py` and `roshan.py`
  import `Fight` / `AegisEvent` (and `combat.py`'s `CombatLogEntry`,
  `roshan.py`'s `ParsedMatch`) under `if TYPE_CHECKING:`, so there is no runtime
  dependency on the extractor or results packages. The runtime imports outside
  `analysis` are the bundled map data: `gem.catalog.map` (camp zones, map
  constants) and `gem.state.game_clock`.
- `is_active_fight_participant` and `ward_vision_impact` deliberately accept
  `object` / duck-typed args (read via `getattr`) so they work with any
  stats/ward shape, not just the concrete extractor dataclass.

## What This Package Does Not Do

- **Read replay bytes / bits.** That is `binary` (`DemoStream`, `BitReader`).
- **Build serializers or decode entity fields.** That is `schema`.
- **Track string tables or entity lifecycle.** That is `state`.
- **Ingest the combat log.** Producing `CombatLogEntry` objects (S1 + S2 paths)
  is `combat`; this package only *reads* the finished `match.combat_log`.
- **Collect facts during a parse.** Sampling player snapshots, ward placements,
  fight windows, draft, objectives, etc. is `extractors`. Analysis only
  imports extractor result *types* (under `TYPE_CHECKING`).
- **Assemble `ParsedMatch` / export DataFrames/JSON/Parquet.** That is `results`
  (`assembly.py`, `dataframes.py`, `models.py`).
- **Render HTML reports.** That is `reports`; it *consumes* analysis output (and
  shares `_shared.py` constants), but the rendering lives there.
- **Resolve hero/item/ability/map names from IDs.** That is `catalog` (and the
  `constants` facade). `farming.py` and `regions.py` read map data through
  `catalog.map`; `format_npc_name` is only string munging, not a catalog lookup.

If a value looks wrong here, the bug is usually upstream: a missing
`position_log` sample, an empty `fights` list, or a mis-extracted ward — fix
it in the extractor that produced the field, not in the lookup that reads it.

## Common Pitfalls

### Point vision / `ward_vision_impact` are approximations, not truth
They do flat 2D radius checks with no high-ground, tree, or cliff modelling, and
sample positions only every ~1–5 seconds. `PointVisionStatus.UNSUPPORTED` means
"no *modelled* source", not a guaranteed fog state. Do not treat the geometry
output as replay-accurate visibility.

### Direct reveals are target evidence, not point coverage
`assess_point_vision(..., target_player_id=...)` reports defensible direct-target
modifier intervals separately from hero/observer geometry. Do not turn Track,
Corrosive Haze, Dust, or a carrier/aura record into general map coverage.

### `net_worth_at` scans linearly; `position_at_tick` bisects
`net_worth_at` uses an O(N) `min()` over `player.times`, while `position_at_tick`
and `fight_at_tick` use `bisect`. Don't assume all "at_tick" helpers share
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

### `fight_at_tick` assumes non-overlapping, sorted fights
It binary-searches on `start_tick` and checks a single candidate window. If the
`fights` list is unsorted or windows overlap, it can miss a containing fight.

### `region_of` is traced from one map image
The river outline was traced from the water in `assets/maps/Game_map_7.41.jpg`
(both Roshan pools included) and runs only between the top-lane and bottom-lane
crossings; the lanes are not river. The half line follows the river's middle and,
past its ends, runs straight out to the map edges. Lotus areas are 700-unit
circles round the `CDOTA_BaseNPC_LotusPool` entities and belong to neither half.
`scripts/trace_river_region.py` regenerates the outline and half line from the
image (`--check`, `--write`, `--overlay`); a map patch that moves the river needs
a new image and a re-run. Two camps' annotated owners
disagree with the terrain they sit in (camps 4 and 25); `region_of` follows the
terrain.

### The heavy builders encode documented choices
`build_rosh_conversions` and `build_farming_routes` choose window boundaries,
sample-gap limits and evidence categories. They are documented and inspectable,
not ground truth; read the raw counts and swings rather than treating any
category as a verdict. Interpretation (did this Roshan "convert"? was that farm
safe?) belongs outside gem; see the recipes in `examples/cookbook/`.

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
