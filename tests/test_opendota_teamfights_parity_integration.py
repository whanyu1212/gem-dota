"""Integration test: ``ParsedMatch.opendota_teamfights`` matches OpenDota.

Parses the shared feature-parity fixture and compares its OpenDota-shaped
teamfights with the OpenDota match API. The replay covers what HY-87 fixed:

- the game's final fight, which OpenDota never closes and so leaves out;
- ``deaths_pos`` in map cells and ``xp_start`` / ``xp_end`` from the
  once-a-second interval reads.

The stored OpenDota JSON follows odota/parser ``efe5794b`` (August 2026), which
leaves an Aegis reincarnation out of a fight's deaths, as gem does (HY-178);
``test_aegis_reincarnation_integration.py`` covers that rule on two Aegises.

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
