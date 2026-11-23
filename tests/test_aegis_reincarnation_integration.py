"""Integration test: OpenDota's August 2026 reincarnation rule (HY-178).

In the long fixture 9101299342 (BLAST SLAM IX) Kez (player 5) picks up the Aegis
at 2075 s and 4033 s and reincarnates at 2224 s and 4176 s. OpenDota's older rule
tracked one holder and one death second; odota/parser ``efe5794b`` lets each
pickup cover one death, so OpenDota's JSON for this match has neither death.

Marked ``slow`` + ``integration``: needs the full ``.dem`` plus its
``.opendota.json``.
"""

from __future__ import annotations

from dataclasses import asdict

import pytest

_KEZ = "npc_dota_hero_kez"
_REINCARNATIONS = [2224, 4176]

pytestmark = [pytest.mark.integration, pytest.mark.slow]


@pytest.fixture(scope="module")
def parsed(long_parsed_match):
    return long_parsed_match


@pytest.fixture(scope="module")
def opendota(long_reference) -> dict:
    return long_reference


def test_kez_reincarnates_on_two_aegises(parsed) -> None:
    reincarnations = [
        entry.game_time_s
        for entry in parsed.combat_log
        if entry.log_type == "DEATH" and entry.target_name == _KEZ and entry.will_reincarnate
    ]
    assert reincarnations == _REINCARNATIONS
    pickups = [event.player_id for event in parsed.aegis_events if event.event_type == "pickup"]
    assert pickups.count(5) >= 2


def test_teamfights_equal_opendota(parsed, opendota) -> None:
    fights = [asdict(fight) for fight in parsed.opendota_teamfights]
    assert [(f["start"], f["end"]) for f in fights] == [
        (f["start"], f["end"]) for f in opendota["teamfights"]
    ]
    assert fights == opendota["teamfights"]


def test_opendota_counts_neither_reincarnation(opendota) -> None:
    # The reference itself: OpenDota's kills_log has no Kez death at either second.
    kez_deaths = {
        entry["time"]
        for player in opendota["players"]
        for entry in player.get("kills_log") or []
        if entry["key"] == _KEZ
    }
    assert kez_deaths
    assert not kez_deaths & set(_REINCARNATIONS)
