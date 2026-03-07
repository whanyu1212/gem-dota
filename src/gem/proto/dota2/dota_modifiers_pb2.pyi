from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

import networkbasetypes_pb2 as _networkbasetypes_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class DOTA_MODIFIER_ENTRY_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOTA_MODIFIER_ENTRY_TYPE_ACTIVE: _ClassVar[DOTA_MODIFIER_ENTRY_TYPE]
    DOTA_MODIFIER_ENTRY_TYPE_REMOVED: _ClassVar[DOTA_MODIFIER_ENTRY_TYPE]

DOTA_MODIFIER_ENTRY_TYPE_ACTIVE: DOTA_MODIFIER_ENTRY_TYPE
DOTA_MODIFIER_ENTRY_TYPE_REMOVED: DOTA_MODIFIER_ENTRY_TYPE

class CDOTAModifierBuffTableEntry(_message.Message):
    __slots__ = (
        "entry_type",
        "parent",
        "index",
        "serial_num",
        "modifier_class",
        "ability_level",
        "stack_count",
        "creation_time",
        "duration",
        "caster",
        "ability",
        "armor",
        "fade_time",
        "subtle",
        "channel_time",
        "v_start",
        "v_end",
        "portal_loop_appear",
        "portal_loop_disappear",
        "hero_loop_appear",
        "hero_loop_disappear",
        "movement_speed",
        "aura",
        "activity",
        "damage",
        "range",
        "dd_modifier_index",
        "dd_ability_id",
        "illusion_label",
        "active",
        "player_ids",
        "lua_name",
        "attack_speed",
        "aura_owner",
        "bonus_all_stats",
        "bonus_health",
        "bonus_mana",
        "custom_entity",
        "aura_within_range",
        "move_slow",
    )
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
    def __init__(
        self,
        entry_type: DOTA_MODIFIER_ENTRY_TYPE | str | None = ...,
        parent: int | None = ...,
        index: int | None = ...,
        serial_num: int | None = ...,
        modifier_class: int | None = ...,
        ability_level: int | None = ...,
        stack_count: int | None = ...,
        creation_time: float | None = ...,
        duration: float | None = ...,
        caster: int | None = ...,
        ability: int | None = ...,
        armor: int | None = ...,
        fade_time: float | None = ...,
        subtle: bool = ...,
        channel_time: float | None = ...,
        v_start: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
        v_end: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
        portal_loop_appear: str | None = ...,
        portal_loop_disappear: str | None = ...,
        hero_loop_appear: str | None = ...,
        hero_loop_disappear: str | None = ...,
        movement_speed: int | None = ...,
        aura: bool = ...,
        activity: int | None = ...,
        damage: int | None = ...,
        range: int | None = ...,
        dd_modifier_index: int | None = ...,
        dd_ability_id: int | None = ...,
        illusion_label: str | None = ...,
        active: bool = ...,
        player_ids: str | None = ...,
        lua_name: str | None = ...,
        attack_speed: int | None = ...,
        aura_owner: int | None = ...,
        bonus_all_stats: int | None = ...,
        bonus_health: int | None = ...,
        bonus_mana: int | None = ...,
        custom_entity: int | None = ...,
        aura_within_range: bool = ...,
        move_slow: float | None = ...,
    ) -> None: ...

class CDOTALuaModifierEntry(_message.Message):
    __slots__ = ("modifier_type", "modifier_filename")
    MODIFIER_TYPE_FIELD_NUMBER: _ClassVar[int]
    MODIFIER_FILENAME_FIELD_NUMBER: _ClassVar[int]
    modifier_type: int
    modifier_filename: str
    def __init__(
        self, modifier_type: int | None = ..., modifier_filename: str | None = ...
    ) -> None: ...
