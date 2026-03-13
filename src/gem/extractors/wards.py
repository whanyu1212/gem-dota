"""Ward placement extractor for Dota 2 replays.

Uses entity ``m_lifeState`` transitions as the primary placement signal — the
same approach as the OpenDota reference parser.  When a ward entity transitions
to ``m_lifeState == 0`` (alive) the entity already carries exact coordinates and
``m_hOwnerEntity``, so no coordinate-matching window is needed.

Ward death/expiry is detected on the transition to ``m_lifeState == 1``
(dying).  The killer is read from the combat log ``DEATH`` queue that was
populated for the matching ward class.

Reference: refs/parser/src/main/java/opendota/processors/warding/Wards.java
           refs/parser/src/main/java/opendota/Parse.java  (buildWardEntry)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from gem.combatlog import CombatLogEntry
from gem.entities import Entity, EntityOp

if TYPE_CHECKING:
    from gem.parser import ReplayParser

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_CELL_SIZE = 128

_WARD_CLASSES: frozenset[str] = frozenset(
    {
        "CDOTA_NPC_Observer_Ward",
        "CDOTA_NPC_Observer_Ward_TrueSight",
    }
)

# Combat-log target names used in DEATH events for wards (ref Wards.java)
_WARD_TARGET_NAMES: frozenset[str] = frozenset({"npc_dota_observer_wards", "npc_dota_sentry_wards"})

# Mapping from entity class → combat-log target name (for killer queue lookup)
_CLASS_TO_TARGET: dict[str, str] = {
    "CDOTA_NPC_Observer_Ward": "npc_dota_observer_wards",
    "CDOTA_NPC_Observer_Ward_TrueSight": "npc_dota_sentry_wards",
}

# Ward lifespan in ticks (~30 ticks/s at normal speed)
_OBSERVER_LIFESPAN_TICKS = 720  # ~6 minutes
_SENTRY_LIFESPAN_TICKS = 360  # ~3 minutes
_EXPIRY_TOLERANCE_TICKS = 30  # grace window to classify natural expiry vs. kill


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _pos(entity: Entity) -> tuple[float, float] | None:
    """Return world (x, y) from cell+vec encoding on the entity.

    Args:
        entity: The entity to read coordinates from.

    Returns:
        ``(x, y)`` world coordinates, or ``None`` if any field is missing.
    """
    cell_x = entity.get_uint32("CBodyComponent.m_cellX")
    cell_y = entity.get_uint32("CBodyComponent.m_cellY")
    vec_x = entity.get_float32("CBodyComponent.m_vecX")
    vec_y = entity.get_float32("CBodyComponent.m_vecY")
    if cell_x is None or cell_y is None or vec_x is None or vec_y is None:
        return None
    return (cell_x * _CELL_SIZE + vec_x, cell_y * _CELL_SIZE + vec_y)


def _player_slot_from_entity(entity: Entity | None) -> int:
    """Read the player slot from a hero/controller entity.

    Mirrors ``getPlayerSlotFromEntity`` in Parse.java — tries ``m_nPlayerID``,
    then ``m_iPlayerID``, then ``m_iPlayerOwnerID``, divides by 2.

    Args:
        entity: Entity to read from, or ``None``.

    Returns:
        Player slot (0-9), or -1 if unresolvable.
    """
    if entity is None:
        return -1
    for field_name in ("m_nPlayerID", "m_iPlayerID", "m_iPlayerOwnerID"):
        val = entity.get_int32(field_name)
        if val is not None and val >= 0:
            return val // 2
    return -1


# ---------------------------------------------------------------------------
# Internal per-slot state
# ---------------------------------------------------------------------------


@dataclass
class _SlotState:
    """Live state for one active ward entity slot."""

    spawn_tick: int
    ward_type: Literal["observer", "sentry"]
    team: int
    x: float
    y: float
    player_id: int
    placer_npc: str  # resolved NPC name, e.g. "npc_dota_hero_shadow_demon"


# ---------------------------------------------------------------------------
# Public data class
# ---------------------------------------------------------------------------


@dataclass
class WardEvent:
    """A complete ward placement record with coordinates.

    Attributes:
        tick: Game tick when the ward was placed.
        player_id: Player slot (0-9), or -1 if unresolvable.
        placer: NPC hero name of the hero who placed the ward.
        ward_type: ``"observer"`` or ``"sentry"``.
        team: Team number (2=Radiant, 3=Dire), or 0 if unknown.
        x: World x coordinate of the ward.
        y: World y coordinate of the ward.
        expires_tick: Tick when the ward expired naturally, or ``None``.
        killed_tick: Tick when the ward was killed by an enemy, or ``None``.
        killer: NPC name of the unit that killed the ward, or ``""`` if not
            applicable.
    """

    tick: int
    player_id: int
    placer: str
    ward_type: Literal["observer", "sentry"]
    team: int
    x: float | None
    y: float | None
    expires_tick: int | None
    killed_tick: int | None
    killer: str


# ---------------------------------------------------------------------------
# Extractor
# ---------------------------------------------------------------------------


class WardsExtractor:
    """Extracts ward placement, expiry, and kill events from the entity stream.

    Uses ``m_lifeState`` transitions on ward entities as the primary signal —
    the same approach as the OpenDota reference parser.  Coordinates and placer
    attribution are read directly from the entity at placement time via
    ``m_hOwnerEntity``, so no post-parse coordinate matching is required.

    Example:
        >>> extractor = WardsExtractor()
        >>> extractor.attach(parser)
        >>> parser.parse()
        >>> for event in extractor.ward_events:
        ...     print(event.tick, event.placer, event.x, event.y)

    Attributes:
        ward_events: Finalized ``WardEvent`` list (available after ``parse()``).
    """

    def __init__(self) -> None:
        """Initialise the extractor."""
        self._parser: ReplayParser | None = None
        # Previous m_lifeState per entity index for transition detection
        self._prev_lifestate: dict[int, int] = {}
        # Live state per entity index (set on spawn, cleared on delete)
        self._active: dict[int, _SlotState] = {}
        # Killer queues per ward target name (matches Wards.java logic)
        self._killer_queue: dict[str, list[str]] = {target: [] for target in _WARD_TARGET_NAMES}
        # Hero NPC name by player_id — populated from entity stream
        self._hero_by_player_id: dict[int, str] = {}
        # Completed placement records
        self.ward_events: list[WardEvent] = []

    def attach(self, parser: ReplayParser) -> None:
        """Register callbacks with the parser.

        Args:
            parser: The ``ReplayParser`` instance to attach to.
        """
        self._parser = parser
        parser.on_combat_log_entry(self._on_combat_log)
        parser.on_entity(self._on_entity)

    @property
    def _tick(self) -> int:
        return self._parser.tick if self._parser is not None else 0

    def finalize(self) -> list[WardEvent]:
        """Back-fill placer names and return ward events.

        For pre-game wards where ``m_hOwnerEntity`` resolved to a
        ``CDOTAPlayerController`` (hero not yet assigned), the hero NPC name
        is filled in from the hero-by-player-id cache built during parsing.

        Returns:
            List of ``WardEvent`` objects in chronological order.
        """
        for ev in self.ward_events:
            if ev.placer == "" and ev.player_id >= 0:
                npc = self._hero_by_player_id.get(ev.player_id, "")
                ev.placer = npc
        return self.ward_events

    # ------------------------------------------------------------------
    # Combat log — killer queues only (mirrors Wards.java onCombatLogEntry)
    # ------------------------------------------------------------------

    def _on_combat_log(self, entry: CombatLogEntry) -> None:
        if entry.log_type == "DEATH" and entry.target_name in _WARD_TARGET_NAMES:
            killer = entry.attacker_name
            if killer:
                self._killer_queue[entry.target_name].append(killer)

    # ------------------------------------------------------------------
    # Entity stream — primary placement/death signal
    # ------------------------------------------------------------------

    def _on_entity(self, entity: Entity, op: EntityOp) -> None:
        cls = entity.get_class_name()

        # Track heroes by player_id for late placer attribution
        if cls.startswith("CDOTA_Unit_Hero_"):
            pid = entity.get_int32("m_nPlayerID")
            if pid is None:
                pid = entity.get_int32("m_iPlayerID")
            if pid is not None and pid >= 0:
                npc = "npc_dota_hero_" + cls[len("CDOTA_Unit_Hero_") :].lower()
                self._hero_by_player_id[pid // 2] = npc
            return

        if cls not in _WARD_CLASSES:
            return

        idx = entity.get_index()
        tick = self._tick

        if op.has(EntityOp.DELETED):
            self._prev_lifestate.pop(idx, None)
            self._active.pop(idx, None)
            return

        life_state = entity.get_int32("m_lifeState")
        if life_state is None:
            life_state = 0 if op.has(EntityOp.CREATED) else 2

        prev_ls = self._prev_lifestate.get(idx, 2)
        self._prev_lifestate[idx] = life_state

        # ---- Transition to alive (0): ward placed ----
        if life_state == 0 and prev_ls != 0:
            self._on_ward_placed(entity, cls, idx, tick)

        # ---- Transition to dying (1): ward killed or expired ----
        elif life_state == 1 and prev_ls == 0:
            self._on_ward_left(cls, idx, tick)

    def _on_ward_placed(
        self,
        entity: Entity,
        cls: str,
        idx: int,
        tick: int,
    ) -> None:
        pos = _pos(entity)
        ward_type: Literal["observer", "sentry"] = "sentry" if "TrueSight" in cls else "observer"
        team = entity.get_int32("m_iTeamNum") or 0

        # Resolve placer via m_hOwnerEntity → owner entity → player slot
        player_id = -1
        placer_npc = ""
        owner_handle = entity.get_uint32("m_hOwnerEntity")
        if owner_handle is not None and self._parser is not None:
            em = self._parser.entity_manager
            if em is not None:
                owner = em.find_by_handle(owner_handle)
                player_id = _player_slot_from_entity(owner)
                if owner is not None:
                    owner_cls = owner.get_class_name()
                    if owner_cls.startswith("CDOTA_Unit_Hero_"):
                        placer_npc = "npc_dota_hero_" + owner_cls[len("CDOTA_Unit_Hero_") :].lower()

        state = _SlotState(
            spawn_tick=tick,
            ward_type=ward_type,
            team=team,
            x=pos[0] if pos else 0.0,
            y=pos[1] if pos else 0.0,
            player_id=player_id,
            placer_npc=placer_npc,
        )
        self._active[idx] = state

        self.ward_events.append(
            WardEvent(
                tick=tick,
                player_id=player_id,
                placer=placer_npc,
                ward_type=ward_type,
                team=team,
                x=pos[0] if pos else None,
                y=pos[1] if pos else None,
                expires_tick=None,
                killed_tick=None,
                killer="",
            )
        )

    def _on_ward_left(self, cls: str, idx: int, tick: int) -> None:
        state = self._active.pop(idx, None)
        if state is None:
            return

        # Find the matching WardEvent in the list (last one for this slot)
        event = self._find_ward_event(state)
        if event is None:
            return

        target_name = _CLASS_TO_TARGET.get(cls, "")
        killer_queue = self._killer_queue.get(target_name, [])

        natural_ticks = (
            _OBSERVER_LIFESPAN_TICKS if state.ward_type == "observer" else _SENTRY_LIFESPAN_TICKS
        )

        if killer_queue:
            killer = killer_queue.pop(0)
            # Ward killing itself = natural expiry reported via combat log
            if killer in _WARD_TARGET_NAMES:
                event.expires_tick = tick
            else:
                event.killed_tick = tick
                event.killer = killer
        elif tick >= state.spawn_tick + natural_ticks - _EXPIRY_TOLERANCE_TICKS:
            event.expires_tick = tick
        else:
            # Killed but no combat log killer arrived yet — mark as killed
            event.killed_tick = tick

    def _find_ward_event(self, state: _SlotState) -> WardEvent | None:
        """Find the most recent WardEvent matching the given slot state.

        Args:
            state: The ``_SlotState`` for the dying ward slot.

        Returns:
            The matching ``WardEvent``, or ``None`` if not found.
        """
        # Scan backwards — most recent placement for this slot
        for ev in reversed(self.ward_events):
            if (
                ev.tick == state.spawn_tick
                and ev.ward_type == state.ward_type
                and ev.player_id == state.player_id
            ):
                return ev
        return None
