# Parser Layer

This page explains `src/gem/parser.py` in execution order.

`parser.py` is the orchestrator layer. It connects:

1. outer stream reading (`stream.py`),
2. protobuf decoding,
3. inner message unpacking,
4. stateful subsystems (send tables, string tables, entities, game events, combat log),
5. user callbacks.

Prerequisite: [Bits & Bytes Primer](../cookbook/bits-and-bytes-primer.md)

## What this layer owns

1. Drive the parse loop over outer messages.
2. Decode outer `CDemo*` envelopes by `EDemoCommands` type.
3. Unpack inner messages from `CDemoPacket.data`.
4. Enforce processing order (string tables before packet entities).
5. Route parsed payloads to the correct subsystem.
6. Track parse state (`tick`, metadata, build, game start/end).

## Constants explained

### Outer command IDs

These are outer `EDemoCommands` IDs (with compression bit already stripped by `stream.py`):

| Constant | Value | Seen where | Why parser cares |
|---|---|---|---|
| `_DEM_FILE_INFO` | `2` | Early outer message carrying `CDemoFileInfo`. | Seeds match metadata (`match_id`, winner, mode). |
| `_DEM_SEND_TABLES` | `4` | Outer send-table envelope. | Builds serializer schema and creates `EntityManager`. |
| `_DEM_CLASS_INFO` | `5` | Outer class mapping envelope. | Enables class-id to class-name mapping for entity decode. |
| `_DEM_PACKET` | `7` | Main gameplay outer packet. | Primary stream for inner net/game updates. |
| `_DEM_SIGNON_PACKET` | `8` | Signon-phase packet. | Bootstrap updates before normal packet flow. |
| `_DEM_FULL_PACKET` | `13` | Checkpoint-like combined packet envelope. | Allows parser to process full packet snapshots. |

### Inner message IDs

These IDs exist inside `CDemoPacket.data`:

| Constant | Value | Seen where | Why parser cares |
|---|---|---|---|
| `_NET_TICK` | `4` | Inner tick marker message. | Low-priority metadata marker; parser mostly skips it. |
| `_SVC_SERVER_INFO` | `40` | Server info inner payload. | Provides build/class sizing context for entity decoding. |
| `_SVC_CREATE_STRING_TABLE` | `44` | New string table payload. | Creates lookup tables required by later entity/combat decode. |
| `_SVC_UPDATE_STRING_TABLE` | `45` | String table delta payload. | Keeps lookup tables current before entity updates run. |
| `_SVC_PACKET_ENTITIES` | `55` | Entity delta payload. | Applies world-state entity create/update/delete deltas. |
| `_SVC_USER_MESSAGE` | `72` | User message wrapper. | Gateway to Dota user messages (combat/chat/etc). |
| `_GE_GAME_EVENT_LIST` | `205` | Game-event schema payload. | Registers event IDs to names/fields before event dispatch. |
| `_GE_GAME_EVENT` | `207` | Actual game-event payload. | Dispatches named events and S1 combat-log path. |

### Dota user/combat/chat IDs

| Constant | Value | Seen where | Why parser cares |
|---|---|---|---|
| `_DOTA_UM_COMBAT_LOG_DATA` | `468` | `svc_UserMessage.msg_type`. | One S2 combat-log bulk transport variant. |
| `_DOTA_UM_COMBAT_LOG_BULK_DATA` | `470` | `svc_UserMessage.msg_type`. | Alternate S2 combat-log bulk variant. |
| `_DOTA_UM_COMBAT_LOG_HLTV` | `554` | Direct inner message type ID. | Handles direct `CMsgDOTACombatLogEntry` path. |
| `_DOTA_UM_CHAT_EVENT` | `466` | Direct inner message type ID. | Handles non-text chat events (including rune pickup side-effects). |
| `_DOTA_UM_CHAT_MESSAGE` | `612` | Direct inner message type ID. | Converts chat payload to normalized `ChatEntry`. |
| `_CHAT_MSG_RUNE_PICKUP` | `22` | `CDOTAUserMsg_ChatEvent.type`. | Detects rune pickup events for combat-log side processing. |
| `_COMBAT_LOG_NAMES_TABLE` | `"CombatLogNames"` | String table name. | Resolves integer combat-log name references to strings. |

Quick mental model for IDs in parser:

1. Outer ID chooses `CDemo*` envelope (`_dispatch_outer`).
2. Inner ID chooses subsystem handler (`_dispatch_inner`).
3. User-message subtype ID chooses Dota payload decode (`_on_user_message`).

## Helper function: `_read_inner_messages`

Purpose: split one `CDemoPacket.data` blob into individual inner messages.

Encoding it expects:

```text
{ type_id(ubit_var), size(varuint32), payload } repeated
```

Implementation core:

```python
r = BitReader(data)
messages = []
while r.rem_bits() >= 8:
    type_id = r.read_ubit_var()
    size = r.read_varuint32()
    payload = r.read_bytes(size)
    messages.append((type_id, payload))
```

Return value:

```python
list[tuple[int, bytes]]
```

## `ReplayParser` state: what each field means

Initialized in `__init__(source)`:

| Field | Meaning |
|---|---|
| `_source` | Input replay path or bytes. |
| `tick` | Current outer message tick. |
| `net_tick` | Current net tick (reserved for net tick path). |
| `game_build` | Build number discovered from server/entity context. |
| `string_tables` | Live string table store. |
| `entity_manager` | Entity state engine (created after send tables). |
| `game_event_manager` | Event schema + dispatch registry. |
| `combat_log` | Unified S1/S2 combat-log processor. |
| `_entity_callbacks` | Registered entity callbacks. |
| `_chat_callbacks` | Registered chat message callbacks. |
| `_chat_event_callbacks` | Registered chat event callbacks. |
| `_stop_at_tick` | Optional early-stop tick. |
| `_pending_server_info` | Cached server info if it arrives before entity manager exists. |
| `match_id`, `game_mode`, `leagueid`, `radiant_win` | Match metadata tracked during parse. |
| `_game_start_callbacks`, `_game_end_callbacks` | Lifecycle callbacks. |
| `_game_ended` | Prevents duplicate game-end callback fire. |

## Public callback methods

| Method | What it does |
|---|---|
| `on_entity(callback)` | Called on entity create/update/delete. |
| `on_game_event(name, handler)` | Register handler for named Source1 event. |
| `on_combat_log_entry(handler)` | Register normalized combat entry callback. |
| `on_chat_message(handler)` | Register parsed chat text callback. |
| `on_chat_event(handler)` | Register raw `CDOTAUserMsg_ChatEvent` callback. |
| `on_game_start(callback)` | Fire once when game starts (`m_flGameStartTime` turns non-zero). |
| `on_game_end(callback)` | Fire once when combat log reports game end state. |
| `stop_after_tick(tick)` | Stop parsing after this tick. |
| `parse()` | Run full parse loop. |

## Parse loop (`parse`) step-by-step

Core logic:

```python
with DemoStream(self._source) as stream:
    for tick, msg_type, data in stream:
        self.tick = tick
        if self._stop_at_tick is not None and tick > self._stop_at_tick:
            break
        self._dispatch_outer(msg_type, data)
```

After loop, parser performs metadata fallback from `CDOTAGamerulesProxy` entity if needed.

Why fallback exists:

- Some replays have missing/zero `CDemoFileInfo` winner/metadata fields.

## Outer dispatch (`_dispatch_outer`)

Behavior by `msg_type`:

1. `_DEM_FILE_INFO`: parse `CDemoFileInfo` and copy match metadata.
2. `_DEM_SEND_TABLES`: call `_on_send_tables` to build serializers/entity manager.
3. `_DEM_CLASS_INFO`: parse class mappings and apply.
4. `_DEM_PACKET`/`_DEM_SIGNON_PACKET`: parse `CDemoPacket`, dispatch inner data.
5. `_DEM_FULL_PACKET`: parse `CDemoFullPacket`, dispatch embedded packet data.

Important ordering detail:

- In full packets, parser dispatches packet data only after envelope parse; this preserves packet boundary semantics.

## Inner packet orchestration (`_dispatch_inner_packet`)

1. Unpack inner messages via `_read_inner_messages`.
2. Sort by priority before dispatch.
3. Dispatch each `(type_id, payload)`.

Priority function in code:

```python
if type_id in (_NET_TICK, _SVC_SERVER_INFO, _SVC_CREATE_STRING_TABLE, _SVC_UPDATE_STRING_TABLE):
    return -10
if type_id == _SVC_PACKET_ENTITIES:
    return 5
if type_id in (_GE_GAME_EVENT, _DOTA_UM_COMBAT_LOG_HLTV):
    return 10
return 0
```

Why this is critical:

- String table updates must be applied before entity deltas that reference them.

## Inner dispatch (`_dispatch_inner`) by message type

### Network + table setup

1. `_SVC_SERVER_INFO` -> parse and call `_on_server_info`.
2. `_SVC_CREATE_STRING_TABLE` -> create table, notify entity manager on `instancebaseline`.
3. `_SVC_UPDATE_STRING_TABLE` -> update table, same baseline hook.

### Entity updates

- `_SVC_PACKET_ENTITIES` path runs only when:
  1. `entity_manager` exists,
  2. `class_id_size > 0` (class info is ready).

### User/game event paths

1. `_SVC_USER_MESSAGE` -> parse wrapper then `_on_user_message`.
2. `_GE_GAME_EVENT_LIST` -> schema registration.
3. `_GE_GAME_EVENT` -> event dispatch and Source1 combat-log path.

### Direct channels

1. `_DOTA_UM_COMBAT_LOG_HLTV` -> parse direct combat entry and process S2 entry path.
2. `_DOTA_UM_CHAT_EVENT` -> parse event, process rune pickup side-effect, emit callbacks.
3. `_DOTA_UM_CHAT_MESSAGE` -> parse message text and emit `ChatEntry`.

## Subsystem handler methods (private)

| Method | Responsibility |
|---|---|
| `_on_send_tables(data)` | Parse serializers, create `EntityManager`, replay cached server info. |
| `_on_server_info(msg)` | Cache if entity manager missing; else apply to manager and update `game_build`. |
| `_on_class_info(msg)` | Apply class IDs and force baseline refresh. |
| `_on_game_event_list(msg)` | Register game-event schemas in `GameEventManager`. |
| `_on_game_event(msg)` | Dispatch event; if `dota_combatlog`, normalize through combat log processor. |
| `_on_user_message(msg)` | Decode combat log bulk user messages and process them. |
| `_emit_chat_message(payload)` | Decode `CDOTAUserMsg_ChatMessage`, normalize channel, emit callbacks. |
| `_on_entity_game_start(entity, op)` | Detect game start via `CDOTAGamerulesProxy` field transition. |

## Why `ServerInfo` caching exists

Problem this solves:

- In some replays, `svc_ServerInfo` can arrive before send tables.
- Entity manager is created only after send tables.

Solution in parser:

1. Cache server info in `_pending_server_info`.
2. After `_on_send_tables` creates `EntityManager`, apply cached server info.

This preserves correctness for early-arriving server info.

## Game start and game end detection

Game start:

- `_on_entity_game_start` watches `CDOTAGamerulesProxy.m_pGameRules.m_flGameStartTime`.
- First non-zero transition triggers callbacks once.

Game end:

- Parser checks combat log for `type == 9` and `value == 6` (`DOTA_COMBATLOG_GAME_STATE == 6`).
- Fires game-end callbacks once on first match.

## Truncation behavior

`parse()` wraps the main loop in `try/except Exception` and tolerates final-block corruption.

Meaning for users:

- Truncated replays can still produce partial, useful outputs instead of hard-failing entire parse.

## How this layer connects to the next layers

`parser.py` coordinates; it does not implement every low-level decode algorithm itself.

Detailed decoding lives in:

1. `reader.py` for bit primitives,
2. `sendtable.py`, `field_decoder.py`, `field_path.py` for schema+field decode,
3. `entities.py` for delta application logic.

When debugging:

1. Ordering/state timing bugs -> start in `parser.py`.
2. Wrong decoded field values -> inspect sendtable/field/entities stack.

## Next pages

1. [SendTable Layer (`sendtable.py`)](sendtable-layer.md)
2. [State Reconstruction Layer (`string_table.py` + `entities.py`)](state-layer.md)
3. [Entity State](../guides/02_entity_state.md)
4. [Combat Log](../guides/03_combat_log.md)
