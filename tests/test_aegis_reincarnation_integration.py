"""Integration test: OpenDota's August 2026 reincarnation rule (HY-178).

In fixture 9040268873 (BLAST SLAM VIII, build 6956) Kez (player 5) picks up the
Aegis at 2262 s and 2941 s and reincarnates at 2388 s and 3087 s. OpenDota's
older rule tracked one holder and one death second, so it counted the second
reincarnation and found a teamfight at 3072-3111 s. odota/parser ``efe5794b``
lets each pickup cover one death; OpenDota's JSON for this match has neither
death and nine teamfights.

Marked ``slow`` + ``integration``: needs the full ``.dem`` plus its
``.opendota.json``.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "opendota"
_MATCH_ID = 9040268873
_KEZ = "npc_dota_hero_kez"

pytestmark = [pytest.mark.integration, pytest.mark.slow]


@pytest.fixture(scope="module")
def parsed(aegis_reincarnation_replay_path: Path):
    import gem

    return gem.parse(str(aegis_reincarnation_replay_path))


@pytest.fixture(scope="module")
def opendota() -> dict:
    path = FIXTURES_DIR / f"{_MATCH_ID}.opendota.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_kez_reincarnates_on_two_aegises(parsed) -> None:
    reincarnations = [
        entry.game_time_s
        for entry in parsed.combat_log
        if entry.log_type == "DEATH" and entry.target_name == _KEZ and entry.will_reincarnate
    ]
    assert reincarnations == [2388, 3087]
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
    assert not kez_deaths & {2388, 3087}
