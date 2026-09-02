from . import steammessages_pb2 as _steammessages_pb2
from . import gcsdk_gcmessages_pb2 as _gcsdk_gcmessages_pb2
from . import dota_shared_enums_pb2 as _dota_shared_enums_pb2
from . import events_pb2 as _events_pb2
from . import dota_gcmessages_common_pb2 as _dota_gcmessages_common_pb2
from . import dota_match_metadata_pb2 as _dota_match_metadata_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ETeamFanContentStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TEAM_FAN_CONTENT_STATUS_INVALID: _ClassVar[ETeamFanContentStatus]
    TEAM_FAN_CONTENT_STATUS_PENDING: _ClassVar[ETeamFanContentStatus]
    TEAM_FAN_CONTENT_STATUS_EVALUATED: _ClassVar[ETeamFanContentStatus]

class ETeamFanContentAssetType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eFanContentAssetType_LogoPNG: _ClassVar[ETeamFanContentAssetType]
    k_eFanContentAssetType_LogoSVG: _ClassVar[ETeamFanContentAssetType]
    k_eFanContentAssetType_Logo3D: _ClassVar[ETeamFanContentAssetType]
    k_eFanContentAssetType_Players: _ClassVar[ETeamFanContentAssetType]
    k_eFanContentAssetType_Sprays: _ClassVar[ETeamFanContentAssetType]
    k_eFanContentAssetType_Wallpapers: _ClassVar[ETeamFanContentAssetType]
    k_eFanContentAssetType_Emoticons: _ClassVar[ETeamFanContentAssetType]
    k_eFanContentAssetType_VoiceLines: _ClassVar[ETeamFanContentAssetType]
    k_eFanContentAssetType_Localization: _ClassVar[ETeamFanContentAssetType]
    k_eFanContentAssetType_Banner: _ClassVar[ETeamFanContentAssetType]
    k_eFanContentAssetType_BaseLogo: _ClassVar[ETeamFanContentAssetType]

class ETeamFanContentAssetStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eFanContentAssetStatus_None: _ClassVar[ETeamFanContentAssetStatus]
    k_eFanContentAssetStatus_Approved: _ClassVar[ETeamFanContentAssetStatus]
    k_eFanContentAssetStatus_Rejected: _ClassVar[ETeamFanContentAssetStatus]

class ETalentContentStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TALENT_CONTENT_STATUS_INVALID: _ClassVar[ETalentContentStatus]
    TALENT_CONTENT_STATUS_PENDING: _ClassVar[ETalentContentStatus]
    TALENT_CONTENT_STATUS_EVALUATED: _ClassVar[ETalentContentStatus]
    TALENT_CONTENT_STATUS_REJECTED: _ClassVar[ETalentContentStatus]
    TALENT_CONTENT_STATUS_APPROVED: _ClassVar[ETalentContentStatus]

class ETalentContentAssetType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eTalentContentAssetType_Photo: _ClassVar[ETalentContentAssetType]
    k_eTalentContentAssetType_Autograph: _ClassVar[ETalentContentAssetType]
    k_eTalentContentAssetType_Voicelines: _ClassVar[ETalentContentAssetType]

class ETalentContentAssetStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eTalentContentAssetStatus_None: _ClassVar[ETalentContentAssetStatus]
    k_eTalentContentAssetStatus_Approved: _ClassVar[ETalentContentAssetStatus]
    k_eTalentContentAssetStatus_Rejected: _ClassVar[ETalentContentAssetStatus]
TEAM_FAN_CONTENT_STATUS_INVALID: ETeamFanContentStatus
TEAM_FAN_CONTENT_STATUS_PENDING: ETeamFanContentStatus
TEAM_FAN_CONTENT_STATUS_EVALUATED: ETeamFanContentStatus
k_eFanContentAssetType_LogoPNG: ETeamFanContentAssetType
k_eFanContentAssetType_LogoSVG: ETeamFanContentAssetType
k_eFanContentAssetType_Logo3D: ETeamFanContentAssetType
k_eFanContentAssetType_Players: ETeamFanContentAssetType
k_eFanContentAssetType_Sprays: ETeamFanContentAssetType
k_eFanContentAssetType_Wallpapers: ETeamFanContentAssetType
k_eFanContentAssetType_Emoticons: ETeamFanContentAssetType
k_eFanContentAssetType_VoiceLines: ETeamFanContentAssetType
k_eFanContentAssetType_Localization: ETeamFanContentAssetType
k_eFanContentAssetType_Banner: ETeamFanContentAssetType
k_eFanContentAssetType_BaseLogo: ETeamFanContentAssetType
k_eFanContentAssetStatus_None: ETeamFanContentAssetStatus
k_eFanContentAssetStatus_Approved: ETeamFanContentAssetStatus
k_eFanContentAssetStatus_Rejected: ETeamFanContentAssetStatus
TALENT_CONTENT_STATUS_INVALID: ETalentContentStatus
TALENT_CONTENT_STATUS_PENDING: ETalentContentStatus
TALENT_CONTENT_STATUS_EVALUATED: ETalentContentStatus
TALENT_CONTENT_STATUS_REJECTED: ETalentContentStatus
TALENT_CONTENT_STATUS_APPROVED: ETalentContentStatus
k_eTalentContentAssetType_Photo: ETalentContentAssetType
k_eTalentContentAssetType_Autograph: ETalentContentAssetType
k_eTalentContentAssetType_Voicelines: ETalentContentAssetType
k_eTalentContentAssetStatus_None: ETalentContentAssetStatus
k_eTalentContentAssetStatus_Approved: ETalentContentAssetStatus
k_eTalentContentAssetStatus_Rejected: ETalentContentAssetStatus

class CMsgArcanaVotes(_message.Message):
    __slots__ = ("matches", "round_time_remaining", "round_number", "voting_state", "is_current_round_calibrating", "closest_active_match_id", "event_id", "voting_start_time")
    class VotingState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FINISHED: _ClassVar[CMsgArcanaVotes.VotingState]
        IN_PROGRESS: _ClassVar[CMsgArcanaVotes.VotingState]
        IN_FUTURE: _ClassVar[CMsgArcanaVotes.VotingState]
    FINISHED: CMsgArcanaVotes.VotingState
    IN_PROGRESS: CMsgArcanaVotes.VotingState
    IN_FUTURE: CMsgArcanaVotes.VotingState
    class Match(_message.Message):
        __slots__ = ("match_id", "hero_id_0", "hero_id_1", "hero_seeding_0", "hero_seeding_1", "vote_count_0", "vote_count_1", "voting_state", "round_number", "is_votes_hidden", "calibration_time_remaining")
        MATCH_ID_FIELD_NUMBER: _ClassVar[int]
        HERO_ID_0_FIELD_NUMBER: _ClassVar[int]
        HERO_ID_1_FIELD_NUMBER: _ClassVar[int]
        HERO_SEEDING_0_FIELD_NUMBER: _ClassVar[int]
        HERO_SEEDING_1_FIELD_NUMBER: _ClassVar[int]
        VOTE_COUNT_0_FIELD_NUMBER: _ClassVar[int]
        VOTE_COUNT_1_FIELD_NUMBER: _ClassVar[int]
        VOTING_STATE_FIELD_NUMBER: _ClassVar[int]
        ROUND_NUMBER_FIELD_NUMBER: _ClassVar[int]
        IS_VOTES_HIDDEN_FIELD_NUMBER: _ClassVar[int]
        CALIBRATION_TIME_REMAINING_FIELD_NUMBER: _ClassVar[int]
        match_id: int
        hero_id_0: int
        hero_id_1: int
        hero_seeding_0: int
        hero_seeding_1: int
        vote_count_0: int
        vote_count_1: int
        voting_state: int
        round_number: int
        is_votes_hidden: bool
        calibration_time_remaining: int
        def __init__(self, match_id: _Optional[int] = ..., hero_id_0: _Optional[int] = ..., hero_id_1: _Optional[int] = ..., hero_seeding_0: _Optional[int] = ..., hero_seeding_1: _Optional[int] = ..., vote_count_0: _Optional[int] = ..., vote_count_1: _Optional[int] = ..., voting_state: _Optional[int] = ..., round_number: _Optional[int] = ..., is_votes_hidden: bool = ..., calibration_time_remaining: _Optional[int] = ...) -> None: ...
    MATCHES_FIELD_NUMBER: _ClassVar[int]
    ROUND_TIME_REMAINING_FIELD_NUMBER: _ClassVar[int]
    ROUND_NUMBER_FIELD_NUMBER: _ClassVar[int]
    VOTING_STATE_FIELD_NUMBER: _ClassVar[int]
    IS_CURRENT_ROUND_CALIBRATING_FIELD_NUMBER: _ClassVar[int]
    CLOSEST_ACTIVE_MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    VOTING_START_TIME_FIELD_NUMBER: _ClassVar[int]
    matches: _containers.RepeatedCompositeFieldContainer[CMsgArcanaVotes.Match]
    round_time_remaining: int
    round_number: int
    voting_state: int
    is_current_round_calibrating: bool
    closest_active_match_id: int
    event_id: int
    voting_start_time: int
    def __init__(self, matches: _Optional[_Iterable[_Union[CMsgArcanaVotes.Match, _Mapping]]] = ..., round_time_remaining: _Optional[int] = ..., round_number: _Optional[int] = ..., voting_state: _Optional[int] = ..., is_current_round_calibrating: bool = ..., closest_active_match_id: _Optional[int] = ..., event_id: _Optional[int] = ..., voting_start_time: _Optional[int] = ...) -> None: ...

class CMsgDOTADPCFeed(_message.Message):
    __slots__ = ("elements",)
    class EFeedElementType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FEED_SERIES_RESULT: _ClassVar[CMsgDOTADPCFeed.EFeedElementType]
        FEED_MATCH_POPULAR: _ClassVar[CMsgDOTADPCFeed.EFeedElementType]
        FEED_TEAM_UPCOMING_MATCH: _ClassVar[CMsgDOTADPCFeed.EFeedElementType]
        FEED_TEAM_LEAGUE_RESULT: _ClassVar[CMsgDOTADPCFeed.EFeedElementType]
        FEED_TEAM_ADD_PLAYER: _ClassVar[CMsgDOTADPCFeed.EFeedElementType]
        FEED_TEAM_REMOVE_PLAYER: _ClassVar[CMsgDOTADPCFeed.EFeedElementType]
        FEED_TEAM_DISBAND: _ClassVar[CMsgDOTADPCFeed.EFeedElementType]
        FEED_LEAGUE_UPCOMING: _ClassVar[CMsgDOTADPCFeed.EFeedElementType]
        FEED_LEAGUE_CONCLUDED: _ClassVar[CMsgDOTADPCFeed.EFeedElementType]
        FEED_DPC_STANDINGS: _ClassVar[CMsgDOTADPCFeed.EFeedElementType]
        FEED_ALERT_PREDICTIONS: _ClassVar[CMsgDOTADPCFeed.EFeedElementType]
        FEED_ALERT_FANTASY: _ClassVar[CMsgDOTADPCFeed.EFeedElementType]
        FEED_LEAGUE_LIVE_MATCH: _ClassVar[CMsgDOTADPCFeed.EFeedElementType]
        FEED_LEAGUE_INPROGRESS_SERIES: _ClassVar[CMsgDOTADPCFeed.EFeedElementType]
    FEED_SERIES_RESULT: CMsgDOTADPCFeed.EFeedElementType
    FEED_MATCH_POPULAR: CMsgDOTADPCFeed.EFeedElementType
    FEED_TEAM_UPCOMING_MATCH: CMsgDOTADPCFeed.EFeedElementType
    FEED_TEAM_LEAGUE_RESULT: CMsgDOTADPCFeed.EFeedElementType
    FEED_TEAM_ADD_PLAYER: CMsgDOTADPCFeed.EFeedElementType
    FEED_TEAM_REMOVE_PLAYER: CMsgDOTADPCFeed.EFeedElementType
    FEED_TEAM_DISBAND: CMsgDOTADPCFeed.EFeedElementType
    FEED_LEAGUE_UPCOMING: CMsgDOTADPCFeed.EFeedElementType
    FEED_LEAGUE_CONCLUDED: CMsgDOTADPCFeed.EFeedElementType
    FEED_DPC_STANDINGS: CMsgDOTADPCFeed.EFeedElementType
    FEED_ALERT_PREDICTIONS: CMsgDOTADPCFeed.EFeedElementType
    FEED_ALERT_FANTASY: CMsgDOTADPCFeed.EFeedElementType
    FEED_LEAGUE_LIVE_MATCH: CMsgDOTADPCFeed.EFeedElementType
    FEED_LEAGUE_INPROGRESS_SERIES: CMsgDOTADPCFeed.EFeedElementType
    class Element(_message.Message):
        __slots__ = ("type", "timestamp", "series_id", "match_id", "team_id", "account_id", "league_id", "node_id", "server_steam_id", "data_1", "data_2", "data_3", "data_4")
        TYPE_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        SERIES_ID_FIELD_NUMBER: _ClassVar[int]
        MATCH_ID_FIELD_NUMBER: _ClassVar[int]
        TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
        NODE_ID_FIELD_NUMBER: _ClassVar[int]
        SERVER_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
        DATA_1_FIELD_NUMBER: _ClassVar[int]
        DATA_2_FIELD_NUMBER: _ClassVar[int]
        DATA_3_FIELD_NUMBER: _ClassVar[int]
        DATA_4_FIELD_NUMBER: _ClassVar[int]
        type: CMsgDOTADPCFeed.EFeedElementType
        timestamp: int
        series_id: int
        match_id: int
        team_id: int
        account_id: int
        league_id: int
        node_id: int
        server_steam_id: int
        data_1: int
        data_2: int
        data_3: int
        data_4: int
        def __init__(self, type: _Optional[_Union[CMsgDOTADPCFeed.EFeedElementType, str]] = ..., timestamp: _Optional[int] = ..., series_id: _Optional[int] = ..., match_id: _Optional[int] = ..., team_id: _Optional[int] = ..., account_id: _Optional[int] = ..., league_id: _Optional[int] = ..., node_id: _Optional[int] = ..., server_steam_id: _Optional[int] = ..., data_1: _Optional[int] = ..., data_2: _Optional[int] = ..., data_3: _Optional[int] = ..., data_4: _Optional[int] = ...) -> None: ...
    ELEMENTS_FIELD_NUMBER: _ClassVar[int]
    elements: _containers.RepeatedCompositeFieldContainer[CMsgDOTADPCFeed.Element]
    def __init__(self, elements: _Optional[_Iterable[_Union[CMsgDOTADPCFeed.Element, _Mapping]]] = ...) -> None: ...

class CMsgDOTADPCUserInfo(_message.Message):
    __slots__ = ("is_plus_subscriber",)
    IS_PLUS_SUBSCRIBER_FIELD_NUMBER: _ClassVar[int]
    is_plus_subscriber: bool
    def __init__(self, is_plus_subscriber: bool = ...) -> None: ...

class CMsgDraftTrivia(_message.Message):
    __slots__ = ("has_valid_match", "match_hero_info", "match_rank_tier", "end_time", "event_id", "current_match_voted_radiant", "previous_result", "current_streak")
    class DraftTriviaHeroInfo(_message.Message):
        __slots__ = ("hero_id", "role")
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        ROLE_FIELD_NUMBER: _ClassVar[int]
        hero_id: int
        role: int
        def __init__(self, hero_id: _Optional[int] = ..., role: _Optional[int] = ...) -> None: ...
    class DraftTriviaMatchInfo(_message.Message):
        __slots__ = ("radiant_heroes", "dire_heroes")
        RADIANT_HEROES_FIELD_NUMBER: _ClassVar[int]
        DIRE_HEROES_FIELD_NUMBER: _ClassVar[int]
        radiant_heroes: _containers.RepeatedCompositeFieldContainer[CMsgDraftTrivia.DraftTriviaHeroInfo]
        dire_heroes: _containers.RepeatedCompositeFieldContainer[CMsgDraftTrivia.DraftTriviaHeroInfo]
        def __init__(self, radiant_heroes: _Optional[_Iterable[_Union[CMsgDraftTrivia.DraftTriviaHeroInfo, _Mapping]]] = ..., dire_heroes: _Optional[_Iterable[_Union[CMsgDraftTrivia.DraftTriviaHeroInfo, _Mapping]]] = ...) -> None: ...
    class PreviousResult(_message.Message):
        __slots__ = ("voted_correctly", "voted_radiant", "match_hero_info", "match_rank_tier", "end_time", "match_id")
        VOTED_CORRECTLY_FIELD_NUMBER: _ClassVar[int]
        VOTED_RADIANT_FIELD_NUMBER: _ClassVar[int]
        MATCH_HERO_INFO_FIELD_NUMBER: _ClassVar[int]
        MATCH_RANK_TIER_FIELD_NUMBER: _ClassVar[int]
        END_TIME_FIELD_NUMBER: _ClassVar[int]
        MATCH_ID_FIELD_NUMBER: _ClassVar[int]
        voted_correctly: bool
        voted_radiant: bool
        match_hero_info: CMsgDraftTrivia.DraftTriviaMatchInfo
        match_rank_tier: int
        end_time: int
        match_id: int
        def __init__(self, voted_correctly: bool = ..., voted_radiant: bool = ..., match_hero_info: _Optional[_Union[CMsgDraftTrivia.DraftTriviaMatchInfo, _Mapping]] = ..., match_rank_tier: _Optional[int] = ..., end_time: _Optional[int] = ..., match_id: _Optional[int] = ...) -> None: ...
    HAS_VALID_MATCH_FIELD_NUMBER: _ClassVar[int]
    MATCH_HERO_INFO_FIELD_NUMBER: _ClassVar[int]
    MATCH_RANK_TIER_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    CURRENT_MATCH_VOTED_RADIANT_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_RESULT_FIELD_NUMBER: _ClassVar[int]
    CURRENT_STREAK_FIELD_NUMBER: _ClassVar[int]
    has_valid_match: bool
    match_hero_info: CMsgDraftTrivia.DraftTriviaMatchInfo
    match_rank_tier: int
    end_time: int
    event_id: int
    current_match_voted_radiant: bool
    previous_result: CMsgDraftTrivia.PreviousResult
    current_streak: int
    def __init__(self, has_valid_match: bool = ..., match_hero_info: _Optional[_Union[CMsgDraftTrivia.DraftTriviaMatchInfo, _Mapping]] = ..., match_rank_tier: _Optional[int] = ..., end_time: _Optional[int] = ..., event_id: _Optional[int] = ..., current_match_voted_radiant: bool = ..., previous_result: _Optional[_Union[CMsgDraftTrivia.PreviousResult, _Mapping]] = ..., current_streak: _Optional[int] = ...) -> None: ...

class CMsgTeamFanContentAssetStatus(_message.Message):
    __slots__ = ("asset_type", "asset_index", "asset_status", "crc")
    ASSET_TYPE_FIELD_NUMBER: _ClassVar[int]
    ASSET_INDEX_FIELD_NUMBER: _ClassVar[int]
    ASSET_STATUS_FIELD_NUMBER: _ClassVar[int]
    CRC_FIELD_NUMBER: _ClassVar[int]
    asset_type: ETeamFanContentAssetType
    asset_index: int
    asset_status: ETeamFanContentAssetStatus
    crc: int
    def __init__(self, asset_type: _Optional[_Union[ETeamFanContentAssetType, str]] = ..., asset_index: _Optional[int] = ..., asset_status: _Optional[_Union[ETeamFanContentAssetStatus, str]] = ..., crc: _Optional[int] = ...) -> None: ...

class CMsgTeamFanContentAssetStatusResponse(_message.Message):
    __slots__ = ("result",)
    class EResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eSuccess: _ClassVar[CMsgTeamFanContentAssetStatusResponse.EResult]
        k_eInternalError: _ClassVar[CMsgTeamFanContentAssetStatusResponse.EResult]
    k_eSuccess: CMsgTeamFanContentAssetStatusResponse.EResult
    k_eInternalError: CMsgTeamFanContentAssetStatusResponse.EResult
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgTeamFanContentAssetStatusResponse.EResult
    def __init__(self, result: _Optional[_Union[CMsgTeamFanContentAssetStatusResponse.EResult, str]] = ...) -> None: ...

class CMsgTeamFanContentStatus(_message.Message):
    __slots__ = ("team_status_list",)
    class TeamStatus(_message.Message):
        __slots__ = ("name", "team_id", "logo_url", "status", "timestamp", "ugc_logo", "workshop_account_id", "abbreviation", "voiceline_count", "spray_count", "emoticon_count", "wallpaper_count", "comment", "comment_timestamp", "asset_status", "email_timestamp", "email_tier", "languages")
        NAME_FIELD_NUMBER: _ClassVar[int]
        TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        LOGO_URL_FIELD_NUMBER: _ClassVar[int]
        STATUS_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        UGC_LOGO_FIELD_NUMBER: _ClassVar[int]
        WORKSHOP_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        ABBREVIATION_FIELD_NUMBER: _ClassVar[int]
        VOICELINE_COUNT_FIELD_NUMBER: _ClassVar[int]
        SPRAY_COUNT_FIELD_NUMBER: _ClassVar[int]
        EMOTICON_COUNT_FIELD_NUMBER: _ClassVar[int]
        WALLPAPER_COUNT_FIELD_NUMBER: _ClassVar[int]
        COMMENT_FIELD_NUMBER: _ClassVar[int]
        COMMENT_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        ASSET_STATUS_FIELD_NUMBER: _ClassVar[int]
        EMAIL_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        EMAIL_TIER_FIELD_NUMBER: _ClassVar[int]
        LANGUAGES_FIELD_NUMBER: _ClassVar[int]
        name: str
        team_id: int
        logo_url: str
        status: ETeamFanContentStatus
        timestamp: int
        ugc_logo: int
        workshop_account_id: int
        abbreviation: str
        voiceline_count: int
        spray_count: int
        emoticon_count: int
        wallpaper_count: int
        comment: str
        comment_timestamp: int
        asset_status: _containers.RepeatedCompositeFieldContainer[CMsgTeamFanContentAssetStatus]
        email_timestamp: int
        email_tier: int
        languages: str
        def __init__(self, name: _Optional[str] = ..., team_id: _Optional[int] = ..., logo_url: _Optional[str] = ..., status: _Optional[_Union[ETeamFanContentStatus, str]] = ..., timestamp: _Optional[int] = ..., ugc_logo: _Optional[int] = ..., workshop_account_id: _Optional[int] = ..., abbreviation: _Optional[str] = ..., voiceline_count: _Optional[int] = ..., spray_count: _Optional[int] = ..., emoticon_count: _Optional[int] = ..., wallpaper_count: _Optional[int] = ..., comment: _Optional[str] = ..., comment_timestamp: _Optional[int] = ..., asset_status: _Optional[_Iterable[_Union[CMsgTeamFanContentAssetStatus, _Mapping]]] = ..., email_timestamp: _Optional[int] = ..., email_tier: _Optional[int] = ..., languages: _Optional[str] = ...) -> None: ...
    TEAM_STATUS_LIST_FIELD_NUMBER: _ClassVar[int]
    team_status_list: _containers.RepeatedCompositeFieldContainer[CMsgTeamFanContentStatus.TeamStatus]
    def __init__(self, team_status_list: _Optional[_Iterable[_Union[CMsgTeamFanContentStatus.TeamStatus, _Mapping]]] = ...) -> None: ...

class CMsgTeamFanContentAutographStatus(_message.Message):
    __slots__ = ("team_autographs",)
    class AutographStatus(_message.Message):
        __slots__ = ("pro_name", "account_id", "timestamp", "file")
        PRO_NAME_FIELD_NUMBER: _ClassVar[int]
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        FILE_FIELD_NUMBER: _ClassVar[int]
        pro_name: str
        account_id: int
        timestamp: int
        file: str
        def __init__(self, pro_name: _Optional[str] = ..., account_id: _Optional[int] = ..., timestamp: _Optional[int] = ..., file: _Optional[str] = ...) -> None: ...
    class TeamStatus(_message.Message):
        __slots__ = ("name", "team_id", "autographs", "workshop_account_id")
        NAME_FIELD_NUMBER: _ClassVar[int]
        TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        AUTOGRAPHS_FIELD_NUMBER: _ClassVar[int]
        WORKSHOP_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        name: str
        team_id: int
        autographs: _containers.RepeatedCompositeFieldContainer[CMsgTeamFanContentAutographStatus.AutographStatus]
        workshop_account_id: int
        def __init__(self, name: _Optional[str] = ..., team_id: _Optional[int] = ..., autographs: _Optional[_Iterable[_Union[CMsgTeamFanContentAutographStatus.AutographStatus, _Mapping]]] = ..., workshop_account_id: _Optional[int] = ...) -> None: ...
    TEAM_AUTOGRAPHS_FIELD_NUMBER: _ClassVar[int]
    team_autographs: _containers.RepeatedCompositeFieldContainer[CMsgTeamFanContentAutographStatus.TeamStatus]
    def __init__(self, team_autographs: _Optional[_Iterable[_Union[CMsgTeamFanContentAutographStatus.TeamStatus, _Mapping]]] = ...) -> None: ...

class CMsgTalentContentAssetStatus(_message.Message):
    __slots__ = ("asset_type", "asset_index", "asset_status", "revision")
    ASSET_TYPE_FIELD_NUMBER: _ClassVar[int]
    ASSET_INDEX_FIELD_NUMBER: _ClassVar[int]
    ASSET_STATUS_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    asset_type: ETalentContentAssetType
    asset_index: int
    asset_status: ETalentContentAssetStatus
    revision: int
    def __init__(self, asset_type: _Optional[_Union[ETalentContentAssetType, str]] = ..., asset_index: _Optional[int] = ..., asset_status: _Optional[_Union[ETalentContentAssetStatus, str]] = ..., revision: _Optional[int] = ...) -> None: ...

class CMsgTalentContentStatus(_message.Message):
    __slots__ = ("talent_status",)
    class EWorkshopItemStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eSuccess: _ClassVar[CMsgTalentContentStatus.EWorkshopItemStatus]
        k_eInvalidWorkshopId: _ClassVar[CMsgTalentContentStatus.EWorkshopItemStatus]
        k_eWrongAppId: _ClassVar[CMsgTalentContentStatus.EWorkshopItemStatus]
        k_eRevenueSharingNotFinalized: _ClassVar[CMsgTalentContentStatus.EWorkshopItemStatus]
        k_eWorkshopItemNotFound: _ClassVar[CMsgTalentContentStatus.EWorkshopItemStatus]
        k_eUnknown: _ClassVar[CMsgTalentContentStatus.EWorkshopItemStatus]
    k_eSuccess: CMsgTalentContentStatus.EWorkshopItemStatus
    k_eInvalidWorkshopId: CMsgTalentContentStatus.EWorkshopItemStatus
    k_eWrongAppId: CMsgTalentContentStatus.EWorkshopItemStatus
    k_eRevenueSharingNotFinalized: CMsgTalentContentStatus.EWorkshopItemStatus
    k_eWorkshopItemNotFound: CMsgTalentContentStatus.EWorkshopItemStatus
    k_eUnknown: CMsgTalentContentStatus.EWorkshopItemStatus
    class SubmitRevision(_message.Message):
        __slots__ = ("zip_file", "timestamp", "revision_number")
        ZIP_FILE_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        REVISION_NUMBER_FIELD_NUMBER: _ClassVar[int]
        zip_file: str
        timestamp: int
        revision_number: int
        def __init__(self, zip_file: _Optional[str] = ..., timestamp: _Optional[int] = ..., revision_number: _Optional[int] = ...) -> None: ...
    class TalentDetails(_message.Message):
        __slots__ = ("account_id", "full_name", "nickname", "workshop_item_id", "status", "asset_status", "broadcast_language", "revision", "revision_count", "workshop_item_status", "workshop_item_details")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        FULL_NAME_FIELD_NUMBER: _ClassVar[int]
        NICKNAME_FIELD_NUMBER: _ClassVar[int]
        WORKSHOP_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
        STATUS_FIELD_NUMBER: _ClassVar[int]
        ASSET_STATUS_FIELD_NUMBER: _ClassVar[int]
        BROADCAST_LANGUAGE_FIELD_NUMBER: _ClassVar[int]
        REVISION_FIELD_NUMBER: _ClassVar[int]
        REVISION_COUNT_FIELD_NUMBER: _ClassVar[int]
        WORKSHOP_ITEM_STATUS_FIELD_NUMBER: _ClassVar[int]
        WORKSHOP_ITEM_DETAILS_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        full_name: str
        nickname: str
        workshop_item_id: int
        status: ETalentContentStatus
        asset_status: _containers.RepeatedCompositeFieldContainer[CMsgTalentContentAssetStatus]
        broadcast_language: int
        revision: _containers.RepeatedCompositeFieldContainer[CMsgTalentContentStatus.SubmitRevision]
        revision_count: int
        workshop_item_status: CMsgTalentContentStatus.EWorkshopItemStatus
        workshop_item_details: str
        def __init__(self, account_id: _Optional[int] = ..., full_name: _Optional[str] = ..., nickname: _Optional[str] = ..., workshop_item_id: _Optional[int] = ..., status: _Optional[_Union[ETalentContentStatus, str]] = ..., asset_status: _Optional[_Iterable[_Union[CMsgTalentContentAssetStatus, _Mapping]]] = ..., broadcast_language: _Optional[int] = ..., revision: _Optional[_Iterable[_Union[CMsgTalentContentStatus.SubmitRevision, _Mapping]]] = ..., revision_count: _Optional[int] = ..., workshop_item_status: _Optional[_Union[CMsgTalentContentStatus.EWorkshopItemStatus, str]] = ..., workshop_item_details: _Optional[str] = ...) -> None: ...
    TALENT_STATUS_FIELD_NUMBER: _ClassVar[int]
    talent_status: _containers.RepeatedCompositeFieldContainer[CMsgTalentContentStatus.TalentDetails]
    def __init__(self, talent_status: _Optional[_Iterable[_Union[CMsgTalentContentStatus.TalentDetails, _Mapping]]] = ...) -> None: ...

class CMsgSetTalentContentResponse(_message.Message):
    __slots__ = ("result",)
    class EResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eSuccess: _ClassVar[CMsgSetTalentContentResponse.EResult]
        k_eInternalError: _ClassVar[CMsgSetTalentContentResponse.EResult]
        k_eOutOfDate: _ClassVar[CMsgSetTalentContentResponse.EResult]
    k_eSuccess: CMsgSetTalentContentResponse.EResult
    k_eInternalError: CMsgSetTalentContentResponse.EResult
    k_eOutOfDate: CMsgSetTalentContentResponse.EResult
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgSetTalentContentResponse.EResult
    def __init__(self, result: _Optional[_Union[CMsgSetTalentContentResponse.EResult, str]] = ...) -> None: ...

class CMsgDPCEvent(_message.Message):
    __slots__ = ("event", "event_type", "leagues", "registration_period", "is_event_upcoming", "is_event_completed", "event_name", "multicast_league_id", "multicast_streams", "tour", "timestamp_drop_lock", "timestamp_add_lock", "timestamp_content_deadline", "is_fantasy_enabled", "timestamp_content_review_deadline")
    class ELeagueEvent(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        EVENT_INVALID: _ClassVar[CMsgDPCEvent.ELeagueEvent]
        SPRING_2021_LEAGUE: _ClassVar[CMsgDPCEvent.ELeagueEvent]
        SPRING_2021_MAJOR: _ClassVar[CMsgDPCEvent.ELeagueEvent]
        INTERNATIONAL_2021_QUALIFIERS: _ClassVar[CMsgDPCEvent.ELeagueEvent]
        INTERNATIONAL_2021: _ClassVar[CMsgDPCEvent.ELeagueEvent]
        WINTER_2021_LEAGUE: _ClassVar[CMsgDPCEvent.ELeagueEvent]
        WINTER_2021_LEAGUE_FINALS: _ClassVar[CMsgDPCEvent.ELeagueEvent]
        SPRING_2022_LEAGUE: _ClassVar[CMsgDPCEvent.ELeagueEvent]
        SPRING_2022_MAJOR: _ClassVar[CMsgDPCEvent.ELeagueEvent]
        SUMMER_2022_LEAGUE: _ClassVar[CMsgDPCEvent.ELeagueEvent]
        SUMMER_2022_MAJOR: _ClassVar[CMsgDPCEvent.ELeagueEvent]
        INTERNATIONAL_2022: _ClassVar[CMsgDPCEvent.ELeagueEvent]
        CHINA_REGIONAL_FINALS: _ClassVar[CMsgDPCEvent.ELeagueEvent]
        INTERNATIONAL_2022_REGIONAL_QUALIFIERS: _ClassVar[CMsgDPCEvent.ELeagueEvent]
        INTERNATIONAL_2022_LAST_CHANCE_QUALIFIERS: _ClassVar[CMsgDPCEvent.ELeagueEvent]
        WINTER_2023_LEAGUE: _ClassVar[CMsgDPCEvent.ELeagueEvent]
        WINTER_2023_MAJOR: _ClassVar[CMsgDPCEvent.ELeagueEvent]
        SPRING_2023_LEAGUE: _ClassVar[CMsgDPCEvent.ELeagueEvent]
        SPRING_2023_MAJOR: _ClassVar[CMsgDPCEvent.ELeagueEvent]
        SUMMER_2023_LEAGUE: _ClassVar[CMsgDPCEvent.ELeagueEvent]
        SUMMER_2023_MAJOR: _ClassVar[CMsgDPCEvent.ELeagueEvent]
        INTERNATIONAL_2023: _ClassVar[CMsgDPCEvent.ELeagueEvent]
        INTERNATIONAL_2024: _ClassVar[CMsgDPCEvent.ELeagueEvent]
        INTERNATIONAL_2025: _ClassVar[CMsgDPCEvent.ELeagueEvent]
    EVENT_INVALID: CMsgDPCEvent.ELeagueEvent
    SPRING_2021_LEAGUE: CMsgDPCEvent.ELeagueEvent
    SPRING_2021_MAJOR: CMsgDPCEvent.ELeagueEvent
    INTERNATIONAL_2021_QUALIFIERS: CMsgDPCEvent.ELeagueEvent
    INTERNATIONAL_2021: CMsgDPCEvent.ELeagueEvent
    WINTER_2021_LEAGUE: CMsgDPCEvent.ELeagueEvent
    WINTER_2021_LEAGUE_FINALS: CMsgDPCEvent.ELeagueEvent
    SPRING_2022_LEAGUE: CMsgDPCEvent.ELeagueEvent
    SPRING_2022_MAJOR: CMsgDPCEvent.ELeagueEvent
    SUMMER_2022_LEAGUE: CMsgDPCEvent.ELeagueEvent
    SUMMER_2022_MAJOR: CMsgDPCEvent.ELeagueEvent
    INTERNATIONAL_2022: CMsgDPCEvent.ELeagueEvent
    CHINA_REGIONAL_FINALS: CMsgDPCEvent.ELeagueEvent
    INTERNATIONAL_2022_REGIONAL_QUALIFIERS: CMsgDPCEvent.ELeagueEvent
    INTERNATIONAL_2022_LAST_CHANCE_QUALIFIERS: CMsgDPCEvent.ELeagueEvent
    WINTER_2023_LEAGUE: CMsgDPCEvent.ELeagueEvent
    WINTER_2023_MAJOR: CMsgDPCEvent.ELeagueEvent
    SPRING_2023_LEAGUE: CMsgDPCEvent.ELeagueEvent
    SPRING_2023_MAJOR: CMsgDPCEvent.ELeagueEvent
    SUMMER_2023_LEAGUE: CMsgDPCEvent.ELeagueEvent
    SUMMER_2023_MAJOR: CMsgDPCEvent.ELeagueEvent
    INTERNATIONAL_2023: CMsgDPCEvent.ELeagueEvent
    INTERNATIONAL_2024: CMsgDPCEvent.ELeagueEvent
    INTERNATIONAL_2025: CMsgDPCEvent.ELeagueEvent
    class ELeagueEventPhase(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PHASE_INVALID: _ClassVar[CMsgDPCEvent.ELeagueEventPhase]
        WILD_CARD: _ClassVar[CMsgDPCEvent.ELeagueEventPhase]
        GROUP_STAGE: _ClassVar[CMsgDPCEvent.ELeagueEventPhase]
        GROUP_A: _ClassVar[CMsgDPCEvent.ELeagueEventPhase]
        GROUP_B: _ClassVar[CMsgDPCEvent.ELeagueEventPhase]
        OVERALL: _ClassVar[CMsgDPCEvent.ELeagueEventPhase]
        PLAYOFF: _ClassVar[CMsgDPCEvent.ELeagueEventPhase]
        RESULTS: _ClassVar[CMsgDPCEvent.ELeagueEventPhase]
        DPC_POINT_STANDINGS: _ClassVar[CMsgDPCEvent.ELeagueEventPhase]
        GROUP_C: _ClassVar[CMsgDPCEvent.ELeagueEventPhase]
        GROUP_D: _ClassVar[CMsgDPCEvent.ELeagueEventPhase]
        PLACEMENT: _ClassVar[CMsgDPCEvent.ELeagueEventPhase]
    PHASE_INVALID: CMsgDPCEvent.ELeagueEventPhase
    WILD_CARD: CMsgDPCEvent.ELeagueEventPhase
    GROUP_STAGE: CMsgDPCEvent.ELeagueEventPhase
    GROUP_A: CMsgDPCEvent.ELeagueEventPhase
    GROUP_B: CMsgDPCEvent.ELeagueEventPhase
    OVERALL: CMsgDPCEvent.ELeagueEventPhase
    PLAYOFF: CMsgDPCEvent.ELeagueEventPhase
    RESULTS: CMsgDPCEvent.ELeagueEventPhase
    DPC_POINT_STANDINGS: CMsgDPCEvent.ELeagueEventPhase
    GROUP_C: CMsgDPCEvent.ELeagueEventPhase
    GROUP_D: CMsgDPCEvent.ELeagueEventPhase
    PLACEMENT: CMsgDPCEvent.ELeagueEventPhase
    class ELeagueEventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[CMsgDPCEvent.ELeagueEventType]
        LEAGUE: _ClassVar[CMsgDPCEvent.ELeagueEventType]
        MAJOR: _ClassVar[CMsgDPCEvent.ELeagueEventType]
        INTERNATIONAL_QUALIFIERS: _ClassVar[CMsgDPCEvent.ELeagueEventType]
        INTERNATIONAL: _ClassVar[CMsgDPCEvent.ELeagueEventType]
        LEAGUE_FINALS: _ClassVar[CMsgDPCEvent.ELeagueEventType]
        EXTERNAL: _ClassVar[CMsgDPCEvent.ELeagueEventType]
    UNKNOWN: CMsgDPCEvent.ELeagueEventType
    LEAGUE: CMsgDPCEvent.ELeagueEventType
    MAJOR: CMsgDPCEvent.ELeagueEventType
    INTERNATIONAL_QUALIFIERS: CMsgDPCEvent.ELeagueEventType
    INTERNATIONAL: CMsgDPCEvent.ELeagueEventType
    LEAGUE_FINALS: CMsgDPCEvent.ELeagueEventType
    EXTERNAL: CMsgDPCEvent.ELeagueEventType
    class ETour(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TOUR_NONE: _ClassVar[CMsgDPCEvent.ETour]
        TOUR_1: _ClassVar[CMsgDPCEvent.ETour]
        TOUR_2: _ClassVar[CMsgDPCEvent.ETour]
        TOUR_3: _ClassVar[CMsgDPCEvent.ETour]
    TOUR_NONE: CMsgDPCEvent.ETour
    TOUR_1: CMsgDPCEvent.ETour
    TOUR_2: CMsgDPCEvent.ETour
    TOUR_3: CMsgDPCEvent.ETour
    class PhaseInfo(_message.Message):
        __slots__ = ("phase", "node_group_id")
        PHASE_FIELD_NUMBER: _ClassVar[int]
        NODE_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
        phase: CMsgDPCEvent.ELeagueEventPhase
        node_group_id: int
        def __init__(self, phase: _Optional[_Union[CMsgDPCEvent.ELeagueEventPhase, str]] = ..., node_group_id: _Optional[int] = ...) -> None: ...
    class League(_message.Message):
        __slots__ = ("region", "division", "league_id", "phases")
        REGION_FIELD_NUMBER: _ClassVar[int]
        DIVISION_FIELD_NUMBER: _ClassVar[int]
        LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
        PHASES_FIELD_NUMBER: _ClassVar[int]
        region: _dota_shared_enums_pb2.ELeagueRegion
        division: _dota_shared_enums_pb2.ELeagueDivision
        league_id: int
        phases: _containers.RepeatedCompositeFieldContainer[CMsgDPCEvent.PhaseInfo]
        def __init__(self, region: _Optional[_Union[_dota_shared_enums_pb2.ELeagueRegion, str]] = ..., division: _Optional[_Union[_dota_shared_enums_pb2.ELeagueDivision, str]] = ..., league_id: _Optional[int] = ..., phases: _Optional[_Iterable[_Union[CMsgDPCEvent.PhaseInfo, _Mapping]]] = ...) -> None: ...
    EVENT_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    LEAGUES_FIELD_NUMBER: _ClassVar[int]
    REGISTRATION_PERIOD_FIELD_NUMBER: _ClassVar[int]
    IS_EVENT_UPCOMING_FIELD_NUMBER: _ClassVar[int]
    IS_EVENT_COMPLETED_FIELD_NUMBER: _ClassVar[int]
    EVENT_NAME_FIELD_NUMBER: _ClassVar[int]
    MULTICAST_LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    MULTICAST_STREAMS_FIELD_NUMBER: _ClassVar[int]
    TOUR_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_DROP_LOCK_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_ADD_LOCK_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_CONTENT_DEADLINE_FIELD_NUMBER: _ClassVar[int]
    IS_FANTASY_ENABLED_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_CONTENT_REVIEW_DEADLINE_FIELD_NUMBER: _ClassVar[int]
    event: CMsgDPCEvent.ELeagueEvent
    event_type: CMsgDPCEvent.ELeagueEventType
    leagues: _containers.RepeatedCompositeFieldContainer[CMsgDPCEvent.League]
    registration_period: int
    is_event_upcoming: bool
    is_event_completed: bool
    event_name: str
    multicast_league_id: int
    multicast_streams: _containers.RepeatedScalarFieldContainer[int]
    tour: CMsgDPCEvent.ETour
    timestamp_drop_lock: int
    timestamp_add_lock: int
    timestamp_content_deadline: int
    is_fantasy_enabled: bool
    timestamp_content_review_deadline: int
    def __init__(self, event: _Optional[_Union[CMsgDPCEvent.ELeagueEvent, str]] = ..., event_type: _Optional[_Union[CMsgDPCEvent.ELeagueEventType, str]] = ..., leagues: _Optional[_Iterable[_Union[CMsgDPCEvent.League, _Mapping]]] = ..., registration_period: _Optional[int] = ..., is_event_upcoming: bool = ..., is_event_completed: bool = ..., event_name: _Optional[str] = ..., multicast_league_id: _Optional[int] = ..., multicast_streams: _Optional[_Iterable[int]] = ..., tour: _Optional[_Union[CMsgDPCEvent.ETour, str]] = ..., timestamp_drop_lock: _Optional[int] = ..., timestamp_add_lock: _Optional[int] = ..., timestamp_content_deadline: _Optional[int] = ..., is_fantasy_enabled: bool = ..., timestamp_content_review_deadline: _Optional[int] = ...) -> None: ...

class CMsgDPCEventList(_message.Message):
    __slots__ = ("events",)
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[CMsgDPCEvent]
    def __init__(self, events: _Optional[_Iterable[_Union[CMsgDPCEvent, _Mapping]]] = ...) -> None: ...

class CMsgDOTAFantasyCardLineup(_message.Message):
    __slots__ = ("periods",)
    class CardBonus(_message.Message):
        __slots__ = ("bonus_stat", "bonus_value")
        BONUS_STAT_FIELD_NUMBER: _ClassVar[int]
        BONUS_VALUE_FIELD_NUMBER: _ClassVar[int]
        bonus_stat: int
        bonus_value: int
        def __init__(self, bonus_stat: _Optional[int] = ..., bonus_value: _Optional[int] = ...) -> None: ...
    class Card(_message.Message):
        __slots__ = ("player_account_id", "player_name", "team_id", "team_name", "role", "bonuses", "score", "finalized", "item_id")
        PLAYER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        PLAYER_NAME_FIELD_NUMBER: _ClassVar[int]
        TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
        ROLE_FIELD_NUMBER: _ClassVar[int]
        BONUSES_FIELD_NUMBER: _ClassVar[int]
        SCORE_FIELD_NUMBER: _ClassVar[int]
        FINALIZED_FIELD_NUMBER: _ClassVar[int]
        ITEM_ID_FIELD_NUMBER: _ClassVar[int]
        player_account_id: int
        player_name: str
        team_id: int
        team_name: str
        role: int
        bonuses: _containers.RepeatedCompositeFieldContainer[CMsgDOTAFantasyCardLineup.CardBonus]
        score: float
        finalized: bool
        item_id: int
        def __init__(self, player_account_id: _Optional[int] = ..., player_name: _Optional[str] = ..., team_id: _Optional[int] = ..., team_name: _Optional[str] = ..., role: _Optional[int] = ..., bonuses: _Optional[_Iterable[_Union[CMsgDOTAFantasyCardLineup.CardBonus, _Mapping]]] = ..., score: _Optional[float] = ..., finalized: bool = ..., item_id: _Optional[int] = ...) -> None: ...
    class League(_message.Message):
        __slots__ = ("league_id", "cards", "score")
        LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
        CARDS_FIELD_NUMBER: _ClassVar[int]
        SCORE_FIELD_NUMBER: _ClassVar[int]
        league_id: int
        cards: _containers.RepeatedCompositeFieldContainer[CMsgDOTAFantasyCardLineup.Card]
        score: float
        def __init__(self, league_id: _Optional[int] = ..., cards: _Optional[_Iterable[_Union[CMsgDOTAFantasyCardLineup.Card, _Mapping]]] = ..., score: _Optional[float] = ...) -> None: ...
    class Period(_message.Message):
        __slots__ = ("fantasy_period", "timestamp_start", "timestamp_end", "leagues")
        FANTASY_PERIOD_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_START_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_END_FIELD_NUMBER: _ClassVar[int]
        LEAGUES_FIELD_NUMBER: _ClassVar[int]
        fantasy_period: int
        timestamp_start: int
        timestamp_end: int
        leagues: _containers.RepeatedCompositeFieldContainer[CMsgDOTAFantasyCardLineup.League]
        def __init__(self, fantasy_period: _Optional[int] = ..., timestamp_start: _Optional[int] = ..., timestamp_end: _Optional[int] = ..., leagues: _Optional[_Iterable[_Union[CMsgDOTAFantasyCardLineup.League, _Mapping]]] = ...) -> None: ...
    PERIODS_FIELD_NUMBER: _ClassVar[int]
    periods: _containers.RepeatedCompositeFieldContainer[CMsgDOTAFantasyCardLineup.Period]
    def __init__(self, periods: _Optional[_Iterable[_Union[CMsgDOTAFantasyCardLineup.Period, _Mapping]]] = ...) -> None: ...

class CMsgDOTAFantasyCardList(_message.Message):
    __slots__ = ("cards",)
    class CardBonus(_message.Message):
        __slots__ = ("bonus_stat", "bonus_value")
        BONUS_STAT_FIELD_NUMBER: _ClassVar[int]
        BONUS_VALUE_FIELD_NUMBER: _ClassVar[int]
        bonus_stat: int
        bonus_value: int
        def __init__(self, bonus_stat: _Optional[int] = ..., bonus_value: _Optional[int] = ...) -> None: ...
    class Card(_message.Message):
        __slots__ = ("player_account_id", "player_name", "team_id", "team_name", "role", "bonuses", "item_id")
        PLAYER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        PLAYER_NAME_FIELD_NUMBER: _ClassVar[int]
        TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
        ROLE_FIELD_NUMBER: _ClassVar[int]
        BONUSES_FIELD_NUMBER: _ClassVar[int]
        ITEM_ID_FIELD_NUMBER: _ClassVar[int]
        player_account_id: int
        player_name: str
        team_id: int
        team_name: str
        role: int
        bonuses: _containers.RepeatedCompositeFieldContainer[CMsgDOTAFantasyCardList.CardBonus]
        item_id: int
        def __init__(self, player_account_id: _Optional[int] = ..., player_name: _Optional[str] = ..., team_id: _Optional[int] = ..., team_name: _Optional[str] = ..., role: _Optional[int] = ..., bonuses: _Optional[_Iterable[_Union[CMsgDOTAFantasyCardList.CardBonus, _Mapping]]] = ..., item_id: _Optional[int] = ...) -> None: ...
    CARDS_FIELD_NUMBER: _ClassVar[int]
    cards: _containers.RepeatedCompositeFieldContainer[CMsgDOTAFantasyCardList.Card]
    def __init__(self, cards: _Optional[_Iterable[_Union[CMsgDOTAFantasyCardList.Card, _Mapping]]] = ...) -> None: ...

class CMsgChatToxicityToxicPlayerMatchesReport(_message.Message):
    __slots__ = ("rows",)
    class IndividualRow(_message.Message):
        __slots__ = ("player_account_id", "num_matches_seen", "num_messages", "num_messages_toxic", "first_match_seen", "last_match_seen")
        PLAYER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        NUM_MATCHES_SEEN_FIELD_NUMBER: _ClassVar[int]
        NUM_MESSAGES_FIELD_NUMBER: _ClassVar[int]
        NUM_MESSAGES_TOXIC_FIELD_NUMBER: _ClassVar[int]
        FIRST_MATCH_SEEN_FIELD_NUMBER: _ClassVar[int]
        LAST_MATCH_SEEN_FIELD_NUMBER: _ClassVar[int]
        player_account_id: int
        num_matches_seen: int
        num_messages: int
        num_messages_toxic: int
        first_match_seen: int
        last_match_seen: int
        def __init__(self, player_account_id: _Optional[int] = ..., num_matches_seen: _Optional[int] = ..., num_messages: _Optional[int] = ..., num_messages_toxic: _Optional[int] = ..., first_match_seen: _Optional[int] = ..., last_match_seen: _Optional[int] = ...) -> None: ...
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[CMsgChatToxicityToxicPlayerMatchesReport.IndividualRow]
    def __init__(self, rows: _Optional[_Iterable[_Union[CMsgChatToxicityToxicPlayerMatchesReport.IndividualRow, _Mapping]]] = ...) -> None: ...

class CMsgChatToxicityReport(_message.Message):
    __slots__ = ("num_matches_seen", "num_messages", "num_messages_ml_thinks_toxic", "status", "result", "message")
    NUM_MATCHES_SEEN_FIELD_NUMBER: _ClassVar[int]
    NUM_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    NUM_MESSAGES_ML_THINKS_TOXIC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    num_matches_seen: int
    num_messages: int
    num_messages_ml_thinks_toxic: int
    status: str
    result: int
    message: str
    def __init__(self, num_matches_seen: _Optional[int] = ..., num_messages: _Optional[int] = ..., num_messages_ml_thinks_toxic: _Optional[int] = ..., status: _Optional[str] = ..., result: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class CMsgGetTeamAuditInformation(_message.Message):
    __slots__ = ("team_id", "team_name", "actions", "last_updated")
    class Action(_message.Message):
        __slots__ = ("registration_period", "account_id", "action", "timestamp", "player_name", "player_real_name")
        REGISTRATION_PERIOD_FIELD_NUMBER: _ClassVar[int]
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        ACTION_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        PLAYER_NAME_FIELD_NUMBER: _ClassVar[int]
        PLAYER_REAL_NAME_FIELD_NUMBER: _ClassVar[int]
        registration_period: int
        account_id: int
        action: int
        timestamp: int
        player_name: str
        player_real_name: str
        def __init__(self, registration_period: _Optional[int] = ..., account_id: _Optional[int] = ..., action: _Optional[int] = ..., timestamp: _Optional[int] = ..., player_name: _Optional[str] = ..., player_real_name: _Optional[str] = ...) -> None: ...
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_FIELD_NUMBER: _ClassVar[int]
    team_id: int
    team_name: str
    actions: _containers.RepeatedCompositeFieldContainer[CMsgGetTeamAuditInformation.Action]
    last_updated: int
    def __init__(self, team_id: _Optional[int] = ..., team_name: _Optional[str] = ..., actions: _Optional[_Iterable[_Union[CMsgGetTeamAuditInformation.Action, _Mapping]]] = ..., last_updated: _Optional[int] = ...) -> None: ...

class CMsgDOTADPCMatch(_message.Message):
    __slots__ = ("match", "metadata")
    MATCH_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    match: _dota_gcmessages_common_pb2.CMsgDOTAMatch
    metadata: _dota_match_metadata_pb2.CDOTAMatchMetadata
    def __init__(self, match: _Optional[_Union[_dota_gcmessages_common_pb2.CMsgDOTAMatch, _Mapping]] = ..., metadata: _Optional[_Union[_dota_match_metadata_pb2.CDOTAMatchMetadata, _Mapping]] = ...) -> None: ...
