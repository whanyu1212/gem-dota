from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

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
    def __init__(self, v4: _Optional[int] = ..., v6: _Optional[bytes] = ...) -> None: ...

class CMsgIPAddressBucket(_message.Message):
    __slots__ = ("original_ip_address", "bucket")
    ORIGINAL_IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    original_ip_address: CMsgIPAddress
    bucket: int
    def __init__(self, original_ip_address: _Optional[_Union[CMsgIPAddress, _Mapping]] = ..., bucket: _Optional[int] = ...) -> None: ...

class CMsgProtoBufHeader(_message.Message):
    __slots__ = ("steamid", "client_sessionid", "routing_appid", "jobid_source", "jobid_target", "target_job_name", "seq_num", "eresult", "error_message", "auth_account_flags", "token_source", "admin_spoofing_user", "transport_error", "messageid", "publisher_group_id", "sysid", "trace_tag", "webapi_key_id", "is_from_external_source", "forward_to_sysid", "cm_sysid", "launcher_type", "realm", "timeout_ms", "debug_source", "ip", "ip_v6")
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
    ip: int
    ip_v6: bytes
    def __init__(self, steamid: _Optional[int] = ..., client_sessionid: _Optional[int] = ..., routing_appid: _Optional[int] = ..., jobid_source: _Optional[int] = ..., jobid_target: _Optional[int] = ..., target_job_name: _Optional[str] = ..., seq_num: _Optional[int] = ..., eresult: _Optional[int] = ..., error_message: _Optional[str] = ..., auth_account_flags: _Optional[int] = ..., token_source: _Optional[int] = ..., admin_spoofing_user: bool = ..., transport_error: _Optional[int] = ..., messageid: _Optional[int] = ..., publisher_group_id: _Optional[int] = ..., sysid: _Optional[int] = ..., trace_tag: _Optional[int] = ..., webapi_key_id: _Optional[int] = ..., is_from_external_source: bool = ..., forward_to_sysid: _Optional[_Iterable[int]] = ..., cm_sysid: _Optional[int] = ..., launcher_type: _Optional[int] = ..., realm: _Optional[int] = ..., timeout_ms: _Optional[int] = ..., debug_source: _Optional[str] = ..., ip: _Optional[int] = ..., ip_v6: _Optional[bytes] = ...) -> None: ...

class CMsgMulti(_message.Message):
    __slots__ = ("size_unzipped", "message_body")
    SIZE_UNZIPPED_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_BODY_FIELD_NUMBER: _ClassVar[int]
    size_unzipped: int
    message_body: bytes
    def __init__(self, size_unzipped: _Optional[int] = ..., message_body: _Optional[bytes] = ...) -> None: ...

class CMsgProtobufWrapped(_message.Message):
    __slots__ = ("message_body",)
    MESSAGE_BODY_FIELD_NUMBER: _ClassVar[int]
    message_body: bytes
    def __init__(self, message_body: _Optional[bytes] = ...) -> None: ...

class CMsgAuthTicket(_message.Message):
    __slots__ = ("estate", "eresult", "steamid", "gameid", "h_steam_pipe", "ticket_crc", "ticket")
    ESTATE_FIELD_NUMBER: _ClassVar[int]
    ERESULT_FIELD_NUMBER: _ClassVar[int]
    STEAMID_FIELD_NUMBER: _ClassVar[int]
    GAMEID_FIELD_NUMBER: _ClassVar[int]
    H_STEAM_PIPE_FIELD_NUMBER: _ClassVar[int]
    TICKET_CRC_FIELD_NUMBER: _ClassVar[int]
    TICKET_FIELD_NUMBER: _ClassVar[int]
    estate: int
    eresult: int
    steamid: int
    gameid: int
    h_steam_pipe: int
    ticket_crc: int
    ticket: bytes
    def __init__(self, estate: _Optional[int] = ..., eresult: _Optional[int] = ..., steamid: _Optional[int] = ..., gameid: _Optional[int] = ..., h_steam_pipe: _Optional[int] = ..., ticket_crc: _Optional[int] = ..., ticket: _Optional[bytes] = ...) -> None: ...

class CCDDBAppDetailCommon(_message.Message):
    __slots__ = ("appid", "name", "icon", "tool", "demo", "media", "community_visible_stats", "friendly_name", "propagation", "has_adult_content", "is_visible_in_steam_china", "app_type")
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
    def __init__(self, appid: _Optional[int] = ..., name: _Optional[str] = ..., icon: _Optional[str] = ..., tool: bool = ..., demo: bool = ..., media: bool = ..., community_visible_stats: bool = ..., friendly_name: _Optional[str] = ..., propagation: _Optional[str] = ..., has_adult_content: bool = ..., is_visible_in_steam_china: bool = ..., app_type: _Optional[int] = ...) -> None: ...

class CMsgAppRights(_message.Message):
    __slots__ = ("edit_info", "publish", "view_error_data", "download", "upload_cdkeys", "generate_cdkeys", "view_financials", "manage_ceg", "manage_signing", "manage_cdkeys", "edit_marketing", "economy_support", "economy_support_supervisor", "manage_pricing", "broadcast_live", "view_marketing_traffic", "edit_store_display_content")
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
    def __init__(self, edit_info: bool = ..., publish: bool = ..., view_error_data: bool = ..., download: bool = ..., upload_cdkeys: bool = ..., generate_cdkeys: bool = ..., view_financials: bool = ..., manage_ceg: bool = ..., manage_signing: bool = ..., manage_cdkeys: bool = ..., edit_marketing: bool = ..., economy_support: bool = ..., economy_support_supervisor: bool = ..., manage_pricing: bool = ..., broadcast_live: bool = ..., view_marketing_traffic: bool = ..., edit_store_display_content: bool = ...) -> None: ...

class CCuratorPreferences(_message.Message):
    __slots__ = ("supported_languages", "platform_windows", "platform_mac", "platform_linux", "vr_content", "adult_content_violence", "adult_content_sex", "timestamp_updated", "tagids_curated", "tagids_filtered", "website_title", "website_url", "discussion_url", "show_broadcast")
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
    def __init__(self, supported_languages: _Optional[int] = ..., platform_windows: bool = ..., platform_mac: bool = ..., platform_linux: bool = ..., vr_content: bool = ..., adult_content_violence: bool = ..., adult_content_sex: bool = ..., timestamp_updated: _Optional[int] = ..., tagids_curated: _Optional[_Iterable[int]] = ..., tagids_filtered: _Optional[_Iterable[int]] = ..., website_title: _Optional[str] = ..., website_url: _Optional[str] = ..., discussion_url: _Optional[str] = ..., show_broadcast: bool = ...) -> None: ...

class CLocalizationToken(_message.Message):
    __slots__ = ("language", "localized_string")
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    LOCALIZED_STRING_FIELD_NUMBER: _ClassVar[int]
    language: int
    localized_string: str
    def __init__(self, language: _Optional[int] = ..., localized_string: _Optional[str] = ...) -> None: ...

class CClanEventUserNewsTuple(_message.Message):
    __slots__ = ("clanid", "event_gid", "announcement_gid", "rtime_start", "rtime_end", "priority_score", "type", "clamp_range_slot", "appid", "rtime32_last_modified")
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
    def __init__(self, clanid: _Optional[int] = ..., event_gid: _Optional[int] = ..., announcement_gid: _Optional[int] = ..., rtime_start: _Optional[int] = ..., rtime_end: _Optional[int] = ..., priority_score: _Optional[int] = ..., type: _Optional[int] = ..., clamp_range_slot: _Optional[int] = ..., appid: _Optional[int] = ..., rtime32_last_modified: _Optional[int] = ...) -> None: ...

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
    def __init__(self, rtime_before: _Optional[int] = ..., rtime_after: _Optional[int] = ..., qualified: _Optional[int] = ..., events: _Optional[_Iterable[_Union[CClanEventUserNewsTuple, _Mapping]]] = ...) -> None: ...

class CCommunity_ClanAnnouncementInfo(_message.Message):
    __slots__ = ("gid", "clanid", "posterid", "headline", "posttime", "updatetime", "body", "commentcount", "tags", "language", "hidden", "forum_topic_id", "event_gid", "voteupcount", "votedowncount", "ban_check_result")
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
    def __init__(self, gid: _Optional[int] = ..., clanid: _Optional[int] = ..., posterid: _Optional[int] = ..., headline: _Optional[str] = ..., posttime: _Optional[int] = ..., updatetime: _Optional[int] = ..., body: _Optional[str] = ..., commentcount: _Optional[int] = ..., tags: _Optional[_Iterable[str]] = ..., language: _Optional[int] = ..., hidden: bool = ..., forum_topic_id: _Optional[int] = ..., event_gid: _Optional[int] = ..., voteupcount: _Optional[int] = ..., votedowncount: _Optional[int] = ..., ban_check_result: _Optional[_Union[EBanContentCheckResult, str]] = ...) -> None: ...

class CClanEventData(_message.Message):
    __slots__ = ("gid", "clan_steamid", "event_name", "event_type", "appid", "server_address", "server_password", "rtime32_start_time", "rtime32_end_time", "comment_count", "creator_steamid", "last_update_steamid", "event_notes", "jsondata", "announcement_body", "published", "hidden", "rtime32_visibility_start", "rtime32_visibility_end", "broadcaster_accountid", "follower_count", "ignore_count", "forum_topic_id", "rtime32_last_modified", "news_post_gid", "rtime_mod_reviewed", "featured_app_tagid", "referenced_appids", "build_id", "build_branch")
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
    def __init__(self, gid: _Optional[int] = ..., clan_steamid: _Optional[int] = ..., event_name: _Optional[str] = ..., event_type: _Optional[_Union[EProtoClanEventType, str]] = ..., appid: _Optional[int] = ..., server_address: _Optional[str] = ..., server_password: _Optional[str] = ..., rtime32_start_time: _Optional[int] = ..., rtime32_end_time: _Optional[int] = ..., comment_count: _Optional[int] = ..., creator_steamid: _Optional[int] = ..., last_update_steamid: _Optional[int] = ..., event_notes: _Optional[str] = ..., jsondata: _Optional[str] = ..., announcement_body: _Optional[_Union[CCommunity_ClanAnnouncementInfo, _Mapping]] = ..., published: bool = ..., hidden: bool = ..., rtime32_visibility_start: _Optional[int] = ..., rtime32_visibility_end: _Optional[int] = ..., broadcaster_accountid: _Optional[int] = ..., follower_count: _Optional[int] = ..., ignore_count: _Optional[int] = ..., forum_topic_id: _Optional[int] = ..., rtime32_last_modified: _Optional[int] = ..., news_post_gid: _Optional[int] = ..., rtime_mod_reviewed: _Optional[int] = ..., featured_app_tagid: _Optional[int] = ..., referenced_appids: _Optional[_Iterable[int]] = ..., build_id: _Optional[int] = ..., build_branch: _Optional[str] = ...) -> None: ...

class CBilling_Address(_message.Message):
    __slots__ = ("first_name", "last_name", "address1", "address2", "city", "us_state", "country_code", "postcode", "zip_plus4", "phone")
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
    def __init__(self, first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., address1: _Optional[str] = ..., address2: _Optional[str] = ..., city: _Optional[str] = ..., us_state: _Optional[str] = ..., country_code: _Optional[str] = ..., postcode: _Optional[str] = ..., zip_plus4: _Optional[int] = ..., phone: _Optional[str] = ...) -> None: ...

class CPackageReservationStatus(_message.Message):
    __slots__ = ("packageid", "reservation_state", "queue_position", "total_queue_size", "reservation_country_code", "expired", "time_expires", "time_reserved")
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
    def __init__(self, packageid: _Optional[int] = ..., reservation_state: _Optional[int] = ..., queue_position: _Optional[int] = ..., total_queue_size: _Optional[int] = ..., reservation_country_code: _Optional[str] = ..., expired: bool = ..., time_expires: _Optional[int] = ..., time_reserved: _Optional[int] = ...) -> None: ...

class CMsgKeyValuePair(_message.Message):
    __slots__ = ("name", "value")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: str
    def __init__(self, name: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class CMsgKeyValueSet(_message.Message):
    __slots__ = ("pairs",)
    PAIRS_FIELD_NUMBER: _ClassVar[int]
    pairs: _containers.RepeatedCompositeFieldContainer[CMsgKeyValuePair]
    def __init__(self, pairs: _Optional[_Iterable[_Union[CMsgKeyValuePair, _Mapping]]] = ...) -> None: ...
