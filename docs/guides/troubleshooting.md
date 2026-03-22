# Troubleshooting

Common setup and parsing issues, with quick fixes.

---

## Installation issues

### `python-snappy` build or import errors

`gem` depends on Snappy support for compressed packet payloads. If install/import fails:

- ensure you are on supported Python (3.10+),
- run `uv sync` from a clean environment,
- install system Snappy development libraries if your platform requires them.

Then retry:

```bash
uv sync
uv run python -c "import snappy; print('snappy OK')"
```

---

## Docs build issues

If docs fail locally:

```bash
cd docs
npm run docs:build
```

If build reports link issues, fix broken links in `docs/` rather than disabling checks.

Maintainers: docs dependencies are intentionally pinned to avoid accidental major-version breakage.

---

## Replay parsing issues

### Truncated or partially downloaded replay files

Some replays may end abruptly (live/unfinished/corrupted downloads). In those cases,
parsing may return partial data or terminate early depending on where truncation occurs.

Recommended checks:
- redownload replay from source,
- compare file size with expected source listing,
- test with a known-good replay to isolate environment vs file quality.

### “Missing” fields on entities

Valve schema/field names can shift across patches. A field that exists in one replay
may be absent or renamed in another.

Debug workflow:
1. confirm entity class name,
2. inspect available fields on that entity at runtime,
3. update field access logic to tolerate missing/renamed fields.

---

## Performance issues

### Parsing feels slow on large replay sets

Use these checks first:

- avoid heavy work directly inside hot callbacks,
- batch expensive post-processing after parse,
- prefer targeted extraction over collecting every possible field.

If needed, profile callback hotspots before optimizing parser internals.

---

## Still stuck?

Please open an issue with:

- Python version + OS,
- exact command run,
- traceback/log output,
- replay source (match id/salt if shareable),
- whether issue reproduces on multiple replays.
