from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

import base_gcmessages_pb2 as _base_gcmessages_pb2
import dota_commonmessages_pb2 as _dota_commonmessages_pb2
import dota_shared_enums_pb2 as _dota_shared_enums_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class EDotaClientMessages(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DOTA_CM_MapLine: _ClassVar[EDotaClientMessages]
    DOTA_CM_AspectRatio: _ClassVar[EDotaClientMessages]
    DOTA_CM_MapPing: _ClassVar[EDotaClientMessages]
    DOTA_CM_UnitsAutoAttack: _ClassVar[EDotaClientMessages]
    DOTA_CM_SearchString: _ClassVar[EDotaClientMessages]
    DOTA_CM_Pause: _ClassVar[EDotaClientMessages]
    DOTA_CM_ShopViewMode: _ClassVar[EDotaClientMessages]
    DOTA_CM_SetUnitShareFlag: _ClassVar[EDotaClientMessages]
    DOTA_CM_SwapRequest: _ClassVar[EDotaClientMessages]
    DOTA_CM_SwapAccept: _ClassVar[EDotaClientMessages]
    DOTA_CM_WorldLine: _ClassVar[EDotaClientMessages]
    DOTA_CM_RequestGraphUpdate: _ClassVar[EDotaClientMessages]
    DOTA_CM_ItemAlert: _ClassVar[EDotaClientMessages]
    DOTA_CM_ChatWheel: _ClassVar[EDotaClientMessages]
    DOTA_CM_SendStatPopup: _ClassVar[EDotaClientMessages]
    DOTA_CM_BeginLastHitChallenge: _ClassVar[EDotaClientMessages]
    DOTA_CM_UpdateQuickBuy: _ClassVar[EDotaClientMessages]
    DOTA_CM_UpdateCoachListen: _ClassVar[EDotaClientMessages]
    DOTA_CM_CoachHUDPing: _ClassVar[EDotaClientMessages]
    DOTA_CM_RecordVote: _ClassVar[EDotaClientMessages]
    DOTA_CM_UnitsAutoAttackAfterSpell: _ClassVar[EDotaClientMessages]
    DOTA_CM_WillPurchaseAlert: _ClassVar[EDotaClientMessages]
    DOTA_CM_PlayerShowCase: _ClassVar[EDotaClientMessages]
    DOTA_CM_TeleportRequiresHalt: _ClassVar[EDotaClientMessages]
    DOTA_CM_CameraZoomAmount: _ClassVar[EDotaClientMessages]
    DOTA_CM_BroadcasterUsingCamerman: _ClassVar[EDotaClientMessages]
    DOTA_CM_BroadcasterUsingAssistedCameraOperator: _ClassVar[EDotaClientMessages]
    DOTA_CM_EnemyItemAlert: _ClassVar[EDotaClientMessages]
    DOTA_CM_FreeInventory: _ClassVar[EDotaClientMessages]
    DOTA_CM_BuyBackStateAlert: _ClassVar[EDotaClientMessages]
    DOTA_CM_QuickBuyAlert: _ClassVar[EDotaClientMessages]
    DOTA_CM_HeroStatueLike: _ClassVar[EDotaClientMessages]
    DOTA_CM_ModifierAlert: _ClassVar[EDotaClientMessages]
    DOTA_CM_TeamShowcaseEditor: _ClassVar[EDotaClientMessages]
    DOTA_CM_HPManaAlert: _ClassVar[EDotaClientMessages]
    DOTA_CM_GlyphAlert: _ClassVar[EDotaClientMessages]
    DOTA_CM_TeamShowcaseClientData: _ClassVar[EDotaClientMessages]
    DOTA_CM_PlayTeamShowcase: _ClassVar[EDotaClientMessages]
    DOTA_CM_EventCNY2015Cmd: _ClassVar[EDotaClientMessages]
    DOTA_CM_FillEmptySlotsWithBots: _ClassVar[EDotaClientMessages]
    DOTA_CM_DemoHero: _ClassVar[EDotaClientMessages]
    DOTA_CM_AbilityLearnModeToggled: _ClassVar[EDotaClientMessages]
    DOTA_CM_AbilityStartUse: _ClassVar[EDotaClientMessages]
    DOTA_CM_ChallengeSelect: _ClassVar[EDotaClientMessages]
    DOTA_CM_ChallengeReroll: _ClassVar[EDotaClientMessages]
    DOTA_CM_ClickedBuff: _ClassVar[EDotaClientMessages]
    DOTA_CM_CoinWager: _ClassVar[EDotaClientMessages]
    DOTA_CM_ExecuteOrders: _ClassVar[EDotaClientMessages]
    DOTA_CM_XPAlert: _ClassVar[EDotaClientMessages]
    DOTA_CM_EventPointsTip: _ClassVar[EDotaClientMessages]
    DOTA_CM_KillMyHero: _ClassVar[EDotaClientMessages]
    DOTA_CM_QuestStatus: _ClassVar[EDotaClientMessages]
    DOTA_CM_ToggleAutoattack: _ClassVar[EDotaClientMessages]
    DOTA_CM_SpecialAbility: _ClassVar[EDotaClientMessages]
    DOTA_CM_KillcamDamageTaken: _ClassVar[EDotaClientMessages]
    DOTA_CM_SetEnemyStartingPosition: _ClassVar[EDotaClientMessages]
    DOTA_CM_SetDesiredWardPlacement: _ClassVar[EDotaClientMessages]
    DOTA_CM_RollDice: _ClassVar[EDotaClientMessages]
    DOTA_CM_FlipCoin: _ClassVar[EDotaClientMessages]
    DOTA_CM_RequestItemSuggestions: _ClassVar[EDotaClientMessages]
    DOTA_CM_MakeTeamCaptain: _ClassVar[EDotaClientMessages]
    DOTA_CM_CoinWagerToken: _ClassVar[EDotaClientMessages]
    DOTA_CM_RankWager: _ClassVar[EDotaClientMessages]
    DOTA_CM_DismissAllStatPopups: _ClassVar[EDotaClientMessages]
    DOTA_CM_HelpTipSystemStateChanged: _ClassVar[EDotaClientMessages]
    DOTA_CM_ChannelRequiresHalt: _ClassVar[EDotaClientMessages]
    DOTA_CM_RequestBulkCombatLog: _ClassVar[EDotaClientMessages]
    DOTA_CM_AbilityDraftRequestAbility: _ClassVar[EDotaClientMessages]
    DOTA_CM_GuideSelectOption: _ClassVar[EDotaClientMessages]
    DOTA_CM_GuideSelected: _ClassVar[EDotaClientMessages]
    DOTA_CM_DamageReport: _ClassVar[EDotaClientMessages]
    DOTA_CM_SalutePlayer: _ClassVar[EDotaClientMessages]
    DOTA_CM_SprayWheel: _ClassVar[EDotaClientMessages]
    DOTA_CM_TipAlert: _ClassVar[EDotaClientMessages]
    DOTA_CM_EmptyTeleportAlert: _ClassVar[EDotaClientMessages]
    DOTA_CM_RadarAlert: _ClassVar[EDotaClientMessages]
    DOTA_CM_TalentTreeAlert: _ClassVar[EDotaClientMessages]
    DOTA_CM_SetCavernMapVariant: _ClassVar[EDotaClientMessages]
    DOTA_CM_PauseGameOrder: _ClassVar[EDotaClientMessages]
    DOTA_CM_VersusScene_PlayerBehavior: _ClassVar[EDotaClientMessages]
    DOTA_CM_PlayerBounty: _ClassVar[EDotaClientMessages]
    DOTA_CM_PlayerBountyCancel: _ClassVar[EDotaClientMessages]
    DOTA_CM_EmptyItemSlotAlert: _ClassVar[EDotaClientMessages]
    DOTA_CM_AddOverwatchReportMarker: _ClassVar[EDotaClientMessages]
    DOTA_CM_AghsStatusAlert: _ClassVar[EDotaClientMessages]
    DOTA_CM_PerfReport: _ClassVar[EDotaClientMessages]
    DOTA_CM_ContextualTips_Subscribe: _ClassVar[EDotaClientMessages]
    DOTA_CM_ChatMessage: _ClassVar[EDotaClientMessages]
    DOTA_CM_AddCommunicationsReportMarker: _ClassVar[EDotaClientMessages]
    DOTA_CM_AddCommunicationsBlockMarker: _ClassVar[EDotaClientMessages]
    DOTA_CM_NeutralCampAlert: _ClassVar[EDotaClientMessages]
    DOTA_CM_DuelAccepted: _ClassVar[EDotaClientMessages]
    DOTA_CM_ChooseNeutralItem: _ClassVar[EDotaClientMessages]
    DOTA_CM_PlayerDraftPick: _ClassVar[EDotaClientMessages]
    DOTA_CM_PlayerDraftSuggest: _ClassVar[EDotaClientMessages]
    DOTA_CM_PlayerDraftPreferRole: _ClassVar[EDotaClientMessages]
    DOTA_CM_PlayerDraftPreferTeam: _ClassVar[EDotaClientMessages]
    DOTA_CM_ChatWheelAlert: _ClassVar[EDotaClientMessages]
    DOTA_CM_AbilityAlert: _ClassVar[EDotaClientMessages]
    DOTA_CM_AllyAbilityAlert: _ClassVar[EDotaClientMessages]
    DOTA_CM_GiftPlayer: _ClassVar[EDotaClientMessages]
    DOTA_CM_GiftEveryone: _ClassVar[EDotaClientMessages]
    DOTA_CM_SelectOverworldTokenRewards: _ClassVar[EDotaClientMessages]
    DOTA_CM_FacetAlert: _ClassVar[EDotaClientMessages]
    DOTA_CM_InnateAlert: _ClassVar[EDotaClientMessages]
    DOTA_CM_SelectOverworldID: _ClassVar[EDotaClientMessages]
    DOTA_CM_RerollNeutralItem: _ClassVar[EDotaClientMessages]
    DOTA_CM_RoshanTimer: _ClassVar[EDotaClientMessages]
    DOTA_CM_SuggestItemPreference: _ClassVar[EDotaClientMessages]
    DOTA_CM_CraftNeutralItem: _ClassVar[EDotaClientMessages]
    DOTA_CM_ChooseCraftedNeutral: _ClassVar[EDotaClientMessages]
    DOTA_CM_TimerAlert: _ClassVar[EDotaClientMessages]
    DOTA_CM_MadstoneAlert: _ClassVar[EDotaClientMessages]
    DOTA_CM_UpdateAutoCourierSettings: _ClassVar[EDotaClientMessages]
    DOTA_CM_AutoCourierExecute: _ClassVar[EDotaClientMessages]
    DOTA_CM_QuickBuyAction: _ClassVar[EDotaClientMessages]
    DOTA_CM_InteractionChannelsRequireHalt: _ClassVar[EDotaClientMessages]
    DOTA_CM_SuggestItemRefresh: _ClassVar[EDotaClientMessages]
    DOTA_CM_SuggestItemVariantRequest: _ClassVar[EDotaClientMessages]
    DOTA_CM_SuggestItemVariantSelect: _ClassVar[EDotaClientMessages]
    DOTA_CM_MonsterHunter_SelectInvestigation: _ClassVar[EDotaClientMessages]
    DOTA_CM_MonsterHunter_HuntAlert: _ClassVar[EDotaClientMessages]
    DOTA_CM_AbilitySpecificChannelRequiresHalt: _ClassVar[EDotaClientMessages]
    DOTA_CM_TormentorTimer: _ClassVar[EDotaClientMessages]

DOTA_CM_MapLine: EDotaClientMessages
DOTA_CM_AspectRatio: EDotaClientMessages
DOTA_CM_MapPing: EDotaClientMessages
DOTA_CM_UnitsAutoAttack: EDotaClientMessages
DOTA_CM_SearchString: EDotaClientMessages
DOTA_CM_Pause: EDotaClientMessages
DOTA_CM_ShopViewMode: EDotaClientMessages
DOTA_CM_SetUnitShareFlag: EDotaClientMessages
DOTA_CM_SwapRequest: EDotaClientMessages
DOTA_CM_SwapAccept: EDotaClientMessages
DOTA_CM_WorldLine: EDotaClientMessages
DOTA_CM_RequestGraphUpdate: EDotaClientMessages
DOTA_CM_ItemAlert: EDotaClientMessages
DOTA_CM_ChatWheel: EDotaClientMessages
DOTA_CM_SendStatPopup: EDotaClientMessages
DOTA_CM_BeginLastHitChallenge: EDotaClientMessages
DOTA_CM_UpdateQuickBuy: EDotaClientMessages
DOTA_CM_UpdateCoachListen: EDotaClientMessages
DOTA_CM_CoachHUDPing: EDotaClientMessages
DOTA_CM_RecordVote: EDotaClientMessages
DOTA_CM_UnitsAutoAttackAfterSpell: EDotaClientMessages
DOTA_CM_WillPurchaseAlert: EDotaClientMessages
DOTA_CM_PlayerShowCase: EDotaClientMessages
DOTA_CM_TeleportRequiresHalt: EDotaClientMessages
DOTA_CM_CameraZoomAmount: EDotaClientMessages
DOTA_CM_BroadcasterUsingCamerman: EDotaClientMessages
DOTA_CM_BroadcasterUsingAssistedCameraOperator: EDotaClientMessages
DOTA_CM_EnemyItemAlert: EDotaClientMessages
DOTA_CM_FreeInventory: EDotaClientMessages
DOTA_CM_BuyBackStateAlert: EDotaClientMessages
DOTA_CM_QuickBuyAlert: EDotaClientMessages
DOTA_CM_HeroStatueLike: EDotaClientMessages
DOTA_CM_ModifierAlert: EDotaClientMessages
DOTA_CM_TeamShowcaseEditor: EDotaClientMessages
DOTA_CM_HPManaAlert: EDotaClientMessages
DOTA_CM_GlyphAlert: EDotaClientMessages
DOTA_CM_TeamShowcaseClientData: EDotaClientMessages
DOTA_CM_PlayTeamShowcase: EDotaClientMessages
DOTA_CM_EventCNY2015Cmd: EDotaClientMessages
DOTA_CM_FillEmptySlotsWithBots: EDotaClientMessages
DOTA_CM_DemoHero: EDotaClientMessages
DOTA_CM_AbilityLearnModeToggled: EDotaClientMessages
DOTA_CM_AbilityStartUse: EDotaClientMessages
DOTA_CM_ChallengeSelect: EDotaClientMessages
DOTA_CM_ChallengeReroll: EDotaClientMessages
DOTA_CM_ClickedBuff: EDotaClientMessages
DOTA_CM_CoinWager: EDotaClientMessages
DOTA_CM_ExecuteOrders: EDotaClientMessages
DOTA_CM_XPAlert: EDotaClientMessages
DOTA_CM_EventPointsTip: EDotaClientMessages
DOTA_CM_KillMyHero: EDotaClientMessages
DOTA_CM_QuestStatus: EDotaClientMessages
DOTA_CM_ToggleAutoattack: EDotaClientMessages
DOTA_CM_SpecialAbility: EDotaClientMessages
DOTA_CM_KillcamDamageTaken: EDotaClientMessages
DOTA_CM_SetEnemyStartingPosition: EDotaClientMessages
DOTA_CM_SetDesiredWardPlacement: EDotaClientMessages
DOTA_CM_RollDice: EDotaClientMessages
DOTA_CM_FlipCoin: EDotaClientMessages
DOTA_CM_RequestItemSuggestions: EDotaClientMessages
DOTA_CM_MakeTeamCaptain: EDotaClientMessages
DOTA_CM_CoinWagerToken: EDotaClientMessages
DOTA_CM_RankWager: EDotaClientMessages
DOTA_CM_DismissAllStatPopups: EDotaClientMessages
DOTA_CM_HelpTipSystemStateChanged: EDotaClientMessages
DOTA_CM_ChannelRequiresHalt: EDotaClientMessages
DOTA_CM_RequestBulkCombatLog: EDotaClientMessages
DOTA_CM_AbilityDraftRequestAbility: EDotaClientMessages
DOTA_CM_GuideSelectOption: EDotaClientMessages
DOTA_CM_GuideSelected: EDotaClientMessages
DOTA_CM_DamageReport: EDotaClientMessages
DOTA_CM_SalutePlayer: EDotaClientMessages
DOTA_CM_SprayWheel: EDotaClientMessages
DOTA_CM_TipAlert: EDotaClientMessages
DOTA_CM_EmptyTeleportAlert: EDotaClientMessages
DOTA_CM_RadarAlert: EDotaClientMessages
DOTA_CM_TalentTreeAlert: EDotaClientMessages
DOTA_CM_SetCavernMapVariant: EDotaClientMessages
DOTA_CM_PauseGameOrder: EDotaClientMessages
DOTA_CM_VersusScene_PlayerBehavior: EDotaClientMessages
DOTA_CM_PlayerBounty: EDotaClientMessages
DOTA_CM_PlayerBountyCancel: EDotaClientMessages
DOTA_CM_EmptyItemSlotAlert: EDotaClientMessages
DOTA_CM_AddOverwatchReportMarker: EDotaClientMessages
DOTA_CM_AghsStatusAlert: EDotaClientMessages
DOTA_CM_PerfReport: EDotaClientMessages
DOTA_CM_ContextualTips_Subscribe: EDotaClientMessages
DOTA_CM_ChatMessage: EDotaClientMessages
DOTA_CM_AddCommunicationsReportMarker: EDotaClientMessages
DOTA_CM_AddCommunicationsBlockMarker: EDotaClientMessages
DOTA_CM_NeutralCampAlert: EDotaClientMessages
DOTA_CM_DuelAccepted: EDotaClientMessages
DOTA_CM_ChooseNeutralItem: EDotaClientMessages
DOTA_CM_PlayerDraftPick: EDotaClientMessages
DOTA_CM_PlayerDraftSuggest: EDotaClientMessages
DOTA_CM_PlayerDraftPreferRole: EDotaClientMessages
DOTA_CM_PlayerDraftPreferTeam: EDotaClientMessages
DOTA_CM_ChatWheelAlert: EDotaClientMessages
DOTA_CM_AbilityAlert: EDotaClientMessages
DOTA_CM_AllyAbilityAlert: EDotaClientMessages
DOTA_CM_GiftPlayer: EDotaClientMessages
DOTA_CM_GiftEveryone: EDotaClientMessages
DOTA_CM_SelectOverworldTokenRewards: EDotaClientMessages
DOTA_CM_FacetAlert: EDotaClientMessages
DOTA_CM_InnateAlert: EDotaClientMessages
DOTA_CM_SelectOverworldID: EDotaClientMessages
DOTA_CM_RerollNeutralItem: EDotaClientMessages
DOTA_CM_RoshanTimer: EDotaClientMessages
DOTA_CM_SuggestItemPreference: EDotaClientMessages
DOTA_CM_CraftNeutralItem: EDotaClientMessages
DOTA_CM_ChooseCraftedNeutral: EDotaClientMessages
DOTA_CM_TimerAlert: EDotaClientMessages
DOTA_CM_MadstoneAlert: EDotaClientMessages
DOTA_CM_UpdateAutoCourierSettings: EDotaClientMessages
DOTA_CM_AutoCourierExecute: EDotaClientMessages
DOTA_CM_QuickBuyAction: EDotaClientMessages
DOTA_CM_InteractionChannelsRequireHalt: EDotaClientMessages
DOTA_CM_SuggestItemRefresh: EDotaClientMessages
DOTA_CM_SuggestItemVariantRequest: EDotaClientMessages
DOTA_CM_SuggestItemVariantSelect: EDotaClientMessages
DOTA_CM_MonsterHunter_SelectInvestigation: EDotaClientMessages
DOTA_CM_MonsterHunter_HuntAlert: EDotaClientMessages
DOTA_CM_AbilitySpecificChannelRequiresHalt: EDotaClientMessages
DOTA_CM_TormentorTimer: EDotaClientMessages

class CDOTAClientMsg_MapPing(_message.Message):
    __slots__ = ("location_ping",)
    LOCATION_PING_FIELD_NUMBER: _ClassVar[int]
    location_ping: _dota_commonmessages_pb2.CDOTAMsg_LocationPing
    def __init__(
        self, location_ping: _dota_commonmessages_pb2.CDOTAMsg_LocationPing | _Mapping | None = ...
    ) -> None: ...

class CDOTAClientMsg_ItemAlert(_message.Message):
    __slots__ = ("item_alert",)
    ITEM_ALERT_FIELD_NUMBER: _ClassVar[int]
    item_alert: _dota_commonmessages_pb2.CDOTAMsg_ItemAlert
    def __init__(
        self, item_alert: _dota_commonmessages_pb2.CDOTAMsg_ItemAlert | _Mapping | None = ...
    ) -> None: ...

class CDOTAClientMsg_EnemyItemAlert(_message.Message):
    __slots__ = (
        "item_entindex",
        "rune_type",
        "item_level",
        "primary_charges",
        "secondary_charges",
        "ability_id",
        "owner_entindex",
    )
    ITEM_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    RUNE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ITEM_LEVEL_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_CHARGES_FIELD_NUMBER: _ClassVar[int]
    SECONDARY_CHARGES_FIELD_NUMBER: _ClassVar[int]
    ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    item_entindex: int
    rune_type: int
    item_level: int
    primary_charges: int
    secondary_charges: int
    ability_id: int
    owner_entindex: int
    def __init__(
        self,
        item_entindex: int | None = ...,
        rune_type: int | None = ...,
        item_level: int | None = ...,
        primary_charges: int | None = ...,
        secondary_charges: int | None = ...,
        ability_id: int | None = ...,
        owner_entindex: int | None = ...,
    ) -> None: ...

class CDOTAClientMsg_ModifierAlert(_message.Message):
    __slots__ = ("buff_internal_index", "target_entindex")
    BUFF_INTERNAL_INDEX_FIELD_NUMBER: _ClassVar[int]
    TARGET_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    buff_internal_index: int
    target_entindex: int
    def __init__(
        self, buff_internal_index: int | None = ..., target_entindex: int | None = ...
    ) -> None: ...

class CDOTAClientMsg_ClickedBuff(_message.Message):
    __slots__ = ("buff_internal_index", "target_entindex")
    BUFF_INTERNAL_INDEX_FIELD_NUMBER: _ClassVar[int]
    TARGET_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    buff_internal_index: int
    target_entindex: int
    def __init__(
        self, buff_internal_index: int | None = ..., target_entindex: int | None = ...
    ) -> None: ...

class CDOTAClientMsg_HPManaAlert(_message.Message):
    __slots__ = ("target_entindex", "show_raw_values")
    TARGET_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    SHOW_RAW_VALUES_FIELD_NUMBER: _ClassVar[int]
    target_entindex: int
    show_raw_values: bool
    def __init__(self, target_entindex: int | None = ..., show_raw_values: bool = ...) -> None: ...

class CDOTAClientMsg_NeutralCampAlert(_message.Message):
    __slots__ = ("spawner_entindex", "unit_entindex", "stack_request")
    SPAWNER_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    UNIT_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    STACK_REQUEST_FIELD_NUMBER: _ClassVar[int]
    spawner_entindex: int
    unit_entindex: int
    stack_request: bool
    def __init__(
        self,
        spawner_entindex: int | None = ...,
        unit_entindex: int | None = ...,
        stack_request: bool = ...,
    ) -> None: ...

class CDOTAClientMsg_GlyphAlert(_message.Message):
    __slots__ = ("negative",)
    NEGATIVE_FIELD_NUMBER: _ClassVar[int]
    negative: bool
    def __init__(self, negative: bool = ...) -> None: ...

class CDOTAClientMsg_RadarAlert(_message.Message):
    __slots__ = ("negative",)
    NEGATIVE_FIELD_NUMBER: _ClassVar[int]
    negative: bool
    def __init__(self, negative: bool = ...) -> None: ...

class CDOTAClientMsg_MapLine(_message.Message):
    __slots__ = ("mapline",)
    MAPLINE_FIELD_NUMBER: _ClassVar[int]
    mapline: _dota_commonmessages_pb2.CDOTAMsg_MapLine
    def __init__(
        self, mapline: _dota_commonmessages_pb2.CDOTAMsg_MapLine | _Mapping | None = ...
    ) -> None: ...

class CDOTAClientMsg_AspectRatio(_message.Message):
    __slots__ = ("ratio",)
    RATIO_FIELD_NUMBER: _ClassVar[int]
    ratio: float
    def __init__(self, ratio: float | None = ...) -> None: ...

class CDOTAClientMsg_UnitsAutoAttackMode(_message.Message):
    __slots__ = ("mode", "unit_type")
    class EMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INVALID: _ClassVar[CDOTAClientMsg_UnitsAutoAttackMode.EMode]
        NEVER: _ClassVar[CDOTAClientMsg_UnitsAutoAttackMode.EMode]
        AFTER_SPELLCAST: _ClassVar[CDOTAClientMsg_UnitsAutoAttackMode.EMode]
        ALWAYS: _ClassVar[CDOTAClientMsg_UnitsAutoAttackMode.EMode]

    INVALID: CDOTAClientMsg_UnitsAutoAttackMode.EMode
    NEVER: CDOTAClientMsg_UnitsAutoAttackMode.EMode
    AFTER_SPELLCAST: CDOTAClientMsg_UnitsAutoAttackMode.EMode
    ALWAYS: CDOTAClientMsg_UnitsAutoAttackMode.EMode
    class EUnitType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NORMAL: _ClassVar[CDOTAClientMsg_UnitsAutoAttackMode.EUnitType]
        SUMMONED: _ClassVar[CDOTAClientMsg_UnitsAutoAttackMode.EUnitType]

    NORMAL: CDOTAClientMsg_UnitsAutoAttackMode.EUnitType
    SUMMONED: CDOTAClientMsg_UnitsAutoAttackMode.EUnitType
    MODE_FIELD_NUMBER: _ClassVar[int]
    UNIT_TYPE_FIELD_NUMBER: _ClassVar[int]
    mode: CDOTAClientMsg_UnitsAutoAttackMode.EMode
    unit_type: CDOTAClientMsg_UnitsAutoAttackMode.EUnitType
    def __init__(
        self,
        mode: CDOTAClientMsg_UnitsAutoAttackMode.EMode | str | None = ...,
        unit_type: CDOTAClientMsg_UnitsAutoAttackMode.EUnitType | str | None = ...,
    ) -> None: ...

class CDOTAClientMsg_UnitsAutoAttackAfterSpell(_message.Message):
    __slots__ = ("enabled",)
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    def __init__(self, enabled: bool = ...) -> None: ...

class CDOTAClientMsg_TeleportRequiresHalt(_message.Message):
    __slots__ = ("enabled",)
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    def __init__(self, enabled: bool = ...) -> None: ...

class CDOTAClientMsg_ChannelRequiresHalt(_message.Message):
    __slots__ = ("enabled",)
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    def __init__(self, enabled: bool = ...) -> None: ...

class CDOTAClientMsg_InteractionChannelsRequireHalt(_message.Message):
    __slots__ = ("enabled",)
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    def __init__(self, enabled: bool = ...) -> None: ...

class CDOTAClientMsg_AbilitySpecificChannelRequiresHalt(_message.Message):
    __slots__ = ("ability_id", "default", "enabled")
    ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    ability_id: int
    default: bool
    enabled: bool
    def __init__(
        self, ability_id: int | None = ..., default: bool = ..., enabled: bool = ...
    ) -> None: ...

class CDOTAClientMsg_SearchString(_message.Message):
    __slots__ = ("search",)
    SEARCH_FIELD_NUMBER: _ClassVar[int]
    search: str
    def __init__(self, search: str | None = ...) -> None: ...

class CDOTAClientMsg_Pause(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CDOTAClientMsg_ShopViewMode(_message.Message):
    __slots__ = ("mode",)
    MODE_FIELD_NUMBER: _ClassVar[int]
    mode: int
    def __init__(self, mode: int | None = ...) -> None: ...

class CDOTAClientMsg_SetUnitShareFlag(_message.Message):
    __slots__ = ("player_id", "flag", "state")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    FLAG_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    flag: int
    state: bool
    def __init__(
        self, player_id: int | None = ..., flag: int | None = ..., state: bool = ...
    ) -> None: ...

class CDOTAClientMsg_SwapRequest(_message.Message):
    __slots__ = ("player_id",)
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    def __init__(self, player_id: int | None = ...) -> None: ...

class CDOTAClientMsg_SwapAccept(_message.Message):
    __slots__ = ("player_id",)
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    def __init__(self, player_id: int | None = ...) -> None: ...

class CDOTAClientMsg_WorldLine(_message.Message):
    __slots__ = ("worldline",)
    WORLDLINE_FIELD_NUMBER: _ClassVar[int]
    worldline: _dota_commonmessages_pb2.CDOTAMsg_WorldLine
    def __init__(
        self, worldline: _dota_commonmessages_pb2.CDOTAMsg_WorldLine | _Mapping | None = ...
    ) -> None: ...

class CDOTAClientMsg_RequestGraphUpdate(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CDOTAClientMsg_ChatWheel(_message.Message):
    __slots__ = ("chat_message_id", "param_hero_id", "emoticon_id")
    CHAT_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    PARAM_HERO_ID_FIELD_NUMBER: _ClassVar[int]
    EMOTICON_ID_FIELD_NUMBER: _ClassVar[int]
    chat_message_id: int
    param_hero_id: int
    emoticon_id: int
    def __init__(
        self,
        chat_message_id: int | None = ...,
        param_hero_id: int | None = ...,
        emoticon_id: int | None = ...,
    ) -> None: ...

class CDOTAClientMsg_SendStatPopup(_message.Message):
    __slots__ = ("statpopup",)
    STATPOPUP_FIELD_NUMBER: _ClassVar[int]
    statpopup: _dota_commonmessages_pb2.CDOTAMsg_SendStatPopup
    def __init__(
        self, statpopup: _dota_commonmessages_pb2.CDOTAMsg_SendStatPopup | _Mapping | None = ...
    ) -> None: ...

class CDOTAClientMsg_DismissAllStatPopups(_message.Message):
    __slots__ = ("dismissallmsg",)
    DISMISSALLMSG_FIELD_NUMBER: _ClassVar[int]
    dismissallmsg: _dota_commonmessages_pb2.CDOTAMsg_DismissAllStatPopups
    def __init__(
        self,
        dismissallmsg: _dota_commonmessages_pb2.CDOTAMsg_DismissAllStatPopups
        | _Mapping
        | None = ...,
    ) -> None: ...

class CDOTAClientMsg_BeginLastHitChallenge(_message.Message):
    __slots__ = ("chosen_lane", "helper_enabled")
    CHOSEN_LANE_FIELD_NUMBER: _ClassVar[int]
    HELPER_ENABLED_FIELD_NUMBER: _ClassVar[int]
    chosen_lane: int
    helper_enabled: bool
    def __init__(self, chosen_lane: int | None = ..., helper_enabled: bool = ...) -> None: ...

class CDOTAClientMsg_UpdateQuickBuyItem(_message.Message):
    __slots__ = ("item_ability_id", "purchasable", "top_level_item_ability_id")
    ITEM_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    PURCHASABLE_FIELD_NUMBER: _ClassVar[int]
    TOP_LEVEL_ITEM_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    item_ability_id: int
    purchasable: bool
    top_level_item_ability_id: int
    def __init__(
        self,
        item_ability_id: int | None = ...,
        purchasable: bool = ...,
        top_level_item_ability_id: int | None = ...,
    ) -> None: ...

class CDOTAClientMsg_UpdateQuickBuy(_message.Message):
    __slots__ = ("items", "goal_item_ability_ids")
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    GOAL_ITEM_ABILITY_IDS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[CDOTAClientMsg_UpdateQuickBuyItem]
    goal_item_ability_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        items: _Iterable[CDOTAClientMsg_UpdateQuickBuyItem | _Mapping] | None = ...,
        goal_item_ability_ids: _Iterable[int] | None = ...,
    ) -> None: ...

class CDOTAClientMsg_QuickBuyAction(_message.Message):
    __slots__ = (
        "action",
        "item_ability_id",
        "slot_index",
        "purchaser_entindex",
        "new_slot_index",
        "top_level_item",
        "old_slot_ability_ids",
    )
    class EActionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INVALID: _ClassVar[CDOTAClientMsg_QuickBuyAction.EActionType]
        PURCHASE: _ClassVar[CDOTAClientMsg_QuickBuyAction.EActionType]
        QUEUE: _ClassVar[CDOTAClientMsg_QuickBuyAction.EActionType]
        REMOVE: _ClassVar[CDOTAClientMsg_QuickBuyAction.EActionType]
        CLEAR: _ClassVar[CDOTAClientMsg_QuickBuyAction.EActionType]
        CLEAR_AND_QUEUE: _ClassVar[CDOTAClientMsg_QuickBuyAction.EActionType]
        MARK_FOR_BUY: _ClassVar[CDOTAClientMsg_QuickBuyAction.EActionType]
        CLEAR_MARK_FOR_BUY: _ClassVar[CDOTAClientMsg_QuickBuyAction.EActionType]
        ENABLE_BUYBACK_PROTECTION: _ClassVar[CDOTAClientMsg_QuickBuyAction.EActionType]
        DISABLE_BUYBACK_PROTECTION: _ClassVar[CDOTAClientMsg_QuickBuyAction.EActionType]
        QUEUE_FIRST_AND_MARK_FOR_BUY: _ClassVar[CDOTAClientMsg_QuickBuyAction.EActionType]
        CHANGE_SLOT: _ClassVar[CDOTAClientMsg_QuickBuyAction.EActionType]

    INVALID: CDOTAClientMsg_QuickBuyAction.EActionType
    PURCHASE: CDOTAClientMsg_QuickBuyAction.EActionType
    QUEUE: CDOTAClientMsg_QuickBuyAction.EActionType
    REMOVE: CDOTAClientMsg_QuickBuyAction.EActionType
    CLEAR: CDOTAClientMsg_QuickBuyAction.EActionType
    CLEAR_AND_QUEUE: CDOTAClientMsg_QuickBuyAction.EActionType
    MARK_FOR_BUY: CDOTAClientMsg_QuickBuyAction.EActionType
    CLEAR_MARK_FOR_BUY: CDOTAClientMsg_QuickBuyAction.EActionType
    ENABLE_BUYBACK_PROTECTION: CDOTAClientMsg_QuickBuyAction.EActionType
    DISABLE_BUYBACK_PROTECTION: CDOTAClientMsg_QuickBuyAction.EActionType
    QUEUE_FIRST_AND_MARK_FOR_BUY: CDOTAClientMsg_QuickBuyAction.EActionType
    CHANGE_SLOT: CDOTAClientMsg_QuickBuyAction.EActionType
    ACTION_FIELD_NUMBER: _ClassVar[int]
    ITEM_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    SLOT_INDEX_FIELD_NUMBER: _ClassVar[int]
    PURCHASER_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    NEW_SLOT_INDEX_FIELD_NUMBER: _ClassVar[int]
    TOP_LEVEL_ITEM_FIELD_NUMBER: _ClassVar[int]
    OLD_SLOT_ABILITY_IDS_FIELD_NUMBER: _ClassVar[int]
    action: CDOTAClientMsg_QuickBuyAction.EActionType
    item_ability_id: int
    slot_index: int
    purchaser_entindex: int
    new_slot_index: int
    top_level_item: bool
    old_slot_ability_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        action: CDOTAClientMsg_QuickBuyAction.EActionType | str | None = ...,
        item_ability_id: int | None = ...,
        slot_index: int | None = ...,
        purchaser_entindex: int | None = ...,
        new_slot_index: int | None = ...,
        top_level_item: bool = ...,
        old_slot_ability_ids: _Iterable[int] | None = ...,
    ) -> None: ...

class CDOTAClientMsg_RecordVote(_message.Message):
    __slots__ = ("choice_index",)
    CHOICE_INDEX_FIELD_NUMBER: _ClassVar[int]
    choice_index: int
    def __init__(self, choice_index: int | None = ...) -> None: ...

class CDOTAClientMsg_WillPurchaseAlert(_message.Message):
    __slots__ = ("item_ability_id", "gold_remaining", "suggestion_player_id")
    ITEM_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    GOLD_REMAINING_FIELD_NUMBER: _ClassVar[int]
    SUGGESTION_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    item_ability_id: int
    gold_remaining: int
    suggestion_player_id: int
    def __init__(
        self,
        item_ability_id: int | None = ...,
        gold_remaining: int | None = ...,
        suggestion_player_id: int | None = ...,
    ) -> None: ...

class CDOTAClientMsg_BuyBackStateAlert(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CDOTAClientMsg_QuickBuyAlert(_message.Message):
    __slots__ = ("item_ability_id", "gold_cost", "item_cooldown_seconds", "show_buyback")
    ITEM_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    GOLD_COST_FIELD_NUMBER: _ClassVar[int]
    ITEM_COOLDOWN_SECONDS_FIELD_NUMBER: _ClassVar[int]
    SHOW_BUYBACK_FIELD_NUMBER: _ClassVar[int]
    item_ability_id: int
    gold_cost: int
    item_cooldown_seconds: int
    show_buyback: bool
    def __init__(
        self,
        item_ability_id: int | None = ...,
        gold_cost: int | None = ...,
        item_cooldown_seconds: int | None = ...,
        show_buyback: bool = ...,
    ) -> None: ...

class CDOTAClientMsg_PlayerShowCase(_message.Message):
    __slots__ = ("showcase",)
    SHOWCASE_FIELD_NUMBER: _ClassVar[int]
    showcase: bool
    def __init__(self, showcase: bool = ...) -> None: ...

class CDOTAClientMsg_CameraZoomAmount(_message.Message):
    __slots__ = ("zoom_amount",)
    ZOOM_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    zoom_amount: float
    def __init__(self, zoom_amount: float | None = ...) -> None: ...

class CDOTAClientMsg_BroadcasterUsingCameraman(_message.Message):
    __slots__ = ("cameraman",)
    CAMERAMAN_FIELD_NUMBER: _ClassVar[int]
    cameraman: bool
    def __init__(self, cameraman: bool = ...) -> None: ...

class CDOTAClientMsg_BroadcasterUsingAssistedCameraOperator(_message.Message):
    __slots__ = ("enabled",)
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    def __init__(self, enabled: bool = ...) -> None: ...

class CDOTAClientMsg_FillEmptySlotsWithBots(_message.Message):
    __slots__ = ("fillwithbots",)
    FILLWITHBOTS_FIELD_NUMBER: _ClassVar[int]
    fillwithbots: bool
    def __init__(self, fillwithbots: bool = ...) -> None: ...

class CDOTAClientMsg_HeroStatueLike(_message.Message):
    __slots__ = ("owner_player_id",)
    OWNER_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    owner_player_id: int
    def __init__(self, owner_player_id: int | None = ...) -> None: ...

class CDOTAClientMsg_EventCNY2015Cmd(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: bytes | None = ...) -> None: ...

class CDOTAClientMsg_DemoHero(_message.Message):
    __slots__ = (
        "hero_id",
        "hero_id_to_spawn",
        "preview_items",
        "item_ids",
        "style_index_override",
        "keep_existing_demohero",
        "item_data",
        "hero_variant",
    )
    class PreviewItem(_message.Message):
        __slots__ = ("item_def", "item_style")
        ITEM_DEF_FIELD_NUMBER: _ClassVar[int]
        ITEM_STYLE_FIELD_NUMBER: _ClassVar[int]
        item_def: int
        item_style: int
        def __init__(self, item_def: int | None = ..., item_style: int | None = ...) -> None: ...

    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_TO_SPAWN_FIELD_NUMBER: _ClassVar[int]
    PREVIEW_ITEMS_FIELD_NUMBER: _ClassVar[int]
    ITEM_IDS_FIELD_NUMBER: _ClassVar[int]
    STYLE_INDEX_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    KEEP_EXISTING_DEMOHERO_FIELD_NUMBER: _ClassVar[int]
    ITEM_DATA_FIELD_NUMBER: _ClassVar[int]
    HERO_VARIANT_FIELD_NUMBER: _ClassVar[int]
    hero_id: int
    hero_id_to_spawn: int
    preview_items: _containers.RepeatedCompositeFieldContainer[CDOTAClientMsg_DemoHero.PreviewItem]
    item_ids: _containers.RepeatedScalarFieldContainer[int]
    style_index_override: int
    keep_existing_demohero: bool
    item_data: _containers.RepeatedCompositeFieldContainer[_base_gcmessages_pb2.CSOEconItem]
    hero_variant: int
    def __init__(
        self,
        hero_id: int | None = ...,
        hero_id_to_spawn: int | None = ...,
        preview_items: _Iterable[CDOTAClientMsg_DemoHero.PreviewItem | _Mapping] | None = ...,
        item_ids: _Iterable[int] | None = ...,
        style_index_override: int | None = ...,
        keep_existing_demohero: bool = ...,
        item_data: _Iterable[_base_gcmessages_pb2.CSOEconItem | _Mapping] | None = ...,
        hero_variant: int | None = ...,
    ) -> None: ...

class CDOTAClientMsg_ChallengeSelect(_message.Message):
    __slots__ = ("event_id", "slot_id", "sequence_id")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    SLOT_ID_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: int
    slot_id: int
    sequence_id: int
    def __init__(
        self, event_id: int | None = ..., slot_id: int | None = ..., sequence_id: int | None = ...
    ) -> None: ...

class CDOTAClientMsg_ChallengeReroll(_message.Message):
    __slots__ = ("event_id", "slot_id", "sequence_id", "hero_id")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    SLOT_ID_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_ID_FIELD_NUMBER: _ClassVar[int]
    HERO_ID_FIELD_NUMBER: _ClassVar[int]
    event_id: _dota_shared_enums_pb2.EEvent
    slot_id: int
    sequence_id: int
    hero_id: int
    def __init__(
        self,
        event_id: _dota_shared_enums_pb2.EEvent | str | None = ...,
        slot_id: int | None = ...,
        sequence_id: int | None = ...,
        hero_id: int | None = ...,
    ) -> None: ...

class CDOTAClientMsg_CoinWager(_message.Message):
    __slots__ = ("wager_amount",)
    WAGER_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    wager_amount: int
    def __init__(self, wager_amount: int | None = ...) -> None: ...

class CDOTAClientMsg_CoinWagerToken(_message.Message):
    __slots__ = ("wager_token_item_id",)
    WAGER_TOKEN_ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    wager_token_item_id: int
    def __init__(self, wager_token_item_id: int | None = ...) -> None: ...

class CDOTAClientMsg_RankWager(_message.Message):
    __slots__ = ("announce_wager",)
    ANNOUNCE_WAGER_FIELD_NUMBER: _ClassVar[int]
    announce_wager: bool
    def __init__(self, announce_wager: bool = ...) -> None: ...

class CDOTAClientMsg_PlayerBounty(_message.Message):
    __slots__ = ("player_id",)
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    def __init__(self, player_id: int | None = ...) -> None: ...

class CDOTAClientMsg_EventPointsTip(_message.Message):
    __slots__ = ("recipient_player_id",)
    RECIPIENT_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    recipient_player_id: int
    def __init__(self, recipient_player_id: int | None = ...) -> None: ...

class CDOTAClientMsg_ExecuteOrders(_message.Message):
    __slots__ = ("orders", "last_order_latency")
    ORDERS_FIELD_NUMBER: _ClassVar[int]
    LAST_ORDER_LATENCY_FIELD_NUMBER: _ClassVar[int]
    orders: _containers.RepeatedCompositeFieldContainer[_dota_commonmessages_pb2.CDOTAMsg_UnitOrder]
    last_order_latency: int
    def __init__(
        self,
        orders: _Iterable[_dota_commonmessages_pb2.CDOTAMsg_UnitOrder | _Mapping] | None = ...,
        last_order_latency: int | None = ...,
    ) -> None: ...

class CDOTAClientMsg_XPAlert(_message.Message):
    __slots__ = ("target_entindex", "damage_taken")
    TARGET_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    DAMAGE_TAKEN_FIELD_NUMBER: _ClassVar[int]
    target_entindex: int
    damage_taken: int
    def __init__(
        self, target_entindex: int | None = ..., damage_taken: int | None = ...
    ) -> None: ...

class CDOTAClientMsg_TalentTreeAlert(_message.Message):
    __slots__ = ("target_entindex", "ability_id", "slot", "learned")
    TARGET_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    SLOT_FIELD_NUMBER: _ClassVar[int]
    LEARNED_FIELD_NUMBER: _ClassVar[int]
    target_entindex: int
    ability_id: int
    slot: int
    learned: bool
    def __init__(
        self,
        target_entindex: int | None = ...,
        ability_id: int | None = ...,
        slot: int | None = ...,
        learned: bool = ...,
    ) -> None: ...

class CDOTAClientMsg_KillcamDamageTaken(_message.Message):
    __slots__ = (
        "target_entindex",
        "damage_taken",
        "item_type",
        "item_ability_id",
        "hero_name",
        "damage_color",
    )
    TARGET_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    DAMAGE_TAKEN_FIELD_NUMBER: _ClassVar[int]
    ITEM_TYPE_FIELD_NUMBER: _ClassVar[int]
    ITEM_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    HERO_NAME_FIELD_NUMBER: _ClassVar[int]
    DAMAGE_COLOR_FIELD_NUMBER: _ClassVar[int]
    target_entindex: int
    damage_taken: int
    item_type: int
    item_ability_id: int
    hero_name: str
    damage_color: str
    def __init__(
        self,
        target_entindex: int | None = ...,
        damage_taken: int | None = ...,
        item_type: int | None = ...,
        item_ability_id: int | None = ...,
        hero_name: str | None = ...,
        damage_color: str | None = ...,
    ) -> None: ...

class CDOTAClientMsg_KillMyHero(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CDOTAClientMsg_QuestStatus(_message.Message):
    __slots__ = (
        "quest_id",
        "challenge_id",
        "progress",
        "goal",
        "query",
        "fail_gametime",
        "item_ability_id",
    )
    QUEST_ID_FIELD_NUMBER: _ClassVar[int]
    CHALLENGE_ID_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    GOAL_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    FAIL_GAMETIME_FIELD_NUMBER: _ClassVar[int]
    ITEM_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    quest_id: int
    challenge_id: int
    progress: int
    goal: int
    query: int
    fail_gametime: float
    item_ability_id: int
    def __init__(
        self,
        quest_id: int | None = ...,
        challenge_id: int | None = ...,
        progress: int | None = ...,
        goal: int | None = ...,
        query: int | None = ...,
        fail_gametime: float | None = ...,
        item_ability_id: int | None = ...,
    ) -> None: ...

class CDOTAClientMsg_ToggleAutoattack(_message.Message):
    __slots__ = ("mode", "show_message")
    MODE_FIELD_NUMBER: _ClassVar[int]
    SHOW_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    mode: int
    show_message: bool
    def __init__(self, mode: int | None = ..., show_message: bool = ...) -> None: ...

class CDOTAClientMsg_SpecialAbility(_message.Message):
    __slots__ = ("ability_index", "target_entindex")
    ABILITY_INDEX_FIELD_NUMBER: _ClassVar[int]
    TARGET_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    ability_index: int
    target_entindex: int
    def __init__(
        self, ability_index: int | None = ..., target_entindex: int | None = ...
    ) -> None: ...

class CDOTAClientMsg_SetEnemyStartingPosition(_message.Message):
    __slots__ = ("enemy_player_id", "enemy_starting_position")
    ENEMY_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    ENEMY_STARTING_POSITION_FIELD_NUMBER: _ClassVar[int]
    enemy_player_id: int
    enemy_starting_position: int
    def __init__(
        self, enemy_player_id: int | None = ..., enemy_starting_position: int | None = ...
    ) -> None: ...

class CDOTAClientMsg_SetDesiredWardPlacement(_message.Message):
    __slots__ = ("ward_index", "ward_x", "ward_y")
    WARD_INDEX_FIELD_NUMBER: _ClassVar[int]
    WARD_X_FIELD_NUMBER: _ClassVar[int]
    WARD_Y_FIELD_NUMBER: _ClassVar[int]
    ward_index: int
    ward_x: float
    ward_y: float
    def __init__(
        self, ward_index: int | None = ..., ward_x: float | None = ..., ward_y: float | None = ...
    ) -> None: ...

class CDOTAClientMsg_RollDice(_message.Message):
    __slots__ = ("channel_type", "roll_min", "roll_max")
    CHANNEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    ROLL_MIN_FIELD_NUMBER: _ClassVar[int]
    ROLL_MAX_FIELD_NUMBER: _ClassVar[int]
    channel_type: int
    roll_min: int
    roll_max: int
    def __init__(
        self, channel_type: int | None = ..., roll_min: int | None = ..., roll_max: int | None = ...
    ) -> None: ...

class CDOTAClientMsg_FlipCoin(_message.Message):
    __slots__ = ("channel_type",)
    CHANNEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    channel_type: int
    def __init__(self, channel_type: int | None = ...) -> None: ...

class CDOTAClientMsg_RequestItemSuggestions(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CDOTAClientMsg_SuggestItemPreference(_message.Message):
    __slots__ = ("item_preferences",)
    class ItemPreference(_message.Message):
        __slots__ = ("item_id", "preference")
        ITEM_ID_FIELD_NUMBER: _ClassVar[int]
        PREFERENCE_FIELD_NUMBER: _ClassVar[int]
        item_id: int
        preference: _dota_shared_enums_pb2.EItemSuggestPreference
        def __init__(
            self,
            item_id: int | None = ...,
            preference: _dota_shared_enums_pb2.EItemSuggestPreference | str | None = ...,
        ) -> None: ...

    ITEM_PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    item_preferences: _containers.RepeatedCompositeFieldContainer[
        CDOTAClientMsg_SuggestItemPreference.ItemPreference
    ]
    def __init__(
        self,
        item_preferences: _Iterable[CDOTAClientMsg_SuggestItemPreference.ItemPreference | _Mapping]
        | None = ...,
    ) -> None: ...

class CDOTAClientMsg_SuggestItemRefresh(_message.Message):
    __slots__ = ("is_out_of_items",)
    IS_OUT_OF_ITEMS_FIELD_NUMBER: _ClassVar[int]
    is_out_of_items: bool
    def __init__(self, is_out_of_items: bool = ...) -> None: ...

class CDOTAClientMsg_SuggestItemGetVariants(_message.Message):
    __slots__ = ("is_out_of_items",)
    IS_OUT_OF_ITEMS_FIELD_NUMBER: _ClassVar[int]
    is_out_of_items: bool
    def __init__(self, is_out_of_items: bool = ...) -> None: ...

class CDOTAClientMsg_SuggestItemSelectVariant(_message.Message):
    __slots__ = ("variant",)
    VARIANT_FIELD_NUMBER: _ClassVar[int]
    variant: int
    def __init__(self, variant: int | None = ...) -> None: ...

class CDOTAClientMsg_MakeTeamCaptain(_message.Message):
    __slots__ = ("player_id",)
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    def __init__(self, player_id: int | None = ...) -> None: ...

class CDOTAClientMsg_HelpTipSystemStateChanged(_message.Message):
    __slots__ = ("tip_displayed",)
    TIP_DISPLAYED_FIELD_NUMBER: _ClassVar[int]
    tip_displayed: bool
    def __init__(self, tip_displayed: bool = ...) -> None: ...

class CDOTAClientMsg_RequestBulkCombatLog(_message.Message):
    __slots__ = ("game_time", "duration", "recent_player_death", "player_id")
    GAME_TIME_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    RECENT_PLAYER_DEATH_FIELD_NUMBER: _ClassVar[int]
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    game_time: float
    duration: float
    recent_player_death: bool
    player_id: int
    def __init__(
        self,
        game_time: float | None = ...,
        duration: float | None = ...,
        recent_player_death: bool = ...,
        player_id: int | None = ...,
    ) -> None: ...

class CDOTAClientMsg_AbilityDraftRequestAbility(_message.Message):
    __slots__ = ("requested_ability_id", "ctrl_is_down", "requested_hero_id", "requested_facet_key")
    REQUESTED_ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    CTRL_IS_DOWN_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_HERO_ID_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_FACET_KEY_FIELD_NUMBER: _ClassVar[int]
    requested_ability_id: int
    ctrl_is_down: bool
    requested_hero_id: int
    requested_facet_key: int
    def __init__(
        self,
        requested_ability_id: int | None = ...,
        ctrl_is_down: bool = ...,
        requested_hero_id: int | None = ...,
        requested_facet_key: int | None = ...,
    ) -> None: ...

class CDOTAClientMsg_GuideSelectOption(_message.Message):
    __slots__ = ("option", "force_recalculate")
    OPTION_FIELD_NUMBER: _ClassVar[int]
    FORCE_RECALCULATE_FIELD_NUMBER: _ClassVar[int]
    option: int
    force_recalculate: bool
    def __init__(self, option: int | None = ..., force_recalculate: bool = ...) -> None: ...

class CDOTAClientMsg_GuideSelected(_message.Message):
    __slots__ = ("guide_workshop_id", "is_plus_guide")
    GUIDE_WORKSHOP_ID_FIELD_NUMBER: _ClassVar[int]
    IS_PLUS_GUIDE_FIELD_NUMBER: _ClassVar[int]
    guide_workshop_id: int
    is_plus_guide: bool
    def __init__(self, guide_workshop_id: int | None = ..., is_plus_guide: bool = ...) -> None: ...

class CDOTAClientMsg_DamageReport(_message.Message):
    __slots__ = ("target_hero_id", "source_hero_id", "damage_amount", "broadcast")
    TARGET_HERO_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_HERO_ID_FIELD_NUMBER: _ClassVar[int]
    DAMAGE_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    BROADCAST_FIELD_NUMBER: _ClassVar[int]
    target_hero_id: int
    source_hero_id: int
    damage_amount: int
    broadcast: bool
    def __init__(
        self,
        target_hero_id: int | None = ...,
        source_hero_id: int | None = ...,
        damage_amount: int | None = ...,
        broadcast: bool = ...,
    ) -> None: ...

class CDOTAClientMsg_SalutePlayer(_message.Message):
    __slots__ = ("target_player_id", "event_id")
    TARGET_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    target_player_id: int
    event_id: int
    def __init__(self, target_player_id: int | None = ..., event_id: int | None = ...) -> None: ...

class CDOTAClientMsg_GiftPlayer(_message.Message):
    __slots__ = ("target_player_id", "item_def_index")
    TARGET_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    ITEM_DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
    target_player_id: int
    item_def_index: int
    def __init__(
        self, target_player_id: int | None = ..., item_def_index: int | None = ...
    ) -> None: ...

class CDOTAClientMsg_GiftEveryone(_message.Message):
    __slots__ = ("item_def_index",)
    ITEM_DEF_INDEX_FIELD_NUMBER: _ClassVar[int]
    item_def_index: int
    def __init__(self, item_def_index: int | None = ...) -> None: ...

class CDOTAClientMsg_TipAlert(_message.Message):
    __slots__ = ("tip_text",)
    TIP_TEXT_FIELD_NUMBER: _ClassVar[int]
    tip_text: str
    def __init__(self, tip_text: str | None = ...) -> None: ...

class CDOTAClientMsg_EmptyTeleportAlert(_message.Message):
    __slots__ = ("target_entindex",)
    TARGET_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    target_entindex: int
    def __init__(self, target_entindex: int | None = ...) -> None: ...

class CDOTAClientMsg_SetCavernMapVariant(_message.Message):
    __slots__ = ("map_variant",)
    MAP_VARIANT_FIELD_NUMBER: _ClassVar[int]
    map_variant: int
    def __init__(self, map_variant: int | None = ...) -> None: ...

class CDOTAClientMsg_PauseGameOrder(_message.Message):
    __slots__ = ("order_id", "data")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    order_id: int
    data: int
    def __init__(self, order_id: int | None = ..., data: int | None = ...) -> None: ...

class CDOTAClientMsg_VersusScene_PlayerBehavior(_message.Message):
    __slots__ = ("behavior", "play_activity", "chat_wheel", "playback_rate")
    BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    PLAY_ACTIVITY_FIELD_NUMBER: _ClassVar[int]
    CHAT_WHEEL_FIELD_NUMBER: _ClassVar[int]
    PLAYBACK_RATE_FIELD_NUMBER: _ClassVar[int]
    behavior: _dota_commonmessages_pb2.EDOTAVersusScenePlayerBehavior
    play_activity: _dota_commonmessages_pb2.VersusScene_PlayActivity
    chat_wheel: _dota_commonmessages_pb2.VersusScene_ChatWheel
    playback_rate: _dota_commonmessages_pb2.VersusScene_PlaybackRate
    def __init__(
        self,
        behavior: _dota_commonmessages_pb2.EDOTAVersusScenePlayerBehavior | str | None = ...,
        play_activity: _dota_commonmessages_pb2.VersusScene_PlayActivity | _Mapping | None = ...,
        chat_wheel: _dota_commonmessages_pb2.VersusScene_ChatWheel | _Mapping | None = ...,
        playback_rate: _dota_commonmessages_pb2.VersusScene_PlaybackRate | _Mapping | None = ...,
    ) -> None: ...

class CDOTAClientMsg_EmptyItemSlotAlert(_message.Message):
    __slots__ = ("target_entindex", "slot_index")
    TARGET_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    SLOT_INDEX_FIELD_NUMBER: _ClassVar[int]
    target_entindex: int
    slot_index: int
    def __init__(self, target_entindex: int | None = ..., slot_index: int | None = ...) -> None: ...

class CDOTAClientMsg_AddOverwatchReportMarker(_message.Message):
    __slots__ = ("target_player_id", "reason", "seconds_ago")
    TARGET_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    SECONDS_AGO_FIELD_NUMBER: _ClassVar[int]
    target_player_id: int
    reason: _dota_shared_enums_pb2.EOverwatchReportReason
    seconds_ago: int
    def __init__(
        self,
        target_player_id: int | None = ...,
        reason: _dota_shared_enums_pb2.EOverwatchReportReason | str | None = ...,
        seconds_ago: int | None = ...,
    ) -> None: ...

class CDOTAClientMsg_AddCommunicationsReportMarker(_message.Message):
    __slots__ = ("target_player_id",)
    TARGET_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    target_player_id: int
    def __init__(self, target_player_id: int | None = ...) -> None: ...

class CDOTAClientMsg_AddCommunicationsBlockMarker(_message.Message):
    __slots__ = ("target_player_id",)
    TARGET_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    target_player_id: int
    def __init__(self, target_player_id: int | None = ...) -> None: ...

class CDOTAClientMsg_AghsStatusAlert(_message.Message):
    __slots__ = ("source_player_id", "target_player_id", "target_entindex", "alert_type")
    SOURCE_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    ALERT_TYPE_FIELD_NUMBER: _ClassVar[int]
    source_player_id: int
    target_player_id: int
    target_entindex: int
    alert_type: int
    def __init__(
        self,
        source_player_id: int | None = ...,
        target_player_id: int | None = ...,
        target_entindex: int | None = ...,
        alert_type: int | None = ...,
    ) -> None: ...

class CDOTAClientMsg_PerfReport(_message.Message):
    __slots__ = (
        "average_frame_time",
        "max_frame_time",
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
    )
    AVERAGE_FRAME_TIME_FIELD_NUMBER: _ClassVar[int]
    MAX_FRAME_TIME_FIELD_NUMBER: _ClassVar[int]
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
    average_frame_time: float
    max_frame_time: float
    average_compute_time: float
    max_compute_time: float
    average_client_tick_time: float
    max_client_tick_time: float
    average_client_simulate_time: float
    max_client_simulate_time: float
    average_output_time: float
    max_output_time: float
    average_wait_for_rendering_to_complete_time: float
    max_wait_for_rendering_to_complete_time: float
    average_swap_time: float
    max_swap_time: float
    average_frame_update_time: float
    max_frame_update_time: float
    average_idle_time: float
    max_idle_time: float
    average_input_processing_time: float
    max_input_processing_time: float
    def __init__(
        self,
        average_frame_time: float | None = ...,
        max_frame_time: float | None = ...,
        average_compute_time: float | None = ...,
        max_compute_time: float | None = ...,
        average_client_tick_time: float | None = ...,
        max_client_tick_time: float | None = ...,
        average_client_simulate_time: float | None = ...,
        max_client_simulate_time: float | None = ...,
        average_output_time: float | None = ...,
        max_output_time: float | None = ...,
        average_wait_for_rendering_to_complete_time: float | None = ...,
        max_wait_for_rendering_to_complete_time: float | None = ...,
        average_swap_time: float | None = ...,
        max_swap_time: float | None = ...,
        average_frame_update_time: float | None = ...,
        max_frame_update_time: float | None = ...,
        average_idle_time: float | None = ...,
        max_idle_time: float | None = ...,
        average_input_processing_time: float | None = ...,
        max_input_processing_time: float | None = ...,
    ) -> None: ...

class CDOTAClientMsg_ContextualTips_Subscribe_Entry(_message.Message):
    __slots__ = ("unsubscribe", "tip_id", "prior_display_count", "variants_seen")
    UNSUBSCRIBE_FIELD_NUMBER: _ClassVar[int]
    TIP_ID_FIELD_NUMBER: _ClassVar[int]
    PRIOR_DISPLAY_COUNT_FIELD_NUMBER: _ClassVar[int]
    VARIANTS_SEEN_FIELD_NUMBER: _ClassVar[int]
    unsubscribe: bool
    tip_id: int
    prior_display_count: int
    variants_seen: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        unsubscribe: bool = ...,
        tip_id: int | None = ...,
        prior_display_count: int | None = ...,
        variants_seen: _Iterable[int] | None = ...,
    ) -> None: ...

class CDOTAClientMsg_ContextualTips_Subscribe(_message.Message):
    __slots__ = ("tips",)
    TIPS_FIELD_NUMBER: _ClassVar[int]
    tips: _containers.RepeatedCompositeFieldContainer[CDOTAClientMsg_ContextualTips_Subscribe_Entry]
    def __init__(
        self, tips: _Iterable[CDOTAClientMsg_ContextualTips_Subscribe_Entry | _Mapping] | None = ...
    ) -> None: ...

class CDOTAClientMsg_ChatMessage(_message.Message):
    __slots__ = ("channel_type", "message_text")
    CHANNEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_TEXT_FIELD_NUMBER: _ClassVar[int]
    channel_type: int
    message_text: str
    def __init__(self, channel_type: int | None = ..., message_text: str | None = ...) -> None: ...

class CDOTAClientMsg_DuelAccepted(_message.Message):
    __slots__ = ("challenger_player_id", "accepter_player_id")
    CHALLENGER_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    ACCEPTER_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    challenger_player_id: int
    accepter_player_id: int
    def __init__(
        self, challenger_player_id: int | None = ..., accepter_player_id: int | None = ...
    ) -> None: ...

class CDOTAClientMsg_ChooseNeutralItem(_message.Message):
    __slots__ = ("neutral_item_index", "target_entindex", "slot_index")
    NEUTRAL_ITEM_INDEX_FIELD_NUMBER: _ClassVar[int]
    TARGET_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    SLOT_INDEX_FIELD_NUMBER: _ClassVar[int]
    neutral_item_index: int
    target_entindex: int
    slot_index: int
    def __init__(
        self,
        neutral_item_index: int | None = ...,
        target_entindex: int | None = ...,
        slot_index: int | None = ...,
    ) -> None: ...

class CDOTAClientMsg_RerollNeutralItem(_message.Message):
    __slots__ = ("target_entindex", "slot_index")
    TARGET_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    SLOT_INDEX_FIELD_NUMBER: _ClassVar[int]
    target_entindex: int
    slot_index: int
    def __init__(self, target_entindex: int | None = ..., slot_index: int | None = ...) -> None: ...

class CDOTAClientMsg_PlayerDraftPick(_message.Message):
    __slots__ = ("player_id",)
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    def __init__(self, player_id: int | None = ...) -> None: ...

class CDOTAClientMsg_PlayerDraftSuggest(_message.Message):
    __slots__ = ("player_id",)
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    def __init__(self, player_id: int | None = ...) -> None: ...

class CDOTAClientMsg_PlayerDraftPreferRole(_message.Message):
    __slots__ = ("role_idx", "desired")
    ROLE_IDX_FIELD_NUMBER: _ClassVar[int]
    DESIRED_FIELD_NUMBER: _ClassVar[int]
    role_idx: int
    desired: bool
    def __init__(self, role_idx: int | None = ..., desired: bool = ...) -> None: ...

class CDOTAClientMsg_PlayerDraftPreferTeam(_message.Message):
    __slots__ = ("team",)
    TEAM_FIELD_NUMBER: _ClassVar[int]
    team: int
    def __init__(self, team: int | None = ...) -> None: ...

class CDOTAClientMsg_AbilityAlert(_message.Message):
    __slots__ = (
        "ability_entindex",
        "ctrl_held",
        "owner_entindex",
        "ability_id",
        "primary_charges",
        "secondary_charges",
        "reclaim_time",
    )
    ABILITY_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    CTRL_HELD_FIELD_NUMBER: _ClassVar[int]
    OWNER_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    ABILITY_ID_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_CHARGES_FIELD_NUMBER: _ClassVar[int]
    SECONDARY_CHARGES_FIELD_NUMBER: _ClassVar[int]
    RECLAIM_TIME_FIELD_NUMBER: _ClassVar[int]
    ability_entindex: int
    ctrl_held: bool
    owner_entindex: int
    ability_id: int
    primary_charges: int
    secondary_charges: int
    reclaim_time: float
    def __init__(
        self,
        ability_entindex: int | None = ...,
        ctrl_held: bool = ...,
        owner_entindex: int | None = ...,
        ability_id: int | None = ...,
        primary_charges: int | None = ...,
        secondary_charges: int | None = ...,
        reclaim_time: float | None = ...,
    ) -> None: ...

class CDOTAClientMsg_SelectOverworldTokenRewards(_message.Message):
    __slots__ = ("token_ids",)
    TOKEN_IDS_FIELD_NUMBER: _ClassVar[int]
    token_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, token_ids: _Iterable[int] | None = ...) -> None: ...

class CDOTAClientMsg_FacetAlert(_message.Message):
    __slots__ = ("facet_strhash", "hero_entindex", "ctrl_held")
    FACET_STRHASH_FIELD_NUMBER: _ClassVar[int]
    HERO_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    CTRL_HELD_FIELD_NUMBER: _ClassVar[int]
    facet_strhash: int
    hero_entindex: int
    ctrl_held: bool
    def __init__(
        self,
        facet_strhash: int | None = ...,
        hero_entindex: int | None = ...,
        ctrl_held: bool = ...,
    ) -> None: ...

class CDOTAClientMsg_InnateAlert(_message.Message):
    __slots__ = ("ability_entindex", "ctrl_held")
    ABILITY_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    CTRL_HELD_FIELD_NUMBER: _ClassVar[int]
    ability_entindex: int
    ctrl_held: bool
    def __init__(self, ability_entindex: int | None = ..., ctrl_held: bool = ...) -> None: ...

class CDOTAClientMsg_SelectOverworldID(_message.Message):
    __slots__ = ("overworld_id",)
    OVERWORLD_ID_FIELD_NUMBER: _ClassVar[int]
    overworld_id: int
    def __init__(self, overworld_id: int | None = ...) -> None: ...

class CDOTAClientMsg_RoshanTimer(_message.Message):
    __slots__ = ("negative",)
    NEGATIVE_FIELD_NUMBER: _ClassVar[int]
    negative: bool
    def __init__(self, negative: bool = ...) -> None: ...

class CDOTAClientMsg_TormentorTimer(_message.Message):
    __slots__ = ("negative",)
    NEGATIVE_FIELD_NUMBER: _ClassVar[int]
    negative: bool
    def __init__(self, negative: bool = ...) -> None: ...

class CDOTAClientMsg_CraftNeutralItem(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CDOTAClientMsg_ChooseCraftedNeutralItem(_message.Message):
    __slots__ = ("neutral_item_index", "item_tier", "enhancement_index")
    NEUTRAL_ITEM_INDEX_FIELD_NUMBER: _ClassVar[int]
    ITEM_TIER_FIELD_NUMBER: _ClassVar[int]
    ENHANCEMENT_INDEX_FIELD_NUMBER: _ClassVar[int]
    neutral_item_index: int
    item_tier: int
    enhancement_index: int
    def __init__(
        self,
        neutral_item_index: int | None = ...,
        item_tier: int | None = ...,
        enhancement_index: int | None = ...,
    ) -> None: ...

class CDOTAClientMsg_TimerAlert(_message.Message):
    __slots__ = ("timer_alert_type",)
    TIMER_ALERT_TYPE_FIELD_NUMBER: _ClassVar[int]
    timer_alert_type: _dota_shared_enums_pb2.ETimerAlertType
    def __init__(
        self, timer_alert_type: _dota_shared_enums_pb2.ETimerAlertType | str | None = ...
    ) -> None: ...

class CDOTAClientMsg_MadstoneAlert(_message.Message):
    __slots__ = ("target_entindex",)
    TARGET_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    target_entindex: int
    def __init__(self, target_entindex: int | None = ...) -> None: ...

class CDOTAClientMsg_UpdateAutoCourierSettings(_message.Message):
    __slots__ = ("auto_deliver",)
    AUTO_DELIVER_FIELD_NUMBER: _ClassVar[int]
    auto_deliver: bool
    def __init__(self, auto_deliver: bool = ...) -> None: ...

class CDOTAClientMsg_AutoCourierExecute(_message.Message):
    __slots__ = ("target_entindex", "is_auto_deliver")
    TARGET_ENTINDEX_FIELD_NUMBER: _ClassVar[int]
    IS_AUTO_DELIVER_FIELD_NUMBER: _ClassVar[int]
    target_entindex: int
    is_auto_deliver: bool
    def __init__(self, target_entindex: int | None = ..., is_auto_deliver: bool = ...) -> None: ...

class CDOTAClientMsg_MonsterHunter_SelectInvestigation(_message.Message):
    __slots__ = ("investigation_index",)
    INVESTIGATION_INDEX_FIELD_NUMBER: _ClassVar[int]
    investigation_index: int
    def __init__(self, investigation_index: int | None = ...) -> None: ...

class CDOTAClientMsg_MonsterHunter_HuntAlert(_message.Message):
    __slots__ = ("investigation_state_index", "ctrl_pressed")
    INVESTIGATION_STATE_INDEX_FIELD_NUMBER: _ClassVar[int]
    CTRL_PRESSED_FIELD_NUMBER: _ClassVar[int]
    investigation_state_index: int
    ctrl_pressed: bool
    def __init__(
        self, investigation_state_index: int | None = ..., ctrl_pressed: bool = ...
    ) -> None: ...
