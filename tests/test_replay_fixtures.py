"""Missing optional assets must skip only the fixture consumers that need them."""

import json
from unittest.mock import Mock

import pytest

import gem
from tests import conftest as replay_fixtures


@pytest.mark.parametrize("match_id", [8868259993, 8855188139])
def test_missing_replay_skips_before_parsing(tmp_path, monkeypatch, match_id):
    monkeypatch.setattr(replay_fixtures, "OPENDOTA_FIXTURES_DIR", tmp_path)
    parse = Mock()
    monkeypatch.setattr(gem, "parse", parse)
    with pytest.raises(pytest.skip.Exception, match=str(match_id)):
        if match_id == 8855188139:
            replay_fixtures.feature_parity_match.__wrapped__()
        else:
            replay_fixtures.ti2026_short_replay_path.__wrapped__()
    parse.assert_not_called()


def test_feature_match_does_not_require_reference_json(tmp_path, monkeypatch):
    monkeypatch.setattr(replay_fixtures, "OPENDOTA_FIXTURES_DIR", tmp_path)
    replay = tmp_path / "8855188139.dem"
    replay.touch()
    parse = Mock(return_value=object())
    monkeypatch.setattr(gem, "parse", parse)
    assert replay_fixtures.feature_parity_match.__wrapped__() is parse.return_value
    parse.assert_called_once_with(str(replay))


def test_missing_reference_skips_without_parsing(tmp_path, monkeypatch):
    monkeypatch.setattr(replay_fixtures, "OPENDOTA_FIXTURES_DIR", tmp_path)
    (tmp_path / "8855188139.dem").touch()
    parse = Mock()
    monkeypatch.setattr(gem, "parse", parse)
    with pytest.raises(pytest.skip.Exception, match="8855188139.opendota.json"):
        replay_fixtures.feature_parity_reference.__wrapped__()
    parse.assert_not_called()


def test_reference_does_not_require_replay(tmp_path, monkeypatch):
    monkeypatch.setattr(replay_fixtures, "OPENDOTA_FIXTURES_DIR", tmp_path)
    reference = {"players": [{"hero_id": 1}]}
    (tmp_path / "8855188139.opendota.json").write_text(json.dumps(reference))
    assert replay_fixtures.feature_parity_reference.__wrapped__() == reference
