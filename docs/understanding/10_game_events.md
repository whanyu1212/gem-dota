# Game Events

Game events are a separate event dispatch system from the combat log. They carry
higher-level game notifications: rune pickups, aegis events, chat messages, Roshan kills,
and more.

---

## Schema registration

The game event schema arrives in an `svc_GameEventList` inner message. It defines a
mapping from **event name** to **(event_id, list of typed fields)**:

```
svc_GameEventList
  descriptors:
    - eventid: 1,  name: "dota_rune_activated_v2",  keys: [...]
    - eventid: 2,  name: "dota_player_kill",         keys: [...]
    ...
```

gem's `GameEventManager` registers this schema on startup:

```python
gem_event_manager.register_schema(schema_dict)
```

---

## Event dispatch

Game events arrive as `svc_GameEvent` inner messages (via `CMsgSource1LegacyGameEvent`):

```
svc_GameEvent
  eventid: 42
  keys:
    - type: 3 (long),  val_long: 5    ← player slot
    - type: 3 (long),  val_long: 2    ← rune type
    ...
```

gem dispatches them by name:

```python
game_event_manager.on_game_event("dota_rune_activated_v2", handler)
```

---

## Field types

Event key types:

| Integer | Type | Python accessor |
|---|---|---|
| 1 | string | `key.val_string` |
| 2 | float | `key.val_float` |
| 3 | long (int32) | `key.val_long` |
| 4 | short (int16) | `key.val_short` |
| 5 | byte (uint8) | `key.val_byte` |
| 6 | bool | `key.val_bool` |
| 7 | uint64 | `key.val_uint64` |

Note: proto attribute access only — the `CMsgSource1LegacyGameEvent.keys` items have
direct attributes (`.val_string`, `.val_long`, etc.) but no `get_val_string()` methods.

---

## CDOTAUserMsg_ChatEvent

Many gem-relevant notifications arrive as `CDOTAUserMsg_ChatEvent` user messages
(inner type 466). These are not game events in the schema sense — they are a separate
user message type. They use a `DOTA_CHAT_MESSAGE` enum to identify the notification kind:

| Chat message type | Value | What it signals |
|---|---|---|
| `CHAT_MESSAGE_RUNE_PICKUP` | 22 | A rune was picked up |
| `CHAT_MESSAGE_AEGIS` | 8 | Aegis of the Immortal picked up |
| `CHAT_MESSAGE_ROSHAN_KILL` | 9 | Roshan was killed |
| `CHAT_MESSAGE_DENIED_AEGIS` | 51 | Aegis was denied (expired) |
| `CHAT_MESSAGE_AEGIS_STOLEN` | 53 | Aegis stolen by enemy |

For rune pickups:
- `playerid_1` = player slot
- `value` = rune type integer

For Roshan kills:
- `playerid_1` = team that got the kill
- `playerid_2` = player slot of the killer

---

## Events used by gem

| Notification | Source | Handler in gem |
|---|---|---|
| Rune pickup | `CDOTAUserMsg_ChatEvent` type 466, message 22 | `players.py` |
| Aegis pickup | `CDOTAUserMsg_ChatEvent` type 466, message 8 | `match_builder.py` |
| Aegis denied | `CDOTAUserMsg_ChatEvent` type 466, message 51 | `match_builder.py` |
| Aegis stolen | `CDOTAUserMsg_ChatEvent` type 466, message 53 | `match_builder.py` |
| Roshan killed | `CDOTAUserMsg_ChatEvent` type 466, message 9 | `match_builder.py` |
| Chat message | `CDOTAUserMsg_ChatMessage` | `match_builder.py` |
| Game state | combat log `GAME_STATE` entries | `match_builder.py` |

---

## Subscribing to game events

```python
from gem.parser import ReplayParser

parser = ReplayParser("my_replay.dem")

def on_rune(event):
    player_slot, _ = event.get_long("playerid_1")
    rune_type, _   = event.get_long("value")
    print(f"tick {event.tick}: player {player_slot} picked up rune {rune_type}")

parser.on_game_event("dota_rune_activated_v2", on_rune)
parser.parse()
```

`GameEvent.get_long(name)` and friends return `(value, error_str|None)` — `error_str`
is `None` on success, a string description on failure.

---

## gem implementation

Source: `src/gem/game_events.py`

`GameEventManager`:
- `register_schema(schema_dict)` — called once with the `svc_GameEventList` data
- `on_game_event(name, handler)` — subscribe by event name
- `has_event(name)` — check if an event name is registered
- `dispatch(raw_event)` — called internally for each incoming event
