# Neutral Camps Extractor

Every creep a neutral camp spawned, and every camp stack.

## Camps, creeps and stacks

Each camp is a `CDOTA_NeutralSpawner` entity at the camp's centre in `camp_zones.json`.
Each creep it spawns is a `CDOTA_BaseNPC_Creep_Neutral` that names its spawner in
`m_hNeutralSpawner`: it spawns when `m_bIsWaitingToSpawn` clears and dies when
`m_lifeState` leaves 0. A camp is stacked when it spawns a wave while creeps from an
earlier wave are still alive.

The game credits each stack to a player: the team data's `m_iCampsStacked` rises on
the spawn tick by the number of camps that player stacked (OpenDota's `camps_stacked`
is this counter). On the local fixtures the stacks found from the creeps equal the
counter's rises at every spawn tick. When one player is credited with every camp
stacked on a tick, the stack is theirs (`player_exact`); otherwise each camp goes to
the credited player nearest it in their sampled positions 3 to 10 seconds before the
spawn.

The combat log names a dying creep's unit but not its entity, so a creep's killer comes
from the neutral `DEATH` entries on its death tick, when they agree on one attacker. A
lane creep as the killer means a pull; a flooded camp's creeps that grow into their
next form are recorded as dying to their camp.

---

## Generated API

## Module `gem.extractors.neutral_camps`

Neutral camp extractor: every creep a camp spawned, and every camp stack.

Source: [src/gem/extractors/neutral_camps.py](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/neutral_camps.py#L1)

### Top-level functions

### `credit_stacks`

```python
def credit_stacks(candidates: list[CampStack], credits: Iterable[tuple[int, int, int]], positions: dict[int, list[tuple[int, float, float]]]) -> list[CampStack]
```

Return the candidate stacks the game credited, each with its player.

Source: [src/gem/extractors/neutral_camps.py:334](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/neutral_camps.py#L334)

### `resolve_killers`

```python
def resolve_killers(creeps: list[NeutralCreep], entries: Iterable[CombatLogEntry], kill_player: Callable[[str, str], int | None]) -> None
```

Set each creep's killer from the combat log's neutral ``DEATH`` entries.

Source: [src/gem/extractors/neutral_camps.py:425](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/neutral_camps.py#L425)

### Top-level classes

### `NeutralCreep`

```python
class NeutralCreep
```

One creep a neutral camp spawned.

Source: [src/gem/extractors/neutral_camps.py:83](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/neutral_camps.py#L83)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `camp_id` | `int \| None` | `-` |
| `spawned_tick` | `int` | `-` |
| `died_tick` | `int \| None` | `None` |
| `killer_name` | `str \| None` | `None` |
| `killer_player_id` | `int \| None` | `None` |

### `CampStack`

```python
class CampStack
```

A camp stack: a spawn while an earlier wave was alive, counted by the game.

Source: [src/gem/extractors/neutral_camps.py:109](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/neutral_camps.py#L109)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `camp_id` | `int \| None` | `-` |
| `camp_type` | `str \| None` | `-` |
| `creeps_before` | `int` | `-` |
| `waves_alive` | `int` | `-` |
| `player_id` | `int \| None` | `None` |
| `player_exact` | `bool` | `False` |

### `StackCredit`

```python
class StackCredit
```

One rise in a team slot's ``m_iCampsStacked``.

Source: [src/gem/extractors/neutral_camps.py:139](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/neutral_camps.py#L139)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `tick` | `int` | `-` |
| `team` | `int` | `-` |
| `team_slot` | `int` | `-` |
| `camps` | `int` | `-` |

### `NeutralCampExtractor`

```python
class NeutralCampExtractor
```

Collects camp creeps, spawner tiers and stack credits during a parse.

Source: [src/gem/extractors/neutral_camps.py:162](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/neutral_camps.py#L162)

#### Properties

##### `_tick`

Signature: `def NeutralCampExtractor._tick(self) -> int`

No docstring available.

Source: [src/gem/extractors/neutral_camps.py:205](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/neutral_camps.py#L205)

#### Methods

##### `attach`

Signature: `def NeutralCampExtractor.attach(self, parser: ReplayParser) -> None`

Register for spawners, camp creeps and the stack counters.

Source: [src/gem/extractors/neutral_camps.py:184](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/neutral_camps.py#L184)

##### `finalize`

Signature: `def NeutralCampExtractor.finalize(self) -> tuple[list[NeutralCreep], list[CampStack]]`

Return the camp creeps that spawned and the candidate stacks.

Source: [src/gem/extractors/neutral_camps.py:259](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/extractors/neutral_camps.py#L259)
