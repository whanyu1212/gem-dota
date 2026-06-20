"""Combat log ingestion for Dota 2 Source 2 replays.

Handles two ingestion paths:
- S1 (legacy): ``dota_combatlog`` game event via ``CMsgSource1LegacyGameEvent``.
  Names are integer indices resolved via the ``CombatLogNames`` string table.
- S2 (modern): ``CDOTAUserMsg_CombatLogBulkData`` user message with name
  indices also resolved via ``CombatLogNames``.

Both paths produce the same ``CombatLogEntry`` output.

Reference: clarity/CombatLog.java, odota/Parse.java
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Any

# ---------------------------------------------------------------------------
# Combat log type constants
# ---------------------------------------------------------------------------

# Sentinel proto_id for surfaced labels with no decoded wire type.
_NO_PROTO_ID = -1


class CombatLogType(str, Enum):
    """The combat-log entry types this parser surfaces.

    Subclasses ``(str, Enum)`` so members compare equal to their string label
    (``CombatLogType.DAMAGE == "DAMAGE"``), work in ``in (...)`` membership
    checks, and match ``case "DAMAGE":`` patterns — keeping the historical
    string-based API backward compatible while adding type safety. (``StrEnum``
    would be cleaner but is Python 3.11+; the project floor is 3.10.)

    Each member also carries ``proto_id`` — the ``DOTA_COMBATLOG_TYPES`` integer
    from the replay wire format — so the int→label mapping and the legacy
    ``COMBAT_LOG_TYPES`` frozenset both derive from this single source of truth.
    Members emitted only from derived paths (not decoded from a wire type) use
    ``proto_id = _NO_PROTO_ID`` and are excluded from the int→label mapping.

    Reference: refs/manta/dota/dota_shared_enums.proto ``DOTA_COMBATLOG_TYPES``.
    Note: proto types 7 (LOCATION) and 9 (GAME_STATE) are intentionally not
    surfaced.
    """

    # __str__ from Enum would render "CombatLogType.DAMAGE"; restore str's so
    # str(member) == "DAMAGE" (f-strings already use str.__format__).
    __str__ = str.__str__

    proto_id: int

    def __new__(cls, label: str, proto_id: int) -> CombatLogType:
        member = str.__new__(cls, label)
        member._value_ = label
        member.proto_id = proto_id
        return member

    DAMAGE = ("DAMAGE", 0)
    HEAL = ("HEAL", 1)
    MODIFIER_ADD = ("MODIFIER_ADD", 2)
    MODIFIER_REMOVE = ("MODIFIER_REMOVE", 3)
    DEATH = ("DEATH", 4)
    ABILITY = ("ABILITY", 5)
    ITEM = ("ITEM", 6)
    GOLD = ("GOLD", 8)
    XP = ("XP", 10)
    PURCHASE = ("PURCHASE", 11)
    BUYBACK = ("BUYBACK", 12)
    NEUTRAL_CAMP_STACK = ("NEUTRAL_CAMP_STACK", 20)
    PICKUP_RUNE = ("PICKUP_RUNE", 21)
    # Surfaced label without a wire type we decode: KILLSTREAK is reported by
    # OpenDota but our pipeline never maps proto type 16, so it stays out of the
    # int→label table (preserving the historical decode behaviour).
    KILLSTREAK = ("KILLSTREAK", _NO_PROTO_ID)


# Backward-compatible frozenset of label strings, derived from the enum.
COMBAT_LOG_TYPES: frozenset[str] = frozenset(t.value for t in CombatLogType)

# Mapping from DOTA_COMBATLOG_TYPES int → enum member, derived from the enum.
# Excludes members with no decoded wire type; unmapped proto types fall back to
# DAMAGE at the call site (preserving the original behaviour).
_LOG_TYPE_NAMES: dict[int, CombatLogType] = {
    t.proto_id: t for t in CombatLogType if t.proto_id != _NO_PROTO_ID
}

# Mapping from CMsgDOTACombatLogEntry.damage_type uint32 → normalized label.
# Despite the HeroDamageType proto enum using 0/1/2, the combat-log wire value
# uses a 1-based scheme: 1=physical, 2=magical, 4=pure.
# Value 0 = field unset (proto default) — occurs for damage against non-hero units
# (wards, creeps, zombies) where Valve does not populate the type field.
# Verified empirically against real replay data.
_DAMAGE_TYPE_NAMES: dict[int, str] = {
    0: "others",
    1: "physical",
    2: "magical",
    4: "pure",
}

# S1 dota_combatlog game event field names (from Clarity S1CombatLogIndices)
_S1_FIELD_TYPE = "type"
_S1_FIELD_TARGET = "targetname"
_S1_FIELD_ATTACKER = "attackername"
_S1_FIELD_SOURCE = "sourcename"
_S1_FIELD_INFLICTOR = "inflictorname"
_S1_FIELD_ATTACKER_ILLUSION = "attackerillusion"
_S1_FIELD_TARGET_ILLUSION = "targetillusion"
_S1_FIELD_ATTACKER_HERO = "attackerhero"
_S1_FIELD_TARGET_HERO = "targethero"
_S1_FIELD_VALUE = "value"
_S1_FIELD_ABILITY_LEVEL = "ability_level"
_S1_FIELD_GOLD_REASON = "gold_reason"
_S1_FIELD_XP_REASON = "xp_reason"


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class CombatLogEntry:
    """One decoded combat log entry.

    Attributes:
        tick: Game tick at which the event occurred.
        log_type: The :class:`CombatLogType` for this entry. Compares equal to
            its string label (e.g. ``log_type == "DAMAGE"``) for backward
            compatibility.
        attacker_name: Name of the attacker unit/hero.
        damage_source_name: Name of the unit credited as the *source* of the
            damage/heal (``damage_source_name`` in the proto). For summon/spell
            damage this is the owning hero even when ``attacker_name`` is the
            summon or projectile. OpenDota attributes the per-target
            ``damage``/``healing`` dicts and the ``hero_damage``/``tower_damage``
            scalars to this field (``unit = e.sourcename``), not ``attacker_name``.
            Empty when the source index is unset. Reference:
            ``parser/Parse.java`` (``sourcename = cle.getDamageSourceName()``).
        target_name: Name of the target unit/hero.
        inflictor_name: Ability or item that caused the event.
        value: Numeric value (damage, heal amount, gold, xp, etc.).
        attacker_is_hero: True if the attacker is a hero.
        target_is_hero: True if the target is a hero.
        attacker_is_illusion: True if the attacker is an illusion.
        target_is_illusion: True if the target is an illusion.
        ability_level: Ability level (for ability/item events).
        gold_reason: Gold reason code (for GOLD events).
        xp_reason: XP reason code (for XP events).
        value_name: Resolved name for the value field (PURCHASE events: item name).
        damage_type: Damage type label for DAMAGE events ("physical", "magical", "pure").
        stun_duration: Duration of stun applied by this event in seconds (S2 only; 0.0 if none).
        neutral_camp_type: Raw neutral camp type from the replay combat log, or 0 if absent.
        neutral_camp_team: Raw neutral camp team from the replay combat log, or 0 if absent.
        location_x: Raw combat-log event x coordinate, or ``None`` if absent.
        location_y: Raw combat-log event y coordinate, or ``None`` if absent.
        timestamp_s: Raw S2 combat-log timestamp in seconds, or ``None`` for S1/derived events.
        game_time_s: OpenDota-style game-relative combat-log time in seconds, or ``None`` when
            the game-start combat-log marker has not been observed.
    """

    tick: int
    log_type: CombatLogType
    attacker_name: str = ""
    damage_source_name: str = ""
    target_name: str = ""
    inflictor_name: str = ""
    value: int = 0
    attacker_is_hero: bool = False
    target_is_hero: bool = False
    attacker_is_illusion: bool = False
    target_is_illusion: bool = False
    ability_level: int = 0
    gold_reason: int = 0
    xp_reason: int = 0
    value_name: str = ""
    damage_type: str = ""
    stun_duration: float = 0.0
    neutral_camp_type: int = 0
    neutral_camp_team: int = 0
    location_x: float | None = None
    location_y: float | None = None
    timestamp_s: float | None = None
    game_time_s: int | None = None


CombatLogHandler = Callable[[CombatLogEntry], None]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _resolve_name(name_table: Any, index: int) -> str:
    """Resolve a name index via the CombatLogNames string table.

    The string table stores items as ``dict[int, (key_str, value_bytes)]``.
    Index 0 means "no name" — return empty string.

    Args:
        name_table: A StringTable object whose ``.items`` is a
            ``dict[int, (str, bytes)]``.
        index: The integer name index from the combat log entry.

    Returns:
        The resolved name string, or empty string if not found.
    """
    if index == 0:
        return ""
    item = name_table.items.get(index)
    if item is None:
        return ""
    key, _ = item
    return key


# ---------------------------------------------------------------------------
# Processor
# ---------------------------------------------------------------------------


class CombatLogProcessor:
    """Parses and dispatches combat log entries.

    Attributes:
        _handlers: Registered CombatLogHandler callables.
    """

    def __init__(self) -> None:
        self._handlers: list[CombatLogHandler] = []

    def on_combat_log_entry(self, handler: CombatLogHandler) -> None:
        """Register a handler to receive decoded CombatLogEntry objects.

        Args:
            handler: Callable ``(CombatLogEntry) -> None``.
        """
        self._handlers.append(handler)

    def process_rune_pickup(self, player_slot: int, rune_type: int, tick: int = 0) -> None:
        """Emit a PICKUP_RUNE CombatLogEntry from a CDOTAUserMsg_ChatEvent.

        Args:
            player_slot: Player slot (0-9) from ChatEvent.playerid_1.
            rune_type: Rune type integer from ChatEvent.value.
            tick: Current game tick.
        """
        entry = CombatLogEntry(
            tick=tick,
            log_type=CombatLogType.PICKUP_RUNE,
            value=player_slot,
            gold_reason=rune_type,
        )
        self._emit(entry)

    def _emit(self, entry: Any) -> None:
        """Dispatch an entry to all registered handlers.

        Args:
            entry: A CombatLogEntry (or any object, for testing).
        """
        for h in self._handlers:
            h(entry)

    def process_s1_event(self, game_event: Any, name_table: Any, tick: int = 0) -> None:
        """Parse a ``dota_combatlog`` S1 game event and emit a CombatLogEntry.

        Names are integer indices resolved via the CombatLogNames string table.

        Args:
            game_event: A ``GameEvent`` object with typed field accessors
                (``get_int32``, ``get_bool``).
            name_table: An object with an ``items`` dict mapping int index →
                ``(key_str, value_bytes)`` for name resolution.
            tick: Current game tick.
        """
        type_val, _ = game_event.get_int32(_S1_FIELD_TYPE)
        log_type = _LOG_TYPE_NAMES.get(type_val, CombatLogType.DAMAGE)

        attacker_idx, _ = game_event.get_int32(_S1_FIELD_ATTACKER)
        source_idx, _ = game_event.get_int32(_S1_FIELD_SOURCE)
        target_idx, _ = game_event.get_int32(_S1_FIELD_TARGET)
        inflictor_idx, _ = game_event.get_int32(_S1_FIELD_INFLICTOR)

        value, _ = game_event.get_int32(_S1_FIELD_VALUE)
        attacker_illusion, _ = game_event.get_bool(_S1_FIELD_ATTACKER_ILLUSION)
        target_illusion, _ = game_event.get_bool(_S1_FIELD_TARGET_ILLUSION)
        attacker_hero, _ = game_event.get_bool(_S1_FIELD_ATTACKER_HERO)
        target_hero, _ = game_event.get_bool(_S1_FIELD_TARGET_HERO)
        ability_level, _ = game_event.get_int32(_S1_FIELD_ABILITY_LEVEL)
        gold_reason, _ = game_event.get_int32(_S1_FIELD_GOLD_REASON)
        xp_reason, _ = game_event.get_int32(_S1_FIELD_XP_REASON)

        entry = CombatLogEntry(
            tick=tick,
            log_type=log_type,
            attacker_name=_resolve_name(name_table, attacker_idx),
            damage_source_name=_resolve_name(name_table, source_idx),
            target_name=_resolve_name(name_table, target_idx),
            inflictor_name=_resolve_name(name_table, inflictor_idx),
            value=value,
            attacker_is_hero=attacker_hero,
            target_is_hero=target_hero,
            attacker_is_illusion=attacker_illusion,
            target_is_illusion=target_illusion,
            ability_level=ability_level,
            gold_reason=gold_reason,
            xp_reason=xp_reason,
        )
        self._emit(entry)

    def process_s2_bulk(self, msg: Any, name_table: Any, tick: int = 0) -> None:
        """Parse a CDOTAUserMsg_CombatLogBulkData and emit CombatLogEntry per entry.

        Args:
            msg: A ``CDOTAUserMsg_CombatLogBulkData`` protobuf message whose
                ``combat_entries`` field is a repeated ``CMsgDOTACombatLogEntry``.
            name_table: String table with ``items`` dict for name resolution.
            tick: Current game tick.
        """
        for entry_msg in msg.combat_entries:
            self.process_s2_entry(entry_msg, name_table, tick=tick)

    def process_s2_entry(
        self,
        msg: Any,
        name_table: Any,
        tick: int = 0,
        game_time_s: int | None = None,
    ) -> None:
        """Parse a CMsgDOTACombatLogEntry and emit a CombatLogEntry.

        Args:
            msg: A ``CMsgDOTACombatLogEntry``-like protobuf message with
                integer name indices and flag attributes.
            name_table: An object with an ``items`` dict mapping int index →
                ``(key_str, value_bytes)`` for name resolution, OR a legacy
                object with a ``get(index, default='')`` method.
            tick: Current game tick.
            game_time_s: Optional game-relative timestamp computed by
                ``ReplayParser`` from the combat-log ``GAME_STATE`` marker.
        """
        log_type = _LOG_TYPE_NAMES.get(msg.type, CombatLogType.DAMAGE)

        # Support both StringTable.items dict and legacy dict-like name_table
        if hasattr(name_table, "items") and isinstance(name_table.items, dict):
            attacker_name = _resolve_name(name_table, msg.attacker_name)
            damage_source_name = _resolve_name(name_table, msg.damage_source_name)
            target_name = _resolve_name(name_table, msg.target_name)
            inflictor_name = _resolve_name(name_table, msg.inflictor_name)
        else:
            attacker_name = name_table.get(msg.attacker_name, "")
            damage_source_name = name_table.get(msg.damage_source_name, "")
            target_name = name_table.get(msg.target_name, "")
            inflictor_name = name_table.get(msg.inflictor_name, "")

        # For PURCHASE events, msg.value is a CombatLogNames index for the item name.
        # Reference: odota/Parse.java cle.getValueName() for DOTA_COMBATLOG_PURCHASE
        value_name = ""
        if log_type == "PURCHASE":
            if hasattr(name_table, "items") and isinstance(name_table.items, dict):
                value_name = _resolve_name(name_table, msg.value)
            elif hasattr(name_table, "get"):
                value_name = name_table.get(msg.value, "")

        # msg.value is proto uint32 but Dota encodes signed values (e.g. gold lost)
        # as two's complement. Reinterpret as signed int32.
        # Reference: clarity-examples/combatlog/Main.java — cle.getValue() < 0 check
        raw_value = msg.value
        value = raw_value if raw_value < 0x80000000 else raw_value - 0x100000000

        stun_duration = msg.stun_duration if msg.HasField("stun_duration") else 0.0
        neutral_camp_type = msg.neutral_camp_type if msg.HasField("neutral_camp_type") else 0
        neutral_camp_team = msg.neutral_camp_team if msg.HasField("neutral_camp_team") else 0
        location_x = msg.location_x if msg.HasField("location_x") else None
        location_y = msg.location_y if msg.HasField("location_y") else None
        timestamp_s = msg.timestamp if hasattr(msg, "timestamp") else None
        damage_type = ""
        if log_type == "DAMAGE" and hasattr(msg, "damage_type"):
            damage_type = _DAMAGE_TYPE_NAMES.get(msg.damage_type, "")
        entry = CombatLogEntry(
            tick=tick,
            log_type=log_type,
            attacker_name=attacker_name,
            damage_source_name=damage_source_name,
            target_name=target_name,
            inflictor_name=inflictor_name,
            value=value,
            attacker_is_hero=msg.is_attacker_hero,
            target_is_hero=msg.is_target_hero,
            attacker_is_illusion=msg.is_attacker_illusion,
            target_is_illusion=msg.is_target_illusion,
            ability_level=msg.ability_level,
            gold_reason=msg.gold_reason,
            xp_reason=msg.xp_reason,
            value_name=value_name,
            damage_type=damage_type,
            stun_duration=stun_duration,
            neutral_camp_type=neutral_camp_type,
            neutral_camp_team=neutral_camp_team,
            location_x=location_x,
            location_y=location_y,
            timestamp_s=timestamp_s,
            game_time_s=game_time_s,
        )
        self._emit(entry)
