from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message

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
    def __init__(
        self,
        appid: int | None = ...,
        log_type: str | None = ...,
        version_string: str | None = ...,
        log_contents: str | None = ...,
    ) -> None: ...

class CHelpRequestLogs_UploadUserApplicationLog_Response(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: int | None = ...) -> None: ...
