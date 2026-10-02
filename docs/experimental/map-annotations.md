# Map Regions and Camps

gem's map analysis (farming context, Roshan territory, map context) labels
positions with a **region** and farmed camps with a **camp** from its catalog.
This page shows both on the 7.41 map, and how each was checked against the
replays.

![gem's map regions and neutral camps on the 7.41 map](/map-annotations.jpg)

Every point is placed with the same projection as the HTML report maps, which
was fitted to replay landmarks (fountains, ancients, lotus pools, wisdom shrines
and outposts) to within about 60 world units.

## Regions

`gem.region_of(x, y)` returns one of five labels (`gem.MAP_REGIONS` lists them):

| Region | Where |
| --- | --- |
| `river` | The river's water between the top-lane and bottom-lane crossings, including both Roshan pools. The lanes are not river. |
| `radiant_half` / `dire_half` | Either side of the half line, which runs along the river's middle and, past its ends, straight out to the map edges. |
| `top_lotus` / `bottom_lotus` | 700 units round each lotus pool. Both teams contest these from their lanes, so they belong to neither half. |

The river outline is traced from the water in the map image
(`scripts/trace_river_region.py`); the lotus areas are centred on the replay's
`CDOTA_BaseNPC_LotusPool` entities. Tests pin the regions to replay entity
positions: both fountains and ancients and both mid tier-one towers are in their
own half, and both power-rune spawners, both Roshan pits and the Roshan spawner
are in the river.

For example, the share of each hero's sampled positions spent in the river:

```python
from collections import Counter

import gem

match = gem.parse("replay.dem")
for player in match.players:
    regions = Counter(gem.region_of(x, y) for _, x, y in player.position_log)
    print(player.hero_name, regions["river"] / max(regions.total(), 1))
```

## Neutral camps

`camp_zones.json` lists the 28 camps. Each camp's centre is its
`CDOTA_NeutralSpawner` entity, and its zone is the ellipse for its type. Each side
owns 14 camps with the same mix:

| Type | Per side |
| --- | ---: |
| Small | 2 |
| Medium | 5 |
| Large | 3 |
| Ancient | 1 |
| Flooded small | 1 |
| Flooded medium | 2 |

**Types** come from the replays, checked two ways on the 9 local fixtures:

- the spawner's `m_Type` when it is created (0 small, 1 medium, 2 large,
  3 ancient; flooded camps report their starting tier and change it as they
  evolve);
- the creeps that actually spawn there, matched to camp compositions on
  [Liquipedia's Neutral Creeps page](https://liquipedia.net/dota2/Neutral_Creeps).
  A large camp spawns Hellbears, Wildwings, Trolls, Warpines or the large
  Centaur and Satyr groups; a medium camp only ever spawns the medium groups.

Liquipedia's camp table still shows the older layout (10 large and 4 ancient
camps). Its [changelog](https://liquipedia.net/dota2/Neutral_Creeps/Changelogs)
has the 7.40 and 7.41 demotions that the replays and the catalog follow:
ancients by the stream ends and some large camps became medium camps, and the
medium camps by the offlane gates became small camps. The flooded camps by the
bounty runes (13 and 16) can evolve into ancient frog camps; the other two stop
at large.

**Owners** come from the combat log. Each neutral death carries the game's
`neutral_camp_team`, and every death at a camp carries the same value. All 28
camps agree with it except camp 22: it sits in Dire jungle, and the catalog
follows the terrain, which keeps the two sides mirrored, while the game files it
under Radiant.

## Regenerating

```bash
# The picture on this page
uv run python scripts/render_camp_zones_overlay.py --regions --width 1800 \
    --margin 40 --legend-panel 420 --output docs/public/map-annotations.jpg

# Re-trace the river from the map image (needs OpenCV)
uv run --with opencv-python-headless python scripts/trace_river_region.py --check
```

A map patch that moves the river or the camps needs a new map image, a new trace,
and new spawner positions; `tests/test_camp_zones_integration.py` checks the
camp centres, types and owners against the canonical replay.
