from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

import dota_shared_enums_pb2 as _dota_shared_enums_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class ETeamInviteResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TEAM_INVITE_SUCCESS: _ClassVar[ETeamInviteResult]
    TEAM_INVITE_FAILURE_INVITE_REJECTED: _ClassVar[ETeamInviteResult]
    TEAM_INVITE_FAILURE_INVITE_TIMEOUT: _ClassVar[ETeamInviteResult]
    TEAM_INVITE_ERROR_TEAM_AT_MEMBER_LIMIT: _ClassVar[ETeamInviteResult]
    TEAM_INVITE_ERROR_TEAM_LOCKED: _ClassVar[ETeamInviteResult]
    TEAM_INVITE_ERROR_INVITEE_NOT_AVAILABLE: _ClassVar[ETeamInviteResult]
    TEAM_INVITE_ERROR_INVITEE_BUSY: _ClassVar[ETeamInviteResult]
    TEAM_INVITE_ERROR_INVITEE_ALREADY_MEMBER: _ClassVar[ETeamInviteResult]
    TEAM_INVITE_ERROR_INVITEE_AT_TEAM_LIMIT: _ClassVar[ETeamInviteResult]
    TEAM_INVITE_ERROR_INVITEE_INSUFFICIENT_PLAY_TIME: _ClassVar[ETeamInviteResult]
    TEAM_INVITE_ERROR_INVITER_INVALID_ACCOUNT_TYPE: _ClassVar[ETeamInviteResult]
    TEAM_INVITE_ERROR_INVITER_NOT_ADMIN: _ClassVar[ETeamInviteResult]
    TEAM_INVITE_ERROR_INCORRECT_USER_RESPONDED: _ClassVar[ETeamInviteResult]
    TEAM_INVITE_ERROR_UNSPECIFIED: _ClassVar[ETeamInviteResult]

TEAM_INVITE_SUCCESS: ETeamInviteResult
TEAM_INVITE_FAILURE_INVITE_REJECTED: ETeamInviteResult
TEAM_INVITE_FAILURE_INVITE_TIMEOUT: ETeamInviteResult
TEAM_INVITE_ERROR_TEAM_AT_MEMBER_LIMIT: ETeamInviteResult
TEAM_INVITE_ERROR_TEAM_LOCKED: ETeamInviteResult
TEAM_INVITE_ERROR_INVITEE_NOT_AVAILABLE: ETeamInviteResult
TEAM_INVITE_ERROR_INVITEE_BUSY: ETeamInviteResult
TEAM_INVITE_ERROR_INVITEE_ALREADY_MEMBER: ETeamInviteResult
TEAM_INVITE_ERROR_INVITEE_AT_TEAM_LIMIT: ETeamInviteResult
TEAM_INVITE_ERROR_INVITEE_INSUFFICIENT_PLAY_TIME: ETeamInviteResult
TEAM_INVITE_ERROR_INVITER_INVALID_ACCOUNT_TYPE: ETeamInviteResult
TEAM_INVITE_ERROR_INVITER_NOT_ADMIN: ETeamInviteResult
TEAM_INVITE_ERROR_INCORRECT_USER_RESPONDED: ETeamInviteResult
TEAM_INVITE_ERROR_UNSPECIFIED: ETeamInviteResult

class CMsgDOTATeamInfo(_message.Message):
    __slots__ = (
        "members",
        "team_id",
        "name",
        "tag",
        "time_created",
        "pro",
        "pickup_team",
        "ugc_logo",
        "ugc_base_logo",
        "ugc_banner_logo",
        "ugc_sponsor_logo",
        "country_code",
        "url",
        "wins",
        "losses",
        "games_played_total",
        "games_played_matchmaking",
        "url_logo",
        "audit_entries",
        "region",
        "abbreviation",
        "member_stats",
        "team_stats",
        "dpc_results",
        "color_primary",
        "color_secondary",
        "team_captain",
    )
    class HeroStats(_message.Message):
        __slots__ = (
            "hero_id",
            "picks",
            "wins",
            "bans",
            "avg_kills",
            "avg_deaths",
            "avg_assists",
            "avg_gpm",
            "avg_xpm",
        )
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        PICKS_FIELD_NUMBER: _ClassVar[int]
        WINS_FIELD_NUMBER: _ClassVar[int]
        BANS_FIELD_NUMBER: _ClassVar[int]
        AVG_KILLS_FIELD_NUMBER: _ClassVar[int]
        AVG_DEATHS_FIELD_NUMBER: _ClassVar[int]
        AVG_ASSISTS_FIELD_NUMBER: _ClassVar[int]
        AVG_GPM_FIELD_NUMBER: _ClassVar[int]
        AVG_XPM_FIELD_NUMBER: _ClassVar[int]
        hero_id: int
        picks: int
        wins: int
        bans: int
        avg_kills: float
        avg_deaths: float
        avg_assists: float
        avg_gpm: float
        avg_xpm: float
        def __init__(
            self,
            hero_id: int | None = ...,
            picks: int | None = ...,
            wins: int | None = ...,
            bans: int | None = ...,
            avg_kills: float | None = ...,
            avg_deaths: float | None = ...,
            avg_assists: float | None = ...,
            avg_gpm: float | None = ...,
            avg_xpm: float | None = ...,
        ) -> None: ...

    class MemberStats(_message.Message):
        __slots__ = (
            "account_id",
            "wins_with_team",
            "losses_with_team",
            "top_heroes",
            "avg_kills",
            "avg_deaths",
            "avg_assists",
        )
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        WINS_WITH_TEAM_FIELD_NUMBER: _ClassVar[int]
        LOSSES_WITH_TEAM_FIELD_NUMBER: _ClassVar[int]
        TOP_HEROES_FIELD_NUMBER: _ClassVar[int]
        AVG_KILLS_FIELD_NUMBER: _ClassVar[int]
        AVG_DEATHS_FIELD_NUMBER: _ClassVar[int]
        AVG_ASSISTS_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        wins_with_team: int
        losses_with_team: int
        top_heroes: _containers.RepeatedCompositeFieldContainer[CMsgDOTATeamInfo.HeroStats]
        avg_kills: float
        avg_deaths: float
        avg_assists: float
        def __init__(
            self,
            account_id: int | None = ...,
            wins_with_team: int | None = ...,
            losses_with_team: int | None = ...,
            top_heroes: _Iterable[CMsgDOTATeamInfo.HeroStats | _Mapping] | None = ...,
            avg_kills: float | None = ...,
            avg_deaths: float | None = ...,
            avg_assists: float | None = ...,
        ) -> None: ...

    class TeamStats(_message.Message):
        __slots__ = (
            "played_heroes",
            "farming",
            "fighting",
            "versatility",
            "avg_kills",
            "avg_deaths",
            "avg_duration",
        )
        PLAYED_HEROES_FIELD_NUMBER: _ClassVar[int]
        FARMING_FIELD_NUMBER: _ClassVar[int]
        FIGHTING_FIELD_NUMBER: _ClassVar[int]
        VERSATILITY_FIELD_NUMBER: _ClassVar[int]
        AVG_KILLS_FIELD_NUMBER: _ClassVar[int]
        AVG_DEATHS_FIELD_NUMBER: _ClassVar[int]
        AVG_DURATION_FIELD_NUMBER: _ClassVar[int]
        played_heroes: _containers.RepeatedCompositeFieldContainer[CMsgDOTATeamInfo.HeroStats]
        farming: float
        fighting: float
        versatility: float
        avg_kills: float
        avg_deaths: float
        avg_duration: float
        def __init__(
            self,
            played_heroes: _Iterable[CMsgDOTATeamInfo.HeroStats | _Mapping] | None = ...,
            farming: float | None = ...,
            fighting: float | None = ...,
            versatility: float | None = ...,
            avg_kills: float | None = ...,
            avg_deaths: float | None = ...,
            avg_duration: float | None = ...,
        ) -> None: ...

    class DPCResult(_message.Message):
        __slots__ = ("league_id", "standing", "points", "earnings", "timestamp")
        LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
        STANDING_FIELD_NUMBER: _ClassVar[int]
        POINTS_FIELD_NUMBER: _ClassVar[int]
        EARNINGS_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        league_id: int
        standing: int
        points: int
        earnings: int
        timestamp: int
        def __init__(
            self,
            league_id: int | None = ...,
            standing: int | None = ...,
            points: int | None = ...,
            earnings: int | None = ...,
            timestamp: int | None = ...,
        ) -> None: ...

    class Member(_message.Message):
        __slots__ = ("account_id", "time_joined", "admin", "pro_name", "role", "real_name")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        TIME_JOINED_FIELD_NUMBER: _ClassVar[int]
        ADMIN_FIELD_NUMBER: _ClassVar[int]
        PRO_NAME_FIELD_NUMBER: _ClassVar[int]
        ROLE_FIELD_NUMBER: _ClassVar[int]
        REAL_NAME_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        time_joined: int
        admin: bool
        pro_name: str
        role: _dota_shared_enums_pb2.Fantasy_Roles
        real_name: str
        def __init__(
            self,
            account_id: int | None = ...,
            time_joined: int | None = ...,
            admin: bool = ...,
            pro_name: str | None = ...,
            role: _dota_shared_enums_pb2.Fantasy_Roles | str | None = ...,
            real_name: str | None = ...,
        ) -> None: ...

    class AuditEntry(_message.Message):
        __slots__ = ("audit_action", "timestamp", "account_id")
        AUDIT_ACTION_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        audit_action: int
        timestamp: int
        account_id: int
        def __init__(
            self,
            audit_action: int | None = ...,
            timestamp: int | None = ...,
            account_id: int | None = ...,
        ) -> None: ...

    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    TIME_CREATED_FIELD_NUMBER: _ClassVar[int]
    PRO_FIELD_NUMBER: _ClassVar[int]
    PICKUP_TEAM_FIELD_NUMBER: _ClassVar[int]
    UGC_LOGO_FIELD_NUMBER: _ClassVar[int]
    UGC_BASE_LOGO_FIELD_NUMBER: _ClassVar[int]
    UGC_BANNER_LOGO_FIELD_NUMBER: _ClassVar[int]
    UGC_SPONSOR_LOGO_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_CODE_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    WINS_FIELD_NUMBER: _ClassVar[int]
    LOSSES_FIELD_NUMBER: _ClassVar[int]
    GAMES_PLAYED_TOTAL_FIELD_NUMBER: _ClassVar[int]
    GAMES_PLAYED_MATCHMAKING_FIELD_NUMBER: _ClassVar[int]
    URL_LOGO_FIELD_NUMBER: _ClassVar[int]
    AUDIT_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    ABBREVIATION_FIELD_NUMBER: _ClassVar[int]
    MEMBER_STATS_FIELD_NUMBER: _ClassVar[int]
    TEAM_STATS_FIELD_NUMBER: _ClassVar[int]
    DPC_RESULTS_FIELD_NUMBER: _ClassVar[int]
    COLOR_PRIMARY_FIELD_NUMBER: _ClassVar[int]
    COLOR_SECONDARY_FIELD_NUMBER: _ClassVar[int]
    TEAM_CAPTAIN_FIELD_NUMBER: _ClassVar[int]
    members: _containers.RepeatedCompositeFieldContainer[CMsgDOTATeamInfo.Member]
    team_id: int
    name: str
    tag: str
    time_created: int
    pro: bool
    pickup_team: bool
    ugc_logo: int
    ugc_base_logo: int
    ugc_banner_logo: int
    ugc_sponsor_logo: int
    country_code: str
    url: str
    wins: int
    losses: int
    games_played_total: int
    games_played_matchmaking: int
    url_logo: str
    audit_entries: _containers.RepeatedCompositeFieldContainer[CMsgDOTATeamInfo.AuditEntry]
    region: _dota_shared_enums_pb2.ELeagueRegion
    abbreviation: str
    member_stats: _containers.RepeatedCompositeFieldContainer[CMsgDOTATeamInfo.MemberStats]
    team_stats: CMsgDOTATeamInfo.TeamStats
    dpc_results: _containers.RepeatedCompositeFieldContainer[CMsgDOTATeamInfo.DPCResult]
    color_primary: str
    color_secondary: str
    team_captain: int
    def __init__(
        self,
        members: _Iterable[CMsgDOTATeamInfo.Member | _Mapping] | None = ...,
        team_id: int | None = ...,
        name: str | None = ...,
        tag: str | None = ...,
        time_created: int | None = ...,
        pro: bool = ...,
        pickup_team: bool = ...,
        ugc_logo: int | None = ...,
        ugc_base_logo: int | None = ...,
        ugc_banner_logo: int | None = ...,
        ugc_sponsor_logo: int | None = ...,
        country_code: str | None = ...,
        url: str | None = ...,
        wins: int | None = ...,
        losses: int | None = ...,
        games_played_total: int | None = ...,
        games_played_matchmaking: int | None = ...,
        url_logo: str | None = ...,
        audit_entries: _Iterable[CMsgDOTATeamInfo.AuditEntry | _Mapping] | None = ...,
        region: _dota_shared_enums_pb2.ELeagueRegion | str | None = ...,
        abbreviation: str | None = ...,
        member_stats: _Iterable[CMsgDOTATeamInfo.MemberStats | _Mapping] | None = ...,
        team_stats: CMsgDOTATeamInfo.TeamStats | _Mapping | None = ...,
        dpc_results: _Iterable[CMsgDOTATeamInfo.DPCResult | _Mapping] | None = ...,
        color_primary: str | None = ...,
        color_secondary: str | None = ...,
        team_captain: int | None = ...,
    ) -> None: ...

class CMsgDOTATeamsInfo(_message.Message):
    __slots__ = ("league_id", "teams")
    LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    TEAMS_FIELD_NUMBER: _ClassVar[int]
    league_id: int
    teams: _containers.RepeatedCompositeFieldContainer[CMsgDOTATeamInfo]
    def __init__(
        self,
        league_id: int | None = ...,
        teams: _Iterable[CMsgDOTATeamInfo | _Mapping] | None = ...,
    ) -> None: ...

class CMsgDOTATeamInfoList(_message.Message):
    __slots__ = ("teams",)
    TEAMS_FIELD_NUMBER: _ClassVar[int]
    teams: _containers.RepeatedCompositeFieldContainer[CMsgDOTATeamInfo]
    def __init__(self, teams: _Iterable[CMsgDOTATeamInfo | _Mapping] | None = ...) -> None: ...

class CMsgDOTATeamInfoCache(_message.Message):
    __slots__ = ("cache_timestamp", "team_list")
    CACHE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TEAM_LIST_FIELD_NUMBER: _ClassVar[int]
    cache_timestamp: int
    team_list: CMsgDOTATeamInfoList
    def __init__(
        self,
        cache_timestamp: int | None = ...,
        team_list: CMsgDOTATeamInfoList | _Mapping | None = ...,
    ) -> None: ...

class CMsgDOTAMyTeamInfoRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgDOTACreateTeam(_message.Message):
    __slots__ = (
        "name",
        "tag",
        "logo",
        "base_logo",
        "banner_logo",
        "sponsor_logo",
        "country_code",
        "url",
        "pickup_team",
        "abbreviation",
    )
    NAME_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    LOGO_FIELD_NUMBER: _ClassVar[int]
    BASE_LOGO_FIELD_NUMBER: _ClassVar[int]
    BANNER_LOGO_FIELD_NUMBER: _ClassVar[int]
    SPONSOR_LOGO_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_CODE_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    PICKUP_TEAM_FIELD_NUMBER: _ClassVar[int]
    ABBREVIATION_FIELD_NUMBER: _ClassVar[int]
    name: str
    tag: str
    logo: int
    base_logo: int
    banner_logo: int
    sponsor_logo: int
    country_code: str
    url: str
    pickup_team: bool
    abbreviation: str
    def __init__(
        self,
        name: str | None = ...,
        tag: str | None = ...,
        logo: int | None = ...,
        base_logo: int | None = ...,
        banner_logo: int | None = ...,
        sponsor_logo: int | None = ...,
        country_code: str | None = ...,
        url: str | None = ...,
        pickup_team: bool = ...,
        abbreviation: str | None = ...,
    ) -> None: ...

class CMsgDOTACreateTeamResponse(_message.Message):
    __slots__ = ("result", "team_id")
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INVALID: _ClassVar[CMsgDOTACreateTeamResponse.Result]
        SUCCESS: _ClassVar[CMsgDOTACreateTeamResponse.Result]
        NAME_EMPTY: _ClassVar[CMsgDOTACreateTeamResponse.Result]
        NAME_BAD_CHARACTERS: _ClassVar[CMsgDOTACreateTeamResponse.Result]
        NAME_TAKEN: _ClassVar[CMsgDOTACreateTeamResponse.Result]
        NAME_TOO_LONG: _ClassVar[CMsgDOTACreateTeamResponse.Result]
        TAG_EMPTY: _ClassVar[CMsgDOTACreateTeamResponse.Result]
        TAG_BAD_CHARACTERS: _ClassVar[CMsgDOTACreateTeamResponse.Result]
        TAG_TAKEN: _ClassVar[CMsgDOTACreateTeamResponse.Result]
        TAG_TOO_LONG: _ClassVar[CMsgDOTACreateTeamResponse.Result]
        CREATOR_BUSY: _ClassVar[CMsgDOTACreateTeamResponse.Result]
        UNSPECIFIED_ERROR: _ClassVar[CMsgDOTACreateTeamResponse.Result]
        CREATOR_TEAM_LIMIT_REACHED: _ClassVar[CMsgDOTACreateTeamResponse.Result]
        NO_LOGO: _ClassVar[CMsgDOTACreateTeamResponse.Result]
        CREATOR_TEAM_CREATION_COOLDOWN: _ClassVar[CMsgDOTACreateTeamResponse.Result]
        LOGO_UPLOAD_FAILED: _ClassVar[CMsgDOTACreateTeamResponse.Result]
        NAME_CHANGED_TOO_RECENTLY: _ClassVar[CMsgDOTACreateTeamResponse.Result]
        CREATOR_INSUFFICIENT_LEVEL: _ClassVar[CMsgDOTACreateTeamResponse.Result]
        INVALID_ACCOUNT_TYPE: _ClassVar[CMsgDOTACreateTeamResponse.Result]

    INVALID: CMsgDOTACreateTeamResponse.Result
    SUCCESS: CMsgDOTACreateTeamResponse.Result
    NAME_EMPTY: CMsgDOTACreateTeamResponse.Result
    NAME_BAD_CHARACTERS: CMsgDOTACreateTeamResponse.Result
    NAME_TAKEN: CMsgDOTACreateTeamResponse.Result
    NAME_TOO_LONG: CMsgDOTACreateTeamResponse.Result
    TAG_EMPTY: CMsgDOTACreateTeamResponse.Result
    TAG_BAD_CHARACTERS: CMsgDOTACreateTeamResponse.Result
    TAG_TAKEN: CMsgDOTACreateTeamResponse.Result
    TAG_TOO_LONG: CMsgDOTACreateTeamResponse.Result
    CREATOR_BUSY: CMsgDOTACreateTeamResponse.Result
    UNSPECIFIED_ERROR: CMsgDOTACreateTeamResponse.Result
    CREATOR_TEAM_LIMIT_REACHED: CMsgDOTACreateTeamResponse.Result
    NO_LOGO: CMsgDOTACreateTeamResponse.Result
    CREATOR_TEAM_CREATION_COOLDOWN: CMsgDOTACreateTeamResponse.Result
    LOGO_UPLOAD_FAILED: CMsgDOTACreateTeamResponse.Result
    NAME_CHANGED_TOO_RECENTLY: CMsgDOTACreateTeamResponse.Result
    CREATOR_INSUFFICIENT_LEVEL: CMsgDOTACreateTeamResponse.Result
    INVALID_ACCOUNT_TYPE: CMsgDOTACreateTeamResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    result: CMsgDOTACreateTeamResponse.Result
    team_id: int
    def __init__(
        self,
        result: CMsgDOTACreateTeamResponse.Result | str | None = ...,
        team_id: int | None = ...,
    ) -> None: ...

class CMsgDOTAEditTeamDetails(_message.Message):
    __slots__ = (
        "team_id",
        "name",
        "tag",
        "logo",
        "base_logo",
        "banner_logo",
        "sponsor_logo",
        "country_code",
        "url",
        "in_use_by_party",
        "abbreviation",
    )
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    LOGO_FIELD_NUMBER: _ClassVar[int]
    BASE_LOGO_FIELD_NUMBER: _ClassVar[int]
    BANNER_LOGO_FIELD_NUMBER: _ClassVar[int]
    SPONSOR_LOGO_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_CODE_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    IN_USE_BY_PARTY_FIELD_NUMBER: _ClassVar[int]
    ABBREVIATION_FIELD_NUMBER: _ClassVar[int]
    team_id: int
    name: str
    tag: str
    logo: int
    base_logo: int
    banner_logo: int
    sponsor_logo: int
    country_code: str
    url: str
    in_use_by_party: bool
    abbreviation: str
    def __init__(
        self,
        team_id: int | None = ...,
        name: str | None = ...,
        tag: str | None = ...,
        logo: int | None = ...,
        base_logo: int | None = ...,
        banner_logo: int | None = ...,
        sponsor_logo: int | None = ...,
        country_code: str | None = ...,
        url: str | None = ...,
        in_use_by_party: bool = ...,
        abbreviation: str | None = ...,
    ) -> None: ...

class CMsgDOTAEditTeamDetailsResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgDOTAEditTeamDetailsResponse.Result]
        FAILURE_INVALID_ACCOUNT_TYPE: _ClassVar[CMsgDOTAEditTeamDetailsResponse.Result]
        FAILURE_NOT_MEMBER: _ClassVar[CMsgDOTAEditTeamDetailsResponse.Result]
        FAILURE_TEAM_LOCKED: _ClassVar[CMsgDOTAEditTeamDetailsResponse.Result]
        FAILURE_UNSPECIFIED_ERROR: _ClassVar[CMsgDOTAEditTeamDetailsResponse.Result]

    SUCCESS: CMsgDOTAEditTeamDetailsResponse.Result
    FAILURE_INVALID_ACCOUNT_TYPE: CMsgDOTAEditTeamDetailsResponse.Result
    FAILURE_NOT_MEMBER: CMsgDOTAEditTeamDetailsResponse.Result
    FAILURE_TEAM_LOCKED: CMsgDOTAEditTeamDetailsResponse.Result
    FAILURE_UNSPECIFIED_ERROR: CMsgDOTAEditTeamDetailsResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgDOTAEditTeamDetailsResponse.Result
    def __init__(
        self, result: CMsgDOTAEditTeamDetailsResponse.Result | str | None = ...
    ) -> None: ...

class CMsgDOTATeamInvite_InviterToGC(_message.Message):
    __slots__ = ("account_id", "team_id")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    team_id: int
    def __init__(self, account_id: int | None = ..., team_id: int | None = ...) -> None: ...

class CMsgDOTATeamInvite_GCImmediateResponseToInviter(_message.Message):
    __slots__ = ("result", "invitee_name", "required_play_time")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    INVITEE_NAME_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_PLAY_TIME_FIELD_NUMBER: _ClassVar[int]
    result: ETeamInviteResult
    invitee_name: str
    required_play_time: int
    def __init__(
        self,
        result: ETeamInviteResult | str | None = ...,
        invitee_name: str | None = ...,
        required_play_time: int | None = ...,
    ) -> None: ...

class CMsgDOTATeamInvite_GCRequestToInvitee(_message.Message):
    __slots__ = ("inviter_account_id", "team_name", "team_tag", "logo")
    INVITER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
    TEAM_TAG_FIELD_NUMBER: _ClassVar[int]
    LOGO_FIELD_NUMBER: _ClassVar[int]
    inviter_account_id: int
    team_name: str
    team_tag: str
    logo: int
    def __init__(
        self,
        inviter_account_id: int | None = ...,
        team_name: str | None = ...,
        team_tag: str | None = ...,
        logo: int | None = ...,
    ) -> None: ...

class CMsgDOTATeamInvite_InviteeResponseToGC(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: ETeamInviteResult
    def __init__(self, result: ETeamInviteResult | str | None = ...) -> None: ...

class CMsgDOTATeamInvite_GCResponseToInviter(_message.Message):
    __slots__ = ("result", "invitee_name")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    INVITEE_NAME_FIELD_NUMBER: _ClassVar[int]
    result: ETeamInviteResult
    invitee_name: str
    def __init__(
        self, result: ETeamInviteResult | str | None = ..., invitee_name: str | None = ...
    ) -> None: ...

class CMsgDOTATeamInvite_GCResponseToInvitee(_message.Message):
    __slots__ = ("result", "team_name")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
    result: ETeamInviteResult
    team_name: str
    def __init__(
        self, result: ETeamInviteResult | str | None = ..., team_name: str | None = ...
    ) -> None: ...

class CMsgDOTAKickTeamMember(_message.Message):
    __slots__ = ("account_id", "team_id")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    team_id: int
    def __init__(self, account_id: int | None = ..., team_id: int | None = ...) -> None: ...

class CMsgDOTAKickTeamMemberResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgDOTAKickTeamMemberResponse.Result]
        FAILURE_INVALID_ACCOUNT_TYPE: _ClassVar[CMsgDOTAKickTeamMemberResponse.Result]
        FAILURE_KICKER_NOT_ADMIN: _ClassVar[CMsgDOTAKickTeamMemberResponse.Result]
        FAILURE_KICKEE_NOT_MEMBER: _ClassVar[CMsgDOTAKickTeamMemberResponse.Result]
        FAILURE_TEAM_LOCKED: _ClassVar[CMsgDOTAKickTeamMemberResponse.Result]
        FAILURE_UNSPECIFIED_ERROR: _ClassVar[CMsgDOTAKickTeamMemberResponse.Result]

    SUCCESS: CMsgDOTAKickTeamMemberResponse.Result
    FAILURE_INVALID_ACCOUNT_TYPE: CMsgDOTAKickTeamMemberResponse.Result
    FAILURE_KICKER_NOT_ADMIN: CMsgDOTAKickTeamMemberResponse.Result
    FAILURE_KICKEE_NOT_MEMBER: CMsgDOTAKickTeamMemberResponse.Result
    FAILURE_TEAM_LOCKED: CMsgDOTAKickTeamMemberResponse.Result
    FAILURE_UNSPECIFIED_ERROR: CMsgDOTAKickTeamMemberResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgDOTAKickTeamMemberResponse.Result
    def __init__(
        self, result: CMsgDOTAKickTeamMemberResponse.Result | str | None = ...
    ) -> None: ...

class CMsgDOTATransferTeamAdmin(_message.Message):
    __slots__ = ("new_admin_account_id", "team_id")
    NEW_ADMIN_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    new_admin_account_id: int
    team_id: int
    def __init__(
        self, new_admin_account_id: int | None = ..., team_id: int | None = ...
    ) -> None: ...

class CMsgDOTATransferTeamAdminResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgDOTATransferTeamAdminResponse.Result]
        FAILURE_INVALID_ACCOUNT_TYPE: _ClassVar[CMsgDOTATransferTeamAdminResponse.Result]
        FAILURE_NOT_ADMIN: _ClassVar[CMsgDOTATransferTeamAdminResponse.Result]
        FAILURE_SAME_ACCOUNT: _ClassVar[CMsgDOTATransferTeamAdminResponse.Result]
        FAILURE_NOT_MEMBER: _ClassVar[CMsgDOTATransferTeamAdminResponse.Result]
        FAILURE_UNSPECIFIED_ERROR: _ClassVar[CMsgDOTATransferTeamAdminResponse.Result]

    SUCCESS: CMsgDOTATransferTeamAdminResponse.Result
    FAILURE_INVALID_ACCOUNT_TYPE: CMsgDOTATransferTeamAdminResponse.Result
    FAILURE_NOT_ADMIN: CMsgDOTATransferTeamAdminResponse.Result
    FAILURE_SAME_ACCOUNT: CMsgDOTATransferTeamAdminResponse.Result
    FAILURE_NOT_MEMBER: CMsgDOTATransferTeamAdminResponse.Result
    FAILURE_UNSPECIFIED_ERROR: CMsgDOTATransferTeamAdminResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgDOTATransferTeamAdminResponse.Result
    def __init__(
        self, result: CMsgDOTATransferTeamAdminResponse.Result | str | None = ...
    ) -> None: ...

class CMsgDOTALeaveTeam(_message.Message):
    __slots__ = ("team_id",)
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    team_id: int
    def __init__(self, team_id: int | None = ...) -> None: ...

class CMsgDOTALeaveTeamResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgDOTALeaveTeamResponse.Result]
        FAILURE_NOT_MEMBER: _ClassVar[CMsgDOTALeaveTeamResponse.Result]
        FAILURE_TEAM_LOCKED: _ClassVar[CMsgDOTALeaveTeamResponse.Result]
        FAILURE_UNSPECIFIED_ERROR: _ClassVar[CMsgDOTALeaveTeamResponse.Result]

    SUCCESS: CMsgDOTALeaveTeamResponse.Result
    FAILURE_NOT_MEMBER: CMsgDOTALeaveTeamResponse.Result
    FAILURE_TEAM_LOCKED: CMsgDOTALeaveTeamResponse.Result
    FAILURE_UNSPECIFIED_ERROR: CMsgDOTALeaveTeamResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgDOTALeaveTeamResponse.Result
    def __init__(self, result: CMsgDOTALeaveTeamResponse.Result | str | None = ...) -> None: ...

class CMsgDOTABetaParticipation(_message.Message):
    __slots__ = ("access_rights",)
    ACCESS_RIGHTS_FIELD_NUMBER: _ClassVar[int]
    access_rights: int
    def __init__(self, access_rights: int | None = ...) -> None: ...
