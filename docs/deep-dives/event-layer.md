# Event Normalization Layer

This page explains how gem converts raw event payloads into typed game events and normalized combat log entries.

Modules covered:

1. `src/gem/game_events.py`
2. `src/gem/combatlog.py`

Prerequisites:

1. [Bits & Bytes Primer](../cookbook/bits-and-bytes-primer.md)
2. [Stream Layer (`stream.py`)](stream-layer.md)
3. [Parser Layer (`parser.py`)](parser-layer.md)
4. [SendTable Layer (`sendtable.py`)](sendtable-layer.md)
5. [State Reconstruction Layer (`string_table.py` + `entities.py`)](state-layer.md)

## Why this is the next layer

After entities/state are reconstructed, parser still needs to handle semantic event channels:

1. Source1 game events (`CMsgSource1LegacyGameEventList` + `CMsgSource1LegacyGameEvent`)
2. Source2 combat log user messages (`CDOTAUserMsg_CombatLogBulkData`)
3. Direct combat/chat inner messages in some streams

This layer turns those channels into stable Python objects/callbacks.

## `game_events.py`: schema-driven typed access

### Core constants

| Constant | Value | Meaning |
|---|---|---|
| `_TYPE_STRING` | `1` | Event key is string |
| `_TYPE_FLOAT` | `2` | Event key is float |
| `_TYPE_LONG` | `3` | Event key is int32-long |
| `_TYPE_SHORT` | `4` | Event key is int16 |
| `_TYPE_BYTE` | `5` | Event key is int8 |
| `_TYPE_BOOL` | `6` | Event key is bool |
| `_TYPE_UINT64` | `7` | Event key is uint64 |

These are used by typed getters (`get_string`, `get_float`, `get_int32`, etc.) to validate field type before returning values.

### Main types

| Type | Role |
|---|---|
| `GameEventSchema` | Event schema metadata (`event_id`, name, fields map) |
| `GameEvent` | One typed event instance with accessor methods |
| `GameEventManager` | Schema registry + handler dispatch hub |

### Event flow

1. Parser receives event schema list message.
2. `GameEventManager.register_schema(...)` stores event id -> schema mapping.
3. Parser receives raw event instance.
4. `GameEventManager.dispatch(...)` looks up schema and builds `GameEvent`.
5. Registered handlers for that event name are called.

Why schema registration matters:

- Raw events store keys as indexed values.
- Schema converts those positional keys into named, typed fields.

## `combatlog.py`: unify S1 + S2 combat channels

`combatlog.py` normalizes multiple input paths to one output model: `CombatLogEntry`.

### Key constants

| Constant | Meaning |
|---|---|
| `COMBAT_LOG_TYPES` | Supported normalized log labels |
| `_LOG_TYPE_NAMES` | Dota combat type int -> normalized label |
| `_DAMAGE_TYPE_NAMES` | Damage type int -> `physical`/`magical`/`pure`/`others` |
| `_S1_FIELD_*` | Field names for legacy Source1 `dota_combatlog` event keys |

### `CombatLogEntry`

Single normalized record with fields such as:

1. `tick`, `log_type`
2. attacker/target/inflictor names
3. `value`, `value_name`, `damage_type`
4. hero/illusion flags
5. `ability_level`, `gold_reason`, `xp_reason`
6. `stun_duration`

### Name resolution helper

`_resolve_name(name_table, index)` maps integer indices via `CombatLogNames` string table.

This is critical because many combat payloads carry only numeric name references.

## Ingestion paths handled

### Path A: Source1 legacy game event

`process_s1_event(...)`:

1. reads integer/string/bool fields from typed `GameEvent`
2. resolves attacker/target/inflictor indices
3. maps log type int -> normalized label
4. emits `CombatLogEntry`

### Path B: Source2 bulk user message

`process_s2_bulk(...)`:

1. iterates each `CMsgDOTACombatLogEntry`
2. delegates each entry to `process_s2_entry(...)`

### Path C: Source2 direct single entry

`process_s2_entry(...)` handles direct HLTV-style channel too.

Important normalization details:

1. purchase events resolve `value_name` from `msg.value` index.
2. combat `msg.value` is decoded as signed int32 from uint32 wire value (two's complement reinterpretation).
3. damage type gets mapped to normalized labels.
4. stun duration is included if field exists.

## Parser integration points

In `parser.py`, this layer is invoked from:

1. `_on_game_event(...)` for S1 `dota_combatlog`
2. `_on_user_message(...)` for S2 bulk combat log
3. `_dispatch_inner(...)` direct `CMsgDOTACombatLogEntry` and chat events

This is where game-end detection also hooks in (`GAME_STATE == 6` path).

## Real snapshot from fixture

Using `tests/fixtures/8520014563.dem` and parsing up to tick `12000`:

```text
tick_end 12002
game_events_seen 90
unique_game_events 2
GE dota_chase_hero 89
GE hltv_versioninfo 1
combat_entries 2147
CL DAMAGE 1047
CL MODIFIER_ADD 211
CL MODIFIER_REMOVE 196
CL XP 183
CL DEATH 139
CL GOLD 107
CL ITEM 82
CL HEAL 65
CL PURCHASE 58
CL ABILITY 54
CL PICKUP_RUNE 5
combat_samples
(2235, 'DAMAGE', '', '', '', 3, '')
(3135, 'DAMAGE', '', '', '', 8, '')
(3618, 'MODIFIER_ADD', 'npc_dota_hero_muerta', 'npc_dota_hero_muerta', 'modifier_muerta_gunslinger', 0, '')
(3620, 'GOLD', '', 'npc_dota_hero_queenofpain', '', 600, '')
...
```

Interpretation:

1. Game-event channel can be sparse/limited depending on replay path.
2. Combat log channel carries the majority of actionable timeline events.
3. Normalized output has consistent shape regardless of S1/S2 input route.

## Common failure modes in this layer

1. Missing `CombatLogNames` table -> names resolve as empty strings.
2. Wrong signed-value handling -> negative gold/damage semantics break.
3. S1/S2 path drift -> inconsistent outputs for same replay behavior.
4. Wrong type mapping -> event getters return errors/defaults.

When symptoms are “stats/extractors look wrong but entity state seems fine,” inspect this layer next.

## Next pages

1. [Extractors Layer](extractors-layer.md)
2. [Entity State](../guides/02_entity_state.md)
3. [Combat Log](../guides/03_combat_log.md)
