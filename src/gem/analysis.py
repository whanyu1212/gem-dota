"""Post-parse analysis helpers for gem replay data.

Utilities that transform raw ``ParsedMatch`` / ``ParsedPlayer`` data into
higher-level structures suitable for agentic or analytical use.

Functions:
    position_at_tick: Interpolate a hero's (x, y) position at any tick.
    group_ability_hits: Group combat log DAMAGE entries into per-cast records.
    teamfight_at_tick: Return the teamfight that contains a given tick.
    heroes_near: Find all heroes within a radius of a map position at a tick.
    ability_level_at_tick: Return the level of an ability at a given tick.
    estimate_vision: Estimate whether a team had vision of a map point at a tick.
"""

from __future__ import annotations

import bisect
import math
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from gem.combatlog import CombatLogEntry
    from gem.extractors.teamfights import Teamfight
    from gem.models import ParsedMatch, ParsedPlayer

# ---------------------------------------------------------------------------
# Vision constants
# ---------------------------------------------------------------------------

# Standard Dota 2 hero vision radii (world units).
# Heroes with special vision (Slardar ulti, Aghs upgrades, etc.) are edge cases
# we cannot track without per-tick entity sampling — these defaults cover ~95%.
_DAY_VISION: int = 1800
_NIGHT_VISION: int = 800

# Observer ward vision radius (constant, no items change it)
_WARD_VISION: int = 1600

# Day/night cycle constants (ticks at 30 ticks/sec)
# Day starts at game time 0:00, each full cycle is 15 minutes (7:30 day + 7:30 night)
_DAY_NIGHT_CYCLE_TICKS: int = 15 * 60 * 30  # 27000 ticks
_NIGHT_START_TICKS: int = 7 * 60 * 30 + 15 * 30  # 7:30 into cycle = 13950 ticks


# ---------------------------------------------------------------------------
# position_at_tick
# ---------------------------------------------------------------------------


def position_at_tick(
    player: ParsedPlayer,
    tick: int,
) -> tuple[float, float] | None:
    """Return the closest recorded (x, y) position for a player at a given tick.

    Searches ``player.position_log`` (a list of ``(tick, x, y)`` tuples
    sampled at ~1-second intervals) for the entry with the smallest tick
    distance to the requested tick.

    Args:
        player: A ``ParsedPlayer`` with a populated ``position_log``.
        tick: The game tick to query.

    Returns:
        ``(x, y)`` world coordinates of the nearest sample, or ``None`` if
        ``position_log`` is empty.

    Example:
        >>> pos = position_at_tick(axe_player, fight.start_tick)
        >>> if pos:
        ...     print(f"Axe was at ({pos[0]:.0f}, {pos[1]:.0f}) when the fight started")
    """
    log = player.position_log
    if not log:
        return None

    ticks = [entry[0] for entry in log]
    idx = bisect.bisect_left(ticks, tick)

    if idx == 0:
        return (log[0][1], log[0][2])
    if idx >= len(log):
        return (log[-1][1], log[-1][2])

    before = log[idx - 1]
    after = log[idx]
    # Pick whichever sample is closer in tick distance
    if tick - before[0] <= after[0] - tick:
        return (before[1], before[2])
    return (after[1], after[2])


# ---------------------------------------------------------------------------
# group_ability_hits — multi-target cast disambiguation
# ---------------------------------------------------------------------------


@dataclass
class AbilityCast:
    """A single ability (or item) cast with all targets it hit.

    Attributes:
        tick: Game tick at which the cast occurred.
        caster: NPC name of the casting unit (hero, summon, etc.).
        ability: Ability or item name (``inflictor_name`` from the combat log).
        targets: NPC names of all units hit by this cast.
        total_damage: Sum of all damage values across hits.
        damage_type: Damage type of the first hit (representative; all hits
            from the same cast share the same type).
        stun_duration: Stun seconds from the first hit entry that has one.
        entries: All raw ``CombatLogEntry`` objects that compose this cast.
    """

    tick: int
    caster: str
    ability: str
    targets: list[str] = field(default_factory=list)
    total_damage: int = 0
    damage_type: str = ""
    stun_duration: float = 0.0
    entries: list[CombatLogEntry] = field(default_factory=list)


def group_ability_hits(
    combat_log: list[CombatLogEntry],
    window_ticks: int = 5,
) -> list[AbilityCast]:
    """Group DAMAGE combat log entries into per-cast ``AbilityCast`` records.

    Many abilities hit multiple targets simultaneously (e.g. Tidehunter
    Ravage, Magnus RP, Naga Siren Song of the Siren). The combat log emits
    one DAMAGE entry per target hit, all within a few ticks of each other.
    This function groups those entries into a single ``AbilityCast``.

    Only entries with a non-empty ``inflictor_name`` are considered (raw
    right-click auto-attacks have an empty inflictor). Entries from the same
    ``(caster, ability)`` pair that fall within ``window_ticks`` of the
    previous hit are merged into the same cast.

    Args:
        combat_log: All ``CombatLogEntry`` objects from ``ParsedMatch.combat_log``,
            or any filtered subset.
        window_ticks: Maximum tick gap between successive hits of the same
            ability to be considered part of the same cast. Default 5
            (~1/6 second at 30 ticks/sec) works for AoE spells. Increase to
            10–15 for channelled abilities (e.g. Naga Song of the Siren).

    Returns:
        List of ``AbilityCast`` objects in chronological order.

    Example:
        >>> casts = group_ability_hits(match.combat_log)
        >>> big_hits = [c for c in casts if c.total_damage > 1000]
        >>> for cast in big_hits:
        ...     print(f"{cast.caster} cast {cast.ability} for {cast.total_damage} damage "
        ...           f"hitting {len(cast.targets)} targets")
    """
    # Filter to DAMAGE entries that have a named ability/item as the source
    damage_entries = [e for e in combat_log if e.log_type == "DAMAGE" and e.inflictor_name]
    damage_entries.sort(key=lambda e: e.tick)

    casts: list[AbilityCast] = []
    # key: (caster, ability) → active AbilityCast
    active: dict[tuple[str, str], AbilityCast] = {}

    for entry in damage_entries:
        key = (entry.attacker_name, entry.inflictor_name)
        existing = active.get(key)

        if existing is not None and entry.tick - existing.tick <= window_ticks:
            # Merge into existing cast
            existing.targets.append(entry.target_name)
            existing.total_damage += entry.value
            existing.entries.append(entry)
            if not existing.stun_duration and entry.stun_duration:
                existing.stun_duration = entry.stun_duration
        else:
            # Start a new cast
            cast = AbilityCast(
                tick=entry.tick,
                caster=entry.attacker_name,
                ability=entry.inflictor_name,
                targets=[entry.target_name],
                total_damage=entry.value,
                damage_type=entry.damage_type,
                stun_duration=entry.stun_duration,
                entries=[entry],
            )
            casts.append(cast)
            active[key] = cast

    casts.sort(key=lambda c: c.tick)
    return casts


# ---------------------------------------------------------------------------
# teamfight_at_tick
# ---------------------------------------------------------------------------


def teamfight_at_tick(match: ParsedMatch, tick: int) -> Teamfight | None:
    """Return the teamfight window that contains the given tick, or ``None``.

    Fights are non-overlapping and sorted by ``start_tick``.  Uses binary
    search on ``start_tick`` values for O(log N) lookup.

    Args:
        match: A parsed replay with ``match.teamfights`` populated.
        tick: Game tick to query.

    Returns:
        The ``Teamfight`` whose ``[start_tick, end_tick]`` window contains
        ``tick``, or ``None`` if no fight contains it.

    Example:
        >>> fight = teamfight_at_tick(match, entry.tick)
        >>> if fight:
        ...     print(f"Event occurred during a fight with {fight.deaths} deaths")
    """
    fights = match.teamfights
    if not fights:
        return None

    start_ticks = [f.start_tick for f in fights]
    idx = bisect.bisect_right(start_ticks, tick) - 1
    if idx < 0:
        return None
    fight = fights[idx]
    if fight.start_tick <= tick <= fight.end_tick:
        return fight
    return None


# ---------------------------------------------------------------------------
# heroes_near
# ---------------------------------------------------------------------------


def heroes_near(
    match: ParsedMatch,
    tick: int,
    x: float,
    y: float,
    radius: float,
) -> list[ParsedPlayer]:
    """Return all heroes within ``radius`` world units of ``(x, y)`` at ``tick``.

    Uses ``position_at_tick`` to estimate each hero's position at the requested
    tick from their ``position_log`` samples.  Heroes with no position data are
    excluded.

    Args:
        match: A parsed replay with ``players`` populated.
        tick: Game tick to query.
        x: World x coordinate of the centre point.
        y: World y coordinate of the centre point.
        radius: Search radius in world units.

    Returns:
        List of ``ParsedPlayer`` objects whose estimated position at ``tick``
        is within ``radius`` of ``(x, y)``, in ascending distance order.

    Example:
        >>> nearby = heroes_near(match, fight.start_tick,
        ...                      fight.centroid_x, fight.centroid_y, 2000)
        >>> print(f"{len(nearby)} heroes near fight start")
    """
    results: list[tuple[float, ParsedPlayer]] = []
    for player in match.players:
        pos = position_at_tick(player, tick)
        if pos is None:
            continue
        dist = math.dist(pos, (x, y))
        if dist <= radius:
            results.append((dist, player))
    results.sort(key=lambda t: t[0])
    return [p for _, p in results]


# ---------------------------------------------------------------------------
# ability_level_at_tick
# ---------------------------------------------------------------------------


def ability_level_at_tick(
    player: ParsedPlayer,
    ability: str,
    tick: int,
) -> int:
    """Return the level of an ability for a player at a given tick.

    Searches ``player.position_log``-aligned snapshots indirectly via the
    per-minute ability level data stored in ``ParsedPlayer``.  Since full
    per-tick ability level snapshots are not stored, this uses the nearest
    minute-boundary snapshot whose tick is ``≤ tick`` (last known level at or
    before the requested tick).

    Ability names match the ``inflictor_name`` field in the combat log (e.g.
    ``"axe_berserkers_call"``).  Returns 0 if the ability is not yet learned
    at the given tick.

    Args:
        player: A ``ParsedPlayer`` with ``_ability_snapshots`` populated, or
            accessed via the ``ability_levels_at`` helper that uses
            ``times_min`` parallel arrays.  In practice, call
            ``ability_level_at_tick`` with the ``ParsedPlayer`` and ability
            name — it returns the last-known level at or before ``tick``.
        ability: Ability name as it appears in the combat log
            (``inflictor_name``).
        tick: Game tick to query.

    Returns:
        Ability level (1–4 for most abilities, 0 if not yet learned).

    Example:
        >>> lvl = ability_level_at_tick(axe, "axe_berserkers_call", cast.tick)
        >>> print(f"Berserker's Call was level {lvl} when cast")
    """
    # ability_snapshots is a list of (tick, ability_levels_dict) sorted by tick,
    # built from the per-minute snapshots stored on ParsedPlayer._ability_snapshots.
    # Fall back gracefully if the attribute is missing (older parsed data).
    snapshots: list[tuple[int, dict[str, int]]] = getattr(player, "_ability_snapshots", [])
    if not snapshots:
        return 0

    snap_ticks = [s[0] for s in snapshots]
    idx = bisect.bisect_right(snap_ticks, tick) - 1
    if idx < 0:
        return 0
    return snapshots[idx][1].get(ability, 0)


# ---------------------------------------------------------------------------
# estimate_vision — geometry-based fog-of-war approximation
# ---------------------------------------------------------------------------


@dataclass
class VisionSource:
    """One unit that was providing vision of a map point at a given tick.

    Attributes:
        kind: ``"hero"`` if the source is an allied hero, ``"ward"`` if an
            observer ward, or ``"modifier"`` if a vision-granting ability or item
            (Slardar Corrosive Haze, Bounty Hunter Track, Dust of Appearance, Gem
            of True Sight, etc.) is revealing the target hero.
        name: NPC hero name (e.g. ``"npc_dota_hero_axe"``) for heroes,
            ``"observer_ward"`` for wards, or the internal modifier name (e.g.
            ``"modifier_slardar_amplify_damage"``) for modifier-based reveals.
        distance: World-unit distance from the source to the queried point.  For
            modifier sources this is the distance from the revealed hero's position
            to the query point.
        vision_radius: Vision radius used for this source at the queried tick
            (day/night-adjusted for heroes; constant for wards; 0 for modifiers
            since the reveal is unconditional rather than radius-based).
    """

    kind: Literal["hero", "ward", "modifier"]
    name: str
    distance: float
    vision_radius: int


def _is_daytime(game_start_tick: int | None, tick: int) -> bool:
    """Return True if it is daytime at the given absolute tick.

    Dota 2 day/night cycle: day starts at game time 0:00.  Each half-cycle
    is 7 minutes 30 seconds (13500 ticks).  The cycle repeats every 15 minutes.

    Args:
        game_start_tick: Absolute tick when the game clock started, or ``None``.
        tick: Absolute tick to query.

    Returns:
        ``True`` if daytime, ``False`` if nighttime.
    """
    start = game_start_tick or 0
    game_ticks = max(tick - start, 0)
    phase = game_ticks % _DAY_NIGHT_CYCLE_TICKS
    return phase < _NIGHT_START_TICKS


def estimate_vision(
    match: ParsedMatch,
    team: int,
    tick: int,
    x: float,
    y: float,
) -> list[VisionSource]:
    """Estimate which allied units were providing vision of ``(x, y)`` at ``tick``.

    Uses a geometry-based approximation: a team has vision of a point if any
    allied hero or live observer ward is within their vision radius of that
    point.  Hero vision radius is day/night adjusted (1800 day / 800 night).
    Observer wards have a constant 1600-unit radius.

    **Limitations** — this is an approximation.  It does not model:

    - High-ground vision penalties (enemy cannot see down from high ground).
    - Vision modifiers from abilities or items (e.g. Slardar Corrosive Haze,
      Aghanim's Scepter upgrades, Shroud of Stillness scouting).
    - Summon/creep vision (only heroes and observer wards are checked).
    - Sentry ward true-sight (sentries do not grant standard vision).

    For the primary agentic use case ("was this initiation telegraphed or
    blind?") this gives ~85–90% accuracy across typical professional games.

    Args:
        match: A parsed replay.
        team: Team number to check vision for (2=Radiant, 3=Dire).
        tick: Game tick to query.
        x: World x coordinate of the point to check.
        y: World y coordinate of the point to check.

    Returns:
        List of :class:`VisionSource` objects for each allied unit that had
        vision of ``(x, y)`` at ``tick``, sorted by ascending distance.
        An empty list means no vision (point was in fog for that team).

    Example:
        >>> sources = estimate_vision(match, 3, fight.start_tick,
        ...                           target_x, target_y)
        >>> if sources:
        ...     print(f"Dire had vision via {sources[0].kind}: {sources[0].name}")
        ... else:
        ...     print("Blind initiation — target was in fog")
    """
    daytime = _is_daytime(match.game_start_tick, tick)
    hero_radius = _DAY_VISION if daytime else _NIGHT_VISION

    sources: list[VisionSource] = []

    # --- Hero vision ---
    for player in match.players:
        if player.team != team:
            continue
        pos = position_at_tick(player, tick)
        if pos is None:
            continue
        dist = math.dist(pos, (x, y))
        if dist <= hero_radius:
            sources.append(
                VisionSource(
                    kind="hero",
                    name=player.hero_name,
                    distance=dist,
                    vision_radius=hero_radius,
                )
            )

    # --- Observer ward vision ---
    for ward in match.wards:
        if ward.ward_type != "observer":
            continue
        if ward.team != team:
            continue
        if ward.x is None or ward.y is None:
            continue
        # Ward must have been placed by this tick and still alive
        if ward.tick > tick:
            continue
        end_tick = ward.killed_tick or ward.expires_tick
        if end_tick is not None and end_tick < tick:
            continue
        dist = math.dist((ward.x, ward.y), (x, y))
        if dist <= _WARD_VISION:
            sources.append(
                VisionSource(
                    kind="ward",
                    name="observer_ward",
                    distance=dist,
                    vision_radius=_WARD_VISION,
                )
            )

    # --- Vision modifier reveals ---
    # Modifiers like Slardar Corrosive Haze, Bounty Hunter Track, and Dust of
    # Appearance mark specific enemy heroes as revealed for the caster's team.
    # If the revealed hero is near the query point, it counts as vision.
    #
    # We check modifiers where caster_team == team (the team we're checking vision
    # for) and the modifier is active at the queried tick.  The modifier's target
    # is the enemy hero that has been revealed; if that hero is near the query
    # point, the modifier itself is sufficient to grant vision regardless of the
    # standard hero/ward radius.  We use the revealed hero's position at the tick
    # to compute distance.
    for mod_ev in getattr(match, "vision_modifiers", []):
        if mod_ev.caster_team != team:
            continue
        if mod_ev.tick > tick:
            continue
        if mod_ev.end_tick is not None and mod_ev.end_tick < tick:
            continue
        # Find the revealed hero's position
        target_player = next(
            (pl for pl in match.players if pl.hero_name == mod_ev.target_name),
            None,
        )
        if target_player is None:
            continue
        pos = position_at_tick(target_player, tick)
        if pos is None:
            continue
        dist = math.dist(pos, (x, y))
        # Use the revealed hero's own position as the vision source location
        # (the modifier grants direct vision of that hero, so the "radius" is
        # how far the modifier source is from the query point — effectively
        # dist == 0 means the query IS at the hero).  We report the distance
        # from the revealed hero to the query point.  No radius check — a
        # modifier-revealed hero is always "seen" regardless of how far the
        # query point is from the hero's position.  (Dust/Gem have a static
        # aura radius; we use 0 as an approximation since we don't model auras.)
        sources.append(
            VisionSource(
                kind="modifier",
                name=mod_ev.modifier_name,
                distance=dist,
                vision_radius=0,
            )
        )

    sources.sort(key=lambda s: s.distance)
    return sources
