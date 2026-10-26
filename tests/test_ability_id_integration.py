"""Full-replay check that ``AbilityID_t`` entity fields decode as signed varints.

The neutral craft arrays on the team data entity (``m_vecTrinketChoices``,
``m_vecEnhancementChoices``) are ``AbilityID_t``. The pick each player made,
read through ``m_vecSelectedTrinkets``/``m_vecSelectedEnhancements``, must equal
the IDs ``DOTA_UM_FoundNeutralItem`` reports. Decoded unsigned, they read 2x.

Reference: skadistats/clarity S2DecoderFactory.java (signed ID types such as
``HeroID_t``); see HY-174.
"""

from __future__ import annotations

from collections import Counter

import pytest

from gem.state.entities import Entity

_TEAM_DATA = ("CDOTA_DataRadiant", "CDOTA_DataDire", "CDOTADataRadiant", "CDOTADataDire")
_TIERS = 5
_SLOTS_PER_TIER = 9


def _picks(entity: Entity) -> tuple[Counter[int], Counter[int]]:
    trinkets: Counter[int] = Counter()
    enhancements: Counter[int] = Counter()
    for slot in range(entity.get("m_vecDataTeam") or 0):
        row = f"m_vecDataTeam.{slot:04d}"
        for tier in range(_TIERS):
            for picked, choices, out in (
                ("m_vecSelectedTrinkets", "m_vecTrinketChoices", trinkets),
                ("m_vecSelectedEnhancements", "m_vecEnhancementChoices", enhancements),
            ):
                index = entity.get(f"{row}.{picked}.{tier:04d}")
                if index is None or index < 0:
                    continue
                out[entity.get(f"{row}.{choices}.{tier * _SLOTS_PER_TIER + index:04d}")] += 1
    return trinkets, enhancements


@pytest.mark.integration
@pytest.mark.slow
def test_neutral_craft_picks_match_found_neutral_items(canonical_replay_pass) -> None:
    parser, finds = canonical_replay_pass.parser, canonical_replay_pass.neutral_item_finds
    assert parser.parse_error is None
    assert parser.entity_manager is not None
    team_data = parser.entity_manager.filter(lambda e: e.cls.name.startswith(_TEAM_DATA))

    assert len(team_data) == 2
    assert finds, "fixture has no neutral item finds"
    trinkets: Counter[int] = Counter()
    enhancements: Counter[int] = Counter()
    for entity in team_data:
        t, e = _picks(entity)
        trinkets += t
        enhancements += e

    assert trinkets == Counter(f.item_ability_id for f in finds)
    assert enhancements == Counter(f.enhancement_ability_id for f in finds)
