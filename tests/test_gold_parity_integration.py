"""Integration test: per-player current gold and gold spent match OpenDota.

``gold_t`` is current unspent gold, read each sample from the team data entity
as ``m_iReliableGold + m_iUnreliableGold``. ``gold_spent`` comes from the
replay's embedded ``CMsgDOTAMatch`` postgame summary, the same Game Coordinator
record OpenDota reports. The pinned odota/parser ``Parse.java`` reads neither
value; its interval ``gold`` is ``m_iTotalEarnedGold``, which is what
``gold_t_min`` mirrors.

Marked ``slow`` + ``integration`` — needs a real ``.dem`` plus its
``.opendota.json``.
"""

from __future__ import annotations

import pytest

# The last dense sample lands a moment away from the Game Coordinator's
# snapshot, so passive gold can differ by a tick's worth.
_FINAL_GOLD_TOLERANCE = 5


def _od_player_slot(player_id: int) -> int:
    return player_id if player_id < 5 else 128 + (player_id - 5)


@pytest.mark.slow
@pytest.mark.integration
class TestGoldMatchesOpenDota:
    @pytest.fixture(scope="class")
    def pairs(self, feature_parity_reference, feature_parity_match):
        by_slot = {p["player_slot"]: p for p in feature_parity_reference["players"]}
        return [
            (player, by_slot[_od_player_slot(player.player_id)])
            for player in feature_parity_match.players
        ]

    def test_gold_spent_is_exact(self, pairs):
        mismatches = {
            player.player_id: (player.gold_spent, od["gold_spent"])
            for player, od in pairs
            if player.gold_spent != od["gold_spent"]
        }
        assert mismatches == {}

    def test_current_gold_series_is_populated(self, pairs):
        for player, _ in pairs:
            assert any(player.gold_t), f"player {player.player_id} has an all-zero gold_t"
            assert min(player.gold_t) >= 0

    def test_final_current_gold_matches(self, pairs):
        mismatches = {
            player.player_id: (player.gold_t[-1], od["gold"])
            for player, od in pairs
            if abs(player.gold_t[-1] - od["gold"]) > _FINAL_GOLD_TOLERANCE
        }
        assert mismatches == {}

    def test_minute_gold_is_cumulative_earned(self, pairs):
        for player, od in pairs:
            assert player.gold_t_min == od["gold_t"]
