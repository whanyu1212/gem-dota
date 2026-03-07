from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

import base_gcmessages_pb2 as _base_gcmessages_pb2
import dota_client_enums_pb2 as _dota_client_enums_pb2
import dota_gcmessages_common_lobby_pb2 as _dota_gcmessages_common_lobby_pb2
import dota_shared_enums_pb2 as _dota_shared_enums_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class EStartFindingMatchResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EStartFindingMatchResult_Invalid: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_OK: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_AlreadySearching: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_FailGeneric: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_FailedIgnore: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_MatchmakingDisabled: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_RegionOffline: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_MatchmakingCooldown: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_ClientOutOfDate: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_CompetitiveNoLowPriority: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_CompetitiveNotUnlocked: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_GameModeNotUnlocked: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_CompetitiveNotEnoughPlayTime: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_MissingInitialSkill: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_CompetitiveRankSpreadTooLarge: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_MemberAlreadyInLobby: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_MemberNotVACVerified: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_WeekendTourneyBadPartySize: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_WeekendTourneyTeamBuyInTooSmall: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_WeekendTourneyIndividualBuyInTooLarge: _ClassVar[
        EStartFindingMatchResult
    ]
    k_EStartFindingMatchResult_WeekendTourneyTeamBuyInTooLarge: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_MemberMissingEventOwnership: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_WeekendTourneyNotUnlocked: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_WeekendTourneyRecentParticipation: _ClassVar[
        EStartFindingMatchResult
    ]
    k_EStartFindingMatchResult_MemberMissingAnchoredPhoneNumber: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_NotMemberOfClan: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_CoachesChallengeBadPartySize: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_CoachesChallengeRequirementsNotMet: _ClassVar[
        EStartFindingMatchResult
    ]
    k_EStartFindingMatchResult_InvalidRoleSelections: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_PhoneNumberDiscrepancy: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_NoQueuePoints: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_MemberMissingGauntletFlag: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_MemberGauntletTooRecent: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_DifficultyNotUnlocked: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_CoachesNotAllowedInParty: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_MatchmakingBusy: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_SteamChinaBanned: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_SteamChinaInvalidMixedParty: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_RestrictedFromRanked: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_RankPreventsParties: _ClassVar[EStartFindingMatchResult]
    k_EStartFindingMatchResult_RegisteredNameRequired: _ClassVar[EStartFindingMatchResult]

k_EStartFindingMatchResult_Invalid: EStartFindingMatchResult
k_EStartFindingMatchResult_OK: EStartFindingMatchResult
k_EStartFindingMatchResult_AlreadySearching: EStartFindingMatchResult
k_EStartFindingMatchResult_FailGeneric: EStartFindingMatchResult
k_EStartFindingMatchResult_FailedIgnore: EStartFindingMatchResult
k_EStartFindingMatchResult_MatchmakingDisabled: EStartFindingMatchResult
k_EStartFindingMatchResult_RegionOffline: EStartFindingMatchResult
k_EStartFindingMatchResult_MatchmakingCooldown: EStartFindingMatchResult
k_EStartFindingMatchResult_ClientOutOfDate: EStartFindingMatchResult
k_EStartFindingMatchResult_CompetitiveNoLowPriority: EStartFindingMatchResult
k_EStartFindingMatchResult_CompetitiveNotUnlocked: EStartFindingMatchResult
k_EStartFindingMatchResult_GameModeNotUnlocked: EStartFindingMatchResult
k_EStartFindingMatchResult_CompetitiveNotEnoughPlayTime: EStartFindingMatchResult
k_EStartFindingMatchResult_MissingInitialSkill: EStartFindingMatchResult
k_EStartFindingMatchResult_CompetitiveRankSpreadTooLarge: EStartFindingMatchResult
k_EStartFindingMatchResult_MemberAlreadyInLobby: EStartFindingMatchResult
k_EStartFindingMatchResult_MemberNotVACVerified: EStartFindingMatchResult
k_EStartFindingMatchResult_WeekendTourneyBadPartySize: EStartFindingMatchResult
k_EStartFindingMatchResult_WeekendTourneyTeamBuyInTooSmall: EStartFindingMatchResult
k_EStartFindingMatchResult_WeekendTourneyIndividualBuyInTooLarge: EStartFindingMatchResult
k_EStartFindingMatchResult_WeekendTourneyTeamBuyInTooLarge: EStartFindingMatchResult
k_EStartFindingMatchResult_MemberMissingEventOwnership: EStartFindingMatchResult
k_EStartFindingMatchResult_WeekendTourneyNotUnlocked: EStartFindingMatchResult
k_EStartFindingMatchResult_WeekendTourneyRecentParticipation: EStartFindingMatchResult
k_EStartFindingMatchResult_MemberMissingAnchoredPhoneNumber: EStartFindingMatchResult
k_EStartFindingMatchResult_NotMemberOfClan: EStartFindingMatchResult
k_EStartFindingMatchResult_CoachesChallengeBadPartySize: EStartFindingMatchResult
k_EStartFindingMatchResult_CoachesChallengeRequirementsNotMet: EStartFindingMatchResult
k_EStartFindingMatchResult_InvalidRoleSelections: EStartFindingMatchResult
k_EStartFindingMatchResult_PhoneNumberDiscrepancy: EStartFindingMatchResult
k_EStartFindingMatchResult_NoQueuePoints: EStartFindingMatchResult
k_EStartFindingMatchResult_MemberMissingGauntletFlag: EStartFindingMatchResult
k_EStartFindingMatchResult_MemberGauntletTooRecent: EStartFindingMatchResult
k_EStartFindingMatchResult_DifficultyNotUnlocked: EStartFindingMatchResult
k_EStartFindingMatchResult_CoachesNotAllowedInParty: EStartFindingMatchResult
k_EStartFindingMatchResult_MatchmakingBusy: EStartFindingMatchResult
k_EStartFindingMatchResult_SteamChinaBanned: EStartFindingMatchResult
k_EStartFindingMatchResult_SteamChinaInvalidMixedParty: EStartFindingMatchResult
k_EStartFindingMatchResult_RestrictedFromRanked: EStartFindingMatchResult
k_EStartFindingMatchResult_RankPreventsParties: EStartFindingMatchResult
k_EStartFindingMatchResult_RegisteredNameRequired: EStartFindingMatchResult

class CMsgStartFindingMatch(_message.Message):
    __slots__ = (
        "key",
        "matchgroups",
        "client_version",
        "game_modes",
        "match_type",
        "matchlanguages",
        "team_id",
        "game_language_enum",
        "game_language_name",
        "ping_data",
        "region_select_flags",
        "solo_queue",
        "steam_clan_account_id",
        "is_challenge_match",
        "lane_selection_flags",
        "high_priority_disabled",
        "disable_experimental_gameplay",
        "custom_game_difficulty_mask",
        "bot_difficulty_mask",
        "bot_script_index_mask",
    )
    KEY_FIELD_NUMBER: _ClassVar[int]
    MATCHGROUPS_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    GAME_MODES_FIELD_NUMBER: _ClassVar[int]
    MATCH_TYPE_FIELD_NUMBER: _ClassVar[int]
    MATCHLANGUAGES_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    GAME_LANGUAGE_ENUM_FIELD_NUMBER: _ClassVar[int]
    GAME_LANGUAGE_NAME_FIELD_NUMBER: _ClassVar[int]
    PING_DATA_FIELD_NUMBER: _ClassVar[int]
    REGION_SELECT_FLAGS_FIELD_NUMBER: _ClassVar[int]
    SOLO_QUEUE_FIELD_NUMBER: _ClassVar[int]
    STEAM_CLAN_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    IS_CHALLENGE_MATCH_FIELD_NUMBER: _ClassVar[int]
    LANE_SELECTION_FLAGS_FIELD_NUMBER: _ClassVar[int]
    HIGH_PRIORITY_DISABLED_FIELD_NUMBER: _ClassVar[int]
    DISABLE_EXPERIMENTAL_GAMEPLAY_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_DIFFICULTY_MASK_FIELD_NUMBER: _ClassVar[int]
    BOT_DIFFICULTY_MASK_FIELD_NUMBER: _ClassVar[int]
    BOT_SCRIPT_INDEX_MASK_FIELD_NUMBER: _ClassVar[int]
    key: str
    matchgroups: int
    client_version: int
    game_modes: int
    match_type: _dota_shared_enums_pb2.MatchType
    matchlanguages: int
    team_id: int
    game_language_enum: _dota_shared_enums_pb2.MatchLanguages
    game_language_name: str
    ping_data: _base_gcmessages_pb2.CMsgClientPingData
    region_select_flags: int
    solo_queue: bool
    steam_clan_account_id: int
    is_challenge_match: bool
    lane_selection_flags: int
    high_priority_disabled: bool
    disable_experimental_gameplay: bool
    custom_game_difficulty_mask: int
    bot_difficulty_mask: int
    bot_script_index_mask: int
    def __init__(
        self,
        key: str | None = ...,
        matchgroups: int | None = ...,
        client_version: int | None = ...,
        game_modes: int | None = ...,
        match_type: _dota_shared_enums_pb2.MatchType | str | None = ...,
        matchlanguages: int | None = ...,
        team_id: int | None = ...,
        game_language_enum: _dota_shared_enums_pb2.MatchLanguages | str | None = ...,
        game_language_name: str | None = ...,
        ping_data: _base_gcmessages_pb2.CMsgClientPingData | _Mapping | None = ...,
        region_select_flags: int | None = ...,
        solo_queue: bool = ...,
        steam_clan_account_id: int | None = ...,
        is_challenge_match: bool = ...,
        lane_selection_flags: int | None = ...,
        high_priority_disabled: bool = ...,
        disable_experimental_gameplay: bool = ...,
        custom_game_difficulty_mask: int | None = ...,
        bot_difficulty_mask: int | None = ...,
        bot_script_index_mask: int | None = ...,
    ) -> None: ...

class CMsgStartFindingMatchResult(_message.Message):
    __slots__ = (
        "legacy_generic_eresult",
        "result",
        "error_token",
        "debug_message",
        "responsible_party_members",
        "result_metadata",
    )
    LEGACY_GENERIC_ERESULT_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    ERROR_TOKEN_FIELD_NUMBER: _ClassVar[int]
    DEBUG_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    RESPONSIBLE_PARTY_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    RESULT_METADATA_FIELD_NUMBER: _ClassVar[int]
    legacy_generic_eresult: int
    result: EStartFindingMatchResult
    error_token: str
    debug_message: str
    responsible_party_members: _containers.RepeatedScalarFieldContainer[int]
    result_metadata: int
    def __init__(
        self,
        legacy_generic_eresult: int | None = ...,
        result: EStartFindingMatchResult | str | None = ...,
        error_token: str | None = ...,
        debug_message: str | None = ...,
        responsible_party_members: _Iterable[int] | None = ...,
        result_metadata: int | None = ...,
    ) -> None: ...

class CMsgStopFindingMatch(_message.Message):
    __slots__ = ("accept_cooldown",)
    ACCEPT_COOLDOWN_FIELD_NUMBER: _ClassVar[int]
    accept_cooldown: bool
    def __init__(self, accept_cooldown: bool = ...) -> None: ...

class CMsgPartyBuilderOptions(_message.Message):
    __slots__ = ("additional_slots", "match_type", "matchgroups", "client_version", "language")
    ADDITIONAL_SLOTS_FIELD_NUMBER: _ClassVar[int]
    MATCH_TYPE_FIELD_NUMBER: _ClassVar[int]
    MATCHGROUPS_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    additional_slots: int
    match_type: _dota_shared_enums_pb2.MatchType
    matchgroups: int
    client_version: int
    language: _dota_shared_enums_pb2.MatchLanguages
    def __init__(
        self,
        additional_slots: int | None = ...,
        match_type: _dota_shared_enums_pb2.MatchType | str | None = ...,
        matchgroups: int | None = ...,
        client_version: int | None = ...,
        language: _dota_shared_enums_pb2.MatchLanguages | str | None = ...,
    ) -> None: ...

class CMsgReadyUp(_message.Message):
    __slots__ = ("state", "ready_up_key", "hardware_specs")
    STATE_FIELD_NUMBER: _ClassVar[int]
    READY_UP_KEY_FIELD_NUMBER: _ClassVar[int]
    HARDWARE_SPECS_FIELD_NUMBER: _ClassVar[int]
    state: _dota_shared_enums_pb2.DOTALobbyReadyState
    ready_up_key: int
    hardware_specs: _dota_shared_enums_pb2.CDOTAClientHardwareSpecs
    def __init__(
        self,
        state: _dota_shared_enums_pb2.DOTALobbyReadyState | str | None = ...,
        ready_up_key: int | None = ...,
        hardware_specs: _dota_shared_enums_pb2.CDOTAClientHardwareSpecs | _Mapping | None = ...,
    ) -> None: ...

class CMsgReadyUpStatus(_message.Message):
    __slots__ = (
        "lobby_id",
        "accepted_ids",
        "declined_ids",
        "accepted_indices",
        "declined_indices",
        "local_ready_state",
    )
    LOBBY_ID_FIELD_NUMBER: _ClassVar[int]
    ACCEPTED_IDS_FIELD_NUMBER: _ClassVar[int]
    DECLINED_IDS_FIELD_NUMBER: _ClassVar[int]
    ACCEPTED_INDICES_FIELD_NUMBER: _ClassVar[int]
    DECLINED_INDICES_FIELD_NUMBER: _ClassVar[int]
    LOCAL_READY_STATE_FIELD_NUMBER: _ClassVar[int]
    lobby_id: int
    accepted_ids: _containers.RepeatedScalarFieldContainer[int]
    declined_ids: _containers.RepeatedScalarFieldContainer[int]
    accepted_indices: _containers.RepeatedScalarFieldContainer[int]
    declined_indices: _containers.RepeatedScalarFieldContainer[int]
    local_ready_state: _dota_shared_enums_pb2.DOTALobbyReadyState
    def __init__(
        self,
        lobby_id: int | None = ...,
        accepted_ids: _Iterable[int] | None = ...,
        declined_ids: _Iterable[int] | None = ...,
        accepted_indices: _Iterable[int] | None = ...,
        declined_indices: _Iterable[int] | None = ...,
        local_ready_state: _dota_shared_enums_pb2.DOTALobbyReadyState | str | None = ...,
    ) -> None: ...

class CMsgAbandonCurrentGame(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgLobbyScenarioSave(_message.Message):
    __slots__ = ("version", "data")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    version: int
    data: bytes
    def __init__(self, version: int | None = ..., data: bytes | None = ...) -> None: ...

class CMsgPracticeLobbySetDetails(_message.Message):
    __slots__ = (
        "lobby_id",
        "game_name",
        "team_details",
        "server_region",
        "game_mode",
        "cm_pick",
        "bot_difficulty_radiant",
        "allow_cheats",
        "fill_with_bots",
        "allow_spectating",
        "pass_key",
        "leagueid",
        "penalty_level_radiant",
        "penalty_level_dire",
        "series_type",
        "radiant_series_wins",
        "dire_series_wins",
        "allchat",
        "dota_tv_delay",
        "lan",
        "custom_game_mode",
        "custom_map_name",
        "custom_difficulty",
        "custom_game_id",
        "custom_min_players",
        "custom_max_players",
        "visibility",
        "custom_game_crc",
        "custom_game_timestamp",
        "previous_match_override",
        "pause_setting",
        "bot_difficulty_dire",
        "bot_radiant",
        "bot_dire",
        "selection_priority_rules",
        "custom_game_penalties",
        "lan_host_ping_location",
        "league_node_id",
        "requested_hero_ids",
        "scenario_save",
        "ability_draft_specific_details",
        "do_player_draft",
        "requested_hero_teams",
    )
    class AbilityDraftSpecificDetails(_message.Message):
        __slots__ = ("shuffle_draft_order",)
        SHUFFLE_DRAFT_ORDER_FIELD_NUMBER: _ClassVar[int]
        shuffle_draft_order: bool
        def __init__(self, shuffle_draft_order: bool = ...) -> None: ...

    LOBBY_ID_FIELD_NUMBER: _ClassVar[int]
    GAME_NAME_FIELD_NUMBER: _ClassVar[int]
    TEAM_DETAILS_FIELD_NUMBER: _ClassVar[int]
    SERVER_REGION_FIELD_NUMBER: _ClassVar[int]
    GAME_MODE_FIELD_NUMBER: _ClassVar[int]
    CM_PICK_FIELD_NUMBER: _ClassVar[int]
    BOT_DIFFICULTY_RADIANT_FIELD_NUMBER: _ClassVar[int]
    ALLOW_CHEATS_FIELD_NUMBER: _ClassVar[int]
    FILL_WITH_BOTS_FIELD_NUMBER: _ClassVar[int]
    ALLOW_SPECTATING_FIELD_NUMBER: _ClassVar[int]
    PASS_KEY_FIELD_NUMBER: _ClassVar[int]
    LEAGUEID_FIELD_NUMBER: _ClassVar[int]
    PENALTY_LEVEL_RADIANT_FIELD_NUMBER: _ClassVar[int]
    PENALTY_LEVEL_DIRE_FIELD_NUMBER: _ClassVar[int]
    SERIES_TYPE_FIELD_NUMBER: _ClassVar[int]
    RADIANT_SERIES_WINS_FIELD_NUMBER: _ClassVar[int]
    DIRE_SERIES_WINS_FIELD_NUMBER: _ClassVar[int]
    ALLCHAT_FIELD_NUMBER: _ClassVar[int]
    DOTA_TV_DELAY_FIELD_NUMBER: _ClassVar[int]
    LAN_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_MODE_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_MAP_NAME_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_DIFFICULTY_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_ID_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_MIN_PLAYERS_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_MAX_PLAYERS_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_CRC_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_MATCH_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    PAUSE_SETTING_FIELD_NUMBER: _ClassVar[int]
    BOT_DIFFICULTY_DIRE_FIELD_NUMBER: _ClassVar[int]
    BOT_RADIANT_FIELD_NUMBER: _ClassVar[int]
    BOT_DIRE_FIELD_NUMBER: _ClassVar[int]
    SELECTION_PRIORITY_RULES_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_PENALTIES_FIELD_NUMBER: _ClassVar[int]
    LAN_HOST_PING_LOCATION_FIELD_NUMBER: _ClassVar[int]
    LEAGUE_NODE_ID_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_HERO_IDS_FIELD_NUMBER: _ClassVar[int]
    SCENARIO_SAVE_FIELD_NUMBER: _ClassVar[int]
    ABILITY_DRAFT_SPECIFIC_DETAILS_FIELD_NUMBER: _ClassVar[int]
    DO_PLAYER_DRAFT_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_HERO_TEAMS_FIELD_NUMBER: _ClassVar[int]
    lobby_id: int
    game_name: str
    team_details: _containers.RepeatedCompositeFieldContainer[
        _dota_gcmessages_common_lobby_pb2.CLobbyTeamDetails
    ]
    server_region: int
    game_mode: int
    cm_pick: _dota_shared_enums_pb2.DOTA_CM_PICK
    bot_difficulty_radiant: _dota_shared_enums_pb2.DOTABotDifficulty
    allow_cheats: bool
    fill_with_bots: bool
    allow_spectating: bool
    pass_key: str
    leagueid: int
    penalty_level_radiant: int
    penalty_level_dire: int
    series_type: int
    radiant_series_wins: int
    dire_series_wins: int
    allchat: bool
    dota_tv_delay: _dota_gcmessages_common_lobby_pb2.LobbyDotaTVDelay
    lan: bool
    custom_game_mode: str
    custom_map_name: str
    custom_difficulty: int
    custom_game_id: int
    custom_min_players: int
    custom_max_players: int
    visibility: _dota_shared_enums_pb2.DOTALobbyVisibility
    custom_game_crc: int
    custom_game_timestamp: int
    previous_match_override: int
    pause_setting: _dota_gcmessages_common_lobby_pb2.LobbyDotaPauseSetting
    bot_difficulty_dire: _dota_shared_enums_pb2.DOTABotDifficulty
    bot_radiant: int
    bot_dire: int
    selection_priority_rules: _dota_shared_enums_pb2.DOTASelectionPriorityRules
    custom_game_penalties: bool
    lan_host_ping_location: str
    league_node_id: int
    requested_hero_ids: _containers.RepeatedScalarFieldContainer[int]
    scenario_save: CMsgLobbyScenarioSave
    ability_draft_specific_details: CMsgPracticeLobbySetDetails.AbilityDraftSpecificDetails
    do_player_draft: bool
    requested_hero_teams: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        lobby_id: int | None = ...,
        game_name: str | None = ...,
        team_details: _Iterable[_dota_gcmessages_common_lobby_pb2.CLobbyTeamDetails | _Mapping]
        | None = ...,
        server_region: int | None = ...,
        game_mode: int | None = ...,
        cm_pick: _dota_shared_enums_pb2.DOTA_CM_PICK | str | None = ...,
        bot_difficulty_radiant: _dota_shared_enums_pb2.DOTABotDifficulty | str | None = ...,
        allow_cheats: bool = ...,
        fill_with_bots: bool = ...,
        allow_spectating: bool = ...,
        pass_key: str | None = ...,
        leagueid: int | None = ...,
        penalty_level_radiant: int | None = ...,
        penalty_level_dire: int | None = ...,
        series_type: int | None = ...,
        radiant_series_wins: int | None = ...,
        dire_series_wins: int | None = ...,
        allchat: bool = ...,
        dota_tv_delay: _dota_gcmessages_common_lobby_pb2.LobbyDotaTVDelay | str | None = ...,
        lan: bool = ...,
        custom_game_mode: str | None = ...,
        custom_map_name: str | None = ...,
        custom_difficulty: int | None = ...,
        custom_game_id: int | None = ...,
        custom_min_players: int | None = ...,
        custom_max_players: int | None = ...,
        visibility: _dota_shared_enums_pb2.DOTALobbyVisibility | str | None = ...,
        custom_game_crc: int | None = ...,
        custom_game_timestamp: int | None = ...,
        previous_match_override: int | None = ...,
        pause_setting: _dota_gcmessages_common_lobby_pb2.LobbyDotaPauseSetting | str | None = ...,
        bot_difficulty_dire: _dota_shared_enums_pb2.DOTABotDifficulty | str | None = ...,
        bot_radiant: int | None = ...,
        bot_dire: int | None = ...,
        selection_priority_rules: _dota_shared_enums_pb2.DOTASelectionPriorityRules
        | str
        | None = ...,
        custom_game_penalties: bool = ...,
        lan_host_ping_location: str | None = ...,
        league_node_id: int | None = ...,
        requested_hero_ids: _Iterable[int] | None = ...,
        scenario_save: CMsgLobbyScenarioSave | _Mapping | None = ...,
        ability_draft_specific_details: CMsgPracticeLobbySetDetails.AbilityDraftSpecificDetails
        | _Mapping
        | None = ...,
        do_player_draft: bool = ...,
        requested_hero_teams: _Iterable[int] | None = ...,
    ) -> None: ...

class CMsgPracticeLobbyCreate(_message.Message):
    __slots__ = ("search_key", "pass_key", "client_version", "lobby_details")
    SEARCH_KEY_FIELD_NUMBER: _ClassVar[int]
    PASS_KEY_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    LOBBY_DETAILS_FIELD_NUMBER: _ClassVar[int]
    search_key: str
    pass_key: str
    client_version: int
    lobby_details: CMsgPracticeLobbySetDetails
    def __init__(
        self,
        search_key: str | None = ...,
        pass_key: str | None = ...,
        client_version: int | None = ...,
        lobby_details: CMsgPracticeLobbySetDetails | _Mapping | None = ...,
    ) -> None: ...

class CMsgPracticeLobbySetTeamSlot(_message.Message):
    __slots__ = ("team", "slot", "bot_difficulty")
    TEAM_FIELD_NUMBER: _ClassVar[int]
    SLOT_FIELD_NUMBER: _ClassVar[int]
    BOT_DIFFICULTY_FIELD_NUMBER: _ClassVar[int]
    team: _dota_shared_enums_pb2.DOTA_GC_TEAM
    slot: int
    bot_difficulty: _dota_shared_enums_pb2.DOTABotDifficulty
    def __init__(
        self,
        team: _dota_shared_enums_pb2.DOTA_GC_TEAM | str | None = ...,
        slot: int | None = ...,
        bot_difficulty: _dota_shared_enums_pb2.DOTABotDifficulty | str | None = ...,
    ) -> None: ...

class CMsgPracticeLobbySetCoach(_message.Message):
    __slots__ = ("team",)
    TEAM_FIELD_NUMBER: _ClassVar[int]
    team: _dota_shared_enums_pb2.DOTA_GC_TEAM
    def __init__(self, team: _dota_shared_enums_pb2.DOTA_GC_TEAM | str | None = ...) -> None: ...

class CMsgPracticeLobbyJoinBroadcastChannel(_message.Message):
    __slots__ = (
        "channel",
        "preferred_description",
        "preferred_country_code",
        "preferred_language_code",
    )
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    PREFERRED_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PREFERRED_COUNTRY_CODE_FIELD_NUMBER: _ClassVar[int]
    PREFERRED_LANGUAGE_CODE_FIELD_NUMBER: _ClassVar[int]
    channel: int
    preferred_description: str
    preferred_country_code: str
    preferred_language_code: str
    def __init__(
        self,
        channel: int | None = ...,
        preferred_description: str | None = ...,
        preferred_country_code: str | None = ...,
        preferred_language_code: str | None = ...,
    ) -> None: ...

class CMsgPracticeLobbyCloseBroadcastChannel(_message.Message):
    __slots__ = ("channel",)
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    channel: int
    def __init__(self, channel: int | None = ...) -> None: ...

class CMsgPracticeLobbyToggleBroadcastChannelCameramanStatus(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgPracticeLobbyKick(_message.Message):
    __slots__ = ("account_id",)
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    def __init__(self, account_id: int | None = ...) -> None: ...

class CMsgPracticeLobbyKickFromTeam(_message.Message):
    __slots__ = ("account_id",)
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    def __init__(self, account_id: int | None = ...) -> None: ...

class CMsgPracticeLobbyLeave(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgPracticeLobbyLaunch(_message.Message):
    __slots__ = ("client_version",)
    CLIENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    client_version: int
    def __init__(self, client_version: int | None = ...) -> None: ...

class CMsgApplyTeamToPracticeLobby(_message.Message):
    __slots__ = ("team_id",)
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    team_id: int
    def __init__(self, team_id: int | None = ...) -> None: ...

class CMsgPracticeLobbyList(_message.Message):
    __slots__ = ("pass_key", "region", "game_mode")
    PASS_KEY_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    GAME_MODE_FIELD_NUMBER: _ClassVar[int]
    pass_key: str
    region: int
    game_mode: _dota_shared_enums_pb2.DOTA_GameMode
    def __init__(
        self,
        pass_key: str | None = ...,
        region: int | None = ...,
        game_mode: _dota_shared_enums_pb2.DOTA_GameMode | str | None = ...,
    ) -> None: ...

class CMsgPracticeLobbyListResponseEntry(_message.Message):
    __slots__ = (
        "id",
        "members",
        "requires_pass_key",
        "leader_account_id",
        "name",
        "custom_game_mode",
        "game_mode",
        "friend_present",
        "players",
        "custom_map_name",
        "max_player_count",
        "server_region",
        "league_id",
        "lan_host_ping_location",
        "min_player_count",
        "penalties_enabled",
    )
    class CLobbyMember(_message.Message):
        __slots__ = ("account_id", "player_name")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        PLAYER_NAME_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        player_name: str
        def __init__(self, account_id: int | None = ..., player_name: str | None = ...) -> None: ...

    ID_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    REQUIRES_PASS_KEY_FIELD_NUMBER: _ClassVar[int]
    LEADER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_MODE_FIELD_NUMBER: _ClassVar[int]
    GAME_MODE_FIELD_NUMBER: _ClassVar[int]
    FRIEND_PRESENT_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_MAP_NAME_FIELD_NUMBER: _ClassVar[int]
    MAX_PLAYER_COUNT_FIELD_NUMBER: _ClassVar[int]
    SERVER_REGION_FIELD_NUMBER: _ClassVar[int]
    LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    LAN_HOST_PING_LOCATION_FIELD_NUMBER: _ClassVar[int]
    MIN_PLAYER_COUNT_FIELD_NUMBER: _ClassVar[int]
    PENALTIES_ENABLED_FIELD_NUMBER: _ClassVar[int]
    id: int
    members: _containers.RepeatedCompositeFieldContainer[
        CMsgPracticeLobbyListResponseEntry.CLobbyMember
    ]
    requires_pass_key: bool
    leader_account_id: int
    name: str
    custom_game_mode: str
    game_mode: _dota_shared_enums_pb2.DOTA_GameMode
    friend_present: bool
    players: int
    custom_map_name: str
    max_player_count: int
    server_region: int
    league_id: int
    lan_host_ping_location: str
    min_player_count: int
    penalties_enabled: bool
    def __init__(
        self,
        id: int | None = ...,
        members: _Iterable[CMsgPracticeLobbyListResponseEntry.CLobbyMember | _Mapping] | None = ...,
        requires_pass_key: bool = ...,
        leader_account_id: int | None = ...,
        name: str | None = ...,
        custom_game_mode: str | None = ...,
        game_mode: _dota_shared_enums_pb2.DOTA_GameMode | str | None = ...,
        friend_present: bool = ...,
        players: int | None = ...,
        custom_map_name: str | None = ...,
        max_player_count: int | None = ...,
        server_region: int | None = ...,
        league_id: int | None = ...,
        lan_host_ping_location: str | None = ...,
        min_player_count: int | None = ...,
        penalties_enabled: bool = ...,
    ) -> None: ...

class CMsgPracticeLobbyListResponse(_message.Message):
    __slots__ = ("lobbies",)
    LOBBIES_FIELD_NUMBER: _ClassVar[int]
    lobbies: _containers.RepeatedCompositeFieldContainer[CMsgPracticeLobbyListResponseEntry]
    def __init__(
        self, lobbies: _Iterable[CMsgPracticeLobbyListResponseEntry | _Mapping] | None = ...
    ) -> None: ...

class CMsgLobbyList(_message.Message):
    __slots__ = ("server_region", "game_mode")
    SERVER_REGION_FIELD_NUMBER: _ClassVar[int]
    GAME_MODE_FIELD_NUMBER: _ClassVar[int]
    server_region: int
    game_mode: _dota_shared_enums_pb2.DOTA_GameMode
    def __init__(
        self,
        server_region: int | None = ...,
        game_mode: _dota_shared_enums_pb2.DOTA_GameMode | str | None = ...,
    ) -> None: ...

class CMsgLobbyListResponse(_message.Message):
    __slots__ = ("lobbies",)
    LOBBIES_FIELD_NUMBER: _ClassVar[int]
    lobbies: _containers.RepeatedCompositeFieldContainer[CMsgPracticeLobbyListResponseEntry]
    def __init__(
        self, lobbies: _Iterable[CMsgPracticeLobbyListResponseEntry | _Mapping] | None = ...
    ) -> None: ...

class CMsgPracticeLobbyJoin(_message.Message):
    __slots__ = (
        "lobby_id",
        "client_version",
        "pass_key",
        "custom_game_crc",
        "custom_game_timestamp",
    )
    LOBBY_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    PASS_KEY_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_CRC_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    lobby_id: int
    client_version: int
    pass_key: str
    custom_game_crc: int
    custom_game_timestamp: int
    def __init__(
        self,
        lobby_id: int | None = ...,
        client_version: int | None = ...,
        pass_key: str | None = ...,
        custom_game_crc: int | None = ...,
        custom_game_timestamp: int | None = ...,
    ) -> None: ...

class CMsgPracticeLobbyJoinResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: _dota_shared_enums_pb2.DOTAJoinLobbyResult
    def __init__(
        self, result: _dota_shared_enums_pb2.DOTAJoinLobbyResult | str | None = ...
    ) -> None: ...

class CMsgFriendPracticeLobbyListRequest(_message.Message):
    __slots__ = ("friends",)
    FRIENDS_FIELD_NUMBER: _ClassVar[int]
    friends: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, friends: _Iterable[int] | None = ...) -> None: ...

class CMsgFriendPracticeLobbyListResponse(_message.Message):
    __slots__ = ("lobbies",)
    LOBBIES_FIELD_NUMBER: _ClassVar[int]
    lobbies: _containers.RepeatedCompositeFieldContainer[CMsgPracticeLobbyListResponseEntry]
    def __init__(
        self, lobbies: _Iterable[CMsgPracticeLobbyListResponseEntry | _Mapping] | None = ...
    ) -> None: ...

class CMsgJoinableCustomGameModesRequest(_message.Message):
    __slots__ = ("server_region",)
    SERVER_REGION_FIELD_NUMBER: _ClassVar[int]
    server_region: int
    def __init__(self, server_region: int | None = ...) -> None: ...

class CMsgJoinableCustomGameModesResponseEntry(_message.Message):
    __slots__ = ("custom_game_id", "lobby_count", "player_count")
    CUSTOM_GAME_ID_FIELD_NUMBER: _ClassVar[int]
    LOBBY_COUNT_FIELD_NUMBER: _ClassVar[int]
    PLAYER_COUNT_FIELD_NUMBER: _ClassVar[int]
    custom_game_id: int
    lobby_count: int
    player_count: int
    def __init__(
        self,
        custom_game_id: int | None = ...,
        lobby_count: int | None = ...,
        player_count: int | None = ...,
    ) -> None: ...

class CMsgJoinableCustomGameModesResponse(_message.Message):
    __slots__ = ("game_modes",)
    GAME_MODES_FIELD_NUMBER: _ClassVar[int]
    game_modes: _containers.RepeatedCompositeFieldContainer[
        CMsgJoinableCustomGameModesResponseEntry
    ]
    def __init__(
        self,
        game_modes: _Iterable[CMsgJoinableCustomGameModesResponseEntry | _Mapping] | None = ...,
    ) -> None: ...

class CMsgJoinableCustomLobbiesRequest(_message.Message):
    __slots__ = ("server_region", "custom_game_id")
    SERVER_REGION_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_ID_FIELD_NUMBER: _ClassVar[int]
    server_region: int
    custom_game_id: int
    def __init__(
        self, server_region: int | None = ..., custom_game_id: int | None = ...
    ) -> None: ...

class CMsgJoinableCustomLobbiesResponseEntry(_message.Message):
    __slots__ = (
        "lobby_id",
        "custom_game_id",
        "lobby_name",
        "member_count",
        "leader_account_id",
        "leader_name",
        "custom_map_name",
        "max_player_count",
        "server_region",
        "has_pass_key",
        "lan_host_ping_location",
        "lobby_creation_time",
        "custom_game_timestamp",
        "custom_game_crc",
        "min_player_count",
        "penalties_enabled",
    )
    LOBBY_ID_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_ID_FIELD_NUMBER: _ClassVar[int]
    LOBBY_NAME_FIELD_NUMBER: _ClassVar[int]
    MEMBER_COUNT_FIELD_NUMBER: _ClassVar[int]
    LEADER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    LEADER_NAME_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_MAP_NAME_FIELD_NUMBER: _ClassVar[int]
    MAX_PLAYER_COUNT_FIELD_NUMBER: _ClassVar[int]
    SERVER_REGION_FIELD_NUMBER: _ClassVar[int]
    HAS_PASS_KEY_FIELD_NUMBER: _ClassVar[int]
    LAN_HOST_PING_LOCATION_FIELD_NUMBER: _ClassVar[int]
    LOBBY_CREATION_TIME_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_CRC_FIELD_NUMBER: _ClassVar[int]
    MIN_PLAYER_COUNT_FIELD_NUMBER: _ClassVar[int]
    PENALTIES_ENABLED_FIELD_NUMBER: _ClassVar[int]
    lobby_id: int
    custom_game_id: int
    lobby_name: str
    member_count: int
    leader_account_id: int
    leader_name: str
    custom_map_name: str
    max_player_count: int
    server_region: int
    has_pass_key: bool
    lan_host_ping_location: str
    lobby_creation_time: int
    custom_game_timestamp: int
    custom_game_crc: int
    min_player_count: int
    penalties_enabled: bool
    def __init__(
        self,
        lobby_id: int | None = ...,
        custom_game_id: int | None = ...,
        lobby_name: str | None = ...,
        member_count: int | None = ...,
        leader_account_id: int | None = ...,
        leader_name: str | None = ...,
        custom_map_name: str | None = ...,
        max_player_count: int | None = ...,
        server_region: int | None = ...,
        has_pass_key: bool = ...,
        lan_host_ping_location: str | None = ...,
        lobby_creation_time: int | None = ...,
        custom_game_timestamp: int | None = ...,
        custom_game_crc: int | None = ...,
        min_player_count: int | None = ...,
        penalties_enabled: bool = ...,
    ) -> None: ...

class CMsgJoinableCustomLobbiesResponse(_message.Message):
    __slots__ = ("lobbies",)
    LOBBIES_FIELD_NUMBER: _ClassVar[int]
    lobbies: _containers.RepeatedCompositeFieldContainer[CMsgJoinableCustomLobbiesResponseEntry]
    def __init__(
        self, lobbies: _Iterable[CMsgJoinableCustomLobbiesResponseEntry | _Mapping] | None = ...
    ) -> None: ...

class CMsgQuickJoinCustomLobby(_message.Message):
    __slots__ = (
        "legacy_server_region",
        "custom_game_id",
        "client_version",
        "create_lobby_details",
        "allow_any_map",
        "legacy_region_pings",
        "ping_data",
    )
    class LegacyRegionPing(_message.Message):
        __slots__ = ("server_region", "ping", "region_code")
        SERVER_REGION_FIELD_NUMBER: _ClassVar[int]
        PING_FIELD_NUMBER: _ClassVar[int]
        REGION_CODE_FIELD_NUMBER: _ClassVar[int]
        server_region: int
        ping: int
        region_code: int
        def __init__(
            self,
            server_region: int | None = ...,
            ping: int | None = ...,
            region_code: int | None = ...,
        ) -> None: ...

    LEGACY_SERVER_REGION_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    CREATE_LOBBY_DETAILS_FIELD_NUMBER: _ClassVar[int]
    ALLOW_ANY_MAP_FIELD_NUMBER: _ClassVar[int]
    LEGACY_REGION_PINGS_FIELD_NUMBER: _ClassVar[int]
    PING_DATA_FIELD_NUMBER: _ClassVar[int]
    legacy_server_region: int
    custom_game_id: int
    client_version: int
    create_lobby_details: CMsgPracticeLobbySetDetails
    allow_any_map: bool
    legacy_region_pings: _containers.RepeatedCompositeFieldContainer[
        CMsgQuickJoinCustomLobby.LegacyRegionPing
    ]
    ping_data: _base_gcmessages_pb2.CMsgClientPingData
    def __init__(
        self,
        legacy_server_region: int | None = ...,
        custom_game_id: int | None = ...,
        client_version: int | None = ...,
        create_lobby_details: CMsgPracticeLobbySetDetails | _Mapping | None = ...,
        allow_any_map: bool = ...,
        legacy_region_pings: _Iterable[CMsgQuickJoinCustomLobby.LegacyRegionPing | _Mapping]
        | None = ...,
        ping_data: _base_gcmessages_pb2.CMsgClientPingData | _Mapping | None = ...,
    ) -> None: ...

class CMsgQuickJoinCustomLobbyResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: _dota_shared_enums_pb2.DOTAJoinLobbyResult
    def __init__(
        self, result: _dota_shared_enums_pb2.DOTAJoinLobbyResult | str | None = ...
    ) -> None: ...

class CMsgBotGameCreate(_message.Message):
    __slots__ = (
        "search_key",
        "client_version",
        "difficulty_radiant",
        "team",
        "game_mode",
        "difficulty_dire",
    )
    SEARCH_KEY_FIELD_NUMBER: _ClassVar[int]
    CLIENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    DIFFICULTY_RADIANT_FIELD_NUMBER: _ClassVar[int]
    TEAM_FIELD_NUMBER: _ClassVar[int]
    GAME_MODE_FIELD_NUMBER: _ClassVar[int]
    DIFFICULTY_DIRE_FIELD_NUMBER: _ClassVar[int]
    search_key: str
    client_version: int
    difficulty_radiant: _dota_shared_enums_pb2.DOTABotDifficulty
    team: _dota_shared_enums_pb2.DOTA_GC_TEAM
    game_mode: int
    difficulty_dire: _dota_shared_enums_pb2.DOTABotDifficulty
    def __init__(
        self,
        search_key: str | None = ...,
        client_version: int | None = ...,
        difficulty_radiant: _dota_shared_enums_pb2.DOTABotDifficulty | str | None = ...,
        team: _dota_shared_enums_pb2.DOTA_GC_TEAM | str | None = ...,
        game_mode: int | None = ...,
        difficulty_dire: _dota_shared_enums_pb2.DOTABotDifficulty | str | None = ...,
    ) -> None: ...

class CMsgDOTAPartyMemberSetCoach(_message.Message):
    __slots__ = ("wants_coach",)
    WANTS_COACH_FIELD_NUMBER: _ClassVar[int]
    wants_coach: bool
    def __init__(self, wants_coach: bool = ...) -> None: ...

class CMsgDOTASetGroupLeader(_message.Message):
    __slots__ = ("new_leader_steamid",)
    NEW_LEADER_STEAMID_FIELD_NUMBER: _ClassVar[int]
    new_leader_steamid: int
    def __init__(self, new_leader_steamid: int | None = ...) -> None: ...

class CMsgDOTACancelGroupInvites(_message.Message):
    __slots__ = ("invited_steamids", "invited_groupids")
    INVITED_STEAMIDS_FIELD_NUMBER: _ClassVar[int]
    INVITED_GROUPIDS_FIELD_NUMBER: _ClassVar[int]
    invited_steamids: _containers.RepeatedScalarFieldContainer[int]
    invited_groupids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        invited_steamids: _Iterable[int] | None = ...,
        invited_groupids: _Iterable[int] | None = ...,
    ) -> None: ...

class CMsgDOTASetGroupOpenStatus(_message.Message):
    __slots__ = ("open",)
    OPEN_FIELD_NUMBER: _ClassVar[int]
    open: bool
    def __init__(self, open: bool = ...) -> None: ...

class CMsgDOTAGroupMergeInvite(_message.Message):
    __slots__ = ("other_group_id",)
    OTHER_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    other_group_id: int
    def __init__(self, other_group_id: int | None = ...) -> None: ...

class CMsgDOTAGroupMergeResponse(_message.Message):
    __slots__ = ("initiator_group_id", "accept")
    INITIATOR_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    ACCEPT_FIELD_NUMBER: _ClassVar[int]
    initiator_group_id: int
    accept: bool
    def __init__(self, initiator_group_id: int | None = ..., accept: bool = ...) -> None: ...

class CMsgDOTAGroupMergeReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: _dota_client_enums_pb2.EDOTAGroupMergeResult
    def __init__(
        self, result: _dota_client_enums_pb2.EDOTAGroupMergeResult | str | None = ...
    ) -> None: ...

class CMsgSpectatorLobbyGameDetails(_message.Message):
    __slots__ = (
        "language",
        "match_id",
        "server_steam_id",
        "stream_url",
        "stream_name",
        "league_id",
        "series_type",
        "series_game",
        "radiant_team",
        "dire_team",
    )
    class Team(_message.Message):
        __slots__ = ("team_id", "team_name", "team_logo")
        TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
        TEAM_LOGO_FIELD_NUMBER: _ClassVar[int]
        team_id: int
        team_name: str
        team_logo: int
        def __init__(
            self,
            team_id: int | None = ...,
            team_name: str | None = ...,
            team_logo: int | None = ...,
        ) -> None: ...

    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    SERVER_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    STREAM_URL_FIELD_NUMBER: _ClassVar[int]
    STREAM_NAME_FIELD_NUMBER: _ClassVar[int]
    LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    SERIES_TYPE_FIELD_NUMBER: _ClassVar[int]
    SERIES_GAME_FIELD_NUMBER: _ClassVar[int]
    RADIANT_TEAM_FIELD_NUMBER: _ClassVar[int]
    DIRE_TEAM_FIELD_NUMBER: _ClassVar[int]
    language: int
    match_id: int
    server_steam_id: int
    stream_url: str
    stream_name: str
    league_id: int
    series_type: int
    series_game: int
    radiant_team: CMsgSpectatorLobbyGameDetails.Team
    dire_team: CMsgSpectatorLobbyGameDetails.Team
    def __init__(
        self,
        language: int | None = ...,
        match_id: int | None = ...,
        server_steam_id: int | None = ...,
        stream_url: str | None = ...,
        stream_name: str | None = ...,
        league_id: int | None = ...,
        series_type: int | None = ...,
        series_game: int | None = ...,
        radiant_team: CMsgSpectatorLobbyGameDetails.Team | _Mapping | None = ...,
        dire_team: CMsgSpectatorLobbyGameDetails.Team | _Mapping | None = ...,
    ) -> None: ...

class CMsgSetSpectatorLobbyDetails(_message.Message):
    __slots__ = ("lobby_id", "lobby_name", "pass_key", "game_details")
    LOBBY_ID_FIELD_NUMBER: _ClassVar[int]
    LOBBY_NAME_FIELD_NUMBER: _ClassVar[int]
    PASS_KEY_FIELD_NUMBER: _ClassVar[int]
    GAME_DETAILS_FIELD_NUMBER: _ClassVar[int]
    lobby_id: int
    lobby_name: str
    pass_key: str
    game_details: CMsgSpectatorLobbyGameDetails
    def __init__(
        self,
        lobby_id: int | None = ...,
        lobby_name: str | None = ...,
        pass_key: str | None = ...,
        game_details: CMsgSpectatorLobbyGameDetails | _Mapping | None = ...,
    ) -> None: ...

class CMsgCreateSpectatorLobby(_message.Message):
    __slots__ = ("client_version", "details")
    CLIENT_VERSION_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    client_version: int
    details: CMsgSetSpectatorLobbyDetails
    def __init__(
        self,
        client_version: int | None = ...,
        details: CMsgSetSpectatorLobbyDetails | _Mapping | None = ...,
    ) -> None: ...

class CMsgSpectatorLobbyList(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgSpectatorLobbyListResponse(_message.Message):
    __slots__ = ("lobbies",)
    class SpectatorLobby(_message.Message):
        __slots__ = (
            "lobby_id",
            "game_name",
            "requires_pass_key",
            "leader_account_id",
            "member_count",
            "game_details",
        )
        LOBBY_ID_FIELD_NUMBER: _ClassVar[int]
        GAME_NAME_FIELD_NUMBER: _ClassVar[int]
        REQUIRES_PASS_KEY_FIELD_NUMBER: _ClassVar[int]
        LEADER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        MEMBER_COUNT_FIELD_NUMBER: _ClassVar[int]
        GAME_DETAILS_FIELD_NUMBER: _ClassVar[int]
        lobby_id: int
        game_name: str
        requires_pass_key: bool
        leader_account_id: int
        member_count: int
        game_details: CMsgSpectatorLobbyGameDetails
        def __init__(
            self,
            lobby_id: int | None = ...,
            game_name: str | None = ...,
            requires_pass_key: bool = ...,
            leader_account_id: int | None = ...,
            member_count: int | None = ...,
            game_details: CMsgSpectatorLobbyGameDetails | _Mapping | None = ...,
        ) -> None: ...

    LOBBIES_FIELD_NUMBER: _ClassVar[int]
    lobbies: _containers.RepeatedCompositeFieldContainer[
        CMsgSpectatorLobbyListResponse.SpectatorLobby
    ]
    def __init__(
        self,
        lobbies: _Iterable[CMsgSpectatorLobbyListResponse.SpectatorLobby | _Mapping] | None = ...,
    ) -> None: ...

class CMsgClientToGCRequestSteamDatagramTicket(_message.Message):
    __slots__ = ("server_steam_id",)
    SERVER_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    server_steam_id: int
    def __init__(self, server_steam_id: int | None = ...) -> None: ...

class CMsgClientToGCRequestSteamDatagramTicketResponse(_message.Message):
    __slots__ = ("serialized_ticket", "message")
    SERIALIZED_TICKET_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    serialized_ticket: bytes
    message: str
    def __init__(
        self, serialized_ticket: bytes | None = ..., message: str | None = ...
    ) -> None: ...

class CMsgGCToClientSteamDatagramTicket(_message.Message):
    __slots__ = (
        "legacy_time_expiry",
        "legacy_authorized_steam_id",
        "legacy_authorized_public_ip",
        "legacy_gameserver_steam_id",
        "legacy_gameserver_net_id",
        "legacy_signature",
        "legacy_app_id",
        "legacy_extra_fields",
        "serialized_ticket",
    )
    LEGACY_TIME_EXPIRY_FIELD_NUMBER: _ClassVar[int]
    LEGACY_AUTHORIZED_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    LEGACY_AUTHORIZED_PUBLIC_IP_FIELD_NUMBER: _ClassVar[int]
    LEGACY_GAMESERVER_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    LEGACY_GAMESERVER_NET_ID_FIELD_NUMBER: _ClassVar[int]
    LEGACY_SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    LEGACY_APP_ID_FIELD_NUMBER: _ClassVar[int]
    LEGACY_EXTRA_FIELDS_FIELD_NUMBER: _ClassVar[int]
    SERIALIZED_TICKET_FIELD_NUMBER: _ClassVar[int]
    legacy_time_expiry: int
    legacy_authorized_steam_id: int
    legacy_authorized_public_ip: int
    legacy_gameserver_steam_id: int
    legacy_gameserver_net_id: int
    legacy_signature: bytes
    legacy_app_id: int
    legacy_extra_fields: _containers.RepeatedScalarFieldContainer[bytes]
    serialized_ticket: bytes
    def __init__(
        self,
        legacy_time_expiry: int | None = ...,
        legacy_authorized_steam_id: int | None = ...,
        legacy_authorized_public_ip: int | None = ...,
        legacy_gameserver_steam_id: int | None = ...,
        legacy_gameserver_net_id: int | None = ...,
        legacy_signature: bytes | None = ...,
        legacy_app_id: int | None = ...,
        legacy_extra_fields: _Iterable[bytes] | None = ...,
        serialized_ticket: bytes | None = ...,
    ) -> None: ...

class CMsgGCToClientRequestLaneSelection(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgGCToClientRequestLaneSelectionResponse(_message.Message):
    __slots__ = ("lane_selection_flags", "high_priority_disabled")
    LANE_SELECTION_FLAGS_FIELD_NUMBER: _ClassVar[int]
    HIGH_PRIORITY_DISABLED_FIELD_NUMBER: _ClassVar[int]
    lane_selection_flags: int
    high_priority_disabled: bool
    def __init__(
        self, lane_selection_flags: int | None = ..., high_priority_disabled: bool = ...
    ) -> None: ...

class CMsgGCToClientRequestMMInfo(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCMMInfo(_message.Message):
    __slots__ = ("lane_selection_flags", "high_priority_disabled")
    LANE_SELECTION_FLAGS_FIELD_NUMBER: _ClassVar[int]
    HIGH_PRIORITY_DISABLED_FIELD_NUMBER: _ClassVar[int]
    lane_selection_flags: int
    high_priority_disabled: bool
    def __init__(
        self, lane_selection_flags: int | None = ..., high_priority_disabled: bool = ...
    ) -> None: ...
