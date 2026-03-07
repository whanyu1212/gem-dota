from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

import base_gcmessages_pb2 as _base_gcmessages_pb2
import dota_gcmessages_common_pb2 as _dota_gcmessages_common_pb2
import dota_shared_enums_pb2 as _dota_shared_enums_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

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
    def __init__(
        self,
        id: int | None = ...,
        original_id: int | None = ...,
        definition_index: int | None = ...,
        equipment_slot_index: int | None = ...,
    ) -> None: ...

class CMsgHeroPlusInfo(_message.Message):
    __slots__ = ("flags",)
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    flags: int
    def __init__(self, flags: int | None = ...) -> None: ...

class CMsgShowcaseItem_Trophy(_message.Message):
    __slots__ = ("data", "trophy_id")
    class Data(_message.Message):
        __slots__ = ("trophy_score",)
        TROPHY_SCORE_FIELD_NUMBER: _ClassVar[int]
        trophy_score: int
        def __init__(self, trophy_score: int | None = ...) -> None: ...

    DATA_FIELD_NUMBER: _ClassVar[int]
    TROPHY_ID_FIELD_NUMBER: _ClassVar[int]
    data: CMsgShowcaseItem_Trophy.Data
    trophy_id: int
    def __init__(
        self,
        data: CMsgShowcaseItem_Trophy.Data | _Mapping | None = ...,
        trophy_id: int | None = ...,
    ) -> None: ...

class CMsgShowcaseItem_EconItem(_message.Message):
    __slots__ = ("data", "ref")
    class Data(_message.Message):
        __slots__ = ("econ_item",)
        ECON_ITEM_FIELD_NUMBER: _ClassVar[int]
        econ_item: _base_gcmessages_pb2.CSOEconItem
        def __init__(
            self, econ_item: _base_gcmessages_pb2.CSOEconItem | _Mapping | None = ...
        ) -> None: ...

    DATA_FIELD_NUMBER: _ClassVar[int]
    REF_FIELD_NUMBER: _ClassVar[int]
    data: CMsgShowcaseItem_EconItem.Data
    ref: CMsgShowcaseEconItemReference
    def __init__(
        self,
        data: CMsgShowcaseItem_EconItem.Data | _Mapping | None = ...,
        ref: CMsgShowcaseEconItemReference | _Mapping | None = ...,
    ) -> None: ...

class CMsgShowcaseItem_Hero(_message.Message):
    __slots__ = (
        "data",
        "hero_id",
        "econ_item_refs",
        "rotation",
        "flags",
        "plus_info",
        "animation_name",
        "animation_playback_speed",
        "animation_offset",
        "zoom",
        "slot_index",
        "model_index",
    )
    class Data(_message.Message):
        __slots__ = ("econ_items", "actual_hero_id", "plus_hero_xp")
        ECON_ITEMS_FIELD_NUMBER: _ClassVar[int]
        ACTUAL_HERO_ID_FIELD_NUMBER: _ClassVar[int]
        PLUS_HERO_XP_FIELD_NUMBER: _ClassVar[int]
        econ_items: _containers.RepeatedCompositeFieldContainer[_base_gcmessages_pb2.CSOEconItem]
        actual_hero_id: int
        plus_hero_xp: int
        def __init__(
            self,
            econ_items: _Iterable[_base_gcmessages_pb2.CSOEconItem | _Mapping] | None = ...,
            actual_hero_id: int | None = ...,
            plus_hero_xp: int | None = ...,
        ) -> None: ...

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
    def __init__(
        self,
        data: CMsgShowcaseItem_Hero.Data | _Mapping | None = ...,
        hero_id: int | None = ...,
        econ_item_refs: _Iterable[CMsgShowcaseEconItemReference | _Mapping] | None = ...,
        rotation: int | None = ...,
        flags: int | None = ...,
        plus_info: CMsgHeroPlusInfo | _Mapping | None = ...,
        animation_name: str | None = ...,
        animation_playback_speed: int | None = ...,
        animation_offset: int | None = ...,
        zoom: int | None = ...,
        slot_index: int | None = ...,
        model_index: int | None = ...,
    ) -> None: ...

class CMsgShowcaseItem_HeroIcon(_message.Message):
    __slots__ = ("data", "hero_id", "econ_item_ref")
    class Data(_message.Message):
        __slots__ = ("econ_item",)
        ECON_ITEM_FIELD_NUMBER: _ClassVar[int]
        econ_item: _base_gcmessages_pb2.CSOEconItem
        def __init__(
            self, econ_item: _base_gcmessages_pb2.CSOEconItem | _Mapping | None = ...
        ) -> None: ...

    DATA_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    ECON_ITEM_REF_FIELD_NUMBER: _ClassVar[int]
    data: CMsgShowcaseItem_HeroIcon.Data
    hero_id: int
    econ_item_ref: CMsgShowcaseEconItemReference
    def __init__(
        self,
        data: CMsgShowcaseItem_HeroIcon.Data | _Mapping | None = ...,
        hero_id: int | None = ...,
        econ_item_ref: CMsgShowcaseEconItemReference | _Mapping | None = ...,
    ) -> None: ...

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
        __slots__ = (
            "hero_id",
            "timestamp",
            "duration",
            "game_mode",
            "outcome",
            "kills",
            "deaths",
            "assists",
        )
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
        def __init__(
            self,
            hero_id: int | None = ...,
            timestamp: int | None = ...,
            duration: int | None = ...,
            game_mode: _dota_shared_enums_pb2.DOTA_GameMode | str | None = ...,
            outcome: CMsgShowcaseItem_PlayerMatch.EPlayerOutcome | str | None = ...,
            kills: int | None = ...,
            deaths: int | None = ...,
            assists: int | None = ...,
        ) -> None: ...

    DATA_FIELD_NUMBER: _ClassVar[int]
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
    data: CMsgShowcaseItem_PlayerMatch.Data
    match_id: int
    player_slot: int
    def __init__(
        self,
        data: CMsgShowcaseItem_PlayerMatch.Data | _Mapping | None = ...,
        match_id: int | None = ...,
        player_slot: int | None = ...,
    ) -> None: ...

class CMsgShowcaseItem_ChatWheel(_message.Message):
    __slots__ = ("data", "chat_wheel_message_id")
    class Data(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...

    DATA_FIELD_NUMBER: _ClassVar[int]
    CHAT_WHEEL_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    data: CMsgShowcaseItem_ChatWheel.Data
    chat_wheel_message_id: int
    def __init__(
        self,
        data: CMsgShowcaseItem_ChatWheel.Data | _Mapping | None = ...,
        chat_wheel_message_id: int | None = ...,
    ) -> None: ...

class CMsgShowcaseItem_Emoticon(_message.Message):
    __slots__ = ("data", "emoticon_id")
    class Data(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...

    DATA_FIELD_NUMBER: _ClassVar[int]
    EMOTICON_ID_FIELD_NUMBER: _ClassVar[int]
    data: CMsgShowcaseItem_Emoticon.Data
    emoticon_id: int
    def __init__(
        self,
        data: CMsgShowcaseItem_Emoticon.Data | _Mapping | None = ...,
        emoticon_id: int | None = ...,
    ) -> None: ...

class CMsgShowcaseItem_SpiderGraph(_message.Message):
    __slots__ = ("data",)
    class Data(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...

    DATA_FIELD_NUMBER: _ClassVar[int]
    data: CMsgShowcaseItem_SpiderGraph.Data
    def __init__(self, data: CMsgShowcaseItem_SpiderGraph.Data | _Mapping | None = ...) -> None: ...

class CMsgShowcaseItem_UserFeed(_message.Message):
    __slots__ = ("data",)
    class Data(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...

    DATA_FIELD_NUMBER: _ClassVar[int]
    data: CMsgShowcaseItem_UserFeed.Data
    def __init__(self, data: CMsgShowcaseItem_UserFeed.Data | _Mapping | None = ...) -> None: ...

class CMsgShowcaseItem_Stat(_message.Message):
    __slots__ = ("data", "stat_id")
    class Data(_message.Message):
        __slots__ = ("stat_score",)
        STAT_SCORE_FIELD_NUMBER: _ClassVar[int]
        stat_score: int
        def __init__(self, stat_score: int | None = ...) -> None: ...

    DATA_FIELD_NUMBER: _ClassVar[int]
    STAT_ID_FIELD_NUMBER: _ClassVar[int]
    data: CMsgShowcaseItem_Stat.Data
    stat_id: _dota_gcmessages_common_pb2.CMsgDOTAProfileCard.EStatID
    def __init__(
        self,
        data: CMsgShowcaseItem_Stat.Data | _Mapping | None = ...,
        stat_id: _dota_gcmessages_common_pb2.CMsgDOTAProfileCard.EStatID | str | None = ...,
    ) -> None: ...

class CMsgShowcaseBackground(_message.Message):
    __slots__ = ("data", "loading_screen_ref", "dim", "blur", "background_id")
    class Data(_message.Message):
        __slots__ = ("loading_screen",)
        LOADING_SCREEN_FIELD_NUMBER: _ClassVar[int]
        loading_screen: _base_gcmessages_pb2.CSOEconItem
        def __init__(
            self, loading_screen: _base_gcmessages_pb2.CSOEconItem | _Mapping | None = ...
        ) -> None: ...

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
    def __init__(
        self,
        data: CMsgShowcaseBackground.Data | _Mapping | None = ...,
        loading_screen_ref: CMsgShowcaseEconItemReference | _Mapping | None = ...,
        dim: int | None = ...,
        blur: int | None = ...,
        background_id: int | None = ...,
    ) -> None: ...

class CMsgShowcaseItemData(_message.Message):
    __slots__ = (
        "trophy",
        "econ_item_icon",
        "sticker",
        "hero_model",
        "player_match",
        "chat_wheel",
        "spray",
        "emoticon",
        "courier",
        "ward",
        "hero_icon",
        "spider_graph",
        "user_feed",
        "stat",
        "roshan",
        "creep",
        "tower",
        "effigy",
        "decoration",
        "background",
    )
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
    def __init__(
        self,
        trophy: CMsgShowcaseItem_Trophy | _Mapping | None = ...,
        econ_item_icon: CMsgShowcaseItem_EconItem | _Mapping | None = ...,
        sticker: CMsgShowcaseItem_EconItem | _Mapping | None = ...,
        hero_model: CMsgShowcaseItem_Hero | _Mapping | None = ...,
        player_match: CMsgShowcaseItem_PlayerMatch | _Mapping | None = ...,
        chat_wheel: CMsgShowcaseItem_ChatWheel | _Mapping | None = ...,
        spray: CMsgShowcaseItem_ChatWheel | _Mapping | None = ...,
        emoticon: CMsgShowcaseItem_Emoticon | _Mapping | None = ...,
        courier: CMsgShowcaseItem_EconItem | _Mapping | None = ...,
        ward: CMsgShowcaseItem_EconItem | _Mapping | None = ...,
        hero_icon: CMsgShowcaseItem_HeroIcon | _Mapping | None = ...,
        spider_graph: CMsgShowcaseItem_SpiderGraph | _Mapping | None = ...,
        user_feed: CMsgShowcaseItem_UserFeed | _Mapping | None = ...,
        stat: CMsgShowcaseItem_Stat | _Mapping | None = ...,
        roshan: CMsgShowcaseItem_EconItem | _Mapping | None = ...,
        creep: CMsgShowcaseItem_EconItem | _Mapping | None = ...,
        tower: CMsgShowcaseItem_EconItem | _Mapping | None = ...,
        effigy: CMsgShowcaseItem_EconItem | _Mapping | None = ...,
        decoration: CMsgShowcaseItem_EconItem | _Mapping | None = ...,
        background: CMsgShowcaseBackground | _Mapping | None = ...,
    ) -> None: ...

class CMsgShowcaseItemPosition(_message.Message):
    __slots__ = (
        "position_x",
        "position_y",
        "scale",
        "width",
        "height",
        "rotation",
        "parent_id",
        "parent_attachment_point_id",
        "attachment_anchor_x",
        "attachment_anchor_y",
    )
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
    def __init__(
        self,
        position_x: int | None = ...,
        position_y: int | None = ...,
        scale: int | None = ...,
        width: int | None = ...,
        height: int | None = ...,
        rotation: int | None = ...,
        parent_id: int | None = ...,
        parent_attachment_point_id: int | None = ...,
        attachment_anchor_x: int | None = ...,
        attachment_anchor_y: int | None = ...,
    ) -> None: ...

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
    def __init__(
        self,
        showcase_item_id: int | None = ...,
        item_position: CMsgShowcaseItemPosition | _Mapping | None = ...,
        item_data: CMsgShowcaseItemData | _Mapping | None = ...,
        state: EShowcaseItemState | str | None = ...,
        flags: int | None = ...,
    ) -> None: ...

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
    def __init__(
        self,
        showcase_items: _Iterable[CMsgShowcaseItem | _Mapping] | None = ...,
        background: CMsgShowcaseItem | _Mapping | None = ...,
        moderation_state: CMsgShowcase.EModerationState | str | None = ...,
    ) -> None: ...

class CMsgClientToGCShowcaseGetUserData(_message.Message):
    __slots__ = ("account_id", "showcase_type")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SHOWCASE_TYPE_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    showcase_type: EShowcaseType
    def __init__(
        self, account_id: int | None = ..., showcase_type: EShowcaseType | str | None = ...
    ) -> None: ...

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
    def __init__(
        self,
        response: CMsgClientToGCShowcaseGetUserDataResponse.EResponse | str | None = ...,
        showcase: CMsgShowcase | _Mapping | None = ...,
    ) -> None: ...

class CMsgClientToGCShowcaseSetUserData(_message.Message):
    __slots__ = ("showcase_type", "showcase", "format_version")
    SHOWCASE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SHOWCASE_FIELD_NUMBER: _ClassVar[int]
    FORMAT_VERSION_FIELD_NUMBER: _ClassVar[int]
    showcase_type: EShowcaseType
    showcase: CMsgShowcase
    format_version: int
    def __init__(
        self,
        showcase_type: EShowcaseType | str | None = ...,
        showcase: CMsgShowcase | _Mapping | None = ...,
        format_version: int | None = ...,
    ) -> None: ...

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
    def __init__(
        self,
        response: CMsgClientToGCShowcaseSetUserDataResponse.EResponse | str | None = ...,
        validated_showcase: CMsgShowcase | _Mapping | None = ...,
        locked_until_timestamp: int | None = ...,
    ) -> None: ...

class CMsgClientToGCShowcaseSubmitReport(_message.Message):
    __slots__ = ("target_account_id", "showcase_type", "report_comment")
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SHOWCASE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REPORT_COMMENT_FIELD_NUMBER: _ClassVar[int]
    target_account_id: int
    showcase_type: EShowcaseType
    report_comment: str
    def __init__(
        self,
        target_account_id: int | None = ...,
        showcase_type: EShowcaseType | str | None = ...,
        report_comment: str | None = ...,
    ) -> None: ...

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
    def __init__(
        self, response: CMsgClientToGCShowcaseSubmitReportResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgShowcaseReportsRollupInfo(_message.Message):
    __slots__ = ("rollup_id", "start_timestamp", "end_timestamp")
    ROLLUP_ID_FIELD_NUMBER: _ClassVar[int]
    START_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    END_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    rollup_id: int
    start_timestamp: int
    end_timestamp: int
    def __init__(
        self,
        rollup_id: int | None = ...,
        start_timestamp: int | None = ...,
        end_timestamp: int | None = ...,
    ) -> None: ...

class CMsgShowcaseReportsRollupList(_message.Message):
    __slots__ = ("rollups",)
    ROLLUPS_FIELD_NUMBER: _ClassVar[int]
    rollups: _containers.RepeatedCompositeFieldContainer[CMsgShowcaseReportsRollupInfo]
    def __init__(
        self, rollups: _Iterable[CMsgShowcaseReportsRollupInfo | _Mapping] | None = ...
    ) -> None: ...

class CMsgShowcaseReportsRollupEntry(_message.Message):
    __slots__ = ("account_id", "showcase_type", "report_count")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SHOWCASE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REPORT_COUNT_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    showcase_type: EShowcaseType
    report_count: int
    def __init__(
        self,
        account_id: int | None = ...,
        showcase_type: EShowcaseType | str | None = ...,
        report_count: int | None = ...,
    ) -> None: ...

class CMsgShowcaseReportsRollup(_message.Message):
    __slots__ = ("rollup_info", "rollup_entries")
    ROLLUP_INFO_FIELD_NUMBER: _ClassVar[int]
    ROLLUP_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    rollup_info: CMsgShowcaseReportsRollupInfo
    rollup_entries: _containers.RepeatedCompositeFieldContainer[CMsgShowcaseReportsRollupEntry]
    def __init__(
        self,
        rollup_info: CMsgShowcaseReportsRollupInfo | _Mapping | None = ...,
        rollup_entries: _Iterable[CMsgShowcaseReportsRollupEntry | _Mapping] | None = ...,
    ) -> None: ...

class CMsgClientToGCShowcaseAdminGetReportsRollupList(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCShowcaseAdminGetReportsRollupListResponse(_message.Message):
    __slots__ = ("response", "rollup_list")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[
            CMsgClientToGCShowcaseAdminGetReportsRollupListResponse.EResponse
        ]
        k_eSuccess: _ClassVar[CMsgClientToGCShowcaseAdminGetReportsRollupListResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCShowcaseAdminGetReportsRollupListResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCShowcaseAdminGetReportsRollupListResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCShowcaseAdminGetReportsRollupListResponse.EResponse]
        k_eNoPermission: _ClassVar[
            CMsgClientToGCShowcaseAdminGetReportsRollupListResponse.EResponse
        ]

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
    def __init__(
        self,
        response: CMsgClientToGCShowcaseAdminGetReportsRollupListResponse.EResponse
        | str
        | None = ...,
        rollup_list: CMsgShowcaseReportsRollupList | _Mapping | None = ...,
    ) -> None: ...

class CMsgClientToGCShowcaseAdminGetReportsRollup(_message.Message):
    __slots__ = ("rollup_id",)
    ROLLUP_ID_FIELD_NUMBER: _ClassVar[int]
    rollup_id: int
    def __init__(self, rollup_id: int | None = ...) -> None: ...

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
    def __init__(
        self,
        response: CMsgClientToGCShowcaseAdminGetReportsRollupResponse.EResponse | str | None = ...,
        rollup: CMsgShowcaseReportsRollup | _Mapping | None = ...,
    ) -> None: ...

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
    def __init__(
        self,
        showcase_type: EShowcaseType | str | None = ...,
        audit_action: EShowcaseAuditAction | str | None = ...,
        audit_data: int | None = ...,
        timestamp: int | None = ...,
    ) -> None: ...

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
    def __init__(
        self,
        reporter_account_id: int | None = ...,
        showcase_type: EShowcaseType | str | None = ...,
        report_timestamp: int | None = ...,
        report_comment: str | None = ...,
    ) -> None: ...

class CMsgShowcaseAdminUserDetails(_message.Message):
    __slots__ = ("locked_until_timestamp", "audit_entries", "reports")
    LOCKED_UNTIL_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    AUDIT_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    REPORTS_FIELD_NUMBER: _ClassVar[int]
    locked_until_timestamp: int
    audit_entries: _containers.RepeatedCompositeFieldContainer[CMsgShowcaseAuditEntry]
    reports: _containers.RepeatedCompositeFieldContainer[CMsgShowcaseReport]
    def __init__(
        self,
        locked_until_timestamp: int | None = ...,
        audit_entries: _Iterable[CMsgShowcaseAuditEntry | _Mapping] | None = ...,
        reports: _Iterable[CMsgShowcaseReport | _Mapping] | None = ...,
    ) -> None: ...

class CMsgClientToGCShowcaseAdminGetUserDetails(_message.Message):
    __slots__ = ("account_id",)
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    def __init__(self, account_id: int | None = ...) -> None: ...

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
    def __init__(
        self,
        response: CMsgClientToGCShowcaseAdminGetUserDetailsResponse.EResponse | str | None = ...,
        user_details: CMsgShowcaseAdminUserDetails | _Mapping | None = ...,
    ) -> None: ...

class CMsgClientToGCShowcaseAdminReset(_message.Message):
    __slots__ = ("target_account_id", "showcase_type")
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SHOWCASE_TYPE_FIELD_NUMBER: _ClassVar[int]
    target_account_id: int
    showcase_type: EShowcaseType
    def __init__(
        self, target_account_id: int | None = ..., showcase_type: EShowcaseType | str | None = ...
    ) -> None: ...

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
    def __init__(
        self, response: CMsgClientToGCShowcaseAdminResetResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCShowcaseAdminLockAccount(_message.Message):
    __slots__ = ("target_account_id", "locked_until_timestamp")
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    LOCKED_UNTIL_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    target_account_id: int
    locked_until_timestamp: int
    def __init__(
        self, target_account_id: int | None = ..., locked_until_timestamp: int | None = ...
    ) -> None: ...

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
    def __init__(
        self, response: CMsgClientToGCShowcaseAdminLockAccountResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCShowcaseAdminConvict(_message.Message):
    __slots__ = ("target_account_id", "showcase_type")
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SHOWCASE_TYPE_FIELD_NUMBER: _ClassVar[int]
    target_account_id: int
    showcase_type: EShowcaseType
    def __init__(
        self, target_account_id: int | None = ..., showcase_type: EShowcaseType | str | None = ...
    ) -> None: ...

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
    def __init__(
        self, response: CMsgClientToGCShowcaseAdminConvictResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCShowcaseAdminExonerate(_message.Message):
    __slots__ = ("target_account_id", "showcase_type")
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SHOWCASE_TYPE_FIELD_NUMBER: _ClassVar[int]
    target_account_id: int
    showcase_type: EShowcaseType
    def __init__(
        self, target_account_id: int | None = ..., showcase_type: EShowcaseType | str | None = ...
    ) -> None: ...

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
    def __init__(
        self, response: CMsgClientToGCShowcaseAdminExonerateResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgShowcaseModerationInfo(_message.Message):
    __slots__ = ("account_id", "showcase_type", "showcase_timestamp")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SHOWCASE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SHOWCASE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    showcase_type: EShowcaseType
    showcase_timestamp: int
    def __init__(
        self,
        account_id: int | None = ...,
        showcase_type: EShowcaseType | str | None = ...,
        showcase_timestamp: int | None = ...,
    ) -> None: ...

class CMsgClientToGCShowcaseModerationGetQueue(_message.Message):
    __slots__ = ("start_timestamp", "result_count")
    START_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    RESULT_COUNT_FIELD_NUMBER: _ClassVar[int]
    start_timestamp: int
    result_count: int
    def __init__(
        self, start_timestamp: int | None = ..., result_count: int | None = ...
    ) -> None: ...

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
    def __init__(
        self,
        response: CMsgClientToGCShowcaseModerationGetQueueResponse.EResponse | str | None = ...,
        showcases: _Iterable[CMsgShowcaseModerationInfo | _Mapping] | None = ...,
    ) -> None: ...

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
    def __init__(
        self,
        account_id: int | None = ...,
        showcase_type: EShowcaseType | str | None = ...,
        showcase_timestamp: int | None = ...,
        approve: bool = ...,
    ) -> None: ...

class CMsgClientToGCShowcaseModerationApplyModerationResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[
            CMsgClientToGCShowcaseModerationApplyModerationResponse.EResponse
        ]
        k_eSuccess: _ClassVar[CMsgClientToGCShowcaseModerationApplyModerationResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCShowcaseModerationApplyModerationResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCShowcaseModerationApplyModerationResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCShowcaseModerationApplyModerationResponse.EResponse]
        k_eNoPermission: _ClassVar[
            CMsgClientToGCShowcaseModerationApplyModerationResponse.EResponse
        ]
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
    def __init__(
        self,
        response: CMsgClientToGCShowcaseModerationApplyModerationResponse.EResponse
        | str
        | None = ...,
    ) -> None: ...
