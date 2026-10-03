# How Fast Did Each Core Farm from 10 to 20 Minutes?

**Question.** Between 10:00 and 20:00, how much did each team's carry, mid and
offlaner earn, how much of it came from the jungle, and where on the map were
they?

## The facts

- `player.total_earned_gold_t_min` and `player.lh_t_min`: earned gold and last
  hits at each minute (index 10 is 10:00).
- `match.combat_log`: every neutral creep death, with its killer and in-game
  time.
- `player.position_log`: sampled `(tick, x, y)` positions, about one a second.
- `gem.region_of(x, y)`: `"radiant_half"`, `"dire_half"`, `"river"`,
  `"top_lotus"` or `"bottom_lotus"`; see [Map Regions and
  Camps](../experimental/map-annotations).
- `player.lane_role` (1 safe lane, 2 mid, 3 off lane) and
  `player.lane_last_hits` (last hits at 10:00).

The cores are each team's safe-lane, mid and off-lane player with the most last
hits at 10:00, the rule the HTML report's Farming tab uses. Earned gold counts
every source (creeps, kills, passive income), not only farm; the neutral kills
column shows how much of the farm came from the jungle.

## The recipe

<<< @/../examples/cookbook/core_farm_10_to_20.py{python}

## On one match

`python examples/cookbook/core_farm_10_to_20.py 8974053011.dem`:

```text
   team    role              hero  gold_per_min  last_hits  neutral_kills  own_half  river  enemy_half
radiant   carry      life_stealer        511.00         91             37      1.00   0.00        0.00
radiant     mid      ember_spirit        366.60         58             34      0.94   0.03        0.03
radiant offlane abyssal_underlord        540.50        105             38      0.92   0.00        0.06
   dire   carry             razor        860.30        168             73      0.46   0.00        0.53
   dire     mid            huskar        665.40        101             70      0.20   0.15        0.65
   dire offlane         dark_seer        599.80        118             76      0.30   0.05        0.64
```

Razor earned 860 gold a minute, with 168 last hits and 73 neutral kills, and
spent half the window in Radiant's half. Every Dire core spent more time on
Radiant's side than its own, while Radiant's three cores barely left theirs.

## Across the fixtures

Averages over the 48 cores in the 8 fixtures that reach 20:00:

```text
role     gold_per_min  last_hits  neutral_kills  own_half  river  enemy_half
carry          675.25     132.81          78.88      0.80   0.04        0.15
mid            546.36      87.69          38.19      0.63   0.10        0.27
offlane        580.08     101.50          52.31      0.50   0.04        0.45
```

## What this does not say

- **Why** a core farmed where it did: map pressure, a plan or a lost lane all
  look the same here.
- **Positions are samples,** about one a second, not a continuous path.
- **Lotus pools** count towards neither half, so `own_half + river +
  enemy_half` can be slightly under 1.

## Variations

- Change `START_MIN` and `END_MIN`, or compare windows side by side.
- For camp-by-camp visits, use `gem.build_farming_routes(match)`; each segment
  has its camp, ticks, neutral kills and the gold and XP earned during the visit.
- Swap `total_earned_gold_t_min` for `total_earned_xp_t_min` to compare XP.
