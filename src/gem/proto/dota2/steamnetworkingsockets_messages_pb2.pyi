import steamnetworkingsockets_messages_certs_pb2 as _steamnetworkingsockets_messages_certs_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ESteamNetworkingSocketsCipher(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_ESteamNetworkingSocketsCipher_INVALID: _ClassVar[ESteamNetworkingSocketsCipher]
    k_ESteamNetworkingSocketsCipher_NULL: _ClassVar[ESteamNetworkingSocketsCipher]
    k_ESteamNetworkingSocketsCipher_AES_256_GCM: _ClassVar[ESteamNetworkingSocketsCipher]
k_ESteamNetworkingSocketsCipher_INVALID: ESteamNetworkingSocketsCipher
k_ESteamNetworkingSocketsCipher_NULL: ESteamNetworkingSocketsCipher
k_ESteamNetworkingSocketsCipher_AES_256_GCM: ESteamNetworkingSocketsCipher

class CMsgSteamDatagramSessionCryptInfo(_message.Message):
    __slots__ = ("key_type", "key_data", "nonce", "protocol_version", "ciphers")
    class EKeyType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INVALID: _ClassVar[CMsgSteamDatagramSessionCryptInfo.EKeyType]
        CURVE25519: _ClassVar[CMsgSteamDatagramSessionCryptInfo.EKeyType]
    INVALID: CMsgSteamDatagramSessionCryptInfo.EKeyType
    CURVE25519: CMsgSteamDatagramSessionCryptInfo.EKeyType
    KEY_TYPE_FIELD_NUMBER: _ClassVar[int]
    KEY_DATA_FIELD_NUMBER: _ClassVar[int]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_VERSION_FIELD_NUMBER: _ClassVar[int]
    CIPHERS_FIELD_NUMBER: _ClassVar[int]
    key_type: CMsgSteamDatagramSessionCryptInfo.EKeyType
    key_data: bytes
    nonce: int
    protocol_version: int
    ciphers: _containers.RepeatedScalarFieldContainer[ESteamNetworkingSocketsCipher]
    def __init__(self, key_type: _Optional[_Union[CMsgSteamDatagramSessionCryptInfo.EKeyType, str]] = ..., key_data: _Optional[bytes] = ..., nonce: _Optional[int] = ..., protocol_version: _Optional[int] = ..., ciphers: _Optional[_Iterable[_Union[ESteamNetworkingSocketsCipher, str]]] = ...) -> None: ...

class CMsgSteamDatagramSessionCryptInfoSigned(_message.Message):
    __slots__ = ("info", "signature")
    INFO_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    info: bytes
    signature: bytes
    def __init__(self, info: _Optional[bytes] = ..., signature: _Optional[bytes] = ...) -> None: ...

class CMsgSteamDatagramDiagnostic(_message.Message):
    __slots__ = ("severity", "text")
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    severity: int
    text: str
    def __init__(self, severity: _Optional[int] = ..., text: _Optional[str] = ...) -> None: ...

class CMsgSteamDatagramLinkInstantaneousStats(_message.Message):
    __slots__ = ("out_packets_per_sec_x10", "out_bytes_per_sec", "in_packets_per_sec_x10", "in_bytes_per_sec", "ping_ms", "packets_dropped_pct", "packets_weird_sequence_pct", "peak_jitter_usec")
    OUT_PACKETS_PER_SEC_X10_FIELD_NUMBER: _ClassVar[int]
    OUT_BYTES_PER_SEC_FIELD_NUMBER: _ClassVar[int]
    IN_PACKETS_PER_SEC_X10_FIELD_NUMBER: _ClassVar[int]
    IN_BYTES_PER_SEC_FIELD_NUMBER: _ClassVar[int]
    PING_MS_FIELD_NUMBER: _ClassVar[int]
    PACKETS_DROPPED_PCT_FIELD_NUMBER: _ClassVar[int]
    PACKETS_WEIRD_SEQUENCE_PCT_FIELD_NUMBER: _ClassVar[int]
    PEAK_JITTER_USEC_FIELD_NUMBER: _ClassVar[int]
    out_packets_per_sec_x10: int
    out_bytes_per_sec: int
    in_packets_per_sec_x10: int
    in_bytes_per_sec: int
    ping_ms: int
    packets_dropped_pct: int
    packets_weird_sequence_pct: int
    peak_jitter_usec: int
    def __init__(self, out_packets_per_sec_x10: _Optional[int] = ..., out_bytes_per_sec: _Optional[int] = ..., in_packets_per_sec_x10: _Optional[int] = ..., in_bytes_per_sec: _Optional[int] = ..., ping_ms: _Optional[int] = ..., packets_dropped_pct: _Optional[int] = ..., packets_weird_sequence_pct: _Optional[int] = ..., peak_jitter_usec: _Optional[int] = ...) -> None: ...

class CMsgSteamDatagramLinkLifetimeStats(_message.Message):
    __slots__ = ("connected_seconds", "packets_sent", "kb_sent", "packets_recv", "kb_recv", "packets_recv_sequenced", "packets_recv_dropped", "packets_recv_out_of_order", "packets_recv_out_of_order_corrected", "packets_recv_duplicate", "packets_recv_lurch", "multipath_packets_recv_sequenced", "multipath_packets_recv_later", "multipath_send_enabled", "quality_histogram_100", "quality_histogram_99", "quality_histogram_97", "quality_histogram_95", "quality_histogram_90", "quality_histogram_75", "quality_histogram_50", "quality_histogram_1", "quality_histogram_dead", "quality_ntile_2nd", "quality_ntile_5th", "quality_ntile_25th", "quality_ntile_50th", "ping_histogram_25", "ping_histogram_50", "ping_histogram_75", "ping_histogram_100", "ping_histogram_125", "ping_histogram_150", "ping_histogram_200", "ping_histogram_300", "ping_histogram_max", "ping_ntile_5th", "ping_ntile_50th", "ping_ntile_75th", "ping_ntile_95th", "ping_ntile_98th", "jitter_histogram_negligible", "jitter_histogram_1", "jitter_histogram_2", "jitter_histogram_5", "jitter_histogram_10", "jitter_histogram_20")
    CONNECTED_SECONDS_FIELD_NUMBER: _ClassVar[int]
    PACKETS_SENT_FIELD_NUMBER: _ClassVar[int]
    KB_SENT_FIELD_NUMBER: _ClassVar[int]
    PACKETS_RECV_FIELD_NUMBER: _ClassVar[int]
    KB_RECV_FIELD_NUMBER: _ClassVar[int]
    PACKETS_RECV_SEQUENCED_FIELD_NUMBER: _ClassVar[int]
    PACKETS_RECV_DROPPED_FIELD_NUMBER: _ClassVar[int]
    PACKETS_RECV_OUT_OF_ORDER_FIELD_NUMBER: _ClassVar[int]
    PACKETS_RECV_OUT_OF_ORDER_CORRECTED_FIELD_NUMBER: _ClassVar[int]
    PACKETS_RECV_DUPLICATE_FIELD_NUMBER: _ClassVar[int]
    PACKETS_RECV_LURCH_FIELD_NUMBER: _ClassVar[int]
    MULTIPATH_PACKETS_RECV_SEQUENCED_FIELD_NUMBER: _ClassVar[int]
    MULTIPATH_PACKETS_RECV_LATER_FIELD_NUMBER: _ClassVar[int]
    MULTIPATH_SEND_ENABLED_FIELD_NUMBER: _ClassVar[int]
    QUALITY_HISTOGRAM_100_FIELD_NUMBER: _ClassVar[int]
    QUALITY_HISTOGRAM_99_FIELD_NUMBER: _ClassVar[int]
    QUALITY_HISTOGRAM_97_FIELD_NUMBER: _ClassVar[int]
    QUALITY_HISTOGRAM_95_FIELD_NUMBER: _ClassVar[int]
    QUALITY_HISTOGRAM_90_FIELD_NUMBER: _ClassVar[int]
    QUALITY_HISTOGRAM_75_FIELD_NUMBER: _ClassVar[int]
    QUALITY_HISTOGRAM_50_FIELD_NUMBER: _ClassVar[int]
    QUALITY_HISTOGRAM_1_FIELD_NUMBER: _ClassVar[int]
    QUALITY_HISTOGRAM_DEAD_FIELD_NUMBER: _ClassVar[int]
    QUALITY_NTILE_2ND_FIELD_NUMBER: _ClassVar[int]
    QUALITY_NTILE_5TH_FIELD_NUMBER: _ClassVar[int]
    QUALITY_NTILE_25TH_FIELD_NUMBER: _ClassVar[int]
    QUALITY_NTILE_50TH_FIELD_NUMBER: _ClassVar[int]
    PING_HISTOGRAM_25_FIELD_NUMBER: _ClassVar[int]
    PING_HISTOGRAM_50_FIELD_NUMBER: _ClassVar[int]
    PING_HISTOGRAM_75_FIELD_NUMBER: _ClassVar[int]
    PING_HISTOGRAM_100_FIELD_NUMBER: _ClassVar[int]
    PING_HISTOGRAM_125_FIELD_NUMBER: _ClassVar[int]
    PING_HISTOGRAM_150_FIELD_NUMBER: _ClassVar[int]
    PING_HISTOGRAM_200_FIELD_NUMBER: _ClassVar[int]
    PING_HISTOGRAM_300_FIELD_NUMBER: _ClassVar[int]
    PING_HISTOGRAM_MAX_FIELD_NUMBER: _ClassVar[int]
    PING_NTILE_5TH_FIELD_NUMBER: _ClassVar[int]
    PING_NTILE_50TH_FIELD_NUMBER: _ClassVar[int]
    PING_NTILE_75TH_FIELD_NUMBER: _ClassVar[int]
    PING_NTILE_95TH_FIELD_NUMBER: _ClassVar[int]
    PING_NTILE_98TH_FIELD_NUMBER: _ClassVar[int]
    JITTER_HISTOGRAM_NEGLIGIBLE_FIELD_NUMBER: _ClassVar[int]
    JITTER_HISTOGRAM_1_FIELD_NUMBER: _ClassVar[int]
    JITTER_HISTOGRAM_2_FIELD_NUMBER: _ClassVar[int]
    JITTER_HISTOGRAM_5_FIELD_NUMBER: _ClassVar[int]
    JITTER_HISTOGRAM_10_FIELD_NUMBER: _ClassVar[int]
    JITTER_HISTOGRAM_20_FIELD_NUMBER: _ClassVar[int]
    connected_seconds: int
    packets_sent: int
    kb_sent: int
    packets_recv: int
    kb_recv: int
    packets_recv_sequenced: int
    packets_recv_dropped: int
    packets_recv_out_of_order: int
    packets_recv_out_of_order_corrected: int
    packets_recv_duplicate: int
    packets_recv_lurch: int
    multipath_packets_recv_sequenced: _containers.RepeatedScalarFieldContainer[int]
    multipath_packets_recv_later: _containers.RepeatedScalarFieldContainer[int]
    multipath_send_enabled: int
    quality_histogram_100: int
    quality_histogram_99: int
    quality_histogram_97: int
    quality_histogram_95: int
    quality_histogram_90: int
    quality_histogram_75: int
    quality_histogram_50: int
    quality_histogram_1: int
    quality_histogram_dead: int
    quality_ntile_2nd: int
    quality_ntile_5th: int
    quality_ntile_25th: int
    quality_ntile_50th: int
    ping_histogram_25: int
    ping_histogram_50: int
    ping_histogram_75: int
    ping_histogram_100: int
    ping_histogram_125: int
    ping_histogram_150: int
    ping_histogram_200: int
    ping_histogram_300: int
    ping_histogram_max: int
    ping_ntile_5th: int
    ping_ntile_50th: int
    ping_ntile_75th: int
    ping_ntile_95th: int
    ping_ntile_98th: int
    jitter_histogram_negligible: int
    jitter_histogram_1: int
    jitter_histogram_2: int
    jitter_histogram_5: int
    jitter_histogram_10: int
    jitter_histogram_20: int
    def __init__(self, connected_seconds: _Optional[int] = ..., packets_sent: _Optional[int] = ..., kb_sent: _Optional[int] = ..., packets_recv: _Optional[int] = ..., kb_recv: _Optional[int] = ..., packets_recv_sequenced: _Optional[int] = ..., packets_recv_dropped: _Optional[int] = ..., packets_recv_out_of_order: _Optional[int] = ..., packets_recv_out_of_order_corrected: _Optional[int] = ..., packets_recv_duplicate: _Optional[int] = ..., packets_recv_lurch: _Optional[int] = ..., multipath_packets_recv_sequenced: _Optional[_Iterable[int]] = ..., multipath_packets_recv_later: _Optional[_Iterable[int]] = ..., multipath_send_enabled: _Optional[int] = ..., quality_histogram_100: _Optional[int] = ..., quality_histogram_99: _Optional[int] = ..., quality_histogram_97: _Optional[int] = ..., quality_histogram_95: _Optional[int] = ..., quality_histogram_90: _Optional[int] = ..., quality_histogram_75: _Optional[int] = ..., quality_histogram_50: _Optional[int] = ..., quality_histogram_1: _Optional[int] = ..., quality_histogram_dead: _Optional[int] = ..., quality_ntile_2nd: _Optional[int] = ..., quality_ntile_5th: _Optional[int] = ..., quality_ntile_25th: _Optional[int] = ..., quality_ntile_50th: _Optional[int] = ..., ping_histogram_25: _Optional[int] = ..., ping_histogram_50: _Optional[int] = ..., ping_histogram_75: _Optional[int] = ..., ping_histogram_100: _Optional[int] = ..., ping_histogram_125: _Optional[int] = ..., ping_histogram_150: _Optional[int] = ..., ping_histogram_200: _Optional[int] = ..., ping_histogram_300: _Optional[int] = ..., ping_histogram_max: _Optional[int] = ..., ping_ntile_5th: _Optional[int] = ..., ping_ntile_50th: _Optional[int] = ..., ping_ntile_75th: _Optional[int] = ..., ping_ntile_95th: _Optional[int] = ..., ping_ntile_98th: _Optional[int] = ..., jitter_histogram_negligible: _Optional[int] = ..., jitter_histogram_1: _Optional[int] = ..., jitter_histogram_2: _Optional[int] = ..., jitter_histogram_5: _Optional[int] = ..., jitter_histogram_10: _Optional[int] = ..., jitter_histogram_20: _Optional[int] = ...) -> None: ...

class CMsgSteamDatagramConnectionQuality(_message.Message):
    __slots__ = ("instantaneous", "lifetime")
    INSTANTANEOUS_FIELD_NUMBER: _ClassVar[int]
    LIFETIME_FIELD_NUMBER: _ClassVar[int]
    instantaneous: CMsgSteamDatagramLinkInstantaneousStats
    lifetime: CMsgSteamDatagramLinkLifetimeStats
    def __init__(self, instantaneous: _Optional[_Union[CMsgSteamDatagramLinkInstantaneousStats, _Mapping]] = ..., lifetime: _Optional[_Union[CMsgSteamDatagramLinkLifetimeStats, _Mapping]] = ...) -> None: ...

class CMsgICECandidate(_message.Message):
    __slots__ = ("candidate",)
    CANDIDATE_FIELD_NUMBER: _ClassVar[int]
    candidate: str
    def __init__(self, candidate: _Optional[str] = ...) -> None: ...

class CMsgICERendezvous(_message.Message):
    __slots__ = ("auth", "add_candidate")
    class Auth(_message.Message):
        __slots__ = ("pwd_frag",)
        PWD_FRAG_FIELD_NUMBER: _ClassVar[int]
        pwd_frag: str
        def __init__(self, pwd_frag: _Optional[str] = ...) -> None: ...
    AUTH_FIELD_NUMBER: _ClassVar[int]
    ADD_CANDIDATE_FIELD_NUMBER: _ClassVar[int]
    auth: CMsgICERendezvous.Auth
    add_candidate: CMsgICECandidate
    def __init__(self, auth: _Optional[_Union[CMsgICERendezvous.Auth, _Mapping]] = ..., add_candidate: _Optional[_Union[CMsgICECandidate, _Mapping]] = ...) -> None: ...

class CMsgSteamNetworkingP2PRendezvous(_message.Message):
    __slots__ = ("from_identity", "from_connection_id", "to_identity", "to_connection_id", "sdr_routes", "ack_peer_routes_revision", "ice_enabled", "hosted_server_ticket", "connect_request", "connect_ok", "connection_closed", "ack_reliable_msg", "first_reliable_msg", "reliable_messages", "application_messages")
    class ConnectRequest(_message.Message):
        __slots__ = ("crypt", "cert", "to_virtual_port", "from_virtual_port", "from_fakeip")
        CRYPT_FIELD_NUMBER: _ClassVar[int]
        CERT_FIELD_NUMBER: _ClassVar[int]
        TO_VIRTUAL_PORT_FIELD_NUMBER: _ClassVar[int]
        FROM_VIRTUAL_PORT_FIELD_NUMBER: _ClassVar[int]
        FROM_FAKEIP_FIELD_NUMBER: _ClassVar[int]
        crypt: CMsgSteamDatagramSessionCryptInfoSigned
        cert: _steamnetworkingsockets_messages_certs_pb2.CMsgSteamDatagramCertificateSigned
        to_virtual_port: int
        from_virtual_port: int
        from_fakeip: str
        def __init__(self, crypt: _Optional[_Union[CMsgSteamDatagramSessionCryptInfoSigned, _Mapping]] = ..., cert: _Optional[_Union[_steamnetworkingsockets_messages_certs_pb2.CMsgSteamDatagramCertificateSigned, _Mapping]] = ..., to_virtual_port: _Optional[int] = ..., from_virtual_port: _Optional[int] = ..., from_fakeip: _Optional[str] = ...) -> None: ...
    class ConnectOK(_message.Message):
        __slots__ = ("crypt", "cert")
        CRYPT_FIELD_NUMBER: _ClassVar[int]
        CERT_FIELD_NUMBER: _ClassVar[int]
        crypt: CMsgSteamDatagramSessionCryptInfoSigned
        cert: _steamnetworkingsockets_messages_certs_pb2.CMsgSteamDatagramCertificateSigned
        def __init__(self, crypt: _Optional[_Union[CMsgSteamDatagramSessionCryptInfoSigned, _Mapping]] = ..., cert: _Optional[_Union[_steamnetworkingsockets_messages_certs_pb2.CMsgSteamDatagramCertificateSigned, _Mapping]] = ...) -> None: ...
    class ConnectionClosed(_message.Message):
        __slots__ = ("debug", "reason_code")
        DEBUG_FIELD_NUMBER: _ClassVar[int]
        REASON_CODE_FIELD_NUMBER: _ClassVar[int]
        debug: str
        reason_code: int
        def __init__(self, debug: _Optional[str] = ..., reason_code: _Optional[int] = ...) -> None: ...
    class ReliableMessage(_message.Message):
        __slots__ = ("ice",)
        ICE_FIELD_NUMBER: _ClassVar[int]
        ice: CMsgICERendezvous
        def __init__(self, ice: _Optional[_Union[CMsgICERendezvous, _Mapping]] = ...) -> None: ...
    class ApplicationMessage(_message.Message):
        __slots__ = ("data", "msg_num", "flags", "lane_idx")
        DATA_FIELD_NUMBER: _ClassVar[int]
        MSG_NUM_FIELD_NUMBER: _ClassVar[int]
        FLAGS_FIELD_NUMBER: _ClassVar[int]
        LANE_IDX_FIELD_NUMBER: _ClassVar[int]
        data: bytes
        msg_num: int
        flags: int
        lane_idx: int
        def __init__(self, data: _Optional[bytes] = ..., msg_num: _Optional[int] = ..., flags: _Optional[int] = ..., lane_idx: _Optional[int] = ...) -> None: ...
    FROM_IDENTITY_FIELD_NUMBER: _ClassVar[int]
    FROM_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    TO_IDENTITY_FIELD_NUMBER: _ClassVar[int]
    TO_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    SDR_ROUTES_FIELD_NUMBER: _ClassVar[int]
    ACK_PEER_ROUTES_REVISION_FIELD_NUMBER: _ClassVar[int]
    ICE_ENABLED_FIELD_NUMBER: _ClassVar[int]
    HOSTED_SERVER_TICKET_FIELD_NUMBER: _ClassVar[int]
    CONNECT_REQUEST_FIELD_NUMBER: _ClassVar[int]
    CONNECT_OK_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_CLOSED_FIELD_NUMBER: _ClassVar[int]
    ACK_RELIABLE_MSG_FIELD_NUMBER: _ClassVar[int]
    FIRST_RELIABLE_MSG_FIELD_NUMBER: _ClassVar[int]
    RELIABLE_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    APPLICATION_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    from_identity: str
    from_connection_id: int
    to_identity: str
    to_connection_id: int
    sdr_routes: bytes
    ack_peer_routes_revision: int
    ice_enabled: bool
    hosted_server_ticket: bytes
    connect_request: CMsgSteamNetworkingP2PRendezvous.ConnectRequest
    connect_ok: CMsgSteamNetworkingP2PRendezvous.ConnectOK
    connection_closed: CMsgSteamNetworkingP2PRendezvous.ConnectionClosed
    ack_reliable_msg: int
    first_reliable_msg: int
    reliable_messages: _containers.RepeatedCompositeFieldContainer[CMsgSteamNetworkingP2PRendezvous.ReliableMessage]
    application_messages: _containers.RepeatedCompositeFieldContainer[CMsgSteamNetworkingP2PRendezvous.ApplicationMessage]
    def __init__(self, from_identity: _Optional[str] = ..., from_connection_id: _Optional[int] = ..., to_identity: _Optional[str] = ..., to_connection_id: _Optional[int] = ..., sdr_routes: _Optional[bytes] = ..., ack_peer_routes_revision: _Optional[int] = ..., ice_enabled: bool = ..., hosted_server_ticket: _Optional[bytes] = ..., connect_request: _Optional[_Union[CMsgSteamNetworkingP2PRendezvous.ConnectRequest, _Mapping]] = ..., connect_ok: _Optional[_Union[CMsgSteamNetworkingP2PRendezvous.ConnectOK, _Mapping]] = ..., connection_closed: _Optional[_Union[CMsgSteamNetworkingP2PRendezvous.ConnectionClosed, _Mapping]] = ..., ack_reliable_msg: _Optional[int] = ..., first_reliable_msg: _Optional[int] = ..., reliable_messages: _Optional[_Iterable[_Union[CMsgSteamNetworkingP2PRendezvous.ReliableMessage, _Mapping]]] = ..., application_messages: _Optional[_Iterable[_Union[CMsgSteamNetworkingP2PRendezvous.ApplicationMessage, _Mapping]]] = ...) -> None: ...

class CMsgSteamNetworkingICESessionSummary(_message.Message):
    __slots__ = ("failure_reason_code", "local_candidate_types", "remote_candidate_types", "initial_route_kind", "initial_ping", "initial_score", "negotiation_ms", "best_route_kind", "best_ping", "best_score", "best_time", "selected_seconds", "user_settings", "ice_enable_var", "local_candidate_types_allowed")
    FAILURE_REASON_CODE_FIELD_NUMBER: _ClassVar[int]
    LOCAL_CANDIDATE_TYPES_FIELD_NUMBER: _ClassVar[int]
    REMOTE_CANDIDATE_TYPES_FIELD_NUMBER: _ClassVar[int]
    INITIAL_ROUTE_KIND_FIELD_NUMBER: _ClassVar[int]
    INITIAL_PING_FIELD_NUMBER: _ClassVar[int]
    INITIAL_SCORE_FIELD_NUMBER: _ClassVar[int]
    NEGOTIATION_MS_FIELD_NUMBER: _ClassVar[int]
    BEST_ROUTE_KIND_FIELD_NUMBER: _ClassVar[int]
    BEST_PING_FIELD_NUMBER: _ClassVar[int]
    BEST_SCORE_FIELD_NUMBER: _ClassVar[int]
    BEST_TIME_FIELD_NUMBER: _ClassVar[int]
    SELECTED_SECONDS_FIELD_NUMBER: _ClassVar[int]
    USER_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    ICE_ENABLE_VAR_FIELD_NUMBER: _ClassVar[int]
    LOCAL_CANDIDATE_TYPES_ALLOWED_FIELD_NUMBER: _ClassVar[int]
    failure_reason_code: int
    local_candidate_types: int
    remote_candidate_types: int
    initial_route_kind: int
    initial_ping: int
    initial_score: int
    negotiation_ms: int
    best_route_kind: int
    best_ping: int
    best_score: int
    best_time: int
    selected_seconds: int
    user_settings: int
    ice_enable_var: int
    local_candidate_types_allowed: int
    def __init__(self, failure_reason_code: _Optional[int] = ..., local_candidate_types: _Optional[int] = ..., remote_candidate_types: _Optional[int] = ..., initial_route_kind: _Optional[int] = ..., initial_ping: _Optional[int] = ..., initial_score: _Optional[int] = ..., negotiation_ms: _Optional[int] = ..., best_route_kind: _Optional[int] = ..., best_ping: _Optional[int] = ..., best_score: _Optional[int] = ..., best_time: _Optional[int] = ..., selected_seconds: _Optional[int] = ..., user_settings: _Optional[int] = ..., ice_enable_var: _Optional[int] = ..., local_candidate_types_allowed: _Optional[int] = ...) -> None: ...
