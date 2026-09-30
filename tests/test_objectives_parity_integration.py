"""Integration test: ``ParsedMatch.objectives`` matches OpenDota.

Parses the shared feature-parity fixture (8855188139) and compares its
objectives with the OpenDota match API. That replay covers every cause HY-86
fixed:

- a hero killed by neutrals before first blood (gem used to call it first
  blood, 240 s instead of 344 s);
- two Tormentor kills whose chat events arrive before their deaths (each used
  to carry the next kill's player);
- courier kills, whose chat event carries the bounty ``value``;
- the Ancient's ``building_kill``, which gem used to leave out.

The reference JSON predates odota/core's read-time ``victim_player_slot``, so
it gets the same annotation the parity audit applies.

Marked ``slow`` + ``integration``: needs a real ``.dem`` plus its
``.opendota.json``.
"""

from __future__ import annotations

import pytest

from scripts.audit_opendota_parity import _annotated_objectives


@pytest.mark.slow
@pytest.mark.integration
class TestObjectivesMatchOpenDota:
    def test_objectives_equal_opendota(self, feature_parity_match, feature_parity_reference):
        assert feature_parity_match.objectives == _annotated_objectives(feature_parity_reference)

    def test_first_blood_is_the_chat_event_kill(self, feature_parity_match):
        (first_blood,) = [
            o for o in feature_parity_match.objectives if o["type"] == "CHAT_MESSAGE_FIRSTBLOOD"
        ]
        assert (first_blood["time"], first_blood["slot"], first_blood["key"]) == (344, 0, "8")

    def test_tormentor_kills_credit_their_own_killer(self, feature_parity_match):
        assert [t.killer_player_id for t in feature_parity_match.tormentors] == [9, 8]
