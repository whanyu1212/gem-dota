# Time-Series & DataFrames

gem samples entity state at regular intervals and assembles per-minute advantage curves.
This guide shows how to work with the time-series data and export it to pandas.

---

## Per-minute advantage curves

`match.radiant_gold_adv` and `match.radiant_xp_adv` are lists of integers, one entry
per game minute. Positive values favour Radiant, negative values favour Dire.

```python
import gem

match = gem.parse("my_replay.dem")

print("Minute  Gold adv  XP adv")
for minute, (gold, xp) in enumerate(
    zip(match.radiant_gold_adv, match.radiant_xp_adv)
):
    sign = "+" if gold >= 0 else ""
    print(f"  {minute:2d}    {sign}{gold:>7,}   {sign}{xp:>7,}")
```

### Important: field sources

The advantage curves use **total earned** gold and XP (monotonically increasing counters),
not current gold/XP (which reset when items are purchased or levels are gained):

| Field | Entity | Behaviour |
|---|---|---|
| `m_iTotalEarnedGold` | `CDOTA_DataRadiant/Dire` | Monotonically increasing — use for advantages |
| `m_iTotalEarnedXP` | `CDOTA_DataRadiant/Dire` | Monotonically increasing — use for advantages |
| `m_iGold` | `CDOTAPlayerController` | Spendable cash — drops when items bought |
| `m_iCurrentXP` | Hero entity | Resets to 0 on each level-up |

---

## Player time series (low-level API)

When you need finer-grained time series data than the per-minute arrays, attach a
`PlayerExtractor` directly:

```python
from gem.parser import ReplayParser
from gem.extractors.players import PlayerExtractor

ext = PlayerExtractor(sample_interval=150)  # sample every 150 ticks = 5 seconds

parser = ReplayParser("my_replay.dem")
parser.attach(ext)
parser.parse()

# Get time series for player 0
ts = ext.time_series(player_id=0)

print(ts.ticks[:5])    # [0, 150, 300, 450, 600]
print(ts.gold_t[:5])   # spendable gold at each sample tick
print(ts.xp_t[:5])     # current XP at each sample tick
print(ts.hp_t[:5])     # HP at each sample tick
print(ts.x_t[:5])      # world X position at each sample tick
```

`PlayerTimeSeries` fields: `player_id`, `ticks`, `gold_t`, `total_earned_gold_t`,
`total_earned_xp_t`, `net_worth_t`, `lh_t`, `dn_t`, `xp_t`, `hp_t`, `mana_t`, `x_t`,
`y_t`, `total_hero_damage_t`, `total_hero_healing_t`, `total_deaths_t`, `total_stuns_t`.

---

## DataFrame export

`gem.parse_to_dataframe()` returns a dict of pandas DataFrames:

```python
import gem

frames = gem.parse_to_dataframe("my_replay.dem")
```

Available DataFrames:

| Key | Contents |
|---|---|
| `"players"` | Per-player snapshot time series (one row per player per sampled tick) |
| `"players_minute"` | Per-player series resampled to one row per game minute |
| `"positions"` | Per-player world `(x, y)` positions over time |
| `"wards"` | Ward placement events with coordinates |
| `"objectives"` | Tower kills, barracks, Roshan kills |
| `"teamfights"` | Teamfight windows with participant stats |
| `"combat_log"` | Raw combat log entries |
| `"chat"` | All chat messages |
| `"draft"` | Pick / ban events |
| `"smoke_events"` | Smoke of Deceit usages and their groups |
| `"courier_snapshots"` | Courier state over time |
| `"radiant_advantage"` | Radiant gold/XP advantage per minute |
| `"match"` | Single-row match-level summary |
| `"neutral_item_finds"` | Neutral item find events with item/enhancement IDs and keys |

### Players DataFrame

```python
df = frames["players"]

print(df.dtypes)
# player_id            int64
# player_name         object
# hero_name           object
# team                 int64
# tick                 int64
# gold                 int64
# total_earned_gold    int64
# net_worth            int64
# lh                   int64
# dn                   int64
# xp                   int64
# kills                int64
# ...                        # plus per-player scalar columns (kda, hero_damage, ...)

# Filter to one hero (hero_name is the NPC name)
axe_df = df[df["hero_name"] == "npc_dota_hero_axe"]
print(axe_df[["tick", "gold", "xp", "net_worth"]].head(10))
```

World positions live in the separate `positions` DataFrame (`tick`, `x`, `y` per player):

```python
pos = frames["positions"]
axe_pos = pos[pos["hero_name"] == "npc_dota_hero_axe"]
print(axe_pos[["tick", "x", "y"]].head(10))
```

---

## Plotting gold advantage with pandas + matplotlib

```python
import gem
import pandas as pd
import matplotlib.pyplot as plt

match = gem.parse("my_replay.dem")

minutes = list(range(len(match.radiant_gold_adv)))
adv = match.radiant_gold_adv

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(minutes, adv, color="green" if adv[-1] > 0 else "red")
ax.axhline(0, color="gray", linewidth=0.8)
ax.fill_between(minutes, adv, 0,
                where=[v > 0 for v in adv], alpha=0.2, color="green", label="Radiant ahead")
ax.fill_between(minutes, adv, 0,
                where=[v < 0 for v in adv], alpha=0.2, color="red",   label="Dire ahead")
ax.set_xlabel("Game minute")
ax.set_ylabel("Gold advantage")
ax.set_title("Radiant gold advantage over time")
ax.legend()
plt.tight_layout()
plt.savefig("gold_adv.png", dpi=150)
```

---

## Full interactive example

The Movement tab in `examples/match_report.py` builds an interactive Plotly heatmap showing hero
positions, ability levels, and stun dealt over time. It demonstrates the full
time-series pipeline:

```bash
python examples/match_report.py my_replay.dem
# Opens a browser window with the report (includes movement heatmap tab)
```
