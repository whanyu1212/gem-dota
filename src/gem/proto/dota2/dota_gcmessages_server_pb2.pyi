from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

import dota_gcmessages_common_craftworks_pb2 as _dota_gcmessages_common_craftworks_pb2
import dota_gcmessages_common_match_management_pb2 as _dota_gcmessages_common_match_management_pb2
import dota_gcmessages_common_monster_hunter_pb2 as _dota_gcmessages_common_monster_hunter_pb2
import dota_gcmessages_common_overworld_pb2 as _dota_gcmessages_common_overworld_pb2
import dota_gcmessages_common_pb2 as _dota_gcmessages_common_pb2
import dota_shared_enums_pb2 as _dota_shared_enums_pb2
import econ_gcmessages_pb2 as _econ_gcmessages_pb2
import gcsdk_gcmessages_pb2 as _gcsdk_gcmessages_pb2
import network_connection_pb2 as _network_connection_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class EPoorNetworkConditionsType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EPoorNetworkConditions_None: _ClassVar[EPoorNetworkConditionsType]
    k_EPoorNetworkConditions_Unknown: _ClassVar[EPoorNetworkConditionsType]
    k_EPoorNetworkConditions_MassDisconnect: _ClassVar[EPoorNetworkConditionsType]
    k_EPoorNetworkConditions_ExcessBadQosIntervals: _ClassVar[EPoorNetworkConditionsType]

k_EPoorNetworkConditions_None: EPoorNetworkConditionsType
k_EPoorNetworkConditions_Unknown: EPoorNetworkConditionsType
k_EPoorNetworkConditions_MassDisconnect: EPoorNetworkConditionsType
k_EPoorNetworkConditions_ExcessBadQosIntervals: EPoorNetworkConditionsType

class CMsgPoorNetworkConditions(_message.Message):
    __slots__ = ("detection_type", "players")
    class Player(_message.Message):
        __slots__ = ("account_id", "disconnect_reason", "num_bad_intervals", "peak_loss_pct")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        DISCONNECT_REASON_FIELD_NUMBER: _ClassVar[int]
        NUM_BAD_INTERVALS_FIELD_NUMBER: _ClassVar[int]
        PEAK_LOSS_PCT_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        disconnect_reason: _network_connection_pb2.ENetworkDisconnectionReason
        num_bad_intervals: int
        peak_loss_pct: int
        def __init__(
            self,
            account_id: int | None = ...,
            disconnect_reason: _network_connection_pb2.ENetworkDisconnectionReason
            | str
            | None = ...,
            num_bad_intervals: int | None = ...,
            peak_loss_pct: int | None = ...,
        ) -> None: ...

    DETECTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    detection_type: EPoorNetworkConditionsType
    players: _containers.RepeatedCompositeFieldContainer[CMsgPoorNetworkConditions.Player]
    def __init__(
        self,
        detection_type: EPoorNetworkConditionsType | str | None = ...,
        players: _Iterable[CMsgPoorNetworkConditions.Player | _Mapping] | None = ...,
    ) -> None: ...

class CMsgGameserverCrash(_message.Message):
    __slots__ = (
        "match_id",
        "lobby_id",
        "game_state",
        "sentinel_save_time",
        "custom_game_id",
        "tournament_id",
        "server_steam_id",
        "server_public_ip_addr",
        "server_port",
        "server_cluster",
        "pid",
        "engine",
    )
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    LOBBY_ID_FIELD_NUMBER: _ClassVar[int]
    GAME_STATE_FIELD_NUMBER: _ClassVar[int]
    SENTINEL_SAVE_TIME_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_ID_FIELD_NUMBER: _ClassVar[int]
    TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    SERVER_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    SERVER_PUBLIC_IP_ADDR_FIELD_NUMBER: _ClassVar[int]
    SERVER_PORT_FIELD_NUMBER: _ClassVar[int]
    SERVER_CLUSTER_FIELD_NUMBER: _ClassVar[int]
    PID_FIELD_NUMBER: _ClassVar[int]
    ENGINE_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    lobby_id: int
    game_state: _dota_shared_enums_pb2.DOTA_GameState
    sentinel_save_time: int
    custom_game_id: int
    tournament_id: int
    server_steam_id: int
    server_public_ip_addr: int
    server_port: int
    server_cluster: int
    pid: int
    engine: int
    def __init__(
        self,
        match_id: int | None = ...,
        lobby_id: int | None = ...,
        game_state: _dota_shared_enums_pb2.DOTA_GameState | str | None = ...,
        sentinel_save_time: int | None = ...,
        custom_game_id: int | None = ...,
        tournament_id: int | None = ...,
        server_steam_id: int | None = ...,
        server_public_ip_addr: int | None = ...,
        server_port: int | None = ...,
        server_cluster: int | None = ...,
        pid: int | None = ...,
        engine: int | None = ...,
    ) -> None: ...

class CMsgConnectedPlayers(_message.Message):
    __slots__ = (
        "connected_players",
        "disconnected_players",
        "game_state",
        "first_blood_happened",
        "poor_network_conditions",
        "send_reason",
        "radiant_kills",
        "dire_kills",
        "radiant_lead",
        "building_state",
        "player_draft",
    )
    class SendReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INVALID: _ClassVar[CMsgConnectedPlayers.SendReason]
        HEARTBEAT: _ClassVar[CMsgConnectedPlayers.SendReason]
        GAME_STATE: _ClassVar[CMsgConnectedPlayers.SendReason]
        FIRST_BLOOD: _ClassVar[CMsgConnectedPlayers.SendReason]
        PLAYER_CONNECTED: _ClassVar[CMsgConnectedPlayers.SendReason]
        PLAYER_HERO: _ClassVar[CMsgConnectedPlayers.SendReason]
        PLAYER_DISCONNECTED_CONSEQUENCES: _ClassVar[CMsgConnectedPlayers.SendReason]
        PLAYER_DISCONNECTED_NOCONSEQUENCES: _ClassVar[CMsgConnectedPlayers.SendReason]
        GAMESTATE_TIMEOUT: _ClassVar[CMsgConnectedPlayers.SendReason]
        MASS_DISCONNECT: _ClassVar[CMsgConnectedPlayers.SendReason]
        KILLS: _ClassVar[CMsgConnectedPlayers.SendReason]
        BUILDING_STATE: _ClassVar[CMsgConnectedPlayers.SendReason]

    INVALID: CMsgConnectedPlayers.SendReason
    HEARTBEAT: CMsgConnectedPlayers.SendReason
    GAME_STATE: CMsgConnectedPlayers.SendReason
    FIRST_BLOOD: CMsgConnectedPlayers.SendReason
    PLAYER_CONNECTED: CMsgConnectedPlayers.SendReason
    PLAYER_HERO: CMsgConnectedPlayers.SendReason
    PLAYER_DISCONNECTED_CONSEQUENCES: CMsgConnectedPlayers.SendReason
    PLAYER_DISCONNECTED_NOCONSEQUENCES: CMsgConnectedPlayers.SendReason
    GAMESTATE_TIMEOUT: CMsgConnectedPlayers.SendReason
    MASS_DISCONNECT: CMsgConnectedPlayers.SendReason
    KILLS: CMsgConnectedPlayers.SendReason
    BUILDING_STATE: CMsgConnectedPlayers.SendReason
    class Player(_message.Message):
        __slots__ = ("steam_id", "hero_id", "leaver_state", "disconnect_reason")
        STEAM_ID_FIELD_NUMBER: _ClassVar[int]
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        LEAVER_STATE_FIELD_NUMBER: _ClassVar[int]
        DISCONNECT_REASON_FIELD_NUMBER: _ClassVar[int]
        steam_id: int
        hero_id: int
        leaver_state: _dota_gcmessages_common_match_management_pb2.CMsgLeaverState
        disconnect_reason: _network_connection_pb2.ENetworkDisconnectionReason
        def __init__(
            self,
            steam_id: int | None = ...,
            hero_id: int | None = ...,
            leaver_state: _dota_gcmessages_common_match_management_pb2.CMsgLeaverState
            | _Mapping
            | None = ...,
            disconnect_reason: _network_connection_pb2.ENetworkDisconnectionReason
            | str
            | None = ...,
        ) -> None: ...

    class PlayerDraft(_message.Message):
        __slots__ = ("steam_id", "team", "team_slot")
        STEAM_ID_FIELD_NUMBER: _ClassVar[int]
        TEAM_FIELD_NUMBER: _ClassVar[int]
        TEAM_SLOT_FIELD_NUMBER: _ClassVar[int]
        steam_id: int
        team: _dota_shared_enums_pb2.DOTA_GC_TEAM
        team_slot: int
        def __init__(
            self,
            steam_id: int | None = ...,
            team: _dota_shared_enums_pb2.DOTA_GC_TEAM | str | None = ...,
            team_slot: int | None = ...,
        ) -> None: ...

    CONNECTED_PLAYERS_FIELD_NUMBER: _ClassVar[int]
    DISCONNECTED_PLAYERS_FIELD_NUMBER: _ClassVar[int]
    GAME_STATE_FIELD_NUMBER: _ClassVar[int]
    FIRST_BLOOD_HAPPENED_FIELD_NUMBER: _ClassVar[int]
    POOR_NETWORK_CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    SEND_REASON_FIELD_NUMBER: _ClassVar[int]
    RADIANT_KILLS_FIELD_NUMBER: _ClassVar[int]
    DIRE_KILLS_FIELD_NUMBER: _ClassVar[int]
    RADIANT_LEAD_FIELD_NUMBER: _ClassVar[int]
    BUILDING_STATE_FIELD_NUMBER: _ClassVar[int]
    PLAYER_DRAFT_FIELD_NUMBER: _ClassVar[int]
    connected_players: _containers.RepeatedCompositeFieldContainer[CMsgConnectedPlayers.Player]
    disconnected_players: _containers.RepeatedCompositeFieldContainer[CMsgConnectedPlayers.Player]
    game_state: _dota_shared_enums_pb2.DOTA_GameState
    first_blood_happened: bool
    poor_network_conditions: CMsgPoorNetworkConditions
    send_reason: CMsgConnectedPlayers.SendReason
    radiant_kills: int
    dire_kills: int
    radiant_lead: int
    building_state: int
    player_draft: _containers.RepeatedCompositeFieldContainer[CMsgConnectedPlayers.PlayerDraft]
    def __init__(
        self,
        connected_players: _Iterable[CMsgConnectedPlayers.Player | _Mapping] | None = ...,
        disconnected_players: _Iterable[CMsgConnectedPlayers.Player | _Mapping] | None = ...,
        game_state: _dota_shared_enums_pb2.DOTA_GameState | str | None = ...,
        first_blood_happened: bool = ...,
        poor_network_conditions: CMsgPoorNetworkConditions | _Mapping | None = ...,
        send_reason: CMsgConnectedPlayers.SendReason | str | None = ...,
        radiant_kills: int | None = ...,
        dire_kills: int | None = ...,
        radiant_lead: int | None = ...,
        building_state: int | None = ...,
        player_draft: _Iterable[CMsgConnectedPlayers.PlayerDraft | _Mapping] | None = ...,
    ) -> None: ...

class CMsgGameServerInfo(_message.Message):
    __slots__ = (
        "server_public_ip_addr",
        "server_private_ip_addr",
        "server_port",
        "server_tv_port",
        "assigned_server_tv_port",
        "legacy_server_steamdatagram_address",
        "server_key",
        "server_hibernation",
        "server_type",
        "server_region",
        "server_loadavg",
        "server_tv_broadcast_time",
        "server_game_time",
        "server_relay_connected_steam_id",
        "relay_slots_max",
        "relays_connected",
        "relay_clients_connected",
        "relayed_game_server_steam_id",
        "parent_relay_count",
        "tv_secret_code",
        "server_version",
        "server_cluster",
        "allow_custom_games",
        "build_version",
        "srcds_instance",
        "dev_force_server_type",
    )
    class ServerType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNSPECIFIED: _ClassVar[CMsgGameServerInfo.ServerType]
        GAME: _ClassVar[CMsgGameServerInfo.ServerType]
        PROXY: _ClassVar[CMsgGameServerInfo.ServerType]
        DOTA_ONLY: _ClassVar[CMsgGameServerInfo.ServerType]
        CUSTOM_GAME_ONLY: _ClassVar[CMsgGameServerInfo.ServerType]
        EVENT_GAME_ONLY: _ClassVar[CMsgGameServerInfo.ServerType]

    UNSPECIFIED: CMsgGameServerInfo.ServerType
    GAME: CMsgGameServerInfo.ServerType
    PROXY: CMsgGameServerInfo.ServerType
    DOTA_ONLY: CMsgGameServerInfo.ServerType
    CUSTOM_GAME_ONLY: CMsgGameServerInfo.ServerType
    EVENT_GAME_ONLY: CMsgGameServerInfo.ServerType
    class CustomGames(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        BOTH: _ClassVar[CMsgGameServerInfo.CustomGames]
        NONE: _ClassVar[CMsgGameServerInfo.CustomGames]
        ONLY: _ClassVar[CMsgGameServerInfo.CustomGames]
        EVENT: _ClassVar[CMsgGameServerInfo.CustomGames]

    BOTH: CMsgGameServerInfo.CustomGames
    NONE: CMsgGameServerInfo.CustomGames
    ONLY: CMsgGameServerInfo.CustomGames
    EVENT: CMsgGameServerInfo.CustomGames
    SERVER_PUBLIC_IP_ADDR_FIELD_NUMBER: _ClassVar[int]
    SERVER_PRIVATE_IP_ADDR_FIELD_NUMBER: _ClassVar[int]
    SERVER_PORT_FIELD_NUMBER: _ClassVar[int]
    SERVER_TV_PORT_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_SERVER_TV_PORT_FIELD_NUMBER: _ClassVar[int]
    LEGACY_SERVER_STEAMDATAGRAM_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SERVER_KEY_FIELD_NUMBER: _ClassVar[int]
    SERVER_HIBERNATION_FIELD_NUMBER: _ClassVar[int]
    SERVER_TYPE_FIELD_NUMBER: _ClassVar[int]
    SERVER_REGION_FIELD_NUMBER: _ClassVar[int]
    SERVER_LOADAVG_FIELD_NUMBER: _ClassVar[int]
    SERVER_TV_BROADCAST_TIME_FIELD_NUMBER: _ClassVar[int]
    SERVER_GAME_TIME_FIELD_NUMBER: _ClassVar[int]
    SERVER_RELAY_CONNECTED_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    RELAY_SLOTS_MAX_FIELD_NUMBER: _ClassVar[int]
    RELAYS_CONNECTED_FIELD_NUMBER: _ClassVar[int]
    RELAY_CLIENTS_CONNECTED_FIELD_NUMBER: _ClassVar[int]
    RELAYED_GAME_SERVER_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_RELAY_COUNT_FIELD_NUMBER: _ClassVar[int]
    TV_SECRET_CODE_FIELD_NUMBER: _ClassVar[int]
    SERVER_VERSION_FIELD_NUMBER: _ClassVar[int]
    SERVER_CLUSTER_FIELD_NUMBER: _ClassVar[int]
    ALLOW_CUSTOM_GAMES_FIELD_NUMBER: _ClassVar[int]
    BUILD_VERSION_FIELD_NUMBER: _ClassVar[int]
    SRCDS_INSTANCE_FIELD_NUMBER: _ClassVar[int]
    DEV_FORCE_SERVER_TYPE_FIELD_NUMBER: _ClassVar[int]
    server_public_ip_addr: int
    server_private_ip_addr: int
    server_port: int
    server_tv_port: int
    assigned_server_tv_port: int
    legacy_server_steamdatagram_address: bytes
    server_key: str
    server_hibernation: bool
    server_type: CMsgGameServerInfo.ServerType
    server_region: int
    server_loadavg: float
    server_tv_broadcast_time: float
    server_game_time: float
    server_relay_connected_steam_id: int
    relay_slots_max: int
    relays_connected: int
    relay_clients_connected: int
    relayed_game_server_steam_id: int
    parent_relay_count: int
    tv_secret_code: int
    server_version: int
    server_cluster: int
    allow_custom_games: CMsgGameServerInfo.CustomGames
    build_version: int
    srcds_instance: int
    dev_force_server_type: bool
    def __init__(
        self,
        server_public_ip_addr: int | None = ...,
        server_private_ip_addr: int | None = ...,
        server_port: int | None = ...,
        server_tv_port: int | None = ...,
        assigned_server_tv_port: int | None = ...,
        legacy_server_steamdatagram_address: bytes | None = ...,
        server_key: str | None = ...,
        server_hibernation: bool = ...,
        server_type: CMsgGameServerInfo.ServerType | str | None = ...,
        server_region: int | None = ...,
        server_loadavg: float | None = ...,
        server_tv_broadcast_time: float | None = ...,
        server_game_time: float | None = ...,
        server_relay_connected_steam_id: int | None = ...,
        relay_slots_max: int | None = ...,
        relays_connected: int | None = ...,
        relay_clients_connected: int | None = ...,
        relayed_game_server_steam_id: int | None = ...,
        parent_relay_count: int | None = ...,
        tv_secret_code: int | None = ...,
        server_version: int | None = ...,
        server_cluster: int | None = ...,
        allow_custom_games: CMsgGameServerInfo.CustomGames | str | None = ...,
        build_version: int | None = ...,
        srcds_instance: int | None = ...,
        dev_force_server_type: bool = ...,
    ) -> None: ...

class CMsgLeaverDetected(_message.Message):
    __slots__ = (
        "steam_id",
        "leaver_status",
        "leaver_state",
        "server_cluster",
        "disconnect_reason",
        "poor_network_conditions",
    )
    STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    LEAVER_STATUS_FIELD_NUMBER: _ClassVar[int]
    LEAVER_STATE_FIELD_NUMBER: _ClassVar[int]
    SERVER_CLUSTER_FIELD_NUMBER: _ClassVar[int]
    DISCONNECT_REASON_FIELD_NUMBER: _ClassVar[int]
    POOR_NETWORK_CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    steam_id: int
    leaver_status: _dota_shared_enums_pb2.DOTALeaverStatus_t
    leaver_state: _dota_gcmessages_common_match_management_pb2.CMsgLeaverState
    server_cluster: int
    disconnect_reason: _network_connection_pb2.ENetworkDisconnectionReason
    poor_network_conditions: CMsgPoorNetworkConditions
    def __init__(
        self,
        steam_id: int | None = ...,
        leaver_status: _dota_shared_enums_pb2.DOTALeaverStatus_t | str | None = ...,
        leaver_state: _dota_gcmessages_common_match_management_pb2.CMsgLeaverState
        | _Mapping
        | None = ...,
        server_cluster: int | None = ...,
        disconnect_reason: _network_connection_pb2.ENetworkDisconnectionReason | str | None = ...,
        poor_network_conditions: CMsgPoorNetworkConditions | _Mapping | None = ...,
    ) -> None: ...

class CMsgLeaverDetectedResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: int
    def __init__(self, result: int | None = ...) -> None: ...

class CMsgDOTAFantasyFinalPlayerStats(_message.Message):
    __slots__ = ("stats",)
    STATS_FIELD_NUMBER: _ClassVar[int]
    stats: _containers.RepeatedCompositeFieldContainer[
        _dota_gcmessages_common_pb2.CMsgDOTAFantasyPlayerStats
    ]
    def __init__(
        self,
        stats: _Iterable[_dota_gcmessages_common_pb2.CMsgDOTAFantasyPlayerStats | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgDOTAFantasyLivePlayerStats(_message.Message):
    __slots__ = ("stats",)
    STATS_FIELD_NUMBER: _ClassVar[int]
    stats: _containers.RepeatedCompositeFieldContainer[
        _dota_gcmessages_common_pb2.CMsgDOTAFantasyPlayerStats
    ]
    def __init__(
        self,
        stats: _Iterable[_dota_gcmessages_common_pb2.CMsgDOTAFantasyPlayerStats | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgServerToGCRealtimeStats(_message.Message):
    __slots__ = ("delayed",)
    DELAYED_FIELD_NUMBER: _ClassVar[int]
    delayed: _dota_gcmessages_common_pb2.CMsgDOTARealtimeGameStatsTerse
    def __init__(
        self,
        delayed: _dota_gcmessages_common_pb2.CMsgDOTARealtimeGameStatsTerse | _Mapping | None = ...,
    ) -> None: ...

class CMsgGCToServerRealtimeStatsStartStop(_message.Message):
    __slots__ = ("delayed",)
    DELAYED_FIELD_NUMBER: _ClassVar[int]
    delayed: bool
    def __init__(self, delayed: bool = ...) -> None: ...

class CMsgGCToServerUpdateSteamBroadcasting(_message.Message):
    __slots__ = ("active",)
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    active: bool
    def __init__(self, active: bool = ...) -> None: ...

class CMsgSignOutGameplayStats(_message.Message):
    __slots__ = ("teams",)
    class CPlayer(_message.Message):
        __slots__ = ("steam_id", "player_slot", "hero_id", "timed_player_stats")
        STEAM_ID_FIELD_NUMBER: _ClassVar[int]
        PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        TIMED_PLAYER_STATS_FIELD_NUMBER: _ClassVar[int]
        steam_id: int
        player_slot: int
        hero_id: int
        timed_player_stats: _containers.RepeatedCompositeFieldContainer[
            _dota_gcmessages_common_pb2.CMatchPlayerTimedStats
        ]
        def __init__(
            self,
            steam_id: int | None = ...,
            player_slot: int | None = ...,
            hero_id: int | None = ...,
            timed_player_stats: _Iterable[
                _dota_gcmessages_common_pb2.CMatchPlayerTimedStats | _Mapping
            ]
            | None = ...,
        ) -> None: ...

    class CTeam(_message.Message):
        __slots__ = ("is_winning_team", "is_radiant_team", "timed_team_stats", "players")
        IS_WINNING_TEAM_FIELD_NUMBER: _ClassVar[int]
        IS_RADIANT_TEAM_FIELD_NUMBER: _ClassVar[int]
        TIMED_TEAM_STATS_FIELD_NUMBER: _ClassVar[int]
        PLAYERS_FIELD_NUMBER: _ClassVar[int]
        is_winning_team: bool
        is_radiant_team: bool
        timed_team_stats: _containers.RepeatedCompositeFieldContainer[
            _dota_gcmessages_common_pb2.CMatchTeamTimedStats
        ]
        players: _containers.RepeatedCompositeFieldContainer[CMsgSignOutGameplayStats.CPlayer]
        def __init__(
            self,
            is_winning_team: bool = ...,
            is_radiant_team: bool = ...,
            timed_team_stats: _Iterable[_dota_gcmessages_common_pb2.CMatchTeamTimedStats | _Mapping]
            | None = ...,
            players: _Iterable[CMsgSignOutGameplayStats.CPlayer | _Mapping] | None = ...,
        ) -> None: ...

    TEAMS_FIELD_NUMBER: _ClassVar[int]
    teams: _containers.RepeatedCompositeFieldContainer[CMsgSignOutGameplayStats.CTeam]
    def __init__(
        self, teams: _Iterable[CMsgSignOutGameplayStats.CTeam | _Mapping] | None = ...
    ) -> None: ...

class CMsgGameMatchSignOut(_message.Message):
    __slots__ = (
        "match_id",
        "duration",
        "good_guys_win",
        "date",
        "teams",
        "tower_status",
        "barracks_status",
        "cluster",
        "server_addr",
        "first_blood_time",
        "event_score",
        "fantasy_stats",
        "player_strange_count_adjustments",
        "automatic_surrender",
        "server_version",
        "poor_network_conditions",
        "additional_msgs",
        "social_feed_events",
        "average_networth_delta",
        "custom_game_data",
        "match_flags",
        "team_scores",
        "pre_game_duration",
        "event_game_leaderboard_entries",
        "ward_placements",
        "gameplay_stats",
        "extra_messages",
        "winning_team",
        "normalized_win_probability_diff",
        "match_tracked_stats",
    )
    class CTeam(_message.Message):
        __slots__ = ("players", "team_tracked_stats")
        class CPlayer(_message.Message):
            __slots__ = (
                "steam_id",
                "hero_id",
                "items",
                "item_purchase_times",
                "gold",
                "kills",
                "deaths",
                "assists",
                "leaver_status",
                "last_hits",
                "denies",
                "gold_per_min",
                "xp_per_minute",
                "gold_spent",
                "level",
                "scaled_hero_damage",
                "scaled_tower_damage",
                "scaled_hero_healing",
                "time_last_seen",
                "support_ability_value",
                "party_id",
                "claimed_farm_gold",
                "support_gold",
                "claimed_denies",
                "claimed_misses",
                "misses",
                "net_worth",
                "hero_damage",
                "tower_damage",
                "hero_healing",
                "ability_upgrades",
                "additional_units_inventory",
                "permanent_buffs",
                "custom_game_data",
                "match_player_flags",
                "talent_ability_ids",
                "hero_pick_order",
                "hero_was_randomed",
                "hero_was_dota_plus_suggestion",
                "lane",
                "is_using_plus_guide",
                "hero_damage_received",
                "hero_damage_dealt",
                "seconds_dead",
                "gold_lost_to_death",
                "command_count",
                "mouse_click_cast_command_count",
                "teleports_used",
                "cavern_crawl_preferred_map_variant",
                "bounty_runes",
                "outposts_captured",
                "dewards",
                "wards_placed",
                "camps_stacked",
                "player_slot",
                "predicted_position",
                "lane_outcomes",
                "friendly_t1_destroyed_time",
                "enemy_t1_destroyed_time",
                "friendly_roshan_kills",
                "enemy_roshan_kills",
                "power_runes",
                "water_runes",
                "stun_duration",
                "team_number",
                "team_slot",
                "time_purchased_shard",
                "time_purchased_aghs",
                "ability_draft_abilities",
                "player_tracked_stats",
                "predicted_rank",
                "selected_facet",
                "enhancement_level",
                "disable_duration",
            )
            class HeroDamageType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                HERO_DAMAGE_PHYSICAL: _ClassVar[CMsgGameMatchSignOut.CTeam.CPlayer.HeroDamageType]
                HERO_DAMAGE_MAGICAL: _ClassVar[CMsgGameMatchSignOut.CTeam.CPlayer.HeroDamageType]
                HERO_DAMAGE_PURE: _ClassVar[CMsgGameMatchSignOut.CTeam.CPlayer.HeroDamageType]

            HERO_DAMAGE_PHYSICAL: CMsgGameMatchSignOut.CTeam.CPlayer.HeroDamageType
            HERO_DAMAGE_MAGICAL: CMsgGameMatchSignOut.CTeam.CPlayer.HeroDamageType
            HERO_DAMAGE_PURE: CMsgGameMatchSignOut.CTeam.CPlayer.HeroDamageType
            class CCustomGameData(_message.Message):
                __slots__ = ("dota_team", "winner")
                DOTA_TEAM_FIELD_NUMBER: _ClassVar[int]
                WINNER_FIELD_NUMBER: _ClassVar[int]
                dota_team: int
                winner: bool
                def __init__(self, dota_team: int | None = ..., winner: bool = ...) -> None: ...

            class HeroDamageReceived(_message.Message):
                __slots__ = ("pre_reduction", "post_reduction", "damage_type")
                PRE_REDUCTION_FIELD_NUMBER: _ClassVar[int]
                POST_REDUCTION_FIELD_NUMBER: _ClassVar[int]
                DAMAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
                pre_reduction: int
                post_reduction: int
                damage_type: CMsgGameMatchSignOut.CTeam.CPlayer.HeroDamageType
                def __init__(
                    self,
                    pre_reduction: int | None = ...,
                    post_reduction: int | None = ...,
                    damage_type: CMsgGameMatchSignOut.CTeam.CPlayer.HeroDamageType
                    | str
                    | None = ...,
                ) -> None: ...

            STEAM_ID_FIELD_NUMBER: _ClassVar[int]
            HERO_ID_FIELD_NUMBER: _ClassVar[int]
            ITEMS_FIELD_NUMBER: _ClassVar[int]
            ITEM_PURCHASE_TIMES_FIELD_NUMBER: _ClassVar[int]
            GOLD_FIELD_NUMBER: _ClassVar[int]
            KILLS_FIELD_NUMBER: _ClassVar[int]
            DEATHS_FIELD_NUMBER: _ClassVar[int]
            ASSISTS_FIELD_NUMBER: _ClassVar[int]
            LEAVER_STATUS_FIELD_NUMBER: _ClassVar[int]
            LAST_HITS_FIELD_NUMBER: _ClassVar[int]
            DENIES_FIELD_NUMBER: _ClassVar[int]
            GOLD_PER_MIN_FIELD_NUMBER: _ClassVar[int]
            XP_PER_MINUTE_FIELD_NUMBER: _ClassVar[int]
            GOLD_SPENT_FIELD_NUMBER: _ClassVar[int]
            LEVEL_FIELD_NUMBER: _ClassVar[int]
            SCALED_HERO_DAMAGE_FIELD_NUMBER: _ClassVar[int]
            SCALED_TOWER_DAMAGE_FIELD_NUMBER: _ClassVar[int]
            SCALED_HERO_HEALING_FIELD_NUMBER: _ClassVar[int]
            TIME_LAST_SEEN_FIELD_NUMBER: _ClassVar[int]
            SUPPORT_ABILITY_VALUE_FIELD_NUMBER: _ClassVar[int]
            PARTY_ID_FIELD_NUMBER: _ClassVar[int]
            CLAIMED_FARM_GOLD_FIELD_NUMBER: _ClassVar[int]
            SUPPORT_GOLD_FIELD_NUMBER: _ClassVar[int]
            CLAIMED_DENIES_FIELD_NUMBER: _ClassVar[int]
            CLAIMED_MISSES_FIELD_NUMBER: _ClassVar[int]
            MISSES_FIELD_NUMBER: _ClassVar[int]
            NET_WORTH_FIELD_NUMBER: _ClassVar[int]
            HERO_DAMAGE_FIELD_NUMBER: _ClassVar[int]
            TOWER_DAMAGE_FIELD_NUMBER: _ClassVar[int]
            HERO_HEALING_FIELD_NUMBER: _ClassVar[int]
            ABILITY_UPGRADES_FIELD_NUMBER: _ClassVar[int]
            ADDITIONAL_UNITS_INVENTORY_FIELD_NUMBER: _ClassVar[int]
            PERMANENT_BUFFS_FIELD_NUMBER: _ClassVar[int]
            CUSTOM_GAME_DATA_FIELD_NUMBER: _ClassVar[int]
            MATCH_PLAYER_FLAGS_FIELD_NUMBER: _ClassVar[int]
            TALENT_ABILITY_IDS_FIELD_NUMBER: _ClassVar[int]
            HERO_PICK_ORDER_FIELD_NUMBER: _ClassVar[int]
            HERO_WAS_RANDOMED_FIELD_NUMBER: _ClassVar[int]
            HERO_WAS_DOTA_PLUS_SUGGESTION_FIELD_NUMBER: _ClassVar[int]
            LANE_FIELD_NUMBER: _ClassVar[int]
            IS_USING_PLUS_GUIDE_FIELD_NUMBER: _ClassVar[int]
            HERO_DAMAGE_RECEIVED_FIELD_NUMBER: _ClassVar[int]
            HERO_DAMAGE_DEALT_FIELD_NUMBER: _ClassVar[int]
            SECONDS_DEAD_FIELD_NUMBER: _ClassVar[int]
            GOLD_LOST_TO_DEATH_FIELD_NUMBER: _ClassVar[int]
            COMMAND_COUNT_FIELD_NUMBER: _ClassVar[int]
            MOUSE_CLICK_CAST_COMMAND_COUNT_FIELD_NUMBER: _ClassVar[int]
            TELEPORTS_USED_FIELD_NUMBER: _ClassVar[int]
            CAVERN_CRAWL_PREFERRED_MAP_VARIANT_FIELD_NUMBER: _ClassVar[int]
            BOUNTY_RUNES_FIELD_NUMBER: _ClassVar[int]
            OUTPOSTS_CAPTURED_FIELD_NUMBER: _ClassVar[int]
            DEWARDS_FIELD_NUMBER: _ClassVar[int]
            WARDS_PLACED_FIELD_NUMBER: _ClassVar[int]
            CAMPS_STACKED_FIELD_NUMBER: _ClassVar[int]
            PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
            PREDICTED_POSITION_FIELD_NUMBER: _ClassVar[int]
            LANE_OUTCOMES_FIELD_NUMBER: _ClassVar[int]
            FRIENDLY_T1_DESTROYED_TIME_FIELD_NUMBER: _ClassVar[int]
            ENEMY_T1_DESTROYED_TIME_FIELD_NUMBER: _ClassVar[int]
            FRIENDLY_ROSHAN_KILLS_FIELD_NUMBER: _ClassVar[int]
            ENEMY_ROSHAN_KILLS_FIELD_NUMBER: _ClassVar[int]
            POWER_RUNES_FIELD_NUMBER: _ClassVar[int]
            WATER_RUNES_FIELD_NUMBER: _ClassVar[int]
            STUN_DURATION_FIELD_NUMBER: _ClassVar[int]
            TEAM_NUMBER_FIELD_NUMBER: _ClassVar[int]
            TEAM_SLOT_FIELD_NUMBER: _ClassVar[int]
            TIME_PURCHASED_SHARD_FIELD_NUMBER: _ClassVar[int]
            TIME_PURCHASED_AGHS_FIELD_NUMBER: _ClassVar[int]
            ABILITY_DRAFT_ABILITIES_FIELD_NUMBER: _ClassVar[int]
            PLAYER_TRACKED_STATS_FIELD_NUMBER: _ClassVar[int]
            PREDICTED_RANK_FIELD_NUMBER: _ClassVar[int]
            SELECTED_FACET_FIELD_NUMBER: _ClassVar[int]
            ENHANCEMENT_LEVEL_FIELD_NUMBER: _ClassVar[int]
            DISABLE_DURATION_FIELD_NUMBER: _ClassVar[int]
            steam_id: int
            hero_id: int
            items: _containers.RepeatedScalarFieldContainer[int]
            item_purchase_times: _containers.RepeatedScalarFieldContainer[int]
            gold: int
            kills: int
            deaths: int
            assists: int
            leaver_status: int
            last_hits: int
            denies: int
            gold_per_min: int
            xp_per_minute: int
            gold_spent: int
            level: int
            scaled_hero_damage: int
            scaled_tower_damage: int
            scaled_hero_healing: int
            time_last_seen: int
            support_ability_value: int
            party_id: int
            claimed_farm_gold: int
            support_gold: int
            claimed_denies: int
            claimed_misses: int
            misses: int
            net_worth: int
            hero_damage: int
            tower_damage: int
            hero_healing: int
            ability_upgrades: _containers.RepeatedCompositeFieldContainer[
                _dota_gcmessages_common_pb2.CMatchPlayerAbilityUpgrade
            ]
            additional_units_inventory: _containers.RepeatedCompositeFieldContainer[
                _dota_gcmessages_common_pb2.CMatchAdditionalUnitInventory
            ]
            permanent_buffs: _containers.RepeatedCompositeFieldContainer[
                _dota_gcmessages_common_pb2.CMatchPlayerPermanentBuff
            ]
            custom_game_data: CMsgGameMatchSignOut.CTeam.CPlayer.CCustomGameData
            match_player_flags: int
            talent_ability_ids: _containers.RepeatedScalarFieldContainer[int]
            hero_pick_order: int
            hero_was_randomed: bool
            hero_was_dota_plus_suggestion: bool
            lane: int
            is_using_plus_guide: bool
            hero_damage_received: _containers.RepeatedCompositeFieldContainer[
                CMsgGameMatchSignOut.CTeam.CPlayer.HeroDamageReceived
            ]
            hero_damage_dealt: _containers.RepeatedCompositeFieldContainer[
                CMsgGameMatchSignOut.CTeam.CPlayer.HeroDamageReceived
            ]
            seconds_dead: int
            gold_lost_to_death: int
            command_count: int
            mouse_click_cast_command_count: int
            teleports_used: int
            cavern_crawl_preferred_map_variant: int
            bounty_runes: int
            outposts_captured: int
            dewards: int
            wards_placed: int
            camps_stacked: int
            player_slot: int
            predicted_position: int
            lane_outcomes: int
            friendly_t1_destroyed_time: int
            enemy_t1_destroyed_time: int
            friendly_roshan_kills: int
            enemy_roshan_kills: int
            power_runes: int
            water_runes: int
            stun_duration: float
            team_number: _dota_shared_enums_pb2.DOTA_GC_TEAM
            team_slot: int
            time_purchased_shard: int
            time_purchased_aghs: int
            ability_draft_abilities: _containers.RepeatedScalarFieldContainer[int]
            player_tracked_stats: _containers.RepeatedCompositeFieldContainer[
                _dota_gcmessages_common_pb2.CMsgTrackedStat
            ]
            predicted_rank: int
            selected_facet: int
            enhancement_level: int
            disable_duration: int
            def __init__(
                self,
                steam_id: int | None = ...,
                hero_id: int | None = ...,
                items: _Iterable[int] | None = ...,
                item_purchase_times: _Iterable[int] | None = ...,
                gold: int | None = ...,
                kills: int | None = ...,
                deaths: int | None = ...,
                assists: int | None = ...,
                leaver_status: int | None = ...,
                last_hits: int | None = ...,
                denies: int | None = ...,
                gold_per_min: int | None = ...,
                xp_per_minute: int | None = ...,
                gold_spent: int | None = ...,
                level: int | None = ...,
                scaled_hero_damage: int | None = ...,
                scaled_tower_damage: int | None = ...,
                scaled_hero_healing: int | None = ...,
                time_last_seen: int | None = ...,
                support_ability_value: int | None = ...,
                party_id: int | None = ...,
                claimed_farm_gold: int | None = ...,
                support_gold: int | None = ...,
                claimed_denies: int | None = ...,
                claimed_misses: int | None = ...,
                misses: int | None = ...,
                net_worth: int | None = ...,
                hero_damage: int | None = ...,
                tower_damage: int | None = ...,
                hero_healing: int | None = ...,
                ability_upgrades: _Iterable[
                    _dota_gcmessages_common_pb2.CMatchPlayerAbilityUpgrade | _Mapping
                ]
                | None = ...,
                additional_units_inventory: _Iterable[
                    _dota_gcmessages_common_pb2.CMatchAdditionalUnitInventory | _Mapping
                ]
                | None = ...,
                permanent_buffs: _Iterable[
                    _dota_gcmessages_common_pb2.CMatchPlayerPermanentBuff | _Mapping
                ]
                | None = ...,
                custom_game_data: CMsgGameMatchSignOut.CTeam.CPlayer.CCustomGameData
                | _Mapping
                | None = ...,
                match_player_flags: int | None = ...,
                talent_ability_ids: _Iterable[int] | None = ...,
                hero_pick_order: int | None = ...,
                hero_was_randomed: bool = ...,
                hero_was_dota_plus_suggestion: bool = ...,
                lane: int | None = ...,
                is_using_plus_guide: bool = ...,
                hero_damage_received: _Iterable[
                    CMsgGameMatchSignOut.CTeam.CPlayer.HeroDamageReceived | _Mapping
                ]
                | None = ...,
                hero_damage_dealt: _Iterable[
                    CMsgGameMatchSignOut.CTeam.CPlayer.HeroDamageReceived | _Mapping
                ]
                | None = ...,
                seconds_dead: int | None = ...,
                gold_lost_to_death: int | None = ...,
                command_count: int | None = ...,
                mouse_click_cast_command_count: int | None = ...,
                teleports_used: int | None = ...,
                cavern_crawl_preferred_map_variant: int | None = ...,
                bounty_runes: int | None = ...,
                outposts_captured: int | None = ...,
                dewards: int | None = ...,
                wards_placed: int | None = ...,
                camps_stacked: int | None = ...,
                player_slot: int | None = ...,
                predicted_position: int | None = ...,
                lane_outcomes: int | None = ...,
                friendly_t1_destroyed_time: int | None = ...,
                enemy_t1_destroyed_time: int | None = ...,
                friendly_roshan_kills: int | None = ...,
                enemy_roshan_kills: int | None = ...,
                power_runes: int | None = ...,
                water_runes: int | None = ...,
                stun_duration: float | None = ...,
                team_number: _dota_shared_enums_pb2.DOTA_GC_TEAM | str | None = ...,
                team_slot: int | None = ...,
                time_purchased_shard: int | None = ...,
                time_purchased_aghs: int | None = ...,
                ability_draft_abilities: _Iterable[int] | None = ...,
                player_tracked_stats: _Iterable[
                    _dota_gcmessages_common_pb2.CMsgTrackedStat | _Mapping
                ]
                | None = ...,
                predicted_rank: int | None = ...,
                selected_facet: int | None = ...,
                enhancement_level: int | None = ...,
                disable_duration: int | None = ...,
            ) -> None: ...

        PLAYERS_FIELD_NUMBER: _ClassVar[int]
        TEAM_TRACKED_STATS_FIELD_NUMBER: _ClassVar[int]
        players: _containers.RepeatedCompositeFieldContainer[CMsgGameMatchSignOut.CTeam.CPlayer]
        team_tracked_stats: _containers.RepeatedCompositeFieldContainer[
            _dota_gcmessages_common_pb2.CMsgTrackedStat
        ]
        def __init__(
            self,
            players: _Iterable[CMsgGameMatchSignOut.CTeam.CPlayer | _Mapping] | None = ...,
            team_tracked_stats: _Iterable[_dota_gcmessages_common_pb2.CMsgTrackedStat | _Mapping]
            | None = ...,
        ) -> None: ...

    class CAdditionalSignoutMsg(_message.Message):
        __slots__ = ("id", "contents")
        ID_FIELD_NUMBER: _ClassVar[int]
        CONTENTS_FIELD_NUMBER: _ClassVar[int]
        id: int
        contents: bytes
        def __init__(self, id: int | None = ..., contents: bytes | None = ...) -> None: ...

    class CSocialFeedMatchEvent(_message.Message):
        __slots__ = ("account_id", "timestamp", "event_type", "game_time", "replay_time")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
        GAME_TIME_FIELD_NUMBER: _ClassVar[int]
        REPLAY_TIME_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        timestamp: int
        event_type: int
        game_time: int
        replay_time: int
        def __init__(
            self,
            account_id: int | None = ...,
            timestamp: int | None = ...,
            event_type: int | None = ...,
            game_time: int | None = ...,
            replay_time: int | None = ...,
        ) -> None: ...

    class CCustomGameData(_message.Message):
        __slots__ = ("publish_timestamp",)
        PUBLISH_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        publish_timestamp: int
        def __init__(self, publish_timestamp: int | None = ...) -> None: ...

    class EventGameLeaderboardEntry(_message.Message):
        __slots__ = (
            "name_suffix",
            "score",
            "extra_data_1",
            "extra_data_2",
            "extra_data_3",
            "extra_data_4",
            "extra_data_5",
        )
        NAME_SUFFIX_FIELD_NUMBER: _ClassVar[int]
        SCORE_FIELD_NUMBER: _ClassVar[int]
        EXTRA_DATA_1_FIELD_NUMBER: _ClassVar[int]
        EXTRA_DATA_2_FIELD_NUMBER: _ClassVar[int]
        EXTRA_DATA_3_FIELD_NUMBER: _ClassVar[int]
        EXTRA_DATA_4_FIELD_NUMBER: _ClassVar[int]
        EXTRA_DATA_5_FIELD_NUMBER: _ClassVar[int]
        name_suffix: str
        score: int
        extra_data_1: int
        extra_data_2: int
        extra_data_3: int
        extra_data_4: int
        extra_data_5: int
        def __init__(
            self,
            name_suffix: str | None = ...,
            score: int | None = ...,
            extra_data_1: int | None = ...,
            extra_data_2: int | None = ...,
            extra_data_3: int | None = ...,
            extra_data_4: int | None = ...,
            extra_data_5: int | None = ...,
        ) -> None: ...

    class WardPlacement(_message.Message):
        __slots__ = (
            "player_id",
            "team_id",
            "placed_time",
            "building_state",
            "creep_state",
            "roshan_alive",
            "position_x",
            "position_y",
        )
        PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
        TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        PLACED_TIME_FIELD_NUMBER: _ClassVar[int]
        BUILDING_STATE_FIELD_NUMBER: _ClassVar[int]
        CREEP_STATE_FIELD_NUMBER: _ClassVar[int]
        ROSHAN_ALIVE_FIELD_NUMBER: _ClassVar[int]
        POSITION_X_FIELD_NUMBER: _ClassVar[int]
        POSITION_Y_FIELD_NUMBER: _ClassVar[int]
        player_id: int
        team_id: int
        placed_time: int
        building_state: int
        creep_state: int
        roshan_alive: bool
        position_x: int
        position_y: int
        def __init__(
            self,
            player_id: int | None = ...,
            team_id: int | None = ...,
            placed_time: int | None = ...,
            building_state: int | None = ...,
            creep_state: int | None = ...,
            roshan_alive: bool = ...,
            position_x: int | None = ...,
            position_y: int | None = ...,
        ) -> None: ...

    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    GOOD_GUYS_WIN_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    TEAMS_FIELD_NUMBER: _ClassVar[int]
    TOWER_STATUS_FIELD_NUMBER: _ClassVar[int]
    BARRACKS_STATUS_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_FIELD_NUMBER: _ClassVar[int]
    SERVER_ADDR_FIELD_NUMBER: _ClassVar[int]
    FIRST_BLOOD_TIME_FIELD_NUMBER: _ClassVar[int]
    EVENT_SCORE_FIELD_NUMBER: _ClassVar[int]
    FANTASY_STATS_FIELD_NUMBER: _ClassVar[int]
    PLAYER_STRANGE_COUNT_ADJUSTMENTS_FIELD_NUMBER: _ClassVar[int]
    AUTOMATIC_SURRENDER_FIELD_NUMBER: _ClassVar[int]
    SERVER_VERSION_FIELD_NUMBER: _ClassVar[int]
    POOR_NETWORK_CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_MSGS_FIELD_NUMBER: _ClassVar[int]
    SOCIAL_FEED_EVENTS_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_NETWORTH_DELTA_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_DATA_FIELD_NUMBER: _ClassVar[int]
    MATCH_FLAGS_FIELD_NUMBER: _ClassVar[int]
    TEAM_SCORES_FIELD_NUMBER: _ClassVar[int]
    PRE_GAME_DURATION_FIELD_NUMBER: _ClassVar[int]
    EVENT_GAME_LEADERBOARD_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    WARD_PLACEMENTS_FIELD_NUMBER: _ClassVar[int]
    GAMEPLAY_STATS_FIELD_NUMBER: _ClassVar[int]
    EXTRA_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    WINNING_TEAM_FIELD_NUMBER: _ClassVar[int]
    NORMALIZED_WIN_PROBABILITY_DIFF_FIELD_NUMBER: _ClassVar[int]
    MATCH_TRACKED_STATS_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    duration: int
    good_guys_win: bool
    date: int
    teams: _containers.RepeatedCompositeFieldContainer[CMsgGameMatchSignOut.CTeam]
    tower_status: _containers.RepeatedScalarFieldContainer[int]
    barracks_status: _containers.RepeatedScalarFieldContainer[int]
    cluster: int
    server_addr: str
    first_blood_time: int
    event_score: int
    fantasy_stats: _containers.RepeatedCompositeFieldContainer[
        _dota_gcmessages_common_pb2.CMsgDOTAFantasyPlayerStats
    ]
    player_strange_count_adjustments: _containers.RepeatedCompositeFieldContainer[
        _econ_gcmessages_pb2.CMsgEconPlayerStrangeCountAdjustment
    ]
    automatic_surrender: bool
    server_version: int
    poor_network_conditions: CMsgPoorNetworkConditions
    additional_msgs: _containers.RepeatedCompositeFieldContainer[
        CMsgGameMatchSignOut.CAdditionalSignoutMsg
    ]
    social_feed_events: _containers.RepeatedCompositeFieldContainer[
        CMsgGameMatchSignOut.CSocialFeedMatchEvent
    ]
    average_networth_delta: int
    custom_game_data: CMsgGameMatchSignOut.CCustomGameData
    match_flags: int
    team_scores: _containers.RepeatedScalarFieldContainer[int]
    pre_game_duration: int
    event_game_leaderboard_entries: _containers.RepeatedCompositeFieldContainer[
        CMsgGameMatchSignOut.EventGameLeaderboardEntry
    ]
    ward_placements: _containers.RepeatedCompositeFieldContainer[CMsgGameMatchSignOut.WardPlacement]
    gameplay_stats: CMsgSignOutGameplayStats
    extra_messages: _containers.RepeatedCompositeFieldContainer[
        _gcsdk_gcmessages_pb2.CExtraMsgBlock
    ]
    winning_team: _dota_shared_enums_pb2.DOTA_GC_TEAM
    normalized_win_probability_diff: float
    match_tracked_stats: _containers.RepeatedCompositeFieldContainer[
        _dota_gcmessages_common_pb2.CMsgTrackedStat
    ]
    def __init__(
        self,
        match_id: int | None = ...,
        duration: int | None = ...,
        good_guys_win: bool = ...,
        date: int | None = ...,
        teams: _Iterable[CMsgGameMatchSignOut.CTeam | _Mapping] | None = ...,
        tower_status: _Iterable[int] | None = ...,
        barracks_status: _Iterable[int] | None = ...,
        cluster: int | None = ...,
        server_addr: str | None = ...,
        first_blood_time: int | None = ...,
        event_score: int | None = ...,
        fantasy_stats: _Iterable[_dota_gcmessages_common_pb2.CMsgDOTAFantasyPlayerStats | _Mapping]
        | None = ...,
        player_strange_count_adjustments: _Iterable[
            _econ_gcmessages_pb2.CMsgEconPlayerStrangeCountAdjustment | _Mapping
        ]
        | None = ...,
        automatic_surrender: bool = ...,
        server_version: int | None = ...,
        poor_network_conditions: CMsgPoorNetworkConditions | _Mapping | None = ...,
        additional_msgs: _Iterable[CMsgGameMatchSignOut.CAdditionalSignoutMsg | _Mapping]
        | None = ...,
        social_feed_events: _Iterable[CMsgGameMatchSignOut.CSocialFeedMatchEvent | _Mapping]
        | None = ...,
        average_networth_delta: int | None = ...,
        custom_game_data: CMsgGameMatchSignOut.CCustomGameData | _Mapping | None = ...,
        match_flags: int | None = ...,
        team_scores: _Iterable[int] | None = ...,
        pre_game_duration: int | None = ...,
        event_game_leaderboard_entries: _Iterable[
            CMsgGameMatchSignOut.EventGameLeaderboardEntry | _Mapping
        ]
        | None = ...,
        ward_placements: _Iterable[CMsgGameMatchSignOut.WardPlacement | _Mapping] | None = ...,
        gameplay_stats: CMsgSignOutGameplayStats | _Mapping | None = ...,
        extra_messages: _Iterable[_gcsdk_gcmessages_pb2.CExtraMsgBlock | _Mapping] | None = ...,
        winning_team: _dota_shared_enums_pb2.DOTA_GC_TEAM | str | None = ...,
        normalized_win_probability_diff: float | None = ...,
        match_tracked_stats: _Iterable[_dota_gcmessages_common_pb2.CMsgTrackedStat | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgSignOutDraftInfo(_message.Message):
    __slots__ = ("radiant_captain_account_id", "dire_captain_account_id", "picks_bans")
    RADIANT_CAPTAIN_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    DIRE_CAPTAIN_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    PICKS_BANS_FIELD_NUMBER: _ClassVar[int]
    radiant_captain_account_id: int
    dire_captain_account_id: int
    picks_bans: _containers.RepeatedCompositeFieldContainer[
        _dota_gcmessages_common_pb2.CMatchHeroSelectEvent
    ]
    def __init__(
        self,
        radiant_captain_account_id: int | None = ...,
        dire_captain_account_id: int | None = ...,
        picks_bans: _Iterable[_dota_gcmessages_common_pb2.CMatchHeroSelectEvent | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgSignOutBotInfo(_message.Message):
    __slots__ = ("allow_cheats", "bot_difficulty_radiant", "created_lobby", "bot_difficulty_dire")
    ALLOW_CHEATS_FIELD_NUMBER: _ClassVar[int]
    BOT_DIFFICULTY_RADIANT_FIELD_NUMBER: _ClassVar[int]
    CREATED_LOBBY_FIELD_NUMBER: _ClassVar[int]
    BOT_DIFFICULTY_DIRE_FIELD_NUMBER: _ClassVar[int]
    allow_cheats: bool
    bot_difficulty_radiant: _dota_shared_enums_pb2.DOTABotDifficulty
    created_lobby: bool
    bot_difficulty_dire: _dota_shared_enums_pb2.DOTABotDifficulty
    def __init__(
        self,
        allow_cheats: bool = ...,
        bot_difficulty_radiant: _dota_shared_enums_pb2.DOTABotDifficulty | str | None = ...,
        created_lobby: bool = ...,
        bot_difficulty_dire: _dota_shared_enums_pb2.DOTABotDifficulty | str | None = ...,
    ) -> None: ...

class CMsgSignOutTextMuteInfo(_message.Message):
    __slots__ = ("text_mute_messages",)
    class TextMuteMessage(_message.Message):
        __slots__ = ("region", "caused_text_mute", "chat_message")
        REGION_FIELD_NUMBER: _ClassVar[int]
        CAUSED_TEXT_MUTE_FIELD_NUMBER: _ClassVar[int]
        CHAT_MESSAGE_FIELD_NUMBER: _ClassVar[int]
        region: int
        caused_text_mute: bool
        chat_message: str
        def __init__(
            self,
            region: int | None = ...,
            caused_text_mute: bool = ...,
            chat_message: str | None = ...,
        ) -> None: ...

    TEXT_MUTE_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    text_mute_messages: _containers.RepeatedCompositeFieldContainer[
        CMsgSignOutTextMuteInfo.TextMuteMessage
    ]
    def __init__(
        self,
        text_mute_messages: _Iterable[CMsgSignOutTextMuteInfo.TextMuteMessage | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgSignOutPlayerStats(_message.Message):
    __slots__ = (
        "account_id",
        "match_id",
        "rank",
        "hero_id",
        "rampages",
        "triple_kills",
        "first_blood_claimed",
        "first_blood_given",
        "couriers_killed",
        "aegises_snatched",
        "cheeses_eaten",
        "creeps_stacked",
        "fight_score",
        "farm_score",
        "support_score",
        "push_score",
        "kills",
        "deaths",
        "assists",
        "last_hits",
        "denies",
        "gpm",
        "xppm",
        "net_worth",
        "damage",
        "heals",
        "rapiers_purchased",
        "observer_wards_placed",
        "wards_destroyed",
        "lobby_type",
    )
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    RAMPAGES_FIELD_NUMBER: _ClassVar[int]
    TRIPLE_KILLS_FIELD_NUMBER: _ClassVar[int]
    FIRST_BLOOD_CLAIMED_FIELD_NUMBER: _ClassVar[int]
    FIRST_BLOOD_GIVEN_FIELD_NUMBER: _ClassVar[int]
    COURIERS_KILLED_FIELD_NUMBER: _ClassVar[int]
    AEGISES_SNATCHED_FIELD_NUMBER: _ClassVar[int]
    CHEESES_EATEN_FIELD_NUMBER: _ClassVar[int]
    CREEPS_STACKED_FIELD_NUMBER: _ClassVar[int]
    FIGHT_SCORE_FIELD_NUMBER: _ClassVar[int]
    FARM_SCORE_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_SCORE_FIELD_NUMBER: _ClassVar[int]
    PUSH_SCORE_FIELD_NUMBER: _ClassVar[int]
    KILLS_FIELD_NUMBER: _ClassVar[int]
    DEATHS_FIELD_NUMBER: _ClassVar[int]
    ASSISTS_FIELD_NUMBER: _ClassVar[int]
    LAST_HITS_FIELD_NUMBER: _ClassVar[int]
    DENIES_FIELD_NUMBER: _ClassVar[int]
    GPM_FIELD_NUMBER: _ClassVar[int]
    XPPM_FIELD_NUMBER: _ClassVar[int]
    NET_WORTH_FIELD_NUMBER: _ClassVar[int]
    DAMAGE_FIELD_NUMBER: _ClassVar[int]
    HEALS_FIELD_NUMBER: _ClassVar[int]
    RAPIERS_PURCHASED_FIELD_NUMBER: _ClassVar[int]
    OBSERVER_WARDS_PLACED_FIELD_NUMBER: _ClassVar[int]
    WARDS_DESTROYED_FIELD_NUMBER: _ClassVar[int]
    LOBBY_TYPE_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    match_id: int
    rank: int
    hero_id: int
    rampages: int
    triple_kills: int
    first_blood_claimed: int
    first_blood_given: int
    couriers_killed: int
    aegises_snatched: int
    cheeses_eaten: int
    creeps_stacked: int
    fight_score: float
    farm_score: float
    support_score: float
    push_score: float
    kills: int
    deaths: int
    assists: int
    last_hits: int
    denies: int
    gpm: float
    xppm: float
    net_worth: float
    damage: float
    heals: float
    rapiers_purchased: int
    observer_wards_placed: int
    wards_destroyed: int
    lobby_type: int
    def __init__(
        self,
        account_id: int | None = ...,
        match_id: int | None = ...,
        rank: int | None = ...,
        hero_id: int | None = ...,
        rampages: int | None = ...,
        triple_kills: int | None = ...,
        first_blood_claimed: int | None = ...,
        first_blood_given: int | None = ...,
        couriers_killed: int | None = ...,
        aegises_snatched: int | None = ...,
        cheeses_eaten: int | None = ...,
        creeps_stacked: int | None = ...,
        fight_score: float | None = ...,
        farm_score: float | None = ...,
        support_score: float | None = ...,
        push_score: float | None = ...,
        kills: int | None = ...,
        deaths: int | None = ...,
        assists: int | None = ...,
        last_hits: int | None = ...,
        denies: int | None = ...,
        gpm: float | None = ...,
        xppm: float | None = ...,
        net_worth: float | None = ...,
        damage: float | None = ...,
        heals: float | None = ...,
        rapiers_purchased: int | None = ...,
        observer_wards_placed: int | None = ...,
        wards_destroyed: int | None = ...,
        lobby_type: int | None = ...,
    ) -> None: ...

class CMsgSignOutCommunicationSummary(_message.Message):
    __slots__ = ("players",)
    class PlayerCommunication(_message.Message):
        __slots__ = (
            "account_id",
            "pings",
            "max_pings_per_interval",
            "teammate_pings",
            "max_teammate_pings_per_interval",
            "team_chat_messages",
            "all_chat_messages",
            "chat_wheel_messages",
            "pauses",
            "unpauses",
            "lines_drawn",
            "voice_chat_seconds",
            "chat_mutes",
            "voice_mutes",
            "ping_details",
            "comms_blocks_solo",
            "comms_blocks_mass",
            "chat_log",
        )
        class PingDetail(_message.Message):
            __slots__ = ("type", "count")
            TYPE_FIELD_NUMBER: _ClassVar[int]
            COUNT_FIELD_NUMBER: _ClassVar[int]
            type: int
            count: int
            def __init__(self, type: int | None = ..., count: int | None = ...) -> None: ...

        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        PINGS_FIELD_NUMBER: _ClassVar[int]
        MAX_PINGS_PER_INTERVAL_FIELD_NUMBER: _ClassVar[int]
        TEAMMATE_PINGS_FIELD_NUMBER: _ClassVar[int]
        MAX_TEAMMATE_PINGS_PER_INTERVAL_FIELD_NUMBER: _ClassVar[int]
        TEAM_CHAT_MESSAGES_FIELD_NUMBER: _ClassVar[int]
        ALL_CHAT_MESSAGES_FIELD_NUMBER: _ClassVar[int]
        CHAT_WHEEL_MESSAGES_FIELD_NUMBER: _ClassVar[int]
        PAUSES_FIELD_NUMBER: _ClassVar[int]
        UNPAUSES_FIELD_NUMBER: _ClassVar[int]
        LINES_DRAWN_FIELD_NUMBER: _ClassVar[int]
        VOICE_CHAT_SECONDS_FIELD_NUMBER: _ClassVar[int]
        CHAT_MUTES_FIELD_NUMBER: _ClassVar[int]
        VOICE_MUTES_FIELD_NUMBER: _ClassVar[int]
        PING_DETAILS_FIELD_NUMBER: _ClassVar[int]
        COMMS_BLOCKS_SOLO_FIELD_NUMBER: _ClassVar[int]
        COMMS_BLOCKS_MASS_FIELD_NUMBER: _ClassVar[int]
        CHAT_LOG_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        pings: int
        max_pings_per_interval: int
        teammate_pings: int
        max_teammate_pings_per_interval: int
        team_chat_messages: int
        all_chat_messages: int
        chat_wheel_messages: int
        pauses: int
        unpauses: int
        lines_drawn: int
        voice_chat_seconds: int
        chat_mutes: int
        voice_mutes: int
        ping_details: _containers.RepeatedCompositeFieldContainer[
            CMsgSignOutCommunicationSummary.PlayerCommunication.PingDetail
        ]
        comms_blocks_solo: int
        comms_blocks_mass: int
        chat_log: _containers.RepeatedScalarFieldContainer[str]
        def __init__(
            self,
            account_id: int | None = ...,
            pings: int | None = ...,
            max_pings_per_interval: int | None = ...,
            teammate_pings: int | None = ...,
            max_teammate_pings_per_interval: int | None = ...,
            team_chat_messages: int | None = ...,
            all_chat_messages: int | None = ...,
            chat_wheel_messages: int | None = ...,
            pauses: int | None = ...,
            unpauses: int | None = ...,
            lines_drawn: int | None = ...,
            voice_chat_seconds: int | None = ...,
            chat_mutes: int | None = ...,
            voice_mutes: int | None = ...,
            ping_details: _Iterable[
                CMsgSignOutCommunicationSummary.PlayerCommunication.PingDetail | _Mapping
            ]
            | None = ...,
            comms_blocks_solo: int | None = ...,
            comms_blocks_mass: int | None = ...,
            chat_log: _Iterable[str] | None = ...,
        ) -> None: ...

    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    players: _containers.RepeatedCompositeFieldContainer[
        CMsgSignOutCommunicationSummary.PlayerCommunication
    ]
    def __init__(
        self,
        players: _Iterable[CMsgSignOutCommunicationSummary.PlayerCommunication | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgGameMatchSignoutResponse(_message.Message):
    __slots__ = (
        "match_id",
        "replay_salt",
        "leagueid",
        "metadata_private_key",
        "match_details",
        "players_metadata",
        "mvp_data",
        "ow_private_key",
        "ow_salt",
        "ow_replay_id",
        "overworld_rewards",
        "monster_hunter_rewards",
    )
    class PlayerMetadata(_message.Message):
        __slots__ = (
            "hero_id",
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
            "games_played",
        )
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
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
        GAMES_PLAYED_FIELD_NUMBER: _ClassVar[int]
        hero_id: int
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
        games_played: int
        def __init__(
            self,
            hero_id: int | None = ...,
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
            games_played: int | None = ...,
        ) -> None: ...

    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    REPLAY_SALT_FIELD_NUMBER: _ClassVar[int]
    LEAGUEID_FIELD_NUMBER: _ClassVar[int]
    METADATA_PRIVATE_KEY_FIELD_NUMBER: _ClassVar[int]
    MATCH_DETAILS_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_METADATA_FIELD_NUMBER: _ClassVar[int]
    MVP_DATA_FIELD_NUMBER: _ClassVar[int]
    OW_PRIVATE_KEY_FIELD_NUMBER: _ClassVar[int]
    OW_SALT_FIELD_NUMBER: _ClassVar[int]
    OW_REPLAY_ID_FIELD_NUMBER: _ClassVar[int]
    OVERWORLD_REWARDS_FIELD_NUMBER: _ClassVar[int]
    MONSTER_HUNTER_REWARDS_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    replay_salt: int
    leagueid: int
    metadata_private_key: int
    match_details: _dota_gcmessages_common_pb2.CMsgDOTAMatch
    players_metadata: _containers.RepeatedCompositeFieldContainer[
        CMsgGameMatchSignoutResponse.PlayerMetadata
    ]
    mvp_data: _dota_gcmessages_common_match_management_pb2.CMvpData
    ow_private_key: int
    ow_salt: int
    ow_replay_id: int
    overworld_rewards: _dota_gcmessages_common_overworld_pb2.CMsgOverworldMatchRewards
    monster_hunter_rewards: _dota_gcmessages_common_monster_hunter_pb2.CMsgMonsterHunterMatchRewards
    def __init__(
        self,
        match_id: int | None = ...,
        replay_salt: int | None = ...,
        leagueid: int | None = ...,
        metadata_private_key: int | None = ...,
        match_details: _dota_gcmessages_common_pb2.CMsgDOTAMatch | _Mapping | None = ...,
        players_metadata: _Iterable[CMsgGameMatchSignoutResponse.PlayerMetadata | _Mapping]
        | None = ...,
        mvp_data: _dota_gcmessages_common_match_management_pb2.CMvpData | _Mapping | None = ...,
        ow_private_key: int | None = ...,
        ow_salt: int | None = ...,
        ow_replay_id: int | None = ...,
        overworld_rewards: _dota_gcmessages_common_overworld_pb2.CMsgOverworldMatchRewards
        | _Mapping
        | None = ...,
        monster_hunter_rewards: _dota_gcmessages_common_monster_hunter_pb2.CMsgMonsterHunterMatchRewards
        | _Mapping
        | None = ...,
    ) -> None: ...

class CMsgGameMatchSignOutPermissionRequest(_message.Message):
    __slots__ = ("server_version", "local_attempt", "total_attempt", "seconds_waited")
    SERVER_VERSION_FIELD_NUMBER: _ClassVar[int]
    LOCAL_ATTEMPT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_ATTEMPT_FIELD_NUMBER: _ClassVar[int]
    SECONDS_WAITED_FIELD_NUMBER: _ClassVar[int]
    server_version: int
    local_attempt: int
    total_attempt: int
    seconds_waited: int
    def __init__(
        self,
        server_version: int | None = ...,
        local_attempt: int | None = ...,
        total_attempt: int | None = ...,
        seconds_waited: int | None = ...,
    ) -> None: ...

class CMsgGameMatchSignOutPermissionResponse(_message.Message):
    __slots__ = ("permission_granted", "abandon_signout", "retry_delay_seconds")
    PERMISSION_GRANTED_FIELD_NUMBER: _ClassVar[int]
    ABANDON_SIGNOUT_FIELD_NUMBER: _ClassVar[int]
    RETRY_DELAY_SECONDS_FIELD_NUMBER: _ClassVar[int]
    permission_granted: bool
    abandon_signout: bool
    retry_delay_seconds: int
    def __init__(
        self,
        permission_granted: bool = ...,
        abandon_signout: bool = ...,
        retry_delay_seconds: int | None = ...,
    ) -> None: ...

class CMsgGameMatchSignOutEventGameData(_message.Message):
    __slots__ = ("event_id", "game_name", "map_name", "event_game_data", "start_time")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    GAME_NAME_FIELD_NUMBER: _ClassVar[int]
    MAP_NAME_FIELD_NUMBER: _ClassVar[int]
    EVENT_GAME_DATA_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    event_id: _dota_shared_enums_pb2.EEvent
    game_name: str
    map_name: str
    event_game_data: bytes
    start_time: int
    def __init__(
        self,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
        game_name: str | None = ...,
        map_name: str | None = ...,
        event_game_data: bytes | None = ...,
        start_time: int | None = ...,
    ) -> None: ...

class CMsgGameMatchSignOutPerfData(_message.Message):
    __slots__ = (
        "average_frame_time",
        "max_frame_time",
        "server_average_frame_time",
        "server_max_frame_time",
        "average_compute_time",
        "max_compute_time",
        "average_client_tick_time",
        "max_client_tick_time",
        "average_client_simulate_time",
        "max_client_simulate_time",
        "average_output_time",
        "max_output_time",
        "average_wait_for_rendering_to_complete_time",
        "max_wait_for_rendering_to_complete_time",
        "average_swap_time",
        "max_swap_time",
        "average_frame_update_time",
        "max_frame_update_time",
        "average_idle_time",
        "max_idle_time",
        "average_input_processing_time",
        "max_input_processing_time",
        "num_slow_frames",
        "server_average_oversleep_frame_time",
        "server_max_oversleep_frame_time",
        "server_average_sleep_frame_time",
        "server_max_sleep_frame_time",
        "num_multitick_frames",
    )
    AVERAGE_FRAME_TIME_FIELD_NUMBER: _ClassVar[int]
    MAX_FRAME_TIME_FIELD_NUMBER: _ClassVar[int]
    SERVER_AVERAGE_FRAME_TIME_FIELD_NUMBER: _ClassVar[int]
    SERVER_MAX_FRAME_TIME_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_COMPUTE_TIME_FIELD_NUMBER: _ClassVar[int]
    MAX_COMPUTE_TIME_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_CLIENT_TICK_TIME_FIELD_NUMBER: _ClassVar[int]
    MAX_CLIENT_TICK_TIME_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_CLIENT_SIMULATE_TIME_FIELD_NUMBER: _ClassVar[int]
    MAX_CLIENT_SIMULATE_TIME_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_OUTPUT_TIME_FIELD_NUMBER: _ClassVar[int]
    MAX_OUTPUT_TIME_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_WAIT_FOR_RENDERING_TO_COMPLETE_TIME_FIELD_NUMBER: _ClassVar[int]
    MAX_WAIT_FOR_RENDERING_TO_COMPLETE_TIME_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_SWAP_TIME_FIELD_NUMBER: _ClassVar[int]
    MAX_SWAP_TIME_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_FRAME_UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    MAX_FRAME_UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_IDLE_TIME_FIELD_NUMBER: _ClassVar[int]
    MAX_IDLE_TIME_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_INPUT_PROCESSING_TIME_FIELD_NUMBER: _ClassVar[int]
    MAX_INPUT_PROCESSING_TIME_FIELD_NUMBER: _ClassVar[int]
    NUM_SLOW_FRAMES_FIELD_NUMBER: _ClassVar[int]
    SERVER_AVERAGE_OVERSLEEP_FRAME_TIME_FIELD_NUMBER: _ClassVar[int]
    SERVER_MAX_OVERSLEEP_FRAME_TIME_FIELD_NUMBER: _ClassVar[int]
    SERVER_AVERAGE_SLEEP_FRAME_TIME_FIELD_NUMBER: _ClassVar[int]
    SERVER_MAX_SLEEP_FRAME_TIME_FIELD_NUMBER: _ClassVar[int]
    NUM_MULTITICK_FRAMES_FIELD_NUMBER: _ClassVar[int]
    average_frame_time: _containers.RepeatedScalarFieldContainer[float]
    max_frame_time: _containers.RepeatedScalarFieldContainer[float]
    server_average_frame_time: float
    server_max_frame_time: float
    average_compute_time: _containers.RepeatedScalarFieldContainer[float]
    max_compute_time: _containers.RepeatedScalarFieldContainer[float]
    average_client_tick_time: _containers.RepeatedScalarFieldContainer[float]
    max_client_tick_time: _containers.RepeatedScalarFieldContainer[float]
    average_client_simulate_time: _containers.RepeatedScalarFieldContainer[float]
    max_client_simulate_time: _containers.RepeatedScalarFieldContainer[float]
    average_output_time: _containers.RepeatedScalarFieldContainer[float]
    max_output_time: _containers.RepeatedScalarFieldContainer[float]
    average_wait_for_rendering_to_complete_time: _containers.RepeatedScalarFieldContainer[float]
    max_wait_for_rendering_to_complete_time: _containers.RepeatedScalarFieldContainer[float]
    average_swap_time: _containers.RepeatedScalarFieldContainer[float]
    max_swap_time: _containers.RepeatedScalarFieldContainer[float]
    average_frame_update_time: _containers.RepeatedScalarFieldContainer[float]
    max_frame_update_time: _containers.RepeatedScalarFieldContainer[float]
    average_idle_time: _containers.RepeatedScalarFieldContainer[float]
    max_idle_time: _containers.RepeatedScalarFieldContainer[float]
    average_input_processing_time: _containers.RepeatedScalarFieldContainer[float]
    max_input_processing_time: _containers.RepeatedScalarFieldContainer[float]
    num_slow_frames: int
    server_average_oversleep_frame_time: float
    server_max_oversleep_frame_time: float
    server_average_sleep_frame_time: float
    server_max_sleep_frame_time: float
    num_multitick_frames: int
    def __init__(
        self,
        average_frame_time: _Iterable[float] | None = ...,
        max_frame_time: _Iterable[float] | None = ...,
        server_average_frame_time: float | None = ...,
        server_max_frame_time: float | None = ...,
        average_compute_time: _Iterable[float] | None = ...,
        max_compute_time: _Iterable[float] | None = ...,
        average_client_tick_time: _Iterable[float] | None = ...,
        max_client_tick_time: _Iterable[float] | None = ...,
        average_client_simulate_time: _Iterable[float] | None = ...,
        max_client_simulate_time: _Iterable[float] | None = ...,
        average_output_time: _Iterable[float] | None = ...,
        max_output_time: _Iterable[float] | None = ...,
        average_wait_for_rendering_to_complete_time: _Iterable[float] | None = ...,
        max_wait_for_rendering_to_complete_time: _Iterable[float] | None = ...,
        average_swap_time: _Iterable[float] | None = ...,
        max_swap_time: _Iterable[float] | None = ...,
        average_frame_update_time: _Iterable[float] | None = ...,
        max_frame_update_time: _Iterable[float] | None = ...,
        average_idle_time: _Iterable[float] | None = ...,
        max_idle_time: _Iterable[float] | None = ...,
        average_input_processing_time: _Iterable[float] | None = ...,
        max_input_processing_time: _Iterable[float] | None = ...,
        num_slow_frames: int | None = ...,
        server_average_oversleep_frame_time: float | None = ...,
        server_max_oversleep_frame_time: float | None = ...,
        server_average_sleep_frame_time: float | None = ...,
        server_max_sleep_frame_time: float | None = ...,
        num_multitick_frames: int | None = ...,
    ) -> None: ...

class CMsgGameMatchSignOutBanData(_message.Message):
    __slots__ = ("hero_bans", "hero_ban_votes")
    HERO_BANS_FIELD_NUMBER: _ClassVar[int]
    HERO_BAN_VOTES_FIELD_NUMBER: _ClassVar[int]
    hero_bans: _containers.RepeatedScalarFieldContainer[int]
    hero_ban_votes: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self, hero_bans: _Iterable[int] | None = ..., hero_ban_votes: _Iterable[int] | None = ...
    ) -> None: ...

class CMsgDOTALiveScoreboardUpdate(_message.Message):
    __slots__ = (
        "tournament_id",
        "tournament_game_id",
        "duration",
        "hltv_delay",
        "team_good",
        "team_bad",
        "roshan_respawn_timer",
        "league_id",
        "match_id",
    )
    class Team(_message.Message):
        __slots__ = ("players", "score", "tower_state", "barracks_state", "hero_picks", "hero_bans")
        class Player(_message.Message):
            __slots__ = (
                "player_slot",
                "player_name",
                "hero_name",
                "hero_id",
                "kills",
                "deaths",
                "assists",
                "last_hits",
                "denies",
                "gold",
                "level",
                "gold_per_min",
                "xp_per_min",
                "ultimate_state",
                "ultimate_cooldown",
                "item0",
                "item1",
                "item2",
                "item3",
                "item4",
                "item5",
                "respawn_timer",
                "account_id",
                "position_x",
                "position_y",
                "net_worth",
                "abilities",
            )
            class DOTAUltimateState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                k_EDOTAUltimateStateNotLearned: _ClassVar[
                    CMsgDOTALiveScoreboardUpdate.Team.Player.DOTAUltimateState
                ]
                k_EDOTAUltimateStateCooldown: _ClassVar[
                    CMsgDOTALiveScoreboardUpdate.Team.Player.DOTAUltimateState
                ]
                k_EDOTAUltimateStateNeedsMana: _ClassVar[
                    CMsgDOTALiveScoreboardUpdate.Team.Player.DOTAUltimateState
                ]
                k_EDOTAUltimateStateReady: _ClassVar[
                    CMsgDOTALiveScoreboardUpdate.Team.Player.DOTAUltimateState
                ]

            k_EDOTAUltimateStateNotLearned: (
                CMsgDOTALiveScoreboardUpdate.Team.Player.DOTAUltimateState
            )
            k_EDOTAUltimateStateCooldown: CMsgDOTALiveScoreboardUpdate.Team.Player.DOTAUltimateState
            k_EDOTAUltimateStateNeedsMana: (
                CMsgDOTALiveScoreboardUpdate.Team.Player.DOTAUltimateState
            )
            k_EDOTAUltimateStateReady: CMsgDOTALiveScoreboardUpdate.Team.Player.DOTAUltimateState
            class HeroAbility(_message.Message):
                __slots__ = ("ability_id", "ability_level")
                ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
                ABILITY_LEVEL_FIELD_NUMBER: _ClassVar[int]
                ability_id: int
                ability_level: int
                def __init__(
                    self, ability_id: int | None = ..., ability_level: int | None = ...
                ) -> None: ...

            PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
            PLAYER_NAME_FIELD_NUMBER: _ClassVar[int]
            HERO_NAME_FIELD_NUMBER: _ClassVar[int]
            HERO_ID_FIELD_NUMBER: _ClassVar[int]
            KILLS_FIELD_NUMBER: _ClassVar[int]
            DEATHS_FIELD_NUMBER: _ClassVar[int]
            ASSISTS_FIELD_NUMBER: _ClassVar[int]
            LAST_HITS_FIELD_NUMBER: _ClassVar[int]
            DENIES_FIELD_NUMBER: _ClassVar[int]
            GOLD_FIELD_NUMBER: _ClassVar[int]
            LEVEL_FIELD_NUMBER: _ClassVar[int]
            GOLD_PER_MIN_FIELD_NUMBER: _ClassVar[int]
            XP_PER_MIN_FIELD_NUMBER: _ClassVar[int]
            ULTIMATE_STATE_FIELD_NUMBER: _ClassVar[int]
            ULTIMATE_COOLDOWN_FIELD_NUMBER: _ClassVar[int]
            ITEM0_FIELD_NUMBER: _ClassVar[int]
            ITEM1_FIELD_NUMBER: _ClassVar[int]
            ITEM2_FIELD_NUMBER: _ClassVar[int]
            ITEM3_FIELD_NUMBER: _ClassVar[int]
            ITEM4_FIELD_NUMBER: _ClassVar[int]
            ITEM5_FIELD_NUMBER: _ClassVar[int]
            RESPAWN_TIMER_FIELD_NUMBER: _ClassVar[int]
            ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
            POSITION_X_FIELD_NUMBER: _ClassVar[int]
            POSITION_Y_FIELD_NUMBER: _ClassVar[int]
            NET_WORTH_FIELD_NUMBER: _ClassVar[int]
            ABILITIES_FIELD_NUMBER: _ClassVar[int]
            player_slot: int
            player_name: str
            hero_name: str
            hero_id: int
            kills: int
            deaths: int
            assists: int
            last_hits: int
            denies: int
            gold: int
            level: int
            gold_per_min: float
            xp_per_min: float
            ultimate_state: CMsgDOTALiveScoreboardUpdate.Team.Player.DOTAUltimateState
            ultimate_cooldown: float
            item0: int
            item1: int
            item2: int
            item3: int
            item4: int
            item5: int
            respawn_timer: int
            account_id: int
            position_x: float
            position_y: float
            net_worth: int
            abilities: _containers.RepeatedCompositeFieldContainer[
                CMsgDOTALiveScoreboardUpdate.Team.Player.HeroAbility
            ]
            def __init__(
                self,
                player_slot: int | None = ...,
                player_name: str | None = ...,
                hero_name: str | None = ...,
                hero_id: int | None = ...,
                kills: int | None = ...,
                deaths: int | None = ...,
                assists: int | None = ...,
                last_hits: int | None = ...,
                denies: int | None = ...,
                gold: int | None = ...,
                level: int | None = ...,
                gold_per_min: float | None = ...,
                xp_per_min: float | None = ...,
                ultimate_state: CMsgDOTALiveScoreboardUpdate.Team.Player.DOTAUltimateState
                | str
                | None = ...,
                ultimate_cooldown: float | None = ...,
                item0: int | None = ...,
                item1: int | None = ...,
                item2: int | None = ...,
                item3: int | None = ...,
                item4: int | None = ...,
                item5: int | None = ...,
                respawn_timer: int | None = ...,
                account_id: int | None = ...,
                position_x: float | None = ...,
                position_y: float | None = ...,
                net_worth: int | None = ...,
                abilities: _Iterable[
                    CMsgDOTALiveScoreboardUpdate.Team.Player.HeroAbility | _Mapping
                ]
                | None = ...,
            ) -> None: ...

        PLAYERS_FIELD_NUMBER: _ClassVar[int]
        SCORE_FIELD_NUMBER: _ClassVar[int]
        TOWER_STATE_FIELD_NUMBER: _ClassVar[int]
        BARRACKS_STATE_FIELD_NUMBER: _ClassVar[int]
        HERO_PICKS_FIELD_NUMBER: _ClassVar[int]
        HERO_BANS_FIELD_NUMBER: _ClassVar[int]
        players: _containers.RepeatedCompositeFieldContainer[
            CMsgDOTALiveScoreboardUpdate.Team.Player
        ]
        score: int
        tower_state: int
        barracks_state: int
        hero_picks: _containers.RepeatedScalarFieldContainer[int]
        hero_bans: _containers.RepeatedScalarFieldContainer[int]
        def __init__(
            self,
            players: _Iterable[CMsgDOTALiveScoreboardUpdate.Team.Player | _Mapping] | None = ...,
            score: int | None = ...,
            tower_state: int | None = ...,
            barracks_state: int | None = ...,
            hero_picks: _Iterable[int] | None = ...,
            hero_bans: _Iterable[int] | None = ...,
        ) -> None: ...

    TOURNAMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TOURNAMENT_GAME_ID_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    HLTV_DELAY_FIELD_NUMBER: _ClassVar[int]
    TEAM_GOOD_FIELD_NUMBER: _ClassVar[int]
    TEAM_BAD_FIELD_NUMBER: _ClassVar[int]
    ROSHAN_RESPAWN_TIMER_FIELD_NUMBER: _ClassVar[int]
    LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    tournament_id: int
    tournament_game_id: int
    duration: float
    hltv_delay: int
    team_good: CMsgDOTALiveScoreboardUpdate.Team
    team_bad: CMsgDOTALiveScoreboardUpdate.Team
    roshan_respawn_timer: int
    league_id: int
    match_id: int
    def __init__(
        self,
        tournament_id: int | None = ...,
        tournament_game_id: int | None = ...,
        duration: float | None = ...,
        hltv_delay: int | None = ...,
        team_good: CMsgDOTALiveScoreboardUpdate.Team | _Mapping | None = ...,
        team_bad: CMsgDOTALiveScoreboardUpdate.Team | _Mapping | None = ...,
        roshan_respawn_timer: int | None = ...,
        league_id: int | None = ...,
        match_id: int | None = ...,
    ) -> None: ...

class CMsgServerToGCRequestBatchPlayerResources(_message.Message):
    __slots__ = ("account_ids", "rank_types", "lobby_type")
    ACCOUNT_IDS_FIELD_NUMBER: _ClassVar[int]
    RANK_TYPES_FIELD_NUMBER: _ClassVar[int]
    LOBBY_TYPE_FIELD_NUMBER: _ClassVar[int]
    account_ids: _containers.RepeatedScalarFieldContainer[int]
    rank_types: _containers.RepeatedScalarFieldContainer[int]
    lobby_type: int
    def __init__(
        self,
        account_ids: _Iterable[int] | None = ...,
        rank_types: _Iterable[int] | None = ...,
        lobby_type: int | None = ...,
    ) -> None: ...

class CMsgServerToGCRequestBatchPlayerResourcesResponse(_message.Message):
    __slots__ = ("results",)
    class Result(_message.Message):
        __slots__ = (
            "account_id",
            "rank",
            "rank_calibrated",
            "low_priority",
            "is_new_player",
            "is_guide_player",
            "comm_level",
            "behavior_level",
            "wins",
            "losses",
            "smurf_category",
            "comm_score",
            "behavior_score",
            "rank_uncertainty",
        )
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        RANK_FIELD_NUMBER: _ClassVar[int]
        RANK_CALIBRATED_FIELD_NUMBER: _ClassVar[int]
        LOW_PRIORITY_FIELD_NUMBER: _ClassVar[int]
        IS_NEW_PLAYER_FIELD_NUMBER: _ClassVar[int]
        IS_GUIDE_PLAYER_FIELD_NUMBER: _ClassVar[int]
        COMM_LEVEL_FIELD_NUMBER: _ClassVar[int]
        BEHAVIOR_LEVEL_FIELD_NUMBER: _ClassVar[int]
        WINS_FIELD_NUMBER: _ClassVar[int]
        LOSSES_FIELD_NUMBER: _ClassVar[int]
        SMURF_CATEGORY_FIELD_NUMBER: _ClassVar[int]
        COMM_SCORE_FIELD_NUMBER: _ClassVar[int]
        BEHAVIOR_SCORE_FIELD_NUMBER: _ClassVar[int]
        RANK_UNCERTAINTY_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        rank: int
        rank_calibrated: bool
        low_priority: bool
        is_new_player: bool
        is_guide_player: bool
        comm_level: int
        behavior_level: int
        wins: int
        losses: int
        smurf_category: int
        comm_score: int
        behavior_score: int
        rank_uncertainty: int
        def __init__(
            self,
            account_id: int | None = ...,
            rank: int | None = ...,
            rank_calibrated: bool = ...,
            low_priority: bool = ...,
            is_new_player: bool = ...,
            is_guide_player: bool = ...,
            comm_level: int | None = ...,
            behavior_level: int | None = ...,
            wins: int | None = ...,
            losses: int | None = ...,
            smurf_category: int | None = ...,
            comm_score: int | None = ...,
            behavior_score: int | None = ...,
            rank_uncertainty: int | None = ...,
        ) -> None: ...

    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[
        CMsgServerToGCRequestBatchPlayerResourcesResponse.Result
    ]
    def __init__(
        self,
        results: _Iterable[CMsgServerToGCRequestBatchPlayerResourcesResponse.Result | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgDOTAPlayerFailedToConnect(_message.Message):
    __slots__ = ("failed_loaders", "abandoned_loaders")
    FAILED_LOADERS_FIELD_NUMBER: _ClassVar[int]
    ABANDONED_LOADERS_FIELD_NUMBER: _ClassVar[int]
    failed_loaders: _containers.RepeatedScalarFieldContainer[int]
    abandoned_loaders: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        failed_loaders: _Iterable[int] | None = ...,
        abandoned_loaders: _Iterable[int] | None = ...,
    ) -> None: ...

class CMsgGCToRelayConnect(_message.Message):
    __slots__ = (
        "source_tv_public_addr",
        "source_tv_private_addr",
        "source_tv_port",
        "game_server_steam_id",
        "parent_count",
        "tv_unique_secret_code",
        "source_tv_steamid",
    )
    SOURCE_TV_PUBLIC_ADDR_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TV_PRIVATE_ADDR_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TV_PORT_FIELD_NUMBER: _ClassVar[int]
    GAME_SERVER_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_COUNT_FIELD_NUMBER: _ClassVar[int]
    TV_UNIQUE_SECRET_CODE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TV_STEAMID_FIELD_NUMBER: _ClassVar[int]
    source_tv_public_addr: int
    source_tv_private_addr: int
    source_tv_port: int
    game_server_steam_id: int
    parent_count: int
    tv_unique_secret_code: int
    source_tv_steamid: int
    def __init__(
        self,
        source_tv_public_addr: int | None = ...,
        source_tv_private_addr: int | None = ...,
        source_tv_port: int | None = ...,
        game_server_steam_id: int | None = ...,
        parent_count: int | None = ...,
        tv_unique_secret_code: int | None = ...,
        source_tv_steamid: int | None = ...,
    ) -> None: ...

class CMsgGCGCToLANServerRelayConnect(_message.Message):
    __slots__ = ("relay_steamid",)
    RELAY_STEAMID_FIELD_NUMBER: _ClassVar[int]
    relay_steamid: int
    def __init__(self, relay_steamid: int | None = ...) -> None: ...

class CMsgGCBanStatusRequest(_message.Message):
    __slots__ = ("account_id",)
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    def __init__(self, account_id: int | None = ...) -> None: ...

class CMsgGCBanStatusResponse(_message.Message):
    __slots__ = ("result", "low_priority", "text_chat_banned", "voice_chat_banned")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    LOW_PRIORITY_FIELD_NUMBER: _ClassVar[int]
    TEXT_CHAT_BANNED_FIELD_NUMBER: _ClassVar[int]
    VOICE_CHAT_BANNED_FIELD_NUMBER: _ClassVar[int]
    result: int
    low_priority: bool
    text_chat_banned: bool
    voice_chat_banned: bool
    def __init__(
        self,
        result: int | None = ...,
        low_priority: bool = ...,
        text_chat_banned: bool = ...,
        voice_chat_banned: bool = ...,
    ) -> None: ...

class CMsgTournamentItemEvent(_message.Message):
    __slots__ = (
        "killer_account_id",
        "victim_account_id",
        "event_type",
        "tv_delay",
        "dota_time",
        "replay_time",
        "loot_list",
        "event_team",
        "multi_kill_count",
        "winner_score",
        "loser_score",
        "hero_statues",
    )
    KILLER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    VICTIM_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    TV_DELAY_FIELD_NUMBER: _ClassVar[int]
    DOTA_TIME_FIELD_NUMBER: _ClassVar[int]
    REPLAY_TIME_FIELD_NUMBER: _ClassVar[int]
    LOOT_LIST_FIELD_NUMBER: _ClassVar[int]
    EVENT_TEAM_FIELD_NUMBER: _ClassVar[int]
    MULTI_KILL_COUNT_FIELD_NUMBER: _ClassVar[int]
    WINNER_SCORE_FIELD_NUMBER: _ClassVar[int]
    LOSER_SCORE_FIELD_NUMBER: _ClassVar[int]
    HERO_STATUES_FIELD_NUMBER: _ClassVar[int]
    killer_account_id: int
    victim_account_id: int
    event_type: _dota_gcmessages_common_pb2.DOTA_TournamentEvents
    tv_delay: int
    dota_time: int
    replay_time: float
    loot_list: str
    event_team: int
    multi_kill_count: int
    winner_score: int
    loser_score: int
    hero_statues: _containers.RepeatedCompositeFieldContainer[
        _dota_gcmessages_common_pb2.CProtoItemHeroStatue
    ]
    def __init__(
        self,
        killer_account_id: int | None = ...,
        victim_account_id: int | None = ...,
        event_type: _dota_gcmessages_common_pb2.DOTA_TournamentEvents | str | None = ...,
        tv_delay: int | None = ...,
        dota_time: int | None = ...,
        replay_time: float | None = ...,
        loot_list: str | None = ...,
        event_team: int | None = ...,
        multi_kill_count: int | None = ...,
        winner_score: int | None = ...,
        loser_score: int | None = ...,
        hero_statues: _Iterable[_dota_gcmessages_common_pb2.CProtoItemHeroStatue | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgTournamentItemEventResponse(_message.Message):
    __slots__ = ("event_type", "viewers_granted")
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    VIEWERS_GRANTED_FIELD_NUMBER: _ClassVar[int]
    event_type: _dota_gcmessages_common_pb2.DOTA_TournamentEvents
    viewers_granted: int
    def __init__(
        self,
        event_type: _dota_gcmessages_common_pb2.DOTA_TournamentEvents | str | None = ...,
        viewers_granted: int | None = ...,
    ) -> None: ...

class CMsgTeamFanfare(_message.Message):
    __slots__ = ("match_id",)
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    def __init__(self, match_id: int | None = ...) -> None: ...

class CMsgResponseTeamFanfare(_message.Message):
    __slots__ = ("fanfare_goodguys", "fanfare_badguys")
    FANFARE_GOODGUYS_FIELD_NUMBER: _ClassVar[int]
    FANFARE_BADGUYS_FIELD_NUMBER: _ClassVar[int]
    fanfare_goodguys: int
    fanfare_badguys: int
    def __init__(
        self, fanfare_goodguys: int | None = ..., fanfare_badguys: int | None = ...
    ) -> None: ...

class CMsgDOTAAwardEventPoints(_message.Message):
    __slots__ = ("award_points", "match_id", "event_id", "timestamp", "audit_action")
    class AwardPoints(_message.Message):
        __slots__ = (
            "account_id",
            "points",
            "premium_points",
            "trade_ban_time",
            "eligible_for_periodic_adjustment",
            "point_cap_periodic_resource_id",
        )
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        POINTS_FIELD_NUMBER: _ClassVar[int]
        PREMIUM_POINTS_FIELD_NUMBER: _ClassVar[int]
        TRADE_BAN_TIME_FIELD_NUMBER: _ClassVar[int]
        ELIGIBLE_FOR_PERIODIC_ADJUSTMENT_FIELD_NUMBER: _ClassVar[int]
        POINT_CAP_PERIODIC_RESOURCE_ID_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        points: int
        premium_points: int
        trade_ban_time: int
        eligible_for_periodic_adjustment: bool
        point_cap_periodic_resource_id: int
        def __init__(
            self,
            account_id: int | None = ...,
            points: int | None = ...,
            premium_points: int | None = ...,
            trade_ban_time: int | None = ...,
            eligible_for_periodic_adjustment: bool = ...,
            point_cap_periodic_resource_id: int | None = ...,
        ) -> None: ...

    AWARD_POINTS_FIELD_NUMBER: _ClassVar[int]
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    AUDIT_ACTION_FIELD_NUMBER: _ClassVar[int]
    award_points: _containers.RepeatedCompositeFieldContainer[CMsgDOTAAwardEventPoints.AwardPoints]
    match_id: int
    event_id: _dota_shared_enums_pb2.EEvent
    timestamp: int
    audit_action: int
    def __init__(
        self,
        award_points: _Iterable[CMsgDOTAAwardEventPoints.AwardPoints | _Mapping] | None = ...,
        match_id: int | None = ...,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
        timestamp: int | None = ...,
        audit_action: int | None = ...,
    ) -> None: ...

class CMsgGCToServerPingRequest(_message.Message):
    __slots__ = ("request_id", "request_time")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_TIME_FIELD_NUMBER: _ClassVar[int]
    request_id: int
    request_time: int
    def __init__(self, request_id: int | None = ..., request_time: int | None = ...) -> None: ...

class CMsgGCToServerPingResponse(_message.Message):
    __slots__ = ("request_id", "request_time", "cluster")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_TIME_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_FIELD_NUMBER: _ClassVar[int]
    request_id: int
    request_time: int
    cluster: int
    def __init__(
        self,
        request_id: int | None = ...,
        request_time: int | None = ...,
        cluster: int | None = ...,
    ) -> None: ...

class CMsgServerToGCMatchConnectionStats(_message.Message):
    __slots__ = ("match_id", "region_id", "league_id", "players", "cluster_id")
    class Player(_message.Message):
        __slots__ = (
            "account_id",
            "ip",
            "avg_ping_ms",
            "packet_loss",
            "ping_deviation",
            "full_resends",
        )
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        IP_FIELD_NUMBER: _ClassVar[int]
        AVG_PING_MS_FIELD_NUMBER: _ClassVar[int]
        PACKET_LOSS_FIELD_NUMBER: _ClassVar[int]
        PING_DEVIATION_FIELD_NUMBER: _ClassVar[int]
        FULL_RESENDS_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        ip: int
        avg_ping_ms: int
        packet_loss: float
        ping_deviation: float
        full_resends: int
        def __init__(
            self,
            account_id: int | None = ...,
            ip: int | None = ...,
            avg_ping_ms: int | None = ...,
            packet_loss: float | None = ...,
            ping_deviation: float | None = ...,
            full_resends: int | None = ...,
        ) -> None: ...

    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    REGION_ID_FIELD_NUMBER: _ClassVar[int]
    LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    region_id: int
    league_id: int
    players: _containers.RepeatedCompositeFieldContainer[CMsgServerToGCMatchConnectionStats.Player]
    cluster_id: int
    def __init__(
        self,
        match_id: int | None = ...,
        region_id: int | None = ...,
        league_id: int | None = ...,
        players: _Iterable[CMsgServerToGCMatchConnectionStats.Player | _Mapping] | None = ...,
        cluster_id: int | None = ...,
    ) -> None: ...

class CMsgServerGCUpdateSpectatorCount(_message.Message):
    __slots__ = ("spectator_count",)
    SPECTATOR_COUNT_FIELD_NUMBER: _ClassVar[int]
    spectator_count: int
    def __init__(self, spectator_count: int | None = ...) -> None: ...

class CSerializedCombatLog(_message.Message):
    __slots__ = ("version", "dictionary", "entries")
    class Dictionary(_message.Message):
        __slots__ = ("strings",)
        class DictString(_message.Message):
            __slots__ = ("id", "value")
            ID_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            id: int
            value: str
            def __init__(self, id: int | None = ..., value: str | None = ...) -> None: ...

        STRINGS_FIELD_NUMBER: _ClassVar[int]
        strings: _containers.RepeatedCompositeFieldContainer[
            CSerializedCombatLog.Dictionary.DictString
        ]
        def __init__(
            self,
            strings: _Iterable[CSerializedCombatLog.Dictionary.DictString | _Mapping] | None = ...,
        ) -> None: ...

    VERSION_FIELD_NUMBER: _ClassVar[int]
    DICTIONARY_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    version: int
    dictionary: CSerializedCombatLog.Dictionary
    entries: _containers.RepeatedCompositeFieldContainer[
        _dota_shared_enums_pb2.CMsgDOTACombatLogEntry
    ]
    def __init__(
        self,
        version: int | None = ...,
        dictionary: CSerializedCombatLog.Dictionary | _Mapping | None = ...,
        entries: _Iterable[_dota_shared_enums_pb2.CMsgDOTACombatLogEntry | _Mapping] | None = ...,
    ) -> None: ...

class CMsgServerToGCVictoryPredictions(_message.Message):
    __slots__ = ("records",)
    class PredictionItem(_message.Message):
        __slots__ = ("item_id", "item_def")
        ITEM_ID_FIELD_NUMBER: _ClassVar[int]
        ITEM_DEF_FIELD_NUMBER: _ClassVar[int]
        item_id: int
        item_def: int
        def __init__(self, item_id: int | None = ..., item_def: int | None = ...) -> None: ...

    class Record(_message.Message):
        __slots__ = ("account_id", "item_ids", "prediction_items")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        ITEM_IDS_FIELD_NUMBER: _ClassVar[int]
        PREDICTION_ITEMS_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        item_ids: _containers.RepeatedScalarFieldContainer[int]
        prediction_items: _containers.RepeatedCompositeFieldContainer[
            CMsgServerToGCVictoryPredictions.PredictionItem
        ]
        def __init__(
            self,
            account_id: int | None = ...,
            item_ids: _Iterable[int] | None = ...,
            prediction_items: _Iterable[CMsgServerToGCVictoryPredictions.PredictionItem | _Mapping]
            | None = ...,
        ) -> None: ...

    RECORDS_FIELD_NUMBER: _ClassVar[int]
    records: _containers.RepeatedCompositeFieldContainer[CMsgServerToGCVictoryPredictions.Record]
    def __init__(
        self, records: _Iterable[CMsgServerToGCVictoryPredictions.Record | _Mapping] | None = ...
    ) -> None: ...

class CMsgServerToGCRequestStatus(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgServerToGCRequestStatus_Response(_message.Message):
    __slots__ = ("response",)
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: int
    def __init__(self, response: int | None = ...) -> None: ...

class CMsgGCToServerEvaluateToxicChat(_message.Message):
    __slots__ = ("target_account_id", "reporter_account_id")
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    REPORTER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    target_account_id: int
    reporter_account_id: int
    def __init__(
        self, target_account_id: int | None = ..., reporter_account_id: int | None = ...
    ) -> None: ...

class CMsgServerToGCEvaluateToxicChat(_message.Message):
    __slots__ = ("target_account_id", "reporter_account_id", "match_id", "timestamp", "line")
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    REPORTER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LINE_FIELD_NUMBER: _ClassVar[int]
    target_account_id: int
    reporter_account_id: int
    match_id: int
    timestamp: _containers.RepeatedScalarFieldContainer[int]
    line: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        target_account_id: int | None = ...,
        reporter_account_id: int | None = ...,
        match_id: int | None = ...,
        timestamp: _Iterable[int] | None = ...,
        line: _Iterable[str] | None = ...,
    ) -> None: ...

class CMsgServerToGCEvaluateToxicChatResponse(_message.Message):
    __slots__ = (
        "target_account_id",
        "reporter_account_id",
        "ban_reason",
        "ban_duration",
        "toxicity_score",
    )
    TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    REPORTER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    BAN_REASON_FIELD_NUMBER: _ClassVar[int]
    BAN_DURATION_FIELD_NUMBER: _ClassVar[int]
    TOXICITY_SCORE_FIELD_NUMBER: _ClassVar[int]
    target_account_id: int
    reporter_account_id: int
    ban_reason: int
    ban_duration: int
    toxicity_score: float
    def __init__(
        self,
        target_account_id: int | None = ...,
        reporter_account_id: int | None = ...,
        ban_reason: int | None = ...,
        ban_duration: int | None = ...,
        toxicity_score: float | None = ...,
    ) -> None: ...

class CMsgSignOutAssassinMiniGameInfo(_message.Message):
    __slots__ = (
        "winning_players",
        "losing_players",
        "arcana_owners",
        "assassin_won",
        "target_hero_id",
        "contract_completed",
        "contract_complete_time",
        "pa_is_radiant",
    )
    WINNING_PLAYERS_FIELD_NUMBER: _ClassVar[int]
    LOSING_PLAYERS_FIELD_NUMBER: _ClassVar[int]
    ARCANA_OWNERS_FIELD_NUMBER: _ClassVar[int]
    ASSASSIN_WON_FIELD_NUMBER: _ClassVar[int]
    TARGET_HERO_ID_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_COMPLETED_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_COMPLETE_TIME_FIELD_NUMBER: _ClassVar[int]
    PA_IS_RADIANT_FIELD_NUMBER: _ClassVar[int]
    winning_players: _containers.RepeatedScalarFieldContainer[int]
    losing_players: _containers.RepeatedScalarFieldContainer[int]
    arcana_owners: _containers.RepeatedScalarFieldContainer[int]
    assassin_won: bool
    target_hero_id: int
    contract_completed: bool
    contract_complete_time: float
    pa_is_radiant: bool
    def __init__(
        self,
        winning_players: _Iterable[int] | None = ...,
        losing_players: _Iterable[int] | None = ...,
        arcana_owners: _Iterable[int] | None = ...,
        assassin_won: bool = ...,
        target_hero_id: int | None = ...,
        contract_completed: bool = ...,
        contract_complete_time: float | None = ...,
        pa_is_radiant: bool = ...,
    ) -> None: ...

class CMsgServerToGCKillSummaries(_message.Message):
    __slots__ = ("ingameevent_id", "summaries")
    class KillSummary(_message.Message):
        __slots__ = ("killer_hero_id", "victim_hero_id", "kill_count")
        KILLER_HERO_ID_FIELD_NUMBER: _ClassVar[int]
        VICTIM_HERO_ID_FIELD_NUMBER: _ClassVar[int]
        KILL_COUNT_FIELD_NUMBER: _ClassVar[int]
        killer_hero_id: int
        victim_hero_id: int
        kill_count: int
        def __init__(
            self,
            killer_hero_id: int | None = ...,
            victim_hero_id: int | None = ...,
            kill_count: int | None = ...,
        ) -> None: ...

    INGAMEEVENT_ID_FIELD_NUMBER: _ClassVar[int]
    SUMMARIES_FIELD_NUMBER: _ClassVar[int]
    ingameevent_id: int
    summaries: _containers.RepeatedCompositeFieldContainer[CMsgServerToGCKillSummaries.KillSummary]
    def __init__(
        self,
        ingameevent_id: int | None = ...,
        summaries: _Iterable[CMsgServerToGCKillSummaries.KillSummary | _Mapping] | None = ...,
    ) -> None: ...

class CMsgServerToGCLockCharmTrading(_message.Message):
    __slots__ = ("account_id", "item_id")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    item_id: int
    def __init__(self, account_id: int | None = ..., item_id: int | None = ...) -> None: ...

class CMsgSignOutUpdatePlayerChallenge(_message.Message):
    __slots__ = ("account_id", "completed", "rerolled", "match_id", "hero_id")
    class Challenge(_message.Message):
        __slots__ = ("event_id", "slot_id", "sequence_id", "progress", "challenge_rank")
        EVENT_ID_FIELD_NUMBER: _ClassVar[int]
        SLOT_ID_FIELD_NUMBER: _ClassVar[int]
        SEQUENCE_ID_FIELD_NUMBER: _ClassVar[int]
        PROGRESS_FIELD_NUMBER: _ClassVar[int]
        CHALLENGE_RANK_FIELD_NUMBER: _ClassVar[int]
        event_id: _dota_shared_enums_pb2.EEvent
        slot_id: int
        sequence_id: int
        progress: int
        challenge_rank: int
        def __init__(
            self,
            event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
            slot_id: int | None = ...,
            sequence_id: int | None = ...,
            progress: int | None = ...,
            challenge_rank: int | None = ...,
        ) -> None: ...

    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    REROLLED_FIELD_NUMBER: _ClassVar[int]
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    completed: _containers.RepeatedCompositeFieldContainer[
        CMsgSignOutUpdatePlayerChallenge.Challenge
    ]
    rerolled: _containers.RepeatedCompositeFieldContainer[
        CMsgSignOutUpdatePlayerChallenge.Challenge
    ]
    match_id: int
    hero_id: int
    def __init__(
        self,
        account_id: int | None = ...,
        completed: _Iterable[CMsgSignOutUpdatePlayerChallenge.Challenge | _Mapping] | None = ...,
        rerolled: _Iterable[CMsgSignOutUpdatePlayerChallenge.Challenge | _Mapping] | None = ...,
        match_id: int | None = ...,
        hero_id: int | None = ...,
    ) -> None: ...

class CMsgServerToGCRerollPlayerChallenge(_message.Message):
    __slots__ = ("account_id", "reroll_msg")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    REROLL_MSG_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    reroll_msg: _dota_gcmessages_common_pb2.CMsgClientToGCRerollPlayerChallenge
    def __init__(
        self,
        account_id: int | None = ...,
        reroll_msg: _dota_gcmessages_common_pb2.CMsgClientToGCRerollPlayerChallenge
        | _Mapping
        | None = ...,
    ) -> None: ...

class CMsgSpendWager(_message.Message):
    __slots__ = ("players", "event_id", "timestamp", "match_id", "server_steam_id")
    class Player(_message.Message):
        __slots__ = ("account_id", "wager", "wager_token_item_id")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        WAGER_FIELD_NUMBER: _ClassVar[int]
        WAGER_TOKEN_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        wager: int
        wager_token_item_id: int
        def __init__(
            self,
            account_id: int | None = ...,
            wager: int | None = ...,
            wager_token_item_id: int | None = ...,
        ) -> None: ...

    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    SERVER_STEAM_ID_FIELD_NUMBER: _ClassVar[int]
    players: _containers.RepeatedCompositeFieldContainer[CMsgSpendWager.Player]
    event_id: _dota_shared_enums_pb2.EEvent
    timestamp: int
    match_id: int
    server_steam_id: int
    def __init__(
        self,
        players: _Iterable[CMsgSpendWager.Player | _Mapping] | None = ...,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
        timestamp: int | None = ...,
        match_id: int | None = ...,
        server_steam_id: int | None = ...,
    ) -> None: ...

class CMsgSignOutXPCoins(_message.Message):
    __slots__ = ("players", "event_id", "match_id", "timestamp")
    class Player(_message.Message):
        __slots__ = (
            "account_id",
            "xp_gained",
            "coins_spent",
            "wager_token_item_id",
            "rank_wager",
            "wager_streak",
        )
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        XP_GAINED_FIELD_NUMBER: _ClassVar[int]
        COINS_SPENT_FIELD_NUMBER: _ClassVar[int]
        WAGER_TOKEN_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
        RANK_WAGER_FIELD_NUMBER: _ClassVar[int]
        WAGER_STREAK_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        xp_gained: int
        coins_spent: int
        wager_token_item_id: int
        rank_wager: int
        wager_streak: int
        def __init__(
            self,
            account_id: int | None = ...,
            xp_gained: int | None = ...,
            coins_spent: int | None = ...,
            wager_token_item_id: int | None = ...,
            rank_wager: int | None = ...,
            wager_streak: int | None = ...,
        ) -> None: ...

    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    players: _containers.RepeatedCompositeFieldContainer[CMsgSignOutXPCoins.Player]
    event_id: _dota_shared_enums_pb2.EEvent
    match_id: int
    timestamp: int
    def __init__(
        self,
        players: _Iterable[CMsgSignOutXPCoins.Player | _Mapping] | None = ...,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
        match_id: int | None = ...,
        timestamp: int | None = ...,
    ) -> None: ...

class CMsgSignOutBounties(_message.Message):
    __slots__ = ("bounties", "event_id", "match_id", "timestamp")
    class Bounty(_message.Message):
        __slots__ = ("issuer_account_id", "completer_account_id", "target_account_id")
        ISSUER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        COMPLETER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        TARGET_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        issuer_account_id: int
        completer_account_id: int
        target_account_id: int
        def __init__(
            self,
            issuer_account_id: int | None = ...,
            completer_account_id: int | None = ...,
            target_account_id: int | None = ...,
        ) -> None: ...

    BOUNTIES_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    bounties: _containers.RepeatedCompositeFieldContainer[CMsgSignOutBounties.Bounty]
    event_id: _dota_shared_enums_pb2.EEvent
    match_id: int
    timestamp: int
    def __init__(
        self,
        bounties: _Iterable[CMsgSignOutBounties.Bounty | _Mapping] | None = ...,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
        match_id: int | None = ...,
        timestamp: int | None = ...,
    ) -> None: ...

class CMsgSignOutCommunityGoalProgress(_message.Message):
    __slots__ = ("event_id", "event_increments")
    class EventGoalIncrement(_message.Message):
        __slots__ = ("event_goal_id", "increment_amount")
        EVENT_GOAL_ID_FIELD_NUMBER: _ClassVar[int]
        INCREMENT_AMOUNT_FIELD_NUMBER: _ClassVar[int]
        event_goal_id: int
        increment_amount: int
        def __init__(
            self, event_goal_id: int | None = ..., increment_amount: int | None = ...
        ) -> None: ...

    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_INCREMENTS_FIELD_NUMBER: _ClassVar[int]
    event_id: _dota_shared_enums_pb2.EEvent
    event_increments: _containers.RepeatedCompositeFieldContainer[
        CMsgSignOutCommunityGoalProgress.EventGoalIncrement
    ]
    def __init__(
        self,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
        event_increments: _Iterable[CMsgSignOutCommunityGoalProgress.EventGoalIncrement | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgServerToGCCloseCompendiumInGamePredictionVoting(_message.Message):
    __slots__ = ("match_id", "hltv_delay", "league_id")
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    HLTV_DELAY_FIELD_NUMBER: _ClassVar[int]
    LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    hltv_delay: int
    league_id: int
    def __init__(
        self, match_id: int | None = ..., hltv_delay: int | None = ..., league_id: int | None = ...
    ) -> None: ...

class CMsgServerToGCCloseCompendiumInGamePredictionVotingResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: bool
    def __init__(self, result: bool = ...) -> None: ...

class CMsgServerToGCCompendiumInGamePredictionResults(_message.Message):
    __slots__ = ("match_id", "results", "league_id", "league_node_id")
    class PredictionResult(_message.Message):
        __slots__ = ("prediction_id", "prediction_value", "prediction_value_is_mask")
        PREDICTION_ID_FIELD_NUMBER: _ClassVar[int]
        PREDICTION_VALUE_FIELD_NUMBER: _ClassVar[int]
        PREDICTION_VALUE_IS_MASK_FIELD_NUMBER: _ClassVar[int]
        prediction_id: int
        prediction_value: int
        prediction_value_is_mask: bool
        def __init__(
            self,
            prediction_id: int | None = ...,
            prediction_value: int | None = ...,
            prediction_value_is_mask: bool = ...,
        ) -> None: ...

    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    LEAGUE_NODE_ID_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    results: _containers.RepeatedCompositeFieldContainer[
        CMsgServerToGCCompendiumInGamePredictionResults.PredictionResult
    ]
    league_id: int
    league_node_id: int
    def __init__(
        self,
        match_id: int | None = ...,
        results: _Iterable[
            CMsgServerToGCCompendiumInGamePredictionResults.PredictionResult | _Mapping
        ]
        | None = ...,
        league_id: int | None = ...,
        league_node_id: int | None = ...,
    ) -> None: ...

class CMsgServerToGCCompendiumChosenInGamePredictions(_message.Message):
    __slots__ = ("match_id", "predictions_chosen", "league_id")
    class Prediction(_message.Message):
        __slots__ = ("prediction_id",)
        PREDICTION_ID_FIELD_NUMBER: _ClassVar[int]
        prediction_id: int
        def __init__(self, prediction_id: int | None = ...) -> None: ...

    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    PREDICTIONS_CHOSEN_FIELD_NUMBER: _ClassVar[int]
    LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    predictions_chosen: _containers.RepeatedCompositeFieldContainer[
        CMsgServerToGCCompendiumChosenInGamePredictions.Prediction
    ]
    league_id: int
    def __init__(
        self,
        match_id: int | None = ...,
        predictions_chosen: _Iterable[
            CMsgServerToGCCompendiumChosenInGamePredictions.Prediction | _Mapping
        ]
        | None = ...,
        league_id: int | None = ...,
    ) -> None: ...

class CMsgGCToGCCompendiumInGamePredictionResults(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: CMsgServerToGCCompendiumInGamePredictionResults
    def __init__(
        self, results: CMsgServerToGCCompendiumInGamePredictionResults | _Mapping | None = ...
    ) -> None: ...

class CMsgServerToGCMatchPlayerItemPurchaseHistory(_message.Message):
    __slots__ = ("match_id", "mmr", "players")
    class ItemPurchase(_message.Message):
        __slots__ = ("item", "gold", "net_worth", "game_time", "inventory_items", "talents_skilled")
        ITEM_FIELD_NUMBER: _ClassVar[int]
        GOLD_FIELD_NUMBER: _ClassVar[int]
        NET_WORTH_FIELD_NUMBER: _ClassVar[int]
        GAME_TIME_FIELD_NUMBER: _ClassVar[int]
        INVENTORY_ITEMS_FIELD_NUMBER: _ClassVar[int]
        TALENTS_SKILLED_FIELD_NUMBER: _ClassVar[int]
        item: int
        gold: int
        net_worth: int
        game_time: int
        inventory_items: _containers.RepeatedScalarFieldContainer[int]
        talents_skilled: _containers.RepeatedScalarFieldContainer[bool]
        def __init__(
            self,
            item: int | None = ...,
            gold: int | None = ...,
            net_worth: int | None = ...,
            game_time: int | None = ...,
            inventory_items: _Iterable[int] | None = ...,
            talents_skilled: _Iterable[bool] | None = ...,
        ) -> None: ...

    class Player(_message.Message):
        __slots__ = (
            "player_slot",
            "account_id",
            "hero_id",
            "allied_hero_ids",
            "enemy_hero_ids",
            "item_purchases",
            "lane",
            "is_winner",
        )
        PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        ALLIED_HERO_IDS_FIELD_NUMBER: _ClassVar[int]
        ENEMY_HERO_IDS_FIELD_NUMBER: _ClassVar[int]
        ITEM_PURCHASES_FIELD_NUMBER: _ClassVar[int]
        LANE_FIELD_NUMBER: _ClassVar[int]
        IS_WINNER_FIELD_NUMBER: _ClassVar[int]
        player_slot: int
        account_id: int
        hero_id: int
        allied_hero_ids: _containers.RepeatedScalarFieldContainer[int]
        enemy_hero_ids: _containers.RepeatedScalarFieldContainer[int]
        item_purchases: _containers.RepeatedCompositeFieldContainer[
            CMsgServerToGCMatchPlayerItemPurchaseHistory.ItemPurchase
        ]
        lane: int
        is_winner: bool
        def __init__(
            self,
            player_slot: int | None = ...,
            account_id: int | None = ...,
            hero_id: int | None = ...,
            allied_hero_ids: _Iterable[int] | None = ...,
            enemy_hero_ids: _Iterable[int] | None = ...,
            item_purchases: _Iterable[
                CMsgServerToGCMatchPlayerItemPurchaseHistory.ItemPurchase | _Mapping
            ]
            | None = ...,
            lane: int | None = ...,
            is_winner: bool = ...,
        ) -> None: ...

    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    MMR_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    mmr: int
    players: _containers.RepeatedCompositeFieldContainer[
        CMsgServerToGCMatchPlayerItemPurchaseHistory.Player
    ]
    def __init__(
        self,
        match_id: int | None = ...,
        mmr: int | None = ...,
        players: _Iterable[CMsgServerToGCMatchPlayerItemPurchaseHistory.Player | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgServerToGCMatchPlayerNeutralItemEquipHistory(_message.Message):
    __slots__ = ("match_id", "players")
    class ItemEquip(_message.Message):
        __slots__ = (
            "item",
            "game_time",
            "inventory_items",
            "talents_skilled",
            "available_neutral_items",
        )
        ITEM_FIELD_NUMBER: _ClassVar[int]
        GAME_TIME_FIELD_NUMBER: _ClassVar[int]
        INVENTORY_ITEMS_FIELD_NUMBER: _ClassVar[int]
        TALENTS_SKILLED_FIELD_NUMBER: _ClassVar[int]
        AVAILABLE_NEUTRAL_ITEMS_FIELD_NUMBER: _ClassVar[int]
        item: int
        game_time: int
        inventory_items: _containers.RepeatedScalarFieldContainer[int]
        talents_skilled: _containers.RepeatedScalarFieldContainer[bool]
        available_neutral_items: _containers.RepeatedScalarFieldContainer[int]
        def __init__(
            self,
            item: int | None = ...,
            game_time: int | None = ...,
            inventory_items: _Iterable[int] | None = ...,
            talents_skilled: _Iterable[bool] | None = ...,
            available_neutral_items: _Iterable[int] | None = ...,
        ) -> None: ...

    class Player(_message.Message):
        __slots__ = ("account_id", "allied_hero_ids", "enemy_hero_ids", "item_equips", "is_winner")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        ALLIED_HERO_IDS_FIELD_NUMBER: _ClassVar[int]
        ENEMY_HERO_IDS_FIELD_NUMBER: _ClassVar[int]
        ITEM_EQUIPS_FIELD_NUMBER: _ClassVar[int]
        IS_WINNER_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        allied_hero_ids: _containers.RepeatedScalarFieldContainer[int]
        enemy_hero_ids: _containers.RepeatedScalarFieldContainer[int]
        item_equips: _containers.RepeatedCompositeFieldContainer[
            CMsgServerToGCMatchPlayerNeutralItemEquipHistory.ItemEquip
        ]
        is_winner: bool
        def __init__(
            self,
            account_id: int | None = ...,
            allied_hero_ids: _Iterable[int] | None = ...,
            enemy_hero_ids: _Iterable[int] | None = ...,
            item_equips: _Iterable[
                CMsgServerToGCMatchPlayerNeutralItemEquipHistory.ItemEquip | _Mapping
            ]
            | None = ...,
            is_winner: bool = ...,
        ) -> None: ...

    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    players: _containers.RepeatedCompositeFieldContainer[
        CMsgServerToGCMatchPlayerNeutralItemEquipHistory.Player
    ]
    def __init__(
        self,
        match_id: int | None = ...,
        players: _Iterable[CMsgServerToGCMatchPlayerNeutralItemEquipHistory.Player | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgServerToGCMatchStateHistory(_message.Message):
    __slots__ = ("match_id", "radiant_won", "mmr", "match_states")
    class PlayerState(_message.Message):
        __slots__ = (
            "hero_id",
            "net_worth",
            "level",
            "deaths",
            "respawn_time",
            "has_buyback",
            "has_aegis",
            "has_rapier",
            "distance",
        )
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        NET_WORTH_FIELD_NUMBER: _ClassVar[int]
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        DEATHS_FIELD_NUMBER: _ClassVar[int]
        RESPAWN_TIME_FIELD_NUMBER: _ClassVar[int]
        HAS_BUYBACK_FIELD_NUMBER: _ClassVar[int]
        HAS_AEGIS_FIELD_NUMBER: _ClassVar[int]
        HAS_RAPIER_FIELD_NUMBER: _ClassVar[int]
        DISTANCE_FIELD_NUMBER: _ClassVar[int]
        hero_id: int
        net_worth: int
        level: int
        deaths: int
        respawn_time: int
        has_buyback: bool
        has_aegis: bool
        has_rapier: bool
        distance: int
        def __init__(
            self,
            hero_id: int | None = ...,
            net_worth: int | None = ...,
            level: int | None = ...,
            deaths: int | None = ...,
            respawn_time: int | None = ...,
            has_buyback: bool = ...,
            has_aegis: bool = ...,
            has_rapier: bool = ...,
            distance: int | None = ...,
        ) -> None: ...

    class TeamState(_message.Message):
        __slots__ = (
            "team",
            "player_states",
            "tower_health_pct",
            "barracks_health_pct",
            "ancient_health_pct",
            "glyph_cooldown",
            "kills",
            "creep_distance_safe",
            "creep_distance_mid",
            "creep_distance_off",
        )
        TEAM_FIELD_NUMBER: _ClassVar[int]
        PLAYER_STATES_FIELD_NUMBER: _ClassVar[int]
        TOWER_HEALTH_PCT_FIELD_NUMBER: _ClassVar[int]
        BARRACKS_HEALTH_PCT_FIELD_NUMBER: _ClassVar[int]
        ANCIENT_HEALTH_PCT_FIELD_NUMBER: _ClassVar[int]
        GLYPH_COOLDOWN_FIELD_NUMBER: _ClassVar[int]
        KILLS_FIELD_NUMBER: _ClassVar[int]
        CREEP_DISTANCE_SAFE_FIELD_NUMBER: _ClassVar[int]
        CREEP_DISTANCE_MID_FIELD_NUMBER: _ClassVar[int]
        CREEP_DISTANCE_OFF_FIELD_NUMBER: _ClassVar[int]
        team: int
        player_states: _containers.RepeatedCompositeFieldContainer[
            CMsgServerToGCMatchStateHistory.PlayerState
        ]
        tower_health_pct: _containers.RepeatedScalarFieldContainer[int]
        barracks_health_pct: _containers.RepeatedScalarFieldContainer[int]
        ancient_health_pct: int
        glyph_cooldown: int
        kills: int
        creep_distance_safe: int
        creep_distance_mid: int
        creep_distance_off: int
        def __init__(
            self,
            team: int | None = ...,
            player_states: _Iterable[CMsgServerToGCMatchStateHistory.PlayerState | _Mapping]
            | None = ...,
            tower_health_pct: _Iterable[int] | None = ...,
            barracks_health_pct: _Iterable[int] | None = ...,
            ancient_health_pct: int | None = ...,
            glyph_cooldown: int | None = ...,
            kills: int | None = ...,
            creep_distance_safe: int | None = ...,
            creep_distance_mid: int | None = ...,
            creep_distance_off: int | None = ...,
        ) -> None: ...

    class MatchState(_message.Message):
        __slots__ = ("game_time", "radiant_state", "dire_state")
        GAME_TIME_FIELD_NUMBER: _ClassVar[int]
        RADIANT_STATE_FIELD_NUMBER: _ClassVar[int]
        DIRE_STATE_FIELD_NUMBER: _ClassVar[int]
        game_time: int
        radiant_state: CMsgServerToGCMatchStateHistory.TeamState
        dire_state: CMsgServerToGCMatchStateHistory.TeamState
        def __init__(
            self,
            game_time: int | None = ...,
            radiant_state: CMsgServerToGCMatchStateHistory.TeamState | _Mapping | None = ...,
            dire_state: CMsgServerToGCMatchStateHistory.TeamState | _Mapping | None = ...,
        ) -> None: ...

    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    RADIANT_WON_FIELD_NUMBER: _ClassVar[int]
    MMR_FIELD_NUMBER: _ClassVar[int]
    MATCH_STATES_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    radiant_won: bool
    mmr: int
    match_states: _containers.RepeatedCompositeFieldContainer[
        CMsgServerToGCMatchStateHistory.MatchState
    ]
    def __init__(
        self,
        match_id: int | None = ...,
        radiant_won: bool = ...,
        mmr: int | None = ...,
        match_states: _Iterable[CMsgServerToGCMatchStateHistory.MatchState | _Mapping] | None = ...,
    ) -> None: ...

class CMsgMatchStateSteamMLEntry(_message.Message):
    __slots__ = ("match_state", "mmr", "radiant_won")
    MATCH_STATE_FIELD_NUMBER: _ClassVar[int]
    MMR_FIELD_NUMBER: _ClassVar[int]
    RADIANT_WON_FIELD_NUMBER: _ClassVar[int]
    match_state: CMsgServerToGCMatchStateHistory.MatchState
    mmr: int
    radiant_won: bool
    def __init__(
        self,
        match_state: CMsgServerToGCMatchStateHistory.MatchState | _Mapping | None = ...,
        mmr: int | None = ...,
        radiant_won: bool = ...,
    ) -> None: ...

class CMsgLaneSelectionSteamMLEntry(_message.Message):
    __slots__ = ("hero_ids", "lanes")
    HERO_IDS_FIELD_NUMBER: _ClassVar[int]
    LANES_FIELD_NUMBER: _ClassVar[int]
    hero_ids: _containers.RepeatedScalarFieldContainer[int]
    lanes: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self, hero_ids: _Iterable[int] | None = ..., lanes: _Iterable[int] | None = ...
    ) -> None: ...

class CMsgAbilitySelectionSteamMLEntry(_message.Message):
    __slots__ = ("mmr", "hero_id", "enemy_hero_ids", "lane", "abilities", "selected_ability")
    MMR_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    ENEMY_HERO_IDS_FIELD_NUMBER: _ClassVar[int]
    LANE_FIELD_NUMBER: _ClassVar[int]
    ABILITIES_FIELD_NUMBER: _ClassVar[int]
    SELECTED_ABILITY_FIELD_NUMBER: _ClassVar[int]
    mmr: int
    hero_id: int
    enemy_hero_ids: _containers.RepeatedScalarFieldContainer[int]
    lane: int
    abilities: _containers.RepeatedScalarFieldContainer[int]
    selected_ability: int
    def __init__(
        self,
        mmr: int | None = ...,
        hero_id: int | None = ...,
        enemy_hero_ids: _Iterable[int] | None = ...,
        lane: int | None = ...,
        abilities: _Iterable[int] | None = ...,
        selected_ability: int | None = ...,
    ) -> None: ...

class CMsgItemPurchasePregameSteamMLEntry(_message.Message):
    __slots__ = ("mmr", "lane", "balance", "hero_id", "allied_hero_ids", "enemy_hero_ids", "items")
    MMR_FIELD_NUMBER: _ClassVar[int]
    LANE_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    ALLIED_HERO_IDS_FIELD_NUMBER: _ClassVar[int]
    ENEMY_HERO_IDS_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    mmr: int
    lane: int
    balance: float
    hero_id: int
    allied_hero_ids: _containers.RepeatedScalarFieldContainer[int]
    enemy_hero_ids: _containers.RepeatedScalarFieldContainer[int]
    items: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        mmr: int | None = ...,
        lane: int | None = ...,
        balance: float | None = ...,
        hero_id: int | None = ...,
        allied_hero_ids: _Iterable[int] | None = ...,
        enemy_hero_ids: _Iterable[int] | None = ...,
        items: _Iterable[int] | None = ...,
    ) -> None: ...

class CMsgItemPurchaseSteamMLEntry(_message.Message):
    __slots__ = (
        "mmr",
        "lane",
        "hero_id",
        "allied_hero_ids",
        "enemy_hero_ids",
        "items",
        "items_to_be_purchased",
    )
    MMR_FIELD_NUMBER: _ClassVar[int]
    LANE_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    ALLIED_HERO_IDS_FIELD_NUMBER: _ClassVar[int]
    ENEMY_HERO_IDS_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    ITEMS_TO_BE_PURCHASED_FIELD_NUMBER: _ClassVar[int]
    mmr: int
    lane: int
    hero_id: int
    allied_hero_ids: _containers.RepeatedScalarFieldContainer[int]
    enemy_hero_ids: _containers.RepeatedScalarFieldContainer[int]
    items: _containers.RepeatedScalarFieldContainer[int]
    items_to_be_purchased: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        mmr: int | None = ...,
        lane: int | None = ...,
        hero_id: int | None = ...,
        allied_hero_ids: _Iterable[int] | None = ...,
        enemy_hero_ids: _Iterable[int] | None = ...,
        items: _Iterable[int] | None = ...,
        items_to_be_purchased: _Iterable[int] | None = ...,
    ) -> None: ...

class CMsgItemPurchaseSequenceSteamMLEntry(_message.Message):
    __slots__ = (
        "mmr",
        "lane",
        "hero_id",
        "allied_hero_ids",
        "enemy_hero_ids",
        "items",
        "item_to_be_purchased",
    )
    MMR_FIELD_NUMBER: _ClassVar[int]
    LANE_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    ALLIED_HERO_IDS_FIELD_NUMBER: _ClassVar[int]
    ENEMY_HERO_IDS_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    ITEM_TO_BE_PURCHASED_FIELD_NUMBER: _ClassVar[int]
    mmr: int
    lane: int
    hero_id: int
    allied_hero_ids: _containers.RepeatedScalarFieldContainer[int]
    enemy_hero_ids: _containers.RepeatedScalarFieldContainer[int]
    items: _containers.RepeatedScalarFieldContainer[int]
    item_to_be_purchased: int
    def __init__(
        self,
        mmr: int | None = ...,
        lane: int | None = ...,
        hero_id: int | None = ...,
        allied_hero_ids: _Iterable[int] | None = ...,
        enemy_hero_ids: _Iterable[int] | None = ...,
        items: _Iterable[int] | None = ...,
        item_to_be_purchased: int | None = ...,
    ) -> None: ...

class CMsgServerToGCCavernCrawlIsHeroActive(_message.Message):
    __slots__ = ("event_id", "account_id", "preferred_map_variant", "hero_id", "turbo_mode")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    PREFERRED_MAP_VARIANT_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    TURBO_MODE_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    account_id: int
    preferred_map_variant: int
    hero_id: int
    turbo_mode: bool
    def __init__(
        self,
        event_id: int | None = ...,
        account_id: int | None = ...,
        preferred_map_variant: int | None = ...,
        hero_id: int | None = ...,
        turbo_mode: bool = ...,
    ) -> None: ...

class CMsgServerToGCPlayerChallengeHistory(_message.Message):
    __slots__ = ("match_id", "average_rank", "challenge_records")
    class PlayerChallenge(_message.Message):
        __slots__ = (
            "account_id",
            "challenge_type",
            "challenge_id1",
            "challenge_id2",
            "progress_value_start",
            "progress_value_end",
            "team_won",
            "audit_data",
            "hero_id",
            "rank_completed",
        )
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        CHALLENGE_TYPE_FIELD_NUMBER: _ClassVar[int]
        CHALLENGE_ID1_FIELD_NUMBER: _ClassVar[int]
        CHALLENGE_ID2_FIELD_NUMBER: _ClassVar[int]
        PROGRESS_VALUE_START_FIELD_NUMBER: _ClassVar[int]
        PROGRESS_VALUE_END_FIELD_NUMBER: _ClassVar[int]
        TEAM_WON_FIELD_NUMBER: _ClassVar[int]
        AUDIT_DATA_FIELD_NUMBER: _ClassVar[int]
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        RANK_COMPLETED_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        challenge_type: _dota_shared_enums_pb2.EPlayerChallengeHistoryType
        challenge_id1: int
        challenge_id2: int
        progress_value_start: int
        progress_value_end: int
        team_won: bool
        audit_data: int
        hero_id: int
        rank_completed: int
        def __init__(
            self,
            account_id: int | None = ...,
            challenge_type: _dota_shared_enums_pb2.EPlayerChallengeHistoryType | str | None = ...,
            challenge_id1: int | None = ...,
            challenge_id2: int | None = ...,
            progress_value_start: int | None = ...,
            progress_value_end: int | None = ...,
            team_won: bool = ...,
            audit_data: int | None = ...,
            hero_id: int | None = ...,
            rank_completed: int | None = ...,
        ) -> None: ...

    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_RANK_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_RECORDS_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    average_rank: int
    challenge_records: _containers.RepeatedCompositeFieldContainer[
        CMsgServerToGCPlayerChallengeHistory.PlayerChallenge
    ]
    def __init__(
        self,
        match_id: int | None = ...,
        average_rank: int | None = ...,
        challenge_records: _Iterable[
            CMsgServerToGCPlayerChallengeHistory.PlayerChallenge | _Mapping
        ]
        | None = ...,
    ) -> None: ...

class CMsgServerToGCCavernCrawlIsHeroActiveResponse(_message.Message):
    __slots__ = (
        "result",
        "map_variant",
        "potential_winnings",
        "map_results",
        "potential_plus_shard_winnings",
    )
    class MapResults(_message.Message):
        __slots__ = ("path_id_completed", "room_id_claimed")
        PATH_ID_COMPLETED_FIELD_NUMBER: _ClassVar[int]
        ROOM_ID_CLAIMED_FIELD_NUMBER: _ClassVar[int]
        path_id_completed: int
        room_id_claimed: int
        def __init__(
            self, path_id_completed: int | None = ..., room_id_claimed: int | None = ...
        ) -> None: ...

    RESULT_FIELD_NUMBER: _ClassVar[int]
    MAP_VARIANT_FIELD_NUMBER: _ClassVar[int]
    POTENTIAL_WINNINGS_FIELD_NUMBER: _ClassVar[int]
    MAP_RESULTS_FIELD_NUMBER: _ClassVar[int]
    POTENTIAL_PLUS_SHARD_WINNINGS_FIELD_NUMBER: _ClassVar[int]
    result: bool
    map_variant: int
    potential_winnings: int
    map_results: _containers.RepeatedCompositeFieldContainer[
        CMsgServerToGCCavernCrawlIsHeroActiveResponse.MapResults
    ]
    potential_plus_shard_winnings: int
    def __init__(
        self,
        result: bool = ...,
        map_variant: int | None = ...,
        potential_winnings: int | None = ...,
        map_results: _Iterable[CMsgServerToGCCavernCrawlIsHeroActiveResponse.MapResults | _Mapping]
        | None = ...,
        potential_plus_shard_winnings: int | None = ...,
    ) -> None: ...

class CMsgNeutralItemStats(_message.Message):
    __slots__ = ("neutral_items",)
    class NeutralItem(_message.Message):
        __slots__ = (
            "item_id",
            "time_dropped",
            "team",
            "time_last_equipped",
            "time_last_unequipped",
            "duration_equipped",
        )
        ITEM_ID_FIELD_NUMBER: _ClassVar[int]
        TIME_DROPPED_FIELD_NUMBER: _ClassVar[int]
        TEAM_FIELD_NUMBER: _ClassVar[int]
        TIME_LAST_EQUIPPED_FIELD_NUMBER: _ClassVar[int]
        TIME_LAST_UNEQUIPPED_FIELD_NUMBER: _ClassVar[int]
        DURATION_EQUIPPED_FIELD_NUMBER: _ClassVar[int]
        item_id: int
        time_dropped: int
        team: int
        time_last_equipped: int
        time_last_unequipped: int
        duration_equipped: int
        def __init__(
            self,
            item_id: int | None = ...,
            time_dropped: int | None = ...,
            team: int | None = ...,
            time_last_equipped: int | None = ...,
            time_last_unequipped: int | None = ...,
            duration_equipped: int | None = ...,
        ) -> None: ...

    NEUTRAL_ITEMS_FIELD_NUMBER: _ClassVar[int]
    neutral_items: _containers.RepeatedCompositeFieldContainer[CMsgNeutralItemStats.NeutralItem]
    def __init__(
        self, neutral_items: _Iterable[CMsgNeutralItemStats.NeutralItem | _Mapping] | None = ...
    ) -> None: ...

class CMsgGCToServerLobbyHeroBanRates(_message.Message):
    __slots__ = ("ban_data",)
    class HeroBanEntry(_message.Message):
        __slots__ = ("hero_id", "ban_count", "pick_count")
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        BAN_COUNT_FIELD_NUMBER: _ClassVar[int]
        PICK_COUNT_FIELD_NUMBER: _ClassVar[int]
        hero_id: int
        ban_count: int
        pick_count: int
        def __init__(
            self,
            hero_id: int | None = ...,
            ban_count: int | None = ...,
            pick_count: int | None = ...,
        ) -> None: ...

    BAN_DATA_FIELD_NUMBER: _ClassVar[int]
    ban_data: _containers.RepeatedCompositeFieldContainer[
        CMsgGCToServerLobbyHeroBanRates.HeroBanEntry
    ]
    def __init__(
        self,
        ban_data: _Iterable[CMsgGCToServerLobbyHeroBanRates.HeroBanEntry | _Mapping] | None = ...,
    ) -> None: ...

class CMsgSignOutGuildContractProgress(_message.Message):
    __slots__ = ("player_contracts",)
    class CompletedGuildEventContracts(_message.Message):
        __slots__ = ("guild_id", "event_id", "contracts")
        GUILD_ID_FIELD_NUMBER: _ClassVar[int]
        EVENT_ID_FIELD_NUMBER: _ClassVar[int]
        CONTRACTS_FIELD_NUMBER: _ClassVar[int]
        guild_id: int
        event_id: int
        contracts: _containers.RepeatedScalarFieldContainer[int]
        def __init__(
            self,
            guild_id: int | None = ...,
            event_id: int | None = ...,
            contracts: _Iterable[int] | None = ...,
        ) -> None: ...

    class PlayerContract(_message.Message):
        __slots__ = ("account_id", "completed_contracts")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        COMPLETED_CONTRACTS_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        completed_contracts: _containers.RepeatedCompositeFieldContainer[
            CMsgSignOutGuildContractProgress.CompletedGuildEventContracts
        ]
        def __init__(
            self,
            account_id: int | None = ...,
            completed_contracts: _Iterable[
                CMsgSignOutGuildContractProgress.CompletedGuildEventContracts | _Mapping
            ]
            | None = ...,
        ) -> None: ...

    PLAYER_CONTRACTS_FIELD_NUMBER: _ClassVar[int]
    player_contracts: _containers.RepeatedCompositeFieldContainer[
        CMsgSignOutGuildContractProgress.PlayerContract
    ]
    def __init__(
        self,
        player_contracts: _Iterable[CMsgSignOutGuildContractProgress.PlayerContract | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgSignOutGuildChallengeProgress(_message.Message):
    __slots__ = ("guild_challenges_progresses",)
    class ChallengeProgress(_message.Message):
        __slots__ = (
            "guild_id",
            "event_id",
            "challenge_instance_id",
            "challenge_instance_timestamp",
            "challenge_period_serial",
            "progress",
            "challenge_parameter",
        )
        GUILD_ID_FIELD_NUMBER: _ClassVar[int]
        EVENT_ID_FIELD_NUMBER: _ClassVar[int]
        CHALLENGE_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
        CHALLENGE_INSTANCE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        CHALLENGE_PERIOD_SERIAL_FIELD_NUMBER: _ClassVar[int]
        PROGRESS_FIELD_NUMBER: _ClassVar[int]
        CHALLENGE_PARAMETER_FIELD_NUMBER: _ClassVar[int]
        guild_id: int
        event_id: int
        challenge_instance_id: int
        challenge_instance_timestamp: int
        challenge_period_serial: int
        progress: int
        challenge_parameter: int
        def __init__(
            self,
            guild_id: int | None = ...,
            event_id: int | None = ...,
            challenge_instance_id: int | None = ...,
            challenge_instance_timestamp: int | None = ...,
            challenge_period_serial: int | None = ...,
            progress: int | None = ...,
            challenge_parameter: int | None = ...,
        ) -> None: ...

    GUILD_CHALLENGES_PROGRESSES_FIELD_NUMBER: _ClassVar[int]
    guild_challenges_progresses: _containers.RepeatedCompositeFieldContainer[
        CMsgSignOutGuildChallengeProgress.ChallengeProgress
    ]
    def __init__(
        self,
        guild_challenges_progresses: _Iterable[
            CMsgSignOutGuildChallengeProgress.ChallengeProgress | _Mapping
        ]
        | None = ...,
    ) -> None: ...

class CMsgSignOutMVPStats(_message.Message):
    __slots__ = ("match_id", "game_mode", "winning_team", "game_time", "players")
    class Player(_message.Message):
        __slots__ = (
            "team_id",
            "team_networth_rank",
            "account_id",
            "player_slot",
            "rank",
            "hero_id",
            "role",
            "kills",
            "deaths",
            "assists",
            "xp",
            "net_worth",
            "support_gold_spent",
            "wards_placed",
            "wards_spotted_for_dewarding",
            "camps_stacked",
            "last_hits",
            "denies",
            "building_damage",
            "other_damage",
            "triple_kills",
            "rampages",
            "first_blood",
            "kill_eater_events",
            "highest_killstreak",
        )
        class KillEaterEvent(_message.Message):
            __slots__ = ("event_type", "amount")
            EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
            AMOUNT_FIELD_NUMBER: _ClassVar[int]
            event_type: int
            amount: int
            def __init__(self, event_type: int | None = ..., amount: int | None = ...) -> None: ...

        TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        TEAM_NETWORTH_RANK_FIELD_NUMBER: _ClassVar[int]
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
        RANK_FIELD_NUMBER: _ClassVar[int]
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        ROLE_FIELD_NUMBER: _ClassVar[int]
        KILLS_FIELD_NUMBER: _ClassVar[int]
        DEATHS_FIELD_NUMBER: _ClassVar[int]
        ASSISTS_FIELD_NUMBER: _ClassVar[int]
        XP_FIELD_NUMBER: _ClassVar[int]
        NET_WORTH_FIELD_NUMBER: _ClassVar[int]
        SUPPORT_GOLD_SPENT_FIELD_NUMBER: _ClassVar[int]
        WARDS_PLACED_FIELD_NUMBER: _ClassVar[int]
        WARDS_SPOTTED_FOR_DEWARDING_FIELD_NUMBER: _ClassVar[int]
        CAMPS_STACKED_FIELD_NUMBER: _ClassVar[int]
        LAST_HITS_FIELD_NUMBER: _ClassVar[int]
        DENIES_FIELD_NUMBER: _ClassVar[int]
        BUILDING_DAMAGE_FIELD_NUMBER: _ClassVar[int]
        OTHER_DAMAGE_FIELD_NUMBER: _ClassVar[int]
        TRIPLE_KILLS_FIELD_NUMBER: _ClassVar[int]
        RAMPAGES_FIELD_NUMBER: _ClassVar[int]
        FIRST_BLOOD_FIELD_NUMBER: _ClassVar[int]
        KILL_EATER_EVENTS_FIELD_NUMBER: _ClassVar[int]
        HIGHEST_KILLSTREAK_FIELD_NUMBER: _ClassVar[int]
        team_id: int
        team_networth_rank: int
        account_id: int
        player_slot: int
        rank: int
        hero_id: int
        role: int
        kills: int
        deaths: int
        assists: int
        xp: int
        net_worth: int
        support_gold_spent: int
        wards_placed: int
        wards_spotted_for_dewarding: int
        camps_stacked: int
        last_hits: int
        denies: int
        building_damage: int
        other_damage: int
        triple_kills: int
        rampages: int
        first_blood: int
        kill_eater_events: _containers.RepeatedCompositeFieldContainer[
            CMsgSignOutMVPStats.Player.KillEaterEvent
        ]
        highest_killstreak: int
        def __init__(
            self,
            team_id: int | None = ...,
            team_networth_rank: int | None = ...,
            account_id: int | None = ...,
            player_slot: int | None = ...,
            rank: int | None = ...,
            hero_id: int | None = ...,
            role: int | None = ...,
            kills: int | None = ...,
            deaths: int | None = ...,
            assists: int | None = ...,
            xp: int | None = ...,
            net_worth: int | None = ...,
            support_gold_spent: int | None = ...,
            wards_placed: int | None = ...,
            wards_spotted_for_dewarding: int | None = ...,
            camps_stacked: int | None = ...,
            last_hits: int | None = ...,
            denies: int | None = ...,
            building_damage: int | None = ...,
            other_damage: int | None = ...,
            triple_kills: int | None = ...,
            rampages: int | None = ...,
            first_blood: int | None = ...,
            kill_eater_events: _Iterable[CMsgSignOutMVPStats.Player.KillEaterEvent | _Mapping]
            | None = ...,
            highest_killstreak: int | None = ...,
        ) -> None: ...

    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    GAME_MODE_FIELD_NUMBER: _ClassVar[int]
    WINNING_TEAM_FIELD_NUMBER: _ClassVar[int]
    GAME_TIME_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    game_mode: int
    winning_team: int
    game_time: float
    players: _containers.RepeatedCompositeFieldContainer[CMsgSignOutMVPStats.Player]
    def __init__(
        self,
        match_id: int | None = ...,
        game_mode: int | None = ...,
        winning_team: int | None = ...,
        game_time: float | None = ...,
        players: _Iterable[CMsgSignOutMVPStats.Player | _Mapping] | None = ...,
    ) -> None: ...

class CMsgServerToGCGetGuildContracts(_message.Message):
    __slots__ = ("account_ids",)
    ACCOUNT_IDS_FIELD_NUMBER: _ClassVar[int]
    account_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, account_ids: _Iterable[int] | None = ...) -> None: ...

class CMsgServerToGCGetGuildContractsResponse(_message.Message):
    __slots__ = ("player_contracts",)
    class ContractDetails(_message.Message):
        __slots__ = (
            "contract_id",
            "challenge_instance_id",
            "challenge_parameter",
            "contract_stars",
            "contract_slot",
        )
        CONTRACT_ID_FIELD_NUMBER: _ClassVar[int]
        CHALLENGE_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
        CHALLENGE_PARAMETER_FIELD_NUMBER: _ClassVar[int]
        CONTRACT_STARS_FIELD_NUMBER: _ClassVar[int]
        CONTRACT_SLOT_FIELD_NUMBER: _ClassVar[int]
        contract_id: int
        challenge_instance_id: int
        challenge_parameter: int
        contract_stars: int
        contract_slot: int
        def __init__(
            self,
            contract_id: int | None = ...,
            challenge_instance_id: int | None = ...,
            challenge_parameter: int | None = ...,
            contract_stars: int | None = ...,
            contract_slot: int | None = ...,
        ) -> None: ...

    class Player(_message.Message):
        __slots__ = ("account_id", "guild_id", "event_id", "contracts")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        GUILD_ID_FIELD_NUMBER: _ClassVar[int]
        EVENT_ID_FIELD_NUMBER: _ClassVar[int]
        CONTRACTS_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        guild_id: int
        event_id: _dota_shared_enums_pb2.EEvent
        contracts: _containers.RepeatedCompositeFieldContainer[
            CMsgServerToGCGetGuildContractsResponse.ContractDetails
        ]
        def __init__(
            self,
            account_id: int | None = ...,
            guild_id: int | None = ...,
            event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
            contracts: _Iterable[CMsgServerToGCGetGuildContractsResponse.ContractDetails | _Mapping]
            | None = ...,
        ) -> None: ...

    PLAYER_CONTRACTS_FIELD_NUMBER: _ClassVar[int]
    player_contracts: _containers.RepeatedCompositeFieldContainer[
        CMsgServerToGCGetGuildContractsResponse.Player
    ]
    def __init__(
        self,
        player_contracts: _Iterable[CMsgServerToGCGetGuildContractsResponse.Player | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgMatchDiretideCandy(_message.Message):
    __slots__ = ("player_candy_data", "event_id")
    class CandyDetails(_message.Message):
        __slots__ = ("amount", "audit")
        AMOUNT_FIELD_NUMBER: _ClassVar[int]
        AUDIT_FIELD_NUMBER: _ClassVar[int]
        amount: int
        audit: int
        def __init__(self, amount: int | None = ..., audit: int | None = ...) -> None: ...

    class PlayerCandy(_message.Message):
        __slots__ = ("account_id", "candy_amount", "consumes_periodic_resource", "candy_breakdown")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        CANDY_AMOUNT_FIELD_NUMBER: _ClassVar[int]
        CONSUMES_PERIODIC_RESOURCE_FIELD_NUMBER: _ClassVar[int]
        CANDY_BREAKDOWN_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        candy_amount: int
        consumes_periodic_resource: bool
        candy_breakdown: _containers.RepeatedCompositeFieldContainer[
            CMsgMatchDiretideCandy.CandyDetails
        ]
        def __init__(
            self,
            account_id: int | None = ...,
            candy_amount: int | None = ...,
            consumes_periodic_resource: bool = ...,
            candy_breakdown: _Iterable[CMsgMatchDiretideCandy.CandyDetails | _Mapping] | None = ...,
        ) -> None: ...

    PLAYER_CANDY_DATA_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    player_candy_data: _containers.RepeatedCompositeFieldContainer[
        CMsgMatchDiretideCandy.PlayerCandy
    ]
    event_id: _dota_shared_enums_pb2.EEvent
    def __init__(
        self,
        player_candy_data: _Iterable[CMsgMatchDiretideCandy.PlayerCandy | _Mapping] | None = ...,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
    ) -> None: ...

class CMsgGCToServerCheerData(_message.Message):
    __slots__ = ("cheer_types",)
    class CheerTypeCount(_message.Message):
        __slots__ = ("cheer_type", "cheer_count")
        CHEER_TYPE_FIELD_NUMBER: _ClassVar[int]
        CHEER_COUNT_FIELD_NUMBER: _ClassVar[int]
        cheer_type: int
        cheer_count: int
        def __init__(self, cheer_type: int | None = ..., cheer_count: int | None = ...) -> None: ...

    CHEER_TYPES_FIELD_NUMBER: _ClassVar[int]
    cheer_types: _containers.RepeatedCompositeFieldContainer[CMsgGCToServerCheerData.CheerTypeCount]
    def __init__(
        self, cheer_types: _Iterable[CMsgGCToServerCheerData.CheerTypeCount | _Mapping] | None = ...
    ) -> None: ...

class CMsgCheerConfig(_message.Message):
    __slots__ = (
        "cheers_enabled",
        "is_valid_league_id",
        "window_duration",
        "window_bucket_count",
        "crowd_level_push_time",
        "crowd_level_low",
        "crowd_level_medium",
        "crowd_level_high",
        "cheer_scale_start",
        "cheer_scale_speed",
        "cheer_scale_push_mark",
        "cheer_scale_pull_mark",
        "cheer_scale_pct_of_max_cps_clamp",
        "cheer_scale_dampener_value",
        "cheer_scale_dampener_lerp_time",
        "cheer_factor_bronze",
        "cheer_factor_silver",
        "cheer_factor_gold",
    )
    CHEERS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    IS_VALID_LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    WINDOW_DURATION_FIELD_NUMBER: _ClassVar[int]
    WINDOW_BUCKET_COUNT_FIELD_NUMBER: _ClassVar[int]
    CROWD_LEVEL_PUSH_TIME_FIELD_NUMBER: _ClassVar[int]
    CROWD_LEVEL_LOW_FIELD_NUMBER: _ClassVar[int]
    CROWD_LEVEL_MEDIUM_FIELD_NUMBER: _ClassVar[int]
    CROWD_LEVEL_HIGH_FIELD_NUMBER: _ClassVar[int]
    CHEER_SCALE_START_FIELD_NUMBER: _ClassVar[int]
    CHEER_SCALE_SPEED_FIELD_NUMBER: _ClassVar[int]
    CHEER_SCALE_PUSH_MARK_FIELD_NUMBER: _ClassVar[int]
    CHEER_SCALE_PULL_MARK_FIELD_NUMBER: _ClassVar[int]
    CHEER_SCALE_PCT_OF_MAX_CPS_CLAMP_FIELD_NUMBER: _ClassVar[int]
    CHEER_SCALE_DAMPENER_VALUE_FIELD_NUMBER: _ClassVar[int]
    CHEER_SCALE_DAMPENER_LERP_TIME_FIELD_NUMBER: _ClassVar[int]
    CHEER_FACTOR_BRONZE_FIELD_NUMBER: _ClassVar[int]
    CHEER_FACTOR_SILVER_FIELD_NUMBER: _ClassVar[int]
    CHEER_FACTOR_GOLD_FIELD_NUMBER: _ClassVar[int]
    cheers_enabled: bool
    is_valid_league_id: bool
    window_duration: float
    window_bucket_count: int
    crowd_level_push_time: float
    crowd_level_low: int
    crowd_level_medium: int
    crowd_level_high: int
    cheer_scale_start: float
    cheer_scale_speed: float
    cheer_scale_push_mark: int
    cheer_scale_pull_mark: int
    cheer_scale_pct_of_max_cps_clamp: float
    cheer_scale_dampener_value: float
    cheer_scale_dampener_lerp_time: int
    cheer_factor_bronze: float
    cheer_factor_silver: float
    cheer_factor_gold: float
    def __init__(
        self,
        cheers_enabled: bool = ...,
        is_valid_league_id: bool = ...,
        window_duration: float | None = ...,
        window_bucket_count: int | None = ...,
        crowd_level_push_time: float | None = ...,
        crowd_level_low: int | None = ...,
        crowd_level_medium: int | None = ...,
        crowd_level_high: int | None = ...,
        cheer_scale_start: float | None = ...,
        cheer_scale_speed: float | None = ...,
        cheer_scale_push_mark: int | None = ...,
        cheer_scale_pull_mark: int | None = ...,
        cheer_scale_pct_of_max_cps_clamp: float | None = ...,
        cheer_scale_dampener_value: float | None = ...,
        cheer_scale_dampener_lerp_time: int | None = ...,
        cheer_factor_bronze: float | None = ...,
        cheer_factor_silver: float | None = ...,
        cheer_factor_gold: float | None = ...,
    ) -> None: ...

class CMsgGCToServerCheerConfig(_message.Message):
    __slots__ = ("cheer_config",)
    CHEER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    cheer_config: CMsgCheerConfig
    def __init__(self, cheer_config: CMsgCheerConfig | _Mapping | None = ...) -> None: ...

class CMsgServerToGCGetCheerConfig(_message.Message):
    __slots__ = ("league_id",)
    LEAGUE_ID_FIELD_NUMBER: _ClassVar[int]
    league_id: int
    def __init__(self, league_id: int | None = ...) -> None: ...

class CMsgServerToGCGetCheerConfigResponse(_message.Message):
    __slots__ = ("cheer_config",)
    CHEER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    cheer_config: CMsgCheerConfig
    def __init__(self, cheer_config: CMsgCheerConfig | _Mapping | None = ...) -> None: ...

class CMsgGCToServerCheerScalesOverride(_message.Message):
    __slots__ = ("scales",)
    SCALES_FIELD_NUMBER: _ClassVar[int]
    scales: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, scales: _Iterable[float] | None = ...) -> None: ...

class CMsgGCToServerGetCheerState(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgCheerTypeState(_message.Message):
    __slots__ = ("cheer_counts", "max_per_second", "cheer_scale", "override_scale")
    CHEER_COUNTS_FIELD_NUMBER: _ClassVar[int]
    MAX_PER_SECOND_FIELD_NUMBER: _ClassVar[int]
    CHEER_SCALE_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_SCALE_FIELD_NUMBER: _ClassVar[int]
    cheer_counts: _containers.RepeatedScalarFieldContainer[int]
    max_per_second: float
    cheer_scale: float
    override_scale: float
    def __init__(
        self,
        cheer_counts: _Iterable[int] | None = ...,
        max_per_second: float | None = ...,
        cheer_scale: float | None = ...,
        override_scale: float | None = ...,
    ) -> None: ...

class CMsgCheerState(_message.Message):
    __slots__ = ("cheer_types", "radiant_crowd_level", "dire_crowd_level")
    CHEER_TYPES_FIELD_NUMBER: _ClassVar[int]
    RADIANT_CROWD_LEVEL_FIELD_NUMBER: _ClassVar[int]
    DIRE_CROWD_LEVEL_FIELD_NUMBER: _ClassVar[int]
    cheer_types: _containers.RepeatedCompositeFieldContainer[CMsgCheerTypeState]
    radiant_crowd_level: int
    dire_crowd_level: int
    def __init__(
        self,
        cheer_types: _Iterable[CMsgCheerTypeState | _Mapping] | None = ...,
        radiant_crowd_level: int | None = ...,
        dire_crowd_level: int | None = ...,
    ) -> None: ...

class CMsgServerToGCReportCheerState(_message.Message):
    __slots__ = ("cheer_config", "cheer_state")
    CHEER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    CHEER_STATE_FIELD_NUMBER: _ClassVar[int]
    cheer_config: CMsgCheerConfig
    cheer_state: CMsgCheerState
    def __init__(
        self,
        cheer_config: CMsgCheerConfig | _Mapping | None = ...,
        cheer_state: CMsgCheerState | _Mapping | None = ...,
    ) -> None: ...

class CMsgServerToGCGetStickerHeroes(_message.Message):
    __slots__ = ("account_ids",)
    ACCOUNT_IDS_FIELD_NUMBER: _ClassVar[int]
    account_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, account_ids: _Iterable[int] | None = ...) -> None: ...

class CMsgServerToGCGetStickerHeroesResponse(_message.Message):
    __slots__ = ("players",)
    class Player(_message.Message):
        __slots__ = ("account_id", "stickers")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        STICKERS_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        stickers: _dota_gcmessages_common_pb2.CMsgStickerHeroes
        def __init__(
            self,
            account_id: int | None = ...,
            stickers: _dota_gcmessages_common_pb2.CMsgStickerHeroes | _Mapping | None = ...,
        ) -> None: ...

    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    players: _containers.RepeatedCompositeFieldContainer[
        CMsgServerToGCGetStickerHeroesResponse.Player
    ]
    def __init__(
        self,
        players: _Iterable[CMsgServerToGCGetStickerHeroesResponse.Player | _Mapping] | None = ...,
    ) -> None: ...

class CMsgSteamLearnMatchInfo(_message.Message):
    __slots__ = ("average_mmr", "radiant_won", "duration", "game_mode", "lobby_type")
    AVERAGE_MMR_FIELD_NUMBER: _ClassVar[int]
    RADIANT_WON_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    GAME_MODE_FIELD_NUMBER: _ClassVar[int]
    LOBBY_TYPE_FIELD_NUMBER: _ClassVar[int]
    average_mmr: int
    radiant_won: bool
    duration: int
    game_mode: int
    lobby_type: int
    def __init__(
        self,
        average_mmr: int | None = ...,
        radiant_won: bool = ...,
        duration: int | None = ...,
        game_mode: int | None = ...,
        lobby_type: int | None = ...,
    ) -> None: ...

class CMsgSteamLearnMatchInfoPlayer(_message.Message):
    __slots__ = ("average_mmr", "team_won", "duration", "game_mode", "lobby_type", "player_mmr")
    AVERAGE_MMR_FIELD_NUMBER: _ClassVar[int]
    TEAM_WON_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    GAME_MODE_FIELD_NUMBER: _ClassVar[int]
    LOBBY_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLAYER_MMR_FIELD_NUMBER: _ClassVar[int]
    average_mmr: int
    team_won: bool
    duration: int
    game_mode: int
    lobby_type: int
    player_mmr: int
    def __init__(
        self,
        average_mmr: int | None = ...,
        team_won: bool = ...,
        duration: int | None = ...,
        game_mode: int | None = ...,
        lobby_type: int | None = ...,
        player_mmr: int | None = ...,
    ) -> None: ...

class CMsgSteamLearnMatchInfoTeam(_message.Message):
    __slots__ = ("radiant_players", "dire_players", "radiant_team_won")
    class Player(_message.Message):
        __slots__ = (
            "prematch_mmr",
            "prematch_rank_uncertainty",
            "prematch_behavior_score",
            "prematch_comm_score",
            "num_players_in_party",
        )
        PREMATCH_MMR_FIELD_NUMBER: _ClassVar[int]
        PREMATCH_RANK_UNCERTAINTY_FIELD_NUMBER: _ClassVar[int]
        PREMATCH_BEHAVIOR_SCORE_FIELD_NUMBER: _ClassVar[int]
        PREMATCH_COMM_SCORE_FIELD_NUMBER: _ClassVar[int]
        NUM_PLAYERS_IN_PARTY_FIELD_NUMBER: _ClassVar[int]
        prematch_mmr: int
        prematch_rank_uncertainty: int
        prematch_behavior_score: int
        prematch_comm_score: int
        num_players_in_party: int
        def __init__(
            self,
            prematch_mmr: int | None = ...,
            prematch_rank_uncertainty: int | None = ...,
            prematch_behavior_score: int | None = ...,
            prematch_comm_score: int | None = ...,
            num_players_in_party: int | None = ...,
        ) -> None: ...

    RADIANT_PLAYERS_FIELD_NUMBER: _ClassVar[int]
    DIRE_PLAYERS_FIELD_NUMBER: _ClassVar[int]
    RADIANT_TEAM_WON_FIELD_NUMBER: _ClassVar[int]
    radiant_players: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearnMatchInfoTeam.Player]
    dire_players: _containers.RepeatedCompositeFieldContainer[CMsgSteamLearnMatchInfoTeam.Player]
    radiant_team_won: bool
    def __init__(
        self,
        radiant_players: _Iterable[CMsgSteamLearnMatchInfoTeam.Player | _Mapping] | None = ...,
        dire_players: _Iterable[CMsgSteamLearnMatchInfoTeam.Player | _Mapping] | None = ...,
        radiant_team_won: bool = ...,
    ) -> None: ...

class CMsgSteamLearnMatchHeroesV3(_message.Message):
    __slots__ = (
        "radiant_hero_ids",
        "dire_hero_ids",
        "radiant_lanes",
        "dire_lanes",
        "radiant_hero_facets",
        "dire_hero_facets",
        "radiant_positions",
        "dire_positions",
    )
    RADIANT_HERO_IDS_FIELD_NUMBER: _ClassVar[int]
    DIRE_HERO_IDS_FIELD_NUMBER: _ClassVar[int]
    RADIANT_LANES_FIELD_NUMBER: _ClassVar[int]
    DIRE_LANES_FIELD_NUMBER: _ClassVar[int]
    RADIANT_HERO_FACETS_FIELD_NUMBER: _ClassVar[int]
    DIRE_HERO_FACETS_FIELD_NUMBER: _ClassVar[int]
    RADIANT_POSITIONS_FIELD_NUMBER: _ClassVar[int]
    DIRE_POSITIONS_FIELD_NUMBER: _ClassVar[int]
    radiant_hero_ids: _containers.RepeatedScalarFieldContainer[int]
    dire_hero_ids: _containers.RepeatedScalarFieldContainer[int]
    radiant_lanes: _containers.RepeatedScalarFieldContainer[int]
    dire_lanes: _containers.RepeatedScalarFieldContainer[int]
    radiant_hero_facets: _containers.RepeatedScalarFieldContainer[int]
    dire_hero_facets: _containers.RepeatedScalarFieldContainer[int]
    radiant_positions: _containers.RepeatedScalarFieldContainer[int]
    dire_positions: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        radiant_hero_ids: _Iterable[int] | None = ...,
        dire_hero_ids: _Iterable[int] | None = ...,
        radiant_lanes: _Iterable[int] | None = ...,
        dire_lanes: _Iterable[int] | None = ...,
        radiant_hero_facets: _Iterable[int] | None = ...,
        dire_hero_facets: _Iterable[int] | None = ...,
        radiant_positions: _Iterable[int] | None = ...,
        dire_positions: _Iterable[int] | None = ...,
    ) -> None: ...

class CMsgSteamLearnMatchHeroesV4(_message.Message):
    __slots__ = (
        "radiant_hero_ids",
        "dire_hero_ids",
        "radiant_lanes",
        "dire_lanes",
        "radiant_positions",
        "dire_positions",
    )
    RADIANT_HERO_IDS_FIELD_NUMBER: _ClassVar[int]
    DIRE_HERO_IDS_FIELD_NUMBER: _ClassVar[int]
    RADIANT_LANES_FIELD_NUMBER: _ClassVar[int]
    DIRE_LANES_FIELD_NUMBER: _ClassVar[int]
    RADIANT_POSITIONS_FIELD_NUMBER: _ClassVar[int]
    DIRE_POSITIONS_FIELD_NUMBER: _ClassVar[int]
    radiant_hero_ids: _containers.RepeatedScalarFieldContainer[int]
    dire_hero_ids: _containers.RepeatedScalarFieldContainer[int]
    radiant_lanes: _containers.RepeatedScalarFieldContainer[int]
    dire_lanes: _containers.RepeatedScalarFieldContainer[int]
    radiant_positions: _containers.RepeatedScalarFieldContainer[int]
    dire_positions: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        radiant_hero_ids: _Iterable[int] | None = ...,
        dire_hero_ids: _Iterable[int] | None = ...,
        radiant_lanes: _Iterable[int] | None = ...,
        dire_lanes: _Iterable[int] | None = ...,
        radiant_positions: _Iterable[int] | None = ...,
        dire_positions: _Iterable[int] | None = ...,
    ) -> None: ...

class CMsgSteamLearnMatchHeroV6(_message.Message):
    __slots__ = (
        "hero_id",
        "facet",
        "hero_and_facet",
        "lane",
        "position",
        "allied_hero_and_facet",
        "enemy_hero_and_facet",
    )
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    FACET_FIELD_NUMBER: _ClassVar[int]
    HERO_AND_FACET_FIELD_NUMBER: _ClassVar[int]
    LANE_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    ALLIED_HERO_AND_FACET_FIELD_NUMBER: _ClassVar[int]
    ENEMY_HERO_AND_FACET_FIELD_NUMBER: _ClassVar[int]
    hero_id: int
    facet: int
    hero_and_facet: int
    lane: int
    position: int
    allied_hero_and_facet: _containers.RepeatedScalarFieldContainer[int]
    enemy_hero_and_facet: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        hero_id: int | None = ...,
        facet: int | None = ...,
        hero_and_facet: int | None = ...,
        lane: int | None = ...,
        position: int | None = ...,
        allied_hero_and_facet: _Iterable[int] | None = ...,
        enemy_hero_and_facet: _Iterable[int] | None = ...,
    ) -> None: ...

class CMsgSteamLearnMatchHeroV8(_message.Message):
    __slots__ = ("hero_id", "lane", "position", "allied_heroes", "enemy_heroes")
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    LANE_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    ALLIED_HEROES_FIELD_NUMBER: _ClassVar[int]
    ENEMY_HEROES_FIELD_NUMBER: _ClassVar[int]
    hero_id: int
    lane: int
    position: int
    allied_heroes: _containers.RepeatedScalarFieldContainer[int]
    enemy_heroes: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        hero_id: int | None = ...,
        lane: int | None = ...,
        position: int | None = ...,
        allied_heroes: _Iterable[int] | None = ...,
        enemy_heroes: _Iterable[int] | None = ...,
    ) -> None: ...

class CMsgSteamLearnPlayerTimedStats(_message.Message):
    __slots__ = ("stat_buckets",)
    class StatBucket(_message.Message):
        __slots__ = (
            "game_time",
            "kills",
            "deaths",
            "assists",
            "experience",
            "last_hits",
            "denies",
            "net_worth",
            "idle_time",
            "commands_issued",
            "sentry_wards_placed",
            "observer_wards_placed",
        )
        GAME_TIME_FIELD_NUMBER: _ClassVar[int]
        KILLS_FIELD_NUMBER: _ClassVar[int]
        DEATHS_FIELD_NUMBER: _ClassVar[int]
        ASSISTS_FIELD_NUMBER: _ClassVar[int]
        EXPERIENCE_FIELD_NUMBER: _ClassVar[int]
        LAST_HITS_FIELD_NUMBER: _ClassVar[int]
        DENIES_FIELD_NUMBER: _ClassVar[int]
        NET_WORTH_FIELD_NUMBER: _ClassVar[int]
        IDLE_TIME_FIELD_NUMBER: _ClassVar[int]
        COMMANDS_ISSUED_FIELD_NUMBER: _ClassVar[int]
        SENTRY_WARDS_PLACED_FIELD_NUMBER: _ClassVar[int]
        OBSERVER_WARDS_PLACED_FIELD_NUMBER: _ClassVar[int]
        game_time: float
        kills: int
        deaths: int
        assists: int
        experience: int
        last_hits: int
        denies: int
        net_worth: int
        idle_time: float
        commands_issued: int
        sentry_wards_placed: int
        observer_wards_placed: int
        def __init__(
            self,
            game_time: float | None = ...,
            kills: int | None = ...,
            deaths: int | None = ...,
            assists: int | None = ...,
            experience: int | None = ...,
            last_hits: int | None = ...,
            denies: int | None = ...,
            net_worth: int | None = ...,
            idle_time: float | None = ...,
            commands_issued: int | None = ...,
            sentry_wards_placed: int | None = ...,
            observer_wards_placed: int | None = ...,
        ) -> None: ...

    STAT_BUCKETS_FIELD_NUMBER: _ClassVar[int]
    stat_buckets: _containers.RepeatedCompositeFieldContainer[
        CMsgSteamLearnPlayerTimedStats.StatBucket
    ]
    def __init__(
        self,
        stat_buckets: _Iterable[CMsgSteamLearnPlayerTimedStats.StatBucket | _Mapping] | None = ...,
    ) -> None: ...

class CMsgSteamLearnMatchStateV5(_message.Message):
    __slots__ = ("game_time", "radiant_state", "dire_state")
    class PlayerState(_message.Message):
        __slots__ = (
            "hero_id",
            "net_worth",
            "level",
            "deaths",
            "respawn_time",
            "has_buyback",
            "has_aegis",
            "has_rapier",
            "distance",
            "hero_facet",
        )
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        NET_WORTH_FIELD_NUMBER: _ClassVar[int]
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        DEATHS_FIELD_NUMBER: _ClassVar[int]
        RESPAWN_TIME_FIELD_NUMBER: _ClassVar[int]
        HAS_BUYBACK_FIELD_NUMBER: _ClassVar[int]
        HAS_AEGIS_FIELD_NUMBER: _ClassVar[int]
        HAS_RAPIER_FIELD_NUMBER: _ClassVar[int]
        DISTANCE_FIELD_NUMBER: _ClassVar[int]
        HERO_FACET_FIELD_NUMBER: _ClassVar[int]
        hero_id: int
        net_worth: int
        level: int
        deaths: int
        respawn_time: int
        has_buyback: bool
        has_aegis: bool
        has_rapier: bool
        distance: int
        hero_facet: int
        def __init__(
            self,
            hero_id: int | None = ...,
            net_worth: int | None = ...,
            level: int | None = ...,
            deaths: int | None = ...,
            respawn_time: int | None = ...,
            has_buyback: bool = ...,
            has_aegis: bool = ...,
            has_rapier: bool = ...,
            distance: int | None = ...,
            hero_facet: int | None = ...,
        ) -> None: ...

    class TeamState(_message.Message):
        __slots__ = (
            "team",
            "player_states",
            "tower_health_pct",
            "barracks_health_pct",
            "ancient_health_pct",
            "glyph_cooldown",
            "kills",
            "creep_distance_safe",
            "creep_distance_mid",
            "creep_distance_off",
        )
        TEAM_FIELD_NUMBER: _ClassVar[int]
        PLAYER_STATES_FIELD_NUMBER: _ClassVar[int]
        TOWER_HEALTH_PCT_FIELD_NUMBER: _ClassVar[int]
        BARRACKS_HEALTH_PCT_FIELD_NUMBER: _ClassVar[int]
        ANCIENT_HEALTH_PCT_FIELD_NUMBER: _ClassVar[int]
        GLYPH_COOLDOWN_FIELD_NUMBER: _ClassVar[int]
        KILLS_FIELD_NUMBER: _ClassVar[int]
        CREEP_DISTANCE_SAFE_FIELD_NUMBER: _ClassVar[int]
        CREEP_DISTANCE_MID_FIELD_NUMBER: _ClassVar[int]
        CREEP_DISTANCE_OFF_FIELD_NUMBER: _ClassVar[int]
        team: int
        player_states: _containers.RepeatedCompositeFieldContainer[
            CMsgSteamLearnMatchStateV5.PlayerState
        ]
        tower_health_pct: _containers.RepeatedScalarFieldContainer[int]
        barracks_health_pct: _containers.RepeatedScalarFieldContainer[int]
        ancient_health_pct: int
        glyph_cooldown: int
        kills: int
        creep_distance_safe: int
        creep_distance_mid: int
        creep_distance_off: int
        def __init__(
            self,
            team: int | None = ...,
            player_states: _Iterable[CMsgSteamLearnMatchStateV5.PlayerState | _Mapping]
            | None = ...,
            tower_health_pct: _Iterable[int] | None = ...,
            barracks_health_pct: _Iterable[int] | None = ...,
            ancient_health_pct: int | None = ...,
            glyph_cooldown: int | None = ...,
            kills: int | None = ...,
            creep_distance_safe: int | None = ...,
            creep_distance_mid: int | None = ...,
            creep_distance_off: int | None = ...,
        ) -> None: ...

    GAME_TIME_FIELD_NUMBER: _ClassVar[int]
    RADIANT_STATE_FIELD_NUMBER: _ClassVar[int]
    DIRE_STATE_FIELD_NUMBER: _ClassVar[int]
    game_time: float
    radiant_state: CMsgSteamLearnMatchStateV5.TeamState
    dire_state: CMsgSteamLearnMatchStateV5.TeamState
    def __init__(
        self,
        game_time: float | None = ...,
        radiant_state: CMsgSteamLearnMatchStateV5.TeamState | _Mapping | None = ...,
        dire_state: CMsgSteamLearnMatchStateV5.TeamState | _Mapping | None = ...,
    ) -> None: ...

class CMsgSteamLearnItemPurchaseV7(_message.Message):
    __slots__ = ("item_id", "purchase_history")
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    PURCHASE_HISTORY_FIELD_NUMBER: _ClassVar[int]
    item_id: int
    purchase_history: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self, item_id: int | None = ..., purchase_history: _Iterable[int] | None = ...
    ) -> None: ...

class CMsgSteamLearnPreGameItemPurchases(_message.Message):
    __slots__ = ("item_ids", "is_radiant_team", "is_using_dota_plus")
    ITEM_IDS_FIELD_NUMBER: _ClassVar[int]
    IS_RADIANT_TEAM_FIELD_NUMBER: _ClassVar[int]
    IS_USING_DOTA_PLUS_FIELD_NUMBER: _ClassVar[int]
    item_ids: _containers.RepeatedScalarFieldContainer[int]
    is_radiant_team: int
    is_using_dota_plus: bool
    def __init__(
        self,
        item_ids: _Iterable[int] | None = ...,
        is_radiant_team: int | None = ...,
        is_using_dota_plus: bool = ...,
    ) -> None: ...

class CMsgSteamLearnPreGameItemPurchase(_message.Message):
    __slots__ = ("purchase_history", "item_id")
    PURCHASE_HISTORY_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    purchase_history: _containers.RepeatedScalarFieldContainer[int]
    item_id: int
    def __init__(
        self, purchase_history: _Iterable[int] | None = ..., item_id: int | None = ...
    ) -> None: ...

class CMsgSteamLearnNeutralItemPurchaseV4(_message.Message):
    __slots__ = ("tier", "trinket_options", "enhancement_options", "trinket_id", "enhancement_id")
    TIER_FIELD_NUMBER: _ClassVar[int]
    TRINKET_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    ENHANCEMENT_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    TRINKET_ID_FIELD_NUMBER: _ClassVar[int]
    ENHANCEMENT_ID_FIELD_NUMBER: _ClassVar[int]
    tier: int
    trinket_options: _containers.RepeatedScalarFieldContainer[int]
    enhancement_options: _containers.RepeatedScalarFieldContainer[int]
    trinket_id: int
    enhancement_id: int
    def __init__(
        self,
        tier: int | None = ...,
        trinket_options: _Iterable[int] | None = ...,
        enhancement_options: _Iterable[int] | None = ...,
        trinket_id: int | None = ...,
        enhancement_id: int | None = ...,
    ) -> None: ...

class CMsgSteamLearnAbilitySkill(_message.Message):
    __slots__ = ("ability_id", "skilled_abilities", "game_time", "is_using_dota_plus")
    ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    SKILLED_ABILITIES_FIELD_NUMBER: _ClassVar[int]
    GAME_TIME_FIELD_NUMBER: _ClassVar[int]
    IS_USING_DOTA_PLUS_FIELD_NUMBER: _ClassVar[int]
    ability_id: int
    skilled_abilities: _containers.RepeatedScalarFieldContainer[int]
    game_time: float
    is_using_dota_plus: bool
    def __init__(
        self,
        ability_id: int | None = ...,
        skilled_abilities: _Iterable[int] | None = ...,
        game_time: float | None = ...,
        is_using_dota_plus: bool = ...,
    ) -> None: ...

class CMsgSteamLearnWardPlacement(_message.Message):
    __slots__ = ("ward_loc", "existing_ward_locs", "team")
    class Location(_message.Message):
        __slots__ = ("x", "y")
        X_FIELD_NUMBER: _ClassVar[int]
        Y_FIELD_NUMBER: _ClassVar[int]
        x: float
        y: float
        def __init__(self, x: float | None = ..., y: float | None = ...) -> None: ...

    WARD_LOC_FIELD_NUMBER: _ClassVar[int]
    EXISTING_WARD_LOCS_FIELD_NUMBER: _ClassVar[int]
    TEAM_FIELD_NUMBER: _ClassVar[int]
    ward_loc: CMsgSteamLearnWardPlacement.Location
    existing_ward_locs: _containers.RepeatedCompositeFieldContainer[
        CMsgSteamLearnWardPlacement.Location
    ]
    team: int
    def __init__(
        self,
        ward_loc: CMsgSteamLearnWardPlacement.Location | _Mapping | None = ...,
        existing_ward_locs: _Iterable[CMsgSteamLearnWardPlacement.Location | _Mapping] | None = ...,
        team: int | None = ...,
    ) -> None: ...

class CMsgSteamLearnPlayerMatchState(_message.Message):
    __slots__ = (
        "net_worth",
        "level",
        "deaths",
        "respawn_time",
        "has_buyback",
        "has_aegis",
        "has_rapier",
        "team_net_worth",
        "enemy_team_net_worth",
        "team_kills",
        "enemy_team_kills",
        "game_time",
    )
    NET_WORTH_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    DEATHS_FIELD_NUMBER: _ClassVar[int]
    RESPAWN_TIME_FIELD_NUMBER: _ClassVar[int]
    HAS_BUYBACK_FIELD_NUMBER: _ClassVar[int]
    HAS_AEGIS_FIELD_NUMBER: _ClassVar[int]
    HAS_RAPIER_FIELD_NUMBER: _ClassVar[int]
    TEAM_NET_WORTH_FIELD_NUMBER: _ClassVar[int]
    ENEMY_TEAM_NET_WORTH_FIELD_NUMBER: _ClassVar[int]
    TEAM_KILLS_FIELD_NUMBER: _ClassVar[int]
    ENEMY_TEAM_KILLS_FIELD_NUMBER: _ClassVar[int]
    GAME_TIME_FIELD_NUMBER: _ClassVar[int]
    net_worth: int
    level: int
    deaths: int
    respawn_time: int
    has_buyback: bool
    has_aegis: bool
    has_rapier: bool
    team_net_worth: int
    enemy_team_net_worth: int
    team_kills: int
    enemy_team_kills: int
    game_time: float
    def __init__(
        self,
        net_worth: int | None = ...,
        level: int | None = ...,
        deaths: int | None = ...,
        respawn_time: int | None = ...,
        has_buyback: bool = ...,
        has_aegis: bool = ...,
        has_rapier: bool = ...,
        team_net_worth: int | None = ...,
        enemy_team_net_worth: int | None = ...,
        team_kills: int | None = ...,
        enemy_team_kills: int | None = ...,
        game_time: float | None = ...,
    ) -> None: ...

class CMsgSignOutMuertaMinigame(_message.Message):
    __slots__ = ("event_game_data",)
    EVENT_GAME_DATA_FIELD_NUMBER: _ClassVar[int]
    event_game_data: bytes
    def __init__(self, event_game_data: bytes | None = ...) -> None: ...

class CMsgSignOutMapStats(_message.Message):
    __slots__ = ("players", "global_stats")
    class Player(_message.Message):
        __slots__ = ("account_id", "personal_stats")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        PERSONAL_STATS_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        personal_stats: _dota_gcmessages_common_pb2.CMsgMapStatsSnapshot
        def __init__(
            self,
            account_id: int | None = ...,
            personal_stats: _dota_gcmessages_common_pb2.CMsgMapStatsSnapshot
            | _Mapping
            | None = ...,
        ) -> None: ...

    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    GLOBAL_STATS_FIELD_NUMBER: _ClassVar[int]
    players: _containers.RepeatedCompositeFieldContainer[CMsgSignOutMapStats.Player]
    global_stats: _dota_gcmessages_common_pb2.CMsgMapStatsSnapshot
    def __init__(
        self,
        players: _Iterable[CMsgSignOutMapStats.Player | _Mapping] | None = ...,
        global_stats: _dota_gcmessages_common_pb2.CMsgMapStatsSnapshot | _Mapping | None = ...,
    ) -> None: ...

class CMsgServerToGCNewBloomGift(_message.Message):
    __slots__ = ("defindex", "gifter_account_id", "target_account_ids")
    DEFINDEX_FIELD_NUMBER: _ClassVar[int]
    GIFTER_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_ACCOUNT_IDS_FIELD_NUMBER: _ClassVar[int]
    defindex: int
    gifter_account_id: int
    target_account_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        defindex: int | None = ...,
        gifter_account_id: int | None = ...,
        target_account_ids: _Iterable[int] | None = ...,
    ) -> None: ...

class CMsgServerToGCNewBloomGiftResponse(_message.Message):
    __slots__ = ("result", "received_account_ids")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_ACCOUNT_IDS_FIELD_NUMBER: _ClassVar[int]
    result: _dota_gcmessages_common_pb2.ENewBloomGiftingResponse
    received_account_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        result: _dota_gcmessages_common_pb2.ENewBloomGiftingResponse | str | None = ...,
        received_account_ids: _Iterable[int] | None = ...,
    ) -> None: ...

class CMsgSignOutOverworld(_message.Message):
    __slots__ = ("players", "event_id")
    class Player(_message.Message):
        __slots__ = ("account_id", "overworld_id", "desired_token_rewards")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
        DESIRED_TOKEN_REWARDS_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        overworld_id: int
        desired_token_rewards: _containers.RepeatedScalarFieldContainer[int]
        def __init__(
            self,
            account_id: int | None = ...,
            overworld_id: int | None = ...,
            desired_token_rewards: _Iterable[int] | None = ...,
        ) -> None: ...

    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    players: _containers.RepeatedCompositeFieldContainer[CMsgSignOutOverworld.Player]
    event_id: _dota_shared_enums_pb2.EEvent
    def __init__(
        self,
        players: _Iterable[CMsgSignOutOverworld.Player | _Mapping] | None = ...,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
    ) -> None: ...

class CMsgSignOutCraftworks(_message.Message):
    __slots__ = ("players", "event_id")
    class Player(_message.Message):
        __slots__ = ("account_id", "components")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        COMPONENTS_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        components: _dota_gcmessages_common_craftworks_pb2.CMsgCraftworksComponents
        def __init__(
            self,
            account_id: int | None = ...,
            components: _dota_gcmessages_common_craftworks_pb2.CMsgCraftworksComponents
            | _Mapping
            | None = ...,
        ) -> None: ...

    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    players: _containers.RepeatedCompositeFieldContainer[CMsgSignOutCraftworks.Player]
    event_id: _dota_shared_enums_pb2.EEvent
    def __init__(
        self,
        players: _Iterable[CMsgSignOutCraftworks.Player | _Mapping] | None = ...,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
    ) -> None: ...

class CMsgSignOutMonsterHunter(_message.Message):
    __slots__ = ("players", "event_id")
    class Player(_message.Message):
        __slots__ = ("account_id", "investigation_game_state", "codex_update_data")
        ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        INVESTIGATION_GAME_STATE_FIELD_NUMBER: _ClassVar[int]
        CODEX_UPDATE_DATA_FIELD_NUMBER: _ClassVar[int]
        account_id: int
        investigation_game_state: _dota_shared_enums_pb2.CMsgMonsterHunterInvestigationGameState
        codex_update_data: _dota_shared_enums_pb2.CMsgMonsterHunterCodexUpdateData
        def __init__(
            self,
            account_id: int | None = ...,
            investigation_game_state: _dota_shared_enums_pb2.CMsgMonsterHunterInvestigationGameState
            | _Mapping
            | None = ...,
            codex_update_data: _dota_shared_enums_pb2.CMsgMonsterHunterCodexUpdateData
            | _Mapping
            | None = ...,
        ) -> None: ...

    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    players: _containers.RepeatedCompositeFieldContainer[CMsgSignOutMonsterHunter.Player]
    event_id: _dota_shared_enums_pb2.EEvent
    def __init__(
        self,
        players: _Iterable[CMsgSignOutMonsterHunter.Player | _Mapping] | None = ...,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
    ) -> None: ...

class CMsgServerToGCWarningLowServerFramerate(_message.Message):
    __slots__ = (
        "match_id",
        "ticks_per_interval_average",
        "custom_game_id",
        "bot_script_id_radiant",
        "bot_script_id_dire",
    )
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    TICKS_PER_INTERVAL_AVERAGE_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_GAME_ID_FIELD_NUMBER: _ClassVar[int]
    BOT_SCRIPT_ID_RADIANT_FIELD_NUMBER: _ClassVar[int]
    BOT_SCRIPT_ID_DIRE_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    ticks_per_interval_average: float
    custom_game_id: int
    bot_script_id_radiant: int
    bot_script_id_dire: int
    def __init__(
        self,
        match_id: int | None = ...,
        ticks_per_interval_average: float | None = ...,
        custom_game_id: int | None = ...,
        bot_script_id_radiant: int | None = ...,
        bot_script_id_dire: int | None = ...,
    ) -> None: ...

class CMsgServerToGCWarningInvalidBotAbilityUsage(_message.Message):
    __slots__ = ("description", "unit_name", "ability_name")
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    UNIT_NAME_FIELD_NUMBER: _ClassVar[int]
    ABILITY_NAME_FIELD_NUMBER: _ClassVar[int]
    description: str
    unit_name: str
    ability_name: str
    def __init__(
        self,
        description: str | None = ...,
        unit_name: str | None = ...,
        ability_name: str | None = ...,
    ) -> None: ...
