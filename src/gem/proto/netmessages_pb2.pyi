from . import networkbasetypes_pb2 as _networkbasetypes_pb2
from . import source2_steam_stats_pb2 as _source2_steam_stats_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CLC_Messages(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    clc_ClientInfo: _ClassVar[CLC_Messages]
    clc_Move: _ClassVar[CLC_Messages]
    clc_VoiceData: _ClassVar[CLC_Messages]
    clc_BaselineAck: _ClassVar[CLC_Messages]
    clc_RespondCvarValue: _ClassVar[CLC_Messages]
    clc_LoadingProgress: _ClassVar[CLC_Messages]
    clc_SplitPlayerConnect: _ClassVar[CLC_Messages]
    clc_SplitPlayerDisconnect: _ClassVar[CLC_Messages]
    clc_ServerStatus: _ClassVar[CLC_Messages]
    clc_RequestPause: _ClassVar[CLC_Messages]
    clc_CmdKeyValues: _ClassVar[CLC_Messages]
    clc_RconServerDetails: _ClassVar[CLC_Messages]
    clc_HltvReplay: _ClassVar[CLC_Messages]
    clc_Diagnostic: _ClassVar[CLC_Messages]

class SVC_Messages(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    svc_ServerInfo: _ClassVar[SVC_Messages]
    svc_FlattenedSerializer: _ClassVar[SVC_Messages]
    svc_ClassInfo: _ClassVar[SVC_Messages]
    svc_SetPause: _ClassVar[SVC_Messages]
    svc_CreateStringTable: _ClassVar[SVC_Messages]
    svc_UpdateStringTable: _ClassVar[SVC_Messages]
    svc_VoiceInit: _ClassVar[SVC_Messages]
    svc_VoiceData: _ClassVar[SVC_Messages]
    svc_Print: _ClassVar[SVC_Messages]
    svc_Sounds: _ClassVar[SVC_Messages]
    svc_SetView: _ClassVar[SVC_Messages]
    svc_ClearAllStringTables: _ClassVar[SVC_Messages]
    svc_CmdKeyValues: _ClassVar[SVC_Messages]
    svc_BSPDecal: _ClassVar[SVC_Messages]
    svc_SplitScreen: _ClassVar[SVC_Messages]
    svc_PacketEntities: _ClassVar[SVC_Messages]
    svc_Prefetch: _ClassVar[SVC_Messages]
    svc_Menu: _ClassVar[SVC_Messages]
    svc_GetCvarValue: _ClassVar[SVC_Messages]
    svc_StopSound: _ClassVar[SVC_Messages]
    svc_PeerList: _ClassVar[SVC_Messages]
    svc_PacketReliable: _ClassVar[SVC_Messages]
    svc_HLTVStatus: _ClassVar[SVC_Messages]
    svc_ServerSteamID: _ClassVar[SVC_Messages]
    svc_FullFrameSplit: _ClassVar[SVC_Messages]
    svc_RconServerDetails: _ClassVar[SVC_Messages]
    svc_UserMessage: _ClassVar[SVC_Messages]
    svc_Broadcast_Command: _ClassVar[SVC_Messages]
    svc_HltvFixupOperatorStatus: _ClassVar[SVC_Messages]
    svc_UserCmds: _ClassVar[SVC_Messages]
    svc_NextMsgPredicted: _ClassVar[SVC_Messages]

class VoiceDataFormat_t(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VOICEDATA_FORMAT_STEAM: _ClassVar[VoiceDataFormat_t]
    VOICEDATA_FORMAT_ENGINE: _ClassVar[VoiceDataFormat_t]
    VOICEDATA_FORMAT_OPUS: _ClassVar[VoiceDataFormat_t]

class RequestPause_t(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RP_PAUSE: _ClassVar[RequestPause_t]
    RP_UNPAUSE: _ClassVar[RequestPause_t]
    RP_TOGGLEPAUSE: _ClassVar[RequestPause_t]

class PrefetchType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PFT_SOUND: _ClassVar[PrefetchType]

class ESplitScreenMessageType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MSG_SPLITSCREEN_ADDUSER: _ClassVar[ESplitScreenMessageType]
    MSG_SPLITSCREEN_REMOVEUSER: _ClassVar[ESplitScreenMessageType]

class EQueryCvarValueStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    eQueryCvarValueStatus_ValueIntact: _ClassVar[EQueryCvarValueStatus]
    eQueryCvarValueStatus_CvarNotFound: _ClassVar[EQueryCvarValueStatus]
    eQueryCvarValueStatus_NotACvar: _ClassVar[EQueryCvarValueStatus]
    eQueryCvarValueStatus_CvarProtected: _ClassVar[EQueryCvarValueStatus]

class DIALOG_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DIALOG_MSG: _ClassVar[DIALOG_TYPE]
    DIALOG_MENU: _ClassVar[DIALOG_TYPE]
    DIALOG_TEXT: _ClassVar[DIALOG_TYPE]
    DIALOG_ENTRY: _ClassVar[DIALOG_TYPE]
    DIALOG_ASKCONNECT: _ClassVar[DIALOG_TYPE]

class SVC_Messages_LowFrequency(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    svc_dummy: _ClassVar[SVC_Messages_LowFrequency]

class Bidirectional_Messages(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    bi_RebroadcastGameEvent: _ClassVar[Bidirectional_Messages]
    bi_RebroadcastSource: _ClassVar[Bidirectional_Messages]
    bi_GameEvent_DEPRECATED: _ClassVar[Bidirectional_Messages]
    bi_PredictionEvent: _ClassVar[Bidirectional_Messages]

class ReplayEventType_t(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REPLAY_EVENT_CANCEL: _ClassVar[ReplayEventType_t]
    REPLAY_EVENT_DEATH: _ClassVar[ReplayEventType_t]
    REPLAY_EVENT_GENERIC: _ClassVar[ReplayEventType_t]
    REPLAY_EVENT_STUCK_NEED_FULL_UPDATE: _ClassVar[ReplayEventType_t]
    REPLAY_EVENT_VICTORY: _ClassVar[ReplayEventType_t]
clc_ClientInfo: CLC_Messages
clc_Move: CLC_Messages
clc_VoiceData: CLC_Messages
clc_BaselineAck: CLC_Messages
clc_RespondCvarValue: CLC_Messages
clc_LoadingProgress: CLC_Messages
clc_SplitPlayerConnect: CLC_Messages
clc_SplitPlayerDisconnect: CLC_Messages
clc_ServerStatus: CLC_Messages
clc_RequestPause: CLC_Messages
clc_CmdKeyValues: CLC_Messages
clc_RconServerDetails: CLC_Messages
clc_HltvReplay: CLC_Messages
clc_Diagnostic: CLC_Messages
svc_ServerInfo: SVC_Messages
svc_FlattenedSerializer: SVC_Messages
svc_ClassInfo: SVC_Messages
svc_SetPause: SVC_Messages
svc_CreateStringTable: SVC_Messages
svc_UpdateStringTable: SVC_Messages
svc_VoiceInit: SVC_Messages
svc_VoiceData: SVC_Messages
svc_Print: SVC_Messages
svc_Sounds: SVC_Messages
svc_SetView: SVC_Messages
svc_ClearAllStringTables: SVC_Messages
svc_CmdKeyValues: SVC_Messages
svc_BSPDecal: SVC_Messages
svc_SplitScreen: SVC_Messages
svc_PacketEntities: SVC_Messages
svc_Prefetch: SVC_Messages
svc_Menu: SVC_Messages
svc_GetCvarValue: SVC_Messages
svc_StopSound: SVC_Messages
svc_PeerList: SVC_Messages
svc_PacketReliable: SVC_Messages
svc_HLTVStatus: SVC_Messages
svc_ServerSteamID: SVC_Messages
svc_FullFrameSplit: SVC_Messages
svc_RconServerDetails: SVC_Messages
svc_UserMessage: SVC_Messages
svc_Broadcast_Command: SVC_Messages
svc_HltvFixupOperatorStatus: SVC_Messages
svc_UserCmds: SVC_Messages
svc_NextMsgPredicted: SVC_Messages
VOICEDATA_FORMAT_STEAM: VoiceDataFormat_t
VOICEDATA_FORMAT_ENGINE: VoiceDataFormat_t
VOICEDATA_FORMAT_OPUS: VoiceDataFormat_t
RP_PAUSE: RequestPause_t
RP_UNPAUSE: RequestPause_t
RP_TOGGLEPAUSE: RequestPause_t
PFT_SOUND: PrefetchType
MSG_SPLITSCREEN_ADDUSER: ESplitScreenMessageType
MSG_SPLITSCREEN_REMOVEUSER: ESplitScreenMessageType
eQueryCvarValueStatus_ValueIntact: EQueryCvarValueStatus
eQueryCvarValueStatus_CvarNotFound: EQueryCvarValueStatus
eQueryCvarValueStatus_NotACvar: EQueryCvarValueStatus
eQueryCvarValueStatus_CvarProtected: EQueryCvarValueStatus
DIALOG_MSG: DIALOG_TYPE
DIALOG_MENU: DIALOG_TYPE
DIALOG_TEXT: DIALOG_TYPE
DIALOG_ENTRY: DIALOG_TYPE
DIALOG_ASKCONNECT: DIALOG_TYPE
svc_dummy: SVC_Messages_LowFrequency
bi_RebroadcastGameEvent: Bidirectional_Messages
bi_RebroadcastSource: Bidirectional_Messages
bi_GameEvent_DEPRECATED: Bidirectional_Messages
bi_PredictionEvent: Bidirectional_Messages
REPLAY_EVENT_CANCEL: ReplayEventType_t
REPLAY_EVENT_DEATH: ReplayEventType_t
REPLAY_EVENT_GENERIC: ReplayEventType_t
REPLAY_EVENT_STUCK_NEED_FULL_UPDATE: ReplayEventType_t
REPLAY_EVENT_VICTORY: ReplayEventType_t

class CCLCMsg_ClientInfo(_message.Message):
    __slots__ = ("send_table_crc", "server_count", "is_hltv", "friends_id", "friends_name")
    SEND_TABLE_CRC_FIELD_NUMBER: _ClassVar[int]
    SERVER_COUNT_FIELD_NUMBER: _ClassVar[int]
    IS_HLTV_FIELD_NUMBER: _ClassVar[int]
    FRIENDS_ID_FIELD_NUMBER: _ClassVar[int]
    FRIENDS_NAME_FIELD_NUMBER: _ClassVar[int]
    send_table_crc: int
    server_count: int
    is_hltv: bool
    friends_id: int
    friends_name: str
    def __init__(self, send_table_crc: _Optional[int] = ..., server_count: _Optional[int] = ..., is_hltv: bool = ..., friends_id: _Optional[int] = ..., friends_name: _Optional[str] = ...) -> None: ...

class CCLCMsg_Move(_message.Message):
    __slots__ = ("data", "last_command_number")
    DATA_FIELD_NUMBER: _ClassVar[int]
    LAST_COMMAND_NUMBER_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    last_command_number: int
    def __init__(self, data: _Optional[bytes] = ..., last_command_number: _Optional[int] = ...) -> None: ...

class CMsgVoiceAudio(_message.Message):
    __slots__ = ("format", "voice_data", "sequence_bytes", "section_number", "sample_rate", "uncompressed_sample_offset", "num_packets", "packet_offsets", "voice_level")
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    VOICE_DATA_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_BYTES_FIELD_NUMBER: _ClassVar[int]
    SECTION_NUMBER_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_RATE_FIELD_NUMBER: _ClassVar[int]
    UNCOMPRESSED_SAMPLE_OFFSET_FIELD_NUMBER: _ClassVar[int]
    NUM_PACKETS_FIELD_NUMBER: _ClassVar[int]
    PACKET_OFFSETS_FIELD_NUMBER: _ClassVar[int]
    VOICE_LEVEL_FIELD_NUMBER: _ClassVar[int]
    format: VoiceDataFormat_t
    voice_data: bytes
    sequence_bytes: int
    section_number: int
    sample_rate: int
    uncompressed_sample_offset: int
    num_packets: int
    packet_offsets: _containers.RepeatedScalarFieldContainer[int]
    voice_level: float
    def __init__(self, format: _Optional[_Union[VoiceDataFormat_t, str]] = ..., voice_data: _Optional[bytes] = ..., sequence_bytes: _Optional[int] = ..., section_number: _Optional[int] = ..., sample_rate: _Optional[int] = ..., uncompressed_sample_offset: _Optional[int] = ..., num_packets: _Optional[int] = ..., packet_offsets: _Optional[_Iterable[int]] = ..., voice_level: _Optional[float] = ...) -> None: ...

class CCLCMsg_VoiceData(_message.Message):
    __slots__ = ("audio", "xuid", "tick")
    AUDIO_FIELD_NUMBER: _ClassVar[int]
    XUID_FIELD_NUMBER: _ClassVar[int]
    TICK_FIELD_NUMBER: _ClassVar[int]
    audio: CMsgVoiceAudio
    xuid: int
    tick: int
    def __init__(self, audio: _Optional[_Union[CMsgVoiceAudio, _Mapping]] = ..., xuid: _Optional[int] = ..., tick: _Optional[int] = ...) -> None: ...

class CCLCMsg_BaselineAck(_message.Message):
    __slots__ = ("baseline_tick", "baseline_nr")
    BASELINE_TICK_FIELD_NUMBER: _ClassVar[int]
    BASELINE_NR_FIELD_NUMBER: _ClassVar[int]
    baseline_tick: int
    baseline_nr: int
    def __init__(self, baseline_tick: _Optional[int] = ..., baseline_nr: _Optional[int] = ...) -> None: ...

class CCLCMsg_ListenEvents(_message.Message):
    __slots__ = ("event_mask",)
    EVENT_MASK_FIELD_NUMBER: _ClassVar[int]
    event_mask: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, event_mask: _Optional[_Iterable[int]] = ...) -> None: ...

class CCLCMsg_RespondCvarValue(_message.Message):
    __slots__ = ("cookie", "status_code", "name", "value")
    COOKIE_FIELD_NUMBER: _ClassVar[int]
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    cookie: int
    status_code: int
    name: str
    value: str
    def __init__(self, cookie: _Optional[int] = ..., status_code: _Optional[int] = ..., name: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class CCLCMsg_LoadingProgress(_message.Message):
    __slots__ = ("progress",)
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    progress: int
    def __init__(self, progress: _Optional[int] = ...) -> None: ...

class CCLCMsg_SplitPlayerConnect(_message.Message):
    __slots__ = ("playername",)
    PLAYERNAME_FIELD_NUMBER: _ClassVar[int]
    playername: str
    def __init__(self, playername: _Optional[str] = ...) -> None: ...

class CCLCMsg_SplitPlayerDisconnect(_message.Message):
    __slots__ = ("slot",)
    SLOT_FIELD_NUMBER: _ClassVar[int]
    slot: int
    def __init__(self, slot: _Optional[int] = ...) -> None: ...

class CCLCMsg_ServerStatus(_message.Message):
    __slots__ = ("simplified",)
    SIMPLIFIED_FIELD_NUMBER: _ClassVar[int]
    simplified: bool
    def __init__(self, simplified: bool = ...) -> None: ...

class CCLCMsg_RequestPause(_message.Message):
    __slots__ = ("pause_type", "pause_group")
    PAUSE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAUSE_GROUP_FIELD_NUMBER: _ClassVar[int]
    pause_type: RequestPause_t
    pause_group: int
    def __init__(self, pause_type: _Optional[_Union[RequestPause_t, str]] = ..., pause_group: _Optional[int] = ...) -> None: ...

class CCLCMsg_CmdKeyValues(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: _Optional[bytes] = ...) -> None: ...

class CCLCMsg_RconServerDetails(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: bytes
    def __init__(self, token: _Optional[bytes] = ...) -> None: ...

class CCLCMsg_Diagnostic(_message.Message):
    __slots__ = ("system_specs", "vprof_report", "downstream_flow", "upstream_flow", "perf_samples")
    SYSTEM_SPECS_FIELD_NUMBER: _ClassVar[int]
    VPROF_REPORT_FIELD_NUMBER: _ClassVar[int]
    DOWNSTREAM_FLOW_FIELD_NUMBER: _ClassVar[int]
    UPSTREAM_FLOW_FIELD_NUMBER: _ClassVar[int]
    PERF_SAMPLES_FIELD_NUMBER: _ClassVar[int]
    system_specs: _source2_steam_stats_pb2.CMsgSource2SystemSpecs
    vprof_report: _source2_steam_stats_pb2.CMsgSource2VProfLiteReport
    downstream_flow: _source2_steam_stats_pb2.CMsgSource2NetworkFlowQuality
    upstream_flow: _source2_steam_stats_pb2.CMsgSource2NetworkFlowQuality
    perf_samples: _containers.RepeatedCompositeFieldContainer[_source2_steam_stats_pb2.CMsgSource2PerfIntervalSample]
    def __init__(self, system_specs: _Optional[_Union[_source2_steam_stats_pb2.CMsgSource2SystemSpecs, _Mapping]] = ..., vprof_report: _Optional[_Union[_source2_steam_stats_pb2.CMsgSource2VProfLiteReport, _Mapping]] = ..., downstream_flow: _Optional[_Union[_source2_steam_stats_pb2.CMsgSource2NetworkFlowQuality, _Mapping]] = ..., upstream_flow: _Optional[_Union[_source2_steam_stats_pb2.CMsgSource2NetworkFlowQuality, _Mapping]] = ..., perf_samples: _Optional[_Iterable[_Union[_source2_steam_stats_pb2.CMsgSource2PerfIntervalSample, _Mapping]]] = ...) -> None: ...

class CSVCMsg_ServerInfo(_message.Message):
    __slots__ = ("protocol", "server_count", "is_dedicated", "is_hltv", "c_os", "max_clients", "max_classes", "player_slot", "tick_interval", "game_dir", "map_name", "sky_name", "host_name", "addon_name", "game_session_config", "game_session_manifest")
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    SERVER_COUNT_FIELD_NUMBER: _ClassVar[int]
    IS_DEDICATED_FIELD_NUMBER: _ClassVar[int]
    IS_HLTV_FIELD_NUMBER: _ClassVar[int]
    C_OS_FIELD_NUMBER: _ClassVar[int]
    MAX_CLIENTS_FIELD_NUMBER: _ClassVar[int]
    MAX_CLASSES_FIELD_NUMBER: _ClassVar[int]
    PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
    TICK_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    GAME_DIR_FIELD_NUMBER: _ClassVar[int]
    MAP_NAME_FIELD_NUMBER: _ClassVar[int]
    SKY_NAME_FIELD_NUMBER: _ClassVar[int]
    HOST_NAME_FIELD_NUMBER: _ClassVar[int]
    ADDON_NAME_FIELD_NUMBER: _ClassVar[int]
    GAME_SESSION_CONFIG_FIELD_NUMBER: _ClassVar[int]
    GAME_SESSION_MANIFEST_FIELD_NUMBER: _ClassVar[int]
    protocol: int
    server_count: int
    is_dedicated: bool
    is_hltv: bool
    c_os: int
    max_clients: int
    max_classes: int
    player_slot: int
    tick_interval: float
    game_dir: str
    map_name: str
    sky_name: str
    host_name: str
    addon_name: str
    game_session_config: _networkbasetypes_pb2.CSVCMsg_GameSessionConfiguration
    game_session_manifest: bytes
    def __init__(self, protocol: _Optional[int] = ..., server_count: _Optional[int] = ..., is_dedicated: bool = ..., is_hltv: bool = ..., c_os: _Optional[int] = ..., max_clients: _Optional[int] = ..., max_classes: _Optional[int] = ..., player_slot: _Optional[int] = ..., tick_interval: _Optional[float] = ..., game_dir: _Optional[str] = ..., map_name: _Optional[str] = ..., sky_name: _Optional[str] = ..., host_name: _Optional[str] = ..., addon_name: _Optional[str] = ..., game_session_config: _Optional[_Union[_networkbasetypes_pb2.CSVCMsg_GameSessionConfiguration, _Mapping]] = ..., game_session_manifest: _Optional[bytes] = ...) -> None: ...

class CSVCMsg_ClassInfo(_message.Message):
    __slots__ = ("create_on_client", "classes")
    class class_t(_message.Message):
        __slots__ = ("class_id", "class_name")
        CLASS_ID_FIELD_NUMBER: _ClassVar[int]
        CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
        class_id: int
        class_name: str
        def __init__(self, class_id: _Optional[int] = ..., class_name: _Optional[str] = ...) -> None: ...
    CREATE_ON_CLIENT_FIELD_NUMBER: _ClassVar[int]
    CLASSES_FIELD_NUMBER: _ClassVar[int]
    create_on_client: bool
    classes: _containers.RepeatedCompositeFieldContainer[CSVCMsg_ClassInfo.class_t]
    def __init__(self, create_on_client: bool = ..., classes: _Optional[_Iterable[_Union[CSVCMsg_ClassInfo.class_t, _Mapping]]] = ...) -> None: ...

class CSVCMsg_SetPause(_message.Message):
    __slots__ = ("paused",)
    PAUSED_FIELD_NUMBER: _ClassVar[int]
    paused: bool
    def __init__(self, paused: bool = ...) -> None: ...

class CSVCMsg_VoiceInit(_message.Message):
    __slots__ = ("quality", "codec", "version")
    QUALITY_FIELD_NUMBER: _ClassVar[int]
    CODEC_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    quality: int
    codec: str
    version: int
    def __init__(self, quality: _Optional[int] = ..., codec: _Optional[str] = ..., version: _Optional[int] = ...) -> None: ...

class CSVCMsg_Print(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    def __init__(self, text: _Optional[str] = ...) -> None: ...

class CSVCMsg_Sounds(_message.Message):
    __slots__ = ("reliable_sound", "sounds")
    class sounddata_t(_message.Message):
        __slots__ = ("origin_x", "origin_y", "origin_z", "volume", "delay_value", "sequence_number", "entity_index", "channel", "pitch", "flags", "sound_num", "sound_num_handle", "speaker_entity", "random_seed", "sound_level", "is_sentence", "is_ambient", "guid", "sound_resource_id")
        ORIGIN_X_FIELD_NUMBER: _ClassVar[int]
        ORIGIN_Y_FIELD_NUMBER: _ClassVar[int]
        ORIGIN_Z_FIELD_NUMBER: _ClassVar[int]
        VOLUME_FIELD_NUMBER: _ClassVar[int]
        DELAY_VALUE_FIELD_NUMBER: _ClassVar[int]
        SEQUENCE_NUMBER_FIELD_NUMBER: _ClassVar[int]
        ENTITY_INDEX_FIELD_NUMBER: _ClassVar[int]
        CHANNEL_FIELD_NUMBER: _ClassVar[int]
        PITCH_FIELD_NUMBER: _ClassVar[int]
        FLAGS_FIELD_NUMBER: _ClassVar[int]
        SOUND_NUM_FIELD_NUMBER: _ClassVar[int]
        SOUND_NUM_HANDLE_FIELD_NUMBER: _ClassVar[int]
        SPEAKER_ENTITY_FIELD_NUMBER: _ClassVar[int]
        RANDOM_SEED_FIELD_NUMBER: _ClassVar[int]
        SOUND_LEVEL_FIELD_NUMBER: _ClassVar[int]
        IS_SENTENCE_FIELD_NUMBER: _ClassVar[int]
        IS_AMBIENT_FIELD_NUMBER: _ClassVar[int]
        GUID_FIELD_NUMBER: _ClassVar[int]
        SOUND_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
        origin_x: int
        origin_y: int
        origin_z: int
        volume: int
        delay_value: float
        sequence_number: int
        entity_index: int
        channel: int
        pitch: int
        flags: int
        sound_num: int
        sound_num_handle: int
        speaker_entity: int
        random_seed: int
        sound_level: int
        is_sentence: bool
        is_ambient: bool
        guid: int
        sound_resource_id: int
        def __init__(self, origin_x: _Optional[int] = ..., origin_y: _Optional[int] = ..., origin_z: _Optional[int] = ..., volume: _Optional[int] = ..., delay_value: _Optional[float] = ..., sequence_number: _Optional[int] = ..., entity_index: _Optional[int] = ..., channel: _Optional[int] = ..., pitch: _Optional[int] = ..., flags: _Optional[int] = ..., sound_num: _Optional[int] = ..., sound_num_handle: _Optional[int] = ..., speaker_entity: _Optional[int] = ..., random_seed: _Optional[int] = ..., sound_level: _Optional[int] = ..., is_sentence: bool = ..., is_ambient: bool = ..., guid: _Optional[int] = ..., sound_resource_id: _Optional[int] = ...) -> None: ...
    RELIABLE_SOUND_FIELD_NUMBER: _ClassVar[int]
    SOUNDS_FIELD_NUMBER: _ClassVar[int]
    reliable_sound: bool
    sounds: _containers.RepeatedCompositeFieldContainer[CSVCMsg_Sounds.sounddata_t]
    def __init__(self, reliable_sound: bool = ..., sounds: _Optional[_Iterable[_Union[CSVCMsg_Sounds.sounddata_t, _Mapping]]] = ...) -> None: ...

class CSVCMsg_Prefetch(_message.Message):
    __slots__ = ("sound_index", "resource_type")
    SOUND_INDEX_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    sound_index: int
    resource_type: PrefetchType
    def __init__(self, sound_index: _Optional[int] = ..., resource_type: _Optional[_Union[PrefetchType, str]] = ...) -> None: ...

class CSVCMsg_SetView(_message.Message):
    __slots__ = ("entity_index", "slot")
    ENTITY_INDEX_FIELD_NUMBER: _ClassVar[int]
    SLOT_FIELD_NUMBER: _ClassVar[int]
    entity_index: int
    slot: int
    def __init__(self, entity_index: _Optional[int] = ..., slot: _Optional[int] = ...) -> None: ...

class CSVCMsg_FixAngle(_message.Message):
    __slots__ = ("relative", "angle")
    RELATIVE_FIELD_NUMBER: _ClassVar[int]
    ANGLE_FIELD_NUMBER: _ClassVar[int]
    relative: bool
    angle: _networkbasetypes_pb2.CMsgQAngle
    def __init__(self, relative: bool = ..., angle: _Optional[_Union[_networkbasetypes_pb2.CMsgQAngle, _Mapping]] = ...) -> None: ...

class CSVCMsg_CrosshairAngle(_message.Message):
    __slots__ = ("angle",)
    ANGLE_FIELD_NUMBER: _ClassVar[int]
    angle: _networkbasetypes_pb2.CMsgQAngle
    def __init__(self, angle: _Optional[_Union[_networkbasetypes_pb2.CMsgQAngle, _Mapping]] = ...) -> None: ...

class CSVCMsg_BSPDecal(_message.Message):
    __slots__ = ("pos", "decal_texture_index", "entity_index", "model_index", "low_priority")
    POS_FIELD_NUMBER: _ClassVar[int]
    DECAL_TEXTURE_INDEX_FIELD_NUMBER: _ClassVar[int]
    ENTITY_INDEX_FIELD_NUMBER: _ClassVar[int]
    MODEL_INDEX_FIELD_NUMBER: _ClassVar[int]
    LOW_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    pos: _networkbasetypes_pb2.CMsgVector
    decal_texture_index: int
    entity_index: int
    model_index: int
    low_priority: bool
    def __init__(self, pos: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., decal_texture_index: _Optional[int] = ..., entity_index: _Optional[int] = ..., model_index: _Optional[int] = ..., low_priority: bool = ...) -> None: ...

class CSVCMsg_SplitScreen(_message.Message):
    __slots__ = ("type", "slot", "player_index")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SLOT_FIELD_NUMBER: _ClassVar[int]
    PLAYER_INDEX_FIELD_NUMBER: _ClassVar[int]
    type: ESplitScreenMessageType
    slot: int
    player_index: int
    def __init__(self, type: _Optional[_Union[ESplitScreenMessageType, str]] = ..., slot: _Optional[int] = ..., player_index: _Optional[int] = ...) -> None: ...

class CSVCMsg_GetCvarValue(_message.Message):
    __slots__ = ("cookie", "cvar_name")
    COOKIE_FIELD_NUMBER: _ClassVar[int]
    CVAR_NAME_FIELD_NUMBER: _ClassVar[int]
    cookie: int
    cvar_name: str
    def __init__(self, cookie: _Optional[int] = ..., cvar_name: _Optional[str] = ...) -> None: ...

class CSVCMsg_Menu(_message.Message):
    __slots__ = ("dialog_type", "menu_key_values")
    DIALOG_TYPE_FIELD_NUMBER: _ClassVar[int]
    MENU_KEY_VALUES_FIELD_NUMBER: _ClassVar[int]
    dialog_type: int
    menu_key_values: bytes
    def __init__(self, dialog_type: _Optional[int] = ..., menu_key_values: _Optional[bytes] = ...) -> None: ...

class CSVCMsg_UserMessage(_message.Message):
    __slots__ = ("msg_type", "msg_data", "passthrough")
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    MSG_DATA_FIELD_NUMBER: _ClassVar[int]
    PASSTHROUGH_FIELD_NUMBER: _ClassVar[int]
    msg_type: int
    msg_data: bytes
    passthrough: int
    def __init__(self, msg_type: _Optional[int] = ..., msg_data: _Optional[bytes] = ..., passthrough: _Optional[int] = ...) -> None: ...

class CSVCMsg_SendTable(_message.Message):
    __slots__ = ("is_end", "net_table_name", "needs_decoder", "props")
    class sendprop_t(_message.Message):
        __slots__ = ("type", "var_name", "flags", "priority", "dt_name", "num_elements", "low_value", "high_value", "num_bits")
        TYPE_FIELD_NUMBER: _ClassVar[int]
        VAR_NAME_FIELD_NUMBER: _ClassVar[int]
        FLAGS_FIELD_NUMBER: _ClassVar[int]
        PRIORITY_FIELD_NUMBER: _ClassVar[int]
        DT_NAME_FIELD_NUMBER: _ClassVar[int]
        NUM_ELEMENTS_FIELD_NUMBER: _ClassVar[int]
        LOW_VALUE_FIELD_NUMBER: _ClassVar[int]
        HIGH_VALUE_FIELD_NUMBER: _ClassVar[int]
        NUM_BITS_FIELD_NUMBER: _ClassVar[int]
        type: int
        var_name: str
        flags: int
        priority: int
        dt_name: str
        num_elements: int
        low_value: float
        high_value: float
        num_bits: int
        def __init__(self, type: _Optional[int] = ..., var_name: _Optional[str] = ..., flags: _Optional[int] = ..., priority: _Optional[int] = ..., dt_name: _Optional[str] = ..., num_elements: _Optional[int] = ..., low_value: _Optional[float] = ..., high_value: _Optional[float] = ..., num_bits: _Optional[int] = ...) -> None: ...
    IS_END_FIELD_NUMBER: _ClassVar[int]
    NET_TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    NEEDS_DECODER_FIELD_NUMBER: _ClassVar[int]
    PROPS_FIELD_NUMBER: _ClassVar[int]
    is_end: bool
    net_table_name: str
    needs_decoder: bool
    props: _containers.RepeatedCompositeFieldContainer[CSVCMsg_SendTable.sendprop_t]
    def __init__(self, is_end: bool = ..., net_table_name: _Optional[str] = ..., needs_decoder: bool = ..., props: _Optional[_Iterable[_Union[CSVCMsg_SendTable.sendprop_t, _Mapping]]] = ...) -> None: ...

class CSVCMsg_GameEventList(_message.Message):
    __slots__ = ("descriptors",)
    class key_t(_message.Message):
        __slots__ = ("type", "name")
        TYPE_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        type: int
        name: str
        def __init__(self, type: _Optional[int] = ..., name: _Optional[str] = ...) -> None: ...
    class descriptor_t(_message.Message):
        __slots__ = ("eventid", "name", "keys")
        EVENTID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        KEYS_FIELD_NUMBER: _ClassVar[int]
        eventid: int
        name: str
        keys: _containers.RepeatedCompositeFieldContainer[CSVCMsg_GameEventList.key_t]
        def __init__(self, eventid: _Optional[int] = ..., name: _Optional[str] = ..., keys: _Optional[_Iterable[_Union[CSVCMsg_GameEventList.key_t, _Mapping]]] = ...) -> None: ...
    DESCRIPTORS_FIELD_NUMBER: _ClassVar[int]
    descriptors: _containers.RepeatedCompositeFieldContainer[CSVCMsg_GameEventList.descriptor_t]
    def __init__(self, descriptors: _Optional[_Iterable[_Union[CSVCMsg_GameEventList.descriptor_t, _Mapping]]] = ...) -> None: ...

class CSVCMsg_PacketEntities(_message.Message):
    __slots__ = ("max_entries", "updated_entries", "legacy_is_delta", "update_baseline", "baseline", "delta_from", "entity_data", "pending_full_frame", "active_spawngroup_handle", "max_spawngroup_creationsequence", "last_cmd_number_executed", "last_cmd_number_recv_delta", "server_tick", "serialized_entities", "alternate_baselines", "has_pvs_vis_bits_deprecated", "cmd_recv_status", "non_transmitted_entities", "cq_starved_command_ticks", "cq_discarded_command_ticks", "outofpvs_entity_updates", "dev_padding")
    class alternate_baseline_t(_message.Message):
        __slots__ = ("entity_index", "baseline_index")
        ENTITY_INDEX_FIELD_NUMBER: _ClassVar[int]
        BASELINE_INDEX_FIELD_NUMBER: _ClassVar[int]
        entity_index: int
        baseline_index: int
        def __init__(self, entity_index: _Optional[int] = ..., baseline_index: _Optional[int] = ...) -> None: ...
    class non_transmitted_entities_t(_message.Message):
        __slots__ = ("header_count", "data")
        HEADER_COUNT_FIELD_NUMBER: _ClassVar[int]
        DATA_FIELD_NUMBER: _ClassVar[int]
        header_count: int
        data: bytes
        def __init__(self, header_count: _Optional[int] = ..., data: _Optional[bytes] = ...) -> None: ...
    class outofpvs_entity_updates_t(_message.Message):
        __slots__ = ("count", "data")
        COUNT_FIELD_NUMBER: _ClassVar[int]
        DATA_FIELD_NUMBER: _ClassVar[int]
        count: int
        data: bytes
        def __init__(self, count: _Optional[int] = ..., data: _Optional[bytes] = ...) -> None: ...
    MAX_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    UPDATED_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    LEGACY_IS_DELTA_FIELD_NUMBER: _ClassVar[int]
    UPDATE_BASELINE_FIELD_NUMBER: _ClassVar[int]
    BASELINE_FIELD_NUMBER: _ClassVar[int]
    DELTA_FROM_FIELD_NUMBER: _ClassVar[int]
    ENTITY_DATA_FIELD_NUMBER: _ClassVar[int]
    PENDING_FULL_FRAME_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_SPAWNGROUP_HANDLE_FIELD_NUMBER: _ClassVar[int]
    MAX_SPAWNGROUP_CREATIONSEQUENCE_FIELD_NUMBER: _ClassVar[int]
    LAST_CMD_NUMBER_EXECUTED_FIELD_NUMBER: _ClassVar[int]
    LAST_CMD_NUMBER_RECV_DELTA_FIELD_NUMBER: _ClassVar[int]
    SERVER_TICK_FIELD_NUMBER: _ClassVar[int]
    SERIALIZED_ENTITIES_FIELD_NUMBER: _ClassVar[int]
    ALTERNATE_BASELINES_FIELD_NUMBER: _ClassVar[int]
    HAS_PVS_VIS_BITS_DEPRECATED_FIELD_NUMBER: _ClassVar[int]
    CMD_RECV_STATUS_FIELD_NUMBER: _ClassVar[int]
    NON_TRANSMITTED_ENTITIES_FIELD_NUMBER: _ClassVar[int]
    CQ_STARVED_COMMAND_TICKS_FIELD_NUMBER: _ClassVar[int]
    CQ_DISCARDED_COMMAND_TICKS_FIELD_NUMBER: _ClassVar[int]
    OUTOFPVS_ENTITY_UPDATES_FIELD_NUMBER: _ClassVar[int]
    DEV_PADDING_FIELD_NUMBER: _ClassVar[int]
    max_entries: int
    updated_entries: int
    legacy_is_delta: bool
    update_baseline: bool
    baseline: int
    delta_from: int
    entity_data: bytes
    pending_full_frame: bool
    active_spawngroup_handle: int
    max_spawngroup_creationsequence: int
    last_cmd_number_executed: int
    last_cmd_number_recv_delta: int
    server_tick: int
    serialized_entities: bytes
    alternate_baselines: _containers.RepeatedCompositeFieldContainer[CSVCMsg_PacketEntities.alternate_baseline_t]
    has_pvs_vis_bits_deprecated: int
    cmd_recv_status: _containers.RepeatedScalarFieldContainer[int]
    non_transmitted_entities: CSVCMsg_PacketEntities.non_transmitted_entities_t
    cq_starved_command_ticks: int
    cq_discarded_command_ticks: int
    outofpvs_entity_updates: CSVCMsg_PacketEntities.outofpvs_entity_updates_t
    dev_padding: bytes
    def __init__(self, max_entries: _Optional[int] = ..., updated_entries: _Optional[int] = ..., legacy_is_delta: bool = ..., update_baseline: bool = ..., baseline: _Optional[int] = ..., delta_from: _Optional[int] = ..., entity_data: _Optional[bytes] = ..., pending_full_frame: bool = ..., active_spawngroup_handle: _Optional[int] = ..., max_spawngroup_creationsequence: _Optional[int] = ..., last_cmd_number_executed: _Optional[int] = ..., last_cmd_number_recv_delta: _Optional[int] = ..., server_tick: _Optional[int] = ..., serialized_entities: _Optional[bytes] = ..., alternate_baselines: _Optional[_Iterable[_Union[CSVCMsg_PacketEntities.alternate_baseline_t, _Mapping]]] = ..., has_pvs_vis_bits_deprecated: _Optional[int] = ..., cmd_recv_status: _Optional[_Iterable[int]] = ..., non_transmitted_entities: _Optional[_Union[CSVCMsg_PacketEntities.non_transmitted_entities_t, _Mapping]] = ..., cq_starved_command_ticks: _Optional[int] = ..., cq_discarded_command_ticks: _Optional[int] = ..., outofpvs_entity_updates: _Optional[_Union[CSVCMsg_PacketEntities.outofpvs_entity_updates_t, _Mapping]] = ..., dev_padding: _Optional[bytes] = ...) -> None: ...

class CSVCMsg_TempEntities(_message.Message):
    __slots__ = ("reliable", "num_entries", "entity_data")
    RELIABLE_FIELD_NUMBER: _ClassVar[int]
    NUM_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    ENTITY_DATA_FIELD_NUMBER: _ClassVar[int]
    reliable: bool
    num_entries: int
    entity_data: bytes
    def __init__(self, reliable: bool = ..., num_entries: _Optional[int] = ..., entity_data: _Optional[bytes] = ...) -> None: ...

class CSVCMsg_CreateStringTable(_message.Message):
    __slots__ = ("name", "num_entries", "user_data_fixed_size", "user_data_size", "user_data_size_bits", "flags", "string_data", "uncompressed_size", "data_compressed", "using_varint_bitcounts")
    NAME_FIELD_NUMBER: _ClassVar[int]
    NUM_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    USER_DATA_FIXED_SIZE_FIELD_NUMBER: _ClassVar[int]
    USER_DATA_SIZE_FIELD_NUMBER: _ClassVar[int]
    USER_DATA_SIZE_BITS_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    STRING_DATA_FIELD_NUMBER: _ClassVar[int]
    UNCOMPRESSED_SIZE_FIELD_NUMBER: _ClassVar[int]
    DATA_COMPRESSED_FIELD_NUMBER: _ClassVar[int]
    USING_VARINT_BITCOUNTS_FIELD_NUMBER: _ClassVar[int]
    name: str
    num_entries: int
    user_data_fixed_size: bool
    user_data_size: int
    user_data_size_bits: int
    flags: int
    string_data: bytes
    uncompressed_size: int
    data_compressed: bool
    using_varint_bitcounts: bool
    def __init__(self, name: _Optional[str] = ..., num_entries: _Optional[int] = ..., user_data_fixed_size: bool = ..., user_data_size: _Optional[int] = ..., user_data_size_bits: _Optional[int] = ..., flags: _Optional[int] = ..., string_data: _Optional[bytes] = ..., uncompressed_size: _Optional[int] = ..., data_compressed: bool = ..., using_varint_bitcounts: bool = ...) -> None: ...

class CSVCMsg_UpdateStringTable(_message.Message):
    __slots__ = ("table_id", "num_changed_entries", "string_data")
    TABLE_ID_FIELD_NUMBER: _ClassVar[int]
    NUM_CHANGED_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    STRING_DATA_FIELD_NUMBER: _ClassVar[int]
    table_id: int
    num_changed_entries: int
    string_data: bytes
    def __init__(self, table_id: _Optional[int] = ..., num_changed_entries: _Optional[int] = ..., string_data: _Optional[bytes] = ...) -> None: ...

class CSVCMsg_VoiceData(_message.Message):
    __slots__ = ("audio", "client_deprecated", "proximity", "xuid", "audible_mask", "tick", "passthrough", "entity")
    AUDIO_FIELD_NUMBER: _ClassVar[int]
    CLIENT_DEPRECATED_FIELD_NUMBER: _ClassVar[int]
    PROXIMITY_FIELD_NUMBER: _ClassVar[int]
    XUID_FIELD_NUMBER: _ClassVar[int]
    AUDIBLE_MASK_FIELD_NUMBER: _ClassVar[int]
    TICK_FIELD_NUMBER: _ClassVar[int]
    PASSTHROUGH_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    audio: CMsgVoiceAudio
    client_deprecated: int
    proximity: bool
    xuid: int
    audible_mask: int
    tick: int
    passthrough: int
    entity: int
    def __init__(self, audio: _Optional[_Union[CMsgVoiceAudio, _Mapping]] = ..., client_deprecated: _Optional[int] = ..., proximity: bool = ..., xuid: _Optional[int] = ..., audible_mask: _Optional[int] = ..., tick: _Optional[int] = ..., passthrough: _Optional[int] = ..., entity: _Optional[int] = ...) -> None: ...

class CSVCMsg_PacketReliable(_message.Message):
    __slots__ = ("tick", "messagessize", "state")
    TICK_FIELD_NUMBER: _ClassVar[int]
    MESSAGESSIZE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    tick: int
    messagessize: int
    state: bool
    def __init__(self, tick: _Optional[int] = ..., messagessize: _Optional[int] = ..., state: bool = ...) -> None: ...

class CSVCMsg_FullFrameSplit(_message.Message):
    __slots__ = ("tick", "section", "total", "data")
    TICK_FIELD_NUMBER: _ClassVar[int]
    SECTION_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    tick: int
    section: int
    total: int
    data: bytes
    def __init__(self, tick: _Optional[int] = ..., section: _Optional[int] = ..., total: _Optional[int] = ..., data: _Optional[bytes] = ...) -> None: ...

class CSVCMsg_HLTVStatus(_message.Message):
    __slots__ = ("master", "clients", "slots", "proxies")
    MASTER_FIELD_NUMBER: _ClassVar[int]
    CLIENTS_FIELD_NUMBER: _ClassVar[int]
    SLOTS_FIELD_NUMBER: _ClassVar[int]
    PROXIES_FIELD_NUMBER: _ClassVar[int]
    master: str
    clients: int
    slots: int
    proxies: int
    def __init__(self, master: _Optional[str] = ..., clients: _Optional[int] = ..., slots: _Optional[int] = ..., proxies: _Optional[int] = ...) -> None: ...

class CSVCMsg_ServerSteamID(_message.Message):
    __slots__ = ("steam_id",)
    STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    steam_id: int
    def __init__(self, steam_id: _Optional[int] = ...) -> None: ...

class CSVCMsg_CmdKeyValues(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: _Optional[bytes] = ...) -> None: ...

class CSVCMsg_RconServerDetails(_message.Message):
    __slots__ = ("token", "details")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    token: bytes
    details: str
    def __init__(self, token: _Optional[bytes] = ..., details: _Optional[str] = ...) -> None: ...

class CMsgIPCAddress(_message.Message):
    __slots__ = ("computer_guid", "process_id")
    COMPUTER_GUID_FIELD_NUMBER: _ClassVar[int]
    PROCESS_ID_FIELD_NUMBER: _ClassVar[int]
    computer_guid: int
    process_id: int
    def __init__(self, computer_guid: _Optional[int] = ..., process_id: _Optional[int] = ...) -> None: ...

class CMsgServerPeer(_message.Message):
    __slots__ = ("player_slot", "steamid", "ipc", "they_hear_you", "you_hear_them", "is_listenserver_host")
    PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
    STEAMID_FIELD_NUMBER: _ClassVar[int]
    IPC_FIELD_NUMBER: _ClassVar[int]
    THEY_HEAR_YOU_FIELD_NUMBER: _ClassVar[int]
    YOU_HEAR_THEM_FIELD_NUMBER: _ClassVar[int]
    IS_LISTENSERVER_HOST_FIELD_NUMBER: _ClassVar[int]
    player_slot: int
    steamid: int
    ipc: CMsgIPCAddress
    they_hear_you: bool
    you_hear_them: bool
    is_listenserver_host: bool
    def __init__(self, player_slot: _Optional[int] = ..., steamid: _Optional[int] = ..., ipc: _Optional[_Union[CMsgIPCAddress, _Mapping]] = ..., they_hear_you: bool = ..., you_hear_them: bool = ..., is_listenserver_host: bool = ...) -> None: ...

class CSVCMsg_PeerList(_message.Message):
    __slots__ = ("peer",)
    PEER_FIELD_NUMBER: _ClassVar[int]
    peer: _containers.RepeatedCompositeFieldContainer[CMsgServerPeer]
    def __init__(self, peer: _Optional[_Iterable[_Union[CMsgServerPeer, _Mapping]]] = ...) -> None: ...

class CSVCMsg_ClearAllStringTables(_message.Message):
    __slots__ = ("mapname", "create_tables_skipped")
    MAPNAME_FIELD_NUMBER: _ClassVar[int]
    CREATE_TABLES_SKIPPED_FIELD_NUMBER: _ClassVar[int]
    mapname: str
    create_tables_skipped: bool
    def __init__(self, mapname: _Optional[str] = ..., create_tables_skipped: bool = ...) -> None: ...

class ProtoFlattenedSerializerField_t(_message.Message):
    __slots__ = ("var_type_sym", "var_name_sym", "bit_count", "low_value", "high_value", "encode_flags", "field_serializer_name_sym", "field_serializer_version", "send_node_sym", "var_encoder_sym", "polymorphic_types", "var_serializer_sym")
    class polymorphic_field_t(_message.Message):
        __slots__ = ("polymorphic_field_serializer_name_sym", "polymorphic_field_serializer_version")
        POLYMORPHIC_FIELD_SERIALIZER_NAME_SYM_FIELD_NUMBER: _ClassVar[int]
        POLYMORPHIC_FIELD_SERIALIZER_VERSION_FIELD_NUMBER: _ClassVar[int]
        polymorphic_field_serializer_name_sym: int
        polymorphic_field_serializer_version: int
        def __init__(self, polymorphic_field_serializer_name_sym: _Optional[int] = ..., polymorphic_field_serializer_version: _Optional[int] = ...) -> None: ...
    VAR_TYPE_SYM_FIELD_NUMBER: _ClassVar[int]
    VAR_NAME_SYM_FIELD_NUMBER: _ClassVar[int]
    BIT_COUNT_FIELD_NUMBER: _ClassVar[int]
    LOW_VALUE_FIELD_NUMBER: _ClassVar[int]
    HIGH_VALUE_FIELD_NUMBER: _ClassVar[int]
    ENCODE_FLAGS_FIELD_NUMBER: _ClassVar[int]
    FIELD_SERIALIZER_NAME_SYM_FIELD_NUMBER: _ClassVar[int]
    FIELD_SERIALIZER_VERSION_FIELD_NUMBER: _ClassVar[int]
    SEND_NODE_SYM_FIELD_NUMBER: _ClassVar[int]
    VAR_ENCODER_SYM_FIELD_NUMBER: _ClassVar[int]
    POLYMORPHIC_TYPES_FIELD_NUMBER: _ClassVar[int]
    VAR_SERIALIZER_SYM_FIELD_NUMBER: _ClassVar[int]
    var_type_sym: int
    var_name_sym: int
    bit_count: int
    low_value: float
    high_value: float
    encode_flags: int
    field_serializer_name_sym: int
    field_serializer_version: int
    send_node_sym: int
    var_encoder_sym: int
    polymorphic_types: _containers.RepeatedCompositeFieldContainer[ProtoFlattenedSerializerField_t.polymorphic_field_t]
    var_serializer_sym: int
    def __init__(self, var_type_sym: _Optional[int] = ..., var_name_sym: _Optional[int] = ..., bit_count: _Optional[int] = ..., low_value: _Optional[float] = ..., high_value: _Optional[float] = ..., encode_flags: _Optional[int] = ..., field_serializer_name_sym: _Optional[int] = ..., field_serializer_version: _Optional[int] = ..., send_node_sym: _Optional[int] = ..., var_encoder_sym: _Optional[int] = ..., polymorphic_types: _Optional[_Iterable[_Union[ProtoFlattenedSerializerField_t.polymorphic_field_t, _Mapping]]] = ..., var_serializer_sym: _Optional[int] = ...) -> None: ...

class ProtoFlattenedSerializer_t(_message.Message):
    __slots__ = ("serializer_name_sym", "serializer_version", "fields_index")
    SERIALIZER_NAME_SYM_FIELD_NUMBER: _ClassVar[int]
    SERIALIZER_VERSION_FIELD_NUMBER: _ClassVar[int]
    FIELDS_INDEX_FIELD_NUMBER: _ClassVar[int]
    serializer_name_sym: int
    serializer_version: int
    fields_index: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, serializer_name_sym: _Optional[int] = ..., serializer_version: _Optional[int] = ..., fields_index: _Optional[_Iterable[int]] = ...) -> None: ...

class CSVCMsg_FlattenedSerializer(_message.Message):
    __slots__ = ("serializers", "symbols", "fields")
    SERIALIZERS_FIELD_NUMBER: _ClassVar[int]
    SYMBOLS_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    serializers: _containers.RepeatedCompositeFieldContainer[ProtoFlattenedSerializer_t]
    symbols: _containers.RepeatedScalarFieldContainer[str]
    fields: _containers.RepeatedCompositeFieldContainer[ProtoFlattenedSerializerField_t]
    def __init__(self, serializers: _Optional[_Iterable[_Union[ProtoFlattenedSerializer_t, _Mapping]]] = ..., symbols: _Optional[_Iterable[str]] = ..., fields: _Optional[_Iterable[_Union[ProtoFlattenedSerializerField_t, _Mapping]]] = ...) -> None: ...

class CSVCMsg_StopSound(_message.Message):
    __slots__ = ("guid",)
    GUID_FIELD_NUMBER: _ClassVar[int]
    guid: int
    def __init__(self, guid: _Optional[int] = ...) -> None: ...

class CBidirMsg_RebroadcastGameEvent(_message.Message):
    __slots__ = ("posttoserver", "buftype", "clientbitcount", "receivingclients")
    POSTTOSERVER_FIELD_NUMBER: _ClassVar[int]
    BUFTYPE_FIELD_NUMBER: _ClassVar[int]
    CLIENTBITCOUNT_FIELD_NUMBER: _ClassVar[int]
    RECEIVINGCLIENTS_FIELD_NUMBER: _ClassVar[int]
    posttoserver: bool
    buftype: int
    clientbitcount: int
    receivingclients: int
    def __init__(self, posttoserver: bool = ..., buftype: _Optional[int] = ..., clientbitcount: _Optional[int] = ..., receivingclients: _Optional[int] = ...) -> None: ...

class CBidirMsg_RebroadcastSource(_message.Message):
    __slots__ = ("eventsource",)
    EVENTSOURCE_FIELD_NUMBER: _ClassVar[int]
    eventsource: int
    def __init__(self, eventsource: _Optional[int] = ...) -> None: ...

class CBidirMsg_PredictionEvent(_message.Message):
    __slots__ = ("event_id", "event_data", "sync_type", "sync_val_uint32")
    class ESyncType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ST_Tick: _ClassVar[CBidirMsg_PredictionEvent.ESyncType]
        ST_UserCmdNum: _ClassVar[CBidirMsg_PredictionEvent.ESyncType]
    ST_Tick: CBidirMsg_PredictionEvent.ESyncType
    ST_UserCmdNum: CBidirMsg_PredictionEvent.ESyncType
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_DATA_FIELD_NUMBER: _ClassVar[int]
    SYNC_TYPE_FIELD_NUMBER: _ClassVar[int]
    SYNC_VAL_UINT32_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    event_data: bytes
    sync_type: int
    sync_val_uint32: int
    def __init__(self, event_id: _Optional[int] = ..., event_data: _Optional[bytes] = ..., sync_type: _Optional[int] = ..., sync_val_uint32: _Optional[int] = ...) -> None: ...

class CMsgServerNetworkStats(_message.Message):
    __slots__ = ("dedicated", "cpu_usage", "memory_used_mb", "memory_free_mb", "uptime", "spawn_count", "num_clients", "num_bots", "num_spectators", "num_tv_relays", "fps", "ports", "avg_ping_ms", "avg_engine_latency_out", "avg_packets_out", "avg_packets_in", "avg_loss_out", "avg_loss_in", "avg_data_out", "avg_data_in", "total_data_in", "total_packets_in", "total_data_out", "total_packets_out", "players")
    class Port(_message.Message):
        __slots__ = ("port", "name")
        PORT_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        port: int
        name: str
        def __init__(self, port: _Optional[int] = ..., name: _Optional[str] = ...) -> None: ...
    class Player(_message.Message):
        __slots__ = ("steamid", "remote_addr", "ping_avg_ms", "packet_loss_pct", "is_bot", "loss_in", "loss_out", "engine_latency_ms")
        STEAMID_FIELD_NUMBER: _ClassVar[int]
        REMOTE_ADDR_FIELD_NUMBER: _ClassVar[int]
        PING_AVG_MS_FIELD_NUMBER: _ClassVar[int]
        PACKET_LOSS_PCT_FIELD_NUMBER: _ClassVar[int]
        IS_BOT_FIELD_NUMBER: _ClassVar[int]
        LOSS_IN_FIELD_NUMBER: _ClassVar[int]
        LOSS_OUT_FIELD_NUMBER: _ClassVar[int]
        ENGINE_LATENCY_MS_FIELD_NUMBER: _ClassVar[int]
        steamid: int
        remote_addr: str
        ping_avg_ms: int
        packet_loss_pct: float
        is_bot: bool
        loss_in: float
        loss_out: float
        engine_latency_ms: int
        def __init__(self, steamid: _Optional[int] = ..., remote_addr: _Optional[str] = ..., ping_avg_ms: _Optional[int] = ..., packet_loss_pct: _Optional[float] = ..., is_bot: bool = ..., loss_in: _Optional[float] = ..., loss_out: _Optional[float] = ..., engine_latency_ms: _Optional[int] = ...) -> None: ...
    DEDICATED_FIELD_NUMBER: _ClassVar[int]
    CPU_USAGE_FIELD_NUMBER: _ClassVar[int]
    MEMORY_USED_MB_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FREE_MB_FIELD_NUMBER: _ClassVar[int]
    UPTIME_FIELD_NUMBER: _ClassVar[int]
    SPAWN_COUNT_FIELD_NUMBER: _ClassVar[int]
    NUM_CLIENTS_FIELD_NUMBER: _ClassVar[int]
    NUM_BOTS_FIELD_NUMBER: _ClassVar[int]
    NUM_SPECTATORS_FIELD_NUMBER: _ClassVar[int]
    NUM_TV_RELAYS_FIELD_NUMBER: _ClassVar[int]
    FPS_FIELD_NUMBER: _ClassVar[int]
    PORTS_FIELD_NUMBER: _ClassVar[int]
    AVG_PING_MS_FIELD_NUMBER: _ClassVar[int]
    AVG_ENGINE_LATENCY_OUT_FIELD_NUMBER: _ClassVar[int]
    AVG_PACKETS_OUT_FIELD_NUMBER: _ClassVar[int]
    AVG_PACKETS_IN_FIELD_NUMBER: _ClassVar[int]
    AVG_LOSS_OUT_FIELD_NUMBER: _ClassVar[int]
    AVG_LOSS_IN_FIELD_NUMBER: _ClassVar[int]
    AVG_DATA_OUT_FIELD_NUMBER: _ClassVar[int]
    AVG_DATA_IN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_DATA_IN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PACKETS_IN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_DATA_OUT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PACKETS_OUT_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    dedicated: bool
    cpu_usage: int
    memory_used_mb: int
    memory_free_mb: int
    uptime: int
    spawn_count: int
    num_clients: int
    num_bots: int
    num_spectators: int
    num_tv_relays: int
    fps: float
    ports: _containers.RepeatedCompositeFieldContainer[CMsgServerNetworkStats.Port]
    avg_ping_ms: float
    avg_engine_latency_out: float
    avg_packets_out: float
    avg_packets_in: float
    avg_loss_out: float
    avg_loss_in: float
    avg_data_out: float
    avg_data_in: float
    total_data_in: int
    total_packets_in: int
    total_data_out: int
    total_packets_out: int
    players: _containers.RepeatedCompositeFieldContainer[CMsgServerNetworkStats.Player]
    def __init__(self, dedicated: bool = ..., cpu_usage: _Optional[int] = ..., memory_used_mb: _Optional[int] = ..., memory_free_mb: _Optional[int] = ..., uptime: _Optional[int] = ..., spawn_count: _Optional[int] = ..., num_clients: _Optional[int] = ..., num_bots: _Optional[int] = ..., num_spectators: _Optional[int] = ..., num_tv_relays: _Optional[int] = ..., fps: _Optional[float] = ..., ports: _Optional[_Iterable[_Union[CMsgServerNetworkStats.Port, _Mapping]]] = ..., avg_ping_ms: _Optional[float] = ..., avg_engine_latency_out: _Optional[float] = ..., avg_packets_out: _Optional[float] = ..., avg_packets_in: _Optional[float] = ..., avg_loss_out: _Optional[float] = ..., avg_loss_in: _Optional[float] = ..., avg_data_out: _Optional[float] = ..., avg_data_in: _Optional[float] = ..., total_data_in: _Optional[int] = ..., total_packets_in: _Optional[int] = ..., total_data_out: _Optional[int] = ..., total_packets_out: _Optional[int] = ..., players: _Optional[_Iterable[_Union[CMsgServerNetworkStats.Player, _Mapping]]] = ...) -> None: ...

class CSVCMsg_HltvReplay(_message.Message):
    __slots__ = ("delay", "primary_target", "replay_stop_at", "replay_start_at", "replay_slowdown_begin", "replay_slowdown_end", "replay_slowdown_rate", "reason")
    DELAY_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_TARGET_FIELD_NUMBER: _ClassVar[int]
    REPLAY_STOP_AT_FIELD_NUMBER: _ClassVar[int]
    REPLAY_START_AT_FIELD_NUMBER: _ClassVar[int]
    REPLAY_SLOWDOWN_BEGIN_FIELD_NUMBER: _ClassVar[int]
    REPLAY_SLOWDOWN_END_FIELD_NUMBER: _ClassVar[int]
    REPLAY_SLOWDOWN_RATE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    delay: int
    primary_target: int
    replay_stop_at: int
    replay_start_at: int
    replay_slowdown_begin: int
    replay_slowdown_end: int
    replay_slowdown_rate: float
    reason: int
    def __init__(self, delay: _Optional[int] = ..., primary_target: _Optional[int] = ..., replay_stop_at: _Optional[int] = ..., replay_start_at: _Optional[int] = ..., replay_slowdown_begin: _Optional[int] = ..., replay_slowdown_end: _Optional[int] = ..., replay_slowdown_rate: _Optional[float] = ..., reason: _Optional[int] = ...) -> None: ...

class CCLCMsg_HltvReplay(_message.Message):
    __slots__ = ("request", "slowdown_length", "slowdown_rate", "primary_target", "event_time")
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    SLOWDOWN_LENGTH_FIELD_NUMBER: _ClassVar[int]
    SLOWDOWN_RATE_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_TARGET_FIELD_NUMBER: _ClassVar[int]
    EVENT_TIME_FIELD_NUMBER: _ClassVar[int]
    request: int
    slowdown_length: float
    slowdown_rate: float
    primary_target: int
    event_time: float
    def __init__(self, request: _Optional[int] = ..., slowdown_length: _Optional[float] = ..., slowdown_rate: _Optional[float] = ..., primary_target: _Optional[int] = ..., event_time: _Optional[float] = ...) -> None: ...

class CSVCMsg_Broadcast_Command(_message.Message):
    __slots__ = ("cmd",)
    CMD_FIELD_NUMBER: _ClassVar[int]
    cmd: str
    def __init__(self, cmd: _Optional[str] = ...) -> None: ...

class CCLCMsg_HltvFixupOperatorTick(_message.Message):
    __slots__ = ("tick", "props_data", "origin", "eye_angles", "observer_mode", "cameraman_scoreboard", "observer_target", "view_offset")
    TICK_FIELD_NUMBER: _ClassVar[int]
    PROPS_DATA_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    EYE_ANGLES_FIELD_NUMBER: _ClassVar[int]
    OBSERVER_MODE_FIELD_NUMBER: _ClassVar[int]
    CAMERAMAN_SCOREBOARD_FIELD_NUMBER: _ClassVar[int]
    OBSERVER_TARGET_FIELD_NUMBER: _ClassVar[int]
    VIEW_OFFSET_FIELD_NUMBER: _ClassVar[int]
    tick: int
    props_data: bytes
    origin: _networkbasetypes_pb2.CMsgVector
    eye_angles: _networkbasetypes_pb2.CMsgQAngle
    observer_mode: int
    cameraman_scoreboard: bool
    observer_target: int
    view_offset: _networkbasetypes_pb2.CMsgVector
    def __init__(self, tick: _Optional[int] = ..., props_data: _Optional[bytes] = ..., origin: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., eye_angles: _Optional[_Union[_networkbasetypes_pb2.CMsgQAngle, _Mapping]] = ..., observer_mode: _Optional[int] = ..., cameraman_scoreboard: bool = ..., observer_target: _Optional[int] = ..., view_offset: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ...) -> None: ...

class CSVCMsg_HltvFixupOperatorStatus(_message.Message):
    __slots__ = ("mode", "override_operator_name")
    MODE_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_OPERATOR_NAME_FIELD_NUMBER: _ClassVar[int]
    mode: int
    override_operator_name: str
    def __init__(self, mode: _Optional[int] = ..., override_operator_name: _Optional[str] = ...) -> None: ...

class CMsgServerUserCmd(_message.Message):
    __slots__ = ("data", "cmd_number", "player_slot", "server_tick_executed", "client_tick", "delta_data")
    DATA_FIELD_NUMBER: _ClassVar[int]
    CMD_NUMBER_FIELD_NUMBER: _ClassVar[int]
    PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
    SERVER_TICK_EXECUTED_FIELD_NUMBER: _ClassVar[int]
    CLIENT_TICK_FIELD_NUMBER: _ClassVar[int]
    DELTA_DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    cmd_number: int
    player_slot: int
    server_tick_executed: int
    client_tick: int
    delta_data: bytes
    def __init__(self, data: _Optional[bytes] = ..., cmd_number: _Optional[int] = ..., player_slot: _Optional[int] = ..., server_tick_executed: _Optional[int] = ..., client_tick: _Optional[int] = ..., delta_data: _Optional[bytes] = ...) -> None: ...

class CSVCMsg_UserCommands(_message.Message):
    __slots__ = ("commands",)
    COMMANDS_FIELD_NUMBER: _ClassVar[int]
    commands: _containers.RepeatedCompositeFieldContainer[CMsgServerUserCmd]
    def __init__(self, commands: _Optional[_Iterable[_Union[CMsgServerUserCmd, _Mapping]]] = ...) -> None: ...

class CSVCMsg_NextMsgPredicted(_message.Message):
    __slots__ = ("predicted_by_player_slot", "message_type_id")
    PREDICTED_BY_PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_TYPE_ID_FIELD_NUMBER: _ClassVar[int]
    predicted_by_player_slot: int
    message_type_id: int
    def __init__(self, predicted_by_player_slot: _Optional[int] = ..., message_type_id: _Optional[int] = ...) -> None: ...
