"""Compatibility coverage for deprecated top-level import shims."""

from __future__ import annotations

import importlib
import re
import sys

import pytest

_SHIMS = [
    ("gem.reader", "gem.binary.reader", "BitReader"),
    ("gem.stream", "gem.binary.stream", "DemoStream"),
    ("gem.sendtable", "gem.schema.sendtable", "parse_send_tables"),
    ("gem.field_decoder", "gem.schema.field_decoder", "find_decoder"),
    ("gem.field_path", "gem.schema.field_path", "FieldPath"),
    ("gem.field_reader", "gem.schema.field_reader", "read_fields"),
    ("gem.field_state", "gem.schema.field_state", "FieldState"),
    ("gem.entities", "gem.state.entities", "EntityManager"),
    ("gem.game_events", "gem.state.game_events", "GameEventManager"),
    ("gem.string_table", "gem.state.string_table", "StringTables"),
    ("gem.combatlog", "gem.combat.log", "CombatLogProcessor"),
    ("gem.combat_aggregator", "gem.combat.aggregator", "_CombatAggregator"),
    ("gem.match_builder", "gem.results.assembly", "build_parsed_match"),
    ("gem.dataframes", "gem.results.dataframes", "build_dataframes"),
]


@pytest.mark.parametrize(("shim_module", "canonical_module", "symbol"), _SHIMS)
def test_deprecated_top_level_shims_warn_and_reexport(
    shim_module: str, canonical_module: str, symbol: str
) -> None:
    """Legacy root modules should still import while warning users to migrate."""
    sys.modules.pop(shim_module, None)

    with pytest.warns(DeprecationWarning, match=rf"{re.escape(shim_module)} is deprecated"):
        shim = importlib.import_module(shim_module)

    canonical = importlib.import_module(canonical_module)
    assert getattr(shim, symbol) is getattr(canonical, symbol)
