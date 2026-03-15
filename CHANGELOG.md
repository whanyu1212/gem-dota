# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/whanyu1212/gem-dota/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/whanyu1212/gem-dota/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/whanyu1212/gem-dota/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/whanyu1212/gem-dota/releases/tag/v0.1.0
