from . import steammessages_pb2 as _steammessages_pb2
from . import dota_shared_enums_pb2 as _dota_shared_enums_pb2
from . import dota_gcmessages_common_pb2 as _dota_gcmessages_common_pb2
from . import dota_gcmessages_common_survivors_pb2 as _dota_gcmessages_common_survivors_pb2
from . import gcsdk_gcmessages_pb2 as _gcsdk_gcmessages_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EOverworldNodeState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eOverworldNodeState_Invalid: _ClassVar[EOverworldNodeState]
    k_eOverworldNodeState_Locked: _ClassVar[EOverworldNodeState]
    k_eOverworldNodeState_Unlocked: _ClassVar[EOverworldNodeState]

class EOverworldPathState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eOverworldPathState_Invalid: _ClassVar[EOverworldPathState]
    k_eOverworldPathState_Incomplete: _ClassVar[EOverworldPathState]
    k_eOverworldPathState_Complete: _ClassVar[EOverworldPathState]

class EOverworldAuditAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eOverworldAuditAction_Invalid: _ClassVar[EOverworldAuditAction]
    k_eOverworldAuditAction_DevModifyTokens: _ClassVar[EOverworldAuditAction]
    k_eOverworldAuditAction_DevClearInventory: _ClassVar[EOverworldAuditAction]
    k_eOverworldAuditAction_DevGrantTokens: _ClassVar[EOverworldAuditAction]
    k_eOverworldAuditAction_CompletePath: _ClassVar[EOverworldAuditAction]
    k_eOverworldAuditAction_ClaimEncounterReward: _ClassVar[EOverworldAuditAction]
    k_eOverworldAuditAction_DevResetNode: _ClassVar[EOverworldAuditAction]
    k_eOverworldAuditAction_DevResetPath: _ClassVar[EOverworldAuditAction]
    k_eOverworldAuditAction_MatchRewardsFull: _ClassVar[EOverworldAuditAction]
    k_eOverworldAuditAction_MatchRewardsHalf: _ClassVar[EOverworldAuditAction]
    k_eOverworldAuditAction_EventActionTokenGrant: _ClassVar[EOverworldAuditAction]
    k_eOverworldAuditAction_TokenTraderLost: _ClassVar[EOverworldAuditAction]
    k_eOverworldAuditAction_TokenTraderGained: _ClassVar[EOverworldAuditAction]
    k_eOverworldAuditAction_EncounterRewardTokenCost: _ClassVar[EOverworldAuditAction]
    k_eOverworldAuditAction_EncounterRewardTokenReward: _ClassVar[EOverworldAuditAction]
    k_eOverworldAuditAction_SupportGrantTokens: _ClassVar[EOverworldAuditAction]
    k_eOverworldAuditAction_TokenGiftSent: _ClassVar[EOverworldAuditAction]
    k_eOverworldAuditAction_DevSetFortune: _ClassVar[EOverworldAuditAction]
    k_eOverworldAuditAction_DevClearFortune: _ClassVar[EOverworldAuditAction]
    k_eOverworldAuditAction_RequestFortune: _ClassVar[EOverworldAuditAction]

class EOverworldMinigameAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eOverworldMinigameAction_Invalid: _ClassVar[EOverworldMinigameAction]
    k_eOverworldMinigameAction_DevReset: _ClassVar[EOverworldMinigameAction]
    k_eOverworldMinigameAction_DevGiveCurrency: _ClassVar[EOverworldMinigameAction]
    k_eOverworldMinigameAction_Purchase: _ClassVar[EOverworldMinigameAction]
    k_eOverworldMinigameAction_SetOption: _ClassVar[EOverworldMinigameAction]
    k_eOverworldMinigameAction_ReportCurrencyGained: _ClassVar[EOverworldMinigameAction]
    k_eOverworldMinigameAction_UnlockDifficulty: _ClassVar[EOverworldMinigameAction]
k_eOverworldNodeState_Invalid: EOverworldNodeState
k_eOverworldNodeState_Locked: EOverworldNodeState
k_eOverworldNodeState_Unlocked: EOverworldNodeState
k_eOverworldPathState_Invalid: EOverworldPathState
k_eOverworldPathState_Incomplete: EOverworldPathState
k_eOverworldPathState_Complete: EOverworldPathState
k_eOverworldAuditAction_Invalid: EOverworldAuditAction
k_eOverworldAuditAction_DevModifyTokens: EOverworldAuditAction
k_eOverworldAuditAction_DevClearInventory: EOverworldAuditAction
k_eOverworldAuditAction_DevGrantTokens: EOverworldAuditAction
k_eOverworldAuditAction_CompletePath: EOverworldAuditAction
k_eOverworldAuditAction_ClaimEncounterReward: EOverworldAuditAction
k_eOverworldAuditAction_DevResetNode: EOverworldAuditAction
k_eOverworldAuditAction_DevResetPath: EOverworldAuditAction
k_eOverworldAuditAction_MatchRewardsFull: EOverworldAuditAction
k_eOverworldAuditAction_MatchRewardsHalf: EOverworldAuditAction
k_eOverworldAuditAction_EventActionTokenGrant: EOverworldAuditAction
k_eOverworldAuditAction_TokenTraderLost: EOverworldAuditAction
k_eOverworldAuditAction_TokenTraderGained: EOverworldAuditAction
k_eOverworldAuditAction_EncounterRewardTokenCost: EOverworldAuditAction
k_eOverworldAuditAction_EncounterRewardTokenReward: EOverworldAuditAction
k_eOverworldAuditAction_SupportGrantTokens: EOverworldAuditAction
k_eOverworldAuditAction_TokenGiftSent: EOverworldAuditAction
k_eOverworldAuditAction_DevSetFortune: EOverworldAuditAction
k_eOverworldAuditAction_DevClearFortune: EOverworldAuditAction
k_eOverworldAuditAction_RequestFortune: EOverworldAuditAction
k_eOverworldMinigameAction_Invalid: EOverworldMinigameAction
k_eOverworldMinigameAction_DevReset: EOverworldMinigameAction
k_eOverworldMinigameAction_DevGiveCurrency: EOverworldMinigameAction
k_eOverworldMinigameAction_Purchase: EOverworldMinigameAction
k_eOverworldMinigameAction_SetOption: EOverworldMinigameAction
k_eOverworldMinigameAction_ReportCurrencyGained: EOverworldMinigameAction
k_eOverworldMinigameAction_UnlockDifficulty: EOverworldMinigameAction

class CMsgOverworldTokenCount(_message.Message):
    __slots__ = ("token_id", "token_count")
    TOKEN_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_COUNT_FIELD_NUMBER: _ClassVar[int]
    token_id: int
    token_count: int
    def __init__(self, token_id: _Optional[int] = ..., token_count: _Optional[int] = ...) -> None: ...

class CMsgOverworldTokenQuantity(_message.Message):
    __slots__ = ("token_counts",)
    TOKEN_COUNTS_FIELD_NUMBER: _ClassVar[int]
    token_counts: _containers.RepeatedCompositeFieldContainer[CMsgOverworldTokenCount]
    def __init__(self, token_counts: _Optional[_Iterable[_Union[CMsgOverworldTokenCount, _Mapping]]] = ...) -> None: ...

class CMsgOverworldEncounterTokenTreasureData(_message.Message):
    __slots__ = ("reward_options",)
    class RewardOption(_message.Message):
        __slots__ = ("reward_data", "token_cost", "token_reward")
        REWARD_DATA_FIELD_NUMBER: _ClassVar[int]
        TOKEN_COST_FIELD_NUMBER: _ClassVar[int]
        TOKEN_REWARD_FIELD_NUMBER: _ClassVar[int]
        reward_data: int
        token_cost: CMsgOverworldTokenQuantity
        token_reward: CMsgOverworldTokenQuantity
        def __init__(self, reward_data: _Optional[int] = ..., token_cost: _Optional[_Union[CMsgOverworldTokenQuantity, _Mapping]] = ..., token_reward: _Optional[_Union[CMsgOverworldTokenQuantity, _Mapping]] = ...) -> None: ...
    REWARD_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    reward_options: _containers.RepeatedCompositeFieldContainer[CMsgOverworldEncounterTokenTreasureData.RewardOption]
    def __init__(self, reward_options: _Optional[_Iterable[_Union[CMsgOverworldEncounterTokenTreasureData.RewardOption, _Mapping]]] = ...) -> None: ...

class CMsgOverworldEncounterTokenQuestData(_message.Message):
    __slots__ = ("quests",)
    class Quest(_message.Message):
        __slots__ = ("reward_data", "token_cost", "token_reward")
        REWARD_DATA_FIELD_NUMBER: _ClassVar[int]
        TOKEN_COST_FIELD_NUMBER: _ClassVar[int]
        TOKEN_REWARD_FIELD_NUMBER: _ClassVar[int]
        reward_data: int
        token_cost: CMsgOverworldTokenQuantity
        token_reward: CMsgOverworldTokenQuantity
        def __init__(self, reward_data: _Optional[int] = ..., token_cost: _Optional[_Union[CMsgOverworldTokenQuantity, _Mapping]] = ..., token_reward: _Optional[_Union[CMsgOverworldTokenQuantity, _Mapping]] = ...) -> None: ...
    QUESTS_FIELD_NUMBER: _ClassVar[int]
    quests: _containers.RepeatedCompositeFieldContainer[CMsgOverworldEncounterTokenQuestData.Quest]
    def __init__(self, quests: _Optional[_Iterable[_Union[CMsgOverworldEncounterTokenQuestData.Quest, _Mapping]]] = ...) -> None: ...

class CMsgOverworldHeroList(_message.Message):
    __slots__ = ("hero_ids",)
    HERO_IDS_FIELD_NUMBER: _ClassVar[int]
    hero_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, hero_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class CMsgOverworldEncounterChooseHeroData(_message.Message):
    __slots__ = ("hero_list", "additive")
    HERO_LIST_FIELD_NUMBER: _ClassVar[int]
    ADDITIVE_FIELD_NUMBER: _ClassVar[int]
    hero_list: CMsgOverworldHeroList
    additive: bool
    def __init__(self, hero_list: _Optional[_Union[CMsgOverworldHeroList, _Mapping]] = ..., additive: bool = ...) -> None: ...

class CMsgOverworldEncounterProgressData(_message.Message):
    __slots__ = ("choice", "progress", "max_progress", "visited")
    CHOICE_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    MAX_PROGRESS_FIELD_NUMBER: _ClassVar[int]
    VISITED_FIELD_NUMBER: _ClassVar[int]
    choice: int
    progress: int
    max_progress: int
    visited: bool
    def __init__(self, choice: _Optional[int] = ..., progress: _Optional[int] = ..., max_progress: _Optional[int] = ..., visited: bool = ...) -> None: ...

class CMsgOverworldEncounterData(_message.Message):
    __slots__ = ("extra_encounter_data",)
    EXTRA_ENCOUNTER_DATA_FIELD_NUMBER: _ClassVar[int]
    extra_encounter_data: _containers.RepeatedCompositeFieldContainer[_gcsdk_gcmessages_pb2.CExtraMsgBlock]
    def __init__(self, extra_encounter_data: _Optional[_Iterable[_Union[_gcsdk_gcmessages_pb2.CExtraMsgBlock, _Mapping]]] = ...) -> None: ...

class CMsgOverworldNode(_message.Message):
    __slots__ = ("node_id", "node_state", "node_encounter_data")
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_STATE_FIELD_NUMBER: _ClassVar[int]
    NODE_ENCOUNTER_DATA_FIELD_NUMBER: _ClassVar[int]
    node_id: int
    node_state: EOverworldNodeState
    node_encounter_data: CMsgOverworldEncounterData
    def __init__(self, node_id: _Optional[int] = ..., node_state: _Optional[_Union[EOverworldNodeState, str]] = ..., node_encounter_data: _Optional[_Union[CMsgOverworldEncounterData, _Mapping]] = ...) -> None: ...

class CMsgOverworldPath(_message.Message):
    __slots__ = ("path_id", "path_cost", "path_state")
    PATH_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_COST_FIELD_NUMBER: _ClassVar[int]
    PATH_STATE_FIELD_NUMBER: _ClassVar[int]
    path_id: int
    path_cost: CMsgOverworldTokenQuantity
    path_state: EOverworldPathState
    def __init__(self, path_id: _Optional[int] = ..., path_cost: _Optional[_Union[CMsgOverworldTokenQuantity, _Mapping]] = ..., path_state: _Optional[_Union[EOverworldPathState, str]] = ...) -> None: ...

class CMsgOverworldMinigameCustomData(_message.Message):
    __slots__ = ("survivors_data",)
    SURVIVORS_DATA_FIELD_NUMBER: _ClassVar[int]
    survivors_data: _dota_gcmessages_common_survivors_pb2.CMsgSurvivorsUserData
    def __init__(self, survivors_data: _Optional[_Union[_dota_gcmessages_common_survivors_pb2.CMsgSurvivorsUserData, _Mapping]] = ...) -> None: ...

class CMsgOverworldMinigameUserData(_message.Message):
    __slots__ = ("node_id", "currency_amount", "custom_data")
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_DATA_FIELD_NUMBER: _ClassVar[int]
    node_id: int
    currency_amount: int
    custom_data: CMsgOverworldMinigameCustomData
    def __init__(self, node_id: _Optional[int] = ..., currency_amount: _Optional[int] = ..., custom_data: _Optional[_Union[CMsgOverworldMinigameCustomData, _Mapping]] = ...) -> None: ...

class CMsgOverworldFortune(_message.Message):
    __slots__ = ("fortune1", "fortune2", "fortune3", "timestamp")
    FORTUNE1_FIELD_NUMBER: _ClassVar[int]
    FORTUNE2_FIELD_NUMBER: _ClassVar[int]
    FORTUNE3_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    fortune1: int
    fortune2: int
    fortune3: int
    timestamp: int
    def __init__(self, fortune1: _Optional[int] = ..., fortune2: _Optional[int] = ..., fortune3: _Optional[int] = ..., timestamp: _Optional[int] = ...) -> None: ...

class CMsgOverworldUserData(_message.Message):
    __slots__ = ("token_inventory", "overworld_nodes", "overworld_paths", "current_node_id", "minigame_data", "current_fortune")
    class MinigameDataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: CMsgOverworldMinigameUserData
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[CMsgOverworldMinigameUserData, _Mapping]] = ...) -> None: ...
    TOKEN_INVENTORY_FIELD_NUMBER: _ClassVar[int]
    OVERWORLD_NODES_FIELD_NUMBER: _ClassVar[int]
    OVERWORLD_PATHS_FIELD_NUMBER: _ClassVar[int]
    CURRENT_NODE_ID_FIELD_NUMBER: _ClassVar[int]
    MINIGAME_DATA_FIELD_NUMBER: _ClassVar[int]
    CURRENT_FORTUNE_FIELD_NUMBER: _ClassVar[int]
    token_inventory: CMsgOverworldTokenQuantity
    overworld_nodes: _containers.RepeatedCompositeFieldContainer[CMsgOverworldNode]
    overworld_paths: _containers.RepeatedCompositeFieldContainer[CMsgOverworldPath]
    current_node_id: int
    minigame_data: _containers.RepeatedCompositeFieldContainer[CMsgOverworldUserData.MinigameDataEntry]
    current_fortune: CMsgOverworldFortune
    def __init__(self, token_inventory: _Optional[_Union[CMsgOverworldTokenQuantity, _Mapping]] = ..., overworld_nodes: _Optional[_Iterable[_Union[CMsgOverworldNode, _Mapping]]] = ..., overworld_paths: _Optional[_Iterable[_Union[CMsgOverworldPath, _Mapping]]] = ..., current_node_id: _Optional[int] = ..., minigame_data: _Optional[_Iterable[_Union[CMsgOverworldUserData.MinigameDataEntry, _Mapping]]] = ..., current_fortune: _Optional[_Union[CMsgOverworldFortune, _Mapping]] = ...) -> None: ...

class CMsgOverworldMatchRewards(_message.Message):
    __slots__ = ("players",)
    class Player(_message.Message):
        __slots__ = ("player_slot", "tokens", "overworld_id")
        PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
        TOKENS_FIELD_NUMBER: _ClassVar[int]
        OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
        player_slot: int
        tokens: CMsgOverworldTokenQuantity
        overworld_id: int
        def __init__(self, player_slot: _Optional[int] = ..., tokens: _Optional[_Union[CMsgOverworldTokenQuantity, _Mapping]] = ..., overworld_id: _Optional[int] = ...) -> None: ...
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    players: _containers.RepeatedCompositeFieldContainer[CMsgOverworldMatchRewards.Player]
    def __init__(self, players: _Optional[_Iterable[_Union[CMsgOverworldMatchRewards.Player, _Mapping]]] = ...) -> None: ...

class CMsgClientToGCOverworldGetUserData(_message.Message):
    __slots__ = ("overworld_id",)
    OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
    overworld_id: int
    def __init__(self, overworld_id: _Optional[int] = ...) -> None: ...

class CMsgClientToGCOverworldGetUserDataResponse(_message.Message):
    __slots__ = ("response", "user_data")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCOverworldGetUserDataResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCOverworldGetUserDataResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCOverworldGetUserDataResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCOverworldGetUserDataResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCOverworldGetUserDataResponse.EResponse]
        k_eInvalidOverworld: _ClassVar[CMsgClientToGCOverworldGetUserDataResponse.EResponse]
    k_eInternalError: CMsgClientToGCOverworldGetUserDataResponse.EResponse
    k_eSuccess: CMsgClientToGCOverworldGetUserDataResponse.EResponse
    k_eTooBusy: CMsgClientToGCOverworldGetUserDataResponse.EResponse
    k_eDisabled: CMsgClientToGCOverworldGetUserDataResponse.EResponse
    k_eTimeout: CMsgClientToGCOverworldGetUserDataResponse.EResponse
    k_eInvalidOverworld: CMsgClientToGCOverworldGetUserDataResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    USER_DATA_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCOverworldGetUserDataResponse.EResponse
    user_data: CMsgOverworldUserData
    def __init__(self, response: _Optional[_Union[CMsgClientToGCOverworldGetUserDataResponse.EResponse, str]] = ..., user_data: _Optional[_Union[CMsgOverworldUserData, _Mapping]] = ...) -> None: ...

class CMsgGCToClientOverworldUserDataUpdated(_message.Message):
    __slots__ = ("overworld_id", "user_data")
    OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
    USER_DATA_FIELD_NUMBER: _ClassVar[int]
    overworld_id: int
    user_data: CMsgOverworldUserData
    def __init__(self, overworld_id: _Optional[int] = ..., user_data: _Optional[_Union[CMsgOverworldUserData, _Mapping]] = ...) -> None: ...

class CMsgClientToGCOverworldCompletePath(_message.Message):
    __slots__ = ("overworld_id", "path_id")
    OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_ID_FIELD_NUMBER: _ClassVar[int]
    overworld_id: int
    path_id: int
    def __init__(self, overworld_id: _Optional[int] = ..., path_id: _Optional[int] = ...) -> None: ...

class CMsgClientToGCOverworldCompletePathResponse(_message.Message):
    __slots__ = ("response", "claim_response")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCOverworldCompletePathResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCOverworldCompletePathResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCOverworldCompletePathResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCOverworldCompletePathResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCOverworldCompletePathResponse.EResponse]
        k_eInvalidOverworld: _ClassVar[CMsgClientToGCOverworldCompletePathResponse.EResponse]
        k_eInvalidPath: _ClassVar[CMsgClientToGCOverworldCompletePathResponse.EResponse]
        k_eNotEnoughTokens: _ClassVar[CMsgClientToGCOverworldCompletePathResponse.EResponse]
        k_ePathIsLocked: _ClassVar[CMsgClientToGCOverworldCompletePathResponse.EResponse]
        k_ePathAlreadyUnlocked: _ClassVar[CMsgClientToGCOverworldCompletePathResponse.EResponse]
        k_eEventExpired: _ClassVar[CMsgClientToGCOverworldCompletePathResponse.EResponse]
    k_eInternalError: CMsgClientToGCOverworldCompletePathResponse.EResponse
    k_eSuccess: CMsgClientToGCOverworldCompletePathResponse.EResponse
    k_eTooBusy: CMsgClientToGCOverworldCompletePathResponse.EResponse
    k_eDisabled: CMsgClientToGCOverworldCompletePathResponse.EResponse
    k_eTimeout: CMsgClientToGCOverworldCompletePathResponse.EResponse
    k_eInvalidOverworld: CMsgClientToGCOverworldCompletePathResponse.EResponse
    k_eInvalidPath: CMsgClientToGCOverworldCompletePathResponse.EResponse
    k_eNotEnoughTokens: CMsgClientToGCOverworldCompletePathResponse.EResponse
    k_ePathIsLocked: CMsgClientToGCOverworldCompletePathResponse.EResponse
    k_ePathAlreadyUnlocked: CMsgClientToGCOverworldCompletePathResponse.EResponse
    k_eEventExpired: CMsgClientToGCOverworldCompletePathResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    CLAIM_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCOverworldCompletePathResponse.EResponse
    claim_response: _dota_gcmessages_common_pb2.CMsgDOTAClaimEventActionResponse
    def __init__(self, response: _Optional[_Union[CMsgClientToGCOverworldCompletePathResponse.EResponse, str]] = ..., claim_response: _Optional[_Union[_dota_gcmessages_common_pb2.CMsgDOTAClaimEventActionResponse, _Mapping]] = ...) -> None: ...

class CMsgOverworldEncounterPitFighterRewardData(_message.Message):
    __slots__ = ("token_id", "choice")
    TOKEN_ID_FIELD_NUMBER: _ClassVar[int]
    CHOICE_FIELD_NUMBER: _ClassVar[int]
    token_id: int
    choice: int
    def __init__(self, token_id: _Optional[int] = ..., choice: _Optional[int] = ...) -> None: ...

class CMsgClientToGCOverworldClaimEncounterReward(_message.Message):
    __slots__ = ("overworld_id", "node_id", "reward_data", "periodic_resource_id", "extra_reward_data", "leaderboard_data", "leaderboard_index", "should_claim_reward")
    OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    REWARD_DATA_FIELD_NUMBER: _ClassVar[int]
    PERIODIC_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    EXTRA_REWARD_DATA_FIELD_NUMBER: _ClassVar[int]
    LEADERBOARD_DATA_FIELD_NUMBER: _ClassVar[int]
    LEADERBOARD_INDEX_FIELD_NUMBER: _ClassVar[int]
    SHOULD_CLAIM_REWARD_FIELD_NUMBER: _ClassVar[int]
    overworld_id: int
    node_id: int
    reward_data: int
    periodic_resource_id: int
    extra_reward_data: CMsgOverworldEncounterData
    leaderboard_data: int
    leaderboard_index: int
    should_claim_reward: bool
    def __init__(self, overworld_id: _Optional[int] = ..., node_id: _Optional[int] = ..., reward_data: _Optional[int] = ..., periodic_resource_id: _Optional[int] = ..., extra_reward_data: _Optional[_Union[CMsgOverworldEncounterData, _Mapping]] = ..., leaderboard_data: _Optional[int] = ..., leaderboard_index: _Optional[int] = ..., should_claim_reward: bool = ...) -> None: ...

class CMsgClientToGCOverworldClaimEncounterRewardResponse(_message.Message):
    __slots__ = ("response", "claim_response", "tokens_received")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse]
        k_eInvalidOverworld: _ClassVar[CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse]
        k_eInvalidNode: _ClassVar[CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse]
        k_eNodeLocked: _ClassVar[CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse]
        k_eRewardAlreadyClaimed: _ClassVar[CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse]
        k_eNodeNotEncounter: _ClassVar[CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse]
        k_eEncounterMissingRewards: _ClassVar[CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse]
        k_eInvalidEncounterRewardStyle: _ClassVar[CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse]
        k_eInvalidEncounterData: _ClassVar[CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse]
        k_eNotEnoughTokensForReward: _ClassVar[CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse]
        k_eNotEnoughResourceForReward: _ClassVar[CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse]
        k_eInvalidRewardData: _ClassVar[CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse]
        k_eEventExpired: _ClassVar[CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse]
    k_eInternalError: CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse
    k_eSuccess: CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse
    k_eTooBusy: CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse
    k_eDisabled: CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse
    k_eTimeout: CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse
    k_eInvalidOverworld: CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse
    k_eInvalidNode: CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse
    k_eNodeLocked: CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse
    k_eRewardAlreadyClaimed: CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse
    k_eNodeNotEncounter: CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse
    k_eEncounterMissingRewards: CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse
    k_eInvalidEncounterRewardStyle: CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse
    k_eInvalidEncounterData: CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse
    k_eNotEnoughTokensForReward: CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse
    k_eNotEnoughResourceForReward: CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse
    k_eInvalidRewardData: CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse
    k_eEventExpired: CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    CLAIM_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    TOKENS_RECEIVED_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse
    claim_response: _dota_gcmessages_common_pb2.CMsgDOTAClaimEventActionResponse
    tokens_received: CMsgOverworldTokenQuantity
    def __init__(self, response: _Optional[_Union[CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse, str]] = ..., claim_response: _Optional[_Union[_dota_gcmessages_common_pb2.CMsgDOTAClaimEventActionResponse, _Mapping]] = ..., tokens_received: _Optional[_Union[CMsgOverworldTokenQuantity, _Mapping]] = ...) -> None: ...

class CMsgClientToGCOverworldVisitEncounter(_message.Message):
    __slots__ = ("overworld_id", "node_id")
    OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    overworld_id: int
    node_id: int
    def __init__(self, overworld_id: _Optional[int] = ..., node_id: _Optional[int] = ...) -> None: ...

class CMsgClientToGCOverworldVisitEncounterResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCOverworldVisitEncounterResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCOverworldVisitEncounterResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCOverworldVisitEncounterResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCOverworldVisitEncounterResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCOverworldVisitEncounterResponse.EResponse]
        k_eInvalidOverworld: _ClassVar[CMsgClientToGCOverworldVisitEncounterResponse.EResponse]
        k_eInvalidNode: _ClassVar[CMsgClientToGCOverworldVisitEncounterResponse.EResponse]
        k_eNodeLocked: _ClassVar[CMsgClientToGCOverworldVisitEncounterResponse.EResponse]
        k_eNodeNotEncounter: _ClassVar[CMsgClientToGCOverworldVisitEncounterResponse.EResponse]
        k_eAlreadyVisited: _ClassVar[CMsgClientToGCOverworldVisitEncounterResponse.EResponse]
    k_eInternalError: CMsgClientToGCOverworldVisitEncounterResponse.EResponse
    k_eSuccess: CMsgClientToGCOverworldVisitEncounterResponse.EResponse
    k_eTooBusy: CMsgClientToGCOverworldVisitEncounterResponse.EResponse
    k_eDisabled: CMsgClientToGCOverworldVisitEncounterResponse.EResponse
    k_eTimeout: CMsgClientToGCOverworldVisitEncounterResponse.EResponse
    k_eInvalidOverworld: CMsgClientToGCOverworldVisitEncounterResponse.EResponse
    k_eInvalidNode: CMsgClientToGCOverworldVisitEncounterResponse.EResponse
    k_eNodeLocked: CMsgClientToGCOverworldVisitEncounterResponse.EResponse
    k_eNodeNotEncounter: CMsgClientToGCOverworldVisitEncounterResponse.EResponse
    k_eAlreadyVisited: CMsgClientToGCOverworldVisitEncounterResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCOverworldVisitEncounterResponse.EResponse
    def __init__(self, response: _Optional[_Union[CMsgClientToGCOverworldVisitEncounterResponse.EResponse, str]] = ...) -> None: ...

class CMsgClientToGCOverworldMoveToNode(_message.Message):
    __slots__ = ("overworld_id", "node_id")
    OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    overworld_id: int
    node_id: int
    def __init__(self, overworld_id: _Optional[int] = ..., node_id: _Optional[int] = ...) -> None: ...

class CMsgClientToGCOverworldMoveToNodeResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCOverworldMoveToNodeResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCOverworldMoveToNodeResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCOverworldMoveToNodeResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCOverworldMoveToNodeResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCOverworldMoveToNodeResponse.EResponse]
        k_eInvalidOverworld: _ClassVar[CMsgClientToGCOverworldMoveToNodeResponse.EResponse]
        k_eInvalidNode: _ClassVar[CMsgClientToGCOverworldMoveToNodeResponse.EResponse]
        k_eNodeLocked: _ClassVar[CMsgClientToGCOverworldMoveToNodeResponse.EResponse]
    k_eInternalError: CMsgClientToGCOverworldMoveToNodeResponse.EResponse
    k_eSuccess: CMsgClientToGCOverworldMoveToNodeResponse.EResponse
    k_eTooBusy: CMsgClientToGCOverworldMoveToNodeResponse.EResponse
    k_eDisabled: CMsgClientToGCOverworldMoveToNodeResponse.EResponse
    k_eTimeout: CMsgClientToGCOverworldMoveToNodeResponse.EResponse
    k_eInvalidOverworld: CMsgClientToGCOverworldMoveToNodeResponse.EResponse
    k_eInvalidNode: CMsgClientToGCOverworldMoveToNodeResponse.EResponse
    k_eNodeLocked: CMsgClientToGCOverworldMoveToNodeResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCOverworldMoveToNodeResponse.EResponse
    def __init__(self, response: _Optional[_Union[CMsgClientToGCOverworldMoveToNodeResponse.EResponse, str]] = ...) -> None: ...

class CMsgClientToGCOverworldTradeTokens(_message.Message):
    __slots__ = ("overworld_id", "token_offer", "token_request", "recipe", "encounter_id")
    OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_OFFER_FIELD_NUMBER: _ClassVar[int]
    TOKEN_REQUEST_FIELD_NUMBER: _ClassVar[int]
    RECIPE_FIELD_NUMBER: _ClassVar[int]
    ENCOUNTER_ID_FIELD_NUMBER: _ClassVar[int]
    overworld_id: int
    token_offer: CMsgOverworldTokenQuantity
    token_request: CMsgOverworldTokenQuantity
    recipe: int
    encounter_id: int
    def __init__(self, overworld_id: _Optional[int] = ..., token_offer: _Optional[_Union[CMsgOverworldTokenQuantity, _Mapping]] = ..., token_request: _Optional[_Union[CMsgOverworldTokenQuantity, _Mapping]] = ..., recipe: _Optional[int] = ..., encounter_id: _Optional[int] = ...) -> None: ...

class CMsgClientToGCOverworldTradeTokensResponse(_message.Message):
    __slots__ = ("response", "tokens_received")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCOverworldTradeTokensResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCOverworldTradeTokensResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCOverworldTradeTokensResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCOverworldTradeTokensResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCOverworldTradeTokensResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCOverworldTradeTokensResponse.EResponse]
        k_eNodeLocked: _ClassVar[CMsgClientToGCOverworldTradeTokensResponse.EResponse]
        k_eInvalidOverworld: _ClassVar[CMsgClientToGCOverworldTradeTokensResponse.EResponse]
        k_eInvalidOffer: _ClassVar[CMsgClientToGCOverworldTradeTokensResponse.EResponse]
        k_eNotEnoughTokens: _ClassVar[CMsgClientToGCOverworldTradeTokensResponse.EResponse]
        k_eInvalidNode: _ClassVar[CMsgClientToGCOverworldTradeTokensResponse.EResponse]
        k_eInvalidEncounter: _ClassVar[CMsgClientToGCOverworldTradeTokensResponse.EResponse]
        k_eRewardDoesNotMatchRecipe: _ClassVar[CMsgClientToGCOverworldTradeTokensResponse.EResponse]
    k_eInternalError: CMsgClientToGCOverworldTradeTokensResponse.EResponse
    k_eSuccess: CMsgClientToGCOverworldTradeTokensResponse.EResponse
    k_eTooBusy: CMsgClientToGCOverworldTradeTokensResponse.EResponse
    k_eDisabled: CMsgClientToGCOverworldTradeTokensResponse.EResponse
    k_eTimeout: CMsgClientToGCOverworldTradeTokensResponse.EResponse
    k_eNotAllowed: CMsgClientToGCOverworldTradeTokensResponse.EResponse
    k_eNodeLocked: CMsgClientToGCOverworldTradeTokensResponse.EResponse
    k_eInvalidOverworld: CMsgClientToGCOverworldTradeTokensResponse.EResponse
    k_eInvalidOffer: CMsgClientToGCOverworldTradeTokensResponse.EResponse
    k_eNotEnoughTokens: CMsgClientToGCOverworldTradeTokensResponse.EResponse
    k_eInvalidNode: CMsgClientToGCOverworldTradeTokensResponse.EResponse
    k_eInvalidEncounter: CMsgClientToGCOverworldTradeTokensResponse.EResponse
    k_eRewardDoesNotMatchRecipe: CMsgClientToGCOverworldTradeTokensResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    TOKENS_RECEIVED_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCOverworldTradeTokensResponse.EResponse
    tokens_received: CMsgOverworldTokenQuantity
    def __init__(self, response: _Optional[_Union[CMsgClientToGCOverworldTradeTokensResponse.EResponse, str]] = ..., tokens_received: _Optional[_Union[CMsgOverworldTokenQuantity, _Mapping]] = ...) -> None: ...

class CMsgClientToGCOverworldGiftTokens(_message.Message):
    __slots__ = ("overworld_id", "token_gift", "recipient_account_id", "periodic_resource_id")
    OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_GIFT_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    PERIODIC_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    overworld_id: int
    token_gift: CMsgOverworldTokenCount
    recipient_account_id: int
    periodic_resource_id: int
    def __init__(self, overworld_id: _Optional[int] = ..., token_gift: _Optional[_Union[CMsgOverworldTokenCount, _Mapping]] = ..., recipient_account_id: _Optional[int] = ..., periodic_resource_id: _Optional[int] = ...) -> None: ...

class CMsgClientToGCOverworldGiftTokensResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCOverworldGiftTokensResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCOverworldGiftTokensResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCOverworldGiftTokensResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCOverworldGiftTokensResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCOverworldGiftTokensResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCOverworldGiftTokensResponse.EResponse]
        k_eNodeLocked: _ClassVar[CMsgClientToGCOverworldGiftTokensResponse.EResponse]
        k_eInvalidOverworld: _ClassVar[CMsgClientToGCOverworldGiftTokensResponse.EResponse]
        k_eInvalidGift: _ClassVar[CMsgClientToGCOverworldGiftTokensResponse.EResponse]
        k_eNotEnoughTokens: _ClassVar[CMsgClientToGCOverworldGiftTokensResponse.EResponse]
        k_eInvalidRecipient: _ClassVar[CMsgClientToGCOverworldGiftTokensResponse.EResponse]
        k_eNotEnoughPeriodicResource: _ClassVar[CMsgClientToGCOverworldGiftTokensResponse.EResponse]
    k_eInternalError: CMsgClientToGCOverworldGiftTokensResponse.EResponse
    k_eSuccess: CMsgClientToGCOverworldGiftTokensResponse.EResponse
    k_eTooBusy: CMsgClientToGCOverworldGiftTokensResponse.EResponse
    k_eDisabled: CMsgClientToGCOverworldGiftTokensResponse.EResponse
    k_eTimeout: CMsgClientToGCOverworldGiftTokensResponse.EResponse
    k_eNotAllowed: CMsgClientToGCOverworldGiftTokensResponse.EResponse
    k_eNodeLocked: CMsgClientToGCOverworldGiftTokensResponse.EResponse
    k_eInvalidOverworld: CMsgClientToGCOverworldGiftTokensResponse.EResponse
    k_eInvalidGift: CMsgClientToGCOverworldGiftTokensResponse.EResponse
    k_eNotEnoughTokens: CMsgClientToGCOverworldGiftTokensResponse.EResponse
    k_eInvalidRecipient: CMsgClientToGCOverworldGiftTokensResponse.EResponse
    k_eNotEnoughPeriodicResource: CMsgClientToGCOverworldGiftTokensResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCOverworldGiftTokensResponse.EResponse
    def __init__(self, response: _Optional[_Union[CMsgClientToGCOverworldGiftTokensResponse.EResponse, str]] = ...) -> None: ...

class CMsgClientToGCOverworldRequestTokensNeededByFriend(_message.Message):
    __slots__ = ("friend_account_id", "overworld_id")
    FRIEND_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
    friend_account_id: int
    overworld_id: int
    def __init__(self, friend_account_id: _Optional[int] = ..., overworld_id: _Optional[int] = ...) -> None: ...

class CMsgClientToGCOverworldRequestTokensNeededByFriendResponse(_message.Message):
    __slots__ = ("response", "token_quantity")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse]
        k_eNodeLocked: _ClassVar[CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse]
        k_eInvalidOverworld: _ClassVar[CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse]
        k_eInvalidFriend: _ClassVar[CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse]
        k_eTooManyRequests: _ClassVar[CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse]
    k_eInternalError: CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse
    k_eSuccess: CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse
    k_eTooBusy: CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse
    k_eDisabled: CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse
    k_eTimeout: CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse
    k_eNotAllowed: CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse
    k_eNodeLocked: CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse
    k_eInvalidOverworld: CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse
    k_eInvalidFriend: CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse
    k_eTooManyRequests: CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    TOKEN_QUANTITY_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse
    token_quantity: CMsgOverworldTokenQuantity
    def __init__(self, response: _Optional[_Union[CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse, str]] = ..., token_quantity: _Optional[_Union[CMsgOverworldTokenQuantity, _Mapping]] = ...) -> None: ...

class CMsgClientToGCOverworldDevResetAll(_message.Message):
    __slots__ = ("overworld_id",)
    OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
    overworld_id: int
    def __init__(self, overworld_id: _Optional[int] = ...) -> None: ...

class CMsgClientToGCOverworldDevResetAllResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCOverworldDevResetAllResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCOverworldDevResetAllResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCOverworldDevResetAllResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCOverworldDevResetAllResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCOverworldDevResetAllResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCOverworldDevResetAllResponse.EResponse]
        k_eInvalidOverworld: _ClassVar[CMsgClientToGCOverworldDevResetAllResponse.EResponse]
    k_eInternalError: CMsgClientToGCOverworldDevResetAllResponse.EResponse
    k_eSuccess: CMsgClientToGCOverworldDevResetAllResponse.EResponse
    k_eTooBusy: CMsgClientToGCOverworldDevResetAllResponse.EResponse
    k_eDisabled: CMsgClientToGCOverworldDevResetAllResponse.EResponse
    k_eTimeout: CMsgClientToGCOverworldDevResetAllResponse.EResponse
    k_eNotAllowed: CMsgClientToGCOverworldDevResetAllResponse.EResponse
    k_eInvalidOverworld: CMsgClientToGCOverworldDevResetAllResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCOverworldDevResetAllResponse.EResponse
    def __init__(self, response: _Optional[_Union[CMsgClientToGCOverworldDevResetAllResponse.EResponse, str]] = ...) -> None: ...

class CMsgClientToGCOverworldDevResetNode(_message.Message):
    __slots__ = ("overworld_id", "node_id")
    OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    overworld_id: int
    node_id: int
    def __init__(self, overworld_id: _Optional[int] = ..., node_id: _Optional[int] = ...) -> None: ...

class CMsgClientToGCOverworldDevResetNodeResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCOverworldDevResetNodeResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCOverworldDevResetNodeResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCOverworldDevResetNodeResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCOverworldDevResetNodeResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCOverworldDevResetNodeResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCOverworldDevResetNodeResponse.EResponse]
        k_eInvalidOverworld: _ClassVar[CMsgClientToGCOverworldDevResetNodeResponse.EResponse]
        k_eInvalidNode: _ClassVar[CMsgClientToGCOverworldDevResetNodeResponse.EResponse]
    k_eInternalError: CMsgClientToGCOverworldDevResetNodeResponse.EResponse
    k_eSuccess: CMsgClientToGCOverworldDevResetNodeResponse.EResponse
    k_eTooBusy: CMsgClientToGCOverworldDevResetNodeResponse.EResponse
    k_eDisabled: CMsgClientToGCOverworldDevResetNodeResponse.EResponse
    k_eTimeout: CMsgClientToGCOverworldDevResetNodeResponse.EResponse
    k_eNotAllowed: CMsgClientToGCOverworldDevResetNodeResponse.EResponse
    k_eInvalidOverworld: CMsgClientToGCOverworldDevResetNodeResponse.EResponse
    k_eInvalidNode: CMsgClientToGCOverworldDevResetNodeResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCOverworldDevResetNodeResponse.EResponse
    def __init__(self, response: _Optional[_Union[CMsgClientToGCOverworldDevResetNodeResponse.EResponse, str]] = ...) -> None: ...

class CMsgClientToGCOverworldDevGrantTokens(_message.Message):
    __slots__ = ("overworld_id", "token_quantity")
    OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_QUANTITY_FIELD_NUMBER: _ClassVar[int]
    overworld_id: int
    token_quantity: CMsgOverworldTokenQuantity
    def __init__(self, overworld_id: _Optional[int] = ..., token_quantity: _Optional[_Union[CMsgOverworldTokenQuantity, _Mapping]] = ...) -> None: ...

class CMsgClientToGCOverworldDevGrantTokensResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCOverworldDevGrantTokensResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCOverworldDevGrantTokensResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCOverworldDevGrantTokensResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCOverworldDevGrantTokensResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCOverworldDevGrantTokensResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCOverworldDevGrantTokensResponse.EResponse]
        k_eInvalidOverworld: _ClassVar[CMsgClientToGCOverworldDevGrantTokensResponse.EResponse]
    k_eInternalError: CMsgClientToGCOverworldDevGrantTokensResponse.EResponse
    k_eSuccess: CMsgClientToGCOverworldDevGrantTokensResponse.EResponse
    k_eTooBusy: CMsgClientToGCOverworldDevGrantTokensResponse.EResponse
    k_eDisabled: CMsgClientToGCOverworldDevGrantTokensResponse.EResponse
    k_eTimeout: CMsgClientToGCOverworldDevGrantTokensResponse.EResponse
    k_eNotAllowed: CMsgClientToGCOverworldDevGrantTokensResponse.EResponse
    k_eInvalidOverworld: CMsgClientToGCOverworldDevGrantTokensResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCOverworldDevGrantTokensResponse.EResponse
    def __init__(self, response: _Optional[_Union[CMsgClientToGCOverworldDevGrantTokensResponse.EResponse, str]] = ...) -> None: ...

class CMsgClientToGCOverworldDevClearInventory(_message.Message):
    __slots__ = ("overworld_id",)
    OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
    overworld_id: int
    def __init__(self, overworld_id: _Optional[int] = ...) -> None: ...

class CMsgClientToGCOverworldDevClearInventoryResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCOverworldDevClearInventoryResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCOverworldDevClearInventoryResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCOverworldDevClearInventoryResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCOverworldDevClearInventoryResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCOverworldDevClearInventoryResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCOverworldDevClearInventoryResponse.EResponse]
        k_eInvalidOverworld: _ClassVar[CMsgClientToGCOverworldDevClearInventoryResponse.EResponse]
    k_eInternalError: CMsgClientToGCOverworldDevClearInventoryResponse.EResponse
    k_eSuccess: CMsgClientToGCOverworldDevClearInventoryResponse.EResponse
    k_eTooBusy: CMsgClientToGCOverworldDevClearInventoryResponse.EResponse
    k_eDisabled: CMsgClientToGCOverworldDevClearInventoryResponse.EResponse
    k_eTimeout: CMsgClientToGCOverworldDevClearInventoryResponse.EResponse
    k_eNotAllowed: CMsgClientToGCOverworldDevClearInventoryResponse.EResponse
    k_eInvalidOverworld: CMsgClientToGCOverworldDevClearInventoryResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCOverworldDevClearInventoryResponse.EResponse
    def __init__(self, response: _Optional[_Union[CMsgClientToGCOverworldDevClearInventoryResponse.EResponse, str]] = ...) -> None: ...

class CMsgClientToGCOverworldDevSetFortune(_message.Message):
    __slots__ = ("overworld_id", "fortune_id")
    OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
    FORTUNE_ID_FIELD_NUMBER: _ClassVar[int]
    overworld_id: int
    fortune_id: int
    def __init__(self, overworld_id: _Optional[int] = ..., fortune_id: _Optional[int] = ...) -> None: ...

class CMsgClientToGCOverworldDevSetFortuneResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCOverworldDevSetFortuneResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCOverworldDevSetFortuneResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCOverworldDevSetFortuneResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCOverworldDevSetFortuneResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCOverworldDevSetFortuneResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCOverworldDevSetFortuneResponse.EResponse]
        k_eInvalidOverworld: _ClassVar[CMsgClientToGCOverworldDevSetFortuneResponse.EResponse]
    k_eInternalError: CMsgClientToGCOverworldDevSetFortuneResponse.EResponse
    k_eSuccess: CMsgClientToGCOverworldDevSetFortuneResponse.EResponse
    k_eTooBusy: CMsgClientToGCOverworldDevSetFortuneResponse.EResponse
    k_eDisabled: CMsgClientToGCOverworldDevSetFortuneResponse.EResponse
    k_eTimeout: CMsgClientToGCOverworldDevSetFortuneResponse.EResponse
    k_eNotAllowed: CMsgClientToGCOverworldDevSetFortuneResponse.EResponse
    k_eInvalidOverworld: CMsgClientToGCOverworldDevSetFortuneResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCOverworldDevSetFortuneResponse.EResponse
    def __init__(self, response: _Optional[_Union[CMsgClientToGCOverworldDevSetFortuneResponse.EResponse, str]] = ...) -> None: ...

class CMsgClientToGCOverworldDevClearFortune(_message.Message):
    __slots__ = ("overworld_id", "fortune_id")
    OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
    FORTUNE_ID_FIELD_NUMBER: _ClassVar[int]
    overworld_id: int
    fortune_id: int
    def __init__(self, overworld_id: _Optional[int] = ..., fortune_id: _Optional[int] = ...) -> None: ...

class CMsgClientToGCOverworldDevClearFortuneResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCOverworldDevClearFortuneResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCOverworldDevClearFortuneResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCOverworldDevClearFortuneResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCOverworldDevClearFortuneResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCOverworldDevClearFortuneResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCOverworldDevClearFortuneResponse.EResponse]
        k_eInvalidOverworld: _ClassVar[CMsgClientToGCOverworldDevClearFortuneResponse.EResponse]
    k_eInternalError: CMsgClientToGCOverworldDevClearFortuneResponse.EResponse
    k_eSuccess: CMsgClientToGCOverworldDevClearFortuneResponse.EResponse
    k_eTooBusy: CMsgClientToGCOverworldDevClearFortuneResponse.EResponse
    k_eDisabled: CMsgClientToGCOverworldDevClearFortuneResponse.EResponse
    k_eTimeout: CMsgClientToGCOverworldDevClearFortuneResponse.EResponse
    k_eNotAllowed: CMsgClientToGCOverworldDevClearFortuneResponse.EResponse
    k_eInvalidOverworld: CMsgClientToGCOverworldDevClearFortuneResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCOverworldDevClearFortuneResponse.EResponse
    def __init__(self, response: _Optional[_Union[CMsgClientToGCOverworldDevClearFortuneResponse.EResponse, str]] = ...) -> None: ...

class CMsgClientToGCOverworldRequestFortune(_message.Message):
    __slots__ = ("overworld_id",)
    OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
    overworld_id: int
    def __init__(self, overworld_id: _Optional[int] = ...) -> None: ...

class CMsgClientToGCOverworldRequestFortuneResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCOverworldRequestFortuneResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCOverworldRequestFortuneResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCOverworldRequestFortuneResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCOverworldRequestFortuneResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCOverworldRequestFortuneResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCOverworldRequestFortuneResponse.EResponse]
        k_eInvalidOverworld: _ClassVar[CMsgClientToGCOverworldRequestFortuneResponse.EResponse]
    k_eInternalError: CMsgClientToGCOverworldRequestFortuneResponse.EResponse
    k_eSuccess: CMsgClientToGCOverworldRequestFortuneResponse.EResponse
    k_eTooBusy: CMsgClientToGCOverworldRequestFortuneResponse.EResponse
    k_eDisabled: CMsgClientToGCOverworldRequestFortuneResponse.EResponse
    k_eTimeout: CMsgClientToGCOverworldRequestFortuneResponse.EResponse
    k_eNotAllowed: CMsgClientToGCOverworldRequestFortuneResponse.EResponse
    k_eInvalidOverworld: CMsgClientToGCOverworldRequestFortuneResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCOverworldRequestFortuneResponse.EResponse
    def __init__(self, response: _Optional[_Union[CMsgClientToGCOverworldRequestFortuneResponse.EResponse, str]] = ...) -> None: ...

class CMsgClientToGCOverworldFeedback(_message.Message):
    __slots__ = ("language", "overworld_id", "feedback")
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
    FEEDBACK_FIELD_NUMBER: _ClassVar[int]
    language: int
    overworld_id: int
    feedback: str
    def __init__(self, language: _Optional[int] = ..., overworld_id: _Optional[int] = ..., feedback: _Optional[str] = ...) -> None: ...

class CMsgClientToGCOverworldFeedbackResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCOverworldFeedbackResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCOverworldFeedbackResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCOverworldFeedbackResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCOverworldFeedbackResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCOverworldFeedbackResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCOverworldFeedbackResponse.EResponse]
        k_eInvalidOverworld: _ClassVar[CMsgClientToGCOverworldFeedbackResponse.EResponse]
    k_eInternalError: CMsgClientToGCOverworldFeedbackResponse.EResponse
    k_eSuccess: CMsgClientToGCOverworldFeedbackResponse.EResponse
    k_eTooBusy: CMsgClientToGCOverworldFeedbackResponse.EResponse
    k_eDisabled: CMsgClientToGCOverworldFeedbackResponse.EResponse
    k_eTimeout: CMsgClientToGCOverworldFeedbackResponse.EResponse
    k_eNotAllowed: CMsgClientToGCOverworldFeedbackResponse.EResponse
    k_eInvalidOverworld: CMsgClientToGCOverworldFeedbackResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCOverworldFeedbackResponse.EResponse
    def __init__(self, response: _Optional[_Union[CMsgClientToGCOverworldFeedbackResponse.EResponse, str]] = ...) -> None: ...

class CMsgClientToGCOverworldGetDynamicImage(_message.Message):
    __slots__ = ("magic", "image_id", "language")
    MAGIC_FIELD_NUMBER: _ClassVar[int]
    IMAGE_ID_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    magic: int
    image_id: int
    language: int
    def __init__(self, magic: _Optional[int] = ..., image_id: _Optional[int] = ..., language: _Optional[int] = ...) -> None: ...

class CMsgClientToGCOverworldGetDynamicImageResponse(_message.Message):
    __slots__ = ("image_id", "images")
    class EDynamicImageFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eUnknown: _ClassVar[CMsgClientToGCOverworldGetDynamicImageResponse.EDynamicImageFormat]
        k_ePNG: _ClassVar[CMsgClientToGCOverworldGetDynamicImageResponse.EDynamicImageFormat]
        k_eData: _ClassVar[CMsgClientToGCOverworldGetDynamicImageResponse.EDynamicImageFormat]
    k_eUnknown: CMsgClientToGCOverworldGetDynamicImageResponse.EDynamicImageFormat
    k_ePNG: CMsgClientToGCOverworldGetDynamicImageResponse.EDynamicImageFormat
    k_eData: CMsgClientToGCOverworldGetDynamicImageResponse.EDynamicImageFormat
    class Image(_message.Message):
        __slots__ = ("width", "height", "format", "image_bytes")
        WIDTH_FIELD_NUMBER: _ClassVar[int]
        HEIGHT_FIELD_NUMBER: _ClassVar[int]
        FORMAT_FIELD_NUMBER: _ClassVar[int]
        IMAGE_BYTES_FIELD_NUMBER: _ClassVar[int]
        width: int
        height: int
        format: CMsgClientToGCOverworldGetDynamicImageResponse.EDynamicImageFormat
        image_bytes: bytes
        def __init__(self, width: _Optional[int] = ..., height: _Optional[int] = ..., format: _Optional[_Union[CMsgClientToGCOverworldGetDynamicImageResponse.EDynamicImageFormat, str]] = ..., image_bytes: _Optional[bytes] = ...) -> None: ...
    IMAGE_ID_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    image_id: int
    images: _containers.RepeatedCompositeFieldContainer[CMsgClientToGCOverworldGetDynamicImageResponse.Image]
    def __init__(self, image_id: _Optional[int] = ..., images: _Optional[_Iterable[_Union[CMsgClientToGCOverworldGetDynamicImageResponse.Image, _Mapping]]] = ...) -> None: ...

class CMsgClientToGCOverworldMinigameAction(_message.Message):
    __slots__ = ("overworld_id", "node_id", "action", "selection", "option_value", "currency_amount")
    OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    SELECTION_FIELD_NUMBER: _ClassVar[int]
    OPTION_VALUE_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    overworld_id: int
    node_id: int
    action: EOverworldMinigameAction
    selection: int
    option_value: int
    currency_amount: int
    def __init__(self, overworld_id: _Optional[int] = ..., node_id: _Optional[int] = ..., action: _Optional[_Union[EOverworldMinigameAction, str]] = ..., selection: _Optional[int] = ..., option_value: _Optional[int] = ..., currency_amount: _Optional[int] = ...) -> None: ...

class CMsgClientToGCOverworldMinigameActionResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCOverworldMinigameActionResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCOverworldMinigameActionResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCOverworldMinigameActionResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCOverworldMinigameActionResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCOverworldMinigameActionResponse.EResponse]
        k_eInvalidOverworld: _ClassVar[CMsgClientToGCOverworldMinigameActionResponse.EResponse]
        k_eInvalidNode: _ClassVar[CMsgClientToGCOverworldMinigameActionResponse.EResponse]
        k_eNodeLocked: _ClassVar[CMsgClientToGCOverworldMinigameActionResponse.EResponse]
        k_eInvalidSelection: _ClassVar[CMsgClientToGCOverworldMinigameActionResponse.EResponse]
        k_eNotEnoughTokens: _ClassVar[CMsgClientToGCOverworldMinigameActionResponse.EResponse]
        k_eNotEnoughMinigameCurrency: _ClassVar[CMsgClientToGCOverworldMinigameActionResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCOverworldMinigameActionResponse.EResponse]
    k_eInternalError: CMsgClientToGCOverworldMinigameActionResponse.EResponse
    k_eSuccess: CMsgClientToGCOverworldMinigameActionResponse.EResponse
    k_eTooBusy: CMsgClientToGCOverworldMinigameActionResponse.EResponse
    k_eDisabled: CMsgClientToGCOverworldMinigameActionResponse.EResponse
    k_eTimeout: CMsgClientToGCOverworldMinigameActionResponse.EResponse
    k_eInvalidOverworld: CMsgClientToGCOverworldMinigameActionResponse.EResponse
    k_eInvalidNode: CMsgClientToGCOverworldMinigameActionResponse.EResponse
    k_eNodeLocked: CMsgClientToGCOverworldMinigameActionResponse.EResponse
    k_eInvalidSelection: CMsgClientToGCOverworldMinigameActionResponse.EResponse
    k_eNotEnoughTokens: CMsgClientToGCOverworldMinigameActionResponse.EResponse
    k_eNotEnoughMinigameCurrency: CMsgClientToGCOverworldMinigameActionResponse.EResponse
    k_eNotAllowed: CMsgClientToGCOverworldMinigameActionResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCOverworldMinigameActionResponse.EResponse
    def __init__(self, response: _Optional[_Union[CMsgClientToGCOverworldMinigameActionResponse.EResponse, str]] = ...) -> None: ...
