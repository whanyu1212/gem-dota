# When Did Each Objective Fall, and Did Teams Convert Their Edges?

**Question.** When did each tower, barracks, Roshan and Tormentor fall, who
took it, and what came before it? And when a team won a fight or held the
Aegis, how often did it turn that into an objective?

::: figure objectives
**Figure 1.** All 34 objectives in match 8856501050 at their places on the
map, with the base as it stood at the end of the match. Drag on the timeline
to see the base at the end of another stretch, and pick an objective for who
damaged it in the 90 seconds before it fell and the fight that came before it
(a link opens that fight on the [fights page](./fights)). Below the map, each
team's edges and what they led to: pick a bar segment for its edges.
:::

## The facts

- `match.towers` and `match.barracks`: every building that fell, its owner and
  the last hit. A building counts for the side that didn't own it, so a deny
  still loses it.
- `match.roshans` and `match.tormentors`: every Roshan and Tormentor kill and
  who made it.
- `match.combat_log`: the damage to each building. A summon's damage counts for
  its owner, the combat log's damage source; lane and siege creeps are grouped.
- `match.fights`: gem's fights, with the kills each side scored.
- `match.game_clock`: in-game seconds, pauses excluded.

The two tier-4 towers of a side share one name in the combat log, so their
damage can't be told apart: their cards show the damage to both. The figure
places every building, Roshan and Tormentor where the replay's own entities put
them.

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
  match_id  time      kind                   name for_side                        last_hit  after_fight  after_fight_s
8856501050 13:24     tower    goodguys_tower1_bot     dire         npc_dota_hero_nevermore            6             10
8856501050 15:22     tower    goodguys_tower1_mid     dire         npc_dota_hero_nevermore            7             60
8856501050 17:16     tower    goodguys_tower1_top     dire    npc_dota_creep_badguys_melee            8            114
...
8856501050 91:35    roshan                 roshan  radiant            npc_dota_hero_sniper           35             26
8856501050 92:14  barracks  badguys_range_rax_mid  radiant              npc_dota_hero_tiny           35             64
8856501050 92:28     tower         badguys_tower4  radiant            npc_dota_hero_sniper           35             78

Each team's edges, by what they led to:
   team  edge  edges  converted  other side first  nothing
   dire aegis      6          4                 0        2
   dire fight     22          9                 6        7
radiant aegis      1          1                 0        0
radiant fight      9          2                 2        5
```

Dire won 22 fights on kills and took the next objective after 9 of them;
Radiant took it after 2 of its 9. Radiant's one Roshan, at 91:35, was followed
within a minute by both Dire tier-4 towers.

## Across the fixtures

Over the 197 objectives in the 9 fixture replays (109 towers, 40 barracks, 31
Roshans and 17 Tormentors), 164 fell within 2 minutes after a fight.

- **Fights won on kills:** 303. The team took the next objective after 117,
  the other side took one first after 44, and nothing fell after 142.
- **The Aegis:** 22 of the 31 Roshans were followed by a building for the
  killing team within five minutes.

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
