from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class CCloud_GetUploadServerInfo_Request(_message.Message):
    __slots__ = ("appid",)
    APPID_FIELD_NUMBER: _ClassVar[int]
    appid: int
    def __init__(self, appid: int | None = ...) -> None: ...

class CCloud_GetUploadServerInfo_Response(_message.Message):
    __slots__ = ("server_url",)
    SERVER_URL_FIELD_NUMBER: _ClassVar[int]
    server_url: str
    def __init__(self, server_url: str | None = ...) -> None: ...

class CCloud_GetFileDetails_Request(_message.Message):
    __slots__ = ("ugcid", "appid")
    UGCID_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    ugcid: int
    appid: int
    def __init__(self, ugcid: int | None = ..., appid: int | None = ...) -> None: ...

class CCloud_UserFile(_message.Message):
    __slots__ = ("appid", "ugcid", "filename", "timestamp", "file_size", "url", "steamid_creator")
    APPID_FIELD_NUMBER: _ClassVar[int]
    UGCID_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    FILE_SIZE_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    STEAMID_CREATOR_FIELD_NUMBER: _ClassVar[int]
    appid: int
    ugcid: int
    filename: str
    timestamp: int
    file_size: int
    url: str
    steamid_creator: int
    def __init__(
        self,
        appid: int | None = ...,
        ugcid: int | None = ...,
        filename: str | None = ...,
        timestamp: int | None = ...,
        file_size: int | None = ...,
        url: str | None = ...,
        steamid_creator: int | None = ...,
    ) -> None: ...

class CCloud_GetFileDetails_Response(_message.Message):
    __slots__ = ("details",)
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    details: CCloud_UserFile
    def __init__(self, details: CCloud_UserFile | _Mapping | None = ...) -> None: ...

class CCloud_EnumerateUserFiles_Request(_message.Message):
    __slots__ = ("appid", "extended_details", "count", "start_index")
    APPID_FIELD_NUMBER: _ClassVar[int]
    EXTENDED_DETAILS_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    START_INDEX_FIELD_NUMBER: _ClassVar[int]
    appid: int
    extended_details: bool
    count: int
    start_index: int
    def __init__(
        self,
        appid: int | None = ...,
        extended_details: bool = ...,
        count: int | None = ...,
        start_index: int | None = ...,
    ) -> None: ...

class CCloud_EnumerateUserFiles_Response(_message.Message):
    __slots__ = ("files", "total_files")
    FILES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FILES_FIELD_NUMBER: _ClassVar[int]
    files: _containers.RepeatedCompositeFieldContainer[CCloud_UserFile]
    total_files: int
    def __init__(
        self,
        files: _Iterable[CCloud_UserFile | _Mapping] | None = ...,
        total_files: int | None = ...,
    ) -> None: ...

class CCloud_Delete_Request(_message.Message):
    __slots__ = ("filename", "appid")
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    filename: str
    appid: int
    def __init__(self, filename: str | None = ..., appid: int | None = ...) -> None: ...

class CCloud_Delete_Response(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
