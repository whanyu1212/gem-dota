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

Source: [src/gem/combat/log.py:331](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/combat/log.py#L331)

#### Methods

##### `on_combat_log_entry`

Signature: `def CombatLogProcessor.on_combat_log_entry(self, handler: CombatLogHandler) -> None`

Register a handler to receive decoded CombatLogEntry objects.

Source: [src/gem/combat/log.py:341](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/combat/log.py#L341)

##### `process_rune_pickup`

Signature: `def CombatLogProcessor.process_rune_pickup(self, player_slot: int, rune_type: int, tick: int = 0) -> None`

Emit a PICKUP_RUNE CombatLogEntry from a CDOTAUserMsg_ChatEvent.

Source: [src/gem/combat/log.py:349](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/combat/log.py#L349)

##### `process_s1_event`

Signature: `def CombatLogProcessor.process_s1_event(self, game_event: Any, name_table: Any, tick: int = 0) -> None`

Parse a ``dota_combatlog`` S1 game event and emit a CombatLogEntry.

Source: [src/gem/combat/log.py:375](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/combat/log.py#L375)

##### `process_s2_bulk`

Signature: `def CombatLogProcessor.process_s2_bulk(self, msg: Any, name_table: Any, tick: int = 0) -> None`

Parse a CDOTAUserMsg_CombatLogBulkData and emit CombatLogEntry per entry.

Source: [src/gem/combat/log.py:446](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/combat/log.py#L446)

##### `process_s2_entry`

Signature: `def CombatLogProcessor.process_s2_entry(self, msg: Any, name_table: Any, tick: int = 0, game_time_s: int | None = None, source: CombatLogSource = CombatLogSource.S2_DIRECT) -> None`

Parse a CMsgDOTACombatLogEntry and emit a CombatLogEntry.

Source: [src/gem/combat/log.py:463](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/combat/log.py#L463)

## `gem.combat.log.CombatLogEntry`

### `CombatLogEntry`

```python
class CombatLogEntry
```

One decoded combat log entry.

Source: [src/gem/combat/log.py:145](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/combat/log.py#L145)

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
| `location_x` | `float \| None` | `None` |
| `location_y` | `float \| None` | `None` |
| `timestamp_s` | `float \| None` | `None` |
| `game_time_s` | `int \| None` | `None` |
| `will_reincarnate` | `bool` | `False` |
| `visible_radiant` | `bool \| None` | `None` |
| `visible_dire` | `bool \| None` | `None` |
| `modifier_duration_s` | `float \| None` | `None` |
| `modifier_elapsed_duration_s` | `float \| None` | `None` |
| `attacker_team` | `int \| None` | `None` |
| `target_team` | `int \| None` | `None` |
| `source` | `CombatLogSource` | `CombatLogSource.UNKNOWN` |
| `aura_modifier` | `bool \| None` | `None` |
| `modifier_purged` | `bool \| None` | `None` |
| `modifier_purged_duration_s` | `float \| None` | `None` |
| `attacker_is_hero_present` | `bool` | `False` |
| `target_is_hero_present` | `bool` | `False` |
| `attacker_is_illusion_present` | `bool` | `False` |
| `target_is_illusion_present` | `bool` | `False` |

#### Methods

##### `visible_to`

Signature: `def CombatLogEntry.visible_to(self, team: int) -> bool | None`

Return this event's S2 visibility flag for a playing team.

Source: [src/gem/combat/log.py:251](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/combat/log.py#L251)
