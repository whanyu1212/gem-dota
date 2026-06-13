from . import steammessages_pb2 as _steammessages_pb2
from . import dota_shared_enums_pb2 as _dota_shared_enums_pb2
from . import dota_gcmessages_common_pb2 as _dota_gcmessages_common_pb2
from . import dota_gcmessages_webapi_pb2 as _dota_gcmessages_webapi_pb2
from . import gcsdk_gcmessages_pb2 as _gcsdk_gcmessages_pb2
from . import base_gcmessages_pb2 as _base_gcmessages_pb2
from . import econ_gcmessages_pb2 as _econ_gcmessages_pb2
from . import dota_gcmessages_client_pb2 as _dota_gcmessages_client_pb2
from . import valveextensions_pb2 as _valveextensions_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EShowcaseHeroPlusFlag(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eShowcaseHeroPlusFlag_None: _ClassVar[EShowcaseHeroPlusFlag]
    k_eShowcaseHeroPlusFlag_BadgePosTop: _ClassVar[EShowcaseHeroPlusFlag]
    k_eShowcaseHeroPlusFlag_BadgePosBottom: _ClassVar[EShowcaseHeroPlusFlag]
    k_eShowcaseHeroPlusFlag_BadgePosLeft: _ClassVar[EShowcaseHeroPlusFlag]
    k_eShowcaseHeroPlusFlag_BadgePosRight: _ClassVar[EShowcaseHeroPlusFlag]
    k_eShowcaseHeroPlusFlag_ShowRelics: _ClassVar[EShowcaseHeroPlusFlag]

class EShowcaseType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eShowcaseType_Invalid: _ClassVar[EShowcaseType]
    k_eShowcaseType_Profile: _ClassVar[EShowcaseType]
    k_eShowcaseType_MiniProfile: _ClassVar[EShowcaseType]
    k_eShowcaseType_DefaultProfile: _ClassVar[EShowcaseType]
    k_eShowcaseType_DefaultMiniProfile: _ClassVar[EShowcaseType]

class EShowcaseItemState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eShowcaseItemState_Ok: _ClassVar[EShowcaseItemState]
    k_eShowcaseItemState_MinorModifications: _ClassVar[EShowcaseItemState]
    k_eShowcaseItemState_ValidityUnknown: _ClassVar[EShowcaseItemState]
    k_eShowcaseItemState_PartiallyInvalid: _ClassVar[EShowcaseItemState]
    k_eShowcaseItemState_Invalid: _ClassVar[EShowcaseItemState]
    k_eShowcaseItemState_Failure: _ClassVar[EShowcaseItemState]

class EShowcaseAuditAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eShowcaseAuditAction_Invalid: _ClassVar[EShowcaseAuditAction]
    k_eShowcaseAuditAction_ShowcaseChanged: _ClassVar[EShowcaseAuditAction]
    k_eShowcaseAuditAction_AdminShowcaseReset: _ClassVar[EShowcaseAuditAction]
    k_eShowcaseAuditAction_AdminShowcaseAccountLocked: _ClassVar[EShowcaseAuditAction]
    k_eShowcaseAuditAction_AdminShowcaseExonerated: _ClassVar[EShowcaseAuditAction]
    k_eShowcaseAuditAction_AdminShowcaseConvicted: _ClassVar[EShowcaseAuditAction]
    k_eShowcaseAuditAction_AdminModerationApproved: _ClassVar[EShowcaseAuditAction]
    k_eShowcaseAuditAction_AdminModerationRejected: _ClassVar[EShowcaseAuditAction]

class EShowcaseItemFlag(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eShowcaseItemFlag_None: _ClassVar[EShowcaseItemFlag]
    k_eShowcaseItemFlag_FlipHorizontally: _ClassVar[EShowcaseItemFlag]

class EShowcaseItemFlag_Hero(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eShowcaseItemFlag_Hero_None: _ClassVar[EShowcaseItemFlag_Hero]
    k_eShowcaseItemFlag_Hero_ShowPedestal: _ClassVar[EShowcaseItemFlag_Hero]
    k_eShowcaseItemFlag_Hero_UseCurrentLoadout: _ClassVar[EShowcaseItemFlag_Hero]
    k_eShowcaseItemFlag_Hero_ShowHeroCard: _ClassVar[EShowcaseItemFlag_Hero]
    k_eShowcaseItemFlag_Hero_HeroCardHideName: _ClassVar[EShowcaseItemFlag_Hero]
    k_eShowcaseItemFlag_Hero_HeroCardUseMovie: _ClassVar[EShowcaseItemFlag_Hero]
k_eShowcaseHeroPlusFlag_None: EShowcaseHeroPlusFlag
k_eShowcaseHeroPlusFlag_BadgePosTop: EShowcaseHeroPlusFlag
k_eShowcaseHeroPlusFlag_BadgePosBottom: EShowcaseHeroPlusFlag
k_eShowcaseHeroPlusFlag_BadgePosLeft: EShowcaseHeroPlusFlag
k_eShowcaseHeroPlusFlag_BadgePosRight: EShowcaseHeroPlusFlag
k_eShowcaseHeroPlusFlag_ShowRelics: EShowcaseHeroPlusFlag
k_eShowcaseType_Invalid: EShowcaseType
k_eShowcaseType_Profile: EShowcaseType
k_eShowcaseType_MiniProfile: EShowcaseType
k_eShowcaseType_DefaultProfile: EShowcaseType
k_eShowcaseType_DefaultMiniProfile: EShowcaseType
k_eShowcaseItemState_Ok: EShowcaseItemState
k_eShowcaseItemState_MinorModifications: EShowcaseItemState
k_eShowcaseItemState_ValidityUnknown: EShowcaseItemState
k_eShowcaseItemState_PartiallyInvalid: EShowcaseItemState
k_eShowcaseItemState_Invalid: EShowcaseItemState
k_eShowcaseItemState_Failure: EShowcaseItemState
k_eShowcaseAuditAction_Invalid: EShowcaseAuditAction
k_eShowcaseAuditAction_ShowcaseChanged: EShowcaseAuditAction
k_eShowcaseAuditAction_AdminShowcaseReset: EShowcaseAuditAction
k_eShowcaseAuditAction_AdminShowcaseAccountLocked: EShowcaseAuditAction
k_eShowcaseAuditAction_AdminShowcaseExonerated: EShowcaseAuditAction
k_eShowcaseAuditAction_AdminShowcaseConvicted: EShowcaseAuditAction
k_eShowcaseAuditAction_AdminModerationApproved: EShowcaseAuditAction
k_eShowcaseAuditAction_AdminModerationRejected: EShowcaseAuditAction
k_eShowcaseItemFlag_None: EShowcaseItemFlag
k_eShowcaseItemFlag_FlipHorizontally: EShowcaseItemFlag
k_eShowcaseItemFlag_Hero_None: EShowcaseItemFlag_Hero
k_eShowcaseItemFlag_Hero_ShowPedestal: EShowcaseItemFlag_Hero
k_eShowcaseItemFlag_Hero_UseCurrentLoadout: EShowcaseItemFlag_Hero
k_eShowcaseItemFlag_Hero_ShowHeroCard: EShowcaseItemFlag_Hero
k_eShowcaseItemFlag_Hero_HeroCardHideName: EShowcaseItemFlag_Hero
k_eShowcaseItemFlag_Hero_HeroCardUseMovie: EShowcaseItemFlag_Hero

class CMsgShowcaseEconItemReference(_message.Message):
    __slots__ = ("id", "original_id", "definition_index", "equipment_slot_index")
    ID_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_ID_FIELD_NUMBER: _ClassVar[int]
    DEFINITION_INDEX_FIELD_NUMBER: _ClassVar[int]
    EQUIPMENT_SLOT_INDEX_FIELD_NUMBER: _ClassVar[int]
    id: int
    original_id: int
    definition_index: int
    equipment_slot_index: int
    def __init__(self, id: _Optional[int] = ..., original_id: _Optional[int] = ..., definition_index: _Optional[int] = ..., equipment_slot_index: _Optional[int] = ...) -> None: ...

class CMsgHeroPlusInfo(_message.Message):
    __slots__ = ("flags",)
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    flags: int
    def __init__(self, flags: _Optional[int] = ...) -> None: ...

class CMsgShowcaseItem_Trophy(_message.Message):
    __slots__ = ("data", "trophy_id")
    class Data(_message.Message):
        __slots__ = ("trophy_score",)
        TROPHY_SCORE_FIELD_NUMBER: _ClassVar[int]
        trophy_score: int
        def __init__(self, trophy_score: _Optional[int] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    TROPHY_ID_FIELD_NUMBER: _ClassVar[int]
    data: CMsgShowcaseItem_Trophy.Data
    trophy_id: int
    def __init__(self, data: _Optional[_Union[CMsgShowcaseItem_Trophy.Data, _Mapping]] = ..., trophy_id: _Optional[int] = ...) -> None: ...

class CMsgShowcaseItem_EconItem(_message.Message):
    __slots__ = ("data", "ref")
    class Data(_message.Message):
        __slots__ = ("econ_item",)
        ECON_ITEM_FIELD_NUMBER: _ClassVar[int]
        econ_item: _base_gcmessages_pb2.CSOEconItem
        def __init__(self, econ_item: _Optional[_Union[_base_gcmessages_pb2.CSOEconItem, _Mapping]] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    REF_FIELD_NUMBER: _ClassVar[int]
    data: CMsgShowcaseItem_EconItem.Data
    ref: CMsgShowcaseEconItemReference
    def __init__(self, data: _Optional[_Union[CMsgShowcaseItem_EconItem.Data, _Mapping]] = ..., ref: _Optional[_Union[CMsgShowcaseEconItemReference, _Mapping]] = ...) -> None: ...

class CMsgShowcaseItem_Hero(_message.Message):
    __slots__ = ("data", "hero_id", "econ_item_refs", "rotation", "flags", "plus_info", "animation_name", "animation_playback_speed", "animation_offset", "zoom", "slot_index", "model_index")
    class Data(_message.Message):
        __slots__ = ("econ_items", "actual_hero_id", "plus_hero_xp")
        ECON_ITEMS_FIELD_NUMBER: _ClassVar[int]
        ACTUAL_HERO_ID_FIELD_NUMBER: _ClassVar[int]
        PLUS_HERO_XP_FIELD_NUMBER: _ClassVar[int]
        econ_items: _containers.RepeatedCompositeFieldContainer[_base_gcmessages_pb2.CSOEconItem]
        actual_hero_id: int
        plus_hero_xp: int
        def __init__(self, econ_items: _Optional[_Iterable[_Union[_base_gcmessages_pb2.CSOEconItem, _Mapping]]] = ..., actual_hero_id: _Optional[int] = ..., plus_hero_xp: _Optional[int] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    ECON_ITEM_REFS_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    PLUS_INFO_FIELD_NUMBER: _ClassVar[int]
    ANIMATION_NAME_FIELD_NUMBER: _ClassVar[int]
    ANIMATION_PLAYBACK_SPEED_FIELD_NUMBER: _ClassVar[int]
    ANIMATION_OFFSET_FIELD_NUMBER: _ClassVar[int]
    ZOOM_FIELD_NUMBER: _ClassVar[int]
    SLOT_INDEX_FIELD_NUMBER: _ClassVar[int]
    MODEL_INDEX_FIELD_NUMBER: _ClassVar[int]
    data: CMsgShowcaseItem_Hero.Data
    hero_id: int
    econ_item_refs: _containers.RepeatedCompositeFieldContainer[CMsgShowcaseEconItemReference]
    rotation: int
    flags: int
    plus_info: CMsgHeroPlusInfo
    animation_name: str
    animation_playback_speed: int
    animation_offset: int
    zoom: int
    slot_index: int
    model_index: int
    def __init__(self, data: _Optional[_Union[CMsgShowcaseItem_Hero.Data, _Mapping]] = ..., hero_id: _Optional[int] = ..., econ_item_refs: _Optional[_Iterable[_Union[CMsgShowcaseEconItemReference, _Mapping]]] = ..., rotation: _Optional[int] = ..., flags: _Optional[int] = ..., plus_info: _Optional[_Union[CMsgHeroPlusInfo, _Mapping]] = ..., animation_name: _Optional[str] = ..., animation_playback_speed: _Optional[int] = ..., animation_offset: _Optional[int] = ..., zoom: _Optional[int] = ..., slot_index: _Optional[int] = ..., model_index: _Optional[int] = ...) -> None: ...

class CMsgShowcaseItem_HeroIcon(_message.Message):
    __slots__ = ("data", "hero_id", "econ_item_ref")
    class Data(_message.Message):
        __slots__ = ("econ_item",)
        ECON_ITEM_FIELD_NUMBER: _ClassVar[int]
        econ_item: _base_gcmessages_pb2.CSOEconItem
        def __init__(self, econ_item: _Optional[_Union[_base_gcmessages_pb2.CSOEconItem, _Mapping]] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    ECON_ITEM_REF_FIELD_NUMBER: _ClassVar[int]
    data: CMsgShowcaseItem_HeroIcon.Data
    hero_id: int
    econ_item_ref: CMsgShowcaseEconItemReference
    def __init__(self, data: _Optional[_Union[CMsgShowcaseItem_HeroIcon.Data, _Mapping]] = ..., hero_id: _Optional[int] = ..., econ_item_ref: _Optional[_Union[CMsgShowcaseEconItemReference, _Mapping]] = ...) -> None: ...

class CMsgShowcaseItem_PlayerMatch(_message.Message):
    __slots__ = ("data", "match_id", "player_slot")
    class EPlayerOutcome(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInvalid: _ClassVar[CMsgShowcaseItem_PlayerMatch.EPlayerOutcome]
        k_eWin: _ClassVar[CMsgShowcaseItem_PlayerMatch.EPlayerOutcome]
        k_eLoss: _ClassVar[CMsgShowcaseItem_PlayerMatch.EPlayerOutcome]
        k_eNotScored: _ClassVar[CMsgShowcaseItem_PlayerMatch.EPlayerOutcome]
    k_eInvalid: CMsgShowcaseItem_PlayerMatch.EPlayerOutcome
    k_eWin: CMsgShowcaseItem_PlayerMatch.EPlayerOutcome
    k_eLoss: CMsgShowcaseItem_PlayerMatch.EPlayerOutcome
    k_eNotScored: CMsgShowcaseItem_PlayerMatch.EPlayerOutcome
    class Data(_message.Message):
        __slots__ = ("hero_id", "timestamp", "duration", "game_mode", "outcome", "kills", "deaths", "assists")
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        DURATION_FIELD_NUMBER: _ClassVar[int]
        GAME_MODE_FIELD_NUMBER: _ClassVar[int]
        OUTCOME_FIELD_NUMBER: _ClassVar[int]
        KILLS_FIELD_NUMBER: _ClassVar[int]
        DEATHS_FIELD_NUMBER: _ClassVar[int]
        ASSISTS_FIELD_NUMBER: _ClassVar[int]
        hero_id: int
        timestamp: int
        duration: int
        game_mode: _dota_shared_enums_pb2.DOTA_GameMode
        outcome: CMsgShowcaseItem_PlayerMatch.EPlayerOutcome
        kills: int
        deaths: int
        assists: int
        def __init__(self, hero_id: _Optional[int] = ..., timestamp: _Optional[int] = ..., duration: _Optional[int] = ..., game_mode: _Optional[_Union[_dota_shared_enums_pb2.DOTA_GameMode, str]] = ..., outcome: _Optional[_Union[CMsgShowcaseItem_PlayerMatch.EPlayerOutcome, str]] = ..., kills: _Optional[int] = ..., deaths: _Optional[int] = ..., assists: _Optional[int] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
    data: CMsgShowcaseItem_PlayerMatch.Data
    match_id: int
    player_slot: int
    def __init__(self, data: _Optional[_Union[CMsgShowcaseItem_PlayerMatch.Data, _Mapping]] = ..., match_id: _Optional[int] = ..., player_slot: _Optional[int] = ...) -> None: ...

class CMsgShowcaseItem_ChatWheel(_message.Message):
    __slots__ = ("data", "chat_wheel_message_id")
    class Data(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    CHAT_WHEEL_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    data: CMsgShowcaseItem_ChatWheel.Data
    chat_wheel_message_id: int
    def __init__(self, data: _Optional[_Union[CMsgShowcaseItem_ChatWheel.Data, _Mapping]] = ..., chat_wheel_message_id: _Optional[int] = ...) -> None: ...

class CMsgShowcaseItem_Emoticon(_message.Message):
    __slots__ = ("data", "emoticon_id")
    class Data(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    EMOTICON_ID_FIELD_NUMBER: _ClassVar[int]
    data: CMsgShowcaseItem_Emoticon.Data
    emoticon_id: int
    def __init__(self, data: _Optional[_Union[CMsgShowcaseItem_Emoticon.Data, _Mapping]] = ..., emoticon_id: _Optional[int] = ...) -> None: ...

class CMsgShowcaseItem_SpiderGraph(_message.Message):
    __slots__ = ("data",)
    class Data(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: CMsgShowcaseItem_SpiderGraph.Data
    def __init__(self, data: _Optional[_Union[CMsgShowcaseItem_SpiderGraph.Data, _Mapping]] = ...) -> None: ...

class CMsgShowcaseItem_UserFeed(_message.Message):
    __slots__ = ("data",)
    class Data(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: CMsgShowcaseItem_UserFeed.Data
    def __init__(self, data: _Optional[_Union[CMsgShowcaseItem_UserFeed.Data, _Mapping]] = ...) -> None: ...

class CMsgShowcaseItem_Stat(_message.Message):
    __slots__ = ("data", "stat_id")
    class Data(_message.Message):
        __slots__ = ("stat_score",)
        STAT_SCORE_FIELD_NUMBER: _ClassVar[int]
        stat_score: int
        def __init__(self, stat_score: _Optional[int] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    STAT_ID_FIELD_NUMBER: _ClassVar[int]
    data: CMsgShowcaseItem_Stat.Data
    stat_id: _dota_gcmessages_common_pb2.CMsgDOTAProfileCard.EStatID
    def __init__(self, data: _Optional[_Union[CMsgShowcaseItem_Stat.Data, _Mapping]] = ..., stat_id: _Optional[_Union[_dota_gcmessages_common_pb2.CMsgDOTAProfileCard.EStatID, str]] = ...) -> None: ...

class CMsgShowcaseBackground(_message.Message):
    __slots__ = ("data", "loading_screen_ref", "dim", "blur", "background_id")
    class Data(_message.Message):
        __slots__ = ("loading_screen",)
        LOADING_SCREEN_FIELD_NUMBER: _ClassVar[int]
        loading_screen: _base_gcmessages_pb2.CSOEconItem
        def __init__(self, loading_screen: _Optional[_Union[_base_gcmessages_pb2.CSOEconItem, _Mapping]] = ...) -> None: ...
    DATA_FIELD_NUMBER: _ClassVar[int]
    LOADING_SCREEN_REF_FIELD_NUMBER: _ClassVar[int]
    DIM_FIELD_NUMBER: _ClassVar[int]
    BLUR_FIELD_NUMBER: _ClassVar[int]
    BACKGROUND_ID_FIELD_NUMBER: _ClassVar[int]
    data: CMsgShowcaseBackground.Data
    loading_screen_ref: CMsgShowcaseEconItemReference
    dim: int
    blur: int
    background_id: int
    def __init__(self, data: _Optional[_Union[CMsgShowcaseBackground.Data, _Mapping]] = ..., loading_screen_ref: _Optional[_Union[CMsgShowcaseEconItemReference, _Mapping]] = ..., dim: _Optional[int] = ..., blur: _Optional[int] = ..., background_id: _Optional[int] = ...) -> None: ...

class CMsgShowcaseItemData(_message.Message):
    __slots__ = ("trophy", "econ_item_icon", "sticker", "hero_model", "player_match", "chat_wheel", "spray", "emoticon", "courier", "ward", "hero_icon", "spider_graph", "user_feed", "stat", "roshan", "creep", "tower", "effigy", "decoration", "background")
    TROPHY_FIELD_NUMBER: _ClassVar[int]
    ECON_ITEM_ICON_FIELD_NUMBER: _ClassVar[int]
    STICKER_FIELD_NUMBER: _ClassVar[int]
    HERO_MODEL_FIELD_NUMBER: _ClassVar[int]
    PLAYER_MATCH_FIELD_NUMBER: _ClassVar[int]
    CHAT_WHEEL_FIELD_NUMBER: _ClassVar[int]
    SPRAY_FIELD_NUMBER: _ClassVar[int]
    EMOTICON_FIELD_NUMBER: _ClassVar[int]
    COURIER_FIELD_NUMBER: _ClassVar[int]
    WARD_FIELD_NUMBER: _ClassVar[int]
    HERO_ICON_FIELD_NUMBER: _ClassVar[int]
    SPIDER_GRAPH_FIELD_NUMBER: _ClassVar[int]
    USER_FEED_FIELD_NUMBER: _ClassVar[int]
    STAT_FIELD_NUMBER: _ClassVar[int]
    ROSHAN_FIELD_NUMBER: _ClassVar[int]
    CREEP_FIELD_NUMBER: _ClassVar[int]
    TOWER_FIELD_NUMBER: _ClassVar[int]
    EFFIGY_FIELD_NUMBER: _ClassVar[int]
    DECORATION_FIELD_NUMBER: _ClassVar[int]
    BACKGROUND_FIELD_NUMBER: _ClassVar[int]
    trophy: CMsgShowcaseItem_Trophy
    econ_item_icon: CMsgShowcaseItem_EconItem
    sticker: CMsgShowcaseItem_EconItem
    hero_model: CMsgShowcaseItem_Hero
    player_match: CMsgShowcaseItem_PlayerMatch
    chat_wheel: CMsgShowcaseItem_ChatWheel
    spray: CMsgShowcaseItem_ChatWheel
    emoticon: CMsgShowcaseItem_Emoticon
    courier: CMsgShowcaseItem_EconItem
    ward: CMsgShowcaseItem_EconItem
    hero_icon: CMsgShowcaseItem_HeroIcon
    spider_graph: CMsgShowcaseItem_SpiderGraph
    user_feed: CMsgShowcaseItem_UserFeed
    stat: CMsgShowcaseItem_Stat
    roshan: CMsgShowcaseItem_EconItem
    creep: CMsgShowcaseItem_EconItem
    tower: CMsgShowcaseItem_EconItem
    effigy: CMsgShowcaseItem_EconItem
    decoration: CMsgShowcaseItem_EconItem
    background: CMsgShowcaseBackground
    def __init__(self, trophy: _Optional[_Union[CMsgShowcaseItem_Trophy, _Mapping]] = ..., econ_item_icon: _Optional[_Union[CMsgShowcaseItem_EconItem, _Mapping]] = ..., sticker: _Optional[_Union[CMsgShowcaseItem_EconItem, _Mapping]] = ..., hero_model: _Optional[_Union[CMsgShowcaseItem_Hero, _Mapping]] = ..., player_match: _Optional[_Union[CMsgShowcaseItem_PlayerMatch, _Mapping]] = ..., chat_wheel: _Optional[_Union[CMsgShowcaseItem_ChatWheel, _Mapping]] = ..., spray: _Optional[_Union[CMsgShowcaseItem_ChatWheel, _Mapping]] = ..., emoticon: _Optional[_Union[CMsgShowcaseItem_Emoticon, _Mapping]] = ..., courier: _Optional[_Union[CMsgShowcaseItem_EconItem, _Mapping]] = ..., ward: _Optional[_Union[CMsgShowcaseItem_EconItem, _Mapping]] = ..., hero_icon: _Optional[_Union[CMsgShowcaseItem_HeroIcon, _Mapping]] = ..., spider_graph: _Optional[_Union[CMsgShowcaseItem_SpiderGraph, _Mapping]] = ..., user_feed: _Optional[_Union[CMsgShowcaseItem_UserFeed, _Mapping]] = ..., stat: _Optional[_Union[CMsgShowcaseItem_Stat, _Mapping]] = ..., roshan: _Optional[_Union[CMsgShowcaseItem_EconItem, _Mapping]] = ..., creep: _Optional[_Union[CMsgShowcaseItem_EconItem, _Mapping]] = ..., tower: _Optional[_Union[CMsgShowcaseItem_EconItem, _Mapping]] = ..., effigy: _Optional[_Union[CMsgShowcaseItem_EconItem, _Mapping]] = ..., decoration: _Optional[_Union[CMsgShowcaseItem_EconItem, _Mapping]] = ..., background: _Optional[_Union[CMsgShowcaseBackground, _Mapping]] = ...) -> None: ...

class CMsgShowcaseItemPosition(_message.Message):
    __slots__ = ("position_x", "position_y", "scale", "width", "height", "rotation", "parent_id", "parent_attachment_point_id", "attachment_anchor_x", "attachment_anchor_y")
    POSITION_X_FIELD_NUMBER: _ClassVar[int]
    POSITION_Y_FIELD_NUMBER: _ClassVar[int]
    SCALE_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    PARENT_ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_ATTACHMENT_POINT_ID_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENT_ANCHOR_X_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENT_ANCHOR_Y_FIELD_NUMBER: _ClassVar[int]
    position_x: int
    position_y: int
    scale: int
    width: int
    height: int
    rotation: int
    parent_id: int
    parent_attachment_point_id: int
    attachment_anchor_x: int
    attachment_anchor_y: int
    def __init__(self, position_x: _Optional[int] = ..., position_y: _Optional[int] = ..., scale: _Optional[int] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., rotation: _Optional[int] = ..., parent_id: _Optional[int] = ..., parent_attachment_point_id: _Optional[int] = ..., attachment_anchor_x: _Optional[int] = ..., attachment_anchor_y: _Optional[int] = ...) -> None: ...

class CMsgShowcaseItem(_message.Message):
    __slots__ = ("showcase_item_id", "item_position", "item_data", "state", "flags")
    SHOWCASE_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_POSITION_FIELD_NUMBER: _ClassVar[int]
    ITEM_DATA_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    showcase_item_id: int
    item_position: CMsgShowcaseItemPosition
    item_data: CMsgShowcaseItemData
    state: EShowcaseItemState
    flags: int
    def __init__(self, showcase_item_id: _Optional[int] = ..., item_position: _Optional[_Union[CMsgShowcaseItemPosition, _Mapping]] = ..., item_data: _Optional[_Union[CMsgShowcaseItemData, _Mapping]] = ..., state: _Optional[_Union[EShowcaseItemState, str]] = ..., flags: _Optional[int] = ...) -> None: ...

class CMsgShowcase(_message.Message):
    __slots__ = ("showcase_items", "background", "moderation_state")
    class EModerationState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eModerationState_Ok: _ClassVar[CMsgShowcase.EModerationState]
        k_eModerationState_PendingApproval: _ClassVar[CMsgShowcase.EModerationState]
    k_eModerationState_Ok: CMsgShowcase.EModerationState
    k_eModerationState_PendingApproval: CMsgShowcase.EModerationState
    SHOWCASE_ITEMS_FIELD_NUMBER: _ClassVar[int]
    BACKGROUND_FIELD_NUMBER: _ClassVar[int]
    MODERATION_STATE_FIELD_NUMBER: _ClassVar[int]
    showcase_items: _containers.RepeatedCompositeFieldContainer[CMsgShowcaseItem]
    background: CMsgShowcaseItem
    moderation_state: CMsgShowcase.EModerationState
    def __init__(self, showcase_items: _Optional[_Iterable[_Union[CMsgShowcaseItem, _Mapping]]] = ..., background: _Optional[_Union[CMsgShowcaseItem, _Mapping]] = ..., moderation_state: _Optional[_Union[CMsgShowcase.EModerationState, str]] = ...) -> None: ...

class CMsgClientToGCShowcaseGetUserData(_message.Message):
    __slots__ = ("account_id", "showcase_type")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SHOWCASE_TYPE_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    showcase_type: EShowcaseType
    def __init__(self, account_id: _Optional[int] = ..., showcase_type: _Optional[_Union[EShowcaseType, str]] = ...) -> None: ...

class CMsgClientToGCShowcaseGetUserDataResponse(_message.Message):
    __slots__ = ("response", "showcase")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCShowcaseGetUserDataResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCShowcaseGetUserDataResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCShowcaseGetUserDataResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCShowcaseGetUserDataResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCShowcaseGetUserDataResponse.EResponse]
        k_eUnknownShowcase: _ClassVar[CMsgClientToGCShowcaseGetUserDataResponse.EResponse]
    k_eInternalError: CMsgClientToGCShowcaseGetUserDataResponse.EResponse
    k_eSuccess: CMsgClientToGCShowcaseGetUserDataResponse.EResponse
    k_eTooBusy: CMsgClientToGCShowcaseGetUserDataResponse.EResponse
    k_eDisabled: CMsgClientToGCShowcaseGetUserDataResponse.EResponse
    k_eTimeout: CMsgClientToGCShowcaseGetUserDataResponse.EResponse
    k_eUnknownShowcase: CMsgClientToGCShowcaseGetUserDataResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    SHOWCASE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCShowcaseGetUserDataResponse.EResponse
    showcase: CMsgShowcase
    def __init__(self, response: _Optional[_Union[CMsgClientToGCShowcaseGetUserDataResponse.EResponse, str]] = ..., showcase: _Optional[_Union[CMsgShowcase, _Mapping]] = ...) -> None: ...

class CMsgClientToGCShowcaseSetUserData(_message.Message):
    __slots__ = ("showcase_type", "showcase", "format_version")
    SHOWCASE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SHOWCASE_FIELD_NUMBER: _ClassVar[int]
    FORMAT_VERSION_FIELD_NUMBER: _ClassVar[int]
    showcase_type: EShowcaseType
    showcase: CMsgShowcase
    format_version: int
    def __init__(self, showcase_type: _Optional[_Union[EShowcaseType, str]] = ..., showcase: _Optional[_Union[CMsgShowcase, _Mapping]] = ..., format_version: _Optional[int] = ...) -> None: ...

class CMsgClientToGCShowcaseSetUserDataResponse(_message.Message):
    __slots__ = ("response", "validated_showcase", "locked_until_timestamp")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCShowcaseSetUserDataResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCShowcaseSetUserDataResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCShowcaseSetUserDataResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCShowcaseSetUserDataResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCShowcaseSetUserDataResponse.EResponse]
        k_eInvalid: _ClassVar[CMsgClientToGCShowcaseSetUserDataResponse.EResponse]
        k_eLockedFromEditing: _ClassVar[CMsgClientToGCShowcaseSetUserDataResponse.EResponse]
        k_eBudgetExceeded: _ClassVar[CMsgClientToGCShowcaseSetUserDataResponse.EResponse]
        k_eCommunicationScoreTooLow: _ClassVar[CMsgClientToGCShowcaseSetUserDataResponse.EResponse]
    k_eInternalError: CMsgClientToGCShowcaseSetUserDataResponse.EResponse
    k_eSuccess: CMsgClientToGCShowcaseSetUserDataResponse.EResponse
    k_eTooBusy: CMsgClientToGCShowcaseSetUserDataResponse.EResponse
    k_eDisabled: CMsgClientToGCShowcaseSetUserDataResponse.EResponse
    k_eTimeout: CMsgClientToGCShowcaseSetUserDataResponse.EResponse
    k_eInvalid: CMsgClientToGCShowcaseSetUserDataResponse.EResponse
    k_eLockedFromEditing: CMsgClientToGCShowcaseSetUserDataResponse.EResponse
    k_eBudgetExceeded: CMsgClientToGCShowcaseSetUserDataResponse.EResponse
    k_eCommunicationScoreTooLow: CMsgClientToGCShowcaseSetUserDataResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    VALIDATED_SHOWCASE_FIELD_NUMBER: _ClassVar[int]
    LOCKED_UNTIL_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCShowcaseSetUserDataResponse.EResponse
    validated_showcase: CMsgShowcase
    locked_until_timestamp: int
    def __init__(self, response: _Optional[_Union[CMsgClientToGCShowcaseSetUserDataResponse.EResponse, str]] = ..., validated_showcase: _Optional[_Union[CMsgShowcase, _Mapping]] = ..., locked_until_timestamp: _Optional[int] = ...) -> None: ...

class CMsgClientToGCShowcaseSubmitReport(_message.Message):
    __slots__ = ("target_account_id", "showcase_type", "report_comment")
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SHOWCASE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REPORT_COMMENT_FIELD_NUMBER: _ClassVar[int]
    target_account_id: int
    showcase_type: EShowcaseType
    report_comment: str
    def __init__(self, target_account_id: _Optional[int] = ..., showcase_type: _Optional[_Union[EShowcaseType, str]] = ..., report_comment: _Optional[str] = ...) -> None: ...

class CMsgClientToGCShowcaseSubmitReportResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCShowcaseSubmitReportResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCShowcaseSubmitReportResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCShowcaseSubmitReportResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCShowcaseSubmitReportResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCShowcaseSubmitReportResponse.EResponse]
        k_eAlreadyReported: _ClassVar[CMsgClientToGCShowcaseSubmitReportResponse.EResponse]
    k_eInternalError: CMsgClientToGCShowcaseSubmitReportResponse.EResponse
    k_eSuccess: CMsgClientToGCShowcaseSubmitReportResponse.EResponse
    k_eTooBusy: CMsgClientToGCShowcaseSubmitReportResponse.EResponse
    k_eDisabled: CMsgClientToGCShowcaseSubmitReportResponse.EResponse
    k_eTimeout: CMsgClientToGCShowcaseSubmitReportResponse.EResponse
    k_eAlreadyReported: CMsgClientToGCShowcaseSubmitReportResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCShowcaseSubmitReportResponse.EResponse
    def __init__(self, response: _Optional[_Union[CMsgClientToGCShowcaseSubmitReportResponse.EResponse, str]] = ...) -> None: ...

class CMsgShowcaseReportsRollupInfo(_message.Message):
    __slots__ = ("rollup_id", "start_timestamp", "end_timestamp")
    ROLLUP_ID_FIELD_NUMBER: _ClassVar[int]
    START_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    END_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    rollup_id: int
    start_timestamp: int
    end_timestamp: int
    def __init__(self, rollup_id: _Optional[int] = ..., start_timestamp: _Optional[int] = ..., end_timestamp: _Optional[int] = ...) -> None: ...

class CMsgShowcaseReportsRollupList(_message.Message):
    __slots__ = ("rollups",)
    ROLLUPS_FIELD_NUMBER: _ClassVar[int]
    rollups: _containers.RepeatedCompositeFieldContainer[CMsgShowcaseReportsRollupInfo]
    def __init__(self, rollups: _Optional[_Iterable[_Union[CMsgShowcaseReportsRollupInfo, _Mapping]]] = ...) -> None: ...

class CMsgShowcaseReportsRollupEntry(_message.Message):
    __slots__ = ("account_id", "showcase_type", "report_count")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SHOWCASE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REPORT_COUNT_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    showcase_type: EShowcaseType
    report_count: int
    def __init__(self, account_id: _Optional[int] = ..., showcase_type: _Optional[_Union[EShowcaseType, str]] = ..., report_count: _Optional[int] = ...) -> None: ...

class CMsgShowcaseReportsRollup(_message.Message):
    __slots__ = ("rollup_info", "rollup_entries")
    ROLLUP_INFO_FIELD_NUMBER: _ClassVar[int]
    ROLLUP_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    rollup_info: CMsgShowcaseReportsRollupInfo
    rollup_entries: _containers.RepeatedCompositeFieldContainer[CMsgShowcaseReportsRollupEntry]
    def __init__(self, rollup_info: _Optional[_Union[CMsgShowcaseReportsRollupInfo, _Mapping]] = ..., rollup_entries: _Optional[_Iterable[_Union[CMsgShowcaseReportsRollupEntry, _Mapping]]] = ...) -> None: ...

class CMsgClientToGCShowcaseAdminGetReportsRollupList(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCShowcaseAdminGetReportsRollupListResponse(_message.Message):
    __slots__ = ("response", "rollup_list")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCShowcaseAdminGetReportsRollupListResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCShowcaseAdminGetReportsRollupListResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCShowcaseAdminGetReportsRollupListResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCShowcaseAdminGetReportsRollupListResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCShowcaseAdminGetReportsRollupListResponse.EResponse]
        k_eNoPermission: _ClassVar[CMsgClientToGCShowcaseAdminGetReportsRollupListResponse.EResponse]
    k_eInternalError: CMsgClientToGCShowcaseAdminGetReportsRollupListResponse.EResponse
    k_eSuccess: CMsgClientToGCShowcaseAdminGetReportsRollupListResponse.EResponse
    k_eTooBusy: CMsgClientToGCShowcaseAdminGetReportsRollupListResponse.EResponse
    k_eDisabled: CMsgClientToGCShowcaseAdminGetReportsRollupListResponse.EResponse
    k_eTimeout: CMsgClientToGCShowcaseAdminGetReportsRollupListResponse.EResponse
    k_eNoPermission: CMsgClientToGCShowcaseAdminGetReportsRollupListResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    ROLLUP_LIST_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCShowcaseAdminGetReportsRollupListResponse.EResponse
    rollup_list: CMsgShowcaseReportsRollupList
    def __init__(self, response: _Optional[_Union[CMsgClientToGCShowcaseAdminGetReportsRollupListResponse.EResponse, str]] = ..., rollup_list: _Optional[_Union[CMsgShowcaseReportsRollupList, _Mapping]] = ...) -> None: ...

class CMsgClientToGCShowcaseAdminGetReportsRollup(_message.Message):
    __slots__ = ("rollup_id",)
    ROLLUP_ID_FIELD_NUMBER: _ClassVar[int]
    rollup_id: int
    def __init__(self, rollup_id: _Optional[int] = ...) -> None: ...

class CMsgClientToGCShowcaseAdminGetReportsRollupResponse(_message.Message):
    __slots__ = ("response", "rollup")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCShowcaseAdminGetReportsRollupResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCShowcaseAdminGetReportsRollupResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCShowcaseAdminGetReportsRollupResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCShowcaseAdminGetReportsRollupResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCShowcaseAdminGetReportsRollupResponse.EResponse]
        k_eNoPermission: _ClassVar[CMsgClientToGCShowcaseAdminGetReportsRollupResponse.EResponse]
        k_eNotFound: _ClassVar[CMsgClientToGCShowcaseAdminGetReportsRollupResponse.EResponse]
    k_eInternalError: CMsgClientToGCShowcaseAdminGetReportsRollupResponse.EResponse
    k_eSuccess: CMsgClientToGCShowcaseAdminGetReportsRollupResponse.EResponse
    k_eTooBusy: CMsgClientToGCShowcaseAdminGetReportsRollupResponse.EResponse
    k_eDisabled: CMsgClientToGCShowcaseAdminGetReportsRollupResponse.EResponse
    k_eTimeout: CMsgClientToGCShowcaseAdminGetReportsRollupResponse.EResponse
    k_eNoPermission: CMsgClientToGCShowcaseAdminGetReportsRollupResponse.EResponse
    k_eNotFound: CMsgClientToGCShowcaseAdminGetReportsRollupResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    ROLLUP_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCShowcaseAdminGetReportsRollupResponse.EResponse
    rollup: CMsgShowcaseReportsRollup
    def __init__(self, response: _Optional[_Union[CMsgClientToGCShowcaseAdminGetReportsRollupResponse.EResponse, str]] = ..., rollup: _Optional[_Union[CMsgShowcaseReportsRollup, _Mapping]] = ...) -> None: ...

class CMsgShowcaseAuditEntry(_message.Message):
    __slots__ = ("showcase_type", "audit_action", "audit_data", "timestamp")
    SHOWCASE_TYPE_FIELD_NUMBER: _ClassVar[int]
    AUDIT_ACTION_FIELD_NUMBER: _ClassVar[int]
    AUDIT_DATA_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    showcase_type: EShowcaseType
    audit_action: EShowcaseAuditAction
    audit_data: int
    timestamp: int
    def __init__(self, showcase_type: _Optional[_Union[EShowcaseType, str]] = ..., audit_action: _Optional[_Union[EShowcaseAuditAction, str]] = ..., audit_data: _Optional[int] = ..., timestamp: _Optional[int] = ...) -> None: ...

class CMsgShowcaseReport(_message.Message):
    __slots__ = ("reporter_account_id", "showcase_type", "report_timestamp", "report_comment")
    REPORTER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SHOWCASE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REPORT_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    REPORT_COMMENT_FIELD_NUMBER: _ClassVar[int]
    reporter_account_id: int
    showcase_type: EShowcaseType
    report_timestamp: int
    report_comment: str
    def __init__(self, reporter_account_id: _Optional[int] = ..., showcase_type: _Optional[_Union[EShowcaseType, str]] = ..., report_timestamp: _Optional[int] = ..., report_comment: _Optional[str] = ...) -> None: ...

class CMsgShowcaseAdminUserDetails(_message.Message):
    __slots__ = ("locked_until_timestamp", "audit_entries", "reports")
    LOCKED_UNTIL_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    AUDIT_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    REPORTS_FIELD_NUMBER: _ClassVar[int]
    locked_until_timestamp: int
    audit_entries: _containers.RepeatedCompositeFieldContainer[CMsgShowcaseAuditEntry]
    reports: _containers.RepeatedCompositeFieldContainer[CMsgShowcaseReport]
    def __init__(self, locked_until_timestamp: _Optional[int] = ..., audit_entries: _Optional[_Iterable[_Union[CMsgShowcaseAuditEntry, _Mapping]]] = ..., reports: _Optional[_Iterable[_Union[CMsgShowcaseReport, _Mapping]]] = ...) -> None: ...

class CMsgClientToGCShowcaseAdminGetUserDetails(_message.Message):
    __slots__ = ("account_id",)
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    def __init__(self, account_id: _Optional[int] = ...) -> None: ...

class CMsgClientToGCShowcaseAdminGetUserDetailsResponse(_message.Message):
    __slots__ = ("response", "user_details")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCShowcaseAdminGetUserDetailsResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCShowcaseAdminGetUserDetailsResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCShowcaseAdminGetUserDetailsResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCShowcaseAdminGetUserDetailsResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCShowcaseAdminGetUserDetailsResponse.EResponse]
        k_eNoPermission: _ClassVar[CMsgClientToGCShowcaseAdminGetUserDetailsResponse.EResponse]
    k_eInternalError: CMsgClientToGCShowcaseAdminGetUserDetailsResponse.EResponse
    k_eSuccess: CMsgClientToGCShowcaseAdminGetUserDetailsResponse.EResponse
    k_eTooBusy: CMsgClientToGCShowcaseAdminGetUserDetailsResponse.EResponse
    k_eDisabled: CMsgClientToGCShowcaseAdminGetUserDetailsResponse.EResponse
    k_eTimeout: CMsgClientToGCShowcaseAdminGetUserDetailsResponse.EResponse
    k_eNoPermission: CMsgClientToGCShowcaseAdminGetUserDetailsResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    USER_DETAILS_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCShowcaseAdminGetUserDetailsResponse.EResponse
    user_details: CMsgShowcaseAdminUserDetails
    def __init__(self, response: _Optional[_Union[CMsgClientToGCShowcaseAdminGetUserDetailsResponse.EResponse, str]] = ..., user_details: _Optional[_Union[CMsgShowcaseAdminUserDetails, _Mapping]] = ...) -> None: ...

class CMsgClientToGCShowcaseAdminReset(_message.Message):
    __slots__ = ("target_account_id", "showcase_type")
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SHOWCASE_TYPE_FIELD_NUMBER: _ClassVar[int]
    target_account_id: int
    showcase_type: EShowcaseType
    def __init__(self, target_account_id: _Optional[int] = ..., showcase_type: _Optional[_Union[EShowcaseType, str]] = ...) -> None: ...

class CMsgClientToGCShowcaseAdminResetResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCShowcaseAdminResetResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCShowcaseAdminResetResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCShowcaseAdminResetResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCShowcaseAdminResetResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCShowcaseAdminResetResponse.EResponse]
        k_eNoPermission: _ClassVar[CMsgClientToGCShowcaseAdminResetResponse.EResponse]
    k_eInternalError: CMsgClientToGCShowcaseAdminResetResponse.EResponse
    k_eSuccess: CMsgClientToGCShowcaseAdminResetResponse.EResponse
    k_eTooBusy: CMsgClientToGCShowcaseAdminResetResponse.EResponse
    k_eDisabled: CMsgClientToGCShowcaseAdminResetResponse.EResponse
    k_eTimeout: CMsgClientToGCShowcaseAdminResetResponse.EResponse
    k_eNoPermission: CMsgClientToGCShowcaseAdminResetResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCShowcaseAdminResetResponse.EResponse
    def __init__(self, response: _Optional[_Union[CMsgClientToGCShowcaseAdminResetResponse.EResponse, str]] = ...) -> None: ...

class CMsgClientToGCShowcaseAdminLockAccount(_message.Message):
    __slots__ = ("target_account_id", "locked_until_timestamp")
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    LOCKED_UNTIL_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    target_account_id: int
    locked_until_timestamp: int
    def __init__(self, target_account_id: _Optional[int] = ..., locked_until_timestamp: _Optional[int] = ...) -> None: ...

class CMsgClientToGCShowcaseAdminLockAccountResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCShowcaseAdminLockAccountResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCShowcaseAdminLockAccountResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCShowcaseAdminLockAccountResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCShowcaseAdminLockAccountResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCShowcaseAdminLockAccountResponse.EResponse]
        k_eNoPermission: _ClassVar[CMsgClientToGCShowcaseAdminLockAccountResponse.EResponse]
    k_eInternalError: CMsgClientToGCShowcaseAdminLockAccountResponse.EResponse
    k_eSuccess: CMsgClientToGCShowcaseAdminLockAccountResponse.EResponse
    k_eTooBusy: CMsgClientToGCShowcaseAdminLockAccountResponse.EResponse
    k_eDisabled: CMsgClientToGCShowcaseAdminLockAccountResponse.EResponse
    k_eTimeout: CMsgClientToGCShowcaseAdminLockAccountResponse.EResponse
    k_eNoPermission: CMsgClientToGCShowcaseAdminLockAccountResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCShowcaseAdminLockAccountResponse.EResponse
    def __init__(self, response: _Optional[_Union[CMsgClientToGCShowcaseAdminLockAccountResponse.EResponse, str]] = ...) -> None: ...

class CMsgClientToGCShowcaseAdminConvict(_message.Message):
    __slots__ = ("target_account_id", "showcase_type")
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SHOWCASE_TYPE_FIELD_NUMBER: _ClassVar[int]
    target_account_id: int
    showcase_type: EShowcaseType
    def __init__(self, target_account_id: _Optional[int] = ..., showcase_type: _Optional[_Union[EShowcaseType, str]] = ...) -> None: ...

class CMsgClientToGCShowcaseAdminConvictResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCShowcaseAdminConvictResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCShowcaseAdminConvictResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCShowcaseAdminConvictResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCShowcaseAdminConvictResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCShowcaseAdminConvictResponse.EResponse]
        k_eNoPermission: _ClassVar[CMsgClientToGCShowcaseAdminConvictResponse.EResponse]
        k_eAlreadyConvicted: _ClassVar[CMsgClientToGCShowcaseAdminConvictResponse.EResponse]
    k_eInternalError: CMsgClientToGCShowcaseAdminConvictResponse.EResponse
    k_eSuccess: CMsgClientToGCShowcaseAdminConvictResponse.EResponse
    k_eTooBusy: CMsgClientToGCShowcaseAdminConvictResponse.EResponse
    k_eDisabled: CMsgClientToGCShowcaseAdminConvictResponse.EResponse
    k_eTimeout: CMsgClientToGCShowcaseAdminConvictResponse.EResponse
    k_eNoPermission: CMsgClientToGCShowcaseAdminConvictResponse.EResponse
    k_eAlreadyConvicted: CMsgClientToGCShowcaseAdminConvictResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCShowcaseAdminConvictResponse.EResponse
    def __init__(self, response: _Optional[_Union[CMsgClientToGCShowcaseAdminConvictResponse.EResponse, str]] = ...) -> None: ...

class CMsgClientToGCShowcaseAdminExonerate(_message.Message):
    __slots__ = ("target_account_id", "showcase_type")
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SHOWCASE_TYPE_FIELD_NUMBER: _ClassVar[int]
    target_account_id: int
    showcase_type: EShowcaseType
    def __init__(self, target_account_id: _Optional[int] = ..., showcase_type: _Optional[_Union[EShowcaseType, str]] = ...) -> None: ...

class CMsgClientToGCShowcaseAdminExonerateResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCShowcaseAdminExonerateResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCShowcaseAdminExonerateResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCShowcaseAdminExonerateResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCShowcaseAdminExonerateResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCShowcaseAdminExonerateResponse.EResponse]
        k_eNoPermission: _ClassVar[CMsgClientToGCShowcaseAdminExonerateResponse.EResponse]
        k_eAlreadyExonerated: _ClassVar[CMsgClientToGCShowcaseAdminExonerateResponse.EResponse]
    k_eInternalError: CMsgClientToGCShowcaseAdminExonerateResponse.EResponse
    k_eSuccess: CMsgClientToGCShowcaseAdminExonerateResponse.EResponse
    k_eTooBusy: CMsgClientToGCShowcaseAdminExonerateResponse.EResponse
    k_eDisabled: CMsgClientToGCShowcaseAdminExonerateResponse.EResponse
    k_eTimeout: CMsgClientToGCShowcaseAdminExonerateResponse.EResponse
    k_eNoPermission: CMsgClientToGCShowcaseAdminExonerateResponse.EResponse
    k_eAlreadyExonerated: CMsgClientToGCShowcaseAdminExonerateResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCShowcaseAdminExonerateResponse.EResponse
    def __init__(self, response: _Optional[_Union[CMsgClientToGCShowcaseAdminExonerateResponse.EResponse, str]] = ...) -> None: ...

class CMsgShowcaseModerationInfo(_message.Message):
    __slots__ = ("account_id", "showcase_type", "showcase_timestamp")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SHOWCASE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SHOWCASE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    showcase_type: EShowcaseType
    showcase_timestamp: int
    def __init__(self, account_id: _Optional[int] = ..., showcase_type: _Optional[_Union[EShowcaseType, str]] = ..., showcase_timestamp: _Optional[int] = ...) -> None: ...

class CMsgClientToGCShowcaseModerationGetQueue(_message.Message):
    __slots__ = ("start_timestamp", "result_count")
    START_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    RESULT_COUNT_FIELD_NUMBER: _ClassVar[int]
    start_timestamp: int
    result_count: int
    def __init__(self, start_timestamp: _Optional[int] = ..., result_count: _Optional[int] = ...) -> None: ...

class CMsgClientToGCShowcaseModerationGetQueueResponse(_message.Message):
    __slots__ = ("response", "showcases")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCShowcaseModerationGetQueueResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCShowcaseModerationGetQueueResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCShowcaseModerationGetQueueResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCShowcaseModerationGetQueueResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCShowcaseModerationGetQueueResponse.EResponse]
        k_eNoPermission: _ClassVar[CMsgClientToGCShowcaseModerationGetQueueResponse.EResponse]
    k_eInternalError: CMsgClientToGCShowcaseModerationGetQueueResponse.EResponse
    k_eSuccess: CMsgClientToGCShowcaseModerationGetQueueResponse.EResponse
    k_eTooBusy: CMsgClientToGCShowcaseModerationGetQueueResponse.EResponse
    k_eDisabled: CMsgClientToGCShowcaseModerationGetQueueResponse.EResponse
    k_eTimeout: CMsgClientToGCShowcaseModerationGetQueueResponse.EResponse
    k_eNoPermission: CMsgClientToGCShowcaseModerationGetQueueResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    SHOWCASES_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCShowcaseModerationGetQueueResponse.EResponse
    showcases: _containers.RepeatedCompositeFieldContainer[CMsgShowcaseModerationInfo]
    def __init__(self, response: _Optional[_Union[CMsgClientToGCShowcaseModerationGetQueueResponse.EResponse, str]] = ..., showcases: _Optional[_Iterable[_Union[CMsgShowcaseModerationInfo, _Mapping]]] = ...) -> None: ...

class CMsgClientToGCShowcaseModerationApplyModeration(_message.Message):
    __slots__ = ("account_id", "showcase_type", "showcase_timestamp", "approve")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SHOWCASE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SHOWCASE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    APPROVE_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    showcase_type: EShowcaseType
    showcase_timestamp: int
    approve: bool
    def __init__(self, account_id: _Optional[int] = ..., showcase_type: _Optional[_Union[EShowcaseType, str]] = ..., showcase_timestamp: _Optional[int] = ..., approve: bool = ...) -> None: ...

class CMsgClientToGCShowcaseModerationApplyModerationResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCShowcaseModerationApplyModerationResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCShowcaseModerationApplyModerationResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCShowcaseModerationApplyModerationResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCShowcaseModerationApplyModerationResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCShowcaseModerationApplyModerationResponse.EResponse]
        k_eNoPermission: _ClassVar[CMsgClientToGCShowcaseModerationApplyModerationResponse.EResponse]
        k_eGone: _ClassVar[CMsgClientToGCShowcaseModerationApplyModerationResponse.EResponse]
    k_eInternalError: CMsgClientToGCShowcaseModerationApplyModerationResponse.EResponse
    k_eSuccess: CMsgClientToGCShowcaseModerationApplyModerationResponse.EResponse
    k_eTooBusy: CMsgClientToGCShowcaseModerationApplyModerationResponse.EResponse
    k_eDisabled: CMsgClientToGCShowcaseModerationApplyModerationResponse.EResponse
    k_eTimeout: CMsgClientToGCShowcaseModerationApplyModerationResponse.EResponse
    k_eNoPermission: CMsgClientToGCShowcaseModerationApplyModerationResponse.EResponse
    k_eGone: CMsgClientToGCShowcaseModerationApplyModerationResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCShowcaseModerationApplyModerationResponse.EResponse
    def __init__(self, response: _Optional[_Union[CMsgClientToGCShowcaseModerationApplyModerationResponse.EResponse, str]] = ...) -> None: ...
