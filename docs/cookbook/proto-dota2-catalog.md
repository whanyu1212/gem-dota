# Full Proto Dota2 Catalog

This page catalogs the full Dota 2 proto surface used by gem.

- Source proto files: **78**
- Generated Python protobuf modules (`*_pb2.py`, including subdirectories): **78**

## Index

Use this list to jump directly to a file section:

- [base_gcmessages.proto](#base-gcmessages-proto) — imports: 3, enums: 6, messages: 62
- [c_peer2peer_netmessages.proto](#c-peer2peer-netmessages-proto) — imports: 2, enums: 2, messages: 7
- [clientmessages.proto](#clientmessages-proto) — imports: 0, enums: 2, messages: 7
- [connectionless_netmessages.proto](#connectionless-netmessages-proto) — imports: 1, enums: 0, messages: 3
- [demo.proto](#demo-proto) — imports: 0, enums: 1, messages: 27
- [dota_broadcastmessages.proto](#dota-broadcastmessages-proto) — imports: 0, enums: 1, messages: 4
- [dota_client_enums.proto](#dota-client-enums-proto) — imports: 1, enums: 7, messages: 0
- [dota_clientmessages.proto](#dota-clientmessages-proto) — imports: 3, enums: 4, messages: 116
- [dota_commonmessages.proto](#dota-commonmessages-proto) — imports: 1, enums: 4, messages: 13
- [dota_fighting_game_p2p_messages.proto](#dota-fighting-game-p2p-messages-proto) — imports: 2, enums: 1, messages: 6
- [dota_gcmessages_client.proto](#dota-gcmessages-client-proto) — imports: 10, enums: 86, messages: 475
- [dota_gcmessages_client_bingo.proto](#dota-gcmessages-client-bingo-proto) — imports: 9, enums: 10, messages: 25
- [dota_gcmessages_client_candy_shop.proto](#dota-gcmessages-client-candy-shop-proto) — imports: 9, enums: 9, messages: 34
- [dota_gcmessages_client_chat.proto](#dota-gcmessages-client-chat-proto) — imports: 1, enums: 2, messages: 27
- [dota_gcmessages_client_coaching.proto](#dota-gcmessages-client-coaching-proto) — imports: 2, enums: 17, messages: 35
- [dota_gcmessages_client_craftworks.proto](#dota-gcmessages-client-craftworks-proto) — imports: 10, enums: 4, messages: 8
- [dota_gcmessages_client_fantasy.proto](#dota-gcmessages-client-fantasy-proto) — imports: 1, enums: 13, messages: 59
- [dota_gcmessages_client_guild.proto](#dota-gcmessages-client-guild-proto) — imports: 1, enums: 26, messages: 61
- [dota_gcmessages_client_guild_events.proto](#dota-gcmessages-client-guild-events-proto) — imports: 1, enums: 7, messages: 22
- [dota_gcmessages_client_match_management.proto](#dota-gcmessages-client-match-management-proto) — imports: 5, enums: 1, messages: 62
- [dota_gcmessages_client_showcase.proto](#dota-gcmessages-client-showcase-proto) — imports: 9, enums: 20, messages: 60
- [dota_gcmessages_client_team.proto](#dota-gcmessages-client-team-proto) — imports: 1, enums: 6, messages: 28
- [dota_gcmessages_client_tournament.proto](#dota-gcmessages-client-tournament-proto) — imports: 1, enums: 1, messages: 20
- [dota_gcmessages_client_watch.proto](#dota-gcmessages-client-watch-proto) — imports: 1, enums: 2, messages: 23
- [dota_gcmessages_common.proto](#dota-gcmessages-common-proto) — imports: 4, enums: 29, messages: 187
- [dota_gcmessages_common_battle_report.proto](#dota-gcmessages-common-battle-report-proto) — imports: 7, enums: 13, messages: 23
- [dota_gcmessages_common_bot_script.proto](#dota-gcmessages-common-bot-script-proto) — imports: 1, enums: 2, messages: 18
- [dota_gcmessages_common_craftworks.proto](#dota-gcmessages-common-craftworks-proto) — imports: 3, enums: 1, messages: 3
- [dota_gcmessages_common_fighting_game.proto](#dota-gcmessages-common-fighting-game-proto) — imports: 4, enums: 2, messages: 8
- [dota_gcmessages_common_league.proto](#dota-gcmessages-common-league-proto) — imports: 1, enums: 2, messages: 37
- [dota_gcmessages_common_lobby.proto](#dota-gcmessages-common-lobby-proto) — imports: 3, enums: 5, messages: 32
- [dota_gcmessages_common_match_management.proto](#dota-gcmessages-common-match-management-proto) — imports: 3, enums: 9, messages: 15
- [dota_gcmessages_common_monster_hunter.proto](#dota-gcmessages-common-monster-hunter-proto) — imports: 4, enums: 16, messages: 36
- [dota_gcmessages_common_overworld.proto](#dota-gcmessages-common-overworld-proto) — imports: 5, enums: 19, messages: 51
- [dota_gcmessages_common_survivors.proto](#dota-gcmessages-common-survivors-proto) — imports: 4, enums: 1, messages: 5
- [dota_gcmessages_msgid.proto](#dota-gcmessages-msgid-proto) — imports: 0, enums: 1, messages: 0
- [dota_gcmessages_server.proto](#dota-gcmessages-server-proto) — imports: 14, enums: 6, messages: 186
- [dota_gcmessages_webapi.proto](#dota-gcmessages-webapi-proto) — imports: 5, enums: 14, messages: 38
- [dota_hud_types.proto](#dota-hud-types-proto) — imports: 1, enums: 1, messages: 0
- [dota_match_metadata.proto](#dota-match-metadata-proto) — imports: 10, enums: 2, messages: 38
- [dota_modifiers.proto](#dota-modifiers-proto) — imports: 1, enums: 1, messages: 2
- [dota_scenariomessages.proto](#dota-scenariomessages-proto) — imports: 1, enums: 0, messages: 23
- [dota_shared_enums.proto](#dota-shared-enums-proto) — imports: 0, enums: 54, messages: 14
- [dota_usercmd.proto](#dota-usercmd-proto) — imports: 2, enums: 0, messages: 1
- [dota_usermessages.proto](#dota-usermessages-proto) — imports: 3, enums: 19, messages: 190
- [econ_gcmessages.proto](#econ-gcmessages-proto) — imports: 4, enums: 15, messages: 143
- [econ_shared_enums.proto](#econ-shared-enums-proto) — imports: 0, enums: 3, messages: 1
- [engine_gcmessages.proto](#engine-gcmessages-proto) — imports: 1, enums: 0, messages: 1
- [enums_clientserver.proto](#enums-clientserver-proto) — imports: 0, enums: 6, messages: 0
- [gameevents.proto](#gameevents-proto) — imports: 1, enums: 1, messages: 16
- [gcsdk_gcmessages.proto](#gcsdk-gcmessages-proto) — imports: 3, enums: 3, messages: 74
- [gcsystemmsgs.proto](#gcsystemmsgs-proto) — imports: 0, enums: 2, messages: 0
- [netmessages.proto](#netmessages-proto) — imports: 1, enums: 13, messages: 82
- [network_connection.proto](#network-connection-proto) — imports: 1, enums: 1, messages: 0
- [networkbasetypes.proto](#networkbasetypes-proto) — imports: 2, enums: 3, messages: 27
- [networksystem_protomessages.proto](#networksystem-protomessages-proto) — imports: 0, enums: 0, messages: 5
- [prediction_events.proto](#prediction-events-proto) — imports: 1, enums: 1, messages: 3
- [steamdatagram_messages_auth.proto](#steamdatagram-messages-auth-proto) — imports: 1, enums: 0, messages: 7
- [steamdatagram_messages_sdr.proto](#steamdatagram-messages-sdr-proto) — imports: 2, enums: 10, messages: 42
- [steammessages.proto](#steammessages-proto) — imports: 1, enums: 2, messages: 5
- [steammessages_base.proto](#steammessages-base-proto) — imports: 1, enums: 4, messages: 21
- [steammessages_cloud.steamworkssdk.proto](#steammessages-cloud-steamworkssdk-proto) — imports: 1, enums: 0, messages: 9
- [steammessages_gamenetworkingui.proto](#steammessages-gamenetworkingui-proto) — imports: 2, enums: 0, messages: 5
- [steammessages_helprequest.steamworkssdk.proto](#steammessages-helprequest-steamworkssdk-proto) — imports: 1, enums: 0, messages: 2
- [steammessages_int.proto](#steammessages-int-proto) — imports: 1, enums: 3, messages: 82
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
- [usercmd.proto](#usercmd-proto) — imports: 1, enums: 0, messages: 5
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
<summary><code>clientmessages.proto</code> — module: <code>clientmessages_pb2</code>; imports: 0; enums: 2; messages: 7</summary>

- Imports: *(none)*

```text
1: enum EBaseClientMessages
12: enum EClientUIEvent
18: message CClientMsg_CustomGameEvent
23: message CClientMsg_CustomGameEventBounce
29: message CClientMsg_ClientUIEvent
37: message CClientMsg_DevPaletteVisibilityChangedEvent
41: message CClientMsg_WorldUIControllerHasPanelChangedEvent
47: message CClientMsg_RotateAnchor
51: message CClientMsg_ListenForResponseFound
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
<summary><code>demo.proto</code> — module: <code>demo_pb2</code>; imports: 0; enums: 1; messages: 27</summary>

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
176: message CDemoRecovery
177: message DemoInitialSpawnGroupEntry
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
<summary><code>dota_clientmessages.proto</code> — module: <code>dota_clientmessages_pb2</code>; imports: 3; enums: 4; messages: 116</summary>

- Imports: dota_commonmessages.proto, dota_shared_enums.proto, base_gcmessages.proto

```text
5: enum EDotaClientMessages
132: message CDOTAClientMsg_MapPing
136: message CDOTAClientMsg_ItemAlert
140: message CDOTAClientMsg_EnemyItemAlert
150: message CDOTAClientMsg_ModifierAlert
155: message CDOTAClientMsg_ClickedBuff
160: message CDOTAClientMsg_HPManaAlert
165: message CDOTAClientMsg_NeutralCampAlert
171: message CDOTAClientMsg_GlyphAlert
175: message CDOTAClientMsg_RadarAlert
179: message CDOTAClientMsg_MapLine
183: message CDOTAClientMsg_AspectRatio
187: message CDOTAClientMsg_UnitsAutoAttackMode
188: enum EMode
195: enum EUnitType
204: message CDOTAClientMsg_UnitsAutoAttackAfterSpell
208: message CDOTAClientMsg_TeleportRequiresHalt
212: message CDOTAClientMsg_ChannelRequiresHalt
216: message CDOTAClientMsg_InteractionChannelsRequireHalt
220: message CDOTAClientMsg_AbilitySpecificChannelRequiresHalt
226: message CDOTAClientMsg_SearchString
230: message CDOTAClientMsg_Pause
233: message CDOTAClientMsg_ShopViewMode
237: message CDOTAClientMsg_SetUnitShareFlag
243: message CDOTAClientMsg_SwapRequest
247: message CDOTAClientMsg_SwapAccept
251: message CDOTAClientMsg_WorldLine
255: message CDOTAClientMsg_RequestGraphUpdate
258: message CDOTAClientMsg_ChatWheel
264: message CDOTAClientMsg_SendStatPopup
268: message CDOTAClientMsg_DismissAllStatPopups
272: message CDOTAClientMsg_BeginLastHitChallenge
277: message CDOTAClientMsg_UpdateQuickBuyItem
283: message CDOTAClientMsg_UpdateQuickBuy
288: message CDOTAClientMsg_QuickBuyAction
289: enum EActionType
313: message CDOTAClientMsg_RecordVote
317: message CDOTAClientMsg_WillPurchaseAlert
323: message CDOTAClientMsg_BuyBackStateAlert
326: message CDOTAClientMsg_QuickBuyAlert
333: message CDOTAClientMsg_PlayerShowCase
337: message CDOTAClientMsg_CameraZoomAmount
341: message CDOTAClientMsg_BroadcasterUsingCameraman
345: message CDOTAClientMsg_BroadcasterUsingAssistedCameraOperator
349: message CDOTAClientMsg_FillEmptySlotsWithBots
353: message CDOTAClientMsg_HeroStatueLike
357: message CDOTAClientMsg_EventCNY2015Cmd
361: message CDOTAClientMsg_DemoHero
362: message PreviewItem
377: message CDOTAClientMsg_ChallengeSelect
383: message CDOTAClientMsg_ChallengeReroll
390: message CDOTAClientMsg_CoinWager
394: message CDOTAClientMsg_CoinWagerToken
398: message CDOTAClientMsg_RankWager
402: message CDOTAClientMsg_PlayerBounty
406: message CDOTAClientMsg_EventPointsTip
410: message CDOTAClientMsg_ExecuteOrders
415: message CDOTAClientMsg_XPAlert
420: message CDOTAClientMsg_TalentTreeAlert
427: message CDOTAClientMsg_KillcamDamageTaken
436: message CDOTAClientMsg_KillMyHero
439: message CDOTAClientMsg_QuestStatus
449: message CDOTAClientMsg_ToggleAutoattack
454: message CDOTAClientMsg_SpecialAbility
459: message CDOTAClientMsg_SetEnemyStartingPosition
464: message CDOTAClientMsg_SetDesiredWardPlacement
470: message CDOTAClientMsg_RollDice
476: message CDOTAClientMsg_FlipCoin
480: message CDOTAClientMsg_RequestItemSuggestions
483: message CDOTAClientMsg_SuggestItemPreference
484: message ItemPreference
492: message CDOTAClientMsg_SuggestItemRefresh
496: message CDOTAClientMsg_SuggestItemGetVariants
500: message CDOTAClientMsg_SuggestItemSelectVariant
504: message CDOTAClientMsg_MakeTeamCaptain
508: message CDOTAClientMsg_HelpTipSystemStateChanged
512: message CDOTAClientMsg_RequestBulkCombatLog
519: message CDOTAClientMsg_AbilityDraftRequestAbility
526: message CDOTAClientMsg_GuideSelectOption
531: message CDOTAClientMsg_GuideSelected
536: message CDOTAClientMsg_DamageReport
543: message CDOTAClientMsg_SalutePlayer
548: message CDOTAClientMsg_GiftPlayer
553: message CDOTAClientMsg_GiftEveryone
557: message CDOTAClientMsg_TipAlert
561: message CDOTAClientMsg_EmptyTeleportAlert
565: message CDOTAClientMsg_SetCavernMapVariant
569: message CDOTAClientMsg_PauseGameOrder
574: message CDOTAClientMsg_VersusScene_PlayerBehavior
581: message CDOTAClientMsg_EmptyItemSlotAlert
586: message CDOTAClientMsg_AddOverwatchReportMarker
592: message CDOTAClientMsg_AddCommunicationsReportMarker
596: message CDOTAClientMsg_AddCommunicationsBlockMarker
600: message CDOTAClientMsg_AghsStatusAlert
607: message CDOTAClientMsg_PerfReport
630: message CDOTAClientMsg_ContextualTips_Subscribe_Entry
637: message CDOTAClientMsg_ContextualTips_Subscribe
641: message CDOTAClientMsg_ChatMessage
646: message CDOTAClientMsg_DuelAccepted
651: message CDOTAClientMsg_ChooseNeutralItem
657: message CDOTAClientMsg_RerollNeutralItem
662: message CDOTAClientMsg_PlayerDraftPick
666: message CDOTAClientMsg_PlayerDraftSuggest
670: message CDOTAClientMsg_PlayerDraftPreferRole
675: message CDOTAClientMsg_PlayerDraftPreferTeam
679: message CDOTAClientMsg_AbilityAlert
689: message CDOTAClientMsg_SelectOverworldTokenRewards
693: message CDOTAClientMsg_FacetAlert
699: message CDOTAClientMsg_InnateAlert
704: message CDOTAClientMsg_SelectOverworldID
708: message CDOTAClientMsg_RoshanTimer
712: message CDOTAClientMsg_TormentorTimer
716: message CDOTAClientMsg_CraftNeutralItem
719: message CDOTAClientMsg_ChooseCraftedNeutralItem
725: message CDOTAClientMsg_TimerAlert
729: message CDOTAClientMsg_MadstoneAlert
733: message CDOTAClientMsg_UpdateAutoCourierSettings
737: message CDOTAClientMsg_AutoCourierExecute
742: message CDOTAClientMsg_MonsterHunter_SelectInvestigation
746: message CDOTAClientMsg_MonsterHunter_HuntAlert
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
1327: message CMsgDOTARedeemItemResponse
1328: enum EResultCode
1336: message CMsgClientToGCSelectCompendiumInGamePrediction
1337: message Prediction
1347: message CMsgClientToGCSelectCompendiumInGamePredictionResponse
1348: enum EResult
1358: message CMsgClientToGCOpenPlayerCardPack
1365: message CMsgClientToGCOpenPlayerCardPackResponse
1366: enum Result
1380: message CMsgClientToGCRecyclePlayerCard
1385: message CMsgClientToGCRecyclePlayerCardResponse
1386: enum Result
1400: message CMsgClientToGCCreatePlayerCardPack
1406: message CMsgClientToGCCreatePlayerCardPackResponse
1407: enum Result
1420: message CMsgClientToGCCreateTeamPlayerCardPack
1427: message CMsgClientToGCCreateTeamPlayerCardPackResponse
1428: enum Result
1441: message CMsgGCToClientBattlePassRollup_International2016
1442: message Questlines
1450: message Wagering
1458: message Achievements
1464: message BattleCup
1469: message Predictions
1475: message Bracket
1480: message PlayerCard
1485: message FantasyChallenge
1501: message CMsgGCToClientBattlePassRollup_Fall2016
1502: message Questlines
1510: message Wagering
1518: message Achievements
1524: message BattleCup
1529: message Predictions
1535: message Bracket
1540: message PlayerCard
1545: message FantasyChallenge
1561: message CMsgGCToClientBattlePassRollup_Winter2017
1562: message Questlines
1570: message Wagering
1578: message Achievements
1584: message BattleCup
1589: message Predictions
1595: message Bracket
1600: message PlayerCard
1605: message FantasyChallenge
1621: message CMsgGCToClientBattlePassRollup_TI7
1622: message Questlines
1630: message Wagering
1638: message Achievements
1644: message BattleCup
1649: message Predictions
1655: message Bracket
1660: message PlayerCard
1665: message FantasyChallenge
1681: message CMsgGCToClientBattlePassRollup_TI8
1682: message CavernCrawl
1689: message Wagering
1697: message Achievements
1703: message Predictions
1709: message Bracket
1714: message PlayerCard
1719: message FantasyChallenge
1734: message CMsgGCToClientBattlePassRollup_TI9
1738: message CMsgGCToClientBattlePassRollup_TI10
1742: message CMsgGCToClientBattlePassRollupRequest
1747: message CMsgGCToClientBattlePassRollupResponse
1757: message CMsgGCToClientBattlePassRollupListRequest
1761: message CMsgGCToClientBattlePassRollupListResponse
1762: message EventInfo
1770: message CMsgClientToGCTransferSeasonalMMRRequest
1774: message CMsgClientToGCTransferSeasonalMMRResponse
1778: message CMsgGCToClientPlaytestStatus
1782: message CMsgClientToGCJoinPlaytest
1786: message CMsgClientToGCJoinPlaytestResponse
1790: message CMsgDOTASetFavoriteTeam
1795: message CMsgDOTATriviaCurrentQuestions
1800: message CMsgDOTASubmitTriviaQuestionAnswer
1805: message CMsgDOTASubmitTriviaQuestionAnswerResponse
1809: message CMsgDOTAStartTriviaSession
1812: message CMsgDOTAStartTriviaSessionResponse
1817: message CMsgDOTAAnchorPhoneNumberRequest
1820: message CMsgDOTAAnchorPhoneNumberResponse
1821: enum Result
1833: message CMsgDOTAUnanchorPhoneNumberRequest
1836: message CMsgDOTAUnanchorPhoneNumberResponse
1837: enum Result
1845: message CMsgGCToClientCommendNotification
1852: message CMsgDOTAClientToGCQuickStatsRequest
1859: message CMsgDOTAClientToGCQuickStatsResponse
1860: message SimpleStats
1876: message CMsgDOTASelectionPriorityChoiceRequest
1880: message CMsgDOTASelectionPriorityChoiceResponse
1881: enum Result
1889: message CMsgDOTAGameAutographReward
1893: message CMsgDOTAGameAutographRewardResponse
1894: enum Result
1902: message CMsgDOTADestroyLobbyRequest
1905: message CMsgDOTADestroyLobbyResponse
1906: enum Result
1914: message CMsgDOTAGetRecentPlayTimeFriendsRequest
1917: message CMsgDOTAGetRecentPlayTimeFriendsResponse
1921: message CMsgPurchaseItemWithEventPoints
1928: message CMsgPurchaseItemWithEventPointsResponse
1929: enum Result
1949: message CMsgPurchaseHeroRandomRelic
1954: message CMsgPurchaseHeroRandomRelicResponse
1959: message CMsgClientToGCRequestPlusWeeklyChallengeResult
1964: message CMsgClientToGCRequestPlusWeeklyChallengeResultResponse
1967: message CMsgProfileRequest
1971: message CMsgProfileResponse
1972: message FeaturedHero
1980: message MatchInfo
1988: enum EResponse
2004: message CMsgProfileUpdate
2009: message CMsgProfileUpdateResponse
2010: enum Result
2021: message CMsgTalentWinRates
2028: message CMsgGlobalHeroAverages
2040: message CMsgHeroGlobalDataRequest
2044: message CMsgHeroGlobalDataResponse
2045: message GraphData
2052: message WeekData
2059: message HeroDataPerRankChunk
2071: message CMsgHeroGlobalDataAllHeroes
2075: message CMsgHeroGlobalDataHeroesAlliesAndEnemies
2076: message HeroData
2084: message RankedHeroData
2092: message CMsgPrivateMetadataKeyRequest
2096: message CMsgPrivateMetadataKeyResponse
2100: message CMsgActivatePlusFreeTrialResponse
2101: enum Result
2112: message CMsgGCToClientCavernCrawlMapPathCompleted
2113: message CompletedPathInfo
2125: message CMsgGCToClientCavernCrawlMapUpdated
2129: message CMsgClientToGCCavernCrawlClaimRoom
2135: message CMsgClientToGCCavernCrawlClaimRoomResponse
2136: enum Result
2145: message CMsgClientToGCCavernCrawlUseItemOnRoom
2152: message CMsgClientToGCCavernCrawlUseItemOnRoomResponse
2153: enum Result
2162: message CMsgClientToGCCavernCrawlUseItemOnPath
2169: message CMsgClientToGCCavernCrawlUseItemOnPathResponse
2170: enum Result
2179: message CMsgClientToGCCavernCrawlRequestMapState
2183: message CMsgClientToGCCavernCrawlRequestMapStateResponse
2184: message SwappedChallenge
2189: message InventoryItem
2194: message TreasureMap
2199: message MapVariant
2218: enum Result
2230: message CMsgClientToGCCavernCrawlGetClaimedRoomCount
2234: message CMsgClientToGCCavernCrawlGetClaimedRoomCountResponse
2235: message MapVariant
2240: enum Result
2251: message CMsgDOTAMutationList
2252: message Mutation
2261: message CMsgEventTipsSummaryRequest
2266: message CMsgEventTipsSummaryResponse
2267: message Tipper
2276: message CMsgSocialFeedRequest
2281: message CMsgSocialFeedResponse
2282: message FeedEvent
2296: enum Result
2309: message CMsgSocialFeedCommentsRequest
2313: message CMsgSocialFeedCommentsResponse
2314: message FeedComment
2320: enum Result
2330: message CMsgClientToGCPlayerCardSpecificPurchaseRequest
2336: message CMsgClientToGCPlayerCardSpecificPurchaseResponse
2337: enum Result
2350: message CMsgClientToGCRequestContestVotes
2354: message CMsgClientToGCRequestContestVotesResponse
2355: message ItemVote
2360: enum EResponse
2371: message CMsgClientToGCRecordContestVote
2377: message CMsgGCToClientRecordContestVoteResponse
2378: enum EResult
2390: message CMsgDevGrantEventPoints
2396: message CMsgDevGrantEventPointsResponse
2400: message CMsgDevGrantEventAction
2406: message CMsgDevGrantEventActionResponse
2410: message CMsgDevDeleteEventActions
2417: message CMsgDevDeleteEventActionsResponse
2421: message CMsgDevResetEventState
2426: message CMsgDevResetEventStateResponse
2430: message CMsgDevReloadAllEvents
2433: message CMsgDevReloadAllEventsResponse
2437: message CMsgConsumeEventSupportGrantItem
2441: message CMsgConsumeEventSupportGrantItemResponse
2445: message CMsgClientToGCGetFilteredPlayers
2448: message CMsgGCToClientGetFilteredPlayersResponse
2449: message CFilterEntry
2456: enum Result
2468: message CMsgClientToGCRemoveFilteredPlayer
2472: message CMsgGCToClientRemoveFilteredPlayerResponse
2473: enum Result
2481: message CMsgClientToGCPurchaseFilteredPlayerSlot
2485: message CMsgGCToClientPurchaseFilteredPlayerSlotResponse
2486: enum Result
2498: message CMsgClientToGCUpdateFilteredPlayerNote
2503: message CMsgGCToClientUpdateFilteredPlayerNoteResponse
2504: enum Result
2513: message CMsgPartySearchPlayer
2519: message CMsgGCToClientPlayerBeaconState
2523: message CMsgGCToClientPartyBeaconUpdate
2529: message CMsgClientToGCUpdatePartyBeacon
2530: enum Action
2538: message CMsgClientToGCRequestActiveBeaconParties
2541: message CMsgGCToClientRequestActiveBeaconPartiesResponse
2542: enum EResponse
2552: message CMsgClientToGCJoinPartyFromBeacon
2558: message CMsgGCToClientJoinPartyFromBeaconResponse
2559: enum EResponse
2569: message CMsgClientToGCManageFavorites
2570: enum Action
2583: message CMsgGCToClientManageFavoritesResponse
2584: enum EResponse
2598: message CMsgClientToGCGetFavoritePlayers
2603: message CMsgGCToClientGetFavoritePlayersResponse
2604: enum EResponse
2614: message CMsgGCToClientPartySearchInvite
2618: message CMsgClientToGCVerifyFavoritePlayers
2622: message CMsgGCToClientVerifyFavoritePlayersResponse
2623: message Result
2631: message CMsgClientToGCRequestPlayerRecentAccomplishments
2635: message CMsgClientToGCRequestPlayerRecentAccomplishmentsResponse
2636: enum EResponse
2647: message CMsgClientToGCRequestPlayerHeroRecentAccomplishments
2652: message CMsgClientToGCRequestPlayerHeroRecentAccomplishmentsResponse
2653: enum EResponse
2664: message CMsgClientToGCSubmitPlayerMatchSurvey
2670: message CMsgClientToGCSubmitPlayerMatchSurveyResponse
2671: enum EResponse
2684: message CMsgGCToClientVACReminder
2687: message CMsgClientToGCUnderDraftRequest
2692: message CMsgClientToGCUnderDraftResponse
2699: message CMsgClientToGCUnderDraftReroll
2703: message CMsgClientToGCUnderDraftRerollResponse
2709: message CMsgClientToGCUnderDraftBuy
2714: message CMsgGCToClientGuildUnderDraftGoldUpdated
2718: message CMsgClientToGCUnderDraftBuyResponse
2725: message CMsgClientToGCUnderDraftRollBackBench
2729: message CMsgClientToGCUnderDraftRollBackBenchResponse
2735: message CMsgClientToGCUnderDraftSell
2740: message CMsgClientToGCUnderDraftSellResponse
2747: message CMsgClientToGCUnderDraftRedeemReward
2752: message CMsgClientToGCUnderDraftRedeemRewardResponse
2756: message CMsgClientToGCSubmitDraftTriviaMatchAnswer
2762: message CMsgClientToGCSubmitDraftTriviaMatchAnswerResponse
2766: message CMsgDraftTriviaVoteCount
2772: message CMsgClientToGCRequestReporterUpdates
2775: message CMsgClientToGCRequestReporterUpdatesResponse
2776: message ReporterUpdate
2783: enum EResponse
2799: message CMsgClientToGCAcknowledgeReporterUpdates
2803: message CMsgClientToGCRecalibrateMMR
2806: message CMsgClientToGCRecalibrateMMRResponse
2807: enum EResponse
2820: message CMsgDOTAPostGameItemAwardNotification
2826: message CMsgClientToGCGetOWMatchDetails
2829: message CMsgClientToGCGetOWMatchDetailsResponse
2830: message Marker
2835: enum EResponse
2857: message CMsgClientToGCSubmitOWConviction
2864: message CMsgClientToGCSubmitOWConvictionResponse
2865: enum EResponse
2880: message CMsgClientToGCChinaSSAURLRequest
2883: message CMsgClientToGCChinaSSAURLResponse
2887: message CMsgClientToGCChinaSSAAcceptedRequest
2890: message CMsgClientToGCChinaSSAAcceptedResponse
2894: message CMsgGCToClientOverwatchCasesAvailable
2898: message CMsgClientToGCStartWatchingOverwatch
2903: message CMsgClientToGCStopWatchingOverwatch
2908: message CMsgClientToGCOverwatchReplayError
2912: message CMsgClientToGCGetDPCFavorites
2915: message CMsgClientToGCGetDPCFavoritesResponse
2916: message Favorite
2921: enum EResponse
2934: message CMsgClientToGCSetDPCFavoriteState
2940: message CMsgClientToGCSetDPCFavoriteStateResponse
2941: enum EResponse
2956: message CMsgClientToGCSetEventActiveSeasonID
2961: message CMsgClientToGCSetEventActiveSeasonIDResponse
2962: enum EResponse
2975: message CMsgClientToGCPurchaseLabyrinthBlessings
2982: message CMsgClientToGCPurchaseLabyrinthBlessingsResponse
2983: enum EResponse
2995: message CMsgClientToGCGetStickerbookRequest
2999: message CMsgClientToGCGetStickerbookResponse
3000: enum EResponse
3012: message CMsgClientToGCCreateStickerbookPageRequest
3018: message CMsgClientToGCCreateStickerbookPageResponse
3019: enum EResponse
3031: message CMsgClientToGCDeleteStickerbookPageRequest
3037: message CMsgClientToGCDeleteStickerbookPageResponse
3038: enum EResponse
3051: message CMsgClientToGCPlaceStickersRequest
3052: message StickerItem
3060: message CMsgClientToGCPlaceStickersResponse
3061: enum EResponse
3076: message CMsgClientToGCPlaceCollectionStickersRequest
3077: message Slot
3088: message CMsgClientToGCPlaceCollectionStickersResponse
3089: enum EResponse
3106: message CMsgClientToGCOrderStickerbookTeamPageRequest
3110: message CMsgClientToGCOrderStickerbookTeamPageResponse
3111: enum EResponse
3123: message CMsgClientToGCSetHeroSticker
3129: message CMsgClientToGCSetHeroStickerResponse
3130: enum EResponse
3143: message CMsgClientToGCGetHeroStickers
3146: message CMsgClientToGCGetHeroStickersResponse
3147: enum EResponse
3158: message CMsgClientToGCSetFavoritePage
3163: message CMsgClientToGCSetFavoritePageResponse
3164: enum EResponse
3175: message CMsgClientToGCClaimSwag
3181: message CMsgClientToGCClaimSwagResponse
3182: enum EResponse
3198: message CMsgClientToGCCollectorsCacheAvailableDataRequest
3202: message CMsgGCToClientCollectorsCacheAvailableDataResponse
3203: message Vote
3204: enum EVoteType
3216: message CMsgClientToGCUploadMatchClip
3220: message CMsgGCToClientUploadMatchClipResponse
3221: enum EResponse
3231: message CMsgClientToGCMapStatsRequest
3234: message CMsgGCToClientMapStatsResponse
3235: enum EResponse
3245: message CMsgRoadToTIAssignedQuest
3253: message CMsgRoadToTIUserData
3257: message CMsgClientToGCRoadToTIGetQuests
3261: message CMsgClientToGCRoadToTIGetQuestsResponse
3262: enum EResponse
3275: message CMsgClientToGCRoadToTIGetActiveQuest
3279: message CMsgClientToGCRoadToTIGetActiveQuestResponse
3280: enum EResponse
3294: message CMsgGCToClientRoadToTIQuestDataUpdated
3299: message CMsgClientToGCRoadToTIUseItem
3305: message CMsgClientToGCRoadToTIUseItemResponse
3306: enum EResponse
3319: message CMsgClientToGCRoadToTIDevForceQuest
3325: message CMsgLobbyRoadToTIMatchQuestData
3331: message CMsgClientToGCNewBloomGift
3337: message CMsgClientToGCNewBloomGiftResponse
3342: message CMsgClientToGCSetBannedHeroes
3346: message CMsgClientToGCUpdateComicBookStats
3347: message SingleStat
3352: message LanguageStats
3363: message CMsgGCRankedPlayerInfoSubmit
3367: message CMsgGCRankedPlayerInfoSubmitResponse
3368: enum EResult
3376: message CMsgDOTAClaimGatedEvent
3380: message CMsgDOTAClaimGatedEventResponse
3381: enum ResultCode
3394: message CMsgClientToGCGetEventRanking
3399: message CMsgClientToGCGetEventRankingResponse
3407: message CMsgClientToGCGetEventCoupon
3412: message CMsgClientToGCGetEventCouponResponse
3413: message Coupon
3418: enum ResultCode
3433: message CMsgClientToGCConvertEventPoints
3440: message CMsgClientToGCConvertEventPointsResponse
3441: enum ResultCode
3453: message CMsgClientToGCInviteToDemoMode
3458: message CMsgGCToClientInviteToDemoMode
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
<summary><code>dota_gcmessages_client_fantasy.proto</code> — module: <code>dota_gcmessages_client_fantasy_pb2</code>; imports: 1; enums: 13; messages: 59</summary>

- Imports: dota_shared_enums.proto

```text
3: enum DOTA_2013PassportSelectionIndices
102: message CMsgDOTAPlayerInfo
103: message Results
109: message AuditEntry
118: message ProRegistration
141: message CMsgDOTAPlayerInfoList
145: message CMsgDOTATeamRoster
152: message CMsgDOTADPCProfileInfo
153: message PredictionInfo
158: message FantasyInfo
171: message CMsgDOTALeaderboards
172: message RegionLeaderboard
180: message CMsgDOTAPassportVoteTeamGuess
186: message CMsgDOTAPassportVoteGenericSelection
191: message CMsgDOTAPassportStampedPlayer
196: message CMsgDOTAPassportPlayerCardChallenge
200: message CMsgDOTAPassportVote
207: message CMsgClientToGCGetPlayerCardRosterRequest
212: message CMsgClientToGCGetPlayerCardRosterResponse
213: enum Result
227: message CMsgClientToGCBatchGetPlayerCardRosterRequest
228: message LeagueTimestamp
236: message CMsgClientToGCBatchGetPlayerCardRosterResponse
237: message RosterResponse
248: enum Result
258: message CMsgClientToGCSetPlayerCardRosterRequest
267: message CMsgClientToGCSetPlayerCardRosterResponse
268: enum Result
285: message CMsgDOTAFantasyDPCLeagueStatus
286: message LeagueInfo
295: enum ERosterStatus
305: message CMsgDOTADPCSearchResults
306: message Player
312: message Team
318: message League
323: enum ESearchResultsDesired
335: message CMsgDOTADPCTeamFavoriteRankings
336: message Team
344: message CMsgDotaFantasyCraftingTabletPeriodData
345: message Gem
353: message Tablet
369: message CMsgDotaFantasyCraftingTabletData
370: message TabletPeriodDataEntry
378: message CMsgDotaFantasyCraftingUserData
379: message PeriodScore
384: message PeriodRollTokensEntry
389: message PeriodScoresEntry
399: message CMsgDotaFantasyCraftingDataCache
400: message CacheEntry
409: message CMsgClientToGCFantasyCraftingGetData
414: message CMsgClientToGCFantasyCraftingGetDataResponse
415: enum EResponse
429: message CMsgClientToGCFantasyCraftingPerformOperation
436: message CMsgClientToGCFantasyCraftingPerformOperationResponse
437: message TitleChoice
442: enum EResponse
464: message CMsgGCToClientFantasyCraftingDataUpdated
470: message CMsgClientToGCFantasyCraftingDevModifyTablet
478: message CMsgClientToGCFantasyCraftingDevModifyTabletResponse
479: enum EResponse
493: message CMsgClientToGCFantasyCraftingSelectPlayer
498: message CMsgClientToGCFantasyCraftingSelectPlayerResponse
499: enum EResponse
513: message CMsgClientToGCFantasyCraftingGenerateTablets
518: message CMsgClientToGCFantasyCraftingGenerateTabletsResponse
519: enum EResponse
534: message CMsgClientToGcFantasyCraftingUpgradeTablets
538: message CMsgClientToGcFantasyCraftingUpgradeTabletsResponse
539: enum EResponse
552: message CMsgClientToGCFantasyCraftingRerollOptions
556: message CMsgClientToGCFantasyCraftingRerollOptionsResponse
557: enum EResponse
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
<summary><code>dota_gcmessages_common.proto</code> — module: <code>dota_gcmessages_common_pb2</code>; imports: 4; enums: 29; messages: 187</summary>

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
301: message CMatchTeamTimedStats
309: message CMatchAdditionalUnitInventory
314: message CMatchPlayerPermanentBuff
320: message CMatchHeroSelectEvent
326: message CMatchClip
338: message CPartySearchClientParty
344: message CMsgDOTAHasItemQuery
349: message CMsgDOTAHasItemResponse
353: message CMsgGCGetPlayerCardItemInfo
359: message CMsgGCGetPlayerCardItemInfoResponse
360: message PlayerCardInfo
369: message CSODOTAMapLocationState
375: message CMsgLeagueAdminList
379: message CMsgDOTAProfileCard
380: message Slot
381: message Trophy
386: message Stat
391: message Item
396: message Hero
402: message Emoticon
406: message Team
419: enum EStatID
445: message CSODOTAPlayerChallenge
465: message CMsgClientToGCRerollPlayerChallenge
471: message CMsgGCRerollPlayerChallengeResponse
472: enum EResult
483: message CMsgGCTopCustomGamesList
488: message CMsgDOTARealtimeGameStats
489: message TeamDetails
503: message ItemDetails
511: message AbilityDetails
519: message HeroToHeroStats
525: message AbilityList
529: message PlayerDetails
582: message BuildingDetails
593: message KillDetails
599: message BroadcasterDetails
603: message PickBanDetails
608: message MatchDetails
632: message GraphData
633: message LocationStats
637: message TeamLocationStats
641: enum eStat
648: enum eLocation
672: message CMsgDOTARealtimeGameStatsTerse
673: message TeamDetails
685: message PlayerDetails
706: message BuildingDetails
717: message PickBanDetails
722: message MatchDetails
739: message GraphData
750: message CMsgDOTABroadcastTimelineEvent
757: message CMsgGCToClientMatchGroupsVersion
761: message CMsgDOTASDOHeroStatsHistory
774: message CMsgPredictionChoice
781: message CMsgInGamePrediction
782: message QueryKeyValues
787: enum ERawValueType_t
792: enum EPredictionType
802: enum EResolutionType_t
814: enum ERandomSelectionGroup_t
837: message CMsgDOTASeasonPredictions
838: message Prediction
839: message Answers
843: enum EPredictionType
854: enum EAnswerType
893: message CMsgAvailablePredictions
894: message MatchPrediction
902: message CMsgLeagueWatchedGames
903: message Series
908: message League
916: message CMsgDOTAMatch
919: message Player
920: message CustomGameData
925: message HeroDamageReceived
931: enum HeroDamageType
1016: message BroadcasterInfo
1021: message BroadcasterChannel
1028: message Coach
1037: message CustomGameData
1042: enum ReplayState
1098: message CMsgPlayerCard
1099: message StatModifier
1108: message CMsgDOTAFantasyPlayerStats
1138: message CMsgDOTAFantasyPlayerMatchStats
1142: message CMsgDOTABotDebugInfo
1143: message Bot
1144: message Mode
1153: message Action
1187: message CMsgSuccessfulHero
1193: message CMsgRecentMatchInfo
1207: message CMsgMatchTips
1208: message SingleTip
1218: message CMsgDOTAMatchMinimal
1219: message Player
1232: message Tourney
1263: message CMsgConsumableUsage
1268: message CMsgMatchConsumableUsage
1269: message PlayerUsage
1277: message CMsgMatchEventActionGrants
1278: message PlayerGrants
1286: message CMsgCustomGameWhitelist
1292: message CMsgCustomGameWhitelistForEdit
1293: message WhitelistEntry
1301: message CMsgPlayerRecentMatchInfo
1312: message CMsgPlayerMatchRecord
1317: message CMsgPlayerRecentMatchOutcomes
1322: message CMsgPlayerRecentCommends
1327: message CMsgPlayerRecentAccomplishments
1338: message CMsgPlayerHeroRecentAccomplishments
1344: message CMsgRecentAccomplishments
1349: message CMsgServerToGCRequestPlayerRecentAccomplishments
1354: message CMsgServerToGCRequestPlayerRecentAccomplishmentsResponse
1355: enum EResponse
1366: message CMsgArcanaVoteMatchVotes
1372: message CMsgGCtoGCAssociatedExploiterAccountInfo
1379: message CMsgGCtoGCAssociatedExploiterAccountInfoResponse
1380: message Account
1393: message CMsgPullTabsData
1394: message Slot
1402: message Jackpot
1413: message CMsgUnderDraftData
1414: message BenchSlot
1420: message ShopSlot
1433: message CMsgPlayerTitleData
1439: message CMsgDOTATriviaQuestion
1448: message CMsgDOTATriviaQuestionAnswersSummary
1453: message CMsgGameDataSpecialValueBonus
1459: message CMsgGameDataSpecialValues
1471: message CMsgGameDataFacetAbilityBonus
1477: message CMsgGameDataAbilityOrItem
1520: message CMsgGameDataAbilityOrItemList
1524: message CMsgGameDataHero
1525: message Facet
1573: message CMsgGameDataAbilities
1577: message CMsgGameDataItems
1581: message CMsgGameDataHeroes
1585: message CMsgGameDataHeroList
1586: message HeroInfo
1598: message CMsgGameDataItemAbilityList
1599: message ItemAbilityInfo
1600: message Recipe
1618: message CMsgLobbyAbilityDraftData
1622: message CSOEconItemDropRateBonus
1633: message CSOEconItemTournamentPassport
1644: message CMsgStickerbookSticker
1657: message CMsgStickerbookPage
1665: message CMsgStickerbookTeamPageOrderSequence
1669: message CMsgStickerbook
1675: message CMsgStickerHero
1682: message CMsgStickerHeroes
1686: message CMsgHeroRoleStats
1692: message CMsgHeroRoleHeroStats
1697: message CMsgHeroRoleRankStats
1702: message CMsgHeroRoleAllRanksStats
1708: message CMsgMapStatsSnapshot
1721: message CMsgGlobalMapStats
1727: message CMsgTrackedStat
1732: message CMsgDOTAClaimEventActionResponse
1733: message MysteryItemRewardData
1738: message LootListRewardData
1742: message ActionListRewardData
1747: message OverworldTokenRewardData
1748: message TokenQuantity
1756: message MonsterHunterMaterialRewardData
1757: message MaterialQuantity
1765: message GrantedRewardData
1773: enum ResultCode
1796: message CMsgClientToGCDotaLabsFeedback
1802: message CMsgClientToGCDotaLabsFeedbackResponse
1803: enum EResponse
1816: message CDotaMsg_PredictionResult
1817: message Prediction
1818: enum EResult
1836: message CDotaMsgStructuredTooltipProperties
1837: message AttributeValueValue
1842: message AttributeValue_Single
1846: message AttributeValue_Variable
1850: message AttributeValue_Delta
1855: message AttributeValue
1863: message FacetDisplayProperties
1871: message Attribute
1878: message AttributeGroupDesc_Basic
1881: message AttributeGroupDesc_Specific
1886: message AttributeGroupDesc_Facet
1890: message AttributeGroupDescription
1898: message AttributeGroup
1903: message ContentChunk_AttributeGroup
1907: message TooltipContentChunk
1913: message SummaryDescriptionEmbedValue
1919: enum EAttributeType
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
30: message VOD
58: message CMsgDOTALeagueNodeGroup
59: message TeamStanding
106: message CMsgDOTALeague
107: message Info
124: message Admin
130: message PrizePoolItem
137: message PrizePool
144: message Stream
153: message SeriesInfo
162: message Player
177: message CMsgDOTALeagueList
181: message CMsgDOTALeagueInfo
193: message CMsgDOTALeagueInfoList
197: message CMsgDOTALeagueLiveGames
198: message LiveGame
217: message CMsgDOTALeagueMessages
218: message Message
227: message CMsgDOTALeaguePrizePool
232: message CMsgDOTALeagueInfoListAdminsRequest
235: message CMsgDOTALeagueAvailableLobbyNodesRequest
239: message CMsgDOTALeagueAvailableLobbyNodes
240: message NodeInfo
251: message CMsgDOTALeagueNodeResults
252: message Result
275: message CMsgDOTADPCLeagueResults
276: message Result
294: message CMsgDOTADPCTeamResults
295: message Result
306: message CMsgDOTADPCSeasonResults
307: message TeamLeagueResult
317: message TeamResult
328: message StandingEntry
337: message Standing
350: message CMsgDOTADPCSeasonSpoilerResults
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
18: enum LobbyDotaPauseSetting
24: message CMsgLobbyCoachFriendRequest
30: message CMsgLobbyPlayerPlusSubscriptionData
31: message HeroBadge
39: message CMsgEventActionData
44: message CMsgPeriodicResourceData
50: message CMsgLobbyEventPoints
51: message AccountPoints
72: message CMsgLobbyEventGameData
77: message CSODOTALobbyInvite
78: message LobbyMember
93: message CSODOTALobbyMember
110: message CSODOTAServerLobbyMember
113: message CSODOTAStaticLobbyMember
120: message CSODOTAServerStaticLobbyMember
141: message CLobbyTeamDetails
158: message CLobbyGuildDetails
172: message CLobbyTimedRewardDetails
180: message CLobbyBroadcastChannelInfo
187: message CLobbyGuildChallenge
198: message CDOTALobbyMatchQualityData
205: message CSODOTALobby
206: message CExtraMsg
211: enum State
221: enum LobbyType
329: message CSODOTAServerLobby
335: message CSODOTAStaticLobby
341: message CSODOTAServerStaticLobby
348: message CMsgAdditionalLobbyStartupAccountData
349: message ChatWheelMessageRange
354: message PingWheelMessageRange
365: message CMsgLobbyInitializationComplete
368: message CMsgLobbyPlaytestDetails
372: message CMsgLocalServerGuildData
384: message CMsgLocalServerFakeLobbyData
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
<summary><code>dota_gcmessages_common_overworld.proto</code> — module: <code>dota_gcmessages_common_overworld_pb2</code>; imports: 5; enums: 19; messages: 51</summary>

- Imports: steammessages.proto, dota_shared_enums.proto, dota_gcmessages_common.proto, dota_gcmessages_common_survivors.proto, gcsdk_gcmessages.proto

```text
7: enum EOverworldNodeState
13: enum EOverworldPathState
19: enum EOverworldAuditAction
39: enum EOverworldMinigameAction
49: message CMsgOverworldTokenCount
54: message CMsgOverworldTokenQuantity
58: message CMsgOverworldEncounterTokenTreasureData
59: message RewardOption
68: message CMsgOverworldEncounterTokenQuestData
69: message Quest
78: message CMsgOverworldHeroList
82: message CMsgOverworldEncounterChooseHeroData
87: message CMsgOverworldEncounterProgressData
94: message CMsgOverworldEncounterData
98: message CMsgOverworldNode
104: message CMsgOverworldPath
110: message CMsgOverworldMinigameCustomData
116: message CMsgOverworldMinigameUserData
122: message CMsgOverworldUserData
123: message MinigameDataEntry
135: message CMsgOverworldMatchRewards
136: message Player
145: message CMsgClientToGCOverworldGetUserData
149: message CMsgClientToGCOverworldGetUserDataResponse
150: enum EResponse
163: message CMsgGCToClientOverworldUserDataUpdated
168: message CMsgClientToGCOverworldCompletePath
173: message CMsgClientToGCOverworldCompletePathResponse
174: enum EResponse
192: message CMsgOverworldEncounterPitFighterRewardData
197: message CMsgClientToGCOverworldClaimEncounterReward
208: message CMsgClientToGCOverworldClaimEncounterRewardResponse
209: enum EResponse
234: message CMsgClientToGCOverworldVisitEncounter
239: message CMsgClientToGCOverworldVisitEncounterResponse
240: enum EResponse
256: message CMsgClientToGCOverworldMoveToNode
261: message CMsgClientToGCOverworldMoveToNodeResponse
262: enum EResponse
276: message CMsgClientToGCOverworldTradeTokens
284: message CMsgClientToGCOverworldTradeTokensResponse
285: enum EResponse
305: message CMsgClientToGCOverworldGiftTokens
312: message CMsgClientToGCOverworldGiftTokensResponse
313: enum EResponse
331: message CMsgClientToGCOverworldRequestTokensNeededByFriend
336: message CMsgClientToGCOverworldRequestTokensNeededByFriendResponse
337: enum EResponse
354: message CMsgClientToGCOverworldDevResetAll
358: message CMsgClientToGCOverworldDevResetAllResponse
359: enum EResponse
372: message CMsgClientToGCOverworldDevResetNode
377: message CMsgClientToGCOverworldDevResetNodeResponse
378: enum EResponse
392: message CMsgClientToGCOverworldDevGrantTokens
397: message CMsgClientToGCOverworldDevGrantTokensResponse
398: enum EResponse
411: message CMsgClientToGCOverworldDevClearInventory
415: message CMsgClientToGCOverworldDevClearInventoryResponse
416: enum EResponse
429: message CMsgClientToGCOverworldFeedback
435: message CMsgClientToGCOverworldFeedbackResponse
436: enum EResponse
449: message CMsgClientToGCOverworldGetDynamicImage
455: message CMsgClientToGCOverworldGetDynamicImageResponse
456: message Image
463: enum EDynamicImageFormat
473: message CMsgClientToGCOverworldMinigameAction
482: message CMsgClientToGCOverworldMinigameActionResponse
483: enum EResponse
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
<summary><code>dota_gcmessages_server.proto</code> — module: <code>dota_gcmessages_server_pb2</code>; imports: 14; enums: 6; messages: 186</summary>

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
288: message CAdditionalSignoutMsg
293: message CSocialFeedMatchEvent
301: message CCustomGameData
305: message EventGameLeaderboardEntry
315: message WardPlacement
358: message CMsgSignOutDraftInfo
364: message CMsgSignOutBotInfo
371: message CMsgSignOutTextMuteInfo
372: message TextMuteMessage
381: message CMsgSignOutPlayerStats
414: message CMsgSignOutCommunicationSummary
415: message PlayerCommunication
416: message PingDetail
444: message CMsgGameMatchSignoutResponse
445: message PlayerMetadata
475: message CMsgGameMatchSignOutPermissionRequest
482: message CMsgGameMatchSignOutPermissionResponse
488: message CMsgGameMatchSignOutEventGameData
496: message CMsgGameMatchSignOutPerfData
527: message CMsgGameMatchSignOutBanData
532: message CMsgDOTALiveScoreboardUpdate
533: message Team
534: message Player
535: message HeroAbility
540: enum DOTAUltimateState
595: message CMsgServerToGCRequestBatchPlayerResources
601: message CMsgServerToGCRequestBatchPlayerResourcesResponse
602: message Result
622: message CMsgDOTAPlayerFailedToConnect
627: message CMsgGCToRelayConnect
637: message CMsgGCGCToLANServerRelayConnect
641: message CMsgGCBanStatusRequest
645: message CMsgGCBanStatusResponse
652: message CMsgTournamentItemEvent
667: message CMsgTournamentItemEventResponse
672: message CMsgTeamFanfare
676: message CMsgResponseTeamFanfare
681: message CMsgDOTAAwardEventPoints
682: message AwardPoints
698: message CMsgGCToServerPingRequest
703: message CMsgGCToServerPingResponse
709: message CMsgServerToGCMatchConnectionStats
710: message Player
726: message CMsgServerGCUpdateSpectatorCount
730: message CSerializedCombatLog
731: message Dictionary
732: message DictString
745: message CMsgServerToGCVictoryPredictions
746: message PredictionItem
751: message Record
760: message CMsgServerToGCRequestStatus
763: message CMsgServerToGCRequestStatus_Response
767: message CMsgGCToServerEvaluateToxicChat
772: message CMsgServerToGCEvaluateToxicChat
780: message CMsgServerToGCEvaluateToxicChatResponse
788: message CMsgSignOutAssassinMiniGameInfo
799: message CMsgServerToGCKillSummaries
800: message KillSummary
810: message CMsgServerToGCLockCharmTrading
815: message CMsgSignOutUpdatePlayerChallenge
816: message Challenge
831: message CMsgServerToGCRerollPlayerChallenge
836: message CMsgSpendWager
837: message Player
850: message CMsgSignOutXPCoins
851: message Player
866: message CMsgSignOutBounties
867: message Bounty
879: message CMsgSignOutCommunityGoalProgress
880: message EventGoalIncrement
889: message CMsgServerToGCCloseCompendiumInGamePredictionVoting
895: message CMsgServerToGCCloseCompendiumInGamePredictionVotingResponse
899: message CMsgServerToGCCompendiumInGamePredictionResults
900: message PredictionResult
912: message CMsgServerToGCCompendiumChosenInGamePredictions
913: message Prediction
922: message CMsgGCToGCCompendiumInGamePredictionResults
926: message CMsgServerToGCMatchPlayerItemPurchaseHistory
927: message ItemPurchase
936: message Player
952: message CMsgServerToGCMatchPlayerNeutralItemEquipHistory
953: message ItemEquip
961: message Player
973: message CMsgServerToGCMatchStateHistory
974: message PlayerState
986: message TeamState
999: message MatchState
1011: message CMsgMatchStateSteamMLEntry
1017: message CMsgLaneSelectionSteamMLEntry
1022: message CMsgAbilitySelectionSteamMLEntry
1031: message CMsgItemPurchasePregameSteamMLEntry
1041: message CMsgItemPurchaseSteamMLEntry
1051: message CMsgItemPurchaseSequenceSteamMLEntry
1061: message CMsgServerToGCCavernCrawlIsHeroActive
1069: message CMsgServerToGCPlayerChallengeHistory
1070: message PlayerChallenge
1088: message CMsgServerToGCCavernCrawlIsHeroActiveResponse
1089: message MapResults
1101: message CMsgNeutralItemStats
1102: message NeutralItem
1114: message CMsgGCToServerLobbyHeroBanRates
1115: message HeroBanEntry
1124: message CMsgSignOutGuildContractProgress
1125: message CompletedGuildEventContracts
1131: message PlayerContract
1139: message CMsgSignOutGuildChallengeProgress
1140: message ChallengeProgress
1153: message CMsgSignOutMVPStats
1154: message Player
1155: message KillEaterEvent
1194: message CMsgServerToGCGetGuildContracts
1198: message CMsgServerToGCGetGuildContractsResponse
1199: message ContractDetails
1207: message Player
1217: message CMsgMatchDiretideCandy
1218: message CandyDetails
1223: message PlayerCandy
1234: message CMsgGCToServerCheerData
1235: message CheerTypeCount
1243: message CMsgCheerConfig
1264: message CMsgGCToServerCheerConfig
1268: message CMsgServerToGCGetCheerConfig
1272: message CMsgServerToGCGetCheerConfigResponse
1276: message CMsgGCToServerCheerScalesOverride
1280: message CMsgGCToServerGetCheerState
1283: message CMsgCheerTypeState
1290: message CMsgCheerState
1296: message CMsgServerToGCReportCheerState
1301: message CMsgServerToGCGetStickerHeroes
1305: message CMsgServerToGCGetStickerHeroesResponse
1306: message Player
1314: message CMsgSteamLearnMatchInfo
1322: message CMsgSteamLearnMatchInfoPlayer
1331: message CMsgSteamLearnMatchInfoTeam
1332: message Player
1345: message CMsgSteamLearnMatchHeroesV3
1356: message CMsgSteamLearnMatchHeroesV4
1365: message CMsgSteamLearnMatchHeroV6
1375: message CMsgSteamLearnMatchHeroV8
1383: message CMsgSteamLearnPlayerTimedStats
1384: message StatBucket
1402: message CMsgSteamLearnMatchStateV5
1403: message PlayerState
1416: message TeamState
1434: message CMsgSteamLearnItemPurchaseV7
1439: message CMsgSteamLearnPreGameItemPurchases
1445: message CMsgSteamLearnPreGameItemPurchase
1450: message CMsgSteamLearnNeutralItemPurchaseV4
1458: message CMsgSteamLearnAbilitySkill
1465: message CMsgSteamLearnWardPlacement
1466: message Location
1476: message CMsgSteamLearnPlayerMatchState
1491: message CMsgSignOutMuertaMinigame
1495: message CMsgSignOutMapStats
1496: message Player
1505: message CMsgServerToGCNewBloomGift
1511: message CMsgServerToGCNewBloomGiftResponse
1516: message CMsgSignOutOverworld
1517: message Player
1527: message CMsgSignOutCraftworks
1528: message Player
1537: message CMsgSignOutMonsterHunter
1538: message Player
1548: message CMsgServerToGCWarningLowServerFramerate
1556: message CMsgServerToGCWarningInvalidBotAbilityUsage
```

</details>

<a id="dota-gcmessages-webapi-proto"></a>
### dota_gcmessages_webapi.proto

<details>
<summary><code>dota_gcmessages_webapi.proto</code> — module: <code>dota_gcmessages_webapi_pb2</code>; imports: 5; enums: 14; messages: 38</summary>

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
220: message CMsgTalentContentStatus
221: message TalentDetails
236: message CMsgSetTalentContentResponse
237: enum EResult
246: message CMsgDPCEvent
247: message PhaseInfo
252: message League
259: enum ELeagueEvent
286: enum ELeagueEventPhase
301: enum ELeagueEventType
311: enum ETour
335: message CMsgDPCEventList
339: message CMsgDOTAFantasyCardLineup
340: message CardBonus
345: message Card
357: message League
363: message Period
373: message CMsgDOTAFantasyCardList
374: message CardBonus
379: message Card
392: message CMsgChatToxicityToxicPlayerMatchesReport
393: message IndividualRow
405: message CMsgChatToxicityReport
414: message CMsgGetTeamAuditInformation
415: message Action
430: message CMsgDOTADPCMatch
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
<summary><code>dota_match_metadata.proto</code> — module: <code>dota_match_metadata_pb2</code>; imports: 10; enums: 2; messages: 38</summary>

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
251: message GuildChallengeProgress
252: message IndividualProgress
267: message Tip
288: message CDOTAMatchPrivateMetadata
289: message StringName
294: message Team
295: message Player
296: message CombatSegment
297: message DamageByAbility
298: message ByHeroTarget
308: message HealingByAbility
309: message ByHeroTarget
324: message BuffRecord
325: message ByHeroTarget
337: message GoldReceived
348: message XPReceived
374: message Building
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
51: message CDOTALuaModifierEntry
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
96: message HeroNeutralChoice
102: message HeroNeutralTier
109: message Hero
180: message Stock
189: message Building
197: message Entity
204: message Item
217: message Modifier
```

</details>

<a id="dota-shared-enums-proto"></a>
### dota_shared_enums.proto

<details>
<summary><code>dota_shared_enums.proto</code> — module: <code>dota_shared_enums_pb2</code>; imports: 0; enums: 54; messages: 14</summary>

- Imports: *(none)*

```text
1: enum DOTA_GameMode
31: enum DOTA_GameState
48: enum DOTA_GC_TEAM
66: enum EEvent
127: enum ERankType
141: enum DOTALeaverStatus_t
154: enum DOTAConnectionState_t
164: enum Fantasy_Roles
172: enum Fantasy_Scoring
195: enum Fantasy_Team_Slots
203: enum Fantasy_Selection_Mode
216: enum Fantasy_Gem_Type
222: enum DOTAChatChannelType_t
250: enum EChatSpecialPrivileges
256: enum DOTACommType_t
275: enum DOTACommLevel_t
286: enum DOTABehaviorLevel_t
294: enum EProfileCardSlotType
304: enum EMatchGroupServerStatus
310: enum DOTA_CM_PICK
316: enum DOTALowPriorityBanType
323: enum DOTALobbyReadyState
330: enum DOTAJoinLobbyResult
348: enum DOTASelectionPriorityRules
353: enum DOTASelectionPriorityChoice
361: enum DOTAMatchVote
367: enum DOTALobbyVisibility
373: enum EDOTAPlayerMMRType
379: enum EDOTAMMRBoostType
385: enum MatchType
395: enum DOTABotDifficulty
408: enum DOTA_BOT_MODE
439: enum MatchLanguages
450: enum ETourneyQueueDeadlineState
460: enum EMatchOutcome
482: enum ELaneType
491: enum EBadgeType
521: enum ELeagueStatus
531: enum ELeagueRegion
541: enum ELeagueTier
554: enum ELeagueTierCategory
560: enum ELeagueDivision
566: enum ELeagueBroadcastProvider
574: enum ELeaguePhase
581: enum ELeagueAuditAction
626: enum DOTA_COMBATLOG_TYPES
675: enum EDPCFavoriteType
682: enum EDPCPushNotification
696: enum EEventActionScoreMode
701: enum EPlayerChallengeHistoryType
710: enum EOverwatchReportReason
719: enum ECandyShopUpgrade
726: enum EItemSuggestPreference
732: enum ETimerAlertType
740: message CDOTAClientHardwareSpecs
750: message CDOTASaveGame
751: message Player
757: message SaveInstance
758: message PlayerPositions
777: message CMsgDOTACombatLogEntry
860: message CMsgPendingEventAward
869: message CMsgMonsterHunterMaterialQuantity
870: message MaterialCountsEntry
878: message CMsgMonsterHunterInvestigation
886: message CMsgMonsterHunterInvestigationGameState
887: message HuntedBy
898: message CMsgMonsterHunterCodexUpdateData
899: message KillInfo
```

</details>

<a id="dota-usercmd-proto"></a>
### dota_usercmd.proto

<details>
<summary><code>dota_usercmd.proto</code> — module: <code>dota_usercmd_pb2</code>; imports: 2; enums: 0; messages: 1</summary>

- Imports: networkbasetypes.proto, usercmd.proto

```text
4: message CDota2UserCmdPB
```

</details>

<a id="dota-usermessages-proto"></a>
### dota_usermessages.proto

<details>
<summary><code>dota_usermessages.proto</code> — module: <code>dota_usermessages_pb2</code>; imports: 3; enums: 19; messages: 190</summary>

- Imports: networkbasetypes.proto, dota_shared_enums.proto, dota_commonmessages.proto

```text
5: enum EDotaUserMessages
176: enum DOTA_CHAT_MESSAGE
294: enum DOTA_NO_BATTLE_POINTS_REASONS
301: enum DOTA_CHAT_INFORMATIONAL
309: enum DOTA_ABILITY_PING_TYPE
328: enum DOTA_REPLAY_STATE_EVENT
337: enum EDotaEntityMessages
347: enum DOTA_OVERHEAD_ALERT
375: enum DOTA_ROSHAN_PHASE
381: enum DOTA_POSITION_CATEGORY
400: enum DOTA_ABILITY_TARGET_TYPE
409: enum EHeroStatType
434: enum EPlayerVoiceListenState
457: enum EProjectionEvent
462: message CDOTAUserMsg_AIDebugLine
466: message CDOTAUserMsg_Ping
471: message CDOTAUserMsg_SwapVerify
475: message CDOTAUserMsg_ChatEvent
489: message CDOTAUserMsg_BotChat
496: message CDOTAUserMsg_CombatHeroPositions
503: message CDOTAUserMsg_CombatLogBulkData
513: message CDOTAUserMsg_ProjectileParticleCPData
518: message CDOTAUserMsg_UpdateLinearProjectileCPData
524: message CDOTAUserMsg_MiniKillCamInfo
525: message Attacker
526: message Ability
540: message CDOTAUserMsg_GlobalLightColor
545: message CDOTAUserMsg_GlobalLightDirection
550: message CDOTAUserMsg_LocationPing
555: message CDOTAUserMsg_PingConfirmation
562: message CDOTAUserMsg_ItemAlert
567: message CDOTAUserMsg_EnemyItemAlert
578: message CDOTAUserMsg_ModifierAlert
587: message CDOTAUserMsg_HPManaAlert
593: message CDOTAUserMsg_NeutralCampAlert
603: message CDOTAUserMsg_GlyphAlert
608: message CDOTAUserMsg_RadarAlert
613: message CDOTAUserMsg_RoshanTimer
618: message CDOTAUserMsg_TormentorTimer
623: message CDOTAUserMsg_WillPurchaseAlert
630: message CDOTAUserMsg_EmptyTeleportAlert
636: message CDOTAUserMsg_MarsArenaOfBloodAttack
642: message CDOTAUserMsg_BuyBackStateAlert
646: message CDOTAUserMsg_QuickBuyAlert
654: message CDOTAUserMsg_CourierKilledAlert
655: message LostItem
669: message CDOTAUserMsg_MinimapEvent
678: message CDOTAUserMsg_MapLine
683: message CDOTAUserMsg_MinimapDebugPoint
691: message CDOTAUserMsg_CreateLinearProjectile
706: message CDOTAUserMsg_DestroyLinearProjectile
710: message CDOTAUserMsg_DodgeTrackingProjectiles
715: message CDOTAUserMsg_SpectatorPlayerClick
721: message CDOTAUserMsg_SpectatorPlayerUnitOrders
735: message CDOTAUserMsg_NevermoreRequiem
742: message CDOTAUserMsg_InvalidCommand
747: message CDOTAUserMsg_HudError
752: message CDOTAUserMsg_SharedCooldown
759: message CDOTAUserMsg_SetNextAutobuyItem
763: message CDOTAUserMsg_HalloweenDrops
769: message CDOTAUserMsg_CourierLeftFountainAlert
773: message CDOTAResponseQuerySerialized
774: message Fact
775: enum ValueType
793: message CDOTASpeechMatchOnClient
800: message CDOTAUserMsg_UnitEvent
801: message Interval
806: message Speech
816: message SpeechMute
820: message AddGesture
829: message RemoveGesture
833: message BloodImpact
839: message FadeGesture
854: message CDOTAUserMsg_ItemPurchased
859: message CDOTAUserMsg_ItemSold
863: message CDOTAUserMsg_ItemFound
871: message CDOTAUserMsg_OverheadEvent
879: message CDOTAUserMsg_TutorialTipInfo
884: message CDOTAUserMsg_TutorialFinish
891: message CDOTAUserMsg_TutorialMinimapPosition
894: message CDOTAUserMsg_SendGenericToolTip
901: message CDOTAUserMsg_WorldLine
906: message CDOTAUserMsg_ChatWheel
914: message CDOTAUserMsg_ReceivedXmasGift
920: message CDOTAUserMsg_ShowSurvey
929: message CDOTAUserMsg_UpdateSharedContent
933: message CDOTAUserMsg_TutorialRequestExp
936: message CDOTAUserMsg_TutorialFade
940: message CDOTAUserMsg_TutorialPingMinimap
948: message CDOTAUserMsg_GamerulesStateChanged
952: message CDOTAUserMsg_AddQuestLogEntry
957: message CDOTAUserMsg_SendStatPopup
962: message CDOTAUserMsg_DismissAllStatPopups
966: message CDOTAUserMsg_SendRoshanSpectatorPhase
972: message CDOTAUserMsg_SendRoshanPopup
977: message CDOTAUserMsg_SendFinalGold
982: message CDOTAUserMsg_CustomMsg
988: message CDOTAUserMsg_CoachHUDPing
993: message CDOTAUserMsg_ClientLoadGridNav
996: message CDOTAUserMsg_TE_Projectile
1017: message CDOTAUserMsg_TE_ProjectileLoc
1036: message CDOTAUserMsg_TE_DestroyProjectile
1040: message CDOTAUserMsg_TE_DotaBloodImpact
1047: message CDOTAUserMsg_AbilityPing
1063: message CDOTAUserMsg_TE_UnitAnimation
1073: message CDOTAUserMsg_TE_UnitAnimationEnd
1078: message CDOTAUserMsg_ShowGenericPopup
1087: message CDOTAUserMsg_VoteStart
1094: message CDOTAUserMsg_VoteUpdate
1098: message CDOTAUserMsg_VoteEnd
1102: message CDOTAUserMsg_BoosterStatePlayer
1110: message CDOTAUserMsg_BoosterState
1114: message CDOTAUserMsg_AbilitySteal
1120: message CDOTAUserMsg_StatsHeroLookup
1127: message CDOTAUserMsg_StatsHeroPositionInfo
1128: message PositionPair
1137: message CDOTAUserMsg_StatsHeroMinuteDetails
1155: message CDOTAUserMsg_StatsTeamMinuteDetails
1156: message LocationPerformance
1174: message CDOTAUserMsg_StatsPlayerKillShare
1183: message CDOTAUserMsg_StatsKillDetails
1192: message CDOTAUserMsg_StatsMatchDetails
1195: message CDOTAUserMsg_StatsFightTeamDetails
1202: message CDOTAUserMsg_StatsFightDetails
1217: message CDOTAUserMsg_MiniTaunt
1221: message CDOTAUserMsg_SpeechBubble
1225: message CDOTAUserMsg_CustomHeaderMessage
1232: message CMsgHeroAbilityStat
1238: message CMsgCombatAnalyzerPlayerStat
1243: message CMsgCombatAnalyzerStats
1248: message CDOTAUserMsg_BeastChat
1255: message CDOTAUserMsg_CustomHudElement_Create
1261: message CDOTAUserMsg_CustomHudElement_Modify
1267: message CDOTAUserMsg_CustomHudElement_Destroy
1271: message CDOTAUserMsg_CompendiumStatePlayer
1276: message CDOTAUserMsg_CompendiumState
1280: message CDOTAUserMsg_ProjectionAbility
1291: message CDOTAUserMsg_ProjectionEvent
1296: message CDOTAUserMsg_XPAlert
1301: message CDOTAUserMsg_TalentTreeAlert
1309: message CDOTAUserMsg_UpdateQuestProgress
1312: message CDOTAUserMsg_QuestStatus
1323: message CDOTAUserMsg_SuggestHeroPick
1330: message CDOTAUserMsg_SuggestHeroRole
1335: message CDOTAUserMsg_KillcamDamageTaken
1344: message CDOTAUserMsg_SelectPenaltyGold
1349: message CDOTAUserMsg_RollDiceResult
1357: message CDOTAUserMsg_FlipCoinResult
1363: message CDOTAUserMessage_RequestItemSuggestions
1367: message CDOTAUserMessage_TeamCaptainChanged
1372: message CDOTAUserMsg_ChatWheelCooldown
1377: message CDOTAUserMsg_HeroRelicProgress
1385: message CDOTAUserMsg_AbilityDraftRequestAbility
1393: message CDOTAUserMsg_DamageReport
1401: message CDOTAUserMsg_SalutePlayer
1410: message CDOTAUserMsg_GiftPlayer
1416: message CDOTAUserMsg_TipAlert
1421: message CDOTAUserMsg_ReplaceQueryUnit
1427: message CDOTAUserMsg_ESArcanaCombo
1433: message CDOTAUserMsg_ESArcanaComboSummary
1439: message CDOTAUserMsg_OMArcanaCombo
1446: message CDOTAUserMsg_HighFiveCompleted
1453: message CDOTAUserMsg_HighFiveLeftHanging
1457: message CDOTAUserMsg_ShovelUnearth
1464: message CDOTAUserMsg_AllStarEvent
1465: message PlayerScore
1477: message CDOTAUserMsg_QueuedOrderRemoved
1481: message CDOTAUserMsg_DebugChallenge
1491: message CDOTAUserMsg_FoundNeutralItem
1501: message CDOTAUserMsg_OutpostCaptured
1506: message CDOTAUserMsg_OutpostGrantedXP
1511: message CDOTAUserMsg_MoveCameraToUnit
1515: message CDOTAUserMsg_PauseMinigameData
1516: message DataBit
1525: message CDOTAUserMsg_VersusScene_PlayerBehavior
1533: message CDOTAUserMsg_QoP_ArcanaSummary
1540: message CDOTAUserMsg_HotPotato_Created
1545: message CDOTAUserMsg_HotPotato_Exploded
1549: message CDOTAUserMsg_WK_Arcana_Progress
1555: message CDOTAUserMsg_GuildChallenge_Progress
1556: message PlayerProgress
1561: enum EChallengeType
1576: message CDOTAUserMsg_WRArcanaProgress
1586: message CDOTAUserMsg_WRArcanaSummary
1597: message CDOTAUserMsg_EmptyItemSlotAlert
1604: message CDOTAUserMsg_AghsStatusAlert
1613: message CDOTAUserMsg_MutedPlayers
1618: message CDOTAUserMsg_ContextualTip
1636: message CDOTAUserMsg_ChatMessage
1642: message CDOTAUserMsg_RockPaperScissorsStarted
1647: message CDOTAUserMsg_RockPaperScissorsFinished
1654: message CDOTAUserMsg_DuelOpponentKilled
1659: message CDOTAUserMsg_DuelAccepted
1664: message CDOTAUserMsg_DuelRequested
1668: message CDOTAUserMsg_MuertaReleaseEvent_AssignedTargetKilled
1676: message CDOTAUserMsg_PlayerDraftSuggestPick
1681: message CDOTAUserMsg_PlayerDraftPick
1687: message CDOTAUserMsg_FacetPing
1694: message CDOTAUserMsg_InnatePing
1700: message CDOTAUserMsg_NeutralCraftAvailable
1703: message CDOTAUserMsg_TimerAlert
1708: message CDOTAUserMsg_MadstoneAlert
1709: enum EMadstoneAlertType
1722: message CDOTAUserMsg_MonsterHunter_InvestigationsAvailable
1726: message CDOTAUserMsg_MonsterHunter_InvestigationGameState
1731: message CDOTAUserMsg_MonsterHunter_HuntAlert
1732: enum EHuntAlertType
1742: enum EHuntStatusType
1755: message CDOTAUserMsg_KillEffect
```

</details>

<a id="econ-gcmessages-proto"></a>
### econ_gcmessages.proto

<details>
<summary><code>econ_gcmessages.proto</code> — module: <code>econ_gcmessages_pb2</code>; imports: 4; enums: 15; messages: 143</summary>

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
443: message CMsgDevUnlockAllItemStyles
447: message CMsgDevUnlockAllItemStylesResponse
451: message CMsgGCGetAccountSubscriptionItem
455: message CMsgGCGetAccountSubscriptionItemResponse
459: message CMsgGCAddGiftItem
467: message CMsgClientToGCWrapAndDeliverGift
473: message CMsgSQLGCToGCRevokeUntrustedGift
478: message CMsgClientToGCWrapAndDeliverGiftResponse
488: message CMsgClientToGCUnwrapGift
492: message CMsgClientToGCGetGiftPermissions
495: message CMsgClientToGCGetGiftPermissionsResponse
496: message FriendPermission
509: message CMsgClientToGCUnpackBundle
513: message CMsgClientToGCUnpackBundleResponse
514: enum EUnpackBundle
529: message CMsgClientToGCPackBundle
534: message CMsgClientToGCPackBundleResponse
535: enum EPackBundle
557: message CMsgGCToClientStoreTransactionCompleted
562: message CMsgClientToGCEquipItems
566: message CMsgClientToGCEquipItemsResponse
570: message CMsgClientToGCSetItemStyle
575: message CMsgClientToGCSetItemStyleResponse
576: enum ESetStyle
585: message CMsgClientToGCUnlockItemStyle
591: message CMsgClientToGCUnlockItemStyleResponse
592: enum EUnlockStyle
613: message CMsgClientToGCSetItemInventoryCategory
620: message CMsgClientToGCUnlockCrate
625: message CMsgClientToGCUnlockCrateResponse
626: message Item
635: message CMsgClientToGCRemoveItemAttribute
639: message CMsgClientToGCRemoveItemAttributeResponse
640: enum ERemoveItemAttribute
652: message CMsgClientToGCNameItem
658: message CMsgClientToGCNameItemResponse
659: enum ENameItem
671: message CMsgGCSetItemPosition
676: message CAttribute_ItemDynamicRecipeComponent
689: message CProtoItemSocket
699: message CProtoItemSocket_Empty
703: message CProtoItemSocket_Effect
708: message CProtoItemSocket_Color
715: message CProtoItemSocket_Strange
721: message CProtoItemSocket_Strange_DESERIALIZE_FROM_STRING_ONLY
728: message CProtoItemSocket_Spectator
736: message CProtoItemSocket_AssetModifier
741: message CProtoItemSocket_AssetModifier_DESERIALIZE_FROM_STRING_ONLY
748: message CProtoItemSocket_Autograph
755: message CProtoItemSocket_StaticVisuals
759: message CAttribute_String
763: message CWorkshop_GetItemDailyRevenue_Request
770: message CWorkshop_GetItemDailyRevenue_Response
771: message CountryDailyRevenue
781: message CWorkshop_GetPackageDailyRevenue_Request
787: message CWorkshop_GetPackageDailyRevenue_Response
788: message CountryDailyRevenue
798: message CMsgSQLGCToGCGrantBackpackSlots
803: message CMsgClientToGCLookupAccountName
807: message CMsgClientToGCLookupAccountNameResponse
812: message CMsgClientToGCCreateStaticRecipe
813: message Item
822: message CMsgClientToGCCreateStaticRecipeResponse
823: message OutputItem
829: message InputError
834: message AdditionalOutput
839: enum EResponse
854: message CMsgProcessTransactionOrder
855: message Item
879: message CMsgGCToGCStoreProcessCDKeyTransaction
885: message CMsgGCToGCStoreProcessCDKeyTransactionResponse
889: message CMsgGCToGCStoreProcessSettlement
893: message CMsgGCToGCStoreProcessSettlementResponse
897: message CMsgGCToGCBroadcastConsoleCommand
905: message CMsgGCToGCConsoleOutput
906: message OutputLine
917: message CMsgItemAges
918: message MaxItemIDTimestamp
926: message CMsgGCToGCInternalTestMsg
936: message CMsgGCToGCClientServerVersionsUpdated
944: message CMsgGCToGCBroadcastMessageFromSub
951: message CMsgGCToClientCurrencyPricePoints
952: message Currency
961: message CMsgBannedWordList
966: message CMsgGCToGCFlushSteamInventoryCache
967: message Key
975: message CMsgGCToGCUpdateSubscriptionItems
980: message CMsgGCToGCSelfPing
984: message CMsgGCToGCGetInfuxIntervalStats
987: message CMsgGCToGCGetInfuxIntervalStatsResponse
995: message CMsgGCToGCPurchaseSucceeded
998: message CMsgClientToGCGetLimitedItemPurchaseQuantity
1002: message CMsgClientToGCGetLimitedItemPurchaseQuantityResponse
1003: enum EResponse
1017: message CMsgClientToGCGetInFlightItemCharges
1021: message CMsgClientToGCGetInFlightItemChargesResponse
1022: enum EResponse
1035: message CMsgClientToGCPurchaseChargeCostItems
1036: message Item
1047: message CMsgClientToGCPurchaseChargeCostItemsResponse
1048: enum EResponse
1065: message CMsgGCToClientInFlightChargesUpdated
1066: message ItemCharges
1074: message CMsgClientToGCCancelUnfinalizedTransactions
1078: message CMsgClientToGCCancelUnfinalizedTransactionsResponse
1082: message CMsgGCToGCUpdateWelcomeMsg
1088: message CMsgClientToGCRecycleMultipleItems
1089: message Item
1098: message CMsgClientToGCRecycleMultipleItemsResponse
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
34: message CMsgGenericResult
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
<summary><code>enums_clientserver.proto</code> — module: <code>enums_clientserver_pb2</code>; imports: 0; enums: 6; messages: 0</summary>

- Imports: *(none)*

```text
4: enum EMsg
1496: enum EClientPersonaStateFlag
1513: enum EMsgClanAccountFlags
1521: enum ESteamReviewScore
1534: enum ECodecUsagePlatform
1542: enum ECodecUsageReason
```

</details>

<a id="gameevents-proto"></a>
### gameevents.proto

<details>
<summary><code>gameevents.proto</code> — module: <code>gameevents_pb2</code>; imports: 1; enums: 1; messages: 16</summary>

- Imports: networkbasetypes.proto

```text
3: enum EBaseGameEvents
19: message CMsgVDebugGameSessionIDEvent
24: message CMsgPlaceDecalEvent
40: message CMsgClearWorldDecalsEvent
44: message CMsgClearEntityDecalsEvent
48: message CMsgClearDecalsForEntityEvent
53: message CMsgSource1LegacyGameEventList
56: message key_t
61: message descriptor_t
70: message CMsgSource1LegacyListenEvents
75: message CMsgSource1LegacyGameEvent
76: message key_t
94: message CMsgSosStartSoundEvent
103: message CMsgSosStopSoundEvent
107: message CMsgSosStopSoundEventHash
112: message CMsgSosSetSoundEventParams
117: message CMsgSosSetLibraryStackFields
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
245: message CMsgClientWelcome
246: message Location
270: message CMsgConnectionStatus
279: message CMsgGCToGCSOCacheSubscribe
280: message CMsgHaveVersions
292: message CMsgGCToGCSOCacheUnsubscribe
298: message CMsgGCClientPing
301: message CMsgGCToGCForwardAccountDetails
307: message CMsgGCToGCLoadSessionSOCache
312: message CMsgGCToGCLoadSessionSOCacheResponse
315: message CMsgGCToGCUpdateSessionStats
321: message CMsgGCToClientRequestDropped
324: message CWorkshop_PopulateItemDescriptions_Request
325: message SingleItemDescription
330: message ItemDescriptionsLanguageBlock
339: message CWorkshop_GetContributors_Request
344: message CWorkshop_GetContributors_Response
348: message CWorkshop_SetItemPaymentRules_Request
349: message WorkshopItemPaymentRule
356: message WorkshopDirectPaymentRule
361: message PartnerItemPaymentRule
376: message CWorkshop_SetItemPaymentRules_Response
380: message CCommunity_ClanAnnouncementInfo
395: message CCommunity_GetClanAnnouncements_Request
411: message CCommunity_GetClanAnnouncements_Response
417: message CBroadcast_PostGameDataFrame_Request
424: message CMsgSerializedSOCache
425: message TypeCache
431: message Cache
432: message Version
448: message CMsgGCToClientPollConvarRequest
453: message CMsgGCToClientPollConvarResponse
458: message CGCMsgCompressedMsgToClient
463: message CMsgGCToGCMasterBroadcastMessage
472: message CMsgGCToGCMasterSubscribeToCache
479: message CMsgGCToGCMasterSubscribeToCacheResponse
482: message CMsgGCToGCMasterSubscribeToCacheAsync
486: message CMsgGCToGCMasterUnsubscribeFromCache
493: message CMsgGCToGCMasterDestroyCache
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
<summary><code>netmessages.proto</code> — module: <code>netmessages_pb2</code>; imports: 1; enums: 13; messages: 82</summary>

- Imports: networkbasetypes.proto

```text
3: enum CLC_Messages
20: enum SVC_Messages
54: enum VoiceDataFormat_t
60: enum RequestPause_t
66: enum PrefetchType
70: enum ESplitScreenMessageType
75: enum EQueryCvarValueStatus
82: enum DIALOG_TYPE
90: enum SVC_Messages_LowFrequency
94: enum Bidirectional_Messages
101: enum Bidirectional_Messages_LowFrequency
106: enum ReplayEventType_t
114: message CCLCMsg_ClientInfo
122: message CCLCMsg_Move
127: message CMsgVoiceAudio
139: message CCLCMsg_VoiceData
145: message CCLCMsg_BaselineAck
150: message CCLCMsg_ListenEvents
154: message CCLCMsg_RespondCvarValue
161: message CCLCMsg_LoadingProgress
165: message CCLCMsg_SplitPlayerConnect
169: message CCLCMsg_SplitPlayerDisconnect
173: message CCLCMsg_ServerStatus
177: message CCLCMsg_RequestPause
182: message CCLCMsg_CmdKeyValues
188: message CCLCMsg_RconServerDetails
192: message CMsgSource2SystemSpecs
209: message CMsgSource2VProfLiteReportItem
230: message CMsgSource2VProfLiteReport
236: message CMsgSource2NetworkFlowQuality
283: message CMsgSource2PerfIntervalSample
284: message Tag
297: message CCLCMsg_Diagnostic
307: message CSource2Metrics_MatchPerfSummary_Notification
308: message Client
327: message CSVCMsg_ServerInfo
348: message CSVCMsg_ClassInfo
349: message class_t
358: message CSVCMsg_SetPause
362: message CSVCMsg_VoiceInit
368: message CSVCMsg_Print
372: message CSVCMsg_Sounds
373: message sounddata_t
399: message CSVCMsg_Prefetch
404: message CSVCMsg_SetView
409: message CSVCMsg_FixAngle
414: message CSVCMsg_CrosshairAngle
418: message CSVCMsg_BSPDecal
426: message CSVCMsg_SplitScreen
432: message CSVCMsg_GetCvarValue
437: message CSVCMsg_Menu
442: message CSVCMsg_UserMessage
448: message CSVCMsg_SendTable
449: message sendprop_t
467: message CSVCMsg_GameEventList
468: message key_t
473: message descriptor_t
482: message CSVCMsg_PacketEntities
485: message alternate_baseline_t
490: message non_transmitted_entities_t
495: message outofpvs_entity_updates_t
524: message CSVCMsg_TempEntities
530: message CSVCMsg_CreateStringTable
545: message CSVCMsg_UpdateStringTable
553: message CSVCMsg_VoiceData
563: message CSVCMsg_PacketReliable
569: message CSVCMsg_FullFrameSplit
576: message CSVCMsg_HLTVStatus
583: message CSVCMsg_ServerSteamID
587: message CSVCMsg_CmdKeyValues
591: message CSVCMsg_RconServerDetails
596: message CMsgIPCAddress
601: message CMsgServerPeer
610: message CSVCMsg_PeerList
614: message CSVCMsg_ClearAllStringTables
619: message ProtoFlattenedSerializerField_t
620: message polymorphic_field_t
639: message ProtoFlattenedSerializer_t
645: message CSVCMsg_FlattenedSerializer
653: message CSVCMsg_StopSound
657: message CBidirMsg_RebroadcastGameEvent
664: message CBidirMsg_RebroadcastSource
668: message CBidirMsg_PredictionEvent
669: enum ESyncType
680: message CMsgServerNetworkStats
681: message Port
686: message Player
724: message CSVCMsg_HltvReplay
735: message CCLCMsg_HltvReplay
743: message CSVCMsg_Broadcast_Command
747: message CCLCMsg_HltvFixupOperatorTick
758: message CSVCMsg_HltvFixupOperatorStatus
763: message CMsgServerUserCmd
771: message CSVCMsg_UserCommands
775: message CSVCMsg_NextMsgPredicted
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
<summary><code>networkbasetypes.proto</code> — module: <code>networkbasetypes_pb2</code>; imports: 2; enums: 3; messages: 27</summary>

- Imports: google/protobuf/descriptor.proto, network_connection.proto

```text
8: enum SignonState_t
19: enum NET_Messages
35: enum SpawnGroupFlags_t
46: message CMsgVector
53: message CMsgVector2D
58: message CMsgQAngle
64: message CMsgQuaternion
71: message CMsgTransform
77: message CMsgRGBA
84: message CMsgPlayerInfo
93: message CEntityMsg
97: message CMsg_CVars
98: message CVar
106: message CNETMsg_NOP
109: message CNETMsg_SplitScreenUser
113: message CNETMsg_Tick
126: message CNETMsg_StringCmd
131: message CNETMsg_SetConVar
137: message CNETMsg_SignonState
146: message CSVCMsg_GameEvent
147: message key_t
163: message CSVCMsgList_GameEvents
164: message event_t
172: message CNETMsg_SpawnGroup_Load
197: message CNETMsg_SpawnGroup_ManifestUpdate
203: message CNETMsg_SpawnGroup_SetCreationTick
209: message CNETMsg_SpawnGroup_Unload
215: message CNETMsg_SpawnGroup_LoadCompleted
219: message CSVCMsg_GameSessionConfiguration
241: message CNETMsg_DebugOverlay
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
15: message CPredictionEvent_StringCommand
19: message CPredictionEvent_Diagnostic
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
21: enum GCProtoBufMsgSrc
30: message CMsgProtoBufHeader
46: message CGCSystemMsg_GetAccountDetails
54: message CGCSystemMsg_GetAccountDetails_Response
97: message CIPLocationInfo
106: message CGCMsgGetIPLocationResponse
```

</details>

<a id="steammessages-base-proto"></a>
### steammessages_base.proto

<details>
<summary><code>steammessages_base.proto</code> — module: <code>steammessages_base_pb2</code>; imports: 1; enums: 4; messages: 21</summary>

- Imports: google/protobuf/descriptor.proto

```text
21: enum EBanContentCheckResult
32: enum EProtoClanEventType
70: enum PartnerEventNotificationType
77: message CMsgIPAddress
84: message CMsgIPAddressBucket
89: message CMsgGCRoutingProtoBufHeader
94: message CMsgProtoBufHeader
95: enum ESessionDisposition
138: message CMsgMulti
143: message CMsgProtobufWrapped
147: message CMsgAuthTicket
159: message CCDDBAppDetailCommon
177: message CMsgAppRights
197: message CCuratorPreferences
214: message CLocalizationToken
219: message CClanEventUserNewsTuple
232: message CClanMatchEventByRange
239: message CCommunity_ClanAnnouncementInfo
259: message CClanEventData
292: message CBilling_Address
305: message CPackageReservationStatus
316: message CMsgKeyValuePair
321: message CMsgKeyValueSet
325: message UserContentDescriptorPreferences
326: message ContentDescriptor
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
<summary><code>steammessages_int.proto</code> — module: <code>steammessages_int_pb2</code>; imports: 1; enums: 3; messages: 82</summary>

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
191: message CMsgTEDust
198: message CMsgTELargeFunnel
203: message CMsgTESparks
210: message CMsgTEPhysicsProp
226: message CMsgTESmoke
231: message CMsgTEWorldDecal
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
<summary><code>usercmd.proto</code> — module: <code>usercmd_pb2</code>; imports: 1; enums: 0; messages: 5</summary>

- Imports: networkbasetypes.proto

```text
3: message CInButtonStatePB
9: message CSubtickMoveStep
19: message CBaseUserCmdExecutionNotes
23: message CBaseUserCmdPB
45: message CUserCmdBasePB
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
66: enum eRollType
74: enum PARTICLE_MESSAGE
117: enum EHapticPulseType
123: message CUserMessageAchievementEvent
127: message CUserMessageCloseCaption
134: message CUserMessageCloseCaptionDirect
141: message CUserMessageCloseCaptionPlaceholder
148: message CUserMessageCurrentTimescale
152: message CUserMessageDesiredTimescale
159: message CUserMessageFade
166: message CUserMessageShake
173: message CUserMessageShakeDir
178: message CUserMessageWaterShake
185: message CUserMessageScreenTilt
193: message CUserMessageSayText
199: message CUserMessageSayText2
209: message CUserMessageHudMsg
219: message CUserMessageHudText
223: message CUserMessageTextMsg
228: message CUserMessageGameTitle
231: message CUserMessageResetHUD
234: message CUserMessageSendAudio
239: message CUserMessageAudioParameter
246: message CUserMessageVoiceMask
252: message CUserMessageRequestState
255: message CUserMessageRumble
261: message CUserMessageSayTextChannel
267: message CUserMessageColoredText
276: message CUserMessageItemPickup
280: message CUserMessageAmmoDenied
284: message CUserMessageShowMenu
291: message CUserMessageCreditsMsg
296: message CEntityMessagePlayJingle
300: message CEntityMessageScreenOverlay
305: message CEntityMessageRemoveAllDecals
310: message CEntityMessagePropagateForce
315: message CEntityMessageDoSpark
326: message CEntityMessageFixAngle
332: message CUserMessageCameraTransition
333: message Transition_DataDriven
344: message CUserMsg_ParticleManager
347: message ReleaseParticleIndex
350: message CreateParticle
363: message DestroyParticle
367: message DestroyParticleInvolving
372: message DestroyParticleNamed
379: message UpdateParticle_OBSOLETE
384: message UpdateParticleFwd_OBSOLETE
389: message UpdateParticleOrient_OBSOLETE
397: message UpdateParticleTransform
404: message UpdateParticleFallback
409: message UpdateParticleOffset
415: message UpdateParticleEnt
426: message UpdateParticleSetFrozen
431: message UpdateParticleShouldDraw
435: message ChangeControlPointAttachment
441: message UpdateEntityPosition
446: message SetParticleFoWProperties
452: message SetParticleShouldCheckFoW
456: message SetControlPointModel
461: message SetControlPointSnapshot
466: message SetParticleText
470: message SetTextureAttribute
475: message SetSceneObjectGenericFlag
479: message SetSceneObjectTintAndDesat
484: message ParticleSkipToTime
488: message ParticleCanFreeze
492: message ParticleFreezeTransitionOverride
496: message FreezeParticleInvolving
502: message AddModellistOverrideElement
508: message ClearModellistOverride
512: message SetParticleNamedValueContext
513: message FloatContextValue
518: message VectorContextValue
523: message TransformContextValue
529: message EHandleContext
540: message CreatePhysicsSim
546: message DestroyPhysicsSim
549: message SetVData
553: message SetMaterialOverride
558: message AddFan
579: message UpdateFan
589: message RemoveFan
592: message SetParticleClusterGrowth
642: message CUserMsg_HudError
646: message CUserMsg_CustomGameEvent
651: message CUserMessageHapticsManagerPulse
658: message CUserMessageHapticsManagerEffect
664: message CUserMessageAnimStateGraphState
669: message CUserMessageUpdateCssClasses
675: message CUserMessageServerFrameTime
679: message CUserMessageLagCompensationError
683: message CUserMessageRequestDllStatus
688: message CUserMessageRequestUtilAction
696: message CUserMessage_UtilMsg_Response
697: message ItemDetail
718: message CUserMessage_DllStatus
719: message CVDiagnostic
726: message CModule
743: message CUserMessageRequestInventory
749: message CUserMessage_Inventory_Response
750: message InventoryDetail
778: message CUserMessageRequestDiagnostic
779: message Diagnostic
798: message CUserMessage_Diagnostic_Response
799: message Diagnostic
825: message CUserMessage_ExtraUserData
833: message CUserMessage_NotifyResponseFound
834: message Criteria
853: message CUserMessage_PlayResponseConditional
```

</details>

<a id="valveextensions-proto"></a>
### valveextensions.proto

<details>
<summary><code>valveextensions.proto</code> — module: <code>valveextensions_pb2</code>; imports: 1; enums: 1; messages: 0</summary>

- Imports: google/protobuf/descriptor.proto

```text
20: enum EProtoDebugVisiblity
```

</details>
