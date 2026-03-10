"""Per-tick player statistics extractor for Dota 2 replays.

Polls hero entity state at configurable tick intervals and accumulates
snapshots for time-series analysis.

Reference: examples/extraction_demo.py, refs/parser/src/main/java/opendota/Parse.java
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from gem.entities import Entity, EntityOp

if TYPE_CHECKING:
    from gem.parser import ReplayParser

# ---------------------------------------------------------------------------
# Inventory constants
# ---------------------------------------------------------------------------

# Slots 0-5 = main inventory, 6-8 = backpack, 9-16 = stash
# Reference: refs/parser/src/main/java/opendota/Parse.java getHeroItem() comment
_ITEM_SLOTS = 17  # total slots to scan (0-16)
_ABILITY_SLOTS = 32  # m_hAbilities.0000-0031 per hero entity
_NULL_HANDLE = 0xFFFFFF  # empty slot sentinel

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

    # Convert entity class name to the canonical NPC name (camelCase → snake_case).
    # "CDOTA_Unit_Hero_TemplarAssassin" → "npc_dota_hero_templar_assassin"
    # "CDOTA_Unit_Hero_Nyx_Assassin"   → "npc_dota_hero_nyx_assassin" (already underscored)
    # This matches dotaconstants keys and the combat log string table.
    # Reference: refs/parser/Parse.java combatLogName2
    _ending = entity.get_class_name()[len("CDOTA_Unit_Hero_") :].replace("_", "")
    _npc_name = "npc_dota_hero" + re.sub(r"([A-Z])", r"_\1", _ending).lower()
    return PlayerStateSnapshot(
        tick=tick,
        player_id=player_id,
        npc_name=_npc_name,
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
        ability_levels: Ability name → level mapping for learned abilities.
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
    ability_levels: dict[str, int] = field(default_factory=dict)


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
        hp_t: Current hit points at each sample tick.
        mana_t: Current mana at each sample tick.
        x_t: World x coordinate at each sample tick (``None`` if unavailable).
        y_t: World y coordinate at each sample tick (``None`` if unavailable).
    """

    player_id: int
    ticks: list[int] = field(default_factory=list)
    gold_t: list[int] = field(default_factory=list)
    net_worth_t: list[int] = field(default_factory=list)
    lh_t: list[int] = field(default_factory=list)
    dn_t: list[int] = field(default_factory=list)
    xp_t: list[int] = field(default_factory=list)
    hp_t: list[int] = field(default_factory=list)
    mana_t: list[float] = field(default_factory=list)
    x_t: list[float | None] = field(default_factory=list)
    y_t: list[float | None] = field(default_factory=list)


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
        # CDOTADataRadiant / CDOTADataDire entities (authoritative gold/LH/DN per team)
        self._data_radiant: Entity | None = None
        self._data_dire: Entity | None = None
        # player_id (0-9) → team slot (0-4) within CDOTADataRadiant/Dire
        # Read from CDOTA_PlayerResource.m_vecPlayerTeamData.%04d.m_iTeamSlot
        self._player_team_slot: dict[int, int] = {}
        # CDOTA_PlayerResource entity for slot lookups
        self._player_resource: Entity | None = None
        self.snapshots = []
        # set of player_ids whose starting inventory has been emitted
        self._inventory_initialized: set[int] = set()
        # player_id → tick of first inventory snapshot (used to suppress
        # duplicate combat log PURCHASE events for the same window)
        self.first_snapshot_tick: dict[int, int] = {}

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
            ts.hp_t.append(snap.hp)
            ts.mana_t.append(snap.mana)
            ts.x_t.append(snap.x)
            ts.y_t.append(snap.y)
        return ts

    def _on_entity(self, entity: Entity, op: EntityOp) -> None:
        cls = entity.get_class_name()

        if cls.startswith("CDOTA_Unit_Hero_"):
            idx = entity.get_index()
            ending = cls[len("CDOTA_Unit_Hero_") :]
            # Register two name forms to cover inconsistent combat log names.
            # "combatLogName":  simple lowercase ("npc_dota_hero_templarassassin")
            # "combatLogName2": insert _ before each capital ("npc_dota_hero_templar_assassin")
            # Reference: refs/parser/src/main/java/opendota/Parse.java
            npc1 = "npc_dota_hero_" + ending.lower()
            npc2 = "npc_dota_hero" + re.sub(r"([A-Z])", r"_\1", ending.replace("_", "")).lower()
            if op.has(EntityOp.DELETED):
                self._heroes.pop(idx, None)
                self._heroes_by_npc.pop(npc1, None)
                self._heroes_by_npc.pop(npc2, None)
            else:
                self._heroes[idx] = entity
                self._heroes_by_npc[npc1] = entity
                self._heroes_by_npc[npc2] = entity
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

        elif cls in ("CDOTADataRadiant", "CDOTA_DataRadiant"):
            self._data_radiant = None if op.has(EntityOp.DELETED) else entity

        elif cls in ("CDOTADataDire", "CDOTA_DataDire"):
            self._data_dire = None if op.has(EntityOp.DELETED) else entity

        elif cls == "CDOTA_PlayerResource":
            if op.has(EntityOp.DELETED):
                self._player_resource = None
            else:
                self._player_resource = entity
                self._refresh_team_slots()

    def _refresh_team_slots(self) -> None:
        """Read m_iTeamSlot for each player from CDOTA_PlayerResource."""
        pr = self._player_resource
        if pr is None:
            return
        for i in range(10):
            slot, ok = pr.get_int32(f"m_vecPlayerTeamData.{i:04d}.m_iTeamSlot")
            if ok and slot >= 0:
                self._player_team_slot[i] = slot

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
            # Overlay authoritative net worth + gold from CDOTADataRadiant/Dire.
            # The field index is the team slot (0-4), read from CDOTA_PlayerResource.
            # Reference: refs/parser/Parse.java getEntityProperty(dataTeam, "m_vecDataTeam.%i.*", teamSlot)
            data_entity = self._data_radiant if snap.team == _TEAM_RADIANT else self._data_dire
            if data_entity is not None:
                # Prefer authoritative team slot; fall back to pid % 5
                team_slot = self._player_team_slot.get(snap.player_id, snap.player_id % 5)
                prefix = f"m_vecDataTeam.{team_slot:04d}"
                nw, ok_nw = data_entity.get_int32(f"{prefix}.m_iNetWorth")
                if ok_nw and nw > 0:
                    snap.net_worth = nw
                if snap.gold == 0:
                    teg, ok_teg = data_entity.get_int32(f"{prefix}.m_iTotalEarnedGold")
                    if ok_teg and teg > 0:
                        snap.gold = teg
                lh, ok_lh = data_entity.get_int32(f"{prefix}.m_iLastHitCount")
                if ok_lh and lh > 0:
                    snap.lh = lh
                dn, ok_dn = data_entity.get_int32(f"{prefix}.m_iDenyCount")
                if ok_dn and dn > 0:
                    snap.dn = dn
            snap.ability_levels = self._read_abilities(entity)
            self.snapshots.append(snap)
            self._diff_inventory(entity, snap.player_id, snap.npc_name, tick)

    def _read_abilities(self, hero: Entity) -> dict[str, int]:
        """Read current ability names and levels from a hero entity.

        Iterates ``m_hAbilities.0000``–``m_hAbilities.0031``, falling back to
        ``m_vecAbilities.*`` for older replays. Resolves each handle to an
        ability entity and reads ``m_iLevel`` and the name from the
        ``EntityNames`` string table.

        Args:
            hero: The hero entity to read from.

        Returns:
            Mapping of ability name → level for all abilities with level > 0.
        """
        if self._parser is None:
            return {}
        em = self._parser.entity_manager
        if em is None:
            return {}
        entity_names = self._parser.string_tables.get_by_name("EntityNames")
        if entity_names is None:
            return {}

        result: dict[str, int] = {}
        for slot in range(_ABILITY_SLOTS):
            handle, ok = hero.get_uint32(f"m_hAbilities.{slot:04d}")
            if not ok:
                handle, ok = hero.get_uint32(f"m_vecAbilities.{slot:04d}")
            if not ok or handle == _NULL_HANDLE:
                continue
            ability_entity = em.find_by_handle(handle)
            if ability_entity is None:
                continue
            name_idx, ok2 = ability_entity.get_int32("m_pEntity.m_nameStringableIndex")
            if not ok2 or name_idx < 0:
                continue
            item = entity_names.items.get(name_idx)
            if item is None:
                continue
            name = item[0] if isinstance(item, tuple) else str(item)
            if not name:
                continue
            level, _ = ability_entity.get_int32("m_iLevel")
            if level > 0:
                result[name] = level
        return result

    def _read_inventory(self, hero: Entity) -> dict[int, str]:
        """Read current item names from a hero entity's item slots.

        Reads ``m_hItems.0000``–``m_hItems.{_ITEM_SLOTS-1:04d}``, resolving each
        handle via the entity manager and looking up the item name from the
        ``EntityNames`` string table.

        Args:
            hero: The hero entity to read from.

        Returns:
            Mapping of slot index → item name for all occupied slots.
        """
        if self._parser is None:
            return {}
        em = self._parser.entity_manager
        if em is None:
            return {}
        entity_names = self._parser.string_tables.get_by_name("EntityNames")
        if entity_names is None:
            return {}

        result: dict[int, str] = {}
        for slot in range(_ITEM_SLOTS):
            handle, ok = hero.get_uint32(f"m_hItems.{slot:04d}")
            if not ok or handle == _NULL_HANDLE:
                continue
            item_entity = em.find_by_handle(handle)
            if item_entity is None:
                continue
            name_idx, ok2 = item_entity.get_int32("m_pEntity.m_nameStringableIndex")
            if not ok2 or name_idx < 0:
                continue
            # EntityNames items are stored as (key_str, value_bytes); key_str is the name
            item = entity_names.items.get(name_idx)
            if item is None:
                continue
            name = item[0] if isinstance(item, tuple) else str(item)
            if name:
                result[slot] = name
        return result

    def _diff_inventory(self, hero: Entity, player_id: int, npc_name: str, tick: int) -> None:
        """Emit synthetic PURCHASE entries for a player's starting inventory.

        Called on the first snapshot per player. Reads all occupied item slots
        and emits a ``PURCHASE`` ``CombatLogEntry`` for each, filling the gap
        before the combat log stream begins recording.

        Args:
            hero: The hero entity.
            player_id: Player slot (0-9).
            npc_name: Hero NPC name for the combat log entry.
            tick: Current game tick.
        """
        if self._parser is None or player_id in self._inventory_initialized:
            return
        current = self._read_inventory(hero)

        from gem.combatlog import CombatLogEntry

        if player_id not in self._inventory_initialized:
            # First snapshot — emit all current items as starting inventory.
            # Subsequent purchases are covered by DOTA_COMBATLOG_PURCHASE events.
            # Reference: refs/parser/Parse.java isPlayerStartingItemsWritten pattern
            self._inventory_initialized.add(player_id)
            self.first_snapshot_tick[player_id] = tick
            for item_name in current.values():
                if item_name and not item_name.startswith("item_recipe"):
                    entry = CombatLogEntry(
                        tick=tick,
                        log_type="PURCHASE",
                        target_name=npc_name,
                        value_name=item_name,
                    )
                    self._parser.combat_log._emit(entry)
