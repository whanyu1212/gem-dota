# Replay fixtures

Small `*_truncated.dem` files are committed for fast parser and fuzz coverage.
Complete replay files are intentionally ignored and live locally under
`tests/fixtures/opendota/`; their OpenDota JSON snapshots and
`opendota/manifest.json` metadata are committed.

Synchronize the canonical short TI2026 replay:

```bash
uv run python scripts/sync_opendota_fixtures.py
```

Select broader tiers or an exact regression fixture when needed:

```bash
uv run python scripts/sync_opendota_fixtures.py --tier extended --tier stress
uv run python scripts/sync_opendota_fixtures.py --match 8855188139
uv run python scripts/sync_opendota_fixtures.py --all-active --verify-only
```

The synchronizer downloads into a temporary directory, verifies the recorded
decompressed size and SHA-256 digest, and only then installs the replay. A
manifest `artifact_url` takes precedence when present; the original Valve
`replay_url` remains the fallback source.

## Fixture tiers

- `canonical`: short TI2026 replay used by generic full-replay integration tests.
- `extended`: medium TI2026 replay used by the default OpenDota parity gate.
- `stress`: 93-minute TI2026 replay for explicit long-match validation.
- `performance-baseline`: replay retained for comparison with performance issue #143.
- `regression`: feature-specific replay selected by exact match ID.
- `archive`: deprecated replay retained as metadata and available only with
  `--include-deprecated`.

Deprecation is metadata-only: keep the manifest entry, set `status` to
`deprecated`, and point `replaced_by` at an active fixture. Do not commit full
replays to normal Git history.
