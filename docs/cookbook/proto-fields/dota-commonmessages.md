# dota_commonmessages.proto

- Module: `dota_commonmessages_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **1**
- Messages: **13** (top-level: 12)
- Enums: **4** (top-level: 4)

## Imports

- `networkbasetypes.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CDOTAMsg_PingWaypointPath</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `x` | `int32` | `optional` | `` |  |
| 2 | `y` | `int32` | `optional` | `` |  |
| 3 | `grid_nav_directions` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMsg_LocationPing</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `x` | `int32` | `optional` | `` |  |
| 2 | `y` | `int32` | `optional` | `` |  |
| 3 | `target` | `int32` | `optional` | `` | default = -1 |
| 4 | `direct_ping` | `bool` | `optional` | `` |  |
| 5 | `type` | `uint32` | `optional` | `` | default = 4294967295 |
| 6 | `ping_source` | `.EPingSource` | `optional` | `` | default = k_ePingSource_Default |
| 7 | `waypoint_path` | `.CDOTAMsg_PingWaypointPath` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMsg_ItemAlert</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `x` | `int32` | `optional` | `` |  |
| 2 | `y` | `int32` | `optional` | `` |  |
| 3 | `item_ability_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAMsg_MapLine</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `x` | `int32` | `optional` | `` |  |
| 2 | `y` | `int32` | `optional` | `` |  |
| 3 | `initial` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMsg_WorldLine</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `x` | `int32` | `optional` | `` |  |
| 2 | `y` | `int32` | `optional` | `` |  |
| 3 | `z` | `int32` | `optional` | `` |  |
| 4 | `initial` | `bool` | `optional` | `` |  |
| 5 | `end` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMsg_SendStatPopup</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `style` | `.EDOTAStatPopupTypes` | `optional` | `` | default = k_EDOTA_SPT_Textline |
| 2 | `stat_strings` | `string` | `repeated` | `` |  |
| 3 | `stat_images` | `int32` | `repeated` | `` |  |
| 4 | `stat_image_types` | `int32` | `repeated` | `` |  |
| 5 | `duration` | `float` | `optional` | `` |  |
| 6 | `use_html` | `bool` | `optional` | `` |  |
| 7 | `movie_name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMsg_DismissAllStatPopups</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `time_delay` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMsg_CoachHUDPing</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `x` | `uint32` | `optional` | `` |  |
| 2 | `y` | `uint32` | `optional` | `` |  |
| 3 | `tgtpath` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAMsg_UnitOrder</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `order_type` | `.dotaunitorder_t` | `optional` | `` | default = DOTA_UNIT_ORDER_NONE |
| 3 | `units` | `int32` | `repeated` | `` |  |
| 4 | `target_index` | `int32` | `optional` | `` | default = 0 |
| 5 | `ability_index` | `int32` | `optional` | `` | default = -1 |
| 6 | `position` | `.CMsgVector` | `optional` | `` |  |
| 8 | `sequence_number` | `int32` | `optional` | `` |  |
| 9 | `flags` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>VersusScene_PlayActivity</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `activities` | `.VersusScene_PlayActivity.ActivityInfo` | `repeated` | `` |  |
| 2 | `playback_rate` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>VersusScene_PlayActivity.ActivityInfo</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `VersusScene_PlayActivity`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `activity` | `string` | `optional` | `` |  |
| 2 | `disable_auto_kill` | `bool` | `optional` | `` |  |
| 3 | `force_looping` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>VersusScene_ChatWheel</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `chat_message_id` | `uint32` | `optional` | `` | default = 4294967295 |
| 2 | `emoticon_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>VersusScene_PlaybackRate</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `rate` | `float` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>EPingSource</code> — values: 4</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_ePingSource_Default` | 0 |
| `k_ePingSource_Warning` | 1 |
| `k_ePingSource_Wheel` | 2 |
| `k_ePingSource_System` | 3 |

</details>

<details>
<summary><code>EDOTAStatPopupTypes</code> — values: 6</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EDOTA_SPT_Textline` | 0 |
| `k_EDOTA_SPT_Basic` | 1 |
| `k_EDOTA_SPT_Poll` | 2 |
| `k_EDOTA_SPT_Grid` | 3 |
| `k_EDOTA_SPT_DualImage` | 4 |
| `k_EDOTA_SPT_Movie` | 5 |

</details>

<details>
<summary><code>dotaunitorder_t</code> — values: 43</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `DOTA_UNIT_ORDER_NONE` | 0 |
| `DOTA_UNIT_ORDER_MOVE_TO_POSITION` | 1 |
| `DOTA_UNIT_ORDER_MOVE_TO_TARGET` | 2 |
| `DOTA_UNIT_ORDER_ATTACK_MOVE` | 3 |
| `DOTA_UNIT_ORDER_ATTACK_TARGET` | 4 |
| `DOTA_UNIT_ORDER_CAST_POSITION` | 5 |
| `DOTA_UNIT_ORDER_CAST_TARGET` | 6 |
| `DOTA_UNIT_ORDER_CAST_TARGET_TREE` | 7 |
| `DOTA_UNIT_ORDER_CAST_NO_TARGET` | 8 |
| `DOTA_UNIT_ORDER_CAST_TOGGLE` | 9 |
| `DOTA_UNIT_ORDER_HOLD_POSITION` | 10 |
| `DOTA_UNIT_ORDER_TRAIN_ABILITY` | 11 |
| `DOTA_UNIT_ORDER_DROP_ITEM` | 12 |
| `DOTA_UNIT_ORDER_GIVE_ITEM` | 13 |
| `DOTA_UNIT_ORDER_PICKUP_ITEM` | 14 |
| `DOTA_UNIT_ORDER_PICKUP_RUNE` | 15 |
| `DOTA_UNIT_ORDER_PURCHASE_ITEM` | 16 |
| `DOTA_UNIT_ORDER_SELL_ITEM` | 17 |
| `DOTA_UNIT_ORDER_DISASSEMBLE_ITEM` | 18 |
| `DOTA_UNIT_ORDER_MOVE_ITEM` | 19 |
| `DOTA_UNIT_ORDER_CAST_TOGGLE_AUTO` | 20 |
| `DOTA_UNIT_ORDER_STOP` | 21 |
| `DOTA_UNIT_ORDER_TAUNT` | 22 |
| `DOTA_UNIT_ORDER_BUYBACK` | 23 |
| `DOTA_UNIT_ORDER_GLYPH` | 24 |
| `DOTA_UNIT_ORDER_EJECT_ITEM_FROM_STASH` | 25 |
| `DOTA_UNIT_ORDER_CAST_RUNE` | 26 |
| `DOTA_UNIT_ORDER_PING_ABILITY` | 27 |
| `DOTA_UNIT_ORDER_MOVE_TO_DIRECTION` | 28 |
| `DOTA_UNIT_ORDER_PATROL` | 29 |
| `DOTA_UNIT_ORDER_VECTOR_TARGET_POSITION` | 30 |
| `DOTA_UNIT_ORDER_RADAR` | 31 |
| `DOTA_UNIT_ORDER_SET_ITEM_COMBINE_LOCK` | 32 |
| `DOTA_UNIT_ORDER_CONTINUE` | 33 |
| `DOTA_UNIT_ORDER_VECTOR_TARGET_CANCELED` | 34 |
| `DOTA_UNIT_ORDER_CAST_RIVER_PAINT` | 35 |
| `DOTA_UNIT_ORDER_PREGAME_ADJUST_ITEM_ASSIGNMENT` | 36 |
| `DOTA_UNIT_ORDER_DROP_ITEM_AT_FOUNTAIN` | 37 |
| `DOTA_UNIT_ORDER_TAKE_ITEM_FROM_NEUTRAL_ITEM_STASH` | 38 |
| `DOTA_UNIT_ORDER_MOVE_RELATIVE` | 39 |
| `DOTA_UNIT_ORDER_CAST_TOGGLE_ALT` | 40 |
| `DOTA_UNIT_ORDER_CONSUME_ITEM` | 41 |
| `DOTA_UNIT_ORDER_SET_ITEM_MARK_FOR_SELL` | 42 |

</details>

<details>
<summary><code>EDOTAVersusScenePlayerBehavior</code> — values: 3</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `VS_PLAYER_BEHAVIOR_PLAY_ACTIVITY` | 1 |
| `VS_PLAYER_BEHAVIOR_CHAT_WHEEL` | 2 |
| `VS_PLAYER_BEHAVIOR_PLAYBACK_RATE` | 3 |

</details>
