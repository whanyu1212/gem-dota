"""A fight's combat log as typed records: casts and what they hit, damage, modifiers, deaths.

Reference: odota/parser ``src/main/java/opendota/CreateParsedDataBlob.java``
(pinned in CLAUDE.md) for the combat-log semantics this reads:
``handleDamageCombat`` credits damage to the owner-resolved ``sourcename``,
``handleDeathCombat`` the kill, ``handleGold`` / ``handleXp`` key gold and XP by
their raw reason code on the receiving hero (``targetname``), and
``handleBuyback`` reads the player slot from ``value``. skadistats/clarity
``processor/gameevents/CombatLog.java`` delivers the entries. Valve's
``EDOTA_ModifyGold_Reason`` (1 death, 12 hero kill) and
``EDOTA_ModifyXP_Reason`` (1 hero kill) give the reason codes.

Everything here is read from the log except one derived field: a cast's
``hits``, the heroes that the cast's own ability damaged or debuffed within a
short window after it (see :func:`build_fight_timeline`). The grouping is
anchored on the ``ABILITY`` / ``ITEM`` entry, unlike
:func:`gem.analysis.combat.group_ability_hits`, which groups ``DAMAGE`` entries
from the first hit and has no cast to attach them to.
"""

from __future__ import annotations

import bisect
from collections import defaultdict, deque
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gem.combat.log import CombatLogEntry
    from gem.results.models import ParsedMatch

    _IsHero = Callable[[str, bool], bool]
    _Credited = Callable[[CombatLogEntry], str | None]

#: ``EDOTA_ModifyGold_Reason``: gold lost on death, and a hero-kill bounty.
GOLD_REASON_DEATH = 1
GOLD_REASON_HERO_KILL = 12
#: ``EDOTA_ModifyXP_Reason``: XP for a hero kill.
XP_REASON_HERO_KILL = 1


@dataclass(frozen=True, slots=True)
class CastHit:
    """What one cast did to one hero.

    Attributes:
        hero: The hero's NPC name.
        damage: Damage the cast's ability or item dealt to the hero.
        damage_type: ``"physical"``, ``"magical"``, ``"pure"`` or ``"others"``
            from the first damaging entry; ``""`` when the cast only debuffed.
        stun_s: Longest stun duration among the modifiers it applied (seconds),
            ``0.0`` when none.
        modifiers: Names of the modifiers it applied to the hero, in order.
    """

    hero: str
    damage: int = 0
    damage_type: str = ""
    stun_s: float = 0.0
    modifiers: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class TimelineCast:
    """One ability or item use by a hero, with the heroes it hit.

    Attributes:
        tick: Tick of the ``ABILITY`` / ``ITEM`` entry.
        caster: The casting hero's NPC name (illusions are left out).
        ability: Ability or item name as logged (items keep their ``item_``
            prefix).
        is_item: ``True`` for an ``ITEM`` entry.
        level: Ability level as logged (``0`` for most items).
        target: The unit the replay records as the cast's target, or ``None``.
            Most casts have none: the replay records a target only for some
            unit-targeted casts, and it need not be a hero or the hero hit.
        target_is_hero: ``True`` when ``target`` is a real (non-illusion) hero.
        hits: Other heroes the cast's ability or item damaged or debuffed
            within the hit window, in the order they were first hit. Derived:
            see :func:`build_fight_timeline`.
        self_effect: What the cast did to the caster (a self-buff such as Black
            King Bar), or ``None``.
    """

    tick: int
    caster: str
    ability: str
    is_item: bool
    level: int = 0
    target: str | None = None
    target_is_hero: bool = False
    hits: tuple[CastHit, ...] = ()
    self_effect: CastHit | None = None

    @property
    def damage(self) -> int:
        """Total damage the cast dealt to other heroes."""
        return sum(hit.damage for hit in self.hits)


@dataclass(frozen=True, slots=True)
class DamageBurst:
    """Damage from one unit to one hero, with one source and type, in a short burst.

    Attributes:
        start_tick: Tick of the first entry in the burst.
        end_tick: Tick of the last entry in the burst.
        attacker: The attacking unit's name (a hero, illusion, summon, tower...).
        attacker_is_illusion: ``True`` when the attacker is an illusion.
        attacker_hero: The hero credited with the damage (``damage_source_name``,
            the owner of a summon or illusion), or ``None`` for creeps, towers
            and other units.
        target: The damaged hero's NPC name.
        source: The ability or item that dealt it; ``""`` (or ``"dota_unknown"``
            as logged) for a right-click attack.
        damage_type: ``"physical"``, ``"magical"``, ``"pure"`` or ``"others"``.
        damage: Total damage.
        hits: Number of ``DAMAGE`` entries.
    """

    start_tick: int
    end_tick: int
    attacker: str
    attacker_is_illusion: bool
    attacker_hero: str | None
    target: str
    source: str
    damage_type: str
    damage: int
    hits: int


@dataclass(frozen=True, slots=True)
class ModifierWindow:
    """A modifier on a hero, from ``MODIFIER_ADD`` to its ``MODIFIER_REMOVE``.

    Attributes:
        target: The hero's NPC name.
        modifier: Modifier name as logged.
        source: The unit that applied it.
        source_hero: The hero credited with it (``damage_source_name``), or
            ``None``.
        start_tick: Tick it was added, or ``None`` when it was added before the
            timeline's window and only its removal is in it.
        end_tick: Tick it was removed, or ``None`` when it outlasted the window.
        duration_s: Duration the log gives on the add (seconds), or ``None``.
        stun_s: Stun duration the log gives on the add (seconds); ``0.0`` when
            it is not a stun.
        aura: ``True`` for an aura modifier, ``None`` when the log doesn't say.
    """

    target: str
    modifier: str
    source: str
    source_hero: str | None
    start_tick: int | None
    end_tick: int | None
    duration_s: float | None = None
    stun_s: float = 0.0
    aura: bool | None = None


@dataclass(frozen=True, slots=True)
class DamageTaken:
    """Damage a hero took from one unit, source and type before dying.

    Attributes:
        attacker: The attacking unit's name.
        attacker_is_illusion: ``True`` when the attacker is an illusion.
        attacker_hero: The hero credited with the damage, or ``None``.
        source: The ability or item, or ``""`` / ``"dota_unknown"`` for attacks.
        damage_type: ``"physical"``, ``"magical"``, ``"pure"`` or ``"others"``.
        damage: Total damage.
    """

    attacker: str
    attacker_is_illusion: bool
    attacker_hero: str | None
    source: str
    damage_type: str
    damage: int


@dataclass(frozen=True, slots=True)
class TimelineDeath:
    """A hero death.

    Attributes:
        tick: Tick of the ``DEATH`` entry.
        victim: The hero's NPC name.
        killer: The killing unit's name.
        killer_hero: The hero credited with the kill (``damage_source_name``),
            or ``None`` when no hero is (a tower, creep or neutral).
        reincarnated: ``True`` when the hero came back (Aegis, Reincarnation).
        gold_lost: Gold the hero lost on this death (gold reason 1), as a
            positive number.
        recent_damage: Damage the hero took in the recap window before the
            death, largest first.
    """

    tick: int
    victim: str
    killer: str
    killer_hero: str | None
    reincarnated: bool
    gold_lost: int = 0
    recent_damage: tuple[DamageTaken, ...] = ()


@dataclass(frozen=True, slots=True)
class KillRewards:
    """The kill gold and XP paid on a tick with hero deaths.

    The log doesn't say which death a bounty is for, so deaths on the same tick
    share one record.

    Attributes:
        tick: The tick.
        victims: NPC names of the heroes that died on it.
        gold: Hero-kill gold (reason 12) per receiving hero.
        xp: Hero-kill XP (reason 1) per receiving hero.
    """

    tick: int
    victims: tuple[str, ...]
    gold: dict[str, int] = field(default_factory=dict)
    xp: dict[str, int] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class TimelineBuyback:
    """A buyback.

    Attributes:
        tick: Tick of the buyback.
        hero: The hero's NPC name.
        cost: Gold paid (see :class:`gem.BuybackEvent`).
        cost_exact: ``True`` when ``cost`` is the observed spend, ``False`` when
            it is the formula estimate.
    """

    tick: int
    hero: str
    cost: int
    cost_exact: bool


@dataclass(frozen=True, slots=True)
class FightTimeline:
    """A window's combat log as typed records, each list in tick order.

    Times are ticks; use ``match.game_clock`` for game seconds.

    Attributes:
        start_tick: First tick of the window.
        end_tick: Last tick of the window.
        player_ids: Player slot for each hero NPC name in the match.
        casts: Ability and item uses by heroes.
        damage: Damage to heroes, in short bursts.
        modifiers: Modifiers on heroes (buffs, debuffs, stuns, auras).
        deaths: Hero deaths.
        rewards: Kill gold and XP, one record per tick with deaths.
        buybacks: Buybacks.
    """

    start_tick: int
    end_tick: int
    player_ids: dict[str, int]
    casts: tuple[TimelineCast, ...] = ()
    damage: tuple[DamageBurst, ...] = ()
    modifiers: tuple[ModifierWindow, ...] = ()
    deaths: tuple[TimelineDeath, ...] = ()
    rewards: tuple[KillRewards, ...] = ()
    buybacks: tuple[TimelineBuyback, ...] = ()

    @property
    def disables(self) -> tuple[ModifierWindow, ...]:
        """The modifiers that stunned (``stun_s > 0``)."""
        return tuple(window for window in self.modifiers if window.stun_s > 0)

    def rewards_at(self, tick: int) -> KillRewards | None:
        """The kill rewards paid on ``tick``, or ``None``."""
        return next((rewards for rewards in self.rewards if rewards.tick == tick), None)


def modifier_matches_ability(modifier: str, ability: str) -> bool:
    """Whether a modifier name looks like it came from an ability or item.

    True for the same name, or a ``modifier_`` name that contains the ability's
    name without its ``item_`` prefix (``lion_voodoo`` and
    ``modifier_lion_voodoo``; ``item_sheepstick`` and
    ``modifier_sheepstick_debuff``). This is a naming convention, not a fact
    in the log, so a modifier named differently from its ability is missed.

    Args:
        modifier: Modifier name from a ``MODIFIER_ADD`` entry.
        ability: Ability or item name from an ``ABILITY`` / ``ITEM`` entry.

    Returns:
        Whether they match.
    """
    if not modifier or not ability:
        return False
    if modifier == ability:
        return True
    key = ability.removeprefix("item_")
    return modifier.startswith("modifier_") and key in modifier


def build_fight_timeline(
    match: ParsedMatch,
    start_tick: int,
    end_tick: int,
    *,
    hit_window_ticks: int = 90,
    recap_ticks: int = 300,
    burst_ticks: int = 15,
) -> FightTimeline:
    """Turn the combat log between two ticks into a fight's typed records.

    For a detected fight, pass its window:
    ``build_fight_timeline(match, fight.start_tick, fight.end_tick)``.

    Rules:

    * **Heroes** are the match's player heroes; illusions are not heroes. Casts
      by illusions are left out; their damage is kept, credited to the owner.
    * **Hits** (derived): a ``DAMAGE`` or ``MODIFIER_ADD`` entry credited to
      the caster (``damage_source_name``, so it may come from a unit the hero
      controls, but not from an illusion) on a hero belongs to the caster's
      latest cast at most
      ``hit_window_ticks`` earlier whose ability is the entry's inflictor (for
      a modifier, :func:`modifier_matches_ability`). Each entry goes to at most
      one cast, so no damage is counted twice. Damage that matches no cast
      (attacks, passives, damage over time after the window) is only in
      ``damage``.
    * **Damage** covers every ``DAMAGE`` entry on a hero, grouped per attacker,
      target, source and type into bursts: a burst opens at its first entry
      and takes the same stream's entries for ``burst_ticks``. A cast's hit
      damage is a subset of it.
    * **Modifiers** pair each ``MODIFIER_ADD`` on a hero with the next
      ``MODIFIER_REMOVE`` of the same modifier on the same hero.
    * **Deaths** and **rewards** read the ``DEATH`` entries and the ``GOLD`` /
      ``XP`` entries on the same tick.

    Args:
        match: The parsed match.
        start_tick: First tick of the window.
        end_tick: Last tick of the window.
        hit_window_ticks: How long after a cast its ability's damage and
            debuffs count as its hits (default 90, three seconds).
        recap_ticks: How far before a death its ``recent_damage`` reaches
            (default 300, ten seconds). It may reach before ``start_tick``.
        burst_ticks: Length of a ``damage`` burst (default 15, half a second).

    Returns:
        The window's records.

    Raises:
        ValueError: If the window is empty or a tick bound is not positive.
    """
    if end_tick < start_tick:
        raise ValueError(f"end_tick {end_tick} is before start_tick {start_tick}")
    if hit_window_ticks < 0 or recap_ticks < 0 or burst_ticks <= 0:
        raise ValueError("hit_window_ticks and recap_ticks must be >= 0, burst_ticks > 0")

    player_ids = {p.hero_name: p.player_id for p in match.players if p.hero_name}
    log = match.combat_log
    ticks = [entry.tick for entry in log]
    lo = bisect.bisect_left(ticks, start_tick)
    hi = bisect.bisect_right(ticks, end_tick)
    window = log[lo:hi]

    def is_hero(name: str, illusion: bool) -> bool:
        return name in player_ids and not illusion

    def credited(entry: CombatLogEntry) -> str | None:
        if entry.damage_source_name in player_ids:
            return entry.damage_source_name
        if entry.attacker_name in player_ids:
            return entry.attacker_name
        return None

    casts = _casts(window, is_hero, credited, hit_window_ticks)
    deaths, rewards = _deaths(log, ticks, window, is_hero, credited, recap_ticks)
    buybacks = sorted(
        (
            TimelineBuyback(b.tick, p.hero_name, b.cost, b.cost_exact)
            for p in match.players
            for b in p.buybacks
            if start_tick <= b.tick <= end_tick
        ),
        key=lambda b: b.tick,
    )
    return FightTimeline(
        start_tick=start_tick,
        end_tick=end_tick,
        player_ids=player_ids,
        casts=tuple(casts),
        damage=tuple(_damage(window, is_hero, credited, burst_ticks)),
        modifiers=tuple(_modifiers(window, is_hero, credited)),
        deaths=tuple(deaths),
        rewards=tuple(rewards),
        buybacks=tuple(buybacks),
    )


class _HitTally:
    __slots__ = ("damage", "damage_type", "modifiers", "stun_s")

    def __init__(self) -> None:
        self.damage = 0
        self.damage_type = ""
        self.stun_s = 0.0
        self.modifiers: list[str] = []

    def freeze(self, hero: str) -> CastHit:
        return CastHit(hero, self.damage, self.damage_type, self.stun_s, tuple(self.modifiers))


def _casts(
    window: Sequence[CombatLogEntry], is_hero: _IsHero, credited: _Credited, hit_window_ticks: int
) -> list[TimelineCast]:
    casts: list[CombatLogEntry] = []
    by_caster: dict[str, list[int]] = defaultdict(list)
    for entry in window:
        if entry.log_type in ("ABILITY", "ITEM") and is_hero(
            entry.attacker_name, entry.attacker_is_illusion
        ):
            by_caster[entry.attacker_name].append(len(casts))
            casts.append(entry)

    tallies: list[dict[str, _HitTally]] = [{} for _ in casts]
    for entry in window:
        if entry.log_type not in ("DAMAGE", "MODIFIER_ADD"):
            continue
        if entry.attacker_is_illusion or not is_hero(entry.target_name, entry.target_is_illusion):
            continue
        is_damage = entry.log_type == "DAMAGE"
        # The credited hero, so a summon or other unit carrying the hero's
        # ability (``damage_source_name``) still finds the hero's cast.
        caster = credited(entry)
        for index in reversed(by_caster.get(caster, ()) if caster else ()):
            cast = casts[index]
            if cast.tick > entry.tick:
                continue
            if entry.tick - cast.tick > hit_window_ticks:
                break
            if (is_damage and entry.inflictor_name == cast.inflictor_name) or (
                not is_damage
                and modifier_matches_ability(entry.inflictor_name, cast.inflictor_name)
            ):
                tally = tallies[index].setdefault(entry.target_name, _HitTally())
                if is_damage:
                    tally.damage += entry.value
                    tally.damage_type = tally.damage_type or entry.damage_type
                else:
                    tally.modifiers.append(entry.inflictor_name)
                    tally.stun_s = max(tally.stun_s, entry.stun_duration or 0.0)
                break

    out = []
    for cast, by_hero in zip(casts, tallies, strict=True):
        caster = cast.attacker_name
        target = cast.target_name or None
        out.append(
            TimelineCast(
                tick=cast.tick,
                caster=caster,
                ability=cast.inflictor_name,
                is_item=cast.log_type == "ITEM",
                level=cast.ability_level,
                target=target,
                target_is_hero=target is not None and is_hero(target, cast.target_is_illusion),
                hits=tuple(t.freeze(hero) for hero, t in by_hero.items() if hero != caster),
                self_effect=by_hero[caster].freeze(caster) if caster in by_hero else None,
            )
        )
    return out


def _damage(
    window: Sequence[CombatLogEntry], is_hero: _IsHero, credited: _Credited, burst_ticks: int
) -> list[DamageBurst]:
    # A burst opens at its first entry and takes the same stream's entries for
    # ``burst_ticks``, like ``group_ability_hits`` anchors a cast on its first hit.
    bursts: list[list] = []
    open_burst: dict[tuple[str, bool, str, str, str], int] = {}
    for entry in window:
        if entry.log_type != "DAMAGE" or not is_hero(entry.target_name, entry.target_is_illusion):
            continue
        key = (
            entry.attacker_name,
            entry.attacker_is_illusion,
            entry.target_name,
            entry.inflictor_name,
            entry.damage_type,
        )
        index = open_burst.get(key)
        if index is not None and entry.tick - bursts[index][0] < burst_ticks:
            burst = bursts[index]
            burst[1] = entry.tick
            burst[3] += entry.value
            burst[4] += 1
        else:
            open_burst[key] = len(bursts)
            bursts.append([entry.tick, entry.tick, credited(entry), entry.value, 1, key])
    return [
        DamageBurst(
            start_tick=first,
            end_tick=last,
            attacker=attacker,
            attacker_is_illusion=illusion,
            attacker_hero=hero,
            target=target,
            source=source,
            damage_type=damage_type,
            damage=damage,
            hits=hits,
        )
        for first, last, hero, damage, hits, (
            attacker,
            illusion,
            target,
            source,
            damage_type,
        ) in bursts
    ]


def _modifiers(
    window: Sequence[CombatLogEntry], is_hero: _IsHero, credited: _Credited
) -> list[ModifierWindow]:
    out: list[ModifierWindow] = []
    open_adds: dict[tuple[str, str], deque[int]] = defaultdict(deque)
    for entry in window:
        if entry.log_type not in ("MODIFIER_ADD", "MODIFIER_REMOVE"):
            continue
        if not is_hero(entry.target_name, entry.target_is_illusion):
            continue
        key = (entry.target_name, entry.inflictor_name)
        if entry.log_type == "MODIFIER_ADD":
            open_adds[key].append(len(out))
            out.append(
                ModifierWindow(
                    target=entry.target_name,
                    modifier=entry.inflictor_name,
                    source=entry.attacker_name,
                    source_hero=credited(entry),
                    start_tick=entry.tick,
                    end_tick=None,
                    duration_s=entry.modifier_duration_s,
                    stun_s=entry.stun_duration or 0.0,
                    aura=entry.aura_modifier,
                )
            )
        elif open_adds[key]:
            index = open_adds[key].popleft()
            added = out[index]
            out[index] = ModifierWindow(
                added.target,
                added.modifier,
                added.source,
                added.source_hero,
                added.start_tick,
                entry.tick,
                added.duration_s,
                added.stun_s,
                added.aura,
            )
        else:
            out.append(
                ModifierWindow(
                    target=entry.target_name,
                    modifier=entry.inflictor_name,
                    source=entry.attacker_name,
                    source_hero=credited(entry),
                    start_tick=None,
                    end_tick=entry.tick,
                )
            )
    out.sort(key=lambda window: window.start_tick if window.start_tick is not None else -1)
    return out


def _deaths(
    log: Sequence[CombatLogEntry],
    ticks: Sequence[int],
    window: Sequence[CombatLogEntry],
    is_hero: _IsHero,
    credited: _Credited,
    recap_ticks: int,
) -> tuple[list[TimelineDeath], list[KillRewards]]:
    death_entries = [
        entry
        for entry in window
        if entry.log_type == "DEATH" and is_hero(entry.target_name, entry.target_is_illusion)
    ]
    on_tick: dict[int, list[CombatLogEntry]] = defaultdict(list)
    for tick in {entry.tick for entry in death_entries}:
        start = bisect.bisect_left(ticks, tick)
        end = bisect.bisect_right(ticks, tick)
        on_tick[tick] = [entry for entry in log[start:end] if entry.log_type in ("GOLD", "XP")]

    deaths = []
    for entry in death_entries:
        victim = entry.target_name
        lost = sum(
            e.value
            for e in on_tick[entry.tick]
            if e.log_type == "GOLD"
            and e.gold_reason == GOLD_REASON_DEATH
            and e.target_name == victim
        )
        start = bisect.bisect_left(ticks, entry.tick - recap_ticks)
        end = bisect.bisect_right(ticks, entry.tick)
        taken: dict[tuple[str, bool, str | None, str, str], int] = defaultdict(int)
        for e in log[start:end]:
            if e.log_type == "DAMAGE" and e.target_name == victim and not e.target_is_illusion:
                key = (
                    e.attacker_name,
                    e.attacker_is_illusion,
                    credited(e),
                    e.inflictor_name,
                    e.damage_type,
                )
                taken[key] += e.value
        recent = sorted(
            (DamageTaken(*key, damage) for key, damage in taken.items()),
            key=lambda d: -d.damage,
        )
        deaths.append(
            TimelineDeath(
                tick=entry.tick,
                victim=victim,
                killer=entry.attacker_name,
                killer_hero=credited(entry),
                reincarnated=bool(entry.will_reincarnate),
                gold_lost=-lost,
                recent_damage=tuple(recent),
            )
        )

    rewards = []
    for tick in sorted(on_tick):
        gold: dict[str, int] = defaultdict(int)
        xp: dict[str, int] = defaultdict(int)
        for e in on_tick[tick]:
            if e.log_type == "GOLD" and e.gold_reason == GOLD_REASON_HERO_KILL:
                gold[e.target_name] += e.value
            elif e.log_type == "XP" and e.xp_reason == XP_REASON_HERO_KILL:
                xp[e.target_name] += e.value
        victims = tuple(d.target_name for d in death_entries if d.tick == tick)
        rewards.append(KillRewards(tick, victims, dict(gold), dict(xp)))
    return deaths, rewards
