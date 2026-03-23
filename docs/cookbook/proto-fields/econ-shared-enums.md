# econ_shared_enums.proto

- Module: `econ_shared_enums_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **0**
- Messages: **1** (top-level: 1)
- Enums: **3** (top-level: 3)

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgGenericResult</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `eresult` | `uint32` | `optional` | `` | default = 2 |
| 2 | `debug_message` | `string` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>EGCEconBaseMsg</code> — values: 1</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EMsgGCGenericResult` | 2579 |

</details>

<details>
<summary><code>EGCMsgResponse</code> — values: 9</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EGCMsgResponseOK` | 0 |
| `k_EGCMsgResponseDenied` | 1 |
| `k_EGCMsgResponseServerError` | 2 |
| `k_EGCMsgResponseTimeout` | 3 |
| `k_EGCMsgResponseInvalid` | 4 |
| `k_EGCMsgResponseNoMatch` | 5 |
| `k_EGCMsgResponseUnknownError` | 6 |
| `k_EGCMsgResponseNotLoggedOn` | 7 |
| `k_EGCMsgFailedToCreate` | 8 |

</details>

<details>
<summary><code>EGCMsgUseItemResponse</code> — values: 14</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EGCMsgUseItemResponse_ItemUsed` | 0 |
| `k_EGCMsgUseItemResponse_GiftNoOtherPlayers` | 1 |
| `k_EGCMsgUseItemResponse_ServerError` | 2 |
| `k_EGCMsgUseItemResponse_MiniGameAlreadyStarted` | 3 |
| `k_EGCMsgUseItemResponse_ItemUsed_ItemsGranted` | 4 |
| `k_EGCMsgUseItemResponse_DropRateBonusAlreadyGranted` | 5 |
| `k_EGCMsgUseItemResponse_NotInLowPriorityPool` | 6 |
| `k_EGCMsgUseItemResponse_NotHighEnoughLevel` | 7 |
| `k_EGCMsgUseItemResponse_EventNotActive` | 8 |
| `k_EGCMsgUseItemResponse_ItemUsed_EventPointsGranted` | 9 |
| `k_EGCMsgUseItemResponse_MissingRequirement` | 10 |
| `k_EGCMsgUseItemResponse_EmoticonUnlock_NoNew` | 11 |
| `k_EGCMsgUseItemResponse_EmoticonUnlock_Complete` | 12 |
| `k_EGCMsgUseItemResponse_ItemUsed_Compendium` | 13 |

</details>
