import steammessages_pb2 as _steammessages_pb2
import dota_shared_enums_pb2 as _dota_shared_enums_pb2
import dota_gcmessages_common_pb2 as _dota_gcmessages_common_pb2
import gcsdk_gcmessages_pb2 as _gcsdk_gcmessages_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CMsgSurvivorsUserData(_message.Message):
    __slots__ = ("attribute_levels", "unlocked_difficulty")
    class AttributeLevelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    ATTRIBUTE_LEVELS_FIELD_NUMBER: _ClassVar[int]
    UNLOCKED_DIFFICULTY_FIELD_NUMBER: _ClassVar[int]
    attribute_levels: _containers.RepeatedCompositeFieldContainer[CMsgSurvivorsUserData.AttributeLevelsEntry]
    unlocked_difficulty: int
    def __init__(self, attribute_levels: _Optional[_Iterable[_Union[CMsgSurvivorsUserData.AttributeLevelsEntry, _Mapping]]] = ..., unlocked_difficulty: _Optional[int] = ...) -> None: ...

class CMsgClientToGCSurvivorsPowerUpTelemetryData(_message.Message):
    __slots__ = ("powerup_id", "level", "time_received", "time_held", "total_damage", "dps", "has_scepter")
    POWERUP_ID_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    TIME_RECEIVED_FIELD_NUMBER: _ClassVar[int]
    TIME_HELD_FIELD_NUMBER: _ClassVar[int]
    TOTAL_DAMAGE_FIELD_NUMBER: _ClassVar[int]
    DPS_FIELD_NUMBER: _ClassVar[int]
    HAS_SCEPTER_FIELD_NUMBER: _ClassVar[int]
    powerup_id: int
    level: int
    time_received: int
    time_held: int
    total_damage: int
    dps: int
    has_scepter: int
    def __init__(self, powerup_id: _Optional[int] = ..., level: _Optional[int] = ..., time_received: _Optional[int] = ..., time_held: _Optional[int] = ..., total_damage: _Optional[int] = ..., dps: _Optional[int] = ..., has_scepter: _Optional[int] = ...) -> None: ...

class CMsgClientToGCSurvivorsGameTelemetryData(_message.Message):
    __slots__ = ("time_survived", "player_level", "game_result", "gold_earned", "powerups", "difficulty", "metaprogression_level")
    TIME_SURVIVED_FIELD_NUMBER: _ClassVar[int]
    PLAYER_LEVEL_FIELD_NUMBER: _ClassVar[int]
    GAME_RESULT_FIELD_NUMBER: _ClassVar[int]
    GOLD_EARNED_FIELD_NUMBER: _ClassVar[int]
    POWERUPS_FIELD_NUMBER: _ClassVar[int]
    DIFFICULTY_FIELD_NUMBER: _ClassVar[int]
    METAPROGRESSION_LEVEL_FIELD_NUMBER: _ClassVar[int]
    time_survived: int
    player_level: int
    game_result: int
    gold_earned: int
    powerups: _containers.RepeatedCompositeFieldContainer[CMsgClientToGCSurvivorsPowerUpTelemetryData]
    difficulty: int
    metaprogression_level: int
    def __init__(self, time_survived: _Optional[int] = ..., player_level: _Optional[int] = ..., game_result: _Optional[int] = ..., gold_earned: _Optional[int] = ..., powerups: _Optional[_Iterable[_Union[CMsgClientToGCSurvivorsPowerUpTelemetryData, _Mapping]]] = ..., difficulty: _Optional[int] = ..., metaprogression_level: _Optional[int] = ...) -> None: ...

class CMsgClientToGCSurvivorsGameTelemetryDataResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCSurvivorsGameTelemetryDataResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCSurvivorsGameTelemetryDataResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCSurvivorsGameTelemetryDataResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCSurvivorsGameTelemetryDataResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCSurvivorsGameTelemetryDataResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCSurvivorsGameTelemetryDataResponse.EResponse]
        k_eInvalidItem: _ClassVar[CMsgClientToGCSurvivorsGameTelemetryDataResponse.EResponse]
    k_eInternalError: CMsgClientToGCSurvivorsGameTelemetryDataResponse.EResponse
    k_eSuccess: CMsgClientToGCSurvivorsGameTelemetryDataResponse.EResponse
    k_eTooBusy: CMsgClientToGCSurvivorsGameTelemetryDataResponse.EResponse
    k_eDisabled: CMsgClientToGCSurvivorsGameTelemetryDataResponse.EResponse
    k_eTimeout: CMsgClientToGCSurvivorsGameTelemetryDataResponse.EResponse
    k_eNotAllowed: CMsgClientToGCSurvivorsGameTelemetryDataResponse.EResponse
    k_eInvalidItem: CMsgClientToGCSurvivorsGameTelemetryDataResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCSurvivorsGameTelemetryDataResponse.EResponse
    def __init__(self, response: _Optional[_Union[CMsgClientToGCSurvivorsGameTelemetryDataResponse.EResponse, str]] = ...) -> None: ...
