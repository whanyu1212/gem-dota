---
pageClass: changelog-minimal
---

# Changelog

This page is a curated narrative summary of the parser, validation, and report changes that materially affect how `gem` behaves today.

It is intentionally short-range. The full per-release SemVer history lives in the canonical [CHANGELOG.md](https://github.com/whanyu1212/gem-dota/blob/main/CHANGELOG.md).

## June 2026 — v0.4.x

The 0.4 line is an **OpenDota match-API parity** effort plus report asset-cache
tooling. The supported top-level API (`gem.parse`, `gem.ParsedMatch`, `gem.find_player`, …)
is unchanged — everything here is additive.

::: tip OpenDota match-API parity

`gem.parse()` now reproduces most of OpenDota's per-match and per-player schema directly from the `.dem` stream, so a parsed match lines up field-for-field with the OpenDota match API:

- `ParsedPlayer.final_items` — end-of-game inventory by slot (exact vs OpenDota `item_0`–`item_5` on the validation fixtures)
- `ParsedPlayer.killed` + derived kill scalars (`ancient_kills`, `neutral_kills`, `lane_kills`, `courier_kills`, `observer_kills`, `sentry_kills`, `roshan_kills`)
- per-inflictor / per-target combat dicts (`damage_inflictor`, `damage_targets`, `ability_targets`, `hero_hits`, `max_hero_hit`) with OpenDota's enemy-hero, non-illusion gating
- derived scalars `hero_id`, `level`, `gold_spent`, `firstblood_claimed`, `teamfight_participation`, and match-level `radiant_score` / `dire_score` / `first_blood_time`
- `ParsedMatch.objectives` — one chronological OpenDota-shaped timeline merging building kills and `CHAT_MESSAGE_*` events; killers resolve source-first
- `tower_status_*` / `barracks_status_*` building-status bitmasks, reconstructed offline and verified **exact** vs OpenDota
- `ParsedMatch.opendota_teamfights` — a death-window, 3-death-minimum projection alongside gem's native spatial `teamfights`

A runnable `examples/opendota_parity.py` cross-checks the output against the real OpenDota match API when a sibling `<match_id>.opendota.json` is present.

:::

::: info Purchase parity (0.4.1)

Per-player `purchase`, `purchase_time`, and `first_purchase_time` now match the OpenDota match API exactly (verified 10/10 players on a validation fixture). `purchase_time` sums every buy of an item, starting-inventory synthesis reads only the main inventory + backpack (not the stash), and `purchase_log` excludes recipes — matching OpenDota's `handlePurchase`. The only residual is a ±1s difference on pre-horn (negative) starting-buy timestamps; counts and positive-time buys are exact.

:::

::: info Partial-parse visibility (0.4.1)

`ReplayParser.parse()` now records a swallowed stream-end exception on the parser as `parse_error` and `truncated_at_tick` (both `None` on a clean parse), and logs it at `WARNING`. Truncated or partial replays legitimately raise on the final corrupt block, but at `DEBUG` that was invisible — consumers can now detect a partial parse programmatically instead of trusting silently-incomplete output.

:::

::: tip Report asset cache

HTML reports can inline hero icons, item icons, and map images from a local user cache instead of bundling them in the wheel. Manage the cache from the CLI:

- `python -m gem reports assets path` — show the cache directories
- `python -m gem reports assets status [--strict]` — report which assets are present or missing
- `python -m gem reports assets download [--icons|--hero-icons|--item-icons] [--force]` — fetch icons (skips unchanged files, falls back across current and legacy Dota CDN paths)
- `python -m gem reports assets add-map <path>` — copy a local map image into the cache

All subcommands accept `--asset-dir`, and the cache root can be set via `GEM_REPORT_ASSET_DIR`. The same surface is importable as `gem.reports.ReportAssets`.

:::

## June 2026 — v0.3.0

A structural + correctness release. The supported top-level API (`gem.parse`, `gem.ParsedMatch`, `gem.find_player`, …) is unchanged.

::: warning Breaking: root-level compatibility shims removed

The root-level import shims from earlier releases have been removed:
`gem.reader`, `gem.models`, `gem.combatlog`, `gem.entities`, `gem.map_context`, `gem.replay_fetch`, and similar.

Use the supported top-level `gem.*` API or the grouped subpackages instead — `gem.binary.reader`, `gem.results.models`, `gem.combat.log`, `gem.state.entities`, … The public `gem.__all__` surface is unaffected, so `gem.parse`, `gem.ParsedMatch`, `gem.find_player`, etc. still work exactly as before.

:::

::: info Package reorganization

Internal modules are grouped into focused subpackages — `binary/`, `schema/`, `state/`, `combat/`, `extractors/`, `analysis/`, `catalog/`, `results/`, `reports/`, `replays/` — each with its own README. The supported public API is unchanged; `gem.api`, `gem.parser`, `gem.constants`, `gem.reports`, `gem.catalog`, and `gem.extractors` still import as before.

:::

::: tip Source-based combat attribution

Per-player combat scalars and per-target dicts now attribute damage/healing to the damage **source** (`damage_source_name`), matching OpenDota:

- `ParsedPlayer.damage` / `damage_taken` / `healing` mirror OpenDota's source-attributed per-target dicts (illusion-prefixed keys; spurious ability/modifier-name keys excluded)
- `tower_damage` is now essentially exact offline (~97.9–100% vs OpenDota, up from ~87%)
- `hero_damage` improved — summon/projectile damage is credited to the owning hero
- new `CombatLogEntry.damage_source_name` and `CombatLogEntry.will_reincarnate` fields
- new `CombatLogType` `(str, Enum)`, backward compatible with string labels (`log_type == "DAMAGE"`)
- unmapped combat-log proto types now resolve to `CombatLogType.UNKNOWN` instead of inflating damage via a `DAMAGE` fallback

:::

::: warning Correctness fixes

- **Day/night cycle** corrected to a 10-minute cycle with night beginning at 5:00 (was a wrong 15-minute assumption), fixing vision-window math
- **Ward lifespans** corrected — observer 360 s (10800 ticks), sentry 420 s (12600 ticks); previous values were off by ~15–35×
- **Teamfight attribution** — gold credited to the recipient, XP deltas read from monotonic `m_iTotalEarnedXP`, spatial guards added, centroid divisor counts only positioned deaths
- **Roshan conversion windows** clamped to the next Roshan boundary (no more double-counting across back-to-back Roshans)
- **Reincarnation deaths** (WK / Aegis trigger deaths) excluded from death curves and teamfight death counts
- **Coach-index remap** fixes scoreboard K/D/A attribution in coached/HLTV replays
- **S1 combat log** PURCHASE item resolution and default attacker/target hero flags
- **Fallback advantage curve** buckets each player by their actual game minute

:::

## May 2026

::: tip Dota 7.41 Fixture Refresh

`gem` now has a stronger replay-backed fixture path for modern Dota patches.

**Recent additions**

- OpenDota fixture download tooling for saving parsed replay data under `tests/fixtures/opendota`
- DreamLeague Season 29 fixture metadata for 7.41 validation work
- neutral item found event parsing across the parser, output models, and dataframes
- constants-audit coverage for newly observed item IDs

:::

::: info Camp Annotation Refresh

The neutral camp annotations were refreshed using replay evidence rather than manual map guesses alone.

**What changed**

- a new camp-audit script groups neutral deaths by `camp_zones.json`
- Source 2 combat logs now preserve neutral camp stack metadata and event locations where present
- confirmed 7.41 camp type swaps were applied to `camp_zones.json`
- the annotated map fixture now uses larger camp icons, type-colored rings, and a top-right legend

:::

## March 2026

::: tip Roshan Conversion Report

There is now a dedicated `Roshan Conversion` report tab and a matching Experimental Features page.

The new report separates:

- the **conversion label**
  `Low Conversion`, `Fight Conversion`, `Objective Conversion`, `Map Squeeze`, `Game-Closing Rosh`
- the **Aegis outcome**
  `Consumed In Fight`, `Expired After Use`, `Expired Unused`, `Denied`, `Window Lost`, `Game Ended`, `Unknown`

**Recent refinements**

- labels and Aegis outcomes are documented directly in the report
- the old single score was removed from the UI
- the report now explains how `Presence Delta` is calculated
- Roshan-fight timing now uses `first_death_tick` instead of the padded teamfight window start

This remains experimental because it is a replay-derived interpretation layer, not a native replay fact.

:::

::: warning Game-End Sampling Fix

`PlayerExtractor` now forces one final snapshot at the exact game-end tick and stops sampling after that point.

**Why this mattered**

- some player time series were drifting into the postgame scoreboard window
- this could inflate late sampled values such as `net_worth_t`
- it created false mismatches when validating against OpenDota

**Concrete impact**

- the sampled end state now reflects the actual replay game-end boundary
- the Tusk mismatch discovered during OpenDota validation was resolved by this fix

:::

::: info Gold Series Split

`gold_t` and `gold_t_min` now mean **current unspent gold only**.

`total_earned_gold_t` and `total_earned_gold_t_min` now mean **cumulative earned gold**.

**Why this mattered**

- the older fallback path could mix current gold and cumulative gold into the same field
- that made economy analysis harder to reason about
- buyback, purchase timing, and “cash on hand” questions need current unspent gold
- advantage curves and lane-economy summaries need cumulative earned gold

**Current state**

- current unspent gold is exposed
- cumulative earned gold is exposed
- reliable and unreliable gold are **not** exposed separately yet

:::

::: tip OpenDota Validation Harness

The OpenDota validator now supports more than a few pinned fixtures.

**It can now**

- randomly sample candidate matches from OpenDota feeds
- download missing replays automatically
- validate in `scalar`, `parsed`, or `full` mode
- request OpenDota replay parsing when richer fields are missing
- write manifests and JSON result files for repeatable checks

**Important validator clarification**

- final scalar checks use end-of-game values
- `[min]` fields are now treated as informational only
- the last whole-minute sample can legitimately precede game end by up to 59 seconds

:::

::: tip Farming Patterns Context

The experimental Farming Patterns work now has an explicit map-context layer.

**That layer uses**

- tower state
- Roshan and Aegis timing
- ward counts
- net-worth and XP advantage
- recent enemy presence by region

**Recent refinements**

- labels were made easier to read
- the old border/river special case was removed as a standalone category
- formulas, thresholds, drivers, and caveats are documented explicitly
- the report now treats route segments as useful farming-pattern evidence even when the support signals are noisy

This feature is still experimental by design.

:::

::: info Replay Edge Cases

There is now a dedicated internals page for replay-specific pitfalls, including:

- duplicate hero entities vs the canonical hero handle
- within-tick sampling caveats
- truncated or incomplete replays
- schema drift across builds
- inference limits for higher-level analytics

If you are debugging parser behavior, read this together with Parser Internals and Experimental Features.

:::

## Recommended follow-up pages

1. [Replay Edge Cases](./deep-dives/replay-edge-cases.md)
2. [Farming Patterns](./experimental/farming-patterns.md)
3. [Roshan Conversion](./experimental/rosh-conversion.md)
4. [Estimate Vision](./experimental/estimate-vision.md)
5. [Vision Modifiers](./experimental/vision-modifiers.md)
