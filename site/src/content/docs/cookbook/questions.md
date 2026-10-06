# Answering Questions from the Facts

gem reports what the replay records and leaves the interpretation to you. These
recipes show what that looks like in practice: each answers one question a
player or analyst might ask, using `gem.parse`, the facts on `ParsedMatch` and
pandas. None of them uses a tag, score or verdict, and none of them uses
anything deprecated in 0.12.

| Question | Facts it joins |
|---|---|
| [Did the Roshan team win the next fight?](./roshan-next-fight) | Roshan kills, Aegis events, fights, the game clock |
| [How fast did each core farm from 10 to 20 minutes?](./core-farm) | Minute curves, neutral deaths in the combat log, positions and `gem.region_of` |
| [How often did a smoke lead to a kill?](./smoke-to-kill) | `gem.build_smoke_analysis`, hero deaths in the combat log, fights |
| [Where did each team ward, and what could the wards see?](./wards) | Wards, `gem.region_of`, hero positions and the replay's own visibility |
| [Where were the fights, and who got the kills?](./fights) | gem's fights, buildings and Roshan kills, the game clock |
| [When did each objective fall, and did teams convert their edges?](./objectives) | Buildings, Roshan and Tormentor kills, building damage in the combat log, fights |
| [What moved the gold and XP lead?](./lead) | The gold ledger, total earned gold and XP, XP and deaths in the combat log |
| [How did each lane go?](./lanes) | Hero positions on OpenDota's lane grid, minute curves, the gold ledger, deaths and teleports in the combat log |
| [Who took each rune, and what happened while a power rune lasted?](./runes) | `match.runes`, `PICKUP_RUNE` entries, rune buffs, kills and damage in the combat log, buildings and Roshan kills |

## How the recipes are laid out

Each recipe is a short script in
[`examples/cookbook/`](https://github.com/whanyu1212/gem-dota/tree/main/examples/cookbook).
It has one function that takes a `ParsedMatch` and returns a DataFrame with
fixed columns, and a `main` that runs it on one replay or on many:

```bash
python examples/cookbook/roshan_next_fight.py match.dem
python examples/cookbook/roshan_next_fight.py replays/*.dem
```

With more than one replay, `main` parses them in parallel with
`gem.parse_many`. Its worker processes re-import the script, so code that calls
`parse_many` needs an `if __name__ == "__main__":` guard; a script piped in
through standard input cannot use it.

The functions are tested in `tests/test_cookbook.py`, both on small built
matches and on a fixture replay, so the code on these pages runs as shown.

## The sample

The outputs come from the TI match 8974053011 (MOUZ vs Natus Vincere; the wards,
fights, objectives, lead, lanes and runes recipes use 8856501050, the home page's match) and, for the totals, the 9 local
fixture replays (`tests/fixtures/opendota/`). Nine pro
matches are enough to show the method, not to draw conclusions; run the same
code over your own replays.

## Times

Replay ticks keep running during pauses, and the in-game clock does not. The
recipes measure every delay and window with the match's game clock
(`match.game_clock`), so a pause between two events is not counted.
