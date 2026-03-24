# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Objective-aware farming context helpers for experimental farming-pattern analysis. These bucket tower state, Roshan/Aegis timing, ward counts, net-worth/XP advantage, and enemy presence into replay-time context that can be joined to camp visits.
- `ParsedPlayer.total_earned_gold_t` — cumulative earned gold at regular sample cadence, exposed alongside the existing per-minute `total_earned_gold_t_min`.

### Changed
- `ParsedPlayer.gold_t` / `gold_t_min` now represent current unspent gold only (`m_iGold`). They no longer fall back to cumulative earned-gold fields.
- DataFrame export now includes both current unspent gold and cumulative earned gold at regular sample cadence.
- OpenDota validator minute-snapshot fields (`[min]`) are now informational only instead of pass/fail parity checks against final Steam scalars, since the last minute boundary can legitimately precede game end by up to 59 seconds.

### Fixed
- Player time-series sampling now stops immediately after the forced game-end snapshot. This removes postgame drift from sampled player stats, including inflated late `net_worth_t` values after `DOTA_COMBATLOG_GAME_STATE == 6`.
- OpenDota scalar validation for `net_worth` now reflects the small residual divergence between replay-exposed net-worth fields and Steam's final server scalar.
- Experimental farming-context labels and thresholds were refined to be easier to read in reports, and the old border/river special case was removed as a standalone category.

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

[Unreleased]: https://github.com/whanyu1212/gem-dota/compare/v0.2.6...HEAD
[0.2.6]: https://github.com/whanyu1212/gem-dota/compare/v0.2.5...v0.2.6
[0.2.5]: https://github.com/whanyu1212/gem-dota/compare/v0.2.4...v0.2.5
[0.2.4]: https://github.com/whanyu1212/gem-dota/compare/v0.2.3...v0.2.4
[0.2.3]: https://github.com/whanyu1212/gem-dota/compare/v0.2.2...v0.2.3
[0.2.2]: https://github.com/whanyu1212/gem-dota/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/whanyu1212/gem-dota/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/whanyu1212/gem-dota/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/whanyu1212/gem-dota/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/whanyu1212/gem-dota/releases/tag/v0.1.0
