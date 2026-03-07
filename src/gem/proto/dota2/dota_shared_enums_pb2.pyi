from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class DOTA_GameMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOTA_GAMEMODE_NONE: _ClassVar[DOTA_GameMode]
    DOTA_GAMEMODE_AP: _ClassVar[DOTA_GameMode]
    DOTA_GAMEMODE_CM: _ClassVar[DOTA_GameMode]
    DOTA_GAMEMODE_RD: _ClassVar[DOTA_GameMode]
    DOTA_GAMEMODE_SD: _ClassVar[DOTA_GameMode]
    DOTA_GAMEMODE_AR: _ClassVar[DOTA_GameMode]
    DOTA_GAMEMODE_INTRO: _ClassVar[DOTA_GameMode]
    DOTA_GAMEMODE_HW: _ClassVar[DOTA_GameMode]
    DOTA_GAMEMODE_REVERSE_CM: _ClassVar[DOTA_GameMode]
    DOTA_GAMEMODE_XMAS: _ClassVar[DOTA_GameMode]
    DOTA_GAMEMODE_TUTORIAL: _ClassVar[DOTA_GameMode]
    DOTA_GAMEMODE_MO: _ClassVar[DOTA_GameMode]
    DOTA_GAMEMODE_LP: _ClassVar[DOTA_GameMode]
    DOTA_GAMEMODE_POOL1: _ClassVar[DOTA_GameMode]
    DOTA_GAMEMODE_FH: _ClassVar[DOTA_GameMode]
    DOTA_GAMEMODE_CUSTOM: _ClassVar[DOTA_GameMode]
    DOTA_GAMEMODE_CD: _ClassVar[DOTA_GameMode]
    DOTA_GAMEMODE_BD: _ClassVar[DOTA_GameMode]
    DOTA_GAMEMODE_ABILITY_DRAFT: _ClassVar[DOTA_GameMode]
    DOTA_GAMEMODE_EVENT: _ClassVar[DOTA_GameMode]
    DOTA_GAMEMODE_ARDM: _ClassVar[DOTA_GameMode]
    DOTA_GAMEMODE_1V1MID: _ClassVar[DOTA_GameMode]
    DOTA_GAMEMODE_ALL_DRAFT: _ClassVar[DOTA_GameMode]
    DOTA_GAMEMODE_TURBO: _ClassVar[DOTA_GameMode]
    DOTA_GAMEMODE_MUTATION: _ClassVar[DOTA_GameMode]
    DOTA_GAMEMODE_COACHES_CHALLENGE: _ClassVar[DOTA_GameMode]
    DOTA_GAMEMODE_BOT_CHALLENGE: _ClassVar[DOTA_GameMode]

class DOTA_GameState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOTA_GAMERULES_STATE_INIT: _ClassVar[DOTA_GameState]
    DOTA_GAMERULES_STATE_WAIT_FOR_PLAYERS_TO_LOAD: _ClassVar[DOTA_GameState]
    DOTA_GAMERULES_STATE_HERO_SELECTION: _ClassVar[DOTA_GameState]
    DOTA_GAMERULES_STATE_STRATEGY_TIME: _ClassVar[DOTA_GameState]
    DOTA_GAMERULES_STATE_PRE_GAME: _ClassVar[DOTA_GameState]
    DOTA_GAMERULES_STATE_GAME_IN_PROGRESS: _ClassVar[DOTA_GameState]
    DOTA_GAMERULES_STATE_POST_GAME: _ClassVar[DOTA_GameState]
    DOTA_GAMERULES_STATE_DISCONNECT: _ClassVar[DOTA_GameState]
    DOTA_GAMERULES_STATE_TEAM_SHOWCASE: _ClassVar[DOTA_GameState]
    DOTA_GAMERULES_STATE_CUSTOM_GAME_SETUP: _ClassVar[DOTA_GameState]
    DOTA_GAMERULES_STATE_WAIT_FOR_MAP_TO_LOAD: _ClassVar[DOTA_GameState]
    DOTA_GAMERULES_STATE_SCENARIO_SETUP: _ClassVar[DOTA_GameState]
    DOTA_GAMERULES_STATE_PLAYER_DRAFT: _ClassVar[DOTA_GameState]
    DOTA_GAMERULES_STATE_LAST: _ClassVar[DOTA_GameState]

class DOTA_GC_TEAM(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOTA_GC_TEAM_GOOD_GUYS: _ClassVar[DOTA_GC_TEAM]
    DOTA_GC_TEAM_BAD_GUYS: _ClassVar[DOTA_GC_TEAM]
    DOTA_GC_TEAM_BROADCASTER: _ClassVar[DOTA_GC_TEAM]
    DOTA_GC_TEAM_SPECTATOR: _ClassVar[DOTA_GC_TEAM]
    DOTA_GC_TEAM_PLAYER_POOL: _ClassVar[DOTA_GC_TEAM]
    DOTA_GC_TEAM_NOTEAM: _ClassVar[DOTA_GC_TEAM]
    DOTA_GC_TEAM_CUSTOM_1: _ClassVar[DOTA_GC_TEAM]
    DOTA_GC_TEAM_CUSTOM_2: _ClassVar[DOTA_GC_TEAM]
    DOTA_GC_TEAM_CUSTOM_3: _ClassVar[DOTA_GC_TEAM]
    DOTA_GC_TEAM_CUSTOM_4: _ClassVar[DOTA_GC_TEAM]
    DOTA_GC_TEAM_CUSTOM_5: _ClassVar[DOTA_GC_TEAM]
    DOTA_GC_TEAM_CUSTOM_6: _ClassVar[DOTA_GC_TEAM]
    DOTA_GC_TEAM_CUSTOM_7: _ClassVar[DOTA_GC_TEAM]
    DOTA_GC_TEAM_CUSTOM_8: _ClassVar[DOTA_GC_TEAM]
    DOTA_GC_TEAM_NEUTRALS: _ClassVar[DOTA_GC_TEAM]

class EEvent(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EVENT_ID_NONE: _ClassVar[EEvent]
    EVENT_ID_DIRETIDE: _ClassVar[EEvent]
    EVENT_ID_SPRING_FESTIVAL: _ClassVar[EEvent]
    EVENT_ID_FROSTIVUS_2013: _ClassVar[EEvent]
    EVENT_ID_COMPENDIUM_2014: _ClassVar[EEvent]
    EVENT_ID_NEXON_PC_BANG: _ClassVar[EEvent]
    EVENT_ID_PWRD_DAC_2015: _ClassVar[EEvent]
    EVENT_ID_NEW_BLOOM_2015: _ClassVar[EEvent]
    EVENT_ID_INTERNATIONAL_2015: _ClassVar[EEvent]
    EVENT_ID_FALL_MAJOR_2015: _ClassVar[EEvent]
    EVENT_ID_ORACLE_PA: _ClassVar[EEvent]
    EVENT_ID_NEW_BLOOM_2015_PREBEAST: _ClassVar[EEvent]
    EVENT_ID_FROSTIVUS: _ClassVar[EEvent]
    EVENT_ID_WINTER_MAJOR_2016: _ClassVar[EEvent]
    EVENT_ID_INTERNATIONAL_2016: _ClassVar[EEvent]
    EVENT_ID_FALL_MAJOR_2016: _ClassVar[EEvent]
    EVENT_ID_WINTER_MAJOR_2017: _ClassVar[EEvent]
    EVENT_ID_NEW_BLOOM_2017: _ClassVar[EEvent]
    EVENT_ID_INTERNATIONAL_2017: _ClassVar[EEvent]
    EVENT_ID_PLUS_SUBSCRIPTION: _ClassVar[EEvent]
    EVENT_ID_SINGLES_DAY_2017: _ClassVar[EEvent]
    EVENT_ID_FROSTIVUS_2017: _ClassVar[EEvent]
    EVENT_ID_INTERNATIONAL_2018: _ClassVar[EEvent]
    EVENT_ID_FROSTIVUS_2018: _ClassVar[EEvent]
    EVENT_ID_NEW_BLOOM_2019: _ClassVar[EEvent]
    EVENT_ID_INTERNATIONAL_2019: _ClassVar[EEvent]
    EVENT_ID_NEW_PLAYER_EXPERIENCE: _ClassVar[EEvent]
    EVENT_ID_FROSTIVUS_2019: _ClassVar[EEvent]
    EVENT_ID_NEW_BLOOM_2020: _ClassVar[EEvent]
    EVENT_ID_INTERNATIONAL_2020: _ClassVar[EEvent]
    EVENT_ID_TEAM_FANDOM: _ClassVar[EEvent]
    EVENT_ID_DIRETIDE_2020: _ClassVar[EEvent]
    EVENT_ID_SPRING_2021: _ClassVar[EEvent]
    EVENT_ID_FALL_2021: _ClassVar[EEvent]
    EVENT_ID_TEAM_FANDOM_FALL_2021: _ClassVar[EEvent]
    EVENT_ID_TEAM_2021_2022_TOUR2: _ClassVar[EEvent]
    EVENT_ID_INTERNATIONAL_2022: _ClassVar[EEvent]
    EVENT_ID_TEAM_2021_2022_TOUR3: _ClassVar[EEvent]
    EVENT_ID_TEAM_INTERNATIONAL_2022: _ClassVar[EEvent]
    EVENT_ID_PERMANENT_GRANTS: _ClassVar[EEvent]
    EVENT_ID_MUERTA_RELEASE_SPRING2023: _ClassVar[EEvent]
    EVENT_ID_TEAM_2023_TOUR1: _ClassVar[EEvent]
    EVENT_ID_TEAM_2023_TOUR2: _ClassVar[EEvent]
    EVENT_ID_TEAM_2023_TOUR3: _ClassVar[EEvent]
    EVENT_ID_INTERNATIONAL_2023: _ClassVar[EEvent]
    EVENT_ID_10TH_ANNIVERSARY: _ClassVar[EEvent]
    EVENT_ID_CROWNFALL: _ClassVar[EEvent]
    EVENT_ID_FROSTIVUS_2023: _ClassVar[EEvent]
    EVENT_ID_INTERNATIONAL_2024: _ClassVar[EEvent]
    EVENT_ID_FROSTIVUS_2024: _ClassVar[EEvent]
    EVENT_ID_MONSTER_HUNTER: _ClassVar[EEvent]
    EVENT_ID_INTERNATIONAL_2025: _ClassVar[EEvent]
    EVENT_ID_FALL_2025: _ClassVar[EEvent]
    EVENT_ID_WINTER_2025: _ClassVar[EEvent]
    EVENT_ID_SPRING_2026: _ClassVar[EEvent]
    EVENT_ID_SUMMER_2026: _ClassVar[EEvent]
    EVENT_ID_FALL_2026: _ClassVar[EEvent]
    EVENT_ID_WINTER_2026: _ClassVar[EEvent]

class ERankType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_ERankType_Invalid: _ClassVar[ERankType]
    k_ERankType_Casual: _ClassVar[ERankType]
    k_ERankType_Ranked: _ClassVar[ERankType]
    k_ERankType_CasualLegacy: _ClassVar[ERankType]
    k_ERankType_RankedLegacy: _ClassVar[ERankType]
    k_ERankType_CasualGlicko: _ClassVar[ERankType]
    k_ERankType_RankedGlicko: _ClassVar[ERankType]
    k_ERankType_RankMax: _ClassVar[ERankType]
    k_ERankType_BehaviorPrivate: _ClassVar[ERankType]
    k_ERankType_BehaviorPublic: _ClassVar[ERankType]
    k_ERankType_Max: _ClassVar[ERankType]

class DOTALeaverStatus_t(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOTA_LEAVER_NONE: _ClassVar[DOTALeaverStatus_t]
    DOTA_LEAVER_DISCONNECTED: _ClassVar[DOTALeaverStatus_t]
    DOTA_LEAVER_DISCONNECTED_TOO_LONG: _ClassVar[DOTALeaverStatus_t]
    DOTA_LEAVER_ABANDONED: _ClassVar[DOTALeaverStatus_t]
    DOTA_LEAVER_AFK: _ClassVar[DOTALeaverStatus_t]
    DOTA_LEAVER_NEVER_CONNECTED: _ClassVar[DOTALeaverStatus_t]
    DOTA_LEAVER_NEVER_CONNECTED_TOO_LONG: _ClassVar[DOTALeaverStatus_t]
    DOTA_LEAVER_FAILED_TO_READY_UP: _ClassVar[DOTALeaverStatus_t]
    DOTA_LEAVER_DECLINED: _ClassVar[DOTALeaverStatus_t]
    DOTA_LEAVER_DECLINED_REQUEUE: _ClassVar[DOTALeaverStatus_t]

class DOTAConnectionState_t(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOTA_CONNECTION_STATE_UNKNOWN: _ClassVar[DOTAConnectionState_t]
    DOTA_CONNECTION_STATE_NOT_YET_CONNECTED: _ClassVar[DOTAConnectionState_t]
    DOTA_CONNECTION_STATE_CONNECTED: _ClassVar[DOTAConnectionState_t]
    DOTA_CONNECTION_STATE_DISCONNECTED: _ClassVar[DOTAConnectionState_t]
    DOTA_CONNECTION_STATE_ABANDONED: _ClassVar[DOTAConnectionState_t]
    DOTA_CONNECTION_STATE_LOADING: _ClassVar[DOTAConnectionState_t]
    DOTA_CONNECTION_STATE_FAILED: _ClassVar[DOTAConnectionState_t]

class Fantasy_Roles(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FANTASY_ROLE_UNDEFINED: _ClassVar[Fantasy_Roles]
    FANTASY_ROLE_CORE: _ClassVar[Fantasy_Roles]
    FANTASY_ROLE_SUPPORT: _ClassVar[Fantasy_Roles]
    FANTASY_ROLE_OFFLANE: _ClassVar[Fantasy_Roles]
    FANTASY_ROLE_MID: _ClassVar[Fantasy_Roles]

class Fantasy_Scoring(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FANTASY_SCORING_KILLS: _ClassVar[Fantasy_Scoring]
    FANTASY_SCORING_DEATHS: _ClassVar[Fantasy_Scoring]
    FANTASY_SCORING_CS: _ClassVar[Fantasy_Scoring]
    FANTASY_SCORING_GPM: _ClassVar[Fantasy_Scoring]
    FANTASY_SCORING_TOWER_KILLS: _ClassVar[Fantasy_Scoring]
    FANTASY_SCORING_ROSHAN_KILLS: _ClassVar[Fantasy_Scoring]
    FANTASY_SCORING_TEAMFIGHT_PARTICIPATION: _ClassVar[Fantasy_Scoring]
    FANTASY_SCORING_WARDS_PLANTED: _ClassVar[Fantasy_Scoring]
    FANTASY_SCORING_CAMPS_STACKED: _ClassVar[Fantasy_Scoring]
    FANTASY_SCORING_RUNES_GRABBED: _ClassVar[Fantasy_Scoring]
    FANTASY_SCORING_FIRST_BLOOD: _ClassVar[Fantasy_Scoring]
    FANTASY_SCORING_STUNS: _ClassVar[Fantasy_Scoring]
    FANTASY_SCORING_SMOKES_USED: _ClassVar[Fantasy_Scoring]
    FANTASY_SCORING_MADSTONE: _ClassVar[Fantasy_Scoring]
    FANTASY_SCORING_WATCHERS_TAKEN: _ClassVar[Fantasy_Scoring]
    FANTASY_SCORING_LOTUSES_GAINED: _ClassVar[Fantasy_Scoring]
    FANTASY_SCORING_TORMENTOR_KILLS: _ClassVar[Fantasy_Scoring]
    FANTASY_SCORING_COURIER_KILLS: _ClassVar[Fantasy_Scoring]
    FANTASY_SCORING_TYPES: _ClassVar[Fantasy_Scoring]
    FANTASY_SCORING_INVALID: _ClassVar[Fantasy_Scoring]

class Fantasy_Team_Slots(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FANTASY_SLOT_NONE: _ClassVar[Fantasy_Team_Slots]
    FANTASY_SLOT_CORE: _ClassVar[Fantasy_Team_Slots]
    FANTASY_SLOT_SUPPORT: _ClassVar[Fantasy_Team_Slots]
    FANTASY_SLOT_ANY: _ClassVar[Fantasy_Team_Slots]
    FANTASY_SLOT_BENCH: _ClassVar[Fantasy_Team_Slots]

class Fantasy_Selection_Mode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FANTASY_SELECTION_INVALID: _ClassVar[Fantasy_Selection_Mode]
    FANTASY_SELECTION_LOCKED: _ClassVar[Fantasy_Selection_Mode]
    FANTASY_SELECTION_SHUFFLE: _ClassVar[Fantasy_Selection_Mode]
    FANTASY_SELECTION_FREE_PICK: _ClassVar[Fantasy_Selection_Mode]
    FANTASY_SELECTION_ENDED: _ClassVar[Fantasy_Selection_Mode]
    FANTASY_SELECTION_PRE_SEASON: _ClassVar[Fantasy_Selection_Mode]
    FANTASY_SELECTION_PRE_DRAFT: _ClassVar[Fantasy_Selection_Mode]
    FANTASY_SELECTION_DRAFTING: _ClassVar[Fantasy_Selection_Mode]
    FANTASY_SELECTION_REGULAR_SEASON: _ClassVar[Fantasy_Selection_Mode]
    FANTASY_SELECTION_CARD_BASED: _ClassVar[Fantasy_Selection_Mode]

class Fantasy_Gem_Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FANTASY_GEM_TYPE_RUBY: _ClassVar[Fantasy_Gem_Type]
    FANTASY_GEM_TYPE_SAPPHIRE: _ClassVar[Fantasy_Gem_Type]
    FANTASY_GEM_TYPE_EMERALD: _ClassVar[Fantasy_Gem_Type]

class DOTAChatChannelType_t(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOTAChannelType_Regional: _ClassVar[DOTAChatChannelType_t]
    DOTAChannelType_Custom: _ClassVar[DOTAChatChannelType_t]
    DOTAChannelType_Party: _ClassVar[DOTAChatChannelType_t]
    DOTAChannelType_Lobby: _ClassVar[DOTAChatChannelType_t]
    DOTAChannelType_Team: _ClassVar[DOTAChatChannelType_t]
    DOTAChannelType_Guild: _ClassVar[DOTAChatChannelType_t]
    DOTAChannelType_Fantasy: _ClassVar[DOTAChatChannelType_t]
    DOTAChannelType_Whisper: _ClassVar[DOTAChatChannelType_t]
    DOTAChannelType_Console: _ClassVar[DOTAChatChannelType_t]
    DOTAChannelType_Tab: _ClassVar[DOTAChatChannelType_t]
    DOTAChannelType_Invalid: _ClassVar[DOTAChatChannelType_t]
    DOTAChannelType_GameAll: _ClassVar[DOTAChatChannelType_t]
    DOTAChannelType_GameAllies: _ClassVar[DOTAChatChannelType_t]
    DOTAChannelType_GameSpectator: _ClassVar[DOTAChatChannelType_t]
    DOTAChannelType_GameCoaching: _ClassVar[DOTAChatChannelType_t]
    DOTAChannelType_Cafe: _ClassVar[DOTAChatChannelType_t]
    DOTAChannelType_CustomGame: _ClassVar[DOTAChatChannelType_t]
    DOTAChannelType_Private: _ClassVar[DOTAChatChannelType_t]
    DOTAChannelType_PostGame: _ClassVar[DOTAChatChannelType_t]
    DOTAChannelType_BattleCup: _ClassVar[DOTAChatChannelType_t]
    DOTAChannelType_HLTVSpectator: _ClassVar[DOTAChatChannelType_t]
    DOTAChannelType_GameEvents: _ClassVar[DOTAChatChannelType_t]
    DOTAChannelType_Trivia: _ClassVar[DOTAChatChannelType_t]
    DOTAChannelType_NewPlayer: _ClassVar[DOTAChatChannelType_t]
    DOTAChannelType_PrivateCoaching: _ClassVar[DOTAChatChannelType_t]

class EChatSpecialPrivileges(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EChatSpecialPrivileges_None: _ClassVar[EChatSpecialPrivileges]
    k_EChatSpecialPrivileges_Moderator: _ClassVar[EChatSpecialPrivileges]
    k_EChatSpecialPrivileges_SuperModerator: _ClassVar[EChatSpecialPrivileges]

class DOTACommType_t(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOTA_COMM_TYPE_NONE: _ClassVar[DOTACommType_t]
    DOTA_COMM_TYPE_PING: _ClassVar[DOTACommType_t]
    DOTA_COMM_TYPE_CHATWHEEL: _ClassVar[DOTACommType_t]
    DOTA_COMM_TYPE_TIP: _ClassVar[DOTACommType_t]
    DOTA_COMM_TYPE_TEXT: _ClassVar[DOTACommType_t]
    DOTA_COMM_TYPE_SHOWCASE: _ClassVar[DOTACommType_t]
    DOTA_COMM_TYPE_VOICE: _ClassVar[DOTACommType_t]
    DOTA_COMM_TYPE_ALLY_ABILITY: _ClassVar[DOTACommType_t]
    DOTA_COMM_TYPE_PAUSE: _ClassVar[DOTACommType_t]
    DOTA_COMM_TYPE_COACHING: _ClassVar[DOTACommType_t]
    DOTA_COMM_TYPE_NOCOOLDOWN: _ClassVar[DOTACommType_t]
    DOTA_COMM_TYPE_RANKEDMATCHMAKE: _ClassVar[DOTACommType_t]
    DOTA_COMM_TYPE_DROPS: _ClassVar[DOTACommType_t]
    DOTA_COMM_TYPE_NEWPLAYER_EXPERT: _ClassVar[DOTACommType_t]
    DOTA_COMM_TYPE_COACHED: _ClassVar[DOTACommType_t]
    DOTA_COMM_TYPE_MAPDRAWING: _ClassVar[DOTACommType_t]

class DOTACommLevel_t(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOTA_COMM_LEVEL_NONE: _ClassVar[DOTACommLevel_t]
    DOTA_COMM_LEVEL_COOLDOWN: _ClassVar[DOTACommLevel_t]
    DOTA_COMM_LEVEL_PINGS: _ClassVar[DOTACommLevel_t]
    DOTA_COMM_LEVEL_MAPDRAWING: _ClassVar[DOTACommLevel_t]
    DOTA_COMM_LEVEL_CHAT: _ClassVar[DOTACommLevel_t]
    DOTA_COMM_LEVEL_TIPPING: _ClassVar[DOTACommLevel_t]
    DOTA_COMM_LEVEL_VOICE: _ClassVar[DOTACommLevel_t]
    DOTA_COMM_LEVEL_ALLIED_ABILITY: _ClassVar[DOTACommLevel_t]

class DOTABehaviorLevel_t(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOTA_BEHAVIOR_LEVEL_NONE: _ClassVar[DOTABehaviorLevel_t]
    DOTA_BEHAVIOR_LEVEL_RANKED_ALLOWED: _ClassVar[DOTABehaviorLevel_t]
    DOTA_BEHAVIOR_LEVEL_PAUSING: _ClassVar[DOTABehaviorLevel_t]
    DOTA_BEHAVIOR_LEVEL_DROPS: _ClassVar[DOTABehaviorLevel_t]
    DOTA_BEHAVIOR_LEVEL_COACHING: _ClassVar[DOTABehaviorLevel_t]

class EProfileCardSlotType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EProfileCardSlotType_Empty: _ClassVar[EProfileCardSlotType]
    k_EProfileCardSlotType_Stat: _ClassVar[EProfileCardSlotType]
    k_EProfileCardSlotType_Trophy: _ClassVar[EProfileCardSlotType]
    k_EProfileCardSlotType_Item: _ClassVar[EProfileCardSlotType]
    k_EProfileCardSlotType_Hero: _ClassVar[EProfileCardSlotType]
    k_EProfileCardSlotType_Emoticon: _ClassVar[EProfileCardSlotType]
    k_EProfileCardSlotType_Team: _ClassVar[EProfileCardSlotType]

class EMatchGroupServerStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EMatchGroupServerStatus_OK: _ClassVar[EMatchGroupServerStatus]
    k_EMatchGroupServerStatus_LimitedAvailability: _ClassVar[EMatchGroupServerStatus]
    k_EMatchGroupServerStatus_Offline: _ClassVar[EMatchGroupServerStatus]

class DOTA_CM_PICK(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOTA_CM_RANDOM: _ClassVar[DOTA_CM_PICK]
    DOTA_CM_GOOD_GUYS: _ClassVar[DOTA_CM_PICK]
    DOTA_CM_BAD_GUYS: _ClassVar[DOTA_CM_PICK]

class DOTALowPriorityBanType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOTA_LOW_PRIORITY_BAN_ABANDON: _ClassVar[DOTALowPriorityBanType]
    DOTA_LOW_PRIORITY_BAN_REPORTS: _ClassVar[DOTALowPriorityBanType]
    DOTA_LOW_PRIORITY_BAN_SECONDARY_ABANDON: _ClassVar[DOTALowPriorityBanType]
    DOTA_LOW_PRIORITY_BAN_PRE_GAME_ROLE: _ClassVar[DOTALowPriorityBanType]

class DOTALobbyReadyState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOTALobbyReadyState_UNDECLARED: _ClassVar[DOTALobbyReadyState]
    DOTALobbyReadyState_ACCEPTED: _ClassVar[DOTALobbyReadyState]
    DOTALobbyReadyState_DECLINED: _ClassVar[DOTALobbyReadyState]
    DOTALobbyReadyState_DECLINED_REQUEUE: _ClassVar[DOTALobbyReadyState]

class DOTAJoinLobbyResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOTA_JOIN_RESULT_SUCCESS: _ClassVar[DOTAJoinLobbyResult]
    DOTA_JOIN_RESULT_ALREADY_IN_GAME: _ClassVar[DOTAJoinLobbyResult]
    DOTA_JOIN_RESULT_INVALID_LOBBY: _ClassVar[DOTAJoinLobbyResult]
    DOTA_JOIN_RESULT_INCORRECT_PASSWORD: _ClassVar[DOTAJoinLobbyResult]
    DOTA_JOIN_RESULT_ACCESS_DENIED: _ClassVar[DOTAJoinLobbyResult]
    DOTA_JOIN_RESULT_GENERIC_ERROR: _ClassVar[DOTAJoinLobbyResult]
    DOTA_JOIN_RESULT_INCORRECT_VERSION: _ClassVar[DOTAJoinLobbyResult]
    DOTA_JOIN_RESULT_IN_TEAM_PARTY: _ClassVar[DOTAJoinLobbyResult]
    DOTA_JOIN_RESULT_NO_LOBBY_FOUND: _ClassVar[DOTAJoinLobbyResult]
    DOTA_JOIN_RESULT_LOBBY_FULL: _ClassVar[DOTAJoinLobbyResult]
    DOTA_JOIN_RESULT_CUSTOM_GAME_INCORRECT_VERSION: _ClassVar[DOTAJoinLobbyResult]
    DOTA_JOIN_RESULT_TIMEOUT: _ClassVar[DOTAJoinLobbyResult]
    DOTA_JOIN_RESULT_CUSTOM_GAME_COOLDOWN: _ClassVar[DOTAJoinLobbyResult]
    DOTA_JOIN_RESULT_BUSY: _ClassVar[DOTAJoinLobbyResult]
    DOTA_JOIN_RESULT_NO_PLAYTIME: _ClassVar[DOTAJoinLobbyResult]

class DOTASelectionPriorityRules(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_DOTASelectionPriorityRules_Manual: _ClassVar[DOTASelectionPriorityRules]
    k_DOTASelectionPriorityRules_Automatic: _ClassVar[DOTASelectionPriorityRules]

class DOTASelectionPriorityChoice(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_DOTASelectionPriorityChoice_Invalid: _ClassVar[DOTASelectionPriorityChoice]
    k_DOTASelectionPriorityChoice_FirstPick: _ClassVar[DOTASelectionPriorityChoice]
    k_DOTASelectionPriorityChoice_SecondPick: _ClassVar[DOTASelectionPriorityChoice]
    k_DOTASelectionPriorityChoice_Radiant: _ClassVar[DOTASelectionPriorityChoice]
    k_DOTASelectionPriorityChoice_Dire: _ClassVar[DOTASelectionPriorityChoice]

class DOTAMatchVote(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOTAMatchVote_INVALID: _ClassVar[DOTAMatchVote]
    DOTAMatchVote_POSITIVE: _ClassVar[DOTAMatchVote]
    DOTAMatchVote_NEGATIVE: _ClassVar[DOTAMatchVote]

class DOTALobbyVisibility(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOTALobbyVisibility_Public: _ClassVar[DOTALobbyVisibility]
    DOTALobbyVisibility_Friends: _ClassVar[DOTALobbyVisibility]
    DOTALobbyVisibility_Unlisted: _ClassVar[DOTALobbyVisibility]

class EDOTAPlayerMMRType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EDOTAPlayerMMRType_Invalid: _ClassVar[EDOTAPlayerMMRType]
    k_EDOTAPlayerMMRType_GeneralHidden: _ClassVar[EDOTAPlayerMMRType]
    k_EDOTAPlayerMMRType_GeneralCompetitive: _ClassVar[EDOTAPlayerMMRType]

class EDOTAMMRBoostType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EDOTAMMRBoostType_None: _ClassVar[EDOTAMMRBoostType]
    k_EDOTAMMRBoostType_Leader: _ClassVar[EDOTAMMRBoostType]
    k_EDOTAMMRBoostType_Follower: _ClassVar[EDOTAMMRBoostType]

class MatchType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MATCH_TYPE_CASUAL: _ClassVar[MatchType]
    MATCH_TYPE_COOP_BOTS: _ClassVar[MatchType]
    MATCH_TYPE_COMPETITIVE: _ClassVar[MatchType]
    MATCH_TYPE_WEEKEND_TOURNEY: _ClassVar[MatchType]
    MATCH_TYPE_EVENT: _ClassVar[MatchType]
    MATCH_TYPE_COACHES_CHALLENGE: _ClassVar[MatchType]
    MATCH_TYPE_NEW_PLAYER_POOL: _ClassVar[MatchType]

class DOTABotDifficulty(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BOT_DIFFICULTY_PASSIVE: _ClassVar[DOTABotDifficulty]
    BOT_DIFFICULTY_EASY: _ClassVar[DOTABotDifficulty]
    BOT_DIFFICULTY_MEDIUM: _ClassVar[DOTABotDifficulty]
    BOT_DIFFICULTY_HARD: _ClassVar[DOTABotDifficulty]
    BOT_DIFFICULTY_UNFAIR: _ClassVar[DOTABotDifficulty]
    BOT_DIFFICULTY_INVALID: _ClassVar[DOTABotDifficulty]
    BOT_DIFFICULTY_EXTRA1: _ClassVar[DOTABotDifficulty]
    BOT_DIFFICULTY_EXTRA2: _ClassVar[DOTABotDifficulty]
    BOT_DIFFICULTY_EXTRA3: _ClassVar[DOTABotDifficulty]
    BOT_DIFFICULTY_NPX: _ClassVar[DOTABotDifficulty]

class DOTA_BOT_MODE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOTA_BOT_MODE_NONE: _ClassVar[DOTA_BOT_MODE]
    DOTA_BOT_MODE_LANING: _ClassVar[DOTA_BOT_MODE]
    DOTA_BOT_MODE_ATTACK: _ClassVar[DOTA_BOT_MODE]
    DOTA_BOT_MODE_ROAM: _ClassVar[DOTA_BOT_MODE]
    DOTA_BOT_MODE_RETREAT: _ClassVar[DOTA_BOT_MODE]
    DOTA_BOT_MODE_SECRET_SHOP: _ClassVar[DOTA_BOT_MODE]
    DOTA_BOT_MODE_SIDE_SHOP: _ClassVar[DOTA_BOT_MODE]
    DOTA_BOT_MODE_RUNE: _ClassVar[DOTA_BOT_MODE]
    DOTA_BOT_MODE_PUSH_TOWER_TOP: _ClassVar[DOTA_BOT_MODE]
    DOTA_BOT_MODE_PUSH_TOWER_MID: _ClassVar[DOTA_BOT_MODE]
    DOTA_BOT_MODE_PUSH_TOWER_BOT: _ClassVar[DOTA_BOT_MODE]
    DOTA_BOT_MODE_DEFEND_TOWER_TOP: _ClassVar[DOTA_BOT_MODE]
    DOTA_BOT_MODE_DEFEND_TOWER_MID: _ClassVar[DOTA_BOT_MODE]
    DOTA_BOT_MODE_DEFEND_TOWER_BOT: _ClassVar[DOTA_BOT_MODE]
    DOTA_BOT_MODE_ASSEMBLE: _ClassVar[DOTA_BOT_MODE]
    DOTA_BOT_MODE_ASSEMBLE_WITH_HUMANS: _ClassVar[DOTA_BOT_MODE]
    DOTA_BOT_MODE_TEAM_ROAM: _ClassVar[DOTA_BOT_MODE]
    DOTA_BOT_MODE_FARM: _ClassVar[DOTA_BOT_MODE]
    DOTA_BOT_MODE_DEFEND_ALLY: _ClassVar[DOTA_BOT_MODE]
    DOTA_BOT_MODE_EVASIVE_MANEUVERS: _ClassVar[DOTA_BOT_MODE]
    DOTA_BOT_MODE_ROSHAN: _ClassVar[DOTA_BOT_MODE]
    DOTA_BOT_MODE_ITEM: _ClassVar[DOTA_BOT_MODE]
    DOTA_BOT_MODE_WARD: _ClassVar[DOTA_BOT_MODE]
    DOTA_BOT_MODE_COMPANION: _ClassVar[DOTA_BOT_MODE]
    DOTA_BOT_MODE_TUTORIAL_BOSS: _ClassVar[DOTA_BOT_MODE]
    DOTA_BOT_MODE_MINION: _ClassVar[DOTA_BOT_MODE]
    DOTA_BOT_MODE_OUTPOST: _ClassVar[DOTA_BOT_MODE]
    DOTA_BOT_MODE_BOT_CHALLENGE_ENDGAME: _ClassVar[DOTA_BOT_MODE]

class MatchLanguages(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MATCH_LANGUAGE_INVALID: _ClassVar[MatchLanguages]
    MATCH_LANGUAGE_ENGLISH: _ClassVar[MatchLanguages]
    MATCH_LANGUAGE_RUSSIAN: _ClassVar[MatchLanguages]
    MATCH_LANGUAGE_CHINESE: _ClassVar[MatchLanguages]
    MATCH_LANGUAGE_KOREAN: _ClassVar[MatchLanguages]
    MATCH_LANGUAGE_SPANISH: _ClassVar[MatchLanguages]
    MATCH_LANGUAGE_PORTUGUESE: _ClassVar[MatchLanguages]
    MATCH_LANGUAGE_ENGLISH2: _ClassVar[MatchLanguages]

class ETourneyQueueDeadlineState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_ETourneyQueueDeadlineState_Normal: _ClassVar[ETourneyQueueDeadlineState]
    k_ETourneyQueueDeadlineState_Missed: _ClassVar[ETourneyQueueDeadlineState]
    k_ETourneyQueueDeadlineState_ExpiredOK: _ClassVar[ETourneyQueueDeadlineState]
    k_ETourneyQueueDeadlineState_SeekingBye: _ClassVar[ETourneyQueueDeadlineState]
    k_ETourneyQueueDeadlineState_EligibleForRefund: _ClassVar[ETourneyQueueDeadlineState]
    k_ETourneyQueueDeadlineState_NA: _ClassVar[ETourneyQueueDeadlineState]
    k_ETourneyQueueDeadlineState_ExpiringSoon: _ClassVar[ETourneyQueueDeadlineState]

class EMatchOutcome(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EMatchOutcome_Unknown: _ClassVar[EMatchOutcome]
    k_EMatchOutcome_RadVictory: _ClassVar[EMatchOutcome]
    k_EMatchOutcome_DireVictory: _ClassVar[EMatchOutcome]
    k_EMatchOutcome_NeutralVictory: _ClassVar[EMatchOutcome]
    k_EMatchOutcome_NoTeamWinner: _ClassVar[EMatchOutcome]
    k_EMatchOutcome_Custom1Victory: _ClassVar[EMatchOutcome]
    k_EMatchOutcome_Custom2Victory: _ClassVar[EMatchOutcome]
    k_EMatchOutcome_Custom3Victory: _ClassVar[EMatchOutcome]
    k_EMatchOutcome_Custom4Victory: _ClassVar[EMatchOutcome]
    k_EMatchOutcome_Custom5Victory: _ClassVar[EMatchOutcome]
    k_EMatchOutcome_Custom6Victory: _ClassVar[EMatchOutcome]
    k_EMatchOutcome_Custom7Victory: _ClassVar[EMatchOutcome]
    k_EMatchOutcome_Custom8Victory: _ClassVar[EMatchOutcome]
    k_EMatchOutcome_NotScored_PoorNetworkConditions: _ClassVar[EMatchOutcome]
    k_EMatchOutcome_NotScored_Leaver: _ClassVar[EMatchOutcome]
    k_EMatchOutcome_NotScored_ServerCrash: _ClassVar[EMatchOutcome]
    k_EMatchOutcome_NotScored_NeverStarted: _ClassVar[EMatchOutcome]
    k_EMatchOutcome_NotScored_Canceled: _ClassVar[EMatchOutcome]
    k_EMatchOutcome_NotScored_Suspicious: _ClassVar[EMatchOutcome]

class ELaneType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LANE_TYPE_UNKNOWN: _ClassVar[ELaneType]
    LANE_TYPE_SAFE: _ClassVar[ELaneType]
    LANE_TYPE_OFF: _ClassVar[ELaneType]
    LANE_TYPE_MID: _ClassVar[ELaneType]
    LANE_TYPE_JUNGLE: _ClassVar[ELaneType]
    LANE_TYPE_ROAM: _ClassVar[ELaneType]

class EBadgeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EBadgeType_Invalid: _ClassVar[EBadgeType]
    k_EBadgeType_TI7_Midweek: _ClassVar[EBadgeType]
    k_EBadgeType_TI7_Finals: _ClassVar[EBadgeType]
    k_EBadgeType_TI7_AllEvent: _ClassVar[EBadgeType]
    k_EBadgeType_TI8_Midweek: _ClassVar[EBadgeType]
    k_EBadgeType_TI8_Finals: _ClassVar[EBadgeType]
    k_EBadgeType_TI8_AllEvent: _ClassVar[EBadgeType]
    k_EBadgeType_TI10: _ClassVar[EBadgeType]
    k_EBadgeType_TI11_PlayoffsDay1: _ClassVar[EBadgeType]
    k_EBadgeType_TI11_PlayoffsDay2: _ClassVar[EBadgeType]
    k_EBadgeType_TI11_PlayoffsDay3: _ClassVar[EBadgeType]
    k_EBadgeType_TI11_PlayoffsDay4: _ClassVar[EBadgeType]
    k_EBadgeType_TI11_FinalsWeekend: _ClassVar[EBadgeType]
    k_EBadgeType_TI12_PlayoffsDay1: _ClassVar[EBadgeType]
    k_EBadgeType_TI12_PlayoffsDay2: _ClassVar[EBadgeType]
    k_EBadgeType_TI12_PlayoffsDay3: _ClassVar[EBadgeType]
    k_EBadgeType_TI12_FinalsWeekend: _ClassVar[EBadgeType]
    k_EBadgeType_TI12_Special: _ClassVar[EBadgeType]
    k_EBadgeType_TI13_FinalsDay1: _ClassVar[EBadgeType]
    k_EBadgeType_TI13_FinalsDay2: _ClassVar[EBadgeType]
    k_EBadgeType_TI13_FinalsDay3: _ClassVar[EBadgeType]
    k_EBadgeType_TI13_Special: _ClassVar[EBadgeType]
    k_EBadgeType_TI14_FinalsDay1: _ClassVar[EBadgeType]
    k_EBadgeType_TI14_FinalsDay2: _ClassVar[EBadgeType]
    k_EBadgeType_TI14_FinalsDay3: _ClassVar[EBadgeType]
    k_EBadgeType_TI14_FinalsDay4: _ClassVar[EBadgeType]
    k_EBadgeType_TI14_Special: _ClassVar[EBadgeType]

class ELeagueStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LEAGUE_STATUS_UNSET: _ClassVar[ELeagueStatus]
    LEAGUE_STATUS_UNSUBMITTED: _ClassVar[ELeagueStatus]
    LEAGUE_STATUS_SUBMITTED: _ClassVar[ELeagueStatus]
    LEAGUE_STATUS_ACCEPTED: _ClassVar[ELeagueStatus]
    LEAGUE_STATUS_REJECTED: _ClassVar[ELeagueStatus]
    LEAGUE_STATUS_CONCLUDED: _ClassVar[ELeagueStatus]
    LEAGUE_STATUS_DELETED: _ClassVar[ELeagueStatus]

class ELeagueRegion(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LEAGUE_REGION_UNSET: _ClassVar[ELeagueRegion]
    LEAGUE_REGION_NA: _ClassVar[ELeagueRegion]
    LEAGUE_REGION_SA: _ClassVar[ELeagueRegion]
    LEAGUE_REGION_WEU: _ClassVar[ELeagueRegion]
    LEAGUE_REGION_EEU: _ClassVar[ELeagueRegion]
    LEAGUE_REGION_CHINA: _ClassVar[ELeagueRegion]
    LEAGUE_REGION_SEA: _ClassVar[ELeagueRegion]

class ELeagueTier(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LEAGUE_TIER_UNSET: _ClassVar[ELeagueTier]
    LEAGUE_TIER_AMATEUR: _ClassVar[ELeagueTier]
    LEAGUE_TIER_PROFESSIONAL: _ClassVar[ELeagueTier]
    LEAGUE_TIER_MINOR: _ClassVar[ELeagueTier]
    LEAGUE_TIER_MAJOR: _ClassVar[ELeagueTier]
    LEAGUE_TIER_INTERNATIONAL: _ClassVar[ELeagueTier]
    LEAGUE_TIER_DPC_QUALIFIER: _ClassVar[ELeagueTier]
    LEAGUE_TIER_DPC_LEAGUE_QUALIFIER: _ClassVar[ELeagueTier]
    LEAGUE_TIER_DPC_LEAGUE: _ClassVar[ELeagueTier]
    LEAGUE_TIER_DPC_LEAGUE_FINALS: _ClassVar[ELeagueTier]

class ELeagueTierCategory(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LEAGUE_TIER_CATEGORY_AMATEUR: _ClassVar[ELeagueTierCategory]
    LEAGUE_TIER_CATEGORY_PROFESSIONAL: _ClassVar[ELeagueTierCategory]
    LEAGUE_TIER_CATEGORY_DPC: _ClassVar[ELeagueTierCategory]

class ELeagueDivision(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LEAGUE_DIVISION_UNSET: _ClassVar[ELeagueDivision]
    LEAGUE_DIVISION_I: _ClassVar[ELeagueDivision]
    LEAGUE_DIVISION_II: _ClassVar[ELeagueDivision]

class ELeagueBroadcastProvider(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LEAGUE_BROADCAST_UNKNOWN: _ClassVar[ELeagueBroadcastProvider]
    LEAGUE_BROADCAST_STEAM: _ClassVar[ELeagueBroadcastProvider]
    LEAGUE_BROADCAST_TWITCH: _ClassVar[ELeagueBroadcastProvider]
    LEAGUE_BROADCAST_YOUTUBE: _ClassVar[ELeagueBroadcastProvider]
    LEAGUE_BROADCAST_OTHER: _ClassVar[ELeagueBroadcastProvider]

class ELeaguePhase(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LEAGUE_PHASE_UNSET: _ClassVar[ELeaguePhase]
    LEAGUE_PHASE_REGIONAL_QUALIFIER: _ClassVar[ELeaguePhase]
    LEAGUE_PHASE_GROUP_STAGE: _ClassVar[ELeaguePhase]
    LEAGUE_PHASE_MAIN_EVENT: _ClassVar[ELeaguePhase]

class ELeagueAuditAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LEAGUE_AUDIT_ACTION_INVALID: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_LEAGUE_CREATE: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_LEAGUE_EDIT: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_LEAGUE_DELETE: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_LEAGUE_ADMIN_ADD: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_LEAGUE_ADMIN_REVOKE: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_LEAGUE_ADMIN_PROMOTE: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_LEAGUE_STREAM_ADD: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_LEAGUE_STREAM_REMOVE: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_LEAGUE_IMAGE_UPDATED: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_LEAGUE_MESSAGE_ADDED: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_LEAGUE_SUBMITTED: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_LEAGUE_SET_PRIZE_POOL: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_LEAGUE_ADD_PRIZE_POOL_ITEM: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_LEAGUE_REMOVE_PRIZE_POOL_ITEM: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_LEAGUE_MATCH_START: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_LEAGUE_MATCH_END: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_LEAGUE_ADD_INVITED_TEAM: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_LEAGUE_REMOVE_INVITED_TEAM: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_LEAGUE_STATUS_CHANGED: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_LEAGUE_STREAM_EDIT: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_LEAGUE_TEAM_SWAP: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_NODEGROUP_CREATE: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_NODEGROUP_DESTROY: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_NODEGROUP_ADD_TEAM: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_NODEGROUP_REMOVE_TEAM: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_NODEGROUP_SET_ADVANCING: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_NODEGROUP_EDIT: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_NODEGROUP_POPULATE: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_NODEGROUP_COMPLETED: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_NODEGROUP_SET_SECONDARY_ADVANCING: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_NODEGROUP_SET_TERTIARY_ADVANCING: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_NODE_CREATE: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_NODE_DESTROY: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_NODE_AUTOCREATE: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_NODE_SET_TEAM: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_NODE_SET_SERIES_ID: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_NODE_SET_ADVANCING: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_NODE_SET_TIME: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_NODE_MATCH_COMPLETED: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_NODE_COMPLETED: _ClassVar[ELeagueAuditAction]
    LEAGUE_AUDIT_ACTION_NODE_EDIT: _ClassVar[ELeagueAuditAction]

class DOTA_COMBATLOG_TYPES(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOTA_COMBATLOG_INVALID: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_DAMAGE: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_HEAL: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_MODIFIER_ADD: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_MODIFIER_REMOVE: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_DEATH: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_ABILITY: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_ITEM: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_LOCATION: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_GOLD: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_GAME_STATE: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_XP: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_PURCHASE: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_BUYBACK: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_ABILITY_TRIGGER: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_PLAYERSTATS: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_MULTIKILL: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_KILLSTREAK: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_TEAM_BUILDING_KILL: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_FIRST_BLOOD: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_MODIFIER_STACK_EVENT: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_NEUTRAL_CAMP_STACK: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_PICKUP_RUNE: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_REVEALED_INVISIBLE: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_HERO_SAVED: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_MANA_RESTORED: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_HERO_LEVELUP: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_BOTTLE_HEAL_ALLY: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_ENDGAME_STATS: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_INTERRUPT_CHANNEL: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_ALLIED_GOLD: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_AEGIS_TAKEN: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_MANA_DAMAGE: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_PHYSICAL_DAMAGE_PREVENTED: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_UNIT_SUMMONED: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_ATTACK_EVADE: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_TREE_CUT: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_SUCCESSFUL_SCAN: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_END_KILLSTREAK: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_BLOODSTONE_CHARGE: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_CRITICAL_DAMAGE: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_SPELL_ABSORB: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_UNIT_TELEPORTED: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_KILL_EATER_EVENT: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_NEUTRAL_ITEM_EARNED: _ClassVar[DOTA_COMBATLOG_TYPES]
    DOTA_COMBATLOG_STAT_TRACKER_PLAYER: _ClassVar[DOTA_COMBATLOG_TYPES]

class EDPCFavoriteType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FAVORITE_TYPE_ALL: _ClassVar[EDPCFavoriteType]
    FAVORITE_TYPE_PLAYER: _ClassVar[EDPCFavoriteType]
    FAVORITE_TYPE_TEAM: _ClassVar[EDPCFavoriteType]
    FAVORITE_TYPE_LEAGUE: _ClassVar[EDPCFavoriteType]

class EDPCPushNotification(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DPC_PUSH_NOTIFICATION_MATCH_STARTING: _ClassVar[EDPCPushNotification]
    DPC_PUSH_NOTIFICATION_PLAYER_LEFT_TEAM: _ClassVar[EDPCPushNotification]
    DPC_PUSH_NOTIFICATION_PLAYER_JOINED_TEAM: _ClassVar[EDPCPushNotification]
    DPC_PUSH_NOTIFICATION_PLAYER_JOINED_TEAM_AS_COACH: _ClassVar[EDPCPushNotification]
    DPC_PUSH_NOTIFICATION_PLAYER_LEFT_TEAM_AS_COACH: _ClassVar[EDPCPushNotification]
    DPC_PUSH_NOTIFICATION_LEAGUE_RESULT: _ClassVar[EDPCPushNotification]
    DPC_PUSH_NOTIFICATION_PREDICTION_MATCHES_AVAILABLE: _ClassVar[EDPCPushNotification]
    DPC_PUSH_NOTIFICATION_PREDICTION_RESULT: _ClassVar[EDPCPushNotification]
    DPC_PUSH_NOTIFICATION_FANTASY_PLAYER_CLEARED: _ClassVar[EDPCPushNotification]
    DPC_PUSH_NOTIFICATION_FANTASY_DAILY_SUMMARY: _ClassVar[EDPCPushNotification]
    DPC_PUSH_NOTIFICATION_FANTASY_FINAL_RESULTS: _ClassVar[EDPCPushNotification]

class EEventActionScoreMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eEventActionScoreMode_Add: _ClassVar[EEventActionScoreMode]
    k_eEventActionScoreMode_Min: _ClassVar[EEventActionScoreMode]

class EPlayerChallengeHistoryType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EPlayerChallengeHistoryType_Invalid: _ClassVar[EPlayerChallengeHistoryType]
    k_EPlayerChallengeHistoryType_KillEater: _ClassVar[EPlayerChallengeHistoryType]
    k_EPlayerChallengeHistoryType_DotaPlusRelic: _ClassVar[EPlayerChallengeHistoryType]
    k_EPlayerChallengeHistoryType_DotaPlusHeroPlayerChallenge: _ClassVar[
        EPlayerChallengeHistoryType
    ]
    k_EPlayerChallengeHistoryType_InGameEventChallenge: _ClassVar[EPlayerChallengeHistoryType]
    k_EPlayerChallengeHistoryType_GuildContract: _ClassVar[EPlayerChallengeHistoryType]

class EOverwatchReportReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EOverwatchReportReason_Unknown: _ClassVar[EOverwatchReportReason]
    k_EOverwatchReportReason_Cheating: _ClassVar[EOverwatchReportReason]
    k_EOverwatchReportReason_Feeding: _ClassVar[EOverwatchReportReason]
    k_EOverwatchReportReason_Griefing: _ClassVar[EOverwatchReportReason]
    k_EOverwatchReportReason_Suspicious: _ClassVar[EOverwatchReportReason]
    k_EOverwatchReportReason_AbilityAbuse: _ClassVar[EOverwatchReportReason]

class ECandyShopUpgrade(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_ECandyShopUpgradeInvalid: _ClassVar[ECandyShopUpgrade]
    k_ECandyShopUpgrade_InventorySize: _ClassVar[ECandyShopUpgrade]
    k_ECandyShopUpgrade_RewardShelf: _ClassVar[ECandyShopUpgrade]
    k_ECandyShopUpgrade_ExtraExchangeRecipe: _ClassVar[ECandyShopUpgrade]

class EItemSuggestPreference(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EItemSuggestPreference_None: _ClassVar[EItemSuggestPreference]
    k_EItemSuggestPreference_Liked: _ClassVar[EItemSuggestPreference]
    k_EItemSuggestPreference_Disliked: _ClassVar[EItemSuggestPreference]

class ETimerAlertType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_TimerAlertType_PowerRune: _ClassVar[ETimerAlertType]
    k_TimerAlertType_BountyRune: _ClassVar[ETimerAlertType]
    k_TimerAlertType_WisdomShrine: _ClassVar[ETimerAlertType]
    k_TimerAlertType_JungleCamps: _ClassVar[ETimerAlertType]
    k_TimerAlertType_LotusPool: _ClassVar[ETimerAlertType]

DOTA_GAMEMODE_NONE: DOTA_GameMode
DOTA_GAMEMODE_AP: DOTA_GameMode
DOTA_GAMEMODE_CM: DOTA_GameMode
DOTA_GAMEMODE_RD: DOTA_GameMode
DOTA_GAMEMODE_SD: DOTA_GameMode
DOTA_GAMEMODE_AR: DOTA_GameMode
DOTA_GAMEMODE_INTRO: DOTA_GameMode
DOTA_GAMEMODE_HW: DOTA_GameMode
DOTA_GAMEMODE_REVERSE_CM: DOTA_GameMode
DOTA_GAMEMODE_XMAS: DOTA_GameMode
DOTA_GAMEMODE_TUTORIAL: DOTA_GameMode
DOTA_GAMEMODE_MO: DOTA_GameMode
DOTA_GAMEMODE_LP: DOTA_GameMode
DOTA_GAMEMODE_POOL1: DOTA_GameMode
DOTA_GAMEMODE_FH: DOTA_GameMode
DOTA_GAMEMODE_CUSTOM: DOTA_GameMode
DOTA_GAMEMODE_CD: DOTA_GameMode
DOTA_GAMEMODE_BD: DOTA_GameMode
DOTA_GAMEMODE_ABILITY_DRAFT: DOTA_GameMode
DOTA_GAMEMODE_EVENT: DOTA_GameMode
DOTA_GAMEMODE_ARDM: DOTA_GameMode
DOTA_GAMEMODE_1V1MID: DOTA_GameMode
DOTA_GAMEMODE_ALL_DRAFT: DOTA_GameMode
DOTA_GAMEMODE_TURBO: DOTA_GameMode
DOTA_GAMEMODE_MUTATION: DOTA_GameMode
DOTA_GAMEMODE_COACHES_CHALLENGE: DOTA_GameMode
DOTA_GAMEMODE_BOT_CHALLENGE: DOTA_GameMode
DOTA_GAMERULES_STATE_INIT: DOTA_GameState
DOTA_GAMERULES_STATE_WAIT_FOR_PLAYERS_TO_LOAD: DOTA_GameState
DOTA_GAMERULES_STATE_HERO_SELECTION: DOTA_GameState
DOTA_GAMERULES_STATE_STRATEGY_TIME: DOTA_GameState
DOTA_GAMERULES_STATE_PRE_GAME: DOTA_GameState
DOTA_GAMERULES_STATE_GAME_IN_PROGRESS: DOTA_GameState
DOTA_GAMERULES_STATE_POST_GAME: DOTA_GameState
DOTA_GAMERULES_STATE_DISCONNECT: DOTA_GameState
DOTA_GAMERULES_STATE_TEAM_SHOWCASE: DOTA_GameState
DOTA_GAMERULES_STATE_CUSTOM_GAME_SETUP: DOTA_GameState
DOTA_GAMERULES_STATE_WAIT_FOR_MAP_TO_LOAD: DOTA_GameState
DOTA_GAMERULES_STATE_SCENARIO_SETUP: DOTA_GameState
DOTA_GAMERULES_STATE_PLAYER_DRAFT: DOTA_GameState
DOTA_GAMERULES_STATE_LAST: DOTA_GameState
DOTA_GC_TEAM_GOOD_GUYS: DOTA_GC_TEAM
DOTA_GC_TEAM_BAD_GUYS: DOTA_GC_TEAM
DOTA_GC_TEAM_BROADCASTER: DOTA_GC_TEAM
DOTA_GC_TEAM_SPECTATOR: DOTA_GC_TEAM
DOTA_GC_TEAM_PLAYER_POOL: DOTA_GC_TEAM
DOTA_GC_TEAM_NOTEAM: DOTA_GC_TEAM
DOTA_GC_TEAM_CUSTOM_1: DOTA_GC_TEAM
DOTA_GC_TEAM_CUSTOM_2: DOTA_GC_TEAM
DOTA_GC_TEAM_CUSTOM_3: DOTA_GC_TEAM
DOTA_GC_TEAM_CUSTOM_4: DOTA_GC_TEAM
DOTA_GC_TEAM_CUSTOM_5: DOTA_GC_TEAM
DOTA_GC_TEAM_CUSTOM_6: DOTA_GC_TEAM
DOTA_GC_TEAM_CUSTOM_7: DOTA_GC_TEAM
DOTA_GC_TEAM_CUSTOM_8: DOTA_GC_TEAM
DOTA_GC_TEAM_NEUTRALS: DOTA_GC_TEAM
EVENT_ID_NONE: EEvent
EVENT_ID_DIRETIDE: EEvent
EVENT_ID_SPRING_FESTIVAL: EEvent
EVENT_ID_FROSTIVUS_2013: EEvent
EVENT_ID_COMPENDIUM_2014: EEvent
EVENT_ID_NEXON_PC_BANG: EEvent
EVENT_ID_PWRD_DAC_2015: EEvent
EVENT_ID_NEW_BLOOM_2015: EEvent
EVENT_ID_INTERNATIONAL_2015: EEvent
EVENT_ID_FALL_MAJOR_2015: EEvent
EVENT_ID_ORACLE_PA: EEvent
EVENT_ID_NEW_BLOOM_2015_PREBEAST: EEvent
EVENT_ID_FROSTIVUS: EEvent
EVENT_ID_WINTER_MAJOR_2016: EEvent
EVENT_ID_INTERNATIONAL_2016: EEvent
EVENT_ID_FALL_MAJOR_2016: EEvent
EVENT_ID_WINTER_MAJOR_2017: EEvent
EVENT_ID_NEW_BLOOM_2017: EEvent
EVENT_ID_INTERNATIONAL_2017: EEvent
EVENT_ID_PLUS_SUBSCRIPTION: EEvent
EVENT_ID_SINGLES_DAY_2017: EEvent
EVENT_ID_FROSTIVUS_2017: EEvent
EVENT_ID_INTERNATIONAL_2018: EEvent
EVENT_ID_FROSTIVUS_2018: EEvent
EVENT_ID_NEW_BLOOM_2019: EEvent
EVENT_ID_INTERNATIONAL_2019: EEvent
EVENT_ID_NEW_PLAYER_EXPERIENCE: EEvent
EVENT_ID_FROSTIVUS_2019: EEvent
EVENT_ID_NEW_BLOOM_2020: EEvent
EVENT_ID_INTERNATIONAL_2020: EEvent
EVENT_ID_TEAM_FANDOM: EEvent
EVENT_ID_DIRETIDE_2020: EEvent
EVENT_ID_SPRING_2021: EEvent
EVENT_ID_FALL_2021: EEvent
EVENT_ID_TEAM_FANDOM_FALL_2021: EEvent
EVENT_ID_TEAM_2021_2022_TOUR2: EEvent
EVENT_ID_INTERNATIONAL_2022: EEvent
EVENT_ID_TEAM_2021_2022_TOUR3: EEvent
EVENT_ID_TEAM_INTERNATIONAL_2022: EEvent
EVENT_ID_PERMANENT_GRANTS: EEvent
EVENT_ID_MUERTA_RELEASE_SPRING2023: EEvent
EVENT_ID_TEAM_2023_TOUR1: EEvent
EVENT_ID_TEAM_2023_TOUR2: EEvent
EVENT_ID_TEAM_2023_TOUR3: EEvent
EVENT_ID_INTERNATIONAL_2023: EEvent
EVENT_ID_10TH_ANNIVERSARY: EEvent
EVENT_ID_CROWNFALL: EEvent
EVENT_ID_FROSTIVUS_2023: EEvent
EVENT_ID_INTERNATIONAL_2024: EEvent
EVENT_ID_FROSTIVUS_2024: EEvent
EVENT_ID_MONSTER_HUNTER: EEvent
EVENT_ID_INTERNATIONAL_2025: EEvent
EVENT_ID_FALL_2025: EEvent
EVENT_ID_WINTER_2025: EEvent
EVENT_ID_SPRING_2026: EEvent
EVENT_ID_SUMMER_2026: EEvent
EVENT_ID_FALL_2026: EEvent
EVENT_ID_WINTER_2026: EEvent
k_ERankType_Invalid: ERankType
k_ERankType_Casual: ERankType
k_ERankType_Ranked: ERankType
k_ERankType_CasualLegacy: ERankType
k_ERankType_RankedLegacy: ERankType
k_ERankType_CasualGlicko: ERankType
k_ERankType_RankedGlicko: ERankType
k_ERankType_RankMax: ERankType
k_ERankType_BehaviorPrivate: ERankType
k_ERankType_BehaviorPublic: ERankType
k_ERankType_Max: ERankType
DOTA_LEAVER_NONE: DOTALeaverStatus_t
DOTA_LEAVER_DISCONNECTED: DOTALeaverStatus_t
DOTA_LEAVER_DISCONNECTED_TOO_LONG: DOTALeaverStatus_t
DOTA_LEAVER_ABANDONED: DOTALeaverStatus_t
DOTA_LEAVER_AFK: DOTALeaverStatus_t
DOTA_LEAVER_NEVER_CONNECTED: DOTALeaverStatus_t
DOTA_LEAVER_NEVER_CONNECTED_TOO_LONG: DOTALeaverStatus_t
DOTA_LEAVER_FAILED_TO_READY_UP: DOTALeaverStatus_t
DOTA_LEAVER_DECLINED: DOTALeaverStatus_t
DOTA_LEAVER_DECLINED_REQUEUE: DOTALeaverStatus_t
DOTA_CONNECTION_STATE_UNKNOWN: DOTAConnectionState_t
DOTA_CONNECTION_STATE_NOT_YET_CONNECTED: DOTAConnectionState_t
DOTA_CONNECTION_STATE_CONNECTED: DOTAConnectionState_t
DOTA_CONNECTION_STATE_DISCONNECTED: DOTAConnectionState_t
DOTA_CONNECTION_STATE_ABANDONED: DOTAConnectionState_t
DOTA_CONNECTION_STATE_LOADING: DOTAConnectionState_t
DOTA_CONNECTION_STATE_FAILED: DOTAConnectionState_t
FANTASY_ROLE_UNDEFINED: Fantasy_Roles
FANTASY_ROLE_CORE: Fantasy_Roles
FANTASY_ROLE_SUPPORT: Fantasy_Roles
FANTASY_ROLE_OFFLANE: Fantasy_Roles
FANTASY_ROLE_MID: Fantasy_Roles
FANTASY_SCORING_KILLS: Fantasy_Scoring
FANTASY_SCORING_DEATHS: Fantasy_Scoring
FANTASY_SCORING_CS: Fantasy_Scoring
FANTASY_SCORING_GPM: Fantasy_Scoring
FANTASY_SCORING_TOWER_KILLS: Fantasy_Scoring
FANTASY_SCORING_ROSHAN_KILLS: Fantasy_Scoring
FANTASY_SCORING_TEAMFIGHT_PARTICIPATION: Fantasy_Scoring
FANTASY_SCORING_WARDS_PLANTED: Fantasy_Scoring
FANTASY_SCORING_CAMPS_STACKED: Fantasy_Scoring
FANTASY_SCORING_RUNES_GRABBED: Fantasy_Scoring
FANTASY_SCORING_FIRST_BLOOD: Fantasy_Scoring
FANTASY_SCORING_STUNS: Fantasy_Scoring
FANTASY_SCORING_SMOKES_USED: Fantasy_Scoring
FANTASY_SCORING_MADSTONE: Fantasy_Scoring
FANTASY_SCORING_WATCHERS_TAKEN: Fantasy_Scoring
FANTASY_SCORING_LOTUSES_GAINED: Fantasy_Scoring
FANTASY_SCORING_TORMENTOR_KILLS: Fantasy_Scoring
FANTASY_SCORING_COURIER_KILLS: Fantasy_Scoring
FANTASY_SCORING_TYPES: Fantasy_Scoring
FANTASY_SCORING_INVALID: Fantasy_Scoring
FANTASY_SLOT_NONE: Fantasy_Team_Slots
FANTASY_SLOT_CORE: Fantasy_Team_Slots
FANTASY_SLOT_SUPPORT: Fantasy_Team_Slots
FANTASY_SLOT_ANY: Fantasy_Team_Slots
FANTASY_SLOT_BENCH: Fantasy_Team_Slots
FANTASY_SELECTION_INVALID: Fantasy_Selection_Mode
FANTASY_SELECTION_LOCKED: Fantasy_Selection_Mode
FANTASY_SELECTION_SHUFFLE: Fantasy_Selection_Mode
FANTASY_SELECTION_FREE_PICK: Fantasy_Selection_Mode
FANTASY_SELECTION_ENDED: Fantasy_Selection_Mode
FANTASY_SELECTION_PRE_SEASON: Fantasy_Selection_Mode
FANTASY_SELECTION_PRE_DRAFT: Fantasy_Selection_Mode
FANTASY_SELECTION_DRAFTING: Fantasy_Selection_Mode
FANTASY_SELECTION_REGULAR_SEASON: Fantasy_Selection_Mode
FANTASY_SELECTION_CARD_BASED: Fantasy_Selection_Mode
FANTASY_GEM_TYPE_RUBY: Fantasy_Gem_Type
FANTASY_GEM_TYPE_SAPPHIRE: Fantasy_Gem_Type
FANTASY_GEM_TYPE_EMERALD: Fantasy_Gem_Type
DOTAChannelType_Regional: DOTAChatChannelType_t
DOTAChannelType_Custom: DOTAChatChannelType_t
DOTAChannelType_Party: DOTAChatChannelType_t
DOTAChannelType_Lobby: DOTAChatChannelType_t
DOTAChannelType_Team: DOTAChatChannelType_t
DOTAChannelType_Guild: DOTAChatChannelType_t
DOTAChannelType_Fantasy: DOTAChatChannelType_t
DOTAChannelType_Whisper: DOTAChatChannelType_t
DOTAChannelType_Console: DOTAChatChannelType_t
DOTAChannelType_Tab: DOTAChatChannelType_t
DOTAChannelType_Invalid: DOTAChatChannelType_t
DOTAChannelType_GameAll: DOTAChatChannelType_t
DOTAChannelType_GameAllies: DOTAChatChannelType_t
DOTAChannelType_GameSpectator: DOTAChatChannelType_t
DOTAChannelType_GameCoaching: DOTAChatChannelType_t
DOTAChannelType_Cafe: DOTAChatChannelType_t
DOTAChannelType_CustomGame: DOTAChatChannelType_t
DOTAChannelType_Private: DOTAChatChannelType_t
DOTAChannelType_PostGame: DOTAChatChannelType_t
DOTAChannelType_BattleCup: DOTAChatChannelType_t
DOTAChannelType_HLTVSpectator: DOTAChatChannelType_t
DOTAChannelType_GameEvents: DOTAChatChannelType_t
DOTAChannelType_Trivia: DOTAChatChannelType_t
DOTAChannelType_NewPlayer: DOTAChatChannelType_t
DOTAChannelType_PrivateCoaching: DOTAChatChannelType_t
k_EChatSpecialPrivileges_None: EChatSpecialPrivileges
k_EChatSpecialPrivileges_Moderator: EChatSpecialPrivileges
k_EChatSpecialPrivileges_SuperModerator: EChatSpecialPrivileges
DOTA_COMM_TYPE_NONE: DOTACommType_t
DOTA_COMM_TYPE_PING: DOTACommType_t
DOTA_COMM_TYPE_CHATWHEEL: DOTACommType_t
DOTA_COMM_TYPE_TIP: DOTACommType_t
DOTA_COMM_TYPE_TEXT: DOTACommType_t
DOTA_COMM_TYPE_SHOWCASE: DOTACommType_t
DOTA_COMM_TYPE_VOICE: DOTACommType_t
DOTA_COMM_TYPE_ALLY_ABILITY: DOTACommType_t
DOTA_COMM_TYPE_PAUSE: DOTACommType_t
DOTA_COMM_TYPE_COACHING: DOTACommType_t
DOTA_COMM_TYPE_NOCOOLDOWN: DOTACommType_t
DOTA_COMM_TYPE_RANKEDMATCHMAKE: DOTACommType_t
DOTA_COMM_TYPE_DROPS: DOTACommType_t
DOTA_COMM_TYPE_NEWPLAYER_EXPERT: DOTACommType_t
DOTA_COMM_TYPE_COACHED: DOTACommType_t
DOTA_COMM_TYPE_MAPDRAWING: DOTACommType_t
DOTA_COMM_LEVEL_NONE: DOTACommLevel_t
DOTA_COMM_LEVEL_COOLDOWN: DOTACommLevel_t
DOTA_COMM_LEVEL_PINGS: DOTACommLevel_t
DOTA_COMM_LEVEL_MAPDRAWING: DOTACommLevel_t
DOTA_COMM_LEVEL_CHAT: DOTACommLevel_t
DOTA_COMM_LEVEL_TIPPING: DOTACommLevel_t
DOTA_COMM_LEVEL_VOICE: DOTACommLevel_t
DOTA_COMM_LEVEL_ALLIED_ABILITY: DOTACommLevel_t
DOTA_BEHAVIOR_LEVEL_NONE: DOTABehaviorLevel_t
DOTA_BEHAVIOR_LEVEL_RANKED_ALLOWED: DOTABehaviorLevel_t
DOTA_BEHAVIOR_LEVEL_PAUSING: DOTABehaviorLevel_t
DOTA_BEHAVIOR_LEVEL_DROPS: DOTABehaviorLevel_t
DOTA_BEHAVIOR_LEVEL_COACHING: DOTABehaviorLevel_t
k_EProfileCardSlotType_Empty: EProfileCardSlotType
k_EProfileCardSlotType_Stat: EProfileCardSlotType
k_EProfileCardSlotType_Trophy: EProfileCardSlotType
k_EProfileCardSlotType_Item: EProfileCardSlotType
k_EProfileCardSlotType_Hero: EProfileCardSlotType
k_EProfileCardSlotType_Emoticon: EProfileCardSlotType
k_EProfileCardSlotType_Team: EProfileCardSlotType
k_EMatchGroupServerStatus_OK: EMatchGroupServerStatus
k_EMatchGroupServerStatus_LimitedAvailability: EMatchGroupServerStatus
k_EMatchGroupServerStatus_Offline: EMatchGroupServerStatus
DOTA_CM_RANDOM: DOTA_CM_PICK
DOTA_CM_GOOD_GUYS: DOTA_CM_PICK
DOTA_CM_BAD_GUYS: DOTA_CM_PICK
DOTA_LOW_PRIORITY_BAN_ABANDON: DOTALowPriorityBanType
DOTA_LOW_PRIORITY_BAN_REPORTS: DOTALowPriorityBanType
DOTA_LOW_PRIORITY_BAN_SECONDARY_ABANDON: DOTALowPriorityBanType
DOTA_LOW_PRIORITY_BAN_PRE_GAME_ROLE: DOTALowPriorityBanType
DOTALobbyReadyState_UNDECLARED: DOTALobbyReadyState
DOTALobbyReadyState_ACCEPTED: DOTALobbyReadyState
DOTALobbyReadyState_DECLINED: DOTALobbyReadyState
DOTALobbyReadyState_DECLINED_REQUEUE: DOTALobbyReadyState
DOTA_JOIN_RESULT_SUCCESS: DOTAJoinLobbyResult
DOTA_JOIN_RESULT_ALREADY_IN_GAME: DOTAJoinLobbyResult
DOTA_JOIN_RESULT_INVALID_LOBBY: DOTAJoinLobbyResult
DOTA_JOIN_RESULT_INCORRECT_PASSWORD: DOTAJoinLobbyResult
DOTA_JOIN_RESULT_ACCESS_DENIED: DOTAJoinLobbyResult
DOTA_JOIN_RESULT_GENERIC_ERROR: DOTAJoinLobbyResult
DOTA_JOIN_RESULT_INCORRECT_VERSION: DOTAJoinLobbyResult
DOTA_JOIN_RESULT_IN_TEAM_PARTY: DOTAJoinLobbyResult
DOTA_JOIN_RESULT_NO_LOBBY_FOUND: DOTAJoinLobbyResult
DOTA_JOIN_RESULT_LOBBY_FULL: DOTAJoinLobbyResult
DOTA_JOIN_RESULT_CUSTOM_GAME_INCORRECT_VERSION: DOTAJoinLobbyResult
DOTA_JOIN_RESULT_TIMEOUT: DOTAJoinLobbyResult
DOTA_JOIN_RESULT_CUSTOM_GAME_COOLDOWN: DOTAJoinLobbyResult
DOTA_JOIN_RESULT_BUSY: DOTAJoinLobbyResult
DOTA_JOIN_RESULT_NO_PLAYTIME: DOTAJoinLobbyResult
k_DOTASelectionPriorityRules_Manual: DOTASelectionPriorityRules
k_DOTASelectionPriorityRules_Automatic: DOTASelectionPriorityRules
k_DOTASelectionPriorityChoice_Invalid: DOTASelectionPriorityChoice
k_DOTASelectionPriorityChoice_FirstPick: DOTASelectionPriorityChoice
k_DOTASelectionPriorityChoice_SecondPick: DOTASelectionPriorityChoice
k_DOTASelectionPriorityChoice_Radiant: DOTASelectionPriorityChoice
k_DOTASelectionPriorityChoice_Dire: DOTASelectionPriorityChoice
DOTAMatchVote_INVALID: DOTAMatchVote
DOTAMatchVote_POSITIVE: DOTAMatchVote
DOTAMatchVote_NEGATIVE: DOTAMatchVote
DOTALobbyVisibility_Public: DOTALobbyVisibility
DOTALobbyVisibility_Friends: DOTALobbyVisibility
DOTALobbyVisibility_Unlisted: DOTALobbyVisibility
k_EDOTAPlayerMMRType_Invalid: EDOTAPlayerMMRType
k_EDOTAPlayerMMRType_GeneralHidden: EDOTAPlayerMMRType
k_EDOTAPlayerMMRType_GeneralCompetitive: EDOTAPlayerMMRType
k_EDOTAMMRBoostType_None: EDOTAMMRBoostType
k_EDOTAMMRBoostType_Leader: EDOTAMMRBoostType
k_EDOTAMMRBoostType_Follower: EDOTAMMRBoostType
MATCH_TYPE_CASUAL: MatchType
MATCH_TYPE_COOP_BOTS: MatchType
MATCH_TYPE_COMPETITIVE: MatchType
MATCH_TYPE_WEEKEND_TOURNEY: MatchType
MATCH_TYPE_EVENT: MatchType
MATCH_TYPE_COACHES_CHALLENGE: MatchType
MATCH_TYPE_NEW_PLAYER_POOL: MatchType
BOT_DIFFICULTY_PASSIVE: DOTABotDifficulty
BOT_DIFFICULTY_EASY: DOTABotDifficulty
BOT_DIFFICULTY_MEDIUM: DOTABotDifficulty
BOT_DIFFICULTY_HARD: DOTABotDifficulty
BOT_DIFFICULTY_UNFAIR: DOTABotDifficulty
BOT_DIFFICULTY_INVALID: DOTABotDifficulty
BOT_DIFFICULTY_EXTRA1: DOTABotDifficulty
BOT_DIFFICULTY_EXTRA2: DOTABotDifficulty
BOT_DIFFICULTY_EXTRA3: DOTABotDifficulty
BOT_DIFFICULTY_NPX: DOTABotDifficulty
DOTA_BOT_MODE_NONE: DOTA_BOT_MODE
DOTA_BOT_MODE_LANING: DOTA_BOT_MODE
DOTA_BOT_MODE_ATTACK: DOTA_BOT_MODE
DOTA_BOT_MODE_ROAM: DOTA_BOT_MODE
DOTA_BOT_MODE_RETREAT: DOTA_BOT_MODE
DOTA_BOT_MODE_SECRET_SHOP: DOTA_BOT_MODE
DOTA_BOT_MODE_SIDE_SHOP: DOTA_BOT_MODE
DOTA_BOT_MODE_RUNE: DOTA_BOT_MODE
DOTA_BOT_MODE_PUSH_TOWER_TOP: DOTA_BOT_MODE
DOTA_BOT_MODE_PUSH_TOWER_MID: DOTA_BOT_MODE
DOTA_BOT_MODE_PUSH_TOWER_BOT: DOTA_BOT_MODE
DOTA_BOT_MODE_DEFEND_TOWER_TOP: DOTA_BOT_MODE
DOTA_BOT_MODE_DEFEND_TOWER_MID: DOTA_BOT_MODE
DOTA_BOT_MODE_DEFEND_TOWER_BOT: DOTA_BOT_MODE
DOTA_BOT_MODE_ASSEMBLE: DOTA_BOT_MODE
DOTA_BOT_MODE_ASSEMBLE_WITH_HUMANS: DOTA_BOT_MODE
DOTA_BOT_MODE_TEAM_ROAM: DOTA_BOT_MODE
DOTA_BOT_MODE_FARM: DOTA_BOT_MODE
DOTA_BOT_MODE_DEFEND_ALLY: DOTA_BOT_MODE
DOTA_BOT_MODE_EVASIVE_MANEUVERS: DOTA_BOT_MODE
DOTA_BOT_MODE_ROSHAN: DOTA_BOT_MODE
DOTA_BOT_MODE_ITEM: DOTA_BOT_MODE
DOTA_BOT_MODE_WARD: DOTA_BOT_MODE
DOTA_BOT_MODE_COMPANION: DOTA_BOT_MODE
DOTA_BOT_MODE_TUTORIAL_BOSS: DOTA_BOT_MODE
DOTA_BOT_MODE_MINION: DOTA_BOT_MODE
DOTA_BOT_MODE_OUTPOST: DOTA_BOT_MODE
DOTA_BOT_MODE_BOT_CHALLENGE_ENDGAME: DOTA_BOT_MODE
MATCH_LANGUAGE_INVALID: MatchLanguages
MATCH_LANGUAGE_ENGLISH: MatchLanguages
MATCH_LANGUAGE_RUSSIAN: MatchLanguages
MATCH_LANGUAGE_CHINESE: MatchLanguages
MATCH_LANGUAGE_KOREAN: MatchLanguages
MATCH_LANGUAGE_SPANISH: MatchLanguages
MATCH_LANGUAGE_PORTUGUESE: MatchLanguages
MATCH_LANGUAGE_ENGLISH2: MatchLanguages
k_ETourneyQueueDeadlineState_Normal: ETourneyQueueDeadlineState
k_ETourneyQueueDeadlineState_Missed: ETourneyQueueDeadlineState
k_ETourneyQueueDeadlineState_ExpiredOK: ETourneyQueueDeadlineState
k_ETourneyQueueDeadlineState_SeekingBye: ETourneyQueueDeadlineState
k_ETourneyQueueDeadlineState_EligibleForRefund: ETourneyQueueDeadlineState
k_ETourneyQueueDeadlineState_NA: ETourneyQueueDeadlineState
k_ETourneyQueueDeadlineState_ExpiringSoon: ETourneyQueueDeadlineState
k_EMatchOutcome_Unknown: EMatchOutcome
k_EMatchOutcome_RadVictory: EMatchOutcome
k_EMatchOutcome_DireVictory: EMatchOutcome
k_EMatchOutcome_NeutralVictory: EMatchOutcome
k_EMatchOutcome_NoTeamWinner: EMatchOutcome
k_EMatchOutcome_Custom1Victory: EMatchOutcome
k_EMatchOutcome_Custom2Victory: EMatchOutcome
k_EMatchOutcome_Custom3Victory: EMatchOutcome
k_EMatchOutcome_Custom4Victory: EMatchOutcome
k_EMatchOutcome_Custom5Victory: EMatchOutcome
k_EMatchOutcome_Custom6Victory: EMatchOutcome
k_EMatchOutcome_Custom7Victory: EMatchOutcome
k_EMatchOutcome_Custom8Victory: EMatchOutcome
k_EMatchOutcome_NotScored_PoorNetworkConditions: EMatchOutcome
k_EMatchOutcome_NotScored_Leaver: EMatchOutcome
k_EMatchOutcome_NotScored_ServerCrash: EMatchOutcome
k_EMatchOutcome_NotScored_NeverStarted: EMatchOutcome
k_EMatchOutcome_NotScored_Canceled: EMatchOutcome
k_EMatchOutcome_NotScored_Suspicious: EMatchOutcome
LANE_TYPE_UNKNOWN: ELaneType
LANE_TYPE_SAFE: ELaneType
LANE_TYPE_OFF: ELaneType
LANE_TYPE_MID: ELaneType
LANE_TYPE_JUNGLE: ELaneType
LANE_TYPE_ROAM: ELaneType
k_EBadgeType_Invalid: EBadgeType
k_EBadgeType_TI7_Midweek: EBadgeType
k_EBadgeType_TI7_Finals: EBadgeType
k_EBadgeType_TI7_AllEvent: EBadgeType
k_EBadgeType_TI8_Midweek: EBadgeType
k_EBadgeType_TI8_Finals: EBadgeType
k_EBadgeType_TI8_AllEvent: EBadgeType
k_EBadgeType_TI10: EBadgeType
k_EBadgeType_TI11_PlayoffsDay1: EBadgeType
k_EBadgeType_TI11_PlayoffsDay2: EBadgeType
k_EBadgeType_TI11_PlayoffsDay3: EBadgeType
k_EBadgeType_TI11_PlayoffsDay4: EBadgeType
k_EBadgeType_TI11_FinalsWeekend: EBadgeType
k_EBadgeType_TI12_PlayoffsDay1: EBadgeType
k_EBadgeType_TI12_PlayoffsDay2: EBadgeType
k_EBadgeType_TI12_PlayoffsDay3: EBadgeType
k_EBadgeType_TI12_FinalsWeekend: EBadgeType
k_EBadgeType_TI12_Special: EBadgeType
k_EBadgeType_TI13_FinalsDay1: EBadgeType
k_EBadgeType_TI13_FinalsDay2: EBadgeType
k_EBadgeType_TI13_FinalsDay3: EBadgeType
k_EBadgeType_TI13_Special: EBadgeType
k_EBadgeType_TI14_FinalsDay1: EBadgeType
k_EBadgeType_TI14_FinalsDay2: EBadgeType
k_EBadgeType_TI14_FinalsDay3: EBadgeType
k_EBadgeType_TI14_FinalsDay4: EBadgeType
k_EBadgeType_TI14_Special: EBadgeType
LEAGUE_STATUS_UNSET: ELeagueStatus
LEAGUE_STATUS_UNSUBMITTED: ELeagueStatus
LEAGUE_STATUS_SUBMITTED: ELeagueStatus
LEAGUE_STATUS_ACCEPTED: ELeagueStatus
LEAGUE_STATUS_REJECTED: ELeagueStatus
LEAGUE_STATUS_CONCLUDED: ELeagueStatus
LEAGUE_STATUS_DELETED: ELeagueStatus
LEAGUE_REGION_UNSET: ELeagueRegion
LEAGUE_REGION_NA: ELeagueRegion
LEAGUE_REGION_SA: ELeagueRegion
LEAGUE_REGION_WEU: ELeagueRegion
LEAGUE_REGION_EEU: ELeagueRegion
LEAGUE_REGION_CHINA: ELeagueRegion
LEAGUE_REGION_SEA: ELeagueRegion
LEAGUE_TIER_UNSET: ELeagueTier
LEAGUE_TIER_AMATEUR: ELeagueTier
LEAGUE_TIER_PROFESSIONAL: ELeagueTier
LEAGUE_TIER_MINOR: ELeagueTier
LEAGUE_TIER_MAJOR: ELeagueTier
LEAGUE_TIER_INTERNATIONAL: ELeagueTier
LEAGUE_TIER_DPC_QUALIFIER: ELeagueTier
LEAGUE_TIER_DPC_LEAGUE_QUALIFIER: ELeagueTier
LEAGUE_TIER_DPC_LEAGUE: ELeagueTier
LEAGUE_TIER_DPC_LEAGUE_FINALS: ELeagueTier
LEAGUE_TIER_CATEGORY_AMATEUR: ELeagueTierCategory
LEAGUE_TIER_CATEGORY_PROFESSIONAL: ELeagueTierCategory
LEAGUE_TIER_CATEGORY_DPC: ELeagueTierCategory
LEAGUE_DIVISION_UNSET: ELeagueDivision
LEAGUE_DIVISION_I: ELeagueDivision
LEAGUE_DIVISION_II: ELeagueDivision
LEAGUE_BROADCAST_UNKNOWN: ELeagueBroadcastProvider
LEAGUE_BROADCAST_STEAM: ELeagueBroadcastProvider
LEAGUE_BROADCAST_TWITCH: ELeagueBroadcastProvider
LEAGUE_BROADCAST_YOUTUBE: ELeagueBroadcastProvider
LEAGUE_BROADCAST_OTHER: ELeagueBroadcastProvider
LEAGUE_PHASE_UNSET: ELeaguePhase
LEAGUE_PHASE_REGIONAL_QUALIFIER: ELeaguePhase
LEAGUE_PHASE_GROUP_STAGE: ELeaguePhase
LEAGUE_PHASE_MAIN_EVENT: ELeaguePhase
LEAGUE_AUDIT_ACTION_INVALID: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_LEAGUE_CREATE: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_LEAGUE_EDIT: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_LEAGUE_DELETE: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_LEAGUE_ADMIN_ADD: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_LEAGUE_ADMIN_REVOKE: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_LEAGUE_ADMIN_PROMOTE: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_LEAGUE_STREAM_ADD: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_LEAGUE_STREAM_REMOVE: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_LEAGUE_IMAGE_UPDATED: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_LEAGUE_MESSAGE_ADDED: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_LEAGUE_SUBMITTED: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_LEAGUE_SET_PRIZE_POOL: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_LEAGUE_ADD_PRIZE_POOL_ITEM: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_LEAGUE_REMOVE_PRIZE_POOL_ITEM: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_LEAGUE_MATCH_START: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_LEAGUE_MATCH_END: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_LEAGUE_ADD_INVITED_TEAM: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_LEAGUE_REMOVE_INVITED_TEAM: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_LEAGUE_STATUS_CHANGED: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_LEAGUE_STREAM_EDIT: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_LEAGUE_TEAM_SWAP: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_NODEGROUP_CREATE: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_NODEGROUP_DESTROY: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_NODEGROUP_ADD_TEAM: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_NODEGROUP_REMOVE_TEAM: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_NODEGROUP_SET_ADVANCING: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_NODEGROUP_EDIT: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_NODEGROUP_POPULATE: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_NODEGROUP_COMPLETED: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_NODEGROUP_SET_SECONDARY_ADVANCING: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_NODEGROUP_SET_TERTIARY_ADVANCING: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_NODE_CREATE: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_NODE_DESTROY: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_NODE_AUTOCREATE: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_NODE_SET_TEAM: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_NODE_SET_SERIES_ID: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_NODE_SET_ADVANCING: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_NODE_SET_TIME: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_NODE_MATCH_COMPLETED: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_NODE_COMPLETED: ELeagueAuditAction
LEAGUE_AUDIT_ACTION_NODE_EDIT: ELeagueAuditAction
DOTA_COMBATLOG_INVALID: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_DAMAGE: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_HEAL: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_MODIFIER_ADD: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_MODIFIER_REMOVE: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_DEATH: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_ABILITY: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_ITEM: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_LOCATION: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_GOLD: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_GAME_STATE: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_XP: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_PURCHASE: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_BUYBACK: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_ABILITY_TRIGGER: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_PLAYERSTATS: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_MULTIKILL: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_KILLSTREAK: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_TEAM_BUILDING_KILL: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_FIRST_BLOOD: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_MODIFIER_STACK_EVENT: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_NEUTRAL_CAMP_STACK: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_PICKUP_RUNE: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_REVEALED_INVISIBLE: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_HERO_SAVED: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_MANA_RESTORED: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_HERO_LEVELUP: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_BOTTLE_HEAL_ALLY: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_ENDGAME_STATS: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_INTERRUPT_CHANNEL: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_ALLIED_GOLD: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_AEGIS_TAKEN: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_MANA_DAMAGE: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_PHYSICAL_DAMAGE_PREVENTED: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_UNIT_SUMMONED: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_ATTACK_EVADE: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_TREE_CUT: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_SUCCESSFUL_SCAN: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_END_KILLSTREAK: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_BLOODSTONE_CHARGE: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_CRITICAL_DAMAGE: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_SPELL_ABSORB: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_UNIT_TELEPORTED: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_KILL_EATER_EVENT: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_NEUTRAL_ITEM_EARNED: DOTA_COMBATLOG_TYPES
DOTA_COMBATLOG_STAT_TRACKER_PLAYER: DOTA_COMBATLOG_TYPES
FAVORITE_TYPE_ALL: EDPCFavoriteType
FAVORITE_TYPE_PLAYER: EDPCFavoriteType
FAVORITE_TYPE_TEAM: EDPCFavoriteType
FAVORITE_TYPE_LEAGUE: EDPCFavoriteType
DPC_PUSH_NOTIFICATION_MATCH_STARTING: EDPCPushNotification
DPC_PUSH_NOTIFICATION_PLAYER_LEFT_TEAM: EDPCPushNotification
DPC_PUSH_NOTIFICATION_PLAYER_JOINED_TEAM: EDPCPushNotification
DPC_PUSH_NOTIFICATION_PLAYER_JOINED_TEAM_AS_COACH: EDPCPushNotification
DPC_PUSH_NOTIFICATION_PLAYER_LEFT_TEAM_AS_COACH: EDPCPushNotification
DPC_PUSH_NOTIFICATION_LEAGUE_RESULT: EDPCPushNotification
DPC_PUSH_NOTIFICATION_PREDICTION_MATCHES_AVAILABLE: EDPCPushNotification
DPC_PUSH_NOTIFICATION_PREDICTION_RESULT: EDPCPushNotification
DPC_PUSH_NOTIFICATION_FANTASY_PLAYER_CLEARED: EDPCPushNotification
DPC_PUSH_NOTIFICATION_FANTASY_DAILY_SUMMARY: EDPCPushNotification
DPC_PUSH_NOTIFICATION_FANTASY_FINAL_RESULTS: EDPCPushNotification
k_eEventActionScoreMode_Add: EEventActionScoreMode
k_eEventActionScoreMode_Min: EEventActionScoreMode
k_EPlayerChallengeHistoryType_Invalid: EPlayerChallengeHistoryType
k_EPlayerChallengeHistoryType_KillEater: EPlayerChallengeHistoryType
k_EPlayerChallengeHistoryType_DotaPlusRelic: EPlayerChallengeHistoryType
k_EPlayerChallengeHistoryType_DotaPlusHeroPlayerChallenge: EPlayerChallengeHistoryType
k_EPlayerChallengeHistoryType_InGameEventChallenge: EPlayerChallengeHistoryType
k_EPlayerChallengeHistoryType_GuildContract: EPlayerChallengeHistoryType
k_EOverwatchReportReason_Unknown: EOverwatchReportReason
k_EOverwatchReportReason_Cheating: EOverwatchReportReason
k_EOverwatchReportReason_Feeding: EOverwatchReportReason
k_EOverwatchReportReason_Griefing: EOverwatchReportReason
k_EOverwatchReportReason_Suspicious: EOverwatchReportReason
k_EOverwatchReportReason_AbilityAbuse: EOverwatchReportReason
k_ECandyShopUpgradeInvalid: ECandyShopUpgrade
k_ECandyShopUpgrade_InventorySize: ECandyShopUpgrade
k_ECandyShopUpgrade_RewardShelf: ECandyShopUpgrade
k_ECandyShopUpgrade_ExtraExchangeRecipe: ECandyShopUpgrade
k_EItemSuggestPreference_None: EItemSuggestPreference
k_EItemSuggestPreference_Liked: EItemSuggestPreference
k_EItemSuggestPreference_Disliked: EItemSuggestPreference
k_TimerAlertType_PowerRune: ETimerAlertType
k_TimerAlertType_BountyRune: ETimerAlertType
k_TimerAlertType_WisdomShrine: ETimerAlertType
k_TimerAlertType_JungleCamps: ETimerAlertType
k_TimerAlertType_LotusPool: ETimerAlertType

class CDOTAClientHardwareSpecs(_message.Message):
    __slots__ = (
        "logical_processors",
        "cpu_cycles_per_second",
        "total_physical_memory",
        "is_64_bit_os",
        "upload_measurement",
        "prefer_not_host",
        "crc",
    )
    LOGICAL_PROCESSORS_FIELD_NUMBER: _ClassVar[int]
    CPU_CYCLES_PER_SECOND_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PHYSICAL_MEMORY_FIELD_NUMBER: _ClassVar[int]
    IS_64_BIT_OS_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_MEASUREMENT_FIELD_NUMBER: _ClassVar[int]
    PREFER_NOT_HOST_FIELD_NUMBER: _ClassVar[int]
    CRC_FIELD_NUMBER: _ClassVar[int]
    logical_processors: int
    cpu_cycles_per_second: int
    total_physical_memory: int
    is_64_bit_os: bool
    upload_measurement: int
    prefer_not_host: bool
    crc: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        logical_processors: int | None = ...,
        cpu_cycles_per_second: int | None = ...,
        total_physical_memory: int | None = ...,
        is_64_bit_os: bool = ...,
        upload_measurement: int | None = ...,
        prefer_not_host: bool = ...,
        crc: _Iterable[int] | None = ...,
    ) -> None: ...

class CDOTASaveGame(_message.Message):
    __slots__ = ("match_id", "save_time", "players", "save_instances")
    class Player(_message.Message):
        __slots__ = ("team", "name", "hero")
        TEAM_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        HERO_FIELD_NUMBER: _ClassVar[int]
        team: DOTA_GC_TEAM
        name: str
        hero: str
        def __init__(
            self,
            team: DOTA_GC_TEAM | str | None = ...,
            name: str | None = ...,
            hero: str | None = ...,
        ) -> None: ...

    class SaveInstance(_message.Message):
        __slots__ = (
            "game_time",
            "team1_score",
            "team2_score",
            "player_positions",
            "save_id",
            "save_time",
        )
        class PlayerPositions(_message.Message):
            __slots__ = ("x", "y")
            X_FIELD_NUMBER: _ClassVar[int]
            Y_FIELD_NUMBER: _ClassVar[int]
            x: float
            y: float
            def __init__(self, x: float | None = ..., y: float | None = ...) -> None: ...

        GAME_TIME_FIELD_NUMBER: _ClassVar[int]
        TEAM1_SCORE_FIELD_NUMBER: _ClassVar[int]
        TEAM2_SCORE_FIELD_NUMBER: _ClassVar[int]
        PLAYER_POSITIONS_FIELD_NUMBER: _ClassVar[int]
        SAVE_ID_FIELD_NUMBER: _ClassVar[int]
        SAVE_TIME_FIELD_NUMBER: _ClassVar[int]
        game_time: int
        team1_score: int
        team2_score: int
        player_positions: _containers.RepeatedCompositeFieldContainer[
            CDOTASaveGame.SaveInstance.PlayerPositions
        ]
        save_id: int
        save_time: int
        def __init__(
            self,
            game_time: int | None = ...,
            team1_score: int | None = ...,
            team2_score: int | None = ...,
            player_positions: _Iterable[CDOTASaveGame.SaveInstance.PlayerPositions | _Mapping]
            | None = ...,
            save_id: int | None = ...,
            save_time: int | None = ...,
        ) -> None: ...

    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    SAVE_TIME_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    SAVE_INSTANCES_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    save_time: int
    players: _containers.RepeatedCompositeFieldContainer[CDOTASaveGame.Player]
    save_instances: _containers.RepeatedCompositeFieldContainer[CDOTASaveGame.SaveInstance]
    def __init__(
        self,
        match_id: int | None = ...,
        save_time: int | None = ...,
        players: _Iterable[CDOTASaveGame.Player | _Mapping] | None = ...,
        save_instances: _Iterable[CDOTASaveGame.SaveInstance | _Mapping] | None = ...,
    ) -> None: ...

class CMsgDOTACombatLogEntry(_message.Message):
    __slots__ = (
        "type",
        "target_name",
        "target_source_name",
        "attacker_name",
        "damage_source_name",
        "inflictor_name",
        "is_attacker_illusion",
        "is_attacker_hero",
        "is_target_illusion",
        "is_target_hero",
        "is_visible_radiant",
        "is_visible_dire",
        "value",
        "health",
        "timestamp",
        "stun_duration",
        "slow_duration",
        "is_ability_toggle_on",
        "is_ability_toggle_off",
        "ability_level",
        "location_x",
        "location_y",
        "gold_reason",
        "timestamp_raw",
        "modifier_duration",
        "xp_reason",
        "last_hits",
        "attacker_team",
        "target_team",
        "obs_wards_placed",
        "assist_player0",
        "assist_player1",
        "assist_player2",
        "assist_player3",
        "stack_count",
        "hidden_modifier",
        "is_target_building",
        "neutral_camp_type",
        "rune_type",
        "assist_players",
        "is_heal_save",
        "is_ultimate_ability",
        "attacker_hero_level",
        "target_hero_level",
        "xpm",
        "gpm",
        "event_location",
        "target_is_self",
        "damage_type",
        "invisibility_modifier",
        "damage_category",
        "networth",
        "building_type",
        "modifier_elapsed_duration",
        "silence_modifier",
        "heal_from_lifesteal",
        "modifier_purged",
        "spell_evaded",
        "motion_controller_modifier",
        "long_range_kill",
        "modifier_purge_ability",
        "modifier_purge_npc",
        "root_modifier",
        "total_unit_death_count",
        "aura_modifier",
        "armor_debuff_modifier",
        "no_physical_damage_modifier",
        "modifier_ability",
        "modifier_hidden",
        "inflictor_is_stolen_ability",
        "kill_eater_event",
        "unit_status_label",
        "spell_generated_attack",
        "at_night_time",
        "attacker_has_scepter",
        "neutral_camp_team",
        "regenerated_health",
        "will_reincarnate",
        "uses_charges",
        "tracked_stat_id",
    )
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TARGET_NAME_FIELD_NUMBER: _ClassVar[int]
    TARGET_SOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    ATTACKER_NAME_FIELD_NUMBER: _ClassVar[int]
    DAMAGE_SOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    INFLICTOR_NAME_FIELD_NUMBER: _ClassVar[int]
    IS_ATTACKER_ILLUSION_FIELD_NUMBER: _ClassVar[int]
    IS_ATTACKER_HERO_FIELD_NUMBER: _ClassVar[int]
    IS_TARGET_ILLUSION_FIELD_NUMBER: _ClassVar[int]
    IS_TARGET_HERO_FIELD_NUMBER: _ClassVar[int]
    IS_VISIBLE_RADIANT_FIELD_NUMBER: _ClassVar[int]
    IS_VISIBLE_DIRE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    HEALTH_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    STUN_DURATION_FIELD_NUMBER: _ClassVar[int]
    SLOW_DURATION_FIELD_NUMBER: _ClassVar[int]
    IS_ABILITY_TOGGLE_ON_FIELD_NUMBER: _ClassVar[int]
    IS_ABILITY_TOGGLE_OFF_FIELD_NUMBER: _ClassVar[int]
    ABILITY_LEVEL_FIELD_NUMBER: _ClassVar[int]
    LOCATION_X_FIELD_NUMBER: _ClassVar[int]
    LOCATION_Y_FIELD_NUMBER: _ClassVar[int]
    GOLD_REASON_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_RAW_FIELD_NUMBER: _ClassVar[int]
    MODIFIER_DURATION_FIELD_NUMBER: _ClassVar[int]
    XP_REASON_FIELD_NUMBER: _ClassVar[int]
    LAST_HITS_FIELD_NUMBER: _ClassVar[int]
    ATTACKER_TEAM_FIELD_NUMBER: _ClassVar[int]
    TARGET_TEAM_FIELD_NUMBER: _ClassVar[int]
    OBS_WARDS_PLACED_FIELD_NUMBER: _ClassVar[int]
    ASSIST_PLAYER0_FIELD_NUMBER: _ClassVar[int]
    ASSIST_PLAYER1_FIELD_NUMBER: _ClassVar[int]
    ASSIST_PLAYER2_FIELD_NUMBER: _ClassVar[int]
    ASSIST_PLAYER3_FIELD_NUMBER: _ClassVar[int]
    STACK_COUNT_FIELD_NUMBER: _ClassVar[int]
    HIDDEN_MODIFIER_FIELD_NUMBER: _ClassVar[int]
    IS_TARGET_BUILDING_FIELD_NUMBER: _ClassVar[int]
    NEUTRAL_CAMP_TYPE_FIELD_NUMBER: _ClassVar[int]
    RUNE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ASSIST_PLAYERS_FIELD_NUMBER: _ClassVar[int]
    IS_HEAL_SAVE_FIELD_NUMBER: _ClassVar[int]
    IS_ULTIMATE_ABILITY_FIELD_NUMBER: _ClassVar[int]
    ATTACKER_HERO_LEVEL_FIELD_NUMBER: _ClassVar[int]
    TARGET_HERO_LEVEL_FIELD_NUMBER: _ClassVar[int]
    XPM_FIELD_NUMBER: _ClassVar[int]
    GPM_FIELD_NUMBER: _ClassVar[int]
    EVENT_LOCATION_FIELD_NUMBER: _ClassVar[int]
    TARGET_IS_SELF_FIELD_NUMBER: _ClassVar[int]
    DAMAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    INVISIBILITY_MODIFIER_FIELD_NUMBER: _ClassVar[int]
    DAMAGE_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    NETWORTH_FIELD_NUMBER: _ClassVar[int]
    BUILDING_TYPE_FIELD_NUMBER: _ClassVar[int]
    MODIFIER_ELAPSED_DURATION_FIELD_NUMBER: _ClassVar[int]
    SILENCE_MODIFIER_FIELD_NUMBER: _ClassVar[int]
    HEAL_FROM_LIFESTEAL_FIELD_NUMBER: _ClassVar[int]
    MODIFIER_PURGED_FIELD_NUMBER: _ClassVar[int]
    SPELL_EVADED_FIELD_NUMBER: _ClassVar[int]
    MOTION_CONTROLLER_MODIFIER_FIELD_NUMBER: _ClassVar[int]
    LONG_RANGE_KILL_FIELD_NUMBER: _ClassVar[int]
    MODIFIER_PURGE_ABILITY_FIELD_NUMBER: _ClassVar[int]
    MODIFIER_PURGE_NPC_FIELD_NUMBER: _ClassVar[int]
    ROOT_MODIFIER_FIELD_NUMBER: _ClassVar[int]
    TOTAL_UNIT_DEATH_COUNT_FIELD_NUMBER: _ClassVar[int]
    AURA_MODIFIER_FIELD_NUMBER: _ClassVar[int]
    ARMOR_DEBUFF_MODIFIER_FIELD_NUMBER: _ClassVar[int]
    NO_PHYSICAL_DAMAGE_MODIFIER_FIELD_NUMBER: _ClassVar[int]
    MODIFIER_ABILITY_FIELD_NUMBER: _ClassVar[int]
    MODIFIER_HIDDEN_FIELD_NUMBER: _ClassVar[int]
    INFLICTOR_IS_STOLEN_ABILITY_FIELD_NUMBER: _ClassVar[int]
    KILL_EATER_EVENT_FIELD_NUMBER: _ClassVar[int]
    UNIT_STATUS_LABEL_FIELD_NUMBER: _ClassVar[int]
    SPELL_GENERATED_ATTACK_FIELD_NUMBER: _ClassVar[int]
    AT_NIGHT_TIME_FIELD_NUMBER: _ClassVar[int]
    ATTACKER_HAS_SCEPTER_FIELD_NUMBER: _ClassVar[int]
    NEUTRAL_CAMP_TEAM_FIELD_NUMBER: _ClassVar[int]
    REGENERATED_HEALTH_FIELD_NUMBER: _ClassVar[int]
    WILL_REINCARNATE_FIELD_NUMBER: _ClassVar[int]
    USES_CHARGES_FIELD_NUMBER: _ClassVar[int]
    TRACKED_STAT_ID_FIELD_NUMBER: _ClassVar[int]
    type: DOTA_COMBATLOG_TYPES
    target_name: int
    target_source_name: int
    attacker_name: int
    damage_source_name: int
    inflictor_name: int
    is_attacker_illusion: bool
    is_attacker_hero: bool
    is_target_illusion: bool
    is_target_hero: bool
    is_visible_radiant: bool
    is_visible_dire: bool
    value: int
    health: int
    timestamp: float
    stun_duration: float
    slow_duration: float
    is_ability_toggle_on: bool
    is_ability_toggle_off: bool
    ability_level: int
    location_x: float
    location_y: float
    gold_reason: int
    timestamp_raw: float
    modifier_duration: float
    xp_reason: int
    last_hits: int
    attacker_team: int
    target_team: int
    obs_wards_placed: int
    assist_player0: int
    assist_player1: int
    assist_player2: int
    assist_player3: int
    stack_count: int
    hidden_modifier: bool
    is_target_building: bool
    neutral_camp_type: int
    rune_type: int
    assist_players: _containers.RepeatedScalarFieldContainer[int]
    is_heal_save: bool
    is_ultimate_ability: bool
    attacker_hero_level: int
    target_hero_level: int
    xpm: int
    gpm: int
    event_location: int
    target_is_self: bool
    damage_type: int
    invisibility_modifier: bool
    damage_category: int
    networth: int
    building_type: int
    modifier_elapsed_duration: float
    silence_modifier: bool
    heal_from_lifesteal: bool
    modifier_purged: bool
    spell_evaded: bool
    motion_controller_modifier: bool
    long_range_kill: bool
    modifier_purge_ability: int
    modifier_purge_npc: int
    root_modifier: bool
    total_unit_death_count: int
    aura_modifier: bool
    armor_debuff_modifier: bool
    no_physical_damage_modifier: bool
    modifier_ability: int
    modifier_hidden: bool
    inflictor_is_stolen_ability: bool
    kill_eater_event: int
    unit_status_label: int
    spell_generated_attack: bool
    at_night_time: bool
    attacker_has_scepter: bool
    neutral_camp_team: int
    regenerated_health: float
    will_reincarnate: bool
    uses_charges: bool
    tracked_stat_id: int
    def __init__(
        self,
        type: DOTA_COMBATLOG_TYPES | str | None = ...,
        target_name: int | None = ...,
        target_source_name: int | None = ...,
        attacker_name: int | None = ...,
        damage_source_name: int | None = ...,
        inflictor_name: int | None = ...,
        is_attacker_illusion: bool = ...,
        is_attacker_hero: bool = ...,
        is_target_illusion: bool = ...,
        is_target_hero: bool = ...,
        is_visible_radiant: bool = ...,
        is_visible_dire: bool = ...,
        value: int | None = ...,
        health: int | None = ...,
        timestamp: float | None = ...,
        stun_duration: float | None = ...,
        slow_duration: float | None = ...,
        is_ability_toggle_on: bool = ...,
        is_ability_toggle_off: bool = ...,
        ability_level: int | None = ...,
        location_x: float | None = ...,
        location_y: float | None = ...,
        gold_reason: int | None = ...,
        timestamp_raw: float | None = ...,
        modifier_duration: float | None = ...,
        xp_reason: int | None = ...,
        last_hits: int | None = ...,
        attacker_team: int | None = ...,
        target_team: int | None = ...,
        obs_wards_placed: int | None = ...,
        assist_player0: int | None = ...,
        assist_player1: int | None = ...,
        assist_player2: int | None = ...,
        assist_player3: int | None = ...,
        stack_count: int | None = ...,
        hidden_modifier: bool = ...,
        is_target_building: bool = ...,
        neutral_camp_type: int | None = ...,
        rune_type: int | None = ...,
        assist_players: _Iterable[int] | None = ...,
        is_heal_save: bool = ...,
        is_ultimate_ability: bool = ...,
        attacker_hero_level: int | None = ...,
        target_hero_level: int | None = ...,
        xpm: int | None = ...,
        gpm: int | None = ...,
        event_location: int | None = ...,
        target_is_self: bool = ...,
        damage_type: int | None = ...,
        invisibility_modifier: bool = ...,
        damage_category: int | None = ...,
        networth: int | None = ...,
        building_type: int | None = ...,
        modifier_elapsed_duration: float | None = ...,
        silence_modifier: bool = ...,
        heal_from_lifesteal: bool = ...,
        modifier_purged: bool = ...,
        spell_evaded: bool = ...,
        motion_controller_modifier: bool = ...,
        long_range_kill: bool = ...,
        modifier_purge_ability: int | None = ...,
        modifier_purge_npc: int | None = ...,
        root_modifier: bool = ...,
        total_unit_death_count: int | None = ...,
        aura_modifier: bool = ...,
        armor_debuff_modifier: bool = ...,
        no_physical_damage_modifier: bool = ...,
        modifier_ability: int | None = ...,
        modifier_hidden: bool = ...,
        inflictor_is_stolen_ability: bool = ...,
        kill_eater_event: int | None = ...,
        unit_status_label: int | None = ...,
        spell_generated_attack: bool = ...,
        at_night_time: bool = ...,
        attacker_has_scepter: bool = ...,
        neutral_camp_team: int | None = ...,
        regenerated_health: float | None = ...,
        will_reincarnate: bool = ...,
        uses_charges: bool = ...,
        tracked_stat_id: int | None = ...,
    ) -> None: ...

class CMsgPendingEventAward(_message.Message):
    __slots__ = (
        "event_id",
        "action_id",
        "num_to_grant",
        "score_mode",
        "audit_action",
        "audit_data",
    )
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_ID_FIELD_NUMBER: _ClassVar[int]
    NUM_TO_GRANT_FIELD_NUMBER: _ClassVar[int]
    SCORE_MODE_FIELD_NUMBER: _ClassVar[int]
    AUDIT_ACTION_FIELD_NUMBER: _ClassVar[int]
    AUDIT_DATA_FIELD_NUMBER: _ClassVar[int]
    event_id: EEvent
    action_id: int
    num_to_grant: int
    score_mode: EEventActionScoreMode
    audit_action: int
    audit_data: int
    def __init__(
        self,
        event_id: EEvent | str | None = ...,
        action_id: int | None = ...,
        num_to_grant: int | None = ...,
        score_mode: EEventActionScoreMode | str | None = ...,
        audit_action: int | None = ...,
        audit_data: int | None = ...,
    ) -> None: ...

class CMsgMonsterHunterMaterialQuantity(_message.Message):
    __slots__ = ("material_counts",)
    class MaterialCountsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: int | None = ..., value: int | None = ...) -> None: ...

    MATERIAL_COUNTS_FIELD_NUMBER: _ClassVar[int]
    material_counts: _containers.RepeatedCompositeFieldContainer[
        CMsgMonsterHunterMaterialQuantity.MaterialCountsEntry
    ]
    def __init__(
        self,
        material_counts: _Iterable[CMsgMonsterHunterMaterialQuantity.MaterialCountsEntry | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgMonsterHunterInvestigation(_message.Message):
    __slots__ = ("hero_id", "persona_id", "match_rewards", "hunt_rewards", "success_state")
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    PERSONA_ID_FIELD_NUMBER: _ClassVar[int]
    MATCH_REWARDS_FIELD_NUMBER: _ClassVar[int]
    HUNT_REWARDS_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_STATE_FIELD_NUMBER: _ClassVar[int]
    hero_id: int
    persona_id: int
    match_rewards: CMsgMonsterHunterMaterialQuantity
    hunt_rewards: CMsgMonsterHunterMaterialQuantity
    success_state: bool
    def __init__(
        self,
        hero_id: int | None = ...,
        persona_id: int | None = ...,
        match_rewards: CMsgMonsterHunterMaterialQuantity | _Mapping | None = ...,
        hunt_rewards: CMsgMonsterHunterMaterialQuantity | _Mapping | None = ...,
        success_state: bool = ...,
    ) -> None: ...

class CMsgMonsterHunterInvestigationGameState(_message.Message):
    __slots__ = ("selected_investigation", "hunted_by")
    class HuntedBy(_message.Message):
        __slots__ = ("hero_id", "persona_id", "hunt_rewards", "success_state")
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        PERSONA_ID_FIELD_NUMBER: _ClassVar[int]
        HUNT_REWARDS_FIELD_NUMBER: _ClassVar[int]
        SUCCESS_STATE_FIELD_NUMBER: _ClassVar[int]
        hero_id: int
        persona_id: int
        hunt_rewards: CMsgMonsterHunterMaterialQuantity
        success_state: bool
        def __init__(
            self,
            hero_id: int | None = ...,
            persona_id: int | None = ...,
            hunt_rewards: CMsgMonsterHunterMaterialQuantity | _Mapping | None = ...,
            success_state: bool = ...,
        ) -> None: ...

    SELECTED_INVESTIGATION_FIELD_NUMBER: _ClassVar[int]
    HUNTED_BY_FIELD_NUMBER: _ClassVar[int]
    selected_investigation: CMsgMonsterHunterInvestigation
    hunted_by: _containers.RepeatedCompositeFieldContainer[
        CMsgMonsterHunterInvestigationGameState.HuntedBy
    ]
    def __init__(
        self,
        selected_investigation: CMsgMonsterHunterInvestigation | _Mapping | None = ...,
        hunted_by: _Iterable[CMsgMonsterHunterInvestigationGameState.HuntedBy | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgMonsterHunterCodexUpdateData(_message.Message):
    __slots__ = ("player_hero", "allies", "enemies", "player_kills")
    class KillInfo(_message.Message):
        __slots__ = ("hero_id", "kill_count")
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        KILL_COUNT_FIELD_NUMBER: _ClassVar[int]
        hero_id: int
        kill_count: int
        def __init__(self, hero_id: int | None = ..., kill_count: int | None = ...) -> None: ...

    PLAYER_HERO_FIELD_NUMBER: _ClassVar[int]
    ALLIES_FIELD_NUMBER: _ClassVar[int]
    ENEMIES_FIELD_NUMBER: _ClassVar[int]
    PLAYER_KILLS_FIELD_NUMBER: _ClassVar[int]
    player_hero: int
    allies: _containers.RepeatedScalarFieldContainer[int]
    enemies: _containers.RepeatedScalarFieldContainer[int]
    player_kills: _containers.RepeatedCompositeFieldContainer[
        CMsgMonsterHunterCodexUpdateData.KillInfo
    ]
    def __init__(
        self,
        player_hero: int | None = ...,
        allies: _Iterable[int] | None = ...,
        enemies: _Iterable[int] | None = ...,
        player_kills: _Iterable[CMsgMonsterHunterCodexUpdateData.KillInfo | _Mapping] | None = ...,
    ) -> None: ...
