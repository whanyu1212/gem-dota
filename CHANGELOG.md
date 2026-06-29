# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- **Breaking:** Replay parsing now fails loudly by default: `ReplayParser.parse()`
  and high-level `gem.parse()` re-raise stream/decoder/extractor errors after
  recording them on `parse_error` / `truncated_at_tick`. Pass
  `allow_partial=True` to opt into the previous best-effort partial-replay
  workflow.

### Added
- `ParsedMatch.parse_error` and `ParsedMatch.truncated_at_tick` surface opt-in
  partial-parse failures in structured output and the `match` DataFrame.
- `build_dataframes()` / parquet exports now include a `vision_modifiers` table
  for `ParsedMatch.vision_modifiers`.
- Parse-result value types including objective events, ward/courier/draft events,
  teamfight records, combat-log records, `SmokeEvent`, and `VisionModifierEvent`
  are now exported consistently from top-level `gem` and `gem.results`.

### Fixed
- Empty and heterogeneous `build_dataframes()` tables now preserve declared columns,
  avoiding KeyErrors and inconsistent export schemas when a match has no rows or
  only a subset of event row types.
- Replay downloads now stream `.bz2` decompression directly to an atomic temporary
  `.dem` file, preserve normal final-file permissions, and leave any existing
  final replay untouched if download or decompression fails.
- Replay download and report asset download helpers now use verified HTTPS/TLS
  contexts instead of disabling certificate and hostname verification; Valve
  replay URLs returned as plain `http://` are upgraded to HTTPS, and other
  non-HTTPS replay URLs are rejected.
- `parse_many(timeout=...)` now enforces the timeout per replay inside each
  worker instead of treating it as a global timeout for the whole batch.
- `parse_many_to_parquet()` now streams completed parse results directly to
  parquet output instead of first holding all `ParsedMatch` objects in memory via
  `parse_many()`.

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

[Unreleased]: https://github.com/whanyu1212/gem-dota/compare/v0.4.0...HEAD
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
