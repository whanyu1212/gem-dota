"""Integration test: derived kill scalars match OpenDota.

Parses one full OpenDota fixture and checks that each player's derived kill
scalars (ancient/neutral/lane/courier/observer/sentry/roshan kills) match
OpenDota for the same hero.

Marked ``slow`` + ``integration`` — needs a real ``.dem`` plus its
``.opendota.json``.
"""

from __future__ import annotations

import pytest

from gem.catalog.heroes import HEROES

_NAME_TO_HERO_ID = {name: meta["id"] for name, meta in HEROES.items()}

_SCALARS = [
    "ancient_kills",
    "neutral_kills",
    "lane_kills",
    "courier_kills",
    "observer_kills",
    "sentry_kills",
    "roshan_kills",
]


@pytest.mark.slow
@pytest.mark.integration
class TestDerivedKillsMatchOpenDota:
    @pytest.fixture(scope="class")
    def rows(self, feature_parity_reference, feature_parity_match):
        """Pair each player in the shared match with OpenDota by hero.

        Returns:
            List of ``(hero_name, {scalar: (gem, od)})`` tuples.
        """
        match = feature_parity_match
        od = feature_parity_reference
        od_by_hero = {p["hero_id"]: p for p in od.get("players") or []}

        out = []
        for pp in match.players:
            odp = od_by_hero.get(_NAME_TO_HERO_ID.get(pp.hero_name))
            if odp is None:
                continue
            out.append((pp.hero_name, {s: (getattr(pp, s), odp.get(s)) for s in _SCALARS}))
        return out

    def test_all_players_paired(self, rows):
        assert len(rows) == 10

    def test_scalars_match_opendota_for_all_players(self, rows):
        mismatches = {
            hero: {s: v for s, v in scalars.items() if v[0] != v[1]}
            for hero, scalars in rows
            if any(v[0] != v[1] for v in scalars.values())
        }
        assert not mismatches, f"kill scalars diverged from OpenDota: {mismatches}"

    def test_clean_categories_match_all_players(self, rows):
        # courier/observer/sentry kills resolve directly (no summon ambiguity)
        # and should match for every player, summon-heavy heroes included.
        for hero, scalars in rows:
            for s in ("courier_kills", "observer_kills", "sentry_kills"):
                gem_val, od_val = scalars[s]
                assert gem_val == od_val, f"{hero} {s}: gem={gem_val} od={od_val}"
