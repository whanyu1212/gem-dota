from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

import dota_commonmessages_pb2 as _dota_commonmessages_pb2
import dota_shared_enums_pb2 as _dota_shared_enums_pb2
import networkbasetypes_pb2 as _networkbasetypes_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class EDotaUserMessages(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOTA_UM_AddUnitToSelection: _ClassVar[EDotaUserMessages]
    DOTA_UM_AIDebugLine: _ClassVar[EDotaUserMessages]
    DOTA_UM_ChatEvent: _ClassVar[EDotaUserMessages]
    DOTA_UM_CombatHeroPositions: _ClassVar[EDotaUserMessages]
    DOTA_UM_CombatLogData: _ClassVar[EDotaUserMessages]
    DOTA_UM_CombatLogBulkData: _ClassVar[EDotaUserMessages]
    DOTA_UM_CreateLinearProjectile: _ClassVar[EDotaUserMessages]
    DOTA_UM_DestroyLinearProjectile: _ClassVar[EDotaUserMessages]
    DOTA_UM_DodgeTrackingProjectiles: _ClassVar[EDotaUserMessages]
    DOTA_UM_GlobalLightColor: _ClassVar[EDotaUserMessages]
    DOTA_UM_GlobalLightDirection: _ClassVar[EDotaUserMessages]
    DOTA_UM_InvalidCommand: _ClassVar[EDotaUserMessages]
    DOTA_UM_LocationPing: _ClassVar[EDotaUserMessages]
    DOTA_UM_MapLine: _ClassVar[EDotaUserMessages]
    DOTA_UM_MiniKillCamInfo: _ClassVar[EDotaUserMessages]
    DOTA_UM_MinimapDebugPoint: _ClassVar[EDotaUserMessages]
    DOTA_UM_MinimapEvent: _ClassVar[EDotaUserMessages]
    DOTA_UM_NevermoreRequiem: _ClassVar[EDotaUserMessages]
    DOTA_UM_OverheadEvent: _ClassVar[EDotaUserMessages]
    DOTA_UM_SetNextAutobuyItem: _ClassVar[EDotaUserMessages]
    DOTA_UM_SharedCooldown: _ClassVar[EDotaUserMessages]
    DOTA_UM_SpectatorPlayerClick: _ClassVar[EDotaUserMessages]
    DOTA_UM_TutorialTipInfo: _ClassVar[EDotaUserMessages]
    DOTA_UM_UnitEvent: _ClassVar[EDotaUserMessages]
    DOTA_UM_ParticleManager: _ClassVar[EDotaUserMessages]
    DOTA_UM_BotChat: _ClassVar[EDotaUserMessages]
    DOTA_UM_HudError: _ClassVar[EDotaUserMessages]
    DOTA_UM_ItemPurchased: _ClassVar[EDotaUserMessages]
    DOTA_UM_Ping: _ClassVar[EDotaUserMessages]
    DOTA_UM_ItemFound: _ClassVar[EDotaUserMessages]
    DOTA_UM_CharacterSpeakConcept: _ClassVar[EDotaUserMessages]
    DOTA_UM_SwapVerify: _ClassVar[EDotaUserMessages]
    DOTA_UM_WorldLine: _ClassVar[EDotaUserMessages]
    DOTA_UM_TournamentDrop: _ClassVar[EDotaUserMessages]
    DOTA_UM_ItemAlert: _ClassVar[EDotaUserMessages]
    DOTA_UM_HalloweenDrops: _ClassVar[EDotaUserMessages]
    DOTA_UM_ChatWheel: _ClassVar[EDotaUserMessages]
    DOTA_UM_ReceivedXmasGift: _ClassVar[EDotaUserMessages]
    DOTA_UM_UpdateSharedContent: _ClassVar[EDotaUserMessages]
    DOTA_UM_TutorialRequestExp: _ClassVar[EDotaUserMessages]
    DOTA_UM_TutorialPingMinimap: _ClassVar[EDotaUserMessages]
    DOTA_UM_GamerulesStateChanged: _ClassVar[EDotaUserMessages]
    DOTA_UM_ShowSurvey: _ClassVar[EDotaUserMessages]
    DOTA_UM_TutorialFade: _ClassVar[EDotaUserMessages]
    DOTA_UM_AddQuestLogEntry: _ClassVar[EDotaUserMessages]
    DOTA_UM_SendStatPopup: _ClassVar[EDotaUserMessages]
    DOTA_UM_TutorialFinish: _ClassVar[EDotaUserMessages]
    DOTA_UM_SendRoshanPopup: _ClassVar[EDotaUserMessages]
    DOTA_UM_SendGenericToolTip: _ClassVar[EDotaUserMessages]
    DOTA_UM_SendFinalGold: _ClassVar[EDotaUserMessages]
    DOTA_UM_CustomMsg: _ClassVar[EDotaUserMessages]
    DOTA_UM_CoachHUDPing: _ClassVar[EDotaUserMessages]
    DOTA_UM_ClientLoadGridNav: _ClassVar[EDotaUserMessages]
    DOTA_UM_TE_Projectile: _ClassVar[EDotaUserMessages]
    DOTA_UM_TE_ProjectileLoc: _ClassVar[EDotaUserMessages]
    DOTA_UM_TE_DotaBloodImpact: _ClassVar[EDotaUserMessages]
    DOTA_UM_TE_UnitAnimation: _ClassVar[EDotaUserMessages]
    DOTA_UM_TE_UnitAnimationEnd: _ClassVar[EDotaUserMessages]
    DOTA_UM_AbilityPing: _ClassVar[EDotaUserMessages]
    DOTA_UM_ShowGenericPopup: _ClassVar[EDotaUserMessages]
    DOTA_UM_VoteStart: _ClassVar[EDotaUserMessages]
    DOTA_UM_VoteUpdate: _ClassVar[EDotaUserMessages]
    DOTA_UM_VoteEnd: _ClassVar[EDotaUserMessages]
    DOTA_UM_BoosterState: _ClassVar[EDotaUserMessages]
    DOTA_UM_WillPurchaseAlert: _ClassVar[EDotaUserMessages]
    DOTA_UM_TutorialMinimapPosition: _ClassVar[EDotaUserMessages]
    DOTA_UM_AbilitySteal: _ClassVar[EDotaUserMessages]
    DOTA_UM_CourierKilledAlert: _ClassVar[EDotaUserMessages]
    DOTA_UM_EnemyItemAlert: _ClassVar[EDotaUserMessages]
    DOTA_UM_StatsMatchDetails: _ClassVar[EDotaUserMessages]
    DOTA_UM_MiniTaunt: _ClassVar[EDotaUserMessages]
    DOTA_UM_BuyBackStateAlert: _ClassVar[EDotaUserMessages]
    DOTA_UM_SpeechBubble: _ClassVar[EDotaUserMessages]
    DOTA_UM_CustomHeaderMessage: _ClassVar[EDotaUserMessages]
    DOTA_UM_QuickBuyAlert: _ClassVar[EDotaUserMessages]
    DOTA_UM_StatsHeroDetails: _ClassVar[EDotaUserMessages]
    DOTA_UM_PredictionResult: _ClassVar[EDotaUserMessages]
    DOTA_UM_ModifierAlert: _ClassVar[EDotaUserMessages]
    DOTA_UM_HPManaAlert: _ClassVar[EDotaUserMessages]
    DOTA_UM_GlyphAlert: _ClassVar[EDotaUserMessages]
    DOTA_UM_BeastChat: _ClassVar[EDotaUserMessages]
    DOTA_UM_SpectatorPlayerUnitOrders: _ClassVar[EDotaUserMessages]
    DOTA_UM_CustomHudElement_Create: _ClassVar[EDotaUserMessages]
    DOTA_UM_CustomHudElement_Modify: _ClassVar[EDotaUserMessages]
    DOTA_UM_CustomHudElement_Destroy: _ClassVar[EDotaUserMessages]
    DOTA_UM_CompendiumState: _ClassVar[EDotaUserMessages]
    DOTA_UM_ProjectionAbility: _ClassVar[EDotaUserMessages]
    DOTA_UM_ProjectionEvent: _ClassVar[EDotaUserMessages]
    DOTA_UM_CombatLogDataHLTV: _ClassVar[EDotaUserMessages]
    DOTA_UM_XPAlert: _ClassVar[EDotaUserMessages]
    DOTA_UM_UpdateQuestProgress: _ClassVar[EDotaUserMessages]
    DOTA_UM_MatchMetadata: _ClassVar[EDotaUserMessages]
    DOTA_UM_MatchDetails: _ClassVar[EDotaUserMessages]
    DOTA_UM_QuestStatus: _ClassVar[EDotaUserMessages]
    DOTA_UM_SuggestHeroPick: _ClassVar[EDotaUserMessages]
    DOTA_UM_SuggestHeroRole: _ClassVar[EDotaUserMessages]
    DOTA_UM_KillcamDamageTaken: _ClassVar[EDotaUserMessages]
    DOTA_UM_SelectPenaltyGold: _ClassVar[EDotaUserMessages]
    DOTA_UM_RollDiceResult: _ClassVar[EDotaUserMessages]
    DOTA_UM_FlipCoinResult: _ClassVar[EDotaUserMessages]
    DOTA_UM_RequestItemSuggestions: _ClassVar[EDotaUserMessages]
    DOTA_UM_TeamCaptainChanged: _ClassVar[EDotaUserMessages]
    DOTA_UM_SendRoshanSpectatorPhase: _ClassVar[EDotaUserMessages]
    DOTA_UM_ChatWheelCooldown: _ClassVar[EDotaUserMessages]
    DOTA_UM_DismissAllStatPopups: _ClassVar[EDotaUserMessages]
    DOTA_UM_TE_DestroyProjectile: _ClassVar[EDotaUserMessages]
    DOTA_UM_HeroRelicProgress: _ClassVar[EDotaUserMessages]
    DOTA_UM_AbilityDraftRequestAbility: _ClassVar[EDotaUserMessages]
    DOTA_UM_ItemSold: _ClassVar[EDotaUserMessages]
    DOTA_UM_DamageReport: _ClassVar[EDotaUserMessages]
    DOTA_UM_SalutePlayer: _ClassVar[EDotaUserMessages]
    DOTA_UM_TipAlert: _ClassVar[EDotaUserMessages]
    DOTA_UM_ReplaceQueryUnit: _ClassVar[EDotaUserMessages]
    DOTA_UM_EmptyTeleportAlert: _ClassVar[EDotaUserMessages]
    DOTA_UM_MarsArenaOfBloodAttack: _ClassVar[EDotaUserMessages]
    DOTA_UM_ESArcanaCombo: _ClassVar[EDotaUserMessages]
    DOTA_UM_ESArcanaComboSummary: _ClassVar[EDotaUserMessages]
    DOTA_UM_HighFiveLeftHanging: _ClassVar[EDotaUserMessages]
    DOTA_UM_HighFiveCompleted: _ClassVar[EDotaUserMessages]
    DOTA_UM_ShovelUnearth: _ClassVar[EDotaUserMessages]
    DOTA_UM_RadarAlert: _ClassVar[EDotaUserMessages]
    DOTA_UM_AllStarEvent: _ClassVar[EDotaUserMessages]
    DOTA_UM_TalentTreeAlert: _ClassVar[EDotaUserMessages]
    DOTA_UM_QueuedOrderRemoved: _ClassVar[EDotaUserMessages]
    DOTA_UM_DebugChallenge: _ClassVar[EDotaUserMessages]
    DOTA_UM_OMArcanaCombo: _ClassVar[EDotaUserMessages]
    DOTA_UM_FoundNeutralItem: _ClassVar[EDotaUserMessages]
    DOTA_UM_OutpostCaptured: _ClassVar[EDotaUserMessages]
    DOTA_UM_OutpostGrantedXP: _ClassVar[EDotaUserMessages]
    DOTA_UM_MoveCameraToUnit: _ClassVar[EDotaUserMessages]
    DOTA_UM_PauseMinigameData: _ClassVar[EDotaUserMessages]
    DOTA_UM_VersusScene_PlayerBehavior: _ClassVar[EDotaUserMessages]
    DOTA_UM_QoP_ArcanaSummary: _ClassVar[EDotaUserMessages]
    DOTA_UM_HotPotato_Created: _ClassVar[EDotaUserMessages]
    DOTA_UM_HotPotato_Exploded: _ClassVar[EDotaUserMessages]
    DOTA_UM_WK_Arcana_Progress: _ClassVar[EDotaUserMessages]
    DOTA_UM_GuildChallenge_Progress: _ClassVar[EDotaUserMessages]
    DOTA_UM_WRArcanaProgress: _ClassVar[EDotaUserMessages]
    DOTA_UM_WRArcanaSummary: _ClassVar[EDotaUserMessages]
    DOTA_UM_EmptyItemSlotAlert: _ClassVar[EDotaUserMessages]
    DOTA_UM_AghsStatusAlert: _ClassVar[EDotaUserMessages]
    DOTA_UM_PingConfirmation: _ClassVar[EDotaUserMessages]
    DOTA_UM_MutedPlayers: _ClassVar[EDotaUserMessages]
    DOTA_UM_ContextualTip: _ClassVar[EDotaUserMessages]
    DOTA_UM_ChatMessage: _ClassVar[EDotaUserMessages]
    DOTA_UM_NeutralCampAlert: _ClassVar[EDotaUserMessages]
    DOTA_UM_RockPaperScissorsStarted: _ClassVar[EDotaUserMessages]
    DOTA_UM_RockPaperScissorsFinished: _ClassVar[EDotaUserMessages]
    DOTA_UM_DuelOpponentKilled: _ClassVar[EDotaUserMessages]
    DOTA_UM_DuelAccepted: _ClassVar[EDotaUserMessages]
    DOTA_UM_DuelRequested: _ClassVar[EDotaUserMessages]
    DOTA_UM_MuertaReleaseEvent_AssignedTargetKilled: _ClassVar[EDotaUserMessages]
    DOTA_UM_PlayerDraftSuggestPick: _ClassVar[EDotaUserMessages]
    DOTA_UM_PlayerDraftPick: _ClassVar[EDotaUserMessages]
    DOTA_UM_UpdateLinearProjectileCPData: _ClassVar[EDotaUserMessages]
    DOTA_UM_GiftPlayer: _ClassVar[EDotaUserMessages]
    DOTA_UM_FacetPing: _ClassVar[EDotaUserMessages]
    DOTA_UM_InnatePing: _ClassVar[EDotaUserMessages]
    DOTA_UM_RoshanTimer: _ClassVar[EDotaUserMessages]
    DOTA_UM_NeutralCraftAvailable: _ClassVar[EDotaUserMessages]
    DOTA_UM_TimerAlert: _ClassVar[EDotaUserMessages]
    DOTA_UM_MadstoneAlert: _ClassVar[EDotaUserMessages]
    DOTA_UM_CourierLeftFountainAlert: _ClassVar[EDotaUserMessages]
    DOTA_UM_MonsterHunter_InvestigationsAvailable: _ClassVar[EDotaUserMessages]
    DOTA_UM_MonsterHunter_InvestigationGameState: _ClassVar[EDotaUserMessages]
    DOTA_UM_MonsterHunter_HuntAlert: _ClassVar[EDotaUserMessages]
    DOTA_UM_TormentorTimer: _ClassVar[EDotaUserMessages]
    DOTA_UM_KillEffect: _ClassVar[EDotaUserMessages]

class DOTA_CHAT_MESSAGE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CHAT_MESSAGE_INVALID: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_HERO_KILL: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_HERO_DENY: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_BARRACKS_KILL: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_TOWER_KILL: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_TOWER_DENY: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_FIRSTBLOOD: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_STREAK_KILL: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_BUYBACK: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_AEGIS: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_ROSHAN_KILL: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_COURIER_LOST: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_COURIER_RESPAWNED: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_GLYPH_USED: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_ITEM_PURCHASE: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_CONNECT: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_DISCONNECT: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_DISCONNECT_WAIT_FOR_RECONNECT: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_DISCONNECT_TIME_REMAINING: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_DISCONNECT_TIME_REMAINING_PLURAL: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_RECONNECT: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_PLAYER_LEFT: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_SAFE_TO_LEAVE: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_RUNE_PICKUP: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_RUNE_BOTTLE: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_RUNE_DENY: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_INTHEBAG: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_SECRETSHOP: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_ITEM_AUTOPURCHASED: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_ITEMS_COMBINED: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_SUPER_CREEPS: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_CANT_USE_ACTION_ITEM: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_CANTPAUSE: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_NOPAUSESLEFT: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_CANTPAUSEYET: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_PAUSED: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_UNPAUSE_COUNTDOWN: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_UNPAUSED: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_AUTO_UNPAUSED: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_YOUPAUSED: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_CANTUNPAUSETEAM: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_VOICE_TEXT_BANNED: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_SPECTATORS_WATCHING_THIS_GAME: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_REPORT_REMINDER: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_ECON_ITEM: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_TAUNT: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_RANDOM: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_RD_TURN: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_DROP_RATE_BONUS: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_NO_BATTLE_POINTS: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_DENIED_AEGIS: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_INFORMATIONAL: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_AEGIS_STOLEN: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_ROSHAN_CANDY: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_ITEM_GIFTED: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_HERO_KILL_WITH_GREEVIL: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_HOLDOUT_TOWER_DESTROYED: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_HOLDOUT_WALL_DESTROYED: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_HOLDOUT_WALL_FINISHED: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_PLAYER_LEFT_LIMITED_HERO: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_ABANDON_LIMITED_HERO_EXPLANATION: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_DISCONNECT_LIMITED_HERO: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_LOW_PRIORITY_COMPLETED_EXPLANATION: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_RECRUITMENT_DROP_RATE_BONUS: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_FROSTIVUS_SHINING_BOOSTER_ACTIVE: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_PLAYER_LEFT_AFK: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_PLAYER_LEFT_DISCONNECTED_TOO_LONG: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_PLAYER_ABANDONED: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_PLAYER_ABANDONED_AFK: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_PLAYER_ABANDONED_DISCONNECTED_TOO_LONG: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_WILL_NOT_BE_SCORED: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_WILL_NOT_BE_SCORED_RANKED: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_WILL_NOT_BE_SCORED_NETWORK: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_WILL_NOT_BE_SCORED_NETWORK_RANKED: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_CAN_QUIT_WITHOUT_ABANDON: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_RANKED_GAME_STILL_SCORED_LEAVERS_GET_LOSS: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_ABANDON_RANKED_BEFORE_FIRST_BLOOD_PARTY: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_COMPENDIUM_LEVEL: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_VICTORY_PREDICTION_STREAK: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_ASSASSIN_ANNOUNCE: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_ASSASSIN_SUCCESS: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_ASSASSIN_DENIED: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_VICTORY_PREDICTION_SINGLE_USER_CONFIRM: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_EFFIGY_KILL: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_VOICE_TEXT_BANNED_OVERFLOW: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_YEAR_BEAST_KILLED: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_PAUSE_COUNTDOWN: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_COINS_WAGERED: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_HERO_NOMINATED_BAN: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_HERO_BANNED: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_HERO_BAN_COUNT: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_RIVER_PAINTED: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_SCAN_USED: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_SHRINE_KILLED: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_WAGER_TOKEN_SPENT: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_RANK_WAGER: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_NEW_PLAYER_REMINDER: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_OBSERVER_WARD_KILLED: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_SENTRY_WARD_KILLED: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_ITEM_PLACED_IN_NEUTRAL_STASH: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_HERO_CHOICE_INVALID: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_BOUNTY: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_ABILITY_DRAFT_START: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_HERO_FOUND_CANDY: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_ABILITY_DRAFT_RANDOMED: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_PRIVATE_COACH_CONNECTED: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_CANT_PAUSE_TOO_EARLY: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_HERO_KILL_WITH_PENGUIN: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_MINIBOSS_KILL: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_PLAYER_IN_GAME_BAN_TEXT: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_BANNER_PLANTED: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_ALCHEMIST_GRANTED_SCEPTER: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_PROTECTOR_SPAWNED: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_CRAFTING_XP: _ClassVar[DOTA_CHAT_MESSAGE]
    CHAT_MESSAGE_ROSHAN_ROAR: _ClassVar[DOTA_CHAT_MESSAGE]

class DOTA_NO_BATTLE_POINTS_REASONS(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NO_BATTLE_POINTS_WRONG_LOBBY_TYPE: _ClassVar[DOTA_NO_BATTLE_POINTS_REASONS]
    NO_BATTLE_POINTS_PRACTICE_BOTS: _ClassVar[DOTA_NO_BATTLE_POINTS_REASONS]
    NO_BATTLE_POINTS_CHEATS_ENABLED: _ClassVar[DOTA_NO_BATTLE_POINTS_REASONS]
    NO_BATTLE_POINTS_LOW_PRIORITY: _ClassVar[DOTA_NO_BATTLE_POINTS_REASONS]

class DOTA_CHAT_INFORMATIONAL(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INFO_COOP_BATTLE_POINTS_RULES: _ClassVar[DOTA_CHAT_INFORMATIONAL]
    INFO_FROSTIVUS_ABANDON_REMINDER: _ClassVar[DOTA_CHAT_INFORMATIONAL]
    INFO_RANKED_REMINDER: _ClassVar[DOTA_CHAT_INFORMATIONAL]
    INFO_COOP_LOW_PRIORITY_PASSIVE_REMINDER: _ClassVar[DOTA_CHAT_INFORMATIONAL]
    INFO_CUSTOM_GAME_PENALTY_REMINDER: _ClassVar[DOTA_CHAT_INFORMATIONAL]

class DOTA_ABILITY_PING_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ABILITY_PING_READY: _ClassVar[DOTA_ABILITY_PING_TYPE]
    ABILITY_PING_MANA: _ClassVar[DOTA_ABILITY_PING_TYPE]
    ABILITY_PING_COOLDOWN: _ClassVar[DOTA_ABILITY_PING_TYPE]
    ABILITY_PING_ENEMY: _ClassVar[DOTA_ABILITY_PING_TYPE]
    ABILITY_PING_UNLEARNED: _ClassVar[DOTA_ABILITY_PING_TYPE]
    ABILITY_PING_INBACKPACK: _ClassVar[DOTA_ABILITY_PING_TYPE]
    ABILITY_PING_INSTASH: _ClassVar[DOTA_ABILITY_PING_TYPE]
    ABILITY_PING_ONCOURIER: _ClassVar[DOTA_ABILITY_PING_TYPE]
    ABILITY_PING_ALLY: _ClassVar[DOTA_ABILITY_PING_TYPE]
    ABILITY_PING_LEARN_READY: _ClassVar[DOTA_ABILITY_PING_TYPE]
    ABILITY_PING_WILL_LEARN: _ClassVar[DOTA_ABILITY_PING_TYPE]
    ABILITY_PING_FUTURE_LEARN: _ClassVar[DOTA_ABILITY_PING_TYPE]
    ABILITY_PING_NEUTRAL_OFFER: _ClassVar[DOTA_ABILITY_PING_TYPE]
    ABILITY_PING_NEUTRAL_REQUEST: _ClassVar[DOTA_ABILITY_PING_TYPE]
    ABILITY_PING_NEUTRAL_EQUIP: _ClassVar[DOTA_ABILITY_PING_TYPE]
    ABILITY_PING_INCOURIERBACKPACK: _ClassVar[DOTA_ABILITY_PING_TYPE]

class DOTA_REPLAY_STATE_EVENT(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOTA_REPLAY_STATE_EVENT_GAME_START: _ClassVar[DOTA_REPLAY_STATE_EVENT]
    DOTA_REPLAY_STATE_EVENT_STARTING_HORN: _ClassVar[DOTA_REPLAY_STATE_EVENT]
    DOTA_REPLAY_STATE_EVENT_FIRST_BLOOD: _ClassVar[DOTA_REPLAY_STATE_EVENT]
    DOTA_REPLAY_STATE_EVENT_SHOWCASE: _ClassVar[DOTA_REPLAY_STATE_EVENT]
    DOTA_REPLAY_STATE_EVENT_POST_GAME: _ClassVar[DOTA_REPLAY_STATE_EVENT]
    DOTA_REPLAY_STATE_EVENT_WAIT_FOR_MAP: _ClassVar[DOTA_REPLAY_STATE_EVENT]

class EDotaEntityMessages(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOTA_UNIT_SPEECH: _ClassVar[EDotaEntityMessages]
    DOTA_UNIT_SPEECH_MUTE: _ClassVar[EDotaEntityMessages]
    DOTA_UNIT_ADD_GESTURE: _ClassVar[EDotaEntityMessages]
    DOTA_UNIT_REMOVE_GESTURE: _ClassVar[EDotaEntityMessages]
    DOTA_UNIT_REMOVE_ALL_GESTURES: _ClassVar[EDotaEntityMessages]
    DOTA_UNIT_FADE_GESTURE: _ClassVar[EDotaEntityMessages]
    DOTA_UNIT_SPEECH_CLIENTSIDE_RULES: _ClassVar[EDotaEntityMessages]

class DOTA_OVERHEAD_ALERT(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OVERHEAD_ALERT_GOLD: _ClassVar[DOTA_OVERHEAD_ALERT]
    OVERHEAD_ALERT_DENY: _ClassVar[DOTA_OVERHEAD_ALERT]
    OVERHEAD_ALERT_CRITICAL: _ClassVar[DOTA_OVERHEAD_ALERT]
    OVERHEAD_ALERT_XP: _ClassVar[DOTA_OVERHEAD_ALERT]
    OVERHEAD_ALERT_BONUS_SPELL_DAMAGE: _ClassVar[DOTA_OVERHEAD_ALERT]
    OVERHEAD_ALERT_MISS: _ClassVar[DOTA_OVERHEAD_ALERT]
    OVERHEAD_ALERT_DAMAGE: _ClassVar[DOTA_OVERHEAD_ALERT]
    OVERHEAD_ALERT_EVADE: _ClassVar[DOTA_OVERHEAD_ALERT]
    OVERHEAD_ALERT_BLOCK: _ClassVar[DOTA_OVERHEAD_ALERT]
    OVERHEAD_ALERT_BONUS_POISON_DAMAGE: _ClassVar[DOTA_OVERHEAD_ALERT]
    OVERHEAD_ALERT_HEAL: _ClassVar[DOTA_OVERHEAD_ALERT]
    OVERHEAD_ALERT_MANA_ADD: _ClassVar[DOTA_OVERHEAD_ALERT]
    OVERHEAD_ALERT_MANA_LOSS: _ClassVar[DOTA_OVERHEAD_ALERT]
    OVERHEAD_ALERT_MAGICAL_BLOCK: _ClassVar[DOTA_OVERHEAD_ALERT]
    OVERHEAD_ALERT_INCOMING_DAMAGE: _ClassVar[DOTA_OVERHEAD_ALERT]
    OVERHEAD_ALERT_OUTGOING_DAMAGE: _ClassVar[DOTA_OVERHEAD_ALERT]
    OVERHEAD_ALERT_DISABLE_RESIST: _ClassVar[DOTA_OVERHEAD_ALERT]
    OVERHEAD_ALERT_DEATH: _ClassVar[DOTA_OVERHEAD_ALERT]
    OVERHEAD_ALERT_BLOCKED: _ClassVar[DOTA_OVERHEAD_ALERT]
    OVERHEAD_ALERT_ITEM_RECEIVED: _ClassVar[DOTA_OVERHEAD_ALERT]
    OVERHEAD_ALERT_SHARD: _ClassVar[DOTA_OVERHEAD_ALERT]
    OVERHEAD_ALERT_DEADLY_BLOW: _ClassVar[DOTA_OVERHEAD_ALERT]
    OVERHEAD_ALERT_FORCE_MISS: _ClassVar[DOTA_OVERHEAD_ALERT]
    OVERHEAD_ALERT_AEGIS: _ClassVar[DOTA_OVERHEAD_ALERT]
    OVERHEAD_ALERT_DISPEL: _ClassVar[DOTA_OVERHEAD_ALERT]

class DOTA_ROSHAN_PHASE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_SRSP_ROSHAN_ALIVE: _ClassVar[DOTA_ROSHAN_PHASE]
    k_SRSP_ROSHAN_BASE_TIMER: _ClassVar[DOTA_ROSHAN_PHASE]
    k_SRSP_ROSHAN_VISIBLE_TIMER: _ClassVar[DOTA_ROSHAN_PHASE]

class DOTA_POSITION_CATEGORY(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOTA_POSITION_NONE: _ClassVar[DOTA_POSITION_CATEGORY]
    DOTA_POSITION_BOTTOM_LANE: _ClassVar[DOTA_POSITION_CATEGORY]
    DOTA_POSITION_MID_LANE: _ClassVar[DOTA_POSITION_CATEGORY]
    DOTA_POSITION_TOP_LANE: _ClassVar[DOTA_POSITION_CATEGORY]
    DOTA_POSITION_RADIANT_JUNGLE: _ClassVar[DOTA_POSITION_CATEGORY]
    DOTA_POSITION_DIRE_JUNGLE: _ClassVar[DOTA_POSITION_CATEGORY]
    DOTA_POSITION_RADIANT_ANCIENTS: _ClassVar[DOTA_POSITION_CATEGORY]
    DOTA_POSITION_DIRE_ANCIENTS: _ClassVar[DOTA_POSITION_CATEGORY]
    DOTA_POSITION_RADIANT_SECRET_SHOP: _ClassVar[DOTA_POSITION_CATEGORY]
    DOTA_POSITION_DIRE_SECRET_SHOP: _ClassVar[DOTA_POSITION_CATEGORY]
    DOTA_POSITION_RIVER: _ClassVar[DOTA_POSITION_CATEGORY]
    DOTA_POSITION_ROSHAN_PIT: _ClassVar[DOTA_POSITION_CATEGORY]
    DOTA_POSITION_RADIANT_BASE: _ClassVar[DOTA_POSITION_CATEGORY]
    DOTA_POSITION_DIRE_BASE: _ClassVar[DOTA_POSITION_CATEGORY]
    DOTA_POSITION_FOUNTAIN: _ClassVar[DOTA_POSITION_CATEGORY]
    DOTA_POSITION_OTHER: _ClassVar[DOTA_POSITION_CATEGORY]

class DOTA_ABILITY_TARGET_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOTA_ABILITY_TARGET_NONE: _ClassVar[DOTA_ABILITY_TARGET_TYPE]
    DOTA_ABILITY_TARGET_SELF: _ClassVar[DOTA_ABILITY_TARGET_TYPE]
    DOTA_ABILITY_TARGET_ALLY_HERO: _ClassVar[DOTA_ABILITY_TARGET_TYPE]
    DOTA_ABILITY_TARGET_ALLY_CREEP: _ClassVar[DOTA_ABILITY_TARGET_TYPE]
    DOTA_ABILITY_TARGET_ENEMY_HERO: _ClassVar[DOTA_ABILITY_TARGET_TYPE]
    DOTA_ABILITY_TARGET_ENEMY_CREEP: _ClassVar[DOTA_ABILITY_TARGET_TYPE]

class EHeroStatType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    k_EHeroStatType_None: _ClassVar[EHeroStatType]
    k_EHeroStatType_AxeTotalDamage: _ClassVar[EHeroStatType]
    k_EHeroStatType_BattleHungerDamage: _ClassVar[EHeroStatType]
    k_EHeroStatType_CounterHelixDamage: _ClassVar[EHeroStatType]
    k_EHeroStatType_CullingBladeDamage: _ClassVar[EHeroStatType]
    k_EHeroStatType_BerserkersCallCastCount: _ClassVar[EHeroStatType]
    k_EHeroStatType_BerserkersCallHeroesHitAverage: _ClassVar[EHeroStatType]
    k_EHeroStatType_BerserkersCallOtherUnitsHit: _ClassVar[EHeroStatType]
    k_EHeroStatType_BerserkersCallHeroAttacksTaken: _ClassVar[EHeroStatType]
    k_EHeroStatType_BerserkersCallOtherAttacksTaken: _ClassVar[EHeroStatType]
    k_EHeroStatType_BattleHungerCastCount: _ClassVar[EHeroStatType]
    k_EHeroStatType_BattleHungerPotentialDuration: _ClassVar[EHeroStatType]
    k_EHeroStatType_BattleHungerAverageDuration: _ClassVar[EHeroStatType]
    k_EHeroStatType_CounterHelixProcCount: _ClassVar[EHeroStatType]
    k_EHeroStatType_CounterHelixHeroProcCount: _ClassVar[EHeroStatType]
    k_EHeroStatType_CounterHelixHeroesHitAverage: _ClassVar[EHeroStatType]
    k_EHeroStatType_CounterHelixOtherUnitsHitCount: _ClassVar[EHeroStatType]
    k_EHeroStatType_CullingBladeCastCount: _ClassVar[EHeroStatType]
    k_EHeroStatType_CullingBladeKillCount: _ClassVar[EHeroStatType]
    k_EHeroStatType_CullingBladeAverageHealthCulled: _ClassVar[EHeroStatType]
    k_EHeroStatType_CullingBladeAverageDamageAvailable: _ClassVar[EHeroStatType]
    k_EHeroStatType_CullingBladeHeroBuffAverage: _ClassVar[EHeroStatType]

class EPlayerVoiceListenState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    kPVLS_None: _ClassVar[EPlayerVoiceListenState]
    kPVLS_DeniedChatBanned: _ClassVar[EPlayerVoiceListenState]
    kPVLS_DeniedPartner: _ClassVar[EPlayerVoiceListenState]
    kPVLS_DeniedHLTVTalkerNotSpectator: _ClassVar[EPlayerVoiceListenState]
    kPVLS_DeniedHLTVNoTalkerPlayerID: _ClassVar[EPlayerVoiceListenState]
    kPVLS_DeniedHLTVTalkerNotBroadcaster: _ClassVar[EPlayerVoiceListenState]
    kPVLS_DeniedTeamSpectator: _ClassVar[EPlayerVoiceListenState]
    kPVLS_DeniedStudent: _ClassVar[EPlayerVoiceListenState]
    kPVLS_DeniedPrivateCoach: _ClassVar[EPlayerVoiceListenState]
    kPVLS_Denied: _ClassVar[EPlayerVoiceListenState]
    kPVLS_AllowHLTVTalkerIsBroadcaster: _ClassVar[EPlayerVoiceListenState]
    kPVLS_AllowCoBroadcaster: _ClassVar[EPlayerVoiceListenState]
    kPVLS_AllowAllChat: _ClassVar[EPlayerVoiceListenState]
    kPVLS_AllowStudentToCoach: _ClassVar[EPlayerVoiceListenState]
    kPVLS_AllowFellowStudent: _ClassVar[EPlayerVoiceListenState]
    kPVLS_AllowTalkerIsCoach: _ClassVar[EPlayerVoiceListenState]
    kPVLS_AllowCoachHearTeam: _ClassVar[EPlayerVoiceListenState]
    kPVLS_AllowSameTeam: _ClassVar[EPlayerVoiceListenState]
    kPVLS_AllowShowcase: _ClassVar[EPlayerVoiceListenState]
    kPVLS_AllowPrivateCoach: _ClassVar[EPlayerVoiceListenState]

class EProjectionEvent(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ePE_FirstBlood: _ClassVar[EProjectionEvent]
    ePE_Killstreak_godlike: _ClassVar[EProjectionEvent]

DOTA_UM_AddUnitToSelection: EDotaUserMessages
DOTA_UM_AIDebugLine: EDotaUserMessages
DOTA_UM_ChatEvent: EDotaUserMessages
DOTA_UM_CombatHeroPositions: EDotaUserMessages
DOTA_UM_CombatLogData: EDotaUserMessages
DOTA_UM_CombatLogBulkData: EDotaUserMessages
DOTA_UM_CreateLinearProjectile: EDotaUserMessages
DOTA_UM_DestroyLinearProjectile: EDotaUserMessages
DOTA_UM_DodgeTrackingProjectiles: EDotaUserMessages
DOTA_UM_GlobalLightColor: EDotaUserMessages
DOTA_UM_GlobalLightDirection: EDotaUserMessages
DOTA_UM_InvalidCommand: EDotaUserMessages
DOTA_UM_LocationPing: EDotaUserMessages
DOTA_UM_MapLine: EDotaUserMessages
DOTA_UM_MiniKillCamInfo: EDotaUserMessages
DOTA_UM_MinimapDebugPoint: EDotaUserMessages
DOTA_UM_MinimapEvent: EDotaUserMessages
DOTA_UM_NevermoreRequiem: EDotaUserMessages
DOTA_UM_OverheadEvent: EDotaUserMessages
DOTA_UM_SetNextAutobuyItem: EDotaUserMessages
DOTA_UM_SharedCooldown: EDotaUserMessages
DOTA_UM_SpectatorPlayerClick: EDotaUserMessages
DOTA_UM_TutorialTipInfo: EDotaUserMessages
DOTA_UM_UnitEvent: EDotaUserMessages
DOTA_UM_ParticleManager: EDotaUserMessages
DOTA_UM_BotChat: EDotaUserMessages
DOTA_UM_HudError: EDotaUserMessages
DOTA_UM_ItemPurchased: EDotaUserMessages
DOTA_UM_Ping: EDotaUserMessages
DOTA_UM_ItemFound: EDotaUserMessages
DOTA_UM_CharacterSpeakConcept: EDotaUserMessages
DOTA_UM_SwapVerify: EDotaUserMessages
DOTA_UM_WorldLine: EDotaUserMessages
DOTA_UM_TournamentDrop: EDotaUserMessages
DOTA_UM_ItemAlert: EDotaUserMessages
DOTA_UM_HalloweenDrops: EDotaUserMessages
DOTA_UM_ChatWheel: EDotaUserMessages
DOTA_UM_ReceivedXmasGift: EDotaUserMessages
DOTA_UM_UpdateSharedContent: EDotaUserMessages
DOTA_UM_TutorialRequestExp: EDotaUserMessages
DOTA_UM_TutorialPingMinimap: EDotaUserMessages
DOTA_UM_GamerulesStateChanged: EDotaUserMessages
DOTA_UM_ShowSurvey: EDotaUserMessages
DOTA_UM_TutorialFade: EDotaUserMessages
DOTA_UM_AddQuestLogEntry: EDotaUserMessages
DOTA_UM_SendStatPopup: EDotaUserMessages
DOTA_UM_TutorialFinish: EDotaUserMessages
DOTA_UM_SendRoshanPopup: EDotaUserMessages
DOTA_UM_SendGenericToolTip: EDotaUserMessages
DOTA_UM_SendFinalGold: EDotaUserMessages
DOTA_UM_CustomMsg: EDotaUserMessages
DOTA_UM_CoachHUDPing: EDotaUserMessages
DOTA_UM_ClientLoadGridNav: EDotaUserMessages
DOTA_UM_TE_Projectile: EDotaUserMessages
DOTA_UM_TE_ProjectileLoc: EDotaUserMessages
DOTA_UM_TE_DotaBloodImpact: EDotaUserMessages
DOTA_UM_TE_UnitAnimation: EDotaUserMessages
DOTA_UM_TE_UnitAnimationEnd: EDotaUserMessages
DOTA_UM_AbilityPing: EDotaUserMessages
DOTA_UM_ShowGenericPopup: EDotaUserMessages
DOTA_UM_VoteStart: EDotaUserMessages
DOTA_UM_VoteUpdate: EDotaUserMessages
DOTA_UM_VoteEnd: EDotaUserMessages
DOTA_UM_BoosterState: EDotaUserMessages
DOTA_UM_WillPurchaseAlert: EDotaUserMessages
DOTA_UM_TutorialMinimapPosition: EDotaUserMessages
DOTA_UM_AbilitySteal: EDotaUserMessages
DOTA_UM_CourierKilledAlert: EDotaUserMessages
DOTA_UM_EnemyItemAlert: EDotaUserMessages
DOTA_UM_StatsMatchDetails: EDotaUserMessages
DOTA_UM_MiniTaunt: EDotaUserMessages
DOTA_UM_BuyBackStateAlert: EDotaUserMessages
DOTA_UM_SpeechBubble: EDotaUserMessages
DOTA_UM_CustomHeaderMessage: EDotaUserMessages
DOTA_UM_QuickBuyAlert: EDotaUserMessages
DOTA_UM_StatsHeroDetails: EDotaUserMessages
DOTA_UM_PredictionResult: EDotaUserMessages
DOTA_UM_ModifierAlert: EDotaUserMessages
DOTA_UM_HPManaAlert: EDotaUserMessages
DOTA_UM_GlyphAlert: EDotaUserMessages
DOTA_UM_BeastChat: EDotaUserMessages
DOTA_UM_SpectatorPlayerUnitOrders: EDotaUserMessages
DOTA_UM_CustomHudElement_Create: EDotaUserMessages
DOTA_UM_CustomHudElement_Modify: EDotaUserMessages
DOTA_UM_CustomHudElement_Destroy: EDotaUserMessages
DOTA_UM_CompendiumState: EDotaUserMessages
DOTA_UM_ProjectionAbility: EDotaUserMessages
DOTA_UM_ProjectionEvent: EDotaUserMessages
DOTA_UM_CombatLogDataHLTV: EDotaUserMessages
DOTA_UM_XPAlert: EDotaUserMessages
DOTA_UM_UpdateQuestProgress: EDotaUserMessages
DOTA_UM_MatchMetadata: EDotaUserMessages
DOTA_UM_MatchDetails: EDotaUserMessages
DOTA_UM_QuestStatus: EDotaUserMessages
DOTA_UM_SuggestHeroPick: EDotaUserMessages
DOTA_UM_SuggestHeroRole: EDotaUserMessages
DOTA_UM_KillcamDamageTaken: EDotaUserMessages
DOTA_UM_SelectPenaltyGold: EDotaUserMessages
DOTA_UM_RollDiceResult: EDotaUserMessages
DOTA_UM_FlipCoinResult: EDotaUserMessages
DOTA_UM_RequestItemSuggestions: EDotaUserMessages
DOTA_UM_TeamCaptainChanged: EDotaUserMessages
DOTA_UM_SendRoshanSpectatorPhase: EDotaUserMessages
DOTA_UM_ChatWheelCooldown: EDotaUserMessages
DOTA_UM_DismissAllStatPopups: EDotaUserMessages
DOTA_UM_TE_DestroyProjectile: EDotaUserMessages
DOTA_UM_HeroRelicProgress: EDotaUserMessages
DOTA_UM_AbilityDraftRequestAbility: EDotaUserMessages
DOTA_UM_ItemSold: EDotaUserMessages
DOTA_UM_DamageReport: EDotaUserMessages
DOTA_UM_SalutePlayer: EDotaUserMessages
DOTA_UM_TipAlert: EDotaUserMessages
DOTA_UM_ReplaceQueryUnit: EDotaUserMessages
DOTA_UM_EmptyTeleportAlert: EDotaUserMessages
DOTA_UM_MarsArenaOfBloodAttack: EDotaUserMessages
DOTA_UM_ESArcanaCombo: EDotaUserMessages
DOTA_UM_ESArcanaComboSummary: EDotaUserMessages
DOTA_UM_HighFiveLeftHanging: EDotaUserMessages
DOTA_UM_HighFiveCompleted: EDotaUserMessages
DOTA_UM_ShovelUnearth: EDotaUserMessages
DOTA_UM_RadarAlert: EDotaUserMessages
DOTA_UM_AllStarEvent: EDotaUserMessages
DOTA_UM_TalentTreeAlert: EDotaUserMessages
DOTA_UM_QueuedOrderRemoved: EDotaUserMessages
DOTA_UM_DebugChallenge: EDotaUserMessages
DOTA_UM_OMArcanaCombo: EDotaUserMessages
DOTA_UM_FoundNeutralItem: EDotaUserMessages
DOTA_UM_OutpostCaptured: EDotaUserMessages
DOTA_UM_OutpostGrantedXP: EDotaUserMessages
DOTA_UM_MoveCameraToUnit: EDotaUserMessages
DOTA_UM_PauseMinigameData: EDotaUserMessages
DOTA_UM_VersusScene_PlayerBehavior: EDotaUserMessages
DOTA_UM_QoP_ArcanaSummary: EDotaUserMessages
DOTA_UM_HotPotato_Created: EDotaUserMessages
DOTA_UM_HotPotato_Exploded: EDotaUserMessages
DOTA_UM_WK_Arcana_Progress: EDotaUserMessages
DOTA_UM_GuildChallenge_Progress: EDotaUserMessages
DOTA_UM_WRArcanaProgress: EDotaUserMessages
DOTA_UM_WRArcanaSummary: EDotaUserMessages
DOTA_UM_EmptyItemSlotAlert: EDotaUserMessages
DOTA_UM_AghsStatusAlert: EDotaUserMessages
DOTA_UM_PingConfirmation: EDotaUserMessages
DOTA_UM_MutedPlayers: EDotaUserMessages
DOTA_UM_ContextualTip: EDotaUserMessages
DOTA_UM_ChatMessage: EDotaUserMessages
DOTA_UM_NeutralCampAlert: EDotaUserMessages
DOTA_UM_RockPaperScissorsStarted: EDotaUserMessages
DOTA_UM_RockPaperScissorsFinished: EDotaUserMessages
DOTA_UM_DuelOpponentKilled: EDotaUserMessages
DOTA_UM_DuelAccepted: EDotaUserMessages
DOTA_UM_DuelRequested: EDotaUserMessages
DOTA_UM_MuertaReleaseEvent_AssignedTargetKilled: EDotaUserMessages
DOTA_UM_PlayerDraftSuggestPick: EDotaUserMessages
DOTA_UM_PlayerDraftPick: EDotaUserMessages
DOTA_UM_UpdateLinearProjectileCPData: EDotaUserMessages
DOTA_UM_GiftPlayer: EDotaUserMessages
DOTA_UM_FacetPing: EDotaUserMessages
DOTA_UM_InnatePing: EDotaUserMessages
DOTA_UM_RoshanTimer: EDotaUserMessages
DOTA_UM_NeutralCraftAvailable: EDotaUserMessages
DOTA_UM_TimerAlert: EDotaUserMessages
DOTA_UM_MadstoneAlert: EDotaUserMessages
DOTA_UM_CourierLeftFountainAlert: EDotaUserMessages
DOTA_UM_MonsterHunter_InvestigationsAvailable: EDotaUserMessages
DOTA_UM_MonsterHunter_InvestigationGameState: EDotaUserMessages
DOTA_UM_MonsterHunter_HuntAlert: EDotaUserMessages
DOTA_UM_TormentorTimer: EDotaUserMessages
DOTA_UM_KillEffect: EDotaUserMessages
CHAT_MESSAGE_INVALID: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_HERO_KILL: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_HERO_DENY: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_BARRACKS_KILL: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_TOWER_KILL: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_TOWER_DENY: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_FIRSTBLOOD: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_STREAK_KILL: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_BUYBACK: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_AEGIS: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_ROSHAN_KILL: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_COURIER_LOST: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_COURIER_RESPAWNED: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_GLYPH_USED: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_ITEM_PURCHASE: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_CONNECT: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_DISCONNECT: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_DISCONNECT_WAIT_FOR_RECONNECT: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_DISCONNECT_TIME_REMAINING: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_DISCONNECT_TIME_REMAINING_PLURAL: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_RECONNECT: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_PLAYER_LEFT: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_SAFE_TO_LEAVE: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_RUNE_PICKUP: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_RUNE_BOTTLE: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_RUNE_DENY: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_INTHEBAG: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_SECRETSHOP: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_ITEM_AUTOPURCHASED: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_ITEMS_COMBINED: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_SUPER_CREEPS: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_CANT_USE_ACTION_ITEM: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_CANTPAUSE: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_NOPAUSESLEFT: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_CANTPAUSEYET: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_PAUSED: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_UNPAUSE_COUNTDOWN: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_UNPAUSED: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_AUTO_UNPAUSED: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_YOUPAUSED: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_CANTUNPAUSETEAM: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_VOICE_TEXT_BANNED: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_SPECTATORS_WATCHING_THIS_GAME: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_REPORT_REMINDER: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_ECON_ITEM: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_TAUNT: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_RANDOM: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_RD_TURN: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_DROP_RATE_BONUS: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_NO_BATTLE_POINTS: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_DENIED_AEGIS: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_INFORMATIONAL: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_AEGIS_STOLEN: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_ROSHAN_CANDY: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_ITEM_GIFTED: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_HERO_KILL_WITH_GREEVIL: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_HOLDOUT_TOWER_DESTROYED: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_HOLDOUT_WALL_DESTROYED: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_HOLDOUT_WALL_FINISHED: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_PLAYER_LEFT_LIMITED_HERO: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_ABANDON_LIMITED_HERO_EXPLANATION: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_DISCONNECT_LIMITED_HERO: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_LOW_PRIORITY_COMPLETED_EXPLANATION: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_RECRUITMENT_DROP_RATE_BONUS: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_FROSTIVUS_SHINING_BOOSTER_ACTIVE: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_PLAYER_LEFT_AFK: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_PLAYER_LEFT_DISCONNECTED_TOO_LONG: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_PLAYER_ABANDONED: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_PLAYER_ABANDONED_AFK: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_PLAYER_ABANDONED_DISCONNECTED_TOO_LONG: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_WILL_NOT_BE_SCORED: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_WILL_NOT_BE_SCORED_RANKED: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_WILL_NOT_BE_SCORED_NETWORK: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_WILL_NOT_BE_SCORED_NETWORK_RANKED: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_CAN_QUIT_WITHOUT_ABANDON: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_RANKED_GAME_STILL_SCORED_LEAVERS_GET_LOSS: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_ABANDON_RANKED_BEFORE_FIRST_BLOOD_PARTY: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_COMPENDIUM_LEVEL: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_VICTORY_PREDICTION_STREAK: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_ASSASSIN_ANNOUNCE: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_ASSASSIN_SUCCESS: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_ASSASSIN_DENIED: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_VICTORY_PREDICTION_SINGLE_USER_CONFIRM: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_EFFIGY_KILL: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_VOICE_TEXT_BANNED_OVERFLOW: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_YEAR_BEAST_KILLED: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_PAUSE_COUNTDOWN: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_COINS_WAGERED: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_HERO_NOMINATED_BAN: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_HERO_BANNED: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_HERO_BAN_COUNT: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_RIVER_PAINTED: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_SCAN_USED: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_SHRINE_KILLED: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_WAGER_TOKEN_SPENT: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_RANK_WAGER: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_NEW_PLAYER_REMINDER: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_OBSERVER_WARD_KILLED: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_SENTRY_WARD_KILLED: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_ITEM_PLACED_IN_NEUTRAL_STASH: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_HERO_CHOICE_INVALID: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_BOUNTY: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_ABILITY_DRAFT_START: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_HERO_FOUND_CANDY: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_ABILITY_DRAFT_RANDOMED: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_PRIVATE_COACH_CONNECTED: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_CANT_PAUSE_TOO_EARLY: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_HERO_KILL_WITH_PENGUIN: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_MINIBOSS_KILL: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_PLAYER_IN_GAME_BAN_TEXT: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_BANNER_PLANTED: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_ALCHEMIST_GRANTED_SCEPTER: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_PROTECTOR_SPAWNED: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_CRAFTING_XP: DOTA_CHAT_MESSAGE
CHAT_MESSAGE_ROSHAN_ROAR: DOTA_CHAT_MESSAGE
NO_BATTLE_POINTS_WRONG_LOBBY_TYPE: DOTA_NO_BATTLE_POINTS_REASONS
NO_BATTLE_POINTS_PRACTICE_BOTS: DOTA_NO_BATTLE_POINTS_REASONS
NO_BATTLE_POINTS_CHEATS_ENABLED: DOTA_NO_BATTLE_POINTS_REASONS
NO_BATTLE_POINTS_LOW_PRIORITY: DOTA_NO_BATTLE_POINTS_REASONS
INFO_COOP_BATTLE_POINTS_RULES: DOTA_CHAT_INFORMATIONAL
INFO_FROSTIVUS_ABANDON_REMINDER: DOTA_CHAT_INFORMATIONAL
INFO_RANKED_REMINDER: DOTA_CHAT_INFORMATIONAL
INFO_COOP_LOW_PRIORITY_PASSIVE_REMINDER: DOTA_CHAT_INFORMATIONAL
INFO_CUSTOM_GAME_PENALTY_REMINDER: DOTA_CHAT_INFORMATIONAL
ABILITY_PING_READY: DOTA_ABILITY_PING_TYPE
ABILITY_PING_MANA: DOTA_ABILITY_PING_TYPE
ABILITY_PING_COOLDOWN: DOTA_ABILITY_PING_TYPE
ABILITY_PING_ENEMY: DOTA_ABILITY_PING_TYPE
ABILITY_PING_UNLEARNED: DOTA_ABILITY_PING_TYPE
ABILITY_PING_INBACKPACK: DOTA_ABILITY_PING_TYPE
ABILITY_PING_INSTASH: DOTA_ABILITY_PING_TYPE
ABILITY_PING_ONCOURIER: DOTA_ABILITY_PING_TYPE
ABILITY_PING_ALLY: DOTA_ABILITY_PING_TYPE
ABILITY_PING_LEARN_READY: DOTA_ABILITY_PING_TYPE
ABILITY_PING_WILL_LEARN: DOTA_ABILITY_PING_TYPE
ABILITY_PING_FUTURE_LEARN: DOTA_ABILITY_PING_TYPE
ABILITY_PING_NEUTRAL_OFFER: DOTA_ABILITY_PING_TYPE
ABILITY_PING_NEUTRAL_REQUEST: DOTA_ABILITY_PING_TYPE
ABILITY_PING_NEUTRAL_EQUIP: DOTA_ABILITY_PING_TYPE
ABILITY_PING_INCOURIERBACKPACK: DOTA_ABILITY_PING_TYPE
DOTA_REPLAY_STATE_EVENT_GAME_START: DOTA_REPLAY_STATE_EVENT
DOTA_REPLAY_STATE_EVENT_STARTING_HORN: DOTA_REPLAY_STATE_EVENT
DOTA_REPLAY_STATE_EVENT_FIRST_BLOOD: DOTA_REPLAY_STATE_EVENT
DOTA_REPLAY_STATE_EVENT_SHOWCASE: DOTA_REPLAY_STATE_EVENT
DOTA_REPLAY_STATE_EVENT_POST_GAME: DOTA_REPLAY_STATE_EVENT
DOTA_REPLAY_STATE_EVENT_WAIT_FOR_MAP: DOTA_REPLAY_STATE_EVENT
DOTA_UNIT_SPEECH: EDotaEntityMessages
DOTA_UNIT_SPEECH_MUTE: EDotaEntityMessages
DOTA_UNIT_ADD_GESTURE: EDotaEntityMessages
DOTA_UNIT_REMOVE_GESTURE: EDotaEntityMessages
DOTA_UNIT_REMOVE_ALL_GESTURES: EDotaEntityMessages
DOTA_UNIT_FADE_GESTURE: EDotaEntityMessages
DOTA_UNIT_SPEECH_CLIENTSIDE_RULES: EDotaEntityMessages
OVERHEAD_ALERT_GOLD: DOTA_OVERHEAD_ALERT
OVERHEAD_ALERT_DENY: DOTA_OVERHEAD_ALERT
OVERHEAD_ALERT_CRITICAL: DOTA_OVERHEAD_ALERT
OVERHEAD_ALERT_XP: DOTA_OVERHEAD_ALERT
OVERHEAD_ALERT_BONUS_SPELL_DAMAGE: DOTA_OVERHEAD_ALERT
OVERHEAD_ALERT_MISS: DOTA_OVERHEAD_ALERT
OVERHEAD_ALERT_DAMAGE: DOTA_OVERHEAD_ALERT
OVERHEAD_ALERT_EVADE: DOTA_OVERHEAD_ALERT
OVERHEAD_ALERT_BLOCK: DOTA_OVERHEAD_ALERT
OVERHEAD_ALERT_BONUS_POISON_DAMAGE: DOTA_OVERHEAD_ALERT
OVERHEAD_ALERT_HEAL: DOTA_OVERHEAD_ALERT
OVERHEAD_ALERT_MANA_ADD: DOTA_OVERHEAD_ALERT
OVERHEAD_ALERT_MANA_LOSS: DOTA_OVERHEAD_ALERT
OVERHEAD_ALERT_MAGICAL_BLOCK: DOTA_OVERHEAD_ALERT
OVERHEAD_ALERT_INCOMING_DAMAGE: DOTA_OVERHEAD_ALERT
OVERHEAD_ALERT_OUTGOING_DAMAGE: DOTA_OVERHEAD_ALERT
OVERHEAD_ALERT_DISABLE_RESIST: DOTA_OVERHEAD_ALERT
OVERHEAD_ALERT_DEATH: DOTA_OVERHEAD_ALERT
OVERHEAD_ALERT_BLOCKED: DOTA_OVERHEAD_ALERT
OVERHEAD_ALERT_ITEM_RECEIVED: DOTA_OVERHEAD_ALERT
OVERHEAD_ALERT_SHARD: DOTA_OVERHEAD_ALERT
OVERHEAD_ALERT_DEADLY_BLOW: DOTA_OVERHEAD_ALERT
OVERHEAD_ALERT_FORCE_MISS: DOTA_OVERHEAD_ALERT
OVERHEAD_ALERT_AEGIS: DOTA_OVERHEAD_ALERT
OVERHEAD_ALERT_DISPEL: DOTA_OVERHEAD_ALERT
k_SRSP_ROSHAN_ALIVE: DOTA_ROSHAN_PHASE
k_SRSP_ROSHAN_BASE_TIMER: DOTA_ROSHAN_PHASE
k_SRSP_ROSHAN_VISIBLE_TIMER: DOTA_ROSHAN_PHASE
DOTA_POSITION_NONE: DOTA_POSITION_CATEGORY
DOTA_POSITION_BOTTOM_LANE: DOTA_POSITION_CATEGORY
DOTA_POSITION_MID_LANE: DOTA_POSITION_CATEGORY
DOTA_POSITION_TOP_LANE: DOTA_POSITION_CATEGORY
DOTA_POSITION_RADIANT_JUNGLE: DOTA_POSITION_CATEGORY
DOTA_POSITION_DIRE_JUNGLE: DOTA_POSITION_CATEGORY
DOTA_POSITION_RADIANT_ANCIENTS: DOTA_POSITION_CATEGORY
DOTA_POSITION_DIRE_ANCIENTS: DOTA_POSITION_CATEGORY
DOTA_POSITION_RADIANT_SECRET_SHOP: DOTA_POSITION_CATEGORY
DOTA_POSITION_DIRE_SECRET_SHOP: DOTA_POSITION_CATEGORY
DOTA_POSITION_RIVER: DOTA_POSITION_CATEGORY
DOTA_POSITION_ROSHAN_PIT: DOTA_POSITION_CATEGORY
DOTA_POSITION_RADIANT_BASE: DOTA_POSITION_CATEGORY
DOTA_POSITION_DIRE_BASE: DOTA_POSITION_CATEGORY
DOTA_POSITION_FOUNTAIN: DOTA_POSITION_CATEGORY
DOTA_POSITION_OTHER: DOTA_POSITION_CATEGORY
DOTA_ABILITY_TARGET_NONE: DOTA_ABILITY_TARGET_TYPE
DOTA_ABILITY_TARGET_SELF: DOTA_ABILITY_TARGET_TYPE
DOTA_ABILITY_TARGET_ALLY_HERO: DOTA_ABILITY_TARGET_TYPE
DOTA_ABILITY_TARGET_ALLY_CREEP: DOTA_ABILITY_TARGET_TYPE
DOTA_ABILITY_TARGET_ENEMY_HERO: DOTA_ABILITY_TARGET_TYPE
DOTA_ABILITY_TARGET_ENEMY_CREEP: DOTA_ABILITY_TARGET_TYPE
k_EHeroStatType_None: EHeroStatType
k_EHeroStatType_AxeTotalDamage: EHeroStatType
k_EHeroStatType_BattleHungerDamage: EHeroStatType
k_EHeroStatType_CounterHelixDamage: EHeroStatType
k_EHeroStatType_CullingBladeDamage: EHeroStatType
k_EHeroStatType_BerserkersCallCastCount: EHeroStatType
k_EHeroStatType_BerserkersCallHeroesHitAverage: EHeroStatType
k_EHeroStatType_BerserkersCallOtherUnitsHit: EHeroStatType
k_EHeroStatType_BerserkersCallHeroAttacksTaken: EHeroStatType
k_EHeroStatType_BerserkersCallOtherAttacksTaken: EHeroStatType
k_EHeroStatType_BattleHungerCastCount: EHeroStatType
k_EHeroStatType_BattleHungerPotentialDuration: EHeroStatType
k_EHeroStatType_BattleHungerAverageDuration: EHeroStatType
k_EHeroStatType_CounterHelixProcCount: EHeroStatType
k_EHeroStatType_CounterHelixHeroProcCount: EHeroStatType
k_EHeroStatType_CounterHelixHeroesHitAverage: EHeroStatType
k_EHeroStatType_CounterHelixOtherUnitsHitCount: EHeroStatType
k_EHeroStatType_CullingBladeCastCount: EHeroStatType
k_EHeroStatType_CullingBladeKillCount: EHeroStatType
k_EHeroStatType_CullingBladeAverageHealthCulled: EHeroStatType
k_EHeroStatType_CullingBladeAverageDamageAvailable: EHeroStatType
k_EHeroStatType_CullingBladeHeroBuffAverage: EHeroStatType
kPVLS_None: EPlayerVoiceListenState
kPVLS_DeniedChatBanned: EPlayerVoiceListenState
kPVLS_DeniedPartner: EPlayerVoiceListenState
kPVLS_DeniedHLTVTalkerNotSpectator: EPlayerVoiceListenState
kPVLS_DeniedHLTVNoTalkerPlayerID: EPlayerVoiceListenState
kPVLS_DeniedHLTVTalkerNotBroadcaster: EPlayerVoiceListenState
kPVLS_DeniedTeamSpectator: EPlayerVoiceListenState
kPVLS_DeniedStudent: EPlayerVoiceListenState
kPVLS_DeniedPrivateCoach: EPlayerVoiceListenState
kPVLS_Denied: EPlayerVoiceListenState
kPVLS_AllowHLTVTalkerIsBroadcaster: EPlayerVoiceListenState
kPVLS_AllowCoBroadcaster: EPlayerVoiceListenState
kPVLS_AllowAllChat: EPlayerVoiceListenState
kPVLS_AllowStudentToCoach: EPlayerVoiceListenState
kPVLS_AllowFellowStudent: EPlayerVoiceListenState
kPVLS_AllowTalkerIsCoach: EPlayerVoiceListenState
kPVLS_AllowCoachHearTeam: EPlayerVoiceListenState
kPVLS_AllowSameTeam: EPlayerVoiceListenState
kPVLS_AllowShowcase: EPlayerVoiceListenState
kPVLS_AllowPrivateCoach: EPlayerVoiceListenState
ePE_FirstBlood: EProjectionEvent
ePE_Killstreak_godlike: EProjectionEvent

class CDOTAUserMsg_AIDebugLine(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: str | None = ...) -> None: ...

class CDOTAUserMsg_Ping(_message.Message):
    __slots__ = ("ping", "loss")
    PING_FIELD_NUMBER: _ClassVar[int]
    LOSS_FIELD_NUMBER: _ClassVar[int]
    ping: int
    loss: int
    def __init__(self, ping: int | None = ..., loss: int | None = ...) -> None: ...

class CDOTAUserMsg_SwapVerify(_message.Message):
    __slots__ = ("player_id",)
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    def __init__(self, player_id: int | None = ...) -> None: ...

class CDOTAUserMsg_ChatEvent(_message.Message):
    __slots__ = (
        "type",
        "value",
        "playerid_1",
        "playerid_2",
        "playerid_3",
        "playerid_4",
        "playerid_5",
        "playerid_6",
        "value2",
        "value3",
        "time",
    )
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    PLAYERID_1_FIELD_NUMBER: _ClassVar[int]
    PLAYERID_2_FIELD_NUMBER: _ClassVar[int]
    PLAYERID_3_FIELD_NUMBER: _ClassVar[int]
    PLAYERID_4_FIELD_NUMBER: _ClassVar[int]
    PLAYERID_5_FIELD_NUMBER: _ClassVar[int]
    PLAYERID_6_FIELD_NUMBER: _ClassVar[int]
    VALUE2_FIELD_NUMBER: _ClassVar[int]
    VALUE3_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    type: DOTA_CHAT_MESSAGE
    value: int
    playerid_1: int
    playerid_2: int
    playerid_3: int
    playerid_4: int
    playerid_5: int
    playerid_6: int
    value2: int
    value3: int
    time: float
    def __init__(
        self,
        type: DOTA_CHAT_MESSAGE | str | None = ...,
        value: int | None = ...,
        playerid_1: int | None = ...,
        playerid_2: int | None = ...,
        playerid_3: int | None = ...,
        playerid_4: int | None = ...,
        playerid_5: int | None = ...,
        playerid_6: int | None = ...,
        value2: int | None = ...,
        value3: int | None = ...,
        time: float | None = ...,
    ) -> None: ...

class CDOTAUserMsg_BotChat(_message.Message):
    __slots__ = ("player_id", "message", "target", "team_only")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    TEAM_ONLY_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    message: str
    target: str
    team_only: bool
    def __init__(
        self,
        player_id: int | None = ...,
        message: str | None = ...,
        target: str | None = ...,
        team_only: bool = ...,
    ) -> None: ...

class CDOTAUserMsg_CombatHeroPositions(_message.Message):
    __slots__ = ("index", "time", "world_pos", "health")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    WORLD_POS_FIELD_NUMBER: _ClassVar[int]
    HEALTH_FIELD_NUMBER: _ClassVar[int]
    index: int
    time: int
    world_pos: _networkbasetypes_pb2.CMsgVector2D
    health: int
    def __init__(
        self,
        index: int | None = ...,
        time: int | None = ...,
        world_pos: _networkbasetypes_pb2.CMsgVector2D | _Mapping | None = ...,
        health: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_CombatLogBulkData(_message.Message):
    __slots__ = ("combat_entries", "timestamp", "duration", "player_id", "request_time")
    COMBAT_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_TIME_FIELD_NUMBER: _ClassVar[int]
    combat_entries: _containers.RepeatedCompositeFieldContainer[
        _dota_shared_enums_pb2.CMsgDOTACombatLogEntry
    ]
    timestamp: float
    duration: float
    player_id: int
    request_time: float
    def __init__(
        self,
        combat_entries: _Iterable[_dota_shared_enums_pb2.CMsgDOTACombatLogEntry | _Mapping]
        | None = ...,
        timestamp: float | None = ...,
        duration: float | None = ...,
        player_id: int | None = ...,
        request_time: float | None = ...,
    ) -> None: ...

class CDOTAUserMsg_ProjectileParticleCPData(_message.Message):
    __slots__ = ("control_point", "vector")
    CONTROL_POINT_FIELD_NUMBER: _ClassVar[int]
    VECTOR_FIELD_NUMBER: _ClassVar[int]
    control_point: int
    vector: _networkbasetypes_pb2.CMsgVector
    def __init__(
        self,
        control_point: int | None = ...,
        vector: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
    ) -> None: ...

class CDOTAUserMsg_UpdateLinearProjectileCPData(_message.Message):
    __slots__ = ("handle", "control_point", "vector")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    CONTROL_POINT_FIELD_NUMBER: _ClassVar[int]
    VECTOR_FIELD_NUMBER: _ClassVar[int]
    handle: int
    control_point: int
    vector: _networkbasetypes_pb2.CMsgVector
    def __init__(
        self,
        handle: int | None = ...,
        control_point: int | None = ...,
        vector: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
    ) -> None: ...

class CDOTAUserMsg_MiniKillCamInfo(_message.Message):
    __slots__ = ("attackers",)
    class Attacker(_message.Message):
        __slots__ = ("attacker", "total_damage", "abilities", "attacker_name")
        class Ability(_message.Message):
            __slots__ = ("ability_id", "damage")
            ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
            DAMAGE_FIELD_NUMBER: _ClassVar[int]
            ability_id: int
            damage: int
            def __init__(self, ability_id: int | None = ..., damage: int | None = ...) -> None: ...

        ATTACKER_FIELD_NUMBER: _ClassVar[int]
        TOTAL_DAMAGE_FIELD_NUMBER: _ClassVar[int]
        ABILITIES_FIELD_NUMBER: _ClassVar[int]
        ATTACKER_NAME_FIELD_NUMBER: _ClassVar[int]
        attacker: int
        total_damage: int
        abilities: _containers.RepeatedCompositeFieldContainer[
            CDOTAUserMsg_MiniKillCamInfo.Attacker.Ability
        ]
        attacker_name: str
        def __init__(
            self,
            attacker: int | None = ...,
            total_damage: int | None = ...,
            abilities: _Iterable[CDOTAUserMsg_MiniKillCamInfo.Attacker.Ability | _Mapping]
            | None = ...,
            attacker_name: str | None = ...,
        ) -> None: ...

    ATTACKERS_FIELD_NUMBER: _ClassVar[int]
    attackers: _containers.RepeatedCompositeFieldContainer[CDOTAUserMsg_MiniKillCamInfo.Attacker]
    def __init__(
        self, attackers: _Iterable[CDOTAUserMsg_MiniKillCamInfo.Attacker | _Mapping] | None = ...
    ) -> None: ...

class CDOTAUserMsg_GlobalLightColor(_message.Message):
    __slots__ = ("color", "duration")
    COLOR_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    color: int
    duration: float
    def __init__(self, color: int | None = ..., duration: float | None = ...) -> None: ...

class CDOTAUserMsg_GlobalLightDirection(_message.Message):
    __slots__ = ("direction", "duration")
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    direction: _networkbasetypes_pb2.CMsgVector
    duration: float
    def __init__(
        self,
        direction: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
        duration: float | None = ...,
    ) -> None: ...

class CDOTAUserMsg_LocationPing(_message.Message):
    __slots__ = ("player_id", "location_ping")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    LOCATION_PING_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    location_ping: _dota_commonmessages_pb2.CDOTAMsg_LocationPing
    def __init__(
        self,
        player_id: int | None = ...,
        location_ping: _dota_commonmessages_pb2.CDOTAMsg_LocationPing | _Mapping | None = ...,
    ) -> None: ...

class CDOTAUserMsg_PingConfirmation(_message.Message):
    __slots__ = ("player_id_of_original_pinger", "entity_index", "icon_type", "location")
    PLAYER_ID_OF_ORIGINAL_PINGER_FIELD_NUMBER: _ClassVar[int]
    ENTITY_INDEX_FIELD_NUMBER: _ClassVar[int]
    ICON_TYPE_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    player_id_of_original_pinger: int
    entity_index: int
    icon_type: int
    location: _networkbasetypes_pb2.CMsgVector
    def __init__(
        self,
        player_id_of_original_pinger: int | None = ...,
        entity_index: int | None = ...,
        icon_type: int | None = ...,
        location: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
    ) -> None: ...

class CDOTAUserMsg_ItemAlert(_message.Message):
    __slots__ = ("player_id", "item_alert")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_ALERT_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    item_alert: _dota_commonmessages_pb2.CDOTAMsg_ItemAlert
    def __init__(
        self,
        player_id: int | None = ...,
        item_alert: _dota_commonmessages_pb2.CDOTAMsg_ItemAlert | _Mapping | None = ...,
    ) -> None: ...

class CDOTAUserMsg_EnemyItemAlert(_message.Message):
    __slots__ = (
        "player_id",
        "target_player_id",
        "item_ability_id",
        "rune_type",
        "entity_id",
        "item_level",
        "primary_charges",
        "secondary_charges",
    )
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    RUNE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_LEVEL_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_CHARGES_FIELD_NUMBER: _ClassVar[int]
    SECONDARY_CHARGES_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    target_player_id: int
    item_ability_id: int
    rune_type: int
    entity_id: int
    item_level: int
    primary_charges: int
    secondary_charges: int
    def __init__(
        self,
        player_id: int | None = ...,
        target_player_id: int | None = ...,
        item_ability_id: int | None = ...,
        rune_type: int | None = ...,
        entity_id: int | None = ...,
        item_level: int | None = ...,
        primary_charges: int | None = ...,
        secondary_charges: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_ModifierAlert(_message.Message):
    __slots__ = (
        "player_id",
        "class_name",
        "stack_count",
        "is_debuff",
        "target_entindex",
        "seconds_remaining",
    )
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
    STACK_COUNT_FIELD_NUMBER: _ClassVar[int]
    IS_DEBUFF_FIELD_NUMBER: _ClassVar[int]
    TARGET_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    SECONDS_REMAINING_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    class_name: str
    stack_count: int
    is_debuff: bool
    target_entindex: int
    seconds_remaining: float
    def __init__(
        self,
        player_id: int | None = ...,
        class_name: str | None = ...,
        stack_count: int | None = ...,
        is_debuff: bool = ...,
        target_entindex: int | None = ...,
        seconds_remaining: float | None = ...,
    ) -> None: ...

class CDOTAUserMsg_HPManaAlert(_message.Message):
    __slots__ = ("player_id", "target_entindex", "show_raw_values")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    SHOW_RAW_VALUES_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    target_entindex: int
    show_raw_values: bool
    def __init__(
        self,
        player_id: int | None = ...,
        target_entindex: int | None = ...,
        show_raw_values: bool = ...,
    ) -> None: ...

class CDOTAUserMsg_NeutralCampAlert(_message.Message):
    __slots__ = (
        "player_id",
        "spawner_entindex",
        "unit_entindex",
        "stack_count",
        "camp_type",
        "stack_request",
        "stack_intention",
    )
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    SPAWNER_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    UNIT_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    STACK_COUNT_FIELD_NUMBER: _ClassVar[int]
    CAMP_TYPE_FIELD_NUMBER: _ClassVar[int]
    STACK_REQUEST_FIELD_NUMBER: _ClassVar[int]
    STACK_INTENTION_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    spawner_entindex: int
    unit_entindex: int
    stack_count: int
    camp_type: int
    stack_request: bool
    stack_intention: bool
    def __init__(
        self,
        player_id: int | None = ...,
        spawner_entindex: int | None = ...,
        unit_entindex: int | None = ...,
        stack_count: int | None = ...,
        camp_type: int | None = ...,
        stack_request: bool = ...,
        stack_intention: bool = ...,
    ) -> None: ...

class CDOTAUserMsg_GlyphAlert(_message.Message):
    __slots__ = ("player_id", "negative")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    NEGATIVE_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    negative: bool
    def __init__(self, player_id: int | None = ..., negative: bool = ...) -> None: ...

class CDOTAUserMsg_RadarAlert(_message.Message):
    __slots__ = ("player_id", "negative")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    NEGATIVE_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    negative: bool
    def __init__(self, player_id: int | None = ..., negative: bool = ...) -> None: ...

class CDOTAUserMsg_RoshanTimer(_message.Message):
    __slots__ = ("player_id", "negative")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    NEGATIVE_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    negative: bool
    def __init__(self, player_id: int | None = ..., negative: bool = ...) -> None: ...

class CDOTAUserMsg_TormentorTimer(_message.Message):
    __slots__ = ("player_id", "negative")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    NEGATIVE_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    negative: bool
    def __init__(self, player_id: int | None = ..., negative: bool = ...) -> None: ...

class CDOTAUserMsg_WillPurchaseAlert(_message.Message):
    __slots__ = ("item_ability_id", "player_id", "gold_remaining", "suggestion_player_id")
    ITEM_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    GOLD_REMAINING_FIELD_NUMBER: _ClassVar[int]
    SUGGESTION_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    item_ability_id: int
    player_id: int
    gold_remaining: int
    suggestion_player_id: int
    def __init__(
        self,
        item_ability_id: int | None = ...,
        player_id: int | None = ...,
        gold_remaining: int | None = ...,
        suggestion_player_id: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_EmptyTeleportAlert(_message.Message):
    __slots__ = ("source_player_id", "target_player_id", "cooldown_seconds")
    SOURCE_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    COOLDOWN_SECONDS_FIELD_NUMBER: _ClassVar[int]
    source_player_id: int
    target_player_id: int
    cooldown_seconds: int
    def __init__(
        self,
        source_player_id: int | None = ...,
        target_player_id: int | None = ...,
        cooldown_seconds: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_MarsArenaOfBloodAttack(_message.Message):
    __slots__ = ("source_ehandle", "target_ehandle", "warrior_index")
    SOURCE_EHANDLE_FIELD_NUMBER: _ClassVar[int]
    TARGET_EHANDLE_FIELD_NUMBER: _ClassVar[int]
    WARRIOR_INDEX_FIELD_NUMBER: _ClassVar[int]
    source_ehandle: int
    target_ehandle: int
    warrior_index: int
    def __init__(
        self,
        source_ehandle: int | None = ...,
        target_ehandle: int | None = ...,
        warrior_index: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_BuyBackStateAlert(_message.Message):
    __slots__ = ("player_id",)
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    def __init__(self, player_id: int | None = ...) -> None: ...

class CDOTAUserMsg_QuickBuyAlert(_message.Message):
    __slots__ = (
        "player_id",
        "item_ability_id",
        "gold_cost",
        "item_cooldown_seconds",
        "show_buyback",
    )
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    GOLD_COST_FIELD_NUMBER: _ClassVar[int]
    ITEM_COOLDOWN_SECONDS_FIELD_NUMBER: _ClassVar[int]
    SHOW_BUYBACK_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    item_ability_id: int
    gold_cost: int
    item_cooldown_seconds: int
    show_buyback: bool
    def __init__(
        self,
        player_id: int | None = ...,
        item_ability_id: int | None = ...,
        gold_cost: int | None = ...,
        item_cooldown_seconds: int | None = ...,
        show_buyback: bool = ...,
    ) -> None: ...

class CDOTAUserMsg_CourierKilledAlert(_message.Message):
    __slots__ = (
        "team",
        "gold_value",
        "entity_handle",
        "timestamp",
        "lost_items",
        "killer_player_id",
        "owning_player_id",
    )
    class LostItem(_message.Message):
        __slots__ = ("item_ability_id", "quantity")
        ITEM_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
        QUANTITY_FIELD_NUMBER: _ClassVar[int]
        item_ability_id: int
        quantity: int
        def __init__(
            self, item_ability_id: int | None = ..., quantity: int | None = ...
        ) -> None: ...

    TEAM_FIELD_NUMBER: _ClassVar[int]
    GOLD_VALUE_FIELD_NUMBER: _ClassVar[int]
    ENTITY_HANDLE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LOST_ITEMS_FIELD_NUMBER: _ClassVar[int]
    KILLER_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    OWNING_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    team: int
    gold_value: int
    entity_handle: int
    timestamp: int
    lost_items: _containers.RepeatedCompositeFieldContainer[
        CDOTAUserMsg_CourierKilledAlert.LostItem
    ]
    killer_player_id: int
    owning_player_id: int
    def __init__(
        self,
        team: int | None = ...,
        gold_value: int | None = ...,
        entity_handle: int | None = ...,
        timestamp: int | None = ...,
        lost_items: _Iterable[CDOTAUserMsg_CourierKilledAlert.LostItem | _Mapping] | None = ...,
        killer_player_id: int | None = ...,
        owning_player_id: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_MinimapEvent(_message.Message):
    __slots__ = ("event_type", "entity_handle", "x", "y", "duration", "target_entity_handle")
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ENTITY_HANDLE_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    TARGET_ENTITY_HANDLE_FIELD_NUMBER: _ClassVar[int]
    event_type: int
    entity_handle: int
    x: int
    y: int
    duration: int
    target_entity_handle: int
    def __init__(
        self,
        event_type: int | None = ...,
        entity_handle: int | None = ...,
        x: int | None = ...,
        y: int | None = ...,
        duration: int | None = ...,
        target_entity_handle: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_MapLine(_message.Message):
    __slots__ = ("player_id", "mapline")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    MAPLINE_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    mapline: _dota_commonmessages_pb2.CDOTAMsg_MapLine
    def __init__(
        self,
        player_id: int | None = ...,
        mapline: _dota_commonmessages_pb2.CDOTAMsg_MapLine | _Mapping | None = ...,
    ) -> None: ...

class CDOTAUserMsg_MinimapDebugPoint(_message.Message):
    __slots__ = ("location", "color", "size", "duration", "index")
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    location: _networkbasetypes_pb2.CMsgVector
    color: int
    size: int
    duration: float
    index: int
    def __init__(
        self,
        location: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
        color: int | None = ...,
        size: int | None = ...,
        duration: float | None = ...,
        index: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_CreateLinearProjectile(_message.Message):
    __slots__ = (
        "origin",
        "velocity",
        "entindex",
        "particle_index",
        "handle",
        "acceleration",
        "max_speed",
        "fow_radius",
        "sticky_fow_reveal",
        "distance",
        "colorgemcolor",
        "particle_cp_data",
    )
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_FIELD_NUMBER: _ClassVar[int]
    ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    PARTICLE_INDEX_FIELD_NUMBER: _ClassVar[int]
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    MAX_SPEED_FIELD_NUMBER: _ClassVar[int]
    FOW_RADIUS_FIELD_NUMBER: _ClassVar[int]
    STICKY_FOW_REVEAL_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    COLORGEMCOLOR_FIELD_NUMBER: _ClassVar[int]
    PARTICLE_CP_DATA_FIELD_NUMBER: _ClassVar[int]
    origin: _networkbasetypes_pb2.CMsgVector
    velocity: _networkbasetypes_pb2.CMsgVector2D
    entindex: int
    particle_index: int
    handle: int
    acceleration: _networkbasetypes_pb2.CMsgVector2D
    max_speed: float
    fow_radius: float
    sticky_fow_reveal: bool
    distance: float
    colorgemcolor: int
    particle_cp_data: _containers.RepeatedCompositeFieldContainer[
        CDOTAUserMsg_ProjectileParticleCPData
    ]
    def __init__(
        self,
        origin: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
        velocity: _networkbasetypes_pb2.CMsgVector2D | _Mapping | None = ...,
        entindex: int | None = ...,
        particle_index: int | None = ...,
        handle: int | None = ...,
        acceleration: _networkbasetypes_pb2.CMsgVector2D | _Mapping | None = ...,
        max_speed: float | None = ...,
        fow_radius: float | None = ...,
        sticky_fow_reveal: bool = ...,
        distance: float | None = ...,
        colorgemcolor: int | None = ...,
        particle_cp_data: _Iterable[CDOTAUserMsg_ProjectileParticleCPData | _Mapping] | None = ...,
    ) -> None: ...

class CDOTAUserMsg_DestroyLinearProjectile(_message.Message):
    __slots__ = ("handle",)
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    handle: int
    def __init__(self, handle: int | None = ...) -> None: ...

class CDOTAUserMsg_DodgeTrackingProjectiles(_message.Message):
    __slots__ = ("entindex", "attacks_only")
    ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    ATTACKS_ONLY_FIELD_NUMBER: _ClassVar[int]
    entindex: int
    attacks_only: bool
    def __init__(self, entindex: int | None = ..., attacks_only: bool = ...) -> None: ...

class CDOTAUserMsg_SpectatorPlayerClick(_message.Message):
    __slots__ = ("entindex", "order_type", "target_index")
    ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    ORDER_TYPE_FIELD_NUMBER: _ClassVar[int]
    TARGET_INDEX_FIELD_NUMBER: _ClassVar[int]
    entindex: int
    order_type: int
    target_index: int
    def __init__(
        self,
        entindex: int | None = ...,
        order_type: int | None = ...,
        target_index: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_SpectatorPlayerUnitOrders(_message.Message):
    __slots__ = (
        "entindex",
        "order_type",
        "units",
        "target_index",
        "ability_id",
        "position",
        "queue",
        "sequence_number",
        "flags",
        "last_order_latency",
        "ping",
    )
    ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    ORDER_TYPE_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    TARGET_INDEX_FIELD_NUMBER: _ClassVar[int]
    ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    QUEUE_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    LAST_ORDER_LATENCY_FIELD_NUMBER: _ClassVar[int]
    PING_FIELD_NUMBER: _ClassVar[int]
    entindex: int
    order_type: int
    units: _containers.RepeatedScalarFieldContainer[int]
    target_index: int
    ability_id: int
    position: _networkbasetypes_pb2.CMsgVector
    queue: bool
    sequence_number: int
    flags: int
    last_order_latency: int
    ping: int
    def __init__(
        self,
        entindex: int | None = ...,
        order_type: int | None = ...,
        units: _Iterable[int] | None = ...,
        target_index: int | None = ...,
        ability_id: int | None = ...,
        position: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
        queue: bool = ...,
        sequence_number: int | None = ...,
        flags: int | None = ...,
        last_order_latency: int | None = ...,
        ping: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_NevermoreRequiem(_message.Message):
    __slots__ = ("entity_handle", "lines", "origin", "reverse")
    ENTITY_HANDLE_FIELD_NUMBER: _ClassVar[int]
    LINES_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    REVERSE_FIELD_NUMBER: _ClassVar[int]
    entity_handle: int
    lines: int
    origin: _networkbasetypes_pb2.CMsgVector
    reverse: bool
    def __init__(
        self,
        entity_handle: int | None = ...,
        lines: int | None = ...,
        origin: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
        reverse: bool = ...,
    ) -> None: ...

class CDOTAUserMsg_InvalidCommand(_message.Message):
    __slots__ = ("message", "sequence_number")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    message: str
    sequence_number: int
    def __init__(self, message: str | None = ..., sequence_number: int | None = ...) -> None: ...

class CDOTAUserMsg_HudError(_message.Message):
    __slots__ = ("order_id", "sequence_number")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    order_id: int
    sequence_number: int
    def __init__(self, order_id: int | None = ..., sequence_number: int | None = ...) -> None: ...

class CDOTAUserMsg_SharedCooldown(_message.Message):
    __slots__ = ("entindex", "name", "cooldown", "name_index")
    ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    COOLDOWN_FIELD_NUMBER: _ClassVar[int]
    NAME_INDEX_FIELD_NUMBER: _ClassVar[int]
    entindex: int
    name: str
    cooldown: float
    name_index: int
    def __init__(
        self,
        entindex: int | None = ...,
        name: str | None = ...,
        cooldown: float | None = ...,
        name_index: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_SetNextAutobuyItem(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: str | None = ...) -> None: ...

class CDOTAUserMsg_HalloweenDrops(_message.Message):
    __slots__ = ("item_defs", "player_ids", "prize_list")
    ITEM_DEFS_FIELD_NUMBER: _ClassVar[int]
    PLAYER_IDS_FIELD_NUMBER: _ClassVar[int]
    PRIZE_LIST_FIELD_NUMBER: _ClassVar[int]
    item_defs: _containers.RepeatedScalarFieldContainer[int]
    player_ids: _containers.RepeatedScalarFieldContainer[int]
    prize_list: int
    def __init__(
        self,
        item_defs: _Iterable[int] | None = ...,
        player_ids: _Iterable[int] | None = ...,
        prize_list: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_CourierLeftFountainAlert(_message.Message):
    __slots__ = ("owning_player_id",)
    OWNING_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    owning_player_id: int
    def __init__(self, owning_player_id: int | None = ...) -> None: ...

class CDOTAResponseQuerySerialized(_message.Message):
    __slots__ = ("facts",)
    class Fact(_message.Message):
        __slots__ = (
            "key",
            "valtype",
            "val_numeric",
            "val_string",
            "val_stringtable_index",
            "val_int_numeric",
        )
        class ValueType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            NUMERIC: _ClassVar[CDOTAResponseQuerySerialized.Fact.ValueType]
            STRING: _ClassVar[CDOTAResponseQuerySerialized.Fact.ValueType]
            STRINGTABLE_INDEX: _ClassVar[CDOTAResponseQuerySerialized.Fact.ValueType]
            INT_NUMERIC: _ClassVar[CDOTAResponseQuerySerialized.Fact.ValueType]

        NUMERIC: CDOTAResponseQuerySerialized.Fact.ValueType
        STRING: CDOTAResponseQuerySerialized.Fact.ValueType
        STRINGTABLE_INDEX: CDOTAResponseQuerySerialized.Fact.ValueType
        INT_NUMERIC: CDOTAResponseQuerySerialized.Fact.ValueType
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALTYPE_FIELD_NUMBER: _ClassVar[int]
        VAL_NUMERIC_FIELD_NUMBER: _ClassVar[int]
        VAL_STRING_FIELD_NUMBER: _ClassVar[int]
        VAL_STRINGTABLE_INDEX_FIELD_NUMBER: _ClassVar[int]
        VAL_INT_NUMERIC_FIELD_NUMBER: _ClassVar[int]
        key: int
        valtype: CDOTAResponseQuerySerialized.Fact.ValueType
        val_numeric: float
        val_string: str
        val_stringtable_index: int
        val_int_numeric: int
        def __init__(
            self,
            key: int | None = ...,
            valtype: CDOTAResponseQuerySerialized.Fact.ValueType | str | None = ...,
            val_numeric: float | None = ...,
            val_string: str | None = ...,
            val_stringtable_index: int | None = ...,
            val_int_numeric: int | None = ...,
        ) -> None: ...

    FACTS_FIELD_NUMBER: _ClassVar[int]
    facts: _containers.RepeatedCompositeFieldContainer[CDOTAResponseQuerySerialized.Fact]
    def __init__(
        self, facts: _Iterable[CDOTAResponseQuerySerialized.Fact | _Mapping] | None = ...
    ) -> None: ...

class CDOTASpeechMatchOnClient(_message.Message):
    __slots__ = ("speech_concept", "recipient_type", "responsequery", "randomseed")
    SPEECH_CONCEPT_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    RESPONSEQUERY_FIELD_NUMBER: _ClassVar[int]
    RANDOMSEED_FIELD_NUMBER: _ClassVar[int]
    speech_concept: int
    recipient_type: int
    responsequery: CDOTAResponseQuerySerialized
    randomseed: int
    def __init__(
        self,
        speech_concept: int | None = ...,
        recipient_type: int | None = ...,
        responsequery: CDOTAResponseQuerySerialized | _Mapping | None = ...,
        randomseed: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_UnitEvent(_message.Message):
    __slots__ = (
        "msg_type",
        "entity_index",
        "speech",
        "speech_mute",
        "add_gesture",
        "remove_gesture",
        "blood_impact",
        "fade_gesture",
        "speech_match_on_client",
    )
    class Interval(_message.Message):
        __slots__ = ("start", "range")
        START_FIELD_NUMBER: _ClassVar[int]
        RANGE_FIELD_NUMBER: _ClassVar[int]
        start: float
        range: float
        def __init__(self, start: float | None = ..., range: float | None = ...) -> None: ...

    class Speech(_message.Message):
        __slots__ = (
            "speech_concept",
            "response",
            "recipient_type",
            "muteable",
            "predelay",
            "flags",
            "response_type",
        )
        SPEECH_CONCEPT_FIELD_NUMBER: _ClassVar[int]
        RESPONSE_FIELD_NUMBER: _ClassVar[int]
        RECIPIENT_TYPE_FIELD_NUMBER: _ClassVar[int]
        MUTEABLE_FIELD_NUMBER: _ClassVar[int]
        PREDELAY_FIELD_NUMBER: _ClassVar[int]
        FLAGS_FIELD_NUMBER: _ClassVar[int]
        RESPONSE_TYPE_FIELD_NUMBER: _ClassVar[int]
        speech_concept: int
        response: str
        recipient_type: int
        muteable: bool
        predelay: CDOTAUserMsg_UnitEvent.Interval
        flags: int
        response_type: int
        def __init__(
            self,
            speech_concept: int | None = ...,
            response: str | None = ...,
            recipient_type: int | None = ...,
            muteable: bool = ...,
            predelay: CDOTAUserMsg_UnitEvent.Interval | _Mapping | None = ...,
            flags: int | None = ...,
            response_type: int | None = ...,
        ) -> None: ...

    class SpeechMute(_message.Message):
        __slots__ = ("delay",)
        DELAY_FIELD_NUMBER: _ClassVar[int]
        delay: float
        def __init__(self, delay: float | None = ...) -> None: ...

    class AddGesture(_message.Message):
        __slots__ = ("activity", "slot", "fade_in", "fade_out", "playback_rate", "sequence_variant")
        ACTIVITY_FIELD_NUMBER: _ClassVar[int]
        SLOT_FIELD_NUMBER: _ClassVar[int]
        FADE_IN_FIELD_NUMBER: _ClassVar[int]
        FADE_OUT_FIELD_NUMBER: _ClassVar[int]
        PLAYBACK_RATE_FIELD_NUMBER: _ClassVar[int]
        SEQUENCE_VARIANT_FIELD_NUMBER: _ClassVar[int]
        activity: int
        slot: int
        fade_in: float
        fade_out: float
        playback_rate: float
        sequence_variant: int
        def __init__(
            self,
            activity: int | None = ...,
            slot: int | None = ...,
            fade_in: float | None = ...,
            fade_out: float | None = ...,
            playback_rate: float | None = ...,
            sequence_variant: int | None = ...,
        ) -> None: ...

    class RemoveGesture(_message.Message):
        __slots__ = ("activity",)
        ACTIVITY_FIELD_NUMBER: _ClassVar[int]
        activity: int
        def __init__(self, activity: int | None = ...) -> None: ...

    class BloodImpact(_message.Message):
        __slots__ = ("scale", "x_normal", "y_normal")
        SCALE_FIELD_NUMBER: _ClassVar[int]
        X_NORMAL_FIELD_NUMBER: _ClassVar[int]
        Y_NORMAL_FIELD_NUMBER: _ClassVar[int]
        scale: int
        x_normal: int
        y_normal: int
        def __init__(
            self, scale: int | None = ..., x_normal: int | None = ..., y_normal: int | None = ...
        ) -> None: ...

    class FadeGesture(_message.Message):
        __slots__ = ("activity",)
        ACTIVITY_FIELD_NUMBER: _ClassVar[int]
        activity: int
        def __init__(self, activity: int | None = ...) -> None: ...

    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    ENTITY_INDEX_FIELD_NUMBER: _ClassVar[int]
    SPEECH_FIELD_NUMBER: _ClassVar[int]
    SPEECH_MUTE_FIELD_NUMBER: _ClassVar[int]
    ADD_GESTURE_FIELD_NUMBER: _ClassVar[int]
    REMOVE_GESTURE_FIELD_NUMBER: _ClassVar[int]
    BLOOD_IMPACT_FIELD_NUMBER: _ClassVar[int]
    FADE_GESTURE_FIELD_NUMBER: _ClassVar[int]
    SPEECH_MATCH_ON_CLIENT_FIELD_NUMBER: _ClassVar[int]
    msg_type: EDotaEntityMessages
    entity_index: int
    speech: CDOTAUserMsg_UnitEvent.Speech
    speech_mute: CDOTAUserMsg_UnitEvent.SpeechMute
    add_gesture: CDOTAUserMsg_UnitEvent.AddGesture
    remove_gesture: CDOTAUserMsg_UnitEvent.RemoveGesture
    blood_impact: CDOTAUserMsg_UnitEvent.BloodImpact
    fade_gesture: CDOTAUserMsg_UnitEvent.FadeGesture
    speech_match_on_client: CDOTASpeechMatchOnClient
    def __init__(
        self,
        msg_type: EDotaEntityMessages | str | None = ...,
        entity_index: int | None = ...,
        speech: CDOTAUserMsg_UnitEvent.Speech | _Mapping | None = ...,
        speech_mute: CDOTAUserMsg_UnitEvent.SpeechMute | _Mapping | None = ...,
        add_gesture: CDOTAUserMsg_UnitEvent.AddGesture | _Mapping | None = ...,
        remove_gesture: CDOTAUserMsg_UnitEvent.RemoveGesture | _Mapping | None = ...,
        blood_impact: CDOTAUserMsg_UnitEvent.BloodImpact | _Mapping | None = ...,
        fade_gesture: CDOTAUserMsg_UnitEvent.FadeGesture | _Mapping | None = ...,
        speech_match_on_client: CDOTASpeechMatchOnClient | _Mapping | None = ...,
    ) -> None: ...

class CDOTAUserMsg_ItemPurchased(_message.Message):
    __slots__ = ("item_ability_id", "from_combine")
    ITEM_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    FROM_COMBINE_FIELD_NUMBER: _ClassVar[int]
    item_ability_id: int
    from_combine: bool
    def __init__(self, item_ability_id: int | None = ..., from_combine: bool = ...) -> None: ...

class CDOTAUserMsg_ItemSold(_message.Message):
    __slots__ = ("item_ability_id",)
    ITEM_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    item_ability_id: int
    def __init__(self, item_ability_id: int | None = ...) -> None: ...

class CDOTAUserMsg_ItemFound(_message.Message):
    __slots__ = ("player", "quality", "rarity", "method", "itemdef")
    PLAYER_FIELD_NUMBER: _ClassVar[int]
    QUALITY_FIELD_NUMBER: _ClassVar[int]
    RARITY_FIELD_NUMBER: _ClassVar[int]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    ITEMDEF_FIELD_NUMBER: _ClassVar[int]
    player: int
    quality: int
    rarity: int
    method: int
    itemdef: int
    def __init__(
        self,
        player: int | None = ...,
        quality: int | None = ...,
        rarity: int | None = ...,
        method: int | None = ...,
        itemdef: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_OverheadEvent(_message.Message):
    __slots__ = (
        "message_type",
        "value",
        "target_player_entindex",
        "target_entindex",
        "source_player_entindex",
    )
    MESSAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    TARGET_PLAYER_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    TARGET_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    SOURCE_PLAYER_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    message_type: DOTA_OVERHEAD_ALERT
    value: int
    target_player_entindex: int
    target_entindex: int
    source_player_entindex: int
    def __init__(
        self,
        message_type: DOTA_OVERHEAD_ALERT | str | None = ...,
        value: int | None = ...,
        target_player_entindex: int | None = ...,
        target_entindex: int | None = ...,
        source_player_entindex: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_TutorialTipInfo(_message.Message):
    __slots__ = ("name", "progress")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    name: str
    progress: int
    def __init__(self, name: str | None = ..., progress: int | None = ...) -> None: ...

class CDOTAUserMsg_TutorialFinish(_message.Message):
    __slots__ = ("heading", "emblem", "body", "success")
    HEADING_FIELD_NUMBER: _ClassVar[int]
    EMBLEM_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    heading: str
    emblem: str
    body: str
    success: bool
    def __init__(
        self,
        heading: str | None = ...,
        emblem: str | None = ...,
        body: str | None = ...,
        success: bool = ...,
    ) -> None: ...

class CDOTAUserMsg_TutorialMinimapPosition(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CDOTAUserMsg_SendGenericToolTip(_message.Message):
    __slots__ = ("title", "text", "entindex", "close")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    CLOSE_FIELD_NUMBER: _ClassVar[int]
    title: str
    text: str
    entindex: int
    close: bool
    def __init__(
        self,
        title: str | None = ...,
        text: str | None = ...,
        entindex: int | None = ...,
        close: bool = ...,
    ) -> None: ...

class CDOTAUserMsg_WorldLine(_message.Message):
    __slots__ = ("player_id", "worldline")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    WORLDLINE_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    worldline: _dota_commonmessages_pb2.CDOTAMsg_WorldLine
    def __init__(
        self,
        player_id: int | None = ...,
        worldline: _dota_commonmessages_pb2.CDOTAMsg_WorldLine | _Mapping | None = ...,
    ) -> None: ...

class CDOTAUserMsg_ChatWheel(_message.Message):
    __slots__ = ("chat_message_id", "player_id", "account_id", "param_hero_id", "emoticon_id")
    CHAT_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    PARAM_HERO_ID_FIELD_NUMBER: _ClassVar[int]
    EMOTICON_ID_FIELD_NUMBER: _ClassVar[int]
    chat_message_id: int
    player_id: int
    account_id: int
    param_hero_id: int
    emoticon_id: int
    def __init__(
        self,
        chat_message_id: int | None = ...,
        player_id: int | None = ...,
        account_id: int | None = ...,
        param_hero_id: int | None = ...,
        emoticon_id: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_ReceivedXmasGift(_message.Message):
    __slots__ = ("player_id", "item_name", "inventory_slot")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_NAME_FIELD_NUMBER: _ClassVar[int]
    INVENTORY_SLOT_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    item_name: str
    inventory_slot: int
    def __init__(
        self,
        player_id: int | None = ...,
        item_name: str | None = ...,
        inventory_slot: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_ShowSurvey(_message.Message):
    __slots__ = (
        "survey_id",
        "match_id",
        "response_style",
        "teammate_hero_id",
        "teammate_name",
        "teammate_account_id",
    )
    SURVEY_ID_FIELD_NUMBER: _ClassVar[int]
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_STYLE_FIELD_NUMBER: _ClassVar[int]
    TEAMMATE_HERO_ID_FIELD_NUMBER: _ClassVar[int]
    TEAMMATE_NAME_FIELD_NUMBER: _ClassVar[int]
    TEAMMATE_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    survey_id: int
    match_id: int
    response_style: str
    teammate_hero_id: int
    teammate_name: str
    teammate_account_id: int
    def __init__(
        self,
        survey_id: int | None = ...,
        match_id: int | None = ...,
        response_style: str | None = ...,
        teammate_hero_id: int | None = ...,
        teammate_name: str | None = ...,
        teammate_account_id: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_UpdateSharedContent(_message.Message):
    __slots__ = ("slot_type",)
    SLOT_TYPE_FIELD_NUMBER: _ClassVar[int]
    slot_type: int
    def __init__(self, slot_type: int | None = ...) -> None: ...

class CDOTAUserMsg_TutorialRequestExp(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CDOTAUserMsg_TutorialFade(_message.Message):
    __slots__ = ("tgt_alpha",)
    TGT_ALPHA_FIELD_NUMBER: _ClassVar[int]
    tgt_alpha: int
    def __init__(self, tgt_alpha: int | None = ...) -> None: ...

class CDOTAUserMsg_TutorialPingMinimap(_message.Message):
    __slots__ = ("player_id", "pos_x", "pos_y", "pos_z", "entity_index")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    POS_X_FIELD_NUMBER: _ClassVar[int]
    POS_Y_FIELD_NUMBER: _ClassVar[int]
    POS_Z_FIELD_NUMBER: _ClassVar[int]
    ENTITY_INDEX_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    pos_x: float
    pos_y: float
    pos_z: float
    entity_index: int
    def __init__(
        self,
        player_id: int | None = ...,
        pos_x: float | None = ...,
        pos_y: float | None = ...,
        pos_z: float | None = ...,
        entity_index: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_GamerulesStateChanged(_message.Message):
    __slots__ = ("state",)
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: int
    def __init__(self, state: int | None = ...) -> None: ...

class CDOTAUserMsg_AddQuestLogEntry(_message.Message):
    __slots__ = ("npc_name", "npc_dialog")
    NPC_NAME_FIELD_NUMBER: _ClassVar[int]
    NPC_DIALOG_FIELD_NUMBER: _ClassVar[int]
    npc_name: str
    npc_dialog: str
    def __init__(self, npc_name: str | None = ..., npc_dialog: str | None = ...) -> None: ...

class CDOTAUserMsg_SendStatPopup(_message.Message):
    __slots__ = ("player_id", "statpopup")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    STATPOPUP_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    statpopup: _dota_commonmessages_pb2.CDOTAMsg_SendStatPopup
    def __init__(
        self,
        player_id: int | None = ...,
        statpopup: _dota_commonmessages_pb2.CDOTAMsg_SendStatPopup | _Mapping | None = ...,
    ) -> None: ...

class CDOTAUserMsg_DismissAllStatPopups(_message.Message):
    __slots__ = ("dismissallmsg",)
    DISMISSALLMSG_FIELD_NUMBER: _ClassVar[int]
    dismissallmsg: _dota_commonmessages_pb2.CDOTAMsg_DismissAllStatPopups
    def __init__(
        self,
        dismissallmsg: _dota_commonmessages_pb2.CDOTAMsg_DismissAllStatPopups
        | _Mapping
        | None = ...,
    ) -> None: ...

class CDOTAUserMsg_SendRoshanSpectatorPhase(_message.Message):
    __slots__ = ("phase", "phase_start_time", "phase_length")
    PHASE_FIELD_NUMBER: _ClassVar[int]
    PHASE_START_TIME_FIELD_NUMBER: _ClassVar[int]
    PHASE_LENGTH_FIELD_NUMBER: _ClassVar[int]
    phase: DOTA_ROSHAN_PHASE
    phase_start_time: int
    phase_length: int
    def __init__(
        self,
        phase: DOTA_ROSHAN_PHASE | str | None = ...,
        phase_start_time: int | None = ...,
        phase_length: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_SendRoshanPopup(_message.Message):
    __slots__ = ("reclaimed", "gametime")
    RECLAIMED_FIELD_NUMBER: _ClassVar[int]
    GAMETIME_FIELD_NUMBER: _ClassVar[int]
    reclaimed: bool
    gametime: int
    def __init__(self, reclaimed: bool = ..., gametime: int | None = ...) -> None: ...

class CDOTAUserMsg_SendFinalGold(_message.Message):
    __slots__ = ("reliable_gold", "unreliable_gold")
    RELIABLE_GOLD_FIELD_NUMBER: _ClassVar[int]
    UNRELIABLE_GOLD_FIELD_NUMBER: _ClassVar[int]
    reliable_gold: _containers.RepeatedScalarFieldContainer[int]
    unreliable_gold: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        reliable_gold: _Iterable[int] | None = ...,
        unreliable_gold: _Iterable[int] | None = ...,
    ) -> None: ...

class CDOTAUserMsg_CustomMsg(_message.Message):
    __slots__ = ("message", "player_id", "value")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    message: str
    player_id: int
    value: int
    def __init__(
        self, message: str | None = ..., player_id: int | None = ..., value: int | None = ...
    ) -> None: ...

class CDOTAUserMsg_CoachHUDPing(_message.Message):
    __slots__ = ("player_id", "hud_ping")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    HUD_PING_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    hud_ping: _dota_commonmessages_pb2.CDOTAMsg_CoachHUDPing
    def __init__(
        self,
        player_id: int | None = ...,
        hud_ping: _dota_commonmessages_pb2.CDOTAMsg_CoachHUDPing | _Mapping | None = ...,
    ) -> None: ...

class CDOTAUserMsg_ClientLoadGridNav(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CDOTAUserMsg_TE_Projectile(_message.Message):
    __slots__ = (
        "source",
        "target",
        "move_speed",
        "source_attachment",
        "particle_system_handle",
        "dodgeable",
        "is_attack",
        "expire_time",
        "maximpacttime",
        "colorgemcolor",
        "launch_tick",
        "handle",
        "target_loc",
        "particle_cp_data",
        "additional_particle_system_handle",
        "original_move_speed",
        "ability",
        "target_projectile_handle",
    )
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    MOVE_SPEED_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ATTACHMENT_FIELD_NUMBER: _ClassVar[int]
    PARTICLE_SYSTEM_HANDLE_FIELD_NUMBER: _ClassVar[int]
    DODGEABLE_FIELD_NUMBER: _ClassVar[int]
    IS_ATTACK_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_TIME_FIELD_NUMBER: _ClassVar[int]
    MAXIMPACTTIME_FIELD_NUMBER: _ClassVar[int]
    COLORGEMCOLOR_FIELD_NUMBER: _ClassVar[int]
    LAUNCH_TICK_FIELD_NUMBER: _ClassVar[int]
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    TARGET_LOC_FIELD_NUMBER: _ClassVar[int]
    PARTICLE_CP_DATA_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_PARTICLE_SYSTEM_HANDLE_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_MOVE_SPEED_FIELD_NUMBER: _ClassVar[int]
    ABILITY_FIELD_NUMBER: _ClassVar[int]
    TARGET_PROJECTILE_HANDLE_FIELD_NUMBER: _ClassVar[int]
    source: int
    target: int
    move_speed: int
    source_attachment: int
    particle_system_handle: int
    dodgeable: bool
    is_attack: bool
    expire_time: float
    maximpacttime: float
    colorgemcolor: int
    launch_tick: int
    handle: int
    target_loc: _networkbasetypes_pb2.CMsgVector
    particle_cp_data: _containers.RepeatedCompositeFieldContainer[
        CDOTAUserMsg_ProjectileParticleCPData
    ]
    additional_particle_system_handle: int
    original_move_speed: int
    ability: int
    target_projectile_handle: int
    def __init__(
        self,
        source: int | None = ...,
        target: int | None = ...,
        move_speed: int | None = ...,
        source_attachment: int | None = ...,
        particle_system_handle: int | None = ...,
        dodgeable: bool = ...,
        is_attack: bool = ...,
        expire_time: float | None = ...,
        maximpacttime: float | None = ...,
        colorgemcolor: int | None = ...,
        launch_tick: int | None = ...,
        handle: int | None = ...,
        target_loc: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
        particle_cp_data: _Iterable[CDOTAUserMsg_ProjectileParticleCPData | _Mapping] | None = ...,
        additional_particle_system_handle: int | None = ...,
        original_move_speed: int | None = ...,
        ability: int | None = ...,
        target_projectile_handle: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_TE_ProjectileLoc(_message.Message):
    __slots__ = (
        "source_loc",
        "target",
        "move_speed",
        "particle_system_handle",
        "dodgeable",
        "is_attack",
        "expire_time",
        "target_loc",
        "colorgemcolor",
        "launch_tick",
        "handle",
        "source",
        "source_attachment",
        "particle_cp_data",
        "additional_particle_system_handle",
        "original_move_speed",
    )
    SOURCE_LOC_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    MOVE_SPEED_FIELD_NUMBER: _ClassVar[int]
    PARTICLE_SYSTEM_HANDLE_FIELD_NUMBER: _ClassVar[int]
    DODGEABLE_FIELD_NUMBER: _ClassVar[int]
    IS_ATTACK_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_TIME_FIELD_NUMBER: _ClassVar[int]
    TARGET_LOC_FIELD_NUMBER: _ClassVar[int]
    COLORGEMCOLOR_FIELD_NUMBER: _ClassVar[int]
    LAUNCH_TICK_FIELD_NUMBER: _ClassVar[int]
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ATTACHMENT_FIELD_NUMBER: _ClassVar[int]
    PARTICLE_CP_DATA_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_PARTICLE_SYSTEM_HANDLE_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_MOVE_SPEED_FIELD_NUMBER: _ClassVar[int]
    source_loc: _networkbasetypes_pb2.CMsgVector
    target: int
    move_speed: int
    particle_system_handle: int
    dodgeable: bool
    is_attack: bool
    expire_time: float
    target_loc: _networkbasetypes_pb2.CMsgVector
    colorgemcolor: int
    launch_tick: int
    handle: int
    source: int
    source_attachment: int
    particle_cp_data: _containers.RepeatedCompositeFieldContainer[
        CDOTAUserMsg_ProjectileParticleCPData
    ]
    additional_particle_system_handle: int
    original_move_speed: int
    def __init__(
        self,
        source_loc: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
        target: int | None = ...,
        move_speed: int | None = ...,
        particle_system_handle: int | None = ...,
        dodgeable: bool = ...,
        is_attack: bool = ...,
        expire_time: float | None = ...,
        target_loc: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
        colorgemcolor: int | None = ...,
        launch_tick: int | None = ...,
        handle: int | None = ...,
        source: int | None = ...,
        source_attachment: int | None = ...,
        particle_cp_data: _Iterable[CDOTAUserMsg_ProjectileParticleCPData | _Mapping] | None = ...,
        additional_particle_system_handle: int | None = ...,
        original_move_speed: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_TE_DestroyProjectile(_message.Message):
    __slots__ = ("handle",)
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    handle: int
    def __init__(self, handle: int | None = ...) -> None: ...

class CDOTAUserMsg_TE_DotaBloodImpact(_message.Message):
    __slots__ = ("entity", "scale", "xnormal", "ynormal")
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    SCALE_FIELD_NUMBER: _ClassVar[int]
    XNORMAL_FIELD_NUMBER: _ClassVar[int]
    YNORMAL_FIELD_NUMBER: _ClassVar[int]
    entity: int
    scale: float
    xnormal: float
    ynormal: float
    def __init__(
        self,
        entity: int | None = ...,
        scale: float | None = ...,
        xnormal: float | None = ...,
        ynormal: float | None = ...,
    ) -> None: ...

class CDOTAUserMsg_AbilityPing(_message.Message):
    __slots__ = (
        "player_id",
        "ability_id",
        "type",
        "cooldown_seconds",
        "level",
        "passive",
        "mana_needed",
        "entity_id",
        "primary_charges",
        "secondary_charges",
        "ctrl_held",
        "reclaim_time",
        "owner_entity",
    )
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    COOLDOWN_SECONDS_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    PASSIVE_FIELD_NUMBER: _ClassVar[int]
    MANA_NEEDED_FIELD_NUMBER: _ClassVar[int]
    ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_CHARGES_FIELD_NUMBER: _ClassVar[int]
    SECONDARY_CHARGES_FIELD_NUMBER: _ClassVar[int]
    CTRL_HELD_FIELD_NUMBER: _ClassVar[int]
    RECLAIM_TIME_FIELD_NUMBER: _ClassVar[int]
    OWNER_ENTITY_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    ability_id: int
    type: DOTA_ABILITY_PING_TYPE
    cooldown_seconds: int
    level: int
    passive: bool
    mana_needed: int
    entity_id: int
    primary_charges: int
    secondary_charges: int
    ctrl_held: bool
    reclaim_time: float
    owner_entity: int
    def __init__(
        self,
        player_id: int | None = ...,
        ability_id: int | None = ...,
        type: DOTA_ABILITY_PING_TYPE | str | None = ...,
        cooldown_seconds: int | None = ...,
        level: int | None = ...,
        passive: bool = ...,
        mana_needed: int | None = ...,
        entity_id: int | None = ...,
        primary_charges: int | None = ...,
        secondary_charges: int | None = ...,
        ctrl_held: bool = ...,
        reclaim_time: float | None = ...,
        owner_entity: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_TE_UnitAnimation(_message.Message):
    __slots__ = (
        "entity",
        "sequence_variant",
        "playbackrate",
        "castpoint",
        "type",
        "activity",
        "lag_compensation_time",
    )
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_VARIANT_FIELD_NUMBER: _ClassVar[int]
    PLAYBACKRATE_FIELD_NUMBER: _ClassVar[int]
    CASTPOINT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_FIELD_NUMBER: _ClassVar[int]
    LAG_COMPENSATION_TIME_FIELD_NUMBER: _ClassVar[int]
    entity: int
    sequence_variant: int
    playbackrate: float
    castpoint: float
    type: int
    activity: int
    lag_compensation_time: float
    def __init__(
        self,
        entity: int | None = ...,
        sequence_variant: int | None = ...,
        playbackrate: float | None = ...,
        castpoint: float | None = ...,
        type: int | None = ...,
        activity: int | None = ...,
        lag_compensation_time: float | None = ...,
    ) -> None: ...

class CDOTAUserMsg_TE_UnitAnimationEnd(_message.Message):
    __slots__ = ("entity", "snap")
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    SNAP_FIELD_NUMBER: _ClassVar[int]
    entity: int
    snap: bool
    def __init__(self, entity: int | None = ..., snap: bool = ...) -> None: ...

class CDOTAUserMsg_ShowGenericPopup(_message.Message):
    __slots__ = ("header", "body", "param1", "param2", "tint_screen", "show_no_other_dialogs")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    PARAM1_FIELD_NUMBER: _ClassVar[int]
    PARAM2_FIELD_NUMBER: _ClassVar[int]
    TINT_SCREEN_FIELD_NUMBER: _ClassVar[int]
    SHOW_NO_OTHER_DIALOGS_FIELD_NUMBER: _ClassVar[int]
    header: str
    body: str
    param1: str
    param2: str
    tint_screen: bool
    show_no_other_dialogs: bool
    def __init__(
        self,
        header: str | None = ...,
        body: str | None = ...,
        param1: str | None = ...,
        param2: str | None = ...,
        tint_screen: bool = ...,
        show_no_other_dialogs: bool = ...,
    ) -> None: ...

class CDOTAUserMsg_VoteStart(_message.Message):
    __slots__ = ("title", "duration", "choice_count", "choices")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    CHOICE_COUNT_FIELD_NUMBER: _ClassVar[int]
    CHOICES_FIELD_NUMBER: _ClassVar[int]
    title: str
    duration: float
    choice_count: int
    choices: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        title: str | None = ...,
        duration: float | None = ...,
        choice_count: int | None = ...,
        choices: _Iterable[str] | None = ...,
    ) -> None: ...

class CDOTAUserMsg_VoteUpdate(_message.Message):
    __slots__ = ("choice_counts",)
    CHOICE_COUNTS_FIELD_NUMBER: _ClassVar[int]
    choice_counts: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, choice_counts: _Iterable[int] | None = ...) -> None: ...

class CDOTAUserMsg_VoteEnd(_message.Message):
    __slots__ = ("selected_choice",)
    SELECTED_CHOICE_FIELD_NUMBER: _ClassVar[int]
    selected_choice: int
    def __init__(self, selected_choice: int | None = ...) -> None: ...

class CDOTAUserMsg_BoosterStatePlayer(_message.Message):
    __slots__ = ("player_id", "bonus", "event_bonus", "bonus_item_id", "event_bonus_item_id")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    BONUS_FIELD_NUMBER: _ClassVar[int]
    EVENT_BONUS_FIELD_NUMBER: _ClassVar[int]
    BONUS_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_BONUS_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    bonus: float
    event_bonus: float
    bonus_item_id: int
    event_bonus_item_id: int
    def __init__(
        self,
        player_id: int | None = ...,
        bonus: float | None = ...,
        event_bonus: float | None = ...,
        bonus_item_id: int | None = ...,
        event_bonus_item_id: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_BoosterState(_message.Message):
    __slots__ = ("boosted_players",)
    BOOSTED_PLAYERS_FIELD_NUMBER: _ClassVar[int]
    boosted_players: _containers.RepeatedCompositeFieldContainer[CDOTAUserMsg_BoosterStatePlayer]
    def __init__(
        self, boosted_players: _Iterable[CDOTAUserMsg_BoosterStatePlayer | _Mapping] | None = ...
    ) -> None: ...

class CDOTAUserMsg_AbilitySteal(_message.Message):
    __slots__ = ("player_id", "ability_id", "ability_level")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    ABILITY_LEVEL_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    ability_id: int
    ability_level: int
    def __init__(
        self,
        player_id: int | None = ...,
        ability_id: int | None = ...,
        ability_level: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_StatsHeroLookup(_message.Message):
    __slots__ = ("player_id", "hero_id", "hero_name", "persona")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    HERO_NAME_FIELD_NUMBER: _ClassVar[int]
    PERSONA_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    hero_id: int
    hero_name: str
    persona: str
    def __init__(
        self,
        player_id: int | None = ...,
        hero_id: int | None = ...,
        hero_name: str | None = ...,
        persona: str | None = ...,
    ) -> None: ...

class CDOTAUserMsg_StatsHeroPositionInfo(_message.Message):
    __slots__ = ("average_position", "position_details")
    class PositionPair(_message.Message):
        __slots__ = ("position_category", "position_count")
        POSITION_CATEGORY_FIELD_NUMBER: _ClassVar[int]
        POSITION_COUNT_FIELD_NUMBER: _ClassVar[int]
        position_category: DOTA_POSITION_CATEGORY
        position_count: int
        def __init__(
            self,
            position_category: DOTA_POSITION_CATEGORY | str | None = ...,
            position_count: int | None = ...,
        ) -> None: ...

    AVERAGE_POSITION_FIELD_NUMBER: _ClassVar[int]
    POSITION_DETAILS_FIELD_NUMBER: _ClassVar[int]
    average_position: float
    position_details: _containers.RepeatedCompositeFieldContainer[
        CDOTAUserMsg_StatsHeroPositionInfo.PositionPair
    ]
    def __init__(
        self,
        average_position: float | None = ...,
        position_details: _Iterable[CDOTAUserMsg_StatsHeroPositionInfo.PositionPair | _Mapping]
        | None = ...,
    ) -> None: ...

class CDOTAUserMsg_StatsHeroMinuteDetails(_message.Message):
    __slots__ = (
        "last_hits",
        "hero_kills",
        "hero_damage",
        "tower_damage",
        "position_info",
        "total_xp",
        "net_worth",
        "harvested_creep_gold",
        "claimed_farm",
        "wards_placed",
        "runes_collected",
        "tps_used",
        "mana_spent",
        "damage_absorbed",
        "damage_done",
    )
    LAST_HITS_FIELD_NUMBER: _ClassVar[int]
    HERO_KILLS_FIELD_NUMBER: _ClassVar[int]
    HERO_DAMAGE_FIELD_NUMBER: _ClassVar[int]
    TOWER_DAMAGE_FIELD_NUMBER: _ClassVar[int]
    POSITION_INFO_FIELD_NUMBER: _ClassVar[int]
    TOTAL_XP_FIELD_NUMBER: _ClassVar[int]
    NET_WORTH_FIELD_NUMBER: _ClassVar[int]
    HARVESTED_CREEP_GOLD_FIELD_NUMBER: _ClassVar[int]
    CLAIMED_FARM_FIELD_NUMBER: _ClassVar[int]
    WARDS_PLACED_FIELD_NUMBER: _ClassVar[int]
    RUNES_COLLECTED_FIELD_NUMBER: _ClassVar[int]
    TPS_USED_FIELD_NUMBER: _ClassVar[int]
    MANA_SPENT_FIELD_NUMBER: _ClassVar[int]
    DAMAGE_ABSORBED_FIELD_NUMBER: _ClassVar[int]
    DAMAGE_DONE_FIELD_NUMBER: _ClassVar[int]
    last_hits: int
    hero_kills: int
    hero_damage: int
    tower_damage: int
    position_info: CDOTAUserMsg_StatsHeroPositionInfo
    total_xp: int
    net_worth: int
    harvested_creep_gold: int
    claimed_farm: int
    wards_placed: int
    runes_collected: int
    tps_used: int
    mana_spent: _containers.RepeatedScalarFieldContainer[int]
    damage_absorbed: _containers.RepeatedScalarFieldContainer[int]
    damage_done: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        last_hits: int | None = ...,
        hero_kills: int | None = ...,
        hero_damage: int | None = ...,
        tower_damage: int | None = ...,
        position_info: CDOTAUserMsg_StatsHeroPositionInfo | _Mapping | None = ...,
        total_xp: int | None = ...,
        net_worth: int | None = ...,
        harvested_creep_gold: int | None = ...,
        claimed_farm: int | None = ...,
        wards_placed: int | None = ...,
        runes_collected: int | None = ...,
        tps_used: int | None = ...,
        mana_spent: _Iterable[int] | None = ...,
        damage_absorbed: _Iterable[int] | None = ...,
        damage_done: _Iterable[int] | None = ...,
    ) -> None: ...

class CDOTAUserMsg_StatsTeamMinuteDetails(_message.Message):
    __slots__ = (
        "player_stats",
        "tower_kills",
        "barrack_kills",
        "available_lane_creep_gold",
        "balance_kill_value",
        "balance_tower_value",
        "balance_barracks_value",
        "balance_gold_value",
        "balance_xp_value",
        "lane_performance",
    )
    class LocationPerformance(_message.Message):
        __slots__ = ("location_category", "stat_type", "value")
        LOCATION_CATEGORY_FIELD_NUMBER: _ClassVar[int]
        STAT_TYPE_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        location_category: int
        stat_type: int
        value: int
        def __init__(
            self,
            location_category: int | None = ...,
            stat_type: int | None = ...,
            value: int | None = ...,
        ) -> None: ...

    PLAYER_STATS_FIELD_NUMBER: _ClassVar[int]
    TOWER_KILLS_FIELD_NUMBER: _ClassVar[int]
    BARRACK_KILLS_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_LANE_CREEP_GOLD_FIELD_NUMBER: _ClassVar[int]
    BALANCE_KILL_VALUE_FIELD_NUMBER: _ClassVar[int]
    BALANCE_TOWER_VALUE_FIELD_NUMBER: _ClassVar[int]
    BALANCE_BARRACKS_VALUE_FIELD_NUMBER: _ClassVar[int]
    BALANCE_GOLD_VALUE_FIELD_NUMBER: _ClassVar[int]
    BALANCE_XP_VALUE_FIELD_NUMBER: _ClassVar[int]
    LANE_PERFORMANCE_FIELD_NUMBER: _ClassVar[int]
    player_stats: _containers.RepeatedCompositeFieldContainer[CDOTAUserMsg_StatsHeroMinuteDetails]
    tower_kills: int
    barrack_kills: int
    available_lane_creep_gold: int
    balance_kill_value: int
    balance_tower_value: int
    balance_barracks_value: int
    balance_gold_value: int
    balance_xp_value: int
    lane_performance: _containers.RepeatedCompositeFieldContainer[
        CDOTAUserMsg_StatsTeamMinuteDetails.LocationPerformance
    ]
    def __init__(
        self,
        player_stats: _Iterable[CDOTAUserMsg_StatsHeroMinuteDetails | _Mapping] | None = ...,
        tower_kills: int | None = ...,
        barrack_kills: int | None = ...,
        available_lane_creep_gold: int | None = ...,
        balance_kill_value: int | None = ...,
        balance_tower_value: int | None = ...,
        balance_barracks_value: int | None = ...,
        balance_gold_value: int | None = ...,
        balance_xp_value: int | None = ...,
        lane_performance: _Iterable[
            CDOTAUserMsg_StatsTeamMinuteDetails.LocationPerformance | _Mapping
        ]
        | None = ...,
    ) -> None: ...

class CDOTAUserMsg_StatsPlayerKillShare(_message.Message):
    __slots__ = (
        "player_id",
        "kill_share_percent",
        "player_loc_x",
        "player_loc_y",
        "health_percent",
        "mana_percent",
    )
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    KILL_SHARE_PERCENT_FIELD_NUMBER: _ClassVar[int]
    PLAYER_LOC_X_FIELD_NUMBER: _ClassVar[int]
    PLAYER_LOC_Y_FIELD_NUMBER: _ClassVar[int]
    HEALTH_PERCENT_FIELD_NUMBER: _ClassVar[int]
    MANA_PERCENT_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    kill_share_percent: float
    player_loc_x: float
    player_loc_y: float
    health_percent: float
    mana_percent: float
    def __init__(
        self,
        player_id: int | None = ...,
        kill_share_percent: float | None = ...,
        player_loc_x: float | None = ...,
        player_loc_y: float | None = ...,
        health_percent: float | None = ...,
        mana_percent: float | None = ...,
    ) -> None: ...

class CDOTAUserMsg_StatsKillDetails(_message.Message):
    __slots__ = (
        "victim_id",
        "kill_shares",
        "damage_to_kill",
        "effective_health",
        "death_time",
        "killer_id",
    )
    VICTIM_ID_FIELD_NUMBER: _ClassVar[int]
    KILL_SHARES_FIELD_NUMBER: _ClassVar[int]
    DAMAGE_TO_KILL_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_HEALTH_FIELD_NUMBER: _ClassVar[int]
    DEATH_TIME_FIELD_NUMBER: _ClassVar[int]
    KILLER_ID_FIELD_NUMBER: _ClassVar[int]
    victim_id: int
    kill_shares: _containers.RepeatedCompositeFieldContainer[CDOTAUserMsg_StatsPlayerKillShare]
    damage_to_kill: int
    effective_health: int
    death_time: float
    killer_id: int
    def __init__(
        self,
        victim_id: int | None = ...,
        kill_shares: _Iterable[CDOTAUserMsg_StatsPlayerKillShare | _Mapping] | None = ...,
        damage_to_kill: int | None = ...,
        effective_health: int | None = ...,
        death_time: float | None = ...,
        killer_id: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_StatsMatchDetails(_message.Message):
    __slots__ = (
        "hero_lookup",
        "radiant_stats",
        "dire_stats",
        "radiant_kills",
        "dire_kills",
        "fight_details",
    )
    class CDOTAUserMsg_StatsFightTeamDetails(_message.Message):
        __slots__ = ("participants", "deaths", "gold_delta", "xp_delta")
        PARTICIPANTS_FIELD_NUMBER: _ClassVar[int]
        DEATHS_FIELD_NUMBER: _ClassVar[int]
        GOLD_DELTA_FIELD_NUMBER: _ClassVar[int]
        XP_DELTA_FIELD_NUMBER: _ClassVar[int]
        participants: _containers.RepeatedScalarFieldContainer[int]
        deaths: _containers.RepeatedScalarFieldContainer[int]
        gold_delta: int
        xp_delta: int
        def __init__(
            self,
            participants: _Iterable[int] | None = ...,
            deaths: _Iterable[int] | None = ...,
            gold_delta: int | None = ...,
            xp_delta: int | None = ...,
        ) -> None: ...

    class CDOTAUserMsg_StatsFightDetails(_message.Message):
        __slots__ = ("start_time", "end_time", "radiant_fight_details", "dire_fight_details")
        START_TIME_FIELD_NUMBER: _ClassVar[int]
        END_TIME_FIELD_NUMBER: _ClassVar[int]
        RADIANT_FIGHT_DETAILS_FIELD_NUMBER: _ClassVar[int]
        DIRE_FIGHT_DETAILS_FIELD_NUMBER: _ClassVar[int]
        start_time: float
        end_time: float
        radiant_fight_details: CDOTAUserMsg_StatsMatchDetails.CDOTAUserMsg_StatsFightTeamDetails
        dire_fight_details: CDOTAUserMsg_StatsMatchDetails.CDOTAUserMsg_StatsFightTeamDetails
        def __init__(
            self,
            start_time: float | None = ...,
            end_time: float | None = ...,
            radiant_fight_details: CDOTAUserMsg_StatsMatchDetails.CDOTAUserMsg_StatsFightTeamDetails
            | _Mapping
            | None = ...,
            dire_fight_details: CDOTAUserMsg_StatsMatchDetails.CDOTAUserMsg_StatsFightTeamDetails
            | _Mapping
            | None = ...,
        ) -> None: ...

    HERO_LOOKUP_FIELD_NUMBER: _ClassVar[int]
    RADIANT_STATS_FIELD_NUMBER: _ClassVar[int]
    DIRE_STATS_FIELD_NUMBER: _ClassVar[int]
    RADIANT_KILLS_FIELD_NUMBER: _ClassVar[int]
    DIRE_KILLS_FIELD_NUMBER: _ClassVar[int]
    FIGHT_DETAILS_FIELD_NUMBER: _ClassVar[int]
    hero_lookup: _containers.RepeatedCompositeFieldContainer[CDOTAUserMsg_StatsHeroLookup]
    radiant_stats: _containers.RepeatedCompositeFieldContainer[CDOTAUserMsg_StatsTeamMinuteDetails]
    dire_stats: _containers.RepeatedCompositeFieldContainer[CDOTAUserMsg_StatsTeamMinuteDetails]
    radiant_kills: _containers.RepeatedCompositeFieldContainer[CDOTAUserMsg_StatsKillDetails]
    dire_kills: _containers.RepeatedCompositeFieldContainer[CDOTAUserMsg_StatsKillDetails]
    fight_details: _containers.RepeatedCompositeFieldContainer[
        CDOTAUserMsg_StatsMatchDetails.CDOTAUserMsg_StatsFightDetails
    ]
    def __init__(
        self,
        hero_lookup: _Iterable[CDOTAUserMsg_StatsHeroLookup | _Mapping] | None = ...,
        radiant_stats: _Iterable[CDOTAUserMsg_StatsTeamMinuteDetails | _Mapping] | None = ...,
        dire_stats: _Iterable[CDOTAUserMsg_StatsTeamMinuteDetails | _Mapping] | None = ...,
        radiant_kills: _Iterable[CDOTAUserMsg_StatsKillDetails | _Mapping] | None = ...,
        dire_kills: _Iterable[CDOTAUserMsg_StatsKillDetails | _Mapping] | None = ...,
        fight_details: _Iterable[
            CDOTAUserMsg_StatsMatchDetails.CDOTAUserMsg_StatsFightDetails | _Mapping
        ]
        | None = ...,
    ) -> None: ...

class CDOTAUserMsg_MiniTaunt(_message.Message):
    __slots__ = ("taunting_player_id",)
    TAUNTING_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    taunting_player_id: int
    def __init__(self, taunting_player_id: int | None = ...) -> None: ...

class CDOTAUserMsg_SpeechBubble(_message.Message):
    __slots__ = ("destroy_all",)
    DESTROY_ALL_FIELD_NUMBER: _ClassVar[int]
    destroy_all: bool
    def __init__(self, destroy_all: bool = ...) -> None: ...

class CDOTAUserMsg_CustomHeaderMessage(_message.Message):
    __slots__ = ("player_id", "duration", "message", "value")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    duration: float
    message: str
    value: int
    def __init__(
        self,
        player_id: int | None = ...,
        duration: float | None = ...,
        message: str | None = ...,
        value: int | None = ...,
    ) -> None: ...

class CMsgHeroAbilityStat(_message.Message):
    __slots__ = ("stat_type", "int_value", "float_value")
    STAT_TYPE_FIELD_NUMBER: _ClassVar[int]
    INT_VALUE_FIELD_NUMBER: _ClassVar[int]
    FLOAT_VALUE_FIELD_NUMBER: _ClassVar[int]
    stat_type: EHeroStatType
    int_value: int
    float_value: float
    def __init__(
        self,
        stat_type: EHeroStatType | str | None = ...,
        int_value: int | None = ...,
        float_value: float | None = ...,
    ) -> None: ...

class CMsgCombatAnalyzerPlayerStat(_message.Message):
    __slots__ = ("account_id", "hero_ability_stats")
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    HERO_ABILITY_STATS_FIELD_NUMBER: _ClassVar[int]
    account_id: int
    hero_ability_stats: _containers.RepeatedCompositeFieldContainer[CMsgHeroAbilityStat]
    def __init__(
        self,
        account_id: int | None = ...,
        hero_ability_stats: _Iterable[CMsgHeroAbilityStat | _Mapping] | None = ...,
    ) -> None: ...

class CMsgCombatAnalyzerStats(_message.Message):
    __slots__ = ("match_id", "player_stats")
    MATCH_ID_FIELD_NUMBER: _ClassVar[int]
    PLAYER_STATS_FIELD_NUMBER: _ClassVar[int]
    match_id: int
    player_stats: _containers.RepeatedCompositeFieldContainer[CMsgCombatAnalyzerPlayerStat]
    def __init__(
        self,
        match_id: int | None = ...,
        player_stats: _Iterable[CMsgCombatAnalyzerPlayerStat | _Mapping] | None = ...,
    ) -> None: ...

class CDOTAUserMsg_BeastChat(_message.Message):
    __slots__ = ("team", "format", "message", "target")
    TEAM_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    team: int
    format: str
    message: str
    target: str
    def __init__(
        self,
        team: int | None = ...,
        format: str | None = ...,
        message: str | None = ...,
        target: str | None = ...,
    ) -> None: ...

class CDOTAUserMsg_CustomHudElement_Create(_message.Message):
    __slots__ = ("element_id", "layout_filename", "data")
    ELEMENT_ID_FIELD_NUMBER: _ClassVar[int]
    LAYOUT_FILENAME_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    element_id: str
    layout_filename: str
    data: bytes
    def __init__(
        self,
        element_id: str | None = ...,
        layout_filename: str | None = ...,
        data: bytes | None = ...,
    ) -> None: ...

class CDOTAUserMsg_CustomHudElement_Modify(_message.Message):
    __slots__ = ("element_id", "modify_visible", "data")
    ELEMENT_ID_FIELD_NUMBER: _ClassVar[int]
    MODIFY_VISIBLE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    element_id: str
    modify_visible: bool
    data: bytes
    def __init__(
        self, element_id: str | None = ..., modify_visible: bool = ..., data: bytes | None = ...
    ) -> None: ...

class CDOTAUserMsg_CustomHudElement_Destroy(_message.Message):
    __slots__ = ("element_id",)
    ELEMENT_ID_FIELD_NUMBER: _ClassVar[int]
    element_id: str
    def __init__(self, element_id: str | None = ...) -> None: ...

class CDOTAUserMsg_CompendiumStatePlayer(_message.Message):
    __slots__ = ("player_id", "level")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    level: int
    def __init__(self, player_id: int | None = ..., level: int | None = ...) -> None: ...

class CDOTAUserMsg_CompendiumState(_message.Message):
    __slots__ = ("compendium_players",)
    COMPENDIUM_PLAYERS_FIELD_NUMBER: _ClassVar[int]
    compendium_players: _containers.RepeatedCompositeFieldContainer[
        CDOTAUserMsg_CompendiumStatePlayer
    ]
    def __init__(
        self,
        compendium_players: _Iterable[CDOTAUserMsg_CompendiumStatePlayer | _Mapping] | None = ...,
    ) -> None: ...

class CDOTAUserMsg_ProjectionAbility(_message.Message):
    __slots__ = (
        "ability_id",
        "caster_ent_index",
        "caster_team",
        "channel_end",
        "origin",
        "track_caster_only",
        "end_time",
        "victim_ent_index",
    )
    ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    CASTER_ENT_INDEX_FIELD_NUMBER: _ClassVar[int]
    CASTER_TEAM_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_END_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    TRACK_CASTER_ONLY_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    VICTIM_ENT_INDEX_FIELD_NUMBER: _ClassVar[int]
    ability_id: int
    caster_ent_index: int
    caster_team: int
    channel_end: bool
    origin: _networkbasetypes_pb2.CMsgVector
    track_caster_only: bool
    end_time: float
    victim_ent_index: int
    def __init__(
        self,
        ability_id: int | None = ...,
        caster_ent_index: int | None = ...,
        caster_team: int | None = ...,
        channel_end: bool = ...,
        origin: _networkbasetypes_pb2.CMsgVector | _Mapping | None = ...,
        track_caster_only: bool = ...,
        end_time: float | None = ...,
        victim_ent_index: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_ProjectionEvent(_message.Message):
    __slots__ = ("event_id", "team")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_FIELD_NUMBER: _ClassVar[int]
    event_id: EProjectionEvent
    team: int
    def __init__(
        self, event_id: EProjectionEvent | str | None = ..., team: int | None = ...
    ) -> None: ...

class CDOTAUserMsg_XPAlert(_message.Message):
    __slots__ = ("player_id", "target_entindex")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    target_entindex: int
    def __init__(self, player_id: int | None = ..., target_entindex: int | None = ...) -> None: ...

class CDOTAUserMsg_TalentTreeAlert(_message.Message):
    __slots__ = ("player_id", "target_entindex", "ability_id", "slot", "learned")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    SLOT_FIELD_NUMBER: _ClassVar[int]
    LEARNED_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    target_entindex: int
    ability_id: int
    slot: int
    learned: bool
    def __init__(
        self,
        player_id: int | None = ...,
        target_entindex: int | None = ...,
        ability_id: int | None = ...,
        slot: int | None = ...,
        learned: bool = ...,
    ) -> None: ...

class CDOTAUserMsg_UpdateQuestProgress(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CDOTAUserMsg_QuestStatus(_message.Message):
    __slots__ = (
        "player_id",
        "quest_id",
        "challenge_id",
        "progress",
        "goal",
        "query",
        "fail_gametime",
        "item_ability_id",
    )
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    QUEST_ID_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_ID_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    GOAL_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    FAIL_GAMETIME_FIELD_NUMBER: _ClassVar[int]
    ITEM_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    quest_id: int
    challenge_id: int
    progress: int
    goal: int
    query: int
    fail_gametime: float
    item_ability_id: int
    def __init__(
        self,
        player_id: int | None = ...,
        quest_id: int | None = ...,
        challenge_id: int | None = ...,
        progress: int | None = ...,
        goal: int | None = ...,
        query: int | None = ...,
        fail_gametime: float | None = ...,
        item_ability_id: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_SuggestHeroPick(_message.Message):
    __slots__ = ("player_id", "hero_id", "ban", "facet_id")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    BAN_FIELD_NUMBER: _ClassVar[int]
    FACET_ID_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    hero_id: int
    ban: bool
    facet_id: int
    def __init__(
        self,
        player_id: int | None = ...,
        hero_id: int | None = ...,
        ban: bool = ...,
        facet_id: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_SuggestHeroRole(_message.Message):
    __slots__ = ("player_id", "hero_role")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    HERO_ROLE_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    hero_role: str
    def __init__(self, player_id: int | None = ..., hero_role: str | None = ...) -> None: ...

class CDOTAUserMsg_KillcamDamageTaken(_message.Message):
    __slots__ = (
        "player_id",
        "damage_taken",
        "item_type",
        "item_ability_id",
        "hero_name",
        "damage_color",
    )
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    DAMAGE_TAKEN_FIELD_NUMBER: _ClassVar[int]
    ITEM_TYPE_FIELD_NUMBER: _ClassVar[int]
    ITEM_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    HERO_NAME_FIELD_NUMBER: _ClassVar[int]
    DAMAGE_COLOR_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    damage_taken: int
    item_type: int
    item_ability_id: int
    hero_name: str
    damage_color: str
    def __init__(
        self,
        player_id: int | None = ...,
        damage_taken: int | None = ...,
        item_type: int | None = ...,
        item_ability_id: int | None = ...,
        hero_name: str | None = ...,
        damage_color: str | None = ...,
    ) -> None: ...

class CDOTAUserMsg_SelectPenaltyGold(_message.Message):
    __slots__ = ("player_id", "cost")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    COST_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    cost: int
    def __init__(self, player_id: int | None = ..., cost: int | None = ...) -> None: ...

class CDOTAUserMsg_RollDiceResult(_message.Message):
    __slots__ = ("player_id", "channel_type", "roll_min", "roll_max", "result")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    ROLL_MIN_FIELD_NUMBER: _ClassVar[int]
    ROLL_MAX_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    channel_type: int
    roll_min: int
    roll_max: int
    result: int
    def __init__(
        self,
        player_id: int | None = ...,
        channel_type: int | None = ...,
        roll_min: int | None = ...,
        roll_max: int | None = ...,
        result: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_FlipCoinResult(_message.Message):
    __slots__ = ("player_id", "channel_type", "result")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    channel_type: int
    result: bool
    def __init__(
        self, player_id: int | None = ..., channel_type: int | None = ..., result: bool = ...
    ) -> None: ...

class CDOTAUserMessage_RequestItemSuggestions(_message.Message):
    __slots__ = ("player_id",)
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    def __init__(self, player_id: int | None = ...) -> None: ...

class CDOTAUserMessage_TeamCaptainChanged(_message.Message):
    __slots__ = ("team", "captain_player_id")
    TEAM_FIELD_NUMBER: _ClassVar[int]
    CAPTAIN_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    team: int
    captain_player_id: int
    def __init__(self, team: int | None = ..., captain_player_id: int | None = ...) -> None: ...

class CDOTAUserMsg_ChatWheelCooldown(_message.Message):
    __slots__ = ("message_id", "cooldown_remaining")
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    COOLDOWN_REMAINING_FIELD_NUMBER: _ClassVar[int]
    message_id: int
    cooldown_remaining: float
    def __init__(
        self, message_id: int | None = ..., cooldown_remaining: float | None = ...
    ) -> None: ...

class CDOTAUserMsg_HeroRelicProgress(_message.Message):
    __slots__ = ("hero_relic_type", "value", "ehandle", "event_id", "value_display")
    HERO_RELIC_TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    EHANDLE_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    VALUE_DISPLAY_FIELD_NUMBER: _ClassVar[int]
    hero_relic_type: int
    value: int
    ehandle: int
    event_id: int
    value_display: float
    def __init__(
        self,
        hero_relic_type: int | None = ...,
        value: int | None = ...,
        ehandle: int | None = ...,
        event_id: int | None = ...,
        value_display: float | None = ...,
    ) -> None: ...

class CDOTAUserMsg_AbilityDraftRequestAbility(_message.Message):
    __slots__ = (
        "player_id",
        "requested_ability_id",
        "ctrl_is_down",
        "requested_hero_id",
        "requested_facet_key",
    )
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    CTRL_IS_DOWN_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_HERO_ID_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_FACET_KEY_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    requested_ability_id: int
    ctrl_is_down: bool
    requested_hero_id: int
    requested_facet_key: int
    def __init__(
        self,
        player_id: int | None = ...,
        requested_ability_id: int | None = ...,
        ctrl_is_down: bool = ...,
        requested_hero_id: int | None = ...,
        requested_facet_key: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_DamageReport(_message.Message):
    __slots__ = ("player_id", "target_hero_id", "source_hero_id", "damage_amount", "broadcast")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_HERO_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_HERO_ID_FIELD_NUMBER: _ClassVar[int]
    DAMAGE_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    BROADCAST_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    target_hero_id: int
    source_hero_id: int
    damage_amount: int
    broadcast: bool
    def __init__(
        self,
        player_id: int | None = ...,
        target_hero_id: int | None = ...,
        source_hero_id: int | None = ...,
        damage_amount: int | None = ...,
        broadcast: bool = ...,
    ) -> None: ...

class CDOTAUserMsg_SalutePlayer(_message.Message):
    __slots__ = (
        "source_player_id",
        "target_player_id",
        "tip_amount",
        "event_id",
        "custom_tip_style",
        "num_recent_tips",
    )
    SOURCE_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    TIP_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_TIP_STYLE_FIELD_NUMBER: _ClassVar[int]
    NUM_RECENT_TIPS_FIELD_NUMBER: _ClassVar[int]
    source_player_id: int
    target_player_id: int
    tip_amount: int
    event_id: int
    custom_tip_style: str
    num_recent_tips: int
    def __init__(
        self,
        source_player_id: int | None = ...,
        target_player_id: int | None = ...,
        tip_amount: int | None = ...,
        event_id: int | None = ...,
        custom_tip_style: str | None = ...,
        num_recent_tips: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_GiftPlayer(_message.Message):
    __slots__ = ("source_player_id", "target_player_id", "gift_item_def_index")
    SOURCE_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    GIFT_ITEM_DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
    source_player_id: int
    target_player_id: int
    gift_item_def_index: int
    def __init__(
        self,
        source_player_id: int | None = ...,
        target_player_id: int | None = ...,
        gift_item_def_index: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_TipAlert(_message.Message):
    __slots__ = ("player_id", "tip_text")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    TIP_TEXT_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    tip_text: str
    def __init__(self, player_id: int | None = ..., tip_text: str | None = ...) -> None: ...

class CDOTAUserMsg_ReplaceQueryUnit(_message.Message):
    __slots__ = ("player_id", "source_entindex", "target_entindex")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    TARGET_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    source_entindex: int
    target_entindex: int
    def __init__(
        self,
        player_id: int | None = ...,
        source_entindex: int | None = ...,
        target_entindex: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_ESArcanaCombo(_message.Message):
    __slots__ = ("ehandle", "combo_count", "arcana_level")
    EHANDLE_FIELD_NUMBER: _ClassVar[int]
    COMBO_COUNT_FIELD_NUMBER: _ClassVar[int]
    ARCANA_LEVEL_FIELD_NUMBER: _ClassVar[int]
    ehandle: int
    combo_count: int
    arcana_level: int
    def __init__(
        self,
        ehandle: int | None = ...,
        combo_count: int | None = ...,
        arcana_level: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_ESArcanaComboSummary(_message.Message):
    __slots__ = ("ehandle", "combo_count", "damage_amount")
    EHANDLE_FIELD_NUMBER: _ClassVar[int]
    COMBO_COUNT_FIELD_NUMBER: _ClassVar[int]
    DAMAGE_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    ehandle: int
    combo_count: int
    damage_amount: int
    def __init__(
        self,
        ehandle: int | None = ...,
        combo_count: int | None = ...,
        damage_amount: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_OMArcanaCombo(_message.Message):
    __slots__ = ("ehandle", "multicast_amount", "arcana_level", "multicast_chance")
    EHANDLE_FIELD_NUMBER: _ClassVar[int]
    MULTICAST_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    ARCANA_LEVEL_FIELD_NUMBER: _ClassVar[int]
    MULTICAST_CHANCE_FIELD_NUMBER: _ClassVar[int]
    ehandle: int
    multicast_amount: int
    arcana_level: int
    multicast_chance: int
    def __init__(
        self,
        ehandle: int | None = ...,
        multicast_amount: int | None = ...,
        arcana_level: int | None = ...,
        multicast_chance: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_HighFiveCompleted(_message.Message):
    __slots__ = ("player_id_1", "player_id_2", "special_high_five", "special_entindex")
    PLAYER_ID_1_FIELD_NUMBER: _ClassVar[int]
    PLAYER_ID_2_FIELD_NUMBER: _ClassVar[int]
    SPECIAL_HIGH_FIVE_FIELD_NUMBER: _ClassVar[int]
    SPECIAL_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    player_id_1: int
    player_id_2: int
    special_high_five: bool
    special_entindex: int
    def __init__(
        self,
        player_id_1: int | None = ...,
        player_id_2: int | None = ...,
        special_high_five: bool = ...,
        special_entindex: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_HighFiveLeftHanging(_message.Message):
    __slots__ = ("player_id",)
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    def __init__(self, player_id: int | None = ...) -> None: ...

class CDOTAUserMsg_ShovelUnearth(_message.Message):
    __slots__ = ("player_id", "all_chat", "locstring", "quantity")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    ALL_CHAT_FIELD_NUMBER: _ClassVar[int]
    LOCSTRING_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    all_chat: bool
    locstring: str
    quantity: int
    def __init__(
        self,
        player_id: int | None = ...,
        all_chat: bool = ...,
        locstring: str | None = ...,
        quantity: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_AllStarEvent(_message.Message):
    __slots__ = (
        "source_player_id",
        "target_player_id",
        "point_amount",
        "event_id",
        "player_scores",
    )
    class PlayerScore(_message.Message):
        __slots__ = ("player_id", "score_sans_kda")
        PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
        SCORE_SANS_KDA_FIELD_NUMBER: _ClassVar[int]
        player_id: int
        score_sans_kda: int
        def __init__(
            self, player_id: int | None = ..., score_sans_kda: int | None = ...
        ) -> None: ...

    SOURCE_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    POINT_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    PLAYER_SCORES_FIELD_NUMBER: _ClassVar[int]
    source_player_id: int
    target_player_id: int
    point_amount: int
    event_id: int
    player_scores: _containers.RepeatedCompositeFieldContainer[
        CDOTAUserMsg_AllStarEvent.PlayerScore
    ]
    def __init__(
        self,
        source_player_id: int | None = ...,
        target_player_id: int | None = ...,
        point_amount: int | None = ...,
        event_id: int | None = ...,
        player_scores: _Iterable[CDOTAUserMsg_AllStarEvent.PlayerScore | _Mapping] | None = ...,
    ) -> None: ...

class CDOTAUserMsg_QueuedOrderRemoved(_message.Message):
    __slots__ = ("unit_order_sequence",)
    UNIT_ORDER_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    unit_order_sequence: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, unit_order_sequence: _Iterable[int] | None = ...) -> None: ...

class CDOTAUserMsg_DebugChallenge(_message.Message):
    __slots__ = (
        "challenge_type",
        "challenge_query_id",
        "event_id",
        "instance_id",
        "challenge_var_0",
        "challenge_var_1",
        "challenge_max_rank",
    )
    CHALLENGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_VAR_0_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_VAR_1_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_MAX_RANK_FIELD_NUMBER: _ClassVar[int]
    challenge_type: int
    challenge_query_id: int
    event_id: int
    instance_id: int
    challenge_var_0: int
    challenge_var_1: int
    challenge_max_rank: int
    def __init__(
        self,
        challenge_type: int | None = ...,
        challenge_query_id: int | None = ...,
        event_id: int | None = ...,
        instance_id: int | None = ...,
        challenge_var_0: int | None = ...,
        challenge_var_1: int | None = ...,
        challenge_max_rank: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_FoundNeutralItem(_message.Message):
    __slots__ = (
        "player_id",
        "item_ability_id",
        "item_tier",
        "tier_item_count",
        "enhancement_ability_id",
        "enhancement_level",
        "trinket_level",
    )
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_TIER_FIELD_NUMBER: _ClassVar[int]
    TIER_ITEM_COUNT_FIELD_NUMBER: _ClassVar[int]
    ENHANCEMENT_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    ENHANCEMENT_LEVEL_FIELD_NUMBER: _ClassVar[int]
    TRINKET_LEVEL_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    item_ability_id: int
    item_tier: int
    tier_item_count: int
    enhancement_ability_id: int
    enhancement_level: int
    trinket_level: int
    def __init__(
        self,
        player_id: int | None = ...,
        item_ability_id: int | None = ...,
        item_tier: int | None = ...,
        tier_item_count: int | None = ...,
        enhancement_ability_id: int | None = ...,
        enhancement_level: int | None = ...,
        trinket_level: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_OutpostCaptured(_message.Message):
    __slots__ = ("outpost_entindex", "team_id")
    OUTPOST_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    outpost_entindex: int
    team_id: int
    def __init__(self, outpost_entindex: int | None = ..., team_id: int | None = ...) -> None: ...

class CDOTAUserMsg_OutpostGrantedXP(_message.Message):
    __slots__ = ("team_id", "xp_amount")
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    XP_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    team_id: int
    xp_amount: int
    def __init__(self, team_id: int | None = ..., xp_amount: int | None = ...) -> None: ...

class CDOTAUserMsg_MoveCameraToUnit(_message.Message):
    __slots__ = ("unit_ehandle",)
    UNIT_EHANDLE_FIELD_NUMBER: _ClassVar[int]
    unit_ehandle: int
    def __init__(self, unit_ehandle: int | None = ...) -> None: ...

class CDOTAUserMsg_PauseMinigameData(_message.Message):
    __slots__ = ("data_bits",)
    class DataBit(_message.Message):
        __slots__ = ("index", "data", "data_extra")
        INDEX_FIELD_NUMBER: _ClassVar[int]
        DATA_FIELD_NUMBER: _ClassVar[int]
        DATA_EXTRA_FIELD_NUMBER: _ClassVar[int]
        index: int
        data: int
        data_extra: int
        def __init__(
            self, index: int | None = ..., data: int | None = ..., data_extra: int | None = ...
        ) -> None: ...

    DATA_BITS_FIELD_NUMBER: _ClassVar[int]
    data_bits: _containers.RepeatedCompositeFieldContainer[CDOTAUserMsg_PauseMinigameData.DataBit]
    def __init__(
        self, data_bits: _Iterable[CDOTAUserMsg_PauseMinigameData.DataBit | _Mapping] | None = ...
    ) -> None: ...

class CDOTAUserMsg_VersusScene_PlayerBehavior(_message.Message):
    __slots__ = ("player_id", "behavior", "play_activity", "chat_wheel", "playback_rate")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    PLAY_ACTIVITY_FIELD_NUMBER: _ClassVar[int]
    CHAT_WHEEL_FIELD_NUMBER: _ClassVar[int]
    PLAYBACK_RATE_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    behavior: _dota_commonmessages_pb2.EDOTAVersusScenePlayerBehavior
    play_activity: _dota_commonmessages_pb2.VersusScene_PlayActivity
    chat_wheel: _dota_commonmessages_pb2.VersusScene_ChatWheel
    playback_rate: _dota_commonmessages_pb2.VersusScene_PlaybackRate
    def __init__(
        self,
        player_id: int | None = ...,
        behavior: _dota_commonmessages_pb2.EDOTAVersusScenePlayerBehavior | str | None = ...,
        play_activity: _dota_commonmessages_pb2.VersusScene_PlayActivity | _Mapping | None = ...,
        chat_wheel: _dota_commonmessages_pb2.VersusScene_ChatWheel | _Mapping | None = ...,
        playback_rate: _dota_commonmessages_pb2.VersusScene_PlaybackRate | _Mapping | None = ...,
    ) -> None: ...

class CDOTAUserMsg_QoP_ArcanaSummary(_message.Message):
    __slots__ = ("ehandle", "arcana_level", "players_hit", "players_killed")
    EHANDLE_FIELD_NUMBER: _ClassVar[int]
    ARCANA_LEVEL_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_HIT_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_KILLED_FIELD_NUMBER: _ClassVar[int]
    ehandle: int
    arcana_level: int
    players_hit: int
    players_killed: int
    def __init__(
        self,
        ehandle: int | None = ...,
        arcana_level: int | None = ...,
        players_hit: int | None = ...,
        players_killed: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_HotPotato_Created(_message.Message):
    __slots__ = ("player_id_1", "player_id_2")
    PLAYER_ID_1_FIELD_NUMBER: _ClassVar[int]
    PLAYER_ID_2_FIELD_NUMBER: _ClassVar[int]
    player_id_1: int
    player_id_2: int
    def __init__(self, player_id_1: int | None = ..., player_id_2: int | None = ...) -> None: ...

class CDOTAUserMsg_HotPotato_Exploded(_message.Message):
    __slots__ = ("player_id",)
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    def __init__(self, player_id: int | None = ...) -> None: ...

class CDOTAUserMsg_WK_Arcana_Progress(_message.Message):
    __slots__ = ("ehandle", "arcana_level", "hero_id")
    EHANDLE_FIELD_NUMBER: _ClassVar[int]
    ARCANA_LEVEL_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    ehandle: int
    arcana_level: int
    hero_id: int
    def __init__(
        self, ehandle: int | None = ..., arcana_level: int | None = ..., hero_id: int | None = ...
    ) -> None: ...

class CDOTAUserMsg_GuildChallenge_Progress(_message.Message):
    __slots__ = (
        "player_progress",
        "guild_id",
        "challenge_instance_id",
        "challenge_parameter",
        "challenge_type",
        "challenge_progress_at_start",
        "complete",
    )
    class EChallengeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        k_EChallengeType_Invalid: _ClassVar[CDOTAUserMsg_GuildChallenge_Progress.EChallengeType]
        k_EChallengeType_Cooperative: _ClassVar[CDOTAUserMsg_GuildChallenge_Progress.EChallengeType]
        k_EChallengeType_Contract: _ClassVar[CDOTAUserMsg_GuildChallenge_Progress.EChallengeType]

    k_EChallengeType_Invalid: CDOTAUserMsg_GuildChallenge_Progress.EChallengeType
    k_EChallengeType_Cooperative: CDOTAUserMsg_GuildChallenge_Progress.EChallengeType
    k_EChallengeType_Contract: CDOTAUserMsg_GuildChallenge_Progress.EChallengeType
    class PlayerProgress(_message.Message):
        __slots__ = ("player_id", "progress")
        PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
        PROGRESS_FIELD_NUMBER: _ClassVar[int]
        player_id: int
        progress: int
        def __init__(self, player_id: int | None = ..., progress: int | None = ...) -> None: ...

    PLAYER_PROGRESS_FIELD_NUMBER: _ClassVar[int]
    GUILD_ID_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_PARAMETER_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_PROGRESS_AT_START_FIELD_NUMBER: _ClassVar[int]
    COMPLETE_FIELD_NUMBER: _ClassVar[int]
    player_progress: _containers.RepeatedCompositeFieldContainer[
        CDOTAUserMsg_GuildChallenge_Progress.PlayerProgress
    ]
    guild_id: int
    challenge_instance_id: int
    challenge_parameter: int
    challenge_type: CDOTAUserMsg_GuildChallenge_Progress.EChallengeType
    challenge_progress_at_start: int
    complete: bool
    def __init__(
        self,
        player_progress: _Iterable[CDOTAUserMsg_GuildChallenge_Progress.PlayerProgress | _Mapping]
        | None = ...,
        guild_id: int | None = ...,
        challenge_instance_id: int | None = ...,
        challenge_parameter: int | None = ...,
        challenge_type: CDOTAUserMsg_GuildChallenge_Progress.EChallengeType | str | None = ...,
        challenge_progress_at_start: int | None = ...,
        complete: bool = ...,
    ) -> None: ...

class CDOTAUserMsg_WRArcanaProgress(_message.Message):
    __slots__ = (
        "ehandle",
        "target_ehandle",
        "arrows_landed",
        "damage_dealt",
        "target_hp",
        "target_max_hp",
        "arcana_level",
    )
    EHANDLE_FIELD_NUMBER: _ClassVar[int]
    TARGET_EHANDLE_FIELD_NUMBER: _ClassVar[int]
    ARROWS_LANDED_FIELD_NUMBER: _ClassVar[int]
    DAMAGE_DEALT_FIELD_NUMBER: _ClassVar[int]
    TARGET_HP_FIELD_NUMBER: _ClassVar[int]
    TARGET_MAX_HP_FIELD_NUMBER: _ClassVar[int]
    ARCANA_LEVEL_FIELD_NUMBER: _ClassVar[int]
    ehandle: int
    target_ehandle: int
    arrows_landed: int
    damage_dealt: int
    target_hp: int
    target_max_hp: int
    arcana_level: int
    def __init__(
        self,
        ehandle: int | None = ...,
        target_ehandle: int | None = ...,
        arrows_landed: int | None = ...,
        damage_dealt: int | None = ...,
        target_hp: int | None = ...,
        target_max_hp: int | None = ...,
        arcana_level: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_WRArcanaSummary(_message.Message):
    __slots__ = (
        "ehandle",
        "target_ehandle",
        "arrows_landed",
        "damage_dealt",
        "target_hp",
        "target_max_hp",
        "arcana_level",
        "success",
    )
    EHANDLE_FIELD_NUMBER: _ClassVar[int]
    TARGET_EHANDLE_FIELD_NUMBER: _ClassVar[int]
    ARROWS_LANDED_FIELD_NUMBER: _ClassVar[int]
    DAMAGE_DEALT_FIELD_NUMBER: _ClassVar[int]
    TARGET_HP_FIELD_NUMBER: _ClassVar[int]
    TARGET_MAX_HP_FIELD_NUMBER: _ClassVar[int]
    ARCANA_LEVEL_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ehandle: int
    target_ehandle: int
    arrows_landed: int
    damage_dealt: int
    target_hp: int
    target_max_hp: int
    arcana_level: int
    success: bool
    def __init__(
        self,
        ehandle: int | None = ...,
        target_ehandle: int | None = ...,
        arrows_landed: int | None = ...,
        damage_dealt: int | None = ...,
        target_hp: int | None = ...,
        target_max_hp: int | None = ...,
        arcana_level: int | None = ...,
        success: bool = ...,
    ) -> None: ...

class CDOTAUserMsg_EmptyItemSlotAlert(_message.Message):
    __slots__ = ("source_player_id", "target_player_id", "slot_index", "cooldown_seconds")
    SOURCE_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    SLOT_INDEX_FIELD_NUMBER: _ClassVar[int]
    COOLDOWN_SECONDS_FIELD_NUMBER: _ClassVar[int]
    source_player_id: int
    target_player_id: int
    slot_index: int
    cooldown_seconds: int
    def __init__(
        self,
        source_player_id: int | None = ...,
        target_player_id: int | None = ...,
        slot_index: int | None = ...,
        cooldown_seconds: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_AghsStatusAlert(_message.Message):
    __slots__ = (
        "source_player_id",
        "target_player_id",
        "target_entindex",
        "alert_type",
        "has_scepter",
        "has_shard",
    )
    SOURCE_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    ALERT_TYPE_FIELD_NUMBER: _ClassVar[int]
    HAS_SCEPTER_FIELD_NUMBER: _ClassVar[int]
    HAS_SHARD_FIELD_NUMBER: _ClassVar[int]
    source_player_id: int
    target_player_id: int
    target_entindex: int
    alert_type: int
    has_scepter: bool
    has_shard: bool
    def __init__(
        self,
        source_player_id: int | None = ...,
        target_player_id: int | None = ...,
        target_entindex: int | None = ...,
        alert_type: int | None = ...,
        has_scepter: bool = ...,
        has_shard: bool = ...,
    ) -> None: ...

class CDOTAUserMsg_MutedPlayers(_message.Message):
    __slots__ = ("text_muted_player_ids", "voice_muted_player_ids")
    TEXT_MUTED_PLAYER_IDS_FIELD_NUMBER: _ClassVar[int]
    VOICE_MUTED_PLAYER_IDS_FIELD_NUMBER: _ClassVar[int]
    text_muted_player_ids: _containers.RepeatedScalarFieldContainer[int]
    voice_muted_player_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        text_muted_player_ids: _Iterable[int] | None = ...,
        voice_muted_player_ids: _Iterable[int] | None = ...,
    ) -> None: ...

class CDOTAUserMsg_ContextualTip(_message.Message):
    __slots__ = (
        "tip_id",
        "referenced_abilities",
        "referenced_units",
        "panorama_classes",
        "force_annotation",
        "variant",
        "int_param",
        "int_param2",
        "float_param",
        "float_param2",
        "string_param",
        "string_param2",
        "tip_text_override",
        "tip_annotation_override",
        "panorama_snippet",
    )
    TIP_ID_FIELD_NUMBER: _ClassVar[int]
    REFERENCED_ABILITIES_FIELD_NUMBER: _ClassVar[int]
    REFERENCED_UNITS_FIELD_NUMBER: _ClassVar[int]
    PANORAMA_CLASSES_FIELD_NUMBER: _ClassVar[int]
    FORCE_ANNOTATION_FIELD_NUMBER: _ClassVar[int]
    VARIANT_FIELD_NUMBER: _ClassVar[int]
    INT_PARAM_FIELD_NUMBER: _ClassVar[int]
    INT_PARAM2_FIELD_NUMBER: _ClassVar[int]
    FLOAT_PARAM_FIELD_NUMBER: _ClassVar[int]
    FLOAT_PARAM2_FIELD_NUMBER: _ClassVar[int]
    STRING_PARAM_FIELD_NUMBER: _ClassVar[int]
    STRING_PARAM2_FIELD_NUMBER: _ClassVar[int]
    TIP_TEXT_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    TIP_ANNOTATION_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    PANORAMA_SNIPPET_FIELD_NUMBER: _ClassVar[int]
    tip_id: int
    referenced_abilities: _containers.RepeatedScalarFieldContainer[str]
    referenced_units: _containers.RepeatedScalarFieldContainer[str]
    panorama_classes: _containers.RepeatedScalarFieldContainer[str]
    force_annotation: bool
    variant: int
    int_param: int
    int_param2: int
    float_param: float
    float_param2: float
    string_param: str
    string_param2: str
    tip_text_override: str
    tip_annotation_override: str
    panorama_snippet: str
    def __init__(
        self,
        tip_id: int | None = ...,
        referenced_abilities: _Iterable[str] | None = ...,
        referenced_units: _Iterable[str] | None = ...,
        panorama_classes: _Iterable[str] | None = ...,
        force_annotation: bool = ...,
        variant: int | None = ...,
        int_param: int | None = ...,
        int_param2: int | None = ...,
        float_param: float | None = ...,
        float_param2: float | None = ...,
        string_param: str | None = ...,
        string_param2: str | None = ...,
        tip_text_override: str | None = ...,
        tip_annotation_override: str | None = ...,
        panorama_snippet: str | None = ...,
    ) -> None: ...

class CDOTAUserMsg_ChatMessage(_message.Message):
    __slots__ = ("source_player_id", "channel_type", "message_text")
    SOURCE_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_TEXT_FIELD_NUMBER: _ClassVar[int]
    source_player_id: int
    channel_type: int
    message_text: str
    def __init__(
        self,
        source_player_id: int | None = ...,
        channel_type: int | None = ...,
        message_text: str | None = ...,
    ) -> None: ...

class CDOTAUserMsg_RockPaperScissorsStarted(_message.Message):
    __slots__ = ("player_id_source", "player_id_target")
    PLAYER_ID_SOURCE_FIELD_NUMBER: _ClassVar[int]
    PLAYER_ID_TARGET_FIELD_NUMBER: _ClassVar[int]
    player_id_source: int
    player_id_target: int
    def __init__(
        self, player_id_source: int | None = ..., player_id_target: int | None = ...
    ) -> None: ...

class CDOTAUserMsg_RockPaperScissorsFinished(_message.Message):
    __slots__ = ("player_id_1", "player_id_2", "player_1_choice", "player_2_choice")
    PLAYER_ID_1_FIELD_NUMBER: _ClassVar[int]
    PLAYER_ID_2_FIELD_NUMBER: _ClassVar[int]
    PLAYER_1_CHOICE_FIELD_NUMBER: _ClassVar[int]
    PLAYER_2_CHOICE_FIELD_NUMBER: _ClassVar[int]
    player_id_1: int
    player_id_2: int
    player_1_choice: int
    player_2_choice: int
    def __init__(
        self,
        player_id_1: int | None = ...,
        player_id_2: int | None = ...,
        player_1_choice: int | None = ...,
        player_2_choice: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_DuelOpponentKilled(_message.Message):
    __slots__ = ("player_id_winner", "player_id_loser")
    PLAYER_ID_WINNER_FIELD_NUMBER: _ClassVar[int]
    PLAYER_ID_LOSER_FIELD_NUMBER: _ClassVar[int]
    player_id_winner: int
    player_id_loser: int
    def __init__(
        self, player_id_winner: int | None = ..., player_id_loser: int | None = ...
    ) -> None: ...

class CDOTAUserMsg_DuelAccepted(_message.Message):
    __slots__ = ("player_id_1", "player_id_2")
    PLAYER_ID_1_FIELD_NUMBER: _ClassVar[int]
    PLAYER_ID_2_FIELD_NUMBER: _ClassVar[int]
    player_id_1: int
    player_id_2: int
    def __init__(self, player_id_1: int | None = ..., player_id_2: int | None = ...) -> None: ...

class CDOTAUserMsg_DuelRequested(_message.Message):
    __slots__ = ("player_id_requestor",)
    PLAYER_ID_REQUESTOR_FIELD_NUMBER: _ClassVar[int]
    player_id_requestor: int
    def __init__(self, player_id_requestor: int | None = ...) -> None: ...

class CDOTAUserMsg_MuertaReleaseEvent_AssignedTargetKilled(_message.Message):
    __slots__ = ("player_id_killer", "player_id_target", "points", "points_total", "last_hit")
    PLAYER_ID_KILLER_FIELD_NUMBER: _ClassVar[int]
    PLAYER_ID_TARGET_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    POINTS_TOTAL_FIELD_NUMBER: _ClassVar[int]
    LAST_HIT_FIELD_NUMBER: _ClassVar[int]
    player_id_killer: int
    player_id_target: int
    points: int
    points_total: int
    last_hit: bool
    def __init__(
        self,
        player_id_killer: int | None = ...,
        player_id_target: int | None = ...,
        points: int | None = ...,
        points_total: int | None = ...,
        last_hit: bool = ...,
    ) -> None: ...

class CDOTAUserMsg_PlayerDraftSuggestPick(_message.Message):
    __slots__ = ("player_id", "suggestion_player_id")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    SUGGESTION_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    suggestion_player_id: int
    def __init__(
        self, player_id: int | None = ..., suggestion_player_id: int | None = ...
    ) -> None: ...

class CDOTAUserMsg_PlayerDraftPick(_message.Message):
    __slots__ = ("player_id_captain", "player_id_target", "team")
    PLAYER_ID_CAPTAIN_FIELD_NUMBER: _ClassVar[int]
    PLAYER_ID_TARGET_FIELD_NUMBER: _ClassVar[int]
    TEAM_FIELD_NUMBER: _ClassVar[int]
    player_id_captain: int
    player_id_target: int
    team: int
    def __init__(
        self,
        player_id_captain: int | None = ...,
        player_id_target: int | None = ...,
        team: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_FacetPing(_message.Message):
    __slots__ = ("player_id", "facet_strhash", "entity_id", "all_chat")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    FACET_STRHASH_FIELD_NUMBER: _ClassVar[int]
    ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    ALL_CHAT_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    facet_strhash: int
    entity_id: int
    all_chat: bool
    def __init__(
        self,
        player_id: int | None = ...,
        facet_strhash: int | None = ...,
        entity_id: int | None = ...,
        all_chat: bool = ...,
    ) -> None: ...

class CDOTAUserMsg_InnatePing(_message.Message):
    __slots__ = ("player_id", "entity_id", "all_chat")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    ALL_CHAT_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    entity_id: int
    all_chat: bool
    def __init__(
        self, player_id: int | None = ..., entity_id: int | None = ..., all_chat: bool = ...
    ) -> None: ...

class CDOTAUserMsg_NeutralCraftAvailable(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CDOTAUserMsg_TimerAlert(_message.Message):
    __slots__ = ("player_id", "timer_alert_type")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    TIMER_ALERT_TYPE_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    timer_alert_type: _dota_shared_enums_pb2.ETimerAlertType
    def __init__(
        self,
        player_id: int | None = ...,
        timer_alert_type: _dota_shared_enums_pb2.ETimerAlertType | str | None = ...,
    ) -> None: ...

class CDOTAUserMsg_MadstoneAlert(_message.Message):
    __slots__ = ("player_id", "target_entindex", "tier", "madstone_alert_type", "value")
    class EMadstoneAlertType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CraftAvailable: _ClassVar[CDOTAUserMsg_MadstoneAlert.EMadstoneAlertType]
        NeedMadstone: _ClassVar[CDOTAUserMsg_MadstoneAlert.EMadstoneAlertType]
        WaitingForNextTier: _ClassVar[CDOTAUserMsg_MadstoneAlert.EMadstoneAlertType]

    CraftAvailable: CDOTAUserMsg_MadstoneAlert.EMadstoneAlertType
    NeedMadstone: CDOTAUserMsg_MadstoneAlert.EMadstoneAlertType
    WaitingForNextTier: CDOTAUserMsg_MadstoneAlert.EMadstoneAlertType
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    TIER_FIELD_NUMBER: _ClassVar[int]
    MADSTONE_ALERT_TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    target_entindex: int
    tier: int
    madstone_alert_type: CDOTAUserMsg_MadstoneAlert.EMadstoneAlertType
    value: int
    def __init__(
        self,
        player_id: int | None = ...,
        target_entindex: int | None = ...,
        tier: int | None = ...,
        madstone_alert_type: CDOTAUserMsg_MadstoneAlert.EMadstoneAlertType | str | None = ...,
        value: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_MonsterHunter_InvestigationsAvailable(_message.Message):
    __slots__ = ("investigations",)
    INVESTIGATIONS_FIELD_NUMBER: _ClassVar[int]
    investigations: _containers.RepeatedCompositeFieldContainer[
        _dota_shared_enums_pb2.CMsgMonsterHunterInvestigation
    ]
    def __init__(
        self,
        investigations: _Iterable[_dota_shared_enums_pb2.CMsgMonsterHunterInvestigation | _Mapping]
        | None = ...,
    ) -> None: ...

class CDOTAUserMsg_MonsterHunter_InvestigationGameState(_message.Message):
    __slots__ = ("investigation_game_state", "investigations_locked")
    INVESTIGATION_GAME_STATE_FIELD_NUMBER: _ClassVar[int]
    INVESTIGATIONS_LOCKED_FIELD_NUMBER: _ClassVar[int]
    investigation_game_state: _dota_shared_enums_pb2.CMsgMonsterHunterInvestigationGameState
    investigations_locked: bool
    def __init__(
        self,
        investigation_game_state: _dota_shared_enums_pb2.CMsgMonsterHunterInvestigationGameState
        | _Mapping
        | None = ...,
        investigations_locked: bool = ...,
    ) -> None: ...

class CDOTAUserMsg_MonsterHunter_HuntAlert(_message.Message):
    __slots__ = ("player_id", "hero_id", "hunt_alert_type", "hunt_status_type", "index")
    class EHuntAlertType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        MainObjective: _ClassVar[CDOTAUserMsg_MonsterHunter_HuntAlert.EHuntAlertType]
        MainObjectiveAll: _ClassVar[CDOTAUserMsg_MonsterHunter_HuntAlert.EHuntAlertType]
        HuntedBy: _ClassVar[CDOTAUserMsg_MonsterHunter_HuntAlert.EHuntAlertType]
        HuntedByAll: _ClassVar[CDOTAUserMsg_MonsterHunter_HuntAlert.EHuntAlertType]
        HunterDuel: _ClassVar[CDOTAUserMsg_MonsterHunter_HuntAlert.EHuntAlertType]
        HunterDuelAll: _ClassVar[CDOTAUserMsg_MonsterHunter_HuntAlert.EHuntAlertType]
        HuntSelection: _ClassVar[CDOTAUserMsg_MonsterHunter_HuntAlert.EHuntAlertType]

    MainObjective: CDOTAUserMsg_MonsterHunter_HuntAlert.EHuntAlertType
    MainObjectiveAll: CDOTAUserMsg_MonsterHunter_HuntAlert.EHuntAlertType
    HuntedBy: CDOTAUserMsg_MonsterHunter_HuntAlert.EHuntAlertType
    HuntedByAll: CDOTAUserMsg_MonsterHunter_HuntAlert.EHuntAlertType
    HunterDuel: CDOTAUserMsg_MonsterHunter_HuntAlert.EHuntAlertType
    HunterDuelAll: CDOTAUserMsg_MonsterHunter_HuntAlert.EHuntAlertType
    HuntSelection: CDOTAUserMsg_MonsterHunter_HuntAlert.EHuntAlertType
    class EHuntStatusType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        Pending: _ClassVar[CDOTAUserMsg_MonsterHunter_HuntAlert.EHuntStatusType]
        Success: _ClassVar[CDOTAUserMsg_MonsterHunter_HuntAlert.EHuntStatusType]
        Failed: _ClassVar[CDOTAUserMsg_MonsterHunter_HuntAlert.EHuntStatusType]

    Pending: CDOTAUserMsg_MonsterHunter_HuntAlert.EHuntStatusType
    Success: CDOTAUserMsg_MonsterHunter_HuntAlert.EHuntStatusType
    Failed: CDOTAUserMsg_MonsterHunter_HuntAlert.EHuntStatusType
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    HUNT_ALERT_TYPE_FIELD_NUMBER: _ClassVar[int]
    HUNT_STATUS_TYPE_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    hero_id: int
    hunt_alert_type: CDOTAUserMsg_MonsterHunter_HuntAlert.EHuntAlertType
    hunt_status_type: CDOTAUserMsg_MonsterHunter_HuntAlert.EHuntStatusType
    index: int
    def __init__(
        self,
        player_id: int | None = ...,
        hero_id: int | None = ...,
        hunt_alert_type: CDOTAUserMsg_MonsterHunter_HuntAlert.EHuntAlertType | str | None = ...,
        hunt_status_type: CDOTAUserMsg_MonsterHunter_HuntAlert.EHuntStatusType | str | None = ...,
        index: int | None = ...,
    ) -> None: ...

class CDOTAUserMsg_KillEffect(_message.Message):
    __slots__ = ("victim_ent_index", "killer_player_id")
    VICTIM_ENT_INDEX_FIELD_NUMBER: _ClassVar[int]
    KILLER_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    victim_ent_index: int
    killer_player_id: int
    def __init__(
        self, victim_ent_index: int | None = ..., killer_player_id: int | None = ...
    ) -> None: ...
