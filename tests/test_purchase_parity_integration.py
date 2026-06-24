"""Integration test: per-player purchase aggregates match OpenDota.

Parses one full OpenDota fixture and checks that each player's
``ParsedPlayer.purchase`` (per-item count map), ``purchase_time`` (OpenDota's
SUM-of-buy-times quirk), and ``first_purchase_time`` (earliest buy) match the
OpenDota match API for the same hero.

Regression guard for issue #95: gem previously deduped starting-inventory
purchases (under-counting multi-copy consumables) and used last-purchase-wins
for ``purchase_time``. After aligning to OpenDota — starting scan limited to
slots 0-7, no dedup, ``purchase_time`` summed — these match exactly.

Assertions avoid two known OpenDota quirks the values must NOT be pinned to:
- pre-horn (negative) timestamps differ by ±1s (boundary quantization), so we
  assert on positive-time items like ``black_king_bar`` instead.
- ``first_purchase_time[tango]`` can skip a time-0 log entry on some players.

Marked ``slow`` + ``integration`` — needs a real ``.dem`` plus its
``.opendota.json``.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import gem
from gem.catalog.heroes import HEROES

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "opendota"
_MATCH_ID = 8855188139

_NAME_TO_HERO_ID = {name: meta["id"] for name, meta in HEROES.items()}

# Per-hero expected purchase counts, verified against the OpenDota fixture.
# Keyed by hero_id (slot-independent so the test is robust to draft order).
_EXPECTED_COUNTS = {
    11: {  # Shadow Fiend
        "tango": 2,
        "faerie_fire": 2,
        "clarity": 5,
        "tpscroll": 2,
        "black_king_bar": 1,
        "recipe_black_king_bar": 1,
    },
    120: {  # Pangolier
        "tango": 2,
        "faerie_fire": 1,
        "clarity": 6,
        "tpscroll": 6,
        "branches": 4,
        "ward_observer": 2,
        "ward_sentry": 2,
    },
}


@pytest.mark.slow
@pytest.mark.integration
class TestPurchaseParityMatchesOpenDota:
    @pytest.fixture(scope="class")
    def paired(self):
        """Parse the fixture once and pair each player with its OpenDota blob.

        Returns:
            Dict of ``hero_id -> (ParsedPlayer, opendota_player_dict)``.
        """
        dem = FIXTURES_DIR / f"{_MATCH_ID}.dem"
        od_path = FIXTURES_DIR / f"{_MATCH_ID}.opendota.json"
        if not dem.exists() or not od_path.exists():
            pytest.skip(f"OpenDota fixture {_MATCH_ID} (.dem + .opendota.json) not available")

        match = gem.parse(str(dem))
        with open(od_path) as fh:
            od = json.load(fh)
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
        # Shadow Fiend (11): clarity sums to 3696, tpscroll to 1377; BKB single buy 1648.
        sf, _ = paired[11]
        assert sf.purchase_time["clarity"] == 3696
        assert sf.purchase_time["tpscroll"] == 1377
        assert sf.purchase_time["black_king_bar"] == 1648

    def test_first_purchase_time_is_earliest(self, paired):
        # first_purchase_time is the earliest buy. BKB is a clean positive-time
        # single buy (avoids the pre-horn ±1 and tango time-0 quirks).
        sf, _ = paired[11]
        assert sf.first_purchase_time["black_king_bar"] == 1648
        assert sf.first_purchase_time["clarity"] == 470

    def test_recipes_counted_but_excluded_from_timing(self, paired):
        # Recipes appear in the count map but never in the timing maps.
        sf, _ = paired[11]
        assert sf.purchase.get("recipe_black_king_bar") == 1
        assert "recipe_black_king_bar" not in sf.purchase_time
        assert "recipe_black_king_bar" not in sf.first_purchase_time

    def test_purchase_log_has_no_recipes(self, paired):
        # purchase_log (chronological) excludes recipe_ entries, like OpenDota.
        for _, (player, _) in paired.items():
            assert not any(
                (e.value_name or "").removeprefix("item_").startswith("recipe_")
                for e in player.purchase_log
            )
