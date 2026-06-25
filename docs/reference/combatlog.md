# Combat Log

Normalizes combat-log data from both Source 1 and Source 2 ingestion paths into a unified entry shape.

See also: [Using the Combat Log](../guides/03_combat_log.md), [How Proto Parsing Works](../cookbook/proto-parsing-pipeline.md)

---

## Generated API

## `gem.combat.log.CombatLogProcessor`

### `CombatLogProcessor`

```python
class CombatLogProcessor
```

Parses and dispatches combat log entries.

Source: [src/gem/combat/log.py:262](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/combat/log.py#L262)

#### Methods

##### `on_combat_log_entry`

Signature: `def CombatLogProcessor.on_combat_log_entry(self, handler: CombatLogHandler) -> None`

Register a handler to receive decoded CombatLogEntry objects.

Source: [src/gem/combat/log.py:272](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/combat/log.py#L272)

##### `process_rune_pickup`

Signature: `def CombatLogProcessor.process_rune_pickup(self, player_slot: int, rune_type: int, tick: int = 0) -> None`

Emit a PICKUP_RUNE CombatLogEntry from a CDOTAUserMsg_ChatEvent.

Source: [src/gem/combat/log.py:280](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/combat/log.py#L280)

##### `process_s1_event`

Signature: `def CombatLogProcessor.process_s1_event(self, game_event: Any, name_table: Any, tick: int = 0) -> None`

Parse a ``dota_combatlog`` S1 game event and emit a CombatLogEntry.

Source: [src/gem/combat/log.py:305](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/combat/log.py#L305)

##### `process_s2_bulk`

Signature: `def CombatLogProcessor.process_s2_bulk(self, msg: Any, name_table: Any, tick: int = 0) -> None`

Parse a CDOTAUserMsg_CombatLogBulkData and emit CombatLogEntry per entry.

Source: [src/gem/combat/log.py:371](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/combat/log.py#L371)

##### `process_s2_entry`

Signature: `def CombatLogProcessor.process_s2_entry(self, msg: Any, name_table: Any, tick: int = 0, game_time_s: int | None = None) -> None`

Parse a CMsgDOTACombatLogEntry and emit a CombatLogEntry.

Source: [src/gem/combat/log.py:383](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/combat/log.py#L383)

## `gem.combat.log.CombatLogEntry`

### `CombatLogEntry`

```python
class CombatLogEntry
```

One decoded combat log entry.

Source: [src/gem/combat/log.py:134](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/combat/log.py#L134)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `log_type` | `CombatLogType` | `-` |
| `attacker_name` | `str` | `''` |
| `damage_source_name` | `str` | `''` |
| `target_name` | `str` | `''` |
| `inflictor_name` | `str` | `''` |
| `value` | `int` | `0` |
| `attacker_is_hero` | `bool` | `False` |
| `target_is_hero` | `bool` | `False` |
| `attacker_is_illusion` | `bool` | `False` |
| `target_is_illusion` | `bool` | `False` |
| `ability_level` | `int` | `0` |
| `gold_reason` | `int` | `0` |
| `xp_reason` | `int` | `0` |
| `value_name` | `str` | `''` |
| `damage_type` | `str` | `''` |
| `stun_duration` | `float` | `0.0` |
| `neutral_camp_type` | `int` | `0` |
| `neutral_camp_team` | `int` | `0` |
| `location_x` | `float | None` | `None` |
| `location_y` | `float | None` | `None` |
| `timestamp_s` | `float | None` | `None` |
| `game_time_s` | `int | None` | `None` |
| `will_reincarnate` | `bool` | `False` |
