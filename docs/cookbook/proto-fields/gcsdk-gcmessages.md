# gcsdk_gcmessages.proto

- Module: `gcsdk_gcmessages_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **3**
- Messages: **74** (top-level: 57)
- Enums: **3** (top-level: 3)

## Imports

- `valveextensions.proto`
- `steammessages.proto`
- `steammessages_steamlearn.steamworkssdk.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CExtraMsgBlock</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `msg_type` | `uint32` | `optional` | `` |  |
| 2 | `contents` | `bytes` | `optional` | `` | (debugprint_visibility) = k_EProtoDebugVisibility_Never |
| 3 | `msg_key` | `uint64` | `optional` | `` |  |
| 4 | `is_compressed` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearnServerInfo</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 4 | `access_tokens` | `.CMsgSteamLearnAccessTokens` | `optional` | `` |  |
| 5 | `project_infos` | `.CMsgSteamLearnServerInfo.ProjectInfo` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearnServerInfo.ProjectInfo</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamLearnServerInfo`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `project_id` | `uint32` | `optional` | `` |  |
| 2 | `snapshot_published_version` | `uint32` | `optional` | `` |  |
| 3 | `inference_published_version` | `uint32` | `optional` | `` |  |
| 6 | `snapshot_percentage` | `uint32` | `optional` | `` |  |
| 7 | `snapshot_enabled` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCAssertJobData</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `message_type` | `string` | `optional` | `` |  |
| 2 | `message_data` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCConCommand</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `command` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSDOAssert</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `sdo_type` | `int32` | `optional` | `` |  |
| 2 | `requests` | `.CMsgSDOAssert.Request` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSDOAssert.Request</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSDOAssert`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `key` | `uint64` | `repeated` | `` |  |
| 2 | `requesting_job` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSOIDOwner</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `type` | `uint32` | `optional` | `` |  |
| 2 | `id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSOSingleObject</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `type_id` | `int32` | `optional` | `` |  |
| 3 | `object_data` | `bytes` | `optional` | `` |  |
| 4 | `version` | `fixed64` | `optional` | `` |  |
| 5 | `owner_soid` | `.CMsgSOIDOwner` | `optional` | `` |  |
| 6 | `service_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSOMultipleObjects</code> — fields: 6; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `objects_modified` | `.CMsgSOMultipleObjects.SingleObject` | `repeated` | `` |  |
| 3 | `version` | `fixed64` | `optional` | `` |  |
| 4 | `objects_added` | `.CMsgSOMultipleObjects.SingleObject` | `repeated` | `` |  |
| 5 | `objects_removed` | `.CMsgSOMultipleObjects.SingleObject` | `repeated` | `` |  |
| 6 | `owner_soid` | `.CMsgSOIDOwner` | `optional` | `` |  |
| 7 | `service_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSOMultipleObjects.SingleObject</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSOMultipleObjects`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `type_id` | `int32` | `optional` | `` |  |
| 2 | `object_data` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSOCacheSubscribed</code> — fields: 6; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `objects` | `.CMsgSOCacheSubscribed.SubscribedType` | `repeated` | `` |  |
| 3 | `version` | `fixed64` | `optional` | `` |  |
| 4 | `owner_soid` | `.CMsgSOIDOwner` | `optional` | `` |  |
| 5 | `service_id` | `uint32` | `optional` | `` |  |
| 6 | `service_list` | `uint32` | `repeated` | `` |  |
| 7 | `sync_version` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSOCacheSubscribed.SubscribedType</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSOCacheSubscribed`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `type_id` | `int32` | `optional` | `` |  |
| 2 | `object_data` | `bytes` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSOCacheSubscribedUpToDate</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `version` | `fixed64` | `optional` | `` |  |
| 2 | `owner_soid` | `.CMsgSOIDOwner` | `optional` | `` |  |
| 3 | `service_id` | `uint32` | `optional` | `` |  |
| 4 | `service_list` | `uint32` | `repeated` | `` |  |
| 5 | `sync_version` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSOCacheUnsubscribed</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `owner_soid` | `.CMsgSOIDOwner` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSOCacheSubscriptionCheck</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `version` | `fixed64` | `optional` | `` |  |
| 3 | `owner_soid` | `.CMsgSOIDOwner` | `optional` | `` |  |
| 4 | `service_id` | `uint32` | `optional` | `` |  |
| 5 | `service_list` | `uint32` | `repeated` | `` |  |
| 6 | `sync_version` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSOCacheSubscriptionRefresh</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `owner_soid` | `.CMsgSOIDOwner` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSOCacheVersion</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `version` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCMultiplexMessage</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `msgtype` | `uint32` | `optional` | `` |  |
| 2 | `payload` | `bytes` | `optional` | `` |  |
| 3 | `steamids` | `fixed64` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCSubGCStarting</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `dir_index` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CGCToGCMsgMasterAck</code> — fields: 4; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `dir_index` | `int32` | `optional` | `` | default = -1 |
| 3 | `machine_name` | `string` | `optional` | `` |  |
| 4 | `process_name` | `string` | `optional` | `` |  |
| 6 | `directory` | `.CGCToGCMsgMasterAck.Process` | `repeated` | `` |  |

</details>

<details>
<summary><code>CGCToGCMsgMasterAck.Process</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CGCToGCMsgMasterAck`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `dir_index` | `int32` | `optional` | `` | default = -1 |
| 2 | `type_instances` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CGCToGCMsgMasterAck_Response</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `eresult` | `int32` | `optional` | `` | default = 2 |

</details>

<details>
<summary><code>CMsgGCToGCUniverseStartup</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `is_initial_startup` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCUniverseStartupResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `eresult` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CGCToGCMsgMasterStartupComplete</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `gc_info` | `.CGCToGCMsgMasterStartupComplete.GCInfo` | `repeated` | `` |  |

</details>

<details>
<summary><code>CGCToGCMsgMasterStartupComplete.GCInfo</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CGCToGCMsgMasterStartupComplete`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `dir_index` | `int32` | `optional` | `` | default = -1 |
| 2 | `machine_name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CGCToGCMsgRouted</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `msg_type` | `uint32` | `optional` | `` |  |
| 2 | `sender_id` | `fixed64` | `optional` | `` |  |
| 3 | `net_message` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CGCToGCMsgRoutedReply</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `msg_type` | `uint32` | `optional` | `` |  |
| 2 | `net_message` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCUpdateSubGCSessionInfo</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `updates` | `.CMsgGCUpdateSubGCSessionInfo.CMsgUpdate` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCUpdateSubGCSessionInfo.CMsgUpdate</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCUpdateSubGCSessionInfo`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steamid` | `fixed64` | `optional` | `` |  |
| 2 | `ip` | `fixed32` | `optional` | `` |  |
| 3 | `trusted` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCRequestSubGCSessionInfo</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steamid` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCRequestSubGCSessionInfoResponse</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ip` | `fixed32` | `optional` | `` |  |
| 2 | `trusted` | `bool` | `optional` | `` |  |
| 3 | `port` | `uint32` | `optional` | `` |  |
| 4 | `success` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSOCacheHaveVersion</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `soid` | `.CMsgSOIDOwner` | `optional` | `` |  |
| 2 | `version` | `fixed64` | `optional` | `` |  |
| 3 | `service_id` | `uint32` | `optional` | `` |  |
| 4 | `cached_file_version` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientHello</code> — fields: 23; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `version` | `uint32` | `optional` | `` |  |
| 2 | `socache_have_versions` | `.CMsgSOCacheHaveVersion` | `repeated` | `` |  |
| 3 | `client_session_need` | `uint32` | `optional` | `` |  |
| 4 | `client_launcher` | `.PartnerAccountType` | `optional` | `` | default = PARTNER_NONE |
| 5 | `secret_key` | `string` | `optional` | `` |  |
| 6 | `client_language` | `uint32` | `optional` | `` |  |
| 7 | `engine` | `.ESourceEngine` | `optional` | `` | default = k_ESE_Source1 |
| 8 | `steamdatagram_login` | `bytes` | `optional` | `` |  |
| 9 | `platform_id` | `uint32` | `optional` | `` |  |
| 10 | `game_msg` | `bytes` | `optional` | `` |  |
| 11 | `os_type` | `int32` | `optional` | `` |  |
| 12 | `render_system` | `uint32` | `optional` | `` |  |
| 13 | `render_system_req` | `uint32` | `optional` | `` |  |
| 14 | `screen_width` | `uint32` | `optional` | `` |  |
| 15 | `screen_height` | `uint32` | `optional` | `` |  |
| 16 | `screen_refresh` | `uint32` | `optional` | `` |  |
| 17 | `render_width` | `uint32` | `optional` | `` |  |
| 18 | `render_height` | `uint32` | `optional` | `` |  |
| 19 | `swap_width` | `uint32` | `optional` | `` |  |
| 20 | `swap_height` | `uint32` | `optional` | `` |  |
| 22 | `is_steam_china` | `bool` | `optional` | `` |  |
| 23 | `platform_name` | `string` | `optional` | `` |  |
| 24 | `is_steam_china_client` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientWelcome</code> — fields: 16; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `version` | `uint32` | `optional` | `` |  |
| 2 | `game_data` | `bytes` | `optional` | `` |  |
| 3 | `outofdate_subscribed_caches` | `.CMsgSOCacheSubscribed` | `repeated` | `` |  |
| 4 | `uptodate_subscribed_caches` | `.CMsgSOCacheSubscriptionCheck` | `repeated` | `` |  |
| 5 | `location` | `.CMsgClientWelcome.Location` | `optional` | `` |  |
| 9 | `gc_socache_file_version` | `uint32` | `optional` | `` |  |
| 10 | `txn_country_code` | `string` | `optional` | `` |  |
| 11 | `game_data2` | `bytes` | `optional` | `` |  |
| 12 | `rtime32_gc_welcome_timestamp` | `uint32` | `optional` | `` |  |
| 13 | `currency` | `uint32` | `optional` | `` |  |
| 14 | `balance` | `uint32` | `optional` | `` |  |
| 15 | `balance_url` | `string` | `optional` | `` |  |
| 16 | `has_accepted_china_ssa` | `bool` | `optional` | `` |  |
| 17 | `is_banned_steam_china` | `bool` | `optional` | `` |  |
| 18 | `additional_welcome_msgs` | `.CExtraMsgBlock` | `optional` | `` |  |
| 20 | `steam_learn_server_info` | `.CMsgSteamLearnServerInfo` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientWelcome.Location</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgClientWelcome`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `latitude` | `float` | `optional` | `` |  |
| 2 | `longitude` | `float` | `optional` | `` |  |
| 3 | `country` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgConnectionStatus</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `status` | `.GCConnectionStatus` | `optional` | `` | default = GCConnectionStatus_HAVE_SESSION |
| 2 | `client_session_need` | `uint32` | `optional` | `` |  |
| 3 | `queue_position` | `int32` | `optional` | `` |  |
| 4 | `queue_size` | `int32` | `optional` | `` |  |
| 5 | `wait_seconds` | `int32` | `optional` | `` |  |
| 6 | `estimated_wait_seconds_remaining` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCSOCacheSubscribe</code> — fields: 5; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `subscriber` | `fixed64` | `optional` | `` |  |
| 2 | `subscribe_to_id` | `fixed64` | `optional` | `` |  |
| 3 | `sync_version` | `fixed64` | `optional` | `` |  |
| 4 | `have_versions` | `.CMsgGCToGCSOCacheSubscribe.CMsgHaveVersions` | `repeated` | `` |  |
| 5 | `subscribe_to_type` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCSOCacheSubscribe.CMsgHaveVersions</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGCToGCSOCacheSubscribe`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `service_id` | `uint32` | `optional` | `` |  |
| 2 | `version` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCSOCacheUnsubscribe</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `subscriber` | `fixed64` | `optional` | `` |  |
| 2 | `unsubscribe_from_id` | `fixed64` | `optional` | `` |  |
| 3 | `unsubscribe_from_type` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCClientPing</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgGCToGCForwardAccountDetails</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steamid` | `fixed64` | `optional` | `` |  |
| 2 | `account_details` | `.CGCSystemMsg_GetAccountDetails_Response` | `optional` | `` |  |
| 3 | `age_seconds` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCLoadSessionSOCache</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `forward_account_details` | `.CMsgGCToGCForwardAccountDetails` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCLoadSessionSOCacheResponse</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgGCToGCUpdateSessionStats</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `user_sessions` | `uint32` | `optional` | `` |  |
| 2 | `server_sessions` | `uint32` | `optional` | `` |  |
| 3 | `in_logon_surge` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientRequestDropped</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CWorkshop_PopulateItemDescriptions_Request</code> — fields: 2; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `appid` | `uint32` | `optional` | `` |  |
| 2 | `languages` | `.CWorkshop_PopulateItemDescriptions_Request.ItemDescriptionsLanguageBlock` | `repeated` | `` |  |

</details>

<details>
<summary><code>CWorkshop_PopulateItemDescriptions_Request.SingleItemDescription</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CWorkshop_PopulateItemDescriptions_Request`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `gameitemid` | `uint32` | `optional` | `` |  |
| 2 | `item_description` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CWorkshop_PopulateItemDescriptions_Request.ItemDescriptionsLanguageBlock</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CWorkshop_PopulateItemDescriptions_Request`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `language` | `string` | `optional` | `` |  |
| 2 | `descriptions` | `.CWorkshop_PopulateItemDescriptions_Request.SingleItemDescription` | `repeated` | `` |  |

</details>

<details>
<summary><code>CWorkshop_GetContributors_Request</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `appid` | `uint32` | `optional` | `` |  |
| 2 | `gameitemid` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CWorkshop_GetContributors_Response</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `contributors` | `fixed64` | `repeated` | `` |  |

</details>

<details>
<summary><code>CWorkshop_SetItemPaymentRules_Request</code> — fields: 7; oneofs: 0; nested messages: 3; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `appid` | `uint32` | `optional` | `` |  |
| 2 | `gameitemid` | `uint32` | `optional` | `` |  |
| 3 | `associated_workshop_files` | `.CWorkshop_SetItemPaymentRules_Request.WorkshopItemPaymentRule` | `repeated` | `` |  |
| 4 | `partner_accounts` | `.CWorkshop_SetItemPaymentRules_Request.PartnerItemPaymentRule` | `repeated` | `` |  |
| 5 | `validate_only` | `bool` | `optional` | `` |  |
| 6 | `make_workshop_files_subscribable` | `bool` | `optional` | `` |  |
| 7 | `associated_workshop_file_for_direct_payments` | `.CWorkshop_SetItemPaymentRules_Request.WorkshopDirectPaymentRule` | `optional` | `` |  |

</details>

<details>
<summary><code>CWorkshop_SetItemPaymentRules_Request.WorkshopItemPaymentRule</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CWorkshop_SetItemPaymentRules_Request`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `workshop_file_id` | `uint64` | `optional` | `` |  |
| 2 | `revenue_percentage` | `float` | `optional` | `` |  |
| 3 | `rule_description` | `string` | `optional` | `` |  |
| 4 | `rule_type` | `uint32` | `optional` | `` | default = 1 |

</details>

<details>
<summary><code>CWorkshop_SetItemPaymentRules_Request.WorkshopDirectPaymentRule</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CWorkshop_SetItemPaymentRules_Request`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `workshop_file_id` | `uint64` | `optional` | `` |  |
| 2 | `rule_description` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CWorkshop_SetItemPaymentRules_Request.PartnerItemPaymentRule</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CWorkshop_SetItemPaymentRules_Request`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `revenue_percentage` | `float` | `optional` | `` |  |
| 3 | `rule_description` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CWorkshop_SetItemPaymentRules_Response</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `validation_errors` | `string` | `repeated` | `` |  |

</details>

<details>
<summary><code>CCommunity_ClanAnnouncementInfo</code> — fields: 12; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `gid` | `uint64` | `optional` | `` |  |
| 2 | `clanid` | `uint64` | `optional` | `` |  |
| 3 | `posterid` | `uint64` | `optional` | `` |  |
| 4 | `headline` | `string` | `optional` | `` |  |
| 5 | `posttime` | `uint32` | `optional` | `` |  |
| 6 | `updatetime` | `uint32` | `optional` | `` |  |
| 7 | `body` | `string` | `optional` | `` |  |
| 8 | `commentcount` | `int32` | `optional` | `` |  |
| 9 | `tags` | `string` | `repeated` | `` |  |
| 10 | `language` | `int32` | `optional` | `` |  |
| 11 | `hidden` | `bool` | `optional` | `` |  |
| 12 | `forum_topic_id` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CCommunity_GetClanAnnouncements_Request</code> — fields: 13; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steamid` | `uint64` | `optional` | `` |  |
| 2 | `offset` | `uint32` | `optional` | `` |  |
| 3 | `count` | `uint32` | `optional` | `` |  |
| 4 | `maxchars` | `uint32` | `optional` | `` |  |
| 5 | `strip_html` | `bool` | `optional` | `` |  |
| 6 | `required_tags` | `string` | `repeated` | `` |  |
| 7 | `require_no_tags` | `bool` | `optional` | `` |  |
| 8 | `language_preference` | `uint32` | `repeated` | `` |  |
| 9 | `hidden_only` | `bool` | `optional` | `` |  |
| 10 | `only_gid` | `bool` | `optional` | `` |  |
| 11 | `rtime_oldest_date` | `uint32` | `optional` | `` |  |
| 12 | `include_hidden` | `bool` | `optional` | `` |  |
| 13 | `include_partner_events` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CCommunity_GetClanAnnouncements_Response</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `maxchars` | `uint32` | `optional` | `` |  |
| 2 | `strip_html` | `bool` | `optional` | `` |  |
| 3 | `announcements` | `.CCommunity_ClanAnnouncementInfo` | `repeated` | `` |  |

</details>

<details>
<summary><code>CBroadcast_PostGameDataFrame_Request</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `appid` | `uint32` | `optional` | `` |  |
| 2 | `steamid` | `fixed64` | `optional` | `` |  |
| 3 | `broadcast_id` | `fixed64` | `optional` | `` |  |
| 4 | `frame_data` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSerializedSOCache</code> — fields: 3; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `file_version` | `uint32` | `optional` | `` |  |
| 2 | `caches` | `.CMsgSerializedSOCache.Cache` | `repeated` | `` |  |
| 3 | `gc_socache_file_version` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSerializedSOCache.TypeCache</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSerializedSOCache`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `type` | `uint32` | `optional` | `` |  |
| 2 | `objects` | `bytes` | `repeated` | `` |  |
| 3 | `service_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSerializedSOCache.Cache</code> — fields: 4; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: `CMsgSerializedSOCache`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `type` | `uint32` | `optional` | `` |  |
| 2 | `id` | `uint64` | `optional` | `` |  |
| 3 | `versions` | `.CMsgSerializedSOCache.Cache.Version` | `repeated` | `` |  |
| 4 | `type_caches` | `.CMsgSerializedSOCache.TypeCache` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSerializedSOCache.Cache.Version</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSerializedSOCache.Cache`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `service` | `uint32` | `optional` | `` |  |
| 2 | `version` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientPollConvarRequest</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `convar_name` | `string` | `optional` | `` |  |
| 2 | `poll_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientPollConvarResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `poll_id` | `uint32` | `optional` | `` |  |
| 2 | `convar_value` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CGCMsgCompressedMsgToClient</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `msg_id` | `uint32` | `optional` | `` |  |
| 2 | `compressed_msg` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCMasterBroadcastMessage</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `users_per_second` | `uint32` | `optional` | `` |  |
| 2 | `send_to_users` | `bool` | `optional` | `` |  |
| 3 | `send_to_servers` | `bool` | `optional` | `` |  |
| 4 | `msg_id` | `uint32` | `optional` | `` |  |
| 5 | `msg_data` | `bytes` | `optional` | `` |  |
| 6 | `trusted_servers_only` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCMasterSubscribeToCache</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `soid_type` | `uint32` | `optional` | `` |  |
| 2 | `soid_id` | `fixed64` | `optional` | `` |  |
| 3 | `account_ids` | `uint32` | `repeated` | `` |  |
| 4 | `steam_ids` | `fixed64` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCMasterSubscribeToCacheResponse</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgGCToGCMasterSubscribeToCacheAsync</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `subscribe_msg` | `.CMsgGCToGCMasterSubscribeToCache` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCMasterUnsubscribeFromCache</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `soid_type` | `uint32` | `optional` | `` |  |
| 2 | `soid_id` | `fixed64` | `optional` | `` |  |
| 3 | `account_ids` | `uint32` | `repeated` | `` |  |
| 4 | `steam_ids` | `fixed64` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCToGCMasterDestroyCache</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `soid_type` | `uint32` | `optional` | `` |  |
| 2 | `soid_id` | `fixed64` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>ESourceEngine</code> — values: 2</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_ESE_Source1` | 0 |
| `k_ESE_Source2` | 1 |

</details>

<details>
<summary><code>PartnerAccountType</code> — values: 3</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `PARTNER_NONE` | 0 |
| `PARTNER_PERFECT_WORLD` | 1 |
| `PARTNER_INVALID` | 3 |

</details>

<details>
<summary><code>GCConnectionStatus</code> — values: 7</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `GCConnectionStatus_HAVE_SESSION` | 0 |
| `GCConnectionStatus_GC_GOING_DOWN` | 1 |
| `GCConnectionStatus_NO_SESSION` | 2 |
| `GCConnectionStatus_NO_SESSION_IN_LOGON_QUEUE` | 3 |
| `GCConnectionStatus_NO_STEAM` | 4 |
| `GCConnectionStatus_SUSPENDED` | 5 |
| `GCConnectionStatus_STEAM_GOING_DOWN` | 6 |

</details>
