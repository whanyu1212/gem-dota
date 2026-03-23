# dota_clientmessages.proto

- Module: `dota_clientmessages_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **3**
- Messages: **116** (top-level: 114)
- Enums: **4** (top-level: 1)

## Imports

- `dota_commonmessages.proto`
- `dota_shared_enums.proto`
- `base_gcmessages.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CDOTAClientMsg_MapPing</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `location_ping` | `.CDOTAMsg_LocationPing` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_ItemAlert</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_alert` | `.CDOTAMsg_ItemAlert` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_EnemyItemAlert</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_entindex` | `int32` | `optional` | `` | default = -1 |
| 2 | `rune_type` | `int32` | `optional` | `` | default = -1 |
| 3 | `item_level` | `int32` | `optional` | `` | default = -1 |
| 4 | `primary_charges` | `int32` | `optional` | `` | default = -1 |
| 5 | `secondary_charges` | `int32` | `optional` | `` | default = -1 |
| 6 | `ability_id` | `int32` | `optional` | `` | default = -1 |
| 7 | `owner_entindex` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAClientMsg_ModifierAlert</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `buff_internal_index` | `int32` | `optional` | `` |  |
| 2 | `target_entindex` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAClientMsg_ClickedBuff</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `buff_internal_index` | `int32` | `optional` | `` |  |
| 2 | `target_entindex` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAClientMsg_HPManaAlert</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_entindex` | `int32` | `optional` | `` | default = -1 |
| 2 | `show_raw_values` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_NeutralCampAlert</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `spawner_entindex` | `int32` | `optional` | `` | default = -1 |
| 2 | `unit_entindex` | `int32` | `optional` | `` | default = -1 |
| 3 | `stack_request` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_GlyphAlert</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `negative` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_RadarAlert</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `negative` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_MapLine</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `mapline` | `.CDOTAMsg_MapLine` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_AspectRatio</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ratio` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_UnitsAutoAttackMode</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 2</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `mode` | `.CDOTAClientMsg_UnitsAutoAttackMode.EMode` | `optional` | `` | default = INVALID |
| 2 | `unit_type` | `.CDOTAClientMsg_UnitsAutoAttackMode.EUnitType` | `optional` | `` | default = NORMAL |

</details>

<details>
<summary><code>CDOTAClientMsg_UnitsAutoAttackAfterSpell</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `enabled` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_TeleportRequiresHalt</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `enabled` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_ChannelRequiresHalt</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `enabled` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_InteractionChannelsRequireHalt</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `enabled` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_AbilitySpecificChannelRequiresHalt</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ability_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `default` | `bool` | `optional` | `` |  |
| 3 | `enabled` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_SearchString</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `search` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_Pause</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CDOTAClientMsg_ShopViewMode</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `mode` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_SetUnitShareFlag</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `flag` | `uint32` | `optional` | `` |  |
| 3 | `state` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_SwapRequest</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAClientMsg_SwapAccept</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAClientMsg_WorldLine</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `worldline` | `.CDOTAMsg_WorldLine` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_RequestGraphUpdate</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CDOTAClientMsg_ChatWheel</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `chat_message_id` | `uint32` | `optional` | `` | default = 4294967295 |
| 2 | `param_hero_id` | `int32` | `optional` | `` |  |
| 3 | `emoticon_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_SendStatPopup</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `statpopup` | `.CDOTAMsg_SendStatPopup` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_DismissAllStatPopups</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `dismissallmsg` | `.CDOTAMsg_DismissAllStatPopups` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_BeginLastHitChallenge</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `chosen_lane` | `uint32` | `optional` | `` |  |
| 2 | `helper_enabled` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_UpdateQuickBuyItem</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_ability_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `purchasable` | `bool` | `optional` | `` | default = false |
| 3 | `top_level_item_ability_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAClientMsg_UpdateQuickBuy</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `items` | `.CDOTAClientMsg_UpdateQuickBuyItem` | `repeated` | `` |  |
| 2 | `goal_item_ability_ids` | `int32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_QuickBuyAction</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 1</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `action` | `.CDOTAClientMsg_QuickBuyAction.EActionType` | `optional` | `` | default = INVALID |
| 2 | `item_ability_id` | `int32` | `optional` | `` | default = -1 |
| 3 | `slot_index` | `int32` | `optional` | `` |  |
| 4 | `purchaser_entindex` | `int32` | `optional` | `` | default = -1 |
| 5 | `new_slot_index` | `int32` | `optional` | `` |  |
| 6 | `top_level_item` | `bool` | `optional` | `` |  |
| 7 | `old_slot_ability_ids` | `int32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_RecordVote</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `choice_index` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_WillPurchaseAlert</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_ability_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `gold_remaining` | `uint32` | `optional` | `` |  |
| 3 | `suggestion_player_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAClientMsg_BuyBackStateAlert</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CDOTAClientMsg_QuickBuyAlert</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_ability_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `gold_cost` | `int32` | `optional` | `` |  |
| 3 | `item_cooldown_seconds` | `int32` | `optional` | `` |  |
| 4 | `show_buyback` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_PlayerShowCase</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `showcase` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_CameraZoomAmount</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `zoom_amount` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_BroadcasterUsingCameraman</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `cameraman` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_BroadcasterUsingAssistedCameraOperator</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `enabled` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_FillEmptySlotsWithBots</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `fillwithbots` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_HeroStatueLike</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `owner_player_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAClientMsg_EventCNY2015Cmd</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `data` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_DemoHero</code> — fields: 8; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hero_id` | `int32` | `optional` | `` |  |
| 2 | `hero_id_to_spawn` | `int32` | `optional` | `` |  |
| 3 | `preview_items` | `.CDOTAClientMsg_DemoHero.PreviewItem` | `repeated` | `` |  |
| 4 | `item_ids` | `uint64` | `repeated` | `` |  |
| 5 | `style_index_override` | `uint32` | `optional` | `` | default = 255 |
| 6 | `keep_existing_demohero` | `bool` | `optional` | `` |  |
| 7 | `item_data` | `.CSOEconItem` | `repeated` | `` |  |
| 8 | `hero_variant` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_DemoHero.PreviewItem</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAClientMsg_DemoHero`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_def` | `uint32` | `optional` | `` |  |
| 2 | `item_style` | `uint32` | `optional` | `` | default = 255 |

</details>

<details>
<summary><code>CDOTAClientMsg_ChallengeSelect</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `uint32` | `optional` | `` |  |
| 2 | `slot_id` | `uint32` | `optional` | `` |  |
| 3 | `sequence_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_ChallengeReroll</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_id` | `.EEvent` | `optional` | `` | default = EVENT_ID_NONE |
| 2 | `slot_id` | `uint32` | `optional` | `` |  |
| 3 | `sequence_id` | `uint32` | `optional` | `` |  |
| 4 | `hero_id` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_CoinWager</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `wager_amount` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_CoinWagerToken</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `wager_token_item_id` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_RankWager</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `announce_wager` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_PlayerBounty</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAClientMsg_EventPointsTip</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `recipient_player_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAClientMsg_ExecuteOrders</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `orders` | `.CDOTAMsg_UnitOrder` | `repeated` | `` |  |
| 2 | `last_order_latency` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_XPAlert</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_entindex` | `int32` | `optional` | `` | default = -1 |
| 2 | `damage_taken` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_TalentTreeAlert</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_entindex` | `int32` | `optional` | `` | default = -1 |
| 2 | `ability_id` | `int32` | `optional` | `` | default = -1 |
| 3 | `slot` | `int32` | `optional` | `` |  |
| 4 | `learned` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_KillcamDamageTaken</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_entindex` | `int32` | `optional` | `` | default = -1 |
| 2 | `damage_taken` | `uint32` | `optional` | `` |  |
| 3 | `item_type` | `uint32` | `optional` | `` |  |
| 4 | `item_ability_id` | `int32` | `optional` | `` | default = -1 |
| 5 | `hero_name` | `string` | `optional` | `` |  |
| 6 | `damage_color` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_KillMyHero</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CDOTAClientMsg_QuestStatus</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `quest_id` | `uint32` | `optional` | `` |  |
| 2 | `challenge_id` | `uint32` | `optional` | `` |  |
| 3 | `progress` | `uint32` | `optional` | `` |  |
| 4 | `goal` | `uint32` | `optional` | `` |  |
| 5 | `query` | `uint32` | `optional` | `` |  |
| 6 | `fail_gametime` | `float` | `optional` | `` |  |
| 7 | `item_ability_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAClientMsg_ToggleAutoattack</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `mode` | `int32` | `optional` | `` |  |
| 2 | `show_message` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_SpecialAbility</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ability_index` | `uint32` | `optional` | `` |  |
| 2 | `target_entindex` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAClientMsg_SetEnemyStartingPosition</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `enemy_player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `enemy_starting_position` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_SetDesiredWardPlacement</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ward_index` | `uint32` | `optional` | `` |  |
| 2 | `ward_x` | `float` | `optional` | `` |  |
| 3 | `ward_y` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_RollDice</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `channel_type` | `uint32` | `optional` | `` |  |
| 2 | `roll_min` | `uint32` | `optional` | `` |  |
| 3 | `roll_max` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_FlipCoin</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `channel_type` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_RequestItemSuggestions</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CDOTAClientMsg_SuggestItemPreference</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_preferences` | `.CDOTAClientMsg_SuggestItemPreference.ItemPreference` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_SuggestItemPreference.ItemPreference</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CDOTAClientMsg_SuggestItemPreference`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `preference` | `.EItemSuggestPreference` | `optional` | `` | default = k_EItemSuggestPreference_None |

</details>

<details>
<summary><code>CDOTAClientMsg_SuggestItemRefresh</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `is_out_of_items` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_SuggestItemGetVariants</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `is_out_of_items` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_SuggestItemSelectVariant</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `variant` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_MakeTeamCaptain</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAClientMsg_HelpTipSystemStateChanged</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `tip_displayed` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_RequestBulkCombatLog</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `game_time` | `float` | `optional` | `` |  |
| 2 | `duration` | `float` | `optional` | `` |  |
| 3 | `recent_player_death` | `bool` | `optional` | `` |  |
| 4 | `player_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAClientMsg_AbilityDraftRequestAbility</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `requested_ability_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `ctrl_is_down` | `bool` | `optional` | `` |  |
| 3 | `requested_hero_id` | `int32` | `optional` | `` |  |
| 4 | `requested_facet_key` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_GuideSelectOption</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `option` | `uint32` | `optional` | `` |  |
| 2 | `force_recalculate` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_GuideSelected</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `guide_workshop_id` | `uint64` | `optional` | `` |  |
| 2 | `is_plus_guide` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_DamageReport</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_hero_id` | `int32` | `optional` | `` |  |
| 2 | `source_hero_id` | `int32` | `optional` | `` |  |
| 3 | `damage_amount` | `int32` | `optional` | `` |  |
| 4 | `broadcast` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_SalutePlayer</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `event_id` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_GiftPlayer</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `item_def_index` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_GiftEveryone</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item_def_index` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_TipAlert</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `tip_text` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_EmptyTeleportAlert</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_entindex` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAClientMsg_SetCavernMapVariant</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `map_variant` | `uint32` | `optional` | `` | default = 255 |

</details>

<details>
<summary><code>CDOTAClientMsg_PauseGameOrder</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `order_id` | `int32` | `optional` | `` |  |
| 2 | `data` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_VersusScene_PlayerBehavior</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `behavior` | `.EDOTAVersusScenePlayerBehavior` | `optional` | `` | default = VS_PLAYER_BEHAVIOR_PLAY_ACTIVITY |
| 2 | `play_activity` | `.VersusScene_PlayActivity` | `optional` | `` |  |
| 3 | `chat_wheel` | `.VersusScene_ChatWheel` | `optional` | `` |  |
| 4 | `playback_rate` | `.VersusScene_PlaybackRate` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_EmptyItemSlotAlert</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_entindex` | `int32` | `optional` | `` | default = -1 |
| 2 | `slot_index` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_AddOverwatchReportMarker</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `reason` | `.EOverwatchReportReason` | `optional` | `` | default = k_EOverwatchReportReason_Unknown |
| 4 | `seconds_ago` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_AddCommunicationsReportMarker</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_player_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAClientMsg_AddCommunicationsBlockMarker</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_player_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAClientMsg_AghsStatusAlert</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `source_player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `target_player_id` | `int32` | `optional` | `` | default = -1 |
| 3 | `target_entindex` | `int32` | `optional` | `` | default = -1 |
| 4 | `alert_type` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_PerfReport</code> — fields: 20; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `average_frame_time` | `float` | `optional` | `` |  |
| 2 | `max_frame_time` | `float` | `optional` | `` |  |
| 3 | `average_compute_time` | `float` | `optional` | `` |  |
| 4 | `max_compute_time` | `float` | `optional` | `` |  |
| 5 | `average_client_tick_time` | `float` | `optional` | `` |  |
| 6 | `max_client_tick_time` | `float` | `optional` | `` |  |
| 7 | `average_client_simulate_time` | `float` | `optional` | `` |  |
| 8 | `max_client_simulate_time` | `float` | `optional` | `` |  |
| 9 | `average_output_time` | `float` | `optional` | `` |  |
| 10 | `max_output_time` | `float` | `optional` | `` |  |
| 11 | `average_wait_for_rendering_to_complete_time` | `float` | `optional` | `` |  |
| 12 | `max_wait_for_rendering_to_complete_time` | `float` | `optional` | `` |  |
| 13 | `average_swap_time` | `float` | `optional` | `` |  |
| 14 | `max_swap_time` | `float` | `optional` | `` |  |
| 15 | `average_frame_update_time` | `float` | `optional` | `` |  |
| 16 | `max_frame_update_time` | `float` | `optional` | `` |  |
| 17 | `average_idle_time` | `float` | `optional` | `` |  |
| 18 | `max_idle_time` | `float` | `optional` | `` |  |
| 19 | `average_input_processing_time` | `float` | `optional` | `` |  |
| 20 | `max_input_processing_time` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_ContextualTips_Subscribe_Entry</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `unsubscribe` | `bool` | `optional` | `` |  |
| 2 | `tip_id` | `int32` | `optional` | `` |  |
| 3 | `prior_display_count` | `int32` | `optional` | `` |  |
| 4 | `variants_seen` | `int32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_ContextualTips_Subscribe</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `tips` | `.CDOTAClientMsg_ContextualTips_Subscribe_Entry` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_ChatMessage</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `channel_type` | `uint32` | `optional` | `` |  |
| 2 | `message_text` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_DuelAccepted</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `challenger_player_id` | `int32` | `optional` | `` | default = -1 |
| 2 | `accepter_player_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAClientMsg_ChooseNeutralItem</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `neutral_item_index` | `int32` | `optional` | `` |  |
| 2 | `target_entindex` | `int32` | `optional` | `` | default = -1 |
| 3 | `slot_index` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_RerollNeutralItem</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_entindex` | `int32` | `optional` | `` | default = -1 |
| 2 | `slot_index` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_PlayerDraftPick</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAClientMsg_PlayerDraftSuggest</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player_id` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAClientMsg_PlayerDraftPreferRole</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `role_idx` | `int32` | `optional` | `` |  |
| 2 | `desired` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_PlayerDraftPreferTeam</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `team` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_AbilityAlert</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ability_entindex` | `uint32` | `optional` | `` | default = 16777215 |
| 2 | `ctrl_held` | `bool` | `optional` | `` |  |
| 3 | `owner_entindex` | `int32` | `optional` | `` | default = -1 |
| 4 | `ability_id` | `int32` | `optional` | `` | default = -1 |
| 5 | `primary_charges` | `uint32` | `optional` | `` |  |
| 6 | `secondary_charges` | `uint32` | `optional` | `` |  |
| 7 | `reclaim_time` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_SelectOverworldTokenRewards</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `token_ids` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_FacetAlert</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `facet_strhash` | `uint32` | `optional` | `` |  |
| 2 | `hero_entindex` | `uint32` | `optional` | `` | default = 16777215 |
| 3 | `ctrl_held` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_InnateAlert</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ability_entindex` | `uint32` | `optional` | `` | default = 16777215 |
| 2 | `ctrl_held` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_SelectOverworldID</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `overworld_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_RoshanTimer</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `negative` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_TormentorTimer</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `negative` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_CraftNeutralItem</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CDOTAClientMsg_ChooseCraftedNeutralItem</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `neutral_item_index` | `int32` | `optional` | `` |  |
| 2 | `item_tier` | `int32` | `optional` | `` |  |
| 3 | `enhancement_index` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_TimerAlert</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `timer_alert_type` | `.ETimerAlertType` | `optional` | `` | default = k_TimerAlertType_PowerRune |

</details>

<details>
<summary><code>CDOTAClientMsg_MadstoneAlert</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_entindex` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CDOTAClientMsg_UpdateAutoCourierSettings</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `auto_deliver` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_AutoCourierExecute</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_entindex` | `int32` | `optional` | `` | default = -1 |
| 2 | `is_auto_deliver` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_MonsterHunter_SelectInvestigation</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `investigation_index` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CDOTAClientMsg_MonsterHunter_HuntAlert</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `investigation_state_index` | `uint32` | `optional` | `` |  |
| 2 | `ctrl_pressed` | `bool` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>EDotaClientMessages</code> — values: 124</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `DOTA_CM_MapLine` | 301 |
| `DOTA_CM_AspectRatio` | 302 |
| `DOTA_CM_MapPing` | 303 |
| `DOTA_CM_UnitsAutoAttack` | 304 |
| `DOTA_CM_SearchString` | 307 |
| `DOTA_CM_Pause` | 308 |
| `DOTA_CM_ShopViewMode` | 309 |
| `DOTA_CM_SetUnitShareFlag` | 310 |
| `DOTA_CM_SwapRequest` | 311 |
| `DOTA_CM_SwapAccept` | 312 |
| `DOTA_CM_WorldLine` | 313 |
| `DOTA_CM_RequestGraphUpdate` | 314 |
| `DOTA_CM_ItemAlert` | 315 |
| `DOTA_CM_ChatWheel` | 316 |
| `DOTA_CM_SendStatPopup` | 317 |
| `DOTA_CM_BeginLastHitChallenge` | 318 |
| `DOTA_CM_UpdateQuickBuy` | 319 |
| `DOTA_CM_UpdateCoachListen` | 320 |
| `DOTA_CM_CoachHUDPing` | 321 |
| `DOTA_CM_RecordVote` | 322 |
| `DOTA_CM_UnitsAutoAttackAfterSpell` | 323 |
| `DOTA_CM_WillPurchaseAlert` | 324 |
| `DOTA_CM_PlayerShowCase` | 325 |
| `DOTA_CM_TeleportRequiresHalt` | 326 |
| `DOTA_CM_CameraZoomAmount` | 327 |
| `DOTA_CM_BroadcasterUsingCamerman` | 328 |
| `DOTA_CM_BroadcasterUsingAssistedCameraOperator` | 329 |
| `DOTA_CM_EnemyItemAlert` | 330 |
| `DOTA_CM_FreeInventory` | 331 |
| `DOTA_CM_BuyBackStateAlert` | 332 |
| `DOTA_CM_QuickBuyAlert` | 333 |
| `DOTA_CM_HeroStatueLike` | 334 |
| `DOTA_CM_ModifierAlert` | 335 |
| `DOTA_CM_TeamShowcaseEditor` | 336 |
| `DOTA_CM_HPManaAlert` | 337 |
| `DOTA_CM_GlyphAlert` | 338 |
| `DOTA_CM_TeamShowcaseClientData` | 339 |
| `DOTA_CM_PlayTeamShowcase` | 340 |
| `DOTA_CM_EventCNY2015Cmd` | 341 |
| `DOTA_CM_FillEmptySlotsWithBots` | 342 |
| `DOTA_CM_DemoHero` | 343 |
| `DOTA_CM_AbilityLearnModeToggled` | 344 |
| `DOTA_CM_AbilityStartUse` | 345 |
| `DOTA_CM_ChallengeSelect` | 346 |
| `DOTA_CM_ChallengeReroll` | 347 |
| `DOTA_CM_ClickedBuff` | 348 |
| `DOTA_CM_CoinWager` | 349 |
| `DOTA_CM_ExecuteOrders` | 350 |
| `DOTA_CM_XPAlert` | 351 |
| `DOTA_CM_EventPointsTip` | 353 |
| `DOTA_CM_KillMyHero` | 355 |
| `DOTA_CM_QuestStatus` | 356 |
| `DOTA_CM_ToggleAutoattack` | 357 |
| `DOTA_CM_SpecialAbility` | 358 |
| `DOTA_CM_KillcamDamageTaken` | 359 |
| `DOTA_CM_SetEnemyStartingPosition` | 360 |
| `DOTA_CM_SetDesiredWardPlacement` | 361 |
| `DOTA_CM_RollDice` | 362 |
| `DOTA_CM_FlipCoin` | 363 |
| `DOTA_CM_RequestItemSuggestions` | 364 |
| `DOTA_CM_MakeTeamCaptain` | 365 |
| `DOTA_CM_CoinWagerToken` | 366 |
| `DOTA_CM_RankWager` | 367 |
| `DOTA_CM_DismissAllStatPopups` | 368 |
| `DOTA_CM_HelpTipSystemStateChanged` | 369 |
| `DOTA_CM_ChannelRequiresHalt` | 370 |
| `DOTA_CM_RequestBulkCombatLog` | 371 |
| `DOTA_CM_AbilityDraftRequestAbility` | 372 |
| `DOTA_CM_GuideSelectOption` | 373 |
| `DOTA_CM_GuideSelected` | 374 |
| `DOTA_CM_DamageReport` | 375 |
| `DOTA_CM_SalutePlayer` | 376 |
| `DOTA_CM_SprayWheel` | 377 |
| `DOTA_CM_TipAlert` | 378 |
| `DOTA_CM_EmptyTeleportAlert` | 379 |
| `DOTA_CM_RadarAlert` | 380 |
| `DOTA_CM_TalentTreeAlert` | 381 |
| `DOTA_CM_SetCavernMapVariant` | 382 |
| `DOTA_CM_PauseGameOrder` | 383 |
| `DOTA_CM_VersusScene_PlayerBehavior` | 384 |
| `DOTA_CM_PlayerBounty` | 385 |
| `DOTA_CM_PlayerBountyCancel` | 386 |
| `DOTA_CM_EmptyItemSlotAlert` | 388 |
| `DOTA_CM_AddOverwatchReportMarker` | 389 |
| `DOTA_CM_AghsStatusAlert` | 390 |
| `DOTA_CM_PerfReport` | 391 |
| `DOTA_CM_ContextualTips_Subscribe` | 393 |
| `DOTA_CM_ChatMessage` | 394 |
| `DOTA_CM_AddCommunicationsReportMarker` | 395 |
| `DOTA_CM_AddCommunicationsBlockMarker` | 396 |
| `DOTA_CM_NeutralCampAlert` | 397 |
| `DOTA_CM_DuelAccepted` | 398 |
| `DOTA_CM_ChooseNeutralItem` | 399 |
| `DOTA_CM_PlayerDraftPick` | 800 |
| `DOTA_CM_PlayerDraftSuggest` | 801 |
| `DOTA_CM_PlayerDraftPreferRole` | 802 |
| `DOTA_CM_PlayerDraftPreferTeam` | 803 |
| `DOTA_CM_ChatWheelAlert` | 804 |
| `DOTA_CM_AbilityAlert` | 805 |
| `DOTA_CM_AllyAbilityAlert` | 806 |
| `DOTA_CM_GiftPlayer` | 807 |
| `DOTA_CM_GiftEveryone` | 808 |
| `DOTA_CM_SelectOverworldTokenRewards` | 809 |
| `DOTA_CM_FacetAlert` | 810 |
| `DOTA_CM_InnateAlert` | 811 |
| `DOTA_CM_SelectOverworldID` | 812 |
| `DOTA_CM_RerollNeutralItem` | 813 |
| `DOTA_CM_RoshanTimer` | 814 |
| `DOTA_CM_SuggestItemPreference` | 815 |
| `DOTA_CM_CraftNeutralItem` | 816 |
| `DOTA_CM_ChooseCraftedNeutral` | 817 |
| `DOTA_CM_TimerAlert` | 818 |
| `DOTA_CM_MadstoneAlert` | 819 |
| `DOTA_CM_UpdateAutoCourierSettings` | 820 |
| `DOTA_CM_AutoCourierExecute` | 821 |
| `DOTA_CM_QuickBuyAction` | 822 |
| `DOTA_CM_InteractionChannelsRequireHalt` | 823 |
| `DOTA_CM_SuggestItemRefresh` | 824 |
| `DOTA_CM_SuggestItemVariantRequest` | 825 |
| `DOTA_CM_SuggestItemVariantSelect` | 826 |
| `DOTA_CM_MonsterHunter_SelectInvestigation` | 827 |
| `DOTA_CM_MonsterHunter_HuntAlert` | 828 |
| `DOTA_CM_AbilitySpecificChannelRequiresHalt` | 829 |
| `DOTA_CM_TormentorTimer` | 830 |

</details>

<details>
<summary><code>CDOTAClientMsg_UnitsAutoAttackMode.EMode</code> — values: 4</summary>

- Parent: `CDOTAClientMsg_UnitsAutoAttackMode`

| Name | Number |
|---|---:|
| `INVALID` | -1 |
| `NEVER` | 0 |
| `AFTER_SPELLCAST` | 1 |
| `ALWAYS` | 2 |

</details>

<details>
<summary><code>CDOTAClientMsg_UnitsAutoAttackMode.EUnitType</code> — values: 2</summary>

- Parent: `CDOTAClientMsg_UnitsAutoAttackMode`

| Name | Number |
|---|---:|
| `NORMAL` | 0 |
| `SUMMONED` | 1 |

</details>

<details>
<summary><code>CDOTAClientMsg_QuickBuyAction.EActionType</code> — values: 12</summary>

- Parent: `CDOTAClientMsg_QuickBuyAction`

| Name | Number |
|---|---:|
| `INVALID` | -1 |
| `PURCHASE` | 0 |
| `QUEUE` | 1 |
| `REMOVE` | 2 |
| `CLEAR` | 3 |
| `CLEAR_AND_QUEUE` | 4 |
| `MARK_FOR_BUY` | 5 |
| `CLEAR_MARK_FOR_BUY` | 6 |
| `ENABLE_BUYBACK_PROTECTION` | 7 |
| `DISABLE_BUYBACK_PROTECTION` | 8 |
| `QUEUE_FIRST_AND_MARK_FOR_BUY` | 9 |
| `CHANGE_SLOT` | 10 |

</details>
