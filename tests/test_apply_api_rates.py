"""Unit tests for explicit API enrichment of postgame player values.

These cover the pure mapping/derivation in ``apply_api_rates`` offline — the
network wrapper ``enrich_with_api_rates`` is a thin shim over ``fetch_opendota_match``
plus this function.
"""

from __future__ import annotations

import contextlib
import io

import pytest

from gem.replays import fetch
from gem.replays.fetch import _opendota_slot_to_player_id, apply_api_rates
from gem.results.models import ParsedMatch


def _match(duration: int = 600) -> ParsedMatch:
    return ParsedMatch(duration=duration)


def test_slot_to_player_id_maps_radiant_and_dire():
    assert _opendota_slot_to_player_id(0) == 0
    assert _opendota_slot_to_player_id(4) == 4
    assert _opendota_slot_to_player_id(128) == 5
    assert _opendota_slot_to_player_id(132) == 9


def test_fetch_opendota_match_raises_value_error_on_non_json(monkeypatch):
    # A non-JSON response (e.g. an HTML error/rate-limit page) should surface a
    # ValueError naming the match, not a bare JSONDecodeError.
    @contextlib.contextmanager
    def fake_urlopen(*_args, **_kwargs):
        yield io.BytesIO(b"<html>rate limited</html>")

    monkeypatch.setattr(fetch.urllib.request, "urlopen", fake_urlopen)
    with pytest.raises(ValueError, match="non-JSON response for match 123"):
        fetch.fetch_opendota_match(123)


def test_applies_rates_and_derives_totals():
    m = _match(duration=600)  # 10 minutes
    od = {
        "duration": 600,
        "players": [
            {"player_slot": 0, "gold_per_min": 500, "xp_per_min": 400},
            {"player_slot": 128, "gold_per_min": 600, "xp_per_min": 700},
        ],
    }
    apply_api_rates(m, od)

    p0 = m.players[0]
    assert p0.gold_per_min == 500
    assert p0.xp_per_min == 400
    assert p0.total_gold == 5000  # 500 * 600 / 60
    assert p0.total_xp == 4000

    p5 = m.players[5]  # dire slot 128 -> player_id 5
    assert p5.gold_per_min == 600
    assert p5.total_gold == 6000


def test_uses_opendota_formula_with_floor():
    # 796 gpm over 4176s -> floor(796 * 4176 / 60) = 55401 (OpenDota's exact value).
    m = _match(duration=4176)
    od = {"duration": 4176, "players": [{"player_slot": 0, "gold_per_min": 796, "xp_per_min": 795}]}
    apply_api_rates(m, od)
    assert m.players[0].total_gold == 55401
    assert m.players[0].total_xp == 55332


def test_falls_back_to_match_duration_when_api_omits_it():
    m = _match(duration=600)
    od = {"players": [{"player_slot": 0, "gold_per_min": 500, "xp_per_min": 400}]}  # no duration
    apply_api_rates(m, od)
    assert m.players[0].total_gold == 5000  # used match.duration=600


def test_missing_rate_leaves_field_zero():
    m = _match(duration=600)
    od = {"duration": 600, "players": [{"player_slot": 0, "gold_per_min": 500}]}  # no xp_per_min
    apply_api_rates(m, od)
    assert m.players[0].gold_per_min == 500
    assert m.players[0].xp_per_min == 0
    assert m.players[0].total_xp == 0


def test_returns_same_match_instance():
    m = _match()
    assert apply_api_rates(m, {"players": []}) is m


def test_ignores_players_without_slot():
    m = _match(duration=600)
    od = {"duration": 600, "players": [{"gold_per_min": 500}]}  # no player_slot
    apply_api_rates(m, od)
    assert all(p.gold_per_min == 0 for p in m.players)


def test_overwrites_combat_scalars_with_exact_api_values():
    m = _match(duration=600)
    # Simulate a reconstructed estimate that the API should override exactly.
    m.players[0].hero_damage = 9999
    od = {
        "duration": 600,
        "players": [
            {"player_slot": 0, "hero_damage": 38922, "tower_damage": 6522, "hero_healing": 0},
        ],
    }
    apply_api_rates(m, od)
    assert m.players[0].hero_damage == 38922
    assert m.players[0].tower_damage == 6522
    assert m.players[0].hero_healing == 0


def test_missing_combat_scalar_preserves_reconstruction():
    m = _match(duration=600)
    m.players[0].hero_damage = 1234  # offline estimate
    od = {"duration": 600, "players": [{"player_slot": 0, "gold_per_min": 500}]}  # no combat stats
    apply_api_rates(m, od)
    assert m.players[0].hero_damage == 1234  # left untouched


def test_applies_top_level_permanent_buff_flags_by_player_slot():
    m = _match()
    od = {
        "players": [
            {
                "player_slot": 0,
                "aghanims_scepter": 1,
                "aghanims_shard": 0,
                "moonshard": 1,
            },
            {
                "player_slot": 128,
                "aghanims_scepter": 0,
                "aghanims_shard": 1,
                "moonshard": 0,
            },
        ]
    }

    apply_api_rates(m, od)

    assert (
        m.players[0].aghanims_scepter,
        m.players[0].aghanims_shard,
        m.players[0].moonshard,
    ) == (1, 0, 1)
    assert (
        m.players[5].aghanims_scepter,
        m.players[5].aghanims_shard,
        m.players[5].moonshard,
    ) == (0, 1, 0)


def test_derives_missing_api_flags_from_permanent_buffs():
    m = _match()
    od = {
        "players": [
            {
                "player_slot": 0,
                "aghanims_scepter": 0,
                "permanent_buffs": [
                    {"permanent_buff": 1},
                    {"permanent_buff": 2},
                    {"permanent_buff": 12},
                    {"permanent_buff": 23},
                    {"missing_id": True},
                ],
            },
            {"player_slot": 128, "permanent_buffs": []},
        ]
    }

    apply_api_rates(m, od)

    # An explicit top-level value wins; missing fields fall back to the array.
    assert (
        m.players[0].aghanims_scepter,
        m.players[0].aghanims_shard,
        m.players[0].moonshard,
    ) == (0, 1, 1)
    assert (
        m.players[5].aghanims_scepter,
        m.players[5].aghanims_shard,
        m.players[5].moonshard,
    ) == (0, 0, 0)


def test_missing_api_buff_data_preserves_existing_availability():
    m = _match()
    m.players[0].aghanims_scepter = 1
    m.players[0].aghanims_shard = 0
    m.players[0].moonshard = 1

    apply_api_rates(m, {"players": [{"player_slot": 0, "gold_per_min": 500}]})

    assert (
        m.players[0].aghanims_scepter,
        m.players[0].aghanims_shard,
        m.players[0].moonshard,
    ) == (1, 0, 1)
    assert m.players[1].aghanims_scepter is None
    assert m.players[1].aghanims_shard is None
    assert m.players[1].moonshard is None
