from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

import networkbasetypes_pb2 as _networkbasetypes_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class EBasePredictionEvents(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BPE_StringCommand: _ClassVar[EBasePredictionEvents]
    BPE_Teleport: _ClassVar[EBasePredictionEvents]
    BPE_Diagnostic: _ClassVar[EBasePredictionEvents]

BPE_StringCommand: EBasePredictionEvents
BPE_Teleport: EBasePredictionEvents
BPE_Diagnostic: EBasePredictionEvents

class CPredictionEvent_Teleport(_message.Message):
    __slots__ = ("origin", "angles", "drop_to_ground_range")
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    ANGLES_FIELD_NUMBER: _ClassVar[int]
    DROP_TO_GROUND_RANGE_FIELD_NUMBER: _ClassVar[int]
    origin: _networkbasetypes_pb2.CMsgVector
    angles: _networkbasetypes_pb2.CMsgQAngle
    drop_to_ground_range: float
    def __init__(
        self,
        origin: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
        angles: _networkbasetypes_pb2.CMsgQAngle | _Mapping | None = ...,
        drop_to_ground_range: float | None = ...,
    ) -> None: ...

class CPredictionEvent_StringCommand(_message.Message):
    __slots__ = ("command",)
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    command: str
    def __init__(self, command: str | None = ...) -> None: ...

class CPredictionEvent_Diagnostic(_message.Message):
    __slots__ = ("id", "requested_sync", "requested_player_index", "execution_sync")
    ID_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_SYNC_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_PLAYER_INDEX_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_SYNC_FIELD_NUMBER: _ClassVar[int]
    id: int
    requested_sync: int
    requested_player_index: int
    execution_sync: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        id: int | None = ...,
        requested_sync: int | None = ...,
        requested_player_index: int | None = ...,
        execution_sync: _Iterable[int] | None = ...,
    ) -> None: ...
