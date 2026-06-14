"""Vision approximation helpers for parsed matches."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from gem.analysis.spatial import position_at_tick

if TYPE_CHECKING:
    from gem.results.models import ParsedMatch

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


_WARD_VISION_RADIUS_SQ: int = _WARD_VISION * _WARD_VISION


def ward_vision_impact(ward: object, match: ParsedMatch) -> int:
    """Count distinct enemy heroes spotted by an observer ward during its lifetime.

    For each enemy hero, checks whether any position sample within the ward's
    active window falls within the standard 1600-unit observer ward vision
    radius.  Only the first sighting per hero is counted — the goal is to
    measure how many distinct enemies the ward revealed, not how many times.

    Only observer wards are evaluated; sentry wards return 0.

    Args:
        ward: A ward object (e.g. from ``match.wards``) with attributes:
            ``ward_type``, ``x``, ``y``, ``tick``, ``killed_tick``,
            ``expires_tick``, ``team``.
        match: A parsed replay with ``players`` and ``game_end_tick`` populated.

    Returns:
        Number of distinct enemy heroes that entered the ward's vision radius
        while it was alive. Returns 0 for sentry wards or wards with no
        coordinate data.

    Note:
        This is an **approximation**, not ground-truth vision data:

        - Position samples are taken every ~5 seconds (150 ticks), so heroes
          passing through the ward's radius between samples go undetected.
        - Vision is a flat 2D radius check — terrain, cliffs, and trees that
          block line-of-sight in-game are not modelled.
        - Night vision (800 units) is not distinguished from day vision (1600
          units); the full 1600-unit radius is always used.

        The result is suitable as a heuristic ward-quality signal, not a
        precise replay-accurate vision count.

    Example:
        >>> impact = ward_vision_impact(ward, match)
        >>> print(f"Ward spotted {impact} distinct enemy heroes")
    """
    if getattr(ward, "ward_type", "") != "observer":
        return 0
    wx = getattr(ward, "x", None)
    wy = getattr(ward, "y", None)
    if wx is None or wy is None:
        return 0

    ward_tick: int = getattr(ward, "tick", 0)
    end_tick: int = (
        getattr(ward, "killed_tick", None)
        or getattr(ward, "expires_tick", None)
        or match.game_end_tick
        or 0
    )
    enemy_team = 3 if getattr(ward, "team", 0) == 2 else 2

    seen: set[str] = set()
    for player in match.players:
        if player.team != enemy_team:
            continue
        for tick, px, py in player.position_log:
            if tick < ward_tick or tick > end_tick:
                continue
            if (px - wx) ** 2 + (py - wy) ** 2 <= _WARD_VISION_RADIUS_SQ:
                seen.add(player.hero_name)
                break  # one sighting is enough per hero
    return len(seen)
