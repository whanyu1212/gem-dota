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
match.radiant_win          # bool | None
match.game_mode            # int: game mode enum
match.leagueid             # int: league ID (0 for non-league)

match.game_start_tick      # int | None: tick when creeps spawned
match.game_end_tick        # int: last tick observed by the parser

match.radiant_gold_adv     # list[int]: per-minute Radiant gold advantage
match.radiant_xp_adv       # list[int]: per-minute Radiant XP advantage
```

### Team identity (league/tournament games)

For league games, team names, tags, and IDs are extracted from `CDOTATeam` entities in the
replay. These are empty/zero for pub games.

```python
match.radiant_team_id      # int: tournament team ID (e.g. 8261500 for Xtreme Gaming)
match.radiant_team_name    # str: team name (e.g. "Xtreme Gaming")
match.radiant_team_tag     # str: team tag (e.g. "XG")
match.dire_team_id         # int: tournament team ID
match.dire_team_name       # str: team name
match.dire_team_tag        # str: team tag

# Team IDs match the OpenDota /teams/{id} URL
# e.g. https://www.opendota.com/teams/8261500
```

---

## Players

`match.players` is a list of 10 `ParsedPlayer` objects, one per player slot in Valve's
ordering (slots 0–4 = Radiant, 5–9 = Dire).

```python
for player in match.players:
    print(player.hero_name)     # "npc_dota_hero_axe"
    print(player.player_id)     # 0–9
    print(player.player_name)   # Steam persona name, e.g. "Ame"
    print(player.team)          # 2 = Radiant, 3 = Dire
    print(player.steam_id)      # 64-bit Steam ID, e.g. 76561198859019881
    print(player.account_id)    # 32-bit account ID, e.g. 898754153

# account_id matches the OpenDota/Dotabuff player URL
# e.g. https://www.opendota.com/players/898754153
```

### Looking up a player by hero name

Instead of iterating `match.players` manually, use `gem.find_player()`:

```python
import gem

match = gem.parse("my_replay.dem")

# All of these are equivalent:
axe = gem.find_player(match, "Axe")               # display name
axe = gem.find_player(match, "axe")               # case-insensitive
axe = gem.find_player(match, "npc_dota_hero_axe") # full NPC name
am  = gem.find_player(match, "Anti-Mage")         # hyphenated display name
am  = gem.find_player(match, "anti mage")         # spaced variant

if axe:
    print(f"Axe: {axe.kills}/{axe.deaths}/{axe.assists}")
```

Returns `None` if the hero was not in the match.  For the reverse lookup
(display name → NPC name) without a match object, use
`gem.constants.hero_npc_name()`:

```python
from gem.constants import hero_npc_name

hero_npc_name("Anti-Mage")   # → "npc_dota_hero_antimage"
hero_npc_name("Shadow Fiend") # → "npc_dota_hero_nevermore"
hero_npc_name("unknown")      # → None
```

---

### Per-player aggregate stats

```python
player.kills           # int: kills attributed (summons credited to owner)
player.deaths          # int: deaths from any cause (hero, tower, creep, neutral)
player.assists         # int

player.stuns_dealt     # float: total stun seconds dealt to enemy heroes

# Net worth / gold / XP are time-series (sampled every tick or per minute)
player.net_worth_t_min[-1]          # int: net worth at game end (last minute sample)
player.total_earned_gold_t_min[-1]  # int: cumulative gold at game end
player.lh_t_min[-1]                 # int: last-hit count at game end
player.dn_t_min[-1]                 # int: deny count at game end

# Total damage dealt / received — dicts keyed by target/attacker NPC name
player.damage            # dict[str, int]: damage dealt per target
player.damage_taken      # dict[str, int]: damage received per attacker
sum(player.damage.values())       # total damage dealt across all targets

player.damage_by_type        # dict[str, int]: damage dealt keyed by "physical"/"magical"/"pure"/"others"
player.damage_taken_by_type  # dict[str, int]: damage received keyed by damage type
```

### Time-series logs

```python
player.purchase_log    # list[{"tick": int, "key": str}]: item purchases in order
player.buyback_log     # list[{"tick": int, "cost": int}]: buyback events
player.runes_log       # list[{"tick": int, "type": int}]: rune pickups

player.lane_pos        # dict[str, int]: grid cell → visit count (first 10 minutes)

player.lane_role           # int: 1=safe, 2=mid, 3=off, 4=jungle, 5=roaming, 0=unknown
player.lane_last_hits      # int: last-hit count at the 10-minute mark
player.lane_denies         # int: deny count at the 10-minute mark
player.lane_total_gold     # int: cumulative total earned gold at the 10-minute mark
player.lane_total_xp       # int: cumulative total earned XP at the 10-minute mark
player.lane_efficiency_pct # int: floor(lane_total_gold / 4948 × 100); can exceed 100
player.lane_gold_adv       # int | None: gold vs lane opponents at 10 min (None for jungle/roaming)
player.lane_xp_adv         # int | None: XP vs lane opponents at 10 min (None for jungle/roaming)
```

`lane_pos` is restricted to the first 10 game-minutes (OpenDota convention). `lane_role` is
inferred by aggregating `lane_pos` into coarse lane zones — see
[Lane Classification](#lane-classification) below.

---

## Lane classification

`lane_role` is inferred from each hero's position heatmap over the first 10 game-minutes.
gem aggregates the `lane_pos` heatmap into coarse lane zones and assigns the role of
whichever zone dominated the hero's time.

| `lane_role` | Label | Description |
|---|---|---|
| 1 | Safe lane | Radiant bottom / Dire top |
| 2 | Mid lane | Diagonal corridor |
| 3 | Off lane | Radiant top / Dire bottom |
| 4 | Jungle | Interior camps, off lane corridors |
| 5 | Roaming | No dominant zone (spread across map) |
| 0 | Unknown | Insufficient position data |

```python
LANE_NAMES = {1: "Safe", 2: "Mid", 3: "Off", 4: "Jungle", 5: "Roaming", 0: "Unknown"}

for player in match.players:
    from gem.constants import hero_display
    print(
        f"{hero_display(player.hero_name):<20}"
        f"  lane: {LANE_NAMES[player.lane_role]:<8}"
        f"  LH@10: {player.lane_last_hits:>3}"
        f"  gold@10: {player.lane_total_gold:>6,}"
    )
```

The safe/off assignment is team-aware: Radiant safe lane is the bottom-right of the map,
Dire safe lane is the top-left.  See [Laning Analysis](08_laning.md) for a full explanation
of the zone-aggregation algorithm, the lane efficiency formula, and gold/XP advantage
computation.

---

## Damage type breakdown

```python
player.damage_by_type        # {"physical": int, "magical": int, "pure": int, "others": int}
player.damage_taken_by_type  # same keys
```

These are populated from the `damage_type` field on `DAMAGE` combat log entries. The
`"others"` bucket covers damage to non-hero units (creeps, wards, zombies) where Valve
does not populate the type field.

```python
for player in match.players:
    d = player.damage_by_type
    total = sum(d.values())
    if total:
        phys_pct = 100 * d.get("physical", 0) / total
        mag_pct  = 100 * d.get("magical",  0) / total
        pure_pct = 100 * d.get("pure",     0) / total
        print(f"{hero_display(player.hero_name)}: "
              f"phys {phys_pct:.0f}%  mag {mag_pct:.0f}%  pure {pure_pct:.0f}%")
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
        f"tick {ward.tick:,}: "
        f"{ward.placer} places {ward.ward_type} ward "
        f"at ({ward.x:.0f}, {ward.y:.0f})"
    )
```

`WardEvent` fields: `tick`, `placer`, `ward_type` (`"observer"` or `"sentry"`),
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
print(f"Winner: {result}")
print(f"Duration: {match.duration_minutes:.1f} min")
print()

for player in match.players:
    hero = hero_display(player.hero_name)
    team = "R" if player.team == 2 else "D"
    nw = player.net_worth_t_min[-1] if player.net_worth_t_min else 0
    dmg = sum(player.damage.values())
    print(
        f"[{team}] {hero:<20}"
        f"  {player.kills}/{player.deaths}/{player.assists}"
        f"  {nw:>7,} NW"
        f"  {dmg:>8,} dmg"
    )
```
