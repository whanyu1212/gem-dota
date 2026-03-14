# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/whanyu1212/gem/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/whanyu1212/gem/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/whanyu1212/gem/releases/tag/v0.1.0
