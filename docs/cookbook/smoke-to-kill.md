# How Often Did a Smoke Lead to a Kill?

**Question.** After a team uses Smoke of Deceit, how often does it get a kill,
how quickly, and how often does it lose a hero instead?

## The facts

- `gem.build_smoke_analysis(match)`: each smoke's activation tick, team and
  members, and its `first_fight`, the first fight whose first death came within
  60 in-game seconds.
- `match.combat_log`: every hero death, with the killing and dying teams and
  the in-game time.
- `match.game_clock`: in-game seconds from the smoke, pauses excluded.

A kill is a hero death that is not an illusion and that the hero did not come
back from (`will_reincarnate` covers the Aegis and Reincarnation). The window is
the 60 seconds after the smoke; change `WINDOW_S` to widen it.

## The recipe

<<< @/../examples/cookbook/smoke_to_kill.py{python}

## On one match

`python examples/cookbook/smoke_to_kill.py 8974053011.dem`:

```text
 smoke   time    team  heroes  first_kill_after_s  first_loss_after_s  first_fight fight_winner
     1 -00:58    dire       5                <NA>                <NA>         <NA>         None
     2 -00:44 radiant       3                <NA>                <NA>         <NA>         None
     3  13:11 radiant       2                <NA>                  35           13         dire
     4  17:55 radiant       2                <NA>                  23           17         dire
     5  19:56    dire       2                   9                <NA>           20         dire
     6  23:49    dire       1                <NA>                <NA>         <NA>         None
     7  32:09 radiant       2                <NA>                <NA>         <NA>         None
```

Only one of the seven smokes got a kill: Dire's at 19:56, nine seconds in.
Both of Radiant's mid-game two-hero smokes lost a hero within 35 seconds.

## Across the fixtures

Over the 137 smokes in the 9 fixture replays:

- 74 got a kill within 60 s, a median of 26 s after the smoke;
- 47 lost a hero within 60 s;
- in 35 smokes the team both got a kill and lost a hero.

## What this does not say

- **Whether the smoke caused the kill.** A kill 50 seconds later may have
  nothing to do with it.
- **Who was seen.** The smoke breaking early, and whether the enemy saw the
  members, are on each smoke's `members`
  ([Smoke Analysis](../experimental/smoke-analysis)).
- **Pre-horn smokes.** Smokes at negative times are often used to walk to a
  rune or a lane and seldom lead to kills.

## Variations

- Count only smokes with at least two heroes: `table[table["heroes"] >= 2]`.
- Compare teams: `table.groupby("team")["first_kill_after_s"].describe()`.
- To know which smoked heroes were in the fight, see each `FightPlayer` in
  `smoke.first_fight.players`.
