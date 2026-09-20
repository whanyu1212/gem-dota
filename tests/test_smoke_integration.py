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

    assert len(match.smoke_events) == 4
    assert sum(len(event.participants) for event in match.smoke_events) == 12
    assert any(
        participant.modifier_duration_s == pytest.approx(45.0)
        for event in match.smoke_events
        for participant in event.participants
    )
    assert all(
        participant.applied_tick >= event.tick
        for event in match.smoke_events
        for participant in event.participants
    )
    assert any(
        participant.applied_tick - event.tick == 82
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
