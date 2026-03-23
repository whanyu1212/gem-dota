# netmessages.proto

- Module: `netmessages_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **1**
- Messages: **82** (top-level: 69)
- Enums: **13** (top-level: 12)

## Imports

- `networkbasetypes.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CCLCMsg_ClientInfo</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `send_table_crc` | `fixed32` | `optional` | `` |  |
| 2 | `server_count` | `uint32` | `optional` | `` |  |
| 3 | `is_hltv` | `bool` | `optional` | `` |  |
| 5 | `friends_id` | `uint32` | `optional` | `` |  |
| 6 | `friends_name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CCLCMsg_Move</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 3 | `data` | `bytes` | `optional` | `` |  |
| 4 | `last_command_number` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgVoiceAudio</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `format` | `.VoiceDataFormat_t` | `optional` | `` | default = VOICEDATA_FORMAT_STEAM |
| 2 | `voice_data` | `bytes` | `optional` | `` |  |
| 3 | `sequence_bytes` | `int32` | `optional` | `` |  |
| 4 | `section_number` | `uint32` | `optional` | `` |  |
| 5 | `sample_rate` | `uint32` | `optional` | `` |  |
| 6 | `uncompressed_sample_offset` | `uint32` | `optional` | `` |  |
| 7 | `num_packets` | `uint32` | `optional` | `` |  |
| 8 | `packet_offsets` | `uint32` | `repeated` | `` | packed = true |
| 9 | `voice_level` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CCLCMsg_VoiceData</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `audio` | `.CMsgVoiceAudio` | `optional` | `` |  |
| 2 | `xuid` | `fixed64` | `optional` | `` |  |
| 3 | `tick` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CCLCMsg_BaselineAck</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `baseline_tick` | `int32` | `optional` | `` |  |
| 2 | `baseline_nr` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CCLCMsg_ListenEvents</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_mask` | `fixed32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CCLCMsg_RespondCvarValue</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `cookie` | `int32` | `optional` | `` |  |
| 2 | `status_code` | `int32` | `optional` | `` |  |
| 3 | `name` | `string` | `optional` | `` |  |
| 4 | `value` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CCLCMsg_LoadingProgress</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `progress` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CCLCMsg_SplitPlayerConnect</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `playername` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CCLCMsg_SplitPlayerDisconnect</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `slot` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CCLCMsg_ServerStatus</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `simplified` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CCLCMsg_RequestPause</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `pause_type` | `.RequestPause_t` | `optional` | `` | default = RP_PAUSE |
| 2 | `pause_group` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CCLCMsg_CmdKeyValues</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `data` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CCLCMsg_RconServerDetails</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `token` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSource2SystemSpecs</code> — fields: 14; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `cpu_id` | `string` | `optional` | `` |  |
| 2 | `cpu_brand` | `string` | `optional` | `` |  |
| 3 | `cpu_model` | `uint32` | `optional` | `` |  |
| 4 | `cpu_num_physical` | `uint32` | `optional` | `` |  |
| 21 | `ram_physical_total_mb` | `uint32` | `optional` | `` |  |
| 41 | `gpu_rendersystem_dll_name` | `string` | `optional` | `` |  |
| 42 | `gpu_vendor_id` | `uint32` | `optional` | `` |  |
| 43 | `gpu_driver_name` | `string` | `optional` | `` |  |
| 44 | `gpu_driver_version_high` | `uint32` | `optional` | `` |  |
| 45 | `gpu_driver_version_low` | `uint32` | `optional` | `` |  |
| 46 | `gpu_dx_support_level` | `uint32` | `optional` | `` |  |
| 47 | `gpu_texture_memory_size_mb` | `uint32` | `optional` | `` |  |
| 51 | `backbuffer_width` | `uint32` | `optional` | `` |  |
| 52 | `backbuffer_height` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSource2VProfLiteReportItem</code> — fields: 18; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `active_samples` | `uint32` | `optional` | `` |  |
| 3 | `usec_max` | `uint32` | `optional` | `` |  |
| 4 | `active_samples_1secmax` | `uint32` | `optional` | `` |  |
| 11 | `usec_avg_active` | `uint32` | `optional` | `` |  |
| 12 | `usec_p50_active` | `uint32` | `optional` | `` |  |
| 13 | `usec_p99_active` | `uint32` | `optional` | `` |  |
| 21 | `usec_avg_all` | `uint32` | `optional` | `` |  |
| 22 | `usec_p50_all` | `uint32` | `optional` | `` |  |
| 23 | `usec_p99_all` | `uint32` | `optional` | `` |  |
| 31 | `usec_1secmax_avg_active` | `uint32` | `optional` | `` |  |
| 32 | `usec_1secmax_p50_active` | `uint32` | `optional` | `` |  |
| 33 | `usec_1secmax_p95_active` | `uint32` | `optional` | `` |  |
| 34 | `usec_1secmax_p99_active` | `uint32` | `optional` | `` |  |
| 41 | `usec_1secmax_avg_all` | `uint32` | `optional` | `` |  |
| 42 | `usec_1secmax_p50_all` | `uint32` | `optional` | `` |  |
| 43 | `usec_1secmax_p95_all` | `uint32` | `optional` | `` |  |
| 44 | `usec_1secmax_p99_all` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSource2VProfLiteReport</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `total` | `.CMsgSource2VProfLiteReportItem` | `optional` | `` |  |
| 2 | `items` | `.CMsgSource2VProfLiteReportItem` | `repeated` | `` |  |
| 3 | `discarded_frames` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSource2NetworkFlowQuality</code> — fields: 44; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `duration` | `uint32` | `optional` | `` |  |
| 5 | `bytes_total` | `uint64` | `optional` | `` |  |
| 6 | `bytes_total_reliable` | `uint64` | `optional` | `` |  |
| 7 | `bytes_total_voice` | `uint64` | `optional` | `` |  |
| 10 | `bytes_sec_p95` | `uint32` | `optional` | `` |  |
| 11 | `bytes_sec_p99` | `uint32` | `optional` | `` |  |
| 20 | `enginemsgs_total` | `uint32` | `optional` | `` |  |
| 21 | `enginemsgs_sec_p95` | `uint32` | `optional` | `` |  |
| 22 | `enginemsgs_sec_p99` | `uint32` | `optional` | `` |  |
| 30 | `netframes_total` | `uint32` | `optional` | `` |  |
| 31 | `netframes_dropped` | `uint32` | `optional` | `` |  |
| 32 | `netframes_outoforder` | `uint32` | `optional` | `` |  |
| 34 | `netframes_size_exceeds_mtu` | `uint32` | `optional` | `` |  |
| 35 | `netframes_size_p95` | `uint32` | `optional` | `` |  |
| 36 | `netframes_size_p99` | `uint32` | `optional` | `` |  |
| 40 | `ticks_total` | `uint32` | `optional` | `` |  |
| 41 | `ticks_good` | `uint32` | `optional` | `` |  |
| 42 | `ticks_good_almost_late` | `uint32` | `optional` | `` |  |
| 43 | `ticks_fixed_dropped` | `uint32` | `optional` | `` |  |
| 44 | `ticks_fixed_late` | `uint32` | `optional` | `` |  |
| 45 | `ticks_bad_dropped` | `uint32` | `optional` | `` |  |
| 46 | `ticks_bad_late` | `uint32` | `optional` | `` |  |
| 47 | `ticks_bad_other` | `uint32` | `optional` | `` |  |
| 50 | `tick_missrate_samples_total` | `uint32` | `optional` | `` |  |
| 51 | `tick_missrate_samples_perfect` | `uint32` | `optional` | `` |  |
| 52 | `tick_missrate_samples_perfectnet` | `uint32` | `optional` | `` |  |
| 53 | `tick_missratenet_p75_x10` | `uint32` | `optional` | `` |  |
| 54 | `tick_missratenet_p95_x10` | `uint32` | `optional` | `` |  |
| 55 | `tick_missratenet_p99_x10` | `uint32` | `optional` | `` |  |
| 61 | `recvmargin_p1` | `sint32` | `optional` | `` |  |
| 62 | `recvmargin_p5` | `sint32` | `optional` | `` |  |
| 63 | `recvmargin_p25` | `sint32` | `optional` | `` |  |
| 64 | `recvmargin_p50` | `sint32` | `optional` | `` |  |
| 65 | `recvmargin_p75` | `sint32` | `optional` | `` |  |
| 66 | `recvmargin_p95` | `sint32` | `optional` | `` |  |
| 70 | `netframe_jitter_p50` | `uint32` | `optional` | `` |  |
| 71 | `netframe_jitter_p99` | `uint32` | `optional` | `` |  |
| 72 | `interval_peakjitter_p50` | `uint32` | `optional` | `` |  |
| 73 | `interval_peakjitter_p95` | `uint32` | `optional` | `` |  |
| 74 | `packet_misdelivery_rate_p50_x4` | `uint32` | `optional` | `` |  |
| 75 | `packet_misdelivery_rate_p95_x4` | `uint32` | `optional` | `` |  |
| 80 | `net_ping_p5` | `uint32` | `optional` | `` |  |
| 81 | `net_ping_p50` | `uint32` | `optional` | `` |  |
| 82 | `net_ping_p95` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSource2PerfIntervalSample</code> — fields: 6; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `frame_time_max_ms` | `float` | `optional` | `` |  |
| 2 | `frame_time_avg_ms` | `float` | `optional` | `` |  |
| 3 | `frame_time_min_ms` | `float` | `optional` | `` |  |
| 4 | `frame_count` | `int32` | `optional` | `` |  |
| 5 | `frame_time_total_ms` | `float` | `optional` | `` |  |
| 6 | `tags` | `.CMsgSource2PerfIntervalSample.Tag` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSource2PerfIntervalSample.Tag</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSource2PerfIntervalSample`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `tag` | `string` | `optional` | `` |  |
| 2 | `max_value` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CCLCMsg_Diagnostic</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `system_specs` | `.CMsgSource2SystemSpecs` | `optional` | `` |  |
| 2 | `vprof_report` | `.CMsgSource2VProfLiteReport` | `optional` | `` |  |
| 3 | `downstream_flow` | `.CMsgSource2NetworkFlowQuality` | `optional` | `` |  |
| 4 | `upstream_flow` | `.CMsgSource2NetworkFlowQuality` | `optional` | `` |  |
| 5 | `perf_samples` | `.CMsgSource2PerfIntervalSample` | `repeated` | `` |  |

</details>

<details>
<summary><code>CSource2Metrics_MatchPerfSummary_Notification</code> — fields: 7; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `appid` | `uint32` | `optional` | `` |  |
| 2 | `game_mode` | `string` | `optional` | `` |  |
| 3 | `server_build_id` | `uint32` | `optional` | `` |  |
| 4 | `server_popid` | `fixed32` | `optional` | `` |  |
| 10 | `server_profile` | `.CMsgSource2VProfLiteReport` | `optional` | `` |  |
| 11 | `clients` | `.CSource2Metrics_MatchPerfSummary_Notification.Client` | `repeated` | `` |  |
| 20 | `map` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CSource2Metrics_MatchPerfSummary_Notification.Client</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CSource2Metrics_MatchPerfSummary_Notification`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `system_specs` | `.CMsgSource2SystemSpecs` | `optional` | `` |  |
| 2 | `profile` | `.CMsgSource2VProfLiteReport` | `optional` | `` |  |
| 3 | `build_id` | `uint32` | `optional` | `` |  |
| 4 | `downstream_flow` | `.CMsgSource2NetworkFlowQuality` | `optional` | `` |  |
| 5 | `upstream_flow` | `.CMsgSource2NetworkFlowQuality` | `optional` | `` |  |
| 10 | `steamid` | `fixed64` | `optional` | `` |  |
| 11 | `perf_samples` | `.CMsgSource2PerfIntervalSample` | `repeated` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_ServerInfo</code> — fields: 16; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `protocol` | `int32` | `optional` | `` |  |
| 2 | `server_count` | `int32` | `optional` | `` |  |
| 3 | `is_dedicated` | `bool` | `optional` | `` |  |
| 4 | `is_hltv` | `bool` | `optional` | `` |  |
| 6 | `c_os` | `int32` | `optional` | `` |  |
| 10 | `max_clients` | `int32` | `optional` | `` |  |
| 11 | `max_classes` | `int32` | `optional` | `` |  |
| 12 | `player_slot` | `int32` | `optional` | `` | default = -1 |
| 13 | `tick_interval` | `float` | `optional` | `` |  |
| 14 | `game_dir` | `string` | `optional` | `` |  |
| 15 | `map_name` | `string` | `optional` | `` |  |
| 16 | `sky_name` | `string` | `optional` | `` |  |
| 17 | `host_name` | `string` | `optional` | `` |  |
| 18 | `addon_name` | `string` | `optional` | `` |  |
| 19 | `game_session_config` | `.CSVCMsg_GameSessionConfiguration` | `optional` | `` |  |
| 20 | `game_session_manifest` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_ClassInfo</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `create_on_client` | `bool` | `optional` | `` |  |
| 2 | `classes` | `.CSVCMsg_ClassInfo.class_t` | `repeated` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_ClassInfo.class_t</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CSVCMsg_ClassInfo`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `class_id` | `int32` | `optional` | `` |  |
| 3 | `class_name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_SetPause</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `paused` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_VoiceInit</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `quality` | `int32` | `optional` | `` |  |
| 2 | `codec` | `string` | `optional` | `` |  |
| 3 | `version` | `int32` | `optional` | `` | default = 0 |

</details>

<details>
<summary><code>CSVCMsg_Print</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `text` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_Sounds</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `reliable_sound` | `bool` | `optional` | `` |  |
| 2 | `sounds` | `.CSVCMsg_Sounds.sounddata_t` | `repeated` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_Sounds.sounddata_t</code> — fields: 19; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CSVCMsg_Sounds`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `origin_x` | `sint32` | `optional` | `` |  |
| 2 | `origin_y` | `sint32` | `optional` | `` |  |
| 3 | `origin_z` | `sint32` | `optional` | `` |  |
| 4 | `volume` | `uint32` | `optional` | `` |  |
| 5 | `delay_value` | `float` | `optional` | `` |  |
| 6 | `sequence_number` | `int32` | `optional` | `` |  |
| 7 | `entity_index` | `int32` | `optional` | `` | default = -1 |
| 8 | `channel` | `int32` | `optional` | `` |  |
| 9 | `pitch` | `int32` | `optional` | `` |  |
| 10 | `flags` | `int32` | `optional` | `` |  |
| 11 | `sound_num` | `uint32` | `optional` | `` |  |
| 12 | `sound_num_handle` | `fixed32` | `optional` | `` |  |
| 13 | `speaker_entity` | `int32` | `optional` | `` |  |
| 14 | `random_seed` | `int32` | `optional` | `` |  |
| 15 | `sound_level` | `int32` | `optional` | `` |  |
| 16 | `is_sentence` | `bool` | `optional` | `` |  |
| 17 | `is_ambient` | `bool` | `optional` | `` |  |
| 18 | `guid` | `uint32` | `optional` | `` |  |
| 19 | `sound_resource_id` | `fixed64` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_Prefetch</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `sound_index` | `int32` | `optional` | `` |  |
| 2 | `resource_type` | `.PrefetchType` | `optional` | `` | default = PFT_SOUND |

</details>

<details>
<summary><code>CSVCMsg_SetView</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `entity_index` | `int32` | `optional` | `` | default = -1 |
| 2 | `slot` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CSVCMsg_FixAngle</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `relative` | `bool` | `optional` | `` |  |
| 2 | `angle` | `.CMsgQAngle` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_CrosshairAngle</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `angle` | `.CMsgQAngle` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_BSPDecal</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `pos` | `.CMsgVector` | `optional` | `` |  |
| 2 | `decal_texture_index` | `int32` | `optional` | `` |  |
| 3 | `entity_index` | `int32` | `optional` | `` | default = -1 |
| 4 | `model_index` | `int32` | `optional` | `` |  |
| 5 | `low_priority` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_SplitScreen</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `type` | `.ESplitScreenMessageType` | `optional` | `` | default = MSG_SPLITSCREEN_ADDUSER |
| 2 | `slot` | `int32` | `optional` | `` |  |
| 3 | `player_index` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CSVCMsg_GetCvarValue</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `cookie` | `int32` | `optional` | `` |  |
| 2 | `cvar_name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_Menu</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `dialog_type` | `int32` | `optional` | `` |  |
| 2 | `menu_key_values` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_UserMessage</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `msg_type` | `int32` | `optional` | `` |  |
| 2 | `msg_data` | `bytes` | `optional` | `` |  |
| 3 | `passthrough` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_SendTable</code> — fields: 4; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `is_end` | `bool` | `optional` | `` |  |
| 2 | `net_table_name` | `string` | `optional` | `` |  |
| 3 | `needs_decoder` | `bool` | `optional` | `` |  |
| 4 | `props` | `.CSVCMsg_SendTable.sendprop_t` | `repeated` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_SendTable.sendprop_t</code> — fields: 9; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CSVCMsg_SendTable`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `type` | `int32` | `optional` | `` |  |
| 2 | `var_name` | `string` | `optional` | `` |  |
| 3 | `flags` | `int32` | `optional` | `` |  |
| 4 | `priority` | `int32` | `optional` | `` |  |
| 5 | `dt_name` | `string` | `optional` | `` |  |
| 6 | `num_elements` | `int32` | `optional` | `` |  |
| 7 | `low_value` | `float` | `optional` | `` |  |
| 8 | `high_value` | `float` | `optional` | `` |  |
| 9 | `num_bits` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_GameEventList</code> — fields: 1; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `descriptors` | `.CSVCMsg_GameEventList.descriptor_t` | `repeated` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_GameEventList.key_t</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CSVCMsg_GameEventList`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `type` | `int32` | `optional` | `` |  |
| 2 | `name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_GameEventList.descriptor_t</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CSVCMsg_GameEventList`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `eventid` | `int32` | `optional` | `` |  |
| 2 | `name` | `string` | `optional` | `` |  |
| 3 | `keys` | `.CSVCMsg_GameEventList.key_t` | `repeated` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_PacketEntities</code> — fields: 22; oneofs: 0; nested messages: 3; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `max_entries` | `int32` | `optional` | `` |  |
| 2 | `updated_entries` | `int32` | `optional` | `` |  |
| 3 | `legacy_is_delta` | `bool` | `optional` | `` |  |
| 4 | `update_baseline` | `bool` | `optional` | `` |  |
| 5 | `baseline` | `int32` | `optional` | `` |  |
| 6 | `delta_from` | `int32` | `optional` | `` |  |
| 7 | `entity_data` | `bytes` | `optional` | `` |  |
| 8 | `pending_full_frame` | `bool` | `optional` | `` |  |
| 9 | `active_spawngroup_handle` | `uint32` | `optional` | `` |  |
| 10 | `max_spawngroup_creationsequence` | `uint32` | `optional` | `` |  |
| 11 | `last_cmd_number_executed` | `uint32` | `optional` | `` |  |
| 12 | `server_tick` | `uint32` | `optional` | `` |  |
| 13 | `serialized_entities` | `bytes` | `optional` | `` |  |
| 15 | `alternate_baselines` | `.CSVCMsg_PacketEntities.alternate_baseline_t` | `repeated` | `` |  |
| 16 | `has_pvs_vis_bits_deprecated` | `uint32` | `optional` | `` |  |
| 17 | `last_cmd_number_recv_delta` | `sint32` | `optional` | `` |  |
| 19 | `non_transmitted_entities` | `.CSVCMsg_PacketEntities.non_transmitted_entities_t` | `optional` | `` |  |
| 20 | `cq_starved_command_ticks` | `uint32` | `optional` | `` |  |
| 21 | `cq_discarded_command_ticks` | `uint32` | `optional` | `` |  |
| 22 | `cmd_recv_status` | `sint32` | `repeated` | `` | packed = true |
| 23 | `outofpvs_entity_updates` | `.CSVCMsg_PacketEntities.outofpvs_entity_updates_t` | `optional` | `` |  |
| 999 | `dev_padding` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_PacketEntities.alternate_baseline_t</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CSVCMsg_PacketEntities`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `entity_index` | `int32` | `optional` | `` |  |
| 2 | `baseline_index` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_PacketEntities.non_transmitted_entities_t</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CSVCMsg_PacketEntities`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `header_count` | `int32` | `optional` | `` |  |
| 2 | `data` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_PacketEntities.outofpvs_entity_updates_t</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CSVCMsg_PacketEntities`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `count` | `int32` | `optional` | `` |  |
| 2 | `data` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_TempEntities</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `reliable` | `bool` | `optional` | `` |  |
| 2 | `num_entries` | `int32` | `optional` | `` |  |
| 3 | `entity_data` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_CreateStringTable</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name` | `string` | `optional` | `` |  |
| 2 | `num_entries` | `int32` | `optional` | `` |  |
| 3 | `user_data_fixed_size` | `bool` | `optional` | `` |  |
| 4 | `user_data_size` | `int32` | `optional` | `` |  |
| 5 | `user_data_size_bits` | `int32` | `optional` | `` |  |
| 6 | `flags` | `int32` | `optional` | `` |  |
| 7 | `string_data` | `bytes` | `optional` | `` |  |
| 8 | `uncompressed_size` | `int32` | `optional` | `` |  |
| 9 | `data_compressed` | `bool` | `optional` | `` |  |
| 10 | `using_varint_bitcounts` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_UpdateStringTable</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `table_id` | `int32` | `optional` | `` |  |
| 2 | `num_changed_entries` | `int32` | `optional` | `` |  |
| 3 | `string_data` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_VoiceData</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `audio` | `.CMsgVoiceAudio` | `optional` | `` |  |
| 2 | `client` | `int32` | `optional` | `` | default = -1 |
| 3 | `proximity` | `bool` | `optional` | `` |  |
| 4 | `xuid` | `fixed64` | `optional` | `` |  |
| 5 | `audible_mask` | `int32` | `optional` | `` |  |
| 6 | `tick` | `uint32` | `optional` | `` |  |
| 7 | `passthrough` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_PacketReliable</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `tick` | `int32` | `optional` | `` |  |
| 2 | `messagessize` | `int32` | `optional` | `` |  |
| 3 | `state` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_FullFrameSplit</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `tick` | `int32` | `optional` | `` |  |
| 2 | `section` | `int32` | `optional` | `` |  |
| 3 | `total` | `int32` | `optional` | `` |  |
| 4 | `data` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_HLTVStatus</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `master` | `string` | `optional` | `` |  |
| 2 | `clients` | `int32` | `optional` | `` |  |
| 3 | `slots` | `int32` | `optional` | `` |  |
| 4 | `proxies` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_ServerSteamID</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steam_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_CmdKeyValues</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `data` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_RconServerDetails</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `token` | `bytes` | `optional` | `` |  |
| 2 | `details` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgIPCAddress</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `computer_guid` | `fixed64` | `optional` | `` |  |
| 2 | `process_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerPeer</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_slot` | `int32` | `optional` | `` | default = -1 |
| 2 | `steamid` | `fixed64` | `optional` | `` |  |
| 3 | `ipc` | `.CMsgIPCAddress` | `optional` | `` |  |
| 4 | `they_hear_you` | `bool` | `optional` | `` |  |
| 5 | `you_hear_them` | `bool` | `optional` | `` |  |
| 6 | `is_listenserver_host` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_PeerList</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `peer` | `.CMsgServerPeer` | `repeated` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_ClearAllStringTables</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `mapname` | `string` | `optional` | `` |  |
| 3 | `create_tables_skipped` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>ProtoFlattenedSerializerField_t</code> — fields: 12; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `var_type_sym` | `int32` | `optional` | `` |  |
| 2 | `var_name_sym` | `int32` | `optional` | `` |  |
| 3 | `bit_count` | `int32` | `optional` | `` |  |
| 4 | `low_value` | `float` | `optional` | `` |  |
| 5 | `high_value` | `float` | `optional` | `` |  |
| 6 | `encode_flags` | `int32` | `optional` | `` |  |
| 7 | `field_serializer_name_sym` | `int32` | `optional` | `` |  |
| 8 | `field_serializer_version` | `int32` | `optional` | `` |  |
| 9 | `send_node_sym` | `int32` | `optional` | `` |  |
| 10 | `var_encoder_sym` | `int32` | `optional` | `` |  |
| 11 | `polymorphic_types` | `.ProtoFlattenedSerializerField_t.polymorphic_field_t` | `repeated` | `` |  |
| 12 | `var_serializer_sym` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>ProtoFlattenedSerializerField_t.polymorphic_field_t</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `ProtoFlattenedSerializerField_t`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `polymorphic_field_serializer_name_sym` | `int32` | `optional` | `` |  |
| 2 | `polymorphic_field_serializer_version` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>ProtoFlattenedSerializer_t</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `serializer_name_sym` | `int32` | `optional` | `` |  |
| 2 | `serializer_version` | `int32` | `optional` | `` |  |
| 3 | `fields_index` | `int32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_FlattenedSerializer</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `serializers` | `.ProtoFlattenedSerializer_t` | `repeated` | `` |  |
| 2 | `symbols` | `string` | `repeated` | `` |  |
| 3 | `fields` | `.ProtoFlattenedSerializerField_t` | `repeated` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_StopSound</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guid` | `fixed32` | `optional` | `` |  |

</details>

<details>
<summary><code>CBidirMsg_RebroadcastGameEvent</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `posttoserver` | `bool` | `optional` | `` |  |
| 2 | `buftype` | `int32` | `optional` | `` |  |
| 3 | `clientbitcount` | `uint32` | `optional` | `` |  |
| 4 | `receivingclients` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CBidirMsg_RebroadcastSource</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `eventsource` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CBidirMsg_PredictionEvent</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `required` | `` |  |
| 2 | `event_data` | `bytes` | `required` | `` |  |
| 3 | `sync_type` | `uint32` | `optional` | `` |  |
| 4 | `sync_val_uint32` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerNetworkStats</code> — fields: 25; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `dedicated` | `bool` | `optional` | `` |  |
| 2 | `cpu_usage` | `int32` | `optional` | `` |  |
| 3 | `memory_used_mb` | `int32` | `optional` | `` |  |
| 4 | `memory_free_mb` | `int32` | `optional` | `` |  |
| 5 | `uptime` | `int32` | `optional` | `` |  |
| 6 | `spawn_count` | `int32` | `optional` | `` |  |
| 8 | `num_clients` | `int32` | `optional` | `` |  |
| 9 | `num_bots` | `int32` | `optional` | `` |  |
| 10 | `num_spectators` | `int32` | `optional` | `` |  |
| 11 | `num_tv_relays` | `int32` | `optional` | `` |  |
| 12 | `fps` | `float` | `optional` | `` |  |
| 17 | `ports` | `.CMsgServerNetworkStats.Port` | `repeated` | `` |  |
| 18 | `avg_ping_ms` | `float` | `optional` | `` |  |
| 19 | `avg_engine_latency_out` | `float` | `optional` | `` |  |
| 20 | `avg_packets_out` | `float` | `optional` | `` |  |
| 21 | `avg_packets_in` | `float` | `optional` | `` |  |
| 22 | `avg_loss_out` | `float` | `optional` | `` |  |
| 23 | `avg_loss_in` | `float` | `optional` | `` |  |
| 24 | `avg_data_out` | `float` | `optional` | `` |  |
| 25 | `avg_data_in` | `float` | `optional` | `` |  |
| 26 | `total_data_in` | `uint64` | `optional` | `` |  |
| 27 | `total_packets_in` | `uint64` | `optional` | `` |  |
| 28 | `total_data_out` | `uint64` | `optional` | `` |  |
| 29 | `total_packets_out` | `uint64` | `optional` | `` |  |
| 30 | `players` | `.CMsgServerNetworkStats.Player` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgServerNetworkStats.Port</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgServerNetworkStats`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `port` | `int32` | `optional` | `` |  |
| 2 | `name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerNetworkStats.Player</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgServerNetworkStats`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `steamid` | `uint64` | `optional` | `` |  |
| 2 | `remote_addr` | `string` | `optional` | `` |  |
| 4 | `ping_avg_ms` | `int32` | `optional` | `` |  |
| 5 | `packet_loss_pct` | `float` | `optional` | `` |  |
| 6 | `is_bot` | `bool` | `optional` | `` |  |
| 7 | `loss_in` | `float` | `optional` | `` |  |
| 8 | `loss_out` | `float` | `optional` | `` |  |
| 9 | `engine_latency_ms` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_HltvReplay</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `delay` | `int32` | `optional` | `` |  |
| 2 | `primary_target` | `int32` | `optional` | `` | default = -1 |
| 3 | `replay_stop_at` | `int32` | `optional` | `` |  |
| 4 | `replay_start_at` | `int32` | `optional` | `` |  |
| 5 | `replay_slowdown_begin` | `int32` | `optional` | `` |  |
| 6 | `replay_slowdown_end` | `int32` | `optional` | `` |  |
| 7 | `replay_slowdown_rate` | `float` | `optional` | `` |  |
| 8 | `reason` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CCLCMsg_HltvReplay</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `request` | `int32` | `optional` | `` |  |
| 2 | `slowdown_length` | `float` | `optional` | `` |  |
| 3 | `slowdown_rate` | `float` | `optional` | `` |  |
| 4 | `primary_target` | `int32` | `optional` | `` | default = -1 |
| 5 | `event_time` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_Broadcast_Command</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `cmd` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CCLCMsg_HltvFixupOperatorTick</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `tick` | `int32` | `optional` | `` |  |
| 2 | `props_data` | `bytes` | `optional` | `` |  |
| 3 | `origin` | `.CMsgVector` | `optional` | `` |  |
| 4 | `eye_angles` | `.CMsgQAngle` | `optional` | `` |  |
| 5 | `observer_mode` | `int32` | `optional` | `` |  |
| 6 | `cameraman_scoreboard` | `bool` | `optional` | `` |  |
| 7 | `observer_target` | `int32` | `optional` | `` |  |
| 8 | `view_offset` | `.CMsgVector` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_HltvFixupOperatorStatus</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `mode` | `uint32` | `optional` | `` |  |
| 2 | `override_operator_name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgServerUserCmd</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `data` | `bytes` | `optional` | `` |  |
| 2 | `cmd_number` | `int32` | `optional` | `` |  |
| 3 | `player_slot` | `int32` | `optional` | `` | default = -1 |
| 4 | `server_tick_executed` | `int32` | `optional` | `` |  |
| 5 | `client_tick` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_UserCommands</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `commands` | `.CMsgServerUserCmd` | `repeated` | `` |  |

</details>

<details>
<summary><code>CSVCMsg_NextMsgPredicted</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `predicted_by_player_slot` | `int32` | `optional` | `` | default = -1 |
| 2 | `message_type_id` | `uint32` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>CLC_Messages</code> — values: 14</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `clc_ClientInfo` | 20 |
| `clc_Move` | 21 |
| `clc_VoiceData` | 22 |
| `clc_BaselineAck` | 23 |
| `clc_RespondCvarValue` | 25 |
| `clc_LoadingProgress` | 27 |
| `clc_SplitPlayerConnect` | 28 |
| `clc_SplitPlayerDisconnect` | 30 |
| `clc_ServerStatus` | 31 |
| `clc_RequestPause` | 33 |
| `clc_CmdKeyValues` | 34 |
| `clc_RconServerDetails` | 35 |
| `clc_HltvReplay` | 36 |
| `clc_Diagnostic` | 37 |

</details>

<details>
<summary><code>SVC_Messages</code> — values: 31</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `svc_ServerInfo` | 40 |
| `svc_FlattenedSerializer` | 41 |
| `svc_ClassInfo` | 42 |
| `svc_SetPause` | 43 |
| `svc_CreateStringTable` | 44 |
| `svc_UpdateStringTable` | 45 |
| `svc_VoiceInit` | 46 |
| `svc_VoiceData` | 47 |
| `svc_Print` | 48 |
| `svc_Sounds` | 49 |
| `svc_SetView` | 50 |
| `svc_ClearAllStringTables` | 51 |
| `svc_CmdKeyValues` | 52 |
| `svc_BSPDecal` | 53 |
| `svc_SplitScreen` | 54 |
| `svc_PacketEntities` | 55 |
| `svc_Prefetch` | 56 |
| `svc_Menu` | 57 |
| `svc_GetCvarValue` | 58 |
| `svc_StopSound` | 59 |
| `svc_PeerList` | 60 |
| `svc_PacketReliable` | 61 |
| `svc_HLTVStatus` | 62 |
| `svc_ServerSteamID` | 63 |
| `svc_FullFrameSplit` | 70 |
| `svc_RconServerDetails` | 71 |
| `svc_UserMessage` | 72 |
| `svc_Broadcast_Command` | 74 |
| `svc_HltvFixupOperatorStatus` | 75 |
| `svc_UserCmds` | 76 |
| `svc_NextMsgPredicted` | 77 |

</details>

<details>
<summary><code>VoiceDataFormat_t</code> — values: 3</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `VOICEDATA_FORMAT_STEAM` | 0 |
| `VOICEDATA_FORMAT_ENGINE` | 1 |
| `VOICEDATA_FORMAT_OPUS` | 2 |

</details>

<details>
<summary><code>RequestPause_t</code> — values: 3</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `RP_PAUSE` | 0 |
| `RP_UNPAUSE` | 1 |
| `RP_TOGGLEPAUSE` | 2 |

</details>

<details>
<summary><code>PrefetchType</code> — values: 1</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `PFT_SOUND` | 0 |

</details>

<details>
<summary><code>ESplitScreenMessageType</code> — values: 2</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `MSG_SPLITSCREEN_ADDUSER` | 0 |
| `MSG_SPLITSCREEN_REMOVEUSER` | 1 |

</details>

<details>
<summary><code>EQueryCvarValueStatus</code> — values: 4</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `eQueryCvarValueStatus_ValueIntact` | 0 |
| `eQueryCvarValueStatus_CvarNotFound` | 1 |
| `eQueryCvarValueStatus_NotACvar` | 2 |
| `eQueryCvarValueStatus_CvarProtected` | 3 |

</details>

<details>
<summary><code>DIALOG_TYPE</code> — values: 5</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `DIALOG_MSG` | 0 |
| `DIALOG_MENU` | 1 |
| `DIALOG_TEXT` | 2 |
| `DIALOG_ENTRY` | 3 |
| `DIALOG_ASKCONNECT` | 4 |

</details>

<details>
<summary><code>SVC_Messages_LowFrequency</code> — values: 1</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `svc_dummy` | 600 |

</details>

<details>
<summary><code>Bidirectional_Messages</code> — values: 4</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `bi_RebroadcastGameEvent` | 16 |
| `bi_RebroadcastSource` | 17 |
| `bi_GameEvent` | 18 |
| `bi_PredictionEvent` | 19 |

</details>

<details>
<summary><code>Bidirectional_Messages_LowFrequency</code> — values: 2</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `bi_RelayInfo` | 700 |
| `bi_RelayPacket` | 701 |

</details>

<details>
<summary><code>ReplayEventType_t</code> — values: 5</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `REPLAY_EVENT_CANCEL` | 0 |
| `REPLAY_EVENT_DEATH` | 1 |
| `REPLAY_EVENT_GENERIC` | 2 |
| `REPLAY_EVENT_STUCK_NEED_FULL_UPDATE` | 3 |
| `REPLAY_EVENT_VICTORY` | 4 |

</details>

<details>
<summary><code>CBidirMsg_PredictionEvent.ESyncType</code> — values: 2</summary>

- Parent: `CBidirMsg_PredictionEvent`

| Name | Number |
|---|---:|
| `ST_Tick` | 0 |
| `ST_UserCmdNum` | 1 |

</details>
