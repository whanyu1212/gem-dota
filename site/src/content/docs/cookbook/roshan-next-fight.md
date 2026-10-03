# Did the Roshan Team Win the Next Fight?

**Question.** After a team kills Roshan, does it win the next fight, and how
long does that fight take to arrive?

## The facts

- `match.roshans`: each kill's tick and the killing team (`killer_team`).
- `match.aegis_events`: who picked up, stole or denied each Aegis.
- `match.fights`: every fight with its first-death tick and its `winner`, the
  team with more kills in it (`"draw"` when even).
- `match.game_clock`: in-game seconds between two ticks, pauses excluded.

The next fight is the first one whose first death comes after the kill and
within five in-game minutes, the Aegis's lifetime. A fight later than that is
not about this Roshan.

## The recipe

<<< @/examples/cookbook/roshan_next_fight.py{python}

## On one match

`python examples/cookbook/roshan_next_fight.py 8974053011.dem`:

```text
 roshan  time killed_by  aegis aegis_by  next_fight  seconds_to_fight fight_winner  killer_team_won
      1 17:06      dire denied   huskar          17                71         dire             True
      2 27:35      dire pickup   huskar          25                51         dire             True
```

Dire took both Roshans and won the fight that followed each, 71 and 51 seconds
later. The first Aegis was denied rather than picked up.

## Across the fixtures

Over the 9 fixture replays (31 Roshans in 8 of them):

- 28 of 31 Roshans had a fight within five minutes, a median of 51 s after the
  kill;
- 24 of those fights had a winner, and the Roshan team won 15.

## What this does not say

- **Cause.** A won fight after Roshan does not mean Roshan won it.
- **Fights already under way.** A fight whose first death came before the kill
  (often the fight at the pit) is not the "next" fight.
- **Winner.** `winner` compares kill counts; it ignores buildings, gold and who
  held the Aegis.

## Variations

- Change `WINDOW_S` to look further ahead.
- To follow the Aegis to the end (consumed, expired, denied), use the lifecycle
  facts on `gem.build_rosh_conversions(match)`: `holder_name`,
  `aegis_pickup_tick`, `aegis_fate` and `aegis_end_tick`.
- For buildings taken after the kill, filter `match.towers` and
  `match.barracks` by tick and `killer_team`.
