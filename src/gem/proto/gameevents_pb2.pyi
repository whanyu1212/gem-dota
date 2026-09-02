from . import networkbasetypes_pb2 as _networkbasetypes_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EBaseGameEvents(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GE_VDebugGameSessionIDEvent: _ClassVar[EBaseGameEvents]
    GE_PlaceDecalEvent: _ClassVar[EBaseGameEvents]
    GE_ClearWorldDecalsEvent: _ClassVar[EBaseGameEvents]
    GE_ClearEntityDecalsEvent: _ClassVar[EBaseGameEvents]
    GE_ClearDecalsForEntityEvent: _ClassVar[EBaseGameEvents]
    GE_Source1LegacyGameEventList: _ClassVar[EBaseGameEvents]
    GE_Source1LegacyListenEvents: _ClassVar[EBaseGameEvents]
    GE_Source1LegacyGameEvent: _ClassVar[EBaseGameEvents]
    GE_SosStartSoundEvent: _ClassVar[EBaseGameEvents]
    GE_SosStopSoundEvent: _ClassVar[EBaseGameEvents]
    GE_SosSetSoundEventParams: _ClassVar[EBaseGameEvents]
    GE_SosSetLibraryStackFields: _ClassVar[EBaseGameEvents]
    GE_SosStopSoundEventHash: _ClassVar[EBaseGameEvents]
    GE_ClothStiffenAnimEvent: _ClassVar[EBaseGameEvents]
    GE_ClothEffectAnimEvent: _ClassVar[EBaseGameEvents]
GE_VDebugGameSessionIDEvent: EBaseGameEvents
GE_PlaceDecalEvent: EBaseGameEvents
GE_ClearWorldDecalsEvent: EBaseGameEvents
GE_ClearEntityDecalsEvent: EBaseGameEvents
GE_ClearDecalsForEntityEvent: EBaseGameEvents
GE_Source1LegacyGameEventList: EBaseGameEvents
GE_Source1LegacyListenEvents: EBaseGameEvents
GE_Source1LegacyGameEvent: EBaseGameEvents
GE_SosStartSoundEvent: EBaseGameEvents
GE_SosStopSoundEvent: EBaseGameEvents
GE_SosSetSoundEventParams: EBaseGameEvents
GE_SosSetLibraryStackFields: EBaseGameEvents
GE_SosStopSoundEventHash: EBaseGameEvents
GE_ClothStiffenAnimEvent: EBaseGameEvents
GE_ClothEffectAnimEvent: EBaseGameEvents

class CMsgVDebugGameSessionIDEvent(_message.Message):
    __slots__ = ("clientid", "gamesessionid")
    CLIENTID_FIELD_NUMBER: _ClassVar[int]
    GAMESESSIONID_FIELD_NUMBER: _ClassVar[int]
    clientid: int
    gamesessionid: str
    def __init__(self, clientid: _Optional[int] = ..., gamesessionid: _Optional[str] = ...) -> None: ...

class CMsgPlaceDecalEvent(_message.Message):
    __slots__ = ("position", "normal", "saxis", "boneindex", "triangleindex", "flags", "color", "random_seed", "decal_group_name", "size_override", "entityhandle", "material_id", "sequence_name", "position_objectspace", "normal_objectspace")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    NORMAL_FIELD_NUMBER: _ClassVar[int]
    SAXIS_FIELD_NUMBER: _ClassVar[int]
    BONEINDEX_FIELD_NUMBER: _ClassVar[int]
    TRIANGLEINDEX_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    RANDOM_SEED_FIELD_NUMBER: _ClassVar[int]
    DECAL_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    SIZE_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    ENTITYHANDLE_FIELD_NUMBER: _ClassVar[int]
    MATERIAL_ID_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_NAME_FIELD_NUMBER: _ClassVar[int]
    POSITION_OBJECTSPACE_FIELD_NUMBER: _ClassVar[int]
    NORMAL_OBJECTSPACE_FIELD_NUMBER: _ClassVar[int]
    position: _networkbasetypes_pb2.CMsgVector
    normal: _networkbasetypes_pb2.CMsgVector
    saxis: _networkbasetypes_pb2.CMsgVector
    boneindex: int
    triangleindex: int
    flags: int
    color: int
    random_seed: int
    decal_group_name: int
    size_override: float
    entityhandle: int
    material_id: int
    sequence_name: int
    position_objectspace: _networkbasetypes_pb2.CMsgVector
    normal_objectspace: _networkbasetypes_pb2.CMsgVector
    def __init__(self, position: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., normal: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., saxis: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., boneindex: _Optional[int] = ..., triangleindex: _Optional[int] = ..., flags: _Optional[int] = ..., color: _Optional[int] = ..., random_seed: _Optional[int] = ..., decal_group_name: _Optional[int] = ..., size_override: _Optional[float] = ..., entityhandle: _Optional[int] = ..., material_id: _Optional[int] = ..., sequence_name: _Optional[int] = ..., position_objectspace: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., normal_objectspace: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ...) -> None: ...

class CMsgClearWorldDecalsEvent(_message.Message):
    __slots__ = ("flagstoclear",)
    FLAGSTOCLEAR_FIELD_NUMBER: _ClassVar[int]
    flagstoclear: int
    def __init__(self, flagstoclear: _Optional[int] = ...) -> None: ...

class CMsgClearEntityDecalsEvent(_message.Message):
    __slots__ = ("flagstoclear",)
    FLAGSTOCLEAR_FIELD_NUMBER: _ClassVar[int]
    flagstoclear: int
    def __init__(self, flagstoclear: _Optional[int] = ...) -> None: ...

class CMsgClearDecalsForEntityEvent(_message.Message):
    __slots__ = ("flagstoclear", "entityhandle")
    FLAGSTOCLEAR_FIELD_NUMBER: _ClassVar[int]
    ENTITYHANDLE_FIELD_NUMBER: _ClassVar[int]
    flagstoclear: int
    entityhandle: int
    def __init__(self, flagstoclear: _Optional[int] = ..., entityhandle: _Optional[int] = ...) -> None: ...

class CMsgSource1LegacyGameEventList(_message.Message):
    __slots__ = ("descriptors",)
    class key_t(_message.Message):
        __slots__ = ("type", "name")
        TYPE_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        type: int
        name: str
        def __init__(self, type: _Optional[int] = ..., name: _Optional[str] = ...) -> None: ...
    class descriptor_t(_message.Message):
        __slots__ = ("eventid", "name", "keys")
        EVENTID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        KEYS_FIELD_NUMBER: _ClassVar[int]
        eventid: int
        name: str
        keys: _containers.RepeatedCompositeFieldContainer[CMsgSource1LegacyGameEventList.key_t]
        def __init__(self, eventid: _Optional[int] = ..., name: _Optional[str] = ..., keys: _Optional[_Iterable[_Union[CMsgSource1LegacyGameEventList.key_t, _Mapping]]] = ...) -> None: ...
    DESCRIPTORS_FIELD_NUMBER: _ClassVar[int]
    descriptors: _containers.RepeatedCompositeFieldContainer[CMsgSource1LegacyGameEventList.descriptor_t]
    def __init__(self, descriptors: _Optional[_Iterable[_Union[CMsgSource1LegacyGameEventList.descriptor_t, _Mapping]]] = ...) -> None: ...

class CMsgSource1LegacyListenEvents(_message.Message):
    __slots__ = ("playerslot", "eventarraybits")
    PLAYERSLOT_FIELD_NUMBER: _ClassVar[int]
    EVENTARRAYBITS_FIELD_NUMBER: _ClassVar[int]
    playerslot: int
    eventarraybits: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, playerslot: _Optional[int] = ..., eventarraybits: _Optional[_Iterable[int]] = ...) -> None: ...

class CMsgSource1LegacyGameEvent(_message.Message):
    __slots__ = ("event_name", "eventid", "keys", "server_tick", "passthrough")
    class key_t(_message.Message):
        __slots__ = ("type", "val_string", "val_float", "val_long", "val_short", "val_byte", "val_bool", "val_uint64")
        TYPE_FIELD_NUMBER: _ClassVar[int]
        VAL_STRING_FIELD_NUMBER: _ClassVar[int]
        VAL_FLOAT_FIELD_NUMBER: _ClassVar[int]
        VAL_LONG_FIELD_NUMBER: _ClassVar[int]
        VAL_SHORT_FIELD_NUMBER: _ClassVar[int]
        VAL_BYTE_FIELD_NUMBER: _ClassVar[int]
        VAL_BOOL_FIELD_NUMBER: _ClassVar[int]
        VAL_UINT64_FIELD_NUMBER: _ClassVar[int]
        type: int
        val_string: str
        val_float: float
        val_long: int
        val_short: int
        val_byte: int
        val_bool: bool
        val_uint64: int
        def __init__(self, type: _Optional[int] = ..., val_string: _Optional[str] = ..., val_float: _Optional[float] = ..., val_long: _Optional[int] = ..., val_short: _Optional[int] = ..., val_byte: _Optional[int] = ..., val_bool: bool = ..., val_uint64: _Optional[int] = ...) -> None: ...
    EVENT_NAME_FIELD_NUMBER: _ClassVar[int]
    EVENTID_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    SERVER_TICK_FIELD_NUMBER: _ClassVar[int]
    PASSTHROUGH_FIELD_NUMBER: _ClassVar[int]
    event_name: str
    eventid: int
    keys: _containers.RepeatedCompositeFieldContainer[CMsgSource1LegacyGameEvent.key_t]
    server_tick: int
    passthrough: int
    def __init__(self, event_name: _Optional[str] = ..., eventid: _Optional[int] = ..., keys: _Optional[_Iterable[_Union[CMsgSource1LegacyGameEvent.key_t, _Mapping]]] = ..., server_tick: _Optional[int] = ..., passthrough: _Optional[int] = ...) -> None: ...

class CMsgSosStartSoundEvent(_message.Message):
    __slots__ = ("soundevent_guid", "soundevent_hash", "source_entity_index", "seed", "packed_params", "start_time")
    SOUNDEVENT_GUID_FIELD_NUMBER: _ClassVar[int]
    SOUNDEVENT_HASH_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ENTITY_INDEX_FIELD_NUMBER: _ClassVar[int]
    SEED_FIELD_NUMBER: _ClassVar[int]
    PACKED_PARAMS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    soundevent_guid: int
    soundevent_hash: int
    source_entity_index: int
    seed: int
    packed_params: bytes
    start_time: float
    def __init__(self, soundevent_guid: _Optional[int] = ..., soundevent_hash: _Optional[int] = ..., source_entity_index: _Optional[int] = ..., seed: _Optional[int] = ..., packed_params: _Optional[bytes] = ..., start_time: _Optional[float] = ...) -> None: ...

class CMsgSosStopSoundEvent(_message.Message):
    __slots__ = ("soundevent_guid",)
    SOUNDEVENT_GUID_FIELD_NUMBER: _ClassVar[int]
    soundevent_guid: int
    def __init__(self, soundevent_guid: _Optional[int] = ...) -> None: ...

class CMsgSosStopSoundEventHash(_message.Message):
    __slots__ = ("soundevent_hash", "source_entity_index")
    SOUNDEVENT_HASH_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ENTITY_INDEX_FIELD_NUMBER: _ClassVar[int]
    soundevent_hash: int
    source_entity_index: int
    def __init__(self, soundevent_hash: _Optional[int] = ..., source_entity_index: _Optional[int] = ...) -> None: ...

class CMsgSosSetSoundEventParams(_message.Message):
    __slots__ = ("soundevent_guid", "packed_params")
    SOUNDEVENT_GUID_FIELD_NUMBER: _ClassVar[int]
    PACKED_PARAMS_FIELD_NUMBER: _ClassVar[int]
    soundevent_guid: int
    packed_params: bytes
    def __init__(self, soundevent_guid: _Optional[int] = ..., packed_params: _Optional[bytes] = ...) -> None: ...

class CMsgSosSetLibraryStackFields(_message.Message):
    __slots__ = ("stack_hash", "packed_fields")
    STACK_HASH_FIELD_NUMBER: _ClassVar[int]
    PACKED_FIELDS_FIELD_NUMBER: _ClassVar[int]
    stack_hash: int
    packed_fields: bytes
    def __init__(self, stack_hash: _Optional[int] = ..., packed_fields: _Optional[bytes] = ...) -> None: ...

class CMsgClothStiffenAnimEvent(_message.Message):
    __slots__ = ("source_entity_index", "vertex_set_hash", "intensity", "length", "speed_in", "speed_out")
    SOURCE_ENTITY_INDEX_FIELD_NUMBER: _ClassVar[int]
    VERTEX_SET_HASH_FIELD_NUMBER: _ClassVar[int]
    INTENSITY_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    SPEED_IN_FIELD_NUMBER: _ClassVar[int]
    SPEED_OUT_FIELD_NUMBER: _ClassVar[int]
    source_entity_index: int
    vertex_set_hash: int
    intensity: float
    length: float
    speed_in: float
    speed_out: float
    def __init__(self, source_entity_index: _Optional[int] = ..., vertex_set_hash: _Optional[int] = ..., intensity: _Optional[float] = ..., length: _Optional[float] = ..., speed_in: _Optional[float] = ..., speed_out: _Optional[float] = ...) -> None: ...

class CMsgClothEffectAnimEvent(_message.Message):
    __slots__ = ("source_entity_index", "effect_name_hash", "operation", "flags", "tags", "pte")
    SOURCE_ENTITY_INDEX_FIELD_NUMBER: _ClassVar[int]
    EFFECT_NAME_HASH_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    PTE_FIELD_NUMBER: _ClassVar[int]
    source_entity_index: int
    effect_name_hash: int
    operation: int
    flags: int
    tags: str
    pte: _networkbasetypes_pb2.CMsgVector
    def __init__(self, source_entity_index: _Optional[int] = ..., effect_name_hash: _Optional[int] = ..., operation: _Optional[int] = ..., flags: _Optional[int] = ..., tags: _Optional[str] = ..., pte: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ...) -> None: ...
