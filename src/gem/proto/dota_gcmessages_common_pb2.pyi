from . import steammessages_pb2 as _steammessages_pb2
from . import gcsdk_gcmessages_pb2 as _gcsdk_gcmessages_pb2
from . import dota_shared_enums_pb2 as _dota_shared_enums_pb2
from . import networkbasetypes_pb2 as _networkbasetypes_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ESpecialPingValue(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_ESpecialPingValue_NoData: _ClassVar[ESpecialPingValue]
    k_ESpecialPingValue_Failed: _ClassVar[ESpecialPingValue]

class EDOTAGCSessionNeed(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EDOTAGCSessionNeed_Unknown: _ClassVar[EDOTAGCSessionNeed]
    k_EDOTAGCSessionNeed_UserNoSessionNeeded: _ClassVar[EDOTAGCSessionNeed]
    k_EDOTAGCSessionNeed_UserInOnlineGame: _ClassVar[EDOTAGCSessionNeed]
    k_EDOTAGCSessionNeed_UserInLocalGame: _ClassVar[EDOTAGCSessionNeed]
    k_EDOTAGCSessionNeed_UserInUIWasConnected: _ClassVar[EDOTAGCSessionNeed]
    k_EDOTAGCSessionNeed_UserInUINeverConnected: _ClassVar[EDOTAGCSessionNeed]
    k_EDOTAGCSessionNeed_UserTutorials: _ClassVar[EDOTAGCSessionNeed]
    k_EDOTAGCSessionNeed_UserInUIWasConnectedIdle: _ClassVar[EDOTAGCSessionNeed]
    k_EDOTAGCSessionNeed_UserInUINeverConnectedIdle: _ClassVar[EDOTAGCSessionNeed]
    k_EDOTAGCSessionNeed_GameServerOnline: _ClassVar[EDOTAGCSessionNeed]
    k_EDOTAGCSessionNeed_GameServerLocal: _ClassVar[EDOTAGCSessionNeed]
    k_EDOTAGCSessionNeed_GameServerIdle: _ClassVar[EDOTAGCSessionNeed]
    k_EDOTAGCSessionNeed_GameServerRelay: _ClassVar[EDOTAGCSessionNeed]
    k_EDOTAGCSessionNeed_GameServerLocalUpload: _ClassVar[EDOTAGCSessionNeed]

class EDOTAMatchPlayerTimeCustomStat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EDOTA_MatchPlayerTimeCustomStat_HPRegenUnderT1Towers: _ClassVar[EDOTAMatchPlayerTimeCustomStat]
    k_EDOTA_MatchPlayerTimeCustomStat_MagicDamageReducedWithNewFormula_Absolute: _ClassVar[EDOTAMatchPlayerTimeCustomStat]
    k_EDOTA_MatchPlayerTimeCustomStat_MagicDamageReducedWithNewFormula_PercentOfTotalHP: _ClassVar[EDOTAMatchPlayerTimeCustomStat]

class DOTA_TournamentEvents(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TE_FIRST_BLOOD: _ClassVar[DOTA_TournamentEvents]
    TE_GAME_END: _ClassVar[DOTA_TournamentEvents]
    TE_MULTI_KILL: _ClassVar[DOTA_TournamentEvents]
    TE_HERO_DENY: _ClassVar[DOTA_TournamentEvents]
    TE_AEGIS_DENY: _ClassVar[DOTA_TournamentEvents]
    TE_AEGIS_STOLEN: _ClassVar[DOTA_TournamentEvents]
    TE_GODLIKE: _ClassVar[DOTA_TournamentEvents]
    TE_COURIER_KILL: _ClassVar[DOTA_TournamentEvents]
    TE_ECHOSLAM: _ClassVar[DOTA_TournamentEvents]
    TE_RAPIER: _ClassVar[DOTA_TournamentEvents]
    TE_EARLY_ROSHAN: _ClassVar[DOTA_TournamentEvents]
    TE_BLACK_HOLE: _ClassVar[DOTA_TournamentEvents]

class EBroadcastTimelineEvent(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EBroadcastTimelineEvent_MatchStarted: _ClassVar[EBroadcastTimelineEvent]
    EBroadcastTimelineEvent_GameStateChanged: _ClassVar[EBroadcastTimelineEvent]
    EBroadcastTimelineEvent_TowerDeath: _ClassVar[EBroadcastTimelineEvent]
    EBroadcastTimelineEvent_BarracksDeath: _ClassVar[EBroadcastTimelineEvent]
    EBroadcastTimelineEvent_AncientDeath: _ClassVar[EBroadcastTimelineEvent]
    EBroadcastTimelineEvent_RoshanDeath: _ClassVar[EBroadcastTimelineEvent]
    EBroadcastTimelineEvent_HeroDeath: _ClassVar[EBroadcastTimelineEvent]
    EBroadcastTimelineEvent_TeamFight: _ClassVar[EBroadcastTimelineEvent]
    EBroadcastTimelineEvent_FirstBlood: _ClassVar[EBroadcastTimelineEvent]

class ECustomGameWhitelistState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CUSTOM_GAME_WHITELIST_STATE_UNKNOWN: _ClassVar[ECustomGameWhitelistState]
    CUSTOM_GAME_WHITELIST_STATE_APPROVED: _ClassVar[ECustomGameWhitelistState]
    CUSTOM_GAME_WHITELIST_STATE_REJECTED: _ClassVar[ECustomGameWhitelistState]

class EDOTATriviaQuestionCategory(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EDOTATriviaQuestionCategory_AbilityIcon: _ClassVar[EDOTATriviaQuestionCategory]
    k_EDOTATriviaQuestionCategory_AbilityCooldown: _ClassVar[EDOTATriviaQuestionCategory]
    k_EDOTATriviaQuestionCategory_HeroAttributes: _ClassVar[EDOTATriviaQuestionCategory]
    k_EDOTATriviaQuestionCategory_HeroMovementSpeed: _ClassVar[EDOTATriviaQuestionCategory]
    k_EDOTATriviaQuestionCategory_TalentTree: _ClassVar[EDOTATriviaQuestionCategory]
    k_EDOTATriviaQuestionCategory_HeroStats: _ClassVar[EDOTATriviaQuestionCategory]
    k_EDOTATriviaQuestionCategory_ItemPrice: _ClassVar[EDOTATriviaQuestionCategory]
    k_EDOTATriviaQuestionCategory_AbilitySound: _ClassVar[EDOTATriviaQuestionCategory]
    k_EDOTATriviaQuestionCategory_InvokerSpells: _ClassVar[EDOTATriviaQuestionCategory]
    k_EDOTATriviaQuestionCategory_AbilityManaCost: _ClassVar[EDOTATriviaQuestionCategory]
    k_EDOTATriviaQuestionCategory_HeroAttackSound: _ClassVar[EDOTATriviaQuestionCategory]
    k_EDOTATriviaQuestionCategory_AbilityName: _ClassVar[EDOTATriviaQuestionCategory]
    k_EDOTATriviaQuestionCategory_ItemComponents: _ClassVar[EDOTATriviaQuestionCategory]
    k_EDOTATriviaQuestionCategory_ItemLore: _ClassVar[EDOTATriviaQuestionCategory]
    k_EDOTATriviaQuestionCategory_ItemPassives: _ClassVar[EDOTATriviaQuestionCategory]
    k_EDOTATriviaQuestionCategory_STATIC_QUESTIONS_END: _ClassVar[EDOTATriviaQuestionCategory]
    k_EDOTATriviaQuestionCategory_DYNAMIC_QUESTIONS_START: _ClassVar[EDOTATriviaQuestionCategory]
    k_EDOTATriviaQuestionCategory_Dynamic_ItemBuild: _ClassVar[EDOTATriviaQuestionCategory]

class EOverwatchConviction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EOverwatchConviction_None: _ClassVar[EOverwatchConviction]
    k_EOverwatchConviction_NotGuilty: _ClassVar[EOverwatchConviction]
    k_EOverwatchConviction_GuiltUnclear: _ClassVar[EOverwatchConviction]
    k_EOverwatchConviction_Guilty: _ClassVar[EOverwatchConviction]

class EHeroRelicRarity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HERO_RELIC_RARITY_INVALID: _ClassVar[EHeroRelicRarity]
    HERO_RELIC_RARITY_COMMON: _ClassVar[EHeroRelicRarity]
    HERO_RELIC_RARITY_RARE: _ClassVar[EHeroRelicRarity]

class EStickerbookAuditAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STICKERBOOK_AUDIT_CREATE_PAGE: _ClassVar[EStickerbookAuditAction]
    STICKERBOOK_AUDIT_DELETE_PAGE: _ClassVar[EStickerbookAuditAction]
    STICKERBOOK_AUDIT_STICK_STICKERS: _ClassVar[EStickerbookAuditAction]
    STICKERBOOK_AUDIT_REPLACE_STICKERS: _ClassVar[EStickerbookAuditAction]
    STICKERBOOK_AUDIT_HERO_STICKER: _ClassVar[EStickerbookAuditAction]

class EStickerbookPageType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STICKER_PAGE_GENERIC: _ClassVar[EStickerbookPageType]
    STICKER_PAGE_TEAM: _ClassVar[EStickerbookPageType]
    STICKER_PAGE_TALENT: _ClassVar[EStickerbookPageType]

class ENewBloomGiftingResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    kENewBloomGifting_Success: _ClassVar[ENewBloomGiftingResponse]
    kENewBloomGifting_UnknownFailure: _ClassVar[ENewBloomGiftingResponse]
    kENewBloomGifting_MalformedRequest: _ClassVar[ENewBloomGiftingResponse]
    kENewBloomGifting_FeatureDisabled: _ClassVar[ENewBloomGiftingResponse]
    kENewBloomGifting_ItemNotFound: _ClassVar[ENewBloomGiftingResponse]
    kENewBloomGifting_PlayerNotAllowedToGiveGifts: _ClassVar[ENewBloomGiftingResponse]
    kENewBloomGifting_TargetNotAllowedToReceiveGifts: _ClassVar[ENewBloomGiftingResponse]
    kENewBloomGifting_ServerNotAuthorized: _ClassVar[ENewBloomGiftingResponse]
    kENewBloomGifting_PlayerNotInLobby: _ClassVar[ENewBloomGiftingResponse]
    kENewBloomGifting_TargetNotInLobby: _ClassVar[ENewBloomGiftingResponse]
    kENewBloomGifting_LobbyNotEligible: _ClassVar[ENewBloomGiftingResponse]
    kENewBloomGifting_TargetNotFriend: _ClassVar[ENewBloomGiftingResponse]
    kENewBloomGifting_TargetFriendDurationTooShort: _ClassVar[ENewBloomGiftingResponse]
k_ESpecialPingValue_NoData: ESpecialPingValue
k_ESpecialPingValue_Failed: ESpecialPingValue
k_EDOTAGCSessionNeed_Unknown: EDOTAGCSessionNeed
k_EDOTAGCSessionNeed_UserNoSessionNeeded: EDOTAGCSessionNeed
k_EDOTAGCSessionNeed_UserInOnlineGame: EDOTAGCSessionNeed
k_EDOTAGCSessionNeed_UserInLocalGame: EDOTAGCSessionNeed
k_EDOTAGCSessionNeed_UserInUIWasConnected: EDOTAGCSessionNeed
k_EDOTAGCSessionNeed_UserInUINeverConnected: EDOTAGCSessionNeed
k_EDOTAGCSessionNeed_UserTutorials: EDOTAGCSessionNeed
k_EDOTAGCSessionNeed_UserInUIWasConnectedIdle: EDOTAGCSessionNeed
k_EDOTAGCSessionNeed_UserInUINeverConnectedIdle: EDOTAGCSessionNeed
k_EDOTAGCSessionNeed_GameServerOnline: EDOTAGCSessionNeed
k_EDOTAGCSessionNeed_GameServerLocal: EDOTAGCSessionNeed
k_EDOTAGCSessionNeed_GameServerIdle: EDOTAGCSessionNeed
k_EDOTAGCSessionNeed_GameServerRelay: EDOTAGCSessionNeed
k_EDOTAGCSessionNeed_GameServerLocalUpload: EDOTAGCSessionNeed
k_EDOTA_MatchPlayerTimeCustomStat_HPRegenUnderT1Towers: EDOTAMatchPlayerTimeCustomStat
k_EDOTA_MatchPlayerTimeCustomStat_MagicDamageReducedWithNewFormula_Absolute: EDOTAMatchPlayerTimeCustomStat
k_EDOTA_MatchPlayerTimeCustomStat_MagicDamageReducedWithNewFormula_PercentOfTotalHP: EDOTAMatchPlayerTimeCustomStat
TE_FIRST_BLOOD: DOTA_TournamentEvents
TE_GAME_END: DOTA_TournamentEvents
TE_MULTI_KILL: DOTA_TournamentEvents
TE_HERO_DENY: DOTA_TournamentEvents
TE_AEGIS_DENY: DOTA_TournamentEvents
TE_AEGIS_STOLEN: DOTA_TournamentEvents
TE_GODLIKE: DOTA_TournamentEvents
TE_COURIER_KILL: DOTA_TournamentEvents
TE_ECHOSLAM: DOTA_TournamentEvents
TE_RAPIER: DOTA_TournamentEvents
TE_EARLY_ROSHAN: DOTA_TournamentEvents
TE_BLACK_HOLE: DOTA_TournamentEvents
EBroadcastTimelineEvent_MatchStarted: EBroadcastTimelineEvent
EBroadcastTimelineEvent_GameStateChanged: EBroadcastTimelineEvent
EBroadcastTimelineEvent_TowerDeath: EBroadcastTimelineEvent
EBroadcastTimelineEvent_BarracksDeath: EBroadcastTimelineEvent
EBroadcastTimelineEvent_AncientDeath: EBroadcastTimelineEvent
EBroadcastTimelineEvent_RoshanDeath: EBroadcastTimelineEvent
EBroadcastTimelineEvent_HeroDeath: EBroadcastTimelineEvent
EBroadcastTimelineEvent_TeamFight: EBroadcastTimelineEvent
EBroadcastTimelineEvent_FirstBlood: EBroadcastTimelineEvent
CUSTOM_GAME_WHITELIST_STATE_UNKNOWN: ECustomGameWhitelistState
CUSTOM_GAME_WHITELIST_STATE_APPROVED: ECustomGameWhitelistState
CUSTOM_GAME_WHITELIST_STATE_REJECTED: ECustomGameWhitelistState
k_EDOTATriviaQuestionCategory_AbilityIcon: EDOTATriviaQuestionCategory
k_EDOTATriviaQuestionCategory_AbilityCooldown: EDOTATriviaQuestionCategory
k_EDOTATriviaQuestionCategory_HeroAttributes: EDOTATriviaQuestionCategory
k_EDOTATriviaQuestionCategory_HeroMovementSpeed: EDOTATriviaQuestionCategory
k_EDOTATriviaQuestionCategory_TalentTree: EDOTATriviaQuestionCategory
k_EDOTATriviaQuestionCategory_HeroStats: EDOTATriviaQuestionCategory
k_EDOTATriviaQuestionCategory_ItemPrice: EDOTATriviaQuestionCategory
k_EDOTATriviaQuestionCategory_AbilitySound: EDOTATriviaQuestionCategory
k_EDOTATriviaQuestionCategory_InvokerSpells: EDOTATriviaQuestionCategory
k_EDOTATriviaQuestionCategory_AbilityManaCost: EDOTATriviaQuestionCategory
k_EDOTATriviaQuestionCategory_HeroAttackSound: EDOTATriviaQuestionCategory
k_EDOTATriviaQuestionCategory_AbilityName: EDOTATriviaQuestionCategory
k_EDOTATriviaQuestionCategory_ItemComponents: EDOTATriviaQuestionCategory
k_EDOTATriviaQuestionCategory_ItemLore: EDOTATriviaQuestionCategory
k_EDOTATriviaQuestionCategory_ItemPassives: EDOTATriviaQuestionCategory
k_EDOTATriviaQuestionCategory_STATIC_QUESTIONS_END: EDOTATriviaQuestionCategory
k_EDOTATriviaQuestionCategory_DYNAMIC_QUESTIONS_START: EDOTATriviaQuestionCategory
k_EDOTATriviaQuestionCategory_Dynamic_ItemBuild: EDOTATriviaQuestionCategory
k_EOverwatchConviction_None: EOverwatchConviction
k_EOverwatchConviction_NotGuilty: EOverwatchConviction
k_EOverwatchConviction_GuiltUnclear: EOverwatchConviction
k_EOverwatchConviction_Guilty: EOverwatchConviction
HERO_RELIC_RARITY_INVALID: EHeroRelicRarity
HERO_RELIC_RARITY_COMMON: EHeroRelicRarity
HERO_RELIC_RARITY_RARE: EHeroRelicRarity
STICKERBOOK_AUDIT_CREATE_PAGE: EStickerbookAuditAction
STICKERBOOK_AUDIT_DELETE_PAGE: EStickerbookAuditAction
STICKERBOOK_AUDIT_STICK_STICKERS: EStickerbookAuditAction
STICKERBOOK_AUDIT_REPLACE_STICKERS: EStickerbookAuditAction
STICKERBOOK_AUDIT_HERO_STICKER: EStickerbookAuditAction
STICKER_PAGE_GENERIC: EStickerbookPageType
STICKER_PAGE_TEAM: EStickerbookPageType
STICKER_PAGE_TALENT: EStickerbookPageType
kENewBloomGifting_Success: ENewBloomGiftingResponse
kENewBloomGifting_UnknownFailure: ENewBloomGiftingResponse
kENewBloomGifting_MalformedRequest: ENewBloomGiftingResponse
kENewBloomGifting_FeatureDisabled: ENewBloomGiftingResponse
kENewBloomGifting_ItemNotFound: ENewBloomGiftingResponse
kENewBloomGifting_PlayerNotAllowedToGiveGifts: ENewBloomGiftingResponse
kENewBloomGifting_TargetNotAllowedToReceiveGifts: ENewBloomGiftingResponse
kENewBloomGifting_ServerNotAuthorized: ENewBloomGiftingResponse
kENewBloomGifting_PlayerNotInLobby: ENewBloomGiftingResponse
kENewBloomGifting_TargetNotInLobby: ENewBloomGiftingResponse
kENewBloomGifting_LobbyNotEligible: ENewBloomGiftingResponse
kENewBloomGifting_TargetNotFriend: ENewBloomGiftingResponse
kENewBloomGifting_TargetFriendDurationTooShort: ENewBloomGiftingResponse

class CSODOTAGameAccountClient(_message.Message):
    __slots__ = ("account_id", "wins", "losses", "xp", "level", "initial_skill", "leaver_count", "secondary_leaver_count", "low_priority_until_date", "prevent_text_chat_until_date", "prevent_voice_until_date", "prevent_public_text_chat_until_date", "prevent_new_player_chat_until_date", "last_abandoned_game_date", "last_secondary_abandoned_game_date", "leaver_penalty_count", "completed_game_streak", "account_disabled_until_date", "account_disabled_count", "match_disabled_until_date", "match_disabled_count", "shutdownlawterminatetimestamp", "low_priority_games_remaining", "recruitment_level", "has_new_notifications", "is_league_admin", "casual_games_played", "solo_competitive_games_played", "party_competitive_games_played", "casual_1v1_games_played", "curr_all_hero_challenge_id", "play_time_points", "account_flags", "play_time_level", "player_behavior_seq_num_last_report", "player_behavior_score_last_report", "player_behavior_report_old_data", "tourney_skill_level", "tourney_recent_participation_date", "anchored_phone_number_id", "ranked_matchmaking_ban_until_date", "recent_game_time_1", "recent_game_time_2", "recent_game_time_3", "favorite_team_packed", "recent_report_time", "custom_game_disabled_until_date", "recent_win_time_1", "recent_win_time_2", "recent_win_time_3", "coach_rating", "queue_points", "role_handicaps", "event_mode_recent_time", "mmr_recalibration_time", "banned_hero_ids")
    class RoleHandicap(_message.Message):
        __slots__ = ("role", "handicap")
        ROLE_FIELD_NUMBER: _ClassVar[int]
        HANDICAP_FIELD_NUMBER: _ClassVar[int]
        role: int
        handicap: float
        def __init__(self, role: _Optional[int] = ..., handicap: _Optional[float] = ...) -> None: ...
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    WINS_FIELD_NUMBER: _ClassVar[int]
    LOSSES_FIELD_NUMBER: _ClassVar[int]
    XP_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    INITIAL_SKILL_FIELD_NUMBER: _ClassVar[int]
    LEAVER_COUNT_FIELD_NUMBER: _ClassVar[int]
    SECONDARY_LEAVER_COUNT_FIELD_NUMBER: _ClassVar[int]
    LOW_PRIORITY_UNTIL_DATE_FIELD_NUMBER: _ClassVar[int]
    PREVENT_TEXT_CHAT_UNTIL_DATE_FIELD_NUMBER: _ClassVar[int]
    PREVENT_VOICE_UNTIL_DATE_FIELD_NUMBER: _ClassVar[int]
    PREVENT_PUBLIC_TEXT_CHAT_UNTIL_DATE_FIELD_NUMBER: _ClassVar[int]
    PREVENT_NEW_PLAYER_CHAT_UNTIL_DATE_FIELD_NUMBER: _ClassVar[int]
    LAST_ABANDONED_GAME_DATE_FIELD_NUMBER: _ClassVar[int]
    LAST_SECONDARY_ABANDONED_GAME_DATE_FIELD_NUMBER: _ClassVar[int]
    LEAVER_PENALTY_COUNT_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_GAME_STREAK_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_DISABLED_UNTIL_DATE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_DISABLED_COUNT_FIELD_NUMBER: _ClassVar[int]
    MATCH_DISABLED_UNTIL_DATE_FIELD_NUMBER: _ClassVar[int]
    MATCH_DISABLED_COUNT_FIELD_NUMBER: _ClassVar[int]
    SHUTDOWNLAWTERMINATETIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LOW_PRIORITY_GAMES_REMAINING_FIELD_NUMBER: _ClassVar[int]
    RECRUITMENT_LEVEL_FIELD_NUMBER: _ClassVar[int]
    HAS_NEW_NOTIFICATIONS_FIELD_NUMBER: _ClassVar[int]
    IS_LEAGUE_ADMIN_FIELD_NUMBER: _ClassVar[int]
    CASUAL_GAMES_PLAYED_FIELD_NUMBER: _ClassVar[int]
    SOLO_COMPETITIVE_GAMES_PLAYED_FIELD_NUMBER: _ClassVar[int]
    PARTY_COMPETITIVE_GAMES_PLAYED_FIELD_NUMBER: _ClassVar[int]
    CASUAL_1V1_GAMES_PLAYED_FIELD_NUMBER: _ClassVar[int]
    CURR_ALL_HERO_CHALLENGE_ID_FIELD_NUMBER: _ClassVar[int]
    PLAY_TIME_POINTS_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_FLAGS_FIELD_NUMBER: _ClassVar[int]
    PLAY_TIME_LEVEL_FIELD_NUMBER: _ClassVar[int]
    PLAYER_BEHAVIOR_SEQ_NUM_LAST_REPORT_FIELD_NUMBER: _ClassVar[int]
    PLAYER_BEHAVIOR_SCORE_LAST_REPORT_FIELD_NUMBER: _ClassVar[int]
    PLAYER_BEHAVIOR_REPORT_OLD_DATA_FIELD_NUMBER: _ClassVar[int]
    TOURNEY_SKILL_LEVEL_FIELD_NUMBER: _ClassVar[int]
    TOURNEY_RECENT_PARTICIPATION_DATE_FIELD_NUMBER: _ClassVar[int]
    ANCHORED_PHONE_NUMBER_ID_FIELD_NUMBER: _ClassVar[int]
    RANKED_MATCHMAKING_BAN_UNTIL_DATE_FIELD_NUMBER: _ClassVar[int]
    RECENT_GAME_TIME_1_FIELD_NUMBER: _ClassVar[int]
    RECENT_GAME_TIME_2_FIELD_NUMBER: _ClassVar[int]
    RECENT_GAME_TIME_3_FIELD_NUMBER: _ClassVar[int]
    FAVORITE_TEAM_PACKED_FIELD_NUMBER: _ClassVar[int]
    RECENT_REPORT_TIME_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_DISABLED_UNTIL_DATE_FIELD_NUMBER: _ClassVar[int]
    RECENT_WIN_TIME_1_FIELD_NUMBER: _ClassVar[int]
    RECENT_WIN_TIME_2_FIELD_NUMBER: _ClassVar[int]
    RECENT_WIN_TIME_3_FIELD_NUMBER: _ClassVar[int]
    COACH_RATING_FIELD_NUMBER: _ClassVar[int]
    QUEUE_POINTS_FIELD_NUMBER: _ClassVar[int]
    ROLE_HANDICAPS_FIELD_NUMBER: _ClassVar[int]
    EVENT_MODE_RECENT_TIME_FIELD_NUMBER: _ClassVar[int]
    MMR_RECALIBRATION_TIME_FIELD_NUMBER: _ClassVar[int]
    BANNED_HERO_IDS_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    wins: int
    losses: int
    xp: int
    level: int
    initial_skill: int
    leaver_count: int
    secondary_leaver_count: int
    low_priority_until_date: int
    prevent_text_chat_until_date: int
    prevent_voice_until_date: int
    prevent_public_text_chat_until_date: int
    prevent_new_player_chat_until_date: int
    last_abandoned_game_date: int
    last_secondary_abandoned_game_date: int
    leaver_penalty_count: int
    completed_game_streak: int
    account_disabled_until_date: int
    account_disabled_count: int
    match_disabled_until_date: int
    match_disabled_count: int
    shutdownlawterminatetimestamp: int
    low_priority_games_remaining: int
    recruitment_level: int
    has_new_notifications: bool
    is_league_admin: bool
    casual_games_played: int
    solo_competitive_games_played: int
    party_competitive_games_played: int
    casual_1v1_games_played: int
    curr_all_hero_challenge_id: int
    play_time_points: int
    account_flags: int
    play_time_level: int
    player_behavior_seq_num_last_report: int
    player_behavior_score_last_report: int
    player_behavior_report_old_data: bool
    tourney_skill_level: int
    tourney_recent_participation_date: int
    anchored_phone_number_id: int
    ranked_matchmaking_ban_until_date: int
    recent_game_time_1: int
    recent_game_time_2: int
    recent_game_time_3: int
    favorite_team_packed: int
    recent_report_time: int
    custom_game_disabled_until_date: int
    recent_win_time_1: int
    recent_win_time_2: int
    recent_win_time_3: int
    coach_rating: int
    queue_points: int
    role_handicaps: _containers.RepeatedCompositeFieldContainer[CSODOTAGameAccountClient.RoleHandicap]
    event_mode_recent_time: int
    mmr_recalibration_time: int
    banned_hero_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, account_id: _Optional[int] = ..., wins: _Optional[int] = ..., losses: _Optional[int] = ..., xp: _Optional[int] = ..., level: _Optional[int] = ..., initial_skill: _Optional[int] = ..., leaver_count: _Optional[int] = ..., secondary_leaver_count: _Optional[int] = ..., low_priority_until_date: _Optional[int] = ..., prevent_text_chat_until_date: _Optional[int] = ..., prevent_voice_until_date: _Optional[int] = ..., prevent_public_text_chat_until_date: _Optional[int] = ..., prevent_new_player_chat_until_date: _Optional[int] = ..., last_abandoned_game_date: _Optional[int] = ..., last_secondary_abandoned_game_date: _Optional[int] = ..., leaver_penalty_count: _Optional[int] = ..., completed_game_streak: _Optional[int] = ..., account_disabled_until_date: _Optional[int] = ..., account_disabled_count: _Optional[int] = ..., match_disabled_until_date: _Optional[int] = ..., match_disabled_count: _Optional[int] = ..., shutdownlawterminatetimestamp: _Optional[int] = ..., low_priority_games_remaining: _Optional[int] = ..., recruitment_level: _Optional[int] = ..., has_new_notifications: bool = ..., is_league_admin: bool = ..., casual_games_played: _Optional[int] = ..., solo_competitive_games_played: _Optional[int] = ..., party_competitive_games_played: _Optional[int] = ..., casual_1v1_games_played: _Optional[int] = ..., curr_all_hero_challenge_id: _Optional[int] = ..., play_time_points: _Optional[int] = ..., account_flags: _Optional[int] = ..., play_time_level: _Optional[int] = ..., player_behavior_seq_num_last_report: _Optional[int] = ..., player_behavior_score_last_report: _Optional[int] = ..., player_behavior_report_old_data: bool = ..., tourney_skill_level: _Optional[int] = ..., tourney_recent_participation_date: _Optional[int] = ..., anchored_phone_number_id: _Optional[int] = ..., ranked_matchmaking_ban_until_date: _Optional[int] = ..., recent_game_time_1: _Optional[int] = ..., recent_game_time_2: _Optional[int] = ..., recent_game_time_3: _Optional[int] = ..., favorite_team_packed: _Optional[int] = ..., recent_report_time: _Optional[int] = ..., custom_game_disabled_until_date: _Optional[int] = ..., recent_win_time_1: _Optional[int] = ..., recent_win_time_2: _Optional[int] = ..., recent_win_time_3: _Optional[int] = ..., coach_rating: _Optional[int] = ..., queue_points: _Optional[int] = ..., role_handicaps: _Optional[_Iterable[_Union[CSODOTAGameAccountClient.RoleHandicap, _Mapping]]] = ..., event_mode_recent_time: _Optional[int] = ..., mmr_recalibration_time: _Optional[int] = ..., banned_hero_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class CSODOTAGameAccountPlus(_message.Message):
    __slots__ = ("account_id", "original_start_date", "plus_flags", "plus_status", "prepaid_time_start", "prepaid_time_balance", "next_payment_date", "steam_agreement_id")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_START_DATE_FIELD_NUMBER: _ClassVar[int]
    PLUS_FLAGS_FIELD_NUMBER: _ClassVar[int]
    PLUS_STATUS_FIELD_NUMBER: _ClassVar[int]
    PREPAID_TIME_START_FIELD_NUMBER: _ClassVar[int]
    PREPAID_TIME_BALANCE_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAYMENT_DATE_FIELD_NUMBER: _ClassVar[int]
    STEAM_AGREEMENT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    original_start_date: int
    plus_flags: int
    plus_status: int
    prepaid_time_start: int
    prepaid_time_balance: int
    next_payment_date: int
    steam_agreement_id: int
    def __init__(self, account_id: _Optional[int] = ..., original_start_date: _Optional[int] = ..., plus_flags: _Optional[int] = ..., plus_status: _Optional[int] = ..., prepaid_time_start: _Optional[int] = ..., prepaid_time_balance: _Optional[int] = ..., next_payment_date: _Optional[int] = ..., steam_agreement_id: _Optional[int] = ...) -> None: ...

class CSODOTAChatWheel(_message.Message):
    __slots__ = ("message_id",)
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    message_id: int
    def __init__(self, message_id: _Optional[int] = ...) -> None: ...

class CMsgLobbyFeaturedGamemodeProgress(_message.Message):
    __slots__ = ("accounts",)
    class AccountProgress(_message.Message):
        __slots__ = ("account_id", "current_value", "max_value")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        CURRENT_VALUE_FIELD_NUMBER: _ClassVar[int]
        MAX_VALUE_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        current_value: int
        max_value: int
        def __init__(self, account_id: _Optional[int] = ..., current_value: _Optional[int] = ..., max_value: _Optional[int] = ...) -> None: ...
    ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    accounts: _containers.RepeatedCompositeFieldContainer[CMsgLobbyFeaturedGamemodeProgress.AccountProgress]
    def __init__(self, accounts: _Optional[_Iterable[_Union[CMsgLobbyFeaturedGamemodeProgress.AccountProgress, _Mapping]]] = ...) -> None: ...

class CMsgBattleCupVictory(_message.Message):
    __slots__ = ("account_id", "win_date", "valid_until", "skill_level", "tournament_id", "division_id", "team_id", "streak", "trophy_id")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    WIN_DATE_FIELD_NUMBER: _ClassVar[int]
    VALID_UNTIL_FIELD_NUMBER: _ClassVar[int]
    SKILL_LEVEL_FIELD_NUMBER: _ClassVar[int]
    TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DIVISION_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    STREAK_FIELD_NUMBER: _ClassVar[int]
    TROPHY_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    win_date: int
    valid_until: int
    skill_level: int
    tournament_id: int
    division_id: int
    team_id: int
    streak: int
    trophy_id: int
    def __init__(self, account_id: _Optional[int] = ..., win_date: _Optional[int] = ..., valid_until: _Optional[int] = ..., skill_level: _Optional[int] = ..., tournament_id: _Optional[int] = ..., division_id: _Optional[int] = ..., team_id: _Optional[int] = ..., streak: _Optional[int] = ..., trophy_id: _Optional[int] = ...) -> None: ...

class CMsgLobbyBattleCupVictoryList(_message.Message):
    __slots__ = ("winners",)
    WINNERS_FIELD_NUMBER: _ClassVar[int]
    winners: _containers.RepeatedCompositeFieldContainer[CMsgBattleCupVictory]
    def __init__(self, winners: _Optional[_Iterable[_Union[CMsgBattleCupVictory, _Mapping]]] = ...) -> None: ...

class CMsgDOTABroadcastNotification(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class CProtoItemHeroStatue(_message.Message):
    __slots__ = ("hero_id", "status_effect_index", "sequence_name", "cycle", "wearable", "inscription", "style", "tournament_drop")
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_EFFECT_INDEX_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_NAME_FIELD_NUMBER: _ClassVar[int]
    CYCLE_FIELD_NUMBER: _ClassVar[int]
    WEARABLE_FIELD_NUMBER: _ClassVar[int]
    INSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STYLE_FIELD_NUMBER: _ClassVar[int]
    TOURNAMENT_DROP_FIELD_NUMBER: _ClassVar[int]
    hero_id: int
    status_effect_index: int
    sequence_name: str
    cycle: float
    wearable: _containers.RepeatedScalarFieldContainer[int]
    inscription: str
    style: _containers.RepeatedScalarFieldContainer[int]
    tournament_drop: bool
    def __init__(self, hero_id: _Optional[int] = ..., status_effect_index: _Optional[int] = ..., sequence_name: _Optional[str] = ..., cycle: _Optional[float] = ..., wearable: _Optional[_Iterable[int]] = ..., inscription: _Optional[str] = ..., style: _Optional[_Iterable[int]] = ..., tournament_drop: bool = ...) -> None: ...

class CMatchPlayerAbilityUpgrade(_message.Message):
    __slots__ = ("ability", "time")
    ABILITY_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    ability: int
    time: int
    def __init__(self, ability: _Optional[int] = ..., time: _Optional[int] = ...) -> None: ...

class CMatchPlayerTimedCustomStat(_message.Message):
    __slots__ = ("stat", "value")
    STAT_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    stat: EDOTAMatchPlayerTimeCustomStat
    value: float
    def __init__(self, stat: _Optional[_Union[EDOTAMatchPlayerTimeCustomStat, str]] = ..., value: _Optional[float] = ...) -> None: ...

class CMatchPlayerTimedStats(_message.Message):
    __slots__ = ("time", "kills", "deaths", "assists", "net_worth", "xp", "last_hits", "denies", "bounty_rune_gold", "range_creep_upgrade_gold", "observer_wards_dewarded", "reliable_gold_earned", "gold_loss_prevented", "hero_kill_gold", "creep_kill_gold", "building_gold", "other_gold", "comeback_gold", "experimental_gold", "experimental2_gold", "creep_deny_gold", "tp_scrolls_purchased_1", "tp_scrolls_purchased_2", "tp_scrolls_purchased_3", "tp_scrolls_purchased_4", "tp_scrolls_purchased_5", "neutral_gold", "courier_gold", "roshan_gold", "income_gold", "item_value", "support_gold_spent", "camps_stacked", "wards_placed", "triple_kills", "rampages", "custom_stats")
    TIME_FIELD_NUMBER: _ClassVar[int]
    KILLS_FIELD_NUMBER: _ClassVar[int]
    DEATHS_FIELD_NUMBER: _ClassVar[int]
    ASSISTS_FIELD_NUMBER: _ClassVar[int]
    NET_WORTH_FIELD_NUMBER: _ClassVar[int]
    XP_FIELD_NUMBER: _ClassVar[int]
    LAST_HITS_FIELD_NUMBER: _ClassVar[int]
    DENIES_FIELD_NUMBER: _ClassVar[int]
    BOUNTY_RUNE_GOLD_FIELD_NUMBER: _ClassVar[int]
    RANGE_CREEP_UPGRADE_GOLD_FIELD_NUMBER: _ClassVar[int]
    OBSERVER_WARDS_DEWARDED_FIELD_NUMBER: _ClassVar[int]
    RELIABLE_GOLD_EARNED_FIELD_NUMBER: _ClassVar[int]
    GOLD_LOSS_PREVENTED_FIELD_NUMBER: _ClassVar[int]
    HERO_KILL_GOLD_FIELD_NUMBER: _ClassVar[int]
    CREEP_KILL_GOLD_FIELD_NUMBER: _ClassVar[int]
    BUILDING_GOLD_FIELD_NUMBER: _ClassVar[int]
    OTHER_GOLD_FIELD_NUMBER: _ClassVar[int]
    COMEBACK_GOLD_FIELD_NUMBER: _ClassVar[int]
    EXPERIMENTAL_GOLD_FIELD_NUMBER: _ClassVar[int]
    EXPERIMENTAL2_GOLD_FIELD_NUMBER: _ClassVar[int]
    CREEP_DENY_GOLD_FIELD_NUMBER: _ClassVar[int]
    TP_SCROLLS_PURCHASED_1_FIELD_NUMBER: _ClassVar[int]
    TP_SCROLLS_PURCHASED_2_FIELD_NUMBER: _ClassVar[int]
    TP_SCROLLS_PURCHASED_3_FIELD_NUMBER: _ClassVar[int]
    TP_SCROLLS_PURCHASED_4_FIELD_NUMBER: _ClassVar[int]
    TP_SCROLLS_PURCHASED_5_FIELD_NUMBER: _ClassVar[int]
    NEUTRAL_GOLD_FIELD_NUMBER: _ClassVar[int]
    COURIER_GOLD_FIELD_NUMBER: _ClassVar[int]
    ROSHAN_GOLD_FIELD_NUMBER: _ClassVar[int]
    INCOME_GOLD_FIELD_NUMBER: _ClassVar[int]
    ITEM_VALUE_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_GOLD_SPENT_FIELD_NUMBER: _ClassVar[int]
    CAMPS_STACKED_FIELD_NUMBER: _ClassVar[int]
    WARDS_PLACED_FIELD_NUMBER: _ClassVar[int]
    TRIPLE_KILLS_FIELD_NUMBER: _ClassVar[int]
    RAMPAGES_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_STATS_FIELD_NUMBER: _ClassVar[int]
    time: int
    kills: int
    deaths: int
    assists: int
    net_worth: int
    xp: int
    last_hits: int
    denies: int
    bounty_rune_gold: int
    range_creep_upgrade_gold: int
    observer_wards_dewarded: int
    reliable_gold_earned: int
    gold_loss_prevented: int
    hero_kill_gold: int
    creep_kill_gold: int
    building_gold: int
    other_gold: int
    comeback_gold: int
    experimental_gold: int
    experimental2_gold: int
    creep_deny_gold: int
    tp_scrolls_purchased_1: int
    tp_scrolls_purchased_2: int
    tp_scrolls_purchased_3: int
    tp_scrolls_purchased_4: int
    tp_scrolls_purchased_5: int
    neutral_gold: int
    courier_gold: int
    roshan_gold: int
    income_gold: int
    item_value: int
    support_gold_spent: int
    camps_stacked: int
    wards_placed: int
    triple_kills: int
    rampages: int
    custom_stats: _containers.RepeatedCompositeFieldContainer[CMatchPlayerTimedCustomStat]
    def __init__(self, time: _Optional[int] = ..., kills: _Optional[int] = ..., deaths: _Optional[int] = ..., assists: _Optional[int] = ..., net_worth: _Optional[int] = ..., xp: _Optional[int] = ..., last_hits: _Optional[int] = ..., denies: _Optional[int] = ..., bounty_rune_gold: _Optional[int] = ..., range_creep_upgrade_gold: _Optional[int] = ..., observer_wards_dewarded: _Optional[int] = ..., reliable_gold_earned: _Optional[int] = ..., gold_loss_prevented: _Optional[int] = ..., hero_kill_gold: _Optional[int] = ..., creep_kill_gold: _Optional[int] = ..., building_gold: _Optional[int] = ..., other_gold: _Optional[int] = ..., comeback_gold: _Optional[int] = ..., experimental_gold: _Optional[int] = ..., experimental2_gold: _Optional[int] = ..., creep_deny_gold: _Optional[int] = ..., tp_scrolls_purchased_1: _Optional[int] = ..., tp_scrolls_purchased_2: _Optional[int] = ..., tp_scrolls_purchased_3: _Optional[int] = ..., tp_scrolls_purchased_4: _Optional[int] = ..., tp_scrolls_purchased_5: _Optional[int] = ..., neutral_gold: _Optional[int] = ..., courier_gold: _Optional[int] = ..., roshan_gold: _Optional[int] = ..., income_gold: _Optional[int] = ..., item_value: _Optional[int] = ..., support_gold_spent: _Optional[int] = ..., camps_stacked: _Optional[int] = ..., wards_placed: _Optional[int] = ..., triple_kills: _Optional[int] = ..., rampages: _Optional[int] = ..., custom_stats: _Optional[_Iterable[_Union[CMatchPlayerTimedCustomStat, _Mapping]]] = ...) -> None: ...

class CMatchTeamTimedStats(_message.Message):
    __slots__ = ("time", "enemy_towers_killed", "enemy_barracks_killed", "enemy_towers_status", "enemy_barracks_status")
    TIME_FIELD_NUMBER: _ClassVar[int]
    ENEMY_TOWERS_KILLED_FIELD_NUMBER: _ClassVar[int]
    ENEMY_BARRACKS_KILLED_FIELD_NUMBER: _ClassVar[int]
    ENEMY_TOWERS_STATUS_FIELD_NUMBER: _ClassVar[int]
    ENEMY_BARRACKS_STATUS_FIELD_NUMBER: _ClassVar[int]
    time: int
    enemy_towers_killed: int
    enemy_barracks_killed: int
    enemy_towers_status: int
    enemy_barracks_status: int
    def __init__(self, time: _Optional[int] = ..., enemy_towers_killed: _Optional[int] = ..., enemy_barracks_killed: _Optional[int] = ..., enemy_towers_status: _Optional[int] = ..., enemy_barracks_status: _Optional[int] = ...) -> None: ...

class CMatchAdditionalUnitInventory(_message.Message):
    __slots__ = ("unit_name", "items")
    UNIT_NAME_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    unit_name: str
    items: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, unit_name: _Optional[str] = ..., items: _Optional[_Iterable[int]] = ...) -> None: ...

class CMatchPlayerPermanentBuff(_message.Message):
    __slots__ = ("permanent_buff", "stack_count", "grant_time")
    PERMANENT_BUFF_FIELD_NUMBER: _ClassVar[int]
    STACK_COUNT_FIELD_NUMBER: _ClassVar[int]
    GRANT_TIME_FIELD_NUMBER: _ClassVar[int]
    permanent_buff: int
    stack_count: int
    grant_time: int
    def __init__(self, permanent_buff: _Optional[int] = ..., stack_count: _Optional[int] = ..., grant_time: _Optional[int] = ...) -> None: ...

class CMatchHeroSelectEvent(_message.Message):
    __slots__ = ("is_pick", "team", "hero_id")
    IS_PICK_FIELD_NUMBER: _ClassVar[int]
    TEAM_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    is_pick: bool
    team: int
    hero_id: int
    def __init__(self, is_pick: bool = ..., team: _Optional[int] = ..., hero_id: _Optional[int] = ...) -> None: ...

class CMatchClip(_message.Message):
    __slots__ = ("match_id", "player_account_id", "game_time_seconds", "duration_seconds", "player_id", "hero_id", "ability_id", "camera_mode", "comment")
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    PLAYER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    GAME_TIME_SECONDS_FIELD_NUMBER: _ClassVar[int]
    DURATION_SECONDS_FIELD_NUMBER: _ClassVar[int]
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    CAMERA_MODE_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    player_account_id: int
    game_time_seconds: int
    duration_seconds: int
    player_id: int
    hero_id: int
    ability_id: int
    camera_mode: int
    comment: str
    def __init__(self, match_id: _Optional[int] = ..., player_account_id: _Optional[int] = ..., game_time_seconds: _Optional[int] = ..., duration_seconds: _Optional[int] = ..., player_id: _Optional[int] = ..., hero_id: _Optional[int] = ..., ability_id: _Optional[int] = ..., camera_mode: _Optional[int] = ..., comment: _Optional[str] = ...) -> None: ...

class CPartySearchClientParty(_message.Message):
    __slots__ = ("party_id", "beacon_type", "party_members")
    PARTY_ID_FIELD_NUMBER: _ClassVar[int]
    BEACON_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARTY_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    party_id: int
    beacon_type: int
    party_members: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, party_id: _Optional[int] = ..., beacon_type: _Optional[int] = ..., party_members: _Optional[_Iterable[int]] = ...) -> None: ...

class CMsgDOTAHasItemQuery(_message.Message):
    __slots__ = ("account_id", "item_id")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    item_id: int
    def __init__(self, account_id: _Optional[int] = ..., item_id: _Optional[int] = ...) -> None: ...

class CMsgDOTAHasItemResponse(_message.Message):
    __slots__ = ("has_item",)
    HAS_ITEM_FIELD_NUMBER: _ClassVar[int]
    has_item: bool
    def __init__(self, has_item: bool = ...) -> None: ...

class CMsgGCGetPlayerCardItemInfo(_message.Message):
    __slots__ = ("account_id", "player_card_item_ids", "all_for_event")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    PLAYER_CARD_ITEM_IDS_FIELD_NUMBER: _ClassVar[int]
    ALL_FOR_EVENT_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    player_card_item_ids: _containers.RepeatedScalarFieldContainer[int]
    all_for_event: int
    def __init__(self, account_id: _Optional[int] = ..., player_card_item_ids: _Optional[_Iterable[int]] = ..., all_for_event: _Optional[int] = ...) -> None: ...

class CMsgGCGetPlayerCardItemInfoResponse(_message.Message):
    __slots__ = ("player_card_infos",)
    class PlayerCardInfo(_message.Message):
        __slots__ = ("player_card_item_id", "account_id", "packed_bonuses")
        PLAYER_CARD_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        PACKED_BONUSES_FIELD_NUMBER: _ClassVar[int]
        player_card_item_id: int
        account_id: int
        packed_bonuses: int
        def __init__(self, player_card_item_id: _Optional[int] = ..., account_id: _Optional[int] = ..., packed_bonuses: _Optional[int] = ...) -> None: ...
    PLAYER_CARD_INFOS_FIELD_NUMBER: _ClassVar[int]
    player_card_infos: _containers.RepeatedCompositeFieldContainer[CMsgGCGetPlayerCardItemInfoResponse.PlayerCardInfo]
    def __init__(self, player_card_infos: _Optional[_Iterable[_Union[CMsgGCGetPlayerCardItemInfoResponse.PlayerCardInfo, _Mapping]]] = ...) -> None: ...

class CSODOTAMapLocationState(_message.Message):
    __slots__ = ("account_id", "location_id", "completed")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    LOCATION_ID_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    location_id: int
    completed: bool
    def __init__(self, account_id: _Optional[int] = ..., location_id: _Optional[int] = ..., completed: bool = ...) -> None: ...

class CMsgLeagueAdminList(_message.Message):
    __slots__ = ("account_ids",)
    ACCOUNT_IDS_FIELD_NUMBER: _ClassVar[int]
    account_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, account_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class CMsgDOTAProfileCard(_message.Message):
    __slots__ = ("account_id", "slots", "badge_points", "event_id", "recent_battle_cup_victory", "rank_tier", "leaderboard_rank", "is_plus_subscriber", "plus_original_start_date", "rank_tier_score", "leaderboard_rank_core", "title", "favorite_team_packed", "lifetime_games", "event_level")
    class EStatID(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eStat_Wins: _ClassVar[CMsgDOTAProfileCard.EStatID]
        k_eStat_Commends: _ClassVar[CMsgDOTAProfileCard.EStatID]
        k_eStat_GamesPlayed: _ClassVar[CMsgDOTAProfileCard.EStatID]
        k_eStat_FirstMatchDate: _ClassVar[CMsgDOTAProfileCard.EStatID]
        k_eStat_PreviousSeasonRank: _ClassVar[CMsgDOTAProfileCard.EStatID]
        k_eStat_GamesMVP: _ClassVar[CMsgDOTAProfileCard.EStatID]
    k_eStat_Wins: CMsgDOTAProfileCard.EStatID
    k_eStat_Commends: CMsgDOTAProfileCard.EStatID
    k_eStat_GamesPlayed: CMsgDOTAProfileCard.EStatID
    k_eStat_FirstMatchDate: CMsgDOTAProfileCard.EStatID
    k_eStat_PreviousSeasonRank: CMsgDOTAProfileCard.EStatID
    k_eStat_GamesMVP: CMsgDOTAProfileCard.EStatID
    class Slot(_message.Message):
        __slots__ = ("slot_id", "trophy", "stat", "item", "hero", "emoticon", "team")
        class Trophy(_message.Message):
            __slots__ = ("trophy_id", "trophy_score")
            TROPHY_ID_FIELD_NUMBER: _ClassVar[int]
            TROPHY_SCORE_FIELD_NUMBER: _ClassVar[int]
            trophy_id: int
            trophy_score: int
            def __init__(self, trophy_id: _Optional[int] = ..., trophy_score: _Optional[int] = ...) -> None: ...
        class Stat(_message.Message):
            __slots__ = ("stat_id", "stat_score")
            STAT_ID_FIELD_NUMBER: _ClassVar[int]
            STAT_SCORE_FIELD_NUMBER: _ClassVar[int]
            stat_id: CMsgDOTAProfileCard.EStatID
            stat_score: int
            def __init__(self, stat_id: _Optional[_Union[CMsgDOTAProfileCard.EStatID, str]] = ..., stat_score: _Optional[int] = ...) -> None: ...
        class Item(_message.Message):
            __slots__ = ("serialized_item", "item_id")
            SERIALIZED_ITEM_FIELD_NUMBER: _ClassVar[int]
            ITEM_ID_FIELD_NUMBER: _ClassVar[int]
            serialized_item: bytes
            item_id: int
            def __init__(self, serialized_item: _Optional[bytes] = ..., item_id: _Optional[int] = ...) -> None: ...
        class Hero(_message.Message):
            __slots__ = ("hero_id", "hero_wins", "hero_losses")
            HERO_ID_FIELD_NUMBER: _ClassVar[int]
            HERO_WINS_FIELD_NUMBER: _ClassVar[int]
            HERO_LOSSES_FIELD_NUMBER: _ClassVar[int]
            hero_id: int
            hero_wins: int
            hero_losses: int
            def __init__(self, hero_id: _Optional[int] = ..., hero_wins: _Optional[int] = ..., hero_losses: _Optional[int] = ...) -> None: ...
        class Emoticon(_message.Message):
            __slots__ = ("emoticon_id",)
            EMOTICON_ID_FIELD_NUMBER: _ClassVar[int]
            emoticon_id: int
            def __init__(self, emoticon_id: _Optional[int] = ...) -> None: ...
        class Team(_message.Message):
            __slots__ = ("team_id",)
            TEAM_ID_FIELD_NUMBER: _ClassVar[int]
            team_id: int
            def __init__(self, team_id: _Optional[int] = ...) -> None: ...
        SLOT_ID_FIELD_NUMBER: _ClassVar[int]
        TROPHY_FIELD_NUMBER: _ClassVar[int]
        STAT_FIELD_NUMBER: _ClassVar[int]
        ITEM_FIELD_NUMBER: _ClassVar[int]
        HERO_FIELD_NUMBER: _ClassVar[int]
        EMOTICON_FIELD_NUMBER: _ClassVar[int]
        TEAM_FIELD_NUMBER: _ClassVar[int]
        slot_id: int
        trophy: CMsgDOTAProfileCard.Slot.Trophy
        stat: CMsgDOTAProfileCard.Slot.Stat
        item: CMsgDOTAProfileCard.Slot.Item
        hero: CMsgDOTAProfileCard.Slot.Hero
        emoticon: CMsgDOTAProfileCard.Slot.Emoticon
        team: CMsgDOTAProfileCard.Slot.Team
        def __init__(self, slot_id: _Optional[int] = ..., trophy: _Optional[_Union[CMsgDOTAProfileCard.Slot.Trophy, _Mapping]] = ..., stat: _Optional[_Union[CMsgDOTAProfileCard.Slot.Stat, _Mapping]] = ..., item: _Optional[_Union[CMsgDOTAProfileCard.Slot.Item, _Mapping]] = ..., hero: _Optional[_Union[CMsgDOTAProfileCard.Slot.Hero, _Mapping]] = ..., emoticon: _Optional[_Union[CMsgDOTAProfileCard.Slot.Emoticon, _Mapping]] = ..., team: _Optional[_Union[CMsgDOTAProfileCard.Slot.Team, _Mapping]] = ...) -> None: ...
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SLOTS_FIELD_NUMBER: _ClassVar[int]
    BADGE_POINTS_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    RECENT_BATTLE_CUP_VICTORY_FIELD_NUMBER: _ClassVar[int]
    RANK_TIER_FIELD_NUMBER: _ClassVar[int]
    LEADERBOARD_RANK_FIELD_NUMBER: _ClassVar[int]
    IS_PLUS_SUBSCRIBER_FIELD_NUMBER: _ClassVar[int]
    PLUS_ORIGINAL_START_DATE_FIELD_NUMBER: _ClassVar[int]
    RANK_TIER_SCORE_FIELD_NUMBER: _ClassVar[int]
    LEADERBOARD_RANK_CORE_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    FAVORITE_TEAM_PACKED_FIELD_NUMBER: _ClassVar[int]
    LIFETIME_GAMES_FIELD_NUMBER: _ClassVar[int]
    EVENT_LEVEL_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    slots: _containers.RepeatedCompositeFieldContainer[CMsgDOTAProfileCard.Slot]
    badge_points: int
    event_id: int
    recent_battle_cup_victory: CMsgBattleCupVictory
    rank_tier: int
    leaderboard_rank: int
    is_plus_subscriber: bool
    plus_original_start_date: int
    rank_tier_score: int
    leaderboard_rank_core: int
    title: int
    favorite_team_packed: int
    lifetime_games: int
    event_level: int
    def __init__(self, account_id: _Optional[int] = ..., slots: _Optional[_Iterable[_Union[CMsgDOTAProfileCard.Slot, _Mapping]]] = ..., badge_points: _Optional[int] = ..., event_id: _Optional[int] = ..., recent_battle_cup_victory: _Optional[_Union[CMsgBattleCupVictory, _Mapping]] = ..., rank_tier: _Optional[int] = ..., leaderboard_rank: _Optional[int] = ..., is_plus_subscriber: bool = ..., plus_original_start_date: _Optional[int] = ..., rank_tier_score: _Optional[int] = ..., leaderboard_rank_core: _Optional[int] = ..., title: _Optional[int] = ..., favorite_team_packed: _Optional[int] = ..., lifetime_games: _Optional[int] = ..., event_level: _Optional[int] = ...) -> None: ...

class CSODOTAPlayerChallenge(_message.Message):
    __slots__ = ("account_id", "event_id", "slot_id", "int_param_0", "int_param_1", "created_time", "completed", "sequence_id", "challenge_tier", "flags", "attempts", "complete_limit", "quest_rank", "max_quest_rank", "instance_id", "hero_id", "template_id")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    SLOT_ID_FIELD_NUMBER: _ClassVar[int]
    INT_PARAM_0_FIELD_NUMBER: _ClassVar[int]
    INT_PARAM_1_FIELD_NUMBER: _ClassVar[int]
    CREATED_TIME_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_ID_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_TIER_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    COMPLETE_LIMIT_FIELD_NUMBER: _ClassVar[int]
    QUEST_RANK_FIELD_NUMBER: _ClassVar[int]
    MAX_QUEST_RANK_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    event_id: int
    slot_id: int
    int_param_0: int
    int_param_1: int
    created_time: int
    completed: int
    sequence_id: int
    challenge_tier: int
    flags: int
    attempts: int
    complete_limit: int
    quest_rank: int
    max_quest_rank: int
    instance_id: int
    hero_id: int
    template_id: int
    def __init__(self, account_id: _Optional[int] = ..., event_id: _Optional[int] = ..., slot_id: _Optional[int] = ..., int_param_0: _Optional[int] = ..., int_param_1: _Optional[int] = ..., created_time: _Optional[int] = ..., completed: _Optional[int] = ..., sequence_id: _Optional[int] = ..., challenge_tier: _Optional[int] = ..., flags: _Optional[int] = ..., attempts: _Optional[int] = ..., complete_limit: _Optional[int] = ..., quest_rank: _Optional[int] = ..., max_quest_rank: _Optional[int] = ..., instance_id: _Optional[int] = ..., hero_id: _Optional[int] = ..., template_id: _Optional[int] = ...) -> None: ...

class CMsgClientToGCRerollPlayerChallenge(_message.Message):
    __slots__ = ("event_id", "sequence_id", "hero_id")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_ID_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: _dota_shared_enums_pb2.EEvent
    sequence_id: int
    hero_id: int
    def __init__(self, event_id: _Optional[_Union[_dota_shared_enums_pb2.EEvent, str]] = ..., sequence_id: _Optional[int] = ..., hero_id: _Optional[int] = ...) -> None: ...

class CMsgGCRerollPlayerChallengeResponse(_message.Message):
    __slots__ = ("result",)
    class EResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        eResult_Success: _ClassVar[CMsgGCRerollPlayerChallengeResponse.EResult]
        eResult_Dropped: _ClassVar[CMsgGCRerollPlayerChallengeResponse.EResult]
        eResult_NotFound: _ClassVar[CMsgGCRerollPlayerChallengeResponse.EResult]
        eResult_CantReroll: _ClassVar[CMsgGCRerollPlayerChallengeResponse.EResult]
        eResult_ServerError: _ClassVar[CMsgGCRerollPlayerChallengeResponse.EResult]
    eResult_Success: CMsgGCRerollPlayerChallengeResponse.EResult
    eResult_Dropped: CMsgGCRerollPlayerChallengeResponse.EResult
    eResult_NotFound: CMsgGCRerollPlayerChallengeResponse.EResult
    eResult_CantReroll: CMsgGCRerollPlayerChallengeResponse.EResult
    eResult_ServerError: CMsgGCRerollPlayerChallengeResponse.EResult
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: CMsgGCRerollPlayerChallengeResponse.EResult
    def __init__(self, result: _Optional[_Union[CMsgGCRerollPlayerChallengeResponse.EResult, str]] = ...) -> None: ...

class CMsgGCTopCustomGamesList(_message.Message):
    __slots__ = ("top_custom_games", "game_of_the_day")
    TOP_CUSTOM_GAMES_FIELD_NUMBER: _ClassVar[int]
    GAME_OF_THE_DAY_FIELD_NUMBER: _ClassVar[int]
    top_custom_games: _containers.RepeatedScalarFieldContainer[int]
    game_of_the_day: int
    def __init__(self, top_custom_games: _Optional[_Iterable[int]] = ..., game_of_the_day: _Optional[int] = ...) -> None: ...

class CMsgDOTARealtimeGameStats(_message.Message):
    __slots__ = ("match", "teams", "buildings", "graph_data", "delta_frame")
    class TeamDetails(_message.Message):
        __slots__ = ("team_number", "team_id", "team_name", "team_logo", "team_tag", "score", "net_worth", "players", "only_team", "cheers", "team_logo_url")
        TEAM_NUMBER_FIELD_NUMBER: _ClassVar[int]
        TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
        TEAM_LOGO_FIELD_NUMBER: _ClassVar[int]
        TEAM_TAG_FIELD_NUMBER: _ClassVar[int]
        SCORE_FIELD_NUMBER: _ClassVar[int]
        NET_WORTH_FIELD_NUMBER: _ClassVar[int]
        PLAYERS_FIELD_NUMBER: _ClassVar[int]
        ONLY_TEAM_FIELD_NUMBER: _ClassVar[int]
        CHEERS_FIELD_NUMBER: _ClassVar[int]
        TEAM_LOGO_URL_FIELD_NUMBER: _ClassVar[int]
        team_number: int
        team_id: int
        team_name: str
        team_logo: int
        team_tag: str
        score: int
        net_worth: int
        players: _containers.RepeatedCompositeFieldContainer[CMsgDOTARealtimeGameStats.PlayerDetails]
        only_team: bool
        cheers: int
        team_logo_url: str
        def __init__(self, team_number: _Optional[int] = ..., team_id: _Optional[int] = ..., team_name: _Optional[str] = ..., team_logo: _Optional[int] = ..., team_tag: _Optional[str] = ..., score: _Optional[int] = ..., net_worth: _Optional[int] = ..., players: _Optional[_Iterable[_Union[CMsgDOTARealtimeGameStats.PlayerDetails, _Mapping]]] = ..., only_team: bool = ..., cheers: _Optional[int] = ..., team_logo_url: _Optional[str] = ...) -> None: ...
    class ItemDetails(_message.Message):
        __slots__ = ("item_ability_id", "name", "time", "sold", "stackcount")
        ITEM_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        TIME_FIELD_NUMBER: _ClassVar[int]
        SOLD_FIELD_NUMBER: _ClassVar[int]
        STACKCOUNT_FIELD_NUMBER: _ClassVar[int]
        item_ability_id: int
        name: str
        time: int
        sold: bool
        stackcount: int
        def __init__(self, item_ability_id: _Optional[int] = ..., name: _Optional[str] = ..., time: _Optional[int] = ..., sold: bool = ..., stackcount: _Optional[int] = ...) -> None: ...
    class AbilityDetails(_message.Message):
        __slots__ = ("id", "name", "level", "cooldown", "cooldown_max")
        ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        COOLDOWN_FIELD_NUMBER: _ClassVar[int]
        COOLDOWN_MAX_FIELD_NUMBER: _ClassVar[int]
        id: int
        name: str
        level: int
        cooldown: float
        cooldown_max: float
        def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., level: _Optional[int] = ..., cooldown: _Optional[float] = ..., cooldown_max: _Optional[float] = ...) -> None: ...
    class HeroToHeroStats(_message.Message):
        __slots__ = ("victimid", "kills", "assists")
        VICTIMID_FIELD_NUMBER: _ClassVar[int]
        KILLS_FIELD_NUMBER: _ClassVar[int]
        ASSISTS_FIELD_NUMBER: _ClassVar[int]
        victimid: int
        kills: int
        assists: int
        def __init__(self, victimid: _Optional[int] = ..., kills: _Optional[int] = ..., assists: _Optional[int] = ...) -> None: ...
    class AbilityList(_message.Message):
        __slots__ = ("id",)
        ID_FIELD_NUMBER: _ClassVar[int]
        id: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, id: _Optional[_Iterable[int]] = ...) -> None: ...
    class PlayerDetails(_message.Message):
        __slots__ = ("accountid", "playerid", "name", "team", "heroid", "healthpoints", "maxhealthpoints", "healthregenrate", "manapoints", "maxmanapoints", "manaregenrate", "base_strength", "base_agility", "base_intelligence", "base_armor", "base_movespeed", "base_damage", "strength", "agility", "intelligence", "armor", "movespeed", "damage", "hero_damage", "tower_damage", "abilities", "level", "kill_count", "death_count", "assists_count", "denies_count", "lh_count", "hero_healing", "gold_per_min", "xp_per_min", "net_gold", "gold", "x", "y", "respawn_time", "ultimate_cooldown", "has_buyback", "items", "stashitems", "itemshoppinglist", "levelpoints", "hero_to_hero_stats", "has_ultimate", "has_ultimate_mana", "team_slot")
        ACCOUNTID_FIELD_NUMBER: _ClassVar[int]
        PLAYERID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        TEAM_FIELD_NUMBER: _ClassVar[int]
        HEROID_FIELD_NUMBER: _ClassVar[int]
        HEALTHPOINTS_FIELD_NUMBER: _ClassVar[int]
        MAXHEALTHPOINTS_FIELD_NUMBER: _ClassVar[int]
        HEALTHREGENRATE_FIELD_NUMBER: _ClassVar[int]
        MANAPOINTS_FIELD_NUMBER: _ClassVar[int]
        MAXMANAPOINTS_FIELD_NUMBER: _ClassVar[int]
        MANAREGENRATE_FIELD_NUMBER: _ClassVar[int]
        BASE_STRENGTH_FIELD_NUMBER: _ClassVar[int]
        BASE_AGILITY_FIELD_NUMBER: _ClassVar[int]
        BASE_INTELLIGENCE_FIELD_NUMBER: _ClassVar[int]
        BASE_ARMOR_FIELD_NUMBER: _ClassVar[int]
        BASE_MOVESPEED_FIELD_NUMBER: _ClassVar[int]
        BASE_DAMAGE_FIELD_NUMBER: _ClassVar[int]
        STRENGTH_FIELD_NUMBER: _ClassVar[int]
        AGILITY_FIELD_NUMBER: _ClassVar[int]
        INTELLIGENCE_FIELD_NUMBER: _ClassVar[int]
        ARMOR_FIELD_NUMBER: _ClassVar[int]
        MOVESPEED_FIELD_NUMBER: _ClassVar[int]
        DAMAGE_FIELD_NUMBER: _ClassVar[int]
        HERO_DAMAGE_FIELD_NUMBER: _ClassVar[int]
        TOWER_DAMAGE_FIELD_NUMBER: _ClassVar[int]
        ABILITIES_FIELD_NUMBER: _ClassVar[int]
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        KILL_COUNT_FIELD_NUMBER: _ClassVar[int]
        DEATH_COUNT_FIELD_NUMBER: _ClassVar[int]
        ASSISTS_COUNT_FIELD_NUMBER: _ClassVar[int]
        DENIES_COUNT_FIELD_NUMBER: _ClassVar[int]
        LH_COUNT_FIELD_NUMBER: _ClassVar[int]
        HERO_HEALING_FIELD_NUMBER: _ClassVar[int]
        GOLD_PER_MIN_FIELD_NUMBER: _ClassVar[int]
        XP_PER_MIN_FIELD_NUMBER: _ClassVar[int]
        NET_GOLD_FIELD_NUMBER: _ClassVar[int]
        GOLD_FIELD_NUMBER: _ClassVar[int]
        X_FIELD_NUMBER: _ClassVar[int]
        Y_FIELD_NUMBER: _ClassVar[int]
        RESPAWN_TIME_FIELD_NUMBER: _ClassVar[int]
        ULTIMATE_COOLDOWN_FIELD_NUMBER: _ClassVar[int]
        HAS_BUYBACK_FIELD_NUMBER: _ClassVar[int]
        ITEMS_FIELD_NUMBER: _ClassVar[int]
        STASHITEMS_FIELD_NUMBER: _ClassVar[int]
        ITEMSHOPPINGLIST_FIELD_NUMBER: _ClassVar[int]
        LEVELPOINTS_FIELD_NUMBER: _ClassVar[int]
        HERO_TO_HERO_STATS_FIELD_NUMBER: _ClassVar[int]
        HAS_ULTIMATE_FIELD_NUMBER: _ClassVar[int]
        HAS_ULTIMATE_MANA_FIELD_NUMBER: _ClassVar[int]
        TEAM_SLOT_FIELD_NUMBER: _ClassVar[int]
        accountid: int
        playerid: int
        name: str
        team: int
        heroid: int
        healthpoints: int
        maxhealthpoints: int
        healthregenrate: float
        manapoints: int
        maxmanapoints: int
        manaregenrate: float
        base_strength: int
        base_agility: int
        base_intelligence: int
        base_armor: int
        base_movespeed: int
        base_damage: int
        strength: int
        agility: int
        intelligence: int
        armor: int
        movespeed: int
        damage: int
        hero_damage: int
        tower_damage: int
        abilities: _containers.RepeatedCompositeFieldContainer[CMsgDOTARealtimeGameStats.AbilityDetails]
        level: int
        kill_count: int
        death_count: int
        assists_count: int
        denies_count: int
        lh_count: int
        hero_healing: int
        gold_per_min: int
        xp_per_min: int
        net_gold: int
        gold: int
        x: float
        y: float
        respawn_time: int
        ultimate_cooldown: int
        has_buyback: bool
        items: _containers.RepeatedCompositeFieldContainer[CMsgDOTARealtimeGameStats.ItemDetails]
        stashitems: _containers.RepeatedCompositeFieldContainer[CMsgDOTARealtimeGameStats.ItemDetails]
        itemshoppinglist: _containers.RepeatedCompositeFieldContainer[CMsgDOTARealtimeGameStats.ItemDetails]
        levelpoints: _containers.RepeatedCompositeFieldContainer[CMsgDOTARealtimeGameStats.AbilityList]
        hero_to_hero_stats: _containers.RepeatedCompositeFieldContainer[CMsgDOTARealtimeGameStats.HeroToHeroStats]
        has_ultimate: bool
        has_ultimate_mana: bool
        team_slot: int
        def __init__(self, accountid: _Optional[int] = ..., playerid: _Optional[int] = ..., name: _Optional[str] = ..., team: _Optional[int] = ..., heroid: _Optional[int] = ..., healthpoints: _Optional[int] = ..., maxhealthpoints: _Optional[int] = ..., healthregenrate: _Optional[float] = ..., manapoints: _Optional[int] = ..., maxmanapoints: _Optional[int] = ..., manaregenrate: _Optional[float] = ..., base_strength: _Optional[int] = ..., base_agility: _Optional[int] = ..., base_intelligence: _Optional[int] = ..., base_armor: _Optional[int] = ..., base_movespeed: _Optional[int] = ..., base_damage: _Optional[int] = ..., strength: _Optional[int] = ..., agility: _Optional[int] = ..., intelligence: _Optional[int] = ..., armor: _Optional[int] = ..., movespeed: _Optional[int] = ..., damage: _Optional[int] = ..., hero_damage: _Optional[int] = ..., tower_damage: _Optional[int] = ..., abilities: _Optional[_Iterable[_Union[CMsgDOTARealtimeGameStats.AbilityDetails, _Mapping]]] = ..., level: _Optional[int] = ..., kill_count: _Optional[int] = ..., death_count: _Optional[int] = ..., assists_count: _Optional[int] = ..., denies_count: _Optional[int] = ..., lh_count: _Optional[int] = ..., hero_healing: _Optional[int] = ..., gold_per_min: _Optional[int] = ..., xp_per_min: _Optional[int] = ..., net_gold: _Optional[int] = ..., gold: _Optional[int] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., respawn_time: _Optional[int] = ..., ultimate_cooldown: _Optional[int] = ..., has_buyback: bool = ..., items: _Optional[_Iterable[_Union[CMsgDOTARealtimeGameStats.ItemDetails, _Mapping]]] = ..., stashitems: _Optional[_Iterable[_Union[CMsgDOTARealtimeGameStats.ItemDetails, _Mapping]]] = ..., itemshoppinglist: _Optional[_Iterable[_Union[CMsgDOTARealtimeGameStats.ItemDetails, _Mapping]]] = ..., levelpoints: _Optional[_Iterable[_Union[CMsgDOTARealtimeGameStats.AbilityList, _Mapping]]] = ..., hero_to_hero_stats: _Optional[_Iterable[_Union[CMsgDOTARealtimeGameStats.HeroToHeroStats, _Mapping]]] = ..., has_ultimate: bool = ..., has_ultimate_mana: bool = ..., team_slot: _Optional[int] = ...) -> None: ...
    class BuildingDetails(_message.Message):
        __slots__ = ("team", "heading", "lane", "tier", "type", "x", "y", "destroyed")
        TEAM_FIELD_NUMBER: _ClassVar[int]
        HEADING_FIELD_NUMBER: _ClassVar[int]
        LANE_FIELD_NUMBER: _ClassVar[int]
        TIER_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        X_FIELD_NUMBER: _ClassVar[int]
        Y_FIELD_NUMBER: _ClassVar[int]
        DESTROYED_FIELD_NUMBER: _ClassVar[int]
        team: int
        heading: float
        lane: int
        tier: int
        type: int
        x: float
        y: float
        destroyed: bool
        def __init__(self, team: _Optional[int] = ..., heading: _Optional[float] = ..., lane: _Optional[int] = ..., tier: _Optional[int] = ..., type: _Optional[int] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., destroyed: bool = ...) -> None: ...
    class KillDetails(_message.Message):
        __slots__ = ("player_id", "death_time", "killer_player_id")
        PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
        DEATH_TIME_FIELD_NUMBER: _ClassVar[int]
        KILLER_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
        player_id: int
        death_time: int
        killer_player_id: int
        def __init__(self, player_id: _Optional[int] = ..., death_time: _Optional[int] = ..., killer_player_id: _Optional[int] = ...) -> None: ...
    class BroadcasterDetails(_message.Message):
        __slots__ = ("player_id",)
        PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
        player_id: int
        def __init__(self, player_id: _Optional[int] = ...) -> None: ...
    class PickBanDetails(_message.Message):
        __slots__ = ("hero", "team")
        HERO_FIELD_NUMBER: _ClassVar[int]
        TEAM_FIELD_NUMBER: _ClassVar[int]
        hero: int
        team: int
        def __init__(self, hero: _Optional[int] = ..., team: _Optional[int] = ...) -> None: ...
    class MatchDetails(_message.Message):
        __slots__ = ("server_steam_id", "match_id", "timestamp", "time_of_day", "is_nightstalker_night", "game_time", "game_state", "teamid_radiant", "teamid_dire", "picks", "bans", "kills", "broadcasters", "game_mode", "league_id", "league_node_id", "single_team", "cheers_peak", "lobby_type", "start_timestamp", "is_player_draft")
        SERVER_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
        MATCH_ID_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        TIME_OF_DAY_FIELD_NUMBER: _ClassVar[int]
        IS_NIGHTSTALKER_NIGHT_FIELD_NUMBER: _ClassVar[int]
        GAME_TIME_FIELD_NUMBER: _ClassVar[int]
        GAME_STATE_FIELD_NUMBER: _ClassVar[int]
        TEAMID_RADIANT_FIELD_NUMBER: _ClassVar[int]
        TEAMID_DIRE_FIELD_NUMBER: _ClassVar[int]
        PICKS_FIELD_NUMBER: _ClassVar[int]
        BANS_FIELD_NUMBER: _ClassVar[int]
        KILLS_FIELD_NUMBER: _ClassVar[int]
        BROADCASTERS_FIELD_NUMBER: _ClassVar[int]
        GAME_MODE_FIELD_NUMBER: _ClassVar[int]
        LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
        LEAGUE_NODE_ID_FIELD_NUMBER: _ClassVar[int]
        SINGLE_TEAM_FIELD_NUMBER: _ClassVar[int]
        CHEERS_PEAK_FIELD_NUMBER: _ClassVar[int]
        LOBBY_TYPE_FIELD_NUMBER: _ClassVar[int]
        START_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        IS_PLAYER_DRAFT_FIELD_NUMBER: _ClassVar[int]
        server_steam_id: int
        match_id: int
        timestamp: int
        time_of_day: float
        is_nightstalker_night: bool
        game_time: int
        game_state: int
        teamid_radiant: int
        teamid_dire: int
        picks: _containers.RepeatedCompositeFieldContainer[CMsgDOTARealtimeGameStats.PickBanDetails]
        bans: _containers.RepeatedCompositeFieldContainer[CMsgDOTARealtimeGameStats.PickBanDetails]
        kills: _containers.RepeatedCompositeFieldContainer[CMsgDOTARealtimeGameStats.KillDetails]
        broadcasters: _containers.RepeatedCompositeFieldContainer[CMsgDOTARealtimeGameStats.BroadcasterDetails]
        game_mode: int
        league_id: int
        league_node_id: int
        single_team: bool
        cheers_peak: int
        lobby_type: int
        start_timestamp: int
        is_player_draft: bool
        def __init__(self, server_steam_id: _Optional[int] = ..., match_id: _Optional[int] = ..., timestamp: _Optional[int] = ..., time_of_day: _Optional[float] = ..., is_nightstalker_night: bool = ..., game_time: _Optional[int] = ..., game_state: _Optional[int] = ..., teamid_radiant: _Optional[int] = ..., teamid_dire: _Optional[int] = ..., picks: _Optional[_Iterable[_Union[CMsgDOTARealtimeGameStats.PickBanDetails, _Mapping]]] = ..., bans: _Optional[_Iterable[_Union[CMsgDOTARealtimeGameStats.PickBanDetails, _Mapping]]] = ..., kills: _Optional[_Iterable[_Union[CMsgDOTARealtimeGameStats.KillDetails, _Mapping]]] = ..., broadcasters: _Optional[_Iterable[_Union[CMsgDOTARealtimeGameStats.BroadcasterDetails, _Mapping]]] = ..., game_mode: _Optional[int] = ..., league_id: _Optional[int] = ..., league_node_id: _Optional[int] = ..., single_team: bool = ..., cheers_peak: _Optional[int] = ..., lobby_type: _Optional[int] = ..., start_timestamp: _Optional[int] = ..., is_player_draft: bool = ...) -> None: ...
    class GraphData(_message.Message):
        __slots__ = ("graph_gold", "graph_xp", "graph_kill", "graph_tower", "graph_rax", "team_loc_stats")
        class eStat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            CreepGoldEarned: _ClassVar[CMsgDOTARealtimeGameStats.GraphData.eStat]
            KillGoldEarned: _ClassVar[CMsgDOTARealtimeGameStats.GraphData.eStat]
            DeathAndBuybackGoldLost: _ClassVar[CMsgDOTARealtimeGameStats.GraphData.eStat]
            XPEarned: _ClassVar[CMsgDOTARealtimeGameStats.GraphData.eStat]
        CreepGoldEarned: CMsgDOTARealtimeGameStats.GraphData.eStat
        KillGoldEarned: CMsgDOTARealtimeGameStats.GraphData.eStat
        DeathAndBuybackGoldLost: CMsgDOTARealtimeGameStats.GraphData.eStat
        XPEarned: CMsgDOTARealtimeGameStats.GraphData.eStat
        class eLocation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            BotLane: _ClassVar[CMsgDOTARealtimeGameStats.GraphData.eLocation]
            MidLane: _ClassVar[CMsgDOTARealtimeGameStats.GraphData.eLocation]
            TopLane: _ClassVar[CMsgDOTARealtimeGameStats.GraphData.eLocation]
            Jungle: _ClassVar[CMsgDOTARealtimeGameStats.GraphData.eLocation]
            Ancients: _ClassVar[CMsgDOTARealtimeGameStats.GraphData.eLocation]
            Other: _ClassVar[CMsgDOTARealtimeGameStats.GraphData.eLocation]
        BotLane: CMsgDOTARealtimeGameStats.GraphData.eLocation
        MidLane: CMsgDOTARealtimeGameStats.GraphData.eLocation
        TopLane: CMsgDOTARealtimeGameStats.GraphData.eLocation
        Jungle: CMsgDOTARealtimeGameStats.GraphData.eLocation
        Ancients: CMsgDOTARealtimeGameStats.GraphData.eLocation
        Other: CMsgDOTARealtimeGameStats.GraphData.eLocation
        class LocationStats(_message.Message):
            __slots__ = ("stats",)
            STATS_FIELD_NUMBER: _ClassVar[int]
            stats: _containers.RepeatedScalarFieldContainer[int]
            def __init__(self, stats: _Optional[_Iterable[int]] = ...) -> None: ...
        class TeamLocationStats(_message.Message):
            __slots__ = ("loc_stats",)
            LOC_STATS_FIELD_NUMBER: _ClassVar[int]
            loc_stats: _containers.RepeatedCompositeFieldContainer[CMsgDOTARealtimeGameStats.GraphData.LocationStats]
            def __init__(self, loc_stats: _Optional[_Iterable[_Union[CMsgDOTARealtimeGameStats.GraphData.LocationStats, _Mapping]]] = ...) -> None: ...
        GRAPH_GOLD_FIELD_NUMBER: _ClassVar[int]
        GRAPH_XP_FIELD_NUMBER: _ClassVar[int]
        GRAPH_KILL_FIELD_NUMBER: _ClassVar[int]
        GRAPH_TOWER_FIELD_NUMBER: _ClassVar[int]
        GRAPH_RAX_FIELD_NUMBER: _ClassVar[int]
        TEAM_LOC_STATS_FIELD_NUMBER: _ClassVar[int]
        graph_gold: _containers.RepeatedScalarFieldContainer[int]
        graph_xp: _containers.RepeatedScalarFieldContainer[int]
        graph_kill: _containers.RepeatedScalarFieldContainer[int]
        graph_tower: _containers.RepeatedScalarFieldContainer[int]
        graph_rax: _containers.RepeatedScalarFieldContainer[int]
        team_loc_stats: _containers.RepeatedCompositeFieldContainer[CMsgDOTARealtimeGameStats.GraphData.TeamLocationStats]
        def __init__(self, graph_gold: _Optional[_Iterable[int]] = ..., graph_xp: _Optional[_Iterable[int]] = ..., graph_kill: _Optional[_Iterable[int]] = ..., graph_tower: _Optional[_Iterable[int]] = ..., graph_rax: _Optional[_Iterable[int]] = ..., team_loc_stats: _Optional[_Iterable[_Union[CMsgDOTARealtimeGameStats.GraphData.TeamLocationStats, _Mapping]]] = ...) -> None: ...
    MATCH_FIELD_NUMBER: _ClassVar[int]
    TEAMS_FIELD_NUMBER: _ClassVar[int]
    BUILDINGS_FIELD_NUMBER: _ClassVar[int]
    GRAPH_DATA_FIELD_NUMBER: _ClassVar[int]
    DELTA_FRAME_FIELD_NUMBER: _ClassVar[int]
    match: CMsgDOTARealtimeGameStats.MatchDetails
    teams: _containers.RepeatedCompositeFieldContainer[CMsgDOTARealtimeGameStats.TeamDetails]
    buildings: _containers.RepeatedCompositeFieldContainer[CMsgDOTARealtimeGameStats.BuildingDetails]
    graph_data: CMsgDOTARealtimeGameStats.GraphData
    delta_frame: bool
    def __init__(self, match: _Optional[_Union[CMsgDOTARealtimeGameStats.MatchDetails, _Mapping]] = ..., teams: _Optional[_Iterable[_Union[CMsgDOTARealtimeGameStats.TeamDetails, _Mapping]]] = ..., buildings: _Optional[_Iterable[_Union[CMsgDOTARealtimeGameStats.BuildingDetails, _Mapping]]] = ..., graph_data: _Optional[_Union[CMsgDOTARealtimeGameStats.GraphData, _Mapping]] = ..., delta_frame: bool = ...) -> None: ...

class CMsgDOTARealtimeGameStatsTerse(_message.Message):
    __slots__ = ("match", "teams", "buildings", "graph_data", "delta_frame")
    class TeamDetails(_message.Message):
        __slots__ = ("team_number", "team_id", "team_name", "team_tag", "team_logo", "score", "net_worth", "team_logo_url", "players")
        TEAM_NUMBER_FIELD_NUMBER: _ClassVar[int]
        TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
        TEAM_TAG_FIELD_NUMBER: _ClassVar[int]
        TEAM_LOGO_FIELD_NUMBER: _ClassVar[int]
        SCORE_FIELD_NUMBER: _ClassVar[int]
        NET_WORTH_FIELD_NUMBER: _ClassVar[int]
        TEAM_LOGO_URL_FIELD_NUMBER: _ClassVar[int]
        PLAYERS_FIELD_NUMBER: _ClassVar[int]
        team_number: int
        team_id: int
        team_name: str
        team_tag: str
        team_logo: int
        score: int
        net_worth: int
        team_logo_url: str
        players: _containers.RepeatedCompositeFieldContainer[CMsgDOTARealtimeGameStatsTerse.PlayerDetails]
        def __init__(self, team_number: _Optional[int] = ..., team_id: _Optional[int] = ..., team_name: _Optional[str] = ..., team_tag: _Optional[str] = ..., team_logo: _Optional[int] = ..., score: _Optional[int] = ..., net_worth: _Optional[int] = ..., team_logo_url: _Optional[str] = ..., players: _Optional[_Iterable[_Union[CMsgDOTARealtimeGameStatsTerse.PlayerDetails, _Mapping]]] = ...) -> None: ...
    class PlayerDetails(_message.Message):
        __slots__ = ("accountid", "playerid", "name", "team", "heroid", "level", "kill_count", "death_count", "assists_count", "denies_count", "lh_count", "gold", "x", "y", "net_worth", "abilities", "items", "team_slot")
        ACCOUNTID_FIELD_NUMBER: _ClassVar[int]
        PLAYERID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        TEAM_FIELD_NUMBER: _ClassVar[int]
        HEROID_FIELD_NUMBER: _ClassVar[int]
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        KILL_COUNT_FIELD_NUMBER: _ClassVar[int]
        DEATH_COUNT_FIELD_NUMBER: _ClassVar[int]
        ASSISTS_COUNT_FIELD_NUMBER: _ClassVar[int]
        DENIES_COUNT_FIELD_NUMBER: _ClassVar[int]
        LH_COUNT_FIELD_NUMBER: _ClassVar[int]
        GOLD_FIELD_NUMBER: _ClassVar[int]
        X_FIELD_NUMBER: _ClassVar[int]
        Y_FIELD_NUMBER: _ClassVar[int]
        NET_WORTH_FIELD_NUMBER: _ClassVar[int]
        ABILITIES_FIELD_NUMBER: _ClassVar[int]
        ITEMS_FIELD_NUMBER: _ClassVar[int]
        TEAM_SLOT_FIELD_NUMBER: _ClassVar[int]
        accountid: int
        playerid: int
        name: str
        team: int
        heroid: int
        level: int
        kill_count: int
        death_count: int
        assists_count: int
        denies_count: int
        lh_count: int
        gold: int
        x: float
        y: float
        net_worth: int
        abilities: _containers.RepeatedScalarFieldContainer[int]
        items: _containers.RepeatedScalarFieldContainer[int]
        team_slot: int
        def __init__(self, accountid: _Optional[int] = ..., playerid: _Optional[int] = ..., name: _Optional[str] = ..., team: _Optional[int] = ..., heroid: _Optional[int] = ..., level: _Optional[int] = ..., kill_count: _Optional[int] = ..., death_count: _Optional[int] = ..., assists_count: _Optional[int] = ..., denies_count: _Optional[int] = ..., lh_count: _Optional[int] = ..., gold: _Optional[int] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., net_worth: _Optional[int] = ..., abilities: _Optional[_Iterable[int]] = ..., items: _Optional[_Iterable[int]] = ..., team_slot: _Optional[int] = ...) -> None: ...
    class BuildingDetails(_message.Message):
        __slots__ = ("team", "heading", "type", "lane", "tier", "x", "y", "destroyed")
        TEAM_FIELD_NUMBER: _ClassVar[int]
        HEADING_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        LANE_FIELD_NUMBER: _ClassVar[int]
        TIER_FIELD_NUMBER: _ClassVar[int]
        X_FIELD_NUMBER: _ClassVar[int]
        Y_FIELD_NUMBER: _ClassVar[int]
        DESTROYED_FIELD_NUMBER: _ClassVar[int]
        team: int
        heading: float
        type: int
        lane: int
        tier: int
        x: float
        y: float
        destroyed: bool
        def __init__(self, team: _Optional[int] = ..., heading: _Optional[float] = ..., type: _Optional[int] = ..., lane: _Optional[int] = ..., tier: _Optional[int] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., destroyed: bool = ...) -> None: ...
    class PickBanDetails(_message.Message):
        __slots__ = ("hero", "team")
        HERO_FIELD_NUMBER: _ClassVar[int]
        TEAM_FIELD_NUMBER: _ClassVar[int]
        hero: int
        team: int
        def __init__(self, hero: _Optional[int] = ..., team: _Optional[int] = ...) -> None: ...
    class MatchDetails(_message.Message):
        __slots__ = ("server_steam_id", "match_id", "timestamp", "game_time", "steam_broadcaster_account_ids", "game_mode", "league_id", "league_node_id", "game_state", "picks", "bans", "lobby_type", "start_timestamp", "is_player_draft")
        SERVER_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
        MATCH_ID_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        GAME_TIME_FIELD_NUMBER: _ClassVar[int]
        STEAM_BROADCASTER_ACCOUNT_IDS_FIELD_NUMBER: _ClassVar[int]
        GAME_MODE_FIELD_NUMBER: _ClassVar[int]
        LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
        LEAGUE_NODE_ID_FIELD_NUMBER: _ClassVar[int]
        GAME_STATE_FIELD_NUMBER: _ClassVar[int]
        PICKS_FIELD_NUMBER: _ClassVar[int]
        BANS_FIELD_NUMBER: _ClassVar[int]
        LOBBY_TYPE_FIELD_NUMBER: _ClassVar[int]
        START_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        IS_PLAYER_DRAFT_FIELD_NUMBER: _ClassVar[int]
        server_steam_id: int
        match_id: int
        timestamp: int
        game_time: int
        steam_broadcaster_account_ids: _containers.RepeatedScalarFieldContainer[int]
        game_mode: int
        league_id: int
        league_node_id: int
        game_state: int
        picks: _containers.RepeatedCompositeFieldContainer[CMsgDOTARealtimeGameStatsTerse.PickBanDetails]
        bans: _containers.RepeatedCompositeFieldContainer[CMsgDOTARealtimeGameStatsTerse.PickBanDetails]
        lobby_type: int
        start_timestamp: int
        is_player_draft: bool
        def __init__(self, server_steam_id: _Optional[int] = ..., match_id: _Optional[int] = ..., timestamp: _Optional[int] = ..., game_time: _Optional[int] = ..., steam_broadcaster_account_ids: _Optional[_Iterable[int]] = ..., game_mode: _Optional[int] = ..., league_id: _Optional[int] = ..., league_node_id: _Optional[int] = ..., game_state: _Optional[int] = ..., picks: _Optional[_Iterable[_Union[CMsgDOTARealtimeGameStatsTerse.PickBanDetails, _Mapping]]] = ..., bans: _Optional[_Iterable[_Union[CMsgDOTARealtimeGameStatsTerse.PickBanDetails, _Mapping]]] = ..., lobby_type: _Optional[int] = ..., start_timestamp: _Optional[int] = ..., is_player_draft: bool = ...) -> None: ...
    class GraphData(_message.Message):
        __slots__ = ("graph_gold",)
        GRAPH_GOLD_FIELD_NUMBER: _ClassVar[int]
        graph_gold: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, graph_gold: _Optional[_Iterable[int]] = ...) -> None: ...
    MATCH_FIELD_NUMBER: _ClassVar[int]
    TEAMS_FIELD_NUMBER: _ClassVar[int]
    BUILDINGS_FIELD_NUMBER: _ClassVar[int]
    GRAPH_DATA_FIELD_NUMBER: _ClassVar[int]
    DELTA_FRAME_FIELD_NUMBER: _ClassVar[int]
    match: CMsgDOTARealtimeGameStatsTerse.MatchDetails
    teams: _containers.RepeatedCompositeFieldContainer[CMsgDOTARealtimeGameStatsTerse.TeamDetails]
    buildings: _containers.RepeatedCompositeFieldContainer[CMsgDOTARealtimeGameStatsTerse.BuildingDetails]
    graph_data: CMsgDOTARealtimeGameStatsTerse.GraphData
    delta_frame: bool
    def __init__(self, match: _Optional[_Union[CMsgDOTARealtimeGameStatsTerse.MatchDetails, _Mapping]] = ..., teams: _Optional[_Iterable[_Union[CMsgDOTARealtimeGameStatsTerse.TeamDetails, _Mapping]]] = ..., buildings: _Optional[_Iterable[_Union[CMsgDOTARealtimeGameStatsTerse.BuildingDetails, _Mapping]]] = ..., graph_data: _Optional[_Union[CMsgDOTARealtimeGameStatsTerse.GraphData, _Mapping]] = ..., delta_frame: bool = ...) -> None: ...

class CMsgDOTABroadcastTimelineEvent(_message.Message):
    __slots__ = ("event", "timestamp", "data", "string_data")
    EVENT_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    STRING_DATA_FIELD_NUMBER: _ClassVar[int]
    event: EBroadcastTimelineEvent
    timestamp: int
    data: int
    string_data: str
    def __init__(self, event: _Optional[_Union[EBroadcastTimelineEvent, str]] = ..., timestamp: _Optional[int] = ..., data: _Optional[int] = ..., string_data: _Optional[str] = ...) -> None: ...

class CMsgGCToClientMatchGroupsVersion(_message.Message):
    __slots__ = ("matchgroups_version",)
    MATCHGROUPS_VERSION_FIELD_NUMBER: _ClassVar[int]
    matchgroups_version: int
    def __init__(self, matchgroups_version: _Optional[int] = ...) -> None: ...

class CMsgDOTASDOHeroStatsHistory(_message.Message):
    __slots__ = ("match_id", "game_mode", "lobby_type", "start_time", "won", "gpm", "xpm", "kills", "deaths", "assists")
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    GAME_MODE_FIELD_NUMBER: _ClassVar[int]
    LOBBY_TYPE_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    WON_FIELD_NUMBER: _ClassVar[int]
    GPM_FIELD_NUMBER: _ClassVar[int]
    XPM_FIELD_NUMBER: _ClassVar[int]
    KILLS_FIELD_NUMBER: _ClassVar[int]
    DEATHS_FIELD_NUMBER: _ClassVar[int]
    ASSISTS_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    game_mode: int
    lobby_type: int
    start_time: int
    won: bool
    gpm: int
    xpm: int
    kills: int
    deaths: int
    assists: int
    def __init__(self, match_id: _Optional[int] = ..., game_mode: _Optional[int] = ..., lobby_type: _Optional[int] = ..., start_time: _Optional[int] = ..., won: bool = ..., gpm: _Optional[int] = ..., xpm: _Optional[int] = ..., kills: _Optional[int] = ..., deaths: _Optional[int] = ..., assists: _Optional[int] = ...) -> None: ...

class CMsgPredictionChoice(_message.Message):
    __slots__ = ("value", "name", "min_raw_value", "max_raw_value")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MIN_RAW_VALUE_FIELD_NUMBER: _ClassVar[int]
    MAX_RAW_VALUE_FIELD_NUMBER: _ClassVar[int]
    value: int
    name: str
    min_raw_value: int
    max_raw_value: int
    def __init__(self, value: _Optional[int] = ..., name: _Optional[str] = ..., min_raw_value: _Optional[int] = ..., max_raw_value: _Optional[int] = ...) -> None: ...

class CMsgInGamePrediction(_message.Message):
    __slots__ = ("id", "name", "type", "group", "question", "choices", "required_heroes", "query_name", "query_values", "answer_resolution_type", "points_to_grant", "reward_action", "debug_force_selection", "raw_value_type")
    class ERawValueType_t(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        Number: _ClassVar[CMsgInGamePrediction.ERawValueType_t]
        Time: _ClassVar[CMsgInGamePrediction.ERawValueType_t]
    Number: CMsgInGamePrediction.ERawValueType_t
    Time: CMsgInGamePrediction.ERawValueType_t
    class EPredictionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        Generic: _ClassVar[CMsgInGamePrediction.EPredictionType]
        Hero: _ClassVar[CMsgInGamePrediction.EPredictionType]
        Team: _ClassVar[CMsgInGamePrediction.EPredictionType]
        Player: _ClassVar[CMsgInGamePrediction.EPredictionType]
        Special: _ClassVar[CMsgInGamePrediction.EPredictionType]
        YesNo: _ClassVar[CMsgInGamePrediction.EPredictionType]
        QualifiersTeam: _ClassVar[CMsgInGamePrediction.EPredictionType]
    Generic: CMsgInGamePrediction.EPredictionType
    Hero: CMsgInGamePrediction.EPredictionType
    Team: CMsgInGamePrediction.EPredictionType
    Player: CMsgInGamePrediction.EPredictionType
    Special: CMsgInGamePrediction.EPredictionType
    YesNo: CMsgInGamePrediction.EPredictionType
    QualifiersTeam: CMsgInGamePrediction.EPredictionType
    class EResolutionType_t(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        InvalidQuery: _ClassVar[CMsgInGamePrediction.EResolutionType_t]
        FirstToPassQuery: _ClassVar[CMsgInGamePrediction.EResolutionType_t]
        LastToPassQuery: _ClassVar[CMsgInGamePrediction.EResolutionType_t]
        LastRemainingQuery: _ClassVar[CMsgInGamePrediction.EResolutionType_t]
        MaxToPassQuery: _ClassVar[CMsgInGamePrediction.EResolutionType_t]
        MinToPassQuery: _ClassVar[CMsgInGamePrediction.EResolutionType_t]
        SumQuery: _ClassVar[CMsgInGamePrediction.EResolutionType_t]
        MaxTeamSumToPassQuery: _ClassVar[CMsgInGamePrediction.EResolutionType_t]
        MinTeamSumToPassQuery: _ClassVar[CMsgInGamePrediction.EResolutionType_t]
    InvalidQuery: CMsgInGamePrediction.EResolutionType_t
    FirstToPassQuery: CMsgInGamePrediction.EResolutionType_t
    LastToPassQuery: CMsgInGamePrediction.EResolutionType_t
    LastRemainingQuery: CMsgInGamePrediction.EResolutionType_t
    MaxToPassQuery: CMsgInGamePrediction.EResolutionType_t
    MinToPassQuery: CMsgInGamePrediction.EResolutionType_t
    SumQuery: CMsgInGamePrediction.EResolutionType_t
    MaxTeamSumToPassQuery: CMsgInGamePrediction.EResolutionType_t
    MinTeamSumToPassQuery: CMsgInGamePrediction.EResolutionType_t
    class ERandomSelectionGroup_t(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        EarlyGame: _ClassVar[CMsgInGamePrediction.ERandomSelectionGroup_t]
        MidGame: _ClassVar[CMsgInGamePrediction.ERandomSelectionGroup_t]
        LateGame: _ClassVar[CMsgInGamePrediction.ERandomSelectionGroup_t]
        Count: _ClassVar[CMsgInGamePrediction.ERandomSelectionGroup_t]
    EarlyGame: CMsgInGamePrediction.ERandomSelectionGroup_t
    MidGame: CMsgInGamePrediction.ERandomSelectionGroup_t
    LateGame: CMsgInGamePrediction.ERandomSelectionGroup_t
    Count: CMsgInGamePrediction.ERandomSelectionGroup_t
    class QueryKeyValues(_message.Message):
        __slots__ = ("name", "value")
        NAME_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        name: str
        value: str
        def __init__(self, name: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    QUESTION_FIELD_NUMBER: _ClassVar[int]
    CHOICES_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_HEROES_FIELD_NUMBER: _ClassVar[int]
    QUERY_NAME_FIELD_NUMBER: _ClassVar[int]
    QUERY_VALUES_FIELD_NUMBER: _ClassVar[int]
    ANSWER_RESOLUTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    POINTS_TO_GRANT_FIELD_NUMBER: _ClassVar[int]
    REWARD_ACTION_FIELD_NUMBER: _ClassVar[int]
    DEBUG_FORCE_SELECTION_FIELD_NUMBER: _ClassVar[int]
    RAW_VALUE_TYPE_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    type: CMsgInGamePrediction.EPredictionType
    group: CMsgInGamePrediction.ERandomSelectionGroup_t
    question: str
    choices: _containers.RepeatedCompositeFieldContainer[CMsgPredictionChoice]
    required_heroes: _containers.RepeatedScalarFieldContainer[str]
    query_name: str
    query_values: _containers.RepeatedCompositeFieldContainer[CMsgInGamePrediction.QueryKeyValues]
    answer_resolution_type: CMsgInGamePrediction.EResolutionType_t
    points_to_grant: int
    reward_action: int
    debug_force_selection: int
    raw_value_type: CMsgInGamePrediction.ERawValueType_t
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., type: _Optional[_Union[CMsgInGamePrediction.EPredictionType, str]] = ..., group: _Optional[_Union[CMsgInGamePrediction.ERandomSelectionGroup_t, str]] = ..., question: _Optional[str] = ..., choices: _Optional[_Iterable[_Union[CMsgPredictionChoice, _Mapping]]] = ..., required_heroes: _Optional[_Iterable[str]] = ..., query_name: _Optional[str] = ..., query_values: _Optional[_Iterable[_Union[CMsgInGamePrediction.QueryKeyValues, _Mapping]]] = ..., answer_resolution_type: _Optional[_Union[CMsgInGamePrediction.EResolutionType_t, str]] = ..., points_to_grant: _Optional[int] = ..., reward_action: _Optional[int] = ..., debug_force_selection: _Optional[int] = ..., raw_value_type: _Optional[_Union[CMsgInGamePrediction.ERawValueType_t, str]] = ...) -> None: ...

class CMsgDOTASeasonPredictions(_message.Message):
    __slots__ = ("predictions", "in_game_predictions", "in_game_prediction_count_per_game", "in_game_prediction_voting_period_minutes")
    class Prediction(_message.Message):
        __slots__ = ("type", "question", "choices", "selection_id", "start_date", "lock_date", "reward", "answer_type", "answer_id", "answers", "query_name", "lock_on_selection_id", "lock_on_selection_value", "lock_on_selection_set", "use_answer_value_ranges", "region", "phases", "reward_event", "league_node_id", "reward_event_action")
        class EPredictionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            Generic: _ClassVar[CMsgDOTASeasonPredictions.Prediction.EPredictionType]
            Hero: _ClassVar[CMsgDOTASeasonPredictions.Prediction.EPredictionType]
            Team: _ClassVar[CMsgDOTASeasonPredictions.Prediction.EPredictionType]
            Player: _ClassVar[CMsgDOTASeasonPredictions.Prediction.EPredictionType]
            Special: _ClassVar[CMsgDOTASeasonPredictions.Prediction.EPredictionType]
            YesNo: _ClassVar[CMsgDOTASeasonPredictions.Prediction.EPredictionType]
            QualifiersTeam: _ClassVar[CMsgDOTASeasonPredictions.Prediction.EPredictionType]
            LastChanceTeam: _ClassVar[CMsgDOTASeasonPredictions.Prediction.EPredictionType]
        Generic: CMsgDOTASeasonPredictions.Prediction.EPredictionType
        Hero: CMsgDOTASeasonPredictions.Prediction.EPredictionType
        Team: CMsgDOTASeasonPredictions.Prediction.EPredictionType
        Player: CMsgDOTASeasonPredictions.Prediction.EPredictionType
        Special: CMsgDOTASeasonPredictions.Prediction.EPredictionType
        YesNo: CMsgDOTASeasonPredictions.Prediction.EPredictionType
        QualifiersTeam: CMsgDOTASeasonPredictions.Prediction.EPredictionType
        LastChanceTeam: CMsgDOTASeasonPredictions.Prediction.EPredictionType
        class EAnswerType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            SingleInt: _ClassVar[CMsgDOTASeasonPredictions.Prediction.EAnswerType]
            SingleFloat: _ClassVar[CMsgDOTASeasonPredictions.Prediction.EAnswerType]
            MultipleInt: _ClassVar[CMsgDOTASeasonPredictions.Prediction.EAnswerType]
            MultipleFloat: _ClassVar[CMsgDOTASeasonPredictions.Prediction.EAnswerType]
            AnswerTeam: _ClassVar[CMsgDOTASeasonPredictions.Prediction.EAnswerType]
            SingleTime: _ClassVar[CMsgDOTASeasonPredictions.Prediction.EAnswerType]
            MultipleTime: _ClassVar[CMsgDOTASeasonPredictions.Prediction.EAnswerType]
            NoAnswer: _ClassVar[CMsgDOTASeasonPredictions.Prediction.EAnswerType]
        SingleInt: CMsgDOTASeasonPredictions.Prediction.EAnswerType
        SingleFloat: CMsgDOTASeasonPredictions.Prediction.EAnswerType
        MultipleInt: CMsgDOTASeasonPredictions.Prediction.EAnswerType
        MultipleFloat: CMsgDOTASeasonPredictions.Prediction.EAnswerType
        AnswerTeam: CMsgDOTASeasonPredictions.Prediction.EAnswerType
        SingleTime: CMsgDOTASeasonPredictions.Prediction.EAnswerType
        MultipleTime: CMsgDOTASeasonPredictions.Prediction.EAnswerType
        NoAnswer: CMsgDOTASeasonPredictions.Prediction.EAnswerType
        class Answers(_message.Message):
            __slots__ = ("answer_id",)
            ANSWER_ID_FIELD_NUMBER: _ClassVar[int]
            answer_id: int
            def __init__(self, answer_id: _Optional[int] = ...) -> None: ...
        TYPE_FIELD_NUMBER: _ClassVar[int]
        QUESTION_FIELD_NUMBER: _ClassVar[int]
        CHOICES_FIELD_NUMBER: _ClassVar[int]
        SELECTION_ID_FIELD_NUMBER: _ClassVar[int]
        START_DATE_FIELD_NUMBER: _ClassVar[int]
        LOCK_DATE_FIELD_NUMBER: _ClassVar[int]
        REWARD_FIELD_NUMBER: _ClassVar[int]
        ANSWER_TYPE_FIELD_NUMBER: _ClassVar[int]
        ANSWER_ID_FIELD_NUMBER: _ClassVar[int]
        ANSWERS_FIELD_NUMBER: _ClassVar[int]
        QUERY_NAME_FIELD_NUMBER: _ClassVar[int]
        LOCK_ON_SELECTION_ID_FIELD_NUMBER: _ClassVar[int]
        LOCK_ON_SELECTION_VALUE_FIELD_NUMBER: _ClassVar[int]
        LOCK_ON_SELECTION_SET_FIELD_NUMBER: _ClassVar[int]
        USE_ANSWER_VALUE_RANGES_FIELD_NUMBER: _ClassVar[int]
        REGION_FIELD_NUMBER: _ClassVar[int]
        PHASES_FIELD_NUMBER: _ClassVar[int]
        REWARD_EVENT_FIELD_NUMBER: _ClassVar[int]
        LEAGUE_NODE_ID_FIELD_NUMBER: _ClassVar[int]
        REWARD_EVENT_ACTION_FIELD_NUMBER: _ClassVar[int]
        type: CMsgDOTASeasonPredictions.Prediction.EPredictionType
        question: str
        choices: _containers.RepeatedCompositeFieldContainer[CMsgPredictionChoice]
        selection_id: int
        start_date: int
        lock_date: int
        reward: int
        answer_type: CMsgDOTASeasonPredictions.Prediction.EAnswerType
        answer_id: int
        answers: _containers.RepeatedCompositeFieldContainer[CMsgDOTASeasonPredictions.Prediction.Answers]
        query_name: str
        lock_on_selection_id: int
        lock_on_selection_value: int
        lock_on_selection_set: bool
        use_answer_value_ranges: bool
        region: _dota_shared_enums_pb2.ELeagueRegion
        phases: _containers.RepeatedScalarFieldContainer[_dota_shared_enums_pb2.ELeaguePhase]
        reward_event: _dota_shared_enums_pb2.EEvent
        league_node_id: int
        reward_event_action: str
        def __init__(self, type: _Optional[_Union[CMsgDOTASeasonPredictions.Prediction.EPredictionType, str]] = ..., question: _Optional[str] = ..., choices: _Optional[_Iterable[_Union[CMsgPredictionChoice, _Mapping]]] = ..., selection_id: _Optional[int] = ..., start_date: _Optional[int] = ..., lock_date: _Optional[int] = ..., reward: _Optional[int] = ..., answer_type: _Optional[_Union[CMsgDOTASeasonPredictions.Prediction.EAnswerType, str]] = ..., answer_id: _Optional[int] = ..., answers: _Optional[_Iterable[_Union[CMsgDOTASeasonPredictions.Prediction.Answers, _Mapping]]] = ..., query_name: _Optional[str] = ..., lock_on_selection_id: _Optional[int] = ..., lock_on_selection_value: _Optional[int] = ..., lock_on_selection_set: bool = ..., use_answer_value_ranges: bool = ..., region: _Optional[_Union[_dota_shared_enums_pb2.ELeagueRegion, str]] = ..., phases: _Optional[_Iterable[_Union[_dota_shared_enums_pb2.ELeaguePhase, str]]] = ..., reward_event: _Optional[_Union[_dota_shared_enums_pb2.EEvent, str]] = ..., league_node_id: _Optional[int] = ..., reward_event_action: _Optional[str] = ...) -> None: ...
    PREDICTIONS_FIELD_NUMBER: _ClassVar[int]
    IN_GAME_PREDICTIONS_FIELD_NUMBER: _ClassVar[int]
    IN_GAME_PREDICTION_COUNT_PER_GAME_FIELD_NUMBER: _ClassVar[int]
    IN_GAME_PREDICTION_VOTING_PERIOD_MINUTES_FIELD_NUMBER: _ClassVar[int]
    predictions: _containers.RepeatedCompositeFieldContainer[CMsgDOTASeasonPredictions.Prediction]
    in_game_predictions: _containers.RepeatedCompositeFieldContainer[CMsgInGamePrediction]
    in_game_prediction_count_per_game: int
    in_game_prediction_voting_period_minutes: int
    def __init__(self, predictions: _Optional[_Iterable[_Union[CMsgDOTASeasonPredictions.Prediction, _Mapping]]] = ..., in_game_predictions: _Optional[_Iterable[_Union[CMsgInGamePrediction, _Mapping]]] = ..., in_game_prediction_count_per_game: _Optional[int] = ..., in_game_prediction_voting_period_minutes: _Optional[int] = ...) -> None: ...

class CMsgAvailablePredictions(_message.Message):
    __slots__ = ("match_predictions",)
    class MatchPrediction(_message.Message):
        __slots__ = ("match_id", "predictions")
        MATCH_ID_FIELD_NUMBER: _ClassVar[int]
        PREDICTIONS_FIELD_NUMBER: _ClassVar[int]
        match_id: int
        predictions: _containers.RepeatedCompositeFieldContainer[CMsgInGamePrediction]
        def __init__(self, match_id: _Optional[int] = ..., predictions: _Optional[_Iterable[_Union[CMsgInGamePrediction, _Mapping]]] = ...) -> None: ...
    MATCH_PREDICTIONS_FIELD_NUMBER: _ClassVar[int]
    match_predictions: _containers.RepeatedCompositeFieldContainer[CMsgAvailablePredictions.MatchPrediction]
    def __init__(self, match_predictions: _Optional[_Iterable[_Union[CMsgAvailablePredictions.MatchPrediction, _Mapping]]] = ...) -> None: ...

class CMsgLeagueWatchedGames(_message.Message):
    __slots__ = ("leagues",)
    class Series(_message.Message):
        __slots__ = ("node_id", "game")
        NODE_ID_FIELD_NUMBER: _ClassVar[int]
        GAME_FIELD_NUMBER: _ClassVar[int]
        node_id: int
        game: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, node_id: _Optional[int] = ..., game: _Optional[_Iterable[int]] = ...) -> None: ...
    class League(_message.Message):
        __slots__ = ("league_id", "series")
        LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
        SERIES_FIELD_NUMBER: _ClassVar[int]
        league_id: int
        series: _containers.RepeatedCompositeFieldContainer[CMsgLeagueWatchedGames.Series]
        def __init__(self, league_id: _Optional[int] = ..., series: _Optional[_Iterable[_Union[CMsgLeagueWatchedGames.Series, _Mapping]]] = ...) -> None: ...
    LEAGUES_FIELD_NUMBER: _ClassVar[int]
    leagues: _containers.RepeatedCompositeFieldContainer[CMsgLeagueWatchedGames.League]
    def __init__(self, leagues: _Optional[_Iterable[_Union[CMsgLeagueWatchedGames.League, _Mapping]]] = ...) -> None: ...

class CMsgDOTAMatch(_message.Message):
    __slots__ = ("duration", "starttime", "players", "match_id", "tower_status", "barracks_status", "cluster", "first_blood_time", "replay_salt", "server_ip", "server_port", "lobby_type", "human_players", "average_skill", "game_balance", "radiant_team_id", "dire_team_id", "leagueid", "radiant_team_name", "dire_team_name", "radiant_team_logo", "dire_team_logo", "radiant_team_logo_url", "dire_team_logo_url", "radiant_team_complete", "dire_team_complete", "game_mode", "picks_bans", "match_seq_num", "replay_state", "radiant_guild_id", "dire_guild_id", "radiant_team_tag", "dire_team_tag", "series_id", "series_type", "broadcaster_channels", "engine", "custom_game_data", "match_flags", "private_metadata_key", "radiant_team_score", "dire_team_score", "match_outcome", "tournament_id", "tournament_round", "pre_game_duration", "coaches")
    class ReplayState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        REPLAY_AVAILABLE: _ClassVar[CMsgDOTAMatch.ReplayState]
        REPLAY_NOT_RECORDED: _ClassVar[CMsgDOTAMatch.ReplayState]
        REPLAY_EXPIRED: _ClassVar[CMsgDOTAMatch.ReplayState]
    REPLAY_AVAILABLE: CMsgDOTAMatch.ReplayState
    REPLAY_NOT_RECORDED: CMsgDOTAMatch.ReplayState
    REPLAY_EXPIRED: CMsgDOTAMatch.ReplayState
    class Player(_message.Message):
        __slots__ = ("account_id", "player_slot", "hero_id", "item_0", "item_1", "item_2", "item_3", "item_4", "item_5", "item_6", "item_7", "item_8", "item_9", "item_10", "item_10_lvl", "expected_team_contribution", "scaled_metric", "previous_rank", "rank_change", "mmr_type", "kills", "deaths", "assists", "leaver_status", "gold", "last_hits", "denies", "gold_per_min", "xp_per_min", "gold_spent", "hero_damage", "tower_damage", "hero_healing", "disable_duration", "level", "time_last_seen", "player_name", "support_ability_value", "feeding_detected", "search_rank", "search_rank_uncertainty", "rank_uncertainty_change", "hero_play_count", "party_id", "scaled_hero_damage", "scaled_tower_damage", "scaled_hero_healing", "scaled_kills", "scaled_deaths", "scaled_assists", "claimed_farm_gold", "support_gold", "claimed_denies", "claimed_misses", "misses", "ability_upgrades", "additional_units_inventory", "permanent_buffs", "pro_name", "real_name", "custom_game_data", "active_plus_subscription", "net_worth", "bot_difficulty", "hero_pick_order", "hero_was_randomed", "hero_was_dota_plus_suggestion", "hero_damage_received", "hero_damage_dealt", "seconds_dead", "gold_lost_to_death", "lane_selection_flags", "bounty_runes", "outposts_captured", "team_number", "team_slot", "selected_facet")
        class HeroDamageType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            HERO_DAMAGE_PHYSICAL: _ClassVar[CMsgDOTAMatch.Player.HeroDamageType]
            HERO_DAMAGE_MAGICAL: _ClassVar[CMsgDOTAMatch.Player.HeroDamageType]
            HERO_DAMAGE_PURE: _ClassVar[CMsgDOTAMatch.Player.HeroDamageType]
        HERO_DAMAGE_PHYSICAL: CMsgDOTAMatch.Player.HeroDamageType
        HERO_DAMAGE_MAGICAL: CMsgDOTAMatch.Player.HeroDamageType
        HERO_DAMAGE_PURE: CMsgDOTAMatch.Player.HeroDamageType
        class CustomGameData(_message.Message):
            __slots__ = ("dota_team", "winner")
            DOTA_TEAM_FIELD_NUMBER: _ClassVar[int]
            WINNER_FIELD_NUMBER: _ClassVar[int]
            dota_team: int
            winner: bool
            def __init__(self, dota_team: _Optional[int] = ..., winner: bool = ...) -> None: ...
        class HeroDamageReceived(_message.Message):
            __slots__ = ("pre_reduction", "post_reduction", "damage_type")
            PRE_REDUCTION_FIELD_NUMBER: _ClassVar[int]
            POST_REDUCTION_FIELD_NUMBER: _ClassVar[int]
            DAMAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
            pre_reduction: int
            post_reduction: int
            damage_type: CMsgDOTAMatch.Player.HeroDamageType
            def __init__(self, pre_reduction: _Optional[int] = ..., post_reduction: _Optional[int] = ..., damage_type: _Optional[_Union[CMsgDOTAMatch.Player.HeroDamageType, str]] = ...) -> None: ...
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        ITEM_0_FIELD_NUMBER: _ClassVar[int]
        ITEM_1_FIELD_NUMBER: _ClassVar[int]
        ITEM_2_FIELD_NUMBER: _ClassVar[int]
        ITEM_3_FIELD_NUMBER: _ClassVar[int]
        ITEM_4_FIELD_NUMBER: _ClassVar[int]
        ITEM_5_FIELD_NUMBER: _ClassVar[int]
        ITEM_6_FIELD_NUMBER: _ClassVar[int]
        ITEM_7_FIELD_NUMBER: _ClassVar[int]
        ITEM_8_FIELD_NUMBER: _ClassVar[int]
        ITEM_9_FIELD_NUMBER: _ClassVar[int]
        ITEM_10_FIELD_NUMBER: _ClassVar[int]
        ITEM_10_LVL_FIELD_NUMBER: _ClassVar[int]
        EXPECTED_TEAM_CONTRIBUTION_FIELD_NUMBER: _ClassVar[int]
        SCALED_METRIC_FIELD_NUMBER: _ClassVar[int]
        PREVIOUS_RANK_FIELD_NUMBER: _ClassVar[int]
        RANK_CHANGE_FIELD_NUMBER: _ClassVar[int]
        MMR_TYPE_FIELD_NUMBER: _ClassVar[int]
        KILLS_FIELD_NUMBER: _ClassVar[int]
        DEATHS_FIELD_NUMBER: _ClassVar[int]
        ASSISTS_FIELD_NUMBER: _ClassVar[int]
        LEAVER_STATUS_FIELD_NUMBER: _ClassVar[int]
        GOLD_FIELD_NUMBER: _ClassVar[int]
        LAST_HITS_FIELD_NUMBER: _ClassVar[int]
        DENIES_FIELD_NUMBER: _ClassVar[int]
        GOLD_PER_MIN_FIELD_NUMBER: _ClassVar[int]
        XP_PER_MIN_FIELD_NUMBER: _ClassVar[int]
        GOLD_SPENT_FIELD_NUMBER: _ClassVar[int]
        HERO_DAMAGE_FIELD_NUMBER: _ClassVar[int]
        TOWER_DAMAGE_FIELD_NUMBER: _ClassVar[int]
        HERO_HEALING_FIELD_NUMBER: _ClassVar[int]
        DISABLE_DURATION_FIELD_NUMBER: _ClassVar[int]
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        TIME_LAST_SEEN_FIELD_NUMBER: _ClassVar[int]
        PLAYER_NAME_FIELD_NUMBER: _ClassVar[int]
        SUPPORT_ABILITY_VALUE_FIELD_NUMBER: _ClassVar[int]
        FEEDING_DETECTED_FIELD_NUMBER: _ClassVar[int]
        SEARCH_RANK_FIELD_NUMBER: _ClassVar[int]
        SEARCH_RANK_UNCERTAINTY_FIELD_NUMBER: _ClassVar[int]
        RANK_UNCERTAINTY_CHANGE_FIELD_NUMBER: _ClassVar[int]
        HERO_PLAY_COUNT_FIELD_NUMBER: _ClassVar[int]
        PARTY_ID_FIELD_NUMBER: _ClassVar[int]
        SCALED_HERO_DAMAGE_FIELD_NUMBER: _ClassVar[int]
        SCALED_TOWER_DAMAGE_FIELD_NUMBER: _ClassVar[int]
        SCALED_HERO_HEALING_FIELD_NUMBER: _ClassVar[int]
        SCALED_KILLS_FIELD_NUMBER: _ClassVar[int]
        SCALED_DEATHS_FIELD_NUMBER: _ClassVar[int]
        SCALED_ASSISTS_FIELD_NUMBER: _ClassVar[int]
        CLAIMED_FARM_GOLD_FIELD_NUMBER: _ClassVar[int]
        SUPPORT_GOLD_FIELD_NUMBER: _ClassVar[int]
        CLAIMED_DENIES_FIELD_NUMBER: _ClassVar[int]
        CLAIMED_MISSES_FIELD_NUMBER: _ClassVar[int]
        MISSES_FIELD_NUMBER: _ClassVar[int]
        ABILITY_UPGRADES_FIELD_NUMBER: _ClassVar[int]
        ADDITIONAL_UNITS_INVENTORY_FIELD_NUMBER: _ClassVar[int]
        PERMANENT_BUFFS_FIELD_NUMBER: _ClassVar[int]
        PRO_NAME_FIELD_NUMBER: _ClassVar[int]
        REAL_NAME_FIELD_NUMBER: _ClassVar[int]
        CUSTOM_GAME_DATA_FIELD_NUMBER: _ClassVar[int]
        ACTIVE_PLUS_SUBSCRIPTION_FIELD_NUMBER: _ClassVar[int]
        NET_WORTH_FIELD_NUMBER: _ClassVar[int]
        BOT_DIFFICULTY_FIELD_NUMBER: _ClassVar[int]
        HERO_PICK_ORDER_FIELD_NUMBER: _ClassVar[int]
        HERO_WAS_RANDOMED_FIELD_NUMBER: _ClassVar[int]
        HERO_WAS_DOTA_PLUS_SUGGESTION_FIELD_NUMBER: _ClassVar[int]
        HERO_DAMAGE_RECEIVED_FIELD_NUMBER: _ClassVar[int]
        HERO_DAMAGE_DEALT_FIELD_NUMBER: _ClassVar[int]
        SECONDS_DEAD_FIELD_NUMBER: _ClassVar[int]
        GOLD_LOST_TO_DEATH_FIELD_NUMBER: _ClassVar[int]
        LANE_SELECTION_FLAGS_FIELD_NUMBER: _ClassVar[int]
        BOUNTY_RUNES_FIELD_NUMBER: _ClassVar[int]
        OUTPOSTS_CAPTURED_FIELD_NUMBER: _ClassVar[int]
        TEAM_NUMBER_FIELD_NUMBER: _ClassVar[int]
        TEAM_SLOT_FIELD_NUMBER: _ClassVar[int]
        SELECTED_FACET_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        player_slot: int
        hero_id: int
        item_0: int
        item_1: int
        item_2: int
        item_3: int
        item_4: int
        item_5: int
        item_6: int
        item_7: int
        item_8: int
        item_9: int
        item_10: int
        item_10_lvl: int
        expected_team_contribution: float
        scaled_metric: float
        previous_rank: int
        rank_change: int
        mmr_type: int
        kills: int
        deaths: int
        assists: int
        leaver_status: int
        gold: int
        last_hits: int
        denies: int
        gold_per_min: int
        xp_per_min: int
        gold_spent: int
        hero_damage: int
        tower_damage: int
        hero_healing: int
        disable_duration: int
        level: int
        time_last_seen: int
        player_name: str
        support_ability_value: int
        feeding_detected: bool
        search_rank: int
        search_rank_uncertainty: int
        rank_uncertainty_change: int
        hero_play_count: int
        party_id: int
        scaled_hero_damage: int
        scaled_tower_damage: int
        scaled_hero_healing: int
        scaled_kills: float
        scaled_deaths: float
        scaled_assists: float
        claimed_farm_gold: int
        support_gold: int
        claimed_denies: int
        claimed_misses: int
        misses: int
        ability_upgrades: _containers.RepeatedCompositeFieldContainer[CMatchPlayerAbilityUpgrade]
        additional_units_inventory: _containers.RepeatedCompositeFieldContainer[CMatchAdditionalUnitInventory]
        permanent_buffs: _containers.RepeatedCompositeFieldContainer[CMatchPlayerPermanentBuff]
        pro_name: str
        real_name: str
        custom_game_data: CMsgDOTAMatch.Player.CustomGameData
        active_plus_subscription: bool
        net_worth: int
        bot_difficulty: int
        hero_pick_order: int
        hero_was_randomed: bool
        hero_was_dota_plus_suggestion: bool
        hero_damage_received: _containers.RepeatedCompositeFieldContainer[CMsgDOTAMatch.Player.HeroDamageReceived]
        hero_damage_dealt: _containers.RepeatedCompositeFieldContainer[CMsgDOTAMatch.Player.HeroDamageReceived]
        seconds_dead: int
        gold_lost_to_death: int
        lane_selection_flags: int
        bounty_runes: int
        outposts_captured: int
        team_number: _dota_shared_enums_pb2.DOTA_GC_TEAM
        team_slot: int
        selected_facet: int
        def __init__(self, account_id: _Optional[int] = ..., player_slot: _Optional[int] = ..., hero_id: _Optional[int] = ..., item_0: _Optional[int] = ..., item_1: _Optional[int] = ..., item_2: _Optional[int] = ..., item_3: _Optional[int] = ..., item_4: _Optional[int] = ..., item_5: _Optional[int] = ..., item_6: _Optional[int] = ..., item_7: _Optional[int] = ..., item_8: _Optional[int] = ..., item_9: _Optional[int] = ..., item_10: _Optional[int] = ..., item_10_lvl: _Optional[int] = ..., expected_team_contribution: _Optional[float] = ..., scaled_metric: _Optional[float] = ..., previous_rank: _Optional[int] = ..., rank_change: _Optional[int] = ..., mmr_type: _Optional[int] = ..., kills: _Optional[int] = ..., deaths: _Optional[int] = ..., assists: _Optional[int] = ..., leaver_status: _Optional[int] = ..., gold: _Optional[int] = ..., last_hits: _Optional[int] = ..., denies: _Optional[int] = ..., gold_per_min: _Optional[int] = ..., xp_per_min: _Optional[int] = ..., gold_spent: _Optional[int] = ..., hero_damage: _Optional[int] = ..., tower_damage: _Optional[int] = ..., hero_healing: _Optional[int] = ..., disable_duration: _Optional[int] = ..., level: _Optional[int] = ..., time_last_seen: _Optional[int] = ..., player_name: _Optional[str] = ..., support_ability_value: _Optional[int] = ..., feeding_detected: bool = ..., search_rank: _Optional[int] = ..., search_rank_uncertainty: _Optional[int] = ..., rank_uncertainty_change: _Optional[int] = ..., hero_play_count: _Optional[int] = ..., party_id: _Optional[int] = ..., scaled_hero_damage: _Optional[int] = ..., scaled_tower_damage: _Optional[int] = ..., scaled_hero_healing: _Optional[int] = ..., scaled_kills: _Optional[float] = ..., scaled_deaths: _Optional[float] = ..., scaled_assists: _Optional[float] = ..., claimed_farm_gold: _Optional[int] = ..., support_gold: _Optional[int] = ..., claimed_denies: _Optional[int] = ..., claimed_misses: _Optional[int] = ..., misses: _Optional[int] = ..., ability_upgrades: _Optional[_Iterable[_Union[CMatchPlayerAbilityUpgrade, _Mapping]]] = ..., additional_units_inventory: _Optional[_Iterable[_Union[CMatchAdditionalUnitInventory, _Mapping]]] = ..., permanent_buffs: _Optional[_Iterable[_Union[CMatchPlayerPermanentBuff, _Mapping]]] = ..., pro_name: _Optional[str] = ..., real_name: _Optional[str] = ..., custom_game_data: _Optional[_Union[CMsgDOTAMatch.Player.CustomGameData, _Mapping]] = ..., active_plus_subscription: bool = ..., net_worth: _Optional[int] = ..., bot_difficulty: _Optional[int] = ..., hero_pick_order: _Optional[int] = ..., hero_was_randomed: bool = ..., hero_was_dota_plus_suggestion: bool = ..., hero_damage_received: _Optional[_Iterable[_Union[CMsgDOTAMatch.Player.HeroDamageReceived, _Mapping]]] = ..., hero_damage_dealt: _Optional[_Iterable[_Union[CMsgDOTAMatch.Player.HeroDamageReceived, _Mapping]]] = ..., seconds_dead: _Optional[int] = ..., gold_lost_to_death: _Optional[int] = ..., lane_selection_flags: _Optional[int] = ..., bounty_runes: _Optional[int] = ..., outposts_captured: _Optional[int] = ..., team_number: _Optional[_Union[_dota_shared_enums_pb2.DOTA_GC_TEAM, str]] = ..., team_slot: _Optional[int] = ..., selected_facet: _Optional[int] = ...) -> None: ...
    class BroadcasterInfo(_message.Message):
        __slots__ = ("account_id", "name")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        name: str
        def __init__(self, account_id: _Optional[int] = ..., name: _Optional[str] = ...) -> None: ...
    class BroadcasterChannel(_message.Message):
        __slots__ = ("country_code", "description", "broadcaster_infos", "language_code")
        COUNTRY_CODE_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        BROADCASTER_INFOS_FIELD_NUMBER: _ClassVar[int]
        LANGUAGE_CODE_FIELD_NUMBER: _ClassVar[int]
        country_code: str
        description: str
        broadcaster_infos: _containers.RepeatedCompositeFieldContainer[CMsgDOTAMatch.BroadcasterInfo]
        language_code: str
        def __init__(self, country_code: _Optional[str] = ..., description: _Optional[str] = ..., broadcaster_infos: _Optional[_Iterable[_Union[CMsgDOTAMatch.BroadcasterInfo, _Mapping]]] = ..., language_code: _Optional[str] = ...) -> None: ...
    class Coach(_message.Message):
        __slots__ = ("account_id", "coach_name", "coach_rating", "coach_team", "coach_party_id", "is_private_coach")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        COACH_NAME_FIELD_NUMBER: _ClassVar[int]
        COACH_RATING_FIELD_NUMBER: _ClassVar[int]
        COACH_TEAM_FIELD_NUMBER: _ClassVar[int]
        COACH_PARTY_ID_FIELD_NUMBER: _ClassVar[int]
        IS_PRIVATE_COACH_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        coach_name: str
        coach_rating: int
        coach_team: int
        coach_party_id: int
        is_private_coach: bool
        def __init__(self, account_id: _Optional[int] = ..., coach_name: _Optional[str] = ..., coach_rating: _Optional[int] = ..., coach_team: _Optional[int] = ..., coach_party_id: _Optional[int] = ..., is_private_coach: bool = ...) -> None: ...
    class CustomGameData(_message.Message):
        __slots__ = ("custom_game_id", "map_name")
        CUSTOM_GAME_ID_FIELD_NUMBER: _ClassVar[int]
        MAP_NAME_FIELD_NUMBER: _ClassVar[int]
        custom_game_id: int
        map_name: str
        def __init__(self, custom_game_id: _Optional[int] = ..., map_name: _Optional[str] = ...) -> None: ...
    DURATION_FIELD_NUMBER: _ClassVar[int]
    STARTTIME_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    TOWER_STATUS_FIELD_NUMBER: _ClassVar[int]
    BARRACKS_STATUS_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_FIELD_NUMBER: _ClassVar[int]
    FIRST_BLOOD_TIME_FIELD_NUMBER: _ClassVar[int]
    REPLAY_SALT_FIELD_NUMBER: _ClassVar[int]
    SERVER_IP_FIELD_NUMBER: _ClassVar[int]
    SERVER_PORT_FIELD_NUMBER: _ClassVar[int]
    LOBBY_TYPE_FIELD_NUMBER: _ClassVar[int]
    HUMAN_PLAYERS_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_SKILL_FIELD_NUMBER: _ClassVar[int]
    GAME_BALANCE_FIELD_NUMBER: _ClassVar[int]
    RADIANT_TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    DIRE_TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    LEAGUEID_FIELD_NUMBER: _ClassVar[int]
    RADIANT_TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
    DIRE_TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
    RADIANT_TEAM_LOGO_FIELD_NUMBER: _ClassVar[int]
    DIRE_TEAM_LOGO_FIELD_NUMBER: _ClassVar[int]
    RADIANT_TEAM_LOGO_URL_FIELD_NUMBER: _ClassVar[int]
    DIRE_TEAM_LOGO_URL_FIELD_NUMBER: _ClassVar[int]
    RADIANT_TEAM_COMPLETE_FIELD_NUMBER: _ClassVar[int]
    DIRE_TEAM_COMPLETE_FIELD_NUMBER: _ClassVar[int]
    GAME_MODE_FIELD_NUMBER: _ClassVar[int]
    PICKS_BANS_FIELD_NUMBER: _ClassVar[int]
    MATCH_SEQ_NUM_FIELD_NUMBER: _ClassVar[int]
    REPLAY_STATE_FIELD_NUMBER: _ClassVar[int]
    RADIANT_GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    DIRE_GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    RADIANT_TEAM_TAG_FIELD_NUMBER: _ClassVar[int]
    DIRE_TEAM_TAG_FIELD_NUMBER: _ClassVar[int]
    SERIES_ID_FIELD_NUMBER: _ClassVar[int]
    SERIES_TYPE_FIELD_NUMBER: _ClassVar[int]
    BROADCASTER_CHANNELS_FIELD_NUMBER: _ClassVar[int]
    ENGINE_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_DATA_FIELD_NUMBER: _ClassVar[int]
    MATCH_FLAGS_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_METADATA_KEY_FIELD_NUMBER: _ClassVar[int]
    RADIANT_TEAM_SCORE_FIELD_NUMBER: _ClassVar[int]
    DIRE_TEAM_SCORE_FIELD_NUMBER: _ClassVar[int]
    MATCH_OUTCOME_FIELD_NUMBER: _ClassVar[int]
    TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TOURNAMENT_ROUND_FIELD_NUMBER: _ClassVar[int]
    PRE_GAME_DURATION_FIELD_NUMBER: _ClassVar[int]
    COACHES_FIELD_NUMBER: _ClassVar[int]
    duration: int
    starttime: int
    players: _containers.RepeatedCompositeFieldContainer[CMsgDOTAMatch.Player]
    match_id: int
    tower_status: _containers.RepeatedScalarFieldContainer[int]
    barracks_status: _containers.RepeatedScalarFieldContainer[int]
    cluster: int
    first_blood_time: int
    replay_salt: int
    server_ip: int
    server_port: int
    lobby_type: int
    human_players: int
    average_skill: int
    game_balance: float
    radiant_team_id: int
    dire_team_id: int
    leagueid: int
    radiant_team_name: str
    dire_team_name: str
    radiant_team_logo: int
    dire_team_logo: int
    radiant_team_logo_url: str
    dire_team_logo_url: str
    radiant_team_complete: int
    dire_team_complete: int
    game_mode: _dota_shared_enums_pb2.DOTA_GameMode
    picks_bans: _containers.RepeatedCompositeFieldContainer[CMatchHeroSelectEvent]
    match_seq_num: int
    replay_state: CMsgDOTAMatch.ReplayState
    radiant_guild_id: int
    dire_guild_id: int
    radiant_team_tag: str
    dire_team_tag: str
    series_id: int
    series_type: int
    broadcaster_channels: _containers.RepeatedCompositeFieldContainer[CMsgDOTAMatch.BroadcasterChannel]
    engine: int
    custom_game_data: CMsgDOTAMatch.CustomGameData
    match_flags: int
    private_metadata_key: int
    radiant_team_score: int
    dire_team_score: int
    match_outcome: _dota_shared_enums_pb2.EMatchOutcome
    tournament_id: int
    tournament_round: int
    pre_game_duration: int
    coaches: _containers.RepeatedCompositeFieldContainer[CMsgDOTAMatch.Coach]
    def __init__(self, duration: _Optional[int] = ..., starttime: _Optional[int] = ..., players: _Optional[_Iterable[_Union[CMsgDOTAMatch.Player, _Mapping]]] = ..., match_id: _Optional[int] = ..., tower_status: _Optional[_Iterable[int]] = ..., barracks_status: _Optional[_Iterable[int]] = ..., cluster: _Optional[int] = ..., first_blood_time: _Optional[int] = ..., replay_salt: _Optional[int] = ..., server_ip: _Optional[int] = ..., server_port: _Optional[int] = ..., lobby_type: _Optional[int] = ..., human_players: _Optional[int] = ..., average_skill: _Optional[int] = ..., game_balance: _Optional[float] = ..., radiant_team_id: _Optional[int] = ..., dire_team_id: _Optional[int] = ..., leagueid: _Optional[int] = ..., radiant_team_name: _Optional[str] = ..., dire_team_name: _Optional[str] = ..., radiant_team_logo: _Optional[int] = ..., dire_team_logo: _Optional[int] = ..., radiant_team_logo_url: _Optional[str] = ..., dire_team_logo_url: _Optional[str] = ..., radiant_team_complete: _Optional[int] = ..., dire_team_complete: _Optional[int] = ..., game_mode: _Optional[_Union[_dota_shared_enums_pb2.DOTA_GameMode, str]] = ..., picks_bans: _Optional[_Iterable[_Union[CMatchHeroSelectEvent, _Mapping]]] = ..., match_seq_num: _Optional[int] = ..., replay_state: _Optional[_Union[CMsgDOTAMatch.ReplayState, str]] = ..., radiant_guild_id: _Optional[int] = ..., dire_guild_id: _Optional[int] = ..., radiant_team_tag: _Optional[str] = ..., dire_team_tag: _Optional[str] = ..., series_id: _Optional[int] = ..., series_type: _Optional[int] = ..., broadcaster_channels: _Optional[_Iterable[_Union[CMsgDOTAMatch.BroadcasterChannel, _Mapping]]] = ..., engine: _Optional[int] = ..., custom_game_data: _Optional[_Union[CMsgDOTAMatch.CustomGameData, _Mapping]] = ..., match_flags: _Optional[int] = ..., private_metadata_key: _Optional[int] = ..., radiant_team_score: _Optional[int] = ..., dire_team_score: _Optional[int] = ..., match_outcome: _Optional[_Union[_dota_shared_enums_pb2.EMatchOutcome, str]] = ..., tournament_id: _Optional[int] = ..., tournament_round: _Optional[int] = ..., pre_game_duration: _Optional[int] = ..., coaches: _Optional[_Iterable[_Union[CMsgDOTAMatch.Coach, _Mapping]]] = ...) -> None: ...

class CMsgPlayerCard(_message.Message):
    __slots__ = ("account_id", "stat_modifier")
    class StatModifier(_message.Message):
        __slots__ = ("stat", "value")
        STAT_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        stat: int
        value: int
        def __init__(self, stat: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    STAT_MODIFIER_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    stat_modifier: _containers.RepeatedCompositeFieldContainer[CMsgPlayerCard.StatModifier]
    def __init__(self, account_id: _Optional[int] = ..., stat_modifier: _Optional[_Iterable[_Union[CMsgPlayerCard.StatModifier, _Mapping]]] = ...) -> None: ...

class CMsgDOTAFantasyPlayerStats(_message.Message):
    __slots__ = ("player_account_id", "match_id", "match_completed", "team_id", "league_id", "delay", "series_id", "series_type", "kills", "deaths", "cs", "gpm", "tower_kills", "roshan_kills", "teamfight_participation", "wards_placed", "camps_stacked", "runes_grabbed", "first_blood", "stuns", "smokes", "watchers", "lotuses", "tormentors", "courier_kills", "title_stats", "madstone")
    PLAYER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    MATCH_COMPLETED_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    DELAY_FIELD_NUMBER: _ClassVar[int]
    SERIES_ID_FIELD_NUMBER: _ClassVar[int]
    SERIES_TYPE_FIELD_NUMBER: _ClassVar[int]
    KILLS_FIELD_NUMBER: _ClassVar[int]
    DEATHS_FIELD_NUMBER: _ClassVar[int]
    CS_FIELD_NUMBER: _ClassVar[int]
    GPM_FIELD_NUMBER: _ClassVar[int]
    TOWER_KILLS_FIELD_NUMBER: _ClassVar[int]
    ROSHAN_KILLS_FIELD_NUMBER: _ClassVar[int]
    TEAMFIGHT_PARTICIPATION_FIELD_NUMBER: _ClassVar[int]
    WARDS_PLACED_FIELD_NUMBER: _ClassVar[int]
    CAMPS_STACKED_FIELD_NUMBER: _ClassVar[int]
    RUNES_GRABBED_FIELD_NUMBER: _ClassVar[int]
    FIRST_BLOOD_FIELD_NUMBER: _ClassVar[int]
    STUNS_FIELD_NUMBER: _ClassVar[int]
    SMOKES_FIELD_NUMBER: _ClassVar[int]
    WATCHERS_FIELD_NUMBER: _ClassVar[int]
    LOTUSES_FIELD_NUMBER: _ClassVar[int]
    TORMENTORS_FIELD_NUMBER: _ClassVar[int]
    COURIER_KILLS_FIELD_NUMBER: _ClassVar[int]
    TITLE_STATS_FIELD_NUMBER: _ClassVar[int]
    MADSTONE_FIELD_NUMBER: _ClassVar[int]
    player_account_id: int
    match_id: int
    match_completed: bool
    team_id: int
    league_id: int
    delay: int
    series_id: int
    series_type: int
    kills: int
    deaths: int
    cs: int
    gpm: float
    tower_kills: int
    roshan_kills: int
    teamfight_participation: float
    wards_placed: int
    camps_stacked: int
    runes_grabbed: int
    first_blood: int
    stuns: float
    smokes: int
    watchers: int
    lotuses: int
    tormentors: int
    courier_kills: int
    title_stats: int
    madstone: int
    def __init__(self, player_account_id: _Optional[int] = ..., match_id: _Optional[int] = ..., match_completed: bool = ..., team_id: _Optional[int] = ..., league_id: _Optional[int] = ..., delay: _Optional[int] = ..., series_id: _Optional[int] = ..., series_type: _Optional[int] = ..., kills: _Optional[int] = ..., deaths: _Optional[int] = ..., cs: _Optional[int] = ..., gpm: _Optional[float] = ..., tower_kills: _Optional[int] = ..., roshan_kills: _Optional[int] = ..., teamfight_participation: _Optional[float] = ..., wards_placed: _Optional[int] = ..., camps_stacked: _Optional[int] = ..., runes_grabbed: _Optional[int] = ..., first_blood: _Optional[int] = ..., stuns: _Optional[float] = ..., smokes: _Optional[int] = ..., watchers: _Optional[int] = ..., lotuses: _Optional[int] = ..., tormentors: _Optional[int] = ..., courier_kills: _Optional[int] = ..., title_stats: _Optional[int] = ..., madstone: _Optional[int] = ...) -> None: ...

class CMsgDOTAFantasyPlayerMatchStats(_message.Message):
    __slots__ = ("matches",)
    MATCHES_FIELD_NUMBER: _ClassVar[int]
    matches: _containers.RepeatedCompositeFieldContainer[CMsgDOTAFantasyPlayerStats]
    def __init__(self, matches: _Optional[_Iterable[_Union[CMsgDOTAFantasyPlayerStats, _Mapping]]] = ...) -> None: ...

class CMsgDOTABotDebugInfo(_message.Message):
    __slots__ = ("bots", "desire_push_lane_top", "desire_push_lane_mid", "desire_push_lane_bot", "desire_defend_lane_top", "desire_defend_lane_mid", "desire_defend_lane_bot", "desire_farm_lane_top", "desire_farm_lane_mid", "desire_farm_lane_bot", "desire_farm_roshan", "execution_time", "rune_status")
    class Bot(_message.Message):
        __slots__ = ("player_owner_id", "hero_id", "difficulty", "power_current", "power_max", "move_target_x", "move_target_y", "move_target_z", "active_mode_id", "execution_time", "modes", "action")
        class Mode(_message.Message):
            __slots__ = ("mode_id", "desire", "target_entity", "target_x", "target_y", "target_z")
            MODE_ID_FIELD_NUMBER: _ClassVar[int]
            DESIRE_FIELD_NUMBER: _ClassVar[int]
            TARGET_ENTITY_FIELD_NUMBER: _ClassVar[int]
            TARGET_X_FIELD_NUMBER: _ClassVar[int]
            TARGET_Y_FIELD_NUMBER: _ClassVar[int]
            TARGET_Z_FIELD_NUMBER: _ClassVar[int]
            mode_id: int
            desire: float
            target_entity: int
            target_x: int
            target_y: int
            target_z: int
            def __init__(self, mode_id: _Optional[int] = ..., desire: _Optional[float] = ..., target_entity: _Optional[int] = ..., target_x: _Optional[int] = ..., target_y: _Optional[int] = ..., target_z: _Optional[int] = ...) -> None: ...
        class Action(_message.Message):
            __slots__ = ("action_id", "action_target")
            ACTION_ID_FIELD_NUMBER: _ClassVar[int]
            ACTION_TARGET_FIELD_NUMBER: _ClassVar[int]
            action_id: int
            action_target: str
            def __init__(self, action_id: _Optional[int] = ..., action_target: _Optional[str] = ...) -> None: ...
        PLAYER_OWNER_ID_FIELD_NUMBER: _ClassVar[int]
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        DIFFICULTY_FIELD_NUMBER: _ClassVar[int]
        POWER_CURRENT_FIELD_NUMBER: _ClassVar[int]
        POWER_MAX_FIELD_NUMBER: _ClassVar[int]
        MOVE_TARGET_X_FIELD_NUMBER: _ClassVar[int]
        MOVE_TARGET_Y_FIELD_NUMBER: _ClassVar[int]
        MOVE_TARGET_Z_FIELD_NUMBER: _ClassVar[int]
        ACTIVE_MODE_ID_FIELD_NUMBER: _ClassVar[int]
        EXECUTION_TIME_FIELD_NUMBER: _ClassVar[int]
        MODES_FIELD_NUMBER: _ClassVar[int]
        ACTION_FIELD_NUMBER: _ClassVar[int]
        player_owner_id: int
        hero_id: int
        difficulty: int
        power_current: int
        power_max: int
        move_target_x: int
        move_target_y: int
        move_target_z: int
        active_mode_id: int
        execution_time: float
        modes: _containers.RepeatedCompositeFieldContainer[CMsgDOTABotDebugInfo.Bot.Mode]
        action: CMsgDOTABotDebugInfo.Bot.Action
        def __init__(self, player_owner_id: _Optional[int] = ..., hero_id: _Optional[int] = ..., difficulty: _Optional[int] = ..., power_current: _Optional[int] = ..., power_max: _Optional[int] = ..., move_target_x: _Optional[int] = ..., move_target_y: _Optional[int] = ..., move_target_z: _Optional[int] = ..., active_mode_id: _Optional[int] = ..., execution_time: _Optional[float] = ..., modes: _Optional[_Iterable[_Union[CMsgDOTABotDebugInfo.Bot.Mode, _Mapping]]] = ..., action: _Optional[_Union[CMsgDOTABotDebugInfo.Bot.Action, _Mapping]] = ...) -> None: ...
    BOTS_FIELD_NUMBER: _ClassVar[int]
    DESIRE_PUSH_LANE_TOP_FIELD_NUMBER: _ClassVar[int]
    DESIRE_PUSH_LANE_MID_FIELD_NUMBER: _ClassVar[int]
    DESIRE_PUSH_LANE_BOT_FIELD_NUMBER: _ClassVar[int]
    DESIRE_DEFEND_LANE_TOP_FIELD_NUMBER: _ClassVar[int]
    DESIRE_DEFEND_LANE_MID_FIELD_NUMBER: _ClassVar[int]
    DESIRE_DEFEND_LANE_BOT_FIELD_NUMBER: _ClassVar[int]
    DESIRE_FARM_LANE_TOP_FIELD_NUMBER: _ClassVar[int]
    DESIRE_FARM_LANE_MID_FIELD_NUMBER: _ClassVar[int]
    DESIRE_FARM_LANE_BOT_FIELD_NUMBER: _ClassVar[int]
    DESIRE_FARM_ROSHAN_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_TIME_FIELD_NUMBER: _ClassVar[int]
    RUNE_STATUS_FIELD_NUMBER: _ClassVar[int]
    bots: _containers.RepeatedCompositeFieldContainer[CMsgDOTABotDebugInfo.Bot]
    desire_push_lane_top: float
    desire_push_lane_mid: float
    desire_push_lane_bot: float
    desire_defend_lane_top: float
    desire_defend_lane_mid: float
    desire_defend_lane_bot: float
    desire_farm_lane_top: float
    desire_farm_lane_mid: float
    desire_farm_lane_bot: float
    desire_farm_roshan: float
    execution_time: float
    rune_status: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, bots: _Optional[_Iterable[_Union[CMsgDOTABotDebugInfo.Bot, _Mapping]]] = ..., desire_push_lane_top: _Optional[float] = ..., desire_push_lane_mid: _Optional[float] = ..., desire_push_lane_bot: _Optional[float] = ..., desire_defend_lane_top: _Optional[float] = ..., desire_defend_lane_mid: _Optional[float] = ..., desire_defend_lane_bot: _Optional[float] = ..., desire_farm_lane_top: _Optional[float] = ..., desire_farm_lane_mid: _Optional[float] = ..., desire_farm_lane_bot: _Optional[float] = ..., desire_farm_roshan: _Optional[float] = ..., execution_time: _Optional[float] = ..., rune_status: _Optional[_Iterable[int]] = ...) -> None: ...

class CMsgSuccessfulHero(_message.Message):
    __slots__ = ("hero_id", "win_percent", "longest_streak")
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    WIN_PERCENT_FIELD_NUMBER: _ClassVar[int]
    LONGEST_STREAK_FIELD_NUMBER: _ClassVar[int]
    hero_id: int
    win_percent: float
    longest_streak: int
    def __init__(self, hero_id: _Optional[int] = ..., win_percent: _Optional[float] = ..., longest_streak: _Optional[int] = ...) -> None: ...

class CMsgRecentMatchInfo(_message.Message):
    __slots__ = ("match_id", "game_mode", "kills", "deaths", "assists", "duration", "player_slot", "match_outcome", "timestamp", "lobby_type", "team_number")
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    GAME_MODE_FIELD_NUMBER: _ClassVar[int]
    KILLS_FIELD_NUMBER: _ClassVar[int]
    DEATHS_FIELD_NUMBER: _ClassVar[int]
    ASSISTS_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
    MATCH_OUTCOME_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LOBBY_TYPE_FIELD_NUMBER: _ClassVar[int]
    TEAM_NUMBER_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    game_mode: _dota_shared_enums_pb2.DOTA_GameMode
    kills: int
    deaths: int
    assists: int
    duration: int
    player_slot: int
    match_outcome: _dota_shared_enums_pb2.EMatchOutcome
    timestamp: int
    lobby_type: int
    team_number: int
    def __init__(self, match_id: _Optional[int] = ..., game_mode: _Optional[_Union[_dota_shared_enums_pb2.DOTA_GameMode, str]] = ..., kills: _Optional[int] = ..., deaths: _Optional[int] = ..., assists: _Optional[int] = ..., duration: _Optional[int] = ..., player_slot: _Optional[int] = ..., match_outcome: _Optional[_Union[_dota_shared_enums_pb2.EMatchOutcome, str]] = ..., timestamp: _Optional[int] = ..., lobby_type: _Optional[int] = ..., team_number: _Optional[int] = ...) -> None: ...

class CMsgMatchTips(_message.Message):
    __slots__ = ("tips",)
    class SingleTip(_message.Message):
        __slots__ = ("source_account_id", "target_account_id", "tip_amount", "event_id")
        SOURCE_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        TIP_AMOUNT_FIELD_NUMBER: _ClassVar[int]
        EVENT_ID_FIELD_NUMBER: _ClassVar[int]
        source_account_id: int
        target_account_id: int
        tip_amount: int
        event_id: _dota_shared_enums_pb2.EEvent
        def __init__(self, source_account_id: _Optional[int] = ..., target_account_id: _Optional[int] = ..., tip_amount: _Optional[int] = ..., event_id: _Optional[_Union[_dota_shared_enums_pb2.EEvent, str]] = ...) -> None: ...
    TIPS_FIELD_NUMBER: _ClassVar[int]
    tips: _containers.RepeatedCompositeFieldContainer[CMsgMatchTips.SingleTip]
    def __init__(self, tips: _Optional[_Iterable[_Union[CMsgMatchTips.SingleTip, _Mapping]]] = ...) -> None: ...

class CMsgDOTAMatchMinimal(_message.Message):
    __slots__ = ("match_id", "start_time", "duration", "game_mode", "players", "tourney", "match_outcome", "radiant_score", "dire_score", "lobby_type", "is_player_draft")
    class Player(_message.Message):
        __slots__ = ("account_id", "hero_id", "kills", "deaths", "assists", "items", "player_slot", "pro_name", "level", "team_number")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        KILLS_FIELD_NUMBER: _ClassVar[int]
        DEATHS_FIELD_NUMBER: _ClassVar[int]
        ASSISTS_FIELD_NUMBER: _ClassVar[int]
        ITEMS_FIELD_NUMBER: _ClassVar[int]
        PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
        PRO_NAME_FIELD_NUMBER: _ClassVar[int]
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        TEAM_NUMBER_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        hero_id: int
        kills: int
        deaths: int
        assists: int
        items: _containers.RepeatedScalarFieldContainer[int]
        player_slot: int
        pro_name: str
        level: int
        team_number: _dota_shared_enums_pb2.DOTA_GC_TEAM
        def __init__(self, account_id: _Optional[int] = ..., hero_id: _Optional[int] = ..., kills: _Optional[int] = ..., deaths: _Optional[int] = ..., assists: _Optional[int] = ..., items: _Optional[_Iterable[int]] = ..., player_slot: _Optional[int] = ..., pro_name: _Optional[str] = ..., level: _Optional[int] = ..., team_number: _Optional[_Union[_dota_shared_enums_pb2.DOTA_GC_TEAM, str]] = ...) -> None: ...
    class Tourney(_message.Message):
        __slots__ = ("league_id", "series_type", "series_game", "weekend_tourney_tournament_id", "weekend_tourney_season_trophy_id", "weekend_tourney_division", "weekend_tourney_skill_level", "radiant_team_id", "radiant_team_name", "radiant_team_logo", "radiant_team_logo_url", "dire_team_id", "dire_team_name", "dire_team_logo", "dire_team_logo_url")
        LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
        SERIES_TYPE_FIELD_NUMBER: _ClassVar[int]
        SERIES_GAME_FIELD_NUMBER: _ClassVar[int]
        WEEKEND_TOURNEY_TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
        WEEKEND_TOURNEY_SEASON_TROPHY_ID_FIELD_NUMBER: _ClassVar[int]
        WEEKEND_TOURNEY_DIVISION_FIELD_NUMBER: _ClassVar[int]
        WEEKEND_TOURNEY_SKILL_LEVEL_FIELD_NUMBER: _ClassVar[int]
        RADIANT_TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        RADIANT_TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
        RADIANT_TEAM_LOGO_FIELD_NUMBER: _ClassVar[int]
        RADIANT_TEAM_LOGO_URL_FIELD_NUMBER: _ClassVar[int]
        DIRE_TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        DIRE_TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
        DIRE_TEAM_LOGO_FIELD_NUMBER: _ClassVar[int]
        DIRE_TEAM_LOGO_URL_FIELD_NUMBER: _ClassVar[int]
        league_id: int
        series_type: int
        series_game: int
        weekend_tourney_tournament_id: int
        weekend_tourney_season_trophy_id: int
        weekend_tourney_division: int
        weekend_tourney_skill_level: int
        radiant_team_id: int
        radiant_team_name: str
        radiant_team_logo: int
        radiant_team_logo_url: str
        dire_team_id: int
        dire_team_name: str
        dire_team_logo: int
        dire_team_logo_url: str
        def __init__(self, league_id: _Optional[int] = ..., series_type: _Optional[int] = ..., series_game: _Optional[int] = ..., weekend_tourney_tournament_id: _Optional[int] = ..., weekend_tourney_season_trophy_id: _Optional[int] = ..., weekend_tourney_division: _Optional[int] = ..., weekend_tourney_skill_level: _Optional[int] = ..., radiant_team_id: _Optional[int] = ..., radiant_team_name: _Optional[str] = ..., radiant_team_logo: _Optional[int] = ..., radiant_team_logo_url: _Optional[str] = ..., dire_team_id: _Optional[int] = ..., dire_team_name: _Optional[str] = ..., dire_team_logo: _Optional[int] = ..., dire_team_logo_url: _Optional[str] = ...) -> None: ...
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    GAME_MODE_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    TOURNEY_FIELD_NUMBER: _ClassVar[int]
    MATCH_OUTCOME_FIELD_NUMBER: _ClassVar[int]
    RADIANT_SCORE_FIELD_NUMBER: _ClassVar[int]
    DIRE_SCORE_FIELD_NUMBER: _ClassVar[int]
    LOBBY_TYPE_FIELD_NUMBER: _ClassVar[int]
    IS_PLAYER_DRAFT_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    start_time: int
    duration: int
    game_mode: _dota_shared_enums_pb2.DOTA_GameMode
    players: _containers.RepeatedCompositeFieldContainer[CMsgDOTAMatchMinimal.Player]
    tourney: CMsgDOTAMatchMinimal.Tourney
    match_outcome: _dota_shared_enums_pb2.EMatchOutcome
    radiant_score: int
    dire_score: int
    lobby_type: int
    is_player_draft: bool
    def __init__(self, match_id: _Optional[int] = ..., start_time: _Optional[int] = ..., duration: _Optional[int] = ..., game_mode: _Optional[_Union[_dota_shared_enums_pb2.DOTA_GameMode, str]] = ..., players: _Optional[_Iterable[_Union[CMsgDOTAMatchMinimal.Player, _Mapping]]] = ..., tourney: _Optional[_Union[CMsgDOTAMatchMinimal.Tourney, _Mapping]] = ..., match_outcome: _Optional[_Union[_dota_shared_enums_pb2.EMatchOutcome, str]] = ..., radiant_score: _Optional[int] = ..., dire_score: _Optional[int] = ..., lobby_type: _Optional[int] = ..., is_player_draft: bool = ...) -> None: ...

class CMsgConsumableUsage(_message.Message):
    __slots__ = ("item_def", "quantity_change")
    ITEM_DEF_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_CHANGE_FIELD_NUMBER: _ClassVar[int]
    item_def: int
    quantity_change: int
    def __init__(self, item_def: _Optional[int] = ..., quantity_change: _Optional[int] = ...) -> None: ...

class CMsgMatchConsumableUsage(_message.Message):
    __slots__ = ("player_consumables_used",)
    class PlayerUsage(_message.Message):
        __slots__ = ("account_id", "consumables_used")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        CONSUMABLES_USED_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        consumables_used: _containers.RepeatedCompositeFieldContainer[CMsgConsumableUsage]
        def __init__(self, account_id: _Optional[int] = ..., consumables_used: _Optional[_Iterable[_Union[CMsgConsumableUsage, _Mapping]]] = ...) -> None: ...
    PLAYER_CONSUMABLES_USED_FIELD_NUMBER: _ClassVar[int]
    player_consumables_used: _containers.RepeatedCompositeFieldContainer[CMsgMatchConsumableUsage.PlayerUsage]
    def __init__(self, player_consumables_used: _Optional[_Iterable[_Union[CMsgMatchConsumableUsage.PlayerUsage, _Mapping]]] = ...) -> None: ...

class CMsgMatchEventActionGrants(_message.Message):
    __slots__ = ("player_grants",)
    class PlayerGrants(_message.Message):
        __slots__ = ("account_id", "actions_granted")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        ACTIONS_GRANTED_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        actions_granted: _containers.RepeatedCompositeFieldContainer[_dota_shared_enums_pb2.CMsgPendingEventAward]
        def __init__(self, account_id: _Optional[int] = ..., actions_granted: _Optional[_Iterable[_Union[_dota_shared_enums_pb2.CMsgPendingEventAward, _Mapping]]] = ...) -> None: ...
    PLAYER_GRANTS_FIELD_NUMBER: _ClassVar[int]
    player_grants: _containers.RepeatedCompositeFieldContainer[CMsgMatchEventActionGrants.PlayerGrants]
    def __init__(self, player_grants: _Optional[_Iterable[_Union[CMsgMatchEventActionGrants.PlayerGrants, _Mapping]]] = ...) -> None: ...

class CMsgCustomGameWhitelist(_message.Message):
    __slots__ = ("version", "custom_games_whitelist", "disable_whitelist")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAMES_WHITELIST_FIELD_NUMBER: _ClassVar[int]
    DISABLE_WHITELIST_FIELD_NUMBER: _ClassVar[int]
    version: int
    custom_games_whitelist: _containers.RepeatedScalarFieldContainer[int]
    disable_whitelist: bool
    def __init__(self, version: _Optional[int] = ..., custom_games_whitelist: _Optional[_Iterable[int]] = ..., disable_whitelist: bool = ...) -> None: ...

class CMsgCustomGameWhitelistForEdit(_message.Message):
    __slots__ = ("whitelist_entries",)
    class WhitelistEntry(_message.Message):
        __slots__ = ("custom_game_id", "whitelist_state")
        CUSTOM_GAME_ID_FIELD_NUMBER: _ClassVar[int]
        WHITELIST_STATE_FIELD_NUMBER: _ClassVar[int]
        custom_game_id: int
        whitelist_state: ECustomGameWhitelistState
        def __init__(self, custom_game_id: _Optional[int] = ..., whitelist_state: _Optional[_Union[ECustomGameWhitelistState, str]] = ...) -> None: ...
    WHITELIST_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    whitelist_entries: _containers.RepeatedCompositeFieldContainer[CMsgCustomGameWhitelistForEdit.WhitelistEntry]
    def __init__(self, whitelist_entries: _Optional[_Iterable[_Union[CMsgCustomGameWhitelistForEdit.WhitelistEntry, _Mapping]]] = ...) -> None: ...

class CMsgPlayerRecentMatchInfo(_message.Message):
    __slots__ = ("match_id", "timestamp", "duration", "win", "hero_id", "kills", "deaths", "assists")
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    WIN_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    KILLS_FIELD_NUMBER: _ClassVar[int]
    DEATHS_FIELD_NUMBER: _ClassVar[int]
    ASSISTS_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    timestamp: int
    duration: int
    win: bool
    hero_id: int
    kills: int
    deaths: int
    assists: int
    def __init__(self, match_id: _Optional[int] = ..., timestamp: _Optional[int] = ..., duration: _Optional[int] = ..., win: bool = ..., hero_id: _Optional[int] = ..., kills: _Optional[int] = ..., deaths: _Optional[int] = ..., assists: _Optional[int] = ...) -> None: ...

class CMsgPlayerMatchRecord(_message.Message):
    __slots__ = ("wins", "losses")
    WINS_FIELD_NUMBER: _ClassVar[int]
    LOSSES_FIELD_NUMBER: _ClassVar[int]
    wins: int
    losses: int
    def __init__(self, wins: _Optional[int] = ..., losses: _Optional[int] = ...) -> None: ...

class CMsgPlayerRecentMatchOutcomes(_message.Message):
    __slots__ = ("outcomes", "match_count")
    OUTCOMES_FIELD_NUMBER: _ClassVar[int]
    MATCH_COUNT_FIELD_NUMBER: _ClassVar[int]
    outcomes: int
    match_count: int
    def __init__(self, outcomes: _Optional[int] = ..., match_count: _Optional[int] = ...) -> None: ...

class CMsgPlayerRecentCommends(_message.Message):
    __slots__ = ("commends", "match_count")
    COMMENDS_FIELD_NUMBER: _ClassVar[int]
    MATCH_COUNT_FIELD_NUMBER: _ClassVar[int]
    commends: int
    match_count: int
    def __init__(self, commends: _Optional[int] = ..., match_count: _Optional[int] = ...) -> None: ...

class CMsgPlayerRecentAccomplishments(_message.Message):
    __slots__ = ("recent_outcomes", "total_record", "prediction_streak", "plus_prediction_streak", "recent_commends", "first_match_timestamp", "last_match", "recent_mvps")
    RECENT_OUTCOMES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_RECORD_FIELD_NUMBER: _ClassVar[int]
    PREDICTION_STREAK_FIELD_NUMBER: _ClassVar[int]
    PLUS_PREDICTION_STREAK_FIELD_NUMBER: _ClassVar[int]
    RECENT_COMMENDS_FIELD_NUMBER: _ClassVar[int]
    FIRST_MATCH_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LAST_MATCH_FIELD_NUMBER: _ClassVar[int]
    RECENT_MVPS_FIELD_NUMBER: _ClassVar[int]
    recent_outcomes: CMsgPlayerRecentMatchOutcomes
    total_record: CMsgPlayerMatchRecord
    prediction_streak: int
    plus_prediction_streak: int
    recent_commends: CMsgPlayerRecentCommends
    first_match_timestamp: int
    last_match: CMsgPlayerRecentMatchInfo
    recent_mvps: CMsgPlayerRecentMatchOutcomes
    def __init__(self, recent_outcomes: _Optional[_Union[CMsgPlayerRecentMatchOutcomes, _Mapping]] = ..., total_record: _Optional[_Union[CMsgPlayerMatchRecord, _Mapping]] = ..., prediction_streak: _Optional[int] = ..., plus_prediction_streak: _Optional[int] = ..., recent_commends: _Optional[_Union[CMsgPlayerRecentCommends, _Mapping]] = ..., first_match_timestamp: _Optional[int] = ..., last_match: _Optional[_Union[CMsgPlayerRecentMatchInfo, _Mapping]] = ..., recent_mvps: _Optional[_Union[CMsgPlayerRecentMatchOutcomes, _Mapping]] = ...) -> None: ...

class CMsgPlayerHeroRecentAccomplishments(_message.Message):
    __slots__ = ("recent_outcomes", "total_record", "last_match")
    RECENT_OUTCOMES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_RECORD_FIELD_NUMBER: _ClassVar[int]
    LAST_MATCH_FIELD_NUMBER: _ClassVar[int]
    recent_outcomes: CMsgPlayerRecentMatchOutcomes
    total_record: CMsgPlayerMatchRecord
    last_match: CMsgPlayerRecentMatchInfo
    def __init__(self, recent_outcomes: _Optional[_Union[CMsgPlayerRecentMatchOutcomes, _Mapping]] = ..., total_record: _Optional[_Union[CMsgPlayerMatchRecord, _Mapping]] = ..., last_match: _Optional[_Union[CMsgPlayerRecentMatchInfo, _Mapping]] = ...) -> None: ...

class CMsgRecentAccomplishments(_message.Message):
    __slots__ = ("player_accomplishments", "hero_accomplishments")
    PLAYER_ACCOMPLISHMENTS_FIELD_NUMBER: _ClassVar[int]
    HERO_ACCOMPLISHMENTS_FIELD_NUMBER: _ClassVar[int]
    player_accomplishments: CMsgPlayerRecentAccomplishments
    hero_accomplishments: CMsgPlayerHeroRecentAccomplishments
    def __init__(self, player_accomplishments: _Optional[_Union[CMsgPlayerRecentAccomplishments, _Mapping]] = ..., hero_accomplishments: _Optional[_Union[CMsgPlayerHeroRecentAccomplishments, _Mapping]] = ...) -> None: ...

class CMsgServerToGCRequestPlayerRecentAccomplishments(_message.Message):
    __slots__ = ("account_id", "hero_id")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    hero_id: int
    def __init__(self, account_id: _Optional[int] = ..., hero_id: _Optional[int] = ...) -> None: ...

class CMsgServerToGCRequestPlayerRecentAccomplishmentsResponse(_message.Message):
    __slots__ = ("result", "player_accomplishments")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgServerToGCRequestPlayerRecentAccomplishmentsResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgServerToGCRequestPlayerRecentAccomplishmentsResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgServerToGCRequestPlayerRecentAccomplishmentsResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgServerToGCRequestPlayerRecentAccomplishmentsResponse.EResponse]
        k_eForbidden: _ClassVar[CMsgServerToGCRequestPlayerRecentAccomplishmentsResponse.EResponse]
    k_eInternalError: CMsgServerToGCRequestPlayerRecentAccomplishmentsResponse.EResponse
    k_eSuccess: CMsgServerToGCRequestPlayerRecentAccomplishmentsResponse.EResponse
    k_eTooBusy: CMsgServerToGCRequestPlayerRecentAccomplishmentsResponse.EResponse
    k_eDisabled: CMsgServerToGCRequestPlayerRecentAccomplishmentsResponse.EResponse
    k_eForbidden: CMsgServerToGCRequestPlayerRecentAccomplishmentsResponse.EResponse
    RESULT_FIELD_NUMBER: _ClassVar[int]
    PLAYER_ACCOMPLISHMENTS_FIELD_NUMBER: _ClassVar[int]
    result: CMsgServerToGCRequestPlayerRecentAccomplishmentsResponse.EResponse
    player_accomplishments: CMsgRecentAccomplishments
    def __init__(self, result: _Optional[_Union[CMsgServerToGCRequestPlayerRecentAccomplishmentsResponse.EResponse, str]] = ..., player_accomplishments: _Optional[_Union[CMsgRecentAccomplishments, _Mapping]] = ...) -> None: ...

class CMsgArcanaVoteMatchVotes(_message.Message):
    __slots__ = ("match_id", "hero_id", "vote_count")
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    VOTE_COUNT_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    hero_id: int
    vote_count: int
    def __init__(self, match_id: _Optional[int] = ..., hero_id: _Optional[int] = ..., vote_count: _Optional[int] = ...) -> None: ...

class CMsgGCtoGCAssociatedExploiterAccountInfo(_message.Message):
    __slots__ = ("account_id", "num_matches_to_search", "min_shared_match_count", "num_additional_players")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    NUM_MATCHES_TO_SEARCH_FIELD_NUMBER: _ClassVar[int]
    MIN_SHARED_MATCH_COUNT_FIELD_NUMBER: _ClassVar[int]
    NUM_ADDITIONAL_PLAYERS_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    num_matches_to_search: int
    min_shared_match_count: int
    num_additional_players: int
    def __init__(self, account_id: _Optional[int] = ..., num_matches_to_search: _Optional[int] = ..., min_shared_match_count: _Optional[int] = ..., num_additional_players: _Optional[int] = ...) -> None: ...

class CMsgGCtoGCAssociatedExploiterAccountInfoResponse(_message.Message):
    __slots__ = ("accounts",)
    class Account(_message.Message):
        __slots__ = ("account_id", "num_common_matches", "earliest_common_match", "latest_common_match", "generation", "persona", "already_banned")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        NUM_COMMON_MATCHES_FIELD_NUMBER: _ClassVar[int]
        EARLIEST_COMMON_MATCH_FIELD_NUMBER: _ClassVar[int]
        LATEST_COMMON_MATCH_FIELD_NUMBER: _ClassVar[int]
        GENERATION_FIELD_NUMBER: _ClassVar[int]
        PERSONA_FIELD_NUMBER: _ClassVar[int]
        ALREADY_BANNED_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        num_common_matches: int
        earliest_common_match: int
        latest_common_match: int
        generation: int
        persona: str
        already_banned: bool
        def __init__(self, account_id: _Optional[int] = ..., num_common_matches: _Optional[int] = ..., earliest_common_match: _Optional[int] = ..., latest_common_match: _Optional[int] = ..., generation: _Optional[int] = ..., persona: _Optional[str] = ..., already_banned: bool = ...) -> None: ...
    ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    accounts: _containers.RepeatedCompositeFieldContainer[CMsgGCtoGCAssociatedExploiterAccountInfoResponse.Account]
    def __init__(self, accounts: _Optional[_Iterable[_Union[CMsgGCtoGCAssociatedExploiterAccountInfoResponse.Account, _Mapping]]] = ...) -> None: ...

class CMsgPullTabsData(_message.Message):
    __slots__ = ("slots", "jackpots", "last_board")
    class Slot(_message.Message):
        __slots__ = ("event_id", "board_id", "hero_id", "action_id", "redeemed")
        EVENT_ID_FIELD_NUMBER: _ClassVar[int]
        BOARD_ID_FIELD_NUMBER: _ClassVar[int]
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        ACTION_ID_FIELD_NUMBER: _ClassVar[int]
        REDEEMED_FIELD_NUMBER: _ClassVar[int]
        event_id: int
        board_id: int
        hero_id: int
        action_id: int
        redeemed: bool
        def __init__(self, event_id: _Optional[int] = ..., board_id: _Optional[int] = ..., hero_id: _Optional[int] = ..., action_id: _Optional[int] = ..., redeemed: bool = ...) -> None: ...
    class Jackpot(_message.Message):
        __slots__ = ("board_id", "action_id", "hero_id")
        BOARD_ID_FIELD_NUMBER: _ClassVar[int]
        ACTION_ID_FIELD_NUMBER: _ClassVar[int]
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        board_id: int
        action_id: int
        hero_id: int
        def __init__(self, board_id: _Optional[int] = ..., action_id: _Optional[int] = ..., hero_id: _Optional[int] = ...) -> None: ...
    SLOTS_FIELD_NUMBER: _ClassVar[int]
    JACKPOTS_FIELD_NUMBER: _ClassVar[int]
    LAST_BOARD_FIELD_NUMBER: _ClassVar[int]
    slots: _containers.RepeatedCompositeFieldContainer[CMsgPullTabsData.Slot]
    jackpots: _containers.RepeatedCompositeFieldContainer[CMsgPullTabsData.Jackpot]
    last_board: int
    def __init__(self, slots: _Optional[_Iterable[_Union[CMsgPullTabsData.Slot, _Mapping]]] = ..., jackpots: _Optional[_Iterable[_Union[CMsgPullTabsData.Jackpot, _Mapping]]] = ..., last_board: _Optional[int] = ...) -> None: ...

class CMsgUnderDraftData(_message.Message):
    __slots__ = ("bench_slots", "shop_slots", "gold", "total_gold", "not_restorable")
    class BenchSlot(_message.Message):
        __slots__ = ("slot_id", "hero_id", "stars")
        SLOT_ID_FIELD_NUMBER: _ClassVar[int]
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        STARS_FIELD_NUMBER: _ClassVar[int]
        slot_id: int
        hero_id: int
        stars: int
        def __init__(self, slot_id: _Optional[int] = ..., hero_id: _Optional[int] = ..., stars: _Optional[int] = ...) -> None: ...
    class ShopSlot(_message.Message):
        __slots__ = ("slot_id", "hero_id", "is_special_reward")
        SLOT_ID_FIELD_NUMBER: _ClassVar[int]
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        IS_SPECIAL_REWARD_FIELD_NUMBER: _ClassVar[int]
        slot_id: int
        hero_id: int
        is_special_reward: bool
        def __init__(self, slot_id: _Optional[int] = ..., hero_id: _Optional[int] = ..., is_special_reward: bool = ...) -> None: ...
    BENCH_SLOTS_FIELD_NUMBER: _ClassVar[int]
    SHOP_SLOTS_FIELD_NUMBER: _ClassVar[int]
    GOLD_FIELD_NUMBER: _ClassVar[int]
    TOTAL_GOLD_FIELD_NUMBER: _ClassVar[int]
    NOT_RESTORABLE_FIELD_NUMBER: _ClassVar[int]
    bench_slots: _containers.RepeatedCompositeFieldContainer[CMsgUnderDraftData.BenchSlot]
    shop_slots: _containers.RepeatedCompositeFieldContainer[CMsgUnderDraftData.ShopSlot]
    gold: int
    total_gold: int
    not_restorable: bool
    def __init__(self, bench_slots: _Optional[_Iterable[_Union[CMsgUnderDraftData.BenchSlot, _Mapping]]] = ..., shop_slots: _Optional[_Iterable[_Union[CMsgUnderDraftData.ShopSlot, _Mapping]]] = ..., gold: _Optional[int] = ..., total_gold: _Optional[int] = ..., not_restorable: bool = ...) -> None: ...

class CMsgPlayerTitleData(_message.Message):
    __slots__ = ("title", "event_id", "active")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    title: _containers.RepeatedScalarFieldContainer[int]
    event_id: _containers.RepeatedScalarFieldContainer[int]
    active: int
    def __init__(self, title: _Optional[_Iterable[int]] = ..., event_id: _Optional[_Iterable[int]] = ..., active: _Optional[int] = ...) -> None: ...

class CMsgDOTATriviaQuestion(_message.Message):
    __slots__ = ("question_id", "category", "timestamp", "question_value", "answer_values", "correct_answer_index")
    QUESTION_ID_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    QUESTION_VALUE_FIELD_NUMBER: _ClassVar[int]
    ANSWER_VALUES_FIELD_NUMBER: _ClassVar[int]
    CORRECT_ANSWER_INDEX_FIELD_NUMBER: _ClassVar[int]
    question_id: int
    category: EDOTATriviaQuestionCategory
    timestamp: int
    question_value: str
    answer_values: _containers.RepeatedScalarFieldContainer[str]
    correct_answer_index: int
    def __init__(self, question_id: _Optional[int] = ..., category: _Optional[_Union[EDOTATriviaQuestionCategory, str]] = ..., timestamp: _Optional[int] = ..., question_value: _Optional[str] = ..., answer_values: _Optional[_Iterable[str]] = ..., correct_answer_index: _Optional[int] = ...) -> None: ...

class CMsgDOTATriviaQuestionAnswersSummary(_message.Message):
    __slots__ = ("summary_available", "picked_count")
    SUMMARY_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    PICKED_COUNT_FIELD_NUMBER: _ClassVar[int]
    summary_available: bool
    picked_count: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, summary_available: bool = ..., picked_count: _Optional[_Iterable[int]] = ...) -> None: ...

class CMsgGameDataSpecialValueBonus(_message.Message):
    __slots__ = ("name", "value", "operation")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: float
    operation: int
    def __init__(self, name: _Optional[str] = ..., value: _Optional[float] = ..., operation: _Optional[int] = ...) -> None: ...

class CMsgGameDataSpecialValues(_message.Message):
    __slots__ = ("name", "values_float", "is_percentage", "heading_loc", "bonuses", "values_shard", "values_scepter", "facet_bonus", "required_facet")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUES_FLOAT_FIELD_NUMBER: _ClassVar[int]
    IS_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    HEADING_LOC_FIELD_NUMBER: _ClassVar[int]
    BONUSES_FIELD_NUMBER: _ClassVar[int]
    VALUES_SHARD_FIELD_NUMBER: _ClassVar[int]
    VALUES_SCEPTER_FIELD_NUMBER: _ClassVar[int]
    FACET_BONUS_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_FACET_FIELD_NUMBER: _ClassVar[int]
    name: str
    values_float: _containers.RepeatedScalarFieldContainer[float]
    is_percentage: bool
    heading_loc: str
    bonuses: _containers.RepeatedCompositeFieldContainer[CMsgGameDataSpecialValueBonus]
    values_shard: _containers.RepeatedScalarFieldContainer[float]
    values_scepter: _containers.RepeatedScalarFieldContainer[float]
    facet_bonus: CMsgGameDataFacetAbilityBonus
    required_facet: str
    def __init__(self, name: _Optional[str] = ..., values_float: _Optional[_Iterable[float]] = ..., is_percentage: bool = ..., heading_loc: _Optional[str] = ..., bonuses: _Optional[_Iterable[_Union[CMsgGameDataSpecialValueBonus, _Mapping]]] = ..., values_shard: _Optional[_Iterable[float]] = ..., values_scepter: _Optional[_Iterable[float]] = ..., facet_bonus: _Optional[_Union[CMsgGameDataFacetAbilityBonus, _Mapping]] = ..., required_facet: _Optional[str] = ...) -> None: ...

class CMsgGameDataFacetAbilityBonus(_message.Message):
    __slots__ = ("name", "values", "operation")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    name: str
    values: _containers.RepeatedScalarFieldContainer[float]
    operation: int
    def __init__(self, name: _Optional[str] = ..., values: _Optional[_Iterable[float]] = ..., operation: _Optional[int] = ...) -> None: ...

class CMsgGameDataAbilityOrItem(_message.Message):
    __slots__ = ("id", "name", "name_loc", "desc_loc", "lore_loc", "notes_loc", "shard_loc", "scepter_loc", "facets_loc", "type", "behavior", "target_team", "target_type", "flags", "damage", "immunity", "dispellable", "max_level", "cast_ranges", "cast_points", "channel_times", "cooldowns", "durations", "damages", "mana_costs", "gold_costs", "health_costs", "special_values", "is_item", "ability_has_scepter", "ability_has_shard", "ability_is_granted_by_scepter", "ability_is_granted_by_shard", "ability_is_innate", "item_cost", "item_initial_charges", "item_neutral_tier", "item_stock_max", "item_stock_time", "item_quality")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_LOC_FIELD_NUMBER: _ClassVar[int]
    DESC_LOC_FIELD_NUMBER: _ClassVar[int]
    LORE_LOC_FIELD_NUMBER: _ClassVar[int]
    NOTES_LOC_FIELD_NUMBER: _ClassVar[int]
    SHARD_LOC_FIELD_NUMBER: _ClassVar[int]
    SCEPTER_LOC_FIELD_NUMBER: _ClassVar[int]
    FACETS_LOC_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    TARGET_TEAM_FIELD_NUMBER: _ClassVar[int]
    TARGET_TYPE_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    DAMAGE_FIELD_NUMBER: _ClassVar[int]
    IMMUNITY_FIELD_NUMBER: _ClassVar[int]
    DISPELLABLE_FIELD_NUMBER: _ClassVar[int]
    MAX_LEVEL_FIELD_NUMBER: _ClassVar[int]
    CAST_RANGES_FIELD_NUMBER: _ClassVar[int]
    CAST_POINTS_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_TIMES_FIELD_NUMBER: _ClassVar[int]
    COOLDOWNS_FIELD_NUMBER: _ClassVar[int]
    DURATIONS_FIELD_NUMBER: _ClassVar[int]
    DAMAGES_FIELD_NUMBER: _ClassVar[int]
    MANA_COSTS_FIELD_NUMBER: _ClassVar[int]
    GOLD_COSTS_FIELD_NUMBER: _ClassVar[int]
    HEALTH_COSTS_FIELD_NUMBER: _ClassVar[int]
    SPECIAL_VALUES_FIELD_NUMBER: _ClassVar[int]
    IS_ITEM_FIELD_NUMBER: _ClassVar[int]
    ABILITY_HAS_SCEPTER_FIELD_NUMBER: _ClassVar[int]
    ABILITY_HAS_SHARD_FIELD_NUMBER: _ClassVar[int]
    ABILITY_IS_GRANTED_BY_SCEPTER_FIELD_NUMBER: _ClassVar[int]
    ABILITY_IS_GRANTED_BY_SHARD_FIELD_NUMBER: _ClassVar[int]
    ABILITY_IS_INNATE_FIELD_NUMBER: _ClassVar[int]
    ITEM_COST_FIELD_NUMBER: _ClassVar[int]
    ITEM_INITIAL_CHARGES_FIELD_NUMBER: _ClassVar[int]
    ITEM_NEUTRAL_TIER_FIELD_NUMBER: _ClassVar[int]
    ITEM_STOCK_MAX_FIELD_NUMBER: _ClassVar[int]
    ITEM_STOCK_TIME_FIELD_NUMBER: _ClassVar[int]
    ITEM_QUALITY_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    name_loc: str
    desc_loc: str
    lore_loc: str
    notes_loc: _containers.RepeatedScalarFieldContainer[str]
    shard_loc: str
    scepter_loc: str
    facets_loc: _containers.RepeatedScalarFieldContainer[str]
    type: int
    behavior: int
    target_team: int
    target_type: int
    flags: int
    damage: int
    immunity: int
    dispellable: int
    max_level: int
    cast_ranges: _containers.RepeatedScalarFieldContainer[int]
    cast_points: _containers.RepeatedScalarFieldContainer[float]
    channel_times: _containers.RepeatedScalarFieldContainer[float]
    cooldowns: _containers.RepeatedScalarFieldContainer[float]
    durations: _containers.RepeatedScalarFieldContainer[float]
    damages: _containers.RepeatedScalarFieldContainer[int]
    mana_costs: _containers.RepeatedScalarFieldContainer[int]
    gold_costs: _containers.RepeatedScalarFieldContainer[int]
    health_costs: _containers.RepeatedScalarFieldContainer[int]
    special_values: _containers.RepeatedCompositeFieldContainer[CMsgGameDataSpecialValues]
    is_item: bool
    ability_has_scepter: bool
    ability_has_shard: bool
    ability_is_granted_by_scepter: bool
    ability_is_granted_by_shard: bool
    ability_is_innate: bool
    item_cost: int
    item_initial_charges: int
    item_neutral_tier: int
    item_stock_max: int
    item_stock_time: float
    item_quality: int
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., name_loc: _Optional[str] = ..., desc_loc: _Optional[str] = ..., lore_loc: _Optional[str] = ..., notes_loc: _Optional[_Iterable[str]] = ..., shard_loc: _Optional[str] = ..., scepter_loc: _Optional[str] = ..., facets_loc: _Optional[_Iterable[str]] = ..., type: _Optional[int] = ..., behavior: _Optional[int] = ..., target_team: _Optional[int] = ..., target_type: _Optional[int] = ..., flags: _Optional[int] = ..., damage: _Optional[int] = ..., immunity: _Optional[int] = ..., dispellable: _Optional[int] = ..., max_level: _Optional[int] = ..., cast_ranges: _Optional[_Iterable[int]] = ..., cast_points: _Optional[_Iterable[float]] = ..., channel_times: _Optional[_Iterable[float]] = ..., cooldowns: _Optional[_Iterable[float]] = ..., durations: _Optional[_Iterable[float]] = ..., damages: _Optional[_Iterable[int]] = ..., mana_costs: _Optional[_Iterable[int]] = ..., gold_costs: _Optional[_Iterable[int]] = ..., health_costs: _Optional[_Iterable[int]] = ..., special_values: _Optional[_Iterable[_Union[CMsgGameDataSpecialValues, _Mapping]]] = ..., is_item: bool = ..., ability_has_scepter: bool = ..., ability_has_shard: bool = ..., ability_is_granted_by_scepter: bool = ..., ability_is_granted_by_shard: bool = ..., ability_is_innate: bool = ..., item_cost: _Optional[int] = ..., item_initial_charges: _Optional[int] = ..., item_neutral_tier: _Optional[int] = ..., item_stock_max: _Optional[int] = ..., item_stock_time: _Optional[float] = ..., item_quality: _Optional[int] = ...) -> None: ...

class CMsgGameDataAbilityOrItemList(_message.Message):
    __slots__ = ("abilities",)
    ABILITIES_FIELD_NUMBER: _ClassVar[int]
    abilities: _containers.RepeatedCompositeFieldContainer[CMsgGameDataAbilityOrItem]
    def __init__(self, abilities: _Optional[_Iterable[_Union[CMsgGameDataAbilityOrItem, _Mapping]]] = ...) -> None: ...

class CMsgGameDataHero(_message.Message):
    __slots__ = ("id", "name", "order_id", "name_loc", "bio_loc", "hype_loc", "npe_desc_loc", "facets", "str_base", "str_gain", "agi_base", "agi_gain", "int_base", "int_gain", "primary_attr", "complexity", "attack_capability", "role_levels", "damage_min", "damage_max", "attack_rate", "attack_range", "projectile_speed", "armor", "magic_resistance", "movement_speed", "turn_rate", "sight_range_day", "sight_range_night", "max_health", "health_regen", "max_mana", "mana_regen", "abilities", "talents", "facet_abilities")
    class Facet(_message.Message):
        __slots__ = ("color", "title_loc", "description_loc", "name", "icon", "gradient_id", "index")
        COLOR_FIELD_NUMBER: _ClassVar[int]
        TITLE_LOC_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_LOC_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        ICON_FIELD_NUMBER: _ClassVar[int]
        GRADIENT_ID_FIELD_NUMBER: _ClassVar[int]
        INDEX_FIELD_NUMBER: _ClassVar[int]
        color: int
        title_loc: str
        description_loc: str
        name: str
        icon: str
        gradient_id: int
        index: int
        def __init__(self, color: _Optional[int] = ..., title_loc: _Optional[str] = ..., description_loc: _Optional[str] = ..., name: _Optional[str] = ..., icon: _Optional[str] = ..., gradient_id: _Optional[int] = ..., index: _Optional[int] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_LOC_FIELD_NUMBER: _ClassVar[int]
    BIO_LOC_FIELD_NUMBER: _ClassVar[int]
    HYPE_LOC_FIELD_NUMBER: _ClassVar[int]
    NPE_DESC_LOC_FIELD_NUMBER: _ClassVar[int]
    FACETS_FIELD_NUMBER: _ClassVar[int]
    STR_BASE_FIELD_NUMBER: _ClassVar[int]
    STR_GAIN_FIELD_NUMBER: _ClassVar[int]
    AGI_BASE_FIELD_NUMBER: _ClassVar[int]
    AGI_GAIN_FIELD_NUMBER: _ClassVar[int]
    INT_BASE_FIELD_NUMBER: _ClassVar[int]
    INT_GAIN_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_ATTR_FIELD_NUMBER: _ClassVar[int]
    COMPLEXITY_FIELD_NUMBER: _ClassVar[int]
    ATTACK_CAPABILITY_FIELD_NUMBER: _ClassVar[int]
    ROLE_LEVELS_FIELD_NUMBER: _ClassVar[int]
    DAMAGE_MIN_FIELD_NUMBER: _ClassVar[int]
    DAMAGE_MAX_FIELD_NUMBER: _ClassVar[int]
    ATTACK_RATE_FIELD_NUMBER: _ClassVar[int]
    ATTACK_RANGE_FIELD_NUMBER: _ClassVar[int]
    PROJECTILE_SPEED_FIELD_NUMBER: _ClassVar[int]
    ARMOR_FIELD_NUMBER: _ClassVar[int]
    MAGIC_RESISTANCE_FIELD_NUMBER: _ClassVar[int]
    MOVEMENT_SPEED_FIELD_NUMBER: _ClassVar[int]
    TURN_RATE_FIELD_NUMBER: _ClassVar[int]
    SIGHT_RANGE_DAY_FIELD_NUMBER: _ClassVar[int]
    SIGHT_RANGE_NIGHT_FIELD_NUMBER: _ClassVar[int]
    MAX_HEALTH_FIELD_NUMBER: _ClassVar[int]
    HEALTH_REGEN_FIELD_NUMBER: _ClassVar[int]
    MAX_MANA_FIELD_NUMBER: _ClassVar[int]
    MANA_REGEN_FIELD_NUMBER: _ClassVar[int]
    ABILITIES_FIELD_NUMBER: _ClassVar[int]
    TALENTS_FIELD_NUMBER: _ClassVar[int]
    FACET_ABILITIES_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    order_id: int
    name_loc: str
    bio_loc: str
    hype_loc: str
    npe_desc_loc: str
    facets: _containers.RepeatedCompositeFieldContainer[CMsgGameDataHero.Facet]
    str_base: int
    str_gain: float
    agi_base: int
    agi_gain: float
    int_base: int
    int_gain: float
    primary_attr: int
    complexity: int
    attack_capability: int
    role_levels: _containers.RepeatedScalarFieldContainer[int]
    damage_min: int
    damage_max: int
    attack_rate: float
    attack_range: int
    projectile_speed: int
    armor: float
    magic_resistance: int
    movement_speed: int
    turn_rate: float
    sight_range_day: int
    sight_range_night: int
    max_health: int
    health_regen: float
    max_mana: int
    mana_regen: float
    abilities: _containers.RepeatedCompositeFieldContainer[CMsgGameDataAbilityOrItem]
    talents: _containers.RepeatedCompositeFieldContainer[CMsgGameDataAbilityOrItem]
    facet_abilities: _containers.RepeatedCompositeFieldContainer[CMsgGameDataAbilityOrItemList]
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., order_id: _Optional[int] = ..., name_loc: _Optional[str] = ..., bio_loc: _Optional[str] = ..., hype_loc: _Optional[str] = ..., npe_desc_loc: _Optional[str] = ..., facets: _Optional[_Iterable[_Union[CMsgGameDataHero.Facet, _Mapping]]] = ..., str_base: _Optional[int] = ..., str_gain: _Optional[float] = ..., agi_base: _Optional[int] = ..., agi_gain: _Optional[float] = ..., int_base: _Optional[int] = ..., int_gain: _Optional[float] = ..., primary_attr: _Optional[int] = ..., complexity: _Optional[int] = ..., attack_capability: _Optional[int] = ..., role_levels: _Optional[_Iterable[int]] = ..., damage_min: _Optional[int] = ..., damage_max: _Optional[int] = ..., attack_rate: _Optional[float] = ..., attack_range: _Optional[int] = ..., projectile_speed: _Optional[int] = ..., armor: _Optional[float] = ..., magic_resistance: _Optional[int] = ..., movement_speed: _Optional[int] = ..., turn_rate: _Optional[float] = ..., sight_range_day: _Optional[int] = ..., sight_range_night: _Optional[int] = ..., max_health: _Optional[int] = ..., health_regen: _Optional[float] = ..., max_mana: _Optional[int] = ..., mana_regen: _Optional[float] = ..., abilities: _Optional[_Iterable[_Union[CMsgGameDataAbilityOrItem, _Mapping]]] = ..., talents: _Optional[_Iterable[_Union[CMsgGameDataAbilityOrItem, _Mapping]]] = ..., facet_abilities: _Optional[_Iterable[_Union[CMsgGameDataAbilityOrItemList, _Mapping]]] = ...) -> None: ...

class CMsgGameDataAbilities(_message.Message):
    __slots__ = ("abilities",)
    ABILITIES_FIELD_NUMBER: _ClassVar[int]
    abilities: _containers.RepeatedCompositeFieldContainer[CMsgGameDataAbilityOrItem]
    def __init__(self, abilities: _Optional[_Iterable[_Union[CMsgGameDataAbilityOrItem, _Mapping]]] = ...) -> None: ...

class CMsgGameDataItems(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[CMsgGameDataAbilityOrItem]
    def __init__(self, items: _Optional[_Iterable[_Union[CMsgGameDataAbilityOrItem, _Mapping]]] = ...) -> None: ...

class CMsgGameDataHeroes(_message.Message):
    __slots__ = ("heroes",)
    HEROES_FIELD_NUMBER: _ClassVar[int]
    heroes: _containers.RepeatedCompositeFieldContainer[CMsgGameDataHero]
    def __init__(self, heroes: _Optional[_Iterable[_Union[CMsgGameDataHero, _Mapping]]] = ...) -> None: ...

class CMsgGameDataHeroList(_message.Message):
    __slots__ = ("heroes",)
    class HeroInfo(_message.Message):
        __slots__ = ("id", "name", "name_loc", "name_english_loc", "primary_attr", "complexity")
        ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        NAME_LOC_FIELD_NUMBER: _ClassVar[int]
        NAME_ENGLISH_LOC_FIELD_NUMBER: _ClassVar[int]
        PRIMARY_ATTR_FIELD_NUMBER: _ClassVar[int]
        COMPLEXITY_FIELD_NUMBER: _ClassVar[int]
        id: int
        name: str
        name_loc: str
        name_english_loc: str
        primary_attr: int
        complexity: int
        def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., name_loc: _Optional[str] = ..., name_english_loc: _Optional[str] = ..., primary_attr: _Optional[int] = ..., complexity: _Optional[int] = ...) -> None: ...
    HEROES_FIELD_NUMBER: _ClassVar[int]
    heroes: _containers.RepeatedCompositeFieldContainer[CMsgGameDataHeroList.HeroInfo]
    def __init__(self, heroes: _Optional[_Iterable[_Union[CMsgGameDataHeroList.HeroInfo, _Mapping]]] = ...) -> None: ...

class CMsgGameDataItemAbilityList(_message.Message):
    __slots__ = ("itemabilities",)
    class ItemAbilityInfo(_message.Message):
        __slots__ = ("id", "name", "name_loc", "name_english_loc", "neutral_item_tier", "is_pregame_suggested", "is_earlygame_suggested", "is_lategame_suggested", "recipes", "is_innate")
        class Recipe(_message.Message):
            __slots__ = ("items",)
            ITEMS_FIELD_NUMBER: _ClassVar[int]
            items: _containers.RepeatedScalarFieldContainer[int]
            def __init__(self, items: _Optional[_Iterable[int]] = ...) -> None: ...
        ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        NAME_LOC_FIELD_NUMBER: _ClassVar[int]
        NAME_ENGLISH_LOC_FIELD_NUMBER: _ClassVar[int]
        NEUTRAL_ITEM_TIER_FIELD_NUMBER: _ClassVar[int]
        IS_PREGAME_SUGGESTED_FIELD_NUMBER: _ClassVar[int]
        IS_EARLYGAME_SUGGESTED_FIELD_NUMBER: _ClassVar[int]
        IS_LATEGAME_SUGGESTED_FIELD_NUMBER: _ClassVar[int]
        RECIPES_FIELD_NUMBER: _ClassVar[int]
        IS_INNATE_FIELD_NUMBER: _ClassVar[int]
        id: int
        name: str
        name_loc: str
        name_english_loc: str
        neutral_item_tier: int
        is_pregame_suggested: bool
        is_earlygame_suggested: bool
        is_lategame_suggested: bool
        recipes: _containers.RepeatedCompositeFieldContainer[CMsgGameDataItemAbilityList.ItemAbilityInfo.Recipe]
        is_innate: bool
        def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., name_loc: _Optional[str] = ..., name_english_loc: _Optional[str] = ..., neutral_item_tier: _Optional[int] = ..., is_pregame_suggested: bool = ..., is_earlygame_suggested: bool = ..., is_lategame_suggested: bool = ..., recipes: _Optional[_Iterable[_Union[CMsgGameDataItemAbilityList.ItemAbilityInfo.Recipe, _Mapping]]] = ..., is_innate: bool = ...) -> None: ...
    ITEMABILITIES_FIELD_NUMBER: _ClassVar[int]
    itemabilities: _containers.RepeatedCompositeFieldContainer[CMsgGameDataItemAbilityList.ItemAbilityInfo]
    def __init__(self, itemabilities: _Optional[_Iterable[_Union[CMsgGameDataItemAbilityList.ItemAbilityInfo, _Mapping]]] = ...) -> None: ...

class CMsgLobbyAbilityDraftData(_message.Message):
    __slots__ = ("shuffle_draft_order",)
    SHUFFLE_DRAFT_ORDER_FIELD_NUMBER: _ClassVar[int]
    shuffle_draft_order: bool
    def __init__(self, shuffle_draft_order: bool = ...) -> None: ...

class CSOEconItemDropRateBonus(_message.Message):
    __slots__ = ("account_id", "expiration_date", "bonus", "bonus_count", "item_id", "def_index", "seconds_left", "booster_type")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_DATE_FIELD_NUMBER: _ClassVar[int]
    BONUS_FIELD_NUMBER: _ClassVar[int]
    BONUS_COUNT_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
    SECONDS_LEFT_FIELD_NUMBER: _ClassVar[int]
    BOOSTER_TYPE_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    expiration_date: int
    bonus: float
    bonus_count: int
    item_id: int
    def_index: int
    seconds_left: int
    booster_type: int
    def __init__(self, account_id: _Optional[int] = ..., expiration_date: _Optional[int] = ..., bonus: _Optional[float] = ..., bonus_count: _Optional[int] = ..., item_id: _Optional[int] = ..., def_index: _Optional[int] = ..., seconds_left: _Optional[int] = ..., booster_type: _Optional[int] = ...) -> None: ...

class CSOEconItemTournamentPassport(_message.Message):
    __slots__ = ("account_id", "league_id", "item_id", "original_purchaser_id", "passports_bought", "version", "def_index", "reward_flags")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_PURCHASER_ID_FIELD_NUMBER: _ClassVar[int]
    PASSPORTS_BOUGHT_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
    REWARD_FLAGS_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    league_id: int
    item_id: int
    original_purchaser_id: int
    passports_bought: int
    version: int
    def_index: int
    reward_flags: int
    def __init__(self, account_id: _Optional[int] = ..., league_id: _Optional[int] = ..., item_id: _Optional[int] = ..., original_purchaser_id: _Optional[int] = ..., passports_bought: _Optional[int] = ..., version: _Optional[int] = ..., def_index: _Optional[int] = ..., reward_flags: _Optional[int] = ...) -> None: ...

class CMsgStickerbookSticker(_message.Message):
    __slots__ = ("item_def_id", "sticker_num", "quality", "position_x", "position_y", "position_z", "rotation", "scale", "source_item_id", "depth_bias")
    ITEM_DEF_ID_FIELD_NUMBER: _ClassVar[int]
    STICKER_NUM_FIELD_NUMBER: _ClassVar[int]
    QUALITY_FIELD_NUMBER: _ClassVar[int]
    POSITION_X_FIELD_NUMBER: _ClassVar[int]
    POSITION_Y_FIELD_NUMBER: _ClassVar[int]
    POSITION_Z_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    SCALE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    DEPTH_BIAS_FIELD_NUMBER: _ClassVar[int]
    item_def_id: int
    sticker_num: int
    quality: int
    position_x: float
    position_y: float
    position_z: float
    rotation: float
    scale: float
    source_item_id: int
    depth_bias: int
    def __init__(self, item_def_id: _Optional[int] = ..., sticker_num: _Optional[int] = ..., quality: _Optional[int] = ..., position_x: _Optional[float] = ..., position_y: _Optional[float] = ..., position_z: _Optional[float] = ..., rotation: _Optional[float] = ..., scale: _Optional[float] = ..., source_item_id: _Optional[int] = ..., depth_bias: _Optional[int] = ...) -> None: ...

class CMsgStickerbookPage(_message.Message):
    __slots__ = ("page_num", "event_id", "team_id", "stickers", "page_type")
    PAGE_NUM_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    STICKERS_FIELD_NUMBER: _ClassVar[int]
    PAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    page_num: int
    event_id: _dota_shared_enums_pb2.EEvent
    team_id: int
    stickers: _containers.RepeatedCompositeFieldContainer[CMsgStickerbookSticker]
    page_type: EStickerbookPageType
    def __init__(self, page_num: _Optional[int] = ..., event_id: _Optional[_Union[_dota_shared_enums_pb2.EEvent, str]] = ..., team_id: _Optional[int] = ..., stickers: _Optional[_Iterable[_Union[CMsgStickerbookSticker, _Mapping]]] = ..., page_type: _Optional[_Union[EStickerbookPageType, str]] = ...) -> None: ...

class CMsgStickerbookTeamPageOrderSequence(_message.Message):
    __slots__ = ("page_numbers",)
    PAGE_NUMBERS_FIELD_NUMBER: _ClassVar[int]
    page_numbers: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, page_numbers: _Optional[_Iterable[int]] = ...) -> None: ...

class CMsgStickerbook(_message.Message):
    __slots__ = ("pages", "team_page_order_sequence", "favorite_page_num")
    PAGES_FIELD_NUMBER: _ClassVar[int]
    TEAM_PAGE_ORDER_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    FAVORITE_PAGE_NUM_FIELD_NUMBER: _ClassVar[int]
    pages: _containers.RepeatedCompositeFieldContainer[CMsgStickerbookPage]
    team_page_order_sequence: CMsgStickerbookTeamPageOrderSequence
    favorite_page_num: int
    def __init__(self, pages: _Optional[_Iterable[_Union[CMsgStickerbookPage, _Mapping]]] = ..., team_page_order_sequence: _Optional[_Union[CMsgStickerbookTeamPageOrderSequence, _Mapping]] = ..., favorite_page_num: _Optional[int] = ...) -> None: ...

class CMsgStickerHero(_message.Message):
    __slots__ = ("hero_id", "item_def_id", "quality", "source_item_id")
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_DEF_ID_FIELD_NUMBER: _ClassVar[int]
    QUALITY_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    hero_id: int
    item_def_id: int
    quality: int
    source_item_id: int
    def __init__(self, hero_id: _Optional[int] = ..., item_def_id: _Optional[int] = ..., quality: _Optional[int] = ..., source_item_id: _Optional[int] = ...) -> None: ...

class CMsgStickerHeroes(_message.Message):
    __slots__ = ("heroes",)
    HEROES_FIELD_NUMBER: _ClassVar[int]
    heroes: _containers.RepeatedCompositeFieldContainer[CMsgStickerHero]
    def __init__(self, heroes: _Optional[_Iterable[_Union[CMsgStickerHero, _Mapping]]] = ...) -> None: ...

class CMsgHeroRoleStats(_message.Message):
    __slots__ = ("lane_selection_flags", "match_count", "win_count")
    LANE_SELECTION_FLAGS_FIELD_NUMBER: _ClassVar[int]
    MATCH_COUNT_FIELD_NUMBER: _ClassVar[int]
    WIN_COUNT_FIELD_NUMBER: _ClassVar[int]
    lane_selection_flags: int
    match_count: int
    win_count: int
    def __init__(self, lane_selection_flags: _Optional[int] = ..., match_count: _Optional[int] = ..., win_count: _Optional[int] = ...) -> None: ...

class CMsgHeroRoleHeroStats(_message.Message):
    __slots__ = ("hero_id", "role_stats")
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_STATS_FIELD_NUMBER: _ClassVar[int]
    hero_id: int
    role_stats: _containers.RepeatedCompositeFieldContainer[CMsgHeroRoleStats]
    def __init__(self, hero_id: _Optional[int] = ..., role_stats: _Optional[_Iterable[_Union[CMsgHeroRoleStats, _Mapping]]] = ...) -> None: ...

class CMsgHeroRoleRankStats(_message.Message):
    __slots__ = ("rank_tier", "hero_stats")
    RANK_TIER_FIELD_NUMBER: _ClassVar[int]
    HERO_STATS_FIELD_NUMBER: _ClassVar[int]
    rank_tier: int
    hero_stats: _containers.RepeatedCompositeFieldContainer[CMsgHeroRoleHeroStats]
    def __init__(self, rank_tier: _Optional[int] = ..., hero_stats: _Optional[_Iterable[_Union[CMsgHeroRoleHeroStats, _Mapping]]] = ...) -> None: ...

class CMsgHeroRoleAllRanksStats(_message.Message):
    __slots__ = ("start_timestamp", "end_timestamp", "rank_stats")
    START_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    END_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    RANK_STATS_FIELD_NUMBER: _ClassVar[int]
    start_timestamp: int
    end_timestamp: int
    rank_stats: _containers.RepeatedCompositeFieldContainer[CMsgHeroRoleRankStats]
    def __init__(self, start_timestamp: _Optional[int] = ..., end_timestamp: _Optional[int] = ..., rank_stats: _Optional[_Iterable[_Union[CMsgHeroRoleRankStats, _Mapping]]] = ...) -> None: ...

class CMsgMapStatsSnapshot(_message.Message):
    __slots__ = ("timestamp", "lotuses_gained", "wisdom_runes_gained", "roshan_kills_day", "roshan_kills_night", "portals_used", "watchers_taken", "tormentor_kills", "outposts_captured", "shield_runes_gained")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LOTUSES_GAINED_FIELD_NUMBER: _ClassVar[int]
    WISDOM_RUNES_GAINED_FIELD_NUMBER: _ClassVar[int]
    ROSHAN_KILLS_DAY_FIELD_NUMBER: _ClassVar[int]
    ROSHAN_KILLS_NIGHT_FIELD_NUMBER: _ClassVar[int]
    PORTALS_USED_FIELD_NUMBER: _ClassVar[int]
    WATCHERS_TAKEN_FIELD_NUMBER: _ClassVar[int]
    TORMENTOR_KILLS_FIELD_NUMBER: _ClassVar[int]
    OUTPOSTS_CAPTURED_FIELD_NUMBER: _ClassVar[int]
    SHIELD_RUNES_GAINED_FIELD_NUMBER: _ClassVar[int]
    timestamp: int
    lotuses_gained: int
    wisdom_runes_gained: int
    roshan_kills_day: int
    roshan_kills_night: int
    portals_used: int
    watchers_taken: int
    tormentor_kills: int
    outposts_captured: int
    shield_runes_gained: int
    def __init__(self, timestamp: _Optional[int] = ..., lotuses_gained: _Optional[int] = ..., wisdom_runes_gained: _Optional[int] = ..., roshan_kills_day: _Optional[int] = ..., roshan_kills_night: _Optional[int] = ..., portals_used: _Optional[int] = ..., watchers_taken: _Optional[int] = ..., tormentor_kills: _Optional[int] = ..., outposts_captured: _Optional[int] = ..., shield_runes_gained: _Optional[int] = ...) -> None: ...

class CMsgGlobalMapStats(_message.Message):
    __slots__ = ("current", "window_start", "window_end")
    CURRENT_FIELD_NUMBER: _ClassVar[int]
    WINDOW_START_FIELD_NUMBER: _ClassVar[int]
    WINDOW_END_FIELD_NUMBER: _ClassVar[int]
    current: CMsgMapStatsSnapshot
    window_start: CMsgMapStatsSnapshot
    window_end: CMsgMapStatsSnapshot
    def __init__(self, current: _Optional[_Union[CMsgMapStatsSnapshot, _Mapping]] = ..., window_start: _Optional[_Union[CMsgMapStatsSnapshot, _Mapping]] = ..., window_end: _Optional[_Union[CMsgMapStatsSnapshot, _Mapping]] = ...) -> None: ...

class CMsgTrackedStat(_message.Message):
    __slots__ = ("tracked_stat_id", "tracked_stat_value")
    TRACKED_STAT_ID_FIELD_NUMBER: _ClassVar[int]
    TRACKED_STAT_VALUE_FIELD_NUMBER: _ClassVar[int]
    tracked_stat_id: int
    tracked_stat_value: int
    def __init__(self, tracked_stat_id: _Optional[int] = ..., tracked_stat_value: _Optional[int] = ...) -> None: ...

class CMsgDOTAClaimEventActionResponse(_message.Message):
    __slots__ = ("result", "reward_results", "action_id")
    class ResultCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        Success: _ClassVar[CMsgDOTAClaimEventActionResponse.ResultCode]
        InvalidEvent: _ClassVar[CMsgDOTAClaimEventActionResponse.ResultCode]
        EventNotActive: _ClassVar[CMsgDOTAClaimEventActionResponse.ResultCode]
        InvalidAction: _ClassVar[CMsgDOTAClaimEventActionResponse.ResultCode]
        ServerError: _ClassVar[CMsgDOTAClaimEventActionResponse.ResultCode]
        InsufficientPoints: _ClassVar[CMsgDOTAClaimEventActionResponse.ResultCode]
        InsufficentLevel: _ClassVar[CMsgDOTAClaimEventActionResponse.ResultCode]
        AlreadyClaimed: _ClassVar[CMsgDOTAClaimEventActionResponse.ResultCode]
        SDOLockFailure: _ClassVar[CMsgDOTAClaimEventActionResponse.ResultCode]
        SDOLoadFailure: _ClassVar[CMsgDOTAClaimEventActionResponse.ResultCode]
        EventNotOwned: _ClassVar[CMsgDOTAClaimEventActionResponse.ResultCode]
        Timeout: _ClassVar[CMsgDOTAClaimEventActionResponse.ResultCode]
        RequiresPlusSubscription: _ClassVar[CMsgDOTAClaimEventActionResponse.ResultCode]
        InvalidItem: _ClassVar[CMsgDOTAClaimEventActionResponse.ResultCode]
        AsyncRewards: _ClassVar[CMsgDOTAClaimEventActionResponse.ResultCode]
    Success: CMsgDOTAClaimEventActionResponse.ResultCode
    InvalidEvent: CMsgDOTAClaimEventActionResponse.ResultCode
    EventNotActive: CMsgDOTAClaimEventActionResponse.ResultCode
    InvalidAction: CMsgDOTAClaimEventActionResponse.ResultCode
    ServerError: CMsgDOTAClaimEventActionResponse.ResultCode
    InsufficientPoints: CMsgDOTAClaimEventActionResponse.ResultCode
    InsufficentLevel: CMsgDOTAClaimEventActionResponse.ResultCode
    AlreadyClaimed: CMsgDOTAClaimEventActionResponse.ResultCode
    SDOLockFailure: CMsgDOTAClaimEventActionResponse.ResultCode
    SDOLoadFailure: CMsgDOTAClaimEventActionResponse.ResultCode
    EventNotOwned: CMsgDOTAClaimEventActionResponse.ResultCode
    Timeout: CMsgDOTAClaimEventActionResponse.ResultCode
    RequiresPlusSubscription: CMsgDOTAClaimEventActionResponse.ResultCode
    InvalidItem: CMsgDOTAClaimEventActionResponse.ResultCode
    AsyncRewards: CMsgDOTAClaimEventActionResponse.ResultCode
    class MysteryItemRewardData(_message.Message):
        __slots__ = ("item_def", "item_category")
        ITEM_DEF_FIELD_NUMBER: _ClassVar[int]
        ITEM_CATEGORY_FIELD_NUMBER: _ClassVar[int]
        item_def: int
        item_category: int
        def __init__(self, item_def: _Optional[int] = ..., item_category: _Optional[int] = ...) -> None: ...
    class LootListRewardData(_message.Message):
        __slots__ = ("item_def",)
        ITEM_DEF_FIELD_NUMBER: _ClassVar[int]
        item_def: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, item_def: _Optional[_Iterable[int]] = ...) -> None: ...
    class ActionListRewardData(_message.Message):
        __slots__ = ("action_id", "result_reward_data")
        ACTION_ID_FIELD_NUMBER: _ClassVar[int]
        RESULT_REWARD_DATA_FIELD_NUMBER: _ClassVar[int]
        action_id: int
        result_reward_data: bytes
        def __init__(self, action_id: _Optional[int] = ..., result_reward_data: _Optional[bytes] = ...) -> None: ...
    class OverworldTokenRewardData(_message.Message):
        __slots__ = ("tokens",)
        class TokenQuantity(_message.Message):
            __slots__ = ("token_id", "token_count")
            TOKEN_ID_FIELD_NUMBER: _ClassVar[int]
            TOKEN_COUNT_FIELD_NUMBER: _ClassVar[int]
            token_id: int
            token_count: int
            def __init__(self, token_id: _Optional[int] = ..., token_count: _Optional[int] = ...) -> None: ...
        TOKENS_FIELD_NUMBER: _ClassVar[int]
        tokens: _containers.RepeatedCompositeFieldContainer[CMsgDOTAClaimEventActionResponse.OverworldTokenRewardData.TokenQuantity]
        def __init__(self, tokens: _Optional[_Iterable[_Union[CMsgDOTAClaimEventActionResponse.OverworldTokenRewardData.TokenQuantity, _Mapping]]] = ...) -> None: ...
    class MonsterHunterMaterialRewardData(_message.Message):
        __slots__ = ("materials",)
        class MaterialQuantity(_message.Message):
            __slots__ = ("material_id", "material_count")
            MATERIAL_ID_FIELD_NUMBER: _ClassVar[int]
            MATERIAL_COUNT_FIELD_NUMBER: _ClassVar[int]
            material_id: int
            material_count: int
            def __init__(self, material_id: _Optional[int] = ..., material_count: _Optional[int] = ...) -> None: ...
        MATERIALS_FIELD_NUMBER: _ClassVar[int]
        materials: _containers.RepeatedCompositeFieldContainer[CMsgDOTAClaimEventActionResponse.MonsterHunterMaterialRewardData.MaterialQuantity]
        def __init__(self, materials: _Optional[_Iterable[_Union[CMsgDOTAClaimEventActionResponse.MonsterHunterMaterialRewardData.MaterialQuantity, _Mapping]]] = ...) -> None: ...
    class GrantedRewardData(_message.Message):
        __slots__ = ("grant_index", "score_index", "reward_index", "reward_data", "action_id")
        GRANT_INDEX_FIELD_NUMBER: _ClassVar[int]
        SCORE_INDEX_FIELD_NUMBER: _ClassVar[int]
        REWARD_INDEX_FIELD_NUMBER: _ClassVar[int]
        REWARD_DATA_FIELD_NUMBER: _ClassVar[int]
        ACTION_ID_FIELD_NUMBER: _ClassVar[int]
        grant_index: int
        score_index: int
        reward_index: int
        reward_data: bytes
        action_id: int
        def __init__(self, grant_index: _Optional[int] = ..., score_index: _Optional[int] = ..., reward_index: _Optional[int] = ..., reward_data: _Optional[bytes] = ..., action_id: _Optional[int] = ...) -> None: ...
    RESULT_FIELD_NUMBER: _ClassVar[int]
    REWARD_RESULTS_FIELD_NUMBER: _ClassVar[int]
    ACTION_ID_FIELD_NUMBER: _ClassVar[int]
    result: CMsgDOTAClaimEventActionResponse.ResultCode
    reward_results: _containers.RepeatedCompositeFieldContainer[CMsgDOTAClaimEventActionResponse.GrantedRewardData]
    action_id: int
    def __init__(self, result: _Optional[_Union[CMsgDOTAClaimEventActionResponse.ResultCode, str]] = ..., reward_results: _Optional[_Iterable[_Union[CMsgDOTAClaimEventActionResponse.GrantedRewardData, _Mapping]]] = ..., action_id: _Optional[int] = ...) -> None: ...

class CMsgClientToGCDotaLabsFeedback(_message.Message):
    __slots__ = ("language", "feedback_item", "feedback")
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    FEEDBACK_ITEM_FIELD_NUMBER: _ClassVar[int]
    FEEDBACK_FIELD_NUMBER: _ClassVar[int]
    language: int
    feedback_item: int
    feedback: str
    def __init__(self, language: _Optional[int] = ..., feedback_item: _Optional[int] = ..., feedback: _Optional[str] = ...) -> None: ...

class CMsgClientToGCDotaLabsFeedbackResponse(_message.Message):
    __slots__ = ("response",)
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCDotaLabsFeedbackResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCDotaLabsFeedbackResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCDotaLabsFeedbackResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCDotaLabsFeedbackResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCDotaLabsFeedbackResponse.EResponse]
        k_eNotAllowed: _ClassVar[CMsgClientToGCDotaLabsFeedbackResponse.EResponse]
        k_eInvalidItem: _ClassVar[CMsgClientToGCDotaLabsFeedbackResponse.EResponse]
    k_eInternalError: CMsgClientToGCDotaLabsFeedbackResponse.EResponse
    k_eSuccess: CMsgClientToGCDotaLabsFeedbackResponse.EResponse
    k_eTooBusy: CMsgClientToGCDotaLabsFeedbackResponse.EResponse
    k_eDisabled: CMsgClientToGCDotaLabsFeedbackResponse.EResponse
    k_eTimeout: CMsgClientToGCDotaLabsFeedbackResponse.EResponse
    k_eNotAllowed: CMsgClientToGCDotaLabsFeedbackResponse.EResponse
    k_eInvalidItem: CMsgClientToGCDotaLabsFeedbackResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCDotaLabsFeedbackResponse.EResponse
    def __init__(self, response: _Optional[_Union[CMsgClientToGCDotaLabsFeedbackResponse.EResponse, str]] = ...) -> None: ...

class CDotaMsg_PredictionResult(_message.Message):
    __slots__ = ("account_id", "match_id", "correct", "predictions")
    class Prediction(_message.Message):
        __slots__ = ("item_def", "num_correct", "num_fails", "result", "granted_item_defs")
        class EResult(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            k_eResult_ItemGranted: _ClassVar[CDotaMsg_PredictionResult.Prediction.EResult]
            k_eResult_Destroyed: _ClassVar[CDotaMsg_PredictionResult.Prediction.EResult]
        k_eResult_ItemGranted: CDotaMsg_PredictionResult.Prediction.EResult
        k_eResult_Destroyed: CDotaMsg_PredictionResult.Prediction.EResult
        ITEM_DEF_FIELD_NUMBER: _ClassVar[int]
        NUM_CORRECT_FIELD_NUMBER: _ClassVar[int]
        NUM_FAILS_FIELD_NUMBER: _ClassVar[int]
        RESULT_FIELD_NUMBER: _ClassVar[int]
        GRANTED_ITEM_DEFS_FIELD_NUMBER: _ClassVar[int]
        item_def: int
        num_correct: int
        num_fails: int
        result: CDotaMsg_PredictionResult.Prediction.EResult
        granted_item_defs: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, item_def: _Optional[int] = ..., num_correct: _Optional[int] = ..., num_fails: _Optional[int] = ..., result: _Optional[_Union[CDotaMsg_PredictionResult.Prediction.EResult, str]] = ..., granted_item_defs: _Optional[_Iterable[int]] = ...) -> None: ...
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    CORRECT_FIELD_NUMBER: _ClassVar[int]
    PREDICTIONS_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    match_id: int
    correct: bool
    predictions: _containers.RepeatedCompositeFieldContainer[CDotaMsg_PredictionResult.Prediction]
    def __init__(self, account_id: _Optional[int] = ..., match_id: _Optional[int] = ..., correct: bool = ..., predictions: _Optional[_Iterable[_Union[CDotaMsg_PredictionResult.Prediction, _Mapping]]] = ...) -> None: ...

class CDotaMsgStructuredTooltipProperties(_message.Message):
    __slots__ = ("ability_name_loc_token", "ability_category", "ability_level", "current_mana_cost", "current_health_cost", "current_cooldown", "summary_description_loc_token", "summary_description_embed_values", "summary_description_surfaced_lines", "summary_description_embedded_sub_abilities", "summary_description_aghs_scepter", "summary_description_aghs_shard", "preview_video_url", "chunks")
    class EAbilityTooltipCategory(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        kPassive: _ClassVar[CDotaMsgStructuredTooltipProperties.EAbilityTooltipCategory]
        kAutocast: _ClassVar[CDotaMsgStructuredTooltipProperties.EAbilityTooltipCategory]
        kToggle: _ClassVar[CDotaMsgStructuredTooltipProperties.EAbilityTooltipCategory]
        kChanneled: _ClassVar[CDotaMsgStructuredTooltipProperties.EAbilityTooltipCategory]
    kPassive: CDotaMsgStructuredTooltipProperties.EAbilityTooltipCategory
    kAutocast: CDotaMsgStructuredTooltipProperties.EAbilityTooltipCategory
    kToggle: CDotaMsgStructuredTooltipProperties.EAbilityTooltipCategory
    kChanneled: CDotaMsgStructuredTooltipProperties.EAbilityTooltipCategory
    class EAttributeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        kUnknown: _ClassVar[CDotaMsgStructuredTooltipProperties.EAttributeType]
        kDuration: _ClassVar[CDotaMsgStructuredTooltipProperties.EAttributeType]
        kManaCost: _ClassVar[CDotaMsgStructuredTooltipProperties.EAttributeType]
        kHealthCost: _ClassVar[CDotaMsgStructuredTooltipProperties.EAttributeType]
        kCastRange: _ClassVar[CDotaMsgStructuredTooltipProperties.EAttributeType]
        kAreaOfEffectRadius: _ClassVar[CDotaMsgStructuredTooltipProperties.EAttributeType]
        kPhysicalDamage: _ClassVar[CDotaMsgStructuredTooltipProperties.EAttributeType]
        kMagicalDamage: _ClassVar[CDotaMsgStructuredTooltipProperties.EAttributeType]
        kPureDamage: _ClassVar[CDotaMsgStructuredTooltipProperties.EAttributeType]
        kCooldown: _ClassVar[CDotaMsgStructuredTooltipProperties.EAttributeType]
        kDebuffPercentage: _ClassVar[CDotaMsgStructuredTooltipProperties.EAttributeType]
        kDebuffValue: _ClassVar[CDotaMsgStructuredTooltipProperties.EAttributeType]
        kBuffPercentage: _ClassVar[CDotaMsgStructuredTooltipProperties.EAttributeType]
        kBuffValue: _ClassVar[CDotaMsgStructuredTooltipProperties.EAttributeType]
        kMagicalDamagePercentage: _ClassVar[CDotaMsgStructuredTooltipProperties.EAttributeType]
        kHealthPercentage: _ClassVar[CDotaMsgStructuredTooltipProperties.EAttributeType]
        kManaPercentage: _ClassVar[CDotaMsgStructuredTooltipProperties.EAttributeType]
        kNumCharges: _ClassVar[CDotaMsgStructuredTooltipProperties.EAttributeType]
        kDebuffDuration: _ClassVar[CDotaMsgStructuredTooltipProperties.EAttributeType]
        kBuffDuration: _ClassVar[CDotaMsgStructuredTooltipProperties.EAttributeType]
        kAbilityDefinedDamage: _ClassVar[CDotaMsgStructuredTooltipProperties.EAttributeType]
        kDispellability: _ClassVar[CDotaMsgStructuredTooltipProperties.EAttributeType]
        kSpellImmunityPiercing: _ClassVar[CDotaMsgStructuredTooltipProperties.EAttributeType]
    kUnknown: CDotaMsgStructuredTooltipProperties.EAttributeType
    kDuration: CDotaMsgStructuredTooltipProperties.EAttributeType
    kManaCost: CDotaMsgStructuredTooltipProperties.EAttributeType
    kHealthCost: CDotaMsgStructuredTooltipProperties.EAttributeType
    kCastRange: CDotaMsgStructuredTooltipProperties.EAttributeType
    kAreaOfEffectRadius: CDotaMsgStructuredTooltipProperties.EAttributeType
    kPhysicalDamage: CDotaMsgStructuredTooltipProperties.EAttributeType
    kMagicalDamage: CDotaMsgStructuredTooltipProperties.EAttributeType
    kPureDamage: CDotaMsgStructuredTooltipProperties.EAttributeType
    kCooldown: CDotaMsgStructuredTooltipProperties.EAttributeType
    kDebuffPercentage: CDotaMsgStructuredTooltipProperties.EAttributeType
    kDebuffValue: CDotaMsgStructuredTooltipProperties.EAttributeType
    kBuffPercentage: CDotaMsgStructuredTooltipProperties.EAttributeType
    kBuffValue: CDotaMsgStructuredTooltipProperties.EAttributeType
    kMagicalDamagePercentage: CDotaMsgStructuredTooltipProperties.EAttributeType
    kHealthPercentage: CDotaMsgStructuredTooltipProperties.EAttributeType
    kManaPercentage: CDotaMsgStructuredTooltipProperties.EAttributeType
    kNumCharges: CDotaMsgStructuredTooltipProperties.EAttributeType
    kDebuffDuration: CDotaMsgStructuredTooltipProperties.EAttributeType
    kBuffDuration: CDotaMsgStructuredTooltipProperties.EAttributeType
    kAbilityDefinedDamage: CDotaMsgStructuredTooltipProperties.EAttributeType
    kDispellability: CDotaMsgStructuredTooltipProperties.EAttributeType
    kSpellImmunityPiercing: CDotaMsgStructuredTooltipProperties.EAttributeType
    class AttributeValueValue(_message.Message):
        __slots__ = ("value", "is_active_value")
        VALUE_FIELD_NUMBER: _ClassVar[int]
        IS_ACTIVE_VALUE_FIELD_NUMBER: _ClassVar[int]
        value: float
        is_active_value: bool
        def __init__(self, value: _Optional[float] = ..., is_active_value: bool = ...) -> None: ...
    class AttributeValue_Single(_message.Message):
        __slots__ = ("single_value",)
        SINGLE_VALUE_FIELD_NUMBER: _ClassVar[int]
        single_value: CDotaMsgStructuredTooltipProperties.AttributeValueValue
        def __init__(self, single_value: _Optional[_Union[CDotaMsgStructuredTooltipProperties.AttributeValueValue, _Mapping]] = ...) -> None: ...
    class AttributeValue_Variable(_message.Message):
        __slots__ = ("values",)
        VALUES_FIELD_NUMBER: _ClassVar[int]
        values: _containers.RepeatedCompositeFieldContainer[CDotaMsgStructuredTooltipProperties.AttributeValueValue]
        def __init__(self, values: _Optional[_Iterable[_Union[CDotaMsgStructuredTooltipProperties.AttributeValueValue, _Mapping]]] = ...) -> None: ...
    class AttributeValue_Delta(_message.Message):
        __slots__ = ("prev", "next")
        PREV_FIELD_NUMBER: _ClassVar[int]
        NEXT_FIELD_NUMBER: _ClassVar[int]
        prev: CDotaMsgStructuredTooltipProperties.AttributeValueValue
        next: CDotaMsgStructuredTooltipProperties.AttributeValueValue
        def __init__(self, prev: _Optional[_Union[CDotaMsgStructuredTooltipProperties.AttributeValueValue, _Mapping]] = ..., next: _Optional[_Union[CDotaMsgStructuredTooltipProperties.AttributeValueValue, _Mapping]] = ...) -> None: ...
    class AttributeValue(_message.Message):
        __slots__ = ("single", "variable", "delta")
        SINGLE_FIELD_NUMBER: _ClassVar[int]
        VARIABLE_FIELD_NUMBER: _ClassVar[int]
        DELTA_FIELD_NUMBER: _ClassVar[int]
        single: CDotaMsgStructuredTooltipProperties.AttributeValue_Single
        variable: CDotaMsgStructuredTooltipProperties.AttributeValue_Variable
        delta: CDotaMsgStructuredTooltipProperties.AttributeValue_Delta
        def __init__(self, single: _Optional[_Union[CDotaMsgStructuredTooltipProperties.AttributeValue_Single, _Mapping]] = ..., variable: _Optional[_Union[CDotaMsgStructuredTooltipProperties.AttributeValue_Variable, _Mapping]] = ..., delta: _Optional[_Union[CDotaMsgStructuredTooltipProperties.AttributeValue_Delta, _Mapping]] = ...) -> None: ...
    class Attribute(_message.Message):
        __slots__ = ("internal_name", "localized_name_text", "type", "value")
        INTERNAL_NAME_FIELD_NUMBER: _ClassVar[int]
        LOCALIZED_NAME_TEXT_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        internal_name: str
        localized_name_text: str
        type: CDotaMsgStructuredTooltipProperties.EAttributeType
        value: CDotaMsgStructuredTooltipProperties.AttributeValue
        def __init__(self, internal_name: _Optional[str] = ..., localized_name_text: _Optional[str] = ..., type: _Optional[_Union[CDotaMsgStructuredTooltipProperties.EAttributeType, str]] = ..., value: _Optional[_Union[CDotaMsgStructuredTooltipProperties.AttributeValue, _Mapping]] = ...) -> None: ...
    class AttributeGroupDesc_Basic(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class AttributeGroupDesc_Specific(_message.Message):
        __slots__ = ("title_loc_token", "desc_loc_token")
        TITLE_LOC_TOKEN_FIELD_NUMBER: _ClassVar[int]
        DESC_LOC_TOKEN_FIELD_NUMBER: _ClassVar[int]
        title_loc_token: str
        desc_loc_token: str
        def __init__(self, title_loc_token: _Optional[str] = ..., desc_loc_token: _Optional[str] = ...) -> None: ...
    class AttributeGroupDescription(_message.Message):
        __slots__ = ("basic", "characteristics", "specific")
        BASIC_FIELD_NUMBER: _ClassVar[int]
        CHARACTERISTICS_FIELD_NUMBER: _ClassVar[int]
        SPECIFIC_FIELD_NUMBER: _ClassVar[int]
        basic: CDotaMsgStructuredTooltipProperties.AttributeGroupDesc_Basic
        characteristics: CDotaMsgStructuredTooltipProperties.AttributeGroupDesc_Basic
        specific: CDotaMsgStructuredTooltipProperties.AttributeGroupDesc_Specific
        def __init__(self, basic: _Optional[_Union[CDotaMsgStructuredTooltipProperties.AttributeGroupDesc_Basic, _Mapping]] = ..., characteristics: _Optional[_Union[CDotaMsgStructuredTooltipProperties.AttributeGroupDesc_Basic, _Mapping]] = ..., specific: _Optional[_Union[CDotaMsgStructuredTooltipProperties.AttributeGroupDesc_Specific, _Mapping]] = ...) -> None: ...
    class AttributeGroup(_message.Message):
        __slots__ = ("desc", "attributes")
        DESC_FIELD_NUMBER: _ClassVar[int]
        ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
        desc: CDotaMsgStructuredTooltipProperties.AttributeGroupDescription
        attributes: _containers.RepeatedCompositeFieldContainer[CDotaMsgStructuredTooltipProperties.Attribute]
        def __init__(self, desc: _Optional[_Union[CDotaMsgStructuredTooltipProperties.AttributeGroupDescription, _Mapping]] = ..., attributes: _Optional[_Iterable[_Union[CDotaMsgStructuredTooltipProperties.Attribute, _Mapping]]] = ...) -> None: ...
    class ContentChunk_AttributeGroup(_message.Message):
        __slots__ = ("groups",)
        GROUPS_FIELD_NUMBER: _ClassVar[int]
        groups: _containers.RepeatedCompositeFieldContainer[CDotaMsgStructuredTooltipProperties.AttributeGroup]
        def __init__(self, groups: _Optional[_Iterable[_Union[CDotaMsgStructuredTooltipProperties.AttributeGroup, _Mapping]]] = ...) -> None: ...
    class TooltipContentChunk(_message.Message):
        __slots__ = ("attribute_group",)
        ATTRIBUTE_GROUP_FIELD_NUMBER: _ClassVar[int]
        attribute_group: CDotaMsgStructuredTooltipProperties.ContentChunk_AttributeGroup
        def __init__(self, attribute_group: _Optional[_Union[CDotaMsgStructuredTooltipProperties.ContentChunk_AttributeGroup, _Mapping]] = ...) -> None: ...
    class SummaryDescriptionEmbeddedSubAbility(_message.Message):
        __slots__ = ("ability_name_loc_token", "ability_desc_loc_token", "ability_icon_url")
        ABILITY_NAME_LOC_TOKEN_FIELD_NUMBER: _ClassVar[int]
        ABILITY_DESC_LOC_TOKEN_FIELD_NUMBER: _ClassVar[int]
        ABILITY_ICON_URL_FIELD_NUMBER: _ClassVar[int]
        ability_name_loc_token: str
        ability_desc_loc_token: str
        ability_icon_url: str
        def __init__(self, ability_name_loc_token: _Optional[str] = ..., ability_desc_loc_token: _Optional[str] = ..., ability_icon_url: _Optional[str] = ...) -> None: ...
    ABILITY_NAME_LOC_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ABILITY_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    ABILITY_LEVEL_FIELD_NUMBER: _ClassVar[int]
    CURRENT_MANA_COST_FIELD_NUMBER: _ClassVar[int]
    CURRENT_HEALTH_COST_FIELD_NUMBER: _ClassVar[int]
    CURRENT_COOLDOWN_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_DESCRIPTION_LOC_TOKEN_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_DESCRIPTION_EMBED_VALUES_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_DESCRIPTION_SURFACED_LINES_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_DESCRIPTION_EMBEDDED_SUB_ABILITIES_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_DESCRIPTION_AGHS_SCEPTER_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_DESCRIPTION_AGHS_SHARD_FIELD_NUMBER: _ClassVar[int]
    PREVIEW_VIDEO_URL_FIELD_NUMBER: _ClassVar[int]
    CHUNKS_FIELD_NUMBER: _ClassVar[int]
    ability_name_loc_token: str
    ability_category: CDotaMsgStructuredTooltipProperties.EAbilityTooltipCategory
    ability_level: int
    current_mana_cost: int
    current_health_cost: int
    current_cooldown: float
    summary_description_loc_token: str
    summary_description_embed_values: _containers.RepeatedCompositeFieldContainer[CDotaMsgStructuredTooltipProperties.Attribute]
    summary_description_surfaced_lines: _containers.RepeatedScalarFieldContainer[str]
    summary_description_embedded_sub_abilities: _containers.RepeatedCompositeFieldContainer[CDotaMsgStructuredTooltipProperties.SummaryDescriptionEmbeddedSubAbility]
    summary_description_aghs_scepter: str
    summary_description_aghs_shard: str
    preview_video_url: str
    chunks: _containers.RepeatedCompositeFieldContainer[CDotaMsgStructuredTooltipProperties.TooltipContentChunk]
    def __init__(self, ability_name_loc_token: _Optional[str] = ..., ability_category: _Optional[_Union[CDotaMsgStructuredTooltipProperties.EAbilityTooltipCategory, str]] = ..., ability_level: _Optional[int] = ..., current_mana_cost: _Optional[int] = ..., current_health_cost: _Optional[int] = ..., current_cooldown: _Optional[float] = ..., summary_description_loc_token: _Optional[str] = ..., summary_description_embed_values: _Optional[_Iterable[_Union[CDotaMsgStructuredTooltipProperties.Attribute, _Mapping]]] = ..., summary_description_surfaced_lines: _Optional[_Iterable[str]] = ..., summary_description_embedded_sub_abilities: _Optional[_Iterable[_Union[CDotaMsgStructuredTooltipProperties.SummaryDescriptionEmbeddedSubAbility, _Mapping]]] = ..., summary_description_aghs_scepter: _Optional[str] = ..., summary_description_aghs_shard: _Optional[str] = ..., preview_video_url: _Optional[str] = ..., chunks: _Optional[_Iterable[_Union[CDotaMsgStructuredTooltipProperties.TooltipContentChunk, _Mapping]]] = ...) -> None: ...
