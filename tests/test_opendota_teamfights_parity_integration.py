"""Integration test: ``ParsedMatch.opendota_teamfights`` matches OpenDota.

Parses the shared feature-parity fixture (8855188139) and compares its
OpenDota-shaped teamfights with the OpenDota match API. The replay covers what
HY-87 fixed:

- the fight at 1847 s, whose three deaths include Ember Spirit's reincarnation
  (OpenDota skips only the Aegis holder's death);
- the game's final fight, which OpenDota never closes and so leaves out;
- ``deaths_pos`` in map cells and ``xp_start`` / ``xp_end`` from the
  once-a-second interval reads.

Marked ``slow`` + ``integration``: needs a real ``.dem`` plus its
``.opendota.json``.
"""

from __future__ import annotations

from dataclasses import asdict

import pytest


@pytest.mark.slow
@pytest.mark.integration
class TestOpenDotaTeamfightsMatchOpenDota:
    def test_teamfights_equal_opendota(self, feature_parity_match, feature_parity_reference):
        fights = [asdict(fight) for fight in feature_parity_match.opendota_teamfights]
        assert fights == feature_parity_reference["teamfights"]

    def test_the_final_fight_stays_in_gems_own_list(self, feature_parity_match):
        last_opendota_end = feature_parity_match.opendota_teamfights[-1].end
        clock = feature_parity_match.game_clock
        assert any(
            clock.game_seconds_at(fight.first_death_tick) > last_opendota_end
            for fight in feature_parity_match.fights
            if fight.deaths >= 3
        )
