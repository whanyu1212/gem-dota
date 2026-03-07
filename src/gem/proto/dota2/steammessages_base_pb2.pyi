from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class EBanContentCheckResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EBanContentCheckResult_NotScanned: _ClassVar[EBanContentCheckResult]
    k_EBanContentCheckResult_Reset: _ClassVar[EBanContentCheckResult]
    k_EBanContentCheckResult_NeedsChecking: _ClassVar[EBanContentCheckResult]
    k_EBanContentCheckResult_VeryUnlikely: _ClassVar[EBanContentCheckResult]
    k_EBanContentCheckResult_Unlikely: _ClassVar[EBanContentCheckResult]
    k_EBanContentCheckResult_Possible: _ClassVar[EBanContentCheckResult]
    k_EBanContentCheckResult_Likely: _ClassVar[EBanContentCheckResult]
    k_EBanContentCheckResult_VeryLikely: _ClassVar[EBanContentCheckResult]

class EProtoClanEventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EClanOtherEvent: _ClassVar[EProtoClanEventType]
    k_EClanGameEvent: _ClassVar[EProtoClanEventType]
    k_EClanPartyEvent: _ClassVar[EProtoClanEventType]
    k_EClanMeetingEvent: _ClassVar[EProtoClanEventType]
    k_EClanSpecialCauseEvent: _ClassVar[EProtoClanEventType]
    k_EClanMusicAndArtsEvent: _ClassVar[EProtoClanEventType]
    k_EClanSportsEvent: _ClassVar[EProtoClanEventType]
    k_EClanTripEvent: _ClassVar[EProtoClanEventType]
    k_EClanChatEvent: _ClassVar[EProtoClanEventType]
    k_EClanGameReleaseEvent: _ClassVar[EProtoClanEventType]
    k_EClanBroadcastEvent: _ClassVar[EProtoClanEventType]
    k_EClanSmallUpdateEvent: _ClassVar[EProtoClanEventType]
    k_EClanPreAnnounceMajorUpdateEvent: _ClassVar[EProtoClanEventType]
    k_EClanMajorUpdateEvent: _ClassVar[EProtoClanEventType]
    k_EClanDLCReleaseEvent: _ClassVar[EProtoClanEventType]
    k_EClanFutureReleaseEvent: _ClassVar[EProtoClanEventType]
    k_EClanESportTournamentStreamEvent: _ClassVar[EProtoClanEventType]
    k_EClanDevStreamEvent: _ClassVar[EProtoClanEventType]
    k_EClanFamousStreamEvent: _ClassVar[EProtoClanEventType]
    k_EClanGameSalesEvent: _ClassVar[EProtoClanEventType]
    k_EClanGameItemSalesEvent: _ClassVar[EProtoClanEventType]
    k_EClanInGameBonusXPEvent: _ClassVar[EProtoClanEventType]
    k_EClanInGameLootEvent: _ClassVar[EProtoClanEventType]
    k_EClanInGamePerksEvent: _ClassVar[EProtoClanEventType]
    k_EClanInGameChallengeEvent: _ClassVar[EProtoClanEventType]
    k_EClanInGameContestEvent: _ClassVar[EProtoClanEventType]
    k_EClanIRLEvent: _ClassVar[EProtoClanEventType]
    k_EClanNewsEvent: _ClassVar[EProtoClanEventType]
    k_EClanBetaReleaseEvent: _ClassVar[EProtoClanEventType]
    k_EClanInGameContentReleaseEvent: _ClassVar[EProtoClanEventType]
    k_EClanFreeTrial: _ClassVar[EProtoClanEventType]
    k_EClanSeasonRelease: _ClassVar[EProtoClanEventType]
    k_EClanSeasonUpdate: _ClassVar[EProtoClanEventType]
    k_EClanCrosspostEvent: _ClassVar[EProtoClanEventType]
    k_EClanInGameEventGeneral: _ClassVar[EProtoClanEventType]

class PartnerEventNotificationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EEventStart: _ClassVar[PartnerEventNotificationType]
    k_EEventBroadcastStart: _ClassVar[PartnerEventNotificationType]
    k_EEventMatchStart: _ClassVar[PartnerEventNotificationType]
    k_EEventPartnerMaxType: _ClassVar[PartnerEventNotificationType]

k_EBanContentCheckResult_NotScanned: EBanContentCheckResult
k_EBanContentCheckResult_Reset: EBanContentCheckResult
k_EBanContentCheckResult_NeedsChecking: EBanContentCheckResult
k_EBanContentCheckResult_VeryUnlikely: EBanContentCheckResult
k_EBanContentCheckResult_Unlikely: EBanContentCheckResult
k_EBanContentCheckResult_Possible: EBanContentCheckResult
k_EBanContentCheckResult_Likely: EBanContentCheckResult
k_EBanContentCheckResult_VeryLikely: EBanContentCheckResult
k_EClanOtherEvent: EProtoClanEventType
k_EClanGameEvent: EProtoClanEventType
k_EClanPartyEvent: EProtoClanEventType
k_EClanMeetingEvent: EProtoClanEventType
k_EClanSpecialCauseEvent: EProtoClanEventType
k_EClanMusicAndArtsEvent: EProtoClanEventType
k_EClanSportsEvent: EProtoClanEventType
k_EClanTripEvent: EProtoClanEventType
k_EClanChatEvent: EProtoClanEventType
k_EClanGameReleaseEvent: EProtoClanEventType
k_EClanBroadcastEvent: EProtoClanEventType
k_EClanSmallUpdateEvent: EProtoClanEventType
k_EClanPreAnnounceMajorUpdateEvent: EProtoClanEventType
k_EClanMajorUpdateEvent: EProtoClanEventType
k_EClanDLCReleaseEvent: EProtoClanEventType
k_EClanFutureReleaseEvent: EProtoClanEventType
k_EClanESportTournamentStreamEvent: EProtoClanEventType
k_EClanDevStreamEvent: EProtoClanEventType
k_EClanFamousStreamEvent: EProtoClanEventType
k_EClanGameSalesEvent: EProtoClanEventType
k_EClanGameItemSalesEvent: EProtoClanEventType
k_EClanInGameBonusXPEvent: EProtoClanEventType
k_EClanInGameLootEvent: EProtoClanEventType
k_EClanInGamePerksEvent: EProtoClanEventType
k_EClanInGameChallengeEvent: EProtoClanEventType
k_EClanInGameContestEvent: EProtoClanEventType
k_EClanIRLEvent: EProtoClanEventType
k_EClanNewsEvent: EProtoClanEventType
k_EClanBetaReleaseEvent: EProtoClanEventType
k_EClanInGameContentReleaseEvent: EProtoClanEventType
k_EClanFreeTrial: EProtoClanEventType
k_EClanSeasonRelease: EProtoClanEventType
k_EClanSeasonUpdate: EProtoClanEventType
k_EClanCrosspostEvent: EProtoClanEventType
k_EClanInGameEventGeneral: EProtoClanEventType
k_EEventStart: PartnerEventNotificationType
k_EEventBroadcastStart: PartnerEventNotificationType
k_EEventMatchStart: PartnerEventNotificationType
k_EEventPartnerMaxType: PartnerEventNotificationType
MSGPOOL_SOFT_LIMIT_FIELD_NUMBER: _ClassVar[int]
msgpool_soft_limit: _descriptor.FieldDescriptor
MSGPOOL_HARD_LIMIT_FIELD_NUMBER: _ClassVar[int]
msgpool_hard_limit: _descriptor.FieldDescriptor
FORCE_PHP_GENERATION_FIELD_NUMBER: _ClassVar[int]
force_php_generation: _descriptor.FieldDescriptor
PHP_OUTPUT_ALWAYS_NUMBER_FIELD_NUMBER: _ClassVar[int]
php_output_always_number: _descriptor.FieldDescriptor
ALLOW_FIELD_NAMED_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
allow_field_named_steam_id: _descriptor.FieldDescriptor

class CMsgIPAddress(_message.Message):
    __slots__ = ("v4", "v6")
    V4_FIELD_NUMBER: _ClassVar[int]
    V6_FIELD_NUMBER: _ClassVar[int]
    v4: int
    v6: bytes
    def __init__(self, v4: int | None = ..., v6: bytes | None = ...) -> None: ...

class CMsgIPAddressBucket(_message.Message):
    __slots__ = ("original_ip_address", "bucket")
    ORIGINAL_IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    original_ip_address: CMsgIPAddress
    bucket: int
    def __init__(
        self, original_ip_address: CMsgIPAddress | _Mapping | None = ..., bucket: int | None = ...
    ) -> None: ...

class CMsgGCRoutingProtoBufHeader(_message.Message):
    __slots__ = ("dst_gcid_queue", "dst_gc_dir_index")
    DST_GCID_QUEUE_FIELD_NUMBER: _ClassVar[int]
    DST_GC_DIR_INDEX_FIELD_NUMBER: _ClassVar[int]
    dst_gcid_queue: int
    dst_gc_dir_index: int
    def __init__(
        self, dst_gcid_queue: int | None = ..., dst_gc_dir_index: int | None = ...
    ) -> None: ...

class CMsgProtoBufHeader(_message.Message):
    __slots__ = (
        "steamid",
        "client_sessionid",
        "routing_appid",
        "jobid_source",
        "jobid_target",
        "target_job_name",
        "seq_num",
        "eresult",
        "error_message",
        "auth_account_flags",
        "token_source",
        "admin_spoofing_user",
        "transport_error",
        "messageid",
        "publisher_group_id",
        "sysid",
        "trace_tag",
        "webapi_key_id",
        "is_from_external_source",
        "forward_to_sysid",
        "cm_sysid",
        "launcher_type",
        "realm",
        "timeout_ms",
        "debug_source",
        "debug_source_string_index",
        "token_id",
        "routing_gc",
        "session_disposition",
        "wg_token",
        "webui_auth_key",
        "ip",
        "ip_v6",
    )
    class ESessionDisposition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_ESessionDispositionNormal: _ClassVar[CMsgProtoBufHeader.ESessionDisposition]
        k_ESessionDispositionDisconnect: _ClassVar[CMsgProtoBufHeader.ESessionDisposition]

    k_ESessionDispositionNormal: CMsgProtoBufHeader.ESessionDisposition
    k_ESessionDispositionDisconnect: CMsgProtoBufHeader.ESessionDisposition
    STEAMID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SESSIONID_FIELD_NUMBER: _ClassVar[int]
    ROUTING_APPID_FIELD_NUMBER: _ClassVar[int]
    JOBID_SOURCE_FIELD_NUMBER: _ClassVar[int]
    JOBID_TARGET_FIELD_NUMBER: _ClassVar[int]
    TARGET_JOB_NAME_FIELD_NUMBER: _ClassVar[int]
    SEQ_NUM_FIELD_NUMBER: _ClassVar[int]
    ERESULT_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    AUTH_ACCOUNT_FLAGS_FIELD_NUMBER: _ClassVar[int]
    TOKEN_SOURCE_FIELD_NUMBER: _ClassVar[int]
    ADMIN_SPOOFING_USER_FIELD_NUMBER: _ClassVar[int]
    TRANSPORT_ERROR_FIELD_NUMBER: _ClassVar[int]
    MESSAGEID_FIELD_NUMBER: _ClassVar[int]
    PUBLISHER_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    SYSID_FIELD_NUMBER: _ClassVar[int]
    TRACE_TAG_FIELD_NUMBER: _ClassVar[int]
    WEBAPI_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    IS_FROM_EXTERNAL_SOURCE_FIELD_NUMBER: _ClassVar[int]
    FORWARD_TO_SYSID_FIELD_NUMBER: _ClassVar[int]
    CM_SYSID_FIELD_NUMBER: _ClassVar[int]
    LAUNCHER_TYPE_FIELD_NUMBER: _ClassVar[int]
    REALM_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    DEBUG_SOURCE_FIELD_NUMBER: _ClassVar[int]
    DEBUG_SOURCE_STRING_INDEX_FIELD_NUMBER: _ClassVar[int]
    TOKEN_ID_FIELD_NUMBER: _ClassVar[int]
    ROUTING_GC_FIELD_NUMBER: _ClassVar[int]
    SESSION_DISPOSITION_FIELD_NUMBER: _ClassVar[int]
    WG_TOKEN_FIELD_NUMBER: _ClassVar[int]
    WEBUI_AUTH_KEY_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    IP_V6_FIELD_NUMBER: _ClassVar[int]
    steamid: int
    client_sessionid: int
    routing_appid: int
    jobid_source: int
    jobid_target: int
    target_job_name: str
    seq_num: int
    eresult: int
    error_message: str
    auth_account_flags: int
    token_source: int
    admin_spoofing_user: bool
    transport_error: int
    messageid: int
    publisher_group_id: int
    sysid: int
    trace_tag: int
    webapi_key_id: int
    is_from_external_source: bool
    forward_to_sysid: _containers.RepeatedScalarFieldContainer[int]
    cm_sysid: int
    launcher_type: int
    realm: int
    timeout_ms: int
    debug_source: str
    debug_source_string_index: int
    token_id: int
    routing_gc: CMsgGCRoutingProtoBufHeader
    session_disposition: CMsgProtoBufHeader.ESessionDisposition
    wg_token: str
    webui_auth_key: str
    ip: int
    ip_v6: bytes
    def __init__(
        self,
        steamid: int | None = ...,
        client_sessionid: int | None = ...,
        routing_appid: int | None = ...,
        jobid_source: int | None = ...,
        jobid_target: int | None = ...,
        target_job_name: str | None = ...,
        seq_num: int | None = ...,
        eresult: int | None = ...,
        error_message: str | None = ...,
        auth_account_flags: int | None = ...,
        token_source: int | None = ...,
        admin_spoofing_user: bool = ...,
        transport_error: int | None = ...,
        messageid: int | None = ...,
        publisher_group_id: int | None = ...,
        sysid: int | None = ...,
        trace_tag: int | None = ...,
        webapi_key_id: int | None = ...,
        is_from_external_source: bool = ...,
        forward_to_sysid: _Iterable[int] | None = ...,
        cm_sysid: int | None = ...,
        launcher_type: int | None = ...,
        realm: int | None = ...,
        timeout_ms: int | None = ...,
        debug_source: str | None = ...,
        debug_source_string_index: int | None = ...,
        token_id: int | None = ...,
        routing_gc: CMsgGCRoutingProtoBufHeader | _Mapping | None = ...,
        session_disposition: CMsgProtoBufHeader.ESessionDisposition | str | None = ...,
        wg_token: str | None = ...,
        webui_auth_key: str | None = ...,
        ip: int | None = ...,
        ip_v6: bytes | None = ...,
    ) -> None: ...

class CMsgMulti(_message.Message):
    __slots__ = ("size_unzipped", "message_body")
    SIZE_UNZIPPED_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_BODY_FIELD_NUMBER: _ClassVar[int]
    size_unzipped: int
    message_body: bytes
    def __init__(
        self, size_unzipped: int | None = ..., message_body: bytes | None = ...
    ) -> None: ...

class CMsgProtobufWrapped(_message.Message):
    __slots__ = ("message_body",)
    MESSAGE_BODY_FIELD_NUMBER: _ClassVar[int]
    message_body: bytes
    def __init__(self, message_body: bytes | None = ...) -> None: ...

class CMsgAuthTicket(_message.Message):
    __slots__ = (
        "estate",
        "eresult",
        "steamid",
        "gameid",
        "h_steam_pipe",
        "ticket_crc",
        "ticket",
        "server_secret",
        "ticket_type",
    )
    ESTATE_FIELD_NUMBER: _ClassVar[int]
    ERESULT_FIELD_NUMBER: _ClassVar[int]
    STEAMID_FIELD_NUMBER: _ClassVar[int]
    GAMEID_FIELD_NUMBER: _ClassVar[int]
    H_STEAM_PIPE_FIELD_NUMBER: _ClassVar[int]
    TICKET_CRC_FIELD_NUMBER: _ClassVar[int]
    TICKET_FIELD_NUMBER: _ClassVar[int]
    SERVER_SECRET_FIELD_NUMBER: _ClassVar[int]
    TICKET_TYPE_FIELD_NUMBER: _ClassVar[int]
    estate: int
    eresult: int
    steamid: int
    gameid: int
    h_steam_pipe: int
    ticket_crc: int
    ticket: bytes
    server_secret: bytes
    ticket_type: int
    def __init__(
        self,
        estate: int | None = ...,
        eresult: int | None = ...,
        steamid: int | None = ...,
        gameid: int | None = ...,
        h_steam_pipe: int | None = ...,
        ticket_crc: int | None = ...,
        ticket: bytes | None = ...,
        server_secret: bytes | None = ...,
        ticket_type: int | None = ...,
    ) -> None: ...

class CCDDBAppDetailCommon(_message.Message):
    __slots__ = (
        "appid",
        "name",
        "icon",
        "tool",
        "demo",
        "media",
        "community_visible_stats",
        "friendly_name",
        "propagation",
        "has_adult_content",
        "is_visible_in_steam_china",
        "app_type",
        "has_adult_content_sex",
        "has_adult_content_violence",
        "content_descriptorids",
    )
    APPID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ICON_FIELD_NUMBER: _ClassVar[int]
    TOOL_FIELD_NUMBER: _ClassVar[int]
    DEMO_FIELD_NUMBER: _ClassVar[int]
    MEDIA_FIELD_NUMBER: _ClassVar[int]
    COMMUNITY_VISIBLE_STATS_FIELD_NUMBER: _ClassVar[int]
    FRIENDLY_NAME_FIELD_NUMBER: _ClassVar[int]
    PROPAGATION_FIELD_NUMBER: _ClassVar[int]
    HAS_ADULT_CONTENT_FIELD_NUMBER: _ClassVar[int]
    IS_VISIBLE_IN_STEAM_CHINA_FIELD_NUMBER: _ClassVar[int]
    APP_TYPE_FIELD_NUMBER: _ClassVar[int]
    HAS_ADULT_CONTENT_SEX_FIELD_NUMBER: _ClassVar[int]
    HAS_ADULT_CONTENT_VIOLENCE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_DESCRIPTORIDS_FIELD_NUMBER: _ClassVar[int]
    appid: int
    name: str
    icon: str
    tool: bool
    demo: bool
    media: bool
    community_visible_stats: bool
    friendly_name: str
    propagation: str
    has_adult_content: bool
    is_visible_in_steam_china: bool
    app_type: int
    has_adult_content_sex: bool
    has_adult_content_violence: bool
    content_descriptorids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        appid: int | None = ...,
        name: str | None = ...,
        icon: str | None = ...,
        tool: bool = ...,
        demo: bool = ...,
        media: bool = ...,
        community_visible_stats: bool = ...,
        friendly_name: str | None = ...,
        propagation: str | None = ...,
        has_adult_content: bool = ...,
        is_visible_in_steam_china: bool = ...,
        app_type: int | None = ...,
        has_adult_content_sex: bool = ...,
        has_adult_content_violence: bool = ...,
        content_descriptorids: _Iterable[int] | None = ...,
    ) -> None: ...

class CMsgAppRights(_message.Message):
    __slots__ = (
        "edit_info",
        "publish",
        "view_error_data",
        "download",
        "upload_cdkeys",
        "generate_cdkeys",
        "view_financials",
        "manage_ceg",
        "manage_signing",
        "manage_cdkeys",
        "edit_marketing",
        "economy_support",
        "economy_support_supervisor",
        "manage_pricing",
        "broadcast_live",
        "view_marketing_traffic",
        "edit_store_display_content",
    )
    EDIT_INFO_FIELD_NUMBER: _ClassVar[int]
    PUBLISH_FIELD_NUMBER: _ClassVar[int]
    VIEW_ERROR_DATA_FIELD_NUMBER: _ClassVar[int]
    DOWNLOAD_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_CDKEYS_FIELD_NUMBER: _ClassVar[int]
    GENERATE_CDKEYS_FIELD_NUMBER: _ClassVar[int]
    VIEW_FINANCIALS_FIELD_NUMBER: _ClassVar[int]
    MANAGE_CEG_FIELD_NUMBER: _ClassVar[int]
    MANAGE_SIGNING_FIELD_NUMBER: _ClassVar[int]
    MANAGE_CDKEYS_FIELD_NUMBER: _ClassVar[int]
    EDIT_MARKETING_FIELD_NUMBER: _ClassVar[int]
    ECONOMY_SUPPORT_FIELD_NUMBER: _ClassVar[int]
    ECONOMY_SUPPORT_SUPERVISOR_FIELD_NUMBER: _ClassVar[int]
    MANAGE_PRICING_FIELD_NUMBER: _ClassVar[int]
    BROADCAST_LIVE_FIELD_NUMBER: _ClassVar[int]
    VIEW_MARKETING_TRAFFIC_FIELD_NUMBER: _ClassVar[int]
    EDIT_STORE_DISPLAY_CONTENT_FIELD_NUMBER: _ClassVar[int]
    edit_info: bool
    publish: bool
    view_error_data: bool
    download: bool
    upload_cdkeys: bool
    generate_cdkeys: bool
    view_financials: bool
    manage_ceg: bool
    manage_signing: bool
    manage_cdkeys: bool
    edit_marketing: bool
    economy_support: bool
    economy_support_supervisor: bool
    manage_pricing: bool
    broadcast_live: bool
    view_marketing_traffic: bool
    edit_store_display_content: bool
    def __init__(
        self,
        edit_info: bool = ...,
        publish: bool = ...,
        view_error_data: bool = ...,
        download: bool = ...,
        upload_cdkeys: bool = ...,
        generate_cdkeys: bool = ...,
        view_financials: bool = ...,
        manage_ceg: bool = ...,
        manage_signing: bool = ...,
        manage_cdkeys: bool = ...,
        edit_marketing: bool = ...,
        economy_support: bool = ...,
        economy_support_supervisor: bool = ...,
        manage_pricing: bool = ...,
        broadcast_live: bool = ...,
        view_marketing_traffic: bool = ...,
        edit_store_display_content: bool = ...,
    ) -> None: ...

class CCuratorPreferences(_message.Message):
    __slots__ = (
        "supported_languages",
        "platform_windows",
        "platform_mac",
        "platform_linux",
        "vr_content",
        "adult_content_violence",
        "adult_content_sex",
        "timestamp_updated",
        "tagids_curated",
        "tagids_filtered",
        "website_title",
        "website_url",
        "discussion_url",
        "show_broadcast",
    )
    SUPPORTED_LANGUAGES_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_WINDOWS_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_MAC_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_LINUX_FIELD_NUMBER: _ClassVar[int]
    VR_CONTENT_FIELD_NUMBER: _ClassVar[int]
    ADULT_CONTENT_VIOLENCE_FIELD_NUMBER: _ClassVar[int]
    ADULT_CONTENT_SEX_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_UPDATED_FIELD_NUMBER: _ClassVar[int]
    TAGIDS_CURATED_FIELD_NUMBER: _ClassVar[int]
    TAGIDS_FILTERED_FIELD_NUMBER: _ClassVar[int]
    WEBSITE_TITLE_FIELD_NUMBER: _ClassVar[int]
    WEBSITE_URL_FIELD_NUMBER: _ClassVar[int]
    DISCUSSION_URL_FIELD_NUMBER: _ClassVar[int]
    SHOW_BROADCAST_FIELD_NUMBER: _ClassVar[int]
    supported_languages: int
    platform_windows: bool
    platform_mac: bool
    platform_linux: bool
    vr_content: bool
    adult_content_violence: bool
    adult_content_sex: bool
    timestamp_updated: int
    tagids_curated: _containers.RepeatedScalarFieldContainer[int]
    tagids_filtered: _containers.RepeatedScalarFieldContainer[int]
    website_title: str
    website_url: str
    discussion_url: str
    show_broadcast: bool
    def __init__(
        self,
        supported_languages: int | None = ...,
        platform_windows: bool = ...,
        platform_mac: bool = ...,
        platform_linux: bool = ...,
        vr_content: bool = ...,
        adult_content_violence: bool = ...,
        adult_content_sex: bool = ...,
        timestamp_updated: int | None = ...,
        tagids_curated: _Iterable[int] | None = ...,
        tagids_filtered: _Iterable[int] | None = ...,
        website_title: str | None = ...,
        website_url: str | None = ...,
        discussion_url: str | None = ...,
        show_broadcast: bool = ...,
    ) -> None: ...

class CLocalizationToken(_message.Message):
    __slots__ = ("language", "localized_string")
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    LOCALIZED_STRING_FIELD_NUMBER: _ClassVar[int]
    language: int
    localized_string: str
    def __init__(self, language: int | None = ..., localized_string: str | None = ...) -> None: ...

class CClanEventUserNewsTuple(_message.Message):
    __slots__ = (
        "clanid",
        "event_gid",
        "announcement_gid",
        "rtime_start",
        "rtime_end",
        "priority_score",
        "type",
        "clamp_range_slot",
        "appid",
        "rtime32_last_modified",
    )
    CLANID_FIELD_NUMBER: _ClassVar[int]
    EVENT_GID_FIELD_NUMBER: _ClassVar[int]
    ANNOUNCEMENT_GID_FIELD_NUMBER: _ClassVar[int]
    RTIME_START_FIELD_NUMBER: _ClassVar[int]
    RTIME_END_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_SCORE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CLAMP_RANGE_SLOT_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    RTIME32_LAST_MODIFIED_FIELD_NUMBER: _ClassVar[int]
    clanid: int
    event_gid: int
    announcement_gid: int
    rtime_start: int
    rtime_end: int
    priority_score: int
    type: int
    clamp_range_slot: int
    appid: int
    rtime32_last_modified: int
    def __init__(
        self,
        clanid: int | None = ...,
        event_gid: int | None = ...,
        announcement_gid: int | None = ...,
        rtime_start: int | None = ...,
        rtime_end: int | None = ...,
        priority_score: int | None = ...,
        type: int | None = ...,
        clamp_range_slot: int | None = ...,
        appid: int | None = ...,
        rtime32_last_modified: int | None = ...,
    ) -> None: ...

class CClanMatchEventByRange(_message.Message):
    __slots__ = ("rtime_before", "rtime_after", "qualified", "events")
    RTIME_BEFORE_FIELD_NUMBER: _ClassVar[int]
    RTIME_AFTER_FIELD_NUMBER: _ClassVar[int]
    QUALIFIED_FIELD_NUMBER: _ClassVar[int]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    rtime_before: int
    rtime_after: int
    qualified: int
    events: _containers.RepeatedCompositeFieldContainer[CClanEventUserNewsTuple]
    def __init__(
        self,
        rtime_before: int | None = ...,
        rtime_after: int | None = ...,
        qualified: int | None = ...,
        events: _Iterable[CClanEventUserNewsTuple | _Mapping] | None = ...,
    ) -> None: ...

class CCommunity_ClanAnnouncementInfo(_message.Message):
    __slots__ = (
        "gid",
        "clanid",
        "posterid",
        "headline",
        "posttime",
        "updatetime",
        "body",
        "commentcount",
        "tags",
        "language",
        "hidden",
        "forum_topic_id",
        "event_gid",
        "voteupcount",
        "votedowncount",
        "ban_check_result",
        "banned",
    )
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
    EVENT_GID_FIELD_NUMBER: _ClassVar[int]
    VOTEUPCOUNT_FIELD_NUMBER: _ClassVar[int]
    VOTEDOWNCOUNT_FIELD_NUMBER: _ClassVar[int]
    BAN_CHECK_RESULT_FIELD_NUMBER: _ClassVar[int]
    BANNED_FIELD_NUMBER: _ClassVar[int]
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
    event_gid: int
    voteupcount: int
    votedowncount: int
    ban_check_result: EBanContentCheckResult
    banned: bool
    def __init__(
        self,
        gid: int | None = ...,
        clanid: int | None = ...,
        posterid: int | None = ...,
        headline: str | None = ...,
        posttime: int | None = ...,
        updatetime: int | None = ...,
        body: str | None = ...,
        commentcount: int | None = ...,
        tags: _Iterable[str] | None = ...,
        language: int | None = ...,
        hidden: bool = ...,
        forum_topic_id: int | None = ...,
        event_gid: int | None = ...,
        voteupcount: int | None = ...,
        votedowncount: int | None = ...,
        ban_check_result: EBanContentCheckResult | str | None = ...,
        banned: bool = ...,
    ) -> None: ...

class CClanEventData(_message.Message):
    __slots__ = (
        "gid",
        "clan_steamid",
        "event_name",
        "event_type",
        "appid",
        "server_address",
        "server_password",
        "rtime32_start_time",
        "rtime32_end_time",
        "comment_count",
        "creator_steamid",
        "last_update_steamid",
        "event_notes",
        "jsondata",
        "announcement_body",
        "published",
        "hidden",
        "rtime32_visibility_start",
        "rtime32_visibility_end",
        "broadcaster_accountid",
        "follower_count",
        "ignore_count",
        "forum_topic_id",
        "rtime32_last_modified",
        "news_post_gid",
        "rtime_mod_reviewed",
        "featured_app_tagid",
        "referenced_appids",
        "build_id",
        "build_branch",
    )
    GID_FIELD_NUMBER: _ClassVar[int]
    CLAN_STEAMID_FIELD_NUMBER: _ClassVar[int]
    EVENT_NAME_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    SERVER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SERVER_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    RTIME32_START_TIME_FIELD_NUMBER: _ClassVar[int]
    RTIME32_END_TIME_FIELD_NUMBER: _ClassVar[int]
    COMMENT_COUNT_FIELD_NUMBER: _ClassVar[int]
    CREATOR_STEAMID_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATE_STEAMID_FIELD_NUMBER: _ClassVar[int]
    EVENT_NOTES_FIELD_NUMBER: _ClassVar[int]
    JSONDATA_FIELD_NUMBER: _ClassVar[int]
    ANNOUNCEMENT_BODY_FIELD_NUMBER: _ClassVar[int]
    PUBLISHED_FIELD_NUMBER: _ClassVar[int]
    HIDDEN_FIELD_NUMBER: _ClassVar[int]
    RTIME32_VISIBILITY_START_FIELD_NUMBER: _ClassVar[int]
    RTIME32_VISIBILITY_END_FIELD_NUMBER: _ClassVar[int]
    BROADCASTER_ACCOUNTID_FIELD_NUMBER: _ClassVar[int]
    FOLLOWER_COUNT_FIELD_NUMBER: _ClassVar[int]
    IGNORE_COUNT_FIELD_NUMBER: _ClassVar[int]
    FORUM_TOPIC_ID_FIELD_NUMBER: _ClassVar[int]
    RTIME32_LAST_MODIFIED_FIELD_NUMBER: _ClassVar[int]
    NEWS_POST_GID_FIELD_NUMBER: _ClassVar[int]
    RTIME_MOD_REVIEWED_FIELD_NUMBER: _ClassVar[int]
    FEATURED_APP_TAGID_FIELD_NUMBER: _ClassVar[int]
    REFERENCED_APPIDS_FIELD_NUMBER: _ClassVar[int]
    BUILD_ID_FIELD_NUMBER: _ClassVar[int]
    BUILD_BRANCH_FIELD_NUMBER: _ClassVar[int]
    gid: int
    clan_steamid: int
    event_name: str
    event_type: EProtoClanEventType
    appid: int
    server_address: str
    server_password: str
    rtime32_start_time: int
    rtime32_end_time: int
    comment_count: int
    creator_steamid: int
    last_update_steamid: int
    event_notes: str
    jsondata: str
    announcement_body: CCommunity_ClanAnnouncementInfo
    published: bool
    hidden: bool
    rtime32_visibility_start: int
    rtime32_visibility_end: int
    broadcaster_accountid: int
    follower_count: int
    ignore_count: int
    forum_topic_id: int
    rtime32_last_modified: int
    news_post_gid: int
    rtime_mod_reviewed: int
    featured_app_tagid: int
    referenced_appids: _containers.RepeatedScalarFieldContainer[int]
    build_id: int
    build_branch: str
    def __init__(
        self,
        gid: int | None = ...,
        clan_steamid: int | None = ...,
        event_name: str | None = ...,
        event_type: EProtoClanEventType | str | None = ...,
        appid: int | None = ...,
        server_address: str | None = ...,
        server_password: str | None = ...,
        rtime32_start_time: int | None = ...,
        rtime32_end_time: int | None = ...,
        comment_count: int | None = ...,
        creator_steamid: int | None = ...,
        last_update_steamid: int | None = ...,
        event_notes: str | None = ...,
        jsondata: str | None = ...,
        announcement_body: CCommunity_ClanAnnouncementInfo | _Mapping | None = ...,
        published: bool = ...,
        hidden: bool = ...,
        rtime32_visibility_start: int | None = ...,
        rtime32_visibility_end: int | None = ...,
        broadcaster_accountid: int | None = ...,
        follower_count: int | None = ...,
        ignore_count: int | None = ...,
        forum_topic_id: int | None = ...,
        rtime32_last_modified: int | None = ...,
        news_post_gid: int | None = ...,
        rtime_mod_reviewed: int | None = ...,
        featured_app_tagid: int | None = ...,
        referenced_appids: _Iterable[int] | None = ...,
        build_id: int | None = ...,
        build_branch: str | None = ...,
    ) -> None: ...

class CBilling_Address(_message.Message):
    __slots__ = (
        "first_name",
        "last_name",
        "address1",
        "address2",
        "city",
        "us_state",
        "country_code",
        "postcode",
        "zip_plus4",
        "phone",
    )
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    ADDRESS1_FIELD_NUMBER: _ClassVar[int]
    ADDRESS2_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    US_STATE_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_CODE_FIELD_NUMBER: _ClassVar[int]
    POSTCODE_FIELD_NUMBER: _ClassVar[int]
    ZIP_PLUS4_FIELD_NUMBER: _ClassVar[int]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    first_name: str
    last_name: str
    address1: str
    address2: str
    city: str
    us_state: str
    country_code: str
    postcode: str
    zip_plus4: int
    phone: str
    def __init__(
        self,
        first_name: str | None = ...,
        last_name: str | None = ...,
        address1: str | None = ...,
        address2: str | None = ...,
        city: str | None = ...,
        us_state: str | None = ...,
        country_code: str | None = ...,
        postcode: str | None = ...,
        zip_plus4: int | None = ...,
        phone: str | None = ...,
    ) -> None: ...

class CPackageReservationStatus(_message.Message):
    __slots__ = (
        "packageid",
        "reservation_state",
        "queue_position",
        "total_queue_size",
        "reservation_country_code",
        "expired",
        "time_expires",
        "time_reserved",
    )
    PACKAGEID_FIELD_NUMBER: _ClassVar[int]
    RESERVATION_STATE_FIELD_NUMBER: _ClassVar[int]
    QUEUE_POSITION_FIELD_NUMBER: _ClassVar[int]
    TOTAL_QUEUE_SIZE_FIELD_NUMBER: _ClassVar[int]
    RESERVATION_COUNTRY_CODE_FIELD_NUMBER: _ClassVar[int]
    EXPIRED_FIELD_NUMBER: _ClassVar[int]
    TIME_EXPIRES_FIELD_NUMBER: _ClassVar[int]
    TIME_RESERVED_FIELD_NUMBER: _ClassVar[int]
    packageid: int
    reservation_state: int
    queue_position: int
    total_queue_size: int
    reservation_country_code: str
    expired: bool
    time_expires: int
    time_reserved: int
    def __init__(
        self,
        packageid: int | None = ...,
        reservation_state: int | None = ...,
        queue_position: int | None = ...,
        total_queue_size: int | None = ...,
        reservation_country_code: str | None = ...,
        expired: bool = ...,
        time_expires: int | None = ...,
        time_reserved: int | None = ...,
    ) -> None: ...

class CMsgKeyValuePair(_message.Message):
    __slots__ = ("name", "value")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: str
    def __init__(self, name: str | None = ..., value: str | None = ...) -> None: ...

class CMsgKeyValueSet(_message.Message):
    __slots__ = ("pairs",)
    PAIRS_FIELD_NUMBER: _ClassVar[int]
    pairs: _containers.RepeatedCompositeFieldContainer[CMsgKeyValuePair]
    def __init__(self, pairs: _Iterable[CMsgKeyValuePair | _Mapping] | None = ...) -> None: ...

class UserContentDescriptorPreferences(_message.Message):
    __slots__ = ("content_descriptors_to_exclude",)
    class ContentDescriptor(_message.Message):
        __slots__ = ("content_descriptorid", "timestamp_added")
        CONTENT_DESCRIPTORID_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_ADDED_FIELD_NUMBER: _ClassVar[int]
        content_descriptorid: int
        timestamp_added: int
        def __init__(
            self, content_descriptorid: int | None = ..., timestamp_added: int | None = ...
        ) -> None: ...

    CONTENT_DESCRIPTORS_TO_EXCLUDE_FIELD_NUMBER: _ClassVar[int]
    content_descriptors_to_exclude: _containers.RepeatedCompositeFieldContainer[
        UserContentDescriptorPreferences.ContentDescriptor
    ]
    def __init__(
        self,
        content_descriptors_to_exclude: _Iterable[
            UserContentDescriptorPreferences.ContentDescriptor | _Mapping
        ]
        | None = ...,
    ) -> None: ...
