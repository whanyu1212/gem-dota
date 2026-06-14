"""Deprecated compatibility shim for :mod:`gem.combat.log`."""

import warnings

warnings.warn(
    "gem.combatlog is deprecated; import from gem.combat.log instead.",
    DeprecationWarning,
    stacklevel=2,
)

from gem.combat.log import (  # noqa: E402
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
