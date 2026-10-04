# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Docs: Recipes** (HY-102). Three pages that each answer one question from
  gem's facts and pandas, with no tags, scores or deprecated APIs: whether the
  team that killed Roshan won the next fight, how fast each core farmed from 10
  to 20 minutes and where, and how often a smoke led to a kill. The code lives
  in `examples/cookbook/`, runs on one replay or many, and is tested.

- **Hero HP and mana over time** (HY-121). `ParsedPlayer.hp_t`, `max_hp_t`,
  `mana_t` and `max_mana_t` hold the hero's own health and mana at each sample
  (about one a second), parallel to `times`; HP is 0 while the hero is dead. The
  `player_timeseries` DataFrame gains `hp`, `max_hp`, `mana` and `max_mana`
  columns, and `PlayerTimeSeries` gains `max_hp_t` / `max_mana_t`. The values
  are read from the hero entity (`m_iHealth`, `m_iMaxHealth`, `m_flMana`,
  `m_flMaxMana`); JSON files written by older versions load with the lists
  empty, and their DataFrame columns are missing values rather than 0.

- **Fight timeline (experimental)** (HY-122). `gem.build_fight_timeline(match,
  start_tick, end_tick)` turns a window's combat log into typed records: each
  ability and item use with the heroes it hit and the damage it did to each,
  damage on heroes in half-second bursts (credited to the owner for summons and
  illusions), modifier windows (buffs, debuffs, stuns), deaths with the gold
  lost and the damage taken in the last ten seconds, the kill gold and XP paid
  on each death tick, and buybacks with their cost. A cast's hits are the one
  derived field: the heroes its own ability damaged or debuffed within three
  seconds. See the new Fight Timeline page.

### Changed

- **Docs site** (HY-110). The documentation at
  <https://whanyu1212.github.io/gem-dota/> is rebuilt in Astro with a new design:
  a light theme and a dark one that follows your system setting (or the toggle),
  site search, and sections for Guide, Recipes, Reference, Internals and the
  Changelog. Every existing URL and `#anchor` still works. The home page's
  figures come from a real TI2026 replay: gem's map model, the wards up at the
  match's biggest fight (with observer vision), and that fight played back
  (HY-119, HY-123): each hero's HP and mana, every cast with the heroes it hit
  and the damage it did, damage lines by type, disables, buffs and the gold at
  each death on the map, beside each hero's status and a feed you can filter,
  with a recap for each death. Click a hero to follow it. It also shows which
  heroes were smoked and which the enemy couldn't see (the replay's own
  visibility), starting from the smoke that led into the fight (HY-139), and
  every disable, debuff and buff a hero put on another, each with its duration,
  in the feed, with deaths and buybacks marked along the timeline (HY-140).

- **JSON `schema_version` is 4.** The `analysis` section no longer has
  `smoke_fights`, the farming segment `context`, or the Roshan tags, verdicts and
  territory fields. `load_json()` does not decode that section, so schema 3 files
  still load unchanged.
- **Roshan `analysis_status`** no longer turns `partial` because a territory
  window lacked position coverage (`before_territory_unavailable`,
  `during_territory_unavailable`), since territory is gone. On the 9 local
  fixtures no record's status changed.
- **`FarmingRouteSegment` uses `__slots__` again** (it gave them up in 0.12 for
  the deprecated `context` field).
- **`gem.analyze` is about 20 times faster** (HY-7). Farming routes no longer
  scan the whole combat log once per camp visit: neutral-creep deaths and damage
  are indexed by hero once, and each visit looks up its own window. Resource
  endpoints are found by binary search too. The routes are unchanged (identical
  output on all 9 local fixtures). With the 0.12 interpretation removed as well:

  | Fixture | 0.12.0 | Now |
  |---|---:|---:|
  | 8856501050 (92:56) | 164.0 s | 6.6 s |
  | 8974053011 (38:00) | 27.5 s | 1.2 s |

### Removed

Everything deprecated in 0.12 (HY-96, HY-103). gem presents facts; for examples
of answering questions from them, see the Recipes docs.

- **Map context:** the `gem.analysis.map_context` module,
  `build_map_context_timeline`, `score_camp_visit_context`, `MapContextBucket`,
  `CampVisitContext` and `gem.analysis.world_in_bounds`.
- **`estimate_vision`.** Use `gem.assess_point_vision(...).sources`.
- **Farming segment context:** the `gem.analysis.farming_context` module,
  `FarmingRouteSegment.context`, `FarmingSegmentContext`, `FarmingContextTag`,
  `FarmingContextConfig`, `DEFAULT_FARMING_CONTEXT_CONFIG` and
  `build_farming_routes(context_config=...)`. In the DataFrames, the
  `farming_context_tags` table and the `context_*`, presence, point-vision,
  tower, advantage, Aegis, Roshan, Tormentor and territory columns of
  `farming_route_segments`.
- **Smoke-fight insights:** the `gem.analysis.smoke_fight` module,
  `build_smoke_fight_insights` and its 15 types, `MatchAnalysis.smoke_fights`,
  and the `smoke_fight_insights`, `smoke_fight_members` and
  `smoke_fight_followups` tables. Use `SmokeAnalysis.first_fight`.
- **Roshan tags, verdicts and territory:**
  - the `gem.analysis._territory` module;
  - on `RoshConversion`: `conversion_tags`, `conversion_score`,
    `conversion_label`, `aegis_outcome`, `drivers` and
    `enemy_half_farm_share_before` / `_during` / `_delta`;
  - on `RoshDifferentialProfile`: `tags`, `tag_ruleset`, `before_territory`,
    `during_territory` and the six coverage and depth swings;
  - `RoshTagThresholds`, `DEFAULT_ROSH_TAG_THRESHOLDS`, `RoshTerritoryConfig`,
    `RoshTerritoryWindow`, `RoshCoverageCell`, the `ROSH_TAG_*` constants, and
    `build_rosh_conversions(tag_thresholds=..., territory_config=...)`;
  - the `roshan_conversions` columns `aegis_outcome`, the four `*_coverage_pct`
    columns, `coverage_swing_pct`, `depth_swing`, `conversion_tags`,
    `tag_ruleset` and `legacy_conversion_score` / `_label`.
- **The 0.10 `teamfights` names**, renamed to `fights` in 0.11:
  - `ParsedMatch.teamfights` and the `teamfights=` keyword;
  - `MatchAnalysis.teamfight_positioning` and `SmokeAnalysis.first_teamfight`,
    attributes and keywords;
  - `Teamfight`, `TeamfightPlayer`, `detect_teamfights`, `teamfight_at_tick`,
    `is_active_teamfight_participant`, `TeamfightPositioning` and
    `build_teamfight_positioning`;
  - the `gem.extractors.teamfights` and `gem.analysis.teamfight_positioning`
    modules;
  - the `teamfights`, `teamfight_players` and `teamfight_positioning` table
    names in `build_dataframes` and `read_parquet_table`;
  - the rename helpers in `gem._deprecation`.

  JSON files with the old `teamfights` key still load as `fights`. OpenDota's
  `opendota_teamfights` and `teamfight_participation` are unchanged.
- **Calibration tooling for the removed heuristics.**
  - `scripts/calibrate_farming_context.py` is now `scripts/audit_farming_routes.py`,
    and its corpus is `tests/fixtures/opendota/farming_routes_corpus.json`. Both
    keep only the route facts.
  - The Roshan corpus drops its tag observations.
  - The Smoke/Fight Insights docs page is gone, and the calibration pages keep
    only the fact findings.

### Deprecated

- **`VisionSource`**, the return type of the removed `estimate_vision`, warns
  when imported from `gem` or `gem.analysis` and is removed in 0.14. Use
  `PointVisionSource`, from `gem.assess_point_vision(...).sources`.

- **The HTML report** (HY-136). `gem.reports`, `write_html_report`,
  `build_html_report`, `python -m gem reports` and `examples/match_report.py`
  warn and are removed in 0.14. The report's views move to the recipes on the
  docs site, each a question answered from the match's facts (HY-124).
  `import gem` no longer imports the report; `gem.reports` still works, and warns,
  until 0.14. The map calibration (`MAP_XMIN`…`MAP_YMAX`, `world_to_map_image`,
  `map_image_to_world`) moves to `gem.catalog.map`.

## [0.12.0] - 2026-10-03

gem now presents replay facts and leaves interpretation to you. The tags, scores
and verdicts layered on top of the facts are deprecated: the `map_context` API,
the farming segment context, the smoke-fight insights, the Roshan conversion
tags, verdicts and territory, and `estimate_vision`. They warn when used and are
removed in 0.13. The map is corrected underneath: the "river" region is the real
river (it was the mid lane), lotus pools are their own regions, and the neutral
camp catalog's types and owners now match the replays. `gem.region_of` and
`gem.MAP_REGIONS` are public. The HTML report is trimmed to facts, and replay and
icon downloads verify TLS certificates.

Upgrading from 0.11: deprecated names keep working with a `DeprecationWarning`
and are out of `__all__`; deprecated dataclass fields warn when read, while gem's
own JSON, DataFrame and report output stay silent and unchanged until 0.13.
Region labels and camp types and owners change with the corrected map, which
moves farming-route sides and Roshan territory numbers (see Fixed).
`map_constants.json` replaces `river_strip` with `regions`, `neutral_camps.json`
is removed (`load_neutral_camps()` reads `camp_zones.json`), and
`SmokeAnalysis.first_fight` now uses a 60-second in-game window. The JSON schema
is unchanged (`schema_version` 3). Python 3.10+ support is preserved.

### Fixed

- **`SmokeAnalysis.first_fight` measures its 60-second window in in-game time.**
  It used 1,800 replay ticks. Pauses stop the game clock but not the ticks, so a
  fight 50 in-game seconds after a smoke could be missed when a pause fell in
  between.
- **Replay fetching now verifies TLS certificates.** `gem.replays.fetch`
  (`fetch_replay`, `fetch_replay_url`, `download_and_decompress`,
  `fetch_opendota_match`, `enrich_with_api_rates`) used to turn off certificate
  and hostname checks for every request. That left the OpenDota API calls open
  to tampering.
  - **Verification.** Requests now use the system trust store, plus `certifi`'s
    roots when `certifi` is installed. `certifi` is not a new dependency.
  - **No CA bundle.** A certificate failure raises `urllib.error.URLError` with a
    hint: run Python's `Install Certificates.command` or `pip install certifi`.
  - **Replay downloads are still plain HTTP.** OpenDota's `replay_url` points at
    `http://replayNNN.valve.net/...`, and those Valve hosts do not accept TLS
    connections. No HTTPS host for the same files was found, so TLS cannot
    protect the replay bytes themselves. Only `https` URLs are verified.
  - **Tests.** The draft integration test now uses the same verifying context.

- **Report icon downloads now verify TLS certificates.** The hero and item icon
  downloader (`python -m gem reports assets download`, `scripts/fetch_*_icons.py`)
  used to turn off certificate and hostname checks, to cope with python.org macOS
  builds that ship without a CA bundle. That left the downloads open to tampering.
  - **Verification.** It now uses the system trust store, plus `certifi`'s roots
    when `certifi` is installed. `certifi` is not a new dependency.
  - **No CA bundle.** If no icon can be verified, the run still reports `FAIL` per
    icon, then prints one hint: run Python's `Install Certificates.command` or
    `pip install certifi`.
  - **CDN host.** `cdn.dota2.com` serves a certificate that does not cover its own
    name, so it only worked with checks off. Item icons (where it was the first
    URL) and the hero fallback now come from `cdn.cloudflare.steamstatic.com`. The
    files are byte-identical, and every hero and item icon still downloads.

- **The analysis "river" region is now the river.** It used to be a band along
  the `x = y` diagonal. That band was really the mid lane: it held both mid T1
  towers, while the power runes and Roshan pits fell into a team half.
  - **River.** The region is now the river traced from the 7.41 map image. It
    runs from the top-lane crossing to the bottom-lane crossing, and includes
    both Roshan pools.
  - **Halves.** They are split by a line along the river's middle, which
    continues straight out to the map edges past the river's ends.
  - **Lotus pools.** A new `top_lotus` / `bottom_lotus` area covers 700 units
    round each lotus pool. Both teams contest it, so it belongs to neither half.
  - **Effect on analysis.** The change reaches Roshan territory coverage, the
    enemy-half ward and farm checks, farming `territorial_advance`, and map
    context `enemy_presence_by_region`. That dict now also has `top_lotus` and
    `bottom_lotus` keys. `score_camp_visit_context` reads only the halves and
    `"river"` from it, so enemy heroes in a lotus area no longer count towards
    its safety or pressure.
  - **Measured on the 9 local fixtures:**
    - `territorial_advance` goes from 1,812 to 1,924 of 8,391 farming segments
      (202 gained, 90 lost).
    - Roshan `vision_expansion` goes from 15 to 18 of 31 conversions; no other
      Roshan tag changes.
    - Roshan `enemy_half_observer_delta` changes on 12 of 31 conversions, and
      the enemy-half farm shares and territory values on all 31.
    - 18 deprecated `conversion_score`s move. Two deprecated
      `conversion_label`s flip: 8855188139 Roshan 1 goes from `map_squeeze` to
      `low_conversion`, and 8855242704 Roshan 1 from `low_conversion` to
      `map_squeeze`.
    - Smoke, smoke-fight and fight-positioning output does not change.
- **The neutral camp catalog now matches the replays** (`camp_zones.json`
  version 4). Each camp's type was checked against its spawner and the creeps
  that spawn there, using the camp compositions on Liquipedia's Neutral Creeps
  page. Each owner was checked against the combat log's `neutral_camp_team`.
  - **Camp 10 is a medium camp,** not large. Its zone shrinks to the medium
    ellipse.
  - **Owners.** Camps 4 and 25 had their owners swapped: 4 is Dire's and 25 is
    Radiant's. Camps 12 and 17 had no owner; they are Radiant's and Dire's. Each
    side now owns 14 camps with the same mix of types.
  - **`gem.catalog.load_neutral_camps()`** returned out-of-date types for 7
    camps (2, 5, 6, 20, 22, 26, 28). It is now built from `camp_zones.json`, and
    `neutral_camps.json` is removed.
  - **Effect on farming routes, measured on the 7 corpus matches:**
    - `border` segments go from 767 to 0;
    - `own_side` goes from 3,145 to 3,532, and `enemy_side` from 1,936 to 2,282;
    - `territorial_advance` goes from 1,378 to 1,607, mostly at camps 12 and 17;
    - the segment total goes from 5,848 to 5,814, because camp 10's zone is
      smaller.
- **`scripts/audit_camp_annotations.py`** no longer reports a flooded camp as an
  ancient camp when it evolves into ancient frogs (camp 16).
- **The report's Laning map puts each hero on its lane.** It used to place a hero
  at the average of all its first-10-minute positions. Time in base, rotations
  and the L-shaped side lanes pulled that average into the river or jungle.
  - **Placement:** each hero now sits at its busiest spot inside its assigned
    lane.
  - **Overlaps:** lane partners' icons are spread apart, and a dot with a short
    line marks each hero's true spot.
- **Reports say which icons are missing.** A stale icon cache used to show
  some heroes and items as names with no notice (Kez, Largo, Muerta, Primal
  Beast and Ringmaster for a cache older than them). `build_html_report` now
  logs one warning naming the missing icons that can be downloaded.

### Added

- **`gem.region_of(x, y)` and `gem.MAP_REGIONS` are public.** `region_of` maps
  a world position to `river`, `radiant_half`, `dire_half`, `top_lotus` or
  `bottom_lotus`. It is a fixed lookup, checked against replay entities, so it
  belongs with gem's facts. It moves from the private `gem.analysis._shared` to
  the new module `gem.analysis.regions`, which the API reference documents.
- **`scripts/trace_river_region.py`** regenerates the river outline and half
  line from the map image. `--check` compares the trace with
  `map_constants.json`, `--write` updates it, and `--overlay` saves a preview.
  It needs OpenCV, which is not a project dependency:
  `uv run --with opencv-python-headless python scripts/trace_river_region.py --check`.
- **`gem.reports.fetch_match_icons(match, assets)`** downloads the hero and
  item icons one match needs into the report asset cache, skipping any already
  there, and returns the assets to render with. `gem.reports.match_icon_shorts`
  lists those icons. `examples/match_report.py` now fetches them before
  rendering; pass `--offline` to skip it. Icons are Valve's artwork, so gem
  still downloads them on the user's machine instead of shipping them.
- **Docs: Map Regions and Camps.** The page shows gem's regions and neutral
  camps on the 7.41 map, and explains how each was checked against the replays.

### Changed

- **New logo and README banner.** The logo is a cut emerald rendered as glass:
  shaded facets, a reflection in the table and lit edges
  (`docs/public/logo.svg`). The docs site's favicon is a heavier version that
  stays legible at 16 px (`docs/public/favicon.svg`).
  The banner pairs it with the wordmark and tagline over the real 7.41 map,
  annotated with gem's own river, halves, lotus pools and camps.
  `scripts/render_readme_banner.py` renders it (text set in Inter and converted
  to outlines). The README's report screenshots are retaken from the current
  report, and its feature list now describes facts rather than the deprecated
  interpretation.
- **`map_constants.json`** (`gem.catalog.load_map_constants()`): `river_strip`
  is replaced by `regions`, which holds `river_outline`, `half_line`,
  `lotus_pools` and `lotus_radius`.
- **`scripts/render_camp_zones_overlay.py`** places camps with the report
  maps' calibrated projection, on `assets/maps/Game_map_7.41.jpg` by default.
  It used to stretch the map over `camp_zones.json`'s `world_bounds`, which
  drew camps up to 115 px from where they are. New options:
  - `--regions` also draws the halves, river and lotus areas;
  - camp IDs sit on chips coloured by owner;
  - `--width` and `--margin` size the output.

  `camp_zones.json` drops `world_bounds` and `source_image`, which only this
  script read.
- **The HTML report shows facts and leaves interpretation to the reader**
  (HY-105). The analysis it no longer renders stays available in Python and the
  DataFrame exports.
  - **Farming** shows each team's cores only. For each team and lane role
    (safe lane → carry, mid → mid, off lane → offlaner), the core is the player
    with the most last hits at 10:00. Each camp visit shows its duration, the
    hero's neutral kills in the camp zone, and the gold and XP earned during the
    visit. The evidence, context-tag and context-evidence columns, the "Why
    these tags?" details and the legacy heuristic reference are gone.
  - **Roshan** (was "Roshan Conversion") is one table:
    - each kill's time, killing team and hero, and drops;
    - the Aegis holder and pickup time;
    - when and how the Aegis ended, with `*` when consumption is inferred;
    - the fights during the hold, and the enemy buildings the holder's team
      destroyed in it (denies excluded).

    A denied Aegis counts as never held. The tags, balance and resource panels,
    occupancy maps, timeline and differential summary table are gone.
  - **Smoke Operations** shows each smoke's time, team, members, when it broke,
    and its first fight (number, in-game delay, winner). These come from
    `SmokeAnalysis.first_fight` rather than the deprecated smoke-fight insights.
    The visibility, nearest-enemy, member-timing and bounded-fight evidence
    columns are gone.
  - **Fight cards** are badged "after Smoke #N" and "during Aegis #N" instead
    of the smoke-fight status and Roshan window-relation labels.
  - The **ward table** drops "Enemies seen".
  - **Map image:** the embedded image is downscaled to 4096 px wide
    (`gem.reports.assets.REPORT_MAP_MAX_WIDTH`). On a TI replay the map drops
    from 12.4 MB to 5.4 MB of the report. The image file is not modified.
  - `build_smokes(..., analyses=)` and `build_fights(..., smokes=)` take
    `SmokeAnalysis` lists in place of `SmokeFightInsight` lists.
    `build_rosh_conversion(match, conversions)` drops its `map_b64` argument.

### Deprecated

gem presents replay facts; the interpretation layer (tags, scores, verdicts) is
leaving the library (HY-96). Deprecated names still work in 0.12, warn with a
`DeprecationWarning` when used, are no longer in `__all__`, and are removed in 0.13.
Deprecated fields (such as `FarmingRouteSegment.context`,
`MatchAnalysis.smoke_fights` and `RoshConversion.conversion_tags`) warn when read. Printing, comparing or serializing an object does not warn, and
gem's own `analyze()`, report, JSON and DataFrame output stay silent.

- **`map_context` API:** `build_map_context_timeline`, `score_camp_visit_context`,
  `MapContextBucket`, `CampVisitContext` and `gem.analysis.world_in_bounds`.
  Nothing in gem uses them. The facts they combine (wards, towers, positions,
  `gem.region_of`) stay on `ParsedMatch`.
- **Farming segment context:** `FarmingRouteSegment.context`,
  `FarmingSegmentContext`, `FarmingContextTag`, `FarmingContextConfig`,
  `DEFAULT_FARMING_CONTEXT_CONFIG`, and `build_farming_routes(context_config=...)`,
  which warns when passed. Their DataFrame table `farming_context_tags` and the
  context columns of `farming_route_segments` go with them. The segments stay:
  camp, owner, lane, area, ticks, neutral kills and damage, XP and gold deltas,
  and evidence strength.
- **Smoke-fight insights:** `build_smoke_fight_insights` and its 15 types
  (`SmokeFightInsight`, `SmokeFightStatus`, `FollowUpWindow`, …),
  `MatchAnalysis.smoke_fights`, and the DataFrame tables `smoke_fight_insights`,
  `smoke_fight_members` and `smoke_fight_followups`. Use
  `SmokeAnalysis.first_fight` instead. The Smoke Analysis docs show how to get
  the delay and which smoked heroes fought.
- **Roshan conversion interpretation** (HY-99). On `RoshConversion`:
  `conversion_tags`, `conversion_score`, `conversion_label`, `aegis_outcome`,
  `drivers` and `enemy_half_farm_share_before` / `_during` / `_delta`. On
  `RoshDifferentialProfile`: `tags`, `tag_ruleset`, `before_territory`,
  `during_territory` and the coverage and depth swings. Also `RoshTagThresholds`,
  `DEFAULT_ROSH_TAG_THRESHOLDS`, `RoshTerritoryConfig`, `RoshTerritoryWindow`,
  `RoshCoverageCell`, and `build_rosh_conversions(tag_thresholds=...,
  territory_config=...)`, which warn when passed.
  - The fields warn when read. `conversion_score` and `conversion_label`, which
    were deprecated in 0.9 without a date, now warn too.
  - The deprecated constructor arguments are optional now, and still accepted.
  - The `roshan_conversions` DataFrame columns `aegis_outcome`, the four
    `*_coverage_pct` columns, `coverage_swing_pct`, `depth_swing`,
    `conversion_tags`, `tag_ruleset` and `legacy_conversion_score` /
    `_label` go with them.
  - The facts stay: kill and attribution, Aegis lifecycle (`aegis_fate`,
    `aegis_fate_source`), window ticks, fights, structures, economy swings,
    forward wards, Tormentors, buybacks, drops, banner plants and
    `timeline_events`. `enemy_half_observer_delta`, a ward count, stays too.
- **`estimate_vision`:** the same coordinate query is
  `gem.assess_point_vision(...).sources`. For what a team could actually see, use
  `gem.hero_visibility_at` / `gem.entity_visibility_at`.

## [0.11.0] - 2026-10-02

Brings gem's OpenDota-compatible output to parity, and fixes the ward and kill
attribution underneath it. On the 8 local OpenDota fixtures (80 players), 105 of
the 108 fields both parsers produce now match exactly; the other 3 (`kills_log`,
`killed`, `killed_by`) differ only where OpenDota counts a death the hero came
back from as a kill. gem's own fight list is renamed `fights` and can be
regrouped after parsing with `gem.find_fights`; `opendota_teamfights` now equals
OpenDota's teamfights. Players gain a gold ledger with exact buyback costs, and
`multi_kills`, `kill_streaks` and `killed_by`.

Upgrading from 0.10: `match.teamfights` is now `match.fights`, and the other
"teamfight" names for gem's own fights are renamed too (see Changed). The old
names keep working with a `DeprecationWarning` for this release, except Parquet
file names (`fights.parquet`) and the keys of the `to_json` `analysis` section.
JSON output is `schema_version` 3; files from 0.10 still load, with an empty
`lane_pos`, which is now OpenDota's `{x: {y: count}}` cell map. `lane_role` has
no roaming value (5); use `is_roaming`. `kills_log` no longer lists deaths the
target came back from, ward kills and expiries are reattributed, and DataFrame
columns use pandas nullable dtypes. Python 3.10+ support is preserved.

### Added

- **`ParsedPlayer.multi_kills`, `kill_streaks` and `killed_by`**, OpenDota's
  per-player fields of the same names.
  - `multi_kills` (`{kills in the chain: count}`) and `kill_streaks` (`{streak
    length: count}`) come from the combat log's own MULTIKILL and KILLSTREAK
    entries (wire types 15 and 16), which gem now decodes as
    `CombatLogType.MULTIKILL` / `KILLSTREAK` instead of `UNKNOWN`. They match
    OpenDota for 80 of 80 players on the local fixtures.
  - `killed_by` (`{unit: count}`) names what killed the player's hero, keyed on
    the combat log's damage source (the owning hero for a summon's kill). Like
    `kills_log`, it leaves out deaths the hero came back from, so it differs from
    OpenDota on the same 3 of 80 players, where OpenDota counts one such death.
  - The `player_breakdown` DataFrame gains rows for all three. The audit now
    compares 108 fields, 105 exactly.
- **`gem.find_fights(match, window_s=15, radius=3000.0)`** regroups a parsed or
  loaded match's hero deaths into fights with your own settings, without parsing
  again. Filtering `match.fights` can only drop fights; on the 8 local OpenDota
  fixtures the default 3,000-unit radius splits 13 of OpenDota's 37 teamfights into
  smaller pieces, which a filter cannot put back together. `radius=None` groups by
  time only, as OpenDota does. With the defaults it returns exactly `match.fights`
  (checked on all 8 fixtures, including matches loaded from JSON).
  `detect_fights` takes the same `window_s` and `radius` keyword arguments, and
  `FIGHT_WINDOW_S` / `FIGHT_RADIUS` are the defaults. The radius is inclusive: a
  death exactly `radius` from a fight's centre joins it (before, it had to be
  strictly closer, which no real replay hit).
- `scripts/audit_opendota_parity.py`: an offline, field-by-field comparison of
  gem's output with OpenDota's parsed match JSON on the local replay fixtures. It
  maps gem's format onto OpenDota's (per-minute arrays, log entries as
  `(key, time)`, the `item_` prefix, …), compares every other shared field as-is,
  and can cache parses and compare against a previous run. It found the gaps
  fixed in this release and those still open.
- **Per-player gold ledger.** `ParsedPlayer.gold_ledger` (`gem.GoldLedger`) breaks
  each player's gold down using the running totals the replay's team data keeps per
  player:
  - earned by source: hero kills, lane creeps, neutrals, passive income, buildings,
    Roshan, bounty runes, wards, couriers, abilities, comeback, denies, other, plus
    shared gold;
  - spent on items, consumables, support items and buybacks;
  - lost on death.

  `final` (a `gem.GoldLedgerSnapshot`) is read at the game-end tick, and
  `per_minute` runs parallel to `game_times_min`. A ledger with any field missing is
  `None`, never zero-filled.

  The values agree with the replay's postgame summary on all 9 local OpenDota
  fixtures: items + consumables equals `gold_spent` for 90 of 90 players, and the
  earned sources sum to total earned gold. DataFrames gain an opt-in
  `include="gold_ledger"` group (`player_gold_ledger`,
  `player_gold_ledger_minutes`).
- `ParsedPlayer.gold`: unspent gold at game end, OpenDota's `gold`. It comes from
  the postgame summary when present, else the last dense sample. `player_summary`
  gains a `gold` column.

### Changed

- **gem's own fight list is `fights`, not `teamfights`.** It holds every fight gem
  detects, and 70% of them (173 of 246 on the local fixtures) are single pickoffs,
  so "teamfight" promised something the list is not. What counts as a teamfight is
  the user's filter (deaths, active participants) or `find_fights` grouping.
  "Teamfight" names now mean OpenDota's definition only: `opendota_teamfights`,
  `OpenDotaTeamfight`, `detect_opendota_teamfights` and `teamfight_participation`
  are unchanged.

  | Old name | New name |
  | --- | --- |
  | `ParsedMatch.teamfights` | `ParsedMatch.fights` |
  | `Teamfight`, `TeamfightPlayer` | `Fight`, `FightPlayer` (now exported from `gem`) |
  | `detect_teamfights` | `detect_fights` |
  | `teamfight_at_tick` | `fight_at_tick` |
  | `is_active_teamfight_participant` | `is_active_fight_participant` |
  | `TeamfightPositioning`, `build_teamfight_positioning` | `FightPositioning`, `build_fight_positioning` |
  | `MatchAnalysis.teamfight_positioning` | `MatchAnalysis.fight_positioning` |
  | `SmokeAnalysis.first_teamfight` | `SmokeAnalysis.first_fight` |
  | `gem.extractors.teamfights` | `gem.extractors.fights` |
  | `gem.analysis.teamfight_positioning` | `gem.analysis.fight_positioning` |
  | DataFrame tables `teamfights`, `teamfight_players`, `teamfight_positioning` | `fights`, `fight_players`, `fight_positioning` |

  The old names still work and emit a `DeprecationWarning`; they will be removed in
  a future release. That covers the module attributes, both old modules, the
  `ParsedMatch` / `MatchAnalysis` / `SmokeAnalysis` attributes and constructor
  keywords (e.g. `ParsedMatch(teamfights=...)`), the DataFrame dict (indexing and
  `.get`) and `read_parquet_table`. Not covered: Parquet file names
  (`parse_many_to_parquet` now writes `fights.parquet`), the `analysis` section of
  `to_json` output
  (`fight_positioning`), and the internal report builder
  `gem.reports.sections.build_teamfights` (now `build_fights`).
  - The JSON `schema_version` is now 3 and the top-level key is `fights`.
    `load_json` / `from_dict` still read the `teamfights` key of older files.
  - The guide moved to `guides/06_fights` and the positioning page to
    `experimental/fight-positioning`.

- **Lanes are computed the way OpenDota computes them.** `lane_pos`, `lane_role`, and
  the new `lane` and `is_roaming` fields match OpenDota for 80 of 80 players on the local
  fixtures. Before, `lane_pos` never matched and `lane_role` matched for 71 of 80.
  - `ParsedPlayer.lane_pos` is now OpenDota's `{x: {y: count}}` map over map cells
    (world units / 128). It counts one position sample per second, read when OpenDota
    reads them, up to game time 600 s with the pre-game included. It used to be a flat
    `{"x_y": count}` map on a 64-unit grid. To get world coordinates, multiply a cell
    by 128.
  - `lane_role` no longer has a roaming value (5). Roaming is the new
    `ParsedPlayer.is_roaming` flag: the most common lane holds under 45% of the
    samples. `ParsedPlayer.lane` is OpenDota's lane: 1 bot, 2 mid, 3 top,
    4 Radiant jungle, 5 Dire jungle.
  - `classify_lane` is replaced by `gem.extractors.lane.assign_lane`, a port of
    OpenDota's lane grid.
  - `player_summary` gains `lane` and `is_roaming` columns.
  - Loading a JSON file from gem 0.10 or earlier (schema 1) leaves its `lane_pos`
    empty, because the old grid cannot be converted to cells.
- **Report maps line up with the 7.41 map image.** The HTML report placed positions up to
  about 290 world units (130 px) off, most visibly towards the Dire side. Its y scale was
  3% short, and the movement animation and the smoke and ward canvases stretched the
  image instead of cropping it like the other maps. The window is now calibrated against building positions read from a
  replay. Towers, outposts, ancients, fountains, lotus pools and the Tormentor land on
  their structures, within about 60 world units. The laning minimap marks roaming
  players with a dashed ring.

- **Buyback costs are exact.** The replay's team data counts each player's gold
  spent on buybacks. The counter rises on the BUYBACK entry's tick, by exactly the
  cost. `BuybackEvent.cost` now comes from that rise (`cost_exact=True`) on all 98
  buybacks across the local fixtures; the old estimate `200 + net_worth // 13` was
  off by up to ~8% and remains the fallback.
  - The new `BuybackEvent.reliable_gold` / `unreliable_gold` estimate how the
    buyback was paid. Dota spends unreliable gold first. The estimate is dropped
    (`None`) when a pool fell by more than it says was paid from that pool, e.g.
    after a purchase on the same update.
  - `player_buyback_log` gains `cost_exact`, `reliable_gold` and `unreliable_gold`
    columns. The HTML report marks estimated costs with `~` and shows the split
    as an estimate.
  - This corrects the documented claim that the cost and its split can't be
    recovered from a replay (issue #119).
- `ParsedPlayer.net_worth` comes from the postgame summary when present. It
  matches OpenDota exactly; the last dense sample was 1 gold off for one player
  on 8855188139. Without the summary, `gold_spent` falls back to the ledger's
  items + consumables instead of `0`.

- `ReplayParser` is smaller and simpler, with no behavior change:
  - It owns the `EntityTracker` from the start and hands it to the
    `EntityManager`, which gains an optional `tracker` argument. Before,
    registrations were forwarded through three layers, and the forwarding code
    existed twice.
  - The live game-clock and pause tracking moved to `GameClockTracker` in
    `gem.state.game_clock`, next to the `GameClock` it builds. The parser's clock
    attributes (`net_tick`, `game_time_s`, `game_clock`, `game_start_tick`,
    `combat_log_time_s`, `duration_s`) read from it.
- `CombatLogEntry.rune_type` holds the rune type of a `PICKUP_RUNE` entry (and the
  S2 combat log's own `rune_type` field when present). Rune pickups used to carry
  it only in `gold_reason`, which still holds it for compatibility. The
  `player_runes_log` DataFrame gains a `rune_type` column, and the HTML report
  reads it, falling back to `gold_reason` for matches loaded from older JSON.
- `GameEvent` has Pythonic field access: `event.get(name, default=None)`,
  `event[name]` (raises `KeyError`), `event.to_dict()`, and `event.name`. The
  `get_*` methods, which return a `(value, error)` pair, are unchanged.
  `get_int32` now also reads key types 8 and 9, the player identifiers
  (`userid`, `userid_pawn`) in events such as `player_team`, as Clarity does.
- New deep dive, "String Tables". It covers:
  - what the tables hold, and the three gem reads;
  - the create, update, and clear messages;
  - the bit-level entry format, and name compression, with a real example;
  - how `ActiveModifiers` entry names show which decoding rules are correct.

  The String Tables reference page lost its stray separators.
- New page, "Rust Kernel Plan". It collects the performance findings from the
  "How Entities Are Decoded" series:
  - where parse time goes, layer by layer;
  - what not to port;
  - a two-stage optional Rust kernel (`read_fields()`, then the per-entity packet
    loop), with illustrative upper bounds;
  - the exact-behaviour rules a kernel must keep;
  - packaging, adoption checks, and the Python-only wins available without Rust.

  It is a plan; nothing is implemented, and no speedup is promised.
- New deep dive, "How Entities Are Decoded, Part 5: Entity Lifecycle". It covers:
  - the entity packet: slot gaps and the 2-bit create/update/leave/delete command;
  - how an entity is created, from its class ID, serial, and class baseline;
  - `EntityOp` flags, and why full packets after the first are skipped;
  - slots, serials, and handles, including the invalid handle;
  - when handlers run within a packet, compared with Manta and Clarity;
  - the edge cases Clarity handles that never occurred in three full replays;
  - where the entity loop's time goes.
- Corrected the "Reading Entity State" guide. Most of its example field names
  don't exist in current replays (`m_iGold`, `m_iLastHitCount`, `m_bIsAlive`,
  `CDOTAGamerules.m_fGameTime`, the score fields), and its position formula
  disagreed with gem's (`cell × 128 + offset`). The tables now list names checked
  against a full replay, with team data, player resource, and game-rules paths.
- `Entity` no longer has the private `_state` dict. Only tests wrote to it, yet
  every field read checked it first. Entity values now live only in the
  `FieldState` tree. Tests build synthetic entities with `tests/_entities.py`
  (`set_fields`, `clear_fields`), so their reads go through the same schema
  resolution as a real replay. Parse output is byte-identical.
- New deep dive, "How Entities Are Decoded, Part 4: Field State". It covers:
  - how `read_fields()` decodes one update, including the class baseline applied
    on creation;
  - how a field path finds its decoder through the five field models, and the
    per-class decoder cache (99.76% hits on a 99-minute replay);
  - `FieldState` as a sparse tree of lists, and its growth rule;
  - how tables and arrays live in the tree, and how arrays shrink;
  - reading values back by name, and the "which fields changed" signal;
  - where the decode loop's time goes.

  A new Field State reference page covers `read_fields` and `FieldState`.
- Cleaned up the entity-decode layer. Parse output is byte-identical and speed is
  unchanged.
  - Inner-message unpacking moved from `gem.parser` into the new
    `gem.binary.packet` module. It is now public as
    `gem.binary.read_inner_messages()`.
  - `FieldState.get()` and `set()` now reuse the internal fast paths instead
    of duplicating them.
  - Removed dead and test-only helpers: the `FieldPath` decoder-resolver
    wrappers and their aliases, `FieldState._ensure()`, `_has_slot()` and
    `_is_child()`, and `state.entities._find_field_path()`.
  - `gem.schema.sendtable`, `gem.schema.field_path`, and
    `gem.schema.field_decoder` no longer re-export underscore-prefixed
    internals. Import those from their defining submodules. Public names
    (`__all__`) are unchanged.
- New deep dive, "How Entities Are Decoded, Part 3: Field Decoders": how each
  field's decoder is chosen, every decoder family with real fields (including how
  positions split into a cell and an offset), quantized-float flags and why their
  setup follows float32 while values stay float64, and the part-2 update's
  decoded values.
- New deep dive, "How Entities Are Decoded, Part 2: Field Paths": how an entity
  update says which fields changed, the 40 field-path operations, the Huffman
  code and gem's 17-bit lookup table, and a real update traced step by step
  from the committed TI14 fixture. Tests now pin all 40 Huffman codes to the
  ones Manta's `huffman.go` produces.
- New deep dive, "How Entities Are Decoded, Part 1: The Schema": what the
  send-table schema is, how the flattened symbols, fields, and serializers
  become gem's `Serializer`/`Field` tree, the five field models with real
  examples, nesting and naming, versions, and build patches. All figures and
  snippets use the committed TI14 fixture.
- Rewrote the Bits & Bytes Primer as a crash course for Python programmers:
  binary and hex, bit operations, byte order, LSB-first bitstreams, signed
  integers and zigzag, varints and `ubit_var`, quantized floats, prefix codes,
  and a decode-it-yourself exercise on real replay bytes, with "Try it"
  questions at the end of each section. Every snippet runs against the current
  code. The replay-layout material it duplicated now links to "How Proto Parsing
  Works". New `examples/bits_and_bytes_exercises.py`: 12 graded exercises that
  build a tiny bit reader, checked against real replay bytes and gem's
  `BitReader` (solutions in `examples/bits_and_bytes_solutions.py`).
- Removed the unused `BitReader.read_string_n`. It decoded Latin-1 while
  `read_string` decodes UTF-8.
- **DataFrame columns use pandas nullable dtypes** (`Int64`, `Float64`,
  `boolean`, `string`). Dtypes come from the source dataclass type hints
  (`CombatLogEntry`, `SmokeParticipant`, `VisionModifierEvent`, `ParsedPlayer`,
  ...) or from explicit per-table schemas for the hand-built tables. Missing
  values are `pd.NA` rather than `None`/`NaN`. Integer columns with gaps stay
  integers instead of becoming floats. `fight_positioning` (then `teamfight_positioning`) now joins
  `active_reveal_modifiers` and `evidence_gaps` with `";"` (they were tuples),
  and `opendota_teamfights.players` is a JSON string (it was a list of dicts
  keyed by hero, ability, and item names).
- Rewrote the Proto Cookbook docs for newcomers. "How Proto Parsing Works" now
  explains what protobuf is and walks through each layer of a replay with counts
  from a real match, ending with a traced first-blood packet. A new page, "The
  Proto Files gem Uses", explains where the 84 `.proto` files come from, maps all
  of them by family, and describes the 8 files gem reads, message by message.
- The Proto Field Atlas now marks every file as used by gem, loaded only as a
  dependency, or not used, and lists the used files first. The overlapping
  single-page "Full Proto Dota2 Catalog" and its generator were removed.

### Fixed

- **`kills_log` leaves out deaths the target came back from.** A hero with the
  Aegis or Wraith King's Reincarnation dies and comes straight back; the game flags
  that death `will_reincarnate` and leaves it off the scoreboard. gem listed it as
  a kill, so only 70 of 80 players' `kills_log` had as many hero kills as their
  scoreboard `kills`; now 80 of 80. `killed` already left these deaths out.
  - `kills_log` now matches OpenDota for 77 of 80 players, up from 73.
  - **Known difference from OpenDota.** OpenDota approximates this with an
    Aegis-holder rule (odota/parser `handleDeathCombat`) that loses track of the
    holder, so on 3 of the 80 players it counts one death the hero came back from
    as a kill (8855188139 Ember Spirit at 1865 s; Shadow Fiend at 3172 s on
    8855242704 and 4740 s on 8856501050). Its list is then one longer than the
    scoreboard; gem's matches the scoreboard. `killed` differs from OpenDota on the
    same 3 players for the same reason.

- **Ward kills and expiries are attributed correctly, and the ward-left logs match
  OpenDota.** `obs_left_log` and `sen_left_log` now match OpenDota for 80 of 80
  players on the local fixtures, up from 29 and 39; the audit is at 103 of 105
  fields.
  - **Killed vs expired.** A ward that expires logs a combat-log `DEATH` whose
    attacker is the ward itself. gem decided the ward's fate when its
    `m_lifeState` changed, which comes before that `DEATH` in the same tick, so
    the `DEATH` was left queued and the *next* ward of that class took it. On the
    8 audited fixtures this swapped killed and expired on 372 of 944 wards and gave
    99 more the wrong killer (e.g. 158 "killed" wards had lasted their full
    lifespan; now 1). As OpenDota does, a ward that leaves is now resolved once
    its tick is over, after that tick's combat log. Leave ticks are unchanged, so
    vision and map-context analysis are unaffected; the report's killed/expired
    labels and killer names change.
  - **`attackername`** is the `DEATH`'s damage source, as OpenDota logs it: the
    owner's hero for an expiry, the owning hero for a summon's kill. It is left
    out when no `DEATH` was paired. `WardEvent.left_attacker` holds it.
  - **Owner at leave time.** OpenDota reads the ward's owner when it leaves; when
    that owner entity is gone, the leave is logged for no player.
    `WardEvent.left_player_id` holds that slot (`-1` when unresolved), and the
    left logs use it.
  - The left logs are in the order wards left, not the order they were placed.

- **`life_state_dead`, `kda`, `teamfight_participation` and `max_hero_hit` match
  OpenDota** for 80 of 80 players on the local fixtures, up from 28, 78, 50 and 63.
  The audit is at 101 of 105 fields.
  - `life_state_dead` counts OpenDota's once-a-second interval reads (from game
    time 0 until post-game) where the hero is dying or dead. gem counted distinct
    dead seconds of its denser snapshots, which sample at different moments; that
    remains the fallback without interval reads. The interval reads now carry the
    hero's `m_lifeState`.
  - `kda` rounds an exact half up, as odota/core's JavaScript `toFixed(2)` does:
    (6 + 11) / 8 = 2.125 is now 2.13, not 2.12.
  - `teamfight_participation` is the game's float32 value as OpenDota's JSON holds
    it (0.65384614); gem had rounded it to 7 decimals (0.6538461).
  - `max_hero_hit` leaves out `inflictor` for an auto-attack, as OpenDota does,
    instead of the string `"null"`. The `player_summary` DataFrame's
    `max_hero_hit_inflictor` is now missing (NA) there.

- **`opendota_teamfights` matches OpenDota exactly.** It now equals OpenDota's
  `teamfights` on all 8 local fixtures, up from none. `match.fights` (previously
  `match.teamfights`), gem's own list of every fight, is unchanged. There were four differences:
  - **The game's final fight.** OpenDota closes a fight at its first once-a-second
    interval 15 s or more after the last death. The recording ends before that
    for the final fight, so OpenDota leaves it out. gem kept it, with its end clamped
    to the match duration (7 of 8 fixtures). It is now left out too.
  - **Deaths the hero comes back from.** gem skipped every reincarnation death.
    OpenDota only skips the Aegis holder's next death, and forgets the holder when
    `modifier_aegis_regen` appears. 8855188139 was missing OpenDota's fight at
    1847 s, whose three deaths include Ember Spirit's reincarnation.
  - **`deaths_pos`** is now in OpenDota's map cells (world units / 128), read
    from the victim's interval position in the death's second. It was in world
    coordinates. As in OpenDota, a death without an interval read in that second
    adds to neither `deaths` nor `deaths_pos`.
  - **`xp_start` / `xp_end`** are now the interval XP at exactly the fight's
    first and last second, not the nearest snapshot's.

  `PlayerExtractor` now reads OpenDota's once-a-second interval for the whole
  game, not just the first 600 s. `detect_opendota_teamfights` takes the new
  `interval_samples` and `aegis_events` arguments; without them it keeps the
  old approximation. `scripts/audit_opendota_parity.py` now compares
  `opendota_teamfights` with OpenDota's `teamfights` instead of comparing the
  number of gem's own fights.
- **`objectives` matches OpenDota.** `ParsedMatch.objectives` now equals OpenDota's
  on all 8 local fixtures, up from none. There were five causes:
  - **Tormentor kills credited the next kill's player.** The
    `CHAT_MESSAGE_MINIBOSS_KILL` chat event arrives just before its combat-log
    death, so it was pinned to the previous Tormentor kill, and the last kill had no
    player. `TormentorKill.killer_player_id` (and so `match.tormentors`) now pairs
    each chat event with its own death. The objective's `slot` and `team` come from
    the chat event, as OpenDota's do, so a kill by no player reads `slot` `-1`.
    On the 8 local fixtures, 11 of 13 Tormentor kills change player. Roshan
    conversions and farming context are unchanged, since they use the killer's
    team, which was already right. One smoke-fight follow-up changes its
    actor (8974053011).
  - **The Ancient was missing.** `building_kill` objectives now come from every
    combat-log building death OpenDota counts (towers, barracks, shrines and the
    Ancient). They are timed like the combat-log entry, which fixes two tower kills
    that were a second late. A kill with no killer name reads `unit`
    `"dota_unknown"`, as OpenDota prints it.
  - **Courier kills lacked `value`**, the bounty the chat event carries. `team` and
    `killer` also come from the chat event now.
  - **First blood could be the wrong death.** gem took the first hero death, but a
    hero killed by neutrals is not first blood. The objective now takes its killer
    and victim from the `CHAT_MESSAGE_FIRSTBLOOD` chat event, and adds OpenDota's
    `victim_player_slot`. Without the postgame summary, `first_blood_time` uses
    the death at that chat event too. On 8855188139 it was 240 s; it is now 344 s,
    as in OpenDota.
  - **Objectives in the same second follow replay order**, not building kills
    first.

  The `opendota_objectives` DataFrame gains `value` and `victim_player_slot`
  columns.
- **The fountain anchors are the fountains.** `map_constants.json` put the fountains
  at (9684, 9684) and (23120, 22350), fitted to the 7.40 report map image. The
  replay's fountain entities (`CDOTA_Unit_Fountain`) sit at (8928, 9446) and
  (23792, 23232) on every local fixture, 793 and 1,109 world units away. The anchors
  (and `catalog.load_map_constants()["fountains"]`) now use the entity positions.
  - `region_of` splits the halves at the perpendicular bisector of the two fountains.
    Their midpoint is 51 units from the map centre (16384, 16384); the old anchors'
    midpoint was 367 units off.
  - Territory depth now reaches 1.0 at the enemy fountain, as documented. It used
    to reach 1.0 at the old anchor, 800 to 1,100 units short of it.
  - On the 9 local fixtures, no Roshan conversion tag or status changes. Territory
    coverage and depth values shift, 9 of 31 conversion scores move (8 by 1 or 2
    points, one by 6), and one ward-count driver changes. `territorial_advance`
    changes on 94 of 8,391 farming segments (1,307 to 1,281 on the calibration
    corpus). `map_context` enemy presence by half changes in 326 of 1,952 buckets.
    No neutral camp changes map half.

- **Neutral camp zones sit on the camps.** The 28 zone centres in `camp_zones.json`
  were hand-placed 125–700 world units (mean 322) from where the camps are. Each is
  now the position of its camp's `CDOTA_NeutralSpawner` entity. That position is the
  same in all 9 local 7.41 fixtures, and the neutral creeps spawn within about 100
  units of it. Ids, types, topology and radii are unchanged, and every observed
  spawn falls well inside its zone. The legacy `neutral_camps.json` centres (used by
  `map_context`) move with them; no camp changes map half.
  - The catalog is now `version` 3 with `dota_patch` "7.41", so `FarmingRoute` /
    segment `camp_catalog_version` and `camp_map_patch` read `3` and `"7.41"`.
  - On the 9 fixtures, farming routes find 8,391 camp segments instead of 8,269,
    with 8,525 neutral kills inside them instead of 8,342. 2,901 segments have
    strong farm evidence, up from 2,706, and 3,622 are transit-like, down from
    3,775. About 6.5% of the neutral deaths the camp audit assigns change camp.
    The largest moves are at camps 4 (+241 segments), 6 (−153), 9 (+116) and
    19 (−96). The farming-context corpus is regenerated.
  - Camp 10 stays annotated `large`, but its spawner reports a medium camp; it is
    flagged for review.

- **Ward cells round the way OpenDota rounds them.** gem rounded ward positions with
  Python's `round()`, which rounds half to even, and skipped OpenDota's first rounding
  to one decimal. That put some wards one cell off, e.g. `[91,156]` for `[92,156]`.
  `obs` and `sen` now match OpenDota for 80 of 80 players, up from 64 and 56. The
  `obs_left_log` / `sen_left_log` keys use the same rounding.

- **The purchase timeline matches OpenDota.** `purchase_log`, `purchase_time`,
  `first_purchase_time`, `purchase` and the ward-purchase counts now match
  OpenDota for 80 of 80 players on the local fixtures. Before, `purchase_log` and
  `purchase_time` matched for 24, `purchase` for 76, and the observer and sentry
  counts for 46 of 49 and 39 of 43. There were three causes:
  - **When starting items are read.** OpenDota reads each player's starting
    inventory at the first once-a-second interval where the hero exists, at the
    start of a tick, and times it with the same clock as rune pickups. gem read it
    at its own first per-second snapshot, so starting items were a second early or
    late. Sometimes an observer and a sentry had also merged into a dispenser in
    between. Starting items now come from OpenDota's read and carry `game_time_s`.
    Like OpenDota, the read only waits for the player resource entity, not for
    all ten players, so starting items are still recorded in a truncated replay
    or a custom match with fewer players.
  - **Ward dispensers.** The combat log records a `ward_dispenser` purchase
    whenever an observer and a sentry ward merge. OpenDota leaves these out of
    `purchase_log`, `purchase_time` and `first_purchase_time`, as it does recipes,
    and still counts them in `purchase`. gem now does the same.
  - **Purchases at exactly 0:00.** OpenDota replaces a `first_purchase_time` of 0
    with the item's next purchase time, and gem now does the same.
- **Rune pickups and chat-based objectives are timed the way OpenDota times
  them.** OpenDota stamps chat events with its clock at the start of each tick,
  which reads the network tick the previous tick left behind. gem timed rune
  pickups from the replay tick, and rebuilt objectives such as courier kills from
  combat-log deaths, so about one in four players' rune times and some objectives
  were a second off.
  - `PICKUP_RUNE` entries now carry `game_time_s`, and `runes_log` matches
    OpenDota for 80 of 80 players (473 of 473 pickups).
  - Courier, Roshan, Aegis and first-blood objectives take their time from the
    matching chat event; the 10 that were a second off now match.
  - `ReplayParser.opendota_tick_start_raw_s` and `opendota_start_s` expose that
    clock.
- **Hero names come from the replay's own name table on current replays.**
  `PlayerExtractor` read the entity name index only from the older
  `m_nameStringableIndex` field, so on current replays (which carry
  `m_nameStringTableIndex`) every hero kept a name guessed from its entity class.
  That guess is wrong for compound names: Queen of Pain became
  `npc_dota_hero_queen_of_pain` instead of `npc_dota_hero_queenofpain`, so her
  `hero_id` was `0`. Because fight detection matches combat-log names to
  `hero_name`, none of her kills, damage or ability uses counted in any fight
  either. On replay 8855242704 `hero_id` now matches OpenDota (80 of 80 players
  across the fixtures), and her fight rows are filled in. The other fixtures
  are unchanged.
- **`first_blood_time`, `pre_game_duration`, `radiant_score` and `dire_score`
  come from the postgame summary.** The replay's embedded `CMsgDOTAMatch` carries
  all four, and they equal OpenDota's on every local fixture. gem had reconstructed
  first blood from the first hero death (1 s off on 5 of 8 fixtures), summed team
  scores from player kills (off on 2 of 8, e.g. 31 vs 33), and left
  `pre_game_duration` at `0` (it is 90). Without the summary, the reconstructions
  remain.
- **The daily protobuf watch can open its update PR again.** It had failed every
  run since the upstream Dota 2 protos last changed. The failure was in its own
  check, which imported every generated module into one process. Upstream's
  `steammessages.proto` and `steammessages_base.proto` declare the same custom
  options, so that check could never pass. The new
  `scripts/check_proto_imports.py` imports each module in its own interpreter;
  the one known conflict, `steammessages_base_pb2`, which nothing imports, must
  fail with exactly that error. No generated binding or runtime behavior changes.
- **Illusions of enemy heroes no longer steal combat-log credit.** gem mapped a
  combat-log hero name to whichever entity of that hero class had updated last.
  Dark Seer's Wall of Replica, Shadow Demon's Disruption and Morphling's Replicate
  create illusions of *enemy* heroes that carry the caster's player ID, so while
  one existed the real hero's entries went to the caster. When it disappeared,
  the name was dropped and the real hero's entries were lost until its next
  update. A name now maps only to the player's own hero (the controller's
  `m_hAssignedHero`, else PlayerResource's `m_hSelectedHero`), and the mapping is
  never removed, as OpenDota's `name_to_slot` works.
  - On replay 8974053011 (a Dark Seer game), `gold_reasons`, `xp_reasons`,
    `damage`, `damage_taken`, `damage_inflictor`, `damage_inflictor_received`,
    `damage_targets`, `healing`, `ability_uses` and `hero_hits` now match OpenDota
    for 10 of 10 players instead of 4. `killed`, `ability_targets`, lane and
    neutral kills, purchases, `kills_log` and the per-minute running totals are
    corrected too.
  - On 8868259993 (an Ember Spirit game), an Ember Spirit tower kill and a
    courier kill were credited to a Radiant player; they now match OpenDota.
    The other 7 local OpenDota fixtures parse byte-identically.
- **Per-player current gold and gold spent are correct.** `ParsedPlayer.gold_t`
  was all zeros on current replays. It read `CDOTAPlayerController.m_iGold`, a
  field those replays don't have.
  - `gold_t` is now current unspent gold from the team data entity
    (`m_iReliableGold + m_iUnreliableGold`). At game end it matches OpenDota's
    `gold` to within a gold or two. The DataFrame `gold` column, the CLI's final
    gold, and the HTML movement view read it and are fixed too.
  - `gold_spent` was total earned gold minus that zero, so it equalled total
    earned gold. It now comes from the replay's embedded postgame summary
    (`CMsgDOTAMatch`) and matches OpenDota exactly. It is `0` when the summary
    is missing, as `gold_per_min` is, because earned minus current gold is not
    gold spent.
  - On replays without complete interval data, `gold_t_min` fell back to current
    gold. It now uses cumulative earned gold, as OpenDota's `gold_t` and the
    interval path do.
- **Minute zero of the per-minute curves is sampled when OpenDota samples it.**
  OpenDota reads an interval every raw clock second from pregame and labels the
  one at the rounded game start as t=0. gem waited until the game start was
  visible, which can be up to a second later.
  - On replay 8855242704 the start appeared only after gem's rounded clock
    already read 1, so minute 0 was skipped. `gold_t_min`, `xp_t_min`,
    `lh_t_min`, `dn_t_min`, `net_worth_t_min`, `times_min`/`game_times_min`,
    `radiant_gold_adv` and `radiant_xp_adv` had 69 entries and were shifted one
    minute early. So were the laning stats (`lane_efficiency_pct`,
    `lane_total_gold`, …) that read minute 10. The per-minute running totals
    (`total_hero_damage_t_min`, …) still had 70, so indices disagreed between
    fields.
  - On 8974053011 a last hit landed in that gap and showed up in `lh_t_min[0]`.
  - All per-minute arrays now match OpenDota on every local fixture. On the
    other fixtures only the minute-0 tick stamp (`times_min[0]`) moves, to the
    tick OpenDota samples, which can precede `game_start_tick` by under a
    second. `ReplayParser.raw_game_time_s` exposes the raw clock this uses.
- **A bug in a callback no longer silently cuts a parse short, and partial
  parses are visible.** `ReplayParser.parse()` caught every exception, so any error
  in gem's extractors or in your own handlers became the warning "Replay stream
  ended early" and a partial result. That error was also never passed on to the
  result, so `gem.parse()` and `parse_many()` reported partial parses as success.
  - Only problems in the replay data end a parse early now: a
    `gem.ReplayDataError`. gem reports its own protobuf, Snappy, and bitstream
    decoding failures that way. Everything else propagates, including errors your
    callbacks raise.
  - The stream detects a truncated file itself and raises
    `gem.TruncatedReplayError`, a `ReplayDataError` that is also an `EOFError`.
  - `ParsedMatch.parse_error` and `truncated_at_tick` record why and where a
    partial parse stopped. `ParseResult.complete` is `False` for one.
  - Existing data errors now subclass `ReplayDataError` but keep their old types,
    so `except` clauses written for them still match: `BufferReadError` is an
    `EOFError`, an unknown string table a `KeyError`, LZSS tables
    `NotImplementedError`, entity-table inconsistencies a `RuntimeError`, and a
    varint overflow an `OverflowError`.
  - Behavior change: `gem.parse()` on a missing file now raises
    `FileNotFoundError` instead of returning an empty match.
- **Combat-log entries by non-hero units are credited like OpenDota.** When an
  entry's attacker wasn't a hero, gem searched for a unit with that name and
  credited its owner. That search never matched on current replays, because the
  name field was renamed. When it did match, it picked whichever unit came first,
  so all 10 couriers' ability uses would go to one player. gem now credits only
  heroes, as OpenDota's `CreateParsedDataBlob` does. Kills by summons still reach
  their owner: in the replays checked, every kill by a boar, hawk, Brewmaster
  spirit, or Warlock golem names the owning hero as its damage source. Output on
  current replays is unchanged, and `gem.parse()` no longer scans every entity
  slot about 2,500 times per match (about 5 s faster on a 99-minute replay).
- `EntityManager.find_by_npc_name()` works on current replays, which name the
  field `m_nameStringTableIndex`. It reads the old spelling as well.
- **String tables now decode index jumps, key history, and empty updates like
  Clarity.** gem followed Manta, which gets three rules wrong:
  - An entry that jumps ahead moves relative to the previous one
    (`index += varint + 2`); gem set it absolutely (`varint + 1`).
  - Names can reuse the start of one of the last 32 entries' names, counting
    every entry; gem counted only entries that sent a name.
  - An update without a value clears the old one; gem kept it.

  `ActiveModifiers` names each entry by its index, so a replay shows the correct
  rule. On a 99-minute replay, Clarity's rules put all 279 jumped-to entries at
  the index their name says, and gem's put none there. gem's copy of that table
  was wrong from about ten minutes in: at the end, 42 of 1,774 modifiers were in
  place. The tables gem reads (`CombatLogNames`, `instancebaseline`,
  `EntityNames`) never jump in the replays checked, so parse output is unchanged.
  gem now also handles `svc_ClearAllStringTables`, and string-table errors name
  the table.
- **`Entity.to_map()` now returns the entity's values.** It returned a copy of a
  dict that only tests wrote to, so on a real replay it was always empty. It now
  lists every stored value by the names `get()` accepts, like Manta's
  `Entity.Map()`. Array lengths and table presence flags are left out. When a
  class declares the same field name twice, as `DataTeamPlayer_t` does with
  `m_nPlayerID`, only the first field is listed, the one `get()` reads.
- **Variable-length entity arrays now shrink.** When a variable-length array or
  table got a new length after it had elements, gem ignored the length, as Manta
  does. Elements past the new length stayed readable, and the length itself
  could not be read: `entity.get("m_vecPlayerTeamData")` returned an internal
  `FieldState` object. gem now follows Clarity. A new length drops the elements
  past it, and reading the array's own name returns its length. Reading a fixed
  table's own name returns its presence flag, which is `True` once the table has
  fields.

  A 99-minute replay had 1,159 such shrinks, for example
  `m_vecKnownClearCamps` dropping to 0 while 28 old camps stayed, and
  `CDOTATeam.m_aPlayers` going from 14 to 13. Nothing in `ParsedMatch` reads
  these arrays, so parse output is unchanged. Raw entity access through
  `on_entity` sees the corrected values.
- **Quantized-float flags now match Manta and Clarity.** Whether a quantized
  float keeps its round-up/round-down/encode-zero flags, and so how many bits
  each value uses, depends on exact float comparisons that gem did in 64-bit
  arithmetic while the reference parsers use 32-bit. For `m_flSpriteFramerate`
  on `CSprite`/`CSpriteOriented`, gem dropped the round-up flag and would have
  read one bit too few per value, misreading the rest of the packet. No replay
  checked contains a sprite entity, so no output changes; decoded values keep
  their 64-bit precision.
- **Hero mana was 1/8 of its real value.** The send-table schema was parsed
  before the game build was known, so it was treated as build 0 and the
  pre-955 patch shrank `m_flMana` / `m_flMaxMana`'s range from the replay's own
  0–65,536 to 0–8,192. `ReplayParser` now records the build as soon as
  `svc_ServerInfo` arrives, as Manta does. This fixes `Entity.get_float32("m_flMana")`,
  `PlayerStateSnapshot.mana` / `max_mana`, and `PlayerTimeSeries.mana_t` (e.g.
  Queen of Pain's level-7 max mana: 91.5 → 732.3). `ParsedMatch` output is
  unchanged: it doesn't include mana.
- **32-bit varints wrap like Valve's reader.** `BitReader.read_varuint32`
  could return values up to 35 bits, and `read_varint32` values outside the
  int32 range, when a 5-byte varint's last byte was above `0x0F`. Both now keep
  the low 32 bits before zigzag decoding, as Valve's `bf_read::ReadVarInt32` and
  Manta do. Valve's writer never produces such bytes, so real replays parse the
  same; only malformed input is affected.
- **Chat channel labels match the documented contract.** `ChatEntry.channel`
  was `"team"` for every channel except all-chat, so guild, spectator, coach, and
  broadcast chat were reported as team chat. It is now `"all"` for all-chat,
  `"team"` for team chat (`DOTAChannelType_GameAllies`), and the raw channel number
  as a string for anything else (for example `"13"` for spectator chat), as
  OpenDota does. The HTML report shows those as `CH 13`.
- **Parquet schemas no longer depend on match content.** Before this fix, the
  same table could get a different Parquet schema in different replays, so
  `read_parquet_table` and other multi-file readers could not combine them.
  Every table in `CORE_TABLES` and `OPTIONAL_GROUPS` now has the same columns
  and types for every match, including an empty one. Examples of the old
  drift: all-`None` columns were written as the Arrow `null` type (for example
  `vision_modifiers.remove_modifier_duration_s`); `player_summary.lane_gold_adv`
  and `smoke_members.player_id` switched between `int64` and `double`;
  `player_buyback_log` had no columns when a match had no buybacks; and
  `objectives.x`/`y`/`killer_player_id` only existed when banner-plant or
  Tormentor rows did.
- Docs: `DEM_FileInfo` was described as arriving early; it is the last envelope
  in the file. Header bytes 8–15 are the `DEM_FileInfo` and `DEM_SpawnGroups`
  offsets, not unspecified metadata. S2 combat-log names are string-table
  indexes, not pre-resolved names (`CLAUDE.md`).
- The atlas generator missed `import public` lines (such as
  `dota_shared_enums.proto` → `events.proto`) and printed placeholder
  `Syntax`/`Package` values.

## [0.10.0] - 2026-09-24

Slims the tabular export to flat core tables. DataFrame and Parquet output no
longer repeats every per-player statistic on every sampled row, and the
post-parse analysis tables are now opt-in. On a 40-minute replay
(`8822520406`), peak memory while building DataFrames drops from 832 MB to
296 MB, total table size from 497 MB to 54 MB, and `build_dataframes` time from
11.0 s to 3.3 s. **Breaking for DataFrame/Parquet consumers:** the `players`
table is replaced, and the analysis and OpenDota tables need `include=`.

JSON becomes the full-fidelity format and can now be loaded back:
`gem.load_json()` rebuilds a `ParsedMatch` from `to_json` output in about 3 s,
instead of re-parsing the replay (about 60 s on the same fixture), and
`gem.analyze()` bundles every post-parse analysis so it can be embedded in the
JSON.

Upgrading from 0.9: read `frames["player_summary"]` and
`frames["player_timeseries"]` instead of `frames["players"]`; pass
`include=["analysis"]` (or `--include analysis`) for the farming, smoke-fight,
Roshan-conversion, and teamfight-positioning tables; and replace
`parse_many_to_dataframe` / `gem batch --format dataframe` with
`parse_many_to_parquet` plus `read_parquet_table`. `ParsedMatch`, the existing
JSON fields, and the other public APIs are unchanged, and Python 3.10+ support
is preserved.

### Added

- **`gem.load_json(path)` and `gem.from_dict(data)`.** Rebuild a `ParsedMatch`
  from `to_json` output, or from a bare `to_dict` payload written by older
  versions. Enums, tuples such as `position_log`, integer keys such as
  `final_items`, and `game_clock` come back with their original types, so the
  loaded match equals the parsed one and every analysis helper works on it.
  Unknown keys are ignored, missing keys use field defaults, and a newer
  `schema_version` raises `ValueError`. The `analysis` section is not decoded;
  call `gem.analyze()` on the loaded match.
- **`gem.analyze(match)` and `gem.MatchAnalysis`.** Run the smoke, smoke-fight,
  Roshan-conversion, farming-route, and teamfight-positioning analyses with
  their defaults in one call.
- **Analysis in JSON.** `to_json(match, analysis=...)`,
  `parse_to_json(path, analyze=True)`, and
  `gem parse --format json --analysis` embed the analysis results under a
  top-level `analysis` key.

- **`player_summary`, `player_timeseries`, and `player_breakdowns` tables.**
  `player_summary` has one row per player with every end-of-game scalar,
  including the damage-type split and the largest hero hit
  (`max_hero_hit_value`/`_inflictor`/`_target`/`_time`). `player_timeseries`
  holds the sampled `gold`, `total_earned_gold`, `total_earned_xp`,
  `net_worth`, `lh`, `dn`, and `xp` by tick. `player_breakdowns` exports the
  per-player dict statistics (`damage`, `damage_targets`, `ability_uses`,
  `purchase`, `gold_reasons`, `lane_pos`, `killed`, and more) in long form as
  `(player_id, stat, key, subkey, value)`.
- **`teamfight_players` table.** One row per fight and player, holding the
  scalar `TeamfightPlayer` stats and joined to `teamfights` by `fight_index`.
- **`include=` table groups.** `build_dataframes`, `parse_to_dataframe`,
  `to_parquet`, `parse_to_parquet`, and `parse_many_to_parquet` accept
  `include=["analysis"]` and/or `include=["opendota"]`. The CLI takes a
  repeatable `--include GROUP` flag on `gem parse --format parquet` and on
  `gem batch`. `gem.results.dataframes.CORE_TABLES` and `OPTIONAL_GROUPS` list
  the table names.
- **`gem.read_parquet_table(output_dir, table)`.** Loads one table across every
  replay directory written by `parse_many_to_parquet`, adding a `replay` column.
- `pyarrow` is now in the `dev` dependency group, so the Parquet tests run
  locally instead of being skipped.

### Changed

- **`to_json` output carries `schema_version` and `gem_version`.** Both keys
  sit at the top level beside the unchanged `ParsedMatch` fields, so existing
  readers keep working. `gem.SCHEMA_VERSION` is the current layout version.
  `to_dict(match)` still returns the bare match fields.
- **`to_json` writes strict JSON.** A `NaN` or infinite float now raises
  `ValueError` instead of producing a non-standard `NaN`/`Infinity` literal.
  None occur in current parser output.

- **`players` DataFrame removed.** It is replaced by `player_summary`,
  `player_timeseries`, and `player_breakdowns`. The old table repeated about 70
  constant columns, including 17 dict-valued columns, on every sampled row. Its
  `final_net_worth`/`final_last_hits`/`final_denies` columns are
  `net_worth`/`last_hits`/`denies` in `player_summary`.
- **Analysis and OpenDota tables are opt-in.** Pass `include=["analysis"]` for
  `teamfight_positioning`, `roshan_conversions`, `roshan_conversion_fights`,
  `smoke_fight_*`, and `farming_*`, which runs those analyses only when asked.
  Pass `include=["opendota"]` for `opendota_objectives` and
  `opendota_teamfights`.
- **Every DataFrame/Parquet table starts with a `match_id` column** (`0` when
  the replay carries no match ID).
- **Core tables hold only primitive cells.** `teamfights` drops its nested
  `players` column (see `teamfight_players`), and adds `fight_index`.
  `smoke_events` drops `participants` (already in `smoke_members`) and joins
  `smoked` with `";"`. `vision_modifiers.evidence_gaps` and
  `vision_modifier_pairing_issues.candidate_add_ticks` are joined with `";"`.

### Deprecated

- **`parse_many_to_dataframe`.** It emits a `DeprecationWarning`: it keeps
  every parsed match and every table in memory until the batch finishes, and
  it drops failed replays without a report. Use `parse_many_to_parquet` plus
  `read_parquet_table` instead.

### Removed

- **`gem batch --format dataframe`.** Use the default per-replay Parquet
  layout and `gem.read_parquet_table()`.

## [0.9.0] - 2026-09-24

Adds evidence-first match analysis built on authoritative replay visibility:
per-team hero and NPC visibility timelines, hardened smoke and vision-modifier
lifecycles, point-vision assessment with explicit evidence gaps, teamfight
positioning, smoke-to-fight insights, calibrated Roshan conversion evidence, and
farming routes with comparative context. It also adds a pause-aware in-game
clock (`ParsedMatch.game_clock`) and `ParsedMatch.post_game_tick`.

Some outputs change relative to 0.8.0. In matches with pauses,
OpenDota-compatible objective and ward-expiry times now follow the in-game
clock (building kills match OpenDota exactly). Roshan, smoke, and ward-impact
windows now end when the Ancient falls rather than at the end of the recording,
which changes some Roshan Aegis fates and tags. Reports show in-game times and
the real match duration. Roshan `conversion_score` / `conversion_label` are
deprecated and remain available through the 0.9 line. Existing constructor
positions, public APIs, and Python 3.10+ support are preserved.

### Added

- **Evidence-first farming routes.** Add deterministic camp-zone assignment,
  sample-gap and large-jump boundaries, same-camp micro-exit merging, neutral
  and fresh cumulative-resource support, explicit strength/gap records, public
  Python models, and flat route/segment/point DataFrame exports. Dense parsed
  players now preserve cumulative total-earned XP alongside level-local XP. The
  final context layer adds explicit camp topology, contiguous distance,
  comparative local presence, modeled observer coverage, lane-tower state,
  bounded objective/territory provenance, composable tags, a normalized tag
  export, and a calibrated real-replay corpus. The Farming report consumes the
  same public records, leads with evidence and tags, preserves discontinuities
  while downsampling long routes, and exposes missing context instead of
  inserting neutral values.

- **Calibrated Roshan conversion evidence.** Add a reproducible real-replay
  corpus (including denied, stolen, expired, inferred-consumed, preexisting-
  fight, late, partial, and no-tag cases), inspectable tag and territory
  configuration, engagement-aware fight evidence, lifecycle/team provenance,
  bidirectional report links, and flat conversion/fight DataFrame exports.

- **Vision-aware smoke and fight insights.** Add reusable, bounded smoke-to-fight
  observations with exact event evidence, sampled formation context,
  authoritative visibility, ambiguity-safe association, and objective or ward
  follow-up. Public records, flat DataFrame exports, and cross-linked report
  views preserve incomplete evidence without assigning a success score or
  claiming why smoke ended.
- **Evidence-first teamfight positioning.** Add deterministic pre-engagement,
  engagement-start, first-death, and fight-end snapshots with bounded sampled
  positions, derived team geometry, authoritative opposing-team visibility,
  smoke/reveal context, and explicit completeness. A flat DataFrame export and
  interactive report map preserve missing or stale evidence without assigning
  qualitative positioning grades.
- **Evidence-aware point-vision assessment.** Add
  `assess_point_vision(...)` with explicit supported, unsupported, and
  incomplete states; bounded sampled-position provenance; observer lifetime
  and missing-evidence details; optional authoritative canonical-hero
  visibility; and target-specific reveal evidence kept separate from map-point
  coverage.
- **Evidence-preserving vision modifier lifecycles.** Classify direct reveals,
  reveal auras, and Gem carriers; retain protocol/source/duration/purge evidence,
  non-hero applications, conservative lifecycle states, and public ambiguous or
  orphan removal issues. JSON and stable flat DataFrame exports include both
  applications and pairing issues.
- **Evidence-first Smoke of Deceit analysis.** Preserve exact activation and
  per-hero modifier ticks, duration evidence, sampled application/removal
  positions, and authoritative enemy visibility; expose
  `build_smoke_analysis(...)` plus a flat `smoke_members` DataFrame. The report's
  new Smoke Operations card separates early removal, visibility, sampled enemy
  proximity, and follow-up fights instead of assigning a success score or a
  guessed break cause.
- **Authoritative hero visibility timeline.** Parse the Radiant and Dire
  `m_bNPCVisibleState` entity bitsets into change-only
  `ParsedMatch.hero_visibility_events`, expose tri-state
  `gem.hero_visibility_at(...)` queries, and preserve the optional Radiant/Dire
  visibility flags carried by Source 2 combat-log entries. JSON, DataFrame, and
  Parquet exports include the new visibility data; unavailable replay state is
  reported as `unknown`, never inferred to mean hidden.
- **Authoritative all-NPC entity visibility.** Add identity-safe, change-only
  packet-boundary visibility and lifecycle events for active networked Dota NPC
  entities, plus `entity_visibility_at(...)` and JSON/DataFrame export. This
  does not reconstruct arbitrary-point fog of war, attribute visibility
  sources, model temporary viewers, or simulate terrain/navigation.
- **Final Python performance profile.** Add a reproducible full-replay profiling
  harness and v0.8.0 public/core CPU and memory measurements, with exact output
  checks and an entity-field decode/apply boundary selected for a future Rust
  prototype. The harness rejects dirty parser sources or fixture manifests and
  incompatible public output hashes before saving measurements. No parser
  behavior or runtime requirement changes.
- **Pause-aware game clock and match end.** Record in-game pauses from the
  game-rules entity (`m_bGamePaused`, `m_nPauseStartTick`,
  `m_nTotalPausedTicks`) and expose them as `ParsedMatch.game_clock`
  (`gem.GameClock` / `gem.GamePause`) with `game_time_at`, `game_seconds_at`,
  `tick_at`, and `format_tick`. Add `ParsedMatch.post_game_tick`, the tick the
  Ancient fell, since `game_end_tick` is the end of the recording and can run
  many minutes later. The match DataFrame gains a `post_game_tick` column.

### Changed

- **Roshan compatibility migration.** Formally deprecate the aggregate
  `conversion_score` and exclusive `conversion_label`, retain them through the
  0.9 line, remove them from reports, and prefer raw differential evidence,
  status, and non-exclusive tags. Unknown structure or Tormentor attribution is
  now counted and never silently credited.

- **Patch 7.41 report map.** Replace the default patch 7.40 report background
  with Liquipedia's patch 7.41 map, normalized to the existing 8,878 × 8,356
  canvas so report layout and coordinate projection dimensions stay stable.
- **Safer experimental vision interpretation.** `estimate_vision(...)` keeps
  its compatibility list result while using the hardened freshness and ward
  boundary rules, and direct-target modifiers no longer act as unlimited
  arbitrary-point sources. The kill feed now reports authoritative
  visible/hidden/unknown hero state instead of inferring a blind kill from an
  empty geometry result.
- **Evidence-first Roshan conversion.** Harden Aegis attribution and per-Roshan
  boundaries, add signed fight, tier-weighted structure, gold, XP, sustained
  territory, forward-ward, and Tormentor differentials, and replace the report's
  exclusive-label emphasis with non-exclusive tags, paired occupancy maps,
  resource slopes, and a two-sided event timeline. Existing public conversion
  fields and constructor behavior remain available for compatibility; missing
  telemetry is now reported as unavailable instead of a neutral zero.
- **README refresh.** Rework the project README into a concise landing page,
  update API and replay-scope guidance, remove stale release, roadmap, and sample
  claims, and replace the legacy screenshot gallery with current overview,
  vision, and teamfight views.

### Fixed

- **In-game times after pauses.** OpenDota-compatible objective times, ward
  expiry (`obs_left_log` / `sen_left_log`) times, the lane-position window, and
  OpenDota teamfight `xp_start` / `xp_end` sample points no longer count paused
  ticks as game time. On TI2026 match 8860187335 (one 22-second pause) objective
  times were up to 21 s late; building kills now match OpenDota exactly.
- **Match reports show the in-game clock.** The header shows the match duration
  instead of the recording length (65:52 → 50:05 on match 8860187335), every
  report time and the ward-map playback label are pause-aware, Roshan respawn
  windows account for pauses, and Movement tab frame labels are measured from
  the horn instead of from the first replay tick.
- **Analysis windows end when the Ancient falls.** Roshan conversion, smoke
  follow-up, smoke lifecycle, and ward vision-impact windows are bounded by
  `post_game_tick` instead of the end of the recording. An Aegis still held when
  the game ends now reports `aegis_fate="game_end"` instead of `expired`,
  `game_closing` can fire on real replays, and final windows no longer report
  territory or economy evidence as unavailable merely because they ran into the
  post-game recording. Roshan net-worth and XP differentials now map minute
  samples to ticks through the pause-aware clock. The calibration corpus and
  tag-frequency audit are updated accordingly (`game_closing` 0 → 5,
  `counter_conversion` 3 → 7 of 31 conversions).
- **Report map in source checkouts.** `ReportAssets.auto()` now falls back to
  the repository's `assets/maps/Game_map_7.41.jpg` when the user cache has no
  map and no `fallback_map` is given, matching the existing icon fallback.
  Reports built directly through the Python API in a checkout previously had no
  map, so map panels were blank and the Movement tab was omitted.
- **Pause-aware smoke lifecycle matching.** Associate modifier removals using
  reported elapsed duration or pause-aware game time before falling back to raw
  replay ticks, so a long pause cannot leave a legitimate removal unobserved.
- **Dota protobuf ping failure bitmasks.** Regenerate the public descriptors so
  `CMsgClientPingData.region_ping_failed_bitmask` and
  `CSODOTAPartyMember.region_ping_failed_bitmask` use the upstream `uint64` type
  instead of `uint32`.

## [0.8.0] - 2026-09-08

Reduces parser lookup, decoding, and sampling overhead and bounds outstanding
replay results during batch Parquet export. Public APIs, result models, and
Python 3.10+ support remain unchanged.

### Fixed

- Bound outstanding replay results during batch Parquet export and release each match after writing. Parquet export now documents a cooperative batch deadline, including writing, and preserves partial outputs on failure.

### Changed
- **Parser record compatibility study.** Evaluate slotted records and document
  their memory tradeoffs while retaining public dataclass dictionaries, dynamic
  attributes, and weak-reference support.
- **Python runtime guidance.** Document controlled CPython 3.10–3.13 parser
  benchmarks and a separate 3.14 dependency-environment comparison, with
  compatibility results and reproducible measurements for macOS arm64.
- **Lower field-decoding overhead.** Specialize shallow compact field-state paths
  and store Huffman operation/count lookups in compact byte tables.
- **Less interval-frame copying.** Read team values at sampling boundaries after
  the initial interval, preserving minute-zero history and terminal counters.
- **Less draft polling.** Stop scanning draft slots after the game-start tick,
  preserving start-tick assignments and late hero-name resolution.
- **Lower string-table payload overhead.** Use bulk byte reads for larger payloads,
  preserving partial-byte packing and truncated-input behavior.
- **Less repeated test setup.** Share read-only replay results across integration
  checks and separate fast, offline, and live-network test commands.
- **Lower player sampling overhead.** Reuse guarded player-ID resolutions and
  select hero candidates before constructing full snapshots, preserving attribution
  and sampling behavior.
- **Faster teamfight snapshot lookup.** Reuse binary-search tick indexes for
  chronological position and XP queries, preserving ties and unordered-input
  compatibility.
- **Fewer summon ownership scans.** Skip redundant entity lookups for damage
  events with a source name and no positive stun duration, preserving damage,
  stun, ability/item usage, and kill attribution.
- **Lower entity-operation check overhead.** `EntityOp.has()` checks flag values
  directly, avoiding `IntFlag` operation overhead in extractor callbacks while
  preserving overlap semantics and integer-mask compatibility.

### Compatibility and known limitations

- **Batch Parquet timeout.** `parse_many_to_parquet()` uses one cooperative
  deadline covering parsing and interleaved writing after path collection.
  Running parses and synchronous writes are not forcibly interrupted; cleanup
  can exceed the deadline and partial outputs remain on failure. Other batch
  APIs retain their existing timeout behavior.
- **Existing PyArrow limitation.** Full-replay export with PyArrow 21.0.0 can
  fail on an empty `ability_targets` struct. The batch-memory study used the
  supported Fastparquet engine for both revisions; this release does not change
  engine selection or resolve that serialization limitation.
- **Performance scope.** Improvements depend on workload and environment.
  Large-batch throughput measurements were inconclusive under host contention;
  bounded result retention does not imply constant total RSS or a guaranteed
  throughput improvement. See the [parser performance studies](docs/deep-dives/parser-performance.md)
  and [batch-export measurements](https://github.com/whanyu1212/gem-dota/pull/181#issuecomment-5572954464).

## [0.7.1] - 2026-09-04

Improves full-replay parsing speed without changing public APIs or normalized
parser output, and makes integration fixture selection reproducible across
development environments.

### Added
- **Curated TI2026 replay corpus.** The short, medium, and long TI2026 qualifier
  replays are now named canonical, extended, and stress fixture tiers in the
  committed OpenDota manifest. The new `scripts/sync_opendota_fixtures.py`
  command downloads ignored full replays atomically and verifies their recorded
  decompressed size and SHA-256 digest.

### Changed
- **Compact cached field decoding.** Entity deltas now retain compact immutable
  field paths and reuse parse-scoped serializer decoder resolutions, reducing
  path allocation and repeated schema traversal without changing decoded state.
- **Shared compiled entity field access.** Entity field-name resolutions now
  live on parse-scoped serializers, and built-in parser/extractor hot loops
  reuse compiled field plans instead of allocating per-entity lookup caches.
- **Faster entity field traversal.** Nested entity field reads and writes now
  inline their slot and child checks, reducing core decoder overhead without
  changing the stored state model or missing-value behavior.
- **Lower per-entity parser overhead.** Replay parsing now skips unused
  entity-operation result tuples, deduplicates player sampling checks per tick,
  and caches stable hero-name resolution without changing parsed output.
- **Class-aware entity callback dispatch.** Built-in entity handlers are now
  precompiled into ordered class-ID-specific dispatch tables, avoiding callbacks
  for entity classes they do not consume while preserving catch-all callbacks and
  handler ordering.
- **Deterministic integration fixture selection.** Generic full-replay tests and
  examples now use the explicit short TI2026 fixture instead of whichever local
  replay happens to be found first. The DreamLeague performance baseline and
  feature-specific regression fixtures remain available, while replaced medium
  and long DreamLeague entries are retained as deprecated manifest records.
- **Documented parser performance profile.** A new maintainer deep dive records
  the benchmark method, the effect of the five Python optimization passes, output
  parity checks, measurement limitations, and the remaining CPU and memory work.

## [0.7.0] - 2026-09-02

Completes exact offline OpenDota parity for current complete replays by using
their embedded Game Coordinator postgame summary, closes the remaining
minute-zero boundary residuals, and exposes consumed-upgrade flags on each
player.

### Added
- **Exact consumed-upgrade flags.** `ParsedPlayer.aghanims_scepter`,
  `aghanims_shard`, and `moonshard` now mirror OpenDota's `0`/`1` flags from
  the replay-embedded Game Coordinator `permanent_buffs` summary. They remain
  `None` when that summary is unavailable, preserving the distinction between
  unknown and a confirmed zero; explicit API enrichment can populate or
  override them from either OpenDota's top-level flags or `permanent_buffs[]`.

### Fixed
- **Exact minute-zero interval phase.** Minute zero is now sampled immediately
  from the preceding observed team-data frame, while later minute boundaries
  retain their one-tick deferral. This excludes transient initialization values
  and same-tick bounty payouts without zeroing or subtracting legitimate
  pre-horn earnings, closing the remaining TI2026 gold-curve residuals under the
  strict 0.25% gate.
- **Exact offline postgame scalars.** Complete replays now decode the embedded
  `DOTA_UM_MatchDetails` / `CMsgDOTAMatch` summary and use its exact duration,
  `hero_damage`, `tower_damage`, `hero_healing`, GPM, and XPM values. Derived
  `total_gold` / `total_xp` now match OpenDota exactly without a network call;
  combat-log reconstruction and explicit API enrichment remain fallbacks.

## [0.6.0] - 2026-09-02

Aligns Gem's minute-level gold, XP, last-hit, and deny curves exactly with
OpenDota's effective sampling boundaries on current replays, adds explicit
game-time axes to time-series output, and refreshes the bundled Dota 2 protobuf
definitions.

### Added
- **Explicit game-time axes for minute curves.** `ParsedPlayer.game_times_min`
  and `ParsedMatch.game_times_min` now carry the game-relative seconds
  (`0, 60, 120, ...`) parallel to their minute arrays. The `players_minute` and
  `radiant_advantage` DataFrames expose the same axis as `game_time_s` plus the
  derived integer `minute`, so callers no longer need to infer time from list
  position or absolute replay ticks.

### Fixed
- **OpenDota minute-curve boundary parity.** Minute-zero interval samples now
  retain live player counters instead of synthetic zeros, remove only the
  observed one-unit earned-gold initialization offset, and sample one decoded
  network tick after the first rounded-minute crossing to match Clarity's
  effective `@OnTickStart` phase. Terminal recovery no longer fabricates a
  future interval boundary when postGame arrives before the next minute.
- **OpenDota validation alignment.** Minute curves are now joined by explicit
  game-minute keys before comparison, so equal-length shifted curves fail the
  gate instead of being compared positionally. End-of-game net worth, last hits,
  and denies are compared terminal-to-terminal; the misleading last-minute vs
  final-scalar rows were removed. In-tolerance residuals above the review band
  are reported as warnings without changing the validator's exit code.
- **Stricter OpenDota minute-curve gates.** Match gold/XP curve limits are now
  0.25% (from 3.0%/2.5%), player gold/XP limits are both 0.25% (from 3.0%),
  and the review band begins at 0.05%. Last-hit curves now allow
  `max(2, 0.25%)` instead of `max(5, 2%)`, deny curves allow one unit, and any
  count mismatch enters review. The separate terminal net-worth limit is
  unchanged because it compares replay state with a Steam-sourced scalar.

### Changed
- **Dota 2 protobuf definitions refreshed.** Regenerated the bundled Python
  bindings from the latest `SteamTracking/Protobufs` Dota 2 definitions through
  commit `e52bafd` (80 → 84 source files), including the new event proto modules
  and recent match-metadata, modifier, user-message, and network-message fields.
  The proto downloader now completes full refreshes reliably, and the compiler
  rewrites protobuf public imports for use inside the `gem.proto` package.

## [0.5.1] - 2026-09-02

Restores replay downloads for current Valve CDN archives while preserving
support for older replays.

### Fixed
- **`fetch_replay` on Zstandard replays.** Valve switched replay compression from
  bzip2 to Zstandard around late July 2026 while keeping the `.dem.bz2` URL
  extension, so `download_and_decompress` raised
  `OSError: Invalid data stream` on newer matches. The archive format is now
  detected from the payload's magic bytes (`BZh` vs `28 b5 2f fd`) instead of the
  filename, and both formats decompress correctly. Adds a `zstandard` dependency.
  Thanks to @codeturtleam for the report ([#137](https://github.com/whanyu1212/gem-dota/issues/137)).

## [0.5.0] - 2026-06-28

Extends the Roshan conversion analysis beyond the Aegis. Non-Aegis Roshan drops
(Cheese, Refresher Shard, Roshan's Banner) are now surfaced from the entity
stream, and a new banner→rax conversion signal links a planted Roshan's Banner
to a barracks push. All additions are backward-compatible: new `ParsedMatch` /
`RoshConversion` fields carry safe defaults and the public `RoshConversion`
constructor is unchanged for existing callers. Parse/export output for prior
fields is unaffected (OpenDota parity validator unchanged).

### Added
- **Roshan non-Aegis drops** surfaced on the conversion analysis. `RoshConversion`
  now carries `drops` (mirrors `RoshanKill.drops` — Cheese, Refresher Shard,
  Roshan's Banner, captured from the entity stream) and a `had_high_value_drop`
  convenience flag. These are descriptive only and do **not** affect
  `conversion_score`/`conversion_label`. The objectives DataFrame gains a `drops`
  column and the HTML Roshan Conversion section shows the drops per card plus a
  Drops summary-table column with a high-value marker.
- **Roshan's Banner plant tracking + banner→rax conversion signal.**
  `ParsedMatch.banner_plants: list[BannerPlant]` records each planted banner's
  tick, team, planter slot, and world position, recovered from the
  `CDOTA_Unit_Roshans_Banner` unit in the entity stream (the position-less banner
  *item* drop is unchanged). `RoshConversion` gains `banner_planted`,
  `banner_rax_conversion`, and `banner_rax_lane`: an associative (lane + time)
  signal flagging when a banner planted inside the conversion window was followed
  by an enemy barracks falling. Like the drop flags it is descriptive and does
  not affect the score/label. Surfaced in the report (a "Banner planted → Rax"
  badge on the card and a ⚑ marker in the summary Rax cell) and the objectives
  DataFrame (a `banner_plant` row type with coordinates). Note: gem does not
  store barracks world positions, so this is a lane-associative signal, not a
  proven banner-to-rax *distance* link.

### Fixed
- Roshan drop tracking now removes an item entity on any delete (bitwise
  `EntityOp.DELETED` test) rather than only the exact `DELETED_LEFT` composite, so
  a delete arriving without the `LEFT` bit no longer leaves a stale item in the
  drop snapshot.

## [0.4.3] - 2026-06-26

Adds per-buyback gold cost to the model and bundles a set of code-quality
refactors (#106). The one user-visible addition is `ParsedPlayer.buybacks` /
`gem.BuybackEvent`; the rest are behaviour-preserving internal cleanups with no
change to parse/export output (OpenDota parity validator unchanged).

### Added

- `ParsedPlayer.buybacks` — a list of `BuybackEvent` (`tick`, `player_slot`,
  `net_worth`, estimated `cost`) alongside the raw `buyback_log`; also added to the
  `player_buyback_log` DataFrame (`cost`/`net_worth` columns) and exported as
  `gem.BuybackEvent`. The HTML report's buyback table reads this `cost` instead of
  recomputing it; the canonical formula lives in `gem.results.derived.buyback_cost`.

  **The `cost` is an estimate, not a measured value.** It uses Dota 2's published
  formula `200 + net_worth // 13` over net worth at the buyback tick, because the
  exact per-buyback cost is **not recoverable from the replay** — confirmed against
  all three major parsers: gem's entity gold-pool fields reflect gold *after* the
  deduction (before/after delta is zero) and the BUYBACK combat-log entry carries
  no gold amount; OpenDota records no per-buyback cost; and STRATZ's API `cost`
  field is `0` for every buyback (24 events across 3 matches). The
  reliable/unreliable split is likewise not provided.

  Buyback *detection* (event timing + hero) is **cross-validated against STRATZ** —
  times and hero IDs match exactly on every event in those matches. Only the cost
  *value* is an unverifiable formula estimate. (#119)

### Changed

- Refactored the HTML report's ward-map section (`reports/sections/vision.py`,
  `build_wards`) to inject its data through an inert
  `<script type="application/json">` tag — matching the cleaner pattern already
  used by the farming section in the same file — instead of interpolating it into
  the executable `<script>`. This removes ~240 lines of fragile doubled-brace
  (`{{ }}`) f-string escaping. No change to the rendered report. (#106 item #6)
- **Internal:** the inline Smoke-of-Deceit and vision-modifier collection logic
  (~100 lines of closures in `gem.api.parse`) is extracted into
  `gem.extractors.smoke_vision` (`SmokeExtractor`, `VisionModifierExtractor`),
  following the existing `attach()`/`finalize()` extractor contract. Both take the
  `PlayerExtractor` (same dependency pattern as `_CombatAggregator`) for live hero
  positions and the post-parse team back-fill. No output change — smoke groups,
  centroids, and vision-modifier windows are identical (verified end-to-end on a
  replay fixture); the extractors are internal and not part of the public API.
  (#106 item #2)
- **Internal:** the ~234-line per-player population loop in
  `results/assembly.build_parsed_match` is extracted into a dedicated
  `_populate_player_series(match, ...)` helper, shrinking the orchestrator from
  527 to ~310 lines. Each player slot is populated independently (no cross-player
  state), so the loop moved verbatim behind an explicit keyword-only signature.
  No output change — the OpenDota parity validator and the full suite are
  unchanged. (#106 item #3)

## [0.4.2] - 2026-06-25

Report asset-cache tooling and a documentation overhaul. No change to the
parsing pipeline or the supported parse/export API; the additions are the
report asset CLI and the `ReportAssets` cache surface.

### Added
- Report asset cache (`gem.reports.asset_cache`, exposed as `ReportAssets`):
  HTML reports can inline hero icons, item icons, and map images from a local
  user cache instead of bundling them in the wheel. New CLI subcommands under
  `python -m gem reports assets`:
  - `path` — show the cache directories
  - `status [--strict] [--include-recipes]` — report which assets are present
    or missing (`--strict` exits non-zero when any kind is incomplete)
  - `download [--icons|--hero-icons|--item-icons] [--force] [--include-recipes]`
    — fetch icon assets into the cache (skips unchanged files)
  - `add-map <path> [--name NAME]` — copy a local map image into the cache
  All subcommands accept `--asset-dir`, and the cache root can also be set via
  the `GEM_REPORT_ASSET_DIR` environment variable.

### Changed
- HTML reports now degrade gracefully when no icon cache is present. Item rows
  (purchases, kill-feed inflictors, ward/rune legends) drop the icon and keep
  their existing text label rather than rendering an empty cell, and missing
  hero portraits fall back to the hero's name (in icon+name cells) or a sized
  placeholder that preserves the card footprint and team-color cue (draft cards,
  teamfight participant cards) instead of a grey 1×1 placeholder image. Reports
  generated without running `gem reports assets download` are now fully readable.
- Documentation site polished for production: code-first landing page with a
  replay-decoding hero, consolidated parser-internals deep dive, corrected API
  references in guides (`EntityManager.find_by_handle`, combat-log snippet
  imports), and fixed heading hierarchy across the experimental pages.

## [0.4.1] - 2026-06-24

Follow-up to the 0.4.0 OpenDota-parity release: brings the purchase aggregates
to exact parity, surfaces partial-parse state, and an internal extractor
consolidation. The supported top-level API is unchanged; the one behaviour
change is corrected purchase output (now exact vs OpenDota).

### Changed
- `ReplayParser.parse()` now logs a swallowed stream-end exception at `WARNING`
  instead of `DEBUG`, and records it on the parser as `ReplayParser.parse_error`
  (the exception) and `ReplayParser.truncated_at_tick` (the last tick reached);
  both stay `None` on a clean parse. The broad catch is intentional
  (truncated/partial replays legitimately raise on the final corrupt block, and
  parsing continues with whatever was read), but a genuine mid-stream
  decoder/extractor bug is indistinguishable from an expected truncated tail — at
  `DEBUG` it was invisible at the default log level, so silent partial output
  could look complete. Consumers can now inspect these attributes to detect a
  partial parse programmatically. No behavior change beyond log visibility and
  the new attributes.
- **Internal:** the duplicated `CDOTA_PlayerResource` scan and team-data field
  paths shared by `PlayerExtractor` and `IntervalExtractor` are consolidated into
  `gem.extractors._snapshots` (`scan_player_resource`, `team_data_prefix`,
  `team_data_field`, and the `TEAM_RADIANT`/`TEAM_DIRE`/`PLAYER_RESOURCE_SCAN_LIMIT`
  constants). No output change — the OpenDota parity validator and full suite are
  unchanged — but the two extractors no longer keep divergent copies of the scan
  loop and field strings. The intentionally-different `m_vecDataTeam` *reading*
  logic (the interval extractor's two-frame history) is left separate.

### Fixed
- OpenDota purchase parity (issue #95): per-player `purchase`, `purchase_time`,
  and `first_purchase_time` now match the OpenDota match API exactly (verified
  10/10 players on fixture 8855188139). Four corrections: (1) `purchase_time` now
  **sums** every buy time for an item — OpenDota's behaviour — instead of keeping
  only the last buy; (2) starting-inventory synthesis scans only slots 0-7 (main
  inventory + backpack 6-7, mirroring OpenDota's `getHeroInventory`) instead of
  0-16, so stash items are no longer miscounted as starting purchases; (3) removed
  the gem-original starting-window purchase dedup that under-counted multi-copy
  starting consumables (e.g. 2× `faerie_fire` counted as 1); (4) `purchase_log`
  now excludes recipes (matching OpenDota — recipes remain in the `purchase`
  count map). The earlier "needs a synthetic-inventory subsystem rewrite" note on
  this issue was based on a misreading of the OpenDota reference (it emits
  assembled items, not component+recipe — same as gem). Backed by a new
  fixture-backed integration test (`tests/test_purchase_parity_integration.py`).

### Note
- OpenDota's per-player `purchase` / `purchase_time` / `first_purchase_time`
  maps now match the OpenDota match API exactly (see Fixed; verified 10/10
  players on a validation fixture). The only residual is that pre-horn (negative)
  buy timestamps for starting items can differ from OpenDota by ±1s — boundary
  quantization on negative times only; counts and positive-time buys are exact.

## [0.4.0] - 2026-06-23

OpenDota match-API parity release. `gem.parse()` now reproduces most of
OpenDota's per-match and per-player schema directly from the `.dem` stream —
final inventories, OpenDota-style kill breakdowns, building-status bitmasks, the
unified objectives timeline, per-inflictor/per-target combat dicts, the purchase
timeline, and ward departure logs — plus a runnable `examples/opendota_parity.py`
that cross-checks the output against the real OpenDota match API. The supported
top-level API (`gem.parse`, `gem.ParsedMatch`, …) is unchanged; everything here
is additive.

### Added
- Report asset setup tooling: `python -m gem reports assets path/status/download/add-map`,
  `ReportAssets.auto()`, and importable cache helpers so HTML report users can
  populate local hero/item icon and map assets without shipping those assets in
  the wheel. The downloader validates cached PNGs and falls back across current
  and legacy Dota CDN icon paths.
- `ParsedPlayer.final_items` — end-of-game inventory by slot index (0-5 main,
  6-8 backpack, 9-16 stash), keyed item name with the `item_` prefix. Read from
  the hero entity at the game-end tick; verified to match OpenDota's
  `item_0`–`item_5` for every player on the validation fixtures. (Tier-1 coverage
  gap vs the OpenDota match API.)
- `ParsedPlayer.killed` and the derived kill scalars `ancient_kills`,
  `neutral_kills`, `lane_kills`, `courier_kills`, `observer_kills`,
  `sentry_kills`, `roshan_kills` — per-unit kill counts and OpenDota-style
  category totals, reshaped from `kills_log`. Verified to match OpenDota for
  every player without a transient summon army (8/10 on the validation fixture;
  see the multi-summon note below). Backed by a new bundled `ancients.json`
  data file and `gem.catalog.units` NPC classifiers.
- **OpenDota-shaped teamfights.** `ParsedMatch.opendota_teamfights` — a
  compatibility projection of teamfights matching OpenDota's
  `teamfights[].players[]` schema (temporal death-windows, 3-death minimum),
  alongside gem's native spatial `teamfights`. A game-ending throne fight whose
  window extends past the match duration is kept with its `end` clamped to the
  duration, rather than dropped.
- **Per-inflictor / per-target combat attribution** on `ParsedPlayer`:
  `damage_inflictor`, `damage_inflictor_received`, `damage_targets`,
  `ability_targets`, `hero_hits`, and `max_hero_hit` — spell/item-level damage
  breakdowns matching OpenDota's gating (enemy-hero, non-illusion targets;
  self-damage excluded; auto-attacks keyed `null`). `hero_hits`/`max_hero_hit`
  verified exact vs OpenDota.
- **Derived per-player scalars** on `ParsedPlayer`: `hero_id` (numeric),
  `level` (terminal), `gold_spent`, `life_state_dead`, `firstblood_claimed`,
  and `teamfight_participation` — the last two read from the authoritative
  `CDOTA_PlayerResource` fields OpenDota itself uses (10/10 exact). New
  `gem.catalog.hero_id()` helper.
- **Match-level scalars** on `ParsedMatch`: `radiant_score`, `dire_score`, and
  `first_blood_time` (game-clock, illusion deaths excluded).
- **Purchase timeline** on `ParsedPlayer`: `purchase` (item→count),
  `purchase_time`/`first_purchase_time` (game-seconds), `purchase_tpscroll`,
  `purchase_ward_observer`/`purchase_ward_sentry`, `observer_uses`/`sentry_uses`,
  and `observers_placed` — derived from `purchase_log`/`item_uses`, recipe
  handling matching OpenDota's `handlePurchase`.
- **Ward expiry logs + coordinate maps** on `ParsedPlayer`: `obs_left_log`/
  `sen_left_log` (OpenDota-shaped departure events with killer attribution) and
  the nested `obs`/`sen` `{x:{y:count}}` placement histograms. Ward coordinates
  in the OpenDota-shaped outputs are converted from world units to cell units
  (`world / 128`, per `Parse.java`) to match OpenDota; native `WardEvent` keeps
  world coords. `player_slot` uses OpenDota's 0-4/128-132 encoding.
- **Unified objectives timeline** `ParsedMatch.objectives` — one chronological
  OpenDota-shaped list merging `building_kill` and the `CHAT_MESSAGE_*` events
  (Roshan, Aegis, Tormentor, first blood, courier lost), alongside gem's native
  typed objective fields. Killers resolve source-first (summon/projectile kills
  credit the owning hero).
- **Building-status bitmasks** on `ParsedMatch`: `tower_status_radiant`/`_dire`
  and `barracks_status_radiant`/`_dire` — reconstructed offline from building
  kills using the Steam GC bit layout (the replay carries no such entity field).
  Verified **exact** vs OpenDota across validation matches.
- `ParsedMatch.courier_deaths` (and `gem.extractors.objectives.CourierDeath`) —
  courier deaths captured from the combat log, feeding the objectives timeline's
  `CHAT_MESSAGE_COURIER_LOST`.
- **Examples:** `examples/opendota_parity.py` — a runnable showcase of the
  OpenDota-parity outputs above (final inventory, kill breakdown, building-status
  bitmasks, objectives timeline, per-inflictor/per-target combat dicts, purchase
  timeline, ward departure logs, and the `gem.catalog.hero_id` / `gem.catalog.units`
  helpers). When a sibling `<match_id>.opendota.json` is present it cross-checks
  gem's output against the real OpenDota match API field by field. `examples/quickstart.py`
  gains a short teaser of these fields and a pointer to the full showcase.

### Fixed
- `PlayerExtractor._read_inventory` read only the legacy
  `m_pEntity.m_nameStringableIndex`; modern replays expose item names via
  `m_pEntity.m_nameStringTableIndex`, so inventory reads silently returned empty
  on those replays. Now tries both (mirroring `_read_abilities`), which also
  restores the starting-item synthetic `PURCHASE` entries emitted by
  `_diff_inventory`.
- Summon kills are now credited to the owning hero in `kills_log` (the combat
  aggregator's summon→owner fallback previously covered DAMAGE/ABILITY/ITEM but
  not DEATH), matching CLAUDE.md's stated rule and OpenDota's kill attribution
  for single-summon heroes (Warlock Golem, Lone Druid bear, etc.).
- `killed`-derived counts skip reincarnation/aegis *trigger* deaths
  (`will_reincarnate`), consistent with teamfight attribution — fixes a
  double-counted hero kill on heroes that reincarnate.

### Note
- Permanent buffs and the derived `aghanims_scepter` / `aghanims_shard` /
  `moonshard` flags remain **out of scope** for the parser: the relevant entity
  fields (`m_vecPermanentBuffs`, `m_nScepterUpgradeID`, `m_nShardUpgradeID`,
  `m_iAghanimsAbilityPoints`) stay zero across all validation replays — OpenDota
  sources these from Game Coordinator match data, not the `.dem` stream.
- Kill counts for heroes that field many transient, identically-named summons
  (Beastmaster boars/hawk, Brewmaster split units) under-count: gem resolves a
  summon to its owner by a single live name→entity lookup, which can't attribute
  each kill from an army of same-named units. Tracked as a follow-up.
- `ParsedMatch.pre_game_duration` is declared but currently always `0`: deriving
  it needs the `GAME_IN_PROGRESS` state-transition timestamp the parser does not
  yet expose (`m_flGameStartTime` is the clock anchor, not the pre-game span).
  Tracked as a follow-up.
- `ParsedMatch.objectives` `building_kill` count can trail OpenDota by one when a
  building is finished by a siege creep / neutral (no player attribution) — the
  building-status bitmasks, which depend only on *which* buildings fell, remain
  exact.

## [0.3.0] - 2026-06-20

A structural + correctness release. The package was reorganized into focused
subpackages (each with its own README), the combat-stat reconstruction was
realigned to OpenDota's source-based attribution, and a multi-pass adversarial
bug hunt fixed a series of correctness issues across the analysis, extractor, and
combat-log layers. The supported top-level API (`gem.parse`, `gem.ParsedMatch`,
`gem.find_player`, …) is unchanged.

### Added
- `CombatLogEntry.damage_source_name` — the unit credited as the *source* of a
  damage/heal (proto `damage_source_name`; S1 `sourcename`). For spell/projectile
  damage this is the casting hero even when `attacker_name` is the projectile.
- `CombatLogEntry.will_reincarnate` — marks a DEATH that is a reincarnation/aegis
  *trigger* (the hero returns), not a final death (S2 proto field 78).
- `CombatLogType` — a `(str, Enum)` for combat-log entry types, backward
  compatible with the historical string labels (`log_type == "DAMAGE"`).
- Per-package `README.md` files for `binary/`, `schema/`, `state/`, `combat/`,
  `extractors/`, `analysis/`, `reports/`, and `replays/` documenting each
  subsystem's mental model, mechanics, and pitfalls.

### Changed
- **Package reorganization.** Internal modules are grouped into subpackages —
  `binary/`, `schema/`, `state/`, `combat/`, `extractors/`, `analysis/`,
  `catalog/`, `results/`, `reports/`, `replays/`. The supported public API
  (everything in `gem.__all__`) is unchanged; `gem.api`, `gem.parser`,
  `gem.constants`, `gem.reports`, `gem.catalog`, and `gem.extractors` still
  import as before.
- **Source-based combat attribution.** Per-player combat scalars and per-target
  dicts now attribute damage/healing to the damage **source**
  (`damage_source_name`), matching OpenDota (`CreateParsedDataBlob`,
  `unit = e.sourcename`):
  - `ParsedPlayer.damage` / `damage_taken` / `healing` mirror OpenDota's
    source-attributed per-target dicts; target keys are illusion-prefixed
    (`illusion_npc_dota_hero_*`); spurious ability/modifier-name keys are excluded.
  - `tower_damage` is now essentially exact offline (~97.9–100% vs OpenDota,
    up from ~87%).
  - `hero_damage` attribution improved (summon/projectile damage credited to the
    owning hero; redundant `others`-type heuristic dropped).
- Unmapped combat-log proto types now resolve to `CombatLogType.UNKNOWN` instead
  of silently falling back to `DAMAGE` (which previously let `CRITICAL_DAMAGE`
  and `MODIFIER_STACK_EVENT` inflate damage aggregates).
- Map-geometry constants are now sourced from `map_constants.json` (single source
  of truth) rather than duplicated in `analysis/_shared.py`.

### Fixed
- **Day/night cycle** — corrected to a 10-minute cycle with night beginning at
  5:00 (was a wrong 15-minute / late-night assumption), fixing vision-window math.
- **Ward lifespans** — observer 360 s (10800 ticks) and sentry 420 s (12600
  ticks); previous values were off by ~15–35×.
- **Teamfight attribution** — gold credited to the recipient (not the killed
  unit), XP deltas read from monotonic `m_iTotalEarnedXP` (not `m_iCurrentXP`,
  which resets on level-up), spatial guards added to DEATH/BUYBACK/GOLD, and the
  centroid divisor counts only positioned deaths.
- **Roshan conversion windows** — clamped to the next Roshan boundary so
  towers/fights/buybacks are no longer double-counted across back-to-back Roshans.
- **Reincarnation deaths** — WK/Aegis trigger deaths are excluded from the death
  curve and teamfight death counts (the headline K/D/A was already correct).
- **Coach-index remap** — scoreboard K/D/A and team-slot reads now use OpenDota's
  `validIndices` mapping, fixing attribution in coached/HLTV replays.
- **S1 combat log** — PURCHASE events resolve item `value_name`, and
  attacker/target hero flags default to `True` when a legacy descriptor omits
  them (matching Clarity).
- **Fallback advantage curve** — buckets each player's samples by their actual
  game minute (no longer truncated to the shortest player's array or shifted by a
  leading gap).
- **Entity invariants** — a missing baseline at CREATE and a LEAVE for an
  already-inactive entity now raise instead of being silently swallowed
  (robustness; never fires on well-formed replays).
- Narrowed broad `except Exception` blocks across fetch/parser/report paths to
  specific exception types.

### Removed
- Root-level compatibility shims from earlier releases (`gem.reader`,
  `gem.models`, `gem.combatlog`, `gem.entities`, `gem.map_context`,
  `gem.replay_fetch`, …) have been removed. Use the supported top-level `gem.*`
  API or the grouped subpackages (`gem.binary.reader`, `gem.results.models`,
  `gem.combat.log`, `gem.state.entities`, …). The public `gem.__all__` surface is
  unaffected.

## [0.2.8] - 2026-05-24

### Added
- OpenDota fixture refresh tooling via `scripts/fetch_opendota_fixture.py`, plus DreamLeague Season 29 fixture metadata for patch 7.41 validation.
- Neutral item found event parsing, including model/dataframe outputs and constants-audit coverage for newly observed item IDs.
- Neutral camp annotation audit tooling via `scripts/audit_camp_annotations.py`, which groups neutral deaths by camp zones and reports replay-derived evidence.
- A regenerated 7.40 map fixture with 7.41 camp annotations, larger camp icons, type-colored rings, and a legend for camp tiers.
- Pull request template checks for release hygiene and parser safety.

### Changed
- Updated bundled constants from current OpenDota/dotaconstants references for 7.41-era items and abilities.
- Refreshed camp-zone annotations for confirmed 7.41 camp type swaps.
- Hero and item icon fetch scripts now support cache checks so unchanged icon assets are not rewritten unnecessarily.
- Source 2 combat log parsing now preserves neutral camp stack metadata and event locations when available.

### Fixed
- Nearby-gold attribution in the camp audit now ignores unscoped `GOLD` events whose attacker and target names are both absent, preventing inflated camp summaries.

## [0.2.7] - 2026-03-24

### Added
- Objective-aware farming context helpers for experimental farming-pattern analysis. These bucket tower state, Roshan/Aegis timing, ward counts, net-worth/XP advantage, and enemy presence into replay-time context that can be joined to camp visits.
- `ParsedPlayer.total_earned_gold_t` — cumulative earned gold at regular sample cadence, exposed alongside the existing per-minute `total_earned_gold_t_min`.
- Roshan conversion analysis (`gem.build_rosh_conversions`) plus a dedicated `Roshan Conversion` tab in the HTML report.

### Changed
- `ParsedPlayer.gold_t` / `gold_t_min` now represent current unspent gold only (`m_iGold`). They no longer fall back to cumulative earned-gold fields.
- DataFrame export now includes both current unspent gold and cumulative earned gold at regular sample cadence.
- OpenDota validator now supports random replay sampling/fetching and treats minute-snapshot fields (`[min]`) as informational only instead of pass/fail parity checks against final Steam scalars, since the last minute boundary can legitimately precede game end by up to 59 seconds.

### Fixed
- Player time-series sampling now stops immediately after the forced game-end snapshot. This removes postgame drift from sampled player stats, including inflated late `net_worth_t` values after `DOTA_COMBATLOG_GAME_STATE == 6`.
- OpenDota scalar validation for `net_worth` now reflects the small residual divergence between replay-exposed net-worth fields and Steam's final server scalar.
- Experimental farming-context labels and thresholds were refined to be easier to read in reports, and the old border/river special case was removed as a standalone category.
- Player movement sampling now resolves each player through the canonical selected/assigned hero handle, preventing illusion/duplicate-hero entities from polluting position trails.

## [0.2.6] - 2026-03-21

### Added
- `ParsedMatch.radiant_team_id`, `radiant_team_name`, `radiant_team_tag` — team identity for the Radiant side, extracted from `CDOTATeam` entities (field `m_unTournamentTeamID`, `m_szTeamname`, `m_szTag`). Defaults to `0`/`""` for pub games.
- `ParsedMatch.dire_team_id`, `dire_team_name`, `dire_team_tag` — same for the Dire side.
- `ParsedPlayer.steam_id` — 64-bit Steam ID from `CDOTA_PlayerResource.m_vecPlayerData.{slot}.m_iPlayerSteamID`. Defaults to `0`.
- `ParsedPlayer.account_id` — 32-bit Steam account ID (the ID in OpenDota/Dotabuff URLs), derived as `steam_id - 76561197960265728`. Defaults to `0`.
- Scoreboard in HTML match report now displays each player's account ID below their hero name.

## [0.2.5] - 2026-03-20

### Added
- `gem.fetch_replay(match_id, out_dir)` — download and decompress a replay from OpenDota in one call. Importable from notebooks and scripts without any extra dependencies.
- `gem.fetch_replay_url(match_id)` and `gem.download_and_decompress(match_id, url, out_dir)` — lower-level replay fetch helpers, now part of the public API via `src/gem/replay_fetch.py`.
- `gem.resolve_pick_team(event, players)` — resolves the team (Radiant/Dire) for a draft pick/ban event. Uses the post-game player roster as the authoritative source rather than `m_pGameRules.m_iActiveTeam`, which is unreliable for picks in HLTV and coach-slot replays.
- `gem.net_worth_at(player, tick)` — nearest-sample net worth lookup for a player at any tick.
- `gem.ward_vision_impact(ward, match)` — heuristic count of distinct enemy heroes spotted by an observer ward during its lifetime.
- `gem.is_active_teamfight_participant(player_stats)` — returns `True` if a player actively participated in a teamfight (deaths, damage dealt/taken, or healing).
- `gem.format_npc_name(name)` — strips `npc_dota_`, `goodguys_`, `badguys_` prefixes for human-readable display.
- Integration test `tests/test_draft_integration.py` — downloads 5 captains-mode pro replays, parses them, and verifies draft picks/bans against the OpenDota API. Run with `pytest -m integration`.

### Fixed
- `DraftExtractor._resolve_name()` now always tries `hero_id // 2` before falling back to a direct lookup. Modern replays store `api_id * 2` in `m_BannedHeroes`/`m_SelectedHeroes` entity fields; the previous guard (`if hero_id not in _HERO_ID_TO_NPC`) was always `False`, making halving unreachable and causing bans to resolve to wrong heroes (e.g. hero_id=158 → Bloodseeker instead of Shadow Demon).

## [0.2.4] - 2026-03-17

### Added
- `gem.teamfight_at_tick(match, tick)` — O(log N) binary-search lookup returning the `Teamfight` whose window contains a given tick, or `None`. Lets agents locate fight context from any combat log event tick.
- `gem.heroes_near(match, tick, x, y, radius)` — spatial query returning all `ParsedPlayer` objects within `radius` world units of a map coordinate at a given tick, sorted by distance. Uses `position_at_tick` internally.
- `gem.ability_level_at_tick(player, ability, tick)` — returns the level (1–4) of an ability at any tick using per-minute snapshot data. Returns 0 if the ability was not yet learned.
- `Teamfight.radiant_kills`, `Teamfight.dire_kills`, `Teamfight.winner` — fight outcome fields. `winner` is `"radiant"`, `"dire"`, `"draw"`, or `"unknown"`. Populated automatically from `slot_to_team` in `match_builder`.
- `group_ability_hits` now used in the HTML match report fight combat log — AoE spells (Ravage, Black Hole, RP, etc.) are collapsed into a single grouped cast row showing all targets and total damage, instead of one row per target.
- Sample report gallery page added to docs (`docs/reports/`) with a live TI14 Grand Finals G1 (XG vs Falcons) report hosted on GitHub Pages.

### Fixed
- HTML match report file size reduced from ~459 MB to ~58 MB. The 9 MB map image was being base64-encoded 22 times (once per teamfight minimap SVG + ward canvas + laning minimap). It is now emitted once as `window._GEM_MAP_SRC` and patched into SVG elements on `DOMContentLoaded`. Repeated hero icon PNGs are similarly hoisted into JS globals.
- Plotly Movement tab frame count reduced by subsampling position log to one frame per 150 ticks (~5 seconds). Previously one frame per raw tick sample caused ~50k Plotly traces and ~180 MB of embedded figure JSON.
- Plotly Movement tab map image resized to 1024px before embedding (down from 8878×8356 source).
- Ward map heatmap overlay was rendered upside-down — grid row 0 (world `YMIN`, south) was drawn at the top of the canvas. Fixed by flipping the row index when reading the heatmap grid.


## [0.2.3] - 2026-03-17

### Added
- Per-minute combat running totals on `PlayerStateSnapshot` and `PlayerTimeSeries`: `total_hero_damage`, `total_hero_healing`, `total_deaths`, `total_stuns` — accumulated from the combat log as monotonically increasing counters and exposed as `*_t_min` lists on `ParsedPlayer`. Ready for ML feature extraction (diff any window for per-minute rates).
- Combat time-series charts added to the match report HTML (Combat tab) — 2×2 grid showing per-minute hero damage, healing, deaths, and stun duration per player.
- `gem.find_player(match, hero)` — look up a player by hero name without iterating `match.players`. Accepts display names (`"Axe"`, `"Anti-Mage"`), NPC names (`"npc_dota_hero_axe"`), or bare suffixes.
- `gem.constants.hero_npc_name(name)` — reverse lookup from display name to `npc_dota_hero_*` NPC name. Normalises hyphens, underscores, and casing. All 127 heroes in the bundled data are resolvable.
- `ParsedMatch.duration_seconds` and `ParsedMatch.duration_minutes` — convenience properties derived from `game_start_tick` and `game_end_tick`.
- `examples/quickstart.py` — executable version of the quickstart guide, verified against a real replay.

### Fixed
- `docs/guides/01_quickstart.md`, `docs/guides/04_match_data.md`, and `README.md` had numerous references to nonexistent fields (`player.net_worth`, `player.last_hits`, `player.hero_damage`, `player.gold_per_min`, `player.item_builds`, `match.radiant_score`, `ward.placed_by`, etc.) — all corrected to the real API.

## [0.2.2] - 2026-03-16

### Added
- Batch processing API — `gem.parse_many()`, `gem.parse_many_to_dataframe()`, `gem.parse_many_to_parquet()` for parallel multi-replay parsing using `ProcessPoolExecutor`.
- CLI `batch` subcommand — `python -m gem batch replays/ --format parquet --output ./out`; legacy bare-path invocation (`python -m gem match.dem`) preserved.
- Docs home page redesigned — hero section with feature cards; Material theme navigation improvements (breadcrumbs, TOC follow, tooltips, social footer links).
- CLI reference guide and batch API reference page added to docs.
- Annotated JSON output guide — real TI14 G1 (XG vs Falcons) replay output explained field by field.
- `examples/ti14_sample.json` — real JSON output from TI14 Grand Finals G1 used as docs reference.

## [0.2.1] - 2026-03-16

### Added
- JSON export API — `gem.to_json()`, `gem.to_dict()`, `gem.parse_to_json()`.
- Parquet export API — `gem.to_parquet()`, `gem.parse_to_parquet()` (requires `pyarrow` or `fastparquet`).
- Rich CLI overhaul — live progress bar (`--progress`), timing summary table (`--timings`), pixel-art banner in a `HEAVY` box, Radiant/Dire colour-coded summary table.
- Docs architecture page redesigned — single pipeline diagram, layer badge rows, output model table; custom stylesheet added.
- Diamond icon added to MkDocs nav bar and favicon.
- Laning guide and Lane Classifier reference added to docs nav (were previously orphaned pages).
- Export formats (JSON, Parquet) documented across home page, quickstart guide, and API reference index.

### Fixed
- `mypy` error in `__main__.py` — `_task_ids` typed as `dict[str, TaskID]` (was `dict[str, object]`), fixing `Progress.update()` argument type error.
- `mypy` error in `dataframes.py` — tormentor loop variable renamed from `t` to `tm` to avoid type collision with the towers loop.

## [0.2.0] - 2026-03-15

### Added
- Buyback table in HTML report now shows gold spent per buyback using the exact formula `floor(200 + net_worth / 13)`.
- Extended test coverage for teamfight internals (`_update_centroid`, `_nearest_pos`, `_nearest_xp`, `_near_fight`, HEAL attribution, self-heal exclusion, gold/XP delta, item use).
- Extended test coverage for `_dedup_purchase_log` edge cases.
- Known limitations documented in README: healing lotus pickups (not in `.dem` combat log), reliable vs unreliable gold distinction.
- Releases section in README with per-version high-level summaries.

### Changed
- `CHANGELOG.md` and all repo URLs corrected from `whanyu1212/gem` to `whanyu1212/gem-dota`.
- README screenshots updated and resized to uniform dimensions.

### Removed
- `ParsedMatch.lotus_pickups` — healing lotus pickups are not recorded in the `.dem` combat log under any event type across all tested patches. This field always returned an empty list and has been removed from the public API.

## [0.1.1] - 2026-03-14

### Added
- Laning extraction and decomposition via `gem.extractors.lane`.
- Lane-related outputs in parsed match models and dataframe export.
- Damage-type breakdown in combat aggregation outputs.
- Extended ability metadata and parsing support for Aghanim's Scepter/Shard interactions.

### Changed
- Teamfight detection uses temporal windowing only (spatial split behavior removed).

## [0.1.0] - 2026-03-14

### Added
- Initial public release of `gem-dota`.
- Core Source 2 replay parser pipeline (stream/reader/sendtables/field decoding/entities/string tables/parser).
- Game events and combat log normalization (Source 1 + Source 2 paths).
- Extractors for players, objectives, wards, courier, draft, and teamfights.
- Match assembly and dataframe export APIs.
- CLI and example scripts, including HTML match report.
- Validation, fuzzing, and parser robustness foundations.

[Unreleased]: https://github.com/whanyu1212/gem-dota/compare/v0.12.0...HEAD
[0.12.0]: https://github.com/whanyu1212/gem-dota/compare/v0.11.0...v0.12.0
[0.11.0]: https://github.com/whanyu1212/gem-dota/compare/v0.10.0...v0.11.0
[0.10.0]: https://github.com/whanyu1212/gem-dota/compare/v0.9.0...v0.10.0
[0.9.0]: https://github.com/whanyu1212/gem-dota/compare/v0.8.0...v0.9.0
[0.8.0]: https://github.com/whanyu1212/gem-dota/compare/v0.7.1...v0.8.0
[0.7.1]: https://github.com/whanyu1212/gem-dota/compare/v0.7.0...v0.7.1
[0.7.0]: https://github.com/whanyu1212/gem-dota/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/whanyu1212/gem-dota/compare/v0.5.1...v0.6.0
[0.5.1]: https://github.com/whanyu1212/gem-dota/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/whanyu1212/gem-dota/compare/v0.4.3...v0.5.0
[0.4.3]: https://github.com/whanyu1212/gem-dota/compare/v0.4.2...v0.4.3
[0.4.2]: https://github.com/whanyu1212/gem-dota/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/whanyu1212/gem-dota/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/whanyu1212/gem-dota/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/whanyu1212/gem-dota/compare/v0.2.8...v0.3.0
[0.2.8]: https://github.com/whanyu1212/gem-dota/compare/v0.2.7...v0.2.8
[0.2.7]: https://github.com/whanyu1212/gem-dota/compare/v0.2.6...v0.2.7
[0.2.6]: https://github.com/whanyu1212/gem-dota/compare/v0.2.5...v0.2.6
[0.2.5]: https://github.com/whanyu1212/gem-dota/compare/v0.2.4...v0.2.5
[0.2.4]: https://github.com/whanyu1212/gem-dota/compare/v0.2.3...v0.2.4
[0.2.3]: https://github.com/whanyu1212/gem-dota/compare/v0.2.2...v0.2.3
[0.2.2]: https://github.com/whanyu1212/gem-dota/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/whanyu1212/gem-dota/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/whanyu1212/gem-dota/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/whanyu1212/gem-dota/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/whanyu1212/gem-dota/releases/tag/v0.1.0
