from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

import steamnetworkingsockets_messages_certs_pb2 as _steamnetworkingsockets_messages_certs_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class CMsgSteamDatagramRelayAuthTicket(_message.Message):
    __slots__ = (
        "time_expiry",
        "authorized_client_identity_string",
        "gameserver_identity_string",
        "authorized_public_ip",
        "gameserver_address",
        "app_id",
        "virtual_port",
        "extra_fields",
        "legacy_authorized_steam_id",
        "legacy_gameserver_steam_id",
        "legacy_gameserver_pop_id",
        "legacy_authorized_client_identity_binary",
        "legacy_gameserver_identity_binary",
    )
    class ExtraField(_message.Message):
        __slots__ = ("name", "string_value", "int64_value", "fixed64_value")
        NAME_FIELD_NUMBER: _ClassVar[int]
        STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
        INT64_VALUE_FIELD_NUMBER: _ClassVar[int]
        FIXED64_VALUE_FIELD_NUMBER: _ClassVar[int]
        name: str
        string_value: str
        int64_value: int
        fixed64_value: int
        def __init__(
            self,
            name: str | None = ...,
            string_value: str | None = ...,
            int64_value: int | None = ...,
            fixed64_value: int | None = ...,
        ) -> None: ...

    TIME_EXPIRY_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZED_CLIENT_IDENTITY_STRING_FIELD_NUMBER: _ClassVar[int]
    GAMESERVER_IDENTITY_STRING_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZED_PUBLIC_IP_FIELD_NUMBER: _ClassVar[int]
    GAMESERVER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    VIRTUAL_PORT_FIELD_NUMBER: _ClassVar[int]
    EXTRA_FIELDS_FIELD_NUMBER: _ClassVar[int]
    LEGACY_AUTHORIZED_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    LEGACY_GAMESERVER_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    LEGACY_GAMESERVER_POP_ID_FIELD_NUMBER: _ClassVar[int]
    LEGACY_AUTHORIZED_CLIENT_IDENTITY_BINARY_FIELD_NUMBER: _ClassVar[int]
    LEGACY_GAMESERVER_IDENTITY_BINARY_FIELD_NUMBER: _ClassVar[int]
    time_expiry: int
    authorized_client_identity_string: str
    gameserver_identity_string: str
    authorized_public_ip: int
    gameserver_address: bytes
    app_id: int
    virtual_port: int
    extra_fields: _containers.RepeatedCompositeFieldContainer[
        CMsgSteamDatagramRelayAuthTicket.ExtraField
    ]
    legacy_authorized_steam_id: int
    legacy_gameserver_steam_id: int
    legacy_gameserver_pop_id: int
    legacy_authorized_client_identity_binary: bytes
    legacy_gameserver_identity_binary: bytes
    def __init__(
        self,
        time_expiry: int | None = ...,
        authorized_client_identity_string: str | None = ...,
        gameserver_identity_string: str | None = ...,
        authorized_public_ip: int | None = ...,
        gameserver_address: bytes | None = ...,
        app_id: int | None = ...,
        virtual_port: int | None = ...,
        extra_fields: _Iterable[CMsgSteamDatagramRelayAuthTicket.ExtraField | _Mapping]
        | None = ...,
        legacy_authorized_steam_id: int | None = ...,
        legacy_gameserver_steam_id: int | None = ...,
        legacy_gameserver_pop_id: int | None = ...,
        legacy_authorized_client_identity_binary: bytes | None = ...,
        legacy_gameserver_identity_binary: bytes | None = ...,
    ) -> None: ...

class CMsgSteamDatagramSignedRelayAuthTicket(_message.Message):
    __slots__ = ("reserved_do_not_use", "ticket", "signature", "key_id", "certs")
    RESERVED_DO_NOT_USE_FIELD_NUMBER: _ClassVar[int]
    TICKET_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    KEY_ID_FIELD_NUMBER: _ClassVar[int]
    CERTS_FIELD_NUMBER: _ClassVar[int]
    reserved_do_not_use: int
    ticket: bytes
    signature: bytes
    key_id: int
    certs: _containers.RepeatedCompositeFieldContainer[
        _steamnetworkingsockets_messages_certs_pb2.CMsgSteamDatagramCertificateSigned
    ]
    def __init__(
        self,
        reserved_do_not_use: int | None = ...,
        ticket: bytes | None = ...,
        signature: bytes | None = ...,
        key_id: int | None = ...,
        certs: _Iterable[
            _steamnetworkingsockets_messages_certs_pb2.CMsgSteamDatagramCertificateSigned | _Mapping
        ]
        | None = ...,
    ) -> None: ...

class CMsgSteamDatagramCachedCredentialsForApp(_message.Message):
    __slots__ = ("private_key", "cert", "relay_tickets")
    PRIVATE_KEY_FIELD_NUMBER: _ClassVar[int]
    CERT_FIELD_NUMBER: _ClassVar[int]
    RELAY_TICKETS_FIELD_NUMBER: _ClassVar[int]
    private_key: bytes
    cert: bytes
    relay_tickets: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(
        self,
        private_key: bytes | None = ...,
        cert: bytes | None = ...,
        relay_tickets: _Iterable[bytes] | None = ...,
    ) -> None: ...

class CMsgSteamDatagramGameCoordinatorServerLogin(_message.Message):
    __slots__ = (
        "time_generated",
        "appid",
        "routing",
        "appdata",
        "legacy_identity_binary",
        "identity_string",
        "dummy_steam_id",
    )
    TIME_GENERATED_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    ROUTING_FIELD_NUMBER: _ClassVar[int]
    APPDATA_FIELD_NUMBER: _ClassVar[int]
    LEGACY_IDENTITY_BINARY_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_STRING_FIELD_NUMBER: _ClassVar[int]
    DUMMY_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    time_generated: int
    appid: int
    routing: bytes
    appdata: bytes
    legacy_identity_binary: bytes
    identity_string: str
    dummy_steam_id: int
    def __init__(
        self,
        time_generated: int | None = ...,
        appid: int | None = ...,
        routing: bytes | None = ...,
        appdata: bytes | None = ...,
        legacy_identity_binary: bytes | None = ...,
        identity_string: str | None = ...,
        dummy_steam_id: int | None = ...,
    ) -> None: ...

class CMsgSteamDatagramSignedGameCoordinatorServerLogin(_message.Message):
    __slots__ = ("cert", "login", "signature")
    CERT_FIELD_NUMBER: _ClassVar[int]
    LOGIN_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    cert: _steamnetworkingsockets_messages_certs_pb2.CMsgSteamDatagramCertificateSigned
    login: bytes
    signature: bytes
    def __init__(
        self,
        cert: _steamnetworkingsockets_messages_certs_pb2.CMsgSteamDatagramCertificateSigned
        | _Mapping
        | None = ...,
        login: bytes | None = ...,
        signature: bytes | None = ...,
    ) -> None: ...

class CMsgSteamDatagramHostedServerAddressPlaintext(_message.Message):
    __slots__ = ("ipv4", "ipv6", "port", "routing_secret", "protocol_version")
    IPV4_FIELD_NUMBER: _ClassVar[int]
    IPV6_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    ROUTING_SECRET_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_VERSION_FIELD_NUMBER: _ClassVar[int]
    ipv4: int
    ipv6: bytes
    port: int
    routing_secret: int
    protocol_version: int
    def __init__(
        self,
        ipv4: int | None = ...,
        ipv6: bytes | None = ...,
        port: int | None = ...,
        routing_secret: int | None = ...,
        protocol_version: int | None = ...,
    ) -> None: ...
