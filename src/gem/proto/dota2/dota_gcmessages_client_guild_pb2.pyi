from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class EGuildAuditAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EGuildAuditAction_Invalid: _ClassVar[EGuildAuditAction]
    k_EGuildAuditAction_GuildCreated: _ClassVar[EGuildAuditAction]
    k_EGuildAuditAction_GuildLanguageChanged: _ClassVar[EGuildAuditAction]
    k_EGuildAuditAction_GuildFlagsChanged: _ClassVar[EGuildAuditAction]
    k_EGuildAuditAction_GuildMemberJoined: _ClassVar[EGuildAuditAction]
    k_EGuildAuditAction_GuildMemberLeft: _ClassVar[EGuildAuditAction]
    k_EGuildAuditAction_GuildMemberKicked: _ClassVar[EGuildAuditAction]
    k_EGuildAuditAction_GuildMemberRoleChanged: _ClassVar[EGuildAuditAction]
    k_EGuildAuditAction_GuildLogoChanged: _ClassVar[EGuildAuditAction]
    k_EGuildAuditAction_GuildRegionChanged: _ClassVar[EGuildAuditAction]
    k_EGuildAuditAction_GuildDescriptionChanged: _ClassVar[EGuildAuditAction]
    k_EGuildAuditAction_GuildPrimaryColorChanged: _ClassVar[EGuildAuditAction]
    k_EGuildAuditAction_GuildSecondaryColorChanged: _ClassVar[EGuildAuditAction]
    k_EGuildAuditAction_GuildPatternChanged: _ClassVar[EGuildAuditAction]
    k_EGuildAuditAction_AdminClearedLogo: _ClassVar[EGuildAuditAction]
    k_EGuildAuditAction_GuildRequiredRankChanged: _ClassVar[EGuildAuditAction]
    k_EGuildAuditAction_GuildMotDChanged: _ClassVar[EGuildAuditAction]
    k_EGuildAuditAction_AdminResetName: _ClassVar[EGuildAuditAction]
    k_EGuildAuditAction_AdminResetTag: _ClassVar[EGuildAuditAction]
    k_EGuildAuditAction_AdminLock: _ClassVar[EGuildAuditAction]
    k_EGuildAuditAction_GuildNameChanged: _ClassVar[EGuildAuditAction]
    k_EGuildAuditAction_GuildTagChanged: _ClassVar[EGuildAuditAction]
    k_EGuildAuditAction_AdminPermitted: _ClassVar[EGuildAuditAction]
    k_EGuildAuditAction_AdminBlocked: _ClassVar[EGuildAuditAction]
    k_EGuildAuditAction_AdminBannedUser: _ClassVar[EGuildAuditAction]
    k_EGuildAuditAction_AdminExonerated: _ClassVar[EGuildAuditAction]

class EGuildChatType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EGuildChatType_Unspecified: _ClassVar[EGuildChatType]
    k_EGuildChatType_SteamChatGroup: _ClassVar[EGuildChatType]
    k_EGuildChatType_GC: _ClassVar[EGuildChatType]

k_EGuildAuditAction_Invalid: EGuildAuditAction
k_EGuildAuditAction_GuildCreated: EGuildAuditAction
k_EGuildAuditAction_GuildLanguageChanged: EGuildAuditAction
k_EGuildAuditAction_GuildFlagsChanged: EGuildAuditAction
k_EGuildAuditAction_GuildMemberJoined: EGuildAuditAction
k_EGuildAuditAction_GuildMemberLeft: EGuildAuditAction
k_EGuildAuditAction_GuildMemberKicked: EGuildAuditAction
k_EGuildAuditAction_GuildMemberRoleChanged: EGuildAuditAction
k_EGuildAuditAction_GuildLogoChanged: EGuildAuditAction
k_EGuildAuditAction_GuildRegionChanged: EGuildAuditAction
k_EGuildAuditAction_GuildDescriptionChanged: EGuildAuditAction
k_EGuildAuditAction_GuildPrimaryColorChanged: EGuildAuditAction
k_EGuildAuditAction_GuildSecondaryColorChanged: EGuildAuditAction
k_EGuildAuditAction_GuildPatternChanged: EGuildAuditAction
k_EGuildAuditAction_AdminClearedLogo: EGuildAuditAction
k_EGuildAuditAction_GuildRequiredRankChanged: EGuildAuditAction
k_EGuildAuditAction_GuildMotDChanged: EGuildAuditAction
k_EGuildAuditAction_AdminResetName: EGuildAuditAction
k_EGuildAuditAction_AdminResetTag: EGuildAuditAction
k_EGuildAuditAction_AdminLock: EGuildAuditAction
k_EGuildAuditAction_GuildNameChanged: EGuildAuditAction
k_EGuildAuditAction_GuildTagChanged: EGuildAuditAction
k_EGuildAuditAction_AdminPermitted: EGuildAuditAction
k_EGuildAuditAction_AdminBlocked: EGuildAuditAction
k_EGuildAuditAction_AdminBannedUser: EGuildAuditAction
k_EGuildAuditAction_AdminExonerated: EGuildAuditAction
k_EGuildChatType_Unspecified: EGuildChatType
k_EGuildChatType_SteamChatGroup: EGuildChatType
k_EGuildChatType_GC: EGuildChatType

class CMsgGuildInfo(_message.Message):
    __slots__ = (
        "guild_name",
        "guild_tag",
        "created_timestamp",
        "guild_language",
        "guild_flags",
        "guild_logo",
        "guild_region",
        "guild_chat_group_id",
        "guild_description",
        "default_chat_channel_id",
        "guild_primary_color",
        "guild_secondary_color",
        "guild_pattern",
        "guild_refresh_time_offset",
        "guild_required_rank_tier",
        "guild_motd_timestamp",
        "guild_motd",
    )
    GUILD_NAME_FIELD_NUMBER: _ClassVar[int]
    GUILD_TAG_FIELD_NUMBER: _ClassVar[int]
    CREATED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    GUILD_LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    GUILD_FLAGS_FIELD_NUMBER: _ClassVar[int]
    GUILD_LOGO_FIELD_NUMBER: _ClassVar[int]
    GUILD_REGION_FIELD_NUMBER: _ClassVar[int]
    GUILD_CHAT_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    GUILD_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_CHAT_CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    GUILD_PRIMARY_COLOR_FIELD_NUMBER: _ClassVar[int]
    GUILD_SECONDARY_COLOR_FIELD_NUMBER: _ClassVar[int]
    GUILD_PATTERN_FIELD_NUMBER: _ClassVar[int]
    GUILD_REFRESH_TIME_OFFSET_FIELD_NUMBER: _ClassVar[int]
    GUILD_REQUIRED_RANK_TIER_FIELD_NUMBER: _ClassVar[int]
    GUILD_MOTD_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    GUILD_MOTD_FIELD_NUMBER: _ClassVar[int]
    guild_name: str
    guild_tag: str
    created_timestamp: int
    guild_language: int
    guild_flags: int
    guild_logo: int
    guild_region: int
    guild_chat_group_id: int
    guild_description: str
    default_chat_channel_id: int
    guild_primary_color: int
    guild_secondary_color: int
    guild_pattern: int
    guild_refresh_time_offset: int
    guild_required_rank_tier: int
    guild_motd_timestamp: int
    guild_motd: str
    def __init__(
        self,
        guild_name: str | None = ...,
        guild_tag: str | None = ...,
        created_timestamp: int | None = ...,
        guild_language: int | None = ...,
        guild_flags: int | None = ...,
        guild_logo: int | None = ...,
        guild_region: int | None = ...,
        guild_chat_group_id: int | None = ...,
        guild_description: str | None = ...,
        default_chat_channel_id: int | None = ...,
        guild_primary_color: int | None = ...,
        guild_secondary_color: int | None = ...,
        guild_pattern: int | None = ...,
        guild_refresh_time_offset: int | None = ...,
        guild_required_rank_tier: int | None = ...,
        guild_motd_timestamp: int | None = ...,
        guild_motd: str | None = ...,
    ) -> None: ...

class CMsgGuildSummary(_message.Message):
    __slots__ = ("guild_info", "member_count", "event_points")
    class EventPoints(_message.Message):
        __slots__ = (
            "event_id",
            "guild_points",
            "guild_rank",
            "guild_weekly_rank",
            "guild_weekly_percentile",
            "guild_current_percentile",
        )
        EVENT_ID_FIELD_NUMBER: _ClassVar[int]
        GUILD_POINTS_FIELD_NUMBER: _ClassVar[int]
        GUILD_RANK_FIELD_NUMBER: _ClassVar[int]
        GUILD_WEEKLY_RANK_FIELD_NUMBER: _ClassVar[int]
        GUILD_WEEKLY_PERCENTILE_FIELD_NUMBER: _ClassVar[int]
        GUILD_CURRENT_PERCENTILE_FIELD_NUMBER: _ClassVar[int]
        event_id: int
        guild_points: int
        guild_rank: int
        guild_weekly_rank: int
        guild_weekly_percentile: int
        guild_current_percentile: int
        def __init__(
            self,
            event_id: int | None = ...,
            guild_points: int | None = ...,
            guild_rank: int | None = ...,
            guild_weekly_rank: int | None = ...,
            guild_weekly_percentile: int | None = ...,
            guild_current_percentile: int | None = ...,
        ) -> None: ...

    GUILD_INFO_FIELD_NUMBER: _ClassVar[int]
    MEMBER_COUNT_FIELD_NUMBER: _ClassVar[int]
    EVENT_POINTS_FIELD_NUMBER: _ClassVar[int]
    guild_info: CMsgGuildInfo
    member_count: int
    event_points: _containers.RepeatedCompositeFieldContainer[CMsgGuildSummary.EventPoints]
    def __init__(
        self,
        guild_info: CMsgGuildInfo | _Mapping | None = ...,
        member_count: int | None = ...,
        event_points: _Iterable[CMsgGuildSummary.EventPoints | _Mapping] | None = ...,
    ) -> None: ...

class CMsgGuildRole(_message.Message):
    __slots__ = ("role_id", "role_name", "role_flags", "role_order")
    ROLE_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_NAME_FIELD_NUMBER: _ClassVar[int]
    ROLE_FLAGS_FIELD_NUMBER: _ClassVar[int]
    ROLE_ORDER_FIELD_NUMBER: _ClassVar[int]
    role_id: int
    role_name: str
    role_flags: int
    role_order: int
    def __init__(
        self,
        role_id: int | None = ...,
        role_name: str | None = ...,
        role_flags: int | None = ...,
        role_order: int | None = ...,
    ) -> None: ...

class CMsgGuildMember(_message.Message):
    __slots__ = (
        "member_account_id",
        "member_role_id",
        "member_joined_timestamp",
        "member_last_active_timestamp",
    )
    MEMBER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    MEMBER_ROLE_ID_FIELD_NUMBER: _ClassVar[int]
    MEMBER_JOINED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MEMBER_LAST_ACTIVE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    member_account_id: int
    member_role_id: int
    member_joined_timestamp: int
    member_last_active_timestamp: int
    def __init__(
        self,
        member_account_id: int | None = ...,
        member_role_id: int | None = ...,
        member_joined_timestamp: int | None = ...,
        member_last_active_timestamp: int | None = ...,
    ) -> None: ...

class CMsgGuildInvite(_message.Message):
    __slots__ = ("requester_account_id", "target_account_id", "timestamp_sent")
    REQUESTER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_SENT_FIELD_NUMBER: _ClassVar[int]
    requester_account_id: int
    target_account_id: int
    timestamp_sent: int
    def __init__(
        self,
        requester_account_id: int | None = ...,
        target_account_id: int | None = ...,
        timestamp_sent: int | None = ...,
    ) -> None: ...

class CMsgGuildData(_message.Message):
    __slots__ = ("guild_id", "guild_info", "guild_roles", "guild_members", "guild_invites")
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    GUILD_INFO_FIELD_NUMBER: _ClassVar[int]
    GUILD_ROLES_FIELD_NUMBER: _ClassVar[int]
    GUILD_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    GUILD_INVITES_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    guild_info: CMsgGuildInfo
    guild_roles: _containers.RepeatedCompositeFieldContainer[CMsgGuildRole]
    guild_members: _containers.RepeatedCompositeFieldContainer[CMsgGuildMember]
    guild_invites: _containers.RepeatedCompositeFieldContainer[CMsgGuildInvite]
    def __init__(
        self,
        guild_id: int | None = ...,
        guild_info: CMsgGuildInfo | _Mapping | None = ...,
        guild_roles: _Iterable[CMsgGuildRole | _Mapping] | None = ...,
        guild_members: _Iterable[CMsgGuildMember | _Mapping] | None = ...,
        guild_invites: _Iterable[CMsgGuildInvite | _Mapping] | None = ...,
    ) -> None: ...

class CMsgAccountGuildInvite(_message.Message):
    __slots__ = ("guild_id", "requester_account_id", "timestamp_sent")
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    REQUESTER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_SENT_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    requester_account_id: int
    timestamp_sent: int
    def __init__(
        self,
        guild_id: int | None = ...,
        requester_account_id: int | None = ...,
        timestamp_sent: int | None = ...,
    ) -> None: ...

class CMsgAccountGuildMemberships(_message.Message):
    __slots__ = ("guild_ids", "guild_invites")
    GUILD_IDS_FIELD_NUMBER: _ClassVar[int]
    GUILD_INVITES_FIELD_NUMBER: _ClassVar[int]
    guild_ids: _containers.RepeatedScalarFieldContainer[int]
    guild_invites: _containers.RepeatedCompositeFieldContainer[CMsgAccountGuildInvite]
    def __init__(
        self,
        guild_ids: _Iterable[int] | None = ...,
        guild_invites: _Iterable[CMsgAccountGuildInvite | _Mapping] | None = ...,
    ) -> None: ...

class CMsgGuildPersonaInfo(_message.Message):
    __slots__ = ("guild_id", "guild_tag", "guild_flags")
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    GUILD_TAG_FIELD_NUMBER: _ClassVar[int]
    GUILD_FLAGS_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    guild_tag: str
    guild_flags: int
    def __init__(
        self, guild_id: int | None = ..., guild_tag: str | None = ..., guild_flags: int | None = ...
    ) -> None: ...

class CMsgAccountGuildsPersonaInfo(_message.Message):
    __slots__ = ("guild_persona_infos",)
    GUILD_PERSONA_INFOS_FIELD_NUMBER: _ClassVar[int]
    guild_persona_infos: _containers.RepeatedCompositeFieldContainer[CMsgGuildPersonaInfo]
    def __init__(
        self, guild_persona_infos: _Iterable[CMsgGuildPersonaInfo | _Mapping] | None = ...
    ) -> None: ...

class CMsgGuildFeedEvent(_message.Message):
    __slots__ = (
        "feed_event_id",
        "timestamp",
        "event_type",
        "param_uint_1",
        "param_uint_2",
        "param_uint_3",
    )
    FEED_EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARAM_UINT_1_FIELD_NUMBER: _ClassVar[int]
    PARAM_UINT_2_FIELD_NUMBER: _ClassVar[int]
    PARAM_UINT_3_FIELD_NUMBER: _ClassVar[int]
    feed_event_id: int
    timestamp: int
    event_type: int
    param_uint_1: int
    param_uint_2: int
    param_uint_3: int
    def __init__(
        self,
        feed_event_id: int | None = ...,
        timestamp: int | None = ...,
        event_type: int | None = ...,
        param_uint_1: int | None = ...,
        param_uint_2: int | None = ...,
        param_uint_3: int | None = ...,
    ) -> None: ...

class CMsgClientToGCCreateGuild(_message.Message):
    __slots__ = ("guild_info", "guild_chat_type")
    GUILD_INFO_FIELD_NUMBER: _ClassVar[int]
    GUILD_CHAT_TYPE_FIELD_NUMBER: _ClassVar[int]
    guild_info: CMsgGuildInfo
    guild_chat_type: EGuildChatType
    def __init__(
        self,
        guild_info: CMsgGuildInfo | _Mapping | None = ...,
        guild_chat_type: EGuildChatType | str | None = ...,
    ) -> None: ...

class CMsgClientToGCCreateGuildResponse(_message.Message):
    __slots__ = ("result", "guild_id")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCCreateGuildResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCCreateGuildResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCCreateGuildResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCCreateGuildResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCCreateGuildResponse.EResponse]
        k_eInvalidName: _ClassVar[CMsgClientToGCCreateGuildResponse.EResponse]
        k_eNameAlreadyUsed: _ClassVar[CMsgClientToGCCreateGuildResponse.EResponse]
        k_eInvalidTag: _ClassVar[CMsgClientToGCCreateGuildResponse.EResponse]
        k_eTagAlreadyUsed: _ClassVar[CMsgClientToGCCreateGuildResponse.EResponse]
        k_eInvalidDescription: _ClassVar[CMsgClientToGCCreateGuildResponse.EResponse]
        k_eInvalidRegion: _ClassVar[CMsgClientToGCCreateGuildResponse.EResponse]
        k_eInvalidLogo: _ClassVar[CMsgClientToGCCreateGuildResponse.EResponse]
        k_eDoesNotOwnEvent: _ClassVar[CMsgClientToGCCreateGuildResponse.EResponse]
        k_eGuildLimit: _ClassVar[CMsgClientToGCCreateGuildResponse.EResponse]
        k_eInvalidMotD: _ClassVar[CMsgClientToGCCreateGuildResponse.EResponse]
        k_eBlocked: _ClassVar[CMsgClientToGCCreateGuildResponse.EResponse]
        k_eFreeTrialNotAllowed: _ClassVar[CMsgClientToGCCreateGuildResponse.EResponse]

    k_eInternalError: CMsgClientToGCCreateGuildResponse.EResponse
    k_eSuccess: CMsgClientToGCCreateGuildResponse.EResponse
    k_eTooBusy: CMsgClientToGCCreateGuildResponse.EResponse
    k_eDisabled: CMsgClientToGCCreateGuildResponse.EResponse
    k_eTimeout: CMsgClientToGCCreateGuildResponse.EResponse
    k_eInvalidName: CMsgClientToGCCreateGuildResponse.EResponse
    k_eNameAlreadyUsed: CMsgClientToGCCreateGuildResponse.EResponse
    k_eInvalidTag: CMsgClientToGCCreateGuildResponse.EResponse
    k_eTagAlreadyUsed: CMsgClientToGCCreateGuildResponse.EResponse
    k_eInvalidDescription: CMsgClientToGCCreateGuildResponse.EResponse
    k_eInvalidRegion: CMsgClientToGCCreateGuildResponse.EResponse
    k_eInvalidLogo: CMsgClientToGCCreateGuildResponse.EResponse
    k_eDoesNotOwnEvent: CMsgClientToGCCreateGuildResponse.EResponse
    k_eGuildLimit: CMsgClientToGCCreateGuildResponse.EResponse
    k_eInvalidMotD: CMsgClientToGCCreateGuildResponse.EResponse
    k_eBlocked: CMsgClientToGCCreateGuildResponse.EResponse
    k_eFreeTrialNotAllowed: CMsgClientToGCCreateGuildResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCCreateGuildResponse.EResponse
    guild_id: int
    def __init__(
        self,
        result: CMsgClientToGCCreateGuildResponse.EResponse | str | None = ...,
        guild_id: int | None = ...,
    ) -> None: ...

class CMsgClientToGCSetGuildInfo(_message.Message):
    __slots__ = ("guild_id", "guild_info", "guild_chat_type")
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    GUILD_INFO_FIELD_NUMBER: _ClassVar[int]
    GUILD_CHAT_TYPE_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    guild_info: CMsgGuildInfo
    guild_chat_type: EGuildChatType
    def __init__(
        self,
        guild_id: int | None = ...,
        guild_info: CMsgGuildInfo | _Mapping | None = ...,
        guild_chat_type: EGuildChatType | str | None = ...,
    ) -> None: ...

class CMsgClientToGCSetGuildInfoResponse(_message.Message):
    __slots__ = ("result",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCSetGuildInfoResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCSetGuildInfoResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCSetGuildInfoResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCSetGuildInfoResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCSetGuildInfoResponse.EResponse]
        k_eInvalidGuild: _ClassVar[CMsgClientToGCSetGuildInfoResponse.EResponse]
        k_eNotMember: _ClassVar[CMsgClientToGCSetGuildInfoResponse.EResponse]
        k_eNoPermission: _ClassVar[CMsgClientToGCSetGuildInfoResponse.EResponse]
        k_eMotDTooLong: _ClassVar[CMsgClientToGCSetGuildInfoResponse.EResponse]
        k_eNameChangeNoPermissions: _ClassVar[CMsgClientToGCSetGuildInfoResponse.EResponse]
        k_eTagChangeNoPermissions: _ClassVar[CMsgClientToGCSetGuildInfoResponse.EResponse]
        k_eNameInvalid: _ClassVar[CMsgClientToGCSetGuildInfoResponse.EResponse]
        k_eTagInvalid: _ClassVar[CMsgClientToGCSetGuildInfoResponse.EResponse]
        k_eDescriptionInvalid: _ClassVar[CMsgClientToGCSetGuildInfoResponse.EResponse]
        k_eBlocked: _ClassVar[CMsgClientToGCSetGuildInfoResponse.EResponse]

    k_eInternalError: CMsgClientToGCSetGuildInfoResponse.EResponse
    k_eSuccess: CMsgClientToGCSetGuildInfoResponse.EResponse
    k_eTooBusy: CMsgClientToGCSetGuildInfoResponse.EResponse
    k_eDisabled: CMsgClientToGCSetGuildInfoResponse.EResponse
    k_eTimeout: CMsgClientToGCSetGuildInfoResponse.EResponse
    k_eInvalidGuild: CMsgClientToGCSetGuildInfoResponse.EResponse
    k_eNotMember: CMsgClientToGCSetGuildInfoResponse.EResponse
    k_eNoPermission: CMsgClientToGCSetGuildInfoResponse.EResponse
    k_eMotDTooLong: CMsgClientToGCSetGuildInfoResponse.EResponse
    k_eNameChangeNoPermissions: CMsgClientToGCSetGuildInfoResponse.EResponse
    k_eTagChangeNoPermissions: CMsgClientToGCSetGuildInfoResponse.EResponse
    k_eNameInvalid: CMsgClientToGCSetGuildInfoResponse.EResponse
    k_eTagInvalid: CMsgClientToGCSetGuildInfoResponse.EResponse
    k_eDescriptionInvalid: CMsgClientToGCSetGuildInfoResponse.EResponse
    k_eBlocked: CMsgClientToGCSetGuildInfoResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCSetGuildInfoResponse.EResponse
    def __init__(
        self, result: CMsgClientToGCSetGuildInfoResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCRequestGuildData(_message.Message):
    __slots__ = ("guild_id",)
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    def __init__(self, guild_id: int | None = ...) -> None: ...

class CMsgClientToGCRequestGuildDataResponse(_message.Message):
    __slots__ = ("result", "guild_data")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCRequestGuildDataResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCRequestGuildDataResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCRequestGuildDataResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCRequestGuildDataResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCRequestGuildDataResponse.EResponse]
        k_eInvalidGuild: _ClassVar[CMsgClientToGCRequestGuildDataResponse.EResponse]
        k_eNotMember: _ClassVar[CMsgClientToGCRequestGuildDataResponse.EResponse]

    k_eInternalError: CMsgClientToGCRequestGuildDataResponse.EResponse
    k_eSuccess: CMsgClientToGCRequestGuildDataResponse.EResponse
    k_eTooBusy: CMsgClientToGCRequestGuildDataResponse.EResponse
    k_eDisabled: CMsgClientToGCRequestGuildDataResponse.EResponse
    k_eTimeout: CMsgClientToGCRequestGuildDataResponse.EResponse
    k_eInvalidGuild: CMsgClientToGCRequestGuildDataResponse.EResponse
    k_eNotMember: CMsgClientToGCRequestGuildDataResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    GUILD_DATA_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCRequestGuildDataResponse.EResponse
    guild_data: CMsgGuildData
    def __init__(
        self,
        result: CMsgClientToGCRequestGuildDataResponse.EResponse | str | None = ...,
        guild_data: CMsgGuildData | _Mapping | None = ...,
    ) -> None: ...

class CMsgGCToClientGuildDataUpdated(_message.Message):
    __slots__ = ("guild_data", "update_flags")
    GUILD_DATA_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FLAGS_FIELD_NUMBER: _ClassVar[int]
    guild_data: CMsgGuildData
    update_flags: int
    def __init__(
        self, guild_data: CMsgGuildData | _Mapping | None = ..., update_flags: int | None = ...
    ) -> None: ...

class CMsgGCToClientGuildMembersDataUpdated(_message.Message):
    __slots__ = ("guild_id", "members_data")
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_DATA_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    members_data: _containers.RepeatedCompositeFieldContainer[CMsgGuildMember]
    def __init__(
        self,
        guild_id: int | None = ...,
        members_data: _Iterable[CMsgGuildMember | _Mapping] | None = ...,
    ) -> None: ...

class CMsgClientToGCRequestGuildMembership(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCRequestGuildMembershipResponse(_message.Message):
    __slots__ = ("result", "guild_memberships")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCRequestGuildMembershipResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCRequestGuildMembershipResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCRequestGuildMembershipResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCRequestGuildMembershipResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCRequestGuildMembershipResponse.EResponse]

    k_eInternalError: CMsgClientToGCRequestGuildMembershipResponse.EResponse
    k_eSuccess: CMsgClientToGCRequestGuildMembershipResponse.EResponse
    k_eTooBusy: CMsgClientToGCRequestGuildMembershipResponse.EResponse
    k_eDisabled: CMsgClientToGCRequestGuildMembershipResponse.EResponse
    k_eTimeout: CMsgClientToGCRequestGuildMembershipResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    GUILD_MEMBERSHIPS_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCRequestGuildMembershipResponse.EResponse
    guild_memberships: CMsgAccountGuildMemberships
    def __init__(
        self,
        result: CMsgClientToGCRequestGuildMembershipResponse.EResponse | str | None = ...,
        guild_memberships: CMsgAccountGuildMemberships | _Mapping | None = ...,
    ) -> None: ...

class CMsgGCToClientGuildMembershipUpdated(_message.Message):
    __slots__ = ("guild_memberships",)
    GUILD_MEMBERSHIPS_FIELD_NUMBER: _ClassVar[int]
    guild_memberships: CMsgAccountGuildMemberships
    def __init__(
        self, guild_memberships: CMsgAccountGuildMemberships | _Mapping | None = ...
    ) -> None: ...

class CMsgClientToGCJoinGuild(_message.Message):
    __slots__ = ("guild_id",)
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    def __init__(self, guild_id: int | None = ...) -> None: ...

class CMsgClientToGCJoinGuildResponse(_message.Message):
    __slots__ = ("result",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCJoinGuildResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCJoinGuildResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCJoinGuildResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCJoinGuildResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCJoinGuildResponse.EResponse]
        k_eInvalidGuild: _ClassVar[CMsgClientToGCJoinGuildResponse.EResponse]
        k_eGuildFull: _ClassVar[CMsgClientToGCJoinGuildResponse.EResponse]
        k_eAlreadyMember: _ClassVar[CMsgClientToGCJoinGuildResponse.EResponse]
        k_eGuildLimit: _ClassVar[CMsgClientToGCJoinGuildResponse.EResponse]
        k_eGuildRequiresInvite: _ClassVar[CMsgClientToGCJoinGuildResponse.EResponse]
        k_eGuildRankTooLow: _ClassVar[CMsgClientToGCJoinGuildResponse.EResponse]

    k_eInternalError: CMsgClientToGCJoinGuildResponse.EResponse
    k_eSuccess: CMsgClientToGCJoinGuildResponse.EResponse
    k_eTooBusy: CMsgClientToGCJoinGuildResponse.EResponse
    k_eDisabled: CMsgClientToGCJoinGuildResponse.EResponse
    k_eTimeout: CMsgClientToGCJoinGuildResponse.EResponse
    k_eInvalidGuild: CMsgClientToGCJoinGuildResponse.EResponse
    k_eGuildFull: CMsgClientToGCJoinGuildResponse.EResponse
    k_eAlreadyMember: CMsgClientToGCJoinGuildResponse.EResponse
    k_eGuildLimit: CMsgClientToGCJoinGuildResponse.EResponse
    k_eGuildRequiresInvite: CMsgClientToGCJoinGuildResponse.EResponse
    k_eGuildRankTooLow: CMsgClientToGCJoinGuildResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCJoinGuildResponse.EResponse
    def __init__(
        self, result: CMsgClientToGCJoinGuildResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCLeaveGuild(_message.Message):
    __slots__ = ("guild_id",)
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    def __init__(self, guild_id: int | None = ...) -> None: ...

class CMsgClientToGCLeaveGuildResponse(_message.Message):
    __slots__ = ("result",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCLeaveGuildResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCLeaveGuildResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCLeaveGuildResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCLeaveGuildResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCLeaveGuildResponse.EResponse]
        k_eInvalidGuild: _ClassVar[CMsgClientToGCLeaveGuildResponse.EResponse]
        k_eNotMember: _ClassVar[CMsgClientToGCLeaveGuildResponse.EResponse]
        k_eLastAdmin: _ClassVar[CMsgClientToGCLeaveGuildResponse.EResponse]

    k_eInternalError: CMsgClientToGCLeaveGuildResponse.EResponse
    k_eSuccess: CMsgClientToGCLeaveGuildResponse.EResponse
    k_eTooBusy: CMsgClientToGCLeaveGuildResponse.EResponse
    k_eDisabled: CMsgClientToGCLeaveGuildResponse.EResponse
    k_eTimeout: CMsgClientToGCLeaveGuildResponse.EResponse
    k_eInvalidGuild: CMsgClientToGCLeaveGuildResponse.EResponse
    k_eNotMember: CMsgClientToGCLeaveGuildResponse.EResponse
    k_eLastAdmin: CMsgClientToGCLeaveGuildResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCLeaveGuildResponse.EResponse
    def __init__(
        self, result: CMsgClientToGCLeaveGuildResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCKickGuildMember(_message.Message):
    __slots__ = ("guild_id", "target_account_id")
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    target_account_id: int
    def __init__(self, guild_id: int | None = ..., target_account_id: int | None = ...) -> None: ...

class CMsgClientToGCKickGuildMemberResponse(_message.Message):
    __slots__ = ("result",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCKickGuildMemberResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCKickGuildMemberResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCKickGuildMemberResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCKickGuildMemberResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCKickGuildMemberResponse.EResponse]
        k_eInvalidGuild: _ClassVar[CMsgClientToGCKickGuildMemberResponse.EResponse]
        k_eRequesterNotMember: _ClassVar[CMsgClientToGCKickGuildMemberResponse.EResponse]
        k_eTargetNotMember: _ClassVar[CMsgClientToGCKickGuildMemberResponse.EResponse]
        k_eNoPermission: _ClassVar[CMsgClientToGCKickGuildMemberResponse.EResponse]
        k_eCantKickSelf: _ClassVar[CMsgClientToGCKickGuildMemberResponse.EResponse]

    k_eInternalError: CMsgClientToGCKickGuildMemberResponse.EResponse
    k_eSuccess: CMsgClientToGCKickGuildMemberResponse.EResponse
    k_eTooBusy: CMsgClientToGCKickGuildMemberResponse.EResponse
    k_eDisabled: CMsgClientToGCKickGuildMemberResponse.EResponse
    k_eTimeout: CMsgClientToGCKickGuildMemberResponse.EResponse
    k_eInvalidGuild: CMsgClientToGCKickGuildMemberResponse.EResponse
    k_eRequesterNotMember: CMsgClientToGCKickGuildMemberResponse.EResponse
    k_eTargetNotMember: CMsgClientToGCKickGuildMemberResponse.EResponse
    k_eNoPermission: CMsgClientToGCKickGuildMemberResponse.EResponse
    k_eCantKickSelf: CMsgClientToGCKickGuildMemberResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCKickGuildMemberResponse.EResponse
    def __init__(
        self, result: CMsgClientToGCKickGuildMemberResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCSetGuildMemberRole(_message.Message):
    __slots__ = ("guild_id", "target_account_id", "target_role_id")
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_ROLE_ID_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    target_account_id: int
    target_role_id: int
    def __init__(
        self,
        guild_id: int | None = ...,
        target_account_id: int | None = ...,
        target_role_id: int | None = ...,
    ) -> None: ...

class CMsgClientToGCSetGuildMemberRoleResponse(_message.Message):
    __slots__ = ("result",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCSetGuildMemberRoleResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCSetGuildMemberRoleResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCSetGuildMemberRoleResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCSetGuildMemberRoleResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCSetGuildMemberRoleResponse.EResponse]
        k_eInvalidGuild: _ClassVar[CMsgClientToGCSetGuildMemberRoleResponse.EResponse]
        k_eRequesterNotMember: _ClassVar[CMsgClientToGCSetGuildMemberRoleResponse.EResponse]
        k_eTargetNotMember: _ClassVar[CMsgClientToGCSetGuildMemberRoleResponse.EResponse]
        k_eNoPermission: _ClassVar[CMsgClientToGCSetGuildMemberRoleResponse.EResponse]
        k_eInvalidRole: _ClassVar[CMsgClientToGCSetGuildMemberRoleResponse.EResponse]
        k_eAdminViolation: _ClassVar[CMsgClientToGCSetGuildMemberRoleResponse.EResponse]

    k_eInternalError: CMsgClientToGCSetGuildMemberRoleResponse.EResponse
    k_eSuccess: CMsgClientToGCSetGuildMemberRoleResponse.EResponse
    k_eTooBusy: CMsgClientToGCSetGuildMemberRoleResponse.EResponse
    k_eDisabled: CMsgClientToGCSetGuildMemberRoleResponse.EResponse
    k_eTimeout: CMsgClientToGCSetGuildMemberRoleResponse.EResponse
    k_eInvalidGuild: CMsgClientToGCSetGuildMemberRoleResponse.EResponse
    k_eRequesterNotMember: CMsgClientToGCSetGuildMemberRoleResponse.EResponse
    k_eTargetNotMember: CMsgClientToGCSetGuildMemberRoleResponse.EResponse
    k_eNoPermission: CMsgClientToGCSetGuildMemberRoleResponse.EResponse
    k_eInvalidRole: CMsgClientToGCSetGuildMemberRoleResponse.EResponse
    k_eAdminViolation: CMsgClientToGCSetGuildMemberRoleResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCSetGuildMemberRoleResponse.EResponse
    def __init__(
        self, result: CMsgClientToGCSetGuildMemberRoleResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCInviteToGuild(_message.Message):
    __slots__ = ("guild_id", "target_account_id")
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    target_account_id: int
    def __init__(self, guild_id: int | None = ..., target_account_id: int | None = ...) -> None: ...

class CMsgClientToGCInviteToGuildResponse(_message.Message):
    __slots__ = ("result",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCInviteToGuildResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCInviteToGuildResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCInviteToGuildResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCInviteToGuildResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCInviteToGuildResponse.EResponse]
        k_eInvalidGuild: _ClassVar[CMsgClientToGCInviteToGuildResponse.EResponse]
        k_eGuildFull: _ClassVar[CMsgClientToGCInviteToGuildResponse.EResponse]
        k_eRequesterNotMember: _ClassVar[CMsgClientToGCInviteToGuildResponse.EResponse]
        k_eAlreadyAMember: _ClassVar[CMsgClientToGCInviteToGuildResponse.EResponse]
        k_eAlreadyInvited: _ClassVar[CMsgClientToGCInviteToGuildResponse.EResponse]
        k_eNoInvitePermissions: _ClassVar[CMsgClientToGCInviteToGuildResponse.EResponse]
        k_eTooManyInvites: _ClassVar[CMsgClientToGCInviteToGuildResponse.EResponse]
        k_eInvalidUser: _ClassVar[CMsgClientToGCInviteToGuildResponse.EResponse]

    k_eInternalError: CMsgClientToGCInviteToGuildResponse.EResponse
    k_eSuccess: CMsgClientToGCInviteToGuildResponse.EResponse
    k_eTooBusy: CMsgClientToGCInviteToGuildResponse.EResponse
    k_eDisabled: CMsgClientToGCInviteToGuildResponse.EResponse
    k_eTimeout: CMsgClientToGCInviteToGuildResponse.EResponse
    k_eInvalidGuild: CMsgClientToGCInviteToGuildResponse.EResponse
    k_eGuildFull: CMsgClientToGCInviteToGuildResponse.EResponse
    k_eRequesterNotMember: CMsgClientToGCInviteToGuildResponse.EResponse
    k_eAlreadyAMember: CMsgClientToGCInviteToGuildResponse.EResponse
    k_eAlreadyInvited: CMsgClientToGCInviteToGuildResponse.EResponse
    k_eNoInvitePermissions: CMsgClientToGCInviteToGuildResponse.EResponse
    k_eTooManyInvites: CMsgClientToGCInviteToGuildResponse.EResponse
    k_eInvalidUser: CMsgClientToGCInviteToGuildResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCInviteToGuildResponse.EResponse
    def __init__(
        self, result: CMsgClientToGCInviteToGuildResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCDeclineInviteToGuild(_message.Message):
    __slots__ = ("guild_id",)
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    def __init__(self, guild_id: int | None = ...) -> None: ...

class CMsgClientToGCDeclineInviteToGuildResponse(_message.Message):
    __slots__ = ("result",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCDeclineInviteToGuildResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCDeclineInviteToGuildResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCDeclineInviteToGuildResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCDeclineInviteToGuildResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCDeclineInviteToGuildResponse.EResponse]
        k_eInvalidGuild: _ClassVar[CMsgClientToGCDeclineInviteToGuildResponse.EResponse]
        k_eNoInviteFound: _ClassVar[CMsgClientToGCDeclineInviteToGuildResponse.EResponse]

    k_eInternalError: CMsgClientToGCDeclineInviteToGuildResponse.EResponse
    k_eSuccess: CMsgClientToGCDeclineInviteToGuildResponse.EResponse
    k_eTooBusy: CMsgClientToGCDeclineInviteToGuildResponse.EResponse
    k_eDisabled: CMsgClientToGCDeclineInviteToGuildResponse.EResponse
    k_eTimeout: CMsgClientToGCDeclineInviteToGuildResponse.EResponse
    k_eInvalidGuild: CMsgClientToGCDeclineInviteToGuildResponse.EResponse
    k_eNoInviteFound: CMsgClientToGCDeclineInviteToGuildResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCDeclineInviteToGuildResponse.EResponse
    def __init__(
        self, result: CMsgClientToGCDeclineInviteToGuildResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCAcceptInviteToGuild(_message.Message):
    __slots__ = ("guild_id",)
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    def __init__(self, guild_id: int | None = ...) -> None: ...

class CMsgClientToGCAcceptInviteToGuildResponse(_message.Message):
    __slots__ = ("result",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCAcceptInviteToGuildResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCAcceptInviteToGuildResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCAcceptInviteToGuildResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCAcceptInviteToGuildResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCAcceptInviteToGuildResponse.EResponse]
        k_eInvalidGuild: _ClassVar[CMsgClientToGCAcceptInviteToGuildResponse.EResponse]
        k_eNoInviteFound: _ClassVar[CMsgClientToGCAcceptInviteToGuildResponse.EResponse]
        k_eGuildFull: _ClassVar[CMsgClientToGCAcceptInviteToGuildResponse.EResponse]
        k_eGuildLimit: _ClassVar[CMsgClientToGCAcceptInviteToGuildResponse.EResponse]
        k_eInvalidInviter: _ClassVar[CMsgClientToGCAcceptInviteToGuildResponse.EResponse]
        k_eAlreadyInGuild: _ClassVar[CMsgClientToGCAcceptInviteToGuildResponse.EResponse]

    k_eInternalError: CMsgClientToGCAcceptInviteToGuildResponse.EResponse
    k_eSuccess: CMsgClientToGCAcceptInviteToGuildResponse.EResponse
    k_eTooBusy: CMsgClientToGCAcceptInviteToGuildResponse.EResponse
    k_eDisabled: CMsgClientToGCAcceptInviteToGuildResponse.EResponse
    k_eTimeout: CMsgClientToGCAcceptInviteToGuildResponse.EResponse
    k_eInvalidGuild: CMsgClientToGCAcceptInviteToGuildResponse.EResponse
    k_eNoInviteFound: CMsgClientToGCAcceptInviteToGuildResponse.EResponse
    k_eGuildFull: CMsgClientToGCAcceptInviteToGuildResponse.EResponse
    k_eGuildLimit: CMsgClientToGCAcceptInviteToGuildResponse.EResponse
    k_eInvalidInviter: CMsgClientToGCAcceptInviteToGuildResponse.EResponse
    k_eAlreadyInGuild: CMsgClientToGCAcceptInviteToGuildResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCAcceptInviteToGuildResponse.EResponse
    def __init__(
        self, result: CMsgClientToGCAcceptInviteToGuildResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCCancelInviteToGuild(_message.Message):
    __slots__ = ("guild_id", "target_account_id")
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    target_account_id: int
    def __init__(self, guild_id: int | None = ..., target_account_id: int | None = ...) -> None: ...

class CMsgClientToGCCancelInviteToGuildResponse(_message.Message):
    __slots__ = ("result",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCCancelInviteToGuildResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCCancelInviteToGuildResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCCancelInviteToGuildResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCCancelInviteToGuildResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCCancelInviteToGuildResponse.EResponse]
        k_eInvalidGuild: _ClassVar[CMsgClientToGCCancelInviteToGuildResponse.EResponse]
        k_eNoInviteFound: _ClassVar[CMsgClientToGCCancelInviteToGuildResponse.EResponse]
        k_eNoPermissions: _ClassVar[CMsgClientToGCCancelInviteToGuildResponse.EResponse]

    k_eInternalError: CMsgClientToGCCancelInviteToGuildResponse.EResponse
    k_eSuccess: CMsgClientToGCCancelInviteToGuildResponse.EResponse
    k_eTooBusy: CMsgClientToGCCancelInviteToGuildResponse.EResponse
    k_eDisabled: CMsgClientToGCCancelInviteToGuildResponse.EResponse
    k_eTimeout: CMsgClientToGCCancelInviteToGuildResponse.EResponse
    k_eInvalidGuild: CMsgClientToGCCancelInviteToGuildResponse.EResponse
    k_eNoInviteFound: CMsgClientToGCCancelInviteToGuildResponse.EResponse
    k_eNoPermissions: CMsgClientToGCCancelInviteToGuildResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCCancelInviteToGuildResponse.EResponse
    def __init__(
        self, result: CMsgClientToGCCancelInviteToGuildResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCAddGuildRole(_message.Message):
    __slots__ = ("guild_id", "role_name", "role_flags")
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_NAME_FIELD_NUMBER: _ClassVar[int]
    ROLE_FLAGS_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    role_name: str
    role_flags: int
    def __init__(
        self, guild_id: int | None = ..., role_name: str | None = ..., role_flags: int | None = ...
    ) -> None: ...

class CMsgClientToGCAddGuildRoleResponse(_message.Message):
    __slots__ = ("result", "role_id")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCAddGuildRoleResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCAddGuildRoleResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCAddGuildRoleResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCAddGuildRoleResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCAddGuildRoleResponse.EResponse]
        k_eInvalidGuild: _ClassVar[CMsgClientToGCAddGuildRoleResponse.EResponse]
        k_eNameAlreadyUsed: _ClassVar[CMsgClientToGCAddGuildRoleResponse.EResponse]
        k_eNoPermissions: _ClassVar[CMsgClientToGCAddGuildRoleResponse.EResponse]
        k_eInvalidFlags: _ClassVar[CMsgClientToGCAddGuildRoleResponse.EResponse]
        k_eInvalidName: _ClassVar[CMsgClientToGCAddGuildRoleResponse.EResponse]
        k_eAdminViolation: _ClassVar[CMsgClientToGCAddGuildRoleResponse.EResponse]
        k_eTooManyRoles: _ClassVar[CMsgClientToGCAddGuildRoleResponse.EResponse]
        k_eBlocked: _ClassVar[CMsgClientToGCAddGuildRoleResponse.EResponse]

    k_eInternalError: CMsgClientToGCAddGuildRoleResponse.EResponse
    k_eSuccess: CMsgClientToGCAddGuildRoleResponse.EResponse
    k_eTooBusy: CMsgClientToGCAddGuildRoleResponse.EResponse
    k_eDisabled: CMsgClientToGCAddGuildRoleResponse.EResponse
    k_eTimeout: CMsgClientToGCAddGuildRoleResponse.EResponse
    k_eInvalidGuild: CMsgClientToGCAddGuildRoleResponse.EResponse
    k_eNameAlreadyUsed: CMsgClientToGCAddGuildRoleResponse.EResponse
    k_eNoPermissions: CMsgClientToGCAddGuildRoleResponse.EResponse
    k_eInvalidFlags: CMsgClientToGCAddGuildRoleResponse.EResponse
    k_eInvalidName: CMsgClientToGCAddGuildRoleResponse.EResponse
    k_eAdminViolation: CMsgClientToGCAddGuildRoleResponse.EResponse
    k_eTooManyRoles: CMsgClientToGCAddGuildRoleResponse.EResponse
    k_eBlocked: CMsgClientToGCAddGuildRoleResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    ROLE_ID_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCAddGuildRoleResponse.EResponse
    role_id: int
    def __init__(
        self,
        result: CMsgClientToGCAddGuildRoleResponse.EResponse | str | None = ...,
        role_id: int | None = ...,
    ) -> None: ...

class CMsgClientToGCModifyGuildRole(_message.Message):
    __slots__ = ("guild_id", "role_id", "role_name", "role_flags")
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_NAME_FIELD_NUMBER: _ClassVar[int]
    ROLE_FLAGS_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    role_id: int
    role_name: str
    role_flags: int
    def __init__(
        self,
        guild_id: int | None = ...,
        role_id: int | None = ...,
        role_name: str | None = ...,
        role_flags: int | None = ...,
    ) -> None: ...

class CMsgClientToGCModifyGuildRoleResponse(_message.Message):
    __slots__ = ("result",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCModifyGuildRoleResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCModifyGuildRoleResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCModifyGuildRoleResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCModifyGuildRoleResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCModifyGuildRoleResponse.EResponse]
        k_eInvalidGuild: _ClassVar[CMsgClientToGCModifyGuildRoleResponse.EResponse]
        k_eInvalidRole: _ClassVar[CMsgClientToGCModifyGuildRoleResponse.EResponse]
        k_eNameAlreadyUsed: _ClassVar[CMsgClientToGCModifyGuildRoleResponse.EResponse]
        k_eInvalidFlags: _ClassVar[CMsgClientToGCModifyGuildRoleResponse.EResponse]
        k_eInvalidName: _ClassVar[CMsgClientToGCModifyGuildRoleResponse.EResponse]
        k_eNoPermissions: _ClassVar[CMsgClientToGCModifyGuildRoleResponse.EResponse]
        k_eAdminViolation: _ClassVar[CMsgClientToGCModifyGuildRoleResponse.EResponse]
        k_eBlocked: _ClassVar[CMsgClientToGCModifyGuildRoleResponse.EResponse]

    k_eInternalError: CMsgClientToGCModifyGuildRoleResponse.EResponse
    k_eSuccess: CMsgClientToGCModifyGuildRoleResponse.EResponse
    k_eTooBusy: CMsgClientToGCModifyGuildRoleResponse.EResponse
    k_eDisabled: CMsgClientToGCModifyGuildRoleResponse.EResponse
    k_eTimeout: CMsgClientToGCModifyGuildRoleResponse.EResponse
    k_eInvalidGuild: CMsgClientToGCModifyGuildRoleResponse.EResponse
    k_eInvalidRole: CMsgClientToGCModifyGuildRoleResponse.EResponse
    k_eNameAlreadyUsed: CMsgClientToGCModifyGuildRoleResponse.EResponse
    k_eInvalidFlags: CMsgClientToGCModifyGuildRoleResponse.EResponse
    k_eInvalidName: CMsgClientToGCModifyGuildRoleResponse.EResponse
    k_eNoPermissions: CMsgClientToGCModifyGuildRoleResponse.EResponse
    k_eAdminViolation: CMsgClientToGCModifyGuildRoleResponse.EResponse
    k_eBlocked: CMsgClientToGCModifyGuildRoleResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCModifyGuildRoleResponse.EResponse
    def __init__(
        self, result: CMsgClientToGCModifyGuildRoleResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCRemoveGuildRole(_message.Message):
    __slots__ = ("guild_id", "role_id")
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_ID_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    role_id: int
    def __init__(self, guild_id: int | None = ..., role_id: int | None = ...) -> None: ...

class CMsgClientToGCRemoveGuildRoleResponse(_message.Message):
    __slots__ = ("result",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCRemoveGuildRoleResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCRemoveGuildRoleResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCRemoveGuildRoleResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCRemoveGuildRoleResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCRemoveGuildRoleResponse.EResponse]
        k_eInvalidGuild: _ClassVar[CMsgClientToGCRemoveGuildRoleResponse.EResponse]
        k_eInvalidRole: _ClassVar[CMsgClientToGCRemoveGuildRoleResponse.EResponse]
        k_eRoleNotEmpty: _ClassVar[CMsgClientToGCRemoveGuildRoleResponse.EResponse]
        k_eNoPermissions: _ClassVar[CMsgClientToGCRemoveGuildRoleResponse.EResponse]
        k_eAdminViolation: _ClassVar[CMsgClientToGCRemoveGuildRoleResponse.EResponse]
        k_eCantRemoveDefaultRole: _ClassVar[CMsgClientToGCRemoveGuildRoleResponse.EResponse]

    k_eInternalError: CMsgClientToGCRemoveGuildRoleResponse.EResponse
    k_eSuccess: CMsgClientToGCRemoveGuildRoleResponse.EResponse
    k_eTooBusy: CMsgClientToGCRemoveGuildRoleResponse.EResponse
    k_eDisabled: CMsgClientToGCRemoveGuildRoleResponse.EResponse
    k_eTimeout: CMsgClientToGCRemoveGuildRoleResponse.EResponse
    k_eInvalidGuild: CMsgClientToGCRemoveGuildRoleResponse.EResponse
    k_eInvalidRole: CMsgClientToGCRemoveGuildRoleResponse.EResponse
    k_eRoleNotEmpty: CMsgClientToGCRemoveGuildRoleResponse.EResponse
    k_eNoPermissions: CMsgClientToGCRemoveGuildRoleResponse.EResponse
    k_eAdminViolation: CMsgClientToGCRemoveGuildRoleResponse.EResponse
    k_eCantRemoveDefaultRole: CMsgClientToGCRemoveGuildRoleResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCRemoveGuildRoleResponse.EResponse
    def __init__(
        self, result: CMsgClientToGCRemoveGuildRoleResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCSetGuildRoleOrder(_message.Message):
    __slots__ = ("guild_id", "requested_role_ids", "previous_role_ids")
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_ROLE_IDS_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_ROLE_IDS_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    requested_role_ids: _containers.RepeatedScalarFieldContainer[int]
    previous_role_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        guild_id: int | None = ...,
        requested_role_ids: _Iterable[int] | None = ...,
        previous_role_ids: _Iterable[int] | None = ...,
    ) -> None: ...

class CMsgClientToGCSetGuildRoleOrderResponse(_message.Message):
    __slots__ = ("result", "confirmed_role_ids")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCSetGuildRoleOrderResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCSetGuildRoleOrderResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCSetGuildRoleOrderResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCSetGuildRoleOrderResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCSetGuildRoleOrderResponse.EResponse]
        k_eInvalidGuild: _ClassVar[CMsgClientToGCSetGuildRoleOrderResponse.EResponse]
        k_eInvalidRole: _ClassVar[CMsgClientToGCSetGuildRoleOrderResponse.EResponse]
        k_eInvalidOrder: _ClassVar[CMsgClientToGCSetGuildRoleOrderResponse.EResponse]
        k_eNoPermissions: _ClassVar[CMsgClientToGCSetGuildRoleOrderResponse.EResponse]
        k_eAdminViolation: _ClassVar[CMsgClientToGCSetGuildRoleOrderResponse.EResponse]

    k_eInternalError: CMsgClientToGCSetGuildRoleOrderResponse.EResponse
    k_eSuccess: CMsgClientToGCSetGuildRoleOrderResponse.EResponse
    k_eTooBusy: CMsgClientToGCSetGuildRoleOrderResponse.EResponse
    k_eDisabled: CMsgClientToGCSetGuildRoleOrderResponse.EResponse
    k_eTimeout: CMsgClientToGCSetGuildRoleOrderResponse.EResponse
    k_eInvalidGuild: CMsgClientToGCSetGuildRoleOrderResponse.EResponse
    k_eInvalidRole: CMsgClientToGCSetGuildRoleOrderResponse.EResponse
    k_eInvalidOrder: CMsgClientToGCSetGuildRoleOrderResponse.EResponse
    k_eNoPermissions: CMsgClientToGCSetGuildRoleOrderResponse.EResponse
    k_eAdminViolation: CMsgClientToGCSetGuildRoleOrderResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    CONFIRMED_ROLE_IDS_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCSetGuildRoleOrderResponse.EResponse
    confirmed_role_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        result: CMsgClientToGCSetGuildRoleOrderResponse.EResponse | str | None = ...,
        confirmed_role_ids: _Iterable[int] | None = ...,
    ) -> None: ...

class CMsgClientToGCGuildFeedRequest(_message.Message):
    __slots__ = ("guild_id", "last_seen_id")
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_SEEN_ID_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    last_seen_id: int
    def __init__(self, guild_id: int | None = ..., last_seen_id: int | None = ...) -> None: ...

class CMsgClientToGCRequestGuildFeedResponse(_message.Message):
    __slots__ = ("result", "guild_id", "feed_events")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCRequestGuildFeedResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCRequestGuildFeedResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCRequestGuildFeedResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCRequestGuildFeedResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCRequestGuildFeedResponse.EResponse]
        k_eInvalidGuild: _ClassVar[CMsgClientToGCRequestGuildFeedResponse.EResponse]
        k_eNoPermissions: _ClassVar[CMsgClientToGCRequestGuildFeedResponse.EResponse]

    k_eInternalError: CMsgClientToGCRequestGuildFeedResponse.EResponse
    k_eSuccess: CMsgClientToGCRequestGuildFeedResponse.EResponse
    k_eTooBusy: CMsgClientToGCRequestGuildFeedResponse.EResponse
    k_eDisabled: CMsgClientToGCRequestGuildFeedResponse.EResponse
    k_eTimeout: CMsgClientToGCRequestGuildFeedResponse.EResponse
    k_eInvalidGuild: CMsgClientToGCRequestGuildFeedResponse.EResponse
    k_eNoPermissions: CMsgClientToGCRequestGuildFeedResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    FEED_EVENTS_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCRequestGuildFeedResponse.EResponse
    guild_id: int
    feed_events: _containers.RepeatedCompositeFieldContainer[CMsgGuildFeedEvent]
    def __init__(
        self,
        result: CMsgClientToGCRequestGuildFeedResponse.EResponse | str | None = ...,
        guild_id: int | None = ...,
        feed_events: _Iterable[CMsgGuildFeedEvent | _Mapping] | None = ...,
    ) -> None: ...

class CMsgGCToClientGuildFeedUpdated(_message.Message):
    __slots__ = ("guild_id",)
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    def __init__(self, guild_id: int | None = ...) -> None: ...

class CMsgClientToGCAddPlayerToGuildChat(_message.Message):
    __slots__ = ("guild_id",)
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    def __init__(self, guild_id: int | None = ...) -> None: ...

class CMsgClientToGCAddPlayerToGuildChatResponse(_message.Message):
    __slots__ = ("result",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCAddPlayerToGuildChatResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCAddPlayerToGuildChatResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCAddPlayerToGuildChatResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCAddPlayerToGuildChatResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCAddPlayerToGuildChatResponse.EResponse]
        k_eInvalidGuild: _ClassVar[CMsgClientToGCAddPlayerToGuildChatResponse.EResponse]
        k_eNotMember: _ClassVar[CMsgClientToGCAddPlayerToGuildChatResponse.EResponse]
        k_eSteamChatNotEnabled: _ClassVar[CMsgClientToGCAddPlayerToGuildChatResponse.EResponse]

    k_eInternalError: CMsgClientToGCAddPlayerToGuildChatResponse.EResponse
    k_eSuccess: CMsgClientToGCAddPlayerToGuildChatResponse.EResponse
    k_eTooBusy: CMsgClientToGCAddPlayerToGuildChatResponse.EResponse
    k_eDisabled: CMsgClientToGCAddPlayerToGuildChatResponse.EResponse
    k_eTimeout: CMsgClientToGCAddPlayerToGuildChatResponse.EResponse
    k_eInvalidGuild: CMsgClientToGCAddPlayerToGuildChatResponse.EResponse
    k_eNotMember: CMsgClientToGCAddPlayerToGuildChatResponse.EResponse
    k_eSteamChatNotEnabled: CMsgClientToGCAddPlayerToGuildChatResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCAddPlayerToGuildChatResponse.EResponse
    def __init__(
        self, result: CMsgClientToGCAddPlayerToGuildChatResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgFindGuildByTagResponse(_message.Message):
    __slots__ = ("result", "guild_id", "guild_summary")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgFindGuildByTagResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgFindGuildByTagResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgFindGuildByTagResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgFindGuildByTagResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgFindGuildByTagResponse.EResponse]
        k_eInvalidTag: _ClassVar[CMsgFindGuildByTagResponse.EResponse]
        k_eGuildNotFound: _ClassVar[CMsgFindGuildByTagResponse.EResponse]

    k_eInternalError: CMsgFindGuildByTagResponse.EResponse
    k_eSuccess: CMsgFindGuildByTagResponse.EResponse
    k_eTooBusy: CMsgFindGuildByTagResponse.EResponse
    k_eDisabled: CMsgFindGuildByTagResponse.EResponse
    k_eTimeout: CMsgFindGuildByTagResponse.EResponse
    k_eInvalidTag: CMsgFindGuildByTagResponse.EResponse
    k_eGuildNotFound: CMsgFindGuildByTagResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    GUILD_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    result: CMsgFindGuildByTagResponse.EResponse
    guild_id: int
    guild_summary: CMsgGuildSummary
    def __init__(
        self,
        result: CMsgFindGuildByTagResponse.EResponse | str | None = ...,
        guild_id: int | None = ...,
        guild_summary: CMsgGuildSummary | _Mapping | None = ...,
    ) -> None: ...

class CMsgSearchForOpenGuildsResponse(_message.Message):
    __slots__ = ("result", "search_results", "use_whitelist")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgSearchForOpenGuildsResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgSearchForOpenGuildsResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgSearchForOpenGuildsResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgSearchForOpenGuildsResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgSearchForOpenGuildsResponse.EResponse]

    k_eInternalError: CMsgSearchForOpenGuildsResponse.EResponse
    k_eSuccess: CMsgSearchForOpenGuildsResponse.EResponse
    k_eTooBusy: CMsgSearchForOpenGuildsResponse.EResponse
    k_eDisabled: CMsgSearchForOpenGuildsResponse.EResponse
    k_eTimeout: CMsgSearchForOpenGuildsResponse.EResponse
    class SearchResult(_message.Message):
        __slots__ = ("guild_id", "guild_summary")
        GUILD_ID_FIELD_NUMBER: _ClassVar[int]
        GUILD_SUMMARY_FIELD_NUMBER: _ClassVar[int]
        guild_id: int
        guild_summary: CMsgGuildSummary
        def __init__(
            self,
            guild_id: int | None = ...,
            guild_summary: CMsgGuildSummary | _Mapping | None = ...,
        ) -> None: ...

    RESULT_FIELD_NUMBER: _ClassVar[int]
    SEARCH_RESULTS_FIELD_NUMBER: _ClassVar[int]
    USE_WHITELIST_FIELD_NUMBER: _ClassVar[int]
    result: CMsgSearchForOpenGuildsResponse.EResponse
    search_results: _containers.RepeatedCompositeFieldContainer[
        CMsgSearchForOpenGuildsResponse.SearchResult
    ]
    use_whitelist: bool
    def __init__(
        self,
        result: CMsgSearchForOpenGuildsResponse.EResponse | str | None = ...,
        search_results: _Iterable[CMsgSearchForOpenGuildsResponse.SearchResult | _Mapping]
        | None = ...,
        use_whitelist: bool = ...,
    ) -> None: ...

class CMsgClientToGCReportGuildContent(_message.Message):
    __slots__ = ("guild_id", "guild_content_flags")
    class EContentFlags(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eNone: _ClassVar[CMsgClientToGCReportGuildContent.EContentFlags]
        k_eInappropriateName: _ClassVar[CMsgClientToGCReportGuildContent.EContentFlags]
        k_eInappropriateTag: _ClassVar[CMsgClientToGCReportGuildContent.EContentFlags]
        k_eInappropriateLogo: _ClassVar[CMsgClientToGCReportGuildContent.EContentFlags]
        k_eValidFlags: _ClassVar[CMsgClientToGCReportGuildContent.EContentFlags]

    k_eNone: CMsgClientToGCReportGuildContent.EContentFlags
    k_eInappropriateName: CMsgClientToGCReportGuildContent.EContentFlags
    k_eInappropriateTag: CMsgClientToGCReportGuildContent.EContentFlags
    k_eInappropriateLogo: CMsgClientToGCReportGuildContent.EContentFlags
    k_eValidFlags: CMsgClientToGCReportGuildContent.EContentFlags
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    GUILD_CONTENT_FLAGS_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    guild_content_flags: int
    def __init__(
        self, guild_id: int | None = ..., guild_content_flags: int | None = ...
    ) -> None: ...

class CMsgClientToGCReportGuildContentResponse(_message.Message):
    __slots__ = ("result",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCReportGuildContentResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCReportGuildContentResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCReportGuildContentResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCReportGuildContentResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCReportGuildContentResponse.EResponse]
        k_eGuildNotFound: _ClassVar[CMsgClientToGCReportGuildContentResponse.EResponse]
        k_eFlagsInvalid: _ClassVar[CMsgClientToGCReportGuildContentResponse.EResponse]

    k_eInternalError: CMsgClientToGCReportGuildContentResponse.EResponse
    k_eSuccess: CMsgClientToGCReportGuildContentResponse.EResponse
    k_eTooBusy: CMsgClientToGCReportGuildContentResponse.EResponse
    k_eDisabled: CMsgClientToGCReportGuildContentResponse.EResponse
    k_eTimeout: CMsgClientToGCReportGuildContentResponse.EResponse
    k_eGuildNotFound: CMsgClientToGCReportGuildContentResponse.EResponse
    k_eFlagsInvalid: CMsgClientToGCReportGuildContentResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCReportGuildContentResponse.EResponse
    def __init__(
        self, result: CMsgClientToGCReportGuildContentResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCRequestAccountGuildPersonaInfo(_message.Message):
    __slots__ = ("account_id",)
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    def __init__(self, account_id: int | None = ...) -> None: ...

class CMsgClientToGCRequestAccountGuildPersonaInfoResponse(_message.Message):
    __slots__ = ("result", "persona_info")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCRequestAccountGuildPersonaInfoResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCRequestAccountGuildPersonaInfoResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCRequestAccountGuildPersonaInfoResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCRequestAccountGuildPersonaInfoResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCRequestAccountGuildPersonaInfoResponse.EResponse]
        k_eInvalidAccount: _ClassVar[CMsgClientToGCRequestAccountGuildPersonaInfoResponse.EResponse]

    k_eInternalError: CMsgClientToGCRequestAccountGuildPersonaInfoResponse.EResponse
    k_eSuccess: CMsgClientToGCRequestAccountGuildPersonaInfoResponse.EResponse
    k_eTooBusy: CMsgClientToGCRequestAccountGuildPersonaInfoResponse.EResponse
    k_eDisabled: CMsgClientToGCRequestAccountGuildPersonaInfoResponse.EResponse
    k_eTimeout: CMsgClientToGCRequestAccountGuildPersonaInfoResponse.EResponse
    k_eInvalidAccount: CMsgClientToGCRequestAccountGuildPersonaInfoResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    PERSONA_INFO_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCRequestAccountGuildPersonaInfoResponse.EResponse
    persona_info: CMsgAccountGuildsPersonaInfo
    def __init__(
        self,
        result: CMsgClientToGCRequestAccountGuildPersonaInfoResponse.EResponse | str | None = ...,
        persona_info: CMsgAccountGuildsPersonaInfo | _Mapping | None = ...,
    ) -> None: ...

class CMsgClientToGCRequestAccountGuildPersonaInfoBatch(_message.Message):
    __slots__ = ("account_ids",)
    ACCOUNT_IDS_FIELD_NUMBER: _ClassVar[int]
    account_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, account_ids: _Iterable[int] | None = ...) -> None: ...

class CMsgClientToGCRequestAccountGuildPersonaInfoBatchResponse(_message.Message):
    __slots__ = ("result", "persona_infos")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[
            CMsgClientToGCRequestAccountGuildPersonaInfoBatchResponse.EResponse
        ]
        k_eSuccess: _ClassVar[CMsgClientToGCRequestAccountGuildPersonaInfoBatchResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCRequestAccountGuildPersonaInfoBatchResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCRequestAccountGuildPersonaInfoBatchResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCRequestAccountGuildPersonaInfoBatchResponse.EResponse]
        k_eInvalidRequest: _ClassVar[
            CMsgClientToGCRequestAccountGuildPersonaInfoBatchResponse.EResponse
        ]

    k_eInternalError: CMsgClientToGCRequestAccountGuildPersonaInfoBatchResponse.EResponse
    k_eSuccess: CMsgClientToGCRequestAccountGuildPersonaInfoBatchResponse.EResponse
    k_eTooBusy: CMsgClientToGCRequestAccountGuildPersonaInfoBatchResponse.EResponse
    k_eDisabled: CMsgClientToGCRequestAccountGuildPersonaInfoBatchResponse.EResponse
    k_eTimeout: CMsgClientToGCRequestAccountGuildPersonaInfoBatchResponse.EResponse
    k_eInvalidRequest: CMsgClientToGCRequestAccountGuildPersonaInfoBatchResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    PERSONA_INFOS_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCRequestAccountGuildPersonaInfoBatchResponse.EResponse
    persona_infos: _containers.RepeatedCompositeFieldContainer[CMsgAccountGuildsPersonaInfo]
    def __init__(
        self,
        result: CMsgClientToGCRequestAccountGuildPersonaInfoBatchResponse.EResponse
        | str
        | None = ...,
        persona_infos: _Iterable[CMsgAccountGuildsPersonaInfo | _Mapping] | None = ...,
    ) -> None: ...
