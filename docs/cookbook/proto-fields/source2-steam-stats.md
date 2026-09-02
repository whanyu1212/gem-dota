# source2_steam_stats.proto

- Module: `source2_steam_stats_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **0**
- Messages: **16** (top-level: 11)
- Enums: **1** (top-level: 1)

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgSource2SystemSpecs</code> — fields: 14; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `cpu_id` | `string` | `optional` |  |  |
| 2 | `cpu_brand` | `string` | `optional` |  |  |
| 3 | `cpu_model` | `uint32` | `optional` |  |  |
| 4 | `cpu_num_physical` | `uint32` | `optional` |  |  |
| 21 | `ram_physical_total_mb` | `uint32` | `optional` |  |  |
| 41 | `gpu_rendersystem_dll_name` | `string` | `optional` |  |  |
| 42 | `gpu_vendor_id` | `uint32` | `optional` |  |  |
| 43 | `gpu_driver_name` | `string` | `optional` |  |  |
| 44 | `gpu_driver_version_high` | `uint32` | `optional` |  |  |
| 45 | `gpu_driver_version_low` | `uint32` | `optional` |  |  |
| 46 | `gpu_dx_support_level` | `uint32` | `optional` |  |  |
| 47 | `gpu_texture_memory_size_mb` | `uint32` | `optional` |  |  |
| 51 | `backbuffer_width` | `uint32` | `optional` |  |  |
| 52 | `backbuffer_height` | `uint32` | `optional` |  |  |

</details>

<details>
<summary><code>CMsgSource2VProfLiteReportItem</code> — fields: 18; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` |  |  |
| 2 | `active_samples` | `uint32` | `optional` |  |  |
| 3 | `usec_max` | `uint32` | `optional` |  |  |
| 4 | `active_samples_1secmax` | `uint32` | `optional` |  |  |
| 11 | `usec_avg_active` | `uint32` | `optional` |  |  |
| 12 | `usec_p50_active` | `uint32` | `optional` |  |  |
| 13 | `usec_p99_active` | `uint32` | `optional` |  |  |
| 21 | `usec_avg_all` | `uint32` | `optional` |  |  |
| 22 | `usec_p50_all` | `uint32` | `optional` |  |  |
| 23 | `usec_p99_all` | `uint32` | `optional` |  |  |
| 31 | `usec_1secmax_avg_active` | `uint32` | `optional` |  |  |
| 32 | `usec_1secmax_p50_active` | `uint32` | `optional` |  |  |
| 33 | `usec_1secmax_p95_active` | `uint32` | `optional` |  |  |
| 34 | `usec_1secmax_p99_active` | `uint32` | `optional` |  |  |
| 41 | `usec_1secmax_avg_all` | `uint32` | `optional` |  |  |
| 42 | `usec_1secmax_p50_all` | `uint32` | `optional` |  |  |
| 43 | `usec_1secmax_p95_all` | `uint32` | `optional` |  |  |
| 44 | `usec_1secmax_p99_all` | `uint32` | `optional` |  |  |

</details>

<details>
<summary><code>CMsgSource2VProfLiteReport</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `total` | `.CMsgSource2VProfLiteReportItem` | `optional` |  |  |
| 2 | `items` | `.CMsgSource2VProfLiteReportItem` | `repeated` |  |  |
| 3 | `discarded_frames` | `uint32` | `optional` |  |  |

</details>

<details>
<summary><code>CMsgSource2NetworkFlowQuality</code> — fields: 44; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `duration` | `uint32` | `optional` |  |  |
| 5 | `bytes_total` | `uint64` | `optional` |  |  |
| 6 | `bytes_total_reliable` | `uint64` | `optional` |  |  |
| 7 | `bytes_total_voice` | `uint64` | `optional` |  |  |
| 10 | `bytes_sec_p95` | `uint32` | `optional` |  |  |
| 11 | `bytes_sec_p99` | `uint32` | `optional` |  |  |
| 20 | `enginemsgs_total` | `uint32` | `optional` |  |  |
| 21 | `enginemsgs_sec_p95` | `uint32` | `optional` |  |  |
| 22 | `enginemsgs_sec_p99` | `uint32` | `optional` |  |  |
| 30 | `netframes_total` | `uint32` | `optional` |  |  |
| 31 | `netframes_dropped` | `uint32` | `optional` |  |  |
| 32 | `netframes_outoforder` | `uint32` | `optional` |  |  |
| 34 | `netframes_size_exceeds_mtu` | `uint32` | `optional` |  |  |
| 35 | `netframes_size_p95` | `uint32` | `optional` |  |  |
| 36 | `netframes_size_p99` | `uint32` | `optional` |  |  |
| 40 | `ticks_total` | `uint32` | `optional` |  |  |
| 41 | `ticks_good` | `uint32` | `optional` |  |  |
| 42 | `ticks_good_almost_late` | `uint32` | `optional` |  |  |
| 43 | `ticks_fixed_dropped` | `uint32` | `optional` |  |  |
| 44 | `ticks_fixed_late` | `uint32` | `optional` |  |  |
| 45 | `ticks_bad_dropped` | `uint32` | `optional` |  |  |
| 46 | `ticks_bad_late` | `uint32` | `optional` |  |  |
| 47 | `ticks_bad_other` | `uint32` | `optional` |  |  |
| 50 | `tick_missrate_samples_total` | `uint32` | `optional` |  |  |
| 51 | `tick_missrate_samples_perfect` | `uint32` | `optional` |  |  |
| 52 | `tick_missrate_samples_perfectnet` | `uint32` | `optional` |  |  |
| 53 | `tick_missratenet_p75_x10` | `uint32` | `optional` |  |  |
| 54 | `tick_missratenet_p95_x10` | `uint32` | `optional` |  |  |
| 55 | `tick_missratenet_p99_x10` | `uint32` | `optional` |  |  |
| 61 | `recvmargin_p1` | `sint32` | `optional` |  |  |
| 62 | `recvmargin_p5` | `sint32` | `optional` |  |  |
| 63 | `recvmargin_p25` | `sint32` | `optional` |  |  |
| 64 | `recvmargin_p50` | `sint32` | `optional` |  |  |
| 65 | `recvmargin_p75` | `sint32` | `optional` |  |  |
| 66 | `recvmargin_p95` | `sint32` | `optional` |  |  |
| 70 | `netframe_jitter_p50` | `uint32` | `optional` |  |  |
| 71 | `netframe_jitter_p99` | `uint32` | `optional` |  |  |
| 72 | `interval_peakjitter_p50` | `uint32` | `optional` |  |  |
| 73 | `interval_peakjitter_p95` | `uint32` | `optional` |  |  |
| 74 | `packet_misdelivery_rate_p50_x4` | `uint32` | `optional` |  |  |
| 75 | `packet_misdelivery_rate_p95_x4` | `uint32` | `optional` |  |  |
| 80 | `net_ping_p5` | `uint32` | `optional` |  |  |
| 81 | `net_ping_p50` | `uint32` | `optional` |  |  |
| 82 | `net_ping_p95` | `uint32` | `optional` |  |  |

</details>

<details>
<summary><code>CMsgSource2PerfIntervalSample</code> — fields: 6; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `frame_time_max_ms` | `float` | `optional` |  |  |
| 2 | `frame_time_avg_ms` | `float` | `optional` |  |  |
| 3 | `frame_time_min_ms` | `float` | `optional` |  |  |
| 4 | `frame_count` | `int32` | `optional` |  |  |
| 5 | `frame_time_total_ms` | `float` | `optional` |  |  |
| 6 | `tags` | `.CMsgSource2PerfIntervalSample.Tag` | `repeated` |  |  |

</details>

<details>
<summary><code>CMsgSource2PerfIntervalSample.Tag</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSource2PerfIntervalSample`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `tag` | `string` | `optional` |  |  |
| 2 | `max_value` | `uint32` | `optional` |  |  |

</details>

<details>
<summary><code>CSource2Metrics_MatchPerfSummary_Notification</code> — fields: 7; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `appid` | `uint32` | `optional` |  |  |
| 2 | `game_mode` | `string` | `optional` |  |  |
| 3 | `server_build_id` | `uint32` | `optional` |  |  |
| 4 | `server_popid` | `fixed32` | `optional` |  |  |
| 10 | `server_profile` | `.CMsgSource2VProfLiteReport` | `optional` |  |  |
| 11 | `clients` | `.CSource2Metrics_MatchPerfSummary_Notification.Client` | `repeated` |  |  |
| 20 | `map` | `string` | `optional` |  |  |

</details>

<details>
<summary><code>CSource2Metrics_MatchPerfSummary_Notification.Client</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CSource2Metrics_MatchPerfSummary_Notification`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `system_specs` | `.CMsgSource2SystemSpecs` | `optional` |  |  |
| 2 | `profile` | `.CMsgSource2VProfLiteReport` | `optional` |  |  |
| 3 | `build_id` | `uint32` | `optional` |  |  |
| 4 | `downstream_flow` | `.CMsgSource2NetworkFlowQuality` | `optional` |  |  |
| 5 | `upstream_flow` | `.CMsgSource2NetworkFlowQuality` | `optional` |  |  |
| 10 | `steamid` | `fixed64` | `optional` |  |  |
| 11 | `perf_samples` | `.CMsgSource2PerfIntervalSample` | `repeated` |  |  |

</details>

<details>
<summary><code>CMsgSource2PlayStatsPackedRecordList</code> — fields: 20; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `record_name` | `string` | `optional` |  |  |
| 2 | `field_defs` | `.CMsgSource2PlayStatsPackedRecordList.FieldDef` | `repeated` |  |  |
| 3 | `record_count` | `uint32` | `optional` |  |  |
| 4 | `uint64_vals` | `uint64` | `repeated` |  | packed = true |
| 5 | `uint32_vals` | `uint32` | `repeated` |  | packed = true |
| 6 | `uint16_vals` | `uint32` | `repeated` |  | packed = true |
| 7 | `uint8_vals` | `uint32` | `repeated` |  | packed = true |
| 8 | `int64_vals` | `int64` | `repeated` |  | packed = true |
| 9 | `int32_vals` | `int32` | `repeated` |  | packed = true |
| 10 | `int16_vals` | `int32` | `repeated` |  | packed = true |
| 11 | `int8_vals` | `int32` | `repeated` |  | packed = true |
| 12 | `float64_vals` | `double` | `repeated` |  | packed = true |
| 13 | `float32_vals` | `float` | `repeated` |  | packed = true |
| 14 | `bool_vals` | `bool` | `repeated` |  | packed = true |
| 15 | `string_vals` | `string` | `repeated` |  |  |
| 16 | `low_cardinality_string_vals` | `string` | `repeated` |  |  |
| 17 | `utcdatetime_vals` | `fixed32` | `repeated` |  | packed = true |
| 18 | `steamidtrustbucket_vals` | `fixed64` | `repeated` |  | packed = true |
| 19 | `trustbucket_vals` | `.CMsgSource2PlayStatsPackedRecordList.SteamIDList` | `repeated` |  |  |
| 20 | `steamid_vals` | `uint64` | `repeated` |  | packed = true |

</details>

<details>
<summary><code>CMsgSource2PlayStatsPackedRecordList.FieldDef</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSource2PlayStatsPackedRecordList`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `field_name` | `string` | `optional` |  |  |
| 2 | `field_type` | `.ESource2PlayStatsFieldType` | `optional` |  | default = Source2PlayStats_Invalid |

</details>

<details>
<summary><code>CMsgSource2PlayStatsPackedRecordList.SteamIDList</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSource2PlayStatsPackedRecordList`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steamid` | `fixed64` | `repeated` |  | packed = true |

</details>

<details>
<summary><code>CSource2Metrics_RecordPlayStats_Notification</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `record_types` | `.CMsgSource2PlayStatsPackedRecordList` | `repeated` |  |  |
| 2 | `appid` | `uint32` | `optional` |  |  |

</details>

<details>
<summary><code>CSource2Metrics_FetchMapData_Request</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `appid` | `uint32` | `optional` |  |  |
| 2 | `map_name` | `string` | `optional` |  |  |
| 3 | `game_type` | `uint32` | `optional` |  |  |
| 4 | `game_mode` | `uint32` | `optional` |  |  |
| 5 | `param` | `string` | `optional` |  |  |
| 6 | `time_span` | `uint32` | `optional` |  |  |

</details>

<details>
<summary><code>CSource2Metrics_FetchMapData_Response</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `results` | `.CSource2Metrics_FetchMapData_Response.MapData` | `repeated` |  |  |

</details>

<details>
<summary><code>CSource2Metrics_FetchMapData_Response.MapData</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CSource2Metrics_FetchMapData_Response`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` |  |  |
| 2 | `type` | `string` | `optional` |  |  |
| 3 | `data` | `string` | `optional` |  |  |

</details>

<details>
<summary><code>CUserMessage_UserSentBugBug</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `command_line` | `string` | `optional` |  |  |
| 2 | `autoexec_cfg` | `string` | `optional` |  |  |
| 3 | `system_specs` | `.CMsgSource2SystemSpecs` | `optional` |  |  |
| 4 | `build_id` | `uint32` | `optional` |  |  |
| 5 | `osversion` | `int32` | `optional` |  |  |
| 6 | `command_logs` | `string` | `optional` |  |  |
| 7 | `bugbug_no` | `int32` | `optional` |  |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>ESource2PlayStatsFieldType</code> — values: 18</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `Source2PlayStats_Invalid` | 0 |
| `Source2PlayStats_UInt64` | 1 |
| `Source2PlayStats_UInt32` | 2 |
| `Source2PlayStats_UInt16` | 3 |
| `Source2PlayStats_UInt8` | 4 |
| `Source2PlayStats_Int64` | 5 |
| `Source2PlayStats_Int32` | 6 |
| `Source2PlayStats_Int16` | 7 |
| `Source2PlayStats_Int8` | 8 |
| `Source2PlayStats_Float64` | 9 |
| `Source2PlayStats_Float32` | 10 |
| `Source2PlayStats_Bool` | 11 |
| `Source2PlayStats_String` | 12 |
| `Source2PlayStats_LowCardinalityString` | 13 |
| `Source2PlayStats_UTCDateTime` | 14 |
| `Source2PlayStats_SteamIDTrustBucket` | 15 |
| `Source2PlayStats_SteamIDTrustBucketMin` | 16 |
| `Source2PlayStats_SteamID` | 17 |

</details>
