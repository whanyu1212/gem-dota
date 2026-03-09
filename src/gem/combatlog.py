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
from typing import Any

# ---------------------------------------------------------------------------
# Combat log type constants
# ---------------------------------------------------------------------------

COMBAT_LOG_TYPES: frozenset[str] = frozenset(
    [
        "DAMAGE",
        "HEAL",
        "MODIFIER_ADD",
        "MODIFIER_REMOVE",
        "DEATH",
        "ABILITY",
        "ITEM",
        "GOLD",
        "XP",
        "PURCHASE",
        "BUYBACK",
        "KILLSTREAK",
    ]
)

# Mapping from DOTA_COMBATLOG_TYPES int → string label
_LOG_TYPE_NAMES: dict[int, str] = {
    0: "DAMAGE",
    1: "HEAL",
    2: "MODIFIER_ADD",
    3: "MODIFIER_REMOVE",
    4: "DEATH",
    5: "ABILITY",
    6: "ITEM",
    7: "GOLD",
    8: "XP",
    9: "PURCHASE",
    10: "BUYBACK",
    11: "KILLSTREAK",
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
        log_type: String label from COMBAT_LOG_TYPES.
        attacker_name: Name of the attacker unit/hero.
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
    """

    tick: int
    log_type: str
    attacker_name: str = ""
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
        log_type = _LOG_TYPE_NAMES.get(type_val, "DAMAGE")

        attacker_idx, _ = game_event.get_int32(_S1_FIELD_ATTACKER)
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

    def process_s2_entry(self, msg: Any, name_table: Any, tick: int = 0) -> None:
        """Parse a CMsgDOTACombatLogEntry and emit a CombatLogEntry.

        Args:
            msg: A ``CMsgDOTACombatLogEntry``-like protobuf message with
                integer name indices and flag attributes.
            name_table: An object with an ``items`` dict mapping int index →
                ``(key_str, value_bytes)`` for name resolution, OR a legacy
                object with a ``get(index, default='')`` method.
            tick: Current game tick.
        """
        log_type = _LOG_TYPE_NAMES.get(msg.type, "DAMAGE")

        # Support both StringTable.items dict and legacy dict-like name_table
        if hasattr(name_table, "items") and isinstance(name_table.items, dict):
            attacker_name = _resolve_name(name_table, msg.attacker_name)
            target_name = _resolve_name(name_table, msg.target_name)
            inflictor_name = _resolve_name(name_table, msg.inflictor_name)
        else:
            attacker_name = name_table.get(msg.attacker_name, "")
            target_name = name_table.get(msg.target_name, "")
            inflictor_name = name_table.get(msg.inflictor_name, "")

        entry = CombatLogEntry(
            tick=tick,
            log_type=log_type,
            attacker_name=attacker_name,
            target_name=target_name,
            inflictor_name=inflictor_name,
            value=msg.value,
            attacker_is_hero=msg.is_attacker_hero,
            target_is_hero=msg.is_target_hero,
            attacker_is_illusion=msg.is_attacker_illusion,
            target_is_illusion=msg.is_target_illusion,
            ability_level=msg.ability_level,
            gold_reason=msg.gold_reason,
            xp_reason=msg.xp_reason,
        )
        self._emit(entry)
