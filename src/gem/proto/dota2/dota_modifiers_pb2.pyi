import networkbasetypes_pb2 as _networkbasetypes_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DOTA_MODIFIER_ENTRY_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOTA_MODIFIER_ENTRY_TYPE_ACTIVE: _ClassVar[DOTA_MODIFIER_ENTRY_TYPE]
    DOTA_MODIFIER_ENTRY_TYPE_REMOVED: _ClassVar[DOTA_MODIFIER_ENTRY_TYPE]
DOTA_MODIFIER_ENTRY_TYPE_ACTIVE: DOTA_MODIFIER_ENTRY_TYPE
DOTA_MODIFIER_ENTRY_TYPE_REMOVED: DOTA_MODIFIER_ENTRY_TYPE

class CDOTAModifierBuffTableEntry(_message.Message):
    __slots__ = ("entry_type", "parent", "index", "serial_num", "modifier_class", "ability_level", "stack_count", "creation_time", "duration", "caster", "ability", "armor", "fade_time", "subtle", "channel_time", "v_start", "v_end", "portal_loop_appear", "portal_loop_disappear", "hero_loop_appear", "hero_loop_disappear", "movement_speed", "aura", "activity", "damage", "range", "dd_modifier_index", "dd_ability_id", "illusion_label", "active", "player_ids", "lua_name", "attack_speed", "aura_owner", "bonus_all_stats", "bonus_health", "bonus_mana", "custom_entity", "aura_within_range", "move_slow", "has_scepter", "has_shard")
    ENTRY_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    SERIAL_NUM_FIELD_NUMBER: _ClassVar[int]
    MODIFIER_CLASS_FIELD_NUMBER: _ClassVar[int]
    ABILITY_LEVEL_FIELD_NUMBER: _ClassVar[int]
    STACK_COUNT_FIELD_NUMBER: _ClassVar[int]
    CREATION_TIME_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    CASTER_FIELD_NUMBER: _ClassVar[int]
    ABILITY_FIELD_NUMBER: _ClassVar[int]
    ARMOR_FIELD_NUMBER: _ClassVar[int]
    FADE_TIME_FIELD_NUMBER: _ClassVar[int]
    SUBTLE_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_TIME_FIELD_NUMBER: _ClassVar[int]
    V_START_FIELD_NUMBER: _ClassVar[int]
    V_END_FIELD_NUMBER: _ClassVar[int]
    PORTAL_LOOP_APPEAR_FIELD_NUMBER: _ClassVar[int]
    PORTAL_LOOP_DISAPPEAR_FIELD_NUMBER: _ClassVar[int]
    HERO_LOOP_APPEAR_FIELD_NUMBER: _ClassVar[int]
    HERO_LOOP_DISAPPEAR_FIELD_NUMBER: _ClassVar[int]
    MOVEMENT_SPEED_FIELD_NUMBER: _ClassVar[int]
    AURA_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_FIELD_NUMBER: _ClassVar[int]
    DAMAGE_FIELD_NUMBER: _ClassVar[int]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    DD_MODIFIER_INDEX_FIELD_NUMBER: _ClassVar[int]
    DD_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    ILLUSION_LABEL_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    PLAYER_IDS_FIELD_NUMBER: _ClassVar[int]
    LUA_NAME_FIELD_NUMBER: _ClassVar[int]
    ATTACK_SPEED_FIELD_NUMBER: _ClassVar[int]
    AURA_OWNER_FIELD_NUMBER: _ClassVar[int]
    BONUS_ALL_STATS_FIELD_NUMBER: _ClassVar[int]
    BONUS_HEALTH_FIELD_NUMBER: _ClassVar[int]
    BONUS_MANA_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_ENTITY_FIELD_NUMBER: _ClassVar[int]
    AURA_WITHIN_RANGE_FIELD_NUMBER: _ClassVar[int]
    MOVE_SLOW_FIELD_NUMBER: _ClassVar[int]
    HAS_SCEPTER_FIELD_NUMBER: _ClassVar[int]
    HAS_SHARD_FIELD_NUMBER: _ClassVar[int]
    entry_type: DOTA_MODIFIER_ENTRY_TYPE
    parent: int
    index: int
    serial_num: int
    modifier_class: int
    ability_level: int
    stack_count: int
    creation_time: float
    duration: float
    caster: int
    ability: int
    armor: int
    fade_time: float
    subtle: bool
    channel_time: float
    v_start: _networkbasetypes_pb2.CMsgVector
    v_end: _networkbasetypes_pb2.CMsgVector
    portal_loop_appear: str
    portal_loop_disappear: str
    hero_loop_appear: str
    hero_loop_disappear: str
    movement_speed: int
    aura: bool
    activity: int
    damage: int
    range: int
    dd_modifier_index: int
    dd_ability_id: int
    illusion_label: str
    active: bool
    player_ids: str
    lua_name: str
    attack_speed: int
    aura_owner: int
    bonus_all_stats: int
    bonus_health: int
    bonus_mana: int
    custom_entity: int
    aura_within_range: bool
    move_slow: float
    has_scepter: bool
    has_shard: bool
    def __init__(self, entry_type: _Optional[_Union[DOTA_MODIFIER_ENTRY_TYPE, str]] = ..., parent: _Optional[int] = ..., index: _Optional[int] = ..., serial_num: _Optional[int] = ..., modifier_class: _Optional[int] = ..., ability_level: _Optional[int] = ..., stack_count: _Optional[int] = ..., creation_time: _Optional[float] = ..., duration: _Optional[float] = ..., caster: _Optional[int] = ..., ability: _Optional[int] = ..., armor: _Optional[int] = ..., fade_time: _Optional[float] = ..., subtle: bool = ..., channel_time: _Optional[float] = ..., v_start: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., v_end: _Optional[_Union[_networkbasetypes_pb2.CMsgVector, _Mapping]] = ..., portal_loop_appear: _Optional[str] = ..., portal_loop_disappear: _Optional[str] = ..., hero_loop_appear: _Optional[str] = ..., hero_loop_disappear: _Optional[str] = ..., movement_speed: _Optional[int] = ..., aura: bool = ..., activity: _Optional[int] = ..., damage: _Optional[int] = ..., range: _Optional[int] = ..., dd_modifier_index: _Optional[int] = ..., dd_ability_id: _Optional[int] = ..., illusion_label: _Optional[str] = ..., active: bool = ..., player_ids: _Optional[str] = ..., lua_name: _Optional[str] = ..., attack_speed: _Optional[int] = ..., aura_owner: _Optional[int] = ..., bonus_all_stats: _Optional[int] = ..., bonus_health: _Optional[int] = ..., bonus_mana: _Optional[int] = ..., custom_entity: _Optional[int] = ..., aura_within_range: bool = ..., move_slow: _Optional[float] = ..., has_scepter: bool = ..., has_shard: bool = ...) -> None: ...

class CDOTALuaModifierEntry(_message.Message):
    __slots__ = ("modifier_type", "modifier_filename")
    MODIFIER_TYPE_FIELD_NUMBER: _ClassVar[int]
    MODIFIER_FILENAME_FIELD_NUMBER: _ClassVar[int]
    modifier_type: int
    modifier_filename: str
    def __init__(self, modifier_type: _Optional[int] = ..., modifier_filename: _Optional[str] = ...) -> None: ...
