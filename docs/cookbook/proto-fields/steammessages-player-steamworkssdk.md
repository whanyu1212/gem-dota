# steammessages_player.steamworkssdk.proto

- Module: `steammessages_player.steamworkssdk_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **1**
- Messages: **38** (top-level: 33)
- Enums: **1** (top-level: 1)

## Imports

- `steammessages_unified_base.steamworkssdk.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CPlayer_GetMutualFriendsForIncomingInvites_Request</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CPlayer_IncomingInviteMutualFriendList</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steamid` | `fixed64` | `optional` | `` |  |
| 2 | `mutual_friend_account_ids` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CPlayer_GetMutualFriendsForIncomingInvites_Response</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `incoming_invite_mutual_friends_lists` | `.CPlayer_IncomingInviteMutualFriendList` | `repeated` | `` |  |

</details>

<details>
<summary><code>CPlayer_GetFriendsGameplayInfo_Request</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `appid` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CPlayer_GetFriendsGameplayInfo_Response</code> — fields: 6; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `your_info` | `.CPlayer_GetFriendsGameplayInfo_Response.OwnGameplayInfo` | `optional` | `` |  |
| 2 | `in_game` | `.CPlayer_GetFriendsGameplayInfo_Response.FriendsGameplayInfo` | `repeated` | `` |  |
| 3 | `played_recently` | `.CPlayer_GetFriendsGameplayInfo_Response.FriendsGameplayInfo` | `repeated` | `` |  |
| 4 | `played_ever` | `.CPlayer_GetFriendsGameplayInfo_Response.FriendsGameplayInfo` | `repeated` | `` |  |
| 5 | `owns` | `.CPlayer_GetFriendsGameplayInfo_Response.FriendsGameplayInfo` | `repeated` | `` |  |
| 6 | `in_wishlist` | `.CPlayer_GetFriendsGameplayInfo_Response.FriendsGameplayInfo` | `repeated` | `` |  |

</details>

<details>
<summary><code>CPlayer_GetFriendsGameplayInfo_Response.FriendsGameplayInfo</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CPlayer_GetFriendsGameplayInfo_Response`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steamid` | `fixed64` | `optional` | `` |  |
| 2 | `minutes_played` | `uint32` | `optional` | `` |  |
| 3 | `minutes_played_forever` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CPlayer_GetFriendsGameplayInfo_Response.OwnGameplayInfo</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CPlayer_GetFriendsGameplayInfo_Response`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steamid` | `fixed64` | `optional` | `` |  |
| 2 | `minutes_played` | `uint32` | `optional` | `` |  |
| 3 | `minutes_played_forever` | `uint32` | `optional` | `` |  |
| 4 | `in_wishlist` | `bool` | `optional` | `` |  |
| 5 | `owned` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CPlayer_GetGameBadgeLevels_Request</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `appid` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CPlayer_GetGameBadgeLevels_Response</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_level` | `uint32` | `optional` | `` |  |
| 2 | `badges` | `.CPlayer_GetGameBadgeLevels_Response.Badge` | `repeated` | `` |  |

</details>

<details>
<summary><code>CPlayer_GetGameBadgeLevels_Response.Badge</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CPlayer_GetGameBadgeLevels_Response`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `level` | `int32` | `optional` | `` |  |
| 2 | `series` | `int32` | `optional` | `` |  |
| 3 | `border_color` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CPlayer_GetLastPlayedTimes_Request</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `min_last_played` | `uint32` | `optional` | `` | (description) = "The most recent last-played time the client already knows about" |

</details>

<details>
<summary><code>CPlayer_GetLastPlayedTimes_Response</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `games` | `.CPlayer_GetLastPlayedTimes_Response.Game` | `repeated` | `` |  |

</details>

<details>
<summary><code>CPlayer_GetLastPlayedTimes_Response.Game</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CPlayer_GetLastPlayedTimes_Response`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `appid` | `int32` | `optional` | `` |  |
| 2 | `last_playtime` | `uint32` | `optional` | `` |  |
| 3 | `playtime_2weeks` | `int32` | `optional` | `` |  |
| 4 | `playtime_forever` | `int32` | `optional` | `` |  |
| 5 | `first_playtime` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CPlayer_AcceptSSA_Request</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CPlayer_AcceptSSA_Response</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CPlayer_GetNicknameList_Request</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CPlayer_GetNicknameList_Response</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `nicknames` | `.CPlayer_GetNicknameList_Response.PlayerNickname` | `repeated` | `` |  |

</details>

<details>
<summary><code>CPlayer_GetNicknameList_Response.PlayerNickname</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CPlayer_GetNicknameList_Response`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `accountid` | `fixed32` | `optional` | `` |  |
| 2 | `nickname` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CPlayer_GetPerFriendPreferences_Request</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>PerFriendPreferences</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `accountid` | `fixed32` | `optional` | `` |  |
| 2 | `nickname` | `string` | `optional` | `` |  |
| 3 | `notifications_showingame` | `.ENotificationSetting` | `optional` | `` | default = k_ENotificationSettingNotifyUseDefault |
| 4 | `notifications_showonline` | `.ENotificationSetting` | `optional` | `` | default = k_ENotificationSettingNotifyUseDefault |
| 5 | `notifications_showmessages` | `.ENotificationSetting` | `optional` | `` | default = k_ENotificationSettingNotifyUseDefault |
| 6 | `sounds_showingame` | `.ENotificationSetting` | `optional` | `` | default = k_ENotificationSettingNotifyUseDefault |
| 7 | `sounds_showonline` | `.ENotificationSetting` | `optional` | `` | default = k_ENotificationSettingNotifyUseDefault |
| 8 | `sounds_showmessages` | `.ENotificationSetting` | `optional` | `` | default = k_ENotificationSettingNotifyUseDefault |
| 9 | `notifications_sendmobile` | `.ENotificationSetting` | `optional` | `` | default = k_ENotificationSettingNotifyUseDefault |

</details>

<details>
<summary><code>CPlayer_GetPerFriendPreferences_Response</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `preferences` | `.PerFriendPreferences` | `repeated` | `` |  |

</details>

<details>
<summary><code>CPlayer_SetPerFriendPreferences_Request</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `preferences` | `.PerFriendPreferences` | `optional` | `` |  |

</details>

<details>
<summary><code>CPlayer_SetPerFriendPreferences_Response</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CPlayer_AddFriend_Request</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steamid` | `fixed64` | `optional` | `` | (description) = "Steam ID of user to whom to send a friend invite." |

</details>

<details>
<summary><code>CPlayer_AddFriend_Response</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `invite_sent` | `bool` | `optional` | `` | (description) = "True if the operation was successful, false otherwise." |
| 2 | `friend_relationship` | `uint32` | `optional` | `` | (description) = "the resulting relationship.  Depending on state, may move directly to friends rather than invite sent" |

</details>

<details>
<summary><code>CPlayer_RemoveFriend_Request</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steamid` | `fixed64` | `optional` | `` | (description) = "Steam ID of friend to remove." |

</details>

<details>
<summary><code>CPlayer_RemoveFriend_Response</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `friend_relationship` | `uint32` | `optional` | `` | (description) = "the resulting relationship" |

</details>

<details>
<summary><code>CPlayer_IgnoreFriend_Request</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steamid` | `fixed64` | `optional` | `` |  |
| 2 | `unignore` | `bool` | `optional` | `` | (description) = "If set, remove from ignore/block list instead of adding " |

</details>

<details>
<summary><code>CPlayer_IgnoreFriend_Response</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `friend_relationship` | `uint32` | `optional` | `` | (description) = "the resulting relationship" |

</details>

<details>
<summary><code>CPlayer_GetCommunityPreferences_Request</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CPlayer_CommunityPreferences</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hide_adult_content_violence` | `bool` | `optional` | `` | default = true |
| 2 | `hide_adult_content_sex` | `bool` | `optional` | `` | default = true |
| 3 | `timestamp_updated` | `uint32` | `optional` | `` |  |
| 4 | `parenthesize_nicknames` | `bool` | `optional` | `` | default = false |

</details>

<details>
<summary><code>CPlayer_GetCommunityPreferences_Response</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `preferences` | `.CPlayer_CommunityPreferences` | `optional` | `` |  |

</details>

<details>
<summary><code>CPlayer_SetCommunityPreferences_Request</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `preferences` | `.CPlayer_CommunityPreferences` | `optional` | `` |  |

</details>

<details>
<summary><code>CPlayer_SetCommunityPreferences_Response</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CPlayer_GetNewSteamAnnouncementState_Request</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `language` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CPlayer_GetNewSteamAnnouncementState_Response</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `state` | `int32` | `optional` | `` |  |
| 2 | `announcement_headline` | `string` | `optional` | `` |  |
| 3 | `announcement_url` | `string` | `optional` | `` |  |
| 4 | `time_posted` | `uint32` | `optional` | `` |  |
| 5 | `announcement_gid` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CPlayer_UpdateSteamAnnouncementLastRead_Request</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `announcement_gid` | `uint64` | `optional` | `` |  |
| 2 | `time_posted` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CPlayer_UpdateSteamAnnouncementLastRead_Response</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>ENotificationSetting</code> — values: 3</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_ENotificationSettingNotifyUseDefault` | 0 |
| `k_ENotificationSettingAlways` | 1 |
| `k_ENotificationSettingNever` | 2 |

</details>
