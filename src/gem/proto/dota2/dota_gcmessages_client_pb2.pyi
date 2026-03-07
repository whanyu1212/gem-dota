from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

import base_gcmessages_pb2 as _base_gcmessages_pb2
import dota_gcmessages_common_lobby_pb2 as _dota_gcmessages_common_lobby_pb2
import dota_gcmessages_common_match_management_pb2 as _dota_gcmessages_common_match_management_pb2
import dota_gcmessages_common_pb2 as _dota_gcmessages_common_pb2
import dota_shared_enums_pb2 as _dota_shared_enums_pb2
import gcsdk_gcmessages_pb2 as _gcsdk_gcmessages_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class CMsgDOTARequestMatches_SkillLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CMsgDOTARequestMatches_SkillLevel_Any: _ClassVar[CMsgDOTARequestMatches_SkillLevel]
    CMsgDOTARequestMatches_SkillLevel_Normal: _ClassVar[CMsgDOTARequestMatches_SkillLevel]
    CMsgDOTARequestMatches_SkillLevel_High: _ClassVar[CMsgDOTARequestMatches_SkillLevel]
    CMsgDOTARequestMatches_SkillLevel_VeryHigh: _ClassVar[CMsgDOTARequestMatches_SkillLevel]

class DOTA_WatchReplayType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOTA_WATCH_REPLAY_NORMAL: _ClassVar[DOTA_WatchReplayType]
    DOTA_WATCH_REPLAY_HIGHLIGHTS: _ClassVar[DOTA_WatchReplayType]

class EItemEditorReservationResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EItemEditorReservationResult_OK: _ClassVar[EItemEditorReservationResult]
    k_EItemEditorReservationResult_AlreadyExists: _ClassVar[EItemEditorReservationResult]
    k_EItemEditorReservationResult_Reserved: _ClassVar[EItemEditorReservationResult]
    k_EItemEditorReservationResult_TimedOut: _ClassVar[EItemEditorReservationResult]

class EWeekendTourneyRichPresenceEvent(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EWeekendTourneyRichPresenceEvent_None: _ClassVar[EWeekendTourneyRichPresenceEvent]
    k_EWeekendTourneyRichPresenceEvent_StartedMatch: _ClassVar[EWeekendTourneyRichPresenceEvent]
    k_EWeekendTourneyRichPresenceEvent_WonMatch: _ClassVar[EWeekendTourneyRichPresenceEvent]
    k_EWeekendTourneyRichPresenceEvent_Eliminated: _ClassVar[EWeekendTourneyRichPresenceEvent]

class EDOTATriviaAnswerResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EDOTATriviaAnswerResult_Success: _ClassVar[EDOTATriviaAnswerResult]
    k_EDOTATriviaAnswerResult_InvalidQuestion: _ClassVar[EDOTATriviaAnswerResult]
    k_EDOTATriviaAnswerResult_InvalidAnswer: _ClassVar[EDOTATriviaAnswerResult]
    k_EDOTATriviaAnswerResult_QuestionLocked: _ClassVar[EDOTATriviaAnswerResult]
    k_EDOTATriviaAnswerResult_AlreadyAnswered: _ClassVar[EDOTATriviaAnswerResult]
    k_EDOTATriviaAnswerResult_TriviaDisabled: _ClassVar[EDOTATriviaAnswerResult]

class EPurchaseHeroRelicResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EPurchaseHeroRelicResult_Success: _ClassVar[EPurchaseHeroRelicResult]
    k_EPurchaseHeroRelicResult_FailedToSend: _ClassVar[EPurchaseHeroRelicResult]
    k_EPurchaseHeroRelicResult_NotEnoughPoints: _ClassVar[EPurchaseHeroRelicResult]
    k_EPurchaseHeroRelicResult_InternalServerError: _ClassVar[EPurchaseHeroRelicResult]
    k_EPurchaseHeroRelicResult_PurchaseNotAllowed: _ClassVar[EPurchaseHeroRelicResult]
    k_EPurchaseHeroRelicResult_InvalidRelic: _ClassVar[EPurchaseHeroRelicResult]
    k_EPurchaseHeroRelicResult_AlreadyOwned: _ClassVar[EPurchaseHeroRelicResult]
    k_EPurchaseHeroRelicResult_InvalidRarity: _ClassVar[EPurchaseHeroRelicResult]

class EDevEventRequestResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EDevEventRequestResult_Success: _ClassVar[EDevEventRequestResult]
    k_EDevEventRequestResult_NotAllowed: _ClassVar[EDevEventRequestResult]
    k_EDevEventRequestResult_InvalidEvent: _ClassVar[EDevEventRequestResult]
    k_EDevEventRequestResult_SqlFailure: _ClassVar[EDevEventRequestResult]
    k_EDevEventRequestResult_Timeout: _ClassVar[EDevEventRequestResult]
    k_EDevEventRequestResult_LockFailure: _ClassVar[EDevEventRequestResult]
    k_EDevEventRequestResult_SDOLoadFailure: _ClassVar[EDevEventRequestResult]

class ESupportEventRequestResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_ESupportEventRequestResult_Success: _ClassVar[ESupportEventRequestResult]
    k_ESupportEventRequestResult_Timeout: _ClassVar[ESupportEventRequestResult]
    k_ESupportEventRequestResult_CantLockSOCache: _ClassVar[ESupportEventRequestResult]
    k_ESupportEventRequestResult_ItemNotInInventory: _ClassVar[ESupportEventRequestResult]
    k_ESupportEventRequestResult_InvalidItemDef: _ClassVar[ESupportEventRequestResult]
    k_ESupportEventRequestResult_InvalidEvent: _ClassVar[ESupportEventRequestResult]
    k_ESupportEventRequestResult_EventExpired: _ClassVar[ESupportEventRequestResult]
    k_ESupportEventRequestResult_InvalidSupportAccount: _ClassVar[ESupportEventRequestResult]
    k_ESupportEventRequestResult_InvalidSupportMessage: _ClassVar[ESupportEventRequestResult]
    k_ESupportEventRequestResult_InvalidEventPoints: _ClassVar[ESupportEventRequestResult]
    k_ESupportEventRequestResult_InvalidPremiumPoints: _ClassVar[ESupportEventRequestResult]
    k_ESupportEventRequestResult_InvalidActionID: _ClassVar[ESupportEventRequestResult]
    k_ESupportEventRequestResult_InvalidActionScore: _ClassVar[ESupportEventRequestResult]
    k_ESupportEventRequestResult_TransactionFailed: _ClassVar[ESupportEventRequestResult]

class EUnderDraftResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eInternalError: _ClassVar[EUnderDraftResponse]
    k_eSuccess: _ClassVar[EUnderDraftResponse]
    k_eNoGold: _ClassVar[EUnderDraftResponse]
    k_eInvalidSlot: _ClassVar[EUnderDraftResponse]
    k_eNoBenchSpace: _ClassVar[EUnderDraftResponse]
    k_eNoTickets: _ClassVar[EUnderDraftResponse]
    k_eEventNotOwned: _ClassVar[EUnderDraftResponse]
    k_eInvalidReward: _ClassVar[EUnderDraftResponse]
    k_eHasBigReward: _ClassVar[EUnderDraftResponse]
    k_eNoGCConnection: _ClassVar[EUnderDraftResponse]
    k_eTooBusy: _ClassVar[EUnderDraftResponse]
    k_eCantRollBack: _ClassVar[EUnderDraftResponse]

class EDOTADraftTriviaAnswerResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EDOTADraftTriviaAnswerResult_Success: _ClassVar[EDOTADraftTriviaAnswerResult]
    k_EDOTADraftTriviaAnswerResult_InvalidMatchID: _ClassVar[EDOTADraftTriviaAnswerResult]
    k_EDOTADraftTriviaAnswerResult_AlreadyAnswered: _ClassVar[EDOTADraftTriviaAnswerResult]
    k_EDOTADraftTriviaAnswerResult_InternalError: _ClassVar[EDOTADraftTriviaAnswerResult]
    k_EDOTADraftTriviaAnswerResult_TriviaDisabled: _ClassVar[EDOTADraftTriviaAnswerResult]
    k_EDOTADraftTriviaAnswerResult_GCDown: _ClassVar[EDOTADraftTriviaAnswerResult]

class CMsgClientToGCUpdateComicBookStat_Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CMsgClientToGCUpdateComicBookStat_Type_HighestPageRead: _ClassVar[
        CMsgClientToGCUpdateComicBookStat_Type
    ]
    CMsgClientToGCUpdateComicBookStat_Type_SecondsSpentReading: _ClassVar[
        CMsgClientToGCUpdateComicBookStat_Type
    ]
    CMsgClientToGCUpdateComicBookStat_Type_HighestPercentRead: _ClassVar[
        CMsgClientToGCUpdateComicBookStat_Type
    ]

CMsgDOTARequestMatches_SkillLevel_Any: CMsgDOTARequestMatches_SkillLevel
CMsgDOTARequestMatches_SkillLevel_Normal: CMsgDOTARequestMatches_SkillLevel
CMsgDOTARequestMatches_SkillLevel_High: CMsgDOTARequestMatches_SkillLevel
CMsgDOTARequestMatches_SkillLevel_VeryHigh: CMsgDOTARequestMatches_SkillLevel
DOTA_WATCH_REPLAY_NORMAL: DOTA_WatchReplayType
DOTA_WATCH_REPLAY_HIGHLIGHTS: DOTA_WatchReplayType
k_EItemEditorReservationResult_OK: EItemEditorReservationResult
k_EItemEditorReservationResult_AlreadyExists: EItemEditorReservationResult
k_EItemEditorReservationResult_Reserved: EItemEditorReservationResult
k_EItemEditorReservationResult_TimedOut: EItemEditorReservationResult
k_EWeekendTourneyRichPresenceEvent_None: EWeekendTourneyRichPresenceEvent
k_EWeekendTourneyRichPresenceEvent_StartedMatch: EWeekendTourneyRichPresenceEvent
k_EWeekendTourneyRichPresenceEvent_WonMatch: EWeekendTourneyRichPresenceEvent
k_EWeekendTourneyRichPresenceEvent_Eliminated: EWeekendTourneyRichPresenceEvent
k_EDOTATriviaAnswerResult_Success: EDOTATriviaAnswerResult
k_EDOTATriviaAnswerResult_InvalidQuestion: EDOTATriviaAnswerResult
k_EDOTATriviaAnswerResult_InvalidAnswer: EDOTATriviaAnswerResult
k_EDOTATriviaAnswerResult_QuestionLocked: EDOTATriviaAnswerResult
k_EDOTATriviaAnswerResult_AlreadyAnswered: EDOTATriviaAnswerResult
k_EDOTATriviaAnswerResult_TriviaDisabled: EDOTATriviaAnswerResult
k_EPurchaseHeroRelicResult_Success: EPurchaseHeroRelicResult
k_EPurchaseHeroRelicResult_FailedToSend: EPurchaseHeroRelicResult
k_EPurchaseHeroRelicResult_NotEnoughPoints: EPurchaseHeroRelicResult
k_EPurchaseHeroRelicResult_InternalServerError: EPurchaseHeroRelicResult
k_EPurchaseHeroRelicResult_PurchaseNotAllowed: EPurchaseHeroRelicResult
k_EPurchaseHeroRelicResult_InvalidRelic: EPurchaseHeroRelicResult
k_EPurchaseHeroRelicResult_AlreadyOwned: EPurchaseHeroRelicResult
k_EPurchaseHeroRelicResult_InvalidRarity: EPurchaseHeroRelicResult
k_EDevEventRequestResult_Success: EDevEventRequestResult
k_EDevEventRequestResult_NotAllowed: EDevEventRequestResult
k_EDevEventRequestResult_InvalidEvent: EDevEventRequestResult
k_EDevEventRequestResult_SqlFailure: EDevEventRequestResult
k_EDevEventRequestResult_Timeout: EDevEventRequestResult
k_EDevEventRequestResult_LockFailure: EDevEventRequestResult
k_EDevEventRequestResult_SDOLoadFailure: EDevEventRequestResult
k_ESupportEventRequestResult_Success: ESupportEventRequestResult
k_ESupportEventRequestResult_Timeout: ESupportEventRequestResult
k_ESupportEventRequestResult_CantLockSOCache: ESupportEventRequestResult
k_ESupportEventRequestResult_ItemNotInInventory: ESupportEventRequestResult
k_ESupportEventRequestResult_InvalidItemDef: ESupportEventRequestResult
k_ESupportEventRequestResult_InvalidEvent: ESupportEventRequestResult
k_ESupportEventRequestResult_EventExpired: ESupportEventRequestResult
k_ESupportEventRequestResult_InvalidSupportAccount: ESupportEventRequestResult
k_ESupportEventRequestResult_InvalidSupportMessage: ESupportEventRequestResult
k_ESupportEventRequestResult_InvalidEventPoints: ESupportEventRequestResult
k_ESupportEventRequestResult_InvalidPremiumPoints: ESupportEventRequestResult
k_ESupportEventRequestResult_InvalidActionID: ESupportEventRequestResult
k_ESupportEventRequestResult_InvalidActionScore: ESupportEventRequestResult
k_ESupportEventRequestResult_TransactionFailed: ESupportEventRequestResult
k_eInternalError: EUnderDraftResponse
k_eSuccess: EUnderDraftResponse
k_eNoGold: EUnderDraftResponse
k_eInvalidSlot: EUnderDraftResponse
k_eNoBenchSpace: EUnderDraftResponse
k_eNoTickets: EUnderDraftResponse
k_eEventNotOwned: EUnderDraftResponse
k_eInvalidReward: EUnderDraftResponse
k_eHasBigReward: EUnderDraftResponse
k_eNoGCConnection: EUnderDraftResponse
k_eTooBusy: EUnderDraftResponse
k_eCantRollBack: EUnderDraftResponse
k_EDOTADraftTriviaAnswerResult_Success: EDOTADraftTriviaAnswerResult
k_EDOTADraftTriviaAnswerResult_InvalidMatchID: EDOTADraftTriviaAnswerResult
k_EDOTADraftTriviaAnswerResult_AlreadyAnswered: EDOTADraftTriviaAnswerResult
k_EDOTADraftTriviaAnswerResult_InternalError: EDOTADraftTriviaAnswerResult
k_EDOTADraftTriviaAnswerResult_TriviaDisabled: EDOTADraftTriviaAnswerResult
k_EDOTADraftTriviaAnswerResult_GCDown: EDOTADraftTriviaAnswerResult
CMsgClientToGCUpdateComicBookStat_Type_HighestPageRead: CMsgClientToGCUpdateComicBookStat_Type
CMsgClientToGCUpdateComicBookStat_Type_SecondsSpentReading: CMsgClientToGCUpdateComicBookStat_Type
CMsgClientToGCUpdateComicBookStat_Type_HighestPercentRead: CMsgClientToGCUpdateComicBookStat_Type

class CMsgClientSuspended(_message.Message):
    __slots__ = ("time_end",)
    TIME_END_FIELD_NUMBER: _ClassVar[int]
    time_end: int
    def __init__(self, time_end: int | None = ...) -> None: ...

class CMsgBalancedShuffleLobby(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgInitialQuestionnaireResponse(_message.Message):
    __slots__ = ("initial_skill",)
    INITIAL_SKILL_FIELD_NUMBER: _ClassVar[int]
    initial_skill: int
    def __init__(self, initial_skill: int | None = ...) -> None: ...

class CMsgDOTARequestMatchesResponse(_message.Message):
    __slots__ = ("matches", "series", "request_id", "total_results", "results_remaining")
    class Series(_message.Message):
        __slots__ = ("matches", "series_id", "series_type")
        MATCHES_FIELD_NUMBER: _ClassVar[int]
        SERIES_ID_FIELD_NUMBER: _ClassVar[int]
        SERIES_TYPE_FIELD_NUMBER: _ClassVar[int]
        matches: _containers.RepeatedCompositeFieldContainer[
            _dota_gcmessages_common_pb2.CMsgDOTAMatch
        ]
        series_id: int
        series_type: int
        def __init__(
            self,
            matches: _Iterable[_dota_gcmessages_common_pb2.CMsgDOTAMatch | _Mapping] | None = ...,
            series_id: int | None = ...,
            series_type: int | None = ...,
        ) -> None: ...

    MATCHES_FIELD_NUMBER: _ClassVar[int]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    TOTAL_RESULTS_FIELD_NUMBER: _ClassVar[int]
    RESULTS_REMAINING_FIELD_NUMBER: _ClassVar[int]
    matches: _containers.RepeatedCompositeFieldContainer[_dota_gcmessages_common_pb2.CMsgDOTAMatch]
    series: _containers.RepeatedCompositeFieldContainer[CMsgDOTARequestMatchesResponse.Series]
    request_id: int
    total_results: int
    results_remaining: int
    def __init__(
        self,
        matches: _Iterable[_dota_gcmessages_common_pb2.CMsgDOTAMatch | _Mapping] | None = ...,
        series: _Iterable[CMsgDOTARequestMatchesResponse.Series | _Mapping] | None = ...,
        request_id: int | None = ...,
        total_results: int | None = ...,
        results_remaining: int | None = ...,
    ) -> None: ...

class CMsgDOTAPopup(_message.Message):
    __slots__ = (
        "id",
        "custom_text",
        "int_data",
        "popup_data",
        "loc_token_header",
        "loc_token_msg",
        "var_names",
        "var_values",
        "debug_text",
    )
    class PopupID(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NONE: _ClassVar[CMsgDOTAPopup.PopupID]
        KICKED_FROM_LOBBY: _ClassVar[CMsgDOTAPopup.PopupID]
        KICKED_FROM_PARTY: _ClassVar[CMsgDOTAPopup.PopupID]
        KICKED_FROM_TEAM: _ClassVar[CMsgDOTAPopup.PopupID]
        TEAM_WAS_DISBANDED: _ClassVar[CMsgDOTAPopup.PopupID]
        TEAM_MATCHMAKE_ALREADY_MATCH: _ClassVar[CMsgDOTAPopup.PopupID]
        TEAM_MATCHMAKE_ALREADY_FINDING: _ClassVar[CMsgDOTAPopup.PopupID]
        TEAM_MATCHMAKE_FULL: _ClassVar[CMsgDOTAPopup.PopupID]
        TEAM_MATCHMAKE_FAIL_ADD: _ClassVar[CMsgDOTAPopup.PopupID]
        TEAM_MATCHMAKE_FAIL_ADD_CURRENT: _ClassVar[CMsgDOTAPopup.PopupID]
        TEAM_MATCHMAKE_FAILED_TEAM_MEMBER: _ClassVar[CMsgDOTAPopup.PopupID]
        TEAM_MATCHMAKE_ALREADY_GAME: _ClassVar[CMsgDOTAPopup.PopupID]
        TEAM_MATCHMAKE_FAIL_GET_PARTY: _ClassVar[CMsgDOTAPopup.PopupID]
        MATCHMAKING_DISABLED: _ClassVar[CMsgDOTAPopup.PopupID]
        INVITE_DENIED: _ClassVar[CMsgDOTAPopup.PopupID]
        PARTY_FULL: _ClassVar[CMsgDOTAPopup.PopupID]
        MADE_ADMIN: _ClassVar[CMsgDOTAPopup.PopupID]
        NEED_TO_PURCHASE: _ClassVar[CMsgDOTAPopup.PopupID]
        SIGNON_MESSAGE: _ClassVar[CMsgDOTAPopup.PopupID]
        MATCHMAKING_REGION_OFFLINE: _ClassVar[CMsgDOTAPopup.PopupID]
        TOURNAMENT_GAME_NOT_FOUND: _ClassVar[CMsgDOTAPopup.PopupID]
        TOURNAMENT_GAME_HAS_LOBBY_ID: _ClassVar[CMsgDOTAPopup.PopupID]
        TOURNAMENT_GAME_HAS_MATCH_ID: _ClassVar[CMsgDOTAPopup.PopupID]
        TOURNAMENT_GAME_HAS_NO_RADIANT_TEAM: _ClassVar[CMsgDOTAPopup.PopupID]
        TOURNAMENT_GAME_HAS_NO_DIRE_TEAM: _ClassVar[CMsgDOTAPopup.PopupID]
        TOURNAMENT_GAME_SQL_UPDATE_FAILED: _ClassVar[CMsgDOTAPopup.PopupID]
        NOT_LEAGUE_ADMIN: _ClassVar[CMsgDOTAPopup.PopupID]
        IN_ANOTHER_GAME: _ClassVar[CMsgDOTAPopup.PopupID]
        PARTY_MEMBER_IN_ANOTHER_GAME: _ClassVar[CMsgDOTAPopup.PopupID]
        PARTY_MEMBER_IN_LOW_PRIORITY: _ClassVar[CMsgDOTAPopup.PopupID]
        CLIENT_OUT_OF_DATE: _ClassVar[CMsgDOTAPopup.PopupID]
        SAVE_GAME_CORRUPT: _ClassVar[CMsgDOTAPopup.PopupID]
        INSUFFICIENT_INGOTS: _ClassVar[CMsgDOTAPopup.PopupID]
        COMPETITIVE_MM_NOT_ENOUGH_PLAY_TIME_PLAY_MORE_CASUAL: _ClassVar[CMsgDOTAPopup.PopupID]
        PARTY_LEADER_JOINED_LOBBY: _ClassVar[CMsgDOTAPopup.PopupID]
        WEEKEND_TOURNEY_UNMATCHED: _ClassVar[CMsgDOTAPopup.PopupID]
        POST_MATCH_SURVEY: _ClassVar[CMsgDOTAPopup.PopupID]
        TROPHY_AWARDED: _ClassVar[CMsgDOTAPopup.PopupID]
        TROPHY_LEVEL_UP: _ClassVar[CMsgDOTAPopup.PopupID]
        ALL_HERO_CHALLENGE_PROGRESS: _ClassVar[CMsgDOTAPopup.PopupID]
        NEED_INITIAL_SKILL: _ClassVar[CMsgDOTAPopup.PopupID]
        NEED_INITIAL_SKILL_IN_PARTY: _ClassVar[CMsgDOTAPopup.PopupID]
        TARGET_ENGINE_MISMATCH: _ClassVar[CMsgDOTAPopup.PopupID]
        VAC_NOT_VERIFIED: _ClassVar[CMsgDOTAPopup.PopupID]
        KICKED_FROM_QUEUE_EVENT_STARTING: _ClassVar[CMsgDOTAPopup.PopupID]
        KICKED_FROM_QUEUE_EVENT_ENDING: _ClassVar[CMsgDOTAPopup.PopupID]
        LOBBY_FULL: _ClassVar[CMsgDOTAPopup.PopupID]
        EVENT_POINTS_EARNED: _ClassVar[CMsgDOTAPopup.PopupID]
        CUSTOM_GAME_INCORRECT_VERSION: _ClassVar[CMsgDOTAPopup.PopupID]
        LIMITED_USER_CHAT: _ClassVar[CMsgDOTAPopup.PopupID]
        EVENT_PREMIUM_POINTS_EARNED: _ClassVar[CMsgDOTAPopup.PopupID]
        LOBBY_MVP_AWARDED: _ClassVar[CMsgDOTAPopup.PopupID]
        LOW_BADGE_LEVEL_CHAT: _ClassVar[CMsgDOTAPopup.PopupID]
        LOW_WINS_CHAT: _ClassVar[CMsgDOTAPopup.PopupID]
        UNVERIFIED_USER_CHAT: _ClassVar[CMsgDOTAPopup.PopupID]
        PARTY_STARTED_FINDING_EVENT_MATCH: _ClassVar[CMsgDOTAPopup.PopupID]
        GENERIC_INFO: _ClassVar[CMsgDOTAPopup.PopupID]
        GENERIC_ERROR: _ClassVar[CMsgDOTAPopup.PopupID]
        RANK_TIER_UPDATED: _ClassVar[CMsgDOTAPopup.PopupID]
        CUSTOM_GAME_COOLDOWN_RESTRICTED: _ClassVar[CMsgDOTAPopup.PopupID]
        CREATE_LOBBY_FAILED_TOO_MUCH_PLAYTIME: _ClassVar[CMsgDOTAPopup.PopupID]
        CUSTOM_GAME_TOO_FEW_GAMES: _ClassVar[CMsgDOTAPopup.PopupID]
        COMM_SCORE_TOO_LOW: _ClassVar[CMsgDOTAPopup.PopupID]

    NONE: CMsgDOTAPopup.PopupID
    KICKED_FROM_LOBBY: CMsgDOTAPopup.PopupID
    KICKED_FROM_PARTY: CMsgDOTAPopup.PopupID
    KICKED_FROM_TEAM: CMsgDOTAPopup.PopupID
    TEAM_WAS_DISBANDED: CMsgDOTAPopup.PopupID
    TEAM_MATCHMAKE_ALREADY_MATCH: CMsgDOTAPopup.PopupID
    TEAM_MATCHMAKE_ALREADY_FINDING: CMsgDOTAPopup.PopupID
    TEAM_MATCHMAKE_FULL: CMsgDOTAPopup.PopupID
    TEAM_MATCHMAKE_FAIL_ADD: CMsgDOTAPopup.PopupID
    TEAM_MATCHMAKE_FAIL_ADD_CURRENT: CMsgDOTAPopup.PopupID
    TEAM_MATCHMAKE_FAILED_TEAM_MEMBER: CMsgDOTAPopup.PopupID
    TEAM_MATCHMAKE_ALREADY_GAME: CMsgDOTAPopup.PopupID
    TEAM_MATCHMAKE_FAIL_GET_PARTY: CMsgDOTAPopup.PopupID
    MATCHMAKING_DISABLED: CMsgDOTAPopup.PopupID
    INVITE_DENIED: CMsgDOTAPopup.PopupID
    PARTY_FULL: CMsgDOTAPopup.PopupID
    MADE_ADMIN: CMsgDOTAPopup.PopupID
    NEED_TO_PURCHASE: CMsgDOTAPopup.PopupID
    SIGNON_MESSAGE: CMsgDOTAPopup.PopupID
    MATCHMAKING_REGION_OFFLINE: CMsgDOTAPopup.PopupID
    TOURNAMENT_GAME_NOT_FOUND: CMsgDOTAPopup.PopupID
    TOURNAMENT_GAME_HAS_LOBBY_ID: CMsgDOTAPopup.PopupID
    TOURNAMENT_GAME_HAS_MATCH_ID: CMsgDOTAPopup.PopupID
    TOURNAMENT_GAME_HAS_NO_RADIANT_TEAM: CMsgDOTAPopup.PopupID
    TOURNAMENT_GAME_HAS_NO_DIRE_TEAM: CMsgDOTAPopup.PopupID
    TOURNAMENT_GAME_SQL_UPDATE_FAILED: CMsgDOTAPopup.PopupID
    NOT_LEAGUE_ADMIN: CMsgDOTAPopup.PopupID
    IN_ANOTHER_GAME: CMsgDOTAPopup.PopupID
    PARTY_MEMBER_IN_ANOTHER_GAME: CMsgDOTAPopup.PopupID
    PARTY_MEMBER_IN_LOW_PRIORITY: CMsgDOTAPopup.PopupID
    CLIENT_OUT_OF_DATE: CMsgDOTAPopup.PopupID
    SAVE_GAME_CORRUPT: CMsgDOTAPopup.PopupID
    INSUFFICIENT_INGOTS: CMsgDOTAPopup.PopupID
    COMPETITIVE_MM_NOT_ENOUGH_PLAY_TIME_PLAY_MORE_CASUAL: CMsgDOTAPopup.PopupID
    PARTY_LEADER_JOINED_LOBBY: CMsgDOTAPopup.PopupID
    WEEKEND_TOURNEY_UNMATCHED: CMsgDOTAPopup.PopupID
    POST_MATCH_SURVEY: CMsgDOTAPopup.PopupID
    TROPHY_AWARDED: CMsgDOTAPopup.PopupID
    TROPHY_LEVEL_UP: CMsgDOTAPopup.PopupID
    ALL_HERO_CHALLENGE_PROGRESS: CMsgDOTAPopup.PopupID
    NEED_INITIAL_SKILL: CMsgDOTAPopup.PopupID
    NEED_INITIAL_SKILL_IN_PARTY: CMsgDOTAPopup.PopupID
    TARGET_ENGINE_MISMATCH: CMsgDOTAPopup.PopupID
    VAC_NOT_VERIFIED: CMsgDOTAPopup.PopupID
    KICKED_FROM_QUEUE_EVENT_STARTING: CMsgDOTAPopup.PopupID
    KICKED_FROM_QUEUE_EVENT_ENDING: CMsgDOTAPopup.PopupID
    LOBBY_FULL: CMsgDOTAPopup.PopupID
    EVENT_POINTS_EARNED: CMsgDOTAPopup.PopupID
    CUSTOM_GAME_INCORRECT_VERSION: CMsgDOTAPopup.PopupID
    LIMITED_USER_CHAT: CMsgDOTAPopup.PopupID
    EVENT_PREMIUM_POINTS_EARNED: CMsgDOTAPopup.PopupID
    LOBBY_MVP_AWARDED: CMsgDOTAPopup.PopupID
    LOW_BADGE_LEVEL_CHAT: CMsgDOTAPopup.PopupID
    LOW_WINS_CHAT: CMsgDOTAPopup.PopupID
    UNVERIFIED_USER_CHAT: CMsgDOTAPopup.PopupID
    PARTY_STARTED_FINDING_EVENT_MATCH: CMsgDOTAPopup.PopupID
    GENERIC_INFO: CMsgDOTAPopup.PopupID
    GENERIC_ERROR: CMsgDOTAPopup.PopupID
    RANK_TIER_UPDATED: CMsgDOTAPopup.PopupID
    CUSTOM_GAME_COOLDOWN_RESTRICTED: CMsgDOTAPopup.PopupID
    CREATE_LOBBY_FAILED_TOO_MUCH_PLAYTIME: CMsgDOTAPopup.PopupID
    CUSTOM_GAME_TOO_FEW_GAMES: CMsgDOTAPopup.PopupID
    COMM_SCORE_TOO_LOW: CMsgDOTAPopup.PopupID
    ID_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_TEXT_FIELD_NUMBER: _ClassVar[int]
    INT_DATA_FIELD_NUMBER: _ClassVar[int]
    POPUP_DATA_FIELD_NUMBER: _ClassVar[int]
    LOC_TOKEN_HEADER_FIELD_NUMBER: _ClassVar[int]
    LOC_TOKEN_MSG_FIELD_NUMBER: _ClassVar[int]
    VAR_NAMES_FIELD_NUMBER: _ClassVar[int]
    VAR_VALUES_FIELD_NUMBER: _ClassVar[int]
    DEBUG_TEXT_FIELD_NUMBER: _ClassVar[int]
    id: CMsgDOTAPopup.PopupID
    custom_text: str
    int_data: int
    popup_data: bytes
    loc_token_header: str
    loc_token_msg: str
    var_names: _containers.RepeatedScalarFieldContainer[str]
    var_values: _containers.RepeatedScalarFieldContainer[str]
    debug_text: str
    def __init__(
        self,
        id: CMsgDOTAPopup.PopupID | str | None = ...,
        custom_text: str | None = ...,
        int_data: int | None = ...,
        popup_data: bytes | None = ...,
        loc_token_header: str | None = ...,
        loc_token_msg: str | None = ...,
        var_names: _Iterable[str] | None = ...,
        var_values: _Iterable[str] | None = ...,
        debug_text: str | None = ...,
    ) -> None: ...

class CMsgDOTAReportsRemainingRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgDOTAReportsRemainingResponse(_message.Message):
    __slots__ = (
        "num_positive_reports_remaining",
        "num_negative_reports_remaining",
        "num_positive_reports_total",
        "num_negative_reports_total",
        "num_comms_reports_remaining",
        "num_comms_reports_total",
    )
    NUM_POSITIVE_REPORTS_REMAINING_FIELD_NUMBER: _ClassVar[int]
    NUM_NEGATIVE_REPORTS_REMAINING_FIELD_NUMBER: _ClassVar[int]
    NUM_POSITIVE_REPORTS_TOTAL_FIELD_NUMBER: _ClassVar[int]
    NUM_NEGATIVE_REPORTS_TOTAL_FIELD_NUMBER: _ClassVar[int]
    NUM_COMMS_REPORTS_REMAINING_FIELD_NUMBER: _ClassVar[int]
    NUM_COMMS_REPORTS_TOTAL_FIELD_NUMBER: _ClassVar[int]
    num_positive_reports_remaining: int
    num_negative_reports_remaining: int
    num_positive_reports_total: int
    num_negative_reports_total: int
    num_comms_reports_remaining: int
    num_comms_reports_total: int
    def __init__(
        self,
        num_positive_reports_remaining: int | None = ...,
        num_negative_reports_remaining: int | None = ...,
        num_positive_reports_total: int | None = ...,
        num_negative_reports_total: int | None = ...,
        num_comms_reports_remaining: int | None = ...,
        num_comms_reports_total: int | None = ...,
    ) -> None: ...

class CMsgDOTASubmitPlayerReport(_message.Message):
    __slots__ = ("target_account_id", "report_flags", "lobby_id", "comment")
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    REPORT_FLAGS_FIELD_NUMBER: _ClassVar[int]
    LOBBY_ID_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    target_account_id: int
    report_flags: int
    lobby_id: int
    comment: str
    def __init__(
        self,
        target_account_id: int | None = ...,
        report_flags: int | None = ...,
        lobby_id: int | None = ...,
        comment: str | None = ...,
    ) -> None: ...

class CMsgDOTASubmitPlayerReportResponse(_message.Message):
    __slots__ = ("target_account_id", "report_flags", "debug_message", "enum_result")
    class EResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgDOTASubmitPlayerReportResponse.EResult]
        k_eSuccess: _ClassVar[CMsgDOTASubmitPlayerReportResponse.EResult]
        k_eDuplicateReport: _ClassVar[CMsgDOTASubmitPlayerReportResponse.EResult]
        k_eMixedReportFlags: _ClassVar[CMsgDOTASubmitPlayerReportResponse.EResult]
        k_eTooLate: _ClassVar[CMsgDOTASubmitPlayerReportResponse.EResult]
        k_eInvalidPregameReport: _ClassVar[CMsgDOTASubmitPlayerReportResponse.EResult]
        k_eHasntChatted: _ClassVar[CMsgDOTASubmitPlayerReportResponse.EResult]
        k_eInvalid: _ClassVar[CMsgDOTASubmitPlayerReportResponse.EResult]
        k_eOwnership: _ClassVar[CMsgDOTASubmitPlayerReportResponse.EResult]
        k_eMissingRequirements: _ClassVar[CMsgDOTASubmitPlayerReportResponse.EResult]
        k_eInvalidRoleReport: _ClassVar[CMsgDOTASubmitPlayerReportResponse.EResult]
        k_eInvalidCoachReport: _ClassVar[CMsgDOTASubmitPlayerReportResponse.EResult]
        k_eNoRemainingReports: _ClassVar[CMsgDOTASubmitPlayerReportResponse.EResult]
        k_eInvalidMember: _ClassVar[CMsgDOTASubmitPlayerReportResponse.EResult]

    k_eInternalError: CMsgDOTASubmitPlayerReportResponse.EResult
    k_eSuccess: CMsgDOTASubmitPlayerReportResponse.EResult
    k_eDuplicateReport: CMsgDOTASubmitPlayerReportResponse.EResult
    k_eMixedReportFlags: CMsgDOTASubmitPlayerReportResponse.EResult
    k_eTooLate: CMsgDOTASubmitPlayerReportResponse.EResult
    k_eInvalidPregameReport: CMsgDOTASubmitPlayerReportResponse.EResult
    k_eHasntChatted: CMsgDOTASubmitPlayerReportResponse.EResult
    k_eInvalid: CMsgDOTASubmitPlayerReportResponse.EResult
    k_eOwnership: CMsgDOTASubmitPlayerReportResponse.EResult
    k_eMissingRequirements: CMsgDOTASubmitPlayerReportResponse.EResult
    k_eInvalidRoleReport: CMsgDOTASubmitPlayerReportResponse.EResult
    k_eInvalidCoachReport: CMsgDOTASubmitPlayerReportResponse.EResult
    k_eNoRemainingReports: CMsgDOTASubmitPlayerReportResponse.EResult
    k_eInvalidMember: CMsgDOTASubmitPlayerReportResponse.EResult
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    REPORT_FLAGS_FIELD_NUMBER: _ClassVar[int]
    DEBUG_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ENUM_RESULT_FIELD_NUMBER: _ClassVar[int]
    target_account_id: int
    report_flags: int
    debug_message: str
    enum_result: CMsgDOTASubmitPlayerReportResponse.EResult
    def __init__(
        self,
        target_account_id: int | None = ...,
        report_flags: int | None = ...,
        debug_message: str | None = ...,
        enum_result: CMsgDOTASubmitPlayerReportResponse.EResult | str | None = ...,
    ) -> None: ...

class CMsgDOTASubmitPlayerAvoidRequest(_message.Message):
    __slots__ = ("target_account_id", "lobby_id", "user_note")
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    LOBBY_ID_FIELD_NUMBER: _ClassVar[int]
    USER_NOTE_FIELD_NUMBER: _ClassVar[int]
    target_account_id: int
    lobby_id: int
    user_note: str
    def __init__(
        self,
        target_account_id: int | None = ...,
        lobby_id: int | None = ...,
        user_note: str | None = ...,
    ) -> None: ...

class CMsgDOTASubmitPlayerAvoidRequestResponse(_message.Message):
    __slots__ = ("target_account_id", "result", "debug_message")
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    DEBUG_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    target_account_id: int
    result: int
    debug_message: str
    def __init__(
        self,
        target_account_id: int | None = ...,
        result: int | None = ...,
        debug_message: str | None = ...,
    ) -> None: ...

class CMsgDOTASubmitPlayerReportV2(_message.Message):
    __slots__ = (
        "target_account_id",
        "report_reason",
        "lobby_id",
        "game_time",
        "debug_slot",
        "debug_match_id",
    )
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    REPORT_REASON_FIELD_NUMBER: _ClassVar[int]
    LOBBY_ID_FIELD_NUMBER: _ClassVar[int]
    GAME_TIME_FIELD_NUMBER: _ClassVar[int]
    DEBUG_SLOT_FIELD_NUMBER: _ClassVar[int]
    DEBUG_MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    target_account_id: int
    report_reason: _containers.RepeatedScalarFieldContainer[int]
    lobby_id: int
    game_time: float
    debug_slot: int
    debug_match_id: int
    def __init__(
        self,
        target_account_id: int | None = ...,
        report_reason: _Iterable[int] | None = ...,
        lobby_id: int | None = ...,
        game_time: float | None = ...,
        debug_slot: int | None = ...,
        debug_match_id: int | None = ...,
    ) -> None: ...

class CMsgDOTASubmitPlayerReportResponseV2(_message.Message):
    __slots__ = ("target_account_id", "report_reason", "debug_message", "enum_result")
    class EResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgDOTASubmitPlayerReportResponseV2.EResult]
        k_eSuccess: _ClassVar[CMsgDOTASubmitPlayerReportResponseV2.EResult]
        k_eDuplicateReport: _ClassVar[CMsgDOTASubmitPlayerReportResponseV2.EResult]
        k_eMixedReportFlags: _ClassVar[CMsgDOTASubmitPlayerReportResponseV2.EResult]
        k_eTooLate: _ClassVar[CMsgDOTASubmitPlayerReportResponseV2.EResult]
        k_eInvalidPregameReport: _ClassVar[CMsgDOTASubmitPlayerReportResponseV2.EResult]
        k_eHasntChatted: _ClassVar[CMsgDOTASubmitPlayerReportResponseV2.EResult]
        k_eInvalid: _ClassVar[CMsgDOTASubmitPlayerReportResponseV2.EResult]
        k_eOwnership: _ClassVar[CMsgDOTASubmitPlayerReportResponseV2.EResult]
        k_eMissingRequirements: _ClassVar[CMsgDOTASubmitPlayerReportResponseV2.EResult]
        k_eInvalidRoleReport: _ClassVar[CMsgDOTASubmitPlayerReportResponseV2.EResult]
        k_eInvalidCoachReport: _ClassVar[CMsgDOTASubmitPlayerReportResponseV2.EResult]
        k_eNoRemainingReports: _ClassVar[CMsgDOTASubmitPlayerReportResponseV2.EResult]
        k_eInvalidMember: _ClassVar[CMsgDOTASubmitPlayerReportResponseV2.EResult]
        k_eCannotReportPartyMember: _ClassVar[CMsgDOTASubmitPlayerReportResponseV2.EResult]

    k_eInternalError: CMsgDOTASubmitPlayerReportResponseV2.EResult
    k_eSuccess: CMsgDOTASubmitPlayerReportResponseV2.EResult
    k_eDuplicateReport: CMsgDOTASubmitPlayerReportResponseV2.EResult
    k_eMixedReportFlags: CMsgDOTASubmitPlayerReportResponseV2.EResult
    k_eTooLate: CMsgDOTASubmitPlayerReportResponseV2.EResult
    k_eInvalidPregameReport: CMsgDOTASubmitPlayerReportResponseV2.EResult
    k_eHasntChatted: CMsgDOTASubmitPlayerReportResponseV2.EResult
    k_eInvalid: CMsgDOTASubmitPlayerReportResponseV2.EResult
    k_eOwnership: CMsgDOTASubmitPlayerReportResponseV2.EResult
    k_eMissingRequirements: CMsgDOTASubmitPlayerReportResponseV2.EResult
    k_eInvalidRoleReport: CMsgDOTASubmitPlayerReportResponseV2.EResult
    k_eInvalidCoachReport: CMsgDOTASubmitPlayerReportResponseV2.EResult
    k_eNoRemainingReports: CMsgDOTASubmitPlayerReportResponseV2.EResult
    k_eInvalidMember: CMsgDOTASubmitPlayerReportResponseV2.EResult
    k_eCannotReportPartyMember: CMsgDOTASubmitPlayerReportResponseV2.EResult
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    REPORT_REASON_FIELD_NUMBER: _ClassVar[int]
    DEBUG_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ENUM_RESULT_FIELD_NUMBER: _ClassVar[int]
    target_account_id: int
    report_reason: _containers.RepeatedScalarFieldContainer[int]
    debug_message: str
    enum_result: CMsgDOTASubmitPlayerReportResponseV2.EResult
    def __init__(
        self,
        target_account_id: int | None = ...,
        report_reason: _Iterable[int] | None = ...,
        debug_message: str | None = ...,
        enum_result: CMsgDOTASubmitPlayerReportResponseV2.EResult | str | None = ...,
    ) -> None: ...

class CMsgDOTASubmitLobbyMVPVote(_message.Message):
    __slots__ = ("target_account_id",)
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    target_account_id: int
    def __init__(self, target_account_id: int | None = ...) -> None: ...

class CMsgDOTASubmitLobbyMVPVoteResponse(_message.Message):
    __slots__ = ("target_account_id", "eresult")
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ERESULT_FIELD_NUMBER: _ClassVar[int]
    target_account_id: int
    eresult: int
    def __init__(self, target_account_id: int | None = ..., eresult: int | None = ...) -> None: ...

class CMsgDOTALobbyMVPAwarded(_message.Message):
    __slots__ = ("match_id", "mvp_account_id")
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    MVP_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    mvp_account_id: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self, match_id: int | None = ..., mvp_account_id: _Iterable[int] | None = ...
    ) -> None: ...

class CMsgDOTAKickedFromMatchmakingQueue(_message.Message):
    __slots__ = ("match_type",)
    MATCH_TYPE_FIELD_NUMBER: _ClassVar[int]
    match_type: _dota_shared_enums_pb2.MatchType
    def __init__(self, match_type: _dota_shared_enums_pb2.MatchType | str | None = ...) -> None: ...

class CMsgGCMatchDetailsRequest(_message.Message):
    __slots__ = ("match_id",)
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    def __init__(self, match_id: int | None = ...) -> None: ...

class CMsgGCMatchDetailsResponse(_message.Message):
    __slots__ = ("result", "match", "vote")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    MATCH_FIELD_NUMBER: _ClassVar[int]
    VOTE_FIELD_NUMBER: _ClassVar[int]
    result: int
    match: _dota_gcmessages_common_pb2.CMsgDOTAMatch
    vote: _dota_shared_enums_pb2.DOTAMatchVote
    def __init__(
        self,
        result: int | None = ...,
        match: _dota_gcmessages_common_pb2.CMsgDOTAMatch | _Mapping | None = ...,
        vote: _dota_shared_enums_pb2.DOTAMatchVote | str | None = ...,
    ) -> None: ...

class CMsgDOTAProfileTickets(_message.Message):
    __slots__ = ("result", "account_id", "league_passes")
    class LeaguePass(_message.Message):
        __slots__ = ("league_id", "item_def")
        LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
        ITEM_DEF_FIELD_NUMBER: _ClassVar[int]
        league_id: int
        item_def: int
        def __init__(self, league_id: int | None = ..., item_def: int | None = ...) -> None: ...

    RESULT_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    LEAGUE_PASSES_FIELD_NUMBER: _ClassVar[int]
    result: int
    account_id: int
    league_passes: _containers.RepeatedCompositeFieldContainer[CMsgDOTAProfileTickets.LeaguePass]
    def __init__(
        self,
        result: int | None = ...,
        account_id: int | None = ...,
        league_passes: _Iterable[CMsgDOTAProfileTickets.LeaguePass | _Mapping] | None = ...,
    ) -> None: ...

class CMsgClientToGCGetProfileTickets(_message.Message):
    __slots__ = ("account_id",)
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    def __init__(self, account_id: int | None = ...) -> None: ...

class CMsgGCToClientPartySearchInvites(_message.Message):
    __slots__ = ("invites",)
    INVITES_FIELD_NUMBER: _ClassVar[int]
    invites: _containers.RepeatedCompositeFieldContainer[CMsgGCToClientPartySearchInvite]
    def __init__(
        self, invites: _Iterable[CMsgGCToClientPartySearchInvite | _Mapping] | None = ...
    ) -> None: ...

class CMsgDOTAWelcome(_message.Message):
    __slots__ = (
        "store_item_hash",
        "timeplayedconsecutively",
        "allow_3rd_party_match_history",
        "last_ip_address",
        "profile_private",
        "currency",
        "should_request_player_origin",
        "gc_socache_file_version",
        "is_perfect_world_test_account",
        "extra_messages",
        "minimum_recent_item_id",
        "active_event",
        "additional_user_message",
        "custom_game_whitelist_version",
        "party_search_friend_invites",
        "remaining_playtime",
        "disable_guild_persona_info",
        "extra_message_blocks",
        "active_event_for_display",
    )
    class CExtraMsg(_message.Message):
        __slots__ = ("id", "contents")
        ID_FIELD_NUMBER: _ClassVar[int]
        CONTENTS_FIELD_NUMBER: _ClassVar[int]
        id: int
        contents: bytes
        def __init__(self, id: int | None = ..., contents: bytes | None = ...) -> None: ...

    STORE_ITEM_HASH_FIELD_NUMBER: _ClassVar[int]
    TIMEPLAYEDCONSECUTIVELY_FIELD_NUMBER: _ClassVar[int]
    ALLOW_3RD_PARTY_MATCH_HISTORY_FIELD_NUMBER: _ClassVar[int]
    LAST_IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PROFILE_PRIVATE_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    SHOULD_REQUEST_PLAYER_ORIGIN_FIELD_NUMBER: _ClassVar[int]
    GC_SOCACHE_FILE_VERSION_FIELD_NUMBER: _ClassVar[int]
    IS_PERFECT_WORLD_TEST_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    EXTRA_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    MINIMUM_RECENT_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_EVENT_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_USER_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_WHITELIST_VERSION_FIELD_NUMBER: _ClassVar[int]
    PARTY_SEARCH_FRIEND_INVITES_FIELD_NUMBER: _ClassVar[int]
    REMAINING_PLAYTIME_FIELD_NUMBER: _ClassVar[int]
    DISABLE_GUILD_PERSONA_INFO_FIELD_NUMBER: _ClassVar[int]
    EXTRA_MESSAGE_BLOCKS_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_EVENT_FOR_DISPLAY_FIELD_NUMBER: _ClassVar[int]
    store_item_hash: int
    timeplayedconsecutively: int
    allow_3rd_party_match_history: bool
    last_ip_address: int
    profile_private: bool
    currency: int
    should_request_player_origin: bool
    gc_socache_file_version: int
    is_perfect_world_test_account: bool
    extra_messages: _containers.RepeatedCompositeFieldContainer[CMsgDOTAWelcome.CExtraMsg]
    minimum_recent_item_id: int
    active_event: _dota_shared_enums_pb2.EEvent
    additional_user_message: int
    custom_game_whitelist_version: int
    party_search_friend_invites: CMsgGCToClientPartySearchInvites
    remaining_playtime: int
    disable_guild_persona_info: bool
    extra_message_blocks: _containers.RepeatedCompositeFieldContainer[
        _gcsdk_gcmessages_pb2.CExtraMsgBlock
    ]
    active_event_for_display: _dota_shared_enums_pb2.EEvent
    def __init__(
        self,
        store_item_hash: int | None = ...,
        timeplayedconsecutively: int | None = ...,
        allow_3rd_party_match_history: bool = ...,
        last_ip_address: int | None = ...,
        profile_private: bool = ...,
        currency: int | None = ...,
        should_request_player_origin: bool = ...,
        gc_socache_file_version: int | None = ...,
        is_perfect_world_test_account: bool = ...,
        extra_messages: _Iterable[CMsgDOTAWelcome.CExtraMsg | _Mapping] | None = ...,
        minimum_recent_item_id: int | None = ...,
        active_event: _dota_shared_enums_pb2.EEvent | str | None = ...,
        additional_user_message: int | None = ...,
        custom_game_whitelist_version: int | None = ...,
        party_search_friend_invites: CMsgGCToClientPartySearchInvites | _Mapping | None = ...,
        remaining_playtime: int | None = ...,
        disable_guild_persona_info: bool = ...,
        extra_message_blocks: _Iterable[_gcsdk_gcmessages_pb2.CExtraMsgBlock | _Mapping]
        | None = ...,
        active_event_for_display: _dota_shared_enums_pb2.EEvent | str | None = ...,
    ) -> None: ...

class CSODOTAGameHeroFavorites(_message.Message):
    __slots__ = ("account_id", "hero_id")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    hero_id: int
    def __init__(self, account_id: int | None = ..., hero_id: int | None = ...) -> None: ...

class CMsgDOTAMatchVotes(_message.Message):
    __slots__ = ("match_id", "votes")
    class PlayerVote(_message.Message):
        __slots__ = ("account_id", "vote")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        VOTE_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        vote: int
        def __init__(self, account_id: int | None = ..., vote: int | None = ...) -> None: ...

    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    VOTES_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    votes: _containers.RepeatedCompositeFieldContainer[CMsgDOTAMatchVotes.PlayerVote]
    def __init__(
        self,
        match_id: int | None = ...,
        votes: _Iterable[CMsgDOTAMatchVotes.PlayerVote | _Mapping] | None = ...,
    ) -> None: ...

class CMsgMatchmakingMatchGroupInfo(_message.Message):
    __slots__ = (
        "players_searching",
        "auto_region_select_ping_penalty",
        "auto_region_select_ping_penalty_custom",
        "status",
    )
    PLAYERS_SEARCHING_FIELD_NUMBER: _ClassVar[int]
    AUTO_REGION_SELECT_PING_PENALTY_FIELD_NUMBER: _ClassVar[int]
    AUTO_REGION_SELECT_PING_PENALTY_CUSTOM_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    players_searching: int
    auto_region_select_ping_penalty: int
    auto_region_select_ping_penalty_custom: int
    status: _dota_shared_enums_pb2.EMatchGroupServerStatus
    def __init__(
        self,
        players_searching: int | None = ...,
        auto_region_select_ping_penalty: int | None = ...,
        auto_region_select_ping_penalty_custom: int | None = ...,
        status: _dota_shared_enums_pb2.EMatchGroupServerStatus | str | None = ...,
    ) -> None: ...

class CMsgDOTAMatchmakingStatsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgDOTAMatchmakingStatsResponse(_message.Message):
    __slots__ = ("matchgroups_version", "legacy_searching_players_by_group_source2", "match_groups")
    MATCHGROUPS_VERSION_FIELD_NUMBER: _ClassVar[int]
    LEGACY_SEARCHING_PLAYERS_BY_GROUP_SOURCE2_FIELD_NUMBER: _ClassVar[int]
    MATCH_GROUPS_FIELD_NUMBER: _ClassVar[int]
    matchgroups_version: int
    legacy_searching_players_by_group_source2: _containers.RepeatedScalarFieldContainer[int]
    match_groups: _containers.RepeatedCompositeFieldContainer[CMsgMatchmakingMatchGroupInfo]
    def __init__(
        self,
        matchgroups_version: int | None = ...,
        legacy_searching_players_by_group_source2: _Iterable[int] | None = ...,
        match_groups: _Iterable[CMsgMatchmakingMatchGroupInfo | _Mapping] | None = ...,
    ) -> None: ...

class CMsgDOTAUpdateMatchmakingStats(_message.Message):
    __slots__ = ("stats",)
    STATS_FIELD_NUMBER: _ClassVar[int]
    stats: CMsgDOTAMatchmakingStatsResponse
    def __init__(self, stats: CMsgDOTAMatchmakingStatsResponse | _Mapping | None = ...) -> None: ...

class CMsgDOTAUpdateMatchManagementStats(_message.Message):
    __slots__ = ("stats",)
    STATS_FIELD_NUMBER: _ClassVar[int]
    stats: CMsgDOTAMatchmakingStatsResponse
    def __init__(self, stats: CMsgDOTAMatchmakingStatsResponse | _Mapping | None = ...) -> None: ...

class CMsgDOTASetMatchHistoryAccess(_message.Message):
    __slots__ = ("allow_3rd_party_match_history",)
    ALLOW_3RD_PARTY_MATCH_HISTORY_FIELD_NUMBER: _ClassVar[int]
    allow_3rd_party_match_history: bool
    def __init__(self, allow_3rd_party_match_history: bool = ...) -> None: ...

class CMsgDOTASetMatchHistoryAccessResponse(_message.Message):
    __slots__ = ("eresult",)
    ERESULT_FIELD_NUMBER: _ClassVar[int]
    eresult: int
    def __init__(self, eresult: int | None = ...) -> None: ...

class CMsgDOTANotifyAccountFlagsChange(_message.Message):
    __slots__ = ("accountid", "account_flags")
    ACCOUNTID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_FLAGS_FIELD_NUMBER: _ClassVar[int]
    accountid: int
    account_flags: int
    def __init__(self, accountid: int | None = ..., account_flags: int | None = ...) -> None: ...

class CMsgDOTASetProfilePrivacy(_message.Message):
    __slots__ = ("profile_private",)
    PROFILE_PRIVATE_FIELD_NUMBER: _ClassVar[int]
    profile_private: bool
    def __init__(self, profile_private: bool = ...) -> None: ...

class CMsgDOTASetProfilePrivacyResponse(_message.Message):
    __slots__ = ("eresult",)
    ERESULT_FIELD_NUMBER: _ClassVar[int]
    eresult: int
    def __init__(self, eresult: int | None = ...) -> None: ...

class CMsgUpgradeLeagueItem(_message.Message):
    __slots__ = ("match_id", "league_id")
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    league_id: int
    def __init__(self, match_id: int | None = ..., league_id: int | None = ...) -> None: ...

class CMsgUpgradeLeagueItemResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgGCWatchDownloadedReplay(_message.Message):
    __slots__ = ("match_id", "watch_type")
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    WATCH_TYPE_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    watch_type: DOTA_WatchReplayType
    def __init__(
        self, match_id: int | None = ..., watch_type: DOTA_WatchReplayType | str | None = ...
    ) -> None: ...

class CMsgClientToGCWatchingBroadcast(_message.Message):
    __slots__ = ("match_id",)
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    def __init__(self, match_id: int | None = ...) -> None: ...

class CMsgClientsRejoinChatChannels(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgGCGetHeroStandings(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgGCGetHeroStandingsResponse(_message.Message):
    __slots__ = ("standings",)
    class Hero(_message.Message):
        __slots__ = (
            "hero_id",
            "wins",
            "losses",
            "win_streak",
            "best_win_streak",
            "avg_kills",
            "avg_deaths",
            "avg_assists",
            "avg_gpm",
            "avg_xpm",
            "best_kills",
            "best_assists",
            "best_gpm",
            "best_xpm",
            "performance",
            "wins_with_ally",
            "losses_with_ally",
            "wins_against_enemy",
            "losses_against_enemy",
            "networth_peak",
            "lasthit_peak",
            "deny_peak",
            "damage_peak",
            "longest_game_peak",
            "healing_peak",
            "avg_lasthits",
            "avg_denies",
        )
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        WINS_FIELD_NUMBER: _ClassVar[int]
        LOSSES_FIELD_NUMBER: _ClassVar[int]
        WIN_STREAK_FIELD_NUMBER: _ClassVar[int]
        BEST_WIN_STREAK_FIELD_NUMBER: _ClassVar[int]
        AVG_KILLS_FIELD_NUMBER: _ClassVar[int]
        AVG_DEATHS_FIELD_NUMBER: _ClassVar[int]
        AVG_ASSISTS_FIELD_NUMBER: _ClassVar[int]
        AVG_GPM_FIELD_NUMBER: _ClassVar[int]
        AVG_XPM_FIELD_NUMBER: _ClassVar[int]
        BEST_KILLS_FIELD_NUMBER: _ClassVar[int]
        BEST_ASSISTS_FIELD_NUMBER: _ClassVar[int]
        BEST_GPM_FIELD_NUMBER: _ClassVar[int]
        BEST_XPM_FIELD_NUMBER: _ClassVar[int]
        PERFORMANCE_FIELD_NUMBER: _ClassVar[int]
        WINS_WITH_ALLY_FIELD_NUMBER: _ClassVar[int]
        LOSSES_WITH_ALLY_FIELD_NUMBER: _ClassVar[int]
        WINS_AGAINST_ENEMY_FIELD_NUMBER: _ClassVar[int]
        LOSSES_AGAINST_ENEMY_FIELD_NUMBER: _ClassVar[int]
        NETWORTH_PEAK_FIELD_NUMBER: _ClassVar[int]
        LASTHIT_PEAK_FIELD_NUMBER: _ClassVar[int]
        DENY_PEAK_FIELD_NUMBER: _ClassVar[int]
        DAMAGE_PEAK_FIELD_NUMBER: _ClassVar[int]
        LONGEST_GAME_PEAK_FIELD_NUMBER: _ClassVar[int]
        HEALING_PEAK_FIELD_NUMBER: _ClassVar[int]
        AVG_LASTHITS_FIELD_NUMBER: _ClassVar[int]
        AVG_DENIES_FIELD_NUMBER: _ClassVar[int]
        hero_id: int
        wins: int
        losses: int
        win_streak: int
        best_win_streak: int
        avg_kills: float
        avg_deaths: float
        avg_assists: float
        avg_gpm: float
        avg_xpm: float
        best_kills: int
        best_assists: int
        best_gpm: int
        best_xpm: int
        performance: float
        wins_with_ally: int
        losses_with_ally: int
        wins_against_enemy: int
        losses_against_enemy: int
        networth_peak: int
        lasthit_peak: int
        deny_peak: int
        damage_peak: int
        longest_game_peak: int
        healing_peak: int
        avg_lasthits: float
        avg_denies: float
        def __init__(
            self,
            hero_id: int | None = ...,
            wins: int | None = ...,
            losses: int | None = ...,
            win_streak: int | None = ...,
            best_win_streak: int | None = ...,
            avg_kills: float | None = ...,
            avg_deaths: float | None = ...,
            avg_assists: float | None = ...,
            avg_gpm: float | None = ...,
            avg_xpm: float | None = ...,
            best_kills: int | None = ...,
            best_assists: int | None = ...,
            best_gpm: int | None = ...,
            best_xpm: int | None = ...,
            performance: float | None = ...,
            wins_with_ally: int | None = ...,
            losses_with_ally: int | None = ...,
            wins_against_enemy: int | None = ...,
            losses_against_enemy: int | None = ...,
            networth_peak: int | None = ...,
            lasthit_peak: int | None = ...,
            deny_peak: int | None = ...,
            damage_peak: int | None = ...,
            longest_game_peak: int | None = ...,
            healing_peak: int | None = ...,
            avg_lasthits: float | None = ...,
            avg_denies: float | None = ...,
        ) -> None: ...

    STANDINGS_FIELD_NUMBER: _ClassVar[int]
    standings: _containers.RepeatedCompositeFieldContainer[CMsgGCGetHeroStandingsResponse.Hero]
    def __init__(
        self, standings: _Iterable[CMsgGCGetHeroStandingsResponse.Hero | _Mapping] | None = ...
    ) -> None: ...

class CMatchPlayerTimedStatAverages(_message.Message):
    __slots__ = (
        "kills",
        "deaths",
        "assists",
        "net_worth",
        "last_hits",
        "denies",
        "item_value",
        "support_gold_spent",
        "camps_stacked",
        "wards_placed",
        "dewards",
        "triple_kills",
        "rampages",
    )
    KILLS_FIELD_NUMBER: _ClassVar[int]
    DEATHS_FIELD_NUMBER: _ClassVar[int]
    ASSISTS_FIELD_NUMBER: _ClassVar[int]
    NET_WORTH_FIELD_NUMBER: _ClassVar[int]
    LAST_HITS_FIELD_NUMBER: _ClassVar[int]
    DENIES_FIELD_NUMBER: _ClassVar[int]
    ITEM_VALUE_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_GOLD_SPENT_FIELD_NUMBER: _ClassVar[int]
    CAMPS_STACKED_FIELD_NUMBER: _ClassVar[int]
    WARDS_PLACED_FIELD_NUMBER: _ClassVar[int]
    DEWARDS_FIELD_NUMBER: _ClassVar[int]
    TRIPLE_KILLS_FIELD_NUMBER: _ClassVar[int]
    RAMPAGES_FIELD_NUMBER: _ClassVar[int]
    kills: float
    deaths: float
    assists: float
    net_worth: float
    last_hits: float
    denies: float
    item_value: float
    support_gold_spent: float
    camps_stacked: float
    wards_placed: float
    dewards: float
    triple_kills: float
    rampages: float
    def __init__(
        self,
        kills: float | None = ...,
        deaths: float | None = ...,
        assists: float | None = ...,
        net_worth: float | None = ...,
        last_hits: float | None = ...,
        denies: float | None = ...,
        item_value: float | None = ...,
        support_gold_spent: float | None = ...,
        camps_stacked: float | None = ...,
        wards_placed: float | None = ...,
        dewards: float | None = ...,
        triple_kills: float | None = ...,
        rampages: float | None = ...,
    ) -> None: ...

class CMatchPlayerTimedStatStdDeviations(_message.Message):
    __slots__ = (
        "kills",
        "deaths",
        "assists",
        "net_worth",
        "last_hits",
        "denies",
        "item_value",
        "support_gold_spent",
        "camps_stacked",
        "wards_placed",
        "dewards",
        "triple_kills",
        "rampages",
    )
    KILLS_FIELD_NUMBER: _ClassVar[int]
    DEATHS_FIELD_NUMBER: _ClassVar[int]
    ASSISTS_FIELD_NUMBER: _ClassVar[int]
    NET_WORTH_FIELD_NUMBER: _ClassVar[int]
    LAST_HITS_FIELD_NUMBER: _ClassVar[int]
    DENIES_FIELD_NUMBER: _ClassVar[int]
    ITEM_VALUE_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_GOLD_SPENT_FIELD_NUMBER: _ClassVar[int]
    CAMPS_STACKED_FIELD_NUMBER: _ClassVar[int]
    WARDS_PLACED_FIELD_NUMBER: _ClassVar[int]
    DEWARDS_FIELD_NUMBER: _ClassVar[int]
    TRIPLE_KILLS_FIELD_NUMBER: _ClassVar[int]
    RAMPAGES_FIELD_NUMBER: _ClassVar[int]
    kills: float
    deaths: float
    assists: float
    net_worth: float
    last_hits: float
    denies: float
    item_value: float
    support_gold_spent: float
    camps_stacked: float
    wards_placed: float
    dewards: float
    triple_kills: float
    rampages: float
    def __init__(
        self,
        kills: float | None = ...,
        deaths: float | None = ...,
        assists: float | None = ...,
        net_worth: float | None = ...,
        last_hits: float | None = ...,
        denies: float | None = ...,
        item_value: float | None = ...,
        support_gold_spent: float | None = ...,
        camps_stacked: float | None = ...,
        wards_placed: float | None = ...,
        dewards: float | None = ...,
        triple_kills: float | None = ...,
        rampages: float | None = ...,
    ) -> None: ...

class CMsgGCGetHeroTimedStatsResponse(_message.Message):
    __slots__ = ("hero_id", "rank_chunked_stats")
    class TimedStatsContainer(_message.Message):
        __slots__ = (
            "time",
            "all_stats",
            "winning_stats",
            "losing_stats",
            "winning_stddevs",
            "losing_stddevs",
        )
        TIME_FIELD_NUMBER: _ClassVar[int]
        ALL_STATS_FIELD_NUMBER: _ClassVar[int]
        WINNING_STATS_FIELD_NUMBER: _ClassVar[int]
        LOSING_STATS_FIELD_NUMBER: _ClassVar[int]
        WINNING_STDDEVS_FIELD_NUMBER: _ClassVar[int]
        LOSING_STDDEVS_FIELD_NUMBER: _ClassVar[int]
        time: int
        all_stats: CMatchPlayerTimedStatAverages
        winning_stats: CMatchPlayerTimedStatAverages
        losing_stats: CMatchPlayerTimedStatAverages
        winning_stddevs: CMatchPlayerTimedStatStdDeviations
        losing_stddevs: CMatchPlayerTimedStatStdDeviations
        def __init__(
            self,
            time: int | None = ...,
            all_stats: CMatchPlayerTimedStatAverages | _Mapping | None = ...,
            winning_stats: CMatchPlayerTimedStatAverages | _Mapping | None = ...,
            losing_stats: CMatchPlayerTimedStatAverages | _Mapping | None = ...,
            winning_stddevs: CMatchPlayerTimedStatStdDeviations | _Mapping | None = ...,
            losing_stddevs: CMatchPlayerTimedStatStdDeviations | _Mapping | None = ...,
        ) -> None: ...

    class RankChunkedStats(_message.Message):
        __slots__ = ("rank_chunk", "timed_stats")
        RANK_CHUNK_FIELD_NUMBER: _ClassVar[int]
        TIMED_STATS_FIELD_NUMBER: _ClassVar[int]
        rank_chunk: int
        timed_stats: _containers.RepeatedCompositeFieldContainer[
            CMsgGCGetHeroTimedStatsResponse.TimedStatsContainer
        ]
        def __init__(
            self,
            rank_chunk: int | None = ...,
            timed_stats: _Iterable[CMsgGCGetHeroTimedStatsResponse.TimedStatsContainer | _Mapping]
            | None = ...,
        ) -> None: ...

    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    RANK_CHUNKED_STATS_FIELD_NUMBER: _ClassVar[int]
    hero_id: int
    rank_chunked_stats: _containers.RepeatedCompositeFieldContainer[
        CMsgGCGetHeroTimedStatsResponse.RankChunkedStats
    ]
    def __init__(
        self,
        hero_id: int | None = ...,
        rank_chunked_stats: _Iterable[CMsgGCGetHeroTimedStatsResponse.RankChunkedStats | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgGCItemEditorReservationsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgGCItemEditorReservation(_message.Message):
    __slots__ = ("def_index", "name")
    DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    def_index: int
    name: str
    def __init__(self, def_index: int | None = ..., name: str | None = ...) -> None: ...

class CMsgGCItemEditorReservationsResponse(_message.Message):
    __slots__ = ("reservations",)
    RESERVATIONS_FIELD_NUMBER: _ClassVar[int]
    reservations: _containers.RepeatedCompositeFieldContainer[CMsgGCItemEditorReservation]
    def __init__(
        self, reservations: _Iterable[CMsgGCItemEditorReservation | _Mapping] | None = ...
    ) -> None: ...

class CMsgGCItemEditorReserveItemDef(_message.Message):
    __slots__ = ("def_index", "username")
    DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    def_index: int
    username: str
    def __init__(self, def_index: int | None = ..., username: str | None = ...) -> None: ...

class CMsgGCItemEditorReserveItemDefResponse(_message.Message):
    __slots__ = ("def_index", "username", "result")
    DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    def_index: int
    username: str
    result: int
    def __init__(
        self, def_index: int | None = ..., username: str | None = ..., result: int | None = ...
    ) -> None: ...

class CMsgGCItemEditorReleaseReservation(_message.Message):
    __slots__ = ("def_index", "username")
    DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    def_index: int
    username: str
    def __init__(self, def_index: int | None = ..., username: str | None = ...) -> None: ...

class CMsgGCItemEditorReleaseReservationResponse(_message.Message):
    __slots__ = ("def_index", "released")
    DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
    RELEASED_FIELD_NUMBER: _ClassVar[int]
    def_index: int
    released: bool
    def __init__(self, def_index: int | None = ..., released: bool = ...) -> None: ...

class CMsgFlipLobbyTeams(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgGCLobbyUpdateBroadcastChannelInfo(_message.Message):
    __slots__ = ("channel_id", "country_code", "description", "language_code")
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_CODE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_CODE_FIELD_NUMBER: _ClassVar[int]
    channel_id: int
    country_code: str
    description: str
    language_code: str
    def __init__(
        self,
        channel_id: int | None = ...,
        country_code: str | None = ...,
        description: str | None = ...,
        language_code: str | None = ...,
    ) -> None: ...

class CMsgDOTAClaimEventActionData(_message.Message):
    __slots__ = ("grant_item_gift_data", "grant_item_choice_item_def")
    class GrantItemGiftData(_message.Message):
        __slots__ = ("give_to_account_id", "gift_message")
        GIVE_TO_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        GIFT_MESSAGE_FIELD_NUMBER: _ClassVar[int]
        give_to_account_id: int
        gift_message: str
        def __init__(
            self, give_to_account_id: int | None = ..., gift_message: str | None = ...
        ) -> None: ...

    GRANT_ITEM_GIFT_DATA_FIELD_NUMBER: _ClassVar[int]
    GRANT_ITEM_CHOICE_ITEM_DEF_FIELD_NUMBER: _ClassVar[int]
    grant_item_gift_data: CMsgDOTAClaimEventActionData.GrantItemGiftData
    grant_item_choice_item_def: int
    def __init__(
        self,
        grant_item_gift_data: CMsgDOTAClaimEventActionData.GrantItemGiftData
        | _Mapping
        | None = ...,
        grant_item_choice_item_def: int | None = ...,
    ) -> None: ...

class CMsgDOTAClaimEventAction(_message.Message):
    __slots__ = ("event_id", "action_id", "quantity", "data", "score_mode", "suppress_rewards")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_ID_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    SCORE_MODE_FIELD_NUMBER: _ClassVar[int]
    SUPPRESS_REWARDS_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    action_id: int
    quantity: int
    data: CMsgDOTAClaimEventActionData
    score_mode: _dota_shared_enums_pb2.EEventActionScoreMode
    suppress_rewards: bool
    def __init__(
        self,
        event_id: int | None = ...,
        action_id: int | None = ...,
        quantity: int | None = ...,
        data: CMsgDOTAClaimEventActionData | _Mapping | None = ...,
        score_mode: _dota_shared_enums_pb2.EEventActionScoreMode | str | None = ...,
        suppress_rewards: bool = ...,
    ) -> None: ...

class CMsgClientToGCClaimEventActionUsingItem(_message.Message):
    __slots__ = ("event_id", "action_id", "item_id", "quantity", "suppress_rewards")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    SUPPRESS_REWARDS_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    action_id: int
    item_id: int
    quantity: int
    suppress_rewards: bool
    def __init__(
        self,
        event_id: int | None = ...,
        action_id: int | None = ...,
        item_id: int | None = ...,
        quantity: int | None = ...,
        suppress_rewards: bool = ...,
    ) -> None: ...

class CMsgClientToGCClaimEventActionUsingItemResponse(_message.Message):
    __slots__ = ("action_results",)
    ACTION_RESULTS_FIELD_NUMBER: _ClassVar[int]
    action_results: _dota_gcmessages_common_pb2.CMsgDOTAClaimEventActionResponse
    def __init__(
        self,
        action_results: _dota_gcmessages_common_pb2.CMsgDOTAClaimEventActionResponse
        | _Mapping
        | None = ...,
    ) -> None: ...

class CMsgGCToClientClaimEventActionUsingItemCompleted(_message.Message):
    __slots__ = ("item_id", "action_results")
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_RESULTS_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    action_results: _dota_gcmessages_common_pb2.CMsgDOTAClaimEventActionResponse
    def __init__(
        self,
        item_id: int | None = ...,
        action_results: _dota_gcmessages_common_pb2.CMsgDOTAClaimEventActionResponse
        | _Mapping
        | None = ...,
    ) -> None: ...

class CMsgDOTAGetEventPoints(_message.Message):
    __slots__ = ("event_id", "account_id")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    account_id: int
    def __init__(self, event_id: int | None = ..., account_id: int | None = ...) -> None: ...

class CMsgDOTAGetEventPointsResponse(_message.Message):
    __slots__ = (
        "total_points",
        "total_premium_points",
        "event_id",
        "points",
        "premium_points",
        "completed_actions",
        "account_id",
        "owned",
        "audit_action",
        "active_season_id",
    )
    class Action(_message.Message):
        __slots__ = ("action_id", "times_completed")
        ACTION_ID_FIELD_NUMBER: _ClassVar[int]
        TIMES_COMPLETED_FIELD_NUMBER: _ClassVar[int]
        action_id: int
        times_completed: int
        def __init__(
            self, action_id: int | None = ..., times_completed: int | None = ...
        ) -> None: ...

    TOTAL_POINTS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PREMIUM_POINTS_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    PREMIUM_POINTS_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_ACTIONS_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    OWNED_FIELD_NUMBER: _ClassVar[int]
    AUDIT_ACTION_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    total_points: int
    total_premium_points: int
    event_id: int
    points: int
    premium_points: int
    completed_actions: _containers.RepeatedCompositeFieldContainer[
        CMsgDOTAGetEventPointsResponse.Action
    ]
    account_id: int
    owned: bool
    audit_action: int
    active_season_id: int
    def __init__(
        self,
        total_points: int | None = ...,
        total_premium_points: int | None = ...,
        event_id: int | None = ...,
        points: int | None = ...,
        premium_points: int | None = ...,
        completed_actions: _Iterable[CMsgDOTAGetEventPointsResponse.Action | _Mapping] | None = ...,
        account_id: int | None = ...,
        owned: bool = ...,
        audit_action: int | None = ...,
        active_season_id: int | None = ...,
    ) -> None: ...

class CMsgDOTAGetPeriodicResource(_message.Message):
    __slots__ = ("account_id", "periodic_resource_id", "timestamp")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    PERIODIC_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    periodic_resource_id: int
    timestamp: int
    def __init__(
        self,
        account_id: int | None = ...,
        periodic_resource_id: int | None = ...,
        timestamp: int | None = ...,
    ) -> None: ...

class CMsgDOTAGetPeriodicResourceResponse(_message.Message):
    __slots__ = ("periodic_resource_max", "periodic_resource_used")
    PERIODIC_RESOURCE_MAX_FIELD_NUMBER: _ClassVar[int]
    PERIODIC_RESOURCE_USED_FIELD_NUMBER: _ClassVar[int]
    periodic_resource_max: int
    periodic_resource_used: int
    def __init__(
        self, periodic_resource_max: int | None = ..., periodic_resource_used: int | None = ...
    ) -> None: ...

class CMsgDOTAPeriodicResourceUpdated(_message.Message):
    __slots__ = ("periodic_resource_key", "periodic_resource_value")
    PERIODIC_RESOURCE_KEY_FIELD_NUMBER: _ClassVar[int]
    PERIODIC_RESOURCE_VALUE_FIELD_NUMBER: _ClassVar[int]
    periodic_resource_key: CMsgDOTAGetPeriodicResource
    periodic_resource_value: CMsgDOTAGetPeriodicResourceResponse
    def __init__(
        self,
        periodic_resource_key: CMsgDOTAGetPeriodicResource | _Mapping | None = ...,
        periodic_resource_value: CMsgDOTAGetPeriodicResourceResponse | _Mapping | None = ...,
    ) -> None: ...

class CMsgDOTACompendiumSelection(_message.Message):
    __slots__ = ("selection_index", "selection", "leagueid")
    SELECTION_INDEX_FIELD_NUMBER: _ClassVar[int]
    SELECTION_FIELD_NUMBER: _ClassVar[int]
    LEAGUEID_FIELD_NUMBER: _ClassVar[int]
    selection_index: int
    selection: int
    leagueid: int
    def __init__(
        self,
        selection_index: int | None = ...,
        selection: int | None = ...,
        leagueid: int | None = ...,
    ) -> None: ...

class CMsgDOTACompendiumSelectionResponse(_message.Message):
    __slots__ = ("eresult",)
    ERESULT_FIELD_NUMBER: _ClassVar[int]
    eresult: int
    def __init__(self, eresult: int | None = ...) -> None: ...

class CMsgDOTACompendiumRemoveAllSelections(_message.Message):
    __slots__ = ("leagueid",)
    LEAGUEID_FIELD_NUMBER: _ClassVar[int]
    leagueid: int
    def __init__(self, leagueid: int | None = ...) -> None: ...

class CMsgDOTACompendiumRemoveAllSelectionsResponse(_message.Message):
    __slots__ = ("eresult",)
    ERESULT_FIELD_NUMBER: _ClassVar[int]
    eresult: int
    def __init__(self, eresult: int | None = ...) -> None: ...

class CMsgDOTACompendiumData(_message.Message):
    __slots__ = ("selections",)
    SELECTIONS_FIELD_NUMBER: _ClassVar[int]
    selections: _containers.RepeatedCompositeFieldContainer[CMsgDOTACompendiumSelection]
    def __init__(
        self, selections: _Iterable[CMsgDOTACompendiumSelection | _Mapping] | None = ...
    ) -> None: ...

class CMsgDOTACompendiumDataRequest(_message.Message):
    __slots__ = ("account_id", "leagueid")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    LEAGUEID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    leagueid: int
    def __init__(self, account_id: int | None = ..., leagueid: int | None = ...) -> None: ...

class CMsgDOTACompendiumDataResponse(_message.Message):
    __slots__ = ("account_id", "leagueid", "result", "compendium_data")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    LEAGUEID_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    COMPENDIUM_DATA_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    leagueid: int
    result: int
    compendium_data: CMsgDOTACompendiumData
    def __init__(
        self,
        account_id: int | None = ...,
        leagueid: int | None = ...,
        result: int | None = ...,
        compendium_data: CMsgDOTACompendiumData | _Mapping | None = ...,
    ) -> None: ...

class CMsgDOTAGetPlayerMatchHistory(_message.Message):
    __slots__ = (
        "account_id",
        "start_at_match_id",
        "matches_requested",
        "hero_id",
        "request_id",
        "include_practice_matches",
        "include_custom_games",
        "include_event_games",
    )
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    START_AT_MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    MATCHES_REQUESTED_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_PRACTICE_MATCHES_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_CUSTOM_GAMES_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_EVENT_GAMES_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    start_at_match_id: int
    matches_requested: int
    hero_id: int
    request_id: int
    include_practice_matches: bool
    include_custom_games: bool
    include_event_games: bool
    def __init__(
        self,
        account_id: int | None = ...,
        start_at_match_id: int | None = ...,
        matches_requested: int | None = ...,
        hero_id: int | None = ...,
        request_id: int | None = ...,
        include_practice_matches: bool = ...,
        include_custom_games: bool = ...,
        include_event_games: bool = ...,
    ) -> None: ...

class CMsgDOTAGetPlayerMatchHistoryResponse(_message.Message):
    __slots__ = ("matches", "request_id")
    class Match(_message.Message):
        __slots__ = (
            "match_id",
            "start_time",
            "hero_id",
            "winner",
            "game_mode",
            "rank_change",
            "previous_rank",
            "lobby_type",
            "solo_rank",
            "abandon",
            "duration",
            "engine",
            "active_plus_subscription",
            "seasonal_rank",
            "tourney_id",
            "tourney_round",
            "tourney_tier",
            "tourney_division",
            "team_id",
            "team_name",
            "ugc_team_ui_logo",
            "selected_facet",
        )
        MATCH_ID_FIELD_NUMBER: _ClassVar[int]
        START_TIME_FIELD_NUMBER: _ClassVar[int]
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        WINNER_FIELD_NUMBER: _ClassVar[int]
        GAME_MODE_FIELD_NUMBER: _ClassVar[int]
        RANK_CHANGE_FIELD_NUMBER: _ClassVar[int]
        PREVIOUS_RANK_FIELD_NUMBER: _ClassVar[int]
        LOBBY_TYPE_FIELD_NUMBER: _ClassVar[int]
        SOLO_RANK_FIELD_NUMBER: _ClassVar[int]
        ABANDON_FIELD_NUMBER: _ClassVar[int]
        DURATION_FIELD_NUMBER: _ClassVar[int]
        ENGINE_FIELD_NUMBER: _ClassVar[int]
        ACTIVE_PLUS_SUBSCRIPTION_FIELD_NUMBER: _ClassVar[int]
        SEASONAL_RANK_FIELD_NUMBER: _ClassVar[int]
        TOURNEY_ID_FIELD_NUMBER: _ClassVar[int]
        TOURNEY_ROUND_FIELD_NUMBER: _ClassVar[int]
        TOURNEY_TIER_FIELD_NUMBER: _ClassVar[int]
        TOURNEY_DIVISION_FIELD_NUMBER: _ClassVar[int]
        TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
        UGC_TEAM_UI_LOGO_FIELD_NUMBER: _ClassVar[int]
        SELECTED_FACET_FIELD_NUMBER: _ClassVar[int]
        match_id: int
        start_time: int
        hero_id: int
        winner: bool
        game_mode: int
        rank_change: int
        previous_rank: int
        lobby_type: int
        solo_rank: bool
        abandon: bool
        duration: int
        engine: int
        active_plus_subscription: bool
        seasonal_rank: bool
        tourney_id: int
        tourney_round: int
        tourney_tier: int
        tourney_division: int
        team_id: int
        team_name: str
        ugc_team_ui_logo: int
        selected_facet: int
        def __init__(
            self,
            match_id: int | None = ...,
            start_time: int | None = ...,
            hero_id: int | None = ...,
            winner: bool = ...,
            game_mode: int | None = ...,
            rank_change: int | None = ...,
            previous_rank: int | None = ...,
            lobby_type: int | None = ...,
            solo_rank: bool = ...,
            abandon: bool = ...,
            duration: int | None = ...,
            engine: int | None = ...,
            active_plus_subscription: bool = ...,
            seasonal_rank: bool = ...,
            tourney_id: int | None = ...,
            tourney_round: int | None = ...,
            tourney_tier: int | None = ...,
            tourney_division: int | None = ...,
            team_id: int | None = ...,
            team_name: str | None = ...,
            ugc_team_ui_logo: int | None = ...,
            selected_facet: int | None = ...,
        ) -> None: ...

    MATCHES_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    matches: _containers.RepeatedCompositeFieldContainer[
        CMsgDOTAGetPlayerMatchHistoryResponse.Match
    ]
    request_id: int
    def __init__(
        self,
        matches: _Iterable[CMsgDOTAGetPlayerMatchHistoryResponse.Match | _Mapping] | None = ...,
        request_id: int | None = ...,
    ) -> None: ...

class CMsgGCNotificationsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgGCNotifications_Notification(_message.Message):
    __slots__ = (
        "id",
        "type",
        "timestamp",
        "reference_a",
        "reference_b",
        "reference_c",
        "message",
        "unread",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_A_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_B_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_C_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    UNREAD_FIELD_NUMBER: _ClassVar[int]
    id: int
    type: int
    timestamp: int
    reference_a: int
    reference_b: int
    reference_c: int
    message: str
    unread: bool
    def __init__(
        self,
        id: int | None = ...,
        type: int | None = ...,
        timestamp: int | None = ...,
        reference_a: int | None = ...,
        reference_b: int | None = ...,
        reference_c: int | None = ...,
        message: str | None = ...,
        unread: bool = ...,
    ) -> None: ...

class CMsgGCNotificationsUpdate(_message.Message):
    __slots__ = ("result", "notifications")
    class EResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgGCNotificationsUpdate.EResult]
        ERROR_UNSPECIFIED: _ClassVar[CMsgGCNotificationsUpdate.EResult]

    SUCCESS: CMsgGCNotificationsUpdate.EResult
    ERROR_UNSPECIFIED: CMsgGCNotificationsUpdate.EResult
    RESULT_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATIONS_FIELD_NUMBER: _ClassVar[int]
    result: CMsgGCNotificationsUpdate.EResult
    notifications: _containers.RepeatedCompositeFieldContainer[CMsgGCNotifications_Notification]
    def __init__(
        self,
        result: CMsgGCNotificationsUpdate.EResult | str | None = ...,
        notifications: _Iterable[CMsgGCNotifications_Notification | _Mapping] | None = ...,
    ) -> None: ...

class CMsgGCNotificationsResponse(_message.Message):
    __slots__ = ("update",)
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    update: CMsgGCNotificationsUpdate
    def __init__(self, update: CMsgGCNotificationsUpdate | _Mapping | None = ...) -> None: ...

class CMsgGCNotificationsMarkReadRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgGCPlayerInfoSubmit(_message.Message):
    __slots__ = (
        "player_name",
        "country_code",
        "fantasy_role",
        "team_id",
        "sponsor",
        "accepted_pro_agreement",
        "registration_period",
        "real_name",
    )
    PLAYER_NAME_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_CODE_FIELD_NUMBER: _ClassVar[int]
    FANTASY_ROLE_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    SPONSOR_FIELD_NUMBER: _ClassVar[int]
    ACCEPTED_PRO_AGREEMENT_FIELD_NUMBER: _ClassVar[int]
    REGISTRATION_PERIOD_FIELD_NUMBER: _ClassVar[int]
    REAL_NAME_FIELD_NUMBER: _ClassVar[int]
    player_name: str
    country_code: str
    fantasy_role: int
    team_id: int
    sponsor: str
    accepted_pro_agreement: bool
    registration_period: int
    real_name: str
    def __init__(
        self,
        player_name: str | None = ...,
        country_code: str | None = ...,
        fantasy_role: int | None = ...,
        team_id: int | None = ...,
        sponsor: str | None = ...,
        accepted_pro_agreement: bool = ...,
        registration_period: int | None = ...,
        real_name: str | None = ...,
    ) -> None: ...

class CMsgGCPlayerInfoSubmitResponse(_message.Message):
    __slots__ = ("result",)
    class EResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgGCPlayerInfoSubmitResponse.EResult]
        ERROR_UNSPECIFIED: _ClassVar[CMsgGCPlayerInfoSubmitResponse.EResult]
        ERROR_INFO_LOCKED: _ClassVar[CMsgGCPlayerInfoSubmitResponse.EResult]
        ERROR_NOT_MEMBER_OF_TEAM: _ClassVar[CMsgGCPlayerInfoSubmitResponse.EResult]

    SUCCESS: CMsgGCPlayerInfoSubmitResponse.EResult
    ERROR_UNSPECIFIED: CMsgGCPlayerInfoSubmitResponse.EResult
    ERROR_INFO_LOCKED: CMsgGCPlayerInfoSubmitResponse.EResult
    ERROR_NOT_MEMBER_OF_TEAM: CMsgGCPlayerInfoSubmitResponse.EResult
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgGCPlayerInfoSubmitResponse.EResult
    def __init__(
        self, result: CMsgGCPlayerInfoSubmitResponse.EResult | str | None = ...
    ) -> None: ...

class CMsgDOTAEmoticonAccessSDO(_message.Message):
    __slots__ = ("account_id", "unlocked_emoticons")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    UNLOCKED_EMOTICONS_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    unlocked_emoticons: bytes
    def __init__(
        self, account_id: int | None = ..., unlocked_emoticons: bytes | None = ...
    ) -> None: ...

class CMsgClientToGCEmoticonDataRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgGCToClientEmoticonData(_message.Message):
    __slots__ = ("emoticon_access",)
    EMOTICON_ACCESS_FIELD_NUMBER: _ClassVar[int]
    emoticon_access: CMsgDOTAEmoticonAccessSDO
    def __init__(
        self, emoticon_access: CMsgDOTAEmoticonAccessSDO | _Mapping | None = ...
    ) -> None: ...

class CMsgGCToClientTournamentItemDrop(_message.Message):
    __slots__ = ("item_def", "event_type")
    ITEM_DEF_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    item_def: int
    event_type: int
    def __init__(self, item_def: int | None = ..., event_type: int | None = ...) -> None: ...

class CMsgClientToGCGetAllHeroOrder(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCGetAllHeroOrderResponse(_message.Message):
    __slots__ = ("hero_ids",)
    HERO_IDS_FIELD_NUMBER: _ClassVar[int]
    hero_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, hero_ids: _Iterable[int] | None = ...) -> None: ...

class CMsgClientToGCGetAllHeroProgress(_message.Message):
    __slots__ = ("account_id",)
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    def __init__(self, account_id: int | None = ...) -> None: ...

class CMsgClientToGCGetAllHeroProgressResponse(_message.Message):
    __slots__ = (
        "account_id",
        "curr_hero_id",
        "laps_completed",
        "curr_hero_games",
        "curr_lap_time_started",
        "curr_lap_games",
        "best_lap_games",
        "best_lap_time",
        "lap_heroes_completed",
        "lap_heroes_remaining",
        "next_hero_id",
        "prev_hero_id",
        "prev_hero_games",
        "prev_avg_tries",
        "curr_avg_tries",
        "next_avg_tries",
        "full_lap_avg_tries",
        "curr_lap_avg_tries",
        "profile_name",
        "start_hero_id",
    )
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    CURR_HERO_ID_FIELD_NUMBER: _ClassVar[int]
    LAPS_COMPLETED_FIELD_NUMBER: _ClassVar[int]
    CURR_HERO_GAMES_FIELD_NUMBER: _ClassVar[int]
    CURR_LAP_TIME_STARTED_FIELD_NUMBER: _ClassVar[int]
    CURR_LAP_GAMES_FIELD_NUMBER: _ClassVar[int]
    BEST_LAP_GAMES_FIELD_NUMBER: _ClassVar[int]
    BEST_LAP_TIME_FIELD_NUMBER: _ClassVar[int]
    LAP_HEROES_COMPLETED_FIELD_NUMBER: _ClassVar[int]
    LAP_HEROES_REMAINING_FIELD_NUMBER: _ClassVar[int]
    NEXT_HERO_ID_FIELD_NUMBER: _ClassVar[int]
    PREV_HERO_ID_FIELD_NUMBER: _ClassVar[int]
    PREV_HERO_GAMES_FIELD_NUMBER: _ClassVar[int]
    PREV_AVG_TRIES_FIELD_NUMBER: _ClassVar[int]
    CURR_AVG_TRIES_FIELD_NUMBER: _ClassVar[int]
    NEXT_AVG_TRIES_FIELD_NUMBER: _ClassVar[int]
    FULL_LAP_AVG_TRIES_FIELD_NUMBER: _ClassVar[int]
    CURR_LAP_AVG_TRIES_FIELD_NUMBER: _ClassVar[int]
    PROFILE_NAME_FIELD_NUMBER: _ClassVar[int]
    START_HERO_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    curr_hero_id: int
    laps_completed: int
    curr_hero_games: int
    curr_lap_time_started: int
    curr_lap_games: int
    best_lap_games: int
    best_lap_time: int
    lap_heroes_completed: int
    lap_heroes_remaining: int
    next_hero_id: int
    prev_hero_id: int
    prev_hero_games: int
    prev_avg_tries: float
    curr_avg_tries: float
    next_avg_tries: float
    full_lap_avg_tries: float
    curr_lap_avg_tries: float
    profile_name: str
    start_hero_id: int
    def __init__(
        self,
        account_id: int | None = ...,
        curr_hero_id: int | None = ...,
        laps_completed: int | None = ...,
        curr_hero_games: int | None = ...,
        curr_lap_time_started: int | None = ...,
        curr_lap_games: int | None = ...,
        best_lap_games: int | None = ...,
        best_lap_time: int | None = ...,
        lap_heroes_completed: int | None = ...,
        lap_heroes_remaining: int | None = ...,
        next_hero_id: int | None = ...,
        prev_hero_id: int | None = ...,
        prev_hero_games: int | None = ...,
        prev_avg_tries: float | None = ...,
        curr_avg_tries: float | None = ...,
        next_avg_tries: float | None = ...,
        full_lap_avg_tries: float | None = ...,
        curr_lap_avg_tries: float | None = ...,
        profile_name: str | None = ...,
        start_hero_id: int | None = ...,
    ) -> None: ...

class CMsgClientToGCGetTrophyList(_message.Message):
    __slots__ = ("account_id",)
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    def __init__(self, account_id: int | None = ...) -> None: ...

class CMsgClientToGCGetTrophyListResponse(_message.Message):
    __slots__ = ("trophies",)
    class Trophy(_message.Message):
        __slots__ = ("trophy_id", "trophy_score", "last_updated")
        TROPHY_ID_FIELD_NUMBER: _ClassVar[int]
        TROPHY_SCORE_FIELD_NUMBER: _ClassVar[int]
        LAST_UPDATED_FIELD_NUMBER: _ClassVar[int]
        trophy_id: int
        trophy_score: int
        last_updated: int
        def __init__(
            self,
            trophy_id: int | None = ...,
            trophy_score: int | None = ...,
            last_updated: int | None = ...,
        ) -> None: ...

    TROPHIES_FIELD_NUMBER: _ClassVar[int]
    trophies: _containers.RepeatedCompositeFieldContainer[
        CMsgClientToGCGetTrophyListResponse.Trophy
    ]
    def __init__(
        self,
        trophies: _Iterable[CMsgClientToGCGetTrophyListResponse.Trophy | _Mapping] | None = ...,
    ) -> None: ...

class CMsgGCToClientTrophyAwarded(_message.Message):
    __slots__ = ("trophy_id", "trophy_score", "trophy_old_score", "last_updated")
    TROPHY_ID_FIELD_NUMBER: _ClassVar[int]
    TROPHY_SCORE_FIELD_NUMBER: _ClassVar[int]
    TROPHY_OLD_SCORE_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_FIELD_NUMBER: _ClassVar[int]
    trophy_id: int
    trophy_score: int
    trophy_old_score: int
    last_updated: int
    def __init__(
        self,
        trophy_id: int | None = ...,
        trophy_score: int | None = ...,
        trophy_old_score: int | None = ...,
        last_updated: int | None = ...,
    ) -> None: ...

class CMsgClientToGCRankRequest(_message.Message):
    __slots__ = ("rank_type",)
    RANK_TYPE_FIELD_NUMBER: _ClassVar[int]
    rank_type: _dota_shared_enums_pb2.ERankType
    def __init__(self, rank_type: _dota_shared_enums_pb2.ERankType | str | None = ...) -> None: ...

class CMsgGCToClientRankResponse(_message.Message):
    __slots__ = ("result", "rank_value", "rank_data1", "rank_data2", "rank_data3")
    class EResultCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_Succeeded: _ClassVar[CMsgGCToClientRankResponse.EResultCode]
        k_Failed: _ClassVar[CMsgGCToClientRankResponse.EResultCode]
        k_InvalidRankType: _ClassVar[CMsgGCToClientRankResponse.EResultCode]

    k_Succeeded: CMsgGCToClientRankResponse.EResultCode
    k_Failed: CMsgGCToClientRankResponse.EResultCode
    k_InvalidRankType: CMsgGCToClientRankResponse.EResultCode
    RESULT_FIELD_NUMBER: _ClassVar[int]
    RANK_VALUE_FIELD_NUMBER: _ClassVar[int]
    RANK_DATA1_FIELD_NUMBER: _ClassVar[int]
    RANK_DATA2_FIELD_NUMBER: _ClassVar[int]
    RANK_DATA3_FIELD_NUMBER: _ClassVar[int]
    result: CMsgGCToClientRankResponse.EResultCode
    rank_value: int
    rank_data1: int
    rank_data2: int
    rank_data3: int
    def __init__(
        self,
        result: CMsgGCToClientRankResponse.EResultCode | str | None = ...,
        rank_value: int | None = ...,
        rank_data1: int | None = ...,
        rank_data2: int | None = ...,
        rank_data3: int | None = ...,
    ) -> None: ...

class CMsgGCToClientRankUpdate(_message.Message):
    __slots__ = ("rank_type", "rank_info")
    RANK_TYPE_FIELD_NUMBER: _ClassVar[int]
    RANK_INFO_FIELD_NUMBER: _ClassVar[int]
    rank_type: _dota_shared_enums_pb2.ERankType
    rank_info: CMsgGCToClientRankResponse
    def __init__(
        self,
        rank_type: _dota_shared_enums_pb2.ERankType | str | None = ...,
        rank_info: CMsgGCToClientRankResponse | _Mapping | None = ...,
    ) -> None: ...

class CMsgClientToGCGetProfileCard(_message.Message):
    __slots__ = ("account_id",)
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    def __init__(self, account_id: int | None = ...) -> None: ...

class CMsgClientToGCSetProfileCardSlots(_message.Message):
    __slots__ = ("slots",)
    class CardSlot(_message.Message):
        __slots__ = ("slot_id", "slot_type", "slot_value")
        SLOT_ID_FIELD_NUMBER: _ClassVar[int]
        SLOT_TYPE_FIELD_NUMBER: _ClassVar[int]
        SLOT_VALUE_FIELD_NUMBER: _ClassVar[int]
        slot_id: int
        slot_type: _dota_shared_enums_pb2.EProfileCardSlotType
        slot_value: int
        def __init__(
            self,
            slot_id: int | None = ...,
            slot_type: _dota_shared_enums_pb2.EProfileCardSlotType | str | None = ...,
            slot_value: int | None = ...,
        ) -> None: ...

    SLOTS_FIELD_NUMBER: _ClassVar[int]
    slots: _containers.RepeatedCompositeFieldContainer[CMsgClientToGCSetProfileCardSlots.CardSlot]
    def __init__(
        self, slots: _Iterable[CMsgClientToGCSetProfileCardSlots.CardSlot | _Mapping] | None = ...
    ) -> None: ...

class CMsgClientToGCGetProfileCardStats(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCCreateHeroStatue(_message.Message):
    __slots__ = (
        "source_item_id",
        "hero_id",
        "sequence_name",
        "cycle",
        "wearables",
        "inscription",
        "styles",
        "reforger_item_id",
        "tournament_drop",
    )
    SOURCE_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_NAME_FIELD_NUMBER: _ClassVar[int]
    CYCLE_FIELD_NUMBER: _ClassVar[int]
    WEARABLES_FIELD_NUMBER: _ClassVar[int]
    INSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STYLES_FIELD_NUMBER: _ClassVar[int]
    REFORGER_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    TOURNAMENT_DROP_FIELD_NUMBER: _ClassVar[int]
    source_item_id: int
    hero_id: int
    sequence_name: str
    cycle: float
    wearables: _containers.RepeatedScalarFieldContainer[int]
    inscription: str
    styles: _containers.RepeatedScalarFieldContainer[int]
    reforger_item_id: int
    tournament_drop: bool
    def __init__(
        self,
        source_item_id: int | None = ...,
        hero_id: int | None = ...,
        sequence_name: str | None = ...,
        cycle: float | None = ...,
        wearables: _Iterable[int] | None = ...,
        inscription: str | None = ...,
        styles: _Iterable[int] | None = ...,
        reforger_item_id: int | None = ...,
        tournament_drop: bool = ...,
    ) -> None: ...

class CMsgGCToClientHeroStatueCreateResult(_message.Message):
    __slots__ = ("resulting_item_id",)
    RESULTING_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    resulting_item_id: int
    def __init__(self, resulting_item_id: int | None = ...) -> None: ...

class CMsgClientToGCPlayerStatsRequest(_message.Message):
    __slots__ = ("account_id",)
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    def __init__(self, account_id: int | None = ...) -> None: ...

class CMsgGCToClientPlayerStatsResponse(_message.Message):
    __slots__ = (
        "account_id",
        "player_stats",
        "match_count",
        "mean_gpm",
        "mean_xppm",
        "mean_lasthits",
        "rampages",
        "triple_kills",
        "first_blood_claimed",
        "first_blood_given",
        "couriers_killed",
        "aegises_snatched",
        "cheeses_eaten",
        "creeps_stacked",
        "fight_score",
        "farm_score",
        "support_score",
        "push_score",
        "versatility_score",
        "mean_networth",
        "mean_damage",
        "mean_heals",
        "rapiers_purchased",
    )
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    PLAYER_STATS_FIELD_NUMBER: _ClassVar[int]
    MATCH_COUNT_FIELD_NUMBER: _ClassVar[int]
    MEAN_GPM_FIELD_NUMBER: _ClassVar[int]
    MEAN_XPPM_FIELD_NUMBER: _ClassVar[int]
    MEAN_LASTHITS_FIELD_NUMBER: _ClassVar[int]
    RAMPAGES_FIELD_NUMBER: _ClassVar[int]
    TRIPLE_KILLS_FIELD_NUMBER: _ClassVar[int]
    FIRST_BLOOD_CLAIMED_FIELD_NUMBER: _ClassVar[int]
    FIRST_BLOOD_GIVEN_FIELD_NUMBER: _ClassVar[int]
    COURIERS_KILLED_FIELD_NUMBER: _ClassVar[int]
    AEGISES_SNATCHED_FIELD_NUMBER: _ClassVar[int]
    CHEESES_EATEN_FIELD_NUMBER: _ClassVar[int]
    CREEPS_STACKED_FIELD_NUMBER: _ClassVar[int]
    FIGHT_SCORE_FIELD_NUMBER: _ClassVar[int]
    FARM_SCORE_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_SCORE_FIELD_NUMBER: _ClassVar[int]
    PUSH_SCORE_FIELD_NUMBER: _ClassVar[int]
    VERSATILITY_SCORE_FIELD_NUMBER: _ClassVar[int]
    MEAN_NETWORTH_FIELD_NUMBER: _ClassVar[int]
    MEAN_DAMAGE_FIELD_NUMBER: _ClassVar[int]
    MEAN_HEALS_FIELD_NUMBER: _ClassVar[int]
    RAPIERS_PURCHASED_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    player_stats: _containers.RepeatedScalarFieldContainer[float]
    match_count: int
    mean_gpm: float
    mean_xppm: float
    mean_lasthits: float
    rampages: int
    triple_kills: int
    first_blood_claimed: int
    first_blood_given: int
    couriers_killed: int
    aegises_snatched: int
    cheeses_eaten: int
    creeps_stacked: int
    fight_score: float
    farm_score: float
    support_score: float
    push_score: float
    versatility_score: float
    mean_networth: float
    mean_damage: float
    mean_heals: float
    rapiers_purchased: int
    def __init__(
        self,
        account_id: int | None = ...,
        player_stats: _Iterable[float] | None = ...,
        match_count: int | None = ...,
        mean_gpm: float | None = ...,
        mean_xppm: float | None = ...,
        mean_lasthits: float | None = ...,
        rampages: int | None = ...,
        triple_kills: int | None = ...,
        first_blood_claimed: int | None = ...,
        first_blood_given: int | None = ...,
        couriers_killed: int | None = ...,
        aegises_snatched: int | None = ...,
        cheeses_eaten: int | None = ...,
        creeps_stacked: int | None = ...,
        fight_score: float | None = ...,
        farm_score: float | None = ...,
        support_score: float | None = ...,
        push_score: float | None = ...,
        versatility_score: float | None = ...,
        mean_networth: float | None = ...,
        mean_damage: float | None = ...,
        mean_heals: float | None = ...,
        rapiers_purchased: int | None = ...,
    ) -> None: ...

class CMsgClientToGCCustomGamesFriendsPlayedRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgGCToClientCustomGamesFriendsPlayedResponse(_message.Message):
    __slots__ = ("account_id", "games")
    class CustomGame(_message.Message):
        __slots__ = ("custom_game_id", "account_ids")
        CUSTOM_GAME_ID_FIELD_NUMBER: _ClassVar[int]
        ACCOUNT_IDS_FIELD_NUMBER: _ClassVar[int]
        custom_game_id: int
        account_ids: _containers.RepeatedScalarFieldContainer[int]
        def __init__(
            self, custom_game_id: int | None = ..., account_ids: _Iterable[int] | None = ...
        ) -> None: ...

    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    GAMES_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    games: _containers.RepeatedCompositeFieldContainer[
        CMsgGCToClientCustomGamesFriendsPlayedResponse.CustomGame
    ]
    def __init__(
        self,
        account_id: int | None = ...,
        games: _Iterable[CMsgGCToClientCustomGamesFriendsPlayedResponse.CustomGame | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgClientToGCSocialFeedPostCommentRequest(_message.Message):
    __slots__ = ("event_id", "comment")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    comment: str
    def __init__(self, event_id: int | None = ..., comment: str | None = ...) -> None: ...

class CMsgGCToClientSocialFeedPostCommentResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class CMsgClientToGCSocialFeedPostMessageRequest(_message.Message):
    __slots__ = ("message", "match_id", "match_timestamp")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    MATCH_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    message: str
    match_id: int
    match_timestamp: int
    def __init__(
        self,
        message: str | None = ...,
        match_id: int | None = ...,
        match_timestamp: int | None = ...,
    ) -> None: ...

class CMsgGCToClientSocialFeedPostMessageResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class CMsgClientToGCFriendsPlayedCustomGameRequest(_message.Message):
    __slots__ = ("custom_game_id",)
    CUSTOM_GAME_ID_FIELD_NUMBER: _ClassVar[int]
    custom_game_id: int
    def __init__(self, custom_game_id: int | None = ...) -> None: ...

class CMsgGCToClientFriendsPlayedCustomGameResponse(_message.Message):
    __slots__ = ("custom_game_id", "account_ids")
    CUSTOM_GAME_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_IDS_FIELD_NUMBER: _ClassVar[int]
    custom_game_id: int
    account_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self, custom_game_id: int | None = ..., account_ids: _Iterable[int] | None = ...
    ) -> None: ...

class CMsgDOTAPartyRichPresence(_message.Message):
    __slots__ = (
        "party_id",
        "party_state",
        "open",
        "low_priority",
        "team_id",
        "team_name",
        "ugc_team_ui_logo",
        "members",
        "weekend_tourney",
    )
    class Member(_message.Message):
        __slots__ = ("steam_id", "coach")
        STEAM_ID_FIELD_NUMBER: _ClassVar[int]
        COACH_FIELD_NUMBER: _ClassVar[int]
        steam_id: int
        coach: bool
        def __init__(self, steam_id: int | None = ..., coach: bool = ...) -> None: ...

    class WeekendTourney(_message.Message):
        __slots__ = (
            "division",
            "skill_level",
            "round",
            "tournament_id",
            "state_seq_num",
            "event",
            "event_round",
        )
        DIVISION_FIELD_NUMBER: _ClassVar[int]
        SKILL_LEVEL_FIELD_NUMBER: _ClassVar[int]
        ROUND_FIELD_NUMBER: _ClassVar[int]
        TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
        STATE_SEQ_NUM_FIELD_NUMBER: _ClassVar[int]
        EVENT_FIELD_NUMBER: _ClassVar[int]
        EVENT_ROUND_FIELD_NUMBER: _ClassVar[int]
        division: int
        skill_level: int
        round: int
        tournament_id: int
        state_seq_num: int
        event: EWeekendTourneyRichPresenceEvent
        event_round: int
        def __init__(
            self,
            division: int | None = ...,
            skill_level: int | None = ...,
            round: int | None = ...,
            tournament_id: int | None = ...,
            state_seq_num: int | None = ...,
            event: EWeekendTourneyRichPresenceEvent | str | None = ...,
            event_round: int | None = ...,
        ) -> None: ...

    PARTY_ID_FIELD_NUMBER: _ClassVar[int]
    PARTY_STATE_FIELD_NUMBER: _ClassVar[int]
    OPEN_FIELD_NUMBER: _ClassVar[int]
    LOW_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
    UGC_TEAM_UI_LOGO_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    WEEKEND_TOURNEY_FIELD_NUMBER: _ClassVar[int]
    party_id: int
    party_state: _dota_gcmessages_common_match_management_pb2.CSODOTAParty.State
    open: bool
    low_priority: bool
    team_id: int
    team_name: str
    ugc_team_ui_logo: int
    members: _containers.RepeatedCompositeFieldContainer[CMsgDOTAPartyRichPresence.Member]
    weekend_tourney: CMsgDOTAPartyRichPresence.WeekendTourney
    def __init__(
        self,
        party_id: int | None = ...,
        party_state: _dota_gcmessages_common_match_management_pb2.CSODOTAParty.State
        | str
        | None = ...,
        open: bool = ...,
        low_priority: bool = ...,
        team_id: int | None = ...,
        team_name: str | None = ...,
        ugc_team_ui_logo: int | None = ...,
        members: _Iterable[CMsgDOTAPartyRichPresence.Member | _Mapping] | None = ...,
        weekend_tourney: CMsgDOTAPartyRichPresence.WeekendTourney | _Mapping | None = ...,
    ) -> None: ...

class CMsgDOTALobbyRichPresence(_message.Message):
    __slots__ = (
        "lobby_id",
        "lobby_state",
        "password",
        "game_mode",
        "member_count",
        "max_member_count",
        "custom_game_id",
        "name",
        "lobby_type",
    )
    LOBBY_ID_FIELD_NUMBER: _ClassVar[int]
    LOBBY_STATE_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    GAME_MODE_FIELD_NUMBER: _ClassVar[int]
    MEMBER_COUNT_FIELD_NUMBER: _ClassVar[int]
    MAX_MEMBER_COUNT_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    LOBBY_TYPE_FIELD_NUMBER: _ClassVar[int]
    lobby_id: int
    lobby_state: _dota_gcmessages_common_lobby_pb2.CSODOTALobby.State
    password: bool
    game_mode: _dota_shared_enums_pb2.DOTA_GameMode
    member_count: int
    max_member_count: int
    custom_game_id: int
    name: str
    lobby_type: int
    def __init__(
        self,
        lobby_id: int | None = ...,
        lobby_state: _dota_gcmessages_common_lobby_pb2.CSODOTALobby.State | str | None = ...,
        password: bool = ...,
        game_mode: _dota_shared_enums_pb2.DOTA_GameMode | str | None = ...,
        member_count: int | None = ...,
        max_member_count: int | None = ...,
        custom_game_id: int | None = ...,
        name: str | None = ...,
        lobby_type: int | None = ...,
    ) -> None: ...

class CMsgDOTACustomGameListenServerStartedLoading(_message.Message):
    __slots__ = ("lobby_id", "custom_game_id", "lobby_members", "start_time")
    LOBBY_ID_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_ID_FIELD_NUMBER: _ClassVar[int]
    LOBBY_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    lobby_id: int
    custom_game_id: int
    lobby_members: _containers.RepeatedScalarFieldContainer[int]
    start_time: int
    def __init__(
        self,
        lobby_id: int | None = ...,
        custom_game_id: int | None = ...,
        lobby_members: _Iterable[int] | None = ...,
        start_time: int | None = ...,
    ) -> None: ...

class CMsgDOTACustomGameClientFinishedLoading(_message.Message):
    __slots__ = (
        "lobby_id",
        "loading_duration",
        "result_code",
        "result_string",
        "signon_states",
        "comment",
    )
    LOBBY_ID_FIELD_NUMBER: _ClassVar[int]
    LOADING_DURATION_FIELD_NUMBER: _ClassVar[int]
    RESULT_CODE_FIELD_NUMBER: _ClassVar[int]
    RESULT_STRING_FIELD_NUMBER: _ClassVar[int]
    SIGNON_STATES_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    lobby_id: int
    loading_duration: int
    result_code: int
    result_string: str
    signon_states: int
    comment: str
    def __init__(
        self,
        lobby_id: int | None = ...,
        loading_duration: int | None = ...,
        result_code: int | None = ...,
        result_string: str | None = ...,
        signon_states: int | None = ...,
        comment: str | None = ...,
    ) -> None: ...

class CMsgClientToGCApplyGemCombiner(_message.Message):
    __slots__ = ("item_id_1", "item_id_2")
    ITEM_ID_1_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_2_FIELD_NUMBER: _ClassVar[int]
    item_id_1: int
    item_id_2: int
    def __init__(self, item_id_1: int | None = ..., item_id_2: int | None = ...) -> None: ...

class CMsgClientToGCH264Unsupported(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCGetQuestProgress(_message.Message):
    __slots__ = ("quest_ids",)
    QUEST_IDS_FIELD_NUMBER: _ClassVar[int]
    quest_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, quest_ids: _Iterable[int] | None = ...) -> None: ...

class CMsgClientToGCGetQuestProgressResponse(_message.Message):
    __slots__ = ("success", "quests")
    class Challenge(_message.Message):
        __slots__ = (
            "challenge_id",
            "time_completed",
            "attempts",
            "hero_id",
            "template_id",
            "quest_rank",
        )
        CHALLENGE_ID_FIELD_NUMBER: _ClassVar[int]
        TIME_COMPLETED_FIELD_NUMBER: _ClassVar[int]
        ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
        QUEST_RANK_FIELD_NUMBER: _ClassVar[int]
        challenge_id: int
        time_completed: int
        attempts: int
        hero_id: int
        template_id: int
        quest_rank: int
        def __init__(
            self,
            challenge_id: int | None = ...,
            time_completed: int | None = ...,
            attempts: int | None = ...,
            hero_id: int | None = ...,
            template_id: int | None = ...,
            quest_rank: int | None = ...,
        ) -> None: ...

    class Quest(_message.Message):
        __slots__ = ("quest_id", "completed_challenges")
        QUEST_ID_FIELD_NUMBER: _ClassVar[int]
        COMPLETED_CHALLENGES_FIELD_NUMBER: _ClassVar[int]
        quest_id: int
        completed_challenges: _containers.RepeatedCompositeFieldContainer[
            CMsgClientToGCGetQuestProgressResponse.Challenge
        ]
        def __init__(
            self,
            quest_id: int | None = ...,
            completed_challenges: _Iterable[
                CMsgClientToGCGetQuestProgressResponse.Challenge | _Mapping
            ]
            | None = ...,
        ) -> None: ...

    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    QUESTS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    quests: _containers.RepeatedCompositeFieldContainer[
        CMsgClientToGCGetQuestProgressResponse.Quest
    ]
    def __init__(
        self,
        success: bool = ...,
        quests: _Iterable[CMsgClientToGCGetQuestProgressResponse.Quest | _Mapping] | None = ...,
    ) -> None: ...

class CMsgGCToClientMatchSignedOut(_message.Message):
    __slots__ = ("match_id",)
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    def __init__(self, match_id: int | None = ...) -> None: ...

class CMsgGCGetHeroStatsHistory(_message.Message):
    __slots__ = ("hero_id",)
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    hero_id: int
    def __init__(self, hero_id: int | None = ...) -> None: ...

class CMsgGCGetHeroStatsHistoryResponse(_message.Message):
    __slots__ = ("hero_id", "records", "result")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgGCGetHeroStatsHistoryResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgGCGetHeroStatsHistoryResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgGCGetHeroStatsHistoryResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgGCGetHeroStatsHistoryResponse.EResponse]

    k_eInternalError: CMsgGCGetHeroStatsHistoryResponse.EResponse
    k_eSuccess: CMsgGCGetHeroStatsHistoryResponse.EResponse
    k_eTooBusy: CMsgGCGetHeroStatsHistoryResponse.EResponse
    k_eDisabled: CMsgGCGetHeroStatsHistoryResponse.EResponse
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    hero_id: int
    records: _containers.RepeatedCompositeFieldContainer[
        _dota_gcmessages_common_pb2.CMsgDOTASDOHeroStatsHistory
    ]
    result: CMsgGCGetHeroStatsHistoryResponse.EResponse
    def __init__(
        self,
        hero_id: int | None = ...,
        records: _Iterable[_dota_gcmessages_common_pb2.CMsgDOTASDOHeroStatsHistory | _Mapping]
        | None = ...,
        result: CMsgGCGetHeroStatsHistoryResponse.EResponse | str | None = ...,
    ) -> None: ...

class CMsgPlayerConductScorecardRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgPlayerConductScorecard(_message.Message):
    __slots__ = (
        "account_id",
        "match_id",
        "seq_num",
        "reasons",
        "matches_in_report",
        "matches_clean",
        "matches_reported",
        "matches_abandoned",
        "reports_count",
        "reports_parties",
        "commend_count",
        "date",
        "raw_behavior_score",
        "old_raw_behavior_score",
        "comms_reports",
        "comms_parties",
        "behavior_rating",
    )
    class EBehaviorRating(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eBehaviorGood: _ClassVar[CMsgPlayerConductScorecard.EBehaviorRating]
        k_eBehaviorWarning: _ClassVar[CMsgPlayerConductScorecard.EBehaviorRating]
        k_eBehaviorBad: _ClassVar[CMsgPlayerConductScorecard.EBehaviorRating]

    k_eBehaviorGood: CMsgPlayerConductScorecard.EBehaviorRating
    k_eBehaviorWarning: CMsgPlayerConductScorecard.EBehaviorRating
    k_eBehaviorBad: CMsgPlayerConductScorecard.EBehaviorRating
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    SEQ_NUM_FIELD_NUMBER: _ClassVar[int]
    REASONS_FIELD_NUMBER: _ClassVar[int]
    MATCHES_IN_REPORT_FIELD_NUMBER: _ClassVar[int]
    MATCHES_CLEAN_FIELD_NUMBER: _ClassVar[int]
    MATCHES_REPORTED_FIELD_NUMBER: _ClassVar[int]
    MATCHES_ABANDONED_FIELD_NUMBER: _ClassVar[int]
    REPORTS_COUNT_FIELD_NUMBER: _ClassVar[int]
    REPORTS_PARTIES_FIELD_NUMBER: _ClassVar[int]
    COMMEND_COUNT_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    RAW_BEHAVIOR_SCORE_FIELD_NUMBER: _ClassVar[int]
    OLD_RAW_BEHAVIOR_SCORE_FIELD_NUMBER: _ClassVar[int]
    COMMS_REPORTS_FIELD_NUMBER: _ClassVar[int]
    COMMS_PARTIES_FIELD_NUMBER: _ClassVar[int]
    BEHAVIOR_RATING_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    match_id: int
    seq_num: int
    reasons: int
    matches_in_report: int
    matches_clean: int
    matches_reported: int
    matches_abandoned: int
    reports_count: int
    reports_parties: int
    commend_count: int
    date: int
    raw_behavior_score: int
    old_raw_behavior_score: int
    comms_reports: int
    comms_parties: int
    behavior_rating: CMsgPlayerConductScorecard.EBehaviorRating
    def __init__(
        self,
        account_id: int | None = ...,
        match_id: int | None = ...,
        seq_num: int | None = ...,
        reasons: int | None = ...,
        matches_in_report: int | None = ...,
        matches_clean: int | None = ...,
        matches_reported: int | None = ...,
        matches_abandoned: int | None = ...,
        reports_count: int | None = ...,
        reports_parties: int | None = ...,
        commend_count: int | None = ...,
        date: int | None = ...,
        raw_behavior_score: int | None = ...,
        old_raw_behavior_score: int | None = ...,
        comms_reports: int | None = ...,
        comms_parties: int | None = ...,
        behavior_rating: CMsgPlayerConductScorecard.EBehaviorRating | str | None = ...,
    ) -> None: ...

class CMsgClientToGCWageringRequest(_message.Message):
    __slots__ = ("event_id",)
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    def __init__(self, event_id: int | None = ...) -> None: ...

class CMsgGCToClientWageringResponse(_message.Message):
    __slots__ = (
        "coins_remaining",
        "total_points_won",
        "total_points_wagered",
        "total_points_tipped",
        "success_rate",
        "total_games_wagered",
        "coins_max",
        "rank_wagers_remaining",
        "rank_wagers_max",
        "prediction_tokens_remaining",
        "prediction_tokens_max",
        "bounties_remaining",
        "bounties_max",
    )
    COINS_REMAINING_FIELD_NUMBER: _ClassVar[int]
    TOTAL_POINTS_WON_FIELD_NUMBER: _ClassVar[int]
    TOTAL_POINTS_WAGERED_FIELD_NUMBER: _ClassVar[int]
    TOTAL_POINTS_TIPPED_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_RATE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_GAMES_WAGERED_FIELD_NUMBER: _ClassVar[int]
    COINS_MAX_FIELD_NUMBER: _ClassVar[int]
    RANK_WAGERS_REMAINING_FIELD_NUMBER: _ClassVar[int]
    RANK_WAGERS_MAX_FIELD_NUMBER: _ClassVar[int]
    PREDICTION_TOKENS_REMAINING_FIELD_NUMBER: _ClassVar[int]
    PREDICTION_TOKENS_MAX_FIELD_NUMBER: _ClassVar[int]
    BOUNTIES_REMAINING_FIELD_NUMBER: _ClassVar[int]
    BOUNTIES_MAX_FIELD_NUMBER: _ClassVar[int]
    coins_remaining: int
    total_points_won: int
    total_points_wagered: int
    total_points_tipped: int
    success_rate: int
    total_games_wagered: int
    coins_max: int
    rank_wagers_remaining: int
    rank_wagers_max: int
    prediction_tokens_remaining: int
    prediction_tokens_max: int
    bounties_remaining: int
    bounties_max: int
    def __init__(
        self,
        coins_remaining: int | None = ...,
        total_points_won: int | None = ...,
        total_points_wagered: int | None = ...,
        total_points_tipped: int | None = ...,
        success_rate: int | None = ...,
        total_games_wagered: int | None = ...,
        coins_max: int | None = ...,
        rank_wagers_remaining: int | None = ...,
        rank_wagers_max: int | None = ...,
        prediction_tokens_remaining: int | None = ...,
        prediction_tokens_max: int | None = ...,
        bounties_remaining: int | None = ...,
        bounties_max: int | None = ...,
    ) -> None: ...

class CMsgGCToClientWageringUpdate(_message.Message):
    __slots__ = ("event_id", "wagering_info")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    WAGERING_INFO_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    wagering_info: CMsgGCToClientWageringResponse
    def __init__(
        self,
        event_id: int | None = ...,
        wagering_info: CMsgGCToClientWageringResponse | _Mapping | None = ...,
    ) -> None: ...

class CMsgGCToClientArcanaVotesUpdate(_message.Message):
    __slots__ = ("event_id", "arcana_votes")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ARCANA_VOTES_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    arcana_votes: CMsgClientToGCRequestArcanaVotesRemainingResponse
    def __init__(
        self,
        event_id: int | None = ...,
        arcana_votes: CMsgClientToGCRequestArcanaVotesRemainingResponse | _Mapping | None = ...,
    ) -> None: ...

class CMsgClientToGCGetEventGoals(_message.Message):
    __slots__ = ("event_ids",)
    EVENT_IDS_FIELD_NUMBER: _ClassVar[int]
    event_ids: _containers.RepeatedScalarFieldContainer[_dota_shared_enums_pb2.EEvent]
    def __init__(
        self, event_ids: _Iterable[_dota_shared_enums_pb2.EEvent | str] | None = ...
    ) -> None: ...

class CMsgEventGoals(_message.Message):
    __slots__ = ("event_goals",)
    class EventGoal(_message.Message):
        __slots__ = ("event_id", "goal_id", "value")
        EVENT_ID_FIELD_NUMBER: _ClassVar[int]
        GOAL_ID_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        event_id: _dota_shared_enums_pb2.EEvent
        goal_id: int
        value: int
        def __init__(
            self,
            event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
            goal_id: int | None = ...,
            value: int | None = ...,
        ) -> None: ...

    EVENT_GOALS_FIELD_NUMBER: _ClassVar[int]
    event_goals: _containers.RepeatedCompositeFieldContainer[CMsgEventGoals.EventGoal]
    def __init__(
        self, event_goals: _Iterable[CMsgEventGoals.EventGoal | _Mapping] | None = ...
    ) -> None: ...

class CMsgGCToGCLeaguePredictions(_message.Message):
    __slots__ = ("league_id",)
    LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    league_id: int
    def __init__(self, league_id: int | None = ...) -> None: ...

class CMsgPredictionRankings(_message.Message):
    __slots__ = ("predictions",)
    class PredictionLine(_message.Message):
        __slots__ = ("answer_id", "answer_name", "answer_logo", "answer_value")
        ANSWER_ID_FIELD_NUMBER: _ClassVar[int]
        ANSWER_NAME_FIELD_NUMBER: _ClassVar[int]
        ANSWER_LOGO_FIELD_NUMBER: _ClassVar[int]
        ANSWER_VALUE_FIELD_NUMBER: _ClassVar[int]
        answer_id: int
        answer_name: str
        answer_logo: int
        answer_value: float
        def __init__(
            self,
            answer_id: int | None = ...,
            answer_name: str | None = ...,
            answer_logo: int | None = ...,
            answer_value: float | None = ...,
        ) -> None: ...

    class Prediction(_message.Message):
        __slots__ = ("selection_id", "prediction_lines")
        SELECTION_ID_FIELD_NUMBER: _ClassVar[int]
        PREDICTION_LINES_FIELD_NUMBER: _ClassVar[int]
        selection_id: int
        prediction_lines: _containers.RepeatedCompositeFieldContainer[
            CMsgPredictionRankings.PredictionLine
        ]
        def __init__(
            self,
            selection_id: int | None = ...,
            prediction_lines: _Iterable[CMsgPredictionRankings.PredictionLine | _Mapping]
            | None = ...,
        ) -> None: ...

    PREDICTIONS_FIELD_NUMBER: _ClassVar[int]
    predictions: _containers.RepeatedCompositeFieldContainer[CMsgPredictionRankings.Prediction]
    def __init__(
        self, predictions: _Iterable[CMsgPredictionRankings.Prediction | _Mapping] | None = ...
    ) -> None: ...

class CMsgPredictionResults(_message.Message):
    __slots__ = ("results",)
    class ResultBreakdown(_message.Message):
        __slots__ = ("answer_selection", "answer_value")
        ANSWER_SELECTION_FIELD_NUMBER: _ClassVar[int]
        ANSWER_VALUE_FIELD_NUMBER: _ClassVar[int]
        answer_selection: int
        answer_value: float
        def __init__(
            self, answer_selection: int | None = ..., answer_value: float | None = ...
        ) -> None: ...

    class Result(_message.Message):
        __slots__ = ("selection_id", "result_breakdown")
        SELECTION_ID_FIELD_NUMBER: _ClassVar[int]
        RESULT_BREAKDOWN_FIELD_NUMBER: _ClassVar[int]
        selection_id: int
        result_breakdown: _containers.RepeatedCompositeFieldContainer[
            CMsgPredictionResults.ResultBreakdown
        ]
        def __init__(
            self,
            selection_id: int | None = ...,
            result_breakdown: _Iterable[CMsgPredictionResults.ResultBreakdown | _Mapping]
            | None = ...,
        ) -> None: ...

    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[CMsgPredictionResults.Result]
    def __init__(
        self, results: _Iterable[CMsgPredictionResults.Result | _Mapping] | None = ...
    ) -> None: ...

class CMsgClientToGCHasPlayerVotedForMVP(_message.Message):
    __slots__ = ("match_id",)
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    def __init__(self, match_id: int | None = ...) -> None: ...

class CMsgClientToGCHasPlayerVotedForMVPResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: bool
    def __init__(self, result: bool = ...) -> None: ...

class CMsgClientToGCVoteForMVP(_message.Message):
    __slots__ = ("match_id", "account_id")
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    account_id: int
    def __init__(self, match_id: int | None = ..., account_id: int | None = ...) -> None: ...

class CMsgClientToGCVoteForMVPResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: bool
    def __init__(self, result: bool = ...) -> None: ...

class CMsgClientToGCMVPVoteTimeout(_message.Message):
    __slots__ = ("match_id",)
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    def __init__(self, match_id: int | None = ...) -> None: ...

class CMsgClientToGCMVPVoteTimeoutResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: bool
    def __init__(self, result: bool = ...) -> None: ...

class CMsgClientToGCTeammateStatsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCTeammateStatsResponse(_message.Message):
    __slots__ = ("success", "teammate_stats")
    class TeammateStat(_message.Message):
        __slots__ = (
            "account_id",
            "games",
            "wins",
            "most_recent_game_timestamp",
            "most_recent_game_match_id",
            "performance",
        )
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        GAMES_FIELD_NUMBER: _ClassVar[int]
        WINS_FIELD_NUMBER: _ClassVar[int]
        MOST_RECENT_GAME_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        MOST_RECENT_GAME_MATCH_ID_FIELD_NUMBER: _ClassVar[int]
        PERFORMANCE_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        games: int
        wins: int
        most_recent_game_timestamp: int
        most_recent_game_match_id: int
        performance: float
        def __init__(
            self,
            account_id: int | None = ...,
            games: int | None = ...,
            wins: int | None = ...,
            most_recent_game_timestamp: int | None = ...,
            most_recent_game_match_id: int | None = ...,
            performance: float | None = ...,
        ) -> None: ...

    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    TEAMMATE_STATS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    teammate_stats: _containers.RepeatedCompositeFieldContainer[
        CMsgClientToGCTeammateStatsResponse.TeammateStat
    ]
    def __init__(
        self,
        success: bool = ...,
        teammate_stats: _Iterable[CMsgClientToGCTeammateStatsResponse.TeammateStat | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgClientToGCVoteForArcana(_message.Message):
    __slots__ = ("matches",)
    MATCHES_FIELD_NUMBER: _ClassVar[int]
    matches: _containers.RepeatedCompositeFieldContainer[
        _dota_gcmessages_common_pb2.CMsgArcanaVoteMatchVotes
    ]
    def __init__(
        self,
        matches: _Iterable[_dota_gcmessages_common_pb2.CMsgArcanaVoteMatchVotes | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgClientToGCVoteForArcanaResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCEEDED: _ClassVar[CMsgClientToGCVoteForArcanaResponse.Result]
        VOTING_NOT_ENABLED_FOR_ROUND: _ClassVar[CMsgClientToGCVoteForArcanaResponse.Result]
        UNKNOWN_FAILURE: _ClassVar[CMsgClientToGCVoteForArcanaResponse.Result]

    SUCCEEDED: CMsgClientToGCVoteForArcanaResponse.Result
    VOTING_NOT_ENABLED_FOR_ROUND: CMsgClientToGCVoteForArcanaResponse.Result
    UNKNOWN_FAILURE: CMsgClientToGCVoteForArcanaResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCVoteForArcanaResponse.Result
    def __init__(
        self, result: CMsgClientToGCVoteForArcanaResponse.Result | str | None = ...
    ) -> None: ...

class CMsgClientToGCRequestArcanaVotesRemaining(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCRequestArcanaVotesRemainingResponse(_message.Message):
    __slots__ = ("result", "votes_remaining", "votes_total", "matches_previously_voted_for")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    VOTES_REMAINING_FIELD_NUMBER: _ClassVar[int]
    VOTES_TOTAL_FIELD_NUMBER: _ClassVar[int]
    MATCHES_PREVIOUSLY_VOTED_FOR_FIELD_NUMBER: _ClassVar[int]
    result: bool
    votes_remaining: int
    votes_total: int
    matches_previously_voted_for: _containers.RepeatedCompositeFieldContainer[
        _dota_gcmessages_common_pb2.CMsgArcanaVoteMatchVotes
    ]
    def __init__(
        self,
        result: bool = ...,
        votes_remaining: int | None = ...,
        votes_total: int | None = ...,
        matches_previously_voted_for: _Iterable[
            _dota_gcmessages_common_pb2.CMsgArcanaVoteMatchVotes | _Mapping
        ]
        | None = ...,
    ) -> None: ...

class CMsgClientToGCRequestEventPointLogV2(_message.Message):
    __slots__ = ("event_id",)
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    def __init__(self, event_id: int | None = ...) -> None: ...

class CMsgClientToGCRequestEventPointLogResponseV2(_message.Message):
    __slots__ = ("result", "event_id", "log_entries")
    class LogEntry(_message.Message):
        __slots__ = ("timestamp", "audit_action", "event_points", "audit_data")
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        AUDIT_ACTION_FIELD_NUMBER: _ClassVar[int]
        EVENT_POINTS_FIELD_NUMBER: _ClassVar[int]
        AUDIT_DATA_FIELD_NUMBER: _ClassVar[int]
        timestamp: int
        audit_action: int
        event_points: int
        audit_data: int
        def __init__(
            self,
            timestamp: int | None = ...,
            audit_action: int | None = ...,
            event_points: int | None = ...,
            audit_data: int | None = ...,
        ) -> None: ...

    RESULT_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    LOG_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    result: bool
    event_id: _dota_shared_enums_pb2.EEvent
    log_entries: _containers.RepeatedCompositeFieldContainer[
        CMsgClientToGCRequestEventPointLogResponseV2.LogEntry
    ]
    def __init__(
        self,
        result: bool = ...,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
        log_entries: _Iterable[CMsgClientToGCRequestEventPointLogResponseV2.LogEntry | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgClientToGCPublishUserStat(_message.Message):
    __slots__ = ("user_stats_event", "reference_data")
    USER_STATS_EVENT_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_DATA_FIELD_NUMBER: _ClassVar[int]
    user_stats_event: int
    reference_data: int
    def __init__(
        self, user_stats_event: int | None = ..., reference_data: int | None = ...
    ) -> None: ...

class CMsgClientToGCRequestSlarkGameResult(_message.Message):
    __slots__ = ("event_id", "slot_chosen", "week")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    SLOT_CHOSEN_FIELD_NUMBER: _ClassVar[int]
    WEEK_FIELD_NUMBER: _ClassVar[int]
    event_id: _dota_shared_enums_pb2.EEvent
    slot_chosen: int
    week: int
    def __init__(
        self,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
        slot_chosen: int | None = ...,
        week: int | None = ...,
    ) -> None: ...

class CMsgClientToGCRequestSlarkGameResultResponse(_message.Message):
    __slots__ = ("points_won", "aura_won")
    POINTS_WON_FIELD_NUMBER: _ClassVar[int]
    AURA_WON_FIELD_NUMBER: _ClassVar[int]
    points_won: int
    aura_won: bool
    def __init__(self, points_won: int | None = ..., aura_won: bool = ...) -> None: ...

class CMsgGCToClientQuestProgressUpdated(_message.Message):
    __slots__ = ("quest_id", "completed_challenges")
    class Challenge(_message.Message):
        __slots__ = (
            "challenge_id",
            "time_completed",
            "attempts",
            "hero_id",
            "template_id",
            "quest_rank",
            "max_quest_rank",
        )
        CHALLENGE_ID_FIELD_NUMBER: _ClassVar[int]
        TIME_COMPLETED_FIELD_NUMBER: _ClassVar[int]
        ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
        QUEST_RANK_FIELD_NUMBER: _ClassVar[int]
        MAX_QUEST_RANK_FIELD_NUMBER: _ClassVar[int]
        challenge_id: int
        time_completed: int
        attempts: int
        hero_id: int
        template_id: int
        quest_rank: int
        max_quest_rank: int
        def __init__(
            self,
            challenge_id: int | None = ...,
            time_completed: int | None = ...,
            attempts: int | None = ...,
            hero_id: int | None = ...,
            template_id: int | None = ...,
            quest_rank: int | None = ...,
            max_quest_rank: int | None = ...,
        ) -> None: ...

    QUEST_ID_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_CHALLENGES_FIELD_NUMBER: _ClassVar[int]
    quest_id: int
    completed_challenges: _containers.RepeatedCompositeFieldContainer[
        CMsgGCToClientQuestProgressUpdated.Challenge
    ]
    def __init__(
        self,
        quest_id: int | None = ...,
        completed_challenges: _Iterable[CMsgGCToClientQuestProgressUpdated.Challenge | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgDOTARedeemItem(_message.Message):
    __slots__ = ("currency_id", "purchase_def")
    CURRENCY_ID_FIELD_NUMBER: _ClassVar[int]
    PURCHASE_DEF_FIELD_NUMBER: _ClassVar[int]
    currency_id: int
    purchase_def: int
    def __init__(self, currency_id: int | None = ..., purchase_def: int | None = ...) -> None: ...

class CMsgDOTARedeemItemResponse(_message.Message):
    __slots__ = ("response",)
    class EResultCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_Succeeded: _ClassVar[CMsgDOTARedeemItemResponse.EResultCode]
        k_Failed: _ClassVar[CMsgDOTARedeemItemResponse.EResultCode]

    k_Succeeded: CMsgDOTARedeemItemResponse.EResultCode
    k_Failed: CMsgDOTARedeemItemResponse.EResultCode
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgDOTARedeemItemResponse.EResultCode
    def __init__(
        self, response: CMsgDOTARedeemItemResponse.EResultCode | str | None = ...
    ) -> None: ...

class CMsgClientToGCSelectCompendiumInGamePrediction(_message.Message):
    __slots__ = ("match_id", "predictions", "league_id")
    class Prediction(_message.Message):
        __slots__ = ("prediction_id", "prediction_value")
        PREDICTION_ID_FIELD_NUMBER: _ClassVar[int]
        PREDICTION_VALUE_FIELD_NUMBER: _ClassVar[int]
        prediction_id: int
        prediction_value: int
        def __init__(
            self, prediction_id: int | None = ..., prediction_value: int | None = ...
        ) -> None: ...

    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    PREDICTIONS_FIELD_NUMBER: _ClassVar[int]
    LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    predictions: _containers.RepeatedCompositeFieldContainer[
        CMsgClientToGCSelectCompendiumInGamePrediction.Prediction
    ]
    league_id: int
    def __init__(
        self,
        match_id: int | None = ...,
        predictions: _Iterable[CMsgClientToGCSelectCompendiumInGamePrediction.Prediction | _Mapping]
        | None = ...,
        league_id: int | None = ...,
    ) -> None: ...

class CMsgClientToGCSelectCompendiumInGamePredictionResponse(_message.Message):
    __slots__ = ("result",)
    class EResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgClientToGCSelectCompendiumInGamePredictionResponse.EResult]
        INVALID_MATCH: _ClassVar[CMsgClientToGCSelectCompendiumInGamePredictionResponse.EResult]
        PREDICTIONS_ARE_CLOSED: _ClassVar[
            CMsgClientToGCSelectCompendiumInGamePredictionResponse.EResult
        ]
        OTHER_ERROR: _ClassVar[CMsgClientToGCSelectCompendiumInGamePredictionResponse.EResult]

    SUCCESS: CMsgClientToGCSelectCompendiumInGamePredictionResponse.EResult
    INVALID_MATCH: CMsgClientToGCSelectCompendiumInGamePredictionResponse.EResult
    PREDICTIONS_ARE_CLOSED: CMsgClientToGCSelectCompendiumInGamePredictionResponse.EResult
    OTHER_ERROR: CMsgClientToGCSelectCompendiumInGamePredictionResponse.EResult
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCSelectCompendiumInGamePredictionResponse.EResult
    def __init__(
        self,
        result: CMsgClientToGCSelectCompendiumInGamePredictionResponse.EResult | str | None = ...,
    ) -> None: ...

class CMsgClientToGCOpenPlayerCardPack(_message.Message):
    __slots__ = ("player_card_pack_item_id", "team_id", "deprecated_league_id", "region")
    PLAYER_CARD_PACK_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    DEPRECATED_LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    player_card_pack_item_id: int
    team_id: int
    deprecated_league_id: int
    region: _dota_shared_enums_pb2.ELeagueRegion
    def __init__(
        self,
        player_card_pack_item_id: int | None = ...,
        team_id: int | None = ...,
        deprecated_league_id: int | None = ...,
        region: _dota_shared_enums_pb2.ELeagueRegion | str | None = ...,
    ) -> None: ...

class CMsgClientToGCOpenPlayerCardPackResponse(_message.Message):
    __slots__ = ("result", "player_card_item_ids")
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgClientToGCOpenPlayerCardPackResponse.Result]
        ERROR_INTERNAL: _ClassVar[CMsgClientToGCOpenPlayerCardPackResponse.Result]
        ERROR_FAILED_TO_FIND_PACK: _ClassVar[CMsgClientToGCOpenPlayerCardPackResponse.Result]
        ERROR_ITEM_NOT_CARD_PACK: _ClassVar[CMsgClientToGCOpenPlayerCardPackResponse.Result]
        ERROR_FAILED_CARD_CREATE: _ClassVar[CMsgClientToGCOpenPlayerCardPackResponse.Result]
        ERROR_INVALID_TEAM_ID_ATTRIBUTE: _ClassVar[CMsgClientToGCOpenPlayerCardPackResponse.Result]
        ERROR_INVALID_TEAM_ID: _ClassVar[CMsgClientToGCOpenPlayerCardPackResponse.Result]

    SUCCESS: CMsgClientToGCOpenPlayerCardPackResponse.Result
    ERROR_INTERNAL: CMsgClientToGCOpenPlayerCardPackResponse.Result
    ERROR_FAILED_TO_FIND_PACK: CMsgClientToGCOpenPlayerCardPackResponse.Result
    ERROR_ITEM_NOT_CARD_PACK: CMsgClientToGCOpenPlayerCardPackResponse.Result
    ERROR_FAILED_CARD_CREATE: CMsgClientToGCOpenPlayerCardPackResponse.Result
    ERROR_INVALID_TEAM_ID_ATTRIBUTE: CMsgClientToGCOpenPlayerCardPackResponse.Result
    ERROR_INVALID_TEAM_ID: CMsgClientToGCOpenPlayerCardPackResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    PLAYER_CARD_ITEM_IDS_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCOpenPlayerCardPackResponse.Result
    player_card_item_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        result: CMsgClientToGCOpenPlayerCardPackResponse.Result | str | None = ...,
        player_card_item_ids: _Iterable[int] | None = ...,
    ) -> None: ...

class CMsgClientToGCRecyclePlayerCard(_message.Message):
    __slots__ = ("player_card_item_ids", "event_id")
    PLAYER_CARD_ITEM_IDS_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    player_card_item_ids: _containers.RepeatedScalarFieldContainer[int]
    event_id: int
    def __init__(
        self, player_card_item_ids: _Iterable[int] | None = ..., event_id: int | None = ...
    ) -> None: ...

class CMsgClientToGCRecyclePlayerCardResponse(_message.Message):
    __slots__ = ("result", "dust_amount")
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgClientToGCRecyclePlayerCardResponse.Result]
        ERROR_INTERNAL: _ClassVar[CMsgClientToGCRecyclePlayerCardResponse.Result]
        ERROR_FAILED_TO_FIND_PLAYER_CARD: _ClassVar[CMsgClientToGCRecyclePlayerCardResponse.Result]
        ERROR_ITEM_NOT_PLAYER_CARD: _ClassVar[CMsgClientToGCRecyclePlayerCardResponse.Result]
        ERROR_FAILED_DUST_CARD_CREATE: _ClassVar[CMsgClientToGCRecyclePlayerCardResponse.Result]
        ERROR_CARD_LOCKED: _ClassVar[CMsgClientToGCRecyclePlayerCardResponse.Result]
        ERROR_NO_CARDS_SPECIFIED: _ClassVar[CMsgClientToGCRecyclePlayerCardResponse.Result]

    SUCCESS: CMsgClientToGCRecyclePlayerCardResponse.Result
    ERROR_INTERNAL: CMsgClientToGCRecyclePlayerCardResponse.Result
    ERROR_FAILED_TO_FIND_PLAYER_CARD: CMsgClientToGCRecyclePlayerCardResponse.Result
    ERROR_ITEM_NOT_PLAYER_CARD: CMsgClientToGCRecyclePlayerCardResponse.Result
    ERROR_FAILED_DUST_CARD_CREATE: CMsgClientToGCRecyclePlayerCardResponse.Result
    ERROR_CARD_LOCKED: CMsgClientToGCRecyclePlayerCardResponse.Result
    ERROR_NO_CARDS_SPECIFIED: CMsgClientToGCRecyclePlayerCardResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    DUST_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCRecyclePlayerCardResponse.Result
    dust_amount: int
    def __init__(
        self,
        result: CMsgClientToGCRecyclePlayerCardResponse.Result | str | None = ...,
        dust_amount: int | None = ...,
    ) -> None: ...

class CMsgClientToGCCreatePlayerCardPack(_message.Message):
    __slots__ = ("card_dust_item_id", "event_id", "premium_pack")
    CARD_DUST_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    PREMIUM_PACK_FIELD_NUMBER: _ClassVar[int]
    card_dust_item_id: int
    event_id: int
    premium_pack: bool
    def __init__(
        self,
        card_dust_item_id: int | None = ...,
        event_id: int | None = ...,
        premium_pack: bool = ...,
    ) -> None: ...

class CMsgClientToGCCreatePlayerCardPackResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgClientToGCCreatePlayerCardPackResponse.Result]
        ERROR_INTERNAL: _ClassVar[CMsgClientToGCCreatePlayerCardPackResponse.Result]
        ERROR_INSUFFICIENT_DUST: _ClassVar[CMsgClientToGCCreatePlayerCardPackResponse.Result]
        ERROR_ITEM_NOT_DUST_ITEM: _ClassVar[CMsgClientToGCCreatePlayerCardPackResponse.Result]
        ERROR_FAILED_CARD_PACK_CREATE: _ClassVar[CMsgClientToGCCreatePlayerCardPackResponse.Result]
        ERROR_NO_CARD_PACK: _ClassVar[CMsgClientToGCCreatePlayerCardPackResponse.Result]
        ERROR_NOT_AVAILABLE: _ClassVar[CMsgClientToGCCreatePlayerCardPackResponse.Result]

    SUCCESS: CMsgClientToGCCreatePlayerCardPackResponse.Result
    ERROR_INTERNAL: CMsgClientToGCCreatePlayerCardPackResponse.Result
    ERROR_INSUFFICIENT_DUST: CMsgClientToGCCreatePlayerCardPackResponse.Result
    ERROR_ITEM_NOT_DUST_ITEM: CMsgClientToGCCreatePlayerCardPackResponse.Result
    ERROR_FAILED_CARD_PACK_CREATE: CMsgClientToGCCreatePlayerCardPackResponse.Result
    ERROR_NO_CARD_PACK: CMsgClientToGCCreatePlayerCardPackResponse.Result
    ERROR_NOT_AVAILABLE: CMsgClientToGCCreatePlayerCardPackResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCCreatePlayerCardPackResponse.Result
    def __init__(
        self, result: CMsgClientToGCCreatePlayerCardPackResponse.Result | str | None = ...
    ) -> None: ...

class CMsgClientToGCCreateTeamPlayerCardPack(_message.Message):
    __slots__ = ("card_dust_item_id", "event_id", "premium_pack", "team_id")
    CARD_DUST_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    PREMIUM_PACK_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    card_dust_item_id: int
    event_id: int
    premium_pack: bool
    team_id: int
    def __init__(
        self,
        card_dust_item_id: int | None = ...,
        event_id: int | None = ...,
        premium_pack: bool = ...,
        team_id: int | None = ...,
    ) -> None: ...

class CMsgClientToGCCreateTeamPlayerCardPackResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgClientToGCCreateTeamPlayerCardPackResponse.Result]
        ERROR_INTERNAL: _ClassVar[CMsgClientToGCCreateTeamPlayerCardPackResponse.Result]
        ERROR_INSUFFICIENT_DUST: _ClassVar[CMsgClientToGCCreateTeamPlayerCardPackResponse.Result]
        ERROR_ITEM_NOT_DUST_ITEM: _ClassVar[CMsgClientToGCCreateTeamPlayerCardPackResponse.Result]
        ERROR_FAILED_CARD_PACK_CREATE: _ClassVar[
            CMsgClientToGCCreateTeamPlayerCardPackResponse.Result
        ]
        ERROR_NO_CARD_PACK: _ClassVar[CMsgClientToGCCreateTeamPlayerCardPackResponse.Result]
        ERROR_NOT_AVAILABLE: _ClassVar[CMsgClientToGCCreateTeamPlayerCardPackResponse.Result]

    SUCCESS: CMsgClientToGCCreateTeamPlayerCardPackResponse.Result
    ERROR_INTERNAL: CMsgClientToGCCreateTeamPlayerCardPackResponse.Result
    ERROR_INSUFFICIENT_DUST: CMsgClientToGCCreateTeamPlayerCardPackResponse.Result
    ERROR_ITEM_NOT_DUST_ITEM: CMsgClientToGCCreateTeamPlayerCardPackResponse.Result
    ERROR_FAILED_CARD_PACK_CREATE: CMsgClientToGCCreateTeamPlayerCardPackResponse.Result
    ERROR_NO_CARD_PACK: CMsgClientToGCCreateTeamPlayerCardPackResponse.Result
    ERROR_NOT_AVAILABLE: CMsgClientToGCCreateTeamPlayerCardPackResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCCreateTeamPlayerCardPackResponse.Result
    def __init__(
        self, result: CMsgClientToGCCreateTeamPlayerCardPackResponse.Result | str | None = ...
    ) -> None: ...

class CMsgGCToClientBattlePassRollup_International2016(_message.Message):
    __slots__ = (
        "battle_pass_level",
        "questlines",
        "wagering",
        "achievements",
        "battle_cup",
        "predictions",
        "bracket",
        "player_cards",
        "fantasy_challenge",
    )
    class Questlines(_message.Message):
        __slots__ = ("name", "onestar", "twostar", "threestar", "total")
        NAME_FIELD_NUMBER: _ClassVar[int]
        ONESTAR_FIELD_NUMBER: _ClassVar[int]
        TWOSTAR_FIELD_NUMBER: _ClassVar[int]
        THREESTAR_FIELD_NUMBER: _ClassVar[int]
        TOTAL_FIELD_NUMBER: _ClassVar[int]
        name: str
        onestar: int
        twostar: int
        threestar: int
        total: int
        def __init__(
            self,
            name: str | None = ...,
            onestar: int | None = ...,
            twostar: int | None = ...,
            threestar: int | None = ...,
            total: int | None = ...,
        ) -> None: ...

    class Wagering(_message.Message):
        __slots__ = ("total_wagered", "total_won", "average_won", "success_rate", "total_tips")
        TOTAL_WAGERED_FIELD_NUMBER: _ClassVar[int]
        TOTAL_WON_FIELD_NUMBER: _ClassVar[int]
        AVERAGE_WON_FIELD_NUMBER: _ClassVar[int]
        SUCCESS_RATE_FIELD_NUMBER: _ClassVar[int]
        TOTAL_TIPS_FIELD_NUMBER: _ClassVar[int]
        total_wagered: int
        total_won: int
        average_won: int
        success_rate: int
        total_tips: int
        def __init__(
            self,
            total_wagered: int | None = ...,
            total_won: int | None = ...,
            average_won: int | None = ...,
            success_rate: int | None = ...,
            total_tips: int | None = ...,
        ) -> None: ...

    class Achievements(_message.Message):
        __slots__ = ("completed", "total", "points")
        COMPLETED_FIELD_NUMBER: _ClassVar[int]
        TOTAL_FIELD_NUMBER: _ClassVar[int]
        POINTS_FIELD_NUMBER: _ClassVar[int]
        completed: int
        total: int
        points: int
        def __init__(
            self, completed: int | None = ..., total: int | None = ..., points: int | None = ...
        ) -> None: ...

    class BattleCup(_message.Message):
        __slots__ = ("wins", "score")
        WINS_FIELD_NUMBER: _ClassVar[int]
        SCORE_FIELD_NUMBER: _ClassVar[int]
        wins: int
        score: int
        def __init__(self, wins: int | None = ..., score: int | None = ...) -> None: ...

    class Predictions(_message.Message):
        __slots__ = ("correct", "total", "points")
        CORRECT_FIELD_NUMBER: _ClassVar[int]
        TOTAL_FIELD_NUMBER: _ClassVar[int]
        POINTS_FIELD_NUMBER: _ClassVar[int]
        correct: int
        total: int
        points: int
        def __init__(
            self, correct: int | None = ..., total: int | None = ..., points: int | None = ...
        ) -> None: ...

    class Bracket(_message.Message):
        __slots__ = ("correct", "points")
        CORRECT_FIELD_NUMBER: _ClassVar[int]
        POINTS_FIELD_NUMBER: _ClassVar[int]
        correct: int
        points: int
        def __init__(self, correct: int | None = ..., points: int | None = ...) -> None: ...

    class PlayerCard(_message.Message):
        __slots__ = ("account_id", "quality")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        QUALITY_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        quality: int
        def __init__(self, account_id: int | None = ..., quality: int | None = ...) -> None: ...

    class FantasyChallenge(_message.Message):
        __slots__ = ("total_score", "percentile")
        TOTAL_SCORE_FIELD_NUMBER: _ClassVar[int]
        PERCENTILE_FIELD_NUMBER: _ClassVar[int]
        total_score: float
        percentile: float
        def __init__(
            self, total_score: float | None = ..., percentile: float | None = ...
        ) -> None: ...

    BATTLE_PASS_LEVEL_FIELD_NUMBER: _ClassVar[int]
    QUESTLINES_FIELD_NUMBER: _ClassVar[int]
    WAGERING_FIELD_NUMBER: _ClassVar[int]
    ACHIEVEMENTS_FIELD_NUMBER: _ClassVar[int]
    BATTLE_CUP_FIELD_NUMBER: _ClassVar[int]
    PREDICTIONS_FIELD_NUMBER: _ClassVar[int]
    BRACKET_FIELD_NUMBER: _ClassVar[int]
    PLAYER_CARDS_FIELD_NUMBER: _ClassVar[int]
    FANTASY_CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    battle_pass_level: int
    questlines: _containers.RepeatedCompositeFieldContainer[
        CMsgGCToClientBattlePassRollup_International2016.Questlines
    ]
    wagering: CMsgGCToClientBattlePassRollup_International2016.Wagering
    achievements: CMsgGCToClientBattlePassRollup_International2016.Achievements
    battle_cup: CMsgGCToClientBattlePassRollup_International2016.BattleCup
    predictions: CMsgGCToClientBattlePassRollup_International2016.Predictions
    bracket: CMsgGCToClientBattlePassRollup_International2016.Bracket
    player_cards: _containers.RepeatedCompositeFieldContainer[
        CMsgGCToClientBattlePassRollup_International2016.PlayerCard
    ]
    fantasy_challenge: CMsgGCToClientBattlePassRollup_International2016.FantasyChallenge
    def __init__(
        self,
        battle_pass_level: int | None = ...,
        questlines: _Iterable[
            CMsgGCToClientBattlePassRollup_International2016.Questlines | _Mapping
        ]
        | None = ...,
        wagering: CMsgGCToClientBattlePassRollup_International2016.Wagering | _Mapping | None = ...,
        achievements: CMsgGCToClientBattlePassRollup_International2016.Achievements
        | _Mapping
        | None = ...,
        battle_cup: CMsgGCToClientBattlePassRollup_International2016.BattleCup
        | _Mapping
        | None = ...,
        predictions: CMsgGCToClientBattlePassRollup_International2016.Predictions
        | _Mapping
        | None = ...,
        bracket: CMsgGCToClientBattlePassRollup_International2016.Bracket | _Mapping | None = ...,
        player_cards: _Iterable[
            CMsgGCToClientBattlePassRollup_International2016.PlayerCard | _Mapping
        ]
        | None = ...,
        fantasy_challenge: CMsgGCToClientBattlePassRollup_International2016.FantasyChallenge
        | _Mapping
        | None = ...,
    ) -> None: ...

class CMsgGCToClientBattlePassRollup_Fall2016(_message.Message):
    __slots__ = (
        "battle_pass_level",
        "questlines",
        "wagering",
        "achievements",
        "battle_cup",
        "predictions",
        "bracket",
        "player_cards",
        "fantasy_challenge",
    )
    class Questlines(_message.Message):
        __slots__ = ("name", "onestar", "twostar", "threestar", "total")
        NAME_FIELD_NUMBER: _ClassVar[int]
        ONESTAR_FIELD_NUMBER: _ClassVar[int]
        TWOSTAR_FIELD_NUMBER: _ClassVar[int]
        THREESTAR_FIELD_NUMBER: _ClassVar[int]
        TOTAL_FIELD_NUMBER: _ClassVar[int]
        name: str
        onestar: int
        twostar: int
        threestar: int
        total: int
        def __init__(
            self,
            name: str | None = ...,
            onestar: int | None = ...,
            twostar: int | None = ...,
            threestar: int | None = ...,
            total: int | None = ...,
        ) -> None: ...

    class Wagering(_message.Message):
        __slots__ = ("total_wagered", "total_won", "average_won", "success_rate", "total_tips")
        TOTAL_WAGERED_FIELD_NUMBER: _ClassVar[int]
        TOTAL_WON_FIELD_NUMBER: _ClassVar[int]
        AVERAGE_WON_FIELD_NUMBER: _ClassVar[int]
        SUCCESS_RATE_FIELD_NUMBER: _ClassVar[int]
        TOTAL_TIPS_FIELD_NUMBER: _ClassVar[int]
        total_wagered: int
        total_won: int
        average_won: int
        success_rate: int
        total_tips: int
        def __init__(
            self,
            total_wagered: int | None = ...,
            total_won: int | None = ...,
            average_won: int | None = ...,
            success_rate: int | None = ...,
            total_tips: int | None = ...,
        ) -> None: ...

    class Achievements(_message.Message):
        __slots__ = ("completed", "total", "points")
        COMPLETED_FIELD_NUMBER: _ClassVar[int]
        TOTAL_FIELD_NUMBER: _ClassVar[int]
        POINTS_FIELD_NUMBER: _ClassVar[int]
        completed: int
        total: int
        points: int
        def __init__(
            self, completed: int | None = ..., total: int | None = ..., points: int | None = ...
        ) -> None: ...

    class BattleCup(_message.Message):
        __slots__ = ("wins", "score")
        WINS_FIELD_NUMBER: _ClassVar[int]
        SCORE_FIELD_NUMBER: _ClassVar[int]
        wins: int
        score: int
        def __init__(self, wins: int | None = ..., score: int | None = ...) -> None: ...

    class Predictions(_message.Message):
        __slots__ = ("correct", "total", "points")
        CORRECT_FIELD_NUMBER: _ClassVar[int]
        TOTAL_FIELD_NUMBER: _ClassVar[int]
        POINTS_FIELD_NUMBER: _ClassVar[int]
        correct: int
        total: int
        points: int
        def __init__(
            self, correct: int | None = ..., total: int | None = ..., points: int | None = ...
        ) -> None: ...

    class Bracket(_message.Message):
        __slots__ = ("correct", "points")
        CORRECT_FIELD_NUMBER: _ClassVar[int]
        POINTS_FIELD_NUMBER: _ClassVar[int]
        correct: int
        points: int
        def __init__(self, correct: int | None = ..., points: int | None = ...) -> None: ...

    class PlayerCard(_message.Message):
        __slots__ = ("account_id", "quality")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        QUALITY_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        quality: int
        def __init__(self, account_id: int | None = ..., quality: int | None = ...) -> None: ...

    class FantasyChallenge(_message.Message):
        __slots__ = ("total_score", "percentile")
        TOTAL_SCORE_FIELD_NUMBER: _ClassVar[int]
        PERCENTILE_FIELD_NUMBER: _ClassVar[int]
        total_score: float
        percentile: float
        def __init__(
            self, total_score: float | None = ..., percentile: float | None = ...
        ) -> None: ...

    BATTLE_PASS_LEVEL_FIELD_NUMBER: _ClassVar[int]
    QUESTLINES_FIELD_NUMBER: _ClassVar[int]
    WAGERING_FIELD_NUMBER: _ClassVar[int]
    ACHIEVEMENTS_FIELD_NUMBER: _ClassVar[int]
    BATTLE_CUP_FIELD_NUMBER: _ClassVar[int]
    PREDICTIONS_FIELD_NUMBER: _ClassVar[int]
    BRACKET_FIELD_NUMBER: _ClassVar[int]
    PLAYER_CARDS_FIELD_NUMBER: _ClassVar[int]
    FANTASY_CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    battle_pass_level: int
    questlines: _containers.RepeatedCompositeFieldContainer[
        CMsgGCToClientBattlePassRollup_Fall2016.Questlines
    ]
    wagering: CMsgGCToClientBattlePassRollup_Fall2016.Wagering
    achievements: CMsgGCToClientBattlePassRollup_Fall2016.Achievements
    battle_cup: CMsgGCToClientBattlePassRollup_Fall2016.BattleCup
    predictions: CMsgGCToClientBattlePassRollup_Fall2016.Predictions
    bracket: CMsgGCToClientBattlePassRollup_Fall2016.Bracket
    player_cards: _containers.RepeatedCompositeFieldContainer[
        CMsgGCToClientBattlePassRollup_Fall2016.PlayerCard
    ]
    fantasy_challenge: CMsgGCToClientBattlePassRollup_Fall2016.FantasyChallenge
    def __init__(
        self,
        battle_pass_level: int | None = ...,
        questlines: _Iterable[CMsgGCToClientBattlePassRollup_Fall2016.Questlines | _Mapping]
        | None = ...,
        wagering: CMsgGCToClientBattlePassRollup_Fall2016.Wagering | _Mapping | None = ...,
        achievements: CMsgGCToClientBattlePassRollup_Fall2016.Achievements | _Mapping | None = ...,
        battle_cup: CMsgGCToClientBattlePassRollup_Fall2016.BattleCup | _Mapping | None = ...,
        predictions: CMsgGCToClientBattlePassRollup_Fall2016.Predictions | _Mapping | None = ...,
        bracket: CMsgGCToClientBattlePassRollup_Fall2016.Bracket | _Mapping | None = ...,
        player_cards: _Iterable[CMsgGCToClientBattlePassRollup_Fall2016.PlayerCard | _Mapping]
        | None = ...,
        fantasy_challenge: CMsgGCToClientBattlePassRollup_Fall2016.FantasyChallenge
        | _Mapping
        | None = ...,
    ) -> None: ...

class CMsgGCToClientBattlePassRollup_Winter2017(_message.Message):
    __slots__ = (
        "battle_pass_level",
        "questlines",
        "wagering",
        "achievements",
        "battle_cup",
        "predictions",
        "bracket",
        "player_cards",
        "fantasy_challenge",
    )
    class Questlines(_message.Message):
        __slots__ = ("name", "onestar", "twostar", "threestar", "total")
        NAME_FIELD_NUMBER: _ClassVar[int]
        ONESTAR_FIELD_NUMBER: _ClassVar[int]
        TWOSTAR_FIELD_NUMBER: _ClassVar[int]
        THREESTAR_FIELD_NUMBER: _ClassVar[int]
        TOTAL_FIELD_NUMBER: _ClassVar[int]
        name: str
        onestar: int
        twostar: int
        threestar: int
        total: int
        def __init__(
            self,
            name: str | None = ...,
            onestar: int | None = ...,
            twostar: int | None = ...,
            threestar: int | None = ...,
            total: int | None = ...,
        ) -> None: ...

    class Wagering(_message.Message):
        __slots__ = ("total_wagered", "total_won", "average_won", "success_rate", "total_tips")
        TOTAL_WAGERED_FIELD_NUMBER: _ClassVar[int]
        TOTAL_WON_FIELD_NUMBER: _ClassVar[int]
        AVERAGE_WON_FIELD_NUMBER: _ClassVar[int]
        SUCCESS_RATE_FIELD_NUMBER: _ClassVar[int]
        TOTAL_TIPS_FIELD_NUMBER: _ClassVar[int]
        total_wagered: int
        total_won: int
        average_won: int
        success_rate: int
        total_tips: int
        def __init__(
            self,
            total_wagered: int | None = ...,
            total_won: int | None = ...,
            average_won: int | None = ...,
            success_rate: int | None = ...,
            total_tips: int | None = ...,
        ) -> None: ...

    class Achievements(_message.Message):
        __slots__ = ("completed", "total", "points")
        COMPLETED_FIELD_NUMBER: _ClassVar[int]
        TOTAL_FIELD_NUMBER: _ClassVar[int]
        POINTS_FIELD_NUMBER: _ClassVar[int]
        completed: int
        total: int
        points: int
        def __init__(
            self, completed: int | None = ..., total: int | None = ..., points: int | None = ...
        ) -> None: ...

    class BattleCup(_message.Message):
        __slots__ = ("wins", "score")
        WINS_FIELD_NUMBER: _ClassVar[int]
        SCORE_FIELD_NUMBER: _ClassVar[int]
        wins: int
        score: int
        def __init__(self, wins: int | None = ..., score: int | None = ...) -> None: ...

    class Predictions(_message.Message):
        __slots__ = ("correct", "total", "points")
        CORRECT_FIELD_NUMBER: _ClassVar[int]
        TOTAL_FIELD_NUMBER: _ClassVar[int]
        POINTS_FIELD_NUMBER: _ClassVar[int]
        correct: int
        total: int
        points: int
        def __init__(
            self, correct: int | None = ..., total: int | None = ..., points: int | None = ...
        ) -> None: ...

    class Bracket(_message.Message):
        __slots__ = ("correct", "points")
        CORRECT_FIELD_NUMBER: _ClassVar[int]
        POINTS_FIELD_NUMBER: _ClassVar[int]
        correct: int
        points: int
        def __init__(self, correct: int | None = ..., points: int | None = ...) -> None: ...

    class PlayerCard(_message.Message):
        __slots__ = ("account_id", "quality")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        QUALITY_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        quality: int
        def __init__(self, account_id: int | None = ..., quality: int | None = ...) -> None: ...

    class FantasyChallenge(_message.Message):
        __slots__ = ("total_score", "percentile")
        TOTAL_SCORE_FIELD_NUMBER: _ClassVar[int]
        PERCENTILE_FIELD_NUMBER: _ClassVar[int]
        total_score: float
        percentile: float
        def __init__(
            self, total_score: float | None = ..., percentile: float | None = ...
        ) -> None: ...

    BATTLE_PASS_LEVEL_FIELD_NUMBER: _ClassVar[int]
    QUESTLINES_FIELD_NUMBER: _ClassVar[int]
    WAGERING_FIELD_NUMBER: _ClassVar[int]
    ACHIEVEMENTS_FIELD_NUMBER: _ClassVar[int]
    BATTLE_CUP_FIELD_NUMBER: _ClassVar[int]
    PREDICTIONS_FIELD_NUMBER: _ClassVar[int]
    BRACKET_FIELD_NUMBER: _ClassVar[int]
    PLAYER_CARDS_FIELD_NUMBER: _ClassVar[int]
    FANTASY_CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    battle_pass_level: int
    questlines: _containers.RepeatedCompositeFieldContainer[
        CMsgGCToClientBattlePassRollup_Winter2017.Questlines
    ]
    wagering: CMsgGCToClientBattlePassRollup_Winter2017.Wagering
    achievements: CMsgGCToClientBattlePassRollup_Winter2017.Achievements
    battle_cup: CMsgGCToClientBattlePassRollup_Winter2017.BattleCup
    predictions: CMsgGCToClientBattlePassRollup_Winter2017.Predictions
    bracket: CMsgGCToClientBattlePassRollup_Winter2017.Bracket
    player_cards: _containers.RepeatedCompositeFieldContainer[
        CMsgGCToClientBattlePassRollup_Winter2017.PlayerCard
    ]
    fantasy_challenge: CMsgGCToClientBattlePassRollup_Winter2017.FantasyChallenge
    def __init__(
        self,
        battle_pass_level: int | None = ...,
        questlines: _Iterable[CMsgGCToClientBattlePassRollup_Winter2017.Questlines | _Mapping]
        | None = ...,
        wagering: CMsgGCToClientBattlePassRollup_Winter2017.Wagering | _Mapping | None = ...,
        achievements: CMsgGCToClientBattlePassRollup_Winter2017.Achievements
        | _Mapping
        | None = ...,
        battle_cup: CMsgGCToClientBattlePassRollup_Winter2017.BattleCup | _Mapping | None = ...,
        predictions: CMsgGCToClientBattlePassRollup_Winter2017.Predictions | _Mapping | None = ...,
        bracket: CMsgGCToClientBattlePassRollup_Winter2017.Bracket | _Mapping | None = ...,
        player_cards: _Iterable[CMsgGCToClientBattlePassRollup_Winter2017.PlayerCard | _Mapping]
        | None = ...,
        fantasy_challenge: CMsgGCToClientBattlePassRollup_Winter2017.FantasyChallenge
        | _Mapping
        | None = ...,
    ) -> None: ...

class CMsgGCToClientBattlePassRollup_TI7(_message.Message):
    __slots__ = (
        "battle_pass_level",
        "questlines",
        "wagering",
        "achievements",
        "battle_cup",
        "predictions",
        "bracket",
        "player_cards",
        "fantasy_challenge",
    )
    class Questlines(_message.Message):
        __slots__ = ("name", "onestar", "twostar", "threestar", "total")
        NAME_FIELD_NUMBER: _ClassVar[int]
        ONESTAR_FIELD_NUMBER: _ClassVar[int]
        TWOSTAR_FIELD_NUMBER: _ClassVar[int]
        THREESTAR_FIELD_NUMBER: _ClassVar[int]
        TOTAL_FIELD_NUMBER: _ClassVar[int]
        name: str
        onestar: int
        twostar: int
        threestar: int
        total: int
        def __init__(
            self,
            name: str | None = ...,
            onestar: int | None = ...,
            twostar: int | None = ...,
            threestar: int | None = ...,
            total: int | None = ...,
        ) -> None: ...

    class Wagering(_message.Message):
        __slots__ = ("total_wagered", "total_won", "average_won", "success_rate", "total_tips")
        TOTAL_WAGERED_FIELD_NUMBER: _ClassVar[int]
        TOTAL_WON_FIELD_NUMBER: _ClassVar[int]
        AVERAGE_WON_FIELD_NUMBER: _ClassVar[int]
        SUCCESS_RATE_FIELD_NUMBER: _ClassVar[int]
        TOTAL_TIPS_FIELD_NUMBER: _ClassVar[int]
        total_wagered: int
        total_won: int
        average_won: int
        success_rate: int
        total_tips: int
        def __init__(
            self,
            total_wagered: int | None = ...,
            total_won: int | None = ...,
            average_won: int | None = ...,
            success_rate: int | None = ...,
            total_tips: int | None = ...,
        ) -> None: ...

    class Achievements(_message.Message):
        __slots__ = ("completed", "total", "points")
        COMPLETED_FIELD_NUMBER: _ClassVar[int]
        TOTAL_FIELD_NUMBER: _ClassVar[int]
        POINTS_FIELD_NUMBER: _ClassVar[int]
        completed: int
        total: int
        points: int
        def __init__(
            self, completed: int | None = ..., total: int | None = ..., points: int | None = ...
        ) -> None: ...

    class BattleCup(_message.Message):
        __slots__ = ("wins", "score")
        WINS_FIELD_NUMBER: _ClassVar[int]
        SCORE_FIELD_NUMBER: _ClassVar[int]
        wins: int
        score: int
        def __init__(self, wins: int | None = ..., score: int | None = ...) -> None: ...

    class Predictions(_message.Message):
        __slots__ = ("correct", "total", "points")
        CORRECT_FIELD_NUMBER: _ClassVar[int]
        TOTAL_FIELD_NUMBER: _ClassVar[int]
        POINTS_FIELD_NUMBER: _ClassVar[int]
        correct: int
        total: int
        points: int
        def __init__(
            self, correct: int | None = ..., total: int | None = ..., points: int | None = ...
        ) -> None: ...

    class Bracket(_message.Message):
        __slots__ = ("correct", "points")
        CORRECT_FIELD_NUMBER: _ClassVar[int]
        POINTS_FIELD_NUMBER: _ClassVar[int]
        correct: int
        points: int
        def __init__(self, correct: int | None = ..., points: int | None = ...) -> None: ...

    class PlayerCard(_message.Message):
        __slots__ = ("account_id", "quality")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        QUALITY_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        quality: int
        def __init__(self, account_id: int | None = ..., quality: int | None = ...) -> None: ...

    class FantasyChallenge(_message.Message):
        __slots__ = ("total_score", "percentile")
        TOTAL_SCORE_FIELD_NUMBER: _ClassVar[int]
        PERCENTILE_FIELD_NUMBER: _ClassVar[int]
        total_score: float
        percentile: float
        def __init__(
            self, total_score: float | None = ..., percentile: float | None = ...
        ) -> None: ...

    BATTLE_PASS_LEVEL_FIELD_NUMBER: _ClassVar[int]
    QUESTLINES_FIELD_NUMBER: _ClassVar[int]
    WAGERING_FIELD_NUMBER: _ClassVar[int]
    ACHIEVEMENTS_FIELD_NUMBER: _ClassVar[int]
    BATTLE_CUP_FIELD_NUMBER: _ClassVar[int]
    PREDICTIONS_FIELD_NUMBER: _ClassVar[int]
    BRACKET_FIELD_NUMBER: _ClassVar[int]
    PLAYER_CARDS_FIELD_NUMBER: _ClassVar[int]
    FANTASY_CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    battle_pass_level: int
    questlines: _containers.RepeatedCompositeFieldContainer[
        CMsgGCToClientBattlePassRollup_TI7.Questlines
    ]
    wagering: CMsgGCToClientBattlePassRollup_TI7.Wagering
    achievements: CMsgGCToClientBattlePassRollup_TI7.Achievements
    battle_cup: CMsgGCToClientBattlePassRollup_TI7.BattleCup
    predictions: CMsgGCToClientBattlePassRollup_TI7.Predictions
    bracket: CMsgGCToClientBattlePassRollup_TI7.Bracket
    player_cards: _containers.RepeatedCompositeFieldContainer[
        CMsgGCToClientBattlePassRollup_TI7.PlayerCard
    ]
    fantasy_challenge: CMsgGCToClientBattlePassRollup_TI7.FantasyChallenge
    def __init__(
        self,
        battle_pass_level: int | None = ...,
        questlines: _Iterable[CMsgGCToClientBattlePassRollup_TI7.Questlines | _Mapping]
        | None = ...,
        wagering: CMsgGCToClientBattlePassRollup_TI7.Wagering | _Mapping | None = ...,
        achievements: CMsgGCToClientBattlePassRollup_TI7.Achievements | _Mapping | None = ...,
        battle_cup: CMsgGCToClientBattlePassRollup_TI7.BattleCup | _Mapping | None = ...,
        predictions: CMsgGCToClientBattlePassRollup_TI7.Predictions | _Mapping | None = ...,
        bracket: CMsgGCToClientBattlePassRollup_TI7.Bracket | _Mapping | None = ...,
        player_cards: _Iterable[CMsgGCToClientBattlePassRollup_TI7.PlayerCard | _Mapping]
        | None = ...,
        fantasy_challenge: CMsgGCToClientBattlePassRollup_TI7.FantasyChallenge
        | _Mapping
        | None = ...,
    ) -> None: ...

class CMsgGCToClientBattlePassRollup_TI8(_message.Message):
    __slots__ = (
        "battle_pass_level",
        "cavern_crawl",
        "wagering",
        "achievements",
        "predictions",
        "bracket",
        "player_cards",
        "fantasy_challenge",
    )
    class CavernCrawl(_message.Message):
        __slots__ = ("rooms_cleared", "carry_completed", "support_completed", "utility_completed")
        ROOMS_CLEARED_FIELD_NUMBER: _ClassVar[int]
        CARRY_COMPLETED_FIELD_NUMBER: _ClassVar[int]
        SUPPORT_COMPLETED_FIELD_NUMBER: _ClassVar[int]
        UTILITY_COMPLETED_FIELD_NUMBER: _ClassVar[int]
        rooms_cleared: int
        carry_completed: bool
        support_completed: bool
        utility_completed: bool
        def __init__(
            self,
            rooms_cleared: int | None = ...,
            carry_completed: bool = ...,
            support_completed: bool = ...,
            utility_completed: bool = ...,
        ) -> None: ...

    class Wagering(_message.Message):
        __slots__ = ("total_wagered", "total_won", "average_won", "success_rate", "total_tips")
        TOTAL_WAGERED_FIELD_NUMBER: _ClassVar[int]
        TOTAL_WON_FIELD_NUMBER: _ClassVar[int]
        AVERAGE_WON_FIELD_NUMBER: _ClassVar[int]
        SUCCESS_RATE_FIELD_NUMBER: _ClassVar[int]
        TOTAL_TIPS_FIELD_NUMBER: _ClassVar[int]
        total_wagered: int
        total_won: int
        average_won: int
        success_rate: int
        total_tips: int
        def __init__(
            self,
            total_wagered: int | None = ...,
            total_won: int | None = ...,
            average_won: int | None = ...,
            success_rate: int | None = ...,
            total_tips: int | None = ...,
        ) -> None: ...

    class Achievements(_message.Message):
        __slots__ = ("completed", "total", "points")
        COMPLETED_FIELD_NUMBER: _ClassVar[int]
        TOTAL_FIELD_NUMBER: _ClassVar[int]
        POINTS_FIELD_NUMBER: _ClassVar[int]
        completed: int
        total: int
        points: int
        def __init__(
            self, completed: int | None = ..., total: int | None = ..., points: int | None = ...
        ) -> None: ...

    class Predictions(_message.Message):
        __slots__ = ("correct", "total", "points")
        CORRECT_FIELD_NUMBER: _ClassVar[int]
        TOTAL_FIELD_NUMBER: _ClassVar[int]
        POINTS_FIELD_NUMBER: _ClassVar[int]
        correct: int
        total: int
        points: int
        def __init__(
            self, correct: int | None = ..., total: int | None = ..., points: int | None = ...
        ) -> None: ...

    class Bracket(_message.Message):
        __slots__ = ("correct", "points")
        CORRECT_FIELD_NUMBER: _ClassVar[int]
        POINTS_FIELD_NUMBER: _ClassVar[int]
        correct: int
        points: int
        def __init__(self, correct: int | None = ..., points: int | None = ...) -> None: ...

    class PlayerCard(_message.Message):
        __slots__ = ("account_id", "quality")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        QUALITY_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        quality: int
        def __init__(self, account_id: int | None = ..., quality: int | None = ...) -> None: ...

    class FantasyChallenge(_message.Message):
        __slots__ = ("total_score", "percentile")
        TOTAL_SCORE_FIELD_NUMBER: _ClassVar[int]
        PERCENTILE_FIELD_NUMBER: _ClassVar[int]
        total_score: float
        percentile: float
        def __init__(
            self, total_score: float | None = ..., percentile: float | None = ...
        ) -> None: ...

    BATTLE_PASS_LEVEL_FIELD_NUMBER: _ClassVar[int]
    CAVERN_CRAWL_FIELD_NUMBER: _ClassVar[int]
    WAGERING_FIELD_NUMBER: _ClassVar[int]
    ACHIEVEMENTS_FIELD_NUMBER: _ClassVar[int]
    PREDICTIONS_FIELD_NUMBER: _ClassVar[int]
    BRACKET_FIELD_NUMBER: _ClassVar[int]
    PLAYER_CARDS_FIELD_NUMBER: _ClassVar[int]
    FANTASY_CHALLENGE_FIELD_NUMBER: _ClassVar[int]
    battle_pass_level: int
    cavern_crawl: CMsgGCToClientBattlePassRollup_TI8.CavernCrawl
    wagering: CMsgGCToClientBattlePassRollup_TI8.Wagering
    achievements: CMsgGCToClientBattlePassRollup_TI8.Achievements
    predictions: CMsgGCToClientBattlePassRollup_TI8.Predictions
    bracket: CMsgGCToClientBattlePassRollup_TI8.Bracket
    player_cards: _containers.RepeatedCompositeFieldContainer[
        CMsgGCToClientBattlePassRollup_TI8.PlayerCard
    ]
    fantasy_challenge: CMsgGCToClientBattlePassRollup_TI8.FantasyChallenge
    def __init__(
        self,
        battle_pass_level: int | None = ...,
        cavern_crawl: CMsgGCToClientBattlePassRollup_TI8.CavernCrawl | _Mapping | None = ...,
        wagering: CMsgGCToClientBattlePassRollup_TI8.Wagering | _Mapping | None = ...,
        achievements: CMsgGCToClientBattlePassRollup_TI8.Achievements | _Mapping | None = ...,
        predictions: CMsgGCToClientBattlePassRollup_TI8.Predictions | _Mapping | None = ...,
        bracket: CMsgGCToClientBattlePassRollup_TI8.Bracket | _Mapping | None = ...,
        player_cards: _Iterable[CMsgGCToClientBattlePassRollup_TI8.PlayerCard | _Mapping]
        | None = ...,
        fantasy_challenge: CMsgGCToClientBattlePassRollup_TI8.FantasyChallenge
        | _Mapping
        | None = ...,
    ) -> None: ...

class CMsgGCToClientBattlePassRollup_TI9(_message.Message):
    __slots__ = ("battle_pass_level",)
    BATTLE_PASS_LEVEL_FIELD_NUMBER: _ClassVar[int]
    battle_pass_level: int
    def __init__(self, battle_pass_level: int | None = ...) -> None: ...

class CMsgGCToClientBattlePassRollup_TI10(_message.Message):
    __slots__ = ("battle_pass_level",)
    BATTLE_PASS_LEVEL_FIELD_NUMBER: _ClassVar[int]
    battle_pass_level: int
    def __init__(self, battle_pass_level: int | None = ...) -> None: ...

class CMsgGCToClientBattlePassRollupRequest(_message.Message):
    __slots__ = ("event_id", "account_id")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    account_id: int
    def __init__(self, event_id: int | None = ..., account_id: int | None = ...) -> None: ...

class CMsgGCToClientBattlePassRollupResponse(_message.Message):
    __slots__ = (
        "event_ti6",
        "event_fall2016",
        "event_winter2017",
        "event_ti7",
        "event_ti8",
        "event_ti9",
        "event_ti10",
    )
    EVENT_TI6_FIELD_NUMBER: _ClassVar[int]
    EVENT_FALL2016_FIELD_NUMBER: _ClassVar[int]
    EVENT_WINTER2017_FIELD_NUMBER: _ClassVar[int]
    EVENT_TI7_FIELD_NUMBER: _ClassVar[int]
    EVENT_TI8_FIELD_NUMBER: _ClassVar[int]
    EVENT_TI9_FIELD_NUMBER: _ClassVar[int]
    EVENT_TI10_FIELD_NUMBER: _ClassVar[int]
    event_ti6: CMsgGCToClientBattlePassRollup_International2016
    event_fall2016: CMsgGCToClientBattlePassRollup_Fall2016
    event_winter2017: CMsgGCToClientBattlePassRollup_Winter2017
    event_ti7: CMsgGCToClientBattlePassRollup_TI7
    event_ti8: CMsgGCToClientBattlePassRollup_TI8
    event_ti9: CMsgGCToClientBattlePassRollup_TI9
    event_ti10: CMsgGCToClientBattlePassRollup_TI10
    def __init__(
        self,
        event_ti6: CMsgGCToClientBattlePassRollup_International2016 | _Mapping | None = ...,
        event_fall2016: CMsgGCToClientBattlePassRollup_Fall2016 | _Mapping | None = ...,
        event_winter2017: CMsgGCToClientBattlePassRollup_Winter2017 | _Mapping | None = ...,
        event_ti7: CMsgGCToClientBattlePassRollup_TI7 | _Mapping | None = ...,
        event_ti8: CMsgGCToClientBattlePassRollup_TI8 | _Mapping | None = ...,
        event_ti9: CMsgGCToClientBattlePassRollup_TI9 | _Mapping | None = ...,
        event_ti10: CMsgGCToClientBattlePassRollup_TI10 | _Mapping | None = ...,
    ) -> None: ...

class CMsgGCToClientBattlePassRollupListRequest(_message.Message):
    __slots__ = ("account_id",)
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    def __init__(self, account_id: int | None = ...) -> None: ...

class CMsgGCToClientBattlePassRollupListResponse(_message.Message):
    __slots__ = ("event_info",)
    class EventInfo(_message.Message):
        __slots__ = ("event_id", "level")
        EVENT_ID_FIELD_NUMBER: _ClassVar[int]
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        event_id: int
        level: int
        def __init__(self, event_id: int | None = ..., level: int | None = ...) -> None: ...

    EVENT_INFO_FIELD_NUMBER: _ClassVar[int]
    event_info: _containers.RepeatedCompositeFieldContainer[
        CMsgGCToClientBattlePassRollupListResponse.EventInfo
    ]
    def __init__(
        self,
        event_info: _Iterable[CMsgGCToClientBattlePassRollupListResponse.EventInfo | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgClientToGCTransferSeasonalMMRRequest(_message.Message):
    __slots__ = ("is_party",)
    IS_PARTY_FIELD_NUMBER: _ClassVar[int]
    is_party: bool
    def __init__(self, is_party: bool = ...) -> None: ...

class CMsgClientToGCTransferSeasonalMMRResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class CMsgGCToClientPlaytestStatus(_message.Message):
    __slots__ = ("active",)
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    active: bool
    def __init__(self, active: bool = ...) -> None: ...

class CMsgClientToGCJoinPlaytest(_message.Message):
    __slots__ = ("client_version",)
    CLIENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    client_version: int
    def __init__(self, client_version: int | None = ...) -> None: ...

class CMsgClientToGCJoinPlaytestResponse(_message.Message):
    __slots__ = ("error",)
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: str
    def __init__(self, error: str | None = ...) -> None: ...

class CMsgDOTASetFavoriteTeam(_message.Message):
    __slots__ = ("team_id", "event_id")
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    team_id: int
    event_id: int
    def __init__(self, team_id: int | None = ..., event_id: int | None = ...) -> None: ...

class CMsgDOTATriviaCurrentQuestions(_message.Message):
    __slots__ = ("questions", "trivia_enabled")
    QUESTIONS_FIELD_NUMBER: _ClassVar[int]
    TRIVIA_ENABLED_FIELD_NUMBER: _ClassVar[int]
    questions: _containers.RepeatedCompositeFieldContainer[
        _dota_gcmessages_common_pb2.CMsgDOTATriviaQuestion
    ]
    trivia_enabled: bool
    def __init__(
        self,
        questions: _Iterable[_dota_gcmessages_common_pb2.CMsgDOTATriviaQuestion | _Mapping]
        | None = ...,
        trivia_enabled: bool = ...,
    ) -> None: ...

class CMsgDOTASubmitTriviaQuestionAnswer(_message.Message):
    __slots__ = ("question_id", "answer_index")
    QUESTION_ID_FIELD_NUMBER: _ClassVar[int]
    ANSWER_INDEX_FIELD_NUMBER: _ClassVar[int]
    question_id: int
    answer_index: int
    def __init__(self, question_id: int | None = ..., answer_index: int | None = ...) -> None: ...

class CMsgDOTASubmitTriviaQuestionAnswerResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: EDOTATriviaAnswerResult
    def __init__(self, result: EDOTATriviaAnswerResult | str | None = ...) -> None: ...

class CMsgDOTAStartTriviaSession(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgDOTAStartTriviaSessionResponse(_message.Message):
    __slots__ = ("trivia_enabled", "current_timestamp")
    TRIVIA_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CURRENT_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    trivia_enabled: bool
    current_timestamp: int
    def __init__(self, trivia_enabled: bool = ..., current_timestamp: int | None = ...) -> None: ...

class CMsgDOTAAnchorPhoneNumberRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgDOTAAnchorPhoneNumberResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgDOTAAnchorPhoneNumberResponse.Result]
        ERROR_UNKNOWN: _ClassVar[CMsgDOTAAnchorPhoneNumberResponse.Result]
        ERROR_NO_STEAM_PHONE: _ClassVar[CMsgDOTAAnchorPhoneNumberResponse.Result]
        ERROR_ALREADY_IN_USE: _ClassVar[CMsgDOTAAnchorPhoneNumberResponse.Result]
        ERROR_COOLDOWN_ACTIVE: _ClassVar[CMsgDOTAAnchorPhoneNumberResponse.Result]
        ERROR_GAC_ISSUE: _ClassVar[CMsgDOTAAnchorPhoneNumberResponse.Result]

    SUCCESS: CMsgDOTAAnchorPhoneNumberResponse.Result
    ERROR_UNKNOWN: CMsgDOTAAnchorPhoneNumberResponse.Result
    ERROR_NO_STEAM_PHONE: CMsgDOTAAnchorPhoneNumberResponse.Result
    ERROR_ALREADY_IN_USE: CMsgDOTAAnchorPhoneNumberResponse.Result
    ERROR_COOLDOWN_ACTIVE: CMsgDOTAAnchorPhoneNumberResponse.Result
    ERROR_GAC_ISSUE: CMsgDOTAAnchorPhoneNumberResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgDOTAAnchorPhoneNumberResponse.Result
    def __init__(
        self, result: CMsgDOTAAnchorPhoneNumberResponse.Result | str | None = ...
    ) -> None: ...

class CMsgDOTAUnanchorPhoneNumberRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgDOTAUnanchorPhoneNumberResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgDOTAUnanchorPhoneNumberResponse.Result]
        ERROR_UNKNOWN: _ClassVar[CMsgDOTAUnanchorPhoneNumberResponse.Result]

    SUCCESS: CMsgDOTAUnanchorPhoneNumberResponse.Result
    ERROR_UNKNOWN: CMsgDOTAUnanchorPhoneNumberResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgDOTAUnanchorPhoneNumberResponse.Result
    def __init__(
        self, result: CMsgDOTAUnanchorPhoneNumberResponse.Result | str | None = ...
    ) -> None: ...

class CMsgGCToClientCommendNotification(_message.Message):
    __slots__ = ("commender_account_id", "commender_name", "flags", "commender_hero_id")
    COMMENDER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    COMMENDER_NAME_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    COMMENDER_HERO_ID_FIELD_NUMBER: _ClassVar[int]
    commender_account_id: int
    commender_name: str
    flags: int
    commender_hero_id: int
    def __init__(
        self,
        commender_account_id: int | None = ...,
        commender_name: str | None = ...,
        flags: int | None = ...,
        commender_hero_id: int | None = ...,
    ) -> None: ...

class CMsgDOTAClientToGCQuickStatsRequest(_message.Message):
    __slots__ = ("player_account_id", "hero_id", "item_id", "league_id")
    PLAYER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    player_account_id: int
    hero_id: int
    item_id: int
    league_id: int
    def __init__(
        self,
        player_account_id: int | None = ...,
        hero_id: int | None = ...,
        item_id: int | None = ...,
        league_id: int | None = ...,
    ) -> None: ...

class CMsgDOTAClientToGCQuickStatsResponse(_message.Message):
    __slots__ = (
        "original_request",
        "hero_stats",
        "item_stats",
        "item_hero_stats",
        "item_player_stats",
        "hero_player_stats",
        "full_set_stats",
    )
    class SimpleStats(_message.Message):
        __slots__ = ("win_percent", "pick_percent", "win_count", "pick_count")
        WIN_PERCENT_FIELD_NUMBER: _ClassVar[int]
        PICK_PERCENT_FIELD_NUMBER: _ClassVar[int]
        WIN_COUNT_FIELD_NUMBER: _ClassVar[int]
        PICK_COUNT_FIELD_NUMBER: _ClassVar[int]
        win_percent: float
        pick_percent: float
        win_count: int
        pick_count: int
        def __init__(
            self,
            win_percent: float | None = ...,
            pick_percent: float | None = ...,
            win_count: int | None = ...,
            pick_count: int | None = ...,
        ) -> None: ...

    ORIGINAL_REQUEST_FIELD_NUMBER: _ClassVar[int]
    HERO_STATS_FIELD_NUMBER: _ClassVar[int]
    ITEM_STATS_FIELD_NUMBER: _ClassVar[int]
    ITEM_HERO_STATS_FIELD_NUMBER: _ClassVar[int]
    ITEM_PLAYER_STATS_FIELD_NUMBER: _ClassVar[int]
    HERO_PLAYER_STATS_FIELD_NUMBER: _ClassVar[int]
    FULL_SET_STATS_FIELD_NUMBER: _ClassVar[int]
    original_request: CMsgDOTAClientToGCQuickStatsRequest
    hero_stats: CMsgDOTAClientToGCQuickStatsResponse.SimpleStats
    item_stats: CMsgDOTAClientToGCQuickStatsResponse.SimpleStats
    item_hero_stats: CMsgDOTAClientToGCQuickStatsResponse.SimpleStats
    item_player_stats: CMsgDOTAClientToGCQuickStatsResponse.SimpleStats
    hero_player_stats: CMsgDOTAClientToGCQuickStatsResponse.SimpleStats
    full_set_stats: CMsgDOTAClientToGCQuickStatsResponse.SimpleStats
    def __init__(
        self,
        original_request: CMsgDOTAClientToGCQuickStatsRequest | _Mapping | None = ...,
        hero_stats: CMsgDOTAClientToGCQuickStatsResponse.SimpleStats | _Mapping | None = ...,
        item_stats: CMsgDOTAClientToGCQuickStatsResponse.SimpleStats | _Mapping | None = ...,
        item_hero_stats: CMsgDOTAClientToGCQuickStatsResponse.SimpleStats | _Mapping | None = ...,
        item_player_stats: CMsgDOTAClientToGCQuickStatsResponse.SimpleStats | _Mapping | None = ...,
        hero_player_stats: CMsgDOTAClientToGCQuickStatsResponse.SimpleStats | _Mapping | None = ...,
        full_set_stats: CMsgDOTAClientToGCQuickStatsResponse.SimpleStats | _Mapping | None = ...,
    ) -> None: ...

class CMsgDOTASelectionPriorityChoiceRequest(_message.Message):
    __slots__ = ("choice",)
    CHOICE_FIELD_NUMBER: _ClassVar[int]
    choice: _dota_shared_enums_pb2.DOTASelectionPriorityChoice
    def __init__(
        self, choice: _dota_shared_enums_pb2.DOTASelectionPriorityChoice | str | None = ...
    ) -> None: ...

class CMsgDOTASelectionPriorityChoiceResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgDOTASelectionPriorityChoiceResponse.Result]
        ERROR_UNKNOWN: _ClassVar[CMsgDOTASelectionPriorityChoiceResponse.Result]

    SUCCESS: CMsgDOTASelectionPriorityChoiceResponse.Result
    ERROR_UNKNOWN: CMsgDOTASelectionPriorityChoiceResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgDOTASelectionPriorityChoiceResponse.Result
    def __init__(
        self, result: CMsgDOTASelectionPriorityChoiceResponse.Result | str | None = ...
    ) -> None: ...

class CMsgDOTAGameAutographReward(_message.Message):
    __slots__ = ("badge_id",)
    BADGE_ID_FIELD_NUMBER: _ClassVar[int]
    badge_id: str
    def __init__(self, badge_id: str | None = ...) -> None: ...

class CMsgDOTAGameAutographRewardResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgDOTAGameAutographRewardResponse.Result]
        ERROR_UNKNOWN: _ClassVar[CMsgDOTAGameAutographRewardResponse.Result]

    SUCCESS: CMsgDOTAGameAutographRewardResponse.Result
    ERROR_UNKNOWN: CMsgDOTAGameAutographRewardResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgDOTAGameAutographRewardResponse.Result
    def __init__(
        self, result: CMsgDOTAGameAutographRewardResponse.Result | str | None = ...
    ) -> None: ...

class CMsgDOTADestroyLobbyRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgDOTADestroyLobbyResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgDOTADestroyLobbyResponse.Result]
        ERROR_UNKNOWN: _ClassVar[CMsgDOTADestroyLobbyResponse.Result]

    SUCCESS: CMsgDOTADestroyLobbyResponse.Result
    ERROR_UNKNOWN: CMsgDOTADestroyLobbyResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgDOTADestroyLobbyResponse.Result
    def __init__(self, result: CMsgDOTADestroyLobbyResponse.Result | str | None = ...) -> None: ...

class CMsgDOTAGetRecentPlayTimeFriendsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgDOTAGetRecentPlayTimeFriendsResponse(_message.Message):
    __slots__ = ("account_ids",)
    ACCOUNT_IDS_FIELD_NUMBER: _ClassVar[int]
    account_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, account_ids: _Iterable[int] | None = ...) -> None: ...

class CMsgPurchaseItemWithEventPoints(_message.Message):
    __slots__ = ("item_def", "quantity", "event_id", "use_premium_points")
    ITEM_DEF_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    USE_PREMIUM_POINTS_FIELD_NUMBER: _ClassVar[int]
    item_def: int
    quantity: int
    event_id: _dota_shared_enums_pb2.EEvent
    use_premium_points: bool
    def __init__(
        self,
        item_def: int | None = ...,
        quantity: int | None = ...,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
        use_premium_points: bool = ...,
    ) -> None: ...

class CMsgPurchaseItemWithEventPointsResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgPurchaseItemWithEventPointsResponse.Result]
        UNKNOWN_EVENT: _ClassVar[CMsgPurchaseItemWithEventPointsResponse.Result]
        UNKNOWN_ITEM: _ClassVar[CMsgPurchaseItemWithEventPointsResponse.Result]
        BAD_QUANTITY: _ClassVar[CMsgPurchaseItemWithEventPointsResponse.Result]
        NOT_PURCHASEABLE: _ClassVar[CMsgPurchaseItemWithEventPointsResponse.Result]
        SDO_LOAD_FAILED: _ClassVar[CMsgPurchaseItemWithEventPointsResponse.Result]
        NOT_ENOUGH_POINTS: _ClassVar[CMsgPurchaseItemWithEventPointsResponse.Result]
        SQL_ERROR: _ClassVar[CMsgPurchaseItemWithEventPointsResponse.Result]
        FAILED_TO_SEND: _ClassVar[CMsgPurchaseItemWithEventPointsResponse.Result]
        SERVER_ERROR: _ClassVar[CMsgPurchaseItemWithEventPointsResponse.Result]
        NOT_ALLOWED: _ClassVar[CMsgPurchaseItemWithEventPointsResponse.Result]
        CANCELLED: _ClassVar[CMsgPurchaseItemWithEventPointsResponse.Result]
        CLIENT_ERROR: _ClassVar[CMsgPurchaseItemWithEventPointsResponse.Result]
        SUBSCRIPTION_REQUIRED: _ClassVar[CMsgPurchaseItemWithEventPointsResponse.Result]

    SUCCESS: CMsgPurchaseItemWithEventPointsResponse.Result
    UNKNOWN_EVENT: CMsgPurchaseItemWithEventPointsResponse.Result
    UNKNOWN_ITEM: CMsgPurchaseItemWithEventPointsResponse.Result
    BAD_QUANTITY: CMsgPurchaseItemWithEventPointsResponse.Result
    NOT_PURCHASEABLE: CMsgPurchaseItemWithEventPointsResponse.Result
    SDO_LOAD_FAILED: CMsgPurchaseItemWithEventPointsResponse.Result
    NOT_ENOUGH_POINTS: CMsgPurchaseItemWithEventPointsResponse.Result
    SQL_ERROR: CMsgPurchaseItemWithEventPointsResponse.Result
    FAILED_TO_SEND: CMsgPurchaseItemWithEventPointsResponse.Result
    SERVER_ERROR: CMsgPurchaseItemWithEventPointsResponse.Result
    NOT_ALLOWED: CMsgPurchaseItemWithEventPointsResponse.Result
    CANCELLED: CMsgPurchaseItemWithEventPointsResponse.Result
    CLIENT_ERROR: CMsgPurchaseItemWithEventPointsResponse.Result
    SUBSCRIPTION_REQUIRED: CMsgPurchaseItemWithEventPointsResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgPurchaseItemWithEventPointsResponse.Result
    def __init__(
        self, result: CMsgPurchaseItemWithEventPointsResponse.Result | str | None = ...
    ) -> None: ...

class CMsgPurchaseHeroRandomRelic(_message.Message):
    __slots__ = ("hero_id", "relic_rarity")
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    RELIC_RARITY_FIELD_NUMBER: _ClassVar[int]
    hero_id: int
    relic_rarity: _dota_gcmessages_common_pb2.EHeroRelicRarity
    def __init__(
        self,
        hero_id: int | None = ...,
        relic_rarity: _dota_gcmessages_common_pb2.EHeroRelicRarity | str | None = ...,
    ) -> None: ...

class CMsgPurchaseHeroRandomRelicResponse(_message.Message):
    __slots__ = ("result", "kill_eater_type")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    KILL_EATER_TYPE_FIELD_NUMBER: _ClassVar[int]
    result: EPurchaseHeroRelicResult
    kill_eater_type: int
    def __init__(
        self, result: EPurchaseHeroRelicResult | str | None = ..., kill_eater_type: int | None = ...
    ) -> None: ...

class CMsgClientToGCRequestPlusWeeklyChallengeResult(_message.Message):
    __slots__ = ("event_id", "week")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    WEEK_FIELD_NUMBER: _ClassVar[int]
    event_id: _dota_shared_enums_pb2.EEvent
    week: int
    def __init__(
        self, event_id: _dota_shared_enums_pb2.EEvent | str | None = ..., week: int | None = ...
    ) -> None: ...

class CMsgClientToGCRequestPlusWeeklyChallengeResultResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgProfileRequest(_message.Message):
    __slots__ = ("account_id",)
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    def __init__(self, account_id: int | None = ...) -> None: ...

class CMsgProfileResponse(_message.Message):
    __slots__ = (
        "background_item",
        "featured_heroes",
        "recent_matches",
        "successful_heroes",
        "recent_match_details",
        "result",
        "stickerbook_page",
    )
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgProfileResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgProfileResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgProfileResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgProfileResponse.EResponse]

    k_eInternalError: CMsgProfileResponse.EResponse
    k_eSuccess: CMsgProfileResponse.EResponse
    k_eTooBusy: CMsgProfileResponse.EResponse
    k_eDisabled: CMsgProfileResponse.EResponse
    class FeaturedHero(_message.Message):
        __slots__ = (
            "hero_id",
            "equipped_econ_items",
            "manually_set",
            "plus_hero_xp",
            "plus_hero_relics_item",
        )
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        EQUIPPED_ECON_ITEMS_FIELD_NUMBER: _ClassVar[int]
        MANUALLY_SET_FIELD_NUMBER: _ClassVar[int]
        PLUS_HERO_XP_FIELD_NUMBER: _ClassVar[int]
        PLUS_HERO_RELICS_ITEM_FIELD_NUMBER: _ClassVar[int]
        hero_id: int
        equipped_econ_items: _containers.RepeatedCompositeFieldContainer[
            _base_gcmessages_pb2.CSOEconItem
        ]
        manually_set: bool
        plus_hero_xp: int
        plus_hero_relics_item: _base_gcmessages_pb2.CSOEconItem
        def __init__(
            self,
            hero_id: int | None = ...,
            equipped_econ_items: _Iterable[_base_gcmessages_pb2.CSOEconItem | _Mapping]
            | None = ...,
            manually_set: bool = ...,
            plus_hero_xp: int | None = ...,
            plus_hero_relics_item: _base_gcmessages_pb2.CSOEconItem | _Mapping | None = ...,
        ) -> None: ...

    class MatchInfo(_message.Message):
        __slots__ = ("match_id", "match_timestamp", "performance_rating", "hero_id", "won_match")
        MATCH_ID_FIELD_NUMBER: _ClassVar[int]
        MATCH_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        PERFORMANCE_RATING_FIELD_NUMBER: _ClassVar[int]
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        WON_MATCH_FIELD_NUMBER: _ClassVar[int]
        match_id: int
        match_timestamp: int
        performance_rating: int
        hero_id: int
        won_match: bool
        def __init__(
            self,
            match_id: int | None = ...,
            match_timestamp: int | None = ...,
            performance_rating: int | None = ...,
            hero_id: int | None = ...,
            won_match: bool = ...,
        ) -> None: ...

    BACKGROUND_ITEM_FIELD_NUMBER: _ClassVar[int]
    FEATURED_HEROES_FIELD_NUMBER: _ClassVar[int]
    RECENT_MATCHES_FIELD_NUMBER: _ClassVar[int]
    SUCCESSFUL_HEROES_FIELD_NUMBER: _ClassVar[int]
    RECENT_MATCH_DETAILS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    STICKERBOOK_PAGE_FIELD_NUMBER: _ClassVar[int]
    background_item: _base_gcmessages_pb2.CSOEconItem
    featured_heroes: _containers.RepeatedCompositeFieldContainer[CMsgProfileResponse.FeaturedHero]
    recent_matches: _containers.RepeatedCompositeFieldContainer[CMsgProfileResponse.MatchInfo]
    successful_heroes: _containers.RepeatedCompositeFieldContainer[
        _dota_gcmessages_common_pb2.CMsgSuccessfulHero
    ]
    recent_match_details: _dota_gcmessages_common_pb2.CMsgRecentMatchInfo
    result: CMsgProfileResponse.EResponse
    stickerbook_page: _dota_gcmessages_common_pb2.CMsgStickerbookPage
    def __init__(
        self,
        background_item: _base_gcmessages_pb2.CSOEconItem | _Mapping | None = ...,
        featured_heroes: _Iterable[CMsgProfileResponse.FeaturedHero | _Mapping] | None = ...,
        recent_matches: _Iterable[CMsgProfileResponse.MatchInfo | _Mapping] | None = ...,
        successful_heroes: _Iterable[_dota_gcmessages_common_pb2.CMsgSuccessfulHero | _Mapping]
        | None = ...,
        recent_match_details: _dota_gcmessages_common_pb2.CMsgRecentMatchInfo
        | _Mapping
        | None = ...,
        result: CMsgProfileResponse.EResponse | str | None = ...,
        stickerbook_page: _dota_gcmessages_common_pb2.CMsgStickerbookPage | _Mapping | None = ...,
    ) -> None: ...

class CMsgProfileUpdate(_message.Message):
    __slots__ = ("background_item_id", "featured_hero_ids")
    BACKGROUND_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURED_HERO_IDS_FIELD_NUMBER: _ClassVar[int]
    background_item_id: int
    featured_hero_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self, background_item_id: int | None = ..., featured_hero_ids: _Iterable[int] | None = ...
    ) -> None: ...

class CMsgProfileUpdateResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgProfileUpdateResponse.Result]
        FAILURE: _ClassVar[CMsgProfileUpdateResponse.Result]
        FAILURE_BAD_HERO1: _ClassVar[CMsgProfileUpdateResponse.Result]
        FAILURE_BAD_HERO2: _ClassVar[CMsgProfileUpdateResponse.Result]
        FAILURE_BAD_HERO3: _ClassVar[CMsgProfileUpdateResponse.Result]

    SUCCESS: CMsgProfileUpdateResponse.Result
    FAILURE: CMsgProfileUpdateResponse.Result
    FAILURE_BAD_HERO1: CMsgProfileUpdateResponse.Result
    FAILURE_BAD_HERO2: CMsgProfileUpdateResponse.Result
    FAILURE_BAD_HERO3: CMsgProfileUpdateResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgProfileUpdateResponse.Result
    def __init__(self, result: CMsgProfileUpdateResponse.Result | str | None = ...) -> None: ...

class CMsgTalentWinRates(_message.Message):
    __slots__ = ("last_run", "ability_id", "game_count", "win_count")
    LAST_RUN_FIELD_NUMBER: _ClassVar[int]
    ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    GAME_COUNT_FIELD_NUMBER: _ClassVar[int]
    WIN_COUNT_FIELD_NUMBER: _ClassVar[int]
    last_run: int
    ability_id: int
    game_count: int
    win_count: int
    def __init__(
        self,
        last_run: int | None = ...,
        ability_id: int | None = ...,
        game_count: int | None = ...,
        win_count: int | None = ...,
    ) -> None: ...

class CMsgGlobalHeroAverages(_message.Message):
    __slots__ = (
        "last_run",
        "avg_gold_per_min",
        "avg_xp_per_min",
        "avg_kills",
        "avg_deaths",
        "avg_assists",
        "avg_last_hits",
        "avg_denies",
        "avg_net_worth",
    )
    LAST_RUN_FIELD_NUMBER: _ClassVar[int]
    AVG_GOLD_PER_MIN_FIELD_NUMBER: _ClassVar[int]
    AVG_XP_PER_MIN_FIELD_NUMBER: _ClassVar[int]
    AVG_KILLS_FIELD_NUMBER: _ClassVar[int]
    AVG_DEATHS_FIELD_NUMBER: _ClassVar[int]
    AVG_ASSISTS_FIELD_NUMBER: _ClassVar[int]
    AVG_LAST_HITS_FIELD_NUMBER: _ClassVar[int]
    AVG_DENIES_FIELD_NUMBER: _ClassVar[int]
    AVG_NET_WORTH_FIELD_NUMBER: _ClassVar[int]
    last_run: int
    avg_gold_per_min: int
    avg_xp_per_min: int
    avg_kills: int
    avg_deaths: int
    avg_assists: int
    avg_last_hits: int
    avg_denies: int
    avg_net_worth: int
    def __init__(
        self,
        last_run: int | None = ...,
        avg_gold_per_min: int | None = ...,
        avg_xp_per_min: int | None = ...,
        avg_kills: int | None = ...,
        avg_deaths: int | None = ...,
        avg_assists: int | None = ...,
        avg_last_hits: int | None = ...,
        avg_denies: int | None = ...,
        avg_net_worth: int | None = ...,
    ) -> None: ...

class CMsgHeroGlobalDataRequest(_message.Message):
    __slots__ = ("hero_id",)
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    hero_id: int
    def __init__(self, hero_id: int | None = ...) -> None: ...

class CMsgHeroGlobalDataResponse(_message.Message):
    __slots__ = ("hero_id", "hero_data_per_chunk")
    class GraphData(_message.Message):
        __slots__ = ("day", "win_percent", "pick_percent", "ban_percent")
        DAY_FIELD_NUMBER: _ClassVar[int]
        WIN_PERCENT_FIELD_NUMBER: _ClassVar[int]
        PICK_PERCENT_FIELD_NUMBER: _ClassVar[int]
        BAN_PERCENT_FIELD_NUMBER: _ClassVar[int]
        day: int
        win_percent: float
        pick_percent: float
        ban_percent: float
        def __init__(
            self,
            day: int | None = ...,
            win_percent: float | None = ...,
            pick_percent: float | None = ...,
            ban_percent: float | None = ...,
        ) -> None: ...

    class WeekData(_message.Message):
        __slots__ = ("week", "win_percent", "pick_percent", "ban_percent")
        WEEK_FIELD_NUMBER: _ClassVar[int]
        WIN_PERCENT_FIELD_NUMBER: _ClassVar[int]
        PICK_PERCENT_FIELD_NUMBER: _ClassVar[int]
        BAN_PERCENT_FIELD_NUMBER: _ClassVar[int]
        week: int
        win_percent: float
        pick_percent: float
        ban_percent: float
        def __init__(
            self,
            week: int | None = ...,
            win_percent: float | None = ...,
            pick_percent: float | None = ...,
            ban_percent: float | None = ...,
        ) -> None: ...

    class HeroDataPerRankChunk(_message.Message):
        __slots__ = ("rank_chunk", "talent_win_rates", "hero_averages", "graph_data", "week_data")
        RANK_CHUNK_FIELD_NUMBER: _ClassVar[int]
        TALENT_WIN_RATES_FIELD_NUMBER: _ClassVar[int]
        HERO_AVERAGES_FIELD_NUMBER: _ClassVar[int]
        GRAPH_DATA_FIELD_NUMBER: _ClassVar[int]
        WEEK_DATA_FIELD_NUMBER: _ClassVar[int]
        rank_chunk: int
        talent_win_rates: _containers.RepeatedCompositeFieldContainer[CMsgTalentWinRates]
        hero_averages: CMsgGlobalHeroAverages
        graph_data: _containers.RepeatedCompositeFieldContainer[
            CMsgHeroGlobalDataResponse.GraphData
        ]
        week_data: _containers.RepeatedCompositeFieldContainer[CMsgHeroGlobalDataResponse.WeekData]
        def __init__(
            self,
            rank_chunk: int | None = ...,
            talent_win_rates: _Iterable[CMsgTalentWinRates | _Mapping] | None = ...,
            hero_averages: CMsgGlobalHeroAverages | _Mapping | None = ...,
            graph_data: _Iterable[CMsgHeroGlobalDataResponse.GraphData | _Mapping] | None = ...,
            week_data: _Iterable[CMsgHeroGlobalDataResponse.WeekData | _Mapping] | None = ...,
        ) -> None: ...

    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    HERO_DATA_PER_CHUNK_FIELD_NUMBER: _ClassVar[int]
    hero_id: int
    hero_data_per_chunk: _containers.RepeatedCompositeFieldContainer[
        CMsgHeroGlobalDataResponse.HeroDataPerRankChunk
    ]
    def __init__(
        self,
        hero_id: int | None = ...,
        hero_data_per_chunk: _Iterable[CMsgHeroGlobalDataResponse.HeroDataPerRankChunk | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgHeroGlobalDataAllHeroes(_message.Message):
    __slots__ = ("heroes",)
    HEROES_FIELD_NUMBER: _ClassVar[int]
    heroes: _containers.RepeatedCompositeFieldContainer[CMsgHeroGlobalDataResponse]
    def __init__(
        self, heroes: _Iterable[CMsgHeroGlobalDataResponse | _Mapping] | None = ...
    ) -> None: ...

class CMsgHeroGlobalDataHeroesAlliesAndEnemies(_message.Message):
    __slots__ = ("ranked_hero_data",)
    class HeroData(_message.Message):
        __slots__ = (
            "hero_id",
            "win_rate",
            "first_other_hero_id",
            "ally_win_rate",
            "enemy_win_rate",
        )
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        WIN_RATE_FIELD_NUMBER: _ClassVar[int]
        FIRST_OTHER_HERO_ID_FIELD_NUMBER: _ClassVar[int]
        ALLY_WIN_RATE_FIELD_NUMBER: _ClassVar[int]
        ENEMY_WIN_RATE_FIELD_NUMBER: _ClassVar[int]
        hero_id: int
        win_rate: int
        first_other_hero_id: int
        ally_win_rate: _containers.RepeatedScalarFieldContainer[int]
        enemy_win_rate: _containers.RepeatedScalarFieldContainer[int]
        def __init__(
            self,
            hero_id: int | None = ...,
            win_rate: int | None = ...,
            first_other_hero_id: int | None = ...,
            ally_win_rate: _Iterable[int] | None = ...,
            enemy_win_rate: _Iterable[int] | None = ...,
        ) -> None: ...

    class RankedHeroData(_message.Message):
        __slots__ = ("rank", "hero_data")
        RANK_FIELD_NUMBER: _ClassVar[int]
        HERO_DATA_FIELD_NUMBER: _ClassVar[int]
        rank: int
        hero_data: _containers.RepeatedCompositeFieldContainer[
            CMsgHeroGlobalDataHeroesAlliesAndEnemies.HeroData
        ]
        def __init__(
            self,
            rank: int | None = ...,
            hero_data: _Iterable[CMsgHeroGlobalDataHeroesAlliesAndEnemies.HeroData | _Mapping]
            | None = ...,
        ) -> None: ...

    RANKED_HERO_DATA_FIELD_NUMBER: _ClassVar[int]
    ranked_hero_data: _containers.RepeatedCompositeFieldContainer[
        CMsgHeroGlobalDataHeroesAlliesAndEnemies.RankedHeroData
    ]
    def __init__(
        self,
        ranked_hero_data: _Iterable[
            CMsgHeroGlobalDataHeroesAlliesAndEnemies.RankedHeroData | _Mapping
        ]
        | None = ...,
    ) -> None: ...

class CMsgPrivateMetadataKeyRequest(_message.Message):
    __slots__ = ("match_id",)
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    def __init__(self, match_id: int | None = ...) -> None: ...

class CMsgPrivateMetadataKeyResponse(_message.Message):
    __slots__ = ("private_key",)
    PRIVATE_KEY_FIELD_NUMBER: _ClassVar[int]
    private_key: int
    def __init__(self, private_key: int | None = ...) -> None: ...

class CMsgActivatePlusFreeTrialResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgActivatePlusFreeTrialResponse.Result]
        ERROR_GENERIC: _ClassVar[CMsgActivatePlusFreeTrialResponse.Result]
        ERROR_ALREADY_IN_FREE_TRIAL: _ClassVar[CMsgActivatePlusFreeTrialResponse.Result]
        ERROR_ALREADY_USED_FREE_TRIAL: _ClassVar[CMsgActivatePlusFreeTrialResponse.Result]
        ERROR_OFFER_NOT_VALID: _ClassVar[CMsgActivatePlusFreeTrialResponse.Result]

    SUCCESS: CMsgActivatePlusFreeTrialResponse.Result
    ERROR_GENERIC: CMsgActivatePlusFreeTrialResponse.Result
    ERROR_ALREADY_IN_FREE_TRIAL: CMsgActivatePlusFreeTrialResponse.Result
    ERROR_ALREADY_USED_FREE_TRIAL: CMsgActivatePlusFreeTrialResponse.Result
    ERROR_OFFER_NOT_VALID: CMsgActivatePlusFreeTrialResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgActivatePlusFreeTrialResponse.Result
    def __init__(
        self, result: CMsgActivatePlusFreeTrialResponse.Result | str | None = ...
    ) -> None: ...

class CMsgGCToClientCavernCrawlMapPathCompleted(_message.Message):
    __slots__ = ("event_id", "hero_id_completed", "completed_paths", "map_variant")
    class CompletedPathInfo(_message.Message):
        __slots__ = ("path_id_completed", "received_ultra_rare_reward", "half_completed")
        PATH_ID_COMPLETED_FIELD_NUMBER: _ClassVar[int]
        RECEIVED_ULTRA_RARE_REWARD_FIELD_NUMBER: _ClassVar[int]
        HALF_COMPLETED_FIELD_NUMBER: _ClassVar[int]
        path_id_completed: int
        received_ultra_rare_reward: bool
        half_completed: bool
        def __init__(
            self,
            path_id_completed: int | None = ...,
            received_ultra_rare_reward: bool = ...,
            half_completed: bool = ...,
        ) -> None: ...

    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_COMPLETED_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_PATHS_FIELD_NUMBER: _ClassVar[int]
    MAP_VARIANT_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    hero_id_completed: int
    completed_paths: _containers.RepeatedCompositeFieldContainer[
        CMsgGCToClientCavernCrawlMapPathCompleted.CompletedPathInfo
    ]
    map_variant: int
    def __init__(
        self,
        event_id: int | None = ...,
        hero_id_completed: int | None = ...,
        completed_paths: _Iterable[
            CMsgGCToClientCavernCrawlMapPathCompleted.CompletedPathInfo | _Mapping
        ]
        | None = ...,
        map_variant: int | None = ...,
    ) -> None: ...

class CMsgGCToClientCavernCrawlMapUpdated(_message.Message):
    __slots__ = ("event_id",)
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    def __init__(self, event_id: int | None = ...) -> None: ...

class CMsgClientToGCCavernCrawlClaimRoom(_message.Message):
    __slots__ = ("event_id", "room_id", "map_variant")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    MAP_VARIANT_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    room_id: int
    map_variant: int
    def __init__(
        self, event_id: int | None = ..., room_id: int | None = ..., map_variant: int | None = ...
    ) -> None: ...

class CMsgClientToGCCavernCrawlClaimRoomResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgClientToGCCavernCrawlClaimRoomResponse.Result]
        ERROR_UNKNOWN: _ClassVar[CMsgClientToGCCavernCrawlClaimRoomResponse.Result]
        RECEIVED_ULTRA_RARE_REWARD: _ClassVar[CMsgClientToGCCavernCrawlClaimRoomResponse.Result]

    SUCCESS: CMsgClientToGCCavernCrawlClaimRoomResponse.Result
    ERROR_UNKNOWN: CMsgClientToGCCavernCrawlClaimRoomResponse.Result
    RECEIVED_ULTRA_RARE_REWARD: CMsgClientToGCCavernCrawlClaimRoomResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCCavernCrawlClaimRoomResponse.Result
    def __init__(
        self, result: CMsgClientToGCCavernCrawlClaimRoomResponse.Result | str | None = ...
    ) -> None: ...

class CMsgClientToGCCavernCrawlUseItemOnRoom(_message.Message):
    __slots__ = ("event_id", "room_id", "item_type", "map_variant")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_TYPE_FIELD_NUMBER: _ClassVar[int]
    MAP_VARIANT_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    room_id: int
    item_type: int
    map_variant: int
    def __init__(
        self,
        event_id: int | None = ...,
        room_id: int | None = ...,
        item_type: int | None = ...,
        map_variant: int | None = ...,
    ) -> None: ...

class CMsgClientToGCCavernCrawlUseItemOnRoomResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgClientToGCCavernCrawlUseItemOnRoomResponse.Result]
        ERROR_UNKNOWN: _ClassVar[CMsgClientToGCCavernCrawlUseItemOnRoomResponse.Result]
        RECEIVED_ULTRA_RARE_REWARD: _ClassVar[CMsgClientToGCCavernCrawlUseItemOnRoomResponse.Result]

    SUCCESS: CMsgClientToGCCavernCrawlUseItemOnRoomResponse.Result
    ERROR_UNKNOWN: CMsgClientToGCCavernCrawlUseItemOnRoomResponse.Result
    RECEIVED_ULTRA_RARE_REWARD: CMsgClientToGCCavernCrawlUseItemOnRoomResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCCavernCrawlUseItemOnRoomResponse.Result
    def __init__(
        self, result: CMsgClientToGCCavernCrawlUseItemOnRoomResponse.Result | str | None = ...
    ) -> None: ...

class CMsgClientToGCCavernCrawlUseItemOnPath(_message.Message):
    __slots__ = ("event_id", "path_id", "item_type", "map_variant")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_TYPE_FIELD_NUMBER: _ClassVar[int]
    MAP_VARIANT_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    path_id: int
    item_type: int
    map_variant: int
    def __init__(
        self,
        event_id: int | None = ...,
        path_id: int | None = ...,
        item_type: int | None = ...,
        map_variant: int | None = ...,
    ) -> None: ...

class CMsgClientToGCCavernCrawlUseItemOnPathResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgClientToGCCavernCrawlUseItemOnPathResponse.Result]
        ERROR_UNKNOWN: _ClassVar[CMsgClientToGCCavernCrawlUseItemOnPathResponse.Result]
        RECEIVED_ULTRA_RARE_REWARD: _ClassVar[CMsgClientToGCCavernCrawlUseItemOnPathResponse.Result]

    SUCCESS: CMsgClientToGCCavernCrawlUseItemOnPathResponse.Result
    ERROR_UNKNOWN: CMsgClientToGCCavernCrawlUseItemOnPathResponse.Result
    RECEIVED_ULTRA_RARE_REWARD: CMsgClientToGCCavernCrawlUseItemOnPathResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCCavernCrawlUseItemOnPathResponse.Result
    def __init__(
        self, result: CMsgClientToGCCavernCrawlUseItemOnPathResponse.Result | str | None = ...
    ) -> None: ...

class CMsgClientToGCCavernCrawlRequestMapState(_message.Message):
    __slots__ = ("event_id",)
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    def __init__(self, event_id: int | None = ...) -> None: ...

class CMsgClientToGCCavernCrawlRequestMapStateResponse(_message.Message):
    __slots__ = ("result", "available_map_variants_mask", "inventory_item", "map_variants")
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgClientToGCCavernCrawlRequestMapStateResponse.Result]
        ERROR_UNKNOWN: _ClassVar[CMsgClientToGCCavernCrawlRequestMapStateResponse.Result]
        EVENT_NOT_OWNED: _ClassVar[CMsgClientToGCCavernCrawlRequestMapStateResponse.Result]

    SUCCESS: CMsgClientToGCCavernCrawlRequestMapStateResponse.Result
    ERROR_UNKNOWN: CMsgClientToGCCavernCrawlRequestMapStateResponse.Result
    EVENT_NOT_OWNED: CMsgClientToGCCavernCrawlRequestMapStateResponse.Result
    class SwappedChallenge(_message.Message):
        __slots__ = ("path_id_1", "path_id_2")
        PATH_ID_1_FIELD_NUMBER: _ClassVar[int]
        PATH_ID_2_FIELD_NUMBER: _ClassVar[int]
        path_id_1: int
        path_id_2: int
        def __init__(self, path_id_1: int | None = ..., path_id_2: int | None = ...) -> None: ...

    class InventoryItem(_message.Message):
        __slots__ = ("item_type", "count")
        ITEM_TYPE_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        item_type: int
        count: int
        def __init__(self, item_type: int | None = ..., count: int | None = ...) -> None: ...

    class TreasureMap(_message.Message):
        __slots__ = ("map_room_id", "revealed_room_id")
        MAP_ROOM_ID_FIELD_NUMBER: _ClassVar[int]
        REVEALED_ROOM_ID_FIELD_NUMBER: _ClassVar[int]
        map_room_id: int
        revealed_room_id: int
        def __init__(
            self, map_room_id: int | None = ..., revealed_room_id: int | None = ...
        ) -> None: ...

    class MapVariant(_message.Message):
        __slots__ = (
            "map_variant",
            "claimed_rooms_1",
            "claimed_rooms_2",
            "revealed_rooms_1",
            "revealed_rooms_2",
            "completed_paths_1",
            "completed_paths_2",
            "completed_paths_3",
            "completed_paths_4",
            "half_completed_paths_1",
            "half_completed_paths_2",
            "half_completed_paths_3",
            "half_completed_paths_4",
            "swapped_challenge",
            "ultra_rare_reward_room_number",
            "treasure_map",
        )
        MAP_VARIANT_FIELD_NUMBER: _ClassVar[int]
        CLAIMED_ROOMS_1_FIELD_NUMBER: _ClassVar[int]
        CLAIMED_ROOMS_2_FIELD_NUMBER: _ClassVar[int]
        REVEALED_ROOMS_1_FIELD_NUMBER: _ClassVar[int]
        REVEALED_ROOMS_2_FIELD_NUMBER: _ClassVar[int]
        COMPLETED_PATHS_1_FIELD_NUMBER: _ClassVar[int]
        COMPLETED_PATHS_2_FIELD_NUMBER: _ClassVar[int]
        COMPLETED_PATHS_3_FIELD_NUMBER: _ClassVar[int]
        COMPLETED_PATHS_4_FIELD_NUMBER: _ClassVar[int]
        HALF_COMPLETED_PATHS_1_FIELD_NUMBER: _ClassVar[int]
        HALF_COMPLETED_PATHS_2_FIELD_NUMBER: _ClassVar[int]
        HALF_COMPLETED_PATHS_3_FIELD_NUMBER: _ClassVar[int]
        HALF_COMPLETED_PATHS_4_FIELD_NUMBER: _ClassVar[int]
        SWAPPED_CHALLENGE_FIELD_NUMBER: _ClassVar[int]
        ULTRA_RARE_REWARD_ROOM_NUMBER_FIELD_NUMBER: _ClassVar[int]
        TREASURE_MAP_FIELD_NUMBER: _ClassVar[int]
        map_variant: int
        claimed_rooms_1: int
        claimed_rooms_2: int
        revealed_rooms_1: int
        revealed_rooms_2: int
        completed_paths_1: int
        completed_paths_2: int
        completed_paths_3: int
        completed_paths_4: int
        half_completed_paths_1: int
        half_completed_paths_2: int
        half_completed_paths_3: int
        half_completed_paths_4: int
        swapped_challenge: _containers.RepeatedCompositeFieldContainer[
            CMsgClientToGCCavernCrawlRequestMapStateResponse.SwappedChallenge
        ]
        ultra_rare_reward_room_number: int
        treasure_map: _containers.RepeatedCompositeFieldContainer[
            CMsgClientToGCCavernCrawlRequestMapStateResponse.TreasureMap
        ]
        def __init__(
            self,
            map_variant: int | None = ...,
            claimed_rooms_1: int | None = ...,
            claimed_rooms_2: int | None = ...,
            revealed_rooms_1: int | None = ...,
            revealed_rooms_2: int | None = ...,
            completed_paths_1: int | None = ...,
            completed_paths_2: int | None = ...,
            completed_paths_3: int | None = ...,
            completed_paths_4: int | None = ...,
            half_completed_paths_1: int | None = ...,
            half_completed_paths_2: int | None = ...,
            half_completed_paths_3: int | None = ...,
            half_completed_paths_4: int | None = ...,
            swapped_challenge: _Iterable[
                CMsgClientToGCCavernCrawlRequestMapStateResponse.SwappedChallenge | _Mapping
            ]
            | None = ...,
            ultra_rare_reward_room_number: int | None = ...,
            treasure_map: _Iterable[
                CMsgClientToGCCavernCrawlRequestMapStateResponse.TreasureMap | _Mapping
            ]
            | None = ...,
        ) -> None: ...

    RESULT_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_MAP_VARIANTS_MASK_FIELD_NUMBER: _ClassVar[int]
    INVENTORY_ITEM_FIELD_NUMBER: _ClassVar[int]
    MAP_VARIANTS_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCCavernCrawlRequestMapStateResponse.Result
    available_map_variants_mask: int
    inventory_item: _containers.RepeatedCompositeFieldContainer[
        CMsgClientToGCCavernCrawlRequestMapStateResponse.InventoryItem
    ]
    map_variants: _containers.RepeatedCompositeFieldContainer[
        CMsgClientToGCCavernCrawlRequestMapStateResponse.MapVariant
    ]
    def __init__(
        self,
        result: CMsgClientToGCCavernCrawlRequestMapStateResponse.Result | str | None = ...,
        available_map_variants_mask: int | None = ...,
        inventory_item: _Iterable[
            CMsgClientToGCCavernCrawlRequestMapStateResponse.InventoryItem | _Mapping
        ]
        | None = ...,
        map_variants: _Iterable[
            CMsgClientToGCCavernCrawlRequestMapStateResponse.MapVariant | _Mapping
        ]
        | None = ...,
    ) -> None: ...

class CMsgClientToGCCavernCrawlGetClaimedRoomCount(_message.Message):
    __slots__ = ("event_id",)
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    def __init__(self, event_id: int | None = ...) -> None: ...

class CMsgClientToGCCavernCrawlGetClaimedRoomCountResponse(_message.Message):
    __slots__ = ("result", "map_variants", "available_map_variants_mask")
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgClientToGCCavernCrawlGetClaimedRoomCountResponse.Result]
        ERROR_UNKNOWN: _ClassVar[CMsgClientToGCCavernCrawlGetClaimedRoomCountResponse.Result]
        EVENT_NOT_OWNED: _ClassVar[CMsgClientToGCCavernCrawlGetClaimedRoomCountResponse.Result]

    SUCCESS: CMsgClientToGCCavernCrawlGetClaimedRoomCountResponse.Result
    ERROR_UNKNOWN: CMsgClientToGCCavernCrawlGetClaimedRoomCountResponse.Result
    EVENT_NOT_OWNED: CMsgClientToGCCavernCrawlGetClaimedRoomCountResponse.Result
    class MapVariant(_message.Message):
        __slots__ = ("map_variant", "count")
        MAP_VARIANT_FIELD_NUMBER: _ClassVar[int]
        COUNT_FIELD_NUMBER: _ClassVar[int]
        map_variant: int
        count: int
        def __init__(self, map_variant: int | None = ..., count: int | None = ...) -> None: ...

    RESULT_FIELD_NUMBER: _ClassVar[int]
    MAP_VARIANTS_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_MAP_VARIANTS_MASK_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCCavernCrawlGetClaimedRoomCountResponse.Result
    map_variants: _containers.RepeatedCompositeFieldContainer[
        CMsgClientToGCCavernCrawlGetClaimedRoomCountResponse.MapVariant
    ]
    available_map_variants_mask: int
    def __init__(
        self,
        result: CMsgClientToGCCavernCrawlGetClaimedRoomCountResponse.Result | str | None = ...,
        map_variants: _Iterable[
            CMsgClientToGCCavernCrawlGetClaimedRoomCountResponse.MapVariant | _Mapping
        ]
        | None = ...,
        available_map_variants_mask: int | None = ...,
    ) -> None: ...

class CMsgDOTAMutationList(_message.Message):
    __slots__ = ("mutations",)
    class Mutation(_message.Message):
        __slots__ = ("id", "name", "description")
        ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        id: int
        name: str
        description: str
        def __init__(
            self, id: int | None = ..., name: str | None = ..., description: str | None = ...
        ) -> None: ...

    MUTATIONS_FIELD_NUMBER: _ClassVar[int]
    mutations: _containers.RepeatedCompositeFieldContainer[CMsgDOTAMutationList.Mutation]
    def __init__(
        self, mutations: _Iterable[CMsgDOTAMutationList.Mutation | _Mapping] | None = ...
    ) -> None: ...

class CMsgEventTipsSummaryRequest(_message.Message):
    __slots__ = ("event_id", "account_id")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: _dota_shared_enums_pb2.EEvent
    account_id: int
    def __init__(
        self,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
        account_id: int | None = ...,
    ) -> None: ...

class CMsgEventTipsSummaryResponse(_message.Message):
    __slots__ = ("result", "tips_received")
    class Tipper(_message.Message):
        __slots__ = ("tipper_account_id", "tip_count")
        TIPPER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        TIP_COUNT_FIELD_NUMBER: _ClassVar[int]
        tipper_account_id: int
        tip_count: int
        def __init__(
            self, tipper_account_id: int | None = ..., tip_count: int | None = ...
        ) -> None: ...

    RESULT_FIELD_NUMBER: _ClassVar[int]
    TIPS_RECEIVED_FIELD_NUMBER: _ClassVar[int]
    result: bool
    tips_received: _containers.RepeatedCompositeFieldContainer[CMsgEventTipsSummaryResponse.Tipper]
    def __init__(
        self,
        result: bool = ...,
        tips_received: _Iterable[CMsgEventTipsSummaryResponse.Tipper | _Mapping] | None = ...,
    ) -> None: ...

class CMsgSocialFeedRequest(_message.Message):
    __slots__ = ("account_id", "self_only")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SELF_ONLY_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    self_only: bool
    def __init__(self, account_id: int | None = ..., self_only: bool = ...) -> None: ...

class CMsgSocialFeedResponse(_message.Message):
    __slots__ = ("result", "feed_events")
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgSocialFeedResponse.Result]
        FAILED_TO_LOAD_FRIENDS: _ClassVar[CMsgSocialFeedResponse.Result]
        FAILED_TO_LOAD_FEED_DATA: _ClassVar[CMsgSocialFeedResponse.Result]
        FAILED_TO_LOAD_FEED_ENTRY: _ClassVar[CMsgSocialFeedResponse.Result]
        FAILED_TO_LOAD_COMMENTS: _ClassVar[CMsgSocialFeedResponse.Result]
        FAILED_TOO_MANY_REQUESTS: _ClassVar[CMsgSocialFeedResponse.Result]

    SUCCESS: CMsgSocialFeedResponse.Result
    FAILED_TO_LOAD_FRIENDS: CMsgSocialFeedResponse.Result
    FAILED_TO_LOAD_FEED_DATA: CMsgSocialFeedResponse.Result
    FAILED_TO_LOAD_FEED_ENTRY: CMsgSocialFeedResponse.Result
    FAILED_TO_LOAD_COMMENTS: CMsgSocialFeedResponse.Result
    FAILED_TOO_MANY_REQUESTS: CMsgSocialFeedResponse.Result
    class FeedEvent(_message.Message):
        __slots__ = (
            "feed_event_id",
            "account_id",
            "timestamp",
            "comment_count",
            "event_type",
            "event_sub_type",
            "param_big_int_1",
            "param_int_1",
            "param_int_2",
            "param_int_3",
            "param_string",
        )
        FEED_EVENT_ID_FIELD_NUMBER: _ClassVar[int]
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        COMMENT_COUNT_FIELD_NUMBER: _ClassVar[int]
        EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
        EVENT_SUB_TYPE_FIELD_NUMBER: _ClassVar[int]
        PARAM_BIG_INT_1_FIELD_NUMBER: _ClassVar[int]
        PARAM_INT_1_FIELD_NUMBER: _ClassVar[int]
        PARAM_INT_2_FIELD_NUMBER: _ClassVar[int]
        PARAM_INT_3_FIELD_NUMBER: _ClassVar[int]
        PARAM_STRING_FIELD_NUMBER: _ClassVar[int]
        feed_event_id: int
        account_id: int
        timestamp: int
        comment_count: int
        event_type: int
        event_sub_type: int
        param_big_int_1: int
        param_int_1: int
        param_int_2: int
        param_int_3: int
        param_string: str
        def __init__(
            self,
            feed_event_id: int | None = ...,
            account_id: int | None = ...,
            timestamp: int | None = ...,
            comment_count: int | None = ...,
            event_type: int | None = ...,
            event_sub_type: int | None = ...,
            param_big_int_1: int | None = ...,
            param_int_1: int | None = ...,
            param_int_2: int | None = ...,
            param_int_3: int | None = ...,
            param_string: str | None = ...,
        ) -> None: ...

    RESULT_FIELD_NUMBER: _ClassVar[int]
    FEED_EVENTS_FIELD_NUMBER: _ClassVar[int]
    result: CMsgSocialFeedResponse.Result
    feed_events: _containers.RepeatedCompositeFieldContainer[CMsgSocialFeedResponse.FeedEvent]
    def __init__(
        self,
        result: CMsgSocialFeedResponse.Result | str | None = ...,
        feed_events: _Iterable[CMsgSocialFeedResponse.FeedEvent | _Mapping] | None = ...,
    ) -> None: ...

class CMsgSocialFeedCommentsRequest(_message.Message):
    __slots__ = ("feed_event_id",)
    FEED_EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    feed_event_id: int
    def __init__(self, feed_event_id: int | None = ...) -> None: ...

class CMsgSocialFeedCommentsResponse(_message.Message):
    __slots__ = ("result", "feed_comments")
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgSocialFeedCommentsResponse.Result]
        FAILED_TOO_MANY_REQUESTS: _ClassVar[CMsgSocialFeedCommentsResponse.Result]
        FAILED_TO_LOAD_COMMENTS: _ClassVar[CMsgSocialFeedCommentsResponse.Result]

    SUCCESS: CMsgSocialFeedCommentsResponse.Result
    FAILED_TOO_MANY_REQUESTS: CMsgSocialFeedCommentsResponse.Result
    FAILED_TO_LOAD_COMMENTS: CMsgSocialFeedCommentsResponse.Result
    class FeedComment(_message.Message):
        __slots__ = ("commenter_account_id", "timestamp", "comment_text")
        COMMENTER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        COMMENT_TEXT_FIELD_NUMBER: _ClassVar[int]
        commenter_account_id: int
        timestamp: int
        comment_text: str
        def __init__(
            self,
            commenter_account_id: int | None = ...,
            timestamp: int | None = ...,
            comment_text: str | None = ...,
        ) -> None: ...

    RESULT_FIELD_NUMBER: _ClassVar[int]
    FEED_COMMENTS_FIELD_NUMBER: _ClassVar[int]
    result: CMsgSocialFeedCommentsResponse.Result
    feed_comments: _containers.RepeatedCompositeFieldContainer[
        CMsgSocialFeedCommentsResponse.FeedComment
    ]
    def __init__(
        self,
        result: CMsgSocialFeedCommentsResponse.Result | str | None = ...,
        feed_comments: _Iterable[CMsgSocialFeedCommentsResponse.FeedComment | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgClientToGCPlayerCardSpecificPurchaseRequest(_message.Message):
    __slots__ = ("player_account_id", "event_id", "card_dust_item_id")
    PLAYER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    CARD_DUST_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    player_account_id: int
    event_id: int
    card_dust_item_id: int
    def __init__(
        self,
        player_account_id: int | None = ...,
        event_id: int | None = ...,
        card_dust_item_id: int | None = ...,
    ) -> None: ...

class CMsgClientToGCPlayerCardSpecificPurchaseResponse(_message.Message):
    __slots__ = ("result", "item_id")
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgClientToGCPlayerCardSpecificPurchaseResponse.Result]
        ERROR_INTERNAL: _ClassVar[CMsgClientToGCPlayerCardSpecificPurchaseResponse.Result]
        ERROR_INSUFFICIENT_DUST: _ClassVar[CMsgClientToGCPlayerCardSpecificPurchaseResponse.Result]
        ERROR_ITEM_NOT_DUST_ITEM: _ClassVar[CMsgClientToGCPlayerCardSpecificPurchaseResponse.Result]
        ERROR_FAILED_CARD_PACK_CREATE: _ClassVar[
            CMsgClientToGCPlayerCardSpecificPurchaseResponse.Result
        ]
        ERROR_NOT_AVAILABLE: _ClassVar[CMsgClientToGCPlayerCardSpecificPurchaseResponse.Result]

    SUCCESS: CMsgClientToGCPlayerCardSpecificPurchaseResponse.Result
    ERROR_INTERNAL: CMsgClientToGCPlayerCardSpecificPurchaseResponse.Result
    ERROR_INSUFFICIENT_DUST: CMsgClientToGCPlayerCardSpecificPurchaseResponse.Result
    ERROR_ITEM_NOT_DUST_ITEM: CMsgClientToGCPlayerCardSpecificPurchaseResponse.Result
    ERROR_FAILED_CARD_PACK_CREATE: CMsgClientToGCPlayerCardSpecificPurchaseResponse.Result
    ERROR_NOT_AVAILABLE: CMsgClientToGCPlayerCardSpecificPurchaseResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCPlayerCardSpecificPurchaseResponse.Result
    item_id: int
    def __init__(
        self,
        result: CMsgClientToGCPlayerCardSpecificPurchaseResponse.Result | str | None = ...,
        item_id: int | None = ...,
    ) -> None: ...

class CMsgClientToGCRequestContestVotes(_message.Message):
    __slots__ = ("contest_id",)
    CONTEST_ID_FIELD_NUMBER: _ClassVar[int]
    contest_id: int
    def __init__(self, contest_id: int | None = ...) -> None: ...

class CMsgClientToGCRequestContestVotesResponse(_message.Message):
    __slots__ = ("result", "votes")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCRequestContestVotesResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCRequestContestVotesResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCRequestContestVotesResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCRequestContestVotesResponse.EResponse]

    k_eInternalError: CMsgClientToGCRequestContestVotesResponse.EResponse
    k_eSuccess: CMsgClientToGCRequestContestVotesResponse.EResponse
    k_eTooBusy: CMsgClientToGCRequestContestVotesResponse.EResponse
    k_eDisabled: CMsgClientToGCRequestContestVotesResponse.EResponse
    class ItemVote(_message.Message):
        __slots__ = ("contest_item_id", "vote")
        CONTEST_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
        VOTE_FIELD_NUMBER: _ClassVar[int]
        contest_item_id: int
        vote: int
        def __init__(self, contest_item_id: int | None = ..., vote: int | None = ...) -> None: ...

    RESULT_FIELD_NUMBER: _ClassVar[int]
    VOTES_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCRequestContestVotesResponse.EResponse
    votes: _containers.RepeatedCompositeFieldContainer[
        CMsgClientToGCRequestContestVotesResponse.ItemVote
    ]
    def __init__(
        self,
        result: CMsgClientToGCRequestContestVotesResponse.EResponse | str | None = ...,
        votes: _Iterable[CMsgClientToGCRequestContestVotesResponse.ItemVote | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgClientToGCRecordContestVote(_message.Message):
    __slots__ = ("contest_id", "contest_item_id", "vote")
    CONTEST_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEST_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    VOTE_FIELD_NUMBER: _ClassVar[int]
    contest_id: int
    contest_item_id: int
    vote: int
    def __init__(
        self,
        contest_id: int | None = ...,
        contest_item_id: int | None = ...,
        vote: int | None = ...,
    ) -> None: ...

class CMsgGCToClientRecordContestVoteResponse(_message.Message):
    __slots__ = ("eresult",)
    class EResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgGCToClientRecordContestVoteResponse.EResult]
        FAILED_EVENT_NOT_OWNED: _ClassVar[CMsgGCToClientRecordContestVoteResponse.EResult]
        FAILED_SQL_INSERT_FAILED: _ClassVar[CMsgGCToClientRecordContestVoteResponse.EResult]
        FAILED_INVALID_CONTEST: _ClassVar[CMsgGCToClientRecordContestVoteResponse.EResult]
        FAILED_CONTEST_NOT_ACTIVE: _ClassVar[CMsgGCToClientRecordContestVoteResponse.EResult]
        FAILED_TIMEOUT: _ClassVar[CMsgGCToClientRecordContestVoteResponse.EResult]

    SUCCESS: CMsgGCToClientRecordContestVoteResponse.EResult
    FAILED_EVENT_NOT_OWNED: CMsgGCToClientRecordContestVoteResponse.EResult
    FAILED_SQL_INSERT_FAILED: CMsgGCToClientRecordContestVoteResponse.EResult
    FAILED_INVALID_CONTEST: CMsgGCToClientRecordContestVoteResponse.EResult
    FAILED_CONTEST_NOT_ACTIVE: CMsgGCToClientRecordContestVoteResponse.EResult
    FAILED_TIMEOUT: CMsgGCToClientRecordContestVoteResponse.EResult
    ERESULT_FIELD_NUMBER: _ClassVar[int]
    eresult: CMsgGCToClientRecordContestVoteResponse.EResult
    def __init__(
        self, eresult: CMsgGCToClientRecordContestVoteResponse.EResult | str | None = ...
    ) -> None: ...

class CMsgDevGrantEventPoints(_message.Message):
    __slots__ = ("event_id", "event_points", "premium_points")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_POINTS_FIELD_NUMBER: _ClassVar[int]
    PREMIUM_POINTS_FIELD_NUMBER: _ClassVar[int]
    event_id: _dota_shared_enums_pb2.EEvent
    event_points: int
    premium_points: int
    def __init__(
        self,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
        event_points: int | None = ...,
        premium_points: int | None = ...,
    ) -> None: ...

class CMsgDevGrantEventPointsResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: EDevEventRequestResult
    def __init__(self, result: EDevEventRequestResult | str | None = ...) -> None: ...

class CMsgDevGrantEventAction(_message.Message):
    __slots__ = ("event_id", "action_id", "action_score")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_SCORE_FIELD_NUMBER: _ClassVar[int]
    event_id: _dota_shared_enums_pb2.EEvent
    action_id: int
    action_score: int
    def __init__(
        self,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
        action_id: int | None = ...,
        action_score: int | None = ...,
    ) -> None: ...

class CMsgDevGrantEventActionResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: EDevEventRequestResult
    def __init__(self, result: EDevEventRequestResult | str | None = ...) -> None: ...

class CMsgDevDeleteEventActions(_message.Message):
    __slots__ = ("event_id", "start_action_id", "end_action_id", "remove_audit")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    START_ACTION_ID_FIELD_NUMBER: _ClassVar[int]
    END_ACTION_ID_FIELD_NUMBER: _ClassVar[int]
    REMOVE_AUDIT_FIELD_NUMBER: _ClassVar[int]
    event_id: _dota_shared_enums_pb2.EEvent
    start_action_id: int
    end_action_id: int
    remove_audit: bool
    def __init__(
        self,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
        start_action_id: int | None = ...,
        end_action_id: int | None = ...,
        remove_audit: bool = ...,
    ) -> None: ...

class CMsgDevDeleteEventActionsResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: EDevEventRequestResult
    def __init__(self, result: EDevEventRequestResult | str | None = ...) -> None: ...

class CMsgDevResetEventState(_message.Message):
    __slots__ = ("event_id", "remove_audit")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    REMOVE_AUDIT_FIELD_NUMBER: _ClassVar[int]
    event_id: _dota_shared_enums_pb2.EEvent
    remove_audit: bool
    def __init__(
        self, event_id: _dota_shared_enums_pb2.EEvent | str | None = ..., remove_audit: bool = ...
    ) -> None: ...

class CMsgDevResetEventStateResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: EDevEventRequestResult
    def __init__(self, result: EDevEventRequestResult | str | None = ...) -> None: ...

class CMsgDevReloadAllEvents(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgDevReloadAllEventsResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: EDevEventRequestResult
    def __init__(self, result: EDevEventRequestResult | str | None = ...) -> None: ...

class CMsgConsumeEventSupportGrantItem(_message.Message):
    __slots__ = ("item_id",)
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    def __init__(self, item_id: int | None = ...) -> None: ...

class CMsgConsumeEventSupportGrantItemResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: ESupportEventRequestResult
    def __init__(self, result: ESupportEventRequestResult | str | None = ...) -> None: ...

class CMsgClientToGCGetFilteredPlayers(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgGCToClientGetFilteredPlayersResponse(_message.Message):
    __slots__ = ("result", "filtered_players", "base_slots", "additional_slots", "next_slot_cost")
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgGCToClientGetFilteredPlayersResponse.Result]
        FAILURE: _ClassVar[CMsgGCToClientGetFilteredPlayersResponse.Result]

    SUCCESS: CMsgGCToClientGetFilteredPlayersResponse.Result
    FAILURE: CMsgGCToClientGetFilteredPlayersResponse.Result
    class CFilterEntry(_message.Message):
        __slots__ = ("account_id", "time_added", "time_expires", "note")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        TIME_ADDED_FIELD_NUMBER: _ClassVar[int]
        TIME_EXPIRES_FIELD_NUMBER: _ClassVar[int]
        NOTE_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        time_added: int
        time_expires: int
        note: str
        def __init__(
            self,
            account_id: int | None = ...,
            time_added: int | None = ...,
            time_expires: int | None = ...,
            note: str | None = ...,
        ) -> None: ...

    RESULT_FIELD_NUMBER: _ClassVar[int]
    FILTERED_PLAYERS_FIELD_NUMBER: _ClassVar[int]
    BASE_SLOTS_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_SLOTS_FIELD_NUMBER: _ClassVar[int]
    NEXT_SLOT_COST_FIELD_NUMBER: _ClassVar[int]
    result: CMsgGCToClientGetFilteredPlayersResponse.Result
    filtered_players: _containers.RepeatedCompositeFieldContainer[
        CMsgGCToClientGetFilteredPlayersResponse.CFilterEntry
    ]
    base_slots: int
    additional_slots: int
    next_slot_cost: int
    def __init__(
        self,
        result: CMsgGCToClientGetFilteredPlayersResponse.Result | str | None = ...,
        filtered_players: _Iterable[
            CMsgGCToClientGetFilteredPlayersResponse.CFilterEntry | _Mapping
        ]
        | None = ...,
        base_slots: int | None = ...,
        additional_slots: int | None = ...,
        next_slot_cost: int | None = ...,
    ) -> None: ...

class CMsgClientToGCRemoveFilteredPlayer(_message.Message):
    __slots__ = ("account_id_to_remove",)
    ACCOUNT_ID_TO_REMOVE_FIELD_NUMBER: _ClassVar[int]
    account_id_to_remove: int
    def __init__(self, account_id_to_remove: int | None = ...) -> None: ...

class CMsgGCToClientRemoveFilteredPlayerResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgGCToClientRemoveFilteredPlayerResponse.Result]
        FAILURE: _ClassVar[CMsgGCToClientRemoveFilteredPlayerResponse.Result]

    SUCCESS: CMsgGCToClientRemoveFilteredPlayerResponse.Result
    FAILURE: CMsgGCToClientRemoveFilteredPlayerResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgGCToClientRemoveFilteredPlayerResponse.Result
    def __init__(
        self, result: CMsgGCToClientRemoveFilteredPlayerResponse.Result | str | None = ...
    ) -> None: ...

class CMsgClientToGCPurchaseFilteredPlayerSlot(_message.Message):
    __slots__ = ("additional_slots_current",)
    ADDITIONAL_SLOTS_CURRENT_FIELD_NUMBER: _ClassVar[int]
    additional_slots_current: int
    def __init__(self, additional_slots_current: int | None = ...) -> None: ...

class CMsgGCToClientPurchaseFilteredPlayerSlotResponse(_message.Message):
    __slots__ = ("result", "additional_slots", "next_slot_cost")
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgGCToClientPurchaseFilteredPlayerSlotResponse.Result]
        FAILURE: _ClassVar[CMsgGCToClientPurchaseFilteredPlayerSlotResponse.Result]
        CURRENT_SLOTCOUNT_DOESNT_MATCH: _ClassVar[
            CMsgGCToClientPurchaseFilteredPlayerSlotResponse.Result
        ]
        CANT_AFFORD: _ClassVar[CMsgGCToClientPurchaseFilteredPlayerSlotResponse.Result]

    SUCCESS: CMsgGCToClientPurchaseFilteredPlayerSlotResponse.Result
    FAILURE: CMsgGCToClientPurchaseFilteredPlayerSlotResponse.Result
    CURRENT_SLOTCOUNT_DOESNT_MATCH: CMsgGCToClientPurchaseFilteredPlayerSlotResponse.Result
    CANT_AFFORD: CMsgGCToClientPurchaseFilteredPlayerSlotResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_SLOTS_FIELD_NUMBER: _ClassVar[int]
    NEXT_SLOT_COST_FIELD_NUMBER: _ClassVar[int]
    result: CMsgGCToClientPurchaseFilteredPlayerSlotResponse.Result
    additional_slots: int
    next_slot_cost: int
    def __init__(
        self,
        result: CMsgGCToClientPurchaseFilteredPlayerSlotResponse.Result | str | None = ...,
        additional_slots: int | None = ...,
        next_slot_cost: int | None = ...,
    ) -> None: ...

class CMsgClientToGCUpdateFilteredPlayerNote(_message.Message):
    __slots__ = ("target_account_id", "new_note")
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_NOTE_FIELD_NUMBER: _ClassVar[int]
    target_account_id: int
    new_note: str
    def __init__(self, target_account_id: int | None = ..., new_note: str | None = ...) -> None: ...

class CMsgGCToClientUpdateFilteredPlayerNoteResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgGCToClientUpdateFilteredPlayerNoteResponse.Result]
        FAILURE: _ClassVar[CMsgGCToClientUpdateFilteredPlayerNoteResponse.Result]
        NOT_FOUND: _ClassVar[CMsgGCToClientUpdateFilteredPlayerNoteResponse.Result]

    SUCCESS: CMsgGCToClientUpdateFilteredPlayerNoteResponse.Result
    FAILURE: CMsgGCToClientUpdateFilteredPlayerNoteResponse.Result
    NOT_FOUND: CMsgGCToClientUpdateFilteredPlayerNoteResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgGCToClientUpdateFilteredPlayerNoteResponse.Result
    def __init__(
        self, result: CMsgGCToClientUpdateFilteredPlayerNoteResponse.Result | str | None = ...
    ) -> None: ...

class CMsgPartySearchPlayer(_message.Message):
    __slots__ = ("account_id", "match_id", "creation_time")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    CREATION_TIME_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    match_id: int
    creation_time: int
    def __init__(
        self,
        account_id: int | None = ...,
        match_id: int | None = ...,
        creation_time: int | None = ...,
    ) -> None: ...

class CMsgGCToClientPlayerBeaconState(_message.Message):
    __slots__ = ("num_active_beacons",)
    NUM_ACTIVE_BEACONS_FIELD_NUMBER: _ClassVar[int]
    num_active_beacons: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, num_active_beacons: _Iterable[int] | None = ...) -> None: ...

class CMsgGCToClientPartyBeaconUpdate(_message.Message):
    __slots__ = ("beacon_added", "beacon_type", "account_id")
    BEACON_ADDED_FIELD_NUMBER: _ClassVar[int]
    BEACON_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    beacon_added: bool
    beacon_type: int
    account_id: int
    def __init__(
        self, beacon_added: bool = ..., beacon_type: int | None = ..., account_id: int | None = ...
    ) -> None: ...

class CMsgClientToGCUpdatePartyBeacon(_message.Message):
    __slots__ = ("action",)
    class Action(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ON: _ClassVar[CMsgClientToGCUpdatePartyBeacon.Action]
        OFF: _ClassVar[CMsgClientToGCUpdatePartyBeacon.Action]

    ON: CMsgClientToGCUpdatePartyBeacon.Action
    OFF: CMsgClientToGCUpdatePartyBeacon.Action
    ACTION_FIELD_NUMBER: _ClassVar[int]
    action: CMsgClientToGCUpdatePartyBeacon.Action
    def __init__(
        self, action: CMsgClientToGCUpdatePartyBeacon.Action | str | None = ...
    ) -> None: ...

class CMsgClientToGCRequestActiveBeaconParties(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgGCToClientRequestActiveBeaconPartiesResponse(_message.Message):
    __slots__ = ("response", "active_parties")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgGCToClientRequestActiveBeaconPartiesResponse.EResponse]
        FAILURE: _ClassVar[CMsgGCToClientRequestActiveBeaconPartiesResponse.EResponse]
        BUSY: _ClassVar[CMsgGCToClientRequestActiveBeaconPartiesResponse.EResponse]

    SUCCESS: CMsgGCToClientRequestActiveBeaconPartiesResponse.EResponse
    FAILURE: CMsgGCToClientRequestActiveBeaconPartiesResponse.EResponse
    BUSY: CMsgGCToClientRequestActiveBeaconPartiesResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_PARTIES_FIELD_NUMBER: _ClassVar[int]
    response: CMsgGCToClientRequestActiveBeaconPartiesResponse.EResponse
    active_parties: _containers.RepeatedCompositeFieldContainer[
        _dota_gcmessages_common_pb2.CPartySearchClientParty
    ]
    def __init__(
        self,
        response: CMsgGCToClientRequestActiveBeaconPartiesResponse.EResponse | str | None = ...,
        active_parties: _Iterable[_dota_gcmessages_common_pb2.CPartySearchClientParty | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgClientToGCJoinPartyFromBeacon(_message.Message):
    __slots__ = ("party_id", "account_id", "beacon_type")
    PARTY_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    BEACON_TYPE_FIELD_NUMBER: _ClassVar[int]
    party_id: int
    account_id: int
    beacon_type: int
    def __init__(
        self,
        party_id: int | None = ...,
        account_id: int | None = ...,
        beacon_type: int | None = ...,
    ) -> None: ...

class CMsgGCToClientJoinPartyFromBeaconResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgGCToClientJoinPartyFromBeaconResponse.EResponse]
        FAILURE: _ClassVar[CMsgGCToClientJoinPartyFromBeaconResponse.EResponse]
        BUSY: _ClassVar[CMsgGCToClientJoinPartyFromBeaconResponse.EResponse]
        NOT_LEADER: _ClassVar[CMsgGCToClientJoinPartyFromBeaconResponse.EResponse]

    SUCCESS: CMsgGCToClientJoinPartyFromBeaconResponse.EResponse
    FAILURE: CMsgGCToClientJoinPartyFromBeaconResponse.EResponse
    BUSY: CMsgGCToClientJoinPartyFromBeaconResponse.EResponse
    NOT_LEADER: CMsgGCToClientJoinPartyFromBeaconResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgGCToClientJoinPartyFromBeaconResponse.EResponse
    def __init__(
        self, response: CMsgGCToClientJoinPartyFromBeaconResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCManageFavorites(_message.Message):
    __slots__ = (
        "action",
        "account_id",
        "favorite_name",
        "invite_response",
        "from_friendlist",
        "lobby_id",
    )
    class Action(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ADD: _ClassVar[CMsgClientToGCManageFavorites.Action]
        REMOVE: _ClassVar[CMsgClientToGCManageFavorites.Action]

    ADD: CMsgClientToGCManageFavorites.Action
    REMOVE: CMsgClientToGCManageFavorites.Action
    ACTION_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    FAVORITE_NAME_FIELD_NUMBER: _ClassVar[int]
    INVITE_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    FROM_FRIENDLIST_FIELD_NUMBER: _ClassVar[int]
    LOBBY_ID_FIELD_NUMBER: _ClassVar[int]
    action: CMsgClientToGCManageFavorites.Action
    account_id: int
    favorite_name: str
    invite_response: bool
    from_friendlist: bool
    lobby_id: int
    def __init__(
        self,
        action: CMsgClientToGCManageFavorites.Action | str | None = ...,
        account_id: int | None = ...,
        favorite_name: str | None = ...,
        invite_response: bool = ...,
        from_friendlist: bool = ...,
        lobby_id: int | None = ...,
    ) -> None: ...

class CMsgGCToClientManageFavoritesResponse(_message.Message):
    __slots__ = ("response", "debug_message", "player")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgGCToClientManageFavoritesResponse.EResponse]
        FAILURE: _ClassVar[CMsgGCToClientManageFavoritesResponse.EResponse]
        NO_INVITE_PRESENT: _ClassVar[CMsgGCToClientManageFavoritesResponse.EResponse]
        INVITE_SENT: _ClassVar[CMsgGCToClientManageFavoritesResponse.EResponse]
        EXPIRED: _ClassVar[CMsgGCToClientManageFavoritesResponse.EResponse]
        BUSY: _ClassVar[CMsgGCToClientManageFavoritesResponse.EResponse]

    SUCCESS: CMsgGCToClientManageFavoritesResponse.EResponse
    FAILURE: CMsgGCToClientManageFavoritesResponse.EResponse
    NO_INVITE_PRESENT: CMsgGCToClientManageFavoritesResponse.EResponse
    INVITE_SENT: CMsgGCToClientManageFavoritesResponse.EResponse
    EXPIRED: CMsgGCToClientManageFavoritesResponse.EResponse
    BUSY: CMsgGCToClientManageFavoritesResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    DEBUG_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    PLAYER_FIELD_NUMBER: _ClassVar[int]
    response: CMsgGCToClientManageFavoritesResponse.EResponse
    debug_message: str
    player: CMsgPartySearchPlayer
    def __init__(
        self,
        response: CMsgGCToClientManageFavoritesResponse.EResponse | str | None = ...,
        debug_message: str | None = ...,
        player: CMsgPartySearchPlayer | _Mapping | None = ...,
    ) -> None: ...

class CMsgClientToGCGetFavoritePlayers(_message.Message):
    __slots__ = ("pagination_key", "pagination_count")
    PAGINATION_KEY_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_COUNT_FIELD_NUMBER: _ClassVar[int]
    pagination_key: int
    pagination_count: int
    def __init__(
        self, pagination_key: int | None = ..., pagination_count: int | None = ...
    ) -> None: ...

class CMsgGCToClientGetFavoritePlayersResponse(_message.Message):
    __slots__ = ("response", "players", "next_pagination_key")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgGCToClientGetFavoritePlayersResponse.EResponse]
        FAILURE: _ClassVar[CMsgGCToClientGetFavoritePlayersResponse.EResponse]

    SUCCESS: CMsgGCToClientGetFavoritePlayersResponse.EResponse
    FAILURE: CMsgGCToClientGetFavoritePlayersResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGINATION_KEY_FIELD_NUMBER: _ClassVar[int]
    response: CMsgGCToClientGetFavoritePlayersResponse.EResponse
    players: _containers.RepeatedCompositeFieldContainer[CMsgPartySearchPlayer]
    next_pagination_key: int
    def __init__(
        self,
        response: CMsgGCToClientGetFavoritePlayersResponse.EResponse | str | None = ...,
        players: _Iterable[CMsgPartySearchPlayer | _Mapping] | None = ...,
        next_pagination_key: int | None = ...,
    ) -> None: ...

class CMsgGCToClientPartySearchInvite(_message.Message):
    __slots__ = ("account_id",)
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    def __init__(self, account_id: int | None = ...) -> None: ...

class CMsgClientToGCVerifyFavoritePlayers(_message.Message):
    __slots__ = ("account_ids",)
    ACCOUNT_IDS_FIELD_NUMBER: _ClassVar[int]
    account_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, account_ids: _Iterable[int] | None = ...) -> None: ...

class CMsgGCToClientVerifyFavoritePlayersResponse(_message.Message):
    __slots__ = ("results",)
    class Result(_message.Message):
        __slots__ = ("player", "is_favorite")
        PLAYER_FIELD_NUMBER: _ClassVar[int]
        IS_FAVORITE_FIELD_NUMBER: _ClassVar[int]
        player: CMsgPartySearchPlayer
        is_favorite: bool
        def __init__(
            self, player: CMsgPartySearchPlayer | _Mapping | None = ..., is_favorite: bool = ...
        ) -> None: ...

    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[
        CMsgGCToClientVerifyFavoritePlayersResponse.Result
    ]
    def __init__(
        self,
        results: _Iterable[CMsgGCToClientVerifyFavoritePlayersResponse.Result | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgClientToGCRequestPlayerRecentAccomplishments(_message.Message):
    __slots__ = ("account_id",)
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    def __init__(self, account_id: int | None = ...) -> None: ...

class CMsgClientToGCRequestPlayerRecentAccomplishmentsResponse(_message.Message):
    __slots__ = ("result", "player_accomplishments")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[
            CMsgClientToGCRequestPlayerRecentAccomplishmentsResponse.EResponse
        ]
        k_eSuccess: _ClassVar[CMsgClientToGCRequestPlayerRecentAccomplishmentsResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCRequestPlayerRecentAccomplishmentsResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCRequestPlayerRecentAccomplishmentsResponse.EResponse]

    k_eInternalError: CMsgClientToGCRequestPlayerRecentAccomplishmentsResponse.EResponse
    k_eSuccess: CMsgClientToGCRequestPlayerRecentAccomplishmentsResponse.EResponse
    k_eTooBusy: CMsgClientToGCRequestPlayerRecentAccomplishmentsResponse.EResponse
    k_eDisabled: CMsgClientToGCRequestPlayerRecentAccomplishmentsResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    PLAYER_ACCOMPLISHMENTS_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCRequestPlayerRecentAccomplishmentsResponse.EResponse
    player_accomplishments: _dota_gcmessages_common_pb2.CMsgPlayerRecentAccomplishments
    def __init__(
        self,
        result: CMsgClientToGCRequestPlayerRecentAccomplishmentsResponse.EResponse
        | str
        | None = ...,
        player_accomplishments: _dota_gcmessages_common_pb2.CMsgPlayerRecentAccomplishments
        | _Mapping
        | None = ...,
    ) -> None: ...

class CMsgClientToGCRequestPlayerHeroRecentAccomplishments(_message.Message):
    __slots__ = ("account_id", "hero_id")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    hero_id: int
    def __init__(self, account_id: int | None = ..., hero_id: int | None = ...) -> None: ...

class CMsgClientToGCRequestPlayerHeroRecentAccomplishmentsResponse(_message.Message):
    __slots__ = ("result", "hero_accomplishments")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[
            CMsgClientToGCRequestPlayerHeroRecentAccomplishmentsResponse.EResponse
        ]
        k_eSuccess: _ClassVar[
            CMsgClientToGCRequestPlayerHeroRecentAccomplishmentsResponse.EResponse
        ]
        k_eTooBusy: _ClassVar[
            CMsgClientToGCRequestPlayerHeroRecentAccomplishmentsResponse.EResponse
        ]
        k_eDisabled: _ClassVar[
            CMsgClientToGCRequestPlayerHeroRecentAccomplishmentsResponse.EResponse
        ]

    k_eInternalError: CMsgClientToGCRequestPlayerHeroRecentAccomplishmentsResponse.EResponse
    k_eSuccess: CMsgClientToGCRequestPlayerHeroRecentAccomplishmentsResponse.EResponse
    k_eTooBusy: CMsgClientToGCRequestPlayerHeroRecentAccomplishmentsResponse.EResponse
    k_eDisabled: CMsgClientToGCRequestPlayerHeroRecentAccomplishmentsResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    HERO_ACCOMPLISHMENTS_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCRequestPlayerHeroRecentAccomplishmentsResponse.EResponse
    hero_accomplishments: _dota_gcmessages_common_pb2.CMsgPlayerHeroRecentAccomplishments
    def __init__(
        self,
        result: CMsgClientToGCRequestPlayerHeroRecentAccomplishmentsResponse.EResponse
        | str
        | None = ...,
        hero_accomplishments: _dota_gcmessages_common_pb2.CMsgPlayerHeroRecentAccomplishments
        | _Mapping
        | None = ...,
    ) -> None: ...

class CMsgClientToGCSubmitPlayerMatchSurvey(_message.Message):
    __slots__ = ("match_id", "rating", "flags")
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    rating: int
    flags: int
    def __init__(
        self, match_id: int | None = ..., rating: int | None = ..., flags: int | None = ...
    ) -> None: ...

class CMsgClientToGCSubmitPlayerMatchSurveyResponse(_message.Message):
    __slots__ = ("eresult", "account_id")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCSubmitPlayerMatchSurveyResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCSubmitPlayerMatchSurveyResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCSubmitPlayerMatchSurveyResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCSubmitPlayerMatchSurveyResponse.EResponse]
        k_eAlreadySubmitted: _ClassVar[CMsgClientToGCSubmitPlayerMatchSurveyResponse.EResponse]
        k_ePlayerNotValid: _ClassVar[CMsgClientToGCSubmitPlayerMatchSurveyResponse.EResponse]

    k_eInternalError: CMsgClientToGCSubmitPlayerMatchSurveyResponse.EResponse
    k_eSuccess: CMsgClientToGCSubmitPlayerMatchSurveyResponse.EResponse
    k_eTooBusy: CMsgClientToGCSubmitPlayerMatchSurveyResponse.EResponse
    k_eDisabled: CMsgClientToGCSubmitPlayerMatchSurveyResponse.EResponse
    k_eAlreadySubmitted: CMsgClientToGCSubmitPlayerMatchSurveyResponse.EResponse
    k_ePlayerNotValid: CMsgClientToGCSubmitPlayerMatchSurveyResponse.EResponse
    ERESULT_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    eresult: CMsgClientToGCSubmitPlayerMatchSurveyResponse.EResponse
    account_id: int
    def __init__(
        self,
        eresult: CMsgClientToGCSubmitPlayerMatchSurveyResponse.EResponse | str | None = ...,
        account_id: int | None = ...,
    ) -> None: ...

class CMsgGCToClientVACReminder(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCUnderDraftRequest(_message.Message):
    __slots__ = ("account_id", "event_id")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    event_id: int
    def __init__(self, account_id: int | None = ..., event_id: int | None = ...) -> None: ...

class CMsgClientToGCUnderDraftResponse(_message.Message):
    __slots__ = ("result", "account_id", "event_id", "draft_data")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    DRAFT_DATA_FIELD_NUMBER: _ClassVar[int]
    result: EUnderDraftResponse
    account_id: int
    event_id: int
    draft_data: _dota_gcmessages_common_pb2.CMsgUnderDraftData
    def __init__(
        self,
        result: EUnderDraftResponse | str | None = ...,
        account_id: int | None = ...,
        event_id: int | None = ...,
        draft_data: _dota_gcmessages_common_pb2.CMsgUnderDraftData | _Mapping | None = ...,
    ) -> None: ...

class CMsgClientToGCUnderDraftReroll(_message.Message):
    __slots__ = ("event_id",)
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    def __init__(self, event_id: int | None = ...) -> None: ...

class CMsgClientToGCUnderDraftRerollResponse(_message.Message):
    __slots__ = ("result", "event_id", "draft_data")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    DRAFT_DATA_FIELD_NUMBER: _ClassVar[int]
    result: EUnderDraftResponse
    event_id: int
    draft_data: _dota_gcmessages_common_pb2.CMsgUnderDraftData
    def __init__(
        self,
        result: EUnderDraftResponse | str | None = ...,
        event_id: int | None = ...,
        draft_data: _dota_gcmessages_common_pb2.CMsgUnderDraftData | _Mapping | None = ...,
    ) -> None: ...

class CMsgClientToGCUnderDraftBuy(_message.Message):
    __slots__ = ("event_id", "slot_id")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    SLOT_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    slot_id: int
    def __init__(self, event_id: int | None = ..., slot_id: int | None = ...) -> None: ...

class CMsgGCToClientGuildUnderDraftGoldUpdated(_message.Message):
    __slots__ = ("event_id",)
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    def __init__(self, event_id: int | None = ...) -> None: ...

class CMsgClientToGCUnderDraftBuyResponse(_message.Message):
    __slots__ = ("result", "event_id", "slot_id", "draft_data")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    SLOT_ID_FIELD_NUMBER: _ClassVar[int]
    DRAFT_DATA_FIELD_NUMBER: _ClassVar[int]
    result: EUnderDraftResponse
    event_id: int
    slot_id: int
    draft_data: _dota_gcmessages_common_pb2.CMsgUnderDraftData
    def __init__(
        self,
        result: EUnderDraftResponse | str | None = ...,
        event_id: int | None = ...,
        slot_id: int | None = ...,
        draft_data: _dota_gcmessages_common_pb2.CMsgUnderDraftData | _Mapping | None = ...,
    ) -> None: ...

class CMsgClientToGCUnderDraftRollBackBench(_message.Message):
    __slots__ = ("event_id",)
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    def __init__(self, event_id: int | None = ...) -> None: ...

class CMsgClientToGCUnderDraftRollBackBenchResponse(_message.Message):
    __slots__ = ("result", "event_id", "draft_data")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    DRAFT_DATA_FIELD_NUMBER: _ClassVar[int]
    result: EUnderDraftResponse
    event_id: int
    draft_data: _dota_gcmessages_common_pb2.CMsgUnderDraftData
    def __init__(
        self,
        result: EUnderDraftResponse | str | None = ...,
        event_id: int | None = ...,
        draft_data: _dota_gcmessages_common_pb2.CMsgUnderDraftData | _Mapping | None = ...,
    ) -> None: ...

class CMsgClientToGCUnderDraftSell(_message.Message):
    __slots__ = ("event_id", "slot_id")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    SLOT_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    slot_id: int
    def __init__(self, event_id: int | None = ..., slot_id: int | None = ...) -> None: ...

class CMsgClientToGCUnderDraftSellResponse(_message.Message):
    __slots__ = ("result", "event_id", "slot_id", "draft_data")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    SLOT_ID_FIELD_NUMBER: _ClassVar[int]
    DRAFT_DATA_FIELD_NUMBER: _ClassVar[int]
    result: EUnderDraftResponse
    event_id: int
    slot_id: int
    draft_data: _dota_gcmessages_common_pb2.CMsgUnderDraftData
    def __init__(
        self,
        result: EUnderDraftResponse | str | None = ...,
        event_id: int | None = ...,
        slot_id: int | None = ...,
        draft_data: _dota_gcmessages_common_pb2.CMsgUnderDraftData | _Mapping | None = ...,
    ) -> None: ...

class CMsgClientToGCUnderDraftRedeemReward(_message.Message):
    __slots__ = ("event_id", "action_id")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    action_id: int
    def __init__(self, event_id: int | None = ..., action_id: int | None = ...) -> None: ...

class CMsgClientToGCUnderDraftRedeemRewardResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: EUnderDraftResponse
    def __init__(self, result: EUnderDraftResponse | str | None = ...) -> None: ...

class CMsgClientToGCSubmitDraftTriviaMatchAnswer(_message.Message):
    __slots__ = ("chose_radiant_as_winner", "event_id", "end_time")
    CHOSE_RADIANT_AS_WINNER_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    chose_radiant_as_winner: bool
    event_id: int
    end_time: int
    def __init__(
        self,
        chose_radiant_as_winner: bool = ...,
        event_id: int | None = ...,
        end_time: int | None = ...,
    ) -> None: ...

class CMsgClientToGCSubmitDraftTriviaMatchAnswerResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: EDOTADraftTriviaAnswerResult
    def __init__(self, result: EDOTADraftTriviaAnswerResult | str | None = ...) -> None: ...

class CMsgDraftTriviaVoteCount(_message.Message):
    __slots__ = ("total_votes", "radiant_votes", "dire_votes")
    TOTAL_VOTES_FIELD_NUMBER: _ClassVar[int]
    RADIANT_VOTES_FIELD_NUMBER: _ClassVar[int]
    DIRE_VOTES_FIELD_NUMBER: _ClassVar[int]
    total_votes: int
    radiant_votes: int
    dire_votes: int
    def __init__(
        self,
        total_votes: int | None = ...,
        radiant_votes: int | None = ...,
        dire_votes: int | None = ...,
    ) -> None: ...

class CMsgClientToGCRequestReporterUpdates(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCRequestReporterUpdatesResponse(_message.Message):
    __slots__ = ("enum_result", "updates", "num_reported", "num_no_action_taken")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCRequestReporterUpdatesResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCRequestReporterUpdatesResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCRequestReporterUpdatesResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCRequestReporterUpdatesResponse.EResponse]
        k_eNotPermitted: _ClassVar[CMsgClientToGCRequestReporterUpdatesResponse.EResponse]
        k_eNotToSoon: _ClassVar[CMsgClientToGCRequestReporterUpdatesResponse.EResponse]
        k_eNotValid: _ClassVar[CMsgClientToGCRequestReporterUpdatesResponse.EResponse]

    k_eInternalError: CMsgClientToGCRequestReporterUpdatesResponse.EResponse
    k_eSuccess: CMsgClientToGCRequestReporterUpdatesResponse.EResponse
    k_eTimeout: CMsgClientToGCRequestReporterUpdatesResponse.EResponse
    k_eTooBusy: CMsgClientToGCRequestReporterUpdatesResponse.EResponse
    k_eNotPermitted: CMsgClientToGCRequestReporterUpdatesResponse.EResponse
    k_eNotToSoon: CMsgClientToGCRequestReporterUpdatesResponse.EResponse
    k_eNotValid: CMsgClientToGCRequestReporterUpdatesResponse.EResponse
    class ReporterUpdate(_message.Message):
        __slots__ = ("match_id", "hero_id", "report_reason", "timestamp")
        MATCH_ID_FIELD_NUMBER: _ClassVar[int]
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        REPORT_REASON_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        match_id: int
        hero_id: int
        report_reason: int
        timestamp: int
        def __init__(
            self,
            match_id: int | None = ...,
            hero_id: int | None = ...,
            report_reason: int | None = ...,
            timestamp: int | None = ...,
        ) -> None: ...

    ENUM_RESULT_FIELD_NUMBER: _ClassVar[int]
    UPDATES_FIELD_NUMBER: _ClassVar[int]
    NUM_REPORTED_FIELD_NUMBER: _ClassVar[int]
    NUM_NO_ACTION_TAKEN_FIELD_NUMBER: _ClassVar[int]
    enum_result: CMsgClientToGCRequestReporterUpdatesResponse.EResponse
    updates: _containers.RepeatedCompositeFieldContainer[
        CMsgClientToGCRequestReporterUpdatesResponse.ReporterUpdate
    ]
    num_reported: int
    num_no_action_taken: int
    def __init__(
        self,
        enum_result: CMsgClientToGCRequestReporterUpdatesResponse.EResponse | str | None = ...,
        updates: _Iterable[CMsgClientToGCRequestReporterUpdatesResponse.ReporterUpdate | _Mapping]
        | None = ...,
        num_reported: int | None = ...,
        num_no_action_taken: int | None = ...,
    ) -> None: ...

class CMsgClientToGCAcknowledgeReporterUpdates(_message.Message):
    __slots__ = ("match_ids",)
    MATCH_IDS_FIELD_NUMBER: _ClassVar[int]
    match_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, match_ids: _Iterable[int] | None = ...) -> None: ...

class CMsgClientToGCRecalibrateMMR(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCRecalibrateMMRResponse(_message.Message):
    __slots__ = ("result",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCRecalibrateMMRResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCRecalibrateMMRResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCRecalibrateMMRResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCRecalibrateMMRResponse.EResponse]
        k_eNotPermitted: _ClassVar[CMsgClientToGCRecalibrateMMRResponse.EResponse]
        k_eNotToSoon: _ClassVar[CMsgClientToGCRecalibrateMMRResponse.EResponse]
        k_eNotValid: _ClassVar[CMsgClientToGCRecalibrateMMRResponse.EResponse]

    k_eInternalError: CMsgClientToGCRecalibrateMMRResponse.EResponse
    k_eSuccess: CMsgClientToGCRecalibrateMMRResponse.EResponse
    k_eTimeout: CMsgClientToGCRecalibrateMMRResponse.EResponse
    k_eTooBusy: CMsgClientToGCRecalibrateMMRResponse.EResponse
    k_eNotPermitted: CMsgClientToGCRecalibrateMMRResponse.EResponse
    k_eNotToSoon: CMsgClientToGCRecalibrateMMRResponse.EResponse
    k_eNotValid: CMsgClientToGCRecalibrateMMRResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCRecalibrateMMRResponse.EResponse
    def __init__(
        self, result: CMsgClientToGCRecalibrateMMRResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgDOTAPostGameItemAwardNotification(_message.Message):
    __slots__ = ("receiver_account_id", "item_def_index", "action_id")
    RECEIVER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
    ACTION_ID_FIELD_NUMBER: _ClassVar[int]
    receiver_account_id: int
    item_def_index: _containers.RepeatedScalarFieldContainer[int]
    action_id: int
    def __init__(
        self,
        receiver_account_id: int | None = ...,
        item_def_index: _Iterable[int] | None = ...,
        action_id: int | None = ...,
    ) -> None: ...

class CMsgClientToGCGetOWMatchDetails(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCGetOWMatchDetailsResponse(_message.Message):
    __slots__ = (
        "result",
        "overwatch_replay_id",
        "decryption_key",
        "cluster",
        "overwatch_salt",
        "target_player_slot",
        "markers",
        "report_reason",
        "target_hero_id",
        "rank_tier",
        "lane_selection_flags",
    )
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCGetOWMatchDetailsResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCGetOWMatchDetailsResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCGetOWMatchDetailsResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCGetOWMatchDetailsResponse.EResponse]
        k_eNotPermitted: _ClassVar[CMsgClientToGCGetOWMatchDetailsResponse.EResponse]
        k_eNoCaseAvailable: _ClassVar[CMsgClientToGCGetOWMatchDetailsResponse.EResponse]

    k_eInternalError: CMsgClientToGCGetOWMatchDetailsResponse.EResponse
    k_eSuccess: CMsgClientToGCGetOWMatchDetailsResponse.EResponse
    k_eTimeout: CMsgClientToGCGetOWMatchDetailsResponse.EResponse
    k_eTooBusy: CMsgClientToGCGetOWMatchDetailsResponse.EResponse
    k_eNotPermitted: CMsgClientToGCGetOWMatchDetailsResponse.EResponse
    k_eNoCaseAvailable: CMsgClientToGCGetOWMatchDetailsResponse.EResponse
    class Marker(_message.Message):
        __slots__ = ("start_game_time_s", "end_game_time_s")
        START_GAME_TIME_S_FIELD_NUMBER: _ClassVar[int]
        END_GAME_TIME_S_FIELD_NUMBER: _ClassVar[int]
        start_game_time_s: int
        end_game_time_s: int
        def __init__(
            self, start_game_time_s: int | None = ..., end_game_time_s: int | None = ...
        ) -> None: ...

    RESULT_FIELD_NUMBER: _ClassVar[int]
    OVERWATCH_REPLAY_ID_FIELD_NUMBER: _ClassVar[int]
    DECRYPTION_KEY_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_FIELD_NUMBER: _ClassVar[int]
    OVERWATCH_SALT_FIELD_NUMBER: _ClassVar[int]
    TARGET_PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
    MARKERS_FIELD_NUMBER: _ClassVar[int]
    REPORT_REASON_FIELD_NUMBER: _ClassVar[int]
    TARGET_HERO_ID_FIELD_NUMBER: _ClassVar[int]
    RANK_TIER_FIELD_NUMBER: _ClassVar[int]
    LANE_SELECTION_FLAGS_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCGetOWMatchDetailsResponse.EResponse
    overwatch_replay_id: int
    decryption_key: int
    cluster: int
    overwatch_salt: int
    target_player_slot: int
    markers: _containers.RepeatedCompositeFieldContainer[
        CMsgClientToGCGetOWMatchDetailsResponse.Marker
    ]
    report_reason: _dota_shared_enums_pb2.EOverwatchReportReason
    target_hero_id: int
    rank_tier: int
    lane_selection_flags: int
    def __init__(
        self,
        result: CMsgClientToGCGetOWMatchDetailsResponse.EResponse | str | None = ...,
        overwatch_replay_id: int | None = ...,
        decryption_key: int | None = ...,
        cluster: int | None = ...,
        overwatch_salt: int | None = ...,
        target_player_slot: int | None = ...,
        markers: _Iterable[CMsgClientToGCGetOWMatchDetailsResponse.Marker | _Mapping] | None = ...,
        report_reason: _dota_shared_enums_pb2.EOverwatchReportReason | str | None = ...,
        target_hero_id: int | None = ...,
        rank_tier: int | None = ...,
        lane_selection_flags: int | None = ...,
    ) -> None: ...

class CMsgClientToGCSubmitOWConviction(_message.Message):
    __slots__ = (
        "overwatch_replay_id",
        "target_player_slot",
        "cheating_conviction",
        "griefing_conviction",
    )
    OVERWATCH_REPLAY_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
    CHEATING_CONVICTION_FIELD_NUMBER: _ClassVar[int]
    GRIEFING_CONVICTION_FIELD_NUMBER: _ClassVar[int]
    overwatch_replay_id: int
    target_player_slot: int
    cheating_conviction: _dota_gcmessages_common_pb2.EOverwatchConviction
    griefing_conviction: _dota_gcmessages_common_pb2.EOverwatchConviction
    def __init__(
        self,
        overwatch_replay_id: int | None = ...,
        target_player_slot: int | None = ...,
        cheating_conviction: _dota_gcmessages_common_pb2.EOverwatchConviction | str | None = ...,
        griefing_conviction: _dota_gcmessages_common_pb2.EOverwatchConviction | str | None = ...,
    ) -> None: ...

class CMsgClientToGCSubmitOWConvictionResponse(_message.Message):
    __slots__ = ("result", "overwatch_replay_id")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCSubmitOWConvictionResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCSubmitOWConvictionResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCSubmitOWConvictionResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCSubmitOWConvictionResponse.EResponse]
        k_eNotPermitted: _ClassVar[CMsgClientToGCSubmitOWConvictionResponse.EResponse]
        k_eInvalidReplayID: _ClassVar[CMsgClientToGCSubmitOWConvictionResponse.EResponse]
        k_eInvalidConviction: _ClassVar[CMsgClientToGCSubmitOWConvictionResponse.EResponse]
        k_eInvalidPlayerSlot: _ClassVar[CMsgClientToGCSubmitOWConvictionResponse.EResponse]

    k_eInternalError: CMsgClientToGCSubmitOWConvictionResponse.EResponse
    k_eSuccess: CMsgClientToGCSubmitOWConvictionResponse.EResponse
    k_eTimeout: CMsgClientToGCSubmitOWConvictionResponse.EResponse
    k_eTooBusy: CMsgClientToGCSubmitOWConvictionResponse.EResponse
    k_eNotPermitted: CMsgClientToGCSubmitOWConvictionResponse.EResponse
    k_eInvalidReplayID: CMsgClientToGCSubmitOWConvictionResponse.EResponse
    k_eInvalidConviction: CMsgClientToGCSubmitOWConvictionResponse.EResponse
    k_eInvalidPlayerSlot: CMsgClientToGCSubmitOWConvictionResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    OVERWATCH_REPLAY_ID_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCSubmitOWConvictionResponse.EResponse
    overwatch_replay_id: int
    def __init__(
        self,
        result: CMsgClientToGCSubmitOWConvictionResponse.EResponse | str | None = ...,
        overwatch_replay_id: int | None = ...,
    ) -> None: ...

class CMsgClientToGCChinaSSAURLRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCChinaSSAURLResponse(_message.Message):
    __slots__ = ("agreement_url",)
    AGREEMENT_URL_FIELD_NUMBER: _ClassVar[int]
    agreement_url: str
    def __init__(self, agreement_url: str | None = ...) -> None: ...

class CMsgClientToGCChinaSSAAcceptedRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCChinaSSAAcceptedResponse(_message.Message):
    __slots__ = ("agreement_accepted",)
    AGREEMENT_ACCEPTED_FIELD_NUMBER: _ClassVar[int]
    agreement_accepted: bool
    def __init__(self, agreement_accepted: bool = ...) -> None: ...

class CMsgGCToClientOverwatchCasesAvailable(_message.Message):
    __slots__ = ("expire_time",)
    EXPIRE_TIME_FIELD_NUMBER: _ClassVar[int]
    expire_time: int
    def __init__(self, expire_time: int | None = ...) -> None: ...

class CMsgClientToGCStartWatchingOverwatch(_message.Message):
    __slots__ = ("overwatch_replay_id", "target_player_slot")
    OVERWATCH_REPLAY_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
    overwatch_replay_id: int
    target_player_slot: int
    def __init__(
        self, overwatch_replay_id: int | None = ..., target_player_slot: int | None = ...
    ) -> None: ...

class CMsgClientToGCStopWatchingOverwatch(_message.Message):
    __slots__ = ("overwatch_replay_id", "target_player_slot")
    OVERWATCH_REPLAY_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
    overwatch_replay_id: int
    target_player_slot: int
    def __init__(
        self, overwatch_replay_id: int | None = ..., target_player_slot: int | None = ...
    ) -> None: ...

class CMsgClientToGCOverwatchReplayError(_message.Message):
    __slots__ = ("overwatch_replay_id",)
    OVERWATCH_REPLAY_ID_FIELD_NUMBER: _ClassVar[int]
    overwatch_replay_id: int
    def __init__(self, overwatch_replay_id: int | None = ...) -> None: ...

class CMsgClientToGCGetDPCFavorites(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCGetDPCFavoritesResponse(_message.Message):
    __slots__ = ("result", "favorites")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCGetDPCFavoritesResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCGetDPCFavoritesResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCGetDPCFavoritesResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCGetDPCFavoritesResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCGetDPCFavoritesResponse.EResponse]
        k_eInvalidRequest: _ClassVar[CMsgClientToGCGetDPCFavoritesResponse.EResponse]

    k_eInternalError: CMsgClientToGCGetDPCFavoritesResponse.EResponse
    k_eSuccess: CMsgClientToGCGetDPCFavoritesResponse.EResponse
    k_eTooBusy: CMsgClientToGCGetDPCFavoritesResponse.EResponse
    k_eDisabled: CMsgClientToGCGetDPCFavoritesResponse.EResponse
    k_eTimeout: CMsgClientToGCGetDPCFavoritesResponse.EResponse
    k_eInvalidRequest: CMsgClientToGCGetDPCFavoritesResponse.EResponse
    class Favorite(_message.Message):
        __slots__ = ("favorite_type", "favorite_id")
        FAVORITE_TYPE_FIELD_NUMBER: _ClassVar[int]
        FAVORITE_ID_FIELD_NUMBER: _ClassVar[int]
        favorite_type: _dota_shared_enums_pb2.EDPCFavoriteType
        favorite_id: int
        def __init__(
            self,
            favorite_type: _dota_shared_enums_pb2.EDPCFavoriteType | str | None = ...,
            favorite_id: int | None = ...,
        ) -> None: ...

    RESULT_FIELD_NUMBER: _ClassVar[int]
    FAVORITES_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCGetDPCFavoritesResponse.EResponse
    favorites: _containers.RepeatedCompositeFieldContainer[
        CMsgClientToGCGetDPCFavoritesResponse.Favorite
    ]
    def __init__(
        self,
        result: CMsgClientToGCGetDPCFavoritesResponse.EResponse | str | None = ...,
        favorites: _Iterable[CMsgClientToGCGetDPCFavoritesResponse.Favorite | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgClientToGCSetDPCFavoriteState(_message.Message):
    __slots__ = ("favorite_type", "favorite_id", "enabled")
    FAVORITE_TYPE_FIELD_NUMBER: _ClassVar[int]
    FAVORITE_ID_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    favorite_type: _dota_shared_enums_pb2.EDPCFavoriteType
    favorite_id: int
    enabled: bool
    def __init__(
        self,
        favorite_type: _dota_shared_enums_pb2.EDPCFavoriteType | str | None = ...,
        favorite_id: int | None = ...,
        enabled: bool = ...,
    ) -> None: ...

class CMsgClientToGCSetDPCFavoriteStateResponse(_message.Message):
    __slots__ = ("result",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCSetDPCFavoriteStateResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCSetDPCFavoriteStateResponse.EResponse]
        k_eFavoriteTypeOutOfRange: _ClassVar[CMsgClientToGCSetDPCFavoriteStateResponse.EResponse]
        k_eLockFailed: _ClassVar[CMsgClientToGCSetDPCFavoriteStateResponse.EResponse]
        k_eAlreadyFavorited: _ClassVar[CMsgClientToGCSetDPCFavoriteStateResponse.EResponse]
        k_eAlreadyUnfavorited: _ClassVar[CMsgClientToGCSetDPCFavoriteStateResponse.EResponse]
        k_eInsertRecordFailed: _ClassVar[CMsgClientToGCSetDPCFavoriteStateResponse.EResponse]
        k_eRemoveRecordFailed: _ClassVar[CMsgClientToGCSetDPCFavoriteStateResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCSetDPCFavoriteStateResponse.EResponse]

    k_eInternalError: CMsgClientToGCSetDPCFavoriteStateResponse.EResponse
    k_eSuccess: CMsgClientToGCSetDPCFavoriteStateResponse.EResponse
    k_eFavoriteTypeOutOfRange: CMsgClientToGCSetDPCFavoriteStateResponse.EResponse
    k_eLockFailed: CMsgClientToGCSetDPCFavoriteStateResponse.EResponse
    k_eAlreadyFavorited: CMsgClientToGCSetDPCFavoriteStateResponse.EResponse
    k_eAlreadyUnfavorited: CMsgClientToGCSetDPCFavoriteStateResponse.EResponse
    k_eInsertRecordFailed: CMsgClientToGCSetDPCFavoriteStateResponse.EResponse
    k_eRemoveRecordFailed: CMsgClientToGCSetDPCFavoriteStateResponse.EResponse
    k_eTimeout: CMsgClientToGCSetDPCFavoriteStateResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCSetDPCFavoriteStateResponse.EResponse
    def __init__(
        self, result: CMsgClientToGCSetDPCFavoriteStateResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCSetEventActiveSeasonID(_message.Message):
    __slots__ = ("event_id", "active_season_id")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_SEASON_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    active_season_id: int
    def __init__(self, event_id: int | None = ..., active_season_id: int | None = ...) -> None: ...

class CMsgClientToGCSetEventActiveSeasonIDResponse(_message.Message):
    __slots__ = ("result",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCSetEventActiveSeasonIDResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCSetEventActiveSeasonIDResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCSetEventActiveSeasonIDResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCSetEventActiveSeasonIDResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCSetEventActiveSeasonIDResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCSetEventActiveSeasonIDResponse.EResponse]
        k_eInternalSuccessNoChange: _ClassVar[
            CMsgClientToGCSetEventActiveSeasonIDResponse.EResponse
        ]

    k_eInternalError: CMsgClientToGCSetEventActiveSeasonIDResponse.EResponse
    k_eSuccess: CMsgClientToGCSetEventActiveSeasonIDResponse.EResponse
    k_eDisabled: CMsgClientToGCSetEventActiveSeasonIDResponse.EResponse
    k_eTooBusy: CMsgClientToGCSetEventActiveSeasonIDResponse.EResponse
    k_eNotAllowed: CMsgClientToGCSetEventActiveSeasonIDResponse.EResponse
    k_eTimeout: CMsgClientToGCSetEventActiveSeasonIDResponse.EResponse
    k_eInternalSuccessNoChange: CMsgClientToGCSetEventActiveSeasonIDResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCSetEventActiveSeasonIDResponse.EResponse
    def __init__(
        self, result: CMsgClientToGCSetEventActiveSeasonIDResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCPurchaseLabyrinthBlessings(_message.Message):
    __slots__ = ("event_id", "blessing_ids", "debug", "debug_remove")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    BLESSING_IDS_FIELD_NUMBER: _ClassVar[int]
    DEBUG_FIELD_NUMBER: _ClassVar[int]
    DEBUG_REMOVE_FIELD_NUMBER: _ClassVar[int]
    event_id: _dota_shared_enums_pb2.EEvent
    blessing_ids: _containers.RepeatedScalarFieldContainer[int]
    debug: bool
    debug_remove: bool
    def __init__(
        self,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
        blessing_ids: _Iterable[int] | None = ...,
        debug: bool = ...,
        debug_remove: bool = ...,
    ) -> None: ...

class CMsgClientToGCPurchaseLabyrinthBlessingsResponse(_message.Message):
    __slots__ = ("result",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCPurchaseLabyrinthBlessingsResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCPurchaseLabyrinthBlessingsResponse.EResponse]
        k_eNoSuchBlessing: _ClassVar[CMsgClientToGCPurchaseLabyrinthBlessingsResponse.EResponse]
        k_eNotEnoughShards: _ClassVar[CMsgClientToGCPurchaseLabyrinthBlessingsResponse.EResponse]
        k_eNoPath: _ClassVar[CMsgClientToGCPurchaseLabyrinthBlessingsResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCPurchaseLabyrinthBlessingsResponse.EResponse]

    k_eInternalError: CMsgClientToGCPurchaseLabyrinthBlessingsResponse.EResponse
    k_eSuccess: CMsgClientToGCPurchaseLabyrinthBlessingsResponse.EResponse
    k_eNoSuchBlessing: CMsgClientToGCPurchaseLabyrinthBlessingsResponse.EResponse
    k_eNotEnoughShards: CMsgClientToGCPurchaseLabyrinthBlessingsResponse.EResponse
    k_eNoPath: CMsgClientToGCPurchaseLabyrinthBlessingsResponse.EResponse
    k_eTimeout: CMsgClientToGCPurchaseLabyrinthBlessingsResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCPurchaseLabyrinthBlessingsResponse.EResponse
    def __init__(
        self, result: CMsgClientToGCPurchaseLabyrinthBlessingsResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCGetStickerbookRequest(_message.Message):
    __slots__ = ("account_id",)
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    def __init__(self, account_id: int | None = ...) -> None: ...

class CMsgClientToGCGetStickerbookResponse(_message.Message):
    __slots__ = ("response", "stickerbook")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCGetStickerbookResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCGetStickerbookResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCGetStickerbookResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCGetStickerbookResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCGetStickerbookResponse.EResponse]

    k_eInternalError: CMsgClientToGCGetStickerbookResponse.EResponse
    k_eSuccess: CMsgClientToGCGetStickerbookResponse.EResponse
    k_eTimeout: CMsgClientToGCGetStickerbookResponse.EResponse
    k_eNotAllowed: CMsgClientToGCGetStickerbookResponse.EResponse
    k_eTooBusy: CMsgClientToGCGetStickerbookResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    STICKERBOOK_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCGetStickerbookResponse.EResponse
    stickerbook: _dota_gcmessages_common_pb2.CMsgStickerbook
    def __init__(
        self,
        response: CMsgClientToGCGetStickerbookResponse.EResponse | str | None = ...,
        stickerbook: _dota_gcmessages_common_pb2.CMsgStickerbook | _Mapping | None = ...,
    ) -> None: ...

class CMsgClientToGCCreateStickerbookPageRequest(_message.Message):
    __slots__ = ("team_id", "event_id", "page_type")
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    team_id: int
    event_id: _dota_shared_enums_pb2.EEvent
    page_type: _dota_gcmessages_common_pb2.EStickerbookPageType
    def __init__(
        self,
        team_id: int | None = ...,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
        page_type: _dota_gcmessages_common_pb2.EStickerbookPageType | str | None = ...,
    ) -> None: ...

class CMsgClientToGCCreateStickerbookPageResponse(_message.Message):
    __slots__ = ("response", "page_number")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCCreateStickerbookPageResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCCreateStickerbookPageResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCCreateStickerbookPageResponse.EResponse]
        k_eTooManyPages: _ClassVar[CMsgClientToGCCreateStickerbookPageResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCCreateStickerbookPageResponse.EResponse]

    k_eInternalError: CMsgClientToGCCreateStickerbookPageResponse.EResponse
    k_eSuccess: CMsgClientToGCCreateStickerbookPageResponse.EResponse
    k_eTimeout: CMsgClientToGCCreateStickerbookPageResponse.EResponse
    k_eTooManyPages: CMsgClientToGCCreateStickerbookPageResponse.EResponse
    k_eTooBusy: CMsgClientToGCCreateStickerbookPageResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    PAGE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCCreateStickerbookPageResponse.EResponse
    page_number: int
    def __init__(
        self,
        response: CMsgClientToGCCreateStickerbookPageResponse.EResponse | str | None = ...,
        page_number: int | None = ...,
    ) -> None: ...

class CMsgClientToGCDeleteStickerbookPageRequest(_message.Message):
    __slots__ = ("page_num", "sticker_count", "sticker_max")
    PAGE_NUM_FIELD_NUMBER: _ClassVar[int]
    STICKER_COUNT_FIELD_NUMBER: _ClassVar[int]
    STICKER_MAX_FIELD_NUMBER: _ClassVar[int]
    page_num: int
    sticker_count: int
    sticker_max: int
    def __init__(
        self,
        page_num: int | None = ...,
        sticker_count: int | None = ...,
        sticker_max: int | None = ...,
    ) -> None: ...

class CMsgClientToGCDeleteStickerbookPageResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCDeleteStickerbookPageResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCDeleteStickerbookPageResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCDeleteStickerbookPageResponse.EResponse]
        k_eInvalidStickerCount: _ClassVar[CMsgClientToGCDeleteStickerbookPageResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCDeleteStickerbookPageResponse.EResponse]
        k_eInvalidStickerMax: _ClassVar[CMsgClientToGCDeleteStickerbookPageResponse.EResponse]
        k_eInvalidPage: _ClassVar[CMsgClientToGCDeleteStickerbookPageResponse.EResponse]

    k_eInternalError: CMsgClientToGCDeleteStickerbookPageResponse.EResponse
    k_eSuccess: CMsgClientToGCDeleteStickerbookPageResponse.EResponse
    k_eTimeout: CMsgClientToGCDeleteStickerbookPageResponse.EResponse
    k_eInvalidStickerCount: CMsgClientToGCDeleteStickerbookPageResponse.EResponse
    k_eTooBusy: CMsgClientToGCDeleteStickerbookPageResponse.EResponse
    k_eInvalidStickerMax: CMsgClientToGCDeleteStickerbookPageResponse.EResponse
    k_eInvalidPage: CMsgClientToGCDeleteStickerbookPageResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCDeleteStickerbookPageResponse.EResponse
    def __init__(
        self, response: CMsgClientToGCDeleteStickerbookPageResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCPlaceStickersRequest(_message.Message):
    __slots__ = ("sticker_items",)
    class StickerItem(_message.Message):
        __slots__ = ("page_num", "sticker")
        PAGE_NUM_FIELD_NUMBER: _ClassVar[int]
        STICKER_FIELD_NUMBER: _ClassVar[int]
        page_num: int
        sticker: _dota_gcmessages_common_pb2.CMsgStickerbookSticker
        def __init__(
            self,
            page_num: int | None = ...,
            sticker: _dota_gcmessages_common_pb2.CMsgStickerbookSticker | _Mapping | None = ...,
        ) -> None: ...

    STICKER_ITEMS_FIELD_NUMBER: _ClassVar[int]
    sticker_items: _containers.RepeatedCompositeFieldContainer[
        CMsgClientToGCPlaceStickersRequest.StickerItem
    ]
    def __init__(
        self,
        sticker_items: _Iterable[CMsgClientToGCPlaceStickersRequest.StickerItem | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgClientToGCPlaceStickersResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCPlaceStickersResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCPlaceStickersResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCPlaceStickersResponse.EResponse]
        k_eMissingItem: _ClassVar[CMsgClientToGCPlaceStickersResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCPlaceStickersResponse.EResponse]
        k_eDuplicateItem: _ClassVar[CMsgClientToGCPlaceStickersResponse.EResponse]
        k_eInvalidPage: _ClassVar[CMsgClientToGCPlaceStickersResponse.EResponse]
        k_ePageTypeMismatch: _ClassVar[CMsgClientToGCPlaceStickersResponse.EResponse]
        k_eTooManyStickers: _ClassVar[CMsgClientToGCPlaceStickersResponse.EResponse]

    k_eInternalError: CMsgClientToGCPlaceStickersResponse.EResponse
    k_eSuccess: CMsgClientToGCPlaceStickersResponse.EResponse
    k_eTimeout: CMsgClientToGCPlaceStickersResponse.EResponse
    k_eMissingItem: CMsgClientToGCPlaceStickersResponse.EResponse
    k_eTooBusy: CMsgClientToGCPlaceStickersResponse.EResponse
    k_eDuplicateItem: CMsgClientToGCPlaceStickersResponse.EResponse
    k_eInvalidPage: CMsgClientToGCPlaceStickersResponse.EResponse
    k_ePageTypeMismatch: CMsgClientToGCPlaceStickersResponse.EResponse
    k_eTooManyStickers: CMsgClientToGCPlaceStickersResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCPlaceStickersResponse.EResponse
    def __init__(
        self, response: CMsgClientToGCPlaceStickersResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCPlaceCollectionStickersRequest(_message.Message):
    __slots__ = ("slots",)
    class Slot(_message.Message):
        __slots__ = ("page_num", "slot", "new_item_id", "old_item_def_id", "old_quality")
        PAGE_NUM_FIELD_NUMBER: _ClassVar[int]
        SLOT_FIELD_NUMBER: _ClassVar[int]
        NEW_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
        OLD_ITEM_DEF_ID_FIELD_NUMBER: _ClassVar[int]
        OLD_QUALITY_FIELD_NUMBER: _ClassVar[int]
        page_num: int
        slot: int
        new_item_id: int
        old_item_def_id: int
        old_quality: int
        def __init__(
            self,
            page_num: int | None = ...,
            slot: int | None = ...,
            new_item_id: int | None = ...,
            old_item_def_id: int | None = ...,
            old_quality: int | None = ...,
        ) -> None: ...

    SLOTS_FIELD_NUMBER: _ClassVar[int]
    slots: _containers.RepeatedCompositeFieldContainer[
        CMsgClientToGCPlaceCollectionStickersRequest.Slot
    ]
    def __init__(
        self,
        slots: _Iterable[CMsgClientToGCPlaceCollectionStickersRequest.Slot | _Mapping] | None = ...,
    ) -> None: ...

class CMsgClientToGCPlaceCollectionStickersResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCPlaceCollectionStickersResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCPlaceCollectionStickersResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCPlaceCollectionStickersResponse.EResponse]
        k_eMissingItem: _ClassVar[CMsgClientToGCPlaceCollectionStickersResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCPlaceCollectionStickersResponse.EResponse]
        k_eDuplicateItem: _ClassVar[CMsgClientToGCPlaceCollectionStickersResponse.EResponse]
        k_eInvalidPage: _ClassVar[CMsgClientToGCPlaceCollectionStickersResponse.EResponse]
        k_ePageTypeMismatch: _ClassVar[CMsgClientToGCPlaceCollectionStickersResponse.EResponse]
        k_eOldItemMismatch: _ClassVar[CMsgClientToGCPlaceCollectionStickersResponse.EResponse]
        k_eInvalidSlot: _ClassVar[CMsgClientToGCPlaceCollectionStickersResponse.EResponse]
        k_eSlotTypeMismatch: _ClassVar[CMsgClientToGCPlaceCollectionStickersResponse.EResponse]

    k_eInternalError: CMsgClientToGCPlaceCollectionStickersResponse.EResponse
    k_eSuccess: CMsgClientToGCPlaceCollectionStickersResponse.EResponse
    k_eTimeout: CMsgClientToGCPlaceCollectionStickersResponse.EResponse
    k_eMissingItem: CMsgClientToGCPlaceCollectionStickersResponse.EResponse
    k_eTooBusy: CMsgClientToGCPlaceCollectionStickersResponse.EResponse
    k_eDuplicateItem: CMsgClientToGCPlaceCollectionStickersResponse.EResponse
    k_eInvalidPage: CMsgClientToGCPlaceCollectionStickersResponse.EResponse
    k_ePageTypeMismatch: CMsgClientToGCPlaceCollectionStickersResponse.EResponse
    k_eOldItemMismatch: CMsgClientToGCPlaceCollectionStickersResponse.EResponse
    k_eInvalidSlot: CMsgClientToGCPlaceCollectionStickersResponse.EResponse
    k_eSlotTypeMismatch: CMsgClientToGCPlaceCollectionStickersResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCPlaceCollectionStickersResponse.EResponse
    def __init__(
        self, response: CMsgClientToGCPlaceCollectionStickersResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCOrderStickerbookTeamPageRequest(_message.Message):
    __slots__ = ("page_order_sequence",)
    PAGE_ORDER_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    page_order_sequence: _dota_gcmessages_common_pb2.CMsgStickerbookTeamPageOrderSequence
    def __init__(
        self,
        page_order_sequence: _dota_gcmessages_common_pb2.CMsgStickerbookTeamPageOrderSequence
        | _Mapping
        | None = ...,
    ) -> None: ...

class CMsgClientToGCOrderStickerbookTeamPageResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCOrderStickerbookTeamPageResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCOrderStickerbookTeamPageResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCOrderStickerbookTeamPageResponse.EResponse]
        k_eTooManyPages: _ClassVar[CMsgClientToGCOrderStickerbookTeamPageResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCOrderStickerbookTeamPageResponse.EResponse]
        k_eInvalidPage: _ClassVar[CMsgClientToGCOrderStickerbookTeamPageResponse.EResponse]

    k_eInternalError: CMsgClientToGCOrderStickerbookTeamPageResponse.EResponse
    k_eSuccess: CMsgClientToGCOrderStickerbookTeamPageResponse.EResponse
    k_eTimeout: CMsgClientToGCOrderStickerbookTeamPageResponse.EResponse
    k_eTooManyPages: CMsgClientToGCOrderStickerbookTeamPageResponse.EResponse
    k_eTooBusy: CMsgClientToGCOrderStickerbookTeamPageResponse.EResponse
    k_eInvalidPage: CMsgClientToGCOrderStickerbookTeamPageResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCOrderStickerbookTeamPageResponse.EResponse
    def __init__(
        self, response: CMsgClientToGCOrderStickerbookTeamPageResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCSetHeroSticker(_message.Message):
    __slots__ = ("hero_id", "new_item_id", "old_item_id")
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    OLD_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    hero_id: int
    new_item_id: int
    old_item_id: int
    def __init__(
        self,
        hero_id: int | None = ...,
        new_item_id: int | None = ...,
        old_item_id: int | None = ...,
    ) -> None: ...

class CMsgClientToGCSetHeroStickerResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCSetHeroStickerResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCSetHeroStickerResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCSetHeroStickerResponse.EResponse]
        k_eMissingItem: _ClassVar[CMsgClientToGCSetHeroStickerResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCSetHeroStickerResponse.EResponse]
        k_eOldItemMismatch: _ClassVar[CMsgClientToGCSetHeroStickerResponse.EResponse]
        k_eInvalidHero: _ClassVar[CMsgClientToGCSetHeroStickerResponse.EResponse]

    k_eInternalError: CMsgClientToGCSetHeroStickerResponse.EResponse
    k_eSuccess: CMsgClientToGCSetHeroStickerResponse.EResponse
    k_eTimeout: CMsgClientToGCSetHeroStickerResponse.EResponse
    k_eMissingItem: CMsgClientToGCSetHeroStickerResponse.EResponse
    k_eTooBusy: CMsgClientToGCSetHeroStickerResponse.EResponse
    k_eOldItemMismatch: CMsgClientToGCSetHeroStickerResponse.EResponse
    k_eInvalidHero: CMsgClientToGCSetHeroStickerResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCSetHeroStickerResponse.EResponse
    def __init__(
        self, response: CMsgClientToGCSetHeroStickerResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCGetHeroStickers(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCGetHeroStickersResponse(_message.Message):
    __slots__ = ("response", "sticker_heroes")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCGetHeroStickersResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCGetHeroStickersResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCGetHeroStickersResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCGetHeroStickersResponse.EResponse]

    k_eInternalError: CMsgClientToGCGetHeroStickersResponse.EResponse
    k_eSuccess: CMsgClientToGCGetHeroStickersResponse.EResponse
    k_eTimeout: CMsgClientToGCGetHeroStickersResponse.EResponse
    k_eTooBusy: CMsgClientToGCGetHeroStickersResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    STICKER_HEROES_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCGetHeroStickersResponse.EResponse
    sticker_heroes: _dota_gcmessages_common_pb2.CMsgStickerHeroes
    def __init__(
        self,
        response: CMsgClientToGCGetHeroStickersResponse.EResponse | str | None = ...,
        sticker_heroes: _dota_gcmessages_common_pb2.CMsgStickerHeroes | _Mapping | None = ...,
    ) -> None: ...

class CMsgClientToGCSetFavoritePage(_message.Message):
    __slots__ = ("page_num", "clear")
    PAGE_NUM_FIELD_NUMBER: _ClassVar[int]
    CLEAR_FIELD_NUMBER: _ClassVar[int]
    page_num: int
    clear: bool
    def __init__(self, page_num: int | None = ..., clear: bool = ...) -> None: ...

class CMsgClientToGCSetFavoritePageResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCSetFavoritePageResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCSetFavoritePageResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCSetFavoritePageResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCSetFavoritePageResponse.EResponse]
        k_eInvalidPage: _ClassVar[CMsgClientToGCSetFavoritePageResponse.EResponse]

    k_eInternalError: CMsgClientToGCSetFavoritePageResponse.EResponse
    k_eSuccess: CMsgClientToGCSetFavoritePageResponse.EResponse
    k_eTimeout: CMsgClientToGCSetFavoritePageResponse.EResponse
    k_eTooBusy: CMsgClientToGCSetFavoritePageResponse.EResponse
    k_eInvalidPage: CMsgClientToGCSetFavoritePageResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCSetFavoritePageResponse.EResponse
    def __init__(
        self, response: CMsgClientToGCSetFavoritePageResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCClaimSwag(_message.Message):
    __slots__ = ("event_id", "action_id", "data")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    event_id: _dota_shared_enums_pb2.EEvent
    action_id: int
    data: int
    def __init__(
        self,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
        action_id: int | None = ...,
        data: int | None = ...,
    ) -> None: ...

class CMsgClientToGCClaimSwagResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCClaimSwagResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCClaimSwagResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCClaimSwagResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCClaimSwagResponse.EResponse]
        k_eAlreadyClaimed: _ClassVar[CMsgClientToGCClaimSwagResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCClaimSwagResponse.EResponse]
        k_eInvalidRequest: _ClassVar[CMsgClientToGCClaimSwagResponse.EResponse]
        k_eUserNotEligible: _ClassVar[CMsgClientToGCClaimSwagResponse.EResponse]
        k_eStorageError: _ClassVar[CMsgClientToGCClaimSwagResponse.EResponse]
        k_eRewardDisabled: _ClassVar[CMsgClientToGCClaimSwagResponse.EResponse]

    k_eInternalError: CMsgClientToGCClaimSwagResponse.EResponse
    k_eSuccess: CMsgClientToGCClaimSwagResponse.EResponse
    k_eTimeout: CMsgClientToGCClaimSwagResponse.EResponse
    k_eTooBusy: CMsgClientToGCClaimSwagResponse.EResponse
    k_eAlreadyClaimed: CMsgClientToGCClaimSwagResponse.EResponse
    k_eDisabled: CMsgClientToGCClaimSwagResponse.EResponse
    k_eInvalidRequest: CMsgClientToGCClaimSwagResponse.EResponse
    k_eUserNotEligible: CMsgClientToGCClaimSwagResponse.EResponse
    k_eStorageError: CMsgClientToGCClaimSwagResponse.EResponse
    k_eRewardDisabled: CMsgClientToGCClaimSwagResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCClaimSwagResponse.EResponse
    def __init__(
        self, response: CMsgClientToGCClaimSwagResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCCollectorsCacheAvailableDataRequest(_message.Message):
    __slots__ = ("contest_id",)
    CONTEST_ID_FIELD_NUMBER: _ClassVar[int]
    contest_id: int
    def __init__(self, contest_id: int | None = ...) -> None: ...

class CMsgGCToClientCollectorsCacheAvailableDataResponse(_message.Message):
    __slots__ = ("votes",)
    class Vote(_message.Message):
        __slots__ = ("item_def", "vote_type")
        class EVoteType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            k_eUp: _ClassVar[CMsgGCToClientCollectorsCacheAvailableDataResponse.Vote.EVoteType]
            k_eDown: _ClassVar[CMsgGCToClientCollectorsCacheAvailableDataResponse.Vote.EVoteType]

        k_eUp: CMsgGCToClientCollectorsCacheAvailableDataResponse.Vote.EVoteType
        k_eDown: CMsgGCToClientCollectorsCacheAvailableDataResponse.Vote.EVoteType
        ITEM_DEF_FIELD_NUMBER: _ClassVar[int]
        VOTE_TYPE_FIELD_NUMBER: _ClassVar[int]
        item_def: int
        vote_type: CMsgGCToClientCollectorsCacheAvailableDataResponse.Vote.EVoteType
        def __init__(
            self,
            item_def: int | None = ...,
            vote_type: CMsgGCToClientCollectorsCacheAvailableDataResponse.Vote.EVoteType
            | str
            | None = ...,
        ) -> None: ...

    VOTES_FIELD_NUMBER: _ClassVar[int]
    votes: _containers.RepeatedCompositeFieldContainer[
        CMsgGCToClientCollectorsCacheAvailableDataResponse.Vote
    ]
    def __init__(
        self,
        votes: _Iterable[CMsgGCToClientCollectorsCacheAvailableDataResponse.Vote | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgClientToGCUploadMatchClip(_message.Message):
    __slots__ = ("match_clip",)
    MATCH_CLIP_FIELD_NUMBER: _ClassVar[int]
    match_clip: _dota_gcmessages_common_pb2.CMatchClip
    def __init__(
        self, match_clip: _dota_gcmessages_common_pb2.CMatchClip | _Mapping | None = ...
    ) -> None: ...

class CMsgGCToClientUploadMatchClipResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgGCToClientUploadMatchClipResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgGCToClientUploadMatchClipResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgGCToClientUploadMatchClipResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgGCToClientUploadMatchClipResponse.EResponse]

    k_eInternalError: CMsgGCToClientUploadMatchClipResponse.EResponse
    k_eSuccess: CMsgGCToClientUploadMatchClipResponse.EResponse
    k_eTimeout: CMsgGCToClientUploadMatchClipResponse.EResponse
    k_eTooBusy: CMsgGCToClientUploadMatchClipResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgGCToClientUploadMatchClipResponse.EResponse
    def __init__(
        self, response: CMsgGCToClientUploadMatchClipResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCMapStatsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgGCToClientMapStatsResponse(_message.Message):
    __slots__ = ("response", "personal_stats", "global_stats")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgGCToClientMapStatsResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgGCToClientMapStatsResponse.EResponse]

    k_eInternalError: CMsgGCToClientMapStatsResponse.EResponse
    k_eSuccess: CMsgGCToClientMapStatsResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    PERSONAL_STATS_FIELD_NUMBER: _ClassVar[int]
    GLOBAL_STATS_FIELD_NUMBER: _ClassVar[int]
    response: CMsgGCToClientMapStatsResponse.EResponse
    personal_stats: _dota_gcmessages_common_pb2.CMsgMapStatsSnapshot
    global_stats: _dota_gcmessages_common_pb2.CMsgGlobalMapStats
    def __init__(
        self,
        response: CMsgGCToClientMapStatsResponse.EResponse | str | None = ...,
        personal_stats: _dota_gcmessages_common_pb2.CMsgMapStatsSnapshot | _Mapping | None = ...,
        global_stats: _dota_gcmessages_common_pb2.CMsgGlobalMapStats | _Mapping | None = ...,
    ) -> None: ...

class CMsgRoadToTIAssignedQuest(_message.Message):
    __slots__ = ("quest_id", "difficulty", "progress_flags", "half_credit_flags", "completed")
    QUEST_ID_FIELD_NUMBER: _ClassVar[int]
    DIFFICULTY_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FLAGS_FIELD_NUMBER: _ClassVar[int]
    HALF_CREDIT_FLAGS_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    quest_id: int
    difficulty: int
    progress_flags: int
    half_credit_flags: int
    completed: bool
    def __init__(
        self,
        quest_id: int | None = ...,
        difficulty: int | None = ...,
        progress_flags: int | None = ...,
        half_credit_flags: int | None = ...,
        completed: bool = ...,
    ) -> None: ...

class CMsgRoadToTIUserData(_message.Message):
    __slots__ = ("quests",)
    QUESTS_FIELD_NUMBER: _ClassVar[int]
    quests: _containers.RepeatedCompositeFieldContainer[CMsgRoadToTIAssignedQuest]
    def __init__(
        self, quests: _Iterable[CMsgRoadToTIAssignedQuest | _Mapping] | None = ...
    ) -> None: ...

class CMsgClientToGCRoadToTIGetQuests(_message.Message):
    __slots__ = ("event_id",)
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    def __init__(self, event_id: int | None = ...) -> None: ...

class CMsgClientToGCRoadToTIGetQuestsResponse(_message.Message):
    __slots__ = ("response", "quest_data")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCRoadToTIGetQuestsResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCRoadToTIGetQuestsResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCRoadToTIGetQuestsResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCRoadToTIGetQuestsResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCRoadToTIGetQuestsResponse.EResponse]
        k_eInvalidID: _ClassVar[CMsgClientToGCRoadToTIGetQuestsResponse.EResponse]

    k_eInternalError: CMsgClientToGCRoadToTIGetQuestsResponse.EResponse
    k_eSuccess: CMsgClientToGCRoadToTIGetQuestsResponse.EResponse
    k_eTooBusy: CMsgClientToGCRoadToTIGetQuestsResponse.EResponse
    k_eDisabled: CMsgClientToGCRoadToTIGetQuestsResponse.EResponse
    k_eTimeout: CMsgClientToGCRoadToTIGetQuestsResponse.EResponse
    k_eInvalidID: CMsgClientToGCRoadToTIGetQuestsResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    QUEST_DATA_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCRoadToTIGetQuestsResponse.EResponse
    quest_data: CMsgRoadToTIUserData
    def __init__(
        self,
        response: CMsgClientToGCRoadToTIGetQuestsResponse.EResponse | str | None = ...,
        quest_data: CMsgRoadToTIUserData | _Mapping | None = ...,
    ) -> None: ...

class CMsgClientToGCRoadToTIGetActiveQuest(_message.Message):
    __slots__ = ("event_id",)
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    def __init__(self, event_id: int | None = ...) -> None: ...

class CMsgClientToGCRoadToTIGetActiveQuestResponse(_message.Message):
    __slots__ = ("response", "quest_data")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCRoadToTIGetActiveQuestResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCRoadToTIGetActiveQuestResponse.EResponse]
        k_eNone: _ClassVar[CMsgClientToGCRoadToTIGetActiveQuestResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCRoadToTIGetActiveQuestResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCRoadToTIGetActiveQuestResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCRoadToTIGetActiveQuestResponse.EResponse]
        k_eInvalidID: _ClassVar[CMsgClientToGCRoadToTIGetActiveQuestResponse.EResponse]

    k_eInternalError: CMsgClientToGCRoadToTIGetActiveQuestResponse.EResponse
    k_eSuccess: CMsgClientToGCRoadToTIGetActiveQuestResponse.EResponse
    k_eNone: CMsgClientToGCRoadToTIGetActiveQuestResponse.EResponse
    k_eTooBusy: CMsgClientToGCRoadToTIGetActiveQuestResponse.EResponse
    k_eDisabled: CMsgClientToGCRoadToTIGetActiveQuestResponse.EResponse
    k_eTimeout: CMsgClientToGCRoadToTIGetActiveQuestResponse.EResponse
    k_eInvalidID: CMsgClientToGCRoadToTIGetActiveQuestResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    QUEST_DATA_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCRoadToTIGetActiveQuestResponse.EResponse
    quest_data: CMsgRoadToTIAssignedQuest
    def __init__(
        self,
        response: CMsgClientToGCRoadToTIGetActiveQuestResponse.EResponse | str | None = ...,
        quest_data: CMsgRoadToTIAssignedQuest | _Mapping | None = ...,
    ) -> None: ...

class CMsgGCToClientRoadToTIQuestDataUpdated(_message.Message):
    __slots__ = ("event_id", "quest_data")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    QUEST_DATA_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    quest_data: CMsgRoadToTIUserData
    def __init__(
        self, event_id: int | None = ..., quest_data: CMsgRoadToTIUserData | _Mapping | None = ...
    ) -> None: ...

class CMsgClientToGCRoadToTIUseItem(_message.Message):
    __slots__ = ("event_id", "item_type", "hero_index")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_TYPE_FIELD_NUMBER: _ClassVar[int]
    HERO_INDEX_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    item_type: int
    hero_index: int
    def __init__(
        self, event_id: int | None = ..., item_type: int | None = ..., hero_index: int | None = ...
    ) -> None: ...

class CMsgClientToGCRoadToTIUseItemResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCRoadToTIUseItemResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCRoadToTIUseItemResponse.EResponse]
        k_eBadInput: _ClassVar[CMsgClientToGCRoadToTIUseItemResponse.EResponse]
        k_eNoItem: _ClassVar[CMsgClientToGCRoadToTIUseItemResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCRoadToTIUseItemResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCRoadToTIUseItemResponse.EResponse]
        k_eInvalidID: _ClassVar[CMsgClientToGCRoadToTIUseItemResponse.EResponse]

    k_eInternalError: CMsgClientToGCRoadToTIUseItemResponse.EResponse
    k_eSuccess: CMsgClientToGCRoadToTIUseItemResponse.EResponse
    k_eBadInput: CMsgClientToGCRoadToTIUseItemResponse.EResponse
    k_eNoItem: CMsgClientToGCRoadToTIUseItemResponse.EResponse
    k_eDisabled: CMsgClientToGCRoadToTIUseItemResponse.EResponse
    k_eTimeout: CMsgClientToGCRoadToTIUseItemResponse.EResponse
    k_eInvalidID: CMsgClientToGCRoadToTIUseItemResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCRoadToTIUseItemResponse.EResponse
    def __init__(
        self, response: CMsgClientToGCRoadToTIUseItemResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCRoadToTIDevForceQuest(_message.Message):
    __slots__ = ("event_id", "force_match_type", "force_id")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    FORCE_MATCH_TYPE_FIELD_NUMBER: _ClassVar[int]
    FORCE_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    force_match_type: bool
    force_id: int
    def __init__(
        self, event_id: int | None = ..., force_match_type: bool = ..., force_id: int | None = ...
    ) -> None: ...

class CMsgLobbyRoadToTIMatchQuestData(_message.Message):
    __slots__ = ("quest_data", "quest_period", "quest_number")
    QUEST_DATA_FIELD_NUMBER: _ClassVar[int]
    QUEST_PERIOD_FIELD_NUMBER: _ClassVar[int]
    QUEST_NUMBER_FIELD_NUMBER: _ClassVar[int]
    quest_data: CMsgRoadToTIAssignedQuest
    quest_period: int
    quest_number: int
    def __init__(
        self,
        quest_data: CMsgRoadToTIAssignedQuest | _Mapping | None = ...,
        quest_period: int | None = ...,
        quest_number: int | None = ...,
    ) -> None: ...

class CMsgClientToGCNewBloomGift(_message.Message):
    __slots__ = ("defindex", "lobby_id", "target_account_ids")
    DEFINDEX_FIELD_NUMBER: _ClassVar[int]
    LOBBY_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_ACCOUNT_IDS_FIELD_NUMBER: _ClassVar[int]
    defindex: int
    lobby_id: int
    target_account_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        defindex: int | None = ...,
        lobby_id: int | None = ...,
        target_account_ids: _Iterable[int] | None = ...,
    ) -> None: ...

class CMsgClientToGCNewBloomGiftResponse(_message.Message):
    __slots__ = ("result", "received_account_ids")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_ACCOUNT_IDS_FIELD_NUMBER: _ClassVar[int]
    result: _dota_gcmessages_common_pb2.ENewBloomGiftingResponse
    received_account_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        result: _dota_gcmessages_common_pb2.ENewBloomGiftingResponse | str | None = ...,
        received_account_ids: _Iterable[int] | None = ...,
    ) -> None: ...

class CMsgClientToGCSetBannedHeroes(_message.Message):
    __slots__ = ("banned_hero_ids",)
    BANNED_HERO_IDS_FIELD_NUMBER: _ClassVar[int]
    banned_hero_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, banned_hero_ids: _Iterable[int] | None = ...) -> None: ...

class CMsgClientToGCUpdateComicBookStats(_message.Message):
    __slots__ = ("comic_id", "stats", "language_stats")
    class SingleStat(_message.Message):
        __slots__ = ("stat_type", "stat_value")
        STAT_TYPE_FIELD_NUMBER: _ClassVar[int]
        STAT_VALUE_FIELD_NUMBER: _ClassVar[int]
        stat_type: CMsgClientToGCUpdateComicBookStat_Type
        stat_value: int
        def __init__(
            self,
            stat_type: CMsgClientToGCUpdateComicBookStat_Type | str | None = ...,
            stat_value: int | None = ...,
        ) -> None: ...

    class LanguageStats(_message.Message):
        __slots__ = ("comic_id", "client_language", "client_comic_language")
        COMIC_ID_FIELD_NUMBER: _ClassVar[int]
        CLIENT_LANGUAGE_FIELD_NUMBER: _ClassVar[int]
        CLIENT_COMIC_LANGUAGE_FIELD_NUMBER: _ClassVar[int]
        comic_id: int
        client_language: int
        client_comic_language: int
        def __init__(
            self,
            comic_id: int | None = ...,
            client_language: int | None = ...,
            client_comic_language: int | None = ...,
        ) -> None: ...

    COMIC_ID_FIELD_NUMBER: _ClassVar[int]
    STATS_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_STATS_FIELD_NUMBER: _ClassVar[int]
    comic_id: int
    stats: _containers.RepeatedCompositeFieldContainer[
        CMsgClientToGCUpdateComicBookStats.SingleStat
    ]
    language_stats: CMsgClientToGCUpdateComicBookStats.LanguageStats
    def __init__(
        self,
        comic_id: int | None = ...,
        stats: _Iterable[CMsgClientToGCUpdateComicBookStats.SingleStat | _Mapping] | None = ...,
        language_stats: CMsgClientToGCUpdateComicBookStats.LanguageStats | _Mapping | None = ...,
    ) -> None: ...

class CMsgGCRankedPlayerInfoSubmit(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: str | None = ...) -> None: ...

class CMsgGCRankedPlayerInfoSubmitResponse(_message.Message):
    __slots__ = ("result",)
    class EResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgGCRankedPlayerInfoSubmitResponse.EResult]
        ERROR_UNSPECIFIED: _ClassVar[CMsgGCRankedPlayerInfoSubmitResponse.EResult]

    SUCCESS: CMsgGCRankedPlayerInfoSubmitResponse.EResult
    ERROR_UNSPECIFIED: CMsgGCRankedPlayerInfoSubmitResponse.EResult
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgGCRankedPlayerInfoSubmitResponse.EResult
    def __init__(
        self, result: CMsgGCRankedPlayerInfoSubmitResponse.EResult | str | None = ...
    ) -> None: ...

class CMsgDOTAClaimGatedEvent(_message.Message):
    __slots__ = ("event_id",)
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: _dota_shared_enums_pb2.EEvent
    def __init__(self, event_id: _dota_shared_enums_pb2.EEvent | str | None = ...) -> None: ...

class CMsgDOTAClaimGatedEventResponse(_message.Message):
    __slots__ = ("result",)
    class ResultCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        Success: _ClassVar[CMsgDOTAClaimGatedEventResponse.ResultCode]
        InvalidEvent: _ClassVar[CMsgDOTAClaimGatedEventResponse.ResultCode]
        EventNotActive: _ClassVar[CMsgDOTAClaimGatedEventResponse.ResultCode]
        UserIneligible: _ClassVar[CMsgDOTAClaimGatedEventResponse.ResultCode]
        AlreadyClaimed: _ClassVar[CMsgDOTAClaimGatedEventResponse.ResultCode]
        ServerError: _ClassVar[CMsgDOTAClaimGatedEventResponse.ResultCode]
        RateLimit: _ClassVar[CMsgDOTAClaimGatedEventResponse.ResultCode]

    Success: CMsgDOTAClaimGatedEventResponse.ResultCode
    InvalidEvent: CMsgDOTAClaimGatedEventResponse.ResultCode
    EventNotActive: CMsgDOTAClaimGatedEventResponse.ResultCode
    UserIneligible: CMsgDOTAClaimGatedEventResponse.ResultCode
    AlreadyClaimed: CMsgDOTAClaimGatedEventResponse.ResultCode
    ServerError: CMsgDOTAClaimGatedEventResponse.ResultCode
    RateLimit: CMsgDOTAClaimGatedEventResponse.ResultCode
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgDOTAClaimGatedEventResponse.ResultCode
    def __init__(
        self, result: CMsgDOTAClaimGatedEventResponse.ResultCode | str | None = ...
    ) -> None: ...

class CMsgClientToGCGetEventRanking(_message.Message):
    __slots__ = ("event_id", "account_id")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: _dota_shared_enums_pb2.EEvent
    account_id: int
    def __init__(
        self,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
        account_id: int | None = ...,
    ) -> None: ...

class CMsgClientToGCGetEventRankingResponse(_message.Message):
    __slots__ = ("event_id", "account_id", "score", "percentile", "final_rank_bucket")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    PERCENTILE_FIELD_NUMBER: _ClassVar[int]
    FINAL_RANK_BUCKET_FIELD_NUMBER: _ClassVar[int]
    event_id: _dota_shared_enums_pb2.EEvent
    account_id: int
    score: float
    percentile: float
    final_rank_bucket: int
    def __init__(
        self,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
        account_id: int | None = ...,
        score: float | None = ...,
        percentile: float | None = ...,
        final_rank_bucket: int | None = ...,
    ) -> None: ...

class CMsgClientToGCGetEventCoupon(_message.Message):
    __slots__ = ("event_id", "coupon_ids")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    COUPON_IDS_FIELD_NUMBER: _ClassVar[int]
    event_id: _dota_shared_enums_pb2.EEvent
    coupon_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
        coupon_ids: _Iterable[int] | None = ...,
    ) -> None: ...

class CMsgClientToGCGetEventCouponResponse(_message.Message):
    __slots__ = ("result", "event_id", "coupons")
    class ResultCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        Success: _ClassVar[CMsgClientToGCGetEventCouponResponse.ResultCode]
        InvalidEvent: _ClassVar[CMsgClientToGCGetEventCouponResponse.ResultCode]
        EventNotActive: _ClassVar[CMsgClientToGCGetEventCouponResponse.ResultCode]
        UserIneligible: _ClassVar[CMsgClientToGCGetEventCouponResponse.ResultCode]
        ServerError: _ClassVar[CMsgClientToGCGetEventCouponResponse.ResultCode]
        Timeout: _ClassVar[CMsgClientToGCGetEventCouponResponse.ResultCode]
        MultipleCoupons: _ClassVar[CMsgClientToGCGetEventCouponResponse.ResultCode]

    Success: CMsgClientToGCGetEventCouponResponse.ResultCode
    InvalidEvent: CMsgClientToGCGetEventCouponResponse.ResultCode
    EventNotActive: CMsgClientToGCGetEventCouponResponse.ResultCode
    UserIneligible: CMsgClientToGCGetEventCouponResponse.ResultCode
    ServerError: CMsgClientToGCGetEventCouponResponse.ResultCode
    Timeout: CMsgClientToGCGetEventCouponResponse.ResultCode
    MultipleCoupons: CMsgClientToGCGetEventCouponResponse.ResultCode
    class Coupon(_message.Message):
        __slots__ = ("coupon_id", "coupon_code")
        COUPON_ID_FIELD_NUMBER: _ClassVar[int]
        COUPON_CODE_FIELD_NUMBER: _ClassVar[int]
        coupon_id: int
        coupon_code: str
        def __init__(self, coupon_id: int | None = ..., coupon_code: str | None = ...) -> None: ...

    RESULT_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    COUPONS_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCGetEventCouponResponse.ResultCode
    event_id: _dota_shared_enums_pb2.EEvent
    coupons: _containers.RepeatedCompositeFieldContainer[
        CMsgClientToGCGetEventCouponResponse.Coupon
    ]
    def __init__(
        self,
        result: CMsgClientToGCGetEventCouponResponse.ResultCode | str | None = ...,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
        coupons: _Iterable[CMsgClientToGCGetEventCouponResponse.Coupon | _Mapping] | None = ...,
    ) -> None: ...

class CMsgClientToGCConvertEventPoints(_message.Message):
    __slots__ = (
        "event_id_points_to_buy",
        "event_id_points_to_spend",
        "num_points_to_buy",
        "num_points_to_spend",
    )
    EVENT_ID_POINTS_TO_BUY_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_POINTS_TO_SPEND_FIELD_NUMBER: _ClassVar[int]
    NUM_POINTS_TO_BUY_FIELD_NUMBER: _ClassVar[int]
    NUM_POINTS_TO_SPEND_FIELD_NUMBER: _ClassVar[int]
    event_id_points_to_buy: _dota_shared_enums_pb2.EEvent
    event_id_points_to_spend: _dota_shared_enums_pb2.EEvent
    num_points_to_buy: int
    num_points_to_spend: int
    def __init__(
        self,
        event_id_points_to_buy: _dota_shared_enums_pb2.EEvent | str | None = ...,
        event_id_points_to_spend: _dota_shared_enums_pb2.EEvent | str | None = ...,
        num_points_to_buy: int | None = ...,
        num_points_to_spend: int | None = ...,
    ) -> None: ...

class CMsgClientToGCConvertEventPointsResponse(_message.Message):
    __slots__ = ("result",)
    class ResultCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        Success: _ClassVar[CMsgClientToGCConvertEventPointsResponse.ResultCode]
        InvalidEvent: _ClassVar[CMsgClientToGCConvertEventPointsResponse.ResultCode]
        EventNotActive: _ClassVar[CMsgClientToGCConvertEventPointsResponse.ResultCode]
        UserIneligible: _ClassVar[CMsgClientToGCConvertEventPointsResponse.ResultCode]
        ServerError: _ClassVar[CMsgClientToGCConvertEventPointsResponse.ResultCode]
        Timeout: _ClassVar[CMsgClientToGCConvertEventPointsResponse.ResultCode]

    Success: CMsgClientToGCConvertEventPointsResponse.ResultCode
    InvalidEvent: CMsgClientToGCConvertEventPointsResponse.ResultCode
    EventNotActive: CMsgClientToGCConvertEventPointsResponse.ResultCode
    UserIneligible: CMsgClientToGCConvertEventPointsResponse.ResultCode
    ServerError: CMsgClientToGCConvertEventPointsResponse.ResultCode
    Timeout: CMsgClientToGCConvertEventPointsResponse.ResultCode
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCConvertEventPointsResponse.ResultCode
    def __init__(
        self, result: CMsgClientToGCConvertEventPointsResponse.ResultCode | str | None = ...
    ) -> None: ...

class CMsgClientToGCInviteToDemoMode(_message.Message):
    __slots__ = ("server_id", "invited_player_id")
    SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    INVITED_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    server_id: int
    invited_player_id: int
    def __init__(
        self, server_id: int | None = ..., invited_player_id: int | None = ...
    ) -> None: ...

class CMsgGCToClientInviteToDemoMode(_message.Message):
    __slots__ = ("server_id", "from_player", "party_invite")
    SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    FROM_PLAYER_FIELD_NUMBER: _ClassVar[int]
    PARTY_INVITE_FIELD_NUMBER: _ClassVar[int]
    server_id: int
    from_player: int
    party_invite: bool
    def __init__(
        self, server_id: int | None = ..., from_player: int | None = ..., party_invite: bool = ...
    ) -> None: ...
