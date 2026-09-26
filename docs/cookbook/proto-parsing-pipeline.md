# How Proto Parsing Works

This page explains replay parsing as a pipeline of transformations.

Goal: start with a `.dem` replay file and end with structured events, entities, and match
metadata.

You do **not** need to know bit math to follow this. We will focus on concepts first.

If you want a quick binary-format foundation first, read
[Bits & Bytes Primer](bits-and-bytes-primer.md).

## What protobuf is

Almost everything in a replay is encoded with **Protocol Buffers** ("protobuf"),
Google's format for sending structured data compactly. Both sides share a schema,
written in a `.proto` file. Here is part of one from `demo.proto`:

```proto
message CDemoFileHeader {
    required string demo_file_stamp = 1;
    optional int32 patch_version = 2;
    optional string map_name = 5;
}
```

The number after each field is its **tag**. The encoded bytes contain only tags and
values, never field names. A reader needs the same `.proto` file to know that tag
`5` means `map_name`. It works like a form with numbered boxes and the legend printed
separately.

This has three consequences for replay parsing:

- **It is compact.** Numbers instead of names keep a replay's millions of messages
  small.
- **Old readers keep working.** A reader skips tags it doesn't know. Valve adds
  fields over time, and gem's generated code still reads new replays; it just
  doesn't see the new fields until the definitions are refreshed.
- **Messages don't say what they are.** The bytes of a `CDemoFileHeader` don't
  contain the name `CDemoFileHeader`. Something outside the message has to say which
  type it is. In a replay, that is the numeric `command` on each envelope (Stage 1)
  and the `type_id` on each inner message (Stage 3).

`protoc`, the protobuf compiler, turns each `.proto` file into Python classes:

```python
from gem.proto.demo_pb2 import CDemoFileHeader

header = CDemoFileHeader()
header.ParseFromString(payload)  # payload: bytes known to be a file header
header.map_name
```

[The Proto Files gem Uses](proto-files.md) explains where gem's 84 `.proto` files
come from and which ones matter.

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

Think of a replay as a long stack of envelopes. Stage 1 reads the label on each
envelope without opening it.

The file starts with a 16-byte header, before the first envelope:

| Bytes | Contents | What gem does |
|---|---|---|
| 0–7 | Magic `PBDEMS2\0`: "this is a Source 2 demo" | Checks it and rejects anything else |
| 8–11 | Little-endian int32: byte offset of the `DEM_FileInfo` envelope at the end of the file | Skips it |
| 12–15 | Little-endian int32: byte offset of the `DEM_SpawnGroups` envelope near the end | Skips it |

Clarity uses the first offset to jump straight to the end-of-file summary. Manta
and gem skip both, and a truncated replay shows why: its header still points at
envelopes that were cut off.

After the header, the envelopes follow one after another. Each one is:

```text
command (varuint32) | tick (varuint32) | size (varuint32) | payload (size bytes)
```

- **`command`** says what kind of envelope this is: an `EDemoCommands` value from
  `demo.proto`. If bit `64` (`DEM_IsCompressed`) is set, the payload is
  Snappy-compressed.
- **`tick`** is when the envelope was recorded. The game runs at 30 ticks per
  second. The value `0xFFFFFFFF` means "before the game started", and gem stores
  it as `0`.
- **`size`** is the payload length in bytes.

`binary/stream.py` reads these labels, strips the compression bit, decompresses the
payload, and yields `(tick, msg_type, payload)`. It knows nothing about protobuf.

## Stage 2: Outer protobuf decode (envelope layer)

Now each envelope is opened. `command` says which `CDemo*` message from
`demo.proto` the payload is.

Here is every envelope in one real replay (match `8855242704`, a 99.6-minute
recording). Sizes are after decompression.

| Envelope (`command`) | Count | Payload size | When | What's inside | gem |
|---|---:|---:|---|---|---|
| `DEM_FileHeader` (1) | 1 | 203 B | Start | Server name, build number, demo format version | Skips |
| `DEM_SignonPacket` (8) | 10 | 251 KB | Start | Setup traffic sent before the game begins. Same format as `DEM_Packet` | Reads |
| `DEM_SendTables` (4) | 1 | 837 KB | Start | The entity schema: which fields a hero, tower, or item has | Reads |
| `DEM_ClassInfo` (5) | 1 | 135 KB | Start | Class ID → class name, e.g. which ID means `CDOTA_Unit_Hero_Axe` | Reads |
| `DEM_StringTables` (6) | 1 | 307 KB | Start | Snapshot of the string tables | Skips |
| `DEM_SyncTick` (3) | 1 | 0 B | Start | Empty marker: setup is done | Skips |
| `DEM_Recovery` (18) | 2 | 118 B | Start | Spawn-group recovery data | Skips |
| **`DEM_Packet` (7)** | **89,592** | **291 MB** | About every 2 ticks | **The game itself**: a bundle of inner messages (Stage 3) | Reads |
| `DEM_FullPacket` (13) | 100 | 24 MB | Every 1,800 ticks (60 s) | Checkpoint: a string-table snapshot plus a packet | Reads the packet |
| `DEM_Stop` (0) | 1 | 0 B | End | "Recording over" | Skips |
| `DEM_SpawnGroups` (15) | 1 | 112 B | End | Map-chunk loading data | Skips |
| **`DEM_FileInfo` (2)** | 1 | 763 B | **End** | **Match summary**: match ID, game mode, league, winner, players, picks and bans | Reads part of it |

The other `EDemoCommands` values (`DEM_ConsoleCmd`, `DEM_CustomData`,
`DEM_CustomDataCallbacks`, `DEM_UserCmd`, `DEM_SaveGame`, `DEM_AnimationData`,
`DEM_AnimationHeader`) do not appear in this replay, and gem ignores them.
`DEM_Error`, `DEM_Max`, and `DEM_IsCompressed` are markers, not envelope kinds.

Three things to take from this table:

1. **Packets are the game.** Almost every envelope is a `DEM_Packet`, and packets
   carry about 92% of the bytes. Everything else is setup at the start or a summary
   at the end.
2. **Full packets are checkpoints.** A packet only says what *changed*, so knowing
   the state at minute 40 means replaying minutes 0–39. A full packet is a saved
   state every 60 seconds, so a replay viewer can jump around. gem always reads from
   start to finish, so it opens the `packet` inside a full packet like any other
   packet and ignores the `string_table` snapshot, as Manta does.
3. **The summary comes last.** `DEM_FileInfo` is written when the recording ends.
   gem reads `match_id`, `game_mode`, `leagueid`, and `game_winner` from it. The
   players, picks and bans, and team tags come from the entity stream instead. A
   truncated replay has no summary, so after the loop `parser.py` reads the same
   facts from the `CDOTAGamerulesProxy` entity.

Where this happens:

- `ReplayParser._dispatch_outer` in `parser.py` chooses the `CDemo*` class for
  the five kinds gem reads and drops the rest.
- `CDemoSendTables.data` holds another length-prefixed protobuf,
  `CSVCMsg_FlattenedSerializer` from `netmessages.proto`.
  `schema/sendtable/parser.py` unwraps it.
- `CDemoPacket.data` holds the inner messages. That's Stage 3.

## Stage 3: Inner message unpack (packet multiplexing layer)

`CDemoPacket.data` is not one message. It is a bundle of small inner messages packed
back to back:

```text
{ type_id, size, payload } { type_id, size, payload } ...
```

`type_id` is a `ubit_var` (a variable-length bit field) and `size` is a varuint32.
`parser.py` (`_read_inner_messages`) splits the bundle into `(type_id, payload)`
pairs.

Each inner message is what the game server sent to spectators at that moment. A
replay is that broadcast, saved to disk. The type IDs come from enums spread across
several proto files, so one packet mixes messages from all of them:

| Type IDs | Enum | Defined in | Examples |
|---|---|---|---|
| 0–15 | `NET_Messages` | `networkbasetypes.proto` | `net_Tick` |
| 40–77 | `SVC_Messages` | `netmessages.proto` | `svc_PacketEntities`, `svc_UpdateStringTable` |
| 101–200 | `EBaseUserMessages` | `usermessages.proto` | `UM_ParticleManager` |
| 200–214 | `EBaseGameEvents` | `gameevents.proto` | `GE_Source1LegacyGameEvent` |
| 400–426 | `ETEProtobufIds` | `te.proto` | `TE_EffectDispatchId` |
| 464–636 | `EDotaUserMessages` | `dota_usermessages.proto` | `DOTA_UM_CombatLogDataHLTV` |

Here is what the same replay as Stage 2 (match `8855242704`) carries: 89,702 packets
holding 2.48 million inner messages.

| Inner message (`type_id`) | Count | Share of bytes | gem |
|---|---:|---:|---|
| **`svc_PacketEntities` (55)** | 89,692 | **42.3%** | Reads: entity changes, one per packet |
| `svc_VoiceData` (47) | 1,001,802 | 37.6% | Skips: voice chat audio |
| `DOTA_UM_CombatLogDataHLTV` (554) | 287,687 | 6.5% | Reads: one combat-log line each |
| `svc_UpdateStringTable` (45) | 57,910 | 4.4% | Reads |
| `net_Tick` (4) | 89,693 | 0.4% | Reads: the clock |
| Everything else (player orders, particles, sounds, animations, pings, chat, …) | 952,483 | 8.7% | Mostly skips |

Voice chat takes almost as many bytes as the whole game state, and gem never
decodes it.

### Processing order within a packet

The messages in one packet all belong to the same moment, but some depend on
others. For example, a combat-log line names a hero by string-table index, so the
string table must be up to date first. Before dispatching, gem sorts each packet:

1. First: `net_Tick`, `svc_ServerInfo`, `svc_CreateStringTable`,
   `svc_UpdateStringTable`. These give context.
2. Then everything not listed here.
3. Then `svc_PacketEntities`. Entity changes are applied with that context.
4. Last: `GE_Source1LegacyGameEvent` and `DOTA_UM_CombatLogDataHLTV`. Events are
   read after the entities they mention are up to date.

Manta sorts the same way (`demo_packet.go`). The difference is which messages it
puts first: it includes `net_SpawnGroup_Load` instead of `svc_ServerInfo`, and it
does not delay the combat-log message.

## Stage 4: Inner protobuf decode (semantic layer)

`parser.py` (`ReplayParser._dispatch_inner`) decodes each inner message whose
`type_id` it knows, using the matching protobuf class. Every other message is
skipped without being decoded.

gem decodes inner messages from seven proto files:

| File | Inner messages gem decodes |
|---|---|
| `netmessages.proto` | `svc_ServerInfo`, `svc_CreateStringTable`, `svc_UpdateStringTable`, `svc_PacketEntities` |
| `networkbasetypes.proto` | `net_Tick` |
| `gameevents.proto` | `GE_Source1LegacyGameEventList`, `GE_Source1LegacyGameEvent` |
| `dota_shared_enums.proto` | `CMsgDOTACombatLogEntry`, sent as `DOTA_UM_CombatLogDataHLTV` |
| `dota_usermessages.proto` | `DOTA_UM_ChatEvent`, `DOTA_UM_ChatMessage`, `DOTA_UM_FoundNeutralItem` |
| `dota_match_metadata.proto` | `CDOTAMatchMetadataFile`, sent as `DOTA_UM_MatchMetadata` |
| `dota_gcmessages_common.proto` | `CMsgDOTAMatch`, sent as `DOTA_UM_MatchDetails` |

[The Proto Files gem Uses](proto-files.md) explains each file: what it carries,
what gem reads from it, and what gem does with it.

## Stage 5: Subsystem routing (state-building layer)

Each decoded message is handed to the part of gem that owns that kind of state:

| Message | Handled by | What it builds |
|---|---|---|
| `DEM_SendTables` (`CSVCMsg_FlattenedSerializer`) | `schema/sendtable/` | The serializer tree: every entity class and its fields |
| `DEM_ClassInfo` | `state/entities.py` | Class ID → class name and serializer |
| `svc_CreateStringTable`, `svc_UpdateStringTable` | `state/string_table.py` | Lookup tables such as `CombatLogNames` and the `instancebaseline` entity defaults |
| `svc_PacketEntities` | `state/entities.py` (with `schema/field_path/` and `schema/field_decoder/`) | The live entity table: every hero, building, item, and ward, with current field values |
| `net_Tick` | `parser.py`, `state/game_clock.py` | The clock, pauses, and tick-start callbacks |
| `GE_Source1LegacyGameEvent` | `state/game_events.py`, then `combat/log.py` for `dota_combatlog` | Named events and the old combat log |
| `DOTA_UM_CombatLogDataHLTV` | `combat/log.py` | `CombatLogEntry` records |
| `DOTA_UM_ChatEvent` | `combat/log.py` (rune pickups), `extractors/objectives.py` (Aegis, shrines, Tormentors) | Events the combat log does not attribute |
| `DOTA_UM_ChatMessage`, `DOTA_UM_FoundNeutralItem` | Callbacks collected in `api.py` | `ParsedMatch.chat`, `ParsedMatch.neutral_item_finds` |
| `DOTA_UM_MatchDetails`, `DOTA_UM_MatchMetadata` | Stored on the parser, read by `results/assembly.py` | Valve's final numbers and skill order |

Parsing is **incremental state reconstruction**. No single message says "the
state of the game at minute 20". Each one changes what the earlier messages built.
The extractors (`extractors/`) watch that state as it changes, for example sampling
every hero's gold and position, and `results/assembly.py` turns what they
collected into a `ParsedMatch` at the end.

## Stage 6: Where protobuf stops

"If everything is protobuf, why does gem need its own bit reader?" Because the most
important protobuf fields contain raw bytes in formats Valve designed for size, and
protobuf can't decode those.

The main one is **`CSVCMsg_PacketEntities.entity_data`**: every entity change, packed
at the bit level. For each changed entity it holds:

1. **Which entity**: the distance from the previous changed entity's index, as a
   `ubit_var`.
2. **What happened**, in 2 bits: update, create, leave (still exists, but out of
   view), or delete.
3. **For a create**: the class ID and a serial number. gem first applies the
   class's defaults from the `instancebaseline` string table.
4. **Which fields changed and their new values.** Fields are addressed by *field
   paths*, compressed with a Huffman code (`schema/field_path/`). Each value is
   decoded according to its field's type in the schema: a quantized float, a
   varint, a string, and so on (`schema/field_decoder/`).

Nothing in this blob is labelled. Without the schema from `DEM_SendTables`, it's
just bits. That's why the schema has to arrive before the first entity update.

String tables work the same way on a smaller scale: `CSVCMsg_CreateStringTable`
and `CSVCMsg_UpdateStringTable` are protobuf, but their `string_data` is a
bit-packed list of entries, sometimes Snappy-compressed (`state/string_table.py`).

So parsing a replay uses two kinds of decoding:

- **protobuf** for the structure of messages
- **gem's own bit-level decoding** (`binary/reader.py`, `schema/`, `state/`) for the
  packed game state inside them

## A worked example: first blood

Here is a real packet from match `8855242704`: the one containing first blood, at
replay tick 28,757. It is a 4.7 KB `DEM_Packet` with 56 inner messages. In the
order they appear on the wire:

| Position | Inner messages | gem |
|---|---|---|
| 1–40 | Combat-log lines (damage, gold, XP, first blood, the death), 2 chat events (the hero kill and first blood), animations, particles, sounds, overhead numbers | Reads the combat log and chat events. Skips the rest |
| 41 | `net_Tick`: net tick 29,205 (29,205 − 28,757 = 448, the offset from Stage 1's header) | Reads |
| 42–43 | 2 × `svc_UpdateStringTable` | Reads |
| 44 | `svc_PacketEntities`: 170 entities changed, in 1,423 bytes of `entity_data` | Reads |
| 45–56 | 12 × `svc_VoiceData` | Skips |

The combat-log death line comes *before* the clock tick and the entity update. If
gem processed messages in wire order, it would record the death before advancing
the clock or updating the entities. So gem sorts the packet first (Stage 3):

1. `net_Tick` advances the clock, and `svc_UpdateStringTable` updates the name
   lookups.
2. The chat events are handled: the hero kill and first blood.
3. `svc_PacketEntities` applies the 170 entity changes, including the dying hero.
4. Last, the combat-log lines are read. The death line's `attacker_name` and
   `target_name` are resolved through the up-to-date `CombatLogNames` table, and the
   entities they refer to are already in their state for this tick.

This ordering is why replay parsing is a pipeline, and not a set of independent
per-message decoders.

## When to use this page vs other docs

- Use this page when you want the **big picture** and message roles.
- Use [The Proto Files gem Uses](proto-files.md) for what each relevant proto file
  carries and what gem does with it.
- Use [Proto Field Atlas](proto-fields/index.md) when you need per-message field details.
- Use the [API Reference](../reference/index.md) when you need function and class
  signatures.
