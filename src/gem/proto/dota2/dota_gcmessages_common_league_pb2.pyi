from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

import dota_shared_enums_pb2 as _dota_shared_enums_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class ELeagueNodeGroupType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INVALID_GROUP_TYPE: _ClassVar[ELeagueNodeGroupType]
    ORGANIZATIONAL: _ClassVar[ELeagueNodeGroupType]
    ROUND_ROBIN: _ClassVar[ELeagueNodeGroupType]
    SWISS: _ClassVar[ELeagueNodeGroupType]
    BRACKET_SINGLE: _ClassVar[ELeagueNodeGroupType]
    BRACKET_DOUBLE_SEED_LOSER: _ClassVar[ELeagueNodeGroupType]
    BRACKET_DOUBLE_ALL_WINNER: _ClassVar[ELeagueNodeGroupType]
    SHOWMATCH: _ClassVar[ELeagueNodeGroupType]
    GSL: _ClassVar[ELeagueNodeGroupType]
    PLACEMENT: _ClassVar[ELeagueNodeGroupType]

class ELeagueNodeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INVALID_NODE_TYPE: _ClassVar[ELeagueNodeType]
    BEST_OF_ONE: _ClassVar[ELeagueNodeType]
    BEST_OF_THREE: _ClassVar[ELeagueNodeType]
    BEST_OF_FIVE: _ClassVar[ELeagueNodeType]
    BEST_OF_TWO: _ClassVar[ELeagueNodeType]

INVALID_GROUP_TYPE: ELeagueNodeGroupType
ORGANIZATIONAL: ELeagueNodeGroupType
ROUND_ROBIN: ELeagueNodeGroupType
SWISS: ELeagueNodeGroupType
BRACKET_SINGLE: ELeagueNodeGroupType
BRACKET_DOUBLE_SEED_LOSER: ELeagueNodeGroupType
BRACKET_DOUBLE_ALL_WINNER: ELeagueNodeGroupType
SHOWMATCH: ELeagueNodeGroupType
GSL: ELeagueNodeGroupType
PLACEMENT: ELeagueNodeGroupType
INVALID_NODE_TYPE: ELeagueNodeType
BEST_OF_ONE: ELeagueNodeType
BEST_OF_THREE: ELeagueNodeType
BEST_OF_FIVE: ELeagueNodeType
BEST_OF_TWO: ELeagueNodeType

class CMsgDOTALeagueNode(_message.Message):
    __slots__ = (
        "name",
        "node_id",
        "node_group_id",
        "winning_node_id",
        "losing_node_id",
        "incoming_node_id_1",
        "incoming_node_id_2",
        "node_type",
        "scheduled_time",
        "actual_time",
        "series_id",
        "team_id_1",
        "team_id_2",
        "matches",
        "team_1_wins",
        "team_2_wins",
        "has_started",
        "is_completed",
        "stream_ids",
        "vods",
    )
    class MatchDetails(_message.Message):
        __slots__ = ("match_id", "winning_team_id")
        MATCH_ID_FIELD_NUMBER: _ClassVar[int]
        WINNING_TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        match_id: int
        winning_team_id: int
        def __init__(
            self, match_id: int | None = ..., winning_team_id: int | None = ...
        ) -> None: ...

    class VOD(_message.Message):
        __slots__ = ("series_game", "stream_id", "url")
        SERIES_GAME_FIELD_NUMBER: _ClassVar[int]
        STREAM_ID_FIELD_NUMBER: _ClassVar[int]
        URL_FIELD_NUMBER: _ClassVar[int]
        series_game: int
        stream_id: int
        url: str
        def __init__(
            self, series_game: int | None = ..., stream_id: int | None = ..., url: str | None = ...
        ) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    WINNING_NODE_ID_FIELD_NUMBER: _ClassVar[int]
    LOSING_NODE_ID_FIELD_NUMBER: _ClassVar[int]
    INCOMING_NODE_ID_1_FIELD_NUMBER: _ClassVar[int]
    INCOMING_NODE_ID_2_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SCHEDULED_TIME_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_TIME_FIELD_NUMBER: _ClassVar[int]
    SERIES_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_1_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_2_FIELD_NUMBER: _ClassVar[int]
    MATCHES_FIELD_NUMBER: _ClassVar[int]
    TEAM_1_WINS_FIELD_NUMBER: _ClassVar[int]
    TEAM_2_WINS_FIELD_NUMBER: _ClassVar[int]
    HAS_STARTED_FIELD_NUMBER: _ClassVar[int]
    IS_COMPLETED_FIELD_NUMBER: _ClassVar[int]
    STREAM_IDS_FIELD_NUMBER: _ClassVar[int]
    VODS_FIELD_NUMBER: _ClassVar[int]
    name: str
    node_id: int
    node_group_id: int
    winning_node_id: int
    losing_node_id: int
    incoming_node_id_1: int
    incoming_node_id_2: int
    node_type: ELeagueNodeType
    scheduled_time: int
    actual_time: int
    series_id: int
    team_id_1: int
    team_id_2: int
    matches: _containers.RepeatedCompositeFieldContainer[CMsgDOTALeagueNode.MatchDetails]
    team_1_wins: int
    team_2_wins: int
    has_started: bool
    is_completed: bool
    stream_ids: _containers.RepeatedScalarFieldContainer[int]
    vods: _containers.RepeatedCompositeFieldContainer[CMsgDOTALeagueNode.VOD]
    def __init__(
        self,
        name: str | None = ...,
        node_id: int | None = ...,
        node_group_id: int | None = ...,
        winning_node_id: int | None = ...,
        losing_node_id: int | None = ...,
        incoming_node_id_1: int | None = ...,
        incoming_node_id_2: int | None = ...,
        node_type: ELeagueNodeType | str | None = ...,
        scheduled_time: int | None = ...,
        actual_time: int | None = ...,
        series_id: int | None = ...,
        team_id_1: int | None = ...,
        team_id_2: int | None = ...,
        matches: _Iterable[CMsgDOTALeagueNode.MatchDetails | _Mapping] | None = ...,
        team_1_wins: int | None = ...,
        team_2_wins: int | None = ...,
        has_started: bool = ...,
        is_completed: bool = ...,
        stream_ids: _Iterable[int] | None = ...,
        vods: _Iterable[CMsgDOTALeagueNode.VOD | _Mapping] | None = ...,
    ) -> None: ...

class CMsgDOTALeagueNodeGroup(_message.Message):
    __slots__ = (
        "name",
        "node_group_id",
        "parent_node_group_id",
        "incoming_node_group_ids",
        "advancing_node_group_id",
        "advancing_team_count",
        "team_count",
        "node_group_type",
        "default_node_type",
        "round",
        "max_rounds",
        "win_loss_limit",
        "is_tiebreaker",
        "is_final_group",
        "is_completed",
        "phase",
        "region",
        "start_time",
        "end_time",
        "secondary_advancing_node_group_id",
        "secondary_advancing_team_count",
        "tertiary_advancing_node_group_id",
        "tertiary_advancing_team_count",
        "elimination_dpc_points",
        "team_standings",
        "nodes",
        "node_groups",
    )
    class TeamStanding(_message.Message):
        __slots__ = (
            "standing",
            "team_id",
            "team_name",
            "team_tag",
            "team_logo",
            "team_logo_url",
            "wins",
            "losses",
            "score",
            "team_abbreviation",
            "is_pro",
            "tiebreak_game_win_pct",
            "tiebreak_opponent_match_wins",
            "tiebreak_opponent_game_win_pct",
            "tiebreak_coinflip",
        )
        STANDING_FIELD_NUMBER: _ClassVar[int]
        TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
        TEAM_TAG_FIELD_NUMBER: _ClassVar[int]
        TEAM_LOGO_FIELD_NUMBER: _ClassVar[int]
        TEAM_LOGO_URL_FIELD_NUMBER: _ClassVar[int]
        WINS_FIELD_NUMBER: _ClassVar[int]
        LOSSES_FIELD_NUMBER: _ClassVar[int]
        SCORE_FIELD_NUMBER: _ClassVar[int]
        TEAM_ABBREVIATION_FIELD_NUMBER: _ClassVar[int]
        IS_PRO_FIELD_NUMBER: _ClassVar[int]
        TIEBREAK_GAME_WIN_PCT_FIELD_NUMBER: _ClassVar[int]
        TIEBREAK_OPPONENT_MATCH_WINS_FIELD_NUMBER: _ClassVar[int]
        TIEBREAK_OPPONENT_GAME_WIN_PCT_FIELD_NUMBER: _ClassVar[int]
        TIEBREAK_COINFLIP_FIELD_NUMBER: _ClassVar[int]
        standing: int
        team_id: int
        team_name: str
        team_tag: str
        team_logo: int
        team_logo_url: str
        wins: int
        losses: int
        score: int
        team_abbreviation: str
        is_pro: bool
        tiebreak_game_win_pct: int
        tiebreak_opponent_match_wins: int
        tiebreak_opponent_game_win_pct: int
        tiebreak_coinflip: int
        def __init__(
            self,
            standing: int | None = ...,
            team_id: int | None = ...,
            team_name: str | None = ...,
            team_tag: str | None = ...,
            team_logo: int | None = ...,
            team_logo_url: str | None = ...,
            wins: int | None = ...,
            losses: int | None = ...,
            score: int | None = ...,
            team_abbreviation: str | None = ...,
            is_pro: bool = ...,
            tiebreak_game_win_pct: int | None = ...,
            tiebreak_opponent_match_wins: int | None = ...,
            tiebreak_opponent_game_win_pct: int | None = ...,
            tiebreak_coinflip: int | None = ...,
        ) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_NODE_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    INCOMING_NODE_GROUP_IDS_FIELD_NUMBER: _ClassVar[int]
    ADVANCING_NODE_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    ADVANCING_TEAM_COUNT_FIELD_NUMBER: _ClassVar[int]
    TEAM_COUNT_FIELD_NUMBER: _ClassVar[int]
    NODE_GROUP_TYPE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ROUND_FIELD_NUMBER: _ClassVar[int]
    MAX_ROUNDS_FIELD_NUMBER: _ClassVar[int]
    WIN_LOSS_LIMIT_FIELD_NUMBER: _ClassVar[int]
    IS_TIEBREAKER_FIELD_NUMBER: _ClassVar[int]
    IS_FINAL_GROUP_FIELD_NUMBER: _ClassVar[int]
    IS_COMPLETED_FIELD_NUMBER: _ClassVar[int]
    PHASE_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    SECONDARY_ADVANCING_NODE_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    SECONDARY_ADVANCING_TEAM_COUNT_FIELD_NUMBER: _ClassVar[int]
    TERTIARY_ADVANCING_NODE_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    TERTIARY_ADVANCING_TEAM_COUNT_FIELD_NUMBER: _ClassVar[int]
    ELIMINATION_DPC_POINTS_FIELD_NUMBER: _ClassVar[int]
    TEAM_STANDINGS_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    NODE_GROUPS_FIELD_NUMBER: _ClassVar[int]
    name: str
    node_group_id: int
    parent_node_group_id: int
    incoming_node_group_ids: _containers.RepeatedScalarFieldContainer[int]
    advancing_node_group_id: int
    advancing_team_count: int
    team_count: int
    node_group_type: ELeagueNodeGroupType
    default_node_type: ELeagueNodeType
    round: int
    max_rounds: int
    win_loss_limit: int
    is_tiebreaker: bool
    is_final_group: bool
    is_completed: bool
    phase: _dota_shared_enums_pb2.ELeaguePhase
    region: _dota_shared_enums_pb2.ELeagueRegion
    start_time: int
    end_time: int
    secondary_advancing_node_group_id: int
    secondary_advancing_team_count: int
    tertiary_advancing_node_group_id: int
    tertiary_advancing_team_count: int
    elimination_dpc_points: int
    team_standings: _containers.RepeatedCompositeFieldContainer[
        CMsgDOTALeagueNodeGroup.TeamStanding
    ]
    nodes: _containers.RepeatedCompositeFieldContainer[CMsgDOTALeagueNode]
    node_groups: _containers.RepeatedCompositeFieldContainer[CMsgDOTALeagueNodeGroup]
    def __init__(
        self,
        name: str | None = ...,
        node_group_id: int | None = ...,
        parent_node_group_id: int | None = ...,
        incoming_node_group_ids: _Iterable[int] | None = ...,
        advancing_node_group_id: int | None = ...,
        advancing_team_count: int | None = ...,
        team_count: int | None = ...,
        node_group_type: ELeagueNodeGroupType | str | None = ...,
        default_node_type: ELeagueNodeType | str | None = ...,
        round: int | None = ...,
        max_rounds: int | None = ...,
        win_loss_limit: int | None = ...,
        is_tiebreaker: bool = ...,
        is_final_group: bool = ...,
        is_completed: bool = ...,
        phase: _dota_shared_enums_pb2.ELeaguePhase | str | None = ...,
        region: _dota_shared_enums_pb2.ELeagueRegion | str | None = ...,
        start_time: int | None = ...,
        end_time: int | None = ...,
        secondary_advancing_node_group_id: int | None = ...,
        secondary_advancing_team_count: int | None = ...,
        tertiary_advancing_node_group_id: int | None = ...,
        tertiary_advancing_team_count: int | None = ...,
        elimination_dpc_points: int | None = ...,
        team_standings: _Iterable[CMsgDOTALeagueNodeGroup.TeamStanding | _Mapping] | None = ...,
        nodes: _Iterable[CMsgDOTALeagueNode | _Mapping] | None = ...,
        node_groups: _Iterable[CMsgDOTALeagueNodeGroup | _Mapping] | None = ...,
    ) -> None: ...

class CMsgDOTALeague(_message.Message):
    __slots__ = (
        "info",
        "prize_pool",
        "admins",
        "streams",
        "node_groups",
        "series_infos",
        "registered_players",
    )
    class Info(_message.Message):
        __slots__ = (
            "league_id",
            "name",
            "tier",
            "region",
            "url",
            "description",
            "notes",
            "start_timestamp",
            "end_timestamp",
            "pro_circuit_points",
            "image_bits",
            "status",
            "most_recent_activity",
            "registration_period",
        )
        LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        TIER_FIELD_NUMBER: _ClassVar[int]
        REGION_FIELD_NUMBER: _ClassVar[int]
        URL_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        NOTES_FIELD_NUMBER: _ClassVar[int]
        START_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        END_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        PRO_CIRCUIT_POINTS_FIELD_NUMBER: _ClassVar[int]
        IMAGE_BITS_FIELD_NUMBER: _ClassVar[int]
        STATUS_FIELD_NUMBER: _ClassVar[int]
        MOST_RECENT_ACTIVITY_FIELD_NUMBER: _ClassVar[int]
        REGISTRATION_PERIOD_FIELD_NUMBER: _ClassVar[int]
        league_id: int
        name: str
        tier: _dota_shared_enums_pb2.ELeagueTier
        region: _dota_shared_enums_pb2.ELeagueRegion
        url: str
        description: str
        notes: str
        start_timestamp: int
        end_timestamp: int
        pro_circuit_points: int
        image_bits: int
        status: _dota_shared_enums_pb2.ELeagueStatus
        most_recent_activity: int
        registration_period: int
        def __init__(
            self,
            league_id: int | None = ...,
            name: str | None = ...,
            tier: _dota_shared_enums_pb2.ELeagueTier | str | None = ...,
            region: _dota_shared_enums_pb2.ELeagueRegion | str | None = ...,
            url: str | None = ...,
            description: str | None = ...,
            notes: str | None = ...,
            start_timestamp: int | None = ...,
            end_timestamp: int | None = ...,
            pro_circuit_points: int | None = ...,
            image_bits: int | None = ...,
            status: _dota_shared_enums_pb2.ELeagueStatus | str | None = ...,
            most_recent_activity: int | None = ...,
            registration_period: int | None = ...,
        ) -> None: ...

    class Admin(_message.Message):
        __slots__ = ("account_id", "is_primary", "email_address")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        IS_PRIMARY_FIELD_NUMBER: _ClassVar[int]
        EMAIL_ADDRESS_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        is_primary: bool
        email_address: str
        def __init__(
            self,
            account_id: int | None = ...,
            is_primary: bool = ...,
            email_address: str | None = ...,
        ) -> None: ...

    class PrizePoolItem(_message.Message):
        __slots__ = ("item_def", "sales_stop_timestamp", "revenue_pct", "revenue_cents_per_sale")
        ITEM_DEF_FIELD_NUMBER: _ClassVar[int]
        SALES_STOP_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        REVENUE_PCT_FIELD_NUMBER: _ClassVar[int]
        REVENUE_CENTS_PER_SALE_FIELD_NUMBER: _ClassVar[int]
        item_def: int
        sales_stop_timestamp: int
        revenue_pct: int
        revenue_cents_per_sale: int
        def __init__(
            self,
            item_def: int | None = ...,
            sales_stop_timestamp: int | None = ...,
            revenue_pct: int | None = ...,
            revenue_cents_per_sale: int | None = ...,
        ) -> None: ...

    class PrizePool(_message.Message):
        __slots__ = (
            "base_prize_pool",
            "total_prize_pool",
            "prize_split_pct_x100",
            "prize_pool_items",
        )
        BASE_PRIZE_POOL_FIELD_NUMBER: _ClassVar[int]
        TOTAL_PRIZE_POOL_FIELD_NUMBER: _ClassVar[int]
        PRIZE_SPLIT_PCT_X100_FIELD_NUMBER: _ClassVar[int]
        PRIZE_POOL_ITEMS_FIELD_NUMBER: _ClassVar[int]
        base_prize_pool: int
        total_prize_pool: int
        prize_split_pct_x100: _containers.RepeatedScalarFieldContainer[int]
        prize_pool_items: _containers.RepeatedCompositeFieldContainer[CMsgDOTALeague.PrizePoolItem]
        def __init__(
            self,
            base_prize_pool: int | None = ...,
            total_prize_pool: int | None = ...,
            prize_split_pct_x100: _Iterable[int] | None = ...,
            prize_pool_items: _Iterable[CMsgDOTALeague.PrizePoolItem | _Mapping] | None = ...,
        ) -> None: ...

    class Stream(_message.Message):
        __slots__ = ("stream_id", "language", "name", "broadcast_provider", "stream_url", "vod_url")
        STREAM_ID_FIELD_NUMBER: _ClassVar[int]
        LANGUAGE_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        BROADCAST_PROVIDER_FIELD_NUMBER: _ClassVar[int]
        STREAM_URL_FIELD_NUMBER: _ClassVar[int]
        VOD_URL_FIELD_NUMBER: _ClassVar[int]
        stream_id: int
        language: int
        name: str
        broadcast_provider: _dota_shared_enums_pb2.ELeagueBroadcastProvider
        stream_url: str
        vod_url: str
        def __init__(
            self,
            stream_id: int | None = ...,
            language: int | None = ...,
            name: str | None = ...,
            broadcast_provider: _dota_shared_enums_pb2.ELeagueBroadcastProvider | str | None = ...,
            stream_url: str | None = ...,
            vod_url: str | None = ...,
        ) -> None: ...

    class SeriesInfo(_message.Message):
        __slots__ = (
            "series_id",
            "series_type",
            "start_time",
            "match_ids",
            "team_id_1",
            "team_id_2",
        )
        SERIES_ID_FIELD_NUMBER: _ClassVar[int]
        SERIES_TYPE_FIELD_NUMBER: _ClassVar[int]
        START_TIME_FIELD_NUMBER: _ClassVar[int]
        MATCH_IDS_FIELD_NUMBER: _ClassVar[int]
        TEAM_ID_1_FIELD_NUMBER: _ClassVar[int]
        TEAM_ID_2_FIELD_NUMBER: _ClassVar[int]
        series_id: int
        series_type: int
        start_time: int
        match_ids: _containers.RepeatedScalarFieldContainer[int]
        team_id_1: int
        team_id_2: int
        def __init__(
            self,
            series_id: int | None = ...,
            series_type: int | None = ...,
            start_time: int | None = ...,
            match_ids: _Iterable[int] | None = ...,
            team_id_1: int | None = ...,
            team_id_2: int | None = ...,
        ) -> None: ...

    class Player(_message.Message):
        __slots__ = ("account_id", "name", "team_id")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        name: str
        team_id: int
        def __init__(
            self, account_id: int | None = ..., name: str | None = ..., team_id: int | None = ...
        ) -> None: ...

    INFO_FIELD_NUMBER: _ClassVar[int]
    PRIZE_POOL_FIELD_NUMBER: _ClassVar[int]
    ADMINS_FIELD_NUMBER: _ClassVar[int]
    STREAMS_FIELD_NUMBER: _ClassVar[int]
    NODE_GROUPS_FIELD_NUMBER: _ClassVar[int]
    SERIES_INFOS_FIELD_NUMBER: _ClassVar[int]
    REGISTERED_PLAYERS_FIELD_NUMBER: _ClassVar[int]
    info: CMsgDOTALeague.Info
    prize_pool: CMsgDOTALeague.PrizePool
    admins: _containers.RepeatedCompositeFieldContainer[CMsgDOTALeague.Admin]
    streams: _containers.RepeatedCompositeFieldContainer[CMsgDOTALeague.Stream]
    node_groups: _containers.RepeatedCompositeFieldContainer[CMsgDOTALeagueNodeGroup]
    series_infos: _containers.RepeatedCompositeFieldContainer[CMsgDOTALeague.SeriesInfo]
    registered_players: _containers.RepeatedCompositeFieldContainer[CMsgDOTALeague.Player]
    def __init__(
        self,
        info: CMsgDOTALeague.Info | _Mapping | None = ...,
        prize_pool: CMsgDOTALeague.PrizePool | _Mapping | None = ...,
        admins: _Iterable[CMsgDOTALeague.Admin | _Mapping] | None = ...,
        streams: _Iterable[CMsgDOTALeague.Stream | _Mapping] | None = ...,
        node_groups: _Iterable[CMsgDOTALeagueNodeGroup | _Mapping] | None = ...,
        series_infos: _Iterable[CMsgDOTALeague.SeriesInfo | _Mapping] | None = ...,
        registered_players: _Iterable[CMsgDOTALeague.Player | _Mapping] | None = ...,
    ) -> None: ...

class CMsgDOTALeagueList(_message.Message):
    __slots__ = ("leagues",)
    LEAGUES_FIELD_NUMBER: _ClassVar[int]
    leagues: _containers.RepeatedCompositeFieldContainer[CMsgDOTALeague]
    def __init__(self, leagues: _Iterable[CMsgDOTALeague | _Mapping] | None = ...) -> None: ...

class CMsgDOTALeagueInfo(_message.Message):
    __slots__ = (
        "league_id",
        "name",
        "tier",
        "region",
        "most_recent_activity",
        "total_prize_pool",
        "start_timestamp",
        "end_timestamp",
        "status",
    )
    LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TIER_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    MOST_RECENT_ACTIVITY_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PRIZE_POOL_FIELD_NUMBER: _ClassVar[int]
    START_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    END_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    league_id: int
    name: str
    tier: _dota_shared_enums_pb2.ELeagueTier
    region: _dota_shared_enums_pb2.ELeagueRegion
    most_recent_activity: int
    total_prize_pool: int
    start_timestamp: int
    end_timestamp: int
    status: int
    def __init__(
        self,
        league_id: int | None = ...,
        name: str | None = ...,
        tier: _dota_shared_enums_pb2.ELeagueTier | str | None = ...,
        region: _dota_shared_enums_pb2.ELeagueRegion | str | None = ...,
        most_recent_activity: int | None = ...,
        total_prize_pool: int | None = ...,
        start_timestamp: int | None = ...,
        end_timestamp: int | None = ...,
        status: int | None = ...,
    ) -> None: ...

class CMsgDOTALeagueInfoList(_message.Message):
    __slots__ = ("infos",)
    INFOS_FIELD_NUMBER: _ClassVar[int]
    infos: _containers.RepeatedCompositeFieldContainer[CMsgDOTALeagueInfo]
    def __init__(self, infos: _Iterable[CMsgDOTALeagueInfo | _Mapping] | None = ...) -> None: ...

class CMsgDOTALeagueLiveGames(_message.Message):
    __slots__ = ("games",)
    class LiveGame(_message.Message):
        __slots__ = (
            "league_id",
            "server_steam_id",
            "radiant_name",
            "radiant_logo",
            "radiant_team_id",
            "dire_name",
            "dire_logo",
            "dire_team_id",
            "time",
            "spectators",
            "league_node_id",
            "series_id",
            "match_id",
        )
        LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
        SERVER_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
        RADIANT_NAME_FIELD_NUMBER: _ClassVar[int]
        RADIANT_LOGO_FIELD_NUMBER: _ClassVar[int]
        RADIANT_TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        DIRE_NAME_FIELD_NUMBER: _ClassVar[int]
        DIRE_LOGO_FIELD_NUMBER: _ClassVar[int]
        DIRE_TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        TIME_FIELD_NUMBER: _ClassVar[int]
        SPECTATORS_FIELD_NUMBER: _ClassVar[int]
        LEAGUE_NODE_ID_FIELD_NUMBER: _ClassVar[int]
        SERIES_ID_FIELD_NUMBER: _ClassVar[int]
        MATCH_ID_FIELD_NUMBER: _ClassVar[int]
        league_id: int
        server_steam_id: int
        radiant_name: str
        radiant_logo: int
        radiant_team_id: int
        dire_name: str
        dire_logo: int
        dire_team_id: int
        time: int
        spectators: int
        league_node_id: int
        series_id: int
        match_id: int
        def __init__(
            self,
            league_id: int | None = ...,
            server_steam_id: int | None = ...,
            radiant_name: str | None = ...,
            radiant_logo: int | None = ...,
            radiant_team_id: int | None = ...,
            dire_name: str | None = ...,
            dire_logo: int | None = ...,
            dire_team_id: int | None = ...,
            time: int | None = ...,
            spectators: int | None = ...,
            league_node_id: int | None = ...,
            series_id: int | None = ...,
            match_id: int | None = ...,
        ) -> None: ...

    GAMES_FIELD_NUMBER: _ClassVar[int]
    games: _containers.RepeatedCompositeFieldContainer[CMsgDOTALeagueLiveGames.LiveGame]
    def __init__(
        self, games: _Iterable[CMsgDOTALeagueLiveGames.LiveGame | _Mapping] | None = ...
    ) -> None: ...

class CMsgDOTALeagueMessages(_message.Message):
    __slots__ = ("messages",)
    class Message(_message.Message):
        __slots__ = ("author_account_id", "timestamp", "message")
        AUTHOR_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        MESSAGE_FIELD_NUMBER: _ClassVar[int]
        author_account_id: int
        timestamp: int
        message: str
        def __init__(
            self,
            author_account_id: int | None = ...,
            timestamp: int | None = ...,
            message: str | None = ...,
        ) -> None: ...

    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    messages: _containers.RepeatedCompositeFieldContainer[CMsgDOTALeagueMessages.Message]
    def __init__(
        self, messages: _Iterable[CMsgDOTALeagueMessages.Message | _Mapping] | None = ...
    ) -> None: ...

class CMsgDOTALeaguePrizePool(_message.Message):
    __slots__ = ("prize_pool", "increment_per_second")
    PRIZE_POOL_FIELD_NUMBER: _ClassVar[int]
    INCREMENT_PER_SECOND_FIELD_NUMBER: _ClassVar[int]
    prize_pool: int
    increment_per_second: float
    def __init__(
        self, prize_pool: int | None = ..., increment_per_second: float | None = ...
    ) -> None: ...

class CMsgDOTALeagueInfoListAdminsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgDOTALeagueAvailableLobbyNodesRequest(_message.Message):
    __slots__ = ("league_id",)
    LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    league_id: int
    def __init__(self, league_id: int | None = ...) -> None: ...

class CMsgDOTALeagueAvailableLobbyNodes(_message.Message):
    __slots__ = ("node_infos",)
    class NodeInfo(_message.Message):
        __slots__ = ("node_id", "node_name", "node_group_name", "team_id_1", "team_id_2")
        NODE_ID_FIELD_NUMBER: _ClassVar[int]
        NODE_NAME_FIELD_NUMBER: _ClassVar[int]
        NODE_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
        TEAM_ID_1_FIELD_NUMBER: _ClassVar[int]
        TEAM_ID_2_FIELD_NUMBER: _ClassVar[int]
        node_id: int
        node_name: str
        node_group_name: str
        team_id_1: int
        team_id_2: int
        def __init__(
            self,
            node_id: int | None = ...,
            node_name: str | None = ...,
            node_group_name: str | None = ...,
            team_id_1: int | None = ...,
            team_id_2: int | None = ...,
        ) -> None: ...

    NODE_INFOS_FIELD_NUMBER: _ClassVar[int]
    node_infos: _containers.RepeatedCompositeFieldContainer[
        CMsgDOTALeagueAvailableLobbyNodes.NodeInfo
    ]
    def __init__(
        self,
        node_infos: _Iterable[CMsgDOTALeagueAvailableLobbyNodes.NodeInfo | _Mapping] | None = ...,
    ) -> None: ...

class CMsgDOTALeagueNodeResults(_message.Message):
    __slots__ = ("node_results",)
    class Result(_message.Message):
        __slots__ = (
            "node_id",
            "winning_node_id",
            "losing_node_id",
            "incoming_node_id_1",
            "incoming_node_id_2",
            "team_id_1",
            "team_id_2",
            "team_1_name",
            "team_2_name",
            "team_1_wins",
            "team_2_wins",
            "winning_team_id",
            "losing_team_id",
            "has_started",
            "is_completed",
            "scheduled_time",
            "match_ids",
        )
        NODE_ID_FIELD_NUMBER: _ClassVar[int]
        WINNING_NODE_ID_FIELD_NUMBER: _ClassVar[int]
        LOSING_NODE_ID_FIELD_NUMBER: _ClassVar[int]
        INCOMING_NODE_ID_1_FIELD_NUMBER: _ClassVar[int]
        INCOMING_NODE_ID_2_FIELD_NUMBER: _ClassVar[int]
        TEAM_ID_1_FIELD_NUMBER: _ClassVar[int]
        TEAM_ID_2_FIELD_NUMBER: _ClassVar[int]
        TEAM_1_NAME_FIELD_NUMBER: _ClassVar[int]
        TEAM_2_NAME_FIELD_NUMBER: _ClassVar[int]
        TEAM_1_WINS_FIELD_NUMBER: _ClassVar[int]
        TEAM_2_WINS_FIELD_NUMBER: _ClassVar[int]
        WINNING_TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        LOSING_TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        HAS_STARTED_FIELD_NUMBER: _ClassVar[int]
        IS_COMPLETED_FIELD_NUMBER: _ClassVar[int]
        SCHEDULED_TIME_FIELD_NUMBER: _ClassVar[int]
        MATCH_IDS_FIELD_NUMBER: _ClassVar[int]
        node_id: int
        winning_node_id: int
        losing_node_id: int
        incoming_node_id_1: int
        incoming_node_id_2: int
        team_id_1: int
        team_id_2: int
        team_1_name: str
        team_2_name: str
        team_1_wins: int
        team_2_wins: int
        winning_team_id: int
        losing_team_id: int
        has_started: bool
        is_completed: bool
        scheduled_time: int
        match_ids: _containers.RepeatedScalarFieldContainer[int]
        def __init__(
            self,
            node_id: int | None = ...,
            winning_node_id: int | None = ...,
            losing_node_id: int | None = ...,
            incoming_node_id_1: int | None = ...,
            incoming_node_id_2: int | None = ...,
            team_id_1: int | None = ...,
            team_id_2: int | None = ...,
            team_1_name: str | None = ...,
            team_2_name: str | None = ...,
            team_1_wins: int | None = ...,
            team_2_wins: int | None = ...,
            winning_team_id: int | None = ...,
            losing_team_id: int | None = ...,
            has_started: bool = ...,
            is_completed: bool = ...,
            scheduled_time: int | None = ...,
            match_ids: _Iterable[int] | None = ...,
        ) -> None: ...

    NODE_RESULTS_FIELD_NUMBER: _ClassVar[int]
    node_results: _containers.RepeatedCompositeFieldContainer[CMsgDOTALeagueNodeResults.Result]
    def __init__(
        self, node_results: _Iterable[CMsgDOTALeagueNodeResults.Result | _Mapping] | None = ...
    ) -> None: ...

class CMsgDOTADPCLeagueResults(_message.Message):
    __slots__ = ("results", "points", "dollars")
    class Result(_message.Message):
        __slots__ = (
            "standing",
            "team_id",
            "team_name",
            "team_logo",
            "team_logo_url",
            "points",
            "earnings",
            "timestamp",
            "phase",
            "team_abbreviation",
        )
        STANDING_FIELD_NUMBER: _ClassVar[int]
        TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
        TEAM_LOGO_FIELD_NUMBER: _ClassVar[int]
        TEAM_LOGO_URL_FIELD_NUMBER: _ClassVar[int]
        POINTS_FIELD_NUMBER: _ClassVar[int]
        EARNINGS_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        PHASE_FIELD_NUMBER: _ClassVar[int]
        TEAM_ABBREVIATION_FIELD_NUMBER: _ClassVar[int]
        standing: int
        team_id: int
        team_name: str
        team_logo: int
        team_logo_url: str
        points: int
        earnings: int
        timestamp: int
        phase: _dota_shared_enums_pb2.ELeaguePhase
        team_abbreviation: str
        def __init__(
            self,
            standing: int | None = ...,
            team_id: int | None = ...,
            team_name: str | None = ...,
            team_logo: int | None = ...,
            team_logo_url: str | None = ...,
            points: int | None = ...,
            earnings: int | None = ...,
            timestamp: int | None = ...,
            phase: _dota_shared_enums_pb2.ELeaguePhase | str | None = ...,
            team_abbreviation: str | None = ...,
        ) -> None: ...

    RESULTS_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    DOLLARS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[CMsgDOTADPCLeagueResults.Result]
    points: _containers.RepeatedScalarFieldContainer[int]
    dollars: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        results: _Iterable[CMsgDOTADPCLeagueResults.Result | _Mapping] | None = ...,
        points: _Iterable[int] | None = ...,
        dollars: _Iterable[int] | None = ...,
    ) -> None: ...

class CMsgDOTADPCTeamResults(_message.Message):
    __slots__ = ("results",)
    class Result(_message.Message):
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

    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[CMsgDOTADPCTeamResults.Result]
    def __init__(
        self, results: _Iterable[CMsgDOTADPCTeamResults.Result | _Mapping] | None = ...
    ) -> None: ...

class CMsgDOTADPCSeasonResults(_message.Message):
    __slots__ = (
        "results",
        "standings",
        "major_wildcard_standings",
        "major_group_standings",
        "major_playoff_standings",
    )
    class TeamLeagueResult(_message.Message):
        __slots__ = (
            "timestamp",
            "league_id",
            "standing",
            "points",
            "earnings",
            "audit_action",
            "audit_data",
        )
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
        STANDING_FIELD_NUMBER: _ClassVar[int]
        POINTS_FIELD_NUMBER: _ClassVar[int]
        EARNINGS_FIELD_NUMBER: _ClassVar[int]
        AUDIT_ACTION_FIELD_NUMBER: _ClassVar[int]
        AUDIT_DATA_FIELD_NUMBER: _ClassVar[int]
        timestamp: int
        league_id: int
        standing: int
        points: int
        earnings: int
        audit_action: int
        audit_data: int
        def __init__(
            self,
            timestamp: int | None = ...,
            league_id: int | None = ...,
            standing: int | None = ...,
            points: int | None = ...,
            earnings: int | None = ...,
            audit_action: int | None = ...,
            audit_data: int | None = ...,
        ) -> None: ...

    class TeamResult(_message.Message):
        __slots__ = (
            "team_id",
            "team_name",
            "team_abbreviation",
            "team_logo",
            "team_logo_url",
            "total_points",
            "total_earnings",
            "league_results",
        )
        TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
        TEAM_ABBREVIATION_FIELD_NUMBER: _ClassVar[int]
        TEAM_LOGO_FIELD_NUMBER: _ClassVar[int]
        TEAM_LOGO_URL_FIELD_NUMBER: _ClassVar[int]
        TOTAL_POINTS_FIELD_NUMBER: _ClassVar[int]
        TOTAL_EARNINGS_FIELD_NUMBER: _ClassVar[int]
        LEAGUE_RESULTS_FIELD_NUMBER: _ClassVar[int]
        team_id: int
        team_name: str
        team_abbreviation: str
        team_logo: int
        team_logo_url: str
        total_points: int
        total_earnings: int
        league_results: _containers.RepeatedCompositeFieldContainer[
            CMsgDOTADPCSeasonResults.TeamLeagueResult
        ]
        def __init__(
            self,
            team_id: int | None = ...,
            team_name: str | None = ...,
            team_abbreviation: str | None = ...,
            team_logo: int | None = ...,
            team_logo_url: str | None = ...,
            total_points: int | None = ...,
            total_earnings: int | None = ...,
            league_results: _Iterable[CMsgDOTADPCSeasonResults.TeamLeagueResult | _Mapping]
            | None = ...,
        ) -> None: ...

    class StandingEntry(_message.Message):
        __slots__ = ("team_id", "wins", "losses", "team_url", "team_name", "team_abbreviation")
        TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        WINS_FIELD_NUMBER: _ClassVar[int]
        LOSSES_FIELD_NUMBER: _ClassVar[int]
        TEAM_URL_FIELD_NUMBER: _ClassVar[int]
        TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
        TEAM_ABBREVIATION_FIELD_NUMBER: _ClassVar[int]
        team_id: int
        wins: int
        losses: int
        team_url: str
        team_name: str
        team_abbreviation: str
        def __init__(
            self,
            team_id: int | None = ...,
            wins: int | None = ...,
            losses: int | None = ...,
            team_url: str | None = ...,
            team_name: str | None = ...,
            team_abbreviation: str | None = ...,
        ) -> None: ...

    class Standing(_message.Message):
        __slots__ = ("region", "division", "entries")
        REGION_FIELD_NUMBER: _ClassVar[int]
        DIVISION_FIELD_NUMBER: _ClassVar[int]
        ENTRIES_FIELD_NUMBER: _ClassVar[int]
        region: _dota_shared_enums_pb2.ELeagueRegion
        division: _dota_shared_enums_pb2.ELeagueDivision
        entries: _containers.RepeatedCompositeFieldContainer[CMsgDOTADPCSeasonResults.StandingEntry]
        def __init__(
            self,
            region: _dota_shared_enums_pb2.ELeagueRegion | str | None = ...,
            division: _dota_shared_enums_pb2.ELeagueDivision | str | None = ...,
            entries: _Iterable[CMsgDOTADPCSeasonResults.StandingEntry | _Mapping] | None = ...,
        ) -> None: ...

    RESULTS_FIELD_NUMBER: _ClassVar[int]
    STANDINGS_FIELD_NUMBER: _ClassVar[int]
    MAJOR_WILDCARD_STANDINGS_FIELD_NUMBER: _ClassVar[int]
    MAJOR_GROUP_STANDINGS_FIELD_NUMBER: _ClassVar[int]
    MAJOR_PLAYOFF_STANDINGS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[CMsgDOTADPCSeasonResults.TeamResult]
    standings: _containers.RepeatedCompositeFieldContainer[CMsgDOTADPCSeasonResults.Standing]
    major_wildcard_standings: _containers.RepeatedCompositeFieldContainer[
        CMsgDOTADPCSeasonResults.StandingEntry
    ]
    major_group_standings: _containers.RepeatedCompositeFieldContainer[
        CMsgDOTADPCSeasonResults.StandingEntry
    ]
    major_playoff_standings: _containers.RepeatedCompositeFieldContainer[
        CMsgDOTADPCSeasonResults.StandingEntry
    ]
    def __init__(
        self,
        results: _Iterable[CMsgDOTADPCSeasonResults.TeamResult | _Mapping] | None = ...,
        standings: _Iterable[CMsgDOTADPCSeasonResults.Standing | _Mapping] | None = ...,
        major_wildcard_standings: _Iterable[CMsgDOTADPCSeasonResults.StandingEntry | _Mapping]
        | None = ...,
        major_group_standings: _Iterable[CMsgDOTADPCSeasonResults.StandingEntry | _Mapping]
        | None = ...,
        major_playoff_standings: _Iterable[CMsgDOTADPCSeasonResults.StandingEntry | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgDOTADPCSeasonSpoilerResults(_message.Message):
    __slots__ = ("time_last_updated", "saved_results")
    TIME_LAST_UPDATED_FIELD_NUMBER: _ClassVar[int]
    SAVED_RESULTS_FIELD_NUMBER: _ClassVar[int]
    time_last_updated: int
    saved_results: CMsgDOTADPCSeasonResults
    def __init__(
        self,
        time_last_updated: int | None = ...,
        saved_results: CMsgDOTADPCSeasonResults | _Mapping | None = ...,
    ) -> None: ...
