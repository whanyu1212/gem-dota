from . import steammessages_pb2 as _steammessages_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CMsgWebAPIKey(_message.Message):
    __slots__ = ("status", "account_id", "publisher_group_id", "key_id", "domain")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    PUBLISHER_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    status: int
    account_id: int
    publisher_group_id: int
    key_id: int
    domain: str
    def __init__(self, status: _Optional[int] = ..., account_id: _Optional[int] = ..., publisher_group_id: _Optional[int] = ..., key_id: _Optional[int] = ..., domain: _Optional[str] = ...) -> None: ...

class CMsgHttpRequest(_message.Message):
    __slots__ = ("request_method", "hostname", "url", "headers", "get_params", "post_params", "body", "absolute_timeout", "use_https")
    class RequestHeader(_message.Message):
        __slots__ = ("name", "value")
        NAME_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        name: str
        value: str
        def __init__(self, name: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class QueryParam(_message.Message):
        __slots__ = ("name", "value")
        NAME_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        name: str
        value: bytes
        def __init__(self, name: _Optional[str] = ..., value: _Optional[bytes] = ...) -> None: ...
    REQUEST_METHOD_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    GET_PARAMS_FIELD_NUMBER: _ClassVar[int]
    POST_PARAMS_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    USE_HTTPS_FIELD_NUMBER: _ClassVar[int]
    request_method: int
    hostname: str
    url: str
    headers: _containers.RepeatedCompositeFieldContainer[CMsgHttpRequest.RequestHeader]
    get_params: _containers.RepeatedCompositeFieldContainer[CMsgHttpRequest.QueryParam]
    post_params: _containers.RepeatedCompositeFieldContainer[CMsgHttpRequest.QueryParam]
    body: bytes
    absolute_timeout: int
    use_https: bool
    def __init__(self, request_method: _Optional[int] = ..., hostname: _Optional[str] = ..., url: _Optional[str] = ..., headers: _Optional[_Iterable[_Union[CMsgHttpRequest.RequestHeader, _Mapping]]] = ..., get_params: _Optional[_Iterable[_Union[CMsgHttpRequest.QueryParam, _Mapping]]] = ..., post_params: _Optional[_Iterable[_Union[CMsgHttpRequest.QueryParam, _Mapping]]] = ..., body: _Optional[bytes] = ..., absolute_timeout: _Optional[int] = ..., use_https: bool = ...) -> None: ...

class CMsgWebAPIRequest(_message.Message):
    __slots__ = ("interface_name", "method_name", "version", "api_key", "request", "routing_app_id")
    INTERFACE_NAME_FIELD_NUMBER: _ClassVar[int]
    METHOD_NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    ROUTING_APP_ID_FIELD_NUMBER: _ClassVar[int]
    interface_name: str
    method_name: str
    version: int
    api_key: CMsgWebAPIKey
    request: CMsgHttpRequest
    routing_app_id: int
    def __init__(self, interface_name: _Optional[str] = ..., method_name: _Optional[str] = ..., version: _Optional[int] = ..., api_key: _Optional[_Union[CMsgWebAPIKey, _Mapping]] = ..., request: _Optional[_Union[CMsgHttpRequest, _Mapping]] = ..., routing_app_id: _Optional[int] = ...) -> None: ...

class CMsgHttpResponse(_message.Message):
    __slots__ = ("status_code", "headers", "body")
    class ResponseHeader(_message.Message):
        __slots__ = ("name", "value")
        NAME_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        name: str
        value: str
        def __init__(self, name: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    headers: _containers.RepeatedCompositeFieldContainer[CMsgHttpResponse.ResponseHeader]
    body: bytes
    def __init__(self, status_code: _Optional[int] = ..., headers: _Optional[_Iterable[_Union[CMsgHttpResponse.ResponseHeader, _Mapping]]] = ..., body: _Optional[bytes] = ...) -> None: ...

class CMsgAMFindAccounts(_message.Message):
    __slots__ = ("search_type", "search_string")
    SEARCH_TYPE_FIELD_NUMBER: _ClassVar[int]
    SEARCH_STRING_FIELD_NUMBER: _ClassVar[int]
    search_type: int
    search_string: str
    def __init__(self, search_type: _Optional[int] = ..., search_string: _Optional[str] = ...) -> None: ...

class CMsgAMFindAccountsResponse(_message.Message):
    __slots__ = ("steam_id",)
    STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    steam_id: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, steam_id: _Optional[_Iterable[int]] = ...) -> None: ...

class CMsgNotifyWatchdog(_message.Message):
    __slots__ = ("source", "alert_type", "critical", "time", "appid", "text", "recipient")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    ALERT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CRITICAL_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_FIELD_NUMBER: _ClassVar[int]
    source: int
    alert_type: int
    critical: bool
    time: int
    appid: int
    text: str
    recipient: str
    def __init__(self, source: _Optional[int] = ..., alert_type: _Optional[int] = ..., critical: bool = ..., time: _Optional[int] = ..., appid: _Optional[int] = ..., text: _Optional[str] = ..., recipient: _Optional[str] = ...) -> None: ...

class CMsgAMGetLicenses(_message.Message):
    __slots__ = ("steamid",)
    STEAMID_FIELD_NUMBER: _ClassVar[int]
    steamid: int
    def __init__(self, steamid: _Optional[int] = ...) -> None: ...

class CMsgPackageLicense(_message.Message):
    __slots__ = ("package_id", "time_created", "owner_id")
    PACKAGE_ID_FIELD_NUMBER: _ClassVar[int]
    TIME_CREATED_FIELD_NUMBER: _ClassVar[int]
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    package_id: int
    time_created: int
    owner_id: int
    def __init__(self, package_id: _Optional[int] = ..., time_created: _Optional[int] = ..., owner_id: _Optional[int] = ...) -> None: ...

class CMsgAMGetLicensesResponse(_message.Message):
    __slots__ = ("license", "result")
    LICENSE_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    license: _containers.RepeatedCompositeFieldContainer[CMsgPackageLicense]
    result: int
    def __init__(self, license: _Optional[_Iterable[_Union[CMsgPackageLicense, _Mapping]]] = ..., result: _Optional[int] = ...) -> None: ...

class CMsgGCGetCommandList(_message.Message):
    __slots__ = ("app_id", "command_prefix")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    COMMAND_PREFIX_FIELD_NUMBER: _ClassVar[int]
    app_id: int
    command_prefix: str
    def __init__(self, app_id: _Optional[int] = ..., command_prefix: _Optional[str] = ...) -> None: ...

class CMsgGCGetCommandListResponse(_message.Message):
    __slots__ = ("command_name",)
    COMMAND_NAME_FIELD_NUMBER: _ClassVar[int]
    command_name: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, command_name: _Optional[_Iterable[str]] = ...) -> None: ...

class CGCMsgMemCachedGet(_message.Message):
    __slots__ = ("keys",)
    KEYS_FIELD_NUMBER: _ClassVar[int]
    keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, keys: _Optional[_Iterable[str]] = ...) -> None: ...

class CGCMsgMemCachedGetResponse(_message.Message):
    __slots__ = ("values",)
    class ValueTag(_message.Message):
        __slots__ = ("found", "value")
        FOUND_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        found: bool
        value: bytes
        def __init__(self, found: bool = ..., value: _Optional[bytes] = ...) -> None: ...
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedCompositeFieldContainer[CGCMsgMemCachedGetResponse.ValueTag]
    def __init__(self, values: _Optional[_Iterable[_Union[CGCMsgMemCachedGetResponse.ValueTag, _Mapping]]] = ...) -> None: ...

class CGCMsgMemCachedSet(_message.Message):
    __slots__ = ("keys",)
    class KeyPair(_message.Message):
        __slots__ = ("name", "value")
        NAME_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        name: str
        value: bytes
        def __init__(self, name: _Optional[str] = ..., value: _Optional[bytes] = ...) -> None: ...
    KEYS_FIELD_NUMBER: _ClassVar[int]
    keys: _containers.RepeatedCompositeFieldContainer[CGCMsgMemCachedSet.KeyPair]
    def __init__(self, keys: _Optional[_Iterable[_Union[CGCMsgMemCachedSet.KeyPair, _Mapping]]] = ...) -> None: ...

class CGCMsgMemCachedDelete(_message.Message):
    __slots__ = ("keys",)
    KEYS_FIELD_NUMBER: _ClassVar[int]
    keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, keys: _Optional[_Iterable[str]] = ...) -> None: ...

class CGCMsgMemCachedStats(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CGCMsgMemCachedStatsResponse(_message.Message):
    __slots__ = ("curr_connections", "cmd_get", "cmd_set", "cmd_flush", "get_hits", "get_misses", "delete_hits", "delete_misses", "bytes_read", "bytes_written", "limit_maxbytes", "curr_items", "evictions", "bytes")
    CURR_CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    CMD_GET_FIELD_NUMBER: _ClassVar[int]
    CMD_SET_FIELD_NUMBER: _ClassVar[int]
    CMD_FLUSH_FIELD_NUMBER: _ClassVar[int]
    GET_HITS_FIELD_NUMBER: _ClassVar[int]
    GET_MISSES_FIELD_NUMBER: _ClassVar[int]
    DELETE_HITS_FIELD_NUMBER: _ClassVar[int]
    DELETE_MISSES_FIELD_NUMBER: _ClassVar[int]
    BYTES_READ_FIELD_NUMBER: _ClassVar[int]
    BYTES_WRITTEN_FIELD_NUMBER: _ClassVar[int]
    LIMIT_MAXBYTES_FIELD_NUMBER: _ClassVar[int]
    CURR_ITEMS_FIELD_NUMBER: _ClassVar[int]
    EVICTIONS_FIELD_NUMBER: _ClassVar[int]
    BYTES_FIELD_NUMBER: _ClassVar[int]
    curr_connections: int
    cmd_get: int
    cmd_set: int
    cmd_flush: int
    get_hits: int
    get_misses: int
    delete_hits: int
    delete_misses: int
    bytes_read: int
    bytes_written: int
    limit_maxbytes: int
    curr_items: int
    evictions: int
    bytes: int
    def __init__(self, curr_connections: _Optional[int] = ..., cmd_get: _Optional[int] = ..., cmd_set: _Optional[int] = ..., cmd_flush: _Optional[int] = ..., get_hits: _Optional[int] = ..., get_misses: _Optional[int] = ..., delete_hits: _Optional[int] = ..., delete_misses: _Optional[int] = ..., bytes_read: _Optional[int] = ..., bytes_written: _Optional[int] = ..., limit_maxbytes: _Optional[int] = ..., curr_items: _Optional[int] = ..., evictions: _Optional[int] = ..., bytes: _Optional[int] = ...) -> None: ...

class CGCMsgSQLStats(_message.Message):
    __slots__ = ("schema_catalog",)
    SCHEMA_CATALOG_FIELD_NUMBER: _ClassVar[int]
    schema_catalog: int
    def __init__(self, schema_catalog: _Optional[int] = ...) -> None: ...

class CGCMsgSQLStatsResponse(_message.Message):
    __slots__ = ("threads", "threads_connected", "threads_active", "operations_submitted", "prepared_statements_executed", "non_prepared_statements_executed", "deadlock_retries", "operations_timed_out_in_queue", "errors")
    THREADS_FIELD_NUMBER: _ClassVar[int]
    THREADS_CONNECTED_FIELD_NUMBER: _ClassVar[int]
    THREADS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    OPERATIONS_SUBMITTED_FIELD_NUMBER: _ClassVar[int]
    PREPARED_STATEMENTS_EXECUTED_FIELD_NUMBER: _ClassVar[int]
    NON_PREPARED_STATEMENTS_EXECUTED_FIELD_NUMBER: _ClassVar[int]
    DEADLOCK_RETRIES_FIELD_NUMBER: _ClassVar[int]
    OPERATIONS_TIMED_OUT_IN_QUEUE_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    threads: int
    threads_connected: int
    threads_active: int
    operations_submitted: int
    prepared_statements_executed: int
    non_prepared_statements_executed: int
    deadlock_retries: int
    operations_timed_out_in_queue: int
    errors: int
    def __init__(self, threads: _Optional[int] = ..., threads_connected: _Optional[int] = ..., threads_active: _Optional[int] = ..., operations_submitted: _Optional[int] = ..., prepared_statements_executed: _Optional[int] = ..., non_prepared_statements_executed: _Optional[int] = ..., deadlock_retries: _Optional[int] = ..., operations_timed_out_in_queue: _Optional[int] = ..., errors: _Optional[int] = ...) -> None: ...

class CMsgAMAddFreeLicense(_message.Message):
    __slots__ = ("steamid", "ip_public", "packageid", "store_country_code")
    STEAMID_FIELD_NUMBER: _ClassVar[int]
    IP_PUBLIC_FIELD_NUMBER: _ClassVar[int]
    PACKAGEID_FIELD_NUMBER: _ClassVar[int]
    STORE_COUNTRY_CODE_FIELD_NUMBER: _ClassVar[int]
    steamid: int
    ip_public: int
    packageid: int
    store_country_code: str
    def __init__(self, steamid: _Optional[int] = ..., ip_public: _Optional[int] = ..., packageid: _Optional[int] = ..., store_country_code: _Optional[str] = ...) -> None: ...

class CMsgAMAddFreeLicenseResponse(_message.Message):
    __slots__ = ("eresult", "purchase_result_detail", "transid")
    ERESULT_FIELD_NUMBER: _ClassVar[int]
    PURCHASE_RESULT_DETAIL_FIELD_NUMBER: _ClassVar[int]
    TRANSID_FIELD_NUMBER: _ClassVar[int]
    eresult: int
    purchase_result_detail: int
    transid: int
    def __init__(self, eresult: _Optional[int] = ..., purchase_result_detail: _Optional[int] = ..., transid: _Optional[int] = ...) -> None: ...

class CGCMsgGetIPLocation(_message.Message):
    __slots__ = ("ips",)
    IPS_FIELD_NUMBER: _ClassVar[int]
    ips: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, ips: _Optional[_Iterable[int]] = ...) -> None: ...

class CGCMsgGetIPASN(_message.Message):
    __slots__ = ("ips",)
    IPS_FIELD_NUMBER: _ClassVar[int]
    ips: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, ips: _Optional[_Iterable[int]] = ...) -> None: ...

class CIPASNInfo(_message.Message):
    __slots__ = ("ip", "asn")
    IP_FIELD_NUMBER: _ClassVar[int]
    ASN_FIELD_NUMBER: _ClassVar[int]
    ip: int
    asn: int
    def __init__(self, ip: _Optional[int] = ..., asn: _Optional[int] = ...) -> None: ...

class CGCMsgGetIPASNResponse(_message.Message):
    __slots__ = ("infos",)
    INFOS_FIELD_NUMBER: _ClassVar[int]
    infos: _containers.RepeatedCompositeFieldContainer[CIPASNInfo]
    def __init__(self, infos: _Optional[_Iterable[_Union[CIPASNInfo, _Mapping]]] = ...) -> None: ...

class CMsgAMSendEmail(_message.Message):
    __slots__ = ("steamid", "email_msg_type", "email_format", "persona_name_tokens", "source_gc", "tokens")
    class ReplacementToken(_message.Message):
        __slots__ = ("token_name", "token_value")
        TOKEN_NAME_FIELD_NUMBER: _ClassVar[int]
        TOKEN_VALUE_FIELD_NUMBER: _ClassVar[int]
        token_name: str
        token_value: str
        def __init__(self, token_name: _Optional[str] = ..., token_value: _Optional[str] = ...) -> None: ...
    class PersonaNameReplacementToken(_message.Message):
        __slots__ = ("steamid", "token_name")
        STEAMID_FIELD_NUMBER: _ClassVar[int]
        TOKEN_NAME_FIELD_NUMBER: _ClassVar[int]
        steamid: int
        token_name: str
        def __init__(self, steamid: _Optional[int] = ..., token_name: _Optional[str] = ...) -> None: ...
    STEAMID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FORMAT_FIELD_NUMBER: _ClassVar[int]
    PERSONA_NAME_TOKENS_FIELD_NUMBER: _ClassVar[int]
    SOURCE_GC_FIELD_NUMBER: _ClassVar[int]
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    steamid: int
    email_msg_type: int
    email_format: int
    persona_name_tokens: _containers.RepeatedCompositeFieldContainer[CMsgAMSendEmail.PersonaNameReplacementToken]
    source_gc: int
    tokens: _containers.RepeatedCompositeFieldContainer[CMsgAMSendEmail.ReplacementToken]
    def __init__(self, steamid: _Optional[int] = ..., email_msg_type: _Optional[int] = ..., email_format: _Optional[int] = ..., persona_name_tokens: _Optional[_Iterable[_Union[CMsgAMSendEmail.PersonaNameReplacementToken, _Mapping]]] = ..., source_gc: _Optional[int] = ..., tokens: _Optional[_Iterable[_Union[CMsgAMSendEmail.ReplacementToken, _Mapping]]] = ...) -> None: ...

class CMsgAMSendEmailResponse(_message.Message):
    __slots__ = ("eresult",)
    ERESULT_FIELD_NUMBER: _ClassVar[int]
    eresult: int
    def __init__(self, eresult: _Optional[int] = ...) -> None: ...

class CMsgGCGetEmailTemplate(_message.Message):
    __slots__ = ("app_id", "email_msg_type", "email_lang", "email_format")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    EMAIL_LANG_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FORMAT_FIELD_NUMBER: _ClassVar[int]
    app_id: int
    email_msg_type: int
    email_lang: int
    email_format: int
    def __init__(self, app_id: _Optional[int] = ..., email_msg_type: _Optional[int] = ..., email_lang: _Optional[int] = ..., email_format: _Optional[int] = ...) -> None: ...

class CMsgGCGetEmailTemplateResponse(_message.Message):
    __slots__ = ("eresult", "template_exists", "template")
    ERESULT_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_EXISTS_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    eresult: int
    template_exists: bool
    template: str
    def __init__(self, eresult: _Optional[int] = ..., template_exists: bool = ..., template: _Optional[str] = ...) -> None: ...

class CMsgAMGrantGuestPasses2(_message.Message):
    __slots__ = ("steam_id", "package_id", "passes_to_grant", "days_to_expiration", "action")
    STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    PACKAGE_ID_FIELD_NUMBER: _ClassVar[int]
    PASSES_TO_GRANT_FIELD_NUMBER: _ClassVar[int]
    DAYS_TO_EXPIRATION_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    steam_id: int
    package_id: int
    passes_to_grant: int
    days_to_expiration: int
    action: int
    def __init__(self, steam_id: _Optional[int] = ..., package_id: _Optional[int] = ..., passes_to_grant: _Optional[int] = ..., days_to_expiration: _Optional[int] = ..., action: _Optional[int] = ...) -> None: ...

class CMsgAMGrantGuestPasses2Response(_message.Message):
    __slots__ = ("eresult", "passes_granted")
    ERESULT_FIELD_NUMBER: _ClassVar[int]
    PASSES_GRANTED_FIELD_NUMBER: _ClassVar[int]
    eresult: int
    passes_granted: int
    def __init__(self, eresult: _Optional[int] = ..., passes_granted: _Optional[int] = ...) -> None: ...

class CMsgGCGetPersonaNames(_message.Message):
    __slots__ = ("steamids",)
    STEAMIDS_FIELD_NUMBER: _ClassVar[int]
    steamids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, steamids: _Optional[_Iterable[int]] = ...) -> None: ...

class CMsgGCGetPersonaNames_Response(_message.Message):
    __slots__ = ("succeeded_lookups", "failed_lookup_steamids")
    class PersonaName(_message.Message):
        __slots__ = ("steamid", "persona_name")
        STEAMID_FIELD_NUMBER: _ClassVar[int]
        PERSONA_NAME_FIELD_NUMBER: _ClassVar[int]
        steamid: int
        persona_name: str
        def __init__(self, steamid: _Optional[int] = ..., persona_name: _Optional[str] = ...) -> None: ...
    SUCCEEDED_LOOKUPS_FIELD_NUMBER: _ClassVar[int]
    FAILED_LOOKUP_STEAMIDS_FIELD_NUMBER: _ClassVar[int]
    succeeded_lookups: _containers.RepeatedCompositeFieldContainer[CMsgGCGetPersonaNames_Response.PersonaName]
    failed_lookup_steamids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, succeeded_lookups: _Optional[_Iterable[_Union[CMsgGCGetPersonaNames_Response.PersonaName, _Mapping]]] = ..., failed_lookup_steamids: _Optional[_Iterable[int]] = ...) -> None: ...

class CMsgGCCheckFriendship(_message.Message):
    __slots__ = ("steamid_left", "steamid_right")
    STEAMID_LEFT_FIELD_NUMBER: _ClassVar[int]
    STEAMID_RIGHT_FIELD_NUMBER: _ClassVar[int]
    steamid_left: int
    steamid_right: int
    def __init__(self, steamid_left: _Optional[int] = ..., steamid_right: _Optional[int] = ...) -> None: ...

class CMsgGCCheckFriendship_Response(_message.Message):
    __slots__ = ("success", "found_friendship")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    FOUND_FRIENDSHIP_FIELD_NUMBER: _ClassVar[int]
    success: bool
    found_friendship: bool
    def __init__(self, success: bool = ..., found_friendship: bool = ...) -> None: ...

class CMsgGCGetAppFriendsList(_message.Message):
    __slots__ = ("steamid", "include_friendship_timestamps", "include_friends_with_no_play_time")
    STEAMID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_FRIENDSHIP_TIMESTAMPS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_FRIENDS_WITH_NO_PLAY_TIME_FIELD_NUMBER: _ClassVar[int]
    steamid: int
    include_friendship_timestamps: bool
    include_friends_with_no_play_time: bool
    def __init__(self, steamid: _Optional[int] = ..., include_friendship_timestamps: bool = ..., include_friends_with_no_play_time: bool = ...) -> None: ...

class CMsgGCGetAppFriendsList_Response(_message.Message):
    __slots__ = ("success", "steamids", "friendship_timestamps", "last_playtimes")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STEAMIDS_FIELD_NUMBER: _ClassVar[int]
    FRIENDSHIP_TIMESTAMPS_FIELD_NUMBER: _ClassVar[int]
    LAST_PLAYTIMES_FIELD_NUMBER: _ClassVar[int]
    success: bool
    steamids: _containers.RepeatedScalarFieldContainer[int]
    friendship_timestamps: _containers.RepeatedScalarFieldContainer[int]
    last_playtimes: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, success: bool = ..., steamids: _Optional[_Iterable[int]] = ..., friendship_timestamps: _Optional[_Iterable[int]] = ..., last_playtimes: _Optional[_Iterable[int]] = ...) -> None: ...

class CMsgGCMsgMasterSetDirectory(_message.Message):
    __slots__ = ("master_dir_index", "dir")
    class SubGC(_message.Message):
        __slots__ = ("dir_index", "name", "box", "command_line", "gc_binary")
        DIR_INDEX_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        BOX_FIELD_NUMBER: _ClassVar[int]
        COMMAND_LINE_FIELD_NUMBER: _ClassVar[int]
        GC_BINARY_FIELD_NUMBER: _ClassVar[int]
        dir_index: int
        name: str
        box: str
        command_line: str
        gc_binary: str
        def __init__(self, dir_index: _Optional[int] = ..., name: _Optional[str] = ..., box: _Optional[str] = ..., command_line: _Optional[str] = ..., gc_binary: _Optional[str] = ...) -> None: ...
    MASTER_DIR_INDEX_FIELD_NUMBER: _ClassVar[int]
    DIR_FIELD_NUMBER: _ClassVar[int]
    master_dir_index: int
    dir: _containers.RepeatedCompositeFieldContainer[CMsgGCMsgMasterSetDirectory.SubGC]
    def __init__(self, master_dir_index: _Optional[int] = ..., dir: _Optional[_Iterable[_Union[CMsgGCMsgMasterSetDirectory.SubGC, _Mapping]]] = ...) -> None: ...

class CMsgGCMsgMasterSetDirectory_Response(_message.Message):
    __slots__ = ("eresult", "message")
    ERESULT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    eresult: int
    message: str
    def __init__(self, eresult: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class CMsgGCMsgWebAPIJobRequestForwardResponse(_message.Message):
    __slots__ = ("dir_index",)
    DIR_INDEX_FIELD_NUMBER: _ClassVar[int]
    dir_index: int
    def __init__(self, dir_index: _Optional[int] = ...) -> None: ...

class CGCSystemMsg_GetPurchaseTrust_Request(_message.Message):
    __slots__ = ("steamid",)
    STEAMID_FIELD_NUMBER: _ClassVar[int]
    steamid: int
    def __init__(self, steamid: _Optional[int] = ...) -> None: ...

class CGCSystemMsg_GetPurchaseTrust_Response(_message.Message):
    __slots__ = ("has_prior_purchase_history", "has_no_recent_password_resets", "is_wallet_cash_trusted", "time_all_trusted")
    HAS_PRIOR_PURCHASE_HISTORY_FIELD_NUMBER: _ClassVar[int]
    HAS_NO_RECENT_PASSWORD_RESETS_FIELD_NUMBER: _ClassVar[int]
    IS_WALLET_CASH_TRUSTED_FIELD_NUMBER: _ClassVar[int]
    TIME_ALL_TRUSTED_FIELD_NUMBER: _ClassVar[int]
    has_prior_purchase_history: bool
    has_no_recent_password_resets: bool
    is_wallet_cash_trusted: bool
    time_all_trusted: int
    def __init__(self, has_prior_purchase_history: bool = ..., has_no_recent_password_resets: bool = ..., is_wallet_cash_trusted: bool = ..., time_all_trusted: _Optional[int] = ...) -> None: ...

class CMsgGCHAccountVacStatusChange(_message.Message):
    __slots__ = ("steam_id", "app_id", "rtime_vacban_starts", "is_banned_now", "is_banned_future")
    STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    RTIME_VACBAN_STARTS_FIELD_NUMBER: _ClassVar[int]
    IS_BANNED_NOW_FIELD_NUMBER: _ClassVar[int]
    IS_BANNED_FUTURE_FIELD_NUMBER: _ClassVar[int]
    steam_id: int
    app_id: int
    rtime_vacban_starts: int
    is_banned_now: bool
    is_banned_future: bool
    def __init__(self, steam_id: _Optional[int] = ..., app_id: _Optional[int] = ..., rtime_vacban_starts: _Optional[int] = ..., is_banned_now: bool = ..., is_banned_future: bool = ...) -> None: ...

class CMsgGCRoutingInfo(_message.Message):
    __slots__ = ("dir_index", "method", "fallback", "protobuf_field", "webapi_param")
    class RoutingMethod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        RANDOM: _ClassVar[CMsgGCRoutingInfo.RoutingMethod]
        DISCARD: _ClassVar[CMsgGCRoutingInfo.RoutingMethod]
        CLIENT_STEAMID: _ClassVar[CMsgGCRoutingInfo.RoutingMethod]
        PROTOBUF_FIELD_UINT64: _ClassVar[CMsgGCRoutingInfo.RoutingMethod]
        WEBAPI_PARAM: _ClassVar[CMsgGCRoutingInfo.RoutingMethod]
        WEBAPI_PARAM_STEAMID_ACCOUNTID: _ClassVar[CMsgGCRoutingInfo.RoutingMethod]
    RANDOM: CMsgGCRoutingInfo.RoutingMethod
    DISCARD: CMsgGCRoutingInfo.RoutingMethod
    CLIENT_STEAMID: CMsgGCRoutingInfo.RoutingMethod
    PROTOBUF_FIELD_UINT64: CMsgGCRoutingInfo.RoutingMethod
    WEBAPI_PARAM: CMsgGCRoutingInfo.RoutingMethod
    WEBAPI_PARAM_STEAMID_ACCOUNTID: CMsgGCRoutingInfo.RoutingMethod
    DIR_INDEX_FIELD_NUMBER: _ClassVar[int]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    FALLBACK_FIELD_NUMBER: _ClassVar[int]
    PROTOBUF_FIELD_FIELD_NUMBER: _ClassVar[int]
    WEBAPI_PARAM_FIELD_NUMBER: _ClassVar[int]
    dir_index: _containers.RepeatedScalarFieldContainer[int]
    method: CMsgGCRoutingInfo.RoutingMethod
    fallback: CMsgGCRoutingInfo.RoutingMethod
    protobuf_field: int
    webapi_param: str
    def __init__(self, dir_index: _Optional[_Iterable[int]] = ..., method: _Optional[_Union[CMsgGCRoutingInfo.RoutingMethod, str]] = ..., fallback: _Optional[_Union[CMsgGCRoutingInfo.RoutingMethod, str]] = ..., protobuf_field: _Optional[int] = ..., webapi_param: _Optional[str] = ...) -> None: ...

class CMsgGCMsgMasterSetWebAPIRouting(_message.Message):
    __slots__ = ("entries",)
    class Entry(_message.Message):
        __slots__ = ("interface_name", "method_name", "routing")
        INTERFACE_NAME_FIELD_NUMBER: _ClassVar[int]
        METHOD_NAME_FIELD_NUMBER: _ClassVar[int]
        ROUTING_FIELD_NUMBER: _ClassVar[int]
        interface_name: str
        method_name: str
        routing: CMsgGCRoutingInfo
        def __init__(self, interface_name: _Optional[str] = ..., method_name: _Optional[str] = ..., routing: _Optional[_Union[CMsgGCRoutingInfo, _Mapping]] = ...) -> None: ...
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[CMsgGCMsgMasterSetWebAPIRouting.Entry]
    def __init__(self, entries: _Optional[_Iterable[_Union[CMsgGCMsgMasterSetWebAPIRouting.Entry, _Mapping]]] = ...) -> None: ...

class CMsgGCMsgMasterSetClientMsgRouting(_message.Message):
    __slots__ = ("entries",)
    class Entry(_message.Message):
        __slots__ = ("msg_type", "routing")
        MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
        ROUTING_FIELD_NUMBER: _ClassVar[int]
        msg_type: int
        routing: CMsgGCRoutingInfo
        def __init__(self, msg_type: _Optional[int] = ..., routing: _Optional[_Union[CMsgGCRoutingInfo, _Mapping]] = ...) -> None: ...
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[CMsgGCMsgMasterSetClientMsgRouting.Entry]
    def __init__(self, entries: _Optional[_Iterable[_Union[CMsgGCMsgMasterSetClientMsgRouting.Entry, _Mapping]]] = ...) -> None: ...

class CMsgGCMsgMasterSetWebAPIRouting_Response(_message.Message):
    __slots__ = ("eresult",)
    ERESULT_FIELD_NUMBER: _ClassVar[int]
    eresult: int
    def __init__(self, eresult: _Optional[int] = ...) -> None: ...

class CMsgGCMsgMasterSetClientMsgRouting_Response(_message.Message):
    __slots__ = ("eresult",)
    ERESULT_FIELD_NUMBER: _ClassVar[int]
    eresult: int
    def __init__(self, eresult: _Optional[int] = ...) -> None: ...

class CMsgGCMsgSetOptions(_message.Message):
    __slots__ = ("options", "client_msg_ranges", "gcsql_version")
    class Option(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NOTIFY_USER_SESSIONS: _ClassVar[CMsgGCMsgSetOptions.Option]
        NOTIFY_SERVER_SESSIONS: _ClassVar[CMsgGCMsgSetOptions.Option]
        NOTIFY_ACHIEVEMENTS: _ClassVar[CMsgGCMsgSetOptions.Option]
        NOTIFY_VAC_ACTION: _ClassVar[CMsgGCMsgSetOptions.Option]
    NOTIFY_USER_SESSIONS: CMsgGCMsgSetOptions.Option
    NOTIFY_SERVER_SESSIONS: CMsgGCMsgSetOptions.Option
    NOTIFY_ACHIEVEMENTS: CMsgGCMsgSetOptions.Option
    NOTIFY_VAC_ACTION: CMsgGCMsgSetOptions.Option
    class GCSQLVersion(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        GCSQL_VERSION_BASELINE: _ClassVar[CMsgGCMsgSetOptions.GCSQLVersion]
        GCSQL_VERSION_BOOLTYPE: _ClassVar[CMsgGCMsgSetOptions.GCSQLVersion]
    GCSQL_VERSION_BASELINE: CMsgGCMsgSetOptions.GCSQLVersion
    GCSQL_VERSION_BOOLTYPE: CMsgGCMsgSetOptions.GCSQLVersion
    class MessageRange(_message.Message):
        __slots__ = ("low", "high")
        LOW_FIELD_NUMBER: _ClassVar[int]
        HIGH_FIELD_NUMBER: _ClassVar[int]
        low: int
        high: int
        def __init__(self, low: _Optional[int] = ..., high: _Optional[int] = ...) -> None: ...
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    CLIENT_MSG_RANGES_FIELD_NUMBER: _ClassVar[int]
    GCSQL_VERSION_FIELD_NUMBER: _ClassVar[int]
    options: _containers.RepeatedScalarFieldContainer[CMsgGCMsgSetOptions.Option]
    client_msg_ranges: _containers.RepeatedCompositeFieldContainer[CMsgGCMsgSetOptions.MessageRange]
    gcsql_version: CMsgGCMsgSetOptions.GCSQLVersion
    def __init__(self, options: _Optional[_Iterable[_Union[CMsgGCMsgSetOptions.Option, str]]] = ..., client_msg_ranges: _Optional[_Iterable[_Union[CMsgGCMsgSetOptions.MessageRange, _Mapping]]] = ..., gcsql_version: _Optional[_Union[CMsgGCMsgSetOptions.GCSQLVersion, str]] = ...) -> None: ...

class CMsgGCHUpdateSession(_message.Message):
    __slots__ = ("steam_id", "app_id", "online", "server_steam_id", "server_addr", "server_port", "os_type", "client_addr", "extra_fields")
    class ExtraField(_message.Message):
        __slots__ = ("name", "value")
        NAME_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        name: str
        value: str
        def __init__(self, name: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    ONLINE_FIELD_NUMBER: _ClassVar[int]
    SERVER_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    SERVER_ADDR_FIELD_NUMBER: _ClassVar[int]
    SERVER_PORT_FIELD_NUMBER: _ClassVar[int]
    OS_TYPE_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ADDR_FIELD_NUMBER: _ClassVar[int]
    EXTRA_FIELDS_FIELD_NUMBER: _ClassVar[int]
    steam_id: int
    app_id: int
    online: bool
    server_steam_id: int
    server_addr: int
    server_port: int
    os_type: int
    client_addr: int
    extra_fields: _containers.RepeatedCompositeFieldContainer[CMsgGCHUpdateSession.ExtraField]
    def __init__(self, steam_id: _Optional[int] = ..., app_id: _Optional[int] = ..., online: bool = ..., server_steam_id: _Optional[int] = ..., server_addr: _Optional[int] = ..., server_port: _Optional[int] = ..., os_type: _Optional[int] = ..., client_addr: _Optional[int] = ..., extra_fields: _Optional[_Iterable[_Union[CMsgGCHUpdateSession.ExtraField, _Mapping]]] = ...) -> None: ...

class CMsgNotificationOfSuspiciousActivity(_message.Message):
    __slots__ = ("steamid", "appid", "multiple_instances")
    class MultipleGameInstances(_message.Message):
        __slots__ = ("app_instance_count", "other_steamids")
        APP_INSTANCE_COUNT_FIELD_NUMBER: _ClassVar[int]
        OTHER_STEAMIDS_FIELD_NUMBER: _ClassVar[int]
        app_instance_count: int
        other_steamids: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, app_instance_count: _Optional[int] = ..., other_steamids: _Optional[_Iterable[int]] = ...) -> None: ...
    STEAMID_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_INSTANCES_FIELD_NUMBER: _ClassVar[int]
    steamid: int
    appid: int
    multiple_instances: CMsgNotificationOfSuspiciousActivity.MultipleGameInstances
    def __init__(self, steamid: _Optional[int] = ..., appid: _Optional[int] = ..., multiple_instances: _Optional[_Union[CMsgNotificationOfSuspiciousActivity.MultipleGameInstances, _Mapping]] = ...) -> None: ...

class CMsgGCHVacVerificationChange(_message.Message):
    __slots__ = ("steamid", "appid", "is_verified")
    STEAMID_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    IS_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    steamid: int
    appid: int
    is_verified: bool
    def __init__(self, steamid: _Optional[int] = ..., appid: _Optional[int] = ..., is_verified: bool = ...) -> None: ...

class CMsgGCHAccountPhoneNumberChange(_message.Message):
    __slots__ = ("steamid", "appid", "phone_id", "is_verified", "is_identifying")
    STEAMID_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    PHONE_ID_FIELD_NUMBER: _ClassVar[int]
    IS_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    IS_IDENTIFYING_FIELD_NUMBER: _ClassVar[int]
    steamid: int
    appid: int
    phone_id: int
    is_verified: bool
    is_identifying: bool
    def __init__(self, steamid: _Optional[int] = ..., appid: _Optional[int] = ..., phone_id: _Optional[int] = ..., is_verified: bool = ..., is_identifying: bool = ...) -> None: ...

class CMsgGCHAccountTwoFactorChange(_message.Message):
    __slots__ = ("steamid", "appid", "twofactor_enabled")
    STEAMID_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    TWOFACTOR_ENABLED_FIELD_NUMBER: _ClassVar[int]
    steamid: int
    appid: int
    twofactor_enabled: bool
    def __init__(self, steamid: _Optional[int] = ..., appid: _Optional[int] = ..., twofactor_enabled: bool = ...) -> None: ...

class CMsgGCCheckClanMembership(_message.Message):
    __slots__ = ("steamid", "clanid")
    STEAMID_FIELD_NUMBER: _ClassVar[int]
    CLANID_FIELD_NUMBER: _ClassVar[int]
    steamid: int
    clanid: int
    def __init__(self, steamid: _Optional[int] = ..., clanid: _Optional[int] = ...) -> None: ...

class CMsgGCCheckClanMembership_Response(_message.Message):
    __slots__ = ("ismember",)
    ISMEMBER_FIELD_NUMBER: _ClassVar[int]
    ismember: bool
    def __init__(self, ismember: bool = ...) -> None: ...

class CMsgGCHAppCheersReceived(_message.Message):
    __slots__ = ("appid", "cheer_targets")
    class CheerTypeAmount(_message.Message):
        __slots__ = ("cheer_type", "cheer_amount")
        CHEER_TYPE_FIELD_NUMBER: _ClassVar[int]
        CHEER_AMOUNT_FIELD_NUMBER: _ClassVar[int]
        cheer_type: int
        cheer_amount: int
        def __init__(self, cheer_type: _Optional[int] = ..., cheer_amount: _Optional[int] = ...) -> None: ...
    class CheerTarget(_message.Message):
        __slots__ = ("cheer_target", "cheer_types")
        CHEER_TARGET_FIELD_NUMBER: _ClassVar[int]
        CHEER_TYPES_FIELD_NUMBER: _ClassVar[int]
        cheer_target: int
        cheer_types: _containers.RepeatedCompositeFieldContainer[CMsgGCHAppCheersReceived.CheerTypeAmount]
        def __init__(self, cheer_target: _Optional[int] = ..., cheer_types: _Optional[_Iterable[_Union[CMsgGCHAppCheersReceived.CheerTypeAmount, _Mapping]]] = ...) -> None: ...
    APPID_FIELD_NUMBER: _ClassVar[int]
    CHEER_TARGETS_FIELD_NUMBER: _ClassVar[int]
    appid: int
    cheer_targets: _containers.RepeatedCompositeFieldContainer[CMsgGCHAppCheersReceived.CheerTarget]
    def __init__(self, appid: _Optional[int] = ..., cheer_targets: _Optional[_Iterable[_Union[CMsgGCHAppCheersReceived.CheerTarget, _Mapping]]] = ...) -> None: ...

class CMsgGCHAppCheersGetAllowedTypes(_message.Message):
    __slots__ = ("appid", "cheer_target")
    APPID_FIELD_NUMBER: _ClassVar[int]
    CHEER_TARGET_FIELD_NUMBER: _ClassVar[int]
    appid: int
    cheer_target: int
    def __init__(self, appid: _Optional[int] = ..., cheer_target: _Optional[int] = ...) -> None: ...

class CMsgGCHAppCheersGetAllowedTypesResponse(_message.Message):
    __slots__ = ("cheer_types_valid_all_users", "cheer_remaps", "cache_duration")
    class CheerRemaps(_message.Message):
        __slots__ = ("original_cheer_type", "remapped_cheer_type", "account_ids")
        ORIGINAL_CHEER_TYPE_FIELD_NUMBER: _ClassVar[int]
        REMAPPED_CHEER_TYPE_FIELD_NUMBER: _ClassVar[int]
        ACCOUNT_IDS_FIELD_NUMBER: _ClassVar[int]
        original_cheer_type: int
        remapped_cheer_type: int
        account_ids: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, original_cheer_type: _Optional[int] = ..., remapped_cheer_type: _Optional[int] = ..., account_ids: _Optional[_Iterable[int]] = ...) -> None: ...
    CHEER_TYPES_VALID_ALL_USERS_FIELD_NUMBER: _ClassVar[int]
    CHEER_REMAPS_FIELD_NUMBER: _ClassVar[int]
    CACHE_DURATION_FIELD_NUMBER: _ClassVar[int]
    cheer_types_valid_all_users: _containers.RepeatedScalarFieldContainer[int]
    cheer_remaps: _containers.RepeatedCompositeFieldContainer[CMsgGCHAppCheersGetAllowedTypesResponse.CheerRemaps]
    cache_duration: int
    def __init__(self, cheer_types_valid_all_users: _Optional[_Iterable[int]] = ..., cheer_remaps: _Optional[_Iterable[_Union[CMsgGCHAppCheersGetAllowedTypesResponse.CheerRemaps, _Mapping]]] = ..., cache_duration: _Optional[int] = ...) -> None: ...

class CWorkshop_AddSpecialPayment_Request(_message.Message):
    __slots__ = ("appid", "gameitemid", "date", "payment_us_usd", "payment_row_usd")
    APPID_FIELD_NUMBER: _ClassVar[int]
    GAMEITEMID_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    PAYMENT_US_USD_FIELD_NUMBER: _ClassVar[int]
    PAYMENT_ROW_USD_FIELD_NUMBER: _ClassVar[int]
    appid: int
    gameitemid: int
    date: str
    payment_us_usd: int
    payment_row_usd: int
    def __init__(self, appid: _Optional[int] = ..., gameitemid: _Optional[int] = ..., date: _Optional[str] = ..., payment_us_usd: _Optional[int] = ..., payment_row_usd: _Optional[int] = ...) -> None: ...

class CWorkshop_AddSpecialPayment_Response(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CWorkshop_GetSpecialPayments_Request(_message.Message):
    __slots__ = ("appid", "gameitemid", "date")
    APPID_FIELD_NUMBER: _ClassVar[int]
    GAMEITEMID_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    appid: int
    gameitemid: int
    date: str
    def __init__(self, appid: _Optional[int] = ..., gameitemid: _Optional[int] = ..., date: _Optional[str] = ...) -> None: ...

class CWorkshop_GetSpecialPayments_Response(_message.Message):
    __slots__ = ("special_payments",)
    class SpecialPayment(_message.Message):
        __slots__ = ("appid", "gameitemid", "date", "net_payment_us_usd", "net_payment_row_usd")
        APPID_FIELD_NUMBER: _ClassVar[int]
        GAMEITEMID_FIELD_NUMBER: _ClassVar[int]
        DATE_FIELD_NUMBER: _ClassVar[int]
        NET_PAYMENT_US_USD_FIELD_NUMBER: _ClassVar[int]
        NET_PAYMENT_ROW_USD_FIELD_NUMBER: _ClassVar[int]
        appid: int
        gameitemid: int
        date: str
        net_payment_us_usd: int
        net_payment_row_usd: int
        def __init__(self, appid: _Optional[int] = ..., gameitemid: _Optional[int] = ..., date: _Optional[str] = ..., net_payment_us_usd: _Optional[int] = ..., net_payment_row_usd: _Optional[int] = ...) -> None: ...
    SPECIAL_PAYMENTS_FIELD_NUMBER: _ClassVar[int]
    special_payments: _containers.RepeatedCompositeFieldContainer[CWorkshop_GetSpecialPayments_Response.SpecialPayment]
    def __init__(self, special_payments: _Optional[_Iterable[_Union[CWorkshop_GetSpecialPayments_Response.SpecialPayment, _Mapping]]] = ...) -> None: ...

class CMsgGCReportMetrics(_message.Message):
    __slots__ = ("metric_data",)
    class MetricEntry(_message.Message):
        __slots__ = ("catalog", "operation", "timestamp", "dimensions", "measurements")
        class Dimension(_message.Message):
            __slots__ = ("name", "value_string", "value_integer", "value_boolean")
            NAME_FIELD_NUMBER: _ClassVar[int]
            VALUE_STRING_FIELD_NUMBER: _ClassVar[int]
            VALUE_INTEGER_FIELD_NUMBER: _ClassVar[int]
            VALUE_BOOLEAN_FIELD_NUMBER: _ClassVar[int]
            name: str
            value_string: str
            value_integer: int
            value_boolean: bool
            def __init__(self, name: _Optional[str] = ..., value_string: _Optional[str] = ..., value_integer: _Optional[int] = ..., value_boolean: bool = ...) -> None: ...
        class Measurement(_message.Message):
            __slots__ = ("name", "value_integer", "value_float")
            NAME_FIELD_NUMBER: _ClassVar[int]
            VALUE_INTEGER_FIELD_NUMBER: _ClassVar[int]
            VALUE_FLOAT_FIELD_NUMBER: _ClassVar[int]
            name: str
            value_integer: int
            value_float: float
            def __init__(self, name: _Optional[str] = ..., value_integer: _Optional[int] = ..., value_float: _Optional[float] = ...) -> None: ...
        CATALOG_FIELD_NUMBER: _ClassVar[int]
        OPERATION_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
        MEASUREMENTS_FIELD_NUMBER: _ClassVar[int]
        catalog: str
        operation: str
        timestamp: float
        dimensions: _containers.RepeatedCompositeFieldContainer[CMsgGCReportMetrics.MetricEntry.Dimension]
        measurements: _containers.RepeatedCompositeFieldContainer[CMsgGCReportMetrics.MetricEntry.Measurement]
        def __init__(self, catalog: _Optional[str] = ..., operation: _Optional[str] = ..., timestamp: _Optional[float] = ..., dimensions: _Optional[_Iterable[_Union[CMsgGCReportMetrics.MetricEntry.Dimension, _Mapping]]] = ..., measurements: _Optional[_Iterable[_Union[CMsgGCReportMetrics.MetricEntry.Measurement, _Mapping]]] = ...) -> None: ...
    METRIC_DATA_FIELD_NUMBER: _ClassVar[int]
    metric_data: _containers.RepeatedCompositeFieldContainer[CMsgGCReportMetrics.MetricEntry]
    def __init__(self, metric_data: _Optional[_Iterable[_Union[CMsgGCReportMetrics.MetricEntry, _Mapping]]] = ...) -> None: ...

class CMsgGCReportMetrics_Response(_message.Message):
    __slots__ = ("eresult", "failed_entry_count")
    ERESULT_FIELD_NUMBER: _ClassVar[int]
    FAILED_ENTRY_COUNT_FIELD_NUMBER: _ClassVar[int]
    eresult: int
    failed_entry_count: int
    def __init__(self, eresult: _Optional[int] = ..., failed_entry_count: _Optional[int] = ...) -> None: ...
