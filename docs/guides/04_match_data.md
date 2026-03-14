# Full Match Data

`gem.parse()` returns a `ParsedMatch` object containing everything extracted from the
replay. This guide walks through the fields.

---

## Parsing a replay

```python
import gem

match = gem.parse("my_replay.dem")
```

`gem.parse()` runs the complete pipeline: entity parsing, combat log, game events, all
extractors. A typical 45-minute replay takes 2–4 seconds.

---

## Match-level fields

```python
match.match_id             # int: Valve match ID
match.duration_seconds     # float: game duration in seconds
match.duration_minutes     # float: convenience property
match.radiant_win          # bool
match.game_mode            # int: game mode enum
match.lobby_type           # int: lobby type enum
match.cluster              # int: server cluster ID
match.game_build           # int: Dota 2 build number extracted from svc_ServerInfo

match.radiant_score        # int: Radiant kill count at game end
match.dire_score           # int: Dire kill count at game end

match.radiant_gold_adv     # list[int]: per-minute Radiant gold advantage
match.radiant_xp_adv       # list[int]: per-minute Radiant XP advantage
```

---

## Players

`match.players` is a list of 10 `ParsedPlayer` objects, one per player slot in Valve's
ordering (slots 0–4 = Radiant, 5–9 = Dire).

```python
for player in match.players:
    print(player.hero_name)     # "CDOTA_Unit_Hero_Axe"
    print(player.player_slot)   # 0–9
    print(player.team)          # 2 = Radiant, 3 = Dire
```

### Per-player aggregate stats

```python
player.kills           # int: kills attributed (summons credited to owner)
player.deaths          # int: deaths from any cause (hero, tower, creep, neutral)
player.assists         # int

player.last_hits       # int: creep last hits at game end
player.denies          # int

player.net_worth       # int: total earned gold at game end
player.gold_per_min    # int
player.xp_per_min      # int

player.hero_damage      # int: total hero-to-hero damage dealt
player.tower_damage     # int
player.hero_healing     # int: healing dealt to allied heroes

player.level           # int: hero level at game end
player.stuns_dealt     # float: total stun seconds dealt to enemy heroes
```

### Items and abilities

```python
player.item_builds     # list[str]: final inventory item names
player.ability_upgrades  # list[dict]: each entry {"tick": int, "ability": str, "level": int}
```

### Time-series logs

```python
player.purchase_log    # list[{"tick": int, "key": str}]: item purchases in order
player.buyback_log     # list[{"tick": int, "cost": int}]: buyback events
player.runes_log       # list[{"tick": int, "type": int}]: rune pickups

player.lane_pos        # dict[str, int]: grid cell → visit count (first 10 minutes)
```

---

## Draft

`match.draft` is a list of `DraftEvent` objects in chronological order:

```python
for event in match.draft:
    team   = "Radiant" if event.team == 2 else "Dire"
    action = "picks" if event.is_pick else "bans"
    print(f"  {team} {action} {event.hero_name}")
```

`DraftEvent` fields: `tick`, `team`, `hero_name`, `is_pick`, `order`.

---

## Wards

`match.wards` is a list of `WardEvent` objects:

```python
for ward in match.wards:
    print(
        f"tick {ward.placed_tick:,}: "
        f"{ward.placed_by} places {ward.ward_type} ward "
        f"at ({ward.x:.0f}, {ward.y:.0f})"
    )
```

`WardEvent` fields: `placed_tick`, `placed_by`, `ward_type` (`"observer"` or `"sentry"`),
`x`, `y`, `killed_tick` (or `None`), `expires_tick` (or `None`).

---

## Objectives

### Tower kills

```python
match.tower_kills   # list[dict]: tower kill events
# Each: {"tick": int, "team": int, "building": str, "attacker": str}
```

### Roshan kills

```python
match.roshans   # list[dict]: each Roshan kill event
# Each: {"tick": int, "killer_team": int, "killer_slot": int}
```

### Barracks

```python
match.barracks_kills  # list[dict]: barracks destruction events
```

---

## Aegis events

```python
match.aegis_events   # list[AegisEvent]
# AegisEvent fields: tick, event_type ("pickup"/"deny"/"steal"), player_slot
```

---

## Chat

```python
match.chat   # list[ChatMessage]
# ChatMessage fields: tick, player_slot, text, channel
```

---

## Teamfights

```python
match.teamfights   # list[Teamfight]
```

See [Teamfight Detection](06_teamfights.md) for a full walkthrough.

---

## Example: print a match summary

```python
import gem
from gem.constants import hero_display

match = gem.parse("my_replay.dem")

result = "Radiant" if match.radiant_win else "Dire"
print(f"Winner: {result}  ({match.radiant_score}–{match.dire_score})")
print(f"Duration: {match.duration_minutes:.1f} min")
print()

for player in match.players:
    hero = hero_display(player.hero_name)
    team = "R" if player.team == 2 else "D"
    print(
        f"[{team}] {hero:<20}"
        f"  {player.kills}/{player.deaths}/{player.assists}"
        f"  {player.net_worth:>7,} NW"
        f"  {player.hero_damage:>8,} dmg"
    )
```
