from . import steammessages_pb2 as _steammessages_pb2
from . import dota_shared_enums_pb2 as _dota_shared_enums_pb2
from . import dota_gcmessages_common_pb2 as _dota_gcmessages_common_pb2
from . import gcsdk_gcmessages_pb2 as _gcsdk_gcmessages_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EItemBattlerAuditAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eItemBattlerAuditAction_Invalid: _ClassVar[EItemBattlerAuditAction]

class EItemBattlerGameState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eGameState_Invalid: _ClassVar[EItemBattlerGameState]
    k_eGameState_ChoosingEncounter: _ClassVar[EItemBattlerGameState]
    k_eGameState_Encounter_Choice: _ClassVar[EItemBattlerGameState]
    k_eGameState_Encounter_Shop: _ClassVar[EItemBattlerGameState]
    k_eGameState_ChoosingMonster: _ClassVar[EItemBattlerGameState]
    k_eGameState_SearchingForOpponent: _ClassVar[EItemBattlerGameState]
    k_eGameState_ShowingOpponent: _ClassVar[EItemBattlerGameState]
    k_eGameState_PreFight: _ClassVar[EItemBattlerGameState]
    k_eGameState_Fight: _ClassVar[EItemBattlerGameState]
    k_eGameState_PostFight: _ClassVar[EItemBattlerGameState]
    k_eGameState_GameOver: _ClassVar[EItemBattlerGameState]
k_eItemBattlerAuditAction_Invalid: EItemBattlerAuditAction
k_eGameState_Invalid: EItemBattlerGameState
k_eGameState_ChoosingEncounter: EItemBattlerGameState
k_eGameState_Encounter_Choice: EItemBattlerGameState
k_eGameState_Encounter_Shop: EItemBattlerGameState
k_eGameState_ChoosingMonster: EItemBattlerGameState
k_eGameState_SearchingForOpponent: EItemBattlerGameState
k_eGameState_ShowingOpponent: EItemBattlerGameState
k_eGameState_PreFight: EItemBattlerGameState
k_eGameState_Fight: EItemBattlerGameState
k_eGameState_PostFight: EItemBattlerGameState
k_eGameState_GameOver: EItemBattlerGameState

class CMsgItemBattlerPlayerInfo(_message.Message):
    __slots__ = ("account_id", "rank", "run_count", "victory_count", "concede_count")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    RUN_COUNT_FIELD_NUMBER: _ClassVar[int]
    VICTORY_COUNT_FIELD_NUMBER: _ClassVar[int]
    CONCEDE_COUNT_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    rank: int
    run_count: int
    victory_count: int
    concede_count: int
    def __init__(self, account_id: _Optional[int] = ..., rank: _Optional[int] = ..., run_count: _Optional[int] = ..., victory_count: _Optional[int] = ..., concede_count: _Optional[int] = ...) -> None: ...

class CMsgItemBattlerItemModifier(_message.Message):
    __slots__ = ("type", "value", "multiplicative")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    MULTIPLICATIVE_FIELD_NUMBER: _ClassVar[int]
    type: int
    value: float
    multiplicative: bool
    def __init__(self, type: _Optional[int] = ..., value: _Optional[float] = ..., multiplicative: bool = ...) -> None: ...

class CMsgItemBattlerItem(_message.Message):
    __slots__ = ("item_definition_id", "item_instance_id", "item_container_id", "position_x", "position_y", "permanent_modifiers")
    ITEM_DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_CONTAINER_ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_X_FIELD_NUMBER: _ClassVar[int]
    POSITION_Y_FIELD_NUMBER: _ClassVar[int]
    PERMANENT_MODIFIERS_FIELD_NUMBER: _ClassVar[int]
    item_definition_id: int
    item_instance_id: int
    item_container_id: int
    position_x: int
    position_y: int
    permanent_modifiers: _containers.RepeatedCompositeFieldContainer[CMsgItemBattlerItemModifier]
    def __init__(self, item_definition_id: _Optional[int] = ..., item_instance_id: _Optional[int] = ..., item_container_id: _Optional[int] = ..., position_x: _Optional[int] = ..., position_y: _Optional[int] = ..., permanent_modifiers: _Optional[_Iterable[_Union[CMsgItemBattlerItemModifier, _Mapping]]] = ...) -> None: ...

class CMsgItemBattlerItemContainer(_message.Message):
    __slots__ = ("item_container_id", "item_slot_ids", "width", "height", "is_shop")
    ITEM_CONTAINER_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_SLOT_IDS_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    IS_SHOP_FIELD_NUMBER: _ClassVar[int]
    item_container_id: int
    item_slot_ids: _containers.RepeatedScalarFieldContainer[int]
    width: int
    height: int
    is_shop: bool
    def __init__(self, item_container_id: _Optional[int] = ..., item_slot_ids: _Optional[_Iterable[int]] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., is_shop: bool = ...) -> None: ...

class CMsgItemBattlerFightEvent(_message.Message):
    __slots__ = ("item_instance_id", "item_target_instance_ids", "tick", "effect", "value", "critical", "lifesteal_healing")
    ITEM_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_TARGET_INSTANCE_IDS_FIELD_NUMBER: _ClassVar[int]
    TICK_FIELD_NUMBER: _ClassVar[int]
    EFFECT_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    CRITICAL_FIELD_NUMBER: _ClassVar[int]
    LIFESTEAL_HEALING_FIELD_NUMBER: _ClassVar[int]
    item_instance_id: int
    item_target_instance_ids: _containers.RepeatedScalarFieldContainer[int]
    tick: int
    effect: int
    value: int
    critical: bool
    lifesteal_healing: int
    def __init__(self, item_instance_id: _Optional[int] = ..., item_target_instance_ids: _Optional[_Iterable[int]] = ..., tick: _Optional[int] = ..., effect: _Optional[int] = ..., value: _Optional[int] = ..., critical: bool = ..., lifesteal_healing: _Optional[int] = ...) -> None: ...

class CMsgItemBattlerFightResult(_message.Message):
    __slots__ = ("win", "events", "error")
    WIN_FIELD_NUMBER: _ClassVar[int]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    win: bool
    events: _containers.RepeatedCompositeFieldContainer[CMsgItemBattlerFightEvent]
    error: bool
    def __init__(self, win: bool = ..., events: _Optional[_Iterable[_Union[CMsgItemBattlerFightEvent, _Mapping]]] = ..., error: bool = ...) -> None: ...

class CMsgItemBattlerPlayerData(_message.Message):
    __slots__ = ("account_id", "hero_id", "monster_id", "board", "wins", "losses", "prestige", "level", "experience", "skills", "income", "gold", "base_max_health", "bonus_max_health", "abilities")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    MONSTER_ID_FIELD_NUMBER: _ClassVar[int]
    BOARD_FIELD_NUMBER: _ClassVar[int]
    WINS_FIELD_NUMBER: _ClassVar[int]
    LOSSES_FIELD_NUMBER: _ClassVar[int]
    PRESTIGE_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    EXPERIENCE_FIELD_NUMBER: _ClassVar[int]
    SKILLS_FIELD_NUMBER: _ClassVar[int]
    INCOME_FIELD_NUMBER: _ClassVar[int]
    GOLD_FIELD_NUMBER: _ClassVar[int]
    BASE_MAX_HEALTH_FIELD_NUMBER: _ClassVar[int]
    BONUS_MAX_HEALTH_FIELD_NUMBER: _ClassVar[int]
    ABILITIES_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    hero_id: int
    monster_id: int
    board: CMsgItemBattlerItemContainer
    wins: int
    losses: int
    prestige: int
    level: int
    experience: int
    skills: _containers.RepeatedScalarFieldContainer[int]
    income: int
    gold: int
    base_max_health: int
    bonus_max_health: int
    abilities: CMsgItemBattlerItemContainer
    def __init__(self, account_id: _Optional[int] = ..., hero_id: _Optional[int] = ..., monster_id: _Optional[int] = ..., board: _Optional[_Union[CMsgItemBattlerItemContainer, _Mapping]] = ..., wins: _Optional[int] = ..., losses: _Optional[int] = ..., prestige: _Optional[int] = ..., level: _Optional[int] = ..., experience: _Optional[int] = ..., skills: _Optional[_Iterable[int]] = ..., income: _Optional[int] = ..., gold: _Optional[int] = ..., base_max_health: _Optional[int] = ..., bonus_max_health: _Optional[int] = ..., abilities: _Optional[_Union[CMsgItemBattlerItemContainer, _Mapping]] = ...) -> None: ...

class CMsgItemBattlerEncounterData(_message.Message):
    __slots__ = ("is_shop", "encounter_id", "shop_items")
    IS_SHOP_FIELD_NUMBER: _ClassVar[int]
    ENCOUNTER_ID_FIELD_NUMBER: _ClassVar[int]
    SHOP_ITEMS_FIELD_NUMBER: _ClassVar[int]
    is_shop: bool
    encounter_id: int
    shop_items: CMsgItemBattlerItemContainer
    def __init__(self, is_shop: bool = ..., encounter_id: _Optional[int] = ..., shop_items: _Optional[_Union[CMsgItemBattlerItemContainer, _Mapping]] = ...) -> None: ...

class CMsgItemBattlerGhostData(_message.Message):
    __slots__ = ("player_data", "items", "day", "abilities")
    class ItemsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: CMsgItemBattlerItem
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[CMsgItemBattlerItem, _Mapping]] = ...) -> None: ...
    class AbilitiesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: CMsgItemBattlerItem
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[CMsgItemBattlerItem, _Mapping]] = ...) -> None: ...
    PLAYER_DATA_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    DAY_FIELD_NUMBER: _ClassVar[int]
    ABILITIES_FIELD_NUMBER: _ClassVar[int]
    player_data: CMsgItemBattlerPlayerData
    items: _containers.RepeatedCompositeFieldContainer[CMsgItemBattlerGhostData.ItemsEntry]
    day: int
    abilities: _containers.RepeatedCompositeFieldContainer[CMsgItemBattlerGhostData.AbilitiesEntry]
    def __init__(self, player_data: _Optional[_Union[CMsgItemBattlerPlayerData, _Mapping]] = ..., items: _Optional[_Iterable[_Union[CMsgItemBattlerGhostData.ItemsEntry, _Mapping]]] = ..., day: _Optional[int] = ..., abilities: _Optional[_Iterable[_Union[CMsgItemBattlerGhostData.AbilitiesEntry, _Mapping]]] = ...) -> None: ...

class CMsgItemBattlerWorldData(_message.Message):
    __slots__ = ("run_active", "run_id", "game_state", "player_data", "opponent_data", "stash", "encounter", "fight_result", "items", "day", "hour", "encounter_choices", "monster_choices", "conceded")
    class ItemsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: CMsgItemBattlerItem
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[CMsgItemBattlerItem, _Mapping]] = ...) -> None: ...
    RUN_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    GAME_STATE_FIELD_NUMBER: _ClassVar[int]
    PLAYER_DATA_FIELD_NUMBER: _ClassVar[int]
    OPPONENT_DATA_FIELD_NUMBER: _ClassVar[int]
    STASH_FIELD_NUMBER: _ClassVar[int]
    ENCOUNTER_FIELD_NUMBER: _ClassVar[int]
    FIGHT_RESULT_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    DAY_FIELD_NUMBER: _ClassVar[int]
    HOUR_FIELD_NUMBER: _ClassVar[int]
    ENCOUNTER_CHOICES_FIELD_NUMBER: _ClassVar[int]
    MONSTER_CHOICES_FIELD_NUMBER: _ClassVar[int]
    CONCEDED_FIELD_NUMBER: _ClassVar[int]
    run_active: bool
    run_id: int
    game_state: EItemBattlerGameState
    player_data: CMsgItemBattlerPlayerData
    opponent_data: CMsgItemBattlerPlayerData
    stash: CMsgItemBattlerItemContainer
    encounter: CMsgItemBattlerEncounterData
    fight_result: CMsgItemBattlerFightResult
    items: _containers.RepeatedCompositeFieldContainer[CMsgItemBattlerWorldData.ItemsEntry]
    day: int
    hour: int
    encounter_choices: _containers.RepeatedScalarFieldContainer[int]
    monster_choices: _containers.RepeatedScalarFieldContainer[int]
    conceded: bool
    def __init__(self, run_active: bool = ..., run_id: _Optional[int] = ..., game_state: _Optional[_Union[EItemBattlerGameState, str]] = ..., player_data: _Optional[_Union[CMsgItemBattlerPlayerData, _Mapping]] = ..., opponent_data: _Optional[_Union[CMsgItemBattlerPlayerData, _Mapping]] = ..., stash: _Optional[_Union[CMsgItemBattlerItemContainer, _Mapping]] = ..., encounter: _Optional[_Union[CMsgItemBattlerEncounterData, _Mapping]] = ..., fight_result: _Optional[_Union[CMsgItemBattlerFightResult, _Mapping]] = ..., items: _Optional[_Iterable[_Union[CMsgItemBattlerWorldData.ItemsEntry, _Mapping]]] = ..., day: _Optional[int] = ..., hour: _Optional[int] = ..., encounter_choices: _Optional[_Iterable[int]] = ..., monster_choices: _Optional[_Iterable[int]] = ..., conceded: bool = ...) -> None: ...

class CMsgItemBattlerGameData(_message.Message):
    __slots__ = ("seed", "world_data")
    SEED_FIELD_NUMBER: _ClassVar[int]
    WORLD_DATA_FIELD_NUMBER: _ClassVar[int]
    seed: int
    world_data: CMsgItemBattlerWorldData
    def __init__(self, seed: _Optional[int] = ..., world_data: _Optional[_Union[CMsgItemBattlerWorldData, _Mapping]] = ...) -> None: ...

class CMsgClientToGCItemBattlerGetUserData(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCItemBattlerGetUserDataResponse(_message.Message):
    __slots__ = ("response", "world_data")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCItemBattlerGetUserDataResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCItemBattlerGetUserDataResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCItemBattlerGetUserDataResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCItemBattlerGetUserDataResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCItemBattlerGetUserDataResponse.EResponse]
    k_eInternalError: CMsgClientToGCItemBattlerGetUserDataResponse.EResponse
    k_eSuccess: CMsgClientToGCItemBattlerGetUserDataResponse.EResponse
    k_eTooBusy: CMsgClientToGCItemBattlerGetUserDataResponse.EResponse
    k_eDisabled: CMsgClientToGCItemBattlerGetUserDataResponse.EResponse
    k_eTimeout: CMsgClientToGCItemBattlerGetUserDataResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    WORLD_DATA_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCItemBattlerGetUserDataResponse.EResponse
    world_data: CMsgItemBattlerWorldData
    def __init__(self, response: _Optional[_Union[CMsgClientToGCItemBattlerGetUserDataResponse.EResponse, str]] = ..., world_data: _Optional[_Union[CMsgItemBattlerWorldData, _Mapping]] = ...) -> None: ...

class CMsgItemBattlerItemAction(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCItemBattlerGameAction(_message.Message):
    __slots__ = ("action", "choice_index", "item_instance_id", "item_container_id", "item_position_x", "item_position_y")
    class EAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInvalid: _ClassVar[CMsgClientToGCItemBattlerGameAction.EAction]
        k_eStartNewRun: _ClassVar[CMsgClientToGCItemBattlerGameAction.EAction]
        k_eForfeitRun: _ClassVar[CMsgClientToGCItemBattlerGameAction.EAction]
        k_eChooseOption: _ClassVar[CMsgClientToGCItemBattlerGameAction.EAction]
        k_eContinue: _ClassVar[CMsgClientToGCItemBattlerGameAction.EAction]
        k_eItemMove: _ClassVar[CMsgClientToGCItemBattlerGameAction.EAction]
        k_eItemPurchase: _ClassVar[CMsgClientToGCItemBattlerGameAction.EAction]
        k_eItemSell: _ClassVar[CMsgClientToGCItemBattlerGameAction.EAction]
    k_eInvalid: CMsgClientToGCItemBattlerGameAction.EAction
    k_eStartNewRun: CMsgClientToGCItemBattlerGameAction.EAction
    k_eForfeitRun: CMsgClientToGCItemBattlerGameAction.EAction
    k_eChooseOption: CMsgClientToGCItemBattlerGameAction.EAction
    k_eContinue: CMsgClientToGCItemBattlerGameAction.EAction
    k_eItemMove: CMsgClientToGCItemBattlerGameAction.EAction
    k_eItemPurchase: CMsgClientToGCItemBattlerGameAction.EAction
    k_eItemSell: CMsgClientToGCItemBattlerGameAction.EAction
    ACTION_FIELD_NUMBER: _ClassVar[int]
    CHOICE_INDEX_FIELD_NUMBER: _ClassVar[int]
    ITEM_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_CONTAINER_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_POSITION_X_FIELD_NUMBER: _ClassVar[int]
    ITEM_POSITION_Y_FIELD_NUMBER: _ClassVar[int]
    action: CMsgClientToGCItemBattlerGameAction.EAction
    choice_index: int
    item_instance_id: int
    item_container_id: int
    item_position_x: int
    item_position_y: int
    def __init__(self, action: _Optional[_Union[CMsgClientToGCItemBattlerGameAction.EAction, str]] = ..., choice_index: _Optional[int] = ..., item_instance_id: _Optional[int] = ..., item_container_id: _Optional[int] = ..., item_position_x: _Optional[int] = ..., item_position_y: _Optional[int] = ...) -> None: ...

class CMsgClientToGCItemBattlerGameActionResponse(_message.Message):
    __slots__ = ("response", "updated_world_data")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCItemBattlerGameActionResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCItemBattlerGameActionResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCItemBattlerGameActionResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCItemBattlerGameActionResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCItemBattlerGameActionResponse.EResponse]
        k_eInvalidAction: _ClassVar[CMsgClientToGCItemBattlerGameActionResponse.EResponse]
    k_eInternalError: CMsgClientToGCItemBattlerGameActionResponse.EResponse
    k_eSuccess: CMsgClientToGCItemBattlerGameActionResponse.EResponse
    k_eTooBusy: CMsgClientToGCItemBattlerGameActionResponse.EResponse
    k_eDisabled: CMsgClientToGCItemBattlerGameActionResponse.EResponse
    k_eTimeout: CMsgClientToGCItemBattlerGameActionResponse.EResponse
    k_eInvalidAction: CMsgClientToGCItemBattlerGameActionResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_WORLD_DATA_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCItemBattlerGameActionResponse.EResponse
    updated_world_data: CMsgItemBattlerWorldData
    def __init__(self, response: _Optional[_Union[CMsgClientToGCItemBattlerGameActionResponse.EResponse, str]] = ..., updated_world_data: _Optional[_Union[CMsgItemBattlerWorldData, _Mapping]] = ...) -> None: ...

class CMsgClientToGCItemBattlerDevGrantItem(_message.Message):
    __slots__ = ("item_definition_id",)
    ITEM_DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    item_definition_id: int
    def __init__(self, item_definition_id: _Optional[int] = ...) -> None: ...

class CMsgClientToGCItemBattlerDevGrantItemResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCItemBattlerDevGrantItemResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCItemBattlerDevGrantItemResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCItemBattlerDevGrantItemResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCItemBattlerDevGrantItemResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCItemBattlerDevGrantItemResponse.EResponse]
    k_eInternalError: CMsgClientToGCItemBattlerDevGrantItemResponse.EResponse
    k_eSuccess: CMsgClientToGCItemBattlerDevGrantItemResponse.EResponse
    k_eTooBusy: CMsgClientToGCItemBattlerDevGrantItemResponse.EResponse
    k_eDisabled: CMsgClientToGCItemBattlerDevGrantItemResponse.EResponse
    k_eTimeout: CMsgClientToGCItemBattlerDevGrantItemResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCItemBattlerDevGrantItemResponse.EResponse
    def __init__(self, response: _Optional[_Union[CMsgClientToGCItemBattlerDevGrantItemResponse.EResponse, str]] = ...) -> None: ...

class CMsgGCToClientItemBattlerUserDataUpdated(_message.Message):
    __slots__ = ("world_data",)
    WORLD_DATA_FIELD_NUMBER: _ClassVar[int]
    world_data: CMsgItemBattlerWorldData
    def __init__(self, world_data: _Optional[_Union[CMsgItemBattlerWorldData, _Mapping]] = ...) -> None: ...
