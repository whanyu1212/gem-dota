# Extractors Layer

This page explains how gem converts reconstructed game state + normalized events into analysis-ready records.

Modules covered:

1. `src/gem/extractors/_snapshots.py`
2. `src/gem/extractors/players.py`
3. `src/gem/extractors/objectives.py`
4. `src/gem/extractors/wards.py`
5. `src/gem/extractors/courier.py`
6. `src/gem/extractors/draft.py`
7. `src/gem/extractors/teamfights.py`
8. `src/gem/extractors/lane.py`

Prerequisites:

1. [Bits & Bytes Primer](../cookbook/bits-and-bytes-primer.md)
2. [Stream Layer (`stream.py`)](stream-layer.md)
3. [Parser Layer (`parser.py`)](parser-layer.md)
4. [SendTable Layer (`sendtable.py`)](sendtable-layer.md)
5. [State Reconstruction Layer (`string_table.py` + `entities.py`)](state-layer.md)
6. [Event Normalization Layer (`game_events.py` + `combatlog.py`)](event-layer.md)

## Why this is the next layer

After the parser can produce stable entity updates and normalized combat/game events, extractors turn those low-level signals into match analytics objects:

1. player time series
2. objectives timeline
3. ward placement/kill/expiry timeline
4. courier state snapshots
5. draft picks/bans
6. teamfights and lane roles

## Extractor pattern used across modules

All extractor classes follow the same shape:

1. `attach(parser)` registers callback hooks.
2. Callbacks consume events incrementally during parse.
3. Extractor keeps mutable state in memory.
4. Results are exposed as dataclass lists / time series after parse.

Core parser hooks used in this layer:

| Hook | Payload | Used by |
|---|---|---|
| `on_entity` | `(entity, op)` | players, objectives, wards, courier, draft |
| `on_combat_log_entry` | `CombatLogEntry` | players, objectives, wards, combat aggregation |
| `on_chat_event` | user-message chat events | objectives |
| `on_game_start` | `game_start_tick` | players (minute alignment) |
| `on_game_end` | final tick | players (final snapshot + scoreboard) |

## `_snapshots.py`: shared player snapshot model

This helper file defines the canonical dataclasses used by `players.py`.

### Core constants

| Constant | Value | Meaning |
|---|---|---|
| `_CELL_SIZE` | `128` | World units per grid cell for `cell + vec` coordinate encoding |
| `_HERO_CLASS_PREFIX` | `CDOTA_Unit_Hero_` | Hero entity-class prefix for filtering/resolution |

### Key helpers

1. `_pos(entity)` reads `CBodyComponent.m_cellX/Y` + `m_vecX/Y` to world `(x, y)`.
2. `_snapshot_hero(entity, tick)` builds one `PlayerStateSnapshot` with core hero fields.

## `players.py`: per-player time series extractor

`PlayerExtractor` is the heaviest extractor. It samples hero state over time and overlays combat-log cumulative totals.

### Important constants

| Constant | Value | Meaning |
|---|---|---|
| `_ITEM_SLOTS` | `17` | `m_hItems.0000-0016` (main + backpack + stash) |
| `_ABILITY_SLOTS` | `32` | `m_hAbilities.0000-0031` scan range |
| `_NULL_HANDLE` | `0xFFFFFF` | Empty handle sentinel |
| `_TEAM_RADIANT` / `_TEAM_DIRE` | `2` / `3` | Team ids used in replay state |

### Main methods

| Method | What it does |
|---|---|
| `attach` | Registers `on_entity`, `on_combat_log_entry`, `on_game_start`, `on_game_end` |
| `_on_entity` | Tracks heroes/controllers/team data entities and triggers sampling |
| `_maybe_sample` | Enforces interval + minute-boundary sampling policy |
| `_sample` | Builds snapshots, overlays controller/data-team stats, reads abilities, diffs inventory |
| `_on_combat_log_entry` | Maintains running totals (damage/healing/deaths/stuns) per player |
| `_on_game_end` | Forces final snapshot and captures authoritative K/D/A scoreboard |
| `time_series` / `minute_time_series` | Materializes arrays per player from stored snapshots |

### Sampling model

Two snapshot streams are produced:

1. regular snapshots every `sample_interval` ticks (default `30` = ~1 second)
2. minute snapshots every `1800` ticks from game start (`gold_t_min`, `xp_t_min`, etc.)

Minute snapshots are deduplicated by minute index so repeated same-minute events do not create duplicate buckets.

### Special handling worth knowing

1. Gold/XP source selection is intentional:
   - spendable `gold` from `CDOTAPlayerController.m_iGold`
   - cumulative totals from `CDOTADataRadiant/Dire.m_vecDataTeam.*`
2. Initial inventory is emitted as synthetic `PURCHASE` combat-log entries once per player.
3. Ability levels are resolved via ability handles + `EntityNames` string table.

## `objectives.py`: objective timeline extractor

`ObjectivesExtractor` emits timeline events for towers, barracks, Roshan, Tormentor, shrine kills, and Aegis interactions.

### Key constants

| Constant | Value | Meaning |
|---|---|---|
| `_CHAT_MSG_AEGIS` | `8` | Aegis pickup chat event |
| `_CHAT_MSG_AEGIS_STOLEN` | `53` | Aegis stolen chat event |
| `_CHAT_MSG_DENIED_AEGIS` | `51` | Aegis denied chat event |
| `_CHAT_MSG_SHRINE_KILLED` | `101` | Shrine of Wisdom destroyed |
| `_CHAT_MSG_MINIBOSS_KILL` | `117` | Tormentor kill chat event |

### Main methods

| Method | What it does |
|---|---|
| `attach` | Registers `on_combat_log_entry`, `on_chat_event`, `on_entity` |
| `_on_entity` | Tracks alive Roshan drop-item entities (Aegis/Cheese/Shard/Banner) |
| `_on_chat_event` | Emits `AegisEvent` / `ShrineKill` and patches latest tormentor killer player id |
| `_on_combat_log` | Converts `DEATH` events into `TowerKill`, `BarracksKill`, `RoshanKill`, `TormentorKill` |

Roshan drops are reconstructed from currently alive Roshan item entities at kill tick.

## `wards.py`: ward placement, expiry, and kill attribution

`WardsExtractor` uses `m_lifeState` transitions as the primary ward lifecycle signal.

### Key constants

| Constant | Value | Meaning |
|---|---|---|
| `_WARD_CLASSES` | observer + sentry classes | Tracked entity classes |
| `_WARD_TARGET_NAMES` | observer/sentry combat-log names | Targets for killer queue |
| `_OBSERVER_LIFESPAN_TICKS` | `720` | ~6 minutes |
| `_SENTRY_LIFESPAN_TICKS` | `360` | ~3 minutes |
| `_EXPIRY_TOLERANCE_TICKS` | `30` | Grace window for expiry classification |

### Lifecycle logic

1. `lifeState` transitions to `0` (`alive`) => ward placement event.
2. `lifeState` transitions `0 -> 1` (`dying`) => killed/expired classification.
3. Killer attribution comes from queued ward `DEATH` combat-log events.
4. If no killer appears and age is near lifespan => classify as natural expiry.

### Main methods

| Method | What it does |
|---|---|
| `attach` | Registers `on_entity`, `on_combat_log_entry` |
| `_on_entity` | Tracks hero map and ward lifecycle transitions |
| `_on_ward_placed` | Captures team, placer (`m_hOwnerEntity`), coordinates |
| `_on_ward_left` | Resolves `killed_tick` vs `expires_tick` and killer |
| `_on_combat_log` | Feeds killer queues and same-tick backfill |
| `finalize` | Back-fills missing placer NPC names from player-id map |

## `courier.py`: courier polling extractor

`CourierExtractor` tracks `CDOTA_Unit_Courier*` entities and snapshots at interval.

### Main fields sampled

1. `m_iTeamNum`
2. `m_iCourierState`
3. `m_bFlyingCourier`
4. world position via `_pos(entity)`

### Main methods

| Method | What it does |
|---|---|
| `attach` | Registers `on_entity` |
| `_on_entity` | Adds/removes courier entities and triggers sampling |
| `_maybe_sample` | Interval gate (`sample_interval`, default `150`) |
| `_sample` | Appends `CourierSnapshot` records |

## `draft.py`: pick/ban extractor

`DraftExtractor` polls `CDOTAGamerulesProxy` draft fields and resolves hero names.

### Key constants

| Constant | Value | Meaning |
|---|---|---|
| `_BAN_SLOTS` | `14` | `m_BannedHeroes.0000-0013` |
| `_PICK_SLOTS` | `10` | `m_SelectedHeroes.0000-0009` |

### Resolution logic

1. Capture raw hero ids from gamerules proxy arrays.
2. De-duplicate with `_seen` keys `(is_pick, slot_index, hero_id)`.
3. Resolve hero names using live `hero_id -> npc_name` map first.
4. Fallback to bundled `heroes.json` mapping (`hero_id // 2` preferred).
5. `finalize()` re-resolves names after parse when hero entities are fully known.

### Main methods

| Method | What it does |
|---|---|
| `attach` | Registers `on_entity` |
| `_update_live_map` | Reads selected hero handles from `CDOTA_PlayerResource` |
| `_check_draft` | Emits `DraftEvent` for bans and picks |
| `finalize` | Rewrites names using full live map for correctness |

`resolve_pick_team(event, players)` is a helper that prefers post-game roster team mapping over draft-time active-team field.

## `teamfights.py` + `lane.py`: post-parse derived extractors

These modules are in `extractors/`, but run as derived computations during match assembly.

### `teamfights.py` constants

| Constant | Value | Meaning |
|---|---|---|
| `_COOLDOWN_TICKS` | `15 * 30 = 450` | Death-window merge cooldown |
| `_FIGHT_RADIUS` | `3000.0` | Spatial clustering radius between deaths/fights |

### `detect_teamfights(...)` pass structure

1. Pass 1: open/merge/close fight windows from hero deaths.
2. Pass 2: aggregate per-player damage/heal/death/buyback/gold/use stats inside windows.
3. Pass 3: compute XP deltas via nearest player snapshots.
4. Pass 4: assign winner (`radiant`/`dire`/`draw`) from kill counts.

### `lane.py`

`classify_lane(lane_pos, team)` maps first-10-minute position heatmap into lane roles:

1. safe lane (`1`)
2. mid (`2`)
3. offlane (`3`)
4. jungle (`4`)
5. roaming (`5`)

## How this layer is wired into `gem.parse`

`gem.parse(...)` attaches extractors before parsing:

```python
p = ReplayParser(path)
player_ext = PlayerExtractor()
obj_ext = ObjectivesExtractor()
ward_ext = WardsExtractor()
courier_ext = CourierExtractor()
draft_ext = DraftExtractor()

player_ext.attach(p)
obj_ext.attach(p)
ward_ext.attach(p)
courier_ext.attach(p)
draft_ext.attach(p)
```

After parse:

1. `draft_ext.finalize()` fixes draft hero names with complete live map.
2. `ward_ext.finalize()` back-fills unresolved placer names.
3. `build_parsed_match(...)` consumes all extractor outputs and runs teamfight/lane derivations.

## Real snapshot from fixture (truncated)

From `tests/fixtures/8520014563.dem`:

```text
match_id 8520014563
ticks 6318 104180
players 10
towers 16
barracks 6
roshans 2
aegis_events 2
tormentors 1
shrines 0
wards 119
courier_snapshots 6701
draft_events 0
teamfights 42
combat_log 108594
chat 2
player 0 npc_dota_hero_muerta 2 3819 55 0 0
player 1 npc_dota_hero_queenofpain 2 3497 55 3 1
player 2 npc_dota_hero_pugna 2 3339 55 10 16
...
```

How to read one player line:

1. `player_id`
2. `hero_name`
3. `team`
4. regular snapshot count (`times`)
5. minute snapshot count (`times_min`)
6. observer ward events for that player
7. sentry ward events for that player

## Common failure modes in this layer

1. Missing `EntityNames` table entries causes empty/incorrect hero/item names.
2. Wrong player-id normalization (forgetting `/ 2`) breaks attribution.
3. Minute-boundary logic drift causes mismatched `*_t_min` arrays.
4. Ward same-tick ordering issues can leave temporary empty killer fields.
5. Draft ids interpreted without `hero_id // 2` fallback can mislabel heroes.

## Next pages

1. [Match Assembly Layer](match-assembly-layer.md)
2. [Custom Extractors](../guides/07_custom_extractors.md)
3. [Time-Series and DataFrames](../guides/05_timeseries.md)
