from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

import dota_gcmessages_common_pb2 as _dota_gcmessages_common_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class CSourceTVGameSmall(_message.Message):
    __slots__ = (
        "activate_time",
        "deactivate_time",
        "server_steam_id",
        "lobby_id",
        "league_id",
        "lobby_type",
        "game_time",
        "delay",
        "spectators",
        "game_mode",
        "average_mmr",
        "match_id",
        "series_id",
        "team_name_radiant",
        "team_name_dire",
        "team_logo_radiant",
        "team_logo_dire",
        "team_id_radiant",
        "team_id_dire",
        "sort_score",
        "last_update_time",
        "radiant_lead",
        "radiant_score",
        "dire_score",
        "players",
        "building_state",
        "weekend_tourney_tournament_id",
        "weekend_tourney_division",
        "weekend_tourney_skill_level",
        "weekend_tourney_bracket_round",
        "custom_game_difficulty",
        "is_player_draft",
        "is_watch_eligible",
    )
    class Player(_message.Message):
        __slots__ = ("account_id", "hero_id", "team_slot", "team")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        TEAM_SLOT_FIELD_NUMBER: _ClassVar[int]
        TEAM_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        hero_id: int
        team_slot: int
        team: int
        def __init__(
            self,
            account_id: int | None = ...,
            hero_id: int | None = ...,
            team_slot: int | None = ...,
            team: int | None = ...,
        ) -> None: ...

    ACTIVATE_TIME_FIELD_NUMBER: _ClassVar[int]
    DEACTIVATE_TIME_FIELD_NUMBER: _ClassVar[int]
    SERVER_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    LOBBY_ID_FIELD_NUMBER: _ClassVar[int]
    LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    LOBBY_TYPE_FIELD_NUMBER: _ClassVar[int]
    GAME_TIME_FIELD_NUMBER: _ClassVar[int]
    DELAY_FIELD_NUMBER: _ClassVar[int]
    SPECTATORS_FIELD_NUMBER: _ClassVar[int]
    GAME_MODE_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_MMR_FIELD_NUMBER: _ClassVar[int]
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    SERIES_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_NAME_RADIANT_FIELD_NUMBER: _ClassVar[int]
    TEAM_NAME_DIRE_FIELD_NUMBER: _ClassVar[int]
    TEAM_LOGO_RADIANT_FIELD_NUMBER: _ClassVar[int]
    TEAM_LOGO_DIRE_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_RADIANT_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_DIRE_FIELD_NUMBER: _ClassVar[int]
    SORT_SCORE_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    RADIANT_LEAD_FIELD_NUMBER: _ClassVar[int]
    RADIANT_SCORE_FIELD_NUMBER: _ClassVar[int]
    DIRE_SCORE_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    BUILDING_STATE_FIELD_NUMBER: _ClassVar[int]
    WEEKEND_TOURNEY_TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    WEEKEND_TOURNEY_DIVISION_FIELD_NUMBER: _ClassVar[int]
    WEEKEND_TOURNEY_SKILL_LEVEL_FIELD_NUMBER: _ClassVar[int]
    WEEKEND_TOURNEY_BRACKET_ROUND_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_DIFFICULTY_FIELD_NUMBER: _ClassVar[int]
    IS_PLAYER_DRAFT_FIELD_NUMBER: _ClassVar[int]
    IS_WATCH_ELIGIBLE_FIELD_NUMBER: _ClassVar[int]
    activate_time: int
    deactivate_time: int
    server_steam_id: int
    lobby_id: int
    league_id: int
    lobby_type: int
    game_time: int
    delay: int
    spectators: int
    game_mode: int
    average_mmr: int
    match_id: int
    series_id: int
    team_name_radiant: str
    team_name_dire: str
    team_logo_radiant: int
    team_logo_dire: int
    team_id_radiant: int
    team_id_dire: int
    sort_score: int
    last_update_time: float
    radiant_lead: int
    radiant_score: int
    dire_score: int
    players: _containers.RepeatedCompositeFieldContainer[CSourceTVGameSmall.Player]
    building_state: int
    weekend_tourney_tournament_id: int
    weekend_tourney_division: int
    weekend_tourney_skill_level: int
    weekend_tourney_bracket_round: int
    custom_game_difficulty: int
    is_player_draft: bool
    is_watch_eligible: bool
    def __init__(
        self,
        activate_time: int | None = ...,
        deactivate_time: int | None = ...,
        server_steam_id: int | None = ...,
        lobby_id: int | None = ...,
        league_id: int | None = ...,
        lobby_type: int | None = ...,
        game_time: int | None = ...,
        delay: int | None = ...,
        spectators: int | None = ...,
        game_mode: int | None = ...,
        average_mmr: int | None = ...,
        match_id: int | None = ...,
        series_id: int | None = ...,
        team_name_radiant: str | None = ...,
        team_name_dire: str | None = ...,
        team_logo_radiant: int | None = ...,
        team_logo_dire: int | None = ...,
        team_id_radiant: int | None = ...,
        team_id_dire: int | None = ...,
        sort_score: int | None = ...,
        last_update_time: float | None = ...,
        radiant_lead: int | None = ...,
        radiant_score: int | None = ...,
        dire_score: int | None = ...,
        players: _Iterable[CSourceTVGameSmall.Player | _Mapping] | None = ...,
        building_state: int | None = ...,
        weekend_tourney_tournament_id: int | None = ...,
        weekend_tourney_division: int | None = ...,
        weekend_tourney_skill_level: int | None = ...,
        weekend_tourney_bracket_round: int | None = ...,
        custom_game_difficulty: int | None = ...,
        is_player_draft: bool = ...,
        is_watch_eligible: bool = ...,
    ) -> None: ...

class CMsgClientToGCFindTopSourceTVGames(_message.Message):
    __slots__ = ("search_key", "league_id", "hero_id", "start_game", "game_list_index", "lobby_ids")
    SEARCH_KEY_FIELD_NUMBER: _ClassVar[int]
    LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    START_GAME_FIELD_NUMBER: _ClassVar[int]
    GAME_LIST_INDEX_FIELD_NUMBER: _ClassVar[int]
    LOBBY_IDS_FIELD_NUMBER: _ClassVar[int]
    search_key: str
    league_id: int
    hero_id: int
    start_game: int
    game_list_index: int
    lobby_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        search_key: str | None = ...,
        league_id: int | None = ...,
        hero_id: int | None = ...,
        start_game: int | None = ...,
        game_list_index: int | None = ...,
        lobby_ids: _Iterable[int] | None = ...,
    ) -> None: ...

class CMsgGCToClientFindTopSourceTVGamesResponse(_message.Message):
    __slots__ = (
        "search_key",
        "league_id",
        "hero_id",
        "start_game",
        "num_games",
        "game_list_index",
        "game_list",
        "specific_games",
        "bot_game",
    )
    SEARCH_KEY_FIELD_NUMBER: _ClassVar[int]
    LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    START_GAME_FIELD_NUMBER: _ClassVar[int]
    NUM_GAMES_FIELD_NUMBER: _ClassVar[int]
    GAME_LIST_INDEX_FIELD_NUMBER: _ClassVar[int]
    GAME_LIST_FIELD_NUMBER: _ClassVar[int]
    SPECIFIC_GAMES_FIELD_NUMBER: _ClassVar[int]
    BOT_GAME_FIELD_NUMBER: _ClassVar[int]
    search_key: str
    league_id: int
    hero_id: int
    start_game: int
    num_games: int
    game_list_index: int
    game_list: _containers.RepeatedCompositeFieldContainer[CSourceTVGameSmall]
    specific_games: bool
    bot_game: CSourceTVGameSmall
    def __init__(
        self,
        search_key: str | None = ...,
        league_id: int | None = ...,
        hero_id: int | None = ...,
        start_game: int | None = ...,
        num_games: int | None = ...,
        game_list_index: int | None = ...,
        game_list: _Iterable[CSourceTVGameSmall | _Mapping] | None = ...,
        specific_games: bool = ...,
        bot_game: CSourceTVGameSmall | _Mapping | None = ...,
    ) -> None: ...

class CMsgGCToClientTopWeekendTourneyGames(_message.Message):
    __slots__ = ("live_games",)
    LIVE_GAMES_FIELD_NUMBER: _ClassVar[int]
    live_games: _containers.RepeatedCompositeFieldContainer[CSourceTVGameSmall]
    def __init__(
        self, live_games: _Iterable[CSourceTVGameSmall | _Mapping] | None = ...
    ) -> None: ...

class CMsgClientToGCTopLeagueMatchesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCTopFriendMatchesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCMatchesMinimalRequest(_message.Message):
    __slots__ = ("match_ids",)
    MATCH_IDS_FIELD_NUMBER: _ClassVar[int]
    match_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, match_ids: _Iterable[int] | None = ...) -> None: ...

class CMsgClientToGCMatchesMinimalResponse(_message.Message):
    __slots__ = ("matches", "last_match")
    MATCHES_FIELD_NUMBER: _ClassVar[int]
    LAST_MATCH_FIELD_NUMBER: _ClassVar[int]
    matches: _containers.RepeatedCompositeFieldContainer[
        _dota_gcmessages_common_pb2.CMsgDOTAMatchMinimal
    ]
    last_match: bool
    def __init__(
        self,
        matches: _Iterable[_dota_gcmessages_common_pb2.CMsgDOTAMatchMinimal | _Mapping]
        | None = ...,
        last_match: bool = ...,
    ) -> None: ...

class CMsgGCToClientTopLeagueMatchesResponse(_message.Message):
    __slots__ = ("matches",)
    MATCHES_FIELD_NUMBER: _ClassVar[int]
    matches: _containers.RepeatedCompositeFieldContainer[
        _dota_gcmessages_common_pb2.CMsgDOTAMatchMinimal
    ]
    def __init__(
        self,
        matches: _Iterable[_dota_gcmessages_common_pb2.CMsgDOTAMatchMinimal | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgGCToClientTopFriendMatchesResponse(_message.Message):
    __slots__ = ("matches",)
    MATCHES_FIELD_NUMBER: _ClassVar[int]
    matches: _containers.RepeatedCompositeFieldContainer[
        _dota_gcmessages_common_pb2.CMsgDOTAMatchMinimal
    ]
    def __init__(
        self,
        matches: _Iterable[_dota_gcmessages_common_pb2.CMsgDOTAMatchMinimal | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgSpectateFriendGame(_message.Message):
    __slots__ = ("steam_id", "live")
    STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    LIVE_FIELD_NUMBER: _ClassVar[int]
    steam_id: int
    live: bool
    def __init__(self, steam_id: int | None = ..., live: bool = ...) -> None: ...

class CMsgSpectateFriendGameResponse(_message.Message):
    __slots__ = ("server_steamid", "watch_live_result")
    class EWatchLiveResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[CMsgSpectateFriendGameResponse.EWatchLiveResult]
        ERROR_GENERIC: _ClassVar[CMsgSpectateFriendGameResponse.EWatchLiveResult]
        ERROR_NO_PLUS: _ClassVar[CMsgSpectateFriendGameResponse.EWatchLiveResult]
        ERROR_NOT_FRIENDS: _ClassVar[CMsgSpectateFriendGameResponse.EWatchLiveResult]
        ERROR_LOBBY_NOT_FOUND: _ClassVar[CMsgSpectateFriendGameResponse.EWatchLiveResult]
        ERROR_SPECTATOR_IN_A_LOBBY: _ClassVar[CMsgSpectateFriendGameResponse.EWatchLiveResult]
        ERROR_LOBBY_IS_LAN: _ClassVar[CMsgSpectateFriendGameResponse.EWatchLiveResult]
        ERROR_WRONG_LOBBY_TYPE: _ClassVar[CMsgSpectateFriendGameResponse.EWatchLiveResult]
        ERROR_WRONG_LOBBY_STATE: _ClassVar[CMsgSpectateFriendGameResponse.EWatchLiveResult]
        ERROR_PLAYER_NOT_PLAYER: _ClassVar[CMsgSpectateFriendGameResponse.EWatchLiveResult]
        ERROR_TOO_MANY_SPECTATORS: _ClassVar[CMsgSpectateFriendGameResponse.EWatchLiveResult]
        ERROR_SPECTATOR_SWITCHED_TEAMS: _ClassVar[CMsgSpectateFriendGameResponse.EWatchLiveResult]
        ERROR_FRIENDS_ON_BOTH_SIDES: _ClassVar[CMsgSpectateFriendGameResponse.EWatchLiveResult]
        ERROR_SPECTATOR_IN_THIS_LOBBY: _ClassVar[CMsgSpectateFriendGameResponse.EWatchLiveResult]
        ERROR_LOBBY_IS_LEAGUE: _ClassVar[CMsgSpectateFriendGameResponse.EWatchLiveResult]

    SUCCESS: CMsgSpectateFriendGameResponse.EWatchLiveResult
    ERROR_GENERIC: CMsgSpectateFriendGameResponse.EWatchLiveResult
    ERROR_NO_PLUS: CMsgSpectateFriendGameResponse.EWatchLiveResult
    ERROR_NOT_FRIENDS: CMsgSpectateFriendGameResponse.EWatchLiveResult
    ERROR_LOBBY_NOT_FOUND: CMsgSpectateFriendGameResponse.EWatchLiveResult
    ERROR_SPECTATOR_IN_A_LOBBY: CMsgSpectateFriendGameResponse.EWatchLiveResult
    ERROR_LOBBY_IS_LAN: CMsgSpectateFriendGameResponse.EWatchLiveResult
    ERROR_WRONG_LOBBY_TYPE: CMsgSpectateFriendGameResponse.EWatchLiveResult
    ERROR_WRONG_LOBBY_STATE: CMsgSpectateFriendGameResponse.EWatchLiveResult
    ERROR_PLAYER_NOT_PLAYER: CMsgSpectateFriendGameResponse.EWatchLiveResult
    ERROR_TOO_MANY_SPECTATORS: CMsgSpectateFriendGameResponse.EWatchLiveResult
    ERROR_SPECTATOR_SWITCHED_TEAMS: CMsgSpectateFriendGameResponse.EWatchLiveResult
    ERROR_FRIENDS_ON_BOTH_SIDES: CMsgSpectateFriendGameResponse.EWatchLiveResult
    ERROR_SPECTATOR_IN_THIS_LOBBY: CMsgSpectateFriendGameResponse.EWatchLiveResult
    ERROR_LOBBY_IS_LEAGUE: CMsgSpectateFriendGameResponse.EWatchLiveResult
    SERVER_STEAMID_FIELD_NUMBER: _ClassVar[int]
    WATCH_LIVE_RESULT_FIELD_NUMBER: _ClassVar[int]
    server_steamid: int
    watch_live_result: CMsgSpectateFriendGameResponse.EWatchLiveResult
    def __init__(
        self,
        server_steamid: int | None = ...,
        watch_live_result: CMsgSpectateFriendGameResponse.EWatchLiveResult | str | None = ...,
    ) -> None: ...

class CDOTAReplayDownloadInfo(_message.Message):
    __slots__ = ("match", "title", "description", "size", "tags", "exists_on_disk")
    class Highlight(_message.Message):
        __slots__ = ("timestamp", "description")
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        timestamp: int
        description: str
        def __init__(self, timestamp: int | None = ..., description: str | None = ...) -> None: ...

    MATCH_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    EXISTS_ON_DISK_FIELD_NUMBER: _ClassVar[int]
    match: _dota_gcmessages_common_pb2.CMsgDOTAMatchMinimal
    title: str
    description: str
    size: int
    tags: _containers.RepeatedScalarFieldContainer[str]
    exists_on_disk: bool
    def __init__(
        self,
        match: _dota_gcmessages_common_pb2.CMsgDOTAMatchMinimal | _Mapping | None = ...,
        title: str | None = ...,
        description: str | None = ...,
        size: int | None = ...,
        tags: _Iterable[str] | None = ...,
        exists_on_disk: bool = ...,
    ) -> None: ...

class CMsgWatchGame(_message.Message):
    __slots__ = ("server_steamid", "client_version", "watch_server_steamid", "lobby_id", "regions")
    SERVER_STEAMID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    WATCH_SERVER_STEAMID_FIELD_NUMBER: _ClassVar[int]
    LOBBY_ID_FIELD_NUMBER: _ClassVar[int]
    REGIONS_FIELD_NUMBER: _ClassVar[int]
    server_steamid: int
    client_version: int
    watch_server_steamid: int
    lobby_id: int
    regions: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        server_steamid: int | None = ...,
        client_version: int | None = ...,
        watch_server_steamid: int | None = ...,
        lobby_id: int | None = ...,
        regions: _Iterable[int] | None = ...,
    ) -> None: ...

class CMsgCancelWatchGame(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgWatchGameResponse(_message.Message):
    __slots__ = (
        "watch_game_result",
        "source_tv_public_addr",
        "source_tv_private_addr",
        "source_tv_port",
        "game_server_steamid",
        "watch_server_steamid",
        "watch_tv_unique_secret_code",
        "broadcast_url",
    )
    class WatchGameResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PENDING: _ClassVar[CMsgWatchGameResponse.WatchGameResult]
        READY: _ClassVar[CMsgWatchGameResponse.WatchGameResult]
        GAMESERVERNOTFOUND: _ClassVar[CMsgWatchGameResponse.WatchGameResult]
        UNAVAILABLE: _ClassVar[CMsgWatchGameResponse.WatchGameResult]
        CANCELLED: _ClassVar[CMsgWatchGameResponse.WatchGameResult]
        INCOMPATIBLEVERSION: _ClassVar[CMsgWatchGameResponse.WatchGameResult]
        MISSINGLEAGUESUBSCRIPTION: _ClassVar[CMsgWatchGameResponse.WatchGameResult]
        LOBBYNOTFOUND: _ClassVar[CMsgWatchGameResponse.WatchGameResult]

    PENDING: CMsgWatchGameResponse.WatchGameResult
    READY: CMsgWatchGameResponse.WatchGameResult
    GAMESERVERNOTFOUND: CMsgWatchGameResponse.WatchGameResult
    UNAVAILABLE: CMsgWatchGameResponse.WatchGameResult
    CANCELLED: CMsgWatchGameResponse.WatchGameResult
    INCOMPATIBLEVERSION: CMsgWatchGameResponse.WatchGameResult
    MISSINGLEAGUESUBSCRIPTION: CMsgWatchGameResponse.WatchGameResult
    LOBBYNOTFOUND: CMsgWatchGameResponse.WatchGameResult
    WATCH_GAME_RESULT_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TV_PUBLIC_ADDR_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TV_PRIVATE_ADDR_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TV_PORT_FIELD_NUMBER: _ClassVar[int]
    GAME_SERVER_STEAMID_FIELD_NUMBER: _ClassVar[int]
    WATCH_SERVER_STEAMID_FIELD_NUMBER: _ClassVar[int]
    WATCH_TV_UNIQUE_SECRET_CODE_FIELD_NUMBER: _ClassVar[int]
    BROADCAST_URL_FIELD_NUMBER: _ClassVar[int]
    watch_game_result: CMsgWatchGameResponse.WatchGameResult
    source_tv_public_addr: int
    source_tv_private_addr: int
    source_tv_port: int
    game_server_steamid: int
    watch_server_steamid: int
    watch_tv_unique_secret_code: int
    broadcast_url: str
    def __init__(
        self,
        watch_game_result: CMsgWatchGameResponse.WatchGameResult | str | None = ...,
        source_tv_public_addr: int | None = ...,
        source_tv_private_addr: int | None = ...,
        source_tv_port: int | None = ...,
        game_server_steamid: int | None = ...,
        watch_server_steamid: int | None = ...,
        watch_tv_unique_secret_code: int | None = ...,
        broadcast_url: str | None = ...,
    ) -> None: ...

class CMsgPartyLeaderWatchGamePrompt(_message.Message):
    __slots__ = ("game_server_steamid",)
    GAME_SERVER_STEAMID_FIELD_NUMBER: _ClassVar[int]
    game_server_steamid: int
    def __init__(self, game_server_steamid: int | None = ...) -> None: ...

class CDOTABroadcasterInfo(_message.Message):
    __slots__ = (
        "account_id",
        "server_steam_id",
        "live",
        "team_name_radiant",
        "team_name_dire",
        "series_game",
        "upcoming_broadcast_timestamp",
        "allow_live_video",
        "node_type",
        "node_name",
    )
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SERVER_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    LIVE_FIELD_NUMBER: _ClassVar[int]
    TEAM_NAME_RADIANT_FIELD_NUMBER: _ClassVar[int]
    TEAM_NAME_DIRE_FIELD_NUMBER: _ClassVar[int]
    SERIES_GAME_FIELD_NUMBER: _ClassVar[int]
    UPCOMING_BROADCAST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ALLOW_LIVE_VIDEO_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    server_steam_id: int
    live: bool
    team_name_radiant: str
    team_name_dire: str
    series_game: int
    upcoming_broadcast_timestamp: int
    allow_live_video: bool
    node_type: int
    node_name: str
    def __init__(
        self,
        account_id: int | None = ...,
        server_steam_id: int | None = ...,
        live: bool = ...,
        team_name_radiant: str | None = ...,
        team_name_dire: str | None = ...,
        series_game: int | None = ...,
        upcoming_broadcast_timestamp: int | None = ...,
        allow_live_video: bool = ...,
        node_type: int | None = ...,
        node_name: str | None = ...,
    ) -> None: ...

class CMsgDOTASeries(_message.Message):
    __slots__ = ("series_id", "series_type", "team_1", "team_2", "match_minimal", "live_game")
    class TeamInfo(_message.Message):
        __slots__ = ("team_id", "team_name", "team_logo_url", "wager_count")
        TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
        TEAM_LOGO_URL_FIELD_NUMBER: _ClassVar[int]
        WAGER_COUNT_FIELD_NUMBER: _ClassVar[int]
        team_id: int
        team_name: str
        team_logo_url: str
        wager_count: int
        def __init__(
            self,
            team_id: int | None = ...,
            team_name: str | None = ...,
            team_logo_url: str | None = ...,
            wager_count: int | None = ...,
        ) -> None: ...

    class LiveGame(_message.Message):
        __slots__ = (
            "server_steam_id",
            "team_radiant",
            "team_dire",
            "team_radiant_score",
            "team_dire_score",
        )
        SERVER_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
        TEAM_RADIANT_FIELD_NUMBER: _ClassVar[int]
        TEAM_DIRE_FIELD_NUMBER: _ClassVar[int]
        TEAM_RADIANT_SCORE_FIELD_NUMBER: _ClassVar[int]
        TEAM_DIRE_SCORE_FIELD_NUMBER: _ClassVar[int]
        server_steam_id: int
        team_radiant: CMsgDOTASeries.TeamInfo
        team_dire: CMsgDOTASeries.TeamInfo
        team_radiant_score: int
        team_dire_score: int
        def __init__(
            self,
            server_steam_id: int | None = ...,
            team_radiant: CMsgDOTASeries.TeamInfo | _Mapping | None = ...,
            team_dire: CMsgDOTASeries.TeamInfo | _Mapping | None = ...,
            team_radiant_score: int | None = ...,
            team_dire_score: int | None = ...,
        ) -> None: ...

    SERIES_ID_FIELD_NUMBER: _ClassVar[int]
    SERIES_TYPE_FIELD_NUMBER: _ClassVar[int]
    TEAM_1_FIELD_NUMBER: _ClassVar[int]
    TEAM_2_FIELD_NUMBER: _ClassVar[int]
    MATCH_MINIMAL_FIELD_NUMBER: _ClassVar[int]
    LIVE_GAME_FIELD_NUMBER: _ClassVar[int]
    series_id: int
    series_type: int
    team_1: CMsgDOTASeries.TeamInfo
    team_2: CMsgDOTASeries.TeamInfo
    match_minimal: _containers.RepeatedCompositeFieldContainer[
        _dota_gcmessages_common_pb2.CMsgDOTAMatchMinimal
    ]
    live_game: CMsgDOTASeries.LiveGame
    def __init__(
        self,
        series_id: int | None = ...,
        series_type: int | None = ...,
        team_1: CMsgDOTASeries.TeamInfo | _Mapping | None = ...,
        team_2: CMsgDOTASeries.TeamInfo | _Mapping | None = ...,
        match_minimal: _Iterable[_dota_gcmessages_common_pb2.CMsgDOTAMatchMinimal | _Mapping]
        | None = ...,
        live_game: CMsgDOTASeries.LiveGame | _Mapping | None = ...,
    ) -> None: ...
