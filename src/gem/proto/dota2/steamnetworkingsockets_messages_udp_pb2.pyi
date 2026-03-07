from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

import steamnetworkingsockets_messages_certs_pb2 as _steamnetworkingsockets_messages_certs_pb2
import steamnetworkingsockets_messages_pb2 as _steamnetworkingsockets_messages_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class ESteamNetworkingUDPMsgID(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_ESteamNetworkingUDPMsg_ChallengeRequest: _ClassVar[ESteamNetworkingUDPMsgID]
    k_ESteamNetworkingUDPMsg_ChallengeReply: _ClassVar[ESteamNetworkingUDPMsgID]
    k_ESteamNetworkingUDPMsg_ConnectRequest: _ClassVar[ESteamNetworkingUDPMsgID]
    k_ESteamNetworkingUDPMsg_ConnectOK: _ClassVar[ESteamNetworkingUDPMsgID]
    k_ESteamNetworkingUDPMsg_ConnectionClosed: _ClassVar[ESteamNetworkingUDPMsgID]
    k_ESteamNetworkingUDPMsg_NoConnection: _ClassVar[ESteamNetworkingUDPMsgID]

k_ESteamNetworkingUDPMsg_ChallengeRequest: ESteamNetworkingUDPMsgID
k_ESteamNetworkingUDPMsg_ChallengeReply: ESteamNetworkingUDPMsgID
k_ESteamNetworkingUDPMsg_ConnectRequest: ESteamNetworkingUDPMsgID
k_ESteamNetworkingUDPMsg_ConnectOK: ESteamNetworkingUDPMsgID
k_ESteamNetworkingUDPMsg_ConnectionClosed: ESteamNetworkingUDPMsgID
k_ESteamNetworkingUDPMsg_NoConnection: ESteamNetworkingUDPMsgID

class CMsgSteamSockets_UDP_ChallengeRequest(_message.Message):
    __slots__ = ("connection_id", "my_timestamp", "protocol_version")
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    MY_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_VERSION_FIELD_NUMBER: _ClassVar[int]
    connection_id: int
    my_timestamp: int
    protocol_version: int
    def __init__(
        self,
        connection_id: int | None = ...,
        my_timestamp: int | None = ...,
        protocol_version: int | None = ...,
    ) -> None: ...

class CMsgSteamSockets_UDP_ChallengeReply(_message.Message):
    __slots__ = ("connection_id", "challenge", "your_timestamp", "protocol_version")
    CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    YOUR_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_VERSION_FIELD_NUMBER: _ClassVar[int]
    connection_id: int
    challenge: int
    your_timestamp: int
    protocol_version: int
    def __init__(
        self,
        connection_id: int | None = ...,
        challenge: int | None = ...,
        your_timestamp: int | None = ...,
        protocol_version: int | None = ...,
    ) -> None: ...

class CMsgSteamSockets_UDP_ConnectRequest(_message.Message):
    __slots__ = (
        "client_connection_id",
        "challenge",
        "my_timestamp",
        "ping_est_ms",
        "crypt",
        "cert",
        "legacy_protocol_version",
        "identity_string",
        "legacy_client_steam_id",
        "legacy_identity_binary",
    )
    CLIENT_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    MY_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    PING_EST_MS_FIELD_NUMBER: _ClassVar[int]
    CRYPT_FIELD_NUMBER: _ClassVar[int]
    CERT_FIELD_NUMBER: _ClassVar[int]
    LEGACY_PROTOCOL_VERSION_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_STRING_FIELD_NUMBER: _ClassVar[int]
    LEGACY_CLIENT_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    LEGACY_IDENTITY_BINARY_FIELD_NUMBER: _ClassVar[int]
    client_connection_id: int
    challenge: int
    my_timestamp: int
    ping_est_ms: int
    crypt: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramSessionCryptInfoSigned
    cert: _steamnetworkingsockets_messages_certs_pb2.CMsgSteamDatagramCertificateSigned
    legacy_protocol_version: int
    identity_string: str
    legacy_client_steam_id: int
    legacy_identity_binary: (
        _steamnetworkingsockets_messages_certs_pb2.CMsgSteamNetworkingIdentityLegacyBinary
    )
    def __init__(
        self,
        client_connection_id: int | None = ...,
        challenge: int | None = ...,
        my_timestamp: int | None = ...,
        ping_est_ms: int | None = ...,
        crypt: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramSessionCryptInfoSigned
        | _Mapping
        | None = ...,
        cert: _steamnetworkingsockets_messages_certs_pb2.CMsgSteamDatagramCertificateSigned
        | _Mapping
        | None = ...,
        legacy_protocol_version: int | None = ...,
        identity_string: str | None = ...,
        legacy_client_steam_id: int | None = ...,
        legacy_identity_binary: _steamnetworkingsockets_messages_certs_pb2.CMsgSteamNetworkingIdentityLegacyBinary
        | _Mapping
        | None = ...,
    ) -> None: ...

class CMsgSteamSockets_UDP_ConnectOK(_message.Message):
    __slots__ = (
        "client_connection_id",
        "server_connection_id",
        "your_timestamp",
        "delay_time_usec",
        "crypt",
        "cert",
        "identity_string",
        "legacy_server_steam_id",
        "legacy_identity_binary",
    )
    CLIENT_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    SERVER_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    YOUR_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DELAY_TIME_USEC_FIELD_NUMBER: _ClassVar[int]
    CRYPT_FIELD_NUMBER: _ClassVar[int]
    CERT_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_STRING_FIELD_NUMBER: _ClassVar[int]
    LEGACY_SERVER_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    LEGACY_IDENTITY_BINARY_FIELD_NUMBER: _ClassVar[int]
    client_connection_id: int
    server_connection_id: int
    your_timestamp: int
    delay_time_usec: int
    crypt: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramSessionCryptInfoSigned
    cert: _steamnetworkingsockets_messages_certs_pb2.CMsgSteamDatagramCertificateSigned
    identity_string: str
    legacy_server_steam_id: int
    legacy_identity_binary: (
        _steamnetworkingsockets_messages_certs_pb2.CMsgSteamNetworkingIdentityLegacyBinary
    )
    def __init__(
        self,
        client_connection_id: int | None = ...,
        server_connection_id: int | None = ...,
        your_timestamp: int | None = ...,
        delay_time_usec: int | None = ...,
        crypt: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramSessionCryptInfoSigned
        | _Mapping
        | None = ...,
        cert: _steamnetworkingsockets_messages_certs_pb2.CMsgSteamDatagramCertificateSigned
        | _Mapping
        | None = ...,
        identity_string: str | None = ...,
        legacy_server_steam_id: int | None = ...,
        legacy_identity_binary: _steamnetworkingsockets_messages_certs_pb2.CMsgSteamNetworkingIdentityLegacyBinary
        | _Mapping
        | None = ...,
    ) -> None: ...

class CMsgSteamSockets_UDP_ConnectionClosed(_message.Message):
    __slots__ = ("to_connection_id", "from_connection_id", "debug", "reason_code")
    TO_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    FROM_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    DEBUG_FIELD_NUMBER: _ClassVar[int]
    REASON_CODE_FIELD_NUMBER: _ClassVar[int]
    to_connection_id: int
    from_connection_id: int
    debug: str
    reason_code: int
    def __init__(
        self,
        to_connection_id: int | None = ...,
        from_connection_id: int | None = ...,
        debug: str | None = ...,
        reason_code: int | None = ...,
    ) -> None: ...

class CMsgSteamSockets_UDP_NoConnection(_message.Message):
    __slots__ = ("from_connection_id", "to_connection_id")
    FROM_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    TO_CONNECTION_ID_FIELD_NUMBER: _ClassVar[int]
    from_connection_id: int
    to_connection_id: int
    def __init__(
        self, from_connection_id: int | None = ..., to_connection_id: int | None = ...
    ) -> None: ...

class CMsgSteamSockets_UDP_Stats(_message.Message):
    __slots__ = ("stats", "flags")
    class Flags(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ACK_REQUEST_E2E: _ClassVar[CMsgSteamSockets_UDP_Stats.Flags]
        ACK_REQUEST_IMMEDIATE: _ClassVar[CMsgSteamSockets_UDP_Stats.Flags]
        NOT_PRIMARY_TRANSPORT_E2E: _ClassVar[CMsgSteamSockets_UDP_Stats.Flags]

    ACK_REQUEST_E2E: CMsgSteamSockets_UDP_Stats.Flags
    ACK_REQUEST_IMMEDIATE: CMsgSteamSockets_UDP_Stats.Flags
    NOT_PRIMARY_TRANSPORT_E2E: CMsgSteamSockets_UDP_Stats.Flags
    STATS_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    stats: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality
    flags: int
    def __init__(
        self,
        stats: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality
        | _Mapping
        | None = ...,
        flags: int | None = ...,
    ) -> None: ...
