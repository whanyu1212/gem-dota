"""Teamfight detection from combat log entries.

Detects teamfights by merging hero death events within a rolling cooldown
window, then aggregates per-player stats (damage dealt/taken, healing,
gold delta, XP delta, deaths, buybacks, ability/item uses) for each fight.

Algorithm extends the reference implementation with spatial clustering:
  - A new fight opens on any non-illusion hero death.
  - ``start_tick = first_death_tick - cooldown``
  - The fight closes once ``cooldown`` ticks elapse with no new hero death,
    setting ``end_tick = last_death_tick + cooldown``.
  - When position data is available, concurrent fight windows are tracked.
    A new death extends the nearest active window whose centroid is within
    ``_FIGHT_RADIUS`` world units; otherwise a new parallel window is opened.
    This separates simultaneous skirmishes in different parts of the map.
  - Without position data the algorithm falls back to the original single-
    window temporal approach (reference-compatible).
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

# Maximum world-unit distance between a death and an active fight's centroid
# for the death to be absorbed into that fight rather than opening a new one.
# Arbitrary starting value — calibrate against real replays during validation.
_FIGHT_RADIUS: float = 3000.0


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
        radiant_kills: Hero kills scored by Radiant within the window.
        dire_kills: Hero kills scored by Dire within the window.
        winner: ``"radiant"`` if Radiant scored more kills, ``"dire"`` if Dire
            scored more kills, ``"draw"`` if equal, or ``"unknown"`` if team
            information is unavailable.
        centroid_x: Death-count-weighted mean X of all deaths in the window,
            or ``None`` when position data is unavailable.
        centroid_y: Death-count-weighted mean Y of all deaths in the window,
            or ``None`` when position data is unavailable.
        players: One ``TeamfightPlayer`` per slot (indices 0–9).
    """

    start_tick: int
    end_tick: int
    last_death_tick: int
    deaths: int
    radiant_kills: int = 0
    dire_kills: int = 0
    winner: str = "unknown"
    centroid_x: float | None = None
    centroid_y: float | None = None
    players: list[TeamfightPlayer] = field(default_factory=list)


def detect_teamfights(
    combat_log: list[CombatLogEntry],
    hero_to_slot: dict[str, int] | None = None,
    player_snapshots: dict[int, list[PlayerStateSnapshot]] | None = None,
    slot_to_team: dict[int, int] | None = None,
) -> list[Teamfight]:
    """Detect teamfights from a match combat log.

    When ``player_snapshots`` is provided, spatial clustering is applied in
    addition to the temporal cooldown: a death only extends an existing fight
    window if it falls within ``_FIGHT_RADIUS`` world units of that window's
    current centroid.  Deaths outside all active windows open a new parallel
    window, separating simultaneous skirmishes in different parts of the map.

    Without position data the algorithm falls back to the original single-
    window temporal approach.

    Args:
        combat_log: All ``CombatLogEntry`` objects from ``ParsedMatch.combat_log``.
        hero_to_slot: Mapping of NPC hero name → player slot (0–9).  Built from
            ``{pp.hero_name: pp.player_id for pp in match.players}``.  Used to
            attribute damage/healing/ability events to the correct player slot.
        player_snapshots: Optional mapping of ``player_id → list[PlayerStateSnapshot]``
            used both to compute XP deltas and to resolve hero positions at death
            ticks for spatial clustering.
        slot_to_team: Optional mapping of player slot → team number (2=Radiant,
            3=Dire).  When provided, ``radiant_kills``, ``dire_kills``, and
            ``winner`` are populated on each ``Teamfight``.

    Returns:
        List of ``Teamfight`` objects in chronological order.  No minimum-death
        filter is applied; callers may filter on ``Teamfight.deaths`` or
        participation count.
    """
    h2s: dict[str, int] = hero_to_slot or {}
    entries = sorted(combat_log, key=lambda e: e.tick)

    # --- Pass 1: detect fight windows from hero deaths ----------------------
    # ``active`` holds fights still within their cooldown window.
    # ``closed`` holds fights whose cooldown has expired.
    active: list[Teamfight] = []
    closed: list[Teamfight] = []

    for entry in entries:
        if entry.log_type != "DEATH":
            continue
        if not entry.target_is_hero or entry.target_is_illusion:
            continue

        # Expire any active fights whose cooldown has elapsed before this death.
        still_active: list[Teamfight] = []
        for f in active:
            if entry.tick - f.last_death_tick >= _COOLDOWN_TICKS:
                f.end_tick = f.last_death_tick + _COOLDOWN_TICKS
                closed.append(f)
            else:
                still_active.append(f)
        active = still_active

        # Resolve the dying hero's position from the nearest snapshot.
        death_pos: tuple[float, float] | None = None
        if player_snapshots:
            tgt_slot = h2s.get(entry.target_name)
            if tgt_slot is not None:
                snaps = player_snapshots.get(tgt_slot, [])
                death_pos = _nearest_pos(snaps, entry.tick)

        # Find the best active fight to absorb this death into.
        target_fight: Teamfight | None = None
        if active:
            if death_pos is not None:
                # Spatial mode: pick the closest fight centroid within radius.
                # Fights without a centroid (position unavailable for all their
                # deaths so far) are treated as infinitely far — never absorb
                # into them when we have position data for the current death.
                best_dist = _FIGHT_RADIUS
                for f in active:
                    if f.centroid_x is not None and f.centroid_y is not None:
                        d = math.dist(death_pos, (f.centroid_x, f.centroid_y))
                        if d < best_dist:
                            best_dist = d
                            target_fight = f
            else:
                # No position data for this death — fall back to temporal-only:
                # absorb into the most recently active fight.
                target_fight = max(active, key=lambda f: f.last_death_tick)

        if target_fight is None:
            # No suitable active fight — open a new window.
            target_fight = Teamfight(
                start_tick=max(0, entry.tick - _COOLDOWN_TICKS),
                end_tick=0,
                last_death_tick=entry.tick,
                deaths=0,
                players=[TeamfightPlayer(player_id=i) for i in range(10)],
            )
            active.append(target_fight)

        target_fight.last_death_tick = entry.tick
        target_fight.deaths += 1

        # Update the fight's running centroid with this death's position.
        if death_pos is not None:
            target_fight.centroid_x, target_fight.centroid_y = _update_centroid(
                target_fight.centroid_x,
                target_fight.centroid_y,
                target_fight.deaths,
                death_pos,
            )

    # Close any fights still active at end of log.
    for f in active:
        f.end_tick = f.last_death_tick + _COOLDOWN_TICKS
        closed.append(f)

    fights = sorted(closed, key=lambda f: f.start_tick)

    if not fights:
        return []

    # --- Pass 2: populate per-player stats ----------------------------------
    # For events that carry an attacker (DAMAGE, HEAL, ABILITY, ITEM), apply a
    # spatial proximity check when position data is available: only credit the
    # event to a fight if the attacker was within _FIGHT_RADIUS of that fight's
    # centroid.  This prevents heroes active in a different part of the map
    # from being counted as participants in a fight they weren't present at.
    # DEATH, BUYBACK, and GOLD are not spatially filtered (no reliable position
    # can be derived for them at attribution time).
    for entry in entries:
        for fight in fights:
            if entry.tick < fight.start_tick or entry.tick > fight.end_tick:
                continue

            atk_slot = h2s.get(entry.attacker_name)
            tgt_slot = h2s.get(entry.target_name)

            if entry.log_type == "DAMAGE":
                if entry.target_is_hero and not entry.target_is_illusion and entry.attacker_is_hero:
                    if atk_slot is not None and _near_fight(
                        atk_slot, entry.tick, fight, player_snapshots
                    ):
                        fight.players[atk_slot].damage_dealt += entry.value
                    if tgt_slot is not None and _near_fight(
                        tgt_slot, entry.tick, fight, player_snapshots
                    ):
                        fight.players[tgt_slot].damage_taken += entry.value

            elif entry.log_type == "HEAL":
                # Only count healing dealt to a different allied hero (not self-heals from consumables)
                if (
                    entry.target_is_hero
                    and not entry.target_is_illusion
                    and entry.attacker_is_hero
                    and entry.attacker_name != entry.target_name
                    and atk_slot is not None
                    and _near_fight(atk_slot, entry.tick, fight, player_snapshots)
                ):
                    fight.players[atk_slot].healing += entry.value

            elif entry.log_type == "DEATH":
                if entry.target_is_hero and not entry.target_is_illusion and tgt_slot is not None:
                    fight.players[tgt_slot].deaths += 1
                    # A Radiant hero dying = a kill for Dire, and vice versa.
                    if slot_to_team:
                        dying_team = slot_to_team.get(tgt_slot, 0)
                        if dying_team == 2:
                            fight.dire_kills += 1
                        elif dying_team == 3:
                            fight.radiant_kills += 1

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
                and _near_fight(atk_slot, entry.tick, fight, player_snapshots)
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
            for pid, snaps in player_snapshots.items():
                if not snaps or pid >= 10:
                    continue
                xp_start = _nearest_xp(snaps, fight.start_tick)
                xp_end = _nearest_xp(snaps, fight.end_tick)
                if xp_start is not None and xp_end is not None:
                    fight.players[pid].xp_delta = max(0, xp_end - xp_start)

    # --- Pass 4: compute winner from kill counts ----------------------------
    if slot_to_team:
        for fight in fights:
            r, d = fight.radiant_kills, fight.dire_kills
            if r > d:
                fight.winner = "radiant"
            elif d > r:
                fight.winner = "dire"
            else:
                fight.winner = "draw"

    return fights


def _near_fight(
    slot: int,
    tick: int,
    fight: Teamfight,
    player_snapshots: dict | None,
) -> bool:
    """Return True if the player was spatially close to the fight at the given tick.

    Falls back to True (no filtering) when position data is unavailable for
    either the player or the fight centroid.

    Args:
        slot: Player slot (0–9).
        tick: Game tick of the event.
        fight: The fight whose centroid to check against.
        player_snapshots: Mapping of player_id → snapshots, or None.

    Returns:
        ``True`` if the player is within ``_FIGHT_RADIUS`` of the fight
        centroid, or if position data is missing.
    """
    if player_snapshots is None:
        return True
    if fight.centroid_x is None or fight.centroid_y is None:
        return True
    snaps = player_snapshots.get(slot)
    if not snaps:
        return True
    pos = _nearest_pos(snaps, tick)
    if pos is None:
        return True
    return math.dist(pos, (fight.centroid_x, fight.centroid_y)) <= _FIGHT_RADIUS


def _nearest_xp(snaps: list, tick: int) -> int | None:
    """Return XP from the snapshot nearest to the given tick."""
    if not snaps:
        return None
    return min(snaps, key=lambda s: abs(s.tick - tick)).xp


def _nearest_pos(snaps: list, tick: int) -> tuple[float, float] | None:
    """Return world (x, y) from the snapshot nearest to the given tick."""
    if not snaps:
        return None
    snap = min(snaps, key=lambda s: abs(s.tick - tick))
    if snap.x is None or snap.y is None:
        return None
    return snap.x, snap.y


def _update_centroid(
    cx: float | None,
    cy: float | None,
    new_death_count: int,
    pos: tuple[float, float],
) -> tuple[float, float]:
    """Return an updated running centroid after adding one new death position.

    Uses the incremental mean formula so we never store all raw positions.

    Args:
        cx: Current centroid X, or ``None`` if this is the first death.
        cy: Current centroid Y, or ``None`` if this is the first death.
        new_death_count: Total deaths in the window *after* adding this one.
        pos: World (x, y) of the new death.

    Returns:
        Updated ``(centroid_x, centroid_y)``.
    """
    if cx is None or cy is None:
        return pos
    # Incremental mean: new_mean = old_mean + (new_val - old_mean) / n
    n = new_death_count
    return (cx + (pos[0] - cx) / n, cy + (pos[1] - cy) / n)
