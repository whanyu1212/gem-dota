from ..steammessages_unified_base import steamworkssdk_pb2 as _steamworkssdk_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CCloud_GetUploadServerInfo_Request(_message.Message):
    __slots__ = ("appid",)
    APPID_FIELD_NUMBER: _ClassVar[int]
    appid: int
    def __init__(self, appid: _Optional[int] = ...) -> None: ...

class CCloud_GetUploadServerInfo_Response(_message.Message):
    __slots__ = ("server_url",)
    SERVER_URL_FIELD_NUMBER: _ClassVar[int]
    server_url: str
    def __init__(self, server_url: _Optional[str] = ...) -> None: ...

class CCloud_GetFileDetails_Request(_message.Message):
    __slots__ = ("ugcid", "appid")
    UGCID_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    ugcid: int
    appid: int
    def __init__(self, ugcid: _Optional[int] = ..., appid: _Optional[int] = ...) -> None: ...

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
    def __init__(self, appid: _Optional[int] = ..., ugcid: _Optional[int] = ..., filename: _Optional[str] = ..., timestamp: _Optional[int] = ..., file_size: _Optional[int] = ..., url: _Optional[str] = ..., steamid_creator: _Optional[int] = ...) -> None: ...

class CCloud_GetFileDetails_Response(_message.Message):
    __slots__ = ("details",)
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    details: CCloud_UserFile
    def __init__(self, details: _Optional[_Union[CCloud_UserFile, _Mapping]] = ...) -> None: ...

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
    def __init__(self, appid: _Optional[int] = ..., extended_details: bool = ..., count: _Optional[int] = ..., start_index: _Optional[int] = ...) -> None: ...

class CCloud_EnumerateUserFiles_Response(_message.Message):
    __slots__ = ("files", "total_files")
    FILES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FILES_FIELD_NUMBER: _ClassVar[int]
    files: _containers.RepeatedCompositeFieldContainer[CCloud_UserFile]
    total_files: int
    def __init__(self, files: _Optional[_Iterable[_Union[CCloud_UserFile, _Mapping]]] = ..., total_files: _Optional[int] = ...) -> None: ...

class CCloud_Delete_Request(_message.Message):
    __slots__ = ("filename", "appid")
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    filename: str
    appid: int
    def __init__(self, filename: _Optional[str] = ..., appid: _Optional[int] = ...) -> None: ...

class CCloud_Delete_Response(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
