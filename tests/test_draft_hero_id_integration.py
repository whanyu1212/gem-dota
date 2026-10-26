"""Integration test: draft hero IDs are the real hero IDs (HY-176).

``m_BannedHeroes`` and ``m_SelectedHeroes`` are ``HeroID_t``, a zigzag-signed
varint. Decoded unsigned, every ID read 2x, and ``ParsedMatch.draft`` published
the doubled value. OpenDota (Clarity decodes ``HeroID_t`` signed) is the
reference.

Marked ``slow`` + ``integration``: needs the full ``.dem`` plus its
``.opendota.json``.
"""

from __future__ import annotations

import pytest

pytestmark = [pytest.mark.integration, pytest.mark.slow]


def test_draft_hero_ids_match_opendota(fixed8_encoder_match, fixed8_encoder_reference) -> None:
    gem_draft = sorted((event.is_pick, event.hero_id) for event in fixed8_encoder_match.draft)
    opendota_draft = sorted(
        (entry["is_pick"], entry["hero_id"]) for entry in fixed8_encoder_reference["picks_bans"]
    )
    assert gem_draft == opendota_draft
