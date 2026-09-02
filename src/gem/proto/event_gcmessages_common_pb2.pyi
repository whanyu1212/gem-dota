from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CMsgEventAction(_message.Message):
    __slots__ = ("action_id", "times_completed")
    ACTION_ID_FIELD_NUMBER: _ClassVar[int]
    TIMES_COMPLETED_FIELD_NUMBER: _ClassVar[int]
    action_id: int
    times_completed: int
    def __init__(self, action_id: _Optional[int] = ..., times_completed: _Optional[int] = ...) -> None: ...

class CMsgUserEventPoints(_message.Message):
    __slots__ = ("account_id", "event_id", "total_points", "total_premium_points", "points", "premium_points", "completed_actions", "owned", "active_season_id")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    TOTAL_POINTS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PREMIUM_POINTS_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    PREMIUM_POINTS_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_ACTIONS_FIELD_NUMBER: _ClassVar[int]
    OWNED_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    event_id: int
    total_points: int
    total_premium_points: int
    points: int
    premium_points: int
    completed_actions: _containers.RepeatedCompositeFieldContainer[CMsgEventAction]
    owned: bool
    active_season_id: int
    def __init__(self, account_id: _Optional[int] = ..., event_id: _Optional[int] = ..., total_points: _Optional[int] = ..., total_premium_points: _Optional[int] = ..., points: _Optional[int] = ..., premium_points: _Optional[int] = ..., completed_actions: _Optional[_Iterable[_Union[CMsgEventAction, _Mapping]]] = ..., owned: bool = ..., active_season_id: _Optional[int] = ...) -> None: ...
