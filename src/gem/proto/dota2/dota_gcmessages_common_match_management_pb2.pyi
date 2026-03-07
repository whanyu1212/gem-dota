from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

import dota_shared_enums_pb2 as _dota_shared_enums_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class ELaneSelection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_ELaneSelection_SAFELANE: _ClassVar[ELaneSelection]
    k_ELaneSelection_OFFLANE: _ClassVar[ELaneSelection]
    k_ELaneSelection_MIDLANE: _ClassVar[ELaneSelection]
    k_ELaneSelection_SUPPORT: _ClassVar[ELaneSelection]
    k_ELaneSelection_HARDSUPPORT: _ClassVar[ELaneSelection]

class ELaneSelectionFlags(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_ELaneSelectionFlags_SAFELANE: _ClassVar[ELaneSelectionFlags]
    k_ELaneSelectionFlags_OFFLANE: _ClassVar[ELaneSelectionFlags]
    k_ELaneSelectionFlags_MIDLANE: _ClassVar[ELaneSelectionFlags]
    k_ELaneSelectionFlags_SUPPORT: _ClassVar[ELaneSelectionFlags]
    k_ELaneSelectionFlags_HARDSUPPORT: _ClassVar[ELaneSelectionFlags]
    k_ELaneSelectionFlagGroup_None: _ClassVar[ELaneSelectionFlags]
    k_ELaneSelectionFlagGroup_CORE: _ClassVar[ELaneSelectionFlags]
    k_ELaneSelectionFlagGroup_SUPPORT: _ClassVar[ELaneSelectionFlags]
    k_ELaneSelectionFlagGroup_ALL: _ClassVar[ELaneSelectionFlags]
    k_ELaneSelectionFlagGroup_HIGHDEMAND: _ClassVar[ELaneSelectionFlags]

class EPartyMatchmakingFlags(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EPartyMatchmakingFlags_None: _ClassVar[EPartyMatchmakingFlags]
    k_EPartyMatchmakingFlags_LargeRankSpread: _ClassVar[EPartyMatchmakingFlags]

class EHighPriorityMMState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EHighPriorityMM_Unknown: _ClassVar[EHighPriorityMMState]
    k_EHighPriorityMM_MissingMMData: _ClassVar[EHighPriorityMMState]
    k_EHighPriorityMM_ResourceMissing: _ClassVar[EHighPriorityMMState]
    k_EHighPriorityMM_ManuallyDisabled: _ClassVar[EHighPriorityMMState]
    k_EHighPriorityMM_Min_Enabled: _ClassVar[EHighPriorityMMState]
    k_EHighPriorityMM_AllRolesSelected: _ClassVar[EHighPriorityMMState]
    k_EHighPriorityMM_UsingResource: _ClassVar[EHighPriorityMMState]
    k_EHighPriorityMM_FiveStack: _ClassVar[EHighPriorityMMState]
    k_EHighPriorityMM_HighDemand: _ClassVar[EHighPriorityMMState]

class EReadyCheckStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EReadyCheckStatus_Unknown: _ClassVar[EReadyCheckStatus]
    k_EReadyCheckStatus_NotReady: _ClassVar[EReadyCheckStatus]
    k_EReadyCheckStatus_Ready: _ClassVar[EReadyCheckStatus]

class EReadyCheckRequestResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EReadyCheckRequestResult_Success: _ClassVar[EReadyCheckRequestResult]
    k_EReadyCheckRequestResult_AlreadyInProgress: _ClassVar[EReadyCheckRequestResult]
    k_EReadyCheckRequestResult_NotInParty: _ClassVar[EReadyCheckRequestResult]
    k_EReadyCheckRequestResult_SendError: _ClassVar[EReadyCheckRequestResult]
    k_EReadyCheckRequestResult_UnknownError: _ClassVar[EReadyCheckRequestResult]

class EMatchBehaviorScoreVariance(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EMatchBehaviorScoreVariance_Invalid: _ClassVar[EMatchBehaviorScoreVariance]
    k_EMatchBehaviorScoreVariance_Low: _ClassVar[EMatchBehaviorScoreVariance]
    k_EMatchBehaviorScoreVariance_Medium: _ClassVar[EMatchBehaviorScoreVariance]
    k_EMatchBehaviorScoreVariance_High: _ClassVar[EMatchBehaviorScoreVariance]

k_ELaneSelection_SAFELANE: ELaneSelection
k_ELaneSelection_OFFLANE: ELaneSelection
k_ELaneSelection_MIDLANE: ELaneSelection
k_ELaneSelection_SUPPORT: ELaneSelection
k_ELaneSelection_HARDSUPPORT: ELaneSelection
k_ELaneSelectionFlags_SAFELANE: ELaneSelectionFlags
k_ELaneSelectionFlags_OFFLANE: ELaneSelectionFlags
k_ELaneSelectionFlags_MIDLANE: ELaneSelectionFlags
k_ELaneSelectionFlags_SUPPORT: ELaneSelectionFlags
k_ELaneSelectionFlags_HARDSUPPORT: ELaneSelectionFlags
k_ELaneSelectionFlagGroup_None: ELaneSelectionFlags
k_ELaneSelectionFlagGroup_CORE: ELaneSelectionFlags
k_ELaneSelectionFlagGroup_SUPPORT: ELaneSelectionFlags
k_ELaneSelectionFlagGroup_ALL: ELaneSelectionFlags
k_ELaneSelectionFlagGroup_HIGHDEMAND: ELaneSelectionFlags
k_EPartyMatchmakingFlags_None: EPartyMatchmakingFlags
k_EPartyMatchmakingFlags_LargeRankSpread: EPartyMatchmakingFlags
k_EHighPriorityMM_Unknown: EHighPriorityMMState
k_EHighPriorityMM_MissingMMData: EHighPriorityMMState
k_EHighPriorityMM_ResourceMissing: EHighPriorityMMState
k_EHighPriorityMM_ManuallyDisabled: EHighPriorityMMState
k_EHighPriorityMM_Min_Enabled: EHighPriorityMMState
k_EHighPriorityMM_AllRolesSelected: EHighPriorityMMState
k_EHighPriorityMM_UsingResource: EHighPriorityMMState
k_EHighPriorityMM_FiveStack: EHighPriorityMMState
k_EHighPriorityMM_HighDemand: EHighPriorityMMState
k_EReadyCheckStatus_Unknown: EReadyCheckStatus
k_EReadyCheckStatus_NotReady: EReadyCheckStatus
k_EReadyCheckStatus_Ready: EReadyCheckStatus
k_EReadyCheckRequestResult_Success: EReadyCheckRequestResult
k_EReadyCheckRequestResult_AlreadyInProgress: EReadyCheckRequestResult
k_EReadyCheckRequestResult_NotInParty: EReadyCheckRequestResult
k_EReadyCheckRequestResult_SendError: EReadyCheckRequestResult
k_EReadyCheckRequestResult_UnknownError: EReadyCheckRequestResult
k_EMatchBehaviorScoreVariance_Invalid: EMatchBehaviorScoreVariance
k_EMatchBehaviorScoreVariance_Low: EMatchBehaviorScoreVariance
k_EMatchBehaviorScoreVariance_Medium: EMatchBehaviorScoreVariance
k_EMatchBehaviorScoreVariance_High: EMatchBehaviorScoreVariance

class CSODOTAPartyMember(_message.Message):
    __slots__ = (
        "is_coach",
        "region_ping_codes",
        "region_ping_times",
        "region_ping_failed_bitmask",
        "is_plus_subscriber",
        "tourney_skill_level",
        "tourney_buyin",
        "tourney_prevent_until",
        "mm_data_valid",
        "lane_selection_flags",
        "high_priority_disabled",
        "has_hp_resource",
        "joined_from_partyfinder",
        "is_steam_china",
        "banned_hero_ids",
    )
    IS_COACH_FIELD_NUMBER: _ClassVar[int]
    REGION_PING_CODES_FIELD_NUMBER: _ClassVar[int]
    REGION_PING_TIMES_FIELD_NUMBER: _ClassVar[int]
    REGION_PING_FAILED_BITMASK_FIELD_NUMBER: _ClassVar[int]
    IS_PLUS_SUBSCRIBER_FIELD_NUMBER: _ClassVar[int]
    TOURNEY_SKILL_LEVEL_FIELD_NUMBER: _ClassVar[int]
    TOURNEY_BUYIN_FIELD_NUMBER: _ClassVar[int]
    TOURNEY_PREVENT_UNTIL_FIELD_NUMBER: _ClassVar[int]
    MM_DATA_VALID_FIELD_NUMBER: _ClassVar[int]
    LANE_SELECTION_FLAGS_FIELD_NUMBER: _ClassVar[int]
    HIGH_PRIORITY_DISABLED_FIELD_NUMBER: _ClassVar[int]
    HAS_HP_RESOURCE_FIELD_NUMBER: _ClassVar[int]
    JOINED_FROM_PARTYFINDER_FIELD_NUMBER: _ClassVar[int]
    IS_STEAM_CHINA_FIELD_NUMBER: _ClassVar[int]
    BANNED_HERO_IDS_FIELD_NUMBER: _ClassVar[int]
    is_coach: bool
    region_ping_codes: _containers.RepeatedScalarFieldContainer[int]
    region_ping_times: _containers.RepeatedScalarFieldContainer[int]
    region_ping_failed_bitmask: int
    is_plus_subscriber: bool
    tourney_skill_level: int
    tourney_buyin: int
    tourney_prevent_until: int
    mm_data_valid: bool
    lane_selection_flags: int
    high_priority_disabled: bool
    has_hp_resource: bool
    joined_from_partyfinder: bool
    is_steam_china: bool
    banned_hero_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        is_coach: bool = ...,
        region_ping_codes: _Iterable[int] | None = ...,
        region_ping_times: _Iterable[int] | None = ...,
        region_ping_failed_bitmask: int | None = ...,
        is_plus_subscriber: bool = ...,
        tourney_skill_level: int | None = ...,
        tourney_buyin: int | None = ...,
        tourney_prevent_until: int | None = ...,
        mm_data_valid: bool = ...,
        lane_selection_flags: int | None = ...,
        high_priority_disabled: bool = ...,
        has_hp_resource: bool = ...,
        joined_from_partyfinder: bool = ...,
        is_steam_china: bool = ...,
        banned_hero_ids: _Iterable[int] | None = ...,
    ) -> None: ...

class CSODOTAParty(_message.Message):
    __slots__ = (
        "party_id",
        "leader_id",
        "member_ids",
        "game_modes",
        "state",
        "effective_started_matchmaking_time",
        "raw_started_matchmaking_time",
        "attempt_start_time",
        "attempt_num",
        "matchgroups",
        "low_priority_account_id",
        "match_type",
        "team_id",
        "team_name",
        "team_ui_logo",
        "team_base_logo",
        "match_disabled_until_date",
        "match_disabled_account_id",
        "matchmaking_max_range_minutes",
        "matchlanguages",
        "members",
        "low_priority_games_remaining",
        "open_for_join_requests",
        "sent_invites",
        "recv_invites",
        "account_flags",
        "region_select_flags",
        "exclusive_tournament_id",
        "tourney_division_id",
        "tourney_schedule_time",
        "tourney_skill_level",
        "tourney_bracket_round",
        "tourney_queue_deadline_time",
        "tourney_queue_deadline_state",
        "party_builder_slots_to_fill",
        "party_builder_match_groups",
        "party_builder_start_time",
        "solo_queue",
        "steam_clan_account_id",
        "ready_check",
        "custom_game_disabled_until_date",
        "custom_game_disabled_account_id",
        "is_challenge_match",
        "party_search_beacon_active",
        "matchmaking_flags",
        "high_priority_state",
        "lane_selections_enabled",
        "custom_game_difficulty_mask",
        "is_steam_china",
        "bot_difficulty_mask",
        "bot_script_index_mask",
        "restricted_from_ranked",
        "restricted_from_ranked_account_id",
        "rank_spread_likert_scale",
        "behavior_score_likert_scale",
        "contains_required_playtester",
    )
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UI: _ClassVar[CSODOTAParty.State]
        FINDING_MATCH: _ClassVar[CSODOTAParty.State]
        IN_MATCH: _ClassVar[CSODOTAParty.State]

    UI: CSODOTAParty.State
    FINDING_MATCH: CSODOTAParty.State
    IN_MATCH: CSODOTAParty.State
    PARTY_ID_FIELD_NUMBER: _ClassVar[int]
    LEADER_ID_FIELD_NUMBER: _ClassVar[int]
    MEMBER_IDS_FIELD_NUMBER: _ClassVar[int]
    GAME_MODES_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_STARTED_MATCHMAKING_TIME_FIELD_NUMBER: _ClassVar[int]
    RAW_STARTED_MATCHMAKING_TIME_FIELD_NUMBER: _ClassVar[int]
    ATTEMPT_START_TIME_FIELD_NUMBER: _ClassVar[int]
    ATTEMPT_NUM_FIELD_NUMBER: _ClassVar[int]
    MATCHGROUPS_FIELD_NUMBER: _ClassVar[int]
    LOW_PRIORITY_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    MATCH_TYPE_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
    TEAM_UI_LOGO_FIELD_NUMBER: _ClassVar[int]
    TEAM_BASE_LOGO_FIELD_NUMBER: _ClassVar[int]
    MATCH_DISABLED_UNTIL_DATE_FIELD_NUMBER: _ClassVar[int]
    MATCH_DISABLED_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    MATCHMAKING_MAX_RANGE_MINUTES_FIELD_NUMBER: _ClassVar[int]
    MATCHLANGUAGES_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    LOW_PRIORITY_GAMES_REMAINING_FIELD_NUMBER: _ClassVar[int]
    OPEN_FOR_JOIN_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    SENT_INVITES_FIELD_NUMBER: _ClassVar[int]
    RECV_INVITES_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_FLAGS_FIELD_NUMBER: _ClassVar[int]
    REGION_SELECT_FLAGS_FIELD_NUMBER: _ClassVar[int]
    EXCLUSIVE_TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TOURNEY_DIVISION_ID_FIELD_NUMBER: _ClassVar[int]
    TOURNEY_SCHEDULE_TIME_FIELD_NUMBER: _ClassVar[int]
    TOURNEY_SKILL_LEVEL_FIELD_NUMBER: _ClassVar[int]
    TOURNEY_BRACKET_ROUND_FIELD_NUMBER: _ClassVar[int]
    TOURNEY_QUEUE_DEADLINE_TIME_FIELD_NUMBER: _ClassVar[int]
    TOURNEY_QUEUE_DEADLINE_STATE_FIELD_NUMBER: _ClassVar[int]
    PARTY_BUILDER_SLOTS_TO_FILL_FIELD_NUMBER: _ClassVar[int]
    PARTY_BUILDER_MATCH_GROUPS_FIELD_NUMBER: _ClassVar[int]
    PARTY_BUILDER_START_TIME_FIELD_NUMBER: _ClassVar[int]
    SOLO_QUEUE_FIELD_NUMBER: _ClassVar[int]
    STEAM_CLAN_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    READY_CHECK_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_DISABLED_UNTIL_DATE_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_DISABLED_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    IS_CHALLENGE_MATCH_FIELD_NUMBER: _ClassVar[int]
    PARTY_SEARCH_BEACON_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    MATCHMAKING_FLAGS_FIELD_NUMBER: _ClassVar[int]
    HIGH_PRIORITY_STATE_FIELD_NUMBER: _ClassVar[int]
    LANE_SELECTIONS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_DIFFICULTY_MASK_FIELD_NUMBER: _ClassVar[int]
    IS_STEAM_CHINA_FIELD_NUMBER: _ClassVar[int]
    BOT_DIFFICULTY_MASK_FIELD_NUMBER: _ClassVar[int]
    BOT_SCRIPT_INDEX_MASK_FIELD_NUMBER: _ClassVar[int]
    RESTRICTED_FROM_RANKED_FIELD_NUMBER: _ClassVar[int]
    RESTRICTED_FROM_RANKED_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    RANK_SPREAD_LIKERT_SCALE_FIELD_NUMBER: _ClassVar[int]
    BEHAVIOR_SCORE_LIKERT_SCALE_FIELD_NUMBER: _ClassVar[int]
    CONTAINS_REQUIRED_PLAYTESTER_FIELD_NUMBER: _ClassVar[int]
    party_id: int
    leader_id: int
    member_ids: _containers.RepeatedScalarFieldContainer[int]
    game_modes: int
    state: CSODOTAParty.State
    effective_started_matchmaking_time: int
    raw_started_matchmaking_time: int
    attempt_start_time: int
    attempt_num: int
    matchgroups: int
    low_priority_account_id: int
    match_type: _dota_shared_enums_pb2.MatchType
    team_id: int
    team_name: str
    team_ui_logo: int
    team_base_logo: int
    match_disabled_until_date: int
    match_disabled_account_id: int
    matchmaking_max_range_minutes: int
    matchlanguages: int
    members: _containers.RepeatedCompositeFieldContainer[CSODOTAPartyMember]
    low_priority_games_remaining: int
    open_for_join_requests: bool
    sent_invites: _containers.RepeatedCompositeFieldContainer[CSODOTAPartyInvite]
    recv_invites: _containers.RepeatedCompositeFieldContainer[CSODOTAPartyInvite]
    account_flags: int
    region_select_flags: int
    exclusive_tournament_id: int
    tourney_division_id: int
    tourney_schedule_time: int
    tourney_skill_level: int
    tourney_bracket_round: int
    tourney_queue_deadline_time: int
    tourney_queue_deadline_state: _dota_shared_enums_pb2.ETourneyQueueDeadlineState
    party_builder_slots_to_fill: int
    party_builder_match_groups: int
    party_builder_start_time: int
    solo_queue: bool
    steam_clan_account_id: int
    ready_check: CMsgReadyCheckStatus
    custom_game_disabled_until_date: int
    custom_game_disabled_account_id: int
    is_challenge_match: bool
    party_search_beacon_active: bool
    matchmaking_flags: int
    high_priority_state: EHighPriorityMMState
    lane_selections_enabled: bool
    custom_game_difficulty_mask: int
    is_steam_china: bool
    bot_difficulty_mask: int
    bot_script_index_mask: int
    restricted_from_ranked: bool
    restricted_from_ranked_account_id: int
    rank_spread_likert_scale: int
    behavior_score_likert_scale: int
    contains_required_playtester: bool
    def __init__(
        self,
        party_id: int | None = ...,
        leader_id: int | None = ...,
        member_ids: _Iterable[int] | None = ...,
        game_modes: int | None = ...,
        state: CSODOTAParty.State | str | None = ...,
        effective_started_matchmaking_time: int | None = ...,
        raw_started_matchmaking_time: int | None = ...,
        attempt_start_time: int | None = ...,
        attempt_num: int | None = ...,
        matchgroups: int | None = ...,
        low_priority_account_id: int | None = ...,
        match_type: _dota_shared_enums_pb2.MatchType | str | None = ...,
        team_id: int | None = ...,
        team_name: str | None = ...,
        team_ui_logo: int | None = ...,
        team_base_logo: int | None = ...,
        match_disabled_until_date: int | None = ...,
        match_disabled_account_id: int | None = ...,
        matchmaking_max_range_minutes: int | None = ...,
        matchlanguages: int | None = ...,
        members: _Iterable[CSODOTAPartyMember | _Mapping] | None = ...,
        low_priority_games_remaining: int | None = ...,
        open_for_join_requests: bool = ...,
        sent_invites: _Iterable[CSODOTAPartyInvite | _Mapping] | None = ...,
        recv_invites: _Iterable[CSODOTAPartyInvite | _Mapping] | None = ...,
        account_flags: int | None = ...,
        region_select_flags: int | None = ...,
        exclusive_tournament_id: int | None = ...,
        tourney_division_id: int | None = ...,
        tourney_schedule_time: int | None = ...,
        tourney_skill_level: int | None = ...,
        tourney_bracket_round: int | None = ...,
        tourney_queue_deadline_time: int | None = ...,
        tourney_queue_deadline_state: _dota_shared_enums_pb2.ETourneyQueueDeadlineState
        | str
        | None = ...,
        party_builder_slots_to_fill: int | None = ...,
        party_builder_match_groups: int | None = ...,
        party_builder_start_time: int | None = ...,
        solo_queue: bool = ...,
        steam_clan_account_id: int | None = ...,
        ready_check: CMsgReadyCheckStatus | _Mapping | None = ...,
        custom_game_disabled_until_date: int | None = ...,
        custom_game_disabled_account_id: int | None = ...,
        is_challenge_match: bool = ...,
        party_search_beacon_active: bool = ...,
        matchmaking_flags: int | None = ...,
        high_priority_state: EHighPriorityMMState | str | None = ...,
        lane_selections_enabled: bool = ...,
        custom_game_difficulty_mask: int | None = ...,
        is_steam_china: bool = ...,
        bot_difficulty_mask: int | None = ...,
        bot_script_index_mask: int | None = ...,
        restricted_from_ranked: bool = ...,
        restricted_from_ranked_account_id: int | None = ...,
        rank_spread_likert_scale: int | None = ...,
        behavior_score_likert_scale: int | None = ...,
        contains_required_playtester: bool = ...,
    ) -> None: ...

class CSODOTAPartyInvite(_message.Message):
    __slots__ = (
        "group_id",
        "sender_id",
        "sender_name",
        "members",
        "team_id",
        "low_priority_status",
        "as_coach",
        "invite_gid",
    )
    class PartyMember(_message.Message):
        __slots__ = ("name", "steam_id", "is_coach")
        NAME_FIELD_NUMBER: _ClassVar[int]
        STEAM_ID_FIELD_NUMBER: _ClassVar[int]
        IS_COACH_FIELD_NUMBER: _ClassVar[int]
        name: str
        steam_id: int
        is_coach: bool
        def __init__(
            self, name: str | None = ..., steam_id: int | None = ..., is_coach: bool = ...
        ) -> None: ...

    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    SENDER_ID_FIELD_NUMBER: _ClassVar[int]
    SENDER_NAME_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    LOW_PRIORITY_STATUS_FIELD_NUMBER: _ClassVar[int]
    AS_COACH_FIELD_NUMBER: _ClassVar[int]
    INVITE_GID_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    sender_id: int
    sender_name: str
    members: _containers.RepeatedCompositeFieldContainer[CSODOTAPartyInvite.PartyMember]
    team_id: int
    low_priority_status: bool
    as_coach: bool
    invite_gid: int
    def __init__(
        self,
        group_id: int | None = ...,
        sender_id: int | None = ...,
        sender_name: str | None = ...,
        members: _Iterable[CSODOTAPartyInvite.PartyMember | _Mapping] | None = ...,
        team_id: int | None = ...,
        low_priority_status: bool = ...,
        as_coach: bool = ...,
        invite_gid: int | None = ...,
    ) -> None: ...

class CMsgLeaverState(_message.Message):
    __slots__ = (
        "lobby_state",
        "game_state",
        "leaver_detected",
        "first_blood_happened",
        "discard_match_results",
        "mass_disconnect",
    )
    LOBBY_STATE_FIELD_NUMBER: _ClassVar[int]
    GAME_STATE_FIELD_NUMBER: _ClassVar[int]
    LEAVER_DETECTED_FIELD_NUMBER: _ClassVar[int]
    FIRST_BLOOD_HAPPENED_FIELD_NUMBER: _ClassVar[int]
    DISCARD_MATCH_RESULTS_FIELD_NUMBER: _ClassVar[int]
    MASS_DISCONNECT_FIELD_NUMBER: _ClassVar[int]
    lobby_state: int
    game_state: _dota_shared_enums_pb2.DOTA_GameState
    leaver_detected: bool
    first_blood_happened: bool
    discard_match_results: bool
    mass_disconnect: bool
    def __init__(
        self,
        lobby_state: int | None = ...,
        game_state: _dota_shared_enums_pb2.DOTA_GameState | str | None = ...,
        leaver_detected: bool = ...,
        first_blood_happened: bool = ...,
        discard_match_results: bool = ...,
        mass_disconnect: bool = ...,
    ) -> None: ...

class CMsgReadyCheckStatus(_message.Message):
    __slots__ = ("start_timestamp", "finish_timestamp", "initiator_account_id", "ready_members")
    class ReadyMember(_message.Message):
        __slots__ = ("account_id", "ready_status")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        READY_STATUS_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        ready_status: EReadyCheckStatus
        def __init__(
            self, account_id: int | None = ..., ready_status: EReadyCheckStatus | str | None = ...
        ) -> None: ...

    START_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    FINISH_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    INITIATOR_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    READY_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    start_timestamp: int
    finish_timestamp: int
    initiator_account_id: int
    ready_members: _containers.RepeatedCompositeFieldContainer[CMsgReadyCheckStatus.ReadyMember]
    def __init__(
        self,
        start_timestamp: int | None = ...,
        finish_timestamp: int | None = ...,
        initiator_account_id: int | None = ...,
        ready_members: _Iterable[CMsgReadyCheckStatus.ReadyMember | _Mapping] | None = ...,
    ) -> None: ...

class CMsgPartyReadyCheckRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgPartyReadyCheckResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: EReadyCheckRequestResult
    def __init__(self, result: EReadyCheckRequestResult | str | None = ...) -> None: ...

class CMsgPartyReadyCheckAcknowledge(_message.Message):
    __slots__ = ("ready_status",)
    READY_STATUS_FIELD_NUMBER: _ClassVar[int]
    ready_status: EReadyCheckStatus
    def __init__(self, ready_status: EReadyCheckStatus | str | None = ...) -> None: ...

class CMsgLobbyEventGameDetails(_message.Message):
    __slots__ = ("kv_data",)
    KV_DATA_FIELD_NUMBER: _ClassVar[int]
    kv_data: bytes
    def __init__(self, kv_data: bytes | None = ...) -> None: ...

class CMsgMatchMatchmakingStats(_message.Message):
    __slots__ = ("average_queue_time", "maximum_queue_time", "behavior_score_variance")
    AVERAGE_QUEUE_TIME_FIELD_NUMBER: _ClassVar[int]
    MAXIMUM_QUEUE_TIME_FIELD_NUMBER: _ClassVar[int]
    BEHAVIOR_SCORE_VARIANCE_FIELD_NUMBER: _ClassVar[int]
    average_queue_time: int
    maximum_queue_time: int
    behavior_score_variance: EMatchBehaviorScoreVariance
    def __init__(
        self,
        average_queue_time: int | None = ...,
        maximum_queue_time: int | None = ...,
        behavior_score_variance: EMatchBehaviorScoreVariance | str | None = ...,
    ) -> None: ...

class CMvpData(_message.Message):
    __slots__ = ("mvps", "event_mvps")
    class MvpDatum(_message.Message):
        __slots__ = ("player_slot", "accolades")
        class MvpAccolade(_message.Message):
            __slots__ = ("type", "detail_value")
            class MvpAccoladeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                kills: _ClassVar[CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType]
                deaths: _ClassVar[CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType]
                assists: _ClassVar[CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType]
                net_worth: _ClassVar[CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType]
                item_value: _ClassVar[CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType]
                support_gold_spent: _ClassVar[CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType]
                wards_placed: _ClassVar[CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType]
                dewards: _ClassVar[CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType]
                camps_stacked: _ClassVar[CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType]
                last_hits: _ClassVar[CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType]
                denies: _ClassVar[CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType]
                kKillEaterEvent_Killing_Sprees: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_Godlike: _ClassVar[CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType]
                kKillEaterEvent_Towers_Destroyed: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Invoker_SunstrikeKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Axe_Culls: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Axe_BattleHungerKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_LowHealthKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Invoker_TornadoKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Sven_DoubleStuns: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Sven_WarcryAssists: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Sven_CleaveDoubleKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Sven_TeleportInterrupts: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Faceless_MultiChrono: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Faceless_ChronoKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Ursa_MultiShocks: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_RoshanKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Lion_FingerKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Riki_SmokedHeroKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_HeroesRevealedWithDust: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_SkeletonKing_ReincarnationKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Skywrath_FlareKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Leshrac_SplitEarthStuns: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Mirana_MaxStunArrows: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_PhantomAssassin_CoupdeGraceCrits: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_PhantomAssassin_DaggerCrits: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Meepo_Earthbinds: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Bloodseeker_RuptureKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Slark_LeashedEnemies: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Disruptor_FountainGlimpses: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Rubick_SpellsStolen: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Rubick_UltimatesStolen: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Doom_EnemiesDoomed: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Omniknight_Purifications: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Omniknight_AlliesRepelled: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Omniknight_EnemiesRepelled: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Warlock_FiveHeroFatalBonds: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_CrystalMaiden_FrostbittenEnemies: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_CrystalMaiden_CrystalNovas: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Kunkka_DoubleHeroTorrents: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Kunkka_TripleHeroGhostShips: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_NagaSiren_EnemiesEnsnared: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_NagaSiren_TripleHeroRipTides: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Lycan_KillsDuringShapeshift: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Pudge_DismemberKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Pudge_EnemyHeroesHooked: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Pudge_HookKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Pudge_UnseenEnemyHeroesHooked: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_DrowRanger_EnemiesSilenced: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_DrowRanger_MultiHeroSilences: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_DrowRanger_SilencedKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_DrowRanger_FrostArrowKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_DragonKnight_KillsInDragonForm: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_DragonKnight_BreatheFireKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_DragonKnight_SplashKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_WitchDoctor_CaskStuns: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_WitchDoctor_MaledictKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_WitchDoctor_MultiHeroMaledicts: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_WitchDoctor_DeathWardKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Disruptor_ThunderStrikeKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Disruptor_HeroesGlimpsed: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_CrystalMaiden_FreezingFieldKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Medusa_EnemiesPetrified: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Warlock_FatalBondsKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Warlock_GolemKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Tusk_WalrusPunches: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Tusk_SnowballStuns: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Earthshaker_FissureStuns: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Earthshaker_3HeroEchoslams: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_SandKing_BurrowstrikeStuns: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_SandKing_EpicenterKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_SkywrathMage_AncientSealKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_SkywrathMage_ConcussiveShotKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Luna_LucentBeamKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Luna_EclipseKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_KeeperOfTheLight_IlluminateKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_KeeperOfTheLight_ManaLeakStuns: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_KeeperOfTheLight_TeammatesRecalled: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_LegionCommander_DuelsWon: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Beastmaster_RoarKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Beastmaster_RoarMultiKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Windrunner_FocusFireBuildings: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Windrunner_PowershotKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_PhantomAssassin_DaggerLastHits: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_PhantomAssassin_PhantomStrikeKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_DeathProphet_CryptSwarmKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_DeathProphet_ExorcismBuildingKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_DeathProphet_ExorcismSpiritsSummoned: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_DeathProphet_MultiHeroSilences: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Abaddon_MistCoilKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Abaddon_MistCoilHealed: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Abaddon_AphoticShieldKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Lich_ChainFrostTripleKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Lich_ChainFrostMultiKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Lich_ChainFrostBounces: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Ursa_EnragedKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Ursa_EarthshockKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Lina_LagunaBladeKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Lina_DragonSlaveKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Lina_LightStrikeArrayStuns: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_Barracks_Destroyed: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_TemplarAssassin_MeldKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_TemplarAssassin_HeroesSlowed: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_Sniper_AssassinationKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_Sniper_HeadshotStuns: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_EarthSpirit_SmashStuns: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_EarthSpirit_GripSilences: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_ShadowShaman_ShackleKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_ShadowShaman_HexKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_Centaur_EnemiesStomped: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_Centaur_DoubleEdgeKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_Centaur_ReturnKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_EmberSpirit_EnemiesChained: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_EmberSpirit_SleightOfFistMultiKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_Puck_OrbKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_VengefulSpirit_EnemiesStunned: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_Lifestealer_RageKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_Lifestealer_OpenWoundsKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_Lifestealer_InfestKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_ElderTitan_SpiritKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_ElderTitan_GoodStomps: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_Clockwerk_RocketKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_Clockwerk_BlindRocketKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_StormSpirit_BallKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_StormSpirit_DoubleRemnantKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_StormSpirit_VortexKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_Tinker_DoubleMissileKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_Tinker_LaserKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_Techies_SuicideKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_Techies_LandMineKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_Techies_StatisTrapStuns: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_Techies_RemoteMineKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_ShadowFiend_TripleRazeKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_ShadowFiend_RequiemMultiKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_ShadowFiend_QRazeKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_ShadowFiend_WRazeKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_ShadowFiend_ERazeKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_Oracle_FatesEdictKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_Oracle_FalsePromiseSaves: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEvent_Juggernaut_OmnislashKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_SkeletonKing_SkeletonHeroKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_DarkWillow_CursedCrownTripleStuns: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Dazzle_ShallowGraveSaves: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Dazzle_PoisonTouchKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_ThreeManMeks: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Viper_PoisonAttackKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Viper_CorrosiveSkinKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_ThreeHeroVeils: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Viper_KillsDuringViperStrike: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_SolarCrestKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Tiny_TreeThrowKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Riki_BackstabKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Phoenix_ThreeHeroSupernovaStuns: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Terrorblade_MetamorphosisKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Lion_GreatFingerKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Antimage_SpellsBlockedWithAghanims: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Antimage_ThreeManManaVoids: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_ArcWarden_TempestDoubleKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_ArcWarden_SparkWraithKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Bane_BrainSapKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Bane_FiendsGripKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Batrider_TripleHeroFlamebreaks: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Batrider_DoubleHeroLassoes: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Brewmaster_KillsDuringPrimalSplit: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Bristleback_KillsUnderFourQuillStacks: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Bristleback_TripleHeroNasalGoo: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Broodmother_SpiderlingHeroKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Broodmother_KillsInsideWeb: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Centaur_ThreeHeroStampede: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_ChaosKnight_RealityRiftKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Chen_KillsWithPenitence: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_CrystalMaiden_TwoHeroCrystalNovas: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_CrystalMaiden_ThreeHeroFreezingFields: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Dazzle_ShadowWaveKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_DeathProphet_SiphonKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_DeathProphet_ExorcismKillsDuringEuls: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Disruptor_ThreeHeroKineticFieldStaticStorm: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Doom_InfernalBladeBurnKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_DrowRanger_PrecisionAuraCreepTowerKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_EmberSpirit_RemnantKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_EmberSpirit_SleightOfFistKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Enigma_MidnightPulseBlackHoleCombos: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Enigma_ThreeManBlackHoles: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_FacelessVoid_MultiHeroTimeDilation: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Gyrocopter_ThreeHeroFlakCannon: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Gyrocopter_HomingMissileKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Gyrocopter_RocketBarrageKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Huskar_KillsDuringLifeBreak: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Huskar_BurningSpearKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Invoker_MultiHeroIceWall: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Invoker_ThreeHeroEMP: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Invoker_ThreeHeroDeafeningBlast: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Invoker_MultiHeroChaosMeteor: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Jakiro_MultiHeroDualBreath: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Jakiro_IcePathMacropyreCombos: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Leshrac_PulseNovaKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Leshrac_ThreeHeroLightningStorm: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Lion_ThreeHeroFingerOfDeath: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Meepo_PoofKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Meepo_MultiHeroEarthbinds: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_NightStalker_NighttimeKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Morphling_KillsDuringReplicate: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_OgreMagi_FireblastKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_OgreMagi_IgniteKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_DominatingKillStreaks: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_MegaKillStreaks: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Alchemist_AghanimsGiven: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_VeilsLeadingToKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_DustLeadingToKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_WitchDoctor_MultiHeroCaskStuns: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Weaver_ShukuchiKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Windrunner_ShackleFocusFireKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_VengefulSpirit_VengeanceAuraIllusionKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Tusk_WalrusPunchKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Tinker_MultiHeroLasers: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_TemplarAssassin_MultiHeroPsiBlades: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Sven_KillsDuringGodsStrength: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Sniper_ThreeHeroShrapnels: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Slark_KillsDuringShadowDance: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_ShadowShaman_MultiHeroEtherShocks: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_ShadowShaman_SerpentWardShackleKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Riki_ThreeHeroTricksOfTheTrade: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Razor_EyeOfTheStormKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Pugna_LifeDrainKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_ObsidianDestroyer_SanitysEclipseKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Oracle_MultiHeroFortunesEnd: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Omniknight_PurificationKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_NightStalker_EnemyMissesUnderCripplingFear: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Warlock_ThreeHeroFatalBonds: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Riki_TricksOfTheTradeKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Earthshaker_AftershockHits10: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Earthshaker_5HeroEchoslams: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Lina_LagunaBladeHeroKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Lina_LightStrikeHeroStuns: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Earthshaker_FissureMultiStuns: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Earthshaker_TotemKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Pangolier_SwashbuckleKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Furion_EnemyHeroesTrapped: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Pangolier_HeartpiercerKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Medusa_MultiHeroStoneGaze: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Medusa_SplitShotKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Mirana_MultiHeroStarstorm: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Mirana_KillsFromMoonlightShadow: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Magnus_MultiHeroSkewers: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Magnus_MultiHeroReversePolarity: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Magnus_HeroesSlowedWithShockwave: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_NagaSiren_MultiHeroSong: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_NagaSiren_AlliesHealedBySong: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_LoneDruid_MultiHeroRoar: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_LoneDruid_BattleCryKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_WinterWyvern_ThreeHeroCurses: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Antimage_SpellsBlockedWithCounterspell: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Mars_EnemiesKilledInArena: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Mars_MultiHeroGodsRebuke: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Mars_GodsRebukeKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Snapfire_LizardBlobsKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Snapfire_TwoHeroCookieStuns: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                Custom_KillStreak: _ClassVar[CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType]
                kKillEaterEventType_Muerta_DeadShotKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Muerta_PierceTheVeilKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Muerta_MultiHeroDeadShot: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Muerta_DeadShotsIntoTheCalling: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Ringmaster_LongRangeDaggerHits: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Ringmaster_MultiHeroWhips: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Ringmaster_MultiHeroMesmerizes: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Kez_ParryCounterAttacks: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Kez_RavensVeilKills: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Kez_RaptorDanceHealing: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Kez_KillsDuringFalconRush: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Seasonal_PartyHatsStolen: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Seasonal_TallestHat: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Largo_MultiHeroFrogstomp: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]
                kKillEaterEventType_Largo_AmphibianRhapsodyKillsAndAssists: _ClassVar[
                    CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
                ]

            kills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            deaths: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            assists: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            net_worth: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            item_value: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            support_gold_spent: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            wards_placed: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            dewards: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            camps_stacked: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            last_hits: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            denies: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_Killing_Sprees: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_Godlike: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_Towers_Destroyed: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Invoker_SunstrikeKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Axe_Culls: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Axe_BattleHungerKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_LowHealthKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Invoker_TornadoKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Sven_DoubleStuns: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Sven_WarcryAssists: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Sven_CleaveDoubleKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Sven_TeleportInterrupts: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Faceless_MultiChrono: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Faceless_ChronoKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Ursa_MultiShocks: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_RoshanKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Lion_FingerKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Riki_SmokedHeroKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_HeroesRevealedWithDust: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_SkeletonKing_ReincarnationKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Skywrath_FlareKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Leshrac_SplitEarthStuns: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Mirana_MaxStunArrows: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_PhantomAssassin_CoupdeGraceCrits: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_PhantomAssassin_DaggerCrits: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Meepo_Earthbinds: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Bloodseeker_RuptureKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Slark_LeashedEnemies: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Disruptor_FountainGlimpses: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Rubick_SpellsStolen: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Rubick_UltimatesStolen: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Doom_EnemiesDoomed: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Omniknight_Purifications: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Omniknight_AlliesRepelled: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Omniknight_EnemiesRepelled: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Warlock_FiveHeroFatalBonds: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_CrystalMaiden_FrostbittenEnemies: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_CrystalMaiden_CrystalNovas: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Kunkka_DoubleHeroTorrents: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Kunkka_TripleHeroGhostShips: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_NagaSiren_EnemiesEnsnared: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_NagaSiren_TripleHeroRipTides: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Lycan_KillsDuringShapeshift: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Pudge_DismemberKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Pudge_EnemyHeroesHooked: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Pudge_HookKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Pudge_UnseenEnemyHeroesHooked: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_DrowRanger_EnemiesSilenced: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_DrowRanger_MultiHeroSilences: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_DrowRanger_SilencedKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_DrowRanger_FrostArrowKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_DragonKnight_KillsInDragonForm: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_DragonKnight_BreatheFireKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_DragonKnight_SplashKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_WitchDoctor_CaskStuns: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_WitchDoctor_MaledictKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_WitchDoctor_MultiHeroMaledicts: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_WitchDoctor_DeathWardKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Disruptor_ThunderStrikeKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Disruptor_HeroesGlimpsed: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_CrystalMaiden_FreezingFieldKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Medusa_EnemiesPetrified: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Warlock_FatalBondsKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Warlock_GolemKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Tusk_WalrusPunches: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Tusk_SnowballStuns: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Earthshaker_FissureStuns: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Earthshaker_3HeroEchoslams: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_SandKing_BurrowstrikeStuns: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_SandKing_EpicenterKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_SkywrathMage_AncientSealKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_SkywrathMage_ConcussiveShotKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Luna_LucentBeamKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Luna_EclipseKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_KeeperOfTheLight_IlluminateKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_KeeperOfTheLight_ManaLeakStuns: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_KeeperOfTheLight_TeammatesRecalled: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_LegionCommander_DuelsWon: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Beastmaster_RoarKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Beastmaster_RoarMultiKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Windrunner_FocusFireBuildings: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Windrunner_PowershotKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_PhantomAssassin_DaggerLastHits: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_PhantomAssassin_PhantomStrikeKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_DeathProphet_CryptSwarmKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_DeathProphet_ExorcismBuildingKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_DeathProphet_ExorcismSpiritsSummoned: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_DeathProphet_MultiHeroSilences: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Abaddon_MistCoilKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Abaddon_MistCoilHealed: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Abaddon_AphoticShieldKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Lich_ChainFrostTripleKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Lich_ChainFrostMultiKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Lich_ChainFrostBounces: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Ursa_EnragedKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Ursa_EarthshockKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Lina_LagunaBladeKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Lina_DragonSlaveKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Lina_LightStrikeArrayStuns: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEvent_Barracks_Destroyed: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_TemplarAssassin_MeldKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_TemplarAssassin_HeroesSlowed: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEvent_Sniper_AssassinationKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_Sniper_HeadshotStuns: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_EarthSpirit_SmashStuns: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_EarthSpirit_GripSilences: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_ShadowShaman_ShackleKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_ShadowShaman_HexKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_Centaur_EnemiesStomped: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_Centaur_DoubleEdgeKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_Centaur_ReturnKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_EmberSpirit_EnemiesChained: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEvent_EmberSpirit_SleightOfFistMultiKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEvent_Puck_OrbKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_VengefulSpirit_EnemiesStunned: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEvent_Lifestealer_RageKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_Lifestealer_OpenWoundsKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEvent_Lifestealer_InfestKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_ElderTitan_SpiritKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_ElderTitan_GoodStomps: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_Clockwerk_RocketKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_Clockwerk_BlindRocketKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEvent_StormSpirit_BallKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_StormSpirit_DoubleRemnantKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEvent_StormSpirit_VortexKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_Tinker_DoubleMissileKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_Tinker_LaserKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_Techies_SuicideKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_Techies_LandMineKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_Techies_StatisTrapStuns: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_Techies_RemoteMineKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_ShadowFiend_TripleRazeKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEvent_ShadowFiend_RequiemMultiKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEvent_ShadowFiend_QRazeKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_ShadowFiend_WRazeKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_ShadowFiend_ERazeKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_Oracle_FatesEdictKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_Oracle_FalsePromiseSaves: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEvent_Juggernaut_OmnislashKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_SkeletonKing_SkeletonHeroKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_DarkWillow_CursedCrownTripleStuns: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Dazzle_ShallowGraveSaves: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Dazzle_PoisonTouchKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_ThreeManMeks: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Viper_PoisonAttackKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Viper_CorrosiveSkinKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_ThreeHeroVeils: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Viper_KillsDuringViperStrike: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_SolarCrestKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Tiny_TreeThrowKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Riki_BackstabKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Phoenix_ThreeHeroSupernovaStuns: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Terrorblade_MetamorphosisKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Lion_GreatFingerKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Antimage_SpellsBlockedWithAghanims: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Antimage_ThreeManManaVoids: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_ArcWarden_TempestDoubleKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_ArcWarden_SparkWraithKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Bane_BrainSapKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Bane_FiendsGripKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Batrider_TripleHeroFlamebreaks: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Batrider_DoubleHeroLassoes: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Brewmaster_KillsDuringPrimalSplit: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Bristleback_KillsUnderFourQuillStacks: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Bristleback_TripleHeroNasalGoo: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Broodmother_SpiderlingHeroKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Broodmother_KillsInsideWeb: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Centaur_ThreeHeroStampede: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_ChaosKnight_RealityRiftKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Chen_KillsWithPenitence: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_CrystalMaiden_TwoHeroCrystalNovas: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_CrystalMaiden_ThreeHeroFreezingFields: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Dazzle_ShadowWaveKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_DeathProphet_SiphonKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_DeathProphet_ExorcismKillsDuringEuls: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Disruptor_ThreeHeroKineticFieldStaticStorm: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Doom_InfernalBladeBurnKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_DrowRanger_PrecisionAuraCreepTowerKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_EmberSpirit_RemnantKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_EmberSpirit_SleightOfFistKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Enigma_MidnightPulseBlackHoleCombos: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Enigma_ThreeManBlackHoles: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_FacelessVoid_MultiHeroTimeDilation: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Gyrocopter_ThreeHeroFlakCannon: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Gyrocopter_HomingMissileKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Gyrocopter_RocketBarrageKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Huskar_KillsDuringLifeBreak: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Huskar_BurningSpearKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Invoker_MultiHeroIceWall: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Invoker_ThreeHeroEMP: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Invoker_ThreeHeroDeafeningBlast: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Invoker_MultiHeroChaosMeteor: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Jakiro_MultiHeroDualBreath: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Jakiro_IcePathMacropyreCombos: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Leshrac_PulseNovaKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Leshrac_ThreeHeroLightningStorm: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Lion_ThreeHeroFingerOfDeath: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Meepo_PoofKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Meepo_MultiHeroEarthbinds: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_NightStalker_NighttimeKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Morphling_KillsDuringReplicate: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_OgreMagi_FireblastKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_OgreMagi_IgniteKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_DominatingKillStreaks: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_MegaKillStreaks: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Alchemist_AghanimsGiven: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_VeilsLeadingToKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_DustLeadingToKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_WitchDoctor_MultiHeroCaskStuns: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Weaver_ShukuchiKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Windrunner_ShackleFocusFireKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_VengefulSpirit_VengeanceAuraIllusionKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Tusk_WalrusPunchKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Tinker_MultiHeroLasers: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_TemplarAssassin_MultiHeroPsiBlades: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Sven_KillsDuringGodsStrength: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Sniper_ThreeHeroShrapnels: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Slark_KillsDuringShadowDance: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_ShadowShaman_MultiHeroEtherShocks: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_ShadowShaman_SerpentWardShackleKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Riki_ThreeHeroTricksOfTheTrade: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Razor_EyeOfTheStormKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Pugna_LifeDrainKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_ObsidianDestroyer_SanitysEclipseKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Oracle_MultiHeroFortunesEnd: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Omniknight_PurificationKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_NightStalker_EnemyMissesUnderCripplingFear: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Warlock_ThreeHeroFatalBonds: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Riki_TricksOfTheTradeKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Earthshaker_AftershockHits10: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Earthshaker_5HeroEchoslams: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Lina_LagunaBladeHeroKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Lina_LightStrikeHeroStuns: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Earthshaker_FissureMultiStuns: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Earthshaker_TotemKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Pangolier_SwashbuckleKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Furion_EnemyHeroesTrapped: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Pangolier_HeartpiercerKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Medusa_MultiHeroStoneGaze: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Medusa_SplitShotKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Mirana_MultiHeroStarstorm: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Mirana_KillsFromMoonlightShadow: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Magnus_MultiHeroSkewers: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Magnus_MultiHeroReversePolarity: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Magnus_HeroesSlowedWithShockwave: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_NagaSiren_MultiHeroSong: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_NagaSiren_AlliesHealedBySong: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_LoneDruid_MultiHeroRoar: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_LoneDruid_BattleCryKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_WinterWyvern_ThreeHeroCurses: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Antimage_SpellsBlockedWithCounterspell: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Mars_EnemiesKilledInArena: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Mars_MultiHeroGodsRebuke: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Mars_GodsRebukeKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Snapfire_LizardBlobsKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Snapfire_TwoHeroCookieStuns: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            Custom_KillStreak: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Muerta_DeadShotKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Muerta_PierceTheVeilKills: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Muerta_MultiHeroDeadShot: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Muerta_DeadShotsIntoTheCalling: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Ringmaster_LongRangeDaggerHits: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Ringmaster_MultiHeroWhips: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Ringmaster_MultiHeroMesmerizes: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Kez_ParryCounterAttacks: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Kez_RavensVeilKills: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Kez_RaptorDanceHealing: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Kez_KillsDuringFalconRush: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Seasonal_PartyHatsStolen: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Seasonal_TallestHat: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            kKillEaterEventType_Largo_MultiHeroFrogstomp: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            kKillEaterEventType_Largo_AmphibianRhapsodyKillsAndAssists: (
                CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            )
            TYPE_FIELD_NUMBER: _ClassVar[int]
            DETAIL_VALUE_FIELD_NUMBER: _ClassVar[int]
            type: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType
            detail_value: float
            def __init__(
                self,
                type: CMvpData.MvpDatum.MvpAccolade.MvpAccoladeType | str | None = ...,
                detail_value: float | None = ...,
            ) -> None: ...

        PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
        ACCOLADES_FIELD_NUMBER: _ClassVar[int]
        player_slot: int
        accolades: _containers.RepeatedCompositeFieldContainer[CMvpData.MvpDatum.MvpAccolade]
        def __init__(
            self,
            player_slot: int | None = ...,
            accolades: _Iterable[CMvpData.MvpDatum.MvpAccolade | _Mapping] | None = ...,
        ) -> None: ...

    MVPS_FIELD_NUMBER: _ClassVar[int]
    EVENT_MVPS_FIELD_NUMBER: _ClassVar[int]
    mvps: _containers.RepeatedCompositeFieldContainer[CMvpData.MvpDatum]
    event_mvps: _containers.RepeatedCompositeFieldContainer[CMvpData.MvpDatum]
    def __init__(
        self,
        mvps: _Iterable[CMvpData.MvpDatum | _Mapping] | None = ...,
        event_mvps: _Iterable[CMvpData.MvpDatum | _Mapping] | None = ...,
    ) -> None: ...
