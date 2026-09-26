# steammessages_oauth.steamworkssdk.proto

**Not used by gem**: nothing in this file is needed to parse a replay. See [the map of all 84 files](../proto-files.md#the-map-all-84-files) for what it belongs to.

- Module: `steammessages_oauth.steamworkssdk_pb2`
- Imports: **1**
- Messages: **2** (top-level: 2)
- Enums: **0** (top-level: 0)

## Imports

- `steammessages_unified_base.steamworkssdk.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>COAuthToken_ImplicitGrantNoPrompt_Request</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `clientid` | `string` | `optional` |  | (description) = "Client ID for which to count the number of issued tokens" |

</details>

<details>
<summary><code>COAuthToken_ImplicitGrantNoPrompt_Response</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `access_token` | `string` | `optional` |  | (description) = "OAuth Token, granted on success" |
| 2 | `redirect_uri` | `string` | `optional` |  | (description) = "Redirection URI provided during client registration." |

</details>

## Enums

Expand any enum to inspect all values.

*(No enums in this proto file.)*
