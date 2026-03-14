# Laning Analysis

The laning phase covers roughly the first ten minutes of a Dota 2 match — the period before
heroes rotate and teamfights begin.  gem extracts two things from this window:

1. **Lane role** — which lane each hero was in (safe, mid, off, jungle, roaming)
2. **Lane metrics** — how well each hero performed during those ten minutes

---

## How lane roles are assigned

### Position heatmap (`lane_pos`)

During parsing, gem samples each hero's world coordinates at regular intervals.  Samples
taken inside the first 10 game-minutes (600 seconds × 30 ticks/s = 18 000 ticks) are
binned into a 64 × 64 world-unit grid and accumulated per cell:

```python
match = gem.parse("my_replay.dem")

hero = match.players[1]  # pick any player
print(hero.lane_pos)
# {"250_154": 38, "251_154": 22, "250_155": 17, ...}
#  ^ grid key "gx_gy"   ^ dwell count (number of samples in that cell)
```

Each key encodes the grid cell `(gx, gy)`.  To recover world coordinates:

```python
GRID = 64
for key, count in hero.lane_pos.items():
    gx, gy = map(int, key.split("_"))
    wx = gx * GRID + 32   # cell centre X
    wy = gy * GRID + 32   # cell centre Y
```

`lane_pos` is intentionally limited to the laning window.  `position_log` (full-game
movement trail) is a separate, unfiltered list.

### Zone aggregation

gem does **not** use the raw centroid to decide a lane role, because a hero moving along a
lane corridor spreads across many adjacent 64-unit cells — no single cell would account for
more than ~6 % of samples even for a hero that never left mid lane.

Instead, gem aggregates cells into five coarse **lane zones** using fixed world-coordinate
boundaries, then finds the dominant zone:

| Zone | World-coordinate rule |
|---|---|
| **Mid** | `\|wx − wy\| < 2000` and `10500 < wx < 22000` — the diagonal corridor |
| **Safe-R** | `wy < 12500` (bottom strip) or (`wx > 20000` and `wy < 16000`) (bottom-right corner) |
| **Off-R** | `wx < 12500` and `wy > 19000` (top-left corner) |
| **Jungle** | Interior region: `12500 ≤ wx ≤ 20000` and `12500 ≤ wy ≤ 19000` |
| **Other** | Everything else |

Zones are named from the **Radiant perspective**.  For Dire players the safe/off assignment
is flipped: Dire's safe lane is the top-left (Safe-R = Dire off), and Dire's off lane is
the bottom-right (Off-R = Dire safe).

### Dominant zone → lane role

Once cells are aggregated, gem picks the zone with the most dwell ticks and checks whether
it clears the dominance threshold (45 %):

```
dominant_zone_count / total_ticks ≥ 0.45  →  assign that zone's role
dominant_zone_count / total_ticks < 0.45  →  roaming (role 5)
```

The 45 % threshold mirrors OpenDota's approach — a hero whose time is split too evenly
across zones (supports rotating between lanes, roaming cores, etc.) is classified as
roaming rather than forced into a lane that doesn't describe their game.

### Role numbers

| `lane_role` | Label | Dota equivalent |
|---|---|---|
| 1 | Safe lane | Radiant bottom / Dire top |
| 2 | Mid lane | Diagonal corridor |
| 3 | Off lane | Radiant top / Dire bottom |
| 4 | Jungle | Interior camps, not on a lane |
| 5 | Roaming | No dominant zone — spreading across the map |
| 0 | Unknown | Insufficient position data |

```python
LANE_NAMES = {1: "Safe", 2: "Mid", 3: "Off", 4: "Jungle", 5: "Roaming", 0: "Unknown"}

for p in match.players:
    from gem.constants import hero_display
    print(f"{hero_display(p.hero_name):<22}  {LANE_NAMES[p.lane_role]}")
```

---

## Lane metrics

All laning metrics are computed at the **10-minute mark** (index 10 of the per-minute
time series).

### Raw stats at 10 minutes

```python
p.lane_last_hits   # int: last-hit count at 10 min
p.lane_denies      # int: deny count at 10 min
p.lane_total_gold  # int: cumulative total earned gold at 10 min
p.lane_total_xp    # int: cumulative total earned XP at 10 min
```

`lane_total_gold` and `lane_total_xp` use the **monotonically increasing** earned fields
(`m_iTotalEarnedGold`, `m_iTotalEarnedXP`) from the `CDOTA_DataRadiant/Dire` entity, not
the spendable cash balance.  This means items purchased before 10 minutes do not reduce
the number — it reflects everything a hero ever gained, not what they have left.

### Tier-1 metric: lane efficiency % (`lane_efficiency_pct`)

Lane efficiency answers the question *"what fraction of the theoretically available passive
gold did this hero capture?"*

```
lane_efficiency_pct = floor(lane_total_gold / 4948 × 100)
```

The denominator **4948** is the OpenDota baseline — the maximum passive gold a hero could
earn in 10 minutes by last-hitting every creep and picking up every passive gold tick:

| Source | Calculation | Gold |
|---|---|---|
| Melee creeps (3 / wave, 1 wave/30 s, 40 gold each) | 3 × 20 waves × 40 | 2400 |
| Ranged creeps (1 / wave, 45 gold each) | 1 × 20 waves × 45 | 900 |
| Siege creeps (1 every 5 waves, 74 gold each) | 4 waves × 74 | 148 |
| Passive gold tick (600 / min accumulated) | 600 × 1.5 | 900 |
| Starting gold | — | 600 |
| **Total** | | **4948** |

The same denominator is used for all players regardless of role, so values are directly
comparable across heroes and games.  Efficiency can exceed 100 % — a carry that gets kills
or picks up bounty runes will earn above baseline.

```python
for p in match.players:
    if p.lane_total_gold > 0:
        print(
            f"{hero_display(p.hero_name):<22}"
            f"  eff {p.lane_efficiency_pct:>3}%"
            f"  gold@10 {p.lane_total_gold:>6,}"
        )
```

### Tier-2 metric: lane advantage (`lane_gold_adv`, `lane_xp_adv`)

Lane advantage answers the question *"how did this hero compare against their lane
opponent(s)?"*

```
lane_gold_adv = player.lane_total_gold − sum(opponent.lane_total_gold for opponent in same_role_enemies)
lane_xp_adv   = player.lane_total_xp   − sum(opponent.lane_total_xp   for opponent in same_role_enemies)
```

Opponents are defined as players on the opposing team with the **same `lane_role`**.  In a
standard 1v1 mid lane both midlaners get each other's values — their advantages are
mirrors (one's gain is the other's loss).  In a 2v2 safe lane each player is compared
against the combined gold of both opponents, so both players can end up negative if the
opposing duo outfarmed them.

Jungle (4) and roaming (5) players have `lane_gold_adv = None` and `lane_xp_adv = None`
because they have no defined lane opponent.

```python
for p in match.players:
    if p.lane_gold_adv is None:
        continue
    sign = "+" if p.lane_gold_adv >= 0 else ""
    print(
        f"{hero_display(p.hero_name):<22}"
        f"  gold adv {sign}{p.lane_gold_adv:>+6,}"
        f"  xp adv {sign}{p.lane_xp_adv:>+6,}"
    )
```

---

## Putting it all together

```python
import gem
from gem.constants import hero_display

match = gem.parse("my_replay.dem")

LANE_NAMES = {1: "Safe", 2: "Mid", 3: "Off", 4: "Jungle", 5: "Roaming", 0: "?"}

print(f"{'Hero':<22} {'Team':<5} {'Lane':<8} {'LH':>4} {'DN':>4} "
      f"{'Gold@10':>8} {'XP@10':>7} {'Eff%':>5} {'GoldAdv':>8} {'XPAdv':>7}")
print("-" * 85)

for p in sorted(match.players, key=lambda x: (x.team, x.lane_role)):
    team = "Radiant" if p.team == 2 else "Dire"
    lane = LANE_NAMES[p.lane_role]
    adv_g = f"{p.lane_gold_adv:+,}" if p.lane_gold_adv is not None else "—"
    adv_x = f"{p.lane_xp_adv:+,}"  if p.lane_xp_adv  is not None else "—"
    print(
        f"{hero_display(p.hero_name):<22} {team:<7} {lane:<8}"
        f" {p.lane_last_hits:>4} {p.lane_denies:>4}"
        f" {p.lane_total_gold:>8,} {p.lane_total_xp:>7,}"
        f" {p.lane_efficiency_pct:>4}%"
        f" {adv_g:>8} {adv_x:>7}"
    )
```

Example output (TI14 Grand Final Game 1):

```
Hero                   Team    Lane      LH   DN  Gold@10   XP@10  Eff% GoldAdv   XPAdv
---------------------  ------  --------  ---  --  -------  ------  ---- -------  ------
Shadow Fiend           Radiant Mid        45   2    4,751   7,204   96%  +783    +1,290
Sven                   Radiant Safe       38   1    3,920   5,120   79%  -360      -272
Bane                   Radiant Safe        2   0    1,359   3,480   27%  -360      -272
Slardar                Radiant Off        26   2    3,381   5,844   68%  -987    +1,012
Shadow Demon           Radiant Off         1   0    1,660   3,480   33%  -987    +1,012
Beastmaster            Dire    Mid        38   3    3,968   5,914   80%  -783    -1,290
Gyrocopter             Dire    Safe       33   1    3,408   5,392   68%  ...
Pugna                  Dire    Safe        8   0    2,228   4,848   45%  ...
Pangolier              Dire    Off        44   3    4,368   6,856   88%  ...
Ringmaster             Dire    Off         3   0    1,768   3,468   35%  ...
```

---

## Calling `classify_lane` directly

If you have a custom `lane_pos` dict (e.g. from a subset of ticks), you can classify it
directly:

```python
from gem.extractors.lane import classify_lane

# Synthetic example: hero dwelling at world coordinates (16000, 16000) — mid lane
GRID = 64
wx, wy, count = 16000, 16000, 150
lane_pos = {f"{wx // GRID}_{wy // GRID}": count}

role = classify_lane(lane_pos, team=2)  # 2 = Radiant
print(role)  # 2 (mid)
```

See the [Lane Classifier API reference](../reference/extractors/lane.md) for the full
function signature.
