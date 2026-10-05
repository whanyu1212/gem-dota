# Where Were the Fights, and Who Got the Kills?

**Question.** Where did a match's fights happen, which side got more kills in
each, and did that side also take the next building or Roshan?

::: figure fights
**Figure 1.** All 36 fights in match 8856501050, placed at the centre of their
deaths, sized by deaths and coloured by the side with more kills. Filter by
size, drag on the timeline to pick a stretch, and pick a fight for its card.
Below the map, the picked fight opens in the [home page's](/) fight player:
the activity log, a recap of each death and the damage timeline for every
fight, and the map playback for fights with 3 or more deaths. It opens on the
biggest fight, 42:34.
:::

## The facts

- `match.fights`: gem's fights (every size), with their deaths, the kills
  each side scored, the centre of their deaths, and each player's gold and XP
  near the fight.
- `match.towers`, `match.barracks` and `match.roshans`: every building that fell
  and every Roshan kill. A building counts for the side that didn't own it, so a
  deny still loses it; Roshan counts for the team that killed it.
- `match.game_clock`: in-game seconds, pauses excluded.
- `gem.region_of(x, y)`: the region of a fight's deaths.

"More kills" is just that: the side that scored more hero kills in the fight,
or even when the counts match (`Fight.winner`). The window after a fight is
`WINDOW_S`, 120 in-game seconds from the fight's end.

## The recipe

<<< @/examples/cookbook/fights.py{python}

## On one match

`python examples/cookbook/fights.py 8856501050.dem`, the first and last rows:

```text
  match_id  fight start  deaths  radiant_kills  dire_kills more_kills       region                   next next_for  next_after_s
8856501050      1 01:27       1              0           1       dire    dire_half                   None     None          <NA>
8856501050      2 05:22       2              2           0    radiant    dire_half                   None     None          <NA>
8856501050      3 06:58       2              1           1       even radiant_half                   None     None          <NA>
...
8856501050     17 32:03       5              2           3       dire radiant_half                 roshan     dire            48
8856501050     19 42:34      10              4           6       dire radiant_half                   None     None          <NA>
8856501050     22 46:41       6              4           2    radiant radiant_half                 roshan     dire            14
...
8856501050     35 90:28       5              5           0    radiant radiant_half                 roshan  radiant            26
8856501050     36 92:23       4              3           1    radiant    dire_half                   None     None          <NA>

31 of 36 fights had a side with more kills; 19 of those had a building fall or Roshan killed within 120 s, and the side with more kills got 11 of them.
```

Dire had more kills in 22 of the 36 fights and Radiant in 9. Fight 22 shows
why "more kills" is only half the story: Radiant scored 4 of its 6 deaths, and
Dire killed Roshan 14 seconds after it ended.

## Across the fixtures

Over the 331 fights in the 9 fixture replays:

- 303 had a side with more kills;
- 161 of those were followed within 2 minutes by a building falling or a
  Roshan kill;
- the side with more kills got 117 of those 161.

The bigger the fight, the more often it went that way: the side with more kills
got what fell next after 85 of 123 one-death fights, and after 32 of 38 fights
with two or more deaths.

## What this does not say

- **Whether the fight won the building.** A tower can fall to a push that had
  nothing to do with the fight before it; the 2-minute window is a choice.
- **Who won the fight in any other sense.** Gold, experience, buybacks and
  Aegis lives are on each fight (`FightPlayer`), not in "more kills".
- **OpenDota's teamfights.** gem's fights include one-death skirmishes;
  OpenDota's teamfight definition is `opendota_teamfights`.

## Variations

- Change `WINDOW_S` to widen or narrow what counts as "next".
- Filter `fight_table` to `deaths >= 3` to ask the question of teamfights only.
- Use `gem.build_fight_timeline(match, start, end)` for any fight's casts,
  damage and deaths, the facts behind the player above.
