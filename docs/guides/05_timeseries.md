# Time-Series & DataFrames

gem samples entity state during parsing and assembles per-minute advantage curves,
position logs, player snapshots, and event tables. This guide shows how to use those
outputs from the high-level API and, when needed, from the lower-level extractor API.

## Per-minute advantage curves

`match.radiant_gold_adv` and `match.radiant_xp_adv` are lists of integers, one entry per
game minute. `match.game_times_min` is their parallel, authoritative game-relative axis
in seconds (`0, 60, 120, ...`). Positive values favor Radiant; negative values favor Dire.

```python
import gem

match = gem.parse("my_replay.dem")

print("Minute  Gold adv  XP adv")
for game_time_s, gold, xp in zip(
    match.game_times_min,
    match.radiant_gold_adv,
    match.radiant_xp_adv,
    strict=True,
):
    minute = game_time_s // 60
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

`gem.parse_to_dataframe()` returns a dict of flat pandas DataFrames:

```python
import gem

frames = gem.parse_to_dataframe("my_replay.dem")

print(sorted(frames))
summary = frames["player_summary"]
combat = frames["combat_log"]
```

Every table starts with a `match_id` column (`0` when the replay carries no
match ID), so tables from different replays can be concatenated and joined.
Core tables hold only primitive cells: list-valued fields are joined with `";"`,
and per-player dict statistics are exported in long form. Nested records keep
their full structure in the dataclass and [JSON](10_json_output.md) output.

Core tables (always returned):

| Key | Contents |
|---|---|
| `match` | Single-row match metadata and final status bitmasks |
| `player_summary` | One row per player: identity, K/D/A, final net worth/LH/DN, GPM/XPM, damage/healing totals, lane stats, damage-type split, largest hero hit, consumed Aghanim's/Moon Shard flags |
| `player_timeseries` | Per-player sampled state: `tick`, `gold`, `total_earned_gold`, `total_earned_xp`, `net_worth`, `lh`, `dn`, `xp` |
| `players_minute` | Per-player series resampled to one row per game minute, with `game_time_s` / `minute` join keys |
| `player_breakdowns` | Long-form per-player dict stats: `(player_id, stat, key, subkey, value)` |
| `positions` | Per-player world `(x, y)` positions over time |
| `radiant_advantage` | Radiant gold/XP advantage per minute, with `game_time_s` / `minute` join keys |
| `combat_log` | Raw normalized combat log entries |
| `wards` | Ward placement events with coordinates |
| `objectives` | Typed Gem objective rows such as towers, barracks, Roshan, tormentors, couriers |
| `chat` | Chat messages |
| `draft` | Pick and ban events |
| `teamfights` | Gem teamfight windows, one row per fight with a `fight_index` |
| `teamfight_players` | Per-fight, per-player stats (deaths, damage, healing, gold/XP delta) |
| `smoke_events` | Smoke activations; `smoked` is a `";"`-joined hero list |
| `smoke_members` | Flat per-hero smoke application/removal timing and sampled positions |
| `courier_snapshots` | Courier state over time |
| `neutral_item_finds` | Neutral item find events from `DOTA_UM_FoundNeutralItem` |
| `hero_visibility_events` | Authoritative per-team hero visibility transitions |
| `entity_visibility` | Per-team visibility transitions for tracked NPCs |
| `vision_modifiers` | Vision-granting modifier lifecycles; `evidence_gaps` is `";"`-joined |
| `vision_modifier_pairing_issues` | Modifier add/remove pairing diagnostics |
| `player_kills_log` | Per-player kill log rows |
| `player_purchase_log` | Per-player purchase log rows |
| `player_runes_log` | Per-player rune pickup log rows |
| `player_buyback_log` | Per-player buyback log rows |

Optional groups (pass `include=[...]`):

| Group | Tables |
|---|---|
| `"analysis"` | `teamfight_positioning`, `roshan_conversions`, `roshan_conversion_fights`, `smoke_fight_insights`, `smoke_fight_members`, `smoke_fight_followups`, `farming_routes`, `farming_route_segments`, `farming_route_points`, `farming_context_tags` |
| `"opendota"` | `opendota_objectives`, `opendota_teamfights` |

```python
frames = gem.parse_to_dataframe("my_replay.dem", include=["analysis"])
segments = frames["farming_route_segments"]
```

The analysis group runs the post-parse farming, smoke-fight, Roshan-conversion,
and teamfight-positioning analyses, so it adds several seconds per replay. Leave it
out when you only need the core tables.

### Player tables

```python
summary = frames["player_summary"]
series = frames["player_timeseries"]

print(summary[["player_id", "hero_name", "kills", "deaths", "assists", "net_worth"]])

# Join end-of-game scalars onto the sampled series when you need both.
joined = series.merge(summary[["match_id", "player_id", "lane_role"]], on=["match_id", "player_id"])
```

`player_breakdowns` holds the per-player dict statistics (`damage`,
`damage_targets`, `ability_uses`, `item_uses`, `purchase`, `gold_reasons`,
`lane_pos`, and so on) in long form. `stat` is the `ParsedPlayer` field name;
`subkey` is set only for two-level fields such as `damage_targets`
(`inflictor -> target -> damage`):

```python
breakdowns = frames["player_breakdowns"]
axe_targets = breakdowns[(breakdowns["player_id"] == 0) & (breakdowns["stat"] == "damage_targets")]
by_target = axe_targets.groupby("subkey")["value"].sum()
```

### Positions table

```python
positions = frames["positions"]
axe_positions = positions[positions["hero_name"] == "npc_dota_hero_axe"]

print(axe_positions[["tick", "x", "y"]].head())
```

Positions are split into a dedicated table so movement-heavy analysis does not bloat the
player-state tables.

### Many replays

Use `gem.parse_many_to_parquet()` to write one Parquet directory per replay, then
load a single table across all of them with `gem.read_parquet_table()`:

```python
gem.parse_many_to_parquet("replays/", "./out", workers=4)
combat = gem.read_parquet_table("./out", "combat_log")  # adds a `replay` column
```

Memory stays bounded by the worker count while parsing, and loading scales with the
one table you read. `gem.parse_many_to_dataframe()` is deprecated: it keeps every
parsed match and every table in memory until the batch finishes.

## Plot gold advantage

```python
import matplotlib.pyplot as plt
import gem

match = gem.parse("my_replay.dem")

minutes = [game_time_s / 60 for game_time_s in match.game_times_min]
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
`total_deaths_t`, and `total_stuns_t`. The object returned by
`minute_time_series()` also populates `game_times_s` with its exact game-relative
minute boundaries; the dense `time_series()` output leaves that axis empty.

For most analysis code, prefer `gem.parse()` or `gem.parse_to_dataframe()` and use the
lower-level extractor only when you need a different sampling interval or custom parser
callbacks.
