# Combat Log

Normalizes combat-log data from both Source 1 and Source 2 ingestion paths into a unified entry shape.

See also: [The Combat Log](../understanding/09_combat_log.md), [Using the Combat Log](../guides/03_combat_log.md)


---

## Generated API

## `gem.combatlog.CombatLogProcessor`

### `CombatLogProcessor`

```python
class CombatLogProcessor
```

Parses and dispatches combat log entries.

Source: [src/gem/combatlog.py:171](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/combatlog.py#L171)

#### Methods

##### `on_combat_log_entry`

Signature: `def CombatLogProcessor.on_combat_log_entry(self, handler: CombatLogHandler) -> None`

Register a handler to receive decoded CombatLogEntry objects.

Source: [src/gem/combatlog.py:181](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/combatlog.py#L181)

##### `process_rune_pickup`

Signature: `def CombatLogProcessor.process_rune_pickup(self, player_slot: int, rune_type: int, tick: int = 0) -> None`

Emit a PICKUP_RUNE CombatLogEntry from a CDOTAUserMsg_ChatEvent.

Source: [src/gem/combatlog.py:189](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/combatlog.py#L189)

##### `process_s1_event`

Signature: `def CombatLogProcessor.process_s1_event(self, game_event: Any, name_table: Any, tick: int = 0) -> None`

Parse a ``dota_combatlog`` S1 game event and emit a CombatLogEntry.

Source: [src/gem/combatlog.py:214](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/combatlog.py#L214)

##### `process_s2_bulk`

Signature: `def CombatLogProcessor.process_s2_bulk(self, msg: Any, name_table: Any, tick: int = 0) -> None`

Parse a CDOTAUserMsg_CombatLogBulkData and emit CombatLogEntry per entry.

Source: [src/gem/combatlog.py:259](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/combatlog.py#L259)

##### `process_s2_entry`

Signature: `def CombatLogProcessor.process_s2_entry(self, msg: Any, name_table: Any, tick: int = 0) -> None`

Parse a CMsgDOTACombatLogEntry and emit a CombatLogEntry.

Source: [src/gem/combatlog.py:271](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/combatlog.py#L271)

## `gem.combatlog.CombatLogEntry`

### `CombatLogEntry`

```python
class CombatLogEntry
```

One decoded combat log entry.

Source: [src/gem/combatlog.py:95](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/combatlog.py#L95)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `log_type` | `str` | `-` |
| `attacker_name` | `str` | `''` |
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
