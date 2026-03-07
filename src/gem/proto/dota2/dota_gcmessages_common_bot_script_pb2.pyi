from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class CMsgBotWorldState(_message.Message):
    __slots__ = (
        "team_id",
        "game_time",
        "dota_time",
        "game_state",
        "hero_pick_state",
        "time_of_day",
        "glyph_cooldown",
        "glyph_cooldown_enemy",
        "players",
        "units",
        "dropped_items",
        "dropped_items_deltas",
        "rune_infos",
        "rune_infos_deltas",
        "incoming_teleports",
        "linear_projectiles",
        "avoidance_zones",
        "couriers",
        "ability_events",
        "damage_events",
        "courier_killed_events",
        "roshan_killed_events",
        "tree_events",
    )
    class UnitType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INVALID: _ClassVar[CMsgBotWorldState.UnitType]
        HERO: _ClassVar[CMsgBotWorldState.UnitType]
        CREEP_HERO: _ClassVar[CMsgBotWorldState.UnitType]
        LANE_CREEP: _ClassVar[CMsgBotWorldState.UnitType]
        JUNGLE_CREEP: _ClassVar[CMsgBotWorldState.UnitType]
        ROSHAN: _ClassVar[CMsgBotWorldState.UnitType]
        TOWER: _ClassVar[CMsgBotWorldState.UnitType]
        BARRACKS: _ClassVar[CMsgBotWorldState.UnitType]
        SHRINE: _ClassVar[CMsgBotWorldState.UnitType]
        FORT: _ClassVar[CMsgBotWorldState.UnitType]
        BUILDING: _ClassVar[CMsgBotWorldState.UnitType]
        COURIER: _ClassVar[CMsgBotWorldState.UnitType]
        WARD: _ClassVar[CMsgBotWorldState.UnitType]

    INVALID: CMsgBotWorldState.UnitType
    HERO: CMsgBotWorldState.UnitType
    CREEP_HERO: CMsgBotWorldState.UnitType
    LANE_CREEP: CMsgBotWorldState.UnitType
    JUNGLE_CREEP: CMsgBotWorldState.UnitType
    ROSHAN: CMsgBotWorldState.UnitType
    TOWER: CMsgBotWorldState.UnitType
    BARRACKS: CMsgBotWorldState.UnitType
    SHRINE: CMsgBotWorldState.UnitType
    FORT: CMsgBotWorldState.UnitType
    BUILDING: CMsgBotWorldState.UnitType
    COURIER: CMsgBotWorldState.UnitType
    WARD: CMsgBotWorldState.UnitType
    class CourierState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        COURIER_STATE_INIT: _ClassVar[CMsgBotWorldState.CourierState]
        COURIER_STATE_IDLE: _ClassVar[CMsgBotWorldState.CourierState]
        COURIER_STATE_AT_BASE: _ClassVar[CMsgBotWorldState.CourierState]
        COURIER_STATE_MOVING: _ClassVar[CMsgBotWorldState.CourierState]
        COURIER_STATE_DELIVERING_ITEMS: _ClassVar[CMsgBotWorldState.CourierState]
        COURIER_STATE_RETURNING_TO_BASE: _ClassVar[CMsgBotWorldState.CourierState]
        COURIER_STATE_DEAD: _ClassVar[CMsgBotWorldState.CourierState]
        COURIER_STATE_GOING_TO_SECRET_SHOP: _ClassVar[CMsgBotWorldState.CourierState]
        COURIER_STATE_AT_SECRET_SHOP: _ClassVar[CMsgBotWorldState.CourierState]

    COURIER_STATE_INIT: CMsgBotWorldState.CourierState
    COURIER_STATE_IDLE: CMsgBotWorldState.CourierState
    COURIER_STATE_AT_BASE: CMsgBotWorldState.CourierState
    COURIER_STATE_MOVING: CMsgBotWorldState.CourierState
    COURIER_STATE_DELIVERING_ITEMS: CMsgBotWorldState.CourierState
    COURIER_STATE_RETURNING_TO_BASE: CMsgBotWorldState.CourierState
    COURIER_STATE_DEAD: CMsgBotWorldState.CourierState
    COURIER_STATE_GOING_TO_SECRET_SHOP: CMsgBotWorldState.CourierState
    COURIER_STATE_AT_SECRET_SHOP: CMsgBotWorldState.CourierState
    class Vector(_message.Message):
        __slots__ = ("x", "y", "z")
        X_FIELD_NUMBER: _ClassVar[int]
        Y_FIELD_NUMBER: _ClassVar[int]
        Z_FIELD_NUMBER: _ClassVar[int]
        x: float
        y: float
        z: float
        def __init__(
            self, x: float | None = ..., y: float | None = ..., z: float | None = ...
        ) -> None: ...

    class Player(_message.Message):
        __slots__ = (
            "player_id",
            "hero_id",
            "is_alive",
            "respawn_time",
            "kills",
            "deaths",
            "assists",
            "team_id",
            "primary_unit_handle",
            "mmr",
            "location",
        )
        PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        IS_ALIVE_FIELD_NUMBER: _ClassVar[int]
        RESPAWN_TIME_FIELD_NUMBER: _ClassVar[int]
        KILLS_FIELD_NUMBER: _ClassVar[int]
        DEATHS_FIELD_NUMBER: _ClassVar[int]
        ASSISTS_FIELD_NUMBER: _ClassVar[int]
        TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        PRIMARY_UNIT_HANDLE_FIELD_NUMBER: _ClassVar[int]
        MMR_FIELD_NUMBER: _ClassVar[int]
        LOCATION_FIELD_NUMBER: _ClassVar[int]
        player_id: int
        hero_id: int
        is_alive: bool
        respawn_time: float
        kills: int
        deaths: int
        assists: int
        team_id: int
        primary_unit_handle: int
        mmr: int
        location: CMsgBotWorldState.Vector
        def __init__(
            self,
            player_id: int | None = ...,
            hero_id: int | None = ...,
            is_alive: bool = ...,
            respawn_time: float | None = ...,
            kills: int | None = ...,
            deaths: int | None = ...,
            assists: int | None = ...,
            team_id: int | None = ...,
            primary_unit_handle: int | None = ...,
            mmr: int | None = ...,
            location: CMsgBotWorldState.Vector | _Mapping | None = ...,
        ) -> None: ...

    class Ability(_message.Message):
        __slots__ = (
            "handle",
            "ability_id",
            "slot",
            "caster_handle",
            "level",
            "cast_range",
            "channel_time",
            "cooldown_remaining",
            "is_activated",
            "is_toggled",
            "is_in_ability_phase",
            "is_channeling",
            "is_stolen",
            "is_fully_castable",
            "charges",
            "secondary_charges",
            "is_combined_locked",
            "power_treads_stat",
        )
        HANDLE_FIELD_NUMBER: _ClassVar[int]
        ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
        SLOT_FIELD_NUMBER: _ClassVar[int]
        CASTER_HANDLE_FIELD_NUMBER: _ClassVar[int]
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        CAST_RANGE_FIELD_NUMBER: _ClassVar[int]
        CHANNEL_TIME_FIELD_NUMBER: _ClassVar[int]
        COOLDOWN_REMAINING_FIELD_NUMBER: _ClassVar[int]
        IS_ACTIVATED_FIELD_NUMBER: _ClassVar[int]
        IS_TOGGLED_FIELD_NUMBER: _ClassVar[int]
        IS_IN_ABILITY_PHASE_FIELD_NUMBER: _ClassVar[int]
        IS_CHANNELING_FIELD_NUMBER: _ClassVar[int]
        IS_STOLEN_FIELD_NUMBER: _ClassVar[int]
        IS_FULLY_CASTABLE_FIELD_NUMBER: _ClassVar[int]
        CHARGES_FIELD_NUMBER: _ClassVar[int]
        SECONDARY_CHARGES_FIELD_NUMBER: _ClassVar[int]
        IS_COMBINED_LOCKED_FIELD_NUMBER: _ClassVar[int]
        POWER_TREADS_STAT_FIELD_NUMBER: _ClassVar[int]
        handle: int
        ability_id: int
        slot: int
        caster_handle: int
        level: int
        cast_range: int
        channel_time: float
        cooldown_remaining: float
        is_activated: bool
        is_toggled: bool
        is_in_ability_phase: bool
        is_channeling: bool
        is_stolen: bool
        is_fully_castable: bool
        charges: int
        secondary_charges: int
        is_combined_locked: bool
        power_treads_stat: int
        def __init__(
            self,
            handle: int | None = ...,
            ability_id: int | None = ...,
            slot: int | None = ...,
            caster_handle: int | None = ...,
            level: int | None = ...,
            cast_range: int | None = ...,
            channel_time: float | None = ...,
            cooldown_remaining: float | None = ...,
            is_activated: bool = ...,
            is_toggled: bool = ...,
            is_in_ability_phase: bool = ...,
            is_channeling: bool = ...,
            is_stolen: bool = ...,
            is_fully_castable: bool = ...,
            charges: int | None = ...,
            secondary_charges: int | None = ...,
            is_combined_locked: bool = ...,
            power_treads_stat: int | None = ...,
        ) -> None: ...

    class DroppedItem(_message.Message):
        __slots__ = ("item_id", "location")
        ITEM_ID_FIELD_NUMBER: _ClassVar[int]
        LOCATION_FIELD_NUMBER: _ClassVar[int]
        item_id: int
        location: CMsgBotWorldState.Vector
        def __init__(
            self,
            item_id: int | None = ...,
            location: CMsgBotWorldState.Vector | _Mapping | None = ...,
        ) -> None: ...

    class RuneInfo(_message.Message):
        __slots__ = ("type", "location", "status", "time_since_seen")
        TYPE_FIELD_NUMBER: _ClassVar[int]
        LOCATION_FIELD_NUMBER: _ClassVar[int]
        STATUS_FIELD_NUMBER: _ClassVar[int]
        TIME_SINCE_SEEN_FIELD_NUMBER: _ClassVar[int]
        type: int
        location: CMsgBotWorldState.Vector
        status: int
        time_since_seen: float
        def __init__(
            self,
            type: int | None = ...,
            location: CMsgBotWorldState.Vector | _Mapping | None = ...,
            status: int | None = ...,
            time_since_seen: float | None = ...,
        ) -> None: ...

    class TeleportInfo(_message.Message):
        __slots__ = ("player_id", "location", "time_remaining")
        PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
        LOCATION_FIELD_NUMBER: _ClassVar[int]
        TIME_REMAINING_FIELD_NUMBER: _ClassVar[int]
        player_id: int
        location: CMsgBotWorldState.Vector
        time_remaining: float
        def __init__(
            self,
            player_id: int | None = ...,
            location: CMsgBotWorldState.Vector | _Mapping | None = ...,
            time_remaining: float | None = ...,
        ) -> None: ...

    class Modifier(_message.Message):
        __slots__ = (
            "handle",
            "name",
            "stack_count",
            "ability_handle",
            "ability_id",
            "remaining_duration",
            "auxiliary_units_handles",
        )
        HANDLE_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        STACK_COUNT_FIELD_NUMBER: _ClassVar[int]
        ABILITY_HANDLE_FIELD_NUMBER: _ClassVar[int]
        ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
        REMAINING_DURATION_FIELD_NUMBER: _ClassVar[int]
        AUXILIARY_UNITS_HANDLES_FIELD_NUMBER: _ClassVar[int]
        handle: int
        name: str
        stack_count: int
        ability_handle: int
        ability_id: int
        remaining_duration: float
        auxiliary_units_handles: _containers.RepeatedScalarFieldContainer[int]
        def __init__(
            self,
            handle: int | None = ...,
            name: str | None = ...,
            stack_count: int | None = ...,
            ability_handle: int | None = ...,
            ability_id: int | None = ...,
            remaining_duration: float | None = ...,
            auxiliary_units_handles: _Iterable[int] | None = ...,
        ) -> None: ...

    class LinearProjectile(_message.Message):
        __slots__ = (
            "handle",
            "caster_handle",
            "caster_unit_type",
            "caster_player_id",
            "ability_handle",
            "ability_id",
            "location",
            "velocity",
            "radius",
        )
        HANDLE_FIELD_NUMBER: _ClassVar[int]
        CASTER_HANDLE_FIELD_NUMBER: _ClassVar[int]
        CASTER_UNIT_TYPE_FIELD_NUMBER: _ClassVar[int]
        CASTER_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
        ABILITY_HANDLE_FIELD_NUMBER: _ClassVar[int]
        ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
        LOCATION_FIELD_NUMBER: _ClassVar[int]
        VELOCITY_FIELD_NUMBER: _ClassVar[int]
        RADIUS_FIELD_NUMBER: _ClassVar[int]
        handle: int
        caster_handle: int
        caster_unit_type: CMsgBotWorldState.UnitType
        caster_player_id: int
        ability_handle: int
        ability_id: int
        location: CMsgBotWorldState.Vector
        velocity: CMsgBotWorldState.Vector
        radius: int
        def __init__(
            self,
            handle: int | None = ...,
            caster_handle: int | None = ...,
            caster_unit_type: CMsgBotWorldState.UnitType | str | None = ...,
            caster_player_id: int | None = ...,
            ability_handle: int | None = ...,
            ability_id: int | None = ...,
            location: CMsgBotWorldState.Vector | _Mapping | None = ...,
            velocity: CMsgBotWorldState.Vector | _Mapping | None = ...,
            radius: int | None = ...,
        ) -> None: ...

    class TrackingProjectile(_message.Message):
        __slots__ = (
            "handle",
            "caster_handle",
            "caster_unit_type",
            "caster_player_id",
            "ability_handle",
            "ability_id",
            "location",
            "velocity",
            "is_dodgeable",
            "is_attack",
        )
        HANDLE_FIELD_NUMBER: _ClassVar[int]
        CASTER_HANDLE_FIELD_NUMBER: _ClassVar[int]
        CASTER_UNIT_TYPE_FIELD_NUMBER: _ClassVar[int]
        CASTER_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
        ABILITY_HANDLE_FIELD_NUMBER: _ClassVar[int]
        ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
        LOCATION_FIELD_NUMBER: _ClassVar[int]
        VELOCITY_FIELD_NUMBER: _ClassVar[int]
        IS_DODGEABLE_FIELD_NUMBER: _ClassVar[int]
        IS_ATTACK_FIELD_NUMBER: _ClassVar[int]
        handle: int
        caster_handle: int
        caster_unit_type: CMsgBotWorldState.UnitType
        caster_player_id: int
        ability_handle: int
        ability_id: int
        location: CMsgBotWorldState.Vector
        velocity: int
        is_dodgeable: bool
        is_attack: bool
        def __init__(
            self,
            handle: int | None = ...,
            caster_handle: int | None = ...,
            caster_unit_type: CMsgBotWorldState.UnitType | str | None = ...,
            caster_player_id: int | None = ...,
            ability_handle: int | None = ...,
            ability_id: int | None = ...,
            location: CMsgBotWorldState.Vector | _Mapping | None = ...,
            velocity: int | None = ...,
            is_dodgeable: bool = ...,
            is_attack: bool = ...,
        ) -> None: ...

    class AvoidanceZone(_message.Message):
        __slots__ = (
            "location",
            "caster_handle",
            "caster_unit_type",
            "caster_player_id",
            "ability_handle",
            "ability_id",
            "radius",
        )
        LOCATION_FIELD_NUMBER: _ClassVar[int]
        CASTER_HANDLE_FIELD_NUMBER: _ClassVar[int]
        CASTER_UNIT_TYPE_FIELD_NUMBER: _ClassVar[int]
        CASTER_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
        ABILITY_HANDLE_FIELD_NUMBER: _ClassVar[int]
        ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
        RADIUS_FIELD_NUMBER: _ClassVar[int]
        location: CMsgBotWorldState.Vector
        caster_handle: int
        caster_unit_type: CMsgBotWorldState.UnitType
        caster_player_id: int
        ability_handle: int
        ability_id: int
        radius: int
        def __init__(
            self,
            location: CMsgBotWorldState.Vector | _Mapping | None = ...,
            caster_handle: int | None = ...,
            caster_unit_type: CMsgBotWorldState.UnitType | str | None = ...,
            caster_player_id: int | None = ...,
            ability_handle: int | None = ...,
            ability_id: int | None = ...,
            radius: int | None = ...,
        ) -> None: ...

    class Courier(_message.Message):
        __slots__ = ("handle", "state", "player_id")
        HANDLE_FIELD_NUMBER: _ClassVar[int]
        STATE_FIELD_NUMBER: _ClassVar[int]
        PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
        handle: int
        state: CMsgBotWorldState.CourierState
        player_id: int
        def __init__(
            self,
            handle: int | None = ...,
            state: CMsgBotWorldState.CourierState | str | None = ...,
            player_id: int | None = ...,
        ) -> None: ...

    class EventAbility(_message.Message):
        __slots__ = ("ability_id", "player_id", "unit_handle", "location", "is_channel_start")
        ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
        PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
        UNIT_HANDLE_FIELD_NUMBER: _ClassVar[int]
        LOCATION_FIELD_NUMBER: _ClassVar[int]
        IS_CHANNEL_START_FIELD_NUMBER: _ClassVar[int]
        ability_id: int
        player_id: int
        unit_handle: int
        location: CMsgBotWorldState.Vector
        is_channel_start: bool
        def __init__(
            self,
            ability_id: int | None = ...,
            player_id: int | None = ...,
            unit_handle: int | None = ...,
            location: CMsgBotWorldState.Vector | _Mapping | None = ...,
            is_channel_start: bool = ...,
        ) -> None: ...

    class EventDamage(_message.Message):
        __slots__ = (
            "damage",
            "victim_player_id",
            "victim_unit_handle",
            "attacker_player_id",
            "attacker_unit_handle",
            "ability_id",
        )
        DAMAGE_FIELD_NUMBER: _ClassVar[int]
        VICTIM_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
        VICTIM_UNIT_HANDLE_FIELD_NUMBER: _ClassVar[int]
        ATTACKER_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
        ATTACKER_UNIT_HANDLE_FIELD_NUMBER: _ClassVar[int]
        ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
        damage: int
        victim_player_id: int
        victim_unit_handle: int
        attacker_player_id: int
        attacker_unit_handle: int
        ability_id: int
        def __init__(
            self,
            damage: int | None = ...,
            victim_player_id: int | None = ...,
            victim_unit_handle: int | None = ...,
            attacker_player_id: int | None = ...,
            attacker_unit_handle: int | None = ...,
            ability_id: int | None = ...,
        ) -> None: ...

    class EventCourierKilled(_message.Message):
        __slots__ = ("team_id", "courier_unit_handle", "killer_player_id", "killer_unit_handle")
        TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        COURIER_UNIT_HANDLE_FIELD_NUMBER: _ClassVar[int]
        KILLER_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
        KILLER_UNIT_HANDLE_FIELD_NUMBER: _ClassVar[int]
        team_id: int
        courier_unit_handle: int
        killer_player_id: int
        killer_unit_handle: int
        def __init__(
            self,
            team_id: int | None = ...,
            courier_unit_handle: int | None = ...,
            killer_player_id: int | None = ...,
            killer_unit_handle: int | None = ...,
        ) -> None: ...

    class EventRoshanKilled(_message.Message):
        __slots__ = ("killer_player_id", "killer_unit_handle")
        KILLER_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
        KILLER_UNIT_HANDLE_FIELD_NUMBER: _ClassVar[int]
        killer_player_id: int
        killer_unit_handle: int
        def __init__(
            self, killer_player_id: int | None = ..., killer_unit_handle: int | None = ...
        ) -> None: ...

    class EventTree(_message.Message):
        __slots__ = ("tree_id", "destroyed", "respawned", "location", "delayed")
        TREE_ID_FIELD_NUMBER: _ClassVar[int]
        DESTROYED_FIELD_NUMBER: _ClassVar[int]
        RESPAWNED_FIELD_NUMBER: _ClassVar[int]
        LOCATION_FIELD_NUMBER: _ClassVar[int]
        DELAYED_FIELD_NUMBER: _ClassVar[int]
        tree_id: int
        destroyed: bool
        respawned: bool
        location: CMsgBotWorldState.Vector
        delayed: bool
        def __init__(
            self,
            tree_id: int | None = ...,
            destroyed: bool = ...,
            respawned: bool = ...,
            location: CMsgBotWorldState.Vector | _Mapping | None = ...,
            delayed: bool = ...,
        ) -> None: ...

    class Unit(_message.Message):
        __slots__ = (
            "handle",
            "unit_type",
            "name",
            "team_id",
            "level",
            "location",
            "is_alive",
            "player_id",
            "bounding_radius",
            "facing",
            "ground_height",
            "vision_range_daytime",
            "vision_range_nighttime",
            "health",
            "health_max",
            "health_regen",
            "mana",
            "mana_max",
            "mana_regen",
            "base_movement_speed",
            "current_movement_speed",
            "anim_activity",
            "anim_cycle",
            "base_damage",
            "base_damage_variance",
            "bonus_damage",
            "attack_damage",
            "attack_range",
            "attack_speed",
            "attack_anim_point",
            "attack_acquisition_range",
            "attack_projectile_speed",
            "attack_target_handle",
            "attack_target_name",
            "attacks_per_second",
            "last_attack_time",
            "bounty_xp",
            "bounty_gold_min",
            "bounty_gold_max",
            "is_channeling",
            "active_ability_handle",
            "is_attack_immune",
            "is_blind",
            "is_block_disabled",
            "is_disarmed",
            "is_dominated",
            "is_evade_disabled",
            "is_hexed",
            "is_invisible",
            "is_invulnerable",
            "is_magic_immune",
            "is_muted",
            "is_nightmared",
            "is_rooted",
            "is_silenced",
            "is_specially_deniable",
            "is_stunned",
            "is_unable_to_miss",
            "has_scepter",
            "is_specially_undeniable",
            "abilities",
            "items",
            "modifiers",
            "incoming_tracking_projectiles",
            "action_type",
            "ability_target_handle",
            "ability_target_name",
            "is_using_ability",
            "primary_attribute",
            "is_illusion",
            "respawn_time",
            "buyback_cost",
            "buyback_cooldown",
            "spell_amplification",
            "armor",
            "magic_resist",
            "evasion",
            "xp_needed_to_level",
            "ability_points",
            "reliable_gold",
            "unreliable_gold",
            "last_hits",
            "denies",
            "net_worth",
            "strength",
            "agility",
            "intelligence",
            "remaining_lifespan",
            "flying_courier",
            "shrine_cooldown",
            "is_shrine_healing",
        )
        HANDLE_FIELD_NUMBER: _ClassVar[int]
        UNIT_TYPE_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        LOCATION_FIELD_NUMBER: _ClassVar[int]
        IS_ALIVE_FIELD_NUMBER: _ClassVar[int]
        PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
        BOUNDING_RADIUS_FIELD_NUMBER: _ClassVar[int]
        FACING_FIELD_NUMBER: _ClassVar[int]
        GROUND_HEIGHT_FIELD_NUMBER: _ClassVar[int]
        VISION_RANGE_DAYTIME_FIELD_NUMBER: _ClassVar[int]
        VISION_RANGE_NIGHTTIME_FIELD_NUMBER: _ClassVar[int]
        HEALTH_FIELD_NUMBER: _ClassVar[int]
        HEALTH_MAX_FIELD_NUMBER: _ClassVar[int]
        HEALTH_REGEN_FIELD_NUMBER: _ClassVar[int]
        MANA_FIELD_NUMBER: _ClassVar[int]
        MANA_MAX_FIELD_NUMBER: _ClassVar[int]
        MANA_REGEN_FIELD_NUMBER: _ClassVar[int]
        BASE_MOVEMENT_SPEED_FIELD_NUMBER: _ClassVar[int]
        CURRENT_MOVEMENT_SPEED_FIELD_NUMBER: _ClassVar[int]
        ANIM_ACTIVITY_FIELD_NUMBER: _ClassVar[int]
        ANIM_CYCLE_FIELD_NUMBER: _ClassVar[int]
        BASE_DAMAGE_FIELD_NUMBER: _ClassVar[int]
        BASE_DAMAGE_VARIANCE_FIELD_NUMBER: _ClassVar[int]
        BONUS_DAMAGE_FIELD_NUMBER: _ClassVar[int]
        ATTACK_DAMAGE_FIELD_NUMBER: _ClassVar[int]
        ATTACK_RANGE_FIELD_NUMBER: _ClassVar[int]
        ATTACK_SPEED_FIELD_NUMBER: _ClassVar[int]
        ATTACK_ANIM_POINT_FIELD_NUMBER: _ClassVar[int]
        ATTACK_ACQUISITION_RANGE_FIELD_NUMBER: _ClassVar[int]
        ATTACK_PROJECTILE_SPEED_FIELD_NUMBER: _ClassVar[int]
        ATTACK_TARGET_HANDLE_FIELD_NUMBER: _ClassVar[int]
        ATTACK_TARGET_NAME_FIELD_NUMBER: _ClassVar[int]
        ATTACKS_PER_SECOND_FIELD_NUMBER: _ClassVar[int]
        LAST_ATTACK_TIME_FIELD_NUMBER: _ClassVar[int]
        BOUNTY_XP_FIELD_NUMBER: _ClassVar[int]
        BOUNTY_GOLD_MIN_FIELD_NUMBER: _ClassVar[int]
        BOUNTY_GOLD_MAX_FIELD_NUMBER: _ClassVar[int]
        IS_CHANNELING_FIELD_NUMBER: _ClassVar[int]
        ACTIVE_ABILITY_HANDLE_FIELD_NUMBER: _ClassVar[int]
        IS_ATTACK_IMMUNE_FIELD_NUMBER: _ClassVar[int]
        IS_BLIND_FIELD_NUMBER: _ClassVar[int]
        IS_BLOCK_DISABLED_FIELD_NUMBER: _ClassVar[int]
        IS_DISARMED_FIELD_NUMBER: _ClassVar[int]
        IS_DOMINATED_FIELD_NUMBER: _ClassVar[int]
        IS_EVADE_DISABLED_FIELD_NUMBER: _ClassVar[int]
        IS_HEXED_FIELD_NUMBER: _ClassVar[int]
        IS_INVISIBLE_FIELD_NUMBER: _ClassVar[int]
        IS_INVULNERABLE_FIELD_NUMBER: _ClassVar[int]
        IS_MAGIC_IMMUNE_FIELD_NUMBER: _ClassVar[int]
        IS_MUTED_FIELD_NUMBER: _ClassVar[int]
        IS_NIGHTMARED_FIELD_NUMBER: _ClassVar[int]
        IS_ROOTED_FIELD_NUMBER: _ClassVar[int]
        IS_SILENCED_FIELD_NUMBER: _ClassVar[int]
        IS_SPECIALLY_DENIABLE_FIELD_NUMBER: _ClassVar[int]
        IS_STUNNED_FIELD_NUMBER: _ClassVar[int]
        IS_UNABLE_TO_MISS_FIELD_NUMBER: _ClassVar[int]
        HAS_SCEPTER_FIELD_NUMBER: _ClassVar[int]
        IS_SPECIALLY_UNDENIABLE_FIELD_NUMBER: _ClassVar[int]
        ABILITIES_FIELD_NUMBER: _ClassVar[int]
        ITEMS_FIELD_NUMBER: _ClassVar[int]
        MODIFIERS_FIELD_NUMBER: _ClassVar[int]
        INCOMING_TRACKING_PROJECTILES_FIELD_NUMBER: _ClassVar[int]
        ACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
        ABILITY_TARGET_HANDLE_FIELD_NUMBER: _ClassVar[int]
        ABILITY_TARGET_NAME_FIELD_NUMBER: _ClassVar[int]
        IS_USING_ABILITY_FIELD_NUMBER: _ClassVar[int]
        PRIMARY_ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
        IS_ILLUSION_FIELD_NUMBER: _ClassVar[int]
        RESPAWN_TIME_FIELD_NUMBER: _ClassVar[int]
        BUYBACK_COST_FIELD_NUMBER: _ClassVar[int]
        BUYBACK_COOLDOWN_FIELD_NUMBER: _ClassVar[int]
        SPELL_AMPLIFICATION_FIELD_NUMBER: _ClassVar[int]
        ARMOR_FIELD_NUMBER: _ClassVar[int]
        MAGIC_RESIST_FIELD_NUMBER: _ClassVar[int]
        EVASION_FIELD_NUMBER: _ClassVar[int]
        XP_NEEDED_TO_LEVEL_FIELD_NUMBER: _ClassVar[int]
        ABILITY_POINTS_FIELD_NUMBER: _ClassVar[int]
        RELIABLE_GOLD_FIELD_NUMBER: _ClassVar[int]
        UNRELIABLE_GOLD_FIELD_NUMBER: _ClassVar[int]
        LAST_HITS_FIELD_NUMBER: _ClassVar[int]
        DENIES_FIELD_NUMBER: _ClassVar[int]
        NET_WORTH_FIELD_NUMBER: _ClassVar[int]
        STRENGTH_FIELD_NUMBER: _ClassVar[int]
        AGILITY_FIELD_NUMBER: _ClassVar[int]
        INTELLIGENCE_FIELD_NUMBER: _ClassVar[int]
        REMAINING_LIFESPAN_FIELD_NUMBER: _ClassVar[int]
        FLYING_COURIER_FIELD_NUMBER: _ClassVar[int]
        SHRINE_COOLDOWN_FIELD_NUMBER: _ClassVar[int]
        IS_SHRINE_HEALING_FIELD_NUMBER: _ClassVar[int]
        handle: int
        unit_type: CMsgBotWorldState.UnitType
        name: str
        team_id: int
        level: int
        location: CMsgBotWorldState.Vector
        is_alive: bool
        player_id: int
        bounding_radius: int
        facing: int
        ground_height: int
        vision_range_daytime: int
        vision_range_nighttime: int
        health: int
        health_max: int
        health_regen: float
        mana: int
        mana_max: int
        mana_regen: float
        base_movement_speed: int
        current_movement_speed: int
        anim_activity: int
        anim_cycle: float
        base_damage: int
        base_damage_variance: int
        bonus_damage: int
        attack_damage: int
        attack_range: int
        attack_speed: float
        attack_anim_point: float
        attack_acquisition_range: int
        attack_projectile_speed: int
        attack_target_handle: int
        attack_target_name: str
        attacks_per_second: int
        last_attack_time: float
        bounty_xp: int
        bounty_gold_min: int
        bounty_gold_max: int
        is_channeling: bool
        active_ability_handle: int
        is_attack_immune: bool
        is_blind: bool
        is_block_disabled: bool
        is_disarmed: bool
        is_dominated: bool
        is_evade_disabled: bool
        is_hexed: bool
        is_invisible: bool
        is_invulnerable: bool
        is_magic_immune: bool
        is_muted: bool
        is_nightmared: bool
        is_rooted: bool
        is_silenced: bool
        is_specially_deniable: bool
        is_stunned: bool
        is_unable_to_miss: bool
        has_scepter: bool
        is_specially_undeniable: bool
        abilities: _containers.RepeatedCompositeFieldContainer[CMsgBotWorldState.Ability]
        items: _containers.RepeatedCompositeFieldContainer[CMsgBotWorldState.Ability]
        modifiers: _containers.RepeatedCompositeFieldContainer[CMsgBotWorldState.Modifier]
        incoming_tracking_projectiles: _containers.RepeatedCompositeFieldContainer[
            CMsgBotWorldState.TrackingProjectile
        ]
        action_type: int
        ability_target_handle: int
        ability_target_name: str
        is_using_ability: bool
        primary_attribute: int
        is_illusion: bool
        respawn_time: float
        buyback_cost: int
        buyback_cooldown: float
        spell_amplification: float
        armor: float
        magic_resist: float
        evasion: float
        xp_needed_to_level: int
        ability_points: int
        reliable_gold: int
        unreliable_gold: int
        last_hits: int
        denies: int
        net_worth: int
        strength: int
        agility: int
        intelligence: int
        remaining_lifespan: float
        flying_courier: bool
        shrine_cooldown: float
        is_shrine_healing: bool
        def __init__(
            self,
            handle: int | None = ...,
            unit_type: CMsgBotWorldState.UnitType | str | None = ...,
            name: str | None = ...,
            team_id: int | None = ...,
            level: int | None = ...,
            location: CMsgBotWorldState.Vector | _Mapping | None = ...,
            is_alive: bool = ...,
            player_id: int | None = ...,
            bounding_radius: int | None = ...,
            facing: int | None = ...,
            ground_height: int | None = ...,
            vision_range_daytime: int | None = ...,
            vision_range_nighttime: int | None = ...,
            health: int | None = ...,
            health_max: int | None = ...,
            health_regen: float | None = ...,
            mana: int | None = ...,
            mana_max: int | None = ...,
            mana_regen: float | None = ...,
            base_movement_speed: int | None = ...,
            current_movement_speed: int | None = ...,
            anim_activity: int | None = ...,
            anim_cycle: float | None = ...,
            base_damage: int | None = ...,
            base_damage_variance: int | None = ...,
            bonus_damage: int | None = ...,
            attack_damage: int | None = ...,
            attack_range: int | None = ...,
            attack_speed: float | None = ...,
            attack_anim_point: float | None = ...,
            attack_acquisition_range: int | None = ...,
            attack_projectile_speed: int | None = ...,
            attack_target_handle: int | None = ...,
            attack_target_name: str | None = ...,
            attacks_per_second: int | None = ...,
            last_attack_time: float | None = ...,
            bounty_xp: int | None = ...,
            bounty_gold_min: int | None = ...,
            bounty_gold_max: int | None = ...,
            is_channeling: bool = ...,
            active_ability_handle: int | None = ...,
            is_attack_immune: bool = ...,
            is_blind: bool = ...,
            is_block_disabled: bool = ...,
            is_disarmed: bool = ...,
            is_dominated: bool = ...,
            is_evade_disabled: bool = ...,
            is_hexed: bool = ...,
            is_invisible: bool = ...,
            is_invulnerable: bool = ...,
            is_magic_immune: bool = ...,
            is_muted: bool = ...,
            is_nightmared: bool = ...,
            is_rooted: bool = ...,
            is_silenced: bool = ...,
            is_specially_deniable: bool = ...,
            is_stunned: bool = ...,
            is_unable_to_miss: bool = ...,
            has_scepter: bool = ...,
            is_specially_undeniable: bool = ...,
            abilities: _Iterable[CMsgBotWorldState.Ability | _Mapping] | None = ...,
            items: _Iterable[CMsgBotWorldState.Ability | _Mapping] | None = ...,
            modifiers: _Iterable[CMsgBotWorldState.Modifier | _Mapping] | None = ...,
            incoming_tracking_projectiles: _Iterable[
                CMsgBotWorldState.TrackingProjectile | _Mapping
            ]
            | None = ...,
            action_type: int | None = ...,
            ability_target_handle: int | None = ...,
            ability_target_name: str | None = ...,
            is_using_ability: bool = ...,
            primary_attribute: int | None = ...,
            is_illusion: bool = ...,
            respawn_time: float | None = ...,
            buyback_cost: int | None = ...,
            buyback_cooldown: float | None = ...,
            spell_amplification: float | None = ...,
            armor: float | None = ...,
            magic_resist: float | None = ...,
            evasion: float | None = ...,
            xp_needed_to_level: int | None = ...,
            ability_points: int | None = ...,
            reliable_gold: int | None = ...,
            unreliable_gold: int | None = ...,
            last_hits: int | None = ...,
            denies: int | None = ...,
            net_worth: int | None = ...,
            strength: int | None = ...,
            agility: int | None = ...,
            intelligence: int | None = ...,
            remaining_lifespan: float | None = ...,
            flying_courier: bool = ...,
            shrine_cooldown: float | None = ...,
            is_shrine_healing: bool = ...,
        ) -> None: ...

    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    GAME_TIME_FIELD_NUMBER: _ClassVar[int]
    DOTA_TIME_FIELD_NUMBER: _ClassVar[int]
    GAME_STATE_FIELD_NUMBER: _ClassVar[int]
    HERO_PICK_STATE_FIELD_NUMBER: _ClassVar[int]
    TIME_OF_DAY_FIELD_NUMBER: _ClassVar[int]
    GLYPH_COOLDOWN_FIELD_NUMBER: _ClassVar[int]
    GLYPH_COOLDOWN_ENEMY_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    DROPPED_ITEMS_FIELD_NUMBER: _ClassVar[int]
    DROPPED_ITEMS_DELTAS_FIELD_NUMBER: _ClassVar[int]
    RUNE_INFOS_FIELD_NUMBER: _ClassVar[int]
    RUNE_INFOS_DELTAS_FIELD_NUMBER: _ClassVar[int]
    INCOMING_TELEPORTS_FIELD_NUMBER: _ClassVar[int]
    LINEAR_PROJECTILES_FIELD_NUMBER: _ClassVar[int]
    AVOIDANCE_ZONES_FIELD_NUMBER: _ClassVar[int]
    COURIERS_FIELD_NUMBER: _ClassVar[int]
    ABILITY_EVENTS_FIELD_NUMBER: _ClassVar[int]
    DAMAGE_EVENTS_FIELD_NUMBER: _ClassVar[int]
    COURIER_KILLED_EVENTS_FIELD_NUMBER: _ClassVar[int]
    ROSHAN_KILLED_EVENTS_FIELD_NUMBER: _ClassVar[int]
    TREE_EVENTS_FIELD_NUMBER: _ClassVar[int]
    team_id: int
    game_time: float
    dota_time: float
    game_state: int
    hero_pick_state: int
    time_of_day: float
    glyph_cooldown: float
    glyph_cooldown_enemy: float
    players: _containers.RepeatedCompositeFieldContainer[CMsgBotWorldState.Player]
    units: _containers.RepeatedCompositeFieldContainer[CMsgBotWorldState.Unit]
    dropped_items: _containers.RepeatedCompositeFieldContainer[CMsgBotWorldState.DroppedItem]
    dropped_items_deltas: _containers.RepeatedScalarFieldContainer[int]
    rune_infos: _containers.RepeatedCompositeFieldContainer[CMsgBotWorldState.RuneInfo]
    rune_infos_deltas: _containers.RepeatedScalarFieldContainer[int]
    incoming_teleports: _containers.RepeatedCompositeFieldContainer[CMsgBotWorldState.TeleportInfo]
    linear_projectiles: _containers.RepeatedCompositeFieldContainer[
        CMsgBotWorldState.LinearProjectile
    ]
    avoidance_zones: _containers.RepeatedCompositeFieldContainer[CMsgBotWorldState.AvoidanceZone]
    couriers: _containers.RepeatedCompositeFieldContainer[CMsgBotWorldState.Courier]
    ability_events: _containers.RepeatedCompositeFieldContainer[CMsgBotWorldState.EventAbility]
    damage_events: _containers.RepeatedCompositeFieldContainer[CMsgBotWorldState.EventDamage]
    courier_killed_events: _containers.RepeatedCompositeFieldContainer[
        CMsgBotWorldState.EventCourierKilled
    ]
    roshan_killed_events: _containers.RepeatedCompositeFieldContainer[
        CMsgBotWorldState.EventRoshanKilled
    ]
    tree_events: _containers.RepeatedCompositeFieldContainer[CMsgBotWorldState.EventTree]
    def __init__(
        self,
        team_id: int | None = ...,
        game_time: float | None = ...,
        dota_time: float | None = ...,
        game_state: int | None = ...,
        hero_pick_state: int | None = ...,
        time_of_day: float | None = ...,
        glyph_cooldown: float | None = ...,
        glyph_cooldown_enemy: float | None = ...,
        players: _Iterable[CMsgBotWorldState.Player | _Mapping] | None = ...,
        units: _Iterable[CMsgBotWorldState.Unit | _Mapping] | None = ...,
        dropped_items: _Iterable[CMsgBotWorldState.DroppedItem | _Mapping] | None = ...,
        dropped_items_deltas: _Iterable[int] | None = ...,
        rune_infos: _Iterable[CMsgBotWorldState.RuneInfo | _Mapping] | None = ...,
        rune_infos_deltas: _Iterable[int] | None = ...,
        incoming_teleports: _Iterable[CMsgBotWorldState.TeleportInfo | _Mapping] | None = ...,
        linear_projectiles: _Iterable[CMsgBotWorldState.LinearProjectile | _Mapping] | None = ...,
        avoidance_zones: _Iterable[CMsgBotWorldState.AvoidanceZone | _Mapping] | None = ...,
        couriers: _Iterable[CMsgBotWorldState.Courier | _Mapping] | None = ...,
        ability_events: _Iterable[CMsgBotWorldState.EventAbility | _Mapping] | None = ...,
        damage_events: _Iterable[CMsgBotWorldState.EventDamage | _Mapping] | None = ...,
        courier_killed_events: _Iterable[CMsgBotWorldState.EventCourierKilled | _Mapping]
        | None = ...,
        roshan_killed_events: _Iterable[CMsgBotWorldState.EventRoshanKilled | _Mapping]
        | None = ...,
        tree_events: _Iterable[CMsgBotWorldState.EventTree | _Mapping] | None = ...,
    ) -> None: ...
