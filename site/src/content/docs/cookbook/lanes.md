# How Did Each Lane Go?

**Question.** Who laned where, how far ahead was each side in each lane by
the end of the laning stage, and what happened in the lane to get it there?

::: figure lanes
**Figure 1.** The three lanes of match 8856501050 at 6:00, the end of the
laning stage: each side's heroes, their net worth, XP, last hits and denies,
their earned gold by source, and the deaths, teleports and visits from other
lanes. Switch to 10:00, the reading people usually quote, for what came after
the laning stage: the deaths, teleports and visits up to 10:00.
:::

## The facts

- `ParsedPlayer.position_log`: each hero's position once a second, read with
  `gem.position_at_tick`.
- `lane_for_cell` (`gem.extractors.lane`): OpenDota's grid of which lane a map
  cell is on.
- `ParsedPlayer.net_worth_t_min`, `total_earned_xp_t_min`, `lh_t_min` and
  `dn_t_min`: net worth, XP, last hits and denies at every minute.
- `ParsedPlayer.gold_ledger`: earned gold by source at every minute, as in
  [what moved the lead](./lead).
- `match.combat_log`: hero deaths and Town Portal Scroll uses.

## Two readings: 6:00 and 10:00

The recipe reads each lane twice. `LANE_S`, 6:00, is the end of the laning
stage: on all 9 fixtures it comes before the first wisdom runes (taken at
7:06–7:12 in every match) and before any tower falls (the earliest fell at
7:06). `COMPARE_S`, 10:00, is the number people quote, and the minute OpenDota's
lane efficiency reads (`ParsedPlayer.lane_efficiency_pct`, from earned gold at
10:00). By then the wisdom runes have been taken (7:06–7:12 on every fixture)
and, in 6 of the 9 fixtures, the first tower has fallen.

## Who laned where

Each hero's lane is the one it spent the most of 0:00–6:00 in, on OpenDota's
lane grid. The figure shows the share when it is under 80%. On every fixture
this splits each side 2–1–2, with the lowest share a roaming Spirit Breaker's
30% (8860187335).

This is not `ParsedPlayer.lane`, which follows OpenDota and takes the first 10
minutes. On 8856501050 OpenDota puts Lion in mid as a roamer: over 10 minutes
he spent 276 seconds in mid and 276 top. Over the first 6 he spent 60% top.
The two disagree on 5 of the 90 heroes on the fixtures.

## What happened in the lane

Up to each reading, the recipe lists:

- **Deaths**, placed by where the victim was. A death outside the three lanes
  is listed apart. The killer's own lane is shown when it is another: a
  rotation's kill.
- **Teleports**: a Town Portal Scroll that moved the hero at least
  `TP_MIN_JUMP` (1,500) within `TP_LAND_S` (8 s), placed where it landed.
- **Visits**: a hero from another lane that stayed at least `MIN_VISIT_S`
  (20 s). The walk out of base before `BASE_S` (0:30) doesn't count.

## The recipe

<<< @/examples/cookbook/lanes.py{python}

## On one match

`python examples/cookbook/lanes.py 8856501050.dem`, the lanes and the first
reading (some columns left out):

```text
                            hero    side lane  share
              npc_dota_hero_tiny radiant  bot   1.00
            npc_dota_hero_sniper radiant  mid   1.00
          npc_dota_hero_shredder radiant  top   0.94
              npc_dota_hero_lion radiant  top   0.60
npc_dota_hero_ancient_apparition radiant  bot   0.86
         npc_dota_hero_nevermore    dire  top   0.95
      npc_dota_hero_ember_spirit    dire  mid   1.00
         npc_dota_hero_pangolier    dire  bot   1.00
            npc_dota_hero_rubick    dire  bot   0.61
            npc_dota_hero_treant    dire  top   0.71
lane  reading_s    side  net_worth   xp  last_hits  denies
 top        360 radiant       3556 2678         29       2
 top        360    dire       4695 3271         52      14
 mid        360 radiant       3113 2892         41       9
 mid        360    dire       2115 2251         25       1
 bot        360 radiant       3539 2723         38       5
 bot        360    dire       3543 2647         38       5
```

At 6:00 Dire's top lane was 1.1k ahead (Shadow Fiend had 48 last hits to
Timbersaw's 27), Sniper was 1.0k ahead of Ember Spirit in mid, and the bottom
lane was 4 gold apart. The 10:00 reading adds what came after: Sniper's
teleport top at 7:00, Shadow Fiend's death to Timbersaw at 7:13 with Sniper in
the lane, and Lion's death to Shadow Fiend a second later.

## Across the fixtures

Over the 27 lanes of the 9 fixture replays:

- The side ahead on net worth at 6:00 was still ahead at 10:00 in 22. The 5
  that changed sides were all within 330 gold at 6:00.
- The median gap grew from 789 at 6:00 to 1,034 at 10:00, and grew on the same
  side in 17 of the 22.

## What this does not say

- **Who won the lane.** The numbers are each side's, at two readings; which of
  them matters is the reader's call.
- **How the waves were handled.** Pulls, stacks and the lane's equilibrium
  aren't here: no fixture has a stack in its combat log (HY-150 looks for
  where the replay records them).
- **Where a hero was between seconds.** Positions are once a second, so a
  teleport's landing is placed within a second of it.

## Variations

- Change `LANE_S` and `COMPARE_S` for other readings (whole minutes).
- Group `lane_table` by `side` alone for each side's laning stage as a whole.
- Run it on many replays with `lane_gaps` to see how often each lane's leader
  at 6:00 stayed ahead.
