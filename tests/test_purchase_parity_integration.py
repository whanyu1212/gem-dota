"""Integration test: per-player purchase aggregates match OpenDota.

Parses one full OpenDota fixture and checks that each player's
``ParsedPlayer.purchase`` (per-item count map), ``purchase_time`` (OpenDota's
SUM-of-buy-times quirk), and ``first_purchase_time`` (earliest buy) match the
OpenDota match API for the same hero.

Regression guard for issue #95: gem previously deduped starting-inventory
purchases (under-counting multi-copy consumables) and used last-purchase-wins
for ``purchase_time``. After aligning to OpenDota — starting scan limited to
slots 0-7, no dedup, ``purchase_time`` summed — these match exactly.

HY-80 closed the remaining gaps: starting items are read at OpenDota's first
once-a-second interval and timed by its tick-start clock, ``ward_dispenser`` is
left out of the log and timing maps. The whole purchase timeline now matches,
including pre-horn times. ``first_purchase_time`` keeps a purchase at exactly
0, as OpenDota has since odota/core 7d32aef0; the test applies that rule to
OpenDota's own purchase log, so a fixture JSON from before it compares too.

Marked ``slow`` + ``integration`` — needs a real ``.dem`` plus its
``.opendota.json``.
"""

from __future__ import annotations

import pytest

from gem.catalog.heroes import HEROES

_NAME_TO_HERO_ID = {name: meta["id"] for name, meta in HEROES.items()}

# Per-hero expected purchase counts, verified against the OpenDota fixture.
# Keyed by hero_id (slot-independent so the test is robust to draft order).
_EXPECTED_COUNTS = {
    98: {  # Timbersaw
        "tango": 2,
        "clarity": 3,
        "tpscroll": 5,
        "branches": 2,
        "black_king_bar": 1,
        "recipe_black_king_bar": 1,
    },
    120: {  # Pangolier
        "tango": 1,
        "clarity": 4,
        "tpscroll": 4,
        "branches": 3,
        "ward_observer": 1,
    },
}


@pytest.mark.slow
@pytest.mark.integration
class TestPurchaseParityMatchesOpenDota:
    @pytest.fixture(scope="class")
    def paired(self, feature_parity_reference, feature_parity_match):
        """Pair the shared parsed match with each player's OpenDota blob.

        Returns:
            Dict of ``hero_id -> (ParsedPlayer, opendota_player_dict)``.
        """
        match = feature_parity_match
        od = feature_parity_reference
        od_by_hero = {p["hero_id"]: p for p in od.get("players") or []}

        pairs = {}
        for player in match.players:
            hero_id = _NAME_TO_HERO_ID.get(player.hero_name)
            od_player = od_by_hero.get(hero_id)
            if od_player is not None:
                pairs[hero_id] = (player, od_player)
        return pairs

    def test_all_players_paired(self, paired):
        assert len(paired) == 10

    def test_purchase_counts_match_opendota(self, paired):
        # Every per-item count must match across all 10 players — this is the
        # core #95 parity fix (dedup removal + slot 0-7).
        mismatches = []
        for hero_id, (player, od_player) in paired.items():
            od_counts = od_player.get("purchase") or {}
            for item, count in od_counts.items():
                if player.purchase.get(item, 0) != count:
                    mismatches.append(
                        f"hero {hero_id} {item}: gem={player.purchase.get(item, 0)} od={count}"
                    )
        assert not mismatches, f"purchase count divergence: {mismatches}"

    def test_known_count_oracle(self, paired):
        # Belt-and-braces explicit checks on hand-verified items.
        for hero_id, expected in _EXPECTED_COUNTS.items():
            player, _ = paired[hero_id]
            for item, count in expected.items():
                assert player.purchase.get(item, 0) == count, (
                    f"hero {hero_id} purchase[{item}]={player.purchase.get(item, 0)}, expected {count}"
                )

    def test_purchase_time_is_sum(self, paired):
        # purchase_time matches OpenDota's SUM-of-buy-times on positive-time items.
        # Timbersaw (98): clarity sums to 3076, tpscroll to 6740; BKB single buy 1271.
        timbersaw, _ = paired[98]
        assert timbersaw.purchase_time["clarity"] == 3076
        assert timbersaw.purchase_time["tpscroll"] == 6740
        assert timbersaw.purchase_time["black_king_bar"] == 1271

    def test_first_purchase_time_is_earliest(self, paired):
        # first_purchase_time is the earliest buy. BKB is a clean positive-time
        # single buy (avoids the pre-horn ±1 and tango time-0 quirks).
        timbersaw, _ = paired[98]
        assert timbersaw.first_purchase_time["black_king_bar"] == 1271
        assert timbersaw.first_purchase_time["clarity"] == 705

    def test_recipes_counted_but_excluded_from_timing(self, paired):
        # Recipes appear in the count map but never in the timing maps.
        timbersaw, _ = paired[98]
        assert timbersaw.purchase.get("recipe_black_king_bar") == 1
        assert "recipe_black_king_bar" not in timbersaw.purchase_time
        assert "recipe_black_king_bar" not in timbersaw.first_purchase_time

    def test_purchase_timeline_matches_opendota(self, paired, feature_parity_match):
        # purchase_log (key, time), purchase_time and first_purchase_time match
        # OpenDota for every player, starting items and ward dispensers included.
        from gem.state.game_clock import game_clock_for

        clock = game_clock_for(feature_parity_match)

        def seconds(entry):
            if entry.game_time_s is not None:
                return entry.game_time_s
            return clock.game_seconds_at(entry.tick)

        for hero_id, (player, od_player) in paired.items():
            log = [(e.value_name.removeprefix("item_"), seconds(e)) for e in player.purchase_log]
            assert log == [(e["key"], e["time"]) for e in od_player["purchase_log"]], hero_id
            assert player.purchase_time == od_player["purchase_time"], hero_id
            # The stored JSON predates odota/core 7d32aef0, which keeps a first
            # purchase at 0:00; apply today's rule to OpenDota's own log.
            first_purchase_time: dict[str, int] = {}
            for entry in od_player["purchase_log"]:
                if entry["key"] in od_player["first_purchase_time"]:
                    first_purchase_time.setdefault(entry["key"], entry["time"])
            assert player.first_purchase_time == first_purchase_time, hero_id

    def test_purchase_log_has_no_recipes(self, paired):
        # purchase_log (chronological) excludes recipe_ entries, like OpenDota.
        for _, (player, _) in paired.items():
            assert not any(
                (e.value_name or "").removeprefix("item_").startswith("recipe_")
                for e in player.purchase_log
            )
