"""Combat log ingestion for Dota 2 Source 2 replays.

Parses CMsgDOTACombatLogEntry user messages (S2 path) into normalized
CombatLogEntry objects and dispatches them to registered handlers.

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

# Mapping from CMsgDOTACombatLogEntry.type int → string label
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

    def process_s2_entry(self, msg: Any, name_table: Any) -> None:
        """Parse a CMsgDOTACombatLogEntry and emit a CombatLogEntry.

        Args:
            msg: A ``CMsgDOTACombatLogEntry``-like protobuf message with
                integer name indices and flag attributes.
            name_table: An object with a ``get(index, default='')`` method
                that maps name indices to string names.
        """
        log_type = _LOG_TYPE_NAMES.get(msg.type, "DAMAGE")
        entry = CombatLogEntry(
            tick=0,  # tick is set by the caller if needed
            log_type=log_type,
            attacker_name=name_table.get(msg.attacker_name, ""),
            target_name=name_table.get(msg.target_name, ""),
            inflictor_name=name_table.get(msg.inflictor_name, ""),
            value=msg.value,
            attacker_is_hero=msg.attacker_hero,
            target_is_hero=msg.target_hero,
            attacker_is_illusion=msg.attacker_illusion,
            target_is_illusion=msg.target_illusion,
            ability_level=msg.ability_level,
            gold_reason=msg.gold_reason,
            xp_reason=msg.xp_reason,
        )
        self._emit(entry)
