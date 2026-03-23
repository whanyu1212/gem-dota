# clientmessages.proto

- Module: `clientmessages_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **0**
- Messages: **7** (top-level: 7)
- Enums: **2** (top-level: 2)

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CClientMsg_CustomGameEvent</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_name` | `string` | `optional` | `` |  |
| 2 | `data` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CClientMsg_CustomGameEventBounce</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_name` | `string` | `optional` | `` |  |
| 2 | `data` | `bytes` | `optional` | `` |  |
| 3 | `player_slot` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CClientMsg_ClientUIEvent</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event` | `.EClientUIEvent` | `optional` | `` | default = EClientUIEvent_Invalid |
| 2 | `ent_ehandle` | `uint32` | `optional` | `` |  |
| 3 | `client_ehandle` | `uint32` | `optional` | `` |  |
| 4 | `data1` | `string` | `optional` | `` |  |
| 5 | `data2` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CClientMsg_DevPaletteVisibilityChangedEvent</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `visible` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CClientMsg_WorldUIControllerHasPanelChangedEvent</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `has_panel` | `bool` | `optional` | `` |  |
| 2 | `client_ehandle` | `uint32` | `optional` | `` |  |
| 3 | `literal_hand_type` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CClientMsg_RotateAnchor</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `angle` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CClientMsg_ListenForResponseFound</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_slot` | `int32` | `optional` | `` | default = -1 |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>EBaseClientMessages</code> — values: 8</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `CM_CustomGameEvent` | 280 |
| `CM_CustomGameEventBounce` | 281 |
| `CM_ClientUIEvent` | 282 |
| `CM_DevPaletteVisibilityChanged` | 283 |
| `CM_WorldUIControllerHasPanelChanged` | 284 |
| `CM_RotateAnchor` | 285 |
| `CM_ListenForResponseFound` | 286 |
| `CM_MAX_BASE` | 300 |

</details>

<details>
<summary><code>EClientUIEvent</code> — values: 3</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `EClientUIEvent_Invalid` | 0 |
| `EClientUIEvent_DialogFinished` | 1 |
| `EClientUIEvent_FireOutput` | 2 |

</details>
