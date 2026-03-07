from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class CMsgBattleReport_HighlightType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eHighlightTypeInvalid: _ClassVar[CMsgBattleReport_HighlightType]
    k_eGameWinrate: _ClassVar[CMsgBattleReport_HighlightType]
    k_eLaneWinrate: _ClassVar[CMsgBattleReport_HighlightType]
    k_eMMRDelta: _ClassVar[CMsgBattleReport_HighlightType]
    k_eNumHeroesPlayed: _ClassVar[CMsgBattleReport_HighlightType]
    k_eNumGamesPlayed: _ClassVar[CMsgBattleReport_HighlightType]
    k_eAveragePowerRunesTaken: _ClassVar[CMsgBattleReport_HighlightType]
    k_eAverageBountyRunesTaken: _ClassVar[CMsgBattleReport_HighlightType]
    k_eTotalKillEnemyT1First: _ClassVar[CMsgBattleReport_HighlightType]
    k_eTotalRoshanKills: _ClassVar[CMsgBattleReport_HighlightType]
    k_eTotalDewards: _ClassVar[CMsgBattleReport_HighlightType]
    k_eTotalCampsStacked: _ClassVar[CMsgBattleReport_HighlightType]
    k_eMaxWinstreak: _ClassVar[CMsgBattleReport_HighlightType]
    k_eAverageDewards: _ClassVar[CMsgBattleReport_HighlightType]
    k_eAverageKills: _ClassVar[CMsgBattleReport_HighlightType]
    k_eMaxKills: _ClassVar[CMsgBattleReport_HighlightType]
    k_eAverageAssists: _ClassVar[CMsgBattleReport_HighlightType]
    k_eMaxAssists: _ClassVar[CMsgBattleReport_HighlightType]
    k_eAverageDeaths: _ClassVar[CMsgBattleReport_HighlightType]
    k_eMinDeaths: _ClassVar[CMsgBattleReport_HighlightType]
    k_eAverageCampsStacked: _ClassVar[CMsgBattleReport_HighlightType]
    k_eTotalLastHits: _ClassVar[CMsgBattleReport_HighlightType]
    k_eAverageLastHits: _ClassVar[CMsgBattleReport_HighlightType]
    k_eTotalDenies: _ClassVar[CMsgBattleReport_HighlightType]
    k_eAverageDenies: _ClassVar[CMsgBattleReport_HighlightType]
    k_eTotalGamesWithRoshanAdvantage: _ClassVar[CMsgBattleReport_HighlightType]
    k_ePercentGamesWithRoshanAdvantage: _ClassVar[CMsgBattleReport_HighlightType]
    k_eAverageStunDuration: _ClassVar[CMsgBattleReport_HighlightType]
    k_eTotalStunDuration: _ClassVar[CMsgBattleReport_HighlightType]
    k_eAverageTeleportsUsed: _ClassVar[CMsgBattleReport_HighlightType]
    k_eTotalTeleportsUsed: _ClassVar[CMsgBattleReport_HighlightType]
    k_eAverageHeroDamage: _ClassVar[CMsgBattleReport_HighlightType]
    k_eTotalHeroDamage: _ClassVar[CMsgBattleReport_HighlightType]
    k_eAverageHeroHealing: _ClassVar[CMsgBattleReport_HighlightType]
    k_eTotalHeroHealing: _ClassVar[CMsgBattleReport_HighlightType]
    k_eAverageTowerDamage: _ClassVar[CMsgBattleReport_HighlightType]
    k_eTotalTowerDamage: _ClassVar[CMsgBattleReport_HighlightType]
    k_eMaxLossStreak: _ClassVar[CMsgBattleReport_HighlightType]
    k_eAverageGameDuration: _ClassVar[CMsgBattleReport_HighlightType]
    k_eMaxGameDuration: _ClassVar[CMsgBattleReport_HighlightType]
    k_eMinGameDuration: _ClassVar[CMsgBattleReport_HighlightType]
    k_eAverageWinDuration: _ClassVar[CMsgBattleReport_HighlightType]
    k_eMaxWinDuration: _ClassVar[CMsgBattleReport_HighlightType]
    k_eMinWinDuration: _ClassVar[CMsgBattleReport_HighlightType]
    k_eAverageLossDuration: _ClassVar[CMsgBattleReport_HighlightType]
    k_eMaxLossDuration: _ClassVar[CMsgBattleReport_HighlightType]
    k_eMinLossDuration: _ClassVar[CMsgBattleReport_HighlightType]
    k_ePctGamesEnemyT1TakenFirst: _ClassVar[CMsgBattleReport_HighlightType]
    k_eMaxCampsStacked: _ClassVar[CMsgBattleReport_HighlightType]
    k_eMaxDewards: _ClassVar[CMsgBattleReport_HighlightType]
    k_eMaxRoshanKills: _ClassVar[CMsgBattleReport_HighlightType]
    k_eMaxBountyRunesTaken: _ClassVar[CMsgBattleReport_HighlightType]
    k_eMaxPowerRunesTaken: _ClassVar[CMsgBattleReport_HighlightType]
    k_eMaxDeaths: _ClassVar[CMsgBattleReport_HighlightType]
    k_eMaxLastHits: _ClassVar[CMsgBattleReport_HighlightType]
    k_eMaxDenies: _ClassVar[CMsgBattleReport_HighlightType]
    k_eRadiantWinRate: _ClassVar[CMsgBattleReport_HighlightType]
    k_eDireWinRate: _ClassVar[CMsgBattleReport_HighlightType]
    k_eRadiantGameCount: _ClassVar[CMsgBattleReport_HighlightType]
    k_eDireGameCount: _ClassVar[CMsgBattleReport_HighlightType]
    k_eMaxDamage: _ClassVar[CMsgBattleReport_HighlightType]
    k_eMaxHealing: _ClassVar[CMsgBattleReport_HighlightType]
    k_eMaxTowerDamage: _ClassVar[CMsgBattleReport_HighlightType]
    k_eAverageGPM: _ClassVar[CMsgBattleReport_HighlightType]
    k_eMaxGPM: _ClassVar[CMsgBattleReport_HighlightType]
    k_eAverageXPM: _ClassVar[CMsgBattleReport_HighlightType]
    k_eMaxXPM: _ClassVar[CMsgBattleReport_HighlightType]

class CMsgBattleReport_HighlightCategory(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eHighlightGeneral: _ClassVar[CMsgBattleReport_HighlightCategory]
    k_eHighlightHero: _ClassVar[CMsgBattleReport_HighlightCategory]
    k_eHighlightRole: _ClassVar[CMsgBattleReport_HighlightCategory]

class CMsgBattleReport_Role(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eUnknownRole: _ClassVar[CMsgBattleReport_Role]
    k_eSafelane: _ClassVar[CMsgBattleReport_Role]
    k_eMidlane: _ClassVar[CMsgBattleReport_Role]
    k_eOfflane: _ClassVar[CMsgBattleReport_Role]
    k_eSupport: _ClassVar[CMsgBattleReport_Role]
    k_eHardSupport: _ClassVar[CMsgBattleReport_Role]

class CMsgBattleReport_CompareContext(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eCompareContextInvalid: _ClassVar[CMsgBattleReport_CompareContext]
    k_eAbsoluteValue: _ClassVar[CMsgBattleReport_CompareContext]
    k_ePlayersOfSimilarRank: _ClassVar[CMsgBattleReport_CompareContext]
    k_eAllPlayers: _ClassVar[CMsgBattleReport_CompareContext]
    k_ePlayersPersonalHistory: _ClassVar[CMsgBattleReport_CompareContext]

class CMsgBattleReport_HighlightTier(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eHighlightTierLow: _ClassVar[CMsgBattleReport_HighlightTier]
    k_eHighlightTierNone: _ClassVar[CMsgBattleReport_HighlightTier]
    k_eHighlightTier1: _ClassVar[CMsgBattleReport_HighlightTier]
    k_eHighlightTier2: _ClassVar[CMsgBattleReport_HighlightTier]
    k_eHighlightTier3: _ClassVar[CMsgBattleReport_HighlightTier]
    k_eHighlightTierCustom: _ClassVar[CMsgBattleReport_HighlightTier]

class CMsgBattleReport_HighlightRarity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eHighlightCommon: _ClassVar[CMsgBattleReport_HighlightRarity]
    k_eHighlightUncommon: _ClassVar[CMsgBattleReport_HighlightRarity]
    k_eHighlightRare: _ClassVar[CMsgBattleReport_HighlightRarity]

class CMsgBattleReport_EOutcome(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eWin: _ClassVar[CMsgBattleReport_EOutcome]
    k_eLoss: _ClassVar[CMsgBattleReport_EOutcome]

class CMsgBattleReport_ELaneOutcome(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_eUnknownLaneOutcome: _ClassVar[CMsgBattleReport_ELaneOutcome]
    k_eWonLane: _ClassVar[CMsgBattleReport_ELaneOutcome]
    k_eLostLane: _ClassVar[CMsgBattleReport_ELaneOutcome]
    k_eEvenLane: _ClassVar[CMsgBattleReport_ELaneOutcome]

k_eHighlightTypeInvalid: CMsgBattleReport_HighlightType
k_eGameWinrate: CMsgBattleReport_HighlightType
k_eLaneWinrate: CMsgBattleReport_HighlightType
k_eMMRDelta: CMsgBattleReport_HighlightType
k_eNumHeroesPlayed: CMsgBattleReport_HighlightType
k_eNumGamesPlayed: CMsgBattleReport_HighlightType
k_eAveragePowerRunesTaken: CMsgBattleReport_HighlightType
k_eAverageBountyRunesTaken: CMsgBattleReport_HighlightType
k_eTotalKillEnemyT1First: CMsgBattleReport_HighlightType
k_eTotalRoshanKills: CMsgBattleReport_HighlightType
k_eTotalDewards: CMsgBattleReport_HighlightType
k_eTotalCampsStacked: CMsgBattleReport_HighlightType
k_eMaxWinstreak: CMsgBattleReport_HighlightType
k_eAverageDewards: CMsgBattleReport_HighlightType
k_eAverageKills: CMsgBattleReport_HighlightType
k_eMaxKills: CMsgBattleReport_HighlightType
k_eAverageAssists: CMsgBattleReport_HighlightType
k_eMaxAssists: CMsgBattleReport_HighlightType
k_eAverageDeaths: CMsgBattleReport_HighlightType
k_eMinDeaths: CMsgBattleReport_HighlightType
k_eAverageCampsStacked: CMsgBattleReport_HighlightType
k_eTotalLastHits: CMsgBattleReport_HighlightType
k_eAverageLastHits: CMsgBattleReport_HighlightType
k_eTotalDenies: CMsgBattleReport_HighlightType
k_eAverageDenies: CMsgBattleReport_HighlightType
k_eTotalGamesWithRoshanAdvantage: CMsgBattleReport_HighlightType
k_ePercentGamesWithRoshanAdvantage: CMsgBattleReport_HighlightType
k_eAverageStunDuration: CMsgBattleReport_HighlightType
k_eTotalStunDuration: CMsgBattleReport_HighlightType
k_eAverageTeleportsUsed: CMsgBattleReport_HighlightType
k_eTotalTeleportsUsed: CMsgBattleReport_HighlightType
k_eAverageHeroDamage: CMsgBattleReport_HighlightType
k_eTotalHeroDamage: CMsgBattleReport_HighlightType
k_eAverageHeroHealing: CMsgBattleReport_HighlightType
k_eTotalHeroHealing: CMsgBattleReport_HighlightType
k_eAverageTowerDamage: CMsgBattleReport_HighlightType
k_eTotalTowerDamage: CMsgBattleReport_HighlightType
k_eMaxLossStreak: CMsgBattleReport_HighlightType
k_eAverageGameDuration: CMsgBattleReport_HighlightType
k_eMaxGameDuration: CMsgBattleReport_HighlightType
k_eMinGameDuration: CMsgBattleReport_HighlightType
k_eAverageWinDuration: CMsgBattleReport_HighlightType
k_eMaxWinDuration: CMsgBattleReport_HighlightType
k_eMinWinDuration: CMsgBattleReport_HighlightType
k_eAverageLossDuration: CMsgBattleReport_HighlightType
k_eMaxLossDuration: CMsgBattleReport_HighlightType
k_eMinLossDuration: CMsgBattleReport_HighlightType
k_ePctGamesEnemyT1TakenFirst: CMsgBattleReport_HighlightType
k_eMaxCampsStacked: CMsgBattleReport_HighlightType
k_eMaxDewards: CMsgBattleReport_HighlightType
k_eMaxRoshanKills: CMsgBattleReport_HighlightType
k_eMaxBountyRunesTaken: CMsgBattleReport_HighlightType
k_eMaxPowerRunesTaken: CMsgBattleReport_HighlightType
k_eMaxDeaths: CMsgBattleReport_HighlightType
k_eMaxLastHits: CMsgBattleReport_HighlightType
k_eMaxDenies: CMsgBattleReport_HighlightType
k_eRadiantWinRate: CMsgBattleReport_HighlightType
k_eDireWinRate: CMsgBattleReport_HighlightType
k_eRadiantGameCount: CMsgBattleReport_HighlightType
k_eDireGameCount: CMsgBattleReport_HighlightType
k_eMaxDamage: CMsgBattleReport_HighlightType
k_eMaxHealing: CMsgBattleReport_HighlightType
k_eMaxTowerDamage: CMsgBattleReport_HighlightType
k_eAverageGPM: CMsgBattleReport_HighlightType
k_eMaxGPM: CMsgBattleReport_HighlightType
k_eAverageXPM: CMsgBattleReport_HighlightType
k_eMaxXPM: CMsgBattleReport_HighlightType
k_eHighlightGeneral: CMsgBattleReport_HighlightCategory
k_eHighlightHero: CMsgBattleReport_HighlightCategory
k_eHighlightRole: CMsgBattleReport_HighlightCategory
k_eUnknownRole: CMsgBattleReport_Role
k_eSafelane: CMsgBattleReport_Role
k_eMidlane: CMsgBattleReport_Role
k_eOfflane: CMsgBattleReport_Role
k_eSupport: CMsgBattleReport_Role
k_eHardSupport: CMsgBattleReport_Role
k_eCompareContextInvalid: CMsgBattleReport_CompareContext
k_eAbsoluteValue: CMsgBattleReport_CompareContext
k_ePlayersOfSimilarRank: CMsgBattleReport_CompareContext
k_eAllPlayers: CMsgBattleReport_CompareContext
k_ePlayersPersonalHistory: CMsgBattleReport_CompareContext
k_eHighlightTierLow: CMsgBattleReport_HighlightTier
k_eHighlightTierNone: CMsgBattleReport_HighlightTier
k_eHighlightTier1: CMsgBattleReport_HighlightTier
k_eHighlightTier2: CMsgBattleReport_HighlightTier
k_eHighlightTier3: CMsgBattleReport_HighlightTier
k_eHighlightTierCustom: CMsgBattleReport_HighlightTier
k_eHighlightCommon: CMsgBattleReport_HighlightRarity
k_eHighlightUncommon: CMsgBattleReport_HighlightRarity
k_eHighlightRare: CMsgBattleReport_HighlightRarity
k_eWin: CMsgBattleReport_EOutcome
k_eLoss: CMsgBattleReport_EOutcome
k_eUnknownLaneOutcome: CMsgBattleReport_ELaneOutcome
k_eWonLane: CMsgBattleReport_ELaneOutcome
k_eLostLane: CMsgBattleReport_ELaneOutcome
k_eEvenLane: CMsgBattleReport_ELaneOutcome

class CMsgClientToGCGetBattleReport(_message.Message):
    __slots__ = ("account_id", "timestamp", "duration")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    timestamp: int
    duration: int
    def __init__(
        self, account_id: int | None = ..., timestamp: int | None = ..., duration: int | None = ...
    ) -> None: ...

class CMsgBattleReport_Game(_message.Message):
    __slots__ = (
        "hero_id",
        "kills",
        "deaths",
        "assists",
        "rank_change",
        "last_hits",
        "denies",
        "gpm",
        "xpm",
        "role",
        "outcome",
        "lane_outcome",
        "ranked",
        "match_id",
        "lane_selection_flags",
        "predicted_position",
        "seconds_dead",
        "winning_team",
        "player_slot",
        "party_game",
        "start_time",
        "bounty_runes",
        "water_runes",
        "power_runes",
        "time_enemy_t1_tower_destroyed",
        "time_friendly_t1_tower_destroyed",
        "enemy_roshan_kills",
        "teleports_used",
        "dewards",
        "camps_stacked",
        "support_gold",
        "hero_damage",
        "hero_healing",
        "tower_damage",
        "successful_smokes",
        "stun_duration",
        "duration",
        "friendly_roshan_kills",
        "previous_rank",
        "game_mode",
        "lobby_type",
        "time_purchased_shard",
        "time_purchased_scepter",
        "item0",
        "item1",
        "item2",
        "item3",
        "item4",
        "item5",
        "selected_facet",
    )
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    KILLS_FIELD_NUMBER: _ClassVar[int]
    DEATHS_FIELD_NUMBER: _ClassVar[int]
    ASSISTS_FIELD_NUMBER: _ClassVar[int]
    RANK_CHANGE_FIELD_NUMBER: _ClassVar[int]
    LAST_HITS_FIELD_NUMBER: _ClassVar[int]
    DENIES_FIELD_NUMBER: _ClassVar[int]
    GPM_FIELD_NUMBER: _ClassVar[int]
    XPM_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    OUTCOME_FIELD_NUMBER: _ClassVar[int]
    LANE_OUTCOME_FIELD_NUMBER: _ClassVar[int]
    RANKED_FIELD_NUMBER: _ClassVar[int]
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    LANE_SELECTION_FLAGS_FIELD_NUMBER: _ClassVar[int]
    PREDICTED_POSITION_FIELD_NUMBER: _ClassVar[int]
    SECONDS_DEAD_FIELD_NUMBER: _ClassVar[int]
    WINNING_TEAM_FIELD_NUMBER: _ClassVar[int]
    PLAYER_SLOT_FIELD_NUMBER: _ClassVar[int]
    PARTY_GAME_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    BOUNTY_RUNES_FIELD_NUMBER: _ClassVar[int]
    WATER_RUNES_FIELD_NUMBER: _ClassVar[int]
    POWER_RUNES_FIELD_NUMBER: _ClassVar[int]
    TIME_ENEMY_T1_TOWER_DESTROYED_FIELD_NUMBER: _ClassVar[int]
    TIME_FRIENDLY_T1_TOWER_DESTROYED_FIELD_NUMBER: _ClassVar[int]
    ENEMY_ROSHAN_KILLS_FIELD_NUMBER: _ClassVar[int]
    TELEPORTS_USED_FIELD_NUMBER: _ClassVar[int]
    DEWARDS_FIELD_NUMBER: _ClassVar[int]
    CAMPS_STACKED_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_GOLD_FIELD_NUMBER: _ClassVar[int]
    HERO_DAMAGE_FIELD_NUMBER: _ClassVar[int]
    HERO_HEALING_FIELD_NUMBER: _ClassVar[int]
    TOWER_DAMAGE_FIELD_NUMBER: _ClassVar[int]
    SUCCESSFUL_SMOKES_FIELD_NUMBER: _ClassVar[int]
    STUN_DURATION_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    FRIENDLY_ROSHAN_KILLS_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_RANK_FIELD_NUMBER: _ClassVar[int]
    GAME_MODE_FIELD_NUMBER: _ClassVar[int]
    LOBBY_TYPE_FIELD_NUMBER: _ClassVar[int]
    TIME_PURCHASED_SHARD_FIELD_NUMBER: _ClassVar[int]
    TIME_PURCHASED_SCEPTER_FIELD_NUMBER: _ClassVar[int]
    ITEM0_FIELD_NUMBER: _ClassVar[int]
    ITEM1_FIELD_NUMBER: _ClassVar[int]
    ITEM2_FIELD_NUMBER: _ClassVar[int]
    ITEM3_FIELD_NUMBER: _ClassVar[int]
    ITEM4_FIELD_NUMBER: _ClassVar[int]
    ITEM5_FIELD_NUMBER: _ClassVar[int]
    SELECTED_FACET_FIELD_NUMBER: _ClassVar[int]
    hero_id: int
    kills: int
    deaths: int
    assists: int
    rank_change: int
    last_hits: int
    denies: int
    gpm: int
    xpm: int
    role: CMsgBattleReport_Role
    outcome: CMsgBattleReport_EOutcome
    lane_outcome: CMsgBattleReport_ELaneOutcome
    ranked: bool
    match_id: int
    lane_selection_flags: int
    predicted_position: int
    seconds_dead: int
    winning_team: int
    player_slot: int
    party_game: bool
    start_time: int
    bounty_runes: int
    water_runes: int
    power_runes: int
    time_enemy_t1_tower_destroyed: int
    time_friendly_t1_tower_destroyed: int
    enemy_roshan_kills: int
    teleports_used: int
    dewards: int
    camps_stacked: int
    support_gold: int
    hero_damage: int
    hero_healing: int
    tower_damage: int
    successful_smokes: int
    stun_duration: int
    duration: int
    friendly_roshan_kills: int
    previous_rank: int
    game_mode: int
    lobby_type: int
    time_purchased_shard: float
    time_purchased_scepter: float
    item0: int
    item1: int
    item2: int
    item3: int
    item4: int
    item5: int
    selected_facet: int
    def __init__(
        self,
        hero_id: int | None = ...,
        kills: int | None = ...,
        deaths: int | None = ...,
        assists: int | None = ...,
        rank_change: int | None = ...,
        last_hits: int | None = ...,
        denies: int | None = ...,
        gpm: int | None = ...,
        xpm: int | None = ...,
        role: CMsgBattleReport_Role | str | None = ...,
        outcome: CMsgBattleReport_EOutcome | str | None = ...,
        lane_outcome: CMsgBattleReport_ELaneOutcome | str | None = ...,
        ranked: bool = ...,
        match_id: int | None = ...,
        lane_selection_flags: int | None = ...,
        predicted_position: int | None = ...,
        seconds_dead: int | None = ...,
        winning_team: int | None = ...,
        player_slot: int | None = ...,
        party_game: bool = ...,
        start_time: int | None = ...,
        bounty_runes: int | None = ...,
        water_runes: int | None = ...,
        power_runes: int | None = ...,
        time_enemy_t1_tower_destroyed: int | None = ...,
        time_friendly_t1_tower_destroyed: int | None = ...,
        enemy_roshan_kills: int | None = ...,
        teleports_used: int | None = ...,
        dewards: int | None = ...,
        camps_stacked: int | None = ...,
        support_gold: int | None = ...,
        hero_damage: int | None = ...,
        hero_healing: int | None = ...,
        tower_damage: int | None = ...,
        successful_smokes: int | None = ...,
        stun_duration: int | None = ...,
        duration: int | None = ...,
        friendly_roshan_kills: int | None = ...,
        previous_rank: int | None = ...,
        game_mode: int | None = ...,
        lobby_type: int | None = ...,
        time_purchased_shard: float | None = ...,
        time_purchased_scepter: float | None = ...,
        item0: int | None = ...,
        item1: int | None = ...,
        item2: int | None = ...,
        item3: int | None = ...,
        item4: int | None = ...,
        item5: int | None = ...,
        selected_facet: int | None = ...,
    ) -> None: ...

class CMsgBattleReport_GameList(_message.Message):
    __slots__ = ("games",)
    GAMES_FIELD_NUMBER: _ClassVar[int]
    games: _containers.RepeatedCompositeFieldContainer[CMsgBattleReport_Game]
    def __init__(self, games: _Iterable[CMsgBattleReport_Game | _Mapping] | None = ...) -> None: ...

class CMsgBattleReport(_message.Message):
    __slots__ = ("games", "highlights")
    class HighlightGeneral(_message.Message):
        __slots__ = ("win_loss_window", "win_percent", "mmr_delta", "highlight_score")
        WIN_LOSS_WINDOW_FIELD_NUMBER: _ClassVar[int]
        WIN_PERCENT_FIELD_NUMBER: _ClassVar[int]
        MMR_DELTA_FIELD_NUMBER: _ClassVar[int]
        HIGHLIGHT_SCORE_FIELD_NUMBER: _ClassVar[int]
        win_loss_window: int
        win_percent: float
        mmr_delta: int
        highlight_score: float
        def __init__(
            self,
            win_loss_window: int | None = ...,
            win_percent: float | None = ...,
            mmr_delta: int | None = ...,
            highlight_score: float | None = ...,
        ) -> None: ...

    class Highlight(_message.Message):
        __slots__ = (
            "highlight_id",
            "category",
            "tier",
            "rarity",
            "score",
            "confidence",
            "hero_id",
            "role",
            "comparison_delta_value",
            "context",
        )
        HIGHLIGHT_ID_FIELD_NUMBER: _ClassVar[int]
        CATEGORY_FIELD_NUMBER: _ClassVar[int]
        TIER_FIELD_NUMBER: _ClassVar[int]
        RARITY_FIELD_NUMBER: _ClassVar[int]
        SCORE_FIELD_NUMBER: _ClassVar[int]
        CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        ROLE_FIELD_NUMBER: _ClassVar[int]
        COMPARISON_DELTA_VALUE_FIELD_NUMBER: _ClassVar[int]
        CONTEXT_FIELD_NUMBER: _ClassVar[int]
        highlight_id: int
        category: CMsgBattleReport_HighlightCategory
        tier: CMsgBattleReport_HighlightTier
        rarity: CMsgBattleReport_HighlightRarity
        score: float
        confidence: float
        hero_id: int
        role: CMsgBattleReport_Role
        comparison_delta_value: float
        context: CMsgBattleReport_CompareContext
        def __init__(
            self,
            highlight_id: int | None = ...,
            category: CMsgBattleReport_HighlightCategory | str | None = ...,
            tier: CMsgBattleReport_HighlightTier | str | None = ...,
            rarity: CMsgBattleReport_HighlightRarity | str | None = ...,
            score: float | None = ...,
            confidence: float | None = ...,
            hero_id: int | None = ...,
            role: CMsgBattleReport_Role | str | None = ...,
            comparison_delta_value: float | None = ...,
            context: CMsgBattleReport_CompareContext | str | None = ...,
        ) -> None: ...

    GAMES_FIELD_NUMBER: _ClassVar[int]
    HIGHLIGHTS_FIELD_NUMBER: _ClassVar[int]
    games: _containers.RepeatedCompositeFieldContainer[CMsgBattleReport_Game]
    highlights: CMsgBattleReportHighlights
    def __init__(
        self,
        games: _Iterable[CMsgBattleReport_Game | _Mapping] | None = ...,
        highlights: CMsgBattleReportHighlights | _Mapping | None = ...,
    ) -> None: ...

class CMsgBattleReportInfo(_message.Message):
    __slots__ = (
        "timestamp",
        "duration",
        "acknowledged",
        "featured_hero_id",
        "featured_position",
        "games_played",
        "medal_counts",
    )
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    ACKNOWLEDGED_FIELD_NUMBER: _ClassVar[int]
    FEATURED_HERO_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURED_POSITION_FIELD_NUMBER: _ClassVar[int]
    GAMES_PLAYED_FIELD_NUMBER: _ClassVar[int]
    MEDAL_COUNTS_FIELD_NUMBER: _ClassVar[int]
    timestamp: int
    duration: int
    acknowledged: bool
    featured_hero_id: int
    featured_position: int
    games_played: int
    medal_counts: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        timestamp: int | None = ...,
        duration: int | None = ...,
        acknowledged: bool = ...,
        featured_hero_id: int | None = ...,
        featured_position: int | None = ...,
        games_played: int | None = ...,
        medal_counts: _Iterable[int] | None = ...,
    ) -> None: ...

class CMsgBattleReportInfoList(_message.Message):
    __slots__ = ("battle_report_info",)
    BATTLE_REPORT_INFO_FIELD_NUMBER: _ClassVar[int]
    battle_report_info: _containers.RepeatedCompositeFieldContainer[CMsgBattleReportInfo]
    def __init__(
        self, battle_report_info: _Iterable[CMsgBattleReportInfo | _Mapping] | None = ...
    ) -> None: ...

class CMsgBattleReportHighlights(_message.Message):
    __slots__ = ("highlights",)
    HIGHLIGHTS_FIELD_NUMBER: _ClassVar[int]
    highlights: _containers.RepeatedCompositeFieldContainer[CMsgBattleReport.Highlight]
    def __init__(
        self, highlights: _Iterable[CMsgBattleReport.Highlight | _Mapping] | None = ...
    ) -> None: ...

class CMsgBattleReportAggregateStats(_message.Message):
    __slots__ = ("result",)
    class CMsgBattleReportStat(_message.Message):
        __slots__ = ("mean", "stdev")
        MEAN_FIELD_NUMBER: _ClassVar[int]
        STDEV_FIELD_NUMBER: _ClassVar[int]
        mean: float
        stdev: float
        def __init__(self, mean: float | None = ..., stdev: float | None = ...) -> None: ...

    class CMsgBattleReportAggregate(_message.Message):
        __slots__ = (
            "hero_id",
            "predicted_position",
            "game_count",
            "win_count",
            "lane_win_count",
            "kills",
            "deaths",
            "assists",
            "rank_change",
            "last_hits",
            "denies",
            "gpm",
            "xpm",
            "seconds_dead",
            "bounty_runes",
            "water_runes",
            "power_runes",
            "time_enemy_t1_tower_destroyed",
            "time_friendly_t1_tower_destroyed",
            "enemy_roshan_kills",
            "teleports_used",
            "dewards",
            "camps_stacked",
            "support_gold",
            "hero_damage",
            "hero_healing",
            "tower_damage",
            "successful_smokes",
            "stun_duration",
            "duration",
            "friendly_roshan_kills",
        )
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        PREDICTED_POSITION_FIELD_NUMBER: _ClassVar[int]
        GAME_COUNT_FIELD_NUMBER: _ClassVar[int]
        WIN_COUNT_FIELD_NUMBER: _ClassVar[int]
        LANE_WIN_COUNT_FIELD_NUMBER: _ClassVar[int]
        KILLS_FIELD_NUMBER: _ClassVar[int]
        DEATHS_FIELD_NUMBER: _ClassVar[int]
        ASSISTS_FIELD_NUMBER: _ClassVar[int]
        RANK_CHANGE_FIELD_NUMBER: _ClassVar[int]
        LAST_HITS_FIELD_NUMBER: _ClassVar[int]
        DENIES_FIELD_NUMBER: _ClassVar[int]
        GPM_FIELD_NUMBER: _ClassVar[int]
        XPM_FIELD_NUMBER: _ClassVar[int]
        SECONDS_DEAD_FIELD_NUMBER: _ClassVar[int]
        BOUNTY_RUNES_FIELD_NUMBER: _ClassVar[int]
        WATER_RUNES_FIELD_NUMBER: _ClassVar[int]
        POWER_RUNES_FIELD_NUMBER: _ClassVar[int]
        TIME_ENEMY_T1_TOWER_DESTROYED_FIELD_NUMBER: _ClassVar[int]
        TIME_FRIENDLY_T1_TOWER_DESTROYED_FIELD_NUMBER: _ClassVar[int]
        ENEMY_ROSHAN_KILLS_FIELD_NUMBER: _ClassVar[int]
        TELEPORTS_USED_FIELD_NUMBER: _ClassVar[int]
        DEWARDS_FIELD_NUMBER: _ClassVar[int]
        CAMPS_STACKED_FIELD_NUMBER: _ClassVar[int]
        SUPPORT_GOLD_FIELD_NUMBER: _ClassVar[int]
        HERO_DAMAGE_FIELD_NUMBER: _ClassVar[int]
        HERO_HEALING_FIELD_NUMBER: _ClassVar[int]
        TOWER_DAMAGE_FIELD_NUMBER: _ClassVar[int]
        SUCCESSFUL_SMOKES_FIELD_NUMBER: _ClassVar[int]
        STUN_DURATION_FIELD_NUMBER: _ClassVar[int]
        DURATION_FIELD_NUMBER: _ClassVar[int]
        FRIENDLY_ROSHAN_KILLS_FIELD_NUMBER: _ClassVar[int]
        hero_id: int
        predicted_position: int
        game_count: int
        win_count: int
        lane_win_count: int
        kills: CMsgBattleReportAggregateStats.CMsgBattleReportStat
        deaths: CMsgBattleReportAggregateStats.CMsgBattleReportStat
        assists: CMsgBattleReportAggregateStats.CMsgBattleReportStat
        rank_change: CMsgBattleReportAggregateStats.CMsgBattleReportStat
        last_hits: CMsgBattleReportAggregateStats.CMsgBattleReportStat
        denies: CMsgBattleReportAggregateStats.CMsgBattleReportStat
        gpm: CMsgBattleReportAggregateStats.CMsgBattleReportStat
        xpm: CMsgBattleReportAggregateStats.CMsgBattleReportStat
        seconds_dead: CMsgBattleReportAggregateStats.CMsgBattleReportStat
        bounty_runes: CMsgBattleReportAggregateStats.CMsgBattleReportStat
        water_runes: CMsgBattleReportAggregateStats.CMsgBattleReportStat
        power_runes: CMsgBattleReportAggregateStats.CMsgBattleReportStat
        time_enemy_t1_tower_destroyed: CMsgBattleReportAggregateStats.CMsgBattleReportStat
        time_friendly_t1_tower_destroyed: CMsgBattleReportAggregateStats.CMsgBattleReportStat
        enemy_roshan_kills: CMsgBattleReportAggregateStats.CMsgBattleReportStat
        teleports_used: CMsgBattleReportAggregateStats.CMsgBattleReportStat
        dewards: CMsgBattleReportAggregateStats.CMsgBattleReportStat
        camps_stacked: CMsgBattleReportAggregateStats.CMsgBattleReportStat
        support_gold: CMsgBattleReportAggregateStats.CMsgBattleReportStat
        hero_damage: CMsgBattleReportAggregateStats.CMsgBattleReportStat
        hero_healing: CMsgBattleReportAggregateStats.CMsgBattleReportStat
        tower_damage: CMsgBattleReportAggregateStats.CMsgBattleReportStat
        successful_smokes: CMsgBattleReportAggregateStats.CMsgBattleReportStat
        stun_duration: CMsgBattleReportAggregateStats.CMsgBattleReportStat
        duration: CMsgBattleReportAggregateStats.CMsgBattleReportStat
        friendly_roshan_kills: CMsgBattleReportAggregateStats.CMsgBattleReportStat
        def __init__(
            self,
            hero_id: int | None = ...,
            predicted_position: int | None = ...,
            game_count: int | None = ...,
            win_count: int | None = ...,
            lane_win_count: int | None = ...,
            kills: CMsgBattleReportAggregateStats.CMsgBattleReportStat | _Mapping | None = ...,
            deaths: CMsgBattleReportAggregateStats.CMsgBattleReportStat | _Mapping | None = ...,
            assists: CMsgBattleReportAggregateStats.CMsgBattleReportStat | _Mapping | None = ...,
            rank_change: CMsgBattleReportAggregateStats.CMsgBattleReportStat
            | _Mapping
            | None = ...,
            last_hits: CMsgBattleReportAggregateStats.CMsgBattleReportStat | _Mapping | None = ...,
            denies: CMsgBattleReportAggregateStats.CMsgBattleReportStat | _Mapping | None = ...,
            gpm: CMsgBattleReportAggregateStats.CMsgBattleReportStat | _Mapping | None = ...,
            xpm: CMsgBattleReportAggregateStats.CMsgBattleReportStat | _Mapping | None = ...,
            seconds_dead: CMsgBattleReportAggregateStats.CMsgBattleReportStat
            | _Mapping
            | None = ...,
            bounty_runes: CMsgBattleReportAggregateStats.CMsgBattleReportStat
            | _Mapping
            | None = ...,
            water_runes: CMsgBattleReportAggregateStats.CMsgBattleReportStat
            | _Mapping
            | None = ...,
            power_runes: CMsgBattleReportAggregateStats.CMsgBattleReportStat
            | _Mapping
            | None = ...,
            time_enemy_t1_tower_destroyed: CMsgBattleReportAggregateStats.CMsgBattleReportStat
            | _Mapping
            | None = ...,
            time_friendly_t1_tower_destroyed: CMsgBattleReportAggregateStats.CMsgBattleReportStat
            | _Mapping
            | None = ...,
            enemy_roshan_kills: CMsgBattleReportAggregateStats.CMsgBattleReportStat
            | _Mapping
            | None = ...,
            teleports_used: CMsgBattleReportAggregateStats.CMsgBattleReportStat
            | _Mapping
            | None = ...,
            dewards: CMsgBattleReportAggregateStats.CMsgBattleReportStat | _Mapping | None = ...,
            camps_stacked: CMsgBattleReportAggregateStats.CMsgBattleReportStat
            | _Mapping
            | None = ...,
            support_gold: CMsgBattleReportAggregateStats.CMsgBattleReportStat
            | _Mapping
            | None = ...,
            hero_damage: CMsgBattleReportAggregateStats.CMsgBattleReportStat
            | _Mapping
            | None = ...,
            hero_healing: CMsgBattleReportAggregateStats.CMsgBattleReportStat
            | _Mapping
            | None = ...,
            tower_damage: CMsgBattleReportAggregateStats.CMsgBattleReportStat
            | _Mapping
            | None = ...,
            successful_smokes: CMsgBattleReportAggregateStats.CMsgBattleReportStat
            | _Mapping
            | None = ...,
            stun_duration: CMsgBattleReportAggregateStats.CMsgBattleReportStat
            | _Mapping
            | None = ...,
            duration: CMsgBattleReportAggregateStats.CMsgBattleReportStat | _Mapping | None = ...,
            friendly_roshan_kills: CMsgBattleReportAggregateStats.CMsgBattleReportStat
            | _Mapping
            | None = ...,
        ) -> None: ...

    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: _containers.RepeatedCompositeFieldContainer[
        CMsgBattleReportAggregateStats.CMsgBattleReportAggregate
    ]
    def __init__(
        self,
        result: _Iterable[CMsgBattleReportAggregateStats.CMsgBattleReportAggregate | _Mapping]
        | None = ...,
    ) -> None: ...

class CMsgBattleReportAggregatedGeneralStats(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CMsgClientToGCGetBattleReportResponse(_message.Message):
    __slots__ = ("report", "response", "aggregate_stats", "info")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCGetBattleReportResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCGetBattleReportResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCGetBattleReportResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCGetBattleReportResponse.EResponse]
        k_ePermissionDenied: _ClassVar[CMsgClientToGCGetBattleReportResponse.EResponse]
        k_eNotSubscribedToDotaPlus: _ClassVar[CMsgClientToGCGetBattleReportResponse.EResponse]
        k_eInvalidParameters: _ClassVar[CMsgClientToGCGetBattleReportResponse.EResponse]
        k_eUnableToGetPlusSubInfo: _ClassVar[CMsgClientToGCGetBattleReportResponse.EResponse]
        k_eUnableToLoadBattleReport: _ClassVar[CMsgClientToGCGetBattleReportResponse.EResponse]
        k_eUnableToSaveBattleReport: _ClassVar[CMsgClientToGCGetBattleReportResponse.EResponse]
        k_eUnableToGetAggregates: _ClassVar[CMsgClientToGCGetBattleReportResponse.EResponse]
        k_eNotEnoughGamesPlayed: _ClassVar[CMsgClientToGCGetBattleReportResponse.EResponse]

    k_eInternalError: CMsgClientToGCGetBattleReportResponse.EResponse
    k_eSuccess: CMsgClientToGCGetBattleReportResponse.EResponse
    k_eTooBusy: CMsgClientToGCGetBattleReportResponse.EResponse
    k_eDisabled: CMsgClientToGCGetBattleReportResponse.EResponse
    k_ePermissionDenied: CMsgClientToGCGetBattleReportResponse.EResponse
    k_eNotSubscribedToDotaPlus: CMsgClientToGCGetBattleReportResponse.EResponse
    k_eInvalidParameters: CMsgClientToGCGetBattleReportResponse.EResponse
    k_eUnableToGetPlusSubInfo: CMsgClientToGCGetBattleReportResponse.EResponse
    k_eUnableToLoadBattleReport: CMsgClientToGCGetBattleReportResponse.EResponse
    k_eUnableToSaveBattleReport: CMsgClientToGCGetBattleReportResponse.EResponse
    k_eUnableToGetAggregates: CMsgClientToGCGetBattleReportResponse.EResponse
    k_eNotEnoughGamesPlayed: CMsgClientToGCGetBattleReportResponse.EResponse
    REPORT_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_STATS_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    report: CMsgBattleReport
    response: CMsgClientToGCGetBattleReportResponse.EResponse
    aggregate_stats: CMsgBattleReportAggregateStats
    info: CMsgBattleReportInfo
    def __init__(
        self,
        report: CMsgBattleReport | _Mapping | None = ...,
        response: CMsgClientToGCGetBattleReportResponse.EResponse | str | None = ...,
        aggregate_stats: CMsgBattleReportAggregateStats | _Mapping | None = ...,
        info: CMsgBattleReportInfo | _Mapping | None = ...,
    ) -> None: ...

class CMsgClientToGCGetBattleReportAggregateStats(_message.Message):
    __slots__ = ("aggregate_keys", "timestamp", "duration", "rank")
    class CMsgBattleReportAggregateKey(_message.Message):
        __slots__ = ("hero_id", "predicted_position")
        HERO_ID_FIELD_NUMBER: _ClassVar[int]
        PREDICTED_POSITION_FIELD_NUMBER: _ClassVar[int]
        hero_id: int
        predicted_position: int
        def __init__(
            self, hero_id: int | None = ..., predicted_position: int | None = ...
        ) -> None: ...

    AGGREGATE_KEYS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    aggregate_keys: _containers.RepeatedCompositeFieldContainer[
        CMsgClientToGCGetBattleReportAggregateStats.CMsgBattleReportAggregateKey
    ]
    timestamp: int
    duration: int
    rank: int
    def __init__(
        self,
        aggregate_keys: _Iterable[
            CMsgClientToGCGetBattleReportAggregateStats.CMsgBattleReportAggregateKey | _Mapping
        ]
        | None = ...,
        timestamp: int | None = ...,
        duration: int | None = ...,
        rank: int | None = ...,
    ) -> None: ...

class CMsgClientToGCGetBattleReportAggregateStatsResponse(_message.Message):
    __slots__ = ("aggregate_stats", "response")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCGetBattleReportAggregateStatsResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCGetBattleReportAggregateStatsResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCGetBattleReportAggregateStatsResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCGetBattleReportAggregateStatsResponse.EResponse]
        k_ePermissionDenied: _ClassVar[
            CMsgClientToGCGetBattleReportAggregateStatsResponse.EResponse
        ]
        k_eInvalidParams: _ClassVar[CMsgClientToGCGetBattleReportAggregateStatsResponse.EResponse]
        k_eNotSubscribedToDotaPlus: _ClassVar[
            CMsgClientToGCGetBattleReportAggregateStatsResponse.EResponse
        ]

    k_eInternalError: CMsgClientToGCGetBattleReportAggregateStatsResponse.EResponse
    k_eSuccess: CMsgClientToGCGetBattleReportAggregateStatsResponse.EResponse
    k_eTooBusy: CMsgClientToGCGetBattleReportAggregateStatsResponse.EResponse
    k_eDisabled: CMsgClientToGCGetBattleReportAggregateStatsResponse.EResponse
    k_ePermissionDenied: CMsgClientToGCGetBattleReportAggregateStatsResponse.EResponse
    k_eInvalidParams: CMsgClientToGCGetBattleReportAggregateStatsResponse.EResponse
    k_eNotSubscribedToDotaPlus: CMsgClientToGCGetBattleReportAggregateStatsResponse.EResponse
    AGGREGATE_STATS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    aggregate_stats: CMsgBattleReportAggregateStats
    response: CMsgClientToGCGetBattleReportAggregateStatsResponse.EResponse
    def __init__(
        self,
        aggregate_stats: CMsgBattleReportAggregateStats | _Mapping | None = ...,
        response: CMsgClientToGCGetBattleReportAggregateStatsResponse.EResponse | str | None = ...,
    ) -> None: ...

class CMsgClientToGCGetBattleReportInfo(_message.Message):
    __slots__ = ("account_id",)
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    def __init__(self, account_id: int | None = ...) -> None: ...

class CMsgClientToGCGetBattleReportInfoResponse(_message.Message):
    __slots__ = ("battle_report_info_list", "response")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCGetBattleReportInfoResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCGetBattleReportInfoResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCGetBattleReportInfoResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCGetBattleReportInfoResponse.EResponse]
        k_ePermissionDenied: _ClassVar[CMsgClientToGCGetBattleReportInfoResponse.EResponse]
        k_eNotSubscribedToDotaPlus: _ClassVar[CMsgClientToGCGetBattleReportInfoResponse.EResponse]

    k_eInternalError: CMsgClientToGCGetBattleReportInfoResponse.EResponse
    k_eSuccess: CMsgClientToGCGetBattleReportInfoResponse.EResponse
    k_eTooBusy: CMsgClientToGCGetBattleReportInfoResponse.EResponse
    k_eDisabled: CMsgClientToGCGetBattleReportInfoResponse.EResponse
    k_ePermissionDenied: CMsgClientToGCGetBattleReportInfoResponse.EResponse
    k_eNotSubscribedToDotaPlus: CMsgClientToGCGetBattleReportInfoResponse.EResponse
    BATTLE_REPORT_INFO_LIST_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    battle_report_info_list: CMsgBattleReportInfoList
    response: CMsgClientToGCGetBattleReportInfoResponse.EResponse
    def __init__(
        self,
        battle_report_info_list: CMsgBattleReportInfoList | _Mapping | None = ...,
        response: CMsgClientToGCGetBattleReportInfoResponse.EResponse | str | None = ...,
    ) -> None: ...

class CMsgClientToGCAcknowledgeBattleReport(_message.Message):
    __slots__ = ("account_id", "timestamp", "duration")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    timestamp: int
    duration: int
    def __init__(
        self, account_id: int | None = ..., timestamp: int | None = ..., duration: int | None = ...
    ) -> None: ...

class CMsgClientToGCAcknowledgeBattleReportResponse(_message.Message):
    __slots__ = ("response", "shards_awarded")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCAcknowledgeBattleReportResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCAcknowledgeBattleReportResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCAcknowledgeBattleReportResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCAcknowledgeBattleReportResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCAcknowledgeBattleReportResponse.EResponse]
        k_ePermissionDenied: _ClassVar[CMsgClientToGCAcknowledgeBattleReportResponse.EResponse]
        k_eUnableToLoadBattleReport: _ClassVar[
            CMsgClientToGCAcknowledgeBattleReportResponse.EResponse
        ]
        k_eAlreadyAcknowledged: _ClassVar[CMsgClientToGCAcknowledgeBattleReportResponse.EResponse]
        k_eUnknownReport: _ClassVar[CMsgClientToGCAcknowledgeBattleReportResponse.EResponse]
        k_eNotSubscribedToDotaPlus: _ClassVar[
            CMsgClientToGCAcknowledgeBattleReportResponse.EResponse
        ]
        k_eNotEnoughGamesPlayed: _ClassVar[CMsgClientToGCAcknowledgeBattleReportResponse.EResponse]

    k_eInternalError: CMsgClientToGCAcknowledgeBattleReportResponse.EResponse
    k_eSuccess: CMsgClientToGCAcknowledgeBattleReportResponse.EResponse
    k_eTooBusy: CMsgClientToGCAcknowledgeBattleReportResponse.EResponse
    k_eDisabled: CMsgClientToGCAcknowledgeBattleReportResponse.EResponse
    k_eTimeout: CMsgClientToGCAcknowledgeBattleReportResponse.EResponse
    k_ePermissionDenied: CMsgClientToGCAcknowledgeBattleReportResponse.EResponse
    k_eUnableToLoadBattleReport: CMsgClientToGCAcknowledgeBattleReportResponse.EResponse
    k_eAlreadyAcknowledged: CMsgClientToGCAcknowledgeBattleReportResponse.EResponse
    k_eUnknownReport: CMsgClientToGCAcknowledgeBattleReportResponse.EResponse
    k_eNotSubscribedToDotaPlus: CMsgClientToGCAcknowledgeBattleReportResponse.EResponse
    k_eNotEnoughGamesPlayed: CMsgClientToGCAcknowledgeBattleReportResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    SHARDS_AWARDED_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCAcknowledgeBattleReportResponse.EResponse
    shards_awarded: int
    def __init__(
        self,
        response: CMsgClientToGCAcknowledgeBattleReportResponse.EResponse | str | None = ...,
        shards_awarded: int | None = ...,
    ) -> None: ...

class CMsgClientToGCGetBattleReportMatchHistory(_message.Message):
    __slots__ = ("account_id", "timestamp", "duration")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    timestamp: int
    duration: int
    def __init__(
        self, account_id: int | None = ..., timestamp: int | None = ..., duration: int | None = ...
    ) -> None: ...

class CMsgClientToGCGetBattleReportMatchHistoryResponse(_message.Message):
    __slots__ = ("response", "games")
    class EResponse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_eInternalError: _ClassVar[CMsgClientToGCGetBattleReportMatchHistoryResponse.EResponse]
        k_eSuccess: _ClassVar[CMsgClientToGCGetBattleReportMatchHistoryResponse.EResponse]
        k_eTooBusy: _ClassVar[CMsgClientToGCGetBattleReportMatchHistoryResponse.EResponse]
        k_eDisabled: _ClassVar[CMsgClientToGCGetBattleReportMatchHistoryResponse.EResponse]
        k_eTimeout: _ClassVar[CMsgClientToGCGetBattleReportMatchHistoryResponse.EResponse]
        k_ePermissionDenied: _ClassVar[CMsgClientToGCGetBattleReportMatchHistoryResponse.EResponse]
        k_eNotSubscribedToDotaPlus: _ClassVar[
            CMsgClientToGCGetBattleReportMatchHistoryResponse.EResponse
        ]

    k_eInternalError: CMsgClientToGCGetBattleReportMatchHistoryResponse.EResponse
    k_eSuccess: CMsgClientToGCGetBattleReportMatchHistoryResponse.EResponse
    k_eTooBusy: CMsgClientToGCGetBattleReportMatchHistoryResponse.EResponse
    k_eDisabled: CMsgClientToGCGetBattleReportMatchHistoryResponse.EResponse
    k_eTimeout: CMsgClientToGCGetBattleReportMatchHistoryResponse.EResponse
    k_ePermissionDenied: CMsgClientToGCGetBattleReportMatchHistoryResponse.EResponse
    k_eNotSubscribedToDotaPlus: CMsgClientToGCGetBattleReportMatchHistoryResponse.EResponse
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    GAMES_FIELD_NUMBER: _ClassVar[int]
    response: CMsgClientToGCGetBattleReportMatchHistoryResponse.EResponse
    games: CMsgBattleReport_GameList
    def __init__(
        self,
        response: CMsgClientToGCGetBattleReportMatchHistoryResponse.EResponse | str | None = ...,
        games: CMsgBattleReport_GameList | _Mapping | None = ...,
    ) -> None: ...
