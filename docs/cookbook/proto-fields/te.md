# te.proto

- Module: `te_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **1**
- Messages: **25** (top-level: 25)
- Enums: **1** (top-level: 1)

## Imports

- `networkbasetypes.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgTEArmorRicochet</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `pos` | `.CMsgVector` | `optional` | `` |  |
| 2 | `dir` | `.CMsgVector` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTEBaseBeam</code> — fields: 12; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `modelindex` | `fixed64` | `optional` | `` |  |
| 2 | `haloindex` | `fixed64` | `optional` | `` |  |
| 3 | `startframe` | `uint32` | `optional` | `` |  |
| 4 | `framerate` | `uint32` | `optional` | `` |  |
| 5 | `life` | `float` | `optional` | `` |  |
| 6 | `width` | `float` | `optional` | `` |  |
| 7 | `endwidth` | `float` | `optional` | `` |  |
| 8 | `fadelength` | `uint32` | `optional` | `` |  |
| 9 | `amplitude` | `float` | `optional` | `` |  |
| 10 | `color` | `fixed32` | `optional` | `` |  |
| 11 | `speed` | `uint32` | `optional` | `` |  |
| 12 | `flags` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTEBeamEntPoint</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `base` | `.CMsgTEBaseBeam` | `optional` | `` |  |
| 2 | `startentity` | `uint32` | `optional` | `` |  |
| 3 | `endentity` | `uint32` | `optional` | `` |  |
| 4 | `start` | `.CMsgVector` | `optional` | `` |  |
| 5 | `end` | `.CMsgVector` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTEBeamEnts</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `base` | `.CMsgTEBaseBeam` | `optional` | `` |  |
| 2 | `startentity` | `uint32` | `optional` | `` |  |
| 3 | `endentity` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTEBeamPoints</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `base` | `.CMsgTEBaseBeam` | `optional` | `` |  |
| 2 | `start` | `.CMsgVector` | `optional` | `` |  |
| 3 | `end` | `.CMsgVector` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTEBeamRing</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `base` | `.CMsgTEBaseBeam` | `optional` | `` |  |
| 2 | `startentity` | `uint32` | `optional` | `` |  |
| 3 | `endentity` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTEBubbles</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `mins` | `.CMsgVector` | `optional` | `` |  |
| 2 | `maxs` | `.CMsgVector` | `optional` | `` |  |
| 3 | `height` | `float` | `optional` | `` |  |
| 4 | `count` | `uint32` | `optional` | `` |  |
| 5 | `speed` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTEBubbleTrail</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `mins` | `.CMsgVector` | `optional` | `` |  |
| 2 | `maxs` | `.CMsgVector` | `optional` | `` |  |
| 3 | `waterz` | `float` | `optional` | `` |  |
| 4 | `count` | `uint32` | `optional` | `` |  |
| 5 | `speed` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTEDecal</code> — fields: 5; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `origin` | `.CMsgVector` | `optional` | `` |  |
| 2 | `start` | `.CMsgVector` | `optional` | `` |  |
| 3 | `entity` | `int32` | `optional` | `` | default = -1 |
| 4 | `hitbox` | `uint32` | `optional` | `` |  |
| 5 | `index` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgEffectData</code> — fields: 19; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `origin` | `.CMsgVector` | `optional` | `` |  |
| 2 | `start` | `.CMsgVector` | `optional` | `` |  |
| 3 | `normal` | `.CMsgVector` | `optional` | `` |  |
| 4 | `angles` | `.CMsgQAngle` | `optional` | `` |  |
| 5 | `entity` | `fixed32` | `optional` | `` | default = 16777215 |
| 6 | `otherentity` | `fixed32` | `optional` | `` | default = 16777215 |
| 7 | `scale` | `float` | `optional` | `` |  |
| 8 | `magnitude` | `float` | `optional` | `` |  |
| 9 | `radius` | `float` | `optional` | `` |  |
| 10 | `surfaceprop` | `fixed32` | `optional` | `` |  |
| 11 | `effectindex` | `fixed64` | `optional` | `` |  |
| 12 | `damagetype` | `uint32` | `optional` | `` |  |
| 13 | `material` | `uint32` | `optional` | `` |  |
| 14 | `hitbox` | `uint32` | `optional` | `` |  |
| 15 | `color` | `uint32` | `optional` | `` |  |
| 16 | `flags` | `uint32` | `optional` | `` |  |
| 17 | `attachmentindex` | `int32` | `optional` | `` |  |
| 18 | `effectname` | `uint32` | `optional` | `` |  |
| 19 | `attachmentname` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTEEffectDispatch</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `effectdata` | `.CMsgEffectData` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTEEnergySplash</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `pos` | `.CMsgVector` | `optional` | `` |  |
| 2 | `dir` | `.CMsgVector` | `optional` | `` |  |
| 3 | `explosive` | `bool` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTEFizz</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `entity` | `int32` | `optional` | `` | default = -1 |
| 2 | `density` | `uint32` | `optional` | `` |  |
| 3 | `current` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTEShatterSurface</code> — fields: 10; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `origin` | `.CMsgVector` | `optional` | `` |  |
| 2 | `angles` | `.CMsgQAngle` | `optional` | `` |  |
| 3 | `force` | `.CMsgVector` | `optional` | `` |  |
| 4 | `forcepos` | `.CMsgVector` | `optional` | `` |  |
| 5 | `width` | `float` | `optional` | `` |  |
| 6 | `height` | `float` | `optional` | `` |  |
| 7 | `shardsize` | `float` | `optional` | `` |  |
| 8 | `surfacetype` | `uint32` | `optional` | `` |  |
| 9 | `frontcolor` | `fixed32` | `optional` | `` |  |
| 10 | `backcolor` | `fixed32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTEGlowSprite</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `origin` | `.CMsgVector` | `optional` | `` |  |
| 2 | `scale` | `float` | `optional` | `` |  |
| 3 | `life` | `float` | `optional` | `` |  |
| 4 | `brightness` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTEImpact</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `origin` | `.CMsgVector` | `optional` | `` |  |
| 2 | `normal` | `.CMsgVector` | `optional` | `` |  |
| 3 | `type` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTEMuzzleFlash</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `origin` | `.CMsgVector` | `optional` | `` |  |
| 2 | `angles` | `.CMsgQAngle` | `optional` | `` |  |
| 3 | `scale` | `float` | `optional` | `` |  |
| 4 | `type` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTEBloodStream</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `origin` | `.CMsgVector` | `optional` | `` |  |
| 2 | `direction` | `.CMsgVector` | `optional` | `` |  |
| 3 | `color` | `fixed32` | `optional` | `` |  |
| 4 | `amount` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTEExplosion</code> — fields: 11; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `origin` | `.CMsgVector` | `optional` | `` |  |
| 3 | `flags` | `uint32` | `optional` | `` |  |
| 4 | `normal` | `.CMsgVector` | `optional` | `` |  |
| 6 | `radius` | `uint32` | `optional` | `` |  |
| 7 | `magnitude` | `uint32` | `optional` | `` |  |
| 9 | `affect_ragdolls` | `bool` | `optional` | `` |  |
| 10 | `sound_name` | `string` | `optional` | `` |  |
| 11 | `explosion_type` | `uint32` | `optional` | `` |  |
| 12 | `create_debris` | `bool` | `optional` | `` |  |
| 13 | `debris_origin` | `.CMsgVector` | `optional` | `` |  |
| 14 | `debris_surfaceprop` | `fixed32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTEDust</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `origin` | `.CMsgVector` | `optional` | `` |  |
| 2 | `size` | `float` | `optional` | `` |  |
| 3 | `speed` | `float` | `optional` | `` |  |
| 4 | `direction` | `.CMsgVector` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTELargeFunnel</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `origin` | `.CMsgVector` | `optional` | `` |  |
| 2 | `reversed` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTESparks</code> — fields: 4; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `origin` | `.CMsgVector` | `optional` | `` |  |
| 2 | `magnitude` | `uint32` | `optional` | `` |  |
| 3 | `length` | `uint32` | `optional` | `` |  |
| 4 | `direction` | `.CMsgVector` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTEPhysicsProp</code> — fields: 13; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `origin` | `.CMsgVector` | `optional` | `` |  |
| 2 | `velocity` | `.CMsgVector` | `optional` | `` |  |
| 3 | `angles` | `.CMsgQAngle` | `optional` | `` |  |
| 4 | `skin` | `fixed32` | `optional` | `` |  |
| 5 | `flags` | `uint32` | `optional` | `` |  |
| 6 | `effects` | `uint32` | `optional` | `` |  |
| 7 | `color` | `fixed32` | `optional` | `` |  |
| 8 | `modelindex` | `fixed64` | `optional` | `` |  |
| 9 | `unused_breakmodelsnottomake` | `uint32` | `optional` | `` |  |
| 10 | `scale` | `float` | `optional` | `` |  |
| 11 | `dmgpos` | `.CMsgVector` | `optional` | `` |  |
| 12 | `dmgdir` | `.CMsgVector` | `optional` | `` |  |
| 13 | `dmgtype` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTESmoke</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `origin` | `.CMsgVector` | `optional` | `` |  |
| 2 | `scale` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgTEWorldDecal</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `origin` | `.CMsgVector` | `optional` | `` |  |
| 2 | `normal` | `.CMsgVector` | `optional` | `` |  |
| 3 | `index` | `uint32` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>ETEProtobufIds</code> — values: 23</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `TE_EffectDispatchId` | 400 |
| `TE_ArmorRicochetId` | 401 |
| `TE_BeamEntPointId` | 402 |
| `TE_BeamEntsId` | 403 |
| `TE_BeamPointsId` | 404 |
| `TE_BeamRingId` | 405 |
| `TE_BubblesId` | 408 |
| `TE_BubbleTrailId` | 409 |
| `TE_DecalId` | 410 |
| `TE_WorldDecalId` | 411 |
| `TE_EnergySplashId` | 412 |
| `TE_FizzId` | 413 |
| `TE_ShatterSurfaceId` | 414 |
| `TE_GlowSpriteId` | 415 |
| `TE_ImpactId` | 416 |
| `TE_MuzzleFlashId` | 417 |
| `TE_BloodStreamId` | 418 |
| `TE_ExplosionId` | 419 |
| `TE_DustId` | 420 |
| `TE_LargeFunnelId` | 421 |
| `TE_SparksId` | 422 |
| `TE_PhysicsPropId` | 423 |
| `TE_SmokeId` | 426 |

</details>
