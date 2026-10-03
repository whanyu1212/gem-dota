"""The 0.10 ``teamfights`` names, renamed to ``fights`` in 0.11, are gone in 0.13.

"Teamfight" stays reserved for OpenDota's definition (``opendota_teamfights``,
``teamfight_participation``). Old JSON files that use the ``teamfights`` key
still load: that is file compatibility, not an API alias.
"""

from __future__ import annotations

import importlib
import json
import sys

import pytest

import gem
import gem.analysis
import gem.analysis.combat
from gem.analysis.bundle import MatchAnalysis
from gem.analysis.smoke import SmokeAnalysis, SmokeGroupStatus
from gem.extractors import fights
from gem.results.dataframes import build_dataframes
from gem.results.models import ParsedMatch
from gem.results.serialization import SCHEMA_VERSION, from_dict, to_dict


def _fight() -> fights.Fight:
    return fights.Fight(start_tick=0, end_tick=450, last_death_tick=10, deaths=1)


@pytest.mark.parametrize(
    ("namespace", "old"),
    [
        (gem, "teamfight_at_tick"),
        (gem, "is_active_teamfight_participant"),
        (gem, "TeamfightPositioning"),
        (gem, "build_teamfight_positioning"),
        (gem.analysis, "teamfight_at_tick"),
        (gem.analysis, "TeamfightPositioning"),
        (gem.analysis.combat, "teamfight_at_tick"),
        (gem.analysis.combat, "is_active_teamfight_participant"),
        (fights, "Teamfight"),
        (fights, "TeamfightPlayer"),
        (fights, "detect_teamfights"),
    ],
)
def test_old_names_are_gone(namespace, old):
    with pytest.raises(AttributeError):
        getattr(namespace, old)


@pytest.mark.parametrize(
    "module", ["gem.extractors.teamfights", "gem.analysis.teamfight_positioning"]
)
def test_old_modules_are_gone(module):
    sys.modules.pop(module, None)
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module(module)


def test_opendota_teamfight_names_stay():
    assert fights.detect_opendota_teamfights is not None
    assert fights.OpenDotaTeamfight is not None
    assert "opendota_teamfights" in ParsedMatch.__dataclass_fields__


def test_old_attributes_and_keywords_are_gone():
    match = ParsedMatch(fights=[_fight()])
    assert not hasattr(match, "teamfights")
    with pytest.raises(TypeError):
        ParsedMatch(teamfights=[_fight()])  # type: ignore[call-arg]

    assert not hasattr(MatchAnalysis(), "teamfight_positioning")
    with pytest.raises(TypeError):
        MatchAnalysis(teamfight_positioning=[])  # type: ignore[call-arg]

    analysis = SmokeAnalysis(
        activation_tick=0,
        activator="npc_dota_hero_axe",
        team=2,
        status=SmokeGroupStatus.NO_MEMBERS_OBSERVED,
        activation_x=None,
        activation_y=None,
        member_centroid_x=None,
        member_centroid_y=None,
    )
    assert not hasattr(analysis, "first_teamfight")


def test_old_table_names_are_gone(tmp_path):
    tables = build_dataframes(ParsedMatch(fights=[_fight()]))
    assert "fights" in tables
    for old in ("teamfights", "teamfight_players", "teamfight_positioning"):
        assert old not in tables
        with pytest.raises(KeyError):
            tables[old]
        assert tables.get(old) is None
    with pytest.raises(FileNotFoundError):
        gem.read_parquet_table(tmp_path, "teamfights")


def test_json_uses_fights_and_reads_the_old_key(recwarn):
    data = to_dict(ParsedMatch(match_id=1, fights=[_fight()]))
    assert "fights" in data and "teamfights" not in data
    assert SCHEMA_VERSION >= 3  # fights was renamed in schema 3

    old = json.loads(json.dumps(data))
    old["teamfights"] = old.pop("fights")
    old["schema_version"] = 2
    match = from_dict(old)
    assert [f.deaths for f in match.fights] == [1]
    assert not [w for w in recwarn if issubclass(w.category, DeprecationWarning)]
