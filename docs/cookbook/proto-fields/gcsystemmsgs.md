# gcsystemmsgs.proto

- Module: `gcsystemmsgs_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **0**
- Messages: **0** (top-level: 0)
- Enums: **2** (top-level: 2)

## Messages

Expand any message to inspect all fields.

*(No messages in this proto file.)*

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>ESOMsg</code> — values: 8</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_ESOMsg_Create` | 21 |
| `k_ESOMsg_Update` | 22 |
| `k_ESOMsg_Destroy` | 23 |
| `k_ESOMsg_CacheSubscribed` | 24 |
| `k_ESOMsg_CacheUnsubscribed` | 25 |
| `k_ESOMsg_UpdateMultiple` | 26 |
| `k_ESOMsg_CacheSubscriptionRefresh` | 28 |
| `k_ESOMsg_CacheSubscribedUpToDate` | 29 |

</details>

<details>
<summary><code>EGCBaseClientMsg</code> — values: 13</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EMsgGCPingRequest` | 3001 |
| `k_EMsgGCPingResponse` | 3002 |
| `k_EMsgGCToClientPollConvarRequest` | 3003 |
| `k_EMsgGCToClientPollConvarResponse` | 3004 |
| `k_EMsgGCCompressedMsgToClient` | 3005 |
| `k_EMsgGCCompressedMsgToClient_Legacy` | 523 |
| `k_EMsgGCToClientRequestDropped` | 3006 |
| `k_EMsgGCClientWelcome` | 4004 |
| `k_EMsgGCServerWelcome` | 4005 |
| `k_EMsgGCClientHello` | 4006 |
| `k_EMsgGCServerHello` | 4007 |
| `k_EMsgGCClientConnectionStatus` | 4009 |
| `k_EMsgGCServerConnectionStatus` | 4010 |

</details>
