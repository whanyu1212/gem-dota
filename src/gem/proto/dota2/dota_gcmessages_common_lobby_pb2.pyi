import steammessages_pb2 as _steammessages_pb2
import dota_shared_enums_pb2 as _dota_shared_enums_pb2
import gcsdk_gcmessages_pb2 as _gcsdk_gcmessages_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ELobbyMemberCoachRequestState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eLobbyMemberCoachRequestState_None: _ClassVar[ELobbyMemberCoachRequestState]
    k_eLobbyMemberCoachRequestState_Accepted: _ClassVar[ELobbyMemberCoachRequestState]
    k_eLobbyMemberCoachRequestState_Rejected: _ClassVar[ELobbyMemberCoachRequestState]

class LobbyDotaTVDelay(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LobbyDotaTV_10: _ClassVar[LobbyDotaTVDelay]
    LobbyDotaTV_120: _ClassVar[LobbyDotaTVDelay]
    LobbyDotaTV_300: _ClassVar[LobbyDotaTVDelay]
    LobbyDotaTV_900: _ClassVar[LobbyDotaTVDelay]

class LobbyDotaPauseSetting(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LobbyDotaPauseSetting_Unlimited: _ClassVar[LobbyDotaPauseSetting]
    LobbyDotaPauseSetting_Limited: _ClassVar[LobbyDotaPauseSetting]
    LobbyDotaPauseSetting_Disabled: _ClassVar[LobbyDotaPauseSetting]
k_eLobbyMemberCoachRequestState_None: ELobbyMemberCoachRequestState
k_eLobbyMemberCoachRequestState_Accepted: ELobbyMemberCoachRequestState
k_eLobbyMemberCoachRequestState_Rejected: ELobbyMemberCoachRequestState
LobbyDotaTV_10: LobbyDotaTVDelay
LobbyDotaTV_120: LobbyDotaTVDelay
LobbyDotaTV_300: LobbyDotaTVDelay
LobbyDotaTV_900: LobbyDotaTVDelay
LobbyDotaPauseSetting_Unlimited: LobbyDotaPauseSetting
LobbyDotaPauseSetting_Limited: LobbyDotaPauseSetting
LobbyDotaPauseSetting_Disabled: LobbyDotaPauseSetting

class CMsgLobbyCoachFriendRequest(_message.Message):
    __slots__ = ("coach_account_id", "player_account_id", "request_state")
    COACH_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    PLAYER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_STATE_FIELD_NUMBER: _ClassVar[int]
    coach_account_id: int
    player_account_id: int
    request_state: ELobbyMemberCoachRequestState
    def __init__(self, coach_account_id: _Optional[int] = ..., player_account_id: _Optional[int] = ..., request_state: _Optional[_Union[ELobbyMemberCoachRequestState, str]] = ...) -> None: ...

class CMsgLobbyPlayerPlusSubscriptionData(_message.Message):
    __slots__ = ("hero_badges",)
    class HeroBadge(_message.Message):
        __slots__ = ("hero_id", "hero_badge_xp")
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        HERO_BADGE_XP_FIELD_NUMBER: _ClassVar[int]
        hero_id: int
        hero_badge_xp: int
        def __init__(self, hero_id: _Optional[int] = ..., hero_badge_xp: _Optional[int] = ...) -> None: ...
    HERO_BADGES_FIELD_NUMBER: _ClassVar[int]
    hero_badges: _containers.RepeatedCompositeFieldContainer[CMsgLobbyPlayerPlusSubscriptionData.HeroBadge]
    def __init__(self, hero_badges: _Optional[_Iterable[_Union[CMsgLobbyPlayerPlusSubscriptionData.HeroBadge, _Mapping]]] = ...) -> None: ...

class CMsgEventActionData(_message.Message):
    __slots__ = ("action_id", "action_score")
    ACTION_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_SCORE_FIELD_NUMBER: _ClassVar[int]
    action_id: int
    action_score: int
    def __init__(self, action_id: _Optional[int] = ..., action_score: _Optional[int] = ...) -> None: ...

class CMsgPeriodicResourceData(_message.Message):
    __slots__ = ("periodic_resource_id", "remaining", "max")
    PERIODIC_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    REMAINING_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    periodic_resource_id: int
    remaining: int
    max: int
    def __init__(self, periodic_resource_id: _Optional[int] = ..., remaining: _Optional[int] = ..., max: _Optional[int] = ...) -> None: ...

class CMsgLobbyEventPoints(_message.Message):
    __slots__ = ("event_id", "account_points")
    class AccountPoints(_message.Message):
        __slots__ = ("account_id", "normal_points", "premium_points", "owned", "event_level", "active_effects_mask", "wager_streak", "event_game_custom_actions", "tip_amount_index", "active_event_season_id", "teleport_fx_level", "networked_event_actions", "periodic_resources", "extra_event_messages")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        NORMAL_POINTS_FIELD_NUMBER: _ClassVar[int]
        PREMIUM_POINTS_FIELD_NUMBER: _ClassVar[int]
        OWNED_FIELD_NUMBER: _ClassVar[int]
        EVENT_LEVEL_FIELD_NUMBER: _ClassVar[int]
        ACTIVE_EFFECTS_MASK_FIELD_NUMBER: _ClassVar[int]
        WAGER_STREAK_FIELD_NUMBER: _ClassVar[int]
        EVENT_GAME_CUSTOM_ACTIONS_FIELD_NUMBER: _ClassVar[int]
        TIP_AMOUNT_INDEX_FIELD_NUMBER: _ClassVar[int]
        ACTIVE_EVENT_SEASON_ID_FIELD_NUMBER: _ClassVar[int]
        TELEPORT_FX_LEVEL_FIELD_NUMBER: _ClassVar[int]
        NETWORKED_EVENT_ACTIONS_FIELD_NUMBER: _ClassVar[int]
        PERIODIC_RESOURCES_FIELD_NUMBER: _ClassVar[int]
        EXTRA_EVENT_MESSAGES_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        normal_points: int
        premium_points: int
        owned: bool
        event_level: int
        active_effects_mask: int
        wager_streak: int
        event_game_custom_actions: _containers.RepeatedCompositeFieldContainer[CMsgEventActionData]
        tip_amount_index: int
        active_event_season_id: int
        teleport_fx_level: int
        networked_event_actions: _containers.RepeatedCompositeFieldContainer[CMsgEventActionData]
        periodic_resources: _containers.RepeatedCompositeFieldContainer[CMsgPeriodicResourceData]
        extra_event_messages: _containers.RepeatedCompositeFieldContainer[_gcsdk_gcmessages_pb2.CExtraMsgBlock]
        def __init__(self, account_id: _Optional[int] = ..., normal_points: _Optional[int] = ..., premium_points: _Optional[int] = ..., owned: bool = ..., event_level: _Optional[int] = ..., active_effects_mask: _Optional[int] = ..., wager_streak: _Optional[int] = ..., event_game_custom_actions: _Optional[_Iterable[_Union[CMsgEventActionData, _Mapping]]] = ..., tip_amount_index: _Optional[int] = ..., active_event_season_id: _Optional[int] = ..., teleport_fx_level: _Optional[int] = ..., networked_event_actions: _Optional[_Iterable[_Union[CMsgEventActionData, _Mapping]]] = ..., periodic_resources: _Optional[_Iterable[_Union[CMsgPeriodicResourceData, _Mapping]]] = ..., extra_event_messages: _Optional[_Iterable[_Union[_gcsdk_gcmessages_pb2.CExtraMsgBlock, _Mapping]]] = ...) -> None: ...
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_POINTS_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    account_points: _containers.RepeatedCompositeFieldContainer[CMsgLobbyEventPoints.AccountPoints]
    def __init__(self, event_id: _Optional[int] = ..., account_points: _Optional[_Iterable[_Union[CMsgLobbyEventPoints.AccountPoints, _Mapping]]] = ...) -> None: ...

class CMsgLobbyEventGameData(_message.Message):
    __slots__ = ("game_seed", "event_window_start_time")
    GAME_SEED_FIELD_NUMBER: _ClassVar[int]
    EVENT_WINDOW_START_TIME_FIELD_NUMBER: _ClassVar[int]
    game_seed: int
    event_window_start_time: int
    def __init__(self, game_seed: _Optional[int] = ..., event_window_start_time: _Optional[int] = ...) -> None: ...

class CSODOTALobbyInvite(_message.Message):
    __slots__ = ("group_id", "sender_id", "sender_name", "members", "custom_game_id", "invite_gid", "custom_game_crc", "custom_game_timestamp")
    class LobbyMember(_message.Message):
        __slots__ = ("name", "steam_id")
        NAME_FIELD_NUMBER: _ClassVar[int]
        STEAM_ID_FIELD_NUMBER: _ClassVar[int]
        name: str
        steam_id: int
        def __init__(self, name: _Optional[str] = ..., steam_id: _Optional[int] = ...) -> None: ...
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    SENDER_ID_FIELD_NUMBER: _ClassVar[int]
    SENDER_NAME_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_ID_FIELD_NUMBER: _ClassVar[int]
    INVITE_GID_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_CRC_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    group_id: int
    sender_id: int
    sender_name: str
    members: _containers.RepeatedCompositeFieldContainer[CSODOTALobbyInvite.LobbyMember]
    custom_game_id: int
    invite_gid: int
    custom_game_crc: int
    custom_game_timestamp: int
    def __init__(self, group_id: _Optional[int] = ..., sender_id: _Optional[int] = ..., sender_name: _Optional[str] = ..., members: _Optional[_Iterable[_Union[CSODOTALobbyInvite.LobbyMember, _Mapping]]] = ..., custom_game_id: _Optional[int] = ..., invite_gid: _Optional[int] = ..., custom_game_crc: _Optional[int] = ..., custom_game_timestamp: _Optional[int] = ...) -> None: ...

class CSODOTALobbyMember(_message.Message):
    __slots__ = ("id", "hero_id", "team", "slot", "leaver_status", "leaver_actions", "coach_team", "custom_game_product_ids", "live_spectator_team", "pending_awards", "pending_awards_on_victory", "reports_available", "live_spectator_account_id", "comms_reports_available")
    ID_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_FIELD_NUMBER: _ClassVar[int]
    SLOT_FIELD_NUMBER: _ClassVar[int]
    LEAVER_STATUS_FIELD_NUMBER: _ClassVar[int]
    LEAVER_ACTIONS_FIELD_NUMBER: _ClassVar[int]
    COACH_TEAM_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_PRODUCT_IDS_FIELD_NUMBER: _ClassVar[int]
    LIVE_SPECTATOR_TEAM_FIELD_NUMBER: _ClassVar[int]
    PENDING_AWARDS_FIELD_NUMBER: _ClassVar[int]
    PENDING_AWARDS_ON_VICTORY_FIELD_NUMBER: _ClassVar[int]
    REPORTS_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    LIVE_SPECTATOR_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    COMMS_REPORTS_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    id: int
    hero_id: int
    team: _dota_shared_enums_pb2.DOTA_GC_TEAM
    slot: int
    leaver_status: _dota_shared_enums_pb2.DOTALeaverStatus_t
    leaver_actions: int
    coach_team: _dota_shared_enums_pb2.DOTA_GC_TEAM
    custom_game_product_ids: _containers.RepeatedScalarFieldContainer[int]
    live_spectator_team: _dota_shared_enums_pb2.DOTA_GC_TEAM
    pending_awards: _containers.RepeatedCompositeFieldContainer[_dota_shared_enums_pb2.CMsgPendingEventAward]
    pending_awards_on_victory: _containers.RepeatedCompositeFieldContainer[_dota_shared_enums_pb2.CMsgPendingEventAward]
    reports_available: int
    live_spectator_account_id: int
    comms_reports_available: int
    def __init__(self, id: _Optional[int] = ..., hero_id: _Optional[int] = ..., team: _Optional[_Union[_dota_shared_enums_pb2.DOTA_GC_TEAM, str]] = ..., slot: _Optional[int] = ..., leaver_status: _Optional[_Union[_dota_shared_enums_pb2.DOTALeaverStatus_t, str]] = ..., leaver_actions: _Optional[int] = ..., coach_team: _Optional[_Union[_dota_shared_enums_pb2.DOTA_GC_TEAM, str]] = ..., custom_game_product_ids: _Optional[_Iterable[int]] = ..., live_spectator_team: _Optional[_Union[_dota_shared_enums_pb2.DOTA_GC_TEAM, str]] = ..., pending_awards: _Optional[_Iterable[_Union[_dota_shared_enums_pb2.CMsgPendingEventAward, _Mapping]]] = ..., pending_awards_on_victory: _Optional[_Iterable[_Union[_dota_shared_enums_pb2.CMsgPendingEventAward, _Mapping]]] = ..., reports_available: _Optional[int] = ..., live_spectator_account_id: _Optional[int] = ..., comms_reports_available: _Optional[int] = ...) -> None: ...

class CSODOTAServerLobbyMember(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CSODOTAStaticLobbyMember(_message.Message):
    __slots__ = ("name", "party_id", "channel", "cameraman")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PARTY_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    CAMERAMAN_FIELD_NUMBER: _ClassVar[int]
    name: str
    party_id: int
    channel: int
    cameraman: bool
    def __init__(self, name: _Optional[str] = ..., party_id: _Optional[int] = ..., channel: _Optional[int] = ..., cameraman: bool = ...) -> None: ...

class CSODOTAServerStaticLobbyMember(_message.Message):
    __slots__ = ("steam_id", "rank_tier", "leaderboard_rank", "lane_selection_flags", "rank_mmr_boost_type", "coach_rating", "coached_account_ids", "was_mvp_last_game", "can_earn_rewards", "is_plus_subscriber", "favorite_team_packed", "is_steam_china", "title", "guild_id", "disabled_random_hero_bits", "disabled_hero_id", "enabled_hero_id", "banned_hero_ids")
    STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    RANK_TIER_FIELD_NUMBER: _ClassVar[int]
    LEADERBOARD_RANK_FIELD_NUMBER: _ClassVar[int]
    LANE_SELECTION_FLAGS_FIELD_NUMBER: _ClassVar[int]
    RANK_MMR_BOOST_TYPE_FIELD_NUMBER: _ClassVar[int]
    COACH_RATING_FIELD_NUMBER: _ClassVar[int]
    COACHED_ACCOUNT_IDS_FIELD_NUMBER: _ClassVar[int]
    WAS_MVP_LAST_GAME_FIELD_NUMBER: _ClassVar[int]
    CAN_EARN_REWARDS_FIELD_NUMBER: _ClassVar[int]
    IS_PLUS_SUBSCRIBER_FIELD_NUMBER: _ClassVar[int]
    FAVORITE_TEAM_PACKED_FIELD_NUMBER: _ClassVar[int]
    IS_STEAM_CHINA_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    DISABLED_RANDOM_HERO_BITS_FIELD_NUMBER: _ClassVar[int]
    DISABLED_HERO_ID_FIELD_NUMBER: _ClassVar[int]
    ENABLED_HERO_ID_FIELD_NUMBER: _ClassVar[int]
    BANNED_HERO_IDS_FIELD_NUMBER: _ClassVar[int]
    steam_id: int
    rank_tier: int
    leaderboard_rank: int
    lane_selection_flags: int
    rank_mmr_boost_type: _dota_shared_enums_pb2.EDOTAMMRBoostType
    coach_rating: int
    coached_account_ids: _containers.RepeatedScalarFieldContainer[int]
    was_mvp_last_game: bool
    can_earn_rewards: bool
    is_plus_subscriber: bool
    favorite_team_packed: int
    is_steam_china: bool
    title: int
    guild_id: int
    disabled_random_hero_bits: _containers.RepeatedScalarFieldContainer[int]
    disabled_hero_id: _containers.RepeatedScalarFieldContainer[int]
    enabled_hero_id: _containers.RepeatedScalarFieldContainer[int]
    banned_hero_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, steam_id: _Optional[int] = ..., rank_tier: _Optional[int] = ..., leaderboard_rank: _Optional[int] = ..., lane_selection_flags: _Optional[int] = ..., rank_mmr_boost_type: _Optional[_Union[_dota_shared_enums_pb2.EDOTAMMRBoostType, str]] = ..., coach_rating: _Optional[int] = ..., coached_account_ids: _Optional[_Iterable[int]] = ..., was_mvp_last_game: bool = ..., can_earn_rewards: bool = ..., is_plus_subscriber: bool = ..., favorite_team_packed: _Optional[int] = ..., is_steam_china: bool = ..., title: _Optional[int] = ..., guild_id: _Optional[int] = ..., disabled_random_hero_bits: _Optional[_Iterable[int]] = ..., disabled_hero_id: _Optional[_Iterable[int]] = ..., enabled_hero_id: _Optional[_Iterable[int]] = ..., banned_hero_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class CLobbyTeamDetails(_message.Message):
    __slots__ = ("team_name", "team_tag", "team_id", "team_logo", "team_base_logo", "team_banner_logo", "team_complete", "rank", "rank_change", "is_home_team", "is_challenge_match", "challenge_match_token_account", "team_logo_url", "team_abbreviation")
    TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
    TEAM_TAG_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_LOGO_FIELD_NUMBER: _ClassVar[int]
    TEAM_BASE_LOGO_FIELD_NUMBER: _ClassVar[int]
    TEAM_BANNER_LOGO_FIELD_NUMBER: _ClassVar[int]
    TEAM_COMPLETE_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    RANK_CHANGE_FIELD_NUMBER: _ClassVar[int]
    IS_HOME_TEAM_FIELD_NUMBER: _ClassVar[int]
    IS_CHALLENGE_MATCH_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_MATCH_TOKEN_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    TEAM_LOGO_URL_FIELD_NUMBER: _ClassVar[int]
    TEAM_ABBREVIATION_FIELD_NUMBER: _ClassVar[int]
    team_name: str
    team_tag: str
    team_id: int
    team_logo: int
    team_base_logo: int
    team_banner_logo: int
    team_complete: bool
    rank: int
    rank_change: int
    is_home_team: bool
    is_challenge_match: bool
    challenge_match_token_account: int
    team_logo_url: str
    team_abbreviation: str
    def __init__(self, team_name: _Optional[str] = ..., team_tag: _Optional[str] = ..., team_id: _Optional[int] = ..., team_logo: _Optional[int] = ..., team_base_logo: _Optional[int] = ..., team_banner_logo: _Optional[int] = ..., team_complete: bool = ..., rank: _Optional[int] = ..., rank_change: _Optional[int] = ..., is_home_team: bool = ..., is_challenge_match: bool = ..., challenge_match_token_account: _Optional[int] = ..., team_logo_url: _Optional[str] = ..., team_abbreviation: _Optional[str] = ...) -> None: ...

class CLobbyGuildDetails(_message.Message):
    __slots__ = ("guild_id", "guild_primary_color", "guild_secondary_color", "guild_pattern", "guild_logo", "guild_points", "guild_event", "guild_flags", "team_for_guild", "guild_tag", "guild_weekly_percentile")
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    GUILD_PRIMARY_COLOR_FIELD_NUMBER: _ClassVar[int]
    GUILD_SECONDARY_COLOR_FIELD_NUMBER: _ClassVar[int]
    GUILD_PATTERN_FIELD_NUMBER: _ClassVar[int]
    GUILD_LOGO_FIELD_NUMBER: _ClassVar[int]
    GUILD_POINTS_FIELD_NUMBER: _ClassVar[int]
    GUILD_EVENT_FIELD_NUMBER: _ClassVar[int]
    GUILD_FLAGS_FIELD_NUMBER: _ClassVar[int]
    TEAM_FOR_GUILD_FIELD_NUMBER: _ClassVar[int]
    GUILD_TAG_FIELD_NUMBER: _ClassVar[int]
    GUILD_WEEKLY_PERCENTILE_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    guild_primary_color: int
    guild_secondary_color: int
    guild_pattern: int
    guild_logo: int
    guild_points: int
    guild_event: int
    guild_flags: int
    team_for_guild: _dota_shared_enums_pb2.DOTA_GC_TEAM
    guild_tag: str
    guild_weekly_percentile: int
    def __init__(self, guild_id: _Optional[int] = ..., guild_primary_color: _Optional[int] = ..., guild_secondary_color: _Optional[int] = ..., guild_pattern: _Optional[int] = ..., guild_logo: _Optional[int] = ..., guild_points: _Optional[int] = ..., guild_event: _Optional[int] = ..., guild_flags: _Optional[int] = ..., team_for_guild: _Optional[_Union[_dota_shared_enums_pb2.DOTA_GC_TEAM, str]] = ..., guild_tag: _Optional[str] = ..., guild_weekly_percentile: _Optional[int] = ...) -> None: ...

class CLobbyTimedRewardDetails(_message.Message):
    __slots__ = ("item_def_index", "is_supply_crate", "is_timed_drop", "account_id", "origin")
    ITEM_DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
    IS_SUPPLY_CRATE_FIELD_NUMBER: _ClassVar[int]
    IS_TIMED_DROP_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    item_def_index: int
    is_supply_crate: bool
    is_timed_drop: bool
    account_id: int
    origin: int
    def __init__(self, item_def_index: _Optional[int] = ..., is_supply_crate: bool = ..., is_timed_drop: bool = ..., account_id: _Optional[int] = ..., origin: _Optional[int] = ...) -> None: ...

class CLobbyBroadcastChannelInfo(_message.Message):
    __slots__ = ("channel_id", "country_code", "description", "language_code")
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_CODE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_CODE_FIELD_NUMBER: _ClassVar[int]
    channel_id: int
    country_code: str
    description: str
    language_code: str
    def __init__(self, channel_id: _Optional[int] = ..., country_code: _Optional[str] = ..., description: _Optional[str] = ..., language_code: _Optional[str] = ...) -> None: ...

class CLobbyGuildChallenge(_message.Message):
    __slots__ = ("guild_id", "event_id", "challenge_instance_id", "challenge_parameter", "challenge_timestamp", "challenge_period_serial", "challenge_progress_at_start", "eligible_account_ids")
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_PARAMETER_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_PERIOD_SERIAL_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_PROGRESS_AT_START_FIELD_NUMBER: _ClassVar[int]
    ELIGIBLE_ACCOUNT_IDS_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    event_id: _dota_shared_enums_pb2.EEvent
    challenge_instance_id: int
    challenge_parameter: int
    challenge_timestamp: int
    challenge_period_serial: int
    challenge_progress_at_start: int
    eligible_account_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, guild_id: _Optional[int] = ..., event_id: _Optional[_Union[_dota_shared_enums_pb2.EEvent, str]] = ..., challenge_instance_id: _Optional[int] = ..., challenge_parameter: _Optional[int] = ..., challenge_timestamp: _Optional[int] = ..., challenge_period_serial: _Optional[int] = ..., challenge_progress_at_start: _Optional[int] = ..., eligible_account_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class CDOTALobbyMatchQualityData(_message.Message):
    __slots__ = ("overall_quality", "team_balance", "match_skill_range", "match_behavior")
    OVERALL_QUALITY_FIELD_NUMBER: _ClassVar[int]
    TEAM_BALANCE_FIELD_NUMBER: _ClassVar[int]
    MATCH_SKILL_RANGE_FIELD_NUMBER: _ClassVar[int]
    MATCH_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    overall_quality: int
    team_balance: int
    match_skill_range: int
    match_behavior: int
    def __init__(self, overall_quality: _Optional[int] = ..., team_balance: _Optional[int] = ..., match_skill_range: _Optional[int] = ..., match_behavior: _Optional[int] = ...) -> None: ...

class CSODOTALobby(_message.Message):
    __slots__ = ("lobby_id", "all_members", "member_indices", "left_member_indices", "free_member_indices", "leader_id", "server_id", "game_mode", "pending_invites", "state", "connect", "lobby_type", "allow_cheats", "fill_with_bots", "game_name", "team_details", "tournament_id", "tournament_game_id", "server_region", "game_state", "num_spectators", "matchgroup", "cm_pick", "match_id", "allow_spectating", "bot_difficulty_radiant", "pass_key", "leagueid", "penalty_level_radiant", "penalty_level_dire", "series_type", "radiant_series_wins", "dire_series_wins", "allchat", "dota_tv_delay", "custom_game_mode", "custom_map_name", "custom_difficulty", "lan", "broadcast_channel_info", "first_leaver_accountid", "series_id", "low_priority", "extra_messages", "first_blood_happened", "match_outcome", "mass_disconnect", "custom_game_id", "custom_min_players", "custom_max_players", "visibility", "custom_game_crc", "custom_game_auto_created_lobby", "custom_game_timestamp", "previous_series_matches", "previous_match_override", "game_start_time", "pause_setting", "weekend_tourney_division_id", "weekend_tourney_skill_level", "weekend_tourney_bracket_round", "bot_difficulty_dire", "bot_radiant", "bot_dire", "event_progression_enabled", "selection_priority_rules", "series_previous_selection_priority_team_id", "series_current_selection_priority_team_id", "series_current_priority_team_choice", "series_current_non_priority_team_choice", "series_current_selection_priority_used_coin_toss", "current_primary_event", "current_primary_event_for_display", "emergency_disabled_hero_ids", "custom_game_private_key", "custom_game_penalties", "lan_host_ping_location", "league_node_id", "match_duration", "league_phase", "experimental_gameplay_enabled", "guild_challenges", "guild_details", "requested_hero_ids", "coach_friend_requests", "is_in_steam_china", "with_scenario_save", "lobby_creation_time", "event_game_definition", "match_quality_data", "requested_hero_teams")
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UI: _ClassVar[CSODOTALobby.State]
        READYUP: _ClassVar[CSODOTALobby.State]
        SERVERSETUP: _ClassVar[CSODOTALobby.State]
        RUN: _ClassVar[CSODOTALobby.State]
        POSTGAME: _ClassVar[CSODOTALobby.State]
        NOTREADY: _ClassVar[CSODOTALobby.State]
        SERVERASSIGN: _ClassVar[CSODOTALobby.State]
    UI: CSODOTALobby.State
    READYUP: CSODOTALobby.State
    SERVERSETUP: CSODOTALobby.State
    RUN: CSODOTALobby.State
    POSTGAME: CSODOTALobby.State
    NOTREADY: CSODOTALobby.State
    SERVERASSIGN: CSODOTALobby.State
    class LobbyType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INVALID: _ClassVar[CSODOTALobby.LobbyType]
        CASUAL_MATCH: _ClassVar[CSODOTALobby.LobbyType]
        PRACTICE: _ClassVar[CSODOTALobby.LobbyType]
        COOP_BOT_MATCH: _ClassVar[CSODOTALobby.LobbyType]
        COMPETITIVE_MATCH: _ClassVar[CSODOTALobby.LobbyType]
        WEEKEND_TOURNEY: _ClassVar[CSODOTALobby.LobbyType]
        LOCAL_BOT_MATCH: _ClassVar[CSODOTALobby.LobbyType]
        SPECTATOR: _ClassVar[CSODOTALobby.LobbyType]
        EVENT_MATCH: _ClassVar[CSODOTALobby.LobbyType]
        NEW_PLAYER_POOL: _ClassVar[CSODOTALobby.LobbyType]
        FEATURED_GAMEMODE: _ClassVar[CSODOTALobby.LobbyType]
        AUTOMATED_BOT_ONLY_MATCH: _ClassVar[CSODOTALobby.LobbyType]
    INVALID: CSODOTALobby.LobbyType
    CASUAL_MATCH: CSODOTALobby.LobbyType
    PRACTICE: CSODOTALobby.LobbyType
    COOP_BOT_MATCH: CSODOTALobby.LobbyType
    COMPETITIVE_MATCH: CSODOTALobby.LobbyType
    WEEKEND_TOURNEY: CSODOTALobby.LobbyType
    LOCAL_BOT_MATCH: CSODOTALobby.LobbyType
    SPECTATOR: CSODOTALobby.LobbyType
    EVENT_MATCH: CSODOTALobby.LobbyType
    NEW_PLAYER_POOL: CSODOTALobby.LobbyType
    FEATURED_GAMEMODE: CSODOTALobby.LobbyType
    AUTOMATED_BOT_ONLY_MATCH: CSODOTALobby.LobbyType
    class CExtraMsg(_message.Message):
        __slots__ = ("id", "contents")
        ID_FIELD_NUMBER: _ClassVar[int]
        CONTENTS_FIELD_NUMBER: _ClassVar[int]
        id: int
        contents: bytes
        def __init__(self, id: _Optional[int] = ..., contents: _Optional[bytes] = ...) -> None: ...
    LOBBY_ID_FIELD_NUMBER: _ClassVar[int]
    ALL_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    MEMBER_INDICES_FIELD_NUMBER: _ClassVar[int]
    LEFT_MEMBER_INDICES_FIELD_NUMBER: _ClassVar[int]
    FREE_MEMBER_INDICES_FIELD_NUMBER: _ClassVar[int]
    LEADER_ID_FIELD_NUMBER: _ClassVar[int]
    SERVER_ID_FIELD_NUMBER: _ClassVar[int]
    GAME_MODE_FIELD_NUMBER: _ClassVar[int]
    PENDING_INVITES_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    CONNECT_FIELD_NUMBER: _ClassVar[int]
    LOBBY_TYPE_FIELD_NUMBER: _ClassVar[int]
    ALLOW_CHEATS_FIELD_NUMBER: _ClassVar[int]
    FILL_WITH_BOTS_FIELD_NUMBER: _ClassVar[int]
    GAME_NAME_FIELD_NUMBER: _ClassVar[int]
    TEAM_DETAILS_FIELD_NUMBER: _ClassVar[int]
    TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TOURNAMENT_GAME_ID_FIELD_NUMBER: _ClassVar[int]
    SERVER_REGION_FIELD_NUMBER: _ClassVar[int]
    GAME_STATE_FIELD_NUMBER: _ClassVar[int]
    NUM_SPECTATORS_FIELD_NUMBER: _ClassVar[int]
    MATCHGROUP_FIELD_NUMBER: _ClassVar[int]
    CM_PICK_FIELD_NUMBER: _ClassVar[int]
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    ALLOW_SPECTATING_FIELD_NUMBER: _ClassVar[int]
    BOT_DIFFICULTY_RADIANT_FIELD_NUMBER: _ClassVar[int]
    PASS_KEY_FIELD_NUMBER: _ClassVar[int]
    LEAGUEID_FIELD_NUMBER: _ClassVar[int]
    PENALTY_LEVEL_RADIANT_FIELD_NUMBER: _ClassVar[int]
    PENALTY_LEVEL_DIRE_FIELD_NUMBER: _ClassVar[int]
    SERIES_TYPE_FIELD_NUMBER: _ClassVar[int]
    RADIANT_SERIES_WINS_FIELD_NUMBER: _ClassVar[int]
    DIRE_SERIES_WINS_FIELD_NUMBER: _ClassVar[int]
    ALLCHAT_FIELD_NUMBER: _ClassVar[int]
    DOTA_TV_DELAY_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_MODE_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_MAP_NAME_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_DIFFICULTY_FIELD_NUMBER: _ClassVar[int]
    LAN_FIELD_NUMBER: _ClassVar[int]
    BROADCAST_CHANNEL_INFO_FIELD_NUMBER: _ClassVar[int]
    FIRST_LEAVER_ACCOUNTID_FIELD_NUMBER: _ClassVar[int]
    SERIES_ID_FIELD_NUMBER: _ClassVar[int]
    LOW_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    EXTRA_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    FIRST_BLOOD_HAPPENED_FIELD_NUMBER: _ClassVar[int]
    MATCH_OUTCOME_FIELD_NUMBER: _ClassVar[int]
    MASS_DISCONNECT_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_ID_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_MIN_PLAYERS_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_MAX_PLAYERS_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_CRC_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_AUTO_CREATED_LOBBY_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_SERIES_MATCHES_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_MATCH_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    GAME_START_TIME_FIELD_NUMBER: _ClassVar[int]
    PAUSE_SETTING_FIELD_NUMBER: _ClassVar[int]
    WEEKEND_TOURNEY_DIVISION_ID_FIELD_NUMBER: _ClassVar[int]
    WEEKEND_TOURNEY_SKILL_LEVEL_FIELD_NUMBER: _ClassVar[int]
    WEEKEND_TOURNEY_BRACKET_ROUND_FIELD_NUMBER: _ClassVar[int]
    BOT_DIFFICULTY_DIRE_FIELD_NUMBER: _ClassVar[int]
    BOT_RADIANT_FIELD_NUMBER: _ClassVar[int]
    BOT_DIRE_FIELD_NUMBER: _ClassVar[int]
    EVENT_PROGRESSION_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SELECTION_PRIORITY_RULES_FIELD_NUMBER: _ClassVar[int]
    SERIES_PREVIOUS_SELECTION_PRIORITY_TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    SERIES_CURRENT_SELECTION_PRIORITY_TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    SERIES_CURRENT_PRIORITY_TEAM_CHOICE_FIELD_NUMBER: _ClassVar[int]
    SERIES_CURRENT_NON_PRIORITY_TEAM_CHOICE_FIELD_NUMBER: _ClassVar[int]
    SERIES_CURRENT_SELECTION_PRIORITY_USED_COIN_TOSS_FIELD_NUMBER: _ClassVar[int]
    CURRENT_PRIMARY_EVENT_FIELD_NUMBER: _ClassVar[int]
    CURRENT_PRIMARY_EVENT_FOR_DISPLAY_FIELD_NUMBER: _ClassVar[int]
    EMERGENCY_DISABLED_HERO_IDS_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_PRIVATE_KEY_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_PENALTIES_FIELD_NUMBER: _ClassVar[int]
    LAN_HOST_PING_LOCATION_FIELD_NUMBER: _ClassVar[int]
    LEAGUE_NODE_ID_FIELD_NUMBER: _ClassVar[int]
    MATCH_DURATION_FIELD_NUMBER: _ClassVar[int]
    LEAGUE_PHASE_FIELD_NUMBER: _ClassVar[int]
    EXPERIMENTAL_GAMEPLAY_ENABLED_FIELD_NUMBER: _ClassVar[int]
    GUILD_CHALLENGES_FIELD_NUMBER: _ClassVar[int]
    GUILD_DETAILS_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_HERO_IDS_FIELD_NUMBER: _ClassVar[int]
    COACH_FRIEND_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    IS_IN_STEAM_CHINA_FIELD_NUMBER: _ClassVar[int]
    WITH_SCENARIO_SAVE_FIELD_NUMBER: _ClassVar[int]
    LOBBY_CREATION_TIME_FIELD_NUMBER: _ClassVar[int]
    EVENT_GAME_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    MATCH_QUALITY_DATA_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_HERO_TEAMS_FIELD_NUMBER: _ClassVar[int]
    lobby_id: int
    all_members: _containers.RepeatedCompositeFieldContainer[CSODOTALobbyMember]
    member_indices: _containers.RepeatedScalarFieldContainer[int]
    left_member_indices: _containers.RepeatedScalarFieldContainer[int]
    free_member_indices: _containers.RepeatedScalarFieldContainer[int]
    leader_id: int
    server_id: int
    game_mode: int
    pending_invites: _containers.RepeatedScalarFieldContainer[int]
    state: CSODOTALobby.State
    connect: str
    lobby_type: CSODOTALobby.LobbyType
    allow_cheats: bool
    fill_with_bots: bool
    game_name: str
    team_details: _containers.RepeatedCompositeFieldContainer[CLobbyTeamDetails]
    tournament_id: int
    tournament_game_id: int
    server_region: int
    game_state: _dota_shared_enums_pb2.DOTA_GameState
    num_spectators: int
    matchgroup: int
    cm_pick: _dota_shared_enums_pb2.DOTA_CM_PICK
    match_id: int
    allow_spectating: bool
    bot_difficulty_radiant: _dota_shared_enums_pb2.DOTABotDifficulty
    pass_key: str
    leagueid: int
    penalty_level_radiant: int
    penalty_level_dire: int
    series_type: int
    radiant_series_wins: int
    dire_series_wins: int
    allchat: bool
    dota_tv_delay: LobbyDotaTVDelay
    custom_game_mode: str
    custom_map_name: str
    custom_difficulty: int
    lan: bool
    broadcast_channel_info: _containers.RepeatedCompositeFieldContainer[CLobbyBroadcastChannelInfo]
    first_leaver_accountid: int
    series_id: int
    low_priority: bool
    extra_messages: _containers.RepeatedCompositeFieldContainer[CSODOTALobby.CExtraMsg]
    first_blood_happened: bool
    match_outcome: _dota_shared_enums_pb2.EMatchOutcome
    mass_disconnect: bool
    custom_game_id: int
    custom_min_players: int
    custom_max_players: int
    visibility: _dota_shared_enums_pb2.DOTALobbyVisibility
    custom_game_crc: int
    custom_game_auto_created_lobby: bool
    custom_game_timestamp: int
    previous_series_matches: _containers.RepeatedScalarFieldContainer[int]
    previous_match_override: int
    game_start_time: int
    pause_setting: LobbyDotaPauseSetting
    weekend_tourney_division_id: int
    weekend_tourney_skill_level: int
    weekend_tourney_bracket_round: int
    bot_difficulty_dire: _dota_shared_enums_pb2.DOTABotDifficulty
    bot_radiant: int
    bot_dire: int
    event_progression_enabled: _containers.RepeatedScalarFieldContainer[_dota_shared_enums_pb2.EEvent]
    selection_priority_rules: _dota_shared_enums_pb2.DOTASelectionPriorityRules
    series_previous_selection_priority_team_id: int
    series_current_selection_priority_team_id: int
    series_current_priority_team_choice: _dota_shared_enums_pb2.DOTASelectionPriorityChoice
    series_current_non_priority_team_choice: _dota_shared_enums_pb2.DOTASelectionPriorityChoice
    series_current_selection_priority_used_coin_toss: bool
    current_primary_event: _dota_shared_enums_pb2.EEvent
    current_primary_event_for_display: _dota_shared_enums_pb2.EEvent
    emergency_disabled_hero_ids: _containers.RepeatedScalarFieldContainer[int]
    custom_game_private_key: int
    custom_game_penalties: bool
    lan_host_ping_location: str
    league_node_id: int
    match_duration: int
    league_phase: int
    experimental_gameplay_enabled: bool
    guild_challenges: _containers.RepeatedCompositeFieldContainer[CLobbyGuildChallenge]
    guild_details: _containers.RepeatedCompositeFieldContainer[CLobbyGuildDetails]
    requested_hero_ids: _containers.RepeatedScalarFieldContainer[int]
    coach_friend_requests: _containers.RepeatedCompositeFieldContainer[CMsgLobbyCoachFriendRequest]
    is_in_steam_china: bool
    with_scenario_save: bool
    lobby_creation_time: int
    event_game_definition: str
    match_quality_data: CDOTALobbyMatchQualityData
    requested_hero_teams: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, lobby_id: _Optional[int] = ..., all_members: _Optional[_Iterable[_Union[CSODOTALobbyMember, _Mapping]]] = ..., member_indices: _Optional[_Iterable[int]] = ..., left_member_indices: _Optional[_Iterable[int]] = ..., free_member_indices: _Optional[_Iterable[int]] = ..., leader_id: _Optional[int] = ..., server_id: _Optional[int] = ..., game_mode: _Optional[int] = ..., pending_invites: _Optional[_Iterable[int]] = ..., state: _Optional[_Union[CSODOTALobby.State, str]] = ..., connect: _Optional[str] = ..., lobby_type: _Optional[_Union[CSODOTALobby.LobbyType, str]] = ..., allow_cheats: bool = ..., fill_with_bots: bool = ..., game_name: _Optional[str] = ..., team_details: _Optional[_Iterable[_Union[CLobbyTeamDetails, _Mapping]]] = ..., tournament_id: _Optional[int] = ..., tournament_game_id: _Optional[int] = ..., server_region: _Optional[int] = ..., game_state: _Optional[_Union[_dota_shared_enums_pb2.DOTA_GameState, str]] = ..., num_spectators: _Optional[int] = ..., matchgroup: _Optional[int] = ..., cm_pick: _Optional[_Union[_dota_shared_enums_pb2.DOTA_CM_PICK, str]] = ..., match_id: _Optional[int] = ..., allow_spectating: bool = ..., bot_difficulty_radiant: _Optional[_Union[_dota_shared_enums_pb2.DOTABotDifficulty, str]] = ..., pass_key: _Optional[str] = ..., leagueid: _Optional[int] = ..., penalty_level_radiant: _Optional[int] = ..., penalty_level_dire: _Optional[int] = ..., series_type: _Optional[int] = ..., radiant_series_wins: _Optional[int] = ..., dire_series_wins: _Optional[int] = ..., allchat: bool = ..., dota_tv_delay: _Optional[_Union[LobbyDotaTVDelay, str]] = ..., custom_game_mode: _Optional[str] = ..., custom_map_name: _Optional[str] = ..., custom_difficulty: _Optional[int] = ..., lan: bool = ..., broadcast_channel_info: _Optional[_Iterable[_Union[CLobbyBroadcastChannelInfo, _Mapping]]] = ..., first_leaver_accountid: _Optional[int] = ..., series_id: _Optional[int] = ..., low_priority: bool = ..., extra_messages: _Optional[_Iterable[_Union[CSODOTALobby.CExtraMsg, _Mapping]]] = ..., first_blood_happened: bool = ..., match_outcome: _Optional[_Union[_dota_shared_enums_pb2.EMatchOutcome, str]] = ..., mass_disconnect: bool = ..., custom_game_id: _Optional[int] = ..., custom_min_players: _Optional[int] = ..., custom_max_players: _Optional[int] = ..., visibility: _Optional[_Union[_dota_shared_enums_pb2.DOTALobbyVisibility, str]] = ..., custom_game_crc: _Optional[int] = ..., custom_game_auto_created_lobby: bool = ..., custom_game_timestamp: _Optional[int] = ..., previous_series_matches: _Optional[_Iterable[int]] = ..., previous_match_override: _Optional[int] = ..., game_start_time: _Optional[int] = ..., pause_setting: _Optional[_Union[LobbyDotaPauseSetting, str]] = ..., weekend_tourney_division_id: _Optional[int] = ..., weekend_tourney_skill_level: _Optional[int] = ..., weekend_tourney_bracket_round: _Optional[int] = ..., bot_difficulty_dire: _Optional[_Union[_dota_shared_enums_pb2.DOTABotDifficulty, str]] = ..., bot_radiant: _Optional[int] = ..., bot_dire: _Optional[int] = ..., event_progression_enabled: _Optional[_Iterable[_Union[_dota_shared_enums_pb2.EEvent, str]]] = ..., selection_priority_rules: _Optional[_Union[_dota_shared_enums_pb2.DOTASelectionPriorityRules, str]] = ..., series_previous_selection_priority_team_id: _Optional[int] = ..., series_current_selection_priority_team_id: _Optional[int] = ..., series_current_priority_team_choice: _Optional[_Union[_dota_shared_enums_pb2.DOTASelectionPriorityChoice, str]] = ..., series_current_non_priority_team_choice: _Optional[_Union[_dota_shared_enums_pb2.DOTASelectionPriorityChoice, str]] = ..., series_current_selection_priority_used_coin_toss: bool = ..., current_primary_event: _Optional[_Union[_dota_shared_enums_pb2.EEvent, str]] = ..., current_primary_event_for_display: _Optional[_Union[_dota_shared_enums_pb2.EEvent, str]] = ..., emergency_disabled_hero_ids: _Optional[_Iterable[int]] = ..., custom_game_private_key: _Optional[int] = ..., custom_game_penalties: bool = ..., lan_host_ping_location: _Optional[str] = ..., league_node_id: _Optional[int] = ..., match_duration: _Optional[int] = ..., league_phase: _Optional[int] = ..., experimental_gameplay_enabled: bool = ..., guild_challenges: _Optional[_Iterable[_Union[CLobbyGuildChallenge, _Mapping]]] = ..., guild_details: _Optional[_Iterable[_Union[CLobbyGuildDetails, _Mapping]]] = ..., requested_hero_ids: _Optional[_Iterable[int]] = ..., coach_friend_requests: _Optional[_Iterable[_Union[CMsgLobbyCoachFriendRequest, _Mapping]]] = ..., is_in_steam_china: bool = ..., with_scenario_save: bool = ..., lobby_creation_time: _Optional[int] = ..., event_game_definition: _Optional[str] = ..., match_quality_data: _Optional[_Union[CDOTALobbyMatchQualityData, _Mapping]] = ..., requested_hero_teams: _Optional[_Iterable[int]] = ...) -> None: ...

class CSODOTAServerLobby(_message.Message):
    __slots__ = ("all_members", "extra_startup_messages", "broadcast_active")
    ALL_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    EXTRA_STARTUP_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    BROADCAST_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    all_members: _containers.RepeatedCompositeFieldContainer[CSODOTAServerLobbyMember]
    extra_startup_messages: _containers.RepeatedCompositeFieldContainer[CSODOTALobby.CExtraMsg]
    broadcast_active: bool
    def __init__(self, all_members: _Optional[_Iterable[_Union[CSODOTAServerLobbyMember, _Mapping]]] = ..., extra_startup_messages: _Optional[_Iterable[_Union[CSODOTALobby.CExtraMsg, _Mapping]]] = ..., broadcast_active: bool = ...) -> None: ...

class CSODOTAStaticLobby(_message.Message):
    __slots__ = ("all_members", "is_player_draft", "is_last_match_in_series")
    ALL_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    IS_PLAYER_DRAFT_FIELD_NUMBER: _ClassVar[int]
    IS_LAST_MATCH_IN_SERIES_FIELD_NUMBER: _ClassVar[int]
    all_members: _containers.RepeatedCompositeFieldContainer[CSODOTAStaticLobbyMember]
    is_player_draft: bool
    is_last_match_in_series: bool
    def __init__(self, all_members: _Optional[_Iterable[_Union[CSODOTAStaticLobbyMember, _Mapping]]] = ..., is_player_draft: bool = ..., is_last_match_in_series: bool = ...) -> None: ...

class CSODOTAServerStaticLobby(_message.Message):
    __slots__ = ("all_members", "post_patch_strategy_time_buffer", "lobby_event_points", "broadcast_url")
    ALL_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    POST_PATCH_STRATEGY_TIME_BUFFER_FIELD_NUMBER: _ClassVar[int]
    LOBBY_EVENT_POINTS_FIELD_NUMBER: _ClassVar[int]
    BROADCAST_URL_FIELD_NUMBER: _ClassVar[int]
    all_members: _containers.RepeatedCompositeFieldContainer[CSODOTAServerStaticLobbyMember]
    post_patch_strategy_time_buffer: float
    lobby_event_points: _containers.RepeatedCompositeFieldContainer[CMsgLobbyEventPoints]
    broadcast_url: str
    def __init__(self, all_members: _Optional[_Iterable[_Union[CSODOTAServerStaticLobbyMember, _Mapping]]] = ..., post_patch_strategy_time_buffer: _Optional[float] = ..., lobby_event_points: _Optional[_Iterable[_Union[CMsgLobbyEventPoints, _Mapping]]] = ..., broadcast_url: _Optional[str] = ...) -> None: ...

class CMsgAdditionalLobbyStartupAccountData(_message.Message):
    __slots__ = ("account_id", "plus_data", "unlocked_chat_wheel_message_ranges", "unlocked_ping_wheel_message_ranges")
    class ChatWheelMessageRange(_message.Message):
        __slots__ = ("message_id_start", "message_id_end")
        MESSAGE_ID_START_FIELD_NUMBER: _ClassVar[int]
        MESSAGE_ID_END_FIELD_NUMBER: _ClassVar[int]
        message_id_start: int
        message_id_end: int
        def __init__(self, message_id_start: _Optional[int] = ..., message_id_end: _Optional[int] = ...) -> None: ...
    class PingWheelMessageRange(_message.Message):
        __slots__ = ("message_id_start", "message_id_end")
        MESSAGE_ID_START_FIELD_NUMBER: _ClassVar[int]
        MESSAGE_ID_END_FIELD_NUMBER: _ClassVar[int]
        message_id_start: int
        message_id_end: int
        def __init__(self, message_id_start: _Optional[int] = ..., message_id_end: _Optional[int] = ...) -> None: ...
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    PLUS_DATA_FIELD_NUMBER: _ClassVar[int]
    UNLOCKED_CHAT_WHEEL_MESSAGE_RANGES_FIELD_NUMBER: _ClassVar[int]
    UNLOCKED_PING_WHEEL_MESSAGE_RANGES_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    plus_data: CMsgLobbyPlayerPlusSubscriptionData
    unlocked_chat_wheel_message_ranges: _containers.RepeatedCompositeFieldContainer[CMsgAdditionalLobbyStartupAccountData.ChatWheelMessageRange]
    unlocked_ping_wheel_message_ranges: _containers.RepeatedCompositeFieldContainer[CMsgAdditionalLobbyStartupAccountData.PingWheelMessageRange]
    def __init__(self, account_id: _Optional[int] = ..., plus_data: _Optional[_Union[CMsgLobbyPlayerPlusSubscriptionData, _Mapping]] = ..., unlocked_chat_wheel_message_ranges: _Optional[_Iterable[_Union[CMsgAdditionalLobbyStartupAccountData.ChatWheelMessageRange, _Mapping]]] = ..., unlocked_ping_wheel_message_ranges: _Optional[_Iterable[_Union[CMsgAdditionalLobbyStartupAccountData.PingWheelMessageRange, _Mapping]]] = ...) -> None: ...

class CMsgLobbyInitializationComplete(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgLobbyPlaytestDetails(_message.Message):
    __slots__ = ("json",)
    JSON_FIELD_NUMBER: _ClassVar[int]
    json: str
    def __init__(self, json: _Optional[str] = ...) -> None: ...

class CMsgLocalServerGuildData(_message.Message):
    __slots__ = ("guild_id", "event_id", "guild_points", "guild_logo", "guild_primary_color", "guild_secondary_color", "guild_pattern", "guild_flags", "guild_weekly_percentile")
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    GUILD_POINTS_FIELD_NUMBER: _ClassVar[int]
    GUILD_LOGO_FIELD_NUMBER: _ClassVar[int]
    GUILD_PRIMARY_COLOR_FIELD_NUMBER: _ClassVar[int]
    GUILD_SECONDARY_COLOR_FIELD_NUMBER: _ClassVar[int]
    GUILD_PATTERN_FIELD_NUMBER: _ClassVar[int]
    GUILD_FLAGS_FIELD_NUMBER: _ClassVar[int]
    GUILD_WEEKLY_PERCENTILE_FIELD_NUMBER: _ClassVar[int]
    guild_id: int
    event_id: _dota_shared_enums_pb2.EEvent
    guild_points: int
    guild_logo: int
    guild_primary_color: int
    guild_secondary_color: int
    guild_pattern: int
    guild_flags: int
    guild_weekly_percentile: int
    def __init__(self, guild_id: _Optional[int] = ..., event_id: _Optional[_Union[_dota_shared_enums_pb2.EEvent, str]] = ..., guild_points: _Optional[int] = ..., guild_logo: _Optional[int] = ..., guild_primary_color: _Optional[int] = ..., guild_secondary_color: _Optional[int] = ..., guild_pattern: _Optional[int] = ..., guild_flags: _Optional[int] = ..., guild_weekly_percentile: _Optional[int] = ...) -> None: ...

class CMsgLocalServerFakeLobbyData(_message.Message):
    __slots__ = ("account_id", "event_points", "is_plus_subscriber", "primary_event_id", "favorite_team", "favorite_team_quality", "guild_info", "teleport_fx_level", "additional_data")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_POINTS_FIELD_NUMBER: _ClassVar[int]
    IS_PLUS_SUBSCRIBER_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    FAVORITE_TEAM_FIELD_NUMBER: _ClassVar[int]
    FAVORITE_TEAM_QUALITY_FIELD_NUMBER: _ClassVar[int]
    GUILD_INFO_FIELD_NUMBER: _ClassVar[int]
    TELEPORT_FX_LEVEL_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_DATA_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    event_points: _containers.RepeatedCompositeFieldContainer[CMsgLobbyEventPoints]
    is_plus_subscriber: bool
    primary_event_id: int
    favorite_team: int
    favorite_team_quality: int
    guild_info: CMsgLocalServerGuildData
    teleport_fx_level: int
    additional_data: CMsgAdditionalLobbyStartupAccountData
    def __init__(self, account_id: _Optional[int] = ..., event_points: _Optional[_Iterable[_Union[CMsgLobbyEventPoints, _Mapping]]] = ..., is_plus_subscriber: bool = ..., primary_event_id: _Optional[int] = ..., favorite_team: _Optional[int] = ..., favorite_team_quality: _Optional[int] = ..., guild_info: _Optional[_Union[CMsgLocalServerGuildData, _Mapping]] = ..., teleport_fx_level: _Optional[int] = ..., additional_data: _Optional[_Union[CMsgAdditionalLobbyStartupAccountData, _Mapping]] = ...) -> None: ...
