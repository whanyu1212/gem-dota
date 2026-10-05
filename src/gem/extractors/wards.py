"""Ward placement extractor for Dota 2 replays.

Uses entity ``m_lifeState`` transitions as the primary placement signal — the
same approach as the OpenDota reference parser.  When a ward entity transitions
to ``m_lifeState == 0`` (alive) the entity already carries exact coordinates and
``m_hOwnerEntity``, so no coordinate-matching window is needed.

Ward death/expiry is detected on the transition to ``m_lifeState == 1``
(dying).  Like OpenDota, the transition is handled once its tick is over, after
that tick's combat log: each ward ``DEATH`` entry queues its attacker and damage
source for its ward class, and the leaving ward takes the oldest one. A ward
that expires logs a ``DEATH`` whose attacker is the ward itself and whose damage
source is the owner's hero.

Reference: odota/parser src/main/java/opendota/processors/warding/Wards.java
           odota/parser src/main/java/opendota/Parse.java  (buildWardEntry)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from gem.combat.log import CombatLogEntry
from gem.extractors._snapshots import _hero_npc_name, _player_id_from_entity, _pos
from gem.schema.sendtable.models import FieldAccessPlan
from gem.state.entities import Entity, EntityOp

if TYPE_CHECKING:
    from gem.parser import ReplayParser

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_WARD_CLASSES: frozenset[str] = frozenset(
    {
        "CDOTA_NPC_Observer_Ward",
        "CDOTA_NPC_Observer_Ward_TrueSight",
    }
)
_WARD_FIELDS = FieldAccessPlan(("m_lifeState", "m_iTeamNum", "m_hOwnerEntity"))

# Combat-log target names used in DEATH events for wards (ref Wards.java)
_WARD_TARGET_NAMES: frozenset[str] = frozenset({"npc_dota_observer_wards", "npc_dota_sentry_wards"})

# Mapping from entity class → combat-log target name (for killer queue lookup)
_CLASS_TO_TARGET: dict[str, str] = {
    "CDOTA_NPC_Observer_Ward": "npc_dota_observer_wards",
    "CDOTA_NPC_Observer_Ward_TrueSight": "npc_dota_sentry_wards",
}

# Ward lifespan in ticks (30 ticks/s). Durations per current patch:
# observer 360 s (6 min), sentry 420 s (7 min).
# Reference: https://liquipedia.net/dota2/Observer_Ward,
#            https://liquipedia.net/dota2/Sentry_Ward
_OBSERVER_LIFESPAN_TICKS = 360 * 30  # 10800 ticks (6 min)
_SENTRY_LIFESPAN_TICKS = 420 * 30  # 12600 ticks (7 min)
_EXPIRY_TOLERANCE_TICKS = 30  # grace window to classify natural expiry vs. kill


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
    event: WardEvent | None = None  # this placement's record


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
        left_attacker: Damage source of the combat-log ``DEATH`` paired with the
            ward leaving, as OpenDota's ``attackername`` (the owner's hero for an
            expiry; ``"dota_unknown"`` for an unnamed source), or ``None`` if no
            ``DEATH`` was paired or the ward has not left.
        left_player_id: Player slot of the ward's owner when it left, read from
            ``m_hOwnerEntity`` then, as OpenDota does; ``-1`` if that owner no
            longer resolves (OpenDota then logs the leave for no player), or
            ``None`` if not recorded.
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
    left_attacker: str | None = None
    left_player_id: int | None = None


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
        # (attacker, damage source) of ward DEATH entries per ward target name,
        # oldest first (Wards.java wardKillersByWardClass)
        self._killer_queue: dict[str, list[tuple[str, str]]] = {
            target: [] for target in _WARD_TARGET_NAMES
        }
        # Wards that left during a tick, handled once that tick is over
        # (Wards.java defers lifestate changes to the tick end):
        # (tick, entity class, slot state, owner player id at leave time)
        self._pending_left: list[tuple[int, str, _SlotState, int]] = []
        # Hero NPC name by player_id — populated from entity stream
        self._hero_by_player_id: dict[int, str] = {}
        # Hero class name -> NPC name from the EntityNames string table.
        self._hero_names: dict[str, str] = {}
        # Completed placement records
        self.ward_events: list[WardEvent] = []

    def attach(self, parser: ReplayParser) -> None:
        """Register callbacks with the parser.

        Args:
            parser: The ``ReplayParser`` instance to attach to.
        """
        self._parser = parser
        parser.on_combat_log_entry(self._on_combat_log)
        parser._on_entity_filtered(
            self._on_entity,
            class_names=_WARD_CLASSES,
            class_prefixes=("CDOTA_Unit_Hero_",),
        )

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
        self._flush_pending_left(before_tick=None)
        for ev in self.ward_events:
            if ev.placer == "" and ev.player_id >= 0:
                npc = self._hero_by_player_id.get(ev.player_id, "")
                ev.placer = npc
        return self.ward_events

    # ------------------------------------------------------------------
    # Combat log — killer queues only (mirrors Wards.java onCombatLogEntry)
    # ------------------------------------------------------------------

    def _on_combat_log(self, entry: CombatLogEntry) -> None:
        self._flush_pending_left(before_tick=entry.tick)
        if entry.log_type != "DEATH" or entry.target_name not in _WARD_TARGET_NAMES:
            return
        # CombatLogNames index 0 resolves to ""; OpenDota prints it as dota_unknown.
        source = entry.damage_source_name or "dota_unknown"
        self._killer_queue[entry.target_name].append((entry.attacker_name, source))

    # ------------------------------------------------------------------
    # Entity stream — primary placement/death signal
    # ------------------------------------------------------------------

    def _on_entity(self, entity: Entity, op: EntityOp) -> None:
        cls = entity.get_class_name()

        # Track heroes by player_id for late placer attribution
        if cls.startswith("CDOTA_Unit_Hero_"):
            pid = _player_id_from_entity(entity)
            if pid is not None:
                self._hero_by_player_id[pid] = self._hero_name(entity)
            return

        if cls not in _WARD_CLASSES:
            return

        idx = entity.get_index()
        tick = self._tick
        self._flush_pending_left(before_tick=tick)

        if op.has(EntityOp.DELETED):
            self._prev_lifestate.pop(idx, None)
            self._active.pop(idx, None)
            return

        fields = entity._resolve_fields(_WARD_FIELDS)
        life_state = entity._get_int32_resolved(fields[0])
        if life_state is None:
            life_state = 0 if op.has(EntityOp.CREATED) else 2

        prev_ls = self._prev_lifestate.get(idx, 2)
        self._prev_lifestate[idx] = life_state

        # ---- Transition to alive (0): ward placed ----
        if life_state == 0 and prev_ls != 0:
            self._on_ward_placed(entity, cls, idx, tick)

        # ---- Transition to dying (1): ward killed or expired ----
        elif life_state == 1 and prev_ls == 0:
            self._on_ward_left(entity, cls, idx, tick)

    def _hero_name(self, hero: Entity) -> str:
        """The hero's NPC name, as the combat log and ``ParsedPlayer`` spell it.

        Class names are ambiguous for compound heroes:
        ``CDOTA_Unit_Hero_AncientApparition`` is
        ``npc_dota_hero_ancient_apparition``, so the ``EntityNames`` string table
        decides (as in ``PlayerExtractor``). The lowercased class name is only the
        fallback before the table resolves, and is not cached.
        """
        cls = hero.get_class_name()
        cached = self._hero_names.get(cls)
        if cached is not None:
            return cached
        tables = getattr(self._parser, "string_tables", None)
        resolved = _hero_npc_name(
            hero, tables.get_by_name("EntityNames") if tables is not None else None
        )
        if resolved is None:
            return "npc_dota_hero_" + cls[len("CDOTA_Unit_Hero_") :].lower()
        self._hero_names[cls] = resolved
        return resolved

    def _on_ward_placed(
        self,
        entity: Entity,
        cls: str,
        idx: int,
        tick: int,
    ) -> None:
        pos = _pos(entity)
        ward_type: Literal["observer", "sentry"] = "sentry" if "TrueSight" in cls else "observer"
        fields = entity._resolve_fields(_WARD_FIELDS)
        team = entity._get_int32_resolved(fields[1]) or 0

        # Resolve placer via m_hOwnerEntity → owner entity → player slot
        player_id = -1
        placer_npc = ""
        owner_handle = entity._get_uint32_resolved(fields[2])
        if owner_handle is not None and self._parser is not None:
            em = self._parser.entity_manager
            if em is not None:
                owner = em.find_by_handle(owner_handle)
                # The ward's owner can be an owned unit (not the hero directly),
                # so allow the m_iPlayerOwnerID fallback here.
                # -1 sentinel = unresolved placer (consumed downstream as `>= 0`).
                resolved = _player_id_from_entity(owner, allow_owner=True)
                player_id = resolved if resolved is not None else -1
                if owner is not None:
                    owner_cls = owner.get_class_name()
                    if owner_cls.startswith("CDOTA_Unit_Hero_"):
                        placer_npc = self._hero_name(owner)

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

        state.event = WardEvent(
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
        self.ward_events.append(state.event)

    def _on_ward_left(self, entity: Entity, cls: str, idx: int, tick: int) -> None:
        state = self._active.pop(idx, None)
        if state is None:
            return
        # OpenDota reads the owner's slot when the ward leaves, not at placement.
        owner_id = -1
        owner_handle = entity._get_uint32_resolved(entity._resolve_fields(_WARD_FIELDS)[2])
        if owner_handle is not None and self._parser is not None:
            em = self._parser.entity_manager
            if em is not None:
                resolved = _player_id_from_entity(em.find_by_handle(owner_handle), allow_owner=True)
                owner_id = resolved if resolved is not None else -1
        self._pending_left.append((tick, cls, state, owner_id))

    def _flush_pending_left(self, before_tick: int | None) -> None:
        """Handle wards that left in ticks before ``before_tick`` (all if ``None``).

        By then every ``DEATH`` entry of their tick is queued, so a ward that
        left takes its own entry rather than a later ward's.
        """
        if not self._pending_left:
            return
        ready: list[tuple[int, str, _SlotState, int]] = []
        waiting: list[tuple[int, str, _SlotState, int]] = []
        for pending in self._pending_left:
            (ready if before_tick is None or pending[0] < before_tick else waiting).append(pending)
        self._pending_left = waiting
        for tick, cls, state, owner_id in ready:
            self._resolve_left(tick, cls, state, owner_id)

    def _resolve_left(self, tick: int, cls: str, state: _SlotState, owner_id: int) -> None:
        event = state.event if state.event is not None else self._find_ward_event(state)
        if event is None:
            return
        event.left_player_id = owner_id

        target_name = _CLASS_TO_TARGET.get(cls, "")
        killer_queue = self._killer_queue.get(target_name, [])

        natural_ticks = (
            _OBSERVER_LIFESPAN_TICKS if state.ward_type == "observer" else _SENTRY_LIFESPAN_TICKS
        )

        if killer_queue:
            killer, source = killer_queue.pop(0)
            event.left_attacker = source
            # Ward killing itself = natural expiry reported via combat log
            if killer in _WARD_TARGET_NAMES:
                event.expires_tick = tick
            else:
                event.killed_tick = tick
                event.killer = killer
        elif tick >= state.spawn_tick + natural_ticks - _EXPIRY_TOLERANCE_TICKS:
            event.expires_tick = tick
        else:
            # Killed but no combat log killer was logged — mark as killed
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
