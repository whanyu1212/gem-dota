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
