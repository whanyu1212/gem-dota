from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

import netmessages_pb2 as _netmessages_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class C2S_CONNECT_SameProcessCheck(_message.Message):
    __slots__ = ("localhost_process_id", "key")
    LOCALHOST_PROCESS_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    localhost_process_id: int
    key: int
    def __init__(self, localhost_process_id: int | None = ..., key: int | None = ...) -> None: ...

class C2S_CONNECT_Message(_message.Message):
    __slots__ = (
        "host_version",
        "auth_protocol",
        "challenge_number",
        "reservation_cookie",
        "low_violence",
        "encrypted_password",
        "splitplayers",
        "auth_steam",
        "challenge_context",
        "localhost_same_process_check",
    )
    HOST_VERSION_FIELD_NUMBER: _ClassVar[int]
    AUTH_PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    RESERVATION_COOKIE_FIELD_NUMBER: _ClassVar[int]
    LOW_VIOLENCE_FIELD_NUMBER: _ClassVar[int]
    ENCRYPTED_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    SPLITPLAYERS_FIELD_NUMBER: _ClassVar[int]
    AUTH_STEAM_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    LOCALHOST_SAME_PROCESS_CHECK_FIELD_NUMBER: _ClassVar[int]
    host_version: int
    auth_protocol: int
    challenge_number: int
    reservation_cookie: int
    low_violence: bool
    encrypted_password: bytes
    splitplayers: _containers.RepeatedCompositeFieldContainer[
        _netmessages_pb2.CCLCMsg_SplitPlayerConnect
    ]
    auth_steam: bytes
    challenge_context: str
    localhost_same_process_check: C2S_CONNECT_SameProcessCheck
    def __init__(
        self,
        host_version: int | None = ...,
        auth_protocol: int | None = ...,
        challenge_number: int | None = ...,
        reservation_cookie: int | None = ...,
        low_violence: bool = ...,
        encrypted_password: bytes | None = ...,
        splitplayers: _Iterable[_netmessages_pb2.CCLCMsg_SplitPlayerConnect | _Mapping]
        | None = ...,
        auth_steam: bytes | None = ...,
        challenge_context: str | None = ...,
        localhost_same_process_check: C2S_CONNECT_SameProcessCheck | _Mapping | None = ...,
    ) -> None: ...

class C2S_CONNECTION_Message(_message.Message):
    __slots__ = ("addon_name", "localhost_same_process_check")
    ADDON_NAME_FIELD_NUMBER: _ClassVar[int]
    LOCALHOST_SAME_PROCESS_CHECK_FIELD_NUMBER: _ClassVar[int]
    addon_name: str
    localhost_same_process_check: C2S_CONNECT_SameProcessCheck
    def __init__(
        self,
        addon_name: str | None = ...,
        localhost_same_process_check: C2S_CONNECT_SameProcessCheck | _Mapping | None = ...,
    ) -> None: ...
