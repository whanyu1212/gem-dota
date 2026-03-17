"""Per-player combat log aggregation for gem replay parsing.

Accumulates combat log entries into per-player buckets during a parse,
producing the damage, healing, ability use, gold/XP reason, kill, purchase,
rune, and buyback tallies that populate ``ParsedPlayer``.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from gem.combatlog import CombatLogEntry
    from gem.extractors.players import PlayerExtractor


# ---------------------------------------------------------------------------
# Per-player mutable accumulator
# ---------------------------------------------------------------------------


def _int_counter() -> defaultdict[str, int]:
    return defaultdict(int)


@dataclass(slots=True)
class _ParsedPlayerAgg:
    """Mutable accumulator for per-player combat log aggregates."""

    damage: defaultdict[str, int] = field(default_factory=_int_counter)
    damage_taken: defaultdict[str, int] = field(default_factory=_int_counter)
    damage_by_type: defaultdict[str, int] = field(default_factory=_int_counter)
    damage_taken_by_type: defaultdict[str, int] = field(default_factory=_int_counter)
    healing: defaultdict[str, int] = field(default_factory=_int_counter)
    ability_uses: defaultdict[str, int] = field(default_factory=_int_counter)
    item_uses: defaultdict[str, int] = field(default_factory=_int_counter)
    gold_reasons: defaultdict[str, int] = field(default_factory=_int_counter)
    xp_reasons: defaultdict[str, int] = field(default_factory=_int_counter)
    kills_log: list[CombatLogEntry] = field(default_factory=list)
    purchase_log: list[CombatLogEntry] = field(default_factory=list)
    runes_log: list[CombatLogEntry] = field(default_factory=list)
    buyback_log: list[CombatLogEntry] = field(default_factory=list)
    stuns_dealt: float = 0.0


# ---------------------------------------------------------------------------
# Purchase log deduplication
# ---------------------------------------------------------------------------


def _dedup_purchase_log(
    entries: list[CombatLogEntry],
    first_snap_tick: int | None,
    sample_interval: int,
) -> list[CombatLogEntry]:
    """Deduplicate purchase log entries within the starting inventory window.

    The inventory snapshot and the combat log stream may both emit PURCHASE
    entries for the same item within the first sample window.  Outside that
    window, duplicate item purchases are legitimate (e.g. buying two separate
    Branches) and are kept as-is.

    Args:
        entries: Raw purchase log entries (unsorted).
        first_snap_tick: Tick of the player's first inventory snapshot, or
            ``None`` if no snapshot was taken.
        sample_interval: Width of the starting-item window in ticks.

    Returns:
        Deduplicated list sorted by tick.
    """
    if first_snap_tick is None:
        return sorted(entries, key=lambda e: e.tick)

    cutoff = first_snap_tick + sample_interval
    seen: set[tuple] = set()
    result = []
    for entry in sorted(entries, key=lambda e: e.tick):
        if entry.tick <= cutoff:
            key = (entry.tick, entry.value_name)
            if key in seen:
                continue
            seen.add(key)
        result.append(entry)
    return result


# ---------------------------------------------------------------------------
# Aggregator
# ---------------------------------------------------------------------------


class _CombatAggregator:
    """Aggregates combat log entries into per-player buckets.

    Uses the hero NPC-name → player_id mapping from ``PlayerExtractor``.

    Args:
        player_ext: Attached ``PlayerExtractor`` instance.
    """

    def __init__(self, player_ext: PlayerExtractor) -> None:
        self._player_ext = player_ext
        self.players: dict[int, _ParsedPlayerAgg] = {}

    def _agg(self, player_id: int) -> _ParsedPlayerAgg:
        if player_id not in self.players:
            self.players[player_id] = _ParsedPlayerAgg()
        return self.players[player_id]

    def _hero_to_pid(self, npc_name: str) -> int | None:
        entity = self._player_ext._heroes_by_npc.get(npc_name.lower())
        if entity is None:
            return None
        pid = entity.get_int32("m_nPlayerID")
        if pid is None:
            pid = entity.get_int32("m_iPlayerID")
        if pid is None or pid < 0:
            return None
        return pid // 2

    def _summon_to_pid(self, npc_name: str) -> int | None:
        """Resolve a summoned unit's NPC name to its owner's player slot.

        Looks up the unit entity by class name in the entity manager, reads
        ``m_hOwnerEntity``, resolves that handle to the owning hero entity,
        and extracts the player slot via ``m_nPlayerID`` / ``m_iPlayerID``.

        Returns ``None`` if the unit is not found, has no owner, or the owner
        is not a tracked hero.

        Args:
            npc_name: The NPC class name as it appears in the combat log,
                e.g. ``"npc_dota_unit_warlock_golem"``.

        Returns:
            Player slot 0-9, or ``None`` if unresolvable.
        """
        parser = self._player_ext._parser
        if parser is None:
            return None
        em = parser.entity_manager
        if em is None:
            return None

        # Find the summon entity by iterating current entities for this class.
        # Combat log names are lowercase; entity class names are CamelCase with
        # a "C" prefix, e.g. "npc_dota_unit_warlock_golem" → not directly
        # searchable by class name. Instead resolve via the entity manager's
        # find_by_class_name if available, else fall back to a cache lookup.
        unit = em.find_by_npc_name(npc_name)
        if unit is None:
            return None

        owner_handle = unit.get_uint32("m_hOwnerEntity")
        if owner_handle is None:
            return None

        owner = em.find_by_handle(owner_handle)
        if owner is None:
            return None

        pid = owner.get_int32("m_nPlayerID")
        if pid is None:
            pid = owner.get_int32("m_iPlayerID")
        if pid is None or pid < 0:
            return None
        return pid // 2

    def on_entry(self, entry: Any) -> None:
        """Process a single combat log entry, routing it to the right bucket.

        Args:
            entry: A ``CombatLogEntry`` instance.
        """
        attacker_pid = self._hero_to_pid(entry.attacker_name) if entry.attacker_is_hero else None
        # Credit summoned unit damage/stuns to the owning hero when the attacker
        # is not a hero itself (Warlock Golem, LD bear, Chen creeps, Pugna ward, etc.)
        # Only applies to DAMAGE/ABILITY/ITEM — not GOLD/XP/RUNE/etc.
        if (
            attacker_pid is None
            and not entry.attacker_is_hero
            and entry.attacker_name
            and entry.log_type in ("DAMAGE", "ABILITY", "ITEM")
        ):
            attacker_pid = self._summon_to_pid(entry.attacker_name)
        target_pid = self._hero_to_pid(entry.target_name) if entry.target_is_hero else None

        # For GOLD/XP/PURCHASE in S2 replays, target_is_hero is False even for
        # hero targets — fall back to name lookup unconditionally for those types.
        if (
            target_pid is None
            and entry.target_name
            and entry.log_type in ("GOLD", "XP", "PURCHASE")
        ):
            target_pid = self._hero_to_pid(entry.target_name)

        if entry.stun_duration > 0 and attacker_pid is not None:
            self._agg(attacker_pid).stuns_dealt += entry.stun_duration

        match entry.log_type:
            case "DAMAGE":
                if attacker_pid is not None:
                    self._agg(attacker_pid).damage[entry.target_name] += entry.value
                    if entry.damage_type:
                        self._agg(attacker_pid).damage_by_type[entry.damage_type] += entry.value
                if target_pid is not None:
                    self._agg(target_pid).damage_taken[entry.attacker_name] += entry.value
                    if entry.damage_type:
                        self._agg(target_pid).damage_taken_by_type[entry.damage_type] += entry.value
            case "HEAL":
                if attacker_pid is not None:
                    self._agg(attacker_pid).healing[entry.target_name] += entry.value
            case "ABILITY":
                if attacker_pid is not None and entry.inflictor_name:
                    self._agg(attacker_pid).ability_uses[entry.inflictor_name] += 1
            case "ITEM":
                if attacker_pid is not None and entry.inflictor_name:
                    self._agg(attacker_pid).item_uses[entry.inflictor_name] += 1
            case "GOLD":
                if target_pid is not None:
                    self._agg(target_pid).gold_reasons[str(entry.gold_reason)] += entry.value
            case "XP":
                if target_pid is not None:
                    self._agg(target_pid).xp_reasons[str(entry.xp_reason)] += entry.value
            case "DEATH":
                if attacker_pid is not None:
                    self._agg(attacker_pid).kills_log.append(entry)
            case "PURCHASE":
                pid = attacker_pid if attacker_pid is not None else target_pid
                if pid is not None:
                    self._agg(pid).purchase_log.append(entry)
            case "PICKUP_RUNE":
                # entry.value = player slot (from CDOTAUserMsg_ChatEvent.playerid_1)
                pid = entry.value
                if 0 <= pid < 10:
                    self._agg(pid).runes_log.append(entry)
            case "BUYBACK":
                # Populated via post-processing in match_builder after full name map is built.
                pass
