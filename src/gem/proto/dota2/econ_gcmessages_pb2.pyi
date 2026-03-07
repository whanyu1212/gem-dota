from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

import base_gcmessages_pb2 as _base_gcmessages_pb2
import econ_shared_enums_pb2 as _econ_shared_enums_pb2
import gcsdk_gcmessages_pb2 as _gcsdk_gcmessages_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class EGCItemMsg(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EMsgGCBase: _ClassVar[EGCItemMsg]
    k_EMsgGCSetItemPosition: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCPackBundle: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCPackBundleResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCDelete: _ClassVar[EGCItemMsg]
    k_EMsgGCVerifyCacheSubscription: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCNameItem: _ClassVar[EGCItemMsg]
    k_EMsgGCPaintItem: _ClassVar[EGCItemMsg]
    k_EMsgGCPaintItemResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCNameBaseItem: _ClassVar[EGCItemMsg]
    k_EMsgGCNameBaseItemResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCUseItemRequest: _ClassVar[EGCItemMsg]
    k_EMsgGCUseItemResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCGiftedItems: _ClassVar[EGCItemMsg]
    k_EMsgGCUnwrapGiftRequest: _ClassVar[EGCItemMsg]
    k_EMsgGCUnwrapGiftResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCSortItems: _ClassVar[EGCItemMsg]
    k_EMsgGCBackpackSortFinished: _ClassVar[EGCItemMsg]
    k_EMsgGCAdjustItemEquippedState: _ClassVar[EGCItemMsg]
    k_EMsgGCItemAcknowledged: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCNameItemResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCApplyStrangePart: _ClassVar[EGCItemMsg]
    k_EMsgGCApplyPennantUpgrade: _ClassVar[EGCItemMsg]
    k_EMsgGCSetItemPositions: _ClassVar[EGCItemMsg]
    k_EMsgGCApplyEggEssence: _ClassVar[EGCItemMsg]
    k_EMsgGCNameEggEssenceResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCExtractGems: _ClassVar[EGCItemMsg]
    k_EMsgGCAddSocket: _ClassVar[EGCItemMsg]
    k_EMsgGCAddItemToSocket: _ClassVar[EGCItemMsg]
    k_EMsgGCAddItemToSocketResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCAddSocketResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCResetStrangeGemCount: _ClassVar[EGCItemMsg]
    k_EMsgGCRequestCrateItems: _ClassVar[EGCItemMsg]
    k_EMsgGCRequestCrateItemsResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCExtractGemsResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCResetStrangeGemCountResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCServerUseItemRequest: _ClassVar[EGCItemMsg]
    k_EMsgGCAddGiftItem: _ClassVar[EGCItemMsg]
    k_EMsgSQLGCToGCRevokeUntrustedGift: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCRemoveItemGifterAttributes: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCRemoveItemName: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCRemoveItemDescription: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCRemoveItemAttributeResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCDev_NewItemRequest: _ClassVar[EGCItemMsg]
    k_EMsgGCDev_NewItemRequestResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCDev_UnlockAllItemStylesRequest: _ClassVar[EGCItemMsg]
    k_EMsgGCDev_UnlockAllItemStylesResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCStorePurchaseFinalize: _ClassVar[EGCItemMsg]
    k_EMsgGCStorePurchaseFinalizeResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCStorePurchaseCancel: _ClassVar[EGCItemMsg]
    k_EMsgGCStorePurchaseCancelResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCStorePurchaseInit: _ClassVar[EGCItemMsg]
    k_EMsgGCStorePurchaseInitResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCBannedWordListUpdated: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCDirtySDOCache: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCUpdateSQLKeyValue: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCBroadcastConsoleCommand: _ClassVar[EGCItemMsg]
    k_EMsgGCServerVersionUpdated: _ClassVar[EGCItemMsg]
    k_EMsgGCApplyAutograph: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCWebAPIAccountChanged: _ClassVar[EGCItemMsg]
    k_EMsgGCClientVersionUpdated: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCUpdateWelcomeMsg: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCPlayerStrangeCountAdjustments: _ClassVar[EGCItemMsg]
    k_EMsgGCRequestStoreSalesData: _ClassVar[EGCItemMsg]
    k_EMsgGCRequestStoreSalesDataResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCRequestStoreSalesDataUpToDateResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCPingRequest: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCPingResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCGetUserSessionServer: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCGetUserSessionServerResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCGetUserServerMembers: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCGetUserServerMembersResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCCanUseDropRateBonus: _ClassVar[EGCItemMsg]
    k_EMsgSQLAddDropRateBonus: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCRefreshSOCache: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCGrantAccountRolledItems: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCGrantSelfMadeItemToAccount: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCUnlockCrate: _ClassVar[EGCItemMsg]
    k_EMsgGCStatueCraft: _ClassVar[EGCItemMsg]
    k_EMsgGCRedeemCode: _ClassVar[EGCItemMsg]
    k_EMsgGCRedeemCodeResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCItemConsumptionRollback: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCWrapAndDeliverGift: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCWrapAndDeliverGiftResponse: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCUnpackBundleResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCToClientStoreTransactionCompleted: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCEquipItems: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCEquipItemsResponse: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCUnlockItemStyle: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCUnlockItemStyleResponse: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCSetItemInventoryCategory: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCUnlockCrate: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCUnlockCrateResponse: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCUnpackBundle: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCSetItemStyle: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCSetItemStyleResponse: _ClassVar[EGCItemMsg]
    k_EMsgSQLGCToGCGrantBackpackSlots: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCLookupAccountName: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCLookupAccountNameResponse: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCCreateStaticRecipe: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCCreateStaticRecipeResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCStoreProcessCDKeyTransaction: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCStoreProcessCDKeyTransactionResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCStoreProcessSettlement: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCStoreProcessSettlementResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCConsoleOutput: _ClassVar[EGCItemMsg]
    k_EMsgGCToClientItemAges: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCInternalTestMsg: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCClientServerVersionsUpdated: _ClassVar[EGCItemMsg]
    k_EMsgGCUseMultipleItemsRequest: _ClassVar[EGCItemMsg]
    k_EMsgGCGetAccountSubscriptionItem: _ClassVar[EGCItemMsg]
    k_EMsgGCGetAccountSubscriptionItemResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCBroadcastMessageFromSub: _ClassVar[EGCItemMsg]
    k_EMsgGCToClientCurrencyPricePoints: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCAddSubscriptionTime: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCFlushSteamInventoryCache: _ClassVar[EGCItemMsg]
    k_EMsgGCRequestCrateEscalationLevel: _ClassVar[EGCItemMsg]
    k_EMsgGCRequestCrateEscalationLevelResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCUpdateSubscriptionItems: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCSelfPing: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCGetInfuxIntervalStats: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCGetInfuxIntervalStatsResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCPurchaseSucceeded: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCGetLimitedItemPurchaseQuantity: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCGetLimitedItemPurchaseQuantityResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCToGCBetaDeleteItems: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCGetInFlightItemCharges: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCGetInFlightItemChargesResponse: _ClassVar[EGCItemMsg]
    k_EMsgGCToClientInFlightChargesUpdated: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCPurchaseChargeCostItems: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCPurchaseChargeCostItemsResponse: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCCancelUnfinalizedTransactions: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCCancelUnfinalizedTransactionsResponse: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCRecycleMultipleItems: _ClassVar[EGCItemMsg]
    k_EMsgClientToGCRecycleMultipleItemsResponse: _ClassVar[EGCItemMsg]

class EGCMsgInitiateTradeResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EGCMsgInitiateTradeResponse_Accepted: _ClassVar[EGCMsgInitiateTradeResponse]
    k_EGCMsgInitiateTradeResponse_Declined: _ClassVar[EGCMsgInitiateTradeResponse]
    k_EGCMsgInitiateTradeResponse_VAC_Banned_Initiator: _ClassVar[EGCMsgInitiateTradeResponse]
    k_EGCMsgInitiateTradeResponse_VAC_Banned_Target: _ClassVar[EGCMsgInitiateTradeResponse]
    k_EGCMsgInitiateTradeResponse_Target_Already_Trading: _ClassVar[EGCMsgInitiateTradeResponse]
    k_EGCMsgInitiateTradeResponse_Disabled: _ClassVar[EGCMsgInitiateTradeResponse]
    k_EGCMsgInitiateTradeResponse_NotLoggedIn: _ClassVar[EGCMsgInitiateTradeResponse]
    k_EGCMsgInitiateTradeResponse_Cancel: _ClassVar[EGCMsgInitiateTradeResponse]
    k_EGCMsgInitiateTradeResponse_TooSoon: _ClassVar[EGCMsgInitiateTradeResponse]
    k_EGCMsgInitiateTradeResponse_TooSoonPenalty: _ClassVar[EGCMsgInitiateTradeResponse]
    k_EGCMsgInitiateTradeResponse_Trade_Banned_Initiator: _ClassVar[EGCMsgInitiateTradeResponse]
    k_EGCMsgInitiateTradeResponse_Trade_Banned_Target: _ClassVar[EGCMsgInitiateTradeResponse]
    k_EGCMsgInitiateTradeResponse_Free_Account_Initiator_DEPRECATED: _ClassVar[
        EGCMsgInitiateTradeResponse
    ]
    k_EGCMsgInitiateTradeResponse_Shared_Account_Initiator: _ClassVar[EGCMsgInitiateTradeResponse]
    k_EGCMsgInitiateTradeResponse_Service_Unavailable: _ClassVar[EGCMsgInitiateTradeResponse]
    k_EGCMsgInitiateTradeResponse_Target_Blocked: _ClassVar[EGCMsgInitiateTradeResponse]
    k_EGCMsgInitiateTradeResponse_NeedVerifiedEmail: _ClassVar[EGCMsgInitiateTradeResponse]
    k_EGCMsgInitiateTradeResponse_NeedSteamGuard: _ClassVar[EGCMsgInitiateTradeResponse]
    k_EGCMsgInitiateTradeResponse_SteamGuardDuration: _ClassVar[EGCMsgInitiateTradeResponse]
    k_EGCMsgInitiateTradeResponse_TheyCannotTrade: _ClassVar[EGCMsgInitiateTradeResponse]
    k_EGCMsgInitiateTradeResponse_Recent_Password_Reset: _ClassVar[EGCMsgInitiateTradeResponse]
    k_EGCMsgInitiateTradeResponse_Using_New_Device: _ClassVar[EGCMsgInitiateTradeResponse]
    k_EGCMsgInitiateTradeResponse_Sent_Invalid_Cookie: _ClassVar[EGCMsgInitiateTradeResponse]
    k_EGCMsgInitiateTradeResponse_TooRecentFriend: _ClassVar[EGCMsgInitiateTradeResponse]
    k_EGCMsgInitiateTradeResponse_WalledFundsNotTrusted: _ClassVar[EGCMsgInitiateTradeResponse]

k_EMsgGCBase: EGCItemMsg
k_EMsgGCSetItemPosition: EGCItemMsg
k_EMsgClientToGCPackBundle: EGCItemMsg
k_EMsgClientToGCPackBundleResponse: EGCItemMsg
k_EMsgGCDelete: EGCItemMsg
k_EMsgGCVerifyCacheSubscription: EGCItemMsg
k_EMsgClientToGCNameItem: EGCItemMsg
k_EMsgGCPaintItem: EGCItemMsg
k_EMsgGCPaintItemResponse: EGCItemMsg
k_EMsgGCNameBaseItem: EGCItemMsg
k_EMsgGCNameBaseItemResponse: EGCItemMsg
k_EMsgGCUseItemRequest: EGCItemMsg
k_EMsgGCUseItemResponse: EGCItemMsg
k_EMsgGCGiftedItems: EGCItemMsg
k_EMsgGCUnwrapGiftRequest: EGCItemMsg
k_EMsgGCUnwrapGiftResponse: EGCItemMsg
k_EMsgGCSortItems: EGCItemMsg
k_EMsgGCBackpackSortFinished: EGCItemMsg
k_EMsgGCAdjustItemEquippedState: EGCItemMsg
k_EMsgGCItemAcknowledged: EGCItemMsg
k_EMsgClientToGCNameItemResponse: EGCItemMsg
k_EMsgGCApplyStrangePart: EGCItemMsg
k_EMsgGCApplyPennantUpgrade: EGCItemMsg
k_EMsgGCSetItemPositions: EGCItemMsg
k_EMsgGCApplyEggEssence: EGCItemMsg
k_EMsgGCNameEggEssenceResponse: EGCItemMsg
k_EMsgGCExtractGems: EGCItemMsg
k_EMsgGCAddSocket: EGCItemMsg
k_EMsgGCAddItemToSocket: EGCItemMsg
k_EMsgGCAddItemToSocketResponse: EGCItemMsg
k_EMsgGCAddSocketResponse: EGCItemMsg
k_EMsgGCResetStrangeGemCount: EGCItemMsg
k_EMsgGCRequestCrateItems: EGCItemMsg
k_EMsgGCRequestCrateItemsResponse: EGCItemMsg
k_EMsgGCExtractGemsResponse: EGCItemMsg
k_EMsgGCResetStrangeGemCountResponse: EGCItemMsg
k_EMsgGCServerUseItemRequest: EGCItemMsg
k_EMsgGCAddGiftItem: EGCItemMsg
k_EMsgSQLGCToGCRevokeUntrustedGift: EGCItemMsg
k_EMsgClientToGCRemoveItemGifterAttributes: EGCItemMsg
k_EMsgClientToGCRemoveItemName: EGCItemMsg
k_EMsgClientToGCRemoveItemDescription: EGCItemMsg
k_EMsgClientToGCRemoveItemAttributeResponse: EGCItemMsg
k_EMsgGCDev_NewItemRequest: EGCItemMsg
k_EMsgGCDev_NewItemRequestResponse: EGCItemMsg
k_EMsgGCDev_UnlockAllItemStylesRequest: EGCItemMsg
k_EMsgGCDev_UnlockAllItemStylesResponse: EGCItemMsg
k_EMsgGCStorePurchaseFinalize: EGCItemMsg
k_EMsgGCStorePurchaseFinalizeResponse: EGCItemMsg
k_EMsgGCStorePurchaseCancel: EGCItemMsg
k_EMsgGCStorePurchaseCancelResponse: EGCItemMsg
k_EMsgGCStorePurchaseInit: EGCItemMsg
k_EMsgGCStorePurchaseInitResponse: EGCItemMsg
k_EMsgGCToGCBannedWordListUpdated: EGCItemMsg
k_EMsgGCToGCDirtySDOCache: EGCItemMsg
k_EMsgGCToGCUpdateSQLKeyValue: EGCItemMsg
k_EMsgGCToGCBroadcastConsoleCommand: EGCItemMsg
k_EMsgGCServerVersionUpdated: EGCItemMsg
k_EMsgGCApplyAutograph: EGCItemMsg
k_EMsgGCToGCWebAPIAccountChanged: EGCItemMsg
k_EMsgGCClientVersionUpdated: EGCItemMsg
k_EMsgGCToGCUpdateWelcomeMsg: EGCItemMsg
k_EMsgGCToGCPlayerStrangeCountAdjustments: EGCItemMsg
k_EMsgGCRequestStoreSalesData: EGCItemMsg
k_EMsgGCRequestStoreSalesDataResponse: EGCItemMsg
k_EMsgGCRequestStoreSalesDataUpToDateResponse: EGCItemMsg
k_EMsgGCToGCPingRequest: EGCItemMsg
k_EMsgGCToGCPingResponse: EGCItemMsg
k_EMsgGCToGCGetUserSessionServer: EGCItemMsg
k_EMsgGCToGCGetUserSessionServerResponse: EGCItemMsg
k_EMsgGCToGCGetUserServerMembers: EGCItemMsg
k_EMsgGCToGCGetUserServerMembersResponse: EGCItemMsg
k_EMsgGCToGCCanUseDropRateBonus: EGCItemMsg
k_EMsgSQLAddDropRateBonus: EGCItemMsg
k_EMsgGCToGCRefreshSOCache: EGCItemMsg
k_EMsgGCToGCGrantAccountRolledItems: EGCItemMsg
k_EMsgGCToGCGrantSelfMadeItemToAccount: EGCItemMsg
k_EMsgGCToGCUnlockCrate: EGCItemMsg
k_EMsgGCStatueCraft: EGCItemMsg
k_EMsgGCRedeemCode: EGCItemMsg
k_EMsgGCRedeemCodeResponse: EGCItemMsg
k_EMsgGCToGCItemConsumptionRollback: EGCItemMsg
k_EMsgClientToGCWrapAndDeliverGift: EGCItemMsg
k_EMsgClientToGCWrapAndDeliverGiftResponse: EGCItemMsg
k_EMsgClientToGCUnpackBundleResponse: EGCItemMsg
k_EMsgGCToClientStoreTransactionCompleted: EGCItemMsg
k_EMsgClientToGCEquipItems: EGCItemMsg
k_EMsgClientToGCEquipItemsResponse: EGCItemMsg
k_EMsgClientToGCUnlockItemStyle: EGCItemMsg
k_EMsgClientToGCUnlockItemStyleResponse: EGCItemMsg
k_EMsgClientToGCSetItemInventoryCategory: EGCItemMsg
k_EMsgClientToGCUnlockCrate: EGCItemMsg
k_EMsgClientToGCUnlockCrateResponse: EGCItemMsg
k_EMsgClientToGCUnpackBundle: EGCItemMsg
k_EMsgClientToGCSetItemStyle: EGCItemMsg
k_EMsgClientToGCSetItemStyleResponse: EGCItemMsg
k_EMsgSQLGCToGCGrantBackpackSlots: EGCItemMsg
k_EMsgClientToGCLookupAccountName: EGCItemMsg
k_EMsgClientToGCLookupAccountNameResponse: EGCItemMsg
k_EMsgClientToGCCreateStaticRecipe: EGCItemMsg
k_EMsgClientToGCCreateStaticRecipeResponse: EGCItemMsg
k_EMsgGCToGCStoreProcessCDKeyTransaction: EGCItemMsg
k_EMsgGCToGCStoreProcessCDKeyTransactionResponse: EGCItemMsg
k_EMsgGCToGCStoreProcessSettlement: EGCItemMsg
k_EMsgGCToGCStoreProcessSettlementResponse: EGCItemMsg
k_EMsgGCToGCConsoleOutput: EGCItemMsg
k_EMsgGCToClientItemAges: EGCItemMsg
k_EMsgGCToGCInternalTestMsg: EGCItemMsg
k_EMsgGCToGCClientServerVersionsUpdated: EGCItemMsg
k_EMsgGCUseMultipleItemsRequest: EGCItemMsg
k_EMsgGCGetAccountSubscriptionItem: EGCItemMsg
k_EMsgGCGetAccountSubscriptionItemResponse: EGCItemMsg
k_EMsgGCToGCBroadcastMessageFromSub: EGCItemMsg
k_EMsgGCToClientCurrencyPricePoints: EGCItemMsg
k_EMsgGCToGCAddSubscriptionTime: EGCItemMsg
k_EMsgGCToGCFlushSteamInventoryCache: EGCItemMsg
k_EMsgGCRequestCrateEscalationLevel: EGCItemMsg
k_EMsgGCRequestCrateEscalationLevelResponse: EGCItemMsg
k_EMsgGCToGCUpdateSubscriptionItems: EGCItemMsg
k_EMsgGCToGCSelfPing: EGCItemMsg
k_EMsgGCToGCGetInfuxIntervalStats: EGCItemMsg
k_EMsgGCToGCGetInfuxIntervalStatsResponse: EGCItemMsg
k_EMsgGCToGCPurchaseSucceeded: EGCItemMsg
k_EMsgClientToGCGetLimitedItemPurchaseQuantity: EGCItemMsg
k_EMsgClientToGCGetLimitedItemPurchaseQuantityResponse: EGCItemMsg
k_EMsgGCToGCBetaDeleteItems: EGCItemMsg
k_EMsgClientToGCGetInFlightItemCharges: EGCItemMsg
k_EMsgClientToGCGetInFlightItemChargesResponse: EGCItemMsg
k_EMsgGCToClientInFlightChargesUpdated: EGCItemMsg
k_EMsgClientToGCPurchaseChargeCostItems: EGCItemMsg
k_EMsgClientToGCPurchaseChargeCostItemsResponse: EGCItemMsg
k_EMsgClientToGCCancelUnfinalizedTransactions: EGCItemMsg
k_EMsgClientToGCCancelUnfinalizedTransactionsResponse: EGCItemMsg
k_EMsgClientToGCRecycleMultipleItems: EGCItemMsg
k_EMsgClientToGCRecycleMultipleItemsResponse: EGCItemMsg
k_EGCMsgInitiateTradeResponse_Accepted: EGCMsgInitiateTradeResponse
k_EGCMsgInitiateTradeResponse_Declined: EGCMsgInitiateTradeResponse
k_EGCMsgInitiateTradeResponse_VAC_Banned_Initiator: EGCMsgInitiateTradeResponse
k_EGCMsgInitiateTradeResponse_VAC_Banned_Target: EGCMsgInitiateTradeResponse
k_EGCMsgInitiateTradeResponse_Target_Already_Trading: EGCMsgInitiateTradeResponse
k_EGCMsgInitiateTradeResponse_Disabled: EGCMsgInitiateTradeResponse
k_EGCMsgInitiateTradeResponse_NotLoggedIn: EGCMsgInitiateTradeResponse
k_EGCMsgInitiateTradeResponse_Cancel: EGCMsgInitiateTradeResponse
k_EGCMsgInitiateTradeResponse_TooSoon: EGCMsgInitiateTradeResponse
k_EGCMsgInitiateTradeResponse_TooSoonPenalty: EGCMsgInitiateTradeResponse
k_EGCMsgInitiateTradeResponse_Trade_Banned_Initiator: EGCMsgInitiateTradeResponse
k_EGCMsgInitiateTradeResponse_Trade_Banned_Target: EGCMsgInitiateTradeResponse
k_EGCMsgInitiateTradeResponse_Free_Account_Initiator_DEPRECATED: EGCMsgInitiateTradeResponse
k_EGCMsgInitiateTradeResponse_Shared_Account_Initiator: EGCMsgInitiateTradeResponse
k_EGCMsgInitiateTradeResponse_Service_Unavailable: EGCMsgInitiateTradeResponse
k_EGCMsgInitiateTradeResponse_Target_Blocked: EGCMsgInitiateTradeResponse
k_EGCMsgInitiateTradeResponse_NeedVerifiedEmail: EGCMsgInitiateTradeResponse
k_EGCMsgInitiateTradeResponse_NeedSteamGuard: EGCMsgInitiateTradeResponse
k_EGCMsgInitiateTradeResponse_SteamGuardDuration: EGCMsgInitiateTradeResponse
k_EGCMsgInitiateTradeResponse_TheyCannotTrade: EGCMsgInitiateTradeResponse
k_EGCMsgInitiateTradeResponse_Recent_Password_Reset: EGCMsgInitiateTradeResponse
k_EGCMsgInitiateTradeResponse_Using_New_Device: EGCMsgInitiateTradeResponse
k_EGCMsgInitiateTradeResponse_Sent_Invalid_Cookie: EGCMsgInitiateTradeResponse
k_EGCMsgInitiateTradeResponse_TooRecentFriend: EGCMsgInitiateTradeResponse
k_EGCMsgInitiateTradeResponse_WalledFundsNotTrusted: EGCMsgInitiateTradeResponse

class CMsgApplyAutograph(_message.Message):
    __slots__ = ("autograph_item_id", "item_item_id")
    AUTOGRAPH_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    autograph_item_id: int
    item_item_id: int
    def __init__(
        self, autograph_item_id: int | None = ..., item_item_id: int | None = ...
    ) -> None: ...

class CMsgAdjustItemEquippedState(_message.Message):
    __slots__ = ("item_id", "new_class", "new_slot", "style_index")
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_CLASS_FIELD_NUMBER: _ClassVar[int]
    NEW_SLOT_FIELD_NUMBER: _ClassVar[int]
    STYLE_INDEX_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    new_class: int
    new_slot: int
    style_index: int
    def __init__(
        self,
        item_id: int | None = ...,
        new_class: int | None = ...,
        new_slot: int | None = ...,
        style_index: int | None = ...,
    ) -> None: ...

class CMsgEconPlayerStrangeCountAdjustment(_message.Message):
    __slots__ = ("account_id", "strange_count_adjustments", "turbo_mode")
    class CStrangeCountAdjustment(_message.Message):
        __slots__ = ("event_type", "item_id", "adjustment")
        EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
        ITEM_ID_FIELD_NUMBER: _ClassVar[int]
        ADJUSTMENT_FIELD_NUMBER: _ClassVar[int]
        event_type: int
        item_id: int
        adjustment: int
        def __init__(
            self,
            event_type: int | None = ...,
            item_id: int | None = ...,
            adjustment: int | None = ...,
        ) -> None: ...

    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    STRANGE_COUNT_ADJUSTMENTS_FIELD_NUMBER: _ClassVar[int]
    TURBO_MODE_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    strange_count_adjustments: _containers.RepeatedCompositeFieldContainer[
        CMsgEconPlayerStrangeCountAdjustment.CStrangeCountAdjustment
    ]
    turbo_mode: bool
    def __init__(
        self,
        account_id: int | None = ...,
        strange_count_adjustments: _Iterable[
            CMsgEconPlayerStrangeCountAdjustment.CStrangeCountAdjustment | _Mapping
        ]
        | None = ...,
        turbo_mode: bool = ...,
    ) -> None: ...

class CMsgCraftingResponse(_message.Message):
    __slots__ = ("item_ids",)
    ITEM_IDS_FIELD_NUMBER: _ClassVar[int]
    item_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, item_ids: _Iterable[int] | None = ...) -> None: ...

class CMsgGCRequestStoreSalesData(_message.Message):
    __slots__ = ("version", "currency")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    version: int
    currency: int
    def __init__(self, version: int | None = ..., currency: int | None = ...) -> None: ...

class CMsgGCRequestStoreSalesDataResponse(_message.Message):
    __slots__ = ("sale_price", "version", "expiration_time")
    class Price(_message.Message):
        __slots__ = ("item_def", "price")
        ITEM_DEF_FIELD_NUMBER: _ClassVar[int]
        PRICE_FIELD_NUMBER: _ClassVar[int]
        item_def: int
        price: int
        def __init__(self, item_def: int | None = ..., price: int | None = ...) -> None: ...

    SALE_PRICE_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_TIME_FIELD_NUMBER: _ClassVar[int]
    sale_price: _containers.RepeatedCompositeFieldContainer[
        CMsgGCRequestStoreSalesDataResponse.Price
    ]
    version: int
    expiration_time: int
    def __init__(
        self,
        sale_price: _Iterable[CMsgGCRequestStoreSalesDataResponse.Price | _Mapping] | None = ...,
        version: int | None = ...,
        expiration_time: int | None = ...,
    ) -> None: ...

class CMsgGCRequestStoreSalesDataUpToDateResponse(_message.Message):
    __slots__ = ("version", "expiration_time")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_TIME_FIELD_NUMBER: _ClassVar[int]
    version: int
    expiration_time: int
    def __init__(self, version: int | None = ..., expiration_time: int | None = ...) -> None: ...

class CMsgGCToGCPingRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgGCToGCPingResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgGCToGCGetUserSessionServer(_message.Message):
    __slots__ = ("account_id",)
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    def __init__(self, account_id: int | None = ...) -> None: ...

class CMsgGCToGCGetUserSessionServerResponse(_message.Message):
    __slots__ = ("server_steam_id", "is_online")
    SERVER_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    IS_ONLINE_FIELD_NUMBER: _ClassVar[int]
    server_steam_id: int
    is_online: bool
    def __init__(self, server_steam_id: int | None = ..., is_online: bool = ...) -> None: ...

class CMsgGCToGCGetUserServerMembers(_message.Message):
    __slots__ = ("account_id", "max_spectators")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    MAX_SPECTATORS_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    max_spectators: int
    def __init__(self, account_id: int | None = ..., max_spectators: int | None = ...) -> None: ...

class CMsgGCToGCGetUserServerMembersResponse(_message.Message):
    __slots__ = ("member_account_id",)
    MEMBER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    member_account_id: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, member_account_id: _Iterable[int] | None = ...) -> None: ...

class CMsgLookupMultipleAccountNames(_message.Message):
    __slots__ = ("accountids",)
    ACCOUNTIDS_FIELD_NUMBER: _ClassVar[int]
    accountids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, accountids: _Iterable[int] | None = ...) -> None: ...

class CMsgLookupMultipleAccountNamesResponse(_message.Message):
    __slots__ = ("accounts",)
    class Account(_message.Message):
        __slots__ = ("accountid", "persona")
        ACCOUNTID_FIELD_NUMBER: _ClassVar[int]
        PERSONA_FIELD_NUMBER: _ClassVar[int]
        accountid: int
        persona: str
        def __init__(self, accountid: int | None = ..., persona: str | None = ...) -> None: ...

    ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    accounts: _containers.RepeatedCompositeFieldContainer[
        CMsgLookupMultipleAccountNamesResponse.Account
    ]
    def __init__(
        self,
        accounts: _Iterable[CMsgLookupMultipleAccountNamesResponse.Account | _Mapping] | None = ...,
    ) -> None: ...

class CMsgRequestCrateItems(_message.Message):
    __slots__ = ("crate_item_def",)
    CRATE_ITEM_DEF_FIELD_NUMBER: _ClassVar[int]
    crate_item_def: int
    def __init__(self, crate_item_def: int | None = ...) -> None: ...

class CMsgRequestCrateItemsResponse(_message.Message):
    __slots__ = ("response", "item_defs", "peek_item_defs", "peek_items")
    class EResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_Succeeded: _ClassVar[CMsgRequestCrateItemsResponse.EResult]
        k_Failed: _ClassVar[CMsgRequestCrateItemsResponse.EResult]

    k_Succeeded: CMsgRequestCrateItemsResponse.EResult
    k_Failed: CMsgRequestCrateItemsResponse.EResult
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    ITEM_DEFS_FIELD_NUMBER: _ClassVar[int]
    PEEK_ITEM_DEFS_FIELD_NUMBER: _ClassVar[int]
    PEEK_ITEMS_FIELD_NUMBER: _ClassVar[int]
    response: int
    item_defs: _containers.RepeatedScalarFieldContainer[int]
    peek_item_defs: _containers.RepeatedScalarFieldContainer[int]
    peek_items: _containers.RepeatedCompositeFieldContainer[_base_gcmessages_pb2.CSOEconItem]
    def __init__(
        self,
        response: int | None = ...,
        item_defs: _Iterable[int] | None = ...,
        peek_item_defs: _Iterable[int] | None = ...,
        peek_items: _Iterable[_base_gcmessages_pb2.CSOEconItem | _Mapping] | None = ...,
    ) -> None: ...

class CMsgRequestCrateEscalationLevel(_message.Message):
    __slots__ = ("crate_item_def",)
    CRATE_ITEM_DEF_FIELD_NUMBER: _ClassVar[int]
    crate_item_def: int
    def __init__(self, crate_item_def: int | None = ...) -> None: ...

class CMsgRequestCrateEscalationLevelResponse(_message.Message):
    __slots__ = (
        "response",
        "escalation_level0",
        "escalation_level1",
        "escalation_level2",
        "escalation_level3",
    )
    class EResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_Succeeded: _ClassVar[CMsgRequestCrateEscalationLevelResponse.EResult]
        k_Failed: _ClassVar[CMsgRequestCrateEscalationLevelResponse.EResult]

    k_Succeeded: CMsgRequestCrateEscalationLevelResponse.EResult
    k_Failed: CMsgRequestCrateEscalationLevelResponse.EResult
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    ESCALATION_LEVEL0_FIELD_NUMBER: _ClassVar[int]
    ESCALATION_LEVEL1_FIELD_NUMBER: _ClassVar[int]
    ESCALATION_LEVEL2_FIELD_NUMBER: _ClassVar[int]
    ESCALATION_LEVEL3_FIELD_NUMBER: _ClassVar[int]
    response: int
    escalation_level0: int
    escalation_level1: int
    escalation_level2: int
    escalation_level3: int
    def __init__(
        self,
        response: int | None = ...,
        escalation_level0: int | None = ...,
        escalation_level1: int | None = ...,
        escalation_level2: int | None = ...,
        escalation_level3: int | None = ...,
    ) -> None: ...

class CMsgGCToGCCanUseDropRateBonus(_message.Message):
    __slots__ = (
        "account_id",
        "drop_rate_bonus",
        "booster_type",
        "exclusive_item_def",
        "allow_equal_rate",
    )
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    DROP_RATE_BONUS_FIELD_NUMBER: _ClassVar[int]
    BOOSTER_TYPE_FIELD_NUMBER: _ClassVar[int]
    EXCLUSIVE_ITEM_DEF_FIELD_NUMBER: _ClassVar[int]
    ALLOW_EQUAL_RATE_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    drop_rate_bonus: float
    booster_type: int
    exclusive_item_def: int
    allow_equal_rate: bool
    def __init__(
        self,
        account_id: int | None = ...,
        drop_rate_bonus: float | None = ...,
        booster_type: int | None = ...,
        exclusive_item_def: int | None = ...,
        allow_equal_rate: bool = ...,
    ) -> None: ...

class CMsgSQLAddDropRateBonus(_message.Message):
    __slots__ = (
        "account_id",
        "item_id",
        "item_def",
        "drop_rate_bonus",
        "booster_type",
        "seconds_duration",
        "end_time_stamp",
    )
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_DEF_FIELD_NUMBER: _ClassVar[int]
    DROP_RATE_BONUS_FIELD_NUMBER: _ClassVar[int]
    BOOSTER_TYPE_FIELD_NUMBER: _ClassVar[int]
    SECONDS_DURATION_FIELD_NUMBER: _ClassVar[int]
    END_TIME_STAMP_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    item_id: int
    item_def: int
    drop_rate_bonus: float
    booster_type: int
    seconds_duration: int
    end_time_stamp: int
    def __init__(
        self,
        account_id: int | None = ...,
        item_id: int | None = ...,
        item_def: int | None = ...,
        drop_rate_bonus: float | None = ...,
        booster_type: int | None = ...,
        seconds_duration: int | None = ...,
        end_time_stamp: int | None = ...,
    ) -> None: ...

class CMsgSQLUpgradeBattleBooster(_message.Message):
    __slots__ = ("account_id", "item_def", "bonus_to_add", "booster_type")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_DEF_FIELD_NUMBER: _ClassVar[int]
    BONUS_TO_ADD_FIELD_NUMBER: _ClassVar[int]
    BOOSTER_TYPE_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    item_def: int
    bonus_to_add: float
    booster_type: int
    def __init__(
        self,
        account_id: int | None = ...,
        item_def: int | None = ...,
        bonus_to_add: float | None = ...,
        booster_type: int | None = ...,
    ) -> None: ...

class CMsgGCToGCRefreshSOCache(_message.Message):
    __slots__ = ("account_id", "reload")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    RELOAD_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    reload: bool
    def __init__(self, account_id: int | None = ..., reload: bool = ...) -> None: ...

class CMsgGCToGCAddSubscriptionTime(_message.Message):
    __slots__ = ("account_id", "matching_subscription_def_indexes", "additional_seconds")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    MATCHING_SUBSCRIPTION_DEF_INDEXES_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    matching_subscription_def_indexes: _containers.RepeatedScalarFieldContainer[int]
    additional_seconds: int
    def __init__(
        self,
        account_id: int | None = ...,
        matching_subscription_def_indexes: _Iterable[int] | None = ...,
        additional_seconds: int | None = ...,
    ) -> None: ...

class CMsgGCToGCGrantAccountRolledItems(_message.Message):
    __slots__ = ("account_id", "items", "audit_action", "audit_data")
    class Item(_message.Message):
        __slots__ = (
            "item_def",
            "loot_lists",
            "ignore_limit",
            "origin",
            "dynamic_attributes",
            "additional_audit_entries",
            "inventory_token",
            "quality",
        )
        class DynamicAttribute(_message.Message):
            __slots__ = ("name", "value_uint32", "value_float", "value_string")
            NAME_FIELD_NUMBER: _ClassVar[int]
            VALUE_UINT32_FIELD_NUMBER: _ClassVar[int]
            VALUE_FLOAT_FIELD_NUMBER: _ClassVar[int]
            VALUE_STRING_FIELD_NUMBER: _ClassVar[int]
            name: str
            value_uint32: int
            value_float: float
            value_string: str
            def __init__(
                self,
                name: str | None = ...,
                value_uint32: int | None = ...,
                value_float: float | None = ...,
                value_string: str | None = ...,
            ) -> None: ...

        class AdditionalAuditEntry(_message.Message):
            __slots__ = ("owner_account_id", "audit_action", "audit_data")
            OWNER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
            AUDIT_ACTION_FIELD_NUMBER: _ClassVar[int]
            AUDIT_DATA_FIELD_NUMBER: _ClassVar[int]
            owner_account_id: int
            audit_action: int
            audit_data: int
            def __init__(
                self,
                owner_account_id: int | None = ...,
                audit_action: int | None = ...,
                audit_data: int | None = ...,
            ) -> None: ...

        ITEM_DEF_FIELD_NUMBER: _ClassVar[int]
        LOOT_LISTS_FIELD_NUMBER: _ClassVar[int]
        IGNORE_LIMIT_FIELD_NUMBER: _ClassVar[int]
        ORIGIN_FIELD_NUMBER: _ClassVar[int]
        DYNAMIC_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
        ADDITIONAL_AUDIT_ENTRIES_FIELD_NUMBER: _ClassVar[int]
        INVENTORY_TOKEN_FIELD_NUMBER: _ClassVar[int]
        QUALITY_FIELD_NUMBER: _ClassVar[int]
        item_def: int
        loot_lists: _containers.RepeatedScalarFieldContainer[str]
        ignore_limit: bool
        origin: int
        dynamic_attributes: _containers.RepeatedCompositeFieldContainer[
            CMsgGCToGCGrantAccountRolledItems.Item.DynamicAttribute
        ]
        additional_audit_entries: _containers.RepeatedCompositeFieldContainer[
            CMsgGCToGCGrantAccountRolledItems.Item.AdditionalAuditEntry
        ]
        inventory_token: int
        quality: int
        def __init__(
            self,
            item_def: int | None = ...,
            loot_lists: _Iterable[str] | None = ...,
            ignore_limit: bool = ...,
            origin: int | None = ...,
            dynamic_attributes: _Iterable[
                CMsgGCToGCGrantAccountRolledItems.Item.DynamicAttribute | _Mapping
            ]
            | None = ...,
            additional_audit_entries: _Iterable[
                CMsgGCToGCGrantAccountRolledItems.Item.AdditionalAuditEntry | _Mapping
            ]
            | None = ...,
            inventory_token: int | None = ...,
            quality: int | None = ...,
        ) -> None: ...

    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    AUDIT_ACTION_FIELD_NUMBER: _ClassVar[int]
    AUDIT_DATA_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    items: _containers.RepeatedCompositeFieldContainer[CMsgGCToGCGrantAccountRolledItems.Item]
    audit_action: int
    audit_data: int
    def __init__(
        self,
        account_id: int | None = ...,
        items: _Iterable[CMsgGCToGCGrantAccountRolledItems.Item | _Mapping] | None = ...,
        audit_action: int | None = ...,
        audit_data: int | None = ...,
    ) -> None: ...

class CMsgGCToGCBetaDeleteItems(_message.Message):
    __slots__ = ("account_id", "item_ids", "item_defs")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_IDS_FIELD_NUMBER: _ClassVar[int]
    ITEM_DEFS_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    item_ids: _containers.RepeatedScalarFieldContainer[int]
    item_defs: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        account_id: int | None = ...,
        item_ids: _Iterable[int] | None = ...,
        item_defs: _Iterable[int] | None = ...,
    ) -> None: ...

class CMsgGCToGCGrantSelfMadeItemToAccount(_message.Message):
    __slots__ = ("item_def_index", "accountid")
    ITEM_DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
    ACCOUNTID_FIELD_NUMBER: _ClassVar[int]
    item_def_index: int
    accountid: int
    def __init__(self, item_def_index: int | None = ..., accountid: int | None = ...) -> None: ...

class CMsgGCToGCUnlockCrate(_message.Message):
    __slots__ = ("account_id", "crate_item_id", "key_item_id")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CRATE_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    crate_item_id: int
    key_item_id: int
    def __init__(
        self,
        account_id: int | None = ...,
        crate_item_id: int | None = ...,
        key_item_id: int | None = ...,
    ) -> None: ...

class CMsgUseItem(_message.Message):
    __slots__ = (
        "item_id",
        "target_steam_id",
        "gift__potential_targets",
        "duel__class_lock",
        "initiator_steam_id",
        "itempack__ack_immediately",
    )
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    GIFT__POTENTIAL_TARGETS_FIELD_NUMBER: _ClassVar[int]
    DUEL__CLASS_LOCK_FIELD_NUMBER: _ClassVar[int]
    INITIATOR_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    ITEMPACK__ACK_IMMEDIATELY_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    target_steam_id: int
    gift__potential_targets: _containers.RepeatedScalarFieldContainer[int]
    duel__class_lock: int
    initiator_steam_id: int
    itempack__ack_immediately: bool
    def __init__(
        self,
        item_id: int | None = ...,
        target_steam_id: int | None = ...,
        gift__potential_targets: _Iterable[int] | None = ...,
        duel__class_lock: int | None = ...,
        initiator_steam_id: int | None = ...,
        itempack__ack_immediately: bool = ...,
    ) -> None: ...

class CMsgServerUseItem(_message.Message):
    __slots__ = ("initiator_account_id", "use_item_msg")
    INITIATOR_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    USE_ITEM_MSG_FIELD_NUMBER: _ClassVar[int]
    initiator_account_id: int
    use_item_msg: CMsgUseItem
    def __init__(
        self,
        initiator_account_id: int | None = ...,
        use_item_msg: CMsgUseItem | _Mapping | None = ...,
    ) -> None: ...

class CMsgUseMultipleItems(_message.Message):
    __slots__ = ("item_ids",)
    ITEM_IDS_FIELD_NUMBER: _ClassVar[int]
    item_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, item_ids: _Iterable[int] | None = ...) -> None: ...

class CGCStoreRechargeRedirect_LineItem(_message.Message):
    __slots__ = ("item_def_id", "quantity")
    ITEM_DEF_ID_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    item_def_id: int
    quantity: int
    def __init__(self, item_def_id: int | None = ..., quantity: int | None = ...) -> None: ...

class CMsgGCEconSQLWorkItemEmbeddedRollbackData(_message.Message):
    __slots__ = (
        "account_id",
        "deleted_item_id",
        "old_audit_action",
        "new_audit_action",
        "expected_audit_action",
    )
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    DELETED_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    OLD_AUDIT_ACTION_FIELD_NUMBER: _ClassVar[int]
    NEW_AUDIT_ACTION_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_AUDIT_ACTION_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    deleted_item_id: int
    old_audit_action: int
    new_audit_action: int
    expected_audit_action: int
    def __init__(
        self,
        account_id: int | None = ...,
        deleted_item_id: int | None = ...,
        old_audit_action: int | None = ...,
        new_audit_action: int | None = ...,
        expected_audit_action: int | None = ...,
    ) -> None: ...

class CMsgCraftStatue(_message.Message):
    __slots__ = ("heroid", "sequencename", "cycle", "description", "pedestal_itemdef", "toolid")
    HEROID_FIELD_NUMBER: _ClassVar[int]
    SEQUENCENAME_FIELD_NUMBER: _ClassVar[int]
    CYCLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PEDESTAL_ITEMDEF_FIELD_NUMBER: _ClassVar[int]
    TOOLID_FIELD_NUMBER: _ClassVar[int]
    heroid: int
    sequencename: str
    cycle: float
    description: str
    pedestal_itemdef: int
    toolid: int
    def __init__(
        self,
        heroid: int | None = ...,
        sequencename: str | None = ...,
        cycle: float | None = ...,
        description: str | None = ...,
        pedestal_itemdef: int | None = ...,
        toolid: int | None = ...,
    ) -> None: ...

class CMsgRedeemCode(_message.Message):
    __slots__ = ("code",)
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: str
    def __init__(self, code: str | None = ...) -> None: ...

class CMsgRedeemCodeResponse(_message.Message):
    __slots__ = ("response", "item_id")
    class EResultCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_Succeeded: _ClassVar[CMsgRedeemCodeResponse.EResultCode]
        k_Failed_CodeNotFound: _ClassVar[CMsgRedeemCodeResponse.EResultCode]
        k_Failed_CodeAlreadyUsed: _ClassVar[CMsgRedeemCodeResponse.EResultCode]
        k_Failed_OtherError: _ClassVar[CMsgRedeemCodeResponse.EResultCode]

    k_Succeeded: CMsgRedeemCodeResponse.EResultCode
    k_Failed_CodeNotFound: CMsgRedeemCodeResponse.EResultCode
    k_Failed_CodeAlreadyUsed: CMsgRedeemCodeResponse.EResultCode
    k_Failed_OtherError: CMsgRedeemCodeResponse.EResultCode
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    response: int
    item_id: int
    def __init__(self, response: int | None = ..., item_id: int | None = ...) -> None: ...

class CMsgDevNewItemRequest(_message.Message):
    __slots__ = ("item_def_name", "loot_list_name", "attr_def_name", "attr_value", "item_quality")
    ITEM_DEF_NAME_FIELD_NUMBER: _ClassVar[int]
    LOOT_LIST_NAME_FIELD_NUMBER: _ClassVar[int]
    ATTR_DEF_NAME_FIELD_NUMBER: _ClassVar[int]
    ATTR_VALUE_FIELD_NUMBER: _ClassVar[int]
    ITEM_QUALITY_FIELD_NUMBER: _ClassVar[int]
    item_def_name: str
    loot_list_name: str
    attr_def_name: _containers.RepeatedScalarFieldContainer[str]
    attr_value: _containers.RepeatedScalarFieldContainer[str]
    item_quality: int
    def __init__(
        self,
        item_def_name: str | None = ...,
        loot_list_name: str | None = ...,
        attr_def_name: _Iterable[str] | None = ...,
        attr_value: _Iterable[str] | None = ...,
        item_quality: int | None = ...,
    ) -> None: ...

class CMsgDevNewItemRequestResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class CMsgDevUnlockAllItemStyles(_message.Message):
    __slots__ = ("item_id",)
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    def __init__(self, item_id: int | None = ...) -> None: ...

class CMsgDevUnlockAllItemStylesResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class CMsgGCGetAccountSubscriptionItem(_message.Message):
    __slots__ = ("account_id",)
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    def __init__(self, account_id: int | None = ...) -> None: ...

class CMsgGCGetAccountSubscriptionItemResponse(_message.Message):
    __slots__ = ("def_index",)
    DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
    def_index: int
    def __init__(self, def_index: int | None = ...) -> None: ...

class CMsgGCAddGiftItem(_message.Message):
    __slots__ = (
        "gifter_account_id",
        "receiver_account_id",
        "wrapped_item",
        "gift_message",
        "is_wallet_cash_trusted",
    )
    GIFTER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    RECEIVER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    WRAPPED_ITEM_FIELD_NUMBER: _ClassVar[int]
    GIFT_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    IS_WALLET_CASH_TRUSTED_FIELD_NUMBER: _ClassVar[int]
    gifter_account_id: int
    receiver_account_id: int
    wrapped_item: _base_gcmessages_pb2.CSOEconItem
    gift_message: str
    is_wallet_cash_trusted: bool
    def __init__(
        self,
        gifter_account_id: int | None = ...,
        receiver_account_id: int | None = ...,
        wrapped_item: _base_gcmessages_pb2.CSOEconItem | _Mapping | None = ...,
        gift_message: str | None = ...,
        is_wallet_cash_trusted: bool = ...,
    ) -> None: ...

class CMsgClientToGCWrapAndDeliverGift(_message.Message):
    __slots__ = ("item_id", "give_to_account_id", "gift_message")
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    GIVE_TO_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    GIFT_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    give_to_account_id: int
    gift_message: str
    def __init__(
        self,
        item_id: int | None = ...,
        give_to_account_id: int | None = ...,
        gift_message: str | None = ...,
    ) -> None: ...

class CMsgSQLGCToGCRevokeUntrustedGift(_message.Message):
    __slots__ = ("account_id", "sent_item_id")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SENT_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    sent_item_id: int
    def __init__(self, account_id: int | None = ..., sent_item_id: int | None = ...) -> None: ...

class CMsgClientToGCWrapAndDeliverGiftResponse(_message.Message):
    __slots__ = (
        "response",
        "gifting_charge_uses",
        "gifting_charge_max",
        "gifting_uses",
        "gifting_max",
        "gifting_window_hours",
        "trade_restriction",
    )
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    GIFTING_CHARGE_USES_FIELD_NUMBER: _ClassVar[int]
    GIFTING_CHARGE_MAX_FIELD_NUMBER: _ClassVar[int]
    GIFTING_USES_FIELD_NUMBER: _ClassVar[int]
    GIFTING_MAX_FIELD_NUMBER: _ClassVar[int]
    GIFTING_WINDOW_HOURS_FIELD_NUMBER: _ClassVar[int]
    TRADE_RESTRICTION_FIELD_NUMBER: _ClassVar[int]
    response: _econ_shared_enums_pb2.EGCMsgResponse
    gifting_charge_uses: int
    gifting_charge_max: int
    gifting_uses: int
    gifting_max: int
    gifting_window_hours: int
    trade_restriction: EGCMsgInitiateTradeResponse
    def __init__(
        self,
        response: _econ_shared_enums_pb2.EGCMsgResponse | str | None = ...,
        gifting_charge_uses: int | None = ...,
        gifting_charge_max: int | None = ...,
        gifting_uses: int | None = ...,
        gifting_max: int | None = ...,
        gifting_window_hours: int | None = ...,
        trade_restriction: EGCMsgInitiateTradeResponse | str | None = ...,
    ) -> None: ...

class CMsgClientToGCUnwrapGift(_message.Message):
    __slots__ = ("item_id",)
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    def __init__(self, item_id: int | None = ...) -> None: ...

class CMsgClientToGCGetGiftPermissions(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCGetGiftPermissionsResponse(_message.Message):
    __slots__ = (
        "is_unlimited",
        "has_two_factor",
        "sender_permission",
        "friendship_age_requirement",
        "friendship_age_requirement_two_factor",
        "friend_permissions",
    )
    class FriendPermission(_message.Message):
        __slots__ = ("account_id", "permission")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        PERMISSION_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        permission: EGCMsgInitiateTradeResponse
        def __init__(
            self,
            account_id: int | None = ...,
            permission: EGCMsgInitiateTradeResponse | str | None = ...,
        ) -> None: ...

    IS_UNLIMITED_FIELD_NUMBER: _ClassVar[int]
    HAS_TWO_FACTOR_FIELD_NUMBER: _ClassVar[int]
    SENDER_PERMISSION_FIELD_NUMBER: _ClassVar[int]
    FRIENDSHIP_AGE_REQUIREMENT_FIELD_NUMBER: _ClassVar[int]
    FRIENDSHIP_AGE_REQUIREMENT_TWO_FACTOR_FIELD_NUMBER: _ClassVar[int]
    FRIEND_PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    is_unlimited: bool
    has_two_factor: bool
    sender_permission: EGCMsgInitiateTradeResponse
    friendship_age_requirement: int
    friendship_age_requirement_two_factor: int
    friend_permissions: _containers.RepeatedCompositeFieldContainer[
        CMsgClientToGCGetGiftPermissionsResponse.FriendPermission
    ]
    def __init__(
        self,
        is_unlimited: bool = ...,
        has_two_factor: bool = ...,
        sender_permission: EGCMsgInitiateTradeResponse | str | None = ...,
        friendship_age_requirement: int | None = ...,
        friendship_age_requirement_two_factor: int | None = ...,
        friend_permissions: _Iterable[
            CMsgClientToGCGetGiftPermissionsResponse.FriendPermission | _Mapping
        ]
        | None = ...,
    ) -> None: ...

class CMsgClientToGCUnpackBundle(_message.Message):
    __slots__ = ("item_id",)
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    def __init__(self, item_id: int | None = ...) -> None: ...

class CMsgClientToGCUnpackBundleResponse(_message.Message):
    __slots__ = ("unpacked_item_ids", "response", "unpacked_item_def_indexes")
    class EUnpackBundle(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_UnpackBundle_Succeeded: _ClassVar[CMsgClientToGCUnpackBundleResponse.EUnpackBundle]
        k_UnpackBundle_Failed_ItemIsNotBundle: _ClassVar[
            CMsgClientToGCUnpackBundleResponse.EUnpackBundle
        ]
        k_UnpackBundle_Failed_UnableToCreateContainedItem: _ClassVar[
            CMsgClientToGCUnpackBundleResponse.EUnpackBundle
        ]
        k_UnpackBundle_Failed_SOCacheError: _ClassVar[
            CMsgClientToGCUnpackBundleResponse.EUnpackBundle
        ]
        k_UnpackBundle_Failed_ItemIsInvalid: _ClassVar[
            CMsgClientToGCUnpackBundleResponse.EUnpackBundle
        ]
        k_UnpackBundle_Failed_BadItemQuantity: _ClassVar[
            CMsgClientToGCUnpackBundleResponse.EUnpackBundle
        ]
        k_UnpackBundle_Failed_UnableToDeleteItem: _ClassVar[
            CMsgClientToGCUnpackBundleResponse.EUnpackBundle
        ]

    k_UnpackBundle_Succeeded: CMsgClientToGCUnpackBundleResponse.EUnpackBundle
    k_UnpackBundle_Failed_ItemIsNotBundle: CMsgClientToGCUnpackBundleResponse.EUnpackBundle
    k_UnpackBundle_Failed_UnableToCreateContainedItem: (
        CMsgClientToGCUnpackBundleResponse.EUnpackBundle
    )
    k_UnpackBundle_Failed_SOCacheError: CMsgClientToGCUnpackBundleResponse.EUnpackBundle
    k_UnpackBundle_Failed_ItemIsInvalid: CMsgClientToGCUnpackBundleResponse.EUnpackBundle
    k_UnpackBundle_Failed_BadItemQuantity: CMsgClientToGCUnpackBundleResponse.EUnpackBundle
    k_UnpackBundle_Failed_UnableToDeleteItem: CMsgClientToGCUnpackBundleResponse.EUnpackBundle
    UNPACKED_ITEM_IDS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    UNPACKED_ITEM_DEF_INDEXES_FIELD_NUMBER: _ClassVar[int]
    unpacked_item_ids: _containers.RepeatedScalarFieldContainer[int]
    response: CMsgClientToGCUnpackBundleResponse.EUnpackBundle
    unpacked_item_def_indexes: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        unpacked_item_ids: _Iterable[int] | None = ...,
        response: CMsgClientToGCUnpackBundleResponse.EUnpackBundle | str | None = ...,
        unpacked_item_def_indexes: _Iterable[int] | None = ...,
    ) -> None: ...

class CMsgClientToGCPackBundle(_message.Message):
    __slots__ = ("item_ids", "bundle_item_def_index")
    ITEM_IDS_FIELD_NUMBER: _ClassVar[int]
    BUNDLE_ITEM_DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
    item_ids: _containers.RepeatedScalarFieldContainer[int]
    bundle_item_def_index: int
    def __init__(
        self, item_ids: _Iterable[int] | None = ..., bundle_item_def_index: int | None = ...
    ) -> None: ...

class CMsgClientToGCPackBundleResponse(_message.Message):
    __slots__ = ("item_id", "response")
    class EPackBundle(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_PackBundle_Succeeded: _ClassVar[CMsgClientToGCPackBundleResponse.EPackBundle]
        k_PackBundle_Failed_InternalError: _ClassVar[CMsgClientToGCPackBundleResponse.EPackBundle]
        k_PackBundle_Failed_ItemIsNotBundle: _ClassVar[CMsgClientToGCPackBundleResponse.EPackBundle]
        k_PackBundle_Failed_SOCacheError: _ClassVar[CMsgClientToGCPackBundleResponse.EPackBundle]
        k_PackBundle_Failed_ItemIsInvalid: _ClassVar[CMsgClientToGCPackBundleResponse.EPackBundle]
        k_PackBundle_Failed_BadItemQuantity: _ClassVar[CMsgClientToGCPackBundleResponse.EPackBundle]
        k_PackBundle_Failed_UnableToDeleteItem: _ClassVar[
            CMsgClientToGCPackBundleResponse.EPackBundle
        ]
        k_PackBundle_Failed_BundleCannotBePacked: _ClassVar[
            CMsgClientToGCPackBundleResponse.EPackBundle
        ]
        k_PackBundle_Failed_ItemIsUntradeable: _ClassVar[
            CMsgClientToGCPackBundleResponse.EPackBundle
        ]
        k_PackBundle_Failed_ItemIsEquipped: _ClassVar[CMsgClientToGCPackBundleResponse.EPackBundle]
        k_PackBundle_Failed_ItemHasGems: _ClassVar[CMsgClientToGCPackBundleResponse.EPackBundle]
        k_PackBundle_Failed_ItemMixedQuality: _ClassVar[
            CMsgClientToGCPackBundleResponse.EPackBundle
        ]
        k_PackBundle_Failed_ItemInvalidQuality: _ClassVar[
            CMsgClientToGCPackBundleResponse.EPackBundle
        ]
        k_PackBundle_Failed_ItemIsNonEconomy: _ClassVar[
            CMsgClientToGCPackBundleResponse.EPackBundle
        ]
        k_PackBundle_Failed_Disabled: _ClassVar[CMsgClientToGCPackBundleResponse.EPackBundle]

    k_PackBundle_Succeeded: CMsgClientToGCPackBundleResponse.EPackBundle
    k_PackBundle_Failed_InternalError: CMsgClientToGCPackBundleResponse.EPackBundle
    k_PackBundle_Failed_ItemIsNotBundle: CMsgClientToGCPackBundleResponse.EPackBundle
    k_PackBundle_Failed_SOCacheError: CMsgClientToGCPackBundleResponse.EPackBundle
    k_PackBundle_Failed_ItemIsInvalid: CMsgClientToGCPackBundleResponse.EPackBundle
    k_PackBundle_Failed_BadItemQuantity: CMsgClientToGCPackBundleResponse.EPackBundle
    k_PackBundle_Failed_UnableToDeleteItem: CMsgClientToGCPackBundleResponse.EPackBundle
    k_PackBundle_Failed_BundleCannotBePacked: CMsgClientToGCPackBundleResponse.EPackBundle
    k_PackBundle_Failed_ItemIsUntradeable: CMsgClientToGCPackBundleResponse.EPackBundle
    k_PackBundle_Failed_ItemIsEquipped: CMsgClientToGCPackBundleResponse.EPackBundle
    k_PackBundle_Failed_ItemHasGems: CMsgClientToGCPackBundleResponse.EPackBundle
    k_PackBundle_Failed_ItemMixedQuality: CMsgClientToGCPackBundleResponse.EPackBundle
    k_PackBundle_Failed_ItemInvalidQuality: CMsgClientToGCPackBundleResponse.EPackBundle
    k_PackBundle_Failed_ItemIsNonEconomy: CMsgClientToGCPackBundleResponse.EPackBundle
    k_PackBundle_Failed_Disabled: CMsgClientToGCPackBundleResponse.EPackBundle
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    response: CMsgClientToGCPackBundleResponse.EPackBundle
    def __init__(
        self,
        item_id: int | None = ...,
        response: CMsgClientToGCPackBundleResponse.EPackBundle | str | None = ...,
    ) -> None: ...

class CMsgGCToClientStoreTransactionCompleted(_message.Message):
    __slots__ = ("txn_id", "item_ids")
    TXN_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_IDS_FIELD_NUMBER: _ClassVar[int]
    txn_id: int
    item_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, txn_id: int | None = ..., item_ids: _Iterable[int] | None = ...) -> None: ...

class CMsgClientToGCEquipItems(_message.Message):
    __slots__ = ("equips",)
    EQUIPS_FIELD_NUMBER: _ClassVar[int]
    equips: _containers.RepeatedCompositeFieldContainer[CMsgAdjustItemEquippedState]
    def __init__(
        self, equips: _Iterable[CMsgAdjustItemEquippedState | _Mapping] | None = ...
    ) -> None: ...

class CMsgClientToGCEquipItemsResponse(_message.Message):
    __slots__ = ("so_cache_version_id",)
    SO_CACHE_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    so_cache_version_id: int
    def __init__(self, so_cache_version_id: int | None = ...) -> None: ...

class CMsgClientToGCSetItemStyle(_message.Message):
    __slots__ = ("item_id", "style_index")
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    STYLE_INDEX_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    style_index: int
    def __init__(self, item_id: int | None = ..., style_index: int | None = ...) -> None: ...

class CMsgClientToGCSetItemStyleResponse(_message.Message):
    __slots__ = ("response",)
    class ESetStyle(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_SetStyle_Succeeded: _ClassVar[CMsgClientToGCSetItemStyleResponse.ESetStyle]
        k_SetStyle_Failed: _ClassVar[CMsgClientToGCSetItemStyleResponse.ESetStyle]
        k_SetStyle_Failed_StyleIsLocked: _ClassVar[CMsgClientToGCSetItemStyleResponse.ESetStyle]

    k_SetStyle_Succeeded: CMsgClientToGCSetItemStyleResponse.ESetStyle
    k_SetStyle_Failed: CMsgClientToGCSetItemStyleResponse.ESetStyle
    k_SetStyle_Failed_StyleIsLocked: CMsgClientToGCSetItemStyleResponse.ESetStyle
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCSetItemStyleResponse.ESetStyle
    def __init__(
        self, response: CMsgClientToGCSetItemStyleResponse.ESetStyle | str | None = ...
    ) -> None: ...

class CMsgClientToGCUnlockItemStyle(_message.Message):
    __slots__ = ("item_to_unlock", "style_index", "consumable_item_ids")
    ITEM_TO_UNLOCK_FIELD_NUMBER: _ClassVar[int]
    STYLE_INDEX_FIELD_NUMBER: _ClassVar[int]
    CONSUMABLE_ITEM_IDS_FIELD_NUMBER: _ClassVar[int]
    item_to_unlock: int
    style_index: int
    consumable_item_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        item_to_unlock: int | None = ...,
        style_index: int | None = ...,
        consumable_item_ids: _Iterable[int] | None = ...,
    ) -> None: ...

class CMsgClientToGCUnlockItemStyleResponse(_message.Message):
    __slots__ = ("response", "item_id", "style_index", "style_prereq")
    class EUnlockStyle(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_UnlockStyle_Succeeded: _ClassVar[CMsgClientToGCUnlockItemStyleResponse.EUnlockStyle]
        k_UnlockStyle_Failed_PreReq: _ClassVar[CMsgClientToGCUnlockItemStyleResponse.EUnlockStyle]
        k_UnlockStyle_Failed_CantAfford: _ClassVar[
            CMsgClientToGCUnlockItemStyleResponse.EUnlockStyle
        ]
        k_UnlockStyle_Failed_CantCommit: _ClassVar[
            CMsgClientToGCUnlockItemStyleResponse.EUnlockStyle
        ]
        k_UnlockStyle_Failed_CantLockCache: _ClassVar[
            CMsgClientToGCUnlockItemStyleResponse.EUnlockStyle
        ]
        k_UnlockStyle_Failed_CantAffordAttrib: _ClassVar[
            CMsgClientToGCUnlockItemStyleResponse.EUnlockStyle
        ]
        k_UnlockStyle_Failed_CantAffordGem: _ClassVar[
            CMsgClientToGCUnlockItemStyleResponse.EUnlockStyle
        ]
        k_UnlockStyle_Failed_NoCompendiumLevel: _ClassVar[
            CMsgClientToGCUnlockItemStyleResponse.EUnlockStyle
        ]
        k_UnlockStyle_Failed_AlreadyUnlocked: _ClassVar[
            CMsgClientToGCUnlockItemStyleResponse.EUnlockStyle
        ]
        k_UnlockStyle_Failed_OtherError: _ClassVar[
            CMsgClientToGCUnlockItemStyleResponse.EUnlockStyle
        ]
        k_UnlockStyle_Failed_ItemIsInvalid: _ClassVar[
            CMsgClientToGCUnlockItemStyleResponse.EUnlockStyle
        ]
        k_UnlockStyle_Failed_ToolIsInvalid: _ClassVar[
            CMsgClientToGCUnlockItemStyleResponse.EUnlockStyle
        ]

    k_UnlockStyle_Succeeded: CMsgClientToGCUnlockItemStyleResponse.EUnlockStyle
    k_UnlockStyle_Failed_PreReq: CMsgClientToGCUnlockItemStyleResponse.EUnlockStyle
    k_UnlockStyle_Failed_CantAfford: CMsgClientToGCUnlockItemStyleResponse.EUnlockStyle
    k_UnlockStyle_Failed_CantCommit: CMsgClientToGCUnlockItemStyleResponse.EUnlockStyle
    k_UnlockStyle_Failed_CantLockCache: CMsgClientToGCUnlockItemStyleResponse.EUnlockStyle
    k_UnlockStyle_Failed_CantAffordAttrib: CMsgClientToGCUnlockItemStyleResponse.EUnlockStyle
    k_UnlockStyle_Failed_CantAffordGem: CMsgClientToGCUnlockItemStyleResponse.EUnlockStyle
    k_UnlockStyle_Failed_NoCompendiumLevel: CMsgClientToGCUnlockItemStyleResponse.EUnlockStyle
    k_UnlockStyle_Failed_AlreadyUnlocked: CMsgClientToGCUnlockItemStyleResponse.EUnlockStyle
    k_UnlockStyle_Failed_OtherError: CMsgClientToGCUnlockItemStyleResponse.EUnlockStyle
    k_UnlockStyle_Failed_ItemIsInvalid: CMsgClientToGCUnlockItemStyleResponse.EUnlockStyle
    k_UnlockStyle_Failed_ToolIsInvalid: CMsgClientToGCUnlockItemStyleResponse.EUnlockStyle
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    STYLE_INDEX_FIELD_NUMBER: _ClassVar[int]
    STYLE_PREREQ_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCUnlockItemStyleResponse.EUnlockStyle
    item_id: int
    style_index: int
    style_prereq: int
    def __init__(
        self,
        response: CMsgClientToGCUnlockItemStyleResponse.EUnlockStyle | str | None = ...,
        item_id: int | None = ...,
        style_index: int | None = ...,
        style_prereq: int | None = ...,
    ) -> None: ...

class CMsgClientToGCSetItemInventoryCategory(_message.Message):
    __slots__ = ("item_ids", "set_to_value", "remove_categories", "add_categories")
    ITEM_IDS_FIELD_NUMBER: _ClassVar[int]
    SET_TO_VALUE_FIELD_NUMBER: _ClassVar[int]
    REMOVE_CATEGORIES_FIELD_NUMBER: _ClassVar[int]
    ADD_CATEGORIES_FIELD_NUMBER: _ClassVar[int]
    item_ids: _containers.RepeatedScalarFieldContainer[int]
    set_to_value: int
    remove_categories: int
    add_categories: int
    def __init__(
        self,
        item_ids: _Iterable[int] | None = ...,
        set_to_value: int | None = ...,
        remove_categories: int | None = ...,
        add_categories: int | None = ...,
    ) -> None: ...

class CMsgClientToGCUnlockCrate(_message.Message):
    __slots__ = ("crate_item_id", "key_item_id")
    CRATE_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    KEY_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    crate_item_id: int
    key_item_id: int
    def __init__(self, crate_item_id: int | None = ..., key_item_id: int | None = ...) -> None: ...

class CMsgClientToGCUnlockCrateResponse(_message.Message):
    __slots__ = ("result", "granted_items")
    class Item(_message.Message):
        __slots__ = ("item_id", "def_index")
        ITEM_ID_FIELD_NUMBER: _ClassVar[int]
        DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
        item_id: int
        def_index: int
        def __init__(self, item_id: int | None = ..., def_index: int | None = ...) -> None: ...

    RESULT_FIELD_NUMBER: _ClassVar[int]
    GRANTED_ITEMS_FIELD_NUMBER: _ClassVar[int]
    result: _econ_shared_enums_pb2.EGCMsgResponse
    granted_items: _containers.RepeatedCompositeFieldContainer[
        CMsgClientToGCUnlockCrateResponse.Item
    ]
    def __init__(
        self,
        result: _econ_shared_enums_pb2.EGCMsgResponse | str | None = ...,
        granted_items: _Iterable[CMsgClientToGCUnlockCrateResponse.Item | _Mapping] | None = ...,
    ) -> None: ...

class CMsgClientToGCRemoveItemAttribute(_message.Message):
    __slots__ = ("item_id",)
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    def __init__(self, item_id: int | None = ...) -> None: ...

class CMsgClientToGCRemoveItemAttributeResponse(_message.Message):
    __slots__ = ("response", "item_id")
    class ERemoveItemAttribute(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_RemoveItemAttribute_Succeeded: _ClassVar[
            CMsgClientToGCRemoveItemAttributeResponse.ERemoveItemAttribute
        ]
        k_RemoveItemAttribute_Failed: _ClassVar[
            CMsgClientToGCRemoveItemAttributeResponse.ERemoveItemAttribute
        ]
        k_RemoveItemAttribute_Failed_ItemIsInvalid: _ClassVar[
            CMsgClientToGCRemoveItemAttributeResponse.ERemoveItemAttribute
        ]
        k_RemoveItemAttribute_Failed_AttributeCannotBeRemoved: _ClassVar[
            CMsgClientToGCRemoveItemAttributeResponse.ERemoveItemAttribute
        ]
        k_RemoveItemAttribute_Failed_AttributeDoesntExist: _ClassVar[
            CMsgClientToGCRemoveItemAttributeResponse.ERemoveItemAttribute
        ]

    k_RemoveItemAttribute_Succeeded: CMsgClientToGCRemoveItemAttributeResponse.ERemoveItemAttribute
    k_RemoveItemAttribute_Failed: CMsgClientToGCRemoveItemAttributeResponse.ERemoveItemAttribute
    k_RemoveItemAttribute_Failed_ItemIsInvalid: (
        CMsgClientToGCRemoveItemAttributeResponse.ERemoveItemAttribute
    )
    k_RemoveItemAttribute_Failed_AttributeCannotBeRemoved: (
        CMsgClientToGCRemoveItemAttributeResponse.ERemoveItemAttribute
    )
    k_RemoveItemAttribute_Failed_AttributeDoesntExist: (
        CMsgClientToGCRemoveItemAttributeResponse.ERemoveItemAttribute
    )
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCRemoveItemAttributeResponse.ERemoveItemAttribute
    item_id: int
    def __init__(
        self,
        response: CMsgClientToGCRemoveItemAttributeResponse.ERemoveItemAttribute | str | None = ...,
        item_id: int | None = ...,
    ) -> None: ...

class CMsgClientToGCNameItem(_message.Message):
    __slots__ = ("subject_item_id", "tool_item_id", "name")
    SUBJECT_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    TOOL_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    subject_item_id: int
    tool_item_id: int
    name: str
    def __init__(
        self,
        subject_item_id: int | None = ...,
        tool_item_id: int | None = ...,
        name: str | None = ...,
    ) -> None: ...

class CMsgClientToGCNameItemResponse(_message.Message):
    __slots__ = ("response", "item_id")
    class ENameItem(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_NameItem_Succeeded: _ClassVar[CMsgClientToGCNameItemResponse.ENameItem]
        k_NameItem_Failed: _ClassVar[CMsgClientToGCNameItemResponse.ENameItem]
        k_NameItem_Failed_ToolIsInvalid: _ClassVar[CMsgClientToGCNameItemResponse.ENameItem]
        k_NameItem_Failed_ItemIsInvalid: _ClassVar[CMsgClientToGCNameItemResponse.ENameItem]
        k_NameItem_Failed_NameIsInvalid: _ClassVar[CMsgClientToGCNameItemResponse.ENameItem]

    k_NameItem_Succeeded: CMsgClientToGCNameItemResponse.ENameItem
    k_NameItem_Failed: CMsgClientToGCNameItemResponse.ENameItem
    k_NameItem_Failed_ToolIsInvalid: CMsgClientToGCNameItemResponse.ENameItem
    k_NameItem_Failed_ItemIsInvalid: CMsgClientToGCNameItemResponse.ENameItem
    k_NameItem_Failed_NameIsInvalid: CMsgClientToGCNameItemResponse.ENameItem
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCNameItemResponse.ENameItem
    item_id: int
    def __init__(
        self,
        response: CMsgClientToGCNameItemResponse.ENameItem | str | None = ...,
        item_id: int | None = ...,
    ) -> None: ...

class CMsgGCSetItemPosition(_message.Message):
    __slots__ = ("item_id", "new_position")
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_POSITION_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    new_position: int
    def __init__(self, item_id: int | None = ..., new_position: int | None = ...) -> None: ...

class CAttribute_ItemDynamicRecipeComponent(_message.Message):
    __slots__ = (
        "item_def",
        "item_quality",
        "item_flags",
        "attributes_string",
        "item_count",
        "items_fulfilled",
        "item_rarity",
        "lootlist",
        "fulfilled_item_id",
        "associated_item_def",
    )
    ITEM_DEF_FIELD_NUMBER: _ClassVar[int]
    ITEM_QUALITY_FIELD_NUMBER: _ClassVar[int]
    ITEM_FLAGS_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_STRING_FIELD_NUMBER: _ClassVar[int]
    ITEM_COUNT_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FULFILLED_FIELD_NUMBER: _ClassVar[int]
    ITEM_RARITY_FIELD_NUMBER: _ClassVar[int]
    LOOTLIST_FIELD_NUMBER: _ClassVar[int]
    FULFILLED_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    ASSOCIATED_ITEM_DEF_FIELD_NUMBER: _ClassVar[int]
    item_def: int
    item_quality: int
    item_flags: int
    attributes_string: str
    item_count: int
    items_fulfilled: int
    item_rarity: int
    lootlist: str
    fulfilled_item_id: int
    associated_item_def: int
    def __init__(
        self,
        item_def: int | None = ...,
        item_quality: int | None = ...,
        item_flags: int | None = ...,
        attributes_string: str | None = ...,
        item_count: int | None = ...,
        items_fulfilled: int | None = ...,
        item_rarity: int | None = ...,
        lootlist: str | None = ...,
        fulfilled_item_id: int | None = ...,
        associated_item_def: int | None = ...,
    ) -> None: ...

class CProtoItemSocket(_message.Message):
    __slots__ = (
        "item_id",
        "attr_def_index",
        "required_type",
        "required_hero",
        "gem_def_index",
        "not_tradable",
        "required_item_slot",
    )
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    ATTR_DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_HERO_FIELD_NUMBER: _ClassVar[int]
    GEM_DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
    NOT_TRADABLE_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_ITEM_SLOT_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    attr_def_index: int
    required_type: int
    required_hero: str
    gem_def_index: int
    not_tradable: bool
    required_item_slot: str
    def __init__(
        self,
        item_id: int | None = ...,
        attr_def_index: int | None = ...,
        required_type: int | None = ...,
        required_hero: str | None = ...,
        gem_def_index: int | None = ...,
        not_tradable: bool = ...,
        required_item_slot: str | None = ...,
    ) -> None: ...

class CProtoItemSocket_Empty(_message.Message):
    __slots__ = ("socket",)
    SOCKET_FIELD_NUMBER: _ClassVar[int]
    socket: CProtoItemSocket
    def __init__(self, socket: CProtoItemSocket | _Mapping | None = ...) -> None: ...

class CProtoItemSocket_Effect(_message.Message):
    __slots__ = ("socket", "effect")
    SOCKET_FIELD_NUMBER: _ClassVar[int]
    EFFECT_FIELD_NUMBER: _ClassVar[int]
    socket: CProtoItemSocket
    effect: int
    def __init__(
        self, socket: CProtoItemSocket | _Mapping | None = ..., effect: int | None = ...
    ) -> None: ...

class CProtoItemSocket_Color(_message.Message):
    __slots__ = ("socket", "red", "green", "blue")
    SOCKET_FIELD_NUMBER: _ClassVar[int]
    RED_FIELD_NUMBER: _ClassVar[int]
    GREEN_FIELD_NUMBER: _ClassVar[int]
    BLUE_FIELD_NUMBER: _ClassVar[int]
    socket: CProtoItemSocket
    red: int
    green: int
    blue: int
    def __init__(
        self,
        socket: CProtoItemSocket | _Mapping | None = ...,
        red: int | None = ...,
        green: int | None = ...,
        blue: int | None = ...,
    ) -> None: ...

class CProtoItemSocket_Strange(_message.Message):
    __slots__ = ("socket", "strange_type", "strange_value")
    SOCKET_FIELD_NUMBER: _ClassVar[int]
    STRANGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    STRANGE_VALUE_FIELD_NUMBER: _ClassVar[int]
    socket: CProtoItemSocket
    strange_type: int
    strange_value: int
    def __init__(
        self,
        socket: CProtoItemSocket | _Mapping | None = ...,
        strange_type: int | None = ...,
        strange_value: int | None = ...,
    ) -> None: ...

class CProtoItemSocket_Strange_DESERIALIZE_FROM_STRING_ONLY(_message.Message):
    __slots__ = ("socket", "strange_type", "strange_value", "ability_effect")
    SOCKET_FIELD_NUMBER: _ClassVar[int]
    STRANGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    STRANGE_VALUE_FIELD_NUMBER: _ClassVar[int]
    ABILITY_EFFECT_FIELD_NUMBER: _ClassVar[int]
    socket: CProtoItemSocket
    strange_type: int
    strange_value: int
    ability_effect: int
    def __init__(
        self,
        socket: CProtoItemSocket | _Mapping | None = ...,
        strange_type: int | None = ...,
        strange_value: int | None = ...,
        ability_effect: int | None = ...,
    ) -> None: ...

class CProtoItemSocket_Spectator(_message.Message):
    __slots__ = ("socket", "games_viewed", "corporation_id", "league_id", "team_id")
    SOCKET_FIELD_NUMBER: _ClassVar[int]
    GAMES_VIEWED_FIELD_NUMBER: _ClassVar[int]
    CORPORATION_ID_FIELD_NUMBER: _ClassVar[int]
    LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    socket: CProtoItemSocket
    games_viewed: int
    corporation_id: int
    league_id: int
    team_id: int
    def __init__(
        self,
        socket: CProtoItemSocket | _Mapping | None = ...,
        games_viewed: int | None = ...,
        corporation_id: int | None = ...,
        league_id: int | None = ...,
        team_id: int | None = ...,
    ) -> None: ...

class CProtoItemSocket_AssetModifier(_message.Message):
    __slots__ = ("socket", "asset_modifier")
    SOCKET_FIELD_NUMBER: _ClassVar[int]
    ASSET_MODIFIER_FIELD_NUMBER: _ClassVar[int]
    socket: CProtoItemSocket
    asset_modifier: int
    def __init__(
        self, socket: CProtoItemSocket | _Mapping | None = ..., asset_modifier: int | None = ...
    ) -> None: ...

class CProtoItemSocket_AssetModifier_DESERIALIZE_FROM_STRING_ONLY(_message.Message):
    __slots__ = ("socket", "asset_modifier", "anim_modifier", "ability_effect")
    SOCKET_FIELD_NUMBER: _ClassVar[int]
    ASSET_MODIFIER_FIELD_NUMBER: _ClassVar[int]
    ANIM_MODIFIER_FIELD_NUMBER: _ClassVar[int]
    ABILITY_EFFECT_FIELD_NUMBER: _ClassVar[int]
    socket: CProtoItemSocket
    asset_modifier: int
    anim_modifier: int
    ability_effect: int
    def __init__(
        self,
        socket: CProtoItemSocket | _Mapping | None = ...,
        asset_modifier: int | None = ...,
        anim_modifier: int | None = ...,
        ability_effect: int | None = ...,
    ) -> None: ...

class CProtoItemSocket_Autograph(_message.Message):
    __slots__ = ("socket", "autograph", "autograph_id", "autograph_score")
    SOCKET_FIELD_NUMBER: _ClassVar[int]
    AUTOGRAPH_FIELD_NUMBER: _ClassVar[int]
    AUTOGRAPH_ID_FIELD_NUMBER: _ClassVar[int]
    AUTOGRAPH_SCORE_FIELD_NUMBER: _ClassVar[int]
    socket: CProtoItemSocket
    autograph: str
    autograph_id: int
    autograph_score: int
    def __init__(
        self,
        socket: CProtoItemSocket | _Mapping | None = ...,
        autograph: str | None = ...,
        autograph_id: int | None = ...,
        autograph_score: int | None = ...,
    ) -> None: ...

class CProtoItemSocket_StaticVisuals(_message.Message):
    __slots__ = ("socket",)
    SOCKET_FIELD_NUMBER: _ClassVar[int]
    socket: CProtoItemSocket
    def __init__(self, socket: CProtoItemSocket | _Mapping | None = ...) -> None: ...

class CAttribute_String(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: str | None = ...) -> None: ...

class CWorkshop_GetItemDailyRevenue_Request(_message.Message):
    __slots__ = ("appid", "item_id", "date_start", "date_end")
    APPID_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    DATE_START_FIELD_NUMBER: _ClassVar[int]
    DATE_END_FIELD_NUMBER: _ClassVar[int]
    appid: int
    item_id: int
    date_start: int
    date_end: int
    def __init__(
        self,
        appid: int | None = ...,
        item_id: int | None = ...,
        date_start: int | None = ...,
        date_end: int | None = ...,
    ) -> None: ...

class CWorkshop_GetItemDailyRevenue_Response(_message.Message):
    __slots__ = ("country_revenue",)
    class CountryDailyRevenue(_message.Message):
        __slots__ = ("country_code", "date", "revenue_usd", "units")
        COUNTRY_CODE_FIELD_NUMBER: _ClassVar[int]
        DATE_FIELD_NUMBER: _ClassVar[int]
        REVENUE_USD_FIELD_NUMBER: _ClassVar[int]
        UNITS_FIELD_NUMBER: _ClassVar[int]
        country_code: str
        date: int
        revenue_usd: int
        units: int
        def __init__(
            self,
            country_code: str | None = ...,
            date: int | None = ...,
            revenue_usd: int | None = ...,
            units: int | None = ...,
        ) -> None: ...

    COUNTRY_REVENUE_FIELD_NUMBER: _ClassVar[int]
    country_revenue: _containers.RepeatedCompositeFieldContainer[
        CWorkshop_GetItemDailyRevenue_Response.CountryDailyRevenue
    ]
    def __init__(
        self,
        country_revenue: _Iterable[
            CWorkshop_GetItemDailyRevenue_Response.CountryDailyRevenue | _Mapping
        ]
        | None = ...,
    ) -> None: ...

class CWorkshop_GetPackageDailyRevenue_Request(_message.Message):
    __slots__ = ("packageid", "date_start", "date_end")
    PACKAGEID_FIELD_NUMBER: _ClassVar[int]
    DATE_START_FIELD_NUMBER: _ClassVar[int]
    DATE_END_FIELD_NUMBER: _ClassVar[int]
    packageid: int
    date_start: int
    date_end: int
    def __init__(
        self, packageid: int | None = ..., date_start: int | None = ..., date_end: int | None = ...
    ) -> None: ...

class CWorkshop_GetPackageDailyRevenue_Response(_message.Message):
    __slots__ = ("country_revenue",)
    class CountryDailyRevenue(_message.Message):
        __slots__ = ("country_code", "date", "revenue_usd", "units")
        COUNTRY_CODE_FIELD_NUMBER: _ClassVar[int]
        DATE_FIELD_NUMBER: _ClassVar[int]
        REVENUE_USD_FIELD_NUMBER: _ClassVar[int]
        UNITS_FIELD_NUMBER: _ClassVar[int]
        country_code: str
        date: int
        revenue_usd: int
        units: int
        def __init__(
            self,
            country_code: str | None = ...,
            date: int | None = ...,
            revenue_usd: int | None = ...,
            units: int | None = ...,
        ) -> None: ...

    COUNTRY_REVENUE_FIELD_NUMBER: _ClassVar[int]
    country_revenue: _containers.RepeatedCompositeFieldContainer[
        CWorkshop_GetPackageDailyRevenue_Response.CountryDailyRevenue
    ]
    def __init__(
        self,
        country_revenue: _Iterable[
            CWorkshop_GetPackageDailyRevenue_Response.CountryDailyRevenue | _Mapping
        ]
        | None = ...,
    ) -> None: ...

class CMsgSQLGCToGCGrantBackpackSlots(_message.Message):
    __slots__ = ("account_id", "add_slots")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ADD_SLOTS_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    add_slots: int
    def __init__(self, account_id: int | None = ..., add_slots: int | None = ...) -> None: ...

class CMsgClientToGCLookupAccountName(_message.Message):
    __slots__ = ("account_id",)
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    def __init__(self, account_id: int | None = ...) -> None: ...

class CMsgClientToGCLookupAccountNameResponse(_message.Message):
    __slots__ = ("account_id", "account_name")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_NAME_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    account_name: str
    def __init__(self, account_id: int | None = ..., account_name: str | None = ...) -> None: ...

class CMsgClientToGCCreateStaticRecipe(_message.Message):
    __slots__ = ("items", "recipe_def_index")
    class Item(_message.Message):
        __slots__ = ("item_id", "slot_id")
        ITEM_ID_FIELD_NUMBER: _ClassVar[int]
        SLOT_ID_FIELD_NUMBER: _ClassVar[int]
        item_id: int
        slot_id: int
        def __init__(self, item_id: int | None = ..., slot_id: int | None = ...) -> None: ...

    ITEMS_FIELD_NUMBER: _ClassVar[int]
    RECIPE_DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[CMsgClientToGCCreateStaticRecipe.Item]
    recipe_def_index: int
    def __init__(
        self,
        items: _Iterable[CMsgClientToGCCreateStaticRecipe.Item | _Mapping] | None = ...,
        recipe_def_index: int | None = ...,
    ) -> None: ...

class CMsgClientToGCCreateStaticRecipeResponse(_message.Message):
    __slots__ = ("response", "output_items", "input_errors", "additional_outputs")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        eResponse_Success: _ClassVar[CMsgClientToGCCreateStaticRecipeResponse.EResponse]
        eResponse_OfferingDisabled: _ClassVar[CMsgClientToGCCreateStaticRecipeResponse.EResponse]
        eResponse_InvalidItems: _ClassVar[CMsgClientToGCCreateStaticRecipeResponse.EResponse]
        eResponse_InternalError: _ClassVar[CMsgClientToGCCreateStaticRecipeResponse.EResponse]
        eResponse_MissingLeague: _ClassVar[CMsgClientToGCCreateStaticRecipeResponse.EResponse]
        eResponse_MissingEvent: _ClassVar[CMsgClientToGCCreateStaticRecipeResponse.EResponse]

    eResponse_Success: CMsgClientToGCCreateStaticRecipeResponse.EResponse
    eResponse_OfferingDisabled: CMsgClientToGCCreateStaticRecipeResponse.EResponse
    eResponse_InvalidItems: CMsgClientToGCCreateStaticRecipeResponse.EResponse
    eResponse_InternalError: CMsgClientToGCCreateStaticRecipeResponse.EResponse
    eResponse_MissingLeague: CMsgClientToGCCreateStaticRecipeResponse.EResponse
    eResponse_MissingEvent: CMsgClientToGCCreateStaticRecipeResponse.EResponse
    class OutputItem(_message.Message):
        __slots__ = ("def_index", "item_id", "slot_id")
        DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
        ITEM_ID_FIELD_NUMBER: _ClassVar[int]
        SLOT_ID_FIELD_NUMBER: _ClassVar[int]
        def_index: int
        item_id: int
        slot_id: int
        def __init__(
            self, def_index: int | None = ..., item_id: int | None = ..., slot_id: int | None = ...
        ) -> None: ...

    class InputError(_message.Message):
        __slots__ = ("slot_id", "error")
        SLOT_ID_FIELD_NUMBER: _ClassVar[int]
        ERROR_FIELD_NUMBER: _ClassVar[int]
        slot_id: int
        error: CMsgClientToGCCreateStaticRecipeResponse.EResponse
        def __init__(
            self,
            slot_id: int | None = ...,
            error: CMsgClientToGCCreateStaticRecipeResponse.EResponse | str | None = ...,
        ) -> None: ...

    class AdditionalOutput(_message.Message):
        __slots__ = ("slot_id", "value")
        SLOT_ID_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        slot_id: int
        value: int
        def __init__(self, slot_id: int | None = ..., value: int | None = ...) -> None: ...

    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_ITEMS_FIELD_NUMBER: _ClassVar[int]
    INPUT_ERRORS_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCCreateStaticRecipeResponse.EResponse
    output_items: _containers.RepeatedCompositeFieldContainer[
        CMsgClientToGCCreateStaticRecipeResponse.OutputItem
    ]
    input_errors: _containers.RepeatedCompositeFieldContainer[
        CMsgClientToGCCreateStaticRecipeResponse.InputError
    ]
    additional_outputs: _containers.RepeatedCompositeFieldContainer[
        CMsgClientToGCCreateStaticRecipeResponse.AdditionalOutput
    ]
    def __init__(
        self,
        response: CMsgClientToGCCreateStaticRecipeResponse.EResponse | str | None = ...,
        output_items: _Iterable[CMsgClientToGCCreateStaticRecipeResponse.OutputItem | _Mapping]
        | None = ...,
        input_errors: _Iterable[CMsgClientToGCCreateStaticRecipeResponse.InputError | _Mapping]
        | None = ...,
        additional_outputs: _Iterable[
            CMsgClientToGCCreateStaticRecipeResponse.AdditionalOutput | _Mapping
        ]
        | None = ...,
    ) -> None: ...

class CMsgProcessTransactionOrder(_message.Message):
    __slots__ = (
        "txn_id",
        "steam_txn_id",
        "partner_txn_id",
        "steam_id",
        "time_stamp",
        "watermark",
        "purchase_report_status",
        "currency",
        "items",
    )
    class Item(_message.Message):
        __slots__ = (
            "item_def_index",
            "item_price",
            "quantity",
            "category_desc",
            "store_purchase_type",
            "source_reference_id",
            "parent_stack_index",
            "default_price",
            "is_user_facing",
            "price_index",
        )
        ITEM_DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
        ITEM_PRICE_FIELD_NUMBER: _ClassVar[int]
        QUANTITY_FIELD_NUMBER: _ClassVar[int]
        CATEGORY_DESC_FIELD_NUMBER: _ClassVar[int]
        STORE_PURCHASE_TYPE_FIELD_NUMBER: _ClassVar[int]
        SOURCE_REFERENCE_ID_FIELD_NUMBER: _ClassVar[int]
        PARENT_STACK_INDEX_FIELD_NUMBER: _ClassVar[int]
        DEFAULT_PRICE_FIELD_NUMBER: _ClassVar[int]
        IS_USER_FACING_FIELD_NUMBER: _ClassVar[int]
        PRICE_INDEX_FIELD_NUMBER: _ClassVar[int]
        item_def_index: int
        item_price: int
        quantity: int
        category_desc: str
        store_purchase_type: int
        source_reference_id: int
        parent_stack_index: int
        default_price: bool
        is_user_facing: bool
        price_index: int
        def __init__(
            self,
            item_def_index: int | None = ...,
            item_price: int | None = ...,
            quantity: int | None = ...,
            category_desc: str | None = ...,
            store_purchase_type: int | None = ...,
            source_reference_id: int | None = ...,
            parent_stack_index: int | None = ...,
            default_price: bool = ...,
            is_user_facing: bool = ...,
            price_index: int | None = ...,
        ) -> None: ...

    TXN_ID_FIELD_NUMBER: _ClassVar[int]
    STEAM_TXN_ID_FIELD_NUMBER: _ClassVar[int]
    PARTNER_TXN_ID_FIELD_NUMBER: _ClassVar[int]
    STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    TIME_STAMP_FIELD_NUMBER: _ClassVar[int]
    WATERMARK_FIELD_NUMBER: _ClassVar[int]
    PURCHASE_REPORT_STATUS_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    txn_id: int
    steam_txn_id: int
    partner_txn_id: int
    steam_id: int
    time_stamp: int
    watermark: int
    purchase_report_status: int
    currency: int
    items: _containers.RepeatedCompositeFieldContainer[CMsgProcessTransactionOrder.Item]
    def __init__(
        self,
        txn_id: int | None = ...,
        steam_txn_id: int | None = ...,
        partner_txn_id: int | None = ...,
        steam_id: int | None = ...,
        time_stamp: int | None = ...,
        watermark: int | None = ...,
        purchase_report_status: int | None = ...,
        currency: int | None = ...,
        items: _Iterable[CMsgProcessTransactionOrder.Item | _Mapping] | None = ...,
    ) -> None: ...

class CMsgGCToGCStoreProcessCDKeyTransaction(_message.Message):
    __slots__ = ("order", "reason_code", "partner")
    ORDER_FIELD_NUMBER: _ClassVar[int]
    REASON_CODE_FIELD_NUMBER: _ClassVar[int]
    PARTNER_FIELD_NUMBER: _ClassVar[int]
    order: CMsgProcessTransactionOrder
    reason_code: int
    partner: int
    def __init__(
        self,
        order: CMsgProcessTransactionOrder | _Mapping | None = ...,
        reason_code: int | None = ...,
        partner: int | None = ...,
    ) -> None: ...

class CMsgGCToGCStoreProcessCDKeyTransactionResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class CMsgGCToGCStoreProcessSettlement(_message.Message):
    __slots__ = ("order",)
    ORDER_FIELD_NUMBER: _ClassVar[int]
    order: CMsgProcessTransactionOrder
    def __init__(self, order: CMsgProcessTransactionOrder | _Mapping | None = ...) -> None: ...

class CMsgGCToGCStoreProcessSettlementResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class CMsgGCToGCBroadcastConsoleCommand(_message.Message):
    __slots__ = ("con_command", "report_output", "sending_gc", "output_initiator", "sender_source")
    CON_COMMAND_FIELD_NUMBER: _ClassVar[int]
    REPORT_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    SENDING_GC_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_INITIATOR_FIELD_NUMBER: _ClassVar[int]
    SENDER_SOURCE_FIELD_NUMBER: _ClassVar[int]
    con_command: str
    report_output: bool
    sending_gc: int
    output_initiator: str
    sender_source: str
    def __init__(
        self,
        con_command: str | None = ...,
        report_output: bool = ...,
        sending_gc: int | None = ...,
        output_initiator: str | None = ...,
        sender_source: str | None = ...,
    ) -> None: ...

class CMsgGCToGCConsoleOutput(_message.Message):
    __slots__ = ("initiator", "sending_gc", "msgs", "is_last_for_source_job")
    class OutputLine(_message.Message):
        __slots__ = ("text", "spew_level")
        TEXT_FIELD_NUMBER: _ClassVar[int]
        SPEW_LEVEL_FIELD_NUMBER: _ClassVar[int]
        text: str
        spew_level: int
        def __init__(self, text: str | None = ..., spew_level: int | None = ...) -> None: ...

    INITIATOR_FIELD_NUMBER: _ClassVar[int]
    SENDING_GC_FIELD_NUMBER: _ClassVar[int]
    MSGS_FIELD_NUMBER: _ClassVar[int]
    IS_LAST_FOR_SOURCE_JOB_FIELD_NUMBER: _ClassVar[int]
    initiator: str
    sending_gc: int
    msgs: _containers.RepeatedCompositeFieldContainer[CMsgGCToGCConsoleOutput.OutputLine]
    is_last_for_source_job: bool
    def __init__(
        self,
        initiator: str | None = ...,
        sending_gc: int | None = ...,
        msgs: _Iterable[CMsgGCToGCConsoleOutput.OutputLine | _Mapping] | None = ...,
        is_last_for_source_job: bool = ...,
    ) -> None: ...

class CMsgItemAges(_message.Message):
    __slots__ = ("max_item_id_timestamps",)
    class MaxItemIDTimestamp(_message.Message):
        __slots__ = ("timestamp", "max_item_id")
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        MAX_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
        timestamp: int
        max_item_id: int
        def __init__(self, timestamp: int | None = ..., max_item_id: int | None = ...) -> None: ...

    MAX_ITEM_ID_TIMESTAMPS_FIELD_NUMBER: _ClassVar[int]
    max_item_id_timestamps: _containers.RepeatedCompositeFieldContainer[
        CMsgItemAges.MaxItemIDTimestamp
    ]
    def __init__(
        self,
        max_item_id_timestamps: _Iterable[CMsgItemAges.MaxItemIDTimestamp | _Mapping] | None = ...,
    ) -> None: ...

class CMsgGCToGCInternalTestMsg(_message.Message):
    __slots__ = (
        "sending_gc",
        "sender_id",
        "context",
        "message_id",
        "message_body",
        "job_id_source",
        "job_id_target",
    )
    SENDING_GC_FIELD_NUMBER: _ClassVar[int]
    SENDER_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_BODY_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_SOURCE_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_TARGET_FIELD_NUMBER: _ClassVar[int]
    sending_gc: int
    sender_id: int
    context: int
    message_id: int
    message_body: bytes
    job_id_source: int
    job_id_target: int
    def __init__(
        self,
        sending_gc: int | None = ...,
        sender_id: int | None = ...,
        context: int | None = ...,
        message_id: int | None = ...,
        message_body: bytes | None = ...,
        job_id_source: int | None = ...,
        job_id_target: int | None = ...,
    ) -> None: ...

class CMsgGCToGCClientServerVersionsUpdated(_message.Message):
    __slots__ = (
        "client_min_allowed_version",
        "client_active_version",
        "server_active_version",
        "server_deployed_version",
        "what_changed",
    )
    CLIENT_MIN_ALLOWED_VERSION_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ACTIVE_VERSION_FIELD_NUMBER: _ClassVar[int]
    SERVER_ACTIVE_VERSION_FIELD_NUMBER: _ClassVar[int]
    SERVER_DEPLOYED_VERSION_FIELD_NUMBER: _ClassVar[int]
    WHAT_CHANGED_FIELD_NUMBER: _ClassVar[int]
    client_min_allowed_version: int
    client_active_version: int
    server_active_version: int
    server_deployed_version: int
    what_changed: int
    def __init__(
        self,
        client_min_allowed_version: int | None = ...,
        client_active_version: int | None = ...,
        server_active_version: int | None = ...,
        server_deployed_version: int | None = ...,
        what_changed: int | None = ...,
    ) -> None: ...

class CMsgGCToGCBroadcastMessageFromSub(_message.Message):
    __slots__ = ("msg_id", "serialized_msg", "account_id_list", "steam_id_list")
    MSG_ID_FIELD_NUMBER: _ClassVar[int]
    SERIALIZED_MSG_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_LIST_FIELD_NUMBER: _ClassVar[int]
    STEAM_ID_LIST_FIELD_NUMBER: _ClassVar[int]
    msg_id: int
    serialized_msg: bytes
    account_id_list: _containers.RepeatedScalarFieldContainer[int]
    steam_id_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        msg_id: int | None = ...,
        serialized_msg: bytes | None = ...,
        account_id_list: _Iterable[int] | None = ...,
        steam_id_list: _Iterable[int] | None = ...,
    ) -> None: ...

class CMsgGCToClientCurrencyPricePoints(_message.Message):
    __slots__ = ("price_key", "currencies")
    class Currency(_message.Message):
        __slots__ = ("currency_id", "currency_price")
        CURRENCY_ID_FIELD_NUMBER: _ClassVar[int]
        CURRENCY_PRICE_FIELD_NUMBER: _ClassVar[int]
        currency_id: int
        currency_price: _containers.RepeatedScalarFieldContainer[int]
        def __init__(
            self, currency_id: int | None = ..., currency_price: _Iterable[int] | None = ...
        ) -> None: ...

    PRICE_KEY_FIELD_NUMBER: _ClassVar[int]
    CURRENCIES_FIELD_NUMBER: _ClassVar[int]
    price_key: _containers.RepeatedScalarFieldContainer[int]
    currencies: _containers.RepeatedCompositeFieldContainer[
        CMsgGCToClientCurrencyPricePoints.Currency
    ]
    def __init__(
        self,
        price_key: _Iterable[int] | None = ...,
        currencies: _Iterable[CMsgGCToClientCurrencyPricePoints.Currency | _Mapping] | None = ...,
    ) -> None: ...

class CMsgBannedWordList(_message.Message):
    __slots__ = ("version", "banned_words")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    BANNED_WORDS_FIELD_NUMBER: _ClassVar[int]
    version: int
    banned_words: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self, version: int | None = ..., banned_words: _Iterable[str] | None = ...
    ) -> None: ...

class CMsgGCToGCFlushSteamInventoryCache(_message.Message):
    __slots__ = ("keys",)
    class Key(_message.Message):
        __slots__ = ("steamid", "contextid")
        STEAMID_FIELD_NUMBER: _ClassVar[int]
        CONTEXTID_FIELD_NUMBER: _ClassVar[int]
        steamid: int
        contextid: int
        def __init__(self, steamid: int | None = ..., contextid: int | None = ...) -> None: ...

    KEYS_FIELD_NUMBER: _ClassVar[int]
    keys: _containers.RepeatedCompositeFieldContainer[CMsgGCToGCFlushSteamInventoryCache.Key]
    def __init__(
        self, keys: _Iterable[CMsgGCToGCFlushSteamInventoryCache.Key | _Mapping] | None = ...
    ) -> None: ...

class CMsgGCToGCUpdateSubscriptionItems(_message.Message):
    __slots__ = ("account_id", "always_notify")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ALWAYS_NOTIFY_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    always_notify: bool
    def __init__(self, account_id: int | None = ..., always_notify: bool = ...) -> None: ...

class CMsgGCToGCSelfPing(_message.Message):
    __slots__ = ("sample_id",)
    SAMPLE_ID_FIELD_NUMBER: _ClassVar[int]
    sample_id: int
    def __init__(self, sample_id: int | None = ...) -> None: ...

class CMsgGCToGCGetInfuxIntervalStats(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgGCToGCGetInfuxIntervalStatsResponse(_message.Message):
    __slots__ = ("stat_ids", "stat_total", "stat_samples", "stat_max", "sample_duration_ms")
    STAT_IDS_FIELD_NUMBER: _ClassVar[int]
    STAT_TOTAL_FIELD_NUMBER: _ClassVar[int]
    STAT_SAMPLES_FIELD_NUMBER: _ClassVar[int]
    STAT_MAX_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    stat_ids: _containers.RepeatedScalarFieldContainer[int]
    stat_total: _containers.RepeatedScalarFieldContainer[int]
    stat_samples: _containers.RepeatedScalarFieldContainer[int]
    stat_max: _containers.RepeatedScalarFieldContainer[int]
    sample_duration_ms: int
    def __init__(
        self,
        stat_ids: _Iterable[int] | None = ...,
        stat_total: _Iterable[int] | None = ...,
        stat_samples: _Iterable[int] | None = ...,
        stat_max: _Iterable[int] | None = ...,
        sample_duration_ms: int | None = ...,
    ) -> None: ...

class CMsgGCToGCPurchaseSucceeded(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCGetLimitedItemPurchaseQuantity(_message.Message):
    __slots__ = ("item_def",)
    ITEM_DEF_FIELD_NUMBER: _ClassVar[int]
    item_def: int
    def __init__(self, item_def: int | None = ...) -> None: ...

class CMsgClientToGCGetLimitedItemPurchaseQuantityResponse(_message.Message):
    __slots__ = ("result", "quantity_purchased")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCGetLimitedItemPurchaseQuantityResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCGetLimitedItemPurchaseQuantityResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCGetLimitedItemPurchaseQuantityResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCGetLimitedItemPurchaseQuantityResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCGetLimitedItemPurchaseQuantityResponse.EResponse]
        k_eInvalidItemDef: _ClassVar[CMsgClientToGCGetLimitedItemPurchaseQuantityResponse.EResponse]
        k_eItemDefNotLimited: _ClassVar[
            CMsgClientToGCGetLimitedItemPurchaseQuantityResponse.EResponse
        ]

    k_eInternalError: CMsgClientToGCGetLimitedItemPurchaseQuantityResponse.EResponse
    k_eSuccess: CMsgClientToGCGetLimitedItemPurchaseQuantityResponse.EResponse
    k_eTooBusy: CMsgClientToGCGetLimitedItemPurchaseQuantityResponse.EResponse
    k_eDisabled: CMsgClientToGCGetLimitedItemPurchaseQuantityResponse.EResponse
    k_eTimeout: CMsgClientToGCGetLimitedItemPurchaseQuantityResponse.EResponse
    k_eInvalidItemDef: CMsgClientToGCGetLimitedItemPurchaseQuantityResponse.EResponse
    k_eItemDefNotLimited: CMsgClientToGCGetLimitedItemPurchaseQuantityResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_PURCHASED_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCGetLimitedItemPurchaseQuantityResponse.EResponse
    quantity_purchased: int
    def __init__(
        self,
        result: CMsgClientToGCGetLimitedItemPurchaseQuantityResponse.EResponse | str | None = ...,
        quantity_purchased: int | None = ...,
    ) -> None: ...

class CMsgClientToGCGetInFlightItemCharges(_message.Message):
    __slots__ = ("item_def",)
    ITEM_DEF_FIELD_NUMBER: _ClassVar[int]
    item_def: int
    def __init__(self, item_def: int | None = ...) -> None: ...

class CMsgClientToGCGetInFlightItemChargesResponse(_message.Message):
    __slots__ = ("result", "charges_in_flight")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCGetInFlightItemChargesResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCGetInFlightItemChargesResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCGetInFlightItemChargesResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCGetInFlightItemChargesResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCGetInFlightItemChargesResponse.EResponse]
        k_eInvalidItemDef: _ClassVar[CMsgClientToGCGetInFlightItemChargesResponse.EResponse]

    k_eInternalError: CMsgClientToGCGetInFlightItemChargesResponse.EResponse
    k_eSuccess: CMsgClientToGCGetInFlightItemChargesResponse.EResponse
    k_eTooBusy: CMsgClientToGCGetInFlightItemChargesResponse.EResponse
    k_eDisabled: CMsgClientToGCGetInFlightItemChargesResponse.EResponse
    k_eTimeout: CMsgClientToGCGetInFlightItemChargesResponse.EResponse
    k_eInvalidItemDef: CMsgClientToGCGetInFlightItemChargesResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    CHARGES_IN_FLIGHT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCGetInFlightItemChargesResponse.EResponse
    charges_in_flight: int
    def __init__(
        self,
        result: CMsgClientToGCGetInFlightItemChargesResponse.EResponse | str | None = ...,
        charges_in_flight: int | None = ...,
    ) -> None: ...

class CMsgClientToGCPurchaseChargeCostItems(_message.Message):
    __slots__ = ("items", "currency")
    class Item(_message.Message):
        __slots__ = ("item_def_index", "quantity", "source_reference_id", "price_index")
        ITEM_DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
        QUANTITY_FIELD_NUMBER: _ClassVar[int]
        SOURCE_REFERENCE_ID_FIELD_NUMBER: _ClassVar[int]
        PRICE_INDEX_FIELD_NUMBER: _ClassVar[int]
        item_def_index: int
        quantity: int
        source_reference_id: int
        price_index: int
        def __init__(
            self,
            item_def_index: int | None = ...,
            quantity: int | None = ...,
            source_reference_id: int | None = ...,
            price_index: int | None = ...,
        ) -> None: ...

    ITEMS_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[CMsgClientToGCPurchaseChargeCostItems.Item]
    currency: int
    def __init__(
        self,
        items: _Iterable[CMsgClientToGCPurchaseChargeCostItems.Item | _Mapping] | None = ...,
        currency: int | None = ...,
    ) -> None: ...

class CMsgClientToGCPurchaseChargeCostItemsResponse(_message.Message):
    __slots__ = ("result", "item_ids")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCPurchaseChargeCostItemsResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCPurchaseChargeCostItemsResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCPurchaseChargeCostItemsResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCPurchaseChargeCostItemsResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCPurchaseChargeCostItemsResponse.EResponse]
        k_eInvalidParam: _ClassVar[CMsgClientToGCPurchaseChargeCostItemsResponse.EResponse]
        k_eInvalidPrice: _ClassVar[CMsgClientToGCPurchaseChargeCostItemsResponse.EResponse]
        k_eInsufficientCharges: _ClassVar[CMsgClientToGCPurchaseChargeCostItemsResponse.EResponse]
        k_eLimitedItem: _ClassVar[CMsgClientToGCPurchaseChargeCostItemsResponse.EResponse]
        k_eMissingPrereq: _ClassVar[CMsgClientToGCPurchaseChargeCostItemsResponse.EResponse]

    k_eInternalError: CMsgClientToGCPurchaseChargeCostItemsResponse.EResponse
    k_eSuccess: CMsgClientToGCPurchaseChargeCostItemsResponse.EResponse
    k_eTooBusy: CMsgClientToGCPurchaseChargeCostItemsResponse.EResponse
    k_eDisabled: CMsgClientToGCPurchaseChargeCostItemsResponse.EResponse
    k_eTimeout: CMsgClientToGCPurchaseChargeCostItemsResponse.EResponse
    k_eInvalidParam: CMsgClientToGCPurchaseChargeCostItemsResponse.EResponse
    k_eInvalidPrice: CMsgClientToGCPurchaseChargeCostItemsResponse.EResponse
    k_eInsufficientCharges: CMsgClientToGCPurchaseChargeCostItemsResponse.EResponse
    k_eLimitedItem: CMsgClientToGCPurchaseChargeCostItemsResponse.EResponse
    k_eMissingPrereq: CMsgClientToGCPurchaseChargeCostItemsResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    ITEM_IDS_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCPurchaseChargeCostItemsResponse.EResponse
    item_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        result: CMsgClientToGCPurchaseChargeCostItemsResponse.EResponse | str | None = ...,
        item_ids: _Iterable[int] | None = ...,
    ) -> None: ...

class CMsgGCToClientInFlightChargesUpdated(_message.Message):
    __slots__ = ("in_flight_charges",)
    class ItemCharges(_message.Message):
        __slots__ = ("item_def", "charges_in_flight")
        ITEM_DEF_FIELD_NUMBER: _ClassVar[int]
        CHARGES_IN_FLIGHT_FIELD_NUMBER: _ClassVar[int]
        item_def: int
        charges_in_flight: int
        def __init__(
            self, item_def: int | None = ..., charges_in_flight: int | None = ...
        ) -> None: ...

    IN_FLIGHT_CHARGES_FIELD_NUMBER: _ClassVar[int]
    in_flight_charges: _containers.RepeatedCompositeFieldContainer[
        CMsgGCToClientInFlightChargesUpdated.ItemCharges
    ]
    def __init__(
        self,
        in_flight_charges: _Iterable[CMsgGCToClientInFlightChargesUpdated.ItemCharges | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgClientToGCCancelUnfinalizedTransactions(_message.Message):
    __slots__ = ("unused",)
    UNUSED_FIELD_NUMBER: _ClassVar[int]
    unused: int
    def __init__(self, unused: int | None = ...) -> None: ...

class CMsgClientToGCCancelUnfinalizedTransactionsResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: int
    def __init__(self, result: int | None = ...) -> None: ...

class CMsgGCToGCUpdateWelcomeMsg(_message.Message):
    __slots__ = ("server", "new_msg", "broadcast")
    SERVER_FIELD_NUMBER: _ClassVar[int]
    NEW_MSG_FIELD_NUMBER: _ClassVar[int]
    BROADCAST_FIELD_NUMBER: _ClassVar[int]
    server: bool
    new_msg: _gcsdk_gcmessages_pb2.CExtraMsgBlock
    broadcast: bool
    def __init__(
        self,
        server: bool = ...,
        new_msg: _gcsdk_gcmessages_pb2.CExtraMsgBlock | _Mapping | None = ...,
        broadcast: bool = ...,
    ) -> None: ...

class CMsgClientToGCRecycleMultipleItems(_message.Message):
    __slots__ = ("items",)
    class Item(_message.Message):
        __slots__ = ("item_id", "slot_id", "recipe_def_index")
        ITEM_ID_FIELD_NUMBER: _ClassVar[int]
        SLOT_ID_FIELD_NUMBER: _ClassVar[int]
        RECIPE_DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
        item_id: int
        slot_id: int
        recipe_def_index: int
        def __init__(
            self,
            item_id: int | None = ...,
            slot_id: int | None = ...,
            recipe_def_index: int | None = ...,
        ) -> None: ...

    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[CMsgClientToGCRecycleMultipleItems.Item]
    def __init__(
        self, items: _Iterable[CMsgClientToGCRecycleMultipleItems.Item | _Mapping] | None = ...
    ) -> None: ...

class CMsgClientToGCRecycleMultipleItemsResponse(_message.Message):
    __slots__ = ("responses",)
    RESPONSES_FIELD_NUMBER: _ClassVar[int]
    responses: _containers.RepeatedCompositeFieldContainer[CMsgClientToGCCreateStaticRecipeResponse]
    def __init__(
        self, responses: _Iterable[CMsgClientToGCCreateStaticRecipeResponse | _Mapping] | None = ...
    ) -> None: ...
