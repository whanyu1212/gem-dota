from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NetMessageSplitscreenUserChanged(_message.Message):
    __slots__ = ("slot",)
    SLOT_FIELD_NUMBER: _ClassVar[int]
    slot: int
    def __init__(self, slot: _Optional[int] = ...) -> None: ...

class NetMessageConnectionClosed(_message.Message):
    __slots__ = ("reason", "message")
    REASON_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    reason: int
    message: str
    def __init__(self, reason: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class NetMessageConnectionCrashed(_message.Message):
    __slots__ = ("reason", "message")
    REASON_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    reason: int
    message: str
    def __init__(self, reason: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class NetMessagePacketStart(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class NetMessagePacketEnd(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
