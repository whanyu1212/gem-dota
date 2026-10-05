# Where Did Each Team Ward, and What Could the Wards See?

**Question.** Where did each team put its observer and sentry wards, how long
did they last, and how much of what an observer's circle covers could the
team actually see?

::: figure wards
**Figure 1.** The wards up from 40:00 to 46:00 in match 8856501050, the
stretch around the fight [played back on the home page](/). Drag on the
timeline below the map to pick another stretch, filter by team or ward type,
and click a ward for who placed it, when, and how it ended. Positions and
times are exact; the circle is gem's vision model, not what the ward saw.
:::

## The facts

- `match.wards`: every ward with its exact position, the tick it went up, and
  the tick it expired or was killed, with the killer.
- `gem.region_of(x, y)`: the map region, here folded into the warding team's
  own half, the enemy's half, or the river.
- `gem.analysis.vision.OBSERVER_VISION_RADIUS`: the vision model's observer
  radius, 1,600 world units. It is a flat circle: cliffs and trees that block
  the game's real vision are not in it.
- `match.hero_visibility_events` (read as `gem.hero_visibility_at` does): the
  replay's own record of whether each team could see each hero. This is the
  game's answer, terrain and trees included.
- `player.position_log`: each hero's position, sampled about once a second.
- `gem.build_smoke_analysis(match)`: who was under Smoke of Deceit, and when.

A ward is up from its placement tick until it is killed or expires (gone on
that tick). Times are in-game seconds, pauses excluded.

## The recipe

<<< @/examples/cookbook/wards.py{python}

## On one match

`python examples/cookbook/wards.py 8856501050.dem` lists all 221 wards. The
first rows, then the summaries:

```text
  match_id    team     type                           placer placed  lasted_s     how                           killer       region
8856501050    dire observer             npc_dota_hero_treant -01:00     339.0  killed             npc_dota_hero_sniper    dire_half
8856501050 radiant observer           npc_dota_hero_shredder -00:42     360.0 expired                                  radiant_half
8856501050    dire observer             npc_dota_hero_treant -00:26     360.0 expired                                  radiant_half
8856501050 radiant observer               npc_dota_hero_lion  00:17     360.0 expired                                  radiant_half
8856501050 radiant   sentry               npc_dota_hero_lion  00:32      23.0  killed          npc_dota_hero_nevermore    dire_half
...

Observers by team and side of the map:
   team       side  placed  median_lasted_s  killed
   dire enemy half      30            146.0      18
   dire   own half       9            360.0       4
   dire      river       2            360.0       0
radiant enemy half       7            360.0       1
radiant   own half      33            360.0      13
radiant      river       1            360.0       0

Seconds enemy heroes spent inside live observer circles:
  match_id    team  seconds  visible  hidden  unknown  smoked
8856501050    dire     1937     1519     418        0     104
8856501050 radiant     1775     1192     583        0     168

How often the warding team could see them, by distance from the ward:
 distance  seconds  visible  visible_pct
    0-400      337      330         97.9
  400-800      916      807         88.1
 800-1200     1049      773         73.7
1200-1600     1410      801         56.8
```

Dire put 30 of its 41 observers in Radiant's half, and 18 of those were
killed; Radiant kept 33 of its 41 at home. Inside Dire's circles, Dire could
see the Radiant hero 1,519 of 1,937 seconds; inside Radiant's, Radiant saw the
Dire hero 1,192 of 1,775.

## Across the fixtures

Over the 1,140 wards in the 9 fixture replays (429 observers, 711 sentries):

- 165 of the 429 observers were killed; the other 264 expired;
- observers in the enemy's half were killed more often: 98 of 216, against 65
  of 200 in the team's own half and 2 of 13 in the river;
- a killed observer lasted a median of 1:43;
- 244 of the 711 sentries were killed.

Enemy heroes spent 22,376 seconds inside live observer circles, leaving out
1,367 seconds under smoke. The warding team could see them for 15,522 of those
seconds, and they were hidden for 6,854. How often they were seen falls with the
distance from the ward:

| Distance from the ward | Seconds | Seen |
|---|---|---|
| 0–400 | 1,519 | 95.1% |
| 400–800 | 4,552 | 80.5% |
| 800–1,200 | 7,046 | 69.5% |
| 1,200–1,600 | 9,259 | 59.6% |

## What this does not say

- **What the ward itself saw.** "Seen" is the team's visibility, from any
  source: a hero, a creep or another ward may have seen the hero instead.
  "Hidden" is the clearer fact: the circle covered the hero and the team could
  not see it.
- **Why a hero was hidden.** Cliffs and trees block a ward's vision, and so does
  invisibility: Shadow Blade, Glimmer Cape, Treant's Nature's Guise and other
  invisible heroes count as hidden here. Only smoke is counted apart.
- **The true shape of a ward's vision.** That needs the map's terrain and trees,
  which the replay does not carry.
- **Positions between samples.** Hero positions are sampled about once a
  second, so a second is the unit of the counts.

## Variations

- Change the `step` of `by_distance` for finer distance bands.
- Filter `ward_table` to one placer (`table["placer"] == "npc_dota_hero_lion"`)
  to follow a support's wards.
- Join `circle_samples` with `match.fights` to ask how often the enemy was seen
  coming into a fight.
