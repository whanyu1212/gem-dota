# When Did Each Objective Fall, and Did Teams Convert Their Edges?

**Question.** When did each tower, barracks, Roshan and Tormentor fall, and
each wisdom rune get taken, who took it, and what came before it? And when a
team won a fight or held the Aegis, how often did it turn that into an
objective?

::: figure objectives
**Figure 1.** All 57 objectives in match 8856501050 at their places on the
map, with the base as it stood at the end of the match, and each wisdom rune as
a dot around the shrine it was taken at. Drag on the timeline to see the base
at the end of another stretch, and pick an objective for who damaged it in the
90 seconds before it fell (or took it, and from whose shrine) and the fight
that came before it (a link opens that fight on the [fights page](./fights)).
Below the map, each team's edges and what they led to (pick a bar segment for
its edges), and who took each shrine's wisdom runes.
:::

## The facts

- `match.towers` and `match.barracks`: every building that fell, its owner and
  the last hit. A building counts for the side that didn't own it, so a deny
  still loses it.
- `match.roshans` and `match.tormentors`: every Roshan and Tormentor kill and
  who made it.
- `match.combat_log`: the damage to each building. A summon's damage counts for
  its owner, the combat log's damage source; lane and siege creeps are grouped.
- `match.combat_log`: every wisdom rune taken (`PICKUP_RUNE` entries of the
  wisdom type, whose `value` is the player's slot) and the XP it gave (XP
  entries of reason 4).
- `match.fights`: gem's fights, with the kills each side scored.
- `match.game_clock`: in-game seconds, pauses excluded.

The two tier-4 towers of a side share one name in the combat log, so their
damage can't be told apart: their cards show the damage to both. The figure
places every building, Roshan, Tormentor and wisdom-rune shrine where the
replay's own entities put them.

## Wisdom runes

A wisdom rune spawns at each side's shrine at 7:00 and every 7 minutes after.
The recipe places each pickup at the shrine on the half of the map the hero
was on: a rune taken from the other side's shrine counts for the side that
took it. Its XP goes to the picker's team: on the fixtures every wisdom-rune
XP entry, 228 of 228, came within 3 ticks of a pickup, two heroes' worth per
rune.

For each spawn, `wisdom_runes` says who took each shrine's rune before the
next one: its own side, the other side, or nobody. The replay keeps no entity
for the rune itself, so a rune nobody took is only that: not taken before the
next spawn, or before the game ended. On the fixtures no shrine was ever taken
from twice between two spawns.

## Did each team convert its edges?

An *edge* is a moment a team was ahead, and the recipe reports what it led to,
nothing more:

- **A fight won on kills.** The first building or Roshan within `WINDOW_S`
  (120 in-game seconds) after the fight ended was the team's (*converted*), the
  other side's (*other side first*), or nothing fell.
- **The Aegis.** After each Roshan the team killed, the buildings it took in the
  next `AEGIS_S` (300) seconds, the Aegis's five minutes.

"Converted" says only that the objective came next. It doesn't say the fight or
the Aegis is why.

## The recipe

<<< @/examples/cookbook/objectives.py{python}

## On one match

`python examples/cookbook/objectives.py 8856501050.dem`, the first and last
rows, then each team's edges:

```text
  match_id  time        kind                   name for_side                         last_hit  after_fight  after_fight_s
8856501050 07:05 wisdom_rune       dire_wisdom_rune     dire             npc_dota_hero_rubick            2             61
8856501050 07:14 wisdom_rune    radiant_wisdom_rune  radiant           npc_dota_hero_shredder            2             70
8856501050 13:24       tower    goodguys_tower1_bot     dire          npc_dota_hero_nevermore            6             10
8856501050 14:59 wisdom_rune    radiant_wisdom_rune  radiant               npc_dota_hero_lion            7             37
...
8856501050 92:14    barracks  badguys_range_rax_mid  radiant               npc_dota_hero_tiny           35             64
8856501050 92:17    barracks  badguys_melee_rax_mid  radiant    npc_dota_creep_goodguys_melee           35             67
8856501050 92:28       tower         badguys_tower4  radiant           npc_dota_hero_shredder           35             78
8856501050 92:28       tower         badguys_tower4  radiant             npc_dota_hero_sniper           35             78

Each team's edges, by what they led to:
   team  edge  edges  converted  other side first  nothing
   dire aegis      6          4                 0        2
   dire fight     22          9                 6        7
radiant aegis      1          1                 0        0
radiant fight      9          2                 2        5

Each side's wisdom runes, by who took them:
   spot  spawns  own side  other side  not taken  game ended
   dire      13        11           0          1           1
radiant      13        10           2          0           1
```

Dire won 22 fights on kills and took the next objective after 9 of them;
Radiant took it after 2 of its 9. Radiant's one Roshan, at 91:35, was followed
within a minute by both Dire tier-4 towers. Dire took 2 of the 13 runes at
Radiant's shrine (Ember Spirit at 64:09, Treant Protector at 74:02); Radiant
took none of Dire's 13. A rune's XP grows with each spawn: the picker's team got
400 for a 7:00 rune, and 7,000 for the one taken at 84:57.

## Across the fixtures

Over the 197 buildings and bosses in the 9 fixture replays (109 towers, 40
barracks, 31 Roshans and 17 Tormentors), 164 fell within 2 minutes after a
fight.

- **Fights won on kills:** 303. The team took the next objective after 117,
  the other side took one first after 44, and nothing fell after 142.
- **The Aegis:** 22 of the 31 Roshans were followed by a building for the
  killing team within five minutes.

- **Wisdom runes:** 116 of the 126 spawned were taken. Each side took its own
  rune 93 times and the other side's 23 times; 9 of the 10 left were still there
  when the game ended. The first runes, at 7:00, were taken within 14 seconds in
  17 of the 18.

Heroes do more of the work the deeper the tower. Of the damage to towers in the
90 seconds before they fell, heroes dealt:

| Tier | From heroes |
|---|---|
| 1 | 56% |
| 2 | 78% |
| 3 | 88% |
| 4 | 90% |

## What this does not say

- **Whether a team is good at objectives.** The counts are what followed each
  edge. A team that is behind has fewer edges, and a converted edge may have
  been a tower the enemy left to defend elsewhere.
- **What happened while a team had more heroes alive.** A pickoff that isn't a
  fight in gem's sense doesn't count as an edge here.
- **Who took a Roshan's items.** The Aegis, Cheese and Refresher Shard are in
  [Roshan and the next fight](./roshan-next-fight).

## Variations

- Change `WINDOW_S` or `AEGIS_S` to widen or narrow what counts.
- Filter `edges` to fights with `deaths >= 3` (join on `match.fights`) to ask
  the question of teamfights only.
- Use `building_damage` to ask who pushes: each hero's share of the damage to
  buildings over a match.
