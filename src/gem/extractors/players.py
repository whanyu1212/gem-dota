"""Per-tick player statistics extractor for Dota 2 replays.

Polls hero entity state at configurable tick intervals and accumulates
snapshots for time-series analysis.

Reference: examples/extraction_demo.py, refs/parser/src/main/java/opendota/Parse.java
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from gem.entities import Entity, EntityOp

if TYPE_CHECKING:
    from gem.parser import ReplayParser

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_CELL_SIZE = 128  # Source 2 world units per grid cell
_TEAM_RADIANT = 2
_TEAM_DIRE = 3


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


def _snapshot_hero(entity: Entity, tick: int) -> PlayerStateSnapshot | None:
    """Build a ``PlayerStateSnapshot`` from a hero entity.

    Args:
        entity: A ``CDOTA_Unit_Hero_*`` entity.
        tick: Current game tick.

    Returns:
        A snapshot, or ``None`` if the player ID could not be resolved.
    """
    # m_nPlayerID (post-7.31) or m_iPlayerID (pre-7.31) — raw value is doubled;
    # divide by 2 to get player slot 0-9. Reference: opendota/Parse.java getPlayerSlotFromEntity()
    player_id, ok = entity.get_int32("m_nPlayerID")
    if not ok:
        player_id, ok = entity.get_int32("m_iPlayerID")
    if not ok or player_id < 0:
        return None
    player_id //= 2

    team, _ = entity.get_int32("m_iTeamNum")
    level, _ = entity.get_int32("m_nCurrentLevel")
    xp, _ = entity.get_int32("m_iCurrentXP")
    hp, _ = entity.get_int32("m_iHealth")
    max_hp, _ = entity.get_int32("m_iMaxHealth")
    mana, _ = entity.get_float32("m_flMana")
    max_mana, _ = entity.get_float32("m_flMaxMana")
    lh, _ = entity.get_int32("m_iLastHitCount")
    dn, _ = entity.get_int32("m_iDenies")

    pos = _pos(entity)

    return PlayerStateSnapshot(
        tick=tick,
        player_id=player_id,
        npc_name=entity.get_class_name().replace("CDOTA_Unit_Hero_", "npc_dota_hero_").lower(),
        team=team,
        level=level,
        xp=xp,
        gold=0,  # gold lives on CDOTAPlayerController; set by extractor if available
        net_worth=0,
        lh=lh,
        dn=dn,
        hp=hp,
        max_hp=max_hp,
        mana=mana,
        max_mana=max_mana,
        x=pos[0] if pos else None,
        y=pos[1] if pos else None,
    )


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class PlayerStateSnapshot:
    """A single per-player state sample taken at one tick.

    Attributes:
        tick: Game tick of this sample.
        player_id: Player slot (0-9).
        npc_name: Hero NPC name, e.g. ``"npc_dota_hero_axe"``.
        team: Team number (2=Radiant, 3=Dire).
        level: Hero level (1-30).
        xp: Cumulative XP total.
        gold: Reliable gold from ``CDOTAPlayerController``, or 0 if not read.
        net_worth: Net worth from ``CDOTAPlayerController``, or 0 if not read.
        lh: Last-hit count.
        dn: Deny count.
        hp: Current hit points.
        max_hp: Maximum hit points.
        mana: Current mana.
        max_mana: Maximum mana.
        x: World x coordinate, or ``None`` if unavailable.
        y: World y coordinate, or ``None`` if unavailable.
    """

    tick: int
    player_id: int
    npc_name: str
    team: int
    level: int
    xp: int
    gold: int
    net_worth: int
    lh: int
    dn: int
    hp: int
    max_hp: int
    mana: float
    max_mana: float
    x: float | None
    y: float | None


@dataclass
class PlayerTimeSeries:
    """Time-series data for one player, aggregated from snapshots.

    Attributes:
        player_id: Player slot (0-9).
        ticks: Tick values for each sample.
        gold_t: Reliable gold at each sample tick.
        net_worth_t: Net worth at each sample tick.
        lh_t: Last-hit count at each sample tick.
        dn_t: Deny count at each sample tick.
        xp_t: Cumulative XP at each sample tick.
    """

    player_id: int
    ticks: list[int] = field(default_factory=list)
    gold_t: list[int] = field(default_factory=list)
    net_worth_t: list[int] = field(default_factory=list)
    lh_t: list[int] = field(default_factory=list)
    dn_t: list[int] = field(default_factory=list)
    xp_t: list[int] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Extractor
# ---------------------------------------------------------------------------


class PlayerExtractor:
    """Polls hero entity state each tick and accumulates player snapshots.

    Attach to a ``ReplayParser`` before calling ``parse()``:

    Example:
        >>> extractor = PlayerExtractor(sample_interval=150)
        >>> extractor.attach(parser)
        >>> parser.parse()
        >>> ts = extractor.time_series(player_id=0)

    Attributes:
        snapshots: All collected ``PlayerStateSnapshot`` objects in
            chronological order.
    """

    snapshots: list[PlayerStateSnapshot]

    def __init__(self, sample_interval: int = 150) -> None:
        """Initialise the extractor.

        Args:
            sample_interval: Minimum tick gap between successive snapshots.
                Default 150 ticks ≈ 5 seconds at 30 ticks/sec.
        """
        self._sample_interval = sample_interval
        self._parser: ReplayParser | None = None
        self._last_sample: int = -sample_interval
        # entity index → Entity (mutable reference; entity is updated in place)
        self._heroes: dict[int, Entity] = {}
        # npc_name → Entity (for external position lookups)
        self._heroes_by_npc: dict[str, Entity] = {}
        # player_id → Entity (CDOTAPlayerController)
        self._controllers: dict[int, Entity] = {}
        self.snapshots = []

    def attach(self, parser: ReplayParser) -> None:
        """Register callbacks with the parser.

        Args:
            parser: The ``ReplayParser`` instance to attach to.
        """
        self._parser = parser
        parser.on_entity(self._on_entity)

    def hero_pos(self, npc_name: str) -> tuple[float, float] | None:
        """Return the current world position of a hero by NPC name.

        Args:
            npc_name: NPC hero name, e.g. ``"npc_dota_hero_axe"``.

        Returns:
            ``(x, y)`` world coordinates, or ``None`` if the hero is not tracked.
        """
        entity = self._heroes_by_npc.get(npc_name.lower())
        return _pos(entity) if entity is not None else None

    def time_series(self, player_id: int) -> PlayerTimeSeries:
        """Aggregate snapshots for one player into time-series lists.

        Args:
            player_id: Player slot (0-9).

        Returns:
            A ``PlayerTimeSeries`` with parallel lists indexed by sample number.
        """
        ts = PlayerTimeSeries(player_id=player_id)
        for snap in self.snapshots:
            if snap.player_id != player_id:
                continue
            ts.ticks.append(snap.tick)
            ts.gold_t.append(snap.gold)
            ts.net_worth_t.append(snap.net_worth)
            ts.lh_t.append(snap.lh)
            ts.dn_t.append(snap.dn)
            ts.xp_t.append(snap.xp)
        return ts

    def _on_entity(self, entity: Entity, op: EntityOp) -> None:
        cls = entity.get_class_name()

        if cls.startswith("CDOTA_Unit_Hero_"):
            idx = entity.get_index()
            npc = cls.replace("CDOTA_Unit_Hero_", "npc_dota_hero_").lower()
            if op.has(EntityOp.DELETED):
                self._heroes.pop(idx, None)
                self._heroes_by_npc.pop(npc, None)
            else:
                self._heroes[idx] = entity
                self._heroes_by_npc[npc] = entity
                self._maybe_sample()

        elif cls == "CDOTAPlayerController":
            pid, ok = entity.get_int32("m_nPlayerID")
            if not ok:
                pid, ok = entity.get_int32("m_iPlayerID")
            if ok and pid >= 0:
                pid //= 2
                if op.has(EntityOp.DELETED):
                    self._controllers.pop(pid, None)
                else:
                    self._controllers[pid] = entity

    def _maybe_sample(self) -> None:
        if self._parser is None:
            return
        tick = self._parser.tick
        if tick - self._last_sample < self._sample_interval:
            return
        self._last_sample = tick
        self._sample(tick)

    def _sample(self, tick: int) -> None:
        for entity in self._heroes.values():
            snap = _snapshot_hero(entity, tick)
            if snap is None:
                continue
            # Overlay gold/net_worth from the player controller if available
            ctrl = self._controllers.get(snap.player_id)
            if ctrl is not None:
                gold, ok_g = ctrl.get_int32("m_iGold")
                nw, ok_nw = ctrl.get_int32("m_iNetWorth")
                if ok_g:
                    snap.gold = gold
                if ok_nw:
                    snap.net_worth = nw
            self.snapshots.append(snap)
