# Time-Series & DataFrames

gem samples entity state during parsing and assembles per-minute advantage curves,
position logs, player snapshots, and event tables. This guide shows how to use those
outputs from the high-level API and, when needed, from the lower-level extractor API.

## Per-minute advantage curves

`match.radiant_gold_adv` and `match.radiant_xp_adv` are lists of integers, one entry per
game minute. Positive values favor Radiant; negative values favor Dire.

```python
import gem

match = gem.parse("my_replay.dem")

print("Minute  Gold adv  XP adv")
for minute, (gold, xp) in enumerate(zip(match.radiant_gold_adv, match.radiant_xp_adv)):
    gold_sign = "+" if gold >= 0 else ""
    xp_sign = "+" if xp >= 0 else ""
    print(f"{minute:>6}  {gold_sign}{gold:>8,}  {xp_sign}{xp:>7,}")
```

The advantage curves use total earned gold and XP, not current spendable gold or current
level XP:

| Field | Entity | Behavior |
|---|---|---|
| `m_iTotalEarnedGold` | `CDOTA_DataRadiant/Dire` | Monotonic; use for gold advantage |
| `m_iTotalEarnedXP` | `CDOTA_DataRadiant/Dire` | Monotonic; use for XP advantage |
| `m_iGold` | `CDOTAPlayerController` | Spendable cash; drops when items are bought |
| `m_iCurrentXP` | Hero entity | Resets to 0 on level-up |

## DataFrame export

`gem.parse_to_dataframe()` returns a dict of pandas DataFrames:

```python
import gem

frames = gem.parse_to_dataframe("my_replay.dem")

print(sorted(frames))
players = frames["players"]
combat = frames["combat_log"]
```

Available DataFrames:

| Key | Contents |
|---|---|
| `players` | Per-player sampled state with terminal scalar stats repeated on each row |
| `players_minute` | Per-player series resampled to one row per game minute |
| `positions` | Per-player world `(x, y)` positions over time |
| `combat_log` | Raw normalized combat log entries |
| `wards` | Ward placement events with coordinates |
| `objectives` | Typed Gem objective rows such as towers, barracks, Roshan, tormentors, couriers |
| `opendota_objectives` | OpenDota-shaped unified objective timeline |
| `chat` | Chat messages |
| `match` | Single-row match metadata and final status bitmasks |
| `radiant_advantage` | Radiant gold/XP advantage per minute |
| `draft` | Pick and ban events |
| `teamfights` | Gem teamfight windows with participant stats |
| `opendota_teamfights` | OpenDota-compatible 3+ death temporal teamfight windows |
| `smoke_events` | Smoke of Deceit usages and grouped heroes |
| `vision_modifiers` | Vision/reveal modifier windows used by vision analysis |
| `courier_snapshots` | Courier state over time |
| `neutral_item_finds` | Neutral item find events from `DOTA_UM_FoundNeutralItem` |
| `player_kills_log` | Per-player kill log rows |
| `player_purchase_log` | Per-player purchase log rows |
| `player_runes_log` | Per-player rune pickup log rows |
| `player_buyback_log` | Per-player buyback log rows |

### Players table

```python
df = frames["players"]

print(df[["player_id", "hero_name", "tick", "gold", "net_worth", "lh", "dn"]].head())
```

The `players` table contains sampled state rows. End-of-game scalars such as
`final_net_worth`, `final_last_hits`, `kills`, `deaths`, `assists`, `hero_damage`, and
`lane_role` are repeated on each sampled row for convenient grouping.

### Positions table

```python
positions = frames["positions"]
axe_positions = positions[positions["hero_name"] == "npc_dota_hero_axe"]

print(axe_positions[["tick", "x", "y"]].head())
```

Positions are split into a dedicated table so movement-heavy analysis does not bloat the
main player-state table.

## Plot gold advantage

```python
import matplotlib.pyplot as plt
import gem

match = gem.parse("my_replay.dem")

minutes = list(range(len(match.radiant_gold_adv)))
gold_adv = match.radiant_gold_adv

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(minutes, gold_adv)
ax.axhline(0, color="gray", linewidth=0.8)
ax.set_xlabel("Game minute")
ax.set_ylabel("Radiant gold advantage")
fig.tight_layout()
fig.savefig("gold_adv.png", dpi=150)
```

## Low-level player sampling

When you need a custom sampling interval, attach `PlayerExtractor` directly to a
`ReplayParser`:

```python
from gem.extractors.players import PlayerExtractor
from gem.parser import ReplayParser

parser = ReplayParser("my_replay.dem")
players = PlayerExtractor(sample_interval=150)  # every 150 ticks, roughly 5 seconds
players.attach(parser)

parser.parse()

series = players.time_series(player_id=0)

print(series.ticks[:5])
print(series.gold_t[:5])
print(series.x_t[:5])
print(series.y_t[:5])
```

`PlayerTimeSeries` fields include `player_id`, `ticks`, `gold_t`,
`total_earned_gold_t`, `total_earned_xp_t`, `net_worth_t`, `lh_t`, `dn_t`, `xp_t`,
`hp_t`, `mana_t`, `x_t`, `y_t`, `total_hero_damage_t`, `total_hero_healing_t`,
`total_deaths_t`, and `total_stuns_t`.

For most analysis code, prefer `gem.parse()` or `gem.parse_to_dataframe()` and use the
lower-level extractor only when you need a different sampling interval or custom parser
callbacks.
