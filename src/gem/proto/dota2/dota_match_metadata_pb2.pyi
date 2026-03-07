from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

import base_gcmessages_pb2 as _base_gcmessages_pb2
import dota_gcmessages_common_craftworks_pb2 as _dota_gcmessages_common_craftworks_pb2
import dota_gcmessages_common_match_management_pb2 as _dota_gcmessages_common_match_management_pb2
import dota_gcmessages_common_monster_hunter_pb2 as _dota_gcmessages_common_monster_hunter_pb2
import dota_gcmessages_common_overworld_pb2 as _dota_gcmessages_common_overworld_pb2
import dota_gcmessages_common_pb2 as _dota_gcmessages_common_pb2
import dota_shared_enums_pb2 as _dota_shared_enums_pb2
import gcsdk_gcmessages_pb2 as _gcsdk_gcmessages_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

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
    def __init__(
        self,
        version: int | None = ...,
        match_id: int | None = ...,
        metadata: CDOTAMatchMetadata | _Mapping | None = ...,
        private_metadata: bytes | None = ...,
    ) -> None: ...

class CDOTAMatchMetadata(_message.Message):
    __slots__ = (
        "teams",
        "lobby_id",
        "report_until_time",
        "event_game_custom_table",
        "primary_event_id",
        "matchmaking_stats",
        "mvp_data",
        "guild_challenge_progress",
        "custom_post_game_table",
        "match_tips",
        "match_tracked_stats",
        "primary_event_id_for_display",
    )
    class EconItem(_message.Message):
        __slots__ = ("def_index", "quality", "attribute", "style", "equipped_state")
        DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
        QUALITY_FIELD_NUMBER: _ClassVar[int]
        ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
        STYLE_FIELD_NUMBER: _ClassVar[int]
        EQUIPPED_STATE_FIELD_NUMBER: _ClassVar[int]
        def_index: int
        quality: int
        attribute: _containers.RepeatedCompositeFieldContainer[
            _base_gcmessages_pb2.CSOEconItemAttribute
        ]
        style: int
        equipped_state: _containers.RepeatedCompositeFieldContainer[
            _base_gcmessages_pb2.CSOEconItemEquipped
        ]
        def __init__(
            self,
            def_index: int | None = ...,
            quality: int | None = ...,
            attribute: _Iterable[_base_gcmessages_pb2.CSOEconItemAttribute | _Mapping] | None = ...,
            style: int | None = ...,
            equipped_state: _Iterable[_base_gcmessages_pb2.CSOEconItemEquipped | _Mapping]
            | None = ...,
        ) -> None: ...

    class Team(_message.Message):
        __slots__ = (
            "dota_team",
            "players",
            "graph_experience",
            "graph_gold_earned",
            "graph_net_worth",
            "cm_first_pick",
            "cm_captain_player_id",
            "cm_penalty",
            "team_tracked_stats",
            "kills",
        )
        class PlayerKill(_message.Message):
            __slots__ = ("victim_slot", "count")
            VICTIM_SLOT_FIELD_NUMBER: _ClassVar[int]
            COUNT_FIELD_NUMBER: _ClassVar[int]
            victim_slot: int
            count: int
            def __init__(self, victim_slot: int | None = ..., count: int | None = ...) -> None: ...

        class ItemPurchase(_message.Message):
            __slots__ = ("item_id", "purchase_time")
            ITEM_ID_FIELD_NUMBER: _ClassVar[int]
            PURCHASE_TIME_FIELD_NUMBER: _ClassVar[int]
            item_id: int
            purchase_time: int
            def __init__(
                self, item_id: int | None = ..., purchase_time: int | None = ...
            ) -> None: ...

        class InventorySnapshot(_message.Message):
            __slots__ = (
                "item_id",
                "game_time",
                "kills",
                "deaths",
                "assists",
                "level",
                "backpack_item_id",
                "neutral_item_id",
                "neutral_enhancement_id",
                "last_hits",
                "denies",
                "flags",
            )
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
            def __init__(
                self,
                item_id: _Iterable[int] | None = ...,
                game_time: int | None = ...,
                kills: int | None = ...,
                deaths: int | None = ...,
                assists: int | None = ...,
                level: int | None = ...,
                backpack_item_id: _Iterable[int] | None = ...,
                neutral_item_id: int | None = ...,
                neutral_enhancement_id: int | None = ...,
                last_hits: int | None = ...,
                denies: int | None = ...,
                flags: int | None = ...,
            ) -> None: ...

        class AutoStyleCriteria(_message.Message):
            __slots__ = ("name_token", "value")
            NAME_TOKEN_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            name_token: int
            value: float
            def __init__(self, name_token: int | None = ..., value: float | None = ...) -> None: ...

        class StrangeGemProgress(_message.Message):
            __slots__ = (
                "kill_eater_type",
                "gem_item_def_index",
                "required_hero_id",
                "starting_value",
                "ending_value",
                "owner_item_def_index",
                "owner_item_id",
            )
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
            def __init__(
                self,
                kill_eater_type: int | None = ...,
                gem_item_def_index: int | None = ...,
                required_hero_id: int | None = ...,
                starting_value: int | None = ...,
                ending_value: int | None = ...,
                owner_item_def_index: int | None = ...,
                owner_item_id: int | None = ...,
            ) -> None: ...

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
            def __init__(
                self,
                item_id: int | None = ...,
                item_def_index: int | None = ...,
                starting_value: int | None = ...,
                is_victory: bool = ...,
            ) -> None: ...

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
            def __init__(
                self,
                slot_id: int | None = ...,
                start_value: int | None = ...,
                end_value: int | None = ...,
                completed: bool = ...,
            ) -> None: ...

        class CavernChallengeResult(_message.Message):
            __slots__ = ("completed_path_id", "claimed_room_id")
            COMPLETED_PATH_ID_FIELD_NUMBER: _ClassVar[int]
            CLAIMED_ROOM_ID_FIELD_NUMBER: _ClassVar[int]
            completed_path_id: int
            claimed_room_id: int
            def __init__(
                self, completed_path_id: int | None = ..., claimed_room_id: int | None = ...
            ) -> None: ...

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
            def __init__(
                self,
                action_id: int | None = ...,
                quantity: int | None = ...,
                audit: int | None = ...,
                audit_data: int | None = ...,
            ) -> None: ...

        class CandyGrant(_message.Message):
            __slots__ = ("points", "reason")
            POINTS_FIELD_NUMBER: _ClassVar[int]
            REASON_FIELD_NUMBER: _ClassVar[int]
            points: int
            reason: int
            def __init__(self, points: int | None = ..., reason: int | None = ...) -> None: ...

        class PeriodicResourceData(_message.Message):
            __slots__ = ("periodic_resource_id", "remaining", "max")
            PERIODIC_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
            REMAINING_FIELD_NUMBER: _ClassVar[int]
            MAX_FIELD_NUMBER: _ClassVar[int]
            periodic_resource_id: int
            remaining: int
            max: int
            def __init__(
                self,
                periodic_resource_id: int | None = ...,
                remaining: int | None = ...,
                max: int | None = ...,
            ) -> None: ...

        class EventData(_message.Message):
            __slots__ = (
                "event_id",
                "event_points",
                "challenge_instance_id",
                "challenge_quest_id",
                "challenge_quest_challenge_id",
                "challenge_completed",
                "challenge_rank_completed",
                "challenge_rank_previously_completed",
                "event_owned",
                "sub_challenges_with_progress",
                "wager_winnings",
                "cavern_challenge_active",
                "cavern_challenge_winnings",
                "amount_wagered",
                "periodic_point_adjustments",
                "cavern_challenge_map_results",
                "cavern_challenge_plus_shard_winnings",
                "actions_granted",
                "cavern_crawl_map_variant",
                "team_wager_bonus_pct",
                "wager_streak_pct",
                "candy_points_granted",
                "active_season_id",
                "cavern_crawl_half_credit",
                "periodic_resources",
                "extra_event_messages",
            )
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
            sub_challenges_with_progress: _containers.RepeatedCompositeFieldContainer[
                CDOTAMatchMetadata.Team.SubChallenge
            ]
            wager_winnings: int
            cavern_challenge_active: bool
            cavern_challenge_winnings: int
            amount_wagered: int
            periodic_point_adjustments: int
            cavern_challenge_map_results: _containers.RepeatedCompositeFieldContainer[
                CDOTAMatchMetadata.Team.CavernChallengeResult
            ]
            cavern_challenge_plus_shard_winnings: int
            actions_granted: _containers.RepeatedCompositeFieldContainer[
                CDOTAMatchMetadata.Team.ActionGrant
            ]
            cavern_crawl_map_variant: int
            team_wager_bonus_pct: int
            wager_streak_pct: int
            candy_points_granted: _containers.RepeatedCompositeFieldContainer[
                CDOTAMatchMetadata.Team.CandyGrant
            ]
            active_season_id: int
            cavern_crawl_half_credit: bool
            periodic_resources: _containers.RepeatedCompositeFieldContainer[
                CDOTAMatchMetadata.Team.PeriodicResourceData
            ]
            extra_event_messages: _containers.RepeatedCompositeFieldContainer[
                _gcsdk_gcmessages_pb2.CExtraMsgBlock
            ]
            def __init__(
                self,
                event_id: int | None = ...,
                event_points: int | None = ...,
                challenge_instance_id: int | None = ...,
                challenge_quest_id: int | None = ...,
                challenge_quest_challenge_id: int | None = ...,
                challenge_completed: bool = ...,
                challenge_rank_completed: int | None = ...,
                challenge_rank_previously_completed: int | None = ...,
                event_owned: bool = ...,
                sub_challenges_with_progress: _Iterable[
                    CDOTAMatchMetadata.Team.SubChallenge | _Mapping
                ]
                | None = ...,
                wager_winnings: int | None = ...,
                cavern_challenge_active: bool = ...,
                cavern_challenge_winnings: int | None = ...,
                amount_wagered: int | None = ...,
                periodic_point_adjustments: int | None = ...,
                cavern_challenge_map_results: _Iterable[
                    CDOTAMatchMetadata.Team.CavernChallengeResult | _Mapping
                ]
                | None = ...,
                cavern_challenge_plus_shard_winnings: int | None = ...,
                actions_granted: _Iterable[CDOTAMatchMetadata.Team.ActionGrant | _Mapping]
                | None = ...,
                cavern_crawl_map_variant: int | None = ...,
                team_wager_bonus_pct: int | None = ...,
                wager_streak_pct: int | None = ...,
                candy_points_granted: _Iterable[CDOTAMatchMetadata.Team.CandyGrant | _Mapping]
                | None = ...,
                active_season_id: int | None = ...,
                cavern_crawl_half_credit: bool = ...,
                periodic_resources: _Iterable[
                    CDOTAMatchMetadata.Team.PeriodicResourceData | _Mapping
                ]
                | None = ...,
                extra_event_messages: _Iterable[_gcsdk_gcmessages_pb2.CExtraMsgBlock | _Mapping]
                | None = ...,
            ) -> None: ...

        class FeaturedGamemodeProgress(_message.Message):
            __slots__ = ("start_value", "end_value", "max_value")
            START_VALUE_FIELD_NUMBER: _ClassVar[int]
            END_VALUE_FIELD_NUMBER: _ClassVar[int]
            MAX_VALUE_FIELD_NUMBER: _ClassVar[int]
            start_value: int
            end_value: int
            max_value: int
            def __init__(
                self,
                start_value: int | None = ...,
                end_value: int | None = ...,
                max_value: int | None = ...,
            ) -> None: ...

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
            def __init__(
                self,
                kill_type: CDOTAMatchMetadata.Team.KillInfo.KillType | str | None = ...,
                victim_player_slot: int | None = ...,
                killer_player_slot: _Iterable[int] | None = ...,
                time: int | None = ...,
                bounty: int | None = ...,
            ) -> None: ...

        class Player(_message.Message):
            __slots__ = (
                "ability_upgrades",
                "player_slot",
                "kills",
                "items",
                "avg_kills_x16",
                "avg_deaths_x16",
                "avg_assists_x16",
                "avg_gpm_x16",
                "avg_xpm_x16",
                "best_kills_x16",
                "best_assists_x16",
                "best_gpm_x16",
                "best_xpm_x16",
                "win_streak",
                "best_win_streak",
                "fight_score",
                "farm_score",
                "support_score",
                "push_score",
                "level_up_times",
                "graph_net_worth",
                "inventory_snapshot",
                "avg_stats_calibrated",
                "auto_style_criteria",
                "event_data",
                "strange_gem_progress",
                "hero_xp",
                "camps_stacked",
                "victory_prediction",
                "lane_selection_flags",
                "rampages",
                "triple_kills",
                "aegis_snatched",
                "rapiers_purchased",
                "couriers_killed",
                "net_worth_rank",
                "support_gold_spent",
                "observer_wards_placed",
                "sentry_wards_placed",
                "wards_dewarded",
                "stun_duration",
                "rank_mmr_boost_type",
                "contract_progress",
                "guild_ids",
                "graph_hero_damage",
                "team_number",
                "team_slot",
                "featured_gamemode_progress",
                "featured_hero_sticker_index",
                "featured_hero_sticker_quality",
                "equipped_econ_items",
                "game_player_id",
                "player_tracked_stats",
                "overworld_rewards",
                "craftworks_quest_rewards",
                "ad_facet_hero_id",
                "monster_hunter_rewards",
            )
            class ContractProgress(_message.Message):
                __slots__ = (
                    "guild_id",
                    "event_id",
                    "challenge_instance_id",
                    "challenge_parameter",
                    "contract_stars",
                    "contract_slot",
                    "completed",
                )
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
                def __init__(
                    self,
                    guild_id: int | None = ...,
                    event_id: int | None = ...,
                    challenge_instance_id: int | None = ...,
                    challenge_parameter: int | None = ...,
                    contract_stars: int | None = ...,
                    contract_slot: int | None = ...,
                    completed: bool = ...,
                ) -> None: ...

            class OverworldRewards(_message.Message):
                __slots__ = ("overworld_id", "tokens")
                OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
                TOKENS_FIELD_NUMBER: _ClassVar[int]
                overworld_id: int
                tokens: _dota_gcmessages_common_overworld_pb2.CMsgOverworldTokenQuantity
                def __init__(
                    self,
                    overworld_id: int | None = ...,
                    tokens: _dota_gcmessages_common_overworld_pb2.CMsgOverworldTokenQuantity
                    | _Mapping
                    | None = ...,
                ) -> None: ...

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
            inventory_snapshot: _containers.RepeatedCompositeFieldContainer[
                CDOTAMatchMetadata.Team.InventorySnapshot
            ]
            avg_stats_calibrated: bool
            auto_style_criteria: _containers.RepeatedCompositeFieldContainer[
                CDOTAMatchMetadata.Team.AutoStyleCriteria
            ]
            event_data: _containers.RepeatedCompositeFieldContainer[
                CDOTAMatchMetadata.Team.EventData
            ]
            strange_gem_progress: _containers.RepeatedCompositeFieldContainer[
                CDOTAMatchMetadata.Team.StrangeGemProgress
            ]
            hero_xp: int
            camps_stacked: int
            victory_prediction: _containers.RepeatedCompositeFieldContainer[
                CDOTAMatchMetadata.Team.VictoryPrediction
            ]
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
            contract_progress: _containers.RepeatedCompositeFieldContainer[
                CDOTAMatchMetadata.Team.Player.ContractProgress
            ]
            guild_ids: _containers.RepeatedScalarFieldContainer[int]
            graph_hero_damage: _containers.RepeatedScalarFieldContainer[float]
            team_number: _dota_shared_enums_pb2.DOTA_GC_TEAM
            team_slot: int
            featured_gamemode_progress: CDOTAMatchMetadata.Team.FeaturedGamemodeProgress
            featured_hero_sticker_index: int
            featured_hero_sticker_quality: int
            equipped_econ_items: _containers.RepeatedCompositeFieldContainer[
                CDOTAMatchMetadata.EconItem
            ]
            game_player_id: int
            player_tracked_stats: _containers.RepeatedCompositeFieldContainer[
                _dota_gcmessages_common_pb2.CMsgTrackedStat
            ]
            overworld_rewards: CDOTAMatchMetadata.Team.Player.OverworldRewards
            craftworks_quest_rewards: _containers.RepeatedCompositeFieldContainer[
                _dota_gcmessages_common_craftworks_pb2.CMsgCraftworksQuestReward
            ]
            ad_facet_hero_id: int
            monster_hunter_rewards: (
                _dota_gcmessages_common_monster_hunter_pb2.CMsgMonsterHunterMatchRewards.Player
            )
            def __init__(
                self,
                ability_upgrades: _Iterable[int] | None = ...,
                player_slot: int | None = ...,
                kills: _Iterable[CDOTAMatchMetadata.Team.PlayerKill | _Mapping] | None = ...,
                items: _Iterable[CDOTAMatchMetadata.Team.ItemPurchase | _Mapping] | None = ...,
                avg_kills_x16: int | None = ...,
                avg_deaths_x16: int | None = ...,
                avg_assists_x16: int | None = ...,
                avg_gpm_x16: int | None = ...,
                avg_xpm_x16: int | None = ...,
                best_kills_x16: int | None = ...,
                best_assists_x16: int | None = ...,
                best_gpm_x16: int | None = ...,
                best_xpm_x16: int | None = ...,
                win_streak: int | None = ...,
                best_win_streak: int | None = ...,
                fight_score: float | None = ...,
                farm_score: float | None = ...,
                support_score: float | None = ...,
                push_score: float | None = ...,
                level_up_times: _Iterable[int] | None = ...,
                graph_net_worth: _Iterable[float] | None = ...,
                inventory_snapshot: _Iterable[CDOTAMatchMetadata.Team.InventorySnapshot | _Mapping]
                | None = ...,
                avg_stats_calibrated: bool = ...,
                auto_style_criteria: _Iterable[CDOTAMatchMetadata.Team.AutoStyleCriteria | _Mapping]
                | None = ...,
                event_data: _Iterable[CDOTAMatchMetadata.Team.EventData | _Mapping] | None = ...,
                strange_gem_progress: _Iterable[
                    CDOTAMatchMetadata.Team.StrangeGemProgress | _Mapping
                ]
                | None = ...,
                hero_xp: int | None = ...,
                camps_stacked: int | None = ...,
                victory_prediction: _Iterable[CDOTAMatchMetadata.Team.VictoryPrediction | _Mapping]
                | None = ...,
                lane_selection_flags: int | None = ...,
                rampages: int | None = ...,
                triple_kills: int | None = ...,
                aegis_snatched: int | None = ...,
                rapiers_purchased: int | None = ...,
                couriers_killed: int | None = ...,
                net_worth_rank: int | None = ...,
                support_gold_spent: int | None = ...,
                observer_wards_placed: int | None = ...,
                sentry_wards_placed: int | None = ...,
                wards_dewarded: int | None = ...,
                stun_duration: float | None = ...,
                rank_mmr_boost_type: _dota_shared_enums_pb2.EDOTAMMRBoostType | str | None = ...,
                contract_progress: _Iterable[
                    CDOTAMatchMetadata.Team.Player.ContractProgress | _Mapping
                ]
                | None = ...,
                guild_ids: _Iterable[int] | None = ...,
                graph_hero_damage: _Iterable[float] | None = ...,
                team_number: _dota_shared_enums_pb2.DOTA_GC_TEAM | str | None = ...,
                team_slot: int | None = ...,
                featured_gamemode_progress: CDOTAMatchMetadata.Team.FeaturedGamemodeProgress
                | _Mapping
                | None = ...,
                featured_hero_sticker_index: int | None = ...,
                featured_hero_sticker_quality: int | None = ...,
                equipped_econ_items: _Iterable[CDOTAMatchMetadata.EconItem | _Mapping] | None = ...,
                game_player_id: int | None = ...,
                player_tracked_stats: _Iterable[
                    _dota_gcmessages_common_pb2.CMsgTrackedStat | _Mapping
                ]
                | None = ...,
                overworld_rewards: CDOTAMatchMetadata.Team.Player.OverworldRewards
                | _Mapping
                | None = ...,
                craftworks_quest_rewards: _Iterable[
                    _dota_gcmessages_common_craftworks_pb2.CMsgCraftworksQuestReward | _Mapping
                ]
                | None = ...,
                ad_facet_hero_id: int | None = ...,
                monster_hunter_rewards: _dota_gcmessages_common_monster_hunter_pb2.CMsgMonsterHunterMatchRewards.Player
                | _Mapping
                | None = ...,
            ) -> None: ...

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
        team_tracked_stats: _containers.RepeatedCompositeFieldContainer[
            _dota_gcmessages_common_pb2.CMsgTrackedStat
        ]
        kills: _containers.RepeatedCompositeFieldContainer[CDOTAMatchMetadata.Team.KillInfo]
        def __init__(
            self,
            dota_team: int | None = ...,
            players: _Iterable[CDOTAMatchMetadata.Team.Player | _Mapping] | None = ...,
            graph_experience: _Iterable[float] | None = ...,
            graph_gold_earned: _Iterable[float] | None = ...,
            graph_net_worth: _Iterable[float] | None = ...,
            cm_first_pick: bool = ...,
            cm_captain_player_id: int | None = ...,
            cm_penalty: int | None = ...,
            team_tracked_stats: _Iterable[_dota_gcmessages_common_pb2.CMsgTrackedStat | _Mapping]
            | None = ...,
            kills: _Iterable[CDOTAMatchMetadata.Team.KillInfo | _Mapping] | None = ...,
        ) -> None: ...

    class GuildChallengeProgress(_message.Message):
        __slots__ = (
            "guild_id",
            "event_id",
            "challenge_instance_id",
            "challenge_parameter",
            "challenge_timestamp",
            "challenge_progress_at_start",
            "challenge_progress_accumulated",
            "individual_progress",
        )
        class IndividualProgress(_message.Message):
            __slots__ = ("progress", "player_slot")
            PROGRESS_FIELD_NUMBER: _ClassVar[int]
            PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
            progress: int
            player_slot: int
            def __init__(
                self, progress: int | None = ..., player_slot: int | None = ...
            ) -> None: ...

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
        individual_progress: _containers.RepeatedCompositeFieldContainer[
            CDOTAMatchMetadata.GuildChallengeProgress.IndividualProgress
        ]
        def __init__(
            self,
            guild_id: int | None = ...,
            event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
            challenge_instance_id: int | None = ...,
            challenge_parameter: int | None = ...,
            challenge_timestamp: int | None = ...,
            challenge_progress_at_start: int | None = ...,
            challenge_progress_accumulated: int | None = ...,
            individual_progress: _Iterable[
                CDOTAMatchMetadata.GuildChallengeProgress.IndividualProgress | _Mapping
            ]
            | None = ...,
        ) -> None: ...

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
        def __init__(
            self,
            source_player_slot: int | None = ...,
            target_player_slot: int | None = ...,
            tip_amount: int | None = ...,
            event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
        ) -> None: ...

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
    guild_challenge_progress: _containers.RepeatedCompositeFieldContainer[
        CDOTAMatchMetadata.GuildChallengeProgress
    ]
    custom_post_game_table: bytes
    match_tips: _containers.RepeatedCompositeFieldContainer[CDOTAMatchMetadata.Tip]
    match_tracked_stats: _containers.RepeatedCompositeFieldContainer[
        _dota_gcmessages_common_pb2.CMsgTrackedStat
    ]
    primary_event_id_for_display: int
    def __init__(
        self,
        teams: _Iterable[CDOTAMatchMetadata.Team | _Mapping] | None = ...,
        lobby_id: int | None = ...,
        report_until_time: int | None = ...,
        event_game_custom_table: bytes | None = ...,
        primary_event_id: int | None = ...,
        matchmaking_stats: _dota_gcmessages_common_match_management_pb2.CMsgMatchMatchmakingStats
        | _Mapping
        | None = ...,
        mvp_data: _dota_gcmessages_common_match_management_pb2.CMvpData | _Mapping | None = ...,
        guild_challenge_progress: _Iterable[CDOTAMatchMetadata.GuildChallengeProgress | _Mapping]
        | None = ...,
        custom_post_game_table: bytes | None = ...,
        match_tips: _Iterable[CDOTAMatchMetadata.Tip | _Mapping] | None = ...,
        match_tracked_stats: _Iterable[_dota_gcmessages_common_pb2.CMsgTrackedStat | _Mapping]
        | None = ...,
        primary_event_id_for_display: int | None = ...,
    ) -> None: ...

class CDOTAMatchPrivateMetadata(_message.Message):
    __slots__ = ("teams", "graph_win_probability", "string_names")
    class StringName(_message.Message):
        __slots__ = ("id", "name")
        ID_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        id: int
        name: str
        def __init__(self, id: int | None = ..., name: str | None = ...) -> None: ...

    class Team(_message.Message):
        __slots__ = ("dota_team", "players", "buildings")
        class Player(_message.Message):
            __slots__ = (
                "player_slot",
                "position_stream",
                "combat_segments",
                "damage_unit_names",
                "buff_records",
                "graph_kills",
                "graph_deaths",
                "graph_assists",
                "graph_lasthits",
                "graph_denies",
                "gold_received",
                "xp_received",
                "team_number",
                "team_slot",
            )
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
                        def __init__(
                            self, hero_id: int | None = ..., damage: int | None = ...
                        ) -> None: ...

                    SOURCE_UNIT_INDEX_FIELD_NUMBER: _ClassVar[int]
                    ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
                    BY_HERO_TARGETS_FIELD_NUMBER: _ClassVar[int]
                    source_unit_index: int
                    ability_id: int
                    by_hero_targets: _containers.RepeatedCompositeFieldContainer[
                        CDOTAMatchPrivateMetadata.Team.Player.CombatSegment.DamageByAbility.ByHeroTarget
                    ]
                    def __init__(
                        self,
                        source_unit_index: int | None = ...,
                        ability_id: int | None = ...,
                        by_hero_targets: _Iterable[
                            CDOTAMatchPrivateMetadata.Team.Player.CombatSegment.DamageByAbility.ByHeroTarget
                            | _Mapping
                        ]
                        | None = ...,
                    ) -> None: ...

                class HealingByAbility(_message.Message):
                    __slots__ = ("source_unit_index", "ability_id", "by_hero_targets")
                    class ByHeroTarget(_message.Message):
                        __slots__ = ("hero_id", "healing")
                        HERO_ID_FIELD_NUMBER: _ClassVar[int]
                        HEALING_FIELD_NUMBER: _ClassVar[int]
                        hero_id: int
                        healing: int
                        def __init__(
                            self, hero_id: int | None = ..., healing: int | None = ...
                        ) -> None: ...

                    SOURCE_UNIT_INDEX_FIELD_NUMBER: _ClassVar[int]
                    ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
                    BY_HERO_TARGETS_FIELD_NUMBER: _ClassVar[int]
                    source_unit_index: int
                    ability_id: int
                    by_hero_targets: _containers.RepeatedCompositeFieldContainer[
                        CDOTAMatchPrivateMetadata.Team.Player.CombatSegment.HealingByAbility.ByHeroTarget
                    ]
                    def __init__(
                        self,
                        source_unit_index: int | None = ...,
                        ability_id: int | None = ...,
                        by_hero_targets: _Iterable[
                            CDOTAMatchPrivateMetadata.Team.Player.CombatSegment.HealingByAbility.ByHeroTarget
                            | _Mapping
                        ]
                        | None = ...,
                    ) -> None: ...

                GAME_TIME_FIELD_NUMBER: _ClassVar[int]
                DAMAGE_BY_ABILITY_FIELD_NUMBER: _ClassVar[int]
                HEALING_BY_ABILITY_FIELD_NUMBER: _ClassVar[int]
                game_time: int
                damage_by_ability: _containers.RepeatedCompositeFieldContainer[
                    CDOTAMatchPrivateMetadata.Team.Player.CombatSegment.DamageByAbility
                ]
                healing_by_ability: _containers.RepeatedCompositeFieldContainer[
                    CDOTAMatchPrivateMetadata.Team.Player.CombatSegment.HealingByAbility
                ]
                def __init__(
                    self,
                    game_time: int | None = ...,
                    damage_by_ability: _Iterable[
                        CDOTAMatchPrivateMetadata.Team.Player.CombatSegment.DamageByAbility
                        | _Mapping
                    ]
                    | None = ...,
                    healing_by_ability: _Iterable[
                        CDOTAMatchPrivateMetadata.Team.Player.CombatSegment.HealingByAbility
                        | _Mapping
                    ]
                    | None = ...,
                ) -> None: ...

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
                    def __init__(
                        self,
                        hero_id: int | None = ...,
                        elapsed_duration: float | None = ...,
                        is_hidden: bool = ...,
                        instance_count: int | None = ...,
                    ) -> None: ...

                BUFF_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
                BUFF_MODIFIER_NAME_FIELD_NUMBER: _ClassVar[int]
                BY_HERO_TARGETS_FIELD_NUMBER: _ClassVar[int]
                buff_ability_id: int
                buff_modifier_name: str
                by_hero_targets: _containers.RepeatedCompositeFieldContainer[
                    CDOTAMatchPrivateMetadata.Team.Player.BuffRecord.ByHeroTarget
                ]
                def __init__(
                    self,
                    buff_ability_id: int | None = ...,
                    buff_modifier_name: str | None = ...,
                    by_hero_targets: _Iterable[
                        CDOTAMatchPrivateMetadata.Team.Player.BuffRecord.ByHeroTarget | _Mapping
                    ]
                    | None = ...,
                ) -> None: ...

            class GoldReceived(_message.Message):
                __slots__ = (
                    "creep",
                    "heroes",
                    "bounty_runes",
                    "passive",
                    "buildings",
                    "abilities",
                    "wards",
                    "other",
                )
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
                def __init__(
                    self,
                    creep: int | None = ...,
                    heroes: int | None = ...,
                    bounty_runes: int | None = ...,
                    passive: int | None = ...,
                    buildings: int | None = ...,
                    abilities: int | None = ...,
                    wards: int | None = ...,
                    other: int | None = ...,
                ) -> None: ...

            class XPReceived(_message.Message):
                __slots__ = (
                    "creep",
                    "heroes",
                    "roshan",
                    "tome_of_knowledge",
                    "outpost",
                    "other",
                    "abilities",
                )
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
                def __init__(
                    self,
                    creep: int | None = ...,
                    heroes: int | None = ...,
                    roshan: int | None = ...,
                    tome_of_knowledge: int | None = ...,
                    outpost: int | None = ...,
                    other: int | None = ...,
                    abilities: int | None = ...,
                ) -> None: ...

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
            combat_segments: _containers.RepeatedCompositeFieldContainer[
                CDOTAMatchPrivateMetadata.Team.Player.CombatSegment
            ]
            damage_unit_names: _containers.RepeatedScalarFieldContainer[str]
            buff_records: _containers.RepeatedCompositeFieldContainer[
                CDOTAMatchPrivateMetadata.Team.Player.BuffRecord
            ]
            graph_kills: _containers.RepeatedScalarFieldContainer[float]
            graph_deaths: _containers.RepeatedScalarFieldContainer[float]
            graph_assists: _containers.RepeatedScalarFieldContainer[float]
            graph_lasthits: _containers.RepeatedScalarFieldContainer[float]
            graph_denies: _containers.RepeatedScalarFieldContainer[float]
            gold_received: CDOTAMatchPrivateMetadata.Team.Player.GoldReceived
            xp_received: CDOTAMatchPrivateMetadata.Team.Player.XPReceived
            team_number: _dota_shared_enums_pb2.DOTA_GC_TEAM
            team_slot: int
            def __init__(
                self,
                player_slot: int | None = ...,
                position_stream: bytes | None = ...,
                combat_segments: _Iterable[
                    CDOTAMatchPrivateMetadata.Team.Player.CombatSegment | _Mapping
                ]
                | None = ...,
                damage_unit_names: _Iterable[str] | None = ...,
                buff_records: _Iterable[CDOTAMatchPrivateMetadata.Team.Player.BuffRecord | _Mapping]
                | None = ...,
                graph_kills: _Iterable[float] | None = ...,
                graph_deaths: _Iterable[float] | None = ...,
                graph_assists: _Iterable[float] | None = ...,
                graph_lasthits: _Iterable[float] | None = ...,
                graph_denies: _Iterable[float] | None = ...,
                gold_received: CDOTAMatchPrivateMetadata.Team.Player.GoldReceived
                | _Mapping
                | None = ...,
                xp_received: CDOTAMatchPrivateMetadata.Team.Player.XPReceived
                | _Mapping
                | None = ...,
                team_number: _dota_shared_enums_pb2.DOTA_GC_TEAM | str | None = ...,
                team_slot: int | None = ...,
            ) -> None: ...

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
            def __init__(
                self,
                unit_name: str | None = ...,
                position_quant_x: int | None = ...,
                position_quant_y: int | None = ...,
                death_time: float | None = ...,
            ) -> None: ...

        DOTA_TEAM_FIELD_NUMBER: _ClassVar[int]
        PLAYERS_FIELD_NUMBER: _ClassVar[int]
        BUILDINGS_FIELD_NUMBER: _ClassVar[int]
        dota_team: int
        players: _containers.RepeatedCompositeFieldContainer[CDOTAMatchPrivateMetadata.Team.Player]
        buildings: _containers.RepeatedCompositeFieldContainer[
            CDOTAMatchPrivateMetadata.Team.Building
        ]
        def __init__(
            self,
            dota_team: int | None = ...,
            players: _Iterable[CDOTAMatchPrivateMetadata.Team.Player | _Mapping] | None = ...,
            buildings: _Iterable[CDOTAMatchPrivateMetadata.Team.Building | _Mapping] | None = ...,
        ) -> None: ...

    TEAMS_FIELD_NUMBER: _ClassVar[int]
    GRAPH_WIN_PROBABILITY_FIELD_NUMBER: _ClassVar[int]
    STRING_NAMES_FIELD_NUMBER: _ClassVar[int]
    teams: _containers.RepeatedCompositeFieldContainer[CDOTAMatchPrivateMetadata.Team]
    graph_win_probability: _containers.RepeatedScalarFieldContainer[float]
    string_names: _containers.RepeatedCompositeFieldContainer[CDOTAMatchPrivateMetadata.StringName]
    def __init__(
        self,
        teams: _Iterable[CDOTAMatchPrivateMetadata.Team | _Mapping] | None = ...,
        graph_win_probability: _Iterable[float] | None = ...,
        string_names: _Iterable[CDOTAMatchPrivateMetadata.StringName | _Mapping] | None = ...,
    ) -> None: ...
