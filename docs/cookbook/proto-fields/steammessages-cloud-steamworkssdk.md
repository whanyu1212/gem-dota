# steammessages_cloud.steamworkssdk.proto

- Module: `steammessages_cloud.steamworkssdk_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **1**
- Messages: **9** (top-level: 9)
- Enums: **0** (top-level: 0)

## Imports

- `steammessages_unified_base.steamworkssdk.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CCloud_GetUploadServerInfo_Request</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `appid` | `uint32` | `optional` | `` | (description) = "App ID to which a file will be uploaded to." |

</details>

<details>
<summary><code>CCloud_GetUploadServerInfo_Response</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `server_url` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CCloud_GetFileDetails_Request</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ugcid` | `uint64` | `optional` | `` | (description) = "ID of the Cloud file to get details for." |
| 2 | `appid` | `uint32` | `optional` | `` | (description) = "App ID the file belongs to." |

</details>

<details>
<summary><code>CCloud_UserFile</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `appid` | `uint32` | `optional` | `` |  |
| 2 | `ugcid` | `uint64` | `optional` | `` |  |
| 3 | `filename` | `string` | `optional` | `` |  |
| 4 | `timestamp` | `uint64` | `optional` | `` |  |
| 5 | `file_size` | `uint32` | `optional` | `` |  |
| 6 | `url` | `string` | `optional` | `` |  |
| 7 | `steamid_creator` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CCloud_GetFileDetails_Response</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `details` | `.CCloud_UserFile` | `optional` | `` |  |

</details>

<details>
<summary><code>CCloud_EnumerateUserFiles_Request</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `appid` | `uint32` | `optional` | `` | (description) = "App ID to enumerate the files of." |
| 2 | `extended_details` | `bool` | `optional` | `` | (description) = "(Optional) Get extended details back on the files found. Defaults to only returned the app Id and UGC Id of the files found." |
| 3 | `count` | `uint32` | `optional` | `` | (description) = "(Optional) Maximum number of results to return on this call. Defaults to a maximum of 500 files returned." |
| 4 | `start_index` | `uint32` | `optional` | `` | (description) = "(Optional) Starting index to begin enumeration at. Defaults to the beginning of the list." |

</details>

<details>
<summary><code>CCloud_EnumerateUserFiles_Response</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `files` | `.CCloud_UserFile` | `repeated` | `` |  |
| 2 | `total_files` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CCloud_Delete_Request</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `filename` | `string` | `optional` | `` |  |
| 2 | `appid` | `uint32` | `optional` | `` | (description) = "App ID the file belongs to." |

</details>

<details>
<summary><code>CCloud_Delete_Response</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

## Enums

Expand any enum to inspect all values.

*(No enums in this proto file.)*
