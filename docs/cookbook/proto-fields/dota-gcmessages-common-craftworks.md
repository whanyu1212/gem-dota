# dota_gcmessages_common_craftworks.proto

- Module: `dota_gcmessages_common_craftworks_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **3**
- Messages: **3** (top-level: 2)
- Enums: **1** (top-level: 1)

## Imports

- `steammessages.proto`
- `dota_shared_enums.proto`
- `gcsdk_gcmessages.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgCraftworksComponents</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `component_quantities` | `.CMsgCraftworksComponents.ComponentQuantitiesEntry` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgCraftworksComponents.ComponentQuantitiesEntry</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgCraftworksComponents`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `key` | `uint32` | `optional` | `` |  |
| 2 | `value` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgCraftworksQuestReward</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `quest_id` | `uint32` | `optional` | `` |  |
| 2 | `reward_components` | `.CMsgCraftworksComponents` | `optional` | `` |  |
| 3 | `stat_value` | `uint32` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>ECraftworksAuditAction</code> — values: 4</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eInvalid` | 0 |
| `k_eRecipeCrafted` | 1 |
| `k_eMatchRewards` | 2 |
| `k_eMatchRewardsTurbo` | 3 |

</details>
