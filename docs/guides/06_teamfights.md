# Teamfight Detection

gem exposes two teamfight views:

- `match.teamfights` - Gem's richer fight windows, including spatial separation for
  simultaneous fights when position data is available.
- `match.opendota_teamfights` - OpenDota-compatible temporal windows with the 3+ death
  filter already applied.

Use `match.teamfights` for exploratory analysis and report UI. Use
`match.opendota_teamfights` when you want OpenDota-shaped output.

## Gem teamfights

Gem detects a fight by:

1. Scanning hero death events in the combat log.
2. Opening a 15-second window around each death.
3. Merging windows that share deaths or continuing combat.
4. Splitting simultaneous skirmishes in different map areas when position data is
   available.

```python
import gem

match = gem.parse("my_replay.dem")

for fight in match.teamfights:
    duration = (fight.end_tick - fight.start_tick) / 30
    print(
        f"Fight at tick {fight.start_tick:,}-{fight.end_tick:,} "
        f"({duration:.0f}s), "
        f"{fight.deaths} deaths, "
        f"winner: {fight.winner}, "
        f"kills {fight.radiant_kills}-{fight.dire_kills}"
    )
```

### Teamfight fields

```python
fight.start_tick       # int: padded window open tick
fight.end_tick         # int: padded window close tick
fight.first_death_tick # int: first hero death in the fight
fight.last_death_tick  # int: final hero death in the fight
fight.deaths           # int: total hero deaths in the window
fight.radiant_kills    # int: hero kills scored by Radiant
fight.dire_kills       # int: hero kills scored by Dire
fight.winner           # "radiant", "dire", "draw", or "unknown"
fight.centroid_x       # float | None: mean X of positioned deaths
fight.centroid_y       # float | None: mean Y of positioned deaths
fight.players          # list[TeamfightPlayer], one per slot
```

### Participant stats

```python
for player in fight.players:
    print(player.player_id)
    print(player.deaths)
    print(player.damage_dealt)
    print(player.damage_taken)
    print(player.healing)
    print(player.buybacks)
    print(player.gold_delta)
    print(player.xp_delta)
    print(player.ability_uses)
    print(player.item_uses)
```

A hero is an active participant when they died, dealt hero damage, took hero damage,
healed an allied hero, bought back, or used abilities/items in the fight window.

## OpenDota-compatible teamfights

OpenDota opens a fight at `first_death_time - 15`, extends it while hero deaths continue
inside the 15-second cooldown, and keeps only windows with at least three hero deaths.
gem stores that compatibility projection on `match.opendota_teamfights`.

```python
for fight in match.opendota_teamfights:
    print(f"{fight.start}s-{fight.end}s: {fight.deaths} deaths")

    for slot, player in enumerate(fight.players):
        if player.deaths or player.damage or player.healing or player.buybacks:
            print(slot, player.deaths, player.damage, player.healing)
```

OpenDota-compatible fight times are game-relative seconds. The per-player rows mirror
OpenDota's `teamfights[].players[]` shape with fields such as `deaths`, `buybacks`,
`damage`, `healing`, `gold_delta`, `xp_delta`, `ability_uses`, `item_uses`, and `killed`.

## Finding fight context

Use `gem.teamfight_at_tick()` when you have another event, such as a combat log entry,
and want to know whether it happened inside a Gem teamfight window:

```python
fight = gem.teamfight_at_tick(match, entry.tick)

if fight:
    print(f"Event happened during a {fight.deaths}-death fight")
```

Use `gem.heroes_near()` to find heroes near a fight centroid at the start of the fight:

```python
if fight and fight.centroid_x is not None and fight.centroid_y is not None:
    nearby = gem.heroes_near(
        match,
        fight.start_tick,
        fight.centroid_x,
        fight.centroid_y,
        radius=2000,
    )

    for player in nearby:
        print(player.hero_name)
```

## Reports

The HTML report builder uses the teamfight data for minimaps, timelines, participant
tables, and combat-log drilldowns. See [Match Reports](../reports/index.md) for report
generation and asset-cache setup.

## Implementation

Source: `src/gem/extractors/teamfights.py`

- `detect_teamfights(...)` builds Gem's richer fight windows.
- `detect_opendota_teamfights(...)` builds the OpenDota-compatible projection.
