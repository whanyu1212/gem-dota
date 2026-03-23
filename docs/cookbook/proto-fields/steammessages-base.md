# steammessages_base.proto

- Module: `steammessages_base_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **1**
- Messages: **21** (top-level: 20)
- Enums: **4** (top-level: 3)

## Imports

- `google/protobuf/descriptor.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgIPAddress</code> — fields: 2; oneofs: 1; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: `ip`

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `v4` | `fixed32` | `oneof` | `ip` |  |
| 2 | `v6` | `bytes` | `oneof` | `ip` |  |

</details>

<details>
<summary><code>CMsgIPAddressBucket</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `original_ip_address` | `.CMsgIPAddress` | `optional` | `` |  |
| 2 | `bucket` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgGCRoutingProtoBufHeader</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `dst_gcid_queue` | `uint64` | `optional` | `` |  |
| 2 | `dst_gc_dir_index` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgProtoBufHeader</code> — fields: 33; oneofs: 1; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: `ip_addr`

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steamid` | `fixed64` | `optional` | `` |  |
| 2 | `client_sessionid` | `int32` | `optional` | `` |  |
| 3 | `routing_appid` | `uint32` | `optional` | `` |  |
| 10 | `jobid_source` | `fixed64` | `optional` | `` | default = 18446744073709551615 |
| 11 | `jobid_target` | `fixed64` | `optional` | `` | default = 18446744073709551615 |
| 12 | `target_job_name` | `string` | `optional` | `` |  |
| 13 | `eresult` | `int32` | `optional` | `` | default = 2 |
| 14 | `error_message` | `string` | `optional` | `` |  |
| 15 | `ip` | `uint32` | `oneof` | `ip_addr` |  |
| 16 | `auth_account_flags` | `uint32` | `optional` | `` |  |
| 17 | `transport_error` | `int32` | `optional` | `` | default = 1 |
| 18 | `messageid` | `uint64` | `optional` | `` | default = 18446744073709551615 |
| 19 | `publisher_group_id` | `uint32` | `optional` | `` |  |
| 20 | `sysid` | `uint32` | `optional` | `` |  |
| 21 | `trace_tag` | `uint64` | `optional` | `` |  |
| 22 | `token_source` | `uint32` | `optional` | `` |  |
| 23 | `admin_spoofing_user` | `bool` | `optional` | `` |  |
| 24 | `seq_num` | `int32` | `optional` | `` |  |
| 25 | `webapi_key_id` | `uint32` | `optional` | `` |  |
| 26 | `is_from_external_source` | `bool` | `optional` | `` |  |
| 27 | `forward_to_sysid` | `uint32` | `repeated` | `` |  |
| 28 | `cm_sysid` | `uint32` | `optional` | `` |  |
| 29 | `ip_v6` | `bytes` | `oneof` | `ip_addr` |  |
| 31 | `launcher_type` | `uint32` | `optional` | `` | default = 0 |
| 32 | `realm` | `uint32` | `optional` | `` | default = 0 |
| 33 | `timeout_ms` | `int32` | `optional` | `` | default = -1 |
| 34 | `debug_source` | `string` | `optional` | `` |  |
| 35 | `debug_source_string_index` | `uint32` | `optional` | `` |  |
| 36 | `token_id` | `uint64` | `optional` | `` |  |
| 37 | `routing_gc` | `.CMsgGCRoutingProtoBufHeader` | `optional` | `` |  |
| 38 | `session_disposition` | `.CMsgProtoBufHeader.ESessionDisposition` | `optional` | `` | default = k_ESessionDispositionNormal |
| 39 | `wg_token` | `string` | `optional` | `` |  |
| 40 | `webui_auth_key` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgMulti</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `size_unzipped` | `uint32` | `optional` | `` |  |
| 2 | `message_body` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgProtobufWrapped</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `message_body` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgAuthTicket</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `estate` | `uint32` | `optional` | `` |  |
| 2 | `eresult` | `uint32` | `optional` | `` | default = 2 |
| 3 | `steamid` | `fixed64` | `optional` | `` |  |
| 4 | `gameid` | `fixed64` | `optional` | `` |  |
| 5 | `h_steam_pipe` | `uint32` | `optional` | `` |  |
| 6 | `ticket_crc` | `uint32` | `optional` | `` |  |
| 7 | `ticket` | `bytes` | `optional` | `` |  |
| 8 | `server_secret` | `bytes` | `optional` | `` |  |
| 9 | `ticket_type` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CCDDBAppDetailCommon</code> — fields: 15; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `appid` | `uint32` | `optional` | `` |  |
| 2 | `name` | `string` | `optional` | `` |  |
| 3 | `icon` | `string` | `optional` | `` |  |
| 6 | `tool` | `bool` | `optional` | `` |  |
| 7 | `demo` | `bool` | `optional` | `` |  |
| 8 | `media` | `bool` | `optional` | `` |  |
| 9 | `community_visible_stats` | `bool` | `optional` | `` |  |
| 10 | `friendly_name` | `string` | `optional` | `` |  |
| 11 | `propagation` | `string` | `optional` | `` |  |
| 12 | `has_adult_content` | `bool` | `optional` | `` |  |
| 13 | `is_visible_in_steam_china` | `bool` | `optional` | `` |  |
| 14 | `app_type` | `uint32` | `optional` | `` |  |
| 15 | `has_adult_content_sex` | `bool` | `optional` | `` |  |
| 16 | `has_adult_content_violence` | `bool` | `optional` | `` |  |
| 17 | `content_descriptorids` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgAppRights</code> — fields: 17; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `edit_info` | `bool` | `optional` | `` |  |
| 2 | `publish` | `bool` | `optional` | `` |  |
| 3 | `view_error_data` | `bool` | `optional` | `` |  |
| 4 | `download` | `bool` | `optional` | `` |  |
| 5 | `upload_cdkeys` | `bool` | `optional` | `` |  |
| 6 | `generate_cdkeys` | `bool` | `optional` | `` |  |
| 7 | `view_financials` | `bool` | `optional` | `` |  |
| 8 | `manage_ceg` | `bool` | `optional` | `` |  |
| 9 | `manage_signing` | `bool` | `optional` | `` |  |
| 10 | `manage_cdkeys` | `bool` | `optional` | `` |  |
| 11 | `edit_marketing` | `bool` | `optional` | `` |  |
| 12 | `economy_support` | `bool` | `optional` | `` |  |
| 13 | `economy_support_supervisor` | `bool` | `optional` | `` |  |
| 14 | `manage_pricing` | `bool` | `optional` | `` |  |
| 15 | `broadcast_live` | `bool` | `optional` | `` |  |
| 16 | `view_marketing_traffic` | `bool` | `optional` | `` |  |
| 17 | `edit_store_display_content` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CCuratorPreferences</code> — fields: 14; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `supported_languages` | `uint32` | `optional` | `` |  |
| 2 | `platform_windows` | `bool` | `optional` | `` |  |
| 3 | `platform_mac` | `bool` | `optional` | `` |  |
| 4 | `platform_linux` | `bool` | `optional` | `` |  |
| 5 | `vr_content` | `bool` | `optional` | `` |  |
| 6 | `adult_content_violence` | `bool` | `optional` | `` |  |
| 7 | `adult_content_sex` | `bool` | `optional` | `` |  |
| 8 | `timestamp_updated` | `uint32` | `optional` | `` |  |
| 9 | `tagids_curated` | `uint32` | `repeated` | `` |  |
| 10 | `tagids_filtered` | `uint32` | `repeated` | `` |  |
| 11 | `website_title` | `string` | `optional` | `` |  |
| 12 | `website_url` | `string` | `optional` | `` |  |
| 13 | `discussion_url` | `string` | `optional` | `` |  |
| 14 | `show_broadcast` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CLocalizationToken</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `language` | `uint32` | `optional` | `` |  |
| 2 | `localized_string` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CClanEventUserNewsTuple</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `clanid` | `uint32` | `optional` | `` |  |
| 2 | `event_gid` | `fixed64` | `optional` | `` |  |
| 3 | `announcement_gid` | `fixed64` | `optional` | `` |  |
| 4 | `rtime_start` | `uint32` | `optional` | `` |  |
| 5 | `rtime_end` | `uint32` | `optional` | `` |  |
| 6 | `priority_score` | `uint32` | `optional` | `` |  |
| 7 | `type` | `uint32` | `optional` | `` |  |
| 8 | `clamp_range_slot` | `uint32` | `optional` | `` |  |
| 9 | `appid` | `uint32` | `optional` | `` |  |
| 10 | `rtime32_last_modified` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CClanMatchEventByRange</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `rtime_before` | `uint32` | `optional` | `` |  |
| 2 | `rtime_after` | `uint32` | `optional` | `` |  |
| 3 | `qualified` | `uint32` | `optional` | `` |  |
| 4 | `events` | `.CClanEventUserNewsTuple` | `repeated` | `` |  |

</details>

<details>
<summary><code>CCommunity_ClanAnnouncementInfo</code> — fields: 17; oneofs: 0; nested messages: 0; nested enums: 0</summary>

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
| 13 | `event_gid` | `fixed64` | `optional` | `` |  |
| 14 | `voteupcount` | `int32` | `optional` | `` |  |
| 15 | `votedowncount` | `int32` | `optional` | `` |  |
| 16 | `ban_check_result` | `.EBanContentCheckResult` | `optional` | `` | default = k_EBanContentCheckResult_NotScanned |
| 17 | `banned` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CClanEventData</code> — fields: 30; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `gid` | `fixed64` | `optional` | `` |  |
| 2 | `clan_steamid` | `fixed64` | `optional` | `` |  |
| 3 | `event_name` | `string` | `optional` | `` |  |
| 4 | `event_type` | `.EProtoClanEventType` | `optional` | `` | default = k_EClanOtherEvent |
| 5 | `appid` | `uint32` | `optional` | `` |  |
| 6 | `server_address` | `string` | `optional` | `` |  |
| 7 | `server_password` | `string` | `optional` | `` |  |
| 8 | `rtime32_start_time` | `uint32` | `optional` | `` |  |
| 9 | `rtime32_end_time` | `uint32` | `optional` | `` |  |
| 10 | `comment_count` | `int32` | `optional` | `` |  |
| 11 | `creator_steamid` | `fixed64` | `optional` | `` |  |
| 12 | `last_update_steamid` | `fixed64` | `optional` | `` |  |
| 13 | `event_notes` | `string` | `optional` | `` |  |
| 14 | `jsondata` | `string` | `optional` | `` |  |
| 15 | `announcement_body` | `.CCommunity_ClanAnnouncementInfo` | `optional` | `` |  |
| 16 | `published` | `bool` | `optional` | `` |  |
| 17 | `hidden` | `bool` | `optional` | `` |  |
| 18 | `rtime32_visibility_start` | `uint32` | `optional` | `` |  |
| 19 | `rtime32_visibility_end` | `uint32` | `optional` | `` |  |
| 20 | `broadcaster_accountid` | `uint32` | `optional` | `` |  |
| 21 | `follower_count` | `uint32` | `optional` | `` |  |
| 22 | `ignore_count` | `uint32` | `optional` | `` |  |
| 23 | `forum_topic_id` | `fixed64` | `optional` | `` |  |
| 24 | `rtime32_last_modified` | `uint32` | `optional` | `` |  |
| 25 | `news_post_gid` | `fixed64` | `optional` | `` |  |
| 26 | `rtime_mod_reviewed` | `uint32` | `optional` | `` |  |
| 27 | `featured_app_tagid` | `uint32` | `optional` | `` |  |
| 28 | `referenced_appids` | `uint32` | `repeated` | `` |  |
| 29 | `build_id` | `uint32` | `optional` | `` |  |
| 30 | `build_branch` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CBilling_Address</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `first_name` | `string` | `optional` | `` |  |
| 2 | `last_name` | `string` | `optional` | `` |  |
| 3 | `address1` | `string` | `optional` | `` |  |
| 4 | `address2` | `string` | `optional` | `` |  |
| 5 | `city` | `string` | `optional` | `` |  |
| 6 | `us_state` | `string` | `optional` | `` |  |
| 7 | `country_code` | `string` | `optional` | `` |  |
| 8 | `postcode` | `string` | `optional` | `` |  |
| 9 | `zip_plus4` | `int32` | `optional` | `` |  |
| 10 | `phone` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CPackageReservationStatus</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `packageid` | `uint32` | `optional` | `` |  |
| 2 | `reservation_state` | `int32` | `optional` | `` |  |
| 3 | `queue_position` | `int32` | `optional` | `` |  |
| 4 | `total_queue_size` | `int32` | `optional` | `` |  |
| 5 | `reservation_country_code` | `string` | `optional` | `` |  |
| 6 | `expired` | `bool` | `optional` | `` |  |
| 7 | `time_expires` | `uint32` | `optional` | `` |  |
| 8 | `time_reserved` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgKeyValuePair</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `value` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgKeyValueSet</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `pairs` | `.CMsgKeyValuePair` | `repeated` | `` |  |

</details>

<details>
<summary><code>UserContentDescriptorPreferences</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `content_descriptors_to_exclude` | `.UserContentDescriptorPreferences.ContentDescriptor` | `repeated` | `` |  |

</details>

<details>
<summary><code>UserContentDescriptorPreferences.ContentDescriptor</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `UserContentDescriptorPreferences`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `content_descriptorid` | `uint32` | `optional` | `` |  |
| 2 | `timestamp_added` | `uint32` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>EBanContentCheckResult</code> — values: 8</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EBanContentCheckResult_NotScanned` | 0 |
| `k_EBanContentCheckResult_Reset` | 1 |
| `k_EBanContentCheckResult_NeedsChecking` | 2 |
| `k_EBanContentCheckResult_VeryUnlikely` | 5 |
| `k_EBanContentCheckResult_Unlikely` | 30 |
| `k_EBanContentCheckResult_Possible` | 50 |
| `k_EBanContentCheckResult_Likely` | 75 |
| `k_EBanContentCheckResult_VeryLikely` | 100 |

</details>

<details>
<summary><code>EProtoClanEventType</code> — values: 35</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EClanOtherEvent` | 1 |
| `k_EClanGameEvent` | 2 |
| `k_EClanPartyEvent` | 3 |
| `k_EClanMeetingEvent` | 4 |
| `k_EClanSpecialCauseEvent` | 5 |
| `k_EClanMusicAndArtsEvent` | 6 |
| `k_EClanSportsEvent` | 7 |
| `k_EClanTripEvent` | 8 |
| `k_EClanChatEvent` | 9 |
| `k_EClanGameReleaseEvent` | 10 |
| `k_EClanBroadcastEvent` | 11 |
| `k_EClanSmallUpdateEvent` | 12 |
| `k_EClanPreAnnounceMajorUpdateEvent` | 13 |
| `k_EClanMajorUpdateEvent` | 14 |
| `k_EClanDLCReleaseEvent` | 15 |
| `k_EClanFutureReleaseEvent` | 16 |
| `k_EClanESportTournamentStreamEvent` | 17 |
| `k_EClanDevStreamEvent` | 18 |
| `k_EClanFamousStreamEvent` | 19 |
| `k_EClanGameSalesEvent` | 20 |
| `k_EClanGameItemSalesEvent` | 21 |
| `k_EClanInGameBonusXPEvent` | 22 |
| `k_EClanInGameLootEvent` | 23 |
| `k_EClanInGamePerksEvent` | 24 |
| `k_EClanInGameChallengeEvent` | 25 |
| `k_EClanInGameContestEvent` | 26 |
| `k_EClanIRLEvent` | 27 |
| `k_EClanNewsEvent` | 28 |
| `k_EClanBetaReleaseEvent` | 29 |
| `k_EClanInGameContentReleaseEvent` | 30 |
| `k_EClanFreeTrial` | 31 |
| `k_EClanSeasonRelease` | 32 |
| `k_EClanSeasonUpdate` | 33 |
| `k_EClanCrosspostEvent` | 34 |
| `k_EClanInGameEventGeneral` | 35 |

</details>

<details>
<summary><code>PartnerEventNotificationType</code> — values: 4</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `k_EEventStart` | 0 |
| `k_EEventBroadcastStart` | 1 |
| `k_EEventMatchStart` | 2 |
| `k_EEventPartnerMaxType` | 3 |

</details>

<details>
<summary><code>CMsgProtoBufHeader.ESessionDisposition</code> — values: 2</summary>

- Parent: `CMsgProtoBufHeader`

| Name | Number |
|---|---:|
| `k_ESessionDispositionNormal` | 0 |
| `k_ESessionDispositionDisconnect` | 1 |

</details>
