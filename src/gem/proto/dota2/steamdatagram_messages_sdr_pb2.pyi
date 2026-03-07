import steamnetworkingsockets_messages_certs_pb2 as _steamnetworkingsockets_messages_certs_pb2
import steamnetworkingsockets_messages_pb2 as _steamnetworkingsockets_messages_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ESteamDatagramMsgID(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_ESteamDatagramMsg_Invalid: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_RouterPingRequest: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_RouterPingReply: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_GameserverPingRequest: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_GameserverSessionRequest: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_GameserverSessionEstablished: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_NoSession: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_Diagnostic: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_DataClientToRouter: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_DataRouterToServer: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_DataServerToRouter: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_DataRouterToClient: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_Stats: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_ClientPingSampleRequest: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_ClientPingSampleReply: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_ClientToRouterSwitchedPrimary: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_RelayHealth: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_ConnectRequest: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_ConnectOK: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_ConnectionClosed: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_NoConnection: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_TicketDecryptRequest: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_TicketDecryptReply: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_P2PSessionRequest: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_P2PSessionEstablished: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_P2PStatsClient: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_P2PStatsRelay: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_P2PBadRoute: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_GameserverPingReply: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_LegacyGameserverRegistration: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_SetSecondaryAddressRequest: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_SetSecondaryAddressResult: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_RelayToRelayPingRequest: _ClassVar[ESteamDatagramMsgID]
    k_ESteamDatagramMsg_RelayToRelayPingReply: _ClassVar[ESteamDatagramMsgID]
k_ESteamDatagramMsg_Invalid: ESteamDatagramMsgID
k_ESteamDatagramMsg_RouterPingRequest: ESteamDatagramMsgID
k_ESteamDatagramMsg_RouterPingReply: ESteamDatagramMsgID
k_ESteamDatagramMsg_GameserverPingRequest: ESteamDatagramMsgID
k_ESteamDatagramMsg_GameserverSessionRequest: ESteamDatagramMsgID
k_ESteamDatagramMsg_GameserverSessionEstablished: ESteamDatagramMsgID
k_ESteamDatagramMsg_NoSession: ESteamDatagramMsgID
k_ESteamDatagramMsg_Diagnostic: ESteamDatagramMsgID
k_ESteamDatagramMsg_DataClientToRouter: ESteamDatagramMsgID
k_ESteamDatagramMsg_DataRouterToServer: ESteamDatagramMsgID
k_ESteamDatagramMsg_DataServerToRouter: ESteamDatagramMsgID
k_ESteamDatagramMsg_DataRouterToClient: ESteamDatagramMsgID
k_ESteamDatagramMsg_Stats: ESteamDatagramMsgID
k_ESteamDatagramMsg_ClientPingSampleRequest: ESteamDatagramMsgID
k_ESteamDatagramMsg_ClientPingSampleReply: ESteamDatagramMsgID
k_ESteamDatagramMsg_ClientToRouterSwitchedPrimary: ESteamDatagramMsgID
k_ESteamDatagramMsg_RelayHealth: ESteamDatagramMsgID
k_ESteamDatagramMsg_ConnectRequest: ESteamDatagramMsgID
k_ESteamDatagramMsg_ConnectOK: ESteamDatagramMsgID
k_ESteamDatagramMsg_ConnectionClosed: ESteamDatagramMsgID
k_ESteamDatagramMsg_NoConnection: ESteamDatagramMsgID
k_ESteamDatagramMsg_TicketDecryptRequest: ESteamDatagramMsgID
k_ESteamDatagramMsg_TicketDecryptReply: ESteamDatagramMsgID
k_ESteamDatagramMsg_P2PSessionRequest: ESteamDatagramMsgID
k_ESteamDatagramMsg_P2PSessionEstablished: ESteamDatagramMsgID
k_ESteamDatagramMsg_P2PStatsClient: ESteamDatagramMsgID
k_ESteamDatagramMsg_P2PStatsRelay: ESteamDatagramMsgID
k_ESteamDatagramMsg_P2PBadRoute: ESteamDatagramMsgID
k_ESteamDatagramMsg_GameserverPingReply: ESteamDatagramMsgID
k_ESteamDatagramMsg_LegacyGameserverRegistration: ESteamDatagramMsgID
k_ESteamDatagramMsg_SetSecondaryAddressRequest: ESteamDatagramMsgID
k_ESteamDatagramMsg_SetSecondaryAddressResult: ESteamDatagramMsgID
k_ESteamDatagramMsg_RelayToRelayPingRequest: ESteamDatagramMsgID
k_ESteamDatagramMsg_RelayToRelayPingReply: ESteamDatagramMsgID

class CMsgSteamNetworkingIPAddress(_message.Message):
    __slots__ = ("v4", "v6")
    V4_FIELD_NUMBER: _ClassVar[int]
    V6_FIELD_NUMBER: _ClassVar[int]
    v4: int
    v6: bytes
    def __init__(self, v4: _Optional[int] = ..., v6: _Optional[bytes] = ...) -> None: ...

class CMsgSteamDatagramSignedMessageGeneric(_message.Message):
    __slots__ = ("cert", "signed_data", "signature", "dummy_pad")
    CERT_FIELD_NUMBER: _ClassVar[int]
    SIGNED_DATA_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    DUMMY_PAD_FIELD_NUMBER: _ClassVar[int]
    cert: _steamnetworkingsockets_messages_certs_pb2.CMsgSteamDatagramCertificateSigned
    signed_data: bytes
    signature: bytes
    dummy_pad: bytes
    def __init__(self, cert: _Optional[_Union[_steamnetworkingsockets_messages_certs_pb2.CMsgSteamDatagramCertificateSigned, _Mapping]] = ..., signed_data: _Optional[bytes] = ..., signature: _Optional[bytes] = ..., dummy_pad: _Optional[bytes] = ...) -> None: ...

class CMsgSteamDatagramRouterPingReply(_message.Message):
    __slots__ = ("client_timestamp", "latency_datacenter_ids", "latency_ping_ms", "latency_datacenter_ids_p2p", "latency_ping_ms_p2p", "your_public_ip", "your_public_port", "server_time", "challenge", "seconds_until_shutdown", "client_cookie", "recv_tos", "echo_sent_tos", "sent_tos", "echo_request_reply_tos", "scoring_penalty_relay_cluster", "flags", "route_exceptions", "alt_addresses", "dummy_pad", "dummy_varint")
    class Flags(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FLAG_MAYBE_MORE_DATA_CENTERS: _ClassVar[CMsgSteamDatagramRouterPingReply.Flags]
        FLAG_MAYBE_MORE_ALT_ADDRESSES: _ClassVar[CMsgSteamDatagramRouterPingReply.Flags]
    FLAG_MAYBE_MORE_DATA_CENTERS: CMsgSteamDatagramRouterPingReply.Flags
    FLAG_MAYBE_MORE_ALT_ADDRESSES: CMsgSteamDatagramRouterPingReply.Flags
    class RouteException(_message.Message):
        __slots__ = ("data_center_id", "flags", "penalty")
        DATA_CENTER_ID_FIELD_NUMBER: _ClassVar[int]
        FLAGS_FIELD_NUMBER: _ClassVar[int]
        PENALTY_FIELD_NUMBER: _ClassVar[int]
        data_center_id: int
        flags: int
        penalty: int
        def __init__(self, data_center_id: _Optional[int] = ..., flags: _Optional[int] = ..., penalty: _Optional[int] = ...) -> None: ...
    class AltAddress(_message.Message):
        __slots__ = ("ipv4", "port", "penalty", "protocol", "id")
        class Protocol(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            DefaultProtocol: _ClassVar[CMsgSteamDatagramRouterPingReply.AltAddress.Protocol]
        DefaultProtocol: CMsgSteamDatagramRouterPingReply.AltAddress.Protocol
        IPV4_FIELD_NUMBER: _ClassVar[int]
        PORT_FIELD_NUMBER: _ClassVar[int]
        PENALTY_FIELD_NUMBER: _ClassVar[int]
        PROTOCOL_FIELD_NUMBER: _ClassVar[int]
        ID_FIELD_NUMBER: _ClassVar[int]
        ipv4: int
        port: int
        penalty: int
        protocol: CMsgSteamDatagramRouterPingReply.AltAddress.Protocol
        id: str
        def __init__(self, ipv4: _Optional[int] = ..., port: _Optional[int] = ..., penalty: _Optional[int] = ..., protocol: _Optional[_Union[CMsgSteamDatagramRouterPingReply.AltAddress.Protocol, str]] = ..., id: _Optional[str] = ...) -> None: ...
    CLIENT_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LATENCY_DATACENTER_IDS_FIELD_NUMBER: _ClassVar[int]
    LATENCY_PING_MS_FIELD_NUMBER: _ClassVar[int]
    LATENCY_DATACENTER_IDS_P2P_FIELD_NUMBER: _ClassVar[int]
    LATENCY_PING_MS_P2P_FIELD_NUMBER: _ClassVar[int]
    YOUR_PUBLIC_IP_FIELD_NUMBER: _ClassVar[int]
    YOUR_PUBLIC_PORT_FIELD_NUMBER: _ClassVar[int]
    SERVER_TIME_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    SECONDS_UNTIL_SHUTDOWN_FIELD_NUMBER: _ClassVar[int]
    CLIENT_COOKIE_FIELD_NUMBER: _ClassVar[int]
    RECV_TOS_FIELD_NUMBER: _ClassVar[int]
    ECHO_SENT_TOS_FIELD_NUMBER: _ClassVar[int]
    SENT_TOS_FIELD_NUMBER: _ClassVar[int]
    ECHO_REQUEST_REPLY_TOS_FIELD_NUMBER: _ClassVar[int]
    SCORING_PENALTY_RELAY_CLUSTER_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    ROUTE_EXCEPTIONS_FIELD_NUMBER: _ClassVar[int]
    ALT_ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    DUMMY_PAD_FIELD_NUMBER: _ClassVar[int]
    DUMMY_VARINT_FIELD_NUMBER: _ClassVar[int]
    client_timestamp: int
    latency_datacenter_ids: _containers.RepeatedScalarFieldContainer[int]
    latency_ping_ms: _containers.RepeatedScalarFieldContainer[int]
    latency_datacenter_ids_p2p: _containers.RepeatedScalarFieldContainer[int]
    latency_ping_ms_p2p: _containers.RepeatedScalarFieldContainer[int]
    your_public_ip: int
    your_public_port: int
    server_time: int
    challenge: int
    seconds_until_shutdown: int
    client_cookie: int
    recv_tos: int
    echo_sent_tos: int
    sent_tos: int
    echo_request_reply_tos: int
    scoring_penalty_relay_cluster: int
    flags: int
    route_exceptions: _containers.RepeatedCompositeFieldContainer[CMsgSteamDatagramRouterPingReply.RouteException]
    alt_addresses: _containers.RepeatedCompositeFieldContainer[CMsgSteamDatagramRouterPingReply.AltAddress]
    dummy_pad: bytes
    dummy_varint: int
    def __init__(self, client_timestamp: _Optional[int] = ..., latency_datacenter_ids: _Optional[_Iterable[int]] = ..., latency_ping_ms: _Optional[_Iterable[int]] = ..., latency_datacenter_ids_p2p: _Optional[_Iterable[int]] = ..., latency_ping_ms_p2p: _Optional[_Iterable[int]] = ..., your_public_ip: _Optional[int] = ..., your_public_port: _Optional[int] = ..., server_time: _Optional[int] = ..., challenge: _Optional[int] = ..., seconds_until_shutdown: _Optional[int] = ..., client_cookie: _Optional[int] = ..., recv_tos: _Optional[int] = ..., echo_sent_tos: _Optional[int] = ..., sent_tos: _Optional[int] = ..., echo_request_reply_tos: _Optional[int] = ..., scoring_penalty_relay_cluster: _Optional[int] = ..., flags: _Optional[int] = ..., route_exceptions: _Optional[_Iterable[_Union[CMsgSteamDatagramRouterPingReply.RouteException, _Mapping]]] = ..., alt_addresses: _Optional[_Iterable[_Union[CMsgSteamDatagramRouterPingReply.AltAddress, _Mapping]]] = ..., dummy_pad: _Optional[bytes] = ..., dummy_varint: _Optional[int] = ...) -> None: ...

class CMsgSteamDatagramGameserverPingRequestBody(_message.Message):
    __slots__ = ("relay_popid", "your_public_ip", "your_public_port", "relay_unix_time", "routing_secret", "my_ips", "echo")
    RELAY_POPID_FIELD_NUMBER: _ClassVar[int]
    YOUR_PUBLIC_IP_FIELD_NUMBER: _ClassVar[int]
    YOUR_PUBLIC_PORT_FIELD_NUMBER: _ClassVar[int]
    RELAY_UNIX_TIME_FIELD_NUMBER: _ClassVar[int]
    ROUTING_SECRET_FIELD_NUMBER: _ClassVar[int]
    MY_IPS_FIELD_NUMBER: _ClassVar[int]
    ECHO_FIELD_NUMBER: _ClassVar[int]
    relay_popid: int
    your_public_ip: CMsgSteamNetworkingIPAddress
    your_public_port: int
    relay_unix_time: int
    routing_secret: int
    my_ips: _containers.RepeatedCompositeFieldContainer[CMsgSteamNetworkingIPAddress]
    echo: bytes
    def __init__(self, relay_popid: _Optional[int] = ..., your_public_ip: _Optional[_Union[CMsgSteamNetworkingIPAddress, _Mapping]] = ..., your_public_port: _Optional[int] = ..., relay_unix_time: _Optional[int] = ..., routing_secret: _Optional[int] = ..., my_ips: _Optional[_Iterable[_Union[CMsgSteamNetworkingIPAddress, _Mapping]]] = ..., echo: _Optional[bytes] = ...) -> None: ...

class CMsgSteamDatagramGameserverPingRequestEnvelope(_message.Message):
    __slots__ = ("cert", "signed_data", "signature", "legacy_your_public_ip", "legacy_your_public_port", "legacy_relay_unix_time", "legacy_challenge", "legacy_router_timestamp", "dummy_pad")
    CERT_FIELD_NUMBER: _ClassVar[int]
    SIGNED_DATA_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    LEGACY_YOUR_PUBLIC_IP_FIELD_NUMBER: _ClassVar[int]
    LEGACY_YOUR_PUBLIC_PORT_FIELD_NUMBER: _ClassVar[int]
    LEGACY_RELAY_UNIX_TIME_FIELD_NUMBER: _ClassVar[int]
    LEGACY_CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    LEGACY_ROUTER_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DUMMY_PAD_FIELD_NUMBER: _ClassVar[int]
    cert: _steamnetworkingsockets_messages_certs_pb2.CMsgSteamDatagramCertificateSigned
    signed_data: bytes
    signature: bytes
    legacy_your_public_ip: int
    legacy_your_public_port: int
    legacy_relay_unix_time: int
    legacy_challenge: int
    legacy_router_timestamp: int
    dummy_pad: bytes
    def __init__(self, cert: _Optional[_Union[_steamnetworkingsockets_messages_certs_pb2.CMsgSteamDatagramCertificateSigned, _Mapping]] = ..., signed_data: _Optional[bytes] = ..., signature: _Optional[bytes] = ..., legacy_your_public_ip: _Optional[int] = ..., legacy_your_public_port: _Optional[int] = ..., legacy_relay_unix_time: _Optional[int] = ..., legacy_challenge: _Optional[int] = ..., legacy_router_timestamp: _Optional[int] = ..., dummy_pad: _Optional[bytes] = ...) -> None: ...

class CMsgSteamDatagramGameserverPingReplyData(_message.Message):
    __slots__ = ("echo_relay_unix_time", "echo", "legacy_challenge", "legacy_router_timestamp", "data_center_id", "appid", "protocol_version", "build", "network_config_version", "my_unix_time", "routing_blob")
    ECHO_RELAY_UNIX_TIME_FIELD_NUMBER: _ClassVar[int]
    ECHO_FIELD_NUMBER: _ClassVar[int]
    LEGACY_CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    LEGACY_ROUTER_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DATA_CENTER_ID_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_VERSION_FIELD_NUMBER: _ClassVar[int]
    BUILD_FIELD_NUMBER: _ClassVar[int]
    NETWORK_CONFIG_VERSION_FIELD_NUMBER: _ClassVar[int]
    MY_UNIX_TIME_FIELD_NUMBER: _ClassVar[int]
    ROUTING_BLOB_FIELD_NUMBER: _ClassVar[int]
    echo_relay_unix_time: int
    echo: bytes
    legacy_challenge: int
    legacy_router_timestamp: int
    data_center_id: int
    appid: int
    protocol_version: int
    build: str
    network_config_version: int
    my_unix_time: int
    routing_blob: bytes
    def __init__(self, echo_relay_unix_time: _Optional[int] = ..., echo: _Optional[bytes] = ..., legacy_challenge: _Optional[int] = ..., legacy_router_timestamp: _Optional[int] = ..., data_center_id: _Optional[int] = ..., appid: _Optional[int] = ..., protocol_version: _Optional[int] = ..., build: _Optional[str] = ..., network_config_version: _Optional[int] = ..., my_unix_time: _Optional[int] = ..., routing_blob: _Optional[bytes] = ...) -> None: ...

class CMsgSteamDatagramNoSessionRelayToClient(_message.Message):
    __slots__ = ("connection_id", "your_public_ip", "your_public_port", "server_time", "challenge", "seconds_until_shutdown")
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    YOUR_PUBLIC_IP_FIELD_NUMBER: _ClassVar[int]
    YOUR_PUBLIC_PORT_FIELD_NUMBER: _ClassVar[int]
    SERVER_TIME_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    SECONDS_UNTIL_SHUTDOWN_FIELD_NUMBER: _ClassVar[int]
    connection_id: int
    your_public_ip: int
    your_public_port: int
    server_time: int
    challenge: int
    seconds_until_shutdown: int
    def __init__(self, connection_id: _Optional[int] = ..., your_public_ip: _Optional[int] = ..., your_public_port: _Optional[int] = ..., server_time: _Optional[int] = ..., challenge: _Optional[int] = ..., seconds_until_shutdown: _Optional[int] = ...) -> None: ...

class CMsgSteamDatagramNoSessionRelayToPeer(_message.Message):
    __slots__ = ("legacy_relay_session_id", "from_relay_session_id", "from_connection_id", "kludge_pad")
    LEGACY_RELAY_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    FROM_RELAY_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    FROM_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    KLUDGE_PAD_FIELD_NUMBER: _ClassVar[int]
    legacy_relay_session_id: int
    from_relay_session_id: int
    from_connection_id: int
    kludge_pad: int
    def __init__(self, legacy_relay_session_id: _Optional[int] = ..., from_relay_session_id: _Optional[int] = ..., from_connection_id: _Optional[int] = ..., kludge_pad: _Optional[int] = ...) -> None: ...

class CMsgTOSTreatment(_message.Message):
    __slots__ = ("l4s_detect", "up_ecn1", "down_dscp45")
    L4S_DETECT_FIELD_NUMBER: _ClassVar[int]
    UP_ECN1_FIELD_NUMBER: _ClassVar[int]
    DOWN_DSCP45_FIELD_NUMBER: _ClassVar[int]
    l4s_detect: str
    up_ecn1: str
    down_dscp45: str
    def __init__(self, l4s_detect: _Optional[str] = ..., up_ecn1: _Optional[str] = ..., down_dscp45: _Optional[str] = ...) -> None: ...

class CMsgSteamDatagramClientPingSampleRequest(_message.Message):
    __slots__ = ("connection_id",)
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    connection_id: int
    def __init__(self, connection_id: _Optional[int] = ...) -> None: ...

class CMsgSteamDatagramClientPingSampleReply(_message.Message):
    __slots__ = ("connection_id", "relay_override_active", "tos", "pops", "legacy_data_centers")
    class POP(_message.Message):
        __slots__ = ("pop_id", "default_front_ping_ms", "cluster_penalty", "alt_addresses", "default_e2e_ping_ms", "default_e2e_score", "p2p_via_peer_relay_pop_id", "best_dc_ping_ms", "best_dc_score", "best_dc_via_relay_pop_id", "default_dc_ping_ms", "default_dc_score", "default_dc_via_relay_pop_id", "test_dc_ping_ms", "test_dc_score", "test_dc_via_relay_pop_id")
        class AltAddress(_message.Message):
            __slots__ = ("id", "front_ping_ms", "penalty")
            ID_FIELD_NUMBER: _ClassVar[int]
            FRONT_PING_MS_FIELD_NUMBER: _ClassVar[int]
            PENALTY_FIELD_NUMBER: _ClassVar[int]
            id: str
            front_ping_ms: int
            penalty: int
            def __init__(self, id: _Optional[str] = ..., front_ping_ms: _Optional[int] = ..., penalty: _Optional[int] = ...) -> None: ...
        POP_ID_FIELD_NUMBER: _ClassVar[int]
        DEFAULT_FRONT_PING_MS_FIELD_NUMBER: _ClassVar[int]
        CLUSTER_PENALTY_FIELD_NUMBER: _ClassVar[int]
        ALT_ADDRESSES_FIELD_NUMBER: _ClassVar[int]
        DEFAULT_E2E_PING_MS_FIELD_NUMBER: _ClassVar[int]
        DEFAULT_E2E_SCORE_FIELD_NUMBER: _ClassVar[int]
        P2P_VIA_PEER_RELAY_POP_ID_FIELD_NUMBER: _ClassVar[int]
        BEST_DC_PING_MS_FIELD_NUMBER: _ClassVar[int]
        BEST_DC_SCORE_FIELD_NUMBER: _ClassVar[int]
        BEST_DC_VIA_RELAY_POP_ID_FIELD_NUMBER: _ClassVar[int]
        DEFAULT_DC_PING_MS_FIELD_NUMBER: _ClassVar[int]
        DEFAULT_DC_SCORE_FIELD_NUMBER: _ClassVar[int]
        DEFAULT_DC_VIA_RELAY_POP_ID_FIELD_NUMBER: _ClassVar[int]
        TEST_DC_PING_MS_FIELD_NUMBER: _ClassVar[int]
        TEST_DC_SCORE_FIELD_NUMBER: _ClassVar[int]
        TEST_DC_VIA_RELAY_POP_ID_FIELD_NUMBER: _ClassVar[int]
        pop_id: int
        default_front_ping_ms: int
        cluster_penalty: int
        alt_addresses: _containers.RepeatedCompositeFieldContainer[CMsgSteamDatagramClientPingSampleReply.POP.AltAddress]
        default_e2e_ping_ms: int
        default_e2e_score: int
        p2p_via_peer_relay_pop_id: int
        best_dc_ping_ms: int
        best_dc_score: int
        best_dc_via_relay_pop_id: int
        default_dc_ping_ms: int
        default_dc_score: int
        default_dc_via_relay_pop_id: int
        test_dc_ping_ms: int
        test_dc_score: int
        test_dc_via_relay_pop_id: int
        def __init__(self, pop_id: _Optional[int] = ..., default_front_ping_ms: _Optional[int] = ..., cluster_penalty: _Optional[int] = ..., alt_addresses: _Optional[_Iterable[_Union[CMsgSteamDatagramClientPingSampleReply.POP.AltAddress, _Mapping]]] = ..., default_e2e_ping_ms: _Optional[int] = ..., default_e2e_score: _Optional[int] = ..., p2p_via_peer_relay_pop_id: _Optional[int] = ..., best_dc_ping_ms: _Optional[int] = ..., best_dc_score: _Optional[int] = ..., best_dc_via_relay_pop_id: _Optional[int] = ..., default_dc_ping_ms: _Optional[int] = ..., default_dc_score: _Optional[int] = ..., default_dc_via_relay_pop_id: _Optional[int] = ..., test_dc_ping_ms: _Optional[int] = ..., test_dc_score: _Optional[int] = ..., test_dc_via_relay_pop_id: _Optional[int] = ...) -> None: ...
    class LegacyDataCenter(_message.Message):
        __slots__ = ("data_center_id", "best_dc_via_relay_pop_id", "best_dc_ping_ms")
        DATA_CENTER_ID_FIELD_NUMBER: _ClassVar[int]
        BEST_DC_VIA_RELAY_POP_ID_FIELD_NUMBER: _ClassVar[int]
        BEST_DC_PING_MS_FIELD_NUMBER: _ClassVar[int]
        data_center_id: int
        best_dc_via_relay_pop_id: int
        best_dc_ping_ms: int
        def __init__(self, data_center_id: _Optional[int] = ..., best_dc_via_relay_pop_id: _Optional[int] = ..., best_dc_ping_ms: _Optional[int] = ...) -> None: ...
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    RELAY_OVERRIDE_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    TOS_FIELD_NUMBER: _ClassVar[int]
    POPS_FIELD_NUMBER: _ClassVar[int]
    LEGACY_DATA_CENTERS_FIELD_NUMBER: _ClassVar[int]
    connection_id: int
    relay_override_active: bool
    tos: CMsgTOSTreatment
    pops: _containers.RepeatedCompositeFieldContainer[CMsgSteamDatagramClientPingSampleReply.POP]
    legacy_data_centers: _containers.RepeatedCompositeFieldContainer[CMsgSteamDatagramClientPingSampleReply.LegacyDataCenter]
    def __init__(self, connection_id: _Optional[int] = ..., relay_override_active: bool = ..., tos: _Optional[_Union[CMsgTOSTreatment, _Mapping]] = ..., pops: _Optional[_Iterable[_Union[CMsgSteamDatagramClientPingSampleReply.POP, _Mapping]]] = ..., legacy_data_centers: _Optional[_Iterable[_Union[CMsgSteamDatagramClientPingSampleReply.LegacyDataCenter, _Mapping]]] = ...) -> None: ...

class CMsgSteamDatagramClientSwitchedPrimary(_message.Message):
    __slots__ = ("connection_id", "from_ip", "from_port", "from_router_cluster", "from_active_time", "from_active_packets_recv", "from_dropped_reason", "gap_ms", "from_quality_now", "to_quality_now", "from_quality_then", "to_quality_then")
    class RouterQuality(_message.Message):
        __slots__ = ("score", "front_ping", "back_ping", "seconds_until_down")
        SCORE_FIELD_NUMBER: _ClassVar[int]
        FRONT_PING_FIELD_NUMBER: _ClassVar[int]
        BACK_PING_FIELD_NUMBER: _ClassVar[int]
        SECONDS_UNTIL_DOWN_FIELD_NUMBER: _ClassVar[int]
        score: int
        front_ping: int
        back_ping: int
        seconds_until_down: int
        def __init__(self, score: _Optional[int] = ..., front_ping: _Optional[int] = ..., back_ping: _Optional[int] = ..., seconds_until_down: _Optional[int] = ...) -> None: ...
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    FROM_IP_FIELD_NUMBER: _ClassVar[int]
    FROM_PORT_FIELD_NUMBER: _ClassVar[int]
    FROM_ROUTER_CLUSTER_FIELD_NUMBER: _ClassVar[int]
    FROM_ACTIVE_TIME_FIELD_NUMBER: _ClassVar[int]
    FROM_ACTIVE_PACKETS_RECV_FIELD_NUMBER: _ClassVar[int]
    FROM_DROPPED_REASON_FIELD_NUMBER: _ClassVar[int]
    GAP_MS_FIELD_NUMBER: _ClassVar[int]
    FROM_QUALITY_NOW_FIELD_NUMBER: _ClassVar[int]
    TO_QUALITY_NOW_FIELD_NUMBER: _ClassVar[int]
    FROM_QUALITY_THEN_FIELD_NUMBER: _ClassVar[int]
    TO_QUALITY_THEN_FIELD_NUMBER: _ClassVar[int]
    connection_id: int
    from_ip: int
    from_port: int
    from_router_cluster: int
    from_active_time: int
    from_active_packets_recv: int
    from_dropped_reason: str
    gap_ms: int
    from_quality_now: CMsgSteamDatagramClientSwitchedPrimary.RouterQuality
    to_quality_now: CMsgSteamDatagramClientSwitchedPrimary.RouterQuality
    from_quality_then: CMsgSteamDatagramClientSwitchedPrimary.RouterQuality
    to_quality_then: CMsgSteamDatagramClientSwitchedPrimary.RouterQuality
    def __init__(self, connection_id: _Optional[int] = ..., from_ip: _Optional[int] = ..., from_port: _Optional[int] = ..., from_router_cluster: _Optional[int] = ..., from_active_time: _Optional[int] = ..., from_active_packets_recv: _Optional[int] = ..., from_dropped_reason: _Optional[str] = ..., gap_ms: _Optional[int] = ..., from_quality_now: _Optional[_Union[CMsgSteamDatagramClientSwitchedPrimary.RouterQuality, _Mapping]] = ..., to_quality_now: _Optional[_Union[CMsgSteamDatagramClientSwitchedPrimary.RouterQuality, _Mapping]] = ..., from_quality_then: _Optional[_Union[CMsgSteamDatagramClientSwitchedPrimary.RouterQuality, _Mapping]] = ..., to_quality_then: _Optional[_Union[CMsgSteamDatagramClientSwitchedPrimary.RouterQuality, _Mapping]] = ...) -> None: ...

class CMsgSteamDatagramConnectRequest(_message.Message):
    __slots__ = ("connection_id", "my_timestamp", "ping_est_ms", "virtual_port", "gameserver_relay_session_id", "crypt", "cert", "routing_secret", "legacy_client_steam_id")
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    MY_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    PING_EST_MS_FIELD_NUMBER: _ClassVar[int]
    VIRTUAL_PORT_FIELD_NUMBER: _ClassVar[int]
    GAMESERVER_RELAY_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    CRYPT_FIELD_NUMBER: _ClassVar[int]
    CERT_FIELD_NUMBER: _ClassVar[int]
    ROUTING_SECRET_FIELD_NUMBER: _ClassVar[int]
    LEGACY_CLIENT_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    connection_id: int
    my_timestamp: int
    ping_est_ms: int
    virtual_port: int
    gameserver_relay_session_id: int
    crypt: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramSessionCryptInfoSigned
    cert: _steamnetworkingsockets_messages_certs_pb2.CMsgSteamDatagramCertificateSigned
    routing_secret: int
    legacy_client_steam_id: int
    def __init__(self, connection_id: _Optional[int] = ..., my_timestamp: _Optional[int] = ..., ping_est_ms: _Optional[int] = ..., virtual_port: _Optional[int] = ..., gameserver_relay_session_id: _Optional[int] = ..., crypt: _Optional[_Union[_steamnetworkingsockets_messages_pb2.CMsgSteamDatagramSessionCryptInfoSigned, _Mapping]] = ..., cert: _Optional[_Union[_steamnetworkingsockets_messages_certs_pb2.CMsgSteamDatagramCertificateSigned, _Mapping]] = ..., routing_secret: _Optional[int] = ..., legacy_client_steam_id: _Optional[int] = ...) -> None: ...

class CMsgSteamDatagramConnectOK(_message.Message):
    __slots__ = ("client_connection_id", "server_connection_id", "your_timestamp", "delay_time_usec", "gameserver_relay_session_id", "crypt", "cert")
    CLIENT_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    SERVER_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    YOUR_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DELAY_TIME_USEC_FIELD_NUMBER: _ClassVar[int]
    GAMESERVER_RELAY_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    CRYPT_FIELD_NUMBER: _ClassVar[int]
    CERT_FIELD_NUMBER: _ClassVar[int]
    client_connection_id: int
    server_connection_id: int
    your_timestamp: int
    delay_time_usec: int
    gameserver_relay_session_id: int
    crypt: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramSessionCryptInfoSigned
    cert: _steamnetworkingsockets_messages_certs_pb2.CMsgSteamDatagramCertificateSigned
    def __init__(self, client_connection_id: _Optional[int] = ..., server_connection_id: _Optional[int] = ..., your_timestamp: _Optional[int] = ..., delay_time_usec: _Optional[int] = ..., gameserver_relay_session_id: _Optional[int] = ..., crypt: _Optional[_Union[_steamnetworkingsockets_messages_pb2.CMsgSteamDatagramSessionCryptInfoSigned, _Mapping]] = ..., cert: _Optional[_Union[_steamnetworkingsockets_messages_certs_pb2.CMsgSteamDatagramCertificateSigned, _Mapping]] = ...) -> None: ...

class CMsgSteamNetworkingP2PSDRRoutingSummary(_message.Message):
    __slots__ = ("initial_ping", "initial_ping_front_local", "initial_ping_front_remote", "initial_score", "initial_pop_local", "initial_pop_remote", "best_ping", "best_ping_front_local", "best_ping_front_remote", "best_score", "best_pop_local", "best_pop_remote", "best_time", "negotiation_ms", "selected_seconds")
    INITIAL_PING_FIELD_NUMBER: _ClassVar[int]
    INITIAL_PING_FRONT_LOCAL_FIELD_NUMBER: _ClassVar[int]
    INITIAL_PING_FRONT_REMOTE_FIELD_NUMBER: _ClassVar[int]
    INITIAL_SCORE_FIELD_NUMBER: _ClassVar[int]
    INITIAL_POP_LOCAL_FIELD_NUMBER: _ClassVar[int]
    INITIAL_POP_REMOTE_FIELD_NUMBER: _ClassVar[int]
    BEST_PING_FIELD_NUMBER: _ClassVar[int]
    BEST_PING_FRONT_LOCAL_FIELD_NUMBER: _ClassVar[int]
    BEST_PING_FRONT_REMOTE_FIELD_NUMBER: _ClassVar[int]
    BEST_SCORE_FIELD_NUMBER: _ClassVar[int]
    BEST_POP_LOCAL_FIELD_NUMBER: _ClassVar[int]
    BEST_POP_REMOTE_FIELD_NUMBER: _ClassVar[int]
    BEST_TIME_FIELD_NUMBER: _ClassVar[int]
    NEGOTIATION_MS_FIELD_NUMBER: _ClassVar[int]
    SELECTED_SECONDS_FIELD_NUMBER: _ClassVar[int]
    initial_ping: int
    initial_ping_front_local: int
    initial_ping_front_remote: int
    initial_score: int
    initial_pop_local: int
    initial_pop_remote: int
    best_ping: int
    best_ping_front_local: int
    best_ping_front_remote: int
    best_score: int
    best_pop_local: int
    best_pop_remote: int
    best_time: int
    negotiation_ms: int
    selected_seconds: int
    def __init__(self, initial_ping: _Optional[int] = ..., initial_ping_front_local: _Optional[int] = ..., initial_ping_front_remote: _Optional[int] = ..., initial_score: _Optional[int] = ..., initial_pop_local: _Optional[int] = ..., initial_pop_remote: _Optional[int] = ..., best_ping: _Optional[int] = ..., best_ping_front_local: _Optional[int] = ..., best_ping_front_remote: _Optional[int] = ..., best_score: _Optional[int] = ..., best_pop_local: _Optional[int] = ..., best_pop_remote: _Optional[int] = ..., best_time: _Optional[int] = ..., negotiation_ms: _Optional[int] = ..., selected_seconds: _Optional[int] = ...) -> None: ...

class CMsgSteamDatagramP2PRoutingSummary(_message.Message):
    __slots__ = ("ice", "sdr")
    ICE_FIELD_NUMBER: _ClassVar[int]
    SDR_FIELD_NUMBER: _ClassVar[int]
    ice: _steamnetworkingsockets_messages_pb2.CMsgSteamNetworkingICESessionSummary
    sdr: CMsgSteamNetworkingP2PSDRRoutingSummary
    def __init__(self, ice: _Optional[_Union[_steamnetworkingsockets_messages_pb2.CMsgSteamNetworkingICESessionSummary, _Mapping]] = ..., sdr: _Optional[_Union[CMsgSteamNetworkingP2PSDRRoutingSummary, _Mapping]] = ...) -> None: ...

class CMsgSteamDatagramConnectionClosed(_message.Message):
    __slots__ = ("to_connection_id", "from_connection_id", "from_identity_string", "legacy_from_identity_binary", "legacy_from_steam_id", "legacy_gameserver_relay_session_id", "to_relay_session_id", "from_relay_session_id", "forward_target_relay_routing_token", "forward_target_revision", "relay_mode", "debug", "reason_code", "routing_secret", "not_primary_session", "not_primary_transport", "relay_override_active", "quality_relay", "quality_e2e", "p2p_routing_summary")
    class ERelayMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        None: _ClassVar[CMsgSteamDatagramConnectionClosed.ERelayMode]
        EndToEnd: _ClassVar[CMsgSteamDatagramConnectionClosed.ERelayMode]
        ClosedByPeer: _ClassVar[CMsgSteamDatagramConnectionClosed.ERelayMode]
    None: CMsgSteamDatagramConnectionClosed.ERelayMode
    EndToEnd: CMsgSteamDatagramConnectionClosed.ERelayMode
    ClosedByPeer: CMsgSteamDatagramConnectionClosed.ERelayMode
    TO_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    FROM_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    FROM_IDENTITY_STRING_FIELD_NUMBER: _ClassVar[int]
    LEGACY_FROM_IDENTITY_BINARY_FIELD_NUMBER: _ClassVar[int]
    LEGACY_FROM_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    LEGACY_GAMESERVER_RELAY_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    TO_RELAY_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    FROM_RELAY_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    FORWARD_TARGET_RELAY_ROUTING_TOKEN_FIELD_NUMBER: _ClassVar[int]
    FORWARD_TARGET_REVISION_FIELD_NUMBER: _ClassVar[int]
    RELAY_MODE_FIELD_NUMBER: _ClassVar[int]
    DEBUG_FIELD_NUMBER: _ClassVar[int]
    REASON_CODE_FIELD_NUMBER: _ClassVar[int]
    ROUTING_SECRET_FIELD_NUMBER: _ClassVar[int]
    NOT_PRIMARY_SESSION_FIELD_NUMBER: _ClassVar[int]
    NOT_PRIMARY_TRANSPORT_FIELD_NUMBER: _ClassVar[int]
    RELAY_OVERRIDE_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    QUALITY_RELAY_FIELD_NUMBER: _ClassVar[int]
    QUALITY_E2E_FIELD_NUMBER: _ClassVar[int]
    P2P_ROUTING_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    to_connection_id: int
    from_connection_id: int
    from_identity_string: str
    legacy_from_identity_binary: _steamnetworkingsockets_messages_certs_pb2.CMsgSteamNetworkingIdentityLegacyBinary
    legacy_from_steam_id: int
    legacy_gameserver_relay_session_id: int
    to_relay_session_id: int
    from_relay_session_id: int
    forward_target_relay_routing_token: bytes
    forward_target_revision: int
    relay_mode: CMsgSteamDatagramConnectionClosed.ERelayMode
    debug: str
    reason_code: int
    routing_secret: int
    not_primary_session: bool
    not_primary_transport: bool
    relay_override_active: bool
    quality_relay: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality
    quality_e2e: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality
    p2p_routing_summary: CMsgSteamDatagramP2PRoutingSummary
    def __init__(self, to_connection_id: _Optional[int] = ..., from_connection_id: _Optional[int] = ..., from_identity_string: _Optional[str] = ..., legacy_from_identity_binary: _Optional[_Union[_steamnetworkingsockets_messages_certs_pb2.CMsgSteamNetworkingIdentityLegacyBinary, _Mapping]] = ..., legacy_from_steam_id: _Optional[int] = ..., legacy_gameserver_relay_session_id: _Optional[int] = ..., to_relay_session_id: _Optional[int] = ..., from_relay_session_id: _Optional[int] = ..., forward_target_relay_routing_token: _Optional[bytes] = ..., forward_target_revision: _Optional[int] = ..., relay_mode: _Optional[_Union[CMsgSteamDatagramConnectionClosed.ERelayMode, str]] = ..., debug: _Optional[str] = ..., reason_code: _Optional[int] = ..., routing_secret: _Optional[int] = ..., not_primary_session: bool = ..., not_primary_transport: bool = ..., relay_override_active: bool = ..., quality_relay: _Optional[_Union[_steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality, _Mapping]] = ..., quality_e2e: _Optional[_Union[_steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality, _Mapping]] = ..., p2p_routing_summary: _Optional[_Union[CMsgSteamDatagramP2PRoutingSummary, _Mapping]] = ...) -> None: ...

class CMsgSteamDatagramNoConnection(_message.Message):
    __slots__ = ("to_connection_id", "from_connection_id", "legacy_gameserver_relay_session_id", "to_relay_session_id", "from_relay_session_id", "from_identity_string", "legacy_from_steam_id", "end_to_end", "not_primary_session", "not_primary_transport", "relay_override_active", "quality_relay", "quality_e2e", "p2p_routing_summary", "routing_secret", "dummy_pad")
    TO_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    FROM_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    LEGACY_GAMESERVER_RELAY_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    TO_RELAY_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    FROM_RELAY_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    FROM_IDENTITY_STRING_FIELD_NUMBER: _ClassVar[int]
    LEGACY_FROM_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    END_TO_END_FIELD_NUMBER: _ClassVar[int]
    NOT_PRIMARY_SESSION_FIELD_NUMBER: _ClassVar[int]
    NOT_PRIMARY_TRANSPORT_FIELD_NUMBER: _ClassVar[int]
    RELAY_OVERRIDE_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    QUALITY_RELAY_FIELD_NUMBER: _ClassVar[int]
    QUALITY_E2E_FIELD_NUMBER: _ClassVar[int]
    P2P_ROUTING_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    ROUTING_SECRET_FIELD_NUMBER: _ClassVar[int]
    DUMMY_PAD_FIELD_NUMBER: _ClassVar[int]
    to_connection_id: int
    from_connection_id: int
    legacy_gameserver_relay_session_id: int
    to_relay_session_id: int
    from_relay_session_id: int
    from_identity_string: str
    legacy_from_steam_id: int
    end_to_end: bool
    not_primary_session: bool
    not_primary_transport: bool
    relay_override_active: bool
    quality_relay: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality
    quality_e2e: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality
    p2p_routing_summary: CMsgSteamDatagramP2PRoutingSummary
    routing_secret: int
    dummy_pad: int
    def __init__(self, to_connection_id: _Optional[int] = ..., from_connection_id: _Optional[int] = ..., legacy_gameserver_relay_session_id: _Optional[int] = ..., to_relay_session_id: _Optional[int] = ..., from_relay_session_id: _Optional[int] = ..., from_identity_string: _Optional[str] = ..., legacy_from_steam_id: _Optional[int] = ..., end_to_end: bool = ..., not_primary_session: bool = ..., not_primary_transport: bool = ..., relay_override_active: bool = ..., quality_relay: _Optional[_Union[_steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality, _Mapping]] = ..., quality_e2e: _Optional[_Union[_steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality, _Mapping]] = ..., p2p_routing_summary: _Optional[_Union[CMsgSteamDatagramP2PRoutingSummary, _Mapping]] = ..., routing_secret: _Optional[int] = ..., dummy_pad: _Optional[int] = ...) -> None: ...

class CMsgSteamDatagramGameserverSessionRequest(_message.Message):
    __slots__ = ("ticket", "challenge_time", "challenge", "client_connection_id", "server_connection_id", "network_config_version", "protocol_version", "platform", "build", "dev_gameserver_identity", "dev_client_cert")
    TICKET_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_TIME_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    CLIENT_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    SERVER_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    NETWORK_CONFIG_VERSION_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_VERSION_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    BUILD_FIELD_NUMBER: _ClassVar[int]
    DEV_GAMESERVER_IDENTITY_FIELD_NUMBER: _ClassVar[int]
    DEV_CLIENT_CERT_FIELD_NUMBER: _ClassVar[int]
    ticket: bytes
    challenge_time: int
    challenge: int
    client_connection_id: int
    server_connection_id: int
    network_config_version: int
    protocol_version: int
    platform: str
    build: str
    dev_gameserver_identity: str
    dev_client_cert: _steamnetworkingsockets_messages_certs_pb2.CMsgSteamDatagramCertificateSigned
    def __init__(self, ticket: _Optional[bytes] = ..., challenge_time: _Optional[int] = ..., challenge: _Optional[int] = ..., client_connection_id: _Optional[int] = ..., server_connection_id: _Optional[int] = ..., network_config_version: _Optional[int] = ..., protocol_version: _Optional[int] = ..., platform: _Optional[str] = ..., build: _Optional[str] = ..., dev_gameserver_identity: _Optional[str] = ..., dev_client_cert: _Optional[_Union[_steamnetworkingsockets_messages_certs_pb2.CMsgSteamDatagramCertificateSigned, _Mapping]] = ...) -> None: ...

class CMsgSteamDatagramGameserverSessionEstablished(_message.Message):
    __slots__ = ("connection_id", "gameserver_identity_string", "seconds_until_shutdown", "seq_num_r2c", "dummy_legacy_identity_binary", "legacy_gameserver_steamid")
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    GAMESERVER_IDENTITY_STRING_FIELD_NUMBER: _ClassVar[int]
    SECONDS_UNTIL_SHUTDOWN_FIELD_NUMBER: _ClassVar[int]
    SEQ_NUM_R2C_FIELD_NUMBER: _ClassVar[int]
    DUMMY_LEGACY_IDENTITY_BINARY_FIELD_NUMBER: _ClassVar[int]
    LEGACY_GAMESERVER_STEAMID_FIELD_NUMBER: _ClassVar[int]
    connection_id: int
    gameserver_identity_string: str
    seconds_until_shutdown: int
    seq_num_r2c: int
    dummy_legacy_identity_binary: bytes
    legacy_gameserver_steamid: int
    def __init__(self, connection_id: _Optional[int] = ..., gameserver_identity_string: _Optional[str] = ..., seconds_until_shutdown: _Optional[int] = ..., seq_num_r2c: _Optional[int] = ..., dummy_legacy_identity_binary: _Optional[bytes] = ..., legacy_gameserver_steamid: _Optional[int] = ...) -> None: ...

class CMsgSteamDatagramConnectionStatsClientToRouter(_message.Message):
    __slots__ = ("quality_relay", "quality_e2e", "ack_relay", "legacy_ack_e2e", "flags", "client_connection_id", "seq_num_c2r", "seq_num_e2e")
    class Flags(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ACK_REQUEST_RELAY: _ClassVar[CMsgSteamDatagramConnectionStatsClientToRouter.Flags]
        ACK_REQUEST_E2E: _ClassVar[CMsgSteamDatagramConnectionStatsClientToRouter.Flags]
        ACK_REQUEST_IMMEDIATE: _ClassVar[CMsgSteamDatagramConnectionStatsClientToRouter.Flags]
        NOT_PRIMARY_SESSION: _ClassVar[CMsgSteamDatagramConnectionStatsClientToRouter.Flags]
        CLIENT_RELAY_OVERRIDE: _ClassVar[CMsgSteamDatagramConnectionStatsClientToRouter.Flags]
    ACK_REQUEST_RELAY: CMsgSteamDatagramConnectionStatsClientToRouter.Flags
    ACK_REQUEST_E2E: CMsgSteamDatagramConnectionStatsClientToRouter.Flags
    ACK_REQUEST_IMMEDIATE: CMsgSteamDatagramConnectionStatsClientToRouter.Flags
    NOT_PRIMARY_SESSION: CMsgSteamDatagramConnectionStatsClientToRouter.Flags
    CLIENT_RELAY_OVERRIDE: CMsgSteamDatagramConnectionStatsClientToRouter.Flags
    QUALITY_RELAY_FIELD_NUMBER: _ClassVar[int]
    QUALITY_E2E_FIELD_NUMBER: _ClassVar[int]
    ACK_RELAY_FIELD_NUMBER: _ClassVar[int]
    LEGACY_ACK_E2E_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    CLIENT_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    SEQ_NUM_C2R_FIELD_NUMBER: _ClassVar[int]
    SEQ_NUM_E2E_FIELD_NUMBER: _ClassVar[int]
    quality_relay: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality
    quality_e2e: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality
    ack_relay: _containers.RepeatedScalarFieldContainer[int]
    legacy_ack_e2e: _containers.RepeatedScalarFieldContainer[int]
    flags: int
    client_connection_id: int
    seq_num_c2r: int
    seq_num_e2e: int
    def __init__(self, quality_relay: _Optional[_Union[_steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality, _Mapping]] = ..., quality_e2e: _Optional[_Union[_steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality, _Mapping]] = ..., ack_relay: _Optional[_Iterable[int]] = ..., legacy_ack_e2e: _Optional[_Iterable[int]] = ..., flags: _Optional[int] = ..., client_connection_id: _Optional[int] = ..., seq_num_c2r: _Optional[int] = ..., seq_num_e2e: _Optional[int] = ...) -> None: ...

class CMsgSteamDatagramConnectionStatsRouterToClient(_message.Message):
    __slots__ = ("quality_relay", "quality_e2e", "seconds_until_shutdown", "migrate_request_ip", "migrate_request_port", "scoring_penalty_relay_cluster", "ack_relay", "legacy_ack_e2e", "flags", "client_connection_id", "seq_num_r2c", "seq_num_e2e")
    class Flags(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ACK_REQUEST_RELAY: _ClassVar[CMsgSteamDatagramConnectionStatsRouterToClient.Flags]
        ACK_REQUEST_E2E: _ClassVar[CMsgSteamDatagramConnectionStatsRouterToClient.Flags]
        ACK_REQUEST_IMMEDIATE: _ClassVar[CMsgSteamDatagramConnectionStatsRouterToClient.Flags]
    ACK_REQUEST_RELAY: CMsgSteamDatagramConnectionStatsRouterToClient.Flags
    ACK_REQUEST_E2E: CMsgSteamDatagramConnectionStatsRouterToClient.Flags
    ACK_REQUEST_IMMEDIATE: CMsgSteamDatagramConnectionStatsRouterToClient.Flags
    QUALITY_RELAY_FIELD_NUMBER: _ClassVar[int]
    QUALITY_E2E_FIELD_NUMBER: _ClassVar[int]
    SECONDS_UNTIL_SHUTDOWN_FIELD_NUMBER: _ClassVar[int]
    MIGRATE_REQUEST_IP_FIELD_NUMBER: _ClassVar[int]
    MIGRATE_REQUEST_PORT_FIELD_NUMBER: _ClassVar[int]
    SCORING_PENALTY_RELAY_CLUSTER_FIELD_NUMBER: _ClassVar[int]
    ACK_RELAY_FIELD_NUMBER: _ClassVar[int]
    LEGACY_ACK_E2E_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    CLIENT_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    SEQ_NUM_R2C_FIELD_NUMBER: _ClassVar[int]
    SEQ_NUM_E2E_FIELD_NUMBER: _ClassVar[int]
    quality_relay: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality
    quality_e2e: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality
    seconds_until_shutdown: int
    migrate_request_ip: int
    migrate_request_port: int
    scoring_penalty_relay_cluster: int
    ack_relay: _containers.RepeatedScalarFieldContainer[int]
    legacy_ack_e2e: _containers.RepeatedScalarFieldContainer[int]
    flags: int
    client_connection_id: int
    seq_num_r2c: int
    seq_num_e2e: int
    def __init__(self, quality_relay: _Optional[_Union[_steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality, _Mapping]] = ..., quality_e2e: _Optional[_Union[_steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality, _Mapping]] = ..., seconds_until_shutdown: _Optional[int] = ..., migrate_request_ip: _Optional[int] = ..., migrate_request_port: _Optional[int] = ..., scoring_penalty_relay_cluster: _Optional[int] = ..., ack_relay: _Optional[_Iterable[int]] = ..., legacy_ack_e2e: _Optional[_Iterable[int]] = ..., flags: _Optional[int] = ..., client_connection_id: _Optional[int] = ..., seq_num_r2c: _Optional[int] = ..., seq_num_e2e: _Optional[int] = ...) -> None: ...

class CMsgSteamDatagramConnectionStatsRouterToServer(_message.Message):
    __slots__ = ("quality_relay", "quality_e2e", "ack_relay", "legacy_ack_e2e", "flags", "seq_num_r2s", "seq_num_e2e", "client_identity_string", "legacy_client_steam_id", "relay_session_id", "client_connection_id", "server_connection_id", "routing_secret")
    class Flags(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ACK_REQUEST_RELAY: _ClassVar[CMsgSteamDatagramConnectionStatsRouterToServer.Flags]
        ACK_REQUEST_E2E: _ClassVar[CMsgSteamDatagramConnectionStatsRouterToServer.Flags]
        ACK_REQUEST_IMMEDIATE: _ClassVar[CMsgSteamDatagramConnectionStatsRouterToServer.Flags]
    ACK_REQUEST_RELAY: CMsgSteamDatagramConnectionStatsRouterToServer.Flags
    ACK_REQUEST_E2E: CMsgSteamDatagramConnectionStatsRouterToServer.Flags
    ACK_REQUEST_IMMEDIATE: CMsgSteamDatagramConnectionStatsRouterToServer.Flags
    QUALITY_RELAY_FIELD_NUMBER: _ClassVar[int]
    QUALITY_E2E_FIELD_NUMBER: _ClassVar[int]
    ACK_RELAY_FIELD_NUMBER: _ClassVar[int]
    LEGACY_ACK_E2E_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    SEQ_NUM_R2S_FIELD_NUMBER: _ClassVar[int]
    SEQ_NUM_E2E_FIELD_NUMBER: _ClassVar[int]
    CLIENT_IDENTITY_STRING_FIELD_NUMBER: _ClassVar[int]
    LEGACY_CLIENT_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    RELAY_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    SERVER_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    ROUTING_SECRET_FIELD_NUMBER: _ClassVar[int]
    quality_relay: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality
    quality_e2e: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality
    ack_relay: _containers.RepeatedScalarFieldContainer[int]
    legacy_ack_e2e: _containers.RepeatedScalarFieldContainer[int]
    flags: int
    seq_num_r2s: int
    seq_num_e2e: int
    client_identity_string: str
    legacy_client_steam_id: int
    relay_session_id: int
    client_connection_id: int
    server_connection_id: int
    routing_secret: int
    def __init__(self, quality_relay: _Optional[_Union[_steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality, _Mapping]] = ..., quality_e2e: _Optional[_Union[_steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality, _Mapping]] = ..., ack_relay: _Optional[_Iterable[int]] = ..., legacy_ack_e2e: _Optional[_Iterable[int]] = ..., flags: _Optional[int] = ..., seq_num_r2s: _Optional[int] = ..., seq_num_e2e: _Optional[int] = ..., client_identity_string: _Optional[str] = ..., legacy_client_steam_id: _Optional[int] = ..., relay_session_id: _Optional[int] = ..., client_connection_id: _Optional[int] = ..., server_connection_id: _Optional[int] = ..., routing_secret: _Optional[int] = ...) -> None: ...

class CMsgSteamDatagramConnectionStatsServerToRouter(_message.Message):
    __slots__ = ("quality_relay", "quality_e2e", "ack_relay", "legacy_ack_e2e", "flags", "seq_num_s2r", "seq_num_e2e", "relay_session_id", "client_connection_id", "server_connection_id")
    class Flags(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ACK_REQUEST_RELAY: _ClassVar[CMsgSteamDatagramConnectionStatsServerToRouter.Flags]
        ACK_REQUEST_E2E: _ClassVar[CMsgSteamDatagramConnectionStatsServerToRouter.Flags]
        ACK_REQUEST_IMMEDIATE: _ClassVar[CMsgSteamDatagramConnectionStatsServerToRouter.Flags]
    ACK_REQUEST_RELAY: CMsgSteamDatagramConnectionStatsServerToRouter.Flags
    ACK_REQUEST_E2E: CMsgSteamDatagramConnectionStatsServerToRouter.Flags
    ACK_REQUEST_IMMEDIATE: CMsgSteamDatagramConnectionStatsServerToRouter.Flags
    QUALITY_RELAY_FIELD_NUMBER: _ClassVar[int]
    QUALITY_E2E_FIELD_NUMBER: _ClassVar[int]
    ACK_RELAY_FIELD_NUMBER: _ClassVar[int]
    LEGACY_ACK_E2E_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    SEQ_NUM_S2R_FIELD_NUMBER: _ClassVar[int]
    SEQ_NUM_E2E_FIELD_NUMBER: _ClassVar[int]
    RELAY_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    SERVER_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    quality_relay: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality
    quality_e2e: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality
    ack_relay: _containers.RepeatedScalarFieldContainer[int]
    legacy_ack_e2e: _containers.RepeatedScalarFieldContainer[int]
    flags: int
    seq_num_s2r: int
    seq_num_e2e: int
    relay_session_id: int
    client_connection_id: int
    server_connection_id: int
    def __init__(self, quality_relay: _Optional[_Union[_steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality, _Mapping]] = ..., quality_e2e: _Optional[_Union[_steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality, _Mapping]] = ..., ack_relay: _Optional[_Iterable[int]] = ..., legacy_ack_e2e: _Optional[_Iterable[int]] = ..., flags: _Optional[int] = ..., seq_num_s2r: _Optional[int] = ..., seq_num_e2e: _Optional[int] = ..., relay_session_id: _Optional[int] = ..., client_connection_id: _Optional[int] = ..., server_connection_id: _Optional[int] = ...) -> None: ...

class CMsgSteamDatagramP2PSessionRequestBody(_message.Message):
    __slots__ = ("challenge_time", "challenge", "client_connection_id", "legacy_peer_steam_id", "peer_identity_string", "peer_connection_id", "encrypted_data", "encryption_your_public_key_lead_byte", "encryption_my_ephemeral_public_key", "protocol_version", "network_config_version", "platform", "build")
    class EncryptedData(_message.Message):
        __slots__ = ("peer_identity_string",)
        PEER_IDENTITY_STRING_FIELD_NUMBER: _ClassVar[int]
        peer_identity_string: str
        def __init__(self, peer_identity_string: _Optional[str] = ...) -> None: ...
    CHALLENGE_TIME_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    CLIENT_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    LEGACY_PEER_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    PEER_IDENTITY_STRING_FIELD_NUMBER: _ClassVar[int]
    PEER_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTED_DATA_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTION_YOUR_PUBLIC_KEY_LEAD_BYTE_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTION_MY_EPHEMERAL_PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_VERSION_FIELD_NUMBER: _ClassVar[int]
    NETWORK_CONFIG_VERSION_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    BUILD_FIELD_NUMBER: _ClassVar[int]
    challenge_time: int
    challenge: int
    client_connection_id: int
    legacy_peer_steam_id: int
    peer_identity_string: str
    peer_connection_id: int
    encrypted_data: bytes
    encryption_your_public_key_lead_byte: int
    encryption_my_ephemeral_public_key: bytes
    protocol_version: int
    network_config_version: int
    platform: str
    build: str
    def __init__(self, challenge_time: _Optional[int] = ..., challenge: _Optional[int] = ..., client_connection_id: _Optional[int] = ..., legacy_peer_steam_id: _Optional[int] = ..., peer_identity_string: _Optional[str] = ..., peer_connection_id: _Optional[int] = ..., encrypted_data: _Optional[bytes] = ..., encryption_your_public_key_lead_byte: _Optional[int] = ..., encryption_my_ephemeral_public_key: _Optional[bytes] = ..., protocol_version: _Optional[int] = ..., network_config_version: _Optional[int] = ..., platform: _Optional[str] = ..., build: _Optional[str] = ...) -> None: ...

class CMsgSteamDatagramP2PSessionRequest(_message.Message):
    __slots__ = ("cert", "body", "signature")
    CERT_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    cert: _steamnetworkingsockets_messages_certs_pb2.CMsgSteamDatagramCertificateSigned
    body: bytes
    signature: bytes
    def __init__(self, cert: _Optional[_Union[_steamnetworkingsockets_messages_certs_pb2.CMsgSteamDatagramCertificateSigned, _Mapping]] = ..., body: _Optional[bytes] = ..., signature: _Optional[bytes] = ...) -> None: ...

class CMsgSteamDatagramP2PSessionEstablished(_message.Message):
    __slots__ = ("connection_id", "seconds_until_shutdown", "relay_routing_token", "seq_num_r2c")
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    SECONDS_UNTIL_SHUTDOWN_FIELD_NUMBER: _ClassVar[int]
    RELAY_ROUTING_TOKEN_FIELD_NUMBER: _ClassVar[int]
    SEQ_NUM_R2C_FIELD_NUMBER: _ClassVar[int]
    connection_id: int
    seconds_until_shutdown: int
    relay_routing_token: bytes
    seq_num_r2c: int
    def __init__(self, connection_id: _Optional[int] = ..., seconds_until_shutdown: _Optional[int] = ..., relay_routing_token: _Optional[bytes] = ..., seq_num_r2c: _Optional[int] = ...) -> None: ...

class CMsgSteamDatagramConnectionStatsP2PClientToRouter(_message.Message):
    __slots__ = ("quality_relay", "quality_e2e", "p2p_routing_summary", "ack_relay", "legacy_ack_e2e", "flags", "forward_target_relay_routing_token", "forward_target_revision", "routes", "ack_peer_routes_revision", "connection_id", "seq_num_c2r", "seq_num_e2e")
    class Flags(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ACK_REQUEST_RELAY: _ClassVar[CMsgSteamDatagramConnectionStatsP2PClientToRouter.Flags]
        ACK_REQUEST_E2E: _ClassVar[CMsgSteamDatagramConnectionStatsP2PClientToRouter.Flags]
        ACK_REQUEST_IMMEDIATE: _ClassVar[CMsgSteamDatagramConnectionStatsP2PClientToRouter.Flags]
        NOT_PRIMARY_SESSION: _ClassVar[CMsgSteamDatagramConnectionStatsP2PClientToRouter.Flags]
        NOT_PRIMARY_TRANSPORT_E2E: _ClassVar[CMsgSteamDatagramConnectionStatsP2PClientToRouter.Flags]
        CLIENT_RELAY_OVERRIDE: _ClassVar[CMsgSteamDatagramConnectionStatsP2PClientToRouter.Flags]
    ACK_REQUEST_RELAY: CMsgSteamDatagramConnectionStatsP2PClientToRouter.Flags
    ACK_REQUEST_E2E: CMsgSteamDatagramConnectionStatsP2PClientToRouter.Flags
    ACK_REQUEST_IMMEDIATE: CMsgSteamDatagramConnectionStatsP2PClientToRouter.Flags
    NOT_PRIMARY_SESSION: CMsgSteamDatagramConnectionStatsP2PClientToRouter.Flags
    NOT_PRIMARY_TRANSPORT_E2E: CMsgSteamDatagramConnectionStatsP2PClientToRouter.Flags
    CLIENT_RELAY_OVERRIDE: CMsgSteamDatagramConnectionStatsP2PClientToRouter.Flags
    QUALITY_RELAY_FIELD_NUMBER: _ClassVar[int]
    QUALITY_E2E_FIELD_NUMBER: _ClassVar[int]
    P2P_ROUTING_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    ACK_RELAY_FIELD_NUMBER: _ClassVar[int]
    LEGACY_ACK_E2E_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    FORWARD_TARGET_RELAY_ROUTING_TOKEN_FIELD_NUMBER: _ClassVar[int]
    FORWARD_TARGET_REVISION_FIELD_NUMBER: _ClassVar[int]
    ROUTES_FIELD_NUMBER: _ClassVar[int]
    ACK_PEER_ROUTES_REVISION_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    SEQ_NUM_C2R_FIELD_NUMBER: _ClassVar[int]
    SEQ_NUM_E2E_FIELD_NUMBER: _ClassVar[int]
    quality_relay: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality
    quality_e2e: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality
    p2p_routing_summary: CMsgSteamDatagramP2PRoutingSummary
    ack_relay: _containers.RepeatedScalarFieldContainer[int]
    legacy_ack_e2e: _containers.RepeatedScalarFieldContainer[int]
    flags: int
    forward_target_relay_routing_token: bytes
    forward_target_revision: int
    routes: bytes
    ack_peer_routes_revision: int
    connection_id: int
    seq_num_c2r: int
    seq_num_e2e: int
    def __init__(self, quality_relay: _Optional[_Union[_steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality, _Mapping]] = ..., quality_e2e: _Optional[_Union[_steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality, _Mapping]] = ..., p2p_routing_summary: _Optional[_Union[CMsgSteamDatagramP2PRoutingSummary, _Mapping]] = ..., ack_relay: _Optional[_Iterable[int]] = ..., legacy_ack_e2e: _Optional[_Iterable[int]] = ..., flags: _Optional[int] = ..., forward_target_relay_routing_token: _Optional[bytes] = ..., forward_target_revision: _Optional[int] = ..., routes: _Optional[bytes] = ..., ack_peer_routes_revision: _Optional[int] = ..., connection_id: _Optional[int] = ..., seq_num_c2r: _Optional[int] = ..., seq_num_e2e: _Optional[int] = ...) -> None: ...

class CMsgSteamDatagramConnectionStatsP2PRouterToClient(_message.Message):
    __slots__ = ("quality_relay", "quality_e2e", "seconds_until_shutdown", "migrate_request_ip", "migrate_request_port", "scoring_penalty_relay_cluster", "ack_relay", "legacy_ack_e2e", "flags", "ack_forward_target_revision", "routes", "ack_peer_routes_revision", "connection_id", "seq_num_r2c", "seq_num_e2e")
    class Flags(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ACK_REQUEST_RELAY: _ClassVar[CMsgSteamDatagramConnectionStatsP2PRouterToClient.Flags]
        ACK_REQUEST_E2E: _ClassVar[CMsgSteamDatagramConnectionStatsP2PRouterToClient.Flags]
        ACK_REQUEST_IMMEDIATE: _ClassVar[CMsgSteamDatagramConnectionStatsP2PRouterToClient.Flags]
        NOT_PRIMARY_TRANSPORT_E2E: _ClassVar[CMsgSteamDatagramConnectionStatsP2PRouterToClient.Flags]
    ACK_REQUEST_RELAY: CMsgSteamDatagramConnectionStatsP2PRouterToClient.Flags
    ACK_REQUEST_E2E: CMsgSteamDatagramConnectionStatsP2PRouterToClient.Flags
    ACK_REQUEST_IMMEDIATE: CMsgSteamDatagramConnectionStatsP2PRouterToClient.Flags
    NOT_PRIMARY_TRANSPORT_E2E: CMsgSteamDatagramConnectionStatsP2PRouterToClient.Flags
    QUALITY_RELAY_FIELD_NUMBER: _ClassVar[int]
    QUALITY_E2E_FIELD_NUMBER: _ClassVar[int]
    SECONDS_UNTIL_SHUTDOWN_FIELD_NUMBER: _ClassVar[int]
    MIGRATE_REQUEST_IP_FIELD_NUMBER: _ClassVar[int]
    MIGRATE_REQUEST_PORT_FIELD_NUMBER: _ClassVar[int]
    SCORING_PENALTY_RELAY_CLUSTER_FIELD_NUMBER: _ClassVar[int]
    ACK_RELAY_FIELD_NUMBER: _ClassVar[int]
    LEGACY_ACK_E2E_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    ACK_FORWARD_TARGET_REVISION_FIELD_NUMBER: _ClassVar[int]
    ROUTES_FIELD_NUMBER: _ClassVar[int]
    ACK_PEER_ROUTES_REVISION_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    SEQ_NUM_R2C_FIELD_NUMBER: _ClassVar[int]
    SEQ_NUM_E2E_FIELD_NUMBER: _ClassVar[int]
    quality_relay: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality
    quality_e2e: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality
    seconds_until_shutdown: int
    migrate_request_ip: int
    migrate_request_port: int
    scoring_penalty_relay_cluster: int
    ack_relay: _containers.RepeatedScalarFieldContainer[int]
    legacy_ack_e2e: _containers.RepeatedScalarFieldContainer[int]
    flags: int
    ack_forward_target_revision: int
    routes: bytes
    ack_peer_routes_revision: int
    connection_id: int
    seq_num_r2c: int
    seq_num_e2e: int
    def __init__(self, quality_relay: _Optional[_Union[_steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality, _Mapping]] = ..., quality_e2e: _Optional[_Union[_steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality, _Mapping]] = ..., seconds_until_shutdown: _Optional[int] = ..., migrate_request_ip: _Optional[int] = ..., migrate_request_port: _Optional[int] = ..., scoring_penalty_relay_cluster: _Optional[int] = ..., ack_relay: _Optional[_Iterable[int]] = ..., legacy_ack_e2e: _Optional[_Iterable[int]] = ..., flags: _Optional[int] = ..., ack_forward_target_revision: _Optional[int] = ..., routes: _Optional[bytes] = ..., ack_peer_routes_revision: _Optional[int] = ..., connection_id: _Optional[int] = ..., seq_num_r2c: _Optional[int] = ..., seq_num_e2e: _Optional[int] = ...) -> None: ...

class CMsgSteamDatagramP2PBadRouteRouterToClient(_message.Message):
    __slots__ = ("connection_id", "failed_relay_routing_token", "ack_forward_target_revision", "kludge_pad")
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    FAILED_RELAY_ROUTING_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ACK_FORWARD_TARGET_REVISION_FIELD_NUMBER: _ClassVar[int]
    KLUDGE_PAD_FIELD_NUMBER: _ClassVar[int]
    connection_id: int
    failed_relay_routing_token: bytes
    ack_forward_target_revision: int
    kludge_pad: int
    def __init__(self, connection_id: _Optional[int] = ..., failed_relay_routing_token: _Optional[bytes] = ..., ack_forward_target_revision: _Optional[int] = ..., kludge_pad: _Optional[int] = ...) -> None: ...

class CMsgSteamDatagramP2PRoutes(_message.Message):
    __slots__ = ("relay_clusters", "routes", "revision")
    class RelayCluster(_message.Message):
        __slots__ = ("pop_id", "ping_ms", "score_penalty", "session_relay_routing_token")
        POP_ID_FIELD_NUMBER: _ClassVar[int]
        PING_MS_FIELD_NUMBER: _ClassVar[int]
        SCORE_PENALTY_FIELD_NUMBER: _ClassVar[int]
        SESSION_RELAY_ROUTING_TOKEN_FIELD_NUMBER: _ClassVar[int]
        pop_id: int
        ping_ms: int
        score_penalty: int
        session_relay_routing_token: bytes
        def __init__(self, pop_id: _Optional[int] = ..., ping_ms: _Optional[int] = ..., score_penalty: _Optional[int] = ..., session_relay_routing_token: _Optional[bytes] = ...) -> None: ...
    class Route(_message.Message):
        __slots__ = ("my_pop_id", "your_pop_id", "legacy_score", "interior_score")
        MY_POP_ID_FIELD_NUMBER: _ClassVar[int]
        YOUR_POP_ID_FIELD_NUMBER: _ClassVar[int]
        LEGACY_SCORE_FIELD_NUMBER: _ClassVar[int]
        INTERIOR_SCORE_FIELD_NUMBER: _ClassVar[int]
        my_pop_id: int
        your_pop_id: int
        legacy_score: int
        interior_score: int
        def __init__(self, my_pop_id: _Optional[int] = ..., your_pop_id: _Optional[int] = ..., legacy_score: _Optional[int] = ..., interior_score: _Optional[int] = ...) -> None: ...
    RELAY_CLUSTERS_FIELD_NUMBER: _ClassVar[int]
    ROUTES_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    relay_clusters: _containers.RepeatedCompositeFieldContainer[CMsgSteamDatagramP2PRoutes.RelayCluster]
    routes: _containers.RepeatedCompositeFieldContainer[CMsgSteamDatagramP2PRoutes.Route]
    revision: int
    def __init__(self, relay_clusters: _Optional[_Iterable[_Union[CMsgSteamDatagramP2PRoutes.RelayCluster, _Mapping]]] = ..., routes: _Optional[_Iterable[_Union[CMsgSteamDatagramP2PRoutes.Route, _Mapping]]] = ..., revision: _Optional[int] = ...) -> None: ...

class CMsgSteamDatagramSetSecondaryAddressRequest(_message.Message):
    __slots__ = ("client_main_ip", "client_main_port", "client_connection_id", "client_identity", "request_send_duplication", "kludge_pad")
    CLIENT_MAIN_IP_FIELD_NUMBER: _ClassVar[int]
    CLIENT_MAIN_PORT_FIELD_NUMBER: _ClassVar[int]
    CLIENT_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_IDENTITY_FIELD_NUMBER: _ClassVar[int]
    REQUEST_SEND_DUPLICATION_FIELD_NUMBER: _ClassVar[int]
    KLUDGE_PAD_FIELD_NUMBER: _ClassVar[int]
    client_main_ip: int
    client_main_port: int
    client_connection_id: int
    client_identity: str
    request_send_duplication: bool
    kludge_pad: bytes
    def __init__(self, client_main_ip: _Optional[int] = ..., client_main_port: _Optional[int] = ..., client_connection_id: _Optional[int] = ..., client_identity: _Optional[str] = ..., request_send_duplication: bool = ..., kludge_pad: _Optional[bytes] = ...) -> None: ...

class CMsgSteamDatagramSetSecondaryAddressResult(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...
