"""Integration test: a build-6951+ replay with the ``fixed8`` var encoder (HY-177).

Since build 6951 the send tables mark 90 field definitions ``fixed8`` (8 raw bits).
Read as varints, the first 255 in the ``CParticleSystem`` instance baseline
desynced the bit stream and every such replay stopped with ``BufferReadError``
minutes in (GitHub #301). Fixture 9039619076 (BLAST SLAM VIII, build 6956) must
parse to the end and agree with OpenDota on the per-player totals and curves.

Marked ``slow`` + ``integration``: needs the full ``.dem`` plus its
``.opendota.json``.
"""

from __future__ import annotations

from pathlib import Path

import pytest

_SCALARS = (
    "hero_id",
    "kills",
    "deaths",
    "assists",
    "last_hits",
    "denies",
    "level",
    "net_worth",
    "gold_per_min",
    "xp_per_min",
    "hero_damage",
    "tower_damage",
    "hero_healing",
    "gold_spent",
    "obs_placed",
    "sen_placed",
    "camps_stacked",
    "rune_pickups",
)
_CURVES = {"gold_t": "gold_t_min", "xp_t": "xp_t_min", "lh_t": "lh_t_min", "dn_t": "dn_t_min"}

pytestmark = [pytest.mark.integration, pytest.mark.slow]


@pytest.fixture(scope="module")
def parsed(fixed8_encoder_match):
    return fixed8_encoder_match


@pytest.fixture(scope="module")
def opendota(fixed8_encoder_reference) -> dict:
    return fixed8_encoder_reference


def test_send_tables_use_the_fixed8_encoder(fixed8_encoder_replay_path: Path) -> None:
    from gem.parser import ReplayParser

    parser = ReplayParser(str(fixed8_encoder_replay_path))
    parser.stop_after_tick(1000)
    parser.parse()
    assert parser.entity_manager is not None
    particle = next(
        ci for ci in parser.entity_manager.classes_by_id.values() if ci.name == "CParticleSystem"
    )
    assert particle.serializer is not None
    field = next(
        f for f in particle.serializer.fields if f.var_name == "m_iServerControlPointAssignments"
    )
    # The fixture only guards the fix while the replay still declares fixed8.
    assert field.encoder == "fixed8"


def test_parses_to_the_end(parsed, opendota) -> None:
    assert parsed.parse_error is None
    assert parsed.truncated_at_tick is None
    assert parsed.duration == opendota["duration"]
    assert parsed.radiant_win == opendota["radiant_win"]
    assert len(parsed.opendota_teamfights) == len(opendota["teamfights"])


def test_players_match_opendota(parsed, opendota) -> None:
    by_slot = {p.player_id if p.player_id < 5 else p.player_id + 123: p for p in parsed.players}
    assert sorted(by_slot) == sorted(p["player_slot"] for p in opendota["players"])
    for expected in opendota["players"]:
        player = by_slot[expected["player_slot"]]
        for name in _SCALARS:
            assert getattr(player, name) == expected[name], (expected["player_slot"], name)
        for od_name, gem_name in _CURVES.items():
            assert getattr(player, gem_name) == expected[od_name], (
                expected["player_slot"],
                od_name,
            )
