# Annotated JSON Output

This page walks through the real JSON output from parsing
**TI14 Grand Finals Game 1 — XG vs Falcons**.

Every field is shown exactly as `gem.parse_to_json()` produces it, with annotations
explaining what each value means. Arrays are truncated for readability — the full
output is at [`examples/ti14_sample.json`](https://github.com/whanyu1212/gem-dota/blob/main/examples/ti14_sample.json).

!!! tip "Generate your own"
    ```bash
    python -m gem parse my_replay.dem --format json > my_match.json
    ```

---

## Top-level structure

```json
{
  "match_id": 8461735141,    // (1)
  "game_mode": 2,            // (2)
  "leagueid": 18324,         // (3)
  "radiant_win": true,       // (4)
  "game_start_tick": 26021,  // (5)
  "game_end_tick": 99262,    // (6)

  "players":        [...],   // list[ParsedPlayer]  — one per player
  "draft":          [...],   // list[DraftEvent]    — picks and bans in order
  "combat_log":     [...],   // list[CombatLogEntry] — every damage/kill/heal/item event
  "wards":          [...],   // list[WardEvent]     — ward placements with coordinates
  "towers":         [...],   // list[TowerKill]     — tower deaths
  "barracks":       [...],   // list[BarracksKill]
  "roshans":        [...],   // list[RoshanKill]
  "aegis_events":   [...],   // list[AegisEvent]
  "tormentors":     [...],   // list[TormentorKill]
  "shrines":        [...],   // list[ShrineKill]
  "teamfights":     [...],   // list[Teamfight]     — detected fight windows
  "smoke_events":   [...],   // list[SmokeEvent]
  "chat":           [...],   // list[ChatEntry]
  "courier_snapshots": [...],
  "radiant_gold_adv": [0, -98, 257, -273, -132, -583, -1579, -1777, ...], // (7)
  "radiant_xp_adv":   [0, -168, 89, -310, -491, -963, -2268, -2612, ...] // (8)
}
```

1. Valve match ID — unique identifier for this game.
2. `2` = All Pick. See `gem.constants` for the full mode table.
3. League ID — `18324` is The International 2024.
4. `true` = Radiant won. XG (Radiant) defeated Falcons (Dire).
5. The tick when the game clock started (pre-game has negative virtual time).
6. The tick when the game ended. Divide by 30 to get seconds from game start.
7. Per-minute Radiant gold advantage. Negative = Dire is ahead. This match shows
   Dire pulling ahead in the early game.
8. Same, for XP. Both curves are relative to **total earned** (monotonically
   increasing), not current gold/XP which resets on purchases/level-ups.

---

## `players[]`

One object per player (10 total). `team: 2` = Radiant, `team: 3` = Dire.

```json
{
  "player_id": 0,                       // (1)
  "hero_name": "npc_dota_hero_sven",    // (2)
  "player_name": "Ame",                 // (3)
  "team": 2,                            // (4)

  "kills": 11,
  "deaths": 0,
  "assists": 3,
  "stuns_dealt": 40.57,                 // (5)

  "lane_role": 1,                       // (6)
  "lane_last_hits": 79,
  "lane_denies": 5,
  "lane_total_gold": 3920,
  "lane_total_xp": 4151,
  "lane_efficiency_pct": 79,            // (7)
  "lane_gold_adv": 512,                 // (8)
  "lane_xp_adv": 990,

  "gold_t":      [625, 740, 820, ...],  // (9)
  "lh_t":        [12, 18, 25, ...],     // last hits per minute
  "xp_t":        [480, 960, 1440, ...], // XP earned per minute
  "net_worth_t": [1200, 1600, 2100, ...],

  "kills_log":    [...],                // (10)
  "purchase_log": [...],                // (11)
  "runes_log":    [...],                // (12)
  "buyback_log":  [...],
  "obs_log":      [...],                // observer ward placements
  "sen_log":      [...],                // sentry ward placements

  "damage":          {...},             // (13)
  "damage_taken":    {...},
  "damage_by_type":  {"magical": 12340, "physical": 8920, "pure": 450},
  "healing":         {...},
  "ability_uses":    {"sven_storm_bolt": 18, "sven_gods_strength": 7, ...},
  "item_uses":       {"item_blink": 12, "item_black_king_bar": 6, ...},
  "gold_reasons":    {...},
  "xp_reasons":      {...},
  "lane_pos":        {...},             // (14)
  "position_log":    [...]              // (15)
}
```

1. Slot index 0–9. 0–4 are Radiant (team 2), 5–9 are Dire (team 3).
2. Internal NPC name. Use `gem.constants.hero_display("npc_dota_hero_sven")` → `"Sven"`.
3. Steam display name from the replay header.
4. `2` = Radiant, `3` = Dire.
5. Total seconds of stun dealt to enemy heroes across the whole game.
6. `1` = Safe lane, `2` = Mid, `3` = Off lane, `4` = Jungle/Roaming. Classified from
   the first 10 minutes of position data.
7. Lane efficiency percentage — gold earned vs. the theoretical maximum available in
   that lane during the laning phase.
8. Gold advantage over the opposing laner at the end of the laning phase (10 min).
9. Per-minute time series — one value per game minute. Index 0 = minute 0 (game start).
10. Each kill this hero registered, as a `CombatLogEntry` with `log_type: "KILL"`.
11. Item purchases in order — `value_name` is the item NPC name
    (e.g. `"item_black_king_bar"`).
12. Rune pickups — `gold_reason: 5` = bounty rune.
13. Damage dealt/taken keyed by target or source NPC name.
14. Heatmap of positions during the laning phase, bucketed into 64-unit grid cells.
15. Full tick-by-tick position log: `[{"tick": 26021, "x": 13824, "y": 19584}, ...]`.

---

## `draft[]`

Picks and bans in chronological order.

```json
[
  {
    "tick": 291,
    "slot_index": 0,
    "hero_id": 132,
    "hero_name": "npc_dota_hero_chen",
    "is_pick": false,   // false = ban
    "team": 3           // Dire banned Chen
  },
  {
    "tick": 873,
    "slot_index": 7,
    "hero_name": "npc_dota_hero_naga_siren",
    "is_pick": false,
    "team": 3
  },
  {
    "tick": 1305,
    "hero_name": "npc_dota_hero_mars",
    "is_pick": false,
    "team": 2           // Radiant banned Mars
  }
  // ... 21 more events
]
```

`team: 2` = Radiant action, `team: 3` = Dire action. `is_pick: true` = pick,
`false` = ban. `tick` is in pre-game time (negative virtual clock).

---

## `combat_log[]`

Every damage, kill, heal, item use, and modifier event — 68,591 entries in this match.
All entries share the same schema; `log_type` tells you what happened.

### DAMAGE — hero ability damage

```json
{
  "tick": 25969,
  "log_type": "DAMAGE",
  "attacker_name": "npc_dota_hero_sven",
  "target_name": "npc_dota_hero_pangolier",
  "inflictor_name": "sven_storm_bolt",  // (1)
  "value": 58,                          // (2)
  "attacker_is_hero": true,
  "target_is_hero": true,
  "damage_type": "magical",             // (3)
  "stun_duration": 0.0                  // (4)
}
```

1. The ability or item that dealt the damage. Empty string = right-click (auto-attack).
2. Damage value after reductions.
3. `"magical"`, `"physical"`, `"pure"`, or `"others"`.
4. Non-zero for abilities that also stun (e.g. Storm Bolt itself has a stun duration
   separate from the damage event).

### HEAL

```json
{
  "tick": 27574,
  "log_type": "HEAL",
  "attacker_name": "npc_dota_hero_slardar",
  "target_name": "npc_dota_hero_slardar",  // (1)
  "inflictor_name": "item_tango_single",
  "value": 111
}
```

1. `attacker == target` = self-heal. For teammate heals, they differ.

### PURCHASE

```json
{
  "tick": 23322,
  "log_type": "PURCHASE",
  "target_name": "npc_dota_hero_sven",  // (1)
  "value_name": "item_tango"            // (2)
}
```

1. The hero who bought the item (`attacker_name` is empty for purchases).
2. Item NPC name. Use `gem.constants.item_display("item_tango")` → `"Tango"`.

!!! note "Common `log_type` values"
    | Value | What it records |
    |---|---|
    | `DAMAGE` | Damage dealt (ability or auto-attack) |
    | `KILL` | A unit died |
    | `HEAL` | HP restoration |
    | `ITEM` | Item activated (smoke, ward placed, etc.) |
    | `PURCHASE` | Item purchased from shop |
    | `ABILITY` | Ability cast |
    | `MODIFIER_ADD` | Buff/debuff applied |
    | `MODIFIER_REMOVE` | Buff/debuff expired or dispelled |
    | `GOLD` | Gold gained |
    | `XP` | XP gained |
    | `PICKUP_RUNE` | Rune picked up |
    | `BUYBACK` | Player bought back |

---

## `wards[]`

Ward placements with exact map coordinates extracted from the entity stream.

```json
{
  "tick": 24315,
  "player_id": 1,
  "placer": "npc_dota_hero_nevermore",
  "ward_type": "observer",          // (1)
  "team": 2,
  "x": 15607.5625,                  // (2)
  "y": 17761.65625,
  "expires_tick": 35116,            // (3)
  "killed_tick": null,              // (4)
  "killer": ""
}
```

1. `"observer"` or `"sentry"`.
2. World coordinates in the Source 2 coordinate system. The Dota 2 map spans
   roughly 0–16384 on each axis. Use these directly for heatmaps.
3. Tick when the ward will naturally expire (360 seconds × 30 ticks/sec after placement).
4. `null` if the ward was never killed. Populated if an enemy dewarded it.

---

## `roshans[]`

```json
[
  {
    "tick": 52697,
    "killer": "npc_dota_hero_pugna",
    "kill_number": 1       // (1)
  },
  {
    "tick": 77715,
    "killer": "npc_dota_hero_sven",
    "kill_number": 2
  }
]
```

1. Roshan kill number in this match (1-indexed). Used to determine which drops were
   available (Cheese on kill 2+, Aghanim's Blessing on kill 3+).

---

## `aegis_events[]`

```json
[
  { "tick": 52699, "player_id": 7, "event_type": "pickup" },   // (1)
  { "tick": 77729, "player_id": 0, "event_type": "pickup" }
]
```

1. `event_type` is `"pickup"`, `"stolen"`, or `"denied"`. `player_id` refers to the
   slot index matching `players[].player_id`.

---

## `towers[]`

```json
[
  {
    "tick": 42663,
    "team": 3,                                    // (1)
    "killer": "npc_dota_hero_nevermore",
    "tower_name": "npc_dota_badguys_tower1_mid"   // (2)
  }
]
```

1. `team: 3` = the Dire tower was destroyed (a Radiant tower death would be `team: 2`).
2. NPC name encodes the team (`goodguys`/`badguys`), tier (`tower1`–`tower4`), and
   lane (`top`/`mid`/`bot`). `tower4` = Ancient.

---

## `smoke_events[]`

```json
{
  "tick": 23855,
  "activator": "npc_dota_hero_bane",
  "team": 2,
  "smoked": [                          // (1)
    "npc_dota_hero_sven",
    "npc_dota_hero_bane",
    "npc_dota_hero_slardar",
    "npc_dota_hero_shadow_demon",
    "npc_dota_hero_nevermore"
  ],
  "x": 13898.0078125,                  // (2)
  "y": 20347.984375
}
```

1. All heroes that received the smoke buff. Full 5-man smoke here.
2. Centroid of the group's positions at activation time.

!!! note "Empty group edge case"
    If the activating hero was inside a sentry ward's truesight at activation time,
    the smoke breaks instantly. `smoked` will be an empty list — the item was genuinely
    wasted, not a parsing gap.

---

## `teamfights[]`

Detected fight windows where multiple heroes exchanged damage.

```json
{
  "start_tick": 76186,
  "end_tick": 77572,
  "last_death_tick": 77122,
  "deaths": 5,
  "centroid_x": 13834.40625,    // (1)
  "centroid_y": 16177.85625,
  "players": [
    {
      "player_id": 0,           // Sven (XG carry)
      "deaths": 0,
      "buybacks": 0,
      "damage_dealt": 9957,
      "damage_taken": 5141,
      "healing": 0,
      "gold_delta": 0,
      "xp_delta": 1902,
      "ability_uses": {
        "sven_warcry": 2,
        "sven_gods_strength": 1,
        "sven_storm_bolt": 1
      },
      "item_uses": {
        "item_black_king_bar": 1,
        "item_mask_of_madness": 1,
        "item_blink": 1
      }
    }
    // ... 9 more players
  ]
}
```

1. Average position of all kill events during this fight window — useful for placing
   the fight on the map.

!!! note "Participation vs. presence"
    A player appears in `players[]` for every fight. They are considered an **active
    participant** only if `deaths > 0`, `damage_dealt > 0`, `damage_taken > 0`, or
    `healing > 0` (healing a *different* hero). Players with all-zero stats were
    nearby but did not engage.

---

## `chat[]`

All-chat and team-chat messages with tick and slot.

```json
[
  { "tick": 23603, "player_slot": 4, "channel": "all", "text": "GLHF" },
  { "tick": 23715, "player_slot": 1, "channel": "all", "text": "gl hf" },
  { "tick": 23721, "player_slot": 9, "channel": "all", "text": "hf" },
  { "tick": 24013, "player_slot": 0, "channel": "all", "text": "gl" }
]
```

`channel` is `"all"` or `"team"`. `player_slot` maps to `players[].player_id`.

---

## Further reading

- [Full Match Data](04_match_data.md) — complete field reference for `ParsedMatch` and `ParsedPlayer`
- [Models reference](../reference/models.md) — Python dataclass definitions
- [Time-Series & DataFrames](05_timeseries.md) — working with the per-minute arrays
- [Combat Log guide](03_combat_log.md) — filtering and aggregating combat log entries
