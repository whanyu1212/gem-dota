"""Integration test: chat-event times match OpenDota's tick-start clock.

OpenDota stamps chat events (rune pickups, ``CHAT_MESSAGE_*`` objectives) with
its running clock from ``@OnTickStart`` (odota/parser Parse.java). gem
reproduces that clock per outer tick; rune pickups and chat-type objectives must
carry OpenDota's exact times.

Marked ``slow`` + ``integration``: needs the full ``.dem`` plus its
``.opendota.json``.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "opendota"
_MATCH_IDS = (8822520406, 8860187335)
_CHAT_TYPES = (
    "CHAT_MESSAGE_FIRSTBLOOD",
    "CHAT_MESSAGE_COURIER_LOST",
    "CHAT_MESSAGE_AEGIS",
    "CHAT_MESSAGE_ROSHAN_KILL",
)


def _od_player_slot(player_id: int) -> int:
    return player_id if player_id < 5 else 128 + (player_id - 5)


def _objective_key(entry: dict) -> tuple:
    return tuple(entry.get(k) for k in ("type", "key", "slot", "team", "killer"))


@pytest.mark.slow
@pytest.mark.integration
class TestChatEventClock:
    @pytest.fixture(scope="class", params=_MATCH_IDS)
    def parsed(self, request):
        dem = FIXTURES_DIR / f"{request.param}.dem"
        reference = dem.with_suffix(".opendota.json")
        if not dem.exists() or not reference.exists():
            pytest.skip(f"OpenDota fixture {request.param} (.dem + .opendota.json) not available")
        import gem

        return gem.parse(dem), json.loads(reference.read_text())

    def test_rune_pickup_times_match_opendota(self, parsed):
        match, od = parsed
        by_slot = {p["player_slot"]: p for p in od["players"]}
        mismatched = [
            player.player_id
            for player in match.players
            if [(str(e.rune_type), e.game_time_s) for e in player.runes_log]
            != [
                (e["key"], e["time"])
                for e in by_slot[_od_player_slot(player.player_id)]["runes_log"]
            ]
        ]
        assert mismatched == []

    def test_chat_objective_times_match_opendota(self, parsed):
        match, od = parsed
        expected = defaultdict(list)
        for entry in od["objectives"]:
            if entry["type"] in _CHAT_TYPES:
                expected[_objective_key(entry)].append(entry["time"])
        compared = 0
        for entry in match.objectives:
            times = expected.get(_objective_key(entry))
            if entry["type"] in _CHAT_TYPES and times:
                assert entry["time"] == times.pop(0), entry
                compared += 1
        assert compared
