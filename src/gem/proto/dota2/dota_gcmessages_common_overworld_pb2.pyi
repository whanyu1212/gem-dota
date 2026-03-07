from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

import dota_gcmessages_common_pb2 as _dota_gcmessages_common_pb2
import dota_gcmessages_common_survivors_pb2 as _dota_gcmessages_common_survivors_pb2
import gcsdk_gcmessages_pb2 as _gcsdk_gcmessages_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

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
    def __init__(self, token_id: int | None = ..., token_count: int | None = ...) -> None: ...

class CMsgOverworldTokenQuantity(_message.Message):
    __slots__ = ("token_counts",)
    TOKEN_COUNTS_FIELD_NUMBER: _ClassVar[int]
    token_counts: _containers.RepeatedCompositeFieldContainer[CMsgOverworldTokenCount]
    def __init__(
        self, token_counts: _Iterable[CMsgOverworldTokenCount | _Mapping] | None = ...
    ) -> None: ...

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
        def __init__(
            self,
            reward_data: int | None = ...,
            token_cost: CMsgOverworldTokenQuantity | _Mapping | None = ...,
            token_reward: CMsgOverworldTokenQuantity | _Mapping | None = ...,
        ) -> None: ...

    REWARD_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    reward_options: _containers.RepeatedCompositeFieldContainer[
        CMsgOverworldEncounterTokenTreasureData.RewardOption
    ]
    def __init__(
        self,
        reward_options: _Iterable[CMsgOverworldEncounterTokenTreasureData.RewardOption | _Mapping]
        | None = ...,
    ) -> None: ...

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
        def __init__(
            self,
            reward_data: int | None = ...,
            token_cost: CMsgOverworldTokenQuantity | _Mapping | None = ...,
            token_reward: CMsgOverworldTokenQuantity | _Mapping | None = ...,
        ) -> None: ...

    QUESTS_FIELD_NUMBER: _ClassVar[int]
    quests: _containers.RepeatedCompositeFieldContainer[CMsgOverworldEncounterTokenQuestData.Quest]
    def __init__(
        self, quests: _Iterable[CMsgOverworldEncounterTokenQuestData.Quest | _Mapping] | None = ...
    ) -> None: ...

class CMsgOverworldHeroList(_message.Message):
    __slots__ = ("hero_ids",)
    HERO_IDS_FIELD_NUMBER: _ClassVar[int]
    hero_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, hero_ids: _Iterable[int] | None = ...) -> None: ...

class CMsgOverworldEncounterChooseHeroData(_message.Message):
    __slots__ = ("hero_list", "additive")
    HERO_LIST_FIELD_NUMBER: _ClassVar[int]
    ADDITIVE_FIELD_NUMBER: _ClassVar[int]
    hero_list: CMsgOverworldHeroList
    additive: bool
    def __init__(
        self, hero_list: CMsgOverworldHeroList | _Mapping | None = ..., additive: bool = ...
    ) -> None: ...

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
    def __init__(
        self,
        choice: int | None = ...,
        progress: int | None = ...,
        max_progress: int | None = ...,
        visited: bool = ...,
    ) -> None: ...

class CMsgOverworldEncounterData(_message.Message):
    __slots__ = ("extra_encounter_data",)
    EXTRA_ENCOUNTER_DATA_FIELD_NUMBER: _ClassVar[int]
    extra_encounter_data: _containers.RepeatedCompositeFieldContainer[
        _gcsdk_gcmessages_pb2.CExtraMsgBlock
    ]
    def __init__(
        self,
        extra_encounter_data: _Iterable[_gcsdk_gcmessages_pb2.CExtraMsgBlock | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgOverworldNode(_message.Message):
    __slots__ = ("node_id", "node_state", "node_encounter_data")
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_STATE_FIELD_NUMBER: _ClassVar[int]
    NODE_ENCOUNTER_DATA_FIELD_NUMBER: _ClassVar[int]
    node_id: int
    node_state: EOverworldNodeState
    node_encounter_data: CMsgOverworldEncounterData
    def __init__(
        self,
        node_id: int | None = ...,
        node_state: EOverworldNodeState | str | None = ...,
        node_encounter_data: CMsgOverworldEncounterData | _Mapping | None = ...,
    ) -> None: ...

class CMsgOverworldPath(_message.Message):
    __slots__ = ("path_id", "path_cost", "path_state")
    PATH_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_COST_FIELD_NUMBER: _ClassVar[int]
    PATH_STATE_FIELD_NUMBER: _ClassVar[int]
    path_id: int
    path_cost: CMsgOverworldTokenQuantity
    path_state: EOverworldPathState
    def __init__(
        self,
        path_id: int | None = ...,
        path_cost: CMsgOverworldTokenQuantity | _Mapping | None = ...,
        path_state: EOverworldPathState | str | None = ...,
    ) -> None: ...

class CMsgOverworldMinigameCustomData(_message.Message):
    __slots__ = ("survivors_data",)
    SURVIVORS_DATA_FIELD_NUMBER: _ClassVar[int]
    survivors_data: _dota_gcmessages_common_survivors_pb2.CMsgSurvivorsUserData
    def __init__(
        self,
        survivors_data: _dota_gcmessages_common_survivors_pb2.CMsgSurvivorsUserData
        | _Mapping
        | None = ...,
    ) -> None: ...

class CMsgOverworldMinigameUserData(_message.Message):
    __slots__ = ("node_id", "currency_amount", "custom_data")
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_DATA_FIELD_NUMBER: _ClassVar[int]
    node_id: int
    currency_amount: int
    custom_data: CMsgOverworldMinigameCustomData
    def __init__(
        self,
        node_id: int | None = ...,
        currency_amount: int | None = ...,
        custom_data: CMsgOverworldMinigameCustomData | _Mapping | None = ...,
    ) -> None: ...

class CMsgOverworldUserData(_message.Message):
    __slots__ = (
        "token_inventory",
        "overworld_nodes",
        "overworld_paths",
        "current_node_id",
        "minigame_data",
    )
    class MinigameDataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: CMsgOverworldMinigameUserData
        def __init__(
            self,
            key: int | None = ...,
            value: CMsgOverworldMinigameUserData | _Mapping | None = ...,
        ) -> None: ...

    TOKEN_INVENTORY_FIELD_NUMBER: _ClassVar[int]
    OVERWORLD_NODES_FIELD_NUMBER: _ClassVar[int]
    OVERWORLD_PATHS_FIELD_NUMBER: _ClassVar[int]
    CURRENT_NODE_ID_FIELD_NUMBER: _ClassVar[int]
    MINIGAME_DATA_FIELD_NUMBER: _ClassVar[int]
    token_inventory: CMsgOverworldTokenQuantity
    overworld_nodes: _containers.RepeatedCompositeFieldContainer[CMsgOverworldNode]
    overworld_paths: _containers.RepeatedCompositeFieldContainer[CMsgOverworldPath]
    current_node_id: int
    minigame_data: _containers.RepeatedCompositeFieldContainer[
        CMsgOverworldUserData.MinigameDataEntry
    ]
    def __init__(
        self,
        token_inventory: CMsgOverworldTokenQuantity | _Mapping | None = ...,
        overworld_nodes: _Iterable[CMsgOverworldNode | _Mapping] | None = ...,
        overworld_paths: _Iterable[CMsgOverworldPath | _Mapping] | None = ...,
        current_node_id: int | None = ...,
        minigame_data: _Iterable[CMsgOverworldUserData.MinigameDataEntry | _Mapping] | None = ...,
    ) -> None: ...

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
        def __init__(
            self,
            player_slot: int | None = ...,
            tokens: CMsgOverworldTokenQuantity | _Mapping | None = ...,
            overworld_id: int | None = ...,
        ) -> None: ...

    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    players: _containers.RepeatedCompositeFieldContainer[CMsgOverworldMatchRewards.Player]
    def __init__(
        self, players: _Iterable[CMsgOverworldMatchRewards.Player | _Mapping] | None = ...
    ) -> None: ...

class CMsgClientToGCOverworldGetUserData(_message.Message):
    __slots__ = ("overworld_id",)
    OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
    overworld_id: int
    def __init__(self, overworld_id: int | None = ...) -> None: ...

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
    def __init__(
        self,
        response: CMsgClientToGCOverworldGetUserDataResponse.EResponse | str | None = ...,
        user_data: CMsgOverworldUserData | _Mapping | None = ...,
    ) -> None: ...

class CMsgGCToClientOverworldUserDataUpdated(_message.Message):
    __slots__ = ("overworld_id", "user_data")
    OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
    USER_DATA_FIELD_NUMBER: _ClassVar[int]
    overworld_id: int
    user_data: CMsgOverworldUserData
    def __init__(
        self,
        overworld_id: int | None = ...,
        user_data: CMsgOverworldUserData | _Mapping | None = ...,
    ) -> None: ...

class CMsgClientToGCOverworldCompletePath(_message.Message):
    __slots__ = ("overworld_id", "path_id")
    OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_ID_FIELD_NUMBER: _ClassVar[int]
    overworld_id: int
    path_id: int
    def __init__(self, overworld_id: int | None = ..., path_id: int | None = ...) -> None: ...

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
    def __init__(
        self,
        response: CMsgClientToGCOverworldCompletePathResponse.EResponse | str | None = ...,
        claim_response: _dota_gcmessages_common_pb2.CMsgDOTAClaimEventActionResponse
        | _Mapping
        | None = ...,
    ) -> None: ...

class CMsgOverworldEncounterPitFighterRewardData(_message.Message):
    __slots__ = ("token_id", "choice")
    TOKEN_ID_FIELD_NUMBER: _ClassVar[int]
    CHOICE_FIELD_NUMBER: _ClassVar[int]
    token_id: int
    choice: int
    def __init__(self, token_id: int | None = ..., choice: int | None = ...) -> None: ...

class CMsgClientToGCOverworldClaimEncounterReward(_message.Message):
    __slots__ = (
        "overworld_id",
        "node_id",
        "reward_data",
        "periodic_resource_id",
        "extra_reward_data",
        "leaderboard_data",
        "leaderboard_index",
        "should_claim_reward",
    )
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
    def __init__(
        self,
        overworld_id: int | None = ...,
        node_id: int | None = ...,
        reward_data: int | None = ...,
        periodic_resource_id: int | None = ...,
        extra_reward_data: CMsgOverworldEncounterData | _Mapping | None = ...,
        leaderboard_data: int | None = ...,
        leaderboard_index: int | None = ...,
        should_claim_reward: bool = ...,
    ) -> None: ...

class CMsgClientToGCOverworldClaimEncounterRewardResponse(_message.Message):
    __slots__ = ("response", "claim_response", "tokens_received")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse]
        k_eInvalidOverworld: _ClassVar[
            CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse
        ]
        k_eInvalidNode: _ClassVar[CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse]
        k_eNodeLocked: _ClassVar[CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse]
        k_eRewardAlreadyClaimed: _ClassVar[
            CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse
        ]
        k_eNodeNotEncounter: _ClassVar[
            CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse
        ]
        k_eEncounterMissingRewards: _ClassVar[
            CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse
        ]
        k_eInvalidEncounterRewardStyle: _ClassVar[
            CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse
        ]
        k_eInvalidEncounterData: _ClassVar[
            CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse
        ]
        k_eNotEnoughTokensForReward: _ClassVar[
            CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse
        ]
        k_eNotEnoughResourceForReward: _ClassVar[
            CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse
        ]
        k_eInvalidRewardData: _ClassVar[
            CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse
        ]
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
    def __init__(
        self,
        response: CMsgClientToGCOverworldClaimEncounterRewardResponse.EResponse | str | None = ...,
        claim_response: _dota_gcmessages_common_pb2.CMsgDOTAClaimEventActionResponse
        | _Mapping
        | None = ...,
        tokens_received: CMsgOverworldTokenQuantity | _Mapping | None = ...,
    ) -> None: ...

class CMsgClientToGCOverworldVisitEncounter(_message.Message):
    __slots__ = ("overworld_id", "node_id")
    OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    overworld_id: int
    node_id: int
    def __init__(self, overworld_id: int | None = ..., node_id: int | None = ...) -> None: ...

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
    def __init__(
        self, response: CMsgClientToGCOverworldVisitEncounterResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCOverworldMoveToNode(_message.Message):
    __slots__ = ("overworld_id", "node_id")
    OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    overworld_id: int
    node_id: int
    def __init__(self, overworld_id: int | None = ..., node_id: int | None = ...) -> None: ...

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
    def __init__(
        self, response: CMsgClientToGCOverworldMoveToNodeResponse.EResponse | str | None = ...
    ) -> None: ...

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
    def __init__(
        self,
        overworld_id: int | None = ...,
        token_offer: CMsgOverworldTokenQuantity | _Mapping | None = ...,
        token_request: CMsgOverworldTokenQuantity | _Mapping | None = ...,
        recipe: int | None = ...,
        encounter_id: int | None = ...,
    ) -> None: ...

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
    def __init__(
        self,
        response: CMsgClientToGCOverworldTradeTokensResponse.EResponse | str | None = ...,
        tokens_received: CMsgOverworldTokenQuantity | _Mapping | None = ...,
    ) -> None: ...

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
    def __init__(
        self,
        overworld_id: int | None = ...,
        token_gift: CMsgOverworldTokenCount | _Mapping | None = ...,
        recipient_account_id: int | None = ...,
        periodic_resource_id: int | None = ...,
    ) -> None: ...

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
    def __init__(
        self, response: CMsgClientToGCOverworldGiftTokensResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCOverworldRequestTokensNeededByFriend(_message.Message):
    __slots__ = ("friend_account_id", "overworld_id")
    FRIEND_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
    friend_account_id: int
    overworld_id: int
    def __init__(
        self, friend_account_id: int | None = ..., overworld_id: int | None = ...
    ) -> None: ...

class CMsgClientToGCOverworldRequestTokensNeededByFriendResponse(_message.Message):
    __slots__ = ("response", "token_quantity")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[
            CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse
        ]
        k_eSuccess: _ClassVar[CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse]
        k_eNotAllowed: _ClassVar[
            CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse
        ]
        k_eNodeLocked: _ClassVar[
            CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse
        ]
        k_eInvalidOverworld: _ClassVar[
            CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse
        ]
        k_eInvalidFriend: _ClassVar[
            CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse
        ]
        k_eTooManyRequests: _ClassVar[
            CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse
        ]

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
    def __init__(
        self,
        response: CMsgClientToGCOverworldRequestTokensNeededByFriendResponse.EResponse
        | str
        | None = ...,
        token_quantity: CMsgOverworldTokenQuantity | _Mapping | None = ...,
    ) -> None: ...

class CMsgClientToGCOverworldDevResetAll(_message.Message):
    __slots__ = ("overworld_id",)
    OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
    overworld_id: int
    def __init__(self, overworld_id: int | None = ...) -> None: ...

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
    def __init__(
        self, response: CMsgClientToGCOverworldDevResetAllResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCOverworldDevResetNode(_message.Message):
    __slots__ = ("overworld_id", "node_id")
    OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    overworld_id: int
    node_id: int
    def __init__(self, overworld_id: int | None = ..., node_id: int | None = ...) -> None: ...

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
    def __init__(
        self, response: CMsgClientToGCOverworldDevResetNodeResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCOverworldDevGrantTokens(_message.Message):
    __slots__ = ("overworld_id", "token_quantity")
    OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_QUANTITY_FIELD_NUMBER: _ClassVar[int]
    overworld_id: int
    token_quantity: CMsgOverworldTokenQuantity
    def __init__(
        self,
        overworld_id: int | None = ...,
        token_quantity: CMsgOverworldTokenQuantity | _Mapping | None = ...,
    ) -> None: ...

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
    def __init__(
        self, response: CMsgClientToGCOverworldDevGrantTokensResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCOverworldDevClearInventory(_message.Message):
    __slots__ = ("overworld_id",)
    OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
    overworld_id: int
    def __init__(self, overworld_id: int | None = ...) -> None: ...

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
    def __init__(
        self,
        response: CMsgClientToGCOverworldDevClearInventoryResponse.EResponse | str | None = ...,
    ) -> None: ...

class CMsgClientToGCOverworldFeedback(_message.Message):
    __slots__ = ("language", "overworld_id", "feedback")
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
    FEEDBACK_FIELD_NUMBER: _ClassVar[int]
    language: int
    overworld_id: int
    feedback: str
    def __init__(
        self, language: int | None = ..., overworld_id: int | None = ..., feedback: str | None = ...
    ) -> None: ...

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
    def __init__(
        self, response: CMsgClientToGCOverworldFeedbackResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCOverworldGetDynamicImage(_message.Message):
    __slots__ = ("magic", "image_id", "language")
    MAGIC_FIELD_NUMBER: _ClassVar[int]
    IMAGE_ID_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    magic: int
    image_id: int
    language: int
    def __init__(
        self, magic: int | None = ..., image_id: int | None = ..., language: int | None = ...
    ) -> None: ...

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
        def __init__(
            self,
            width: int | None = ...,
            height: int | None = ...,
            format: CMsgClientToGCOverworldGetDynamicImageResponse.EDynamicImageFormat
            | str
            | None = ...,
            image_bytes: bytes | None = ...,
        ) -> None: ...

    IMAGE_ID_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    image_id: int
    images: _containers.RepeatedCompositeFieldContainer[
        CMsgClientToGCOverworldGetDynamicImageResponse.Image
    ]
    def __init__(
        self,
        image_id: int | None = ...,
        images: _Iterable[CMsgClientToGCOverworldGetDynamicImageResponse.Image | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgClientToGCOverworldMinigameAction(_message.Message):
    __slots__ = (
        "overworld_id",
        "node_id",
        "action",
        "selection",
        "option_value",
        "currency_amount",
    )
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
    def __init__(
        self,
        overworld_id: int | None = ...,
        node_id: int | None = ...,
        action: EOverworldMinigameAction | str | None = ...,
        selection: int | None = ...,
        option_value: int | None = ...,
        currency_amount: int | None = ...,
    ) -> None: ...

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
        k_eNotEnoughMinigameCurrency: _ClassVar[
            CMsgClientToGCOverworldMinigameActionResponse.EResponse
        ]
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
    def __init__(
        self, response: CMsgClientToGCOverworldMinigameActionResponse.EResponse | str | None = ...
    ) -> None: ...
