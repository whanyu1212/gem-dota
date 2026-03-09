"""Ward placement extractor for Dota 2 replays.

Combines the combat log (who placed a ward and when) with the entity stream
(exact map coordinates) to produce complete ward placement records.

Key technique for 100% coordinate coverage:
- Accept ALL non-DELETED entity events for ward entities, including UPDATED
  events on recycled entity slots.
- Do NOT globally consume entity records when matching — the same slot is
  reused across the game, so the same entity event may match multiple
  placements at different ticks.
- For each combat log ITEM ward placement, find the entity event with the
  smallest tick delta within ±``coord_window`` ticks.

Reference: examples/ward_smoke_rosh.py,
           refs/parser/src/main/java/opendota/processors/warding/Wards.java
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

_WARD_ITEMS: frozenset[str] = frozenset(
    {"item_ward_observer", "item_ward_sentry", "item_ward_dispenser"}
)
_ITEM_TO_WARD_TYPE: dict[str, Literal["observer", "sentry"]] = {
    "item_ward_observer": "observer",
    "item_ward_dispenser": "observer",  # dispenser plants an observer ward
    "item_ward_sentry": "sentry",
}

_WARD_CLASSES: frozenset[str] = frozenset(
    {
        "CDOTA_NPC_Observer_Ward",
        "CDOTA_NPC_Observer_Ward_TrueSight",
    }
)


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
    cell_x, ok_cx = entity.get_uint32("CBodyComponent.m_cellX")
    cell_y, ok_cy = entity.get_uint32("CBodyComponent.m_cellY")
    vec_x, ok_vx = entity.get_float32("CBodyComponent.m_vecX")
    vec_y, ok_vy = entity.get_float32("CBodyComponent.m_vecY")
    if not (ok_cx and ok_cy and ok_vx and ok_vy):
        return None
    return (cell_x * _CELL_SIZE + vec_x, cell_y * _CELL_SIZE + vec_y)


# ---------------------------------------------------------------------------
# Internal placement record (pre-finalization)
# ---------------------------------------------------------------------------


@dataclass
class _WardPlacement:
    tick: int
    placer: str  # NPC hero name from combat log
    ward_type: Literal["observer", "sentry"]


# ---------------------------------------------------------------------------
# Public data class
# ---------------------------------------------------------------------------


@dataclass
class WardEvent:
    """A complete ward placement record with coordinates.

    Attributes:
        tick: Game tick when the ward was placed (from combat log).
        player_id: Player slot (0-9), or -1 if unresolvable.
        placer: NPC hero name of the hero who placed the ward.
        ward_type: ``"observer"`` or ``"sentry"``.
        team: Team number (2=Radiant, 3=Dire), or 0 if unknown.
        x: World x coordinate of the ward, or ``None`` if no entity match found.
        y: World y coordinate of the ward, or ``None`` if no entity match found.
        expires_tick: Tick when the ward expired naturally, or ``None``.
        killed_tick: Tick when the ward was killed by an enemy, or ``None``.
        killer: NPC name of the unit that killed the ward, or ``""`` if not applicable.
    """

    tick: int
    player_id: int
    placer: str
    ward_type: Literal["observer", "sentry"]
    team: int
    x: float | None
    y: float | None
    # TODO Phase 6: populate expires_tick and killed_tick via m_lifeState tracking
    expires_tick: int | None
    killed_tick: int | None
    killer: str


# ---------------------------------------------------------------------------
# Entity spawn log entry type alias
# ---------------------------------------------------------------------------

# (tick, ward_type, team, x, y)
_SpawnRecord = tuple[int, str, int, float, float]


# ---------------------------------------------------------------------------
# Coordinate matching
# ---------------------------------------------------------------------------


def _match_coords(
    placements: list[_WardPlacement],
    spawns: list[_SpawnRecord],
    ward_type: Literal["observer", "sentry"],
    window: int,
) -> dict[int, tuple[float, float]]:
    """Match placement ticks to entity spawn coordinates.

    Finds the nearest entity event within ``window`` ticks for each placement.
    The same spawn record may match multiple placements (entity slot reuse).

    Args:
        placements: Internal placement records of the given ``ward_type``.
        spawns: All entity spawn records accumulated during parsing.
        ward_type: Filter spawns to this type before matching.
        window: Maximum tick delta to consider a match.

    Returns:
        Mapping from placement list index to ``(x, y)`` coordinates.
        Placements with no match within the window are absent from the dict.
    """
    relevant = sorted(
        [(t, x, y) for t, wt, _team, x, y in spawns if wt == ward_type],
        key=lambda e: e[0],
    )
    result: dict[int, tuple[float, float]] = {}
    for i, wp in enumerate(placements):
        best_pos: tuple[float, float] | None = None
        best_dt = window + 1
        for et, ex, ey in relevant:
            if et < wp.tick - window:
                continue
            if et > wp.tick + window:
                break
            dt = abs(et - wp.tick)
            if dt < best_dt:
                best_pos = (ex, ey)
                best_dt = dt
        if best_pos is not None:
            result[i] = best_pos
    return result


# ---------------------------------------------------------------------------
# Extractor
# ---------------------------------------------------------------------------


class WardsExtractor:
    """Extracts ward placement events with exact map coordinates.

    Combines two data streams:
    - **Combat log** ``ITEM`` events: who placed a ward and at what tick.
    - **Entity stream**: exact map coordinates from ward entity position fields.

    Coordinate matching is performed lazily when ``ward_events`` is first
    accessed (or explicitly via ``finalize()``). Access ``ward_events`` only
    after ``parse()`` has completed.

    Example:
        >>> extractor = WardsExtractor()
        >>> extractor.attach(parser)
        >>> parser.parse()
        >>> for event in extractor.ward_events:
        ...     print(event.tick, event.placer, event.x, event.y)

    Attributes:
        coord_window: Tick window used for coordinate matching (default 60).
    """

    def __init__(self, coord_window: int = 60) -> None:
        """Initialise the extractor.

        Args:
            coord_window: Maximum tick delta when matching placements to entity
                spawn records. Default 60 ticks ≈ 2 seconds.
        """
        self.coord_window = coord_window
        self._parser: ReplayParser | None = None
        self._placements: list[_WardPlacement] = []
        # Entity spawn log: (tick, ward_type, team, x, y)
        self._spawns: list[_SpawnRecord] = []
        # Hero entity cache for player_id lookup: npc_name → Entity
        self._heroes_by_npc: dict[str, Entity] = {}
        # Cached finalized results
        self._finalized: list[WardEvent] | None = None

    def attach(self, parser: ReplayParser) -> None:
        """Register callbacks with the parser.

        Args:
            parser: The ``ReplayParser`` instance to attach to.
        """
        self._parser = parser
        parser.on_combat_log_entry(self._on_combat_log)
        parser.on_entity(self._on_entity)

    @property
    def ward_events(self) -> list[WardEvent]:
        """Finalized ward placement records with matched coordinates.

        Triggers coordinate matching on first access. Access only after
        ``parse()`` has completed; earlier access yields partial results.

        Returns:
            List of ``WardEvent`` objects in chronological order.
        """
        if self._finalized is None:
            self._finalized = self._finalize()
        return self._finalized

    def finalize(self) -> list[WardEvent]:
        """Force coordinate matching and return results.

        Returns:
            List of ``WardEvent`` objects in chronological order.
        """
        self._finalized = self._finalize()
        return self._finalized

    def _on_combat_log(self, entry: CombatLogEntry) -> None:
        if entry.log_type == "ITEM" and entry.inflictor_name in _WARD_ITEMS:
            ward_type = _ITEM_TO_WARD_TYPE[entry.inflictor_name]
            self._placements.append(
                _WardPlacement(
                    tick=entry.tick,
                    placer=entry.attacker_name,
                    ward_type=ward_type,
                )
            )

    def _on_entity(self, entity: Entity, op: EntityOp) -> None:
        cls = entity.get_class_name()

        # Track hero entities for player_id resolution
        if cls.startswith("CDOTA_Unit_Hero_"):
            npc = cls.replace("CDOTA_Unit_Hero_", "npc_dota_hero_").lower()
            if op.has(EntityOp.DELETED):
                self._heroes_by_npc.pop(npc, None)
            else:
                self._heroes_by_npc[npc] = entity

        # Record ward entity positions (all non-DELETED events, including UPDATED
        # on recycled slots, to achieve 100% coordinate coverage)
        elif cls in _WARD_CLASSES and not op.has(EntityOp.DELETED):
            pos = _pos(entity)
            if pos is None:
                return
            ward_type: Literal["observer", "sentry"] = (
                "sentry" if "TrueSight" in cls else "observer"
            )
            team, _ = entity.get_int32("m_iTeamNum")
            tick = self._parser.tick if self._parser is not None else 0
            self._spawns.append((tick, ward_type, team, pos[0], pos[1]))

    def _finalize(self) -> list[WardEvent]:
        obs = [p for p in self._placements if p.ward_type == "observer"]
        sen = [p for p in self._placements if p.ward_type == "sentry"]

        obs_coords = _match_coords(obs, self._spawns, "observer", self.coord_window)
        sen_coords = _match_coords(sen, self._spawns, "sentry", self.coord_window)

        # Build separate index-to-event lists for each type, then merge by tick
        events: list[WardEvent] = []

        for i, wp in enumerate(obs):
            coord = obs_coords.get(i)
            events.append(self._make_event(wp, coord))

        for i, wp in enumerate(sen):
            coord = sen_coords.get(i)
            events.append(self._make_event(wp, coord))

        events.sort(key=lambda e: e.tick)
        return events

    def _make_event(self, wp: _WardPlacement, coord: tuple[float, float] | None) -> WardEvent:
        # Resolve player_id from hero entity cache
        hero = self._heroes_by_npc.get(wp.placer.lower())
        player_id = -1
        team = 0
        if hero is not None:
            pid, ok = hero.get_int32("m_nPlayerID")
            if not ok:
                pid, ok = hero.get_int32("m_iPlayerID")
            if ok and pid >= 0:
                pid //= 2
                player_id = pid
            t, ok_t = hero.get_int32("m_iTeamNum")
            if ok_t:
                team = t

        return WardEvent(
            tick=wp.tick,
            player_id=player_id,
            placer=wp.placer,
            ward_type=wp.ward_type,
            team=team,
            x=coord[0] if coord is not None else None,
            y=coord[1] if coord is not None else None,
            expires_tick=None,
            killed_tick=None,
            killer="",
        )
