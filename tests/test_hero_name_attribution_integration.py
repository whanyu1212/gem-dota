"""Integration test: enemy-hero illusions do not steal combat-log attribution.

Replay 8974053011 has a Dark Seer whose Wall of Replica spawns
``CDOTA_Unit_Hero_<Target>`` illusions carrying Dark Seer's player ID. Combat-log
hero names must still resolve to the real hero's player, as OpenDota's
``name_to_slot`` does (pinned odota/parser ``Parse.java``), so the per-player
combat dicts match OpenDota for every player.

Marked ``slow`` + ``integration``: needs the full ``.dem`` plus its
``.opendota.json``.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPLAY = Path(__file__).parent / "fixtures" / "opendota" / "8974053011.dem"
REFERENCE = REPLAY.with_suffix(".opendota.json")

# Every per-player combat dict keyed off a combat-log hero name.
_NAME_KEYED_FIELDS = (
    "gold_reasons",
    "xp_reasons",
    "damage",
    "damage_taken",
    "damage_inflictor",
    "damage_inflictor_received",
    "damage_targets",
    "healing",
    "ability_uses",
    "ability_targets",
    "hero_hits",
    "killed",
)


def _od_player_slot(player_id: int) -> int:
    return player_id if player_id < 5 else 128 + (player_id - 5)


@pytest.mark.slow
@pytest.mark.integration
class TestEnemyIllusionAttribution:
    @pytest.fixture(scope="class")
    def pairs(self):
        if not REPLAY.exists() or not REFERENCE.exists():
            pytest.skip(
                "Dark Seer illusion fixture is not available; sync match 8974053011 "
                "with scripts/sync_opendota_fixtures.py"
            )
        import gem

        match = gem.parse(REPLAY)
        reference = json.loads(REFERENCE.read_text(encoding="utf-8"))
        by_slot = {p["player_slot"]: p for p in reference["players"]}
        return [(player, by_slot[_od_player_slot(player.player_id)]) for player in match.players]

    @pytest.mark.parametrize("field_name", _NAME_KEYED_FIELDS)
    def test_name_keyed_combat_dicts_match_opendota(self, pairs, field_name):
        mismatched = [
            player.player_id
            for player, od in pairs
            if getattr(player, field_name) != od[field_name]
        ]
        assert mismatched == []
