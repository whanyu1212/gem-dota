# Laning Analysis

The laning phase covers roughly the first ten minutes of a Dota 2 match — the period before
heroes rotate and teamfights begin.  gem extracts two things from this window:

1. **Lane assignment** — which lane each hero was in (safe, mid, off, jungle), and whether
   they roamed
2. **Lane metrics** — how well each hero performed during those ten minutes

Lane assignment matches OpenDota's `lane_pos`, `lane`, `lane_role` and `is_roaming`
exactly on the local parity fixtures.

---

## How lanes are assigned

### Position heatmap (`lane_pos`)

gem reads each hero's position once a second, at the same moments OpenDota's parser
does, from the hero's spawn until game time 600 s. The pre-game seconds before the horn
count too. Each sample is counted in an OpenDota **map cell**: world units divided by
128, rounded as OpenDota rounds. `lane_pos` nests the counts as `{x: {y: count}}`:

```python
match = gem.parse("my_replay.dem")

hero = match.players[1]  # pick any player
print(hero.lane_pos)
# {"101": {"102": 1}, "103": {"104": 1}, "166": {"78": 41, "79": 12}, ...}
#   ^ cell x   ^ cell y   ^ samples in that cell
```

To recover world coordinates, multiply a cell by 128:

```python
for cx, column in hero.lane_pos.items():
    for cy, count in column.items():
        wx, wy = int(cx) * 128, int(cy) * 128   # cell centre in world units
```

`lane_pos` is limited to the laning window. `position_log` (the full-game movement trail)
is a separate, unfiltered list.

### Cell → lane

OpenDota maps every cell from 64 to 191 on each axis to one of five lanes:

| `lane` | Area |
|---|---|
| 1 | Bottom lane: the bottom and right edges |
| 2 | Mid lane: the diagonal, plus the central band between the jungles |
| 3 | Top lane: the left and top edges |
| 4 | Radiant jungle |
| 5 | Dire jungle |

Samples outside that grid (under 1% on the fixtures, mostly map borders) are skipped.
The most common lane wins. On a tie, the lane that first reaches the highest count wins,
reading cells in ascending x and then ascending y.

### Lane → role, and roaming

`lane_role` depends on the team:

| `lane_role` | Label | Lane |
|---|---|---|
| 1 | Safe lane | Radiant bottom / Dire top |
| 2 | Mid lane | Mid |
| 3 | Off lane | Radiant top / Dire bottom |
| 4 | Jungle | Either jungle |
| 0 | Unknown | No sample on the grid |

**Roaming is a flag, not a role.** `is_roaming` is `True` when the most common lane holds
under 45% of the counted samples. A roaming support still has a `lane_role`: the lane it
spent the most time in.

```python
LANE_NAMES = {1: "Safe", 2: "Mid", 3: "Off", 4: "Jungle", 0: "Unknown"}

for p in match.players:
    from gem.constants import hero_display
    roaming = " (roaming)" if p.is_roaming else ""
    print(f"{hero_display(p.hero_name):<22}  {LANE_NAMES[p.lane_role]}{roaming}")
```

### Placing cells on the map image

The report draws lanes over `assets/maps/Game_map_7.41.jpg`. A cell's world position is
`cell * 128`. The report maps world coordinates onto the image through a window
calibrated against building positions from a replay (`MAP_XMIN` … in
`gem.reports._formatting`). All six T1 towers, the outposts, both ancients and fountains,
the twin gates, the Tormentor and the Roshan pit land on their structures, within about
60 world units. OpenDota's lane grid also fits the 7.41 map: all 18 lane towers fall in
their own lane.

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

Jungle (4) and unknown (0) players have `lane_gold_adv = None` and `lane_xp_adv = None`
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

LANE_NAMES = {1: "Safe", 2: "Mid", 3: "Off", 4: "Jungle", 0: "?"}

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

## Calling `assign_lane` directly

If you have a custom `lane_pos` map (e.g. from a subset of samples), you can assign it
directly:

```python
from gem.extractors.lane import assign_lane

# 150 samples in cell (128, 128): the mid diagonal
result = assign_lane({"128": {"128": 150}}, team=2)  # 2 = Radiant
print(result)  # LaneAssignment(lane=2, lane_role=2, is_roaming=False)
```

See the [Lane Classifier API reference](../reference/extractors/lane.md) for the full
function signature.
