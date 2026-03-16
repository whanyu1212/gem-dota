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
    from gem.entities import Entity

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_CELL_SIZE = 128  # Source 2 world units per grid cell
_HERO_CLASS_PREFIX = "CDOTA_Unit_Hero_"

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
        gold=0,  # spendable gold — set by extractor from CDOTAPlayerController
        total_earned_gold=0,  # cumulative — set by extractor from m_iTotalEarnedGold
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
        gold: Spendable gold from ``CDOTAPlayerController``, or 0 if not read.
        net_worth: Net worth from ``CDOTAPlayerController``, or 0 if not read.
        total_earned_gold: Cumulative gold earned (``m_iTotalEarnedGold``), or 0 if not read.
        total_earned_xp: Cumulative XP earned (``m_iTotalEarnedXP``), or 0 if not read.
        lh: Last-hit count.
        dn: Deny count.
        hp: Current hit points.
        max_hp: Maximum hit points.
        mana: Current mana.
        max_mana: Maximum mana.
        x: World x coordinate, or ``None`` if unavailable.
        y: World y coordinate, or ``None`` if unavailable.
        ability_levels: Ability name → level mapping for learned abilities.
        total_hero_damage: Cumulative hero-vs-hero damage dealt (from combat log).
        total_hero_healing: Cumulative healing dealt to allied heroes (from combat log).
        total_deaths: Cumulative death count (all causes, from combat log).
        total_stuns: Cumulative stun duration dealt in seconds (from combat log).
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
    ability_levels: dict[str, int] = field(default_factory=dict)
    total_hero_damage: int = 0
    total_hero_healing: int = 0
    total_deaths: int = 0
    total_stuns: float = 0.0


@dataclass
class PlayerTimeSeries:
    """Time-series data for one player, aggregated from snapshots.

    Attributes:
        player_id: Player slot (0-9).
        ticks: Tick values for each sample.
        gold_t: Spendable gold at each sample tick.
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
