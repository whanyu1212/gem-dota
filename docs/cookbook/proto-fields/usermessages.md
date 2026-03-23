# usermessages.proto

- Module: `usermessages_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **1**
- Messages: **107** (top-level: 56)
- Enums: **5** (top-level: 5)

## Imports

- `networkbasetypes.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CUserMessageAchievementEvent</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `achievement` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageCloseCaption</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hash` | `fixed32` | `optional` | `` |  |
| 2 | `duration` | `float` | `optional` | `` |  |
| 3 | `from_player` | `bool` | `optional` | `` |  |
| 4 | `ent_index` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CUserMessageCloseCaptionDirect</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hash` | `fixed32` | `optional` | `` |  |
| 2 | `duration` | `float` | `optional` | `` |  |
| 3 | `from_player` | `bool` | `optional` | `` |  |
| 4 | `ent_index` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CUserMessageCloseCaptionPlaceholder</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `string` | `string` | `optional` | `` |  |
| 2 | `duration` | `float` | `optional` | `` |  |
| 3 | `from_player` | `bool` | `optional` | `` |  |
| 4 | `ent_index` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CUserMessageCurrentTimescale</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `current` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageDesiredTimescale</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `desired` | `float` | `optional` | `` |  |
| 2 | `acceleration` | `float` | `optional` | `` |  |
| 3 | `minblendrate` | `float` | `optional` | `` |  |
| 4 | `blenddeltamultiplier` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageFade</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `duration` | `uint32` | `optional` | `` |  |
| 2 | `hold_time` | `uint32` | `optional` | `` |  |
| 3 | `flags` | `uint32` | `optional` | `` |  |
| 4 | `color` | `fixed32` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageShake</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `command` | `uint32` | `optional` | `` |  |
| 2 | `amplitude` | `float` | `optional` | `` |  |
| 3 | `frequency` | `float` | `optional` | `` |  |
| 4 | `duration` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageShakeDir</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `shake` | `.CUserMessageShake` | `optional` | `` |  |
| 2 | `direction` | `.CMsgVector` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageWaterShake</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `command` | `uint32` | `optional` | `` |  |
| 2 | `amplitude` | `float` | `optional` | `` |  |
| 3 | `frequency` | `float` | `optional` | `` |  |
| 4 | `duration` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageScreenTilt</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `command` | `uint32` | `optional` | `` |  |
| 2 | `ease_in_out` | `bool` | `optional` | `` |  |
| 3 | `angle` | `.CMsgVector` | `optional` | `` |  |
| 4 | `duration` | `float` | `optional` | `` |  |
| 5 | `time` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageSayText</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `playerindex` | `int32` | `optional` | `` | default = -1 |
| 2 | `text` | `string` | `optional` | `` |  |
| 3 | `chat` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageSayText2</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `entityindex` | `int32` | `optional` | `` | default = -1 |
| 2 | `chat` | `bool` | `optional` | `` |  |
| 3 | `messagename` | `string` | `optional` | `` |  |
| 4 | `param1` | `string` | `optional` | `` |  |
| 5 | `param2` | `string` | `optional` | `` |  |
| 6 | `param3` | `string` | `optional` | `` |  |
| 7 | `param4` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageHudMsg</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `channel` | `uint32` | `optional` | `` |  |
| 2 | `x` | `float` | `optional` | `` |  |
| 3 | `y` | `float` | `optional` | `` |  |
| 4 | `color1` | `fixed32` | `optional` | `` |  |
| 5 | `color2` | `fixed32` | `optional` | `` |  |
| 6 | `effect` | `uint32` | `optional` | `` |  |
| 11 | `message` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageHudText</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `message` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageTextMsg</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `dest` | `uint32` | `optional` | `` |  |
| 2 | `param` | `string` | `repeated` | `` |  |

</details>

<details>
<summary><code>CUserMessageGameTitle</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CUserMessageResetHUD</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CUserMessageSendAudio</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `soundname` | `string` | `optional` | `` |  |
| 2 | `stop` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageAudioParameter</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `parameter_type` | `uint32` | `optional` | `` |  |
| 2 | `name_hash_code` | `uint32` | `optional` | `` |  |
| 3 | `value` | `float` | `optional` | `` |  |
| 4 | `int_value` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageVoiceMask</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `gamerules_masks` | `uint32` | `repeated` | `` |  |
| 2 | `ban_masks` | `uint32` | `repeated` | `` |  |
| 3 | `mod_enable` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageRequestState</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CUserMessageRumble</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `index` | `int32` | `optional` | `` |  |
| 2 | `data` | `int32` | `optional` | `` |  |
| 3 | `flags` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageSayTextChannel</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `player` | `int32` | `optional` | `` |  |
| 2 | `channel` | `int32` | `optional` | `` |  |
| 3 | `text` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageColoredText</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `color` | `uint32` | `optional` | `` |  |
| 2 | `text` | `string` | `optional` | `` |  |
| 3 | `reset` | `bool` | `optional` | `` |  |
| 4 | `context_player_slot` | `int32` | `optional` | `` | default = -1 |
| 5 | `context_value` | `int32` | `optional` | `` |  |
| 6 | `context_team_id` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageItemPickup</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `itemname` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageAmmoDenied</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ammo_id` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageShowMenu</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `validslots` | `uint32` | `optional` | `` |  |
| 2 | `displaytime` | `uint32` | `optional` | `` |  |
| 3 | `needmore` | `bool` | `optional` | `` |  |
| 4 | `menustring` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageCreditsMsg</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `rolltype` | `.eRollType` | `optional` | `` | default = ROLL_NONE |
| 2 | `logo_length` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CEntityMessagePlayJingle</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `entity_msg` | `.CEntityMsg` | `optional` | `` |  |

</details>

<details>
<summary><code>CEntityMessageScreenOverlay</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `start_effect` | `bool` | `optional` | `` |  |
| 2 | `entity_msg` | `.CEntityMsg` | `optional` | `` |  |

</details>

<details>
<summary><code>CEntityMessageRemoveAllDecals</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `remove_decals` | `bool` | `optional` | `` |  |
| 2 | `entity_msg` | `.CEntityMsg` | `optional` | `` |  |

</details>

<details>
<summary><code>CEntityMessagePropagateForce</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `impulse` | `.CMsgVector` | `optional` | `` |  |
| 2 | `entity_msg` | `.CEntityMsg` | `optional` | `` |  |

</details>

<details>
<summary><code>CEntityMessageDoSpark</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `origin` | `.CMsgVector` | `optional` | `` |  |
| 2 | `entityindex` | `int32` | `optional` | `` | default = -1 |
| 3 | `radius` | `float` | `optional` | `` |  |
| 4 | `color` | `fixed32` | `optional` | `` |  |
| 5 | `beams` | `uint32` | `optional` | `` |  |
| 6 | `thick` | `float` | `optional` | `` |  |
| 7 | `duration` | `float` | `optional` | `` |  |
| 8 | `entity_msg` | `.CEntityMsg` | `optional` | `` |  |

</details>

<details>
<summary><code>CEntityMessageFixAngle</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `relative` | `bool` | `optional` | `` |  |
| 2 | `angle` | `.CMsgQAngle` | `optional` | `` |  |
| 3 | `entity_msg` | `.CEntityMsg` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageCameraTransition</code> — fields: 3; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `camera_type` | `uint32` | `optional` | `` |  |
| 2 | `duration` | `float` | `optional` | `` |  |
| 3 | `params_data_driven` | `.CUserMessageCameraTransition.Transition_DataDriven` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageCameraTransition.Transition_DataDriven</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMessageCameraTransition`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `filename` | `string` | `optional` | `` |  |
| 2 | `attach_ent_index` | `int32` | `optional` | `` | default = -1 |
| 3 | `duration` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager</code> — fields: 41; oneofs: 0; nested messages: 39; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `type` | `.PARTICLE_MESSAGE` | `required` | `` | default = GAME_PARTICLE_MANAGER_EVENT_CREATE |
| 2 | `index` | `uint32` | `required` | `` |  |
| 3 | `release_particle_index` | `.CUserMsg_ParticleManager.ReleaseParticleIndex` | `optional` | `` |  |
| 4 | `create_particle` | `.CUserMsg_ParticleManager.CreateParticle` | `optional` | `` |  |
| 5 | `destroy_particle` | `.CUserMsg_ParticleManager.DestroyParticle` | `optional` | `` |  |
| 6 | `destroy_particle_involving` | `.CUserMsg_ParticleManager.DestroyParticleInvolving` | `optional` | `` |  |
| 7 | `update_particle` | `.CUserMsg_ParticleManager.UpdateParticle_OBSOLETE` | `optional` | `` |  |
| 8 | `update_particle_fwd` | `.CUserMsg_ParticleManager.UpdateParticleFwd_OBSOLETE` | `optional` | `` |  |
| 9 | `update_particle_orient` | `.CUserMsg_ParticleManager.UpdateParticleOrient_OBSOLETE` | `optional` | `` |  |
| 10 | `update_particle_fallback` | `.CUserMsg_ParticleManager.UpdateParticleFallback` | `optional` | `` |  |
| 11 | `update_particle_offset` | `.CUserMsg_ParticleManager.UpdateParticleOffset` | `optional` | `` |  |
| 12 | `update_particle_ent` | `.CUserMsg_ParticleManager.UpdateParticleEnt` | `optional` | `` |  |
| 14 | `update_particle_should_draw` | `.CUserMsg_ParticleManager.UpdateParticleShouldDraw` | `optional` | `` |  |
| 15 | `update_particle_set_frozen` | `.CUserMsg_ParticleManager.UpdateParticleSetFrozen` | `optional` | `` |  |
| 16 | `change_control_point_attachment` | `.CUserMsg_ParticleManager.ChangeControlPointAttachment` | `optional` | `` |  |
| 17 | `update_entity_position` | `.CUserMsg_ParticleManager.UpdateEntityPosition` | `optional` | `` |  |
| 18 | `set_particle_fow_properties` | `.CUserMsg_ParticleManager.SetParticleFoWProperties` | `optional` | `` |  |
| 19 | `set_particle_text` | `.CUserMsg_ParticleManager.SetParticleText` | `optional` | `` |  |
| 20 | `set_particle_should_check_fow` | `.CUserMsg_ParticleManager.SetParticleShouldCheckFoW` | `optional` | `` |  |
| 21 | `set_control_point_model` | `.CUserMsg_ParticleManager.SetControlPointModel` | `optional` | `` |  |
| 22 | `set_control_point_snapshot` | `.CUserMsg_ParticleManager.SetControlPointSnapshot` | `optional` | `` |  |
| 23 | `set_texture_attribute` | `.CUserMsg_ParticleManager.SetTextureAttribute` | `optional` | `` |  |
| 24 | `set_scene_object_generic_flag` | `.CUserMsg_ParticleManager.SetSceneObjectGenericFlag` | `optional` | `` |  |
| 25 | `set_scene_object_tint_and_desat` | `.CUserMsg_ParticleManager.SetSceneObjectTintAndDesat` | `optional` | `` |  |
| 26 | `destroy_particle_named` | `.CUserMsg_ParticleManager.DestroyParticleNamed` | `optional` | `` |  |
| 27 | `particle_skip_to_time` | `.CUserMsg_ParticleManager.ParticleSkipToTime` | `optional` | `` |  |
| 28 | `particle_can_freeze` | `.CUserMsg_ParticleManager.ParticleCanFreeze` | `optional` | `` |  |
| 29 | `set_named_value_context` | `.CUserMsg_ParticleManager.SetParticleNamedValueContext` | `optional` | `` |  |
| 30 | `update_particle_transform` | `.CUserMsg_ParticleManager.UpdateParticleTransform` | `optional` | `` |  |
| 31 | `particle_freeze_transition_override` | `.CUserMsg_ParticleManager.ParticleFreezeTransitionOverride` | `optional` | `` |  |
| 32 | `freeze_particle_involving` | `.CUserMsg_ParticleManager.FreezeParticleInvolving` | `optional` | `` |  |
| 33 | `add_modellist_override_element` | `.CUserMsg_ParticleManager.AddModellistOverrideElement` | `optional` | `` |  |
| 34 | `clear_modellist_override` | `.CUserMsg_ParticleManager.ClearModellistOverride` | `optional` | `` |  |
| 35 | `create_physics_sim` | `.CUserMsg_ParticleManager.CreatePhysicsSim` | `optional` | `` |  |
| 36 | `destroy_physics_sim` | `.CUserMsg_ParticleManager.DestroyPhysicsSim` | `optional` | `` |  |
| 37 | `set_vdata` | `.CUserMsg_ParticleManager.SetVData` | `optional` | `` |  |
| 38 | `set_material_override` | `.CUserMsg_ParticleManager.SetMaterialOverride` | `optional` | `` |  |
| 39 | `add_fan` | `.CUserMsg_ParticleManager.AddFan` | `optional` | `` |  |
| 40 | `update_fan` | `.CUserMsg_ParticleManager.UpdateFan` | `optional` | `` |  |
| 41 | `set_particle_cluster_growth` | `.CUserMsg_ParticleManager.SetParticleClusterGrowth` | `optional` | `` |  |
| 42 | `remove_fan` | `.CUserMsg_ParticleManager.RemoveFan` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.ReleaseParticleIndex</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.CreateParticle</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `particle_name_index` | `fixed64` | `optional` | `` |  |
| 2 | `attach_type` | `int32` | `optional` | `` |  |
| 3 | `entity_handle` | `uint32` | `optional` | `` | default = 16777215 |
| 4 | `entity_handle_for_modifiers` | `uint32` | `optional` | `` | default = 16777215 |
| 5 | `apply_voice_ban_rules` | `bool` | `optional` | `` |  |
| 6 | `team_behavior` | `int32` | `optional` | `` |  |
| 7 | `control_point_configuration` | `string` | `optional` | `` |  |
| 8 | `cluster` | `bool` | `optional` | `` |  |
| 9 | `endcap_time` | `float` | `optional` | `` |  |
| 10 | `aggregation_position` | `.CMsgVector` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.DestroyParticle</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `destroy_immediately` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.DestroyParticleInvolving</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `destroy_immediately` | `bool` | `optional` | `` |  |
| 3 | `entity_handle` | `uint32` | `optional` | `` | default = 16777215 |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.DestroyParticleNamed</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `particle_name_index` | `fixed64` | `optional` | `` |  |
| 2 | `entity_handle` | `uint32` | `optional` | `` | default = 16777215 |
| 3 | `destroy_immediately` | `bool` | `optional` | `` |  |
| 4 | `play_endcap` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.UpdateParticle_OBSOLETE</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `control_point` | `int32` | `optional` | `` |  |
| 2 | `position` | `.CMsgVector` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.UpdateParticleFwd_OBSOLETE</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `control_point` | `int32` | `optional` | `` |  |
| 2 | `forward` | `.CMsgVector` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.UpdateParticleOrient_OBSOLETE</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `control_point` | `int32` | `optional` | `` |  |
| 2 | `forward` | `.CMsgVector` | `optional` | `` |  |
| 3 | `deprecated_right` | `.CMsgVector` | `optional` | `` |  |
| 4 | `up` | `.CMsgVector` | `optional` | `` |  |
| 5 | `left` | `.CMsgVector` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.UpdateParticleTransform</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `control_point` | `int32` | `optional` | `` |  |
| 2 | `position` | `.CMsgVector` | `optional` | `` |  |
| 3 | `orientation` | `.CMsgQuaternion` | `optional` | `` |  |
| 4 | `interpolation_interval` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.UpdateParticleFallback</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `control_point` | `int32` | `optional` | `` |  |
| 2 | `position` | `.CMsgVector` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.UpdateParticleOffset</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `control_point` | `int32` | `optional` | `` |  |
| 2 | `origin_offset` | `.CMsgVector` | `optional` | `` |  |
| 3 | `angle_offset` | `.CMsgQAngle` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.UpdateParticleEnt</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `control_point` | `int32` | `optional` | `` |  |
| 2 | `entity_handle` | `uint32` | `optional` | `` | default = 16777215 |
| 3 | `attach_type` | `int32` | `optional` | `` |  |
| 4 | `attachment` | `int32` | `optional` | `` |  |
| 5 | `fallback_position` | `.CMsgVector` | `optional` | `` |  |
| 6 | `include_wearables` | `bool` | `optional` | `` |  |
| 7 | `offset_position` | `.CMsgVector` | `optional` | `` |  |
| 8 | `offset_angles` | `.CMsgQAngle` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.UpdateParticleSetFrozen</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `set_frozen` | `bool` | `optional` | `` |  |
| 2 | `transition_duration` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.UpdateParticleShouldDraw</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `should_draw` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.ChangeControlPointAttachment</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `attachment_old` | `int32` | `optional` | `` |  |
| 2 | `attachment_new` | `int32` | `optional` | `` |  |
| 3 | `entity_handle` | `uint32` | `optional` | `` | default = 16777215 |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.UpdateEntityPosition</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `entity_handle` | `uint32` | `optional` | `` | default = 16777215 |
| 2 | `position` | `.CMsgVector` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.SetParticleFoWProperties</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `fow_control_point` | `int32` | `optional` | `` |  |
| 2 | `fow_control_point2` | `int32` | `optional` | `` |  |
| 3 | `fow_radius` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.SetParticleShouldCheckFoW</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `check_fow` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.SetControlPointModel</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `control_point` | `int32` | `optional` | `` |  |
| 2 | `model_name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.SetControlPointSnapshot</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `control_point` | `int32` | `optional` | `` |  |
| 2 | `snapshot_name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.SetParticleText</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `text` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.SetTextureAttribute</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `attribute_name` | `string` | `optional` | `` |  |
| 2 | `texture_name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.SetSceneObjectGenericFlag</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `flag_value` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.SetSceneObjectTintAndDesat</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `tint` | `fixed32` | `optional` | `` |  |
| 2 | `desat` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.ParticleSkipToTime</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `skip_to_time` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.ParticleCanFreeze</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `can_freeze` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.ParticleFreezeTransitionOverride</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `freeze_transition_override` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.FreezeParticleInvolving</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `set_frozen` | `bool` | `optional` | `` |  |
| 2 | `transition_duration` | `float` | `optional` | `` |  |
| 3 | `entity_handle` | `uint32` | `optional` | `` | default = 16777215 |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.AddModellistOverrideElement</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `model_name` | `string` | `optional` | `` |  |
| 2 | `spawn_probability` | `float` | `optional` | `` |  |
| 3 | `groupid` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.ClearModellistOverride</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `groupid` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.SetParticleNamedValueContext</code> — fields: 4; oneofs: 0; nested messages: 4; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `float_values` | `.CUserMsg_ParticleManager.SetParticleNamedValueContext.FloatContextValue` | `repeated` | `` |  |
| 2 | `vector_values` | `.CUserMsg_ParticleManager.SetParticleNamedValueContext.VectorContextValue` | `repeated` | `` |  |
| 3 | `transform_values` | `.CUserMsg_ParticleManager.SetParticleNamedValueContext.TransformContextValue` | `repeated` | `` |  |
| 4 | `ehandle_values` | `.CUserMsg_ParticleManager.SetParticleNamedValueContext.EHandleContext` | `repeated` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.SetParticleNamedValueContext.FloatContextValue</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager.SetParticleNamedValueContext`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `value_name_hash` | `uint32` | `optional` | `` |  |
| 2 | `value` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.SetParticleNamedValueContext.VectorContextValue</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager.SetParticleNamedValueContext`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `value_name_hash` | `uint32` | `optional` | `` |  |
| 2 | `value` | `.CMsgVector` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.SetParticleNamedValueContext.TransformContextValue</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager.SetParticleNamedValueContext`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `value_name_hash` | `uint32` | `optional` | `` |  |
| 2 | `angles` | `.CMsgQAngle` | `optional` | `` |  |
| 3 | `translation` | `.CMsgVector` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.SetParticleNamedValueContext.EHandleContext</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager.SetParticleNamedValueContext`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `value_name_hash` | `uint32` | `optional` | `` |  |
| 2 | `ent_index` | `uint32` | `optional` | `` | default = 16777215 |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.CreatePhysicsSim</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `prop_group_name` | `string` | `optional` | `` |  |
| 2 | `use_high_quality_simulation` | `bool` | `optional` | `` |  |
| 3 | `max_particle_count` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.DestroyPhysicsSim</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.SetVData</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `vdata_name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.SetMaterialOverride</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `material_name` | `string` | `optional` | `` |  |
| 2 | `include_children` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.AddFan</code> — fields: 18; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `active` | `bool` | `optional` | `` |  |
| 2 | `bounds_mins` | `.CMsgVector` | `optional` | `` |  |
| 3 | `bounds_maxs` | `.CMsgVector` | `optional` | `` |  |
| 4 | `fan_origin` | `.CMsgVector` | `optional` | `` |  |
| 5 | `fan_origin_offset` | `.CMsgVector` | `optional` | `` |  |
| 6 | `fan_direction` | `.CMsgVector` | `optional` | `` |  |
| 7 | `force` | `float` | `optional` | `` |  |
| 8 | `fan_force_curve` | `string` | `optional` | `` |  |
| 9 | `falloff` | `bool` | `optional` | `` |  |
| 10 | `pull_towards_point` | `bool` | `optional` | `` |  |
| 11 | `curve_min_dist` | `float` | `optional` | `` |  |
| 12 | `curve_max_dist` | `float` | `optional` | `` |  |
| 13 | `fan_type` | `uint32` | `optional` | `` |  |
| 14 | `cone_start_radius` | `float` | `optional` | `` |  |
| 15 | `cone_end_radius` | `float` | `optional` | `` |  |
| 16 | `cone_length` | `float` | `optional` | `` |  |
| 17 | `entity_handle` | `uint32` | `optional` | `` | default = 16777215 |
| 18 | `attachment_name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.UpdateFan</code> — fields: 7; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `active` | `bool` | `optional` | `` |  |
| 2 | `fan_origin` | `.CMsgVector` | `optional` | `` |  |
| 3 | `fan_origin_offset` | `.CMsgVector` | `optional` | `` |  |
| 4 | `fan_direction` | `.CMsgVector` | `optional` | `` |  |
| 5 | `bounds_mins` | `.CMsgVector` | `optional` | `` |  |
| 6 | `bounds_maxs` | `.CMsgVector` | `optional` | `` |  |
| 7 | `fan_ramp_ratio` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.RemoveFan</code> — fields: 0; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| - | *(none)* |  |  |  |  |

</details>

<details>
<summary><code>CUserMsg_ParticleManager.SetParticleClusterGrowth</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMsg_ParticleManager`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `duration` | `float` | `optional` | `` |  |
| 2 | `origin` | `.CMsgVector` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_HudError</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `order_id` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMsg_CustomGameEvent</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_name` | `string` | `optional` | `` |  |
| 2 | `data` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageHapticsManagerPulse</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hand_id` | `int32` | `optional` | `` |  |
| 2 | `effect_amplitude` | `float` | `optional` | `` |  |
| 3 | `effect_frequency` | `float` | `optional` | `` |  |
| 4 | `effect_duration` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageHapticsManagerEffect</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `hand_id` | `int32` | `optional` | `` |  |
| 2 | `effect_name_hash_code` | `uint32` | `optional` | `` |  |
| 3 | `effect_scale` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageAnimStateGraphState</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `entity_index` | `int32` | `optional` | `` |  |
| 2 | `data` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageUpdateCssClasses</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `target_world_panel` | `int32` | `optional` | `` |  |
| 2 | `css_classes` | `string` | `optional` | `` |  |
| 3 | `is_add` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageServerFrameTime</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `frame_time` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageLagCompensationError</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `distance` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageRequestDllStatus</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `dll_action` | `string` | `optional` | `` |  |
| 2 | `full_report` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageRequestUtilAction</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 2 | `util1` | `int32` | `optional` | `` |  |
| 3 | `util2` | `int32` | `optional` | `` |  |
| 4 | `util3` | `int32` | `optional` | `` |  |
| 5 | `util4` | `int32` | `optional` | `` |  |
| 6 | `util5` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessage_UtilMsg_Response</code> — fields: 12; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `crc` | `fixed32` | `optional` | `` |  |
| 2 | `item_count` | `int32` | `optional` | `` |  |
| 3 | `crc2` | `fixed32` | `optional` | `` |  |
| 4 | `item_count2` | `int32` | `optional` | `` |  |
| 5 | `crc_part` | `int32` | `repeated` | `` |  |
| 6 | `crc_part2` | `int32` | `repeated` | `` |  |
| 7 | `client_timestamp` | `int32` | `optional` | `` |  |
| 8 | `platform` | `int32` | `optional` | `` |  |
| 9 | `itemdetails` | `.CUserMessage_UtilMsg_Response.ItemDetail` | `repeated` | `` |  |
| 10 | `itemgroup` | `int32` | `optional` | `` |  |
| 11 | `total_count` | `int32` | `optional` | `` |  |
| 12 | `total_count2` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessage_UtilMsg_Response.ItemDetail</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMessage_UtilMsg_Response`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `index` | `int32` | `optional` | `` |  |
| 2 | `hash` | `int32` | `optional` | `` |  |
| 3 | `crc` | `int32` | `optional` | `` |  |
| 4 | `name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessage_DllStatus</code> — fields: 8; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `file_report` | `string` | `optional` | `` |  |
| 2 | `command_line` | `string` | `optional` | `` |  |
| 3 | `total_files` | `uint32` | `optional` | `` |  |
| 4 | `process_id` | `uint32` | `optional` | `` |  |
| 5 | `osversion` | `int32` | `optional` | `` |  |
| 6 | `client_time` | `uint64` | `optional` | `` |  |
| 7 | `diagnostics` | `.CUserMessage_DllStatus.CVDiagnostic` | `repeated` | `` |  |
| 8 | `modules` | `.CUserMessage_DllStatus.CModule` | `repeated` | `` |  |

</details>

<details>
<summary><code>CUserMessage_DllStatus.CVDiagnostic</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMessage_DllStatus`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `id` | `uint32` | `optional` | `` |  |
| 2 | `extended` | `uint32` | `optional` | `` |  |
| 3 | `value` | `uint64` | `optional` | `` |  |
| 4 | `string_value` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessage_DllStatus.CModule</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMessage_DllStatus`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `base_addr` | `uint64` | `optional` | `` |  |
| 2 | `name` | `string` | `optional` | `` |  |
| 3 | `size` | `uint32` | `optional` | `` |  |
| 4 | `timestamp` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageRequestInventory</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `inventory` | `int32` | `optional` | `` |  |
| 2 | `offset` | `int32` | `optional` | `` |  |
| 3 | `options` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessage_Inventory_Response</code> — fields: 13; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `crc` | `fixed32` | `optional` | `` |  |
| 2 | `item_count` | `int32` | `optional` | `` |  |
| 5 | `osversion` | `int32` | `optional` | `` |  |
| 6 | `perf_time` | `int32` | `optional` | `` |  |
| 7 | `client_timestamp` | `int32` | `optional` | `` |  |
| 8 | `platform` | `int32` | `optional` | `` |  |
| 9 | `inventories` | `.CUserMessage_Inventory_Response.InventoryDetail` | `repeated` | `` |  |
| 10 | `inventories2` | `.CUserMessage_Inventory_Response.InventoryDetail` | `repeated` | `` |  |
| 11 | `inv_type` | `int32` | `optional` | `` |  |
| 12 | `build_version` | `int32` | `optional` | `` |  |
| 13 | `instance` | `int32` | `optional` | `` |  |
| 14 | `inventories3` | `.CUserMessage_Inventory_Response.InventoryDetail` | `repeated` | `` |  |
| 15 | `start_time` | `int64` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessage_Inventory_Response.InventoryDetail</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMessage_Inventory_Response`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `index` | `int32` | `optional` | `` |  |
| 2 | `primary` | `int64` | `optional` | `` |  |
| 3 | `offset` | `int64` | `optional` | `` |  |
| 4 | `first` | `int64` | `optional` | `` |  |
| 5 | `base` | `int64` | `optional` | `` |  |
| 6 | `name` | `string` | `optional` | `` |  |
| 7 | `base_name` | `string` | `optional` | `` |  |
| 8 | `base_detail` | `int32` | `optional` | `` |  |
| 9 | `base_time` | `int32` | `optional` | `` |  |
| 10 | `base_hash` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessageRequestDiagnostic</code> — fields: 1; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `diagnostics` | `.CUserMessageRequestDiagnostic.Diagnostic` | `repeated` | `` |  |

</details>

<details>
<summary><code>CUserMessageRequestDiagnostic.Diagnostic</code> — fields: 13; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMessageRequestDiagnostic`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `index` | `int32` | `optional` | `` |  |
| 2 | `offset` | `int64` | `optional` | `` |  |
| 3 | `param` | `int32` | `optional` | `` |  |
| 4 | `length` | `int32` | `optional` | `` |  |
| 5 | `type` | `int32` | `optional` | `` |  |
| 6 | `base` | `int64` | `optional` | `` |  |
| 7 | `range` | `int64` | `optional` | `` |  |
| 8 | `extent` | `int64` | `optional` | `` |  |
| 9 | `detail` | `int64` | `optional` | `` |  |
| 10 | `name` | `string` | `optional` | `` |  |
| 11 | `alias` | `string` | `optional` | `` |  |
| 12 | `vardetail` | `bytes` | `optional` | `` |  |
| 13 | `context` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessage_Diagnostic_Response</code> — fields: 6; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `diagnostics` | `.CUserMessage_Diagnostic_Response.Diagnostic` | `repeated` | `` |  |
| 2 | `build_version` | `int32` | `optional` | `` |  |
| 3 | `instance` | `int32` | `optional` | `` |  |
| 4 | `start_time` | `int64` | `optional` | `` |  |
| 5 | `osversion` | `int32` | `optional` | `` |  |
| 6 | `platform` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessage_Diagnostic_Response.Diagnostic</code> — fields: 15; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMessage_Diagnostic_Response`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `index` | `int32` | `optional` | `` |  |
| 2 | `offset` | `int64` | `optional` | `` |  |
| 3 | `param` | `int32` | `optional` | `` |  |
| 4 | `length` | `int32` | `optional` | `` |  |
| 5 | `detail` | `bytes` | `optional` | `` |  |
| 6 | `base` | `int64` | `optional` | `` |  |
| 7 | `range` | `int64` | `optional` | `` |  |
| 8 | `type` | `int32` | `optional` | `` |  |
| 10 | `name` | `string` | `optional` | `` |  |
| 11 | `alias` | `string` | `optional` | `` |  |
| 12 | `backup` | `bytes` | `optional` | `` |  |
| 13 | `context` | `int32` | `optional` | `` |  |
| 14 | `control` | `int64` | `optional` | `` |  |
| 15 | `augment` | `int64` | `optional` | `` |  |
| 16 | `placebo` | `int64` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessage_ExtraUserData</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `item` | `int32` | `optional` | `` |  |
| 2 | `value1` | `int64` | `optional` | `` |  |
| 3 | `value2` | `int64` | `optional` | `` |  |
| 4 | `detail1` | `bytes` | `repeated` | `` |  |
| 5 | `detail2` | `bytes` | `repeated` | `` |  |

</details>

<details>
<summary><code>CUserMessage_NotifyResponseFound</code> — fields: 12; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ent_index` | `int32` | `optional` | `` | default = -1 |
| 2 | `rule_name` | `string` | `optional` | `` |  |
| 3 | `response_value` | `string` | `optional` | `` |  |
| 4 | `response_concept` | `string` | `optional` | `` |  |
| 5 | `criteria` | `.CUserMessage_NotifyResponseFound.Criteria` | `repeated` | `` |  |
| 6 | `int_criteria_names` | `uint32` | `repeated` | `` | packed = true |
| 7 | `int_criteria_values` | `int32` | `repeated` | `` | packed = true |
| 8 | `float_criteria_names` | `uint32` | `repeated` | `` | packed = true |
| 9 | `float_criteria_values` | `float` | `repeated` | `` |  |
| 10 | `symbol_criteria_names` | `uint32` | `repeated` | `` | packed = true |
| 11 | `symbol_criteria_values` | `uint32` | `repeated` | `` | packed = true |
| 12 | `speak_result` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessage_NotifyResponseFound.Criteria</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUserMessage_NotifyResponseFound`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `name_symbol` | `uint32` | `optional` | `` |  |
| 2 | `value` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CUserMessage_PlayResponseConditional</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `ent_index` | `int32` | `optional` | `` | default = -1 |
| 2 | `player_slots` | `int32` | `repeated` | `` |  |
| 3 | `response` | `string` | `optional` | `` |  |
| 4 | `ent_origin` | `.CMsgVector` | `optional` | `` |  |
| 5 | `pre_delay` | `float` | `optional` | `` |  |
| 6 | `mix_priority` | `int32` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>EBaseUserMessages</code> — values: 51</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `UM_AchievementEvent` | 101 |
| `UM_CloseCaption` | 102 |
| `UM_CloseCaptionDirect` | 103 |
| `UM_CurrentTimescale` | 104 |
| `UM_DesiredTimescale` | 105 |
| `UM_Fade` | 106 |
| `UM_GameTitle` | 107 |
| `UM_HudMsg` | 110 |
| `UM_HudText` | 111 |
| `UM_ColoredText` | 113 |
| `UM_RequestState` | 114 |
| `UM_ResetHUD` | 115 |
| `UM_Rumble` | 116 |
| `UM_SayText` | 117 |
| `UM_SayText2` | 118 |
| `UM_SayTextChannel` | 119 |
| `UM_Shake` | 120 |
| `UM_ShakeDir` | 121 |
| `UM_WaterShake` | 122 |
| `UM_TextMsg` | 124 |
| `UM_ScreenTilt` | 125 |
| `UM_VoiceMask` | 128 |
| `UM_SendAudio` | 130 |
| `UM_ItemPickup` | 131 |
| `UM_AmmoDenied` | 132 |
| `UM_ShowMenu` | 134 |
| `UM_CreditsMsg` | 135 |
| `UM_CloseCaptionPlaceholder` | 142 |
| `UM_CameraTransition` | 143 |
| `UM_AudioParameter` | 144 |
| `UM_ParticleManager` | 145 |
| `UM_HudError` | 146 |
| `UM_CustomGameEvent` | 148 |
| `UM_AnimGraphUpdate` | 149 |
| `UM_HapticsManagerPulse` | 150 |
| `UM_HapticsManagerEffect` | 151 |
| `UM_UpdateCssClasses` | 153 |
| `UM_ServerFrameTime` | 154 |
| `UM_LagCompensationError` | 155 |
| `UM_RequestDllStatus` | 156 |
| `UM_RequestUtilAction` | 157 |
| `UM_UtilActionResponse` | 158 |
| `UM_DllStatusResponse` | 159 |
| `UM_RequestInventory` | 160 |
| `UM_InventoryResponse` | 161 |
| `UM_RequestDiagnostic` | 162 |
| `UM_DiagnosticResponse` | 163 |
| `UM_ExtraUserData` | 164 |
| `UM_NotifyResponseFound` | 165 |
| `UM_PlayResponseConditional` | 166 |
| `UM_MAX_BASE` | 200 |

</details>

<details>
<summary><code>EBaseEntityMessages</code> — values: 6</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `EM_PlayJingle` | 136 |
| `EM_ScreenOverlay` | 137 |
| `EM_RemoveAllDecals` | 138 |
| `EM_PropagateForce` | 139 |
| `EM_DoSpark` | 140 |
| `EM_FixAngle` | 141 |

</details>

<details>
<summary><code>eRollType</code> — values: 5</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `ROLL_NONE` | -1 |
| `ROLL_STATS` | 0 |
| `ROLL_CREDITS` | 1 |
| `ROLL_LATE_JOIN_LOGO` | 2 |
| `ROLL_OUTTRO` | 3 |

</details>

<details>
<summary><code>PARTICLE_MESSAGE</code> — values: 40</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `GAME_PARTICLE_MANAGER_EVENT_CREATE` | 0 |
| `GAME_PARTICLE_MANAGER_EVENT_UPDATE` | 1 |
| `GAME_PARTICLE_MANAGER_EVENT_UPDATE_FORWARD` | 2 |
| `GAME_PARTICLE_MANAGER_EVENT_UPDATE_ORIENTATION` | 3 |
| `GAME_PARTICLE_MANAGER_EVENT_UPDATE_FALLBACK` | 4 |
| `GAME_PARTICLE_MANAGER_EVENT_UPDATE_ENT` | 5 |
| `GAME_PARTICLE_MANAGER_EVENT_UPDATE_OFFSET` | 6 |
| `GAME_PARTICLE_MANAGER_EVENT_DESTROY` | 7 |
| `GAME_PARTICLE_MANAGER_EVENT_DESTROY_INVOLVING` | 8 |
| `GAME_PARTICLE_MANAGER_EVENT_RELEASE` | 9 |
| `GAME_PARTICLE_MANAGER_EVENT_LATENCY` | 10 |
| `GAME_PARTICLE_MANAGER_EVENT_SHOULD_DRAW` | 11 |
| `GAME_PARTICLE_MANAGER_EVENT_FROZEN` | 12 |
| `GAME_PARTICLE_MANAGER_EVENT_CHANGE_CONTROL_POINT_ATTACHMENT` | 13 |
| `GAME_PARTICLE_MANAGER_EVENT_UPDATE_ENTITY_POSITION` | 14 |
| `GAME_PARTICLE_MANAGER_EVENT_SET_FOW_PROPERTIES` | 15 |
| `GAME_PARTICLE_MANAGER_EVENT_SET_TEXT` | 16 |
| `GAME_PARTICLE_MANAGER_EVENT_SET_SHOULD_CHECK_FOW` | 17 |
| `GAME_PARTICLE_MANAGER_EVENT_SET_CONTROL_POINT_MODEL` | 18 |
| `GAME_PARTICLE_MANAGER_EVENT_SET_CONTROL_POINT_SNAPSHOT` | 19 |
| `GAME_PARTICLE_MANAGER_EVENT_SET_TEXTURE_ATTRIBUTE` | 20 |
| `GAME_PARTICLE_MANAGER_EVENT_SET_SCENE_OBJECT_GENERIC_FLAG` | 21 |
| `GAME_PARTICLE_MANAGER_EVENT_SET_SCENE_OBJECT_TINT_AND_DESAT` | 22 |
| `GAME_PARTICLE_MANAGER_EVENT_DESTROY_NAMED` | 23 |
| `GAME_PARTICLE_MANAGER_EVENT_SKIP_TO_TIME` | 24 |
| `GAME_PARTICLE_MANAGER_EVENT_CAN_FREEZE` | 25 |
| `GAME_PARTICLE_MANAGER_EVENT_SET_NAMED_VALUE_CONTEXT` | 26 |
| `GAME_PARTICLE_MANAGER_EVENT_UPDATE_TRANSFORM` | 27 |
| `GAME_PARTICLE_MANAGER_EVENT_FREEZE_TRANSITION_OVERRIDE` | 28 |
| `GAME_PARTICLE_MANAGER_EVENT_FREEZE_INVOLVING` | 29 |
| `GAME_PARTICLE_MANAGER_EVENT_ADD_MODELLIST_OVERRIDE_ELEMENT` | 30 |
| `GAME_PARTICLE_MANAGER_EVENT_CLEAR_MODELLIST_OVERRIDE` | 31 |
| `GAME_PARTICLE_MANAGER_EVENT_CREATE_PHYSICS_SIM` | 32 |
| `GAME_PARTICLE_MANAGER_EVENT_DESTROY_PHYSICS_SIM` | 33 |
| `GAME_PARTICLE_MANAGER_EVENT_SET_VDATA` | 34 |
| `GAME_PARTICLE_MANAGER_EVENT_SET_MATERIAL_OVERRIDE` | 35 |
| `GAME_PARTICLE_MANAGER_EVENT_ADD_FAN` | 36 |
| `GAME_PARTICLE_MANAGER_EVENT_UPDATE_FAN` | 37 |
| `GAME_PARTICLE_MANAGER_EVENT_SET_CLUSTER_GROWTH` | 38 |
| `GAME_PARTICLE_MANAGER_EVENT_REMOVE_FAN` | 39 |

</details>

<details>
<summary><code>EHapticPulseType</code> — values: 3</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `VR_HAND_HAPTIC_PULSE_LIGHT` | 0 |
| `VR_HAND_HAPTIC_PULSE_MEDIUM` | 1 |
| `VR_HAND_HAPTIC_PULSE_STRONG` | 2 |

</details>
