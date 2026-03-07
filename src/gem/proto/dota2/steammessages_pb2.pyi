from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class EGCPlatform(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eGCPlatform_None: _ClassVar[EGCPlatform]
    k_eGCPlatform_PC: _ClassVar[EGCPlatform]
    k_eGCPlatform_Mac: _ClassVar[EGCPlatform]
    k_eGCPlatform_Linux: _ClassVar[EGCPlatform]
    k_eGCPlatform_Android: _ClassVar[EGCPlatform]
    k_eGCPlatform_iOS: _ClassVar[EGCPlatform]

class GCProtoBufMsgSrc(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GCProtoBufMsgSrc_Unspecified: _ClassVar[GCProtoBufMsgSrc]
    GCProtoBufMsgSrc_FromSystem: _ClassVar[GCProtoBufMsgSrc]
    GCProtoBufMsgSrc_FromSteamID: _ClassVar[GCProtoBufMsgSrc]
    GCProtoBufMsgSrc_FromGC: _ClassVar[GCProtoBufMsgSrc]
    GCProtoBufMsgSrc_ReplySystem: _ClassVar[GCProtoBufMsgSrc]
    GCProtoBufMsgSrc_SpoofedSteamID: _ClassVar[GCProtoBufMsgSrc]

k_eGCPlatform_None: EGCPlatform
k_eGCPlatform_PC: EGCPlatform
k_eGCPlatform_Mac: EGCPlatform
k_eGCPlatform_Linux: EGCPlatform
k_eGCPlatform_Android: EGCPlatform
k_eGCPlatform_iOS: EGCPlatform
GCProtoBufMsgSrc_Unspecified: GCProtoBufMsgSrc
GCProtoBufMsgSrc_FromSystem: GCProtoBufMsgSrc
GCProtoBufMsgSrc_FromSteamID: GCProtoBufMsgSrc
GCProtoBufMsgSrc_FromGC: GCProtoBufMsgSrc
GCProtoBufMsgSrc_ReplySystem: GCProtoBufMsgSrc
GCProtoBufMsgSrc_SpoofedSteamID: GCProtoBufMsgSrc
KEY_FIELD_FIELD_NUMBER: _ClassVar[int]
key_field: _descriptor.FieldDescriptor
MSGPOOL_SOFT_LIMIT_FIELD_NUMBER: _ClassVar[int]
msgpool_soft_limit: _descriptor.FieldDescriptor
MSGPOOL_HARD_LIMIT_FIELD_NUMBER: _ClassVar[int]
msgpool_hard_limit: _descriptor.FieldDescriptor

class CMsgProtoBufHeader(_message.Message):
    __slots__ = (
        "client_steam_id",
        "client_session_id",
        "source_app_id",
        "job_id_source",
        "job_id_target",
        "target_job_name",
        "eresult",
        "error_message",
        "gc_msg_src",
        "gc_dir_index_source",
    )
    CLIENT_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_APP_ID_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_SOURCE_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_TARGET_FIELD_NUMBER: _ClassVar[int]
    TARGET_JOB_NAME_FIELD_NUMBER: _ClassVar[int]
    ERESULT_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    GC_MSG_SRC_FIELD_NUMBER: _ClassVar[int]
    GC_DIR_INDEX_SOURCE_FIELD_NUMBER: _ClassVar[int]
    client_steam_id: int
    client_session_id: int
    source_app_id: int
    job_id_source: int
    job_id_target: int
    target_job_name: str
    eresult: int
    error_message: str
    gc_msg_src: GCProtoBufMsgSrc
    gc_dir_index_source: int
    def __init__(
        self,
        client_steam_id: int | None = ...,
        client_session_id: int | None = ...,
        source_app_id: int | None = ...,
        job_id_source: int | None = ...,
        job_id_target: int | None = ...,
        target_job_name: str | None = ...,
        eresult: int | None = ...,
        error_message: str | None = ...,
        gc_msg_src: GCProtoBufMsgSrc | str | None = ...,
        gc_dir_index_source: int | None = ...,
    ) -> None: ...

class CGCSystemMsg_GetAccountDetails(_message.Message):
    __slots__ = ("steamid", "appid")
    STEAMID_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    steamid: int
    appid: int
    def __init__(self, steamid: int | None = ..., appid: int | None = ...) -> None: ...

class CGCSystemMsg_GetAccountDetails_Response(_message.Message):
    __slots__ = (
        "eresult_deprecated",
        "account_name",
        "persona_name",
        "is_profile_created",
        "is_profile_public",
        "is_inventory_public",
        "is_vac_banned",
        "is_cyber_cafe",
        "is_school_account",
        "is_limited",
        "is_subscribed",
        "package",
        "is_free_trial_account",
        "free_trial_expiration",
        "is_low_violence",
        "is_account_locked_down",
        "is_community_banned",
        "is_trade_banned",
        "trade_ban_expiration",
        "accountid",
        "suspension_end_time",
        "currency",
        "steam_level",
        "friend_count",
        "account_creation_time",
        "is_steamguard_enabled",
        "is_phone_verified",
        "is_two_factor_auth_enabled",
        "two_factor_enabled_time",
        "phone_verification_time",
        "phone_id",
        "is_phone_identifying",
        "rt_identity_linked",
        "rt_birth_date",
        "txn_country_code",
        "has_accepted_china_ssa",
        "is_banned_steam_china",
    )
    ERESULT_DEPRECATED_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_NAME_FIELD_NUMBER: _ClassVar[int]
    PERSONA_NAME_FIELD_NUMBER: _ClassVar[int]
    IS_PROFILE_CREATED_FIELD_NUMBER: _ClassVar[int]
    IS_PROFILE_PUBLIC_FIELD_NUMBER: _ClassVar[int]
    IS_INVENTORY_PUBLIC_FIELD_NUMBER: _ClassVar[int]
    IS_VAC_BANNED_FIELD_NUMBER: _ClassVar[int]
    IS_CYBER_CAFE_FIELD_NUMBER: _ClassVar[int]
    IS_SCHOOL_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    IS_LIMITED_FIELD_NUMBER: _ClassVar[int]
    IS_SUBSCRIBED_FIELD_NUMBER: _ClassVar[int]
    PACKAGE_FIELD_NUMBER: _ClassVar[int]
    IS_FREE_TRIAL_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    FREE_TRIAL_EXPIRATION_FIELD_NUMBER: _ClassVar[int]
    IS_LOW_VIOLENCE_FIELD_NUMBER: _ClassVar[int]
    IS_ACCOUNT_LOCKED_DOWN_FIELD_NUMBER: _ClassVar[int]
    IS_COMMUNITY_BANNED_FIELD_NUMBER: _ClassVar[int]
    IS_TRADE_BANNED_FIELD_NUMBER: _ClassVar[int]
    TRADE_BAN_EXPIRATION_FIELD_NUMBER: _ClassVar[int]
    ACCOUNTID_FIELD_NUMBER: _ClassVar[int]
    SUSPENSION_END_TIME_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    STEAM_LEVEL_FIELD_NUMBER: _ClassVar[int]
    FRIEND_COUNT_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_CREATION_TIME_FIELD_NUMBER: _ClassVar[int]
    IS_STEAMGUARD_ENABLED_FIELD_NUMBER: _ClassVar[int]
    IS_PHONE_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    IS_TWO_FACTOR_AUTH_ENABLED_FIELD_NUMBER: _ClassVar[int]
    TWO_FACTOR_ENABLED_TIME_FIELD_NUMBER: _ClassVar[int]
    PHONE_VERIFICATION_TIME_FIELD_NUMBER: _ClassVar[int]
    PHONE_ID_FIELD_NUMBER: _ClassVar[int]
    IS_PHONE_IDENTIFYING_FIELD_NUMBER: _ClassVar[int]
    RT_IDENTITY_LINKED_FIELD_NUMBER: _ClassVar[int]
    RT_BIRTH_DATE_FIELD_NUMBER: _ClassVar[int]
    TXN_COUNTRY_CODE_FIELD_NUMBER: _ClassVar[int]
    HAS_ACCEPTED_CHINA_SSA_FIELD_NUMBER: _ClassVar[int]
    IS_BANNED_STEAM_CHINA_FIELD_NUMBER: _ClassVar[int]
    eresult_deprecated: int
    account_name: str
    persona_name: str
    is_profile_created: bool
    is_profile_public: bool
    is_inventory_public: bool
    is_vac_banned: bool
    is_cyber_cafe: bool
    is_school_account: bool
    is_limited: bool
    is_subscribed: bool
    package: int
    is_free_trial_account: bool
    free_trial_expiration: int
    is_low_violence: bool
    is_account_locked_down: bool
    is_community_banned: bool
    is_trade_banned: bool
    trade_ban_expiration: int
    accountid: int
    suspension_end_time: int
    currency: str
    steam_level: int
    friend_count: int
    account_creation_time: int
    is_steamguard_enabled: bool
    is_phone_verified: bool
    is_two_factor_auth_enabled: bool
    two_factor_enabled_time: int
    phone_verification_time: int
    phone_id: int
    is_phone_identifying: bool
    rt_identity_linked: int
    rt_birth_date: int
    txn_country_code: str
    has_accepted_china_ssa: bool
    is_banned_steam_china: bool
    def __init__(
        self,
        eresult_deprecated: int | None = ...,
        account_name: str | None = ...,
        persona_name: str | None = ...,
        is_profile_created: bool = ...,
        is_profile_public: bool = ...,
        is_inventory_public: bool = ...,
        is_vac_banned: bool = ...,
        is_cyber_cafe: bool = ...,
        is_school_account: bool = ...,
        is_limited: bool = ...,
        is_subscribed: bool = ...,
        package: int | None = ...,
        is_free_trial_account: bool = ...,
        free_trial_expiration: int | None = ...,
        is_low_violence: bool = ...,
        is_account_locked_down: bool = ...,
        is_community_banned: bool = ...,
        is_trade_banned: bool = ...,
        trade_ban_expiration: int | None = ...,
        accountid: int | None = ...,
        suspension_end_time: int | None = ...,
        currency: str | None = ...,
        steam_level: int | None = ...,
        friend_count: int | None = ...,
        account_creation_time: int | None = ...,
        is_steamguard_enabled: bool = ...,
        is_phone_verified: bool = ...,
        is_two_factor_auth_enabled: bool = ...,
        two_factor_enabled_time: int | None = ...,
        phone_verification_time: int | None = ...,
        phone_id: int | None = ...,
        is_phone_identifying: bool = ...,
        rt_identity_linked: int | None = ...,
        rt_birth_date: int | None = ...,
        txn_country_code: str | None = ...,
        has_accepted_china_ssa: bool = ...,
        is_banned_steam_china: bool = ...,
    ) -> None: ...

class CIPLocationInfo(_message.Message):
    __slots__ = ("ip", "latitude", "longitude", "country", "state", "city")
    IP_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    ip: int
    latitude: float
    longitude: float
    country: str
    state: str
    city: str
    def __init__(
        self,
        ip: int | None = ...,
        latitude: float | None = ...,
        longitude: float | None = ...,
        country: str | None = ...,
        state: str | None = ...,
        city: str | None = ...,
    ) -> None: ...

class CGCMsgGetIPLocationResponse(_message.Message):
    __slots__ = ("infos",)
    INFOS_FIELD_NUMBER: _ClassVar[int]
    infos: _containers.RepeatedCompositeFieldContainer[CIPLocationInfo]
    def __init__(self, infos: _Iterable[CIPLocationInfo | _Mapping] | None = ...) -> None: ...
