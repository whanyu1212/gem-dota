from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class CMsgSteamNetworkingIdentityLegacyBinary(_message.Message):
    __slots__ = ("steam_id", "generic_bytes", "generic_string", "ipv6_and_port")
    STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    GENERIC_BYTES_FIELD_NUMBER: _ClassVar[int]
    GENERIC_STRING_FIELD_NUMBER: _ClassVar[int]
    IPV6_AND_PORT_FIELD_NUMBER: _ClassVar[int]
    steam_id: int
    generic_bytes: bytes
    generic_string: str
    ipv6_and_port: bytes
    def __init__(
        self,
        steam_id: int | None = ...,
        generic_bytes: bytes | None = ...,
        generic_string: str | None = ...,
        ipv6_and_port: bytes | None = ...,
    ) -> None: ...

class CMsgSteamDatagramCertificate(_message.Message):
    __slots__ = (
        "key_type",
        "key_data",
        "legacy_steam_id",
        "legacy_identity_binary",
        "identity_string",
        "gameserver_datacenter_ids",
        "time_created",
        "time_expiry",
        "app_ids",
        "ip_addresses",
    )
    class EKeyType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INVALID: _ClassVar[CMsgSteamDatagramCertificate.EKeyType]
        ED25519: _ClassVar[CMsgSteamDatagramCertificate.EKeyType]

    INVALID: CMsgSteamDatagramCertificate.EKeyType
    ED25519: CMsgSteamDatagramCertificate.EKeyType
    KEY_TYPE_FIELD_NUMBER: _ClassVar[int]
    KEY_DATA_FIELD_NUMBER: _ClassVar[int]
    LEGACY_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    LEGACY_IDENTITY_BINARY_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_STRING_FIELD_NUMBER: _ClassVar[int]
    GAMESERVER_DATACENTER_IDS_FIELD_NUMBER: _ClassVar[int]
    TIME_CREATED_FIELD_NUMBER: _ClassVar[int]
    TIME_EXPIRY_FIELD_NUMBER: _ClassVar[int]
    APP_IDS_FIELD_NUMBER: _ClassVar[int]
    IP_ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    key_type: CMsgSteamDatagramCertificate.EKeyType
    key_data: bytes
    legacy_steam_id: int
    legacy_identity_binary: CMsgSteamNetworkingIdentityLegacyBinary
    identity_string: str
    gameserver_datacenter_ids: _containers.RepeatedScalarFieldContainer[int]
    time_created: int
    time_expiry: int
    app_ids: _containers.RepeatedScalarFieldContainer[int]
    ip_addresses: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        key_type: CMsgSteamDatagramCertificate.EKeyType | str | None = ...,
        key_data: bytes | None = ...,
        legacy_steam_id: int | None = ...,
        legacy_identity_binary: CMsgSteamNetworkingIdentityLegacyBinary | _Mapping | None = ...,
        identity_string: str | None = ...,
        gameserver_datacenter_ids: _Iterable[int] | None = ...,
        time_created: int | None = ...,
        time_expiry: int | None = ...,
        app_ids: _Iterable[int] | None = ...,
        ip_addresses: _Iterable[str] | None = ...,
    ) -> None: ...

class CMsgSteamDatagramCertificateSigned(_message.Message):
    __slots__ = ("cert", "ca_key_id", "ca_signature", "private_key_data")
    CERT_FIELD_NUMBER: _ClassVar[int]
    CA_KEY_ID_FIELD_NUMBER: _ClassVar[int]
    CA_SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_KEY_DATA_FIELD_NUMBER: _ClassVar[int]
    cert: bytes
    ca_key_id: int
    ca_signature: bytes
    private_key_data: bytes
    def __init__(
        self,
        cert: bytes | None = ...,
        ca_key_id: int | None = ...,
        ca_signature: bytes | None = ...,
        private_key_data: bytes | None = ...,
    ) -> None: ...

class CMsgSteamDatagramCertificateRequest(_message.Message):
    __slots__ = ("cert",)
    CERT_FIELD_NUMBER: _ClassVar[int]
    cert: CMsgSteamDatagramCertificate
    def __init__(self, cert: CMsgSteamDatagramCertificate | _Mapping | None = ...) -> None: ...
