from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

import dota_shared_enums_pb2 as _dota_shared_enums_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class ECandyShopAuditAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_ECandyShopAuditAction_Invalid: _ClassVar[ECandyShopAuditAction]
    k_ECandyShopAuditAction_SupportModify: _ClassVar[ECandyShopAuditAction]
    k_ECandyShopAuditAction_PurchaseReward: _ClassVar[ECandyShopAuditAction]
    k_ECandyShopAuditAction_OpenBags: _ClassVar[ECandyShopAuditAction]
    k_ECandyShopAuditAction_RerollRewards: _ClassVar[ECandyShopAuditAction]
    k_ECandyShopAuditAction_DoVariableExchange: _ClassVar[ECandyShopAuditAction]
    k_ECandyShopAuditAction_DoExchange: _ClassVar[ECandyShopAuditAction]
    k_ECandyShopAuditAction_DEPRECATED_EventActionGrantInventorySizeIncrease: _ClassVar[
        ECandyShopAuditAction
    ]
    k_ECandyShopAuditAction_EventActionGrantRerollChargesIncrease: _ClassVar[ECandyShopAuditAction]
    k_ECandyShopAuditAction_EventActionGrantUpgrade_InventorySize: _ClassVar[ECandyShopAuditAction]
    k_ECandyShopAuditAction_EventActionGrantUpgrade_RewardShelf: _ClassVar[ECandyShopAuditAction]
    k_ECandyShopAuditAction_EventActionGrantUpgrade_ExtraExchangeRecipe: _ClassVar[
        ECandyShopAuditAction
    ]

class ECandyShopRewardType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eCandyShopRewardType_None: _ClassVar[ECandyShopRewardType]
    k_eCandyShopRewardType_Item: _ClassVar[ECandyShopRewardType]
    k_eCandyShopRewardType_EventAction: _ClassVar[ECandyShopRewardType]
    k_eCandyShopRewardType_EventPoints: _ClassVar[ECandyShopRewardType]

k_ECandyShopAuditAction_Invalid: ECandyShopAuditAction
k_ECandyShopAuditAction_SupportModify: ECandyShopAuditAction
k_ECandyShopAuditAction_PurchaseReward: ECandyShopAuditAction
k_ECandyShopAuditAction_OpenBags: ECandyShopAuditAction
k_ECandyShopAuditAction_RerollRewards: ECandyShopAuditAction
k_ECandyShopAuditAction_DoVariableExchange: ECandyShopAuditAction
k_ECandyShopAuditAction_DoExchange: ECandyShopAuditAction
k_ECandyShopAuditAction_DEPRECATED_EventActionGrantInventorySizeIncrease: ECandyShopAuditAction
k_ECandyShopAuditAction_EventActionGrantRerollChargesIncrease: ECandyShopAuditAction
k_ECandyShopAuditAction_EventActionGrantUpgrade_InventorySize: ECandyShopAuditAction
k_ECandyShopAuditAction_EventActionGrantUpgrade_RewardShelf: ECandyShopAuditAction
k_ECandyShopAuditAction_EventActionGrantUpgrade_ExtraExchangeRecipe: ECandyShopAuditAction
k_eCandyShopRewardType_None: ECandyShopRewardType
k_eCandyShopRewardType_Item: ECandyShopRewardType
k_eCandyShopRewardType_EventAction: ECandyShopRewardType
k_eCandyShopRewardType_EventPoints: ECandyShopRewardType

class CMsgCandyShopCandyCount(_message.Message):
    __slots__ = ("candy_type", "candy_count")
    CANDY_TYPE_FIELD_NUMBER: _ClassVar[int]
    CANDY_COUNT_FIELD_NUMBER: _ClassVar[int]
    candy_type: int
    candy_count: int
    def __init__(self, candy_type: int | None = ..., candy_count: int | None = ...) -> None: ...

class CMsgCandyShopCandyQuantity(_message.Message):
    __slots__ = ("candy_counts",)
    CANDY_COUNTS_FIELD_NUMBER: _ClassVar[int]
    candy_counts: _containers.RepeatedCompositeFieldContainer[CMsgCandyShopCandyCount]
    def __init__(
        self, candy_counts: _Iterable[CMsgCandyShopCandyCount | _Mapping] | None = ...
    ) -> None: ...

class CMsgCandyShopExchangeRecipe(_message.Message):
    __slots__ = ("recipe_id", "input", "output")
    RECIPE_ID_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    recipe_id: int
    input: CMsgCandyShopCandyQuantity
    output: CMsgCandyShopCandyQuantity
    def __init__(
        self,
        recipe_id: int | None = ...,
        input: CMsgCandyShopCandyQuantity | _Mapping | None = ...,
        output: CMsgCandyShopCandyQuantity | _Mapping | None = ...,
    ) -> None: ...

class CMsgCandyShopRewardData_Item(_message.Message):
    __slots__ = ("item_def",)
    ITEM_DEF_FIELD_NUMBER: _ClassVar[int]
    item_def: int
    def __init__(self, item_def: int | None = ...) -> None: ...

class CMsgCandyShopRewardData_EventAction(_message.Message):
    __slots__ = ("event_id", "action_id")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: _dota_shared_enums_pb2.EEvent
    action_id: int
    def __init__(
        self,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
        action_id: int | None = ...,
    ) -> None: ...

class CMsgCandyShopRewardData_EventPoints(_message.Message):
    __slots__ = ("event_id", "points")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    event_id: _dota_shared_enums_pb2.EEvent
    points: int
    def __init__(
        self, event_id: _dota_shared_enums_pb2.EEvent | str | None = ..., points: int | None = ...
    ) -> None: ...

class CMsgCandyShopReward(_message.Message):
    __slots__ = (
        "reward_id",
        "reward_option_id",
        "price",
        "reward_type",
        "item_data",
        "event_action_data",
        "event_points_data",
    )
    REWARD_ID_FIELD_NUMBER: _ClassVar[int]
    REWARD_OPTION_ID_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    REWARD_TYPE_FIELD_NUMBER: _ClassVar[int]
    ITEM_DATA_FIELD_NUMBER: _ClassVar[int]
    EVENT_ACTION_DATA_FIELD_NUMBER: _ClassVar[int]
    EVENT_POINTS_DATA_FIELD_NUMBER: _ClassVar[int]
    reward_id: int
    reward_option_id: int
    price: CMsgCandyShopCandyQuantity
    reward_type: ECandyShopRewardType
    item_data: CMsgCandyShopRewardData_Item
    event_action_data: CMsgCandyShopRewardData_EventAction
    event_points_data: CMsgCandyShopRewardData_EventPoints
    def __init__(
        self,
        reward_id: int | None = ...,
        reward_option_id: int | None = ...,
        price: CMsgCandyShopCandyQuantity | _Mapping | None = ...,
        reward_type: ECandyShopRewardType | str | None = ...,
        item_data: CMsgCandyShopRewardData_Item | _Mapping | None = ...,
        event_action_data: CMsgCandyShopRewardData_EventAction | _Mapping | None = ...,
        event_points_data: CMsgCandyShopRewardData_EventPoints | _Mapping | None = ...,
    ) -> None: ...

class CMsgCandyShopUserData(_message.Message):
    __slots__ = (
        "inventory_max",
        "inventory",
        "exchange_recipe_max",
        "exchange_reset_timestamp",
        "exchange_recipes",
        "active_reward_max",
        "active_rewards",
        "reroll_charges_max",
        "reroll_charges",
    )
    INVENTORY_MAX_FIELD_NUMBER: _ClassVar[int]
    INVENTORY_FIELD_NUMBER: _ClassVar[int]
    EXCHANGE_RECIPE_MAX_FIELD_NUMBER: _ClassVar[int]
    EXCHANGE_RESET_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    EXCHANGE_RECIPES_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_REWARD_MAX_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_REWARDS_FIELD_NUMBER: _ClassVar[int]
    REROLL_CHARGES_MAX_FIELD_NUMBER: _ClassVar[int]
    REROLL_CHARGES_FIELD_NUMBER: _ClassVar[int]
    inventory_max: int
    inventory: CMsgCandyShopCandyQuantity
    exchange_recipe_max: int
    exchange_reset_timestamp: int
    exchange_recipes: _containers.RepeatedCompositeFieldContainer[CMsgCandyShopExchangeRecipe]
    active_reward_max: int
    active_rewards: _containers.RepeatedCompositeFieldContainer[CMsgCandyShopReward]
    reroll_charges_max: int
    reroll_charges: int
    def __init__(
        self,
        inventory_max: int | None = ...,
        inventory: CMsgCandyShopCandyQuantity | _Mapping | None = ...,
        exchange_recipe_max: int | None = ...,
        exchange_reset_timestamp: int | None = ...,
        exchange_recipes: _Iterable[CMsgCandyShopExchangeRecipe | _Mapping] | None = ...,
        active_reward_max: int | None = ...,
        active_rewards: _Iterable[CMsgCandyShopReward | _Mapping] | None = ...,
        reroll_charges_max: int | None = ...,
        reroll_charges: int | None = ...,
    ) -> None: ...

class CMsgClientToGCCandyShopGetUserData(_message.Message):
    __slots__ = ("candy_shop_id",)
    CANDY_SHOP_ID_FIELD_NUMBER: _ClassVar[int]
    candy_shop_id: int
    def __init__(self, candy_shop_id: int | None = ...) -> None: ...

class CMsgClientToGCCandyShopGetUserDataResponse(_message.Message):
    __slots__ = ("response", "user_data")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCCandyShopGetUserDataResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCCandyShopGetUserDataResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCCandyShopGetUserDataResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCCandyShopGetUserDataResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCCandyShopGetUserDataResponse.EResponse]
        k_eInvalidShop: _ClassVar[CMsgClientToGCCandyShopGetUserDataResponse.EResponse]
        k_eExpiredShop: _ClassVar[CMsgClientToGCCandyShopGetUserDataResponse.EResponse]

    k_eInternalError: CMsgClientToGCCandyShopGetUserDataResponse.EResponse
    k_eSuccess: CMsgClientToGCCandyShopGetUserDataResponse.EResponse
    k_eTooBusy: CMsgClientToGCCandyShopGetUserDataResponse.EResponse
    k_eDisabled: CMsgClientToGCCandyShopGetUserDataResponse.EResponse
    k_eTimeout: CMsgClientToGCCandyShopGetUserDataResponse.EResponse
    k_eInvalidShop: CMsgClientToGCCandyShopGetUserDataResponse.EResponse
    k_eExpiredShop: CMsgClientToGCCandyShopGetUserDataResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    USER_DATA_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCCandyShopGetUserDataResponse.EResponse
    user_data: CMsgCandyShopUserData
    def __init__(
        self,
        response: CMsgClientToGCCandyShopGetUserDataResponse.EResponse | str | None = ...,
        user_data: CMsgCandyShopUserData | _Mapping | None = ...,
    ) -> None: ...

class CMsgGCToClientCandyShopUserDataUpdated(_message.Message):
    __slots__ = ("candy_shop_id", "user_data")
    CANDY_SHOP_ID_FIELD_NUMBER: _ClassVar[int]
    USER_DATA_FIELD_NUMBER: _ClassVar[int]
    candy_shop_id: int
    user_data: CMsgCandyShopUserData
    def __init__(
        self,
        candy_shop_id: int | None = ...,
        user_data: CMsgCandyShopUserData | _Mapping | None = ...,
    ) -> None: ...

class CMsgClientToGCCandyShopPurchaseReward(_message.Message):
    __slots__ = ("candy_shop_id", "reward_id")
    CANDY_SHOP_ID_FIELD_NUMBER: _ClassVar[int]
    REWARD_ID_FIELD_NUMBER: _ClassVar[int]
    candy_shop_id: int
    reward_id: int
    def __init__(self, candy_shop_id: int | None = ..., reward_id: int | None = ...) -> None: ...

class CMsgClientToGCCandyShopPurchaseRewardResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCCandyShopPurchaseRewardResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCCandyShopPurchaseRewardResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCCandyShopPurchaseRewardResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCCandyShopPurchaseRewardResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCCandyShopPurchaseRewardResponse.EResponse]
        k_eInvalidShop: _ClassVar[CMsgClientToGCCandyShopPurchaseRewardResponse.EResponse]
        k_eInvalidReward: _ClassVar[CMsgClientToGCCandyShopPurchaseRewardResponse.EResponse]
        k_eNotEnoughCandy: _ClassVar[CMsgClientToGCCandyShopPurchaseRewardResponse.EResponse]
        k_eExpiredShop: _ClassVar[CMsgClientToGCCandyShopPurchaseRewardResponse.EResponse]

    k_eInternalError: CMsgClientToGCCandyShopPurchaseRewardResponse.EResponse
    k_eSuccess: CMsgClientToGCCandyShopPurchaseRewardResponse.EResponse
    k_eTooBusy: CMsgClientToGCCandyShopPurchaseRewardResponse.EResponse
    k_eDisabled: CMsgClientToGCCandyShopPurchaseRewardResponse.EResponse
    k_eTimeout: CMsgClientToGCCandyShopPurchaseRewardResponse.EResponse
    k_eInvalidShop: CMsgClientToGCCandyShopPurchaseRewardResponse.EResponse
    k_eInvalidReward: CMsgClientToGCCandyShopPurchaseRewardResponse.EResponse
    k_eNotEnoughCandy: CMsgClientToGCCandyShopPurchaseRewardResponse.EResponse
    k_eExpiredShop: CMsgClientToGCCandyShopPurchaseRewardResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCCandyShopPurchaseRewardResponse.EResponse
    def __init__(
        self, response: CMsgClientToGCCandyShopPurchaseRewardResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCCandyShopOpenBags(_message.Message):
    __slots__ = ("candy_shop_id", "bag_count")
    CANDY_SHOP_ID_FIELD_NUMBER: _ClassVar[int]
    BAG_COUNT_FIELD_NUMBER: _ClassVar[int]
    candy_shop_id: int
    bag_count: int
    def __init__(self, candy_shop_id: int | None = ..., bag_count: int | None = ...) -> None: ...

class CMsgClientToGCCandyShopOpenBagsResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCCandyShopOpenBagsResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCCandyShopOpenBagsResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCCandyShopOpenBagsResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCCandyShopOpenBagsResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCCandyShopOpenBagsResponse.EResponse]
        k_eInvalidShop: _ClassVar[CMsgClientToGCCandyShopOpenBagsResponse.EResponse]
        k_eInvalidItem: _ClassVar[CMsgClientToGCCandyShopOpenBagsResponse.EResponse]
        k_eNotEnoughBags: _ClassVar[CMsgClientToGCCandyShopOpenBagsResponse.EResponse]
        k_eNotEnoughSpace: _ClassVar[CMsgClientToGCCandyShopOpenBagsResponse.EResponse]
        k_eExpiredShop: _ClassVar[CMsgClientToGCCandyShopOpenBagsResponse.EResponse]

    k_eInternalError: CMsgClientToGCCandyShopOpenBagsResponse.EResponse
    k_eSuccess: CMsgClientToGCCandyShopOpenBagsResponse.EResponse
    k_eTooBusy: CMsgClientToGCCandyShopOpenBagsResponse.EResponse
    k_eDisabled: CMsgClientToGCCandyShopOpenBagsResponse.EResponse
    k_eTimeout: CMsgClientToGCCandyShopOpenBagsResponse.EResponse
    k_eInvalidShop: CMsgClientToGCCandyShopOpenBagsResponse.EResponse
    k_eInvalidItem: CMsgClientToGCCandyShopOpenBagsResponse.EResponse
    k_eNotEnoughBags: CMsgClientToGCCandyShopOpenBagsResponse.EResponse
    k_eNotEnoughSpace: CMsgClientToGCCandyShopOpenBagsResponse.EResponse
    k_eExpiredShop: CMsgClientToGCCandyShopOpenBagsResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCCandyShopOpenBagsResponse.EResponse
    def __init__(
        self, response: CMsgClientToGCCandyShopOpenBagsResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCCandyShopDoExchange(_message.Message):
    __slots__ = ("candy_shop_id", "recipe_id")
    CANDY_SHOP_ID_FIELD_NUMBER: _ClassVar[int]
    RECIPE_ID_FIELD_NUMBER: _ClassVar[int]
    candy_shop_id: int
    recipe_id: int
    def __init__(self, candy_shop_id: int | None = ..., recipe_id: int | None = ...) -> None: ...

class CMsgClientToGCCandyShopDoExchangeResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCCandyShopDoExchangeResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCCandyShopDoExchangeResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCCandyShopDoExchangeResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCCandyShopDoExchangeResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCCandyShopDoExchangeResponse.EResponse]
        k_eInvalidShop: _ClassVar[CMsgClientToGCCandyShopDoExchangeResponse.EResponse]
        k_eNotEnoughCandy: _ClassVar[CMsgClientToGCCandyShopDoExchangeResponse.EResponse]
        k_eInvalidRecipe: _ClassVar[CMsgClientToGCCandyShopDoExchangeResponse.EResponse]
        k_eNotEnoughSpace: _ClassVar[CMsgClientToGCCandyShopDoExchangeResponse.EResponse]
        k_eExpiredShop: _ClassVar[CMsgClientToGCCandyShopDoExchangeResponse.EResponse]

    k_eInternalError: CMsgClientToGCCandyShopDoExchangeResponse.EResponse
    k_eSuccess: CMsgClientToGCCandyShopDoExchangeResponse.EResponse
    k_eTooBusy: CMsgClientToGCCandyShopDoExchangeResponse.EResponse
    k_eDisabled: CMsgClientToGCCandyShopDoExchangeResponse.EResponse
    k_eTimeout: CMsgClientToGCCandyShopDoExchangeResponse.EResponse
    k_eInvalidShop: CMsgClientToGCCandyShopDoExchangeResponse.EResponse
    k_eNotEnoughCandy: CMsgClientToGCCandyShopDoExchangeResponse.EResponse
    k_eInvalidRecipe: CMsgClientToGCCandyShopDoExchangeResponse.EResponse
    k_eNotEnoughSpace: CMsgClientToGCCandyShopDoExchangeResponse.EResponse
    k_eExpiredShop: CMsgClientToGCCandyShopDoExchangeResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCCandyShopDoExchangeResponse.EResponse
    def __init__(
        self, response: CMsgClientToGCCandyShopDoExchangeResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCCandyShopDoVariableExchange(_message.Message):
    __slots__ = ("candy_shop_id", "input", "output")
    CANDY_SHOP_ID_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    candy_shop_id: int
    input: CMsgCandyShopCandyQuantity
    output: CMsgCandyShopCandyQuantity
    def __init__(
        self,
        candy_shop_id: int | None = ...,
        input: CMsgCandyShopCandyQuantity | _Mapping | None = ...,
        output: CMsgCandyShopCandyQuantity | _Mapping | None = ...,
    ) -> None: ...

class CMsgClientToGCCandyShopDoVariableExchangeResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCCandyShopDoVariableExchangeResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCCandyShopDoVariableExchangeResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCCandyShopDoVariableExchangeResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCCandyShopDoVariableExchangeResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCCandyShopDoVariableExchangeResponse.EResponse]
        k_eInvalidShop: _ClassVar[CMsgClientToGCCandyShopDoVariableExchangeResponse.EResponse]
        k_eNotEnoughCandy: _ClassVar[CMsgClientToGCCandyShopDoVariableExchangeResponse.EResponse]
        k_eInvalidRecipe: _ClassVar[CMsgClientToGCCandyShopDoVariableExchangeResponse.EResponse]
        k_eNotEnoughSpace: _ClassVar[CMsgClientToGCCandyShopDoVariableExchangeResponse.EResponse]
        k_eExpiredShop: _ClassVar[CMsgClientToGCCandyShopDoVariableExchangeResponse.EResponse]

    k_eInternalError: CMsgClientToGCCandyShopDoVariableExchangeResponse.EResponse
    k_eSuccess: CMsgClientToGCCandyShopDoVariableExchangeResponse.EResponse
    k_eTooBusy: CMsgClientToGCCandyShopDoVariableExchangeResponse.EResponse
    k_eDisabled: CMsgClientToGCCandyShopDoVariableExchangeResponse.EResponse
    k_eTimeout: CMsgClientToGCCandyShopDoVariableExchangeResponse.EResponse
    k_eInvalidShop: CMsgClientToGCCandyShopDoVariableExchangeResponse.EResponse
    k_eNotEnoughCandy: CMsgClientToGCCandyShopDoVariableExchangeResponse.EResponse
    k_eInvalidRecipe: CMsgClientToGCCandyShopDoVariableExchangeResponse.EResponse
    k_eNotEnoughSpace: CMsgClientToGCCandyShopDoVariableExchangeResponse.EResponse
    k_eExpiredShop: CMsgClientToGCCandyShopDoVariableExchangeResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCCandyShopDoVariableExchangeResponse.EResponse
    def __init__(
        self,
        response: CMsgClientToGCCandyShopDoVariableExchangeResponse.EResponse | str | None = ...,
    ) -> None: ...

class CMsgClientToGCCandyShopRerollRewards(_message.Message):
    __slots__ = ("candy_shop_id",)
    CANDY_SHOP_ID_FIELD_NUMBER: _ClassVar[int]
    candy_shop_id: int
    def __init__(self, candy_shop_id: int | None = ...) -> None: ...

class CMsgClientToGCCandyShopRerollRewardsResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCCandyShopRerollRewardsResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCCandyShopRerollRewardsResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCCandyShopRerollRewardsResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCCandyShopRerollRewardsResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCCandyShopRerollRewardsResponse.EResponse]
        k_eInvalidShop: _ClassVar[CMsgClientToGCCandyShopRerollRewardsResponse.EResponse]
        k_eNoRerollCharges: _ClassVar[CMsgClientToGCCandyShopRerollRewardsResponse.EResponse]
        k_eExpiredShop: _ClassVar[CMsgClientToGCCandyShopRerollRewardsResponse.EResponse]
        k_eShopNotOpen: _ClassVar[CMsgClientToGCCandyShopRerollRewardsResponse.EResponse]

    k_eInternalError: CMsgClientToGCCandyShopRerollRewardsResponse.EResponse
    k_eSuccess: CMsgClientToGCCandyShopRerollRewardsResponse.EResponse
    k_eTooBusy: CMsgClientToGCCandyShopRerollRewardsResponse.EResponse
    k_eDisabled: CMsgClientToGCCandyShopRerollRewardsResponse.EResponse
    k_eTimeout: CMsgClientToGCCandyShopRerollRewardsResponse.EResponse
    k_eInvalidShop: CMsgClientToGCCandyShopRerollRewardsResponse.EResponse
    k_eNoRerollCharges: CMsgClientToGCCandyShopRerollRewardsResponse.EResponse
    k_eExpiredShop: CMsgClientToGCCandyShopRerollRewardsResponse.EResponse
    k_eShopNotOpen: CMsgClientToGCCandyShopRerollRewardsResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCCandyShopRerollRewardsResponse.EResponse
    def __init__(
        self, response: CMsgClientToGCCandyShopRerollRewardsResponse.EResponse | str | None = ...
    ) -> None: ...

class CCandyShopDev(_message.Message):
    __slots__ = ()
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CCandyShopDev.EResponse]
        k_eSuccess: _ClassVar[CCandyShopDev.EResponse]
        k_eTooBusy: _ClassVar[CCandyShopDev.EResponse]
        k_eDisabled: _ClassVar[CCandyShopDev.EResponse]
        k_eTimeout: _ClassVar[CCandyShopDev.EResponse]
        k_eNotAllowed: _ClassVar[CCandyShopDev.EResponse]
        k_eInvalidShop: _ClassVar[CCandyShopDev.EResponse]
        k_eNotEnoughSpace: _ClassVar[CCandyShopDev.EResponse]

    k_eInternalError: CCandyShopDev.EResponse
    k_eSuccess: CCandyShopDev.EResponse
    k_eTooBusy: CCandyShopDev.EResponse
    k_eDisabled: CCandyShopDev.EResponse
    k_eTimeout: CCandyShopDev.EResponse
    k_eNotAllowed: CCandyShopDev.EResponse
    k_eInvalidShop: CCandyShopDev.EResponse
    k_eNotEnoughSpace: CCandyShopDev.EResponse
    def __init__(self) -> None: ...

class CMsgClientToGCCandyShopDevGrantCandy(_message.Message):
    __slots__ = ("candy_shop_id", "candy_quantity")
    CANDY_SHOP_ID_FIELD_NUMBER: _ClassVar[int]
    CANDY_QUANTITY_FIELD_NUMBER: _ClassVar[int]
    candy_shop_id: int
    candy_quantity: CMsgCandyShopCandyQuantity
    def __init__(
        self,
        candy_shop_id: int | None = ...,
        candy_quantity: CMsgCandyShopCandyQuantity | _Mapping | None = ...,
    ) -> None: ...

class CMsgClientToGCCandyShopDevGrantCandyResponse(_message.Message):
    __slots__ = ("response",)
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CCandyShopDev.EResponse
    def __init__(self, response: CCandyShopDev.EResponse | str | None = ...) -> None: ...

class CMsgClientToGCCandyShopDevClearInventory(_message.Message):
    __slots__ = ("candy_shop_id",)
    CANDY_SHOP_ID_FIELD_NUMBER: _ClassVar[int]
    candy_shop_id: int
    def __init__(self, candy_shop_id: int | None = ...) -> None: ...

class CMsgClientToGCCandyShopDevClearInventoryResponse(_message.Message):
    __slots__ = ("response",)
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CCandyShopDev.EResponse
    def __init__(self, response: CCandyShopDev.EResponse | str | None = ...) -> None: ...

class CMsgClientToGCCandyShopDevGrantCandyBags(_message.Message):
    __slots__ = ("candy_shop_id", "quantity")
    CANDY_SHOP_ID_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    candy_shop_id: int
    quantity: int
    def __init__(self, candy_shop_id: int | None = ..., quantity: int | None = ...) -> None: ...

class CMsgClientToGCCandyShopDevGrantCandyBagsResponse(_message.Message):
    __slots__ = ("response",)
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CCandyShopDev.EResponse
    def __init__(self, response: CCandyShopDev.EResponse | str | None = ...) -> None: ...

class CMsgClientToGCCandyShopDevShuffleExchange(_message.Message):
    __slots__ = ("candy_shop_id",)
    CANDY_SHOP_ID_FIELD_NUMBER: _ClassVar[int]
    candy_shop_id: int
    def __init__(self, candy_shop_id: int | None = ...) -> None: ...

class CMsgClientToGCCandyShopDevShuffleExchangeResponse(_message.Message):
    __slots__ = ("response",)
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CCandyShopDev.EResponse
    def __init__(self, response: CCandyShopDev.EResponse | str | None = ...) -> None: ...

class CMsgClientToGCCandyShopDevGrantRerollCharges(_message.Message):
    __slots__ = ("candy_shop_id", "reroll_charges")
    CANDY_SHOP_ID_FIELD_NUMBER: _ClassVar[int]
    REROLL_CHARGES_FIELD_NUMBER: _ClassVar[int]
    candy_shop_id: int
    reroll_charges: int
    def __init__(
        self, candy_shop_id: int | None = ..., reroll_charges: int | None = ...
    ) -> None: ...

class CMsgClientToGCCandyShopDevGrantRerollChargesResponse(_message.Message):
    __slots__ = ("response",)
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CCandyShopDev.EResponse
    def __init__(self, response: CCandyShopDev.EResponse | str | None = ...) -> None: ...

class CMsgClientToGCCandyShopDevResetShop(_message.Message):
    __slots__ = ("candy_shop_id",)
    CANDY_SHOP_ID_FIELD_NUMBER: _ClassVar[int]
    candy_shop_id: int
    def __init__(self, candy_shop_id: int | None = ...) -> None: ...

class CMsgClientToGCCandyShopDevResetShopResponse(_message.Message):
    __slots__ = ("response",)
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CCandyShopDev.EResponse
    def __init__(self, response: CCandyShopDev.EResponse | str | None = ...) -> None: ...
