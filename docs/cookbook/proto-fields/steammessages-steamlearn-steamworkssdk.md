# steammessages_steamlearn.steamworkssdk.proto

- Module: `steammessages_steamlearn.steamworkssdk_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **1**
- Messages: **52** (top-level: 25)
- Enums: **7** (top-level: 7)

## Imports

- `steammessages_unified_base.steamworkssdk.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgSteamLearnDataSourceDescObject</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `elements` | `.CMsgSteamLearnDataSourceDescElement` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearnDataSourceDescElement</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `data_type` | `.ESteamLearnDataType` | `optional` | `` | default = STEAMLEARN_DATATYPE_INVALID |
| 3 | `object` | `.CMsgSteamLearnDataSourceDescObject` | `optional` | `` |  |
| 4 | `count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearnDataSource</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `id` | `uint32` | `optional` | `` |  |
| 2 | `name` | `string` | `optional` | `` |  |
| 3 | `version` | `uint32` | `optional` | `` |  |
| 4 | `source_description` | `string` | `optional` | `` |  |
| 5 | `structure` | `.CMsgSteamLearnDataSourceDescObject` | `optional` | `` |  |
| 6 | `structure_crc` | `uint32` | `optional` | `` |  |
| 7 | `cache_duration_seconds` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearnDataObject</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `elements` | `.CMsgSteamLearnDataElement` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearnDataElement</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 20 | `data_int32s` | `int32` | `repeated` | `` |  |
| 21 | `data_floats` | `float` | `repeated` | `` |  |
| 22 | `data_bools` | `bool` | `repeated` | `` |  |
| 23 | `data_strings` | `string` | `repeated` | `` |  |
| 24 | `data_objects` | `.CMsgSteamLearnDataObject` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearnData</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `data_source_id` | `uint32` | `optional` | `` |  |
| 2 | `keys` | `uint64` | `repeated` | `` |  |
| 3 | `data_object` | `.CMsgSteamLearnDataObject` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearnDataList</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `data` | `.CMsgSteamLearnData` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_RegisterDataSource_Request</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `access_token` | `string` | `optional` | `` |  |
| 3 | `data_source` | `.CMsgSteamLearnDataSource` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_RegisterDataSource_Response</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.ESteammLearnRegisterDataSourceResult` | `optional` | `` | default = STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_ERROR |
| 2 | `data_source` | `.CMsgSteamLearnDataSource` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_CacheData_Request</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `access_token` | `string` | `optional` | `` |  |
| 3 | `data` | `.CMsgSteamLearnData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_CacheData_Response</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `cache_data_result` | `.ESteamLearnCacheDataResult` | `optional` | `` | default = STEAMLEARN_CACHE_DATA_ERROR |

</details>

<details>
<summary><code>CMsgSteamLearn_SnapshotProject_Request</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `access_token` | `string` | `optional` | `` |  |
| 3 | `project_id` | `uint32` | `optional` | `` |  |
| 4 | `keys` | `uint64` | `repeated` | `` |  |
| 5 | `data` | `.CMsgSteamLearnData` | `repeated` | `` |  |
| 6 | `pending_data_limit_seconds` | `uint32` | `optional` | `` |  |
| 7 | `published_version` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_SnapshotProject_Response</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `snapshot_result` | `.ESteamLearnSnapshotProjectResult` | `optional` | `` | default = STEAMLEARN_SNAPSHOT_PROJECT_ERROR |

</details>

<details>
<summary><code>CMsgSteamLearn_BatchOperation_Request</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `cache_data_requests` | `.CMsgSteamLearn_CacheData_Request` | `repeated` | `` |  |
| 2 | `snapshot_requests` | `.CMsgSteamLearn_SnapshotProject_Request` | `repeated` | `` |  |
| 3 | `inference_requests` | `.CMsgSteamLearn_Inference_Request` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_BatchOperation_Response</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `cache_data_responses` | `.CMsgSteamLearn_CacheData_Response` | `repeated` | `` |  |
| 2 | `snapshot_responses` | `.CMsgSteamLearn_SnapshotProject_Response` | `repeated` | `` |  |
| 3 | `inference_responses` | `.CMsgSteamLearn_Inference_Response` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearnAccessTokens</code> — fields: 4; oneofs: 0; nested messages: 3; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `register_data_source_access_token` | `string` | `optional` | `` |  |
| 2 | `cache_data_access_tokens` | `.CMsgSteamLearnAccessTokens.CacheDataAccessToken` | `repeated` | `` |  |
| 3 | `snapshot_project_access_tokens` | `.CMsgSteamLearnAccessTokens.SnapshotProjectAccessToken` | `repeated` | `` |  |
| 4 | `inference_access_tokens` | `.CMsgSteamLearnAccessTokens.InferenceAccessToken` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearnAccessTokens.CacheDataAccessToken</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamLearnAccessTokens`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `data_source_id` | `uint32` | `optional` | `` |  |
| 2 | `access_token` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearnAccessTokens.SnapshotProjectAccessToken</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamLearnAccessTokens`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `project_id` | `uint32` | `optional` | `` |  |
| 2 | `access_token` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearnAccessTokens.InferenceAccessToken</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamLearnAccessTokens`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `project_id` | `uint32` | `optional` | `` |  |
| 2 | `access_token` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_GetAccessTokens_Request</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `appid` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_GetAccessTokens_Response</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `result` | `.ESteamLearnGetAccessTokensResult` | `optional` | `` | default = STEAMLEARN_GET_ACCESS_TOKENS_ERROR |
| 2 | `access_tokens` | `.CMsgSteamLearnAccessTokens` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgInferenceIterateBeamSearch</code> — fields: 8; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `beam_length` | `uint32` | `optional` | `` |  |
| 2 | `beam_width` | `uint32` | `optional` | `` |  |
| 3 | `item_decay` | `float` | `optional` | `` |  |
| 4 | `next_item_count` | `uint32` | `optional` | `` |  |
| 5 | `item_scalars` | `.CMsgInferenceIterateBeamSearch.CustomItemScalar` | `repeated` | `` |  |
| 7 | `item_sequence_end` | `uint32` | `optional` | `` |  |
| 8 | `item_sequence_end_threshold` | `float` | `optional` | `` |  |
| 9 | `repeat_multiplier` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgInferenceIterateBeamSearch.CustomItemScalar</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgInferenceIterateBeamSearch`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item` | `uint32` | `optional` | `` |  |
| 2 | `scale` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_Inference_Request</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `access_token` | `string` | `optional` | `` |  |
| 3 | `project_id` | `uint32` | `optional` | `` |  |
| 4 | `published_version` | `uint32` | `optional` | `` |  |
| 5 | `override_train_id` | `uint32` | `optional` | `` |  |
| 6 | `data` | `.CMsgSteamLearnDataList` | `optional` | `` |  |
| 7 | `additional_data` | `float` | `repeated` | `` |  |
| 8 | `keys` | `uint64` | `repeated` | `` |  |
| 9 | `named_inference` | `string` | `optional` | `` |  |
| 13 | `iterate_beam_search` | `.CMsgInferenceIterateBeamSearch` | `optional` | `` |  |
| 14 | `debug_spew` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_InferenceMetadata_Request</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `access_token` | `string` | `optional` | `` |  |
| 3 | `project_id` | `uint32` | `optional` | `` |  |
| 4 | `published_version` | `uint32` | `optional` | `` |  |
| 5 | `override_train_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_InferenceMetadataBackend_Request</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `project_id` | `uint32` | `optional` | `` |  |
| 2 | `fetch_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_InferenceMetadata_Response</code> — fields: 9; oneofs: 0; nested messages: 9; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `inference_metadata_result` | `.ESteamLearnInferenceMetadataResult` | `optional` | `` | default = STEAMLEARN_INFERENCE_METADATA_ERROR |
| 2 | `row_range` | `.CMsgSteamLearn_InferenceMetadata_Response.RowRange` | `optional` | `` |  |
| 3 | `ranges` | `.CMsgSteamLearn_InferenceMetadata_Response.Range` | `repeated` | `` |  |
| 4 | `std_devs` | `.CMsgSteamLearn_InferenceMetadata_Response.StdDev` | `repeated` | `` |  |
| 5 | `compact_tables` | `.CMsgSteamLearn_InferenceMetadata_Response.CompactTable` | `repeated` | `` |  |
| 6 | `kmeans` | `.CMsgSteamLearn_InferenceMetadata_Response.KMeans` | `repeated` | `` |  |
| 7 | `snapshot_histogram` | `.CMsgSteamLearn_InferenceMetadata_Response.SnapshotHistogram` | `optional` | `` |  |
| 8 | `app_info` | `.CMsgSteamLearn_InferenceMetadata_Response.AppInfoEntry` | `repeated` | `` |  |
| 9 | `sequence_tables` | `.CMsgSteamLearn_InferenceMetadata_Response.SequenceTable` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_InferenceMetadata_Response.RowRange</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamLearn_InferenceMetadata_Response`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `min_row` | `uint64` | `optional` | `` |  |
| 2 | `max_row` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_InferenceMetadata_Response.Range</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamLearn_InferenceMetadata_Response`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `data_element_path` | `string` | `optional` | `` |  |
| 2 | `min_value` | `float` | `optional` | `` |  |
| 3 | `max_value` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_InferenceMetadata_Response.StdDev</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamLearn_InferenceMetadata_Response`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `data_element_path` | `string` | `optional` | `` |  |
| 2 | `mean` | `float` | `optional` | `` |  |
| 3 | `std_dev` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_InferenceMetadata_Response.CompactTable</code> — fields: 3; oneofs: 0; nested messages: 3; nested enums: 0</summary>

- Parent: `CMsgSteamLearn_InferenceMetadata_Response`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `map_values` | `.CMsgSteamLearn_InferenceMetadata_Response.CompactTable.MapValuesEntry` | `repeated` | `` |  |
| 3 | `map_mappings` | `.CMsgSteamLearn_InferenceMetadata_Response.CompactTable.MapMappingsEntry` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_InferenceMetadata_Response.CompactTable.Entry</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamLearn_InferenceMetadata_Response.CompactTable`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `value` | `uint32` | `optional` | `` |  |
| 2 | `mapping` | `uint32` | `optional` | `` |  |
| 3 | `count` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_InferenceMetadata_Response.CompactTable.MapValuesEntry</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamLearn_InferenceMetadata_Response.CompactTable`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `key` | `uint32` | `optional` | `` |  |
| 2 | `value` | `.CMsgSteamLearn_InferenceMetadata_Response.CompactTable.Entry` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_InferenceMetadata_Response.CompactTable.MapMappingsEntry</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamLearn_InferenceMetadata_Response.CompactTable`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `key` | `uint32` | `optional` | `` |  |
| 2 | `value` | `.CMsgSteamLearn_InferenceMetadata_Response.CompactTable.Entry` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_InferenceMetadata_Response.SequenceTable</code> — fields: 4; oneofs: 0; nested messages: 3; nested enums: 0</summary>

- Parent: `CMsgSteamLearn_InferenceMetadata_Response`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `map_values` | `.CMsgSteamLearn_InferenceMetadata_Response.SequenceTable.MapValuesEntry` | `repeated` | `` |  |
| 3 | `map_mappings` | `.CMsgSteamLearn_InferenceMetadata_Response.SequenceTable.MapMappingsEntry` | `repeated` | `` |  |
| 4 | `total_count` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_InferenceMetadata_Response.SequenceTable.Entry</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamLearn_InferenceMetadata_Response.SequenceTable`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `values` | `uint32` | `repeated` | `` |  |
| 2 | `crc` | `uint32` | `optional` | `` |  |
| 3 | `count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_InferenceMetadata_Response.SequenceTable.MapValuesEntry</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamLearn_InferenceMetadata_Response.SequenceTable`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `key` | `uint32` | `optional` | `` |  |
| 2 | `value` | `.CMsgSteamLearn_InferenceMetadata_Response.SequenceTable.Entry` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_InferenceMetadata_Response.SequenceTable.MapMappingsEntry</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamLearn_InferenceMetadata_Response.SequenceTable`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `key` | `string` | `optional` | `` |  |
| 2 | `value` | `.CMsgSteamLearn_InferenceMetadata_Response.SequenceTable.Entry` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_InferenceMetadata_Response.KMeans</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: `CMsgSteamLearn_InferenceMetadata_Response`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `clusters` | `.CMsgSteamLearn_InferenceMetadata_Response.KMeans.Cluster` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_InferenceMetadata_Response.KMeans.Cluster</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamLearn_InferenceMetadata_Response.KMeans`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `x` | `float` | `optional` | `` |  |
| 2 | `y` | `float` | `optional` | `` |  |
| 3 | `radius` | `float` | `optional` | `` |  |
| 4 | `radius_75pct` | `float` | `optional` | `` |  |
| 5 | `radius_50pct` | `float` | `optional` | `` |  |
| 6 | `radius_25pct` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_InferenceMetadata_Response.SnapshotHistogram</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamLearn_InferenceMetadata_Response`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `min_value` | `float` | `optional` | `` |  |
| 2 | `max_value` | `float` | `optional` | `` |  |
| 3 | `num_buckets` | `uint32` | `optional` | `` |  |
| 4 | `bucket_counts` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_InferenceMetadata_Response.AppInfo</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamLearn_InferenceMetadata_Response`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `country_allow` | `string` | `optional` | `` |  |
| 2 | `country_deny` | `string` | `optional` | `` |  |
| 3 | `platform_win` | `bool` | `optional` | `` |  |
| 4 | `platform_mac` | `bool` | `optional` | `` |  |
| 5 | `platform_linux` | `bool` | `optional` | `` |  |
| 6 | `adult_violence` | `bool` | `optional` | `` |  |
| 7 | `adult_sex` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_InferenceMetadata_Response.AppInfoEntry</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamLearn_InferenceMetadata_Response`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `key` | `uint32` | `optional` | `` |  |
| 2 | `value` | `.CMsgSteamLearn_InferenceMetadata_Response.AppInfo` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_InferenceBackend_Response</code> — fields: 1; oneofs: 0; nested messages: 7; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `outputs` | `.CMsgSteamLearn_InferenceBackend_Response.Output` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_InferenceBackend_Response.Sequence</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamLearn_InferenceBackend_Response`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `value` | `float` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_InferenceBackend_Response.RegressionOutput</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamLearn_InferenceBackend_Response`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `value` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_InferenceBackend_Response.NamedInferenceOutput</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamLearn_InferenceBackend_Response`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 3 | `value` | `float` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_InferenceBackend_Response.BinaryCrossEntropyOutput</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamLearn_InferenceBackend_Response`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `value` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_InferenceBackend_Response.MutliBinaryCrossEntropyOutput</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamLearn_InferenceBackend_Response`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `weight` | `float` | `repeated` | `` |  |
| 2 | `value` | `float` | `repeated` | `` |  |
| 3 | `value_sequence` | `.CMsgSteamLearn_InferenceBackend_Response.Sequence` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_InferenceBackend_Response.CategoricalCrossEntropyOutput</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamLearn_InferenceBackend_Response`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `weight` | `float` | `repeated` | `` |  |
| 2 | `value` | `float` | `repeated` | `` |  |
| 3 | `value_sequence` | `.CMsgSteamLearn_InferenceBackend_Response.Sequence` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_InferenceBackend_Response.Output</code> — fields: 5; oneofs: 1; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSteamLearn_InferenceBackend_Response`
- Oneofs: `ResponseType`

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `binary_crossentropy` | `.CMsgSteamLearn_InferenceBackend_Response.BinaryCrossEntropyOutput` | `oneof` | `ResponseType` |  |
| 2 | `categorical_crossentropy` | `.CMsgSteamLearn_InferenceBackend_Response.CategoricalCrossEntropyOutput` | `oneof` | `ResponseType` |  |
| 3 | `multi_binary_crossentropy` | `.CMsgSteamLearn_InferenceBackend_Response.MutliBinaryCrossEntropyOutput` | `oneof` | `ResponseType` |  |
| 4 | `regression` | `.CMsgSteamLearn_InferenceBackend_Response.RegressionOutput` | `oneof` | `ResponseType` |  |
| 5 | `named_inference` | `.CMsgSteamLearn_InferenceBackend_Response.NamedInferenceOutput` | `oneof` | `ResponseType` |  |

</details>

<details>
<summary><code>CMsgSteamLearn_Inference_Response</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `inference_result` | `.ESteamLearnInferenceResult` | `optional` | `` | default = STEAMLEARN_INFERENCE_ERROR |
| 2 | `backend_response` | `.CMsgSteamLearn_InferenceBackend_Response` | `optional` | `` |  |
| 3 | `keys` | `uint64` | `repeated` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>ESteamLearnDataType</code> — values: 6</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `STEAMLEARN_DATATYPE_INVALID` | 0 |
| `STEAMLEARN_DATATYPE_INT32` | 1 |
| `STEAMLEARN_DATATYPE_FLOAT32` | 2 |
| `STEAMLEARN_DATATYPE_BOOL` | 3 |
| `STEAMLEARN_DATATYPE_STRING` | 4 |
| `STEAMLEARN_DATATYPE_OBJECT` | 5 |

</details>

<details>
<summary><code>ESteammLearnRegisterDataSourceResult</code> — values: 11</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_ERROR` | 0 |
| `STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_SUCCESS_CREATED` | 1 |
| `STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_SUCCESS_FOUND` | 2 |
| `STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_ERROR_GENERIC` | 3 |
| `STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_ERROR_INVALID_NAME` | 4 |
| `STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_ERROR_INVALID_VERSION` | 5 |
| `STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_ERROR_DATA_CHANGED` | 6 |
| `STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_ERROR_DATA_INVALID` | 7 |
| `STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_ERROR_FORBIDDEN` | 8 |
| `STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_ERROR_INVALID_TIMESTAMP` | 9 |
| `STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_DISABLED` | 10 |

</details>

<details>
<summary><code>ESteamLearnCacheDataResult</code> — values: 8</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `STEAMLEARN_CACHE_DATA_ERROR` | 0 |
| `STEAMLEARN_CACHE_DATA_SUCCESS` | 1 |
| `STEAMLEARN_CACHE_DATA_ERROR_UNKNOWN_DATA_SOURCE` | 2 |
| `STEAMLEARN_CACHE_DATA_ERROR_UNCACHED_DATA_SOURCE` | 3 |
| `STEAMLEARN_CACHE_DATA_ERROR_INVALID_KEYS` | 4 |
| `STEAMLEARN_CACHE_DATA_ERROR_FORBIDDEN` | 5 |
| `STEAMLEARN_CACHE_DATA_ERROR_INVALID_TIMESTAMP` | 6 |
| `STEAMLEARN_CACHE_DATA_DISABLED` | 7 |

</details>

<details>
<summary><code>ESteamLearnSnapshotProjectResult</code> — values: 13</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `STEAMLEARN_SNAPSHOT_PROJECT_ERROR` | 0 |
| `STEAMLEARN_SNAPSHOT_PROJECT_SUCCESS_STORED` | 1 |
| `STEAMLEARN_SNAPSHOT_PROJECT_SUCCESS_QUEUED` | 2 |
| `STEAMLEARN_SNAPSHOT_PROJECT_ERROR_INVALID_PROJECT_ID` | 3 |
| `STEAMLEARN_SNAPSHOT_PROJECT_ERROR_UNKNOWN_DATA_SOURCE` | 4 |
| `STEAMLEARN_SNAPSHOT_PROJECT_ERROR_INVALID_DATA_SOURCE_KEY` | 5 |
| `STEAMLEARN_SNAPSHOT_PROJECT_ERROR_MISSING_CACHE_DURATION` | 6 |
| `STEAMLEARN_SNAPSHOT_PROJECT_ERROR_NO_PUBLISHED_CONFIG` | 7 |
| `STEAMLEARN_SNAPSHOT_PROJECT_ERROR_FORBIDDEN` | 8 |
| `STEAMLEARN_SNAPSHOT_PROJECT_ERROR_INVALID_TIMESTAMP` | 9 |
| `STEAMLEARN_SNAPSHOT_PROJECT_ERROR_INTERNAL_DATA_SOURCE_ERROR` | 10 |
| `STEAMLEARN_SNAPSHOT_PROJECT_DISABLED` | 11 |
| `STEAMLEARN_SNAPSHOT_PROJECT_ERROR_INVALID_PUBLISHED_VERSION` | 12 |

</details>

<details>
<summary><code>ESteamLearnGetAccessTokensResult</code> — values: 2</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `STEAMLEARN_GET_ACCESS_TOKENS_ERROR` | 0 |
| `STEAMLEARN_GET_ACCESS_TOKENS_SUCCESS` | 1 |

</details>

<details>
<summary><code>ESteamLearnInferenceResult</code> — values: 15</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `STEAMLEARN_INFERENCE_ERROR` | 0 |
| `STEAMLEARN_INFERENCE_SUCCESS` | 1 |
| `STEAMLEARN_INFERENCE_ERROR_INVALID_PROJECT_ID` | 2 |
| `STEAMLEARN_INFERENCE_ERROR_MISSING_CACHED_SCHEMA_DATA` | 3 |
| `STEAMLEARN_INFERENCE_ERROR_NO_PUBLISHED_CONFIG` | 4 |
| `STEAMLEARN_INFERENCE_ERROR_FORBIDDEN` | 5 |
| `STEAMLEARN_INFERENCE_ERROR_INVALID_TIMESTAMP` | 6 |
| `STEAMLEARN_INFERENCE_ERROR_INVALID_PUBLISHED_VERSION` | 7 |
| `STEAMLEARN_INFERENCE_ERROR_NO_FETCH_ID_FOUND` | 8 |
| `STEAMLEARN_INFERENCE_ERROR_TOO_BUSY` | 9 |
| `STEAMLEARN_INFERENCE_ERROR_UNSUPPLIED_DATA_FAIL` | 10 |
| `STEAMLEARN_INFERENCE_ERROR_UNSUPPLIED_DATA_NO_KEYS` | 11 |
| `STEAMLEARN_INFERENCE_DISABLED` | 12 |
| `STEAMLEARN_INFERENCE_ERROR_NO_OUTPUT` | 13 |
| `STEAMLEARN_INFERENCE_ERROR_INVALID_NAMED_INFERENCE` | 14 |

</details>

<details>
<summary><code>ESteamLearnInferenceMetadataResult</code> — values: 8</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `STEAMLEARN_INFERENCE_METADATA_ERROR` | 0 |
| `STEAMLEARN_INFERENCE_METADATA_SUCCESS` | 1 |
| `STEAMLEARN_INFERENCE_METADATA_ERROR_INVALID_PROJECT_ID` | 2 |
| `STEAMLEARN_INFERENCE_METADATA_ERROR_NO_PUBLISHED_CONFIG` | 3 |
| `STEAMLEARN_INFERENCE_METADATA_ERROR_FORBIDDEN` | 4 |
| `STEAMLEARN_INFERENCE_METADATA_ERROR_INVALID_TIMESTAMP` | 5 |
| `STEAMLEARN_INFERENCE_METADATA_ERROR_INVALID_PUBLISHED_VERSION` | 6 |
| `STEAMLEARN_INFERENCE_METADATA_ERROR_NO_FETCH_ID_FOUND` | 7 |

</details>
