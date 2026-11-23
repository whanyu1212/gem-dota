"""Offline replay regression coverage for Smoke of Deceit lifecycles."""

from __future__ import annotations

import pytest

from gem.analysis.smoke import SmokeLifecycleStatus, build_smoke_analysis
from gem.results.models import ParsedMatch, VisibilityState


@pytest.mark.integration
@pytest.mark.slow
def test_canonical_replay_preserves_smoke_lifecycles(
    canonical_parsed_match: ParsedMatch,
) -> None:
    """Keep the fixture's known smoke activations and per-member timing stable."""
    match = canonical_parsed_match

    assert len(match.smoke_events) == 8
    assert sum(len(event.participants) for event in match.smoke_events) == 23
    # On 7.42 the buff lasts 50 s.
    assert any(
        participant.modifier_duration_s == pytest.approx(50.0)
        for event in match.smoke_events
        for participant in event.participants
    )
    assert all(
        participant.applied_tick >= event.tick
        for event in match.smoke_events
        for participant in event.participants
    )

    analyses = build_smoke_analysis(match)
    members = [member for analysis in analyses for member in analysis.members]

    assert any(member.lifecycle_status is SmokeLifecycleStatus.EXPIRED for member in members)
    early = [member for member in members if member.lifecycle_status is SmokeLifecycleStatus.EARLY]
    assert early
    assert any(member.visibility_at_remove is VisibilityState.HIDDEN for member in early)
    assert any(member.visibility_at_remove is VisibilityState.VISIBLE for member in early)

    # Each smoke's first fight: the first fight whose first death came within
    # 60 in-game seconds of activation. A Radiant and a Dire smoke share fight 13.
    fight_numbers = {id(fight): index for index, fight in enumerate(match.fights)}
    assert [
        fight_numbers[id(analysis.first_fight)] if analysis.first_fight else None
        for analysis in analyses
    ] == [None, None, 6, 9, 13, 13, 15, 29]
    assert analyses[0].activation_tick == match.smoke_events[0].tick == 25_436
    assert analyses[2].activation_tick == 43_768
    assert analyses[2].first_fight is match.fights[6]
    assert match.fights[6].first_death_tick == 44_820


@pytest.mark.integration
@pytest.mark.slow
def test_late_member_gets_the_remaining_duration(feature_parity_match: ParsedMatch) -> None:
    """A hero who gets the buff after activation keeps only what is left of the 50 s."""
    late = [
        (participant.applied_tick - event.tick, participant.modifier_duration_s)
        for event in feature_parity_match.smoke_events
        for participant in event.participants
        if participant.applied_tick > event.tick
    ]
    assert sorted(delay for delay, _ in late) == [32, 76]
    for delay, duration in late:
        assert duration == pytest.approx(50.0 - delay / 30, abs=0.01)
