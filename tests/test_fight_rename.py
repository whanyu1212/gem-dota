"""The ``teamfights`` -> ``fights`` rename keeps the old names working, with a warning."""

from __future__ import annotations

import importlib
import json
import sys

import pytest

import gem
import gem.analysis
from gem.analysis.bundle import MatchAnalysis
from gem.analysis.smoke import SmokeAnalysis, SmokeGroupStatus
from gem.extractors import fights
from gem.results.dataframes import build_dataframes
from gem.results.models import ParsedMatch
from gem.results.serialization import SCHEMA_VERSION, from_dict, to_dict


def _fight() -> fights.Fight:
    return fights.Fight(start_tick=0, end_tick=450, last_death_tick=10, deaths=1)


@pytest.mark.parametrize(
    ("namespace", "old", "new"),
    [
        (gem, "teamfight_at_tick", "fight_at_tick"),
        (gem, "is_active_teamfight_participant", "is_active_fight_participant"),
        (gem, "TeamfightPositioning", "FightPositioning"),
        (gem, "build_teamfight_positioning", "build_fight_positioning"),
        (gem.analysis, "teamfight_at_tick", "fight_at_tick"),
        (gem.analysis, "TeamfightPositioning", "FightPositioning"),
        (fights, "Teamfight", "Fight"),
        (fights, "TeamfightPlayer", "FightPlayer"),
        (fights, "detect_teamfights", "detect_fights"),
    ],
)
def test_old_module_names_warn_and_resolve(namespace, old, new):
    with pytest.warns(DeprecationWarning, match=f"{old} is deprecated.*use .*{new}"):
        value = getattr(namespace, old)
    assert value is getattr(namespace, new)


def test_old_names_are_not_exported():
    assert "teamfight_at_tick" not in gem.__all__
    assert "fight_at_tick" in gem.__all__
    assert "find_fights" in gem.__all__


def test_unknown_names_still_raise_attribute_error():
    with pytest.raises(AttributeError):
        _ = gem.not_a_real_name


@pytest.mark.parametrize(
    ("module", "old", "new"),
    [
        ("gem.extractors.teamfights", "detect_teamfights", "detect_fights"),
        ("gem.analysis.teamfight_positioning", "TeamfightPositioning", "FightPositioning"),
    ],
)
def test_old_modules_warn_on_import_and_keep_old_names(module, old, new):
    sys.modules.pop(module, None)
    with pytest.warns(DeprecationWarning, match=f"{module} is deprecated"):
        imported = importlib.import_module(module)
    assert getattr(imported, old) is getattr(imported, new)


def test_old_extractor_module_keeps_opendota_names_unchanged():
    sys.modules.pop("gem.extractors.teamfights", None)
    with pytest.warns(DeprecationWarning):
        old = importlib.import_module("gem.extractors.teamfights")
    assert old.detect_opendota_teamfights is fights.detect_opendota_teamfights
    assert old.OpenDotaTeamfight is fights.OpenDotaTeamfight


def test_parsed_match_teamfights_reads_and_writes_fights():
    match = ParsedMatch(match_id=1)
    new_fights = [_fight()]
    with pytest.warns(DeprecationWarning, match="ParsedMatch.teamfights"):
        match.teamfights = new_fights
    assert match.fights is new_fights
    with pytest.warns(DeprecationWarning):
        assert match.teamfights is new_fights


def test_analysis_records_keep_their_old_attribute_names():
    analysis = MatchAnalysis()
    with pytest.warns(DeprecationWarning, match="MatchAnalysis.teamfight_positioning"):
        assert analysis.teamfight_positioning is analysis.fight_positioning

    smoke = SmokeAnalysis(
        activation_tick=0,
        activator="npc_dota_hero_axe",
        team=2,
        status=SmokeGroupStatus.NO_MEMBERS_OBSERVED,
        activation_x=None,
        activation_y=None,
        member_centroid_x=None,
        member_centroid_y=None,
        first_fight=_fight(),
    )
    with pytest.warns(DeprecationWarning, match="SmokeAnalysis.first_teamfight"):
        assert smoke.first_teamfight is smoke.first_fight


def test_old_table_names_warn_and_are_not_listed_twice():
    tables = build_dataframes(ParsedMatch(match_id=1, fights=[_fight()]))
    assert "fights" in tables and "fight_players" in tables
    assert "teamfights" not in tables
    with pytest.warns(DeprecationWarning, match="'teamfights' is deprecated"):
        assert tables["teamfights"] is tables["fights"]
    with pytest.warns(DeprecationWarning):
        assert tables["teamfight_players"] is tables["fight_players"]
    with pytest.raises(KeyError):
        _ = tables["no_such_table"]


def test_read_parquet_table_accepts_the_old_name(tmp_path):
    pytest.importorskip("pyarrow")
    tables = build_dataframes(ParsedMatch(match_id=7, fights=[_fight()]))
    (tmp_path / "7").mkdir()
    tables["fights"].to_parquet(tmp_path / "7" / "fights.parquet")
    with pytest.warns(DeprecationWarning):
        frame = gem.read_parquet_table(tmp_path, "teamfights")
    assert len(frame) == 1


def test_json_uses_fights_and_reads_the_old_key(recwarn):
    data = to_dict(ParsedMatch(match_id=1, fights=[_fight()]))
    assert "fights" in data and "teamfights" not in data
    assert SCHEMA_VERSION == 3

    old = json.loads(json.dumps(data))
    old["teamfights"] = old.pop("fights")
    old["schema_version"] = 2
    match = from_dict(old)
    assert [f.deaths for f in match.fights] == [1]
    assert not [w for w in recwarn if issubclass(w.category, DeprecationWarning)]
