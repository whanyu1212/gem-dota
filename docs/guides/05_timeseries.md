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

`PlayerTimeSeries` fields: `ticks`, `gold_t`, `xp_t`, `hp_t`, `mana_t`, `lh_t`,
`dn_t`, `x_t`, `y_t`, `level_t`.

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
| `"players"` | Per-player snapshot time series (one row per player per tick) |
| `"wards"` | Ward placement events with coordinates |
| `"objectives"` | Tower kills, barracks, Roshan kills |
| `"teamfights"` | Teamfight windows with participant stats |
| `"combat_log"` | Raw combat log entries |

### Players DataFrame

```python
df = frames["players"]

print(df.dtypes)
# tick          int64
# hero          object
# gold          int64
# xp            int64
# hp            int64
# mana          float64
# lh            int64
# dn            int64
# x             float64
# y             float64
# level         int64

# Filter to one hero
axe_df = df[df["hero"] == "CDOTA_Unit_Hero_Axe"]
print(axe_df[["tick", "gold", "xp", "hp"]].head(10))
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

`examples/movement_heatmap.py` builds an interactive Plotly heatmap showing hero
positions, ability levels, and stun dealt over time. It demonstrates the full
time-series pipeline:

```bash
python examples/movement_heatmap.py my_replay.dem
# Opens a browser window with the heatmap
```
