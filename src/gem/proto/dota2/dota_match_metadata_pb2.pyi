import base_gcmessages_pb2 as _base_gcmessages_pb2
import dota_gcmessages_common_match_management_pb2 as _dota_gcmessages_common_match_management_pb2
import dota_gcmessages_common_lobby_pb2 as _dota_gcmessages_common_lobby_pb2
import dota_gcmessages_common_overworld_pb2 as _dota_gcmessages_common_overworld_pb2
import dota_gcmessages_common_craftworks_pb2 as _dota_gcmessages_common_craftworks_pb2
import dota_gcmessages_common_monster_hunter_pb2 as _dota_gcmessages_common_monster_hunter_pb2
import dota_gcmessages_common_pb2 as _dota_gcmessages_common_pb2
import dota_shared_enums_pb2 as _dota_shared_enums_pb2
import gcsdk_gcmessages_pb2 as _gcsdk_gcmessages_pb2
import networkbasetypes_pb2 as _networkbasetypes_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EPlayerInventorySnapshotFlags(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EPlayerInventorySnapshotFlags_HasScepter: _ClassVar[EPlayerInventorySnapshotFlags]
    EPlayerInventorySnapshotFlags_HasShard: _ClassVar[EPlayerInventorySnapshotFlags]
EPlayerInventorySnapshotFlags_HasScepter: EPlayerInventorySnapshotFlags
EPlayerInventorySnapshotFlags_HasShard: EPlayerInventorySnapshotFlags

class CDOTAMatchMetadataFile(_message.Message):
    __slots__ = ("version", "match_id", "metadata", "private_metadata")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_METADATA_FIELD_NUMBER: _ClassVar[int]
    version: int
    match_id: int
    metadata: CDOTAMatchMetadata
    private_metadata: bytes
    def __init__(self, version: _Optional[int] = ..., match_id: _Optional[int] = ..., metadata: _Optional[_Union[CDOTAMatchMetadata, _Mapping]] = ..., private_metadata: _Optional[bytes] = ...) -> None: ...

class CDOTAMatchMetadata(_message.Message):
    __slots__ = ("teams", "lobby_id", "report_until_time", "event_game_custom_table", "primary_event_id", "matchmaking_stats", "mvp_data", "guild_challenge_progress", "custom_post_game_table", "match_tips", "match_tracked_stats", "primary_event_id_for_display")
    class EconItem(_message.Message):
        __slots__ = ("def_index", "quality", "attribute", "style", "equipped_state")
        DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
        QUALITY_FIELD_NUMBER: _ClassVar[int]
        ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
        STYLE_FIELD_NUMBER: _ClassVar[int]
        EQUIPPED_STATE_FIELD_NUMBER: _ClassVar[int]
        def_index: int
        quality: int
        attribute: _containers.RepeatedCompositeFieldContainer[_base_gcmessages_pb2.CSOEconItemAttribute]
        style: int
        equipped_state: _containers.RepeatedCompositeFieldContainer[_base_gcmessages_pb2.CSOEconItemEquipped]
        def __init__(self, def_index: _Optional[int] = ..., quality: _Optional[int] = ..., attribute: _Optional[_Iterable[_Union[_base_gcmessages_pb2.CSOEconItemAttribute, _Mapping]]] = ..., style: _Optional[int] = ..., equipped_state: _Optional[_Iterable[_Union[_base_gcmessages_pb2.CSOEconItemEquipped, _Mapping]]] = ...) -> None: ...
    class Team(_message.Message):
        __slots__ = ("dota_team", "players", "graph_experience", "graph_gold_earned", "graph_net_worth", "cm_first_pick", "cm_captain_player_id", "cm_penalty", "team_tracked_stats", "kills")
        class PlayerKill(_message.Message):
            __slots__ = ("victim_slot", "count")
            VICTIM_SLOT_FIELD_NUMBER: _ClassVar[int]
            COUNT_FIELD_NUMBER: _ClassVar[int]
            victim_slot: int
            count: int
            def __init__(self, victim_slot: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
        class ItemPurchase(_message.Message):
            __slots__ = ("item_id", "purchase_time")
            ITEM_ID_FIELD_NUMBER: _ClassVar[int]
            PURCHASE_TIME_FIELD_NUMBER: _ClassVar[int]
            item_id: int
            purchase_time: int
            def __init__(self, item_id: _Optional[int] = ..., purchase_time: _Optional[int] = ...) -> None: ...
        class InventorySnapshot(_message.Message):
            __slots__ = ("item_id", "game_time", "kills", "deaths", "assists", "level", "backpack_item_id", "neutral_item_id", "neutral_enhancement_id", "last_hits", "denies", "flags")
            ITEM_ID_FIELD_NUMBER: _ClassVar[int]
            GAME_TIME_FIELD_NUMBER: _ClassVar[int]
            KILLS_FIELD_NUMBER: _ClassVar[int]
            DEATHS_FIELD_NUMBER: _ClassVar[int]
            ASSISTS_FIELD_NUMBER: _ClassVar[int]
            LEVEL_FIELD_NUMBER: _ClassVar[int]
            BACKPACK_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
            NEUTRAL_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
            NEUTRAL_ENHANCEMENT_ID_FIELD_NUMBER: _ClassVar[int]
            LAST_HITS_FIELD_NUMBER: _ClassVar[int]
            DENIES_FIELD_NUMBER: _ClassVar[int]
            FLAGS_FIELD_NUMBER: _ClassVar[int]
            item_id: _containers.RepeatedScalarFieldContainer[int]
            game_time: int
            kills: int
            deaths: int
            assists: int
            level: int
            backpack_item_id: _containers.RepeatedScalarFieldContainer[int]
            neutral_item_id: int
            neutral_enhancement_id: int
            last_hits: int
            denies: int
            flags: int
            def __init__(self, item_id: _Optional[_Iterable[int]] = ..., game_time: _Optional[int] = ..., kills: _Optional[int] = ..., deaths: _Optional[int] = ..., assists: _Optional[int] = ..., level: _Optional[int] = ..., backpack_item_id: _Optional[_Iterable[int]] = ..., neutral_item_id: _Optional[int] = ..., neutral_enhancement_id: _Optional[int] = ..., last_hits: _Optional[int] = ..., denies: _Optional[int] = ..., flags: _Optional[int] = ...) -> None: ...
        class AutoStyleCriteria(_message.Message):
            __slots__ = ("name_token", "value")
            NAME_TOKEN_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            name_token: int
            value: float
            def __init__(self, name_token: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...
        class StrangeGemProgress(_message.Message):
            __slots__ = ("kill_eater_type", "gem_item_def_index", "required_hero_id", "starting_value", "ending_value", "owner_item_def_index", "owner_item_id")
            KILL_EATER_TYPE_FIELD_NUMBER: _ClassVar[int]
            GEM_ITEM_DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
            REQUIRED_HERO_ID_FIELD_NUMBER: _ClassVar[int]
            STARTING_VALUE_FIELD_NUMBER: _ClassVar[int]
            ENDING_VALUE_FIELD_NUMBER: _ClassVar[int]
            OWNER_ITEM_DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
            OWNER_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
            kill_eater_type: int
            gem_item_def_index: int
            required_hero_id: int
            starting_value: int
            ending_value: int
            owner_item_def_index: int
            owner_item_id: int
            def __init__(self, kill_eater_type: _Optional[int] = ..., gem_item_def_index: _Optional[int] = ..., required_hero_id: _Optional[int] = ..., starting_value: _Optional[int] = ..., ending_value: _Optional[int] = ..., owner_item_def_index: _Optional[int] = ..., owner_item_id: _Optional[int] = ...) -> None: ...
        class VictoryPrediction(_message.Message):
            __slots__ = ("item_id", "item_def_index", "starting_value", "is_victory")
            ITEM_ID_FIELD_NUMBER: _ClassVar[int]
            ITEM_DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
            STARTING_VALUE_FIELD_NUMBER: _ClassVar[int]
            IS_VICTORY_FIELD_NUMBER: _ClassVar[int]
            item_id: int
            item_def_index: int
            starting_value: int
            is_victory: bool
            def __init__(self, item_id: _Optional[int] = ..., item_def_index: _Optional[int] = ..., starting_value: _Optional[int] = ..., is_victory: bool = ...) -> None: ...
        class SubChallenge(_message.Message):
            __slots__ = ("slot_id", "start_value", "end_value", "completed")
            SLOT_ID_FIELD_NUMBER: _ClassVar[int]
            START_VALUE_FIELD_NUMBER: _ClassVar[int]
            END_VALUE_FIELD_NUMBER: _ClassVar[int]
            COMPLETED_FIELD_NUMBER: _ClassVar[int]
            slot_id: int
            start_value: int
            end_value: int
            completed: bool
            def __init__(self, slot_id: _Optional[int] = ..., start_value: _Optional[int] = ..., end_value: _Optional[int] = ..., completed: bool = ...) -> None: ...
        class CavernChallengeResult(_message.Message):
            __slots__ = ("completed_path_id", "claimed_room_id")
            COMPLETED_PATH_ID_FIELD_NUMBER: _ClassVar[int]
            CLAIMED_ROOM_ID_FIELD_NUMBER: _ClassVar[int]
            completed_path_id: int
            claimed_room_id: int
            def __init__(self, completed_path_id: _Optional[int] = ..., claimed_room_id: _Optional[int] = ...) -> None: ...
        class ActionGrant(_message.Message):
            __slots__ = ("action_id", "quantity", "audit", "audit_data")
            ACTION_ID_FIELD_NUMBER: _ClassVar[int]
            QUANTITY_FIELD_NUMBER: _ClassVar[int]
            AUDIT_FIELD_NUMBER: _ClassVar[int]
            AUDIT_DATA_FIELD_NUMBER: _ClassVar[int]
            action_id: int
            quantity: int
            audit: int
            audit_data: int
            def __init__(self, action_id: _Optional[int] = ..., quantity: _Optional[int] = ..., audit: _Optional[int] = ..., audit_data: _Optional[int] = ...) -> None: ...
        class CandyGrant(_message.Message):
            __slots__ = ("points", "reason")
            POINTS_FIELD_NUMBER: _ClassVar[int]
            REASON_FIELD_NUMBER: _ClassVar[int]
            points: int
            reason: int
            def __init__(self, points: _Optional[int] = ..., reason: _Optional[int] = ...) -> None: ...
        class PeriodicResourceData(_message.Message):
            __slots__ = ("periodic_resource_id", "remaining", "max")
            PERIODIC_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
            REMAINING_FIELD_NUMBER: _ClassVar[int]
            MAX_FIELD_NUMBER: _ClassVar[int]
            periodic_resource_id: int
            remaining: int
            max: int
            def __init__(self, periodic_resource_id: _Optional[int] = ..., remaining: _Optional[int] = ..., max: _Optional[int] = ...) -> None: ...
        class EventData(_message.Message):
            __slots__ = ("event_id", "event_points", "challenge_instance_id", "challenge_quest_id", "challenge_quest_challenge_id", "challenge_completed", "challenge_rank_completed", "challenge_rank_previously_completed", "event_owned", "sub_challenges_with_progress", "wager_winnings", "cavern_challenge_active", "cavern_challenge_winnings", "amount_wagered", "periodic_point_adjustments", "cavern_challenge_map_results", "cavern_challenge_plus_shard_winnings", "actions_granted", "cavern_crawl_map_variant", "team_wager_bonus_pct", "wager_streak_pct", "candy_points_granted", "active_season_id", "cavern_crawl_half_credit", "periodic_resources", "extra_event_messages")
            EVENT_ID_FIELD_NUMBER: _ClassVar[int]
            EVENT_POINTS_FIELD_NUMBER: _ClassVar[int]
            CHALLENGE_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
            CHALLENGE_QUEST_ID_FIELD_NUMBER: _ClassVar[int]
            CHALLENGE_QUEST_CHALLENGE_ID_FIELD_NUMBER: _ClassVar[int]
            CHALLENGE_COMPLETED_FIELD_NUMBER: _ClassVar[int]
            CHALLENGE_RANK_COMPLETED_FIELD_NUMBER: _ClassVar[int]
            CHALLENGE_RANK_PREVIOUSLY_COMPLETED_FIELD_NUMBER: _ClassVar[int]
            EVENT_OWNED_FIELD_NUMBER: _ClassVar[int]
            SUB_CHALLENGES_WITH_PROGRESS_FIELD_NUMBER: _ClassVar[int]
            WAGER_WINNINGS_FIELD_NUMBER: _ClassVar[int]
            CAVERN_CHALLENGE_ACTIVE_FIELD_NUMBER: _ClassVar[int]
            CAVERN_CHALLENGE_WINNINGS_FIELD_NUMBER: _ClassVar[int]
            AMOUNT_WAGERED_FIELD_NUMBER: _ClassVar[int]
            PERIODIC_POINT_ADJUSTMENTS_FIELD_NUMBER: _ClassVar[int]
            CAVERN_CHALLENGE_MAP_RESULTS_FIELD_NUMBER: _ClassVar[int]
            CAVERN_CHALLENGE_PLUS_SHARD_WINNINGS_FIELD_NUMBER: _ClassVar[int]
            ACTIONS_GRANTED_FIELD_NUMBER: _ClassVar[int]
            CAVERN_CRAWL_MAP_VARIANT_FIELD_NUMBER: _ClassVar[int]
            TEAM_WAGER_BONUS_PCT_FIELD_NUMBER: _ClassVar[int]
            WAGER_STREAK_PCT_FIELD_NUMBER: _ClassVar[int]
            CANDY_POINTS_GRANTED_FIELD_NUMBER: _ClassVar[int]
            ACTIVE_SEASON_ID_FIELD_NUMBER: _ClassVar[int]
            CAVERN_CRAWL_HALF_CREDIT_FIELD_NUMBER: _ClassVar[int]
            PERIODIC_RESOURCES_FIELD_NUMBER: _ClassVar[int]
            EXTRA_EVENT_MESSAGES_FIELD_NUMBER: _ClassVar[int]
            event_id: int
            event_points: int
            challenge_instance_id: int
            challenge_quest_id: int
            challenge_quest_challenge_id: int
            challenge_completed: bool
            challenge_rank_completed: int
            challenge_rank_previously_completed: int
            event_owned: bool
            sub_challenges_with_progress: _containers.RepeatedCompositeFieldContainer[CDOTAMatchMetadata.Team.SubChallenge]
            wager_winnings: int
            cavern_challenge_active: bool
            cavern_challenge_winnings: int
            amount_wagered: int
            periodic_point_adjustments: int
            cavern_challenge_map_results: _containers.RepeatedCompositeFieldContainer[CDOTAMatchMetadata.Team.CavernChallengeResult]
            cavern_challenge_plus_shard_winnings: int
            actions_granted: _containers.RepeatedCompositeFieldContainer[CDOTAMatchMetadata.Team.ActionGrant]
            cavern_crawl_map_variant: int
            team_wager_bonus_pct: int
            wager_streak_pct: int
            candy_points_granted: _containers.RepeatedCompositeFieldContainer[CDOTAMatchMetadata.Team.CandyGrant]
            active_season_id: int
            cavern_crawl_half_credit: bool
            periodic_resources: _containers.RepeatedCompositeFieldContainer[CDOTAMatchMetadata.Team.PeriodicResourceData]
            extra_event_messages: _containers.RepeatedCompositeFieldContainer[_gcsdk_gcmessages_pb2.CExtraMsgBlock]
            def __init__(self, event_id: _Optional[int] = ..., event_points: _Optional[int] = ..., challenge_instance_id: _Optional[int] = ..., challenge_quest_id: _Optional[int] = ..., challenge_quest_challenge_id: _Optional[int] = ..., challenge_completed: bool = ..., challenge_rank_completed: _Optional[int] = ..., challenge_rank_previously_completed: _Optional[int] = ..., event_owned: bool = ..., sub_challenges_with_progress: _Optional[_Iterable[_Union[CDOTAMatchMetadata.Team.SubChallenge, _Mapping]]] = ..., wager_winnings: _Optional[int] = ..., cavern_challenge_active: bool = ..., cavern_challenge_winnings: _Optional[int] = ..., amount_wagered: _Optional[int] = ..., periodic_point_adjustments: _Optional[int] = ..., cavern_challenge_map_results: _Optional[_Iterable[_Union[CDOTAMatchMetadata.Team.CavernChallengeResult, _Mapping]]] = ..., cavern_challenge_plus_shard_winnings: _Optional[int] = ..., actions_granted: _Optional[_Iterable[_Union[CDOTAMatchMetadata.Team.ActionGrant, _Mapping]]] = ..., cavern_crawl_map_variant: _Optional[int] = ..., team_wager_bonus_pct: _Optional[int] = ..., wager_streak_pct: _Optional[int] = ..., candy_points_granted: _Optional[_Iterable[_Union[CDOTAMatchMetadata.Team.CandyGrant, _Mapping]]] = ..., active_season_id: _Optional[int] = ..., cavern_crawl_half_credit: bool = ..., periodic_resources: _Optional[_Iterable[_Union[CDOTAMatchMetadata.Team.PeriodicResourceData, _Mapping]]] = ..., extra_event_messages: _Optional[_Iterable[_Union[_gcsdk_gcmessages_pb2.CExtraMsgBlock, _Mapping]]] = ...) -> None: ...
        class FeaturedGamemodeProgress(_message.Message):
            __slots__ = ("start_value", "end_value", "max_value")
            START_VALUE_FIELD_NUMBER: _ClassVar[int]
            END_VALUE_FIELD_NUMBER: _ClassVar[int]
            MAX_VALUE_FIELD_NUMBER: _ClassVar[int]
            start_value: int
            end_value: int
            max_value: int
            def __init__(self, start_value: _Optional[int] = ..., end_value: _Optional[int] = ..., max_value: _Optional[int] = ...) -> None: ...
        class KillInfo(_message.Message):
            __slots__ = ("kill_type", "victim_player_slot", "killer_player_slot", "time", "bounty")
            class KillType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                KILL_TYPE_PLAYER: _ClassVar[CDOTAMatchMetadata.Team.KillInfo.KillType]
                KILL_TYPE_TOWER: _ClassVar[CDOTAMatchMetadata.Team.KillInfo.KillType]
                KILL_TYPE_BARRACKS: _ClassVar[CDOTAMatchMetadata.Team.KillInfo.KillType]
                KILL_TYPE_ROSHAN: _ClassVar[CDOTAMatchMetadata.Team.KillInfo.KillType]
                KILL_TYPE_MINIBOSS: _ClassVar[CDOTAMatchMetadata.Team.KillInfo.KillType]
            KILL_TYPE_PLAYER: CDOTAMatchMetadata.Team.KillInfo.KillType
            KILL_TYPE_TOWER: CDOTAMatchMetadata.Team.KillInfo.KillType
            KILL_TYPE_BARRACKS: CDOTAMatchMetadata.Team.KillInfo.KillType
            KILL_TYPE_ROSHAN: CDOTAMatchMetadata.Team.KillInfo.KillType
            KILL_TYPE_MINIBOSS: CDOTAMatchMetadata.Team.KillInfo.KillType
            KILL_TYPE_FIELD_NUMBER: _ClassVar[int]
            VICTIM_PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
            KILLER_PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
            TIME_FIELD_NUMBER: _ClassVar[int]
            BOUNTY_FIELD_NUMBER: _ClassVar[int]
            kill_type: CDOTAMatchMetadata.Team.KillInfo.KillType
            victim_player_slot: int
            killer_player_slot: _containers.RepeatedScalarFieldContainer[int]
            time: int
            bounty: int
            def __init__(self, kill_type: _Optional[_Union[CDOTAMatchMetadata.Team.KillInfo.KillType, str]] = ..., victim_player_slot: _Optional[int] = ..., killer_player_slot: _Optional[_Iterable[int]] = ..., time: _Optional[int] = ..., bounty: _Optional[int] = ...) -> None: ...
        class Player(_message.Message):
            __slots__ = ("ability_upgrades", "player_slot", "kills", "items", "avg_kills_x16", "avg_deaths_x16", "avg_assists_x16", "avg_gpm_x16", "avg_xpm_x16", "best_kills_x16", "best_assists_x16", "best_gpm_x16", "best_xpm_x16", "win_streak", "best_win_streak", "fight_score", "farm_score", "support_score", "push_score", "level_up_times", "graph_net_worth", "inventory_snapshot", "avg_stats_calibrated", "auto_style_criteria", "event_data", "strange_gem_progress", "hero_xp", "camps_stacked", "victory_prediction", "lane_selection_flags", "rampages", "triple_kills", "aegis_snatched", "rapiers_purchased", "couriers_killed", "net_worth_rank", "support_gold_spent", "observer_wards_placed", "sentry_wards_placed", "wards_dewarded", "stun_duration", "rank_mmr_boost_type", "contract_progress", "guild_ids", "graph_hero_damage", "team_number", "team_slot", "featured_gamemode_progress", "featured_hero_sticker_index", "featured_hero_sticker_quality", "equipped_econ_items", "game_player_id", "player_tracked_stats", "overworld_rewards", "craftworks_quest_rewards", "ad_facet_hero_id", "monster_hunter_rewards")
            class ContractProgress(_message.Message):
                __slots__ = ("guild_id", "event_id", "challenge_instance_id", "challenge_parameter", "contract_stars", "contract_slot", "completed")
                GUILD_ID_FIELD_NUMBER: _ClassVar[int]
                EVENT_ID_FIELD_NUMBER: _ClassVar[int]
                CHALLENGE_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
                CHALLENGE_PARAMETER_FIELD_NUMBER: _ClassVar[int]
                CONTRACT_STARS_FIELD_NUMBER: _ClassVar[int]
                CONTRACT_SLOT_FIELD_NUMBER: _ClassVar[int]
                COMPLETED_FIELD_NUMBER: _ClassVar[int]
                guild_id: int
                event_id: int
                challenge_instance_id: int
                challenge_parameter: int
                contract_stars: int
                contract_slot: int
                completed: bool
                def __init__(self, guild_id: _Optional[int] = ..., event_id: _Optional[int] = ..., challenge_instance_id: _Optional[int] = ..., challenge_parameter: _Optional[int] = ..., contract_stars: _Optional[int] = ..., contract_slot: _Optional[int] = ..., completed: bool = ...) -> None: ...
            class OverworldRewards(_message.Message):
                __slots__ = ("overworld_id", "tokens")
                OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
                TOKENS_FIELD_NUMBER: _ClassVar[int]
                overworld_id: int
                tokens: _dota_gcmessages_common_overworld_pb2.CMsgOverworldTokenQuantity
                def __init__(self, overworld_id: _Optional[int] = ..., tokens: _Optional[_Union[_dota_gcmessages_common_overworld_pb2.CMsgOverworldTokenQuantity, _Mapping]] = ...) -> None: ...
            ABILITY_UPGRADES_FIELD_NUMBER: _ClassVar[int]
            PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
            KILLS_FIELD_NUMBER: _ClassVar[int]
            ITEMS_FIELD_NUMBER: _ClassVar[int]
            AVG_KILLS_X16_FIELD_NUMBER: _ClassVar[int]
            AVG_DEATHS_X16_FIELD_NUMBER: _ClassVar[int]
            AVG_ASSISTS_X16_FIELD_NUMBER: _ClassVar[int]
            AVG_GPM_X16_FIELD_NUMBER: _ClassVar[int]
            AVG_XPM_X16_FIELD_NUMBER: _ClassVar[int]
            BEST_KILLS_X16_FIELD_NUMBER: _ClassVar[int]
            BEST_ASSISTS_X16_FIELD_NUMBER: _ClassVar[int]
            BEST_GPM_X16_FIELD_NUMBER: _ClassVar[int]
            BEST_XPM_X16_FIELD_NUMBER: _ClassVar[int]
            WIN_STREAK_FIELD_NUMBER: _ClassVar[int]
            BEST_WIN_STREAK_FIELD_NUMBER: _ClassVar[int]
            FIGHT_SCORE_FIELD_NUMBER: _ClassVar[int]
            FARM_SCORE_FIELD_NUMBER: _ClassVar[int]
            SUPPORT_SCORE_FIELD_NUMBER: _ClassVar[int]
            PUSH_SCORE_FIELD_NUMBER: _ClassVar[int]
            LEVEL_UP_TIMES_FIELD_NUMBER: _ClassVar[int]
            GRAPH_NET_WORTH_FIELD_NUMBER: _ClassVar[int]
            INVENTORY_SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
            AVG_STATS_CALIBRATED_FIELD_NUMBER: _ClassVar[int]
            AUTO_STYLE_CRITERIA_FIELD_NUMBER: _ClassVar[int]
            EVENT_DATA_FIELD_NUMBER: _ClassVar[int]
            STRANGE_GEM_PROGRESS_FIELD_NUMBER: _ClassVar[int]
            HERO_XP_FIELD_NUMBER: _ClassVar[int]
            CAMPS_STACKED_FIELD_NUMBER: _ClassVar[int]
            VICTORY_PREDICTION_FIELD_NUMBER: _ClassVar[int]
            LANE_SELECTION_FLAGS_FIELD_NUMBER: _ClassVar[int]
            RAMPAGES_FIELD_NUMBER: _ClassVar[int]
            TRIPLE_KILLS_FIELD_NUMBER: _ClassVar[int]
            AEGIS_SNATCHED_FIELD_NUMBER: _ClassVar[int]
            RAPIERS_PURCHASED_FIELD_NUMBER: _ClassVar[int]
            COURIERS_KILLED_FIELD_NUMBER: _ClassVar[int]
            NET_WORTH_RANK_FIELD_NUMBER: _ClassVar[int]
            SUPPORT_GOLD_SPENT_FIELD_NUMBER: _ClassVar[int]
            OBSERVER_WARDS_PLACED_FIELD_NUMBER: _ClassVar[int]
            SENTRY_WARDS_PLACED_FIELD_NUMBER: _ClassVar[int]
            WARDS_DEWARDED_FIELD_NUMBER: _ClassVar[int]
            STUN_DURATION_FIELD_NUMBER: _ClassVar[int]
            RANK_MMR_BOOST_TYPE_FIELD_NUMBER: _ClassVar[int]
            CONTRACT_PROGRESS_FIELD_NUMBER: _ClassVar[int]
            GUILD_IDS_FIELD_NUMBER: _ClassVar[int]
            GRAPH_HERO_DAMAGE_FIELD_NUMBER: _ClassVar[int]
            TEAM_NUMBER_FIELD_NUMBER: _ClassVar[int]
            TEAM_SLOT_FIELD_NUMBER: _ClassVar[int]
            FEATURED_GAMEMODE_PROGRESS_FIELD_NUMBER: _ClassVar[int]
            FEATURED_HERO_STICKER_INDEX_FIELD_NUMBER: _ClassVar[int]
            FEATURED_HERO_STICKER_QUALITY_FIELD_NUMBER: _ClassVar[int]
            EQUIPPED_ECON_ITEMS_FIELD_NUMBER: _ClassVar[int]
            GAME_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
            PLAYER_TRACKED_STATS_FIELD_NUMBER: _ClassVar[int]
            OVERWORLD_REWARDS_FIELD_NUMBER: _ClassVar[int]
            CRAFTWORKS_QUEST_REWARDS_FIELD_NUMBER: _ClassVar[int]
            AD_FACET_HERO_ID_FIELD_NUMBER: _ClassVar[int]
            MONSTER_HUNTER_REWARDS_FIELD_NUMBER: _ClassVar[int]
            ability_upgrades: _containers.RepeatedScalarFieldContainer[int]
            player_slot: int
            kills: _containers.RepeatedCompositeFieldContainer[CDOTAMatchMetadata.Team.PlayerKill]
            items: _containers.RepeatedCompositeFieldContainer[CDOTAMatchMetadata.Team.ItemPurchase]
            avg_kills_x16: int
            avg_deaths_x16: int
            avg_assists_x16: int
            avg_gpm_x16: int
            avg_xpm_x16: int
            best_kills_x16: int
            best_assists_x16: int
            best_gpm_x16: int
            best_xpm_x16: int
            win_streak: int
            best_win_streak: int
            fight_score: float
            farm_score: float
            support_score: float
            push_score: float
            level_up_times: _containers.RepeatedScalarFieldContainer[int]
            graph_net_worth: _containers.RepeatedScalarFieldContainer[float]
            inventory_snapshot: _containers.RepeatedCompositeFieldContainer[CDOTAMatchMetadata.Team.InventorySnapshot]
            avg_stats_calibrated: bool
            auto_style_criteria: _containers.RepeatedCompositeFieldContainer[CDOTAMatchMetadata.Team.AutoStyleCriteria]
            event_data: _containers.RepeatedCompositeFieldContainer[CDOTAMatchMetadata.Team.EventData]
            strange_gem_progress: _containers.RepeatedCompositeFieldContainer[CDOTAMatchMetadata.Team.StrangeGemProgress]
            hero_xp: int
            camps_stacked: int
            victory_prediction: _containers.RepeatedCompositeFieldContainer[CDOTAMatchMetadata.Team.VictoryPrediction]
            lane_selection_flags: int
            rampages: int
            triple_kills: int
            aegis_snatched: int
            rapiers_purchased: int
            couriers_killed: int
            net_worth_rank: int
            support_gold_spent: int
            observer_wards_placed: int
            sentry_wards_placed: int
            wards_dewarded: int
            stun_duration: float
            rank_mmr_boost_type: _dota_shared_enums_pb2.EDOTAMMRBoostType
            contract_progress: _containers.RepeatedCompositeFieldContainer[CDOTAMatchMetadata.Team.Player.ContractProgress]
            guild_ids: _containers.RepeatedScalarFieldContainer[int]
            graph_hero_damage: _containers.RepeatedScalarFieldContainer[float]
            team_number: _dota_shared_enums_pb2.DOTA_GC_TEAM
            team_slot: int
            featured_gamemode_progress: CDOTAMatchMetadata.Team.FeaturedGamemodeProgress
            featured_hero_sticker_index: int
            featured_hero_sticker_quality: int
            equipped_econ_items: _containers.RepeatedCompositeFieldContainer[CDOTAMatchMetadata.EconItem]
            game_player_id: int
            player_tracked_stats: _containers.RepeatedCompositeFieldContainer[_dota_gcmessages_common_pb2.CMsgTrackedStat]
            overworld_rewards: CDOTAMatchMetadata.Team.Player.OverworldRewards
            craftworks_quest_rewards: _containers.RepeatedCompositeFieldContainer[_dota_gcmessages_common_craftworks_pb2.CMsgCraftworksQuestReward]
            ad_facet_hero_id: int
            monster_hunter_rewards: _dota_gcmessages_common_monster_hunter_pb2.CMsgMonsterHunterMatchRewards.Player
            def __init__(self, ability_upgrades: _Optional[_Iterable[int]] = ..., player_slot: _Optional[int] = ..., kills: _Optional[_Iterable[_Union[CDOTAMatchMetadata.Team.PlayerKill, _Mapping]]] = ..., items: _Optional[_Iterable[_Union[CDOTAMatchMetadata.Team.ItemPurchase, _Mapping]]] = ..., avg_kills_x16: _Optional[int] = ..., avg_deaths_x16: _Optional[int] = ..., avg_assists_x16: _Optional[int] = ..., avg_gpm_x16: _Optional[int] = ..., avg_xpm_x16: _Optional[int] = ..., best_kills_x16: _Optional[int] = ..., best_assists_x16: _Optional[int] = ..., best_gpm_x16: _Optional[int] = ..., best_xpm_x16: _Optional[int] = ..., win_streak: _Optional[int] = ..., best_win_streak: _Optional[int] = ..., fight_score: _Optional[float] = ..., farm_score: _Optional[float] = ..., support_score: _Optional[float] = ..., push_score: _Optional[float] = ..., level_up_times: _Optional[_Iterable[int]] = ..., graph_net_worth: _Optional[_Iterable[float]] = ..., inventory_snapshot: _Optional[_Iterable[_Union[CDOTAMatchMetadata.Team.InventorySnapshot, _Mapping]]] = ..., avg_stats_calibrated: bool = ..., auto_style_criteria: _Optional[_Iterable[_Union[CDOTAMatchMetadata.Team.AutoStyleCriteria, _Mapping]]] = ..., event_data: _Optional[_Iterable[_Union[CDOTAMatchMetadata.Team.EventData, _Mapping]]] = ..., strange_gem_progress: _Optional[_Iterable[_Union[CDOTAMatchMetadata.Team.StrangeGemProgress, _Mapping]]] = ..., hero_xp: _Optional[int] = ..., camps_stacked: _Optional[int] = ..., victory_prediction: _Optional[_Iterable[_Union[CDOTAMatchMetadata.Team.VictoryPrediction, _Mapping]]] = ..., lane_selection_flags: _Optional[int] = ..., rampages: _Optional[int] = ..., triple_kills: _Optional[int] = ..., aegis_snatched: _Optional[int] = ..., rapiers_purchased: _Optional[int] = ..., couriers_killed: _Optional[int] = ..., net_worth_rank: _Optional[int] = ..., support_gold_spent: _Optional[int] = ..., observer_wards_placed: _Optional[int] = ..., sentry_wards_placed: _Optional[int] = ..., wards_dewarded: _Optional[int] = ..., stun_duration: _Optional[float] = ..., rank_mmr_boost_type: _Optional[_Union[_dota_shared_enums_pb2.EDOTAMMRBoostType, str]] = ..., contract_progress: _Optional[_Iterable[_Union[CDOTAMatchMetadata.Team.Player.ContractProgress, _Mapping]]] = ..., guild_ids: _Optional[_Iterable[int]] = ..., graph_hero_damage: _Optional[_Iterable[float]] = ..., team_number: _Optional[_Union[_dota_shared_enums_pb2.DOTA_GC_TEAM, str]] = ..., team_slot: _Optional[int] = ..., featured_gamemode_progress: _Optional[_Union[CDOTAMatchMetadata.Team.FeaturedGamemodeProgress, _Mapping]] = ..., featured_hero_sticker_index: _Optional[int] = ..., featured_hero_sticker_quality: _Optional[int] = ..., equipped_econ_items: _Optional[_Iterable[_Union[CDOTAMatchMetadata.EconItem, _Mapping]]] = ..., game_player_id: _Optional[int] = ..., player_tracked_stats: _Optional[_Iterable[_Union[_dota_gcmessages_common_pb2.CMsgTrackedStat, _Mapping]]] = ..., overworld_rewards: _Optional[_Union[CDOTAMatchMetadata.Team.Player.OverworldRewards, _Mapping]] = ..., craftworks_quest_rewards: _Optional[_Iterable[_Union[_dota_gcmessages_common_craftworks_pb2.CMsgCraftworksQuestReward, _Mapping]]] = ..., ad_facet_hero_id: _Optional[int] = ..., monster_hunter_rewards: _Optional[_Union[_dota_gcmessages_common_monster_hunter_pb2.CMsgMonsterHunterMatchRewards.Player, _Mapping]] = ...) -> None: ...
        DOTA_TEAM_FIELD_NUMBER: _ClassVar[int]
        PLAYERS_FIELD_NUMBER: _ClassVar[int]
        GRAPH_EXPERIENCE_FIELD_NUMBER: _ClassVar[int]
        GRAPH_GOLD_EARNED_FIELD_NUMBER: _ClassVar[int]
        GRAPH_NET_WORTH_FIELD_NUMBER: _ClassVar[int]
        CM_FIRST_PICK_FIELD_NUMBER: _ClassVar[int]
        CM_CAPTAIN_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
        CM_PENALTY_FIELD_NUMBER: _ClassVar[int]
        TEAM_TRACKED_STATS_FIELD_NUMBER: _ClassVar[int]
        KILLS_FIELD_NUMBER: _ClassVar[int]
        dota_team: int
        players: _containers.RepeatedCompositeFieldContainer[CDOTAMatchMetadata.Team.Player]
        graph_experience: _containers.RepeatedScalarFieldContainer[float]
        graph_gold_earned: _containers.RepeatedScalarFieldContainer[float]
        graph_net_worth: _containers.RepeatedScalarFieldContainer[float]
        cm_first_pick: bool
        cm_captain_player_id: int
        cm_penalty: int
        team_tracked_stats: _containers.RepeatedCompositeFieldContainer[_dota_gcmessages_common_pb2.CMsgTrackedStat]
        kills: _containers.RepeatedCompositeFieldContainer[CDOTAMatchMetadata.Team.KillInfo]
        def __init__(self, dota_team: _Optional[int] = ..., players: _Optional[_Iterable[_Union[CDOTAMatchMetadata.Team.Player, _Mapping]]] = ..., graph_experience: _Optional[_Iterable[float]] = ..., graph_gold_earned: _Optional[_Iterable[float]] = ..., graph_net_worth: _Optional[_Iterable[float]] = ..., cm_first_pick: bool = ..., cm_captain_player_id: _Optional[int] = ..., cm_penalty: _Optional[int] = ..., team_tracked_stats: _Optional[_Iterable[_Union[_dota_gcmessages_common_pb2.CMsgTrackedStat, _Mapping]]] = ..., kills: _Optional[_Iterable[_Union[CDOTAMatchMetadata.Team.KillInfo, _Mapping]]] = ...) -> None: ...
    class GuildChallengeProgress(_message.Message):
        __slots__ = ("guild_id", "event_id", "challenge_instance_id", "challenge_parameter", "challenge_timestamp", "challenge_progress_at_start", "challenge_progress_accumulated", "individual_progress")
        class IndividualProgress(_message.Message):
            __slots__ = ("progress", "player_slot")
            PROGRESS_FIELD_NUMBER: _ClassVar[int]
            PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
            progress: int
            player_slot: int
            def __init__(self, progress: _Optional[int] = ..., player_slot: _Optional[int] = ...) -> None: ...
        GUILD_ID_FIELD_NUMBER: _ClassVar[int]
        EVENT_ID_FIELD_NUMBER: _ClassVar[int]
        CHALLENGE_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
        CHALLENGE_PARAMETER_FIELD_NUMBER: _ClassVar[int]
        CHALLENGE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        CHALLENGE_PROGRESS_AT_START_FIELD_NUMBER: _ClassVar[int]
        CHALLENGE_PROGRESS_ACCUMULATED_FIELD_NUMBER: _ClassVar[int]
        INDIVIDUAL_PROGRESS_FIELD_NUMBER: _ClassVar[int]
        guild_id: int
        event_id: _dota_shared_enums_pb2.EEvent
        challenge_instance_id: int
        challenge_parameter: int
        challenge_timestamp: int
        challenge_progress_at_start: int
        challenge_progress_accumulated: int
        individual_progress: _containers.RepeatedCompositeFieldContainer[CDOTAMatchMetadata.GuildChallengeProgress.IndividualProgress]
        def __init__(self, guild_id: _Optional[int] = ..., event_id: _Optional[_Union[_dota_shared_enums_pb2.EEvent, str]] = ..., challenge_instance_id: _Optional[int] = ..., challenge_parameter: _Optional[int] = ..., challenge_timestamp: _Optional[int] = ..., challenge_progress_at_start: _Optional[int] = ..., challenge_progress_accumulated: _Optional[int] = ..., individual_progress: _Optional[_Iterable[_Union[CDOTAMatchMetadata.GuildChallengeProgress.IndividualProgress, _Mapping]]] = ...) -> None: ...
    class Tip(_message.Message):
        __slots__ = ("source_player_slot", "target_player_slot", "tip_amount", "event_id")
        SOURCE_PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
        TARGET_PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
        TIP_AMOUNT_FIELD_NUMBER: _ClassVar[int]
        EVENT_ID_FIELD_NUMBER: _ClassVar[int]
        source_player_slot: int
        target_player_slot: int
        tip_amount: int
        event_id: _dota_shared_enums_pb2.EEvent
        def __init__(self, source_player_slot: _Optional[int] = ..., target_player_slot: _Optional[int] = ..., tip_amount: _Optional[int] = ..., event_id: _Optional[_Union[_dota_shared_enums_pb2.EEvent, str]] = ...) -> None: ...
    TEAMS_FIELD_NUMBER: _ClassVar[int]
    LOBBY_ID_FIELD_NUMBER: _ClassVar[int]
    REPORT_UNTIL_TIME_FIELD_NUMBER: _ClassVar[int]
    EVENT_GAME_CUSTOM_TABLE_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    MATCHMAKING_STATS_FIELD_NUMBER: _ClassVar[int]
    MVP_DATA_FIELD_NUMBER: _ClassVar[int]
    GUILD_CHALLENGE_PROGRESS_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_POST_GAME_TABLE_FIELD_NUMBER: _ClassVar[int]
    MATCH_TIPS_FIELD_NUMBER: _ClassVar[int]
    MATCH_TRACKED_STATS_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_EVENT_ID_FOR_DISPLAY_FIELD_NUMBER: _ClassVar[int]
    teams: _containers.RepeatedCompositeFieldContainer[CDOTAMatchMetadata.Team]
    lobby_id: int
    report_until_time: int
    event_game_custom_table: bytes
    primary_event_id: int
    matchmaking_stats: _dota_gcmessages_common_match_management_pb2.CMsgMatchMatchmakingStats
    mvp_data: _dota_gcmessages_common_match_management_pb2.CMvpData
    guild_challenge_progress: _containers.RepeatedCompositeFieldContainer[CDOTAMatchMetadata.GuildChallengeProgress]
    custom_post_game_table: bytes
    match_tips: _containers.RepeatedCompositeFieldContainer[CDOTAMatchMetadata.Tip]
    match_tracked_stats: _containers.RepeatedCompositeFieldContainer[_dota_gcmessages_common_pb2.CMsgTrackedStat]
    primary_event_id_for_display: int
    def __init__(self, teams: _Optional[_Iterable[_Union[CDOTAMatchMetadata.Team, _Mapping]]] = ..., lobby_id: _Optional[int] = ..., report_until_time: _Optional[int] = ..., event_game_custom_table: _Optional[bytes] = ..., primary_event_id: _Optional[int] = ..., matchmaking_stats: _Optional[_Union[_dota_gcmessages_common_match_management_pb2.CMsgMatchMatchmakingStats, _Mapping]] = ..., mvp_data: _Optional[_Union[_dota_gcmessages_common_match_management_pb2.CMvpData, _Mapping]] = ..., guild_challenge_progress: _Optional[_Iterable[_Union[CDOTAMatchMetadata.GuildChallengeProgress, _Mapping]]] = ..., custom_post_game_table: _Optional[bytes] = ..., match_tips: _Optional[_Iterable[_Union[CDOTAMatchMetadata.Tip, _Mapping]]] = ..., match_tracked_stats: _Optional[_Iterable[_Union[_dota_gcmessages_common_pb2.CMsgTrackedStat, _Mapping]]] = ..., primary_event_id_for_display: _Optional[int] = ...) -> None: ...

class CDOTAMatchPrivateMetadata(_message.Message):
    __slots__ = ("teams", "graph_win_probability", "string_names", "contributions")
    class StringName(_message.Message):
        __slots__ = ("id", "name")
        ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        id: int
        name: str
        def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ...) -> None: ...
    class Team(_message.Message):
        __slots__ = ("dota_team", "players", "buildings")
        class Player(_message.Message):
            __slots__ = ("player_slot", "position_stream", "combat_segments", "damage_unit_names", "buff_records", "graph_kills", "graph_deaths", "graph_assists", "graph_lasthits", "graph_denies", "gold_received", "xp_received", "team_number", "team_slot")
            class CombatSegment(_message.Message):
                __slots__ = ("game_time", "damage_by_ability", "healing_by_ability")
                class DamageByAbility(_message.Message):
                    __slots__ = ("source_unit_index", "ability_id", "by_hero_targets")
                    class ByHeroTarget(_message.Message):
                        __slots__ = ("hero_id", "damage")
                        HERO_ID_FIELD_NUMBER: _ClassVar[int]
                        DAMAGE_FIELD_NUMBER: _ClassVar[int]
                        hero_id: int
                        damage: int
                        def __init__(self, hero_id: _Optional[int] = ..., damage: _Optional[int] = ...) -> None: ...
                    SOURCE_UNIT_INDEX_FIELD_NUMBER: _ClassVar[int]
                    ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
                    BY_HERO_TARGETS_FIELD_NUMBER: _ClassVar[int]
                    source_unit_index: int
                    ability_id: int
                    by_hero_targets: _containers.RepeatedCompositeFieldContainer[CDOTAMatchPrivateMetadata.Team.Player.CombatSegment.DamageByAbility.ByHeroTarget]
                    def __init__(self, source_unit_index: _Optional[int] = ..., ability_id: _Optional[int] = ..., by_hero_targets: _Optional[_Iterable[_Union[CDOTAMatchPrivateMetadata.Team.Player.CombatSegment.DamageByAbility.ByHeroTarget, _Mapping]]] = ...) -> None: ...
                class HealingByAbility(_message.Message):
                    __slots__ = ("source_unit_index", "ability_id", "by_hero_targets")
                    class ByHeroTarget(_message.Message):
                        __slots__ = ("hero_id", "healing")
                        HERO_ID_FIELD_NUMBER: _ClassVar[int]
                        HEALING_FIELD_NUMBER: _ClassVar[int]
                        hero_id: int
                        healing: int
                        def __init__(self, hero_id: _Optional[int] = ..., healing: _Optional[int] = ...) -> None: ...
                    SOURCE_UNIT_INDEX_FIELD_NUMBER: _ClassVar[int]
                    ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
                    BY_HERO_TARGETS_FIELD_NUMBER: _ClassVar[int]
                    source_unit_index: int
                    ability_id: int
                    by_hero_targets: _containers.RepeatedCompositeFieldContainer[CDOTAMatchPrivateMetadata.Team.Player.CombatSegment.HealingByAbility.ByHeroTarget]
                    def __init__(self, source_unit_index: _Optional[int] = ..., ability_id: _Optional[int] = ..., by_hero_targets: _Optional[_Iterable[_Union[CDOTAMatchPrivateMetadata.Team.Player.CombatSegment.HealingByAbility.ByHeroTarget, _Mapping]]] = ...) -> None: ...
                GAME_TIME_FIELD_NUMBER: _ClassVar[int]
                DAMAGE_BY_ABILITY_FIELD_NUMBER: _ClassVar[int]
                HEALING_BY_ABILITY_FIELD_NUMBER: _ClassVar[int]
                game_time: int
                damage_by_ability: _containers.RepeatedCompositeFieldContainer[CDOTAMatchPrivateMetadata.Team.Player.CombatSegment.DamageByAbility]
                healing_by_ability: _containers.RepeatedCompositeFieldContainer[CDOTAMatchPrivateMetadata.Team.Player.CombatSegment.HealingByAbility]
                def __init__(self, game_time: _Optional[int] = ..., damage_by_ability: _Optional[_Iterable[_Union[CDOTAMatchPrivateMetadata.Team.Player.CombatSegment.DamageByAbility, _Mapping]]] = ..., healing_by_ability: _Optional[_Iterable[_Union[CDOTAMatchPrivateMetadata.Team.Player.CombatSegment.HealingByAbility, _Mapping]]] = ...) -> None: ...
            class BuffRecord(_message.Message):
                __slots__ = ("buff_ability_id", "buff_modifier_name", "by_hero_targets")
                class ByHeroTarget(_message.Message):
                    __slots__ = ("hero_id", "elapsed_duration", "is_hidden", "instance_count")
                    HERO_ID_FIELD_NUMBER: _ClassVar[int]
                    ELAPSED_DURATION_FIELD_NUMBER: _ClassVar[int]
                    IS_HIDDEN_FIELD_NUMBER: _ClassVar[int]
                    INSTANCE_COUNT_FIELD_NUMBER: _ClassVar[int]
                    hero_id: int
                    elapsed_duration: float
                    is_hidden: bool
                    instance_count: int
                    def __init__(self, hero_id: _Optional[int] = ..., elapsed_duration: _Optional[float] = ..., is_hidden: bool = ..., instance_count: _Optional[int] = ...) -> None: ...
                BUFF_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
                BUFF_MODIFIER_NAME_FIELD_NUMBER: _ClassVar[int]
                BY_HERO_TARGETS_FIELD_NUMBER: _ClassVar[int]
                buff_ability_id: int
                buff_modifier_name: str
                by_hero_targets: _containers.RepeatedCompositeFieldContainer[CDOTAMatchPrivateMetadata.Team.Player.BuffRecord.ByHeroTarget]
                def __init__(self, buff_ability_id: _Optional[int] = ..., buff_modifier_name: _Optional[str] = ..., by_hero_targets: _Optional[_Iterable[_Union[CDOTAMatchPrivateMetadata.Team.Player.BuffRecord.ByHeroTarget, _Mapping]]] = ...) -> None: ...
            class GoldReceived(_message.Message):
                __slots__ = ("creep", "heroes", "bounty_runes", "passive", "buildings", "abilities", "wards", "other")
                CREEP_FIELD_NUMBER: _ClassVar[int]
                HEROES_FIELD_NUMBER: _ClassVar[int]
                BOUNTY_RUNES_FIELD_NUMBER: _ClassVar[int]
                PASSIVE_FIELD_NUMBER: _ClassVar[int]
                BUILDINGS_FIELD_NUMBER: _ClassVar[int]
                ABILITIES_FIELD_NUMBER: _ClassVar[int]
                WARDS_FIELD_NUMBER: _ClassVar[int]
                OTHER_FIELD_NUMBER: _ClassVar[int]
                creep: int
                heroes: int
                bounty_runes: int
                passive: int
                buildings: int
                abilities: int
                wards: int
                other: int
                def __init__(self, creep: _Optional[int] = ..., heroes: _Optional[int] = ..., bounty_runes: _Optional[int] = ..., passive: _Optional[int] = ..., buildings: _Optional[int] = ..., abilities: _Optional[int] = ..., wards: _Optional[int] = ..., other: _Optional[int] = ...) -> None: ...
            class XPReceived(_message.Message):
                __slots__ = ("creep", "heroes", "roshan", "tome_of_knowledge", "outpost", "other", "abilities")
                CREEP_FIELD_NUMBER: _ClassVar[int]
                HEROES_FIELD_NUMBER: _ClassVar[int]
                ROSHAN_FIELD_NUMBER: _ClassVar[int]
                TOME_OF_KNOWLEDGE_FIELD_NUMBER: _ClassVar[int]
                OUTPOST_FIELD_NUMBER: _ClassVar[int]
                OTHER_FIELD_NUMBER: _ClassVar[int]
                ABILITIES_FIELD_NUMBER: _ClassVar[int]
                creep: int
                heroes: int
                roshan: int
                tome_of_knowledge: int
                outpost: int
                other: int
                abilities: int
                def __init__(self, creep: _Optional[int] = ..., heroes: _Optional[int] = ..., roshan: _Optional[int] = ..., tome_of_knowledge: _Optional[int] = ..., outpost: _Optional[int] = ..., other: _Optional[int] = ..., abilities: _Optional[int] = ...) -> None: ...
            PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
            POSITION_STREAM_FIELD_NUMBER: _ClassVar[int]
            COMBAT_SEGMENTS_FIELD_NUMBER: _ClassVar[int]
            DAMAGE_UNIT_NAMES_FIELD_NUMBER: _ClassVar[int]
            BUFF_RECORDS_FIELD_NUMBER: _ClassVar[int]
            GRAPH_KILLS_FIELD_NUMBER: _ClassVar[int]
            GRAPH_DEATHS_FIELD_NUMBER: _ClassVar[int]
            GRAPH_ASSISTS_FIELD_NUMBER: _ClassVar[int]
            GRAPH_LASTHITS_FIELD_NUMBER: _ClassVar[int]
            GRAPH_DENIES_FIELD_NUMBER: _ClassVar[int]
            GOLD_RECEIVED_FIELD_NUMBER: _ClassVar[int]
            XP_RECEIVED_FIELD_NUMBER: _ClassVar[int]
            TEAM_NUMBER_FIELD_NUMBER: _ClassVar[int]
            TEAM_SLOT_FIELD_NUMBER: _ClassVar[int]
            player_slot: int
            position_stream: bytes
            combat_segments: _containers.RepeatedCompositeFieldContainer[CDOTAMatchPrivateMetadata.Team.Player.CombatSegment]
            damage_unit_names: _containers.RepeatedScalarFieldContainer[str]
            buff_records: _containers.RepeatedCompositeFieldContainer[CDOTAMatchPrivateMetadata.Team.Player.BuffRecord]
            graph_kills: _containers.RepeatedScalarFieldContainer[float]
            graph_deaths: _containers.RepeatedScalarFieldContainer[float]
            graph_assists: _containers.RepeatedScalarFieldContainer[float]
            graph_lasthits: _containers.RepeatedScalarFieldContainer[float]
            graph_denies: _containers.RepeatedScalarFieldContainer[float]
            gold_received: CDOTAMatchPrivateMetadata.Team.Player.GoldReceived
            xp_received: CDOTAMatchPrivateMetadata.Team.Player.XPReceived
            team_number: _dota_shared_enums_pb2.DOTA_GC_TEAM
            team_slot: int
            def __init__(self, player_slot: _Optional[int] = ..., position_stream: _Optional[bytes] = ..., combat_segments: _Optional[_Iterable[_Union[CDOTAMatchPrivateMetadata.Team.Player.CombatSegment, _Mapping]]] = ..., damage_unit_names: _Optional[_Iterable[str]] = ..., buff_records: _Optional[_Iterable[_Union[CDOTAMatchPrivateMetadata.Team.Player.BuffRecord, _Mapping]]] = ..., graph_kills: _Optional[_Iterable[float]] = ..., graph_deaths: _Optional[_Iterable[float]] = ..., graph_assists: _Optional[_Iterable[float]] = ..., graph_lasthits: _Optional[_Iterable[float]] = ..., graph_denies: _Optional[_Iterable[float]] = ..., gold_received: _Optional[_Union[CDOTAMatchPrivateMetadata.Team.Player.GoldReceived, _Mapping]] = ..., xp_received: _Optional[_Union[CDOTAMatchPrivateMetadata.Team.Player.XPReceived, _Mapping]] = ..., team_number: _Optional[_Union[_dota_shared_enums_pb2.DOTA_GC_TEAM, str]] = ..., team_slot: _Optional[int] = ...) -> None: ...
        class Building(_message.Message):
            __slots__ = ("unit_name", "position_quant_x", "position_quant_y", "death_time")
            UNIT_NAME_FIELD_NUMBER: _ClassVar[int]
            POSITION_QUANT_X_FIELD_NUMBER: _ClassVar[int]
            POSITION_QUANT_Y_FIELD_NUMBER: _ClassVar[int]
            DEATH_TIME_FIELD_NUMBER: _ClassVar[int]
            unit_name: str
            position_quant_x: int
            position_quant_y: int
            death_time: float
            def __init__(self, unit_name: _Optional[str] = ..., position_quant_x: _Optional[int] = ..., position_quant_y: _Optional[int] = ..., death_time: _Optional[float] = ...) -> None: ...
        DOTA_TEAM_FIELD_NUMBER: _ClassVar[int]
        PLAYERS_FIELD_NUMBER: _ClassVar[int]
        BUILDINGS_FIELD_NUMBER: _ClassVar[int]
        dota_team: int
        players: _containers.RepeatedCompositeFieldContainer[CDOTAMatchPrivateMetadata.Team.Player]
        buildings: _containers.RepeatedCompositeFieldContainer[CDOTAMatchPrivateMetadata.Team.Building]
        def __init__(self, dota_team: _Optional[int] = ..., players: _Optional[_Iterable[_Union[CDOTAMatchPrivateMetadata.Team.Player, _Mapping]]] = ..., buildings: _Optional[_Iterable[_Union[CDOTAMatchPrivateMetadata.Team.Building, _Mapping]]] = ...) -> None: ...
    class ContributionsCombatSegment(_message.Message):
        __slots__ = ("game_time", "damage_contributions", "damage_mitigations", "healing_contributions", "healing_reductions", "killing_blows", "dispels")
        class DamageContributionRecord(_message.Message):
            __slots__ = ("attacker_ability_id", "attacker_hero_id", "target_hero_id", "contributor_ability_id", "contributor_hero_id", "value", "type")
            ATTACKER_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
            ATTACKER_HERO_ID_FIELD_NUMBER: _ClassVar[int]
            TARGET_HERO_ID_FIELD_NUMBER: _ClassVar[int]
            CONTRIBUTOR_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
            CONTRIBUTOR_HERO_ID_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            TYPE_FIELD_NUMBER: _ClassVar[int]
            attacker_ability_id: int
            attacker_hero_id: int
            target_hero_id: int
            contributor_ability_id: int
            contributor_hero_id: int
            value: int
            type: int
            def __init__(self, attacker_ability_id: _Optional[int] = ..., attacker_hero_id: _Optional[int] = ..., target_hero_id: _Optional[int] = ..., contributor_ability_id: _Optional[int] = ..., contributor_hero_id: _Optional[int] = ..., value: _Optional[int] = ..., type: _Optional[int] = ...) -> None: ...
        class DamageMitigationRecord(_message.Message):
            __slots__ = ("attacker_ability_id", "attacker_hero_id", "target_hero_id", "contributor_ability_id", "contributor_hero_id", "value", "type")
            ATTACKER_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
            ATTACKER_HERO_ID_FIELD_NUMBER: _ClassVar[int]
            TARGET_HERO_ID_FIELD_NUMBER: _ClassVar[int]
            CONTRIBUTOR_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
            CONTRIBUTOR_HERO_ID_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            TYPE_FIELD_NUMBER: _ClassVar[int]
            attacker_ability_id: int
            attacker_hero_id: int
            target_hero_id: int
            contributor_ability_id: int
            contributor_hero_id: int
            value: int
            type: int
            def __init__(self, attacker_ability_id: _Optional[int] = ..., attacker_hero_id: _Optional[int] = ..., target_hero_id: _Optional[int] = ..., contributor_ability_id: _Optional[int] = ..., contributor_hero_id: _Optional[int] = ..., value: _Optional[int] = ..., type: _Optional[int] = ...) -> None: ...
        class HealingContributionRecord(_message.Message):
            __slots__ = ("attacker_ability_id", "attacker_hero_id", "target_hero_id", "contributor_ability_id", "contributor_hero_id", "value", "type")
            ATTACKER_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
            ATTACKER_HERO_ID_FIELD_NUMBER: _ClassVar[int]
            TARGET_HERO_ID_FIELD_NUMBER: _ClassVar[int]
            CONTRIBUTOR_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
            CONTRIBUTOR_HERO_ID_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            TYPE_FIELD_NUMBER: _ClassVar[int]
            attacker_ability_id: int
            attacker_hero_id: int
            target_hero_id: int
            contributor_ability_id: int
            contributor_hero_id: int
            value: int
            type: int
            def __init__(self, attacker_ability_id: _Optional[int] = ..., attacker_hero_id: _Optional[int] = ..., target_hero_id: _Optional[int] = ..., contributor_ability_id: _Optional[int] = ..., contributor_hero_id: _Optional[int] = ..., value: _Optional[int] = ..., type: _Optional[int] = ...) -> None: ...
        class HealingReductionRecord(_message.Message):
            __slots__ = ("attacker_ability_id", "attacker_hero_id", "target_hero_id", "contributor_ability_id", "contributor_hero_id", "value", "type")
            ATTACKER_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
            ATTACKER_HERO_ID_FIELD_NUMBER: _ClassVar[int]
            TARGET_HERO_ID_FIELD_NUMBER: _ClassVar[int]
            CONTRIBUTOR_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
            CONTRIBUTOR_HERO_ID_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            TYPE_FIELD_NUMBER: _ClassVar[int]
            attacker_ability_id: int
            attacker_hero_id: int
            target_hero_id: int
            contributor_ability_id: int
            contributor_hero_id: int
            value: int
            type: int
            def __init__(self, attacker_ability_id: _Optional[int] = ..., attacker_hero_id: _Optional[int] = ..., target_hero_id: _Optional[int] = ..., contributor_ability_id: _Optional[int] = ..., contributor_hero_id: _Optional[int] = ..., value: _Optional[int] = ..., type: _Optional[int] = ...) -> None: ...
        class KillingBlow(_message.Message):
            __slots__ = ("attacker_hero_id", "target_hero_id", "inflictor_ability_id")
            ATTACKER_HERO_ID_FIELD_NUMBER: _ClassVar[int]
            TARGET_HERO_ID_FIELD_NUMBER: _ClassVar[int]
            INFLICTOR_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
            attacker_hero_id: int
            target_hero_id: int
            inflictor_ability_id: int
            def __init__(self, attacker_hero_id: _Optional[int] = ..., target_hero_id: _Optional[int] = ..., inflictor_ability_id: _Optional[int] = ...) -> None: ...
        class Dispel(_message.Message):
            __slots__ = ("attacker_hero_id", "target_hero_id", "inflictor_ability_id", "modifier_ability_id", "duration_reduced")
            ATTACKER_HERO_ID_FIELD_NUMBER: _ClassVar[int]
            TARGET_HERO_ID_FIELD_NUMBER: _ClassVar[int]
            INFLICTOR_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
            MODIFIER_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
            DURATION_REDUCED_FIELD_NUMBER: _ClassVar[int]
            attacker_hero_id: int
            target_hero_id: int
            inflictor_ability_id: int
            modifier_ability_id: int
            duration_reduced: float
            def __init__(self, attacker_hero_id: _Optional[int] = ..., target_hero_id: _Optional[int] = ..., inflictor_ability_id: _Optional[int] = ..., modifier_ability_id: _Optional[int] = ..., duration_reduced: _Optional[float] = ...) -> None: ...
        GAME_TIME_FIELD_NUMBER: _ClassVar[int]
        DAMAGE_CONTRIBUTIONS_FIELD_NUMBER: _ClassVar[int]
        DAMAGE_MITIGATIONS_FIELD_NUMBER: _ClassVar[int]
        HEALING_CONTRIBUTIONS_FIELD_NUMBER: _ClassVar[int]
        HEALING_REDUCTIONS_FIELD_NUMBER: _ClassVar[int]
        KILLING_BLOWS_FIELD_NUMBER: _ClassVar[int]
        DISPELS_FIELD_NUMBER: _ClassVar[int]
        game_time: int
        damage_contributions: _containers.RepeatedCompositeFieldContainer[CDOTAMatchPrivateMetadata.ContributionsCombatSegment.DamageContributionRecord]
        damage_mitigations: _containers.RepeatedCompositeFieldContainer[CDOTAMatchPrivateMetadata.ContributionsCombatSegment.DamageMitigationRecord]
        healing_contributions: _containers.RepeatedCompositeFieldContainer[CDOTAMatchPrivateMetadata.ContributionsCombatSegment.HealingContributionRecord]
        healing_reductions: _containers.RepeatedCompositeFieldContainer[CDOTAMatchPrivateMetadata.ContributionsCombatSegment.HealingReductionRecord]
        killing_blows: _containers.RepeatedCompositeFieldContainer[CDOTAMatchPrivateMetadata.ContributionsCombatSegment.KillingBlow]
        dispels: _containers.RepeatedCompositeFieldContainer[CDOTAMatchPrivateMetadata.ContributionsCombatSegment.Dispel]
        def __init__(self, game_time: _Optional[int] = ..., damage_contributions: _Optional[_Iterable[_Union[CDOTAMatchPrivateMetadata.ContributionsCombatSegment.DamageContributionRecord, _Mapping]]] = ..., damage_mitigations: _Optional[_Iterable[_Union[CDOTAMatchPrivateMetadata.ContributionsCombatSegment.DamageMitigationRecord, _Mapping]]] = ..., healing_contributions: _Optional[_Iterable[_Union[CDOTAMatchPrivateMetadata.ContributionsCombatSegment.HealingContributionRecord, _Mapping]]] = ..., healing_reductions: _Optional[_Iterable[_Union[CDOTAMatchPrivateMetadata.ContributionsCombatSegment.HealingReductionRecord, _Mapping]]] = ..., killing_blows: _Optional[_Iterable[_Union[CDOTAMatchPrivateMetadata.ContributionsCombatSegment.KillingBlow, _Mapping]]] = ..., dispels: _Optional[_Iterable[_Union[CDOTAMatchPrivateMetadata.ContributionsCombatSegment.Dispel, _Mapping]]] = ...) -> None: ...
    TEAMS_FIELD_NUMBER: _ClassVar[int]
    GRAPH_WIN_PROBABILITY_FIELD_NUMBER: _ClassVar[int]
    STRING_NAMES_FIELD_NUMBER: _ClassVar[int]
    CONTRIBUTIONS_FIELD_NUMBER: _ClassVar[int]
    teams: _containers.RepeatedCompositeFieldContainer[CDOTAMatchPrivateMetadata.Team]
    graph_win_probability: _containers.RepeatedScalarFieldContainer[float]
    string_names: _containers.RepeatedCompositeFieldContainer[CDOTAMatchPrivateMetadata.StringName]
    contributions: _containers.RepeatedCompositeFieldContainer[CDOTAMatchPrivateMetadata.ContributionsCombatSegment]
    def __init__(self, teams: _Optional[_Iterable[_Union[CDOTAMatchPrivateMetadata.Team, _Mapping]]] = ..., graph_win_probability: _Optional[_Iterable[float]] = ..., string_names: _Optional[_Iterable[_Union[CDOTAMatchPrivateMetadata.StringName, _Mapping]]] = ..., contributions: _Optional[_Iterable[_Union[CDOTAMatchPrivateMetadata.ContributionsCombatSegment, _Mapping]]] = ...) -> None: ...
