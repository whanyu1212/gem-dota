from . import events_pb2 as _events_pb2
from . import event_gcmessages_common_pb2 as _event_gcmessages_common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EGCEventClientMessages(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EMsgClientToGCGetEventPoints: _ClassVar[EGCEventClientMessages]
    k_EMsgClientToGCGetEventPointsResponse: _ClassVar[EGCEventClientMessages]
    k_EMsgGCToClientEventPointsUpdated: _ClassVar[EGCEventClientMessages]
k_EMsgClientToGCGetEventPoints: EGCEventClientMessages
k_EMsgClientToGCGetEventPointsResponse: EGCEventClientMessages
k_EMsgGCToClientEventPointsUpdated: EGCEventClientMessages

class CMsgClientToGCGetEventPoints(_message.Message):
    __slots__ = ("event_id", "account_id")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: _events_pb2.EEvent
    account_id: int
    def __init__(self, event_id: _Optional[_Union[_events_pb2.EEvent, str]] = ..., account_id: _Optional[int] = ...) -> None: ...

class CMsgClientToGCGetEventPointsResponse(_message.Message):
    __slots__ = ("result", "event_points")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCGetEventPointsResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCGetEventPointsResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCGetEventPointsResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCGetEventPointsResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCGetEventPointsResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCGetEventPointsResponse.EResponse]
    k_eInternalError: CMsgClientToGCGetEventPointsResponse.EResponse
    k_eSuccess: CMsgClientToGCGetEventPointsResponse.EResponse
    k_eTooBusy: CMsgClientToGCGetEventPointsResponse.EResponse
    k_eDisabled: CMsgClientToGCGetEventPointsResponse.EResponse
    k_eTimeout: CMsgClientToGCGetEventPointsResponse.EResponse
    k_eNotAllowed: CMsgClientToGCGetEventPointsResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    EVENT_POINTS_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCGetEventPointsResponse.EResponse
    event_points: _event_gcmessages_common_pb2.CMsgUserEventPoints
    def __init__(self, result: _Optional[_Union[CMsgClientToGCGetEventPointsResponse.EResponse, str]] = ..., event_points: _Optional[_Union[_event_gcmessages_common_pb2.CMsgUserEventPoints, _Mapping]] = ...) -> None: ...

class CMsgGCToClientEventPointsUpdated(_message.Message):
    __slots__ = ("event_id", "event_points")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_POINTS_FIELD_NUMBER: _ClassVar[int]
    event_id: _events_pb2.EEvent
    event_points: _event_gcmessages_common_pb2.CMsgUserEventPoints
    def __init__(self, event_id: _Optional[_Union[_events_pb2.EEvent, str]] = ..., event_points: _Optional[_Union[_event_gcmessages_common_pb2.CMsgUserEventPoints, _Mapping]] = ...) -> None: ...
