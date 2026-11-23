"""Integration test: a kill by an illusion of the victim counts (HY-237).

In fixture 9101479361 (BLAST SLAM IX, patch 7.42) Dazzle dies at 1985 s to an
illusion of himself from Dark Seer's Wall of Replica. The illusion has Dazzle's
unit name, so gem once dropped such a death as a suicide. odota/parser
``c206d0db`` credits it to the illusion's owner, and OpenDota's JSON for this
match (a parse with its current rules) counts it.

Marked ``slow`` + ``integration``: needs the full ``.dem`` plus its
``.opendota.json``.
"""

from __future__ import annotations

from dataclasses import asdict

import pytest

_DAZZLE = "npc_dota_hero_dazzle"
_DARK_SEER = "npc_dota_hero_dark_seer"
_DEATH_S = 1985

pytestmark = [pytest.mark.integration, pytest.mark.slow]


def test_dazzle_dies_to_his_own_wall_of_replica_illusion(patch_742_parsed_match) -> None:
    (death,) = [
        entry
        for entry in patch_742_parsed_match.combat_log
        if entry.log_type == "DEATH"
        and entry.target_name == _DAZZLE
        and not entry.target_is_illusion
        and entry.game_time_s == _DEATH_S
    ]
    assert death.attacker_name == _DAZZLE
    assert death.attacker_is_illusion
    assert death.damage_source_name == _DARK_SEER


def test_the_kill_is_dark_seers(patch_742_parsed_match) -> None:
    import gem

    dark_seer = gem.find_player(patch_742_parsed_match, _DARK_SEER)
    dazzle = gem.find_player(patch_742_parsed_match, _DAZZLE)
    assert dark_seer is not None and dazzle is not None
    assert _DEATH_S in [
        entry.game_time_s for entry in dark_seer.kills_log if entry.target_name == _DAZZLE
    ]
    assert dazzle.killed_by.get(_DARK_SEER, 0) >= 1


def test_teamfights_equal_opendota(patch_742_parsed_match, patch_742_reference) -> None:
    fights = [asdict(fight) for fight in patch_742_parsed_match.opendota_teamfights]
    assert fights == patch_742_reference["teamfights"]


def test_kills_match_opendota(patch_742_parsed_match, patch_742_reference) -> None:
    by_slot = {
        p.player_id if p.player_id < 5 else p.player_id + 123: p
        for p in patch_742_parsed_match.players
    }
    for expected in patch_742_reference["players"]:
        player = by_slot[expected["player_slot"]]
        assert player.killed == expected["killed"], expected["player_slot"]
        assert player.killed_by == expected["killed_by"], expected["player_slot"]
