"""Player state snapshot and time-series dataclasses for the player extractor.

Contains the data models and helper functions for sampling hero entity state.
These are implementation details of the ``extractors`` package; consumers should
import ``PlayerStateSnapshot`` and ``PlayerTimeSeries`` from
``gem.extractors.players`` or ``gem.extractors``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gem.state.entities import Entity

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_CELL_SIZE = 128  # Source 2 world units per grid cell
_HERO_CLASS_PREFIX = "CDOTA_Unit_Hero_"

# Dota team ids on ``CDOTA_PlayerResource.m_vecPlayerData.*.m_iPlayerTeam``.
# Spectators/coaches use other ids (1/14) and are skipped by the scan.
TEAM_RADIANT = 2
TEAM_DIRE = 3
# CDOTA_PlayerResource rows to scan when building the logical→resource remap.
# A coach occupies a row, so the 10 players can span more than 10 indices.
PLAYER_RESOURCE_SCAN_LIMIT = 30

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


def _player_id_from_entity(entity: Entity | None, *, allow_owner: bool = False) -> int | None:
    """Resolve a hero/controller/owned-unit entity to a player slot (0-9).

    Reads ``m_nPlayerID`` then ``m_iPlayerID`` and halves the raw value (the
    replay stores ``slot * 2``). When ``allow_owner`` is set, also falls back to
    ``m_iPlayerOwnerID`` — needed when the entity is an *owned unit* (e.g. a
    ward's owner unit) whose slot lives on the owning-player field.

    ``allow_owner`` must stay ``False`` for hero-name lookups: a hero-class
    illusion (Manta / Dark Seer wall / Shadow Demon disruption) shares the real
    hero's class and may carry only ``m_iPlayerOwnerID``; resolving it via the
    owner field would misattribute the real hero's stats/position to the
    illusion owner. Hero entities always carry ``m_nPlayerID``/``m_iPlayerID``,
    so they never need the owner fallback.

    Mirrors ``getPlayerSlotFromEntity`` in
    ``refs/parser/src/main/java/opendota/Parse.java``.

    Args:
        entity: The entity to read from, or ``None``.
        allow_owner: Include the ``m_iPlayerOwnerID`` fallback (owned-unit
            contexts only).

    Returns:
        Player slot 0-9, or ``None`` if unresolvable.
    """
    if entity is None:
        return None
    fields = (
        ("m_nPlayerID", "m_iPlayerID", "m_iPlayerOwnerID")
        if allow_owner
        else (
            "m_nPlayerID",
            "m_iPlayerID",
        )
    )
    for field_name in fields:
        val = entity.get_int32(field_name)
        if val is not None and val >= 0:
            return val // 2
    return None


@dataclass(frozen=True)
class PlayerResourceScan:
    """Logical-slot mappings derived from one ``CDOTA_PlayerResource`` scan.

    OpenDota scans PlayerResource for rows whose team is Radiant or Dire (a coach
    has team 1/14 and is skipped), then uses the scan order as the logical player
    slot ``0..9``. The resource-array index is not always the logical slot, so the
    indirection is kept explicit. ``resolved`` is ``True`` only when all 10 players
    were found, letting callers decide whether to adopt a partial early-game scan.

    Attributes:
        index_by_id: Logical slot ``0..9`` → ``m_vecPlayerData`` array index.
        team_by_id: Logical slot → team id (``TEAM_RADIANT``/``TEAM_DIRE``).
        team_slot_by_id: Logical slot → ``m_iTeamSlot`` (the ``m_vecDataTeam`` index).
        resolved: ``True`` iff all 10 player slots were resolved.
    """

    index_by_id: dict[int, int]
    team_by_id: dict[int, int]
    team_slot_by_id: dict[int, int]
    resolved: bool


def scan_player_resource(player_resource: Entity) -> PlayerResourceScan:
    """Scan ``CDOTA_PlayerResource`` for the logical player→resource mappings.

    Walks the first ``PLAYER_RESOURCE_SCAN_LIMIT`` rows, skipping any whose team is
    not Radiant/Dire or whose team slot is missing/negative (coaches, empty rows),
    and assigns the surviving rows logical slots ``0..9`` in scan order.

    Reference: refs/parser/src/main/java/opendota/Parse.java (validIndices).

    Args:
        player_resource: The live ``CDOTA_PlayerResource`` entity.

    Returns:
        A :class:`PlayerResourceScan` with the three slot maps and a ``resolved``
        flag (``True`` once all 10 players are mapped).
    """
    index_by_id: dict[int, int] = {}
    team_by_id: dict[int, int] = {}
    team_slot_by_id: dict[int, int] = {}

    for resource_idx in range(PLAYER_RESOURCE_SCAN_LIMIT):
        team = player_resource.get_int32(f"m_vecPlayerData.{resource_idx:04d}.m_iPlayerTeam")
        team_slot = player_resource.get_int32(f"m_vecPlayerTeamData.{resource_idx:04d}.m_iTeamSlot")
        if team not in (TEAM_RADIANT, TEAM_DIRE) or team_slot is None or team_slot < 0:
            continue
        player_id = len(index_by_id)
        if player_id >= 10:
            break
        index_by_id[player_id] = resource_idx
        team_by_id[player_id] = team
        team_slot_by_id[player_id] = team_slot

    return PlayerResourceScan(
        index_by_id=index_by_id,
        team_by_id=team_by_id,
        team_slot_by_id=team_slot_by_id,
        resolved=len(index_by_id) == 10,
    )


def team_data_prefix(team_slot: int) -> str:
    """Build the ``m_vecDataTeam`` entry prefix for a team slot.

    The ``CDOTA_DataRadiant``/``CDOTA_DataDire`` entities expose per-player data
    under ``m_vecDataTeam.{slot:04d}.*``. Callers that read several fields off the
    same slot keep this prefix and append field names; callers reading a single
    field can use :func:`team_data_field` instead.

    Args:
        team_slot: The ``m_iTeamSlot`` index into ``m_vecDataTeam``.

    Returns:
        The entry prefix, e.g. ``"m_vecDataTeam.0003"``.
    """
    return f"m_vecDataTeam.{team_slot:04d}"


def team_data_field(team_slot: int, field_name: str) -> str:
    """Build a ``m_vecDataTeam`` field path for a team slot.

    The ``CDOTA_DataRadiant``/``CDOTA_DataDire`` entities expose per-player
    counters (``m_iTotalEarnedGold``, ``m_iTotalEarnedXP``, ``m_iLastHitCount``,
    ``m_iDenyCount``, ``m_iNetWorth``) under ``m_vecDataTeam.{slot}``.

    Args:
        team_slot: The ``m_iTeamSlot`` index into ``m_vecDataTeam``.
        field_name: The counter field, e.g. ``"m_iTotalEarnedGold"``.

    Returns:
        The dotted field path, e.g. ``"m_vecDataTeam.0003.m_iTotalEarnedGold"``.
    """
    return f"{team_data_prefix(team_slot)}.{field_name}"


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
    player_id = entity.get_int32("m_nPlayerID")
    if player_id is None:
        player_id = entity.get_int32("m_iPlayerID")
    if player_id is None or player_id < 0:
        return None
    player_id //= 2

    team = entity.get_int32("m_iTeamNum") or 0
    level = entity.get_int32("m_nCurrentLevel") or 0
    xp = entity.get_int32("m_iCurrentXP") or 0
    hp = entity.get_int32("m_iHealth") or 0
    max_hp = entity.get_int32("m_iMaxHealth") or 0
    mana = entity.get_float32("m_flMana") or 0.0
    max_mana = entity.get_float32("m_flMaxMana") or 0.0
    lh = entity.get_int32("m_iLastHitCount") or 0
    dn = entity.get_int32("m_iDenies") or 0
    # m_lifeState: 0 = alive, 1 = dying, 2 = dead. OpenDota's life_state_dead
    # counts time spent in the non-alive states; we treat any non-zero value as
    # dead for the per-snapshot sample. Defaults to 0 (alive) when absent.
    life_state = entity.get_int32("m_lifeState") or 0

    pos = _pos(entity)

    # Convert entity class name to the canonical NPC name (camelCase → snake_case).
    # "CDOTA_Unit_Hero_TemplarAssassin" → "npc_dota_hero_templar_assassin"
    # "CDOTA_Unit_Hero_Nyx_Assassin"   → "npc_dota_hero_nyx_assassin" (already underscored)
    # This matches dotaconstants keys and the combat log string table.
    # Reference: refs/parser/Parse.java combatLogName2
    _ending = entity.get_class_name()[len(_HERO_CLASS_PREFIX) :].replace("_", "")
    _npc_name = "npc_dota_hero" + re.sub(r"([A-Z])", r"_\1", _ending).lower()
    return PlayerStateSnapshot(
        tick=tick,
        player_id=player_id,
        npc_name=_npc_name,
        team=team,
        level=level,
        xp=xp,
        gold=0,  # current unspent gold — set by extractor from CDOTAPlayerController
        total_earned_gold=0,  # cumulative — set by extractor from m_iTotalEarnedGold
        net_worth=0,
        lh=lh,
        dn=dn,
        hp=hp,
        max_hp=max_hp,
        mana=mana,
        max_mana=max_mana,
        life_state=life_state,
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
        game_time_s: OpenDota-style game-relative sample time in seconds, or
            ``None`` when the parser has not observed the game clock yet.
        player_id: Player slot (0-9).
        npc_name: Hero NPC name, e.g. ``"npc_dota_hero_axe"``.
        team: Team number (2=Radiant, 3=Dire).
        level: Hero level (1-30).
        xp: Current XP toward the next level (``m_iCurrentXP``); resets to 0 on
            each level-up. For cumulative XP use ``total_earned_xp``.
        gold: Current unspent gold from ``CDOTAPlayerController``, or 0 if not read.
        net_worth: Net worth from ``CDOTAPlayerController``, or 0 if not read.
        total_earned_gold: Cumulative gold earned (``m_iTotalEarnedGold``), or 0 if not read.
        total_earned_xp: Cumulative XP earned (``m_iTotalEarnedXP``), or 0 if not read.
        lh: Last-hit count.
        dn: Deny count.
        hp: Current hit points.
        max_hp: Maximum hit points.
        mana: Current mana.
        max_mana: Maximum mana.
        life_state: Hero life state (``m_lifeState``): 0 = alive, 1 = dying,
            2 = dead. Used to derive OpenDota's ``life_state_dead``.
        x: World x coordinate, or ``None`` if unavailable.
        y: World y coordinate, or ``None`` if unavailable.
        ability_levels: Ability name → level mapping for learned abilities.
        total_hero_damage: Cumulative hero-vs-hero damage dealt (from combat log).
        total_hero_healing: Cumulative healing dealt to allied heroes (from combat log).
        total_deaths: Cumulative death count (all causes, from combat log).
        total_stuns: Cumulative stun duration dealt in seconds (from combat log).
        items: Item names by slot index for occupied slots (0-5 main inventory,
            6-8 backpack, 9-16 stash). Populated only on the dense series, not
            minute snapshots; the last dense sample gives end-of-game inventory.
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
    total_earned_gold: int = 0
    total_earned_xp: int = 0
    game_time_s: int | None = None
    life_state: int = 0
    ability_levels: dict[str, int] = field(default_factory=dict)
    total_hero_damage: int = 0
    total_hero_healing: int = 0
    total_deaths: int = 0
    total_stuns: float = 0.0
    items: dict[int, str] = field(default_factory=dict)


@dataclass
class PlayerTimeSeries:
    """Time-series data for one player, aggregated from snapshots.

    Attributes:
        player_id: Player slot (0-9).
        ticks: Tick values for each sample.
        game_times_s: Game-relative seconds for each minute sample, using exact
            non-negative 60-second boundaries. Populated by
            ``PlayerExtractor.minute_time_series``; empty for the dense series.
        gold_t: Current unspent gold at each sample tick.
        total_earned_gold_t: Cumulative total earned gold at each sample tick.
        total_earned_xp_t: Cumulative total earned XP at each sample tick.
        net_worth_t: Net worth at each sample tick.
        lh_t: Last-hit count at each sample tick.
        dn_t: Deny count at each sample tick.
        xp_t: Cumulative XP at each sample tick.
        hp_t: Current hit points at each sample tick.
        mana_t: Current mana at each sample tick.
        x_t: World x coordinate at each sample tick (``None`` if unavailable).
        y_t: World y coordinate at each sample tick (``None`` if unavailable).
        total_hero_damage_t: Cumulative hero-vs-hero damage dealt at each sample tick.
        total_hero_healing_t: Cumulative healing dealt to allied heroes at each sample tick.
        total_deaths_t: Cumulative death count at each sample tick.
        total_stuns_t: Cumulative stun duration dealt (seconds) at each sample tick.
    """

    player_id: int
    ticks: list[int] = field(default_factory=list)
    gold_t: list[int] = field(default_factory=list)
    total_earned_gold_t: list[int] = field(default_factory=list)
    total_earned_xp_t: list[int] = field(default_factory=list)
    net_worth_t: list[int] = field(default_factory=list)
    lh_t: list[int] = field(default_factory=list)
    dn_t: list[int] = field(default_factory=list)
    xp_t: list[int] = field(default_factory=list)
    hp_t: list[int] = field(default_factory=list)
    mana_t: list[float] = field(default_factory=list)
    x_t: list[float | None] = field(default_factory=list)
    y_t: list[float | None] = field(default_factory=list)
    total_hero_damage_t: list[int] = field(default_factory=list)
    total_hero_healing_t: list[int] = field(default_factory=list)
    total_deaths_t: list[int] = field(default_factory=list)
    total_stuns_t: list[float] = field(default_factory=list)
    # Append-only: this internal dataclass is also constructed in downstream
    # integrations, so keep new defaulted fields at the end.
    game_times_s: list[int] = field(default_factory=list)
