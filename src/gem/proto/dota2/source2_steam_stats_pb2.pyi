from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ESource2PlayStatsFieldType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Source2PlayStats_Invalid: _ClassVar[ESource2PlayStatsFieldType]
    Source2PlayStats_UInt64: _ClassVar[ESource2PlayStatsFieldType]
    Source2PlayStats_UInt32: _ClassVar[ESource2PlayStatsFieldType]
    Source2PlayStats_UInt16: _ClassVar[ESource2PlayStatsFieldType]
    Source2PlayStats_UInt8: _ClassVar[ESource2PlayStatsFieldType]
    Source2PlayStats_Int64: _ClassVar[ESource2PlayStatsFieldType]
    Source2PlayStats_Int32: _ClassVar[ESource2PlayStatsFieldType]
    Source2PlayStats_Int16: _ClassVar[ESource2PlayStatsFieldType]
    Source2PlayStats_Int8: _ClassVar[ESource2PlayStatsFieldType]
    Source2PlayStats_Float64: _ClassVar[ESource2PlayStatsFieldType]
    Source2PlayStats_Float32: _ClassVar[ESource2PlayStatsFieldType]
    Source2PlayStats_Bool: _ClassVar[ESource2PlayStatsFieldType]
    Source2PlayStats_String: _ClassVar[ESource2PlayStatsFieldType]
    Source2PlayStats_LowCardinalityString: _ClassVar[ESource2PlayStatsFieldType]
    Source2PlayStats_UTCDateTime: _ClassVar[ESource2PlayStatsFieldType]
    Source2PlayStats_SteamIDTrustBucket: _ClassVar[ESource2PlayStatsFieldType]
    Source2PlayStats_SteamIDTrustBucketMin: _ClassVar[ESource2PlayStatsFieldType]
Source2PlayStats_Invalid: ESource2PlayStatsFieldType
Source2PlayStats_UInt64: ESource2PlayStatsFieldType
Source2PlayStats_UInt32: ESource2PlayStatsFieldType
Source2PlayStats_UInt16: ESource2PlayStatsFieldType
Source2PlayStats_UInt8: ESource2PlayStatsFieldType
Source2PlayStats_Int64: ESource2PlayStatsFieldType
Source2PlayStats_Int32: ESource2PlayStatsFieldType
Source2PlayStats_Int16: ESource2PlayStatsFieldType
Source2PlayStats_Int8: ESource2PlayStatsFieldType
Source2PlayStats_Float64: ESource2PlayStatsFieldType
Source2PlayStats_Float32: ESource2PlayStatsFieldType
Source2PlayStats_Bool: ESource2PlayStatsFieldType
Source2PlayStats_String: ESource2PlayStatsFieldType
Source2PlayStats_LowCardinalityString: ESource2PlayStatsFieldType
Source2PlayStats_UTCDateTime: ESource2PlayStatsFieldType
Source2PlayStats_SteamIDTrustBucket: ESource2PlayStatsFieldType
Source2PlayStats_SteamIDTrustBucketMin: ESource2PlayStatsFieldType

class CMsgSource2SystemSpecs(_message.Message):
    __slots__ = ("cpu_id", "cpu_brand", "cpu_model", "cpu_num_physical", "ram_physical_total_mb", "gpu_rendersystem_dll_name", "gpu_vendor_id", "gpu_driver_name", "gpu_driver_version_high", "gpu_driver_version_low", "gpu_dx_support_level", "gpu_texture_memory_size_mb", "backbuffer_width", "backbuffer_height")
    CPU_ID_FIELD_NUMBER: _ClassVar[int]
    CPU_BRAND_FIELD_NUMBER: _ClassVar[int]
    CPU_MODEL_FIELD_NUMBER: _ClassVar[int]
    CPU_NUM_PHYSICAL_FIELD_NUMBER: _ClassVar[int]
    RAM_PHYSICAL_TOTAL_MB_FIELD_NUMBER: _ClassVar[int]
    GPU_RENDERSYSTEM_DLL_NAME_FIELD_NUMBER: _ClassVar[int]
    GPU_VENDOR_ID_FIELD_NUMBER: _ClassVar[int]
    GPU_DRIVER_NAME_FIELD_NUMBER: _ClassVar[int]
    GPU_DRIVER_VERSION_HIGH_FIELD_NUMBER: _ClassVar[int]
    GPU_DRIVER_VERSION_LOW_FIELD_NUMBER: _ClassVar[int]
    GPU_DX_SUPPORT_LEVEL_FIELD_NUMBER: _ClassVar[int]
    GPU_TEXTURE_MEMORY_SIZE_MB_FIELD_NUMBER: _ClassVar[int]
    BACKBUFFER_WIDTH_FIELD_NUMBER: _ClassVar[int]
    BACKBUFFER_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    cpu_id: str
    cpu_brand: str
    cpu_model: int
    cpu_num_physical: int
    ram_physical_total_mb: int
    gpu_rendersystem_dll_name: str
    gpu_vendor_id: int
    gpu_driver_name: str
    gpu_driver_version_high: int
    gpu_driver_version_low: int
    gpu_dx_support_level: int
    gpu_texture_memory_size_mb: int
    backbuffer_width: int
    backbuffer_height: int
    def __init__(self, cpu_id: _Optional[str] = ..., cpu_brand: _Optional[str] = ..., cpu_model: _Optional[int] = ..., cpu_num_physical: _Optional[int] = ..., ram_physical_total_mb: _Optional[int] = ..., gpu_rendersystem_dll_name: _Optional[str] = ..., gpu_vendor_id: _Optional[int] = ..., gpu_driver_name: _Optional[str] = ..., gpu_driver_version_high: _Optional[int] = ..., gpu_driver_version_low: _Optional[int] = ..., gpu_dx_support_level: _Optional[int] = ..., gpu_texture_memory_size_mb: _Optional[int] = ..., backbuffer_width: _Optional[int] = ..., backbuffer_height: _Optional[int] = ...) -> None: ...

class CMsgSource2VProfLiteReportItem(_message.Message):
    __slots__ = ("name", "active_samples", "active_samples_1secmax", "usec_max", "usec_avg_active", "usec_p50_active", "usec_p99_active", "usec_avg_all", "usec_p50_all", "usec_p99_all", "usec_1secmax_avg_active", "usec_1secmax_p50_active", "usec_1secmax_p95_active", "usec_1secmax_p99_active", "usec_1secmax_avg_all", "usec_1secmax_p50_all", "usec_1secmax_p95_all", "usec_1secmax_p99_all")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_SAMPLES_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_SAMPLES_1SECMAX_FIELD_NUMBER: _ClassVar[int]
    USEC_MAX_FIELD_NUMBER: _ClassVar[int]
    USEC_AVG_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    USEC_P50_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    USEC_P99_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    USEC_AVG_ALL_FIELD_NUMBER: _ClassVar[int]
    USEC_P50_ALL_FIELD_NUMBER: _ClassVar[int]
    USEC_P99_ALL_FIELD_NUMBER: _ClassVar[int]
    USEC_1SECMAX_AVG_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    USEC_1SECMAX_P50_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    USEC_1SECMAX_P95_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    USEC_1SECMAX_P99_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    USEC_1SECMAX_AVG_ALL_FIELD_NUMBER: _ClassVar[int]
    USEC_1SECMAX_P50_ALL_FIELD_NUMBER: _ClassVar[int]
    USEC_1SECMAX_P95_ALL_FIELD_NUMBER: _ClassVar[int]
    USEC_1SECMAX_P99_ALL_FIELD_NUMBER: _ClassVar[int]
    name: str
    active_samples: int
    active_samples_1secmax: int
    usec_max: int
    usec_avg_active: int
    usec_p50_active: int
    usec_p99_active: int
    usec_avg_all: int
    usec_p50_all: int
    usec_p99_all: int
    usec_1secmax_avg_active: int
    usec_1secmax_p50_active: int
    usec_1secmax_p95_active: int
    usec_1secmax_p99_active: int
    usec_1secmax_avg_all: int
    usec_1secmax_p50_all: int
    usec_1secmax_p95_all: int
    usec_1secmax_p99_all: int
    def __init__(self, name: _Optional[str] = ..., active_samples: _Optional[int] = ..., active_samples_1secmax: _Optional[int] = ..., usec_max: _Optional[int] = ..., usec_avg_active: _Optional[int] = ..., usec_p50_active: _Optional[int] = ..., usec_p99_active: _Optional[int] = ..., usec_avg_all: _Optional[int] = ..., usec_p50_all: _Optional[int] = ..., usec_p99_all: _Optional[int] = ..., usec_1secmax_avg_active: _Optional[int] = ..., usec_1secmax_p50_active: _Optional[int] = ..., usec_1secmax_p95_active: _Optional[int] = ..., usec_1secmax_p99_active: _Optional[int] = ..., usec_1secmax_avg_all: _Optional[int] = ..., usec_1secmax_p50_all: _Optional[int] = ..., usec_1secmax_p95_all: _Optional[int] = ..., usec_1secmax_p99_all: _Optional[int] = ...) -> None: ...

class CMsgSource2VProfLiteReport(_message.Message):
    __slots__ = ("total", "items", "discarded_frames")
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    DISCARDED_FRAMES_FIELD_NUMBER: _ClassVar[int]
    total: CMsgSource2VProfLiteReportItem
    items: _containers.RepeatedCompositeFieldContainer[CMsgSource2VProfLiteReportItem]
    discarded_frames: int
    def __init__(self, total: _Optional[_Union[CMsgSource2VProfLiteReportItem, _Mapping]] = ..., items: _Optional[_Iterable[_Union[CMsgSource2VProfLiteReportItem, _Mapping]]] = ..., discarded_frames: _Optional[int] = ...) -> None: ...

class CMsgSource2NetworkFlowQuality(_message.Message):
    __slots__ = ("duration", "bytes_total", "bytes_total_reliable", "bytes_total_voice", "bytes_sec_p95", "bytes_sec_p99", "enginemsgs_total", "enginemsgs_sec_p95", "enginemsgs_sec_p99", "netframes_total", "netframes_dropped", "netframes_outoforder", "netframes_size_exceeds_mtu", "netframes_size_p95", "netframes_size_p99", "ticks_total", "ticks_good", "ticks_good_almost_late", "ticks_fixed_dropped", "ticks_fixed_late", "ticks_bad_dropped", "ticks_bad_late", "ticks_bad_other", "tick_missrate_samples_total", "tick_missrate_samples_perfect", "tick_missrate_samples_perfectnet", "tick_missratenet_p75_x10", "tick_missratenet_p95_x10", "tick_missratenet_p99_x10", "recvmargin_p1", "recvmargin_p5", "recvmargin_p25", "recvmargin_p50", "recvmargin_p75", "recvmargin_p95", "netframe_jitter_p50", "netframe_jitter_p99", "interval_peakjitter_p50", "interval_peakjitter_p95", "packet_misdelivery_rate_p50_x4", "packet_misdelivery_rate_p95_x4", "net_ping_p5", "net_ping_p50", "net_ping_p95")
    DURATION_FIELD_NUMBER: _ClassVar[int]
    BYTES_TOTAL_FIELD_NUMBER: _ClassVar[int]
    BYTES_TOTAL_RELIABLE_FIELD_NUMBER: _ClassVar[int]
    BYTES_TOTAL_VOICE_FIELD_NUMBER: _ClassVar[int]
    BYTES_SEC_P95_FIELD_NUMBER: _ClassVar[int]
    BYTES_SEC_P99_FIELD_NUMBER: _ClassVar[int]
    ENGINEMSGS_TOTAL_FIELD_NUMBER: _ClassVar[int]
    ENGINEMSGS_SEC_P95_FIELD_NUMBER: _ClassVar[int]
    ENGINEMSGS_SEC_P99_FIELD_NUMBER: _ClassVar[int]
    NETFRAMES_TOTAL_FIELD_NUMBER: _ClassVar[int]
    NETFRAMES_DROPPED_FIELD_NUMBER: _ClassVar[int]
    NETFRAMES_OUTOFORDER_FIELD_NUMBER: _ClassVar[int]
    NETFRAMES_SIZE_EXCEEDS_MTU_FIELD_NUMBER: _ClassVar[int]
    NETFRAMES_SIZE_P95_FIELD_NUMBER: _ClassVar[int]
    NETFRAMES_SIZE_P99_FIELD_NUMBER: _ClassVar[int]
    TICKS_TOTAL_FIELD_NUMBER: _ClassVar[int]
    TICKS_GOOD_FIELD_NUMBER: _ClassVar[int]
    TICKS_GOOD_ALMOST_LATE_FIELD_NUMBER: _ClassVar[int]
    TICKS_FIXED_DROPPED_FIELD_NUMBER: _ClassVar[int]
    TICKS_FIXED_LATE_FIELD_NUMBER: _ClassVar[int]
    TICKS_BAD_DROPPED_FIELD_NUMBER: _ClassVar[int]
    TICKS_BAD_LATE_FIELD_NUMBER: _ClassVar[int]
    TICKS_BAD_OTHER_FIELD_NUMBER: _ClassVar[int]
    TICK_MISSRATE_SAMPLES_TOTAL_FIELD_NUMBER: _ClassVar[int]
    TICK_MISSRATE_SAMPLES_PERFECT_FIELD_NUMBER: _ClassVar[int]
    TICK_MISSRATE_SAMPLES_PERFECTNET_FIELD_NUMBER: _ClassVar[int]
    TICK_MISSRATENET_P75_X10_FIELD_NUMBER: _ClassVar[int]
    TICK_MISSRATENET_P95_X10_FIELD_NUMBER: _ClassVar[int]
    TICK_MISSRATENET_P99_X10_FIELD_NUMBER: _ClassVar[int]
    RECVMARGIN_P1_FIELD_NUMBER: _ClassVar[int]
    RECVMARGIN_P5_FIELD_NUMBER: _ClassVar[int]
    RECVMARGIN_P25_FIELD_NUMBER: _ClassVar[int]
    RECVMARGIN_P50_FIELD_NUMBER: _ClassVar[int]
    RECVMARGIN_P75_FIELD_NUMBER: _ClassVar[int]
    RECVMARGIN_P95_FIELD_NUMBER: _ClassVar[int]
    NETFRAME_JITTER_P50_FIELD_NUMBER: _ClassVar[int]
    NETFRAME_JITTER_P99_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_PEAKJITTER_P50_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_PEAKJITTER_P95_FIELD_NUMBER: _ClassVar[int]
    PACKET_MISDELIVERY_RATE_P50_X4_FIELD_NUMBER: _ClassVar[int]
    PACKET_MISDELIVERY_RATE_P95_X4_FIELD_NUMBER: _ClassVar[int]
    NET_PING_P5_FIELD_NUMBER: _ClassVar[int]
    NET_PING_P50_FIELD_NUMBER: _ClassVar[int]
    NET_PING_P95_FIELD_NUMBER: _ClassVar[int]
    duration: int
    bytes_total: int
    bytes_total_reliable: int
    bytes_total_voice: int
    bytes_sec_p95: int
    bytes_sec_p99: int
    enginemsgs_total: int
    enginemsgs_sec_p95: int
    enginemsgs_sec_p99: int
    netframes_total: int
    netframes_dropped: int
    netframes_outoforder: int
    netframes_size_exceeds_mtu: int
    netframes_size_p95: int
    netframes_size_p99: int
    ticks_total: int
    ticks_good: int
    ticks_good_almost_late: int
    ticks_fixed_dropped: int
    ticks_fixed_late: int
    ticks_bad_dropped: int
    ticks_bad_late: int
    ticks_bad_other: int
    tick_missrate_samples_total: int
    tick_missrate_samples_perfect: int
    tick_missrate_samples_perfectnet: int
    tick_missratenet_p75_x10: int
    tick_missratenet_p95_x10: int
    tick_missratenet_p99_x10: int
    recvmargin_p1: int
    recvmargin_p5: int
    recvmargin_p25: int
    recvmargin_p50: int
    recvmargin_p75: int
    recvmargin_p95: int
    netframe_jitter_p50: int
    netframe_jitter_p99: int
    interval_peakjitter_p50: int
    interval_peakjitter_p95: int
    packet_misdelivery_rate_p50_x4: int
    packet_misdelivery_rate_p95_x4: int
    net_ping_p5: int
    net_ping_p50: int
    net_ping_p95: int
    def __init__(self, duration: _Optional[int] = ..., bytes_total: _Optional[int] = ..., bytes_total_reliable: _Optional[int] = ..., bytes_total_voice: _Optional[int] = ..., bytes_sec_p95: _Optional[int] = ..., bytes_sec_p99: _Optional[int] = ..., enginemsgs_total: _Optional[int] = ..., enginemsgs_sec_p95: _Optional[int] = ..., enginemsgs_sec_p99: _Optional[int] = ..., netframes_total: _Optional[int] = ..., netframes_dropped: _Optional[int] = ..., netframes_outoforder: _Optional[int] = ..., netframes_size_exceeds_mtu: _Optional[int] = ..., netframes_size_p95: _Optional[int] = ..., netframes_size_p99: _Optional[int] = ..., ticks_total: _Optional[int] = ..., ticks_good: _Optional[int] = ..., ticks_good_almost_late: _Optional[int] = ..., ticks_fixed_dropped: _Optional[int] = ..., ticks_fixed_late: _Optional[int] = ..., ticks_bad_dropped: _Optional[int] = ..., ticks_bad_late: _Optional[int] = ..., ticks_bad_other: _Optional[int] = ..., tick_missrate_samples_total: _Optional[int] = ..., tick_missrate_samples_perfect: _Optional[int] = ..., tick_missrate_samples_perfectnet: _Optional[int] = ..., tick_missratenet_p75_x10: _Optional[int] = ..., tick_missratenet_p95_x10: _Optional[int] = ..., tick_missratenet_p99_x10: _Optional[int] = ..., recvmargin_p1: _Optional[int] = ..., recvmargin_p5: _Optional[int] = ..., recvmargin_p25: _Optional[int] = ..., recvmargin_p50: _Optional[int] = ..., recvmargin_p75: _Optional[int] = ..., recvmargin_p95: _Optional[int] = ..., netframe_jitter_p50: _Optional[int] = ..., netframe_jitter_p99: _Optional[int] = ..., interval_peakjitter_p50: _Optional[int] = ..., interval_peakjitter_p95: _Optional[int] = ..., packet_misdelivery_rate_p50_x4: _Optional[int] = ..., packet_misdelivery_rate_p95_x4: _Optional[int] = ..., net_ping_p5: _Optional[int] = ..., net_ping_p50: _Optional[int] = ..., net_ping_p95: _Optional[int] = ...) -> None: ...

class CMsgSource2PerfIntervalSample(_message.Message):
    __slots__ = ("frame_time_max_ms", "frame_time_avg_ms", "frame_time_min_ms", "frame_count", "frame_time_total_ms", "tags")
    class Tag(_message.Message):
        __slots__ = ("tag", "max_value")
        TAG_FIELD_NUMBER: _ClassVar[int]
        MAX_VALUE_FIELD_NUMBER: _ClassVar[int]
        tag: str
        max_value: int
        def __init__(self, tag: _Optional[str] = ..., max_value: _Optional[int] = ...) -> None: ...
    FRAME_TIME_MAX_MS_FIELD_NUMBER: _ClassVar[int]
    FRAME_TIME_AVG_MS_FIELD_NUMBER: _ClassVar[int]
    FRAME_TIME_MIN_MS_FIELD_NUMBER: _ClassVar[int]
    FRAME_COUNT_FIELD_NUMBER: _ClassVar[int]
    FRAME_TIME_TOTAL_MS_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    frame_time_max_ms: float
    frame_time_avg_ms: float
    frame_time_min_ms: float
    frame_count: int
    frame_time_total_ms: float
    tags: _containers.RepeatedCompositeFieldContainer[CMsgSource2PerfIntervalSample.Tag]
    def __init__(self, frame_time_max_ms: _Optional[float] = ..., frame_time_avg_ms: _Optional[float] = ..., frame_time_min_ms: _Optional[float] = ..., frame_count: _Optional[int] = ..., frame_time_total_ms: _Optional[float] = ..., tags: _Optional[_Iterable[_Union[CMsgSource2PerfIntervalSample.Tag, _Mapping]]] = ...) -> None: ...

class CSource2Metrics_MatchPerfSummary_Notification(_message.Message):
    __slots__ = ("appid", "game_mode", "server_build_id", "server_popid", "server_profile", "clients", "map")
    class Client(_message.Message):
        __slots__ = ("system_specs", "profile", "build_id", "downstream_flow", "upstream_flow", "steamid", "perf_samples")
        SYSTEM_SPECS_FIELD_NUMBER: _ClassVar[int]
        PROFILE_FIELD_NUMBER: _ClassVar[int]
        BUILD_ID_FIELD_NUMBER: _ClassVar[int]
        DOWNSTREAM_FLOW_FIELD_NUMBER: _ClassVar[int]
        UPSTREAM_FLOW_FIELD_NUMBER: _ClassVar[int]
        STEAMID_FIELD_NUMBER: _ClassVar[int]
        PERF_SAMPLES_FIELD_NUMBER: _ClassVar[int]
        system_specs: CMsgSource2SystemSpecs
        profile: CMsgSource2VProfLiteReport
        build_id: int
        downstream_flow: CMsgSource2NetworkFlowQuality
        upstream_flow: CMsgSource2NetworkFlowQuality
        steamid: int
        perf_samples: _containers.RepeatedCompositeFieldContainer[CMsgSource2PerfIntervalSample]
        def __init__(self, system_specs: _Optional[_Union[CMsgSource2SystemSpecs, _Mapping]] = ..., profile: _Optional[_Union[CMsgSource2VProfLiteReport, _Mapping]] = ..., build_id: _Optional[int] = ..., downstream_flow: _Optional[_Union[CMsgSource2NetworkFlowQuality, _Mapping]] = ..., upstream_flow: _Optional[_Union[CMsgSource2NetworkFlowQuality, _Mapping]] = ..., steamid: _Optional[int] = ..., perf_samples: _Optional[_Iterable[_Union[CMsgSource2PerfIntervalSample, _Mapping]]] = ...) -> None: ...
    APPID_FIELD_NUMBER: _ClassVar[int]
    GAME_MODE_FIELD_NUMBER: _ClassVar[int]
    SERVER_BUILD_ID_FIELD_NUMBER: _ClassVar[int]
    SERVER_POPID_FIELD_NUMBER: _ClassVar[int]
    SERVER_PROFILE_FIELD_NUMBER: _ClassVar[int]
    CLIENTS_FIELD_NUMBER: _ClassVar[int]
    MAP_FIELD_NUMBER: _ClassVar[int]
    appid: int
    game_mode: str
    server_build_id: int
    server_popid: int
    server_profile: CMsgSource2VProfLiteReport
    clients: _containers.RepeatedCompositeFieldContainer[CSource2Metrics_MatchPerfSummary_Notification.Client]
    map: str
    def __init__(self, appid: _Optional[int] = ..., game_mode: _Optional[str] = ..., server_build_id: _Optional[int] = ..., server_popid: _Optional[int] = ..., server_profile: _Optional[_Union[CMsgSource2VProfLiteReport, _Mapping]] = ..., clients: _Optional[_Iterable[_Union[CSource2Metrics_MatchPerfSummary_Notification.Client, _Mapping]]] = ..., map: _Optional[str] = ...) -> None: ...

class CMsgSource2PlayStatsPackedRecordList(_message.Message):
    __slots__ = ("record_name", "field_defs", "record_count", "uint64_vals", "uint32_vals", "uint16_vals", "uint8_vals", "int64_vals", "int32_vals", "int16_vals", "int8_vals", "float64_vals", "float32_vals", "bool_vals", "string_vals", "low_cardinality_string_vals", "utcdatetime_vals", "steamidtrustbucket_vals", "trustbucket_vals")
    class FieldDef(_message.Message):
        __slots__ = ("field_name", "field_type")
        FIELD_NAME_FIELD_NUMBER: _ClassVar[int]
        FIELD_TYPE_FIELD_NUMBER: _ClassVar[int]
        field_name: str
        field_type: ESource2PlayStatsFieldType
        def __init__(self, field_name: _Optional[str] = ..., field_type: _Optional[_Union[ESource2PlayStatsFieldType, str]] = ...) -> None: ...
    class SteamIDList(_message.Message):
        __slots__ = ("steamid",)
        STEAMID_FIELD_NUMBER: _ClassVar[int]
        steamid: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, steamid: _Optional[_Iterable[int]] = ...) -> None: ...
    RECORD_NAME_FIELD_NUMBER: _ClassVar[int]
    FIELD_DEFS_FIELD_NUMBER: _ClassVar[int]
    RECORD_COUNT_FIELD_NUMBER: _ClassVar[int]
    UINT64_VALS_FIELD_NUMBER: _ClassVar[int]
    UINT32_VALS_FIELD_NUMBER: _ClassVar[int]
    UINT16_VALS_FIELD_NUMBER: _ClassVar[int]
    UINT8_VALS_FIELD_NUMBER: _ClassVar[int]
    INT64_VALS_FIELD_NUMBER: _ClassVar[int]
    INT32_VALS_FIELD_NUMBER: _ClassVar[int]
    INT16_VALS_FIELD_NUMBER: _ClassVar[int]
    INT8_VALS_FIELD_NUMBER: _ClassVar[int]
    FLOAT64_VALS_FIELD_NUMBER: _ClassVar[int]
    FLOAT32_VALS_FIELD_NUMBER: _ClassVar[int]
    BOOL_VALS_FIELD_NUMBER: _ClassVar[int]
    STRING_VALS_FIELD_NUMBER: _ClassVar[int]
    LOW_CARDINALITY_STRING_VALS_FIELD_NUMBER: _ClassVar[int]
    UTCDATETIME_VALS_FIELD_NUMBER: _ClassVar[int]
    STEAMIDTRUSTBUCKET_VALS_FIELD_NUMBER: _ClassVar[int]
    TRUSTBUCKET_VALS_FIELD_NUMBER: _ClassVar[int]
    record_name: str
    field_defs: _containers.RepeatedCompositeFieldContainer[CMsgSource2PlayStatsPackedRecordList.FieldDef]
    record_count: int
    uint64_vals: _containers.RepeatedScalarFieldContainer[int]
    uint32_vals: _containers.RepeatedScalarFieldContainer[int]
    uint16_vals: _containers.RepeatedScalarFieldContainer[int]
    uint8_vals: _containers.RepeatedScalarFieldContainer[int]
    int64_vals: _containers.RepeatedScalarFieldContainer[int]
    int32_vals: _containers.RepeatedScalarFieldContainer[int]
    int16_vals: _containers.RepeatedScalarFieldContainer[int]
    int8_vals: _containers.RepeatedScalarFieldContainer[int]
    float64_vals: _containers.RepeatedScalarFieldContainer[float]
    float32_vals: _containers.RepeatedScalarFieldContainer[float]
    bool_vals: _containers.RepeatedScalarFieldContainer[bool]
    string_vals: _containers.RepeatedScalarFieldContainer[str]
    low_cardinality_string_vals: _containers.RepeatedScalarFieldContainer[str]
    utcdatetime_vals: _containers.RepeatedScalarFieldContainer[int]
    steamidtrustbucket_vals: _containers.RepeatedScalarFieldContainer[int]
    trustbucket_vals: _containers.RepeatedCompositeFieldContainer[CMsgSource2PlayStatsPackedRecordList.SteamIDList]
    def __init__(self, record_name: _Optional[str] = ..., field_defs: _Optional[_Iterable[_Union[CMsgSource2PlayStatsPackedRecordList.FieldDef, _Mapping]]] = ..., record_count: _Optional[int] = ..., uint64_vals: _Optional[_Iterable[int]] = ..., uint32_vals: _Optional[_Iterable[int]] = ..., uint16_vals: _Optional[_Iterable[int]] = ..., uint8_vals: _Optional[_Iterable[int]] = ..., int64_vals: _Optional[_Iterable[int]] = ..., int32_vals: _Optional[_Iterable[int]] = ..., int16_vals: _Optional[_Iterable[int]] = ..., int8_vals: _Optional[_Iterable[int]] = ..., float64_vals: _Optional[_Iterable[float]] = ..., float32_vals: _Optional[_Iterable[float]] = ..., bool_vals: _Optional[_Iterable[bool]] = ..., string_vals: _Optional[_Iterable[str]] = ..., low_cardinality_string_vals: _Optional[_Iterable[str]] = ..., utcdatetime_vals: _Optional[_Iterable[int]] = ..., steamidtrustbucket_vals: _Optional[_Iterable[int]] = ..., trustbucket_vals: _Optional[_Iterable[_Union[CMsgSource2PlayStatsPackedRecordList.SteamIDList, _Mapping]]] = ...) -> None: ...

class CSource2Metrics_RecordPlayStats_Notification(_message.Message):
    __slots__ = ("record_types", "appid")
    RECORD_TYPES_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    record_types: _containers.RepeatedCompositeFieldContainer[CMsgSource2PlayStatsPackedRecordList]
    appid: int
    def __init__(self, record_types: _Optional[_Iterable[_Union[CMsgSource2PlayStatsPackedRecordList, _Mapping]]] = ..., appid: _Optional[int] = ...) -> None: ...

class CSource2Metrics_FetchMapData_Request(_message.Message):
    __slots__ = ("appid", "map_name", "game_type", "game_mode", "param", "time_span")
    APPID_FIELD_NUMBER: _ClassVar[int]
    MAP_NAME_FIELD_NUMBER: _ClassVar[int]
    GAME_TYPE_FIELD_NUMBER: _ClassVar[int]
    GAME_MODE_FIELD_NUMBER: _ClassVar[int]
    PARAM_FIELD_NUMBER: _ClassVar[int]
    TIME_SPAN_FIELD_NUMBER: _ClassVar[int]
    appid: int
    map_name: str
    game_type: int
    game_mode: int
    param: str
    time_span: int
    def __init__(self, appid: _Optional[int] = ..., map_name: _Optional[str] = ..., game_type: _Optional[int] = ..., game_mode: _Optional[int] = ..., param: _Optional[str] = ..., time_span: _Optional[int] = ...) -> None: ...

class CSource2Metrics_FetchMapData_Response(_message.Message):
    __slots__ = ("results",)
    class MapData(_message.Message):
        __slots__ = ("name", "type", "data")
        NAME_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        DATA_FIELD_NUMBER: _ClassVar[int]
        name: str
        type: str
        data: str
        def __init__(self, name: _Optional[str] = ..., type: _Optional[str] = ..., data: _Optional[str] = ...) -> None: ...
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[CSource2Metrics_FetchMapData_Response.MapData]
    def __init__(self, results: _Optional[_Iterable[_Union[CSource2Metrics_FetchMapData_Response.MapData, _Mapping]]] = ...) -> None: ...
