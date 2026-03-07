from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

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
    def __init__(
        self,
        status: int | None = ...,
        account_id: int | None = ...,
        publisher_group_id: int | None = ...,
        key_id: int | None = ...,
        domain: str | None = ...,
    ) -> None: ...

class CMsgHttpRequest(_message.Message):
    __slots__ = (
        "request_method",
        "hostname",
        "url",
        "headers",
        "get_params",
        "post_params",
        "body",
        "absolute_timeout",
        "use_https",
    )
    class RequestHeader(_message.Message):
        __slots__ = ("name", "value")
        NAME_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        name: str
        value: str
        def __init__(self, name: str | None = ..., value: str | None = ...) -> None: ...

    class QueryParam(_message.Message):
        __slots__ = ("name", "value")
        NAME_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        name: str
        value: bytes
        def __init__(self, name: str | None = ..., value: bytes | None = ...) -> None: ...

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
    def __init__(
        self,
        request_method: int | None = ...,
        hostname: str | None = ...,
        url: str | None = ...,
        headers: _Iterable[CMsgHttpRequest.RequestHeader | _Mapping] | None = ...,
        get_params: _Iterable[CMsgHttpRequest.QueryParam | _Mapping] | None = ...,
        post_params: _Iterable[CMsgHttpRequest.QueryParam | _Mapping] | None = ...,
        body: bytes | None = ...,
        absolute_timeout: int | None = ...,
        use_https: bool = ...,
    ) -> None: ...

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
    def __init__(
        self,
        interface_name: str | None = ...,
        method_name: str | None = ...,
        version: int | None = ...,
        api_key: CMsgWebAPIKey | _Mapping | None = ...,
        request: CMsgHttpRequest | _Mapping | None = ...,
        routing_app_id: int | None = ...,
    ) -> None: ...

class CMsgHttpResponse(_message.Message):
    __slots__ = ("status_code", "headers", "body")
    class ResponseHeader(_message.Message):
        __slots__ = ("name", "value")
        NAME_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        name: str
        value: str
        def __init__(self, name: str | None = ..., value: str | None = ...) -> None: ...

    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    headers: _containers.RepeatedCompositeFieldContainer[CMsgHttpResponse.ResponseHeader]
    body: bytes
    def __init__(
        self,
        status_code: int | None = ...,
        headers: _Iterable[CMsgHttpResponse.ResponseHeader | _Mapping] | None = ...,
        body: bytes | None = ...,
    ) -> None: ...

class CMsgAMFindAccounts(_message.Message):
    __slots__ = ("search_type", "search_string")
    SEARCH_TYPE_FIELD_NUMBER: _ClassVar[int]
    SEARCH_STRING_FIELD_NUMBER: _ClassVar[int]
    search_type: int
    search_string: str
    def __init__(self, search_type: int | None = ..., search_string: str | None = ...) -> None: ...

class CMsgAMFindAccountsResponse(_message.Message):
    __slots__ = ("steam_id",)
    STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    steam_id: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, steam_id: _Iterable[int] | None = ...) -> None: ...

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
    def __init__(
        self,
        source: int | None = ...,
        alert_type: int | None = ...,
        critical: bool = ...,
        time: int | None = ...,
        appid: int | None = ...,
        text: str | None = ...,
        recipient: str | None = ...,
    ) -> None: ...

class CMsgAMGetLicenses(_message.Message):
    __slots__ = ("steamid",)
    STEAMID_FIELD_NUMBER: _ClassVar[int]
    steamid: int
    def __init__(self, steamid: int | None = ...) -> None: ...

class CMsgPackageLicense(_message.Message):
    __slots__ = ("package_id", "time_created", "owner_id")
    PACKAGE_ID_FIELD_NUMBER: _ClassVar[int]
    TIME_CREATED_FIELD_NUMBER: _ClassVar[int]
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    package_id: int
    time_created: int
    owner_id: int
    def __init__(
        self,
        package_id: int | None = ...,
        time_created: int | None = ...,
        owner_id: int | None = ...,
    ) -> None: ...

class CMsgAMGetLicensesResponse(_message.Message):
    __slots__ = ("license", "result")
    LICENSE_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    license: _containers.RepeatedCompositeFieldContainer[CMsgPackageLicense]
    result: int
    def __init__(
        self,
        license: _Iterable[CMsgPackageLicense | _Mapping] | None = ...,
        result: int | None = ...,
    ) -> None: ...

class CMsgGCGetCommandList(_message.Message):
    __slots__ = ("app_id", "command_prefix")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    COMMAND_PREFIX_FIELD_NUMBER: _ClassVar[int]
    app_id: int
    command_prefix: str
    def __init__(self, app_id: int | None = ..., command_prefix: str | None = ...) -> None: ...

class CMsgGCGetCommandListResponse(_message.Message):
    __slots__ = ("command_name",)
    COMMAND_NAME_FIELD_NUMBER: _ClassVar[int]
    command_name: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, command_name: _Iterable[str] | None = ...) -> None: ...

class CGCMsgMemCachedGet(_message.Message):
    __slots__ = ("keys",)
    KEYS_FIELD_NUMBER: _ClassVar[int]
    keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, keys: _Iterable[str] | None = ...) -> None: ...

class CGCMsgMemCachedGetResponse(_message.Message):
    __slots__ = ("values",)
    class ValueTag(_message.Message):
        __slots__ = ("found", "value")
        FOUND_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        found: bool
        value: bytes
        def __init__(self, found: bool = ..., value: bytes | None = ...) -> None: ...

    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedCompositeFieldContainer[CGCMsgMemCachedGetResponse.ValueTag]
    def __init__(
        self, values: _Iterable[CGCMsgMemCachedGetResponse.ValueTag | _Mapping] | None = ...
    ) -> None: ...

class CGCMsgMemCachedSet(_message.Message):
    __slots__ = ("keys",)
    class KeyPair(_message.Message):
        __slots__ = ("name", "value")
        NAME_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        name: str
        value: bytes
        def __init__(self, name: str | None = ..., value: bytes | None = ...) -> None: ...

    KEYS_FIELD_NUMBER: _ClassVar[int]
    keys: _containers.RepeatedCompositeFieldContainer[CGCMsgMemCachedSet.KeyPair]
    def __init__(
        self, keys: _Iterable[CGCMsgMemCachedSet.KeyPair | _Mapping] | None = ...
    ) -> None: ...

class CGCMsgMemCachedDelete(_message.Message):
    __slots__ = ("keys",)
    KEYS_FIELD_NUMBER: _ClassVar[int]
    keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, keys: _Iterable[str] | None = ...) -> None: ...

class CGCMsgMemCachedStats(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CGCMsgMemCachedStatsResponse(_message.Message):
    __slots__ = (
        "curr_connections",
        "cmd_get",
        "cmd_set",
        "cmd_flush",
        "get_hits",
        "get_misses",
        "delete_hits",
        "delete_misses",
        "bytes_read",
        "bytes_written",
        "limit_maxbytes",
        "curr_items",
        "evictions",
        "bytes",
    )
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
    def __init__(
        self,
        curr_connections: int | None = ...,
        cmd_get: int | None = ...,
        cmd_set: int | None = ...,
        cmd_flush: int | None = ...,
        get_hits: int | None = ...,
        get_misses: int | None = ...,
        delete_hits: int | None = ...,
        delete_misses: int | None = ...,
        bytes_read: int | None = ...,
        bytes_written: int | None = ...,
        limit_maxbytes: int | None = ...,
        curr_items: int | None = ...,
        evictions: int | None = ...,
        bytes: int | None = ...,
    ) -> None: ...

class CGCMsgSQLStats(_message.Message):
    __slots__ = ("schema_catalog",)
    SCHEMA_CATALOG_FIELD_NUMBER: _ClassVar[int]
    schema_catalog: int
    def __init__(self, schema_catalog: int | None = ...) -> None: ...

class CGCMsgSQLStatsResponse(_message.Message):
    __slots__ = (
        "threads",
        "threads_connected",
        "threads_active",
        "operations_submitted",
        "prepared_statements_executed",
        "non_prepared_statements_executed",
        "deadlock_retries",
        "operations_timed_out_in_queue",
        "errors",
    )
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
    def __init__(
        self,
        threads: int | None = ...,
        threads_connected: int | None = ...,
        threads_active: int | None = ...,
        operations_submitted: int | None = ...,
        prepared_statements_executed: int | None = ...,
        non_prepared_statements_executed: int | None = ...,
        deadlock_retries: int | None = ...,
        operations_timed_out_in_queue: int | None = ...,
        errors: int | None = ...,
    ) -> None: ...

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
    def __init__(
        self,
        steamid: int | None = ...,
        ip_public: int | None = ...,
        packageid: int | None = ...,
        store_country_code: str | None = ...,
    ) -> None: ...

class CMsgAMAddFreeLicenseResponse(_message.Message):
    __slots__ = ("eresult", "purchase_result_detail", "transid")
    ERESULT_FIELD_NUMBER: _ClassVar[int]
    PURCHASE_RESULT_DETAIL_FIELD_NUMBER: _ClassVar[int]
    TRANSID_FIELD_NUMBER: _ClassVar[int]
    eresult: int
    purchase_result_detail: int
    transid: int
    def __init__(
        self,
        eresult: int | None = ...,
        purchase_result_detail: int | None = ...,
        transid: int | None = ...,
    ) -> None: ...

class CGCMsgGetIPLocation(_message.Message):
    __slots__ = ("ips",)
    IPS_FIELD_NUMBER: _ClassVar[int]
    ips: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, ips: _Iterable[int] | None = ...) -> None: ...

class CGCMsgGetIPASN(_message.Message):
    __slots__ = ("ips",)
    IPS_FIELD_NUMBER: _ClassVar[int]
    ips: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, ips: _Iterable[int] | None = ...) -> None: ...

class CIPASNInfo(_message.Message):
    __slots__ = ("ip", "asn")
    IP_FIELD_NUMBER: _ClassVar[int]
    ASN_FIELD_NUMBER: _ClassVar[int]
    ip: int
    asn: int
    def __init__(self, ip: int | None = ..., asn: int | None = ...) -> None: ...

class CGCMsgGetIPASNResponse(_message.Message):
    __slots__ = ("infos",)
    INFOS_FIELD_NUMBER: _ClassVar[int]
    infos: _containers.RepeatedCompositeFieldContainer[CIPASNInfo]
    def __init__(self, infos: _Iterable[CIPASNInfo | _Mapping] | None = ...) -> None: ...

class CMsgAMSendEmail(_message.Message):
    __slots__ = (
        "steamid",
        "email_msg_type",
        "email_format",
        "persona_name_tokens",
        "source_gc",
        "tokens",
    )
    class ReplacementToken(_message.Message):
        __slots__ = ("token_name", "token_value")
        TOKEN_NAME_FIELD_NUMBER: _ClassVar[int]
        TOKEN_VALUE_FIELD_NUMBER: _ClassVar[int]
        token_name: str
        token_value: str
        def __init__(self, token_name: str | None = ..., token_value: str | None = ...) -> None: ...

    class PersonaNameReplacementToken(_message.Message):
        __slots__ = ("steamid", "token_name")
        STEAMID_FIELD_NUMBER: _ClassVar[int]
        TOKEN_NAME_FIELD_NUMBER: _ClassVar[int]
        steamid: int
        token_name: str
        def __init__(self, steamid: int | None = ..., token_name: str | None = ...) -> None: ...

    STEAMID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FORMAT_FIELD_NUMBER: _ClassVar[int]
    PERSONA_NAME_TOKENS_FIELD_NUMBER: _ClassVar[int]
    SOURCE_GC_FIELD_NUMBER: _ClassVar[int]
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    steamid: int
    email_msg_type: int
    email_format: int
    persona_name_tokens: _containers.RepeatedCompositeFieldContainer[
        CMsgAMSendEmail.PersonaNameReplacementToken
    ]
    source_gc: int
    tokens: _containers.RepeatedCompositeFieldContainer[CMsgAMSendEmail.ReplacementToken]
    def __init__(
        self,
        steamid: int | None = ...,
        email_msg_type: int | None = ...,
        email_format: int | None = ...,
        persona_name_tokens: _Iterable[CMsgAMSendEmail.PersonaNameReplacementToken | _Mapping]
        | None = ...,
        source_gc: int | None = ...,
        tokens: _Iterable[CMsgAMSendEmail.ReplacementToken | _Mapping] | None = ...,
    ) -> None: ...

class CMsgAMSendEmailResponse(_message.Message):
    __slots__ = ("eresult",)
    ERESULT_FIELD_NUMBER: _ClassVar[int]
    eresult: int
    def __init__(self, eresult: int | None = ...) -> None: ...

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
    def __init__(
        self,
        app_id: int | None = ...,
        email_msg_type: int | None = ...,
        email_lang: int | None = ...,
        email_format: int | None = ...,
    ) -> None: ...

class CMsgGCGetEmailTemplateResponse(_message.Message):
    __slots__ = ("eresult", "template_exists", "template")
    ERESULT_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_EXISTS_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    eresult: int
    template_exists: bool
    template: str
    def __init__(
        self, eresult: int | None = ..., template_exists: bool = ..., template: str | None = ...
    ) -> None: ...

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
    def __init__(
        self,
        steam_id: int | None = ...,
        package_id: int | None = ...,
        passes_to_grant: int | None = ...,
        days_to_expiration: int | None = ...,
        action: int | None = ...,
    ) -> None: ...

class CMsgAMGrantGuestPasses2Response(_message.Message):
    __slots__ = ("eresult", "passes_granted")
    ERESULT_FIELD_NUMBER: _ClassVar[int]
    PASSES_GRANTED_FIELD_NUMBER: _ClassVar[int]
    eresult: int
    passes_granted: int
    def __init__(self, eresult: int | None = ..., passes_granted: int | None = ...) -> None: ...

class CMsgGCGetPersonaNames(_message.Message):
    __slots__ = ("steamids",)
    STEAMIDS_FIELD_NUMBER: _ClassVar[int]
    steamids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, steamids: _Iterable[int] | None = ...) -> None: ...

class CMsgGCGetPersonaNames_Response(_message.Message):
    __slots__ = ("succeeded_lookups", "failed_lookup_steamids")
    class PersonaName(_message.Message):
        __slots__ = ("steamid", "persona_name")
        STEAMID_FIELD_NUMBER: _ClassVar[int]
        PERSONA_NAME_FIELD_NUMBER: _ClassVar[int]
        steamid: int
        persona_name: str
        def __init__(self, steamid: int | None = ..., persona_name: str | None = ...) -> None: ...

    SUCCEEDED_LOOKUPS_FIELD_NUMBER: _ClassVar[int]
    FAILED_LOOKUP_STEAMIDS_FIELD_NUMBER: _ClassVar[int]
    succeeded_lookups: _containers.RepeatedCompositeFieldContainer[
        CMsgGCGetPersonaNames_Response.PersonaName
    ]
    failed_lookup_steamids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        succeeded_lookups: _Iterable[CMsgGCGetPersonaNames_Response.PersonaName | _Mapping]
        | None = ...,
        failed_lookup_steamids: _Iterable[int] | None = ...,
    ) -> None: ...

class CMsgGCCheckFriendship(_message.Message):
    __slots__ = ("steamid_left", "steamid_right")
    STEAMID_LEFT_FIELD_NUMBER: _ClassVar[int]
    STEAMID_RIGHT_FIELD_NUMBER: _ClassVar[int]
    steamid_left: int
    steamid_right: int
    def __init__(self, steamid_left: int | None = ..., steamid_right: int | None = ...) -> None: ...

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
    def __init__(
        self,
        steamid: int | None = ...,
        include_friendship_timestamps: bool = ...,
        include_friends_with_no_play_time: bool = ...,
    ) -> None: ...

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
    def __init__(
        self,
        success: bool = ...,
        steamids: _Iterable[int] | None = ...,
        friendship_timestamps: _Iterable[int] | None = ...,
        last_playtimes: _Iterable[int] | None = ...,
    ) -> None: ...

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
        def __init__(
            self,
            dir_index: int | None = ...,
            name: str | None = ...,
            box: str | None = ...,
            command_line: str | None = ...,
            gc_binary: str | None = ...,
        ) -> None: ...

    MASTER_DIR_INDEX_FIELD_NUMBER: _ClassVar[int]
    DIR_FIELD_NUMBER: _ClassVar[int]
    master_dir_index: int
    dir: _containers.RepeatedCompositeFieldContainer[CMsgGCMsgMasterSetDirectory.SubGC]
    def __init__(
        self,
        master_dir_index: int | None = ...,
        dir: _Iterable[CMsgGCMsgMasterSetDirectory.SubGC | _Mapping] | None = ...,
    ) -> None: ...

class CMsgGCMsgMasterSetDirectory_Response(_message.Message):
    __slots__ = ("eresult", "message")
    ERESULT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    eresult: int
    message: str
    def __init__(self, eresult: int | None = ..., message: str | None = ...) -> None: ...

class CMsgGCMsgWebAPIJobRequestForwardResponse(_message.Message):
    __slots__ = ("dir_index",)
    DIR_INDEX_FIELD_NUMBER: _ClassVar[int]
    dir_index: int
    def __init__(self, dir_index: int | None = ...) -> None: ...

class CGCSystemMsg_GetPurchaseTrust_Request(_message.Message):
    __slots__ = ("steamid",)
    STEAMID_FIELD_NUMBER: _ClassVar[int]
    steamid: int
    def __init__(self, steamid: int | None = ...) -> None: ...

class CGCSystemMsg_GetPurchaseTrust_Response(_message.Message):
    __slots__ = (
        "has_prior_purchase_history",
        "has_no_recent_password_resets",
        "is_wallet_cash_trusted",
        "time_all_trusted",
    )
    HAS_PRIOR_PURCHASE_HISTORY_FIELD_NUMBER: _ClassVar[int]
    HAS_NO_RECENT_PASSWORD_RESETS_FIELD_NUMBER: _ClassVar[int]
    IS_WALLET_CASH_TRUSTED_FIELD_NUMBER: _ClassVar[int]
    TIME_ALL_TRUSTED_FIELD_NUMBER: _ClassVar[int]
    has_prior_purchase_history: bool
    has_no_recent_password_resets: bool
    is_wallet_cash_trusted: bool
    time_all_trusted: int
    def __init__(
        self,
        has_prior_purchase_history: bool = ...,
        has_no_recent_password_resets: bool = ...,
        is_wallet_cash_trusted: bool = ...,
        time_all_trusted: int | None = ...,
    ) -> None: ...

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
    def __init__(
        self,
        steam_id: int | None = ...,
        app_id: int | None = ...,
        rtime_vacban_starts: int | None = ...,
        is_banned_now: bool = ...,
        is_banned_future: bool = ...,
    ) -> None: ...

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
    def __init__(
        self,
        dir_index: _Iterable[int] | None = ...,
        method: CMsgGCRoutingInfo.RoutingMethod | str | None = ...,
        fallback: CMsgGCRoutingInfo.RoutingMethod | str | None = ...,
        protobuf_field: int | None = ...,
        webapi_param: str | None = ...,
    ) -> None: ...

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
        def __init__(
            self,
            interface_name: str | None = ...,
            method_name: str | None = ...,
            routing: CMsgGCRoutingInfo | _Mapping | None = ...,
        ) -> None: ...

    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[CMsgGCMsgMasterSetWebAPIRouting.Entry]
    def __init__(
        self, entries: _Iterable[CMsgGCMsgMasterSetWebAPIRouting.Entry | _Mapping] | None = ...
    ) -> None: ...

class CMsgGCMsgMasterSetClientMsgRouting(_message.Message):
    __slots__ = ("entries",)
    class Entry(_message.Message):
        __slots__ = ("msg_type", "routing")
        MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
        ROUTING_FIELD_NUMBER: _ClassVar[int]
        msg_type: int
        routing: CMsgGCRoutingInfo
        def __init__(
            self, msg_type: int | None = ..., routing: CMsgGCRoutingInfo | _Mapping | None = ...
        ) -> None: ...

    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[CMsgGCMsgMasterSetClientMsgRouting.Entry]
    def __init__(
        self, entries: _Iterable[CMsgGCMsgMasterSetClientMsgRouting.Entry | _Mapping] | None = ...
    ) -> None: ...

class CMsgGCMsgMasterSetWebAPIRouting_Response(_message.Message):
    __slots__ = ("eresult",)
    ERESULT_FIELD_NUMBER: _ClassVar[int]
    eresult: int
    def __init__(self, eresult: int | None = ...) -> None: ...

class CMsgGCMsgMasterSetClientMsgRouting_Response(_message.Message):
    __slots__ = ("eresult",)
    ERESULT_FIELD_NUMBER: _ClassVar[int]
    eresult: int
    def __init__(self, eresult: int | None = ...) -> None: ...

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
        def __init__(self, low: int | None = ..., high: int | None = ...) -> None: ...

    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    CLIENT_MSG_RANGES_FIELD_NUMBER: _ClassVar[int]
    GCSQL_VERSION_FIELD_NUMBER: _ClassVar[int]
    options: _containers.RepeatedScalarFieldContainer[CMsgGCMsgSetOptions.Option]
    client_msg_ranges: _containers.RepeatedCompositeFieldContainer[CMsgGCMsgSetOptions.MessageRange]
    gcsql_version: CMsgGCMsgSetOptions.GCSQLVersion
    def __init__(
        self,
        options: _Iterable[CMsgGCMsgSetOptions.Option | str] | None = ...,
        client_msg_ranges: _Iterable[CMsgGCMsgSetOptions.MessageRange | _Mapping] | None = ...,
        gcsql_version: CMsgGCMsgSetOptions.GCSQLVersion | str | None = ...,
    ) -> None: ...

class CMsgGCHUpdateSession(_message.Message):
    __slots__ = (
        "steam_id",
        "app_id",
        "online",
        "server_steam_id",
        "server_addr",
        "server_port",
        "os_type",
        "client_addr",
        "extra_fields",
    )
    class ExtraField(_message.Message):
        __slots__ = ("name", "value")
        NAME_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        name: str
        value: str
        def __init__(self, name: str | None = ..., value: str | None = ...) -> None: ...

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
    def __init__(
        self,
        steam_id: int | None = ...,
        app_id: int | None = ...,
        online: bool = ...,
        server_steam_id: int | None = ...,
        server_addr: int | None = ...,
        server_port: int | None = ...,
        os_type: int | None = ...,
        client_addr: int | None = ...,
        extra_fields: _Iterable[CMsgGCHUpdateSession.ExtraField | _Mapping] | None = ...,
    ) -> None: ...

class CMsgNotificationOfSuspiciousActivity(_message.Message):
    __slots__ = ("steamid", "appid", "multiple_instances")
    class MultipleGameInstances(_message.Message):
        __slots__ = ("app_instance_count", "other_steamids")
        APP_INSTANCE_COUNT_FIELD_NUMBER: _ClassVar[int]
        OTHER_STEAMIDS_FIELD_NUMBER: _ClassVar[int]
        app_instance_count: int
        other_steamids: _containers.RepeatedScalarFieldContainer[int]
        def __init__(
            self, app_instance_count: int | None = ..., other_steamids: _Iterable[int] | None = ...
        ) -> None: ...

    STEAMID_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    MULTIPLE_INSTANCES_FIELD_NUMBER: _ClassVar[int]
    steamid: int
    appid: int
    multiple_instances: CMsgNotificationOfSuspiciousActivity.MultipleGameInstances
    def __init__(
        self,
        steamid: int | None = ...,
        appid: int | None = ...,
        multiple_instances: CMsgNotificationOfSuspiciousActivity.MultipleGameInstances
        | _Mapping
        | None = ...,
    ) -> None: ...

class CMsgGCHVacVerificationChange(_message.Message):
    __slots__ = ("steamid", "appid", "is_verified")
    STEAMID_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    IS_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    steamid: int
    appid: int
    is_verified: bool
    def __init__(
        self, steamid: int | None = ..., appid: int | None = ..., is_verified: bool = ...
    ) -> None: ...

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
    def __init__(
        self,
        steamid: int | None = ...,
        appid: int | None = ...,
        phone_id: int | None = ...,
        is_verified: bool = ...,
        is_identifying: bool = ...,
    ) -> None: ...

class CMsgGCHAccountTwoFactorChange(_message.Message):
    __slots__ = ("steamid", "appid", "twofactor_enabled")
    STEAMID_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    TWOFACTOR_ENABLED_FIELD_NUMBER: _ClassVar[int]
    steamid: int
    appid: int
    twofactor_enabled: bool
    def __init__(
        self, steamid: int | None = ..., appid: int | None = ..., twofactor_enabled: bool = ...
    ) -> None: ...

class CMsgGCCheckClanMembership(_message.Message):
    __slots__ = ("steamid", "clanid")
    STEAMID_FIELD_NUMBER: _ClassVar[int]
    CLANID_FIELD_NUMBER: _ClassVar[int]
    steamid: int
    clanid: int
    def __init__(self, steamid: int | None = ..., clanid: int | None = ...) -> None: ...

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
        def __init__(
            self, cheer_type: int | None = ..., cheer_amount: int | None = ...
        ) -> None: ...

    class CheerTarget(_message.Message):
        __slots__ = ("cheer_target", "cheer_types")
        CHEER_TARGET_FIELD_NUMBER: _ClassVar[int]
        CHEER_TYPES_FIELD_NUMBER: _ClassVar[int]
        cheer_target: int
        cheer_types: _containers.RepeatedCompositeFieldContainer[
            CMsgGCHAppCheersReceived.CheerTypeAmount
        ]
        def __init__(
            self,
            cheer_target: int | None = ...,
            cheer_types: _Iterable[CMsgGCHAppCheersReceived.CheerTypeAmount | _Mapping]
            | None = ...,
        ) -> None: ...

    APPID_FIELD_NUMBER: _ClassVar[int]
    CHEER_TARGETS_FIELD_NUMBER: _ClassVar[int]
    appid: int
    cheer_targets: _containers.RepeatedCompositeFieldContainer[CMsgGCHAppCheersReceived.CheerTarget]
    def __init__(
        self,
        appid: int | None = ...,
        cheer_targets: _Iterable[CMsgGCHAppCheersReceived.CheerTarget | _Mapping] | None = ...,
    ) -> None: ...

class CMsgGCHAppCheersGetAllowedTypes(_message.Message):
    __slots__ = ("appid", "cheer_target")
    APPID_FIELD_NUMBER: _ClassVar[int]
    CHEER_TARGET_FIELD_NUMBER: _ClassVar[int]
    appid: int
    cheer_target: int
    def __init__(self, appid: int | None = ..., cheer_target: int | None = ...) -> None: ...

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
        def __init__(
            self,
            original_cheer_type: int | None = ...,
            remapped_cheer_type: int | None = ...,
            account_ids: _Iterable[int] | None = ...,
        ) -> None: ...

    CHEER_TYPES_VALID_ALL_USERS_FIELD_NUMBER: _ClassVar[int]
    CHEER_REMAPS_FIELD_NUMBER: _ClassVar[int]
    CACHE_DURATION_FIELD_NUMBER: _ClassVar[int]
    cheer_types_valid_all_users: _containers.RepeatedScalarFieldContainer[int]
    cheer_remaps: _containers.RepeatedCompositeFieldContainer[
        CMsgGCHAppCheersGetAllowedTypesResponse.CheerRemaps
    ]
    cache_duration: int
    def __init__(
        self,
        cheer_types_valid_all_users: _Iterable[int] | None = ...,
        cheer_remaps: _Iterable[CMsgGCHAppCheersGetAllowedTypesResponse.CheerRemaps | _Mapping]
        | None = ...,
        cache_duration: int | None = ...,
    ) -> None: ...

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
    def __init__(
        self,
        appid: int | None = ...,
        gameitemid: int | None = ...,
        date: str | None = ...,
        payment_us_usd: int | None = ...,
        payment_row_usd: int | None = ...,
    ) -> None: ...

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
    def __init__(
        self, appid: int | None = ..., gameitemid: int | None = ..., date: str | None = ...
    ) -> None: ...

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
        def __init__(
            self,
            appid: int | None = ...,
            gameitemid: int | None = ...,
            date: str | None = ...,
            net_payment_us_usd: int | None = ...,
            net_payment_row_usd: int | None = ...,
        ) -> None: ...

    SPECIAL_PAYMENTS_FIELD_NUMBER: _ClassVar[int]
    special_payments: _containers.RepeatedCompositeFieldContainer[
        CWorkshop_GetSpecialPayments_Response.SpecialPayment
    ]
    def __init__(
        self,
        special_payments: _Iterable[CWorkshop_GetSpecialPayments_Response.SpecialPayment | _Mapping]
        | None = ...,
    ) -> None: ...
