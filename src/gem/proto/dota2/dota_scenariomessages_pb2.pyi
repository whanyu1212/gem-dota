from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class CScenario_Position(_message.Message):
    __slots__ = ("x", "y")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    def __init__(self, x: float | None = ..., y: float | None = ...) -> None: ...

class CScenarioGame_RoshanSpawner(_message.Message):
    __slots__ = ("kill_count", "state", "cooldown", "killer_team")
    KILL_COUNT_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    COOLDOWN_FIELD_NUMBER: _ClassVar[int]
    KILLER_TEAM_FIELD_NUMBER: _ClassVar[int]
    kill_count: int
    state: int
    cooldown: float
    killer_team: int
    def __init__(
        self,
        kill_count: int | None = ...,
        state: int | None = ...,
        cooldown: float | None = ...,
        killer_team: int | None = ...,
    ) -> None: ...

class CScenarioEnt_Courier(_message.Message):
    __slots__ = ("team_number", "owner_player_id", "cooldown")
    TEAM_NUMBER_FIELD_NUMBER: _ClassVar[int]
    OWNER_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    COOLDOWN_FIELD_NUMBER: _ClassVar[int]
    team_number: int
    owner_player_id: int
    cooldown: float
    def __init__(
        self,
        team_number: int | None = ...,
        owner_player_id: int | None = ...,
        cooldown: float | None = ...,
    ) -> None: ...

class CScenarioEnt_NPC(_message.Message):
    __slots__ = (
        "position",
        "unit_name",
        "team_number",
        "health_frac",
        "owning_camp",
        "owning_camp_position",
        "invade_goal",
    )
    POSITION_FIELD_NUMBER: _ClassVar[int]
    UNIT_NAME_FIELD_NUMBER: _ClassVar[int]
    TEAM_NUMBER_FIELD_NUMBER: _ClassVar[int]
    HEALTH_FRAC_FIELD_NUMBER: _ClassVar[int]
    OWNING_CAMP_FIELD_NUMBER: _ClassVar[int]
    OWNING_CAMP_POSITION_FIELD_NUMBER: _ClassVar[int]
    INVADE_GOAL_FIELD_NUMBER: _ClassVar[int]
    position: CScenario_Position
    unit_name: str
    team_number: int
    health_frac: float
    owning_camp: str
    owning_camp_position: CScenario_Position
    invade_goal: str
    def __init__(
        self,
        position: CScenario_Position | _Mapping | None = ...,
        unit_name: str | None = ...,
        team_number: int | None = ...,
        health_frac: float | None = ...,
        owning_camp: str | None = ...,
        owning_camp_position: CScenario_Position | _Mapping | None = ...,
        invade_goal: str | None = ...,
    ) -> None: ...

class CScenarioEnt_SpiritBear(_message.Message):
    __slots__ = ("owner_id", "team_id")
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    owner_id: int
    team_id: int
    def __init__(self, owner_id: int | None = ..., team_id: int | None = ...) -> None: ...

class CScenarioEnt_DroppedItem(_message.Message):
    __slots__ = ("position",)
    POSITION_FIELD_NUMBER: _ClassVar[int]
    position: CScenario_Position
    def __init__(self, position: CScenario_Position | _Mapping | None = ...) -> None: ...

class CMsgDotaScenario(_message.Message):
    __slots__ = (
        "lobby_id",
        "game",
        "teams",
        "heroes",
        "stock",
        "buildings",
        "entities",
        "items",
        "modifiers",
    )
    class EntityRef(_message.Message):
        __slots__ = ("player_id", "neutral_stash_id", "entity_idx", "roshan", "ability_name")
        PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
        NEUTRAL_STASH_ID_FIELD_NUMBER: _ClassVar[int]
        ENTITY_IDX_FIELD_NUMBER: _ClassVar[int]
        ROSHAN_FIELD_NUMBER: _ClassVar[int]
        ABILITY_NAME_FIELD_NUMBER: _ClassVar[int]
        player_id: int
        neutral_stash_id: int
        entity_idx: int
        roshan: bool
        ability_name: str
        def __init__(
            self,
            player_id: int | None = ...,
            neutral_stash_id: int | None = ...,
            entity_idx: int | None = ...,
            roshan: bool = ...,
            ability_name: str | None = ...,
        ) -> None: ...

    class Game(_message.Message):
        __slots__ = ("match_id", "game_mode", "clock_time", "internal_time", "roshan")
        MATCH_ID_FIELD_NUMBER: _ClassVar[int]
        GAME_MODE_FIELD_NUMBER: _ClassVar[int]
        CLOCK_TIME_FIELD_NUMBER: _ClassVar[int]
        INTERNAL_TIME_FIELD_NUMBER: _ClassVar[int]
        ROSHAN_FIELD_NUMBER: _ClassVar[int]
        match_id: int
        game_mode: int
        clock_time: float
        internal_time: float
        roshan: CScenarioGame_RoshanSpawner
        def __init__(
            self,
            match_id: int | None = ...,
            game_mode: int | None = ...,
            clock_time: float | None = ...,
            internal_time: float | None = ...,
            roshan: CScenarioGame_RoshanSpawner | _Mapping | None = ...,
        ) -> None: ...

    class TeamNeutralItem(_message.Message):
        __slots__ = ("name", "consumed", "tier")
        NAME_FIELD_NUMBER: _ClassVar[int]
        CONSUMED_FIELD_NUMBER: _ClassVar[int]
        TIER_FIELD_NUMBER: _ClassVar[int]
        name: str
        consumed: bool
        tier: int
        def __init__(
            self, name: str | None = ..., consumed: bool = ..., tier: int | None = ...
        ) -> None: ...

    class Team(_message.Message):
        __slots__ = (
            "team_number",
            "neutral_items",
            "hero_kills",
            "tower_kills",
            "barracks_kills",
            "glyph_cooldown",
            "radar_cooldown",
        )
        TEAM_NUMBER_FIELD_NUMBER: _ClassVar[int]
        NEUTRAL_ITEMS_FIELD_NUMBER: _ClassVar[int]
        HERO_KILLS_FIELD_NUMBER: _ClassVar[int]
        TOWER_KILLS_FIELD_NUMBER: _ClassVar[int]
        BARRACKS_KILLS_FIELD_NUMBER: _ClassVar[int]
        GLYPH_COOLDOWN_FIELD_NUMBER: _ClassVar[int]
        RADAR_COOLDOWN_FIELD_NUMBER: _ClassVar[int]
        team_number: int
        neutral_items: _containers.RepeatedCompositeFieldContainer[CMsgDotaScenario.TeamNeutralItem]
        hero_kills: int
        tower_kills: int
        barracks_kills: int
        glyph_cooldown: float
        radar_cooldown: float
        def __init__(
            self,
            team_number: int | None = ...,
            neutral_items: _Iterable[CMsgDotaScenario.TeamNeutralItem | _Mapping] | None = ...,
            hero_kills: int | None = ...,
            tower_kills: int | None = ...,
            barracks_kills: int | None = ...,
            glyph_cooldown: float | None = ...,
            radar_cooldown: float | None = ...,
        ) -> None: ...

    class HeroHeroInt(_message.Message):
        __slots__ = ("player_id", "value")
        PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        player_id: int
        value: int
        def __init__(self, player_id: int | None = ..., value: int | None = ...) -> None: ...

    class HeroHeroFloat(_message.Message):
        __slots__ = ("player_id", "value")
        PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        player_id: int
        value: float
        def __init__(self, player_id: int | None = ..., value: float | None = ...) -> None: ...

    class DamageStatsByType(_message.Message):
        __slots__ = (
            "damage_type",
            "received_pre_reduction",
            "received_post_reduction",
            "outgoing_pre_reduction",
            "outgoing_post_reduction",
        )
        DAMAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
        RECEIVED_PRE_REDUCTION_FIELD_NUMBER: _ClassVar[int]
        RECEIVED_POST_REDUCTION_FIELD_NUMBER: _ClassVar[int]
        OUTGOING_PRE_REDUCTION_FIELD_NUMBER: _ClassVar[int]
        OUTGOING_POST_REDUCTION_FIELD_NUMBER: _ClassVar[int]
        damage_type: int
        received_pre_reduction: float
        received_post_reduction: float
        outgoing_pre_reduction: float
        outgoing_post_reduction: float
        def __init__(
            self,
            damage_type: int | None = ...,
            received_pre_reduction: float | None = ...,
            received_post_reduction: float | None = ...,
            outgoing_pre_reduction: float | None = ...,
            outgoing_post_reduction: float | None = ...,
        ) -> None: ...

    class HeroAbility(_message.Message):
        __slots__ = ("name", "level")
        NAME_FIELD_NUMBER: _ClassVar[int]
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        name: str
        level: int
        def __init__(self, name: str | None = ..., level: int | None = ...) -> None: ...

    class HeroNeutralChoice(_message.Message):
        __slots__ = ("choice_index", "artifact_name", "enchantment_name")
        CHOICE_INDEX_FIELD_NUMBER: _ClassVar[int]
        ARTIFACT_NAME_FIELD_NUMBER: _ClassVar[int]
        ENCHANTMENT_NAME_FIELD_NUMBER: _ClassVar[int]
        choice_index: int
        artifact_name: str
        enchantment_name: str
        def __init__(
            self,
            choice_index: int | None = ...,
            artifact_name: str | None = ...,
            enchantment_name: str | None = ...,
        ) -> None: ...

    class HeroNeutralTier(_message.Message):
        __slots__ = ("tier", "choices", "selected_artifact", "selected_enchantment")
        TIER_FIELD_NUMBER: _ClassVar[int]
        CHOICES_FIELD_NUMBER: _ClassVar[int]
        SELECTED_ARTIFACT_FIELD_NUMBER: _ClassVar[int]
        SELECTED_ENCHANTMENT_FIELD_NUMBER: _ClassVar[int]
        tier: int
        choices: _containers.RepeatedCompositeFieldContainer[CMsgDotaScenario.HeroNeutralChoice]
        selected_artifact: int
        selected_enchantment: int
        def __init__(
            self,
            tier: int | None = ...,
            choices: _Iterable[CMsgDotaScenario.HeroNeutralChoice | _Mapping] | None = ...,
            selected_artifact: int | None = ...,
            selected_enchantment: int | None = ...,
        ) -> None: ...

    class Hero(_message.Message):
        __slots__ = (
            "steam_id",
            "player_id",
            "team_id",
            "hero",
            "total_xp",
            "bkb_charges_used",
            "aeon_charges_used",
            "reliable_gold",
            "unreliable_gold",
            "total_earned_gold",
            "shared_gold",
            "hero_kill_gold",
            "creep_kill_gold",
            "neutral_kill_gold",
            "courier_gold",
            "bounty_gold",
            "roshan_gold",
            "building_gold",
            "other_gold",
            "income_gold",
            "ward_kill_gold",
            "ability_gold",
            "denies",
            "last_hits",
            "last_hit_streak",
            "last_hit_multikill",
            "nearby_creep_death_count",
            "claimed_deny_count",
            "claimed_miss_count",
            "miss_count",
            "buyback_cooldown_time",
            "buyback_gold_limit_time",
            "stun_duration",
            "healing",
            "tower_kills",
            "roshan_kills",
            "observer_wards_placed",
            "sentry_wards_placed",
            "creeps_stacked",
            "camps_stacked",
            "rune_pickups",
            "gold_spent_on_support",
            "hero_damage",
            "wards_purchased",
            "wards_destroyed",
            "gold_spent_on_consumables",
            "gold_spent_on_items",
            "gold_spent_on_buybacks",
            "gold_lost_to_death",
            "kills",
            "assists",
            "deaths",
            "kill_streak",
            "respawn_seconds",
            "last_buyback_time",
            "first_blood_claimed",
            "first_blood_given",
            "bounty_runes",
            "outposts_captured",
            "position",
            "enemy_kills",
            "damage_stats",
            "abilities",
            "hero_facet",
            "total_madstone",
            "current_madstone",
            "neutral_tiers",
            "refresher_charges_used",
        )
        STEAM_ID_FIELD_NUMBER: _ClassVar[int]
        PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
        TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        HERO_FIELD_NUMBER: _ClassVar[int]
        TOTAL_XP_FIELD_NUMBER: _ClassVar[int]
        BKB_CHARGES_USED_FIELD_NUMBER: _ClassVar[int]
        AEON_CHARGES_USED_FIELD_NUMBER: _ClassVar[int]
        RELIABLE_GOLD_FIELD_NUMBER: _ClassVar[int]
        UNRELIABLE_GOLD_FIELD_NUMBER: _ClassVar[int]
        TOTAL_EARNED_GOLD_FIELD_NUMBER: _ClassVar[int]
        SHARED_GOLD_FIELD_NUMBER: _ClassVar[int]
        HERO_KILL_GOLD_FIELD_NUMBER: _ClassVar[int]
        CREEP_KILL_GOLD_FIELD_NUMBER: _ClassVar[int]
        NEUTRAL_KILL_GOLD_FIELD_NUMBER: _ClassVar[int]
        COURIER_GOLD_FIELD_NUMBER: _ClassVar[int]
        BOUNTY_GOLD_FIELD_NUMBER: _ClassVar[int]
        ROSHAN_GOLD_FIELD_NUMBER: _ClassVar[int]
        BUILDING_GOLD_FIELD_NUMBER: _ClassVar[int]
        OTHER_GOLD_FIELD_NUMBER: _ClassVar[int]
        INCOME_GOLD_FIELD_NUMBER: _ClassVar[int]
        WARD_KILL_GOLD_FIELD_NUMBER: _ClassVar[int]
        ABILITY_GOLD_FIELD_NUMBER: _ClassVar[int]
        DENIES_FIELD_NUMBER: _ClassVar[int]
        LAST_HITS_FIELD_NUMBER: _ClassVar[int]
        LAST_HIT_STREAK_FIELD_NUMBER: _ClassVar[int]
        LAST_HIT_MULTIKILL_FIELD_NUMBER: _ClassVar[int]
        NEARBY_CREEP_DEATH_COUNT_FIELD_NUMBER: _ClassVar[int]
        CLAIMED_DENY_COUNT_FIELD_NUMBER: _ClassVar[int]
        CLAIMED_MISS_COUNT_FIELD_NUMBER: _ClassVar[int]
        MISS_COUNT_FIELD_NUMBER: _ClassVar[int]
        BUYBACK_COOLDOWN_TIME_FIELD_NUMBER: _ClassVar[int]
        BUYBACK_GOLD_LIMIT_TIME_FIELD_NUMBER: _ClassVar[int]
        STUN_DURATION_FIELD_NUMBER: _ClassVar[int]
        HEALING_FIELD_NUMBER: _ClassVar[int]
        TOWER_KILLS_FIELD_NUMBER: _ClassVar[int]
        ROSHAN_KILLS_FIELD_NUMBER: _ClassVar[int]
        OBSERVER_WARDS_PLACED_FIELD_NUMBER: _ClassVar[int]
        SENTRY_WARDS_PLACED_FIELD_NUMBER: _ClassVar[int]
        CREEPS_STACKED_FIELD_NUMBER: _ClassVar[int]
        CAMPS_STACKED_FIELD_NUMBER: _ClassVar[int]
        RUNE_PICKUPS_FIELD_NUMBER: _ClassVar[int]
        GOLD_SPENT_ON_SUPPORT_FIELD_NUMBER: _ClassVar[int]
        HERO_DAMAGE_FIELD_NUMBER: _ClassVar[int]
        WARDS_PURCHASED_FIELD_NUMBER: _ClassVar[int]
        WARDS_DESTROYED_FIELD_NUMBER: _ClassVar[int]
        GOLD_SPENT_ON_CONSUMABLES_FIELD_NUMBER: _ClassVar[int]
        GOLD_SPENT_ON_ITEMS_FIELD_NUMBER: _ClassVar[int]
        GOLD_SPENT_ON_BUYBACKS_FIELD_NUMBER: _ClassVar[int]
        GOLD_LOST_TO_DEATH_FIELD_NUMBER: _ClassVar[int]
        KILLS_FIELD_NUMBER: _ClassVar[int]
        ASSISTS_FIELD_NUMBER: _ClassVar[int]
        DEATHS_FIELD_NUMBER: _ClassVar[int]
        KILL_STREAK_FIELD_NUMBER: _ClassVar[int]
        RESPAWN_SECONDS_FIELD_NUMBER: _ClassVar[int]
        LAST_BUYBACK_TIME_FIELD_NUMBER: _ClassVar[int]
        FIRST_BLOOD_CLAIMED_FIELD_NUMBER: _ClassVar[int]
        FIRST_BLOOD_GIVEN_FIELD_NUMBER: _ClassVar[int]
        BOUNTY_RUNES_FIELD_NUMBER: _ClassVar[int]
        OUTPOSTS_CAPTURED_FIELD_NUMBER: _ClassVar[int]
        POSITION_FIELD_NUMBER: _ClassVar[int]
        ENEMY_KILLS_FIELD_NUMBER: _ClassVar[int]
        DAMAGE_STATS_FIELD_NUMBER: _ClassVar[int]
        ABILITIES_FIELD_NUMBER: _ClassVar[int]
        HERO_FACET_FIELD_NUMBER: _ClassVar[int]
        TOTAL_MADSTONE_FIELD_NUMBER: _ClassVar[int]
        CURRENT_MADSTONE_FIELD_NUMBER: _ClassVar[int]
        NEUTRAL_TIERS_FIELD_NUMBER: _ClassVar[int]
        REFRESHER_CHARGES_USED_FIELD_NUMBER: _ClassVar[int]
        steam_id: int
        player_id: int
        team_id: int
        hero: str
        total_xp: int
        bkb_charges_used: int
        aeon_charges_used: int
        reliable_gold: int
        unreliable_gold: int
        total_earned_gold: int
        shared_gold: int
        hero_kill_gold: int
        creep_kill_gold: int
        neutral_kill_gold: int
        courier_gold: int
        bounty_gold: int
        roshan_gold: int
        building_gold: int
        other_gold: int
        income_gold: int
        ward_kill_gold: int
        ability_gold: int
        denies: int
        last_hits: int
        last_hit_streak: int
        last_hit_multikill: int
        nearby_creep_death_count: int
        claimed_deny_count: int
        claimed_miss_count: int
        miss_count: int
        buyback_cooldown_time: float
        buyback_gold_limit_time: float
        stun_duration: float
        healing: float
        tower_kills: int
        roshan_kills: int
        observer_wards_placed: int
        sentry_wards_placed: int
        creeps_stacked: int
        camps_stacked: int
        rune_pickups: int
        gold_spent_on_support: int
        hero_damage: float
        wards_purchased: int
        wards_destroyed: int
        gold_spent_on_consumables: int
        gold_spent_on_items: int
        gold_spent_on_buybacks: int
        gold_lost_to_death: int
        kills: int
        assists: int
        deaths: int
        kill_streak: int
        respawn_seconds: int
        last_buyback_time: int
        first_blood_claimed: bool
        first_blood_given: bool
        bounty_runes: int
        outposts_captured: int
        position: CScenario_Position
        enemy_kills: _containers.RepeatedCompositeFieldContainer[CMsgDotaScenario.HeroHeroInt]
        damage_stats: _containers.RepeatedCompositeFieldContainer[
            CMsgDotaScenario.DamageStatsByType
        ]
        abilities: _containers.RepeatedCompositeFieldContainer[CMsgDotaScenario.HeroAbility]
        hero_facet: int
        total_madstone: int
        current_madstone: int
        neutral_tiers: _containers.RepeatedCompositeFieldContainer[CMsgDotaScenario.HeroNeutralTier]
        refresher_charges_used: int
        def __init__(
            self,
            steam_id: int | None = ...,
            player_id: int | None = ...,
            team_id: int | None = ...,
            hero: str | None = ...,
            total_xp: int | None = ...,
            bkb_charges_used: int | None = ...,
            aeon_charges_used: int | None = ...,
            reliable_gold: int | None = ...,
            unreliable_gold: int | None = ...,
            total_earned_gold: int | None = ...,
            shared_gold: int | None = ...,
            hero_kill_gold: int | None = ...,
            creep_kill_gold: int | None = ...,
            neutral_kill_gold: int | None = ...,
            courier_gold: int | None = ...,
            bounty_gold: int | None = ...,
            roshan_gold: int | None = ...,
            building_gold: int | None = ...,
            other_gold: int | None = ...,
            income_gold: int | None = ...,
            ward_kill_gold: int | None = ...,
            ability_gold: int | None = ...,
            denies: int | None = ...,
            last_hits: int | None = ...,
            last_hit_streak: int | None = ...,
            last_hit_multikill: int | None = ...,
            nearby_creep_death_count: int | None = ...,
            claimed_deny_count: int | None = ...,
            claimed_miss_count: int | None = ...,
            miss_count: int | None = ...,
            buyback_cooldown_time: float | None = ...,
            buyback_gold_limit_time: float | None = ...,
            stun_duration: float | None = ...,
            healing: float | None = ...,
            tower_kills: int | None = ...,
            roshan_kills: int | None = ...,
            observer_wards_placed: int | None = ...,
            sentry_wards_placed: int | None = ...,
            creeps_stacked: int | None = ...,
            camps_stacked: int | None = ...,
            rune_pickups: int | None = ...,
            gold_spent_on_support: int | None = ...,
            hero_damage: float | None = ...,
            wards_purchased: int | None = ...,
            wards_destroyed: int | None = ...,
            gold_spent_on_consumables: int | None = ...,
            gold_spent_on_items: int | None = ...,
            gold_spent_on_buybacks: int | None = ...,
            gold_lost_to_death: int | None = ...,
            kills: int | None = ...,
            assists: int | None = ...,
            deaths: int | None = ...,
            kill_streak: int | None = ...,
            respawn_seconds: int | None = ...,
            last_buyback_time: int | None = ...,
            first_blood_claimed: bool = ...,
            first_blood_given: bool = ...,
            bounty_runes: int | None = ...,
            outposts_captured: int | None = ...,
            position: CScenario_Position | _Mapping | None = ...,
            enemy_kills: _Iterable[CMsgDotaScenario.HeroHeroInt | _Mapping] | None = ...,
            damage_stats: _Iterable[CMsgDotaScenario.DamageStatsByType | _Mapping] | None = ...,
            abilities: _Iterable[CMsgDotaScenario.HeroAbility | _Mapping] | None = ...,
            hero_facet: int | None = ...,
            total_madstone: int | None = ...,
            current_madstone: int | None = ...,
            neutral_tiers: _Iterable[CMsgDotaScenario.HeroNeutralTier | _Mapping] | None = ...,
            refresher_charges_used: int | None = ...,
        ) -> None: ...

    class Stock(_message.Message):
        __slots__ = ("name", "team_number", "player_id", "current_stock", "cooldown", "bonus_stock")
        NAME_FIELD_NUMBER: _ClassVar[int]
        TEAM_NUMBER_FIELD_NUMBER: _ClassVar[int]
        PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
        CURRENT_STOCK_FIELD_NUMBER: _ClassVar[int]
        COOLDOWN_FIELD_NUMBER: _ClassVar[int]
        BONUS_STOCK_FIELD_NUMBER: _ClassVar[int]
        name: str
        team_number: int
        player_id: int
        current_stock: int
        cooldown: float
        bonus_stock: int
        def __init__(
            self,
            name: str | None = ...,
            team_number: int | None = ...,
            player_id: int | None = ...,
            current_stock: int | None = ...,
            cooldown: float | None = ...,
            bonus_stock: int | None = ...,
        ) -> None: ...

    class Building(_message.Message):
        __slots__ = ("entity_name", "entity_class", "team_id", "is_destroyed", "health_frac")
        ENTITY_NAME_FIELD_NUMBER: _ClassVar[int]
        ENTITY_CLASS_FIELD_NUMBER: _ClassVar[int]
        TEAM_ID_FIELD_NUMBER: _ClassVar[int]
        IS_DESTROYED_FIELD_NUMBER: _ClassVar[int]
        HEALTH_FRAC_FIELD_NUMBER: _ClassVar[int]
        entity_name: str
        entity_class: str
        team_id: int
        is_destroyed: bool
        health_frac: float
        def __init__(
            self,
            entity_name: str | None = ...,
            entity_class: str | None = ...,
            team_id: int | None = ...,
            is_destroyed: bool = ...,
            health_frac: float | None = ...,
        ) -> None: ...

    class Entity(_message.Message):
        __slots__ = ("courier", "npc", "spirit_bear", "dropped_item")
        COURIER_FIELD_NUMBER: _ClassVar[int]
        NPC_FIELD_NUMBER: _ClassVar[int]
        SPIRIT_BEAR_FIELD_NUMBER: _ClassVar[int]
        DROPPED_ITEM_FIELD_NUMBER: _ClassVar[int]
        courier: CScenarioEnt_Courier
        npc: CScenarioEnt_NPC
        spirit_bear: CScenarioEnt_SpiritBear
        dropped_item: CScenarioEnt_DroppedItem
        def __init__(
            self,
            courier: CScenarioEnt_Courier | _Mapping | None = ...,
            npc: CScenarioEnt_NPC | _Mapping | None = ...,
            spirit_bear: CScenarioEnt_SpiritBear | _Mapping | None = ...,
            dropped_item: CScenarioEnt_DroppedItem | _Mapping | None = ...,
        ) -> None: ...

    class Item(_message.Message):
        __slots__ = (
            "name",
            "location",
            "owner_id",
            "item_slot",
            "neutral_drop_team",
            "charges",
            "secondary_charges",
            "lifetime",
            "stored_rune_type",
            "level",
        )
        NAME_FIELD_NUMBER: _ClassVar[int]
        LOCATION_FIELD_NUMBER: _ClassVar[int]
        OWNER_ID_FIELD_NUMBER: _ClassVar[int]
        ITEM_SLOT_FIELD_NUMBER: _ClassVar[int]
        NEUTRAL_DROP_TEAM_FIELD_NUMBER: _ClassVar[int]
        CHARGES_FIELD_NUMBER: _ClassVar[int]
        SECONDARY_CHARGES_FIELD_NUMBER: _ClassVar[int]
        LIFETIME_FIELD_NUMBER: _ClassVar[int]
        STORED_RUNE_TYPE_FIELD_NUMBER: _ClassVar[int]
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        name: str
        location: CMsgDotaScenario.EntityRef
        owner_id: int
        item_slot: int
        neutral_drop_team: int
        charges: int
        secondary_charges: int
        lifetime: float
        stored_rune_type: int
        level: int
        def __init__(
            self,
            name: str | None = ...,
            location: CMsgDotaScenario.EntityRef | _Mapping | None = ...,
            owner_id: int | None = ...,
            item_slot: int | None = ...,
            neutral_drop_team: int | None = ...,
            charges: int | None = ...,
            secondary_charges: int | None = ...,
            lifetime: float | None = ...,
            stored_rune_type: int | None = ...,
            level: int | None = ...,
        ) -> None: ...

    class Modifier(_message.Message):
        __slots__ = (
            "name",
            "parent",
            "caster",
            "ability",
            "duration",
            "lifetime_remaining",
            "stack_count",
            "create_even_if_existing",
            "create_without_caster",
            "create_without_ability",
            "moonshard_consumed_bonus",
            "moonshard_consumed_bonus_night_vision",
            "wardtruesight_range",
            "ultimate_scepter_consumed_alchemist_bonus_all_stats",
            "ultimate_scepter_consumed_alchemist_bonus_health",
            "ultimate_scepter_consumed_alchemist_bonus_mana",
        )
        NAME_FIELD_NUMBER: _ClassVar[int]
        PARENT_FIELD_NUMBER: _ClassVar[int]
        CASTER_FIELD_NUMBER: _ClassVar[int]
        ABILITY_FIELD_NUMBER: _ClassVar[int]
        DURATION_FIELD_NUMBER: _ClassVar[int]
        LIFETIME_REMAINING_FIELD_NUMBER: _ClassVar[int]
        STACK_COUNT_FIELD_NUMBER: _ClassVar[int]
        CREATE_EVEN_IF_EXISTING_FIELD_NUMBER: _ClassVar[int]
        CREATE_WITHOUT_CASTER_FIELD_NUMBER: _ClassVar[int]
        CREATE_WITHOUT_ABILITY_FIELD_NUMBER: _ClassVar[int]
        MOONSHARD_CONSUMED_BONUS_FIELD_NUMBER: _ClassVar[int]
        MOONSHARD_CONSUMED_BONUS_NIGHT_VISION_FIELD_NUMBER: _ClassVar[int]
        WARDTRUESIGHT_RANGE_FIELD_NUMBER: _ClassVar[int]
        ULTIMATE_SCEPTER_CONSUMED_ALCHEMIST_BONUS_ALL_STATS_FIELD_NUMBER: _ClassVar[int]
        ULTIMATE_SCEPTER_CONSUMED_ALCHEMIST_BONUS_HEALTH_FIELD_NUMBER: _ClassVar[int]
        ULTIMATE_SCEPTER_CONSUMED_ALCHEMIST_BONUS_MANA_FIELD_NUMBER: _ClassVar[int]
        name: str
        parent: CMsgDotaScenario.EntityRef
        caster: CMsgDotaScenario.EntityRef
        ability: CMsgDotaScenario.EntityRef
        duration: float
        lifetime_remaining: float
        stack_count: int
        create_even_if_existing: bool
        create_without_caster: bool
        create_without_ability: bool
        moonshard_consumed_bonus: int
        moonshard_consumed_bonus_night_vision: int
        wardtruesight_range: int
        ultimate_scepter_consumed_alchemist_bonus_all_stats: int
        ultimate_scepter_consumed_alchemist_bonus_health: int
        ultimate_scepter_consumed_alchemist_bonus_mana: int
        def __init__(
            self,
            name: str | None = ...,
            parent: CMsgDotaScenario.EntityRef | _Mapping | None = ...,
            caster: CMsgDotaScenario.EntityRef | _Mapping | None = ...,
            ability: CMsgDotaScenario.EntityRef | _Mapping | None = ...,
            duration: float | None = ...,
            lifetime_remaining: float | None = ...,
            stack_count: int | None = ...,
            create_even_if_existing: bool = ...,
            create_without_caster: bool = ...,
            create_without_ability: bool = ...,
            moonshard_consumed_bonus: int | None = ...,
            moonshard_consumed_bonus_night_vision: int | None = ...,
            wardtruesight_range: int | None = ...,
            ultimate_scepter_consumed_alchemist_bonus_all_stats: int | None = ...,
            ultimate_scepter_consumed_alchemist_bonus_health: int | None = ...,
            ultimate_scepter_consumed_alchemist_bonus_mana: int | None = ...,
        ) -> None: ...

    LOBBY_ID_FIELD_NUMBER: _ClassVar[int]
    GAME_FIELD_NUMBER: _ClassVar[int]
    TEAMS_FIELD_NUMBER: _ClassVar[int]
    HEROES_FIELD_NUMBER: _ClassVar[int]
    STOCK_FIELD_NUMBER: _ClassVar[int]
    BUILDINGS_FIELD_NUMBER: _ClassVar[int]
    ENTITIES_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    MODIFIERS_FIELD_NUMBER: _ClassVar[int]
    lobby_id: int
    game: CMsgDotaScenario.Game
    teams: _containers.RepeatedCompositeFieldContainer[CMsgDotaScenario.Team]
    heroes: _containers.RepeatedCompositeFieldContainer[CMsgDotaScenario.Hero]
    stock: _containers.RepeatedCompositeFieldContainer[CMsgDotaScenario.Stock]
    buildings: _containers.RepeatedCompositeFieldContainer[CMsgDotaScenario.Building]
    entities: _containers.RepeatedCompositeFieldContainer[CMsgDotaScenario.Entity]
    items: _containers.RepeatedCompositeFieldContainer[CMsgDotaScenario.Item]
    modifiers: _containers.RepeatedCompositeFieldContainer[CMsgDotaScenario.Modifier]
    def __init__(
        self,
        lobby_id: int | None = ...,
        game: CMsgDotaScenario.Game | _Mapping | None = ...,
        teams: _Iterable[CMsgDotaScenario.Team | _Mapping] | None = ...,
        heroes: _Iterable[CMsgDotaScenario.Hero | _Mapping] | None = ...,
        stock: _Iterable[CMsgDotaScenario.Stock | _Mapping] | None = ...,
        buildings: _Iterable[CMsgDotaScenario.Building | _Mapping] | None = ...,
        entities: _Iterable[CMsgDotaScenario.Entity | _Mapping] | None = ...,
        items: _Iterable[CMsgDotaScenario.Item | _Mapping] | None = ...,
        modifiers: _Iterable[CMsgDotaScenario.Modifier | _Mapping] | None = ...,
    ) -> None: ...
