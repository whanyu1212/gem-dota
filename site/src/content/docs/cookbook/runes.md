# Who Took Each Rune, and What Happened While a Power Rune Lasted?

**Question.** Where did each rune spawn, and who took it, put it in a Bottle,
denied it, or left it? Who took the four bounties at 0:00, and who was near?
And while each power rune lasted, did its taker get a kill, hit Roshan or a
building, or did its team take an objective?

::: figure runes
**Figure 1.** The 98 runes of match 8856501050: each side's by kind, the four
spots with the runes each side took there, the 0:00 bounties, and every power
rune with what happened while it lasted. Pick a stage, or drag on the timeline
for a stretch of your own, to see the runes taken in it (the 0:00 bounties
stay). A highlighted power rune was followed by an objective for its team.
:::

## The facts

- `match.runes`: every power, bounty and water rune that spawned, from its
  entity in the replay: when and where it appeared, and how it ended
  (`picked_up`, `bottled`, `denied`, `not_taken`, `still_there`), with the
  player and, for a bottled rune, when the Bottle was used.
- `match.combat_log`:
  - `PICKUP_RUNE` entries: each rune taken and each Bottle used, timed by
    OpenDota's clock for its chat event (at most half a second from the game
    clock). A rune bottled, denied or not taken has no such entry and is timed
    by the game clock when it left the map;
  - each power rune's buff, `modifier_rune_*` added and removed, and an
    illusion rune's illusions (`modifier_illusion`);
  - hero deaths, and damage to Roshan and to buildings.
- `match.towers`, `match.barracks`, `match.roshans`, `match.tormentors`: the
  objectives.
- Hero positions (about one a second) and `gem.region_of` for the spots.

## Spots and stages

Each rune is at one of four spots: the top or bottom river (power and water
runes, and two of the four bounties at 0:00), or a side's jungle (bounties).
A bounty taken from the other side's jungle counts as such. A bounty nobody
took stays on the map and stacks with the next one, so one hero can take two
or three at once: each is its own rune.

The recipe splits the match into three stages: 0:00 to 6:00 (the
[lanes recipe](./lanes)'s laning stage, with the water runes), 6:00 to 20:00,
and 20:00 to the end. A rune counts in the stage it left the map in.

A rune put in a Bottle counts as taken when it was bottled. Using the Bottle
later is a second `PICKUP_RUNE` entry, which OpenDota also counts as a pickup;
the recipe ties it back to the rune.

## The 0:00 bounties

Four bounties spawn at the horn. For each, the recipe lists who took it, how
many seconds after the horn, whose it was (the river, the taker's own jungle,
or the other side's), and the enemy heroes within `NEAR` (1,200 world units)
of the taker at the pickup, from the heroes' sampled positions (about one a
second). It also lists every hero death up to 1:30,
counting the ones before the horn.

## While a power rune lasted

A power rune's buff starts when it is taken, or when it is used from a Bottle.
The combat log adds its modifier then and removes it when the buff ends, or
earlier when the hero dies. The recipe takes that window as it is. A buff can
run longer than its usual length, and the combat log's own duration agrees: in
8821954344 a shield buff that began at 42:08 lasted 99.75 s.

An illusion rune has no buff. Its two illusions appear a few ticks after the
pickup, and the window runs until both are gone, at most `ILLUSION_S` (75 s;
5 of the 28 on the fixtures ran the full 75).

For each window, the recipe lists:

- the taker's kills;
- the taker's damage to Roshan and to buildings;
- the objectives its team took during the window or within `AFTER_S` (30 s)
  after it.

A summon's or an illusion's kill or damage counts for its hero, the combat
log's damage source. An objective after a power rune is what followed it, not
what it caused.

## The recipe

<<< @/examples/cookbook/runes.py{python}

## On one match

`python examples/cookbook/runes.py 8856501050.dem`, with the power runes'
first and last rows:

```text
8856501050: runes taken by each side, by stage
     stage    side  power  water  bounty_own_jungle  bounty_other_jungle  bounty_river  denied
 0:00-6:00 radiant      0      0                  1                    0             1       3
 0:00-6:00    dire      0      1                  1                    1             1       0
6:00-20:00 radiant      2      0                  3                    0             0       1
6:00-20:00    dire      4      0                  4                    0             0       0
 20:00-end radiant      5      0                  7                    3             0       0
 20:00-end    dire     23      0                 16                   11             0       1

The 0:00 bounties:
          spot                    hero    side whose  after_horn_s enemies_near
   dire_jungle npc_dota_hero_nevermore    dire   own           0.0
radiant_jungle      npc_dota_hero_tiny radiant   own           0.0
     top_river    npc_dota_hero_treant    dire river           0.0
     bot_river      npc_dota_hero_lion radiant river           1.0
Hero deaths up to 1:30: 0

Power runes, and what happened while each lasted:
start          rune                       hero  from_bottle  lasted_s  kills  objectives
 6:10      illusion       npc_dota_hero_sniper        False      19.0      0           0
 8:00        shield       npc_dota_hero_treant        False      75.0      0           0
10:56  invisibility npc_dota_hero_ember_spirit         True      10.0      0           0
...
86:31        arcane npc_dota_hero_ember_spirit        False      50.0      0           0
90:22         haste     npc_dota_hero_shredder        False      22.0      0           0

Objectives the taker's team took during one or within 30 s after:
  19:24 regeneration, npc_dota_hero_ember_spirit: roshan
  23:14 arcane, npc_dota_hero_ember_spirit: goodguys_tower2_top
  35:11 illusion, npc_dota_hero_ember_spirit: goodguys_tower2_mid
  56:13 arcane, npc_dota_hero_ember_spirit: goodguys_tower3_top, goodguys_melee_rax_top
  60:56 shield, npc_dota_hero_ember_spirit: goodguys_range_rax_top, goodguys_tower3_mid, goodguys_melee_rax_mid, goodguys_range_rax_mid
  70:33 haste, npc_dota_hero_ember_spirit: goodguys_tower3_bot

6 of 34 power runes were followed by an objective for the taker's team during them or within 30 s after.
```

Dire took 27 of the 34 power runes, 23 of them after 20:00. Ember Spirit had 20
of the 34 windows, 15 of them from a Bottle. Dire also took 12 bounties from
Radiant's jungle; Radiant took 3 from Dire's. All four 0:00 bounties were taken
within a second of the horn, each by its own side or in the river, with no
enemy within 1,200 units, and no hero died before 1:30.

## Across the fixtures

The 9 fixture replays have 514 runes:

- **Taken or bottled:** 478 (253 bounties, 193 power runes, 32 water runes).
  Of the power runes, 131 were taken after 20:00, and none before 6:00.
- **Bounties:** 145 taken from the taker's own jungle, 90 from the other
  side's, and 18 in the river at 0:00.
- **Denied:** 5. **Not taken** (gone at the next spawn): 15, all power or
  water runes. **Still there** when the game ended: 16, 11 of them bounties.
- **The 0:00 bounties:** all 36 were taken within 13 s of the horn, 6 from the
  other side's jungle. 7 had an enemy hero within 1,200 units at the pickup.
  Only one replay had a death before 1:30, two heroes, both before the horn.

Of the 192 power-rune windows (106 of them from a Bottle), 26 had a kill by the
taker, and 51 were followed by an objective for the team during the window or
within 30 s after:

| Rune | Windows | With a kill | With an objective |
|---|---|---|---|
| Arcane | 31 | 6 | 9 |
| Haste | 29 | 5 | 6 |
| Double Damage | 28 | 7 | 8 |
| Illusion | 28 | 1 | 7 |
| Shield | 27 | 4 | 12 |
| Regeneration | 26 | 3 | 4 |
| Invisibility | 23 | 0 | 5 |

## What this does not say

- **Whether a rune decided anything.** An objective after a power rune came
  next; the team may have been taking it anyway.
- **Who fought over a rune.** The pickup's taker is known, and who was near at
  0:00; who walked to a rune and left without it is not in this recipe.
- **Wisdom runes.** They have no entity in the replay, and they are in the
  [objectives recipe](./objectives).

## Variations

- Change `NEAR` to ask who was close to the 0:00 bounties, or `AFTER_S` to
  widen what follows a power rune.
- Filter `rune_windows` to `double_damage` and join the `killed` heroes on the
  [fights](./fights) they died in.
- Group `rune_table` by `hero` and `rune` to ask who uses a Bottle for which
  runes.
