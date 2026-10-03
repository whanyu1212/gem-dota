# Fight Detection

gem exposes two fight views:

- `match.fights` - every fight gem detects, from a single pickoff up, with spatial
  separation for simultaneous fights when position data is available. What counts as a
  *teamfight* is up to you: filter on deaths or participants, or regroup with
  `gem.find_fights`.
- `match.opendota_teamfights` - OpenDota's teamfights exactly: temporal windows with
  OpenDota's 3+ death filter already applied.

Use `match.fights` for exploratory analysis and report UI. Use
`match.opendota_teamfights` when you want OpenDota-shaped output.

`match.fights` was called `match.teamfights` in gem 0.10 and earlier. gem 0.11
renamed it and gem 0.13 removed the old names (`match.teamfights`, `Teamfight`,
`teamfight_at_tick`, the `teamfights` DataFrame table, …). JSON files written
with the old `teamfights` key still load.

## Gem fights

Gem detects a fight by:

1. Scanning hero death events in the combat log.
2. Opening a 15-second window around each death.
3. Merging windows that share deaths or continuing combat.
4. Splitting simultaneous skirmishes more than 3,000 world units apart when position
   data is available.

No minimum is applied, so most fights have one or two deaths. Keep the ones you
consider teamfights:

```python
teamfights = [
    fight
    for fight in match.fights
    if fight.deaths >= 3
    and sum(gem.is_active_fight_participant(p) for p in fight.players) >= 6
]
```

```python
import gem

match = gem.parse("my_replay.dem")

for fight in match.fights:
    duration = (fight.end_tick - fight.start_tick) / 30
    print(
        f"Fight at tick {fight.start_tick:,}-{fight.end_tick:,} "
        f"({duration:.0f}s), "
        f"{fight.deaths} deaths, "
        f"winner: {fight.winner}, "
        f"kills {fight.radiant_kills}-{fight.dire_kills}"
    )
```

### Fight fields

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
fight.players          # list[FightPlayer], one per slot
```

### Regrouping fights

Filtering can only drop fights; it cannot merge two fights the default grouping split.
`gem.find_fights` regroups a parsed (or `gem.load_json`-loaded) match with your own
window and radius, without parsing the replay again:

```python
# Group by time only, as OpenDota does: simultaneous fights anywhere become one.
by_time = gem.find_fights(match, radius=None)

# Wider areas, a shorter cooldown.
wide = gem.find_fights(match, window_s=10, radius=5000)
```

`window_s` is how long after a fight's last death a new death still joins it (it also
pads the fight's start and end); `radius` is the largest distance between a death and
the fight's centre. The radius also decides whose damage, healing, gold and ability uses
count for a fight. With the defaults (`window_s=15`, `radius=3000`), `find_fights`
returns exactly `match.fights`.

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
or healed an allied hero in the fight window. Buybacks, ability uses, and item uses
remain available as fight statistics, but do not by themselves establish direct
combat participation.

## Evidence-first positioning snapshots

Use `gem.build_fight_positioning(match)` to obtain four deterministic
spatial views for every Gem fight:

```python
for positioning in gem.build_fight_positioning(match):
    for snapshot in positioning.snapshots:
        print(snapshot.kind.value, snapshot.tick)
        print(snapshot.radiant.completeness.value)
        print(snapshot.dire.completeness.value)

        for hero in snapshot.heroes:
            print(
                hero.hero_name,
                hero.active_participant,
                hero.x,
                hero.y,
                hero.sample_tick,
                hero.sample_age_ticks,
                hero.visibility.value,
            )
```

The requested moment tick and the sampled position tick are intentionally
separate. By default, a position older than 60 ticks is treated as unavailable,
although its sample tick and age remain in the result. Team spread is RMS
distance from the fresh-position centroid. Opposing-team visibility is the
authoritative canonical-hero state and is never replaced by a geometric guess.

See [Fight Positioning](../experimental/fight-positioning.md) for the
moment definitions, geometry formulas, smoke/reveal boundaries, and report UI.

## Linking smoke operations to fights

When the question begins with a Smoke of Deceit activation rather than a fight
window, each `SmokeAnalysis` from `gem.build_smoke_analysis(match)` names its
`first_fight`: the first fight whose first death came within 60 in-game seconds
of the smoke.

```python
for smoke in gem.build_smoke_analysis(match):
    if smoke.first_fight is not None:
        print(smoke.activation_tick, match.fights.index(smoke.first_fight), smoke.first_fight.winner)
```

See [Smoke Analysis](../experimental/smoke-analysis.md) and the
[smoke recipe](../cookbook/smoke-to-kill.md).

## OpenDota-compatible teamfights

OpenDota opens a fight at `first_death_time - 15`, extends it while hero deaths continue
inside the 15-second cooldown, and keeps only windows with at least three hero deaths.
gem stores that compatibility projection on `match.opendota_teamfights`, and it equals
OpenDota's `teamfights` on every local fixture. That includes OpenDota's quirks:

- A fight closes at OpenDota's first once-a-second interval 15 s or more after its last
  death. A fight still open when the recording ends never closes, so the game's final
  fight is usually missing. `match.fights` keeps it.
- The Aegis holder's next death is skipped. OpenDota forgets the holder only when
  `modifier_aegis_regen` (the buff an unused Aegis gives as it expires) appears, so a
  holder whose Aegis ran out without it loses their next real death too.
- A death adds to `deaths` and `deaths_pos` only when the victim has an interval read in
  that second. `deaths_pos` uses OpenDota's map cells (world units / 128), and
  `xp_start` / `xp_end` are the interval XP at exactly the fight's first and last second.

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

Use `gem.fight_at_tick()` when you have another event, such as a combat log entry,
and want to know whether it happened inside a Gem fight window:

```python
fight = gem.fight_at_tick(match, entry.tick)

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

The HTML report builder uses the fight data for minimaps, timelines, participant
tables, and combat-log drilldowns. See [Match Reports](../reports/index.md) for report
generation and asset-cache setup.

## Implementation

Source: `src/gem/extractors/fights.py`

- `detect_fights(...)` builds Gem's fight windows (`window_s`, `radius`);
  `gem.find_fights(match, ...)` calls it on a parsed match.
- `detect_opendota_teamfights(...)` builds the OpenDota-compatible projection.
