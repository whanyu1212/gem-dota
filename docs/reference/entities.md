# Entities

Manages packet entity lifecycle (create/update/delete) and typed access to live networked field state.

See also: [Entity State](../guides/02_entity_state.md), [How Proto Parsing Works](../cookbook/proto-parsing-pipeline.md)


---


---

## Generated API

## `gem.state.entities.EntityOp`

### `EntityOp`

```python
class EntityOp(enum.IntFlag)
```

Bitmask indicating what happened to an entity in a packet.

Source: [src/gem/state/entities.py:49](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L49)

#### Methods

##### `has`

Signature: `def EntityOp.has(self, other: EntityOp) -> bool`

Return True if this op overlaps any bit in *other*.

Source: [src/gem/state/entities.py:64](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L64)

## `gem.state.entities.Entity`

### `Entity`

```python
class Entity
```

A live game entity with decoded field state.

Source: [src/gem/state/entities.py:103](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L103)

#### Methods

##### `get`

Signature: `def Entity.get(self, name: str) -> Any`

Return the current value of *name*, or None if absent.

Source: [src/gem/state/entities.py:142](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L142)

##### `exists`

Signature: `def Entity.exists(self, name: str) -> bool`

Return True if *name* has a value in the entity state.

Source: [src/gem/state/entities.py:231](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L231)

##### `get_int32`

Signature: `def Entity.get_int32(self, name: str) -> int | None`

Return the value as int32, or None if absent/wrong type.

Source: [src/gem/state/entities.py:239](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L239)

##### `get_uint32`

Signature: `def Entity.get_uint32(self, name: str) -> int | None`

Return the value as uint32 (low 32 bits), or None if absent.

Source: [src/gem/state/entities.py:251](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L251)

##### `get_uint64`

Signature: `def Entity.get_uint64(self, name: str) -> int | None`

Return the value as uint64, or None if absent.

Source: [src/gem/state/entities.py:265](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L265)

##### `get_float32`

Signature: `def Entity.get_float32(self, name: str) -> float | None`

Return the value as float32, or None if absent.

Source: [src/gem/state/entities.py:277](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L277)

##### `get_string`

Signature: `def Entity.get_string(self, name: str) -> str | None`

Return the value as str, or None if absent.

Source: [src/gem/state/entities.py:289](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L289)

##### `get_bool`

Signature: `def Entity.get_bool(self, name: str) -> bool | None`

Return the value as bool, or None if absent.

Source: [src/gem/state/entities.py:301](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L301)

##### `to_map`

Signature: `def Entity.to_map(self) -> dict[str, Any]`

Return a snapshot of the flat _state dict.

Source: [src/gem/state/entities.py:313](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L313)

##### `get_class_name`

Signature: `def Entity.get_class_name(self) -> str`

Return the entity class name.

Source: [src/gem/state/entities.py:321](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L321)

##### `get_class_id`

Signature: `def Entity.get_class_id(self) -> int`

Return the entity class ID.

Source: [src/gem/state/entities.py:325](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L325)

##### `get_index`

Signature: `def Entity.get_index(self) -> int`

Return the entity slot index.

Source: [src/gem/state/entities.py:329](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L329)

##### `get_serial`

Signature: `def Entity.get_serial(self) -> int`

Return the entity serial number.

Source: [src/gem/state/entities.py:333](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L333)

## `gem.state.entities.EntityManager`

### `EntityManager`

```python
class EntityManager
```

Manages entity lifecycle across a replay stream.

Source: [src/gem/state/entities.py:570](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L570)

#### Methods

##### `on_entity`

Signature: `def EntityManager.on_entity(self, handler: EntityHandler) -> None`

Register an entity event handler.

Source: [src/gem/state/entities.py:601](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L601)

##### `on_server_info`

Signature: `def EntityManager.on_server_info(self, msg: object) -> None`

Extract classIdSize and game build from CSVCMsg_ServerInfo.

Source: [src/gem/state/entities.py:641](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L641)

##### `on_class_info`

Signature: `def EntityManager.on_class_info(self, msg: object) -> None`

Build class maps from CDemoClassInfo.

Source: [src/gem/state/entities.py:660](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L660)

##### `on_baseline_updated`

Signature: `def EntityManager.on_baseline_updated(self) -> None`

Call after instancebaseline string table is created or updated.

Source: [src/gem/state/entities.py:678](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L678)

##### `on_packet_entities`

Signature: `def EntityManager.on_packet_entities(self, msg: object) -> list[tuple[Entity, EntityOp]]`

Decode a CSVCMsg_PacketEntities message.

Source: [src/gem/state/entities.py:682](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L682)

##### `find`

Signature: `def EntityManager.find(self, index: int) -> Entity | None`

Return the entity at the given slot index, or None.

Source: [src/gem/state/entities.py:809](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L809)

##### `find_by_handle`

Signature: `def EntityManager.find_by_handle(self, handle: int) -> Entity | None`

Return the entity for a Source 2 entity handle, or None.

Source: [src/gem/state/entities.py:819](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L819)

##### `filter`

Signature: `def EntityManager.filter(self, predicate: Any) -> list[Entity]`

Return all entities matching a predicate.

Source: [src/gem/state/entities.py:832](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L832)

##### `find_by_class_name`

Signature: `def EntityManager.find_by_class_name(self, class_name: str) -> Entity | None`

Return the first active entity whose class name matches, or None.

Source: [src/gem/state/entities.py:843](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L843)

##### `find_by_npc_name`

Signature: `def EntityManager.find_by_npc_name(self, npc_name: str) -> Entity | None`

Return the first active entity whose NPC name matches, or None.

Source: [src/gem/state/entities.py:854](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L854)

##### `all_active`

Signature: `def EntityManager.all_active(self) -> list[Entity]`

Return all currently active entities.

Source: [src/gem/state/entities.py:890](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L890)
