"""Per-player combat log aggregation for gem replay parsing.

Accumulates combat log entries into per-player buckets during a parse,
producing the damage, healing, ability use, gold/XP reason, kill, purchase,
rune, and buyback tallies that populate ``ParsedPlayer``.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from gem.combat.log import CombatLogType, opendota_translate
from gem.extractors._snapshots import _player_id_from_entity

if TYPE_CHECKING:
    from gem.combat.log import CombatLogEntry
    from gem.extractors.players import PlayerExtractor


# ---------------------------------------------------------------------------
# Per-player mutable accumulator
# ---------------------------------------------------------------------------


def _int_counter() -> defaultdict[str, int]:
    return defaultdict(int)


def _nested_int_counter() -> defaultdict[str, defaultdict[str, int]]:
    """Two-level ``str -> str -> int`` counter for inflictor×target breakdowns."""
    return defaultdict(_int_counter)


def _inflictor_key(inflictor_name: str) -> str | None:
    """Translate an inflictor name to its OpenDota dict-key form.

    Like :func:`opendota_translate` but maps the empty/no-inflictor case
    (auto-attacks) to the literal key ``"null"`` — OpenDota emits a JSON ``null``
    inflictor that becomes the object key ``"null"`` once stringified. Returns
    ``None`` only for ``dota_unknown`` (which OpenDota drops entirely).

    Args:
        inflictor_name: The raw combat-log ``inflictor_name``.

    Returns:
        The OpenDota key (``"null"`` for auto-attacks), or ``None`` to skip.
    """
    translated = opendota_translate(inflictor_name)
    if translated is None:
        return None
    return translated or "null"


def _illusion_key(name: str, is_illusion: bool) -> str:
    """Prefix a unit name with ``illusion_`` when it is an illusion.

    Mirrors OpenDota's ``computeIllusionString`` so the per-target ``damage`` /
    ``healing`` dict keys match its reconstruction (an illusion's damage is keyed
    separately from the real hero's).

    Args:
        name: The unit NPC name.
        is_illusion: Whether the unit is an illusion.

    Returns:
        ``"illusion_" + name`` when ``is_illusion`` is true, else ``name``.
    """
    return f"illusion_{name}" if is_illusion else name


def _is_unit_target(name: str) -> bool:
    """Return whether a combat-log target name denotes a real unit/building.

    Valve occasionally logs damage against an ability/modifier name
    (e.g. ``"nevermore_necromastery"``) rather than a unit; OpenDota's per-target
    ``damage`` dict excludes these. A real target starts with ``npc_`` (units,
    creeps, buildings) or ``dota_`` (e.g. ``dota_fountain``).

    Args:
        name: The combat-log ``target_name``.

    Returns:
        True if ``name`` is a unit/building target.
    """
    return name.startswith("npc_") or name.startswith("dota_")


@dataclass(slots=True)
class _ParsedPlayerAgg:
    """Mutable accumulator for per-player combat log aggregates."""

    damage: defaultdict[str, int] = field(default_factory=_int_counter)
    damage_taken: defaultdict[str, int] = field(default_factory=_int_counter)
    damage_by_type: defaultdict[str, int] = field(default_factory=_int_counter)
    damage_taken_by_type: defaultdict[str, int] = field(default_factory=_int_counter)
    # OpenDota per-inflictor / per-target attribution breakdowns, all keyed on the
    # translated inflictor name (item_ prefix stripped). Populated only for damage
    # against an enemy hero (non-illusion), matching CreateParsedDataBlob.
    # handleDamageCombat / handleAbility gating. damage_targets/ability_targets are
    # nested inflictor -> {target_hero: value/count}; damage_inflictor and
    # damage_inflictor_received are flat inflictor -> value; hero_hits counts
    # instances (not summed damage); max_hero_hit holds the single largest hit.
    damage_inflictor: defaultdict[str, int] = field(default_factory=_int_counter)
    damage_inflictor_received: defaultdict[str, int] = field(default_factory=_int_counter)
    damage_targets: defaultdict[str, defaultdict[str, int]] = field(
        default_factory=_nested_int_counter
    )
    ability_targets: defaultdict[str, defaultdict[str, int]] = field(
        default_factory=_nested_int_counter
    )
    hero_hits: defaultdict[str, int] = field(default_factory=_int_counter)
    max_hero_hit: dict[str, Any] | None = None
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
    # OpenDota-style combat scalars reconstructed from the combat log by
    # crediting the damage *source* (see _accumulate_hero_tower_damage). Assembly
    # uses these as a fallback, then overlays exact Game Coordinator values from
    # the replay-embedded CMsgDOTAMatch postgame summary when available.
    hero_damage: int = 0
    tower_damage: int = 0
    hero_healing: int = 0


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
        return _player_id_from_entity(entity)

    def _summon_to_pid(self, npc_name: str) -> int | None:
        """Resolve a summoned unit's NPC name to its owner's player slot.

        Looks up the unit entity by class name in the entity manager, reads
        ``m_hOwnerEntity``, resolves that handle to the owning hero entity,
        and extracts the player slot via :func:`_player_id_from_entity`.

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
        return _player_id_from_entity(owner)

    def resolve_kill_pid(self, source_name: str, attacker_name: str) -> int | None:
        """Resolve the crediting player for a DEATH, source-first.

        Mirrors the DEATH-branch attribution used for the native ``kills_log`` so
        objective kills (towers, Roshan, courier) attribute the same way: the
        ``damage_source_name`` hero is preferred (a summon or projectile carries
        the owning hero there even when ``attacker_name`` is the non-hero unit),
        then the attacker hero, then the attacker's summon owner.

        Args:
            source_name: The combat-log ``damage_source_name`` (may be empty).
            attacker_name: The combat-log ``attacker_name``.

        Returns:
            The crediting player's slot 0-9, or ``None`` if unresolvable.
        """
        if source_name:
            pid = self._hero_to_pid(source_name)
            if pid is not None:
                return pid
        if attacker_name:
            pid = self._hero_to_pid(attacker_name)
            if pid is not None:
                return pid
            return self._summon_to_pid(attacker_name)
        return None

    def _accumulate_hero_tower_damage(self, source_pid: int, entry: Any) -> None:
        """Add one DAMAGE entry to the source hero's hero_damage / tower_damage.

        Mirrors OpenDota's reconstruction (``CreateParsedDataBlob.handleDamageCombat``
        + ``expand``): damage is credited to the *source* unit
        (``damage_source_name``), not the attacker — so a hero's spell / projectile
        damage (where the attacker is the projectile) lands on the hero.
        ``hero_damage`` counts source-attributed damage to a non-illusion hero
        target; ``tower_damage`` counts damage to any building (tower / barracks /
        fort). Illusion-dealt damage is folded into the source hero exactly as
        OpenDota does (``unit = e.sourcename`` resolved via ``hero_to_slot``; the
        combat log carries no illusion marker on the source name), keeping the
        scalar consistent with the per-target ``damage`` dict.

        These counters are fallback estimates: the combat log does not expose all
        of the in-engine mitigation and illusion accounting represented by the
        headline Game Coordinator values. Match assembly overlays exact values
        from the replay-embedded ``CMsgDOTAMatch`` summary when present; explicit
        API enrichment can overwrite them as well.

        Args:
            source_pid: The resolved damage-source player slot 0-9.
            entry: A DAMAGE ``CombatLogEntry``.
        """
        target = entry.target_name or ""
        if entry.target_is_hero and not entry.target_is_illusion:
            self._agg(source_pid).hero_damage += entry.value
        elif any(s in target for s in ("_tower", "_rax", "_fort")):
            # OpenDota's tower_damage counts all building damage (towers,
            # barracks, fort/ancient), not just towers.
            self._agg(source_pid).tower_damage += entry.value

    def _accumulate_inflictor_damage(
        self,
        source_pid: int,
        target_pid: int | None,
        source_unit: str,
        entry: Any,
    ) -> None:
        """Add one hero-target DAMAGE entry to the OpenDota inflictor breakdowns.

        Implements ``CreateParsedDataBlob.handleDamageCombat``'s inflictor block,
        which the caller has already gated on the target being a non-illusion hero
        and the source being resolved. All keys use the translated inflictor name
        (``item_`` stripped); ``dota_unknown`` (auto-attacks) is dropped.

        ``damage_targets`` (inflictor→{target:dmg}) and ``hero_hits``
        (inflictor→hit count) are always recorded. ``damage_inflictor``,
        ``max_hero_hit`` and ``damage_inflictor_received`` are additionally gated on
        the damage not being self-inflicted (OpenDota's ``!key.equals(unit)``):
        ``damage_inflictor_received`` is the victim-side mirror, recorded only when
        the *source* is an enemy hero.

        Args:
            source_pid: The resolved damage-source player slot 0-9.
            target_pid: The resolved target hero's player slot, or ``None``.
            source_unit: The crediting source unit name (OpenDota ``unit``).
            entry: A DAMAGE ``CombatLogEntry`` against a non-illusion hero.
        """
        inflictor = _inflictor_key(entry.inflictor_name)
        if inflictor is None:
            return
        target_key = _illusion_key(entry.target_name, entry.target_is_illusion)
        src = self._agg(source_pid)
        translated_target = opendota_translate(entry.target_name) or entry.target_name
        src.damage_targets[inflictor][translated_target] += entry.value
        src.hero_hits[inflictor] += 1

        # Self-damage gate: OpenDota skips damage_inflictor / max_hero_hit /
        # damage_inflictor_received when the (illusion-keyed) target is the source.
        if target_key == source_unit:
            return
        src.damage_inflictor[inflictor] += entry.value
        if src.max_hero_hit is None or entry.value > src.max_hero_hit["value"]:
            src.max_hero_hit = {
                "type": "max_hero_hit",
                "time": entry.game_time_s if entry.game_time_s is not None else entry.timestamp_s,
                "max": True,
                "inflictor": inflictor,
                "unit": source_unit,
                "key": target_key,
                "value": entry.value,
            }
        # damage_inflictor_received is keyed on the victim and recorded only when an
        # enemy hero dealt the damage (OpenDota: source contains "npc_dota_hero_").
        if target_pid is not None and "npc_dota_hero_" in source_unit:
            self._agg(target_pid).damage_inflictor_received[inflictor] += entry.value

    def _is_self_death(self, entry: Any) -> bool:
        """Return whether a DEATH entry is a self-kill OpenDota would ignore."""
        if not entry.target_name:
            return False
        return entry.attacker_name == _illusion_key(entry.target_name, entry.target_is_illusion)

    def on_entry(self, entry: Any) -> None:
        """Process a single combat log entry, routing it to the right bucket.

        Args:
            entry: A ``CombatLogEntry`` instance.
        """
        attacker_pid = self._hero_to_pid(entry.attacker_name) if entry.attacker_is_hero else None
        source_name = getattr(entry, "damage_source_name", "") or ""
        # Resolve summon ownership for ability/item uses, positive stuns, and
        # damage without a source name. Sourced damage does not otherwise use
        # the owner slot, even when the source is not a hero. DEATH has separate
        # source-first attribution below.
        if (
            attacker_pid is None
            and not entry.attacker_is_hero
            and entry.attacker_name
            and entry.log_type in ("DAMAGE", "ABILITY", "ITEM")
            and (
                entry.log_type != CombatLogType.DAMAGE or not source_name or entry.stun_duration > 0
            )
        ):
            attacker_pid = self._summon_to_pid(entry.attacker_name)

        # OpenDota attributes the per-target damage/healing dicts and the
        # hero_damage/tower_damage scalars, plus the killed/kills_log streams, to
        # the *source* unit
        # (``damage_source_name``), not the attacker — so a hero's spell /
        # projectile damage (where the attacker is the projectile) lands on the
        # hero. For DAMAGE/HEAL, attribution is strictly to the source *hero*: a
        # summon's own damage stays under the summon's name and is NOT rolled up
        # to the owner, matching OpenDota's reconstruction (``unit =
        # e.sourcename``, see CreateParsedDataBlob.handleDamageCombat). For
        # DEATH, the same source-first rule closes summon kill attribution for
        # transient units such as Beastmaster boars and Brewmaster split units.
        # When the source name is empty (auto-attack: source == attacker), fall
        # back to the attacker slot.
        if source_name:
            source_pid = self._hero_to_pid(source_name)
            source_unit = source_name
        else:
            source_pid = attacker_pid
            source_unit = entry.attacker_name

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
            case CombatLogType.DAMAGE:
                # Skip entries whose target is an ability/modifier name rather than
                # a real unit (Valve logs some absorb/redirect interactions this
                # way); OpenDota's per-target damage dict excludes them.
                if source_pid is not None and _is_unit_target(entry.target_name):
                    # Key by the illusion-prefixed target so an illusion's damage
                    # is tallied separately from the real hero (OpenDota parity).
                    dmg_key = _illusion_key(entry.target_name, entry.target_is_illusion)
                    self._agg(source_pid).damage[dmg_key] += entry.value
                    if entry.damage_type:
                        self._agg(source_pid).damage_by_type[entry.damage_type] += entry.value
                    self._accumulate_hero_tower_damage(source_pid, entry)
                # damage_taken: only for non-illusion hero targets, keyed by the
                # raw source unit (OpenDota does not illusion-prefix the source).
                if target_pid is not None and not entry.target_is_illusion:
                    self._agg(target_pid).damage_taken[source_unit] += entry.value
                    if entry.damage_type:
                        self._agg(target_pid).damage_taken_by_type[entry.damage_type] += entry.value
                # Per-inflictor / per-target breakdowns fire only for damage dealt
                # to an enemy hero (non-illusion), matching OpenDota's gating.
                if source_pid is not None and entry.target_is_hero and not entry.target_is_illusion:
                    self._accumulate_inflictor_damage(source_pid, target_pid, source_unit, entry)
            case CombatLogType.HEAL:
                if source_pid is not None and _is_unit_target(entry.target_name):
                    heal_key = _illusion_key(entry.target_name, entry.target_is_illusion)
                    self._agg(source_pid).healing[heal_key] += entry.value
                    # OpenDota hero_healing: healing to a hero other than oneself.
                    if (
                        entry.target_is_hero
                        and not entry.target_is_illusion
                        and entry.target_name != source_unit
                    ):
                        self._agg(source_pid).hero_healing += entry.value
            case CombatLogType.ABILITY:
                if attacker_pid is not None and entry.inflictor_name:
                    self._agg(attacker_pid).ability_uses[entry.inflictor_name] += 1
                    # ability_targets: ability -> {target_hero: count}, credited to
                    # the caster, only when the target is an enemy hero (non-illusion).
                    if entry.target_is_hero and not entry.target_is_illusion and entry.target_name:
                        ability = opendota_translate(entry.inflictor_name)
                        target = opendota_translate(entry.target_name)
                        if ability is not None and target is not None:
                            self._agg(attacker_pid).ability_targets[ability][target] += 1
            case CombatLogType.ITEM:
                if attacker_pid is not None and entry.inflictor_name:
                    self._agg(attacker_pid).item_uses[entry.inflictor_name] += 1
            case CombatLogType.GOLD:
                if target_pid is not None:
                    self._agg(target_pid).gold_reasons[str(entry.gold_reason)] += entry.value
            case CombatLogType.XP:
                if target_pid is not None:
                    self._agg(target_pid).xp_reasons[str(entry.xp_reason)] += entry.value
            case CombatLogType.DEATH:
                # OpenDota's DOTA_COMBATLOG_DEATH expansion uses sourcename as
                # the killing unit and ignores self-kills. This is crucial for
                # multi-summon heroes: their transient units often appear as the
                # attacker, while damage_source_name is the owning hero.
                if self._is_self_death(entry):
                    return
                death_pid = source_pid if source_pid is not None else attacker_pid
                if death_pid is None and not entry.attacker_is_hero and entry.attacker_name:
                    death_pid = self._summon_to_pid(entry.attacker_name)
                if death_pid is not None:
                    self._agg(death_pid).kills_log.append(entry)
            case CombatLogType.PURCHASE:
                pid = attacker_pid if attacker_pid is not None else target_pid
                if pid is not None:
                    self._agg(pid).purchase_log.append(entry)
            case CombatLogType.PICKUP_RUNE:
                # entry.value = player slot (from CDOTAUserMsg_ChatEvent.playerid_1)
                pid = entry.value
                if 0 <= pid < 10:
                    self._agg(pid).runes_log.append(entry)
            case CombatLogType.BUYBACK:
                # Populated via post-processing in match_builder after full name map is built.
                pass
