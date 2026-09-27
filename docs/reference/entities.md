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

Source: [src/gem/state/entities.py:73](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L73)

#### Methods

##### `has`

Signature: `def EntityOp.has(self, other: EntityOp) -> bool`

Return True if this op overlaps any bit in *other*.

Source: [src/gem/state/entities.py:88](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L88)

## `gem.state.entities.Entity`

### `Entity`

```python
class Entity
```

A live game entity with decoded field state.

Source: [src/gem/state/entities.py:127](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L127)

#### Methods

##### `get`

Signature: `def Entity.get(self, name: str) -> Any`

Return the current value of *name*, or None if absent.

Source: [src/gem/state/entities.py:162](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L162)

##### `exists`

Signature: `def Entity.exists(self, name: str) -> bool`

Return True if *name* has a value in the entity state.

Source: [src/gem/state/entities.py:230](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L230)

##### `get_int32`

Signature: `def Entity.get_int32(self, name: str) -> int | None`

Return the value as int32, or None if absent/wrong type.

Source: [src/gem/state/entities.py:238](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L238)

##### `get_uint32`

Signature: `def Entity.get_uint32(self, name: str) -> int | None`

Return the value as uint32 (low 32 bits), or None if absent.

Source: [src/gem/state/entities.py:250](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L250)

##### `get_uint64`

Signature: `def Entity.get_uint64(self, name: str) -> int | None`

Return the value as uint64, or None if absent.

Source: [src/gem/state/entities.py:264](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L264)

##### `get_float32`

Signature: `def Entity.get_float32(self, name: str) -> float | None`

Return the value as float32, or None if absent.

Source: [src/gem/state/entities.py:276](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L276)

##### `get_string`

Signature: `def Entity.get_string(self, name: str) -> str | None`

Return the value as str, or None if absent.

Source: [src/gem/state/entities.py:288](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L288)

##### `get_bool`

Signature: `def Entity.get_bool(self, name: str) -> bool | None`

Return the value as bool, or None if absent.

Source: [src/gem/state/entities.py:300](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L300)

##### `to_map`

Signature: `def Entity.to_map(self) -> dict[str, Any]`

Return every stored field value by name.

Source: [src/gem/state/entities.py:312](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L312)

##### `get_class_name`

Signature: `def Entity.get_class_name(self) -> str`

Return the entity class name.

Source: [src/gem/state/entities.py:331](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L331)

##### `get_class_id`

Signature: `def Entity.get_class_id(self) -> int`

Return the entity class ID.

Source: [src/gem/state/entities.py:335](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L335)

##### `get_index`

Signature: `def Entity.get_index(self) -> int`

Return the entity slot index.

Source: [src/gem/state/entities.py:339](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L339)

##### `get_serial`

Signature: `def Entity.get_serial(self) -> int`

Return the entity serial number.

Source: [src/gem/state/entities.py:343](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L343)

## `gem.state.entities.EntityManager`

### `EntityManager`

```python
class EntityManager
```

Manages entity lifecycle across a replay stream.

Source: [src/gem/state/entities.py:612](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L612)

#### Methods

##### `on_entity`

Signature: `def EntityManager.on_entity(self, handler: EntityHandler) -> None`

Register an entity event handler.

Source: [src/gem/state/entities.py:643](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L643)

##### `on_server_info`

Signature: `def EntityManager.on_server_info(self, msg: object) -> None`

Extract classIdSize and game build from CSVCMsg_ServerInfo.

Source: [src/gem/state/entities.py:683](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L683)

##### `on_class_info`

Signature: `def EntityManager.on_class_info(self, msg: object) -> None`

Build class maps from CDemoClassInfo.

Source: [src/gem/state/entities.py:701](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L701)

##### `on_baseline_updated`

Signature: `def EntityManager.on_baseline_updated(self) -> None`

Call after instancebaseline string table is created or updated.

Source: [src/gem/state/entities.py:719](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L719)

##### `on_packet_entities`

Signature: `def EntityManager.on_packet_entities(self, msg: object) -> list[tuple[Entity, EntityOp]]`

Decode a CSVCMsg_PacketEntities message.

Source: [src/gem/state/entities.py:723](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L723)

##### `find`

Signature: `def EntityManager.find(self, index: int) -> Entity | None`

Return the entity at the given slot index, or None.

Source: [src/gem/state/entities.py:850](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L850)

##### `find_by_handle`

Signature: `def EntityManager.find_by_handle(self, handle: int) -> Entity | None`

Return the entity for a Source 2 entity handle, or None.

Source: [src/gem/state/entities.py:860](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L860)

##### `filter`

Signature: `def EntityManager.filter(self, predicate: Any) -> list[Entity]`

Return all entities matching a predicate.

Source: [src/gem/state/entities.py:873](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L873)

##### `find_by_class_name`

Signature: `def EntityManager.find_by_class_name(self, class_name: str) -> Entity | None`

Return the first active entity whose class name matches, or None.

Source: [src/gem/state/entities.py:884](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L884)

##### `find_by_npc_name`

Signature: `def EntityManager.find_by_npc_name(self, npc_name: str) -> Entity | None`

Return the first active entity whose NPC name matches, or None.

Source: [src/gem/state/entities.py:895](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L895)

##### `all_active`

Signature: `def EntityManager.all_active(self) -> list[Entity]`

Return all currently active entities.

Source: [src/gem/state/entities.py:931](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/state/entities.py#L931)
