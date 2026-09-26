# The Proto Files gem Uses

Valve's snapshot of Dota 2 protobuf definitions has 84 `.proto` files. gem reads
messages from 8 of them. This page explains those 8: what each one carries, which
messages gem reads, and what it does with them.

Read [How Proto Parsing Works](proto-parsing-pipeline.md) first for how a replay is
layered. For every field of every message in all 84 files, see the
[Proto Field Atlas](proto-fields/index.md).

## Where the proto files come from

Valve does not publish its `.proto` files. The community project
[SteamTracking/Protobufs](https://github.com/SteamTracking/Protobufs) extracts them
from the game files after every Dota 2 update. gem pins one snapshot of them and
commits only the Python generated from it:

1. **`proto-upstream.lock.json`** records the exact upstream commit and folder of
   the snapshot. **`scripts/download_protos.sh`** downloads its 84 `.proto` files,
   unchanged, into `proto_definitions/dota2/`. That folder is gitignored: a fresh
   clone doesn't have it, and you only need it to regenerate the Python modules or
   the [Proto Field Atlas](proto-fields/index.md).
2. **`scripts/compile_protos.py`** runs `protoc` on every file and writes the
   generated Python classes (`*_pb2.py`) and type stubs (`*_pb2.pyi`) to
   `src/gem/proto/`. A dotted file name becomes a subpackage:
   `steammessages_steamlearn.steamworkssdk.proto` becomes
   `steammessages_steamlearn/steamworkssdk_pb2.py`. Never edit the generated files
   by hand. Regenerate them instead.
3. **`.github/workflows/proto-watch.yml`** checks upstream every day. When the Dota 2
   folder changes, it downloads the new snapshot, regenerates the Python modules and
   the generated reference pages, imports every module, runs the fast test suite,
   updates the lock file, and opens (or updates) a single draft pull request.

To download the `.proto` files locally, pass the `commit` from
`proto-upstream.lock.json` (without `PROTO_UPSTREAM_REF`, the script downloads
upstream's latest `master` instead). Add the second command to regenerate the Python
modules from them:

```bash
PROTO_UPSTREAM_REF=<40-character-SHA> FORCE=1 bash scripts/download_protos.sh
uv run python scripts/compile_protos.py --force
```

## The map: all 84 files

Why does gem need only 8 of 84 files? Because Dota 2 carries on three separate
conversations, and Valve's snapshot contains the definitions for all of them:

1. **Game server ↔ players and spectators**: "a hero moved", "a tower died",
   "someone typed in chat". This is the only conversation recorded in a replay.
2. **Dota client ↔ Valve's backend, the Game Coordinator (GC)**: matchmaking,
   profiles, the store, fantasy leagues, guilds. It never happens inside a match, so
   it is not in the replay, except for the two postgame summaries the game server
   embeds at the end.
3. **Steam itself**: accounts, cloud saves, the Workshop, and the relay network
   that carries game traffic. None of it is Dota-specific.

In the tables below:

- **Used**: gem decodes messages from this file.
- **Loaded**: gem never uses it, but a used file imports it, so it is loaded
  anyway.
- **—**: not needed for replays.

This split was measured by importing the used modules and listing what Python
loaded, not by hand: 8 used and 16 loaded, 24 in total.

### Replay container (1 file)

| File | Contains | gem |
|---|---|---|
| `demo` | The outer envelopes (`EDemoCommands`, `CDemo*`) | Used |

### Source 2 engine (17 files)

These are shared by every Source 2 game, not only Dota 2.

| File | Contains | gem |
|---|---|---|
| `netmessages` | Server messages (`svc_*`): server info, string tables, entity updates, the entity schema | Used |
| `networkbasetypes` | `net_Tick`, loading messages, shared types like `CMsgVector` | Used |
| `gameevents` | Named game events (`GE_*`), including the old combat log | Used |
| `network_connection` | Disconnect reasons | Loaded |
| `source2_steam_stats` | Performance and telemetry reports | Loaded |
| `valveextensions` | Valve's custom protobuf options | Loaded |
| `usermessages` | Generic effects (`UM_*`): particles, sounds, screen shake. Present in replays, skipped | — |
| `te` | Temporary one-shot effects (`TE_*`). Present in replays, skipped | — |
| `usercmd` | A player's input: buttons, movement | — |
| `clientmessages` | Client-side UI events | — |
| `prediction_events` | Client-side prediction | — |
| `connectionless_netmessages` | The connection handshake | — |
| `c_peer2peer_netmessages` | Peer-to-peer voice and text | — |
| `networksystem_protomessages` | Low-level connection events | — |
| `engine_gcmessages` | Broadcast synchronisation | — |
| `uifontfile_format` | UI font packaging | — |

### Dota in-game (11 files)

| File | Contains | gem |
|---|---|---|
| `dota_shared_enums` | Dota's shared enums and `CMsgDOTACombatLogEntry` | Used |
| `dota_usermessages` | Dota's broadcasts (`DOTA_UM_*`): combat-log lines, chat, neutral items, effects, pings | Used |
| `dota_commonmessages` | Pings, map lines, and unit orders shared by the files above | Loaded |
| `events` | Seasonal event IDs (Diretide, The International, …) | Loaded |
| `dota_clientmessages` | What a player's client sends to the server: pings, alerts, clicks | — |
| `dota_usercmd` | Dota's version of a player input command | — |
| `dota_modifiers` | A buff/debuff entry (`CDOTAModifierBuffTableEntry`) | — |
| `dota_scenariomessages` | Saved game scenarios | — |
| `dota_broadcastmessages` | LAN lobby discovery | — |
| `dota_fighting_game_p2p_messages` | A fighting-game minigame | — |
| `dota_hud_types`, `dota_client_enums` | Enums for UI text and tournaments | — |

`dota_modifiers` does appear in replays: the entries of the `ActiveModifiers`
string table use its format. gem tracks buffs through the combat log instead.

### Game Coordinator (38 files)

| File(s) | Contains | gem |
|---|---|---|
| `dota_gcmessages_common` | Shared GC data, including `CMsgDOTAMatch`, the postgame summary | Used |
| `dota_match_metadata` | `CDOTAMatchMetadataFile`, the postgame screens' data | Used |
| `dota_gcmessages_common_lobby`, `_match_management`, `_overworld`, `_monster_hunter`, `_craftworks`, `_survivors` | Lobbies, matchmaking, and seasonal game modes, referenced by the match metadata | Loaded |
| `base_gcmessages`, `gcsdk_gcmessages` | The GC's base messages and framework | Loaded |
| `dota_gcmessages_client` and its 13 topic files (`_bingo`, `_candy_shop`, `_chat`, `_coaching`, `_craftworks`, `_fantasy`, `_guild`, `_guild_events`, `_match_management`, `_showcase`, `_team`, `_tournament`, `_watch`) | Everything the Dota client asks the backend for | — |
| `dota_gcmessages_common_battle_report`, `_bot_script`, `_fighting_game`, `_item_battler`, `_league` | Battle reports, bot scripting, minigames, leagues | — |
| `dota_gcmessages_server` | Game server ↔ GC traffic | — |
| `dota_gcmessages_webapi` | Web API data | — |
| `dota_gcmessages_msgid` | The list of GC message IDs | — |
| `econ_gcmessages`, `econ_shared_enums` | The cosmetics economy: items, trading, crafting | — |
| `event_gcmessages_client`, `_common`, `_server` | Event points | — |
| `gcsystemmsgs` | GC system message IDs | — |

### Steam platform (17 files)

| File(s) | Contains | gem |
|---|---|---|
| `steammessages` | Steam's base message header | Loaded |
| `steammessages_steamlearn.steamworkssdk`, `steammessages_unified_base.steamworkssdk` | Steam's machine-learning service; shared service options | Loaded |
| `steammessages_base`, `steammessages_int`, `steammessages_player.steamworkssdk`, `steammessages_cloud.steamworkssdk`, `steammessages_publishedfile.steamworkssdk`, `steammessages_oauth.steamworkssdk`, `steammessages_helprequest.steamworkssdk`, `steammessages_gamenetworkingui` | Accounts, friends, cloud saves, the Workshop, sign-in, support logs, network diagnostics | — |
| `steamnetworkingsockets_messages`, `_certs`, `_udp`; `steamdatagram_messages_auth`, `_sdr` | Valve's relay network that carries game traffic | — |
| `enums_clientserver` | Steam message IDs and account flags | — |

## The 8 files gem reads

| File | What gem reads | Used for |
|---|---|---|
| `demo.proto` | The outer envelopes (`CDemo*`) | Reading the file; match ID, mode, and winner |
| `netmessages.proto` | Server info, string tables, entity updates, the entity schema | Entity state, name lookups |
| `networkbasetypes.proto` | `net_Tick` | The clock |
| `gameevents.proto` | Named game events | The combat log in older replays |
| `dota_shared_enums.proto` | `CMsgDOTACombatLogEntry` | The combat log |
| `dota_usermessages.proto` | Combat-log line IDs, chat, neutral items, the postgame pair | Combat log, runes, Aegis, chat, neutral items |
| `dota_gcmessages_common.proto` | `CMsgDOTAMatch` | Valve's final numbers (duration, damage, GPM/XPM, Aghanim's) |
| `dota_match_metadata.proto` | `CDOTAMatchMetadataFile` | Skill order |

## `demo.proto`: the outer envelopes

`demo.proto` defines the envelopes a replay is packed into: which kinds exist
(`EDemoCommands`) and what each one holds (`CDemoPacket`, `CDemoFileInfo`, and so
on). It is covered in
[Stages 1 and 2](proto-parsing-pipeline.md#stage-1-outer-framing-container-layer)
of the pipeline page, because it describes the replay's structure rather than its
content.

## `netmessages.proto`: the engine's server messages

This file holds the Source 2 engine's network messages. It defines three families
of type IDs:

- `SVC_Messages` (`svc_*`): server to client. These are what a replay records.
- `CLC_Messages` (`clc_*`): client to server, such as movement, voice, or pause
  requests. A replay contains none, because spectators don't send anything.
- `Bidirectional_Messages` (`bi_*`): both directions. Also absent from replays.

gem reads five of its messages:

| Message | Arrives | What gem reads | Why |
|---|---|---|---|
| `CSVCMsg_ServerInfo` | Once, at the start | `max_classes`, `game_dir` | `max_classes` sets how many bits a class ID takes in entity data. `game_dir` contains the game build (e.g. `dota_v6808`). |
| `CSVCMsg_CreateStringTable` | About 20 times, in the signon packets before the game starts | The whole table | Creates a string table (see below) |
| `CSVCMsg_UpdateStringTable` | Tens of thousands of times | Changed rows | Keeps string tables current |
| `CSVCMsg_PacketEntities` | Once per packet | `entity_data`, `updated_entries`, `legacy_is_delta` | Entity create/update/delete. See below. |
| `CSVCMsg_FlattenedSerializer` | Once, inside the outer `DEM_SendTables` envelope | Everything | The entity schema |

**String tables** are lookup lists that the server and viewers share, like a
glossary. `CombatLogNames` turns a number into a name like `npc_dota_hero_axe`.
`instancebaseline` holds each entity class's default field values. The server
sends each table once with `CSVCMsg_CreateStringTable`, and afterwards only the
changed rows with `CSVCMsg_UpdateStringTable`. gem keeps them in
`state/string_table.py`.

**`CSVCMsg_PacketEntities`** is where protobuf stops. It has about 20 fields, but
the important one, `entity_data`, is a raw bit-packed blob in Valve's own format.
`state/entities.py` and `schema/` decode it with the schema from
`CSVCMsg_FlattenedSerializer` (see
[Stage 6](proto-parsing-pipeline.md#stage-6-where-protobuf-stops)).

**`CSVCMsg_FlattenedSerializer`** is the schema. It describes every entity class
compactly:

- `symbols`: every name, stored once and referenced by index.
- `fields`: field definitions, with type, bit count, and value range.
- `serializers`: each class as a list of field indices.

It is not sent as an inner message. It arrives inside the outer `DEM_SendTables`
envelope. `CSVCMsg_ServerInfo` arrives *before* the schema, so `parser.py` holds it
until the schema has been built (`_pending_server_info`).

**`CSVCMsg_UserMessage`** (`svc_UserMessage`, 72) is a generic wrapper: "here is a
message of type X". gem handles the combat-log IDs 468 and 470 and the match
metadata and details IDs through it. It never appeared in the replays we checked.
Current replays send every Dota message directly as its own inner type (for example
554 for combat-log lines), so the wrapper path is kept only for replays that use it.

Everything else in this file is skipped, including `svc_VoiceData`, `svc_ClassInfo`
(gem uses the outer `DEM_ClassInfo` instead), `svc_HLTVStatus`, and
`svc_ClearAllStringTables`.

## `networkbasetypes.proto`: the clock and shared building blocks

This file holds the lowest-level engine messages (`NET_Messages`, `net_*`), plus
small types that other proto files reuse: `CMsgVector` (a position), `CMsgQAngle`
(a rotation), `CMsgRGBA` (a color), and so on. It also defines the
`maximum_size_bytes` option that many messages carry, which is why almost every
other proto file imports it.

gem reads one message from it: **`CNETMsg_Tick`** (`net_Tick`, 4). Every `DEM_Packet`
and `DEM_FullPacket` contains exactly one; most signon packets contain none. gem
reads only its `tick` field. The other fields report
server performance.

That makes two clocks:

- **Replay tick**: the `tick` on each outer envelope
  ([Stage 1](proto-parsing-pipeline.md#stage-1-outer-framing-container-layer)). It starts at `0`
  when the recording starts.
- **Net tick**: `CNETMsg_Tick.tick`, the game server's own tick counter. It
  started when the server started, which was before the recording.

The difference is constant for a whole replay, and it equals
`CDemoFileHeader.server_start_tick`: 448, 391, and 1,394 in the three replays we
checked. It matters because pause fields on the game-rules entity count net ticks.
`state/game_clock.py` stores the difference as `net_tick_offset` so that pauses
line up with replay ticks. gem measures the offset from the first `net_Tick` rather
than reading the header.

`net_Tick` is also gem's "a new tick starts" signal. When it arrives, `parser.py`
updates the game clock and calls the tick-start callbacks before the packet's
entity changes are applied, matching OpenDota and Clarity (`@OnTickStart`).

The rest of `NET_Messages` in a replay is loading and setup traffic that gem skips:
`net_SpawnGroup_*` (loading map chunks), `net_SignonState`, and `net_SetConVar`.

## `gameevents.proto`: named game events (and the old combat log)

Game events are a Source 1 leftover: named events with typed keys, like
`dota_combatlog { type: 4, attackername: 12, value: 250 }`. To keep messages small,
the names are sent once and each event refers to them by number:

1. **`CMsgSource1LegacyGameEventList`** (`GE_Source1LegacyGameEventList`, 205)
   arrives once. It is the schema: every event's ID, name, and key names and types.
2. **`CMsgSource1LegacyGameEvent`** (`GE_Source1LegacyGameEvent`, 207) is one event.
   It carries only the event ID and the key values, in schema order.

`state/game_events.py` stores the schema and turns each event back into named
fields (`GameEvent.get_int32("value")`, and so on). You can subscribe to events by
name with `ReplayParser.on_game_event`.

**The old combat log lives here.** Older replays send every combat-log line as a
`dota_combatlog` game event, with names given as indexes into the `CombatLogNames`
string table. gem converts these to the same `CombatLogEntry` as the current path
(the "S1" path in `combat/log.py`).

Current replays no longer use it. In match `8855242704` the schema declares 363
event types, including `dota_combatlog`, but only three were actually sent:
`dota_chase_hero` (1,008 times, camera hints for broadcasts), `hltv_title`, and
`hltv_versioninfo`. The combat log arrives as `DOTA_UM_CombatLogDataHLTV` instead
(see `dota_shared_enums.proto` below).

The other `EBaseGameEvents` in a replay are sound events (`GE_Sos*`, about 180,000
in the same replay). gem skips them.

## `dota_shared_enums.proto`: the combat-log entry and Dota's shared vocabulary

Despite its name, this file is not only enums. It holds the numbering systems that
Dota's game server, client, and backend all share: game modes (`DOTA_GameMode`),
game phases (`DOTA_GameState`), match outcomes (`EMatchOutcome`), combat-log
types (`DOTA_COMBATLOG_TYPES`), and around 50 more, many of them about lobbies,
fantasy leagues, and the store. It also defines one message gem depends on heavily.

**`CMsgDOTACombatLogEntry` is one line of the combat log.** Each one arrives as its
own inner message, `DOTA_UM_CombatLogDataHLTV` (554). The ID is listed in
`dota_usermessages.proto`, but the message class lives here. It has 82 optional
fields, and each line fills in only the ones that apply. Here is a real hero kill
from match `8855242704`:

```text
type: 4 (DEATH)            timestamp: 973.5
attacker_name: 4           target_name: 18
is_attacker_hero: true     is_target_hero: true
attacker_team: 2           target_team: 3
assist_players: [1]        damage_type: 1
networth: 1354             last_hits: 6
```

`attacker_name` and `target_name` are **numbers, not names**. They are indexes
into the `CombatLogNames` string table (see `netmessages.proto` above), where `4` is
`npc_dota_hero_queenofpain` and `18` is `npc_dota_hero_storm_spirit`.
`combat/log.py` looks them up. The old game-event path works the same way, so both
paths produce the same `CombatLogEntry`.

What one full match contains (287,687 lines in match `8855242704`):

| `type` | Share | gem |
|---|---:|---|
| `MODIFIER_STACK_EVENT` (19) | 31.0% | Labelled `UNKNOWN`, ignored |
| `DAMAGE` (0) | 24.8% | Damage totals, per-target and per-ability breakdowns |
| `MODIFIER_ADD` / `MODIFIER_REMOVE` (2 / 3) | 27.6% | Buffs and debuffs, e.g. Smoke of Deceit |
| `HEAL` (1) | 4.6% | Healing totals |
| `XP` (10), `GOLD` (8) | 5.7% | Earnings by reason |
| `DEATH` (4) | 2.8% | Kills and deaths |
| `ABILITY` (5), `ITEM` (6) | 3.1% | Ability and item uses, ward placements |
| `PURCHASE` (11), `BUYBACK` (12) | 0.3% | Purchase log, buybacks |
| Others (`PLAYERSTATS`, `CRITICAL_DAMAGE`, `KILLSTREAK`, `GAME_STATE`, …) | 0.2% | Mostly ignored |

`CombatLogType` in `combat/log.py` lists the types gem surfaces. Every other type
becomes `UNKNOWN`, so it can't be mistaken for damage. For example,
`CRITICAL_DAMAGE` repeats damage that was already logged as a `DAMAGE` line.

**`GAME_STATE` lines mark the game's phases.** Their `value` is a `DOTA_GameState`.
The same match logged seven: strategy time, team showcase, map load, pre-game, game
in progress, post-game, and disconnect. gem watches for `type == 9`
(`DOTA_COMBATLOG_GAME_STATE`) with `value == 6`
(`DOTA_GAMERULES_STATE_POST_GAME`): the Ancient has fallen. It marks the end of
the match, which is usually minutes before the recording ends.

## `dota_usermessages.proto`: everything else Dota broadcasts

This is the biggest file gem reads from: 191 messages under `EDotaUserMessages`
(`DOTA_UM_*`, IDs 464–636). A "user message" is anything the server sends to
update the players' screens: hit effects, projectiles, minimap pings, overhead
numbers, chat lines. Most of it is visual feedback that gem doesn't need. gem
decodes six of them:

| Message (ID) | Per match | What it is | What gem does with it |
|---|---:|---|---|
| `DOTA_UM_CombatLogDataHLTV` (554) | ~290,000 | One combat-log line, as a `CMsgDOTACombatLogEntry` | The combat log (see `dota_shared_enums.proto` above) |
| `DOTA_UM_ChatEvent` (466) | ~500 | A system line in the chat box: kills, rune pickups, Aegis, glyphs, pauses | Rune pickups, Aegis events, shrine kills, Tormentor kills. Also passed to `ReplayParser.on_chat_event` |
| `DOTA_UM_ChatMessage` (612) | a few | A chat line a player typed | `ParsedMatch.chat` |
| `DOTA_UM_FoundNeutralItem` (593) | ~50 | A player received a neutral item | `ParsedMatch.neutral_item_finds` |
| `DOTA_UM_MatchMetadata` (557) | 1 | A `CDOTAMatchMetadataFile` (from `dota_match_metadata.proto`) | Stored as `ReplayParser.match_metadata` |
| `DOTA_UM_MatchDetails` (558) | 1 | A `CMsgDOTAMatch` postgame summary (from `dota_gcmessages_common.proto`) | Stored as `ReplayParser.match_details` |

**Chat events are the chat box's system lines**, not typed chat. Each
`CDOTAUserMsg_ChatEvent` has a `type` from the `DOTA_CHAT_MESSAGE` enum and up to
six player IDs plus values. In match `8855242704`, the most common were item
purchases (112), rune pickups (89), and hero kills (56). There were also Aegis
pickups, Roshan kills, Tormentor kills (`CHAT_MESSAGE_MINIBOSS_KILL`), glyphs,
pauses, and disconnects.

**Typed chat** is `CDOTAUserMsg_ChatMessage`: the player, the channel, and the
text. gem labels channel `11` (`DOTAChannelType_GameAll`) as `"all"` and channel
`12` (`DOTAChannelType_GameAllies`) as `"team"`. Any other channel keeps its raw
number as a string, for example `"13"` for spectator chat, as OpenDota does.

**Neutral items**: `CDOTAUserMsg_FoundNeutralItem` gives the player, the item's
ability ID, its tier, and any enhancement. gem looks up the item name
(`item_key`) from the ability ID in its bundled constants.

**The two postgame messages** arrive together, about 1.4 seconds after the Ancient
falls. They are summaries that the game server gets from Valve's backend, the Game
Coordinator, and embeds in the replay. The next two sections describe them.

Two older IDs, `DOTA_UM_CombatLogData` (468) and `DOTA_UM_CombatLogBulkData` (470),
carry many combat-log lines at once in a `CDOTAUserMsg_CombatLogBulkData`. gem
accepts them only inside the `svc_UserMessage` wrapper, which current replays don't
use.

## `dota_gcmessages_common.proto`: Valve's official postgame summary

Most of the 29 `dota_gcmessages_*` files describe how the Dota client talks to
Valve's backend, the Game Coordinator (GC): matchmaking, profiles, the store,
fantasy leagues. None of that happens inside a match, so it never reaches a replay.
The one exception is **`CMsgDOTAMatch`**, the match summary the GC keeps. The game
server embeds a copy in the replay as `DOTA_UM_MatchDetails` (558), about 3 KB,
right after the Ancient falls.

It has the match (duration, start time, league, teams, game mode, picks and bans,
tower and barracks status, score) and, for each player, the familiar postgame
scoreboard: K/D/A, last hits, GPM/XPM, hero and tower damage, healing, final items,
net worth, and permanent buffs.

Because these are Valve's own final numbers, gem uses them to override its
reconstructed values when they are present (`_apply_match_details_scalars` in
`results/assembly.py`):

- match `duration`
- per player: `hero_damage`, `tower_damage`, `hero_healing`, `gold_per_min`,
  `xp_per_min` (and from them, `total_gold` and `total_xp`)
- per player: `permanent_buffs`, which become OpenDota's `aghanims_scepter`,
  `aghanims_shard`, and `moonshard` flags (buff IDs 2, 12, and 1)

gem also takes `match_id` from here when `DEM_FileInfo` did not provide it.
Everything else in the summary, such as player names, items, and picks and bans, is
rebuilt from the entity stream instead, so it also works for truncated replays that
end before the summary.

## `dota_match_metadata.proto`: the postgame metadata file

**`CDOTAMatchMetadataFile`** arrives as `DOTA_UM_MatchMetadata` (557), in the same
packet as the match details. At about 85 KB it is much larger, because it holds the
data behind the postgame screens: per-team gold, XP, and net-worth graphs, per-player
item purchase times, inventory snapshots, level-up times, kill lists, ward counts,
and the equipped cosmetics.

gem uses exactly one thing from it: each player's **`ability_upgrades`**, the order
in which they skilled their abilities. It becomes `ParsedPlayer.ability_upgrades_arr`.

This file pulls in the most unused proto modules. The metadata refers to types
from seasonal events, lobbies, and other backend areas, so importing it loads 7 more
generated modules (overworld, monster hunter, survivors, craftworks, lobby, match
management, and `base_gcmessages`) that gem never uses directly.

## Files loaded only as dependencies

Importing the files above loads 24 generated modules in total, because proto files
import each other:

| Directly used | Modules loaded so far |
|---|---:|
| The six in-game files (`demo` through `dota_usermessages`) | 11 |
| + `dota_gcmessages_common` | 16 |
| + `dota_match_metadata` | 24 |

`parser.py` also imports `network_connection_pb2` and `dota_commonmessages_pb2` by
name, without using anything from them. Both are among the 11 above, imported by
`networkbasetypes.proto` and `dota_usermessages.proto`.
