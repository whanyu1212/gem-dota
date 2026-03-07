from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

import dota_gcmessages_common_lobby_pb2 as _dota_gcmessages_common_lobby_pb2
import dota_shared_enums_pb2 as _dota_shared_enums_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class ECoachTeammateRating(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_ECoachTeammateRating_None: _ClassVar[ECoachTeammateRating]
    k_ECoachTeammateRating_Positive: _ClassVar[ECoachTeammateRating]
    k_ECoachTeammateRating_Negative: _ClassVar[ECoachTeammateRating]
    k_ECoachTeammateRating_Abusive: _ClassVar[ECoachTeammateRating]

class EPrivateCoachingSessionState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_ePrivateCoachingSessionState_Invalid: _ClassVar[EPrivateCoachingSessionState]
    k_ePrivateCoachingSessionState_SearchingForCoach: _ClassVar[EPrivateCoachingSessionState]
    k_ePrivateCoachingSessionState_CoachAssigned: _ClassVar[EPrivateCoachingSessionState]
    k_ePrivateCoachingSessionState_Finished: _ClassVar[EPrivateCoachingSessionState]
    k_ePrivateCoachingSessionState_Expired: _ClassVar[EPrivateCoachingSessionState]
    k_ePrivateCoachingSessionState_Abandoned: _ClassVar[EPrivateCoachingSessionState]

class EPrivateCoachingSessionMemberFlag(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EPrivateCoachingSessionMemberFlag_Requester: _ClassVar[EPrivateCoachingSessionMemberFlag]
    k_EPrivateCoachingSessionMemberFlag_Coach: _ClassVar[EPrivateCoachingSessionMemberFlag]
    k_EPrivateCoachingSessionMemberFlag_LeftSession: _ClassVar[EPrivateCoachingSessionMemberFlag]

class EPlayerCoachMatchFlag(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EPlayerCoachMatchFlag_EligibleForRewards: _ClassVar[EPlayerCoachMatchFlag]
    k_EPlayerCoachMatchFlag_PrivateCoach: _ClassVar[EPlayerCoachMatchFlag]

k_ECoachTeammateRating_None: ECoachTeammateRating
k_ECoachTeammateRating_Positive: ECoachTeammateRating
k_ECoachTeammateRating_Negative: ECoachTeammateRating
k_ECoachTeammateRating_Abusive: ECoachTeammateRating
k_ePrivateCoachingSessionState_Invalid: EPrivateCoachingSessionState
k_ePrivateCoachingSessionState_SearchingForCoach: EPrivateCoachingSessionState
k_ePrivateCoachingSessionState_CoachAssigned: EPrivateCoachingSessionState
k_ePrivateCoachingSessionState_Finished: EPrivateCoachingSessionState
k_ePrivateCoachingSessionState_Expired: EPrivateCoachingSessionState
k_ePrivateCoachingSessionState_Abandoned: EPrivateCoachingSessionState
k_EPrivateCoachingSessionMemberFlag_Requester: EPrivateCoachingSessionMemberFlag
k_EPrivateCoachingSessionMemberFlag_Coach: EPrivateCoachingSessionMemberFlag
k_EPrivateCoachingSessionMemberFlag_LeftSession: EPrivateCoachingSessionMemberFlag
k_EPlayerCoachMatchFlag_EligibleForRewards: EPlayerCoachMatchFlag
k_EPlayerCoachMatchFlag_PrivateCoach: EPlayerCoachMatchFlag

class CMsgPlayerCoachMatch(_message.Message):
    __slots__ = (
        "match_id",
        "match_outcome",
        "coached_team",
        "start_time",
        "duration",
        "teammate_ratings",
        "coach_flags",
    )
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    MATCH_OUTCOME_FIELD_NUMBER: _ClassVar[int]
    COACHED_TEAM_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    TEAMMATE_RATINGS_FIELD_NUMBER: _ClassVar[int]
    COACH_FLAGS_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    match_outcome: _dota_shared_enums_pb2.EMatchOutcome
    coached_team: int
    start_time: int
    duration: int
    teammate_ratings: _containers.RepeatedScalarFieldContainer[ECoachTeammateRating]
    coach_flags: int
    def __init__(
        self,
        match_id: int | None = ...,
        match_outcome: _dota_shared_enums_pb2.EMatchOutcome | str | None = ...,
        coached_team: int | None = ...,
        start_time: int | None = ...,
        duration: int | None = ...,
        teammate_ratings: _Iterable[ECoachTeammateRating | str] | None = ...,
        coach_flags: int | None = ...,
    ) -> None: ...

class CMsgPrivateCoachingSessionMember(_message.Message):
    __slots__ = ("account_id", "member_flags", "member_session_rating")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    MEMBER_FLAGS_FIELD_NUMBER: _ClassVar[int]
    MEMBER_SESSION_RATING_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    member_flags: int
    member_session_rating: ECoachTeammateRating
    def __init__(
        self,
        account_id: int | None = ...,
        member_flags: int | None = ...,
        member_session_rating: ECoachTeammateRating | str | None = ...,
    ) -> None: ...

class CMsgPrivateCoachingSession(_message.Message):
    __slots__ = (
        "private_coaching_session_id",
        "requested_timestamp",
        "requested_language",
        "coaching_session_state",
        "session_members",
        "current_lobby_id",
        "current_server_steam_id",
        "accepted_timestamp",
        "completed_timestamp",
    )
    PRIVATE_COACHING_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    COACHING_SESSION_STATE_FIELD_NUMBER: _ClassVar[int]
    SESSION_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    CURRENT_LOBBY_ID_FIELD_NUMBER: _ClassVar[int]
    CURRENT_SERVER_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    ACCEPTED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    private_coaching_session_id: int
    requested_timestamp: int
    requested_language: int
    coaching_session_state: EPrivateCoachingSessionState
    session_members: _containers.RepeatedCompositeFieldContainer[CMsgPrivateCoachingSessionMember]
    current_lobby_id: int
    current_server_steam_id: int
    accepted_timestamp: int
    completed_timestamp: int
    def __init__(
        self,
        private_coaching_session_id: int | None = ...,
        requested_timestamp: int | None = ...,
        requested_language: int | None = ...,
        coaching_session_state: EPrivateCoachingSessionState | str | None = ...,
        session_members: _Iterable[CMsgPrivateCoachingSessionMember | _Mapping] | None = ...,
        current_lobby_id: int | None = ...,
        current_server_steam_id: int | None = ...,
        accepted_timestamp: int | None = ...,
        completed_timestamp: int | None = ...,
    ) -> None: ...

class CMsgPrivateCoachingSessionStatus(_message.Message):
    __slots__ = ("requester_competitive_rank_tier", "requester_games_played")
    REQUESTER_COMPETITIVE_RANK_TIER_FIELD_NUMBER: _ClassVar[int]
    REQUESTER_GAMES_PLAYED_FIELD_NUMBER: _ClassVar[int]
    requester_competitive_rank_tier: int
    requester_games_played: int
    def __init__(
        self,
        requester_competitive_rank_tier: int | None = ...,
        requester_games_played: int | None = ...,
    ) -> None: ...

class CMsgAvailablePrivateCoachingSession(_message.Message):
    __slots__ = ("coaching_session", "coaching_session_status")
    COACHING_SESSION_FIELD_NUMBER: _ClassVar[int]
    COACHING_SESSION_STATUS_FIELD_NUMBER: _ClassVar[int]
    coaching_session: CMsgPrivateCoachingSession
    coaching_session_status: CMsgPrivateCoachingSessionStatus
    def __init__(
        self,
        coaching_session: CMsgPrivateCoachingSession | _Mapping | None = ...,
        coaching_session_status: CMsgPrivateCoachingSessionStatus | _Mapping | None = ...,
    ) -> None: ...

class CMsgAvailablePrivateCoachingSessionList(_message.Message):
    __slots__ = ("available_coaching_sessions",)
    AVAILABLE_COACHING_SESSIONS_FIELD_NUMBER: _ClassVar[int]
    available_coaching_sessions: _containers.RepeatedCompositeFieldContainer[
        CMsgAvailablePrivateCoachingSession
    ]
    def __init__(
        self,
        available_coaching_sessions: _Iterable[CMsgAvailablePrivateCoachingSession | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgAvailablePrivateCoachingSessionSummary(_message.Message):
    __slots__ = ("coaching_session_count",)
    COACHING_SESSION_COUNT_FIELD_NUMBER: _ClassVar[int]
    coaching_session_count: int
    def __init__(self, coaching_session_count: int | None = ...) -> None: ...

class CMsgClientToGCRequestPlayerCoachMatches(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCRequestPlayerCoachMatchesResponse(_message.Message):
    __slots__ = ("result", "coach_matches")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCRequestPlayerCoachMatchesResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCRequestPlayerCoachMatchesResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCRequestPlayerCoachMatchesResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCRequestPlayerCoachMatchesResponse.EResponse]

    k_eInternalError: CMsgClientToGCRequestPlayerCoachMatchesResponse.EResponse
    k_eSuccess: CMsgClientToGCRequestPlayerCoachMatchesResponse.EResponse
    k_eTooBusy: CMsgClientToGCRequestPlayerCoachMatchesResponse.EResponse
    k_eDisabled: CMsgClientToGCRequestPlayerCoachMatchesResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    COACH_MATCHES_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCRequestPlayerCoachMatchesResponse.EResponse
    coach_matches: _containers.RepeatedCompositeFieldContainer[CMsgPlayerCoachMatch]
    def __init__(
        self,
        result: CMsgClientToGCRequestPlayerCoachMatchesResponse.EResponse | str | None = ...,
        coach_matches: _Iterable[CMsgPlayerCoachMatch | _Mapping] | None = ...,
    ) -> None: ...

class CMsgClientToGCRequestPlayerCoachMatch(_message.Message):
    __slots__ = ("match_id",)
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    def __init__(self, match_id: int | None = ...) -> None: ...

class CMsgClientToGCRequestPlayerCoachMatchResponse(_message.Message):
    __slots__ = ("result", "coach_match")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCRequestPlayerCoachMatchResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCRequestPlayerCoachMatchResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCRequestPlayerCoachMatchResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCRequestPlayerCoachMatchResponse.EResponse]

    k_eInternalError: CMsgClientToGCRequestPlayerCoachMatchResponse.EResponse
    k_eSuccess: CMsgClientToGCRequestPlayerCoachMatchResponse.EResponse
    k_eTooBusy: CMsgClientToGCRequestPlayerCoachMatchResponse.EResponse
    k_eDisabled: CMsgClientToGCRequestPlayerCoachMatchResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    COACH_MATCH_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCRequestPlayerCoachMatchResponse.EResponse
    coach_match: CMsgPlayerCoachMatch
    def __init__(
        self,
        result: CMsgClientToGCRequestPlayerCoachMatchResponse.EResponse | str | None = ...,
        coach_match: CMsgPlayerCoachMatch | _Mapping | None = ...,
    ) -> None: ...

class CMsgClientToGCSubmitCoachTeammateRating(_message.Message):
    __slots__ = ("match_id", "coach_account_id", "rating", "reason")
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    COACH_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    coach_account_id: int
    rating: ECoachTeammateRating
    reason: str
    def __init__(
        self,
        match_id: int | None = ...,
        coach_account_id: int | None = ...,
        rating: ECoachTeammateRating | str | None = ...,
        reason: str | None = ...,
    ) -> None: ...

class CMsgClientToGCSubmitCoachTeammateRatingResponse(_message.Message):
    __slots__ = ("result",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCSubmitCoachTeammateRatingResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCSubmitCoachTeammateRatingResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCSubmitCoachTeammateRatingResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCSubmitCoachTeammateRatingResponse.EResponse]
        k_eInvalidInput: _ClassVar[CMsgClientToGCSubmitCoachTeammateRatingResponse.EResponse]
        k_eAlreadySubmitted: _ClassVar[CMsgClientToGCSubmitCoachTeammateRatingResponse.EResponse]
        k_eVotingFinished: _ClassVar[CMsgClientToGCSubmitCoachTeammateRatingResponse.EResponse]
        k_ePlayerNotInMatch: _ClassVar[CMsgClientToGCSubmitCoachTeammateRatingResponse.EResponse]
        k_eCoachNotInMatch: _ClassVar[CMsgClientToGCSubmitCoachTeammateRatingResponse.EResponse]
        k_ePlayerNotOnCoachTeam: _ClassVar[
            CMsgClientToGCSubmitCoachTeammateRatingResponse.EResponse
        ]
        k_ePlayerInSamePartyAsCoach: _ClassVar[
            CMsgClientToGCSubmitCoachTeammateRatingResponse.EResponse
        ]
        k_eMatchNotEligible: _ClassVar[CMsgClientToGCSubmitCoachTeammateRatingResponse.EResponse]

    k_eInternalError: CMsgClientToGCSubmitCoachTeammateRatingResponse.EResponse
    k_eSuccess: CMsgClientToGCSubmitCoachTeammateRatingResponse.EResponse
    k_eTooBusy: CMsgClientToGCSubmitCoachTeammateRatingResponse.EResponse
    k_eDisabled: CMsgClientToGCSubmitCoachTeammateRatingResponse.EResponse
    k_eInvalidInput: CMsgClientToGCSubmitCoachTeammateRatingResponse.EResponse
    k_eAlreadySubmitted: CMsgClientToGCSubmitCoachTeammateRatingResponse.EResponse
    k_eVotingFinished: CMsgClientToGCSubmitCoachTeammateRatingResponse.EResponse
    k_ePlayerNotInMatch: CMsgClientToGCSubmitCoachTeammateRatingResponse.EResponse
    k_eCoachNotInMatch: CMsgClientToGCSubmitCoachTeammateRatingResponse.EResponse
    k_ePlayerNotOnCoachTeam: CMsgClientToGCSubmitCoachTeammateRatingResponse.EResponse
    k_ePlayerInSamePartyAsCoach: CMsgClientToGCSubmitCoachTeammateRatingResponse.EResponse
    k_eMatchNotEligible: CMsgClientToGCSubmitCoachTeammateRatingResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCSubmitCoachTeammateRatingResponse.EResponse
    def __init__(
        self, result: CMsgClientToGCSubmitCoachTeammateRatingResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgGCToClientCoachTeammateRatingsChanged(_message.Message):
    __slots__ = ("coach_match",)
    COACH_MATCH_FIELD_NUMBER: _ClassVar[int]
    coach_match: CMsgPlayerCoachMatch
    def __init__(self, coach_match: CMsgPlayerCoachMatch | _Mapping | None = ...) -> None: ...

class CMsgClientToGCRequestPrivateCoachingSession(_message.Message):
    __slots__ = ("language",)
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    language: int
    def __init__(self, language: int | None = ...) -> None: ...

class CMsgClientToGCRequestPrivateCoachingSessionResponse(_message.Message):
    __slots__ = ("result", "coaching_session")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse]
        k_eAlreadyInSession: _ClassVar[
            CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse
        ]
        k_eBehaviorScoreTooLow: _ClassVar[
            CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse
        ]
        k_eInvalidLobbyType: _ClassVar[
            CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse
        ]
        k_eLowPriorityPlayer: _ClassVar[
            CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse
        ]
        k_eLowPriorityLobby: _ClassVar[
            CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse
        ]
        k_eLowPriorityParty: _ClassVar[
            CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse
        ]
        k_eTextChatBan: _ClassVar[CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse]
        k_eVoiceChatBan: _ClassVar[CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse]
        k_eMatchBan: _ClassVar[CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse]

    k_eInternalError: CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse
    k_eSuccess: CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse
    k_eTooBusy: CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse
    k_eDisabled: CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse
    k_eTimeout: CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse
    k_eAlreadyInSession: CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse
    k_eBehaviorScoreTooLow: CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse
    k_eInvalidLobbyType: CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse
    k_eLowPriorityPlayer: CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse
    k_eLowPriorityLobby: CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse
    k_eLowPriorityParty: CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse
    k_eTextChatBan: CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse
    k_eVoiceChatBan: CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse
    k_eMatchBan: CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    COACHING_SESSION_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse
    coaching_session: CMsgPrivateCoachingSession
    def __init__(
        self,
        result: CMsgClientToGCRequestPrivateCoachingSessionResponse.EResponse | str | None = ...,
        coaching_session: CMsgPrivateCoachingSession | _Mapping | None = ...,
    ) -> None: ...

class CMsgClientToGCAcceptPrivateCoachingSession(_message.Message):
    __slots__ = ("coaching_session_id",)
    COACHING_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    coaching_session_id: int
    def __init__(self, coaching_session_id: int | None = ...) -> None: ...

class CMsgClientToGCAcceptPrivateCoachingSessionResponse(_message.Message):
    __slots__ = ("result", "coaching_session")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse]
        k_eUnknownSession: _ClassVar[CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse]
        k_eAlreadyHasCoach: _ClassVar[CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse]
        k_eAlreadyHasSession: _ClassVar[
            CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse
        ]
        k_eInvalidUser: _ClassVar[CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse]
        k_eAlreadyFinished: _ClassVar[CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse]
        k_eInvalidLobbyType: _ClassVar[CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse]
        k_eAlreadyInLobby: _ClassVar[CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse]
        k_eLobbyIsLan: _ClassVar[CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse]
        k_eLobbyIsLeague: _ClassVar[CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse]
        k_eInvalidLobbyState: _ClassVar[
            CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse
        ]
        k_eRequesterIsNotPlayer: _ClassVar[
            CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse
        ]
        k_eTooManyCoaches: _ClassVar[CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse]
        k_eCoachWasPlayer: _ClassVar[CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse]
        k_eCoachBehaviorScoreTooLow: _ClassVar[
            CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse
        ]
        k_eCoachRankNotCalibrated: _ClassVar[
            CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse
        ]
        k_eCoachRankNotEligible: _ClassVar[
            CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse
        ]
        k_eCoachRankTooLow: _ClassVar[CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse]

    k_eInternalError: CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse
    k_eSuccess: CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse
    k_eTooBusy: CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse
    k_eDisabled: CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse
    k_eTimeout: CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse
    k_eUnknownSession: CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse
    k_eAlreadyHasCoach: CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse
    k_eAlreadyHasSession: CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse
    k_eInvalidUser: CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse
    k_eAlreadyFinished: CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse
    k_eInvalidLobbyType: CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse
    k_eAlreadyInLobby: CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse
    k_eLobbyIsLan: CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse
    k_eLobbyIsLeague: CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse
    k_eInvalidLobbyState: CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse
    k_eRequesterIsNotPlayer: CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse
    k_eTooManyCoaches: CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse
    k_eCoachWasPlayer: CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse
    k_eCoachBehaviorScoreTooLow: CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse
    k_eCoachRankNotCalibrated: CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse
    k_eCoachRankNotEligible: CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse
    k_eCoachRankTooLow: CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    COACHING_SESSION_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse
    coaching_session: CMsgPrivateCoachingSession
    def __init__(
        self,
        result: CMsgClientToGCAcceptPrivateCoachingSessionResponse.EResponse | str | None = ...,
        coaching_session: CMsgPrivateCoachingSession | _Mapping | None = ...,
    ) -> None: ...

class CMsgClientToGCLeavePrivateCoachingSession(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCLeavePrivateCoachingSessionResponse(_message.Message):
    __slots__ = ("result",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCLeavePrivateCoachingSessionResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCLeavePrivateCoachingSessionResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCLeavePrivateCoachingSessionResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCLeavePrivateCoachingSessionResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCLeavePrivateCoachingSessionResponse.EResponse]
        k_eNoSession: _ClassVar[CMsgClientToGCLeavePrivateCoachingSessionResponse.EResponse]
        k_eAlreadyLeft: _ClassVar[CMsgClientToGCLeavePrivateCoachingSessionResponse.EResponse]

    k_eInternalError: CMsgClientToGCLeavePrivateCoachingSessionResponse.EResponse
    k_eSuccess: CMsgClientToGCLeavePrivateCoachingSessionResponse.EResponse
    k_eTooBusy: CMsgClientToGCLeavePrivateCoachingSessionResponse.EResponse
    k_eDisabled: CMsgClientToGCLeavePrivateCoachingSessionResponse.EResponse
    k_eTimeout: CMsgClientToGCLeavePrivateCoachingSessionResponse.EResponse
    k_eNoSession: CMsgClientToGCLeavePrivateCoachingSessionResponse.EResponse
    k_eAlreadyLeft: CMsgClientToGCLeavePrivateCoachingSessionResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCLeavePrivateCoachingSessionResponse.EResponse
    def __init__(
        self, result: CMsgClientToGCLeavePrivateCoachingSessionResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCGetCurrentPrivateCoachingSession(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCGetCurrentPrivateCoachingSessionResponse(_message.Message):
    __slots__ = ("result", "current_session")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[
            CMsgClientToGCGetCurrentPrivateCoachingSessionResponse.EResponse
        ]
        k_eSuccess: _ClassVar[CMsgClientToGCGetCurrentPrivateCoachingSessionResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCGetCurrentPrivateCoachingSessionResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCGetCurrentPrivateCoachingSessionResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCGetCurrentPrivateCoachingSessionResponse.EResponse]

    k_eInternalError: CMsgClientToGCGetCurrentPrivateCoachingSessionResponse.EResponse
    k_eSuccess: CMsgClientToGCGetCurrentPrivateCoachingSessionResponse.EResponse
    k_eTooBusy: CMsgClientToGCGetCurrentPrivateCoachingSessionResponse.EResponse
    k_eDisabled: CMsgClientToGCGetCurrentPrivateCoachingSessionResponse.EResponse
    k_eTimeout: CMsgClientToGCGetCurrentPrivateCoachingSessionResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    CURRENT_SESSION_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCGetCurrentPrivateCoachingSessionResponse.EResponse
    current_session: CMsgPrivateCoachingSession
    def __init__(
        self,
        result: CMsgClientToGCGetCurrentPrivateCoachingSessionResponse.EResponse | str | None = ...,
        current_session: CMsgPrivateCoachingSession | _Mapping | None = ...,
    ) -> None: ...

class CMsgGCToClientPrivateCoachingSessionUpdated(_message.Message):
    __slots__ = ("coaching_session",)
    COACHING_SESSION_FIELD_NUMBER: _ClassVar[int]
    coaching_session: CMsgPrivateCoachingSession
    def __init__(
        self, coaching_session: CMsgPrivateCoachingSession | _Mapping | None = ...
    ) -> None: ...

class CMsgClientToGCSubmitPrivateCoachingSessionRating(_message.Message):
    __slots__ = ("coaching_session_id", "session_rating")
    COACHING_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    SESSION_RATING_FIELD_NUMBER: _ClassVar[int]
    coaching_session_id: int
    session_rating: ECoachTeammateRating
    def __init__(
        self,
        coaching_session_id: int | None = ...,
        session_rating: ECoachTeammateRating | str | None = ...,
    ) -> None: ...

class CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse(_message.Message):
    __slots__ = ("result",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[
            CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse.EResponse
        ]
        k_eSuccess: _ClassVar[CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse.EResponse]
        k_eUnknownSession: _ClassVar[
            CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse.EResponse
        ]
        k_eNotMember: _ClassVar[CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse.EResponse]
        k_eAlreadySubmitted: _ClassVar[
            CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse.EResponse
        ]
        k_eSessionActive: _ClassVar[
            CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse.EResponse
        ]
        k_eSessionTooShort: _ClassVar[
            CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse.EResponse
        ]
        k_eNoCoach: _ClassVar[CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse.EResponse]
        k_eInvalidRating: _ClassVar[
            CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse.EResponse
        ]

    k_eInternalError: CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse.EResponse
    k_eSuccess: CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse.EResponse
    k_eTooBusy: CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse.EResponse
    k_eDisabled: CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse.EResponse
    k_eTimeout: CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse.EResponse
    k_eUnknownSession: CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse.EResponse
    k_eNotMember: CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse.EResponse
    k_eAlreadySubmitted: CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse.EResponse
    k_eSessionActive: CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse.EResponse
    k_eSessionTooShort: CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse.EResponse
    k_eNoCoach: CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse.EResponse
    k_eInvalidRating: CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse.EResponse
    def __init__(
        self,
        result: CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse.EResponse
        | str
        | None = ...,
    ) -> None: ...

class CMsgClientToGCGetAvailablePrivateCoachingSessions(_message.Message):
    __slots__ = ("language",)
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    language: int
    def __init__(self, language: int | None = ...) -> None: ...

class CMsgClientToGCGetAvailablePrivateCoachingSessionsResponse(_message.Message):
    __slots__ = ("result", "available_sessions_list")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[
            CMsgClientToGCGetAvailablePrivateCoachingSessionsResponse.EResponse
        ]
        k_eSuccess: _ClassVar[CMsgClientToGCGetAvailablePrivateCoachingSessionsResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCGetAvailablePrivateCoachingSessionsResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCGetAvailablePrivateCoachingSessionsResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCGetAvailablePrivateCoachingSessionsResponse.EResponse]

    k_eInternalError: CMsgClientToGCGetAvailablePrivateCoachingSessionsResponse.EResponse
    k_eSuccess: CMsgClientToGCGetAvailablePrivateCoachingSessionsResponse.EResponse
    k_eTooBusy: CMsgClientToGCGetAvailablePrivateCoachingSessionsResponse.EResponse
    k_eDisabled: CMsgClientToGCGetAvailablePrivateCoachingSessionsResponse.EResponse
    k_eTimeout: CMsgClientToGCGetAvailablePrivateCoachingSessionsResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_SESSIONS_LIST_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCGetAvailablePrivateCoachingSessionsResponse.EResponse
    available_sessions_list: CMsgAvailablePrivateCoachingSessionList
    def __init__(
        self,
        result: CMsgClientToGCGetAvailablePrivateCoachingSessionsResponse.EResponse
        | str
        | None = ...,
        available_sessions_list: CMsgAvailablePrivateCoachingSessionList | _Mapping | None = ...,
    ) -> None: ...

class CMsgClientToGCGetAvailablePrivateCoachingSessionsSummary(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCGetAvailablePrivateCoachingSessionsSummaryResponse(_message.Message):
    __slots__ = ("result", "coaching_session_summary")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[
            CMsgClientToGCGetAvailablePrivateCoachingSessionsSummaryResponse.EResponse
        ]
        k_eSuccess: _ClassVar[
            CMsgClientToGCGetAvailablePrivateCoachingSessionsSummaryResponse.EResponse
        ]
        k_eTooBusy: _ClassVar[
            CMsgClientToGCGetAvailablePrivateCoachingSessionsSummaryResponse.EResponse
        ]
        k_eDisabled: _ClassVar[
            CMsgClientToGCGetAvailablePrivateCoachingSessionsSummaryResponse.EResponse
        ]
        k_eTimeout: _ClassVar[
            CMsgClientToGCGetAvailablePrivateCoachingSessionsSummaryResponse.EResponse
        ]

    k_eInternalError: CMsgClientToGCGetAvailablePrivateCoachingSessionsSummaryResponse.EResponse
    k_eSuccess: CMsgClientToGCGetAvailablePrivateCoachingSessionsSummaryResponse.EResponse
    k_eTooBusy: CMsgClientToGCGetAvailablePrivateCoachingSessionsSummaryResponse.EResponse
    k_eDisabled: CMsgClientToGCGetAvailablePrivateCoachingSessionsSummaryResponse.EResponse
    k_eTimeout: CMsgClientToGCGetAvailablePrivateCoachingSessionsSummaryResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    COACHING_SESSION_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCGetAvailablePrivateCoachingSessionsSummaryResponse.EResponse
    coaching_session_summary: CMsgAvailablePrivateCoachingSessionSummary
    def __init__(
        self,
        result: CMsgClientToGCGetAvailablePrivateCoachingSessionsSummaryResponse.EResponse
        | str
        | None = ...,
        coaching_session_summary: CMsgAvailablePrivateCoachingSessionSummary
        | _Mapping
        | None = ...,
    ) -> None: ...

class CMsgClientToGCJoinPrivateCoachingSessionLobby(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse(_message.Message):
    __slots__ = ("result",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse]
        k_eNoSession: _ClassVar[CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse]
        k_eSessionFinished: _ClassVar[
            CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse
        ]
        k_eAlreadyLeft: _ClassVar[CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse]
        k_eNotACoach: _ClassVar[CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse]
        k_eNoLobby: _ClassVar[CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse]
        k_eCoachInThisLobby: _ClassVar[
            CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse
        ]
        k_eCoachInALobby: _ClassVar[CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse]
        k_eLobbyIsLan: _ClassVar[CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse]
        k_eLobbyIsLeague: _ClassVar[CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse]
        k_eInvalidLobbyType: _ClassVar[
            CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse
        ]
        k_eInvalidLobbyState: _ClassVar[
            CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse
        ]
        k_eRequesterIsNotPlayer: _ClassVar[
            CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse
        ]
        k_eTooManyCoaches: _ClassVar[
            CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse
        ]
        k_eCoachWasPlayer: _ClassVar[
            CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse
        ]
        k_eJoinFailed: _ClassVar[CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse]

    k_eInternalError: CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse
    k_eSuccess: CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse
    k_eTooBusy: CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse
    k_eDisabled: CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse
    k_eTimeout: CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse
    k_eNoSession: CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse
    k_eSessionFinished: CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse
    k_eAlreadyLeft: CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse
    k_eNotACoach: CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse
    k_eNoLobby: CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse
    k_eCoachInThisLobby: CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse
    k_eCoachInALobby: CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse
    k_eLobbyIsLan: CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse
    k_eLobbyIsLeague: CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse
    k_eInvalidLobbyType: CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse
    k_eInvalidLobbyState: CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse
    k_eRequesterIsNotPlayer: CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse
    k_eTooManyCoaches: CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse
    k_eCoachWasPlayer: CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse
    k_eJoinFailed: CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse
    def __init__(
        self,
        result: CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse.EResponse | str | None = ...,
    ) -> None: ...

class CMsgClientToGCCoachFriend(_message.Message):
    __slots__ = ("target_account_id",)
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    target_account_id: int
    def __init__(self, target_account_id: int | None = ...) -> None: ...

class CMsgClientToGCCoachFriendResponse(_message.Message):
    __slots__ = ("result",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCCoachFriendResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCCoachFriendResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCCoachFriendResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCCoachFriendResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCCoachFriendResponse.EResponse]
        k_eCoachNotSubscriber: _ClassVar[CMsgClientToGCCoachFriendResponse.EResponse]
        k_eLobbyNotFound: _ClassVar[CMsgClientToGCCoachFriendResponse.EResponse]
        k_eFriendsOnBothSides: _ClassVar[CMsgClientToGCCoachFriendResponse.EResponse]
        k_eNotFriends: _ClassVar[CMsgClientToGCCoachFriendResponse.EResponse]
        k_eCoachInThisLobby: _ClassVar[CMsgClientToGCCoachFriendResponse.EResponse]
        k_eCoachInALobby: _ClassVar[CMsgClientToGCCoachFriendResponse.EResponse]
        k_eLobbyIsLan: _ClassVar[CMsgClientToGCCoachFriendResponse.EResponse]
        k_eInvalidLobbyType: _ClassVar[CMsgClientToGCCoachFriendResponse.EResponse]
        k_eInvalidLobbyState: _ClassVar[CMsgClientToGCCoachFriendResponse.EResponse]
        k_eFriendIsNotAPlayer: _ClassVar[CMsgClientToGCCoachFriendResponse.EResponse]
        k_eTooManyCoaches: _ClassVar[CMsgClientToGCCoachFriendResponse.EResponse]
        k_eCoachSwitchedTeams: _ClassVar[CMsgClientToGCCoachFriendResponse.EResponse]
        k_eLobbyIsLeague: _ClassVar[CMsgClientToGCCoachFriendResponse.EResponse]
        k_eCoachWasPlayer: _ClassVar[CMsgClientToGCCoachFriendResponse.EResponse]
        k_eRequestRejected: _ClassVar[CMsgClientToGCCoachFriendResponse.EResponse]

    k_eInternalError: CMsgClientToGCCoachFriendResponse.EResponse
    k_eSuccess: CMsgClientToGCCoachFriendResponse.EResponse
    k_eTooBusy: CMsgClientToGCCoachFriendResponse.EResponse
    k_eDisabled: CMsgClientToGCCoachFriendResponse.EResponse
    k_eTimeout: CMsgClientToGCCoachFriendResponse.EResponse
    k_eCoachNotSubscriber: CMsgClientToGCCoachFriendResponse.EResponse
    k_eLobbyNotFound: CMsgClientToGCCoachFriendResponse.EResponse
    k_eFriendsOnBothSides: CMsgClientToGCCoachFriendResponse.EResponse
    k_eNotFriends: CMsgClientToGCCoachFriendResponse.EResponse
    k_eCoachInThisLobby: CMsgClientToGCCoachFriendResponse.EResponse
    k_eCoachInALobby: CMsgClientToGCCoachFriendResponse.EResponse
    k_eLobbyIsLan: CMsgClientToGCCoachFriendResponse.EResponse
    k_eInvalidLobbyType: CMsgClientToGCCoachFriendResponse.EResponse
    k_eInvalidLobbyState: CMsgClientToGCCoachFriendResponse.EResponse
    k_eFriendIsNotAPlayer: CMsgClientToGCCoachFriendResponse.EResponse
    k_eTooManyCoaches: CMsgClientToGCCoachFriendResponse.EResponse
    k_eCoachSwitchedTeams: CMsgClientToGCCoachFriendResponse.EResponse
    k_eLobbyIsLeague: CMsgClientToGCCoachFriendResponse.EResponse
    k_eCoachWasPlayer: CMsgClientToGCCoachFriendResponse.EResponse
    k_eRequestRejected: CMsgClientToGCCoachFriendResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCCoachFriendResponse.EResponse
    def __init__(
        self, result: CMsgClientToGCCoachFriendResponse.EResponse | str | None = ...
    ) -> None: ...

class CMsgClientToGCRespondToCoachFriendRequest(_message.Message):
    __slots__ = ("coach_account_id", "response")
    COACH_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    coach_account_id: int
    response: _dota_gcmessages_common_lobby_pb2.ELobbyMemberCoachRequestState
    def __init__(
        self,
        coach_account_id: int | None = ...,
        response: _dota_gcmessages_common_lobby_pb2.ELobbyMemberCoachRequestState
        | str
        | None = ...,
    ) -> None: ...

class CMsgClientToGCRespondToCoachFriendRequestResponse(_message.Message):
    __slots__ = ("result",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCRespondToCoachFriendRequestResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCRespondToCoachFriendRequestResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCRespondToCoachFriendRequestResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCRespondToCoachFriendRequestResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCRespondToCoachFriendRequestResponse.EResponse]
        k_eLobbyNotFound: _ClassVar[CMsgClientToGCRespondToCoachFriendRequestResponse.EResponse]
        k_eInvalidLobbyState: _ClassVar[CMsgClientToGCRespondToCoachFriendRequestResponse.EResponse]
        k_eCoachNotInLobby: _ClassVar[CMsgClientToGCRespondToCoachFriendRequestResponse.EResponse]
        k_ePlayerInvalidTeam: _ClassVar[CMsgClientToGCRespondToCoachFriendRequestResponse.EResponse]
        k_eCoachInvalidTeam: _ClassVar[CMsgClientToGCRespondToCoachFriendRequestResponse.EResponse]
        k_eNoRequest: _ClassVar[CMsgClientToGCRespondToCoachFriendRequestResponse.EResponse]
        k_eInvalidResponse: _ClassVar[CMsgClientToGCRespondToCoachFriendRequestResponse.EResponse]
        k_eAlreadyResponded: _ClassVar[CMsgClientToGCRespondToCoachFriendRequestResponse.EResponse]

    k_eInternalError: CMsgClientToGCRespondToCoachFriendRequestResponse.EResponse
    k_eSuccess: CMsgClientToGCRespondToCoachFriendRequestResponse.EResponse
    k_eTooBusy: CMsgClientToGCRespondToCoachFriendRequestResponse.EResponse
    k_eDisabled: CMsgClientToGCRespondToCoachFriendRequestResponse.EResponse
    k_eTimeout: CMsgClientToGCRespondToCoachFriendRequestResponse.EResponse
    k_eLobbyNotFound: CMsgClientToGCRespondToCoachFriendRequestResponse.EResponse
    k_eInvalidLobbyState: CMsgClientToGCRespondToCoachFriendRequestResponse.EResponse
    k_eCoachNotInLobby: CMsgClientToGCRespondToCoachFriendRequestResponse.EResponse
    k_ePlayerInvalidTeam: CMsgClientToGCRespondToCoachFriendRequestResponse.EResponse
    k_eCoachInvalidTeam: CMsgClientToGCRespondToCoachFriendRequestResponse.EResponse
    k_eNoRequest: CMsgClientToGCRespondToCoachFriendRequestResponse.EResponse
    k_eInvalidResponse: CMsgClientToGCRespondToCoachFriendRequestResponse.EResponse
    k_eAlreadyResponded: CMsgClientToGCRespondToCoachFriendRequestResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgClientToGCRespondToCoachFriendRequestResponse.EResponse
    def __init__(
        self, result: CMsgClientToGCRespondToCoachFriendRequestResponse.EResponse | str | None = ...
    ) -> None: ...
