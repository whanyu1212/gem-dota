# Who Stacked Each Camp, Who Cleared It, and What Did the Stacks Give?

**Question.** Which camps were stacked, and by whom? Who killed the stacked
creeps: a teammate, the stacker, or the enemy? And how much gold did stacked
camps give each player?

::: figure stacks
**Figure 1.** The 30 stacks of match 8856501050. First, each stack at its time,
on the row of the player the game credited with it: a bar is as tall as its
stacked creeps and split by who killed them. Rows by killer show who farmed the
stacks. Then the stacked camps, sized by how often each was stacked and ringed by
the side that stacked it, and each player's numbers: stacked creeps killed, their
gold, and its share of the player's neutral gold. Pick a stack, a camp or a
player to see its stacks in every part.
:::

## The facts

- `match.camp_stacks`: every stack the game counted. A camp spawned a wave
  while creeps from an earlier wave were still alive, and the game credited a
  player with it (`m_iCampsStacked`, OpenDota's `camps_stacked`). Each has its
  camp, tier, waves alive and player; `player_exact` says whether the credit left
  no choice of camp, or the camp was matched to the player by position.
- `match.neutral_creeps`: every creep a camp spawned, with its camp, when it
  spawned and died, and who killed it.
- `match.combat_log`: `GOLD` entries for killing a neutral (reason 14), and
  neutral `DEATH` entries.
- `player.lh_t_min`: last hits at 10:00, for supports and cores.

## What counts

- **A stacked creep** is one of the camp's creeps alive at a stack: the earlier
  waves and the new one. A camp stacked again while those creeps live adds only
  its new wave; the rest stay with the first stack.
- **The gold a stacked creep gave** is its killer's neutral-kill gold on the
  tick it died, split evenly over the neutrals that player's units killed on
  that tick. A summon's or an illusion's kill counts for its hero.
- **A pull** is a stacked creep a lane creep killed. It counts for no player.
- **Supports and cores**: the `SUPPORTS_PER_TEAM` (2) players of each side with
  the fewest last hits at 10:00 are supports. That is this recipe's choice;
  change it to use another.

The [core farm recipe](./core-farm) looks at the cores' whole income from 10 to
20 minutes; this one follows the stacks through the whole game.

## The recipe

<<< @/examples/cookbook/stacks.py{python}

## On one match

`python examples/cookbook/stacks.py 8856501050.dem`, with the stacks' first and
last rows and the largest flows:

```text
8856501050: 30 stacks (radiant 22, dire 8), 13 by supports; stacked creeps pulled: 1
 time_s  camp camp_type                             hero    side    role  exact  waves  creeps
    240     3   ancient               npc_dota_hero_lion radiant support   True      2       6
    240     6    medium               npc_dota_hero_lion radiant support   True      2       4
    300     1     large               npc_dota_hero_lion radiant support   True      2       6
    360     4     large          npc_dota_hero_nevermore    dire    core   True      2       3
    420    21     small npc_dota_hero_ancient_apparition radiant support   True      2       6
...
   4440     3   ancient          npc_dota_hero_pangolier    dire    core   True      2       4
   5460    16   ancient             npc_dota_hero_sniper radiant    core   True      2       6
Stacked by -> cleared by:
                         stacker stacker_side                     killer killer_side  enemy  creeps  gold
          npc_dota_hero_shredder      radiant     npc_dota_hero_shredder     radiant  False      35  1393
npc_dota_hero_ancient_apparition      radiant         npc_dota_hero_tiny     radiant  False      26   535
         npc_dota_hero_nevermore         dire    npc_dota_hero_nevermore        dire  False      14   449
              npc_dota_hero_lion      radiant     npc_dota_hero_shredder     radiant  False      12   475
         npc_dota_hero_pangolier         dire    npc_dota_hero_pangolier        dire  False       9   401
              npc_dota_hero_lion      radiant npc_dota_hero_ember_spirit        dire   True       7   201
              npc_dota_hero_lion      radiant       npc_dota_hero_sniper     radiant  False       7   276
            npc_dota_hero_rubick         dire    npc_dota_hero_nevermore        dire  False       5   219
...
                            hero    side    role  stacks  exact  killed  gold  neutral_gold
              npc_dota_hero_tiny radiant    core       1      0      32   824         14539
            npc_dota_hero_sniper radiant    core       2      1      15   592         12917
          npc_dota_hero_shredder radiant    core       8      6      48  1896         13956
              npc_dota_hero_lion radiant support       6      5       0     0           256
npc_dota_hero_ancient_apparition radiant support       5      4       0     0           469
         npc_dota_hero_nevermore    dire    core       4      3      19   668         23049
      npc_dota_hero_ember_spirit    dire    core       0      0       7   201          7966
         npc_dota_hero_pangolier    dire    core       2      1       9   401         20561
            npc_dota_hero_rubick    dire support       2      1       5   131          3298
            npc_dota_hero_treant    dire support       0      0       0     0          1571
```

Radiant made 22 of the 30 stacks, 19 of them by 20:00. Timbersaw stacked 8
camps and killed 48 stacked creeps, 35 of them his own, for 1,896 gold: 14% of
his neutral gold. Ancient Apparition's 5 stacks went to Tiny (26 creeps), and
Lion's 6 were split between Timbersaw, Sniper, Tiny and Ember Spirit, on the
other side, who took 7 of them. On Dire, Shadow Fiend and Pangolier mostly
stacked for themselves.

## Across the fixtures

The 9 fixture replays have 229 stacks:

| Match | Stacks (Radiant / Dire) | By supports | Stacked creeps killed by cores | Killed by the enemy | Cores' neutral gold from stacks |
|---|---|---|---|---|---|
| 8822520406 | 13 (3 / 10) | 5 | 58 of 61 | 12 | 16% |
| 8822593932 | 18 (11 / 7) | 8 | 90 of 96 | 11 | 11% |
| 8855188139 | 22 (8 / 14) | 12 | 95 of 111 | 6 | 11% |
| 8855242704 | 50 (25 / 25) | 27 | 204 of 236 | 11 | 11% |
| 8856501050 | 30 (22 / 8) | 13 | 130 of 135 | 9 | 5% |
| 8860187335 | 30 (11 / 19) | 25 | 129 of 139 | 10 | 10% |
| 8868259993 | 13 (6 / 7) | 4 | 56 of 58 | 14 | 25% |
| 8974053011 | 21 (6 / 15) | 6 | 98 of 99 | 8 | 13% |
| 9039619076 | 32 (16 / 16) | 29 | 141 of 145 | 6 | 15% |
| **All 9** | **229 (108 / 121)** | **129** | **1,001 of 1,080** | **87** | **10%** |

- **Who stacks:** supports made 129 of the 229 stacks (56%), from 29 of 32 on
  9039619076 to 6 of 21 on 8974053011. The game's credit fixed the camp for 89
  stacks; the other 140 were matched to their player by position.
- **Who clears:** cores killed 93% of the stacked creeps a player killed, and
  supports 79. 445 of the 1,080 (41%) were killed by the player who stacked them:
  Alchemist on 8855242704 stacked 13 camps and killed 96 stacked creeps for 3,297
  gold, a quarter of his neutral gold.
- **The enemy** killed 87 stacked creeps (8%), and lane creeps 14 (pulls).
- **What stacks gave:** 33,477 of the cores' 333,671 neutral gold (10%) came
  from stacked creeps, from 5% on 8856501050 to 25% on 8868259993.

## What this does not say

- **Whether a stack was worth it.** The gold is what the stacked creeps gave,
  not what the stacker or the farmer would have earned doing something else.
- **Who pulled the camp.** The game credits one player with a stack; a teammate
  who helped, or a stack made from range, is not in the credit.
- **Which hero a creep's gold went to when two players killed neutrals on one
  tick.** A creep's killer is the combat log's attacker on its death tick, and a
  creep that died on a tick another neutral died to someone else has no killer.

## Variations

- Change `SUPPORTS_PER_TEAM` or `ROLE_READING_S`, or replace `roles` with
  OpenDota's `player.lane_role`.
- Filter `stacked_creeps` to `pulled` to see which camps fed the
  [lanes](./lanes), and when.
- Group `stack_table` by `camp` and `camp_type` to ask which camps each side
  stacks, or by `time_s // 600` to see when.
