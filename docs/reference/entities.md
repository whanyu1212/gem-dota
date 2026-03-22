# Entities

Manages packet entity lifecycle (create/update/delete) and typed access to live networked field state.

See also: [The Entity System](../understanding/08_entity_system.md), [Entity State](../guides/02_entity_state.md)


---


---

## Generated API

## `gem.entities.EntityOp`

### `EntityOp`

```python
class EntityOp(enum.IntFlag)
```

Bitmask indicating what happened to an entity in a packet.

Source: [src/gem/entities.py:50](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/entities.py#L50)

#### Methods

##### `has`

Signature: `def EntityOp.has(self, other: EntityOp) -> bool`

Return True if this op includes *other*.

Source: [src/gem/entities.py:65](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/entities.py#L65)

## `gem.entities.Entity`

### `Entity`

```python
class Entity
```

A live game entity with decoded field state.

Source: [src/gem/entities.py:102](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/entities.py#L102)

#### Methods

##### `get`

Signature: `def Entity.get(self, name: str) -> Any`

Return the current value of *name*, or None if absent.

Source: [src/gem/entities.py:143](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/entities.py#L143)

##### `exists`

Signature: `def Entity.exists(self, name: str) -> bool`

Return True if *name* has a value in the entity state.

Source: [src/gem/entities.py:176](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/entities.py#L176)

##### `get_int32`

Signature: `def Entity.get_int32(self, name: str) -> int | None`

Return the value as int32, or None if absent/wrong type.

Source: [src/gem/entities.py:184](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/entities.py#L184)

##### `get_uint32`

Signature: `def Entity.get_uint32(self, name: str) -> int | None`

Return the value as uint32 (low 32 bits), or None if absent.

Source: [src/gem/entities.py:196](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/entities.py#L196)

##### `get_uint64`

Signature: `def Entity.get_uint64(self, name: str) -> int | None`

Return the value as uint64, or None if absent.

Source: [src/gem/entities.py:210](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/entities.py#L210)

##### `get_float32`

Signature: `def Entity.get_float32(self, name: str) -> float | None`

Return the value as float32, or None if absent.

Source: [src/gem/entities.py:222](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/entities.py#L222)

##### `get_string`

Signature: `def Entity.get_string(self, name: str) -> str | None`

Return the value as str, or None if absent.

Source: [src/gem/entities.py:234](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/entities.py#L234)

##### `get_bool`

Signature: `def Entity.get_bool(self, name: str) -> bool | None`

Return the value as bool, or None if absent.

Source: [src/gem/entities.py:246](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/entities.py#L246)

##### `to_map`

Signature: `def Entity.to_map(self) -> dict[str, Any]`

Return a snapshot of the flat _state dict.

Source: [src/gem/entities.py:258](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/entities.py#L258)

##### `get_class_name`

Signature: `def Entity.get_class_name(self) -> str`

Return the entity class name.

Source: [src/gem/entities.py:266](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/entities.py#L266)

##### `get_class_id`

Signature: `def Entity.get_class_id(self) -> int`

Return the entity class ID.

Source: [src/gem/entities.py:270](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/entities.py#L270)

##### `get_index`

Signature: `def Entity.get_index(self) -> int`

Return the entity slot index.

Source: [src/gem/entities.py:274](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/entities.py#L274)

##### `get_serial`

Signature: `def Entity.get_serial(self) -> int`

Return the entity serial number.

Source: [src/gem/entities.py:278](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/entities.py#L278)

## `gem.entities.EntityManager`

### `EntityManager`

```python
class EntityManager
```

Manages entity lifecycle across a replay stream.

Source: [src/gem/entities.py:382](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/entities.py#L382)

#### Methods

##### `on_entity`

Signature: `def EntityManager.on_entity(self, handler: EntityHandler) -> None`

Register an entity event handler.

Source: [src/gem/entities.py:413](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/entities.py#L413)

##### `on_server_info`

Signature: `def EntityManager.on_server_info(self, msg: object) -> None`

Extract classIdSize and game build from CSVCMsg_ServerInfo.

Source: [src/gem/entities.py:425](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/entities.py#L425)

##### `on_class_info`

Signature: `def EntityManager.on_class_info(self, msg: object) -> None`

Build class maps from CDemoClassInfo.

Source: [src/gem/entities.py:444](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/entities.py#L444)

##### `on_baseline_updated`

Signature: `def EntityManager.on_baseline_updated(self) -> None`

Call after instancebaseline string table is created or updated.

Source: [src/gem/entities.py:461](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/entities.py#L461)

##### `on_packet_entities`

Signature: `def EntityManager.on_packet_entities(self, msg: object) -> list[tuple[Entity, EntityOp]]`

Decode a CSVCMsg_PacketEntities message.

Source: [src/gem/entities.py:465](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/entities.py#L465)

##### `find`

Signature: `def EntityManager.find(self, index: int) -> Entity | None`

Return the entity at the given slot index, or None.

Source: [src/gem/entities.py:564](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/entities.py#L564)

##### `find_by_handle`

Signature: `def EntityManager.find_by_handle(self, handle: int) -> Entity | None`

Return the entity for a Source 2 entity handle, or None.

Source: [src/gem/entities.py:574](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/entities.py#L574)

##### `filter`

Signature: `def EntityManager.filter(self, predicate: Any) -> list[Entity]`

Return all entities matching a predicate.

Source: [src/gem/entities.py:587](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/entities.py#L587)

##### `find_by_class_name`

Signature: `def EntityManager.find_by_class_name(self, class_name: str) -> Entity | None`

Return the first active entity whose class name matches, or None.

Source: [src/gem/entities.py:598](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/entities.py#L598)

##### `find_by_npc_name`

Signature: `def EntityManager.find_by_npc_name(self, npc_name: str) -> Entity | None`

Return the first active entity whose NPC name matches, or None.

Source: [src/gem/entities.py:609](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/entities.py#L609)

##### `all_active`

Signature: `def EntityManager.all_active(self) -> list[Entity]`

Return all currently active entities.

Source: [src/gem/entities.py:644](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/entities.py#L644)
