# Full Proto Dota2 Catalog

This page catalogs the full Dota 2 proto surface used by gem.

- Source proto files: **84**
- Generated Python protobuf modules (`*_pb2.py`, including subdirectories): **84**

## Index

Use this list to jump directly to a file section:

- [base_gcmessages.proto](#base-gcmessages-proto) — imports: 3, enums: 6, messages: 62
- [c_peer2peer_netmessages.proto](#c-peer2peer-netmessages-proto) — imports: 2, enums: 2, messages: 7
- [clientmessages.proto](#clientmessages-proto) — imports: 0, enums: 2, messages: 6
- [connectionless_netmessages.proto](#connectionless-netmessages-proto) — imports: 1, enums: 0, messages: 3
- [demo.proto](#demo-proto) — imports: 0, enums: 1, messages: 28
- [dota_broadcastmessages.proto](#dota-broadcastmessages-proto) — imports: 0, enums: 1, messages: 4
- [dota_client_enums.proto](#dota-client-enums-proto) — imports: 1, enums: 7, messages: 0
- [dota_clientmessages.proto](#dota-clientmessages-proto) — imports: 3, enums: 4, messages: 120
- [dota_commonmessages.proto](#dota-commonmessages-proto) — imports: 1, enums: 4, messages: 13
- [dota_fighting_game_p2p_messages.proto](#dota-fighting-game-p2p-messages-proto) — imports: 2, enums: 1, messages: 6
- [dota_gcmessages_client.proto](#dota-gcmessages-client-proto) — imports: 10, enums: 86, messages: 475
- [dota_gcmessages_client_bingo.proto](#dota-gcmessages-client-bingo-proto) — imports: 9, enums: 10, messages: 25
- [dota_gcmessages_client_candy_shop.proto](#dota-gcmessages-client-candy-shop-proto) — imports: 9, enums: 9, messages: 34
- [dota_gcmessages_client_chat.proto](#dota-gcmessages-client-chat-proto) — imports: 1, enums: 2, messages: 27
- [dota_gcmessages_client_coaching.proto](#dota-gcmessages-client-coaching-proto) — imports: 2, enums: 17, messages: 35
- [dota_gcmessages_client_craftworks.proto](#dota-gcmessages-client-craftworks-proto) — imports: 10, enums: 4, messages: 8
- [dota_gcmessages_client_fantasy.proto](#dota-gcmessages-client-fantasy-proto) — imports: 1, enums: 16, messages: 66
- [dota_gcmessages_client_guild.proto](#dota-gcmessages-client-guild-proto) — imports: 1, enums: 26, messages: 61
- [dota_gcmessages_client_guild_events.proto](#dota-gcmessages-client-guild-events-proto) — imports: 1, enums: 7, messages: 22
- [dota_gcmessages_client_match_management.proto](#dota-gcmessages-client-match-management-proto) — imports: 5, enums: 1, messages: 62
- [dota_gcmessages_client_showcase.proto](#dota-gcmessages-client-showcase-proto) — imports: 9, enums: 20, messages: 60
- [dota_gcmessages_client_team.proto](#dota-gcmessages-client-team-proto) — imports: 1, enums: 6, messages: 28
- [dota_gcmessages_client_tournament.proto](#dota-gcmessages-client-tournament-proto) — imports: 1, enums: 1, messages: 20
- [dota_gcmessages_client_watch.proto](#dota-gcmessages-client-watch-proto) — imports: 1, enums: 2, messages: 23
- [dota_gcmessages_common.proto](#dota-gcmessages-common-proto) — imports: 4, enums: 30, messages: 185
- [dota_gcmessages_common_battle_report.proto](#dota-gcmessages-common-battle-report-proto) — imports: 7, enums: 13, messages: 23
- [dota_gcmessages_common_bot_script.proto](#dota-gcmessages-common-bot-script-proto) — imports: 1, enums: 2, messages: 18
- [dota_gcmessages_common_craftworks.proto](#dota-gcmessages-common-craftworks-proto) — imports: 3, enums: 1, messages: 3
- [dota_gcmessages_common_fighting_game.proto](#dota-gcmessages-common-fighting-game-proto) — imports: 4, enums: 2, messages: 8
- [dota_gcmessages_common_item_battler.proto](#dota-gcmessages-common-item-battler-proto) — imports: 4, enums: 6, messages: 22
- [dota_gcmessages_common_league.proto](#dota-gcmessages-common-league-proto) — imports: 1, enums: 2, messages: 37
- [dota_gcmessages_common_lobby.proto](#dota-gcmessages-common-lobby-proto) — imports: 3, enums: 5, messages: 32
- [dota_gcmessages_common_match_management.proto](#dota-gcmessages-common-match-management-proto) — imports: 3, enums: 9, messages: 15
- [dota_gcmessages_common_monster_hunter.proto](#dota-gcmessages-common-monster-hunter-proto) — imports: 4, enums: 16, messages: 36
- [dota_gcmessages_common_overworld.proto](#dota-gcmessages-common-overworld-proto) — imports: 5, enums: 26, messages: 68
- [dota_gcmessages_common_survivors.proto](#dota-gcmessages-common-survivors-proto) — imports: 4, enums: 1, messages: 5
- [dota_gcmessages_msgid.proto](#dota-gcmessages-msgid-proto) — imports: 0, enums: 1, messages: 0
- [dota_gcmessages_server.proto](#dota-gcmessages-server-proto) — imports: 14, enums: 6, messages: 170
- [dota_gcmessages_webapi.proto](#dota-gcmessages-webapi-proto) — imports: 5, enums: 15, messages: 39
- [dota_hud_types.proto](#dota-hud-types-proto) — imports: 1, enums: 1, messages: 0
- [dota_match_metadata.proto](#dota-match-metadata-proto) — imports: 10, enums: 2, messages: 46
- [dota_modifiers.proto](#dota-modifiers-proto) — imports: 1, enums: 1, messages: 2
- [dota_scenariomessages.proto](#dota-scenariomessages-proto) — imports: 1, enums: 0, messages: 23
- [dota_shared_enums.proto](#dota-shared-enums-proto) — imports: 0, enums: 53, messages: 14
- [dota_usercmd.proto](#dota-usercmd-proto) — imports: 3, enums: 0, messages: 1
- [dota_usermessages.proto](#dota-usermessages-proto) — imports: 3, enums: 20, messages: 191
- [econ_gcmessages.proto](#econ-gcmessages-proto) — imports: 4, enums: 16, messages: 143
- [econ_shared_enums.proto](#econ-shared-enums-proto) — imports: 0, enums: 3, messages: 1
- [engine_gcmessages.proto](#engine-gcmessages-proto) — imports: 1, enums: 0, messages: 1
- [enums_clientserver.proto](#enums-clientserver-proto) — imports: 0, enums: 4, messages: 0
- [event_gcmessages_client.proto](#event-gcmessages-client-proto) — imports: 2, enums: 2, messages: 3
- [event_gcmessages_common.proto](#event-gcmessages-common-proto) — imports: 0, enums: 0, messages: 2
- [event_gcmessages_server.proto](#event-gcmessages-server-proto) — imports: 0, enums: 0, messages: 0
- [events.proto](#events-proto) — imports: 0, enums: 1, messages: 0
- [gameevents.proto](#gameevents-proto) — imports: 1, enums: 1, messages: 18
- [gcsdk_gcmessages.proto](#gcsdk-gcmessages-proto) — imports: 3, enums: 3, messages: 74
- [gcsystemmsgs.proto](#gcsystemmsgs-proto) — imports: 0, enums: 2, messages: 0
- [netmessages.proto](#netmessages-proto) — imports: 2, enums: 12, messages: 74
- [network_connection.proto](#network-connection-proto) — imports: 1, enums: 1, messages: 0
- [networkbasetypes.proto](#networkbasetypes-proto) — imports: 3, enums: 3, messages: 27
- [networksystem_protomessages.proto](#networksystem-protomessages-proto) — imports: 0, enums: 0, messages: 5
- [prediction_events.proto](#prediction-events-proto) — imports: 1, enums: 1, messages: 3
- [source2_steam_stats.proto](#source2-steam-stats-proto) — imports: 0, enums: 1, messages: 16
- [steamdatagram_messages_auth.proto](#steamdatagram-messages-auth-proto) — imports: 1, enums: 0, messages: 7
- [steamdatagram_messages_sdr.proto](#steamdatagram-messages-sdr-proto) — imports: 2, enums: 10, messages: 42
- [steammessages.proto](#steammessages-proto) — imports: 1, enums: 2, messages: 5
- [steammessages_base.proto](#steammessages-base-proto) — imports: 1, enums: 3, messages: 18
- [steammessages_cloud.steamworkssdk.proto](#steammessages-cloud-steamworkssdk-proto) — imports: 1, enums: 0, messages: 9
- [steammessages_gamenetworkingui.proto](#steammessages-gamenetworkingui-proto) — imports: 2, enums: 0, messages: 5
- [steammessages_helprequest.steamworkssdk.proto](#steammessages-helprequest-steamworkssdk-proto) — imports: 1, enums: 0, messages: 2
- [steammessages_int.proto](#steammessages-int-proto) — imports: 1, enums: 3, messages: 87
- [steammessages_oauth.steamworkssdk.proto](#steammessages-oauth-steamworkssdk-proto) — imports: 1, enums: 0, messages: 2
- [steammessages_player.steamworkssdk.proto](#steammessages-player-steamworkssdk-proto) — imports: 1, enums: 1, messages: 38
- [steammessages_publishedfile.steamworkssdk.proto](#steammessages-publishedfile-steamworkssdk-proto) — imports: 1, enums: 0, messages: 21
- [steammessages_steamlearn.steamworkssdk.proto](#steammessages-steamlearn-steamworkssdk-proto) — imports: 1, enums: 7, messages: 52
- [steammessages_unified_base.steamworkssdk.proto](#steammessages-unified-base-steamworkssdk-proto) — imports: 1, enums: 1, messages: 0
- [steamnetworkingsockets_messages.proto](#steamnetworkingsockets-messages-proto) — imports: 1, enums: 2, messages: 16
- [steamnetworkingsockets_messages_certs.proto](#steamnetworkingsockets-messages-certs-proto) — imports: 0, enums: 1, messages: 4
- [steamnetworkingsockets_messages_udp.proto](#steamnetworkingsockets-messages-udp-proto) — imports: 2, enums: 2, messages: 7
- [te.proto](#te-proto) — imports: 1, enums: 1, messages: 25
- [uifontfile_format.proto](#uifontfile-format-proto) — imports: 0, enums: 0, messages: 3
- [usercmd.proto](#usercmd-proto) — imports: 2, enums: 0, messages: 5
- [usermessages.proto](#usermessages-proto) — imports: 1, enums: 5, messages: 107
- [valveextensions.proto](#valveextensions-proto) — imports: 1, enums: 1, messages: 0

## Per-file declarations

Each file is collapsed by default. Expand to view its declarations.

<a id="base-gcmessages-proto"></a>
### base_gcmessages.proto

<details>
<summary><code>base_gcmessages.proto</code> — module: <code>base_gcmessages_pb2</code>; imports: 3; enums: 6; messages: 62</summary>

- Imports: steammessages.proto, gcsdk_gcmessages.proto, steammessages_steamlearn.steamworkssdk.proto

```text
5: enum EGCBaseMsg
32: enum ECustomGameInstallStatus
45: message CGCStorePurchaseInit_LineItem
54: message CMsgGCStorePurchaseInit
61: message CMsgGCStorePurchaseInitResponse
66: message CMsgClientPingData
74: message CMsgInviteToParty
82: message CMsgInviteToLobby
87: message CMsgInvitationCreated
93: message CMsgPartyInviteResponse
100: message CMsgLobbyInviteResponse
108: message CMsgKickFromParty
112: message CMsgLeaveParty
115: message CMsgCustomGameInstallStatus
121: message CMsgServerAvailable
125: message CMsgLANServerAvailable
129: message CSOEconGameAccountClient
140: message CMsgApplyStrangePart
145: message CMsgApplyPennantUpgrade
150: message CMsgApplyEggEssence
155: message CSOEconItemAttribute
161: message CSOEconItemEquipped
166: message CSOEconItem
183: message CMsgSortItems
187: message CMsgItemAcknowledged
196: message CMsgSetItemPositions
197: message ItemPosition
205: message CMsgGCStorePurchaseCancel
209: message CMsgGCStorePurchaseCancelResponse
213: message CMsgGCStorePurchaseFinalize
217: message CMsgGCStorePurchaseFinalizeResponse
222: message CMsgGCToGCBannedWordListUpdated
226: message CMsgGCToGCDirtySDOCache
231: message CMsgSDONoMemcached
234: message CMsgGCToGCUpdateSQLKeyValue
238: message CMsgGCServerVersionUpdated
242: message CMsgGCClientVersionUpdated
246: message CMsgGCToGCWebAPIAccountChanged
249: message CMsgExtractGems
255: message CMsgExtractGemsResponse
256: enum EExtractGems
268: message CMsgAddSocket
274: message CMsgAddSocketResponse
275: enum EAddSocket
287: message CMsgAddItemToSocketData
292: message CMsgAddItemToSocket
297: message CMsgAddItemToSocketResponse
298: enum EAddGem
314: message CMsgResetStrangeGemCount
319: message CMsgResetStrangeGemCountResponse
320: enum EResetGem
331: message CMsgGCToClientPollFileRequest
337: message CMsgGCToClientPollFileResponse
343: message CMsgGCToGCPerformManualOp
348: message CMsgGCToGCPerformManualOpCompleted
353: message CMsgGCToGCReloadServerRegionSettings
356: message CMsgGCAdditionalWelcomeMsgList
360: message CMsgApplyRemoteConVars
361: message ConVar
372: message CMsgGCToClientApplyRemoteConVars
376: message CMsgGCToServerApplyRemoteConVars
380: message CMsgClientToGCIntegrityStatus
381: message keyvalue
393: message CMsgClientToGCAggregateMetrics
394: message SingleMetric
402: message CMsgGCToClientAggregateMetricsBackoff
406: message CMsgGCToServerSteamLearnAccessTokensChanged
410: message CMsgGCToServerSteamLearnUseHTTP
```

</details>

<a id="c-peer2peer-netmessages-proto"></a>
### c_peer2peer_netmessages.proto

<details>
<summary><code>c_peer2peer_netmessages.proto</code> — module: <code>c_peer2peer_netmessages_pb2</code>; imports: 2; enums: 2; messages: 7</summary>

- Imports: netmessages.proto, networkbasetypes.proto

```text
4: enum P2P_Messages
14: message CP2P_TextMessage
18: message CSteam_Voice_Encoding
22: message CP2P_Voice
23: enum Handler_Flags
31: message CP2P_Ping
36: message CP2P_VRAvatarPosition
37: message COrientation
48: message CP2P_WatchSynchronization
```

</details>

<a id="clientmessages-proto"></a>
### clientmessages.proto

<details>
<summary><code>clientmessages.proto</code> — module: <code>clientmessages_pb2</code>; imports: 0; enums: 2; messages: 6</summary>

- Imports: *(none)*

```text
1: enum EBaseClientMessages
11: enum EClientUIEvent
17: message CClientMsg_CustomGameEvent
22: message CClientMsg_CustomGameEventBounce
28: message CClientMsg_ClientUIEvent
36: message CClientMsg_DevPaletteVisibilityChangedEvent
40: message CClientMsg_WorldUIControllerHasPanelChangedEvent
46: message CClientMsg_RotateAnchor
```

</details>

<a id="connectionless-netmessages-proto"></a>
### connectionless_netmessages.proto

<details>
<summary><code>connectionless_netmessages.proto</code> — module: <code>connectionless_netmessages_pb2</code>; imports: 1; enums: 0; messages: 3</summary>

- Imports: netmessages.proto

```text
3: message C2S_CONNECT_SameProcessCheck
8: message C2S_CONNECT_Message
21: message C2S_CONNECTION_Message
```

</details>

<a id="demo-proto"></a>
### demo.proto

<details>
<summary><code>demo.proto</code> — module: <code>demo_pb2</code>; imports: 0; enums: 1; messages: 28</summary>

- Imports: *(none)*

```text
1: enum EDemoCommands
26: message CDemoFileHeader
44: message CGameInfo
45: message CDotaGameInfo
46: message CPlayerInfo
54: message CHeroSelectEvent
73: message CCSGameInfo
81: message CDemoFileInfo
88: message CDemoPacket
92: message CDemoFullPacket
97: message CDemoSaveGame
104: message CDemoSyncTick
107: message CDemoConsoleCmd
111: message CDemoSendTables
115: message CDemoClassInfo
116: message class_t
125: message CDemoCustomData
130: message CDemoCustomDataCallbacks
134: message CDemoAnimationHeader
140: message CDemoAnimationData
148: message CDemoStringTables
149: message items_t
154: message table_t
164: message CDemoStop
167: message CDemoUserCmd
172: message CDemoSpawnGroups
176: message CDemoSpawnGroupsHLTVBroadcast
180: message CDemoRecovery
181: message DemoInitialSpawnGroupEntry
```

</details>

<a id="dota-broadcastmessages-proto"></a>
### dota_broadcastmessages.proto

<details>
<summary><code>dota_broadcastmessages.proto</code> — module: <code>dota_broadcastmessages_pb2</code>; imports: 0; enums: 1; messages: 4</summary>

- Imports: *(none)*

```text
1: enum EDotaBroadcastMessages
6: message CDOTABroadcastMsg
11: message CDOTABroadcastMsg_LANLobbyRequest
14: message CDOTABroadcastMsg_LANLobbyReply
15: message CLobbyMember
```

</details>

<a id="dota-client-enums-proto"></a>
### dota_client_enums.proto

<details>
<summary><code>dota_client_enums.proto</code> — module: <code>dota_client_enums_pb2</code>; imports: 1; enums: 7; messages: 0</summary>

- Imports: dota_shared_enums.proto

```text
3: enum ETournamentTemplate
8: enum ETournamentGameState
21: enum ETournamentTeamState
45: enum ETournamentState
60: enum ETournamentNodeState
77: enum EDOTAGroupMergeResult
90: enum EPartyBeaconType
```

</details>

<a id="dota-clientmessages-proto"></a>
### dota_clientmessages.proto

<details>
<summary><code>dota_clientmessages.proto</code> — module: <code>dota_clientmessages_pb2</code>; imports: 3; enums: 4; messages: 120</summary>

- Imports: dota_commonmessages.proto, dota_shared_enums.proto, base_gcmessages.proto

```text
5: enum EDotaClientMessages
136: message CDOTAClientMsg_MapPing
140: message CDOTAClientMsg_ItemAlert
144: message CDOTAClientMsg_EnemyItemAlert
154: message CDOTAClientMsg_ModifierAlert
159: message CDOTAClientMsg_ClickedBuff
164: message CDOTAClientMsg_HPManaAlert
169: message CDOTAClientMsg_NeutralCampAlert
175: message CDOTAClientMsg_GlyphAlert
179: message CDOTAClientMsg_RadarAlert
183: message CDOTAClientMsg_MapLine
187: message CDOTAClientMsg_AspectRatio
191: message CDOTAClientMsg_UnitsAutoAttackMode
192: enum EMode
199: enum EUnitType
208: message CDOTAClientMsg_UnitsAutoAttackAfterSpell
212: message CDOTAClientMsg_TeleportRequiresHalt
216: message CDOTAClientMsg_ChannelRequiresHalt
220: message CDOTAClientMsg_InteractionChannelsRequireHalt
224: message CDOTAClientMsg_AbilitySpecificChannelRequiresHalt
230: message CDOTAClientMsg_SearchString
234: message CDOTAClientMsg_Pause
237: message CDOTAClientMsg_ShopViewMode
241: message CDOTAClientMsg_SetUnitShareFlag
247: message CDOTAClientMsg_SwapRequest
251: message CDOTAClientMsg_SwapAccept
255: message CDOTAClientMsg_WorldLine
259: message CDOTAClientMsg_RequestGraphUpdate
262: message CDOTAClientMsg_ChatWheel
268: message CDOTAClientMsg_SendStatPopup
272: message CDOTAClientMsg_DismissAllStatPopups
276: message CDOTAClientMsg_BeginLastHitChallenge
281: message CDOTAClientMsg_UpdateQuickBuyItem
287: message CDOTAClientMsg_UpdateQuickBuy
292: message CDOTAClientMsg_QuickBuyAction
293: enum EActionType
318: message CDOTAClientMsg_RecordVote
322: message CDOTAClientMsg_WillPurchaseAlert
328: message CDOTAClientMsg_BuyBackStateAlert
331: message CDOTAClientMsg_QuickBuyAlert
338: message CDOTAClientMsg_PlayerShowCase
342: message CDOTAClientMsg_CameraZoomAmount
346: message CDOTAClientMsg_BroadcasterUsingCameraman
350: message CDOTAClientMsg_BroadcasterUsingAssistedCameraOperator
354: message CDOTAClientMsg_FillEmptySlotsWithBots
358: message CDOTAClientMsg_HeroStatueLike
362: message CDOTAClientMsg_EventCNY2015Cmd
366: message CDOTAClientMsg_DemoHero
367: message PreviewItem
382: message CDOTAClientMsg_ChallengeSelect
388: message CDOTAClientMsg_ChallengeReroll
395: message CDOTAClientMsg_CoinWager
399: message CDOTAClientMsg_CoinWagerToken
403: message CDOTAClientMsg_RankWager
407: message CDOTAClientMsg_PlayerBounty
411: message CDOTAClientMsg_EventPointsTip
415: message CDOTAClientMsg_ExecuteOrders
420: message CDOTAClientMsg_XPAlert
425: message CDOTAClientMsg_TalentTreeAlert
432: message CDOTAClientMsg_KillcamDamageTaken
441: message CDOTAClientMsg_KillMyHero
444: message CDOTAClientMsg_QuestStatus
454: message CDOTAClientMsg_ToggleAutoattack
459: message CDOTAClientMsg_SpecialAbility
464: message CDOTAClientMsg_SetEnemyStartingPosition
469: message CDOTAClientMsg_SetDesiredWardPlacement
475: message CDOTAClientMsg_RollDice
481: message CDOTAClientMsg_FlipCoin
485: message CDOTAClientMsg_RequestItemSuggestions
488: message CDOTAClientMsg_SuggestItemPreference
489: message ItemPreference
497: message CDOTAClientMsg_SuggestItemRefresh
501: message CDOTAClientMsg_SuggestItemGetVariants
505: message CDOTAClientMsg_SuggestItemSelectVariant
509: message CDOTAClientMsg_MakeTeamCaptain
513: message CDOTAClientMsg_HelpTipSystemStateChanged
517: message CDOTAClientMsg_RequestBulkCombatLog
524: message CDOTAClientMsg_AbilityDraftRequestAbility
531: message CDOTAClientMsg_GuideSelectOption
536: message CDOTAClientMsg_GuideSelected
541: message CDOTAClientMsg_DamageReport
548: message CDOTAClientMsg_SalutePlayer
553: message CDOTAClientMsg_GiftPlayer
558: message CDOTAClientMsg_GiftEveryone
562: message CDOTAClientMsg_TipAlert
566: message CDOTAClientMsg_EmptyTeleportAlert
570: message CDOTAClientMsg_SetCavernMapVariant
574: message CDOTAClientMsg_PauseGameOrder
579: message CDOTAClientMsg_VersusScene_PlayerBehavior
586: message CDOTAClientMsg_EmptyItemSlotAlert
591: message CDOTAClientMsg_AddOverwatchReportMarker
597: message CDOTAClientMsg_AddCommunicationsReportMarker
601: message CDOTAClientMsg_AddCommunicationsBlockMarker
605: message CDOTAClientMsg_AghsStatusAlert
612: message CDOTAClientMsg_PerfReport
637: message CDOTAClientMsg_ContextualTips_Subscribe_Entry
644: message CDOTAClientMsg_ContextualTips_Subscribe
648: message CDOTAClientMsg_ChatMessage
653: message CDOTAClientMsg_DuelAccepted
658: message CDOTAClientMsg_ChooseNeutralItem
664: message CDOTAClientMsg_RerollNeutralItem
669: message CDOTAClientMsg_PlayerDraftPick
673: message CDOTAClientMsg_PlayerDraftSuggest
677: message CDOTAClientMsg_PlayerDraftPreferRole
682: message CDOTAClientMsg_PlayerDraftPreferTeam
686: message CDOTAClientMsg_AbilityAlert
696: message CDOTAClientMsg_SelectOverworldTokenRewards
700: message CDOTAClientMsg_FacetAlert
706: message CDOTAClientMsg_InnateAlert
711: message CDOTAClientMsg_SelectOverworldID
715: message CDOTAClientMsg_RoshanTimer
719: message CDOTAClientMsg_TormentorTimer
723: message CDOTAClientMsg_CraftNeutralItem
726: message CDOTAClientMsg_ChooseCraftedNeutralItem
732: message CDOTAClientMsg_TimerAlert
736: message CDOTAClientMsg_MadstoneAlert
740: message CDOTAClientMsg_UpdateAutoCourierSettings
744: message CDOTAClientMsg_AutoCourierExecute
749: message CDOTAClientMsg_MonsterHunter_SelectInvestigation
753: message CDOTAClientMsg_MonsterHunter_HuntAlert
758: message CDOTAClientMsg_ChooseDeityBlessing
762: message CDOTAClientMsg_ChooseAghanimUpgrade
768: message CDOTAClientMsg_ChooseAbilityImbue
772: message CDOTAClientMsg_NetworkStats
```

</details>

<a id="dota-commonmessages-proto"></a>
### dota_commonmessages.proto

<details>
<summary><code>dota_commonmessages.proto</code> — module: <code>dota_commonmessages_pb2</code>; imports: 1; enums: 4; messages: 13</summary>

- Imports: networkbasetypes.proto

```text
3: enum EPingSource
10: enum EDOTAStatPopupTypes
19: enum dotaunitorder_t
65: enum EDOTAVersusScenePlayerBehavior
71: message CDOTAMsg_PingWaypointPath
77: message CDOTAMsg_LocationPing
87: message CDOTAMsg_ItemAlert
93: message CDOTAMsg_MapLine
99: message CDOTAMsg_WorldLine
107: message CDOTAMsg_SendStatPopup
117: message CDOTAMsg_DismissAllStatPopups
121: message CDOTAMsg_CoachHUDPing
127: message CDOTAMsg_UnitOrder
137: message VersusScene_PlayActivity
138: message ActivityInfo
148: message VersusScene_ChatWheel
153: message VersusScene_PlaybackRate
```

</details>

<a id="dota-fighting-game-p2p-messages-proto"></a>
### dota_fighting_game_p2p_messages.proto

<details>
<summary><code>dota_fighting_game_p2p_messages.proto</code> — module: <code>dota_fighting_game_p2p_messages_pb2</code>; imports: 2; enums: 1; messages: 6</summary>

- Imports: netmessages.proto, networkbasetypes.proto

```text
4: message CMsgFightingGame_GameData_Fighting
5: message InputSample
19: message CMsgFightingGame_GameData_CharacterSelect
20: message Item
33: message CMsgFightingGame_GameData_Loaded
40: message CP2P_FightingGame_GameData
41: enum EState
```

</details>

<a id="dota-gcmessages-client-proto"></a>
### dota_gcmessages_client.proto

<details>
<summary><code>dota_gcmessages_client.proto</code> — module: <code>dota_gcmessages_client_pb2</code>; imports: 10; enums: 86; messages: 475</summary>

- Imports: steammessages.proto, dota_shared_enums.proto, dota_gcmessages_common.proto, dota_gcmessages_webapi.proto, gcsdk_gcmessages.proto, dota_gcmessages_common_lobby.proto, dota_gcmessages_common_match_management.proto, base_gcmessages.proto, econ_gcmessages.proto, valveextensions.proto

```text
12: enum CMsgDOTARequestMatches_SkillLevel
19: enum DOTA_WatchReplayType
24: enum EItemEditorReservationResult
31: enum EWeekendTourneyRichPresenceEvent
38: enum EDOTATriviaAnswerResult
47: enum EPurchaseHeroRelicResult
58: enum EDevEventRequestResult
68: enum ESupportEventRequestResult
85: enum EUnderDraftResponse
100: enum EDOTADraftTriviaAnswerResult
109: enum CMsgClientToGCUpdateComicBookStat_Type
115: message CMsgClientSuspended
119: message CMsgBalancedShuffleLobby
122: message CMsgInitialQuestionnaireResponse
126: message CMsgDOTARequestMatchesResponse
127: message Series
140: message CMsgDOTAPopup
141: enum PopupID
218: message CMsgDOTAReportsRemainingRequest
221: message CMsgDOTAReportsRemainingResponse
230: message CMsgDOTASubmitPlayerReport
237: message CMsgDOTASubmitPlayerReportResponse
238: enum EResult
261: message CMsgDOTASubmitPlayerAvoidRequest
267: message CMsgDOTASubmitPlayerAvoidRequestResponse
273: message CMsgDOTASubmitPlayerReportV2
282: message CMsgDOTASubmitPlayerReportResponseV2
283: enum EResult
307: message CMsgDOTASubmitLobbyMVPVote
311: message CMsgDOTASubmitLobbyMVPVoteResponse
316: message CMsgDOTALobbyMVPAwarded
321: message CMsgDOTAKickedFromMatchmakingQueue
325: message CMsgGCMatchDetailsRequest
329: message CMsgGCMatchDetailsResponse
335: message CMsgDOTAProfileTickets
336: message LeaguePass
346: message CMsgClientToGCGetProfileTickets
350: message CMsgGCToClientPartySearchInvites
354: message CMsgDOTAWelcome
355: message CExtraMsg
381: message CSODOTAGameHeroFavorites
386: message CMsgDOTAMatchVotes
387: message PlayerVote
396: message CMsgMatchmakingMatchGroupInfo
403: message CMsgDOTAMatchmakingStatsRequest
406: message CMsgDOTAMatchmakingStatsResponse
412: message CMsgDOTAUpdateMatchmakingStats
416: message CMsgDOTAUpdateMatchManagementStats
420: message CMsgDOTASetMatchHistoryAccess
424: message CMsgDOTASetMatchHistoryAccessResponse
428: message CMsgDOTANotifyAccountFlagsChange
433: message CMsgDOTASetProfilePrivacy
437: message CMsgDOTASetProfilePrivacyResponse
441: message CMsgUpgradeLeagueItem
446: message CMsgUpgradeLeagueItemResponse
449: message CMsgGCWatchDownloadedReplay
454: message CMsgClientToGCWatchingBroadcast
458: message CMsgClientsRejoinChatChannels
461: message CMsgGCGetHeroStandings
464: message CMsgGCGetHeroStandingsResponse
465: message Hero
498: message CMatchPlayerTimedStatAverages
514: message CMatchPlayerTimedStatStdDeviations
530: message CMsgGCGetHeroTimedStatsResponse
531: message TimedStatsContainer
540: message RankChunkedStats
549: message CMsgGCItemEditorReservationsRequest
552: message CMsgGCItemEditorReservation
557: message CMsgGCItemEditorReservationsResponse
561: message CMsgGCItemEditorReserveItemDef
566: message CMsgGCItemEditorReserveItemDefResponse
572: message CMsgGCItemEditorReleaseReservation
577: message CMsgGCItemEditorReleaseReservationResponse
582: message CMsgFlipLobbyTeams
585: message CMsgGCLobbyUpdateBroadcastChannelInfo
592: message CMsgDOTAClaimEventActionData
593: message GrantItemGiftData
602: message CMsgDOTAClaimEventAction
611: message CMsgClientToGCClaimEventActionUsingItem
619: message CMsgClientToGCClaimEventActionUsingItemResponse
623: message CMsgGCToClientClaimEventActionUsingItemCompleted
628: message CMsgDOTAGetEventPoints
633: message CMsgDOTAGetEventPointsResponse
634: message Action
651: message CMsgDOTAGetPeriodicResource
657: message CMsgDOTAGetPeriodicResourceResponse
662: message CMsgDOTAPeriodicResourceUpdated
667: message CMsgDOTACompendiumSelection
673: message CMsgDOTACompendiumSelectionResponse
677: message CMsgDOTACompendiumRemoveAllSelections
681: message CMsgDOTACompendiumRemoveAllSelectionsResponse
685: message CMsgDOTACompendiumData
689: message CMsgDOTACompendiumDataRequest
694: message CMsgDOTACompendiumDataResponse
701: message CMsgDOTAGetPlayerMatchHistory
712: message CMsgDOTAGetPlayerMatchHistoryResponse
713: message Match
742: message CMsgGCNotificationsRequest
745: message CMsgGCNotifications_Notification
756: message CMsgGCNotificationsUpdate
757: enum EResult
766: message CMsgGCNotificationsResponse
770: message CMsgGCNotificationsMarkReadRequest
773: message CMsgGCPlayerInfoSubmit
784: message CMsgGCPlayerInfoSubmitResponse
785: enum EResult
795: message CMsgDOTAEmoticonAccessSDO
800: message CMsgClientToGCEmoticonDataRequest
803: message CMsgGCToClientEmoticonData
807: message CMsgGCToClientTournamentItemDrop
812: message CMsgClientToGCGetAllHeroOrder
815: message CMsgClientToGCGetAllHeroOrderResponse
819: message CMsgClientToGCGetAllHeroProgress
823: message CMsgClientToGCGetAllHeroProgressResponse
846: message CMsgClientToGCGetTrophyList
850: message CMsgClientToGCGetTrophyListResponse
851: message Trophy
860: message CMsgGCToClientTrophyAwarded
867: message CMsgClientToGCRankRequest
871: message CMsgGCToClientRankResponse
872: enum EResultCode
885: message CMsgGCToClientRankUpdate
890: message CMsgClientToGCGetProfileCard
894: message CMsgClientToGCSetProfileCardSlots
895: message CardSlot
904: message CMsgClientToGCGetProfileCardStats
907: message CMsgClientToGCCreateHeroStatue
919: message CMsgGCToClientHeroStatueCreateResult
923: message CMsgClientToGCPlayerStatsRequest
927: message CMsgGCToClientPlayerStatsResponse
953: message CMsgClientToGCCustomGamesFriendsPlayedRequest
956: message CMsgGCToClientCustomGamesFriendsPlayedResponse
957: message CustomGame
966: message CMsgClientToGCSocialFeedPostCommentRequest
971: message CMsgGCToClientSocialFeedPostCommentResponse
975: message CMsgClientToGCSocialFeedPostMessageRequest
981: message CMsgGCToClientSocialFeedPostMessageResponse
985: message CMsgClientToGCFriendsPlayedCustomGameRequest
989: message CMsgGCToClientFriendsPlayedCustomGameResponse
994: message CMsgDOTAPartyRichPresence
995: message Member
1000: message WeekendTourney
1021: message CMsgDOTALobbyRichPresence
1033: message CMsgDOTACustomGameListenServerStartedLoading
1040: message CMsgDOTACustomGameClientFinishedLoading
1049: message CMsgClientToGCApplyGemCombiner
1054: message CMsgClientToGCH264Unsupported
1057: message CMsgClientToGCGetQuestProgress
1061: message CMsgClientToGCGetQuestProgressResponse
1062: message Challenge
1071: message Quest
1080: message CMsgGCToClientMatchSignedOut
1084: message CMsgGCGetHeroStatsHistory
1088: message CMsgGCGetHeroStatsHistoryResponse
1089: enum EResponse
1101: message CMsgPlayerConductScorecardRequest
1104: message CMsgPlayerConductScorecard
1105: enum EBehaviorRating
1130: message CMsgClientToGCWageringRequest
1134: message CMsgGCToClientWageringResponse
1150: message CMsgGCToClientWageringUpdate
1155: message CMsgGCToClientArcanaVotesUpdate
1160: message CMsgClientToGCGetEventGoals
1164: message CMsgEventGoals
1165: message EventGoal
1174: message CMsgGCToGCLeaguePredictions
1178: message CMsgPredictionRankings
1179: message PredictionLine
1186: message Prediction
1194: message CMsgPredictionResults
1195: message ResultBreakdown
1200: message Result
1208: message CMsgClientToGCHasPlayerVotedForMVP
1212: message CMsgClientToGCHasPlayerVotedForMVPResponse
1216: message CMsgClientToGCVoteForMVP
1221: message CMsgClientToGCVoteForMVPResponse
1225: message CMsgClientToGCMVPVoteTimeout
1229: message CMsgClientToGCMVPVoteTimeoutResponse
1233: message CMsgClientToGCTeammateStatsRequest
1236: message CMsgClientToGCTeammateStatsResponse
1237: message TeammateStat
1250: message CMsgClientToGCVoteForArcana
1254: message CMsgClientToGCVoteForArcanaResponse
1255: enum Result
1264: message CMsgClientToGCRequestArcanaVotesRemaining
1267: message CMsgClientToGCRequestArcanaVotesRemainingResponse
1274: message CMsgClientToGCRequestEventPointLogV2
1278: message CMsgClientToGCRequestEventPointLogResponseV2
1279: message LogEntry
1291: message CMsgClientToGCPublishUserStat
1296: message CMsgClientToGCRequestSlarkGameResult
1302: message CMsgClientToGCRequestSlarkGameResultResponse
1307: message CMsgGCToClientQuestProgressUpdated
1308: message Challenge
1322: message CMsgDOTARedeemItem
1328: message CMsgDOTARedeemItemResponse
1329: enum EResultCode
1337: message CMsgClientToGCSelectCompendiumInGamePrediction
1338: message Prediction
1348: message CMsgClientToGCSelectCompendiumInGamePredictionResponse
1349: enum EResult
1359: message CMsgClientToGCOpenPlayerCardPack
1366: message CMsgClientToGCOpenPlayerCardPackResponse
1367: enum Result
1381: message CMsgClientToGCRecyclePlayerCard
1386: message CMsgClientToGCRecyclePlayerCardResponse
1387: enum Result
1401: message CMsgClientToGCCreatePlayerCardPack
1407: message CMsgClientToGCCreatePlayerCardPackResponse
1408: enum Result
1421: message CMsgClientToGCCreateTeamPlayerCardPack
1428: message CMsgClientToGCCreateTeamPlayerCardPackResponse
1429: enum Result
1442: message CMsgGCToClientBattlePassRollup_International2016
1443: message Questlines
1451: message Wagering
1459: message Achievements
1465: message BattleCup
1470: message Predictions
1476: message Bracket
1481: message PlayerCard
1486: message FantasyChallenge
1502: message CMsgGCToClientBattlePassRollup_Fall2016
1503: message Questlines
1511: message Wagering
1519: message Achievements
1525: message BattleCup
1530: message Predictions
1536: message Bracket
1541: message PlayerCard
1546: message FantasyChallenge
1562: message CMsgGCToClientBattlePassRollup_Winter2017
1563: message Questlines
1571: message Wagering
1579: message Achievements
1585: message BattleCup
1590: message Predictions
1596: message Bracket
1601: message PlayerCard
1606: message FantasyChallenge
1622: message CMsgGCToClientBattlePassRollup_TI7
1623: message Questlines
1631: message Wagering
1639: message Achievements
1645: message BattleCup
1650: message Predictions
1656: message Bracket
1661: message PlayerCard
1666: message FantasyChallenge
1682: message CMsgGCToClientBattlePassRollup_TI8
1683: message CavernCrawl
1690: message Wagering
1698: message Achievements
1704: message Predictions
1710: message Bracket
1715: message PlayerCard
1720: message FantasyChallenge
1735: message CMsgGCToClientBattlePassRollup_TI9
1739: message CMsgGCToClientBattlePassRollup_TI10
1743: message CMsgGCToClientBattlePassRollupRequest
1748: message CMsgGCToClientBattlePassRollupResponse
1758: message CMsgGCToClientBattlePassRollupListRequest
1762: message CMsgGCToClientBattlePassRollupListResponse
1763: message EventInfo
1771: message CMsgClientToGCTransferSeasonalMMRRequest
1775: message CMsgClientToGCTransferSeasonalMMRResponse
1779: message CMsgGCToClientPlaytestStatus
1783: message CMsgClientToGCJoinPlaytest
1787: message CMsgClientToGCJoinPlaytestResponse
1791: message CMsgDOTASetFavoriteTeam
1796: message CMsgDOTATriviaCurrentQuestions
1801: message CMsgDOTASubmitTriviaQuestionAnswer
1806: message CMsgDOTASubmitTriviaQuestionAnswerResponse
1810: message CMsgDOTAStartTriviaSession
1813: message CMsgDOTAStartTriviaSessionResponse
1818: message CMsgDOTAAnchorPhoneNumberRequest
1821: message CMsgDOTAAnchorPhoneNumberResponse
1822: enum Result
1834: message CMsgDOTAUnanchorPhoneNumberRequest
1837: message CMsgDOTAUnanchorPhoneNumberResponse
1838: enum Result
1846: message CMsgGCToClientCommendNotification
1853: message CMsgDOTAClientToGCQuickStatsRequest
1860: message CMsgDOTAClientToGCQuickStatsResponse
1861: message SimpleStats
1877: message CMsgDOTASelectionPriorityChoiceRequest
1881: message CMsgDOTASelectionPriorityChoiceResponse
1882: enum Result
1890: message CMsgDOTAGameAutographReward
1894: message CMsgDOTAGameAutographRewardResponse
1895: enum Result
1903: message CMsgDOTADestroyLobbyRequest
1906: message CMsgDOTADestroyLobbyResponse
1907: enum Result
1915: message CMsgDOTAGetRecentPlayTimeFriendsRequest
1918: message CMsgDOTAGetRecentPlayTimeFriendsResponse
1922: message CMsgPurchaseItemWithEventPoints
1929: message CMsgPurchaseItemWithEventPointsResponse
1930: enum Result
1950: message CMsgPurchaseHeroRandomRelic
1955: message CMsgPurchaseHeroRandomRelicResponse
1960: message CMsgClientToGCRequestPlusWeeklyChallengeResult
1965: message CMsgClientToGCRequestPlusWeeklyChallengeResultResponse
1968: message CMsgProfileRequest
1972: message CMsgProfileResponse
1973: message FeaturedHero
1981: message MatchInfo
1989: enum EResponse
2005: message CMsgProfileUpdate
2010: message CMsgProfileUpdateResponse
2011: enum Result
2022: message CMsgTalentWinRates
2029: message CMsgGlobalHeroAverages
2041: message CMsgHeroGlobalDataRequest
2045: message CMsgHeroGlobalDataResponse
2046: message GraphData
2053: message WeekData
2060: message HeroDataPerRankChunk
2072: message CMsgHeroGlobalDataAllHeroes
2076: message CMsgHeroGlobalDataHeroesAlliesAndEnemies
2077: message HeroData
2085: message RankedHeroData
2093: message CMsgPrivateMetadataKeyRequest
2097: message CMsgPrivateMetadataKeyResponse
2101: message CMsgActivatePlusFreeTrialResponse
2102: enum Result
2113: message CMsgGCToClientCavernCrawlMapPathCompleted
2114: message CompletedPathInfo
2126: message CMsgGCToClientCavernCrawlMapUpdated
2130: message CMsgClientToGCCavernCrawlClaimRoom
2136: message CMsgClientToGCCavernCrawlClaimRoomResponse
2137: enum Result
2146: message CMsgClientToGCCavernCrawlUseItemOnRoom
2153: message CMsgClientToGCCavernCrawlUseItemOnRoomResponse
2154: enum Result
2163: message CMsgClientToGCCavernCrawlUseItemOnPath
2170: message CMsgClientToGCCavernCrawlUseItemOnPathResponse
2171: enum Result
2180: message CMsgClientToGCCavernCrawlRequestMapState
2184: message CMsgClientToGCCavernCrawlRequestMapStateResponse
2185: message SwappedChallenge
2190: message InventoryItem
2195: message TreasureMap
2200: message MapVariant
2219: enum Result
2231: message CMsgClientToGCCavernCrawlGetClaimedRoomCount
2235: message CMsgClientToGCCavernCrawlGetClaimedRoomCountResponse
2236: message MapVariant
2241: enum Result
2252: message CMsgDOTAMutationList
2253: message Mutation
2262: message CMsgEventTipsSummaryRequest
2267: message CMsgEventTipsSummaryResponse
2268: message Tipper
2277: message CMsgSocialFeedRequest
2282: message CMsgSocialFeedResponse
2283: message FeedEvent
2297: enum Result
2310: message CMsgSocialFeedCommentsRequest
2314: message CMsgSocialFeedCommentsResponse
2315: message FeedComment
2321: enum Result
2331: message CMsgClientToGCPlayerCardSpecificPurchaseRequest
2337: message CMsgClientToGCPlayerCardSpecificPurchaseResponse
2338: enum Result
2351: message CMsgClientToGCRequestContestVotes
2355: message CMsgClientToGCRequestContestVotesResponse
2356: message ItemVote
2361: enum EResponse
2372: message CMsgClientToGCRecordContestVote
2378: message CMsgGCToClientRecordContestVoteResponse
2379: enum EResult
2391: message CMsgDevGrantEventPoints
2397: message CMsgDevGrantEventPointsResponse
2401: message CMsgDevGrantEventAction
2407: message CMsgDevGrantEventActionResponse
2411: message CMsgDevDeleteEventActions
2418: message CMsgDevDeleteEventActionsResponse
2422: message CMsgDevResetEventState
2427: message CMsgDevResetEventStateResponse
2431: message CMsgDevReloadAllEvents
2434: message CMsgDevReloadAllEventsResponse
2438: message CMsgConsumeEventSupportGrantItem
2442: message CMsgConsumeEventSupportGrantItemResponse
2446: message CMsgClientToGCGetFilteredPlayers
2449: message CMsgGCToClientGetFilteredPlayersResponse
2450: message CFilterEntry
2457: enum Result
2469: message CMsgClientToGCRemoveFilteredPlayer
2473: message CMsgGCToClientRemoveFilteredPlayerResponse
2474: enum Result
2482: message CMsgClientToGCPurchaseFilteredPlayerSlot
2486: message CMsgGCToClientPurchaseFilteredPlayerSlotResponse
2487: enum Result
2499: message CMsgClientToGCUpdateFilteredPlayerNote
2504: message CMsgGCToClientUpdateFilteredPlayerNoteResponse
2505: enum Result
2514: message CMsgPartySearchPlayer
2520: message CMsgGCToClientPlayerBeaconState
2524: message CMsgGCToClientPartyBeaconUpdate
2530: message CMsgClientToGCUpdatePartyBeacon
2531: enum Action
2539: message CMsgClientToGCRequestActiveBeaconParties
2542: message CMsgGCToClientRequestActiveBeaconPartiesResponse
2543: enum EResponse
2553: message CMsgClientToGCJoinPartyFromBeacon
2559: message CMsgGCToClientJoinPartyFromBeaconResponse
2560: enum EResponse
2570: message CMsgClientToGCManageFavorites
2571: enum Action
2584: message CMsgGCToClientManageFavoritesResponse
2585: enum EResponse
2599: message CMsgClientToGCGetFavoritePlayers
2604: message CMsgGCToClientGetFavoritePlayersResponse
2605: enum EResponse
2615: message CMsgGCToClientPartySearchInvite
2619: message CMsgClientToGCVerifyFavoritePlayers
2623: message CMsgGCToClientVerifyFavoritePlayersResponse
2624: message Result
2632: message CMsgClientToGCRequestPlayerRecentAccomplishments
2636: message CMsgClientToGCRequestPlayerRecentAccomplishmentsResponse
2637: enum EResponse
2648: message CMsgClientToGCRequestPlayerHeroRecentAccomplishments
2653: message CMsgClientToGCRequestPlayerHeroRecentAccomplishmentsResponse
2654: enum EResponse
2665: message CMsgClientToGCSubmitPlayerMatchSurvey
2671: message CMsgClientToGCSubmitPlayerMatchSurveyResponse
2672: enum EResponse
2685: message CMsgGCToClientVACReminder
2688: message CMsgClientToGCUnderDraftRequest
2693: message CMsgClientToGCUnderDraftResponse
2700: message CMsgClientToGCUnderDraftReroll
2704: message CMsgClientToGCUnderDraftRerollResponse
2710: message CMsgClientToGCUnderDraftBuy
2715: message CMsgGCToClientGuildUnderDraftGoldUpdated
2719: message CMsgClientToGCUnderDraftBuyResponse
2726: message CMsgClientToGCUnderDraftRollBackBench
2730: message CMsgClientToGCUnderDraftRollBackBenchResponse
2736: message CMsgClientToGCUnderDraftSell
2741: message CMsgClientToGCUnderDraftSellResponse
2748: message CMsgClientToGCUnderDraftRedeemReward
2753: message CMsgClientToGCUnderDraftRedeemRewardResponse
2757: message CMsgClientToGCSubmitDraftTriviaMatchAnswer
2763: message CMsgClientToGCSubmitDraftTriviaMatchAnswerResponse
2767: message CMsgDraftTriviaVoteCount
2773: message CMsgClientToGCRequestReporterUpdates
2776: message CMsgClientToGCRequestReporterUpdatesResponse
2777: message ReporterUpdate
2784: enum EResponse
2800: message CMsgClientToGCAcknowledgeReporterUpdates
2804: message CMsgClientToGCRecalibrateMMR
2807: message CMsgClientToGCRecalibrateMMRResponse
2808: enum EResponse
2821: message CMsgDOTAPostGameItemAwardNotification
2827: message CMsgClientToGCGetOWMatchDetails
2830: message CMsgClientToGCGetOWMatchDetailsResponse
2831: message Marker
2836: enum EResponse
2858: message CMsgClientToGCSubmitOWConviction
2865: message CMsgClientToGCSubmitOWConvictionResponse
2866: enum EResponse
2881: message CMsgClientToGCChinaSSAURLRequest
2884: message CMsgClientToGCChinaSSAURLResponse
2888: message CMsgClientToGCChinaSSAAcceptedRequest
2891: message CMsgClientToGCChinaSSAAcceptedResponse
2895: message CMsgGCToClientOverwatchCasesAvailable
2899: message CMsgClientToGCStartWatchingOverwatch
2904: message CMsgClientToGCStopWatchingOverwatch
2909: message CMsgClientToGCOverwatchReplayError
2913: message CMsgClientToGCGetDPCFavorites
2916: message CMsgClientToGCGetDPCFavoritesResponse
2917: message Favorite
2922: enum EResponse
2935: message CMsgClientToGCSetDPCFavoriteState
2941: message CMsgClientToGCSetDPCFavoriteStateResponse
2942: enum EResponse
2957: message CMsgClientToGCSetEventActiveSeasonID
2962: message CMsgClientToGCSetEventActiveSeasonIDResponse
2963: enum EResponse
2976: message CMsgClientToGCPurchaseLabyrinthBlessings
2983: message CMsgClientToGCPurchaseLabyrinthBlessingsResponse
2984: enum EResponse
2996: message CMsgClientToGCGetStickerbookRequest
3000: message CMsgClientToGCGetStickerbookResponse
3001: enum EResponse
3013: message CMsgClientToGCCreateStickerbookPageRequest
3019: message CMsgClientToGCCreateStickerbookPageResponse
3020: enum EResponse
3032: message CMsgClientToGCDeleteStickerbookPageRequest
3038: message CMsgClientToGCDeleteStickerbookPageResponse
3039: enum EResponse
3052: message CMsgClientToGCPlaceStickersRequest
3053: message StickerItem
3061: message CMsgClientToGCPlaceStickersResponse
3062: enum EResponse
3077: message CMsgClientToGCPlaceCollectionStickersRequest
3078: message Slot
3089: message CMsgClientToGCPlaceCollectionStickersResponse
3090: enum EResponse
3107: message CMsgClientToGCOrderStickerbookTeamPageRequest
3111: message CMsgClientToGCOrderStickerbookTeamPageResponse
3112: enum EResponse
3124: message CMsgClientToGCSetHeroSticker
3130: message CMsgClientToGCSetHeroStickerResponse
3131: enum EResponse
3144: message CMsgClientToGCGetHeroStickers
3147: message CMsgClientToGCGetHeroStickersResponse
3148: enum EResponse
3159: message CMsgClientToGCSetFavoritePage
3164: message CMsgClientToGCSetFavoritePageResponse
3165: enum EResponse
3176: message CMsgClientToGCClaimSwag
3182: message CMsgClientToGCClaimSwagResponse
3183: enum EResponse
3199: message CMsgClientToGCCollectorsCacheAvailableDataRequest
3203: message CMsgGCToClientCollectorsCacheAvailableDataResponse
3204: message Vote
3205: enum EVoteType
3217: message CMsgClientToGCUploadMatchClip
3221: message CMsgGCToClientUploadMatchClipResponse
3222: enum EResponse
3232: message CMsgClientToGCMapStatsRequest
3235: message CMsgGCToClientMapStatsResponse
3236: enum EResponse
3246: message CMsgRoadToTIAssignedQuest
3254: message CMsgRoadToTIUserData
3258: message CMsgClientToGCRoadToTIGetQuests
3262: message CMsgClientToGCRoadToTIGetQuestsResponse
3263: enum EResponse
3276: message CMsgClientToGCRoadToTIGetActiveQuest
3280: message CMsgClientToGCRoadToTIGetActiveQuestResponse
3281: enum EResponse
3295: message CMsgGCToClientRoadToTIQuestDataUpdated
3300: message CMsgClientToGCRoadToTIUseItem
3306: message CMsgClientToGCRoadToTIUseItemResponse
3307: enum EResponse
3320: message CMsgClientToGCRoadToTIDevForceQuest
3326: message CMsgLobbyRoadToTIMatchQuestData
3332: message CMsgClientToGCNewBloomGift
3338: message CMsgClientToGCNewBloomGiftResponse
3343: message CMsgClientToGCSetBannedHeroes
3347: message CMsgClientToGCUpdateComicBookStats
3348: message SingleStat
3353: message LanguageStats
3364: message CMsgGCRankedPlayerInfoSubmit
3368: message CMsgGCRankedPlayerInfoSubmitResponse
3369: enum EResult
3377: message CMsgDOTAClaimGatedEvent
3381: message CMsgDOTAClaimGatedEventResponse
3382: enum ResultCode
3395: message CMsgClientToGCGetEventRanking
3400: message CMsgClientToGCGetEventRankingResponse
3409: message CMsgClientToGCGetEventCoupon
3413: message CMsgClientToGCGetEventCouponResponse
3414: message Coupon
3419: enum ResultCode
3434: message CMsgClientToGCConvertEventPoints
3441: message CMsgClientToGCConvertEventPointsResponse
3442: enum ResultCode
3454: message CMsgClientToGCInviteToDemoMode
3459: message CMsgGCToClientInviteToDemoMode
```

</details>

<a id="dota-gcmessages-client-bingo-proto"></a>
### dota_gcmessages_client_bingo.proto

<details>
<summary><code>dota_gcmessages_client_bingo.proto</code> — module: <code>dota_gcmessages_client_bingo_pb2</code>; imports: 9; enums: 10; messages: 25</summary>

- Imports: steammessages.proto, dota_shared_enums.proto, dota_gcmessages_common.proto, dota_gcmessages_webapi.proto, gcsdk_gcmessages.proto, base_gcmessages.proto, econ_gcmessages.proto, dota_gcmessages_client.proto, valveextensions.proto

```text
11: enum EBingoAuditAction
25: message CMsgBingoSquare
31: message CMsgBingoTokens
35: message CMsgBingoCard
39: message CMsgBingoUserData
40: message BingoCardsEntry
45: message BingoTokensEntry
54: message CMsgClientToGCBingoGetUserData
58: message CMsgClientToGCBingoGetUserDataResponse
59: enum EResponse
71: message CMsgBingoIndividualStatData
76: message CMsgBingoStatsData
80: message CMsgClientToGCBingoGetStatsData
85: message CMsgClientToGCBingoGetStatsDataResponse
86: enum EResponse
98: message CMsgGCToClientBingoUserDataUpdated
103: message CMsgClientToGCBingoClaimRow
109: message CMsgClientToGCBingoClaimRowResponse
110: enum EResponse
123: message CMsgClientToGCBingoShuffleCard
128: message CMsgClientToGCBingoShuffleCardResponse
129: enum EResponse
143: message CMsgClientToGCBingoModifySquare
144: enum EModifyAction
155: message CMsgClientToGCBingoModifySquareResponse
156: enum EResponse
173: message CMsgClientToGCBingoDevRerollCard
178: message CMsgClientToGCBingoDevRerollCardResponse
179: enum EResponse
192: message CMsgClientToGCBingoDevAddTokens
198: message CMsgClientToGCBingoDevAddTokensResponse
199: enum EResponse
212: message CMsgClientToGCBingoDevClearInventory
216: message CMsgClientToGCBingoDevClearInventoryResponse
217: enum EResponse
```

</details>

<a id="dota-gcmessages-client-candy-shop-proto"></a>
### dota_gcmessages_client_candy_shop.proto

<details>
<summary><code>dota_gcmessages_client_candy_shop.proto</code> — module: <code>dota_gcmessages_client_candy_shop_pb2</code>; imports: 9; enums: 9; messages: 34</summary>

- Imports: steammessages.proto, dota_shared_enums.proto, dota_gcmessages_common.proto, dota_gcmessages_webapi.proto, gcsdk_gcmessages.proto, base_gcmessages.proto, econ_gcmessages.proto, dota_gcmessages_client.proto, valveextensions.proto

```text
11: enum ECandyShopAuditAction
26: enum ECandyShopRewardType
33: message CMsgCandyShopCandyCount
38: message CMsgCandyShopCandyQuantity
42: message CMsgCandyShopExchangeRecipe
48: message CMsgCandyShopRewardData_Item
52: message CMsgCandyShopRewardData_EventAction
57: message CMsgCandyShopRewardData_EventPoints
62: message CMsgCandyShopReward
72: message CMsgCandyShopUserData
84: message CMsgClientToGCCandyShopGetUserData
88: message CMsgClientToGCCandyShopGetUserDataResponse
89: enum EResponse
103: message CMsgGCToClientCandyShopUserDataUpdated
108: message CMsgClientToGCCandyShopPurchaseReward
113: message CMsgClientToGCCandyShopPurchaseRewardResponse
114: enum EResponse
129: message CMsgClientToGCCandyShopOpenBags
134: message CMsgClientToGCCandyShopOpenBagsResponse
135: enum EResponse
151: message CMsgClientToGCCandyShopDoExchange
156: message CMsgClientToGCCandyShopDoExchangeResponse
157: enum EResponse
173: message CMsgClientToGCCandyShopDoVariableExchange
179: message CMsgClientToGCCandyShopDoVariableExchangeResponse
180: enum EResponse
196: message CMsgClientToGCCandyShopRerollRewards
200: message CMsgClientToGCCandyShopRerollRewardsResponse
201: enum EResponse
216: message CCandyShopDev
217: enum EResponse
229: message CMsgClientToGCCandyShopDevGrantCandy
234: message CMsgClientToGCCandyShopDevGrantCandyResponse
238: message CMsgClientToGCCandyShopDevClearInventory
242: message CMsgClientToGCCandyShopDevClearInventoryResponse
246: message CMsgClientToGCCandyShopDevGrantCandyBags
251: message CMsgClientToGCCandyShopDevGrantCandyBagsResponse
255: message CMsgClientToGCCandyShopDevShuffleExchange
259: message CMsgClientToGCCandyShopDevShuffleExchangeResponse
263: message CMsgClientToGCCandyShopDevGrantRerollCharges
268: message CMsgClientToGCCandyShopDevGrantRerollChargesResponse
272: message CMsgClientToGCCandyShopDevResetShop
276: message CMsgClientToGCCandyShopDevResetShopResponse
```

</details>

<a id="dota-gcmessages-client-chat-proto"></a>
### dota_gcmessages_client_chat.proto

<details>
<summary><code>dota_gcmessages_client_chat.proto</code> — module: <code>dota_gcmessages_client_chat_pb2</code>; imports: 1; enums: 2; messages: 27</summary>

- Imports: dota_shared_enums.proto

```text
3: message CMsgClientToGCPrivateChatInvite
8: message CMsgClientToGCPrivateChatKick
13: message CMsgClientToGCPrivateChatPromote
18: message CMsgClientToGCPrivateChatDemote
23: message CMsgGCToClientPrivateChatResponse
24: enum Result
47: message CMsgDOTAJoinChatChannel
53: message CMsgDOTALeaveChatChannel
57: message CMsgGCChatReportPublicSpam
62: message CMsgDOTAChatModeratorBan
68: message CMsgDOTAChatMessage
69: message DiceRoll
75: message TriviaAnswered
83: message PlayerDraftPick
88: message ChatWheelMessage
139: message CMsgDOTAChatMember
146: message CMsgDOTAJoinChatChannelResponse
147: enum Result
182: message CMsgDOTAOtherJoinedChatChannel
190: message CMsgDOTAOtherLeftChatChannel
196: message CMsgDOTARequestChatChannelList
199: message CMsgDOTARequestChatChannelListResponse
200: message ChatChannel
209: message CMsgDOTAChatGetUserListResponse
210: message Member
221: message CMsgDOTAChatGetMemberCount
226: message CMsgDOTAChatGetMemberCountResponse
232: message CMsgDOTAChatRegionsEnabled
233: message Region
```

</details>

<a id="dota-gcmessages-client-coaching-proto"></a>
### dota_gcmessages_client_coaching.proto

<details>
<summary><code>dota_gcmessages_client_coaching.proto</code> — module: <code>dota_gcmessages_client_coaching_pb2</code>; imports: 2; enums: 17; messages: 35</summary>

- Imports: dota_shared_enums.proto, dota_gcmessages_common_lobby.proto

```text
4: enum ECoachTeammateRating
11: enum EPrivateCoachingSessionState
20: enum EPrivateCoachingSessionMemberFlag
26: enum EPlayerCoachMatchFlag
31: message CMsgPlayerCoachMatch
41: message CMsgPrivateCoachingSessionMember
47: message CMsgPrivateCoachingSession
59: message CMsgPrivateCoachingSessionStatus
64: message CMsgAvailablePrivateCoachingSession
69: message CMsgAvailablePrivateCoachingSessionList
73: message CMsgAvailablePrivateCoachingSessionSummary
77: message CMsgClientToGCRequestPlayerCoachMatches
80: message CMsgClientToGCRequestPlayerCoachMatchesResponse
81: enum EResponse
92: message CMsgClientToGCRequestPlayerCoachMatch
96: message CMsgClientToGCRequestPlayerCoachMatchResponse
97: enum EResponse
108: message CMsgClientToGCSubmitCoachTeammateRating
115: message CMsgClientToGCSubmitCoachTeammateRatingResponse
116: enum EResponse
134: message CMsgGCToClientCoachTeammateRatingsChanged
138: message CMsgClientToGCRequestPrivateCoachingSession
142: message CMsgClientToGCRequestPrivateCoachingSessionResponse
143: enum EResponse
164: message CMsgClientToGCAcceptPrivateCoachingSession
168: message CMsgClientToGCAcceptPrivateCoachingSessionResponse
169: enum EResponse
198: message CMsgClientToGCLeavePrivateCoachingSession
201: message CMsgClientToGCLeavePrivateCoachingSessionResponse
202: enum EResponse
215: message CMsgClientToGCGetCurrentPrivateCoachingSession
218: message CMsgClientToGCGetCurrentPrivateCoachingSessionResponse
219: enum EResponse
231: message CMsgGCToClientPrivateCoachingSessionUpdated
235: message CMsgClientToGCSubmitPrivateCoachingSessionRating
240: message CMsgClientToGCSubmitPrivateCoachingSessionRatingResponse
241: enum EResponse
259: message CMsgClientToGCGetAvailablePrivateCoachingSessions
263: message CMsgClientToGCGetAvailablePrivateCoachingSessionsResponse
264: enum EResponse
276: message CMsgClientToGCGetAvailablePrivateCoachingSessionsSummary
279: message CMsgClientToGCGetAvailablePrivateCoachingSessionsSummaryResponse
280: enum EResponse
292: message CMsgClientToGCJoinPrivateCoachingSessionLobby
295: message CMsgClientToGCJoinPrivateCoachingSessionLobbyResponse
296: enum EResponse
322: message CMsgClientToGCCoachFriend
326: message CMsgClientToGCCoachFriendResponse
327: enum EResponse
353: message CMsgClientToGCRespondToCoachFriendRequest
358: message CMsgClientToGCRespondToCoachFriendRequestResponse
359: enum EResponse
```

</details>

<a id="dota-gcmessages-client-craftworks-proto"></a>
### dota_gcmessages_client_craftworks.proto

<details>
<summary><code>dota_gcmessages_client_craftworks.proto</code> — module: <code>dota_gcmessages_client_craftworks_pb2</code>; imports: 10; enums: 4; messages: 8</summary>

- Imports: steammessages.proto, dota_shared_enums.proto, dota_gcmessages_common.proto, dota_gcmessages_webapi.proto, gcsdk_gcmessages.proto, base_gcmessages.proto, econ_gcmessages.proto, dota_gcmessages_client.proto, valveextensions.proto, dota_gcmessages_common_craftworks.proto

```text
12: message CMsgCraftworksUserData
16: message CMsgClientToGCCraftworksGetUserData
20: message CMsgClientToGCCraftworksGetUserDataResponse
21: enum EResponse
35: message CMsgGCToClientCraftworksUserDataUpdated
40: message CMsgClientToGCCraftworksCraftRecipe
45: message CMsgClientToGCCraftworksCraftRecipeResponse
46: enum EResponse
64: message CMsgClientToGCCraftworksDevModifyComponents
65: enum EOperation
75: message CMsgClientToGCCraftworksDevModifyComponentsResponse
76: enum EResponse
```

</details>

<a id="dota-gcmessages-client-fantasy-proto"></a>
### dota_gcmessages_client_fantasy.proto

<details>
<summary><code>dota_gcmessages_client_fantasy.proto</code> — module: <code>dota_gcmessages_client_fantasy_pb2</code>; imports: 1; enums: 16; messages: 66</summary>

- Imports: dota_shared_enums.proto

```text
3: enum DOTA_2013PassportSelectionIndices
102: message CMsgDOTAPlayerInfo
103: message Results
109: message AuditEntry
118: message ProRegistration
141: message CMsgDOTAPlayerInfoList
146: message CMsgDOTATeamRoster
153: message CMsgDOTADPCProfileInfo
154: message PredictionInfo
159: message FantasyInfo
172: message CMsgDOTALeaderboards
173: message RegionLeaderboard
181: message CMsgDOTAPassportVoteTeamGuess
187: message CMsgDOTAPassportVoteGenericSelection
192: message CMsgDOTAPassportStampedPlayer
197: message CMsgDOTAPassportPlayerCardChallenge
201: message CMsgDOTAPassportVote
208: message CMsgClientToGCGetPlayerCardRosterRequest
213: message CMsgClientToGCGetPlayerCardRosterResponse
214: enum Result
228: message CMsgClientToGCBatchGetPlayerCardRosterRequest
229: message LeagueTimestamp
237: message CMsgClientToGCBatchGetPlayerCardRosterResponse
238: message RosterResponse
249: enum Result
259: message CMsgClientToGCSetPlayerCardRosterRequest
268: message CMsgClientToGCSetPlayerCardRosterResponse
269: enum Result
286: message CMsgDOTAFantasyDPCLeagueStatus
287: message LeagueInfo
296: enum ERosterStatus
306: message CMsgDOTADPCSearchResults
307: message Player
313: message Team
319: message League
324: enum ESearchResultsDesired
336: message CMsgDOTADPCTeamFavoriteRankings
337: message Team
345: message CMsgDotaFantasyCraftingTabletPeriodData
346: message Gem
354: message Tablet
371: message CMsgDotaFantasyCraftingTabletData
372: message TabletPeriodDataEntry
380: message CMsgDotaFantasyCraftingUserData
381: message PeriodScore
386: message PeriodRollTokensEntry
391: message PeriodScoresEntry
401: message CMsgDotaFantasyCraftingDataCache
402: message CacheEntry
411: message CMsgClientToGCFantasyCraftingGetData
416: message CMsgClientToGCFantasyCraftingGetDataResponse
417: enum EResponse
431: message CMsgClientToGCFantasyCraftingPerformOperation
438: message CMsgClientToGCFantasyCraftingPerformOperationResponse
439: message TitleChoice
444: enum EResponse
466: message CMsgGCToClientFantasyCraftingDataUpdated
472: message CMsgClientToGCFantasyCraftingDevModifyTablet
480: message CMsgClientToGCFantasyCraftingDevModifyTabletResponse
481: enum EResponse
495: message CMsgClientToGCFantasyCraftingSelectPlayer
500: message CMsgClientToGCFantasyCraftingSelectPlayerResponse
501: enum EResponse
515: message CMsgClientToGCFantasyCraftingSelectTeam
521: message CMsgClientToGCFantasyCraftingSelectTeamResponse
522: enum EResponse
536: message CMsgClientToGCFantasyCraftingSelectGlobalPrefix
541: message CMsgClientToGCFantasyCraftingSelectGlobalPrefixResponse
542: enum EResponse
556: message CMsgClientToGCFantasyCraftingSelectGlobalSuffix
561: message CMsgClientToGCFantasyCraftingSelectGlobalSuffixResponse
562: enum EResponse
576: message CMsgClientToGCFantasyCraftingGenerateTablets
577: message TeamChoice
587: message CMsgClientToGCFantasyCraftingGenerateTabletsResponse
588: enum EResponse
604: message CMsgClientToGcFantasyCraftingUpgradeTablets
608: message CMsgClientToGcFantasyCraftingUpgradeTabletsResponse
609: enum EResponse
622: message CMsgClientToGCFantasyCraftingRerollOptions
626: message CMsgClientToGCFantasyCraftingRerollOptionsResponse
627: enum EResponse
```

</details>

<a id="dota-gcmessages-client-guild-proto"></a>
### dota_gcmessages_client_guild.proto

<details>
<summary><code>dota_gcmessages_client_guild.proto</code> — module: <code>dota_gcmessages_client_guild_pb2</code>; imports: 1; enums: 26; messages: 61</summary>

- Imports: dota_shared_enums.proto

```text
3: enum EGuildAuditAction
32: enum EGuildChatType
38: message CMsgGuildInfo
58: message CMsgGuildSummary
59: message EventPoints
73: message CMsgGuildRole
80: message CMsgGuildMember
87: message CMsgGuildInvite
93: message CMsgGuildData
101: message CMsgAccountGuildInvite
107: message CMsgAccountGuildMemberships
112: message CMsgGuildPersonaInfo
118: message CMsgAccountGuildsPersonaInfo
122: message CMsgGuildFeedEvent
131: message CMsgClientToGCCreateGuild
136: message CMsgClientToGCCreateGuildResponse
137: enum EResponse
161: message CMsgClientToGCSetGuildInfo
167: message CMsgClientToGCSetGuildInfoResponse
168: enum EResponse
189: message CMsgClientToGCRequestGuildData
193: message CMsgClientToGCRequestGuildDataResponse
194: enum EResponse
208: message CMsgGCToClientGuildDataUpdated
213: message CMsgGCToClientGuildMembersDataUpdated
218: message CMsgClientToGCRequestGuildMembership
221: message CMsgClientToGCRequestGuildMembershipResponse
222: enum EResponse
234: message CMsgGCToClientGuildMembershipUpdated
238: message CMsgClientToGCJoinGuild
242: message CMsgClientToGCJoinGuildResponse
243: enum EResponse
260: message CMsgClientToGCLeaveGuild
264: message CMsgClientToGCLeaveGuildResponse
265: enum EResponse
279: message CMsgClientToGCKickGuildMember
284: message CMsgClientToGCKickGuildMemberResponse
285: enum EResponse
301: message CMsgClientToGCSetGuildMemberRole
307: message CMsgClientToGCSetGuildMemberRoleResponse
308: enum EResponse
325: message CMsgClientToGCInviteToGuild
330: message CMsgClientToGCInviteToGuildResponse
331: enum EResponse
350: message CMsgClientToGCDeclineInviteToGuild
354: message CMsgClientToGCDeclineInviteToGuildResponse
355: enum EResponse
368: message CMsgClientToGCAcceptInviteToGuild
372: message CMsgClientToGCAcceptInviteToGuildResponse
373: enum EResponse
390: message CMsgClientToGCCancelInviteToGuild
395: message CMsgClientToGCCancelInviteToGuildResponse
396: enum EResponse
410: message CMsgClientToGCAddGuildRole
416: message CMsgClientToGCAddGuildRoleResponse
417: enum EResponse
437: message CMsgClientToGCModifyGuildRole
444: message CMsgClientToGCModifyGuildRoleResponse
445: enum EResponse
464: message CMsgClientToGCRemoveGuildRole
469: message CMsgClientToGCRemoveGuildRoleResponse
470: enum EResponse
487: message CMsgClientToGCSetGuildRoleOrder
493: message CMsgClientToGCSetGuildRoleOrderResponse
494: enum EResponse
511: message CMsgClientToGCGuildFeedRequest
516: message CMsgClientToGCRequestGuildFeedResponse
517: enum EResponse
532: message CMsgGCToClientGuildFeedUpdated
536: message CMsgClientToGCAddPlayerToGuildChat
540: message CMsgClientToGCAddPlayerToGuildChatResponse
541: enum EResponse
555: message CMsgFindGuildByTagResponse
556: enum EResponse
571: message CMsgSearchForOpenGuildsResponse
572: message SearchResult
577: enum EResponse
590: message CMsgClientToGCReportGuildContent
591: enum EContentFlags
603: message CMsgClientToGCReportGuildContentResponse
604: enum EResponse
617: message CMsgClientToGCRequestAccountGuildPersonaInfo
621: message CMsgClientToGCRequestAccountGuildPersonaInfoResponse
622: enum EResponse
635: message CMsgClientToGCRequestAccountGuildPersonaInfoBatch
639: message CMsgClientToGCRequestAccountGuildPersonaInfoBatchResponse
640: enum EResponse
```

</details>

<a id="dota-gcmessages-client-guild-events-proto"></a>
### dota_gcmessages_client_guild_events.proto

<details>
<summary><code>dota_gcmessages_client_guild_events.proto</code> — module: <code>dota_gcmessages_client_guild_events_pb2</code>; imports: 1; enums: 7; messages: 22</summary>

- Imports: dota_shared_enums.proto

```text
3: enum EGuildEventAuditAction
15: message CMsgGuildContract
24: message CMsgGuildContractSlot
28: message CMsgAccountGuildEventData
40: message CMsgGuildActiveContracts
45: message CMsgGuildChallenge
53: message CMsgGuildEventMember
58: message CMsgClientToGCRequestAccountGuildEventData
63: message CMsgClientToGCRequestAccountGuildEventDataResponse
64: enum EResponse
81: message CMsgGCToClientAccountGuildEventDataUpdated
89: message CMsgClientToGCRequestActiveGuildContracts
94: message CMsgClientToGCRequestActiveGuildContractsResponse
95: enum EResponse
112: message CMsgGCToClientActiveGuildContractsUpdated
117: message CMsgClientToGCSelectGuildContract
124: message CMsgClientToGCSelectGuildContractResponse
125: enum EResponse
148: message CMsgClientToGCRequestActiveGuildChallenge
153: message CMsgClientToGCRequestActiveGuildChallengeResponse
154: enum EResponse
170: message CMsgGCToClientActiveGuildChallengeUpdated
176: message CMsgClientToGCRequestGuildEventMembers
181: message CMsgClientToGCRequestGuildEventMembersResponse
182: enum EResponse
198: message CMsgGuildLeaderboardCombinedResponse
209: message CMsgClientToGCClaimLeaderboardRewards
214: message CMsgClientToGCClaimLeaderboardRewardsResponse
215: enum EResponse
```

</details>

<a id="dota-gcmessages-client-match-management-proto"></a>
### dota_gcmessages_client_match_management.proto

<details>
<summary><code>dota_gcmessages_client_match_management.proto</code> — module: <code>dota_gcmessages_client_match_management_pb2</code>; imports: 5; enums: 1; messages: 62</summary>

- Imports: steammessages.proto, dota_shared_enums.proto, dota_client_enums.proto, base_gcmessages.proto, dota_gcmessages_common_lobby.proto

```text
7: enum EStartFindingMatchResult
51: message CMsgStartFindingMatch
74: message CMsgStartFindingMatchResult
83: message CMsgStopFindingMatch
87: message CMsgPartyBuilderOptions
95: message CMsgReadyUp
101: message CMsgReadyUpStatus
110: message CMsgAbandonCurrentGame
113: message CMsgLobbyScenarioSave
118: message CMsgPracticeLobbySetDetails
119: message AbilityDraftSpecificDetails
168: message CMsgPracticeLobbyCreate
175: message CMsgPracticeLobbySetTeamSlot
181: message CMsgPracticeLobbySetCoach
185: message CMsgPracticeLobbyJoinBroadcastChannel
192: message CMsgPracticeLobbyCloseBroadcastChannel
196: message CMsgPracticeLobbyToggleBroadcastChannelCameramanStatus
199: message CMsgPracticeLobbyKick
203: message CMsgPracticeLobbyKickFromTeam
207: message CMsgPracticeLobbyLeave
210: message CMsgPracticeLobbyLaunch
214: message CMsgApplyTeamToPracticeLobby
218: message CMsgPracticeLobbyList
224: message CMsgPracticeLobbyListResponseEntry
225: message CLobbyMember
248: message CMsgPracticeLobbyListResponse
252: message CMsgLobbyList
257: message CMsgLobbyListResponse
261: message CMsgPracticeLobbyJoin
269: message CMsgPracticeLobbyJoinResponse
273: message CMsgFriendPracticeLobbyListRequest
277: message CMsgFriendPracticeLobbyListResponse
281: message CMsgJoinableCustomGameModesRequest
285: message CMsgJoinableCustomGameModesResponseEntry
291: message CMsgJoinableCustomGameModesResponse
295: message CMsgJoinableCustomLobbiesRequest
300: message CMsgJoinableCustomLobbiesResponseEntry
319: message CMsgJoinableCustomLobbiesResponse
323: message CMsgQuickJoinCustomLobby
324: message LegacyRegionPing
339: message CMsgQuickJoinCustomLobbyResponse
343: message CMsgBotGameCreate
352: message CMsgDOTAPartyMemberSetCoach
356: message CMsgDOTASetGroupLeader
360: message CMsgDOTACancelGroupInvites
365: message CMsgDOTASetGroupOpenStatus
369: message CMsgDOTAGroupMergeInvite
373: message CMsgDOTAGroupMergeResponse
378: message CMsgDOTAGroupMergeReply
382: message CMsgSpectatorLobbyGameDetails
383: message Team
401: message CMsgSetSpectatorLobbyDetails
408: message CMsgCreateSpectatorLobby
413: message CMsgSpectatorLobbyList
416: message CMsgSpectatorLobbyListResponse
417: message SpectatorLobby
429: message CMsgClientToGCRequestSteamDatagramTicket
433: message CMsgClientToGCRequestSteamDatagramTicketResponse
438: message CMsgGCToClientSteamDatagramTicket
450: message CMsgGCToClientRequestLaneSelection
453: message CMsgGCToClientRequestLaneSelectionResponse
458: message CMsgGCToClientRequestMMInfo
461: message CMsgClientToGCMMInfo
```

</details>

<a id="dota-gcmessages-client-showcase-proto"></a>
### dota_gcmessages_client_showcase.proto

<details>
<summary><code>dota_gcmessages_client_showcase.proto</code> — module: <code>dota_gcmessages_client_showcase_pb2</code>; imports: 9; enums: 20; messages: 60</summary>

- Imports: steammessages.proto, dota_shared_enums.proto, dota_gcmessages_common.proto, dota_gcmessages_webapi.proto, gcsdk_gcmessages.proto, base_gcmessages.proto, econ_gcmessages.proto, dota_gcmessages_client.proto, valveextensions.proto

```text
11: enum EShowcaseHeroPlusFlag
20: enum EShowcaseType
28: enum EShowcaseItemState
37: enum EShowcaseAuditAction
48: enum EShowcaseItemFlag
53: enum EShowcaseItemFlag_Hero
62: message CMsgShowcaseEconItemReference
69: message CMsgHeroPlusInfo
73: message CMsgShowcaseItem_Trophy
74: message Data
82: message CMsgShowcaseItem_EconItem
83: message Data
91: message CMsgShowcaseItem_Hero
92: message Data
112: message CMsgShowcaseItem_HeroIcon
113: message Data
122: message CMsgShowcaseItem_PlayerMatch
123: message Data
134: enum EPlayerOutcome
146: message CMsgShowcaseItem_ChatWheel
147: message Data
154: message CMsgShowcaseItem_Emoticon
155: message Data
162: message CMsgShowcaseItem_SpiderGraph
163: message Data
169: message CMsgShowcaseItem_UserFeed
170: message Data
176: message CMsgShowcaseItem_Stat
177: message Data
185: message CMsgShowcaseBackground
186: message Data
197: message CMsgShowcaseItemData
222: message CMsgShowcaseItemPosition
235: message CMsgShowcaseItem
243: message CMsgShowcase
244: enum EModerationState
254: message CMsgClientToGCShowcaseGetUserData
259: message CMsgClientToGCShowcaseGetUserDataResponse
260: enum EResponse
273: message CMsgClientToGCShowcaseSetUserData
279: message CMsgClientToGCShowcaseSetUserDataResponse
280: enum EResponse
297: message CMsgClientToGCShowcaseSubmitReport
303: message CMsgClientToGCShowcaseSubmitReportResponse
304: enum EResponse
316: message CMsgShowcaseReportsRollupInfo
322: message CMsgShowcaseReportsRollupList
326: message CMsgShowcaseReportsRollupEntry
332: message CMsgShowcaseReportsRollup
337: message CMsgClientToGCShowcaseAdminGetReportsRollupList
340: message CMsgClientToGCShowcaseAdminGetReportsRollupListResponse
341: enum EResponse
354: message CMsgClientToGCShowcaseAdminGetReportsRollup
358: message CMsgClientToGCShowcaseAdminGetReportsRollupResponse
359: enum EResponse
373: message CMsgShowcaseAuditEntry
380: message CMsgShowcaseReport
387: message CMsgShowcaseAdminUserDetails
393: message CMsgClientToGCShowcaseAdminGetUserDetails
397: message CMsgClientToGCShowcaseAdminGetUserDetailsResponse
398: enum EResponse
411: message CMsgClientToGCShowcaseAdminReset
416: message CMsgClientToGCShowcaseAdminResetResponse
417: enum EResponse
429: message CMsgClientToGCShowcaseAdminLockAccount
434: message CMsgClientToGCShowcaseAdminLockAccountResponse
435: enum EResponse
447: message CMsgClientToGCShowcaseAdminConvict
452: message CMsgClientToGCShowcaseAdminConvictResponse
453: enum EResponse
466: message CMsgClientToGCShowcaseAdminExonerate
471: message CMsgClientToGCShowcaseAdminExonerateResponse
472: enum EResponse
485: message CMsgShowcaseModerationInfo
491: message CMsgClientToGCShowcaseModerationGetQueue
496: message CMsgClientToGCShowcaseModerationGetQueueResponse
497: enum EResponse
510: message CMsgClientToGCShowcaseModerationApplyModeration
517: message CMsgClientToGCShowcaseModerationApplyModerationResponse
518: enum EResponse
```

</details>

<a id="dota-gcmessages-client-team-proto"></a>
### dota_gcmessages_client_team.proto

<details>
<summary><code>dota_gcmessages_client_team.proto</code> — module: <code>dota_gcmessages_client_team_pb2</code>; imports: 1; enums: 6; messages: 28</summary>

- Imports: dota_shared_enums.proto

```text
3: enum ETeamInviteResult
20: message CMsgDOTATeamInfo
21: message HeroStats
33: message MemberStats
43: message TeamStats
53: message DPCResult
61: message Member
70: message AuditEntry
105: message CMsgDOTATeamsInfo
110: message CMsgDOTATeamInfoList
114: message CMsgDOTATeamInfoCache
119: message CMsgDOTAMyTeamInfoRequest
122: message CMsgDOTACreateTeam
135: message CMsgDOTACreateTeamResponse
136: enum Result
162: message CMsgDOTAEditTeamDetails
176: message CMsgDOTAEditTeamDetailsResponse
177: enum Result
188: message CMsgDOTATeamInvite_InviterToGC
193: message CMsgDOTATeamInvite_GCImmediateResponseToInviter
199: message CMsgDOTATeamInvite_GCRequestToInvitee
206: message CMsgDOTATeamInvite_InviteeResponseToGC
210: message CMsgDOTATeamInvite_GCResponseToInviter
215: message CMsgDOTATeamInvite_GCResponseToInvitee
220: message CMsgDOTAKickTeamMember
225: message CMsgDOTAKickTeamMemberResponse
226: enum Result
238: message CMsgDOTATransferTeamAdmin
243: message CMsgDOTATransferTeamAdminResponse
244: enum Result
256: message CMsgDOTALeaveTeam
260: message CMsgDOTALeaveTeamResponse
261: enum Result
271: message CMsgDOTABetaParticipation
```

</details>

<a id="dota-gcmessages-client-tournament-proto"></a>
### dota_gcmessages_client_tournament.proto

<details>
<summary><code>dota_gcmessages_client_tournament.proto</code> — module: <code>dota_gcmessages_client_tournament_pb2</code>; imports: 1; enums: 1; messages: 20</summary>

- Imports: dota_client_enums.proto

```text
3: enum ETournamentEvent
18: message CMsgRequestWeekendTourneySchedule
21: message CMsgWeekendTourneySchedule
22: message Division
34: message CMsgWeekendTourneyOpts
45: message CMsgWeekendTourneyLeave
48: message CMsgDOTATournament
49: message Team
62: message Game
71: message Node
91: message CMsgDOTATournamentStateChange
92: message GameChange
97: message TeamChange
112: message CMsgDOTAWeekendTourneyPlayerSkillLevelStats
125: message CMsgDOTAWeekendTourneyPlayerStats
132: message CMsgDOTAWeekendTourneyPlayerStatsRequest
137: message CMsgDOTAWeekendTourneyPlayerHistory
138: message Tournament
154: message CMsgDOTAWeekendTourneyParticipationDetails
155: message Tier
166: message Division
```

</details>

<a id="dota-gcmessages-client-watch-proto"></a>
### dota_gcmessages_client_watch.proto

<details>
<summary><code>dota_gcmessages_client_watch.proto</code> — module: <code>dota_gcmessages_client_watch_pb2</code>; imports: 1; enums: 2; messages: 23</summary>

- Imports: dota_gcmessages_common.proto

```text
3: message CSourceTVGameSmall
4: message Player
46: message CMsgClientToGCFindTopSourceTVGames
55: message CMsgGCToClientFindTopSourceTVGamesResponse
67: message CMsgGCToClientTopWeekendTourneyGames
71: message CMsgClientToGCTopLeagueMatchesRequest
74: message CMsgClientToGCTopFriendMatchesRequest
77: message CMsgClientToGCMatchesMinimalRequest
81: message CMsgClientToGCMatchesMinimalResponse
86: message CMsgGCToClientTopLeagueMatchesResponse
90: message CMsgGCToClientTopFriendMatchesResponse
94: message CMsgSpectateFriendGame
99: message CMsgSpectateFriendGameResponse
100: enum EWatchLiveResult
122: message CDOTAReplayDownloadInfo
123: message Highlight
136: message CMsgWatchGame
144: message CMsgCancelWatchGame
147: message CMsgWatchGameResponse
148: enum WatchGameResult
169: message CMsgPartyLeaderWatchGamePrompt
173: message CDOTABroadcasterInfo
186: message CMsgDOTASeries
187: message TeamInfo
194: message LiveGame
```

</details>

<a id="dota-gcmessages-common-proto"></a>
### dota_gcmessages_common.proto

<details>
<summary><code>dota_gcmessages_common.proto</code> — module: <code>dota_gcmessages_common_pb2</code>; imports: 4; enums: 30; messages: 185</summary>

- Imports: steammessages.proto, gcsdk_gcmessages.proto, dota_shared_enums.proto, networkbasetypes.proto

```text
6: enum ESpecialPingValue
11: enum EDOTAGCSessionNeed
28: enum EDOTAMatchPlayerTimeCustomStat
34: enum DOTA_TournamentEvents
49: enum EBroadcastTimelineEvent
61: enum ECustomGameWhitelistState
67: enum EDOTATriviaQuestionCategory
88: enum EOverwatchConviction
95: enum EHeroRelicRarity
101: enum EStickerbookAuditAction
109: enum EStickerbookPageType
115: enum ENewBloomGiftingResponse
131: message CSODOTAGameAccountClient
132: message RoleHandicap
195: message CSODOTAGameAccountPlus
206: message CSODOTAChatWheel
210: message CMsgLobbyFeaturedGamemodeProgress
211: message AccountProgress
220: message CMsgBattleCupVictory
232: message CMsgLobbyBattleCupVictoryList
236: message CMsgDOTABroadcastNotification
240: message CProtoItemHeroStatue
251: message CMatchPlayerAbilityUpgrade
256: message CMatchPlayerTimedCustomStat
261: message CMatchPlayerTimedStats
302: message CMatchTeamTimedStats
310: message CMatchAdditionalUnitInventory
315: message CMatchPlayerPermanentBuff
321: message CMatchHeroSelectEvent
327: message CMatchClip
339: message CPartySearchClientParty
345: message CMsgDOTAHasItemQuery
350: message CMsgDOTAHasItemResponse
354: message CMsgGCGetPlayerCardItemInfo
360: message CMsgGCGetPlayerCardItemInfoResponse
361: message PlayerCardInfo
370: message CSODOTAMapLocationState
376: message CMsgLeagueAdminList
380: message CMsgDOTAProfileCard
381: message Slot
382: message Trophy
387: message Stat
392: message Item
397: message Hero
403: message Emoticon
407: message Team
420: enum EStatID
446: message CSODOTAPlayerChallenge
466: message CMsgClientToGCRerollPlayerChallenge
472: message CMsgGCRerollPlayerChallengeResponse
473: enum EResult
484: message CMsgGCTopCustomGamesList
489: message CMsgDOTARealtimeGameStats
490: message TeamDetails
504: message ItemDetails
512: message AbilityDetails
520: message HeroToHeroStats
526: message AbilityList
530: message PlayerDetails
583: message BuildingDetails
594: message KillDetails
600: message BroadcasterDetails
604: message PickBanDetails
609: message MatchDetails
633: message GraphData
634: message LocationStats
638: message TeamLocationStats
642: enum eStat
649: enum eLocation
673: message CMsgDOTARealtimeGameStatsTerse
674: message TeamDetails
686: message PlayerDetails
707: message BuildingDetails
718: message PickBanDetails
723: message MatchDetails
740: message GraphData
751: message CMsgDOTABroadcastTimelineEvent
758: message CMsgGCToClientMatchGroupsVersion
762: message CMsgDOTASDOHeroStatsHistory
775: message CMsgPredictionChoice
782: message CMsgInGamePrediction
783: message QueryKeyValues
788: enum ERawValueType_t
793: enum EPredictionType
803: enum EResolutionType_t
815: enum ERandomSelectionGroup_t
838: message CMsgDOTASeasonPredictions
839: message Prediction
840: message Answers
844: enum EPredictionType
855: enum EAnswerType
894: message CMsgAvailablePredictions
895: message MatchPrediction
903: message CMsgLeagueWatchedGames
904: message Series
909: message League
917: message CMsgDOTAMatch
920: message Player
921: message CustomGameData
926: message HeroDamageReceived
932: enum HeroDamageType
1017: message BroadcasterInfo
1022: message BroadcasterChannel
1029: message Coach
1038: message CustomGameData
1043: enum ReplayState
1099: message CMsgPlayerCard
1100: message StatModifier
1109: message CMsgDOTAFantasyPlayerStats
1139: message CMsgDOTAFantasyPlayerMatchStats
1143: message CMsgDOTABotDebugInfo
1144: message Bot
1145: message Mode
1154: message Action
1188: message CMsgSuccessfulHero
1194: message CMsgRecentMatchInfo
1208: message CMsgMatchTips
1209: message SingleTip
1219: message CMsgDOTAMatchMinimal
1220: message Player
1233: message Tourney
1264: message CMsgConsumableUsage
1269: message CMsgMatchConsumableUsage
1270: message PlayerUsage
1278: message CMsgMatchEventActionGrants
1279: message PlayerGrants
1287: message CMsgCustomGameWhitelist
1293: message CMsgCustomGameWhitelistForEdit
1294: message WhitelistEntry
1302: message CMsgPlayerRecentMatchInfo
1313: message CMsgPlayerMatchRecord
1318: message CMsgPlayerRecentMatchOutcomes
1323: message CMsgPlayerRecentCommends
1328: message CMsgPlayerRecentAccomplishments
1339: message CMsgPlayerHeroRecentAccomplishments
1345: message CMsgRecentAccomplishments
1350: message CMsgServerToGCRequestPlayerRecentAccomplishments
1355: message CMsgServerToGCRequestPlayerRecentAccomplishmentsResponse
1356: enum EResponse
1368: message CMsgArcanaVoteMatchVotes
1374: message CMsgGCtoGCAssociatedExploiterAccountInfo
1381: message CMsgGCtoGCAssociatedExploiterAccountInfoResponse
1382: message Account
1395: message CMsgPullTabsData
1396: message Slot
1404: message Jackpot
1415: message CMsgUnderDraftData
1416: message BenchSlot
1422: message ShopSlot
1435: message CMsgPlayerTitleData
1441: message CMsgDOTATriviaQuestion
1450: message CMsgDOTATriviaQuestionAnswersSummary
1455: message CMsgGameDataSpecialValueBonus
1461: message CMsgGameDataSpecialValues
1473: message CMsgGameDataFacetAbilityBonus
1479: message CMsgGameDataAbilityOrItem
1522: message CMsgGameDataAbilityOrItemList
1526: message CMsgGameDataHero
1527: message Facet
1575: message CMsgGameDataAbilities
1579: message CMsgGameDataItems
1583: message CMsgGameDataHeroes
1587: message CMsgGameDataHeroList
1588: message HeroInfo
1600: message CMsgGameDataItemAbilityList
1601: message ItemAbilityInfo
1602: message Recipe
1621: message CMsgLobbyAbilityDraftData
1625: message CSOEconItemDropRateBonus
1636: message CSOEconItemTournamentPassport
1647: message CMsgStickerbookSticker
1660: message CMsgStickerbookPage
1668: message CMsgStickerbookTeamPageOrderSequence
1672: message CMsgStickerbook
1678: message CMsgStickerHero
1685: message CMsgStickerHeroes
1689: message CMsgHeroRoleStats
1695: message CMsgHeroRoleHeroStats
1700: message CMsgHeroRoleRankStats
1705: message CMsgHeroRoleAllRanksStats
1711: message CMsgMapStatsSnapshot
1724: message CMsgGlobalMapStats
1730: message CMsgTrackedStat
1735: message CMsgDOTAClaimEventActionResponse
1736: message MysteryItemRewardData
1741: message LootListRewardData
1745: message ActionListRewardData
1750: message OverworldTokenRewardData
1751: message TokenQuantity
1759: message MonsterHunterMaterialRewardData
1760: message MaterialQuantity
1768: message GrantedRewardData
1776: enum ResultCode
1799: message CMsgClientToGCDotaLabsFeedback
1805: message CMsgClientToGCDotaLabsFeedbackResponse
1806: enum EResponse
1819: message CDotaMsg_PredictionResult
1820: message Prediction
1821: enum EResult
1839: message CDotaMsgStructuredTooltipProperties
1840: message AttributeValueValue
1845: message AttributeValue_Single
1849: message AttributeValue_Variable
1853: message AttributeValue_Delta
1858: message AttributeValue
1866: message Attribute
1873: message AttributeGroupDesc_Basic
1876: message AttributeGroupDesc_Specific
1881: message AttributeGroupDescription
1889: message AttributeGroup
1894: message ContentChunk_AttributeGroup
1898: message TooltipContentChunk
1904: message SummaryDescriptionEmbeddedSubAbility
1910: enum EAbilityTooltipCategory
1917: enum EAttributeType
```

</details>

<a id="dota-gcmessages-common-battle-report-proto"></a>
### dota_gcmessages_common_battle_report.proto

<details>
<summary><code>dota_gcmessages_common_battle_report.proto</code> — module: <code>dota_gcmessages_common_battle_report_pb2</code>; imports: 7; enums: 13; messages: 23</summary>

- Imports: steammessages.proto, dota_shared_enums.proto, dota_gcmessages_common.proto, gcsdk_gcmessages.proto, base_gcmessages.proto, econ_gcmessages.proto, valveextensions.proto

```text
9: enum CMsgBattleReport_HighlightType
79: enum CMsgBattleReport_HighlightCategory
85: enum CMsgBattleReport_Role
94: enum CMsgBattleReport_CompareContext
102: enum CMsgBattleReport_HighlightTier
111: enum CMsgBattleReport_HighlightRarity
117: enum CMsgBattleReport_EOutcome
122: enum CMsgBattleReport_ELaneOutcome
129: message CMsgClientToGCGetBattleReport
135: message CMsgBattleReport_Game
188: message CMsgBattleReport_GameList
192: message CMsgBattleReport
193: message HighlightGeneral
200: message Highlight
217: message CMsgBattleReportInfo
227: message CMsgBattleReportInfoList
231: message CMsgBattleReportHighlights
235: message CMsgBattleReportAggregateStats
236: message CMsgBattleReportStat
241: message CMsgBattleReportAggregate
278: message CMsgBattleReportAggregatedGeneralStats
281: message CMsgClientToGCGetBattleReportResponse
282: enum EResponse
303: message CMsgClientToGCGetBattleReportAggregateStats
304: message CMsgBattleReportAggregateKey
315: message CMsgClientToGCGetBattleReportAggregateStatsResponse
316: enum EResponse
330: message CMsgClientToGCGetBattleReportInfo
334: message CMsgClientToGCGetBattleReportInfoResponse
335: enum EResponse
348: message CMsgClientToGCAcknowledgeBattleReport
354: message CMsgClientToGCAcknowledgeBattleReportResponse
355: enum EResponse
373: message CMsgClientToGCGetBattleReportMatchHistory
379: message CMsgClientToGCGetBattleReportMatchHistoryResponse
380: enum EResponse
```

</details>

<a id="dota-gcmessages-common-bot-script-proto"></a>
### dota_gcmessages_common_bot_script.proto

<details>
<summary><code>dota_gcmessages_common_bot_script.proto</code> — module: <code>dota_gcmessages_common_bot_script_pb2</code>; imports: 1; enums: 2; messages: 18</summary>

- Imports: valveextensions.proto

```text
3: message CMsgBotWorldState
4: message Vector
10: message Player
24: message Ability
45: message DroppedItem
50: message RuneInfo
57: message TeleportInfo
63: message Modifier
73: message LinearProjectile
85: message TrackingProjectile
98: message AvoidanceZone
108: message Courier
114: message EventAbility
122: message EventDamage
131: message EventCourierKilled
138: message EventRoshanKilled
143: message EventTree
151: message Unit
245: enum UnitType
261: enum CourierState
```

</details>

<a id="dota-gcmessages-common-craftworks-proto"></a>
### dota_gcmessages_common_craftworks.proto

<details>
<summary><code>dota_gcmessages_common_craftworks.proto</code> — module: <code>dota_gcmessages_common_craftworks_pb2</code>; imports: 3; enums: 1; messages: 3</summary>

- Imports: steammessages.proto, dota_shared_enums.proto, gcsdk_gcmessages.proto

```text
5: enum ECraftworksAuditAction
12: message CMsgCraftworksComponents
13: message ComponentQuantitiesEntry
21: message CMsgCraftworksQuestReward
```

</details>

<a id="dota-gcmessages-common-fighting-game-proto"></a>
### dota_gcmessages_common_fighting_game.proto

<details>
<summary><code>dota_gcmessages_common_fighting_game.proto</code> — module: <code>dota_gcmessages_common_fighting_game_pb2</code>; imports: 4; enums: 2; messages: 8</summary>

- Imports: steammessages.proto, dota_shared_enums.proto, dota_gcmessages_common.proto, gcsdk_gcmessages.proto

```text
6: message CMsgClientToGCFightingGameChallengeFriend
10: message CMsgClientToGCFightingGameChallengeFriendResponse
11: enum EResponse
24: message CMsgClientToGCFightingGameCancelChallengeFriend
28: message CMsgClientToGCFightingGameAnswerChallenge
33: message CMsgClientToGCFightingGameAnswerChallengeResponse
34: enum EResponse
46: message CMsgGCToClientFightingGameChallenge
50: message CMsgGCToClientFightingGameChallengeCanceled
55: message CMsgGCToClientFightingGameStartMatch
```

</details>

<a id="dota-gcmessages-common-item-battler-proto"></a>
### dota_gcmessages_common_item_battler.proto

<details>
<summary><code>dota_gcmessages_common_item_battler.proto</code> — module: <code>dota_gcmessages_common_item_battler_pb2</code>; imports: 4; enums: 6; messages: 22</summary>

- Imports: steammessages.proto, dota_shared_enums.proto, dota_gcmessages_common.proto, gcsdk_gcmessages.proto

```text
6: enum EItemBattlerAuditAction
10: enum EItemBattlerGameState
24: message CMsgItemBattlerPlayerInfo
32: message CMsgItemBattlerItemModifier
38: message CMsgItemBattlerItem
47: message CMsgItemBattlerItemContainer
55: message CMsgItemBattlerFightEvent
65: message CMsgItemBattlerFightResult
71: message CMsgItemBattlerPlayerData
89: message CMsgItemBattlerEncounterData
95: message CMsgItemBattlerGhostData
96: message ItemsEntry
101: message AbilitiesEntry
112: message CMsgItemBattlerWorldData
113: message ItemsEntry
134: message CMsgItemBattlerGameData
139: message CMsgClientToGCItemBattlerGetUserData
142: message CMsgClientToGCItemBattlerGetUserDataResponse
143: enum EResponse
155: message CMsgItemBattlerItemAction
158: message CMsgClientToGCItemBattlerGameAction
159: enum EAction
178: message CMsgClientToGCItemBattlerGameActionResponse
179: enum EResponse
192: message CMsgClientToGCItemBattlerDevGrantItem
196: message CMsgClientToGCItemBattlerDevGrantItemResponse
197: enum EResponse
208: message CMsgGCToClientItemBattlerUserDataUpdated
```

</details>

<a id="dota-gcmessages-common-league-proto"></a>
### dota_gcmessages_common_league.proto

<details>
<summary><code>dota_gcmessages_common_league.proto</code> — module: <code>dota_gcmessages_common_league_pb2</code>; imports: 1; enums: 2; messages: 37</summary>

- Imports: dota_shared_enums.proto

```text
3: enum ELeagueNodeGroupType
16: enum ELeagueNodeType
24: message CMsgDOTALeagueNode
25: message MatchDetails
31: message VOD
59: message CMsgDOTALeagueNodeGroup
60: message TeamStanding
108: message CMsgDOTALeague
109: message Info
126: message Admin
132: message PrizePoolItem
139: message PrizePool
146: message Stream
155: message SeriesInfo
164: message Player
179: message CMsgDOTALeagueList
183: message CMsgDOTALeagueInfo
195: message CMsgDOTALeagueInfoList
199: message CMsgDOTALeagueLiveGames
200: message LiveGame
219: message CMsgDOTALeagueMessages
220: message Message
229: message CMsgDOTALeaguePrizePool
234: message CMsgDOTALeagueInfoListAdminsRequest
237: message CMsgDOTALeagueAvailableLobbyNodesRequest
241: message CMsgDOTALeagueAvailableLobbyNodes
242: message NodeInfo
253: message CMsgDOTALeagueNodeResults
254: message Result
277: message CMsgDOTADPCLeagueResults
278: message Result
296: message CMsgDOTADPCTeamResults
297: message Result
308: message CMsgDOTADPCSeasonResults
309: message TeamLeagueResult
319: message TeamResult
330: message StandingEntry
339: message Standing
352: message CMsgDOTADPCSeasonSpoilerResults
```

</details>

<a id="dota-gcmessages-common-lobby-proto"></a>
### dota_gcmessages_common_lobby.proto

<details>
<summary><code>dota_gcmessages_common_lobby.proto</code> — module: <code>dota_gcmessages_common_lobby_pb2</code>; imports: 3; enums: 5; messages: 32</summary>

- Imports: steammessages.proto, dota_shared_enums.proto, gcsdk_gcmessages.proto

```text
5: enum ELobbyMemberCoachRequestState
11: enum LobbyDotaTVDelay
19: enum LobbyDotaPauseSetting
25: message CMsgLobbyCoachFriendRequest
31: message CMsgLobbyPlayerPlusSubscriptionData
32: message HeroBadge
40: message CMsgEventActionData
45: message CMsgPeriodicResourceData
51: message CMsgLobbyEventPoints
52: message AccountPoints
73: message CMsgLobbyEventGameData
78: message CSODOTALobbyInvite
79: message LobbyMember
94: message CSODOTALobbyMember
111: message CSODOTAServerLobbyMember
114: message CSODOTAStaticLobbyMember
121: message CSODOTAServerStaticLobbyMember
142: message CLobbyTeamDetails
159: message CLobbyGuildDetails
173: message CLobbyTimedRewardDetails
181: message CLobbyBroadcastChannelInfo
188: message CLobbyGuildChallenge
199: message CDOTALobbyMatchQualityData
206: message CSODOTALobby
207: message CExtraMsg
212: enum State
222: enum LobbyType
330: message CSODOTAServerLobby
336: message CSODOTAStaticLobby
342: message CSODOTAServerStaticLobby
349: message CMsgAdditionalLobbyStartupAccountData
350: message ChatWheelMessageRange
355: message PingWheelMessageRange
366: message CMsgLobbyInitializationComplete
369: message CMsgLobbyPlaytestDetails
373: message CMsgLocalServerGuildData
385: message CMsgLocalServerFakeLobbyData
```

</details>

<a id="dota-gcmessages-common-match-management-proto"></a>
### dota_gcmessages_common_match_management.proto

<details>
<summary><code>dota_gcmessages_common_match_management.proto</code> — module: <code>dota_gcmessages_common_match_management_pb2</code>; imports: 3; enums: 9; messages: 15</summary>

- Imports: steammessages.proto, gcsdk_gcmessages.proto, dota_shared_enums.proto

```text
5: enum ELaneSelection
13: enum ELaneSelectionFlags
26: enum EPartyMatchmakingFlags
31: enum EHighPriorityMMState
43: enum EReadyCheckStatus
49: enum EReadyCheckRequestResult
57: enum EMatchBehaviorScoreVariance
64: message CSODOTAPartyMember
82: message CSODOTAParty
83: enum State
147: message CSODOTAPartyInvite
148: message PartyMember
164: message CMsgLeaverState
173: message CMsgReadyCheckStatus
174: message ReadyMember
185: message CMsgPartyReadyCheckRequest
188: message CMsgPartyReadyCheckResponse
192: message CMsgPartyReadyCheckAcknowledge
196: message CMsgLobbyEventGameDetails
200: message CMsgMatchMatchmakingStats
206: message CMvpData
207: message MvpDatum
208: message MvpAccolade
209: enum MvpAccoladeType
```

</details>

<a id="dota-gcmessages-common-monster-hunter-proto"></a>
### dota_gcmessages_common_monster_hunter.proto

<details>
<summary><code>dota_gcmessages_common_monster_hunter.proto</code> — module: <code>dota_gcmessages_common_monster_hunter_pb2</code>; imports: 4; enums: 16; messages: 36</summary>

- Imports: steammessages.proto, dota_shared_enums.proto, dota_gcmessages_common.proto, gcsdk_gcmessages.proto

```text
6: enum EMonsterHunterAuditAction
25: enum EHeroCodexEntryStatType
38: message CMsgMonsterHunterMaterialCount
43: message CMsgMonsterHunterHeroCodexEntry
48: message CMsgMonsterHunterUserData
49: message HeroCodexEntry
59: message CMsgMonsterHunterMatchRewards
60: message Player
61: message HuntReward
78: message CMsgClientToGCMonsterHunterGetUserData
81: message CMsgClientToGCMonsterHunterGetUserDataResponse
82: enum EResponse
94: message CMsgGCToClientMonsterHunterUserDataUpdated
98: message CMsgClientToGCMonsterHunterClaimReward
105: message CMsgClientToGCMonsterHunterClaimRewardResponse
106: enum EResponse
124: message CMsgMonsterHunterItemSet
129: message CMsgClientToGCMonsterHunterClaimSetReward
133: message CMsgClientToGCMonsterHunterClaimSetRewardResponse
134: enum EResponse
149: message CMsgClientToGCMonsterHunterTradeMaterials
155: message CMsgClientToGCMonsterHunterTradeMaterialsResponse
156: enum EResponse
173: message CMsgClientToGCMonsterHunterGiftMaterials
179: message CMsgClientToGCMonsterHunterGiftMaterialsResponse
180: enum EResponse
196: message CMsgClientToGCMonsterHunterRequestMaterialsNeededByFriend
200: message CMsgClientToGCMonsterHunterRequestMaterialsNeededByFriendResponse
201: enum EResponse
216: message CMsgClientToGCMonsterHunterDevResetAll
220: message CMsgClientToGCMonsterHunterDevResetAllResponse
221: enum EResponse
233: message CMsgClientToGCMonsterHunterDevGrantMaterials
237: message CMsgClientToGCMonsterHunterDevGrantMaterialsResponse
238: enum EResponse
250: message CMsgClientToGCMonsterHunterDevClearInventory
253: message CMsgClientToGCMonsterHunterDevClearInventoryResponse
254: enum EResponse
266: message CMsgClientToGCMonsterHunterDevClaimInvestigationRewards
271: message CMsgClientToGCMonsterHunterDevClaimInvestigationRewardsResponse
272: enum EResponse
284: message CMsgClientToGCMonsterHunterClaimCodexReward
289: message CMsgClientToGCMonsterHunterClaimCodexRewardResponse
290: enum EResponse
304: message CMsgDevModifyCodexAction
305: enum EAction
315: message CMsgClientToGCMonsterHunterDevModifyHeroCodex
319: message CMsgClientToGCMonsterHunterDevModifyHeroCodexResponse
320: enum EResponse
332: message CMsgClientToGCMonsterHunterFeedback
337: message CMsgClientToGCMonsterHunterFeedbackResponse
338: enum EResponse
```

</details>

<a id="dota-gcmessages-common-overworld-proto"></a>
### dota_gcmessages_common_overworld.proto

<details>
<summary><code>dota_gcmessages_common_overworld.proto</code> — module: <code>dota_gcmessages_common_overworld_pb2</code>; imports: 5; enums: 26; messages: 68</summary>

- Imports: steammessages.proto, dota_shared_enums.proto, dota_gcmessages_common.proto, dota_gcmessages_common_survivors.proto, gcsdk_gcmessages.proto

```text
7: enum EOverworldNodeState
13: enum EOverworldPathState
19: enum EOverworldAuditAction
47: enum EOverworldMinigameAction
57: message CMsgOverworldTokenCount
62: message CMsgOverworldTokenQuantity
66: message CMsgOverworldEncounterTokenTreasureData
67: message RewardOption
76: message CMsgOverworldEncounterTokenQuestData
77: message Quest
86: message CMsgOverworldHeroList
90: message CMsgOverworldEncounterChooseHeroData
95: message CMsgOverworldEncounterProgressData
102: message CMsgOverworldEncounterData
106: message CMsgOverworldNode
112: message CMsgOverworldPath
118: message CMsgOverworldMinigameCustomData
124: message CMsgOverworldMinigameUserData
130: message CMsgOverworldFortune
131: message CMsgFortuneCount
144: message CMsgLobbyOverworldFortuneList
149: message CMsgOverworldUserData
150: message MinigameDataEntry
165: message CMsgOverworldMatchRewards
166: message Player
175: message CMsgClientToGCOverworldGetUserData
179: message CMsgClientToGCOverworldGetUserDataResponse
180: enum EResponse
193: message CMsgGCToClientOverworldUserDataUpdated
198: message CMsgClientToGCOverworldCompletePath
205: message CMsgClientToGCOverworldCompletePathResponse
206: enum EResponse
225: message CMsgOverworldEncounterPitFighterRewardData
230: message CMsgClientToGCOverworldClaimEncounterReward
241: message CMsgClientToGCOverworldClaimEncounterRewardResponse
242: enum EResponse
267: message CMsgClientToGCOverworldVisitEncounter
272: message CMsgClientToGCOverworldVisitEncounterResponse
273: enum EResponse
289: message CMsgClientToGCOverworldMoveToNode
294: message CMsgClientToGCOverworldMoveToNodeResponse
295: enum EResponse
309: message CMsgClientToGCOverworldTradeTokens
317: message CMsgClientToGCOverworldTradeTokensResponse
318: enum EResponse
338: message CMsgClientToGCOverworldGiftTokens
345: message CMsgClientToGCOverworldGiftTokensResponse
346: enum EResponse
364: message CMsgClientToGCOverworldRequestTokensNeededByFriend
369: message CMsgClientToGCOverworldRequestTokensNeededByFriendResponse
370: enum EResponse
387: message CMsgClientToGCOverworldDevResetAll
391: message CMsgClientToGCOverworldDevResetAllResponse
392: enum EResponse
405: message CMsgClientToGCOverworldDevResetNode
410: message CMsgClientToGCOverworldDevResetNodeResponse
411: enum EResponse
425: message CMsgClientToGCOverworldDevGrantTokens
430: message CMsgClientToGCOverworldDevGrantTokensResponse
431: enum EResponse
444: message CMsgClientToGCOverworldDevClearInventory
448: message CMsgClientToGCOverworldDevClearInventoryResponse
449: enum EResponse
462: message CMsgClientToGCOverworldDevSetFortune
467: message CMsgClientToGCOverworldDevSetFortuneResponse
468: enum EResponse
481: message CMsgClientToGCOverworldDevClearFortune
486: message CMsgClientToGCOverworldDevClearFortuneResponse
487: enum EResponse
500: message CMsgClientToGCOverworldDevGrantFortuneTellerCoin
504: message CMsgClientToGCOverworldDevGrantFortuneTellerCoinResponse
505: enum EResponse
518: message CMsgClientToGCOverworldRequestFortune
522: message CMsgClientToGCOverworldRequestFortuneResponse
523: enum EResponse
539: message CMsgClientToGCOverworldClaimFortuneReward
543: message CMsgClientToGCOverworldClaimFortuneRewardResponse
544: enum EResponse
560: message CMsgClientToGCOverworldClaimFortunePermanentReward
565: message CMsgClientToGCOverworldClaimFortunePermanentRewardResponse
566: enum EResponse
581: message CMsgClientToGCOverworldFeedback
587: message CMsgClientToGCOverworldFeedbackResponse
588: enum EResponse
601: message CMsgClientToGCOverworldGetDynamicImage
607: message CMsgClientToGCOverworldGetDynamicImageResponse
608: message Image
615: enum EDynamicImageFormat
625: message CMsgClientToGCOverworldMinigameAction
634: message CMsgClientToGCOverworldMinigameActionResponse
635: enum EResponse
653: message CMsgClientToGCOverworldClaimFortuneTellerStoryNode
658: message CMsgClientToGCOverworldClaimFortuneTellerStoryNodeResponse
659: enum EResponse
```

</details>

<a id="dota-gcmessages-common-survivors-proto"></a>
### dota_gcmessages_common_survivors.proto

<details>
<summary><code>dota_gcmessages_common_survivors.proto</code> — module: <code>dota_gcmessages_common_survivors_pb2</code>; imports: 4; enums: 1; messages: 5</summary>

- Imports: steammessages.proto, dota_shared_enums.proto, dota_gcmessages_common.proto, gcsdk_gcmessages.proto

```text
6: message CMsgSurvivorsUserData
7: message AttributeLevelsEntry
16: message CMsgClientToGCSurvivorsPowerUpTelemetryData
26: message CMsgClientToGCSurvivorsGameTelemetryData
36: message CMsgClientToGCSurvivorsGameTelemetryDataResponse
37: enum EResponse
```

</details>

<a id="dota-gcmessages-msgid-proto"></a>
### dota_gcmessages_msgid.proto

<details>
<summary><code>dota_gcmessages_msgid.proto</code> — module: <code>dota_gcmessages_msgid_pb2</code>; imports: 0; enums: 1; messages: 0</summary>

- Imports: *(none)*

```text
1: enum EDOTAGCMsg
```

</details>

<a id="dota-gcmessages-server-proto"></a>
### dota_gcmessages_server.proto

<details>
<summary><code>dota_gcmessages_server.proto</code> — module: <code>dota_gcmessages_server_pb2</code>; imports: 14; enums: 6; messages: 170</summary>

- Imports: steammessages.proto, valveextensions.proto, dota_shared_enums.proto, dota_gcmessages_common.proto, econ_gcmessages.proto, base_gcmessages.proto, network_connection.proto, dota_gcmessages_common_lobby.proto, dota_gcmessages_common_match_management.proto, dota_gcmessages_common_overworld.proto, dota_gcmessages_common_craftworks.proto, dota_gcmessages_common_monster_hunter.proto, gcsdk_gcmessages.proto, steammessages_steamlearn.steamworkssdk.proto

```text
16: enum EPoorNetworkConditionsType
23: message CMsgPoorNetworkConditions
24: message Player
35: message CMsgGameserverCrash
50: message CMsgConnectedPlayers
51: message Player
58: message PlayerDraft
64: enum SendReason
92: message CMsgGameServerInfo
93: enum ServerType
102: enum CustomGames
137: message CMsgLeaverDetected
146: message CMsgLeaverDetectedResponse
150: message CMsgDOTAFantasyFinalPlayerStats
154: message CMsgDOTAFantasyLivePlayerStats
158: message CMsgServerToGCRealtimeStats
162: message CMsgGCToServerRealtimeStatsStartStop
166: message CMsgGCToServerUpdateSteamBroadcasting
170: message CMsgSignOutGameplayStats
171: message CPlayer
178: message CTeam
188: message CMsgGameMatchSignOut
189: message CTeam
190: message CPlayer
191: message CCustomGameData
196: message HeroDamageReceived
202: enum HeroDamageType
290: message CAdditionalSignoutMsg
295: message CSocialFeedMatchEvent
303: message CCustomGameData
307: message EventGameLeaderboardEntry
348: message CMsgSignOutDraftInfo
354: message CMsgSignOutBotInfo
361: message CMsgSignOutTextMuteInfo
362: message TextMuteMessage
371: message CMsgSignOutPlayerStats
405: message CMsgSignOutCommunicationSummary
406: message PlayerCommunication
407: message PingDetail
435: message CMsgGameMatchSignoutResponse
436: message PlayerMetadata
466: message CMsgGameMatchSignOutPermissionRequest
473: message CMsgGameMatchSignOutPermissionResponse
479: message CMsgGameMatchSignOutEventGameData
487: message CMsgGameMatchSignOutPerfData
520: message CMsgGameMatchSignOutBanData
525: message CMsgDOTALiveScoreboardUpdate
526: message Team
527: message Player
528: message HeroAbility
534: enum DOTAUltimateState
589: message CMsgServerToGCRequestBatchPlayerResources
595: message CMsgServerToGCRequestBatchPlayerResourcesResponse
596: message Result
616: message CMsgDOTAPlayerFailedToConnect
621: message CMsgGCToRelayConnect
631: message CMsgGCGCToLANServerRelayConnect
635: message CMsgGCBanStatusRequest
639: message CMsgGCBanStatusResponse
646: message CMsgTournamentItemEvent
661: message CMsgTournamentItemEventResponse
666: message CMsgTeamFanfare
670: message CMsgResponseTeamFanfare
675: message CMsgDOTAAwardEventPoints
676: message AwardPoints
692: message CMsgGCToServerPingRequest
697: message CMsgGCToServerPingResponse
703: message CMsgServerToGCMatchConnectionStats
704: message Player
720: message CMsgServerGCUpdateSpectatorCount
724: message CSerializedCombatLog
725: message Dictionary
726: message DictString
739: message CMsgServerToGCVictoryPredictions
740: message PredictionItem
745: message Record
754: message CMsgServerToGCRequestStatus
757: message CMsgServerToGCRequestStatus_Response
761: message CMsgGCToServerEvaluateToxicChat
766: message CMsgServerToGCEvaluateToxicChat
774: message CMsgServerToGCEvaluateToxicChatResponse
782: message CMsgSignOutAssassinMiniGameInfo
793: message CMsgServerToGCKillSummaries
794: message KillSummary
804: message CMsgServerToGCLockCharmTrading
809: message CMsgSignOutUpdatePlayerChallenge
810: message Challenge
825: message CMsgServerToGCRerollPlayerChallenge
830: message CMsgSpendWager
831: message Player
844: message CMsgSignOutXPCoins
845: message Player
860: message CMsgSignOutBounties
861: message Bounty
873: message CMsgSignOutCommunityGoalProgress
874: message EventGoalIncrement
883: message CMsgServerToGCCloseCompendiumInGamePredictionVoting
889: message CMsgServerToGCCloseCompendiumInGamePredictionVotingResponse
893: message CMsgServerToGCCompendiumInGamePredictionResults
894: message PredictionResult
906: message CMsgServerToGCCompendiumChosenInGamePredictions
907: message Prediction
916: message CMsgGCToGCCompendiumInGamePredictionResults
920: message CMsgServerToGCCavernCrawlIsHeroActive
928: message CMsgServerToGCPlayerChallengeHistory
929: message PlayerChallenge
947: message CMsgServerToGCCavernCrawlIsHeroActiveResponse
948: message MapResults
960: message CMsgNeutralItemStats
961: message NeutralItem
973: message CMsgGCToServerLobbyHeroBanRates
974: message HeroBanEntry
983: message CMsgSignOutGuildContractProgress
984: message CompletedGuildEventContracts
990: message PlayerContract
998: message CMsgSignOutGuildChallengeProgress
999: message ChallengeProgress
1012: message CMsgSignOutMVPStats
1013: message Player
1014: message KillEaterEvent
1053: message CMsgServerToGCGetGuildContracts
1057: message CMsgServerToGCGetGuildContractsResponse
1058: message ContractDetails
1066: message Player
1076: message CMsgMatchDiretideCandy
1077: message CandyDetails
1082: message PlayerCandy
1093: message CMsgGCToServerCheerData
1094: message CheerTypeCount
1102: message CMsgCheerConfig
1123: message CMsgGCToServerCheerConfig
1127: message CMsgServerToGCGetCheerConfig
1131: message CMsgServerToGCGetCheerConfigResponse
1135: message CMsgGCToServerCheerScalesOverride
1139: message CMsgGCToServerGetCheerState
1142: message CMsgCheerTypeState
1149: message CMsgCheerState
1155: message CMsgServerToGCReportCheerState
1160: message CMsgServerToGCGetStickerHeroes
1164: message CMsgServerToGCGetStickerHeroesResponse
1165: message Player
1173: message CMsgSteamLearnMatchInfo
1181: message CMsgSteamLearnMatchInfoPlayer
1190: message CMsgSteamLearnMatchInfoTeam
1191: message Player
1204: message CMsgSteamLearnMatchHeroesV3
1215: message CMsgSteamLearnMatchHeroesV4
1224: message CMsgSteamLearnMatchHeroV6
1234: message CMsgSteamLearnMatchHeroV8
1242: message CMsgSteamLearnPlayerTimedStats
1243: message StatBucket
1261: message CMsgSteamLearnMatchStateV5
1262: message PlayerState
1275: message TeamState
1293: message CMsgSteamLearnItemPurchaseV7
1298: message CMsgSteamLearnPreGameItemPurchases
1304: message CMsgSteamLearnPreGameItemPurchase
1309: message CMsgSteamLearnNeutralItemPurchaseV4
1317: message CMsgSteamLearnNeutralItemPurchaseV6
1325: message CMsgSteamLearnAbilitySkill
1332: message CMsgSteamLearnWardPlacement
1333: message Location
1343: message CMsgSteamLearnPlayerMatchState
1358: message CMsgSignOutMuertaMinigame
1362: message CMsgSignOutMapStats
1363: message Player
1372: message CMsgServerToGCNewBloomGift
1378: message CMsgServerToGCNewBloomGiftResponse
1383: message CMsgSignOutOverworld
1384: message Player
1395: message CMsgSignOutCraftworks
1396: message Player
1405: message CMsgSignOutMonsterHunter
1406: message Player
1416: message CMsgServerToGCWarningLowServerFramerate
1424: message CMsgServerToGCWarningInvalidBotAbilityUsage
```

</details>

<a id="dota-gcmessages-webapi-proto"></a>
### dota_gcmessages_webapi.proto

<details>
<summary><code>dota_gcmessages_webapi.proto</code> — module: <code>dota_gcmessages_webapi_pb2</code>; imports: 5; enums: 15; messages: 39</summary>

- Imports: steammessages.proto, gcsdk_gcmessages.proto, dota_shared_enums.proto, dota_gcmessages_common.proto, dota_match_metadata.proto

```text
7: enum ETeamFanContentStatus
13: enum ETeamFanContentAssetType
27: enum ETeamFanContentAssetStatus
33: enum ETalentContentStatus
41: enum ETalentContentAssetType
47: enum ETalentContentAssetStatus
53: message CMsgArcanaVotes
54: message Match
68: enum VotingState
84: message CMsgDOTADPCFeed
85: message Element
101: enum EFeedElementType
121: message CMsgDOTADPCUserInfo
125: message CMsgDraftTrivia
126: message DraftTriviaHeroInfo
131: message DraftTriviaMatchInfo
136: message PreviousResult
155: message CMsgTeamFanContentAssetStatus
162: message CMsgTeamFanContentAssetStatusResponse
163: enum EResult
171: message CMsgTeamFanContentStatus
172: message TeamStatus
196: message CMsgTeamFanContentAutographStatus
197: message AutographStatus
204: message TeamStatus
214: message CMsgTalentContentAssetStatus
221: message CMsgTalentContentStatus
222: message SubmitRevision
228: message TalentDetails
242: enum EWorkshopItemStatus
254: message CMsgSetTalentContentResponse
255: enum EResult
264: message CMsgDPCEvent
265: message PhaseInfo
270: message League
277: enum ELeagueEvent
304: enum ELeagueEventPhase
319: enum ELeagueEventType
329: enum ETour
353: message CMsgDPCEventList
357: message CMsgDOTAFantasyCardLineup
358: message CardBonus
363: message Card
375: message League
381: message Period
391: message CMsgDOTAFantasyCardList
392: message CardBonus
397: message Card
410: message CMsgChatToxicityToxicPlayerMatchesReport
411: message IndividualRow
423: message CMsgChatToxicityReport
432: message CMsgGetTeamAuditInformation
433: message Action
448: message CMsgDOTADPCMatch
```

</details>

<a id="dota-hud-types-proto"></a>
### dota_hud_types.proto

<details>
<summary><code>dota_hud_types.proto</code> — module: <code>dota_hud_types_pb2</code>; imports: 1; enums: 1; messages: 0</summary>

- Imports: google/protobuf/descriptor.proto

```text
7: enum EHeroSelectionText
```

</details>

<a id="dota-match-metadata-proto"></a>
### dota_match_metadata.proto

<details>
<summary><code>dota_match_metadata.proto</code> — module: <code>dota_match_metadata_pb2</code>; imports: 10; enums: 2; messages: 46</summary>

- Imports: base_gcmessages.proto, dota_gcmessages_common_match_management.proto, dota_gcmessages_common_lobby.proto, dota_gcmessages_common_overworld.proto, dota_gcmessages_common_craftworks.proto, dota_gcmessages_common_monster_hunter.proto, dota_gcmessages_common.proto, dota_shared_enums.proto, gcsdk_gcmessages.proto, networkbasetypes.proto

```text
12: enum EPlayerInventorySnapshotFlags
17: message CDOTAMatchMetadataFile
26: message CDOTAMatchMetadata
27: message EconItem
35: message Team
36: message PlayerKill
41: message ItemPurchase
46: message InventorySnapshot
61: message AutoStyleCriteria
66: message StrangeGemProgress
76: message VictoryPrediction
83: message SubChallenge
90: message CavernChallengeResult
95: message ActionGrant
102: message CandyGrant
107: message PeriodicResourceData
113: message EventData
142: message FeaturedGamemodeProgress
148: message KillInfo
149: enum KillType
164: message Player
165: message ContractProgress
175: message OverworldRewards
180: message NeutralItem
259: message GuildChallengeProgress
260: message IndividualProgress
275: message Tip
296: message CDOTAMatchPrivateMetadata
297: message StringName
302: message Team
303: message Player
304: message CombatSegment
305: message DamageByAbility
306: message ByHeroTarget
316: message HealingByAbility
317: message ByHeroTarget
332: message BuffRecord
333: message ByHeroTarget
345: message GoldReceived
357: message XPReceived
384: message Building
396: message ContributionsCombatSegment
397: message DamageContributionRecord
408: message DamageMitigationRecord
419: message HealingContributionRecord
430: message HealingReductionRecord
441: message KillingBlow
447: message Dispel
```

</details>

<a id="dota-modifiers-proto"></a>
### dota_modifiers.proto

<details>
<summary><code>dota_modifiers.proto</code> — module: <code>dota_modifiers_pb2</code>; imports: 1; enums: 1; messages: 2</summary>

- Imports: networkbasetypes.proto

```text
3: enum DOTA_MODIFIER_ENTRY_TYPE
8: message CDOTAModifierBuffTableEntry
55: message CDOTALuaModifierEntry
```

</details>

<a id="dota-scenariomessages-proto"></a>
### dota_scenariomessages.proto

<details>
<summary><code>dota_scenariomessages.proto</code> — module: <code>dota_scenariomessages_pb2</code>; imports: 1; enums: 0; messages: 23</summary>

- Imports: dota_shared_enums.proto

```text
3: message CScenario_Position
8: message CScenarioGame_RoshanSpawner
15: message CScenarioEnt_Courier
21: message CScenarioEnt_NPC
31: message CScenarioEnt_SpiritBear
36: message CScenarioEnt_DroppedItem
40: message CMsgDotaScenario
41: message EntityRef
49: message Game
57: message TeamNeutralItem
63: message Team
73: message HeroHeroInt
78: message HeroHeroFloat
83: message DamageStatsByType
91: message HeroAbility
97: message HeroNeutralChoice
103: message HeroNeutralTier
110: message Hero
183: message Stock
192: message Building
200: message Entity
207: message Item
220: message Modifier
```

</details>

<a id="dota-shared-enums-proto"></a>
### dota_shared_enums.proto

<details>
<summary><code>dota_shared_enums.proto</code> — module: <code>dota_shared_enums_pb2</code>; imports: 0; enums: 53; messages: 14</summary>

- Imports: *(none)*

```text
3: enum DOTA_GameMode
33: enum DOTA_GameState
50: enum DOTA_GC_TEAM
68: enum ERankType
82: enum DOTALeaverStatus_t
95: enum DOTAConnectionState_t
105: enum Fantasy_Roles
113: enum Fantasy_Scoring
136: enum Fantasy_Team_Slots
144: enum Fantasy_Selection_Mode
157: enum Fantasy_Gem_Type
163: enum DOTAChatChannelType_t
191: enum EChatSpecialPrivileges
197: enum DOTACommType_t
216: enum DOTACommLevel_t
227: enum DOTABehaviorLevel_t
235: enum EProfileCardSlotType
245: enum EMatchGroupServerStatus
251: enum DOTA_CM_PICK
257: enum DOTALowPriorityBanType
264: enum DOTALobbyReadyState
271: enum DOTAJoinLobbyResult
289: enum DOTASelectionPriorityRules
294: enum DOTASelectionPriorityChoice
302: enum DOTAMatchVote
308: enum DOTALobbyVisibility
314: enum EDOTAPlayerMMRType
320: enum EDOTAMMRBoostType
326: enum MatchType
336: enum DOTABotDifficulty
349: enum DOTA_BOT_MODE
384: enum MatchLanguages
395: enum ETourneyQueueDeadlineState
405: enum EMatchOutcome
427: enum ELaneType
436: enum EBadgeType
471: enum ELeagueStatus
481: enum ELeagueRegion
491: enum ELeagueTier
504: enum ELeagueTierCategory
510: enum ELeagueDivision
516: enum ELeagueBroadcastProvider
524: enum ELeaguePhase
531: enum ELeagueAuditAction
576: enum DOTA_COMBATLOG_TYPES
625: enum EDPCFavoriteType
632: enum EDPCPushNotification
646: enum EEventActionScoreMode
651: enum EPlayerChallengeHistoryType
660: enum EOverwatchReportReason
669: enum ECandyShopUpgrade
676: enum EItemSuggestPreference
682: enum ETimerAlertType
690: message CDOTAClientHardwareSpecs
700: message CDOTASaveGame
701: message Player
707: message SaveInstance
708: message PlayerPositions
727: message CMsgDOTACombatLogEntry
812: message CMsgPendingEventAward
821: message CMsgMonsterHunterMaterialQuantity
822: message MaterialCountsEntry
830: message CMsgMonsterHunterInvestigation
838: message CMsgMonsterHunterInvestigationGameState
839: message HuntedBy
850: message CMsgMonsterHunterCodexUpdateData
851: message KillInfo
```

</details>

<a id="dota-usercmd-proto"></a>
### dota_usercmd.proto

<details>
<summary><code>dota_usercmd.proto</code> — module: <code>dota_usercmd_pb2</code>; imports: 3; enums: 0; messages: 1</summary>

- Imports: valveextensions.proto, networkbasetypes.proto, usercmd.proto

```text
5: message CDota2UserCmdPB
```

</details>

<a id="dota-usermessages-proto"></a>
### dota_usermessages.proto

<details>
<summary><code>dota_usermessages.proto</code> — module: <code>dota_usermessages_pb2</code>; imports: 3; enums: 20; messages: 191</summary>

- Imports: networkbasetypes.proto, dota_shared_enums.proto, dota_commonmessages.proto

```text
5: enum EDotaUserMessages
177: enum DOTA_CHAT_MESSAGE
298: enum DOTA_NO_BATTLE_POINTS_REASONS
305: enum DOTA_CHAT_INFORMATIONAL
313: enum DOTA_ABILITY_PING_TYPE
332: enum DOTA_REPLAY_STATE_EVENT
341: enum EDotaEntityMessages
351: enum DOTA_OVERHEAD_ALERT
380: enum DOTA_ROSHAN_PHASE
386: enum DOTA_POSITION_CATEGORY
405: enum DOTA_ABILITY_TARGET_TYPE
414: enum EHeroStatType
439: enum EPlayerVoiceListenState
462: enum EProjectionEvent
467: message CDOTAUserMsg_AIDebugLine
471: message CDOTAUserMsg_Ping
476: message CDOTAUserMsg_SwapVerify
480: message CDOTAUserMsg_ChatEvent
494: message CDOTAUserMsg_BotChat
501: message CDOTAUserMsg_CombatHeroPositions
508: message CDOTAUserMsg_CombatLogBulkData
518: message CDOTAUserMsg_ProjectileParticleCPData
523: message CDOTAUserMsg_UpdateLinearProjectileCPData
529: message CDOTAUserMsg_MiniKillCamInfo
530: message Attacker
531: message Ability
545: message CDOTAUserMsg_GlobalLightColor
550: message CDOTAUserMsg_GlobalLightDirection
555: message CDOTAUserMsg_LocationPing
560: message CDOTAUserMsg_PingConfirmation
567: message CDOTAUserMsg_ItemAlert
572: message CDOTAUserMsg_EnemyItemAlert
583: message CDOTAUserMsg_ModifierAlert
592: message CDOTAUserMsg_HPManaAlert
598: message CDOTAUserMsg_NeutralCampAlert
608: message CDOTAUserMsg_GlyphAlert
613: message CDOTAUserMsg_RadarAlert
618: message CDOTAUserMsg_RoshanTimer
623: message CDOTAUserMsg_TormentorTimer
628: message CDOTAUserMsg_WillPurchaseAlert
635: message CDOTAUserMsg_EmptyTeleportAlert
641: message CDOTAUserMsg_MarsArenaOfBloodAttack
647: message CDOTAUserMsg_BuyBackStateAlert
651: message CDOTAUserMsg_QuickBuyAlert
659: message CDOTAUserMsg_CourierKilledAlert
660: message LostItem
674: message CDOTAUserMsg_MinimapEvent
683: message CDOTAUserMsg_MapLine
688: message CDOTAUserMsg_MinimapDebugPoint
696: message CDOTAUserMsg_CreateLinearProjectile
711: message CDOTAUserMsg_DestroyLinearProjectile
715: message CDOTAUserMsg_DodgeTrackingProjectiles
720: message CDOTAUserMsg_SpectatorPlayerClick
726: message CDOTAUserMsg_SpectatorPlayerUnitOrders
740: message CDOTAUserMsg_NevermoreRequiem
747: message CDOTAUserMsg_InvalidCommand
752: message CDOTAUserMsg_HudError
757: message CDOTAUserMsg_SharedCooldown
764: message CDOTAUserMsg_SetNextAutobuyItem
768: message CDOTAUserMsg_HalloweenDrops
774: message CDOTAUserMsg_CourierLeftFountainAlert
778: message CDOTAResponseQuerySerialized
779: message Fact
780: enum ValueType
798: message CDOTASpeechMatchOnClient
805: message CDOTAUserMsg_UnitEvent
806: message Interval
811: message Speech
821: message SpeechMute
825: message AddGesture
834: message RemoveGesture
838: message BloodImpact
844: message FadeGesture
859: message CDOTAUserMsg_ItemPurchased
864: message CDOTAUserMsg_ItemSold
868: message CDOTAUserMsg_ItemFound
876: message CDOTAUserMsg_OverheadEvent
884: message CDOTAUserMsg_TutorialTipInfo
889: message CDOTAUserMsg_TutorialFinish
896: message CDOTAUserMsg_TutorialMinimapPosition
899: message CDOTAUserMsg_SendGenericToolTip
906: message CDOTAUserMsg_WorldLine
911: message CDOTAUserMsg_ChatWheel
919: message CDOTAUserMsg_ReceivedXmasGift
925: message CDOTAUserMsg_ShowSurvey
934: message CDOTAUserMsg_UpdateSharedContent
938: message CDOTAUserMsg_TutorialRequestExp
941: message CDOTAUserMsg_TutorialFade
945: message CDOTAUserMsg_TutorialPingMinimap
953: message CDOTAUserMsg_GamerulesStateChanged
957: message CDOTAUserMsg_AddQuestLogEntry
962: message CDOTAUserMsg_SendStatPopup
967: message CDOTAUserMsg_DismissAllStatPopups
971: message CDOTAUserMsg_SendRoshanSpectatorPhase
977: message CDOTAUserMsg_SendRoshanPopup
982: message CDOTAUserMsg_SendFinalGold
987: message CDOTAUserMsg_CustomMsg
993: message CDOTAUserMsg_CoachHUDPing
998: message CDOTAUserMsg_ClientLoadGridNav
1001: message CDOTAUserMsg_TE_Projectile
1022: message CDOTAUserMsg_TE_ProjectileLoc
1041: message CDOTAUserMsg_TE_DestroyProjectile
1045: message CDOTAUserMsg_TE_DotaBloodImpact
1052: message CDOTAUserMsg_AbilityPing
1068: message CDOTAUserMsg_TE_UnitAnimation
1078: message CDOTAUserMsg_TE_UnitAnimationEnd
1083: message CDOTAUserMsg_ShowGenericPopup
1092: message CDOTAUserMsg_VoteStart
1099: message CDOTAUserMsg_VoteUpdate
1103: message CDOTAUserMsg_VoteEnd
1107: message CDOTAUserMsg_BoosterStatePlayer
1115: message CDOTAUserMsg_BoosterState
1119: message CDOTAUserMsg_AbilitySteal
1125: message CDOTAUserMsg_StatsHeroLookup
1132: message CDOTAUserMsg_StatsHeroPositionInfo
1133: message PositionPair
1142: message CDOTAUserMsg_StatsHeroMinuteDetails
1160: message CDOTAUserMsg_StatsTeamMinuteDetails
1161: message LocationPerformance
1179: message CDOTAUserMsg_StatsPlayerKillShare
1188: message CDOTAUserMsg_StatsKillDetails
1197: message CDOTAUserMsg_StatsMatchDetails
1200: message CDOTAUserMsg_StatsFightTeamDetails
1207: message CDOTAUserMsg_StatsFightDetails
1222: message CDOTAUserMsg_MiniTaunt
1226: message CDOTAUserMsg_SpeechBubble
1230: message CDOTAUserMsg_CustomHeaderMessage
1237: message CMsgHeroAbilityStat
1243: message CMsgCombatAnalyzerPlayerStat
1248: message CMsgCombatAnalyzerStats
1253: message CDOTAUserMsg_BeastChat
1260: message CDOTAUserMsg_CustomHudElement_Create
1266: message CDOTAUserMsg_CustomHudElement_Modify
1272: message CDOTAUserMsg_CustomHudElement_Destroy
1276: message CDOTAUserMsg_CompendiumStatePlayer
1281: message CDOTAUserMsg_CompendiumState
1285: message CDOTAUserMsg_ProjectionAbility
1296: message CDOTAUserMsg_ProjectionEvent
1301: message CDOTAUserMsg_XPAlert
1306: message CDOTAUserMsg_TalentTreeAlert
1314: message CDOTAUserMsg_UpdateQuestProgress
1317: message CDOTAUserMsg_QuestStatus
1328: message CDOTAUserMsg_SuggestHeroPick
1335: message CDOTAUserMsg_SuggestHeroRole
1340: message CDOTAUserMsg_KillcamDamageTaken
1349: message CDOTAUserMsg_SelectPenaltyGold
1354: message CDOTAUserMsg_RollDiceResult
1362: message CDOTAUserMsg_FlipCoinResult
1368: message CDOTAUserMessage_RequestItemSuggestions
1372: message CDOTAUserMessage_TeamCaptainChanged
1377: message CDOTAUserMsg_ChatWheelCooldown
1382: message CDOTAUserMsg_HeroRelicProgress
1390: message CDOTAUserMsg_AbilityDraftRequestAbility
1398: message CDOTAUserMsg_DamageReport
1406: message CDOTAUserMsg_SalutePlayer
1415: message CDOTAUserMsg_GiftPlayer
1421: message CDOTAUserMsg_TipAlert
1426: message CDOTAUserMsg_ReplaceQueryUnit
1432: message CDOTAUserMsg_ESArcanaCombo
1438: message CDOTAUserMsg_ESArcanaComboSummary
1444: message CDOTAUserMsg_OMArcanaCombo
1451: message CDOTAUserMsg_HighFiveCompleted
1458: message CDOTAUserMsg_HighFiveLeftHanging
1462: message CDOTAUserMsg_ShovelUnearth
1469: message CDOTAUserMsg_AllStarEvent
1470: message PlayerScore
1482: message CDOTAUserMsg_QueuedOrderRemoved
1486: message CDOTAUserMsg_DebugChallenge
1496: message CDOTAUserMsg_FoundNeutralItem
1506: message CDOTAUserMsg_OutpostCaptured
1511: message CDOTAUserMsg_OutpostGrantedXP
1516: message CDOTAUserMsg_MoveCameraToUnit
1520: message CDOTAUserMsg_PauseMinigameData
1521: message DataBit
1530: message CDOTAUserMsg_VersusScene_PlayerBehavior
1538: message CDOTAUserMsg_QoP_ArcanaSummary
1545: message CDOTAUserMsg_HotPotato_Created
1550: message CDOTAUserMsg_HotPotato_Exploded
1554: message CDOTAUserMsg_WK_Arcana_Progress
1560: message CDOTAUserMsg_GuildChallenge_Progress
1561: message PlayerProgress
1566: enum EChallengeType
1581: message CDOTAUserMsg_WRArcanaProgress
1591: message CDOTAUserMsg_WRArcanaSummary
1602: message CDOTAUserMsg_EmptyItemSlotAlert
1609: message CDOTAUserMsg_AghsStatusAlert
1618: message CDOTAUserMsg_MutedPlayers
1623: message CDOTAUserMsg_ContextualTip
1641: message CDOTAUserMsg_ChatMessage
1647: message CDOTAUserMsg_RockPaperScissorsStarted
1652: message CDOTAUserMsg_RockPaperScissorsFinished
1659: message CDOTAUserMsg_DuelOpponentKilled
1664: message CDOTAUserMsg_DuelAccepted
1669: message CDOTAUserMsg_DuelRequested
1673: message CDOTAUserMsg_MuertaReleaseEvent_AssignedTargetKilled
1681: message CDOTAUserMsg_PlayerDraftSuggestPick
1686: message CDOTAUserMsg_PlayerDraftPick
1692: message CDOTAUserMsg_FacetPing
1699: message CDOTAUserMsg_InnatePing
1705: message CDOTAUserMsg_NeutralCraftAvailable
1708: message CDOTAUserMsg_TimerAlert
1713: message CDOTAUserMsg_MadstoneAlert
1714: enum EMadstoneAlertType
1727: message CDOTAUserMsg_MonsterHunter_InvestigationsAvailable
1731: message CDOTAUserMsg_MonsterHunter_InvestigationGameState
1736: message CDOTAUserMsg_MonsterHunter_HuntAlert
1737: enum EHuntAlertType
1747: enum EHuntStatusType
1760: message CDOTAUserMsg_KillEffect
1765: message CDOTAUserMsg_GiveItem
1766: enum EGiveStatus
```

</details>

<a id="econ-gcmessages-proto"></a>
### econ_gcmessages.proto

<details>
<summary><code>econ_gcmessages.proto</code> — module: <code>econ_gcmessages_pb2</code>; imports: 4; enums: 16; messages: 143</summary>

- Imports: steammessages.proto, econ_shared_enums.proto, gcsdk_gcmessages.proto, base_gcmessages.proto

```text
6: enum EGCItemMsg
144: enum EGCMsgInitiateTradeResponse
172: message CMsgApplyAutograph
177: message CMsgAdjustItemEquippedState
184: message CMsgEconPlayerStrangeCountAdjustment
185: message CStrangeCountAdjustment
196: message CMsgCraftingResponse
200: message CMsgGCRequestStoreSalesData
205: message CMsgGCRequestStoreSalesDataResponse
206: message Price
216: message CMsgGCRequestStoreSalesDataUpToDateResponse
221: message CMsgGCToGCPingRequest
224: message CMsgGCToGCPingResponse
227: message CMsgGCToGCGetUserSessionServer
231: message CMsgGCToGCGetUserSessionServerResponse
236: message CMsgGCToGCGetUserServerMembers
241: message CMsgGCToGCGetUserServerMembersResponse
245: message CMsgLookupMultipleAccountNames
249: message CMsgLookupMultipleAccountNamesResponse
250: message Account
258: message CMsgRequestCrateItems
262: message CMsgRequestCrateItemsResponse
263: enum EResult
274: message CMsgRequestCrateEscalationLevel
278: message CMsgRequestCrateEscalationLevelResponse
279: enum EResult
291: message CMsgGCToGCCanUseDropRateBonus
299: message CMsgSQLAddDropRateBonus
309: message CMsgSQLUpgradeBattleBooster
316: message CMsgGCToGCRefreshSOCache
321: message CMsgGCToGCAddSubscriptionTime
327: message CMsgGCToGCGrantAccountRolledItems
328: message Item
329: message DynamicAttribute
336: message AdditionalAuditEntry
358: message CMsgGCToGCBetaDeleteItems
364: message CMsgGCToGCGrantSelfMadeItemToAccount
369: message CMsgGCToGCUnlockCrate
375: message CMsgUseItem
384: message CMsgServerUseItem
389: message CMsgUseMultipleItems
393: message CGCStoreRechargeRedirect_LineItem
398: message CMsgGCEconSQLWorkItemEmbeddedRollbackData
406: message CMsgCraftStatue
415: message CMsgRedeemCode
419: message CMsgRedeemCodeResponse
420: enum EResultCode
431: message CMsgDevNewItemRequest
439: message CMsgDevNewItemRequestResponse
440: enum EResponse
454: message CMsgDevUnlockAllItemStyles
458: message CMsgDevUnlockAllItemStylesResponse
462: message CMsgGCGetAccountSubscriptionItem
466: message CMsgGCGetAccountSubscriptionItemResponse
470: message CMsgGCAddGiftItem
478: message CMsgClientToGCWrapAndDeliverGift
484: message CMsgSQLGCToGCRevokeUntrustedGift
489: message CMsgClientToGCWrapAndDeliverGiftResponse
499: message CMsgClientToGCUnwrapGift
503: message CMsgClientToGCGetGiftPermissions
506: message CMsgClientToGCGetGiftPermissionsResponse
507: message FriendPermission
520: message CMsgClientToGCUnpackBundle
524: message CMsgClientToGCUnpackBundleResponse
525: enum EUnpackBundle
540: message CMsgClientToGCPackBundle
545: message CMsgClientToGCPackBundleResponse
546: enum EPackBundle
568: message CMsgGCToClientStoreTransactionCompleted
573: message CMsgClientToGCEquipItems
577: message CMsgClientToGCEquipItemsResponse
581: message CMsgClientToGCSetItemStyle
586: message CMsgClientToGCSetItemStyleResponse
587: enum ESetStyle
596: message CMsgClientToGCUnlockItemStyle
602: message CMsgClientToGCUnlockItemStyleResponse
603: enum EUnlockStyle
624: message CMsgClientToGCSetItemInventoryCategory
631: message CMsgClientToGCUnlockCrate
636: message CMsgClientToGCUnlockCrateResponse
637: message Item
646: message CMsgClientToGCRemoveItemAttribute
650: message CMsgClientToGCRemoveItemAttributeResponse
651: enum ERemoveItemAttribute
663: message CMsgClientToGCNameItem
669: message CMsgClientToGCNameItemResponse
670: enum ENameItem
682: message CMsgGCSetItemPosition
687: message CAttribute_ItemDynamicRecipeComponent
700: message CProtoItemSocket
710: message CProtoItemSocket_Empty
714: message CProtoItemSocket_Effect
719: message CProtoItemSocket_Color
726: message CProtoItemSocket_Strange
732: message CProtoItemSocket_Strange_DESERIALIZE_FROM_STRING_ONLY
739: message CProtoItemSocket_Spectator
747: message CProtoItemSocket_AssetModifier
752: message CProtoItemSocket_AssetModifier_DESERIALIZE_FROM_STRING_ONLY
759: message CProtoItemSocket_Autograph
766: message CProtoItemSocket_StaticVisuals
770: message CAttribute_String
774: message CWorkshop_GetItemDailyRevenue_Request
781: message CWorkshop_GetItemDailyRevenue_Response
782: message CountryDailyRevenue
792: message CWorkshop_GetPackageDailyRevenue_Request
798: message CWorkshop_GetPackageDailyRevenue_Response
799: message CountryDailyRevenue
809: message CMsgSQLGCToGCGrantBackpackSlots
814: message CMsgClientToGCLookupAccountName
818: message CMsgClientToGCLookupAccountNameResponse
823: message CMsgClientToGCCreateStaticRecipe
824: message Item
833: message CMsgClientToGCCreateStaticRecipeResponse
834: message OutputItem
840: message InputError
845: message AdditionalOutput
850: enum EResponse
865: message CMsgProcessTransactionOrder
866: message Item
890: message CMsgGCToGCStoreProcessCDKeyTransaction
896: message CMsgGCToGCStoreProcessCDKeyTransactionResponse
900: message CMsgGCToGCStoreProcessSettlement
904: message CMsgGCToGCStoreProcessSettlementResponse
908: message CMsgGCToGCBroadcastConsoleCommand
916: message CMsgGCToGCConsoleOutput
917: message OutputLine
928: message CMsgItemAges
929: message MaxItemIDTimestamp
937: message CMsgGCToGCInternalTestMsg
947: message CMsgGCToGCClientServerVersionsUpdated
955: message CMsgGCToGCBroadcastMessageFromSub
962: message CMsgGCToClientCurrencyPricePoints
963: message Currency
972: message CMsgBannedWordList
977: message CMsgGCToGCFlushSteamInventoryCache
978: message Key
986: message CMsgGCToGCUpdateSubscriptionItems
991: message CMsgGCToGCSelfPing
995: message CMsgGCToGCGetInfuxIntervalStats
998: message CMsgGCToGCGetInfuxIntervalStatsResponse
1006: message CMsgGCToGCPurchaseSucceeded
1009: message CMsgClientToGCGetLimitedItemPurchaseQuantity
1013: message CMsgClientToGCGetLimitedItemPurchaseQuantityResponse
1014: enum EResponse
1028: message CMsgClientToGCGetInFlightItemCharges
1032: message CMsgClientToGCGetInFlightItemChargesResponse
1033: enum EResponse
1046: message CMsgClientToGCPurchaseChargeCostItems
1047: message Item
1058: message CMsgClientToGCPurchaseChargeCostItemsResponse
1059: enum EResponse
1076: message CMsgGCToClientInFlightChargesUpdated
1077: message ItemCharges
1085: message CMsgClientToGCCancelUnfinalizedTransactions
1089: message CMsgClientToGCCancelUnfinalizedTransactionsResponse
1093: message CMsgGCToGCUpdateWelcomeMsg
1099: message CMsgClientToGCRecycleMultipleItems
1100: message Item
1109: message CMsgClientToGCRecycleMultipleItemsResponse
```

</details>

<a id="econ-shared-enums-proto"></a>
### econ_shared_enums.proto

<details>
<summary><code>econ_shared_enums.proto</code> — module: <code>econ_shared_enums_pb2</code>; imports: 0; enums: 3; messages: 1</summary>

- Imports: *(none)*

```text
1: enum EGCEconBaseMsg
5: enum EGCMsgResponse
17: enum EGCMsgUseItemResponse
37: message CMsgGenericResult
```

</details>

<a id="engine-gcmessages-proto"></a>
### engine_gcmessages.proto

<details>
<summary><code>engine_gcmessages.proto</code> — module: <code>engine_gcmessages_pb2</code>; imports: 1; enums: 0; messages: 1</summary>

- Imports: google/protobuf/descriptor.proto

```text
3: message CEngineGotvSyncPacket
```

</details>

<a id="enums-clientserver-proto"></a>
### enums_clientserver.proto

<details>
<summary><code>enums_clientserver.proto</code> — module: <code>enums_clientserver_pb2</code>; imports: 0; enums: 4; messages: 0</summary>

- Imports: *(none)*

```text
4: enum EMsg
1493: enum EClientPersonaStateFlag
1510: enum EMsgClanAccountFlags
1518: enum ESteamReviewScore
```

</details>

<a id="event-gcmessages-client-proto"></a>
### event_gcmessages_client.proto

<details>
<summary><code>event_gcmessages_client.proto</code> — module: <code>event_gcmessages_client_pb2</code>; imports: 2; enums: 2; messages: 3</summary>

- Imports: events.proto, event_gcmessages_common.proto

```text
4: enum EGCEventClientMessages
10: message CMsgClientToGCGetEventPoints
15: message CMsgClientToGCGetEventPointsResponse
16: enum EResponse
29: message CMsgGCToClientEventPointsUpdated
```

</details>

<a id="event-gcmessages-common-proto"></a>
### event_gcmessages_common.proto

<details>
<summary><code>event_gcmessages_common.proto</code> — module: <code>event_gcmessages_common_pb2</code>; imports: 0; enums: 0; messages: 2</summary>

- Imports: *(none)*

```text
1: message CMsgEventAction
6: message CMsgUserEventPoints
```

</details>

<a id="event-gcmessages-server-proto"></a>
### event_gcmessages_server.proto

<details>
<summary><code>event_gcmessages_server.proto</code> — module: <code>event_gcmessages_server_pb2</code>; imports: 0; enums: 0; messages: 0</summary>

- Imports: *(none)*

```text
```

</details>

<a id="events-proto"></a>
### events.proto

<details>
<summary><code>events.proto</code> — module: <code>events_pb2</code>; imports: 0; enums: 1; messages: 0</summary>

- Imports: *(none)*

```text
1: enum EEvent
```

</details>

<a id="gameevents-proto"></a>
### gameevents.proto

<details>
<summary><code>gameevents.proto</code> — module: <code>gameevents_pb2</code>; imports: 1; enums: 1; messages: 18</summary>

- Imports: networkbasetypes.proto

```text
3: enum EBaseGameEvents
21: message CMsgVDebugGameSessionIDEvent
26: message CMsgPlaceDecalEvent
44: message CMsgClearWorldDecalsEvent
48: message CMsgClearEntityDecalsEvent
52: message CMsgClearDecalsForEntityEvent
57: message CMsgSource1LegacyGameEventList
60: message key_t
65: message descriptor_t
74: message CMsgSource1LegacyListenEvents
79: message CMsgSource1LegacyGameEvent
80: message key_t
98: message CMsgSosStartSoundEvent
107: message CMsgSosStopSoundEvent
111: message CMsgSosStopSoundEventHash
116: message CMsgSosSetSoundEventParams
121: message CMsgSosSetLibraryStackFields
126: message CMsgClothStiffenAnimEvent
135: message CMsgClothEffectAnimEvent
```

</details>

<a id="gcsdk-gcmessages-proto"></a>
### gcsdk_gcmessages.proto

<details>
<summary><code>gcsdk_gcmessages.proto</code> — module: <code>gcsdk_gcmessages_pb2</code>; imports: 3; enums: 3; messages: 74</summary>

- Imports: valveextensions.proto, steammessages.proto, steammessages_steamlearn.steamworkssdk.proto

```text
5: enum ESourceEngine
10: enum PartnerAccountType
16: enum GCConnectionStatus
26: message CExtraMsgBlock
33: message CMsgSteamLearnServerInfo
34: message ProjectInfo
46: message CMsgGCAssertJobData
51: message CMsgGCConCommand
55: message CMsgSDOAssert
56: message Request
65: message CMsgSOIDOwner
70: message CMsgSOSingleObject
78: message CMsgSOMultipleObjects
79: message SingleObject
95: message CMsgSOCacheSubscribed
96: message SubscribedType
109: message CMsgSOCacheSubscribedUpToDate
117: message CMsgSOCacheUnsubscribed
121: message CMsgSOCacheSubscriptionCheck
129: message CMsgSOCacheSubscriptionRefresh
133: message CMsgSOCacheVersion
137: message CMsgGCMultiplexMessage
143: message CMsgGCToGCSubGCStarting
147: message CGCToGCMsgMasterAck
148: message Process
159: message CGCToGCMsgMasterAck_Response
163: message CMsgGCToGCUniverseStartup
167: message CMsgGCToGCUniverseStartupResponse
171: message CGCToGCMsgMasterStartupComplete
172: message GCInfo
180: message CGCToGCMsgRouted
186: message CGCToGCMsgRoutedReply
191: message CMsgGCUpdateSubGCSessionInfo
192: message CMsgUpdate
201: message CMsgGCRequestSubGCSessionInfo
205: message CMsgGCRequestSubGCSessionInfoResponse
212: message CMsgSOCacheHaveVersion
219: message CMsgClientHello
244: message CMsgClientWelcome
245: message Location
269: message CMsgConnectionStatus
278: message CMsgGCToGCSOCacheSubscribe
279: message CMsgHaveVersions
291: message CMsgGCToGCSOCacheUnsubscribe
297: message CMsgGCClientPing
300: message CMsgGCToGCForwardAccountDetails
306: message CMsgGCToGCLoadSessionSOCache
311: message CMsgGCToGCLoadSessionSOCacheResponse
314: message CMsgGCToGCUpdateSessionStats
320: message CMsgGCToClientRequestDropped
323: message CWorkshop_PopulateItemDescriptions_Request
324: message SingleItemDescription
329: message ItemDescriptionsLanguageBlock
338: message CWorkshop_GetContributors_Request
343: message CWorkshop_GetContributors_Response
347: message CWorkshop_SetItemPaymentRules_Request
348: message WorkshopItemPaymentRule
355: message WorkshopDirectPaymentRule
360: message PartnerItemPaymentRule
375: message CWorkshop_SetItemPaymentRules_Response
379: message CCommunity_ClanAnnouncementInfo
394: message CCommunity_GetClanAnnouncements_Request
410: message CCommunity_GetClanAnnouncements_Response
416: message CBroadcast_PostGameDataFrame_Request
423: message CMsgSerializedSOCache
424: message TypeCache
430: message Cache
431: message Version
447: message CMsgGCToClientPollConvarRequest
452: message CMsgGCToClientPollConvarResponse
457: message CGCMsgCompressedMsgToClient
462: message CMsgGCToGCMasterBroadcastMessage
471: message CMsgGCToGCMasterSubscribeToCache
478: message CMsgGCToGCMasterSubscribeToCacheResponse
481: message CMsgGCToGCMasterSubscribeToCacheAsync
485: message CMsgGCToGCMasterUnsubscribeFromCache
492: message CMsgGCToGCMasterDestroyCache
```

</details>

<a id="gcsystemmsgs-proto"></a>
### gcsystemmsgs.proto

<details>
<summary><code>gcsystemmsgs.proto</code> — module: <code>gcsystemmsgs_pb2</code>; imports: 0; enums: 2; messages: 0</summary>

- Imports: *(none)*

```text
1: enum ESOMsg
12: enum EGCBaseClientMsg
```

</details>

<a id="netmessages-proto"></a>
### netmessages.proto

<details>
<summary><code>netmessages.proto</code> — module: <code>netmessages_pb2</code>; imports: 2; enums: 12; messages: 74</summary>

- Imports: networkbasetypes.proto, source2_steam_stats.proto

```text
4: enum CLC_Messages
21: enum SVC_Messages
55: enum VoiceDataFormat_t
61: enum RequestPause_t
67: enum PrefetchType
71: enum ESplitScreenMessageType
76: enum EQueryCvarValueStatus
83: enum DIALOG_TYPE
91: enum SVC_Messages_LowFrequency
95: enum Bidirectional_Messages
102: enum ReplayEventType_t
110: message CCLCMsg_ClientInfo
118: message CCLCMsg_Move
123: message CMsgVoiceAudio
135: message CCLCMsg_VoiceData
141: message CCLCMsg_BaselineAck
146: message CCLCMsg_ListenEvents
150: message CCLCMsg_RespondCvarValue
157: message CCLCMsg_LoadingProgress
161: message CCLCMsg_SplitPlayerConnect
165: message CCLCMsg_SplitPlayerDisconnect
169: message CCLCMsg_ServerStatus
173: message CCLCMsg_RequestPause
178: message CCLCMsg_CmdKeyValues
184: message CCLCMsg_RconServerDetails
188: message CCLCMsg_Diagnostic
198: message CSVCMsg_ServerInfo
219: message CSVCMsg_ClassInfo
222: message class_t
231: message CSVCMsg_SetPause
235: message CSVCMsg_VoiceInit
241: message CSVCMsg_Print
247: message CSVCMsg_Sounds
248: message sounddata_t
274: message CSVCMsg_Prefetch
279: message CSVCMsg_SetView
284: message CSVCMsg_FixAngle
289: message CSVCMsg_CrosshairAngle
293: message CSVCMsg_BSPDecal
301: message CSVCMsg_SplitScreen
307: message CSVCMsg_GetCvarValue
312: message CSVCMsg_Menu
317: message CSVCMsg_UserMessage
323: message CSVCMsg_SendTable
324: message sendprop_t
342: message CSVCMsg_GameEventList
343: message key_t
348: message descriptor_t
357: message CSVCMsg_PacketEntities
360: message alternate_baseline_t
365: message non_transmitted_entities_t
370: message outofpvs_entity_updates_t
399: message CSVCMsg_TempEntities
405: message CSVCMsg_CreateStringTable
420: message CSVCMsg_UpdateStringTable
428: message CSVCMsg_VoiceData
439: message CSVCMsg_PacketReliable
445: message CSVCMsg_FullFrameSplit
452: message CSVCMsg_HLTVStatus
459: message CSVCMsg_ServerSteamID
463: message CSVCMsg_CmdKeyValues
467: message CSVCMsg_RconServerDetails
472: message CMsgIPCAddress
477: message CMsgServerPeer
486: message CSVCMsg_PeerList
490: message CSVCMsg_ClearAllStringTables
495: message ProtoFlattenedSerializerField_t
496: message polymorphic_field_t
515: message ProtoFlattenedSerializer_t
521: message CSVCMsg_FlattenedSerializer
529: message CSVCMsg_StopSound
533: message CBidirMsg_RebroadcastGameEvent
540: message CBidirMsg_RebroadcastSource
544: message CBidirMsg_PredictionEvent
545: enum ESyncType
556: message CMsgServerNetworkStats
557: message Port
562: message Player
600: message CSVCMsg_HltvReplay
611: message CCLCMsg_HltvReplay
619: message CSVCMsg_Broadcast_Command
623: message CCLCMsg_HltvFixupOperatorTick
634: message CSVCMsg_HltvFixupOperatorStatus
639: message CMsgServerUserCmd
648: message CSVCMsg_UserCommands
652: message CSVCMsg_NextMsgPredicted
```

</details>

<a id="network-connection-proto"></a>
### network_connection.proto

<details>
<summary><code>network_connection.proto</code> — module: <code>network_connection_pb2</code>; imports: 1; enums: 1; messages: 0</summary>

- Imports: google/protobuf/descriptor.proto

```text
9: enum ENetworkDisconnectionReason
```

</details>

<a id="networkbasetypes-proto"></a>
### networkbasetypes.proto

<details>
<summary><code>networkbasetypes.proto</code> — module: <code>networkbasetypes_pb2</code>; imports: 3; enums: 3; messages: 27</summary>

- Imports: valveextensions.proto, google/protobuf/descriptor.proto, network_connection.proto

```text
9: enum SignonState_t
20: enum NET_Messages
36: enum SpawnGroupFlags_t
47: message CMsgVector
56: message CMsgVector2D
63: message CMsgQAngle
71: message CMsgQuaternion
80: message CMsgTransform
88: message CMsgRGBA
97: message CMsgPlayerInfo
106: message CEntityMsg
110: message CMsg_CVars
111: message CVar
119: message CNETMsg_NOP
122: message CNETMsg_SplitScreenUser
126: message CNETMsg_Tick
139: message CNETMsg_StringCmd
144: message CNETMsg_SetConVar
150: message CNETMsg_SignonState
159: message CSVCMsg_GameEvent
160: message key_t
176: message CSVCMsgList_GameEvents
177: message event_t
185: message CNETMsg_SpawnGroup_Load
210: message CNETMsg_SpawnGroup_ManifestUpdate
218: message CNETMsg_SpawnGroup_SetCreationTick
224: message CNETMsg_SpawnGroup_Unload
230: message CNETMsg_SpawnGroup_LoadCompleted
234: message CSVCMsg_GameSessionConfiguration
256: message CNETMsg_DebugOverlay
```

</details>

<a id="networksystem-protomessages-proto"></a>
### networksystem_protomessages.proto

<details>
<summary><code>networksystem_protomessages.proto</code> — module: <code>networksystem_protomessages_pb2</code>; imports: 0; enums: 0; messages: 5</summary>

- Imports: *(none)*

```text
1: message NetMessageSplitscreenUserChanged
5: message NetMessageConnectionClosed
10: message NetMessageConnectionCrashed
15: message NetMessagePacketStart
18: message NetMessagePacketEnd
```

</details>

<a id="prediction-events-proto"></a>
### prediction_events.proto

<details>
<summary><code>prediction_events.proto</code> — module: <code>prediction_events_pb2</code>; imports: 1; enums: 1; messages: 3</summary>

- Imports: networkbasetypes.proto

```text
3: enum EBasePredictionEvents
9: message CPredictionEvent_Teleport
16: message CPredictionEvent_StringCommand
20: message CPredictionEvent_Diagnostic
```

</details>

<a id="source2-steam-stats-proto"></a>
### source2_steam_stats.proto

<details>
<summary><code>source2_steam_stats.proto</code> — module: <code>source2_steam_stats_pb2</code>; imports: 0; enums: 1; messages: 16</summary>

- Imports: *(none)*

```text
1: enum ESource2PlayStatsFieldType
22: message CMsgSource2SystemSpecs
39: message CMsgSource2VProfLiteReportItem
60: message CMsgSource2VProfLiteReport
66: message CMsgSource2NetworkFlowQuality
113: message CMsgSource2PerfIntervalSample
114: message Tag
127: message CSource2Metrics_MatchPerfSummary_Notification
128: message Client
147: message CMsgSource2PlayStatsPackedRecordList
148: message FieldDef
153: message SteamIDList
179: message CSource2Metrics_RecordPlayStats_Notification
184: message CSource2Metrics_FetchMapData_Request
193: message CSource2Metrics_FetchMapData_Response
194: message MapData
203: message CUserMessage_UserSentBugBug
```

</details>

<a id="steamdatagram-messages-auth-proto"></a>
### steamdatagram_messages_auth.proto

<details>
<summary><code>steamdatagram_messages_auth.proto</code> — module: <code>steamdatagram_messages_auth_pb2</code>; imports: 1; enums: 0; messages: 7</summary>

- Imports: steamnetworkingsockets_messages_certs.proto

```text
6: message CMsgSteamDatagramRelayAuthTicket
7: message ExtraField
29: message CMsgSteamDatagramSignedRelayAuthTicket
37: message CMsgSteamDatagramCachedCredentialsForApp
43: message CMsgSteamDatagramGameCoordinatorServerLogin
53: message CMsgSteamDatagramSignedGameCoordinatorServerLogin
59: message CMsgSteamDatagramHostedServerAddressPlaintext
```

</details>

<a id="steamdatagram-messages-sdr-proto"></a>
### steamdatagram_messages_sdr.proto

<details>
<summary><code>steamdatagram_messages_sdr.proto</code> — module: <code>steamdatagram_messages_sdr_pb2</code>; imports: 2; enums: 10; messages: 42</summary>

- Imports: steamnetworkingsockets_messages_certs.proto, steamnetworkingsockets_messages.proto

```text
7: enum ESteamDatagramMsgID
44: message CMsgSteamNetworkingIPAddress
49: message CMsgSteamDatagramSignedMessageGeneric
56: message CMsgSteamDatagramRouterPingReply
57: message RouteException
63: message AltAddress
64: enum Protocol
75: enum Flags
103: message CMsgSteamDatagramGameserverPingRequestBody
113: message CMsgSteamDatagramGameserverPingRequestEnvelope
125: message CMsgSteamDatagramGameserverPingReplyData
139: message CMsgSteamDatagramNoSessionRelayToClient
148: message CMsgSteamDatagramNoSessionRelayToPeer
155: message CMsgTOSTreatment
161: message CMsgSteamDatagramClientPingSampleRequest
165: message CMsgSteamDatagramClientPingSampleReply
166: message POP
167: message AltAddress
191: message LegacyDataCenter
204: message CMsgSteamDatagramClientSwitchedPrimary
205: message RouterQuality
226: message CMsgSteamDatagramConnectRequest
238: message CMsgSteamDatagramConnectOK
248: message CMsgSteamNetworkingP2PSDRRoutingSummary
266: message CMsgSteamDatagramP2PRoutingSummary
271: message CMsgSteamDatagramConnectionClosed
272: enum ERelayMode
300: message CMsgSteamDatagramNoConnection
319: message CMsgSteamDatagramGameserverSessionRequest
333: message CMsgSteamDatagramGameserverSessionEstablished
342: message CMsgSteamDatagramConnectionStatsClientToRouter
343: enum Flags
361: message CMsgSteamDatagramConnectionStatsRouterToClient
362: enum Flags
382: message CMsgSteamDatagramConnectionStatsRouterToServer
383: enum Flags
404: message CMsgSteamDatagramConnectionStatsServerToRouter
405: enum Flags
423: message CMsgSteamDatagramP2PSessionRequestBody
424: message EncryptedData
443: message CMsgSteamDatagramP2PSessionRequest
449: message CMsgSteamDatagramP2PSessionEstablished
456: message CMsgSteamDatagramConnectionStatsP2PClientToRouter
457: enum Flags
481: message CMsgSteamDatagramConnectionStatsP2PRouterToClient
482: enum Flags
506: message CMsgSteamDatagramP2PBadRouteRouterToClient
513: message CMsgSteamDatagramP2PRoutes
514: message RelayCluster
521: message Route
533: message CMsgSteamDatagramSetSecondaryAddressRequest
542: message CMsgSteamDatagramSetSecondaryAddressResult
```

</details>

<a id="steammessages-proto"></a>
### steammessages.proto

<details>
<summary><code>steammessages.proto</code> — module: <code>steammessages_pb2</code>; imports: 1; enums: 2; messages: 5</summary>

- Imports: google/protobuf/descriptor.proto

```text
12: enum EGCPlatform
19: enum GCProtoBufMsgSrc
28: message CMsgProtoBufHeader
44: message CGCSystemMsg_GetAccountDetails
52: message CGCSystemMsg_GetAccountDetails_Response
95: message CIPLocationInfo
104: message CGCMsgGetIPLocationResponse
```

</details>

<a id="steammessages-base-proto"></a>
### steammessages_base.proto

<details>
<summary><code>steammessages_base.proto</code> — module: <code>steammessages_base_pb2</code>; imports: 1; enums: 3; messages: 18</summary>

- Imports: google/protobuf/descriptor.proto

```text
21: enum EBanContentCheckResult
32: enum EProtoClanEventType
70: enum PartnerEventNotificationType
77: message CMsgIPAddress
84: message CMsgIPAddressBucket
89: message CMsgProtoBufHeader
122: message CMsgMulti
127: message CMsgProtobufWrapped
131: message CMsgAuthTicket
141: message CCDDBAppDetailCommon
156: message CMsgAppRights
176: message CCuratorPreferences
193: message CLocalizationToken
198: message CClanEventUserNewsTuple
211: message CClanMatchEventByRange
218: message CCommunity_ClanAnnouncementInfo
237: message CClanEventData
270: message CBilling_Address
283: message CPackageReservationStatus
294: message CMsgKeyValuePair
299: message CMsgKeyValueSet
```

</details>

<a id="steammessages-cloud-steamworkssdk-proto"></a>
### steammessages_cloud.steamworkssdk.proto

<details>
<summary><code>steammessages_cloud.steamworkssdk.proto</code> — module: <code>steammessages_cloud.steamworkssdk_pb2</code>; imports: 1; enums: 0; messages: 9</summary>

- Imports: steammessages_unified_base.steamworkssdk.proto

```text
3: message CCloud_GetUploadServerInfo_Request
7: message CCloud_GetUploadServerInfo_Response
11: message CCloud_GetFileDetails_Request
16: message CCloud_UserFile
26: message CCloud_GetFileDetails_Response
30: message CCloud_EnumerateUserFiles_Request
37: message CCloud_EnumerateUserFiles_Response
42: message CCloud_Delete_Request
47: message CCloud_Delete_Response
```

</details>

<a id="steammessages-gamenetworkingui-proto"></a>
### steammessages_gamenetworkingui.proto

<details>
<summary><code>steammessages_gamenetworkingui.proto</code> — module: <code>steammessages_gamenetworkingui_pb2</code>; imports: 2; enums: 0; messages: 5</summary>

- Imports: steamnetworkingsockets_messages.proto, steamdatagram_messages_sdr.proto

```text
7: message CGameNetworkingUI_GlobalState
10: message CGameNetworkingUI_ConnectionState
40: message CGameNetworkingUI_Message
44: message CGameNetworkingUI_ConnectionSummary
55: message CGameNetworkingUI_AppSummary
```

</details>

<a id="steammessages-helprequest-steamworkssdk-proto"></a>
### steammessages_helprequest.steamworkssdk.proto

<details>
<summary><code>steammessages_helprequest.steamworkssdk.proto</code> — module: <code>steammessages_helprequest.steamworkssdk_pb2</code>; imports: 1; enums: 0; messages: 2</summary>

- Imports: steammessages_unified_base.steamworkssdk.proto

```text
5: message CHelpRequestLogs_UploadUserApplicationLog_Request
12: message CHelpRequestLogs_UploadUserApplicationLog_Response
```

</details>

<a id="steammessages-int-proto"></a>
### steammessages_int.proto

<details>
<summary><code>steammessages_int.proto</code> — module: <code>steammessages_int_pb2</code>; imports: 1; enums: 3; messages: 87</summary>

- Imports: steammessages.proto

```text
3: message CMsgWebAPIKey
11: message CMsgHttpRequest
12: message RequestHeader
17: message QueryParam
33: message CMsgWebAPIRequest
42: message CMsgHttpResponse
43: message ResponseHeader
53: message CMsgAMFindAccounts
58: message CMsgAMFindAccountsResponse
62: message CMsgNotifyWatchdog
72: message CMsgAMGetLicenses
76: message CMsgPackageLicense
82: message CMsgAMGetLicensesResponse
87: message CMsgGCGetCommandList
92: message CMsgGCGetCommandListResponse
96: message CGCMsgMemCachedGet
100: message CGCMsgMemCachedGetResponse
101: message ValueTag
109: message CGCMsgMemCachedSet
110: message KeyPair
118: message CGCMsgMemCachedDelete
122: message CGCMsgMemCachedStats
125: message CGCMsgMemCachedStatsResponse
142: message CGCMsgSQLStats
146: message CGCMsgSQLStatsResponse
158: message CMsgAMAddFreeLicense
165: message CMsgAMAddFreeLicenseResponse
171: message CGCMsgGetIPLocation
175: message CGCMsgGetIPASN
179: message CIPASNInfo
184: message CGCMsgGetIPASNResponse
188: message CMsgAMSendEmail
189: message ReplacementToken
194: message PersonaNameReplacementToken
207: message CMsgAMSendEmailResponse
211: message CMsgGCGetEmailTemplate
218: message CMsgGCGetEmailTemplateResponse
224: message CMsgAMGrantGuestPasses2
232: message CMsgAMGrantGuestPasses2Response
237: message CMsgGCGetPersonaNames
241: message CMsgGCGetPersonaNames_Response
242: message PersonaName
251: message CMsgGCCheckFriendship
256: message CMsgGCCheckFriendship_Response
261: message CMsgGCGetAppFriendsList
267: message CMsgGCGetAppFriendsList_Response
274: message CMsgGCMsgMasterSetDirectory
275: message SubGC
287: message CMsgGCMsgMasterSetDirectory_Response
292: message CMsgGCMsgWebAPIJobRequestForwardResponse
296: message CGCSystemMsg_GetPurchaseTrust_Request
300: message CGCSystemMsg_GetPurchaseTrust_Response
307: message CMsgGCHAccountVacStatusChange
315: message CMsgGCRoutingInfo
316: enum RoutingMethod
332: message CMsgGCMsgMasterSetWebAPIRouting
333: message Entry
342: message CMsgGCMsgMasterSetClientMsgRouting
343: message Entry
351: message CMsgGCMsgMasterSetWebAPIRouting_Response
355: message CMsgGCMsgMasterSetClientMsgRouting_Response
359: message CMsgGCMsgSetOptions
360: message MessageRange
365: enum Option
372: enum GCSQLVersion
382: message CMsgGCHUpdateSession
383: message ExtraField
399: message CMsgNotificationOfSuspiciousActivity
400: message MultipleGameInstances
410: message CMsgGCHVacVerificationChange
416: message CMsgGCHAccountPhoneNumberChange
424: message CMsgGCHAccountTwoFactorChange
430: message CMsgGCCheckClanMembership
435: message CMsgGCCheckClanMembership_Response
439: message CMsgGCHAppCheersReceived
440: message CheerTypeAmount
445: message CheerTarget
454: message CMsgGCHAppCheersGetAllowedTypes
459: message CMsgGCHAppCheersGetAllowedTypesResponse
460: message CheerRemaps
471: message CWorkshop_AddSpecialPayment_Request
479: message CWorkshop_AddSpecialPayment_Response
482: message CWorkshop_GetSpecialPayments_Request
488: message CWorkshop_GetSpecialPayments_Response
489: message SpecialPayment
500: message CMsgGCReportMetrics
501: message MetricEntry
502: message Dimension
512: message Measurement
531: message CMsgGCReportMetrics_Response
```

</details>

<a id="steammessages-oauth-steamworkssdk-proto"></a>
### steammessages_oauth.steamworkssdk.proto

<details>
<summary><code>steammessages_oauth.steamworkssdk.proto</code> — module: <code>steammessages_oauth.steamworkssdk_pb2</code>; imports: 1; enums: 0; messages: 2</summary>

- Imports: steammessages_unified_base.steamworkssdk.proto

```text
3: message COAuthToken_ImplicitGrantNoPrompt_Request
7: message COAuthToken_ImplicitGrantNoPrompt_Response
```

</details>

<a id="steammessages-player-steamworkssdk-proto"></a>
### steammessages_player.steamworkssdk.proto

<details>
<summary><code>steammessages_player.steamworkssdk.proto</code> — module: <code>steammessages_player.steamworkssdk_pb2</code>; imports: 1; enums: 1; messages: 38</summary>

- Imports: steammessages_unified_base.steamworkssdk.proto

```text
5: enum ENotificationSetting
11: message CPlayer_GetMutualFriendsForIncomingInvites_Request
14: message CPlayer_IncomingInviteMutualFriendList
19: message CPlayer_GetMutualFriendsForIncomingInvites_Response
23: message CPlayer_GetFriendsGameplayInfo_Request
27: message CPlayer_GetFriendsGameplayInfo_Response
28: message FriendsGameplayInfo
34: message OwnGameplayInfo
50: message CPlayer_GetGameBadgeLevels_Request
54: message CPlayer_GetGameBadgeLevels_Response
55: message Badge
65: message CPlayer_GetLastPlayedTimes_Request
69: message CPlayer_GetLastPlayedTimes_Response
70: message Game
81: message CPlayer_AcceptSSA_Request
84: message CPlayer_AcceptSSA_Response
87: message CPlayer_GetNicknameList_Request
90: message CPlayer_GetNicknameList_Response
91: message PlayerNickname
99: message CPlayer_GetPerFriendPreferences_Request
102: message PerFriendPreferences
114: message CPlayer_GetPerFriendPreferences_Response
118: message CPlayer_SetPerFriendPreferences_Request
122: message CPlayer_SetPerFriendPreferences_Response
125: message CPlayer_AddFriend_Request
129: message CPlayer_AddFriend_Response
134: message CPlayer_RemoveFriend_Request
138: message CPlayer_RemoveFriend_Response
142: message CPlayer_IgnoreFriend_Request
147: message CPlayer_IgnoreFriend_Response
151: message CPlayer_GetCommunityPreferences_Request
154: message CPlayer_CommunityPreferences
161: message CPlayer_GetCommunityPreferences_Response
165: message CPlayer_SetCommunityPreferences_Request
169: message CPlayer_SetCommunityPreferences_Response
172: message CPlayer_GetNewSteamAnnouncementState_Request
176: message CPlayer_GetNewSteamAnnouncementState_Response
184: message CPlayer_UpdateSteamAnnouncementLastRead_Request
189: message CPlayer_UpdateSteamAnnouncementLastRead_Response
```

</details>

<a id="steammessages-publishedfile-steamworkssdk-proto"></a>
### steammessages_publishedfile.steamworkssdk.proto

<details>
<summary><code>steammessages_publishedfile.steamworkssdk.proto</code> — module: <code>steammessages_publishedfile.steamworkssdk_pb2</code>; imports: 1; enums: 0; messages: 21</summary>

- Imports: steammessages_unified_base.steamworkssdk.proto

```text
3: message CPublishedFile_Subscribe_Request
10: message CPublishedFile_Subscribe_Response
13: message CPublishedFile_Unsubscribe_Request
20: message CPublishedFile_Unsubscribe_Response
23: message CPublishedFile_Publish_Request
42: message CPublishedFile_Publish_Response
47: message CPublishedFile_GetDetails_Request
57: message PublishedFileDetails
58: message Tag
63: message Preview
72: message Child
78: message KVTag
83: message VoteData
147: message CPublishedFile_GetDetails_Response
151: message CPublishedFile_GetUserFiles_Request
163: message CPublishedFile_GetUserFiles_Response
164: message App
177: message CPublishedFile_Update_Request
188: message CPublishedFile_Update_Response
191: message CPublishedFile_RefreshVotingQueue_Request
200: message CPublishedFile_RefreshVotingQueue_Response
```

</details>

<a id="steammessages-steamlearn-steamworkssdk-proto"></a>
### steammessages_steamlearn.steamworkssdk.proto

<details>
<summary><code>steammessages_steamlearn.steamworkssdk.proto</code> — module: <code>steammessages_steamlearn.steamworkssdk_pb2</code>; imports: 1; enums: 7; messages: 52</summary>

- Imports: steammessages_unified_base.steamworkssdk.proto

```text
3: enum ESteamLearnDataType
12: enum ESteammLearnRegisterDataSourceResult
26: enum ESteamLearnCacheDataResult
37: enum ESteamLearnSnapshotProjectResult
53: enum ESteamLearnGetAccessTokensResult
58: enum ESteamLearnInferenceResult
76: enum ESteamLearnInferenceMetadataResult
87: message CMsgSteamLearnDataSourceDescObject
91: message CMsgSteamLearnDataSourceDescElement
98: message CMsgSteamLearnDataSource
108: message CMsgSteamLearnDataObject
112: message CMsgSteamLearnDataElement
121: message CMsgSteamLearnData
127: message CMsgSteamLearnDataList
131: message CMsgSteamLearn_RegisterDataSource_Request
136: message CMsgSteamLearn_RegisterDataSource_Response
141: message CMsgSteamLearn_CacheData_Request
146: message CMsgSteamLearn_CacheData_Response
150: message CMsgSteamLearn_SnapshotProject_Request
159: message CMsgSteamLearn_SnapshotProject_Response
163: message CMsgSteamLearn_BatchOperation_Request
169: message CMsgSteamLearn_BatchOperation_Response
175: message CMsgSteamLearnAccessTokens
176: message CacheDataAccessToken
181: message SnapshotProjectAccessToken
186: message InferenceAccessToken
197: message CMsgSteamLearn_GetAccessTokens_Request
201: message CMsgSteamLearn_GetAccessTokens_Response
206: message CMsgInferenceIterateBeamSearch
207: message CustomItemScalar
222: message CMsgSteamLearn_Inference_Request
235: message CMsgSteamLearn_InferenceMetadata_Request
242: message CMsgSteamLearn_InferenceMetadataBackend_Request
247: message CMsgSteamLearn_InferenceMetadata_Response
248: message RowRange
253: message Range
259: message StdDev
265: message CompactTable
266: message Entry
272: message MapValuesEntry
277: message MapMappingsEntry
287: message SequenceTable
288: message Entry
294: message MapValuesEntry
299: message MapMappingsEntry
310: message KMeans
311: message Cluster
324: message SnapshotHistogram
331: message AppInfo
341: message AppInfoEntry
357: message CMsgSteamLearn_InferenceBackend_Response
358: message Sequence
362: message RegressionOutput
366: message NamedInferenceOutput
370: message BinaryCrossEntropyOutput
374: message MutliBinaryCrossEntropyOutput
380: message CategoricalCrossEntropyOutput
386: message Output
399: message CMsgSteamLearn_Inference_Response
```

</details>

<a id="steammessages-unified-base-steamworkssdk-proto"></a>
### steammessages_unified_base.steamworkssdk.proto

<details>
<summary><code>steammessages_unified_base.steamworkssdk.proto</code> — module: <code>steammessages_unified_base.steamworkssdk_pb2</code>; imports: 1; enums: 1; messages: 0</summary>

- Imports: google/protobuf/descriptor.proto

```text
27: enum EProtoExecutionSite
```

</details>

<a id="steamnetworkingsockets-messages-proto"></a>
### steamnetworkingsockets_messages.proto

<details>
<summary><code>steamnetworkingsockets_messages.proto</code> — module: <code>steamnetworkingsockets_messages_pb2</code>; imports: 1; enums: 2; messages: 16</summary>

- Imports: steamnetworkingsockets_messages_certs.proto

```text
6: enum ESteamNetworkingSocketsCipher
12: message CMsgSteamDatagramSessionCryptInfo
13: enum EKeyType
25: message CMsgSteamDatagramSessionCryptInfoSigned
30: message CMsgSteamDatagramDiagnostic
35: message CMsgSteamDatagramLinkInstantaneousStats
46: message CMsgSteamDatagramLinkLifetimeStats
96: message CMsgSteamDatagramConnectionQuality
101: message CMsgICECandidate
105: message CMsgICERendezvous
106: message Auth
114: message CMsgSteamNetworkingP2PRendezvous
115: message ConnectRequest
123: message ConnectOK
128: message ConnectionClosed
133: message ReliableMessage
137: message ApplicationMessage
161: message CMsgSteamNetworkingICESessionSummary
```

</details>

<a id="steamnetworkingsockets-messages-certs-proto"></a>
### steamnetworkingsockets_messages_certs.proto

<details>
<summary><code>steamnetworkingsockets_messages_certs.proto</code> — module: <code>steamnetworkingsockets_messages_certs_pb2</code>; imports: 0; enums: 1; messages: 4</summary>

- Imports: *(none)*

```text
4: message CMsgSteamNetworkingIdentityLegacyBinary
11: message CMsgSteamDatagramCertificate
12: enum EKeyType
29: message CMsgSteamDatagramCertificateSigned
36: message CMsgSteamDatagramCertificateRequest
```

</details>

<a id="steamnetworkingsockets-messages-udp-proto"></a>
### steamnetworkingsockets_messages_udp.proto

<details>
<summary><code>steamnetworkingsockets_messages_udp.proto</code> — module: <code>steamnetworkingsockets_messages_udp_pb2</code>; imports: 2; enums: 2; messages: 7</summary>

- Imports: steamnetworkingsockets_messages_certs.proto, steamnetworkingsockets_messages.proto

```text
7: enum ESteamNetworkingUDPMsgID
16: message CMsgSteamSockets_UDP_ChallengeRequest
22: message CMsgSteamSockets_UDP_ChallengeReply
29: message CMsgSteamSockets_UDP_ConnectRequest
42: message CMsgSteamSockets_UDP_ConnectOK
54: message CMsgSteamSockets_UDP_ConnectionClosed
61: message CMsgSteamSockets_UDP_NoConnection
66: message CMsgSteamSockets_UDP_Stats
67: enum Flags
```

</details>

<a id="te-proto"></a>
### te.proto

<details>
<summary><code>te.proto</code> — module: <code>te_pb2</code>; imports: 1; enums: 1; messages: 25</summary>

- Imports: networkbasetypes.proto

```text
3: enum ETEProtobufIds
29: message CMsgTEArmorRicochet
34: message CMsgTEBaseBeam
49: message CMsgTEBeamEntPoint
57: message CMsgTEBeamEnts
63: message CMsgTEBeamPoints
69: message CMsgTEBeamRing
75: message CMsgTEBubbles
83: message CMsgTEBubbleTrail
91: message CMsgTEDecal
99: message CMsgEffectData
121: message CMsgTEEffectDispatch
125: message CMsgTEEnergySplash
131: message CMsgTEFizz
137: message CMsgTEShatterSurface
150: message CMsgTEGlowSprite
157: message CMsgTEImpact
163: message CMsgTEMuzzleFlash
170: message CMsgTEBloodStream
177: message CMsgTEExplosion
192: message CMsgTEDust
199: message CMsgTELargeFunnel
204: message CMsgTESparks
211: message CMsgTEPhysicsProp
227: message CMsgTESmoke
232: message CMsgTEWorldDecal
```

</details>

<a id="uifontfile-format-proto"></a>
### uifontfile_format.proto

<details>
<summary><code>uifontfile_format.proto</code> — module: <code>uifontfile_format_pb2</code>; imports: 0; enums: 0; messages: 3</summary>

- Imports: *(none)*

```text
1: message CUIFontFilePB
6: message CUIFontFilePackagePB
7: message CUIEncryptedFontFilePB
```

</details>

<a id="usercmd-proto"></a>
### usercmd.proto

<details>
<summary><code>usercmd.proto</code> — module: <code>usercmd_pb2</code>; imports: 2; enums: 0; messages: 5</summary>

- Imports: valveextensions.proto, networkbasetypes.proto

```text
4: message CInButtonStatePB
12: message CSubtickMoveStep
24: message CBaseUserCmdExecutionNotes
30: message CBaseUserCmdPB
54: message CUserCmdBasePB
```

</details>

<a id="usermessages-proto"></a>
### usermessages.proto

<details>
<summary><code>usermessages.proto</code> — module: <code>usermessages_pb2</code>; imports: 1; enums: 5; messages: 107</summary>

- Imports: networkbasetypes.proto

```text
3: enum EBaseUserMessages
57: enum EBaseEntityMessages
65: enum eRollType
73: enum PARTICLE_MESSAGE
118: enum EHapticPulseType
124: message CUserMessageAchievementEvent
128: message CUserMessageCloseCaptionPlaceholder
135: message CUserMessageCurrentTimescale
139: message CUserMessageDesiredTimescale
146: message CUserMessageFade
153: message CUserMessageShake
160: message CUserMessageShakeDir
165: message CUserMessageWaterShake
172: message CUserMessageScreenTilt
180: message CUserMessageSayText
186: message CUserMessageSayText2
196: message CUserMessageHudMsg
206: message CUserMessageHudText
210: message CUserMessageTextMsg
215: message CUserMessageGameTitle
218: message CUserMessageResetHUD
221: message CUserMessageSendAudio
226: message CUserMessageAudioParameter
233: message CUserMessageVoiceMask
239: message CUserMessageRequestState
242: message CUserMessageRumble
248: message CUserMessageSayTextChannel
254: message CUserMessageColoredText
263: message CUserMessageItemPickup
267: message CUserMessageAmmoDenied
271: message CUserMessageShowMenu
278: message CUserMessageCreditsMsg
283: message CEntityMessagePlayJingle
287: message CEntityMessageScreenOverlay
292: message CEntityMessagePropagateForce
297: message CEntityMessageDoSpark
308: message CEntityMessageFixAngle
314: message CUserMessageCameraTransition
315: message Transition_DataDriven
326: message CUserMsg_ParticleManager
329: message ReleaseParticleIndex
332: message CreateParticle
345: message DestroyParticle
349: message DestroyParticleInvolving
354: message DestroyParticleNamed
361: message UpdateParticle_OBSOLETE
366: message UpdateParticleFwd_OBSOLETE
371: message UpdateParticleOrient_OBSOLETE
379: message UpdateParticleTransform
386: message UpdateParticleFallback
391: message UpdateParticleOffset
397: message UpdateParticleEnt
408: message UpdateParticleSetFrozen
413: message UpdateParticleShouldDraw
417: message ChangeControlPointAttachment
423: message UpdateEntityPosition
428: message SetParticleFoWProperties
434: message SetParticleShouldCheckFoW
438: message SetControlPointModel
443: message SetControlPointSnapshot
448: message SetParticleText
453: message SetTextureAttribute
458: message SetOverrideTexture
462: message SetSceneObjectGenericFlag
466: message SetSceneObjectTintAndDesat
471: message ParticleSkipToTime
475: message ParticleCanFreeze
479: message ParticleFreezeTransitionOverride
483: message FreezeParticleInvolving
489: message AddModellistOverrideElement
495: message ClearModellistOverride
499: message SetParticleNamedValueContext
500: message FloatContextValue
505: message VectorContextValue
510: message TransformContextValue
516: message EHandleContext
527: message CreatePhysicsSim
533: message DestroyPhysicsSim
536: message CreateSmokeGrid
540: message SetVData
544: message SetMaterialOverride
549: message AddFan
570: message UpdateFan
580: message RemoveFan
583: message SetParticleClusterGrowth
635: message CUserMsg_HudError
639: message CUserMsg_CustomGameEvent
644: message CUserMessageHapticsManagerPulse
651: message CUserMessageHapticsManagerEffect
657: message CUserMessageAnimStateGraphState
662: message CUserMessageUpdateCssClasses
668: message CUserMessageServerFrameTime
672: message CUserMessageLagCompensationError
676: message CUserMessageRequestDllStatus
681: message CUserMessageRequestUtilAction
689: message CUserMessage_UtilMsg_Response
690: message ItemDetail
711: message CUserMessage_DllStatus
712: message CVDiagnostic
719: message CModule
736: message CUserMessageRequestInventory
742: message CUserMessage_Inventory_Response
743: message InventoryDetail
771: message CUserMessageRequestDiagnostic
772: message Diagnostic
791: message CUserMessage_Diagnostic_Response
792: message Diagnostic
818: message CUserMessage_ExtraUserData
826: message CUserMessage_NotifyResponseFound
827: message Criteria
846: message CUserMessage_PlayResponseConditional
855: message CUserMessage_UsageReport
```

</details>

<a id="valveextensions-proto"></a>
### valveextensions.proto

<details>
<summary><code>valveextensions.proto</code> — module: <code>valveextensions_pb2</code>; imports: 1; enums: 1; messages: 0</summary>

- Imports: google/protobuf/descriptor.proto

```text
25: enum EProtoDebugVisiblity
```

</details>
