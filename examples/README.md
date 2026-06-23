# examples/

Runnable scripts demonstrating gem's replay parsing capabilities.
Run any example from the project root (with the venv activated):

```bash
python examples/quickstart.py path/to/your.dem            # minimal: KDA, draft, wards, 0.4.0 taste
python examples/opendota_parity.py                        # 0.4.0 OpenDota-parity showcase (no-arg: see note below)
python examples/opendota_parity.py path/to/your.dem       # or supply your own
python examples/match_report.py path/to/your.dem          # comprehensive HTML report
python examples/extraction_demo.py                        # uses bundled fixture
python examples/extraction_demo.py path/to/your.dem       # or supply your own
python examples/steam_match_info.py <match_id>            # Steam API integration
```

## Scripts

| Script | What it demonstrates |
|---|---|
| `quickstart.py` | Minimal high-level `gem.parse()` intro: per-player KDA/net worth, draft, ward counts, plus a taste of the 0.4.0 OpenDota-parity fields |
| `opendota_parity.py` | Full 0.4.0 OpenDota match-API parity surface — final inventory, OpenDota-style kill breakdown, building-status bitmasks, objectives timeline, per-inflictor/per-target combat dicts, purchase timeline, ward departure logs, and the new `catalog` helpers. Cross-checks against the sibling `<match_id>.opendota.json` when present |
| `match_report.py` | Thin wrapper around `gem.reports.write_html_report()` for a comprehensive HTML replay dashboard |
| `extraction_demo.py` | Developer-oriented baseline: low-level `ReplayParser` + entity polling, with combat log summary and periodic entity snapshots |
| `steam_match_info.py` | Fetches and displays match metadata from the Steam Web API (`STEAM_API_KEY` required) |

## Replay fixtures (`opendota_parity.py` no-arg default)

The full OpenDota validation replay and its sibling `<match_id>.opendota.json`
(which powers the parity cross-check) are **local/ignored downloads, not committed**
to the repo (see the root `CLAUDE.md` and `tests/fixtures/` notes). With no argument,
`opendota_parity.py` prefers that download when present (full match + parity
cross-check), and otherwise falls back to the committed but **truncated** TI14
replay — which runs on a *partial* match with no OpenDota reference, and prints a
heads-up saying so. For the complete experience, fetch a replay:

```bash
uv run python -c "import gem; gem.fetch_replay(8822520406, 'tests/fixtures/opendota')"
```

or pass any replay path with a sibling `<match_id>.opendota.json` to enable the
cross-check.

## Ward coordinates

All ward placements get exact entity coordinates. The key: every entity event on a live
ward carries its position — including `UPDATED` events on recycled slots. Match each
combat log `ITEM` event to the nearest entity event within ±60 ticks, without globally
consuming entity records (slots are reused across the game).

## Smoke "no heroes resolved"

If a smoke `ITEM` event is recorded but the group list is empty, it means the hero
activated smoke while already inside a sentry ward's truesight radius (or another
instant-dispel condition). The item was genuinely consumed but broke before anyone
received the buff. This is correct game behaviour, not a parsing gap.

## gem.constants

Both examples use `gem.constants` for display names (heroes, items, abilities) and
XP thresholds. The bundled data lives in `src/gem/data/` and is regenerated from
`refs/dotaconstants/` by running:

```bash
python scripts/build_constants.py
```

The `refs/` folder is a development reference only and is not required at runtime.
