from ..steammessages_unified_base import steamworkssdk_pb2 as _steamworkssdk_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CHelpRequestLogs_UploadUserApplicationLog_Request(_message.Message):
    __slots__ = ("appid", "log_type", "version_string", "log_contents")
    APPID_FIELD_NUMBER: _ClassVar[int]
    LOG_TYPE_FIELD_NUMBER: _ClassVar[int]
    VERSION_STRING_FIELD_NUMBER: _ClassVar[int]
    LOG_CONTENTS_FIELD_NUMBER: _ClassVar[int]
    appid: int
    log_type: str
    version_string: str
    log_contents: str
    def __init__(self, appid: _Optional[int] = ..., log_type: _Optional[str] = ..., version_string: _Optional[str] = ..., log_contents: _Optional[str] = ...) -> None: ...

class CHelpRequestLogs_UploadUserApplicationLog_Response(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...
