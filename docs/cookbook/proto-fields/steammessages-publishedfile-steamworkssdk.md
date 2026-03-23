# steammessages_publishedfile.steamworkssdk.proto

- Module: `steammessages_publishedfile.steamworkssdk_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **1**
- Messages: **21** (top-level: 15)
- Enums: **0** (top-level: 0)

## Imports

- `steammessages_unified_base.steamworkssdk.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CPublishedFile_Subscribe_Request</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `publishedfileid` | `uint64` | `optional` | `` |  |
| 2 | `list_type` | `uint32` | `optional` | `` |  |
| 3 | `appid` | `int32` | `optional` | `` |  |
| 4 | `notify_client` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CPublishedFile_Subscribe_Response</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CPublishedFile_Unsubscribe_Request</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `publishedfileid` | `uint64` | `optional` | `` |  |
| 2 | `list_type` | `uint32` | `optional` | `` |  |
| 3 | `appid` | `int32` | `optional` | `` |  |
| 4 | `notify_client` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CPublishedFile_Unsubscribe_Response</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CPublishedFile_Publish_Request</code> — fields: 16; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `appid` | `uint32` | `optional` | `` | (description) = "App Id this file is being published FROM." |
| 2 | `consumer_appid` | `uint32` | `optional` | `` | (description) = "App Id this file is being published TO." |
| 3 | `cloudfilename` | `string` | `optional` | `` | (description) = "Name of the file to publish in the user's cloud." |
| 4 | `preview_cloudfilename` | `string` | `optional` | `` | (description) = "Name of the file to use as the published file's preview." |
| 5 | `title` | `string` | `optional` | `` | (description) = "Text title for the published file." |
| 6 | `file_description` | `string` | `optional` | `` | (description) = "Text description for the published file." |
| 7 | `file_type` | `uint32` | `optional` | `` | (description) = "(EWorkshopFileType) Type of Workshop file to publish." |
| 8 | `consumer_shortcut_name` | `string` | `optional` | `` | (description) = "Shortcut name for the published file." |
| 9 | `youtube_username` | `string` | `optional` | `` | (description) = "(Optional) User's YouTube account username." |
| 10 | `youtube_videoid` | `string` | `optional` | `` | (description) = "(Optional) Video Id of a YouTube video for this published file." |
| 11 | `visibility` | `uint32` | `optional` | `` | (description) = "(ERemoteStoragePublishedFileVisibility) Visibility of the published file (private, friends, public, etc.)" |
| 12 | `redirect_uri` | `string` | `optional` | `` | (description) = "(Optional) If supplied, the resulting published file's Id is appended to the URI." |
| 13 | `tags` | `string` | `repeated` | `` | (description) = "Array of text tags to apply to the published file." |
| 14 | `collection_type` | `string` | `optional` | `` | (description) = "(Optional) Type of collection the published file represents." |
| 15 | `game_type` | `string` | `optional` | `` | (description) = "(Optional) Type of game the published file represents." |
| 16 | `url` | `string` | `optional` | `` | (description) = "(Optional) If this represents a game, this is the URL to that game's page." |

</details>

<details>
<summary><code>CPublishedFile_Publish_Response</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `publishedfileid` | `uint64` | `optional` | `` |  |
| 2 | `redirect_uri` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CPublishedFile_GetDetails_Request</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `publishedfileids` | `fixed64` | `repeated` | `` | (description) = "Set of published file Ids to retrieve details for." |
| 2 | `includetags` | `bool` | `optional` | `` | (description) = "If true, return tag information in the returned details." |
| 3 | `includeadditionalpreviews` | `bool` | `optional` | `` | (description) = "If true, return preview information in the returned details." |
| 4 | `includechildren` | `bool` | `optional` | `` | (description) = "If true, return children in the returned details." |
| 5 | `includekvtags` | `bool` | `optional` | `` | (description) = "If true, return key value tags in the returned details." |
| 6 | `includevotes` | `bool` | `optional` | `` | (description) = "If true, return vote data in the returned details." |
| 8 | `short_description` | `bool` | `optional` | `` | (description) = "If true, return a short description instead of the full description." |

</details>

<details>
<summary><code>PublishedFileDetails</code> — fields: 56; oneofs: 0; nested messages: 5; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `uint32` | `optional` | `` |  |
| 2 | `publishedfileid` | `uint64` | `optional` | `` |  |
| 3 | `creator` | `fixed64` | `optional` | `` |  |
| 4 | `creator_appid` | `uint32` | `optional` | `` |  |
| 5 | `consumer_appid` | `uint32` | `optional` | `` |  |
| 6 | `consumer_shortcutid` | `uint32` | `optional` | `` |  |
| 7 | `filename` | `string` | `optional` | `` |  |
| 8 | `file_size` | `uint64` | `optional` | `` |  |
| 9 | `preview_file_size` | `uint64` | `optional` | `` |  |
| 10 | `file_url` | `string` | `optional` | `` |  |
| 11 | `preview_url` | `string` | `optional` | `` |  |
| 12 | `youtubevideoid` | `string` | `optional` | `` |  |
| 13 | `url` | `string` | `optional` | `` |  |
| 14 | `hcontent_file` | `fixed64` | `optional` | `` |  |
| 15 | `hcontent_preview` | `fixed64` | `optional` | `` |  |
| 16 | `title` | `string` | `optional` | `` |  |
| 17 | `file_description` | `string` | `optional` | `` |  |
| 18 | `short_description` | `string` | `optional` | `` |  |
| 19 | `time_created` | `uint32` | `optional` | `` |  |
| 20 | `time_updated` | `uint32` | `optional` | `` |  |
| 21 | `visibility` | `uint32` | `optional` | `` |  |
| 22 | `flags` | `uint32` | `optional` | `` |  |
| 23 | `workshop_file` | `bool` | `optional` | `` |  |
| 24 | `workshop_accepted` | `bool` | `optional` | `` |  |
| 25 | `show_subscribe_all` | `bool` | `optional` | `` |  |
| 26 | `num_comments_developer` | `int32` | `optional` | `` |  |
| 27 | `num_comments_public` | `int32` | `optional` | `` |  |
| 28 | `banned` | `bool` | `optional` | `` |  |
| 29 | `ban_reason` | `string` | `optional` | `` |  |
| 30 | `banner` | `fixed64` | `optional` | `` |  |
| 31 | `can_be_deleted` | `bool` | `optional` | `` |  |
| 32 | `incompatible` | `bool` | `optional` | `` |  |
| 33 | `app_name` | `string` | `optional` | `` |  |
| 34 | `file_type` | `uint32` | `optional` | `` |  |
| 35 | `can_subscribe` | `bool` | `optional` | `` |  |
| 36 | `subscriptions` | `uint32` | `optional` | `` |  |
| 37 | `favorited` | `uint32` | `optional` | `` |  |
| 38 | `followers` | `uint32` | `optional` | `` |  |
| 39 | `lifetime_subscriptions` | `uint32` | `optional` | `` |  |
| 40 | `lifetime_favorited` | `uint32` | `optional` | `` |  |
| 41 | `lifetime_followers` | `uint32` | `optional` | `` |  |
| 42 | `views` | `uint32` | `optional` | `` |  |
| 43 | `image_width` | `uint32` | `optional` | `` |  |
| 44 | `image_height` | `uint32` | `optional` | `` |  |
| 45 | `image_url` | `string` | `optional` | `` |  |
| 46 | `spoiler_tag` | `bool` | `optional` | `` |  |
| 47 | `shortcutid` | `uint32` | `optional` | `` |  |
| 48 | `shortcutname` | `string` | `optional` | `` |  |
| 49 | `num_children` | `uint32` | `optional` | `` |  |
| 50 | `num_reports` | `uint32` | `optional` | `` |  |
| 51 | `previews` | `.PublishedFileDetails.Preview` | `repeated` | `` |  |
| 52 | `tags` | `.PublishedFileDetails.Tag` | `repeated` | `` |  |
| 53 | `children` | `.PublishedFileDetails.Child` | `repeated` | `` |  |
| 54 | `kvtags` | `.PublishedFileDetails.KVTag` | `repeated` | `` |  |
| 55 | `vote_data` | `.PublishedFileDetails.VoteData` | `optional` | `` |  |
| 56 | `time_subscribed` | `uint32` | `optional` | `` | (description) = "Only valid in PublishedFile.GetUserFiles and not normal PublishedFile.GetDetail calls" |

</details>

<details>
<summary><code>PublishedFileDetails.Tag</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `PublishedFileDetails`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `tag` | `string` | `optional` | `` |  |
| 2 | `adminonly` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>PublishedFileDetails.Preview</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `PublishedFileDetails`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `previewid` | `uint64` | `optional` | `` |  |
| 2 | `sortorder` | `uint32` | `optional` | `` |  |
| 3 | `url` | `string` | `optional` | `` |  |
| 4 | `size` | `uint32` | `optional` | `` |  |
| 5 | `filename` | `string` | `optional` | `` |  |
| 6 | `youtubevideoid` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>PublishedFileDetails.Child</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `PublishedFileDetails`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `publishedfileid` | `uint64` | `optional` | `` |  |
| 2 | `sortorder` | `uint32` | `optional` | `` |  |
| 3 | `file_type` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>PublishedFileDetails.KVTag</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `PublishedFileDetails`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `key` | `string` | `optional` | `` |  |
| 2 | `value` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>PublishedFileDetails.VoteData</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `PublishedFileDetails`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `score` | `float` | `optional` | `` |  |
| 2 | `votes_up` | `uint32` | `optional` | `` |  |
| 3 | `votes_down` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CPublishedFile_GetDetails_Response</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `publishedfiledetails` | `.PublishedFileDetails` | `repeated` | `` |  |

</details>

<details>
<summary><code>CPublishedFile_GetUserFiles_Request</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `appid` | `uint32` | `optional` | `` | (description) = "App Id to retrieve published files from." |
| 3 | `page` | `uint32` | `optional` | `` | default = 1, (description) = "(Optional) Starting page for results." |
| 4 | `numperpage` | `uint32` | `optional` | `` | default = 1, (description) = "(Optional) The number of results, per page to return." |
| 6 | `sortmethod` | `string` | `optional` | `` | default = "lastupdated", (description) = "(Optional) Sorting method to use on returned values." |
| 7 | `totalonly` | `bool` | `optional` | `` | (description) = "(Optional) If true, only return the total number of files that satisfy this query." |
| 9 | `privacy` | `uint32` | `optional` | `` | (description) = "(optional) Filter by privacy settings." |
| 10 | `ids_only` | `bool` | `optional` | `` | (description) = "(Optional) If true, only return the published file ids of files that satisfy this query." |
| 11 | `requiredtags` | `string` | `repeated` | `` | (description) = "(Optional) Tags that must be present on a published file to satisfy the query." |
| 12 | `excludedtags` | `string` | `repeated` | `` | (description) = "(Optional) Tags that must NOT be present on a published file to satisfy the query." |

</details>

<details>
<summary><code>CPublishedFile_GetUserFiles_Response</code> — fields: 4; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `total` | `uint32` | `optional` | `` |  |
| 2 | `startindex` | `uint32` | `optional` | `` |  |
| 3 | `publishedfiledetails` | `.PublishedFileDetails` | `repeated` | `` |  |
| 4 | `apps` | `.CPublishedFile_GetUserFiles_Response.App` | `repeated` | `` |  |

</details>

<details>
<summary><code>CPublishedFile_GetUserFiles_Response.App</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CPublishedFile_GetUserFiles_Response`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `appid` | `uint32` | `optional` | `` |  |
| 2 | `name` | `string` | `optional` | `` |  |
| 3 | `shortcutid` | `uint32` | `optional` | `` |  |
| 4 | `private` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CPublishedFile_Update_Request</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `appid` | `uint32` | `optional` | `` | (description) = "App Id this published file belongs to." |
| 2 | `publishedfileid` | `fixed64` | `optional` | `` | (description) = "Published file id of the file we'd like update." |
| 3 | `title` | `string` | `optional` | `` | (description) = "(Optional) Title of the published file." |
| 4 | `file_description` | `string` | `optional` | `` | (description) = "(Optional) Description of the published file." |
| 5 | `visibility` | `uint32` | `optional` | `` | (description) = "(Optional) Visibility of the published file." |
| 6 | `tags` | `string` | `repeated` | `` | (description) = "(Optional) Set of tags for the published file." |
| 7 | `filename` | `string` | `optional` | `` | (description) = "(Optional) Filename for the published file." |
| 8 | `preview_filename` | `string` | `optional` | `` | (description) = "(Optional) Preview filename for the published file." |

</details>

<details>
<summary><code>CPublishedFile_Update_Response</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CPublishedFile_RefreshVotingQueue_Request</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `appid` | `uint32` | `optional` | `` |  |
| 2 | `matching_file_type` | `uint32` | `optional` | `` | (description) = "EPublishedFileInfoMatchingFileType" |
| 3 | `tags` | `string` | `repeated` | `` | (description) = "Include files that have all the tags or any of the tags if match_all_tags is set to false." |
| 4 | `match_all_tags` | `bool` | `optional` | `` | default = true, (description) = "If true, then files must have all the tags specified.  If false, then must have at least one of the tags specified." |
| 5 | `excluded_tags` | `string` | `repeated` | `` | (description) = "Exclude any files that have any of these tags." |
| 6 | `desired_queue_size` | `uint32` | `optional` | `` | (description) = "Desired number of items in the voting queue.  May be clamped by the server" |

</details>

<details>
<summary><code>CPublishedFile_RefreshVotingQueue_Response</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

## Enums

Expand any enum to inspect all values.

*(No enums in this proto file.)*
