# gem.extractors

`gem.extractors` is the *during-parse* observation layer. While the replay is
streaming, each extractor attaches to a `ReplayParser`, registers callbacks, and
accumulates structured records (per-player snapshots, objective kills, ward
placements, draft picks/bans, courier state, per-minute interval curves). It
answers "what happened, tick by tick, as the entity/combat-log state evolved" —
a question the lower layers (`binary`, `schema`, `state`, `combat`) cannot
answer because they only know how to *produce* events, not which of them to keep.

This is distinct from `gem.analysis`, which runs *after* parsing on an already
assembled `ParsedMatch`. Extractors need the live parser; analysis helpers do
not.

## Mental Model

Every extractor follows the same three-phase contract: **attach → parse →
read**.

```text
extractor = SomeExtractor()
extractor.attach(parser)     # phase 1: register callbacks (before parse())
parser.parse()               # phase 2: parser drives callbacks tick by tick
results = extractor.results  # phase 3: read accumulated records (after parse())
```

During phase 2 the parser calls into each extractor through a small set of
registration hooks it exposes (`parser.py`):

```text
ReplayParser
  ├─ on_entity(cb)             → cb(entity, op)        entity create/update/delete
  ├─ on_combat_log_entry(cb)   → cb(entry)             every CombatLogEntry
  ├─ on_chat_event(cb)         → cb(msg, tick)         CDOTAUserMsg_ChatEvent
  ├─ on_game_start(cb)         → cb(game_start_tick)
  └─ on_game_end(cb)           → cb(tick)
```

An extractor's `attach()` wires itself to whichever subset it needs, stashes the
`parser` reference (to read `parser.tick`, `parser.game_time_s`,
`parser.combat_log_time_s`, `parser.entity_manager`, `parser.string_tables`),
then does nothing further until the parser pushes data at it.

```text
                 attach()                  parse()                    read
  Extractor  ───────────────►  ReplayParser  ───callbacks──►  Extractor  ──► records
   (empty)      registers       (drives loop)    fire           (full)
```

The package splits into two tiers:

- **Core extractors** (re-exported from `gem.extractors.__init__`):
  `PlayerExtractor`, `ObjectivesExtractor`, `WardsExtractor`, `CourierExtractor`,
  `DraftExtractor`, plus their record dataclasses.
- **Internal helpers** (not in `__all__`): `IntervalExtractor` (intervals.py),
  `detect_teamfights` (teamfights.py), `classify_lane` (lane.py), and the shared
  `_snapshots.py` helpers. These are wired up by `gem.api.parse` and
  `gem.results.assembly`, not imported by end users.

## The attach → parse → read timing contract

`attach(parser)` is the only setup step, and it must run **before**
`parser.parse()` — callbacks registered after the stream starts miss earlier
ticks. Inside `attach`, an extractor:

1. saves `self._parser = parser` so it can read live parser state later;
2. registers its callbacks (`parser.on_entity(self._on_entity)`, etc.).

Results are only complete **after** `parse()` returns. Two extractors need an
explicit post-parse finalize step, and `gem.api.parse` calls both
(api.py:273-274):

- `DraftExtractor.finalize()` — re-resolves *all* draft hero names through the
  now fully-populated live `hero_id → npc_name` map, correcting picks that the
  static fallback guessed wrong during the draft phase (see Pitfalls).
- `WardsExtractor.finalize()` — back-fills placer NPC names for pre-game wards
  whose owner resolved to a `CDOTAPlayerController` before a hero was assigned.

`WardsExtractor.ward_events` and `ObjectivesExtractor.*_kills` are plain
attributes populated incrementally; `PlayerExtractor.snapshots` likewise. The
`time_series(player_id)` / `minute_time_series(player_id)` methods are *views*
computed on demand from the accumulated snapshots, not separate buffers.

## Core extractors

### PlayerExtractor (players.py)

The heaviest extractor. On every `on_entity` it tracks live references to the
hero entities (`CDOTA_Unit_Hero_*`), player controllers
(`CDOTAPlayerController`), team data entities
(`CDOTADataRadiant`/`CDOTA_DataRadiant`, `CDOTADataDire`/`CDOTA_DataDire`), and
`CDOTA_PlayerResource`. When `CDOTAGamerulesProxy` or a tracked entity updates,
it calls `_maybe_sample()`, which gates on two cadences:

- a **regular** interval gap (`sample_interval`, default 30 ticks ≈ 1 s), and
- **minute boundaries** (`minute_snapshots=True` by default), aligned to the
  game clock — `parser.game_time_s` when available, else every 1800 ticks from
  game start.

Each sample (`_sample`) builds a `PlayerStateSnapshot` per player from
`_snapshot_hero`, then overlays the *authoritative* fields: current unspent gold
and net worth from the controller (`m_iGold`, `m_iNetWorth`), and cumulative
totals from the team data entity (`m_iTotalEarnedGold`, `m_iTotalEarnedXP`,
`m_iNetWorth`, `m_iLastHitCount`, `m_iDenyCount`) addressed by
`m_vecDataTeam.{team_slot:04d}.*`. This field-source distinction is critical:
advantage curves must use the monotonic `m_iTotalEarnedGold`/`m_iTotalEarnedXP`,
never the spendable `m_iGold` or the resets-on-level-up `m_iCurrentXP`.

`PlayerExtractor` also subscribes to `on_combat_log_entry` to keep running,
monotonic per-player totals (`_total_hero_damage`, `_total_hero_healing`,
`_total_deaths`, `_total_stuns`) that it stamps into each snapshot, and on the
first snapshot per player it emits synthetic `PURCHASE` combat-log entries for
the starting inventory (`_diff_inventory`) by calling
`parser.combat_log._emit`. At `on_game_end` it reads the authoritative
kills/deaths/assists scoreboard from `CDOTA_PlayerResource`
(`m_vecPlayerTeamData.{i:04d}.m_iKills/Deaths/Assists`).

`hero_pos(npc_name)` exposes a live position lookup, resolving the canonical
hero entity via the controller's `m_hAssignedHero` handle when possible.

### ObjectivesExtractor (objectives.py)

Listens to `on_combat_log_entry` for `DEATH` events and classifies the target
NPC name into `TowerKill`, `RoshanKill`, `BarracksKill`, or `TormentorKill`
(target `npc_dota_miniboss`). Tower/barracks ownership is resolved by NPC-name
prefix (`npc_dota_goodguys_*` = Radiant, `npc_dota_badguys_*` = Dire). It also
hooks `on_entity` to snapshot which Roshan drop item entities
(`CDOTA_Item_Aegis`, `CDOTA_Item_Cheese`, `CDOTA_Item_RefresherOrb_Shard`,
`CDOTA_Item_Roshans_Banner`) are alive at the kill tick, and `on_chat_event`
for Aegis pickup/steal/denial (`AegisEvent`), Shrine kills (`ShrineKill`), and
Tormentor player-slot attribution (patched onto the most recent `TormentorKill`).

### WardsExtractor (wards.py)

Uses `m_lifeState` *transitions* on ward entities (`CDOTA_NPC_Observer_Ward`,
`CDOTA_NPC_Observer_Ward_TrueSight`) as the primary signal — the OpenDota
approach. A transition to `m_lifeState == 0` (alive) is a placement: the entity
already carries exact coordinates (`_pos`) and `m_hOwnerEntity`, so no
coordinate-matching window is needed. A transition to `m_lifeState == 1` (dying)
is a kill or natural expiry, disambiguated against per-target killer queues fed
from combat-log `DEATH` events and lifespan tolerances
(`_OBSERVER_LIFESPAN_TICKS`, `_SENTRY_LIFESPAN_TICKS`,
`_EXPIRY_TOLERANCE_TICKS`). `finalize()` returns `ward_events`.

### CourierExtractor (courier.py)

Tracks `CDOTA_Unit_Courier*` entities and emits a `CourierSnapshot` (team,
`m_iCourierState`, `m_bFlyingCourier`, position) at a fixed `sample_interval`
(default 150 ticks ≈ 5 s).

### DraftExtractor (draft.py)

Polls `CDOTAGamerulesProxy` for `m_pGameRules.m_BannedHeroes.{i:04d}` (14 ban
slots) and `m_pGameRules.m_SelectedHeroes.{i:04d}` (10 pick slots), emitting an
idempotent `DraftEvent` per new `(is_pick, slot_index, hero_id)`. Hero-ID
resolution is three-tier (`_resolve_name`): live map from hero entity class
names, then `hero_id // 2` against bundled `heroes.json` (modern replays store
`api_id * 2`), then a direct `heroes.json` lookup. `resolve_pick_team` is a
module-level helper used at assembly time to pin a pick to the correct team via
the player roster.

## Internal extractors and helpers

### IntervalExtractor (intervals.py) — INTERNAL

The OpenDota-parity per-minute curve source. It is deliberately *not*
re-exported from `gem.extractors`; `gem.api.parse` constructs it and
`gem.results.assembly` consumes it. It exists separately from `PlayerExtractor`
so the authoritative `gold_t`/`xp_t` advantage curves come from
`CDOTA_DataRadiant`/`Dire` (via `m_vecDataTeam`) sampled exactly on game-clock
interval boundaries, without overloading `PlayerExtractor`.

Three subtle behaviours distinguish it from the dense player sampler:

- **Network-tick clock**: `ReplayParser` decodes `CNETMsg_Tick` and refreshes
  `game_time_s` from that server tick (including pause ticks), rather than the
  unrelated outer demo tick or the latest, possibly stale combat-log event.
- **Clarity phase** (`_on_tick_start`): minute zero is sampled immediately from
  the preceding observed team-data frame, preventing transient initialization
  values and same-tick bounty payouts from leaking backward. Later rounded-minute
  crossings are sampled at the following network tick start, including the
  crossing tick's entity deltas but preceding the next tick's. Parsers without
  the callback retain the two-frame entity fallback.
- **Raw minute-zero counters**: no blanket zeroing or numeric compensation is
  applied, so legitimate pre-horn earnings remain intact.
  `_emit_final_boundary` remains a live terminal read.

It also carries terminal scalar counters (`team_counters`) read from the same
`m_vecDataTeam` entry (camps/creeps stacked, wards placed, rune pickups, tower
kills) and emits OpenDota's observed t=0 baseline.

### teamfights.py — `detect_teamfights` (post-parse function)

Not an extractor with `attach()` — a pure function called from
`gem.results.assembly` on the finished combat log. It merges hero deaths within
a 15-second cooldown (`_COOLDOWN_TICKS`), optionally splits concurrent fights by
spatial centroid (`_FIGHT_RADIUS`) using `PlayerStateSnapshot` positions, then
aggregates per-player stats into `Teamfight`/`TeamfightPlayer`. No
minimum-death filter is applied.

### lane.py — `classify_lane` (post-parse utility)

A stateless function, no `Extractor` class. Given a player's `lane_pos` heatmap
(64-unit grid cells) and team, it maps cells to coarse zones (`_cell_zone`),
finds the dominant zone, and returns an OpenDota lane role
(1=safe, 2=mid, 3=off, 4=jungle, 5=roaming, 0=unknown). Called from
`gem.results.assembly`.

### _snapshots.py — shared helpers

Holds the dataclasses and helpers reused across extractors so each module need
not re-derive them:

- `PlayerStateSnapshot` / `PlayerTimeSeries` dataclasses (re-exported through
  `players.py` and `gem.extractors`).
- `_pos(entity)` — world `(x, y)` from `CBodyComponent.m_cellX/m_cellY` (×128)
  plus `m_vecX/m_vecY`. Called directly by players, wards, courier, and
  `_snapshot_hero`. (teamfights does not call `_pos`; it reads positions off the
  already-built snapshot `.x`/`.y` via its own `_nearest_pos`.)
- `_player_id_from_entity(entity, *, allow_owner=False)` — resolves an entity to
  a player slot 0-9 by reading `m_nPlayerID`/`m_iPlayerID` and halving the
  doubled raw value. `allow_owner` adds an `m_iPlayerOwnerID` fallback for
  *owned units* (e.g. a ward's owner unit), but **must stay False for hero-name
  lookups** so a hero-class illusion is not misattributed to the real hero.
- `_snapshot_hero(entity, tick)` — builds a base `PlayerStateSnapshot` (gold and
  cumulative fields left at 0 for the extractor to overlay).

## What This Package Does Not Do

- **It does not read bytes or bits.** Outer/inner stream framing and bit-level
  decoding live in `gem.binary` (`DemoStream`, `BitReader`).
- **It does not build serializers or decode entity field values.** The send-table
  schema and field decoders are `gem.schema`; the entity lifecycle, `FieldState`
  tree, and `EntityOp` come from `gem.state` (`entities.py`,
  `string_table.py`). Extractors only *read* finished `Entity` objects via
  `entity.get_int32`/`get_uint32`/`get_float32`/`get_bool`/`get_class_name`.
- **It does not produce combat-log entries.** S1/S2 combat-log ingestion and
  normalization are `gem.combat` (`log.py`, `aggregator.py`). Extractors consume
  `CombatLogEntry` objects through `on_combat_log_entry`. (`PlayerExtractor`
  does *emit* synthetic starting-inventory PURCHASE entries via
  `parser.combat_log._emit`, but it does not parse the wire format.)
- **It does not drive the parse loop or own the parser callbacks.** That is
  `gem.parser.ReplayParser`. Extractors are passive subscribers.
- **It does not map IDs to display names beyond hero-ID resolution.**
  Hero/item/ability/XP lookups are `gem.catalog` (DraftExtractor imports
  `HEROES` from it). Extractors store internal NPC/entity names, not localized
  display strings.
- **It does not assemble the final output model.** `ParsedMatch`/`ParsedPlayer`
  construction is `gem.results` (`models.py`, `assembly.py`), which is where
  `detect_teamfights` and `classify_lane` are actually invoked.
- **It does not do post-parse analysis on `ParsedMatch`.** Position/net-worth
  lookups, ability-hit grouping, vision geometry, map-context buckets, and Roshan
  conversion records are `gem.analysis`. The boundary: if it needs the live
  parser, it belongs here; if it needs only an assembled `ParsedMatch`, it
  belongs in `gem.analysis`.
- **It does not render reports.** That is `gem.reports`.

## Common Pitfalls

### Registering callbacks after `parse()` has started

`attach(parser)` must be called before `parser.parse()`. Callbacks added late
silently miss every earlier tick. There is no replay/rewind.

### Reading results before the parse finishes (or before finalize)

`time_series`, `minute_time_series`, `ward_events`, and `*_kills` are only
complete after `parse()` returns. For `DraftExtractor` and `WardsExtractor` you
must also call `finalize()` — `gem.api.parse` does this for you, but direct
users of the extractors must not skip it. `DraftExtractor.finalize()`
intentionally re-resolves **all** events, not just empty ones, because the
direct-lookup fallback fires first during the draft and produces wrong heroes
for doubled-ID picks.

### Using the wrong gold/XP field

`m_iGold` (controller) is spendable cash and drops on every purchase;
`m_iCurrentXP` (hero) resets to 0 each level-up. For advantage curves use the
monotonic `m_iTotalEarnedGold`/`m_iTotalEarnedXP` on
`CDOTADataRadiant`/`CDOTADataDire` (`m_vecDataTeam.{slot}.*`). `PlayerExtractor`
and `IntervalExtractor` both encode this; do not "simplify" by reading the hero
or controller gold.

### Passing `allow_owner=True` to a hero-name lookup

`_player_id_from_entity(..., allow_owner=True)` is correct only for *owned
units* (the ward's owner-unit path in `wards.py`). A hero-class illusion (Manta,
Shadow Demon disruption) shares the real hero's class and may carry only
`m_iPlayerOwnerID`; resolving it via the owner field misattributes the real
hero's stats to the illusion's owner. Hero entities always carry
`m_nPlayerID`/`m_iPlayerID`, so the default `allow_owner=False` is right for them.

### Both NPC-name forms are registered on purpose

Combat-log hero names are inconsistent: `templarassassin` vs
`templar_assassin`. `players.py` and `draft.py` register *two* candidate NPC
names per hero (a simple lowercase fold and a camelCase-split form) and overlay
the canonical name from the `EntityNames` string table when available
(`_sample` in players.py). Dropping either form breaks resolution for some
heroes.

### Treating `IntervalExtractor`, `detect_teamfights`, or `classify_lane` as public

They are not in `gem.extractors.__all__`. `IntervalExtractor` is internal
plumbing for OpenDota parity; `detect_teamfights` and `classify_lane` are
post-parse functions invoked by `gem.results.assembly`, not attach-style
extractors. Import them from their submodules only if you are extending the
pipeline.

### Recycled entity slots and `m_lifeState`

Wards (and other entities) reuse index slots across a game. `WardsExtractor`
keys live state by entity index and tracks the *previous* `m_lifeState` per
index, detecting transitions rather than filtering on `EntityOp.CREATED`. A slot
that emits `UPDATED` (not `CREATED`) still carries a valid placement; do not
filter to `CREATED`-only.

### Roshan drop entities are alive only between spawn and pickup

`ObjectivesExtractor` snapshots `self._roshan_items` (items currently alive) at
the `DEATH` tick. Items are created when Roshan spawns and deleted when picked
up, so the alive set at kill time is exactly the drop list. It clears entries on
`EntityOp.DELETED_LEFT`.

## When To Add Code Here

Add code to `gem.extractors` when the change is about **observing live
entity/combat-log/chat state as the replay streams** and turning it into
structured records.

Good fits:

- a new during-parse signal: a new objective, a new entity-state time series, a
  new chat-event-derived record;
- a new field overlay on `PlayerStateSnapshot` sourced from an entity read each
  tick;
- a new attach-style extractor following the `attach → callbacks → read`
  contract, plus its record dataclass.

Poor fits:

- anything computed from a finished `ParsedMatch` with no live parser — put it in
  `gem.analysis` (e.g. `position_at_tick`, vision estimation, Roshan
  conversion);
- new bit/byte decoding (`gem.binary`), entity-field decoding (`gem.schema` /
  `gem.state`), or combat-log wire parsing (`gem.combat`);
- ID→display-name tables (`gem.catalog`);
- shaping the final output model or DataFrame/JSON export (`gem.results`);
- HTML/report rendering (`gem.reports`).

When adding shared snapshot dataclasses or helpers reused by more than one
extractor, put them in `_snapshots.py` rather than duplicating per module.
