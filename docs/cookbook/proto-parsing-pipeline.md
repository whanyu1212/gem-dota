# How Proto Parsing Works

This page explains replay parsing as a pipeline of transformations.

Goal: start with a `.dem` replay file and end with structured events, entities, and match
metadata.

You do **not** need to know bit math to follow this. We will focus on concepts first.

If you want a quick binary-format foundation first, read
[Bits & Bytes Primer](bits-and-bytes-primer.md).

## The mental model

Think of a replay as nested containers:

1. A file-level stream of **outer messages**.
2. Some outer messages contain a byte blob with many **inner messages**.
3. Most inner messages are protobuf payloads with named fields.
4. A few inner fields (especially entity deltas) contain custom bit-packed data that is
   not protobuf.

So parsing is not one decoder. It is a chain of decoders.

## The pipeline at a glance

```text
Replay .dem bytes
  -> outer framing decoder
  -> outer protobuf decode (CDemo*)
  -> inner message unpack ({type, size, payload} repeated)
  -> inner protobuf decode (CSVC*/CNET*/game events/user messages)
  -> subsystem handlers (string tables, entities, combat log, events)
  -> structured match outputs
```

## Stage 1: Outer framing (container layer)

The file is read as a sequence of records. Each record has:

- command/type id
- tick
- payload size
- payload bytes

At this point, payload bytes are still opaque. The parser only knows:
"this payload belongs to outer message type X at tick Y."

If the compression flag is set on that record, payload bytes are decompressed before
continuing.

## Stage 2: Outer protobuf decode (envelope layer)

Now each outer payload is decoded as a specific `CDemo*` message based on command type.

Example:

- If the command is send tables, decode payload as `CDemoSendTables`.
- If the command is packet/signon packet, decode as `CDemoPacket`.
- If the command is full packet, decode as `CDemoFullPacket`.

This stage answers: "what kind of replay structure is this payload?"

## Stage 3: Inner message unpack (packet multiplexing layer)

`CDemoPacket.data` is not one message. It is a packed stream of many inner messages:

```text
{ type_id, size, payload } { type_id, size, payload } ...
```

The parser loops through this byte stream and splits it into inner chunks.

Conceptually:

- outer packet = batch container
- inner messages = actual network/game update units

## Stage 4: Inner protobuf decode (semantic layer)

After unpacking inner chunks, each chunk is decoded by `type_id`:

- string table updates
- packet entities
- user messages
- game event schema + events
- server info

Most of these are protobuf payloads and become typed objects with named fields.

## Stage 5: Subsystem routing (state-building layer)

Decoded messages are then routed to specific subsystems:

- String table subsystem builds name/value dictionaries used elsewhere.
- Entity subsystem applies create/update/delete deltas to world state.
- Game event subsystem dispatches named events to callbacks.
- Combat log subsystem normalizes Source 1 + Source 2 combat entries.

Important concept: parsing is incremental state reconstruction. Later messages often depend
on context from earlier messages.

## Stage 6: Non-protobuf payloads inside protobuf fields

A common confusion: "If everything is protobuf, why do we need custom bit readers?"

Because some protobuf fields contain raw encoded byte blobs that are **not** protobuf.
Example: entity delta payloads.

So there are two decode worlds:

- protobuf decode for message structure
- custom bit-level decode for packed gameplay state

Both are required for a full parser.

## Outer protobuf messages (complete list)

You are right to ask for a complete reference. The outer stream is defined by
`EDemoCommands`, and each command maps to a `CDemo*` protobuf envelope.

| Command | Outer protobuf envelope | What it contains | Why it matters |
|---|---|---|---|
| `DEM_Stop (0)` | `CDemoStop` | Empty stop marker. | Clean end-of-stream signal. |
| `DEM_FileHeader (1)` | `CDemoFileHeader` | Demo stamp, patch/build, map/server/client metadata. | Format/version context for the file. |
| `DEM_FileInfo (2)` | `CDemoFileInfo` | `CGameInfo` snapshot (match id, mode, winner, teams, players). | Seeds high-level match metadata early. |
| `DEM_SyncTick (3)` | `CDemoSyncTick` | Empty sync marker. | Stream alignment/synchronization point. |
| `DEM_SendTables (4)` | `CDemoSendTables` | Bytes containing flattened serializer schema payload. | Required before entity delta decode. |
| `DEM_ClassInfo (5)` | `CDemoClassInfo` | Class id to network/table name mappings. | Binds runtime class ids to schema names. |
| `DEM_StringTables (6)` | `CDemoStringTables` | Full table snapshots (`table_name`, items, clientside items, flags). | Rebuilds lookup dictionaries used by many systems. |
| `DEM_Packet (7)` | `CDemoPacket` | `data` blob with many inner messages. | Main gameplay update channel. |
| `DEM_SignonPacket (8)` | `CDemoPacket` | Same shape as packet, during signon phase. | Early bootstrap/update channel. |
| `DEM_ConsoleCmd (9)` | `CDemoConsoleCmd` | Console command string. | Ancillary command/debug info. |
| `DEM_CustomData (10)` | `CDemoCustomData` | Callback index + opaque custom bytes. | Extension/custom payload channel. |
| `DEM_CustomDataCallbacks (11)` | `CDemoCustomDataCallbacks` | Callback save IDs list. | Metadata for custom callback channel. |
| `DEM_UserCmd (12)` | `CDemoUserCmd` | User cmd number + encoded cmd bytes. | Input-command stream data. |
| `DEM_FullPacket (13)` | `CDemoFullPacket` | Optional `string_table` snapshot + `packet`. | Combined checkpoint-style state update. |
| `DEM_SaveGame (14)` | `CDemoSaveGame` | Save payload + steam/signature/version fields. | Save/restore-related metadata. |
| `DEM_SpawnGroups (15)` | `CDemoSpawnGroups` | Repeated spawn-group message blobs. | Spawn-group state transfer. |
| `DEM_AnimationData (16)` | `CDemoAnimationData` | Entity id, tick range, data blob, checksum. | Animation segment payloads. |
| `DEM_AnimationHeader (17)` | `CDemoAnimationHeader` | Entity id, tick, header data blob. | Animation stream metadata/header path. |
| `DEM_Recovery (18)` | `CDemoRecovery` | Initial spawn-group entry + recovery message bytes. | Recovery/state reconstruction path. |

Note: `DEM_Error (-1)` and `DEM_Max (19)` are enum sentinels, not normal payload-carrying
stream messages.

## Where `CDOTA*` messages live

`CDOTA*` protobufs are usually **not outer envelopes**. They are payload types decoded
after the parser enters the inner message layer.

| Family | Wrapped by | Examples | Role |
|---|---|---|---|
| `CSVCMsg_*` | Inner packet message type IDs | `CSVCMsg_ServerInfo`, `CSVCMsg_CreateStringTable`, `CSVCMsg_PacketEntities` | Core server update channel inside `CDemoPacket.data`. |
| `CSVCMsg_UserMessage` + `CDOTAUserMsg_*` | `CSVCMsg_UserMessage.msg_data` (or direct inner IDs in some replays) | `CDOTAUserMsg_CombatLogBulkData`, `CDOTAUserMsg_ChatEvent`, `CDOTAUserMsg_ChatMessage` | Dota-specific user-message payloads. |
| `CMsgSource1LegacyGameEvent*` | Inner game event type IDs | `CMsgSource1LegacyGameEventList`, `CMsgSource1LegacyGameEvent` | Schema + instances for named game events. |
| `CMsgDOTACombatLogEntry` | Direct inner message in some streams (e.g., HLTV path) | `CMsgDOTACombatLogEntry` | Direct combat-log entry path. |

So if you are looking for `CDOTA...` types, treat them as **inner semantic payloads**, not
top-level outer replay envelopes.

## A worked example (no byte math)

Suppose the parser encounters this sequence:

1. `CDemoSendTables`
2. `CDemoClassInfo`
3. `CDemoPacket` with inner messages:
   - `svc_CreateStringTable`
   - `svc_UpdateStringTable`
   - `svc_PacketEntities`
   - `GE_Source1LegacyGameEvent`

Conceptually, the parser does:

1. Build entity schema from send tables.
2. Map class ids to class names.
3. Apply string table updates first so lookups are ready.
4. Decode entity deltas using schema + string table context.
5. Dispatch game event with updated context.

That ordering is the core reason replay parsing is a pipeline, not independent per-message
parsing.

## When to use this page vs other docs

- Use this page when you want the **big picture** and message roles.
- Use [Proto Field Atlas](proto-fields/index.md) when you need per-message field details.
- Use **API Reference** when you need function/class signatures.
