"""Compatibility shim for :mod:`gem.combat.aggregator`."""

from gem.combat.aggregator import (
    _CombatAggregator,
    _dedup_purchase_log,
    _int_counter,
    _ParsedPlayerAgg,
)

__all__ = ["_CombatAggregator", "_ParsedPlayerAgg", "_dedup_purchase_log", "_int_counter"]
