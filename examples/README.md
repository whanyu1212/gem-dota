# examples/

Runnable scripts demonstrating gem's replay parsing capabilities.
Run any example from the project root (with the venv activated):

```bash
python examples/extraction_demo.py                        # uses bundled fixture
python examples/extraction_demo.py path/to/your.dem       # or supply your own
python examples/ward_smoke_rosh.py path/to/your.dem       # focused vision/objective report
```

## Scripts

| Script | What it demonstrates |
|---|---|
| `extraction_demo.py` | Full replay parse: combat log summary (damage, kills, heals, abilities, gold/XP), entity state snapshots every ~1 min, ward placements, smoke events, hero level/XP progression |
| `ward_smoke_rosh.py` | Focused: observer/sentry ward placements with coordinates, Smoke of Deceit activations with hero group composition, Roshan kills with respawn windows |

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
