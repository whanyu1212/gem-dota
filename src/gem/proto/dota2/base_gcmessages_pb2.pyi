from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

import gcsdk_gcmessages_pb2 as _gcsdk_gcmessages_pb2
import steammessages_pb2 as _steammessages_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from steammessages_steamlearn import steamworkssdk_pb2 as _steamworkssdk_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class EGCBaseMsg(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EMsgGCInviteToParty: _ClassVar[EGCBaseMsg]
    k_EMsgGCInvitationCreated: _ClassVar[EGCBaseMsg]
    k_EMsgGCPartyInviteResponse: _ClassVar[EGCBaseMsg]
    k_EMsgGCKickFromParty: _ClassVar[EGCBaseMsg]
    k_EMsgGCLeaveParty: _ClassVar[EGCBaseMsg]
    k_EMsgGCServerAvailable: _ClassVar[EGCBaseMsg]
    k_EMsgGCClientConnectToServer: _ClassVar[EGCBaseMsg]
    k_EMsgGCGameServerInfo: _ClassVar[EGCBaseMsg]
    k_EMsgGCLANServerAvailable: _ClassVar[EGCBaseMsg]
    k_EMsgGCInviteToLobby: _ClassVar[EGCBaseMsg]
    k_EMsgGCLobbyInviteResponse: _ClassVar[EGCBaseMsg]
    k_EMsgGCToClientPollFileRequest: _ClassVar[EGCBaseMsg]
    k_EMsgGCToClientPollFileResponse: _ClassVar[EGCBaseMsg]
    k_EMsgGCToGCPerformManualOp: _ClassVar[EGCBaseMsg]
    k_EMsgGCToGCPerformManualOpCompleted: _ClassVar[EGCBaseMsg]
    k_EMsgGCToGCReloadServerRegionSettings: _ClassVar[EGCBaseMsg]
    k_EMsgGCAdditionalWelcomeMsgList: _ClassVar[EGCBaseMsg]
    k_EMsgGCToClientApplyRemoteConVars: _ClassVar[EGCBaseMsg]
    k_EMsgGCToServerApplyRemoteConVars: _ClassVar[EGCBaseMsg]
    k_EMsgClientToGCIntegrityStatus: _ClassVar[EGCBaseMsg]
    k_EMsgClientToGCAggregateMetrics: _ClassVar[EGCBaseMsg]
    k_EMsgGCToClientAggregateMetricsBackoff: _ClassVar[EGCBaseMsg]
    k_EMsgGCToServerSteamLearnAccessTokensChanged: _ClassVar[EGCBaseMsg]
    k_EMsgGCToServerSteamLearnUseHTTP: _ClassVar[EGCBaseMsg]

class ECustomGameInstallStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_ECustomGameInstallStatus_Unknown: _ClassVar[ECustomGameInstallStatus]
    k_ECustomGameInstallStatus_Ready: _ClassVar[ECustomGameInstallStatus]
    k_ECustomGameInstallStatus_Busy: _ClassVar[ECustomGameInstallStatus]
    k_ECustomGameInstallStatus_FailedGeneric: _ClassVar[ECustomGameInstallStatus]
    k_ECustomGameInstallStatus_FailedInternalError: _ClassVar[ECustomGameInstallStatus]
    k_ECustomGameInstallStatus_RequestedTimestampTooOld: _ClassVar[ECustomGameInstallStatus]
    k_ECustomGameInstallStatus_RequestedTimestampTooNew: _ClassVar[ECustomGameInstallStatus]
    k_ECustomGameInstallStatus_CRCMismatch: _ClassVar[ECustomGameInstallStatus]
    k_ECustomGameInstallStatus_FailedSteam: _ClassVar[ECustomGameInstallStatus]
    k_ECustomGameInstallStatus_FailedCanceled: _ClassVar[ECustomGameInstallStatus]

k_EMsgGCInviteToParty: EGCBaseMsg
k_EMsgGCInvitationCreated: EGCBaseMsg
k_EMsgGCPartyInviteResponse: EGCBaseMsg
k_EMsgGCKickFromParty: EGCBaseMsg
k_EMsgGCLeaveParty: EGCBaseMsg
k_EMsgGCServerAvailable: EGCBaseMsg
k_EMsgGCClientConnectToServer: EGCBaseMsg
k_EMsgGCGameServerInfo: EGCBaseMsg
k_EMsgGCLANServerAvailable: EGCBaseMsg
k_EMsgGCInviteToLobby: EGCBaseMsg
k_EMsgGCLobbyInviteResponse: EGCBaseMsg
k_EMsgGCToClientPollFileRequest: EGCBaseMsg
k_EMsgGCToClientPollFileResponse: EGCBaseMsg
k_EMsgGCToGCPerformManualOp: EGCBaseMsg
k_EMsgGCToGCPerformManualOpCompleted: EGCBaseMsg
k_EMsgGCToGCReloadServerRegionSettings: EGCBaseMsg
k_EMsgGCAdditionalWelcomeMsgList: EGCBaseMsg
k_EMsgGCToClientApplyRemoteConVars: EGCBaseMsg
k_EMsgGCToServerApplyRemoteConVars: EGCBaseMsg
k_EMsgClientToGCIntegrityStatus: EGCBaseMsg
k_EMsgClientToGCAggregateMetrics: EGCBaseMsg
k_EMsgGCToClientAggregateMetricsBackoff: EGCBaseMsg
k_EMsgGCToServerSteamLearnAccessTokensChanged: EGCBaseMsg
k_EMsgGCToServerSteamLearnUseHTTP: EGCBaseMsg
k_ECustomGameInstallStatus_Unknown: ECustomGameInstallStatus
k_ECustomGameInstallStatus_Ready: ECustomGameInstallStatus
k_ECustomGameInstallStatus_Busy: ECustomGameInstallStatus
k_ECustomGameInstallStatus_FailedGeneric: ECustomGameInstallStatus
k_ECustomGameInstallStatus_FailedInternalError: ECustomGameInstallStatus
k_ECustomGameInstallStatus_RequestedTimestampTooOld: ECustomGameInstallStatus
k_ECustomGameInstallStatus_RequestedTimestampTooNew: ECustomGameInstallStatus
k_ECustomGameInstallStatus_CRCMismatch: ECustomGameInstallStatus
k_ECustomGameInstallStatus_FailedSteam: ECustomGameInstallStatus
k_ECustomGameInstallStatus_FailedCanceled: ECustomGameInstallStatus

class CGCStorePurchaseInit_LineItem(_message.Message):
    __slots__ = (
        "item_def_id",
        "quantity",
        "cost_in_local_currency",
        "purchase_type",
        "source_reference_id",
        "price_index",
    )
    ITEM_DEF_ID_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    COST_IN_LOCAL_CURRENCY_FIELD_NUMBER: _ClassVar[int]
    PURCHASE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_REFERENCE_ID_FIELD_NUMBER: _ClassVar[int]
    PRICE_INDEX_FIELD_NUMBER: _ClassVar[int]
    item_def_id: int
    quantity: int
    cost_in_local_currency: int
    purchase_type: int
    source_reference_id: int
    price_index: int
    def __init__(
        self,
        item_def_id: int | None = ...,
        quantity: int | None = ...,
        cost_in_local_currency: int | None = ...,
        purchase_type: int | None = ...,
        source_reference_id: int | None = ...,
        price_index: int | None = ...,
    ) -> None: ...

class CMsgGCStorePurchaseInit(_message.Message):
    __slots__ = ("country", "language", "currency", "line_items")
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    LINE_ITEMS_FIELD_NUMBER: _ClassVar[int]
    country: str
    language: int
    currency: int
    line_items: _containers.RepeatedCompositeFieldContainer[CGCStorePurchaseInit_LineItem]
    def __init__(
        self,
        country: str | None = ...,
        language: int | None = ...,
        currency: int | None = ...,
        line_items: _Iterable[CGCStorePurchaseInit_LineItem | _Mapping] | None = ...,
    ) -> None: ...

class CMsgGCStorePurchaseInitResponse(_message.Message):
    __slots__ = ("result", "txn_id")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    TXN_ID_FIELD_NUMBER: _ClassVar[int]
    result: int
    txn_id: int
    def __init__(self, result: int | None = ..., txn_id: int | None = ...) -> None: ...

class CMsgClientPingData(_message.Message):
    __slots__ = (
        "relay_codes",
        "relay_pings",
        "region_codes",
        "region_pings",
        "region_ping_failed_bitmask",
    )
    RELAY_CODES_FIELD_NUMBER: _ClassVar[int]
    RELAY_PINGS_FIELD_NUMBER: _ClassVar[int]
    REGION_CODES_FIELD_NUMBER: _ClassVar[int]
    REGION_PINGS_FIELD_NUMBER: _ClassVar[int]
    REGION_PING_FAILED_BITMASK_FIELD_NUMBER: _ClassVar[int]
    relay_codes: _containers.RepeatedScalarFieldContainer[int]
    relay_pings: _containers.RepeatedScalarFieldContainer[int]
    region_codes: _containers.RepeatedScalarFieldContainer[int]
    region_pings: _containers.RepeatedScalarFieldContainer[int]
    region_ping_failed_bitmask: int
    def __init__(
        self,
        relay_codes: _Iterable[int] | None = ...,
        relay_pings: _Iterable[int] | None = ...,
        region_codes: _Iterable[int] | None = ...,
        region_pings: _Iterable[int] | None = ...,
        region_ping_failed_bitmask: int | None = ...,
    ) -> None: ...

class CMsgInviteToParty(_message.Message):
    __slots__ = ("steam_id", "client_version", "team_id", "as_coach", "ping_data")
    STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    AS_COACH_FIELD_NUMBER: _ClassVar[int]
    PING_DATA_FIELD_NUMBER: _ClassVar[int]
    steam_id: int
    client_version: int
    team_id: int
    as_coach: bool
    ping_data: CMsgClientPingData
    def __init__(
        self,
        steam_id: int | None = ...,
        client_version: int | None = ...,
        team_id: int | None = ...,
        as_coach: bool = ...,
        ping_data: CMsgClientPingData | _Mapping | None = ...,
    ) -> None: ...

class CMsgInviteToLobby(_message.Message):
    __slots__ = ("steam_id", "client_version")
    STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    steam_id: int
    client_version: int
    def __init__(self, steam_id: int | None = ..., client_version: int | None = ...) -> None: ...

class CMsgInvitationCreated(_message.Message):
    __slots__ = ("group_id", "steam_id", "user_offline")
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    USER_OFFLINE_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    steam_id: int
    user_offline: bool
    def __init__(
        self, group_id: int | None = ..., steam_id: int | None = ..., user_offline: bool = ...
    ) -> None: ...

class CMsgPartyInviteResponse(_message.Message):
    __slots__ = ("party_id", "accept", "client_version", "ping_data")
    PARTY_ID_FIELD_NUMBER: _ClassVar[int]
    ACCEPT_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    PING_DATA_FIELD_NUMBER: _ClassVar[int]
    party_id: int
    accept: bool
    client_version: int
    ping_data: CMsgClientPingData
    def __init__(
        self,
        party_id: int | None = ...,
        accept: bool = ...,
        client_version: int | None = ...,
        ping_data: CMsgClientPingData | _Mapping | None = ...,
    ) -> None: ...

class CMsgLobbyInviteResponse(_message.Message):
    __slots__ = ("lobby_id", "accept", "client_version", "custom_game_crc", "custom_game_timestamp")
    LOBBY_ID_FIELD_NUMBER: _ClassVar[int]
    ACCEPT_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_CRC_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    lobby_id: int
    accept: bool
    client_version: int
    custom_game_crc: int
    custom_game_timestamp: int
    def __init__(
        self,
        lobby_id: int | None = ...,
        accept: bool = ...,
        client_version: int | None = ...,
        custom_game_crc: int | None = ...,
        custom_game_timestamp: int | None = ...,
    ) -> None: ...

class CMsgKickFromParty(_message.Message):
    __slots__ = ("steam_id",)
    STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    steam_id: int
    def __init__(self, steam_id: int | None = ...) -> None: ...

class CMsgLeaveParty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgCustomGameInstallStatus(_message.Message):
    __slots__ = ("status", "message", "latest_timestamp_from_steam")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LATEST_TIMESTAMP_FROM_STEAM_FIELD_NUMBER: _ClassVar[int]
    status: ECustomGameInstallStatus
    message: str
    latest_timestamp_from_steam: int
    def __init__(
        self,
        status: ECustomGameInstallStatus | str | None = ...,
        message: str | None = ...,
        latest_timestamp_from_steam: int | None = ...,
    ) -> None: ...

class CMsgServerAvailable(_message.Message):
    __slots__ = ("custom_game_install_status",)
    CUSTOM_GAME_INSTALL_STATUS_FIELD_NUMBER: _ClassVar[int]
    custom_game_install_status: CMsgCustomGameInstallStatus
    def __init__(
        self, custom_game_install_status: CMsgCustomGameInstallStatus | _Mapping | None = ...
    ) -> None: ...

class CMsgLANServerAvailable(_message.Message):
    __slots__ = ("lobby_id",)
    LOBBY_ID_FIELD_NUMBER: _ClassVar[int]
    lobby_id: int
    def __init__(self, lobby_id: int | None = ...) -> None: ...

class CSOEconGameAccountClient(_message.Message):
    __slots__ = (
        "additional_backpack_slots",
        "trial_account",
        "eligible_for_online_play",
        "need_to_choose_most_helpful_friend",
        "in_coaches_list",
        "trade_ban_expiration",
        "duel_ban_expiration",
        "made_first_purchase",
    )
    ADDITIONAL_BACKPACK_SLOTS_FIELD_NUMBER: _ClassVar[int]
    TRIAL_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    ELIGIBLE_FOR_ONLINE_PLAY_FIELD_NUMBER: _ClassVar[int]
    NEED_TO_CHOOSE_MOST_HELPFUL_FRIEND_FIELD_NUMBER: _ClassVar[int]
    IN_COACHES_LIST_FIELD_NUMBER: _ClassVar[int]
    TRADE_BAN_EXPIRATION_FIELD_NUMBER: _ClassVar[int]
    DUEL_BAN_EXPIRATION_FIELD_NUMBER: _ClassVar[int]
    MADE_FIRST_PURCHASE_FIELD_NUMBER: _ClassVar[int]
    additional_backpack_slots: int
    trial_account: bool
    eligible_for_online_play: bool
    need_to_choose_most_helpful_friend: bool
    in_coaches_list: bool
    trade_ban_expiration: int
    duel_ban_expiration: int
    made_first_purchase: bool
    def __init__(
        self,
        additional_backpack_slots: int | None = ...,
        trial_account: bool = ...,
        eligible_for_online_play: bool = ...,
        need_to_choose_most_helpful_friend: bool = ...,
        in_coaches_list: bool = ...,
        trade_ban_expiration: int | None = ...,
        duel_ban_expiration: int | None = ...,
        made_first_purchase: bool = ...,
    ) -> None: ...

class CMsgApplyStrangePart(_message.Message):
    __slots__ = ("strange_part_item_id", "item_item_id")
    STRANGE_PART_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    strange_part_item_id: int
    item_item_id: int
    def __init__(
        self, strange_part_item_id: int | None = ..., item_item_id: int | None = ...
    ) -> None: ...

class CMsgApplyPennantUpgrade(_message.Message):
    __slots__ = ("upgrade_item_id", "pennant_item_id")
    UPGRADE_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    PENNANT_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    upgrade_item_id: int
    pennant_item_id: int
    def __init__(
        self, upgrade_item_id: int | None = ..., pennant_item_id: int | None = ...
    ) -> None: ...

class CMsgApplyEggEssence(_message.Message):
    __slots__ = ("essence_item_id", "egg_item_id")
    ESSENCE_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    EGG_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    essence_item_id: int
    egg_item_id: int
    def __init__(
        self, essence_item_id: int | None = ..., egg_item_id: int | None = ...
    ) -> None: ...

class CSOEconItemAttribute(_message.Message):
    __slots__ = ("def_index", "value", "value_bytes")
    DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    VALUE_BYTES_FIELD_NUMBER: _ClassVar[int]
    def_index: int
    value: int
    value_bytes: bytes
    def __init__(
        self, def_index: int | None = ..., value: int | None = ..., value_bytes: bytes | None = ...
    ) -> None: ...

class CSOEconItemEquipped(_message.Message):
    __slots__ = ("new_class", "new_slot")
    NEW_CLASS_FIELD_NUMBER: _ClassVar[int]
    NEW_SLOT_FIELD_NUMBER: _ClassVar[int]
    new_class: int
    new_slot: int
    def __init__(self, new_class: int | None = ..., new_slot: int | None = ...) -> None: ...

class CSOEconItem(_message.Message):
    __slots__ = (
        "id",
        "account_id",
        "inventory",
        "def_index",
        "quantity",
        "level",
        "quality",
        "flags",
        "origin",
        "attribute",
        "interior_item",
        "style",
        "original_id",
        "equipped_state",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    INVENTORY_FIELD_NUMBER: _ClassVar[int]
    DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    QUALITY_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    INTERIOR_ITEM_FIELD_NUMBER: _ClassVar[int]
    STYLE_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_ID_FIELD_NUMBER: _ClassVar[int]
    EQUIPPED_STATE_FIELD_NUMBER: _ClassVar[int]
    id: int
    account_id: int
    inventory: int
    def_index: int
    quantity: int
    level: int
    quality: int
    flags: int
    origin: int
    attribute: _containers.RepeatedCompositeFieldContainer[CSOEconItemAttribute]
    interior_item: CSOEconItem
    style: int
    original_id: int
    equipped_state: _containers.RepeatedCompositeFieldContainer[CSOEconItemEquipped]
    def __init__(
        self,
        id: int | None = ...,
        account_id: int | None = ...,
        inventory: int | None = ...,
        def_index: int | None = ...,
        quantity: int | None = ...,
        level: int | None = ...,
        quality: int | None = ...,
        flags: int | None = ...,
        origin: int | None = ...,
        attribute: _Iterable[CSOEconItemAttribute | _Mapping] | None = ...,
        interior_item: CSOEconItem | _Mapping | None = ...,
        style: int | None = ...,
        original_id: int | None = ...,
        equipped_state: _Iterable[CSOEconItemEquipped | _Mapping] | None = ...,
    ) -> None: ...

class CMsgSortItems(_message.Message):
    __slots__ = ("sort_type",)
    SORT_TYPE_FIELD_NUMBER: _ClassVar[int]
    sort_type: int
    def __init__(self, sort_type: int | None = ...) -> None: ...

class CMsgItemAcknowledged(_message.Message):
    __slots__ = ("account_id", "inventory", "def_index", "quality", "rarity", "origin")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    INVENTORY_FIELD_NUMBER: _ClassVar[int]
    DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
    QUALITY_FIELD_NUMBER: _ClassVar[int]
    RARITY_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    inventory: int
    def_index: int
    quality: int
    rarity: int
    origin: int
    def __init__(
        self,
        account_id: int | None = ...,
        inventory: int | None = ...,
        def_index: int | None = ...,
        quality: int | None = ...,
        rarity: int | None = ...,
        origin: int | None = ...,
    ) -> None: ...

class CMsgSetItemPositions(_message.Message):
    __slots__ = ("item_positions",)
    class ItemPosition(_message.Message):
        __slots__ = ("item_id", "position")
        ITEM_ID_FIELD_NUMBER: _ClassVar[int]
        POSITION_FIELD_NUMBER: _ClassVar[int]
        item_id: int
        position: int
        def __init__(self, item_id: int | None = ..., position: int | None = ...) -> None: ...

    ITEM_POSITIONS_FIELD_NUMBER: _ClassVar[int]
    item_positions: _containers.RepeatedCompositeFieldContainer[CMsgSetItemPositions.ItemPosition]
    def __init__(
        self, item_positions: _Iterable[CMsgSetItemPositions.ItemPosition | _Mapping] | None = ...
    ) -> None: ...

class CMsgGCStorePurchaseCancel(_message.Message):
    __slots__ = ("txn_id",)
    TXN_ID_FIELD_NUMBER: _ClassVar[int]
    txn_id: int
    def __init__(self, txn_id: int | None = ...) -> None: ...

class CMsgGCStorePurchaseCancelResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: int
    def __init__(self, result: int | None = ...) -> None: ...

class CMsgGCStorePurchaseFinalize(_message.Message):
    __slots__ = ("txn_id",)
    TXN_ID_FIELD_NUMBER: _ClassVar[int]
    txn_id: int
    def __init__(self, txn_id: int | None = ...) -> None: ...

class CMsgGCStorePurchaseFinalizeResponse(_message.Message):
    __slots__ = ("result", "item_ids")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    ITEM_IDS_FIELD_NUMBER: _ClassVar[int]
    result: int
    item_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, result: int | None = ..., item_ids: _Iterable[int] | None = ...) -> None: ...

class CMsgGCToGCBannedWordListUpdated(_message.Message):
    __slots__ = ("group_id",)
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    def __init__(self, group_id: int | None = ...) -> None: ...

class CMsgGCToGCDirtySDOCache(_message.Message):
    __slots__ = ("sdo_type", "key_uint64")
    SDO_TYPE_FIELD_NUMBER: _ClassVar[int]
    KEY_UINT64_FIELD_NUMBER: _ClassVar[int]
    sdo_type: int
    key_uint64: int
    def __init__(self, sdo_type: int | None = ..., key_uint64: int | None = ...) -> None: ...

class CMsgSDONoMemcached(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgGCToGCUpdateSQLKeyValue(_message.Message):
    __slots__ = ("key_name",)
    KEY_NAME_FIELD_NUMBER: _ClassVar[int]
    key_name: str
    def __init__(self, key_name: str | None = ...) -> None: ...

class CMsgGCServerVersionUpdated(_message.Message):
    __slots__ = ("server_version",)
    SERVER_VERSION_FIELD_NUMBER: _ClassVar[int]
    server_version: int
    def __init__(self, server_version: int | None = ...) -> None: ...

class CMsgGCClientVersionUpdated(_message.Message):
    __slots__ = ("client_version",)
    CLIENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    client_version: int
    def __init__(self, client_version: int | None = ...) -> None: ...

class CMsgGCToGCWebAPIAccountChanged(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgExtractGems(_message.Message):
    __slots__ = ("tool_item_id", "item_item_id", "item_socket_id")
    TOOL_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_SOCKET_ID_FIELD_NUMBER: _ClassVar[int]
    tool_item_id: int
    item_item_id: int
    item_socket_id: int
    def __init__(
        self,
        tool_item_id: int | None = ...,
        item_item_id: int | None = ...,
        item_socket_id: int | None = ...,
    ) -> None: ...

class CMsgExtractGemsResponse(_message.Message):
    __slots__ = ("item_id", "response")
    class EExtractGems(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_ExtractGems_Succeeded: _ClassVar[CMsgExtractGemsResponse.EExtractGems]
        k_ExtractGems_Failed_ToolIsInvalid: _ClassVar[CMsgExtractGemsResponse.EExtractGems]
        k_ExtractGems_Failed_ItemIsInvalid: _ClassVar[CMsgExtractGemsResponse.EExtractGems]
        k_ExtractGems_Failed_ToolCannotRemoveGem: _ClassVar[CMsgExtractGemsResponse.EExtractGems]
        k_ExtractGems_Failed_FailedToRemoveGem: _ClassVar[CMsgExtractGemsResponse.EExtractGems]

    k_ExtractGems_Succeeded: CMsgExtractGemsResponse.EExtractGems
    k_ExtractGems_Failed_ToolIsInvalid: CMsgExtractGemsResponse.EExtractGems
    k_ExtractGems_Failed_ItemIsInvalid: CMsgExtractGemsResponse.EExtractGems
    k_ExtractGems_Failed_ToolCannotRemoveGem: CMsgExtractGemsResponse.EExtractGems
    k_ExtractGems_Failed_FailedToRemoveGem: CMsgExtractGemsResponse.EExtractGems
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    response: CMsgExtractGemsResponse.EExtractGems
    def __init__(
        self,
        item_id: int | None = ...,
        response: CMsgExtractGemsResponse.EExtractGems | str | None = ...,
    ) -> None: ...

class CMsgAddSocket(_message.Message):
    __slots__ = ("tool_item_id", "item_item_id", "unusual")
    TOOL_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    UNUSUAL_FIELD_NUMBER: _ClassVar[int]
    tool_item_id: int
    item_item_id: int
    unusual: bool
    def __init__(
        self, tool_item_id: int | None = ..., item_item_id: int | None = ..., unusual: bool = ...
    ) -> None: ...

class CMsgAddSocketResponse(_message.Message):
    __slots__ = ("item_id", "updated_socket_index", "response")
    class EAddSocket(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_AddSocket_Succeeded: _ClassVar[CMsgAddSocketResponse.EAddSocket]
        k_AddSocket_Failed_ToolIsInvalid: _ClassVar[CMsgAddSocketResponse.EAddSocket]
        k_AddSocket_Failed_ItemCannotBeSocketed: _ClassVar[CMsgAddSocketResponse.EAddSocket]
        k_AddSocket_Failed_FailedToAddSocket: _ClassVar[CMsgAddSocketResponse.EAddSocket]

    k_AddSocket_Succeeded: CMsgAddSocketResponse.EAddSocket
    k_AddSocket_Failed_ToolIsInvalid: CMsgAddSocketResponse.EAddSocket
    k_AddSocket_Failed_ItemCannotBeSocketed: CMsgAddSocketResponse.EAddSocket
    k_AddSocket_Failed_FailedToAddSocket: CMsgAddSocketResponse.EAddSocket
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    UPDATED_SOCKET_INDEX_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    updated_socket_index: _containers.RepeatedScalarFieldContainer[int]
    response: CMsgAddSocketResponse.EAddSocket
    def __init__(
        self,
        item_id: int | None = ...,
        updated_socket_index: _Iterable[int] | None = ...,
        response: CMsgAddSocketResponse.EAddSocket | str | None = ...,
    ) -> None: ...

class CMsgAddItemToSocketData(_message.Message):
    __slots__ = ("gem_item_id", "socket_index")
    GEM_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    SOCKET_INDEX_FIELD_NUMBER: _ClassVar[int]
    gem_item_id: int
    socket_index: int
    def __init__(self, gem_item_id: int | None = ..., socket_index: int | None = ...) -> None: ...

class CMsgAddItemToSocket(_message.Message):
    __slots__ = ("item_item_id", "gems_to_socket")
    ITEM_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    GEMS_TO_SOCKET_FIELD_NUMBER: _ClassVar[int]
    item_item_id: int
    gems_to_socket: _containers.RepeatedCompositeFieldContainer[CMsgAddItemToSocketData]
    def __init__(
        self,
        item_item_id: int | None = ...,
        gems_to_socket: _Iterable[CMsgAddItemToSocketData | _Mapping] | None = ...,
    ) -> None: ...

class CMsgAddItemToSocketResponse(_message.Message):
    __slots__ = ("item_item_id", "updated_socket_index", "response")
    class EAddGem(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_AddGem_Succeeded: _ClassVar[CMsgAddItemToSocketResponse.EAddGem]
        k_AddGem_Failed_GemIsInvalid: _ClassVar[CMsgAddItemToSocketResponse.EAddGem]
        k_AddGem_Failed_ItemIsInvalid: _ClassVar[CMsgAddItemToSocketResponse.EAddGem]
        k_AddGem_Failed_FailedToAddGem: _ClassVar[CMsgAddItemToSocketResponse.EAddGem]
        k_AddGem_Failed_InvalidGemTypeForSocket: _ClassVar[CMsgAddItemToSocketResponse.EAddGem]
        k_AddGem_Failed_InvalidGemTypeForHero: _ClassVar[CMsgAddItemToSocketResponse.EAddGem]
        k_AddGem_Failed_InvalidGemTypeForSlot: _ClassVar[CMsgAddItemToSocketResponse.EAddGem]
        k_AddGem_Failed_SocketContainsUnremovableGem: _ClassVar[CMsgAddItemToSocketResponse.EAddGem]

    k_AddGem_Succeeded: CMsgAddItemToSocketResponse.EAddGem
    k_AddGem_Failed_GemIsInvalid: CMsgAddItemToSocketResponse.EAddGem
    k_AddGem_Failed_ItemIsInvalid: CMsgAddItemToSocketResponse.EAddGem
    k_AddGem_Failed_FailedToAddGem: CMsgAddItemToSocketResponse.EAddGem
    k_AddGem_Failed_InvalidGemTypeForSocket: CMsgAddItemToSocketResponse.EAddGem
    k_AddGem_Failed_InvalidGemTypeForHero: CMsgAddItemToSocketResponse.EAddGem
    k_AddGem_Failed_InvalidGemTypeForSlot: CMsgAddItemToSocketResponse.EAddGem
    k_AddGem_Failed_SocketContainsUnremovableGem: CMsgAddItemToSocketResponse.EAddGem
    ITEM_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    UPDATED_SOCKET_INDEX_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    item_item_id: int
    updated_socket_index: _containers.RepeatedScalarFieldContainer[int]
    response: CMsgAddItemToSocketResponse.EAddGem
    def __init__(
        self,
        item_item_id: int | None = ...,
        updated_socket_index: _Iterable[int] | None = ...,
        response: CMsgAddItemToSocketResponse.EAddGem | str | None = ...,
    ) -> None: ...

class CMsgResetStrangeGemCount(_message.Message):
    __slots__ = ("item_item_id", "socket_index")
    ITEM_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    SOCKET_INDEX_FIELD_NUMBER: _ClassVar[int]
    item_item_id: int
    socket_index: int
    def __init__(self, item_item_id: int | None = ..., socket_index: int | None = ...) -> None: ...

class CMsgResetStrangeGemCountResponse(_message.Message):
    __slots__ = ("response",)
    class EResetGem(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_ResetGem_Succeeded: _ClassVar[CMsgResetStrangeGemCountResponse.EResetGem]
        k_ResetGem_Failed_FailedToResetGem: _ClassVar[CMsgResetStrangeGemCountResponse.EResetGem]
        k_ResetGem_Failed_ItemIsInvalid: _ClassVar[CMsgResetStrangeGemCountResponse.EResetGem]
        k_ResetGem_Failed_InvalidSocketId: _ClassVar[CMsgResetStrangeGemCountResponse.EResetGem]
        k_ResetGem_Failed_SocketCannotBeReset: _ClassVar[CMsgResetStrangeGemCountResponse.EResetGem]

    k_ResetGem_Succeeded: CMsgResetStrangeGemCountResponse.EResetGem
    k_ResetGem_Failed_FailedToResetGem: CMsgResetStrangeGemCountResponse.EResetGem
    k_ResetGem_Failed_ItemIsInvalid: CMsgResetStrangeGemCountResponse.EResetGem
    k_ResetGem_Failed_InvalidSocketId: CMsgResetStrangeGemCountResponse.EResetGem
    k_ResetGem_Failed_SocketCannotBeReset: CMsgResetStrangeGemCountResponse.EResetGem
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgResetStrangeGemCountResponse.EResetGem
    def __init__(
        self, response: CMsgResetStrangeGemCountResponse.EResetGem | str | None = ...
    ) -> None: ...

class CMsgGCToClientPollFileRequest(_message.Message):
    __slots__ = ("file_name", "client_version", "poll_id")
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    POLL_ID_FIELD_NUMBER: _ClassVar[int]
    file_name: str
    client_version: int
    poll_id: int
    def __init__(
        self,
        file_name: str | None = ...,
        client_version: int | None = ...,
        poll_id: int | None = ...,
    ) -> None: ...

class CMsgGCToClientPollFileResponse(_message.Message):
    __slots__ = ("poll_id", "file_size", "file_crc")
    POLL_ID_FIELD_NUMBER: _ClassVar[int]
    FILE_SIZE_FIELD_NUMBER: _ClassVar[int]
    FILE_CRC_FIELD_NUMBER: _ClassVar[int]
    poll_id: int
    file_size: int
    file_crc: int
    def __init__(
        self, poll_id: int | None = ..., file_size: int | None = ..., file_crc: int | None = ...
    ) -> None: ...

class CMsgGCToGCPerformManualOp(_message.Message):
    __slots__ = ("op_id", "group_code")
    OP_ID_FIELD_NUMBER: _ClassVar[int]
    GROUP_CODE_FIELD_NUMBER: _ClassVar[int]
    op_id: int
    group_code: int
    def __init__(self, op_id: int | None = ..., group_code: int | None = ...) -> None: ...

class CMsgGCToGCPerformManualOpCompleted(_message.Message):
    __slots__ = ("success", "source_gc")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    SOURCE_GC_FIELD_NUMBER: _ClassVar[int]
    success: bool
    source_gc: int
    def __init__(self, success: bool = ..., source_gc: int | None = ...) -> None: ...

class CMsgGCToGCReloadServerRegionSettings(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgGCAdditionalWelcomeMsgList(_message.Message):
    __slots__ = ("welcome_messages",)
    WELCOME_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    welcome_messages: _containers.RepeatedCompositeFieldContainer[
        _gcsdk_gcmessages_pb2.CExtraMsgBlock
    ]
    def __init__(
        self,
        welcome_messages: _Iterable[_gcsdk_gcmessages_pb2.CExtraMsgBlock | _Mapping] | None = ...,
    ) -> None: ...

class CMsgApplyRemoteConVars(_message.Message):
    __slots__ = ("con_vars",)
    class ConVar(_message.Message):
        __slots__ = ("name", "value", "version_min", "version_max", "platform")
        NAME_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        VERSION_MIN_FIELD_NUMBER: _ClassVar[int]
        VERSION_MAX_FIELD_NUMBER: _ClassVar[int]
        PLATFORM_FIELD_NUMBER: _ClassVar[int]
        name: str
        value: str
        version_min: int
        version_max: int
        platform: _steammessages_pb2.EGCPlatform
        def __init__(
            self,
            name: str | None = ...,
            value: str | None = ...,
            version_min: int | None = ...,
            version_max: int | None = ...,
            platform: _steammessages_pb2.EGCPlatform | str | None = ...,
        ) -> None: ...

    CON_VARS_FIELD_NUMBER: _ClassVar[int]
    con_vars: _containers.RepeatedCompositeFieldContainer[CMsgApplyRemoteConVars.ConVar]
    def __init__(
        self, con_vars: _Iterable[CMsgApplyRemoteConVars.ConVar | _Mapping] | None = ...
    ) -> None: ...

class CMsgGCToClientApplyRemoteConVars(_message.Message):
    __slots__ = ("msg",)
    MSG_FIELD_NUMBER: _ClassVar[int]
    msg: CMsgApplyRemoteConVars
    def __init__(self, msg: CMsgApplyRemoteConVars | _Mapping | None = ...) -> None: ...

class CMsgGCToServerApplyRemoteConVars(_message.Message):
    __slots__ = ("msg",)
    MSG_FIELD_NUMBER: _ClassVar[int]
    msg: CMsgApplyRemoteConVars
    def __init__(self, msg: CMsgApplyRemoteConVars | _Mapping | None = ...) -> None: ...

class CMsgClientToGCIntegrityStatus(_message.Message):
    __slots__ = ("report", "secure_allowed", "diagnostics")
    class keyvalue(_message.Message):
        __slots__ = ("id", "extended", "value", "string_value")
        ID_FIELD_NUMBER: _ClassVar[int]
        EXTENDED_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
        id: int
        extended: int
        value: int
        string_value: str
        def __init__(
            self,
            id: int | None = ...,
            extended: int | None = ...,
            value: int | None = ...,
            string_value: str | None = ...,
        ) -> None: ...

    REPORT_FIELD_NUMBER: _ClassVar[int]
    SECURE_ALLOWED_FIELD_NUMBER: _ClassVar[int]
    DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
    report: str
    secure_allowed: bool
    diagnostics: _containers.RepeatedCompositeFieldContainer[CMsgClientToGCIntegrityStatus.keyvalue]
    def __init__(
        self,
        report: str | None = ...,
        secure_allowed: bool = ...,
        diagnostics: _Iterable[CMsgClientToGCIntegrityStatus.keyvalue | _Mapping] | None = ...,
    ) -> None: ...

class CMsgClientToGCAggregateMetrics(_message.Message):
    __slots__ = ("metrics",)
    class SingleMetric(_message.Message):
        __slots__ = ("metric_name", "metric_count")
        METRIC_NAME_FIELD_NUMBER: _ClassVar[int]
        METRIC_COUNT_FIELD_NUMBER: _ClassVar[int]
        metric_name: str
        metric_count: int
        def __init__(
            self, metric_name: str | None = ..., metric_count: int | None = ...
        ) -> None: ...

    METRICS_FIELD_NUMBER: _ClassVar[int]
    metrics: _containers.RepeatedCompositeFieldContainer[
        CMsgClientToGCAggregateMetrics.SingleMetric
    ]
    def __init__(
        self,
        metrics: _Iterable[CMsgClientToGCAggregateMetrics.SingleMetric | _Mapping] | None = ...,
    ) -> None: ...

class CMsgGCToClientAggregateMetricsBackoff(_message.Message):
    __slots__ = ("upload_rate_modifier",)
    UPLOAD_RATE_MODIFIER_FIELD_NUMBER: _ClassVar[int]
    upload_rate_modifier: float
    def __init__(self, upload_rate_modifier: float | None = ...) -> None: ...

class CMsgGCToServerSteamLearnAccessTokensChanged(_message.Message):
    __slots__ = ("access_tokens",)
    ACCESS_TOKENS_FIELD_NUMBER: _ClassVar[int]
    access_tokens: _steamworkssdk_pb2.CMsgSteamLearnAccessTokens
    def __init__(
        self, access_tokens: _steamworkssdk_pb2.CMsgSteamLearnAccessTokens | _Mapping | None = ...
    ) -> None: ...

class CMsgGCToServerSteamLearnUseHTTP(_message.Message):
    __slots__ = ("use_http",)
    USE_HTTP_FIELD_NUMBER: _ClassVar[int]
    use_http: bool
    def __init__(self, use_http: bool = ...) -> None: ...
