"""Integration test: a kill by an illusion of the victim counts (HY-237).

In fixture 9039619076 (BLAST SLAM VIII, build 6956) Pangolier dies at 2079 s to
an illusion of himself from Grimstroke's Dark Portrait. The illusion has
Pangolier's unit name, so gem dropped the death as a suicide. odota/parser
``c206d0db`` credits it to the illusion's owner, and OpenDota's JSON for this
match (a parse with its current rules) counts it.

Marked ``slow`` + ``integration``: needs the full ``.dem`` plus its
``.opendota.json``.
"""

from __future__ import annotations

from dataclasses import asdict

import pytest

_PANGOLIER = "npc_dota_hero_pangolier"
_GRIMSTROKE = "npc_dota_hero_grimstroke"

pytestmark = [pytest.mark.integration, pytest.mark.slow]


def test_pangolier_dies_to_his_own_dark_portrait_illusion(fixed8_encoder_match) -> None:
    (death,) = [
        entry
        for entry in fixed8_encoder_match.combat_log
        if entry.log_type == "DEATH"
        and entry.target_name == _PANGOLIER
        and entry.game_time_s == 2079
    ]
    assert death.attacker_name == _PANGOLIER
    assert death.attacker_is_illusion
    assert death.damage_source_name == _GRIMSTROKE


def test_the_kill_is_grimstrokes(fixed8_encoder_match) -> None:
    import gem

    grimstroke = gem.find_player(fixed8_encoder_match, _GRIMSTROKE)
    pangolier = gem.find_player(fixed8_encoder_match, _PANGOLIER)
    assert grimstroke is not None and pangolier is not None
    assert 2079 in [
        entry.game_time_s for entry in grimstroke.kills_log if entry.target_name == _PANGOLIER
    ]
    assert pangolier.killed_by.get(_GRIMSTROKE, 0) >= 1


def test_teamfights_equal_opendota(fixed8_encoder_match, fixed8_encoder_reference) -> None:
    fights = [asdict(fight) for fight in fixed8_encoder_match.opendota_teamfights]
    assert fights == fixed8_encoder_reference["teamfights"]


def test_kills_match_opendota(fixed8_encoder_match, fixed8_encoder_reference) -> None:
    by_slot = {
        p.player_id if p.player_id < 5 else p.player_id + 123: p
        for p in fixed8_encoder_match.players
    }
    for expected in fixed8_encoder_reference["players"]:
        player = by_slot[expected["player_slot"]]
        assert player.killed == expected["killed"], expected["player_slot"]
        assert player.killed_by == expected["killed_by"], expected["player_slot"]
