"""Integration test: the gold ledger and exact buyback costs on real replays.

The team data entity's per-player ledger (``m_vecDataTeam.NNNN.*``) must agree
with the replay's embedded postgame summary, which OpenDota reports:

- items + consumables spent == ``gold_spent``;
- terminal ``gold`` and ``net_worth`` == OpenDota's;
- each buyback's exact cost sums to the ledger's gold spent on buybacks;
- the earned sources minus shared gold == total earned gold.

Fixtures: 8855242704 (16 buybacks), 8856501050 (31 buybacks) and 8855188139,
where the last dense net-worth sample was 1 gold off the summary for one player.

Marked ``slow`` + ``integration``: needs the full ``.dem`` plus its
``.opendota.json``.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "opendota"
_MATCH_IDS = (8855242704, 8856501050, 8855188139)
_EARNED_SOURCES = (
    "hero_kill_gold",
    "creep_kill_gold",
    "neutral_kill_gold",
    "income_gold",
    "building_gold",
    "roshan_gold",
    "bounty_gold",
    "ward_kill_gold",
    "courier_gold",
    "ability_gold",
    "comeback_gold",
    "creep_deny_gold",
    "other_gold",
)


def _od_player_slot(player_id: int) -> int:
    return player_id if player_id < 5 else 128 + (player_id - 5)


@pytest.mark.slow
@pytest.mark.integration
class TestGoldLedgerOnReplays:
    @pytest.fixture(scope="class", params=_MATCH_IDS)
    def pairs(self, request):
        dem = FIXTURES_DIR / f"{request.param}.dem"
        reference = dem.with_suffix(".opendota.json")
        if not dem.exists() or not reference.exists():
            pytest.skip(f"OpenDota fixture {request.param} (.dem + .opendota.json) not available")
        import gem

        match = gem.parse(dem)
        by_slot = {p["player_slot"]: p for p in json.loads(reference.read_text())["players"]}
        return [(player, by_slot[_od_player_slot(player.player_id)]) for player in match.players]

    def test_terminal_gold_scalars_match_opendota(self, pairs):
        mismatches = {
            player.player_id: (
                (player.gold, od["gold"]),
                (player.net_worth, od["net_worth"]),
                (player.gold_spent, od["gold_spent"]),
            )
            for player, od in pairs
            if (player.gold, player.net_worth, player.gold_spent)
            != (od["gold"], od["net_worth"], od["gold_spent"])
        }
        assert mismatches == {}

    def test_ledger_spending_matches_gold_spent(self, pairs):
        for player, _ in pairs:
            final = player.gold_ledger.final
            assert final.spent_on_items + final.spent_on_consumables == player.gold_spent

    def test_earned_sources_sum_to_total_earned(self, pairs):
        for player, _ in pairs:
            final = player.gold_ledger.final
            earned = sum(getattr(final, name) for name in _EARNED_SOURCES)
            assert earned == player.total_earned_gold_t[-1], player.player_id

    def test_every_buyback_cost_is_exact_and_sums_to_the_ledger(self, pairs):
        buybacks = [bb for player, _ in pairs for bb in player.buybacks]
        assert buybacks
        assert all(bb.cost_exact for bb in buybacks)
        for player, _ in pairs:
            assert sum(bb.cost for bb in player.buybacks) == (
                player.gold_ledger.final.spent_on_buybacks
            )

    def test_buyback_splits_add_up(self, pairs):
        for player, _ in pairs:
            for bb in player.buybacks:
                if bb.reliable_gold is not None:
                    assert bb.reliable_gold + bb.unreliable_gold == bb.cost
                    assert min(bb.reliable_gold, bb.unreliable_gold) >= 0

    def test_per_minute_ledger_follows_the_minute_axis(self, pairs):
        for player, _ in pairs:
            per_minute = player.gold_ledger.per_minute
            assert [snap.game_time_s for snap in per_minute] == player.game_times_min
            spent = [snap.spent_on_items for snap in per_minute]
            assert spent == sorted(spent)
