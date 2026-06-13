"""Compatibility shim for :mod:`gem.combat.log`."""

from gem.combat.log import (
    COMBAT_LOG_TYPES,
    CombatLogEntry,
    CombatLogHandler,
    CombatLogProcessor,
    _resolve_name,
)

__all__ = [
    "COMBAT_LOG_TYPES",
    "CombatLogEntry",
    "CombatLogHandler",
    "CombatLogProcessor",
    "_resolve_name",
]
