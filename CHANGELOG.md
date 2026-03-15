# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/whanyu1212/gem-dota/compare/v0.2.2...HEAD
[0.2.2]: https://github.com/whanyu1212/gem-dota/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/whanyu1212/gem-dota/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/whanyu1212/gem-dota/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/whanyu1212/gem-dota/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/whanyu1212/gem-dota/releases/tag/v0.1.0
