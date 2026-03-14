# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Changelog tracking for future releases.

## [0.1.0] - 2026-03-14

### Added
- Initial public release of `gem-dota`.
- Core Source 2 replay parser pipeline (stream/reader/sendtables/field decoding/entities/string tables/parser).
- Game events and combat log normalization (Source 1 + Source 2 paths).
- Extractors for players, objectives, wards, courier, draft, and teamfights.
- Match assembly and dataframe export APIs.
- CLI and example scripts, including HTML match report.
- Validation, fuzzing, and parser robustness foundations.

[Unreleased]: https://github.com/whanyu1212/gem/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/whanyu1212/gem/releases/tag/v0.1.0
