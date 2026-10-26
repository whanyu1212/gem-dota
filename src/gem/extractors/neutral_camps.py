"""Neutral camp extractor: every creep a camp spawned, and every camp stack.

Each neutral camp is a ``CDOTA_NeutralSpawner`` entity; its position is the
camp's centre in ``camp_zones.json`` and ``m_Type`` its tier (0 small … 3
ancient). Each creep it spawns is a ``CDOTA_BaseNPC_Creep_Neutral`` whose
``m_hNeutralSpawner`` is the spawner's handle. A creep spawns on the tick its
``m_bIsWaitingToSpawn`` clears and dies on the tick its ``m_lifeState`` leaves 0
(the entity is deleted 5–10 s later, with the corpse).

A camp is stacked when it spawns a wave while creeps from an earlier wave are
still alive, and the game counts it: the team data's
``m_vecDataTeam.NNNN.m_iCampsStacked`` rises for the stacking player on that spawn
tick, by the number of camps they stacked. A lone straggler from an earlier wave
(a creep left outside its camp) also lets the camp respawn, but uncounted; on 8 of
the 10 local fixtures there is none, and every overlapping spawn is a credited
stack. Which of a tick's stacks is whose comes from sampled hero positions before
the spawn (see :func:`credit_stacks`); a creep's killer comes from the combat
log's ``DEATH`` entries (see :func:`resolve_killers`).

The combat log's ``NEUTRAL_CAMP_STACK`` type never appears in these replays.
odota/parser reads only the counters (``m_iCampsStacked`` and
``m_iCreepsStacked``, as ``camps_stacked`` and ``creeps_stacked``); the creep and
spawner fields are gem-original, checked against those counters.

Reference: odota/parser src/main/java/opendota/Parse.java (pinned revision in
CLAUDE.md).
"""

from __future__ import annotations

import bisect
import math
from collections import Counter, defaultdict
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import TYPE_CHECKING

from gem.catalog.map import load_neutral_camps
from gem.extractors._snapshots import (
    TEAM_DIRE,
    TEAM_RADIANT,
    _pos,
    team_data_prefix,
)
from gem.schema.sendtable.models import FieldAccessPlan
from gem.state.entities import EntityOp

if TYPE_CHECKING:
    from gem.combat.log import CombatLogEntry
    from gem.parser import ReplayParser
    from gem.state.entities import Entity

__all__ = [
    "CampStack",
    "NeutralCampExtractor",
    "NeutralCreep",
    "StackCredit",
    "credit_stacks",
    "resolve_killers",
]

_SPAWNER_CLASS = "CDOTA_NeutralSpawner"
_NEUTRAL_PREFIX = "npc_dota_neutral_"
_NULL_HANDLE = 0xFFFFFF
_HANDLE_INDEX_MASK = 0x3FFF
_CAMP_TYPES = ("small", "medium", "large", "ancient")
#: A spawner further than this from every catalogued camp centre maps to no camp.
_CAMP_MATCH_DISTANCE = 16.0
_TICKS_PER_SECOND = 30
#: Hero positions sampled this many seconds before the spawn place a stacker
#: (the pull starts about xx:53).
_STACKER_WINDOW_S = (3, 10)
#: A stacker further than this from a stacked camp in that window is not its stacker.
_STACKER_MAX_DISTANCE = 1500.0

_CREEP_FIELDS = ("m_hNeutralSpawner", "m_bIsWaitingToSpawn", "m_lifeState")
_COUNTER_FIELDS = FieldAccessPlan(
    tuple(f"{team_data_prefix(team_slot)}.m_iCampsStacked" for team_slot in range(5))
)


@dataclass
class NeutralCreep:
    """One creep a neutral camp spawned.

    Attributes:
        camp_id: The camp's ``id`` in ``camp_zones.json``, or ``None`` if its
            spawner matches no catalogued camp.
        spawned_tick: Replay tick the creep spawned.
        died_tick: Replay tick it died, or ``None`` if it was alive at the end.
        killer_name: The ``attacker_name`` of the neutral ``DEATH`` entries on
            its death tick, when they agree on one. A lane creep here means a
            pull; a neutral means a flooded camp's creep growing into its next
            form, which the combat log records as a death to its camp. ``None``
            if they disagree (another neutral died on the same tick to someone
            else) or are missing.
        killer_player_id: The player credited with the kill (a summon's or
            illusion's kill goes to its owner, as for hero kills), or ``None``.
    """

    camp_id: int | None
    spawned_tick: int
    died_tick: int | None = None
    killer_name: str | None = None
    killer_player_id: int | None = None


@dataclass
class CampStack:
    """A camp stack: a spawn while an earlier wave was alive, counted by the game.

    Attributes:
        tick: Replay tick of the spawn (the tick the game credits the stack).
        camp_id: The camp's ``id`` in ``camp_zones.json``, or ``None``.
        camp_type: ``small``, ``medium``, ``large`` or ``ancient``: the spawner's
            ``m_Type`` at the spawn (flooded camps report their current tier), or
            ``None`` if unknown.
        creeps_before: Creeps from earlier waves alive at the spawn; one that
            dies on the spawn tick is not counted.
        waves_alive: Waves with a creep alive after the spawn, the new one
            included (2 for a camp stacked once).
        player_id: The player the game credited with the stack, or ``None`` if
            the credit could not be placed (no sampled position near the camp).
        player_exact: ``True`` when the credit leaves no choice (one player
            credited with every camp stacked on the tick); ``False`` when the
            camp was matched to the player by sampled position, or unresolved.
    """

    tick: int
    camp_id: int | None
    camp_type: str | None
    creeps_before: int
    waves_alive: int
    player_id: int | None = None
    player_exact: bool = False


@dataclass(frozen=True, slots=True)
class StackCredit:
    """One rise in a team slot's ``m_iCampsStacked``.

    Attributes:
        tick: Replay tick of the rise.
        team: ``TEAM_RADIANT`` or ``TEAM_DIRE``.
        team_slot: The ``m_vecDataTeam`` row, 0-4.
        camps: How many camps the rise credits.
    """

    tick: int
    team: int
    team_slot: int
    camps: int


@dataclass
class _CreepRecord:
    spawner: int
    spawned_tick: int | None = None
    died_tick: int | None = None


class NeutralCampExtractor:
    """Collects camp creeps, spawner tiers and stack credits during a parse.

    Attach to a ``ReplayParser`` before calling ``parse()``, then call
    :meth:`finalize`.

    Attributes:
        credits: Rises in each team slot's ``m_iCampsStacked``, in replay order.
    """

    def __init__(self) -> None:
        """Initialise an empty extractor."""
        self.credits: list[StackCredit] = []
        self._parser: ReplayParser | None = None
        self._camp_centres = [(camp["id"], (camp["x"], camp["y"])) for camp in load_neutral_camps()]
        # Spawner entity index -> camp id, and its (tick, m_Type) history.
        self._spawner_camp: dict[int, int | None] = {}
        self._spawner_types: dict[int, list[tuple[int, int]]] = defaultdict(list)
        # (entity index, serial) -> creep.
        self._creeps: dict[tuple[int, int], _CreepRecord] = {}
        self._stacked: dict[tuple[int, int], int] = {}

    def attach(self, parser: ReplayParser) -> None:
        """Register for spawners, camp creeps and the stack counters.

        Creep and counter updates are gated on their fields: neutral creeps
        update every tick they move.

        Args:
            parser: The replay parser to attach to.
        """
        self._parser = parser
        parser._on_entity_filtered(self._on_spawner, class_names=(_SPAWNER_CLASS,))
        parser._on_entity_fields(
            self._on_creep, required_fields=(_CREEP_FIELDS[0],), changed_fields=_CREEP_FIELDS
        )
        parser._on_entity_fields(
            self._on_counters,
            required_fields=(_COUNTER_FIELDS.names[0],),
            changed_fields=_COUNTER_FIELDS.names,
        )

    @property
    def _tick(self) -> int:
        return self._parser.tick if self._parser is not None else 0

    def _on_spawner(self, entity: Entity, op: EntityOp) -> None:
        if op.has(EntityOp.DELETED):
            return
        index = entity.get_index()
        if index not in self._spawner_camp:
            self._spawner_camp[index] = self._camp_at(_pos(entity))
        camp_type = entity.get_int32("m_Type")
        history = self._spawner_types[index]
        if camp_type is not None and (not history or history[-1][1] != camp_type):
            history.append((self._tick, camp_type))

    def _camp_at(self, pos: tuple[float, float] | None) -> int | None:
        if pos is None:
            return None
        distance, camp_id = min(
            (math.dist(pos, centre), camp_id) for camp_id, centre in self._camp_centres
        )
        return camp_id if distance <= _CAMP_MATCH_DISTANCE else None

    def _on_creep(self, entity: Entity, op: EntityOp) -> None:
        if op.has(EntityOp.DELETED):
            return
        key = (entity.get_index(), entity.get_serial())
        creep = self._creeps.get(key)
        if creep is None:
            handle = entity.get_uint32("m_hNeutralSpawner")
            if handle is None or handle == _NULL_HANDLE:
                return
            creep = self._creeps[key] = _CreepRecord(handle & _HANDLE_INDEX_MASK)
        if creep.spawned_tick is None:
            if entity.get_bool("m_bIsWaitingToSpawn") is False:
                creep.spawned_tick = self._tick
            return
        if creep.died_tick is None and (entity.get_int32("m_lifeState") or 0) != 0:
            creep.died_tick = self._tick

    def _on_counters(self, entity: Entity, op: EntityOp) -> None:
        if op.has(EntityOp.DELETED):
            return
        team = TEAM_RADIANT if "Radiant" in entity.get_class_name() else TEAM_DIRE
        fresh = op.has(EntityOp.CREATED_ENTERED)
        fields = entity._resolve_fields(_COUNTER_FIELDS)
        for team_slot in range(5):
            value = entity._get_int32_resolved(fields[team_slot])
            if value is None:
                continue
            before = None if fresh else self._stacked.get((team, team_slot))
            self._stacked[(team, team_slot)] = value
            if before is not None and value > before:
                self.credits.append(StackCredit(self._tick, team, team_slot, value - before))

    def finalize(self) -> tuple[list[NeutralCreep], list[CampStack]]:
        """Return the camp creeps that spawned and the candidate stacks.

        Candidates are found from the creeps alone: spawns with an earlier wave
        alive. :func:`credit_stacks` keeps those the game credited and sets
        their players; :func:`resolve_killers` sets the creeps' killers.

        Returns:
            Every camp creep that spawned, by spawn tick, and every candidate
            stack, by tick.
        """
        creeps = [
            NeutralCreep(
                camp_id=self._spawner_camp.get(creep.spawner),
                spawned_tick=creep.spawned_tick,
                died_tick=creep.died_tick,
            )
            for creep in self._creeps.values()
            if creep.spawned_tick is not None
        ]
        creeps.sort(key=lambda creep: creep.spawned_tick)
        stacks = [
            CampStack(
                tick=tick,
                camp_id=self._spawner_camp.get(spawner),
                camp_type=self._camp_type(spawner, tick),
                creeps_before=creeps_before,
                waves_alive=waves_alive,
            )
            for spawner, tick, creeps_before, waves_alive in _find_stacks(
                (creep.spawner, creep.spawned_tick, creep.died_tick)
                for creep in self._creeps.values()
                if creep.spawned_tick is not None
            )
        ]
        stacks.sort(key=lambda stack: (stack.tick, stack.camp_id is None, stack.camp_id or 0))
        return creeps, stacks

    def _camp_type(self, spawner: int, tick: int) -> str | None:
        history = self._spawner_types.get(spawner, [])
        at = bisect.bisect_right(history, tick, key=lambda change: change[0]) - 1
        if at < 0:
            return None
        camp_type = history[at][1]
        return _CAMP_TYPES[camp_type] if 0 <= camp_type < len(_CAMP_TYPES) else None


def _find_stacks(
    creeps: Iterable[tuple[int, int, int | None]],
) -> list[tuple[int, int, int, int]]:
    """Find the spawns that came while an earlier wave of the camp was alive.

    Args:
        creeps: ``(camp key, spawned tick, died tick or None)`` per creep.

    Returns:
        ``(camp key, spawn tick, earlier creeps alive, waves alive)`` per stack.
    """
    waves: dict[int, dict[int, list[int | None]]] = defaultdict(lambda: defaultdict(list))
    for camp, spawned_tick, died_tick in creeps:
        waves[camp][spawned_tick].append(died_tick)
    stacks = []
    for camp, by_tick in waves.items():
        for tick in sorted(by_tick):
            alive_waves = [
                sum(1 for died in deaths if died is None or died > tick)
                for wave_tick, deaths in by_tick.items()
                if wave_tick < tick
            ]
            creeps_before = sum(alive_waves)
            if creeps_before:
                stacks.append((camp, tick, creeps_before, sum(1 for n in alive_waves if n) + 1))
    return stacks


def credit_stacks(
    candidates: list[CampStack],
    credits: Iterable[tuple[int, int, int]],
    positions: dict[int, list[tuple[int, float, float]]],
) -> list[CampStack]:
    """Return the candidate stacks the game credited, each with its player.

    A spawn with an earlier wave alive is a stack only if the game counted it:
    ``m_iCampsStacked`` rises on the spawn tick. A lone straggler from an earlier
    wave (a creep left outside its camp) lets the camp respawn without a credit.

    On each spawn tick, every player credited with ``n`` stacks takes ``n`` of
    that tick's candidates. If one player is credited with all of them, the
    assignment is exact. Otherwise camps go to the nearest credited player
    first, measured from the player's sampled positions 3–10 s before the spawn;
    a player with no sample in that window, or none within
    ``_STACKER_MAX_DISTANCE`` of the camp, takes no camp there. When a tick has
    more candidates than credits, the ones no player took are dropped; a tick
    with no credit keeps none.

    Args:
        candidates: Spawns with an earlier wave alive (``finalize``); their
            ``player_id`` and ``player_exact`` are set in place.
        credits: ``(tick, player id, camps credited)`` per counter rise.
        positions: Sampled ``(tick, x, y)`` positions per player id, by tick.

    Returns:
        The credited stacks, in tick order.
    """
    centres = {camp["id"]: (camp["x"], camp["y"]) for camp in load_neutral_camps()}
    quota_by_tick: dict[int, dict[int, int]] = defaultdict(lambda: defaultdict(int))
    for tick, player_id, camps in credits:
        quota_by_tick[tick][player_id] += camps
    by_tick: dict[int, list[CampStack]] = defaultdict(list)
    for stack in candidates:
        by_tick[stack.tick].append(stack)
    credited = []
    for tick, on_tick in by_tick.items():
        quota = quota_by_tick.get(tick, {})
        _assign(on_tick, quota, positions, centres, tick)
        if len(on_tick) > sum(quota.values()):
            on_tick = [stack for stack in on_tick if stack.player_id is not None]
        credited.extend(on_tick)
    return sorted(credited, key=lambda stack: stack.tick)


def _assign(
    stacks: list[CampStack],
    quota: dict[int, int],
    positions: dict[int, list[tuple[int, float, float]]],
    centres: dict[int, tuple[float, float]],
    tick: int,
) -> None:
    """Give each credited player their quota of one tick's stacks."""
    if len(quota) == 1:
        ((player_id, camps),) = quota.items()
        if camps == len(stacks):
            for stack in stacks:
                stack.player_id, stack.player_exact = player_id, True
            return
    pairs = sorted(
        (distance, player_id, index)
        for index, stack in enumerate(stacks)
        if stack.camp_id in centres
        for player_id in quota
        if (
            distance := _distance_before(positions.get(player_id, []), centres[stack.camp_id], tick)
        )
        is not None
        and distance <= _STACKER_MAX_DISTANCE
    )
    left = dict(quota)
    for _, player_id, index in pairs:
        stack = stacks[index]
        if stack.player_id is None and left[player_id] > 0:
            stack.player_id = player_id
            left[player_id] -= 1


def _distance_before(
    samples: list[tuple[int, float, float]], centre: tuple[float, float], tick: int
) -> float | None:
    """Closest sampled distance to ``centre`` within the stacker window before ``tick``."""
    start = tick - _STACKER_WINDOW_S[1] * _TICKS_PER_SECOND
    end = tick - _STACKER_WINDOW_S[0] * _TICKS_PER_SECOND
    lo = bisect.bisect_left(samples, start, key=lambda sample: sample[0])
    hi = bisect.bisect_right(samples, end, key=lambda sample: sample[0])
    distances = [math.dist((x, y), centre) for _, x, y in samples[lo:hi]]
    return min(distances) if distances else None


def resolve_killers(
    creeps: list[NeutralCreep],
    entries: Iterable[CombatLogEntry],
    kill_player: Callable[[str, str], int | None],
) -> None:
    """Set each creep's killer from the combat log's neutral ``DEATH`` entries.

    The combat log names a creep's unit but not its entity, so a creep is matched
    by its death tick: the killer is set when that tick has at least as many
    neutral ``DEATH`` entries as camp creeps dying, all with one attacker and
    credited player.

    Args:
        creeps: The creeps, updated in place.
        entries: The match's combat log.
        kill_player: ``(damage_source_name, attacker_name) -> player id``, the
            rule hero kills are credited by.
    """
    deaths: dict[int, list[tuple[str, int | None]]] = defaultdict(list)
    for entry in entries:
        if entry.log_type == "DEATH" and entry.target_name.startswith(_NEUTRAL_PREFIX):
            deaths[entry.tick].append(
                (entry.attacker_name, kill_player(entry.damage_source_name, entry.attacker_name))
            )
    dying = Counter(creep.died_tick for creep in creeps if creep.died_tick is not None)
    for creep in creeps:
        if creep.died_tick is None:
            continue
        on_tick = deaths.get(creep.died_tick, [])
        killers = set(on_tick)
        if len(on_tick) >= dying[creep.died_tick] and len(killers) == 1:
            ((creep.killer_name, creep.killer_player_id),) = killers
