"""Teamfight detection from combat log entries.

Detects teamfights by merging hero death events within a rolling cooldown
window, then aggregates per-player stats (damage dealt/taken, healing,
gold delta, XP delta, deaths, buybacks, ability/item uses) for each fight.

Algorithm mirrors the reference implementation:
  - A new fight opens on any non-illusion hero death.
  - ``start_tick = first_death_tick - cooldown``
  - The fight closes once ``cooldown`` ticks elapse with no new hero death,
    setting ``end_tick = last_death_tick + cooldown``.
  - Per-player stats are collected from combat log entries whose tick falls
    within ``[start_tick, end_tick]``.
  - XP delta is derived from the nearest player snapshots bracketing the window.

No minimum-death filter is applied — all detected fights are returned so that
callers can threshold on ``Teamfight.deaths`` or participation count.

Reference: refs/parser/src/main/java/opendota/CreateParsedDataBlob.java
           processTeamfights() lines 1224–1353
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from gem.combatlog import CombatLogEntry

if TYPE_CHECKING:
    from gem.extractors.players import PlayerStateSnapshot

# 15 seconds × 30 ticks/second  (reference uses 15s cooldown)
_COOLDOWN_TICKS: int = 15 * 30

# Maximum distance (world units) between a new death and the current fight's
# centroid before treating it as a separate fight.  Top-to-bottom lane is
# ~8 000 units; a threshold of 3 000 cleanly separates simultaneous skirmishes
# on different parts of the map while keeping deaths within the same fight grouped.
_SPATIAL_THRESHOLD: float = 3000.0


@dataclass
class TeamfightPlayer:
    """Per-player stats accumulated within one teamfight window.

    Attributes:
        player_id: Player slot (0–9).
        deaths: Hero deaths within the window.
        buybacks: Buybacks within the window.
        damage_dealt: Damage dealt to enemy heroes (non-illusion).
        damage_taken: Damage received from any source within the window.
        healing: Healing dealt to allied heroes.
        gold_delta: Gold earned within the window.
        xp_delta: XP earned within the window (from snapshot diff).
        ability_uses: Ability name → use count.
        item_uses: Item name → use count.
    """

    player_id: int
    deaths: int = 0
    buybacks: int = 0
    damage_dealt: int = 0
    damage_taken: int = 0
    healing: int = 0
    gold_delta: int = 0
    xp_delta: int = 0
    ability_uses: dict[str, int] = field(default_factory=dict)
    item_uses: dict[str, int] = field(default_factory=dict)


@dataclass
class Teamfight:
    """A detected teamfight window with per-player breakdowns.

    Attributes:
        start_tick: Window open tick (first_death_tick − cooldown).
        end_tick: Window close tick (last_death_tick + cooldown).
        last_death_tick: Tick of the final hero death in the fight.
        deaths: Total hero deaths within the window.
        players: One ``TeamfightPlayer`` per slot (indices 0–9).
    """

    start_tick: int
    end_tick: int
    last_death_tick: int
    deaths: int
    players: list[TeamfightPlayer] = field(default_factory=list)


def _hero_pos_at_tick(
    hero_name: str,
    tick: int,
    hero_to_slot: dict[str, int],
    player_snapshots: dict[int, list[PlayerStateSnapshot]],
) -> tuple[float, float] | None:
    """Return the (x, y) world position of a hero nearest to ``tick``, or None."""
    slot = hero_to_slot.get(hero_name)
    if slot is None:
        return None
    snaps = player_snapshots.get(slot)
    if not snaps:
        return None
    nearest = min(snaps, key=lambda s: abs(s.tick - tick))
    if nearest.x is None or nearest.y is None:
        return None
    return (float(nearest.x), float(nearest.y))


def detect_teamfights(
    combat_log: list[CombatLogEntry],
    hero_to_slot: dict[str, int] | None = None,
    player_snapshots: dict[int, list[PlayerStateSnapshot]] | None = None,
) -> list[Teamfight]:
    """Detect teamfights from a match combat log.

    Uses a temporal rolling window (hero deaths within ``_COOLDOWN_TICKS``) and
    a spatial check: if a death occurs within the cooldown but the dying hero's
    position is more than ``_SPATIAL_THRESHOLD`` world units from the current
    fight's death centroid, it is treated as a new separate fight.

    Args:
        combat_log: All ``CombatLogEntry`` objects from ``ParsedMatch.combat_log``.
        hero_to_slot: Mapping of NPC hero name → player slot (0–9).  Built from
            ``{pp.hero_name: pp.player_id for pp in match.players}``.  Used to
            attribute damage/healing/ability events to the correct player slot.
        player_snapshots: Optional mapping of ``player_id → list[PlayerStateSnapshot]``
            used to compute XP deltas and death positions for spatial splitting.

    Returns:
        List of ``Teamfight`` objects in chronological order.  No minimum-death
        filter is applied; callers may filter on ``Teamfight.deaths`` or
        participation count.
    """
    h2s: dict[str, int] = hero_to_slot or {}
    snaps: dict[int, list[PlayerStateSnapshot]] = player_snapshots or {}
    entries = sorted(combat_log, key=lambda e: e.tick)

    # --- Pass 1: detect fight windows from hero deaths ----------------------
    fights: list[Teamfight] = []
    current: Teamfight | None = None
    # Track centroid of death positions for the current fight (for spatial split).
    centroid_sum: list[float] = [0.0, 0.0]
    centroid_count: int = 0

    for entry in entries:
        if entry.log_type != "DEATH":
            continue
        if not entry.target_is_hero or entry.target_is_illusion:
            continue

        death_pos = _hero_pos_at_tick(entry.target_name, entry.tick, h2s, snaps)

        # Determine if this death should extend current fight or start a new one.
        temporal_gap = (
            current is not None and entry.tick - current.last_death_tick >= _COOLDOWN_TICKS
        )
        spatial_split = False
        if (
            current is not None
            and not temporal_gap
            and death_pos is not None
            and centroid_count > 0
        ):
            cx = centroid_sum[0] / centroid_count
            cy = centroid_sum[1] / centroid_count
            dist = math.hypot(death_pos[0] - cx, death_pos[1] - cy)
            spatial_split = dist > _SPATIAL_THRESHOLD

        if current is None:
            current = Teamfight(
                start_tick=max(0, entry.tick - _COOLDOWN_TICKS),
                end_tick=0,
                last_death_tick=entry.tick,
                deaths=0,
                players=[TeamfightPlayer(player_id=i) for i in range(10)],
            )
            centroid_sum = [0.0, 0.0]
            centroid_count = 0
        elif temporal_gap or spatial_split:
            # Close current fight and open a new one
            current.end_tick = current.last_death_tick + _COOLDOWN_TICKS
            fights.append(current)
            current = Teamfight(
                start_tick=max(0, entry.tick - _COOLDOWN_TICKS),
                end_tick=0,
                last_death_tick=entry.tick,
                deaths=0,
                players=[TeamfightPlayer(player_id=i) for i in range(10)],
            )
            centroid_sum = [0.0, 0.0]
            centroid_count = 0

        current.last_death_tick = entry.tick
        current.deaths += 1
        # Update centroid with this death's position
        if death_pos is not None:
            centroid_sum[0] += death_pos[0]
            centroid_sum[1] += death_pos[1]
            centroid_count += 1

    if current is not None:
        current.end_tick = current.last_death_tick + _COOLDOWN_TICKS
        fights.append(current)

    if not fights:
        return []

    # --- Pass 2: populate per-player stats ----------------------------------
    for entry in entries:
        for fight in fights:
            if entry.tick < fight.start_tick or entry.tick > fight.end_tick:
                continue

            atk_slot = h2s.get(entry.attacker_name)
            tgt_slot = h2s.get(entry.target_name)

            if entry.log_type == "DAMAGE":
                if entry.target_is_hero and not entry.target_is_illusion and entry.attacker_is_hero:
                    if atk_slot is not None:
                        fight.players[atk_slot].damage_dealt += entry.value
                    if tgt_slot is not None:
                        fight.players[tgt_slot].damage_taken += entry.value

            elif entry.log_type == "HEAL":
                # Only count healing dealt to a different allied hero (not self-heals from consumables)
                if (
                    entry.target_is_hero
                    and not entry.target_is_illusion
                    and entry.attacker_is_hero
                    and entry.attacker_name != entry.target_name
                    and atk_slot is not None
                ):
                    fight.players[atk_slot].healing += entry.value

            elif entry.log_type == "DEATH":
                if entry.target_is_hero and not entry.target_is_illusion and tgt_slot is not None:
                    fight.players[tgt_slot].deaths += 1

            elif entry.log_type == "BUYBACK":
                bslot = entry.value  # buyback value = player slot
                if isinstance(bslot, int) and 0 <= bslot < 10:
                    fight.players[bslot].buybacks += 1

            elif entry.log_type == "GOLD":
                if atk_slot is not None:
                    fight.players[atk_slot].gold_delta += entry.value

            elif entry.log_type in ("ABILITY", "ITEM") and (
                entry.attacker_is_hero
                and not entry.attacker_is_illusion
                and atk_slot is not None
                and entry.inflictor_name
            ):
                uses = (
                    fight.players[atk_slot].ability_uses
                    if entry.log_type == "ABILITY"
                    else fight.players[atk_slot].item_uses
                )
                uses[entry.inflictor_name] = uses.get(entry.inflictor_name, 0) + 1

    # --- Pass 3: XP deltas from snapshots -----------------------------------
    if player_snapshots:
        for fight in fights:
            for pid, pid_snaps in player_snapshots.items():
                if not pid_snaps or pid >= 10:
                    continue
                xp_start = _nearest_xp(pid_snaps, fight.start_tick)
                xp_end = _nearest_xp(pid_snaps, fight.end_tick)
                if xp_start is not None and xp_end is not None:
                    fight.players[pid].xp_delta = max(0, xp_end - xp_start)

    return fights


def _nearest_xp(snaps: list, tick: int) -> int | None:
    """Return XP from the snapshot nearest to the given tick."""
    if not snaps:
        return None
    return min(snaps, key=lambda s: abs(s.tick - tick)).xp
