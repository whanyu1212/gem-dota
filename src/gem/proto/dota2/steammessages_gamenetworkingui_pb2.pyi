from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

import steamdatagram_messages_sdr_pb2 as _steamdatagram_messages_sdr_pb2
import steamnetworkingsockets_messages_pb2 as _steamnetworkingsockets_messages_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class CGameNetworkingUI_GlobalState(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CGameNetworkingUI_ConnectionState(_message.Message):
    __slots__ = (
        "connection_key",
        "appid",
        "connection_id_local",
        "identity_local",
        "identity_remote",
        "connection_state",
        "start_time",
        "close_time",
        "close_reason",
        "close_message",
        "status_loc_token",
        "transport_kind",
        "sdrpopid_local",
        "sdrpopid_remote",
        "address_remote",
        "p2p_routing",
        "ping_interior",
        "ping_remote_front",
        "ping_default_internet_route",
        "e2e_quality_local",
        "e2e_quality_remote",
        "e2e_quality_remote_instantaneous_time",
        "e2e_quality_remote_lifetime_time",
        "front_quality_local",
        "front_quality_remote",
        "front_quality_remote_instantaneous_time",
        "front_quality_remote_lifetime_time",
    )
    CONNECTION_KEY_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_ID_LOCAL_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_LOCAL_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_REMOTE_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_STATE_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    CLOSE_TIME_FIELD_NUMBER: _ClassVar[int]
    CLOSE_REASON_FIELD_NUMBER: _ClassVar[int]
    CLOSE_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    STATUS_LOC_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TRANSPORT_KIND_FIELD_NUMBER: _ClassVar[int]
    SDRPOPID_LOCAL_FIELD_NUMBER: _ClassVar[int]
    SDRPOPID_REMOTE_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_REMOTE_FIELD_NUMBER: _ClassVar[int]
    P2P_ROUTING_FIELD_NUMBER: _ClassVar[int]
    PING_INTERIOR_FIELD_NUMBER: _ClassVar[int]
    PING_REMOTE_FRONT_FIELD_NUMBER: _ClassVar[int]
    PING_DEFAULT_INTERNET_ROUTE_FIELD_NUMBER: _ClassVar[int]
    E2E_QUALITY_LOCAL_FIELD_NUMBER: _ClassVar[int]
    E2E_QUALITY_REMOTE_FIELD_NUMBER: _ClassVar[int]
    E2E_QUALITY_REMOTE_INSTANTANEOUS_TIME_FIELD_NUMBER: _ClassVar[int]
    E2E_QUALITY_REMOTE_LIFETIME_TIME_FIELD_NUMBER: _ClassVar[int]
    FRONT_QUALITY_LOCAL_FIELD_NUMBER: _ClassVar[int]
    FRONT_QUALITY_REMOTE_FIELD_NUMBER: _ClassVar[int]
    FRONT_QUALITY_REMOTE_INSTANTANEOUS_TIME_FIELD_NUMBER: _ClassVar[int]
    FRONT_QUALITY_REMOTE_LIFETIME_TIME_FIELD_NUMBER: _ClassVar[int]
    connection_key: str
    appid: int
    connection_id_local: int
    identity_local: str
    identity_remote: str
    connection_state: int
    start_time: int
    close_time: int
    close_reason: int
    close_message: str
    status_loc_token: str
    transport_kind: int
    sdrpopid_local: str
    sdrpopid_remote: str
    address_remote: str
    p2p_routing: _steamdatagram_messages_sdr_pb2.CMsgSteamDatagramP2PRoutingSummary
    ping_interior: int
    ping_remote_front: int
    ping_default_internet_route: int
    e2e_quality_local: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality
    e2e_quality_remote: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality
    e2e_quality_remote_instantaneous_time: int
    e2e_quality_remote_lifetime_time: int
    front_quality_local: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality
    front_quality_remote: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality
    front_quality_remote_instantaneous_time: int
    front_quality_remote_lifetime_time: int
    def __init__(
        self,
        connection_key: str | None = ...,
        appid: int | None = ...,
        connection_id_local: int | None = ...,
        identity_local: str | None = ...,
        identity_remote: str | None = ...,
        connection_state: int | None = ...,
        start_time: int | None = ...,
        close_time: int | None = ...,
        close_reason: int | None = ...,
        close_message: str | None = ...,
        status_loc_token: str | None = ...,
        transport_kind: int | None = ...,
        sdrpopid_local: str | None = ...,
        sdrpopid_remote: str | None = ...,
        address_remote: str | None = ...,
        p2p_routing: _steamdatagram_messages_sdr_pb2.CMsgSteamDatagramP2PRoutingSummary
        | _Mapping
        | None = ...,
        ping_interior: int | None = ...,
        ping_remote_front: int | None = ...,
        ping_default_internet_route: int | None = ...,
        e2e_quality_local: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality
        | _Mapping
        | None = ...,
        e2e_quality_remote: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality
        | _Mapping
        | None = ...,
        e2e_quality_remote_instantaneous_time: int | None = ...,
        e2e_quality_remote_lifetime_time: int | None = ...,
        front_quality_local: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality
        | _Mapping
        | None = ...,
        front_quality_remote: _steamnetworkingsockets_messages_pb2.CMsgSteamDatagramConnectionQuality
        | _Mapping
        | None = ...,
        front_quality_remote_instantaneous_time: int | None = ...,
        front_quality_remote_lifetime_time: int | None = ...,
    ) -> None: ...

class CGameNetworkingUI_Message(_message.Message):
    __slots__ = ("connection_state",)
    CONNECTION_STATE_FIELD_NUMBER: _ClassVar[int]
    connection_state: _containers.RepeatedCompositeFieldContainer[CGameNetworkingUI_ConnectionState]
    def __init__(
        self, connection_state: _Iterable[CGameNetworkingUI_ConnectionState | _Mapping] | None = ...
    ) -> None: ...

class CGameNetworkingUI_ConnectionSummary(_message.Message):
    __slots__ = (
        "transport_kind",
        "connection_state",
        "sdrpop_local",
        "sdrpop_remote",
        "ping_ms",
        "packet_loss",
        "ping_default_internet_route",
        "ip_was_shared",
    )
    TRANSPORT_KIND_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_STATE_FIELD_NUMBER: _ClassVar[int]
    SDRPOP_LOCAL_FIELD_NUMBER: _ClassVar[int]
    SDRPOP_REMOTE_FIELD_NUMBER: _ClassVar[int]
    PING_MS_FIELD_NUMBER: _ClassVar[int]
    PACKET_LOSS_FIELD_NUMBER: _ClassVar[int]
    PING_DEFAULT_INTERNET_ROUTE_FIELD_NUMBER: _ClassVar[int]
    IP_WAS_SHARED_FIELD_NUMBER: _ClassVar[int]
    transport_kind: int
    connection_state: int
    sdrpop_local: str
    sdrpop_remote: str
    ping_ms: int
    packet_loss: float
    ping_default_internet_route: int
    ip_was_shared: bool
    def __init__(
        self,
        transport_kind: int | None = ...,
        connection_state: int | None = ...,
        sdrpop_local: str | None = ...,
        sdrpop_remote: str | None = ...,
        ping_ms: int | None = ...,
        packet_loss: float | None = ...,
        ping_default_internet_route: int | None = ...,
        ip_was_shared: bool = ...,
    ) -> None: ...

class CGameNetworkingUI_AppSummary(_message.Message):
    __slots__ = (
        "appid",
        "ip_was_shared_with_friend",
        "ip_was_shared_with_nonfriend",
        "active_connections",
        "main_cxn",
    )
    APPID_FIELD_NUMBER: _ClassVar[int]
    IP_WAS_SHARED_WITH_FRIEND_FIELD_NUMBER: _ClassVar[int]
    IP_WAS_SHARED_WITH_NONFRIEND_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    MAIN_CXN_FIELD_NUMBER: _ClassVar[int]
    appid: int
    ip_was_shared_with_friend: bool
    ip_was_shared_with_nonfriend: bool
    active_connections: int
    main_cxn: CGameNetworkingUI_ConnectionSummary
    def __init__(
        self,
        appid: int | None = ...,
        ip_was_shared_with_friend: bool = ...,
        ip_was_shared_with_nonfriend: bool = ...,
        active_connections: int | None = ...,
        main_cxn: CGameNetworkingUI_ConnectionSummary | _Mapping | None = ...,
    ) -> None: ...
