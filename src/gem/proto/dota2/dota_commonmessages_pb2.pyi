from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

import networkbasetypes_pb2 as _networkbasetypes_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class EPingSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_ePingSource_Default: _ClassVar[EPingSource]
    k_ePingSource_Warning: _ClassVar[EPingSource]
    k_ePingSource_Wheel: _ClassVar[EPingSource]
    k_ePingSource_System: _ClassVar[EPingSource]

class EDOTAStatPopupTypes(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EDOTA_SPT_Textline: _ClassVar[EDOTAStatPopupTypes]
    k_EDOTA_SPT_Basic: _ClassVar[EDOTAStatPopupTypes]
    k_EDOTA_SPT_Poll: _ClassVar[EDOTAStatPopupTypes]
    k_EDOTA_SPT_Grid: _ClassVar[EDOTAStatPopupTypes]
    k_EDOTA_SPT_DualImage: _ClassVar[EDOTAStatPopupTypes]
    k_EDOTA_SPT_Movie: _ClassVar[EDOTAStatPopupTypes]

class dotaunitorder_t(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOTA_UNIT_ORDER_NONE: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_MOVE_TO_POSITION: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_MOVE_TO_TARGET: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_ATTACK_MOVE: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_ATTACK_TARGET: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_CAST_POSITION: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_CAST_TARGET: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_CAST_TARGET_TREE: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_CAST_NO_TARGET: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_CAST_TOGGLE: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_HOLD_POSITION: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_TRAIN_ABILITY: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_DROP_ITEM: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_GIVE_ITEM: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_PICKUP_ITEM: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_PICKUP_RUNE: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_PURCHASE_ITEM: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_SELL_ITEM: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_DISASSEMBLE_ITEM: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_MOVE_ITEM: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_CAST_TOGGLE_AUTO: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_STOP: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_TAUNT: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_BUYBACK: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_GLYPH: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_EJECT_ITEM_FROM_STASH: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_CAST_RUNE: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_PING_ABILITY: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_MOVE_TO_DIRECTION: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_PATROL: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_VECTOR_TARGET_POSITION: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_RADAR: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_SET_ITEM_COMBINE_LOCK: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_CONTINUE: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_VECTOR_TARGET_CANCELED: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_CAST_RIVER_PAINT: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_PREGAME_ADJUST_ITEM_ASSIGNMENT: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_DROP_ITEM_AT_FOUNTAIN: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_TAKE_ITEM_FROM_NEUTRAL_ITEM_STASH: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_MOVE_RELATIVE: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_CAST_TOGGLE_ALT: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_CONSUME_ITEM: _ClassVar[dotaunitorder_t]
    DOTA_UNIT_ORDER_SET_ITEM_MARK_FOR_SELL: _ClassVar[dotaunitorder_t]

class EDOTAVersusScenePlayerBehavior(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VS_PLAYER_BEHAVIOR_PLAY_ACTIVITY: _ClassVar[EDOTAVersusScenePlayerBehavior]
    VS_PLAYER_BEHAVIOR_CHAT_WHEEL: _ClassVar[EDOTAVersusScenePlayerBehavior]
    VS_PLAYER_BEHAVIOR_PLAYBACK_RATE: _ClassVar[EDOTAVersusScenePlayerBehavior]

k_ePingSource_Default: EPingSource
k_ePingSource_Warning: EPingSource
k_ePingSource_Wheel: EPingSource
k_ePingSource_System: EPingSource
k_EDOTA_SPT_Textline: EDOTAStatPopupTypes
k_EDOTA_SPT_Basic: EDOTAStatPopupTypes
k_EDOTA_SPT_Poll: EDOTAStatPopupTypes
k_EDOTA_SPT_Grid: EDOTAStatPopupTypes
k_EDOTA_SPT_DualImage: EDOTAStatPopupTypes
k_EDOTA_SPT_Movie: EDOTAStatPopupTypes
DOTA_UNIT_ORDER_NONE: dotaunitorder_t
DOTA_UNIT_ORDER_MOVE_TO_POSITION: dotaunitorder_t
DOTA_UNIT_ORDER_MOVE_TO_TARGET: dotaunitorder_t
DOTA_UNIT_ORDER_ATTACK_MOVE: dotaunitorder_t
DOTA_UNIT_ORDER_ATTACK_TARGET: dotaunitorder_t
DOTA_UNIT_ORDER_CAST_POSITION: dotaunitorder_t
DOTA_UNIT_ORDER_CAST_TARGET: dotaunitorder_t
DOTA_UNIT_ORDER_CAST_TARGET_TREE: dotaunitorder_t
DOTA_UNIT_ORDER_CAST_NO_TARGET: dotaunitorder_t
DOTA_UNIT_ORDER_CAST_TOGGLE: dotaunitorder_t
DOTA_UNIT_ORDER_HOLD_POSITION: dotaunitorder_t
DOTA_UNIT_ORDER_TRAIN_ABILITY: dotaunitorder_t
DOTA_UNIT_ORDER_DROP_ITEM: dotaunitorder_t
DOTA_UNIT_ORDER_GIVE_ITEM: dotaunitorder_t
DOTA_UNIT_ORDER_PICKUP_ITEM: dotaunitorder_t
DOTA_UNIT_ORDER_PICKUP_RUNE: dotaunitorder_t
DOTA_UNIT_ORDER_PURCHASE_ITEM: dotaunitorder_t
DOTA_UNIT_ORDER_SELL_ITEM: dotaunitorder_t
DOTA_UNIT_ORDER_DISASSEMBLE_ITEM: dotaunitorder_t
DOTA_UNIT_ORDER_MOVE_ITEM: dotaunitorder_t
DOTA_UNIT_ORDER_CAST_TOGGLE_AUTO: dotaunitorder_t
DOTA_UNIT_ORDER_STOP: dotaunitorder_t
DOTA_UNIT_ORDER_TAUNT: dotaunitorder_t
DOTA_UNIT_ORDER_BUYBACK: dotaunitorder_t
DOTA_UNIT_ORDER_GLYPH: dotaunitorder_t
DOTA_UNIT_ORDER_EJECT_ITEM_FROM_STASH: dotaunitorder_t
DOTA_UNIT_ORDER_CAST_RUNE: dotaunitorder_t
DOTA_UNIT_ORDER_PING_ABILITY: dotaunitorder_t
DOTA_UNIT_ORDER_MOVE_TO_DIRECTION: dotaunitorder_t
DOTA_UNIT_ORDER_PATROL: dotaunitorder_t
DOTA_UNIT_ORDER_VECTOR_TARGET_POSITION: dotaunitorder_t
DOTA_UNIT_ORDER_RADAR: dotaunitorder_t
DOTA_UNIT_ORDER_SET_ITEM_COMBINE_LOCK: dotaunitorder_t
DOTA_UNIT_ORDER_CONTINUE: dotaunitorder_t
DOTA_UNIT_ORDER_VECTOR_TARGET_CANCELED: dotaunitorder_t
DOTA_UNIT_ORDER_CAST_RIVER_PAINT: dotaunitorder_t
DOTA_UNIT_ORDER_PREGAME_ADJUST_ITEM_ASSIGNMENT: dotaunitorder_t
DOTA_UNIT_ORDER_DROP_ITEM_AT_FOUNTAIN: dotaunitorder_t
DOTA_UNIT_ORDER_TAKE_ITEM_FROM_NEUTRAL_ITEM_STASH: dotaunitorder_t
DOTA_UNIT_ORDER_MOVE_RELATIVE: dotaunitorder_t
DOTA_UNIT_ORDER_CAST_TOGGLE_ALT: dotaunitorder_t
DOTA_UNIT_ORDER_CONSUME_ITEM: dotaunitorder_t
DOTA_UNIT_ORDER_SET_ITEM_MARK_FOR_SELL: dotaunitorder_t
VS_PLAYER_BEHAVIOR_PLAY_ACTIVITY: EDOTAVersusScenePlayerBehavior
VS_PLAYER_BEHAVIOR_CHAT_WHEEL: EDOTAVersusScenePlayerBehavior
VS_PLAYER_BEHAVIOR_PLAYBACK_RATE: EDOTAVersusScenePlayerBehavior

class CDOTAMsg_PingWaypointPath(_message.Message):
    __slots__ = ("x", "y", "grid_nav_directions")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    GRID_NAV_DIRECTIONS_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    grid_nav_directions: bytes
    def __init__(
        self, x: int | None = ..., y: int | None = ..., grid_nav_directions: bytes | None = ...
    ) -> None: ...

class CDOTAMsg_LocationPing(_message.Message):
    __slots__ = ("x", "y", "target", "direct_ping", "type", "ping_source", "waypoint_path")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    DIRECT_PING_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PING_SOURCE_FIELD_NUMBER: _ClassVar[int]
    WAYPOINT_PATH_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    target: int
    direct_ping: bool
    type: int
    ping_source: EPingSource
    waypoint_path: CDOTAMsg_PingWaypointPath
    def __init__(
        self,
        x: int | None = ...,
        y: int | None = ...,
        target: int | None = ...,
        direct_ping: bool = ...,
        type: int | None = ...,
        ping_source: EPingSource | str | None = ...,
        waypoint_path: CDOTAMsg_PingWaypointPath | _Mapping | None = ...,
    ) -> None: ...

class CDOTAMsg_ItemAlert(_message.Message):
    __slots__ = ("x", "y", "item_ability_id")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    ITEM_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    item_ability_id: int
    def __init__(
        self, x: int | None = ..., y: int | None = ..., item_ability_id: int | None = ...
    ) -> None: ...

class CDOTAMsg_MapLine(_message.Message):
    __slots__ = ("x", "y", "initial")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    INITIAL_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    initial: bool
    def __init__(self, x: int | None = ..., y: int | None = ..., initial: bool = ...) -> None: ...

class CDOTAMsg_WorldLine(_message.Message):
    __slots__ = ("x", "y", "z", "initial", "end")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    INITIAL_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    z: int
    initial: bool
    end: bool
    def __init__(
        self,
        x: int | None = ...,
        y: int | None = ...,
        z: int | None = ...,
        initial: bool = ...,
        end: bool = ...,
    ) -> None: ...

class CDOTAMsg_SendStatPopup(_message.Message):
    __slots__ = (
        "style",
        "stat_strings",
        "stat_images",
        "stat_image_types",
        "duration",
        "use_html",
        "movie_name",
    )
    STYLE_FIELD_NUMBER: _ClassVar[int]
    STAT_STRINGS_FIELD_NUMBER: _ClassVar[int]
    STAT_IMAGES_FIELD_NUMBER: _ClassVar[int]
    STAT_IMAGE_TYPES_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    USE_HTML_FIELD_NUMBER: _ClassVar[int]
    MOVIE_NAME_FIELD_NUMBER: _ClassVar[int]
    style: EDOTAStatPopupTypes
    stat_strings: _containers.RepeatedScalarFieldContainer[str]
    stat_images: _containers.RepeatedScalarFieldContainer[int]
    stat_image_types: _containers.RepeatedScalarFieldContainer[int]
    duration: float
    use_html: bool
    movie_name: str
    def __init__(
        self,
        style: EDOTAStatPopupTypes | str | None = ...,
        stat_strings: _Iterable[str] | None = ...,
        stat_images: _Iterable[int] | None = ...,
        stat_image_types: _Iterable[int] | None = ...,
        duration: float | None = ...,
        use_html: bool = ...,
        movie_name: str | None = ...,
    ) -> None: ...

class CDOTAMsg_DismissAllStatPopups(_message.Message):
    __slots__ = ("time_delay",)
    TIME_DELAY_FIELD_NUMBER: _ClassVar[int]
    time_delay: float
    def __init__(self, time_delay: float | None = ...) -> None: ...

class CDOTAMsg_CoachHUDPing(_message.Message):
    __slots__ = ("x", "y", "tgtpath")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    TGTPATH_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    tgtpath: str
    def __init__(
        self, x: int | None = ..., y: int | None = ..., tgtpath: str | None = ...
    ) -> None: ...

class CDOTAMsg_UnitOrder(_message.Message):
    __slots__ = (
        "order_type",
        "units",
        "target_index",
        "ability_index",
        "position",
        "sequence_number",
        "flags",
    )
    ORDER_TYPE_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    TARGET_INDEX_FIELD_NUMBER: _ClassVar[int]
    ABILITY_INDEX_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    order_type: dotaunitorder_t
    units: _containers.RepeatedScalarFieldContainer[int]
    target_index: int
    ability_index: int
    position: _networkbasetypes_pb2.CMsgVector
    sequence_number: int
    flags: int
    def __init__(
        self,
        order_type: dotaunitorder_t | str | None = ...,
        units: _Iterable[int] | None = ...,
        target_index: int | None = ...,
        ability_index: int | None = ...,
        position: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
        sequence_number: int | None = ...,
        flags: int | None = ...,
    ) -> None: ...

class VersusScene_PlayActivity(_message.Message):
    __slots__ = ("activities", "playback_rate")
    class ActivityInfo(_message.Message):
        __slots__ = ("activity", "disable_auto_kill", "force_looping")
        ACTIVITY_FIELD_NUMBER: _ClassVar[int]
        DISABLE_AUTO_KILL_FIELD_NUMBER: _ClassVar[int]
        FORCE_LOOPING_FIELD_NUMBER: _ClassVar[int]
        activity: str
        disable_auto_kill: bool
        force_looping: bool
        def __init__(
            self,
            activity: str | None = ...,
            disable_auto_kill: bool = ...,
            force_looping: bool = ...,
        ) -> None: ...

    ACTIVITIES_FIELD_NUMBER: _ClassVar[int]
    PLAYBACK_RATE_FIELD_NUMBER: _ClassVar[int]
    activities: _containers.RepeatedCompositeFieldContainer[VersusScene_PlayActivity.ActivityInfo]
    playback_rate: float
    def __init__(
        self,
        activities: _Iterable[VersusScene_PlayActivity.ActivityInfo | _Mapping] | None = ...,
        playback_rate: float | None = ...,
    ) -> None: ...

class VersusScene_ChatWheel(_message.Message):
    __slots__ = ("chat_message_id", "emoticon_id")
    CHAT_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    EMOTICON_ID_FIELD_NUMBER: _ClassVar[int]
    chat_message_id: int
    emoticon_id: int
    def __init__(
        self, chat_message_id: int | None = ..., emoticon_id: int | None = ...
    ) -> None: ...

class VersusScene_PlaybackRate(_message.Message):
    __slots__ = ("rate",)
    RATE_FIELD_NUMBER: _ClassVar[int]
    rate: float
    def __init__(self, rate: float | None = ...) -> None: ...
