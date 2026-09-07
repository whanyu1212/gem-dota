"""Public record behavior that an eventual compact layout must account for.

Reference: src/gem/combat/log.py and src/gem/extractors/_snapshots.py.
"""

from __future__ import annotations

import pickle
import weakref
from dataclasses import asdict, fields, replace

import pytest

import gem
from gem.combat import CombatLogEntry, CombatLogType
from gem.extractors import PlayerStateSnapshot
from gem.results.models import ParsedMatch


class ExtendedCombatEntry(CombatLogEntry):
    """An ordinary downstream subclass with inherited construction."""


class ExtendedSnapshot(PlayerStateSnapshot):
    """An ordinary downstream subclass with inherited construction."""


_COMBAT_ARGS = (30, CombatLogType.DAMAGE)
_SNAPSHOT_ARGS = (
    30,
    0,
    "npc_dota_hero_axe",
    2,
    5,
    100,
    200,
    300,
    4,
    1,
    500,
    600,
    70.0,
    80.0,
    None,
    0.0,
)
_SNAPSHOT_KEYS = (
    "tick",
    "player_id",
    "npc_name",
    "team",
    "level",
    "xp",
    "gold",
    "net_worth",
    "lh",
    "dn",
    "hp",
    "max_hp",
    "mana",
    "max_mana",
    "x",
    "y",
)


@pytest.fixture(params=["combat", "snapshot"])
def record_spec(request):
    if request.param == "combat":
        return CombatLogEntry, ExtendedCombatEntry, _COMBAT_ARGS, ("tick", "log_type")
    return PlayerStateSnapshot, ExtendedSnapshot, _SNAPSHOT_ARGS, _SNAPSHOT_KEYS


def test_construction_defaults_and_subclass(record_spec):
    cls, subclass, args, keys = record_spec
    positional = cls(*args)
    keyword = cls(**dict(zip(keys, args, strict=True)))
    assert positional == keyword
    assert asdict(subclass(*args)) == asdict(positional)
    if cls is CombatLogEntry:
        assert positional.attacker_name == ""
        assert positional.value == 0
        assert positional.will_reincarnate is False
    else:
        assert positional.total_earned_xp == 0
        assert positional.items == {}
        assert positional.ability_levels == {}
        positional.items[0] = "item_blink"
        positional.ability_levels["axe_berserkers_call"] = 2
        assert keyword.items == {}
        assert keyword.ability_levels == {}
    assert positional.game_time_s is None


def test_instance_dictionary_is_live_and_contains_declared_fields(record_spec):
    cls, _, args, _ = record_spec
    record = cls(*args)
    state = vars(record)
    assert state is record.__dict__
    assert set(state) == {field.name for field in fields(record)}
    state["tick"] = 60
    assert record.tick == 60
    record.tick = 90
    assert state["tick"] == 90


def test_dynamic_attributes(record_spec):
    cls, _, args, _ = record_spec
    record = cls(*args)
    annotation = {"source": "downstream"}
    record.annotation = annotation
    assert vars(record)["annotation"] is annotation


def test_weak_references(record_spec):
    cls, _, args, _ = record_spec
    record = cls(*args)
    reference = weakref.ref(record)
    assert reference() is record
    del record
    assert reference() is None


def test_dataclass_value_operations(record_spec):
    cls, _, args, _ = record_spec
    record = cls(*args)
    same = cls(*args)
    assert record == same
    assert repr(record) == repr(same)
    assert repr(record).startswith(f"{cls.__name__}(tick=30, ")
    assert "annotation" not in asdict(record)
    changed = replace(record, tick=60)
    assert changed.tick == 60
    assert record.tick == 30
    assert changed != record
    assert not hasattr(changed, "annotation")
    assert asdict(changed) == {**asdict(record), "tick": 60}


def test_value_operations_ignore_extension_attributes(record_spec):
    cls, _, args, _ = record_spec
    record = cls(*args)
    same = cls(*args)
    record.annotation = "downstream"
    assert record == same
    assert repr(record) == repr(same)
    assert asdict(record) == asdict(same)
    assert not hasattr(replace(record), "annotation")


@pytest.mark.parametrize("with_extension", [False, True])
@pytest.mark.parametrize("protocol", [4, pickle.HIGHEST_PROTOCOL])
def test_record_pickle_preserves_fields_and_extensions(record_spec, protocol, with_extension):
    cls, _, args, _ = record_spec
    record = cls(*args)
    if with_extension:
        record.annotation = {"source": "downstream"}
    if isinstance(record, PlayerStateSnapshot):
        record.items[0] = "item_blink"
        record.ability_levels["axe_berserkers_call"] = 2
    restored = pickle.loads(pickle.dumps(record, protocol=protocol))
    assert type(restored) is cls
    assert restored == record
    assert asdict(restored) == asdict(record)
    if with_extension:
        assert vars(restored) == vars(record)
        assert restored.annotation is not record.annotation
    if isinstance(record, PlayerStateSnapshot):
        assert restored.items is not record.items
        assert restored.ability_levels is not record.ability_levels


@pytest.mark.parametrize("with_extension", [False, True])
@pytest.mark.parametrize("protocol", [4, pickle.HIGHEST_PROTOCOL])
def test_match_pickle_preserves_shared_combat_entries(protocol, with_extension):
    entry = CombatLogEntry(*_COMBAT_ARGS, attacker_name="npc_dota_hero_axe", value=17)
    if with_extension:
        entry.annotation = "downstream"
    match = ParsedMatch(match_id=42, combat_log=[entry, entry])
    restored = pickle.loads(pickle.dumps(match, protocol=protocol))
    assert restored == match
    assert restored.combat_log[0] is restored.combat_log[1]
    assert restored.combat_log[0] is not entry
    if with_extension:
        assert restored.combat_log[0].annotation == "downstream"
    assert gem.to_dict(restored) == gem.to_dict(match)
    assert "annotation" not in gem.to_dict(restored)["combat_log"][0]
