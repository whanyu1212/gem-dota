import netmessages_pb2 as _netmessages_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class C2S_CONNECT_SameProcessCheck(_message.Message):
    __slots__ = ("localhost_process_id", "key")
    LOCALHOST_PROCESS_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    localhost_process_id: int
    key: int
    def __init__(self, localhost_process_id: _Optional[int] = ..., key: _Optional[int] = ...) -> None: ...

class C2S_CONNECT_Message(_message.Message):
    __slots__ = ("host_version", "auth_protocol", "challenge_number", "reservation_cookie", "low_violence", "encrypted_password", "splitplayers", "auth_steam", "challenge_context", "localhost_same_process_check")
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
    splitplayers: _containers.RepeatedCompositeFieldContainer[_netmessages_pb2.CCLCMsg_SplitPlayerConnect]
    auth_steam: bytes
    challenge_context: str
    localhost_same_process_check: C2S_CONNECT_SameProcessCheck
    def __init__(self, host_version: _Optional[int] = ..., auth_protocol: _Optional[int] = ..., challenge_number: _Optional[int] = ..., reservation_cookie: _Optional[int] = ..., low_violence: bool = ..., encrypted_password: _Optional[bytes] = ..., splitplayers: _Optional[_Iterable[_Union[_netmessages_pb2.CCLCMsg_SplitPlayerConnect, _Mapping]]] = ..., auth_steam: _Optional[bytes] = ..., challenge_context: _Optional[str] = ..., localhost_same_process_check: _Optional[_Union[C2S_CONNECT_SameProcessCheck, _Mapping]] = ...) -> None: ...

class C2S_CONNECTION_Message(_message.Message):
    __slots__ = ("addon_name", "localhost_same_process_check")
    ADDON_NAME_FIELD_NUMBER: _ClassVar[int]
    LOCALHOST_SAME_PROCESS_CHECK_FIELD_NUMBER: _ClassVar[int]
    addon_name: str
    localhost_same_process_check: C2S_CONNECT_SameProcessCheck
    def __init__(self, addon_name: _Optional[str] = ..., localhost_same_process_check: _Optional[_Union[C2S_CONNECT_SameProcessCheck, _Mapping]] = ...) -> None: ...
