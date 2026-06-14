"""Deprecated compatibility shim for :mod:`gem.combat.aggregator`."""

import warnings

warnings.warn(
    "gem.combat_aggregator is deprecated; import from gem.combat.aggregator instead.",
    DeprecationWarning,
    stacklevel=2,
)

from gem.combat.aggregator import (  # noqa: E402
    _CombatAggregator,
    _dedup_purchase_log,
    _int_counter,
    _ParsedPlayerAgg,
)

__all__ = ["_CombatAggregator", "_ParsedPlayerAgg", "_dedup_purchase_log", "_int_counter"]
