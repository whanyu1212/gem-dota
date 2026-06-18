"""Unit tests for API-rate enrichment (gold_per_min/xp_per_min and derived totals).

These cover the pure mapping/derivation in ``apply_api_rates`` offline — the
network wrapper ``enrich_with_api_rates`` is a thin shim over ``fetch_opendota_match``
plus this function.
"""

from __future__ import annotations

from gem.replays.fetch import _opendota_slot_to_player_id, apply_api_rates
from gem.results.models import ParsedMatch


def _match(duration: int = 600) -> ParsedMatch:
    return ParsedMatch(duration=duration)


def test_slot_to_player_id_maps_radiant_and_dire():
    assert _opendota_slot_to_player_id(0) == 0
    assert _opendota_slot_to_player_id(4) == 4
    assert _opendota_slot_to_player_id(128) == 5
    assert _opendota_slot_to_player_id(132) == 9


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
