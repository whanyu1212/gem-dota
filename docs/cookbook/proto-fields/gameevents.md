# gameevents.proto

- Module: `gameevents_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **1**
- Messages: **16** (top-level: 13)
- Enums: **1** (top-level: 1)

## Imports

- `networkbasetypes.proto`

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CMsgVDebugGameSessionIDEvent</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `clientid` | `int32` | `optional` | `` |  |
| 2 | `gamesessionid` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgPlaceDecalEvent</code> — fields: 13; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `position` | `.CMsgVector` | `optional` | `` |  |
| 2 | `normal` | `.CMsgVector` | `optional` | `` |  |
| 3 | `saxis` | `.CMsgVector` | `optional` | `` |  |
| 4 | `boneindex` | `int32` | `optional` | `` |  |
| 5 | `flags` | `uint32` | `optional` | `` |  |
| 6 | `color` | `fixed32` | `optional` | `` |  |
| 7 | `random_seed` | `int32` | `optional` | `` |  |
| 8 | `decal_group_name` | `uint32` | `optional` | `` |  |
| 9 | `size_override` | `float` | `optional` | `` |  |
| 10 | `entityhandle` | `uint32` | `optional` | `` | default = 16777215 |
| 11 | `material_id` | `uint64` | `optional` | `` |  |
| 12 | `sequence_name` | `uint32` | `optional` | `` |  |
| 13 | `triangleindex` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClearWorldDecalsEvent</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `flagstoclear` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClearEntityDecalsEvent</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `flagstoclear` | `uint32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgClearDecalsForEntityEvent</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `flagstoclear` | `uint32` | `optional` | `` |  |
| 2 | `entityhandle` | `uint32` | `optional` | `` | default = 16777215 |

</details>

<details>
<summary><code>CMsgSource1LegacyGameEventList</code> — fields: 1; oneofs: 0; nested messages: 2; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `descriptors` | `.CMsgSource1LegacyGameEventList.descriptor_t` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSource1LegacyGameEventList.key_t</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSource1LegacyGameEventList`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `type` | `int32` | `optional` | `` |  |
| 2 | `name` | `string` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSource1LegacyGameEventList.descriptor_t</code> — fields: 3; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSource1LegacyGameEventList`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `eventid` | `int32` | `optional` | `` |  |
| 2 | `name` | `string` | `optional` | `` |  |
| 3 | `keys` | `.CMsgSource1LegacyGameEventList.key_t` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSource1LegacyListenEvents</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `playerslot` | `int32` | `optional` | `` |  |
| 2 | `eventarraybits` | `uint32` | `repeated` | `` |  |

</details>

<details>
<summary><code>CMsgSource1LegacyGameEvent</code> — fields: 5; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `event_name` | `string` | `optional` | `` |  |
| 2 | `eventid` | `int32` | `optional` | `` |  |
| 3 | `keys` | `.CMsgSource1LegacyGameEvent.key_t` | `repeated` | `` |  |
| 4 | `server_tick` | `int32` | `optional` | `` |  |
| 5 | `passthrough` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSource1LegacyGameEvent.key_t</code> — fields: 8; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CMsgSource1LegacyGameEvent`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `type` | `int32` | `optional` | `` |  |
| 2 | `val_string` | `string` | `optional` | `` |  |
| 3 | `val_float` | `float` | `optional` | `` |  |
| 4 | `val_long` | `int32` | `optional` | `` |  |
| 5 | `val_short` | `int32` | `optional` | `` |  |
| 6 | `val_byte` | `int32` | `optional` | `` |  |
| 7 | `val_bool` | `bool` | `optional` | `` |  |
| 8 | `val_uint64` | `uint64` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSosStartSoundEvent</code> — fields: 6; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `soundevent_guid` | `int32` | `optional` | `` |  |
| 2 | `soundevent_hash` | `fixed32` | `optional` | `` |  |
| 3 | `source_entity_index` | `int32` | `optional` | `` | default = -1 |
| 4 | `seed` | `int32` | `optional` | `` |  |
| 5 | `packed_params` | `bytes` | `optional` | `` |  |
| 6 | `start_time` | `float` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSosStopSoundEvent</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `soundevent_guid` | `int32` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSosStopSoundEventHash</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `soundevent_hash` | `fixed32` | `optional` | `` |  |
| 2 | `source_entity_index` | `int32` | `optional` | `` | default = -1 |

</details>

<details>
<summary><code>CMsgSosSetSoundEventParams</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `soundevent_guid` | `int32` | `optional` | `` |  |
| 5 | `packed_params` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CMsgSosSetLibraryStackFields</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `stack_hash` | `fixed32` | `optional` | `` |  |
| 5 | `packed_fields` | `bytes` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

<details>
<summary><code>EBaseGameEvents</code> — values: 13</summary>

- Parent: *(top-level)*

| Name | Number |
|---|---:|
| `GE_VDebugGameSessionIDEvent` | 200 |
| `GE_PlaceDecalEvent` | 201 |
| `GE_ClearWorldDecalsEvent` | 202 |
| `GE_ClearEntityDecalsEvent` | 203 |
| `GE_ClearDecalsForEntityEvent` | 204 |
| `GE_Source1LegacyGameEventList` | 205 |
| `GE_Source1LegacyListenEvents` | 206 |
| `GE_Source1LegacyGameEvent` | 207 |
| `GE_SosStartSoundEvent` | 208 |
| `GE_SosStopSoundEvent` | 209 |
| `GE_SosSetSoundEventParams` | 210 |
| `GE_SosSetLibraryStackFields` | 211 |
| `GE_SosStopSoundEventHash` | 212 |

</details>
