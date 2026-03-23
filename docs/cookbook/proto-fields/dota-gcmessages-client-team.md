# dota_gcmessages_client_team.proto

- Module: `dota_gcmessages_client_team_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **1**
- Messages: **28** (top-level: 22)
- Enums: **6** (top-level: 1)

## Imports

- `dota_shared_enums.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgDOTATeamInfo</code> — fields: 27; oneofs: 0; nested messages: 6; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `members` | `.CMsgDOTATeamInfo.Member` | `repeated` | `` |  |
| 2 | `team_id` | `uint32` | `optional` | `` |  |
| 3 | `name` | `string` | `optional` | `` |  |
| 4 | `tag` | `string` | `optional` | `` |  |
| 5 | `time_created` | `uint32` | `optional` | `` |  |
| 6 | `pro` | `bool` | `optional` | `` |  |
| 8 | `pickup_team` | `bool` | `optional` | `` |  |
| 9 | `ugc_logo` | `uint64` | `optional` | `` |  |
| 10 | `ugc_base_logo` | `uint64` | `optional` | `` |  |
| 11 | `ugc_banner_logo` | `uint64` | `optional` | `` |  |
| 12 | `ugc_sponsor_logo` | `uint64` | `optional` | `` |  |
| 13 | `country_code` | `string` | `optional` | `` |  |
| 14 | `url` | `string` | `optional` | `` |  |
| 15 | `wins` | `uint32` | `optional` | `` |  |
| 16 | `losses` | `uint32` | `optional` | `` |  |
| 19 | `games_played_total` | `uint32` | `optional` | `` |  |
| 20 | `games_played_matchmaking` | `uint32` | `optional` | `` |  |
| 24 | `url_logo` | `string` | `optional` | `` |  |
| 29 | `region` | `.ELeagueRegion` | `optional` | `` | default = LEAGUE_REGION_UNSET |
| 31 | `audit_entries` | `.CMsgDOTATeamInfo.AuditEntry` | `repeated` | `` |  |
| 32 | `abbreviation` | `string` | `optional` | `` |  |
| 33 | `member_stats` | `.CMsgDOTATeamInfo.MemberStats` | `repeated` | `` |  |
| 34 | `team_stats` | `.CMsgDOTATeamInfo.TeamStats` | `optional` | `` |  |
| 35 | `dpc_results` | `.CMsgDOTATeamInfo.DPCResult` | `repeated` | `` |  |
| 37 | `color_primary` | `string` | `optional` | `` |  |
| 38 | `color_secondary` | `string` | `optional` | `` |  |
| 39 | `team_captain` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTATeamInfo.HeroStats</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTATeamInfo`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `picks` | `uint32` | `optional` | `` |  |
| 3 | `wins` | `uint32` | `optional` | `` |  |
| 4 | `bans` | `uint32` | `optional` | `` |  |
| 5 | `avg_kills` | `float` | `optional` | `` |  |
| 6 | `avg_deaths` | `float` | `optional` | `` |  |
| 7 | `avg_assists` | `float` | `optional` | `` |  |
| 8 | `avg_gpm` | `float` | `optional` | `` |  |
| 9 | `avg_xpm` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTATeamInfo.MemberStats</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTATeamInfo`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `wins_with_team` | `uint32` | `optional` | `` |  |
| 3 | `losses_with_team` | `uint32` | `optional` | `` |  |
| 4 | `top_heroes` | `.CMsgDOTATeamInfo.HeroStats` | `repeated` | `` |  |
| 5 | `avg_kills` | `float` | `optional` | `` |  |
| 6 | `avg_deaths` | `float` | `optional` | `` |  |
| 7 | `avg_assists` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTATeamInfo.TeamStats</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTATeamInfo`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `played_heroes` | `.CMsgDOTATeamInfo.HeroStats` | `repeated` | `` |  |
| 2 | `farming` | `float` | `optional` | `` |  |
| 3 | `fighting` | `float` | `optional` | `` |  |
| 4 | `versatility` | `float` | `optional` | `` |  |
| 5 | `avg_kills` | `float` | `optional` | `` |  |
| 6 | `avg_deaths` | `float` | `optional` | `` |  |
| 7 | `avg_duration` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTATeamInfo.DPCResult</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTATeamInfo`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_id` | `uint32` | `optional` | `` |  |
| 2 | `standing` | `uint32` | `optional` | `` |  |
| 3 | `points` | `uint32` | `optional` | `` |  |
| 4 | `earnings` | `uint32` | `optional` | `` |  |
| 5 | `timestamp` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTATeamInfo.Member</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTATeamInfo`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `time_joined` | `uint32` | `optional` | `` |  |
| 3 | `admin` | `bool` | `optional` | `` |  |
| 6 | `pro_name` | `string` | `optional` | `` |  |
| 8 | `role` | `.Fantasy_Roles` | `optional` | `` | default = FANTASY_ROLE_UNDEFINED |
| 9 | `real_name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTATeamInfo.AuditEntry</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgDOTATeamInfo`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `audit_action` | `uint32` | `optional` | `` |  |
| 2 | `timestamp` | `uint32` | `optional` | `` |  |
| 3 | `account_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTATeamsInfo</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `league_id` | `uint32` | `optional` | `` |  |
| 2 | `teams` | `.CMsgDOTATeamInfo` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTATeamInfoList</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `teams` | `.CMsgDOTATeamInfo` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgDOTATeamInfoCache</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `cache_timestamp` | `uint32` | `optional` | `` |  |
| 2 | `team_list` | `.CMsgDOTATeamInfoList` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAMyTeamInfoRequest</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CMsgDOTACreateTeam</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `tag` | `string` | `optional` | `` |  |
| 3 | `logo` | `uint64` | `optional` | `` |  |
| 4 | `base_logo` | `uint64` | `optional` | `` |  |
| 5 | `banner_logo` | `uint64` | `optional` | `` |  |
| 6 | `sponsor_logo` | `uint64` | `optional` | `` |  |
| 7 | `country_code` | `string` | `optional` | `` |  |
| 8 | `url` | `string` | `optional` | `` |  |
| 9 | `pickup_team` | `bool` | `optional` | `` |  |
| 10 | `abbreviation` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTACreateTeamResponse</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgDOTACreateTeamResponse.Result` | `optional` | `` | default = INVALID |
| 2 | `team_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAEditTeamDetails</code> — fields: 11; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team_id` | `uint32` | `optional` | `` |  |
| 2 | `name` | `string` | `optional` | `` |  |
| 3 | `tag` | `string` | `optional` | `` |  |
| 4 | `logo` | `uint64` | `optional` | `` |  |
| 5 | `base_logo` | `uint64` | `optional` | `` |  |
| 6 | `banner_logo` | `uint64` | `optional` | `` |  |
| 7 | `sponsor_logo` | `uint64` | `optional` | `` |  |
| 8 | `country_code` | `string` | `optional` | `` |  |
| 9 | `url` | `string` | `optional` | `` |  |
| 10 | `in_use_by_party` | `bool` | `optional` | `` |  |
| 11 | `abbreviation` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAEditTeamDetailsResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgDOTAEditTeamDetailsResponse.Result` | `optional` | `` | default = SUCCESS |

</details>

<details>
<summary><code>CMsgDOTATeamInvite_InviterToGC</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `team_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTATeamInvite_GCImmediateResponseToInviter</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.ETeamInviteResult` | `optional` | `` | default = TEAM_INVITE_SUCCESS |
| 2 | `invitee_name` | `string` | `optional` | `` |  |
| 3 | `required_play_time` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTATeamInvite_GCRequestToInvitee</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `inviter_account_id` | `uint32` | `optional` | `` |  |
| 2 | `team_name` | `string` | `optional` | `` |  |
| 3 | `team_tag` | `string` | `optional` | `` |  |
| 4 | `logo` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTATeamInvite_InviteeResponseToGC</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.ETeamInviteResult` | `optional` | `` | default = TEAM_INVITE_SUCCESS |

</details>

<details>
<summary><code>CMsgDOTATeamInvite_GCResponseToInviter</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.ETeamInviteResult` | `optional` | `` | default = TEAM_INVITE_SUCCESS |
| 2 | `invitee_name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTATeamInvite_GCResponseToInvitee</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.ETeamInviteResult` | `optional` | `` | default = TEAM_INVITE_SUCCESS |
| 2 | `team_name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAKickTeamMember</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `account_id` | `uint32` | `optional` | `` |  |
| 2 | `team_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTAKickTeamMemberResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgDOTAKickTeamMemberResponse.Result` | `optional` | `` | default = SUCCESS |

</details>

<details>
<summary><code>CMsgDOTATransferTeamAdmin</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `new_admin_account_id` | `uint32` | `optional` | `` |  |
| 2 | `team_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTATransferTeamAdminResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgDOTATransferTeamAdminResponse.Result` | `optional` | `` | default = SUCCESS |

</details>

<details>
<summary><code>CMsgDOTALeaveTeam</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgDOTALeaveTeamResponse</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.CMsgDOTALeaveTeamResponse.Result` | `optional` | `` | default = SUCCESS |

</details>

<details>
<summary><code>CMsgDOTABetaParticipation</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `access_rights` | `uint32` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>ETeamInviteResult</code> — values: 14</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `TEAM_INVITE_SUCCESS` | 0 |
| `TEAM_INVITE_FAILURE_INVITE_REJECTED` | 1 |
| `TEAM_INVITE_FAILURE_INVITE_TIMEOUT` | 2 |
| `TEAM_INVITE_ERROR_TEAM_AT_MEMBER_LIMIT` | 3 |
| `TEAM_INVITE_ERROR_TEAM_LOCKED` | 4 |
| `TEAM_INVITE_ERROR_INVITEE_NOT_AVAILABLE` | 5 |
| `TEAM_INVITE_ERROR_INVITEE_BUSY` | 6 |
| `TEAM_INVITE_ERROR_INVITEE_ALREADY_MEMBER` | 7 |
| `TEAM_INVITE_ERROR_INVITEE_AT_TEAM_LIMIT` | 8 |
| `TEAM_INVITE_ERROR_INVITEE_INSUFFICIENT_PLAY_TIME` | 9 |
| `TEAM_INVITE_ERROR_INVITER_INVALID_ACCOUNT_TYPE` | 10 |
| `TEAM_INVITE_ERROR_INVITER_NOT_ADMIN` | 11 |
| `TEAM_INVITE_ERROR_INCORRECT_USER_RESPONDED` | 12 |
| `TEAM_INVITE_ERROR_UNSPECIFIED` | 13 |

</details>

<details>
<summary><code>CMsgDOTACreateTeamResponse.Result</code> — values: 19</summary>

- Parent: `CMsgDOTACreateTeamResponse`

| Name | Number |
|---|---:|
| `INVALID` | -1 |
| `SUCCESS` | 0 |
| `NAME_EMPTY` | 1 |
| `NAME_BAD_CHARACTERS` | 2 |
| `NAME_TAKEN` | 3 |
| `NAME_TOO_LONG` | 4 |
| `TAG_EMPTY` | 5 |
| `TAG_BAD_CHARACTERS` | 6 |
| `TAG_TAKEN` | 7 |
| `TAG_TOO_LONG` | 8 |
| `CREATOR_BUSY` | 9 |
| `UNSPECIFIED_ERROR` | 10 |
| `CREATOR_TEAM_LIMIT_REACHED` | 11 |
| `NO_LOGO` | 12 |
| `CREATOR_TEAM_CREATION_COOLDOWN` | 13 |
| `LOGO_UPLOAD_FAILED` | 14 |
| `NAME_CHANGED_TOO_RECENTLY` | 15 |
| `CREATOR_INSUFFICIENT_LEVEL` | 16 |
| `INVALID_ACCOUNT_TYPE` | 17 |

</details>

<details>
<summary><code>CMsgDOTAEditTeamDetailsResponse.Result</code> — values: 5</summary>

- Parent: `CMsgDOTAEditTeamDetailsResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `FAILURE_INVALID_ACCOUNT_TYPE` | 1 |
| `FAILURE_NOT_MEMBER` | 2 |
| `FAILURE_TEAM_LOCKED` | 3 |
| `FAILURE_UNSPECIFIED_ERROR` | 4 |

</details>

<details>
<summary><code>CMsgDOTAKickTeamMemberResponse.Result</code> — values: 6</summary>

- Parent: `CMsgDOTAKickTeamMemberResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `FAILURE_INVALID_ACCOUNT_TYPE` | 1 |
| `FAILURE_KICKER_NOT_ADMIN` | 2 |
| `FAILURE_KICKEE_NOT_MEMBER` | 3 |
| `FAILURE_TEAM_LOCKED` | 4 |
| `FAILURE_UNSPECIFIED_ERROR` | 5 |

</details>

<details>
<summary><code>CMsgDOTATransferTeamAdminResponse.Result</code> — values: 6</summary>

- Parent: `CMsgDOTATransferTeamAdminResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `FAILURE_INVALID_ACCOUNT_TYPE` | 1 |
| `FAILURE_NOT_ADMIN` | 2 |
| `FAILURE_SAME_ACCOUNT` | 3 |
| `FAILURE_NOT_MEMBER` | 4 |
| `FAILURE_UNSPECIFIED_ERROR` | 5 |

</details>

<details>
<summary><code>CMsgDOTALeaveTeamResponse.Result</code> — values: 4</summary>

- Parent: `CMsgDOTALeaveTeamResponse`

| Name | Number |
|---|---:|
| `SUCCESS` | 0 |
| `FAILURE_NOT_MEMBER` | 1 |
| `FAILURE_TEAM_LOCKED` | 2 |
| `FAILURE_UNSPECIFIED_ERROR` | 3 |

</details>
