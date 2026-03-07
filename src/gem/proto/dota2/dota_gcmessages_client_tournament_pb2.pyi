from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

import dota_client_enums_pb2 as _dota_client_enums_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class ETournamentEvent(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_ETournamentEvent_None: _ClassVar[ETournamentEvent]
    k_ETournamentEvent_TournamentCreated: _ClassVar[ETournamentEvent]
    k_ETournamentEvent_TournamentsMerged: _ClassVar[ETournamentEvent]
    k_ETournamentEvent_GameOutcome: _ClassVar[ETournamentEvent]
    k_ETournamentEvent_TeamGivenBye: _ClassVar[ETournamentEvent]
    k_ETournamentEvent_TournamentCanceledByAdmin: _ClassVar[ETournamentEvent]
    k_ETournamentEvent_TeamAbandoned: _ClassVar[ETournamentEvent]
    k_ETournamentEvent_ScheduledGameStarted: _ClassVar[ETournamentEvent]
    k_ETournamentEvent_Canceled: _ClassVar[ETournamentEvent]
    k_ETournamentEvent_TeamParticipationTimedOut_EntryFeeRefund: _ClassVar[ETournamentEvent]
    k_ETournamentEvent_TeamParticipationTimedOut_EntryFeeForfeit: _ClassVar[ETournamentEvent]
    k_ETournamentEvent_TeamParticipationTimedOut_GrantedVictory: _ClassVar[ETournamentEvent]

k_ETournamentEvent_None: ETournamentEvent
k_ETournamentEvent_TournamentCreated: ETournamentEvent
k_ETournamentEvent_TournamentsMerged: ETournamentEvent
k_ETournamentEvent_GameOutcome: ETournamentEvent
k_ETournamentEvent_TeamGivenBye: ETournamentEvent
k_ETournamentEvent_TournamentCanceledByAdmin: ETournamentEvent
k_ETournamentEvent_TeamAbandoned: ETournamentEvent
k_ETournamentEvent_ScheduledGameStarted: ETournamentEvent
k_ETournamentEvent_Canceled: ETournamentEvent
k_ETournamentEvent_TeamParticipationTimedOut_EntryFeeRefund: ETournamentEvent
k_ETournamentEvent_TeamParticipationTimedOut_EntryFeeForfeit: ETournamentEvent
k_ETournamentEvent_TeamParticipationTimedOut_GrantedVictory: ETournamentEvent

class CMsgRequestWeekendTourneySchedule(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgWeekendTourneySchedule(_message.Message):
    __slots__ = ("divisions",)
    class Division(_message.Message):
        __slots__ = (
            "division_code",
            "time_window_open",
            "time_window_close",
            "time_window_open_next",
            "trophy_id",
            "free_weekend",
        )
        DIVISION_CODE_FIELD_NUMBER: _ClassVar[int]
        TIME_WINDOW_OPEN_FIELD_NUMBER: _ClassVar[int]
        TIME_WINDOW_CLOSE_FIELD_NUMBER: _ClassVar[int]
        TIME_WINDOW_OPEN_NEXT_FIELD_NUMBER: _ClassVar[int]
        TROPHY_ID_FIELD_NUMBER: _ClassVar[int]
        FREE_WEEKEND_FIELD_NUMBER: _ClassVar[int]
        division_code: int
        time_window_open: int
        time_window_close: int
        time_window_open_next: int
        trophy_id: int
        free_weekend: bool
        def __init__(
            self,
            division_code: int | None = ...,
            time_window_open: int | None = ...,
            time_window_close: int | None = ...,
            time_window_open_next: int | None = ...,
            trophy_id: int | None = ...,
            free_weekend: bool = ...,
        ) -> None: ...

    DIVISIONS_FIELD_NUMBER: _ClassVar[int]
    divisions: _containers.RepeatedCompositeFieldContainer[CMsgWeekendTourneySchedule.Division]
    def __init__(
        self, divisions: _Iterable[CMsgWeekendTourneySchedule.Division | _Mapping] | None = ...
    ) -> None: ...

class CMsgWeekendTourneyOpts(_message.Message):
    __slots__ = (
        "participating",
        "division_id",
        "buyin",
        "skill_level",
        "match_groups",
        "team_id",
        "pickup_team_name",
        "pickup_team_logo",
    )
    PARTICIPATING_FIELD_NUMBER: _ClassVar[int]
    DIVISION_ID_FIELD_NUMBER: _ClassVar[int]
    BUYIN_FIELD_NUMBER: _ClassVar[int]
    SKILL_LEVEL_FIELD_NUMBER: _ClassVar[int]
    MATCH_GROUPS_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    PICKUP_TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
    PICKUP_TEAM_LOGO_FIELD_NUMBER: _ClassVar[int]
    participating: bool
    division_id: int
    buyin: int
    skill_level: int
    match_groups: int
    team_id: int
    pickup_team_name: str
    pickup_team_logo: int
    def __init__(
        self,
        participating: bool = ...,
        division_id: int | None = ...,
        buyin: int | None = ...,
        skill_level: int | None = ...,
        match_groups: int | None = ...,
        team_id: int | None = ...,
        pickup_team_name: str | None = ...,
        pickup_team_logo: int | None = ...,
    ) -> None: ...

class CMsgWeekendTourneyLeave(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgDOTATournament(_message.Message):
    __slots__ = (
        "tournament_id",
        "division_id",
        "schedule_time",
        "skill_level",
        "tournament_template",
        "state",
        "state_seq_num",
        "season_trophy_id",
        "teams",
        "games",
        "nodes",
    )
    class Team(_message.Message):
        __slots__ = (
            "team_gid",
            "node_or_state",
            "players",
            "player_buyin",
            "player_skill_level",
            "match_group_mask",
            "team_id",
            "team_name",
            "team_base_logo",
            "team_ui_logo",
        )
        TEAM_GID_FIELD_NUMBER: _ClassVar[int]
        NODE_OR_STATE_FIELD_NUMBER: _ClassVar[int]
        PLAYERS_FIELD_NUMBER: _ClassVar[int]
        PLAYER_BUYIN_FIELD_NUMBER: _ClassVar[int]
        PLAYER_SKILL_LEVEL_FIELD_NUMBER: _ClassVar[int]
        MATCH_GROUP_MASK_FIELD_NUMBER: _ClassVar[int]
        TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
        TEAM_BASE_LOGO_FIELD_NUMBER: _ClassVar[int]
        TEAM_UI_LOGO_FIELD_NUMBER: _ClassVar[int]
        team_gid: int
        node_or_state: int
        players: _containers.RepeatedScalarFieldContainer[int]
        player_buyin: _containers.RepeatedScalarFieldContainer[int]
        player_skill_level: _containers.RepeatedScalarFieldContainer[int]
        match_group_mask: int
        team_id: int
        team_name: str
        team_base_logo: int
        team_ui_logo: int
        def __init__(
            self,
            team_gid: int | None = ...,
            node_or_state: int | None = ...,
            players: _Iterable[int] | None = ...,
            player_buyin: _Iterable[int] | None = ...,
            player_skill_level: _Iterable[int] | None = ...,
            match_group_mask: int | None = ...,
            team_id: int | None = ...,
            team_name: str | None = ...,
            team_base_logo: int | None = ...,
            team_ui_logo: int | None = ...,
        ) -> None: ...

    class Game(_message.Message):
        __slots__ = ("node_idx", "lobby_id", "match_id", "team_a_good", "state", "start_time")
        NODE_IDX_FIELD_NUMBER: _ClassVar[int]
        LOBBY_ID_FIELD_NUMBER: _ClassVar[int]
        MATCH_ID_FIELD_NUMBER: _ClassVar[int]
        TEAM_A_GOOD_FIELD_NUMBER: _ClassVar[int]
        STATE_FIELD_NUMBER: _ClassVar[int]
        START_TIME_FIELD_NUMBER: _ClassVar[int]
        node_idx: int
        lobby_id: int
        match_id: int
        team_a_good: bool
        state: _dota_client_enums_pb2.ETournamentGameState
        start_time: int
        def __init__(
            self,
            node_idx: int | None = ...,
            lobby_id: int | None = ...,
            match_id: int | None = ...,
            team_a_good: bool = ...,
            state: _dota_client_enums_pb2.ETournamentGameState | str | None = ...,
            start_time: int | None = ...,
        ) -> None: ...

    class Node(_message.Message):
        __slots__ = ("node_id", "team_idx_a", "team_idx_b", "node_state")
        NODE_ID_FIELD_NUMBER: _ClassVar[int]
        TEAM_IDX_A_FIELD_NUMBER: _ClassVar[int]
        TEAM_IDX_B_FIELD_NUMBER: _ClassVar[int]
        NODE_STATE_FIELD_NUMBER: _ClassVar[int]
        node_id: int
        team_idx_a: int
        team_idx_b: int
        node_state: _dota_client_enums_pb2.ETournamentNodeState
        def __init__(
            self,
            node_id: int | None = ...,
            team_idx_a: int | None = ...,
            team_idx_b: int | None = ...,
            node_state: _dota_client_enums_pb2.ETournamentNodeState | str | None = ...,
        ) -> None: ...

    TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DIVISION_ID_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_TIME_FIELD_NUMBER: _ClassVar[int]
    SKILL_LEVEL_FIELD_NUMBER: _ClassVar[int]
    TOURNAMENT_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    STATE_SEQ_NUM_FIELD_NUMBER: _ClassVar[int]
    SEASON_TROPHY_ID_FIELD_NUMBER: _ClassVar[int]
    TEAMS_FIELD_NUMBER: _ClassVar[int]
    GAMES_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    tournament_id: int
    division_id: int
    schedule_time: int
    skill_level: int
    tournament_template: _dota_client_enums_pb2.ETournamentTemplate
    state: _dota_client_enums_pb2.ETournamentState
    state_seq_num: int
    season_trophy_id: int
    teams: _containers.RepeatedCompositeFieldContainer[CMsgDOTATournament.Team]
    games: _containers.RepeatedCompositeFieldContainer[CMsgDOTATournament.Game]
    nodes: _containers.RepeatedCompositeFieldContainer[CMsgDOTATournament.Node]
    def __init__(
        self,
        tournament_id: int | None = ...,
        division_id: int | None = ...,
        schedule_time: int | None = ...,
        skill_level: int | None = ...,
        tournament_template: _dota_client_enums_pb2.ETournamentTemplate | str | None = ...,
        state: _dota_client_enums_pb2.ETournamentState | str | None = ...,
        state_seq_num: int | None = ...,
        season_trophy_id: int | None = ...,
        teams: _Iterable[CMsgDOTATournament.Team | _Mapping] | None = ...,
        games: _Iterable[CMsgDOTATournament.Game | _Mapping] | None = ...,
        nodes: _Iterable[CMsgDOTATournament.Node | _Mapping] | None = ...,
    ) -> None: ...

class CMsgDOTATournamentStateChange(_message.Message):
    __slots__ = (
        "new_tournament_id",
        "event",
        "new_tournament_state",
        "game_changes",
        "team_changes",
        "merged_tournament_ids",
        "state_seq_num",
    )
    class GameChange(_message.Message):
        __slots__ = ("match_id", "new_state")
        MATCH_ID_FIELD_NUMBER: _ClassVar[int]
        NEW_STATE_FIELD_NUMBER: _ClassVar[int]
        match_id: int
        new_state: _dota_client_enums_pb2.ETournamentGameState
        def __init__(
            self,
            match_id: int | None = ...,
            new_state: _dota_client_enums_pb2.ETournamentGameState | str | None = ...,
        ) -> None: ...

    class TeamChange(_message.Message):
        __slots__ = ("team_gid", "new_node_or_state", "old_node_or_state")
        TEAM_GID_FIELD_NUMBER: _ClassVar[int]
        NEW_NODE_OR_STATE_FIELD_NUMBER: _ClassVar[int]
        OLD_NODE_OR_STATE_FIELD_NUMBER: _ClassVar[int]
        team_gid: int
        new_node_or_state: int
        old_node_or_state: int
        def __init__(
            self,
            team_gid: int | None = ...,
            new_node_or_state: int | None = ...,
            old_node_or_state: int | None = ...,
        ) -> None: ...

    NEW_TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    NEW_TOURNAMENT_STATE_FIELD_NUMBER: _ClassVar[int]
    GAME_CHANGES_FIELD_NUMBER: _ClassVar[int]
    TEAM_CHANGES_FIELD_NUMBER: _ClassVar[int]
    MERGED_TOURNAMENT_IDS_FIELD_NUMBER: _ClassVar[int]
    STATE_SEQ_NUM_FIELD_NUMBER: _ClassVar[int]
    new_tournament_id: int
    event: ETournamentEvent
    new_tournament_state: _dota_client_enums_pb2.ETournamentState
    game_changes: _containers.RepeatedCompositeFieldContainer[
        CMsgDOTATournamentStateChange.GameChange
    ]
    team_changes: _containers.RepeatedCompositeFieldContainer[
        CMsgDOTATournamentStateChange.TeamChange
    ]
    merged_tournament_ids: _containers.RepeatedScalarFieldContainer[int]
    state_seq_num: int
    def __init__(
        self,
        new_tournament_id: int | None = ...,
        event: ETournamentEvent | str | None = ...,
        new_tournament_state: _dota_client_enums_pb2.ETournamentState | str | None = ...,
        game_changes: _Iterable[CMsgDOTATournamentStateChange.GameChange | _Mapping] | None = ...,
        team_changes: _Iterable[CMsgDOTATournamentStateChange.TeamChange | _Mapping] | None = ...,
        merged_tournament_ids: _Iterable[int] | None = ...,
        state_seq_num: int | None = ...,
    ) -> None: ...

class CMsgDOTAWeekendTourneyPlayerSkillLevelStats(_message.Message):
    __slots__ = (
        "skill_level",
        "times_won_0",
        "times_won_1",
        "times_won_2",
        "times_won_3",
        "times_bye_and_lost",
        "times_bye_and_won",
        "times_unusual_champ",
        "total_games_won",
        "score",
    )
    SKILL_LEVEL_FIELD_NUMBER: _ClassVar[int]
    TIMES_WON_0_FIELD_NUMBER: _ClassVar[int]
    TIMES_WON_1_FIELD_NUMBER: _ClassVar[int]
    TIMES_WON_2_FIELD_NUMBER: _ClassVar[int]
    TIMES_WON_3_FIELD_NUMBER: _ClassVar[int]
    TIMES_BYE_AND_LOST_FIELD_NUMBER: _ClassVar[int]
    TIMES_BYE_AND_WON_FIELD_NUMBER: _ClassVar[int]
    TIMES_UNUSUAL_CHAMP_FIELD_NUMBER: _ClassVar[int]
    TOTAL_GAMES_WON_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    skill_level: int
    times_won_0: int
    times_won_1: int
    times_won_2: int
    times_won_3: int
    times_bye_and_lost: int
    times_bye_and_won: int
    times_unusual_champ: int
    total_games_won: int
    score: int
    def __init__(
        self,
        skill_level: int | None = ...,
        times_won_0: int | None = ...,
        times_won_1: int | None = ...,
        times_won_2: int | None = ...,
        times_won_3: int | None = ...,
        times_bye_and_lost: int | None = ...,
        times_bye_and_won: int | None = ...,
        times_unusual_champ: int | None = ...,
        total_games_won: int | None = ...,
        score: int | None = ...,
    ) -> None: ...

class CMsgDOTAWeekendTourneyPlayerStats(_message.Message):
    __slots__ = ("account_id", "season_trophy_id", "skill_levels", "current_tier")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SEASON_TROPHY_ID_FIELD_NUMBER: _ClassVar[int]
    SKILL_LEVELS_FIELD_NUMBER: _ClassVar[int]
    CURRENT_TIER_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    season_trophy_id: int
    skill_levels: _containers.RepeatedCompositeFieldContainer[
        CMsgDOTAWeekendTourneyPlayerSkillLevelStats
    ]
    current_tier: int
    def __init__(
        self,
        account_id: int | None = ...,
        season_trophy_id: int | None = ...,
        skill_levels: _Iterable[CMsgDOTAWeekendTourneyPlayerSkillLevelStats | _Mapping]
        | None = ...,
        current_tier: int | None = ...,
    ) -> None: ...

class CMsgDOTAWeekendTourneyPlayerStatsRequest(_message.Message):
    __slots__ = ("account_id", "season_trophy_id")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SEASON_TROPHY_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    season_trophy_id: int
    def __init__(
        self, account_id: int | None = ..., season_trophy_id: int | None = ...
    ) -> None: ...

class CMsgDOTAWeekendTourneyPlayerHistory(_message.Message):
    __slots__ = ("account_id", "tournaments")
    class Tournament(_message.Message):
        __slots__ = (
            "tournament_id",
            "start_time",
            "tournament_tier",
            "team_id",
            "team_date",
            "team_result",
            "account_id",
            "team_name",
            "season_trophy_id",
        )
        TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
        START_TIME_FIELD_NUMBER: _ClassVar[int]
        TOURNAMENT_TIER_FIELD_NUMBER: _ClassVar[int]
        TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        TEAM_DATE_FIELD_NUMBER: _ClassVar[int]
        TEAM_RESULT_FIELD_NUMBER: _ClassVar[int]
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
        SEASON_TROPHY_ID_FIELD_NUMBER: _ClassVar[int]
        tournament_id: int
        start_time: int
        tournament_tier: int
        team_id: int
        team_date: int
        team_result: int
        account_id: _containers.RepeatedScalarFieldContainer[int]
        team_name: str
        season_trophy_id: int
        def __init__(
            self,
            tournament_id: int | None = ...,
            start_time: int | None = ...,
            tournament_tier: int | None = ...,
            team_id: int | None = ...,
            team_date: int | None = ...,
            team_result: int | None = ...,
            account_id: _Iterable[int] | None = ...,
            team_name: str | None = ...,
            season_trophy_id: int | None = ...,
        ) -> None: ...

    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TOURNAMENTS_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    tournaments: _containers.RepeatedCompositeFieldContainer[
        CMsgDOTAWeekendTourneyPlayerHistory.Tournament
    ]
    def __init__(
        self,
        account_id: int | None = ...,
        tournaments: _Iterable[CMsgDOTAWeekendTourneyPlayerHistory.Tournament | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgDOTAWeekendTourneyParticipationDetails(_message.Message):
    __slots__ = ("divisions",)
    class Tier(_message.Message):
        __slots__ = (
            "tier",
            "players",
            "teams",
            "winning_teams",
            "players_streak_2",
            "players_streak_3",
            "players_streak_4",
            "players_streak_5",
        )
        TIER_FIELD_NUMBER: _ClassVar[int]
        PLAYERS_FIELD_NUMBER: _ClassVar[int]
        TEAMS_FIELD_NUMBER: _ClassVar[int]
        WINNING_TEAMS_FIELD_NUMBER: _ClassVar[int]
        PLAYERS_STREAK_2_FIELD_NUMBER: _ClassVar[int]
        PLAYERS_STREAK_3_FIELD_NUMBER: _ClassVar[int]
        PLAYERS_STREAK_4_FIELD_NUMBER: _ClassVar[int]
        PLAYERS_STREAK_5_FIELD_NUMBER: _ClassVar[int]
        tier: int
        players: int
        teams: int
        winning_teams: int
        players_streak_2: int
        players_streak_3: int
        players_streak_4: int
        players_streak_5: int
        def __init__(
            self,
            tier: int | None = ...,
            players: int | None = ...,
            teams: int | None = ...,
            winning_teams: int | None = ...,
            players_streak_2: int | None = ...,
            players_streak_3: int | None = ...,
            players_streak_4: int | None = ...,
            players_streak_5: int | None = ...,
        ) -> None: ...

    class Division(_message.Message):
        __slots__ = ("division_id", "schedule_time", "tiers")
        DIVISION_ID_FIELD_NUMBER: _ClassVar[int]
        SCHEDULE_TIME_FIELD_NUMBER: _ClassVar[int]
        TIERS_FIELD_NUMBER: _ClassVar[int]
        division_id: int
        schedule_time: int
        tiers: _containers.RepeatedCompositeFieldContainer[
            CMsgDOTAWeekendTourneyParticipationDetails.Tier
        ]
        def __init__(
            self,
            division_id: int | None = ...,
            schedule_time: int | None = ...,
            tiers: _Iterable[CMsgDOTAWeekendTourneyParticipationDetails.Tier | _Mapping]
            | None = ...,
        ) -> None: ...

    DIVISIONS_FIELD_NUMBER: _ClassVar[int]
    divisions: _containers.RepeatedCompositeFieldContainer[
        CMsgDOTAWeekendTourneyParticipationDetails.Division
    ]
    def __init__(
        self,
        divisions: _Iterable[CMsgDOTAWeekendTourneyParticipationDetails.Division | _Mapping]
        | None = ...,
    ) -> None: ...
