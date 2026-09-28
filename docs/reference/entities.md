# Entities

Manages packet entity lifecycle (create/update/delete) and typed access to live networked field state.

See also: [How Entities Are Decoded, Part 5: Entity Lifecycle](../deep-dives/entity-lifecycle.md),
[Entity State](../guides/02_entity_state.md), and
[How Proto Parsing Works](../cookbook/proto-parsing-pipeline.md).

---

## Generated API

## `gem.state.entities.EntityOp`

### `EntityOp`

```python
class EntityOp(enum.IntFlag)
```

Bitmask indicating what happened to an entity in a packet.

Source: [src/gem/state/entities.py:77](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L77)

#### Methods

##### `has`

Signature: `def EntityOp.has(self, other: EntityOp) -> bool`

Return True if this op overlaps any bit in *other*.

Source: [src/gem/state/entities.py:92](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L92)

## `gem.state.entities.Entity`

### `Entity`

```python
class Entity
```

A live game entity with decoded field state.

Source: [src/gem/state/entities.py:131](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L131)

#### Methods

##### `get`

Signature: `def Entity.get(self, name: str) -> Any`

Return the current value of *name*, or None if absent.

Source: [src/gem/state/entities.py:166](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L166)

##### `exists`

Signature: `def Entity.exists(self, name: str) -> bool`

Return True if *name* has a value in the entity state.

Source: [src/gem/state/entities.py:234](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L234)

##### `get_int32`

Signature: `def Entity.get_int32(self, name: str) -> int | None`

Return the value as int32, or None if absent/wrong type.

Source: [src/gem/state/entities.py:242](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L242)

##### `get_uint32`

Signature: `def Entity.get_uint32(self, name: str) -> int | None`

Return the value as uint32 (low 32 bits), or None if absent.

Source: [src/gem/state/entities.py:254](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L254)

##### `get_uint64`

Signature: `def Entity.get_uint64(self, name: str) -> int | None`

Return the value as uint64, or None if absent.

Source: [src/gem/state/entities.py:268](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L268)

##### `get_float32`

Signature: `def Entity.get_float32(self, name: str) -> float | None`

Return the value as float32, or None if absent.

Source: [src/gem/state/entities.py:280](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L280)

##### `get_string`

Signature: `def Entity.get_string(self, name: str) -> str | None`

Return the value as str, or None if absent.

Source: [src/gem/state/entities.py:292](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L292)

##### `get_bool`

Signature: `def Entity.get_bool(self, name: str) -> bool | None`

Return the value as bool, or None if absent.

Source: [src/gem/state/entities.py:304](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L304)

##### `to_map`

Signature: `def Entity.to_map(self) -> dict[str, Any]`

Return every stored field value by name.

Source: [src/gem/state/entities.py:316](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L316)

##### `get_class_name`

Signature: `def Entity.get_class_name(self) -> str`

Return the entity class name.

Source: [src/gem/state/entities.py:335](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L335)

##### `get_class_id`

Signature: `def Entity.get_class_id(self) -> int`

Return the entity class ID.

Source: [src/gem/state/entities.py:339](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L339)

##### `get_index`

Signature: `def Entity.get_index(self) -> int`

Return the entity slot index.

Source: [src/gem/state/entities.py:343](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L343)

##### `get_serial`

Signature: `def Entity.get_serial(self) -> int`

Return the entity serial number.

Source: [src/gem/state/entities.py:347](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L347)

## `gem.state.entities.EntityManager`

### `EntityManager`

```python
class EntityManager
```

Manages entity lifecycle across a replay stream.

Source: [src/gem/state/entities.py:616](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L616)

#### Methods

##### `on_entity`

Signature: `def EntityManager.on_entity(self, handler: EntityHandler) -> None`

Register an entity event handler.

Source: [src/gem/state/entities.py:647](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L647)

##### `on_server_info`

Signature: `def EntityManager.on_server_info(self, msg: object) -> None`

Extract classIdSize and game build from CSVCMsg_ServerInfo.

Source: [src/gem/state/entities.py:687](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L687)

##### `on_class_info`

Signature: `def EntityManager.on_class_info(self, msg: object) -> None`

Build class maps from CDemoClassInfo.

Source: [src/gem/state/entities.py:705](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L705)

##### `on_baseline_updated`

Signature: `def EntityManager.on_baseline_updated(self) -> None`

Call after instancebaseline string table is created or updated.

Source: [src/gem/state/entities.py:723](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L723)

##### `on_packet_entities`

Signature: `def EntityManager.on_packet_entities(self, msg: object) -> list[tuple[Entity, EntityOp]]`

Decode a CSVCMsg_PacketEntities message.

Source: [src/gem/state/entities.py:727](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L727)

##### `find`

Signature: `def EntityManager.find(self, index: int) -> Entity | None`

Return the entity at the given slot index, or None.

Source: [src/gem/state/entities.py:854](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L854)

##### `find_by_handle`

Signature: `def EntityManager.find_by_handle(self, handle: int) -> Entity | None`

Return the entity for a Source 2 entity handle, or None.

Source: [src/gem/state/entities.py:864](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L864)

##### `filter`

Signature: `def EntityManager.filter(self, predicate: Any) -> list[Entity]`

Return all entities matching a predicate.

Source: [src/gem/state/entities.py:877](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L877)

##### `find_by_class_name`

Signature: `def EntityManager.find_by_class_name(self, class_name: str) -> Entity | None`

Return the first active entity whose class name matches, or None.

Source: [src/gem/state/entities.py:888](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L888)

##### `find_by_npc_name`

Signature: `def EntityManager.find_by_npc_name(self, npc_name: str) -> Entity | None`

Return the first active entity whose NPC name matches, or None.

Source: [src/gem/state/entities.py:899](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L899)

##### `all_active`

Signature: `def EntityManager.all_active(self) -> list[Entity]`

Return all currently active entities.

Source: [src/gem/state/entities.py:939](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L939)
