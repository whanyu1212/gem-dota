# dota_gcmessages_client_chat.proto

- Module: `dota_gcmessages_client_chat_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **1**
- Messages: **27** (top-level: 20)
- Enums: **2** (top-level: 0)

## Imports

- `dota_shared_enums.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgClientToGCPrivateChatInvite</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `private_chat_channel_name` | `string` | `optional` | `` |  |
| 2 | `invited_account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCPrivateChatKick</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `private_chat_channel_name` | `string` | `optional` | `` |  |
| 2 | `kick_account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCPrivateChatPromote</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `private_chat_channel_name` | `string` | `optional` | `` |  |
| 2 | `promote_account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClientToGCPrivateChatDemote</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `private_chat_channel_name` | `string` | `optional` | `` |  |
| 2 | `demote_account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCToClientPrivateChatResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `private_chat_channel_name` | `string` | `optional` | `` |  |
| 2 | `result` | `.CMsgGCToClientPrivateChatResponse.Result` | `optional` | `` | default = SUCCESS |
| 3 | `username` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAJoinChatChannel</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `channel_name` | `string` | `optional` | `` |  |
| 4 | `channel_type` | `.DOTAChatChannelType_t` | `optional` | `` | default = DOTAChannelType_Regional |
| 5 | `silent_rejection` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALeaveChatChannel</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `channel_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCChatReportPublicSpam</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `channel_id` | `uint64` | `optional` | `` |  |
| 2 | `channel_user_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAChatModeratorBan</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `channel_id` | `uint64` | `optional` | `` |  |
| 2 | `account_id` | `uint32` | `optional` | `` |  |
| 3 | `duration` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAChatMessage</code> — fields: 42; oneofs: 0; nested messages: 4; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `channel_id` | `uint64` | `optional` | `` |  |
| 3 | `persona_name` | `string` | `optional` | `` |  |
| 4 | `text` | `string` | `optional` | `` |  |
| 5 | `timestamp` | `uint32` | `optional` | `` |  |
| 6 | `suggest_invite_account_id` | `uint32` | `optional` | `` |  |
| 7 | `suggest_invite_name` | `string` | `optional` | `` |  |
| 8 | `fantasy_draft_owner_account_id` | `uint32` | `optional` | `` |  |
| 9 | `fantasy_draft_player_account_id` | `uint32` | `optional` | `` |  |
| 10 | `event_id` | `uint32` | `optional` | `` |  |
| 11 | `suggest_invite_to_lobby` | `bool` | `optional` | `` |  |
| 13 | `coin_flip` | `bool` | `optional` | `` |  |
| 14 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 15 | `share_profile_account_id` | `uint32` | `optional` | `` |  |
| 16 | `channel_user_id` | `uint32` | `optional` | `` |  |
| 17 | `dice_roll` | `.CMsgDOTAChatMessage.DiceRoll` | `optional` | `` |  |
| 18 | `share_party_id` | `uint64` | `optional` | `` |  |
| 19 | `share_lobby_id` | `uint64` | `optional` | `` |  |
| 20 | `share_lobby_custom_game_id` | `uint64` | `optional` | `` |  |
| 21 | `share_lobby_passkey` | `string` | `optional` | `` |  |
| 22 | `private_chat_channel_id` | `uint32` | `optional` | `` |  |
| 23 | `status` | `uint32` | `optional` | `` |  |
| 24 | `legacy_battle_cup_victory` | `bool` | `optional` | `` |  |
| 25 | `badge_level` | `uint32` | `optional` | `` |  |
| 26 | `suggest_pick_hero_id` | `int32` | `optional` | `` |  |
| 27 | `suggest_pick_hero_role` | `string` | `optional` | `` |  |
| 29 | `battle_cup_streak` | `uint32` | `optional` | `` |  |
| 30 | `suggest_ban_hero_id` | `int32` | `optional` | `` |  |
| 32 | `trivia_answer` | `.CMsgDOTAChatMessage.TriviaAnswered` | `optional` | `` |  |
| 33 | `requested_ability_id` | `int32` | `optional` | `` | default = -1 |
| 34 | `chat_flags` | `uint32` | `optional` | `` |  |
| 35 | `started_finding_match` | `bool` | `optional` | `` |  |
| 36 | `ctrl_is_down` | `bool` | `optional` | `` |  |
| 37 | `favorite_team_id` | `uint32` | `optional` | `` |  |
| 38 | `favorite_team_quality` | `uint32` | `optional` | `` |  |
| 39 | `suggest_player_draft_pick` | `int32` | `optional` | `` | default = -1 |
| 40 | `player_draft_pick` | `.CMsgDOTAChatMessage.PlayerDraftPick` | `optional` | `` |  |
| 41 | `chat_wheel_message` | `.CMsgDOTAChatMessage.ChatWheelMessage` | `optional` | `` |  |
| 42 | `event_level` | `uint32` | `optional` | `` |  |
| 43 | `suggest_pick_hero_facet` | `uint32` | `optional` | `` |  |
| 44 | `requested_hero_id` | `int32` | `optional` | `` |  |
| 45 | `requested_hero_facet_key` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAChatMessage.DiceRoll</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAChatMessage`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `roll_min` | `int32` | `optional` | `` |  |
| 2 | `roll_max` | `int32` | `optional` | `` |  |
| 3 | `result` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAChatMessage.TriviaAnswered</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAChatMessage`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `question_id` | `uint32` | `optional` | `` |  |
| 2 | `answer_index` | `uint32` | `optional` | `` |  |
| 3 | `party_questions_correct` | `uint32` | `optional` | `` |  |
| 4 | `party_questions_viewed` | `uint32` | `optional` | `` |  |
| 5 | `party_trivia_points` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAChatMessage.PlayerDraftPick</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAChatMessage`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `team` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAChatMessage.ChatWheelMessage</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAChatMessage`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `message_id` | `uint32` | `optional` | `` | default = 4294967295 |
| 2 | `emoticon_id` | `uint32` | `optional` | `` |  |
| 3 | `message_text` | `string` | `optional` | `` |  |
| 4 | `hero_badge_tier` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAChatMember</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steam_id` | `fixed64` | `optional` | `` |  |
| 2 | `persona_name` | `string` | `optional` | `` |  |
| 3 | `channel_user_id` | `uint32` | `optional` | `` |  |
| 4 | `status` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAJoinChatChannelResponse</code> — fields: 11; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `response` | `uint32` | `optional` | `` |  |
| 2 | `channel_name` | `string` | `optional` | `` |  |
| 3 | `channel_id` | `fixed64` | `optional` | `` |  |
| 4 | `max_members` | `uint32` | `optional` | `` |  |
| 5 | `members` | `.CMsgDOTAChatMember` | `repeated` | `` |  |
| 6 | `channel_type` | `.DOTAChatChannelType_t` | `optional` | `` | default = DOTAChannelType_Regional |
| 7 | `result` | `.CMsgDOTAJoinChatChannelResponse.Result` | `optional` | `` | default = JOIN_SUCCESS |
| 8 | `gc_initiated_join` | `bool` | `optional` | `` |  |
| 9 | `channel_user_id` | `uint32` | `optional` | `` |  |
| 10 | `welcome_message` | `string` | `optional` | `` |  |
| 11 | `special_privileges` | `.EChatSpecialPrivileges` | `optional` | `` | default = k_EChatSpecialPrivileges_None |

</details>

<details>
<summary><code>CMsgDOTAOtherJoinedChatChannel</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `channel_id` | `fixed64` | `optional` | `` |  |
| 2 | `persona_name` | `string` | `optional` | `` |  |
| 3 | `steam_id` | `fixed64` | `optional` | `` |  |
| 4 | `channel_user_id` | `uint32` | `optional` | `` |  |
| 5 | `status` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAOtherLeftChatChannel</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `channel_id` | `fixed64` | `optional` | `` |  |
| 2 | `steam_id` | `fixed64` | `optional` | `` |  |
| 3 | `channel_user_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTARequestChatChannelList</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgDOTARequestChatChannelListResponse</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `channels` | `.CMsgDOTARequestChatChannelListResponse.ChatChannel` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTARequestChatChannelListResponse.ChatChannel</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTARequestChatChannelListResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `channel_name` | `string` | `optional` | `` |  |
| 2 | `num_members` | `uint32` | `optional` | `` |  |
| 3 | `channel_type` | `.DOTAChatChannelType_t` | `optional` | `` | default = DOTAChannelType_Regional |

</details>

<details>
<summary><code>CMsgDOTAChatGetUserListResponse</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `channel_id` | `fixed64` | `optional` | `` |  |
| 2 | `members` | `.CMsgDOTAChatGetUserListResponse.Member` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAChatGetUserListResponse.Member</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAChatGetUserListResponse`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steam_id` | `fixed64` | `optional` | `` |  |
| 2 | `persona_name` | `string` | `optional` | `` |  |
| 3 | `channel_user_id` | `uint32` | `optional` | `` |  |
| 4 | `status` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAChatGetMemberCount</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `channel_name` | `string` | `optional` | `` |  |
| 2 | `channel_type` | `.DOTAChatChannelType_t` | `optional` | `` | default = DOTAChannelType_Regional |

</details>

<details>
<summary><code>CMsgDOTAChatGetMemberCountResponse</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `channel_name` | `string` | `optional` | `` |  |
| 2 | `channel_type` | `.DOTAChatChannelType_t` | `optional` | `` | default = DOTAChannelType_Regional |
| 3 | `member_count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAChatRegionsEnabled</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `enable_all_regions` | `bool` | `optional` | `` |  |
| 2 | `enabled_regions` | `.CMsgDOTAChatRegionsEnabled.Region` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAChatRegionsEnabled.Region</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTAChatRegionsEnabled`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `min_latitude` | `float` | `optional` | `` |  |
| 2 | `max_latitude` | `float` | `optional` | `` |  |
| 3 | `min_longitude` | `float` | `optional` | `` |  |
| 4 | `max_longitude` | `float` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>CMsgGCToClientPrivateChatResponse.Result</code> — values: 15</summary>

- Parent: `CMsgGCToClientPrivateChatResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `FAILURE_CREATION_LOCK` | 1 |
| `FAILURE_SQL_TRANSACTION` | 2 |
| `FAILURE_SDO_LOAD` | 3 |
| `FAILURE_NO_PERMISSION` | 4 |
| `FAILURE_ALREADY_MEMBER` | 5 |
| `FAILURE_NOT_A_MEMBER` | 7 |
| `FAILURE_NO_REMAINING_ADMINS` | 8 |
| `FAILURE_NO_ROOM` | 9 |
| `FAILURE_CREATION_RATE_LIMITED` | 10 |
| `FAILURE_UNKNOWN_CHANNEL_NAME` | 11 |
| `FAILURE_UNKNOWN_USER` | 12 |
| `FAILURE_UNKNOWN_ERROR` | 13 |
| `FAILURE_CANNOT_KICK_ADMIN` | 14 |
| `FAILURE_ALREADY_ADMIN` | 15 |

</details>

<details>
<summary><code>CMsgDOTAJoinChatChannelResponse.Result</code> — values: 19</summary>

- Parent: `CMsgDOTAJoinChatChannelResponse`

| Name | Number |
|---|---:|
| `JOIN_SUCCESS` | 0 |
| `INVALID_CHANNEL_TYPE` | 1 |
| `ACCOUNT_NOT_FOUND` | 2 |
| `ACH_FAILED` | 3 |
| `USER_IN_TOO_MANY_CHANNELS` | 4 |
| `RATE_LIMIT_EXCEEDED` | 5 |
| `CHANNEL_FULL` | 6 |
| `CHANNEL_FULL_OVERFLOWED` | 7 |
| `FAILED_TO_ADD_USER` | 8 |
| `CHANNEL_TYPE_DISABLED` | 9 |
| `PRIVATE_CHAT_CREATE_FAILED` | 10 |
| `PRIVATE_CHAT_NO_PERMISSION` | 11 |
| `PRIVATE_CHAT_CREATE_LOCK_FAILED` | 12 |
| `PRIVATE_CHAT_KICKED` | 13 |
| `USER_NOT_ALLOWED` | 14 |
| `ENSURE_SPECIAL_PRIVILEGES_FAILED` | 15 |
| `NEW_PLAYER_USER_NOT_ELIGIBLE` | 16 |
| `SILENT_ERROR` | 17 |
| `NEW_PLAYER_USER_BANNED` | 18 |

</details>
