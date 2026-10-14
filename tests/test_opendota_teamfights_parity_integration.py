"""Integration test: ``ParsedMatch.opendota_teamfights`` matches OpenDota.

Parses the shared feature-parity fixture (8855188139) and compares its
OpenDota-shaped teamfights with the OpenDota match API. The replay covers what
HY-87 fixed:

- the game's final fight, which OpenDota never closes and so leaves out;
- ``deaths_pos`` in map cells and ``xp_start`` / ``xp_end`` from the
  once-a-second interval reads.

The stored OpenDota JSON predates odota/parser ``efe5794b`` (August 2026): its
fight at 1847 s counts Ember Spirit's Aegis reincarnation at 1865 s. gem follows
the new rule (HY-178), so that fight has two deaths and is not a teamfight.

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
        before_the_new_rule = [
            f for f in feature_parity_reference["teamfights"] if f["start"] != 1847
        ]
        assert fights == before_the_new_rule

    def test_the_old_rules_extra_fight_holds_a_reincarnation(self, feature_parity_match):
        (reincarnation,) = [
            entry
            for entry in feature_parity_match.combat_log
            if entry.log_type == "DEATH"
            and entry.target_is_hero
            and 1847 <= (entry.game_time_s or 0) <= 1873
            and entry.will_reincarnate
        ]
        assert (reincarnation.target_name, reincarnation.game_time_s) == (
            "npc_dota_hero_ember_spirit",
            1865,
        )

    def test_the_final_fight_stays_in_gems_own_list(self, feature_parity_match):
        last_opendota_end = feature_parity_match.opendota_teamfights[-1].end
        clock = feature_parity_match.game_clock
        assert any(
            clock.game_seconds_at(fight.first_death_tick) > last_opendota_end
            for fight in feature_parity_match.fights
            if fight.deaths >= 3
        )
