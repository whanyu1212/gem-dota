# event_gcmessages_client.proto

- Module: `event_gcmessages_client_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **2**
- Messages: **3** (top-level: 3)
- Enums: **2** (top-level: 1)

## Imports

- `events.proto`
- `event_gcmessages_common.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgClientToGCGetEventPoints</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` |  | default = EVENT_ID_NONE |
| 2 | `account_id` | `uint32` | `optional` |  |  |

</details>

<details>
<summary><code>CMsgClientToGCGetEventPointsResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCGetEventPointsResponse.EResponse` | `optional` |  | default = k_eInternalError |
| 2 | `event_points` | `.CMsgUserEventPoints` | `optional` |  |  |

</details>

<details>
<summary><code>CMsgGCToClientEventPointsUpdated</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` |  | default = EVENT_ID_NONE |
| 2 | `event_points` | `.CMsgUserEventPoints` | `optional` |  |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>EGCEventClientMessages</code> — values: 3</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EMsgClientToGCGetEventPoints` | 15000 |
| `k_EMsgClientToGCGetEventPointsResponse` | 15001 |
| `k_EMsgGCToClientEventPointsUpdated` | 15002 |

</details>

<details>
<summary><code>CMsgClientToGCGetEventPointsResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCGetEventPointsResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNotAllowed` | 5 |

</details>
