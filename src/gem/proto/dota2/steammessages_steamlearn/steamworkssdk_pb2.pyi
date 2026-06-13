from steammessages_unified_base import steamworkssdk_pb2 as _steamworkssdk_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ESteamLearnDataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STEAMLEARN_DATATYPE_INVALID: _ClassVar[ESteamLearnDataType]
    STEAMLEARN_DATATYPE_INT32: _ClassVar[ESteamLearnDataType]
    STEAMLEARN_DATATYPE_FLOAT32: _ClassVar[ESteamLearnDataType]
    STEAMLEARN_DATATYPE_BOOL: _ClassVar[ESteamLearnDataType]
    STEAMLEARN_DATATYPE_STRING: _ClassVar[ESteamLearnDataType]
    STEAMLEARN_DATATYPE_OBJECT: _ClassVar[ESteamLearnDataType]

class ESteammLearnRegisterDataSourceResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_ERROR: _ClassVar[ESteammLearnRegisterDataSourceResult]
    STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_SUCCESS_CREATED: _ClassVar[ESteammLearnRegisterDataSourceResult]
    STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_SUCCESS_FOUND: _ClassVar[ESteammLearnRegisterDataSourceResult]
    STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_ERROR_GENERIC: _ClassVar[ESteammLearnRegisterDataSourceResult]
    STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_ERROR_INVALID_NAME: _ClassVar[ESteammLearnRegisterDataSourceResult]
    STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_ERROR_INVALID_VERSION: _ClassVar[ESteammLearnRegisterDataSourceResult]
    STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_ERROR_DATA_CHANGED: _ClassVar[ESteammLearnRegisterDataSourceResult]
    STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_ERROR_DATA_INVALID: _ClassVar[ESteammLearnRegisterDataSourceResult]
    STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_ERROR_FORBIDDEN: _ClassVar[ESteammLearnRegisterDataSourceResult]
    STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_ERROR_INVALID_TIMESTAMP: _ClassVar[ESteammLearnRegisterDataSourceResult]
    STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_DISABLED: _ClassVar[ESteammLearnRegisterDataSourceResult]

class ESteamLearnCacheDataResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STEAMLEARN_CACHE_DATA_ERROR: _ClassVar[ESteamLearnCacheDataResult]
    STEAMLEARN_CACHE_DATA_SUCCESS: _ClassVar[ESteamLearnCacheDataResult]
    STEAMLEARN_CACHE_DATA_ERROR_UNKNOWN_DATA_SOURCE: _ClassVar[ESteamLearnCacheDataResult]
    STEAMLEARN_CACHE_DATA_ERROR_UNCACHED_DATA_SOURCE: _ClassVar[ESteamLearnCacheDataResult]
    STEAMLEARN_CACHE_DATA_ERROR_INVALID_KEYS: _ClassVar[ESteamLearnCacheDataResult]
    STEAMLEARN_CACHE_DATA_ERROR_FORBIDDEN: _ClassVar[ESteamLearnCacheDataResult]
    STEAMLEARN_CACHE_DATA_ERROR_INVALID_TIMESTAMP: _ClassVar[ESteamLearnCacheDataResult]
    STEAMLEARN_CACHE_DATA_DISABLED: _ClassVar[ESteamLearnCacheDataResult]

class ESteamLearnSnapshotProjectResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STEAMLEARN_SNAPSHOT_PROJECT_ERROR: _ClassVar[ESteamLearnSnapshotProjectResult]
    STEAMLEARN_SNAPSHOT_PROJECT_SUCCESS_STORED: _ClassVar[ESteamLearnSnapshotProjectResult]
    STEAMLEARN_SNAPSHOT_PROJECT_SUCCESS_QUEUED: _ClassVar[ESteamLearnSnapshotProjectResult]
    STEAMLEARN_SNAPSHOT_PROJECT_ERROR_INVALID_PROJECT_ID: _ClassVar[ESteamLearnSnapshotProjectResult]
    STEAMLEARN_SNAPSHOT_PROJECT_ERROR_UNKNOWN_DATA_SOURCE: _ClassVar[ESteamLearnSnapshotProjectResult]
    STEAMLEARN_SNAPSHOT_PROJECT_ERROR_INVALID_DATA_SOURCE_KEY: _ClassVar[ESteamLearnSnapshotProjectResult]
    STEAMLEARN_SNAPSHOT_PROJECT_ERROR_MISSING_CACHE_DURATION: _ClassVar[ESteamLearnSnapshotProjectResult]
    STEAMLEARN_SNAPSHOT_PROJECT_ERROR_NO_PUBLISHED_CONFIG: _ClassVar[ESteamLearnSnapshotProjectResult]
    STEAMLEARN_SNAPSHOT_PROJECT_ERROR_FORBIDDEN: _ClassVar[ESteamLearnSnapshotProjectResult]
    STEAMLEARN_SNAPSHOT_PROJECT_ERROR_INVALID_TIMESTAMP: _ClassVar[ESteamLearnSnapshotProjectResult]
    STEAMLEARN_SNAPSHOT_PROJECT_ERROR_INTERNAL_DATA_SOURCE_ERROR: _ClassVar[ESteamLearnSnapshotProjectResult]
    STEAMLEARN_SNAPSHOT_PROJECT_DISABLED: _ClassVar[ESteamLearnSnapshotProjectResult]
    STEAMLEARN_SNAPSHOT_PROJECT_ERROR_INVALID_PUBLISHED_VERSION: _ClassVar[ESteamLearnSnapshotProjectResult]

class ESteamLearnGetAccessTokensResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STEAMLEARN_GET_ACCESS_TOKENS_ERROR: _ClassVar[ESteamLearnGetAccessTokensResult]
    STEAMLEARN_GET_ACCESS_TOKENS_SUCCESS: _ClassVar[ESteamLearnGetAccessTokensResult]

class ESteamLearnInferenceResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STEAMLEARN_INFERENCE_ERROR: _ClassVar[ESteamLearnInferenceResult]
    STEAMLEARN_INFERENCE_SUCCESS: _ClassVar[ESteamLearnInferenceResult]
    STEAMLEARN_INFERENCE_ERROR_INVALID_PROJECT_ID: _ClassVar[ESteamLearnInferenceResult]
    STEAMLEARN_INFERENCE_ERROR_MISSING_CACHED_SCHEMA_DATA: _ClassVar[ESteamLearnInferenceResult]
    STEAMLEARN_INFERENCE_ERROR_NO_PUBLISHED_CONFIG: _ClassVar[ESteamLearnInferenceResult]
    STEAMLEARN_INFERENCE_ERROR_FORBIDDEN: _ClassVar[ESteamLearnInferenceResult]
    STEAMLEARN_INFERENCE_ERROR_INVALID_TIMESTAMP: _ClassVar[ESteamLearnInferenceResult]
    STEAMLEARN_INFERENCE_ERROR_INVALID_PUBLISHED_VERSION: _ClassVar[ESteamLearnInferenceResult]
    STEAMLEARN_INFERENCE_ERROR_NO_FETCH_ID_FOUND: _ClassVar[ESteamLearnInferenceResult]
    STEAMLEARN_INFERENCE_ERROR_TOO_BUSY: _ClassVar[ESteamLearnInferenceResult]
    STEAMLEARN_INFERENCE_ERROR_UNSUPPLIED_DATA_FAIL: _ClassVar[ESteamLearnInferenceResult]
    STEAMLEARN_INFERENCE_ERROR_UNSUPPLIED_DATA_NO_KEYS: _ClassVar[ESteamLearnInferenceResult]
    STEAMLEARN_INFERENCE_DISABLED: _ClassVar[ESteamLearnInferenceResult]
    STEAMLEARN_INFERENCE_ERROR_NO_OUTPUT: _ClassVar[ESteamLearnInferenceResult]
    STEAMLEARN_INFERENCE_ERROR_INVALID_NAMED_INFERENCE: _ClassVar[ESteamLearnInferenceResult]

class ESteamLearnInferenceMetadataResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STEAMLEARN_INFERENCE_METADATA_ERROR: _ClassVar[ESteamLearnInferenceMetadataResult]
    STEAMLEARN_INFERENCE_METADATA_SUCCESS: _ClassVar[ESteamLearnInferenceMetadataResult]
    STEAMLEARN_INFERENCE_METADATA_ERROR_INVALID_PROJECT_ID: _ClassVar[ESteamLearnInferenceMetadataResult]
    STEAMLEARN_INFERENCE_METADATA_ERROR_NO_PUBLISHED_CONFIG: _ClassVar[ESteamLearnInferenceMetadataResult]
    STEAMLEARN_INFERENCE_METADATA_ERROR_FORBIDDEN: _ClassVar[ESteamLearnInferenceMetadataResult]
    STEAMLEARN_INFERENCE_METADATA_ERROR_INVALID_TIMESTAMP: _ClassVar[ESteamLearnInferenceMetadataResult]
    STEAMLEARN_INFERENCE_METADATA_ERROR_INVALID_PUBLISHED_VERSION: _ClassVar[ESteamLearnInferenceMetadataResult]
    STEAMLEARN_INFERENCE_METADATA_ERROR_NO_FETCH_ID_FOUND: _ClassVar[ESteamLearnInferenceMetadataResult]
STEAMLEARN_DATATYPE_INVALID: ESteamLearnDataType
STEAMLEARN_DATATYPE_INT32: ESteamLearnDataType
STEAMLEARN_DATATYPE_FLOAT32: ESteamLearnDataType
STEAMLEARN_DATATYPE_BOOL: ESteamLearnDataType
STEAMLEARN_DATATYPE_STRING: ESteamLearnDataType
STEAMLEARN_DATATYPE_OBJECT: ESteamLearnDataType
STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_ERROR: ESteammLearnRegisterDataSourceResult
STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_SUCCESS_CREATED: ESteammLearnRegisterDataSourceResult
STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_SUCCESS_FOUND: ESteammLearnRegisterDataSourceResult
STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_ERROR_GENERIC: ESteammLearnRegisterDataSourceResult
STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_ERROR_INVALID_NAME: ESteammLearnRegisterDataSourceResult
STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_ERROR_INVALID_VERSION: ESteammLearnRegisterDataSourceResult
STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_ERROR_DATA_CHANGED: ESteammLearnRegisterDataSourceResult
STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_ERROR_DATA_INVALID: ESteammLearnRegisterDataSourceResult
STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_ERROR_FORBIDDEN: ESteammLearnRegisterDataSourceResult
STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_ERROR_INVALID_TIMESTAMP: ESteammLearnRegisterDataSourceResult
STEAMLEARN_REGISTER_DATA_SOURCE_RESULT_DISABLED: ESteammLearnRegisterDataSourceResult
STEAMLEARN_CACHE_DATA_ERROR: ESteamLearnCacheDataResult
STEAMLEARN_CACHE_DATA_SUCCESS: ESteamLearnCacheDataResult
STEAMLEARN_CACHE_DATA_ERROR_UNKNOWN_DATA_SOURCE: ESteamLearnCacheDataResult
STEAMLEARN_CACHE_DATA_ERROR_UNCACHED_DATA_SOURCE: ESteamLearnCacheDataResult
STEAMLEARN_CACHE_DATA_ERROR_INVALID_KEYS: ESteamLearnCacheDataResult
STEAMLEARN_CACHE_DATA_ERROR_FORBIDDEN: ESteamLearnCacheDataResult
STEAMLEARN_CACHE_DATA_ERROR_INVALID_TIMESTAMP: ESteamLearnCacheDataResult
STEAMLEARN_CACHE_DATA_DISABLED: ESteamLearnCacheDataResult
STEAMLEARN_SNAPSHOT_PROJECT_ERROR: ESteamLearnSnapshotProjectResult
STEAMLEARN_SNAPSHOT_PROJECT_SUCCESS_STORED: ESteamLearnSnapshotProjectResult
STEAMLEARN_SNAPSHOT_PROJECT_SUCCESS_QUEUED: ESteamLearnSnapshotProjectResult
STEAMLEARN_SNAPSHOT_PROJECT_ERROR_INVALID_PROJECT_ID: ESteamLearnSnapshotProjectResult
STEAMLEARN_SNAPSHOT_PROJECT_ERROR_UNKNOWN_DATA_SOURCE: ESteamLearnSnapshotProjectResult
STEAMLEARN_SNAPSHOT_PROJECT_ERROR_INVALID_DATA_SOURCE_KEY: ESteamLearnSnapshotProjectResult
STEAMLEARN_SNAPSHOT_PROJECT_ERROR_MISSING_CACHE_DURATION: ESteamLearnSnapshotProjectResult
STEAMLEARN_SNAPSHOT_PROJECT_ERROR_NO_PUBLISHED_CONFIG: ESteamLearnSnapshotProjectResult
STEAMLEARN_SNAPSHOT_PROJECT_ERROR_FORBIDDEN: ESteamLearnSnapshotProjectResult
STEAMLEARN_SNAPSHOT_PROJECT_ERROR_INVALID_TIMESTAMP: ESteamLearnSnapshotProjectResult
STEAMLEARN_SNAPSHOT_PROJECT_ERROR_INTERNAL_DATA_SOURCE_ERROR: ESteamLearnSnapshotProjectResult
STEAMLEARN_SNAPSHOT_PROJECT_DISABLED: ESteamLearnSnapshotProjectResult
STEAMLEARN_SNAPSHOT_PROJECT_ERROR_INVALID_PUBLISHED_VERSION: ESteamLearnSnapshotProjectResult
STEAMLEARN_GET_ACCESS_TOKENS_ERROR: ESteamLearnGetAccessTokensResult
STEAMLEARN_GET_ACCESS_TOKENS_SUCCESS: ESteamLearnGetAccessTokensResult
STEAMLEARN_INFERENCE_ERROR: ESteamLearnInferenceResult
STEAMLEARN_INFERENCE_SUCCESS: ESteamLearnInferenceResult
STEAMLEARN_INFERENCE_ERROR_INVALID_PROJECT_ID: ESteamLearnInferenceResult
STEAMLEARN_INFERENCE_ERROR_MISSING_CACHED_SCHEMA_DATA: ESteamLearnInferenceResult
STEAMLEARN_INFERENCE_ERROR_NO_PUBLISHED_CONFIG: ESteamLearnInferenceResult
STEAMLEARN_INFERENCE_ERROR_FORBIDDEN: ESteamLearnInferenceResult
STEAMLEARN_INFERENCE_ERROR_INVALID_TIMESTAMP: ESteamLearnInferenceResult
STEAMLEARN_INFERENCE_ERROR_INVALID_PUBLISHED_VERSION: ESteamLearnInferenceResult
STEAMLEARN_INFERENCE_ERROR_NO_FETCH_ID_FOUND: ESteamLearnInferenceResult
STEAMLEARN_INFERENCE_ERROR_TOO_BUSY: ESteamLearnInferenceResult
STEAMLEARN_INFERENCE_ERROR_UNSUPPLIED_DATA_FAIL: ESteamLearnInferenceResult
STEAMLEARN_INFERENCE_ERROR_UNSUPPLIED_DATA_NO_KEYS: ESteamLearnInferenceResult
STEAMLEARN_INFERENCE_DISABLED: ESteamLearnInferenceResult
STEAMLEARN_INFERENCE_ERROR_NO_OUTPUT: ESteamLearnInferenceResult
STEAMLEARN_INFERENCE_ERROR_INVALID_NAMED_INFERENCE: ESteamLearnInferenceResult
STEAMLEARN_INFERENCE_METADATA_ERROR: ESteamLearnInferenceMetadataResult
STEAMLEARN_INFERENCE_METADATA_SUCCESS: ESteamLearnInferenceMetadataResult
STEAMLEARN_INFERENCE_METADATA_ERROR_INVALID_PROJECT_ID: ESteamLearnInferenceMetadataResult
STEAMLEARN_INFERENCE_METADATA_ERROR_NO_PUBLISHED_CONFIG: ESteamLearnInferenceMetadataResult
STEAMLEARN_INFERENCE_METADATA_ERROR_FORBIDDEN: ESteamLearnInferenceMetadataResult
STEAMLEARN_INFERENCE_METADATA_ERROR_INVALID_TIMESTAMP: ESteamLearnInferenceMetadataResult
STEAMLEARN_INFERENCE_METADATA_ERROR_INVALID_PUBLISHED_VERSION: ESteamLearnInferenceMetadataResult
STEAMLEARN_INFERENCE_METADATA_ERROR_NO_FETCH_ID_FOUND: ESteamLearnInferenceMetadataResult

class CMsgSteamLearnDataSourceDescObject(_message.Message):
    __slots__ = ("elements",)
    ELEMENTS_FIELD_NUMBER: _ClassVar[int]
    elements: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearnDataSourceDescElement]
    def __init__(self, elements: _Optional[_Iterable[_Union[CMsgSteamLearnDataSourceDescElement, _Mapping]]] = ...) -> None: ...

class CMsgSteamLearnDataSourceDescElement(_message.Message):
    __slots__ = ("name", "data_type", "object", "count")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    name: str
    data_type: ESteamLearnDataType
    object: CMsgSteamLearnDataSourceDescObject
    count: int
    def __init__(self, name: _Optional[str] = ..., data_type: _Optional[_Union[ESteamLearnDataType, str]] = ..., object: _Optional[_Union[CMsgSteamLearnDataSourceDescObject, _Mapping]] = ..., count: _Optional[int] = ...) -> None: ...

class CMsgSteamLearnDataSource(_message.Message):
    __slots__ = ("id", "name", "version", "source_description", "structure", "structure_crc", "cache_duration_seconds")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    SOURCE_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STRUCTURE_FIELD_NUMBER: _ClassVar[int]
    STRUCTURE_CRC_FIELD_NUMBER: _ClassVar[int]
    CACHE_DURATION_SECONDS_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    version: int
    source_description: str
    structure: CMsgSteamLearnDataSourceDescObject
    structure_crc: int
    cache_duration_seconds: int
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., version: _Optional[int] = ..., source_description: _Optional[str] = ..., structure: _Optional[_Union[CMsgSteamLearnDataSourceDescObject, _Mapping]] = ..., structure_crc: _Optional[int] = ..., cache_duration_seconds: _Optional[int] = ...) -> None: ...

class CMsgSteamLearnDataObject(_message.Message):
    __slots__ = ("elements",)
    ELEMENTS_FIELD_NUMBER: _ClassVar[int]
    elements: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearnDataElement]
    def __init__(self, elements: _Optional[_Iterable[_Union[CMsgSteamLearnDataElement, _Mapping]]] = ...) -> None: ...

class CMsgSteamLearnDataElement(_message.Message):
    __slots__ = ("name", "data_int32s", "data_floats", "data_bools", "data_strings", "data_objects")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_INT32S_FIELD_NUMBER: _ClassVar[int]
    DATA_FLOATS_FIELD_NUMBER: _ClassVar[int]
    DATA_BOOLS_FIELD_NUMBER: _ClassVar[int]
    DATA_STRINGS_FIELD_NUMBER: _ClassVar[int]
    DATA_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    name: str
    data_int32s: _containers.RepeatedScalarFieldContainer[int]
    data_floats: _containers.RepeatedScalarFieldContainer[float]
    data_bools: _containers.RepeatedScalarFieldContainer[bool]
    data_strings: _containers.RepeatedScalarFieldContainer[str]
    data_objects: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearnDataObject]
    def __init__(self, name: _Optional[str] = ..., data_int32s: _Optional[_Iterable[int]] = ..., data_floats: _Optional[_Iterable[float]] = ..., data_bools: _Optional[_Iterable[bool]] = ..., data_strings: _Optional[_Iterable[str]] = ..., data_objects: _Optional[_Iterable[_Union[CMsgSteamLearnDataObject, _Mapping]]] = ...) -> None: ...

class CMsgSteamLearnData(_message.Message):
    __slots__ = ("data_source_id", "keys", "data_object")
    DATA_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    DATA_OBJECT_FIELD_NUMBER: _ClassVar[int]
    data_source_id: int
    keys: _containers.RepeatedScalarFieldContainer[int]
    data_object: CMsgSteamLearnDataObject
    def __init__(self, data_source_id: _Optional[int] = ..., keys: _Optional[_Iterable[int]] = ..., data_object: _Optional[_Union[CMsgSteamLearnDataObject, _Mapping]] = ...) -> None: ...

class CMsgSteamLearnDataList(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearnData]
    def __init__(self, data: _Optional[_Iterable[_Union[CMsgSteamLearnData, _Mapping]]] = ...) -> None: ...

class CMsgSteamLearn_RegisterDataSource_Request(_message.Message):
    __slots__ = ("access_token", "data_source")
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    data_source: CMsgSteamLearnDataSource
    def __init__(self, access_token: _Optional[str] = ..., data_source: _Optional[_Union[CMsgSteamLearnDataSource, _Mapping]] = ...) -> None: ...

class CMsgSteamLearn_RegisterDataSource_Response(_message.Message):
    __slots__ = ("result", "data_source")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_FIELD_NUMBER: _ClassVar[int]
    result: ESteammLearnRegisterDataSourceResult
    data_source: CMsgSteamLearnDataSource
    def __init__(self, result: _Optional[_Union[ESteammLearnRegisterDataSourceResult, str]] = ..., data_source: _Optional[_Union[CMsgSteamLearnDataSource, _Mapping]] = ...) -> None: ...

class CMsgSteamLearn_CacheData_Request(_message.Message):
    __slots__ = ("access_token", "data")
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    data: CMsgSteamLearnData
    def __init__(self, access_token: _Optional[str] = ..., data: _Optional[_Union[CMsgSteamLearnData, _Mapping]] = ...) -> None: ...

class CMsgSteamLearn_CacheData_Response(_message.Message):
    __slots__ = ("cache_data_result",)
    CACHE_DATA_RESULT_FIELD_NUMBER: _ClassVar[int]
    cache_data_result: ESteamLearnCacheDataResult
    def __init__(self, cache_data_result: _Optional[_Union[ESteamLearnCacheDataResult, str]] = ...) -> None: ...

class CMsgSteamLearn_SnapshotProject_Request(_message.Message):
    __slots__ = ("access_token", "project_id", "published_version", "keys", "data", "pending_data_limit_seconds")
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    PUBLISHED_VERSION_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    PENDING_DATA_LIMIT_SECONDS_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    project_id: int
    published_version: int
    keys: _containers.RepeatedScalarFieldContainer[int]
    data: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearnData]
    pending_data_limit_seconds: int
    def __init__(self, access_token: _Optional[str] = ..., project_id: _Optional[int] = ..., published_version: _Optional[int] = ..., keys: _Optional[_Iterable[int]] = ..., data: _Optional[_Iterable[_Union[CMsgSteamLearnData, _Mapping]]] = ..., pending_data_limit_seconds: _Optional[int] = ...) -> None: ...

class CMsgSteamLearn_SnapshotProject_Response(_message.Message):
    __slots__ = ("snapshot_result",)
    SNAPSHOT_RESULT_FIELD_NUMBER: _ClassVar[int]
    snapshot_result: ESteamLearnSnapshotProjectResult
    def __init__(self, snapshot_result: _Optional[_Union[ESteamLearnSnapshotProjectResult, str]] = ...) -> None: ...

class CMsgSteamLearn_BatchOperation_Request(_message.Message):
    __slots__ = ("cache_data_requests", "snapshot_requests", "inference_requests")
    CACHE_DATA_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    INFERENCE_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    cache_data_requests: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearn_CacheData_Request]
    snapshot_requests: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearn_SnapshotProject_Request]
    inference_requests: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearn_Inference_Request]
    def __init__(self, cache_data_requests: _Optional[_Iterable[_Union[CMsgSteamLearn_CacheData_Request, _Mapping]]] = ..., snapshot_requests: _Optional[_Iterable[_Union[CMsgSteamLearn_SnapshotProject_Request, _Mapping]]] = ..., inference_requests: _Optional[_Iterable[_Union[CMsgSteamLearn_Inference_Request, _Mapping]]] = ...) -> None: ...

class CMsgSteamLearn_BatchOperation_Response(_message.Message):
    __slots__ = ("cache_data_responses", "snapshot_responses", "inference_responses")
    CACHE_DATA_RESPONSES_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_RESPONSES_FIELD_NUMBER: _ClassVar[int]
    INFERENCE_RESPONSES_FIELD_NUMBER: _ClassVar[int]
    cache_data_responses: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearn_CacheData_Response]
    snapshot_responses: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearn_SnapshotProject_Response]
    inference_responses: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearn_Inference_Response]
    def __init__(self, cache_data_responses: _Optional[_Iterable[_Union[CMsgSteamLearn_CacheData_Response, _Mapping]]] = ..., snapshot_responses: _Optional[_Iterable[_Union[CMsgSteamLearn_SnapshotProject_Response, _Mapping]]] = ..., inference_responses: _Optional[_Iterable[_Union[CMsgSteamLearn_Inference_Response, _Mapping]]] = ...) -> None: ...

class CMsgSteamLearnAccessTokens(_message.Message):
    __slots__ = ("register_data_source_access_token", "cache_data_access_tokens", "snapshot_project_access_tokens", "inference_access_tokens")
    class CacheDataAccessToken(_message.Message):
        __slots__ = ("data_source_id", "access_token")
        DATA_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
        ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
        data_source_id: int
        access_token: str
        def __init__(self, data_source_id: _Optional[int] = ..., access_token: _Optional[str] = ...) -> None: ...
    class SnapshotProjectAccessToken(_message.Message):
        __slots__ = ("project_id", "access_token")
        PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
        ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
        project_id: int
        access_token: str
        def __init__(self, project_id: _Optional[int] = ..., access_token: _Optional[str] = ...) -> None: ...
    class InferenceAccessToken(_message.Message):
        __slots__ = ("project_id", "access_token")
        PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
        ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
        project_id: int
        access_token: str
        def __init__(self, project_id: _Optional[int] = ..., access_token: _Optional[str] = ...) -> None: ...
    REGISTER_DATA_SOURCE_ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CACHE_DATA_ACCESS_TOKENS_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_PROJECT_ACCESS_TOKENS_FIELD_NUMBER: _ClassVar[int]
    INFERENCE_ACCESS_TOKENS_FIELD_NUMBER: _ClassVar[int]
    register_data_source_access_token: str
    cache_data_access_tokens: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearnAccessTokens.CacheDataAccessToken]
    snapshot_project_access_tokens: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearnAccessTokens.SnapshotProjectAccessToken]
    inference_access_tokens: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearnAccessTokens.InferenceAccessToken]
    def __init__(self, register_data_source_access_token: _Optional[str] = ..., cache_data_access_tokens: _Optional[_Iterable[_Union[CMsgSteamLearnAccessTokens.CacheDataAccessToken, _Mapping]]] = ..., snapshot_project_access_tokens: _Optional[_Iterable[_Union[CMsgSteamLearnAccessTokens.SnapshotProjectAccessToken, _Mapping]]] = ..., inference_access_tokens: _Optional[_Iterable[_Union[CMsgSteamLearnAccessTokens.InferenceAccessToken, _Mapping]]] = ...) -> None: ...

class CMsgSteamLearn_GetAccessTokens_Request(_message.Message):
    __slots__ = ("appid",)
    APPID_FIELD_NUMBER: _ClassVar[int]
    appid: int
    def __init__(self, appid: _Optional[int] = ...) -> None: ...

class CMsgSteamLearn_GetAccessTokens_Response(_message.Message):
    __slots__ = ("result", "access_tokens")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKENS_FIELD_NUMBER: _ClassVar[int]
    result: ESteamLearnGetAccessTokensResult
    access_tokens: CMsgSteamLearnAccessTokens
    def __init__(self, result: _Optional[_Union[ESteamLearnGetAccessTokensResult, str]] = ..., access_tokens: _Optional[_Union[CMsgSteamLearnAccessTokens, _Mapping]] = ...) -> None: ...

class CMsgInferenceIterateBeamSearch(_message.Message):
    __slots__ = ("beam_length", "beam_width", "item_decay", "next_item_count", "item_scalars", "item_sequence_end", "item_sequence_end_threshold", "repeat_multiplier")
    class CustomItemScalar(_message.Message):
        __slots__ = ("item", "scale")
        ITEM_FIELD_NUMBER: _ClassVar[int]
        SCALE_FIELD_NUMBER: _ClassVar[int]
        item: int
        scale: float
        def __init__(self, item: _Optional[int] = ..., scale: _Optional[float] = ...) -> None: ...
    BEAM_LENGTH_FIELD_NUMBER: _ClassVar[int]
    BEAM_WIDTH_FIELD_NUMBER: _ClassVar[int]
    ITEM_DECAY_FIELD_NUMBER: _ClassVar[int]
    NEXT_ITEM_COUNT_FIELD_NUMBER: _ClassVar[int]
    ITEM_SCALARS_FIELD_NUMBER: _ClassVar[int]
    ITEM_SEQUENCE_END_FIELD_NUMBER: _ClassVar[int]
    ITEM_SEQUENCE_END_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    REPEAT_MULTIPLIER_FIELD_NUMBER: _ClassVar[int]
    beam_length: int
    beam_width: int
    item_decay: float
    next_item_count: int
    item_scalars: _containers.RepeatedCompositeFieldContainer[CMsgInferenceIterateBeamSearch.CustomItemScalar]
    item_sequence_end: int
    item_sequence_end_threshold: float
    repeat_multiplier: float
    def __init__(self, beam_length: _Optional[int] = ..., beam_width: _Optional[int] = ..., item_decay: _Optional[float] = ..., next_item_count: _Optional[int] = ..., item_scalars: _Optional[_Iterable[_Union[CMsgInferenceIterateBeamSearch.CustomItemScalar, _Mapping]]] = ..., item_sequence_end: _Optional[int] = ..., item_sequence_end_threshold: _Optional[float] = ..., repeat_multiplier: _Optional[float] = ...) -> None: ...

class CMsgSteamLearn_Inference_Request(_message.Message):
    __slots__ = ("access_token", "project_id", "published_version", "override_train_id", "data", "additional_data", "keys", "named_inference", "iterate_beam_search", "debug_spew")
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    PUBLISHED_VERSION_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_TRAIN_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_DATA_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    NAMED_INFERENCE_FIELD_NUMBER: _ClassVar[int]
    ITERATE_BEAM_SEARCH_FIELD_NUMBER: _ClassVar[int]
    DEBUG_SPEW_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    project_id: int
    published_version: int
    override_train_id: int
    data: CMsgSteamLearnDataList
    additional_data: _containers.RepeatedScalarFieldContainer[float]
    keys: _containers.RepeatedScalarFieldContainer[int]
    named_inference: str
    iterate_beam_search: CMsgInferenceIterateBeamSearch
    debug_spew: int
    def __init__(self, access_token: _Optional[str] = ..., project_id: _Optional[int] = ..., published_version: _Optional[int] = ..., override_train_id: _Optional[int] = ..., data: _Optional[_Union[CMsgSteamLearnDataList, _Mapping]] = ..., additional_data: _Optional[_Iterable[float]] = ..., keys: _Optional[_Iterable[int]] = ..., named_inference: _Optional[str] = ..., iterate_beam_search: _Optional[_Union[CMsgInferenceIterateBeamSearch, _Mapping]] = ..., debug_spew: _Optional[int] = ...) -> None: ...

class CMsgSteamLearn_InferenceMetadata_Request(_message.Message):
    __slots__ = ("access_token", "project_id", "published_version", "override_train_id")
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    PUBLISHED_VERSION_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_TRAIN_ID_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    project_id: int
    published_version: int
    override_train_id: int
    def __init__(self, access_token: _Optional[str] = ..., project_id: _Optional[int] = ..., published_version: _Optional[int] = ..., override_train_id: _Optional[int] = ...) -> None: ...

class CMsgSteamLearn_InferenceMetadataBackend_Request(_message.Message):
    __slots__ = ("project_id", "fetch_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    FETCH_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: int
    fetch_id: int
    def __init__(self, project_id: _Optional[int] = ..., fetch_id: _Optional[int] = ...) -> None: ...

class CMsgSteamLearn_InferenceMetadata_Response(_message.Message):
    __slots__ = ("inference_metadata_result", "row_range", "ranges", "std_devs", "compact_tables", "sequence_tables", "kmeans", "app_info", "snapshot_histogram")
    class RowRange(_message.Message):
        __slots__ = ("min_row", "max_row")
        MIN_ROW_FIELD_NUMBER: _ClassVar[int]
        MAX_ROW_FIELD_NUMBER: _ClassVar[int]
        min_row: int
        max_row: int
        def __init__(self, min_row: _Optional[int] = ..., max_row: _Optional[int] = ...) -> None: ...
    class Range(_message.Message):
        __slots__ = ("data_element_path", "min_value", "max_value")
        DATA_ELEMENT_PATH_FIELD_NUMBER: _ClassVar[int]
        MIN_VALUE_FIELD_NUMBER: _ClassVar[int]
        MAX_VALUE_FIELD_NUMBER: _ClassVar[int]
        data_element_path: str
        min_value: float
        max_value: float
        def __init__(self, data_element_path: _Optional[str] = ..., min_value: _Optional[float] = ..., max_value: _Optional[float] = ...) -> None: ...
    class StdDev(_message.Message):
        __slots__ = ("data_element_path", "mean", "std_dev")
        DATA_ELEMENT_PATH_FIELD_NUMBER: _ClassVar[int]
        MEAN_FIELD_NUMBER: _ClassVar[int]
        STD_DEV_FIELD_NUMBER: _ClassVar[int]
        data_element_path: str
        mean: float
        std_dev: float
        def __init__(self, data_element_path: _Optional[str] = ..., mean: _Optional[float] = ..., std_dev: _Optional[float] = ...) -> None: ...
    class CompactTable(_message.Message):
        __slots__ = ("name", "map_values", "map_mappings")
        class Entry(_message.Message):
            __slots__ = ("value", "mapping", "count")
            VALUE_FIELD_NUMBER: _ClassVar[int]
            MAPPING_FIELD_NUMBER: _ClassVar[int]
            COUNT_FIELD_NUMBER: _ClassVar[int]
            value: int
            mapping: int
            count: int
            def __init__(self, value: _Optional[int] = ..., mapping: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
        class MapValuesEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: int
            value: CMsgSteamLearn_InferenceMetadata_Response.CompactTable.Entry
            def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[CMsgSteamLearn_InferenceMetadata_Response.CompactTable.Entry, _Mapping]] = ...) -> None: ...
        class MapMappingsEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: int
            value: CMsgSteamLearn_InferenceMetadata_Response.CompactTable.Entry
            def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[CMsgSteamLearn_InferenceMetadata_Response.CompactTable.Entry, _Mapping]] = ...) -> None: ...
        NAME_FIELD_NUMBER: _ClassVar[int]
        MAP_VALUES_FIELD_NUMBER: _ClassVar[int]
        MAP_MAPPINGS_FIELD_NUMBER: _ClassVar[int]
        name: str
        map_values: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearn_InferenceMetadata_Response.CompactTable.MapValuesEntry]
        map_mappings: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearn_InferenceMetadata_Response.CompactTable.MapMappingsEntry]
        def __init__(self, name: _Optional[str] = ..., map_values: _Optional[_Iterable[_Union[CMsgSteamLearn_InferenceMetadata_Response.CompactTable.MapValuesEntry, _Mapping]]] = ..., map_mappings: _Optional[_Iterable[_Union[CMsgSteamLearn_InferenceMetadata_Response.CompactTable.MapMappingsEntry, _Mapping]]] = ...) -> None: ...
    class SequenceTable(_message.Message):
        __slots__ = ("name", "map_values", "map_mappings", "total_count")
        class Entry(_message.Message):
            __slots__ = ("values", "crc", "count")
            VALUES_FIELD_NUMBER: _ClassVar[int]
            CRC_FIELD_NUMBER: _ClassVar[int]
            COUNT_FIELD_NUMBER: _ClassVar[int]
            values: _containers.RepeatedScalarFieldContainer[int]
            crc: int
            count: int
            def __init__(self, values: _Optional[_Iterable[int]] = ..., crc: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
        class MapValuesEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: int
            value: CMsgSteamLearn_InferenceMetadata_Response.SequenceTable.Entry
            def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[CMsgSteamLearn_InferenceMetadata_Response.SequenceTable.Entry, _Mapping]] = ...) -> None: ...
        class MapMappingsEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: CMsgSteamLearn_InferenceMetadata_Response.SequenceTable.Entry
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[CMsgSteamLearn_InferenceMetadata_Response.SequenceTable.Entry, _Mapping]] = ...) -> None: ...
        NAME_FIELD_NUMBER: _ClassVar[int]
        MAP_VALUES_FIELD_NUMBER: _ClassVar[int]
        MAP_MAPPINGS_FIELD_NUMBER: _ClassVar[int]
        TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
        name: str
        map_values: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearn_InferenceMetadata_Response.SequenceTable.MapValuesEntry]
        map_mappings: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearn_InferenceMetadata_Response.SequenceTable.MapMappingsEntry]
        total_count: int
        def __init__(self, name: _Optional[str] = ..., map_values: _Optional[_Iterable[_Union[CMsgSteamLearn_InferenceMetadata_Response.SequenceTable.MapValuesEntry, _Mapping]]] = ..., map_mappings: _Optional[_Iterable[_Union[CMsgSteamLearn_InferenceMetadata_Response.SequenceTable.MapMappingsEntry, _Mapping]]] = ..., total_count: _Optional[int] = ...) -> None: ...
    class KMeans(_message.Message):
        __slots__ = ("name", "clusters")
        class Cluster(_message.Message):
            __slots__ = ("x", "y", "radius", "radius_75pct", "radius_50pct", "radius_25pct")
            X_FIELD_NUMBER: _ClassVar[int]
            Y_FIELD_NUMBER: _ClassVar[int]
            RADIUS_FIELD_NUMBER: _ClassVar[int]
            RADIUS_75PCT_FIELD_NUMBER: _ClassVar[int]
            RADIUS_50PCT_FIELD_NUMBER: _ClassVar[int]
            RADIUS_25PCT_FIELD_NUMBER: _ClassVar[int]
            x: float
            y: float
            radius: float
            radius_75pct: float
            radius_50pct: float
            radius_25pct: float
            def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ..., radius: _Optional[float] = ..., radius_75pct: _Optional[float] = ..., radius_50pct: _Optional[float] = ..., radius_25pct: _Optional[float] = ...) -> None: ...
        NAME_FIELD_NUMBER: _ClassVar[int]
        CLUSTERS_FIELD_NUMBER: _ClassVar[int]
        name: str
        clusters: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearn_InferenceMetadata_Response.KMeans.Cluster]
        def __init__(self, name: _Optional[str] = ..., clusters: _Optional[_Iterable[_Union[CMsgSteamLearn_InferenceMetadata_Response.KMeans.Cluster, _Mapping]]] = ...) -> None: ...
    class SnapshotHistogram(_message.Message):
        __slots__ = ("min_value", "max_value", "num_buckets", "bucket_counts")
        MIN_VALUE_FIELD_NUMBER: _ClassVar[int]
        MAX_VALUE_FIELD_NUMBER: _ClassVar[int]
        NUM_BUCKETS_FIELD_NUMBER: _ClassVar[int]
        BUCKET_COUNTS_FIELD_NUMBER: _ClassVar[int]
        min_value: float
        max_value: float
        num_buckets: int
        bucket_counts: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, min_value: _Optional[float] = ..., max_value: _Optional[float] = ..., num_buckets: _Optional[int] = ..., bucket_counts: _Optional[_Iterable[int]] = ...) -> None: ...
    class AppInfo(_message.Message):
        __slots__ = ("country_allow", "country_deny", "platform_win", "platform_mac", "platform_linux", "adult_violence", "adult_sex")
        COUNTRY_ALLOW_FIELD_NUMBER: _ClassVar[int]
        COUNTRY_DENY_FIELD_NUMBER: _ClassVar[int]
        PLATFORM_WIN_FIELD_NUMBER: _ClassVar[int]
        PLATFORM_MAC_FIELD_NUMBER: _ClassVar[int]
        PLATFORM_LINUX_FIELD_NUMBER: _ClassVar[int]
        ADULT_VIOLENCE_FIELD_NUMBER: _ClassVar[int]
        ADULT_SEX_FIELD_NUMBER: _ClassVar[int]
        country_allow: str
        country_deny: str
        platform_win: bool
        platform_mac: bool
        platform_linux: bool
        adult_violence: bool
        adult_sex: bool
        def __init__(self, country_allow: _Optional[str] = ..., country_deny: _Optional[str] = ..., platform_win: bool = ..., platform_mac: bool = ..., platform_linux: bool = ..., adult_violence: bool = ..., adult_sex: bool = ...) -> None: ...
    class AppInfoEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: CMsgSteamLearn_InferenceMetadata_Response.AppInfo
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[CMsgSteamLearn_InferenceMetadata_Response.AppInfo, _Mapping]] = ...) -> None: ...
    INFERENCE_METADATA_RESULT_FIELD_NUMBER: _ClassVar[int]
    ROW_RANGE_FIELD_NUMBER: _ClassVar[int]
    RANGES_FIELD_NUMBER: _ClassVar[int]
    STD_DEVS_FIELD_NUMBER: _ClassVar[int]
    COMPACT_TABLES_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_TABLES_FIELD_NUMBER: _ClassVar[int]
    KMEANS_FIELD_NUMBER: _ClassVar[int]
    APP_INFO_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_HISTOGRAM_FIELD_NUMBER: _ClassVar[int]
    inference_metadata_result: ESteamLearnInferenceMetadataResult
    row_range: CMsgSteamLearn_InferenceMetadata_Response.RowRange
    ranges: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearn_InferenceMetadata_Response.Range]
    std_devs: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearn_InferenceMetadata_Response.StdDev]
    compact_tables: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearn_InferenceMetadata_Response.CompactTable]
    sequence_tables: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearn_InferenceMetadata_Response.SequenceTable]
    kmeans: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearn_InferenceMetadata_Response.KMeans]
    app_info: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearn_InferenceMetadata_Response.AppInfoEntry]
    snapshot_histogram: CMsgSteamLearn_InferenceMetadata_Response.SnapshotHistogram
    def __init__(self, inference_metadata_result: _Optional[_Union[ESteamLearnInferenceMetadataResult, str]] = ..., row_range: _Optional[_Union[CMsgSteamLearn_InferenceMetadata_Response.RowRange, _Mapping]] = ..., ranges: _Optional[_Iterable[_Union[CMsgSteamLearn_InferenceMetadata_Response.Range, _Mapping]]] = ..., std_devs: _Optional[_Iterable[_Union[CMsgSteamLearn_InferenceMetadata_Response.StdDev, _Mapping]]] = ..., compact_tables: _Optional[_Iterable[_Union[CMsgSteamLearn_InferenceMetadata_Response.CompactTable, _Mapping]]] = ..., sequence_tables: _Optional[_Iterable[_Union[CMsgSteamLearn_InferenceMetadata_Response.SequenceTable, _Mapping]]] = ..., kmeans: _Optional[_Iterable[_Union[CMsgSteamLearn_InferenceMetadata_Response.KMeans, _Mapping]]] = ..., app_info: _Optional[_Iterable[_Union[CMsgSteamLearn_InferenceMetadata_Response.AppInfoEntry, _Mapping]]] = ..., snapshot_histogram: _Optional[_Union[CMsgSteamLearn_InferenceMetadata_Response.SnapshotHistogram, _Mapping]] = ...) -> None: ...

class CMsgSteamLearn_InferenceBackend_Response(_message.Message):
    __slots__ = ("outputs",)
    class Sequence(_message.Message):
        __slots__ = ("value",)
        VALUE_FIELD_NUMBER: _ClassVar[int]
        value: _containers.RepeatedScalarFieldContainer[float]
        def __init__(self, value: _Optional[_Iterable[float]] = ...) -> None: ...
    class RegressionOutput(_message.Message):
        __slots__ = ("value",)
        VALUE_FIELD_NUMBER: _ClassVar[int]
        value: float
        def __init__(self, value: _Optional[float] = ...) -> None: ...
    class NamedInferenceOutput(_message.Message):
        __slots__ = ("value",)
        VALUE_FIELD_NUMBER: _ClassVar[int]
        value: _containers.RepeatedScalarFieldContainer[float]
        def __init__(self, value: _Optional[_Iterable[float]] = ...) -> None: ...
    class BinaryCrossEntropyOutput(_message.Message):
        __slots__ = ("value",)
        VALUE_FIELD_NUMBER: _ClassVar[int]
        value: float
        def __init__(self, value: _Optional[float] = ...) -> None: ...
    class MutliBinaryCrossEntropyOutput(_message.Message):
        __slots__ = ("weight", "value", "value_sequence")
        WEIGHT_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        VALUE_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
        weight: _containers.RepeatedScalarFieldContainer[float]
        value: _containers.RepeatedScalarFieldContainer[float]
        value_sequence: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearn_InferenceBackend_Response.Sequence]
        def __init__(self, weight: _Optional[_Iterable[float]] = ..., value: _Optional[_Iterable[float]] = ..., value_sequence: _Optional[_Iterable[_Union[CMsgSteamLearn_InferenceBackend_Response.Sequence, _Mapping]]] = ...) -> None: ...
    class CategoricalCrossEntropyOutput(_message.Message):
        __slots__ = ("weight", "value", "value_sequence")
        WEIGHT_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        VALUE_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
        weight: _containers.RepeatedScalarFieldContainer[float]
        value: _containers.RepeatedScalarFieldContainer[float]
        value_sequence: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearn_InferenceBackend_Response.Sequence]
        def __init__(self, weight: _Optional[_Iterable[float]] = ..., value: _Optional[_Iterable[float]] = ..., value_sequence: _Optional[_Iterable[_Union[CMsgSteamLearn_InferenceBackend_Response.Sequence, _Mapping]]] = ...) -> None: ...
    class Output(_message.Message):
        __slots__ = ("binary_crossentropy", "categorical_crossentropy", "multi_binary_crossentropy", "regression", "named_inference")
        BINARY_CROSSENTROPY_FIELD_NUMBER: _ClassVar[int]
        CATEGORICAL_CROSSENTROPY_FIELD_NUMBER: _ClassVar[int]
        MULTI_BINARY_CROSSENTROPY_FIELD_NUMBER: _ClassVar[int]
        REGRESSION_FIELD_NUMBER: _ClassVar[int]
        NAMED_INFERENCE_FIELD_NUMBER: _ClassVar[int]
        binary_crossentropy: CMsgSteamLearn_InferenceBackend_Response.BinaryCrossEntropyOutput
        categorical_crossentropy: CMsgSteamLearn_InferenceBackend_Response.CategoricalCrossEntropyOutput
        multi_binary_crossentropy: CMsgSteamLearn_InferenceBackend_Response.MutliBinaryCrossEntropyOutput
        regression: CMsgSteamLearn_InferenceBackend_Response.RegressionOutput
        named_inference: CMsgSteamLearn_InferenceBackend_Response.NamedInferenceOutput
        def __init__(self, binary_crossentropy: _Optional[_Union[CMsgSteamLearn_InferenceBackend_Response.BinaryCrossEntropyOutput, _Mapping]] = ..., categorical_crossentropy: _Optional[_Union[CMsgSteamLearn_InferenceBackend_Response.CategoricalCrossEntropyOutput, _Mapping]] = ..., multi_binary_crossentropy: _Optional[_Union[CMsgSteamLearn_InferenceBackend_Response.MutliBinaryCrossEntropyOutput, _Mapping]] = ..., regression: _Optional[_Union[CMsgSteamLearn_InferenceBackend_Response.RegressionOutput, _Mapping]] = ..., named_inference: _Optional[_Union[CMsgSteamLearn_InferenceBackend_Response.NamedInferenceOutput, _Mapping]] = ...) -> None: ...
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    outputs: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearn_InferenceBackend_Response.Output]
    def __init__(self, outputs: _Optional[_Iterable[_Union[CMsgSteamLearn_InferenceBackend_Response.Output, _Mapping]]] = ...) -> None: ...

class CMsgSteamLearn_Inference_Response(_message.Message):
    __slots__ = ("inference_result", "backend_response", "keys")
    INFERENCE_RESULT_FIELD_NUMBER: _ClassVar[int]
    BACKEND_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    inference_result: ESteamLearnInferenceResult
    backend_response: CMsgSteamLearn_InferenceBackend_Response
    keys: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, inference_result: _Optional[_Union[ESteamLearnInferenceResult, str]] = ..., backend_response: _Optional[_Union[CMsgSteamLearn_InferenceBackend_Response, _Mapping]] = ..., keys: _Optional[_Iterable[int]] = ...) -> None: ...
