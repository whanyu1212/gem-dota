# steammessages.proto

- Module: `steammessages_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **1**
- Messages: **5** (top-level: 5)
- Enums: **2** (top-level: 2)

## Imports

- `google/protobuf/descriptor.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgProtoBufHeader</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `client_steam_id` | `fixed64` | `optional` | `` |  |
| 2 | `client_session_id` | `int32` | `optional` | `` |  |
| 3 | `source_app_id` | `uint32` | `optional` | `` |  |
| 10 | `job_id_source` | `fixed64` | `optional` | `` | default = 18446744073709551615 |
| 11 | `job_id_target` | `fixed64` | `optional` | `` | default = 18446744073709551615 |
| 12 | `target_job_name` | `string` | `optional` | `` |  |
| 13 | `eresult` | `int32` | `optional` | `` | default = 2 |
| 14 | `error_message` | `string` | `optional` | `` |  |
| 200 | `gc_msg_src` | `.GCProtoBufMsgSrc` | `optional` | `` | default = GCProtoBufMsgSrc_Unspecified |
| 201 | `gc_dir_index_source` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CGCSystemMsg_GetAccountDetails</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steamid` | `fixed64` | `optional` | `` |  |
| 2 | `appid` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CGCSystemMsg_GetAccountDetails_Response</code> — fields: 37; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `eresult_deprecated` | `uint32` | `optional` | `` | default = 2 |
| 2 | `account_name` | `string` | `optional` | `` |  |
| 3 | `persona_name` | `string` | `optional` | `` |  |
| 4 | `is_profile_public` | `bool` | `optional` | `` |  |
| 5 | `is_inventory_public` | `bool` | `optional` | `` |  |
| 7 | `is_vac_banned` | `bool` | `optional` | `` |  |
| 8 | `is_cyber_cafe` | `bool` | `optional` | `` |  |
| 9 | `is_school_account` | `bool` | `optional` | `` |  |
| 10 | `is_limited` | `bool` | `optional` | `` |  |
| 11 | `is_subscribed` | `bool` | `optional` | `` |  |
| 12 | `package` | `uint32` | `optional` | `` |  |
| 13 | `is_free_trial_account` | `bool` | `optional` | `` |  |
| 14 | `free_trial_expiration` | `uint32` | `optional` | `` |  |
| 15 | `is_low_violence` | `bool` | `optional` | `` |  |
| 16 | `is_account_locked_down` | `bool` | `optional` | `` |  |
| 17 | `is_community_banned` | `bool` | `optional` | `` |  |
| 18 | `is_trade_banned` | `bool` | `optional` | `` |  |
| 19 | `trade_ban_expiration` | `uint32` | `optional` | `` |  |
| 20 | `accountid` | `uint32` | `optional` | `` |  |
| 21 | `suspension_end_time` | `uint32` | `optional` | `` |  |
| 22 | `currency` | `string` | `optional` | `` |  |
| 23 | `steam_level` | `uint32` | `optional` | `` |  |
| 24 | `friend_count` | `uint32` | `optional` | `` |  |
| 25 | `account_creation_time` | `uint32` | `optional` | `` |  |
| 26 | `is_profile_created` | `bool` | `optional` | `` |  |
| 27 | `is_steamguard_enabled` | `bool` | `optional` | `` |  |
| 28 | `is_phone_verified` | `bool` | `optional` | `` |  |
| 29 | `is_two_factor_auth_enabled` | `bool` | `optional` | `` |  |
| 30 | `two_factor_enabled_time` | `uint32` | `optional` | `` |  |
| 31 | `phone_verification_time` | `uint32` | `optional` | `` |  |
| 33 | `phone_id` | `uint64` | `optional` | `` |  |
| 34 | `is_phone_identifying` | `bool` | `optional` | `` |  |
| 35 | `rt_identity_linked` | `uint32` | `optional` | `` |  |
| 36 | `rt_birth_date` | `uint32` | `optional` | `` |  |
| 37 | `txn_country_code` | `string` | `optional` | `` |  |
| 38 | `has_accepted_china_ssa` | `bool` | `optional` | `` |  |
| 39 | `is_banned_steam_china` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CIPLocationInfo</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ip` | `uint32` | `optional` | `` |  |
| 2 | `latitude` | `float` | `optional` | `` |  |
| 3 | `longitude` | `float` | `optional` | `` |  |
| 4 | `country` | `string` | `optional` | `` |  |
| 5 | `state` | `string` | `optional` | `` |  |
| 6 | `city` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CGCMsgGetIPLocationResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `infos` | `.CIPLocationInfo` | `repeated` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>EGCPlatform</code> — values: 6</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_eGCPlatform_None` | 0 |
| `k_eGCPlatform_PC` | 1 |
| `k_eGCPlatform_Mac` | 2 |
| `k_eGCPlatform_Linux` | 3 |
| `k_eGCPlatform_Android` | 4 |
| `k_eGCPlatform_iOS` | 5 |

</details>

<details>
<summary><code>GCProtoBufMsgSrc</code> — values: 6</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `GCProtoBufMsgSrc_Unspecified` | 0 |
| `GCProtoBufMsgSrc_FromSystem` | 1 |
| `GCProtoBufMsgSrc_FromSteamID` | 2 |
| `GCProtoBufMsgSrc_FromGC` | 3 |
| `GCProtoBufMsgSrc_ReplySystem` | 4 |
| `GCProtoBufMsgSrc_SpoofedSteamID` | 5 |

</details>
