"""Coverage for removed top-level compatibility modules."""

from __future__ import annotations

import importlib
import sys

import pytest

_REMOVED_MODULES = [
    "gem.batch",
    "gem.reader",
    "gem.stream",
    "gem.sendtable",
    "gem.field_decoder",
    "gem.field_path",
    "gem.field_reader",
    "gem.field_state",
    "gem.entities",
    "gem.game_events",
    "gem.string_table",
    "gem.combatlog",
    "gem.combat_aggregator",
    "gem.match_builder",
    "gem.dataframes",
    "gem.replay_fetch",
    "gem.models",
    "gem.map_context",
    "gem.rosh_conversion",
]

_CANONICAL_IMPORTS = [
    ("gem.replays.batch", "parse_many"),
    ("gem.binary.reader", "BitReader"),
    ("gem.binary.stream", "DemoStream"),
    ("gem.schema.sendtable", "parse_send_tables"),
    ("gem.schema.field_decoder", "find_decoder"),
    ("gem.schema.field_path", "FieldPath"),
    ("gem.schema.field_reader", "read_fields"),
    ("gem.schema.field_state", "FieldState"),
    ("gem.state.entities", "EntityManager"),
    ("gem.state.game_events", "GameEventManager"),
    ("gem.state.string_table", "StringTables"),
    ("gem.combat.log", "CombatLogProcessor"),
    ("gem.combat.aggregator", "_CombatAggregator"),
    ("gem.results.assembly", "build_parsed_match"),
    ("gem.results.dataframes", "build_dataframes"),
    ("gem.replays.fetch", "fetch_replay"),
    ("gem.results.models", "ParsedMatch"),
    ("gem.analysis.map_context", "MapContextBucket"),
    ("gem.analysis.roshan", "RoshConversion"),
]


@pytest.mark.parametrize("module_name", _REMOVED_MODULES)
def test_removed_top_level_compatibility_modules_do_not_import(module_name: str) -> None:
    """Breaking releases should not carry root compatibility modules."""
    sys.modules.pop(module_name, None)

    with pytest.raises(ModuleNotFoundError):
        importlib.import_module(module_name)


@pytest.mark.parametrize(("module_name", "symbol"), _CANONICAL_IMPORTS)
def test_canonical_replacements_remain_importable(module_name: str, symbol: str) -> None:
    """Canonical grouped modules replace the removed root compatibility paths."""
    module = importlib.import_module(module_name)
    assert getattr(module, symbol) is not None
