"""Integration test: ``ParsedMatch.objectives`` matches OpenDota.

Parses the shared feature-parity fixture and compares its objectives with the
OpenDota match API, then checks the causes HY-86 fixed:

- first blood is the chat event's kill (gem once took a hero killed by neutrals
  before it; no fixture has one now, so ``TestFirstBloodDeath`` in
  ``test_opendota_chat_clock.py`` covers that case);
- Tormentor kills whose chat events arrive before their deaths (each used to
  carry the next kill's player), on the long fixture's three Tormentors;
- courier kills, whose chat event carries the bounty ``value``;
- the Ancient's ``building_kill``, which gem used to leave out.

The reference JSON gets the read-time ``victim_player_slot`` annotation the
parity audit applies, for JSON from before odota/core added it.

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
        assert (first_blood["time"], first_blood["slot"], first_blood["key"]) == (137, 1, "7")

    def test_tormentor_kills_credit_their_own_killer(self, long_parsed_match):
        # OpenDota's chat event names no player for the first kill either (slot -1).
        assert [t.killer_player_id for t in long_parsed_match.tormentors] == [-1, 4, 8]
