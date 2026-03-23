# dota_gcmessages_common_survivors.proto

- Module: `dota_gcmessages_common_survivors_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **4**
- Messages: **5** (top-level: 4)
- Enums: **1** (top-level: 0)

## Imports

- `steammessages.proto`
- `dota_shared_enums.proto`
- `dota_gcmessages_common.proto`
- `gcsdk_gcmessages.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgSurvivorsUserData</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `attribute_levels` | `.CMsgSurvivorsUserData.AttributeLevelsEntry` | `repeated` | `` |  |
| 2 | `unlocked_difficulty` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSurvivorsUserData.AttributeLevelsEntry</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSurvivorsUserData`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `key` | `int32` | `optional` | `` |  |
| 2 | `value` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCSurvivorsPowerUpTelemetryData</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `powerup_id` | `uint32` | `optional` | `` |  |
| 2 | `level` | `uint32` | `optional` | `` |  |
| 3 | `time_received` | `uint32` | `optional` | `` |  |
| 4 | `time_held` | `uint32` | `optional` | `` |  |
| 5 | `total_damage` | `uint64` | `optional` | `` |  |
| 6 | `dps` | `uint32` | `optional` | `` |  |
| 7 | `has_scepter` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCSurvivorsGameTelemetryData</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `time_survived` | `uint32` | `optional` | `` |  |
| 2 | `player_level` | `uint32` | `optional` | `` |  |
| 3 | `game_result` | `uint32` | `optional` | `` |  |
| 4 | `gold_earned` | `uint32` | `optional` | `` |  |
| 5 | `powerups` | `.CMsgClientToGCSurvivorsPowerUpTelemetryData` | `repeated` | `` |  |
| 6 | `difficulty` | `uint32` | `optional` | `` |  |
| 7 | `metaprogression_level` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCSurvivorsGameTelemetryDataResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `.CMsgClientToGCSurvivorsGameTelemetryDataResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>CMsgClientToGCSurvivorsGameTelemetryDataResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCSurvivorsGameTelemetryDataResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eNotAllowed` | 5 |
| `k_eInvalidItem` | 6 |

</details>
