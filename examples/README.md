# examples/

Runnable scripts demonstrating gem's replay parsing capabilities.
Run any example from the project root (with the venv activated):

```bash
python examples/match_report.py path/to/your.dem          # comprehensive HTML report
python examples/extraction_demo.py                        # uses bundled fixture
python examples/extraction_demo.py path/to/your.dem       # or supply your own
python examples/steam_match_info.py <match_id>            # Steam API integration
```

## Scripts

| Script | What it demonstrates |
|---|---|
| `match_report.py` | Comprehensive HTML replay analysis dashboard (overview, combat, vision, economy, movement, draft, teamfights, and more) |
| `extraction_demo.py` | Developer-oriented baseline: full replay parse with combat log summary and periodic entity snapshots |
| `steam_match_info.py` | Fetches and displays match metadata from the Steam Web API (`STEAM_API_KEY` required) |

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
