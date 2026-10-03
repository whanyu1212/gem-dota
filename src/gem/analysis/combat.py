"""Combat-log and fight analysis helpers.

Reference: fight windows follow odota/parser
src/main/java/opendota/CreateParsedDataBlob.java ``processTeamfights`` (pinned
in CLAUDE.md), extended with gem's spatial split in
:mod:`gem.extractors.fights`.
"""

from __future__ import annotations

import bisect
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from gem.extractors.fights import FIGHT_RADIUS, FIGHT_WINDOW_S, detect_fights

if TYPE_CHECKING:
    from gem.combat.log import CombatLogEntry
    from gem.extractors.fights import Fight
    from gem.extractors.players import PlayerStateSnapshot
    from gem.results.models import ParsedMatch, ParsedPlayer


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
    ``(caster, ability)`` pair that fall within ``window_ticks`` of the cast's
    *start tick* (the first hit) are merged into the same cast. The window is
    anchored at the cast's start, not the most recent hit, so a long sustained
    stream of same-ability hits will not keep extending one cast indefinitely.

    Args:
        combat_log: All ``CombatLogEntry`` objects from ``ParsedMatch.combat_log``,
            or any filtered subset.
        window_ticks: Maximum tick gap from a cast's start tick for a later hit
            of the same ability to be folded into it. Default 5 (~1/6 second at
            30 ticks/sec) works for AoE spells. Increase to 10–15 for channelled
            abilities (e.g. Naga Song of the Siren).

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


def find_fights(
    match: ParsedMatch,
    *,
    window_s: float = FIGHT_WINDOW_S,
    radius: float | None = FIGHT_RADIUS,
) -> list[Fight]:
    """Group a parsed match's hero deaths into fights with your own settings.

    ``match.fights`` uses the defaults. Filtering it can only drop fights; this
    regroups them instead, without parsing the replay again (a loaded
    :func:`gem.load_json` match works too). With the defaults it returns the
    same fights as ``match.fights``.

    Args:
        match: A parsed or loaded match.
        window_s: Seconds after a fight's last death that a new death still
            joins it.
        radius: Largest distance, in world units, between a death and a
            fight's centroid for the death to join that fight. ``None`` groups
            by time only, as OpenDota does, so simultaneous fights in different
            places become one.

    Returns:
        The fights, in chronological order, with per-player breakdowns.

    Example:
        >>> by_time = gem.find_fights(match, radius=None)
        >>> teamfights = [f for f in by_time if f.deaths >= 3]
    """
    return detect_fights(
        match.combat_log,
        hero_to_slot={pp.hero_name: pp.player_id for pp in match.players if pp.hero_name},
        player_snapshots={pp.player_id: _fight_samples(pp) for pp in match.players},
        slot_to_team={pp.player_id: pp.team for pp in match.players if pp.team},
        window_s=window_s,
        radius=radius,
    )


def _fight_samples(player: ParsedPlayer) -> list[PlayerStateSnapshot]:
    """Rebuild the snapshot positions and XP that fight detection reads."""
    from gem.extractors.players import PlayerStateSnapshot

    positions = {tick: (x, y) for tick, x, y in reversed(player.position_log)}
    samples = []
    for index, tick in enumerate(player.times):
        x, y = positions.get(tick, (None, None))
        xp = player.total_earned_xp_t[index] if index < len(player.total_earned_xp_t) else 0
        samples.append(
            PlayerStateSnapshot(
                tick=tick,
                player_id=player.player_id,
                npc_name=player.hero_name,
                team=player.team,
                level=0,
                xp=0,
                gold=0,
                net_worth=0,
                lh=0,
                dn=0,
                hp=0,
                max_hp=0,
                mana=0.0,
                max_mana=0.0,
                x=x,
                y=y,
                total_earned_xp=xp,
            )
        )
    return samples


def fight_at_tick(match: ParsedMatch, tick: int) -> Fight | None:
    """Return the fight window that contains the given tick, or ``None``.

    Fights are non-overlapping and sorted by ``start_tick``.  Uses binary
    search on ``start_tick`` values for O(log N) lookup.

    Args:
        match: A parsed replay with ``match.fights`` populated.
        tick: Game tick to query.

    Returns:
        The ``Fight`` whose ``[start_tick, end_tick]`` window contains
        ``tick``, or ``None`` if no fight contains it.

    Example:
        >>> fight = fight_at_tick(match, entry.tick)
        >>> if fight:
        ...     print(f"Event occurred during a fight with {fight.deaths} deaths")
    """
    fights = match.fights
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


def is_active_fight_participant(player_stats: object) -> bool:
    """Return True if a player was an active participant in a fight.

    A player is considered active if they had any direct hero-vs-hero combat
    during the fight window: a death, dealing damage to an enemy hero, taking
    damage from an enemy hero, or healing an allied hero.

    Passive presence (e.g. farming nearby, casting only on creeps) does not
    count. This mirrors the definition used by the HTML match report and the
    fight detection logic documented in MEMORY.md.

    Args:
        player_stats: A fight player stats object with optional numeric
            attributes: ``deaths``, ``damage_dealt``, ``damage_taken``,
            ``healing``. Missing attributes are treated as 0.

    Returns:
        ``True`` if the player had direct combat involvement, ``False``
        otherwise.

    Example:
        >>> fight = match.fights[0]
        >>> active = [p for p in fight.players if is_active_fight_participant(p)]
        >>> print(f"{len(active)} active participants in fight")
    """
    return (
        getattr(player_stats, "deaths", 0) > 0
        or getattr(player_stats, "damage_dealt", 0) > 0
        or getattr(player_stats, "damage_taken", 0) > 0
        or getattr(player_stats, "healing", 0) > 0
    )
