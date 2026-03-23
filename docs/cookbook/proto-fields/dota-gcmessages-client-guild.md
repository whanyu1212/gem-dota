# dota_gcmessages_client_guild.proto

- Module: `dota_gcmessages_client_guild_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **1**
- Messages: **61** (top-level: 59)
- Enums: **26** (top-level: 2)

## Imports

- `dota_shared_enums.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgGuildInfo</code> — fields: 17; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_name` | `string` | `optional` | `` |  |
| 2 | `guild_tag` | `string` | `optional` | `` |  |
| 3 | `created_timestamp` | `uint32` | `optional` | `` |  |
| 4 | `guild_language` | `uint32` | `optional` | `` |  |
| 5 | `guild_flags` | `uint32` | `optional` | `` |  |
| 7 | `guild_logo` | `uint64` | `optional` | `` |  |
| 8 | `guild_region` | `uint32` | `optional` | `` |  |
| 9 | `guild_chat_group_id` | `uint64` | `optional` | `` |  |
| 10 | `guild_description` | `string` | `optional` | `` |  |
| 11 | `default_chat_channel_id` | `uint64` | `optional` | `` |  |
| 12 | `guild_primary_color` | `uint32` | `optional` | `` |  |
| 13 | `guild_secondary_color` | `uint32` | `optional` | `` |  |
| 14 | `guild_pattern` | `uint32` | `optional` | `` |  |
| 15 | `guild_refresh_time_offset` | `uint32` | `optional` | `` |  |
| 16 | `guild_required_rank_tier` | `uint32` | `optional` | `` |  |
| 17 | `guild_motd_timestamp` | `uint32` | `optional` | `` |  |
| 18 | `guild_motd` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGuildSummary</code> — fields: 3; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_info` | `.CMsgGuildInfo` | `optional` | `` |  |
| 2 | `member_count` | `uint32` | `optional` | `` |  |
| 3 | `event_points` | `.CMsgGuildSummary.EventPoints` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGuildSummary.EventPoints</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgGuildSummary`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |
| 2 | `guild_points` | `uint32` | `optional` | `` |  |
| 3 | `guild_rank` | `uint32` | `optional` | `` |  |
| 4 | `guild_weekly_rank` | `uint32` | `optional` | `` |  |
| 5 | `guild_weekly_percentile` | `uint32` | `optional` | `` |  |
| 6 | `guild_current_percentile` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGuildRole</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `role_id` | `uint32` | `optional` | `` |  |
| 2 | `role_name` | `string` | `optional` | `` |  |
| 3 | `role_flags` | `uint32` | `optional` | `` |  |
| 4 | `role_order` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGuildMember</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `member_account_id` | `uint32` | `optional` | `` |  |
| 2 | `member_role_id` | `uint32` | `optional` | `` |  |
| 3 | `member_joined_timestamp` | `uint32` | `optional` | `` |  |
| 4 | `member_last_active_timestamp` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGuildInvite</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `requester_account_id` | `uint32` | `optional` | `` |  |
| 2 | `target_account_id` | `uint32` | `optional` | `` |  |
| 3 | `timestamp_sent` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGuildData</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `guild_info` | `.CMsgGuildInfo` | `optional` | `` |  |
| 3 | `guild_roles` | `.CMsgGuildRole` | `repeated` | `` |  |
| 4 | `guild_members` | `.CMsgGuildMember` | `repeated` | `` |  |
| 5 | `guild_invites` | `.CMsgGuildInvite` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgAccountGuildInvite</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `requester_account_id` | `uint32` | `optional` | `` |  |
| 3 | `timestamp_sent` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgAccountGuildMemberships</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_ids` | `uint32` | `repeated` | `` |  |
| 2 | `guild_invites` | `.CMsgAccountGuildInvite` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGuildPersonaInfo</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `guild_tag` | `string` | `optional` | `` |  |
| 3 | `guild_flags` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgAccountGuildsPersonaInfo</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_persona_infos` | `.CMsgGuildPersonaInfo` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGuildFeedEvent</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `feed_event_id` | `uint64` | `optional` | `` |  |
| 2 | `timestamp` | `uint32` | `optional` | `` |  |
| 3 | `event_type` | `uint32` | `optional` | `` |  |
| 4 | `param_uint_1` | `uint32` | `optional` | `` |  |
| 5 | `param_uint_2` | `uint32` | `optional` | `` |  |
| 6 | `param_uint_3` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCreateGuild</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_info` | `.CMsgGuildInfo` | `optional` | `` |  |
| 2 | `guild_chat_type` | `.EGuildChatType` | `optional` | `` | default = k_EGuildChatType_Unspecified |

</details>

<details>
<summary><code>CMsgClientToGCCreateGuildResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCCreateGuildResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `guild_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCSetGuildInfo</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `guild_info` | `.CMsgGuildInfo` | `optional` | `` |  |
| 3 | `guild_chat_type` | `.EGuildChatType` | `optional` | `` | default = k_EGuildChatType_Unspecified |

</details>

<details>
<summary><code>CMsgClientToGCSetGuildInfoResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCSetGuildInfoResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCRequestGuildData</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestGuildDataResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCRequestGuildDataResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `guild_data` | `.CMsgGuildData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientGuildDataUpdated</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_data` | `.CMsgGuildData` | `optional` | `` |  |
| 2 | `update_flags` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientGuildMembersDataUpdated</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `members_data` | `.CMsgGuildMember` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestGuildMembership</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestGuildMembershipResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCRequestGuildMembershipResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `guild_memberships` | `.CMsgAccountGuildMemberships` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientGuildMembershipUpdated</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_memberships` | `.CMsgAccountGuildMemberships` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCJoinGuild</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCJoinGuildResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCJoinGuildResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCLeaveGuild</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCLeaveGuildResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCLeaveGuildResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCKickGuildMember</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `target_account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCKickGuildMemberResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCKickGuildMemberResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCSetGuildMemberRole</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `target_account_id` | `uint32` | `optional` | `` |  |
| 3 | `target_role_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCSetGuildMemberRoleResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCSetGuildMemberRoleResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCInviteToGuild</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `target_account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCInviteToGuildResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCInviteToGuildResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCDeclineInviteToGuild</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCDeclineInviteToGuildResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCDeclineInviteToGuildResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCAcceptInviteToGuild</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCAcceptInviteToGuildResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCAcceptInviteToGuildResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCCancelInviteToGuild</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `target_account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCCancelInviteToGuildResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCCancelInviteToGuildResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCAddGuildRole</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `role_name` | `string` | `optional` | `` |  |
| 3 | `role_flags` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCAddGuildRoleResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCAddGuildRoleResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `role_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCModifyGuildRole</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `role_id` | `uint32` | `optional` | `` |  |
| 3 | `role_name` | `string` | `optional` | `` |  |
| 4 | `role_flags` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCModifyGuildRoleResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCModifyGuildRoleResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCRemoveGuildRole</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `role_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRemoveGuildRoleResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCRemoveGuildRoleResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCSetGuildRoleOrder</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `requested_role_ids` | `uint32` | `repeated` | `` |  |
| 3 | `previous_role_ids` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCSetGuildRoleOrderResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCSetGuildRoleOrderResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `confirmed_role_ids` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCGuildFeedRequest</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `last_seen_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestGuildFeedResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCRequestGuildFeedResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `guild_id` | `uint32` | `optional` | `` |  |
| 3 | `feed_events` | `.CMsgGuildFeedEvent` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientGuildFeedUpdated</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCAddPlayerToGuildChat</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCAddPlayerToGuildChatResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCAddPlayerToGuildChatResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgFindGuildByTagResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgFindGuildByTagResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `guild_id` | `uint32` | `optional` | `` |  |
| 3 | `guild_summary` | `.CMsgGuildSummary` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSearchForOpenGuildsResponse</code> — fields: 3; oneofs: 0; nested messages: 1; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgSearchForOpenGuildsResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `search_results` | `.CMsgSearchForOpenGuildsResponse.SearchResult` | `repeated` | `` |  |
| 3 | `use_whitelist` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSearchForOpenGuildsResponse.SearchResult</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSearchForOpenGuildsResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `guild_summary` | `.CMsgGuildSummary` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCReportGuildContent</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guild_id` | `uint32` | `optional` | `` |  |
| 2 | `guild_content_flags` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCReportGuildContentResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCReportGuildContentResponse.EResponse` | `optional` | `` | default = k_eInternalError |

</details>

<details>
<summary><code>CMsgClientToGCRequestAccountGuildPersonaInfo</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestAccountGuildPersonaInfoResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCRequestAccountGuildPersonaInfoResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `persona_info` | `.CMsgAccountGuildsPersonaInfo` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestAccountGuildPersonaInfoBatch</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_ids` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCRequestAccountGuildPersonaInfoBatchResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgClientToGCRequestAccountGuildPersonaInfoBatchResponse.EResponse` | `optional` | `` | default = k_eInternalError |
| 2 | `persona_infos` | `.CMsgAccountGuildsPersonaInfo` | `repeated` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>EGuildAuditAction</code> — values: 26</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EGuildAuditAction_Invalid` | 0 |
| `k_EGuildAuditAction_GuildCreated` | 1 |
| `k_EGuildAuditAction_GuildLanguageChanged` | 2 |
| `k_EGuildAuditAction_GuildFlagsChanged` | 3 |
| `k_EGuildAuditAction_GuildMemberJoined` | 5 |
| `k_EGuildAuditAction_GuildMemberLeft` | 6 |
| `k_EGuildAuditAction_GuildMemberKicked` | 7 |
| `k_EGuildAuditAction_GuildMemberRoleChanged` | 8 |
| `k_EGuildAuditAction_GuildLogoChanged` | 9 |
| `k_EGuildAuditAction_GuildRegionChanged` | 10 |
| `k_EGuildAuditAction_GuildDescriptionChanged` | 11 |
| `k_EGuildAuditAction_GuildPrimaryColorChanged` | 12 |
| `k_EGuildAuditAction_GuildSecondaryColorChanged` | 13 |
| `k_EGuildAuditAction_GuildPatternChanged` | 14 |
| `k_EGuildAuditAction_AdminClearedLogo` | 15 |
| `k_EGuildAuditAction_GuildRequiredRankChanged` | 16 |
| `k_EGuildAuditAction_GuildMotDChanged` | 18 |
| `k_EGuildAuditAction_AdminResetName` | 19 |
| `k_EGuildAuditAction_AdminResetTag` | 20 |
| `k_EGuildAuditAction_AdminLock` | 21 |
| `k_EGuildAuditAction_GuildNameChanged` | 22 |
| `k_EGuildAuditAction_GuildTagChanged` | 23 |
| `k_EGuildAuditAction_AdminPermitted` | 24 |
| `k_EGuildAuditAction_AdminBlocked` | 25 |
| `k_EGuildAuditAction_AdminBannedUser` | 26 |
| `k_EGuildAuditAction_AdminExonerated` | 27 |

</details>

<details>
<summary><code>EGuildChatType</code> — values: 3</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EGuildChatType_Unspecified` | 0 |
| `k_EGuildChatType_SteamChatGroup` | 1 |
| `k_EGuildChatType_GC` | 2 |

</details>

<details>
<summary><code>CMsgClientToGCCreateGuildResponse.EResponse</code> — values: 17</summary>

- Parent: `CMsgClientToGCCreateGuildResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidName` | 5 |
| `k_eNameAlreadyUsed` | 6 |
| `k_eInvalidTag` | 7 |
| `k_eTagAlreadyUsed` | 8 |
| `k_eInvalidDescription` | 9 |
| `k_eInvalidRegion` | 10 |
| `k_eInvalidLogo` | 11 |
| `k_eDoesNotOwnEvent` | 12 |
| `k_eGuildLimit` | 13 |
| `k_eInvalidMotD` | 14 |
| `k_eBlocked` | 15 |
| `k_eFreeTrialNotAllowed` | 16 |

</details>

<details>
<summary><code>CMsgClientToGCSetGuildInfoResponse.EResponse</code> — values: 15</summary>

- Parent: `CMsgClientToGCSetGuildInfoResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidGuild` | 5 |
| `k_eNotMember` | 6 |
| `k_eNoPermission` | 7 |
| `k_eMotDTooLong` | 8 |
| `k_eNameChangeNoPermissions` | 9 |
| `k_eTagChangeNoPermissions` | 10 |
| `k_eNameInvalid` | 11 |
| `k_eTagInvalid` | 12 |
| `k_eDescriptionInvalid` | 13 |
| `k_eBlocked` | 14 |

</details>

<details>
<summary><code>CMsgClientToGCRequestGuildDataResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCRequestGuildDataResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidGuild` | 5 |
| `k_eNotMember` | 6 |

</details>

<details>
<summary><code>CMsgClientToGCRequestGuildMembershipResponse.EResponse</code> — values: 5</summary>

- Parent: `CMsgClientToGCRequestGuildMembershipResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |

</details>

<details>
<summary><code>CMsgClientToGCJoinGuildResponse.EResponse</code> — values: 11</summary>

- Parent: `CMsgClientToGCJoinGuildResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidGuild` | 5 |
| `k_eGuildFull` | 6 |
| `k_eAlreadyMember` | 7 |
| `k_eGuildLimit` | 8 |
| `k_eGuildRequiresInvite` | 9 |
| `k_eGuildRankTooLow` | 10 |

</details>

<details>
<summary><code>CMsgClientToGCLeaveGuildResponse.EResponse</code> — values: 8</summary>

- Parent: `CMsgClientToGCLeaveGuildResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidGuild` | 5 |
| `k_eNotMember` | 6 |
| `k_eLastAdmin` | 7 |

</details>

<details>
<summary><code>CMsgClientToGCKickGuildMemberResponse.EResponse</code> — values: 10</summary>

- Parent: `CMsgClientToGCKickGuildMemberResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidGuild` | 5 |
| `k_eRequesterNotMember` | 6 |
| `k_eTargetNotMember` | 7 |
| `k_eNoPermission` | 8 |
| `k_eCantKickSelf` | 9 |

</details>

<details>
<summary><code>CMsgClientToGCSetGuildMemberRoleResponse.EResponse</code> — values: 11</summary>

- Parent: `CMsgClientToGCSetGuildMemberRoleResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidGuild` | 5 |
| `k_eRequesterNotMember` | 6 |
| `k_eTargetNotMember` | 7 |
| `k_eNoPermission` | 8 |
| `k_eInvalidRole` | 9 |
| `k_eAdminViolation` | 10 |

</details>

<details>
<summary><code>CMsgClientToGCInviteToGuildResponse.EResponse</code> — values: 13</summary>

- Parent: `CMsgClientToGCInviteToGuildResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidGuild` | 5 |
| `k_eGuildFull` | 6 |
| `k_eRequesterNotMember` | 7 |
| `k_eAlreadyAMember` | 8 |
| `k_eAlreadyInvited` | 9 |
| `k_eNoInvitePermissions` | 10 |
| `k_eTooManyInvites` | 11 |
| `k_eInvalidUser` | 12 |

</details>

<details>
<summary><code>CMsgClientToGCDeclineInviteToGuildResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCDeclineInviteToGuildResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidGuild` | 5 |
| `k_eNoInviteFound` | 6 |

</details>

<details>
<summary><code>CMsgClientToGCAcceptInviteToGuildResponse.EResponse</code> — values: 11</summary>

- Parent: `CMsgClientToGCAcceptInviteToGuildResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidGuild` | 5 |
| `k_eNoInviteFound` | 6 |
| `k_eGuildFull` | 7 |
| `k_eGuildLimit` | 8 |
| `k_eInvalidInviter` | 9 |
| `k_eAlreadyInGuild` | 10 |

</details>

<details>
<summary><code>CMsgClientToGCCancelInviteToGuildResponse.EResponse</code> — values: 8</summary>

- Parent: `CMsgClientToGCCancelInviteToGuildResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidGuild` | 5 |
| `k_eNoInviteFound` | 6 |
| `k_eNoPermissions` | 7 |

</details>

<details>
<summary><code>CMsgClientToGCAddGuildRoleResponse.EResponse</code> — values: 13</summary>

- Parent: `CMsgClientToGCAddGuildRoleResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidGuild` | 5 |
| `k_eNameAlreadyUsed` | 6 |
| `k_eNoPermissions` | 7 |
| `k_eInvalidFlags` | 8 |
| `k_eInvalidName` | 9 |
| `k_eAdminViolation` | 10 |
| `k_eTooManyRoles` | 11 |
| `k_eBlocked` | 12 |

</details>

<details>
<summary><code>CMsgClientToGCModifyGuildRoleResponse.EResponse</code> — values: 13</summary>

- Parent: `CMsgClientToGCModifyGuildRoleResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidGuild` | 5 |
| `k_eInvalidRole` | 6 |
| `k_eNameAlreadyUsed` | 7 |
| `k_eInvalidFlags` | 8 |
| `k_eInvalidName` | 9 |
| `k_eNoPermissions` | 10 |
| `k_eAdminViolation` | 11 |
| `k_eBlocked` | 12 |

</details>

<details>
<summary><code>CMsgClientToGCRemoveGuildRoleResponse.EResponse</code> — values: 11</summary>

- Parent: `CMsgClientToGCRemoveGuildRoleResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidGuild` | 5 |
| `k_eInvalidRole` | 6 |
| `k_eRoleNotEmpty` | 7 |
| `k_eNoPermissions` | 8 |
| `k_eAdminViolation` | 9 |
| `k_eCantRemoveDefaultRole` | 10 |

</details>

<details>
<summary><code>CMsgClientToGCSetGuildRoleOrderResponse.EResponse</code> — values: 10</summary>

- Parent: `CMsgClientToGCSetGuildRoleOrderResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidGuild` | 5 |
| `k_eInvalidRole` | 6 |
| `k_eInvalidOrder` | 7 |
| `k_eNoPermissions` | 8 |
| `k_eAdminViolation` | 9 |

</details>

<details>
<summary><code>CMsgClientToGCRequestGuildFeedResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCRequestGuildFeedResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidGuild` | 5 |
| `k_eNoPermissions` | 6 |

</details>

<details>
<summary><code>CMsgClientToGCAddPlayerToGuildChatResponse.EResponse</code> — values: 8</summary>

- Parent: `CMsgClientToGCAddPlayerToGuildChatResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidGuild` | 5 |
| `k_eNotMember` | 6 |
| `k_eSteamChatNotEnabled` | 7 |

</details>

<details>
<summary><code>CMsgFindGuildByTagResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgFindGuildByTagResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidTag` | 5 |
| `k_eGuildNotFound` | 6 |

</details>

<details>
<summary><code>CMsgSearchForOpenGuildsResponse.EResponse</code> — values: 5</summary>

- Parent: `CMsgSearchForOpenGuildsResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |

</details>

<details>
<summary><code>CMsgClientToGCReportGuildContent.EContentFlags</code> — values: 5</summary>

- Parent: `CMsgClientToGCReportGuildContent`

| Name | Number |
|---|---:|
| `k_eNone` | 0 |
| `k_eInappropriateName` | 1 |
| `k_eInappropriateTag` | 2 |
| `k_eInappropriateLogo` | 4 |
| `k_eValidFlags` | 7 |

</details>

<details>
<summary><code>CMsgClientToGCReportGuildContentResponse.EResponse</code> — values: 7</summary>

- Parent: `CMsgClientToGCReportGuildContentResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eGuildNotFound` | 5 |
| `k_eFlagsInvalid` | 6 |

</details>

<details>
<summary><code>CMsgClientToGCRequestAccountGuildPersonaInfoResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCRequestAccountGuildPersonaInfoResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidAccount` | 5 |

</details>

<details>
<summary><code>CMsgClientToGCRequestAccountGuildPersonaInfoBatchResponse.EResponse</code> — values: 6</summary>

- Parent: `CMsgClientToGCRequestAccountGuildPersonaInfoBatchResponse`

| Name | Number |
|---|---:|
| `k_eInternalError` | 0 |
| `k_eSuccess` | 1 |
| `k_eTooBusy` | 2 |
| `k_eDisabled` | 3 |
| `k_eTimeout` | 4 |
| `k_eInvalidRequest` | 5 |

</details>
