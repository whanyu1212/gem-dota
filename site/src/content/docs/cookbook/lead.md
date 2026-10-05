# What Moved the Gold and XP Lead?

**Question.** Over a match, or any stretch of it, where did each team's gold
and XP come from, and which sources moved the lead?

::: figure lead
**Figure 1.** Radiant's gold lead in match 8856501050 at every minute and at
the end of the game, with the fights and objectives under it. Below the curve,
what moved the lead over the match by source, each hero's gold, and the
minutes the lead changed hands. Switch to the XP lead, or drag on the curve to
pick a stretch, and everything below redraws for it. A fight's dot opens it on
the [fights page](./fights).
:::

## The facts

- `ParsedPlayer.gold_ledger`: the game's running totals of each player's
  earned gold by source, read every game minute and at the end of the game.
- `ParsedPlayer.total_earned_gold_t_min` and `total_earned_gold_t`: each
  player's total earned gold (`m_iTotalEarnedGold`). Radiant's minus Dire's is
  the gold lead, `match.radiant_gold_adv`.
- `ParsedPlayer.total_earned_xp_t_min` and `total_earned_xp_t`: the same for
  XP, and `match.radiant_xp_adv`.
- `match.combat_log`: every XP entry, with the hero, the amount and its reason,
  and every unit's death.

## How the lead splits

A player's ledger sources add up to the player's total earned gold, so the gold
lead splits into its sources exactly: hero kills and assists, lane creeps,
neutral creeps, buildings, Roshan, bounty runes, passive income, and the rest
(wards, couriers, abilities, denies). On the fixtures the hero-kill gold equals
the combat log's hero-kill gold for every player, and 501 of the 525 kills
that paid it paid a hero besides the killer: it includes assists. Gold from a
source the replay has no total for is its own row, *not in the gold totals*;
the bars still add up to the lead.

The XP lead splits by the reason on each XP entry: hero kills, creeps, Roshan
and wisdom runes (every XP entry of that reason on the fixtures, 228 of 228,
came within 3 ticks of a wisdom-rune pickup). The combat log doesn't say which
creep gave the XP, so the recipe looks at the units that died on its tick:
lane creeps, neutral creeps, or summons and other units. When more than one
kind died, or none did, the XP is *creeps, kind unclear*: 5.2% of the creep XP
on the fixtures.

Neither lead counts what was spent or lost. Gold spent on items and buybacks
and gold lost on death leave earned gold as it was.

## The recipe

<<< @/examples/cookbook/lead.py{python}

## On one match

`python examples/cookbook/lead.py 8856501050.dem`:

```text
8856501050, at the end of the game (92:56). Radiant's lead:
gold -10,730, XP -38,457

Gold lead by source over the match (+ toward Radiant):
hero_kills        17184
lane_creeps        3921
neutral_creeps   -14201
buildings         -2351
roshan            -8112
bounty_runes      -9590
passive_income      299
other              2120
lead             -10730

XP lead by source over the match (+ toward Radiant):
hero_kills        -8777
lane_creeps      -13674
neutral_creeps     2867
other_units         424
unclear_creeps      -26
roshan            -6014
wisdom_runes     -15000
other              1743
lead             -38457

The gold lead changed hands at: 02:00 dire, 06:00 radiant, 07:00 dire, 08:00 radiant, 09:00 dire, 10:00 radiant, 11:00 dire, 15:00 radiant, 16:00 dire
```

Radiant won this match 10.7k gold and 38.5k XP behind. Its heroes earned 17.2k
more from hero kills and assists; Dire's earned 14.2k more from neutral
creeps, 9.6k more from bounty runes and 8.1k more from Roshan. Of Dire's XP
lead, 15k came from wisdom runes.

The end of the game is a reading of its own. At 92:00 Dire led by 20.9k; in
the 56 seconds before the end, fight 36 was fought and two Dire barracks and
both Dire tier-4 towers fell, and the lead closed by 10.2k.

## Across the fixtures

Over the 9 fixture replays, at the end of the game:

- The side ahead in gold won 8 of the 9 matches; 8856501050 is the other one.
- Buildings moved the gold lead toward the side that ended ahead in all 9,
  neutral creeps in 8 and hero kills and assists in 7.
- The gold lead changed hands between 0 and 12 times.
- The one gap in the gold totals is on 8974053011: 1,344 gold over six
  players (1,288 of it on the lead), all of it combat-log gold of reason 22,
  which the replay has no ledger field for.

## What this does not say

- **Why a source favoured a side.** The bars say where the gold came from, not
  what made it come.
- **Anything finer than a minute.** The ledger is read once a game minute and
  at the end, so a stretch starts and ends on those readings. The gold from a
  fight that crosses a minute is split between the two minutes.
- **Net worth.** Items bought and gold lost on death change net worth but not
  earned gold, so the lead here is not the net-worth difference.
- **Which creep gave the XP** when more than one kind died on the tick.

## Variations

- Pass `start_s` and `end_s` to `what_moved` for a stretch, e.g. the laning
  stage: `what_moved(lead, 0, 600)`.
- Group `gold_sources` by `hero` instead of `team` for each hero's sources over
  a stretch.
- Run it on many replays and count how often each source moved the lead
  toward the winner.
