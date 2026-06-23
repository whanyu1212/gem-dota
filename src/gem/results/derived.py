"""Derive OpenDota-shaped per-player kill aggregates from existing logs.

These helpers turn a player's already-extracted ``kills_log`` (a list of
:class:`~gem.combat.log.CombatLogEntry`) into the per-unit ``killed`` count map
and the specialty kill scalars OpenDota exposes per player. They add no new
parsing — the underlying DEATH events are produced by the combat-log aggregator
(which credits summon kills to the owning hero); this module only reshapes them.

Reference: refs/parser/src/main/java/opendota/CreateParsedDataBlob.java and
odota/core per-player kill categorization.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import TYPE_CHECKING

from gem.catalog import units

if TYPE_CHECKING:
    from gem.combat.log import CombatLogEntry


def killed_counts(kills_log: list[CombatLogEntry]) -> dict[str, int]:
    """Count kills per target unit name, matching OpenDota's ``killed`` map.

    Reincarnation/aegis *trigger* deaths (``will_reincarnate``) are skipped — the
    combat log fires two DEATH events for such a death and only the second is the
    true kill, matching how teamfight attribution and OpenDota count them.

    Args:
        kills_log: The player's DEATH entries where they were the attacker
            (summon kills already credited to the owner).

    Returns:
        Target NPC name -> kill count.
    """
    counts: Counter[str] = Counter()
    for entry in kills_log:
        if entry.target_name and not entry.will_reincarnate:
            counts[entry.target_name] += 1
    return dict(counts)


@dataclass
class KillCategories:
    """Specialty kill scalars derived from a player's killed map.

    Mirrors OpenDota's per-player ``*_kills`` counters. ``lane_kills`` counts all
    lane-creep kills over the whole game (not just the laning phase); this matches
    odota/core's lane-creep total rather than its laning-window metric.

    Attributes:
        ancient_kills: Ancient-neutral creeps killed.
        neutral_kills: All neutral creeps killed (includes ancients).
        lane_kills: Lane creeps killed.
        courier_kills: Couriers killed.
        observer_kills: Observer wards killed.
        sentry_kills: Sentry wards killed.
        roshan_kills: Roshans killed.
    """

    ancient_kills: int = 0
    neutral_kills: int = 0
    lane_kills: int = 0
    courier_kills: int = 0
    observer_kills: int = 0
    sentry_kills: int = 0
    roshan_kills: int = 0


def categorize_kills(killed: dict[str, int]) -> KillCategories:
    """Categorize a ``killed`` map into specialty kill scalars.

    Args:
        killed: Target NPC name -> kill count (from :func:`killed_counts`).

    Returns:
        A :class:`KillCategories` with summed counts per category.
    """
    cat = KillCategories()
    for name, count in killed.items():
        if units.is_neutral(name):
            cat.neutral_kills += count
            if units.is_ancient(name):
                cat.ancient_kills += count
        elif units.is_lane_creep(name):
            cat.lane_kills += count
        elif units.is_courier(name):
            cat.courier_kills += count
        elif units.is_observer_ward(name):
            cat.observer_kills += count
        elif units.is_sentry_ward(name):
            cat.sentry_kills += count
        elif units.is_roshan(name):
            cat.roshan_kills += count
    return cat


# ---------------------------------------------------------------------------
# Building-status bitmasks (Steam GC convention)
# ---------------------------------------------------------------------------

# Lane bit offsets within each building bitmask.
_TOWER_LANE_OFFSET = {"top": 0, "mid": 3, "bot": 6}
_RAX_LANE_OFFSET = {"top": 0, "mid": 2, "bot": 4}
# All 11 tower bits set (3 tiers × 3 lanes + 2 tier-4) / all 6 barracks bits set.
_ALL_TOWERS_STANDING = (1 << 11) - 1
_ALL_RAX_STANDING = (1 << 6) - 1


# Bit indices of the two tier-4 (ancient) towers, cleared in occurrence order
# because both share the NPC name ``..._tower4`` (no lane suffix).
_TIER4_BITS = (9, 10)


def _tower_bit(tower_name: str) -> int | None:
    """Return the Steam-GC tower-status bit index for a TIER 1-3 tower NPC name.

    Layout (bit set = standing): per lane, tier1/2/3 occupy ``lane_offset+0/1/2``
    with lane offsets top=0, mid=3, bot=6. Tier-4 (ancient) towers share the name
    ``..._tower4`` and are handled separately (bits 9, 10). Reference: Steam Web
    API ``tower_status_<team>``.

    Args:
        tower_name: e.g. ``npc_dota_goodguys_tower2_mid``.

    Returns:
        Bit index 0-8, or ``None`` if not a recognized tier 1-3 tower.
    """
    for lane, offset in _TOWER_LANE_OFFSET.items():
        if tower_name.endswith(f"_{lane}"):
            for tier in (1, 2, 3):
                if f"_tower{tier}_" in tower_name:
                    return offset + (tier - 1)
    return None


def _rax_bit(rax_name: str) -> int | None:
    """Return the Steam-GC barracks-status bit index for a barracks NPC name.

    Layout (bit set = standing): per lane, melee then ranged at ``lane_offset+0/1``
    with lane offsets top=0, mid=2, bot=4. Reference: Steam Web API
    ``barracks_status_<team>``.

    Args:
        rax_name: e.g. ``npc_dota_badguys_melee_rax_mid``.

    Returns:
        Bit index 0-5, or ``None`` if the name is not a recognized barracks.
    """
    for lane, offset in _RAX_LANE_OFFSET.items():
        if rax_name.endswith(f"_rax_{lane}"):
            if "_melee_rax" in rax_name:
                return offset
            if "_range_rax" in rax_name:
                return offset + 1
    return None


def _tower_mask(tower_names: list[str]) -> int:
    """Return a tower-status mask (set=standing) after the given tower deaths.

    Tier 1-3 towers map to a fixed bit; the two tier-4 towers share the NPC name
    ``..._tower4``, so the first such death clears bit 9 and the second clears
    bit 10 (occurrence order).
    """
    mask = _ALL_TOWERS_STANDING
    tier4_seen = 0
    for name in tower_names:
        if "_tower4" in name:
            if tier4_seen < len(_TIER4_BITS):
                mask &= ~(1 << _TIER4_BITS[tier4_seen])
                tier4_seen += 1
            continue
        bit = _tower_bit(name)
        if bit is not None:
            mask &= ~(1 << bit)
    return mask


def _rax_mask(rax_names: list[str]) -> int:
    """Return a barracks-status mask (set=standing) after the given rax deaths."""
    mask = _ALL_RAX_STANDING
    for name in rax_names:
        bit = _rax_bit(name)
        if bit is not None:
            mask &= ~(1 << bit)
    return mask


def building_status(tower_kills: list, barracks_kills: list) -> dict[str, int]:
    """Reconstruct OpenDota building-status bitmasks from destruction events.

    Buildings start all-standing; each destroyed building clears its bit. The
    result is the end-of-game mask per team, matching Steam GC /
    OpenDota's ``tower_status_<team>`` / ``barracks_status_<team>``.

    Args:
        tower_kills: ``TowerKill`` events (each with ``.team`` and ``.tower_name``).
        barracks_kills: ``BarracksKill`` events (``.team`` and ``.barracks_name``).

    Returns:
        ``{tower_status_radiant, tower_status_dire, barracks_status_radiant,
        barracks_status_dire}`` as ints. Team 2 = Radiant, 3 = Dire.
    """
    rad_towers = [k.tower_name for k in tower_kills if k.team == 2]
    dire_towers = [k.tower_name for k in tower_kills if k.team == 3]
    rad_rax = [k.barracks_name for k in barracks_kills if k.team == 2]
    dire_rax = [k.barracks_name for k in barracks_kills if k.team == 3]
    return {
        "tower_status_radiant": _tower_mask(rad_towers),
        "tower_status_dire": _tower_mask(dire_towers),
        "barracks_status_radiant": _rax_mask(rad_rax),
        "barracks_status_dire": _rax_mask(dire_rax),
    }
