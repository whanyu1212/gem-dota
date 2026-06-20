from . import steammessages_pb2 as _steammessages_pb2
from . import dota_shared_enums_pb2 as _dota_shared_enums_pb2
from . import dota_gcmessages_common_pb2 as _dota_gcmessages_common_pb2
from . import gcsdk_gcmessages_pb2 as _gcsdk_gcmessages_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CMsgClientToGCFightingGameChallengeFriend(_message.Message):
    __slots__ = ("friend_account_id",)
    FRIEND_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    friend_account_id: int
    def __init__(self, friend_account_id: _Optional[int] = ...) -> None: ...

class CMsgClientToGCFightingGameChallengeFriendResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCFightingGameChallengeFriendResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCFightingGameChallengeFriendResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCFightingGameChallengeFriendResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCFightingGameChallengeFriendResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCFightingGameChallengeFriendResponse.EResponse]
        k_eInvalidAccountID: _ClassVar[CMsgClientToGCFightingGameChallengeFriendResponse.EResponse]
        k_eStillWaitingOnAnotherChallenge: _ClassVar[CMsgClientToGCFightingGameChallengeFriendResponse.EResponse]
    k_eInternalError: CMsgClientToGCFightingGameChallengeFriendResponse.EResponse
    k_eSuccess: CMsgClientToGCFightingGameChallengeFriendResponse.EResponse
    k_eTooBusy: CMsgClientToGCFightingGameChallengeFriendResponse.EResponse
    k_eDisabled: CMsgClientToGCFightingGameChallengeFriendResponse.EResponse
    k_eTimeout: CMsgClientToGCFightingGameChallengeFriendResponse.EResponse
    k_eInvalidAccountID: CMsgClientToGCFightingGameChallengeFriendResponse.EResponse
    k_eStillWaitingOnAnotherChallenge: CMsgClientToGCFightingGameChallengeFriendResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCFightingGameChallengeFriendResponse.EResponse
    def __init__(self, response: _Optional[_Union[CMsgClientToGCFightingGameChallengeFriendResponse.EResponse, str]] = ...) -> None: ...

class CMsgClientToGCFightingGameCancelChallengeFriend(_message.Message):
    __slots__ = ("friend_account_id",)
    FRIEND_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    friend_account_id: int
    def __init__(self, friend_account_id: _Optional[int] = ...) -> None: ...

class CMsgClientToGCFightingGameAnswerChallenge(_message.Message):
    __slots__ = ("challenger_account_id", "accept")
    CHALLENGER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ACCEPT_FIELD_NUMBER: _ClassVar[int]
    challenger_account_id: int
    accept: bool
    def __init__(self, challenger_account_id: _Optional[int] = ..., accept: bool = ...) -> None: ...

class CMsgClientToGCFightingGameAnswerChallengeResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCFightingGameAnswerChallengeResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCFightingGameAnswerChallengeResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCFightingGameAnswerChallengeResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCFightingGameAnswerChallengeResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCFightingGameAnswerChallengeResponse.EResponse]
        k_eInvalidChallenge: _ClassVar[CMsgClientToGCFightingGameAnswerChallengeResponse.EResponse]
    k_eInternalError: CMsgClientToGCFightingGameAnswerChallengeResponse.EResponse
    k_eSuccess: CMsgClientToGCFightingGameAnswerChallengeResponse.EResponse
    k_eTooBusy: CMsgClientToGCFightingGameAnswerChallengeResponse.EResponse
    k_eDisabled: CMsgClientToGCFightingGameAnswerChallengeResponse.EResponse
    k_eTimeout: CMsgClientToGCFightingGameAnswerChallengeResponse.EResponse
    k_eInvalidChallenge: CMsgClientToGCFightingGameAnswerChallengeResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCFightingGameAnswerChallengeResponse.EResponse
    def __init__(self, response: _Optional[_Union[CMsgClientToGCFightingGameAnswerChallengeResponse.EResponse, str]] = ...) -> None: ...

class CMsgGCToClientFightingGameChallenge(_message.Message):
    __slots__ = ("challenger_account_id",)
    CHALLENGER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    challenger_account_id: int
    def __init__(self, challenger_account_id: _Optional[int] = ...) -> None: ...

class CMsgGCToClientFightingGameChallengeCanceled(_message.Message):
    __slots__ = ("challenger_account_id", "responder_account_id")
    CHALLENGER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONDER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    challenger_account_id: int
    responder_account_id: int
    def __init__(self, challenger_account_id: _Optional[int] = ..., responder_account_id: _Optional[int] = ...) -> None: ...

class CMsgGCToClientFightingGameStartMatch(_message.Message):
    __slots__ = ("challenger_account_id", "responder_account_id")
    CHALLENGER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONDER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    challenger_account_id: int
    responder_account_id: int
    def __init__(self, challenger_account_id: _Optional[int] = ..., responder_account_id: _Optional[int] = ...) -> None: ...
