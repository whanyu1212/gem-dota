from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class EBingoAuditAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eBingoAuditAction_Invalid: _ClassVar[EBingoAuditAction]
    k_eBingoAuditAction_DevModifyTokens: _ClassVar[EBingoAuditAction]
    k_eBingoAuditAction_DevClearInventory: _ClassVar[EBingoAuditAction]
    k_eBingoAuditAction_DevRerollCard: _ClassVar[EBingoAuditAction]
    k_eBingoAuditAction_ShuffleCard: _ClassVar[EBingoAuditAction]
    k_eBingoAuditAction_RerollSquare: _ClassVar[EBingoAuditAction]
    k_eBingoAuditAction_UpgradeSquare: _ClassVar[EBingoAuditAction]
    k_eBingoAuditAction_ClaimRow: _ClassVar[EBingoAuditAction]
    k_eBingoAuditAction_EventActionTokenGrant: _ClassVar[EBingoAuditAction]
    k_eBingoAuditAction_SupportGrantTokens: _ClassVar[EBingoAuditAction]
    k_eBingoAuditAction_SupportStatThresholdFixup: _ClassVar[EBingoAuditAction]

k_eBingoAuditAction_Invalid: EBingoAuditAction
k_eBingoAuditAction_DevModifyTokens: EBingoAuditAction
k_eBingoAuditAction_DevClearInventory: EBingoAuditAction
k_eBingoAuditAction_DevRerollCard: EBingoAuditAction
k_eBingoAuditAction_ShuffleCard: EBingoAuditAction
k_eBingoAuditAction_RerollSquare: EBingoAuditAction
k_eBingoAuditAction_UpgradeSquare: EBingoAuditAction
k_eBingoAuditAction_ClaimRow: EBingoAuditAction
k_eBingoAuditAction_EventActionTokenGrant: EBingoAuditAction
k_eBingoAuditAction_SupportGrantTokens: EBingoAuditAction
k_eBingoAuditAction_SupportStatThresholdFixup: EBingoAuditAction

class CMsgBingoSquare(_message.Message):
    __slots__ = ("stat_id", "stat_threshold", "upgrade_level")
    STAT_ID_FIELD_NUMBER: _ClassVar[int]
    STAT_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    UPGRADE_LEVEL_FIELD_NUMBER: _ClassVar[int]
    stat_id: int
    stat_threshold: int
    upgrade_level: int
    def __init__(
        self,
        stat_id: int | None = ...,
        stat_threshold: int | None = ...,
        upgrade_level: int | None = ...,
    ) -> None: ...

class CMsgBingoTokens(_message.Message):
    __slots__ = ("token_count",)
    TOKEN_COUNT_FIELD_NUMBER: _ClassVar[int]
    token_count: int
    def __init__(self, token_count: int | None = ...) -> None: ...

class CMsgBingoCard(_message.Message):
    __slots__ = ("squares",)
    SQUARES_FIELD_NUMBER: _ClassVar[int]
    squares: _containers.RepeatedCompositeFieldContainer[CMsgBingoSquare]
    def __init__(self, squares: _Iterable[CMsgBingoSquare | _Mapping] | None = ...) -> None: ...

class CMsgBingoUserData(_message.Message):
    __slots__ = ("bingo_cards", "bingo_tokens")
    class BingoCardsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: CMsgBingoCard
        def __init__(
            self, key: int | None = ..., value: CMsgBingoCard | _Mapping | None = ...
        ) -> None: ...

    class BingoTokensEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: CMsgBingoTokens
        def __init__(
            self, key: int | None = ..., value: CMsgBingoTokens | _Mapping | None = ...
        ) -> None: ...

    BINGO_CARDS_FIELD_NUMBER: _ClassVar[int]
    BINGO_TOKENS_FIELD_NUMBER: _ClassVar[int]
    bingo_cards: _containers.RepeatedCompositeFieldContainer[CMsgBingoUserData.BingoCardsEntry]
    bingo_tokens: _containers.RepeatedCompositeFieldContainer[CMsgBingoUserData.BingoTokensEntry]
    def __init__(
        self,
        bingo_cards: _Iterable[CMsgBingoUserData.BingoCardsEntry | _Mapping] | None = ...,
        bingo_tokens: _Iterable[CMsgBingoUserData.BingoTokensEntry | _Mapping] | None = ...,
    ) -> None: ...

class CMsgClientToGCBingoGetUserData(_message.Message):
    __slots__ = ("league_id",)
    LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    league_id: int
    def __init__(self, league_id: int | None = ...) -> None: ...

class CMsgClientToGCBingoGetUserDataResponse(_message.Message):
    __slots__ = ("response", "user_data")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCBingoGetUserDataResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCBingoGetUserDataResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCBingoGetUserDataResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCBingoGetUserDataResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCBingoGetUserDataResponse.EResponse]

    k_eInternalError: CMsgClientToGCBingoGetUserDataResponse.EResponse
    k_eSuccess: CMsgClientToGCBingoGetUserDataResponse.EResponse
    k_eTooBusy: CMsgClientToGCBingoGetUserDataResponse.EResponse
    k_eDisabled: CMsgClientToGCBingoGetUserDataResponse.EResponse
    k_eTimeout: CMsgClientToGCBingoGetUserDataResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    USER_DATA_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCBingoGetUserDataResponse.EResponse
    user_data: CMsgBingoUserData
    def __init__(
        self,
        response: CMsgClientToGCBingoGetUserDataResponse.EResponse | str | None = ...,
        user_data: CMsgBingoUserData | _Mapping | None = ...,
    ) -> None: ...

class CMsgBingoIndividualStatData(_message.Message):
    __slots__ = ("stat_id", "stat_value")
    STAT_ID_FIELD_NUMBER: _ClassVar[int]
    STAT_VALUE_FIELD_NUMBER: _ClassVar[int]
    stat_id: int
    stat_value: int
    def __init__(self, stat_id: int | None = ..., stat_value: int | None = ...) -> None: ...

class CMsgBingoStatsData(_message.Message):
    __slots__ = ("stats_data",)
    STATS_DATA_FIELD_NUMBER: _ClassVar[int]
    stats_data: _containers.RepeatedCompositeFieldContainer[CMsgBingoIndividualStatData]
    def __init__(
        self, stats_data: _Iterable[CMsgBingoIndividualStatData | _Mapping] | None = ...
    ) -> None: ...

class CMsgClientToGCBingoGetStatsData(_message.Message):
    __slots__ = ("league_id", "league_phase")
    LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    LEAGUE_PHASE_FIELD_NUMBER: _ClassVar[int]
    league_id: int
    league_phase: int
    def __init__(self, league_id: int | None = ..., league_phase: int | None = ...) -> None: ...

class CMsgClientToGCBingoGetStatsDataResponse(_message.Message):
    __slots__ = ("response", "stats_data")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCBingoGetStatsDataResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCBingoGetStatsDataResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCBingoGetStatsDataResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCBingoGetStatsDataResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCBingoGetStatsDataResponse.EResponse]

    k_eInternalError: CMsgClientToGCBingoGetStatsDataResponse.EResponse
    k_eSuccess: CMsgClientToGCBingoGetStatsDataResponse.EResponse
    k_eTooBusy: CMsgClientToGCBingoGetStatsDataResponse.EResponse
    k_eDisabled: CMsgClientToGCBingoGetStatsDataResponse.EResponse
    k_eTimeout: CMsgClientToGCBingoGetStatsDataResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    STATS_DATA_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCBingoGetStatsDataResponse.EResponse
    stats_data: CMsgBingoStatsData
    def __init__(
        self,
        response: CMsgClientToGCBingoGetStatsDataResponse.EResponse | str | None = ...,
        stats_data: CMsgBingoStatsData | _Mapping | None = ...,
    ) -> None: ...

class CMsgGCToClientBingoUserDataUpdated(_message.Message):
    __slots__ = ("league_id", "user_data")
    LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_DATA_FIELD_NUMBER: _ClassVar[int]
    league_id: int
    user_data: CMsgBingoUserData
    def __init__(
        self, league_id: int | None = ..., user_data: CMsgBingoUserData | _Mapping | None = ...
    ) -> None: ...

class CMsgClientToGCBingoClaimRow(_message.Message):
    __slots__ = ("league_id", "league_phase", "row_index")
    LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    LEAGUE_PHASE_FIELD_NUMBER: _ClassVar[int]
    ROW_INDEX_FIELD_NUMBER: _ClassVar[int]
    league_id: int
    league_phase: int
    row_index: int
    def __init__(
        self,
        league_id: int | None = ...,
        league_phase: int | None = ...,
        row_index: int | None = ...,
    ) -> None: ...

class CMsgClientToGCBingoClaimRowResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCBingoClaimRowResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCBingoClaimRowResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCBingoClaimRowResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCBingoClaimRowResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCBingoClaimRowResponse.EResponse]
        k_eInvalidRow: _ClassVar[CMsgClientToGCBingoClaimRowResponse.EResponse]
        k_eExpiredCard: _ClassVar[CMsgClientToGCBingoClaimRowResponse.EResponse]

    k_eInternalError: CMsgClientToGCBingoClaimRowResponse.EResponse
    k_eSuccess: CMsgClientToGCBingoClaimRowResponse.EResponse
    k_eTooBusy: CMsgClientToGCBingoClaimRowResponse.EResponse
    k_eDisabled: CMsgClientToGCBingoClaimRowResponse.EResponse
    k_eTimeout: CMsgClientToGCBingoClaimRowResponse.EResponse
    k_eInvalidRow: CMsgClientToGCBingoClaimRowResponse.EResponse
    k_eExpiredCard: CMsgClientToGCBingoClaimRowResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCBingoClaimRowResponse.EResponse
    def __init__(
        self, response: CMsgClientToGCBingoClaimRowResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCBingoShuffleCard(_message.Message):
    __slots__ = ("league_id", "league_phase")
    LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    LEAGUE_PHASE_FIELD_NUMBER: _ClassVar[int]
    league_id: int
    league_phase: int
    def __init__(self, league_id: int | None = ..., league_phase: int | None = ...) -> None: ...

class CMsgClientToGCBingoShuffleCardResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCBingoShuffleCardResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCBingoShuffleCardResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCBingoShuffleCardResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCBingoShuffleCardResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCBingoShuffleCardResponse.EResponse]
        k_eExpiredCard: _ClassVar[CMsgClientToGCBingoShuffleCardResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCBingoShuffleCardResponse.EResponse]
        k_eInsufficientTokens: _ClassVar[CMsgClientToGCBingoShuffleCardResponse.EResponse]

    k_eInternalError: CMsgClientToGCBingoShuffleCardResponse.EResponse
    k_eSuccess: CMsgClientToGCBingoShuffleCardResponse.EResponse
    k_eTooBusy: CMsgClientToGCBingoShuffleCardResponse.EResponse
    k_eDisabled: CMsgClientToGCBingoShuffleCardResponse.EResponse
    k_eTimeout: CMsgClientToGCBingoShuffleCardResponse.EResponse
    k_eExpiredCard: CMsgClientToGCBingoShuffleCardResponse.EResponse
    k_eNotAllowed: CMsgClientToGCBingoShuffleCardResponse.EResponse
    k_eInsufficientTokens: CMsgClientToGCBingoShuffleCardResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCBingoShuffleCardResponse.EResponse
    def __init__(
        self, response: CMsgClientToGCBingoShuffleCardResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCBingoModifySquare(_message.Message):
    __slots__ = ("league_id", "league_phase", "square_index", "action")
    class EModifyAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eRerollStat: _ClassVar[CMsgClientToGCBingoModifySquare.EModifyAction]
        k_eUpgrade: _ClassVar[CMsgClientToGCBingoModifySquare.EModifyAction]

    k_eRerollStat: CMsgClientToGCBingoModifySquare.EModifyAction
    k_eUpgrade: CMsgClientToGCBingoModifySquare.EModifyAction
    LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    LEAGUE_PHASE_FIELD_NUMBER: _ClassVar[int]
    SQUARE_INDEX_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    league_id: int
    league_phase: int
    square_index: int
    action: CMsgClientToGCBingoModifySquare.EModifyAction
    def __init__(
        self,
        league_id: int | None = ...,
        league_phase: int | None = ...,
        square_index: int | None = ...,
        action: CMsgClientToGCBingoModifySquare.EModifyAction | str | None = ...,
    ) -> None: ...

class CMsgClientToGCBingoModifySquareResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCBingoModifySquareResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCBingoModifySquareResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCBingoModifySquareResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCBingoModifySquareResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCBingoModifySquareResponse.EResponse]
        k_eExpiredCard: _ClassVar[CMsgClientToGCBingoModifySquareResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCBingoModifySquareResponse.EResponse]
        k_eInsufficientTokens: _ClassVar[CMsgClientToGCBingoModifySquareResponse.EResponse]
        k_eCantUpgrade: _ClassVar[CMsgClientToGCBingoModifySquareResponse.EResponse]
        k_eCantReroll: _ClassVar[CMsgClientToGCBingoModifySquareResponse.EResponse]
        k_eInvalidSquare: _ClassVar[CMsgClientToGCBingoModifySquareResponse.EResponse]

    k_eInternalError: CMsgClientToGCBingoModifySquareResponse.EResponse
    k_eSuccess: CMsgClientToGCBingoModifySquareResponse.EResponse
    k_eTooBusy: CMsgClientToGCBingoModifySquareResponse.EResponse
    k_eDisabled: CMsgClientToGCBingoModifySquareResponse.EResponse
    k_eTimeout: CMsgClientToGCBingoModifySquareResponse.EResponse
    k_eExpiredCard: CMsgClientToGCBingoModifySquareResponse.EResponse
    k_eNotAllowed: CMsgClientToGCBingoModifySquareResponse.EResponse
    k_eInsufficientTokens: CMsgClientToGCBingoModifySquareResponse.EResponse
    k_eCantUpgrade: CMsgClientToGCBingoModifySquareResponse.EResponse
    k_eCantReroll: CMsgClientToGCBingoModifySquareResponse.EResponse
    k_eInvalidSquare: CMsgClientToGCBingoModifySquareResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCBingoModifySquareResponse.EResponse
    def __init__(
        self, response: CMsgClientToGCBingoModifySquareResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCBingoDevRerollCard(_message.Message):
    __slots__ = ("league_id", "league_phase")
    LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    LEAGUE_PHASE_FIELD_NUMBER: _ClassVar[int]
    league_id: int
    league_phase: int
    def __init__(self, league_id: int | None = ..., league_phase: int | None = ...) -> None: ...

class CMsgClientToGCBingoDevRerollCardResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCBingoDevRerollCardResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCBingoDevRerollCardResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCBingoDevRerollCardResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCBingoDevRerollCardResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCBingoDevRerollCardResponse.EResponse]
        k_eExpiredCard: _ClassVar[CMsgClientToGCBingoDevRerollCardResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCBingoDevRerollCardResponse.EResponse]

    k_eInternalError: CMsgClientToGCBingoDevRerollCardResponse.EResponse
    k_eSuccess: CMsgClientToGCBingoDevRerollCardResponse.EResponse
    k_eTooBusy: CMsgClientToGCBingoDevRerollCardResponse.EResponse
    k_eDisabled: CMsgClientToGCBingoDevRerollCardResponse.EResponse
    k_eTimeout: CMsgClientToGCBingoDevRerollCardResponse.EResponse
    k_eExpiredCard: CMsgClientToGCBingoDevRerollCardResponse.EResponse
    k_eNotAllowed: CMsgClientToGCBingoDevRerollCardResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCBingoDevRerollCardResponse.EResponse
    def __init__(
        self, response: CMsgClientToGCBingoDevRerollCardResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCBingoDevAddTokens(_message.Message):
    __slots__ = ("league_id", "league_phase", "token_count")
    LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    LEAGUE_PHASE_FIELD_NUMBER: _ClassVar[int]
    TOKEN_COUNT_FIELD_NUMBER: _ClassVar[int]
    league_id: int
    league_phase: int
    token_count: int
    def __init__(
        self,
        league_id: int | None = ...,
        league_phase: int | None = ...,
        token_count: int | None = ...,
    ) -> None: ...

class CMsgClientToGCBingoDevAddTokensResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCBingoDevAddTokensResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCBingoDevAddTokensResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCBingoDevAddTokensResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCBingoDevAddTokensResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCBingoDevAddTokensResponse.EResponse]
        k_eExpiredCard: _ClassVar[CMsgClientToGCBingoDevAddTokensResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCBingoDevAddTokensResponse.EResponse]

    k_eInternalError: CMsgClientToGCBingoDevAddTokensResponse.EResponse
    k_eSuccess: CMsgClientToGCBingoDevAddTokensResponse.EResponse
    k_eTooBusy: CMsgClientToGCBingoDevAddTokensResponse.EResponse
    k_eDisabled: CMsgClientToGCBingoDevAddTokensResponse.EResponse
    k_eTimeout: CMsgClientToGCBingoDevAddTokensResponse.EResponse
    k_eExpiredCard: CMsgClientToGCBingoDevAddTokensResponse.EResponse
    k_eNotAllowed: CMsgClientToGCBingoDevAddTokensResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCBingoDevAddTokensResponse.EResponse
    def __init__(
        self, response: CMsgClientToGCBingoDevAddTokensResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCBingoDevClearInventory(_message.Message):
    __slots__ = ("league_id",)
    LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    league_id: int
    def __init__(self, league_id: int | None = ...) -> None: ...

class CMsgClientToGCBingoDevClearInventoryResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCBingoDevClearInventoryResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCBingoDevClearInventoryResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCBingoDevClearInventoryResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCBingoDevClearInventoryResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCBingoDevClearInventoryResponse.EResponse]
        k_eExpiredCard: _ClassVar[CMsgClientToGCBingoDevClearInventoryResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCBingoDevClearInventoryResponse.EResponse]

    k_eInternalError: CMsgClientToGCBingoDevClearInventoryResponse.EResponse
    k_eSuccess: CMsgClientToGCBingoDevClearInventoryResponse.EResponse
    k_eTooBusy: CMsgClientToGCBingoDevClearInventoryResponse.EResponse
    k_eDisabled: CMsgClientToGCBingoDevClearInventoryResponse.EResponse
    k_eTimeout: CMsgClientToGCBingoDevClearInventoryResponse.EResponse
    k_eExpiredCard: CMsgClientToGCBingoDevClearInventoryResponse.EResponse
    k_eNotAllowed: CMsgClientToGCBingoDevClearInventoryResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCBingoDevClearInventoryResponse.EResponse
    def __init__(
        self, response: CMsgClientToGCBingoDevClearInventoryResponse.EResponse | str | None = ...
    ) -> None: ...
