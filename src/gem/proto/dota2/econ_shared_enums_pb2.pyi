from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class EGCEconBaseMsg(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EMsgGCGenericResult: _ClassVar[EGCEconBaseMsg]

class EGCMsgResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EGCMsgResponseOK: _ClassVar[EGCMsgResponse]
    k_EGCMsgResponseDenied: _ClassVar[EGCMsgResponse]
    k_EGCMsgResponseServerError: _ClassVar[EGCMsgResponse]
    k_EGCMsgResponseTimeout: _ClassVar[EGCMsgResponse]
    k_EGCMsgResponseInvalid: _ClassVar[EGCMsgResponse]
    k_EGCMsgResponseNoMatch: _ClassVar[EGCMsgResponse]
    k_EGCMsgResponseUnknownError: _ClassVar[EGCMsgResponse]
    k_EGCMsgResponseNotLoggedOn: _ClassVar[EGCMsgResponse]
    k_EGCMsgFailedToCreate: _ClassVar[EGCMsgResponse]

class EGCMsgUseItemResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EGCMsgUseItemResponse_ItemUsed: _ClassVar[EGCMsgUseItemResponse]
    k_EGCMsgUseItemResponse_GiftNoOtherPlayers: _ClassVar[EGCMsgUseItemResponse]
    k_EGCMsgUseItemResponse_ServerError: _ClassVar[EGCMsgUseItemResponse]
    k_EGCMsgUseItemResponse_MiniGameAlreadyStarted: _ClassVar[EGCMsgUseItemResponse]
    k_EGCMsgUseItemResponse_ItemUsed_ItemsGranted: _ClassVar[EGCMsgUseItemResponse]
    k_EGCMsgUseItemResponse_DropRateBonusAlreadyGranted: _ClassVar[EGCMsgUseItemResponse]
    k_EGCMsgUseItemResponse_NotInLowPriorityPool: _ClassVar[EGCMsgUseItemResponse]
    k_EGCMsgUseItemResponse_NotHighEnoughLevel: _ClassVar[EGCMsgUseItemResponse]
    k_EGCMsgUseItemResponse_EventNotActive: _ClassVar[EGCMsgUseItemResponse]
    k_EGCMsgUseItemResponse_ItemUsed_EventPointsGranted: _ClassVar[EGCMsgUseItemResponse]
    k_EGCMsgUseItemResponse_MissingRequirement: _ClassVar[EGCMsgUseItemResponse]
    k_EGCMsgUseItemResponse_EmoticonUnlock_NoNew: _ClassVar[EGCMsgUseItemResponse]
    k_EGCMsgUseItemResponse_EmoticonUnlock_Complete: _ClassVar[EGCMsgUseItemResponse]
    k_EGCMsgUseItemResponse_ItemUsed_Compendium: _ClassVar[EGCMsgUseItemResponse]

k_EMsgGCGenericResult: EGCEconBaseMsg
k_EGCMsgResponseOK: EGCMsgResponse
k_EGCMsgResponseDenied: EGCMsgResponse
k_EGCMsgResponseServerError: EGCMsgResponse
k_EGCMsgResponseTimeout: EGCMsgResponse
k_EGCMsgResponseInvalid: EGCMsgResponse
k_EGCMsgResponseNoMatch: EGCMsgResponse
k_EGCMsgResponseUnknownError: EGCMsgResponse
k_EGCMsgResponseNotLoggedOn: EGCMsgResponse
k_EGCMsgFailedToCreate: EGCMsgResponse
k_EGCMsgUseItemResponse_ItemUsed: EGCMsgUseItemResponse
k_EGCMsgUseItemResponse_GiftNoOtherPlayers: EGCMsgUseItemResponse
k_EGCMsgUseItemResponse_ServerError: EGCMsgUseItemResponse
k_EGCMsgUseItemResponse_MiniGameAlreadyStarted: EGCMsgUseItemResponse
k_EGCMsgUseItemResponse_ItemUsed_ItemsGranted: EGCMsgUseItemResponse
k_EGCMsgUseItemResponse_DropRateBonusAlreadyGranted: EGCMsgUseItemResponse
k_EGCMsgUseItemResponse_NotInLowPriorityPool: EGCMsgUseItemResponse
k_EGCMsgUseItemResponse_NotHighEnoughLevel: EGCMsgUseItemResponse
k_EGCMsgUseItemResponse_EventNotActive: EGCMsgUseItemResponse
k_EGCMsgUseItemResponse_ItemUsed_EventPointsGranted: EGCMsgUseItemResponse
k_EGCMsgUseItemResponse_MissingRequirement: EGCMsgUseItemResponse
k_EGCMsgUseItemResponse_EmoticonUnlock_NoNew: EGCMsgUseItemResponse
k_EGCMsgUseItemResponse_EmoticonUnlock_Complete: EGCMsgUseItemResponse
k_EGCMsgUseItemResponse_ItemUsed_Compendium: EGCMsgUseItemResponse

class CMsgGenericResult(_message.Message):
    __slots__ = ("eresult", "debug_message")
    ERESULT_FIELD_NUMBER: _ClassVar[int]
    DEBUG_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    eresult: int
    debug_message: str
    def __init__(self, eresult: int | None = ..., debug_message: str | None = ...) -> None: ...
