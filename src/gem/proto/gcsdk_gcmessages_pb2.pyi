from . import valveextensions_pb2 as _valveextensions_pb2
from . import steammessages_pb2 as _steammessages_pb2
from .steammessages_steamlearn import steamworkssdk_pb2 as _steamworkssdk_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ESourceEngine(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_ESE_Source1: _ClassVar[ESourceEngine]
    k_ESE_Source2: _ClassVar[ESourceEngine]

class PartnerAccountType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PARTNER_NONE: _ClassVar[PartnerAccountType]
    PARTNER_PERFECT_WORLD: _ClassVar[PartnerAccountType]
    PARTNER_INVALID: _ClassVar[PartnerAccountType]

class GCConnectionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GCConnectionStatus_HAVE_SESSION: _ClassVar[GCConnectionStatus]
    GCConnectionStatus_GC_GOING_DOWN: _ClassVar[GCConnectionStatus]
    GCConnectionStatus_NO_SESSION: _ClassVar[GCConnectionStatus]
    GCConnectionStatus_NO_SESSION_IN_LOGON_QUEUE: _ClassVar[GCConnectionStatus]
    GCConnectionStatus_NO_STEAM: _ClassVar[GCConnectionStatus]
    GCConnectionStatus_SUSPENDED: _ClassVar[GCConnectionStatus]
    GCConnectionStatus_STEAM_GOING_DOWN: _ClassVar[GCConnectionStatus]
k_ESE_Source1: ESourceEngine
k_ESE_Source2: ESourceEngine
PARTNER_NONE: PartnerAccountType
PARTNER_PERFECT_WORLD: PartnerAccountType
PARTNER_INVALID: PartnerAccountType
GCConnectionStatus_HAVE_SESSION: GCConnectionStatus
GCConnectionStatus_GC_GOING_DOWN: GCConnectionStatus
GCConnectionStatus_NO_SESSION: GCConnectionStatus
GCConnectionStatus_NO_SESSION_IN_LOGON_QUEUE: GCConnectionStatus
GCConnectionStatus_NO_STEAM: GCConnectionStatus
GCConnectionStatus_SUSPENDED: GCConnectionStatus
GCConnectionStatus_STEAM_GOING_DOWN: GCConnectionStatus

class CExtraMsgBlock(_message.Message):
    __slots__ = ("msg_type", "contents", "msg_key", "is_compressed")
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTENTS_FIELD_NUMBER: _ClassVar[int]
    MSG_KEY_FIELD_NUMBER: _ClassVar[int]
    IS_COMPRESSED_FIELD_NUMBER: _ClassVar[int]
    msg_type: int
    contents: bytes
    msg_key: int
    is_compressed: bool
    def __init__(self, msg_type: _Optional[int] = ..., contents: _Optional[bytes] = ..., msg_key: _Optional[int] = ..., is_compressed: bool = ...) -> None: ...

class CMsgSteamLearnServerInfo(_message.Message):
    __slots__ = ("access_tokens", "project_infos")
    class ProjectInfo(_message.Message):
        __slots__ = ("project_id", "snapshot_published_version", "inference_published_version", "snapshot_percentage", "snapshot_enabled")
        PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
        SNAPSHOT_PUBLISHED_VERSION_FIELD_NUMBER: _ClassVar[int]
        INFERENCE_PUBLISHED_VERSION_FIELD_NUMBER: _ClassVar[int]
        SNAPSHOT_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
        SNAPSHOT_ENABLED_FIELD_NUMBER: _ClassVar[int]
        project_id: int
        snapshot_published_version: int
        inference_published_version: int
        snapshot_percentage: int
        snapshot_enabled: bool
        def __init__(self, project_id: _Optional[int] = ..., snapshot_published_version: _Optional[int] = ..., inference_published_version: _Optional[int] = ..., snapshot_percentage: _Optional[int] = ..., snapshot_enabled: bool = ...) -> None: ...
    ACCESS_TOKENS_FIELD_NUMBER: _ClassVar[int]
    PROJECT_INFOS_FIELD_NUMBER: _ClassVar[int]
    access_tokens: _steamworkssdk_pb2.CMsgSteamLearnAccessTokens
    project_infos: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearnServerInfo.ProjectInfo]
    def __init__(self, access_tokens: _Optional[_Union[_steamworkssdk_pb2.CMsgSteamLearnAccessTokens, _Mapping]] = ..., project_infos: _Optional[_Iterable[_Union[CMsgSteamLearnServerInfo.ProjectInfo, _Mapping]]] = ...) -> None: ...

class CMsgGCAssertJobData(_message.Message):
    __slots__ = ("message_type", "message_data")
    MESSAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_DATA_FIELD_NUMBER: _ClassVar[int]
    message_type: str
    message_data: bytes
    def __init__(self, message_type: _Optional[str] = ..., message_data: _Optional[bytes] = ...) -> None: ...

class CMsgGCConCommand(_message.Message):
    __slots__ = ("command",)
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    command: str
    def __init__(self, command: _Optional[str] = ...) -> None: ...

class CMsgSDOAssert(_message.Message):
    __slots__ = ("sdo_type", "requests")
    class Request(_message.Message):
        __slots__ = ("key", "requesting_job")
        KEY_FIELD_NUMBER: _ClassVar[int]
        REQUESTING_JOB_FIELD_NUMBER: _ClassVar[int]
        key: _containers.RepeatedScalarFieldContainer[int]
        requesting_job: str
        def __init__(self, key: _Optional[_Iterable[int]] = ..., requesting_job: _Optional[str] = ...) -> None: ...
    SDO_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    sdo_type: int
    requests: _containers.RepeatedCompositeFieldContainer[CMsgSDOAssert.Request]
    def __init__(self, sdo_type: _Optional[int] = ..., requests: _Optional[_Iterable[_Union[CMsgSDOAssert.Request, _Mapping]]] = ...) -> None: ...

class CMsgSOIDOwner(_message.Message):
    __slots__ = ("type", "id")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    type: int
    id: int
    def __init__(self, type: _Optional[int] = ..., id: _Optional[int] = ...) -> None: ...

class CMsgSOSingleObject(_message.Message):
    __slots__ = ("type_id", "object_data", "version", "owner_soid", "service_id")
    TYPE_ID_FIELD_NUMBER: _ClassVar[int]
    OBJECT_DATA_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    OWNER_SOID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
    type_id: int
    object_data: bytes
    version: int
    owner_soid: CMsgSOIDOwner
    service_id: int
    def __init__(self, type_id: _Optional[int] = ..., object_data: _Optional[bytes] = ..., version: _Optional[int] = ..., owner_soid: _Optional[_Union[CMsgSOIDOwner, _Mapping]] = ..., service_id: _Optional[int] = ...) -> None: ...

class CMsgSOMultipleObjects(_message.Message):
    __slots__ = ("objects_modified", "version", "objects_added", "objects_removed", "owner_soid", "service_id")
    class SingleObject(_message.Message):
        __slots__ = ("type_id", "object_data")
        TYPE_ID_FIELD_NUMBER: _ClassVar[int]
        OBJECT_DATA_FIELD_NUMBER: _ClassVar[int]
        type_id: int
        object_data: bytes
        def __init__(self, type_id: _Optional[int] = ..., object_data: _Optional[bytes] = ...) -> None: ...
    OBJECTS_MODIFIED_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    OBJECTS_ADDED_FIELD_NUMBER: _ClassVar[int]
    OBJECTS_REMOVED_FIELD_NUMBER: _ClassVar[int]
    OWNER_SOID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
    objects_modified: _containers.RepeatedCompositeFieldContainer[CMsgSOMultipleObjects.SingleObject]
    version: int
    objects_added: _containers.RepeatedCompositeFieldContainer[CMsgSOMultipleObjects.SingleObject]
    objects_removed: _containers.RepeatedCompositeFieldContainer[CMsgSOMultipleObjects.SingleObject]
    owner_soid: CMsgSOIDOwner
    service_id: int
    def __init__(self, objects_modified: _Optional[_Iterable[_Union[CMsgSOMultipleObjects.SingleObject, _Mapping]]] = ..., version: _Optional[int] = ..., objects_added: _Optional[_Iterable[_Union[CMsgSOMultipleObjects.SingleObject, _Mapping]]] = ..., objects_removed: _Optional[_Iterable[_Union[CMsgSOMultipleObjects.SingleObject, _Mapping]]] = ..., owner_soid: _Optional[_Union[CMsgSOIDOwner, _Mapping]] = ..., service_id: _Optional[int] = ...) -> None: ...

class CMsgSOCacheSubscribed(_message.Message):
    __slots__ = ("objects", "version", "owner_soid", "service_id", "service_list", "sync_version")
    class SubscribedType(_message.Message):
        __slots__ = ("type_id", "object_data")
        TYPE_ID_FIELD_NUMBER: _ClassVar[int]
        OBJECT_DATA_FIELD_NUMBER: _ClassVar[int]
        type_id: int
        object_data: _containers.RepeatedScalarFieldContainer[bytes]
        def __init__(self, type_id: _Optional[int] = ..., object_data: _Optional[_Iterable[bytes]] = ...) -> None: ...
    OBJECTS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    OWNER_SOID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_LIST_FIELD_NUMBER: _ClassVar[int]
    SYNC_VERSION_FIELD_NUMBER: _ClassVar[int]
    objects: _containers.RepeatedCompositeFieldContainer[CMsgSOCacheSubscribed.SubscribedType]
    version: int
    owner_soid: CMsgSOIDOwner
    service_id: int
    service_list: _containers.RepeatedScalarFieldContainer[int]
    sync_version: int
    def __init__(self, objects: _Optional[_Iterable[_Union[CMsgSOCacheSubscribed.SubscribedType, _Mapping]]] = ..., version: _Optional[int] = ..., owner_soid: _Optional[_Union[CMsgSOIDOwner, _Mapping]] = ..., service_id: _Optional[int] = ..., service_list: _Optional[_Iterable[int]] = ..., sync_version: _Optional[int] = ...) -> None: ...

class CMsgSOCacheSubscribedUpToDate(_message.Message):
    __slots__ = ("version", "owner_soid", "service_id", "service_list", "sync_version")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    OWNER_SOID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_LIST_FIELD_NUMBER: _ClassVar[int]
    SYNC_VERSION_FIELD_NUMBER: _ClassVar[int]
    version: int
    owner_soid: CMsgSOIDOwner
    service_id: int
    service_list: _containers.RepeatedScalarFieldContainer[int]
    sync_version: int
    def __init__(self, version: _Optional[int] = ..., owner_soid: _Optional[_Union[CMsgSOIDOwner, _Mapping]] = ..., service_id: _Optional[int] = ..., service_list: _Optional[_Iterable[int]] = ..., sync_version: _Optional[int] = ...) -> None: ...

class CMsgSOCacheUnsubscribed(_message.Message):
    __slots__ = ("owner_soid",)
    OWNER_SOID_FIELD_NUMBER: _ClassVar[int]
    owner_soid: CMsgSOIDOwner
    def __init__(self, owner_soid: _Optional[_Union[CMsgSOIDOwner, _Mapping]] = ...) -> None: ...

class CMsgSOCacheSubscriptionCheck(_message.Message):
    __slots__ = ("version", "owner_soid", "service_id", "service_list", "sync_version")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    OWNER_SOID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_LIST_FIELD_NUMBER: _ClassVar[int]
    SYNC_VERSION_FIELD_NUMBER: _ClassVar[int]
    version: int
    owner_soid: CMsgSOIDOwner
    service_id: int
    service_list: _containers.RepeatedScalarFieldContainer[int]
    sync_version: int
    def __init__(self, version: _Optional[int] = ..., owner_soid: _Optional[_Union[CMsgSOIDOwner, _Mapping]] = ..., service_id: _Optional[int] = ..., service_list: _Optional[_Iterable[int]] = ..., sync_version: _Optional[int] = ...) -> None: ...

class CMsgSOCacheSubscriptionRefresh(_message.Message):
    __slots__ = ("owner_soid",)
    OWNER_SOID_FIELD_NUMBER: _ClassVar[int]
    owner_soid: CMsgSOIDOwner
    def __init__(self, owner_soid: _Optional[_Union[CMsgSOIDOwner, _Mapping]] = ...) -> None: ...

class CMsgSOCacheVersion(_message.Message):
    __slots__ = ("version",)
    VERSION_FIELD_NUMBER: _ClassVar[int]
    version: int
    def __init__(self, version: _Optional[int] = ...) -> None: ...

class CMsgGCMultiplexMessage(_message.Message):
    __slots__ = ("msgtype", "payload", "steamids")
    MSGTYPE_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    STEAMIDS_FIELD_NUMBER: _ClassVar[int]
    msgtype: int
    payload: bytes
    steamids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, msgtype: _Optional[int] = ..., payload: _Optional[bytes] = ..., steamids: _Optional[_Iterable[int]] = ...) -> None: ...

class CMsgGCToGCSubGCStarting(_message.Message):
    __slots__ = ("dir_index",)
    DIR_INDEX_FIELD_NUMBER: _ClassVar[int]
    dir_index: int
    def __init__(self, dir_index: _Optional[int] = ...) -> None: ...

class CGCToGCMsgMasterAck(_message.Message):
    __slots__ = ("dir_index", "machine_name", "process_name", "directory")
    class Process(_message.Message):
        __slots__ = ("dir_index", "type_instances")
        DIR_INDEX_FIELD_NUMBER: _ClassVar[int]
        TYPE_INSTANCES_FIELD_NUMBER: _ClassVar[int]
        dir_index: int
        type_instances: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, dir_index: _Optional[int] = ..., type_instances: _Optional[_Iterable[int]] = ...) -> None: ...
    DIR_INDEX_FIELD_NUMBER: _ClassVar[int]
    MACHINE_NAME_FIELD_NUMBER: _ClassVar[int]
    PROCESS_NAME_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    dir_index: int
    machine_name: str
    process_name: str
    directory: _containers.RepeatedCompositeFieldContainer[CGCToGCMsgMasterAck.Process]
    def __init__(self, dir_index: _Optional[int] = ..., machine_name: _Optional[str] = ..., process_name: _Optional[str] = ..., directory: _Optional[_Iterable[_Union[CGCToGCMsgMasterAck.Process, _Mapping]]] = ...) -> None: ...

class CGCToGCMsgMasterAck_Response(_message.Message):
    __slots__ = ("eresult",)
    ERESULT_FIELD_NUMBER: _ClassVar[int]
    eresult: int
    def __init__(self, eresult: _Optional[int] = ...) -> None: ...

class CMsgGCToGCUniverseStartup(_message.Message):
    __slots__ = ("is_initial_startup",)
    IS_INITIAL_STARTUP_FIELD_NUMBER: _ClassVar[int]
    is_initial_startup: bool
    def __init__(self, is_initial_startup: bool = ...) -> None: ...

class CMsgGCToGCUniverseStartupResponse(_message.Message):
    __slots__ = ("eresult",)
    ERESULT_FIELD_NUMBER: _ClassVar[int]
    eresult: int
    def __init__(self, eresult: _Optional[int] = ...) -> None: ...

class CGCToGCMsgMasterStartupComplete(_message.Message):
    __slots__ = ("gc_info",)
    class GCInfo(_message.Message):
        __slots__ = ("dir_index", "machine_name")
        DIR_INDEX_FIELD_NUMBER: _ClassVar[int]
        MACHINE_NAME_FIELD_NUMBER: _ClassVar[int]
        dir_index: int
        machine_name: str
        def __init__(self, dir_index: _Optional[int] = ..., machine_name: _Optional[str] = ...) -> None: ...
    GC_INFO_FIELD_NUMBER: _ClassVar[int]
    gc_info: _containers.RepeatedCompositeFieldContainer[CGCToGCMsgMasterStartupComplete.GCInfo]
    def __init__(self, gc_info: _Optional[_Iterable[_Union[CGCToGCMsgMasterStartupComplete.GCInfo, _Mapping]]] = ...) -> None: ...

class CGCToGCMsgRouted(_message.Message):
    __slots__ = ("msg_type", "sender_id", "net_message")
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    SENDER_ID_FIELD_NUMBER: _ClassVar[int]
    NET_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    msg_type: int
    sender_id: int
    net_message: bytes
    def __init__(self, msg_type: _Optional[int] = ..., sender_id: _Optional[int] = ..., net_message: _Optional[bytes] = ...) -> None: ...

class CGCToGCMsgRoutedReply(_message.Message):
    __slots__ = ("msg_type", "net_message")
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    NET_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    msg_type: int
    net_message: bytes
    def __init__(self, msg_type: _Optional[int] = ..., net_message: _Optional[bytes] = ...) -> None: ...

class CMsgGCUpdateSubGCSessionInfo(_message.Message):
    __slots__ = ("updates",)
    class CMsgUpdate(_message.Message):
        __slots__ = ("steamid", "ip", "trusted")
        STEAMID_FIELD_NUMBER: _ClassVar[int]
        IP_FIELD_NUMBER: _ClassVar[int]
        TRUSTED_FIELD_NUMBER: _ClassVar[int]
        steamid: int
        ip: int
        trusted: bool
        def __init__(self, steamid: _Optional[int] = ..., ip: _Optional[int] = ..., trusted: bool = ...) -> None: ...
    UPDATES_FIELD_NUMBER: _ClassVar[int]
    updates: _containers.RepeatedCompositeFieldContainer[CMsgGCUpdateSubGCSessionInfo.CMsgUpdate]
    def __init__(self, updates: _Optional[_Iterable[_Union[CMsgGCUpdateSubGCSessionInfo.CMsgUpdate, _Mapping]]] = ...) -> None: ...

class CMsgGCRequestSubGCSessionInfo(_message.Message):
    __slots__ = ("steamid",)
    STEAMID_FIELD_NUMBER: _ClassVar[int]
    steamid: int
    def __init__(self, steamid: _Optional[int] = ...) -> None: ...

class CMsgGCRequestSubGCSessionInfoResponse(_message.Message):
    __slots__ = ("ip", "trusted", "port", "success")
    IP_FIELD_NUMBER: _ClassVar[int]
    TRUSTED_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ip: int
    trusted: bool
    port: int
    success: bool
    def __init__(self, ip: _Optional[int] = ..., trusted: bool = ..., port: _Optional[int] = ..., success: bool = ...) -> None: ...

class CMsgSOCacheHaveVersion(_message.Message):
    __slots__ = ("soid", "version", "service_id", "cached_file_version")
    SOID_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
    CACHED_FILE_VERSION_FIELD_NUMBER: _ClassVar[int]
    soid: CMsgSOIDOwner
    version: int
    service_id: int
    cached_file_version: int
    def __init__(self, soid: _Optional[_Union[CMsgSOIDOwner, _Mapping]] = ..., version: _Optional[int] = ..., service_id: _Optional[int] = ..., cached_file_version: _Optional[int] = ...) -> None: ...

class CMsgClientHello(_message.Message):
    __slots__ = ("version", "socache_have_versions", "client_session_need", "client_launcher", "client_language", "engine", "steamdatagram_login", "platform_id", "game_msg", "os_type", "render_system", "render_system_req", "screen_width", "screen_height", "screen_refresh", "render_width", "render_height", "swap_width", "swap_height", "is_steam_china", "is_steam_china_client", "platform_name")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    SOCACHE_HAVE_VERSIONS_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SESSION_NEED_FIELD_NUMBER: _ClassVar[int]
    CLIENT_LAUNCHER_FIELD_NUMBER: _ClassVar[int]
    CLIENT_LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    ENGINE_FIELD_NUMBER: _ClassVar[int]
    STEAMDATAGRAM_LOGIN_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_ID_FIELD_NUMBER: _ClassVar[int]
    GAME_MSG_FIELD_NUMBER: _ClassVar[int]
    OS_TYPE_FIELD_NUMBER: _ClassVar[int]
    RENDER_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    RENDER_SYSTEM_REQ_FIELD_NUMBER: _ClassVar[int]
    SCREEN_WIDTH_FIELD_NUMBER: _ClassVar[int]
    SCREEN_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    SCREEN_REFRESH_FIELD_NUMBER: _ClassVar[int]
    RENDER_WIDTH_FIELD_NUMBER: _ClassVar[int]
    RENDER_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    SWAP_WIDTH_FIELD_NUMBER: _ClassVar[int]
    SWAP_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    IS_STEAM_CHINA_FIELD_NUMBER: _ClassVar[int]
    IS_STEAM_CHINA_CLIENT_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_NAME_FIELD_NUMBER: _ClassVar[int]
    version: int
    socache_have_versions: _containers.RepeatedCompositeFieldContainer[CMsgSOCacheHaveVersion]
    client_session_need: int
    client_launcher: PartnerAccountType
    client_language: int
    engine: ESourceEngine
    steamdatagram_login: bytes
    platform_id: int
    game_msg: bytes
    os_type: int
    render_system: int
    render_system_req: int
    screen_width: int
    screen_height: int
    screen_refresh: int
    render_width: int
    render_height: int
    swap_width: int
    swap_height: int
    is_steam_china: bool
    is_steam_china_client: bool
    platform_name: str
    def __init__(self, version: _Optional[int] = ..., socache_have_versions: _Optional[_Iterable[_Union[CMsgSOCacheHaveVersion, _Mapping]]] = ..., client_session_need: _Optional[int] = ..., client_launcher: _Optional[_Union[PartnerAccountType, str]] = ..., client_language: _Optional[int] = ..., engine: _Optional[_Union[ESourceEngine, str]] = ..., steamdatagram_login: _Optional[bytes] = ..., platform_id: _Optional[int] = ..., game_msg: _Optional[bytes] = ..., os_type: _Optional[int] = ..., render_system: _Optional[int] = ..., render_system_req: _Optional[int] = ..., screen_width: _Optional[int] = ..., screen_height: _Optional[int] = ..., screen_refresh: _Optional[int] = ..., render_width: _Optional[int] = ..., render_height: _Optional[int] = ..., swap_width: _Optional[int] = ..., swap_height: _Optional[int] = ..., is_steam_china: bool = ..., is_steam_china_client: bool = ..., platform_name: _Optional[str] = ...) -> None: ...

class CMsgClientWelcome(_message.Message):
    __slots__ = ("version", "game_data", "outofdate_subscribed_caches", "uptodate_subscribed_caches", "location", "gc_socache_file_version", "txn_country_code", "game_data2", "rtime32_gc_welcome_timestamp", "currency", "balance", "balance_url", "has_accepted_china_ssa", "is_banned_steam_china", "additional_welcome_msgs", "steam_learn_server_info")
    class Location(_message.Message):
        __slots__ = ("latitude", "longitude", "country")
        LATITUDE_FIELD_NUMBER: _ClassVar[int]
        LONGITUDE_FIELD_NUMBER: _ClassVar[int]
        COUNTRY_FIELD_NUMBER: _ClassVar[int]
        latitude: float
        longitude: float
        country: str
        def __init__(self, latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., country: _Optional[str] = ...) -> None: ...
    VERSION_FIELD_NUMBER: _ClassVar[int]
    GAME_DATA_FIELD_NUMBER: _ClassVar[int]
    OUTOFDATE_SUBSCRIBED_CACHES_FIELD_NUMBER: _ClassVar[int]
    UPTODATE_SUBSCRIBED_CACHES_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    GC_SOCACHE_FILE_VERSION_FIELD_NUMBER: _ClassVar[int]
    TXN_COUNTRY_CODE_FIELD_NUMBER: _ClassVar[int]
    GAME_DATA2_FIELD_NUMBER: _ClassVar[int]
    RTIME32_GC_WELCOME_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    BALANCE_URL_FIELD_NUMBER: _ClassVar[int]
    HAS_ACCEPTED_CHINA_SSA_FIELD_NUMBER: _ClassVar[int]
    IS_BANNED_STEAM_CHINA_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_WELCOME_MSGS_FIELD_NUMBER: _ClassVar[int]
    STEAM_LEARN_SERVER_INFO_FIELD_NUMBER: _ClassVar[int]
    version: int
    game_data: bytes
    outofdate_subscribed_caches: _containers.RepeatedCompositeFieldContainer[CMsgSOCacheSubscribed]
    uptodate_subscribed_caches: _containers.RepeatedCompositeFieldContainer[CMsgSOCacheSubscriptionCheck]
    location: CMsgClientWelcome.Location
    gc_socache_file_version: int
    txn_country_code: str
    game_data2: bytes
    rtime32_gc_welcome_timestamp: int
    currency: int
    balance: int
    balance_url: str
    has_accepted_china_ssa: bool
    is_banned_steam_china: bool
    additional_welcome_msgs: CExtraMsgBlock
    steam_learn_server_info: CMsgSteamLearnServerInfo
    def __init__(self, version: _Optional[int] = ..., game_data: _Optional[bytes] = ..., outofdate_subscribed_caches: _Optional[_Iterable[_Union[CMsgSOCacheSubscribed, _Mapping]]] = ..., uptodate_subscribed_caches: _Optional[_Iterable[_Union[CMsgSOCacheSubscriptionCheck, _Mapping]]] = ..., location: _Optional[_Union[CMsgClientWelcome.Location, _Mapping]] = ..., gc_socache_file_version: _Optional[int] = ..., txn_country_code: _Optional[str] = ..., game_data2: _Optional[bytes] = ..., rtime32_gc_welcome_timestamp: _Optional[int] = ..., currency: _Optional[int] = ..., balance: _Optional[int] = ..., balance_url: _Optional[str] = ..., has_accepted_china_ssa: bool = ..., is_banned_steam_china: bool = ..., additional_welcome_msgs: _Optional[_Union[CExtraMsgBlock, _Mapping]] = ..., steam_learn_server_info: _Optional[_Union[CMsgSteamLearnServerInfo, _Mapping]] = ...) -> None: ...

class CMsgConnectionStatus(_message.Message):
    __slots__ = ("status", "client_session_need", "queue_position", "queue_size", "wait_seconds", "estimated_wait_seconds_remaining")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SESSION_NEED_FIELD_NUMBER: _ClassVar[int]
    QUEUE_POSITION_FIELD_NUMBER: _ClassVar[int]
    QUEUE_SIZE_FIELD_NUMBER: _ClassVar[int]
    WAIT_SECONDS_FIELD_NUMBER: _ClassVar[int]
    ESTIMATED_WAIT_SECONDS_REMAINING_FIELD_NUMBER: _ClassVar[int]
    status: GCConnectionStatus
    client_session_need: int
    queue_position: int
    queue_size: int
    wait_seconds: int
    estimated_wait_seconds_remaining: int
    def __init__(self, status: _Optional[_Union[GCConnectionStatus, str]] = ..., client_session_need: _Optional[int] = ..., queue_position: _Optional[int] = ..., queue_size: _Optional[int] = ..., wait_seconds: _Optional[int] = ..., estimated_wait_seconds_remaining: _Optional[int] = ...) -> None: ...

class CMsgGCToGCSOCacheSubscribe(_message.Message):
    __slots__ = ("subscriber", "subscribe_to_id", "sync_version", "have_versions", "subscribe_to_type")
    class CMsgHaveVersions(_message.Message):
        __slots__ = ("service_id", "version")
        SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
        VERSION_FIELD_NUMBER: _ClassVar[int]
        service_id: int
        version: int
        def __init__(self, service_id: _Optional[int] = ..., version: _Optional[int] = ...) -> None: ...
    SUBSCRIBER_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIBE_TO_ID_FIELD_NUMBER: _ClassVar[int]
    SYNC_VERSION_FIELD_NUMBER: _ClassVar[int]
    HAVE_VERSIONS_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIBE_TO_TYPE_FIELD_NUMBER: _ClassVar[int]
    subscriber: int
    subscribe_to_id: int
    sync_version: int
    have_versions: _containers.RepeatedCompositeFieldContainer[CMsgGCToGCSOCacheSubscribe.CMsgHaveVersions]
    subscribe_to_type: int
    def __init__(self, subscriber: _Optional[int] = ..., subscribe_to_id: _Optional[int] = ..., sync_version: _Optional[int] = ..., have_versions: _Optional[_Iterable[_Union[CMsgGCToGCSOCacheSubscribe.CMsgHaveVersions, _Mapping]]] = ..., subscribe_to_type: _Optional[int] = ...) -> None: ...

class CMsgGCToGCSOCacheUnsubscribe(_message.Message):
    __slots__ = ("subscriber", "unsubscribe_from_id", "unsubscribe_from_type")
    SUBSCRIBER_FIELD_NUMBER: _ClassVar[int]
    UNSUBSCRIBE_FROM_ID_FIELD_NUMBER: _ClassVar[int]
    UNSUBSCRIBE_FROM_TYPE_FIELD_NUMBER: _ClassVar[int]
    subscriber: int
    unsubscribe_from_id: int
    unsubscribe_from_type: int
    def __init__(self, subscriber: _Optional[int] = ..., unsubscribe_from_id: _Optional[int] = ..., unsubscribe_from_type: _Optional[int] = ...) -> None: ...

class CMsgGCClientPing(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgGCToGCForwardAccountDetails(_message.Message):
    __slots__ = ("steamid", "account_details", "age_seconds")
    STEAMID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_DETAILS_FIELD_NUMBER: _ClassVar[int]
    AGE_SECONDS_FIELD_NUMBER: _ClassVar[int]
    steamid: int
    account_details: _steammessages_pb2.CGCSystemMsg_GetAccountDetails_Response
    age_seconds: int
    def __init__(self, steamid: _Optional[int] = ..., account_details: _Optional[_Union[_steammessages_pb2.CGCSystemMsg_GetAccountDetails_Response, _Mapping]] = ..., age_seconds: _Optional[int] = ...) -> None: ...

class CMsgGCToGCLoadSessionSOCache(_message.Message):
    __slots__ = ("account_id", "forward_account_details")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    FORWARD_ACCOUNT_DETAILS_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    forward_account_details: CMsgGCToGCForwardAccountDetails
    def __init__(self, account_id: _Optional[int] = ..., forward_account_details: _Optional[_Union[CMsgGCToGCForwardAccountDetails, _Mapping]] = ...) -> None: ...

class CMsgGCToGCLoadSessionSOCacheResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgGCToGCUpdateSessionStats(_message.Message):
    __slots__ = ("user_sessions", "server_sessions", "in_logon_surge")
    USER_SESSIONS_FIELD_NUMBER: _ClassVar[int]
    SERVER_SESSIONS_FIELD_NUMBER: _ClassVar[int]
    IN_LOGON_SURGE_FIELD_NUMBER: _ClassVar[int]
    user_sessions: int
    server_sessions: int
    in_logon_surge: bool
    def __init__(self, user_sessions: _Optional[int] = ..., server_sessions: _Optional[int] = ..., in_logon_surge: bool = ...) -> None: ...

class CMsgGCToClientRequestDropped(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CWorkshop_PopulateItemDescriptions_Request(_message.Message):
    __slots__ = ("appid", "languages")
    class SingleItemDescription(_message.Message):
        __slots__ = ("gameitemid", "item_description")
        GAMEITEMID_FIELD_NUMBER: _ClassVar[int]
        ITEM_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        gameitemid: int
        item_description: str
        def __init__(self, gameitemid: _Optional[int] = ..., item_description: _Optional[str] = ...) -> None: ...
    class ItemDescriptionsLanguageBlock(_message.Message):
        __slots__ = ("language", "descriptions")
        LANGUAGE_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
        language: str
        descriptions: _containers.RepeatedCompositeFieldContainer[CWorkshop_PopulateItemDescriptions_Request.SingleItemDescription]
        def __init__(self, language: _Optional[str] = ..., descriptions: _Optional[_Iterable[_Union[CWorkshop_PopulateItemDescriptions_Request.SingleItemDescription, _Mapping]]] = ...) -> None: ...
    APPID_FIELD_NUMBER: _ClassVar[int]
    LANGUAGES_FIELD_NUMBER: _ClassVar[int]
    appid: int
    languages: _containers.RepeatedCompositeFieldContainer[CWorkshop_PopulateItemDescriptions_Request.ItemDescriptionsLanguageBlock]
    def __init__(self, appid: _Optional[int] = ..., languages: _Optional[_Iterable[_Union[CWorkshop_PopulateItemDescriptions_Request.ItemDescriptionsLanguageBlock, _Mapping]]] = ...) -> None: ...

class CWorkshop_GetContributors_Request(_message.Message):
    __slots__ = ("appid", "gameitemid")
    APPID_FIELD_NUMBER: _ClassVar[int]
    GAMEITEMID_FIELD_NUMBER: _ClassVar[int]
    appid: int
    gameitemid: int
    def __init__(self, appid: _Optional[int] = ..., gameitemid: _Optional[int] = ...) -> None: ...

class CWorkshop_GetContributors_Response(_message.Message):
    __slots__ = ("contributors",)
    CONTRIBUTORS_FIELD_NUMBER: _ClassVar[int]
    contributors: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, contributors: _Optional[_Iterable[int]] = ...) -> None: ...

class CWorkshop_SetItemPaymentRules_Request(_message.Message):
    __slots__ = ("appid", "gameitemid", "associated_workshop_files", "partner_accounts", "validate_only", "make_workshop_files_subscribable", "associated_workshop_file_for_direct_payments")
    class WorkshopItemPaymentRule(_message.Message):
        __slots__ = ("workshop_file_id", "revenue_percentage", "rule_description", "rule_type")
        WORKSHOP_FILE_ID_FIELD_NUMBER: _ClassVar[int]
        REVENUE_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
        RULE_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        RULE_TYPE_FIELD_NUMBER: _ClassVar[int]
        workshop_file_id: int
        revenue_percentage: float
        rule_description: str
        rule_type: int
        def __init__(self, workshop_file_id: _Optional[int] = ..., revenue_percentage: _Optional[float] = ..., rule_description: _Optional[str] = ..., rule_type: _Optional[int] = ...) -> None: ...
    class WorkshopDirectPaymentRule(_message.Message):
        __slots__ = ("workshop_file_id", "rule_description")
        WORKSHOP_FILE_ID_FIELD_NUMBER: _ClassVar[int]
        RULE_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        workshop_file_id: int
        rule_description: str
        def __init__(self, workshop_file_id: _Optional[int] = ..., rule_description: _Optional[str] = ...) -> None: ...
    class PartnerItemPaymentRule(_message.Message):
        __slots__ = ("account_id", "revenue_percentage", "rule_description")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        REVENUE_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
        RULE_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        revenue_percentage: float
        rule_description: str
        def __init__(self, account_id: _Optional[int] = ..., revenue_percentage: _Optional[float] = ..., rule_description: _Optional[str] = ...) -> None: ...
    APPID_FIELD_NUMBER: _ClassVar[int]
    GAMEITEMID_FIELD_NUMBER: _ClassVar[int]
    ASSOCIATED_WORKSHOP_FILES_FIELD_NUMBER: _ClassVar[int]
    PARTNER_ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    VALIDATE_ONLY_FIELD_NUMBER: _ClassVar[int]
    MAKE_WORKSHOP_FILES_SUBSCRIBABLE_FIELD_NUMBER: _ClassVar[int]
    ASSOCIATED_WORKSHOP_FILE_FOR_DIRECT_PAYMENTS_FIELD_NUMBER: _ClassVar[int]
    appid: int
    gameitemid: int
    associated_workshop_files: _containers.RepeatedCompositeFieldContainer[CWorkshop_SetItemPaymentRules_Request.WorkshopItemPaymentRule]
    partner_accounts: _containers.RepeatedCompositeFieldContainer[CWorkshop_SetItemPaymentRules_Request.PartnerItemPaymentRule]
    validate_only: bool
    make_workshop_files_subscribable: bool
    associated_workshop_file_for_direct_payments: CWorkshop_SetItemPaymentRules_Request.WorkshopDirectPaymentRule
    def __init__(self, appid: _Optional[int] = ..., gameitemid: _Optional[int] = ..., associated_workshop_files: _Optional[_Iterable[_Union[CWorkshop_SetItemPaymentRules_Request.WorkshopItemPaymentRule, _Mapping]]] = ..., partner_accounts: _Optional[_Iterable[_Union[CWorkshop_SetItemPaymentRules_Request.PartnerItemPaymentRule, _Mapping]]] = ..., validate_only: bool = ..., make_workshop_files_subscribable: bool = ..., associated_workshop_file_for_direct_payments: _Optional[_Union[CWorkshop_SetItemPaymentRules_Request.WorkshopDirectPaymentRule, _Mapping]] = ...) -> None: ...

class CWorkshop_SetItemPaymentRules_Response(_message.Message):
    __slots__ = ("validation_errors",)
    VALIDATION_ERRORS_FIELD_NUMBER: _ClassVar[int]
    validation_errors: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, validation_errors: _Optional[_Iterable[str]] = ...) -> None: ...

class CCommunity_ClanAnnouncementInfo(_message.Message):
    __slots__ = ("gid", "clanid", "posterid", "headline", "posttime", "updatetime", "body", "commentcount", "tags", "language", "hidden", "forum_topic_id")
    GID_FIELD_NUMBER: _ClassVar[int]
    CLANID_FIELD_NUMBER: _ClassVar[int]
    POSTERID_FIELD_NUMBER: _ClassVar[int]
    HEADLINE_FIELD_NUMBER: _ClassVar[int]
    POSTTIME_FIELD_NUMBER: _ClassVar[int]
    UPDATETIME_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    COMMENTCOUNT_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    HIDDEN_FIELD_NUMBER: _ClassVar[int]
    FORUM_TOPIC_ID_FIELD_NUMBER: _ClassVar[int]
    gid: int
    clanid: int
    posterid: int
    headline: str
    posttime: int
    updatetime: int
    body: str
    commentcount: int
    tags: _containers.RepeatedScalarFieldContainer[str]
    language: int
    hidden: bool
    forum_topic_id: int
    def __init__(self, gid: _Optional[int] = ..., clanid: _Optional[int] = ..., posterid: _Optional[int] = ..., headline: _Optional[str] = ..., posttime: _Optional[int] = ..., updatetime: _Optional[int] = ..., body: _Optional[str] = ..., commentcount: _Optional[int] = ..., tags: _Optional[_Iterable[str]] = ..., language: _Optional[int] = ..., hidden: bool = ..., forum_topic_id: _Optional[int] = ...) -> None: ...

class CCommunity_GetClanAnnouncements_Request(_message.Message):
    __slots__ = ("steamid", "offset", "count", "maxchars", "strip_html", "required_tags", "require_no_tags", "language_preference", "hidden_only", "only_gid", "rtime_oldest_date", "include_hidden", "include_partner_events")
    STEAMID_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    MAXCHARS_FIELD_NUMBER: _ClassVar[int]
    STRIP_HTML_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_TAGS_FIELD_NUMBER: _ClassVar[int]
    REQUIRE_NO_TAGS_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_PREFERENCE_FIELD_NUMBER: _ClassVar[int]
    HIDDEN_ONLY_FIELD_NUMBER: _ClassVar[int]
    ONLY_GID_FIELD_NUMBER: _ClassVar[int]
    RTIME_OLDEST_DATE_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_HIDDEN_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_PARTNER_EVENTS_FIELD_NUMBER: _ClassVar[int]
    steamid: int
    offset: int
    count: int
    maxchars: int
    strip_html: bool
    required_tags: _containers.RepeatedScalarFieldContainer[str]
    require_no_tags: bool
    language_preference: _containers.RepeatedScalarFieldContainer[int]
    hidden_only: bool
    only_gid: bool
    rtime_oldest_date: int
    include_hidden: bool
    include_partner_events: bool
    def __init__(self, steamid: _Optional[int] = ..., offset: _Optional[int] = ..., count: _Optional[int] = ..., maxchars: _Optional[int] = ..., strip_html: bool = ..., required_tags: _Optional[_Iterable[str]] = ..., require_no_tags: bool = ..., language_preference: _Optional[_Iterable[int]] = ..., hidden_only: bool = ..., only_gid: bool = ..., rtime_oldest_date: _Optional[int] = ..., include_hidden: bool = ..., include_partner_events: bool = ...) -> None: ...

class CCommunity_GetClanAnnouncements_Response(_message.Message):
    __slots__ = ("maxchars", "strip_html", "announcements")
    MAXCHARS_FIELD_NUMBER: _ClassVar[int]
    STRIP_HTML_FIELD_NUMBER: _ClassVar[int]
    ANNOUNCEMENTS_FIELD_NUMBER: _ClassVar[int]
    maxchars: int
    strip_html: bool
    announcements: _containers.RepeatedCompositeFieldContainer[CCommunity_ClanAnnouncementInfo]
    def __init__(self, maxchars: _Optional[int] = ..., strip_html: bool = ..., announcements: _Optional[_Iterable[_Union[CCommunity_ClanAnnouncementInfo, _Mapping]]] = ...) -> None: ...

class CBroadcast_PostGameDataFrame_Request(_message.Message):
    __slots__ = ("appid", "steamid", "broadcast_id", "frame_data")
    APPID_FIELD_NUMBER: _ClassVar[int]
    STEAMID_FIELD_NUMBER: _ClassVar[int]
    BROADCAST_ID_FIELD_NUMBER: _ClassVar[int]
    FRAME_DATA_FIELD_NUMBER: _ClassVar[int]
    appid: int
    steamid: int
    broadcast_id: int
    frame_data: bytes
    def __init__(self, appid: _Optional[int] = ..., steamid: _Optional[int] = ..., broadcast_id: _Optional[int] = ..., frame_data: _Optional[bytes] = ...) -> None: ...

class CMsgSerializedSOCache(_message.Message):
    __slots__ = ("file_version", "caches", "gc_socache_file_version")
    class TypeCache(_message.Message):
        __slots__ = ("type", "objects", "service_id")
        TYPE_FIELD_NUMBER: _ClassVar[int]
        OBJECTS_FIELD_NUMBER: _ClassVar[int]
        SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
        type: int
        objects: _containers.RepeatedScalarFieldContainer[bytes]
        service_id: int
        def __init__(self, type: _Optional[int] = ..., objects: _Optional[_Iterable[bytes]] = ..., service_id: _Optional[int] = ...) -> None: ...
    class Cache(_message.Message):
        __slots__ = ("type", "id", "versions", "type_caches")
        class Version(_message.Message):
            __slots__ = ("service", "version")
            SERVICE_FIELD_NUMBER: _ClassVar[int]
            VERSION_FIELD_NUMBER: _ClassVar[int]
            service: int
            version: int
            def __init__(self, service: _Optional[int] = ..., version: _Optional[int] = ...) -> None: ...
        TYPE_FIELD_NUMBER: _ClassVar[int]
        ID_FIELD_NUMBER: _ClassVar[int]
        VERSIONS_FIELD_NUMBER: _ClassVar[int]
        TYPE_CACHES_FIELD_NUMBER: _ClassVar[int]
        type: int
        id: int
        versions: _containers.RepeatedCompositeFieldContainer[CMsgSerializedSOCache.Cache.Version]
        type_caches: _containers.RepeatedCompositeFieldContainer[CMsgSerializedSOCache.TypeCache]
        def __init__(self, type: _Optional[int] = ..., id: _Optional[int] = ..., versions: _Optional[_Iterable[_Union[CMsgSerializedSOCache.Cache.Version, _Mapping]]] = ..., type_caches: _Optional[_Iterable[_Union[CMsgSerializedSOCache.TypeCache, _Mapping]]] = ...) -> None: ...
    FILE_VERSION_FIELD_NUMBER: _ClassVar[int]
    CACHES_FIELD_NUMBER: _ClassVar[int]
    GC_SOCACHE_FILE_VERSION_FIELD_NUMBER: _ClassVar[int]
    file_version: int
    caches: _containers.RepeatedCompositeFieldContainer[CMsgSerializedSOCache.Cache]
    gc_socache_file_version: int
    def __init__(self, file_version: _Optional[int] = ..., caches: _Optional[_Iterable[_Union[CMsgSerializedSOCache.Cache, _Mapping]]] = ..., gc_socache_file_version: _Optional[int] = ...) -> None: ...

class CMsgGCToClientPollConvarRequest(_message.Message):
    __slots__ = ("convar_name", "poll_id")
    CONVAR_NAME_FIELD_NUMBER: _ClassVar[int]
    POLL_ID_FIELD_NUMBER: _ClassVar[int]
    convar_name: str
    poll_id: int
    def __init__(self, convar_name: _Optional[str] = ..., poll_id: _Optional[int] = ...) -> None: ...

class CMsgGCToClientPollConvarResponse(_message.Message):
    __slots__ = ("poll_id", "convar_value")
    POLL_ID_FIELD_NUMBER: _ClassVar[int]
    CONVAR_VALUE_FIELD_NUMBER: _ClassVar[int]
    poll_id: int
    convar_value: str
    def __init__(self, poll_id: _Optional[int] = ..., convar_value: _Optional[str] = ...) -> None: ...

class CGCMsgCompressedMsgToClient(_message.Message):
    __slots__ = ("msg_id", "compressed_msg")
    MSG_ID_FIELD_NUMBER: _ClassVar[int]
    COMPRESSED_MSG_FIELD_NUMBER: _ClassVar[int]
    msg_id: int
    compressed_msg: bytes
    def __init__(self, msg_id: _Optional[int] = ..., compressed_msg: _Optional[bytes] = ...) -> None: ...

class CMsgGCToGCMasterBroadcastMessage(_message.Message):
    __slots__ = ("users_per_second", "send_to_users", "send_to_servers", "msg_id", "msg_data", "trusted_servers_only")
    USERS_PER_SECOND_FIELD_NUMBER: _ClassVar[int]
    SEND_TO_USERS_FIELD_NUMBER: _ClassVar[int]
    SEND_TO_SERVERS_FIELD_NUMBER: _ClassVar[int]
    MSG_ID_FIELD_NUMBER: _ClassVar[int]
    MSG_DATA_FIELD_NUMBER: _ClassVar[int]
    TRUSTED_SERVERS_ONLY_FIELD_NUMBER: _ClassVar[int]
    users_per_second: int
    send_to_users: bool
    send_to_servers: bool
    msg_id: int
    msg_data: bytes
    trusted_servers_only: bool
    def __init__(self, users_per_second: _Optional[int] = ..., send_to_users: bool = ..., send_to_servers: bool = ..., msg_id: _Optional[int] = ..., msg_data: _Optional[bytes] = ..., trusted_servers_only: bool = ...) -> None: ...

class CMsgGCToGCMasterSubscribeToCache(_message.Message):
    __slots__ = ("soid_type", "soid_id", "account_ids", "steam_ids")
    SOID_TYPE_FIELD_NUMBER: _ClassVar[int]
    SOID_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_IDS_FIELD_NUMBER: _ClassVar[int]
    STEAM_IDS_FIELD_NUMBER: _ClassVar[int]
    soid_type: int
    soid_id: int
    account_ids: _containers.RepeatedScalarFieldContainer[int]
    steam_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, soid_type: _Optional[int] = ..., soid_id: _Optional[int] = ..., account_ids: _Optional[_Iterable[int]] = ..., steam_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class CMsgGCToGCMasterSubscribeToCacheResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgGCToGCMasterSubscribeToCacheAsync(_message.Message):
    __slots__ = ("subscribe_msg",)
    SUBSCRIBE_MSG_FIELD_NUMBER: _ClassVar[int]
    subscribe_msg: CMsgGCToGCMasterSubscribeToCache
    def __init__(self, subscribe_msg: _Optional[_Union[CMsgGCToGCMasterSubscribeToCache, _Mapping]] = ...) -> None: ...

class CMsgGCToGCMasterUnsubscribeFromCache(_message.Message):
    __slots__ = ("soid_type", "soid_id", "account_ids", "steam_ids")
    SOID_TYPE_FIELD_NUMBER: _ClassVar[int]
    SOID_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_IDS_FIELD_NUMBER: _ClassVar[int]
    STEAM_IDS_FIELD_NUMBER: _ClassVar[int]
    soid_type: int
    soid_id: int
    account_ids: _containers.RepeatedScalarFieldContainer[int]
    steam_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, soid_type: _Optional[int] = ..., soid_id: _Optional[int] = ..., account_ids: _Optional[_Iterable[int]] = ..., steam_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class CMsgGCToGCMasterDestroyCache(_message.Message):
    __slots__ = ("soid_type", "soid_id")
    SOID_TYPE_FIELD_NUMBER: _ClassVar[int]
    SOID_ID_FIELD_NUMBER: _ClassVar[int]
    soid_type: int
    soid_id: int
    def __init__(self, soid_type: _Optional[int] = ..., soid_id: _Optional[int] = ...) -> None: ...
