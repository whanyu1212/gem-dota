"""Offline real-replay coverage for vision-modifier evidence."""

from __future__ import annotations

import pytest

from gem.results.models import (
    ParsedMatch,
    VisionModifierCloseEvidence,
    VisionModifierSemantic,
)


@pytest.mark.integration
@pytest.mark.slow
def test_replay_keeps_gem_as_carrier_evidence(
    patch_742_parsed_match: ParsedMatch,
) -> None:
    # Bristleback carries the Gem of True Sight to the end of the game.
    gem_events = [
        event
        for event in patch_742_parsed_match.vision_modifiers
        if event.modifier_name == "modifier_item_gem_of_true_sight"
    ]

    assert len(gem_events) == 1
    event = gem_events[0]
    assert event.semantic is VisionModifierSemantic.AURA_CARRIER
    assert event.caster_name == event.target_name
    assert event.caster_team == event.target_team
    assert event.end_tick is None


@pytest.mark.integration
@pytest.mark.slow
def test_canonical_replay_preserves_haze_lifecycles_and_ambiguity(
    canonical_parsed_match: ParsedMatch,
) -> None:
    # Slardar plays in the canonical replay.
    match = canonical_parsed_match
    haze_events = [
        event
        for event in match.vision_modifiers
        if event.modifier_name == "modifier_slardar_amplify_damage"
    ]

    assert haze_events
    assert all(
        event.semantic is VisionModifierSemantic.DIRECT_TARGET_REVEAL for event in haze_events
    )
    assert any(event.target_is_hero for event in haze_events)
    assert any(not event.target_is_hero for event in haze_events)
    assert any(
        event.end_tick is not None and event.close_evidence is VisionModifierCloseEvidence.OBSERVED
        for event in haze_events
    )
    assert any(
        issue.reason == "ambiguous" and issue.candidate_add_ticks
        for issue in match.vision_modifier_pairing_issues
    )
