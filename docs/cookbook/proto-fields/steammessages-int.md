# steammessages_int.proto

- Module: `steammessages_int_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **1**
- Messages: **82** (top-level: 64)
- Enums: **3** (top-level: 0)

## Imports

- `steammessages.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgWebAPIKey</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `status` | `uint32` | `optional` | `` | default = 255 |
| 2 | `account_id` | `uint32` | `optional` | `` | default = 0 |
| 3 | `publisher_group_id` | `uint32` | `optional` | `` | default = 0 |
| 4 | `key_id` | `uint32` | `optional` | `` |  |
| 5 | `domain` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgHttpRequest</code> — fields: 9; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `request_method` | `uint32` | `optional` | `` |  |
| 2 | `hostname` | `string` | `optional` | `` |  |
| 3 | `url` | `string` | `optional` | `` |  |
| 4 | `headers` | `.CMsgHttpRequest.RequestHeader` | `repeated` | `` |  |
| 5 | `get_params` | `.CMsgHttpRequest.QueryParam` | `repeated` | `` |  |
| 6 | `post_params` | `.CMsgHttpRequest.QueryParam` | `repeated` | `` |  |
| 7 | `body` | `bytes` | `optional` | `` |  |
| 8 | `absolute_timeout` | `uint32` | `optional` | `` |  |
| 9 | `use_https` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgHttpRequest.RequestHeader</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgHttpRequest`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `value` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgHttpRequest.QueryParam</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgHttpRequest`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `value` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgWebAPIRequest</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `interface_name` | `string` | `optional` | `` |  |
| 3 | `method_name` | `string` | `optional` | `` |  |
| 4 | `version` | `uint32` | `optional` | `` |  |
| 5 | `api_key` | `.CMsgWebAPIKey` | `optional` | `` |  |
| 6 | `request` | `.CMsgHttpRequest` | `optional` | `` |  |
| 7 | `routing_app_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgHttpResponse</code> — fields: 3; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `status_code` | `uint32` | `optional` | `` |  |
| 2 | `headers` | `.CMsgHttpResponse.ResponseHeader` | `repeated` | `` |  |
| 3 | `body` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgHttpResponse.ResponseHeader</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgHttpResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `value` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgAMFindAccounts</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `search_type` | `uint32` | `optional` | `` |  |
| 2 | `search_string` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgAMFindAccountsResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steam_id` | `fixed64` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgNotifyWatchdog</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `source` | `uint32` | `optional` | `` |  |
| 2 | `alert_type` | `uint32` | `optional` | `` |  |
| 4 | `critical` | `bool` | `optional` | `` |  |
| 5 | `time` | `uint32` | `optional` | `` |  |
| 6 | `appid` | `uint32` | `optional` | `` |  |
| 7 | `text` | `string` | `optional` | `` |  |
| 12 | `recipient` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgAMGetLicenses</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steamid` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPackageLicense</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `package_id` | `uint32` | `optional` | `` |  |
| 2 | `time_created` | `uint32` | `optional` | `` |  |
| 3 | `owner_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgAMGetLicensesResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `license` | `.CMsgPackageLicense` | `repeated` | `` |  |
| 2 | `result` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCGetCommandList</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `app_id` | `uint32` | `optional` | `` |  |
| 2 | `command_prefix` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCGetCommandListResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `command_name` | `string` | `repeated` | `` |  |

</details>

<details>
<summary><code>CGCMsgMemCachedGet</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `keys` | `string` | `repeated` | `` |  |

</details>

<details>
<summary><code>CGCMsgMemCachedGetResponse</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `values` | `.CGCMsgMemCachedGetResponse.ValueTag` | `repeated` | `` |  |

</details>

<details>
<summary><code>CGCMsgMemCachedGetResponse.ValueTag</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CGCMsgMemCachedGetResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `found` | `bool` | `optional` | `` |  |
| 2 | `value` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CGCMsgMemCachedSet</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `keys` | `.CGCMsgMemCachedSet.KeyPair` | `repeated` | `` |  |

</details>

<details>
<summary><code>CGCMsgMemCachedSet.KeyPair</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CGCMsgMemCachedSet`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `value` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CGCMsgMemCachedDelete</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `keys` | `string` | `repeated` | `` |  |

</details>

<details>
<summary><code>CGCMsgMemCachedStats</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CGCMsgMemCachedStatsResponse</code> — fields: 14; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `curr_connections` | `uint64` | `optional` | `` |  |
| 2 | `cmd_get` | `uint64` | `optional` | `` |  |
| 3 | `cmd_set` | `uint64` | `optional` | `` |  |
| 4 | `cmd_flush` | `uint64` | `optional` | `` |  |
| 5 | `get_hits` | `uint64` | `optional` | `` |  |
| 6 | `get_misses` | `uint64` | `optional` | `` |  |
| 7 | `delete_hits` | `uint64` | `optional` | `` |  |
| 8 | `delete_misses` | `uint64` | `optional` | `` |  |
| 9 | `bytes_read` | `uint64` | `optional` | `` |  |
| 10 | `bytes_written` | `uint64` | `optional` | `` |  |
| 11 | `limit_maxbytes` | `uint64` | `optional` | `` |  |
| 12 | `curr_items` | `uint64` | `optional` | `` |  |
| 13 | `evictions` | `uint64` | `optional` | `` |  |
| 14 | `bytes` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CGCMsgSQLStats</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `schema_catalog` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CGCMsgSQLStatsResponse</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `threads` | `uint32` | `optional` | `` |  |
| 2 | `threads_connected` | `uint32` | `optional` | `` |  |
| 3 | `threads_active` | `uint32` | `optional` | `` |  |
| 4 | `operations_submitted` | `uint32` | `optional` | `` |  |
| 5 | `prepared_statements_executed` | `uint32` | `optional` | `` |  |
| 6 | `non_prepared_statements_executed` | `uint32` | `optional` | `` |  |
| 7 | `deadlock_retries` | `uint32` | `optional` | `` |  |
| 8 | `operations_timed_out_in_queue` | `uint32` | `optional` | `` |  |
| 9 | `errors` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgAMAddFreeLicense</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steamid` | `fixed64` | `optional` | `` |  |
| 2 | `ip_public` | `uint32` | `optional` | `` |  |
| 3 | `packageid` | `uint32` | `optional` | `` |  |
| 4 | `store_country_code` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgAMAddFreeLicenseResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `eresult` | `int32` | `optional` | `` | default = 2 |
| 2 | `purchase_result_detail` | `int32` | `optional` | `` |  |
| 3 | `transid` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CGCMsgGetIPLocation</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ips` | `fixed32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CGCMsgGetIPASN</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ips` | `fixed32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CIPASNInfo</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ip` | `fixed32` | `optional` | `` |  |
| 2 | `asn` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CGCMsgGetIPASNResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `infos` | `.CIPASNInfo` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgAMSendEmail</code> — fields: 6; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steamid` | `fixed64` | `optional` | `` |  |
| 2 | `email_msg_type` | `uint32` | `optional` | `` |  |
| 3 | `email_format` | `uint32` | `optional` | `` |  |
| 5 | `persona_name_tokens` | `.CMsgAMSendEmail.PersonaNameReplacementToken` | `repeated` | `` |  |
| 6 | `source_gc` | `uint32` | `optional` | `` |  |
| 7 | `tokens` | `.CMsgAMSendEmail.ReplacementToken` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgAMSendEmail.ReplacementToken</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgAMSendEmail`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `token_name` | `string` | `optional` | `` |  |
| 2 | `token_value` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgAMSendEmail.PersonaNameReplacementToken</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgAMSendEmail`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steamid` | `fixed64` | `optional` | `` |  |
| 2 | `token_name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgAMSendEmailResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `eresult` | `uint32` | `optional` | `` | default = 2 |

</details>

<details>
<summary><code>CMsgGCGetEmailTemplate</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `app_id` | `uint32` | `optional` | `` |  |
| 2 | `email_msg_type` | `uint32` | `optional` | `` |  |
| 3 | `email_lang` | `int32` | `optional` | `` |  |
| 4 | `email_format` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCGetEmailTemplateResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `eresult` | `uint32` | `optional` | `` | default = 2 |
| 2 | `template_exists` | `bool` | `optional` | `` |  |
| 3 | `template` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgAMGrantGuestPasses2</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steam_id` | `fixed64` | `optional` | `` |  |
| 2 | `package_id` | `uint32` | `optional` | `` |  |
| 3 | `passes_to_grant` | `int32` | `optional` | `` |  |
| 4 | `days_to_expiration` | `int32` | `optional` | `` |  |
| 5 | `action` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgAMGrantGuestPasses2Response</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `eresult` | `int32` | `optional` | `` | default = 2 |
| 2 | `passes_granted` | `int32` | `optional` | `` | default = 0 |

</details>

<details>
<summary><code>CMsgGCGetPersonaNames</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steamids` | `fixed64` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCGetPersonaNames_Response</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `succeeded_lookups` | `.CMsgGCGetPersonaNames_Response.PersonaName` | `repeated` | `` |  |
| 2 | `failed_lookup_steamids` | `fixed64` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCGetPersonaNames_Response.PersonaName</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCGetPersonaNames_Response`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steamid` | `fixed64` | `optional` | `` |  |
| 2 | `persona_name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCCheckFriendship</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steamid_left` | `fixed64` | `optional` | `` |  |
| 2 | `steamid_right` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCCheckFriendship_Response</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `success` | `bool` | `optional` | `` |  |
| 2 | `found_friendship` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCGetAppFriendsList</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steamid` | `fixed64` | `optional` | `` |  |
| 2 | `include_friendship_timestamps` | `bool` | `optional` | `` |  |
| 3 | `include_friends_with_no_play_time` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCGetAppFriendsList_Response</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `success` | `bool` | `optional` | `` |  |
| 2 | `steamids` | `fixed64` | `repeated` | `` |  |
| 3 | `friendship_timestamps` | `fixed32` | `repeated` | `` |  |
| 4 | `last_playtimes` | `fixed32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCMsgMasterSetDirectory</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `master_dir_index` | `int32` | `optional` | `` | default = -1 |
| 2 | `dir` | `.CMsgGCMsgMasterSetDirectory.SubGC` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCMsgMasterSetDirectory.SubGC</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCMsgMasterSetDirectory`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `dir_index` | `int32` | `optional` | `` | default = -1 |
| 2 | `name` | `string` | `optional` | `` |  |
| 3 | `box` | `string` | `optional` | `` |  |
| 4 | `command_line` | `string` | `optional` | `` |  |
| 5 | `gc_binary` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCMsgMasterSetDirectory_Response</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `eresult` | `int32` | `optional` | `` | default = 2 |
| 2 | `message` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCMsgWebAPIJobRequestForwardResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `dir_index` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CGCSystemMsg_GetPurchaseTrust_Request</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steamid` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CGCSystemMsg_GetPurchaseTrust_Response</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `has_prior_purchase_history` | `bool` | `optional` | `` |  |
| 2 | `has_no_recent_password_resets` | `bool` | `optional` | `` |  |
| 3 | `is_wallet_cash_trusted` | `bool` | `optional` | `` |  |
| 4 | `time_all_trusted` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCHAccountVacStatusChange</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steam_id` | `fixed64` | `optional` | `` |  |
| 2 | `app_id` | `uint32` | `optional` | `` |  |
| 3 | `rtime_vacban_starts` | `uint32` | `optional` | `` |  |
| 4 | `is_banned_now` | `bool` | `optional` | `` |  |
| 5 | `is_banned_future` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCRoutingInfo</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `dir_index` | `int32` | `repeated` | `` |  |
| 2 | `method` | `.CMsgGCRoutingInfo.RoutingMethod` | `optional` | `` | default = RANDOM |
| 3 | `fallback` | `.CMsgGCRoutingInfo.RoutingMethod` | `optional` | `` | default = DISCARD |
| 4 | `protobuf_field` | `uint32` | `optional` | `` |  |
| 5 | `webapi_param` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCMsgMasterSetWebAPIRouting</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `entries` | `.CMsgGCMsgMasterSetWebAPIRouting.Entry` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCMsgMasterSetWebAPIRouting.Entry</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCMsgMasterSetWebAPIRouting`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `interface_name` | `string` | `optional` | `` |  |
| 2 | `method_name` | `string` | `optional` | `` |  |
| 3 | `routing` | `.CMsgGCRoutingInfo` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCMsgMasterSetClientMsgRouting</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `entries` | `.CMsgGCMsgMasterSetClientMsgRouting.Entry` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCMsgMasterSetClientMsgRouting.Entry</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCMsgMasterSetClientMsgRouting`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `msg_type` | `uint32` | `optional` | `` |  |
| 2 | `routing` | `.CMsgGCRoutingInfo` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCMsgMasterSetWebAPIRouting_Response</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `eresult` | `int32` | `optional` | `` | default = 2 |

</details>

<details>
<summary><code>CMsgGCMsgMasterSetClientMsgRouting_Response</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `eresult` | `int32` | `optional` | `` | default = 2 |

</details>

<details>
<summary><code>CMsgGCMsgSetOptions</code> — fields: 3; oneofs: 0; nested messages: 1; nested enums: 2</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `options` | `.CMsgGCMsgSetOptions.Option` | `repeated` | `` |  |
| 2 | `client_msg_ranges` | `.CMsgGCMsgSetOptions.MessageRange` | `repeated` | `` |  |
| 3 | `gcsql_version` | `.CMsgGCMsgSetOptions.GCSQLVersion` | `optional` | `` | default = GCSQL_VERSION_BASELINE |

</details>

<details>
<summary><code>CMsgGCMsgSetOptions.MessageRange</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCMsgSetOptions`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `low` | `uint32` | `required` | `` |  |
| 2 | `high` | `uint32` | `required` | `` |  |

</details>

<details>
<summary><code>CMsgGCHUpdateSession</code> — fields: 9; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steam_id` | `fixed64` | `optional` | `` |  |
| 2 | `app_id` | `uint32` | `optional` | `` |  |
| 3 | `online` | `bool` | `optional` | `` |  |
| 4 | `server_steam_id` | `fixed64` | `optional` | `` |  |
| 5 | `server_addr` | `uint32` | `optional` | `` |  |
| 6 | `server_port` | `uint32` | `optional` | `` |  |
| 7 | `os_type` | `uint32` | `optional` | `` |  |
| 8 | `client_addr` | `uint32` | `optional` | `` |  |
| 9 | `extra_fields` | `.CMsgGCHUpdateSession.ExtraField` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCHUpdateSession.ExtraField</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCHUpdateSession`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `value` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgNotificationOfSuspiciousActivity</code> — fields: 3; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steamid` | `fixed64` | `optional` | `` |  |
| 2 | `appid` | `uint32` | `optional` | `` |  |
| 3 | `multiple_instances` | `.CMsgNotificationOfSuspiciousActivity.MultipleGameInstances` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgNotificationOfSuspiciousActivity.MultipleGameInstances</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgNotificationOfSuspiciousActivity`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `app_instance_count` | `uint32` | `optional` | `` |  |
| 2 | `other_steamids` | `fixed64` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCHVacVerificationChange</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steamid` | `fixed64` | `optional` | `` |  |
| 2 | `appid` | `uint32` | `optional` | `` |  |
| 3 | `is_verified` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCHAccountPhoneNumberChange</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steamid` | `fixed64` | `optional` | `` |  |
| 2 | `appid` | `uint32` | `optional` | `` |  |
| 3 | `phone_id` | `uint64` | `optional` | `` |  |
| 4 | `is_verified` | `bool` | `optional` | `` |  |
| 5 | `is_identifying` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCHAccountTwoFactorChange</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steamid` | `fixed64` | `optional` | `` |  |
| 2 | `appid` | `uint32` | `optional` | `` |  |
| 3 | `twofactor_enabled` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCCheckClanMembership</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steamid` | `fixed64` | `optional` | `` |  |
| 2 | `clanid` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCCheckClanMembership_Response</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ismember` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCHAppCheersReceived</code> — fields: 2; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `appid` | `uint32` | `optional` | `` |  |
| 2 | `cheer_targets` | `.CMsgGCHAppCheersReceived.CheerTarget` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCHAppCheersReceived.CheerTypeAmount</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCHAppCheersReceived`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `cheer_type` | `uint32` | `optional` | `` |  |
| 2 | `cheer_amount` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCHAppCheersReceived.CheerTarget</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCHAppCheersReceived`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `cheer_target` | `uint64` | `optional` | `` |  |
| 2 | `cheer_types` | `.CMsgGCHAppCheersReceived.CheerTypeAmount` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCHAppCheersGetAllowedTypes</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `appid` | `uint32` | `optional` | `` |  |
| 2 | `cheer_target` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCHAppCheersGetAllowedTypesResponse</code> — fields: 3; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `cheer_types_valid_all_users` | `uint32` | `repeated` | `` |  |
| 2 | `cheer_remaps` | `.CMsgGCHAppCheersGetAllowedTypesResponse.CheerRemaps` | `repeated` | `` |  |
| 3 | `cache_duration` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCHAppCheersGetAllowedTypesResponse.CheerRemaps</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCHAppCheersGetAllowedTypesResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `original_cheer_type` | `uint32` | `optional` | `` |  |
| 2 | `remapped_cheer_type` | `uint32` | `optional` | `` |  |
| 3 | `account_ids` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CWorkshop_AddSpecialPayment_Request</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `appid` | `uint32` | `optional` | `` |  |
| 2 | `gameitemid` | `uint32` | `optional` | `` |  |
| 3 | `date` | `string` | `optional` | `` |  |
| 4 | `payment_us_usd` | `uint64` | `optional` | `` |  |
| 5 | `payment_row_usd` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CWorkshop_AddSpecialPayment_Response</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CWorkshop_GetSpecialPayments_Request</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `appid` | `uint32` | `optional` | `` |  |
| 2 | `gameitemid` | `uint32` | `optional` | `` |  |
| 3 | `date` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CWorkshop_GetSpecialPayments_Response</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `special_payments` | `.CWorkshop_GetSpecialPayments_Response.SpecialPayment` | `repeated` | `` |  |

</details>

<details>
<summary><code>CWorkshop_GetSpecialPayments_Response.SpecialPayment</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CWorkshop_GetSpecialPayments_Response`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `appid` | `uint32` | `optional` | `` |  |
| 2 | `gameitemid` | `uint32` | `optional` | `` |  |
| 3 | `date` | `string` | `optional` | `` |  |
| 4 | `net_payment_us_usd` | `uint64` | `optional` | `` |  |
| 5 | `net_payment_row_usd` | `uint64` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>CMsgGCRoutingInfo.RoutingMethod</code> — values: 6</summary>

- Parent: `CMsgGCRoutingInfo`

| Name | Number |
|---|---:|
| `RANDOM` | 0 |
| `DISCARD` | 1 |
| `CLIENT_STEAMID` | 2 |
| `PROTOBUF_FIELD_UINT64` | 3 |
| `WEBAPI_PARAM` | 4 |
| `WEBAPI_PARAM_STEAMID_ACCOUNTID` | 5 |

</details>

<details>
<summary><code>CMsgGCMsgSetOptions.Option</code> — values: 4</summary>

- Parent: `CMsgGCMsgSetOptions`

| Name | Number |
|---|---:|
| `NOTIFY_USER_SESSIONS` | 0 |
| `NOTIFY_SERVER_SESSIONS` | 1 |
| `NOTIFY_ACHIEVEMENTS` | 2 |
| `NOTIFY_VAC_ACTION` | 3 |

</details>

<details>
<summary><code>CMsgGCMsgSetOptions.GCSQLVersion</code> — values: 2</summary>

- Parent: `CMsgGCMsgSetOptions`

| Name | Number |
|---|---:|
| `GCSQL_VERSION_BASELINE` | 1 |
| `GCSQL_VERSION_BOOLTYPE` | 2 |

</details>
