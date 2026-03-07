from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

import dota_gcmessages_common_pb2 as _dota_gcmessages_common_pb2
import dota_shared_enums_pb2 as _dota_shared_enums_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class EMonsterHunterAuditAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eMonsterHunterAuditAction_Invalid: _ClassVar[EMonsterHunterAuditAction]
    k_eMonsterHunterAuditAction_DevModifyMaterials: _ClassVar[EMonsterHunterAuditAction]
    k_eMonsterHunterAuditAction_DevGrantMaterials: _ClassVar[EMonsterHunterAuditAction]
    k_eMonsterHunterAuditAction_DevResetAll: _ClassVar[EMonsterHunterAuditAction]
    k_eMonsterHunterAuditAction_ClaimReward: _ClassVar[EMonsterHunterAuditAction]
    k_eMonsterHunterAuditAction_MatchRewardsWin: _ClassVar[EMonsterHunterAuditAction]
    k_eMonsterHunterAuditAction_MatchRewardsLose: _ClassVar[EMonsterHunterAuditAction]
    k_eMonsterHunterAuditAction_MaterialTraderLost: _ClassVar[EMonsterHunterAuditAction]
    k_eMonsterHunterAuditAction_MaterialTraderGained: _ClassVar[EMonsterHunterAuditAction]
    k_eMonsterHunterAuditAction_RewardMaterialCost: _ClassVar[EMonsterHunterAuditAction]
    k_eMonsterHunterAuditAction_SupportGrantMaterials: _ClassVar[EMonsterHunterAuditAction]
    k_eMonsterHunterAuditAction_MaterialGiftSent: _ClassVar[EMonsterHunterAuditAction]
    k_eMonsterHunterAuditAction_DevClaimInvestigationRewards: _ClassVar[EMonsterHunterAuditAction]
    k_eMonsterHunterAuditAction_HeroCodexUpdate: _ClassVar[EMonsterHunterAuditAction]
    k_eMonsterHunterAuditAction_EventActionReward: _ClassVar[EMonsterHunterAuditAction]
    k_eMonsterHunterAuditAction_AutoCraft: _ClassVar[EMonsterHunterAuditAction]

class EHeroCodexEntryStatType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eHeroCodexEntryStatType_Killed: _ClassVar[EHeroCodexEntryStatType]
    k_eHeroCodexEntryStatType_WinsPlayingAsHero: _ClassVar[EHeroCodexEntryStatType]
    k_eHeroCodexEntryStatType_WinsWith: _ClassVar[EHeroCodexEntryStatType]
    k_eHeroCodexEntryStatType_LossesPlayingAsHero: _ClassVar[EHeroCodexEntryStatType]
    k_eHeroCodexEntryStatType_LossesWith: _ClassVar[EHeroCodexEntryStatType]
    k_eHeroCodexEntryStatType_TurboWinsPlayingAsHero: _ClassVar[EHeroCodexEntryStatType]
    k_eHeroCodexEntryStatType_TurboWinsWith: _ClassVar[EHeroCodexEntryStatType]
    k_eHeroCodexEntryStatType_TurboLossesPlayingAsHero: _ClassVar[EHeroCodexEntryStatType]
    k_eHeroCodexEntryStatType_TurboLossesWith: _ClassVar[EHeroCodexEntryStatType]
    k_eHeroCodexEntryStatType_Count: _ClassVar[EHeroCodexEntryStatType]

k_eMonsterHunterAuditAction_Invalid: EMonsterHunterAuditAction
k_eMonsterHunterAuditAction_DevModifyMaterials: EMonsterHunterAuditAction
k_eMonsterHunterAuditAction_DevGrantMaterials: EMonsterHunterAuditAction
k_eMonsterHunterAuditAction_DevResetAll: EMonsterHunterAuditAction
k_eMonsterHunterAuditAction_ClaimReward: EMonsterHunterAuditAction
k_eMonsterHunterAuditAction_MatchRewardsWin: EMonsterHunterAuditAction
k_eMonsterHunterAuditAction_MatchRewardsLose: EMonsterHunterAuditAction
k_eMonsterHunterAuditAction_MaterialTraderLost: EMonsterHunterAuditAction
k_eMonsterHunterAuditAction_MaterialTraderGained: EMonsterHunterAuditAction
k_eMonsterHunterAuditAction_RewardMaterialCost: EMonsterHunterAuditAction
k_eMonsterHunterAuditAction_SupportGrantMaterials: EMonsterHunterAuditAction
k_eMonsterHunterAuditAction_MaterialGiftSent: EMonsterHunterAuditAction
k_eMonsterHunterAuditAction_DevClaimInvestigationRewards: EMonsterHunterAuditAction
k_eMonsterHunterAuditAction_HeroCodexUpdate: EMonsterHunterAuditAction
k_eMonsterHunterAuditAction_EventActionReward: EMonsterHunterAuditAction
k_eMonsterHunterAuditAction_AutoCraft: EMonsterHunterAuditAction
k_eHeroCodexEntryStatType_Killed: EHeroCodexEntryStatType
k_eHeroCodexEntryStatType_WinsPlayingAsHero: EHeroCodexEntryStatType
k_eHeroCodexEntryStatType_WinsWith: EHeroCodexEntryStatType
k_eHeroCodexEntryStatType_LossesPlayingAsHero: EHeroCodexEntryStatType
k_eHeroCodexEntryStatType_LossesWith: EHeroCodexEntryStatType
k_eHeroCodexEntryStatType_TurboWinsPlayingAsHero: EHeroCodexEntryStatType
k_eHeroCodexEntryStatType_TurboWinsWith: EHeroCodexEntryStatType
k_eHeroCodexEntryStatType_TurboLossesPlayingAsHero: EHeroCodexEntryStatType
k_eHeroCodexEntryStatType_TurboLossesWith: EHeroCodexEntryStatType
k_eHeroCodexEntryStatType_Count: EHeroCodexEntryStatType

class CMsgMonsterHunterMaterialCount(_message.Message):
    __slots__ = ("material_id", "material_count")
    MATERIAL_ID_FIELD_NUMBER: _ClassVar[int]
    MATERIAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    material_id: int
    material_count: int
    def __init__(self, material_id: int | None = ..., material_count: int | None = ...) -> None: ...

class CMsgMonsterHunterHeroCodexEntry(_message.Message):
    __slots__ = ("stats", "unlocked")
    STATS_FIELD_NUMBER: _ClassVar[int]
    UNLOCKED_FIELD_NUMBER: _ClassVar[int]
    stats: _containers.RepeatedScalarFieldContainer[int]
    unlocked: bool
    def __init__(self, stats: _Iterable[int] | None = ..., unlocked: bool = ...) -> None: ...

class CMsgMonsterHunterUserData(_message.Message):
    __slots__ = ("material_inventory", "hero_codex", "unlocked_count")
    class HeroCodexEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: CMsgMonsterHunterHeroCodexEntry
        def __init__(
            self,
            key: int | None = ...,
            value: CMsgMonsterHunterHeroCodexEntry | _Mapping | None = ...,
        ) -> None: ...

    MATERIAL_INVENTORY_FIELD_NUMBER: _ClassVar[int]
    HERO_CODEX_FIELD_NUMBER: _ClassVar[int]
    UNLOCKED_COUNT_FIELD_NUMBER: _ClassVar[int]
    material_inventory: _dota_shared_enums_pb2.CMsgMonsterHunterMaterialQuantity
    hero_codex: _containers.RepeatedCompositeFieldContainer[
        CMsgMonsterHunterUserData.HeroCodexEntry
    ]
    unlocked_count: int
    def __init__(
        self,
        material_inventory: _dota_shared_enums_pb2.CMsgMonsterHunterMaterialQuantity
        | _Mapping
        | None = ...,
        hero_codex: _Iterable[CMsgMonsterHunterUserData.HeroCodexEntry | _Mapping] | None = ...,
        unlocked_count: int | None = ...,
    ) -> None: ...

class CMsgMonsterHunterMatchRewards(_message.Message):
    __slots__ = ("players",)
    class Player(_message.Message):
        __slots__ = (
            "player_slot",
            "possible_match_reward_materials",
            "actual_match_reward_materials",
            "hunt_reward",
            "denial_rewards",
            "hunter_duel",
        )
        class HuntReward(_message.Message):
            __slots__ = ("hero_id", "materials", "success")
            HERO_ID_FIELD_NUMBER: _ClassVar[int]
            MATERIALS_FIELD_NUMBER: _ClassVar[int]
            SUCCESS_FIELD_NUMBER: _ClassVar[int]
            hero_id: int
            materials: _dota_shared_enums_pb2.CMsgMonsterHunterMaterialQuantity
            success: bool
            def __init__(
                self,
                hero_id: int | None = ...,
                materials: _dota_shared_enums_pb2.CMsgMonsterHunterMaterialQuantity
                | _Mapping
                | None = ...,
                success: bool = ...,
            ) -> None: ...

        PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
        POSSIBLE_MATCH_REWARD_MATERIALS_FIELD_NUMBER: _ClassVar[int]
        ACTUAL_MATCH_REWARD_MATERIALS_FIELD_NUMBER: _ClassVar[int]
        HUNT_REWARD_FIELD_NUMBER: _ClassVar[int]
        DENIAL_REWARDS_FIELD_NUMBER: _ClassVar[int]
        HUNTER_DUEL_FIELD_NUMBER: _ClassVar[int]
        player_slot: int
        possible_match_reward_materials: _dota_shared_enums_pb2.CMsgMonsterHunterMaterialQuantity
        actual_match_reward_materials: _dota_shared_enums_pb2.CMsgMonsterHunterMaterialQuantity
        hunt_reward: CMsgMonsterHunterMatchRewards.Player.HuntReward
        denial_rewards: _containers.RepeatedCompositeFieldContainer[
            CMsgMonsterHunterMatchRewards.Player.HuntReward
        ]
        hunter_duel: bool
        def __init__(
            self,
            player_slot: int | None = ...,
            possible_match_reward_materials: _dota_shared_enums_pb2.CMsgMonsterHunterMaterialQuantity
            | _Mapping
            | None = ...,
            actual_match_reward_materials: _dota_shared_enums_pb2.CMsgMonsterHunterMaterialQuantity
            | _Mapping
            | None = ...,
            hunt_reward: CMsgMonsterHunterMatchRewards.Player.HuntReward | _Mapping | None = ...,
            denial_rewards: _Iterable[CMsgMonsterHunterMatchRewards.Player.HuntReward | _Mapping]
            | None = ...,
            hunter_duel: bool = ...,
        ) -> None: ...

    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    players: _containers.RepeatedCompositeFieldContainer[CMsgMonsterHunterMatchRewards.Player]
    def __init__(
        self, players: _Iterable[CMsgMonsterHunterMatchRewards.Player | _Mapping] | None = ...
    ) -> None: ...

class CMsgClientToGCMonsterHunterGetUserData(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCMonsterHunterGetUserDataResponse(_message.Message):
    __slots__ = ("response", "user_data")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCMonsterHunterGetUserDataResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCMonsterHunterGetUserDataResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCMonsterHunterGetUserDataResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCMonsterHunterGetUserDataResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCMonsterHunterGetUserDataResponse.EResponse]

    k_eInternalError: CMsgClientToGCMonsterHunterGetUserDataResponse.EResponse
    k_eSuccess: CMsgClientToGCMonsterHunterGetUserDataResponse.EResponse
    k_eTooBusy: CMsgClientToGCMonsterHunterGetUserDataResponse.EResponse
    k_eDisabled: CMsgClientToGCMonsterHunterGetUserDataResponse.EResponse
    k_eTimeout: CMsgClientToGCMonsterHunterGetUserDataResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    USER_DATA_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCMonsterHunterGetUserDataResponse.EResponse
    user_data: CMsgMonsterHunterUserData
    def __init__(
        self,
        response: CMsgClientToGCMonsterHunterGetUserDataResponse.EResponse | str | None = ...,
        user_data: CMsgMonsterHunterUserData | _Mapping | None = ...,
    ) -> None: ...

class CMsgGCToClientMonsterHunterUserDataUpdated(_message.Message):
    __slots__ = ("user_data",)
    USER_DATA_FIELD_NUMBER: _ClassVar[int]
    user_data: CMsgMonsterHunterUserData
    def __init__(self, user_data: CMsgMonsterHunterUserData | _Mapping | None = ...) -> None: ...

class CMsgClientToGCMonsterHunterClaimReward(_message.Message):
    __slots__ = ("item_id", "hunter_rank_reward")
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    HUNTER_RANK_REWARD_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    hunter_rank_reward: int
    def __init__(self, item_id: int | None = ..., hunter_rank_reward: int | None = ...) -> None: ...

class CMsgClientToGCMonsterHunterClaimRewardResponse(_message.Message):
    __slots__ = ("response", "claim_response", "materials_received")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCMonsterHunterClaimRewardResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCMonsterHunterClaimRewardResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCMonsterHunterClaimRewardResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCMonsterHunterClaimRewardResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCMonsterHunterClaimRewardResponse.EResponse]
        k_eRewardAlreadyClaimed: _ClassVar[CMsgClientToGCMonsterHunterClaimRewardResponse.EResponse]
        k_eNotEnoughMaterialsForReward: _ClassVar[
            CMsgClientToGCMonsterHunterClaimRewardResponse.EResponse
        ]
        k_eNotEnoughResourceForReward: _ClassVar[
            CMsgClientToGCMonsterHunterClaimRewardResponse.EResponse
        ]
        k_eRequiredHunterLevel: _ClassVar[CMsgClientToGCMonsterHunterClaimRewardResponse.EResponse]
        k_eDontHavePremium: _ClassVar[CMsgClientToGCMonsterHunterClaimRewardResponse.EResponse]

    k_eInternalError: CMsgClientToGCMonsterHunterClaimRewardResponse.EResponse
    k_eSuccess: CMsgClientToGCMonsterHunterClaimRewardResponse.EResponse
    k_eTooBusy: CMsgClientToGCMonsterHunterClaimRewardResponse.EResponse
    k_eDisabled: CMsgClientToGCMonsterHunterClaimRewardResponse.EResponse
    k_eTimeout: CMsgClientToGCMonsterHunterClaimRewardResponse.EResponse
    k_eRewardAlreadyClaimed: CMsgClientToGCMonsterHunterClaimRewardResponse.EResponse
    k_eNotEnoughMaterialsForReward: CMsgClientToGCMonsterHunterClaimRewardResponse.EResponse
    k_eNotEnoughResourceForReward: CMsgClientToGCMonsterHunterClaimRewardResponse.EResponse
    k_eRequiredHunterLevel: CMsgClientToGCMonsterHunterClaimRewardResponse.EResponse
    k_eDontHavePremium: CMsgClientToGCMonsterHunterClaimRewardResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    CLAIM_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    MATERIALS_RECEIVED_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCMonsterHunterClaimRewardResponse.EResponse
    claim_response: _dota_gcmessages_common_pb2.CMsgDOTAClaimEventActionResponse
    materials_received: _dota_shared_enums_pb2.CMsgMonsterHunterMaterialQuantity
    def __init__(
        self,
        response: CMsgClientToGCMonsterHunterClaimRewardResponse.EResponse | str | None = ...,
        claim_response: _dota_gcmessages_common_pb2.CMsgDOTAClaimEventActionResponse
        | _Mapping
        | None = ...,
        materials_received: _dota_shared_enums_pb2.CMsgMonsterHunterMaterialQuantity
        | _Mapping
        | None = ...,
    ) -> None: ...

class CMsgMonsterHunterItemSet(_message.Message):
    __slots__ = ("econ_item_id", "set_index")
    ECON_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    SET_INDEX_FIELD_NUMBER: _ClassVar[int]
    econ_item_id: int
    set_index: int
    def __init__(self, econ_item_id: int | None = ..., set_index: int | None = ...) -> None: ...

class CMsgClientToGCMonsterHunterClaimSetReward(_message.Message):
    __slots__ = ("item_sets",)
    ITEM_SETS_FIELD_NUMBER: _ClassVar[int]
    item_sets: _containers.RepeatedCompositeFieldContainer[CMsgMonsterHunterItemSet]
    def __init__(
        self, item_sets: _Iterable[CMsgMonsterHunterItemSet | _Mapping] | None = ...
    ) -> None: ...

class CMsgClientToGCMonsterHunterClaimSetRewardResponse(_message.Message):
    __slots__ = ("response", "claim_responses")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCMonsterHunterClaimSetRewardResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCMonsterHunterClaimSetRewardResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCMonsterHunterClaimSetRewardResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCMonsterHunterClaimSetRewardResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCMonsterHunterClaimSetRewardResponse.EResponse]
        k_eRewardAlreadyClaimed: _ClassVar[
            CMsgClientToGCMonsterHunterClaimSetRewardResponse.EResponse
        ]
        k_eNotEnoughMaterialsForReward: _ClassVar[
            CMsgClientToGCMonsterHunterClaimSetRewardResponse.EResponse
        ]
        k_eDontHavePremium: _ClassVar[CMsgClientToGCMonsterHunterClaimSetRewardResponse.EResponse]

    k_eInternalError: CMsgClientToGCMonsterHunterClaimSetRewardResponse.EResponse
    k_eSuccess: CMsgClientToGCMonsterHunterClaimSetRewardResponse.EResponse
    k_eTooBusy: CMsgClientToGCMonsterHunterClaimSetRewardResponse.EResponse
    k_eDisabled: CMsgClientToGCMonsterHunterClaimSetRewardResponse.EResponse
    k_eTimeout: CMsgClientToGCMonsterHunterClaimSetRewardResponse.EResponse
    k_eRewardAlreadyClaimed: CMsgClientToGCMonsterHunterClaimSetRewardResponse.EResponse
    k_eNotEnoughMaterialsForReward: CMsgClientToGCMonsterHunterClaimSetRewardResponse.EResponse
    k_eDontHavePremium: CMsgClientToGCMonsterHunterClaimSetRewardResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    CLAIM_RESPONSES_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCMonsterHunterClaimSetRewardResponse.EResponse
    claim_responses: _containers.RepeatedCompositeFieldContainer[
        _dota_gcmessages_common_pb2.CMsgDOTAClaimEventActionResponse
    ]
    def __init__(
        self,
        response: CMsgClientToGCMonsterHunterClaimSetRewardResponse.EResponse | str | None = ...,
        claim_responses: _Iterable[
            _dota_gcmessages_common_pb2.CMsgDOTAClaimEventActionResponse | _Mapping
        ]
        | None = ...,
    ) -> None: ...

class CMsgClientToGCMonsterHunterTradeMaterials(_message.Message):
    __slots__ = ("material_offer", "material_request", "recipe_id")
    MATERIAL_OFFER_FIELD_NUMBER: _ClassVar[int]
    MATERIAL_REQUEST_FIELD_NUMBER: _ClassVar[int]
    RECIPE_ID_FIELD_NUMBER: _ClassVar[int]
    material_offer: _dota_shared_enums_pb2.CMsgMonsterHunterMaterialQuantity
    material_request: _dota_shared_enums_pb2.CMsgMonsterHunterMaterialQuantity
    recipe_id: int
    def __init__(
        self,
        material_offer: _dota_shared_enums_pb2.CMsgMonsterHunterMaterialQuantity
        | _Mapping
        | None = ...,
        material_request: _dota_shared_enums_pb2.CMsgMonsterHunterMaterialQuantity
        | _Mapping
        | None = ...,
        recipe_id: int | None = ...,
    ) -> None: ...

class CMsgClientToGCMonsterHunterTradeMaterialsResponse(_message.Message):
    __slots__ = ("response", "materials_received")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCMonsterHunterTradeMaterialsResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCMonsterHunterTradeMaterialsResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCMonsterHunterTradeMaterialsResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCMonsterHunterTradeMaterialsResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCMonsterHunterTradeMaterialsResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCMonsterHunterTradeMaterialsResponse.EResponse]
        k_eInvalidOffer: _ClassVar[CMsgClientToGCMonsterHunterTradeMaterialsResponse.EResponse]
        k_eNotEnoughMaterials: _ClassVar[
            CMsgClientToGCMonsterHunterTradeMaterialsResponse.EResponse
        ]
        k_eRewardDoesNotMatchRecipe: _ClassVar[
            CMsgClientToGCMonsterHunterTradeMaterialsResponse.EResponse
        ]
        k_eAlreadyClaimedMax: _ClassVar[CMsgClientToGCMonsterHunterTradeMaterialsResponse.EResponse]

    k_eInternalError: CMsgClientToGCMonsterHunterTradeMaterialsResponse.EResponse
    k_eSuccess: CMsgClientToGCMonsterHunterTradeMaterialsResponse.EResponse
    k_eTooBusy: CMsgClientToGCMonsterHunterTradeMaterialsResponse.EResponse
    k_eDisabled: CMsgClientToGCMonsterHunterTradeMaterialsResponse.EResponse
    k_eTimeout: CMsgClientToGCMonsterHunterTradeMaterialsResponse.EResponse
    k_eNotAllowed: CMsgClientToGCMonsterHunterTradeMaterialsResponse.EResponse
    k_eInvalidOffer: CMsgClientToGCMonsterHunterTradeMaterialsResponse.EResponse
    k_eNotEnoughMaterials: CMsgClientToGCMonsterHunterTradeMaterialsResponse.EResponse
    k_eRewardDoesNotMatchRecipe: CMsgClientToGCMonsterHunterTradeMaterialsResponse.EResponse
    k_eAlreadyClaimedMax: CMsgClientToGCMonsterHunterTradeMaterialsResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    MATERIALS_RECEIVED_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCMonsterHunterTradeMaterialsResponse.EResponse
    materials_received: _dota_shared_enums_pb2.CMsgMonsterHunterMaterialQuantity
    def __init__(
        self,
        response: CMsgClientToGCMonsterHunterTradeMaterialsResponse.EResponse | str | None = ...,
        materials_received: _dota_shared_enums_pb2.CMsgMonsterHunterMaterialQuantity
        | _Mapping
        | None = ...,
    ) -> None: ...

class CMsgClientToGCMonsterHunterGiftMaterials(_message.Message):
    __slots__ = ("token_gift", "recipient_account_id", "periodic_resource_id")
    TOKEN_GIFT_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    PERIODIC_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    token_gift: CMsgMonsterHunterMaterialCount
    recipient_account_id: int
    periodic_resource_id: int
    def __init__(
        self,
        token_gift: CMsgMonsterHunterMaterialCount | _Mapping | None = ...,
        recipient_account_id: int | None = ...,
        periodic_resource_id: int | None = ...,
    ) -> None: ...

class CMsgClientToGCMonsterHunterGiftMaterialsResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCMonsterHunterGiftMaterialsResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCMonsterHunterGiftMaterialsResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCMonsterHunterGiftMaterialsResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCMonsterHunterGiftMaterialsResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCMonsterHunterGiftMaterialsResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCMonsterHunterGiftMaterialsResponse.EResponse]
        k_eInvalidGift: _ClassVar[CMsgClientToGCMonsterHunterGiftMaterialsResponse.EResponse]
        k_eNotEnoughMaterials: _ClassVar[CMsgClientToGCMonsterHunterGiftMaterialsResponse.EResponse]
        k_eInvalidRecipient: _ClassVar[CMsgClientToGCMonsterHunterGiftMaterialsResponse.EResponse]
        k_eNotEnoughPeriodicResource: _ClassVar[
            CMsgClientToGCMonsterHunterGiftMaterialsResponse.EResponse
        ]

    k_eInternalError: CMsgClientToGCMonsterHunterGiftMaterialsResponse.EResponse
    k_eSuccess: CMsgClientToGCMonsterHunterGiftMaterialsResponse.EResponse
    k_eTooBusy: CMsgClientToGCMonsterHunterGiftMaterialsResponse.EResponse
    k_eDisabled: CMsgClientToGCMonsterHunterGiftMaterialsResponse.EResponse
    k_eTimeout: CMsgClientToGCMonsterHunterGiftMaterialsResponse.EResponse
    k_eNotAllowed: CMsgClientToGCMonsterHunterGiftMaterialsResponse.EResponse
    k_eInvalidGift: CMsgClientToGCMonsterHunterGiftMaterialsResponse.EResponse
    k_eNotEnoughMaterials: CMsgClientToGCMonsterHunterGiftMaterialsResponse.EResponse
    k_eInvalidRecipient: CMsgClientToGCMonsterHunterGiftMaterialsResponse.EResponse
    k_eNotEnoughPeriodicResource: CMsgClientToGCMonsterHunterGiftMaterialsResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCMonsterHunterGiftMaterialsResponse.EResponse
    def __init__(
        self,
        response: CMsgClientToGCMonsterHunterGiftMaterialsResponse.EResponse | str | None = ...,
    ) -> None: ...

class CMsgClientToGCMonsterHunterRequestMaterialsNeededByFriend(_message.Message):
    __slots__ = ("friend_account_id",)
    FRIEND_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    friend_account_id: int
    def __init__(self, friend_account_id: int | None = ...) -> None: ...

class CMsgClientToGCMonsterHunterRequestMaterialsNeededByFriendResponse(_message.Message):
    __slots__ = ("response", "token_quantity")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[
            CMsgClientToGCMonsterHunterRequestMaterialsNeededByFriendResponse.EResponse
        ]
        k_eSuccess: _ClassVar[
            CMsgClientToGCMonsterHunterRequestMaterialsNeededByFriendResponse.EResponse
        ]
        k_eTooBusy: _ClassVar[
            CMsgClientToGCMonsterHunterRequestMaterialsNeededByFriendResponse.EResponse
        ]
        k_eDisabled: _ClassVar[
            CMsgClientToGCMonsterHunterRequestMaterialsNeededByFriendResponse.EResponse
        ]
        k_eTimeout: _ClassVar[
            CMsgClientToGCMonsterHunterRequestMaterialsNeededByFriendResponse.EResponse
        ]
        k_eNotAllowed: _ClassVar[
            CMsgClientToGCMonsterHunterRequestMaterialsNeededByFriendResponse.EResponse
        ]
        k_eInvalidFriend: _ClassVar[
            CMsgClientToGCMonsterHunterRequestMaterialsNeededByFriendResponse.EResponse
        ]
        k_eTooManyRequests: _ClassVar[
            CMsgClientToGCMonsterHunterRequestMaterialsNeededByFriendResponse.EResponse
        ]

    k_eInternalError: CMsgClientToGCMonsterHunterRequestMaterialsNeededByFriendResponse.EResponse
    k_eSuccess: CMsgClientToGCMonsterHunterRequestMaterialsNeededByFriendResponse.EResponse
    k_eTooBusy: CMsgClientToGCMonsterHunterRequestMaterialsNeededByFriendResponse.EResponse
    k_eDisabled: CMsgClientToGCMonsterHunterRequestMaterialsNeededByFriendResponse.EResponse
    k_eTimeout: CMsgClientToGCMonsterHunterRequestMaterialsNeededByFriendResponse.EResponse
    k_eNotAllowed: CMsgClientToGCMonsterHunterRequestMaterialsNeededByFriendResponse.EResponse
    k_eInvalidFriend: CMsgClientToGCMonsterHunterRequestMaterialsNeededByFriendResponse.EResponse
    k_eTooManyRequests: CMsgClientToGCMonsterHunterRequestMaterialsNeededByFriendResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    TOKEN_QUANTITY_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCMonsterHunterRequestMaterialsNeededByFriendResponse.EResponse
    token_quantity: _dota_shared_enums_pb2.CMsgMonsterHunterMaterialQuantity
    def __init__(
        self,
        response: CMsgClientToGCMonsterHunterRequestMaterialsNeededByFriendResponse.EResponse
        | str
        | None = ...,
        token_quantity: _dota_shared_enums_pb2.CMsgMonsterHunterMaterialQuantity
        | _Mapping
        | None = ...,
    ) -> None: ...

class CMsgClientToGCMonsterHunterDevResetAll(_message.Message):
    __slots__ = ("reset_codex_only",)
    RESET_CODEX_ONLY_FIELD_NUMBER: _ClassVar[int]
    reset_codex_only: bool
    def __init__(self, reset_codex_only: bool = ...) -> None: ...

class CMsgClientToGCMonsterHunterDevResetAllResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCMonsterHunterDevResetAllResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCMonsterHunterDevResetAllResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCMonsterHunterDevResetAllResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCMonsterHunterDevResetAllResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCMonsterHunterDevResetAllResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCMonsterHunterDevResetAllResponse.EResponse]

    k_eInternalError: CMsgClientToGCMonsterHunterDevResetAllResponse.EResponse
    k_eSuccess: CMsgClientToGCMonsterHunterDevResetAllResponse.EResponse
    k_eTooBusy: CMsgClientToGCMonsterHunterDevResetAllResponse.EResponse
    k_eDisabled: CMsgClientToGCMonsterHunterDevResetAllResponse.EResponse
    k_eTimeout: CMsgClientToGCMonsterHunterDevResetAllResponse.EResponse
    k_eNotAllowed: CMsgClientToGCMonsterHunterDevResetAllResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCMonsterHunterDevResetAllResponse.EResponse
    def __init__(
        self, response: CMsgClientToGCMonsterHunterDevResetAllResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCMonsterHunterDevGrantMaterials(_message.Message):
    __slots__ = ("material_quantity",)
    MATERIAL_QUANTITY_FIELD_NUMBER: _ClassVar[int]
    material_quantity: _dota_shared_enums_pb2.CMsgMonsterHunterMaterialQuantity
    def __init__(
        self,
        material_quantity: _dota_shared_enums_pb2.CMsgMonsterHunterMaterialQuantity
        | _Mapping
        | None = ...,
    ) -> None: ...

class CMsgClientToGCMonsterHunterDevGrantMaterialsResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCMonsterHunterDevGrantMaterialsResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCMonsterHunterDevGrantMaterialsResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCMonsterHunterDevGrantMaterialsResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCMonsterHunterDevGrantMaterialsResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCMonsterHunterDevGrantMaterialsResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCMonsterHunterDevGrantMaterialsResponse.EResponse]

    k_eInternalError: CMsgClientToGCMonsterHunterDevGrantMaterialsResponse.EResponse
    k_eSuccess: CMsgClientToGCMonsterHunterDevGrantMaterialsResponse.EResponse
    k_eTooBusy: CMsgClientToGCMonsterHunterDevGrantMaterialsResponse.EResponse
    k_eDisabled: CMsgClientToGCMonsterHunterDevGrantMaterialsResponse.EResponse
    k_eTimeout: CMsgClientToGCMonsterHunterDevGrantMaterialsResponse.EResponse
    k_eNotAllowed: CMsgClientToGCMonsterHunterDevGrantMaterialsResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCMonsterHunterDevGrantMaterialsResponse.EResponse
    def __init__(
        self,
        response: CMsgClientToGCMonsterHunterDevGrantMaterialsResponse.EResponse | str | None = ...,
    ) -> None: ...

class CMsgClientToGCMonsterHunterDevClearInventory(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCMonsterHunterDevClearInventoryResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCMonsterHunterDevClearInventoryResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCMonsterHunterDevClearInventoryResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCMonsterHunterDevClearInventoryResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCMonsterHunterDevClearInventoryResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCMonsterHunterDevClearInventoryResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCMonsterHunterDevClearInventoryResponse.EResponse]

    k_eInternalError: CMsgClientToGCMonsterHunterDevClearInventoryResponse.EResponse
    k_eSuccess: CMsgClientToGCMonsterHunterDevClearInventoryResponse.EResponse
    k_eTooBusy: CMsgClientToGCMonsterHunterDevClearInventoryResponse.EResponse
    k_eDisabled: CMsgClientToGCMonsterHunterDevClearInventoryResponse.EResponse
    k_eTimeout: CMsgClientToGCMonsterHunterDevClearInventoryResponse.EResponse
    k_eNotAllowed: CMsgClientToGCMonsterHunterDevClearInventoryResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCMonsterHunterDevClearInventoryResponse.EResponse
    def __init__(
        self,
        response: CMsgClientToGCMonsterHunterDevClearInventoryResponse.EResponse | str | None = ...,
    ) -> None: ...

class CMsgClientToGCMonsterHunterDevClaimInvestigationRewards(_message.Message):
    __slots__ = ("investigation_game_state", "win")
    INVESTIGATION_GAME_STATE_FIELD_NUMBER: _ClassVar[int]
    WIN_FIELD_NUMBER: _ClassVar[int]
    investigation_game_state: _dota_shared_enums_pb2.CMsgMonsterHunterInvestigationGameState
    win: bool
    def __init__(
        self,
        investigation_game_state: _dota_shared_enums_pb2.CMsgMonsterHunterInvestigationGameState
        | _Mapping
        | None = ...,
        win: bool = ...,
    ) -> None: ...

class CMsgClientToGCMonsterHunterDevClaimInvestigationRewardsResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[
            CMsgClientToGCMonsterHunterDevClaimInvestigationRewardsResponse.EResponse
        ]
        k_eSuccess: _ClassVar[
            CMsgClientToGCMonsterHunterDevClaimInvestigationRewardsResponse.EResponse
        ]
        k_eTooBusy: _ClassVar[
            CMsgClientToGCMonsterHunterDevClaimInvestigationRewardsResponse.EResponse
        ]
        k_eDisabled: _ClassVar[
            CMsgClientToGCMonsterHunterDevClaimInvestigationRewardsResponse.EResponse
        ]
        k_eTimeout: _ClassVar[
            CMsgClientToGCMonsterHunterDevClaimInvestigationRewardsResponse.EResponse
        ]
        k_eNotAllowed: _ClassVar[
            CMsgClientToGCMonsterHunterDevClaimInvestigationRewardsResponse.EResponse
        ]

    k_eInternalError: CMsgClientToGCMonsterHunterDevClaimInvestigationRewardsResponse.EResponse
    k_eSuccess: CMsgClientToGCMonsterHunterDevClaimInvestigationRewardsResponse.EResponse
    k_eTooBusy: CMsgClientToGCMonsterHunterDevClaimInvestigationRewardsResponse.EResponse
    k_eDisabled: CMsgClientToGCMonsterHunterDevClaimInvestigationRewardsResponse.EResponse
    k_eTimeout: CMsgClientToGCMonsterHunterDevClaimInvestigationRewardsResponse.EResponse
    k_eNotAllowed: CMsgClientToGCMonsterHunterDevClaimInvestigationRewardsResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCMonsterHunterDevClaimInvestigationRewardsResponse.EResponse
    def __init__(
        self,
        response: CMsgClientToGCMonsterHunterDevClaimInvestigationRewardsResponse.EResponse
        | str
        | None = ...,
    ) -> None: ...

class CMsgClientToGCMonsterHunterClaimCodexReward(_message.Message):
    __slots__ = ("codex_id", "reward")
    CODEX_ID_FIELD_NUMBER: _ClassVar[int]
    REWARD_FIELD_NUMBER: _ClassVar[int]
    codex_id: int
    reward: int
    def __init__(self, codex_id: int | None = ..., reward: int | None = ...) -> None: ...

class CMsgClientToGCMonsterHunterClaimCodexRewardResponse(_message.Message):
    __slots__ = ("response", "claim_response")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCMonsterHunterClaimCodexRewardResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCMonsterHunterClaimCodexRewardResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCMonsterHunterClaimCodexRewardResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCMonsterHunterClaimCodexRewardResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCMonsterHunterClaimCodexRewardResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCMonsterHunterClaimCodexRewardResponse.EResponse]
        k_eAlreadyClaimed: _ClassVar[CMsgClientToGCMonsterHunterClaimCodexRewardResponse.EResponse]

    k_eInternalError: CMsgClientToGCMonsterHunterClaimCodexRewardResponse.EResponse
    k_eSuccess: CMsgClientToGCMonsterHunterClaimCodexRewardResponse.EResponse
    k_eTooBusy: CMsgClientToGCMonsterHunterClaimCodexRewardResponse.EResponse
    k_eDisabled: CMsgClientToGCMonsterHunterClaimCodexRewardResponse.EResponse
    k_eTimeout: CMsgClientToGCMonsterHunterClaimCodexRewardResponse.EResponse
    k_eNotAllowed: CMsgClientToGCMonsterHunterClaimCodexRewardResponse.EResponse
    k_eAlreadyClaimed: CMsgClientToGCMonsterHunterClaimCodexRewardResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    CLAIM_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCMonsterHunterClaimCodexRewardResponse.EResponse
    claim_response: _dota_gcmessages_common_pb2.CMsgDOTAClaimEventActionResponse
    def __init__(
        self,
        response: CMsgClientToGCMonsterHunterClaimCodexRewardResponse.EResponse | str | None = ...,
        claim_response: _dota_gcmessages_common_pb2.CMsgDOTAClaimEventActionResponse
        | _Mapping
        | None = ...,
    ) -> None: ...

class CMsgDevModifyCodexAction(_message.Message):
    __slots__ = ("codex_id", "stat_type", "action")
    class EAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eClear: _ClassVar[CMsgDevModifyCodexAction.EAction]
        k_eAdd: _ClassVar[CMsgDevModifyCodexAction.EAction]

    k_eClear: CMsgDevModifyCodexAction.EAction
    k_eAdd: CMsgDevModifyCodexAction.EAction
    CODEX_ID_FIELD_NUMBER: _ClassVar[int]
    STAT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    codex_id: int
    stat_type: EHeroCodexEntryStatType
    action: CMsgDevModifyCodexAction.EAction
    def __init__(
        self,
        codex_id: int | None = ...,
        stat_type: EHeroCodexEntryStatType | str | None = ...,
        action: CMsgDevModifyCodexAction.EAction | str | None = ...,
    ) -> None: ...

class CMsgClientToGCMonsterHunterDevModifyHeroCodex(_message.Message):
    __slots__ = ("actions",)
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    actions: _containers.RepeatedCompositeFieldContainer[CMsgDevModifyCodexAction]
    def __init__(
        self, actions: _Iterable[CMsgDevModifyCodexAction | _Mapping] | None = ...
    ) -> None: ...

class CMsgClientToGCMonsterHunterDevModifyHeroCodexResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCMonsterHunterDevModifyHeroCodexResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCMonsterHunterDevModifyHeroCodexResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCMonsterHunterDevModifyHeroCodexResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCMonsterHunterDevModifyHeroCodexResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCMonsterHunterDevModifyHeroCodexResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCMonsterHunterDevModifyHeroCodexResponse.EResponse]

    k_eInternalError: CMsgClientToGCMonsterHunterDevModifyHeroCodexResponse.EResponse
    k_eSuccess: CMsgClientToGCMonsterHunterDevModifyHeroCodexResponse.EResponse
    k_eTooBusy: CMsgClientToGCMonsterHunterDevModifyHeroCodexResponse.EResponse
    k_eDisabled: CMsgClientToGCMonsterHunterDevModifyHeroCodexResponse.EResponse
    k_eTimeout: CMsgClientToGCMonsterHunterDevModifyHeroCodexResponse.EResponse
    k_eNotAllowed: CMsgClientToGCMonsterHunterDevModifyHeroCodexResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCMonsterHunterDevModifyHeroCodexResponse.EResponse
    def __init__(
        self,
        response: CMsgClientToGCMonsterHunterDevModifyHeroCodexResponse.EResponse
        | str
        | None = ...,
    ) -> None: ...

class CMsgClientToGCMonsterHunterFeedback(_message.Message):
    __slots__ = ("language", "feedback")
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    FEEDBACK_FIELD_NUMBER: _ClassVar[int]
    language: int
    feedback: str
    def __init__(self, language: int | None = ..., feedback: str | None = ...) -> None: ...

class CMsgClientToGCMonsterHunterFeedbackResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCMonsterHunterFeedbackResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCMonsterHunterFeedbackResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCMonsterHunterFeedbackResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCMonsterHunterFeedbackResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCMonsterHunterFeedbackResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCMonsterHunterFeedbackResponse.EResponse]

    k_eInternalError: CMsgClientToGCMonsterHunterFeedbackResponse.EResponse
    k_eSuccess: CMsgClientToGCMonsterHunterFeedbackResponse.EResponse
    k_eTooBusy: CMsgClientToGCMonsterHunterFeedbackResponse.EResponse
    k_eDisabled: CMsgClientToGCMonsterHunterFeedbackResponse.EResponse
    k_eTimeout: CMsgClientToGCMonsterHunterFeedbackResponse.EResponse
    k_eNotAllowed: CMsgClientToGCMonsterHunterFeedbackResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCMonsterHunterFeedbackResponse.EResponse
    def __init__(
        self, response: CMsgClientToGCMonsterHunterFeedbackResponse.EResponse | str | None = ...
    ) -> None: ...
